from src.deepbench.image.image import Image
from scipy import ndimage
import numpy as np

from src.deepbench import astro_object


class SkyImage(Image):
    def __init__(self, objects, image_shape):
        super().__init__(objects, image_shape)

    def combine_objects(self):
        image = np.zeros(self.image_shape)

    def generate_noise(self, noise_type, **kwargs):
        noise_map = {
            "gaussian": self._generate_gaussian_noise,
            "poisson": self._generate_poisson_noise,
        }

        if noise_type not in noise_type.keys():
            raise NotImplementedError(f" {noise_type} noise type not available")

        assert self.image is not None, "Unable to add noise, please instantiate objects"
        noise = noise_map[noise_type](**kwargs)

        return noise

    def _generate_astro_object(self, object_type):
        astro_object_map = {
            "star": astro_object.Star,
            "strong_lens": astro_object.StrongLens,
        }
        if object_type not in astro_object_map.keys():
            raise NotImplementedError()

    # TODO Move to own module/to image module
    def _generate_gaussian_noise(self, sigma):
        return ndimage.gaussian_filter(self.image, sigma=sigma)

    def _generate_poisson_noise(self, image_noise):
        return np.random.poisson(lam=image_noise, size=self.image.shape)
