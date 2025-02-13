import { useEffect, useState } from "react";
import { motion } from "framer-motion"; // For smooth animations
import websocketManager from "../utils/websocket";

function MessageWidget() {
  const [message, setMessage] = useState("Loading...");
  const [isSpeaking, setIsSpeaking] = useState(false);

  useEffect(() => {
    const handleTTS = (data) => {
      console.log("🤖 Received AI message:", data);
      setMessage(data.text);
      setIsSpeaking(true);
    };

    websocketManager.subscribe("tts_start", handleTTS);
    websocketManager.subscribe("tts_done", () => setIsSpeaking(false));
    return () => {
      websocketManager.unsubscribe("tts_done", () => setIsSpeaking(false));
      websocketManager.unsubscribe("tts_start", handleTTS);
    };
  }, []);

  if (!isSpeaking) {
    return null;
  }

  return (
    <div className="flex flex-col items-center justify-center w-full h-full">
      <motion.div
        className="relative flex items-center justify-center w-60 h-60 bg-black rounded-full"
        animate={{
          boxShadow: isSpeaking
            ? ["0px 0px 20px #ff0000", "0px 0px 40px #ff3333", "0px 0px 20px #ff0000"]
            : "0px 0px 10px rgba(255, 0, 0, 0.2)",
        }}
        transition={{ duration: 0.8, repeat: isSpeaking ? Infinity : 0 }}
      >
        {/* HAL's glowing red eye effect */}
        <motion.div
          className="absolute w-48 h-48 bg-red-600 rounded-full border-8 border-red-800"
          animate={{
            scale: isSpeaking ? [1, 1.1, 1] : 1,
            opacity: isSpeaking ? [0.8, 1, 0.8] : 1,
          }}
          transition={{ duration: 1.5, repeat: isSpeaking ? Infinity : 0, ease: "easeInOut" }}
        />

        {/* Light reflection */}
        <motion.div
          className="absolute w-10 h-10 bg-white rounded-full opacity-40"
          animate={{ x: [10, -10, 10], y: [-10, 10, -10] }}
          transition={{ duration: 3, repeat: Infinity, ease: "easeInOut" }}
        />
      </motion.div>

      {/* AI message text BELOW the animation */}
      <motion.p
        className="text-white text-lg mt-8 text-center px-6 max-w-md"
        animate={{
          opacity: isSpeaking ? [0.5, 1, 0.5] : 1,
        }}
        transition={{ duration: 1, repeat: isSpeaking ? Infinity : 0 }}
      >
        {message}
      </motion.p>
    </div>
  );
}

export default MessageWidget;