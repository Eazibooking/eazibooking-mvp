import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from duffel import DuffelClient

app = FastAPI(title="EaziBooking API")

# ---------- Schemas ----------
class Slice(BaseModel):
    origin: str = Field(..., example="SFO")
    destination: str = Field(..., example="LAX")
    departure_date: str = Field(..., example="2026-04-10")  # YYYY-MM-DD


class Passenger(BaseModel):
    type: str = Field("adult", example="adult")  # adult, child, infant_without_seat, infant_with_seat


class FlightSearchRequest(BaseModel):
    slices: list[Slice]
    passengers: list[Passenger]
    cabin_class: str | None = Field(None, example="economy")  # economy, premium_economy, business, first
    max_connections: int | None = Field(None, example=0)


# ---------- Basic endpoints ----------
@app.get("/")
async def root():
    return {"status": "EaziBooking API is live"}

@app.get("/health")
async def health():
    return {"ok": True}


# ---------- Flights Search ----------
@app.post("/flights/search")
async def flights_search(req: FlightSearchRequest):
    """
    Creates a Duffel Offer Request and returns offers.
    """
    try:
        client = DuffelClient()

        payload = {
            "slices": [s.model_dump() for s in req.slices],
            "passengers": [p.model_dump() for p in req.passengers],
            "return_offers": True,
        }

        if req.cabin_class:
            payload["cabin_class"] = req.cabin_class

        if req.max_connections is not None:
            payload["max_connections"] = req.max_connections

        duffel_json = await client.search_offers(payload)

        # Return Duffel response (you can later “format” it nicely)
        return duffel_json

    except RuntimeError as e:
        # Duffel errors show here clearly
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")
