"""Phoenix and ADK session plumbing kept out of teaching cells."""

from __future__ import annotations

import os
import warnings
from contextlib import ExitStack, redirect_stderr, redirect_stdout
from dataclasses import dataclass
from getpass import getuser
from io import StringIO
from pathlib import Path
from time import perf_counter
from uuid import uuid4

from google.adk.runners import InMemoryRunner

from .environment import EnvironmentStatus, load_workshop_env


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
MODEL = os.getenv("GOOGLE_MODEL", "gemini-3.1-flash-lite")


@dataclass
class WorkshopRuntime:
    app_name: str
    project_name: str
    tracer_provider: object
    phoenix_url: str
    environment: EnvironmentStatus | None = None


@dataclass(frozen=True)
class RunResult:
    answer: str
    session_id: str
    trace_url: str | None = None
    model_calls: int | None = None
    tool_calls: int | None = None
    tool_names: tuple[str, ...] = ()
    tool_arguments: tuple[dict[str, object], ...] = ()
    tokens: int | None = None
    latency_seconds: float | None = None


_runtime_state: WorkshopRuntime | None = None


def _quiet_teaching_warnings() -> None:
    """Hide dependency experiments that do not require learner action."""

    warnings.filterwarnings("ignore", category=UserWarning, module=r"google\..*")


def setup_workshop(app_name: str) -> WorkshopRuntime:
    """Load settings and enable Phoenix tracing once for this kernel."""

    global _runtime_state
    if _runtime_state is not None:
        return _runtime_state

    _quiet_teaching_warnings()
    environment = load_workshop_env(repository_root=REPOSITORY_ROOT)
    project_name = os.getenv("JUPYTERHUB_USER") or getuser()
    collector = os.getenv(
        "PHOENIX_COLLECTOR_ENDPOINT",
        "https://app.phoenix.arize.com/s/adk-demo-search",
    )
    os.environ["PHOENIX_PROJECT_NAME"] = project_name
    os.environ["PHOENIX_COLLECTOR_ENDPOINT"] = collector
    os.environ.setdefault("GOOGLE_GENAI_USE_VERTEXAI", "FALSE")

    from openinference.instrumentation.google_adk import GoogleADKInstrumentor
    from openinference.instrumentation.google_genai import GoogleGenAIInstrumentor
    from phoenix.otel import register

    tracer_provider = register(
        project_name=project_name,
        batch=True,
        protocol="http/protobuf",
        verbose=False,
    )
    GoogleGenAIInstrumentor().instrument(tracer_provider=tracer_provider)
    GoogleADKInstrumentor().instrument(tracer_provider=tracer_provider)
    _runtime_state = WorkshopRuntime(
        app_name=app_name,
        project_name=project_name,
        tracer_provider=tracer_provider,
        phoenix_url=os.getenv("PHOENIX_UI_URL", collector),
        environment=environment,
    )
    print("✅ Workshop ready · Gemini configured · Phoenix tracing enabled")
    return _runtime_state


def _final_text(events) -> str:
    for event in reversed(events or []):
        content = getattr(event, "content", None)
        for part in reversed(getattr(content, "parts", None) or []):
            text = getattr(part, "text", None)
            if text:
                return text
    return "The agent finished without a text response. Please inspect the trace."


def _display_trace_link(url: str) -> None:
    try:
        from IPython.display import Markdown, display
    except ImportError:
        print(f"🔎 Phoenix trace: {url}")
        return
    display(Markdown(f"🔎 [Open this exact trace in Phoenix]({url})"))


async def run_agent(
    agent,
    prompt: str,
    *,
    session_id: str | None = None,
    trace_name: str | None = None,
) -> RunResult:
    """Run one clean ADK turn and return only learner-useful information."""

    runtime = _runtime_state or setup_workshop("adk-workshop")
    selected_session = session_id or f"lesson-{uuid4().hex[:8]}"
    runner = InMemoryRunner(agent=agent, app_name=trace_name or runtime.app_name)
    started = perf_counter()
    trace_url = runtime.phoenix_url
    trace_failed = False
    events_completed = False
    events = None
    try:
        with ExitStack() as stack:
            try:
                tracer = runtime.tracer_provider.get_tracer("adk-workshop")
                trace_span = stack.enter_context(
                    tracer.start_as_current_span(trace_name or runtime.app_name)
                )
            except Exception:
                trace_span = None

            with (
                redirect_stdout(StringIO()),
                redirect_stderr(StringIO()),
                warnings.catch_warnings(),
            ):
                warnings.simplefilter("ignore")
                if trace_span is not None:
                    try:
                        trace_span.set_attribute("openinference.span.kind", "CHAIN")
                        trace_span.set_attribute("session.id", selected_session)
                    except Exception:
                        trace_failed = True
                        trace_url = runtime.phoenix_url
                events = await runner.run_debug(
                    prompt,
                    session_id=selected_session,
                    verbose=False,
                )
                events_completed = True
            if trace_span is not None and not trace_failed:
                try:
                    trace_id = format(trace_span.get_span_context().trace_id, "032x")
                    trace_url = (
                        f"{runtime.phoenix_url.rstrip('/')}/redirects/traces/{trace_id}"
                    )
                except Exception:
                    trace_failed = True
                    trace_url = runtime.phoenix_url
    except Exception:
        if not events_completed:
            raise
        trace_failed = True
        trace_url = runtime.phoenix_url
    latency = perf_counter() - started
    try:
        if not runtime.tracer_provider.force_flush():
            trace_failed = True
            trace_url = runtime.phoenix_url
    except Exception:
        trace_failed = True
        trace_url = runtime.phoenix_url
    answer = _final_text(events)
    usage = [
        getattr(event, "usage_metadata", None)
        for event in events or []
        if getattr(event, "usage_metadata", None) is not None
    ]
    token_counts = [
        getattr(item, "total_token_count", None)
        for item in usage
        if getattr(item, "total_token_count", None) is not None
    ]
    tool_invocations = tuple(
        (function_call.name, dict(function_call.args or {}))
        for event in events or []
        for part in (getattr(getattr(event, "content", None), "parts", None) or [])
        if (function_call := getattr(part, "function_call", None)) is not None
    )
    tool_names = tuple(name for name, _ in tool_invocations)
    tool_arguments = tuple(arguments for _, arguments in tool_invocations)
    print(answer)
    try:
        _display_trace_link(trace_url)
    except Exception:
        trace_url = runtime.phoenix_url
        print(f"🔎 Phoenix trace: {trace_url}")
    return RunResult(
        answer=answer,
        session_id=selected_session,
        trace_url=trace_url,
        model_calls=len(usage),
        tool_calls=len(tool_names),
        tool_names=tool_names,
        tool_arguments=tool_arguments,
        tokens=sum(token_counts) if token_counts else None,
        latency_seconds=round(latency, 2),
    )
