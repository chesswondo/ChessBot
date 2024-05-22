from typing import Tuple
import pyautogui
import time

class MouseClicker():
    '''Class for mouse clicker.'''
    def __init__(self, config: dict):
        self.config = config

    def make_move(self, coordinates: Tuple[Tuple[int, int], Tuple[int, int]]) -> None:
        '''
        Make move based on screen coordinates.
        
        : param coordinates: (Tuple[Tuple[int, int], Tuple[int, int]]) - coordinates in format
        ((x1, y1), (x2, y2)).

        : return: (None) - this function does not return any value.
        '''
        ((x1, y1), (x2, y2)) = coordinates
        
        pyautogui.click(x=x1, y=y1)
        time.sleep(self.config["move_time"])
        pyautogui.click(x=x2, y=y2)

        print("Success!")