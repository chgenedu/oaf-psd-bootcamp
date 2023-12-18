"""
read_config processes the config file.
"""
# from sys import exit
import json
from typing import Tuple
from util import get_file_path
from exception import ConfigFileError

import logging
logger = logging.getLogger(__name__)

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
            logger.info("Reading config file: " + str(filepath))
            data = json.load(f)
            url = data["configuration"]["url"]
            payload = data["configuration"]["payload"]
    except FileNotFoundError as err:
        raise ConfigFileError("Config file not found.", 
                              filepath, err)
    except KeyError as err:
        raise ConfigFileError("Config file's dictionary key is not found.", 
                              filepath, err)
    except Exception as err:
        raise ConfigFileError("Config file exception error.", 
                              filepath, err)
    return url, payload
