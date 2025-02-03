import { useEffect, useState } from "react";

function ClockWidget() {
  const [time, setTime] = useState(new Date().toLocaleTimeString('sv-SE'));

  useEffect(() => {
    const interval = setInterval(() => {
      setTime(new Date().toLocaleTimeString('sv-SE'));
    }, 1000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="widget clock">
      <h2>⏰ Clock</h2>
      <p>{time}</p>
    </div>
  );
}

export default ClockWidget;