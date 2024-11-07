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

# 2. Load redeemable points from triggers/redeemable.json
try:
    with open("triggers/redeemable.json", "r") as file:
        redeemables = json.load(file)
except Exception as e:
    print(f"Failed to load redeemable points: {str(e)}")
    exit()

# 3. Post redeemable points to the API
redeemable_endpoint = f"{BASE_URL}/redeemable/"

for redeemable in redeemables:
    response = requests.post(redeemable_endpoint,
                             json=redeemable, headers=headers)
    if response.status_code != 200:
        print("Failed to add redeemable point:", redeemable)
        print("Response:", response.json())
    else:
        print(f"Added redeemable point: {redeemable['title']}")
