import json
import os

def load_config(config_path: str) -> dict:
    """
    Loads config file.

    : param config_path: (str) path to config file.
    
    : return: (dict) config dict.
    """
    with open(config_path, "r") as f:
        return json.load(f)
    
def find_file_except_extension(folder_path: str, extension: str) -> str:
    """
    Find the first file without certain extension in a folder.

    : param folder_path: (str) - path to the folder.
    : param extension: (str) - an extension to look for.

    : return: (str) - absolute path to the found file.
    """
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if not file.endswith(extension):
                return os.path.join(root, file)