import os
import httpx


DUFFEL_BASE_URL = os.getenv("DUFFEL_BASE_URL", "https://api.duffel.com")
DUFFEL_VERSION = os.getenv("DUFFEL_VERSION", "v2")
DUFFEL_ACCESS_TOKEN = os.getenv("DUFFEL_ACCESS_TOKEN", "")


class DuffelClient:
    def __init__(self) -> None:
        if not DUFFEL_ACCESS_TOKEN:
            raise RuntimeError("DUFFEL_ACCESS_TOKEN is not set in environment variables")

        self.headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Duffel-Version": DUFFEL_VERSION,
            "Authorization": f"Bearer {DUFFEL_ACCESS_TOKEN}",
        }

    async def search_offers(self, payload: dict) -> dict:
        """
        Calls Duffel Offer Requests endpoint and returns the full Duffel response JSON.
        """
        url = f"{DUFFEL_BASE_URL}/air/offer_requests"

        async with httpx.AsyncClient(timeout=60) as client:
            r = await client.post(url, headers=self.headers, json={"data": payload})

        # Helpful error message if token / payload is wrong
        if r.status_code >= 400:
            try:
                detail = r.json()
            except Exception:
                detail = {"raw": r.text}
            raise RuntimeError(f"Duffel error {r.status_code}: {detail}")

        return r.json()
