from chess_engine.chess_engine_base import ChessEngineBase
from chess_engine.stockfish.chess_engine_stockfish import ChessEngineStockfish
from utils.common_utils import load_config

def create_chess_engine(config: dict) -> ChessEngineBase:

    if config["chess_engine"]["engine_type"] == "stockfish":
        stockfish_config = load_config('assets/configs/chess_engine/stockfish/config.json')
        return ChessEngineStockfish(stockfish_config)