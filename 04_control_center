import json
import time
import threading
import paho.mqtt.client as mqtt

mqtt_connected = threading.Event()

BROKER_HOST = "localhost"
BROKER_PORT = 1883

TOPIC_TELEMETRY = "lab/inverter_01/telemetry"
TOPIC_STATUS = "lab/inverter_01/status"
TOPIC_CONTROL = "lab/inverter_01/control"

latest_telemetry = None
latest_status = None


def on_connect(client, userdata, flags, reason_code, properties):
    print(f"Connected to broker. Reason code: {reason_code}")
    client.subscribe(TOPIC_TELEMETRY)
    client.subscribe(TOPIC_STATUS)
    print(f"Subscribed to topic: {TOPIC_TELEMETRY}")
    print(f"Subscribed to topic: {TOPIC_STATUS}")
    mqtt_connected.set()


def on_message(client, userdata, message):
    global latest_telemetry, latest_status

    try:
        payload = json.loads(message.payload.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        print(f"Invalid message received on topic: {message.topic}")
        return

    if message.topic == TOPIC_TELEMETRY:
        latest_telemetry = payload
    elif message.topic == TOPIC_STATUS:
        latest_status = payload


def show_value(label, source, field=None):
    if source is None:
        print("No message has been received for this topic yet.")
        return

    value = source if field is None else source.get(field, "Field not found")
    print(f"{label}: {json.dumps(value, indent=2)}")


client = mqtt.Client(
    callback_api_version=mqtt.CallbackAPIVersion.VERSION2,
    client_id="control_center",
)

client.on_connect = on_connect
client.on_message = on_message

client.connect(BROKER_HOST, BROKER_PORT)
client.loop_start()

print("Connecting to broker...")

if not mqtt_connected.wait(timeout=10):
    print("Broker connection timed out.")
    client.loop_stop()
    client.disconnect()
    raise SystemExit(1)

print("Control Center running.")

try:
    while True:
        print(f"\nCurrent time: {time.strftime('%Y-%m-%d %H:%M:%S')}")
        print("Request Full Telemetry    : A")
        print("Request Voltage Telemetry : B")
        print("Request Current Telemetry : C")
        print("Request Phase Telemetry   : D")
        print("Request Status            : E")
        print("Control inverter          : control")
        print("Exit                      : exit")

        selected_command = input("Enter your command: ").strip()

        if selected_command.lower() == "exit":
            print("Exiting Control Center.")
            break
        elif selected_command.lower() == "control":
            input_command = input("Enter control command (ON/OFF): ").strip()
            command_payload = json.dumps({"command": input_command.upper()})
            client.publish(TOPIC_CONTROL, command_payload)
            print(f"Published control command: {command_payload}")
        elif selected_command.upper() == "A":
            show_value("Full telemetry", latest_telemetry)
        elif selected_command.upper() == "B":
            show_value("Voltage telemetry", latest_telemetry, "voltage_v")
        elif selected_command.upper() == "C":
            show_value("Current telemetry", latest_telemetry, "current_a")
        elif selected_command.upper() == "D":
            show_value("Phase telemetry", latest_telemetry, "phase_angle_deg")
        elif selected_command.upper() == "E":
            show_value("Status", latest_status, "status")
        else:
            print("Invalid command.")
finally:
    client.loop_stop()
    client.disconnect()
