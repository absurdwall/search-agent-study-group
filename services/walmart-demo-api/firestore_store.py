"""Permanent Firestore cache and atomic lifetime provider-call quota."""

import asyncio
import hashlib
from typing import Any

from fastapi import HTTPException
from google.cloud import firestore_v1

from config import Settings


class FirestoreStore:
    def __init__(self, settings: Settings, use_memory: bool | None = None):
        self.settings = settings
        self.use_memory = settings.use_memory_store if use_memory is None else use_memory
        self._client: firestore_v1.AsyncClient | None = None
        self._cache: dict[str, dict[str, Any]] = {}
        self._used = 0
        self._lock = asyncio.Lock()

    @property
    def used(self) -> int:
        return self._used

    def _db(self) -> firestore_v1.AsyncClient:
        if self._client is None:
            self._client = firestore_v1.AsyncClient(
                project=self.settings.gcp_project,
                database=self.settings.firestore_database,
            )
        return self._client

    def _cache_document(self, key: str):
        document_id = hashlib.sha256(key.encode()).hexdigest()
        return self._db().collection("cache_entries").document(document_id)

    async def get(self, key: str) -> dict[str, Any] | None:
        if self.use_memory:
            return self._cache.get(key)
        snapshot = await self._cache_document(key).get()
        return (
            (snapshot.to_dict() or {}).get("clean_response")
            if snapshot.exists
            else None
        )

    async def put(self, key: str, kind: str, value: dict[str, Any]) -> None:
        if self.use_memory:
            self._cache[key] = value
            return
        await self._cache_document(key).set(
            {
                "canonical_key": key,
                "kind": kind,
                "source": "bright_data",
                "created_at": firestore_v1.SERVER_TIMESTAMP,
                "clean_response": value,
            }
        )

    async def quota_state(self) -> tuple[int, int]:
        if self.use_memory:
            return self.settings.quota_limit, self._used
        snapshot = await self._db().collection("service_state").document(
            "bright_data_quota"
        ).get()
        data = snapshot.to_dict() or {}
        limit = min(int(data.get("limit", self.settings.quota_limit)), self.settings.quota_limit)
        return limit, int(data.get("used", 0))

    async def reserve(self) -> None:
        if self.use_memory:
            async with self._lock:
                if self._used >= self.settings.quota_limit:
                    raise HTTPException(429, "Bright Data quota exhausted")
                self._used += 1
            return

        document = self._db().collection("service_state").document(
            "bright_data_quota"
        )

        @firestore_v1.async_transactional
        async def reserve_in_transaction(transaction):
            snapshot = await document.get(transaction=transaction)
            data = snapshot.to_dict() or {}
            limit = min(
                int(data.get("limit", self.settings.quota_limit)),
                self.settings.quota_limit,
            )
            used = int(data.get("used", 0))
            if used >= limit:
                raise HTTPException(429, "Bright Data quota exhausted")
            transaction.set(document, {"limit": limit, "used": used + 1})

        await reserve_in_transaction(self._db().transaction())
