from abc import abstractmethod, ABC
from PIL import Image as PILImage
import os

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

    def generate_astro_object(self, object_type, object_parameters):
        # TODO Replace with real class names and verify naming scheme
        # TODO Check where Sin objects are
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

    def save_image(self, save_dir="results", image_name="image_1", image_format="jpg"):

        assert self.image is not None, "Image not instantiated"

        save_dir = save_dir.rstrip("/")

        if not os.path.exists(save_dir):
            os.makedirs(save_dir)

        # TODO Check with multiple image shapes
        image = PILImage.fromarray(self.image, "RGB")
        save_path = f"{save_dir}/{image_name}.{image_format}"

        image.save(save_path)
