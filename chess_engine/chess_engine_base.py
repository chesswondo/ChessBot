from abc import ABC, abstractmethod

class ChessEngineBase(ABC):
    '''Base class for chess engine'''
    def __init__(self, config: dict) -> None:
        self.config = config["chess_engine"]["engine_type"]

    @abstractmethod
    def best_move(board, color: bool):
        '''finds best move in certain position'''