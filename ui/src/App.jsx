import { useState, useEffect } from "react";
import BaseWidget from "./components/BaseWidget";
import MessageWidget from "./components/MessageWidget";
import ClockWidget from "./components/ClockWidget";
import CalendarWidget from "./components/CalendarWidget";
import WeatherWidget from "./components/WeatherWidget";

function App() {
  useEffect(() => {
    const socket = new WebSocket("ws://localhost:8000/ws");
  
    socket.onmessage = (event) => {
      const data = JSON.parse(event.data);
      console.log("📡 Received event:", data);
  
      if (data.event === "calendar_update") {
        console.log("📅 Calendar Updated:", data.data);
      }
  
      if (data.event === "face_detected") {
        console.log("👀 Face Detected:", data.data);
      }
  
      // Handle different event types here
    };
  
    socket.onclose = () => {
      console.log("❌ WebSocket disconnected");
    };
  
    return () => socket.close(); // Cleanup on unmount
  }, []);
  
  const [widgets, setWidgets] = useState([
    { id: "weather", component: <WeatherWidget /> },
    { id: "clock", component: <ClockWidget /> },
    { id: "calendar", component: <CalendarWidget /> },
    { id: "message", component: <MessageWidget />, extraClass: "col-span-3" },
    // { id: "message", component: <MessageWidget />, extraClass: "col-span-3" },
  ]);

  return (
    <div className="w-screen h-screen bg-black text-white flex">
        <div className="w-screen h-screen grid grid-cols-3 grid-rows-3 gap-4 w-4/5 h-4/5">
          {widgets.map((widget, index) => (
            <BaseWidget key={widget.id} id={widget.id} index={index} extraClass={widget.extraClass}>
              {widget.component}
            </BaseWidget>
          ))}
        </div>
    </div>

  );
}

export default App;