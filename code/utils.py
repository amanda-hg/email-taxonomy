import os
import re

## MODULES
from global_vars import LIST_OF_FOOTERS_PATH
from get_logger import logger

def get_folder_structure(root_path="./", config_fname="config.json"):
    """Gets and checks the paths the execution folder strucutre. The names of the folder
        are a conventiong. Please don't modify them.
    Args:
        root_path (str, optional): root path of the folder stcuture. Defaults to ./
        config_fname (str, optional): config filename. Defaults to config.json
    Returns:
        (str): dir_data, dir_output, dir_tmp, config_path
    """
    if not isinstance(root_path, str):
        raise TypeError("root_path must be str")
    if not isinstance(config_fname, str):
        raise TypeError("config_fname must be str")
    dir_data = os.path.join(root_path, "data/")
    dir_output = os.path.join(root_path, "output/")
    dir_tmp = os.path.join(root_path, "tmp/")
    config_path = os.path.join(root_path, "config/", config_fname)
    dir_data = os.path.normpath(dir_data)
    dir_output = os.path.normpath(dir_output)
    dir_tmp = os.path.normpath(dir_tmp)
    config_path = os.path.normpath(config_path)
    if not os.path.isdir(dir_data):
        raise Exception("path of input data does not exist: {}".format(dir_data))
    if not os.path.isdir(dir_output):
        raise Exception("path of output data does not exist: {}".format(dir_output))
    if not os.path.isdir(dir_tmp):
        raise Exception("path of tmp data does not exist: {}".format(dir_tmp))
    if not os.path.isfile(config_path):
        logger.info("there is no config file")
        config_path = None
    return dir_data, dir_output, dir_tmp, config_path

def remove_tags_sender(sender):
    """Remove some tag from sender email. Please don't modify them.
    Args:
        sender (str, optional): sender from email
    Returns:
        (str): clean sender
    """
    # Get everything between ''
    parts = re.split(r"\'(.*?)\'", sender)
    if len(parts) > 1:
        return parts[1]
    else:
        return sender

def remove_footers(body, list_footers):
    """Method to get remove the footers of the email body. Please don't modify them.
    Args:
        body (String): the string body of email.
        list_footers (List): the list of the possible footers.
    Returns:
        (str): the email body without footers.
    """
    if list_footers:
        for foot in list_footers:
            try:
                match = re.search(re.escape(foot), body, re.IGNORECASE)
                if match and match[0] != "":
                    (start,_)= match.span()
                    body = body[:start]
            except Exception as exception:
                logger.debug("Something occurred during footer removal")
                logger.debug(exception)
    return body

def get_list_footers():
    """Method to reed the footers file. Please don't modify them.
    Args:
    
    Returns:
        (list): list with possible footers
    """
    try:
        list_of_footers_path = LIST_OF_FOOTERS_PATH
        with open(list_of_footers_path, "r", encoding = "utf-8") as f:
            return [x for x in f.read().split("\n") if x]
    except:
        logger.info("No list of footers found, will not remove footers from body of emails")
        return []