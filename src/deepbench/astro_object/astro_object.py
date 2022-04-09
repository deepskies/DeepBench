from abc import ABC, abstractclassmethod, abstractmethod

from scipy import ndimage
import numpy.random as rand
import numpy as np


class AstroObject(ABC):
    def __init__(self, image_dimensions, radius, amplitude, noise_level):
        """
        Comment Container.
        """

        #   TODO:
        #   - May need a position param: position=(0,0)

        self._image = np.zeros((image_dimensions, image_dimensions))
        self._radius = radius
        self._amplitude = amplitude
        self._noise_level = noise_level

    @abstractmethod
    def create_object(self):
        """
        Function Description.

        :param container: Container Description.
        :type container: Container Type.
        :raise Error: Error Description.
        :return: Output Description.
        :rtype: list[str]
        """
        raise NotImplementedError()

    @staticmethod
    def create_psf(self, gaussian_blur=0.7):
        """ """
        return ndimage.gaussian_filter(self._image.shape, sigma=gaussian_blur)

    @staticmethod
    def create_noise(self, seed=42):
        """ """

        rs = rand.RandomState(seed)
        return rs.poisson(self._noise_level, size=self.image.shape)

    @staticmethod
    def create_meshgrid(self):
        """ """
        meshgrid = np.meshgrid(
            np.arange(np.shape(self.image.shape)[0]),
            np.arange(np.shape(self.image.shape)[1]),
        )

        return meshgrid
