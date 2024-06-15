from abc import ABC, abstractmethod
from typing import Any, List

class SpeechRecognizerBase(ABC):
    '''Base class for speech recognition.'''
    def __init__(self, config: dict) -> None:
        self.config = config

    @abstractmethod
    def record(self) -> Any:
        '''Record audio from micro.'''

    @abstractmethod
    def recognize(self, audio: Any) -> List[str]:
        '''Recognize the given audio.'''