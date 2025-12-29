import os
import httpx

DUFFEL_BASE_URL = os.getenv("DUFFEL_BASE_URL", "https://api.duffel.com").rstrip("/")
DUFFEL_VERSION = os.getenv("DUFFEL_VERSION", "v2")

def headers():
    return {
        "Authorization": f"Bearer {os.environ['DUFFEL_ACCESS_TOKEN']}",
        "Duffel-Version": DUFFEL_VERSION,
        "Accept": "application/json",
        "Content-Type": "application/json",
    }

async def create_offer_request(payload: dict):
    async with httpx.AsyncClient(timeout=60) as client:
        r = await client.post(
            f"{DUFFEL_BASE_URL}/air/offer_requests",
            headers=headers(),
            json={"data": payload},
        )
        r.raise_for_status()
        return r.json()["data"]
