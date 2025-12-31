from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

from duffel_client import search_flights_duffel

app = FastAPI(title="EaziBooking API")


class Slice(BaseModel):
    origin: str
    destination: str
    departure_date: str  # YYYY-MM-DD


class Passenger(BaseModel):
    type: str = "adult"  # adult / child / infant_without_seat / infant_with_seat etc.


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
async def flights_search(payload: FlightSearchRequest):
    try:
        return search_flights_duffel(payload.model_dump())
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
