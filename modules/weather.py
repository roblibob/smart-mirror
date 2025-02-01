import requests
from config_loader import config

def get_weather():
    """Fetches weather data from wttr.in."""
    city = config["weather"]["city"]
    url = f"https://wttr.in/{city}?format=%C+%t"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text.strip()  # Example output: "Clear +5°C"
    except requests.exceptions.RequestException as e:
        print(f"❌ Error fetching weather data: {e}")
        return "Weather unavailable"