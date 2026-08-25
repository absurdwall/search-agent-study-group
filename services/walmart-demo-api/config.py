"""Environment configuration for the demo service."""

from dataclasses import dataclass
import os


@dataclass(frozen=True)
class Settings:
    dataset_id: str = os.getenv("WALMART_DATASET_ID", "gd_l95fol7l1ru6rlo116")
    quota_limit: int = min(int(os.getenv("QUOTA_LIMIT", "1000")), 1_000)
    provider_timeout: int = int(os.getenv("PROVIDER_TIMEOUT_SECONDS", "180"))
    gcp_project: str | None = os.getenv("GCP_PROJECT") or None
    firestore_database: str = os.getenv("FIRESTORE_DATABASE", "(default)")
    use_memory_store: bool = os.getenv("USE_MEMORY_STORE", "false").lower() == "true"


settings = Settings()
