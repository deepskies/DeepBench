from deepbench.astro_object.galaxy_object import GalaxyObject
import numpy as np


class SpiralGalaxyObject(GalaxyObject):
    """
    Create a spiral galaxy object

    Args:
        image_dimensions (Union[int, float, List[int], List[float]]): The dimension(s) of the object to be produced.
        amplitude (Union[int, float]): The amplitude of the object to be produced, surface brightness at the sersic radius.
        noise_level (Union[float, list[float]]): The Poisson noise level to be applied to the object.
        radius (int, optional): Effective half-light radius of the galaxy. Defaults to 25.
        n (float, optional): Sersic Index. Defaults to 1.0.
        ellipse (float, optional): Galaxy Ellipticity. Defaults to random.uniform(0.1, 0.9).
        theta (float, optional): The rotation of the galaxy in radians. Defaults to random.uniform(-1.5, 1.5).
        winding_number (int, optional): number of arms. Defaults to 2.
        spiral_pitch (float, optional): Severity of the spiral, the pitch angle. Defaults to 0.2.
    Examples:

        >>> example_galaxy = SpiralGalaxyObject(image_dimensions=28, winding_number=4)

    """

    def __init__(
        self,
        image_dimensions,
        amplitude=1,
        radius=25,
        n=1.0,
        noise_level=0.2,
        ellipse=np.random.uniform(0.1, 0.9),
        theta=np.random.uniform(-1.5, 1.5),
        winding_number: int = 2,
        spiral_pitch: float = 0.2,
    ):
        self.pitch_angle = spiral_pitch
        self.winding_number = winding_number

        super().__init__(
            image_dimensions=image_dimensions,
            amplitude=amplitude,
            radius=radius,
            n=n,
            ellipse=ellipse,
            theta=theta,
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

        pitch_angle = np.deg2rad(self.pitch_angle)

        # Define the grid
        x, y = self.create_meshgrid()

        # Calculate the distance from the center
        R = np.sqrt(center_x**2 + center_y**2)

        # Calculate the angle from the x-axis
        theta = np.arctan2(y, x) + np.pi

        # Create the spiral pattern
        spiral = np.zeros_like(self._image)

        for arm in range(self.winding_number):
            arm_angle = 2 * np.pi * arm / self.winding_number
            # Calculate logarithmic spiral
            r_spiral = ((self._radius * 2) / (2 * np.pi)) * np.exp(
                (theta - arm_angle) / np.tan(pitch_angle)
            )

            # Calculate distance from each point to the spiral arm
            distance = np.abs(R - r_spiral)

            # Add arm intensity to the spiral pattern
            spiral += self._amplitude * np.exp(
                -(distance**2) / (2 * self._radius**2)
            )

        # Add Poisson noise
        profile = np.random.poisson(spiral * self._noise_level)

        return profile

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
