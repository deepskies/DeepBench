import inspect
from typing import Tuple
from deepbench.shapes import Shapes as ShapeGenerator
from deepbench.image.image import Image


class ShapeImage(Image):
    """
    Create an image that is a composition of multiple shapes

    Args:
        image_shape (Tuple[int, int]): Dimensions of the shape image.
        object_noise_type (str, optional): Noise distribution applied to image. Defaults to "gaussian".
        object_noise_level (float, optional): Relative noise level (scale 0 to 1). Defaults to 0.0.

    """

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

    def combine_objects(self, objects, object_params, instance_params=None, seed=42):
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
            object_params (list): Parameters of each object (ie, position in frame)
            seed (int, optional): random seed for noise. Defaults to 42.

        Returns:
            ndarray : image with objects and noise

        """
        image = self.shapes.create_empty_shape()

        if type(objects) == str:
            objects = [objects]

        if type(object_params) == dict:
            object_params = [object_params]
            
        for shape, params in zip(objects, object_params):
            image += self._create_object(shape, params)
     
        noise = self.generate_noise(seed)
        image += noise
        return image
