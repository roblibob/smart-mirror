import requests

API_GREET_URL = "http://127.0.0.1:8000/greet/"
API_UPDATE_URL = "http://127.0.0.1:8000/recognized_faces/"

def get_greeting(name):
    """Fetches a greeting from the API."""
    response = requests.get(API_GREET_URL + name)
    return response.json().get("message", "Hello!")

def update_recognized_face(name, greeting):
    """Sends recognized face data to the UI."""
    data = {"name": name, "greeting": greeting}
    try:
        requests.post(API_UPDATE_URL, json=data, timeout=2)
    except requests.exceptions.RequestException:
        print("Failed to update API")