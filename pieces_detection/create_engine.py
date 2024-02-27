from pieces_detection.pieces_detection_base import PiecesDetectionBase
from pieces_detection.rtmdet.pieces_detection_rtmdet import PiecesDetectionRtmdet
from utils.common_utils import load_config

def create_detection_engine(config: dict) -> PiecesDetectionBase:
    '''
    Creates an instance of the pieces detection engine based on config.
    
    : param config: (dict) - main config file.
    
    : return: (PiecesDetectionBase) - instance of the pieces detection engine.
    '''
    model_config = load_config(f'assets/configs/pieces_detection/{config["pieces_detection"]["detection_type"]}/config.json')

    if config["pieces_detection"]["detection_type"] == "rtmdet-tiny":
        return PiecesDetectionRtmdet(model_config)