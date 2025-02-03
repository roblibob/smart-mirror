import { useEffect, useState } from "react";
import { motion } from "framer-motion"; // For smooth animations

function MessageWidget() {
  const [message, setMessage] = useState("Loading...");
  const [isSpeaking, setIsSpeaking] = useState(false);

  useEffect(() => {
    const fetchMessage = async () => {
      try {
        const response = await fetch("http://127.0.0.1:8000/recognized_faces");
        const data = await response.json();
        console.log(data);
        setMessage(data.greeting);
        setIsSpeaking(true); // Start animation when message updates
        setTimeout(() => setIsSpeaking(false), 4000); // Stop animation after 4s
      } catch (error) {
        setMessage("Unable to fetch greeting.");
      }
    };

    fetchMessage();
  }, [message]);

  return (
    <div className="relative bg-gray-900 p-6 rounded-lg shadow-lg flex flex-col items-center justify-center">
      <motion.div
        animate={isSpeaking ? { scale: [1, 1.1, 1] } : {}}
        transition={{ duration: 1, repeat: isSpeaking ? Infinity : 0 }}
        className="absolute w-24 h-24 bg-blue-500 rounded-full opacity-30"
      />
      <h2 className="text-xl font-bold text-white">🤖 AI Says:</h2>
      <p className="text-lg text-white mt-2">{message}</p>
    </div>
  );
}

export default MessageWidget;