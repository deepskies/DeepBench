from src.deepbench.astro_object.galaxy_object import GalaxyObject

from numpy import log2, random
from numpy import tan


class SpiralGalaxyObject(GalaxyObject):
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

    def create_sprial_profile(self, center_x, center_y):
        "ref paper: https://doi.org/10.1111/j.1365-2966.2009.14950.x"

        spiral = self._amplitude / log2(
            self.spiral_pitch * tan(self._theta / (2 * self.winding_number))
        )
        # TO BE IMPLEMENTED.
        # WHERE IS THE CODE FOR THIS????????
        return random.default_rng().uniform(size=self._image.shape) * spiral

    def create_object(self, center_x, center_y):
        image_shape = self._image.copy()

        # Add the spiral to the image
        spiral = self.create_sprial_profile(center_x, center_y)
        image_shape += spiral

        # Create the Poisson noise profile.
        noise_profile = self.create_noise(galaxy=True)

        # Append the noise profiles to the object.
        image_shape += noise_profile
        image_shape = self.create_psf(image_shape)

        return image_shape

    def displayObject(self):
        print("Code Container")
