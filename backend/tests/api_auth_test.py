import requests

# Replace with your FastAPI app's base URL if different
BASE_URL = "http://192.168.20.94:8001"

# 1. Login
login_endpoint = f"{BASE_URL}/login"
login_data = {
    "username": "john.doe@package-tracking.com",  # Your user's email
    "password": "securepassword"         # Your user's password
}

response = requests.post(login_endpoint, data=login_data)
response_data = response.json()

if response.status_code != 200:
    print("Failed to login:", response_data)
    exit()

token = response_data["access_token"]
headers = {
    # This header will pass the token for authorization
    "Authorization": f"Bearer {token}"
}

# 2. Another request (example: fetch user details)
user_details_endpoint = f"{BASE_URL}/user/me"

response = requests.get(user_details_endpoint, headers=headers)
user_data = response.json()

if response.status_code == 200:
    print("User details:", user_data)
else:
    print("Failed to fetch user details:", user_data)
