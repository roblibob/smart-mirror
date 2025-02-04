import { useState, useEffect } from "react";

function ClockWidget() {
    const [time, setTime] = useState(new Date());

    useEffect(() => {
        const interval = setInterval(() => setTime(new Date()), 1000);
        return () => clearInterval(interval);
    }, []);

    const formattedTime = time.toLocaleTimeString("sv-SE", {
        hour: "2-digit",
        minute: "2-digit",
        second: "2-digit",
    });

    const formattedDate = time.toLocaleDateString("sv-SE", {
        weekday: "long",
        year: "numeric",
        month: "long",
        day: "numeric",
    });

    return (
        <div className="flex flex-col">
            <span className="text-gray-400 text-xl">{formattedDate}</span>
            <span className="text-white text-6xl font-light tracking-wide">
                {formattedTime}
            </span>
        </div>
    );
}

export default ClockWidget;