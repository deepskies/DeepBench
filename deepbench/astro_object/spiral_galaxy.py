from typing import Tuple, Union
from deepbench.astro_object.galaxy_object import GalaxyObject
import numpy as np


class SpiralGalaxyObject(GalaxyObject):
    """
    Create a spiral galaxy object

    Args:
        image_dimensions (Union[Tuple(int,int), tuple(float,float)]): The dimension(s) of the object to be produced.
        amplitude (Union[int, float]): The amplitude of the object to be produced, surface brightness at the sersic radius.
        noise_level (Union[float, list[float]]): The Poisson noise level to be applied to the object.
        radius (int, optional): Effective half-light radius of the galaxy. Defaults to 25.
        arm_thickness (float, optional): Width of each arm of the spiral. Defaults to 1.0.
        winding_number (int, optional): number of arms. Defaults to 2.
        spiral_pitch (float, optional): Severity of the spiral, the pitch angle. Defaults to 0.2.
    Examples:

        >>> example_galaxy = SpiralGalaxyObject(image_dimensions=(28,28), winding_number=4)

    """

    def __init__(
        self,
        image_dimensions: Union[Tuple[int, int], Tuple[float, float]],
        amplitude=1,
        radius=25,
        arm_thickness=1.0,
        noise_level=0.2,
        winding_number: int = 2,
        spiral_pitch: float = 0.2,
        **kwargs
    ):
        self.pitch_angle = spiral_pitch
        self.winding_number = winding_number

        super().__init__(
            image_dimensions=image_dimensions,
            amplitude=amplitude,
            radius=radius,
            n=arm_thickness,
            ellipse=0.1,
            theta=0.1,
            noise_level=noise_level,
        )

    def create_spiral_profile(self, center_x, center_y):
        """

        ref paper: https://doi.org/10.1111/j.1365-2966.2009.14950.x
        Impliment a spiral galaxy profile

        Args:
            center_x (float): x position of the center of the galaxy
            center_y (float): y position of the center of the galaxy


        Returns:
            spiral profile (numpy array): Profile representing the spiral galaxy
        """

        # Define the grid
        side_length = self._image.shape
        x = np.linspace(-side_length[0] / 2, side_length[0] / 2, side_length[0])
        y = np.linspace(-side_length[1] / 2, side_length[1] / 2, side_length[1])
        X, Y = np.meshgrid(x, y)

        # Calculate the distance from the center
        R = np.sqrt(X**2 + Y**2)  # + np.sqrt(center_x**2 + center_y**2)

        # Calculate the angle from the x-axis
        theta = np.arctan2(Y, X) + np.pi

        # Create the spiral pattern
        spiral = np.zeros_like(R)
        for arm in range(self.winding_number):
            arm_angle = 2 * np.pi * arm / self.winding_number
            # Calculate logarithmic spiral
            r_spiral = ((self._radius * 2) / (2 * np.pi)) * np.exp(
                (theta - arm_angle) / np.tan(self.pitch_angle)
            )

            # Calculate distance from each point to the spiral arm
            distance = np.abs(R - r_spiral)

            # Add arm intensity to the spiral pattern
            spiral += self._amplitude * np.exp(-(distance**2) / (2 * self._n**2))

        return spiral

    def create_object(self, center_x, center_y) -> np.ndarray:
        """

        ref paper: https://doi.org/10.1111/j.1365-2966.2009.14950.x
        Create a spiral galaxy image

        Args:
            center_x (float): x position of the center of the galaxy
            center_y (float): y position of the center of the galaxy


        Returns:
            spiral profile (numpy array): Profile representing the spiral galaxy
        """

        # Create the Poisson noise profile specific to Galaxy objects.
        noise_profile = self.create_noise(galaxy=True)

        # Create the spiral galaxy profile
        image_shape = self.create_spiral_profile(center_x, center_y)

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
