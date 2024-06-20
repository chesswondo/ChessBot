from abc import ABC, abstractmethod

class ChessEngineBase(ABC):
    '''Base class for chess engine.'''
    def __init__(self, config: dict) -> None:
        self._config = config

    @abstractmethod
    def get_best_move(self, fen_position: str) -> str:
        '''Analisys logic.'''
