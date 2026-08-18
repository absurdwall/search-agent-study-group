FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

ENV UV_COMPILE_BYTECODE=1 UV_NO_DEV=1 PYTHONUNBUFFERED=1
WORKDIR /app

COPY pyproject.toml ./
RUN uv sync --no-install-project
COPY *.py orders.json animal_facts.jsonl ./

CMD ["sh", "-c", "exec uv run --no-sync uvicorn app:app --host 0.0.0.0 --port ${PORT:-8080} --no-access-log"]
