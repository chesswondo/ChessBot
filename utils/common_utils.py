import json
import os

def load_config(config_path: str) -> dict:
    """
    Load config file

    :param config_path: (str) path to config file
    :return: (dict) config dict
    """
    with open(config_path, "r") as f:
        return json.load(f)
    
def find_file_with_extension(folder_path: str, extension: str) -> str:
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(extension):
                return os.path.join(root, file)[:-len(extension)]