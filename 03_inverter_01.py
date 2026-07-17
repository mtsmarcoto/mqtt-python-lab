# =========================
# Imports
# =========================

import time
import json
import paho.mqtt.client as mqtt
import math


# =========================
# Variables
# =========================

BROKER_HOST = "localhost"
BROKER_PORT = 1883
TOPIC_TELEMETRY = "lab/inverter_01/telemetry"
TOPIC_STATUS = "lab/inverter_01/status"
TOPIC_CONTROL = "lab/inverter_01/control"

STATUS = "OFF"


# =========================
# MQTT callbacks, client and start
# =========================

def on_connect(client, userdata, flags, reason_code, properties):
    print(f"Connected to broker. Reason code: {reason_code}")
    client.subscribe(TOPIC_CONTROL)
    print(f"Subscribed to topic: {TOPIC_CONTROL}")

def on_message(client, userdata, message):
    global STATUS
    payload = message.payload.decode("utf-8")
    print(f"Message received on topic '{message.topic}': {payload}")
    
    if message.topic == TOPIC_CONTROL:
        try:
            command = json.loads(payload)
            if "command" in command:
                STATUS = command["command"]
                print(f"Status updated to: {STATUS}")
            else:
                print("Invalid command format.")
        except json.JSONDecodeError:
            print("Failed to decode JSON command.")

client = mqtt.Client(
    callback_api_version=mqtt.CallbackAPIVersion.VERSION2, 
    client_id="inverter_01"
)

client.on_connect = on_connect
client.on_message = on_message

client.connect(BROKER_HOST, BROKER_PORT)
client.loop_start()


# =========================
# Machine functions
# =========================

def phase_angle():
    """Generate a phase angle that increases over time."""
    t = time.monotonic()
    fgrid = 60  # Frequency in Hz
    theta = (2*math.pi*t*fgrid) % (2*math.pi)  # Phase angle in radians
    if STATUS == "OFF":
        theta = 0
    return theta

def voltages():
    """Generate a sinusoidal voltage value."""
    theta = phase_angle()
    amplitude = 480 * math.sqrt(2)/math.sqrt(3)  # Amplitude in volts
    Va = math.sin(theta)*amplitude
    Vb = math.sin(theta - 2*math.pi/3)*amplitude
    Vc = math.sin(theta + 2*math.pi/3)*amplitude
    
    Voltages = [Va, Vb, Vc, theta]

    if STATUS == "OFF":
        Voltages = [0, 0, 0, 0]
    return Voltages

def currents():
    """Generate a current value based on the voltage and a fixed impedance."""
    Impedance = 10  # Ohms
    Voltages = voltages()
    Voltages = Voltages[:3]  # Exclude phase angle for current calculation
    phase = Voltages[3] if len(Voltages) > 3 else 0
    currents = [V / Impedance for V in Voltages]
    return [currents, Voltages, phase]


# =========================
# Main loop
# =========================

print("Publisher running. Sending messages...")

counter = 0

while True:
    counter += 1
    samples = currents()
    payload_telemetry = {
        "device_id": "inverter_01",
        "counter": counter,
        "timestamp": time.time(),
        "voltage_v": samples[1],
        "current_a": samples[0],
        "phase_angle_deg": samples[2] * 180 / math.pi
    }

    payload_status = {
        "device_id": "inverter_01",
        "status": STATUS,
        "timestamp": time.time()
    }


    client.publish(TOPIC_TELEMETRY, json.dumps(payload_telemetry))
    client.publish(TOPIC_STATUS, json.dumps(payload_status))
    

    print(f"Published to {TOPIC_TELEMETRY}: {json.dumps(payload_telemetry)}")
    print(f"Published to {TOPIC_STATUS}: {json.dumps(payload_status)}")


    time.sleep(2)
