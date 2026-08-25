"""Lean FastAPI composition for the ecommerce teaching service."""

from contextlib import asynccontextmanager
from datetime import date

from fastapi import FastAPI, Path, Query, Response

from animal_facts_service import AnimalFact, AnimalFactsService
from code_mode_mcp_server import create_ecommerce_code_mode_server
from config import settings
from firestore_store import FirestoreStore
from mcp_server import CanonicalMcpPath, create_mcp_server
from orders_service import OrdersService
from product_service import ProductService


store = FirestoreStore(settings)
products = ProductService(settings, store)
orders = OrdersService()
animal_facts = AnimalFactsService()
mcp = create_mcp_server(products, orders, animal_facts)
ecommerce_code_mcp = create_ecommerce_code_mode_server(products, orders)
ecommerce_code_mcp_app = ecommerce_code_mcp.http_app(
    path="/",
    json_response=True,
    stateless_http=True,
    host_origin_protection=False,
)


@asynccontextmanager
async def lifespan(_: FastAPI):
    async with mcp.session_manager.run():
        async with ecommerce_code_mcp_app.router.lifespan_context(
            ecommerce_code_mcp_app
        ):
            yield


app = FastAPI(
    title="Ecommerce Teaching Demo API",
    version="1.0.0",
    description="Public teaching API with cached catalog products and fake orders.",
    lifespan=lifespan,
)


async def add_product_headers(response: Response, cached: bool) -> None:
    limit, used = await store.quota_state()
    response.headers.update(
        {
            "X-Cache": "HIT" if cached else "MISS",
            "X-Quota-Limit": str(limit),
            "X-Quota-Used": str(used),
            "X-Quota-Remaining": str(max(limit - used, 0)),
        }
    )


@app.get("/v1/products/search")
async def search_products(
    response: Response, q: str = Query(min_length=1, max_length=120)
):
    result = await products.search(q)
    await add_product_headers(response, result["cached"])
    return result


@app.get("/v1/animal-facts/random", response_model=AnimalFact)
def get_random_animal_fact():
    return animal_facts.random_fact()


@app.get("/v1/products/{product_id}")
async def get_product(
    response: Response, product_id: str = Path(pattern=r"^[0-9]{1,32}$")
):
    result = await products.get(product_id)
    await add_product_headers(response, result["cached"])
    return result


@app.get("/v1/orders")
def list_orders(start_date: date | None = None, end_date: date | None = None):
    return orders.list(start_date, end_date)


@app.get("/v1/orders/{order_id}")
def get_order(order_id: str):
    return orders.get(order_id)


@app.get("/health", include_in_schema=False)
def health():
    return {"status": "ok"}


app.add_route("/mcp", CanonicalMcpPath(mcp.streamable_http_app()), methods=["POST"])
app.add_route(
    "/mcp-code",
    CanonicalMcpPath(ecommerce_code_mcp_app),
    methods=["POST"],
)
