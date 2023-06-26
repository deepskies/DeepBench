import pytest
from deepbench.astro_object.astro_object import AstroObject

# Checking all the child classes work
from deepbench.astro_object import GalaxyObject
from deepbench.astro_object import NBodyObject
from deepbench.astro_object import SpiralGalaxyObject
from deepbench.astro_object import StarObject


def test_astro_init():
    with pytest.raises(TypeError):
        AstroObject(image_dimensions=1, radius=1, amplitude=1, noise_level=1)


def test_galaxy_init():
    GalaxyObject(image_dimensions=1)
    assert issubclass(GalaxyObject, AstroObject)


def test_nbody_init():
    NBodyObject(image_dimensions=1)
    assert issubclass(NBodyObject, AstroObject)


def test_spiral_galaxy_init():
    SpiralGalaxyObject(image_dimensions=1)
    assert issubclass(SpiralGalaxyObject, AstroObject)
    assert issubclass(SpiralGalaxyObject, GalaxyObject)


def test_star_init():
    StarObject(image_dimensions=1, noise_level=1)
    assert issubclass(StarObject, AstroObject)


def test_object_contains():

    radius = 5
    centerx = centery = 14
    star = StarObject(image_dimensions=28, noise_level=0, radius=radius).create_object(
        centerx, centery
    )
    galaxy = GalaxyObject(image_dimensions=28, noise_level=0).create_object(
        centerx, centery
    )
    spiral = SpiralGalaxyObject(
        image_dimensions=28, noise_level=0, radius=radius
    ).create_object(centerx, centery)

    assert (star != galaxy).all()
    assert (star != spiral).all()
    assert (galaxy != spiral).all()
