import os
from duffel_api import Duffel

def search_flights(payload: dict):
    token = os.getenv("DUFFEL_ACCESS_TOKEN")
    if not token:
        raise Exception("DUFFEL_ACCESS_TOKEN is missing in Render Environment Variables")

    duffel = Duffel(access_token=token)

    # IMPORTANT: Duffel SDK expects payload inside data={}
    offer_request = duffel.offer_requests.create(
        data={
            "slices": payload["slices"],
            "passengers": payload["passengers"],
            "cabin_class": payload.get("cabin_class", "economy"),
            "max_connections": payload.get("max_connections", 0),
        }
    )

    return {
        "offer_request_id": offer_request["data"]["id"],
        "offers_count": len(offer_request["data"].get("offers", [])),
        "offers": offer_request["data"].get("offers", []),
    }
