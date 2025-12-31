import os
import requests
from fastapi import HTTPException

DUFFEL_URL = "https://api.duffel.com/air/offer_requests"


def search_flights_duffel(body: dict):
    token = os.getenv("DUFFEL_TOKEN")
    if not token:
        raise HTTPException(status_code=500, detail="DUFFEL_TOKEN is missing in environment variables.")

    # Convert your API body -> Duffel format
    data = {
        "data": {
            "slices": body["slices"],
            "passengers": body["passengers"],
            "cabin_class": body.get("cabin_class", "economy"),
            "max_connections": body.get("max_connections", 1),
        }
    }

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        # If Duffel ever complains, change this to the version shown in their docs/account
        "Duffel-Version": "v1",
    }

    r = requests.post(DUFFEL_URL, json=data, headers=headers, timeout=30)

    # Return Duffel error clearly
    if r.status_code >= 400:
        try:
            return {"error": True, "status_code": r.status_code, "detail": r.json()}
        except Exception:
            return {"error": True, "status_code": r.status_code, "detail": r.text}

    return r.json()
