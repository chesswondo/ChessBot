from abc import ABC, abstractmethod
import numpy

class PiecesDetectionBase(ABC):
    '''Base class for pieces detection.'''
    def __init__(self, config: dict) -> None:
        self.config = config

    @abstractmethod
    def detect(self, image: numpy.ndarray) -> str:
        '''Detects chess_pieces on given image.'''