import numpy.random as rand
import numpy as np
import scipy.ndimage
from deepbench.module_draw.generate_draw import *


class AstroObject:

    def __init__(self, position, radius, amplitude, image_noise, gaussian_blur, image_dim):
        """
        :param position:
        :param radius:
        :param amplitude: (float) magnitude of image
        :param image_noise: (float) lambda of Poissonian distribution for image noise
        :param gaussian_blur: (float) deviation (sigma) of Gaussian
        :param image_dim: (int) image dimensions
        """
        self.center = position
        self.radius = radius
        self.amplitude = amplitude
        self.image_noise = image_noise
        self.image_blur = gaussian_blur
        self.image = np.zeros((image_dim, image_dim))

    def create_psf(self):
        """
        :return:
        """

        self.image = scipy.ndimage.gaussian_filter(self.image, sigma=self.image_blur)

    def create_noise(self):
        """
        :return:
        """
        self.image += rand.poisson(lam=self.image_noise, size=self.image.shape)