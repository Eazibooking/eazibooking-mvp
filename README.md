# Travel AI Bot MVP (Python + FastAPI) — Flights (Duffel) + Hotels (stub) + Payments (Stripe-ready)

This is a **basic MVP backend** for a conversational travel booking bot.

- ✅ Flights search + booking via **Duffel**
- ✅ Conversational endpoint (`/chat`) designed for LLM tool-calling
- ✅ Simple REST endpoints for flights (`/flights/*`)
- ✅ Hotels layer included as a **clean interface** (you can plug in Expedia Rapid, Hotelbeds, etc.)
- ✅ Stripe placeholders for charging customers (real payments require your Stripe keys + your chosen booking model)

> You will need API access/credentials:
> - Duffel access token (live + test)
> - Hotel API credentials (e.g., Expedia Rapid / Hotelbeds) — not included
> - OpenAI API key (or swap LLM provider)
> - Stripe secret key (optional for MVP)

## 1) Quickstart

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env
# Fill in keys in .env

uvicorn app.main:app --reload
```

Open:
- API docs: http://127.0.0.1:8000/docs
- Simple chat test: POST http://127.0.0.1:8000/chat

## 2) Environment variables

See `.env.example`.

## 3) What “real booking + payment” means (important)

**Flights (Duffel):**
- You create an **offer request** -> pick an **offer** -> create an **order** (and optionally pay / confirm depending on flow).
Duffel docs:
- Offer requests: https://duffel.com/docs/api/offer-requests/create-offer-request
- Orders: https://duffel.com/docs/api/orders

**Hotels:**
Real hotel booking usually needs a partner API like **Expedia Rapid** or **Hotelbeds** with contracts + compliance.
- Expedia Rapid supports paths “shopping -> booking -> payment” (their docs are partner-gated, but public overview exists).
- Hotelbeds uses Booking API methods (availability/checkrates/bookings).

This code keeps hotels behind an interface so you can plug in the provider you get approved for.

## 4) Recommended MVP path (fastest to launch)

1. Launch **Flights-only** with Duffel (end-to-end booking) + Stripe charge *if your business model requires you to collect payment*.
2. Add **Hotels** using Expedia Rapid (preferred for MVP if you can get access) or Hotelbeds.
3. Add “Trips/Packages” later (bundling is hard; start simple).

## 5) Safety / compliance checklist (do this before going live)

- PCI: Do **not** handle raw card numbers unless you are PCI compliant. Prefer Stripe Checkout / Elements tokenization.
- T&Cs: clearly display fare rules, refundability, baggage, cancellation rules.
- Data privacy: store only what you need; encrypt PII at rest; rotate keys.
- Logging: never log full passport numbers, card data, CVV, etc.

## 6) File structure

- `app/main.py` FastAPI app & routes
- `app/llm.py` LLM wrapper (OpenAI tools-style)
- `app/tools/duffel.py` Duffel client + functions
- `app/tools/hotels.py` Hotel provider interface + stub implementation
- `app/schemas.py` Pydantic request/response models
