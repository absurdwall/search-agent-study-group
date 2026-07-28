"""Prepared Orders workshop setup and trace helpers."""

from __future__ import annotations

import os
from getpass import getuser
from pathlib import Path

from dotenv import load_dotenv
from google.adk.agents import Agent
from google.adk.runners import InMemoryRunner
from openinference.instrumentation.google_adk import GoogleADKInstrumentor
from openinference.instrumentation.google_genai import GoogleGenAIInstrumentor
from opentelemetry import trace
from phoenix.otel import register

from tools_order import get_order, list_orders


__all__ = [
    "Agent",
    "GOOGLE_MODEL",
    "InMemoryRunner",
    "PROJECT_NAME",
    "get_order",
    "list_orders",
    "repository_root",
    "run_traced_turn",
]


repository_root = Path(__file__).resolve().parents[1]
if not (repository_root / "notebooks/tools_order.py").is_file():
    raise RuntimeError("The Orders workshop tool files are missing.")

load_dotenv(repository_root / ".env")

PROJECT_NAME = os.getenv("JUPYTERHUB_USER") or getuser()
os.environ["PHOENIX_PROJECT_NAME"] = PROJECT_NAME
os.environ.setdefault("GOOGLE_GENAI_USE_VERTEXAI", "FALSE")
GOOGLE_MODEL = os.getenv("GOOGLE_MODEL", "gemini-3.1-flash-lite")
PHOENIX_COLLECTOR_ENDPOINT = (
    os.getenv("PHOENIX_COLLECTOR_ENDPOINT")
    or os.getenv("PHOENIX_BASE_ENDPOINT")
    or "https://app.phoenix.arize.com/s/adk-demo-search"
)
os.environ["PHOENIX_COLLECTOR_ENDPOINT"] = PHOENIX_COLLECTOR_ENDPOINT

if "_ORDERS_WORKSHOP_TRACER_PROVIDER" not in globals():
    _ORDERS_WORKSHOP_TRACER_PROVIDER = register(
        project_name=PROJECT_NAME,
        batch=True,
        protocol="http/protobuf",
        verbose=False,
    )
    GoogleGenAIInstrumentor().instrument(
        tracer_provider=_ORDERS_WORKSHOP_TRACER_PROVIDER
    )
    GoogleADKInstrumentor().instrument(
        tracer_provider=_ORDERS_WORKSHOP_TRACER_PROVIDER
    )

tracer_provider = _ORDERS_WORKSHOP_TRACER_PROVIDER
workshop_tracer = trace.get_tracer("orders-agent-workshop")


async def run_traced_turn(*, trace_name, runner, prompt, session_id):
    try:
        with workshop_tracer.start_as_current_span(trace_name):
            result = await runner.run_debug(
                prompt,
                session_id=session_id,
                verbose=True,
            )
    except Exception:
        try:
            tracer_provider.force_flush()
        except Exception:
            pass
        raise
    if not tracer_provider.force_flush():
        raise RuntimeError("Phoenix telemetry did not flush before the timeout.")
    return result


print(
    f"Model: {GOOGLE_MODEL}\n"
    f"Phoenix project: {PROJECT_NAME}\n"
    "Orders API: ready\n"
    "Tracing: ready"
)
