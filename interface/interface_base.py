from abc import ABC, abstractmethod

class InterfaceBase(ABC):
    '''Base class for program interface.'''
    def __init__(self, config: dict) -> None:
        self.config = config

    @abstractmethod
    def get_color(self) -> str:
        '''Gets color from user.'''

    @abstractmethod
    def get_program_mode(self) -> str:
        '''Gets program mode from user.'''