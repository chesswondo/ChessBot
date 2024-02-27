from abc import ABC, abstractmethod

class InterfaceBase(ABC):
    '''Base class for program interface.'''
    def __init__(self, config: dict) -> None:
        self.config = config

    @abstractmethod
    def get_color(self) -> bool:
        '''Main interface logic.'''