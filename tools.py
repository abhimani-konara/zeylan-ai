from datetime import date
from db import SessionLocal, TourPackage, PackagePrice


def search_packages(min_days=None, max_days=None, keyword=None):
    s = SessionLocal()
    q = s.query(TourPackage).filter(
        TourPackage.status == "Published",
        TourPackage.ai_enabled == True,
    )
    if min_days:
        q = q.filter(TourPackage.duration_days >= min_days)
    if max_days:
        q = q.filter(TourPackage.duration_days <= max_days)
    if keyword:
        q = q.filter(TourPackage.name.ilike("%" + keyword + "%"))
    rows = q.all()
    s.close()
    return [
        {
            "id": p.id,
            "name": p.name,
            "duration_days": p.duration_days,
            "duration_nights": p.duration_nights,
            "slug": p.slug,
        }
        for p in rows
    ]


def get_package_price(package_id):
    s = SessionLocal()
    today = date.today().isoformat()
    rows = s.query(PackagePrice).filter(
        PackagePrice.package_id == package_id,
        PackagePrice.status == "Active",
        PackagePrice.validity_start <= today,
        PackagePrice.validity_end >= today,
    ).all()
    s.close()
    if not rows:
        return {
            "status": "PRICE_UNAVAILABLE",
            "package_id": package_id,
            "message": "No approved current price. A travel executive will provide a quotation.",
        }
    return {
        "status": "OK",
        "package_id": package_id,
        "prices": [
            {
                "tier": r.tier,
                "currency": r.currency,
                "selling_price": r.selling_price,
                "price_type": r.price_type,
                "occupancy_type": r.occupancy_type,
                "valid_until": r.validity_end,
            }
            for r in rows
        ],
        "note": "Price is a proposal. Final price and availability are confirmed by a travel executive.",
    }
