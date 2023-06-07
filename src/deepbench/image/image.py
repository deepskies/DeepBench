from abc import abstractmethod, ABC
from typing import Tuple
from PIL import Image as PILImage
import os
import numpy as np


class Image(ABC):
    @abstractmethod
    def __init__(
        self,
        image_shape: Tuple[int, int],
        object_noise_type: str = "gaussian",
        object_noise_level: float = 0.0,
    ):
        assert len(image_shape) >= 2
        "All images must be in at least 2d."

        self.image_shape = image_shape
        self.image = np.zeros(self.image_shape)

        self.object_noise_type = object_noise_type
        self.object_noise_level = object_noise_level

    def create_empty_shape(self):
        return np.zeros(self.image_shape)

    def __len__(self):
        return len(self.objects)

    def _image_parameters(self):
        return self.image_shape, self.objects

    def combine_objects(self, objects, object_params, seed=42):
        raise NotImplementedError

    def generate_noise(self, seed=42):
        """
        Add noise to an image
        Updates SkyImage.image

        """
        noise_map = {
            "gaussian": self._generate_gaussian_noise,
            "poisson": self._generate_poisson_noise,
        }

        if self.object_noise_type not in noise_map.keys():
            raise NotImplementedError(f"{self.object_noise_type} noise not available")

        noise = noise_map[self.object_noise_type](seed)
        return noise

    def save_image(self, save_dir="results", image_name="image_1", image_format="jpg"):
        """
        Save the generated image into the specified directory.
        Will create directory if it does not already exist.

        :param save_dir: Directory to save
        :param image_name: base name of the saved image
        :param image_format: file format. Recommended jpg
        :return: None
        """

        assert self.image is not None, "Image not instantiated"

        save_dir = save_dir.rstrip("/")

        if not os.path.exists(save_dir):
            os.makedirs(save_dir)

        # TODO Check with multiple image shapes
        image = PILImage.fromarray(self.image, "RGB")
        save_path = f"{save_dir}/{image_name}.{image_format}"

        image.save(save_path)

    def _generate_gaussian_noise(self, seed=42):
        return np.random.default_rng(seed=seed).normal(
            scale=self.object_noise_level, size=self.image_shape
        )

    def _generate_poisson_noise(self, seed=42):
        return np.random.default_rng(seed=seed).poisson(
            lam=self.object_noise_level, size=self.image.shape
        )
