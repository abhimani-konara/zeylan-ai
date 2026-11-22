# Zeylan AI

A chat assistant for Zeylan Island Holidays (Sri Lanka tours). It answers questions about tour packages, drafts simple itineraries, and passes customer enquiries to the travel team.

This is a working demo. Packages, prices, stay nights and travel times are placeholder data, to be replaced with approved company data.

## What it does

- Answers package questions using a database. Prices come only from the price tool, never from the AI's own knowledge.
- If a package has no approved current price, it says a travel executive will prepare a quotation.
- Builds and changes proposed itineraries (destinations and nights), with warnings for unverified routes.
- Collects an enquiry (name, email or WhatsApp number, adults, children, travel dates) one question at a time, and saves it only after the customer ticks a consent checkbox.
- Cannot confirm bookings, take payments or approve discounts. It always says that prices and itineraries are proposals confirmed by a travel executive.

## Safety rules built into the code

- Prices: only from `get_package_price`. If the status is `PRICE_UNAVAILABLE`, no price is shown.
- Consent: the enquiry is saved only when the consent checkbox is ticked. The consent time is stored with the lead.
- Required details: an enquiry is not saved without a contact, adults, children and travel dates.
- Contact checks: email addresses and WhatsApp numbers are checked for a valid format (international numbers are accepted). The format is checked, not whether the number exists.
- Staff access: reading leads needs an admin key sent in the `X-Admin-Key` header.
- Itineraries have no approved price. The assistant offers a quotation by the travel team instead.

## Project files

| File | Purpose |
| --- | --- |
| `main.py` | FastAPI app: package, lead, itinerary and chat endpoints |
| `chat_service.py` | Chat used by the web page (prompt, tools, consent handling) |
| `chat_agent.py` | Tool functions, and a terminal version of the chat for testing |
| `tools.py` | Package search and price lookup |
| `itinerary.py` | Itinerary building, changing and validation |
| `leads.py` | Saving, reading and listing leads, contact validation |
| `db.py` | Database models (SQLite) |
| `seed.py`, `seed_prices.py` | Load demo packages and prices |
| `static/chat.html` | Chat page. `static/widget.js` is a chat bubble for a website |

## Setup (Windows PowerShell)

```powershell
python -m venv venv
venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Create a file named `.env` in the project folder:

Never commit `.env`. It is listed in `.gitignore`.

Load the demo data once:

```powershell
python seed.py
python seed_prices.py
```

## Run

```powershell
python -m uvicorn main:app --reload
```

Open http://127.0.0.1:8000/static/chat.html to chat.

If you change `.env`, stop the server (Ctrl+C) and start it again.

## Main endpoints

| Method and path | Access | Purpose |
| --- | --- | --- |
| `GET /api/packages` | public | List packages |
| `GET /api/packages/{id}/pricing` | public | Approved price for a package |
| `POST /api/chat` | public | Chat message |
| `POST /api/leads` | public | Save an enquiry (needs consent) |
| `GET /api/leads` | admin key | List enquiries (`?status=` and `?limit=`) |
| `GET /api/leads/{id}` | admin key | One enquiry |
| `POST /api/itineraries` | public | Create an itinerary |
| `PATCH /api/itineraries/{id}` | public | Change an itinerary |

Example, reading new enquiries as staff:

```powershell
$key = "your ADMIN_API_KEY"
Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/leads?status=New%20Enquiry" -Headers @{ "X-Admin-Key" = $key }
```

## Tests

```powershell
python test_tools.py
python test_itinerary.py
```

## Known limits and next steps

- Package, price, stay-night and travel-time data are placeholders.
- Staff access is a single shared admin key. A real deployment needs HTTPS and a login for each staff member.
- Saving an enquiry does not notify anyone yet. Staff read new enquiries from the endpoint above. Email or WhatsApp alerts are a next step.
- The database is a local SQLite file. A production setup needs a hosted database and backups.
- Itineraries use simple rules and carry no prices.