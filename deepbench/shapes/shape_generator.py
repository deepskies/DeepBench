import numpy as np
from matplotlib.path import Path
from matplotlib import patches
from skimage import transform


class ShapeGenerator:
    def __init__(self, image_shape=(28, 28)):
        self.image_shape = image_shape
        self.n_dimensions = len(self.image_shape)

    def resize(self, image, resize_dimensions=(28, 28)):
        """
        Resize a numpy array
        :param image: Numpy array to resize
        :param resize_dimensions: tuple(*int) Dimensions to reshape the image to
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

    def _convert_patch_to_image(self, image, cutout=None):
        """
        Converts a matplot path or patch object into a numpy array of the designated size
        :param image: Matplotlib image object to convert
        :param image_shape: [tuple(*int)] Size of the desired image
        :return: numpy array of shape image_shape, containing the image
        """
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
        center=(14, 14),
        width=10,
        height=10,
        angle=0,
        line_width=1,
        fill=False,
    ):
        """
        :param image_shape: [tuple(*int)] Shape of the image output
        :param center: [tuple(*int)] Center of the rectangle (coordinate)
        :param width: [int] Horizontal width of the rectangle (in pixels)
        :param height: [int] Vertical height of the rectangle (in pixels)
        :param angle: [float] Angle to rotate, in degrees
        :param line_width: [int] Width (in pixels)
        :param fill: [bool] to color in the center of the rectangle
        :return: Numpy array of size image_shape containing a rectangle
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

        if rectangle_array.ravel().sum() == 0.0:
            raise UserWarning("Image out of bounds, no shape displayed")

        return rectangle_array

    def create_regular_polygon(
        self,
        center=(14, 14),
        angle=45,
        vertices=3,
        radius=10,
        line_width=2,
        fill=False,
    ):
        """
        Create a polygon with equal length sides
        :param image_shape: tuple[*int] Size of the output image (pixels)
        :param center: tuple[*int] Where to center the object
        :param angle: float Angle of rotation (degrees)
        :param vertices: int number of vertices (3=triangle, 4=square, etc)
        :param radius: int Distance from vertex to vertex
        :param line_width: int Width of lines (pixels)
        :param fill: bool Fill center of the object
        :return: Numpy array of shape image_shape containing the polygon
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

        if polygon_array.ravel().sum() == 0.0:
            raise UserWarning("Image out of bounds, no shape displayed")

        return polygon_array

    def create_arc(
        self,
        center=(14, 14),
        radius=10,
        theta1=0,
        theta2=90,
        line_width=1,
    ):
        """
        Create an arc with radius "radius" arcing from theta1 to theta2
        :param image_shape: Shape of the output array (pixels)
        :param center: tuple[*int]Center point of the arc
        :param radius: int distance from the arc to the center point
        :param theta1: float starting point of the arc (degrees)
        :param theta2: float ending point of the arc (degrees)
        :param line_width: int thickness of the arc (pixels)
        :return: Numpy array of the arc
        """

        arc = patches.Wedge(
            center=center, r=radius, theta1=theta1, theta2=theta2, width=line_width
        )
        arc_array = self._convert_patch_to_image(arc)

        if arc_array.ravel().sum() == 0.0:
            raise UserWarning("Image out of bounds, no shape displayed")

        return arc_array

    def create_line(self, start=(0, 0), end=(28, 28), line_width=1):
        """
        Generate a numpy array of a line
        :param image_shape:  tuple(*int) Shape of the output arrray (pixels)
        :param start: tuple(*int) Starting corner of the line
        :param end: tuple(*int) Ending corner of the line
        :param line_width: int Thickness of the line (pixels)
        :return: Numpy array containing the line
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

        if line_array.ravel().sum() == 0.0:
            raise UserWarning("Image out of bounds, no shape displayed")

        return line_array

    def create_ellipse(
        self,
        center=(14, 14),
        width=10,
        height=10,
        angle=0,
        line_width=1,
        fill=False,
    ):
        """
        :param image_shape: tuple(*int) Shape of the output arrray (pixels)
        :param center: tuple(*int) Center point of the ellipse
        :param width: int Horizontal length of the ellipse (pixels)
        :param height: int Vertical height of the ellipse (pixels)
        :param angle: float Rotation angle of the ellipse (degrees)
        :param line_width: int Width of the ellipse's border (pixels)
        :param fill: bool Fill the center of the ellipse
        :return: Numpy array containing the ellipse
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

        if ellipse_array.ravel().sum() == 0.0:
            raise UserWarning("Image out of bounds, no shape displayed")

        return ellipse_array

    def create_empty_shape(self):

        if self.n_dimensions < 2:
            raise ValueError(
                f"Image shape input of length {self.n_dimensions}; but input must be length >=2"
            )

        if 0 in self.image_shape:
            raise ValueError(f"Image size must be greater than 0")

        return np.zeros(self.image_shape)
