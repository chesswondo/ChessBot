import json
from typing import Union


def get_source(camera: int, video: str) -> Union[int, str]:
    """
    Gets the source for capturing video.

    :param camera: (int) - Camera index.
    :param video: (str) - Video file path.
    :return: (int or str) - Camera index or video file path.
    """
    if camera is not None:
        return camera

    if video is not None:
        return video


def load_config(config_path: str) -> dict:
    """
    Load config file

    :param config_path: (str) path to config file
    :return: (dict) config dict
    """
    with open(config_path, "r") as f:
        return json.load(f)