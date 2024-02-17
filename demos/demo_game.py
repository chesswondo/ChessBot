import argparse
import cv2
import numpy as np
import glob
from mss import mss
from IPython.display import display
import chess

from utils.pieces_detection.detection_utils import filter_detections, ChessBoard
from chess_engine.stockfish.chess_engine_stockfish import ChessEngineStockfish
from mmdet.apis import DetInferencer
from utils.demo_utils import load_config

def run_chess_demo(
        #camera: int,
        #video: str,
        config: dict
        ) -> None:
    '''Function to run chess game demo'''

    model_config = load_config(f'assets/configs/pieces_detection/{config["pieces_detection"]["detection_type"]}/config.json')
    model_script = model_config['parameters_path']
    model_checkpoint = glob.glob(model_config['checkpoint_path'])[0]

    device='cpu'

    # Initialize the DetInferencer
    inferencer = DetInferencer(model_script, model_checkpoint, device)

    bounding_box = {'top': 0, 'left': 0, 'width': 1920, 'height': 1080}
    sct = mss()

    num_frame = 0
    while True:
        sct_img = np.array(sct.grab(bounding_box))
        sct_img = cv2.cvtColor(sct_img, cv2.COLOR_BGRA2BGR)
        
        if num_frame % 300 == 0:
            result = filter_detections(inferencer(sct_img), 0.1, 0.3)
            
            chess_board = ChessBoard(result['predictions'][0]['labels'], result['predictions'][0]['bboxes'])
            fen_position = chess_board.detections_to_fen()
            print(fen_position)

            board = chess.Board(fen_position)
            display(board)

            stockfish_engine = ChessEngineStockfish({"chess_engine": None})
            stockfish_engine.process(fen_position)
            #cv2.imshow('screen', np.array(sct_img))

        num_frame += 1
        if (cv2.waitKey(1) & 0xFF) == ord('q'):
            cv2.destroyAllWindows()
            break


def main():
    parser = argparse.ArgumentParser(description="Run chess game demo")
    parser.add_argument(
        "--config", help="Path to config file", required=True, dest="config"
    )
    args = parser.parse_args()

    config = load_config(args.config)

    run_chess_demo(
        config=config,
    )
    

if __name__ == "__main__":
    main()