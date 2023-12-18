"""
read_config processes the config file.
"""

from sys import exit
import json
from typing import Tuple
from util import get_file_path

def get_config(config_filename: str) -> Tuple[str, dict]:
    """
    get_config() gets the configuration information from config_filename,
    which is a json formatted file.
    Returns the url and payload of the API.
    """
    filepath = get_file_path(config_filename, calling_file = __file__)

    try: 
        with open(filepath) as f:
            # extract the url and payload from config_file
            print("Reading config file: ", filepath)
            data = json.load(f)
            url = data["configuration"]["url"]
            payload = data["configuration"]["payload"]
    except FileNotFoundError:
        print("Config file does not exist: ", filepath)
        print("Exception error: ", FileNotFoundError)
        exit(1)
    return url, payload
