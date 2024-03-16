import argparse
import cv2
import numpy as np
from mss import mss
from IPython.display import display
import chess
import time

from utils.clicker import MouseClicker
from utils.interface_utils import ButtonValue
from chess_engine.create_engine import create_chess_engine
from interface.create_engine import create_interface_engine
from pieces_detection.create_engine import create_detection_engine
from speech_recognizer.create_engine import create_speech_recognition_engine
from utils.common_utils import load_config
from utils.pieces_detection.chess_board import is_move_valid

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
    program_mode = program_interface.get_program_mode()

    clicker_config = load_config('assets/configs/clicker/config.json')
    clicker = MouseClicker(clicker_config)

    detection_model = create_detection_engine(config)
    chess_engine = create_chess_engine(config)
    speech_recognition_model = create_speech_recognition_engine(config)

    current_fen = ""

    while True:
        try:
            sct_img = np.array(sct.grab(monitor))
            sct_img = cv2.cvtColor(sct_img, cv2.COLOR_BGRA2BGR)
            (fen_position, chess_board) = detection_model.detect(sct_img, color)

            if program_mode == ButtonValue.AUTO_MODE:
                if fen_position != current_fen:
                    best_move = chess_engine.get_best_move(fen_position)
                    clicker_coordinates = chess_board.chess_move_to_coordinates(best_move)
                    clicker.make_move(clicker_coordinates)
                    time.sleep(config['wait_after_click'])

                current_fen = fen_position
                time.sleep(config["seconds_between_detections"])

            elif program_mode == ButtonValue.SPEECH_RECOGNITION:
                recorded_audio = speech_recognition_model.record()
                recognized_text = speech_recognition_model.recognize(recorded_audio)
                if is_move_valid(recognized_text):
                    clicker_coordinates = chess_board.chess_move_to_coordinates(recognized_text)
                    clicker.make_move(clicker_coordinates)
                    time.sleep(config['wait_after_click'])

            else:
                best_move = chess_engine.get_best_move(fen_position)
                board = chess.Board(fen_position)
                display(board)

        except Exception as e:
            print("Cannot recognize the board. Make sure it is on the correct monitor and fully visible.")
            print(str(e))


def main():
    parser = argparse.ArgumentParser(description="Run chess game demo")
    parser.add_argument(
        "--config", help="Path to config file", required=False, default="assets/configs/main.json", dest="config"
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