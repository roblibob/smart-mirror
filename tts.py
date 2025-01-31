import pyttsx3
import subprocess
import os

# Initialize TTS engine
engine = pyttsx3.init()

def speak_text(text):
    """Speaks the given text using macOS 'say' or pyttsx3."""
    if os.name == "posix":
        subprocess.run(["say", text])  # Use macOS built-in TTS
    else:
        engine.say(text)
        engine.runAndWait()