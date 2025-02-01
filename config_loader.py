import yaml
import os
import sys

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "config.yaml")

def load_config():
    """Loads the YAML configuration file and validates it."""
    if not os.path.exists(CONFIG_PATH):
        print(f"❌ Error: Configuration file '{CONFIG_PATH}' not found!")
        sys.exit(1)

    try:
        with open(CONFIG_PATH, "r") as file:
            config = yaml.safe_load(file)

        # Validate required fields
        required_keys = ["calendars", "tts"]
        for key in required_keys:
            if key not in config:
                print(f"❌ Error: Missing required section '{key}' in config.yaml")
                sys.exit(1)

        print("✅ Config loaded successfully!")
        return config

    except yaml.YAMLError as e:
        print(f"❌ YAML Parsing Error: {e}")
        sys.exit(1)

config = load_config()