# Walmart teaching demo API

A compact public Python service for teaching REST and MCP tool use with ecommerce data.

## What it exposes

| Route/tool | Data |
| --- | --- |
| `GET /v1/products/search?q=tablet` | Live Walmart search, then permanent cache |
| `GET /v1/products/{product_id}` | Live Walmart PDP, then permanent cache |
| `GET /v1/orders` | Four fake orders; defaults to the last 30 days |
| `GET /v1/orders/{order_id}` | Fake order linked to real Walmart product IDs |
| `GET /v1/animal-facts/random` | One randomly selected fact from the packaged dataset |
| MCP `get_random_animal_fact` | One randomly selected fact from the packaged dataset |
| `POST /mcp` | The five operations above as MCP tools |
| `POST /mcp-code` | Ecommerce Code Mode through one `execute` tool |
| `GET /docs` | Swagger UI |

MCP clients discover the available tools automatically by initializing a session and calling `tools/list` on `POST /mcp`; no separately maintained tool registry is required. Each listed tool includes a description of when to use it, documented input fields, and a structured output schema so clients can select and call it correctly.

The direct `/mcp` surface remains the compatibility and teaching baseline with five visible tools. The separate `/mcp-code` surface is an experimental FastMCP Code Mode demo: clients see only `execute`, while its generated Python may call four prepared ecommerce tools inside a Monty sandbox: `search_products`, `product_details`, `list_orders`, and `get_order`. Each program is limited to 10 seconds, 50 MB, and six tool calls; it receives no filesystem, environment, subprocess, or arbitrary network capability. A generated program must end with a JSON-serializable `return` value; `print()` output is not returned to the agent.

Only an uncached Bright Data attempt increments the atomic Firestore counter. The hard lifetime ceiling is 1,000 calls; cached products and fake orders continue working after exhaustion.

Cloud Run is configured to **scale to zero** when idle and to run at most one instance. These settings, the 240-second timeout, image, concurrency, and environment variables are declared in `service.yaml`.

## Run with uv

Python 3.12 is required; any 3.12 patch release is supported. The project and container intentionally reject Python 3.13 so local development matches the hosted workshop runtime.

```bash
uv sync
cp .env.example .env
set -a; source .env; set +a
uv run uvicorn app:app --reload
```

For local use without Firestore, keep `USE_MEMORY_STORE=true`. Swagger is at <http://127.0.0.1:8000/docs>.

Run the focused tests:

```bash
uv run pytest -q
```

## Encrypted deployment secrets

The repository contains `.env.deploy.enc.yaml`, encrypted by [SOPS](https://github.com/getsops/sops) with this GCP KMS key:

```bash
projects/np-public-training/locations/us-east1/keyRings/walmart-demo-sops/cryptoKeys/deployment-secrets
```

Only `BRIGHTDATA_API_KEY` is encrypted; non-secret deployment settings remain readable in the diff. A developer needs `roles/cloudkms.cryptoKeyEncrypterDecrypter` on that key and authenticated Google Application Default Credentials.

Edit the encrypted file without creating plaintext in the repository:

```bash
sops .env.deploy.enc.yaml
```

Verify that it decrypts:

```bash
sops decrypt .env.deploy.enc.yaml >/dev/null
```

Cloud Run ultimately stores these as service environment variables, visible to principals allowed to inspect the service. SOPS protects the secret in Git; it is not a substitute for Secret Manager at runtime.

## Deploy to Cloud Run

The checked-in script builds with Cloud Build, captures that build's immutable image digest, asks SOPS to expose decrypted values only to `envsubst`, renders `service.yaml` to a temporary file, deploys it, restores public invocation, and deletes the rendered plaintext file on exit. Pinning the build result ensures Cloud Run deploys the intended image rather than treating the unchanged `latest` tag name as unchanged configuration:

```bash
./deploy.sh
```

The deployment manifest is the source of truth:

```bash
sed -n '1,240p' service.yaml
```

Its important scaling section is:

```yaml
metadata:
  annotations:
    run.googleapis.com/minScale: "0"
    run.googleapis.com/maxScale: "1"
spec:
  template:
    metadata:
      annotations:
        autoscaling.knative.dev/minScale: "0"
        autoscaling.knative.dev/maxScale: "1"
```

Equivalent manual deployment steps:

```bash
export SERVICE=walmart-demo-api
export IMAGE_REPOSITORY=us-east1-docker.pkg.dev/np-public-training/walmart-demo/walmart-demo-api
export IMAGE_TAG="${IMAGE_REPOSITORY}:latest"
export RENDERED_SERVICE="$(mktemp)"
trap 'rm -f "${RENDERED_SERVICE}"' EXIT

export BUILD_ID="$(
  gcloud builds submit \
    --project=np-public-training \
    --tag="${IMAGE_TAG}" \
    --suppress-logs \
    --format='value(id)' \
    .
)"
if [[ -z "${BUILD_ID}" ]]; then
  echo "Cloud Build did not return a build ID" >&2
  exit 1
fi
export IMAGE_DIGEST="$(
  gcloud builds describe "${BUILD_ID}" \
    --project=np-public-training \
    --format='value(results.images[0].digest)'
)"
if [[ ! "${IMAGE_DIGEST}" =~ ^sha256:[0-9a-f]{64}$ ]]; then
  echo "Could not resolve an immutable digest for ${IMAGE_TAG}" >&2
  exit 1
fi
export IMAGE="${IMAGE_REPOSITORY}@${IMAGE_DIGEST}"
sops exec-env .env.deploy.enc.yaml \
  'envsubst < service.yaml > "${RENDERED_SERVICE}"'
gcloud run services replace "${RENDERED_SERVICE}" \
  --project=np-public-training \
  --region=us-east1 \
  --quiet
```

The Cloud Run service account needs Firestore access. Cache documents live in `cache_entries`; quota state lives at `service_state/bright_data_quota`. To raise an existing deployment's limit, update that document's `limit` while preserving `used`.

## Structure

```text
app.py               lean FastAPI composition and REST routes
config.py            environment settings
firestore_store.py   permanent cache and atomic quota
orders_service.py    deterministic order queries
animal_facts_service.py  random fact selection from packaged JSONL data
product_service.py   Bright Data, cleanup and cache orchestration
mcp_server.py        five discoverable MCP tools over the same services
code_mode_mcp_server.py  bounded ecommerce FastMCP Code Mode server
orders.json          deterministic teaching orders
animal_facts.jsonl   animal facts dataset packaged with the service
test_app.py          focused behavior and packaging regression tests
pyproject.toml       uv dependencies
Dockerfile           uv-based Cloud Run image
service.yaml         declarative Cloud Run service configuration
deploy.sh            SOPS-aware build and deployment
```
