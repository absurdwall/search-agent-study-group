"""Small, friendly interface shared by the ADK workshop notebooks."""

from pathlib import Path

from .display import show_comparison, show_json, show_skill, show_source, show_text
from .mcp import close_mcp_tools, order_code_from_mcp, order_tools_from_mcp
from .runtime import MODEL, RunResult, WorkshopRuntime, run_agent, setup_workshop
from .tools import get_order, get_store_hours, list_orders


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
ORDER_SKILL = REPOSITORY_ROOT / "skills" / "order-support" / "SKILL.md"
STORE_SKILL = REPOSITORY_ROOT / "skills" / "store-information" / "SKILL.md"

__all__ = [
    "MODEL",
    "ORDER_SKILL",
    "STORE_SKILL",
    "RunResult",
    "WorkshopRuntime",
    "close_mcp_tools",
    "get_order",
    "get_store_hours",
    "list_orders",
    "order_code_from_mcp",
    "order_tools_from_mcp",
    "run_agent",
    "setup_workshop",
    "show_comparison",
    "show_json",
    "show_skill",
    "show_source",
    "show_text",
]
