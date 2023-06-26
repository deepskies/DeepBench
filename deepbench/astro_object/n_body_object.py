from typing import Union, Tuple
from deepbench.astro_object.astro_object import AstroObject


class NBodyObject(AstroObject):
    def __init__(
        self,
        image_dimensions: Union[Tuple[int, int], Tuple[float, float]],
        t_duration: float = 2.0,
        dt: float = 0.2,
        dampening: float = 0,
        noise_level: float = 0.02,
        G: float = 9.8,
        plot_real_time: bool = False,
    ):

        super().__init__(
            image_dimensions=image_dimensions,
            radius=None,
            amplitude=None,
            noise_level=noise_level,
        )
        self.t_duration = t_duration
        self.dt = dt
        self.dampening = dampening
        self.G = G
        self.plot_real_time = plot_real_time

    def create_object(self):

        print("Code Container.")

    def get_acceleration(self):

        print("Code Container.")

    def get_energy(self):

        print("Code Container.")

    def displayObject(self):
        print("Code Container")
