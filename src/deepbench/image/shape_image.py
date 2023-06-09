import inspect
from typing import Tuple
from src.deepbench.shape_generator.shape_generator import ShapeGenerator
from src.deepbench.image.image import Image


class ShapeImage(Image):
    def __init__(
        self,
        image_shape: Tuple[int, int],
        object_noise_type: str = "gaussian",
        object_noise_level: float = 0.0,
    ):
        self.shapes = ShapeGenerator(image_shape=image_shape)
        self.method_map = self._get_methods()
        super().__init__(
            image_shape=image_shape,
            object_noise_level=object_noise_level,
            object_noise_type=object_noise_type,
        )

    def _get_methods(self):
        methods = [
            method
            for method in inspect.getmembers(
                ShapeGenerator, predicate=inspect.isfunction
            )
            if "create_" in method[0]
        ]

        return {method[0].split("_")[-1]: method[1] for method in methods}

    def _create_object(self, shape, shape_params):

        if shape not in self.method_map.keys():
            raise NotImplementedError()
        return self.method_map[shape](self.shapes, **shape_params)

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
        image = self.shapes.create_empty_shape()

        if type(objects) == str:
            objects = [objects]
        if type(instance_params) == dict:
            instance_params = [instance_params]
        if type(object_params) == dict:
            object_params = [object_params]

        for shape, _ in zip(objects, instance_params):
            for object in object_params:
                image += self._create_object(shape, object)
        noise = self.generate_noise(seed)
        image += noise
        return image
