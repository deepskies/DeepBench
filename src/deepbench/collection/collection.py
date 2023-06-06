import src.deepbench.image as image
import src.deepbench.physics_object as physics


class Collection:
    def __init__(self, object_config: dict):
        self.object_type = object_config["object_type"]
        self.object_name = object_config["object_name"]

        self.total_objects = object_config["total_objects"]
        self.included_params = object_config["object_parameters"]

        object_parent_class = {
            "sky": image.sky_image.SkyImage,
            "shape": image.shape_image.ShapeImage,
            "physics": physics.physics_object.PhysicsObject,
        }[self.object_type]
        self.object_engine = {
            cls.__name__: cls for cls in object_parent_class.__subclasses__()
        }
        self.object_engine[object_parent_class.__name__] = object_parent_class

        self.object_engine = self.object_engine[self.object_name](
            **self.included_params
        )

        self.n_objects = 0
        self.objects = {}
        self.object_params = {}

    def add_parameter_noise(self):
        pass

    def create_random_seed(self):
        pass

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
