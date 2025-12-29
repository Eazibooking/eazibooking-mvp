import os
import requests

DUFFEL_BASE_URL = "https://api.duffel.com"
DUFFEL_API_VERSION = "beta"  # Duffel requires 'Duffel-Version' header, commonly 'beta'

def search_flights_duffel(payload: dict) -> dict:
    token = os.getenv("DUFFEL_ACCESS_TOKEN")
    if not token:
        return {
            "ok": False,
            "error": "Missing DUFFEL_ACCESS_TOKEN in environment variables (Render)",
        }

    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Duffel-Version": DUFFEL_API_VERSION,
    }

    # Create an offer request
    url = f"{DUFFEL_BASE_URL}/air/offer_requests"
    resp = requests.post(url, json=payload, headers=headers, timeout=30)

    try:
        data = resp.json()
    except Exception:
        return {"ok": False, "status_code": resp.status_code, "error": resp.text}

    if resp.status_code >= 400:
        return {"ok": False, "status_code": resp.status_code, "error": data}

    return {"ok": True, "data": data}
