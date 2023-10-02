import pytest
from deepbench.image import SkyImage


@pytest.fixture()
def star():
    return {
        "objects": "star",
        "object_params": {"center_x": 14, "center_y": 14, "alpha": 1.0},
        "instance_params": {"noise_level": 0, "radius": 1.0, "amplitude": 1.0},
    }


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
    one_image_sky.combine_objects(**star)

    assert image_shape == one_image_sky.image.shape


def test_combine_2_images(star):
    image_shape = (14, 14)
    one_image_sky = SkyImage(image_shape)

    multiple_objects = {
        "objects": [star["objects"], star["objects"]],
        "instance_params": [star["instance_params"], star["instance_params"]],
        "object_params": [star["object_params"], star["object_params"]],
    }
    # Not testing that they're the right ones, only that they're made
    one_image_sky.combine_objects(**multiple_objects)

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
    one_image_sky.combine_objects(**star)

    assert image_shape == one_image_sky.image.shape
    assert (
        one_image_sky.image.all()
        != one_image_sky._generate_astro_object(
            star["objects"], star["instance_params"]
        )
        .create_object(**star["object_params"])
        .all()
    )


def test_generate_gaussian_noise(star):
    image_shape = (14, 14)
    one_image_sky = SkyImage(
        image_shape, object_noise_level=0.1, object_noise_type="poisson"
    )
    one_image_sky.combine_objects(**star)

    assert image_shape == one_image_sky.image.shape
    assert (
        one_image_sky.image.all()
        != one_image_sky._generate_astro_object(
            star["objects"], star["instance_params"]
        )
        .create_object(**star["object_params"])
        .all()
    )


def test_add_fake_noise(star):
    with pytest.raises(NotImplementedError):

        fake_noise = "Not A Noise Type"
        image_shape = (14, 14)
        one_image_sky = SkyImage(image_shape, object_noise_type=fake_noise)
        one_image_sky.combine_objects(**star)


def test_not_an_astro_object(star):
    fake_object = "I wanted to write a funny joke here but my brain is gone"
    with pytest.raises(NotImplementedError):

        image_shape = (14, 14)
        one_image_sky = SkyImage(image_shape)
        one_image_sky.combine_objects(
            fake_object, star["instance_params"], star["object_params"]
        )


def test_make_all_astro_objects():
    sky_objects = ["star", "galaxy", "spiral_galaxy"]
    sky_params = [{"noise_level": 0, "radius": 1.0, "amplitude": 1.0}, {}, {}]
    object_params = [
        {"center_x": 14, "center_y": 14},
        {"center_x": 14, "center_y": 14},
        {"center_x": 14, "center_y": 14},
    ]

    image_shape = (14, 14)
    one_image_sky = SkyImage(image_shape)
    one_image_sky.combine_objects(sky_objects, sky_params, object_params)


def test_make_different_images():

    sky_params = {"noise_level": 0, "radius": 1.0, "amplitude": 1.0}
    object_params = {"center_x": 14, "center_y": 14}

    image_shape = (14, 14)
    one_image_sky = SkyImage(image_shape, scale=False)
    star_image = one_image_sky.combine_objects(["star"], sky_params, object_params)
    galaxy_image = one_image_sky.combine_objects(["galaxy"], sky_params, object_params)

    assert (star_image != galaxy_image).all()


def test_make_the_same_things():

    sky_params = {"noise_level": 0, "radius": 1.0, "amplitude": 1.0}
    object_params = {"center_x": 14, "center_y": 14}

    image_shape = (14, 14)
    one_image_sky = SkyImage(image_shape, scale=True)
    star_image = one_image_sky.combine_objects(["star"], sky_params, object_params)
    galaxy_image = one_image_sky.combine_objects(["galaxy"], sky_params, object_params)

    combined_image = star_image + galaxy_image
    generated_combined_image = one_image_sky.combine_objects(
        ["star", "galaxy"],
        instance_params=[sky_params, sky_params],
        object_params=[object_params, object_params],
    )

    assert (combined_image == generated_combined_image).all()
