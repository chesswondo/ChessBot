from chess_engine.chess_engine_base import ChessEngineBase
from stockfish import Stockfish

class ChessEngineStockfish(ChessEngineBase):

    def __init__(self, config: dict) -> None:
        super().__init__(config)

    def process(self, fen_position: str) -> None:
        stockfish = Stockfish('C:/Users/user/Projects/chess_bot/assets/models/chess_engine/stockfish/stockfish-windows-x86-64-avx2')
        if stockfish.is_fen_valid(fen_position):
            self.position = fen_position
            stockfish.set_fen_position(fen_position)
            print("The best move for white is:", stockfish.get_best_move())
        else:
            print("Sorry, cannot recognize the position")