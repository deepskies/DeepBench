from typing import Union
import numpy as np
from matplotlib.path import Path
from matplotlib import patches
from skimage import transform


class ShapeGenerator:
    def __init__(self, image_shape: tuple = (28, 28)):
        self.image_shape = image_shape
        self.n_dimensions = len(self.image_shape)

    def resize(self, image: np.ndarray, resize_dimensions: tuple = (28, 28)):
        """
        Resize an array-like

        Args:
            image (np.ndarray): shape to resize
            resize_dimensions (tuple, optional): resize to shape. Defaults to (28, 28).

        Raises:
            ValueError: invalid size, either too small (0,0) or having the number of incorrect dimensions

        Returns:
            np.ndarray: array of size (resize_dimensions)
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

    def _convert_patch_to_image(
        self, image: patches.Patch, cutout: patches.Path = None
    ):

        n_dim = len(self.image_shape)
        self.image_shape = tuple(map(lambda dim: int(np.ceil(dim)), self.image_shape))

        if n_dim < 2:
            raise ValueError(
                f"Image shape input of length {n_dim}; but input must be length >=2"
            )

        if 0 in self.image_shape:
            raise ValueError(f"Image size must be greater than 0")

        x = np.arange(0, self.image_shape[0])
        y = np.arange(0, self.image_shape[1])
        meshgrid = np.meshgrid(x, y)

        coordinates = np.array(list(zip(*(c.flat for c in meshgrid))))

        valid_coordinates = Path(image.get_verts()).contains_points(coordinates)
        shape_points = coordinates[valid_coordinates]

        out_array = np.zeros(self.image_shape)
        out_array[shape_points[:, 0], shape_points[:, 1]] = 1.0

        if cutout is not None:
            cutout_coords = Path(cutout.get_verts()).contains_points(coordinates)
            cutout_points = coordinates[cutout_coords]
            out_array[cutout_points[:, 0], cutout_points[:, 1]] = 0.0

        return out_array

    def create_rectangle(
        self,
        center: tuple = (np.random.randint(10, 16), np.random.randint(10, 16)),
        width: int = np.random.randint(10, 16),
        height: int = np.random.randint(10, 16),
        angle: Union[float, int] = 0,
        line_width: int = 1,
        fill: bool = False,
    ):

        """
        Make a rectangle.

        Args:
            center (tuple(*int), optional): Center of the rectangle (coordinate). Defaults to (14, 14).
            width (int, optional): Horizontal width of the rectangle (in pixels). Defaults to random int.
            height (int, optional): Vertical height of the rectangle (in pixels). Defaults to random int.
            angle (Union[float, int], optional): tilt the rectangle (degrees). Defaults to 0.
            line_width (int, optional): line width of the outline. Defaults to 1.
            fill (bool, optional): Fill in the rectangle. Defaults to False.


        Returns:
           np.ndarray: A Rectangle image
        """

        n_center_dim = len(center)
        if self.n_dimensions != n_center_dim:
            raise ValueError(
                f"Image shape input of length {self.n_dimensions}; but supplied center coordinates with dimension f{n_center_dim}"
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

        rectangle_array = self._convert_patch_to_image(rectangle, cutout=cutout)

        return rectangle_array

    def create_regular_polygon(
        self,
        center: tuple = (np.random.randint(10, 16), np.random.randint(10, 16)),
        angle: Union[int, float] = np.random.uniform(20, 90),
        vertices: int = 3,
        radius: Union[int, float] = np.random.uniform(8, 12),
        line_width=1,
        fill=False,
    ):
        """
        Create a polygon with equal length sides

        Args:
            center (tuple[*int], optional): Where to center the object.
            angle (Union[int, float], optional): Angle of rotation (degrees)
            vertices (int, optional): Number of verticies. Defaults to 3, a triangle.
            radius (int, optional): distance from vertex to vertex Defaults to 10.
            line_width (int, optional): line width of the outline. Defaults to 1.
            fill (bool, optional): Fill in the rectangle. Defaults to False.


        Returns:
           np.ndarray: A polygon image
        """

        radius = abs(radius)

        n_center_dim = len(center)
        if self.n_dimensions != n_center_dim:
            raise ValueError(
                f"Image shape input of length {n_center_dim}; but supplied center coordinates with dimension f{n_center_dim}"
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

        polygon_array = self._convert_patch_to_image(polygon, cutout=cutout)

        return polygon_array

    def create_arc(
        self,
        center: tuple = (np.random.randint(10, 16), np.random.randint(10, 16)),
        radius: Union[int, float] = np.random.uniform(8, 12),
        theta1: Union[int, float] = np.random.uniform(0, 45),
        theta2: Union[int, float] = np.random.uniform(85, 120),
        line_width: int = 1,
    ):
        """
        Create an arc with radius "radius" arcing from theta1 to theta2 counter-clockwise

        Args:
            center (tuple, optional): Center point of the arc. Defaults to (np.random.randint(10, 16), np.random.randint(10, 16)).
            radius (Union[int, float], optional): distance from the arc to the center point. Defaults to np.random.random(8, 12).
            theta1 (Union[int, float], optional): starting point of the arc (degrees). Defaults to np.random.random(0, 45).
            theta2 (Union[int, float], optional): ending point of the arc (degrees). Defaults to np.random.random(85, 120).
            line_width (int, optional):  thickness of the arc (pixels) Defaults to 1.


        Returns:
            np.ndarray: The arc image
        """

        arc = patches.Wedge(
            center=center, r=radius, theta1=theta1, theta2=theta2, width=line_width
        )
        arc_array = self._convert_patch_to_image(arc)

        return arc_array

    def create_line(
        self,
        start: tuple = (np.random.randint(0, 10), np.random.randint(0, 10)),
        end: tuple = (np.random.randint(12, 28), np.random.randint(12, 28)),
        line_width: int = 1,
    ):

        """
        Generate a numpy array of a line

        Args:
            start (tuple, optional): Starting corner of the line. Defaults to (np.random.randint(0, 10), np.random.randint(0, 10)).
            end (tuple, optional): Ending corner of the line. Defaults to (np.random.randint(12, 28), np.random.randint(12, 28)).
            line_width (int, optional): Thickness of the line (pixels). Defaults to 1.

        Returns:
            np.ndarray
        """

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
        line_array = self._convert_patch_to_image(line)

        return line_array

    def create_ellipse(
        self,
        center: tuple = (np.random.randint(10, 16), np.random.randint(10, 16)),
        width: int = np.random.randint(10, 16),
        height: int = np.random.randint(10, 16),
        angle: Union[float, int] = 0,
        line_width: int = 1,
        fill: bool = False,
    ):
        """
        Create an ellipse/circle (where width/height are the same)

        Args:
            center (tuple, optional): Center point of the ellipse. Defaults to (np.random.randint(10, 16), np.random.randint(10, 16)).
            width (int, optional): Horizontal length of the ellipse (pixels). Defaults to np.random.randint(10, 16).
            height (int, optional): Vertical height of the ellipse (pixels). Defaults to np.random.randint(10, 16).
            angle (Union[float, int], optional):  Rotation angle of the ellipse (degrees). Defaults to 0.
            line_width (int, optional):  Width of the ellipse's border (pixels). Defaults to 1.
            fill (bool, optional): Fill the center of the ellipse. Defaults to False.


        Returns:
           np.ndarray

        """

        if self.n_dimensions != len(center):
            raise ValueError(
                f"Dimension mismatch, image had dimensions of {self.n_dimensions}, "
                f"but center point had dimensions of {len(center)}"
            )

        height, width = int(np.ceil(height)), int(np.ceil(width))

        ellipse = patches.Ellipse(xy=center, width=width, height=height, angle=angle)

        cutout = None
        if not fill:
            xy_cutout = center
            width_cutout = width - (2 * line_width) if width != 0 else 0
            height_cutout = height - (2 * line_width) if height != 0 else 0

            cutout = patches.Ellipse(
                xy=xy_cutout, width=width_cutout, height=height_cutout, angle=angle
            )

        ellipse_array = self._convert_patch_to_image(ellipse, cutout=cutout)

        return ellipse_array

    def create_empty_shape(self):
        """
        Create an array of 0s with shape self.image_shape

        Returns:
            np.ndarray
        """
        if self.n_dimensions < 2:
            raise ValueError(
                f"Image shape input of length {self.n_dimensions}; but input must be length >=2"
            )

        if 0 in self.image_shape:
            raise ValueError(f"Image size must be greater than 0")

        return np.zeros(self.image_shape)
