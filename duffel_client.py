import os
import requests

DUFFEL_API_BASE = "https://api.duffel.com"
DUFFEL_VERSION = "v1"

def search_flights(payload: dict) -> dict:
    token = os.getenv("DUFFEL_TOKEN")
    if not token:
        raise RuntimeError("DUFFEL_TOKEN is missing in environment variables.")

    url = f"{DUFFEL_API_BASE}/air/offer_requests"

    headers = {
        "Authorization": f"Bearer {token}",
        "Duffel-Version": DUFFEL_VERSION,
        "Content-Type": "application/json",
        "Accept": "application/json",
    }

    body = {"data": payload}

    resp = requests.post(url, headers=headers, json=body, timeout=30)
    # If Duffel returns an error, show it clearly
    if resp.status_code >= 400:
        try:
            return {"error": resp.json(), "status_code": resp.status_code}
        except Exception:
            return {"error": resp.text, "status_code": resp.status_code}

    return resp.json()
