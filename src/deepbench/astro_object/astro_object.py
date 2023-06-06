from abc import ABC, abstractclassmethod, abstractmethod
from typing import Union, List
from scipy import ndimage
import numpy.random as rand
import numpy as np


class AstroObject(ABC):
    """
    Description container.
    """

    def __init__(
        self,
        image_dimensions: Union[int, float, List[int], List[float]],
        radius: Union[int, float],
        amplitude: Union[int, float],
        noise_level: Union[float, List[float]],
    ) -> None:
        """
        The initialization function for the Abstract AstroObject class.

        Args:
            image_dimensions (Union[int, float, List[int], List[float]]): The dimension(s) of the object to be produced.
            radius (Union[int, float]): The radius of the object to be produced.
            amplitude (Union[int, float]): The amplitude of the object to be produced.
            noise_level (Union[float, list[float]]): The Poisson noise level to be applied to the object.

        Examples:

            >>> example_obj = AstroObject(image_dimensions=28, radius=5, amplitude=3, noise_level=0.7)
        """

        #   TODO:
        #   - May need a position param: position=(0,0)

        self._image = np.zeros((image_dimensions, image_dimensions))
        self._radius = radius
        self._amplitude = amplitude
        self._noise_level = noise_level

    @abstractmethod
    def create_object(self):
        """
        Creates the astronomical object.

        Raises:
            NotImplementedError: If the child class does not implement the method.
        """
        raise NotImplementedError()

    def create_psf(self, image_shape, gaussian_blur=0.7) -> np.ndarray:
        """
        Creates the Point Spread Function to append to the object.

        Args:
            gaussian_blur (float): The level of gaussian blur to be applied.

        Returns:
            ndarray: The PSF as an array the same shape as the input.

        Examples:
            >>> example_obj.create_psf(gaussian_blur=1.2)
            >>> example_obj.create_psf()
        """
        return ndimage.gaussian_filter(image_shape, sigma=gaussian_blur)

    # UPDATE THIS METHODS DOCSTRINGS.

    def create_noise(self, seed=42, galaxy=False) -> np.ndarray:
        """
        Creates the Poisson noise added to the object.

        Args:
            seed (int): The random initialization seed used for reproducibility.

        Returns:
            ndarray: A random sample drawn from a Poisson distribution.

        Examples:
            >>> example_obj.create_noise()
            >>> example_obj.create_noise(seed=5)
        """
        if galaxy:
            rs = rand.RandomState(seed)
            return rs.poisson(self._noise_level * 10.0, size=self._image.shape)
        else:
            rs = rand.RandomState(seed)
            return rs.poisson(self._noise_level, size=self._image.shape)

    def create_meshgrid(self) -> np.ndarray:
        """
        Creates a meshgrid for the object.

        Returns:
            ndarray: A vector of coordinates.

        Examples:
            >>> example_obj.create_meshgrid()
        """
        meshgrid = np.meshgrid(
            np.arange(self._image.shape[0]),
            np.arange(self._image.shape[1]),
        )

        return meshgrid

    @abstractmethod
    def displayObject(self):

        # Yet to implement. Will essentially just display a matplotlib image of the Object.

        print("Code Container.")
        raise NotImplementedError()
