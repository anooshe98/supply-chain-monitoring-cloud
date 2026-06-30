import json
import requests
import paho.mqtt.client as mqtt
import os
from dotenv import load_dotenv
load_dotenv()

MQTT_HOST = os.getenv("MQTT_HOST")
MQTT_PORT = int(os.getenv("MQTT_PORT", 8883))
MQTT_USERNAME = os.getenv("MQTT_USERNAME")
MQTT_PASSWORD = os.getenv("MQTT_PASSWORD")
MQTT_TOPIC = os.getenv("MQTT_TOPIC", "supply_chain/readings")
BACKEND_URL = "https://supply-chain-backend-vf0m.onrender.com/readings"

client = mqtt.Client()
client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
client.tls_set()
client.connect(MQTT_HOST, MQTT_PORT, 60)

def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT Broker with result code:", rc)
    client.subscribe(MQTT_TOPIC)
    print("Subscribed to topic:", MQTT_TOPIC)


def on_message(client, userdata, msg):
    try:
        payload = msg.payload.decode("utf-8")
        data = json.loads(payload)

        print("MQTT received:", data)

        response = requests.post(BACKEND_URL, json=data, timeout=60)

        print("Forwarded to backend:", response.status_code)

    except Exception as e:
        print("MQTT processing error:", e)




client.on_connect = on_connect
client.on_message = on_message

client.connect(MQTT_HOST, MQTT_PORT, 60)

print("MQTT Subscriber started...")
client.loop_forever()