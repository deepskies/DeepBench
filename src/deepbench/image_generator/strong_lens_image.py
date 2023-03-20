from image import Image
from shape_generator import shape_generator

from numpy import random


class StrongLensImage(Image):
    """
    Description Container.

    Methods:
    """

    __strong_lens_dict = {"star": {"img_dim": 28.0, "noise": 0.7}, "arc": {}}

    def __init__(self, strong_lens_dict, image_shape=(128, 128)):

        if strong_lens_dict:
            super().__init__(strong_lens_dict, image_shape)
        else:
            super().__init__(self.__strong_lens_dict, image_shape)

    def create_object(self):

        print("Code container.")

    def hasStar(self):

        print("Code container.")
