import pytest
import os
import yaml
from src.deepbench.collection.collection import Collection


@pytest.fixture()
def default_physics():
    return yaml.safe_load(
        open(
            f"{os.path.dirname(__file__)}/../src/deepbench/settings/default_physics_object.yaml"
        )
    )


@pytest.fixture()
def default_sky():
    return yaml.safe_load(
        open(
            f"{os.path.dirname(__file__)}/../src/deepbench/settings/default_sky_object.yaml"
        )
    )


@pytest.fixture()
def default_shape():
    return yaml.safe_load(
        open(
            f"{os.path.dirname(__file__)}/../src/deepbench/settings/default_shapes.yaml"
        )
    )


def test_default_init(default_physics, default_shape, default_sky):
    physics = Collection(default_physics)

    assert physics.n_objects == 0
    assert physics.object_type == "physics"
    assert physics.object_name == "Pendulum"

    from src.deepbench.physics_object.pendulum import Pendulum

    assert physics.object_engine == Pendulum

    physics = Collection(default_shape)
    assert physics.n_objects == 0
    assert physics.object_type == "shape"
    assert physics.object_name == "ShapeImage"

    from src.deepbench.image.shape_image import ShapeImage

    assert physics.object_engine == ShapeImage

    physics = Collection(default_sky)
    assert physics.n_objects == 0
    assert physics.object_type == "sky"
    assert physics.object_name == "SkyImage"

    from src.deepbench.image.sky_image import SkyImage

    assert physics.object_engine == SkyImage


def test_add_single_item():
    pass


def test_format_params():
    pass


def test_add_seed():
    pass


def test_find_modules():
    pass


def test_make_image():
    pass


def test_make_shape():
    pass


def test_make_physics_obj():
    pass


def test_make_multiple():
    pass


def test_missing_param():
    pass
