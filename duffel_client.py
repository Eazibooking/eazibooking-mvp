import os
import json
import urllib.request
import urllib.error


DUFFEL_BASE_URL = "https://api.duffel.com"


def _duffel_request(path: str, payload: dict) -> dict:
    token = os.getenv("DUFFEL_TOKEN")
    if not token:
        raise RuntimeError("DUFFEL_TOKEN is missing in environment variables.")

    url = f"{DUFFEL_BASE_URL}{path}"

    data = json.dumps(payload).encode("utf-8")

    req = urllib.request.Request(
        url,
        data=data,
        method="POST",
        headers={
            "Authorization": f"Bearer {token}",
            "Duffel-Version": "beta",
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
    )

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            body = resp.read().decode("utf-8")
            return json.loads(body)
    except urllib.error.HTTPError as e:
        err_body = e.read().decode("utf-8", errors="ignore")
        raise RuntimeError(f"Duffel API error {e.code}: {err_body}")
    except Exception as e:
        raise RuntimeError(f"Duffel request failed: {str(e)}")


def search_flights(payload: dict) -> dict:
    """
    Expected payload from your API:
    {
      "slices": [{"origin":"SFO","destination":"LAX","departure_date":"2026-02-15"}],
      "passengers": [{"type":"adult"}],
      "cabin_class": "economy",
      "max_connections": 1
    }
    """
    slices = payload.get("slices", [])
    passengers = payload.get("passengers", [])
    cabin_class = payload.get("cabin_class", "economy")
    max_connections = payload.get("max_connections", 1)

    # Duffel wants: { "data": { ... } }
    duffel_payload = {
        "data": {
            "slices": slices,
            "passengers": passengers,
            "cabin_class": cabin_class,
            "max_connections": max_connections,

            # IMPORTANT: this tells Duffel to return offers in same response
            "return_offers": True,
        }
    }

    return _duffel_request("/air/offer_requests", duffel_payload)
