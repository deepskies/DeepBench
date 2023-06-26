from deepbench.shape_generator.shape_generator import ShapeGenerator
from deepbench.astro_object.astro_object import AstroObject
from typing import Union, List, Tuple

from numpy import random
import numpy as np


class SpiralObject(AstroObject):
    def __init__(
        self,
        dimensions: Union[List[int], List[float], int, float],
        radius: Union[int, float] = 40,
        amplitude: Union[int, float]=1,
        noise_level: float=0.7,
        center: Union[Tuple(int, int), Tuple(float, float)]=(50, 50),
        pitch_angle: Union[int, float]=30,
        arm_dict: dict = {"width": 50, "intensity": 20, "number": 4}
    ) -> None:
        """
        Creates a galaxy distribution using a logarithmic spiral profile.

        Args:
            dimensions: The dimensions of the galaxy object.
            radius: The radius of the galaxy object.
            amplitude: The amplitude of the galaxy object.
            noise_level: The noise level of the galaxy object.
            center: The center of the galaxy object.
            pitch_angle: The pitch angle of the galaxy object.
            arm_dict: The dictionary containing the arm width, intensity, and number of arms.
        """
        super().__init__(
            dimensions=dimensions,
            amplitude=amplitude,
            noise_level=noise_level,
            radius=radius,
            center=center
        )

        self.pitch_angle = pitch_angle
        self.arm_dict = arm_dict
        self._overall_size = 500

    def create_spiral_profile(self) -> np.ndarray:
        """
        Creates a spiral profile used to create the desired galaxy distribution.

        Returns:
            a two-dimensional numpy array that simulates the galaxy profile.
        """

        # Convert pitch angle to radians
        pitch_angle = np.deg2rad(self.pitch_angle)

        # Define the grid
        x = np.linspace(-self._overall_size / 2, self._overall_size / 2, self._overall_size)
        y = np.linspace(-self._overall_size / 2, self._overall_size / 2, self._overall_size)
        X, Y = np.meshgrid(x, y)

        # Calculate the distance from the center
        R = np.sqrt(X**2 + Y**2)

        # Calculate the angle from the x-axis
        theta = np.arctan2(Y, X) + np.pi

        # Create the spiral pattern
        spiral = np.zeros_like(R)

        for arm in range(self.arm_dict['number']):
            arm_angle = 2 * np.pi * arm / self.arm_dict['number']
            # Calculate logarithmic spiral
            r_spiral = ((self._radius *2) / (2 * np.pi)) * np.exp((theta - arm_angle) / np.tan(pitch_angle))

            # Calculate distance from each point to the spiral arm
            distance = np.abs(R - r_spiral)

            # Add arm intensity to the spiral pattern
            spiral += self.arm_dict['intensity'] * np.exp(-distance**2 / (2 * self.arm_dict['width']**2))

        # Add Poisson noise
        profile = np.random.poisson(spiral * self._noise)

        return profile


    def create_object(self) -> np.ndarray:
        """
        Create the galaxy object with the desired profile and noise.

        Returns:
            ndarray: Two dimensional Galaxy object, composed of spiral profile and noise.
        """

        # # Create the empty object shape.
        # obj_shape = ShapeGenerator().create_empty_shape(self._dims)

        # Create the Poisson noise profile specific to Galaxy objects.
        noise_profile = self.create_noise(galaxy=True)

        # Create the spiral galaxy profile
        image_shape = self.create_spiral_profile()

        # Append the noise profiles to the object.
        image_shape += noise_profile
        image_shape = self.create_psf(image_shape)

        return image_shape
    