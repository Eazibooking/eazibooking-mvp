import os
import requests


DUFFEL_BASE_URL = "https://api.duffel.com/air/offer_requests"


class DuffelClient:
    def __init__(self, token: str | None = None):
        self.token = token or os.getenv("DUFFEL_TOKEN")
        if not self.token:
            raise RuntimeError("DUFFEL_TOKEN is missing in environment variables.")

    def create_offer_request(self, data: dict) -> dict:
        """
        Calls Duffel API: POST /air/offer_requests?return_offers=true
        Docs: https://duffel.com/docs (Offer Requests)
        """
        headers = {
            "Accept-Encoding": "gzip",
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Duffel-Version": "v2",
            "Authorization": f"Bearer {self.token}",
        }

        payload = {"data": data}

        r = requests.post(
            DUFFEL_BASE_URL,
            params={"return_offers": "true"},
            headers=headers,
            json=payload,
            timeout=30,
        )

        # Raise a clean error if Duffel returns non-200
        try:
            body = r.json()
        except Exception:
            body = {"error": r.text}

        if r.status_code >= 400:
            raise RuntimeError(f"Duffel error {r.status_code}: {body}")

        return body
