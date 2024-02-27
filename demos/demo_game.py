import argparse
import cv2
import numpy as np
import glob
from mss import mss
from IPython.display import display
import chess
import torch

from utils.pieces_detection.detection_utils import filter_detections
from utils.pieces_detection.chess_board import ChessBoard
from chess_engine.create_engine import create_chess_engine
from mmdet.apis import DetInferencer
from utils.common_utils import load_config
from pieces_detection.create_engine import create_detection_engine

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

    device = 'cuda:0' if torch.cuda.is_available() else 'cpu'

    # Initialize the DetInferencer
    sct = mss()
    monitor = sct.monitors[num_monitor]

    num_frame = 0
    while True:
        sct_img = np.array(sct.grab(monitor))
        sct_img = cv2.cvtColor(sct_img, cv2.COLOR_BGRA2BGR)
        
        if num_frame % config['detect_every_n_frames'] == 0:

            detection_model = create_detection_engine(config)
            (fen_position_white, fen_position_black) = detection_model.detect(sct_img)
            chess_engine = create_chess_engine(config)
            chess_engine.process(fen_position_white)
            chess_engine.process(fen_position_black)

            board = chess.Board(fen_position_white)
            display(board)

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