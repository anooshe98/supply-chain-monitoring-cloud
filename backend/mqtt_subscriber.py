import json
import requests
import paho.mqtt.client as mqtt

MQTT_BROKER = "localhost"
MQTT_PORT = 1883
MQTT_TOPIC = "supply_chain/readings"

BACKEND_URL = "http://127.0.0.1:8000/readings"


def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT Broker with result code:", rc)
    client.subscribe(MQTT_TOPIC)
    print("Subscribed to topic:", MQTT_TOPIC)


def on_message(client, userdata, msg):
    try:
        payload = msg.payload.decode("utf-8")
        data = json.loads(payload)

        print("MQTT received:", data)

        response = requests.post(BACKEND_URL, json=data)

        print("Forwarded to backend:", response.status_code)

    except Exception as e:
        print("MQTT processing error:", e)


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(MQTT_BROKER, MQTT_PORT, 60)

print("MQTT Subscriber started...")
client.loop_forever()