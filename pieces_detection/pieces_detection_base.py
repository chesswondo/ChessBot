from abc import ABC, abstractmethod
import numpy

class PiecesDetectionBase(ABC):
    '''Base class for pieces detection'''
    def __init__(self, config: dict) -> None:
        self.config = config["pieces_detection"]

    @abstractmethod
    def detect(image: numpy.ndarray):
        '''detects chess_pieces on given image'''