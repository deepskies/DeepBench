from unittest import TestCase
from src.deepbench.shape_generator import ShapeGenerator

import numpy as np
import matplotlib.patches as patch


class TestShapeGenerator(TestCase):
    def test_patch_conversion_defaults(self):
        # simple patch object. Convert to a numpy array
        simple_patch = patch.Rectangle(xy=(0, 0), width=1, height=1)
        converted_object = ShapeGenerator._convert_patch_to_image(image=simple_patch)
        expected_obj_type = np.array([0, 0])
        self.assertEqual(type(converted_object), type(expected_obj_type))

    def test_patch_conversion_default_dimensions(self):
        simple_patch = patch.Rectangle(xy=(0, 0), width=1, height=1)
        converted_object = ShapeGenerator._convert_patch_to_image(image=simple_patch)
        converted_object_shape_x, converted_object_shape_y = converted_object.shape
        expected_x_dim, expected_y_dim = 28, 28

        self.assertEqual(converted_object_shape_x, expected_x_dim)
        self.assertEqual(converted_object_shape_y, expected_y_dim)

    def test_patch_conversion_single_image_dimension(self):
        with self.assertRaises(ValueError):
            simple_patch = patch.Rectangle(xy=(0, 0), width=1, height=1)
            ShapeGenerator._convert_patch_to_image(
                image=simple_patch, image_shape=tuple([28])
            )

    def test_patch_conversion_N_dimension(self):
        simple_patch = patch.Rectangle(xy=(0, 0), width=1, height=1)
        converted_object = ShapeGenerator._convert_patch_to_image(
            image=simple_patch, image_shape=(28, 28, 28)
        )
        (
            converted_object_shape_x,
            converted_object_shape_y,
            converted_object_shape_z,
        ) = converted_object.shape
        expected_x_dim, expected_y_dim, expected_z_dim = 28, 28, 28

        self.assertEqual(converted_object_shape_x, expected_x_dim)
        self.assertEqual(converted_object_shape_y, expected_y_dim)
        self.assertEqual(converted_object_shape_z, expected_z_dim)

    def test_patch_conversion_size_0(self):
        with self.assertRaises(ValueError):
            simple_patch = patch.Rectangle(xy=(0, 0), width=1, height=1)
            ShapeGenerator._convert_patch_to_image(
                image=simple_patch, image_shape=(0, 0)
            )

    def test_patch_conversion_non_int_size(self):
        simple_patch = patch.Rectangle(xy=(0, 0), width=1, height=1)
        converted_object = ShapeGenerator._convert_patch_to_image(
            image=simple_patch, image_shape=(55.5, 55.5)
        )
        converted_object_shape_x, converted_object_shape_y = converted_object.shape
        expected_x_dim, expected_y_dim = 56, 56

        self.assertEqual(converted_object_shape_x, expected_x_dim)
        self.assertEqual(converted_object_shape_y, expected_y_dim)

    def test_patch_conversion_non_int_size_round(self):
        simple_patch = patch.Rectangle(xy=(0, 0), width=1, height=1)
        converted_object = ShapeGenerator._convert_patch_to_image(
            image=simple_patch, image_shape=(55.1, 55.6)
        )
        converted_object_shape_x, converted_object_shape_y = converted_object.shape
        expected_x_dim, expected_y_dim = 56, 56

        self.assertEqual(converted_object_shape_x, expected_x_dim)
        self.assertEqual(converted_object_shape_y, expected_y_dim)

    def test_resize_default(self):
        simple_image = np.zeros((32, 32))
        resized_image = ShapeGenerator.resize(image=simple_image)
        resized_image_x, resized_image_y = resized_image.shape
        default_new_size_x, default_new_size_y = 28, 28

        self.assertEqual(resized_image_x, default_new_size_x)
        self.assertEqual(resized_image_y, default_new_size_y)

    def test_resize_dim_mismatch(self):
        with self.assertRaises(ValueError):
            simple_image = np.zeros((32, 32))
            resize_dimensions = (1, 1, 1)
            ShapeGenerator.resize(
                image=simple_image, resize_dimensions=resize_dimensions
            )

    def test_resize_zero_size_source(self):
        with self.assertRaises(ValueError):
            simple_image = np.zeros((0, 0))
            resize_dimensions = (1, 1)
            ShapeGenerator.resize(
                image=simple_image, resize_dimensions=resize_dimensions
            )

    def test_resize_zero_size_target(self):
        with self.assertRaises(ValueError):
            simple_image = np.zeros((1, 1))
            resize_dimensions = (0, 0)
            ShapeGenerator.resize(
                image=simple_image, resize_dimensions=resize_dimensions
            )

    def test_resize_upscale(self):
        simple_image = np.zeros((32, 32))
        resize = (50, 50)
        resized_image = ShapeGenerator.resize(
            image=simple_image, resize_dimensions=resize
        )
        resized_image_x, resized_image_y = resized_image.shape
        new_size_x, new_size_y = resize

        self.assertEqual(resized_image_x, new_size_x)
        self.assertEqual(resized_image_y, new_size_y)

    def test_resize_downscale(self):
        simple_image = np.zeros((80, 80))
        resize = (50, 50)
        resized_image = ShapeGenerator.resize(
            image=simple_image, resize_dimensions=resize
        )
        resized_image_x, resized_image_y = resized_image.shape
        new_size_x, new_size_y = resize

        self.assertEqual(resized_image_x, new_size_x)
        self.assertEqual(resized_image_y, new_size_y)

    def test_resize_non_int(self):
        simple_image = np.zeros((80, 80))
        resize = (49.1, 49.6)
        resized_image = ShapeGenerator.resize(
            image=simple_image, resize_dimensions=resize
        )
        resized_image_x, resized_image_y = resized_image.shape
        new_size_x, new_size_y = (50, 50)

        self.assertEqual(resized_image_x, new_size_x)
        self.assertEqual(resized_image_y, new_size_y)

    def test_resize_negative(self):
        with self.assertRaises(ValueError):
            simple_image = np.zeros((80, 80))
            resize = (-1, -1)
            ShapeGenerator.resize(image=simple_image, resize_dimensions=resize)

    def test_rectangle_default(self):
        rectangle = ShapeGenerator.create_rectangle()

        x, y = rectangle.shape
        expected_x, expected_y = (28, 28)
        self.assertEqual(x, expected_x)
        self.assertEqual(y, expected_y)

        # Each corner should have a black pixel
        self.assertEqual(1.0, rectangle[9, 10], "corner 1 failed")
        self.assertEqual(1.0, rectangle[19, 19], "corner 4 failed")

        # Center needs to be white (default is unfilled)
        self.assertEqual(0.0, rectangle[14, 14], "Center Filled")

    def test_rectangle_size_center_dim_mismatch(self):
        with self.assertRaises(ValueError):
            ShapeGenerator.create_rectangle(center=(1, 1, 1))

    def test_rectangle_xy_out_of_range(self):
        with self.assertRaises(UserWarning):
            rectangle = ShapeGenerator.create_rectangle(
                image_shape=(10, 10), center=(100, 100)
            )

            rectangle_contents = rectangle.sum().sum()
            self.assertEqual(0, rectangle_contents)

    def test_rectangle_angle_in_bounds_no_change(self):
        angle = 90
        rectangle_rotated = ShapeGenerator.create_rectangle(angle=angle)

        rectangle_non_rotated = ShapeGenerator.create_rectangle(angle=0)

        # But it's a square so it looks the same
        self.assertEqual(rectangle_rotated.all(), rectangle_non_rotated.all())

    def test_rectangle_angle_in_bounds_change(self):
        angle = 360
        rectangle = ShapeGenerator.create_rectangle(width=10, height=10, angle=angle)

        # Each corner should have a black pixel
        self.assertEqual(1.0, rectangle[9, 10], "corner 1 failed")
        self.assertEqual(1.0, rectangle[19, 19], "corner 4 failed")

        # Center needs to be white (default is unfilled)
        self.assertEqual(0.0, rectangle[14, 14], "Center Filled")

    # TODO Test to check odd n on width and height
    # TODO Checks on line width validity

    def test_rectangle_angle_oob_positive(self):
        angle = 45
        rectangle_rotated = ShapeGenerator.create_rectangle(angle=angle + 360)
        rectangle_non_rotated = ShapeGenerator.create_rectangle(angle=angle)

        self.assertEqual(rectangle_rotated.all(), rectangle_non_rotated.all())

    def test_rectangle_angle_oob_negative(self):
        angle = 45
        rectangle_rotated = ShapeGenerator.create_rectangle(angle=angle - 360)
        rectangle_non_rotated = ShapeGenerator.create_rectangle(angle=angle)

        self.assertEqual(rectangle_rotated.all(), rectangle_non_rotated.all())

    def test_rectangle_fill(self):
        # This should fill the whole screen.
        rectangle = ShapeGenerator.create_rectangle(width=80, height=80, fill=True)
        ideal_rectangle = np.ones((28, 28))

        self.assertEqual(ideal_rectangle.all(), rectangle.all())

    def test_polygon_default(self):
        triangle = ShapeGenerator.create_regular_polygon()

        shape_x, shape_y = triangle.shape
        expected_x, expected_y = 28, 28

        self.assertEqual(shape_x, expected_x)
        self.assertEqual(shape_y, expected_y)

        # Center should be white
        self.assertEqual(0.0, triangle[14, 14])

        # top point should be black
        self.assertEqual(1.0, triangle[21, 17])

        # TODO the trig to check the other points here

    def test_polygon_size_center_mismatch(self):
        with self.assertRaises(ValueError):
            ShapeGenerator.create_regular_polygon(center=(14, 14, 14))

    def test_polygon_oob_xy(self):
        with self.assertRaises(UserWarning):
            triangle = ShapeGenerator.create_regular_polygon(
                image_shape=(10, 10), center=(100, 100)
            )

            contents = triangle.sum().sum()
            self.assertEqual(0.0, contents)

    def test_polygon_positive_oob_angle(self):
        angle = 45
        triangle_rotated = ShapeGenerator.create_regular_polygon(angle=angle + 360)
        triangle_non_rotated = ShapeGenerator.create_regular_polygon(angle=angle)

        self.assertEqual(triangle_rotated.all(), triangle_non_rotated.all())

    def test_polygon_negative_oob_angle(self):
        angle = 45
        triangle_rotated = ShapeGenerator.create_regular_polygon(angle=angle - 360)
        triangle_non_rotated = ShapeGenerator.create_regular_polygon(angle=angle)

        self.assertEqual(triangle_rotated.all(), triangle_non_rotated.all())

    def test_polygon_negative_radius(self):
        triangle = ShapeGenerator.create_regular_polygon(radius=-10)
        self.assertRaises(UserWarning)

        # Center should be white
        self.assertEqual(0.0, triangle[14, 14])

        # top point should be black
        # The radius will just be abs
        self.assertEqual(1.0, triangle[21, 17])

    def test_polygon_negative_vertices(self):
        with self.assertRaises(ValueError):
            ShapeGenerator.create_regular_polygon(vertices=-3)

    def test_arc_default(self):
        arc = ShapeGenerator.create_arc()

        x, y = arc.shape
        expected_x, expected_y = (28, 28)
        self.assertEqual(x, expected_x)
        self.assertEqual(y, expected_y)

        self.assertEqual(0.0, arc[14, 14], "Empty Center")
        self.assertEqual(1.0, arc[14, 24], "Bottom Point")
        self.assertEqual(1.0, arc[23, 15], "Starting Point")

    def test_arc_size_center_dim_mismatch(self):
        with self.assertRaises(ValueError):
            ShapeGenerator.create_arc(center=(0, 0, 0))

    def test_arc_oob_center(self):
        with self.assertRaises(UserWarning):
            triangle = ShapeGenerator.create_arc(center=(100, 100))

            contents = triangle.sum().sum()
            self.assertEqual(0.0, contents)

    def test_arc_oob_negative_theta1(self):
        angle = 45
        arc_rotated = ShapeGenerator.create_arc(theta1=angle - 360)
        arc_non_rotated = ShapeGenerator.create_arc(theta1=angle)

        self.assertEqual(arc_rotated.all(), arc_non_rotated.all())

    def test_arc_oob_positive_theta1(self):
        angle = 45
        arc_rotated = ShapeGenerator.create_arc(theta1=angle + 360)
        arc_non_rotated = ShapeGenerator.create_arc(theta1=angle)

        self.assertEqual(arc_rotated.all(), arc_non_rotated.all())

    def test_arc_oob_negative_theta2(self):
        angle = 45
        arc_rotated = ShapeGenerator.create_arc(theta2=angle - 360)
        arc_non_rotated = ShapeGenerator.create_arc(theta2=angle)

        self.assertEqual(arc_rotated.all(), arc_non_rotated.all())

    def test_arc_oob_positive_theta2(self):
        angle = 45
        arc_rotated = ShapeGenerator.create_arc(theta2=angle + 360)
        arc_non_rotated = ShapeGenerator.create_arc(theta2=angle)

        self.assertEqual(arc_rotated.all(), arc_non_rotated.all())

    def test_arc_theta2_less_than_theta1(self):

        arc_negative_sweep = ShapeGenerator.create_arc(theta1=90, theta2=0)
        arc_positive_sweep = ShapeGenerator.create_arc(theta1=0, theta2=90)

        self.assertEqual(arc_negative_sweep.all(), arc_positive_sweep.all())

    def test_arc_oob_width(self):
        arc = ShapeGenerator.create_arc(
            image_shape=(14, 14), radius=28, line_width=100, theta1=0, theta2=360
        )

        size = arc.size
        n_black_pixels = int(arc.sum().sum())
        self.assertEqual(size, n_black_pixels)

    def test_line_defaults(self):
        line = ShapeGenerator.create_line()

        x, y = line.shape
        expected_x, expected_y = (28, 28)
        self.assertEqual(x, expected_x)
        self.assertEqual(y, expected_y)

        # Bottom left top right are black. Opposite are white
        self.assertEqual(1.0, line[1, 2], "line start incorrect")
        self.assertEqual(1.0, line[26, 27], "line end incorrect")

        self.assertEqual(0.0, line[1, 27], "line corner incorrect")
        self.assertEqual(0.0, line[27, 1], "line corner incorrect")

    def test_line_size_start_dim_mismatch(self):
        with self.assertRaises(ValueError):
            ShapeGenerator.create_line(start=(0, 0, 0))

    def test_line_size_end_dim_mismatch(self):
        with self.assertRaises(ValueError):
            ShapeGenerator.create_line(end=(0, 0, 0))

    def test_line_start_oob(self):
        line = ShapeGenerator.create_line(start=(-200, -100))

        # Bottom left top right are black. Opposite are white
        self.assertEqual(1.0, line[1, 14])
        self.assertEqual(1.0, line[25, 27])

    def test_line_end_oob(self):
        line = ShapeGenerator.create_line(end=(200, 100))
        self.assertRaises(UserWarning)

        self.assertEqual(1.0, line[1, 1], "line start incorrect")
        self.assertEqual(1.0, line[27, 14], "line end incorrect")

    def test_line_same_start_end(self):
        with self.assertRaises(ValueError):
            ShapeGenerator.create_line(end=(0, 0))

    def test_ellipse_default(self):
        circle = ShapeGenerator.create_ellipse()

        shape_x, shape_y = circle.shape
        expected_x, expected_y = 28, 28

        self.assertEqual(shape_x, expected_x)
        self.assertEqual(shape_y, expected_y)

        # Center should be white
        self.assertEqual(0.0, circle[14, 14])

        # Default is a circle
        self.assertEqual(1.0, circle[11, 10])
        self.assertEqual(1.0, circle[14, 19])
        self.assertEqual(1.0, circle[19, 14])
        self.assertEqual(1.0, circle[9, 14])

    def test_ellipse_size_xy_mismatch(self):
        with self.assertRaises(ValueError):
            ShapeGenerator.create_ellipse(center=(14, 14, 14))

    def test_ellipse_0_radius(self):
        ## Nothing is displayed
        with self.assertRaises(UserWarning):
            ShapeGenerator.create_ellipse(width=0, height=0)

    def test_ellipse_non_int_radius(self):
        # Just round up
        circle = ShapeGenerator.create_ellipse(height=9.4)

        # Center should be white
        self.assertEqual(0.0, circle[14, 14])

        # top and bottom points should be black
        self.assertEqual(1.0, circle[14, 19])
        self.assertEqual(1.0, circle[19, 14])

    def test_ellipse_oob_center(self):
        with self.assertRaises(UserWarning):
            circle = ShapeGenerator.create_ellipse(
                image_shape=(10, 10), center=(100, 100)
            )
            contents = circle.sum().sum()
            self.assertEqual(0.0, contents)

    def test_ellipse_non_int_width(self):
        # Just round up
        circle = ShapeGenerator.create_ellipse(width=9.4)

        # Center should be white
        self.assertEqual(0.0, circle[14, 14])

        # top and bottom points should be black
        self.assertEqual(1.0, circle[14, 19])
        self.assertEqual(1.0, circle[19, 14])
