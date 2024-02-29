import argparse
import cv2
import numpy as np
from mss import mss
from IPython.display import display
import chess

from utils.clicker import MouseClicker
from chess_engine.create_engine import create_chess_engine
from interface.create_engine import create_interface_engine
from pieces_detection.create_engine import create_detection_engine
from utils.common_utils import load_config

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
    sct = mss()
    try:
        monitor = sct.monitors[num_monitor]

    except Exception:
        print("Cannot recognize the monitor. Please check your settings and monitor number.")
        return
    
    program_interface = create_interface_engine(config)
    color = program_interface.get_color()
    clicker_config = load_config('assets/configs/clicker/config.json')

    current_fen = ""

    num_frame = 0
    while True:

        sct_img = np.array(sct.grab(monitor))
        sct_img = cv2.cvtColor(sct_img, cv2.COLOR_BGRA2BGR)
        try:
            if num_frame % config['detect_every_n_frames'] == 0:

                detection_model = create_detection_engine(config)
                (fen_position, chess_board) = detection_model.detect(sct_img, color)
                chess_engine = create_chess_engine(config)
                best_move = chess_engine.get_best_move(fen_position)

                if config['clicker'] == "on" and fen_position != current_fen:
                    clicker_coordinates = chess_board.chess_move_to_coordinates(best_move)
                    clicker = MouseClicker(clicker_config)
                    clicker.make_move(clicker_coordinates)

                board = chess.Board(fen_position)
                display(board)
                current_fen = fen_position

        except Exception:
            print("Cannot recognize the board. Make sure it is on the correct monitor and fully visible.")

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