from abc import abstractmethod, ABC
from PIL import Image as PILImage
import os
import numpy as np

from src.deepbench import astro_object


class Image(ABC):
    @abstractmethod
    def __init__(self, object_list, image_shape):
        # TODO Change to something less ambigious than 'objects'
        self.objects = object_list
        self.image_shape = image_shape
        self.image = None

    def __len__(self):
        return len(self.objects)

    def _image_parameters(self):
        return self.image_shape, self.objects

    def combine_objects(self):
        raise NotImplementedError

    def generate_noise(self, noise_type):
        raise NotImplementedError

    def _generate_astro_object(self, object_type, object_parameters):

        if object_type == "test_object":
            astro_object_map = {"test_object": ObjectForTesting}

        else:
            # TODO Replace with real class names and verify naming scheme
            # TODO Check where Sin objects are/if they're included
            # TODO Remove this if/else once astro objects are implimented
            astro_object_map = {
                "star": astro_object.star_object.StarObject,
                "strong_lens": astro_object.strong_lens_object.StrongLensObject,
                "galaxy": astro_object.galaxy_object.GalaxyObject,
                "spiral_galaxy": astro_object.spiral_galaxy_object.SpiralGalaxyObject,
                "n_body": astro_object.n_body_object.NBodyObject,
            }

        if object_type not in astro_object_map.keys():
            raise NotImplementedError(
                f"Object type {object_type}, is not available. "
                f"Please select object from {astro_object_map.keys()}"
            )

        object_parameters["image_shape"] = self.image_shape

        return astro_object_map[object_type](**object_parameters)

    def save_image(self, save_dir="results", image_name="image_1", image_format="jpg"):

        assert self.image is not None, "Image not instantiated"

        save_dir = save_dir.rstrip("/")

        if not os.path.exists(save_dir):
            os.makedirs(save_dir)

        # TODO Check with multiple image shapes
        image = PILImage.fromarray(self.image, "RGB")
        save_path = f"{save_dir}/{image_name}.{image_format}"

        image.save(save_path)


class ObjectForTesting:
    def __init__(self, image_shape):
        self.image = np.zeros(image_shape)

    def create_object(self):
        return self.image
