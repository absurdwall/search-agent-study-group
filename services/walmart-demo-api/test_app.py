from contextlib import asynccontextmanager
from fnmatch import fnmatch
import asyncio
from datetime import date
import json
import os
from pathlib import Path
import shlex
import subprocess

import app as service
import code_mode_mcp_server as code_mode_service
import httpx
import pytest
from fastapi import FastAPI
from firestore_store import FirestoreStore
from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client
from mcp_server import CanonicalMcpPath, create_mcp_server


class DeterministicProductService:
    def __init__(self):
        self.calls = []

    async def search(self, query):
        self.calls.append(("search", query))
        return {
            "query": query,
            "count": 2,
            "cached": True,
            "products": [
                {"product_id": "111", "name": "Alpha TV"},
                {"product_id": "222", "name": "Beta TV"},
            ],
        }

    async def get(self, product_id):
        self.calls.append(("get", product_id))
        return {
            "product_id": product_id,
            "name": "Alpha TV" if product_id == "111" else "Beta TV",
            "cached": True,
        }


class SlowProductService(DeterministicProductService):
    async def search(self, query):
        self.calls.append(("search", query))
        await asyncio.sleep(0.2)
        return {"query": query, "count": 0, "cached": True, "products": []}


class DeterministicOrdersService:
    def __init__(self):
        self.calls = []
        self.order_summaries = [
            {
                "order_id": "WM-DEMO-1004",
                "order_date": "2026-07-29",
                "status": "Delivered",
                "total": "199.99",
                "currency": "USD",
                "item_count": 1,
            },
            {
                "order_id": "WM-DEMO-1003",
                "order_date": "2026-07-11",
                "status": "Shipped",
                "total": "89.50",
                "currency": "USD",
                "item_count": 2,
            },
        ]
        self.order_details = {
            "WM-DEMO-1004": {
                **self.order_summaries[0],
                "items": [
                    {
                        "product_id": "111",
                        "name": "Alpha TV",
                        "unit_price": "199.99",
                        "quantity": 1,
                        "subtotal": "199.99",
                        "currency": "USD",
                        "image_url": "https://example.test/alpha-tv.jpg",
                    }
                ],
                "shipping_address": {
                    "name": "Pat Example",
                    "street": "1 Demo Way",
                    "city": "Bentonville",
                    "state": "AR",
                    "postal_code": "72712",
                    "country": "US",
                },
            },
            "WM-DEMO-1003": {
                **self.order_summaries[1],
                "items": [
                    {
                        "product_id": "222",
                        "name": "Beta TV",
                        "unit_price": "44.75",
                        "quantity": 2,
                        "subtotal": "89.50",
                        "currency": "USD",
                        "image_url": "https://example.test/beta-tv.jpg",
                    }
                ],
                "shipping_address": {
                    "name": "Pat Example",
                    "street": "1 Demo Way",
                    "city": "Bentonville",
                    "state": "AR",
                    "postal_code": "72712",
                    "country": "US",
                },
            },
        }

    def list(self, start: date | None = None, end: date | None = None):
        self.calls.append(
            (
                "list",
                start.isoformat() if start is not None else None,
                end.isoformat() if end is not None else None,
            )
        )
        return self.order_summaries

    def get(self, order_id):
        self.calls.append(("get", order_id))
        return self.order_details[order_id]


def _create_code_mode_server(products, orders):
    factory = getattr(code_mode_service, "create_ecommerce_code_mode_server", None)
    assert factory is not None
    return factory(products, orders)


@asynccontextmanager
async def ecommerce_code_mode_session(products, orders):
    server = _create_code_mode_server(products, orders)
    code_app = server.http_app(
        path="/",
        json_response=True,
        stateless_http=True,
        host_origin_protection=False,
    )
    transport = httpx.ASGITransport(app=code_app)
    async with code_app.router.lifespan_context(code_app):
        async with httpx.AsyncClient(
            transport=transport,
            base_url="https://code.demo.run.app",
        ) as client:
            async with streamable_http_client(
                "https://code.demo.run.app/",
                http_client=client,
            ) as (read, write, _):
                async with ClientSession(read, write) as session:
                    await session.initialize()
                    yield session


def test_code_mode_module_exposes_ecommerce_server_factory():
    assert hasattr(code_mode_service, "create_ecommerce_code_mode_server")


@pytest.mark.asyncio
async def test_code_mode_discovers_products_then_chains_product_tools():
    products = DeterministicProductService()
    orders = DeterministicOrdersService()
    code = """
search = await call_tool(
    "search_products",
    {"query": "55-inch 4K TV under $400"},
)
candidates = search["products"][:2]
details = []
for candidate in candidates:
    details.append(
        await call_tool(
            "product_details",
            {"product_id": candidate["product_id"]},
        )
    )
return {"candidates": details}
"""

    async with ecommerce_code_mode_session(products, orders) as session:
        listed = await session.list_tools()
        discovery = await session.call_tool(
            "search",
            {"query": "product catalog", "tags": ["products"]},
        )
        result = await session.call_tool("execute", {"code": code})

    discovery_text = discovery.content[0].text
    assert {tool.name for tool in listed.tools} == {"search", "execute"}
    assert discovery.isError is False
    assert "search_products" in discovery_text
    assert "product_details" in discovery_text
    assert "query" in discovery_text
    assert "product_id" in discovery_text
    assert "list_orders" not in discovery_text
    assert "get_order" not in discovery_text
    assert result.isError is False
    assert json.loads(result.content[0].text) == {
        "candidates": [
            {"product_id": "111", "name": "Alpha TV", "cached": True},
            {"product_id": "222", "name": "Beta TV", "cached": True},
        ]
    }
    assert products.calls == [
        ("search", "55-inch 4K TV under $400"),
        ("get", "111"),
        ("get", "222"),
    ]
    assert orders.calls == []


@pytest.mark.asyncio
async def test_code_mode_detailed_order_search_then_one_execution():
    products = DeterministicProductService()
    orders = DeterministicOrdersService()
    code = """
order_summaries = await call_tool(
    "list_orders",
    {"start_date": "2026-07-01", "end_date": "2026-07-31"},
)
order_id = order_summaries["result"][0]["order_id"]
order = await call_tool("get_order", {"order_id": order_id})
return {
    "order_id": order["order_id"],
    "order_date": order["order_date"],
    "status": order["status"],
    "total": order["total"],
    "currency": order["currency"],
    "items": [
        {"name": item["name"], "quantity": item["quantity"]}
        for item in order["items"]
    ],
}
"""

    async with ecommerce_code_mode_session(products, orders) as session:
        listed = await session.list_tools()
        discovery = await session.call_tool(
            "search",
            {"query": "customer orders", "tags": ["orders"]},
        )
        result = await session.call_tool("execute", {"code": code})

    discovery_text = discovery.content[0].text
    assert {tool.name for tool in listed.tools} == {"search", "execute"}
    assert discovery.isError is False
    assert "list_orders" in discovery_text
    assert "get_order" in discovery_text
    assert "start_date" in discovery_text
    assert "end_date" in discovery_text
    assert "order_id" in discovery_text
    assert "search_products" not in discovery_text
    assert "product_details" not in discovery_text
    assert result.isError is False
    assert json.loads(result.content[0].text) == {
        "order_id": "WM-DEMO-1004",
        "order_date": "2026-07-29",
        "status": "Delivered",
        "total": "199.99",
        "currency": "USD",
        "items": [
            {
                "name": "Alpha TV",
                "quantity": 1,
            }
        ],
    }
    assert "shipping_address" not in result.content[0].text
    assert orders.calls == [
        ("list", "2026-07-01", "2026-07-31"),
        ("get", "WM-DEMO-1004"),
    ]
    assert products.calls == []


def test_code_mode_uses_standard_registered_tools_without_manual_catalog():
    source = Path(code_mode_service.__file__).read_text()

    assert "class EcommerceCodeMode" not in source
    assert "EXECUTE_DESCRIPTION" not in source
    assert 'tags={"products"}' in source
    assert 'tags={"orders"}' in source
    assert 'Search(default_detail="detailed")' in source


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "code",
    [
        'return await call_tool("delete_everything", {})',
        "this is not valid Python",
    ],
)
async def test_code_mode_returns_bounded_errors_without_server_details(code):
    products = DeterministicProductService()
    orders = DeterministicOrdersService()

    async with ecommerce_code_mode_session(products, orders) as session:
        result = await session.call_tool("execute", {"code": code})

    assert result.isError is True
    message = " ".join(item.text for item in result.content if hasattr(item, "text"))
    assert message.strip()
    assert "traceback" not in message.casefold()
    assert "/home/" not in message


@pytest.mark.asyncio
async def test_code_mode_stops_generated_program_after_six_tool_calls():
    products = DeterministicProductService()
    orders = DeterministicOrdersService()
    code = """
results = []
for product_id in ["1", "2", "3", "4", "5", "6", "7"]:
    results.append(
        await call_tool(
            "product_details",
            {"product_id": product_id},
        )
)
return results
"""

    async with ecommerce_code_mode_session(products, orders) as session:
        result = await session.call_tool("execute", {"code": code})

    assert result.isError is True
    assert len(products.calls) == 6


@pytest.mark.asyncio
async def test_code_mode_timeout_includes_time_awaiting_product_tools(monkeypatch):
    monkeypatch.setattr(code_mode_service, "EXECUTION_TIMEOUT_SECONDS", 0.05)
    products = SlowProductService()
    orders = DeterministicOrdersService()
    code = """
return await call_tool(
    "search_products",
    {"query": "slow search"},
)
"""

    async with ecommerce_code_mode_session(products, orders) as session:
        result = await session.call_tool("execute", {"code": code})

    assert result.isError is True


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "code",
    [
        'return await call_tool("get_order", {})',
        'return await call_tool("list_orders", {"start_date": "2026-07-32"})',
        'return await call_tool("list_orders", {"end_date": "2026-07-99"})',
    ],
)
async def test_code_mode_validates_order_tool_parameters(code):
    products = DeterministicProductService()
    orders = DeterministicOrdersService()

    async with ecommerce_code_mode_session(products, orders) as session:
        result = await session.call_tool("execute", {"code": code})

    assert result.isError is True
    assert orders.calls == []
    assert products.calls == []


def _active_dockerfile_copy_sources(dockerfile: str) -> list[str]:
    logical_lines = []
    continued = ""
    for line in dockerfile.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        continued += stripped
        if continued.endswith("\\"):
            continued = f"{continued[:-1]} "
            continue
        logical_lines.append(continued)
        continued = ""

    sources = []
    for line in logical_lines:
        instruction, separator, arguments = line.partition(" ")
        if not separator or instruction.casefold() != "copy":
            continue
        words = shlex.split(arguments)
        while words and words[0].startswith("--"):
            option = words.pop(0)
            arguments = arguments.lstrip()[len(option) :].lstrip()
        paths = json.loads(arguments) if arguments.startswith("[") else words
        sources.extend(paths[:-1])
    return sources


def test_dockerfile_packages_animal_facts_dataset():
    dockerfile = Path(__file__).with_name("Dockerfile").read_text()
    copy_sources = _active_dockerfile_copy_sources(dockerfile)

    assert any(
        source.rstrip("/") == "." or fnmatch("animal_facts.jsonl", source)
        for source in copy_sources
    )


def test_dockerfile_packaging_check_ignores_commented_copy_instructions():
    dockerfile = "# COPY *.py orders.json animal_facts.jsonl ./\n"

    assert _active_dockerfile_copy_sources(dockerfile) == []


@pytest.mark.parametrize(
    ("dockerfile", "expected_sources"),
    [
        ("COPY animal_facts.jsonl /app/\n", ["animal_facts.jsonl"]),
        ('COPY ["animal_facts.jsonl", "/app/"]\n', ["animal_facts.jsonl"]),
        ("COPY --chown=app *.py \\\n             animal_facts.jsonl /app/\n", ["*.py", "animal_facts.jsonl"]),
    ],
)
def test_dockerfile_packaging_check_accepts_active_copy_layouts(
    dockerfile, expected_sources
):
    assert _active_dockerfile_copy_sources(dockerfile) == expected_sources


def _run_deploy_with_fake_commands(tmp_path, build_digest):
    fake_bin = tmp_path / "bin"
    fake_bin.mkdir()
    call_log = tmp_path / "calls.log"
    rendered_service = tmp_path / "rendered-service.yaml"

    fake_gcloud = fake_bin / "gcloud"
    fake_gcloud.write_text(
        """#!/usr/bin/env bash
set -euo pipefail
printf '%s\\n' "$*" >> "${FAKE_CALL_LOG}"
if [[ "$1 $2" == "builds submit" ]]; then
  printf '%s\\n' "${FAKE_BUILD_ID}"
elif [[ "$1 $2 $3" == "builds describe ${FAKE_BUILD_ID}" ]]; then
  printf '%s\\n' "${FAKE_BUILD_DIGEST}"
elif [[ "$1 $2 $3" == "run services replace" ]]; then
  cp "$4" "${FAKE_RENDERED_SERVICE}"
fi
"""
    )
    fake_gcloud.chmod(0o755)

    fake_sops = fake_bin / "sops"
    fake_sops.write_text(
        """#!/usr/bin/env bash
set -euo pipefail
printf 'sops %s\\n' "$*" >> "${FAKE_CALL_LOG}"
printf 'image: %s\\n' "${IMAGE}" > "${RENDERED_SERVICE}"
"""
    )
    fake_sops.chmod(0o755)

    env = {
        **os.environ,
        "PATH": f"{fake_bin}:{os.environ['PATH']}",
        "PROJECT_ID": "test-project",
        "REGION": "test-region",
        "SERVICE": "test-service",
        "FAKE_BUILD_ID": "build-123",
        "FAKE_BUILD_DIGEST": build_digest,
        "FAKE_CALL_LOG": str(call_log),
        "FAKE_RENDERED_SERVICE": str(rendered_service),
    }
    result = subprocess.run(
        [str(Path(__file__).with_name("deploy.sh"))],
        env=env,
        capture_output=True,
        text=True,
    )
    calls = call_log.read_text() if call_log.exists() else ""
    return result, calls, rendered_service


def test_deploy_script_pins_the_digest_from_its_cloud_build(tmp_path):
    digest = f"sha256:{'a' * 64}"

    result, calls, rendered_service = _run_deploy_with_fake_commands(
        tmp_path, digest
    )

    assert result.returncode == 0, result.stderr
    assert "builds submit" in calls
    assert "--suppress-logs" in calls
    assert "--format=value(id)" in calls
    assert "builds describe build-123" in calls
    assert "--format=value(results.images[0].digest)" in calls
    assert "artifacts docker images describe" not in calls
    assert rendered_service.read_text() == (
        "image: "
        f"test-region-docker.pkg.dev/test-project/walmart-demo/test-service@{digest}\n"
    )


def test_deploy_script_stops_before_rendering_for_an_invalid_digest(tmp_path):
    result, calls, rendered_service = _run_deploy_with_fake_commands(
        tmp_path, "not-a-digest"
    )

    assert result.returncode != 0
    assert "Could not resolve an immutable digest" in result.stderr
    assert "sops " not in calls
    assert "run services replace" not in calls
    assert not rendered_service.exists()


@pytest.mark.asyncio
async def test_orders_and_swagger():
    transport = httpx.ASGITransport(app=service.app)
    async with httpx.AsyncClient(transport=transport, base_url="https://demo.run.app") as client:
        orders = await client.get(
            "/v1/orders", params={"start_date": "2026-07-01", "end_date": "2026-07-31"}
        )
        assert orders.status_code == 200
        assert len(orders.json()) == 4
        assert (await client.get("/docs")).status_code == 200


@pytest.mark.asyncio
async def test_random_animal_fact_rest_endpoint_is_documented(monkeypatch):
    monkeypatch.setattr(
        service.animal_facts,
        "random_fact",
        lambda: {"animal": "Octopus", "fact": "Octopuses have three hearts."},
    )
    transport = httpx.ASGITransport(app=service.app)
    async with httpx.AsyncClient(
        transport=transport, base_url="https://demo.run.app"
    ) as client:
        response = await client.get("/v1/animal-facts/random")
        openapi = (await client.get("/openapi.json")).json()

    assert response.status_code == 200
    assert response.json() == {
        "animal": "Octopus",
        "fact": "Octopuses have three hearts.",
    }
    operation = openapi["paths"]["/v1/animal-facts/random"]["get"]
    schema = operation["responses"]["200"]["content"]["application/json"]["schema"]
    model_name = schema["$ref"].rsplit("/", 1)[-1]
    model = openapi["components"]["schemas"][model_name]
    assert set(model["required"]) == {"animal", "fact"}
    assert model["properties"]["animal"]["type"] == "string"
    assert model["properties"]["fact"]["type"] == "string"


@pytest.mark.asyncio
async def test_product_is_cached_without_spending_twice(monkeypatch):
    memory_store = FirestoreStore(service.settings, use_memory=True)
    monkeypatch.setattr(service.products, "store", memory_store)
    monkeypatch.setattr(service, "store", memory_store)
    calls = 0

    async def fake_product(product_id):
        nonlocal calls
        calls += 1
        return [{"us_item_id": product_id, "name": "Demo", "price": 12.5}]

    monkeypatch.setattr(service.products, "provider_product", fake_product)
    first = await service.products.get("123")
    second = await service.products.get("123")

    assert first["cached"] is False
    assert second["cached"] is True
    assert calls == 1
    assert memory_store.used == 1


@pytest.mark.asyncio
async def test_app_exposes_direct_and_product_code_mode_mcp_routes():
    transport = httpx.ASGITransport(app=service.app)
    async with service.app.router.lifespan_context(service.app):
        async with httpx.AsyncClient(transport=transport, base_url="https://demo.run.app") as client:
            async with streamable_http_client(
                "https://demo.run.app/mcp", http_client=client
            ) as (read, write, _):
                async with ClientSession(read, write) as session:
                    direct_server = await session.initialize()
                    listed = await session.list_tools()
                    animal_fact = await session.call_tool("get_random_animal_fact", {})
            async with streamable_http_client(
                "https://demo.run.app/mcp-code", http_client=client
            ) as (read, write, _):
                async with ClientSession(read, write) as session:
                    code_server = await session.initialize()
                    code_mode_tools = await session.list_tools()

    tools = {tool.name: tool for tool in listed.tools}
    assert direct_server.serverInfo.name == "Ecommerce Teaching Demo"
    assert code_server.serverInfo.name == "Ecommerce Teaching Demo Code Mode"
    assert set(tools) == {
        "search_products",
        "product_details",
        "list_orders",
        "get_order",
        "get_random_animal_fact",
    }

    search_query = tools["search_products"].inputSchema["properties"]["query"]
    assert "natural-language keywords" in search_query["description"].casefold()

    product_id = tools["product_details"].inputSchema["properties"]["product_id"]
    assert "catalog product id returned by search" in product_id["description"].casefold()
    assert "walmart" not in product_id["description"].casefold()

    list_orders = tools["list_orders"]
    assert "inclusive" in list_orders.description.casefold()
    assert "ecommerce shopping orders" in list_orders.description.casefold()
    order_summary = list_orders.outputSchema["$defs"]["OrderSummary"]
    assert {
        "order_id",
        "order_date",
        "status",
        "total",
        "currency",
        "item_count",
    } <= set(order_summary["required"])

    get_order = tools["get_order"]
    assert "ecommerce shopping order" in get_order.description.casefold()
    assert "WM-DEMO-" in get_order.inputSchema["properties"]["order_id"]["description"]
    assert "items" in get_order.outputSchema["required"]

    random_fact = tools["get_random_animal_fact"]
    assert random_fact.inputSchema["properties"] == {}
    assert "randomly selected" in random_fact.description
    assert {"animal", "fact"} <= set(random_fact.outputSchema["required"])

    assert all(
        forbidden not in (tool.description or "").casefold()
        for tool in tools.values()
        for forbidden in ("quota", "cost")
    )
    assert animal_fact.isError is False
    assert animal_fact.structuredContent is not None
    assert animal_fact.structuredContent["animal"].strip()
    assert animal_fact.structuredContent["fact"].strip()
    code_tools = {tool.name: tool for tool in code_mode_tools.tools}
    assert set(code_tools) == {"search", "execute"}
    assert "available tools" in code_tools["search"].description.casefold()
    execute_description = code_tools["execute"].description.casefold()
    assert "call_tool" in execute_description
    assert "available ecommerce tools" not in execute_description
    assert "list_orders" not in execute_description


@pytest.mark.asyncio
async def test_mcp_product_contract_accepts_nested_provider_metadata(monkeypatch):
    memory_store = FirestoreStore(service.settings, use_memory=True)
    monkeypatch.setattr(service.products, "store", memory_store)

    async def fake_product(product_id):
        return [
            {
                "us_item_id": product_id,
                "name": "Demo shelf",
                "category_path": [
                    "Home",
                    {"name": "Furniture", "url": "/cp/furniture/103150"},
                ],
                "specifications": {
                    "Dimensions": {"height": "10 in", "width": 5},
                    "Assembly required": False,
                },
            }
        ]

    monkeypatch.setattr(service.products, "provider_product", fake_product)
    test_mcp = create_mcp_server(
        service.products, service.orders, service.animal_facts
    )

    @asynccontextmanager
    async def lifespan(_: FastAPI):
        async with test_mcp.session_manager.run():
            yield

    test_app = FastAPI(lifespan=lifespan)
    test_app.add_route(
        "/mcp",
        CanonicalMcpPath(test_mcp.streamable_http_app()),
        methods=["POST"],
    )
    transport = httpx.ASGITransport(app=test_app)
    async with test_app.router.lifespan_context(test_app):
        async with httpx.AsyncClient(
            transport=transport, base_url="https://demo.run.app"
        ) as client:
            async with streamable_http_client(
                "https://demo.run.app/mcp", http_client=client
            ) as (read, write, _):
                async with ClientSession(read, write) as session:
                    await session.initialize()
                    result = await session.call_tool(
                        "product_details", {"product_id": "987654321"}
                    )
                    listed = await session.list_tools()

    assert result.isError is False
    assert result.structuredContent["specifications"] == {
        "Dimensions": {"height": "10 in", "width": 5},
        "Assembly required": False,
    }
    product_tool = next(
        tool for tool in listed.tools if tool.name == "product_details"
    )
    product_schema = product_tool.outputSchema
    assert product_schema["properties"]["category_path"]["items"] == {}
    assert (
        product_schema["properties"]["specifications"]["additionalProperties"]
        is True
    )
    assert "#/$defs/JsonValue" not in json.dumps(product_schema)


async def _call_product_tool(products, tool_name, arguments):
    test_mcp = create_mcp_server(products, service.orders, service.animal_facts)

    @asynccontextmanager
    async def lifespan(_: FastAPI):
        async with test_mcp.session_manager.run():
            yield

    test_app = FastAPI(lifespan=lifespan)
    test_app.add_route(
        "/mcp",
        CanonicalMcpPath(test_mcp.streamable_http_app()),
        methods=["POST"],
    )
    transport = httpx.ASGITransport(app=test_app)
    async with test_app.router.lifespan_context(test_app):
        async with httpx.AsyncClient(
            transport=transport, base_url="https://demo.run.app"
        ) as client:
            async with streamable_http_client(
                "https://demo.run.app/mcp", http_client=client
            ) as (read, write, _):
                async with ClientSession(read, write) as session:
                    await session.initialize()
                    return await session.call_tool(tool_name, arguments)


@pytest.mark.asyncio
async def test_mcp_search_normalizes_adverse_provider_values(monkeypatch):
    memory_store = FirestoreStore(service.settings, use_memory=True)
    monkeypatch.setattr(service.products, "store", memory_store)

    async def fake_search(_query):
        return [
            {
                "us_item_id": 123,
                "name": "Demo tablet",
                "price": "$19.95",
                "currency": 840,
                "image_url": 101,
                "url": 202,
                "average_rating": "4.25",
                "number_of_reviews": 7.5,
            }
        ]

    monkeypatch.setattr(service.products, "provider_search", fake_search)

    result = await _call_product_tool(
        service.products, "search_products", {"query": "demo tablet"}
    )

    assert result.isError is False
    assert result.structuredContent == {
        "query": "demo tablet",
        "count": 1,
        "cached": False,
        "products": [
            {
                "product_id": "123",
                "name": "Demo tablet",
                "price": 19.95,
                "currency": "840",
                "image_url": "101",
                "url": "202",
                "rating": 4.25,
                "review_count": "7.5",
            }
        ],
    }


@pytest.mark.asyncio
async def test_mcp_product_normalizes_adverse_legacy_cached_values():
    memory_store = FirestoreStore(service.settings, use_memory=True)
    await memory_store.put(
        "walmart:product:456",
        "product",
        {
            "product_id": 456,
            "name": 789,
            "url": 101,
            "price": "$29.50",
            "currency": 840,
            "availability": 1,
            "seller": 2,
            "brand": 3,
            "description": 4,
            "images": [5, "https://example.test/image.jpg"],
            "category_path": ["Home"],
            "rating": "4.5",
            "review_count": 12.5,
            "specifications": {"Width": 6},
            "cached": False,
        },
    )

    result = await _call_product_tool(
        service.ProductService(service.settings, memory_store),
        "product_details",
        {"product_id": "456"},
    )

    assert result.isError is False
    assert result.structuredContent == {
        "product_id": "456",
        "name": "789",
        "url": "101",
        "price": 29.5,
        "currency": "840",
        "availability": "1",
        "seller": "2",
        "brand": "3",
        "description": "4",
        "images": ["5", "https://example.test/image.jpg"],
        "category_path": ["Home"],
        "rating": 4.5,
        "review_count": "12.5",
        "specifications": {"Width": 6},
        "cached": True,
    }


@pytest.mark.asyncio
async def test_rest_search_normalizes_non_finite_fresh_provider_numbers(monkeypatch):
    memory_store = FirestoreStore(service.settings, use_memory=True)
    monkeypatch.setattr(service.products, "store", memory_store)
    monkeypatch.setattr(service, "store", memory_store)

    async def fake_search(_query):
        return [
            {
                "us_item_id": 789,
                "name": "Finite tablet",
                "price": "NaN",
                "average_rating": "1e9999",
            }
        ]

    monkeypatch.setattr(service.products, "provider_search", fake_search)
    transport = httpx.ASGITransport(app=service.app, raise_app_exceptions=False)

    async with httpx.AsyncClient(
        transport=transport, base_url="https://demo.run.app"
    ) as client:
        response = await client.get(
            "/v1/products/search", params={"q": "finite tablet"}
        )

    assert response.status_code == 200
    assert response.json()["products"][0]["price"] is None
    assert response.json()["products"][0]["rating"] is None
    cached = await memory_store.get("walmart:search:finite tablet")
    assert cached["products"][0]["price"] is None
    assert cached["products"][0]["rating"] is None


@pytest.mark.asyncio
async def test_mcp_product_normalizes_non_finite_legacy_cached_metadata():
    memory_store = FirestoreStore(service.settings, use_memory=True)
    await memory_store.put(
        "walmart:product:987",
        "product",
        {
            "product_id": "987",
            "name": "Legacy shelf",
            "price": float("inf"),
            "currency": "USD",
            "rating": float("nan"),
            "category_path": [
                {
                    "name": "Furniture",
                    "scores": [1.5, float("-inf")],
                }
            ],
            "specifications": {
                "Measurements": {
                    "width": 12.5,
                    "confidence": float("nan"),
                }
            },
            "cached": False,
        },
    )

    products = service.ProductService(service.settings, memory_store)
    result = await _call_product_tool(
        products,
        "product_details",
        {"product_id": "987"},
    )
    normalized = await products.get("987")

    assert result.isError is False
    assert normalized["price"] is None
    assert normalized["rating"] is None
    assert normalized["category_path"] == [
        {"name": "Furniture", "scores": [1.5, None]}
    ]
    assert normalized["specifications"] == {
        "Measurements": {"width": 12.5, "confidence": None}
    }
    assert result.structuredContent["price"] is None
    assert result.structuredContent["rating"] is None
    assert result.structuredContent["category_path"] == [
        {"name": "Furniture", "scores": [1.5, None]}
    ]
    assert result.structuredContent["specifications"] == {
        "Measurements": {"width": 12.5, "confidence": None}
    }
