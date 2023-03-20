from deepbench.module_data.generate_data import *
from deepbench.module_draw.generate_draw import *
from deepbench.module_draw.AstroObject import *

class Star(AstroObject):

    classname = 'Star'

    def __init__(self, center, radius, amplitude, pois_noise, gaussianBlur, img_dim):
        """

        :param center: Tuple (float, float)
        :param radius:
        :param amplitude:
        :param pois_noise:
        :param gaussianBlur:
        """
        super.__init__(Star, self, position=center, radius=radius, amplitude=amplitude,
                       image_noise=pois_noise, gaussian_blur=gaussianBlur, image_dim=img_dim)

    def create(self, n_pix_side):
        """
        Return image of specific size
        :param n_pix_side: specified size
        :return: imshape to be saved
        """

        imshape = empty_imshape(n_pix_side)
        # star event
        imshape = create_Moffat2D(imshape, x_0=round(self.center[0]),
                                  y_0=round(self.center[1]),
                                  amplitude=self.amplitude,
                                  radius=self.radius)

        if self.noise is not 0.:
            noise_profile = create_noise(imshape, self.noise)
            imshape = create_psf(imshape)
        imshape += noise_profile
        return imshape

    def get_params(self):
        """
        Return object labels here?
        :return: parameters defining object
        """
        return self.params
