from abc import ABC, abstractmethod


class Image(ABC):
    def __init__(self, object_dict, image_shape):

        self._object_dict = object_dict
        self._image_shape = image_shape

        print(
            "Initialize image with a list of objects to add to canvas and the shape of the image."
        )

    def __len__(self):

        return len(self._object_dict.keys())
        print("Return the length of the object list.")

    @abstractmethod
    def create_image(self):  # formerly known as 'combine_objects'

        print("Creates the canvas of the concatenated objects.")

    @abstractmethod
    def generate_noise(self, noise_type, **noise_parameters):

        print("Generates pixel noise on the image.")

    def get_image_parameters(self):

        return tuple(self._image_shape, self._object_dict.keys())
        print("Returns the image shape and object_dict keys in multidimensional tuple.")

    def generate_astro_objects(self, **astro_parameters):

        print("Generates all of the specified AstroObjects to be added to canvas.")

    def save_image(self, file_path, format=".jpeg"):

        print("Saves the resultant image as a .jpeg or .h5 file.")
