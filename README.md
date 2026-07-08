# Smart Supply Chain Environmental Monitoring System

## Overview

The **Smart Supply Chain Environmental Monitoring System** is a hybrid cloud-based Industry 4.0 demonstrator developed for monitoring environmental conditions throughout a supply chain.

The system continuously collects environmental sensor data, processes it in the cloud, evaluates shipment risks, stores historical information in a cloud database, and visualizes the results through an interactive web dashboard.

The project demonstrates the integration of IoT communication, cloud computing, data analytics, GPS tracking, and AI-inspired risk assessment.

---

# Features

## Real-Time Monitoring

- Live shipment monitoring
- Current shipment status
- GPS location tracking
- ETA calculation
- Route progress visualization
- Live environmental sensor values

---

## Environmental Parameters

The system monitors:

- Temperature
- Humidity
- Light intensity
- Shock / Vibration
- GPS Position

---

## AI Risk Assessment

The dashboard automatically evaluates shipment quality by calculating a dynamic Risk Score.

Possible outputs include:

- Shipment conditions stable
- Medium future risk detected
- High probability of shipment failure
- Recommended actions

---

## Alert Management

Automatic alert generation for:

- Temperature Risk
- Shock Risk

Each alert contains:

- Severity
- Timestamp
- Shipment ID
- Location
- AI recommendation

---

## Analytics Dashboard

Interactive analytics include:

- Temperature Trend
- Humidity Trend
- Light Exposure Trend
- Shock Trend
- Risk Score Trend
- Alert Distribution
- KPI Overview
- Shipment Statistics

---

## GPS Route Tracking

The dashboard visualizes:

- Planned route
- Current truck position
- Route stations
- Route progress

---

## Reports

The application supports:

- CSV Export
- PDF Report Generation

Generated reports contain:

- Shipment information
- Environmental statistics
- Risk evaluation
- Alert summary

---

# System Architecture

```
Sensor Simulator
        │
        ▼
 HiveMQ Cloud MQTT Broker
        │
        ▼
 MQTT Subscriber
        │
        ▼
 FastAPI Backend
        │
        ▼
 Neon PostgreSQL Database
        │
        ▼
 Streamlit Dashboard
```

---

# Technologies

| Technology | Purpose |
|------------|---------|
| Python | Main programming language |
| FastAPI | REST Backend |
| Streamlit | Dashboard |
| HiveMQ Cloud | MQTT Broker |
| Paho MQTT | MQTT Communication |
| Neon PostgreSQL | Cloud Database |
| SQLAlchemy | ORM |
| Render | Cloud Deployment |
| Plotly | Interactive Charts |
| Pandas | Data Processing |
| ReportLab | PDF Generation |
| Git & GitHub | Version Control |

---

# Project Structure

```
backend/
│
├── main.py
├── database.py
├── models.py
├── mqtt_subscriber.py
├── analytics.py
└── notifications.py

dashboard/
│
└── app.py

sensor_simulator/
│
├── simulator.py
└── routes_config.py

reports/
│
├── PDF Reports
└── CSV Exports

images/

README.md
requirements.txt
```

---

# Dashboard Pages

## Monitoring

Displays:

- Live Shipment Status
- Route Progress
- GPS Tracking
- AI Risk Assessment
- Active Alerts

---

## Analytics

Displays:

- KPI Cards
- Temperature Analysis
- Humidity Analysis
- Light Analysis
- Shock Analysis
- Risk Development
- Alert Statistics

---

## Notifications

Displays:

- Alert History
- Shipment Filter
- Severity Levels
- Download Alert History

---

## Reports

Supports:

- Download Sensor Data as CSV
- Generate PDF Report

---

# Cloud Infrastructure

The project uses a hybrid cloud architecture.

## HiveMQ Cloud

Responsible for:

- MQTT communication
- Sensor data transmission

---

## FastAPI Backend (Render)

Responsible for:

- Receiving MQTT messages
- Risk calculation
- Alert generation
- REST API

---

## Neon PostgreSQL

Responsible for:

- Sensor readings
- Alert history
- Shipment data

---

## Streamlit Dashboard

Responsible for:

- Visualization
- Analytics
- Monitoring
- Reporting

---

# Installation

Clone the repository

```bash
git clone https://github.com/anooshe98/supply-chain-monitoring-cloud.git
```

Install dependencies

```bash
pip install -r requirements.txt
```

Start MQTT Subscriber

```bash
python backend/mqtt_subscriber.py
```

Start Sensor Simulator

```bash
python sensor_simulator/simulator.py
```

Start Dashboard

```bash
streamlit run dashboard/app.py
```

---

# Future Improvements

Possible future extensions:

- ESP32 hardware integration
- Real IoT sensors
- Docker deployment
- Kubernetes
- Machine Learning prediction
- Mobile application
- Email and SMS notifications

---

# Authors


**Anooshe Naderi Khorasgani**

**Parnia Halajani**


---

# Course

**Smart Systems I**

Hochschule Düsseldorf

Summer Semester 2026

Supervisor:

**Prof. Dr.-Ing. Michael Protogerakis**

---

# License

This project was developed for academic purposes as part of the Smart Systems I course at Hochschule Düsseldorf.