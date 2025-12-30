import os
from duffel import Duffel

def search_flights(
    origin: str,
    destination: str,
    departure_date: str,
    passengers: list,
    cabin_class: str = "economy",
    max_connections: int = 1
):
    token = os.getenv("DUFFEL_TOKEN")
    if not token:
        raise RuntimeError("DUFFEL_TOKEN is missing in environment variables.")

    duffel = Duffel(access_token=token)

    payload = {
        "slices": [
            {
                "origin": origin,
                "destination": destination,
                "departure_date": departure_date
            }
        ],
        "passengers": passengers,
        "cabin_class": cabin_class,
        "max_connections": max_connections
    }

    return duffel.offer_requests.create(data=payload)
