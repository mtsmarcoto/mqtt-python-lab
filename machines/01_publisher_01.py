import time
import json
import random
import paho.mqtt.client as mqtt


BROKER_HOST = "localhost"
BROKER_PORT = 1883
TOPIC = "lab/test"


client = mqtt.Client(
    callback_api_version=mqtt.CallbackAPIVersion.VERSION2,
    client_id="publisher-01"
)

client.connect(BROKER_HOST, BROKER_PORT)
client.loop_start()

print("Publisher running. Sending messages...")

counter = 0

while True:
    counter += 1

    payload = {
        "device_id": "virtual-device-01",
        "counter": counter,
        "temperature_c": round(random.uniform(24.0, 30.0), 2)
    }

    payload_json = json.dumps(payload)

    client.publish(TOPIC, payload_json)

    print(f"Published to {TOPIC}: {payload_json}")

    time.sleep(2)