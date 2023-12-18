"""
General utility functions for this project.
"""
# import os
from pathlib import Path
import logging

def get_file_path(input_filename, calling_file = __file__):
    """
    Get the complete file path as a string as seen from the calling_file.
    """
    dir = Path(calling_file).resolve().parent
    filepath = dir.joinpath(input_filename)
    return filepath

def logger_setup(logger, filename, level = logging.DEBUG):
    """
    setup the logging features, given a logger created previously.
    References: 
    https://realpython.com/python-logging/#using-handlers
    https://jdhao.github.io/2020/04/24/python_logging_for_multiple_modules/#google_vignette
    """
    filepath = get_file_path(filename)
    logger.setLevel(level)

    # setup logging handlers
    console_handler = logging.StreamHandler()
    file_handler = logging.FileHandler(filepath)

    # setup logging formatters
    file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(filename)s - %(funcName)s - %(levelname)s - %(message)s')
    console_formatter = logging.Formatter('%(message)s')

    # set the formatters for the handlers    
    file_handler.setFormatter(file_formatter)
    console_handler.setFormatter(console_formatter)

    # add the handlers to the logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    return(logger)
