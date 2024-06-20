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
        program_path = find_file_except_extension(self._config['program_path'], '.txt')
        self._stockfish = Stockfish(program_path)
        if not config["set_default_parameters"]:
            threads = max(int(os.cpu_count()*config["threads_percent"]), 1)
            hash = find_nearest_power_of_two(psutil.virtual_memory().total*config["hash_percent"]//(1024*1024))
            self._stockfish.set_depth(config["depth"])
            self._stockfish.set_skill_level(config["engine_level"])
            self._stockfish.update_engine_parameters({"Hash": hash, "Threads": threads})

    def get_best_move(self, fen_position: str) -> str:
        '''
        Processes the input FEN-position using stockfish engine.

        : param fen_position: (str) - input FEN-position to process.

        : return: (str) - the best move suggestion.
        '''
        if self._stockfish.is_fen_valid(fen_position):
            self.position = fen_position
            self._stockfish.set_fen_position(fen_position)
            if 'w' in fen_position:
                print("The best move for white is:", self._stockfish.get_best_move())
            else:
                print("The best move for black is:", self._stockfish.get_best_move())
        else:
            raise Exception("Stockfish engine cannot recognize best move.")

        return self._stockfish.get_best_move()