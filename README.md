# Smart Supply Chain Environmental Monitoring System

## Overview

The Smart Supply Chain Environmental Monitoring System is an Industry 4.0 application designed to monitor environmental conditions during product transportation.

The system simulates IoT sensor data, transfers it via MQTT to a cloud backend, stores it in a database, analyzes shipment risks in real time, generates alerts, sends automatic email notifications, and provides an interactive dashboard for visualization and reporting.

---

## System Architecture

![System Architecture](images/architecture.png)
```
+-----------------------+
|  Sensor Simulator     |
+-----------------------+
            |
            | MQTT
            v
+-----------------------+
|     HiveMQ Cloud      |
+-----------------------+
            |
            v
+-----------------------+
| MQTT Subscriber       |
+-----------------------+
            |
            | REST API
            v
+-----------------------+
| FastAPI Backend       |
| (Render Cloud)        |
+-----------------------+
            |
      SQLite Database
            |
            v
+-----------------------+
| Streamlit Dashboard   |
+-----------------------+
```

---

## Features

- Real-time shipment monitoring
- IoT sensor simulation
- MQTT communication
- GPS route tracking
- Environmental monitoring
- Risk assessment
- Automatic alert generation
- Email notifications
- PDF report generation
- CSV export
- Interactive analytics dashboard
- Multi-shipment support
- Cloud backend deployment

---

## Technologies

### Backend

- FastAPI
- SQLAlchemy
- SQLite
- Uvicorn

### Frontend

- Streamlit
- Plotly
- Pandas
- Matplotlib

### IoT

- MQTT
- HiveMQ Cloud
- Paho MQTT

### Cloud

- Render
- GitHub

### Python Libraries

- Requests
- ReportLab
- Python-dotenv

---

## Project Structure

```
backend/
dashboard/
sensor_simulator/
reports/
requirements.txt
requirements-worker.txt
README.md
```

---

## How to Run

### 1. Start Backend (Cloud)

Backend is deployed on Render.

```
https://supply-chain-backend-vf0m.onrender.com
```

---

### 2. Start MQTT Subscriber

```bash
python backend/mqtt_subscriber.py
```

---

### 3. Start Sensor Simulator

```bash
python sensor_simulator/simulator.py
```

---

### 4. Start Dashboard

```bash
python -m streamlit run dashboard/app.py
```

---

## Cloud Deployment

The backend is deployed on **Render Cloud**.

The system architecture consists of:

- FastAPI Backend (Render)
- HiveMQ Cloud MQTT Broker
- MQTT Subscriber
- SQLite Database
- Streamlit Dashboard
- GitHub Repository

Sensor data is transmitted via MQTT, processed by the backend, stored in the database, and visualized in real time.

---

## AI-Based Risk Assessment

The system continuously evaluates sensor measurements including:

- Temperature
- Humidity
- Shock
- Light intensity

Based on configurable threshold values, a rule-based risk score is calculated and shipments are classified as:

- Normal
- Warning
- Critical

---

## Reporting

The dashboard supports:

- PDF reports
- CSV export
- Shipment history
- KPI summaries
- Trend analysis

---

## Future Improvements

- Docker deployment
- Kubernetes support
- Machine Learning anomaly detection
- Real IoT sensor integration
- User authentication
- Mobile application
- Interactive live maps

---

## Authors

- Anousheh Naderi
- Parnia Halajani