import re
from datetime import datetime, timezone
from db import SessionLocal, CustomerLead

EMAIL_RE = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+(\.[A-Za-z0-9-]+)*\.[A-Za-z]{2,}$")


def validate_contact(email, whatsapp_number):
    """Return None if the email and WhatsApp number look valid, otherwise a dict with a status and a message."""
    if email and not EMAIL_RE.match(email.strip()):
        return {"status": "INVALID_EMAIL", "message": "The email address does not look valid. Ask the customer to check it and type it again."}
    if whatsapp_number:
        cleaned = re.sub(r"[\s\-().]", "", whatsapp_number)
        if not re.match(r"^\+?\d{8,15}$", cleaned):
            return {"status": "INVALID_PHONE", "message": "The WhatsApp number does not look valid. Ask the customer to type it again with the country code, for example +94771234567."}
    return None


def create_lead(data):
    now = datetime.now(timezone.utc).isoformat()
    s = SessionLocal()
    lead = CustomerLead(
        **data,
        lead_status="New Enquiry",
        consent_timestamp=now,
        created_at=now,
        updated_at=now,
    )
    s.add(lead)
    s.commit()
    lead_id = lead.id
    s.close()
    return lead_id


def get_lead(lead_id):
    s = SessionLocal()
    lead = s.get(CustomerLead, lead_id)
    result = None
    if lead is not None:
        result = {c.name: getattr(lead, c.name) for c in lead.__table__.columns}
    s.close()
    return result
