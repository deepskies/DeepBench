from unittest import TestCase
from src.deepbench.shape_generator import ShapeGenerator


class TestShapeGenerator(TestCase):
    def test_patch_conversion(self):
        # Not sure how to completely separate this one from other test, they all use it
        pass

    def test_patch_conversion_defaults(self):
        pass

    def test_patch_conversion_single_image_dimension(self):
        # Catches incorrect inputs for all the shapes as well
        pass

    def test_patch_conversion_size_0(self):
        # Catches it for all shapes as well
        pass

    def test_patch_conversion_non_int_size(self):
        pass

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
