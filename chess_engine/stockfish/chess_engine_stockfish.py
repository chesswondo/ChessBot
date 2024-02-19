from chess_engine.chess_engine_base import ChessEngineBase
from stockfish import Stockfish
from utils.common_utils import find_file_with_extension

class ChessEngineStockfish(ChessEngineBase):

    def __init__(self, config: dict) -> None:
        super().__init__(config)

    def process(self, fen_position: str) -> None:
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