import os
import unicodedata
import piper
import piper_phonemize
import wave
import platform
from core.base_module import BaseModule  # Assumes all modules extend from a base class
from core.config_loader import config
import subprocess

class Module(BaseModule):
    """TTS implementation using Piper's Python API."""

    def __init__(self, config, event_bus):
        super().__init__(config, event_bus)
        self.os_type = platform.system()
        self.models_dir = os.path.abspath("modules/tts/models/")
        self.model_name = config.get("model_name", "en_US-kristin-medium.onnx")
        self.model_path = os.path.join(self.models_dir, self.model_name)
        self.output_dir = config.get("output_dir", "tts_output")  # Directory for saving audio
        os.makedirs(self.output_dir, exist_ok=True)

        # Load Piper model
        self.piper = piper.PiperVoice.load(self.model_path)
        # Listen for TTS requests
        self.on_event("tts_text", self.handle_speak_request)    

    def clean_text(self, text):
        """Sanitizes text for Piper by normalizing Unicode and removing unsupported characters."""
        text = unicodedata.normalize("NFKC", text)  # Normalize Unicode text
        return text

    def phonemize_text(self, text):
        """Applies phonemization using piper-phonemize if enabled."""
        if config.get("phonemize", False):
            return piper_phonemize.phonemize(text, lang="en")  # Adjust language as needed
        return text

    def synthesize(self, text: str, output_file="output.wav", speaker_id=None, length_scale=1.0, noise_scale=0.667, noise_w=0.8, sentence_silence=0.0):
        """Generates speech using Piper and saves it to a WAV file."""
        if not text.strip():
            raise ValueError("❌ Cannot synthesize empty text.")

        output_path = os.path.abspath(output_file)

        # Debugging output
        print(f"🗣️ Generating speech: '{text}' -> {output_path}")

        # Open a WAV file for writing
        with wave.open(output_path, "wb") as wav_file:
            self.piper.synthesize(
                text=text,
                wav_file=wav_file,
                speaker_id=speaker_id,
                length_scale=length_scale,
                noise_scale=noise_scale,
                noise_w=noise_w,
                sentence_silence=sentence_silence
            )

        return output_path

    def handle_speak_request(self, data):
        """Handles text-to-speech requests from the event bus."""
        text = data.get("text", "")
        if not text:
            print("⚠️ No text received for TTS.")
            return

        print(f"🔊 Synthesizing speech: {text}")
        audio_path = self.synthesize(text)
        self.event_bus.emit("tts_start", {"audio_path": audio_path, "text": text})

        if self.os_type == "Darwin":  # macOS
            subprocess.run(["afplay", audio_path], check=True)
        elif self.os_type == "Linux":  # Linux
            subprocess.run(["aplay", audio_path], check=True)
        else:
            print(f"⚠️ Unsupported OS: {self.os_type}. Cannot play audio.")

        self.event_bus.emit("tts_done", {"audio_path": audio_path})