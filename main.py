import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict, Any

from duffel import create_offer_request

app = FastAPI(title="EaziBooking API")

class Slice(BaseModel):
    origin: str
    destination: str
    departure_date: str  # YYYY-MM-DD

class Passenger(BaseModel):
    type: str = "adult"  # adult/child/infant_without_seat/infant_with_seat

class FlightSearchBody(BaseModel):
    slices: List[Slice]
    passengers: List[Passenger] = [Passenger(type="adult")]
    cabin_class: Optional[str] = None
    max_connections: Optional[int] = None

@app.get("/")
async def root():
    return {"status": "EaziBooking API is live"}

@app.get("/health")
async def health():
    return {"ok": True}

@app.post("/flights/search")
async def flights_search(body: FlightSearchBody):
    if not os.getenv("DUFFEL_ACCESS_TOKEN"):
        raise HTTPException(status_code=500, detail="DUFFEL_ACCESS_TOKEN not set in Render env vars.")

    payload: Dict[str, Any] = {
        "slices": [s.model_dump() for s in body.slices],
        "passengers": [p.model_dump() for p in body.passengers],
    }
    if body.cabin_class:
        payload["cabin_class"] = body.cabin_class
    if body.max_connections is not None:
        payload["max_connections"] = body.max_connections

    data = await create_offer_request(payload)
    return {
        "offer_request_id": data["id"],
        "offers": data.get("offers", []),
    }
