from chess_engine.chess_engine_base import ChessEngineBase
from stockfish import Stockfish
from utils.common_utils import find_file_with_extension

class ChessEngineStockfish(ChessEngineBase):
    '''Class for chess engine using stockfish engine.'''

    def __init__(self, config: dict) -> None:
        '''
        Initializes an instance of ChessEngineStockfish.

        : param config: (dict) - main configuration object.
        
        : return: (None) - this function does not return any value.
        '''
        super().__init__(config)

    def get_best_move(self, fen_position: str) -> str:
        '''
        Processes the input FEN-position using stockfish engine.

        : param fen_position: (str) - input FEN-position to process.

        : return: (str) - the best move suggestion.
        '''
        program_path = find_file_with_extension(self.config['program_path'], '.exe')
        stockfish = Stockfish(program_path)
        if stockfish.is_fen_valid(fen_position):
            self.position = fen_position
            stockfish.set_fen_position(fen_position)
            if 'w' in fen_position:
                print("The best move for white is:", stockfish.get_best_move())
            else:
                print("The best move for black is:", stockfish.get_best_move())
        else:
            print("Sorry, cannot recognize the position")

        return stockfish.get_best_move()