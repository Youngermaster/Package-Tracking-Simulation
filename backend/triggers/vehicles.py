import requests
import json

# Replace with your FastAPI app's base URL if different
BASE_URL = "http://localhost:8000"

# Your user's credentials
credentials = {
    "username": "jane.doe@ecodrive.com",
    "password": "securepassword"
}

# 1. Login
login_endpoint = f"{BASE_URL}/login"

response = requests.post(login_endpoint, data=credentials)
response_data = response.json()

if response.status_code != 200:
    print("Failed to login:", response_data)
    exit()

token = response_data["access_token"]
headers = {
    # This header will pass the token for authorization
    "Authorization": f"Bearer {token}"
}

# 2. Load vehicles from triggers/vehicles.json
try:
    with open("triggers/vehicles.json", "r") as file:
        vehicles = json.load(file)
except Exception as e:
    print(f"Failed to load vehicles data: {str(e)}")
    exit()

# 3. Post vehicles to the API
vehicles_endpoint = f"{BASE_URL}/vehicle/"

for vehicle in vehicles:
    response = requests.post(vehicles_endpoint,
                             json=vehicle, headers=headers)
    if response.status_code != 200:
        print("Failed to add vehicle:", vehicle)
        print("Response:", response.json())
    else:
        print(f"Added vehicle: {vehicle['name']}")
