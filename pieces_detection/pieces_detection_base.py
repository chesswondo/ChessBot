from abc import ABC, abstractmethod
import numpy
from typing import Tuple
from utils.pieces_detection.chess_board import ChessBoard

class PiecesDetectionBase(ABC):
    '''Base class for pieces detection.'''
    def __init__(self, config: dict) -> None:
        self.config = config

    @abstractmethod
    def detect(self, image: numpy.ndarray) -> Tuple[str, ChessBoard]:
        '''Detects chess_pieces on given image.'''