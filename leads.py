from datetime import datetime, timezone
from db import SessionLocal, CustomerLead


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
