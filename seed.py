from db import SessionLocal, TourPackage

data = [
    ("ZP01", "Tropical trails in Sri Lanka", "tropical-trails-in-sri-lanka", 14, 13),
    ("ZP02", "Tropical Trekker", "tropical-trekker", 10, 9),
    ("ZP03", "Lush Getaway", "lush-getaway", 7, 6),
    ("ZP04", "Island Bliss", "island-bliss", 10, 9),
    ("ZP05", "Ceylon Getaway", "ceylon-getaway", 4, 3),
    ("ZP06", "Beyond the Island", "beyond-the-island", 25, 24),
    ("ZP07", "Wild Wonders of Ceylon", "wild-wonders-of-ceylon", 16, 15),
]

s = SessionLocal()
if s.query(TourPackage).count() == 0:
    for code, name, slug, d, n in data:
        s.add(TourPackage(package_code=code, name=name, slug=slug, duration_days=d, duration_nights=n))
    s.commit()
print(s.query(TourPackage).count(), "packages saved")
