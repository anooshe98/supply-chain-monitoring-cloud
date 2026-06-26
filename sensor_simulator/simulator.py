import requests
import random
import time
import json
import paho.mqtt.client as mqtt
import os

from dotenv import load_dotenv

from routes_config import ROUTES
load_dotenv()

API_URL = "http://127.0.0.1:8000/readings"
MQTT_BROKER = os.getenv("MQTT_HOST")
MQTT_PORT = int(os.getenv("MQTT_PORT", 8883))
MQTT_USERNAME = os.getenv("MQTT_USERNAME")
MQTT_PASSWORD = os.getenv("MQTT_PASSWORD")
MQTT_TOPIC = os.getenv("MQTT_TOPIC", "supply_chain/readings")

mqtt_client = mqtt.Client()
mqtt_client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
mqtt_client.tls_set()
mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)

print("Starting simulation for ALL routes")
print("-" * 50)

while True:
    for route_name, route_data in ROUTES.items():

        product = route_data["product"]
        shipment_id = route_data["shipment_id"]
        stations = route_data["stations"]

        for station in stations:

            data = {
                "shipment_id": shipment_id,
                "product": product,
                "route_name": route_name,
                "location": station["location"],
                "lat": station["lat"],
                "lon": station["lon"],
                "temperature": round(random.uniform(*station["temp_range"]), 2),
                "humidity": round(random.uniform(*station["humidity_range"]), 2),
                "shock": round(random.uniform(*station["shock_range"]), 2),
                "light": round(random.uniform(*station["light_range"]), 2)
            }

            try:
                #response = requests.post(API_URL, json=data)
                response = None
                mqtt_client.publish(MQTT_TOPIC, json.dumps(data))
                print("MQTT sent:", MQTT_TOPIC)

                print("Route:", route_name)
                print("Shipment:", shipment_id)
                print("Location:", station["location"])
                print("Status:", "MQTT sent")
                print("-" * 50)

            except Exception as e:
                print("Error sending data:", e)

            time.sleep(2)