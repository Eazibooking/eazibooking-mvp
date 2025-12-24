from __future__ import annotations

from typing import Any, Dict, List, Protocol


class HotelProvider(Protocol):
    async def search(self, city: str, check_in: str, check_out: str, guests: int = 2) -> List[Dict[str, Any]]:
        ...

    async def book(self, offer_id: str, traveler: Dict[str, Any], payment: Dict[str, Any]) -> Dict[str, Any]:
        ...


class StubHotelProvider:
    """Replace this with Expedia Rapid / Hotelbeds provider once you have credentials."""

    async def search(self, city: str, check_in: str, check_out: str, guests: int = 2) -> List[Dict[str, Any]]:
        return [
            {
                "provider": "stub",
                "hotel_name": "Demo Hotel",
                "city": city,
                "check_in": check_in,
                "check_out": check_out,
                "guests": guests,
                "total_price": {"amount": "199.00", "currency": "USD"},
                "offer_id": "stub_offer_123",
                "refundable": False,
            }
        ]

    async def book(self, offer_id: str, traveler: Dict[str, Any], payment: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "provider": "stub",
            "status": "CONFIRMED",
            "offer_id": offer_id,
            "confirmation_number": "STUB-ABC123",
            "traveler": traveler,
            "note": "This is a stub booking. Plug in a real hotel provider to make real reservations."
        }
