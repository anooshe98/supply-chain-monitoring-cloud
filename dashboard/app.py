import streamlit as st
import pandas as pd
import requests
import plotly.express as px
from sensor_simulator.routes_config import ROUTES
from streamlit_autorefresh import st_autorefresh
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import os
import matplotlib.pyplot as plt
from reportlab.lib.utils import ImageReader


READINGS_URL = "https://supply-chain-backend-vf0m.onrender.com/readings"
ALERTS_URL = "https://supply-chain-backend-vf0m.onrender.com/alerts"
ACTIVE_ALERTS_URL = "https://supply-chain-backend-vf0m.onrender.com/active-alerts"
def create_pdf_report(shipment_id, latest, df, alerts_df):
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)

    width, height = A4
    y = height - 50

    pdf.setFont("Helvetica-Bold", 18)
    pdf.drawString(50, y, "Smart Supply Chain Report")

    y -= 35
    pdf.setFont("Helvetica", 11)
    pdf.drawString(50, y, "Industry 4.0 Environmental Monitoring Report")

    # Shipment Information
    y -= 50
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(50, y, "Shipment Information")

    y -= 25

    pdf.setFont("Helvetica", 12)
    pdf.drawString(50, y, f"Shipment ID: {shipment_id}")
    y -= 20
    pdf.drawString(50, y, f"Product: {latest['product']}")
    y -= 20
    pdf.drawString(50, y, f"Current Location: {latest['location']}")
    y -= 20
    pdf.drawString(50, y, f"Status: {latest['status']}")
    y -= 20
    pdf.drawString(50, y, f"Risk Score: {latest['risk_score']}")
    y -= 40

    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(50, y, "Executive Summary")

    y -= 25

    pdf.setFont("Helvetica", 12)

    if latest["risk_score"] >= 70:
        summary = "High risk shipment detected. Immediate action recommended."

    elif latest["risk_score"] >= 40:
        summary = "Medium risk shipment detected. Close monitoring recommended."

    else:
        summary = "Shipment operating within normal conditions."

    pdf.drawString(50, y, summary)
    y -= 50
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(50, y, "Key Performance Indicators")

    y -= 30
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(50, y, "Metric")
    pdf.drawString(280, y, "Value")

    y -= 20
    pdf.setFont("Helvetica", 12)

    kpis = [
        ("Total Measurements", len(df)),
        ("Average Temperature", f"{df['temperature'].mean():.1f} °C"),
        ("Average Humidity", f"{df['humidity'].mean():.1f}%"),
        ("Average Risk Score", f"{df['risk_score'].mean():.1f}"),
        ("Maximum Risk Score", f"{df['risk_score'].max():.1f}"),
        ("Warnings", len(df[df["status"] == "WARNING"])),
        ("Critical Events", len(df[df["status"] == "CRITICAL"])),
    ]

    for metric, value in kpis:
        pdf.drawString(50, y, str(metric))
        pdf.drawString(280, y, str(value))
        y -= 20

    # Alert Summary
    y -= 25
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(50, y, "Alert Summary")

    y -= 25
    pdf.setFont("Helvetica", 12)
    pdf.drawString(50, y, f"Stored Alerts: {len(alerts_df)}")

    if not alerts_df.empty and "severity" in alerts_df.columns:
        y -= 20
        warning_count = len(alerts_df[alerts_df["severity"] == "WARNING"])
        critical_count = len(alerts_df[alerts_df["severity"] == "CRITICAL"])
        pdf.drawString(50, y, f"Warning Alerts: {warning_count}")
        y -= 20
        pdf.drawString(50, y, f"Critical Alerts: {critical_count}")

    # Recommendation
    y -= 40
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(50, y, "Recommendation")

    y -= 25
    pdf.setFont("Helvetica", 12)

    if latest["risk_score"] >= 70:
        recommendation = "Stop shipment and inspect product condition immediately."
    elif latest["risk_score"] >= 40:
        recommendation = "Monitor shipment closely and prepare corrective action."
    else:
        recommendation = "No immediate action required."

    pdf.drawString(50, y, recommendation)

    # Charts Page
    pdf.showPage()

    pdf.setFont("Helvetica-Bold", 18)
    pdf.drawString(50, 800, "Sensor Trend Analysis")

    os.makedirs("reports", exist_ok=True)

    # Temperature chart
    temp_chart_file = "reports/temp_chart.png"

    plt.figure(figsize=(7, 3))
    plt.plot(df["temperature"].tail(100).reset_index(drop=True))
    plt.title("Temperature Trend - Last 100 Readings")
    plt.xlabel("Reading")
    plt.ylabel("Temperature °C")
    plt.tight_layout()
    plt.savefig(temp_chart_file)
    plt.close()

    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(50, 760, "Temperature Trend")
    pdf.drawImage(
        temp_chart_file,
        50,
        500,
        width=500,
        height=220
    )

    # Risk chart
    risk_chart_file = "reports/risk_chart.png"

    plt.figure(figsize=(7, 3))
    plt.plot(df["risk_score"].tail(100).reset_index(drop=True))
    plt.title("Risk Score Trend - Last 100 Readings")
    plt.xlabel("Reading")
    plt.ylabel("Risk Score")
    plt.tight_layout()
    plt.savefig(risk_chart_file)
    plt.close()

    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(50, 450, "Risk Score Trend")
    pdf.drawImage(
        risk_chart_file,
        50,
        190,
        width=500,
        height=220
    )
    try:
        os.remove(temp_chart_file)
        os.remove(risk_chart_file)
    except:
        pass

    pdf.save()
    buffer.seek(0)
    return buffer.getvalue()

st.set_page_config(
    page_title="Smart Supply Chain Monitor",
    layout="wide"
)

st.title("Smart Supply Chain Environmental Monitoring")
st.caption("Industrie 4.0 Demonstrator für Umweltparameter-Tracking entlang einer Lieferkette")

page = st.sidebar.selectbox(
    "Navigation",
    [
        "Monitoring",
        "Analytics",
        "Notifications"
    ]
)
#if page == "Monitoring":
   # st_autorefresh(interval=5000, key="dashboard_refresh")

try:
    readings_response = requests.get(READINGS_URL, timeout=5)
    alerts_response = requests.get(ALERTS_URL, timeout=5)
    active_alerts_response = requests.get(ACTIVE_ALERTS_URL, timeout=5)

    readings = readings_response.json()
    alerts = alerts_response.json()
    active_alerts = active_alerts_response.json()

except Exception as e:
    st.warning("Backend antwortet gerade nicht. Letzte Aktualisierung fehlgeschlagen.")
    st.stop()

readings = readings_response.json()
alerts = alerts_response.json()
active_alerts = active_alerts_response.json()
df = pd.DataFrame(readings)
alerts_df = pd.DataFrame(alerts)
if df.empty:
    st.warning("Noch keine Sensordaten vorhanden.")
    st.stop()

df = df.dropna(subset=["lat", "lon"])
df["lat"] = pd.to_numeric(df["lat"], errors="coerce")
df["lon"] = pd.to_numeric(df["lon"], errors="coerce")
df = df.dropna(subset=["lat", "lon"])
if page == "Analytics":

    st.header("📊 Analytics Dashboard")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Total Readings",
        len(df)
    )

    col2.metric(
        "Avg Temp",
        f"{df['temperature'].mean():.1f} °C"
    )

    col3.metric(
        "Avg Humidity",
        f"{df['humidity'].mean():.1f}%"
    )

    col4.metric(
        "Avg Risk",
        f"{df['risk_score'].mean():.1f}"
    )

    st.subheader("Risk Score Trend")

    analytics_df = df.tail(250)

    risk_fig = px.line(
        analytics_df,
        x="id",
        y="risk_score",
        color="shipment_id",
        title="Risk Score Trend - Last 250 Readings"
    )

    st.plotly_chart(
        risk_fig,
        use_container_width=True
    )

    st.subheader("Temperature Trend")

    temp_fig = px.line(
        analytics_df,
        x="id",
        y="temperature",
        color="shipment_id"
    )

    st.plotly_chart(
        temp_fig,
        use_container_width=True
    )

    st.stop()

if page == "Notifications":

    st.header("🔔 Notification Center")

    selected_alert_shipment = st.selectbox(
    "Filter Shipment",
    ["All"] + alerts_df["shipment_id"].unique().tolist()
)

    if selected_alert_shipment != "All":
        alerts_df = alerts_df[
            alerts_df["shipment_id"] == selected_alert_shipment
        ]

    st.dataframe(
        alerts_df.sort_values(
            "timestamp",
            ascending=False
        ),
        use_container_width=True
    )

    if not alerts_df.empty:

        alerts_csv = alerts_df.to_csv(index=False)

        st.download_button(
            label="📥 Download Alert History",
            data=alerts_csv,
            file_name="alert_history.csv",
            mime="text/csv"
        )

    st.stop()

shipment_options = [
    route_data["shipment_id"]
    for route_data in ROUTES.values()
]

selected_shipment = st.selectbox(
    "Select Shipment",
    shipment_options,
    key="selected_shipment"
)

current_route = [
    route_name
    for route_name, route_data in ROUTES.items()
    if route_data["shipment_id"] == selected_shipment
][0]

route_stations = ROUTES[current_route]["stations"]
route_order = [station["location"] for station in route_stations]

df = df[df["shipment_id"] == selected_shipment]
df = df.sort_values("id")

if df.empty:
    st.warning("Noch keine Sensordaten für diese Lieferung vorhanden.")
    st.stop()

latest = df.iloc[-1]
current_location = latest["location"]



if not alerts_df.empty:
    alerts_df = alerts_df[alerts_df["shipment_id"] == selected_shipment]

map_df = df.copy()
chart_df = df.tail(100)
df = chart_df


if df.empty:
    st.warning("Noch keine Sensordaten vorhanden.")
else:
    latest = df.iloc[-1]

    st.subheader("Live Shipment Status")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Shipment", latest["shipment_id"])
    col2.metric("Aktueller Ort", latest["location"])
    col3.metric("Status", latest["status"])
    col4.metric("Risk Score", latest["risk_score"])
    current_location = latest["location"]
    eta_minutes = 0

    try:
        current_index = route_order.index(current_location)
        remaining_stops = len(route_order) - current_index - 1
        eta_minutes = remaining_stops * 30

        st.info(f"🚚 ETA to Destination: {eta_minutes} minutes")

    except:
        st.info("🚚 ETA unavailable")


    st.subheader("🚚 Route Progress")

    try:
        current_index = route_order.index(current_location)
        progress_value = current_index / (len(route_order) - 1)

        st.progress(progress_value)

        st.write(
            f"Stop {current_index + 1} of {len(route_order)}: {current_location}"
        )

    except:
        st.info("Route progress unavailable")
        # Delay Detection

    if eta_minutes >= 90:
        st.warning("⏰ Possible Shipment Delay Detected")
    if latest["risk_score"] >= 70:
        st.error("Prediction: High probability of shipment failure")

    elif latest["risk_score"] >= 40:
        st.warning("Prediction: Medium future risk detected")

    else:
        st.success("Prediction: Shipment conditions stable")
    if latest["risk_score"] >= 80:
        st.error("Recommendation: STOP SHIPMENT immediately")

    elif latest["status"] == "CRITICAL":
        st.warning("Recommendation: Inspect shipment urgently")

    elif latest["status"] == "WARNING":
        st.info("Recommendation: Monitor shipment closely")

    else:
        st.success("Recommendation: No action required")

    if latest["status"] == "CRITICAL":
        st.error("CRITICAL: Lieferung ist gefährdet.")

    elif latest["status"] == "WARNING":
        st.warning("WARNING: Auffälligkeit erkannt.")

    else:
        st.success("OK: Lieferung befindet sich im sicheren Bereich.")
    st.subheader("Active Alerts - last 30 seconds")

    st.subheader("🤖 AI Risk Assessment")

    if latest["risk_score"] >= 70:
        st.error(
            "AI Assessment: High risk detected. Immediate intervention is recommended."
        )

    elif latest["risk_score"] >= 40:
        st.warning(
            "AI Assessment: Medium risk detected. Shipment should be monitored closely."
        )

    else:
        st.success(
            "AI Assessment: Low risk. Shipment is operating under stable conditions."
        )

active_alerts_df = pd.DataFrame(active_alerts)

if active_alerts_df.empty:
    st.success("No active alerts.")
else:
    critical_count = len(active_alerts_df[active_alerts_df["severity"] == "CRITICAL"])
    warning_count = len(active_alerts_df[active_alerts_df["severity"] == "WARNING"])

    c1, c2 = st.columns(2)
    c1.metric("Active Critical Alerts", critical_count)
    c2.metric("Active Warnings", warning_count)

    st.dataframe(active_alerts_df, use_container_width=True)

    st.divider()

    st.subheader("Route Overview")

    route_order = df["location"].drop_duplicates().tolist()

    completed_locations = df["location"].unique().tolist()

    route_status = []

    for location in route_order:
        if location in completed_locations:
            route_status.append({
                "Station": location,
                "Status": "Visited"
            })
        else:
            route_status.append({
                "Station": location,
                "Status": "Pending"
            })

    route_df = pd.DataFrame(route_status)
    st.dataframe(route_df, use_container_width=True)

    st.subheader("📍 GPS Route Tracking")

    current_route = latest["route_name"]

    route_stations = ROUTES[current_route]["stations"]

    gps_df = pd.DataFrame([
    {
        "station": station["location"],
        "lat": station["lat"],
        "lon": station["lon"]
    }
    for station in route_stations
])

    

    fig = px.scatter_mapbox(
    gps_df,
    lat="lat",
    lon="lon",
    hover_name="station",
    zoom=5,
    height=500
)

    fig.add_scattermapbox(
    lat=gps_df["lat"],
    lon=gps_df["lon"],
    mode="lines+markers",
    name="Planned Route"
)
    
    latest_position = map_df.sort_values("id").iloc[-1]
    st.write(latest_position[["shipment_id", "location", "lat", "lon"]])

    fig.add_scattermapbox(
        lat=[latest_position["lat"]],
        lon=[latest_position["lon"]],
        mode="markers",
        marker=dict(size=18),
        text=[f"Current Position: {latest_position['location']}"],
        name="Current Truck Position"
    )

    fig.update_layout(
         mapbox_style="open-street-map"
)

    st.plotly_chart(fig, use_container_width=True)

    st.divider()

    st.subheader("Key Performance Indicators")

    kpi1, kpi2, kpi3, kpi4 = st.columns(4)

    kpi1.metric("Total Measurements", len(df))
    kpi2.metric("Warnings", len(df[df["status"] == "WARNING"]))
    kpi3.metric("Critical Events", len(df[df["status"] == "CRITICAL"]))
    kpi4.metric("Stored Alerts", len(alerts_df) if not alerts_df.empty else 0)

    st.divider()

    st.subheader("Environmental Data Trends")

    fig_temp = px.line(
        df,
        x="id",
        y="temperature",
        color="location",
        title="Temperature by Route Station"
    )
    st.plotly_chart(fig_temp, use_container_width=True)

    fig_humidity = px.line(
        df,
        x="id",
        y="humidity",
        color="location",
        title="Humidity by Route Station"
    )
    st.plotly_chart(fig_humidity, use_container_width=True)

    fig_shock = px.line(
    df,
    x="id",
    y="shock",
    color="location",
    title="Shock by Route Station"
    )
    st.plotly_chart(fig_shock, use_container_width=True)

    fig_light = px.line(
    df,
    x="id",
    y="light",
    color="location",
    title="Light Exposure by Route Station"
    )
    st.plotly_chart(fig_light, use_container_width=True)

    fig_risk = px.line(
        df,
        x="id",
        y="risk_score",
        color="status",
        title="Risk Score Development"
    )
    st.plotly_chart(fig_risk, use_container_width=True)

    st.divider()

    st.subheader("Sensor Data Table")
    st.dataframe(df, use_container_width=True)

    st.divider()

    st.subheader("Alert History")

    if alerts_df.empty:
        st.success("Keine Alerts vorhanden.")
    else:
        st.dataframe(alerts_df, use_container_width=True)

        fig_alerts = px.histogram(
            alerts_df,
            x="alert_type",
            color="severity",
            title="Alert Distribution"
        )
        st.plotly_chart(fig_alerts, use_container_width=True)
    st.subheader("Email Notification Center")

if alerts_df.empty:
    st.info("No email notifications prepared.")
else:
    latest_alert = alerts_df.iloc[-1]

    email_subject = f"{latest_alert['severity']} Alert - {latest_alert['alert_type']}"

    email_body = f"""
Smart Supply Chain Alert

Shipment: {latest_alert['shipment_id']}
Location: {latest_alert['location']}
Severity: {latest_alert['severity']}
Alert Type: {latest_alert['alert_type']}

Message:
{latest_alert['message']}

Recommended Action:
Please check the shipment immediately.
"""

    st.info("Email notification prepared.")
    st.text_input("To", "supply.manager@company.com")
    st.text_input("Subject", email_subject)
    st.text_area("Email Body", email_body, height=250)

st.subheader("📤 Export Reports")

csv_data = df.to_csv(index=False)

st.download_button(
    label="Download Sensor Data as CSV",
    data=csv_data,
    file_name=f"{selected_shipment}_sensor_data.csv",
    mime="text/csv"
)
if st.button("📄 Generate PDF Report"):

    pdf_report = create_pdf_report(
        selected_shipment,
        latest,
        df,
        alerts_df
    )

    import os
    os.makedirs("reports", exist_ok=True)

    pdf_path = f"reports/{selected_shipment}_report.pdf"

    with open(pdf_path, "wb") as f:
        f.write(pdf_report)

    st.success(f"PDF report created: {pdf_path}")