from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional, Literal

from duffel_service import search_flights_duffel

app = FastAPI(title="EaziBooking API")

class Slice(BaseModel):
    origin: str
    destination: str
    departure_date: str  # YYYY-MM-DD

class Passenger(BaseModel):
    type: Literal["adult", "child", "infant_without_seat", "infant_with_seat"] = "adult"

class FlightSearchRequest(BaseModel):
    slices: List[Slice]
    passengers: List[Passenger]
    cabin_class: Optional[str] = "economy"
    max_connections: Optional[int] = 1

@app.get("/")
async def root():
    return {"status": "EaziBooking API is live"}

@app.get("/health")
async def health():
    return {"ok": True}

@app.post("/flights/search")
async def flights_search(req: FlightSearchRequest):
    # Convert to Duffel format (same structure works well for Duffel Offer Requests)
    payload = {
        "slices": [s.model_dump() for s in req.slices],
        "passengers": [p.model_dump() for p in req.passengers],
        "cabin_class": req.cabin_class,
        "max_connections": req.max_connections,
    }
    return search_flights_duffel(payload)
