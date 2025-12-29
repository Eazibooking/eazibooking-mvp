from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional

from duffel_client import DuffelClient


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
    max_connections: Optional[int] = 0


@app.get("/", tags=["home"])
async def root():
    return {"status": "EaziBooking API is live"}


@app.get("/health", tags=["health"])
async def health():
    return {"ok": True}


@app.post("/flights/search", tags=["flights"])
async def search_flights(req: FlightSearchRequest):
    try:
        client = DuffelClient()
        result = client.create_offer_request(req.model_dump())
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
