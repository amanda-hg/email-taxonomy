import os
import pickle
import pandas as pd
from pandas import ExcelWriter

def save_pickle(obj_to_save, filename, path_to_save):
    ''' Method to save objects as pickle
    Parameters:
        -obj_to_save (object)
        -filename (string)
        -path_to_save (string)
    '''
    fname = os.path.join(path_to_save, filename+".p")
    pickle.dump(obj_to_save, open(fname, "wb"))

def save_as_excel(df, filename, dir_output):
    ''' Method to save Dataframes as excel
    Parameters:
        -df (Dataframe)
        -filename (string)
        -dir_output (string)
    '''
    filename_out = os.path.join(dir_output, filename + ".xlsx")
    df.to_excel(excel_writer=filename_out, index=False, encoding="utf-8")
