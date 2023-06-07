import inspect
import src.deepbench.image as image
import src.deepbench.astro_object as astro
import src.deepbench.physics_object as physics

import numpy as np


class Collection:
    """

    Take a configuration file (dictionary) and produce the simulation output,
    automatically passing arguments where they need to be.

    Handles both compositional images (ones with multiple objects)
    and single object images

    Holds onto all the parameters used to make these files, including the default parameters, for replication.

    """

    def __init__(self, object_config: dict):
        self.object_type = object_config["object_type"]
        self.object_name = object_config["object_name"]

        self.total_objects = object_config["total_runs"]
        self.included_params = object_config["image_parameters"]
        self.object_rules = object_config["object_parameters"]

        object_parent_class = {
            "sky": image.sky_image.SkyImage,
            "shape": image.shape_image.ShapeImage,
            "physics": physics.physics_object.PhysicsObject,
            "astro": astro.astro_object.AstroObject,
        }[self.object_type]

        self.object_engine_classes = {
            cls.__name__: cls for cls in object_parent_class.__subclasses__()
        }
        self.object_engine_classes[object_parent_class.__name__] = object_parent_class

        self.object_engine = self.object_engine_classes[self.object_name](
            **self.included_params
        )

        self.n_objects = 0
        self.objects = {}
        self.object_params = {}

        if "seed" in object_config:
            self.seed = object_config["seed"]

        if "parameter_noise" in object_config:
            self.parameter_noise = object_config["parameter_noise"]

    def add_parameter_noise(self, seed, params):
        """_summary_

        Args:
            seed (int): integer stored by the program to denote the noise seed added to the object
            params (dict): parameters for to add noise to

        Returns:
            dict: parameters with added uniform noise
        """
        if hasattr(self, "parameter_noise"):
            noisy_object_parameters = {
                key: params[key]
                + np.random.default_rng(seed=seed).uniform(
                    high=self.parameter_noise, size=len(params[key])
                )
                for key in params.keys()
            }
            return noisy_object_parameters

        else:
            return params

    def engine_defaults(self):
        """
        Locate the default parameters for any simulation being called, via the `inspect.signature` method

        Returns:
            dictionary: all the parameters either default to the called object or modified by the program
        """
        init_signature = inspect.signature(
            self.object_engine_classes[self.object_name].__init__
        )
        init_signature_defaults = {
            k: v.default
            for k, v in init_signature.parameters.items()
            if v.default is not inspect.Parameter.empty
        }
        if self.object_type in ["sky", "shape"]:
            create = self.object_engine.combine_objects

        elif self.object_type in ["physics", "astro"]:
            create = self.object_engine.create_object

        create_signature = inspect.signature(create)
        create_signature_defaults = {
            k: v.default
            for k, v in create_signature.parameters.items()
            if v.default is not inspect.Parameter.empty
        }
        return {**init_signature_defaults, **create_signature_defaults}

    def add_object(self):
        """
        Use the parameters set by the configuration file to create an object and store that and its associated parameters
        Adds noise to parameters if set by the program perviously

        If the specified object is a composite image, it will only find the default values for the compositor method, not the indivual simulations

        """
        random_seed = (
            np.random.default_rng().integers(1, 10**6, size=1)[0]
            if not hasattr(self, "seed")
            else self.seed
        )

        if self.object_type in ["sky", "shape"]:
            instance_parameters = [
                self.add_parameter_noise(
                    random_seed, self.object_rules[key]["instance"]
                )
                for key in self.object_rules.keys()
            ]

            object_parameters = [
                self.add_parameter_noise(random_seed, self.object_rules[key]["object"])
                for key in self.object_rules.keys()
            ]

            object = self.object_engine.combine_objects(
                self.object_rules.keys(), instance_parameters, object_parameters
            )

            object_parameters = {
                list(self.object_rules.keys())[key_index]: {
                    "object": object_parameters[key_index],
                    "instance": instance_parameters[key_index],
                }
                for key_index in range(len(self.object_rules.keys()))
            }

        elif self.object_type in ["physics", "astro"]:
            object_parameters = self.add_parameter_noise(random_seed, self.object_rules)
            object_parameters["seed"] = random_seed

            object = self.object_engine.create_object(**object_parameters)

        self.objects[self.n_objects] = object

        self.object_params[self.n_objects] = {
            **self.engine_defaults(),
            **object_parameters,
        }
        self.object_params[self.n_objects] = {
            **self.object_params[self.n_objects],
            **self.included_params,
        }
        self.object_params[self.n_objects]["seed"] = random_seed

        self.n_objects += 1

    def __call__(self):
        """
        Create N objects and add them to the `objects` variable.
        """
        for _ in range(self.total_objects):
            self.add_object()
