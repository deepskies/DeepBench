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
        pass

    def test_resize_dim_mismatch(self):
        pass

    def test_resize_zero_size(self):
        pass

    def test_resize_upscale(self):
        pass

    def test_resize_downscale(self):
        pass

    def test_resize_upscale_pad(self):
        pass

    def test_rectangle_default(self):
        pass

    def test_rectangle_single_dim_xy(self):
        pass

    def test_rectangle_size_center_dim_mismatch(self):
        pass

    def test_rectangle_xy_out_of_range(self):
        pass

    def test_rectangle_width_oob(self):
        pass

    def test_rectangle_height_oob(self):
        pass

    def test_rectangle_angle_in_bounds(self):
        pass

    def test_rectangle_angle_oob_positive(self):
        pass

    def test_rectangle_angle_oob_negative(self):
        pass

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
