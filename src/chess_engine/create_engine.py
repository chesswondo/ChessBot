from chess_engine.chess_engine_base import ChessEngineBase
from chess_engine.stockfish.chess_engine_stockfish import ChessEngineStockfish

def create_chess_engine(engine_type: str, config: dict) -> ChessEngineBase:

    if config["chess_engine"]["engine_type"] == "stockfish":
        return ChessEngineStockfish(config)