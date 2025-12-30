from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from duffel_client import search_flights

app = FastAPI(title="EaziBooking API")

class Slice(BaseModel):
    origin: str
    destination: str
    departure_date: str  # YYYY-MM-DD

class Passenger(BaseModel):
    type: str = "adult"

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
async def flights_search(body: FlightSearchRequest):
    try:
        s = body.slices[0]
        result = search_flights(
            origin=s.origin,
            destination=s.destination,
            departure_date=s.departure_date,
            passengers=[p.model_dump() for p in body.passengers],
            cabin_class=body.cabin_class or "economy",
            max_connections=body.max_connections or 1
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
