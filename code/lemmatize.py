import re
from get_logger import logger

## SPACY
import spacy
import en_core_web_sm

def get_nlp_model_dict():
    nlp_en = en_core_web_sm.load()
    return {"english" : nlp_en}

def _lemmatize(body, language="english", nlp={}, allowed_postags=["NOUN", "ADJ", "VERB", "ADV", "PROPN"]):
    ''' Method to lematize text
    Parameters:
        -text (string): body latest
        -language (string): language
    Returns:
        -lemmatized text
    '''
    # Tokenization
    # Make all the strings lowercase and remove non alphabetic characters
    body = re.sub('[^A-Za-zÀ-ÿ]', ' ', body.lower())
    # Remove single characters
    body = re.sub(r'\b\w\b', '', body)
    # Normalize spaces
    body = re.sub(r' +', ' ', body)
    # Join words
    body = " ".join([x for x in body.split() if x])

    doc = nlp(body)
    # Add my stopwrods
    nlp.Defaults.stop_words |= {"enron", "com", "net", "td", "font", "ect", "new", "hou", "www", "http", "tr", "br", "pm", "jeff", "cc", "ees", "rb", "wr", "ga", "phillip"}
    # Remove stopwords and lemmatize body
    body_lemmatized_list = [token.lemma_ for token in doc if (token.pos_ in allowed_postags) and (token.lemma_ not in list(nlp.Defaults.stop_words)) and (len(token) > 3)]
    body_lemmatized_list = list(set(body_lemmatized_list))
    body_lemmatized = " ".join(body_lemmatized_list)
    return body_lemmatized

def lemmatize_bodies(df_base, nlp_model):
    '''Method to lemmatize the bodies of the emails.
    Parameters:
        -df_base (DataFrame): The base dataframe.
    Return:
        -df_base (DataFrame): The base dataframe with the bodies lemmatized
    '''
    # Load model
    nlp = nlp_model['english']
    logger.debug("Creating body lemma.. ")
    # Lemmatize body
    df_base['body_lemma'] = df_base.apply(lambda x: _lemmatize(x["body_latest"], "english", nlp,), axis=1)
    return df_base
