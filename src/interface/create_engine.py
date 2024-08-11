from interface.interface_base import InterfaceBase
from interface.tkinter.tkinter_parallel import TkinterParallel
from utils.common_utils import load_config

def create_interface_engine(config: dict) -> InterfaceBase:
    '''
    Creates an instance of the interface engine based on config.
    
    : param config: (dict) - main config file.
    
    : return: (InterfaceBase) - instance of the interface engine.
    '''
    interface_config = load_config(f'../assets/configs/interface/{config["interface"]["interface_type"]}/config.json')

    if config["interface"]["interface_type"] == "tkinter":
        return TkinterParallel(interface_config)