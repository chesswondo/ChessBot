from interface.interface_base import InterfaceBase

class InterfaceTkinter(InterfaceBase):
    '''Class for program interface using Tkinter library.'''

    def __init__(self, config: dict) -> None:
        '''
        Initializes an instance of InterfaceTkinter.

        : param config: (dict) - tkinter configuration object.
        
        : return: (None) - this function does not return any value.
        '''
        super().__init__(config)

    def start(self) -> None:
        '''
        Launch program interface.

        : return: (None) - this function does not return any value.
        '''
        