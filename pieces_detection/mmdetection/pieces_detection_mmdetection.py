import numpy
import torch
import glob
from mmdet.apis import DetInferencer
from typing import Tuple

from utils.pieces_detection.detection_utils import filter_detections
from pieces_detection.pieces_detection_base import PiecesDetectionBase
from utils.pieces_detection.chess_board import ChessBoard

class PiecesDetectionMMDetection(PiecesDetectionBase):
    '''Class for pieces detection using MMDetection model.'''

    def __init__(self, config: dict) -> None:
        '''
        Initializes an instance of PiecesDetectionMMDetection.

        : param config: (dict) - model configuration object.
        
        : return: (None) - this function does not return any value.
        '''
        super().__init__(config)

    def detect(self, image: numpy.ndarray, color: bool) -> str:
        '''
        Detects chess pieces on the given image.
        
        : param image: (numpy.ndarray) - image to make detections on it.
        : color: (bool) - color which user plays.

        : return: (str) - FEN-position from the given image.
        '''
        model_script = self.config['parameters_path']
        model_checkpoint = glob.glob(self.config['checkpoint_path'])[0]
        device = 'cuda:0' if torch.cuda.is_available() else 'cpu'

        inferencer = DetInferencer(model_script, model_checkpoint, device)
        result = filter_detections(inferencer(image), self.config['iou_threshold'], self.config['score_threshold'])
        
        chess_board = ChessBoard(result['predictions'][0]['labels'], result['predictions'][0]['bboxes'], color)
        
        return chess_board.detections_to_fen()