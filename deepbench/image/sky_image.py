from typing import Union
from deepbench.image.image import Image
from deepbench import astro_object


class SkyImage(Image):
    def __init__(self, image_shape, object_noise_level=0, object_noise_type="gaussian"):
        """
        Create an image that is a composition of multiple astronomy objects

        Args:
            image_shape (tuple(int, int)): Shape of the output image
            object_noise_level (int, optional): Level of noise added to the full image. Defaults to 0.
            object_noise_type (str, optional): Type of noise added. Defaults to "gaussian".

        """
        assert len(image_shape) >= 2, "Image must be 2D or higher."
        super().__init__(image_shape, object_noise_type, object_noise_level)

    def _generate_astro_object(self, object_type, object_parameters):

        astro_object_map = {
            "star": astro_object.star_object.StarObject,
            "galaxy": astro_object.galaxy_object.GalaxyObject,
            "spiral_galaxy": astro_object.spiral_galaxy.SpiralGalaxyObject,
            "n_body": astro_object.n_body_object.NBodyObject,
        }

        if object_type not in astro_object_map.keys():
            raise NotImplementedError(
                f"Object type {object_type}, is not available. "
                f"Please select object from {astro_object_map.keys()}"
            )

        return astro_object_map[object_type](**object_parameters)

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
        image = self.create_empty_shape()
        if type(objects) == str:
            objects = [objects]
        if type(instance_params) == dict:
            instance_params = [instance_params]
        if type(object_params) == dict:
            object_params = [object_params]

        for sky_object, sky_params in zip(objects, instance_params):
            sky_params["image_dimensions"] = self.image_shape[0]
            additional_sky_object = self._generate_astro_object(sky_object, sky_params)
            for object in object_params:
                object_image = additional_sky_object.create_object(**object)
                image += object_image

        noise = self.generate_noise(seed)
        image += noise
        return image
