import time
import json
import random
import paho.mqtt.client as mqtt
import math


BROKER_HOST = "localhost"
BROKER_PORT = 1883
TOPIC1 = "lab/telemetry"
TOPIC2 = "lab/status"
TOPIC3 = "lab/control"

client = mqtt.Client(
    callback_api_version=mqtt.CallbackAPIVersion.VERSION2, 
    client_id="publisher-02_inverter_01"
)

client.connect(BROKER_HOST, BROKER_PORT)
client.loop_start()

print("Publisher running. Sending messages...")

def phase_angle():
    """Generate a phase angle that increases over time."""
    t = time.time()
    fgrid = 60  # Frequency in Hz
    theta = 2*math.pi*t*fgrid
    return theta

def voltages():
    """Generate a sinusoidal voltage value."""
    theta = phase_angle()
    amplitude = 400  # Amplitude in volts
    Va = math.sin(theta)*amplitude
    Vb = math.sin(theta - 2*math.pi/3)*amplitude
    Vc = math.sin(theta + 2*math.pi/3)*amplitude
    
    Voltages = [Va, Vb, Vc]
    return Voltages

def currents():
    """Generate a random current value."""
    Impedance = 10  # Ohms
    Voltages = voltages()
    currents = [V / Impedance for V in Voltages]
    return currents

counter = 0

while True:
    counter += 1

    payload_telemetry = {
        "device_id": "publisher-02_inverter_01",
        "counter": counter,
        "timestamp": time.time(),
        "voltage_v": voltages(),
        "current_a": currents(),
        "phase_angle_deg": phase_angle() * 180 / math.pi
    }

    payload_status = {
        "device_id": "publisher-02_inverter_01",
        "status": random.choice(["ON", "OFF", "FAULT"]),
        "timestamp": time.time()
    }

    payload_control = {
        "device_id": "publisher-02_inverter_01",
        "command": random.choice(["START", "STOP", "RESET"]),
        "timestamp": time.time()
    }

    client.publish(TOPIC1, json.dumps(payload_telemetry))
    client.publish(TOPIC2, json.dumps(payload_status))
    client.publish(TOPIC3, json.dumps(payload_control))

    print(f"Published to {TOPIC1}: {json.dumps(payload_telemetry)}")
    print(f"Published to {TOPIC2}: {json.dumps(payload_status)}")
    print(f"Published to {TOPIC3}: {json.dumps(payload_control)}")

    time.sleep(2)