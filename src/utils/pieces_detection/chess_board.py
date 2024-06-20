import numpy as np
from typing import Tuple
from utils.interface_utils import ButtonValue

class ChessBoard():
    '''Class for chess board'''

    def __init__(self, config: dict, labels: np.ndarray, bboxes: np.ndarray, color: str) -> None:
        '''Initializes an instance of ChessBoard.

        : param config: (dict) - chess board configuration object.
        : param labels: (numpy.ndarray) - labels received from the model.
        : param bboxes: (numpy.ndarray) - bboxes received from the model.
        : param color: (bool) - which color user play.

        : return: (None) - this function doesn't return any value.
        '''
        try:
            config["pieces_indexes"] = {int(key): value for key, value in config["pieces_indexes"].items()}
        except Exception:
            raise ValueError("Incorrect indexes in chess_board configuration file.")
        
        self.pieces_indexes = config["pieces_indexes"]
        self.pieces_names = config["pieces_names"]
        self.board_fields = config["board_fields"]
        self.board_constant = config["board_constant"]
        self.labels = labels
        self.bboxes = bboxes
        self.color  = 'b' if color == ButtonValue.BLACK else 'w'

    def detections_to_fen(self) -> str:
        '''
        Function that converts given image to the FEN position.

        : return: (str) - FEN position for chosen color.
        '''
        board_const = [i for i in self.pieces_indexes if self.pieces_indexes[i]==self.board_constant][0]
        board_index = np.where(self.labels==board_const)[0][0]
        self.board_bbox = self.bboxes[board_index]

        chess_board = np.full((8, 8), None)
        num_detections = len(self.bboxes)
        for i in range(num_detections):
            if i != board_index:
                piece_bbox = self.bboxes[i]
                x, y = self.find_field_by_coordinates(self.board_bbox, piece_bbox)
                label = self.pieces_names[self.pieces_indexes[self.labels[i]]]
                if max(x, y) < 8 and min(x, y) >= 0:
                    chess_board[y][x] = label

        if self.color == 'b':
            chess_board = np.rot90(chess_board, 2)

        if (chess_board == None).all():
            raise ValueError("Empty board.")

        return self.filled_board_to_fen(chess_board)

    @staticmethod
    def find_field_by_coordinates(board_bbox: np.ndarray, piece_bbox: np.ndarray) -> np.ndarray:
        '''
        Finds location of the piece on chess board by their bbox-coordinates got from the model.

        : param board_bbox: (numpy.ndarray) - bounding box of the chess_board.
        : param piece_bbox: (numpy.ndarray) - bounding box of the given piece.

        : return: (numpy.ndarray) - coordinates of the piece located on chess board.
        '''
        piece_center = ((piece_bbox[2]-piece_bbox[0])//2+piece_bbox[0],
                        (piece_bbox[3]-piece_bbox[1])//2+piece_bbox[1])
        x_field = int((piece_center[0]-board_bbox[0])/(board_bbox[2]-board_bbox[0])*8)
        y_field = int((piece_center[1]-board_bbox[1])/(board_bbox[3]-board_bbox[1])*8)

        return x_field, y_field
    
    def filled_board_to_fen(self, chess_board: np.ndarray) -> str:
        '''
        Auxiliary function that converts filled chess_board to FEN positions.

        : param chess_board: (numpy.ndarray) - filled chess board with pieces.
        
        : return: (str) - FEN positions for black and white. 
        '''
        res_fen = ""
        for i in range(8):
            res_fen += self.chess_row_to_fen_row(chess_board[:][i])
            if i != 7:
                res_fen += '/'
        
        res_fen = res_fen + f' {self.color} - - 0 30'
        
        return res_fen

    @staticmethod
    def chess_row_to_fen_row(chess_row: np.ndarray) -> str:
        '''
        Auxiliary function that converts one row on chess board to the part of FEN.

        : param chess_row: (numpy.ndarray) - one chess row with shape (8,).

        : return: (str) - this row as a part of FEN.
        '''
        result_row = ""
        empty_count = 0
        for i in range(8):
            if chess_row[i] is not None:
                if empty_count != 0:
                    result_row += str(empty_count)
                    empty_count = 0
                result_row += chess_row[i]
            else:
                empty_count += 1
                if i == 7:
                    result_row += str(empty_count)

        return result_row
    
    def chess_move_to_coordinates(self, move: str) -> Tuple[Tuple[int, int], Tuple[int, int]]:
        '''
        Convert chess move to screen coordinates.

        : param move: (str) - chess move. Must be in format like "e2e4".

        : return: (Tuple[Tuple[int, int], Tuple[int, int]]) - two pairs of coordinates on the screen.
        '''
        if not is_move_valid(move):
            raise ValueError("Invalid move. Cannot convert to coordinates.")

        x1_board, y1_board = self.board_fields[move[0]], 8-int(move[1])
        x2_board, y2_board = self.board_fields[move[2]], 8-int(move[3])

        if self.color == 'b':
            x1_board = 7-x1_board
            x2_board = 7-x2_board
            y1_board = 7-y1_board
            y2_board = 7-y2_board

        x1 = self.board_bbox[0] + (2*x1_board+1)/16*(self.board_bbox[2]-self.board_bbox[0])
        y1 = self.board_bbox[1] + (2*y1_board+1)/16*(self.board_bbox[3]-self.board_bbox[1])
        x2 = self.board_bbox[0] + (2*x2_board+1)/16*(self.board_bbox[2]-self.board_bbox[0])
        y2 = self.board_bbox[1] + (2*y2_board+1)/16*(self.board_bbox[3]-self.board_bbox[1])

        return ((int(x1), int(y1)), (int(x2), int(y2)))


def is_move_valid(move: str) -> bool:
    '''
    Checks if given move is valid or not.
    
    : param move: (str) - given move.
    
    : return: (bool) - is it valid.
    '''
    if type(move) is not str:
        raise TypeError("Got a move which is not string.")
    
    if len(move) != 4: return False
    if min(move[0], move[2]) < 'a' or max(move[0], move[2]) > 'h':
        return False
    if min(move[1], move[3]) < '1' or max(move[1], move[3]) > '8':
        return False
    
    return True