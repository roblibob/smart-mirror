import { useEffect, useState } from "react";

const WEATHER_API_URL = "http://localhost:8000/weather"

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
      today.setHours(12, 0, 0, 0); // Set today to noon to avoid TZ shifts
      const [year, month, day] = dateString.split("-").map(Number);
      const forecastDate = new Date(year, month - 1, day, 12);

      const dayDifference = Math.floor((forecastDate - today) / (1000 * 60 * 60 * 24));
      console.log(dateString, forecastDate, today, dayDifference);
      if (dayDifference === 1) return "Tomorrow";
      return forecastDate.toLocaleDateString("en-US", { weekday: "long" });
    };

    useEffect(() => {
        const fetchWeather = async () => {
            try {
                const response = await fetch(WEATHER_API_URL);
                const data = await response.json();

                // Extract current conditions
                const current = data.current_condition[0];
                const forecast = data.weather.slice(1, 3).map(day => ({
                    day: `${getDayName(day.date)}`, // Convert to "Tomorrow", "Friday", etc.
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
            } catch (error) {
              console.log(error);
                setWeather({
                    condition: "Error fetching data",
                    temp: "--",
                    feelsLike: "--",
                    wind: "--",
                    humidity: "--",
                    forecast: [],
                });
            }
        };

        fetchWeather();
        const interval = setInterval(fetchWeather, 600000); // Refresh every 10 minutes
        return () => clearInterval(interval);
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
                                📅 <strong>{day.day}</strong> <p className="text-gray-400">{day.condition}, {day.maxTemp}/{day.minTemp} 💨 {day.wind}</p>
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