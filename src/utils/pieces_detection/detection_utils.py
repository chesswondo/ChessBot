import numpy as np
from typing import List
from enum import Enum

class DetectionType(str, Enum):
    '''
    Enumeration for detection model types.

    Possible values:
    - DetectionType.MMDETECTION: "mmdetection"
    '''

    MMDETECTION = "mmdetection"

    def __eq__(self, other):
        return self.value == other

    def __hash__(self):
        return hash(self.value)

def intersection_over_union(bbox1: List[float], bbox2: List[float]) -> float:
    '''
    Calculates the Intersection Over Union (IOU) metric for two bounding boxes.
    Bounding boxes must be specified as [x_min, y_min, x_max, y_max].

    : param bbox1: (List) - first bounding box coordinates.
    : param bbox2: (List) - second bounding box coordinates.
    
    : return: (float) - the IOU metric as a float.
    '''
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