from core.base_module import BaseModule
import google.generativeai as genai
from datetime import datetime

class Module(BaseModule):
    def __init__(self, config, event_bus):
        super().__init__(config, event_bus, update_interval=0)
        self.api_key = config.get("api_key")
        self.model_name = config.get("model", "gemini-1.5-flash")
        self.instruction = config.get("instruction", "You are a AI assistant. Greet the user according to the time of day and present the agenda. The output is converted to speech so don't use headers or markdown. Be brief and concise.")
        self.pending_greeting = {}
        if self.api_key:
            genai.configure(api_key=self.api_key)
        else:
            print("⚠️ No API key provided for Gemini AI.")

        # Subscribe to face detection events
        self.on_event("face_detected", self.handle_face_detected)

        # Subscribe to responses
        self.on_event("agenda_response", self.handle_agenda_response)
        self.on_event("weather_update", self.handle_weather_response)

    def handle_face_detected(self, data):
        try:
            """Handles face detection and generates a greeting."""
            name = data.get("name", "Stranger")
            print(f"🔍 Face detected: {name}, fetching agenda and weather...")

            # Request agenda and weather via event bus
            self.emit_event("fetch_agenda", {"name": name})

            # Store data temporarily
            self.pending_greeting = {"name": name, "agenda": "No agenda", "weather": "Unknown weather"}

        except Exception as e:
            print(f"⚠️ Error handling face detection: {e}")


    def handle_agenda_response(self, data):
        """Receives agenda from the calendar module."""
        self.pending_greeting["agenda"] = data.get("events", "No agenda")
        self.check_ready_to_generate()

    def handle_weather_response(self, data):
        """Receives weather from the weather module."""
        print(f"🌤️ Received weather response")
        weather_summary = data["summary"]
        self.pending_greeting["weather"] = data.get("summary", "Unknown weather")
        self.check_ready_to_generate()

    def check_ready_to_generate(self):
        """Checks if both agenda and weather are available before generating greeting."""
        print(f"🔍 Checking if ready to generate greeting...")
        if "No agenda" not in self.pending_greeting["agenda"] or "Unknown weather" not in self.pending_greeting["weather"]:
            self.generate_greeting(
                self.pending_greeting["name"],
                self.pending_greeting["agenda"],
                self.pending_greeting["weather"],
            )

    def generate_greeting(self, name, agenda, weather):
        """Calls Gemini AI to generate a greeting."""
        print(f"🚀 Generating greeting for {name}...")
        if not self.api_key:
            return "I can't generate a greeting, missing API key."

        try:
            model = genai.GenerativeModel(
                model_name=self.model_name,
                system_instruction=(
                    self.instruction
                ),
            )
            prompt = f"Name: {name}. Current Time: {datetime.now()} Todays agenda: {agenda}. Current weather: {weather}"
            response = model.generate_content(prompt)
            print(f"🎉 Generated greeting: {response.text}")
            self.emit_event("greeting_text", {"greeting": response.text})
            self.pending_greeting = {"name": "None", "agenda": "No agenda", "weather": "Unknown weather"}
            return response.text if response else "I couldn't generate a response."
        except Exception as e:
            print(f"⚠️ Error generating greeting: {e}")
            return "Something went wrong."

    def update(self):
        """This module doesn't need a frequent update cycle."""
        pass