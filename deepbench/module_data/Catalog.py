import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import numpy.random as rand
from ..module_data.generate_data import *


class Catalog:
    """
    The Catalog object stores objects of DeepBench in a way so that it is easy to generate
    imagesets and store the data in a csv file.

    Attributes:
        n_obj (int):
        pix_dim (int): dimension of images stored in Catalog
        data (pandas DataFrame): Data structure storing information
                                 on Catalog objects
        images (List or ListLike): images of Catalog's objects in data

    """
    def __init__(self, n_obj, n_pix_side,id_start=0):

        """
        Constructor for Catalog class.

        Parameters:
             n_obj (int): number of objects to be stored
             n_pix_side (int): image dimension in pixels
             myclass (string): type of object being created.
                                Print self.poss_classes to see
                                all options
             radius (float): radius of object drawn in the image
             amplitude (float, [0, 3]): amplitude of object in image
             id_start (int): start of index in data
             obj_params (List): other parameters passed to DeepBench object for generating it


        """

        # Set parameters for DataFrame object
        self.data = pd.DataFrame(n_obj)
        self.data.index += id_start

        # Other catalog parameters
        self.n_obj = n_obj
        self.pix_dim = n_pix_side
        self.images = None

    def __len__(self):
        """ Return length of DataFrame in Catalog
        """
        return len(self.data)

    def generate_imageset(self):
        """ Populates catalog's self.images array with images of specified
            objects in self.data
        """
        self.images = np.zeros((self.n_obj, self.pix_dim, self.pix_dim))
        for ind, _ in enumerate(self.images):
            self.images[ind] = self._generate_image(self.data.loc[ind], self.pix_dim)

    def _generate_image(self, catalog_single, n_pix_side):
        pass


    def save_images(self, path):
        """
        Save images to a desired folder given.

        Parameters:
            path (string or PathLike): Folder where images will be saved

        Returns:
            Images saved
        """
        assert self.images is not None, "Must generate images before saving. " \
                                        "Try calling catalog.generate_imageset() first."
        if not os.path.exists(path):
            os.mkdir(path)
        for row, img in enumerate(self.images):
            fig = plt.figure(frameon=False)
            plt.contourf(img, cmap='viridis')
            plt.axis('off')
            name = os.path.join(path, str(row) + '.jpg')
            fig.savefig(name, bbox_inches='tight', pad_inches=0)
            plt.close()

    def to_csv(self, path, name):
        """

        """
        if not os.path.exists(path):
            os.mkdir(path)
        path = os.path.join(path, name)
        return self.data.to_csv(path)

    def get_data(self):
        """
        Return the data stored in the Catalog object
        """
        return self.data

    def set_data(self, dataset):
        """
        Set the data object in the Catalog with a new dataFrame.
            Parameters:
                dataset (pandas.DataFrame): object to replace Catalog's data
        """
        if isinstance(dataset, pd.DataFrame):
            self.data = dataset
            self.images = None
        else:
            print("set_data must receive a DataFrame")
        return
