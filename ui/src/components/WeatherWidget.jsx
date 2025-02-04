import { useEffect, useState } from "react";

function WeatherWidget() {
    const [weather, setWeather] = useState({ temp: "--", condition: "Loading..." });

    useEffect(() => {
        const fetchWeather = async () => {
            try {
                const response = await fetch("http://localhost:8000/weather");
                const data = await response.text();
                const json = JSON.parse(data);
                const [condition, temp] = json.weather.split(" ");
                setWeather({ condition, temp });
            } catch (error) {
                console.error(error);
                setWeather({ temp: "--", condition: "Weather unavailable" });
            }
        };

        fetchWeather();
        const interval = setInterval(fetchWeather, 600000); // Update every 10 min
        return () => clearInterval(interval);
    }, []);

    return (
        <div className="flex flex-col">
            <span className="text-gray-400 text-xl">{weather.condition}</span>
            <span className="text-white text-6xl font-light tracking-wide">
                {weather.temp}
            </span>
        </div>
    );
}

export default WeatherWidget;