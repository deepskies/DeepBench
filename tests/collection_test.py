import pytest
import os
import yaml
from src.deepbench.collection.collection import Collection


@pytest.fixture()
def default_physics():
    return yaml.safe_load(
        f"{os.path(__file__)}/../src/deepbench/settings/default_physics_object.yaml"
    )


@pytest.fixture()
def default_sky():
    return yaml.safe_load(
        f"{os.path(__file__)}/../src/deepbench/settings/default_sky_object.yaml"
    )


@pytest.fixture()
def default_shape():
    return yaml.safe_load(
        f"{os.path(__file__)}/../src/deepbench/settings/default_shapes.yaml"
    )


def test_default_init():
    pass


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
