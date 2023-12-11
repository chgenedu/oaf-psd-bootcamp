import os
import json
from typing import Tuple

def get_config(config_filename: str) -> Tuple[str, dict]:
    """
    get_config() gets the configuration information from config_filename,
    which is a json formatted file.
    Returns the url and payload of the API.
    """
    # get the file handler f of config_file
    dir = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(dir, config_filename)
    f = open(filepath)  

    # extract the url and payload from config_file
    data = json.load(f)
    url = data["configuration"]["url"]
    payload = data["configuration"]["payload"]
    return url, payload
