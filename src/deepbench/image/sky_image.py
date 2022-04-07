from src.deepbench.image.image import Image
from scipy import ndimage
import numpy as np

import warnings


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

        for sky_object in self.objects:

            if "object_type" in sky_object.keys():
                object_type = sky_object["object_type"]

                if "object_parameters" in sky_object.keys():
                    object_parameters = sky_object["object_parameters"]

                    additional_sky_object = self._generate_astro_object(
                        object_type, object_parameters
                    )

                else:
                    # TODO Tests
                    # Use the default
                    additional_sky_object = self._generate_astro_object(object_type, {})

                object_image = additional_sky_object.create_object()

                self.image += object_image

            else:
                # TODO Test for this check
                warnings.warn(
                    "Parameter 'object_type' is needed to generate sky objects"
                )

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

    def _generate_gaussian_noise(self, sigma=1):
        return ndimage.gaussian_filter(self.image, sigma=sigma)

    def _generate_poisson_noise(self, image_noise=1):
        return np.random.poisson(lam=image_noise, size=self.image.shape)
