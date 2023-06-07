import pytest
from src.deepbench.shape_generator.shape_generator import ShapeGenerator

import numpy as np
import matplotlib.patches as patch


def test_patch_conversion_defaults():
    # simple patch object. Convert to a numpy array
    simple_patch = patch.Rectangle(xy=(0, 0), width=1, height=1)
    converted_object = ShapeGenerator((28, 28))._convert_patch_to_image(
        image=simple_patch
    )
    expected_obj_type = np.array([0, 0])
    assert type(converted_object) == type(expected_obj_type)


def test_patch_conversion_default_dimensions():
    simple_patch = patch.Rectangle(xy=(0, 0), width=1, height=1)
    converted_object = ShapeGenerator()._convert_patch_to_image(image=simple_patch)
    converted_object_shape_x, converted_object_shape_y = converted_object.shape
    expected_x_dim, expected_y_dim = 28, 28

    assert converted_object_shape_x == expected_x_dim
    assert converted_object_shape_y == expected_y_dim


def test_patch_conversion_single_image_dimension():
    with pytest.raises(TypeError):
        simple_patch = patch.Rectangle(xy=(0, 0), width=1, height=1)
        ShapeGenerator(tuple(28))._convert_patch_to_image(image=simple_patch)


def test_patch_conversion_N_dimension():
    simple_patch = patch.Rectangle(xy=(0, 0), width=1, height=1)
    converted_object = ShapeGenerator((28, 28, 28))._convert_patch_to_image(
        image=simple_patch
    )
    (
        converted_object_shape_x,
        converted_object_shape_y,
        converted_object_shape_z,
    ) = converted_object.shape
    expected_x_dim, expected_y_dim, expected_z_dim = 28, 28, 28

    assert converted_object_shape_x == expected_x_dim
    assert converted_object_shape_y == expected_y_dim
    assert converted_object_shape_z == expected_z_dim


def test_patch_conversion_size_0():
    with pytest.raises(ValueError):
        simple_patch = patch.Rectangle(xy=(0, 0), width=1, height=1)
        ShapeGenerator((0, 0))._convert_patch_to_image(image=simple_patch)


def test_patch_conversion_non_int_size():
    simple_patch = patch.Rectangle(xy=(0, 0), width=1, height=1)
    converted_object = ShapeGenerator((55.5, 55.5))._convert_patch_to_image(
        image=simple_patch
    )
    converted_object_shape_x, converted_object_shape_y = converted_object.shape
    expected_x_dim, expected_y_dim = 56, 56

    assert converted_object_shape_x == expected_x_dim
    assert converted_object_shape_y == expected_y_dim


def test_patch_conversion_non_int_size_round():
    simple_patch = patch.Rectangle(xy=(0, 0), width=1, height=1)
    converted_object = ShapeGenerator(image_shape=(55.1, 55.6))._convert_patch_to_image(
        image=simple_patch
    )
    converted_object_shape_x, converted_object_shape_y = converted_object.shape
    expected_x_dim, expected_y_dim = 56, 56
    assert converted_object_shape_x == expected_x_dim
    assert converted_object_shape_y == expected_y_dim


def test_resize_default():
    simple_image = np.zeros((32, 32))
    resized_image = ShapeGenerator().resize(image=simple_image)
    resized_image_x, resized_image_y = resized_image.shape
    default_new_size_x, default_new_size_y = 28, 28

    assert resized_image_x == default_new_size_x
    assert resized_image_y == default_new_size_y


def test_resize_dim_mismatch():
    with pytest.raises(ValueError):
        simple_image = np.zeros((32, 32))
        resize_dimensions = (1, 1, 1)
        ShapeGenerator().resize(simple_image, resize_dimensions=resize_dimensions)


def test_resize_zero_size_source():
    with pytest.raises(ValueError):
        simple_image = np.zeros((0, 0))
        resize_dimensions = (1, 1)
        ShapeGenerator().resize(image=simple_image, resize_dimensions=resize_dimensions)


def test_resize_zero_size_target():
    with pytest.raises(ValueError):
        simple_image = np.zeros((1, 1))
        resize_dimensions = (0, 0)
        ShapeGenerator().resize(image=simple_image, resize_dimensions=resize_dimensions)


def test_resize_upscale():
    simple_image = np.zeros((32, 32))
    resize = (50, 50)
    resized_image = ShapeGenerator().resize(
        image=simple_image, resize_dimensions=resize
    )
    resized_image_x, resized_image_y = resized_image.shape
    new_size_x, new_size_y = resize

    assert resized_image_x == new_size_x
    assert resized_image_y == new_size_y


def test_resize_negative():
    with pytest.raises(ValueError):
        simple_image = np.zeros((80, 80))
        resize = (-1, -1)
        ShapeGenerator().resize(image=simple_image, resize_dimensions=resize)


def test_rectangle_default():
    rectangle = ShapeGenerator().create_rectangle()

    x, y = rectangle.shape
    expected_x, expected_y = (28, 28)
    assert x == expected_x
    assert y == expected_y

    # Each corner should have a black pixel
    assert 1.0 == rectangle[9, 10], "corner 1 failed"
    assert 1.0 == rectangle[19, 19], "corner 4 failed"

    # Center needs to be white (default is unfilled)
    assert 0.0 == rectangle[14, 14], "Center Filled"


def test_rectangle_size_center_dim_mismatch():
    with pytest.raises(ValueError):
        ShapeGenerator().create_rectangle(center=(1, 1, 1))


def test_rectangle_xy_out_of_range():
    with pytest.raises(UserWarning):
        rectangle = ShapeGenerator((10, 10)).create_rectangle(center=(100, 100))

        rectangle_contents = rectangle.sum().sum()
        assert 0 == rectangle_contents


def test_rectangle_angle_in_bounds_no_change():
    angle = 90
    rectangle_rotated = ShapeGenerator().create_rectangle(angle=angle)

    rectangle_non_rotated = ShapeGenerator().create_rectangle(angle=0)

    # But it's a square so it looks the same
    assert rectangle_rotated.all() == rectangle_non_rotated.all()


def test_rectangle_angle_in_bounds_change():
    angle = 360
    rectangle = ShapeGenerator().create_rectangle(width=10, height=10, angle=angle)

    # Each corner should have a black pixel
    assert (1.0, rectangle[9, 10], "corner 1 failed")
    assert (1.0, rectangle[19, 19], "corner 4 failed")

    # Center needs to be white (default is unfilled)
    assert (0.0, rectangle[14, 14], "Center Filled")


def test_rectangle_angle_oob_positive():
    angle = 45
    rectangle_rotated = ShapeGenerator().create_rectangle(angle=angle + 360)
    rectangle_non_rotated = ShapeGenerator().create_rectangle(angle=angle)

    assert rectangle_rotated.all() == rectangle_non_rotated.all()


def test_rectangle_angle_oob_negative():
    angle = 45
    rectangle_rotated = ShapeGenerator().create_rectangle(angle=angle - 360)
    rectangle_non_rotated = ShapeGenerator().create_rectangle(angle=angle)

    assert rectangle_rotated.all() == rectangle_non_rotated.all()


def test_rectangle_fill():
    # This should fill the whole screen.
    rectangle = ShapeGenerator().create_rectangle(width=80, height=80, fill=True)
    ideal_rectangle = np.ones((28, 28))

    assert ideal_rectangle.all() == rectangle.all()


def test_polygon_default():
    triangle = ShapeGenerator().create_regular_polygon()

    shape_x, shape_y = triangle.shape
    expected_x, expected_y = 28, 28

    assert shape_x == expected_x
    assert shape_y == expected_y

    # Center should be white
    assert 0.0 == triangle[14, 14]

    # top point should be black
    assert 1.0 == triangle[21, 17]

    # TODO the trig to check the other points here


def test_polygon_size_center_mismatch():
    with pytest.raises(ValueError):
        ShapeGenerator().create_regular_polygon(center=(14, 14, 14))


def test_polygon_positive_oob_angle():
    angle = 45
    triangle_rotated = ShapeGenerator().create_regular_polygon(angle=angle + 360)
    triangle_non_rotated = ShapeGenerator().create_regular_polygon(angle=angle)

    assert (triangle_rotated.all(), triangle_non_rotated.all())


def test_polygon_negative_oob_angle():
    angle = 45
    triangle_rotated = ShapeGenerator().create_regular_polygon(angle=angle - 360)
    triangle_non_rotated = ShapeGenerator().create_regular_polygon(angle=angle)

    assert (triangle_rotated.all(), triangle_non_rotated.all())


def test_polygon_negative_radius():
    triangle = ShapeGenerator().create_regular_polygon(radius=-10)
    # Center should be white
    assert (0.0, triangle[14, 14])

    # top point should be black
    # The radius will just be abs
    assert (1.0, triangle[21, 17])


def test_polygon_negative_vertices():
    with pytest.raises(ValueError):
        ShapeGenerator((28, 28)).create_regular_polygon(vertices=-3)


def test_arc_default():
    arc = ShapeGenerator((28, 28)).create_arc()

    x, y = arc.shape
    expected_x, expected_y = (28, 28)
    assert (x, expected_x)
    assert (y, expected_y)

    assert (0.0, arc[14, 14], "Empty Center")
    assert (1.0, arc[14, 24], "Bottom Point")
    assert (1.0, arc[23, 15], "Starting Point")


def test_arc_size_center_dim_mismatch():
    with pytest.raises(ValueError):
        ShapeGenerator().create_arc(center=(0, 0, 0))


def test_arc_oob_negative_theta1():
    angle = 45
    arc_rotated = ShapeGenerator().create_arc(theta1=angle - 360)
    arc_non_rotated = ShapeGenerator().create_arc(theta1=angle)

    assert arc_rotated.all() == arc_non_rotated.all()


def test_arc_oob_positive_theta1():
    angle = 45
    arc_rotated = ShapeGenerator().create_arc(theta1=angle + 360)
    arc_non_rotated = ShapeGenerator().create_arc(theta1=angle)

    assert arc_rotated.all() == arc_non_rotated.all()


def test_arc_oob_negative_theta2():
    angle = 45
    arc_rotated = ShapeGenerator().create_arc(theta2=angle - 360)
    arc_non_rotated = ShapeGenerator().create_arc(theta2=angle)

    assert (arc_rotated.all(), arc_non_rotated.all())


def test_arc_oob_positive_theta2():
    angle = 45
    arc_rotated = ShapeGenerator().create_arc(theta2=angle + 360)
    arc_non_rotated = ShapeGenerator().create_arc(theta2=angle)

    assert (arc_rotated.all(), arc_non_rotated.all())


def test_arc_theta2_less_than_theta1():

    arc_negative_sweep = ShapeGenerator().create_arc(theta1=90, theta2=0)
    arc_positive_sweep = ShapeGenerator().create_arc(theta1=0, theta2=90)

    assert arc_negative_sweep.all() == arc_positive_sweep.all()


def test_arc_oob_width():
    arc = ShapeGenerator((14, 14)).create_arc(
        radius=28, line_width=100, theta1=0, theta2=360
    )

    size = arc.size
    n_black_pixels = int(arc.sum().sum())
    assert size == n_black_pixels


def test_line_defaults():
    line = ShapeGenerator().create_line()

    x, y = line.shape
    expected_x, expected_y = (28, 28)
    assert x == expected_x
    assert y == expected_y

    # Bottom left top right are black. Opposite are white
    assert (1.0 == line[1, 2], "line start incorrect")
    assert (1.0 == line[26, 27], "line end incorrect")

    assert (0.0 == line[1, 27], "line corner incorrect")
    assert (0.0 == line[27, 1], "line corner incorrect")


def test_line_size_start_dim_mismatch():
    with pytest.raises(ValueError):
        ShapeGenerator().create_line(start=(0, 0, 0))


def test_line_size_end_dim_mismatch():
    with pytest.raises(ValueError):
        ShapeGenerator().create_line(end=(0, 0, 0))


def test_line_start_oob():
    line = ShapeGenerator().create_line(start=(-200, -100))

    # Bottom left top right are black. Opposite are white
    assert 1.0 == line[1, 14]
    assert 1.0 == line[25, 27]


def test_line_end_oob():
    line = ShapeGenerator().create_line(end=(200, 100))

    assert 1.0 == line[1, 1]
    assert 1.0 == line[27, 14]


def test_line_same_start_end():
    with pytest.raises(ValueError):
        ShapeGenerator().create_line(end=(0, 0))


def test_ellipse_default():
    circle = ShapeGenerator().create_ellipse()

    shape_x, shape_y = circle.shape
    expected_x, expected_y = 28, 28

    assert shape_x == expected_x
    assert shape_y == expected_y

    # Center should be white
    assert 0.0 == circle[14, 14]

    # Default is a circle
    assert 1.0 == circle[11, 10]
    assert 1.0 == circle[14, 19]
    assert 1.0 == circle[19, 14]
    assert 1.0 == circle[9, 14]


def test_ellipse_size_xy_mismatch():
    with pytest.raises(ValueError):
        ShapeGenerator().create_ellipse(center=(14, 14, 14))


def test_ellipse_0_radius():
    ## Nothing is displayed
    with pytest.raises(UserWarning):
        ShapeGenerator().create_ellipse(width=0, height=0)


def test_ellipse_non_int_radius():
    # Just round up
    circle = ShapeGenerator().create_ellipse(height=9.4)

    # Center should be white
    assert 0.0 == circle[14, 14]

    # top and bottom points should be black
    assert 1.0 == circle[14, 19]
    assert 1.0 == circle[19, 14]


def test_ellipse_oob_center():
    with pytest.raises(UserWarning):
        circle = ShapeGenerator((10, 10)).create_ellipse(center=(100, 100))
        contents = circle.sum().sum()
        assert 0.0 == contents


def test_ellipse_non_int_width():
    # Just round up
    circle = ShapeGenerator().create_ellipse(width=9.4)

    # Center should be white
    assert 0.0 == circle[14, 14]

    # top and bottom points should be black
    assert 1.0 == circle[14, 19]
    assert 1.0 == circle[19, 14]
