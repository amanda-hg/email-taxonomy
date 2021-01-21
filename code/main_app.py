"""This module handles all the input/output of the main workflow.
workflow version: 1.0.0
"""
import os
import time

# MODULES
from global_vars import ROOT_PATH, CONFIG_NAME
from config import get_schema, read_config, validate_config
from get_logger import config_logger, logger
from utils import get_folder_structure
from preprocess_data import clean_data, preprocess_data
from lda_model import train_lda, predict

config_logger(ROOT_PATH)
time_start = time.time()
current_time = time.strftime("%Y-%m-%d %H:%M:%S %Z", time.gmtime(time_start))
logger.info("Execution started at "+current_time)

# Get paths
dir_data, dir_output, dir_tmp, config_path = get_folder_structure(root_path=ROOT_PATH, \
                                                                  config_fname=CONFIG_NAME)

logger.info("Validation config file..")
# Load config
schema = get_schema()
config = read_config(config_path=config_path)
config = validate_config(config=config, schema=schema)

# Clean data
df_cleaned = clean_data(dir_tmp=dir_tmp, path_data=dir_data)
df_base = preprocess_data(df_cleaned, dir_tmp=dir_tmp, path_data=dir_data)

# Create trained model folder
dir_model = os.path.join(dir_output, "model_trained")
print(dir_model)
print(dir_output)
print(config['n_top_words'])

# If its train
if config['train']:
    
    if not os.path.isdir(dir_model):
        os.makedirs(dir_model)

    logger.debug("Calculating best LDA model..")
    search_params = {"n_components" : list(range(5,16)), "learning_decay": [.9]}
    logger.debug("Search parameters used for GridSearch: "+str(search_params))
    # Train
    train_lda(df_base, search_params, dir_model)

# If its predict
if config['predict']:
    # Predict
    predict(config['n_top_words'], dir_model, dir_output)

time_end = time.time()
duration_time = time.strftime("%Hh %Mm %Ss", time.gmtime(time_end-time_start))
logger.debug("Execution ended at " + duration_time)
logger.info("Execution ended at " + duration_time)