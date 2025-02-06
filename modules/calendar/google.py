import requests
import time
from icalendar import Calendar
from datetime import datetime, timedelta
from core.base_module import BaseModule

class Module(BaseModule):
    def __init__(self, config, event_bus):
        super().__init__(config, event_bus, update_interval=600)
        self.calendars = self.parse_calendars(config.get("calendars", []))
        self.cache = {}

    def parse_calendars(self, calendars_list):
        """Converts list of dictionaries into a usable format."""
        calendar_map = {}
        for entry in calendars_list:
            for name, url in entry.items():
                calendar_map[name] = url
        return calendar_map

    def fetch_calendar(self, name):
        """Fetches the ICS calendar for a given name."""
        ics_url = self.calendars.get(name, None)
        if not ics_url:
            print(f"⚠️ No calendar URL found for {name}, skipping fetch.")
            return None

        try:
            response = requests.get(ics_url)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            print(f"⚠️ Error fetching calendar for {name}: {e}")
            return None

    def parse_events(self, ics_data, days=7):
        """Parses ICS data and extracts events for the specified number of days."""
        if not ics_data:
            return []

        calendar = Calendar.from_ical(ics_data)
        today = datetime.now().date()
        upcoming_events = []

        for component in calendar.walk():
            if component.name == "VEVENT":
                event_start = component.get("dtstart").dt
                event_summary = component.get("summary")

                event_date = event_start.date() if isinstance(event_start, datetime) else event_start

                if today <= event_date <= today + timedelta(days=days):
                    event_time = event_start.strftime("%H:%M") if isinstance(event_start, datetime) else "All day"
                    upcoming_events.append({
                        "date": event_date.isoformat(),  # Convert to string (YYYY-MM-DD)
                        "time": event_time,
                        "summary": str(event_summary)
                    })

        return upcoming_events

    def get_agenda(self, name):
        """Fetches and caches agenda for a given name."""
        if name in self.cache:
            return self.cache[name]

        ics_data = self.fetch_calendar(name)
        events = self.parse_events(ics_data, days=7)
        self.cache[name] = events
        return events

    def update(self):
        """Fetches calendar updates every 10 minutes and emits events."""
        print("🔄 Fetching calendar events...")
        for name in self.calendars.keys():
            events = self.get_agenda(name)
            if events:
                self.event_bus.emit("calendar_update", {"name": name, "events": events})
                print(f"📅 {name}'s calendar updated: {len(events)} events")
            else:
                print(f"📅 No events found for {name}.")

        time.sleep(1)  # Sleep for 10 minutes