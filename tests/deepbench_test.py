from deepbench import __version__


def test_version():
    assert __version__ == "0.2.01"


def test_astroobj_module_import():
    from deepbench import astro_object

    from deepbench.astro_object import GalaxyObject
    from deepbench.astro_object import NBodyObject
    from deepbench.astro_object import SpiralGalaxyObject
    from deepbench.astro_object import StarObject

    astro_object.GalaxyObject
    astro_object.NBodyObject
    astro_object.SpiralGalaxyObject
    astro_object.StarObject


def test_collection_import():
    from deepbench.collection import Collection


def test_phyobj_import():
    from deepbench.physics_object import Pendulum
    from deepbench.physics_object import HamiltonianPendulum


def test_image_import():
    from deepbench.image import SkyImage
    from deepbench.image import ShapeImage
