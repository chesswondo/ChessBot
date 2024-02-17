import json

def load_config(config_path: str) -> dict:
    """
    Load config file

    :param config_path: (str) path to config file
    :return: (dict) config dict
    """
    with open(config_path, "r") as f:
        return json.load(f)