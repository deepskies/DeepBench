import pytest
from src.deepbench.image.sky_image import SkyImage


@pytest.fixture()
def star():
    return (
        "star",
        {"center_x": 14, "center_y": 14, "alpha": 1.0},
        {"noise": 0, "radius": 1.0, "amplitude": 1.0},
    )


def test_init():
    test_sky = SkyImage((14, 14))
    assert (14, 14) == test_sky.image_shape


def test_1dim_size():
    with pytest.raises(AssertionError):
        im_shape = (12,)
        SkyImage(im_shape)


def test_3dim_size():
    im_shape = (14, 14, 3)
    test_sky = SkyImage(im_shape)

    assert test_sky.image.shape == im_shape


def test_combine_one_image(star):
    image_shape = (14, 14)
    one_image_sky = SkyImage(image_shape)

    #     # Not testing that they're the right ones, only that they're made
    #     one_image_sky.combine_objects(star)

    assert image_shape == one_image_sky.image.shape


def test_combine_2_images(star):
    image_shape = (14, 14)
    one_image_sky = SkyImage(image_shape)

    multiple_objects = [star[0], star[0]], [star[1], star[1]], [star[2], star[2]]
    # Not testing that they're the right ones, only that they're made
    one_image_sky.combine_objects(multiple_objects)

    assert image_shape == one_image_sky.image.shape


def test_combine_no_images():
    image_shape = (14, 14)
    one_image_sky = SkyImage(image_shape)

    assert 0 == one_image_sky.image.sum()


def test_generate_gaussian_noise(star):
    image_shape = (14, 14)
    one_image_sky = SkyImage(
        image_shape, object_noise_level=0.1, object_noise_type="guassian"
    )
    one_image_sky.combine_objects(star)

    assert image_shape == one_image_sky.image.shape
    assert one_image_sky.image.any() != one_image_sky._generate_astro_object(star)


def test_add_fake_noise():
    with pytest.raises(NotImplementedError):

        fake_noise = "Not A Noise Type"
        image_shape = (14, 14)
        one_image_sky = SkyImage(image_shape, object_noise_type=fake_noise)
        one_image_sky.combine_objects()


def test_image_not_made():
    with pytest.raises(AssertionError):

        image_shape = (14, 14)
        one_image_sky = SkyImage(image_shape)
        one_image_sky.generate_noise()


def test_not_an_astro_object(star):
    fake_object = "I wanted to write a funny joke here but my brain is gone"
    with pytest.raises(AssertionError):

        image_shape = (14, 14)
        one_image_sky = SkyImage(image_shape)
        one_image_sky.generate_noise(fake_object, star[1], star[2])


def test_make_all_astro_objects():
    sky_objects = ["star", "galaxy", "spiral_galaxy"]
    sky_params = [{"noise": 0, "radius": 1.0, "amplitude": 1.0}, {}, {}]
    object_params = [
        {"center_x": 14, "center_y": 14, "alpha": 1.0},
        {"center_x": 14, "center_y": 14},
        {"center_x": 14, "center_y": 14},
    ]

    image_shape = (14, 14)
    one_image_sky = SkyImage(image_shape)
    one_image_sky.combine_objects(sky_objects, sky_params, object_params)
