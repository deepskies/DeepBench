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

    def test_rectangle_single_dim_xy(self):
        with self.assertRaises(ValueError):
            ShapeGenerator.create_rectangle(center=1)

    def test_rectangle_size_center_dim_mismatch(self):
        with self.assertRaises(ValueError):
            ShapeGenerator.create_rectangle(center=1)

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
        self.assertEqual(rectangle_rotated, rectangle_non_rotated)

    def test_rectangle_angle_in_bounds_change(self):
        angle = 90
        rectangle = ShapeGenerator.create_rectangle(width=6, height=10, angle=angle)

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

        self.assertEqual(rectangle_rotated, rectangle_non_rotated)

    def test_rectangle_angle_oob_negative(self):
        angle = 45
        rectangle_rotated = ShapeGenerator.create_rectangle(angle=angle - 360)
        rectangle_non_rotated = ShapeGenerator.create_rectangle(angle=angle)

        self.assertEqual(rectangle_rotated, rectangle_non_rotated)

    def test_rectangle_fill(self):
        # This should fill the whole screen.
        rectangle = ShapeGenerator.create_rectangle(width=28, height=28, fill=True)
        rectangle_sum = rectangle.sum().sum()
        rectangle_size = rectangle.size

        self.assertEqual(rectangle_size, rectangle_sum)

    def test_polygon_default(self):
        triangle = ShapeGenerator.create_regular_polygon()

        shape_x, shape_y = triangle.shape
        expected_x, expected_y = 28, 28

        self.assertEqual(shape_x, expected_x)
        self.assertEqual(shape_y, expected_y)

        # Center should be white
        self.assertEqual(0.0, triangle[14, 14])

        # top point should be black
        self.assertEqual(1.0, triangle[14, 21])

        # TODO the trig to check the other points here

    def test_polygon_size_center_mismatch(self):
        with self.assertRaises(ValueError):
            ShapeGenerator.create_regular_polygon(xy=(14, 14, 14))

    def test_polygon_oob_xy(self):
        with self.assertRaises(UserWarning):
            triangle = ShapeGenerator.create_rectangle(
                image_shape=(10, 10), xy=(100, 100)
            )

        contents = triangle.sum().sum()
        self.assertEqual(0.0, contents)

    def test_polygon_positive_oob_angle(self):
        angle = 45
        triangle_rotated = ShapeGenerator.create_regular_polygon(angle=angle + 360)
        triangle_non_rotated = ShapeGenerator.create_regular_polygon(angle=angle)

        self.assertEqual(triangle_rotated, triangle_non_rotated)

    def test_polygon_negative_oob_angle(self):
        angle = 45
        triangle_rotated = ShapeGenerator.create_regular_polygon(angle=angle - 360)
        triangle_non_rotated = ShapeGenerator.create_regular_polygon(angle=angle)

        self.assertEqual(triangle_rotated, triangle_non_rotated)

    def test_negative_radius(self):
        triangle = ShapeGenerator.create_regular_polygon(radius=-5)
        self.assertRaises(UserWarning)

        # Center should be white
        self.assertEqual(0.0, triangle[14, 14])

        # top point should be black
        # The radius will just be abs
        self.assertEqual(1.0, triangle[14, 21])

    def test_negative_vertices(self):
        ShapeGenerator.create_regular_polygon(vertices=-3)
        self.assertRaises(ValueError)

    def test_arc_default(self):
        arc = ShapeGenerator.create_arc()

        x, y = arc.shape
        expected_x, expected_y = (28, 28)
        self.assertEqual(x, expected_x)
        self.assertEqual(y, expected_y)

        # TODO set defaults on theta1 and theta2. And then math

    def test_arc_size_center_dim_mismatch(self):
        ShapeGenerator.create_arc(center=(0, 0, 0))
        self.assertRaises(ValueError)

    def test_arc_oob_center(self):
        triangle = ShapeGenerator.create_arc(center=(100, 100))
        self.assertRaises(UserWarning)

        contents = triangle.sum().sum()
        self.assertEqual(0.0, contents)

    def test_arc_oob_negative_theta1(self):
        angle = 45
        arc_rotated = ShapeGenerator.create_arc(theta1=angle - 360)
        arc_non_rotated = ShapeGenerator.create_arc(theta1=angle)

        self.assertEqual(arc_rotated, arc_non_rotated)

    def test_arc_oob_positive_theta1(self):
        angle = 45
        arc_rotated = ShapeGenerator.create_arc(theta1=angle + 360)
        arc_non_rotated = ShapeGenerator.create_arc(theta1=angle)

        self.assertEqual(arc_rotated, arc_non_rotated)

    def test_arc_oob_negative_theta2(self):
        angle = 45
        arc_rotated = ShapeGenerator.create_arc(theta2=angle - 360)
        arc_non_rotated = ShapeGenerator.create_arc(theta2=angle)

        self.assertEqual(arc_rotated, arc_non_rotated)

    def test_arc_oob_positive_theta2(self):
        angle = 45
        arc_rotated = ShapeGenerator.create_arc(theta2=angle + 360)
        arc_non_rotated = ShapeGenerator.create_arc(theta2=angle)

        self.assertEqual(arc_rotated, arc_non_rotated)

    def test_arc_oob_width(self):
        arc = ShapeGenerator.create_arc(width=100)

        size = arc.size
        n_black_pixels = arc.sum().sum()
        self.assertEqual(size, n_black_pixels)

    def test_line_defaults(self):
        line = ShapeGenerator.create_line()

        x, y = line.shape
        expected_x, expected_y = (28, 28)
        self.assertEqual(x, expected_x)
        self.assertEqual(y, expected_y)

        # Bottom left top right are black. Opposite are white
        self.assertEqual(1.0, line[0, 0])
        self.assertEqual(1.0, line[28, 28])

        self.assertEqual(0.0, line[0, 28])
        self.assertEqual(0.0, line[28, 0])

    def test_line_size_start_dim_mismatch(self):
        ShapeGenerator.create_line(start=(0, 0, 0))
        self.assertRaises(ValueError)

    def test_line_size_end_dim_mismatch(self):
        ShapeGenerator.create_line(end=(0, 0, 0))
        self.assertRaises(ValueError)

    def test_line_start_oob(self):
        line = ShapeGenerator.create_line(start=(-200, -100))

        # Bottom left top right are black. Opposite are white
        self.assertEqual(1.0, line[14, 0])
        self.assertEqual(1.0, line[28, 28])

    def test_line_end_oob(self):
        line = ShapeGenerator.create_line(end=(200, 100))
        self.assertRaises(UserWarning)

        self.assertEqual(1.0, line[0, 0])
        self.assertEqual(1.0, line[14, 28])

    def test_line_same_start_end(self):
        line = ShapeGenerator.create_line(end=(0, 0))

        self.assertEqual(1.0, line[0, 0])
        self.assertEqual(1.0, line.sum().sum())

    def test_line_max_width(self):
        line = ShapeGenerator.create_line(width=100)

        size = line.size
        n_black_pixels = line.sum().sum()
        self.assertEqual(size, n_black_pixels)

    def test_ellipse_default(self):
        circle = ShapeGenerator.create_ellipse()

        shape_x, shape_y = circle.shape
        expected_x, expected_y = 28, 28

        self.assertEqual(shape_x, expected_x)
        self.assertEqual(shape_y, expected_y)

        # Center should be white
        self.assertEqual(0.0, circle[14, 14])

        # top and bottom points should be black
        self.assertEqual(1.0, circle[21, 21])
        self.assertEqual(1.0, circle[9, 9])

    def test_ellipse_single_dim_xy(self):
        ShapeGenerator.create_ellipse(xy=1)
        self.assertRaises(ValueError)

    def test_ellipse_size_xy_mismatch(self):
        ShapeGenerator.create_ellipse(xy=(14, 14, 14))
        self.assertRaises(ValueError)

    def test_ellipse_0_radius(self):
        circle = ShapeGenerator.create_ellipse(radius=0)
        # Should just make a dot
        self.assertEqual(1.0, circle.sum().sum())

    def test_ellipse_0_width(self):
        circle = ShapeGenerator.create_ellipse(width=0)
        # Should just make a circle

        self.assertEqual(1.0, circle[21, 21])
        self.assertEqual(1.0, circle[9, 9])
        self.assertEqual(1.0, circle[21, 14])
        self.assertEqual(1.0, circle[9, 14])

    def test_ellipse_non_int_radius(self):
        # Just round up
        circle = ShapeGenerator.create_ellipse(radius=4.4)

        # Center should be white
        self.assertEqual(0.0, circle[14, 14])

        # top and bottom points should be black
        self.assertEqual(1.0, circle[21, 21])
        self.assertEqual(1.0, circle[9, 9])

    def test_ellipse_oob_center(self):
        circle = ShapeGenerator.create_ellipse(image_shape=(10, 10), xy=(100, 100))
        self.assertRaises(UserWarning)

        contents = circle.sum().sum()
        self.assertEqual(0.0, contents)

    def test_ellipse_non_int_width(self):
        # Just round up
        circle = ShapeGenerator.create_ellipse(width=4.4)

        # Center should be white
        self.assertEqual(0.0, circle[14, 14])

        # top and bottom points should be black
        self.assertEqual(1.0, circle[21, 21])
        self.assertEqual(1.0, circle[9, 9])

    def test_noise_1(self):
        # TODO
        # Define Noise options
        # Define uhhHHH everything about them
        pass
