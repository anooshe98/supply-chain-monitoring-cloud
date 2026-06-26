# Smart Supply Chain Environmental Monitoring System

## Overview

This project is an Industry 4.0 application for monitoring environmental conditions during product transportation.

The system simulates IoT sensor data, analyses shipment risks in real time, generates alerts, sends automatic email notifications, and provides an interactive monitoring dashboard.

---

## Features

- Real-time shipment monitoring
- IoT sensor simulation
- GPS route tracking
- Environmental monitoring
- AI-based risk assessment
- Automatic alert generation
- Email notifications
- PDF report generation
- CSV export
- Analytics dashboard
- Multi-shipment support

---

## Technologies

Backend
- FastAPI
- SQLite
- SQLAlchemy

Frontend
- Streamlit
- Plotly

Python Libraries
- Pandas
- Matplotlib
- ReportLab

---

## Project Structure

backend/
dashboard/
sensor_simulator/
reports/
database/

---

## How to Run

### Backend

```bash
python -m uvicorn backend.main:app --reload
```

### Sensor Simulator

```bash
python sensor_simulator/simulator.py
```

### Dashboard

```bash
python -m streamlit run dashboard/app.py
```

---

## AI Risk Assessment

The system continuously analyses sensor data such as:

- Temperature
- Humidity
- Shock
- Light

Based on these values, an AI-inspired rule-based model calculates a Risk Score and predicts shipment conditions.

---

## Automatic Notifications

The system automatically sends email notifications when WARNING or CRITICAL alerts are detected.

---

## Reporting

The dashboard supports:

- PDF reports
- CSV export
- KPI summaries
- Trend analysis

---

## Author

Anousheh Naderi
Parnia Halajani