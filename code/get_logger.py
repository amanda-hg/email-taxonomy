"""This module configures the logger of the app.
Every module should import logger from this file.
"""
import os
import logging
PARENT_NAME = __name__.split(".")[0]
LOGGER_NAME = PARENT_NAME  # if you wish, you can change the name of the logger
logger = logging.getLogger(LOGGER_NAME)

def config_logger(root_path, log_debug=True):
    """Cofigure the logger. Should be invoked once.
    Args:
        log_info_fname (str, optional): Filename of the logger for the users.
            Defaults to "./logs/logfile.log".
        log_debug_fname (str, optional): Filename of the logger for the developers.
            Defaults to "./logs/debug.log".
        log_debug (bool, optional): Whether to write the debub log. Defaults to True.
    """
    log_info_fname = os.path.join(root_path, "logs/logfile.log")
    log_debug_fname = os.path.join(root_path, "logs/debug.log")

    # If the file exist -> then remove
    if os.path.isfile(log_info_fname):
        os.remove(log_info_fname)

    # If the file exist -> then remove
    if os.path.isfile(log_debug_fname):
        os.remove(log_debug_fname)

    logger.setLevel(logging.DEBUG)
    format_handler = logging.Formatter('%(levelname)s - %(message)s')
    open(log_info_fname, "a").close()
    file_handler = logging.FileHandler(log_info_fname, "a", "utf-8")
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(format_handler)
    logger.addHandler(file_handler)
    if log_debug:
        open(log_debug_fname, "a").close()
        file_handler = logging.FileHandler(log_debug_fname, "a", "utf-8")
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(format_handler)
        logger.addHandler(file_handler)
