import json
from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Text
from db import Base, engine, SessionLocal

# DEMO DATA: placeholder values, to be replaced with approved company data
STAY_NIGHTS = {
    "Colombo": 1, "Sigiriya": 2, "Kandy": 2, "Nuwara Eliya": 2,
    "Ella": 2, "Yala": 1, "Galle": 2, "Mirissa": 2,
}
TRAVEL_HOURS = {
    frozenset(["Colombo", "Sigiriya"]): 4,
    frozenset(["Sigiriya", "Kandy"]): 3,
    frozenset(["Kandy", "Nuwara Eliya"]): 3,
    frozenset(["Nuwara Eliya", "Ella"]): 3,
    frozenset(["Ella", "Yala"]): 2,
    frozenset(["Yala", "Mirissa"]): 3,
    frozenset(["Mirissa", "Galle"]): 1,
}


class Itinerary(Base):
    __tablename__ = "itineraries"
    id = Column(Integer, primary_key=True)
    created_at = Column(String)


class ItineraryVersion(Base):
    __tablename__ = "itinerary_versions"
    id = Column(Integer, primary_key=True)
    itinerary_id = Column(Integer)
    version_number = Column(Integer)
    stops_json = Column(Text)
    preferences_json = Column(Text)
    change_note = Column(String)
    created_at = Column(String)


Base.metadata.create_all(engine)


def _now():
    return datetime.now(timezone.utc).isoformat()


def validate_itinerary(stops):
    problems = []
    warnings = []
    names = [x["destination"] for x in stops]
    for x in stops:
        if x["destination"] not in STAY_NIGHTS:
            problems.append("Unknown destination: " + x["destination"])
        if x["nights"] < 1:
            problems.append("Nights must be at least 1 for " + x["destination"])
    for a, b in zip(names, names[1:]):
        if a == b:
            problems.append("Same destination twice in a row: " + a)
            continue
        hours = TRAVEL_HOURS.get(frozenset([a, b]))
        if hours is None:
            warnings.append("Route " + a + " to " + b + " not verified; a travel executive must check it.")
        elif hours > 5:
            warnings.append("Long drive (" + str(hours) + " hours) between " + a + " and " + b + ".")
    return {"valid": len(problems) == 0, "problems": problems, "warnings": warnings}


def _result(itinerary_id, version, stops, prefs):
    return {
        "itinerary_id": itinerary_id,
        "version": version,
        "stops": stops,
        "preferences": prefs,
        "total_nights": sum(x["nights"] for x in stops),
        "validation": validate_itinerary(stops),
    }


def _save_version(s, itinerary_id, number, stops, prefs, note):
    s.add(ItineraryVersion(
        itinerary_id=itinerary_id,
        version_number=number,
        stops_json=json.dumps(stops),
        preferences_json=json.dumps(prefs),
        change_note=note,
        created_at=_now(),
    ))
    s.commit()


def create_itinerary(destination_names, preferences=None):
    prefs = preferences or {}
    stops = [{"destination": n, "nights": STAY_NIGHTS.get(n, 1)} for n in destination_names]
    s = SessionLocal()
    it = Itinerary(created_at=_now())
    s.add(it)
    s.commit()
    itinerary_id = it.id
    _save_version(s, itinerary_id, 1, stops, prefs, "original")
    s.close()
    return _result(itinerary_id, 1, stops, prefs)


def modify_itinerary(itinerary_id, add=None, remove=None, nights=None, note=""):
    s = SessionLocal()
    latest = (
        s.query(ItineraryVersion)
        .filter_by(itinerary_id=itinerary_id)
        .order_by(ItineraryVersion.version_number.desc())
        .first()
    )
    if latest is None:
        s.close()
        return None
    stops = json.loads(latest.stops_json)
    prefs = json.loads(latest.preferences_json)
    for name in (remove or []):
        stops = [x for x in stops if x["destination"] != name]
    for name in (add or []):
        stops.append({"destination": name, "nights": STAY_NIGHTS.get(name, 1)})
    for name, n in (nights or {}).items():
        for x in stops:
            if x["destination"] == name:
                x["nights"] = n
    number = latest.version_number + 1
    _save_version(s, itinerary_id, number, stops, prefs, note or "modified")
    s.close()
    return _result(itinerary_id, number, stops, prefs)


def get_itinerary(itinerary_id):
    s = SessionLocal()
    rows = (
        s.query(ItineraryVersion)
        .filter_by(itinerary_id=itinerary_id)
        .order_by(ItineraryVersion.version_number)
        .all()
    )
    result = None
    if rows:
        result = {
            "itinerary_id": itinerary_id,
            "versions": [
                {
                    "version": r.version_number,
                    "stops": json.loads(r.stops_json),
                    "note": r.change_note,
                }
                for r in rows
            ],
        }
    s.close()
    return result
