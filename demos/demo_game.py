import argparse
import cv2
import numpy as np
import glob
from mss import mss
from IPython.display import display
import chess

from utils.pieces_detection.detection_utils import filter_detections
from utils.pieces_detection.chess_board import ChessBoard
from chess_engine.create_engine import create_chess_engine
from mmdet.apis import DetInferencer
from utils.common_utils import load_config
import torch

def run_chess_demo(
        config: dict,
        num_monitor: int,
        ) -> None:
    '''
    Function to run chess game demo.
    
    : param config: (dict) - main config file.
    : param num_monitor: (int) - number of monitor to track.

    : return: (None) - this function doesn't return any value.
    '''

    model_config = load_config(f'assets/configs/pieces_detection/{config["pieces_detection"]["detection_type"]}/config.json')
    model_script = model_config['parameters_path']
    model_checkpoint = glob.glob(model_config['checkpoint_path'])[0]

    device = 'cuda:0' if torch.cuda.is_available() else 'cpu'

    # Initialize the DetInferencer
    inferencer = DetInferencer(model_script, model_checkpoint, device)
    sct = mss()
    monitor = sct.monitors[num_monitor]

    num_frame = 0
    while True:
        sct_img = np.array(sct.grab(monitor))
        sct_img = cv2.cvtColor(sct_img, cv2.COLOR_BGRA2BGR)
        
        if num_frame % config['detect_every_n_frames'] == 0:
            result = filter_detections(inferencer(sct_img), model_config['iou_threshold'], model_config['score_threshold'])
            
            chess_board = ChessBoard(result['predictions'][0]['labels'], result['predictions'][0]['bboxes'])
            (fen_position_white, fen_position_black) = chess_board.detections_to_fen()

            board = chess.Board(fen_position_white)
            display(board)

            chess_engine = create_chess_engine(config)
            chess_engine.process(fen_position_white)
            chess_engine.process(fen_position_black)

        num_frame += 1


def main():
    parser = argparse.ArgumentParser(description="Run chess game demo")
    parser.add_argument(
        "--config", help="Path to config file", required=True, dest="config"
    )
    parser.add_argument(
        "--monitor", help="Number of monitor you'll use", required=False, default=1, dest="monitor"
    )

    args = parser.parse_args()
    config = load_config(args.config)

    run_chess_demo(
        config=config,
        num_monitor=int(args.monitor)
    )
    

if __name__ == "__main__":
    main()