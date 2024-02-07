from chess_engine.chess_engine_base import ChessEngineBase

class ChessEngineStockfish(ChessEngineBase):

    def __init__(self, config: dict) -> None:
        super().__init__(config)