from abc import ABC, abstractclassmethod

from scipy import ndimage
import numpy.random as rand
import numpy as np


class AstroObject(ABC):
    def __init__(self, image_dim, position, radius, amplitude, noise, gaussian_blur):
        """
        Comment Container.
        """
        self.image = np.zeros((image_dim, image_dim))
        self.pos = position
        self.rad = radius
        self.amp = amplitude
        self.noise = noise
        self.blur = gaussian_blur

    def create_object(self):
        """
        Function Description.

        Args:
            Argument Container.
        Returns:
            Output Container.
        Raises:
            Error Container.
        """
        raise NotImplementedError()

    def create_psf(self):
        """
        Comment Container.
        """
        self.image = ndimage.gaussian_filter(self.image, sigma=self.image_blur)

    def create_noise(self):
        """
        Comment Container.
        """
        self.image += rand.poisson(lam=self.image_noise, size=self.image.shape)
