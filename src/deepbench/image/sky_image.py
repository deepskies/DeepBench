from src.deepbench.image.image import Image
from scipy import ndimage
import numpy as np

from src.deepbench import astro_object


class SkyImage(Image):
    def __init__(self, objects, image_shape):

        assert len(image_shape) >= 2, "Image must be 2D or higher."
        assert len(objects) >= 1, "Please pass at least one object per image"

        super().__init__(objects, image_shape)

    def combine_objects(self):
        self.image = np.zeros(self.image_shape)

        """
        Current input parameter assumptions (totally up to change):
        For a single image:
        [{"object_type":"<object_type>",
        "object_parameters":{<parameters specify to that object>}]
        """

        for object in self.objects:

            if "object_type" in object.keys() & "object_parameters" in object.keys():
                object_type = object["object_type"]
                object_parameters = object["object_parameters"]

                additional_object = self._generate_astro_object(
                    object_type, object_parameters
                )
                object_image = additional_object.create_object()

                self.image += object_image

    def generate_noise(self, noise_type, **kwargs):
        noise_map = {
            "gaussian": self._generate_gaussian_noise,
            "poisson": self._generate_poisson_noise,
        }

        if noise_type not in noise_map.keys():
            raise NotImplementedError(f"{noise_type} noise type not available")

        assert (
            self.image is not None
        ), "Image not generated, please run SkyImage.combine_objects"

        noise = noise_map[noise_type](**kwargs)
        self.image += noise

    def _generate_astro_object(self, object_type, object_parameters={}):
        # TODO Replace with real class names and verify naming scheme
        astro_object_map = {
            "star": astro_object.StarObject,
            "strong_lens": astro_object.StrongLensObject,
            "galaxy": astro_object.GalaxyObject,
            "spiral_galaxy": astro_object.SpiralGalaxyObject,
            "n_body": astro_object.NBodyObject,
        }
        if object_type not in astro_object_map.keys():
            raise NotImplementedError(
                f"Object type {object_type}, is not available. "
                f"Please select object from {astro_object_map.keys()}"
            )

        return astro_object_map[object_type](**object_parameters)

    def _generate_gaussian_noise(self, sigma=1):
        return ndimage.gaussian_filter(self.image, sigma=sigma)

    def _generate_poisson_noise(self, image_noise=1):
        return np.random.poisson(lam=image_noise, size=self.image.shape)
