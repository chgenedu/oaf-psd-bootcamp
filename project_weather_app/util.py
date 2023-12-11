"""
General utility functions for this project.
"""
import os
import logging

def get_file_path(input_filename, calling_file = __file__):
    """
    Get the complete file path as a string as seen from the calling_file.
    """
    dir = os.path.dirname(os.path.abspath(calling_file))
    filepath = os.path.join(dir, input_filename)
    return filepath

def log_setup(filename, logger_name):
    """
    setup the logging features
    https://realpython.com/python-logging/#using-handlers
    """
    filepath = get_file_path(filename)
    # logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger(logger_name)

    screen_handler = logging.StreamHandler()
    file_handler = logging.FileHandler(filepath)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    screen_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    logger.addHandler(screen_handler)
    logger.addHandler(file_handler)
    return(logger)
