def calculate_risk(reading):

    risk_score = 0
    alerts = []

    # Temperatur
    if reading.temperature < 2 or reading.temperature > 8:
        risk_score += 35
        alerts.append("Temperature Risk")

    # Luftfeuchtigkeit
    if reading.humidity > 70:
        risk_score += 20
        alerts.append("Humidity Risk")

    # Erschütterung
    if reading.shock > 5:
        risk_score += 30
        alerts.append("Shock Risk")

    # Licht
    if reading.light > 80:
        risk_score += 15
        alerts.append("Light Exposure")

    # Standortabhängige Risiken
    if "Truck" in reading.location:
        risk_score += 10

    # Status bestimmen
    if risk_score >= 80:
        status = "CRITICAL"
    elif risk_score >= 40:
        status = "WARNING"
    else:
        status = "OK"

    return status, risk_score, alerts
def predict_future_risk(current_risk_score):

    if current_risk_score >= 70:
        return "High probability of shipment failure"

    elif current_risk_score >= 40:
        return "Medium future risk detected"

    else:
        return "Shipment conditions stable"
    
def generate_recommendation(status, risk_score):

    if risk_score >= 80:
        return "STOP SHIPMENT immediately"

    elif status == "CRITICAL":
        return "Inspect shipment urgently"

    elif status == "WARNING":
        return "Monitor shipment closely"

    else:
        return "No action required"
def detect_anomaly(reading):

    anomalies = []

    # Extreme Temperaturänderung
    if reading.temperature > 10:
        anomalies.append("Extreme temperature anomaly")

    # Extreme Erschütterung
    if reading.shock > 7:
        anomalies.append("Extreme shock anomaly")

    # Unerwartete Lichtöffnung
    if reading.light > 90:
        anomalies.append("Unexpected package opening")

    return anomalies