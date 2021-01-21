"""Module with functions for validating a config file. The validation is done
with the cerberus package. For this, a schema needs to be defined. This is the
structure that the config file needs to follow. The schema is specific to tha project.
"""

import json
import itertools
from json.decoder import JSONDecodeError
import cerberus
from cerberus.validator import Validator
from get_logger import logger
Validator.types_mapping["integer"] = cerberus.TypeDefinition("integer", (int,), (bool,))

def get_schema():
    """Get the schema of the ceberus's schema of the config file.
    Args:
        None.
    Returns:
        dict: Config file.
    """
    return {'train' : {'type' : 'boolean', 'default' : True},
            'predict' : {'type' : 'boolean', 'default' : False},
            'n_top_words' : {'type' : 'integer', 'default' : 1}}

def read_config(config_path):
    """Reads the config json file.
    Args:
        config_path (str or None): Path to the config json file.
    Raises:
        Exception: If the config file does not exist.
        Exception: If the config file is corrupted.
    Returns:
        dict: Config file.
    """
    if config_path:
        try:
            config = json.load(open(config_path, "rb"))
        except FileNotFoundError:
            logger.error("config file does not exist")
            raise Exception("config file {} does not exist".format(config_path))
        except JSONDecodeError:
            logger.error("issue with config file: file is not in a valid json format. Check if variables are enclosed in double quotes or booleans are in the right format")
            raise Exception("config file {} has issues".format(config_path))
        except:
            logger.error("issue with config file format")
            raise Exception("could not load config file {}".format(config_path))
    else:
        config = {}
    if not config:
        logger.info("The config file is empty")
    return config

def validate_config(config, schema):
    """Validates with cerberus the config file agains the schema.
    Args:
        config (dict): The config file.
        schema (dict): The schema.
    Raises:
        Exception: If the config file has an issue.
    Returns:
        dict: The validated config file.
    """
    validation = Validator(schema)
    if not validation.validate(config):
        logger.error("config file has issues")
        raise Exception("config file has issues:\n{}".format(json.dumps(validation.errors, indent=1)))

    #custom_validations(config)
    document = validation.document
    document.update(config)
    return document
