__all__ = ['Catalog', 'concat_catalogs', 'empty_imshape', 'create_meshgrid',
           'create_Sersic2D','create_Moffat2D','create_Gaussian','create_noise',
           'combine_sky_imshape','create_lensing_event']

import os
import numpy as np
import numpy.random as rand
import pandas as pd

from typing import Union
from matplotlib import pyplot as plt
from astropy.modeling.models import Sersic2D, Gaussian2D, Moffat2D
from deepbench.module_draw.generate_draw import *



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
    column_names = ['x_center', 'y_center',
                    'radius', 'amplitude', 'myclass',
                    'obj_params']
    poss_classes = {'star': 0, 'galaxy': 1, 'lens': 2}

    def __init__(self, n_obj, n_pix_side, myclass,
                 radius, amplitude, id_start=0,
                 obj_params=None):

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
        self.data = pd.DataFrame(
            np.empty((n_obj, len(self.column_names))),
            columns=self.column_names)
        self.data.index += id_start
        self.data.x_center = rand.normal(n_pix_side/2, 5., (n_obj, 1))
        self.data.y_center = rand.normal(n_pix_side/2, 5., (n_obj, 1))
        self.data.radius = radius
        self.data.amplitude = amplitude
        self.data.myclass = self.poss_classes[myclass]
        self.data.obj_params = obj_params

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
            self.images[ind] = self._generate_image(self.data.loc[ind],
                                                    self.pix_dim)

    def _generate_image(self, catalog_single, n_pix_side):
        imshape = empty_imshape(n_pix_side)
        noise = rand.uniform(0.6, 1.5)
        noise_profile = 0

        if catalog_single.myclass == 2:
            # lensing Event
            imshape = create_lensing_event(imshape,
                                           center=(catalog_single.x_center, catalog_single.y_center),
                                           arc_obj=catalog_single.obj_params, star_radius=catalog_single.radius,
                                           star_intensity=catalog_single.amplitude)
            noise_profile = create_noise(imshape, noise+0.1)

        if catalog_single.myclass == 1:
            # galaxy event
            imshape = create_Sersic2D(imshape, x_0=catalog_single.x_center,
                                      y_0=catalog_single.y_center,
                                      amplitude=catalog_single.amplitude,
                                      radius=catalog_single.radius,
                                      ellip=rand.uniform(0.3, 0.7),
                                      theta=rand.uniform(-1.5, 1.5))
            noise_profile = create_noise(imshape, noise*10.0)

        if catalog_single.myclass == 0:
            # star event
            imshape = create_Moffat2D(imshape, x_0=catalog_single.x_center,
                                      y_0=catalog_single.y_center,
                                      amplitude=catalog_single.amplitude,
                                      radius=catalog_single.radius)

            noise_profile = create_noise(imshape, noise)
        imshape += noise_profile
        return imshape

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

def concat_catalogs(target, frames: Union[pd.DataFrame, list]):
    """
    Append data to end of target.
        Parameters:
            target (Catalog object): Catalog object to be returned with new data.
            frames (pandas.DataFrame or list): dataFrames to append to target given individually or in a list.

        Returns:
            Returns target Catalog object with the appended dataFrame.

    """
    if isinstance(frames, pd.DataFrame):
        frames = [frames]

    target.data = target.data.append(frames, ignore_index=True)
    target.n_obj = len(target.data)
    target.images = np.zeros((target.pix_dim, target.pix_dim, len(target)))
    return target


def empty_imshape(n_pix_side):
    """
    Return zeroed numpy array with square dimensions.
        Parameter:
            n_pix_side (unsigned int): dimension of sides of numpy array

        Return:
             numpy array of size [n_pix_side, n_pix_side] initialized to zero

    """
    return np.zeros((n_pix_side, n_pix_side))


def create_meshgrid(imshape):
    """
    Create mesh grid used for Sersic and Moffat distributions.
        Parameters:
            imshape (numpy array): Used to determine the shape of returned mesh grid

        Returns:
            numpy meshgrid object
    """

    return np.meshgrid(np.arange(np.shape(imshape)[0]), np.arange(np.shape(imshape)[1]))


def create_Sersic2D(imshape, amplitude=1, x_0=50,
                    y_0=50, radius=25,
                    n=1, ellip=.5, theta=-1):
    """
    Create a galaxy profile defined by a Sersic distribution
        Parameters:
            imshape (numpy.array): image shape given for calculating size of distribution
            amplitude (float): amplitude of the Sersic distribution
            x_0 (float): horizontal position of center
            y_0 (float): vertical position of center
            radius (float): radius of major axis of the distribution
            n (int (0.5, 10) ): Sersic number
            ellip (float (0,1)): eccentricity of the Sersic distribution
            theta (float): orientation angle of the major axis
        Returns:
            numpy.array with galaxy distribution

    """

    x, y = create_meshgrid(imshape)
    mod = Sersic2D(amplitude=amplitude,
                   x_0=x_0, y_0=y_0,
                   r_eff=radius, n=n,
                   ellip=ellip, theta=theta)
    return mod(x, y)


def create_Moffat2D(imshape, amplitude=1., x_0=0.,
                    y_0=0., radius=1., alpha=1.):
    """
    Create a star profile defined by a Moffat distribution
        Parameters:
            imshape (numpy.array): image shape given for calculating size of distribution
            amplitude (float): amplitude of the Moffat distribution
            x_0 (float): horizontal position of center
            y_0 (float): vertical position of center
            radius (float): radius of major axis of the distribution
            alpha (float): power index of the distribution
        Returns:
            numpy.array with star profile
    """
    x, y = create_meshgrid(imshape)
    mod = Moffat2D(amplitude=amplitude, x_0=x_0,
                   y_0=y_0, gamma=radius, alpha=alpha)

    return mod(x, y)


def create_Gaussian(imshape, amplitude=1, x_mean=0, y_mean=0,
                    x_stddev=None, y_stddev=None,
                    theta=None):
    """
    Create a Gaussian distribution
    Parameters:
        imshape (numpy.array): image shape given for calculating size of distribution
        amplitude (float): amplitude of the Moffat distribution
        x_mean (float): average value of x
        y_mean (float): average value of y
        x_stddev (float): standard deviation in x
        y_stddev (float): standard deviation in y
        theta (float): rotation angle of distribution

    Returns:
        numpy.array with Gaussian profile
    """

    x, y = create_meshgrid(imshape)

    mod = Gaussian2D(amplitude=amplitude,
                     x_mean=x_mean, y_mean=y_mean,
                     x_stddev=x_stddev, y_stddev=y_stddev,
                     theta=theta)

    return mod(x, y)


def create_noise(imshape, noise_level, seed=42):
    """
    Generate Poisson noise into images.
        Parameters:
            imshape (numpy.array): image to generate noise for
            noise_level (unsigned float): Poisson lambda parameter
            seed (float): random seed for reproducibility
        Return:
            numpy.array to be added to image.
    """

    rs = rand.RandomState(seed)
    return rs.poisson(noise_level, size=imshape.shape)


def combine_sky_imshape(imshape_list, amplitude_list):
    """
    Combine clean sky images.
        Parameters:
            imshape_list (list): image objects to combine
            amplitude_list (list): amplitudes of the given imshapes
        Return:
            (numpy.array) Single image with imshape_list objects in it.
    """
    imshape_new = np.zeros((imshape_list[0].shape[0],
                            imshape_list[0].shape[1]))

    for imshape, amplitude in zip(imshape_list, amplitude_list):
        imshape_new += amplitude * imshape
    return imshape_new


def create_lensing_event(canvas, center=(0., 0.), arc_obj=None,
                         star_radius=0.0, star_intensity=1.0):
    """
    Generate an image that mimics the geometric realities of a gravitational lens.
        Parameters:
            canvas (numpy.array): image object that will include gravitational lens
            center (Tuple(float, float)): center of lensing event
            arc_obj( list(list(float)) ): list of arc objects and their parameters
                                            arc: [radius, arc width, start_angle, end_angle]
            star_radius (float): radius of star in image
            star_intensity (float): intensity of star in image.
        Returns:
            (numpy.array) Image of gravitational lensing event.
    """
    if star_radius == 0.0:
        hasStar = rand.uniform(0., 1.) < 0.6
        if hasStar:
            star_radius = rand.uniform(5.0, 20.0)
            star_intensity = rand.uniform(0.5, 2.0)
            star = create_Moffat2D(canvas, amplitude=star_intensity,
                                   x_0=center[0], y_0=center[1],
                                   radius=star_radius)
            canvas += star
    else:
        star = create_Moffat2D(canvas, amplitude=star_intensity,
                               x_0=center[0], y_0=center[1],
                               radius=star_radius)
        canvas += star

    for arc in arc_obj:
        arcShape = create_arc(canvas, center, radius=arc[0],
                              width=arc[1], theta1=arc[2],
                              theta2=arc[3])
        canvas += arcShape * arc[4]
    return canvas
