import numpy as np
from matplotlib.path import Path


class ShapeGenerator:
    def __init__(self):
        pass

    @staticmethod
    def resize(image, resize_dimensions):
        pass

    @staticmethod
    def _convert_patch_to_image(image, image_shape=(28, 28)):
        n_dim = len(image_shape)
        image_shape = [int(np.ceil(n)) for n in image_shape]

        if n_dim < 2:
            raise ValueError(
                f"Image shape input of length {n_dim}; but input must be length >=2"
            )

        if 0 in image_shape:
            raise ValueError(f"Image size must be greater than 0")

        dim_array = [np.arange(1, image_shape[dim]) for dim in [0, 1]]
        grid = np.meshgrid(*dim_array)

        coordinates = np.array(list(zip(*(c.flat for c in grid))))

        vert_path = Path(image.get_verts())
        valid_coordinates = vert_path.contains_points(coordinates)
        path_points = coordinates[valid_coordinates]

        out_image = np.zeros(image_shape)
        points = [path_points[:, dim] for dim in [0, 1]]
        out_image[points] = 1

        return out_image

    @staticmethod
    def create_rectangle():
        pass

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
