import time

class BaseModule:
    def __init__(self, config, event_bus, update_interval=5):
        """
        Base class for all modules.
        
        :param config: The module-specific configuration.
        :param event_bus: The global event bus for communication.
        """
        self.config = config
        self.event_bus = event_bus
        self.name = self.__class__.__name__  # Automatically set module name
        self.last_update = 0
        self.update_interval = config.get("update_interval", update_interval)

    def should_update(self):
        """Checks if enough time has passed since the last update."""
        return time.time() - self.last_update >= self.update_interval

    def update(self):
        """Placeholder for module-specific updates. Must be overridden."""
        pass  # Default does nothing

    def run_update(self):
        """Runs the update only if enough time has passed."""
        if self.should_update():
            self.update()
            self.last_update = time.time()

    def emit_event(self, event_name, data=None):
        """Helper method for emitting events."""
        if self.event_bus:
            self.event_bus.emit(event_name, data)
        else:
            print(f"⚠️ {self.name}: EventBus is not available!")

    def on_event(self, event_name, callback):
        """Helper method for listening to events."""
        if self.event_bus:
            self.event_bus.on(event_name, callback)
        else:
            print(f"⚠️ {self.name}: EventBus is not available!")