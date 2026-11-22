from sqlalchemy import create_engine, Column, Integer, String, Boolean, Float
from sqlalchemy.orm import declarative_base, sessionmaker

engine = create_engine("sqlite:///zeylan.db")
Base = declarative_base()
SessionLocal = sessionmaker(bind=engine)

class TourPackage(Base):
    __tablename__ = "tour_packages"
    id = Column(Integer, primary_key=True)
    package_code = Column(String)
    name = Column(String)
    slug = Column(String)
    duration_days = Column(Integer)
    duration_nights = Column(Integer)
    status = Column(String, default="Published")
    ai_enabled = Column(Boolean, default=True)

class PackagePrice(Base):
    __tablename__ = "package_prices"
    id = Column(Integer, primary_key=True)
    package_id = Column(Integer)
    tier = Column(String)
    currency = Column(String, default="USD")
    price_type = Column(String)
    occupancy_type = Column(String)
    selling_price = Column(Float)
    validity_start = Column(String)
    validity_end = Column(String)
    status = Column(String, default="Active")

class CustomerLead(Base):
    __tablename__ = "customer_leads"
    id = Column(Integer, primary_key=True)
    customer_name = Column(String)
    email = Column(String)
    whatsapp_number = Column(String)
    country = Column(String)
    preferred_contact_method = Column(String)
    arrival_date = Column(String)
    departure_date = Column(String)
    adults = Column(Integer)
    children = Column(Integer)
    children_ages = Column(String)
    travel_preferences = Column(String)
    accommodation_preference = Column(String)
    transport_preference = Column(String)
    budget = Column(Float)
    budget_basis = Column(String)
    package_id = Column(Integer)
    assigned_executive = Column(String)
    lead_status = Column(String)
    consent_timestamp = Column(String)
    created_at = Column(String)
    updated_at = Column(String)

Base.metadata.create_all(engine)
