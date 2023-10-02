from typing import Union
from deepbench.image.image import Image
from deepbench import astro_object
import numpy as np


class SkyImage(Image):
    def __init__(
        self,
        image_shape,
        object_noise_level=0,
        object_noise_type="gaussian",
        scale=True,
    ):
        """
        Create an image that is a composition of multiple astronomy objects

        Args:
            image_shape (tuple(int, int)): Shape of the output image
            object_noise_level (int, optional): Level of noise added to the full image. Defaults to 0.
            object_noise_type (str, optional): Type of noise added. Defaults to "gaussian".
            scale (bool, optional): Scale objects between 0 and 1 before adding to the composition

        """
        self.scale = scale
        assert len(image_shape) >= 2, "Image must be 2D or higher."
        super().__init__(image_shape, object_noise_type, object_noise_level)

    def _generate_astro_object(self, object_type, object_parameters):

        astro_object_map = {
            "star": astro_object.star_object.StarObject,
            "galaxy": astro_object.galaxy_object.GalaxyObject,
            "spiral_galaxy": astro_object.spiral_galaxy.SpiralGalaxyObject,
        }

        if object_type not in astro_object_map.keys():
            raise NotImplementedError(
                f"Object type {object_type}, is not available. "
                f"Please select object from {astro_object_map.keys()}"
            )

        return astro_object_map[object_type](**object_parameters)

    def _scale(self, input_image):
        image = input_image.copy()
        image = (image - input_image.min()) / (input_image.max() - input_image.min())
        return image

    def combine_objects(
        self,
        objects: Union[list, str],
        instance_params: Union[list, dict],
        object_params: Union[list, dict],
        seed: int = 42,
    ):
        """
        Utilize Image._generate_astro_objects to overlay all selected astro objects into one image
        If object parameters are not included in object list, defaults are used.
        Updates SkyImage.image.

        Current input parameter assumptions (totally up to change):
        For a single image:
        [{
            "object_type":"<object_type>",
            "object_parameters":{<parameters for that object>}
        }]

        Args:
            objects (list): str discriptors of the included object
            instance_params (list): Parameters for the instance of the object (ei, overall noise)
            object_params (list): Parameters of each object (ei: position in frame)
            seed (int, optional): random seed for noise. Defaults to 42.

        Returns:
            ndarray : image with objects and noise

        """
        object_images = []

        if type(objects) == str:
            objects = [objects]
        if type(instance_params) == dict:
            instance_params = [instance_params]
        if type(object_params) == dict:
            object_params = [object_params]

        for sky_object, sky_params, object in zip(
            objects, instance_params, object_params
        ):
            import matplotlib.pyplot as plt

            sky_params["image_dimensions"] = self.image_shape
            if "noise_level" not in sky_params:
                sky_params["noise_level"] = 0

            additional_sky_object = self._generate_astro_object(sky_object, sky_params)

            object_image = additional_sky_object.create_object(**object)
            if self.scale:
                object_image = self._scale(object_image)

            object_images.append(object_image)

        noise = self.generate_noise(seed)
        object_images.append(noise)
        image = np.sum(object_images, axis=0)

        return image
