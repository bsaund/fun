import os
from os import path


def get_secret_key(filename=None):
    if filename is None:
        filename = get_default_key_filepath()
    with open(filename) as f:
        return f.readline()


def get_default_key_filepath():
    fp = '/'.join(os.getcwd().split('/')[0:3]) + '/.openai_key'
    if not path.exists(fp):
        raise FileNotFoundError(f"Default openai key file does not exist: {fp}")
    return fp
