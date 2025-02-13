from core.base_module import BaseModule
import google.generativeai as genai
from datetime import datetime, time

class Module(BaseModule):
    def __init__(self, config, event_bus, dependencies):
        super().__init__(config, event_bus, dependencies, update_interval=0)
        self.api_key = config.get("api_key")
        self.model_name = config.get("model", "gemini-1.5-flash")
        self.instruction = config.get("instruction", "You are a AI assistant. Greet the user according to the time of day and present the agenda. The output is converted to speech so don't use headers, markdown. Be brief and concise.")
        if self.api_key:
            genai.configure(api_key=self.api_key)
        else:
            print("⚠️ No API key provided for Gemini AI.")

        # Subscribe to face detection events
        self.on_event("face_detected", self.handle_face_detected)

    def handle_face_detected(self, data):
        try:
            """Handles face detection and generates a greeting."""
            name = data.get("name", "Stranger")
            print(f"🔍 Face detected: {name}, fetching agenda and weather...")

            # Fetch agenda and weather directly
            agenda_data = self.modules["calendar"].get_agenda(name)
            agenda = self.format_agenda(agenda_data)

            weather_data = self.modules["weather"].get_weather()
            self.generate_greeting(name, agenda, weather_data["summary"])
        except Exception as e:
            print(f"⚠️ Error handling face detection: {e}")

    def format_agenda(self, data):
        """Receives agenda from the calendar module."""
        now = datetime.now()
        midnight = datetime.combine(now.date(), time(23, 59, 59))  # Set midnight for today

        filtered_events = []
        for event in data:
            try:
                event_date = datetime.strptime(event["date"], "%Y-%m-%d").date()  # Convert string to date
                event_time = datetime.strptime(event["time"], "%H:%M").time()  # Convert string to time
                event_datetime = datetime.combine(event_date, event_time)
                if now <= event_datetime <= midnight:
                    filtered_events.append(event)
            except Exception as e:
                print(f"⚠️ Error processing agenda event: {event} - {e}")

        return filtered_events

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
            self.emit_event("tts_text", {"text": response.text})
            return response.text if response else "I couldn't generate a response."
        except Exception as e:
            print(f"⚠️ Error generating greeting: {e}")
            return "Something went wrong."

    def update(self):
        """This module doesn't need a frequent update cycle."""
        pass