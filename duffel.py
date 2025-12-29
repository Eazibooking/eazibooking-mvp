import os
import requests

DUFFEL_API_KEY = os.getenv("DUFFEL_ACCESS_TOKEN")
DUFFEL_API_URL = "https://api.duffel.com/air/offer_requests"

HEADERS = {
    "Authorization": f"Bearer {DUFFEL_API_KEY}",
    "Content-Type": "application/json",
    "Duffel-Version": "beta"
}

def search_flights(payload: dict):
    response = requests.post(
        DUFFEL_API_URL,
        headers=HEADERS,
        json={"data": payload}
    )
    response.raise_for_status()
    return response.json()
