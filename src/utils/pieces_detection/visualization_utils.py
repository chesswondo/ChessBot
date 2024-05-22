from typing import List, Tuple, Iterable, Sequence, Set, Dict
import matplotlib.pyplot as plt
import numpy as np
import cv2
from dataclasses import dataclass

def best_text_color(background_color: Tuple[int, int, int]) -> Tuple[int, int, int]:
    """Determine the best color for text to be visible on a given background color.

    :param background_color: RGB values of the background color.
    :return: RGB values of the best text color for the given background color.
    """

    # If the brightness is greater than 0.5, use black text; otherwise, use white text.
    if compute_brightness(background_color) > 0.5:
        return (0, 0, 0)  # Black
    else:
        return (255, 255, 255)  # White


def compute_brightness(color: Tuple[int, int, int]) -> float:
    """Computes the brightness of a given color in RGB format. From https://alienryderflex.com/hsp.html

    :param color: A tuple of three integers representing the RGB values of the color.
    :return: The brightness of the color.
    """
    return (0.299 * color[0] + 0.587 * color[1] + 0.114 * color[0]) / 255


FONT = cv2.FONT_HERSHEY_SIMPLEX
INITIAL_FONT_SIZE = 1
LINE_TYPE = max(int(INITIAL_FONT_SIZE * 2), 1)
MARGIN_SPACE = 20


@dataclass
class LabelInfo:
    """Hold information about labels.

    :attr name: Label name.
    :attr color: Color of the label.
    :attr text_size: Size of the label text.
    """

    name: str
    color: Tuple[int, int, int]
    text_size: Tuple[int, int]


@dataclass
class Row:
    """Represent a row of labels."""

    labels: List[LabelInfo]
    total_width: int


def get_text_size(text: str) -> Tuple[int, int]:
    """Calculate the size of a given text using the CV2 getTextSize function.

    :param text: Input text.
    :return: A tuple of width and height of the text box.
    """
    return cv2.getTextSize(text, FONT, INITIAL_FONT_SIZE, LINE_TYPE)[0]


def get_label_info(name: str, color: Tuple[int, int, int]) -> LabelInfo:
    """Creates a LabelInfo object for a given name and color.

    :param name: Label name.
    :param color: Label color.
    :return: An object of LabelInfo.
    """
    return LabelInfo(name, color, get_text_size(name))


def add_to_row_or_create_new(rows: List[Row], label: LabelInfo, image_width: int) -> List[Row]:
    """Adds a label to a row or creates a new row if the current one is full.

    :param rows: Existing rows of labels.
    :param label: Label to add.
    :param image_width: Width of the image.
    :return: Updated rows of labels.
    """
    if not rows or rows[-1].total_width + label.text_size[0] + 2 * MARGIN_SPACE > image_width:
        # create a new row and initialize total width
        rows.append(Row([label], label.text_size[0] + 2 * MARGIN_SPACE))
    else:
        # append label to existing row and add to total width
        rows[-1].labels.append(label)
        rows[-1].total_width += label.text_size[0] + MARGIN_SPACE
    return rows


def get_sorted_labels(class_color_tuples: Sequence[Tuple[str, Tuple[int, int, int]]]) -> List[LabelInfo]:
    """Sorts and creates LabelInfo for class-color tuples.

    :param class_color_tuples: Tuples of class names and associated colors.
    :return: A sorted list of LabelInfo objects.
    """
    sorted_classes = sorted(class_color_tuples, key=lambda x: x[0])
    return [get_label_info(name, color) for name, color in sorted_classes]


def get_label_rows(labels: List[LabelInfo], image_width: int) -> List[Row]:
    """Arranges labels in rows to fit into the image.

    :param labels: List of labels.
    :param image_width: Width of the image.
    :return: List of label rows.
    """
    rows = []
    for label in labels:
        rows = add_to_row_or_create_new(rows, label, image_width)
    return rows


def draw_label_on_canvas(canvas: np.ndarray, label: LabelInfo, position: Tuple[int, int], font_size: int) -> Tuple[np.ndarray, int]:
    """Draws a label on the canvas.

    :param canvas: The canvas to draw on.
    :param label: The label to draw.
    :param position: Position to draw the label.
    :param font_size: Font size of the label.
    :return: The updated canvas and horizontal position for next label.
    """
    upper_left = (position[0] - MARGIN_SPACE // 2, position[1] - label.text_size[1] - MARGIN_SPACE // 2)
    lower_right = (position[0] + label.text_size[0] + MARGIN_SPACE // 2, position[1] + MARGIN_SPACE // 2)
    canvas = cv2.rectangle(canvas, upper_left, lower_right, label.color, -1)
    canvas = cv2.putText(canvas, label.name, position, FONT, font_size, best_text_color(label.color), LINE_TYPE, lineType=cv2.LINE_AA)
    return canvas, position[0] + label.text_size[0] + MARGIN_SPACE


def draw_legend_on_canvas(image: np.ndarray, class_color_tuples: Iterable[Tuple[str, Tuple[int, int, int]]]) -> np.ndarray:
    """Draws a legend on the canvas.

    :param image: The image to draw the legend on.
    :param class_color_tuples: Iterable of tuples containing class name and its color.
    :return: The canvas with the legend drawnOops, it seems like the response got cut off.
    """
    sorted_labels = get_sorted_labels(class_color_tuples)
    label_rows = get_label_rows(sorted_labels, image.shape[1])

    canvas_height = (sorted_labels[0].text_size[1] + MARGIN_SPACE) * len(label_rows)
    canvas = np.ones((canvas_height, image.shape[1], 3), dtype=np.uint8) * 255

    vertical_position = sorted_labels[0].text_size[1] + MARGIN_SPACE // 2

    for row in label_rows:
        horizontal_position = MARGIN_SPACE
        for label in row.labels:
            canvas, horizontal_position = draw_label_on_canvas(canvas, label, (horizontal_position, vertical_position), INITIAL_FONT_SIZE)
        vertical_position += sorted_labels[0].text_size[1] + MARGIN_SPACE

    return canvas

def resize_and_align_bottom_center(image: np.ndarray, target_shape: Tuple[int, int]) -> np.ndarray:
    """Resizes an image while maintaining its aspect ratio, and aligns it at the bottom center on a canvas of the target size.

    :param image:           Input image to resize and center.
    :param target_shape:    Desired output shape as (height, width).
    :return:                Output image, which is the input image resized, centered horizontally, and aligned at the bottom on a canvas of the target size.
    """
    image_height, image_width = image.shape[:2]
    target_height, target_width = target_shape

    scale_factor = min(target_width / image_width, target_height / image_height)
    new_width = int(image_width * scale_factor)
    new_height = int(image_height * scale_factor)
    resized_image = cv2.resize(image, (new_width, new_height))

    canvas = np.full((target_height, target_width, 3), 255, dtype=np.uint8)
    x = int((target_width - new_width) / 2)
    y = int(target_height - new_height)
    canvas[y : y + new_height, x : x + new_width] = resized_image

    return canvas

def generate_color_mapping(num_classes: int) -> List[Tuple[int, ...]]:
    """Generate a unique BGR color for each class

    :param num_classes: The number of classes in the dataset.
    :return:            List of RGB colors for each class.
    """
    cmap = plt.cm.get_cmap("gist_rainbow", num_classes)
    colors = [cmap(i, bytes=True)[:3][::-1] for i in range(num_classes)]
    return [tuple(int(v) for v in c) for c in colors]

def draw_bbox(
    image: np.ndarray,
    color: Tuple[int, int, int],
    box_thickness: int,
    x1: int,
    y1: int,
    x2: int,
    y2: int,
) -> np.ndarray:
    """Draw a bounding box on an image.

    :param image:           Image on which to draw the bounding box.
    :param color:           RGB values of the color of the bounding box.
    :param box_thickness:   Thickness of the bounding box border.
    :param x1:              x-coordinate of the top-left corner of the bounding box.
    :param y1:              y-coordinate of the top-left corner of the bounding box.
    :param x2:              x-coordinate of the bottom-right corner of the bounding box.
    :param y2:              y-coordinate of the bottom-right corner of the bounding box.
    :return: Image with bbox
    """
    overlay = image.copy()
    overlay = cv2.rectangle(overlay, (int(x1), int(y1)), (int(x2), int(y2)), color, box_thickness)
    return cv2.addWeighted(overlay, 0.75, image, 0.25, 0)


def draw_bboxes(image: np.ndarray, bboxes_xyxy: np.ndarray, bboxes_ids: np.ndarray, class_names: Dict[int, str]) -> np.ndarray:
    """Draw annotated bboxes on an image.

    :param image:       Input image tensor.
    :param bboxes_xyxy: BBoxes, in [N, 4].
    :param bboxes_ids:  Class ids [N].
    :param class_names: Mapping of class_id -> class_name. (unique, not per bbox)
    :return:            Image with annotated bboxes.
    """
    if len(bboxes_ids) == 0:
        return image

    colors = generate_color_mapping(len(class_names) + 1)
    class_names_list = list(class_names.values())

    # Initialize an empty list to store the classes that appear in the image
    classes_in_image_with_color: Set[Tuple[str, Tuple]] = set()

    for (x1, y1, x2, y2), class_id in zip(bboxes_xyxy, bboxes_ids):
        class_name: str = class_names[class_id]
        color_i = class_names_list.index(class_name)
        color = colors[color_i]

        # If the class is not already in the list, add it
        classes_in_image_with_color.add((class_name, color))

        image = draw_bbox(
            image=image,
            color=color,
            box_thickness=2,
            x1=x1,
            y1=y1,
            x2=x2,
            y2=y2,
        )

    image = resize_and_align_bottom_center(image, target_shape=(600, 600))

    canvas = draw_legend_on_canvas(image=image, class_color_tuples=classes_in_image_with_color)
    image = np.concatenate((image, canvas), axis=0)

    return image