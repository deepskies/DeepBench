from deepbench.astro_object.astro_object import AstroObject
from astropy.modeling.models import Moffat2D

from typing import Union, List, Tuple

import numpy as np


class StarObject(AstroObject):
    """
       Create Stars

       Args:
    image_dimensions (Union[int, float, List[int], List[float]]): The dimension(s) of the object to be produced.
           radius (Union[int, float]): The radius of the object to be produced.
           amplitude (Union[int, float]): The amplitude (brightness) of the object to be produced.
           noise_level (Union[float, list[float]]): The Poisson noise level (lambda, the  expected seperation) to be applied to the object.
        seed (Union[float, list[float]], optional): Seed to set the random state for noise in the object. Initialized at the init of the class. Default None.

       Examples:

           >>> example_star = StarObject(image_dimensions=28, noise=5.0, center=3, radius=0.7, amplitude=1.2)
           >>> example_star = StarObject(image_dimensions=(28,28), noise=5.0)
    """

    def __init__(
        self,
        image_dimensions: Union[int, float, List[int], List[float]],
        noise_level: Union[float, List[float]] = 0.0,
        radius: Union[int, float] = 1.0,
        amplitude: Union[int, float] = 1.0,
        seed: Union[int, None] = None,
    ) -> None:

        super().__init__(
            image_dimensions=image_dimensions,
            radius=radius,
            amplitude=amplitude,
            noise_level=noise_level,
            seed=seed,
        )

    def create_Moffat_profile(
        self, center_x: float, center_y: float, alpha=1.0
    ) -> np.ndarray:
        """
        Create the Moffat distribution used to simulate star objects.

        Args:
            center_x (float): The x-axis placement of the star object.
            center_y (float): The y-axis placement of the star object.
            alpha (float): The luminosity of the Moffat distribution.

        Returns:
            ndarray: Two dimensional Moffat distribution.

        Examples:

            >>> example_prof = example_star.create_Moffat_profile(center_x = 1.0, center_y = 0.0, alpha=200.0)
            >>> example_prof = example_star.create_Moffat_profile(center_x = 1.0, center_y = 0.0)

        """
        x, y = self.create_meshgrid()
        profile = Moffat2D(
            amplitude=self._amplitude,
            x_0=center_x,
            y_0=center_y,
            gamma=self._radius,
            alpha=alpha,
        )

        return profile(x, y)

    def create_object(self, center_x: float, center_y: float, alpha=1.0) -> np.ndarray:
        """
        Create the star object from a Moffat distribution and Poisson and PSF noise.

        Args:
            center_x (float): The x-axis placement of the star object.
            center_y (float): The y-axis placement of the star object.
            alpha (float): The luminosity of the Moffat distribution.

        Returns:
            ndarray: Two dimensional Star object, composed of Moffat Distribution and noise appendings.

        Examples:

            >>> example_prof = example_star.create_object(center_x = 1.0, center_y = 0.0, alpha=200.0)
            >>> example_prof = example_star.create_object(center_x = 1.0, center_y = 0.0)

        """

        # Create the empty image shape.
        image_shape = self._image.copy()

        # Create the Poisson noise profile.
        noise_profile = self.create_noise()

        image_shape = self.create_Moffat_profile(
            center_x=center_x, center_y=center_y, alpha=alpha
        )

        # Append the noise profiles to the object.
        image_shape += noise_profile
        image_shape = self.create_psf(image_shape)

        return image_shape

    def displayObject(self):

        # To be implemented. Check parent for details.

        print("Code Container.")
