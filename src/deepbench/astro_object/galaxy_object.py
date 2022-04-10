from astro_object import AstroObject
from shape_generator.shape_generator import create_empty_shape
from astropy.modeling.models import Sersic2D

import numpy as np
from numpy import random


class GalaxyObject(AstroObject):

    # BOUNDS: ellipse -> (0,1), n -> (0.5, 1.0)
    def __init__(
        self,
        img_dim,
        amplitude=1,
        center=(50, 50),
        radius=25,
        n=1.0,
        ellipse=random.uniform(0.1, 0.9),
        theta=random.uniform(-1.5, 1.5),
    ):

        super().__init__(image_dimensions=img_dim, radius=radius, amplitude=amplitude)

        self._center = center
        self._n = n
        self._ellipse = ellipse
        self._theta = theta

    def create_Sersic_profile(self, center_x, center_y):

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

    def create_object(self, center_x: float, center_y: float) -> np.ndarray:
        """
        Create the star object from a Moffat distribution and Poisson and PSF noise.

        Args:
            center_x (float): The x-axis placement of the star object.
            center_y (float): The y-axis placement of the star object.

        Returns:
            ndarray: Two dimensional Galaxy object, composed of Sersic Distribution and noise appendings.

        Examples:

            >>> example_prof = example_star.create_object(center_x = 1.0, center_y = 0.0)

        """

        # Create the empty image shape.
        image_shape = create_empty_shape(self._image)

        # Create the Poisson noise profile specific to Galaxy objects.
        noise_profile = self.create_noise(galaxy=True)

        image_shape = self.create_Sersic_profile(
            center_x=self._center[0], center_y=self._center[1]
        )

        # Append the noise profiles to the object.
        image_shape += noise_profile
        image_shape = self.create_psf(image_shape)

        return image_shape

    def displayImage(self):

        # To be implemented. Check parent for details.

        print("Code Container.")
