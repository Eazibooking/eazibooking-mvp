from duffel import search_flights
from fastapi import FastAPI, Request

app = FastAPI(title="EaziBooking API")

@app.post("/flights/search")
async def flights_search(request: Request):
    body = await request.json()
    return search_flights(body)
