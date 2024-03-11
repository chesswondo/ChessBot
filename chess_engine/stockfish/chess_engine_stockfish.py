import os
import psutil
from stockfish import Stockfish

from chess_engine.chess_engine_base import ChessEngineBase
from utils.common_utils import find_file_except_extension
from utils.chess_engine.stockfish_utils import find_nearest_power_of_two

class ChessEngineStockfish(ChessEngineBase):
    '''Class for chess engine using stockfish engine.'''

    def __init__(self, config: dict) -> None:
        '''
        Initializes an instance of ChessEngineStockfish.

        : param config: (dict) - main configuration object.
        
        : return: (None) - this function does not return any value.
        '''
        super().__init__(config)
        program_path = find_file_except_extension(self.config['program_path'], '.txt')
        self.stockfish = Stockfish(program_path)
        if config["set_default_parameters"] == "no":
            threads = max(int(os.cpu_count()*config["threads_percent"]), 1)
            hash = find_nearest_power_of_two(psutil.virtual_memory().total*config["hash_percent"]//(1024*1024))
            self.stockfish.set_depth(config["depth"])
            self.stockfish.set_skill_level(config["engine_level"])
            self.stockfish.update_engine_parameters({"Hash": hash, "Threads": threads})

    def get_best_move(self, fen_position: str) -> str:
        '''
        Processes the input FEN-position using stockfish engine.

        : param fen_position: (str) - input FEN-position to process.

        : return: (str) - the best move suggestion.
        '''
        if self.stockfish.is_fen_valid(fen_position):
            self.position = fen_position
            self.stockfish.set_fen_position(fen_position)
            if 'w' in fen_position:
                print("The best move for white is:", self.stockfish.get_best_move())
            else:
                print("The best move for black is:", self.stockfish.get_best_move())
        else:
            print("Sorry, cannot recognize the position")

        return self.stockfish.get_best_move()