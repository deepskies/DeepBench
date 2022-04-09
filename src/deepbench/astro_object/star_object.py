from astro_object import AstroObject
from astropy.modeling.models import Moffat2D


class StarObject(AstroObject):
    def __init__(self, img_dim, noise, center=(0, 0), radius=1, amplitude=1):
        """
        Comment Container.
        """
        super.__init__(
            self,
            image_dimensions=img_dim,
            radius=radius,
            amplitude=amplitude,
            noise_level=noise,
        )
        self._center = center

    def create_object(self, center_x, center_y, alpha=1.0):

        x, y = self.create_meshgrid()
        profile = Moffat2D(
            amplitude=self._amplitude,
            x_center=self._center[0],
            y_center=self._center[1],
            gamma=self._radius,
            alpha=alpha,
        )

        return profile(x, y)
