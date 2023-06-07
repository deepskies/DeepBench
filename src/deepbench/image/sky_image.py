from src.deepbench.image.image import Image
from src.deepbench import astro_object


class SkyImage(Image):
    def __init__(self, image_shape, object_noise_level=0, object_noise_type="gaussian"):

        assert len(image_shape) >= 2, "Image must be 2D or higher."
        super().__init__(image_shape, object_noise_type, object_noise_level)

    def _generate_astro_object(self, object_type, object_parameters):
        """
        Utilize the astro_object module and generate instances of the classes

        :param object_type: String identifier of the class.
            Pick from ["star", "strong_lens”, "galaxy", "spiral_galaxy", "n_body"]
        :param object_parameters: Dictionary of the parameters required for the selected class
            Any passed image_shape will be overwritten into Image.image_shape.
        :return: Instance of the selected class initialized with passed object parameters.
        """

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

    def combine_objects(self, objects, instance_params, object_params, seed=42):

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
