from unittest import TestCase
from src.deepbench.shape_generator import ShapeGenerator

import numpy as np
import matplotlib.patches as patch


class TestShapeGenerator(TestCase):
    def test_patch_conversion_defaults(self):
        # simple patch object. Convert to a numpy array
        simple_patch = patch.Rectangle(xy=(0, 0), width=1, height=1)
        converted_object = ShapeGenerator._convert_patch_to_image(image=simple_patch)
        expected_obj_type = np.array
        self.assertIsInstance(converted_object, expected_obj_type)

    def test_patch_conversion_default_dimensions(self):
        simple_patch = patch.Rectangle(xy=(0, 0), width=1, height=1)
        converted_object = ShapeGenerator._convert_patch_to_image(image=simple_patch)
        converted_object_shape_x, converted_object_shape_y = converted_object.shape
        expected_x_dim, expected_y_dim = 28, 28

        self.assertEqual(converted_object_shape_x, expected_x_dim)
        self.assertEqual(converted_object_shape_y, expected_y_dim)

    def test_patch_conversion_single_image_dimension(self):
        simple_patch = patch.Rectangle(xy=(0, 0), width=1, height=1)
        ShapeGenerator._convert_patch_to_image(image=simple_patch, image_shape=28)
        self.assertRaises(ValueError)

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
        simple_patch = patch.Rectangle(xy=(0, 0), width=1, height=1)
        ShapeGenerator._convert_patch_to_image(image=simple_patch, image_shape=(0, 0))
        self.assertRaises(ValueError)

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
        simple_image = np.zeros((32, 32))
        resize_dimensions = (1, 1, 1)
        ShapeGenerator.resize(image=simple_image, resize_dimensions=resize_dimensions)

        self.assertRaises(ValueError)

    def test_resize_zero_size_source(self):
        simple_image = np.zeros((0, 0))
        resize_dimensions = (1, 1)
        ShapeGenerator.resize(image=simple_image, resize_dimensions=resize_dimensions)

        self.assertRaises(ValueError)

    def test_resize_zero_size_target(self):
        simple_image = np.zeros((1, 1))
        resize_dimensions = (0, 0)
        ShapeGenerator.resize(image=simple_image, resize_dimensions=resize_dimensions)

        self.assertRaises(ValueError)

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

    def test_rectangle_default(self):
        rectangle = ShapeGenerator.create_rectangle()

        x, y = rectangle.shape
        expected_x, expected_y = (28, 28)
        self.assertEqual(x, expected_x)
        self.assertEqual(y, expected_y)

        # Each corner should have a black pixel
        self.assertEqual(1, rectangle[21, 9])
        self.assertEqual(1, rectangle[9, 9])
        self.assertEqual(1, rectangle[9, 21])
        self.assertEqual(1, rectangle[21, 21])

        # Center needs to be white (default is unfilled)
        self.assertEqual(0, rectangle[14, 14])

    def test_rectangle_single_dim_xy(self):
        ShapeGenerator.create_rectangle(xy=1)
        self.assertRaises(ValueError)

    def test_rectangle_size_center_dim_mismatch(self):
        ShapeGenerator.create_rectangle(xy=1)
        self.assertRaises(ValueError)

    def test_rectangle_xy_out_of_range(self):
        rectangle = ShapeGenerator.create_rectangle(image_shape=(10, 10), xy=(100, 100))
        self.assertRaises(UserWarning)

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
        self.assertEqual(1, rectangle[21, 21])
        self.assertEqual(1, rectangle[9, 11])
        self.assertEqual(1, rectangle[21, 11])
        self.assertEqual(1, rectangle[9, 21])

    # TODO Test to check odd n on width and height

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
        pass

    def test_polygon_size_center_mismatch(self):
        pass

    def test_polygon_oob_xy(self):
        pass

    def test_polygon_positive_oob_angle(self):
        pass

    def test_polygon_negative_oob_angle(self):
        pass

    def test_negative_radius(self):
        pass

    def test_negative_vertices(self):
        pass

    def test_circle_default(self):
        pass

    def test_circle_single_dim_xy(self):
        pass

    def test_circle_size_xy_mismatch(self):
        pass

    def test_circle_0_radius(self):
        pass

    def test_circle_non_int_radius(self):
        pass

    def test_circle_oob_center(self):
        pass

    def test_circle_non_int_width(self):
        pass

    def test_circle_oob_width(self):
        pass

    def test_arc_default(self):
        pass

    def test_arc_size_center_dim_mismatch(self):
        pass

    def test_arc_oob_center(self):
        pass

    def test_arc_oob_negative_theta1(self):
        pass

    def test_arc_oob_positive_theta1(self):
        pass

    def test_arc_oob_negative_theta2(self):
        pass

    def test_arc_oob_positive_theta2(self):
        pass

    def test_arc_oob_width(self):
        pass

    def test_line_defaults(self):
        pass

    def test_line_size_start_dim_mismatch(self):
        pass

    def test_line_size_end_dim_mismatch(self):
        pass

    def test_line_start_end_dim_mismatch(self):
        pass

    def test_line_start_oob(self):
        pass

    def test_line_end_oob(self):
        pass

    def test_line_same_start_end(self):
        pass

    def test_line_max_width(self):
        pass

    def test_noise_1(self):
        # TODO
        # Define Noise options
        # Define uhhHHH everything about them
        pass
