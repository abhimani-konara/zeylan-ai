import os
import smtplib
import threading
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()


def _clean(value, limit=80):
    return " ".join(("" if value is None else str(value)).split())[:limit]


def _send(lead_id, data):
    host = os.getenv("SMTP_HOST", "smtp.gmail.com")
    port = int(os.getenv("SMTP_PORT", "465"))
    user = os.getenv("SMTP_USER", "")
    password = os.getenv("SMTP_PASSWORD", "")
    recipients = [x.strip() for x in os.getenv("NOTIFY_TO", "").split(",") if x.strip()]
    if not recipients:
        return
    msg = EmailMessage()
    msg["Subject"] = "New enquiry #" + str(lead_id) + ": " + _clean(data.get("customer_name"), 40)
    msg["From"] = user or recipients[0]
    msg["To"] = ", ".join(recipients)
    lines = [
        "A new enquiry was saved.",
        "",
        "Lead id: " + str(lead_id),
        "Name: " + _clean(data.get("customer_name")),
        "Email: " + _clean(data.get("email")),
        "WhatsApp: " + _clean(data.get("whatsapp_number")),
        "Adults: " + _clean(data.get("adults")),
        "Children: " + _clean(data.get("children")),
        "Travel dates: " + _clean(data.get("arrival_date")),
        "Package id: " + _clean(data.get("package_id")),
        "",
        "Open the staff list (admin key needed) to see all details.",
    ]
    msg.set_content("\n".join(lines))
    if port == 465:
        with smtplib.SMTP_SSL(host, port, timeout=15) as s:
            if user:
                s.login(user, password)
            s.send_message(msg)
    else:
        with smtplib.SMTP(host, port, timeout=15) as s:
            s.ehlo()
            if s.has_extn("starttls"):
                s.starttls()
                s.ehlo()
            if user:
                s.login(user, password)
            s.send_message(msg)


def notify_new_lead(lead_id, data):
    """Send an email about a new lead in the background. Never raises."""
    def run():
        try:
            _send(lead_id, data)
        except Exception as e:
            print("NOTIFY ERROR:", str(e)[:200])
    threading.Thread(target=run, daemon=True).start()
