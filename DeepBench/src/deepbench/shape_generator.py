import numpy as np
from matplotlib.path import Path
from matplotlib import patches
from skimage import transform


class ShapeGenerator:
    def __init__(self):
        pass

    @staticmethod
    def resize(image, resize_dimensions=(28, 28)):
        """
        Resize a numpy array

        :param image: Numpy array to resize
        :param resize_dimensions: tuple of integers to resize the passed image to
        :return: numpy array of shape resize_dimensions
        """
        resize_dimensions = tuple(map(lambda dim: int(np.ceil(dim)), resize_dimensions))
        if len(image.shape) != len(resize_dimensions):
            raise ValueError(
                f"Number of dimensions of source image ({image.shape} do not make target dimensions ({resize_dimensions})"
            )
        if 0 in resize_dimensions:
            raise ValueError(
                "Attempting to resize to an invalid size, please increase the size"
            )

        resized_image = transform.resize(image, resize_dimensions)
        return resized_image

    @staticmethod
    def _convert_patch_to_image(image, image_shape=(28, 28), cutout=None):
        """
        Converts a matplot path or patch object into a numpy array of the designated size

        :param image: Matplotlib image object to convert
        :param image_shape: Size of the desired image
        :return: numpy array of shape image_shape, containing the image
        """
        n_dim = len(image_shape)
        image_shape = tuple(map(lambda dim: int(np.ceil(dim)), image_shape))

        if n_dim < 2:
            raise ValueError(
                f"Image shape input of length {n_dim}; but input must be length >=2"
            )

        if 0 in image_shape:
            raise ValueError(f"Image size must be greater than 0")

        x = np.arange(1, image_shape[0])
        y = np.arange(1, image_shape[1])
        g = np.meshgrid(x, y)

        coords = np.array(list(zip(*(c.flat for c in g))))

        valid_coordinates = Path(image.get_verts()).contains_points(coords)
        ellipsepoints = coords[valid_coordinates]

        outim = np.zeros(image_shape)
        outim[ellipsepoints[:, 0], ellipsepoints[:, 1]] = 1.0

        if cutout is not None:
            cutout_coords = Path(cutout.get_verts()).contains_points(coords)
            cutout_points = coords[cutout_coords]
            outim[cutout_points[:, 0], cutout_points[:, 1]] = 0.0

        return outim

    @staticmethod
    def create_rectangle(
        image_shape=(28, 28),
        center=(14, 14),
        width=10,
        height=10,
        angle=0,
        line_width=1,
        fill=False,
    ):

        xy = (center[0] - (width / 2), center[1] - (height / 2))

        rectangle = patches.Rectangle(xy=xy, width=width, height=height, angle=angle)

        cutout = None
        if not fill:

            cutout_h = height - (2 * line_width)
            cutout_w = width - (2 * line_width)
            xy_cutout = (center[0] - (cutout_w / 2), center[1] - (cutout_h / 2))

            cutout = patches.Rectangle(
                xy=xy_cutout, width=cutout_w, height=cutout_h, angle=angle
            )

        rectangle_array = ShapeGenerator._convert_patch_to_image(
            rectangle, image_shape=image_shape, cutout=cutout
        )

        return rectangle_array

    @staticmethod
    def create_regular_polygon():
        pass

    @staticmethod
    def create_arc():
        pass

    @staticmethod
    def create_line():
        pass

    @staticmethod
    def create_ellipse():
        pass

    @staticmethod
    def create_empty_shape():
        pass

    # TODO Define the types of noise allowed
    # TODO Write method to apply noise
