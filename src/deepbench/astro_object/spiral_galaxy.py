from galaxy_object import GalaxyObject

from numpy import random


class SpiralGalaxyObject(GalaxyObject):
    def __init__(
        self,
        img_dim,
        amplitude=1,
        center=(50, 50),
        radius=25,
        n=1.0,
        ellipse=random.uniform(0.1, 0.9),
        theta=random.uniform(-1.5, 1.5),
    ):

        super().__init__(
            img_dim=img_dim,
            amplitude=amplitude,
            center=center,
            radius=radius,
            n=n,
            ellipse=ellipse,
            theta=theta,
        )

    def create_sprial_profile(self):

        # TO BE IMPLEMENTED.
        print("Code Container.")

    def create_object(self):

        # TO BE IMPLEMENTED.
        print("Code Container.")
