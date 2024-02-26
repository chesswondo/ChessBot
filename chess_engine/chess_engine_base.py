from abc import ABC, abstractmethod

class ChessEngineBase(ABC):
    '''Base class for chess engine'''
    def __init__(self, config: dict) -> None:
        self.config = config

    @abstractmethod
    def process(self, fen_position: str) -> None:
        '''analisys logic'''
