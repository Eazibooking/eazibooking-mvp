from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional
from duffel_client import search_offers

app = FastAPI(title="EaziBooking API")

class Slice(BaseModel):
    origin: str = Field(..., description="IATA code e.g. SFO")
    destination: str = Field(..., description="IATA code e.g. LAX")
    departure_date: str = Field(..., description="YYYY-MM-DD")

class Passenger(BaseModel):
    type: str = Field("adult", description="adult | child | infant_without_seat | infant_with_seat")

class FlightSearchRequest(BaseModel):
    slices: List[Slice]
    passengers: List[Passenger] = [Passenger(type="adult")]
    cabin_class: Optional[str] = Field("economy", description="economy | premium_economy | business | first")
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
        result = search_offers(
            slices=[s.model_dump() for s in payload.slices],
            passengers=[p.model_dump() for p in payload.passengers],
            cabin_class=payload.cabin_class,
            max_connections=payload.max_connections,
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
