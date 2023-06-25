import inspect
import deepbench.image as image
import deepbench.astro_object as astro
import deepbench.physics_object as physics
from deepbench.collection import Save

import numpy as np
import yaml
import os 

class Collection:
    """

    Take a configuration file (dictionary) and produce the simulation output,
    automatically passing arguments where they need to be.

    Handles both compositional images (ones with multiple objects)
    and single object images

    Holds onto all the parameters used to make these files, including the default parameters, for replication.

    Args:
        object_config (dict, optional): dictionary containing the parameters for the simulation output. Required fields:
            * object_type: [sky, shape, physics, astro] : overall type of image
            * object_name: Name of the class used in the image generation (e.g. - Pendulum, Star)
            * total_runs: Number of times the simulation will be executed
            * image_parameters: parameters for the image itself. In single object images, this is the parameters for the parent class.
            * object parameters: list of objects that will be included in each image and their parameters
        Defaults to None.

    """

    def __init__(self, object_config: dict=None):

        self.object_type = None
        self.object_name = None

        self.total_objects = None
        self.included_params = None
        self.object_rules = None


        self.object_engine_classes = None 
        self.object_engine = None 

        self.n_objects = 0
        self.objects = {}
        self.object_params = {}

        if object_config is not None: 
            self._set_parameters(object_config)


    def from_config(self, config_path:str):
        """
        Read an external configuration file and initalize the dataset. Must be run if a configuration is not supplied at initalization. 

        Args:
            config_path (str): Path to yaml file containing an object dictionary. Object dictionary must have the parameters: "object_type","object_name",total_runs",image_parameters","object_parameters"
        """
        config = yaml.safe_load(open(config_path))
        
        self._set_parameters(config)


    def _set_parameters(self, object_config): 

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
        
        if "name" in object_config: 
            self.save_path = object_config["name"]
            if not os.path.exists: 
                os.makedirs(self.save_path)


    def add_parameter_noise(self, seed, params):
        """
        Add noise to the image wide parameters

        Args:
            seed (int): integer stored by the program to denote the noise seed added to the object
            params (dict): parameters that have added noise.

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
            dict: all the parameters either default to the called object or modified by the program
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
        assert self.object_type is not None, "Collection parameters not initialized, please run collection.from_config(your_configuration_path)"

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
        
        if hasattr(self, "save_path"): 
            self.save()


    def save(self, save_path:str=None, format:str='h5'): 
        """
        Save generated dataset to path of your choosing. 
        If the path is not specified, the program will look for a save path to be specified by the configation_file 

        Args:
            save_path (str, optional): directory, location to save a file. Will be created if does not already exist. Defaults to None.
            format (str, optional): Format to save the file in. Defaults to h5.
        """

        if save_path is None: 
            assert hasattr(self, "save_path"), "Could not parse save path from config, please supply it manually"
            save_path = self.save_path
        
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        
        Save(self, save_path)(format=format)

        
        