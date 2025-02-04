import os
import sys
import requests
from icalendar import Calendar
from datetime import datetime, timedelta

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from config_loader import config

def fetch_calendar(name: str):
    """Fetches the ICS calendar from the URL."""
    try:
        ICS_URL = config["calendars"][name]
        response = requests.get(ICS_URL)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"Error fetching calendar: {e}")
        return None

def get_today_events(name: str):
    """Parses the ICS calendar and extracts today's events."""
    ics_data = fetch_calendar(name)
    if not ics_data:
        return "Could not fetch calendar."

    calendar = Calendar.from_ical(ics_data)
    today = datetime.now().date()

    events = []
    for component in calendar.walk():
        if component.name == "VEVENT":
            event_start = component.get("dtstart").dt
            event_summary = component.get("summary")

            # Convert to date if it's a datetime object
            event_date = event_start.date() if isinstance(event_start, datetime) else event_start

            # Check if the event is today
            if event_date == today:
                event_time = event_start.strftime("%H:%M") if isinstance(event_start, datetime) else "All day"
                events.append(f"{event_time}: {event_summary}")

    return "\n".join(events) if events else "No events scheduled today."

# Get 7 days agenda
def get_agenda(name: str):
    """Parses the ICS calendar and extracts the next 7 days' events."""
    person = name if name != 'None' else 'default'
    ics_data = fetch_calendar(person)
    if not ics_data:
        return "Could not fetch calendar."

    calendar = Calendar.from_ical(ics_data)
    today = datetime.now().date()

    events = []
    for component in calendar.walk():
        if component.name == "VEVENT":
            event_start = component.get("dtstart").dt
            event_summary = component.get("summary")

            # Convert to date if it's a datetime object
            event_date = event_start.date() if isinstance(event_start, datetime) else event_start

            # Check if the event is within the next 7 days
            if today <= event_date <= today + timedelta(days=7):
                event_time = event_start.strftime("%H:%M") if isinstance(event_start, datetime) else "All day"
                events.append({ "date": event_date, "time": event_time, "summary": event_summary })


    return events

if __name__ == "__main__":
    print(get_agenda("Robert"))