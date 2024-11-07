import paho.mqtt.client as mqtt
from pymongo import MongoClient
import json
from datetime import datetime

# MongoDB and EMQX Broker details
MONGO_URL = "mongodb://root:examplepassword@localhost:27017/?authMechanism=DEFAULT"
DATABASE_NAME = "package_tracking"  # Replace with your database name
COLLECTION_NAME = "measurements_collection"  # Collection to store measurements
BROKER_ADDRESS = "localhost"  # Change to your broker address if different
BROKER_PORT = 1883
TOPIC = "package/measurement"

# Connect to MongoDB
mongo_client = MongoClient(MONGO_URL)
db = mongo_client[DATABASE_NAME]
collection = db[COLLECTION_NAME]

# Define the on_message callback to store received data
def on_message(client, userdata, message):
    payload = json.loads(message.payload.decode())
    print(f"Received message: {payload}")

    # Prepare the document for MongoDB
    document = {
        "fecha_hora": datetime.fromisoformat(payload["fecha_hora"]),
        "temperatura": payload["temperatura"],
        "latitud": payload["latitud"],
        "longitud": payload["longitud"],
        "id_sensor": payload["id_sensor"]
    }
    
    # Insert the document into MongoDB
    collection.insert_one(document)
    print(f"Stored measurement in MongoDB: {document}")

# Setup MQTT client and subscribe to topic
def start_listener():
    client = mqtt.Client()
    client.on_message = on_message
    client.connect(BROKER_ADDRESS, BROKER_PORT)
    client.subscribe(TOPIC)
    client.loop_forever()

if __name__ == "__main__":
    start_listener()
