from __future__ import annotations

import os
from typing import Any, Dict, List
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

from .schemas import (
    FlightSearchRequest, FlightSearchResponse,
    CreateOrderRequest, CreateOrderResponse,
    ChatRequest, ChatResponse
)
from .tools.duffel import DuffelClient
from .tools.hotels import StubHotelProvider
from .llm import run_llm_with_tools


load_dotenv()

app = FastAPI(title="Travel AI Bot MVP", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],

# Serve a tiny landing page
app.mount('/static', StaticFiles(directory=os.path.join(os.path.dirname(__file__), 'static')), name='static')

@app.get('/')
async def root():
    return FileResponse(os.path.join(os.path.dirname(__file__), 'static', 'index.html'))

)


duffel = None
hotel_provider = StubHotelProvider()


@app.on_event("startup")
async def startup() -> None:
    global duffel
    if os.getenv("DUFFEL_ACCESS_TOKEN"):
        duffel = DuffelClient()


@app.get("/health")
async def health() -> Dict[str, Any]:
    return {"ok": True, "env": os.getenv("APP_ENV", "dev")}


@app.post("/flights/search", response_model=FlightSearchResponse)
async def flights_search(req: FlightSearchRequest) -> FlightSearchResponse:
    if duffel is None:
        raise HTTPException(status_code=500, detail="Duffel not configured (missing DUFFEL_ACCESS_TOKEN).")

    offer_req = await duffel.create_offer_request(
        slices=[s.model_dump() for s in req.slices],
        passengers=[p.model_dump(exclude_none=True) for p in req.passengers],
        cabin_class=req.cabin_class,
        max_connections=req.max_connections,
    )

    offers = offer_req.get("offers") or []
    # If offers are not embedded, you can fetch separately:
    if not offers:
        offers = await duffel.list_offers(offer_request_id=offer_req["id"], limit=50)

    return FlightSearchResponse(offer_request_id=offer_req["id"], offers=offers)


@app.post("/flights/book", response_model=CreateOrderResponse)
async def flights_book(req: CreateOrderRequest) -> CreateOrderResponse:
    if duffel is None:
        raise HTTPException(status_code=500, detail="Duffel not configured (missing DUFFEL_ACCESS_TOKEN).")
    order = await duffel.create_order(
        offer_id=req.offer_id,
        passengers=[p.model_dump(exclude_none=True) for p in req.passengers],
        payment=req.payment,
    )
    return CreateOrderResponse(order=order)


@app.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest) -> ChatResponse:
    # Convert messages to OpenAI format
    messages = [{"role": m.role, "content": m.content} for m in req.messages]
    state = dict(req.state or {})

    async def tool_search_flights(args: Dict[str, Any]) -> Dict[str, Any]:
        if duffel is None:
            return {"error": "Duffel not configured."}
        offer_req = await duffel.create_offer_request(
            slices=args["slices"],
            passengers=args["passengers"],
            cabin_class=args.get("cabin_class"),
            max_connections=args.get("max_connections"),
        )
        offers = offer_req.get("offers") or []
        if not offers:
            offers = await duffel.list_offers(offer_request_id=offer_req["id"], limit=30)
        # Store for continuity
        state["last_offer_request_id"] = offer_req["id"]
        return {"offer_request_id": offer_req["id"], "offers": offers}

    async def tool_book_flight(args: Dict[str, Any]) -> Dict[str, Any]:
        if duffel is None:
            return {"error": "Duffel not configured."}
        order = await duffel.create_order(
            offer_id=args["offer_id"],
            passengers=args.get("passengers") or [],
            payment=None,
        )
        state["last_order_id"] = order.get("id")
        return {"order": order}

    async def tool_search_hotels(args: Dict[str, Any]) -> Dict[str, Any]:
        results = await hotel_provider.search(
            city=args["city"],
            check_in=args["check_in"],
            check_out=args["check_out"],
            guests=args.get("guests", 2),
        )
        state["last_hotel_results"] = results
        return {"hotels": results}

    async def tool_book_hotel(args: Dict[str, Any]) -> Dict[str, Any]:
        booking = await hotel_provider.book(
            offer_id=args["offer_id"],
            traveler=args["traveler"],
            payment=args["payment"],
        )
        state["last_hotel_booking"] = booking
        return {"booking": booking}

    tool_handlers = {
        "search_flights": tool_search_flights,
        "book_flight": tool_book_flight,
        "search_hotels": tool_search_hotels,
        "book_hotel": tool_book_hotel,
    }

    new_messages = await run_llm_with_tools(messages=messages, tool_handlers=tool_handlers)
    # Return only last assistant message for UI, but keep full thread if you want
    # We'll return full messages for simplicity.
    return ChatResponse(
        messages=[{"role": m["role"], "content": m.get("content","")} for m in new_messages if m["role"] in ("system","user","assistant")],
        state=state,
    )
