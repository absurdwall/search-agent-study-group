"""MCP tools backed by the same product and order services as REST."""

from datetime import date
from typing import Annotated, TypedDict

from mcp.server.fastmcp import FastMCP
from mcp.server.transport_security import TransportSecuritySettings
from pydantic import Field

from animal_facts_service import AnimalFact, AnimalFactsService
from orders_service import OrdersService
from product_service import ProductService


class ProductSummary(TypedDict):
    product_id: str
    name: str
    price: float | None
    currency: str
    image_url: str | None
    url: str | None
    rating: float | None
    review_count: int | str | None


class ProductSearchResult(TypedDict):
    query: str
    count: int
    cached: bool
    products: list[ProductSummary]


class ProductDetail(TypedDict):
    product_id: str
    name: str
    url: str | None
    price: float | None
    currency: str
    availability: str | None
    seller: str | None
    brand: str | None
    description: str | None
    images: list[str]
    category_path: list[object]
    rating: float | None
    review_count: int | str | None
    specifications: dict[str, object]
    cached: bool


class OrderSummary(TypedDict):
    order_id: str
    order_date: str
    status: str
    total: str
    currency: str
    item_count: int


class OrderItem(TypedDict):
    product_id: str
    name: str
    unit_price: str
    quantity: int
    subtotal: str
    currency: str
    image_url: str


class ShippingAddress(TypedDict):
    name: str
    street: str
    city: str
    state: str
    postal_code: str
    country: str


class OrderDetail(OrderSummary):
    items: list[OrderItem]
    shipping_address: ShippingAddress


def create_mcp_server(
    products: ProductService,
    orders: OrdersService,
    animal_facts: AnimalFactsService,
) -> FastMCP:
    mcp = FastMCP(
        "Ecommerce Teaching Demo",
        stateless_http=True,
        json_response=True,
        transport_security=TransportSecuritySettings(
            enable_dns_rebinding_protection=False
        ),
    )
    mcp.settings.streamable_http_path = "/"

    @mcp.tool()
    async def search_products(
        query: Annotated[
            str,
            Field(description="Natural-language keywords describing products to find."),
        ],
    ) -> ProductSearchResult:
        """Search for products first; retry with broader keywords if no matches appear."""
        return await products.search(query)

    @mcp.tool()
    async def product_details(
        product_id: Annotated[
            str,
            Field(description="Catalog product ID returned by search results."),
        ],
    ) -> ProductDetail:
        """Fetch full product details after search; search again if the item is not found."""
        return await products.get(product_id)

    @mcp.tool()
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
        """List ecommerce shopping orders for inclusive dates; omitted dates use 30 days."""
        return orders.list(start_date, end_date)

    @mcp.tool()
    def get_order(
        order_id: Annotated[
            str,
            Field(description="Demo order ID shaped like WM-DEMO-1001; list orders to recover IDs."),
        ],
    ) -> OrderDetail:
        """Fetch one ecommerce shopping order; list orders if the ID is unknown."""
        return orders.get(order_id)

    @mcp.tool()
    def get_random_animal_fact() -> AnimalFact:
        """Return one randomly selected fact from the bundled animal dataset."""
        return animal_facts.random_fact()

    return mcp


class CanonicalMcpPath:
    """Map public `/mcp` to FastMCP's internal root route."""

    def __init__(self, child):
        self.child = child

    async def __call__(self, scope, receive, send):
        scope = {**scope, "path": "/", "raw_path": b"/"}
        await self.child(scope, receive, send)
