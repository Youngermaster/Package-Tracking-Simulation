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

# 2. Load recommendations from triggers/recommendations.json
try:
    with open("triggers/recommendations.json", "r") as file:
        recommendations = json.load(file)
except Exception as e:
    print(f"Failed to load recommendations: {str(e)}")
    exit()

# 3. Post recommendations to the API
recommendation_endpoint = f"{BASE_URL}/recommendation/"

for recommendation in recommendations:
    response = requests.post(recommendation_endpoint,
                             json=recommendation, headers=headers)
    if response.status_code != 200:
        print("Failed to add recommendation:", recommendation)
        print("Response:", response.json())
    else:
        print(f"Added recommendation: {recommendation['title']}")
