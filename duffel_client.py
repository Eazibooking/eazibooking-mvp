import os
import httpx

DUFFEL_BASE_URL = "https://api.duffel.com"

async def search_flights(payload: dict):
    token = os.getenv("DUFFEL_TOKEN")
    if not token:
        raise ValueError("DUFFEL_TOKEN is missing in environment variables.")

    # Duffel expects: { "data": { "slices": [...], "passengers": [...], "cabin_class": "economy" } }
    body = {
        "data": {
            "slices": payload["slices"],
            "passengers": payload["passengers"],
            "cabin_class": payload.get("cabin_class", "economy"),
        }
    }

    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json",
        "Duffel-Version": "v1",
    }

    async with httpx.AsyncClient(timeout=60) as client:
        r = await client.post(f"{DUFFEL_BASE_URL}/air/offer_requests", json=body, headers=headers)

    # If Duffel returns an error, show it clearly
    if r.status_code >= 400:
        try:
            return {"error": r.json(), "status_code": r.status_code}
        except Exception:
            return {"error": r.text, "status_code": r.status_code}

    return r.json()
