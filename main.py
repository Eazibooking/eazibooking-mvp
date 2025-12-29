from fastapi import FastAPI

app = FastAPI()

@app.get("/", tags=["home"], summary="Root endpoint")
async def root():
    return {"status": "EaziBooking API is live"}

@app.get("/health")
async def health():
    return {"ok": True}
