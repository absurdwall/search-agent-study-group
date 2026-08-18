"""Standard FastMCP Code Mode surface for the ecommerce workshop."""

import asyncio
from datetime import date
from typing import Annotated, Any, Callable

from fastmcp import FastMCP
from fastmcp.experimental.transforms.code_mode import (
    CodeMode,
    MontySandboxProvider,
    Search,
)
from pydantic import Field

from mcp_server import (
    OrderDetail,
    OrderSummary,
    ProductDetail,
    ProductSearchResult,
)
from orders_service import OrdersService
from product_service import ProductService


EXECUTION_TIMEOUT_SECONDS = 10.0
MAX_MEMORY_BYTES = 50_000_000
MAX_TOOL_CALLS = 6


class TimeoutSandboxProvider:
    """Apply a wall-clock timeout around an otherwise standard sandbox."""

    def __init__(self, sandbox: MontySandboxProvider, timeout_seconds: float) -> None:
        self.sandbox = sandbox
        self.timeout_seconds = timeout_seconds

    async def run(
        self,
        code: str,
        *,
        inputs: dict[str, Any] | None = None,
        external_functions: dict[str, Callable[..., Any]] | None = None,
    ) -> Any:
        async with asyncio.timeout(self.timeout_seconds):
            return await self.sandbox.run(
                code,
                inputs=inputs,
                external_functions=external_functions,
            )


def create_ecommerce_code_mode_server(
    products: ProductService,
    orders: OrdersService,
) -> FastMCP:
    """Create standard Code Mode over the registered ecommerce tools."""

    sandbox = MontySandboxProvider(
        limits={
            "max_duration_secs": EXECUTION_TIMEOUT_SECONDS,
            "max_memory": MAX_MEMORY_BYTES,
        }
    )
    code_mode = CodeMode(
        sandbox_provider=TimeoutSandboxProvider(
            sandbox,
            timeout_seconds=EXECUTION_TIMEOUT_SECONDS,
        ),
        discovery_tools=[Search(default_detail="detailed")],
        max_tool_calls=MAX_TOOL_CALLS,
    )
    server = FastMCP(
        "Ecommerce Teaching Demo Code Mode",
        transforms=[code_mode],
        mask_error_details=True,
    )

    @server.tool(tags={"products"})
    async def search_products(
        query: Annotated[
            str,
            Field(description="Natural-language keywords describing products to find."),
        ],
    ) -> ProductSearchResult:
        """Search products and return matching catalog summaries."""
        return await products.search(query)

    @server.tool(tags={"products"})
    async def product_details(
        product_id: Annotated[
            str,
            Field(description="Catalog product ID returned by product search."),
        ],
    ) -> ProductDetail:
        """Retrieve full details for one catalog product ID."""
        return await products.get(product_id)

    @server.tool(tags={"orders"})
    def list_orders(
        start_date: Annotated[
            date | None,
            Field(description="Optional inclusive start date in YYYY-MM-DD format."),
        ] = None,
        end_date: Annotated[
            date | None,
            Field(description="Optional inclusive end date in YYYY-MM-DD format."),
        ] = None,
    ) -> list[OrderSummary]:
        """List ecommerce shopping-order summaries for an inclusive date range."""
        return orders.list(start_date, end_date)

    @server.tool(tags={"orders"})
    def get_order(
        order_id: Annotated[
            str,
            Field(description="Ecommerce order ID returned by list_orders."),
        ],
    ) -> OrderDetail:
        """Retrieve the full ecommerce record for one order ID."""
        return orders.get(order_id)

    return server
