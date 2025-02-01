from abc import ABC, abstractmethod

class TTSProvider(ABC):
    """Abstract class for TTS engines."""
    
    @abstractmethod
    def synthesize(self, text: str) -> str:
        """Generates speech from text and returns the path to the output audio file."""
        pass