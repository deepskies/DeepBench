#TODO: comments

import pandas as pd
import numpy as np


def save_data(f_data_list, data_list, data_type, verbose=False):
    """
    Save Data to File
    """

    if data_type == 'catalog':
        # Pandas Data Frame for tabular data: save to file
        data_list.to_csv(f_data_list)
    elif data_type == 'image':
        # Numpy Array for image data: save to file
        np.save(f_data_list, data_list)

    return


def load_data(f_data_list, data_type, verbose=False):
    """
    Load Data from File
    """

    if data_type == 'catalog':
        data_list = pd.read_csv(f_data_list)
    elif data_type == 'image':
        data_list = np.load(f_data_list)

    return data_list

