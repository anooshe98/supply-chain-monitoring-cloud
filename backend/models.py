from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime, UTC
from backend.database import Base


class SensorReading(Base):
    __tablename__ = "sensor_readings"

    id = Column(Integer, primary_key=True, index=True)
    shipment_id = Column(String, index=True)

    product = Column(String)
    route_name = Column(String)

    timestamp = Column(DateTime, default=lambda: datetime.now(UTC))

    location = Column(String)
    lat = Column(Float)
    lon = Column(Float)
    temperature = Column(Float)
    humidity = Column(Float)
    shock = Column(Float)
    light = Column(Float)

    status = Column(String)
    risk_score = Column(Float)


class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)

    shipment_id = Column(String)
    location = Column(String)

    alert_type = Column(String)
    severity = Column(String)

    message = Column(String)

    timestamp = Column(DateTime, default=datetime.utcnow)