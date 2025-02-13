import { useEffect, useState } from "react";
import websocketManager from "../utils/websocket"; // Ensure you have the WebSocket manager

function WeatherWidget() {
  const [weather, setWeather] = useState({
    condition: "Loading...",
    temp: "--",
    feelsLike: "--",
    wind: "--",
    humidity: "--",
    forecast: [],
  });

  const getDayName = (dateString) => {
    const today = new Date();
    today.setHours(12, 0, 0, 0); // Avoid timezone shifts
    const [year, month, day] = dateString.split("-").map(Number);
    const forecastDate = new Date(year, month - 1, day, 12);

    const dayDifference = Math.floor((forecastDate - today) / (1000 * 60 * 60 * 24));
    if (dayDifference === 1) return "Tomorrow";
    return forecastDate.toLocaleDateString("en-US", { weekday: "long" });
  };

  useEffect(() => {
    const handleWeatherUpdate = (data) => {
      console.log("🌦️ Weather update received:", data);

      const current = data.weather.current_condition[0];
      const forecast = data.weather.weather.slice(1, 3).map(day => ({
        day: getDayName(day.date),
        maxTemp: `${day.maxtempC}°C`,
        minTemp: `${day.mintempC}°C`,
        condition: day.hourly[0].weatherDesc[0].value,
        wind: `${(day.hourly[0].windspeedKmph * 0.27778).toFixed(1)} m/s ${day.hourly[0].winddir16Point}`,
      }));

      setWeather({
        condition: current.weatherDesc[0].value,
        temp: `${current.temp_C}°C`,
        feelsLike: `${current.FeelsLikeC}°C`,
        wind: `${(current.windspeedKmph * 0.27778).toFixed(1)} m/s ${current.winddir16Point}`,
        humidity: `${current.humidity}%`,
        forecast,
      });
    };

    websocketManager.subscribe("weather_update", handleWeatherUpdate);
    return () => websocketManager.unsubscribe("weather_update", handleWeatherUpdate);
  }, []);

  return (
    <div className="flex flex-col text-white">
      {/* Current Weather */}
      <div className="text-gray-400 text-xl">🌤️ {weather.condition}</div>
      <div className="text-white text-6xl font-light">{weather.temp}</div>
      <div className="text-gray-400 text-md">Feels like {weather.feelsLike}</div>
      <div className="text-gray-400 text-md">💨 {weather.wind}</div>
      <div className="text-gray-400 text-md">💧 Humidity: {weather.humidity}</div>

      {/* Forecast */}
      <div className="mt-4 w-full">
        <ul className="mt-2">
          {weather.forecast.length > 0 ? (
            weather.forecast.map((day, index) => (
              <li key={index} className="text-white text-md mt-1">
                📅 <strong>{day.day}</strong>
                <p className="text-gray-400">
                  {day.condition}, {day.maxTemp}/{day.minTemp} 💨 {day.wind}
                </p>
              </li>
            ))
          ) : (
            <p className="text-gray-500">No forecast available.</p>
          )}
        </ul>
      </div>
    </div>
  );
}

export default WeatherWidget;