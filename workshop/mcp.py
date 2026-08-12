"""Small MCP constructors whose real source can be shown in the notebooks."""

from __future__ import annotations

import os
from typing import Any


MCP_ENDPOINT = os.getenv(
    "MCP_ENDPOINT",
    "https://walmart-demo-api-k2yx3oubha-ue.a.run.app/mcp",
)
MCP_CODE_ENDPOINT = os.getenv(
    "MCP_CODE_ENDPOINT",
    MCP_ENDPOINT.removesuffix("/mcp") + "/mcp-code",
)

_active_toolsets: list[Any] = []


def order_tools_from_mcp():
    """Connect to only the two Order tools published by the MCP server."""

    from google.adk.tools.mcp_tool import (
        McpToolset,
        StreamableHTTPConnectionParams,
    )

    toolset = McpToolset(
        connection_params=StreamableHTTPConnectionParams(url=MCP_ENDPOINT),
        tool_filter=["list_orders", "get_order"],
    )
    _active_toolsets.append(toolset)
    return toolset


def order_code_from_mcp():
    """Discover detailed Order schemas, then run one bounded program."""

    from google.adk.tools.mcp_tool import (
        McpToolset,
        StreamableHTTPConnectionParams,
    )

    toolset = McpToolset(
        connection_params=StreamableHTTPConnectionParams(url=MCP_CODE_ENDPOINT),
        tool_filter=["search", "execute"],
    )
    _active_toolsets.append(toolset)
    return toolset


async def close_mcp_tools() -> None:
    """Close toolsets created by this kernel and forget them."""

    toolsets = list(dict.fromkeys(_active_toolsets))
    _active_toolsets.clear()
    for toolset in toolsets:
        await toolset.close()
