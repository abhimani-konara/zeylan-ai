from db import SessionLocal, TourPackage, PackagePrice

s = SessionLocal()
if s.query(PackagePrice).count() == 0:
    lush = s.query(TourPackage).filter_by(slug="lush-getaway").first()
    ceylon = s.query(TourPackage).filter_by(slug="ceylon-getaway").first()
    s.add(PackagePrice(package_id=lush.id, tier="Regular", price_type="Per person", occupancy_type="Double", selling_price=600, validity_start="2026-01-01", validity_end="2027-12-31"))
    s.add(PackagePrice(package_id=lush.id, tier="Gold", price_type="Per person", occupancy_type="Double", selling_price=800, validity_start="2026-01-01", validity_end="2027-12-31"))
    s.add(PackagePrice(package_id=ceylon.id, tier="Gold", price_type="Per person", occupancy_type="Double", selling_price=450, validity_start="2025-01-01", validity_end="2026-01-31"))
    s.commit()
print(s.query(PackagePrice).count(), "demo prices saved")
