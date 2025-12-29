import os
import httpx


DUFFEL_ACCESS_TOKEN = os.getenv("DUFFEL_ACCESS_TOKEN")
DUFFEL_API_URL = "https://api.duffel.com/air/offer_requests"


class DuffelClient:
    def __init__(self):
        if not DUFFEL_ACCESS_TOKEN:
            raise RuntimeError("DUFFEL_ACCESS_TOKEN is not set")

        self.headers = {
            "Authorization": f"Bearer {DUFFEL_ACCESS_TOKEN}",
            "Content-Type": "application/json",
            "Duffel-Version": "v2",
        }

    async def search_flights(self, payload: dict):
        async with httpx.AsyncClient(timeout=60) as client:
            response = await client.post(
                DUFFEL_API_URL,
                headers=self.headers,
                json={"data": payload},
            )

        if response.status_code >= 400:
            raise RuntimeError(response.text)

        return response.json()
