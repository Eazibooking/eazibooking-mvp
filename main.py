from fastapi import FastAPI

app = FastAPI(title="EaziBooking API")

@app.get("/", tags=["home"], summary="Root endpoint")
async def root():
    return {"status": "EaziBooking API is live"}

@app.get("/health")
async def health():
    return {"ok": True}

@app.post("/flights/search")
async def search_flights():
    return {
        "message": "Duffel integration pending",
        "status": "not_connected"
    }
