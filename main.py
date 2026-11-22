from typing import Optional
from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
from db import SessionLocal, TourPackage
from tools import get_package_price
from leads import create_lead, get_lead

app = FastAPI()


def require_admin(key):
    import os
    import secrets
    from dotenv import load_dotenv
    load_dotenv()
    expected = os.getenv("ADMIN_API_KEY")
    if not expected or not key or not secrets.compare_digest(key.encode(), expected.encode()):
        raise HTTPException(status_code=401, detail="Admin key required.")



class LeadIn(BaseModel):
    customer_name: str
    email: Optional[str] = None
    whatsapp_number: Optional[str] = None
    country: Optional[str] = None
    preferred_contact_method: Optional[str] = None
    arrival_date: Optional[str] = None
    departure_date: Optional[str] = None
    adults: int = 1
    children: int = 0
    children_ages: Optional[str] = None
    travel_preferences: Optional[str] = None
    accommodation_preference: Optional[str] = None
    transport_preference: Optional[str] = None
    budget: Optional[float] = None
    budget_basis: Optional[str] = None
    package_id: Optional[int] = None
    consent: bool = False


def pkg_dict(p):
    return {
        "id": p.id,
        "package_code": p.package_code,
        "name": p.name,
        "slug": p.slug,
        "duration_days": p.duration_days,
        "duration_nights": p.duration_nights,
    }


@app.get("/")
def home():
    return {"message": "Zeylan AI is running"}


@app.get("/api/packages")
def list_packages():
    s = SessionLocal()
    rows = s.query(TourPackage).filter(
        TourPackage.status == "Published", TourPackage.ai_enabled == True
    ).all()
    result = [pkg_dict(p) for p in rows]
    s.close()
    return result


@app.get("/api/packages/{package_id}")
def get_package(package_id: int):
    s = SessionLocal()
    p = s.get(TourPackage, package_id)
    result = pkg_dict(p) if p is not None else None
    s.close()
    if result is None:
        raise HTTPException(status_code=404, detail="Package not found")
    return result


@app.get("/api/packages/{package_id}/pricing")
def get_pricing(package_id: int):
    s = SessionLocal()
    exists = s.get(TourPackage, package_id) is not None
    s.close()
    if not exists:
        raise HTTPException(status_code=404, detail="Package not found")
    return get_package_price(package_id)


@app.post("/api/leads")
def post_lead(lead: LeadIn):
    if not lead.consent:
        raise HTTPException(status_code=400, detail="Customer consent is required before saving an enquiry.")
    if not lead.email and not lead.whatsapp_number:
        raise HTTPException(status_code=400, detail="Provide an email or a WhatsApp number.")
    data = lead.model_dump()
    data.pop("consent")
    lead_id = create_lead(data)
    return {
        "lead_id": lead_id,
        "lead_status": "New Enquiry",
        "message": "Enquiry saved. A travel executive will contact you.",
    }


@app.get("/api/leads/{lead_id}")
def read_lead(lead_id: int, x_admin_key: Optional[str] = Header(default=None)):
    require_admin(x_admin_key)
    lead = get_lead(lead_id)
    if lead is None:
        raise HTTPException(status_code=404, detail="Lead not found")
    return lead


from itinerary import create_itinerary, modify_itinerary, get_itinerary

ITINERARY_NOTE = "This itinerary is a proposal. Final pricing and availability require confirmation by a travel executive."


class ItineraryIn(BaseModel):
    destinations: list[str]
    preferences: Optional[dict] = None


class ItineraryChange(BaseModel):
    add: Optional[list[str]] = None
    remove: Optional[list[str]] = None
    nights: Optional[dict] = None
    note: Optional[str] = None


@app.post("/api/itineraries")
def post_itinerary(body: ItineraryIn):
    if not body.destinations:
        raise HTTPException(status_code=400, detail="Provide at least one destination.")
    result = create_itinerary(body.destinations, body.preferences)
    result["note"] = ITINERARY_NOTE
    return result


@app.patch("/api/itineraries/{itinerary_id}")
def patch_itinerary(itinerary_id: int, body: ItineraryChange):
    result = modify_itinerary(
        itinerary_id,
        add=body.add,
        remove=body.remove,
        nights=body.nights,
        note=body.note or "",
    )
    if result is None:
        raise HTTPException(status_code=404, detail="Itinerary not found")
    result["note"] = ITINERARY_NOTE
    return result


@app.get("/api/itineraries/{itinerary_id}")
def read_itinerary(itinerary_id: int):
    result = get_itinerary(itinerary_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Itinerary not found")
    result["note"] = ITINERARY_NOTE
    return result


from fastapi.staticfiles import StaticFiles
from chat_service import send_message


class ChatIn(BaseModel):
    session_id: str
    message: str
    consent: bool = False


@app.post("/api/chat")
def chat_endpoint(body: ChatIn):
    message = body.message.strip()
    if not message:
        raise HTTPException(status_code=400, detail="Message is empty.")
    if len(message) > 1000:
        raise HTTPException(status_code=400, detail="Message is too long.")
    if not (8 <= len(body.session_id) <= 100):
        raise HTTPException(status_code=400, detail="Invalid session id.")
    try:
        reply = send_message(body.session_id, message, body.consent)
    except Exception as e:
        print("CHAT ERROR:", str(e)[:300])
        raise HTTPException(status_code=503, detail="The assistant is busy. Please try again.")
    return {"reply": reply}


app.mount("/static", StaticFiles(directory="static"), name="static")
