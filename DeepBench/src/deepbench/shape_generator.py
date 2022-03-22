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
        :param image_shape: [tuple(int)] Size of the desired image
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
        meshgrid = np.meshgrid(x, y)

        coordinates = np.array(list(zip(*(c.flat for c in meshgrid))))

        valid_coordinates = Path(image.get_verts()).contains_points(coordinates)
        shape_points = coordinates[valid_coordinates]

        out_array = np.zeros(image_shape)
        out_array[shape_points[:, 0], shape_points[:, 1]] = 1.0

        if cutout is not None:
            cutout_coords = Path(cutout.get_verts()).contains_points(coordinates)
            cutout_points = coordinates[cutout_coords]
            out_array[cutout_points[:, 0], cutout_points[:, 1]] = 0.0

        return out_array

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
        """

        :param image_shape: [tuple(int)] Shape of the image output
        :param center: [tuple(int)] Center of the rectangle (coordinate)
        :param width: [int] Horizontal width of the rectangle (in pixels)
        :param height: [int] Vertical height of the rectangle (in pixels)
        :param angle: [float] Angle to rotate, in degrees
        :param line_width: [int] Width (in pixels)
        :param fill: [bool] to color in the center of the rectangle
        :return: Numpy array of size image_shape containing a rectangle
        """

        n_dim = len(image_shape)
        n_center_dim = len(center)
        if n_dim != n_center_dim:
            raise ValueError(
                f"Image shape input of length {n_dim}; but supplied center coordinates with dimension f{n_center_dim}"
            )

        width += line_width
        height += line_width

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

        if rectangle_array.ravel().sum() == 0.0:
            raise UserWarning("Image out of bounds, no shape displayed")

        return rectangle_array

    @staticmethod
    def create_regular_polygon(
        image_shape=(28, 28),
        center=(14, 14),
        angle=45,
        vertices=3,
        radius=10,
        line_width=2,
        fill=False,
    ):
        """
        Create a polygon with equal length sides

        :param image_shape: tuple[int] Size of the output image (pixels)
        :param center: tuple[int] Where to center the object
        :param angle: float Angle of rotation (degrees)
        :param vertices: int number of vertices (3=triangle, 4=square, etc)
        :param radius: int Distance from vertex to vertex
        :param line_width: int Width of lines (pixels)
        :param fill: bool Fill center of the object
        :return: Numpy array of shape image_shape containing the polygon
        """

        radius = abs(radius)

        n_dim = len(image_shape)
        n_center_dim = len(center)
        if n_dim != n_center_dim:
            raise ValueError(
                f"Image shape input of length {n_dim}; but supplied center coordinates with dimension f{n_center_dim}"
            )
        if vertices <= 0:
            raise ValueError(f"Cannot plot a polygon with {vertices}")

        xy = (center[0] - (radius / vertices) / 2, center[1] - (radius / vertices) / 2)
        polygon = patches.RegularPolygon(
            xy=xy, numVertices=vertices, radius=radius, orientation=angle
        )
        cutout = None
        if not fill:
            cutout_radius = radius - line_width
            xy_cutout = (
                center[0] - (cutout_radius / vertices) / 2,
                center[1] - (cutout_radius / vertices) / 2,
            )
            cutout = patches.RegularPolygon(
                xy=xy_cutout,
                numVertices=vertices,
                radius=cutout_radius,
                orientation=angle,
            )

        polygon_array = ShapeGenerator._convert_patch_to_image(
            polygon, image_shape=image_shape, cutout=cutout
        )

        if polygon_array.ravel().sum() == 0.0:
            raise UserWarning("Image out of bounds, no shape displayed")

        return polygon_array

    @staticmethod
    def create_arc():
        pass

    @staticmethod
    def create_line(image_shape=(28, 28), start=(0, 0), end=(28, 28), line_width=1):

        if len(start) != len(end):
            raise ValueError(
                f"Dimension mismatch, start point had dimensions of {len(start)}, but end point had dimensions of {len(end)}"
            )

        if start == end:
            raise ValueError(f"Start point and end point must be different")

        hyp = ((end[1] - start[1]) ** 2 + (end[0] - start[0]) ** 2) ** 0.5
        angle = np.arccos((end[0] - start[0]) / hyp)

        x_shift = line_width / 2.0 * np.cos(np.pi - angle)
        y_shift = line_width / 2.0 * np.sin(np.pi - angle)
        x_start, y_start = start[0] + x_shift, start[1] + y_shift
        x_end, y_end = end[0] + x_shift, end[1] + y_shift

        height_rect = line_width
        width_rect = ((y_end - y_start) ** 2 + (x_end - x_start) ** 2) ** 0.5

        angle_degrees = angle * 180.0 / np.pi
        line = patches.Rectangle(
            (x_start, y_start),
            width=width_rect,
            height=height_rect,
            angle=angle_degrees,
        )
        line_array = ShapeGenerator._convert_patch_to_image(
            line, image_shape=image_shape
        )
        return line_array

    @staticmethod
    def create_ellipse():
        pass

    @staticmethod
    def create_empty_shape(image_shape=(28, 28)):
        n_dim = len(image_shape)
        image_shape = tuple(map(lambda dim: int(np.ceil(dim)), image_shape))

        if n_dim < 2:
            raise ValueError(
                f"Image shape input of length {n_dim}; but input must be length >=2"
            )

        if 0 in image_shape:
            raise ValueError(f"Image size must be greater than 0")

        return np.zeros(image_shape)

    # TODO Define the types of noise allowed
    # TODO Write method to apply noise
