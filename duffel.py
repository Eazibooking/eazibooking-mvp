from __future__ import annotations

import os
from typing import Any, Dict, List, Optional
import httpx


class DuffelClient:
    def __init__(self) -> None:
        self.base_url = os.getenv("DUFFEL_BASE_URL", "https://api.duffel.com").rstrip("/")
        self.token = os.environ["DUFFEL_ACCESS_TOKEN"]
        self.version = os.getenv("DUFFEL_VERSION", "v2")

    def _headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {self.token}",
            "Duffel-Version": self.version,
            "Accept": "application/json",
            "Content-Type": "application/json",
        }

    async def create_offer_request(
        self,
        slices: List[Dict[str, Any]],
        passengers: List[Dict[str, Any]],
        cabin_class: Optional[str] = None,
        max_connections: Optional[int] = None,
    ) -> Dict[str, Any]:
        payload: Dict[str, Any] = {
            "slices": slices,
            "passengers": passengers,
        }
        if cabin_class:
            payload["cabin_class"] = cabin_class
        if max_connections is not None:
            payload["max_connections"] = max_connections

        async with httpx.AsyncClient(timeout=45) as client:
            r = await client.post(
                f"{self.base_url}/air/offer_requests",
                headers=self._headers(),
                json={"data": payload},
            )
            r.raise_for_status()
            return r.json()["data"]

    async def list_offers(self, offer_request_id: str, limit: int = 50) -> List[Dict[str, Any]]:
        # Duffel also returns offers inside offer request response depending on your params.
        # This helper fetches offers endpoint filtered by offer_request_id if needed.
        async with httpx.AsyncClient(timeout=45) as client:
            r = await client.get(
                f"{self.base_url}/air/offers",
                headers=self._headers(),
                params={"offer_request_id": offer_request_id, "limit": limit},
            )
            r.raise_for_status()
            return r.json().get("data", [])

    async def create_order(self, offer_id: str, passengers: Optional[List[Dict[str, Any]]] = None, payment: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        payload: Dict[str, Any] = {
            "selected_offers": [offer_id],
        }
        # In Duffel, you typically need passenger details when creating an order.
        if passengers:
            payload["passengers"] = passengers
        if payment:
            payload["payments"] = [payment]

        async with httpx.AsyncClient(timeout=45) as client:
            r = await client.post(
                f"{self.base_url}/air/orders",
                headers=self._headers(),
                json={"data": payload},
            )
            r.raise_for_status()
            return r.json()["data"]
