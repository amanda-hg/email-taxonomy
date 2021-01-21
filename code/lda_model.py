import os
import pickle
import warnings
import pandas as pd
from get_logger import logger
from save_output import save_pickle, save_as_excel
## LDA
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation as LDA
from sklearn.model_selection import GridSearchCV

warnings.simplefilter("ignore", DeprecationWarning)

def _get_topics(model, count_vectorizer, n_top_words):
        '''Method to train a lda model.
        Parameters:
                -model (LDA): The lda model
                -count_vectorizer (CountVectorizer): The count vectorizer model
                -n_top_words (Int): number of words per topic
        Return:
                -df_topics (DataFrame): The topics dataframe
        '''
        words = count_vectorizer.get_feature_names()
        printable = []
        for topic_idx, topic in enumerate(model.components_):
                printable.append("Topic "+str(topic_idx +1))
                topic_words = " ".join([words[i] for i in topic.argsort()[:-n_top_words -1:-1]])
                printable.append(topic_words)

        list_columns = []
        list_words = []
        for ix, x in enumerate(printable):
                if ix % 2 != 0:
                        list_words.append(x.split())
                else:
                        list_columns.append(x)
        
        df_topics = pd.DataFrame(list_words)
        df_topics = df_topics.transpose()
        df_topics.columns = list_columns

        return df_topics

def _best_model(df, search_params):
        '''Method to get the best parameters to the best lda model.
        Parameters:
                -df (DataFrame): The base dataframe.
                -search_params (Dict): Dictionary with LDA params
        Return:
                -best_lda_model (LDA): The best lda model
                -count_vectorizer (CountVectorizer): The count vectorizer model
                -count_data (CountVectorizer)
        '''
        # Init model
        lda = LDA()
        # Init GrinSearchCV
        model = GridSearchCV(lda, param_grid=search_params, n_jobs=8)

        logger.debug("Initialize the count vectorizer...")
        # Initialize the count vectorizer with the English stop words
        count_vectorizer = CountVectorizer(stop_words='english')
        # Fit and transform the processed titles
        count_data = count_vectorizer.fit_transform(df['body_lemma'])

        logger.info("Training model...")
        model.fit(count_data)

        # Best model
        best_lda_model = model.best_estimator_
        # Model parameters
        logger.debug("Best model's params: {}".format(str(model.best_params_)))
        # Log likelihood score
        logger.debug("Best log likelihood score: {}".format(str(model.best_score_)))
        # Perplexity
        logger.debug("Model perplexity: {}".format(str(best_lda_model.perplexity(count_data))))

        return best_lda_model, count_vectorizer, count_data

def train_lda(df, search_params, dir_model):
        '''Method to train a lda model.
        Parameters:
                -df (DataFrame): The base dataframe.
                -search_params (Dict): Dictionary with LDA params
                -dir_model (String): model folder path
        '''
        logger.debug("Number of rows in df: " + str(len(df)))
        # Remove duplicates
        df = df.drop_duplicates(subset="body_lemma", keep="first")
        logger.debug("Number of rows without duplicates in df: " + str(len(df)))

        logger.info("Getting best lda model...")
        best_lda_model, count_vectorizer, count_data = _best_model(df, search_params)

        # Save counter vectorizer
        # Save lda model
        logger.debug("Saving counter vectorizer...")
        save_pickle(count_vectorizer, "count_vectorizer", dir_model)

        # Save lda model
        logger.info("Saving lda model...")
        save_pickle(best_lda_model, "lda_model", dir_model)

        logger.info("Finished training LDA model")

def predict(n_top_words, dir_model, dir_output):
        '''Method to train a lda model.
        Parameters:
                -n_top_words (Int): number of words per topic
                -dir_model (String): model folder path
                -dir_output (String): model folder path
        '''
        if not os.path.isdir(dir_model):
                logger.error('The model folder doesnt exist.')
                exit(1)

        if not os.path.isfile(dir_model+'/lda_model.p'):
                logger.error('The lda model doesnt exist.')
                exit(1)
        else:
                lda_model = pickle.load(open(dir_model+'/lda_model.p', 'rb'))

        if not os.path.isfile(dir_model+'/count_vectorizer.p'):
                logger.error('The count vectorizer model doesnt exist.')
                exit(1)
        else:
                count_vectorizer = pickle.load(open(dir_model+'/count_vectorizer.p', 'rb'))

        logger.info("Loading lda model...")
        lda_model = pickle.load(open(dir_model+'/lda_model.p', 'rb' ) )
        count_vectorizer = pickle.load(open(dir_model+'/count_vectorizer.p', 'rb' ) )

        logger.info("Calculating topics...")
        df_topics = _get_topics(lda_model, count_vectorizer, n_top_words)

        logger.info("Saving topics...")
        save_as_excel(df_topics, "topics", dir_output)