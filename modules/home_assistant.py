import requests
import time
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from config_loader import config
from hassapi import Hass

# Home Assistant API settings
LIGHT_ENTITY_ID = config["home_assistant"]["light"]
hass = Hass(hassurl=config["home_assistant"]["url"], token=config["home_assistant"]["api_key"])

def turn_on_light():
    hass.turn_on(LIGHT_ENTITY_ID)
    print("Light turned on.")

def turn_off_light():
    hass.turn_off(LIGHT_ENTITY_ID)

def play_message(text):
    """Simulate playing a message and turning the light on/off."""
    turn_on_light()  # Turn on before speaking
    print(f"Speaking: {text}")
    time.sleep(4)  # Simulate speaking duration
    turn_off_light()  # Turn off after speaking

# Example usage
if __name__ == "__main__":
    play_message("Hello! Welcome to the smart mirror.")