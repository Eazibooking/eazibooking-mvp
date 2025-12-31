import os
import requests

DUFFEL_BASE_URL = "https://api.duffel.com"
DUFFEL_VERSION = "v1"


def search_flights_duffel(payload: dict) -> dict:
    """
    Calls Duffel Offer Requests endpoint.
    Expects payload like:
    {
      "slices": [...],
      "passengers": [...],
      "cabin_class": "economy",
      "max_connections": 1
    }
    """
    token = os.getenv("DUFFEL_TOKEN")
    if not token:
        raise RuntimeError("DUFFEL_TOKEN is missing in environment variables.")

    url = f"{DUFFEL_BASE_URL}/air/offer_requests"

    headers = {
        "Authorization": f"Bearer {token}",
        "Duffel-Version": DUFFEL_VERSION,
        "Content-Type": "application/json",
        "Accept": "application/json",
    }

    body = {"data": payload}

    r = requests.post(url, headers=headers, json=body, timeout=30)

    # If Duffel returns an error, show it clearly
    if r.status_code >= 400:
        try:
            return {"error": True, "status_code": r.status_code, "details": r.json()}
        except Exception:
            return {"error": True, "status_code": r.status_code, "details": r.text}

    return r.json()
