import random
import time
import threading
import paho.mqtt.client as mqtt
from datetime import datetime
import json

# EMQX Broker details
BROKER_ADDRESS = "localhost"  # Change to your broker address if different
BROKER_PORT = 1883
TOPIC = "package/measurement"

# List of package IDs (replace with your package IDs)
sensor_ids = ["sensor_id_1", "sensor_id_2", "sensor_id_3"]

# Function to generate random measurements
def generate_measurement(sensor_id):
    return {
        "fecha_hora": datetime.now().isoformat(),
        "temperatura": round(random.uniform(-10, 35), 2),
        "latitud": round(random.uniform(-90, 90), 6),
        "longitud": round(random.uniform(-180, 180), 6),
        "id_sensor": sensor_id
    }

# Function to publish data for a single package
def publish_measurements(sensor_id, client):
    # Random time duration between 5 and 15 seconds
    duration = random.randint(5, 15)
    start_time = time.time()
    
    while time.time() - start_time < duration:
        measurement = generate_measurement(sensor_id)
        client.publish(TOPIC, json.dumps(measurement))
        print(f"Published data for {sensor_id}: {measurement}")
        time.sleep(1)  # Send data every second

    print(f"Stopped publishing for {sensor_id}")

# Main function to start threads for each package
def start_simulation():
    client = mqtt.Client()
    client.connect(BROKER_ADDRESS, BROKER_PORT)

    threads = []
    for sensor_id in sensor_ids:
        thread = threading.Thread(target=publish_measurements, args=(sensor_id, client))
        threads.append(thread)
        thread.start()

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

    client.disconnect()

if __name__ == "__main__":
    start_simulation()
