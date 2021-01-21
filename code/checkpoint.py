"""
Checkpoints
"""

import os
import json
import pickle
import pandas as pd
from hashlib import blake2b
from pandas.util import hash_pandas_object
from get_logger import logger

def _save_hashtable(suffix, suffix_description, hashtable_fname="./tmp/checkpoints_hashtable.txt"):
    """Appends to hashtable_fname two strings: suffix and suffix_description.
    This is intented to store the the description of a hash.
    """
    hashtable = "HASH: " + suffix + "\n" + "DESCRIPTION: " + suffix_description + "\n"
    with open(hashtable_fname, "a+") as f:
        f.writelines(hashtable)

def get_hex_hash_params(*params):
    """
    Returns hex hash representation of parameters. Parameters must be serealizable.
    In future, avoid using json. Check instance and if possible, try to directly hash parameter
    """
    h = blake2b(digest_size=5)
    for param in params:
        if isinstance(param, pd.DataFrame):
            h.update(str(hash_pandas_object(param).sum()).encode())
        else:
            h.update(json.dumps(param).encode())
    return h.hexdigest()

def checkpoint(func, func_args=None, func_kwargs=None, suffix="", save_checkpoint=True, tmp_path = b"/tmp/checkpoint", suffix_description=""):
    """
    Generic function to create checkpoints. This is a wrapper that executes a function *func* with arguments *func_args* and/or kwargs *func_kwargs*.
    It stores the result of the function in a pickle file in *tmp_path*. The name of the checkpoint includes the function name and *suffix*.
    In order to keep track of what a suffix means, fill out *suffix_description*.
    In order to shorten the suffix, use *get_hex_hash_params*.
    Args:
        func (function): function to evaluate.
        func_args (tupple): arguments of the function.
        func_kwargs (dict): kwargs of the function.
        suffix (str): suffix to add the the checkpoint file.
        save_checkpoint (boolean): whether to created checkpoint. Defaults to True.
        tmp_path (bytes): prefix of the checkpoint file. This is a path.
        suffix_description (str): description of the suffix.
    Returs
        res. Result of the function evaluation.
    """
    if func_args is None:
        func_args = ()

    if func_kwargs is None:
        func_kwargs = {}
        
    tmp_fname = tmp_path + b'/' + suffix_description.encode("utf-8") + b".p"

    if os.path.isfile(tmp_fname):
        with open(tmp_fname, "rb") as f:
            res = pickle.load(f)
    else:
        res = func(*func_args, **func_kwargs)
        if save_checkpoint:
            try:
                with open(tmp_fname, "wb") as f:
                    pickle.dump(res, f)

                if suffix_description:
                    _save_hashtable(suffix, suffix_description, hashtable_fname=tmp_path+b".txt")

            except:
                logger.warning("could not save cache of %s", tmp_fname)
                os.remove(tmp_fname)
    return res