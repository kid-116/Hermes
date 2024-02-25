import os

import pandas as pd


def get_tables(_dir):
    files = os.listdir(_dir)
    return [file.strip('.csv') for file in files if file.endswith('.csv')]


def load_tables(_dir, files):
    data = {}
    for file in files:
        data[file] = pd.read_csv(os.path.join(_dir, file + '.csv'))
    return data
