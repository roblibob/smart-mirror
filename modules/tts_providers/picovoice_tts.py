import os
import sys
import unicodedata
import re

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from .base import TTSProvider
from config_loader import config

import pvorca

class PicovoiceTTS(TTSProvider):
    """TTS implementation for Picovoice Orca."""

    def __init__(self):
        self.api_key = config["tts"]["api_key"]
        self.model_path = config["tts"]["model"]

    def clean_text(self, text):
        """Sanitizes text for Picovoice TTS by replacing unsupported characters."""
        # Normalize Unicode text to remove hidden special characters
        text = unicodedata.normalize("NFKC", text)
        
        # Replace en dash (–) and em dash (—) with a hyphen (-)
        text = text.replace("–", "-").replace("—", "-")

        # Remove explicitly unsupported characters
        text = re.sub(r"[*%’@…#^&$]", "", text)  # Add more if needed

        return text
    
    def synthesize(self, text: str) -> str:
        """Generates speech using Picovoice Orca."""
        output_file = "output.wav"
        
        # Clean up unallowed characters from the text
        text = self.clean_text(text)
        orca = pvorca.create(access_key=self.api_key, model_path=self.model_path)
        orca.synthesize_to_file(text=text, output_path=output_file)
        return output_file