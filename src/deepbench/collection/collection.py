import sys

from src.deepbench.image.sky_image import SkyImage
from src.deepbench.image.shape_image import ShapeImage
from src.deepbench.physics_object.physics_object import PhysicsObject


class Collection:
    def __init__(self, object_config: dict):

        self.object_type = object_config["object_type"]
        self.object_name = object_config["object_name"]

        self.total_objects = object_config["total_objects"]
        self.included_params = object_config["object_parameters"]

        object_parent_class = {
            "sky": SkyImage,
            "shape": ShapeImage,
            "physics": PhysicsObject,
        }[self.object_type]

        possible_engines = {
            engine.__name__: engine
            for engine in sys.modules
            if issubclass(engine, object_parent_class)
        }

        self.object_engine = possible_engines[self.object_name]

        self.objects = {}
        self.n_objects = 0

    def add_object(self):
        random_seed = ""

        if self.object_type in ["sky", "shape"]:
            object = self.object_engine.combine_objects()

        elif self.object_type == "physics":
            object = self.object_engine.create_object()

        self.objects[self.n_objects] = object

        self.object_params[self.n_objects] = {param for param in ""}

        self.object_params[self.n_objects]["seed"] = random_seed
        self.n_object += 1

    def __call__(self):
        for _ in self.total_objects:
            self.add_object()
