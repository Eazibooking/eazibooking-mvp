from __future__ import annotations

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class Passenger(BaseModel):
    type: str = Field(description="adult|child|infant_without_seat|infant_with_seat")
    given_name: Optional[str] = None
    family_name: Optional[str] = None
    born_on: Optional[str] = Field(default=None, description="YYYY-MM-DD")
    title: Optional[str] = None


class Slice(BaseModel):
    origin: str = Field(description="IATA airport code or city code (e.g., SFO, NYC)")
    destination: str = Field(description="IATA airport code or city code (e.g., LHR)")
    departure_date: str = Field(description="YYYY-MM-DD")


class FlightSearchRequest(BaseModel):
    slices: List[Slice]
    passengers: List[Passenger] = Field(default_factory=lambda: [Passenger(type="adult")])
    cabin_class: Optional[str] = Field(default=None, description="economy|premium_economy|business|first")
    max_connections: Optional[int] = None


class FlightSearchResponse(BaseModel):
    offer_request_id: str
    offers: List[Dict[str, Any]]


class CreateOrderRequest(BaseModel):
    offer_id: str
    # For a real flow, you will collect passenger details here:
    passengers: List[Passenger] = Field(default_factory=list)
    # Payment is handled separately depending on your model.
    # Duffel supports different patterns; start simple then expand.
    payment: Optional[Dict[str, Any]] = None


class CreateOrderResponse(BaseModel):
    order: Dict[str, Any]


class ChatMessage(BaseModel):
    role: str = Field(description="system|user|assistant|tool")
    content: str


class ChatRequest(BaseModel):
    messages: List[ChatMessage]
    # optional: carry state like selected_offer_id, etc.
    state: Dict[str, Any] = Field(default_factory=dict)


class ChatResponse(BaseModel):
    messages: List[ChatMessage]
    state: Dict[str, Any] = Field(default_factory=dict)
