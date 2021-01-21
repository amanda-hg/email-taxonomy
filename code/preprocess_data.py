import os
import time
import regex as re
import pandas as pd
from glob import glob
from codecs import encode, decode
from get_logger import logger
from checkpoint import checkpoint, get_hex_hash_params
from utils import remove_tags_sender, get_list_footers, remove_footers
from lemmatize import lemmatize_bodies, get_nlp_model_dict

def _get_list_conversations(body):
    ''' Method to split email body by conversations and remove headers
    Parameters:
        -body (String): The string body of email.
    Return:
        -body (String): The last conversation of body.
    ''' 
    start_header = "From:" if "from:" in body.lower() else "---------------------- Forwarded by"
    end_header = r"Subject:(.*)"

    p = re.compile(re.escape(start_header), re.IGNORECASE)
    header_pos = []
    for m in p.finditer(body):
        header_pos.append(m.start())

    p = re.compile(end_header, re.IGNORECASE)
    for m in p.finditer(body):
        header_pos.append(m.end())

    header_pos = sorted(header_pos + [0, len(body)])
    sectioned_body = [body[start:end] for (start, end) in [(x,header_pos[i+1])for i, x in enumerate(header_pos) if i < len(header_pos) - 1]]

    return [x for x in sectioned_body if start_header.lower() not in x[:5].lower()]	

def _get_last_conversation(body, list_of_footers):
    '''Method to exctract the last conversation of the body.
    Parameters:
        -body (string): text containing all the body conversations
        -list_of_footers (list): list of footers to remove from each conversation
    Returns:
        -body (string): cleaned body
    '''
    if body != '':
        list_bodies = _get_list_conversations(body)[0]
        # Remove footers from conversations
        body = " ".join([remove_footers(b, list_of_footers) for b in [list_bodies]])
        # Remove \n
        body = re.sub(r"\n", " ", body)
        
    return body

def _clean_dataset(path_data='', list_footers=[]):
    '''Method to exctract the base information from emls.
    Parameters:
        -path_data (string): The subfolders of mailbox.
    Return:
        -df_base (Dataframe): Dataframe base complete.
    '''
    # Load file
    data_file_path = [f for f in glob(path_data + "**/*.csv", recursive=True)][0]
    df_enron = pd.read_csv(data_file_path, sep=",", error_bad_lines=False, index_col=0)
    # Filter by the information we need it
    df_base = df_enron[['From', 'To', 'content']]

    logger.debug("Cleaning the dataset")
    # Clean NA values
    df_base = df_base.fillna('')
    # Clean From and To
    df_base['from'] = df_base['From'].apply(lambda x: remove_tags_sender(x))
    df_base = df_base.drop('From', axis=1)
    df_base['to'] = df_base['To'].apply(lambda x: remove_tags_sender(x))
    df_base = df_base.drop('To', axis=1)
    # Get body
    df_base['body'] = df_base['content']
    df_base = df_base.drop('content', axis=1)

    logger.debug("Getting the clean last conversation")
    df_base['body_latest'] = df_base.apply(lambda x : _get_last_conversation(x["body"], list_footers), axis=1)

    return df_base

def clean_data(dir_tmp='', path_data=''):
    '''Method to extract all value information from all emls.
    Parameters:
        -dir_tmp (String): The temporal path.
        -path_data (List): The data path.
    Return:
        -df_cleaned (Dataframe): clean dataframe.
    '''
    logger.info("Loading list of footers..")
    list_footers = get_list_footers()

    # Create the dataframe base
    logger.info("Extracting and cleaning the information from the body emails..")
    df_cleaned = checkpoint(func=_clean_dataset, func_args=(path_data, list_footers), func_kwargs={},
                         suffix=get_hex_hash_params(dir_tmp), save_checkpoint=True,
                         tmp_path=dir_tmp.encode(), suffix_description='df_base')
    return df_cleaned

def preprocess_data(df_cleaned, dir_tmp='', path_data=''):
    '''Method to extract all value information from all emls.
    Parameters:
        -dir_tmp (String): The temporal path.
        -path_data (List): The data path.
    Return:
        -df_base (Dataframe): Dataframe complete.
    '''
    time1 = time.time()
    current_time = time.strftime("%Y-%m-%d %H:%M:%S %Z", time.gmtime(time1))
    logger.debug("Execution preprocessing data started at "+current_time)

    logger.info("Loading nlp dictionary..")
    nlp_model = checkpoint(func=get_nlp_model_dict, func_args=(), func_kwargs={},
                            suffix=get_hex_hash_params(dir_tmp), save_checkpoint=True,
                            tmp_path=dir_tmp.encode(), suffix_description='nlp_model')
 
    # Body lemmatization
    logger.info("Lemmatizing bodies of emails..")
    df_base = checkpoint(func=lemmatize_bodies, func_args=(df_cleaned, nlp_model), func_kwargs={},
                          suffix=get_hex_hash_params(dir_tmp), save_checkpoint=True,
                          tmp_path=dir_tmp.encode(), suffix_description='df_base_lemmatized')

    time2 = time.time()
    duration_time = time.strftime("%Hh %Mm %Ss", time.gmtime(time2-time1))
    logger.debug("Preprocessing data ended at " + duration_time)

    return df_base
