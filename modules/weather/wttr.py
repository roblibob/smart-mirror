import requests
import json
from core.base_module import BaseModule

class Module(BaseModule):
    def __init__(self, config, event_bus):
        super().__init__(config, event_bus, update_interval=600)
        """Initialize the weather module."""
        self.location = self.config.get("location", "Skurup")  # Default location

    def get_weather(self):
        """Fetch weather data from wttr.in."""
        try:
            url = f"https://wttr.in/{self.location}?format=j1"
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            weather_data = response.json()
            summary = self.parse_weather(weather_data)
            return { "weather": weather_data, "summary": summary }
        except requests.RequestException as e:
            print(f"⚠️ Error fetching weather: {e}")
            return "Unknown weather"

    def update(self):
        """Periodically fetch and emit weather updates."""
        weather = self.get_weather()
        self.event_bus.emit("weather_update", weather)

    def parse_weather(self, data):
        """Parses weather data and generates a human-readable summary."""
        try:
            current = data.get("current_condition", [{}])[0]
            location = data.get("nearest_area", [{}])[0].get("areaName", [{}])[0].get("value", "Unknown location")

            temperature = current.get("temp_C", "N/A")
            feels_like = current.get("FeelsLikeC", "N/A")
            weather_desc = current.get("weatherDesc", [{}])[0].get("value", "Unknown conditions")
            humidity = current.get("humidity", "N/A")
            wind_speed = current.get("windspeedKmph", "N/A")
            wind_dir = current.get("winddir16Point", "N/A")
            pressure = current.get("pressure", "N/A")

            # Construct a human-readable summary
            summary = (
                f"The weather in {location} is currently {weather_desc.lower()} "
                f"with a temperature of {temperature}°C (feels like {feels_like}°C). "
                f"Humidity is {humidity}%, wind is blowing {wind_speed} km/h from the {wind_dir}. "
                f"Pressure is {pressure} hPa."
            )

            # Return structured weather data with the generated summary
            return summary
        except Exception as e:
            print(f"⚠️ Error parsing weather data: {e}")
            return { "weather": "Unknown weather", "summary": "Unknown weather" }