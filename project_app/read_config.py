import os
import json


def get_config(config_file):
    """
    get_config() gets the configuration information from config_file,
    which is a json formatted file.
    Returns the url and payload of the API.
    """
    # get the file handler f of config_file
    dir = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(dir, config_file)
    f = open(filepath)  

    # extract the url and payload from config_file
    data = json.load(f)
    url = data["configuration"]["url"]
    payload = data["configuration"]["payload"]
    return url, payload
