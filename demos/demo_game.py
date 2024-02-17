import argparse
import cv2
import numpy as np
from mss import mss

from utils.demo_utils import load_config

def run_chess_demo(
        #camera: int,
        #video: str,
        config: dict
        ) -> None:
    '''Function to run chess game demo'''

    bounding_box = {'top': 0, 'left': 0, 'width': 1000, 'height': 700}
    sct = mss()

    while True:
        sct_img = sct.grab(bounding_box)
        #cv2.imshow('screen', np.array(sct_img))

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