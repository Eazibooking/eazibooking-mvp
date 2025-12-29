import os
from duffel_api import Duffel

def search_offers(slices, passengers, cabin_class="economy", max_connections=1):
    token = os.getenv("DUFFEL_ACCESS_TOKEN")
    if not token:
        raise Exception("DUFFEL_ACCESS_TOKEN is missing in environment variables")

    duffel = Duffel(access_token=token)

    # Duffel expects max_connections inside slices (optional).
    # We'll add it to each slice if provided.
    duffel_slices = []
    for s in slices:
        item = {
            "origin": s["origin"],
            "destination": s["destination"],
            "departure_date": s["departure_date"],
        }
        if max_connections is not None:
            item["max_connections"] = max_connections
        duffel_slices.append(item)

    offer_request = duffel.offer_requests.create(
        slices=duffel_slices,
        passengers=passengers,
        cabin_class=cabin_class,
    )

    # Return the offers (first ~20 are usually enough for MVP)
    offers = offer_request.offers or []
    return {
        "offer_request_id": offer_request.id,
        "offers_count": len(offers),
        "offers": offers[:20],
    }
