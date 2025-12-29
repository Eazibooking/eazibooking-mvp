from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from duffel import DuffelClient

app = FastAPI(title="EaziBooking API")


class Slice(BaseModel):
    origin: str
    destination: str
    departure_date: str


class Passenger(BaseModel):
    type: str = "adult"


class FlightSearchRequest(BaseModel):
    slices: list[Slice]
    passengers: list[Passenger]
    cabin_class: str | None = None
    max_connections: int | None = None


@app.get("/")
async def root():
    return {"status": "EaziBooking API is live"}


@app.get("/health")
async def health():
    return {"ok": True}


@app.post("/flights/search")
async def flights_search(req: FlightSearchRequest):
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

        return await client.search_flights(payload)

    except RuntimeError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
