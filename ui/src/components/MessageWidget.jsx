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
    <motion.div
      className="relative p-6 rounded-lg shadow-lg flex flex-col items-center justify-center w-full h-full bg-black"
      animate={{
        boxShadow: isSpeaking
          ? ["0px 0px 10px #00ffcc", "0px 0px 30px #00ffcc", "0px 0px 10px #00ffcc"]
          : "0px 0px 10px rgba(0, 255, 204, 0.2)",
      }}
      transition={{ duration: 0.8, repeat: isSpeaking ? Infinity : 0 }}
    >
      <motion.div
        className="absolute inset-0 w-full h-full bg-gradient-to-r from-transparent via-[#00ffcc33] to-transparent"
        animate={{ x: [0, 100, 0] }}
        transition={{ duration: 2, repeat: Infinity, ease: "easeInOut" }}
      />
      <h2 className="text-xl font-bold text-white">🤖 AI Says:</h2>
      <motion.p
        className="text-lg text-white mt-2"
        animate={{
          opacity: isSpeaking ? [0.5, 1, 0.5] : 1,
          scale: isSpeaking ? [1, 1.05, 1] : 1,
        }}
        transition={{ duration: 0.8, repeat: isSpeaking ? Infinity : 0 }}
      >
        {message}
      </motion.p>
    </motion.div>
  );
}

export default MessageWidget;