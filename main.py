from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

from duffel_service import search_flights

app = FastAPI(title="EaziBooking API")


class Slice(BaseModel):
    origin: str
    destination: str
    departure_date: str  # "YYYY-MM-DD"


class Passenger(BaseModel):
    type: str = "adult"  # "adult", "child", etc.


class FlightSearchRequest(BaseModel):
    slices: List[Slice]
    passengers: List[Passenger]
    cabin_class: Optional[str] = "economy"
    max_connections: Optional[int] = 0


@app.get("/")
async def root():
    return {"status": "EaziBooking API is live"}


@app.get("/health")
async def health():
    return {"ok": True}


@app.post("/flights/search")
async def flights_search(payload: FlightSearchRequest):
    try:
        results = search_flights(payload.model_dump())
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
