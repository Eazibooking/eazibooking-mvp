from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional
from duffel_client import search_flights


app = FastAPI(title="EaziBooking API")


class Slice(BaseModel):
    origin: str = Field(..., example="SFO")
    destination: str = Field(..., example="LAX")
    departure_date: str = Field(..., example="2026-02-15")


class Passenger(BaseModel):
    type: str = Field(..., example="adult")


class FlightSearchRequest(BaseModel):
    slices: List[Slice]
    passengers: List[Passenger]
    cabin_class: Optional[str] = Field("economy", example="economy")
    max_connections: Optional[int] = Field(1, example=1)


@app.get("/")
async def root():
    return {"status": "EaziBooking API is live"}


@app.get("/health")
async def health():
    return {"ok": True}


@app.post("/flights/search")
async def flights_search(req: FlightSearchRequest):
    try:
        payload = req.model_dump()
        result = search_flights(payload)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
