import pytest
import os
import yaml
import numpy as np

from deepbench.collection import Collection


@pytest.fixture()
def default_physics():
    return yaml.safe_load(
        open(
            f"{os.path.dirname(__file__)}/../deepbench/settings/default_physics_object.yaml"
        )
    )


@pytest.fixture()
def default_sky():
    return yaml.safe_load(
        open(
            f"{os.path.dirname(__file__)}/../deepbench/settings/default_sky_object.yaml"
        )
    )


@pytest.fixture()
def default_shape():
    return yaml.safe_load(
        open(f"{os.path.dirname(__file__)}/../deepbench/settings/default_shapes.yaml")
    )


def test_default_init(default_physics, default_shape, default_sky):
    physics = Collection(default_physics)

    assert physics.n_objects == 0
    assert physics.object_type == "physics"
    assert physics.object_name == "Pendulum"

    from deepbench.physics_object import Pendulum

    assert isinstance(physics.object_engine, Pendulum)

    physics = Collection(default_shape)
    assert physics.n_objects == 0
    assert physics.object_type == "shape"
    assert physics.object_name == "ShapeImage"

    from deepbench.image import ShapeImage

    assert isinstance(physics.object_engine, ShapeImage)

    physics = Collection(default_sky)
    assert physics.n_objects == 0
    assert physics.object_type == "sky"
    assert physics.object_name == "SkyImage"

    from deepbench.image import SkyImage

    assert isinstance(physics.object_engine, SkyImage)

def test_load_from_config(): 
    config_path = f"{os.path.dirname(__file__)}/../deepbench/settings/default_physics_object.yaml"
    physics = Collection()
    physics.from_config(config_path)
    
    physics.add_object()

    assert len(physics.objects) == len(physics.object_params) == 1
    assert physics.n_objects == 1

def test_run_without_config(): 
    physics = Collection()
    with pytest.raises(AssertionError): 
        physics.add_object()


def test_add_single_item_phy(default_physics):
    physics = Collection(default_physics)
    physics.add_object()

    assert len(physics.objects) == len(physics.object_params) == 1
    assert physics.n_objects == 1


def test_add_single_item_image(default_sky):
    sky = Collection(default_sky)
    sky.add_object()

    assert len(sky.objects) == len(sky.object_params) == 1
    assert sky.n_objects == 1


def test_add_seed(default_physics):
    phy = Collection(default_physics)
    phy.add_object()
    assert "seed" in phy.object_params[0].keys()


def test_make_image(default_sky):
    sky = Collection(default_sky)
    sky.add_object()
    sky_object = sky.objects[0]
    sky_object_param = sky.object_params[0]

    assert sky_object.shape[0] == sky_object_param["image_shape"][0]


def test_make_shape(default_shape):
    shape = Collection(default_shape)
    shape.add_object()
    shape_object = shape.objects[0]
    shpe_object_param = shape.object_params[0]

    assert shape_object.shape[0] == shpe_object_param["image_shape"][0]


def test_make_physics_obj(default_physics):
    phy = Collection(default_physics)
    phy.add_object()
    phy_object = phy.objects[0]
    phy_object_param = phy.object_params[0]

    assert phy_object.shape[0] == len(phy_object_param["time"])


def test_included_seed(default_physics):
    default_physics["seed"] = 56
    physics = Collection(default_physics)
    physics()
    for key in physics.object_params:
        assert physics.object_params[key]["seed"] == 56


def test_generate_seed(default_physics):
    physics = Collection(default_physics)
    physics()
    seeds = [
        physics.object_params[obj_index]["seed"]
        for obj_index in physics.object_params.keys()
    ]
    assert len(seeds) == len(set(seeds))


def test_find_default_params(default_physics):
    physics = Collection(default_physics)
    default_object_params_keys = {
        "time",
        "seed",
        "pendulum_arm_length",
        "starting_angle_radians",
        "acceleration_due_to_gravity",
        "noise_std_percent",
        "big_G_newton",
        "phi_planet",
        "mass_pendulum_bob",
        "coefficient_friction",
        "verbose",
        "noiseless",
    }

    physics.add_object()
    assert default_object_params_keys == {
        key for key in physics.object_params[0].keys()
    }


def test_number_object_created(default_physics):
    n_objects = 5
    default_physics["total_runs"] = n_objects
    physics = Collection(default_physics)
    physics()

    assert len(physics.objects) == len(physics.object_params) == n_objects


def test_add_parameter_noise(default_physics):
    default_physics["parameter_noise"] = 0.2
    physics = Collection(default_physics)

    physics()

    assert len(
        np.unique(
            np.asarray(
                [
                    physics.object_params[obj_index]["time"]
                    for obj_index in physics.object_params.keys()
                ]
            ).flatten()
        )
    ) == len(
        np.asarray(
            [
                physics.object_params[obj_index]["time"]
                for obj_index in physics.object_params.keys()
            ]
        ).flatten()
    )


def test_no_added_noise(default_physics):
    default_physics.pop("parameter_noise", None)
    physics = Collection(default_physics)

    physics()
    arm_lengths = np.unique(
        np.asarray(
            [
                physics.object_params[obj_index]["time"]
                for obj_index in physics.object_params.keys()
            ]
        ).flatten()
    )
    assert len(arm_lengths) == len(default_physics["object_parameters"]["time"])


def test_save_results_no_path(default_physics): 
    collection = Collection(default_physics)
    collection.add_object()
    with pytest.raises(AssertionError): 
        collection.save()

def test_save_supplied_path(default_physics): 
    collection = Collection(default_physics)
    collection.add_object()
    collection.save("./custom_path/")

    assert os.path.exists("./custom_path/dataset.h5")
    assert os.path.exists("./custom_path/dataset_parameters.yaml")

def test_save_results_yes_path(default_physics): 
    default_physics['name'] = "./from_config_dataset/"
    collection = Collection(default_physics)
    collection.add_object()
    collection.save()
