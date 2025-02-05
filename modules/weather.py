import requests
from config_loader import config

def get_weather():
    """Fetches weather data from wttr.in."""
    city = config["weather"]["city"]
    url = f"https://wttr.in/{city}?format=j1"
    try:
        response = requests.get(url)
        print(response.text)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"❌ Error fetching weather data: {e}")
        return "Weather unavailable"