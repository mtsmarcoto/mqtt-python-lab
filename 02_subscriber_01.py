import paho.mqtt.client as mqtt


BROKER_HOST = "localhost"
BROKER_PORT = 1883
TOPIC = "lab/test"


def on_connect(client, userdata, flags, reason_code, properties):
    print(f"Connected to broker. Reason code: {reason_code}")
    client.subscribe(TOPIC)
    print(f"Subscribed to topic: {TOPIC}")


def on_message(client, userdata, message):
    payload = message.payload.decode("utf-8")
    print(f"Message received on topic '{message.topic}': {payload}")


client = mqtt.Client(
    callback_api_version=mqtt.CallbackAPIVersion.VERSION2,
    client_id="subscriber-01"
)

client.on_connect = on_connect
client.on_message = on_message

client.connect(BROKER_HOST, BROKER_PORT)

print("Subscriber running. Waiting for messages...")
client.loop_forever()