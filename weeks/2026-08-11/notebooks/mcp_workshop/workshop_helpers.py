"""Prepared environment and tracing helpers for the MCP workshop notebooks."""

from __future__ import annotations

import os
from getpass import getuser
from importlib.metadata import PackageNotFoundError
from importlib.metadata import version
from pathlib import Path
from typing import TYPE_CHECKING, Any

from google.adk.agents import Agent
from google.adk.runners import InMemoryRunner
from google.adk.skills import load_skill_from_dir
from google.adk.skills.models import Skill
from google.adk.tools.skill_toolset import SkillToolset
from openinference.instrumentation.google_adk import GoogleADKInstrumentor
from openinference.instrumentation.google_genai import GoogleGenAIInstrumentor
from opentelemetry import trace
from phoenix.otel import register

from .env import load_workshop_env

if TYPE_CHECKING:
    from google.adk.tools.mcp_tool.mcp_session_manager import (
        StreamableHTTPConnectionParams as StreamableHTTPConnectionParams,
    )
    from google.adk.tools.mcp_tool.mcp_toolset import McpToolset as McpToolset
else:
    McpToolset = None
    StreamableHTTPConnectionParams = None


__all__ = [
    "Agent",
    "ENV_FILE",
    "GOOGLE_MODEL",
    "InMemoryRunner",
    "MCP_ENDPOINT",
    "PRODUCT_CODE_MCP_ENDPOINT",
    "PRODUCT_SYSTEM_INSTRUCTIONS",
    "PROJECT_NAME",
    "close_workshop_tools",
    "close_product_skill_tools",
    "load_order_code_tools",
    "load_order_mcp_tools",
    "load_order_skill",
    "load_order_skill_tools",
    "load_product_mcp_tools",
    "load_product_skill_tools",
    "load_store_skill",
    "make_order_agent",
    "make_workshop_runner",
    "make_product_runner",
    "repository_root",
    "run_traced_turn",
    "skill_preview_markdown",
    "tracer_provider",
]


repository_root = Path(__file__).resolve().parents[2]
if not (repository_root / "skills" / "order-support" / "SKILL.md").is_file():
    raise RuntimeError("The MCP workshop repository files are missing.")

ENV_FILE = load_workshop_env(repository_root=repository_root)

PROJECT_NAME = os.getenv("JUPYTERHUB_USER") or getuser()
GOOGLE_MODEL = os.getenv("GOOGLE_MODEL", "gemini-3.1-flash-lite")
MCP_ENDPOINT = "https://walmart-demo-api-k2yx3oubha-ue.a.run.app/mcp"
PRODUCT_CODE_MCP_ENDPOINT = MCP_ENDPOINT.removesuffix("/mcp") + "/mcp-code"
PRODUCT_SYSTEM_INSTRUCTIONS = (
    "Use the supplied product shopping skill for every product request. "
    "Call search_products first, preserve returned product IDs exactly, "
    "then call product_details to retrieve full details before comparing "
    "products. Identify missing data and never invent facts."
)
ORDER_SYSTEM_INSTRUCTIONS = (
    "Answer only from the supplied synthetic order tools. Convert the user's "
    "requested period into inclusive YYYY-MM-DD dates, call list_orders first, "
    "select an order ID only from its returned summaries, and call get_order "
    "before reporting status, totals, item names, or quantities. State missing "
    "fields and tool errors plainly; never invent order facts."
)

ORDER_TOOL_FILTER = ["list_orders", "get_order"]
PRODUCT_TOOL_FILTER = ["search_products", "product_details"]
CODE_TOOL_FILTER = ["execute"]

os.environ["PHOENIX_PROJECT_NAME"] = PROJECT_NAME
os.environ.setdefault("GOOGLE_GENAI_USE_VERTEXAI", "FALSE")
os.environ.setdefault(
    "PHOENIX_COLLECTOR_ENDPOINT",
    "https://app.phoenix.arize.com/s/adk-demo-search",
)

if "_MCP_WORKSHOP_TRACER_PROVIDER" not in globals():
    _MCP_WORKSHOP_TRACER_PROVIDER = register(
        project_name=PROJECT_NAME,
        batch=True,
        protocol="http/protobuf",
        verbose=False,
    )
    GoogleGenAIInstrumentor().instrument(
        tracer_provider=_MCP_WORKSHOP_TRACER_PROVIDER
    )
    GoogleADKInstrumentor().instrument(
        tracer_provider=_MCP_WORKSHOP_TRACER_PROVIDER
    )

tracer_provider = _MCP_WORKSHOP_TRACER_PROVIDER
workshop_tracer = trace.get_tracer("mcp-skill-subagent-workshop")

if "_order_mcp_toolset" not in globals():
    _order_mcp_toolset = None
if "_product_mcp_toolset" not in globals():
    _product_mcp_toolset = None
if "_code_mcp_toolset" not in globals():
    _code_mcp_toolset = None
if "_order_code_mcp_toolset" not in globals():
    _order_code_mcp_toolset = None
if "_product_code_mcp_toolset" not in globals():
    _product_code_mcp_toolset = None
if "_mcp_tool_import_error" not in globals():
    _mcp_tool_import_error = None


def _resolve_mcp_tool_runtime() -> tuple[Any, Any]:
    """Resolve the ADK MCP tool classes lazily for testability and compatibility."""

    global McpToolset, StreamableHTTPConnectionParams, _mcp_tool_import_error
    if McpToolset is not None and StreamableHTTPConnectionParams is not None:
        return McpToolset, StreamableHTTPConnectionParams

    try:
        from google.adk.tools.mcp_tool import (
            McpToolset as imported_toolset,
            StreamableHTTPConnectionParams as imported_connection_params,
        )
    except Exception as import_error:
        try:
            from google.adk.tools.mcp_tool.mcp_session_manager import (
                StreamableHTTPConnectionParams as imported_connection_params,
            )
            from google.adk.tools.mcp_tool.mcp_toolset import (
                McpToolset as imported_toolset,
            )
        except Exception as fallback_error:
            _mcp_tool_import_error = fallback_error
            raise RuntimeError(
                "MCP workshop helpers require google-adk MCP tool support to "
                "load direct or Code Mode toolsets. Install the workshop MCP "
                f"dependencies before calling this helper (google-adk "
                f"{version('google-adk')})."
            ) from fallback_error
        _mcp_tool_import_error = import_error
    else:
        _mcp_tool_import_error = None

    McpToolset = imported_toolset
    StreamableHTTPConnectionParams = imported_connection_params
    return McpToolset, StreamableHTTPConnectionParams


def _make_mcp_toolset(*, url: str, tool_filter: list[str]) -> Any:
    """Build one MCP toolset using the resolved runtime classes."""

    mcp_toolset_cls, connection_params_cls = _resolve_mcp_tool_runtime()
    return mcp_toolset_cls(
        connection_params=connection_params_cls(url=url),
        tool_filter=tool_filter,
    )


def _distribution_version(package_name: str) -> str:
    """Return a best-effort package version for import-time diagnostics."""

    try:
        return version(package_name)
    except PackageNotFoundError:
        return "unavailable"


def load_order_mcp_tools() -> McpToolset:
    """Load the direct Order MCP tools from the public MCP endpoint."""

    global _order_mcp_toolset
    if _order_mcp_toolset is None:
        _order_mcp_toolset = _make_mcp_toolset(
            url=MCP_ENDPOINT,
            tool_filter=ORDER_TOOL_FILTER,
        )
    return _order_mcp_toolset


def load_product_mcp_tools() -> McpToolset:
    """Load the direct Product MCP tools from the public MCP endpoint."""

    global _product_mcp_toolset
    if _product_mcp_toolset is None:
        _product_mcp_toolset = _make_mcp_toolset(
            url=MCP_ENDPOINT,
            tool_filter=PRODUCT_TOOL_FILTER,
        )
    return _product_mcp_toolset


def load_order_code_tools() -> McpToolset:
    """Load the single prepared Code Mode tool from its endpoint."""

    global _code_mcp_toolset, _order_code_mcp_toolset, _product_code_mcp_toolset
    if _code_mcp_toolset is None:
        _code_mcp_toolset = _make_mcp_toolset(
            url=PRODUCT_CODE_MCP_ENDPOINT,
            tool_filter=CODE_TOOL_FILTER,
        )
    _order_code_mcp_toolset = _code_mcp_toolset
    _product_code_mcp_toolset = _code_mcp_toolset
    return _code_mcp_toolset


def _skill_tool_names(skill) -> list[str]:
    frontmatter = getattr(skill, "frontmatter", None)
    metadata = getattr(frontmatter, "metadata", {})
    declared = metadata.get("adk_additional_tools", [])
    return declared if isinstance(declared, list) else []


def load_product_skill_tools(skill_dir: Path) -> SkillToolset:
    """Load a Product Skill with only the MCP tools it declares."""

    skill = load_skill_from_dir(skill_dir)
    if "execute" in _skill_tool_names(skill):
        additional_tools = [load_order_code_tools()]
    else:
        additional_tools = [load_product_mcp_tools()]
    return SkillToolset(
        skills=[skill],
        additional_tools=additional_tools,
    )


def load_order_skill() -> Skill:
    """Load the completed instructor Order Skill."""

    return load_skill_from_dir(repository_root / "skills" / "order-support")


def load_store_skill() -> Skill:
    """Load the completed instructor Store Skill."""

    return load_skill_from_dir(repository_root / "skills" / "store-information")


def skill_preview_markdown(skill_dir: Path) -> str:
    """Return learner-friendly Skill Markdown without YAML frontmatter."""

    skill = load_skill_from_dir(skill_dir)
    title = skill.frontmatter.name.replace("-", " ").title()
    return (
        f"## {title}\n\n"
        f"**When to use:** {skill.frontmatter.description}\n\n"
        f"{skill.instructions.strip()}"
    )


def load_order_skill_tools() -> SkillToolset:
    """Load the completed Order Skill with its direct Order tools."""

    return SkillToolset(
        skills=[load_order_skill()],
        additional_tools=[load_order_mcp_tools()],
    )


def make_order_agent() -> Agent:
    """Build the completed single-turn Order specialist."""

    return Agent(
        name="order_agent",
        model=GOOGLE_MODEL,
        mode="single_turn",
        instruction=ORDER_SYSTEM_INSTRUCTIONS,
        tools=[load_order_mcp_tools()],
    )


def make_workshop_runner(agent: Agent, app_name: str) -> InMemoryRunner:
    """Create an in-memory runner for a workshop agent."""

    return InMemoryRunner(agent=agent, app_name=app_name)


def make_product_runner(agent: Agent) -> InMemoryRunner:
    """Backward-compatible runner for the deferred Product notebook."""

    return make_workshop_runner(agent, "product_code_mode_takehome")


async def close_workshop_tools() -> None:
    """Close each shared workshop toolset once and reset all caches."""

    global _order_mcp_toolset, _product_mcp_toolset, _code_mcp_toolset
    global _order_code_mcp_toolset, _product_code_mcp_toolset
    toolsets = (
        _order_mcp_toolset,
        _product_mcp_toolset,
        _code_mcp_toolset,
        _order_code_mcp_toolset,
        _product_code_mcp_toolset,
    )
    _order_mcp_toolset = None
    _product_mcp_toolset = None
    _code_mcp_toolset = None
    _order_code_mcp_toolset = None
    _product_code_mcp_toolset = None

    closed_ids: set[int] = set()
    close_errors: list[BaseException] = []
    for toolset in toolsets:
        if toolset is None or id(toolset) in closed_ids:
            continue
        closed_ids.add(id(toolset))
        try:
            await toolset.close()
        except BaseException as error:
            close_errors.append(error)

    if close_errors:
        raise close_errors[0]


async def close_product_skill_tools() -> None:
    """Backward-compatible cleanup for the deferred Product notebook."""

    await close_workshop_tools()


async def run_traced_turn(*, trace_name, runner, prompt, session_id):
    """Run one ADK debug turn inside a named span and flush it to Phoenix."""

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
    f"ADK {_distribution_version('google-adk')} | "
    f"MCP {_distribution_version('mcp')} | "
    f"model={GOOGLE_MODEL} | Phoenix project={PROJECT_NAME}"
)
