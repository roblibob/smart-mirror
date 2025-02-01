from .picovoice_tts import PicovoiceTTS
from config_loader import config

def get_tts_engine():
    """Returns the appropriate TTS engine based on config."""
    provider = config["tts"]["provider"]

    if provider == "picovoice":
        return PicovoiceTTS()
    else:
        raise ValueError(f"Unsupported TTS provider: {provider}")