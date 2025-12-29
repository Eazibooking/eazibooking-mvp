from fastapi import FastAPI

app = FastAPI()

@app.get("/", tags=["home"], summary="Root endpoint")
async def root():
    return {"status": "EaziBooking API is live"}

@app.get("/health")
async def health():
    return {"ok": True}
from fastapi import FastAPI

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/flights/search")
def search_flights():
    return {
        "message": "Duffel integration pending",
        "status": "not_connected"
    }
