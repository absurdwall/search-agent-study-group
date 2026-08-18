#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "${SCRIPT_DIR}"

PROJECT_ID="${PROJECT_ID:-np-public-training}"
REGION="${REGION:-us-east1}"
SERVICE="${SERVICE:-walmart-demo-api}"
IMAGE_REPOSITORY="${REGION}-docker.pkg.dev/${PROJECT_ID}/walmart-demo/${SERVICE}"
IMAGE_TAG="${IMAGE_REPOSITORY}:latest"
RENDERED_SERVICE="$(mktemp)"
export PROJECT_ID REGION SERVICE RENDERED_SERVICE
trap 'rm -f "${RENDERED_SERVICE}"' EXIT

BUILD_ID="$(
  gcloud builds submit \
    --project="${PROJECT_ID}" \
    --tag="${IMAGE_TAG}" \
    --suppress-logs \
    --format='value(id)' \
    .
)"
if [[ -z "${BUILD_ID}" ]]; then
  echo "Cloud Build did not return a build ID" >&2
  exit 1
fi
IMAGE_DIGEST="$(
  gcloud builds describe "${BUILD_ID}" \
    --project="${PROJECT_ID}" \
    --format='value(results.images[0].digest)'
)"
if [[ ! "${IMAGE_DIGEST}" =~ ^sha256:[0-9a-f]{64}$ ]]; then
  echo "Could not resolve an immutable digest for ${IMAGE_TAG}" >&2
  exit 1
fi
IMAGE="${IMAGE_REPOSITORY}@${IMAGE_DIGEST}"
export IMAGE
echo "Deploying immutable image ${IMAGE}"

sops exec-env .env.deploy.enc.yaml \
  'envsubst < service.yaml > "${RENDERED_SERVICE}"'
gcloud run services replace "${RENDERED_SERVICE}" \
  --project="${PROJECT_ID}" \
  --region="${REGION}" \
  --quiet
gcloud run services add-iam-policy-binding "${SERVICE}" \
  --project="${PROJECT_ID}" \
  --region="${REGION}" \
  --member=allUsers \
  --role=roles/run.invoker \
  --quiet
