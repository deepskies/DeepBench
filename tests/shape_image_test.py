import pytest
from deepbench.image import ShapeImage


@pytest.fixture()
def rectangle():
    return {
        "objects": "rectangle",
        "object_params": {"fill": True},
        "instance_params": {},
    }


def test_init():
    test_sky = ShapeImage((14, 14))
    assert (14, 14) == test_sky.image_shape


def test_1dim_size():
    with pytest.raises(AssertionError):
        im_shape = (12,)
        ShapeImage(im_shape)


def test_combine_one_image(rectangle):
    image_shape = (14, 14)
    shapes_image = ShapeImage(image_shape)

    #     # Not testing that they're the right ones, only that they're made
    single_image = shapes_image.combine_objects(**rectangle)
    assert image_shape == single_image.shape


def combine_all_images():
    image_shape = (14, 14)
    shapes_image = ShapeImage(image_shape)

    all_shapes = shapes_image.method_map.keys()
    multiple_objects = {
        "objects": [shape for shape in all_shapes],
        "instance_params": [{} for _ in all_shapes],
        "object_params": [{} for _ in all_shapes],
    }
    # Not testing that they're the right ones, only that they're made
    out_image = shapes_image.combine_objects(**multiple_objects)

    assert image_shape == out_image.shape


def test_combine_no_images():
    image_shape = (14, 14)
    shapes_image = ShapeImage(image_shape)

    assert 0 == shapes_image.image.sum()


def test_generate_noise(rectangle):
    image_shape = (14, 14)
    shapes_image_guass = ShapeImage(
        image_shape, object_noise_level=0.8, object_noise_type="gaussian"
    )
    noiseless_image = shapes_image_guass._create_object(
        rectangle["objects"], rectangle["object_params"]
    )

    guass_noise_image = shapes_image_guass.combine_objects(**rectangle)

    assert guass_noise_image.all() != noiseless_image.all()

    shapes_image_poisson = ShapeImage(
        image_shape, object_noise_level=8, object_noise_type="poisson"
    )
    poisson_noise_image = shapes_image_poisson.combine_objects(**rectangle)
    assert poisson_noise_image.all() != noiseless_image.all()

    assert poisson_noise_image[0][0] != guass_noise_image[0][0]


def test_add_fake_noise(rectangle):
    with pytest.raises(NotImplementedError):

        fake_noise = "Not A Noise Type"
        image_shape = (14, 14)
        shapes_image = ShapeImage(image_shape, object_noise_type=fake_noise)
        shapes_image.combine_objects(**rectangle)


def test_not_an_astro_object(rectangle):
    fake_object = "I wanted to write a funny joke here but my brain is gone"
    with pytest.raises(NotImplementedError):

        image_shape = (14, 14)
        shapes_image = ShapeImage(image_shape)
        shapes_image.combine_objects(
            fake_object, rectangle["instance_params"], rectangle["object_params"]
        )
