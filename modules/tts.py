import os
import subprocess
from modules.tts_providers.factory import get_tts_engine

tts_engine = get_tts_engine()

def speak_text(text: str):
    """Synthesizes speech using the configured TTS engine and plays the audio."""
    audio_file = tts_engine.synthesize(text)

    # Play the generated speech
    if os.name == "posix":
        subprocess.run(["afplay", audio_file])  # macOS
    else:
        subprocess.run(["aplay", audio_file])  # Linux

    os.remove(audio_file)  # Clean up