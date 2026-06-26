import smtplib
from email.mime.text import MIMEText
from fastapi import FastAPI, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, timedelta

from .database import Base, engine, SessionLocal
from .models import SensorReading, Alert
from .analytics import calculate_risk, predict_future_risk, generate_recommendation, detect_anomaly
from .notifications import create_email_notification, send_email_alert



Base.metadata.create_all(bind=engine)

app = FastAPI(title="Smart Supply Chain Environmental Monitoring")
last_warning_email = {}
WARNING_EMAIL_INTERVAL = timedelta(minutes=30)

class SensorReadingInput(BaseModel):
    shipment_id: str
    product: str
    route_name: str
    location: str
    lat: float
    lon: float
    temperature: float
    humidity: float
    shock: float
    light: float


class SensorReadingOutput(BaseModel):
    id: int
    shipment_id: str
    product: str
    route_name: str
    location: str
    lat: float
    lon: float
    temperature: float
    humidity: float
    shock: float
    light: float
    status: str
    risk_score: float

    class Config:
        from_attributes = True


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/readings", response_model=SensorReadingOutput)
def create_reading(reading: SensorReadingInput, db: Session = Depends(get_db)):
    status, risk_score, risk_alerts = calculate_risk(reading)
    prediction = predict_future_risk(risk_score)
    recommendation = generate_recommendation(status, risk_score)
    anomalies = detect_anomaly(reading)
    db_reading = SensorReading(
        product=reading.product,
        route_name=reading.route_name,
        shipment_id=reading.shipment_id,
        location=reading.location,
        lat=reading.lat,
        lon=reading.lon,
        temperature=reading.temperature,
        humidity=reading.humidity,
        shock=reading.shock,
        light=reading.light,
        status=status,
        risk_score=risk_score
    )

    db.add(db_reading)
    db.commit()
    db.refresh(db_reading)
            # Intelligente Alerts aus Risk Engine

    for alert_name in risk_alerts:

        alert = Alert(
            shipment_id=reading.shipment_id,
            location=reading.location,
            alert_type=alert_name,
            severity=status,
            message=f"{alert_name} detected at {reading.location}. Prediction: {prediction}. Recommendation: {recommendation}"
        )

        db.add(alert)

        if alert.severity == "CRITICAL":
            email_subject = f"🚨🚨 CRITICAL ALERT | {reading.shipment_id} | {alert.alert_type}"
            severity_label = "CRITICAL - Immediate action required"
            action_level = "URGENT: Stop or inspect shipment immediately."
        else:
            email_subject = f"⚠️ WARNING ALERT | {reading.shipment_id} | {alert.alert_type}"
            severity_label = "WARNING - Monitor shipment closely"
            action_level = "Monitor shipment and inspect if the condition continues."

        email_body = f"""
        Smart Supply Chain Environmental Monitoring

        Shipment ID: {reading.shipment_id}
        Product: {reading.product}
        Current Location: {reading.location}
        Route: {reading.route_name}

        Alert Type: {alert.alert_type}
        Severity Level: {severity_label}
        Risk Score: {risk_score}

        Sensor Values:
        - Temperature: {reading.temperature} °C
        - Humidity: {reading.humidity} %
        - Shock: {reading.shock}
        - Light: {reading.light}

        AI Assessment:
        {prediction}

        Recommended Action:
        {action_level}

        AI Recommendation:
        {recommendation}

        System Message:
        {alert.message}
        """
        
        print("Alert severity:", alert.severity)

        now = datetime.utcnow()

        if alert.severity == "CRITICAL":
            try:
                send_email_alert(email_subject, email_body)
                print("CRITICAL alert email sent.")
            except Exception as e:
                print("Email sending failed:", e)

        elif alert.severity == "WARNING":
            last_sent = last_warning_email.get(reading.shipment_id)

            if last_sent is None or (now - last_sent) > timedelta(minutes=30):
                try:
                    send_email_alert(email_subject, email_body)
                    last_warning_email[reading.shipment_id] = now
                    print("WARNING alert email sent.")
                except Exception as e:
                    print("Email sending failed:", e)


    db.commit()
 
    for anomaly in anomalies:

        anomaly_alert = Alert(
            shipment_id=reading.shipment_id,
            location=reading.location,
            alert_type="ANOMALY",
            severity="CRITICAL",
            message=anomaly
        )

        db.add(anomaly_alert)

    return db_reading


@app.get("/readings", response_model=List[SensorReadingOutput])
def get_readings(db: Session = Depends(get_db)):
    return db.query(SensorReading).all()

@app.get("/alerts")
def get_alerts(db: Session = Depends(get_db)):
    return db.query(Alert).all()

@app.get("/active-alerts")
def get_active_alerts(db: Session = Depends(get_db)):
    time_limit = datetime.utcnow() - timedelta(seconds=30)

    return db.query(Alert).filter(
        Alert.timestamp >= time_limit,
        Alert.severity != "OK"
    ).all()