from __future__ import annotations

import os
import json
from typing import Any, Dict, List, Callable, Awaitable

from openai import OpenAI


def get_client() -> OpenAI:
    return OpenAI(api_key=os.environ["OPENAI_API_KEY"])


def build_tools() -> List[Dict[str, Any]]:
    # Tool schema used by OpenAI Responses/ChatCompletions tool calling.
    # Keep descriptions short and strict to reduce hallucinations.
    return [
        {
            "type": "function",
            "function": {
                "name": "search_flights",
                "description": "Search flights by creating a Duffel offer request and returning offers.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "slices": {"type": "array", "items": {"type": "object"}},
                        "passengers": {"type": "array", "items": {"type": "object"}},
                        "cabin_class": {"type": ["string", "null"]},
                        "max_connections": {"type": ["integer", "null"]},
                    },
                    "required": ["slices", "passengers"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "book_flight",
                "description": "Create a Duffel order from an offer_id (books the flight).",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "offer_id": {"type": "string"},
                        "passengers": {"type": "array", "items": {"type": "object"}},
                    },
                    "required": ["offer_id", "passengers"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "search_hotels",
                "description": "Search hotels (provider-dependent).",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "city": {"type": "string"},
                        "check_in": {"type": "string"},
                        "check_out": {"type": "string"},
                        "guests": {"type": "integer"},
                    },
                    "required": ["city", "check_in", "check_out"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "book_hotel",
                "description": "Book a hotel offer (provider-dependent).",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "offer_id": {"type": "string"},
                        "traveler": {"type": "object"},
                        "payment": {"type": "object"},
                    },
                    "required": ["offer_id", "traveler", "payment"],
                },
            },
        },
    ]


async def run_llm_with_tools(
    messages: List[Dict[str, str]],
    tool_handlers: Dict[str, Callable[[Dict[str, Any]], Awaitable[Dict[str, Any]]]],
    model: str | None = None,
) -> List[Dict[str, str]]:
    """Executes an LLM loop that can call tools and returns assistant+tool messages appended.

    This uses the Chat Completions tool-calling format for broad compatibility.
    """
    client = get_client()
    model = model or os.getenv("OPENAI_MODEL", "gpt-4.1-mini")
    tools = build_tools()

    # A small system guardrail
    if not messages or messages[0]["role"] != "system":
        messages = [
            {"role": "system", "content": "You are a travel booking assistant. Ask only necessary questions. Use tools for flight/hotel search and booking. Never invent prices or confirmations."}
        ] + messages

    while True:
        resp = client.chat.completions.create(
            model=model,
            messages=messages,
            tools=tools,
            tool_choice="auto",
        )
        msg = resp.choices[0].message

        # If no tool call, we are done
        if not msg.tool_calls:
            messages.append({"role": "assistant", "content": msg.content or ""})
            return messages

        # Append assistant message with tool calls (content may be None)
        messages.append({
            "role": "assistant",
            "content": msg.content or "",
            "tool_calls": [tc.model_dump() for tc in msg.tool_calls],
        })

        # Execute each tool call
        for tc in msg.tool_calls:
            name = tc.function.name
            args = json.loads(tc.function.arguments or "{}")

            if name not in tool_handlers:
                tool_result = {"error": f"Tool not implemented: {name}"}
            else:
                tool_result = await tool_handlers[name](args)

            messages.append({
                "role": "tool",
                "tool_call_id": tc.id,
                "content": json.dumps(tool_result),
            })
