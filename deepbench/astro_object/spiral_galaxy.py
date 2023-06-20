from deepbench.astro_object.galaxy_object import GalaxyObject

from numpy import log2, random
from numpy import tan


class SpiralGalaxyObject(GalaxyObject):
    """
    Create a spiral galaxy object

    Args:
        image_dimensions (Union[int, float, List[int], List[float]]): The dimension(s) of the object to be produced.
        amplitude (Union[int, float]): The amplitude of the object to be produced, surface brightness at radius.
        noise_level (Union[float, list[float]]): The Poisson noise level to be applied to the object.
        radius (int, optional): Effective half-light radius of the galaxy. Defaults to 25.
        n (float, optional): Sersic Index. Defaults to 1.0.
        ellipse (float, optional): Galaxy Ellicitcy. Defaults to random.uniform(0.1, 0.9).
        theta (float, optional): _description_. Defaults to random.uniform(-1.5, 1.5).
        winding_number (int, optional): number of arms. Defaults to 2.
        spiral_pitch (float, optional): severity of the spiral. Defaults to 0.2.
    """

    def __init__(
        self,
        image_dimensions,
        amplitude=1,
        radius=25,
        n=1.0,
        noise_level=0.2,
        ellipse=random.uniform(0.1, 0.9),
        theta=random.uniform(-1.5, 1.5),
        winding_number: int = 2,
        spiral_pitch: float = 0.2,
    ):
        self.winding_number = winding_number
        self.spiral_pitch = spiral_pitch

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
        """ref paper: https://doi.org/10.1111/j.1365-2966.2009.14950.x
        Impliment a spiral galaxy profile

        Args:
            center_x (float): x position of the center of the galaxy
            center_y (float): y position of the center of the galaxy


        Returns:
            spiral profile (numpy array): Profile representing the spiral galaxy
        """

        spiral = self._amplitude / log2(
            self.spiral_pitch * tan(self._theta / (2 * self.winding_number))
        )
        sersic = self.create_Sersic_profile(center_x, center_y)

        return sersic * spiral

    def create_object(self, center_x, center_y):
        """
        Create the galaxy object from a Sersic distribution and Poisson and PSF noise.

        Args:
            center_x (float): The x-axis placement of the galaxy object.
            center_y (float): The y-axis placement of the galaxy object.

        Returns:
            ndarray: Two dimensional Spiral object, composed of Spiral Distribution and noise appendings.

        Examples:

            >>> example_prof = example_spiral.create_object(center_x = 1.0, center_y = 0.0)

        """
        image_shape = self._image.copy()

        # Add the spiral to the image
        spiral = self.create_spiral_profile(center_x, center_y)
        image_shape += spiral

        # Create the Poisson noise profile.
        noise_profile = self.create_noise(galaxy=True)

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
