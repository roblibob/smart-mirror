class WebSocketManager {
  constructor(url) {
    this.url = url;
    this.socket = null;
    this.eventListeners = {};
    this.reconnectInterval = 5000; // Reconnect every 5 seconds if disconnected

    this.connect();
  }

  connect() {
    this.socket = new WebSocket(this.url);

    this.socket.onopen = () => {
      console.log("✅ Connected to WebSocket");
    };

    this.socket.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        this.dispatchEvent(data.event, data.data);
      } catch (error) {
        console.error("❌ Error parsing WebSocket message:", error);
      }
    };

    this.socket.onerror = (error) => {
      console.error("⚠️ WebSocket error:", error);
    };

    this.socket.onclose = () => {
      console.log("❌ WebSocket connection closed. Attempting reconnect...");
      setTimeout(() => this.connect(), this.reconnectInterval);
    };
  }

  dispatchEvent(event, data) {
    if (this.eventListeners[event]) {
      this.eventListeners[event].forEach((callback) => callback(data));
    }
  }

  subscribe(event, callback) {
    if (!this.eventListeners[event]) {
      this.eventListeners[event] = [];
    }
    this.eventListeners[event].push(callback);
  }

  unsubscribe(event, callback) {
    if (this.eventListeners[event]) {
      this.eventListeners[event] = this.eventListeners[event].filter(
        (cb) => cb !== callback
      );
    }
  }
}

const websocketManager = new WebSocketManager("ws://127.0.0.1:8000/ws");

export default websocketManager;
