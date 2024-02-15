import numpy as np
from typing import List
from abc import abstractmethod

pieces_names = {
    'black-bishop': 'b',
    'black-king': 'k',
    'black-knight': 'n',
    'black-pawn': 'p',
    'black-queen': 'q',
    'black-rook': 'r',
    'white-bishop': 'B',
    'white-king': 'K',
    'white-knight': 'N',
    'white-pawn': 'P',
    'white-queen': 'Q',
    'white-rook': 'R',
}

pieces_indexes = {
    0:  'pieces',
    1:  'bishop',
    2:  'black-bishop',
    3:  'black-king',
    4:  'black-knight',
    5:  'black-pawn',
    6:  'black-queen',
    7:  'black-rook',
    8:  'white-bishop',
    9:  'white-king',
    10: 'white-knight',
    11: 'white-pawn',
    12: 'white-queen',
    13: 'white-rook',
    14: 'chess-board',
}

class ChessBoard():
    '''class for chess board'''
    def __init__(self, labels: np.ndarray, bboxes: np.ndarray) -> None:
        self.labels = labels
        self.bboxes = bboxes

    def detections_to_fen(self) -> str:
        '''
        Function that converts given image to the FEN position.
        '''
        board_index = np.where(self.labels==14)[0][0]
        board_bbox = self.bboxes[board_index]

        chess_board = np.full((8, 8), None)
        num_detections = len(self.bboxes)
        for i in range(num_detections):
            if i != board_index:
                piece_bbox = self.bboxes[i]
                x, y = self.find_field_by_coordinates(board_bbox, piece_bbox)
                label = pieces_names[pieces_indexes[self.labels[i]]]
                if max(x, y) < 8:
                    chess_board[y][x] = label

        return self.filled_board_to_fen(chess_board)

    def find_field_by_coordinates(self, board_bbox: np.ndarray, piece_bbox: np.ndarray) -> np.ndarray:
        piece_center = ((piece_bbox[2]-piece_bbox[0])//2+piece_bbox[0],
                        (piece_bbox[3]-piece_bbox[1])//2+piece_bbox[1])
        x_field = int((piece_center[0]-board_bbox[0])/(board_bbox[2]-board_bbox[0])*8)
        y_field = int((piece_center[1]-board_bbox[1])/(board_bbox[3]-board_bbox[1])*8)

        return x_field, y_field
    
    def filled_board_to_fen(self, chess_board: np.ndarray):
        res_fen = ""
        for i in range(8):
            res_fen += self.chess_row_to_fen_row(chess_board[:][i])
            if i != 7:
                res_fen += '/'
        
        res_fen += ' w KQkq - 0 1'
        return res_fen

    def chess_row_to_fen_row(self, chess_row: np.ndarray) -> str:
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


def intersection_over_union(bbox1: List[float], bbox2: List[float]) -> float:
    """
    Calculates the Intersection Over Union (IOU) metric for two bounding boxes.
    Bounding boxes must be specified as [x_min, y_min, x_max, y_max].

    : param bbox1: (List) - first bounding box coordinates.
    : param bbox2: (List) - second bounding box coordinates.
    : return: (float) - the IOU metric as a float.
    """
    assert (
        len(bbox1) == 4 and len(bbox2) == 4
    ), "Bounding boxes must be in the format: [x_min, y_min, x_max, y_max]"

    # Determine the (x, y)-coordinates of the intersection rectangle
    x_left = max(bbox1[0], bbox2[0])
    y_top = max(bbox1[1], bbox2[1])
    x_right = min(bbox1[2], bbox2[2])
    y_bottom = min(bbox1[3], bbox2[3])

    # Compute the area of intersection rectangle
    intersection_area = max(x_right - x_left, 0) * max(y_bottom - y_top, 0)
    if intersection_area == 0:
        return 0.0

    # Compute the area of both the prediction and ground-truth rectangles
    area_bbox1 = (bbox1[2] - bbox1[0]) * (bbox1[3] - bbox1[1])
    area_bbox2 = (bbox2[2] - bbox2[0]) * (bbox2[3] - bbox2[1])

    # Compute the intersection over union by dividing the intersection area
    # by the sum of both areas minus the intersection area
    iou = intersection_area / float(area_bbox1 + area_bbox2 - intersection_area)

    return iou


def filter_detections(raw_result: dict, iou_threshold: float, score_threshold: float) -> dict:
    '''
    Receives detection result via DetInferencer and discards extra bboxes.
    
    : param raw_result: (dict) - raw predictions got from the model.
    : param iou_threshold: (float) - max value of iou that is allowed in predictions.
    : param score_threshold: (float) - min score value that is allowed in predictions.

    : return: (dict) - selected predictions in the same format as input values.
    '''

    if not all([key in raw_result.keys() for key in ['predictions', 'visualization']]):
        raise ValueError("Incorrect format. Must have keys 'predictions' and 'visualization'")

    num_predictions = len(raw_result['predictions'][0]['scores'])
    mask = np.full(num_predictions, True, dtype=np.bool_)
    bboxes = np.array(raw_result['predictions'][0]['bboxes'])
    scores = np.array(raw_result['predictions'][0]['scores'])
    labels = np.array(raw_result['predictions'][0]['labels'])

    # filter by iou
    for i in range(num_predictions):
        for j in range(i+1, num_predictions):
            bbox1 = bboxes[i]
            bbox2 = bboxes[j]
            if intersection_over_union(bbox1, bbox2) > iou_threshold:
                if scores[i] < scores[j]:
                    scores[i] = 0.0
                else:
                    scores[j] = 0.0
            
    # filter by scores
    for ind, score in enumerate(scores):
        if score < score_threshold:
            mask[ind] = False

    # apply mask
    result = raw_result.copy()
    result['predictions'][0]['labels'] = labels[mask]
    result['predictions'][0]['scores'] = scores[mask]
    result['predictions'][0]['bboxes'] = bboxes[mask]

    return result