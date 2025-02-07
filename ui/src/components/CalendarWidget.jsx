import { useEffect, useState } from "react";
import websocketManager from "../utils/websocket";

function CalendarWidget() {
  const [events, setEvents] = useState([]);

  useEffect(() => {
    const handleCalendarUpdate = (data) => {
      console.log("📅 Received calendar update:", data);
      setEvents(data.events || []);
    };

    websocketManager.subscribe("calendar_update", handleCalendarUpdate);

    return () => {
      websocketManager.unsubscribe("calendar_update", handleCalendarUpdate);
    };
  }, []);

  const formatDate = (dateStr) => {
    const today = new Date();
    const eventDate = new Date(dateStr);
    const tomorrow = new Date();
    tomorrow.setDate(today.getDate() + 1);

    if (eventDate.toDateString() === today.toDateString()) {
      return "Today";
    } else if (eventDate.toDateString() === tomorrow.toDateString()) {
      return "Tomorrow";
    } else {
      return eventDate.toISOString().split("T")[0]; // YYYY-MM-DD format
    }
  };

  // Group events by date
  const groupedEvents = events.reduce((acc, event) => {
    const dateKey = formatDate(event.date);
    if (!acc[dateKey]) {
      acc[dateKey] = [];
    }
    acc[dateKey].push(event);
    return acc;
  }, {});

  return (
    <div className="flex flex-col">
      <h2 className="text-gray-400 text-xl">📅 Upcoming Events</h2>
      <ul className="mt-2">
        {Object.keys(groupedEvents).length > 0 ? (
          Object.entries(groupedEvents).map(([date, events]) => (
            <div key={date}>
              <h3 className="text-lg font-bold text-white mt-3">{date}</h3>
              {events.map((event, index) => (
                <li key={index} className="text-white text-md mt-1">
                  {event.time} - {event.summary}
                </li>
              ))}
            </div>
          ))
        ) : (
          <p className="text-gray-500">No upcoming events.</p>
        )}
      </ul>
    </div>
  );
}

export default CalendarWidget;