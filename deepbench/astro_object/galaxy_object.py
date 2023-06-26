from typing import Union, Tuple
from deepbench.astro_object.astro_object import AstroObject
from astropy.modeling.models import Sersic2D

import numpy as np
from numpy import random


class GalaxyObject(AstroObject):

    """

    Produce a 2D galaxy using a Sersic2D distribution.
    View https://docs.astropy.org/en/stable/api/astropy.modeling.functional_models.Sersic2D.html
    for implimentation details.

    Args:
        image_dimensions (Union[tuple(int,int), tuple(float,float)]): The dimension(s) of the object to be produced.
        amplitude (Union[int, float]): The amplitude of the object to be produced, surface brightness at radius.
        noise_level (Union[float, list[float]]): The Poisson noise level (lambda, the  expected seperation) to be applied to the object.
        radius (int, optional): Effective half-light radius of the galaxy. Defaults to 25.
        n (float, optional): Sersic Index. Defaults to 1.0.
        ellipse (float, optional): Galaxy Ellipticity. Defaults to random.uniform(0.1, 0.9).
        theta (float, optional): The rotation of the galaxy in radians. Defaults to random.uniform(-1.5, 1.5).
    Examples:

        >>> example_galaxy = GalaxyObject(image_dimensions=28)

    """

    def __init__(
        self,
        image_dimensions: Union[Tuple[int, int], Tuple[float, float]],
        amplitude=1,
        radius=25,
        n=1.0,
        noise_level=0.2,
        ellipse=random.uniform(0.1, 0.9),
        theta=random.uniform(-1.5, 1.5),
    ):
        super().__init__(
            image_dimensions=image_dimensions,
            radius=radius,
            amplitude=amplitude,
            noise_level=noise_level,
        )

        self._n = n
        self._ellipse = ellipse
        self._theta = theta

    def create_Sersic_profile(self, center_x, center_y):
        """
        Wrapper for https://docs.astropy.org/en/stable/api/astropy.modeling.functional_models.Sersic2D.html

        Args:
            center_x (float): x position of the center of the galaxy
            center_y (float): y position of the center of the galaxy

        Returns:
            galaxy (numpy.array): created galaxy profile
        """

        x, y = self.create_meshgrid()
        profile = Sersic2D(
            amplitude=self._amplitude,
            x_0=center_x,
            y_0=center_y,
            r_eff=self._radius,
            n=self._n,
            ellip=self._ellipse,
            theta=self._theta,
        )

        return profile(x, y)

    def create_object(self, center_x=5.0, center_y=5.0) -> np.ndarray:
        """
        Create the galaxy object from a Sersic distribution and Poisson or PSF noise.

        Args:
            center_x (float): The x-axis placement of the galaxy object.
            center_y (float): The y-axis placement of the galaxy object.

        Returns:
            ndarray: Two dimensional Galaxy object, composed of Sersic Distribution and noise appendings.

        Examples:

            >>> example_prof = example_star.create_object(center_x = 1.0, center_y = 0.0)

        """

        # Create the empty image shape.
        # Create the Poisson noise profile specific to Galaxy objects.
        noise_profile = self.create_noise(galaxy=True)

        image_shape = self.create_Sersic_profile(center_x=center_x, center_y=center_y)

        # Append the noise profiles to the object.
        image_shape += noise_profile
        image_shape = self.create_psf(image_shape)

        return image_shape

    def displayObject(self):
        """
        Display the object created in a 2d plot

        Raises:
            NotImplementedError: Raised if not implimented in the child class
        """

        raise NotImplementedError()
