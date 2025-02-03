import { useEffect, useState } from "react";

function WeatherWidget() {
  const [weather, setWeather] = useState("Loading...");

  useEffect(() => {
    fetch("http://localhost:8000/weather")
      .then(response => response.text())
      .then(data => JSON.parse(data))
      .then(data => setWeather(data.weather))
      .catch(() => setWeather("Weather unavailable"));
  }, []);

  return (
    <div className="widget weather">
      <h2>🌤️ Weather</h2>
      <p>{weather}</p>
    </div>
  );
}

export default WeatherWidget;