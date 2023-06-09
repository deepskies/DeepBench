![GitHub Workflow Status](https://img.shields.io/github/workflow/status/deepskies/DeepBench/build-bench)
![GitHub Workflow Status](https://img.shields.io/github/workflow/status/deeepskies/DeepBench/test-bench?label=test)
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
 [![PyPI version](https://badge.fury.io/py/deepbench.svg)](https://badge.fury.io/py/deepbench)



# DeepBench

### What is it?
Simulation library for very simple simulations to *benchmark* machine learning algorithms.
![DeepBench Logo](docs/repository_support/DeepSkies_Logos_DeepBench.png)


### Why do we need it? Why is it useful?
1. There are very universally recognized scientifically meaningful benchmark data sets, or methods with which to generate them.
2. A very simple data set will have objects, patterns, and signals that are intuitively quanitifiable and will be fast to generate.
3. A very simple data set will be a great testing ground for new networks and for newcomers to practice with the technology.


## Requirements
* python = ">=3.8,<3.11,"
* numpy = "^1.24.3"
* matplotlib = "^3.7.1"
* scikit-image = "^0.20.0"
* astropy = "^5.2.2"
* autograd = "^1.5"
* pyyaml = "^6.0"



## Install

### From PyPi
```
pip install deepbench
```

### From Source

```
git clone https://github.com/deepskies/DeepBench.git
pip install poetry
poetry shell
poetry install
poetry run pytest --cov
```

## General Features
1. very fast to generate
2. Mimics in a very basic / toy way what is in astro images
3. Be fully controllable parametrically

![DeepBench Logo](docs/repository_support/DeepBench.png)

### Included Simulations

1. Astronomy Objects - simple astronomical object simulation
- Galaxy, Spiral Galaxy, Star

2. Shapes - simple 2D geometric shapes
- Rectangle, Regular Polygon, Arc, Line, Ellipse

3. Physics Objects - simple physics simulations
- Neutonian Pendulum, Hamiltonian Pendulum

## Example

### Standalone
* Produce 3 instance of a pendulum over 10 different times with some level of noise.
```
import numpy as np
from deepbench import Collection

configuration = {
	"object_type": "physics",
	"object_name": "Pendulum",
	"total_runs": 3,
	"parameter_noise": 0.2,
	"image_parameters": {
		"pendulum_arm_length": 2,
		"starting_angle_radians": 0.25,
		"acceleration_due_to_gravity": 9.8,
		"noise_std_percent":{
			"acceleration_due_to_gravity": 0
	},
	"object_parameters":{
		"time": np.linspace(0, 1, 10)
	}
}

phy_objects = Collection(configuration)()

objects = phy_objects.objects
parameters = phy_objects.object_parameters
```

* Produce a noisy shape image with a rectangle and an arc

```
import numpy as np
from deepbench import Collection

configuration = {
	"object_type": "shape",
	"object_name": "ShapeImage",

	"total_runs": 1,
	"image_parameters": {
		"image_shape": (28, 28),
		"object_noise_level": 0.6
	},

	"object_parameters": {
		[
		"rectangle": {
			"object": {
				"width": np.random.default_rng().integers(2, 28),
				"height": np.random.default_rng().integers(2, 28),
				"fill": True
			},
			"instance": {}
		},
		"arc":{
			"object": {
				"radius": np.random.default_rng().integers(2, 28),
				"theta1":np.random.default_rng().integers(0, 20),
				"theta2":np.random.default_rng().integers(21, 180)
			},
			"instance":{}
		}

		]
	}
}

shape_image = Collection(configuration)()

objects = shape_image.objects
parameters = shape_image.object_parameters
```


### Fine-Grained Control
* Make a whole bunch of stars
```
from deepbench.astro_object.star_object import Star
import numpy as np

star = Star(
        image_dimensions = (28,28),
        noise = 0.3,
        radius= 0.8,
        amplitude = 1.0
    )

generated_stars = []
x_position, y_position = np.random.default_rng().uniform(low=1, high=27, size=(2, 50))
for x_pos, y_pos in zip(x_position, y_position):
	generated-stars.append(star.create_object(x_pos, y_pos))
```


## Original Development Team
1. Craig Brechmos
2. Renee Hlozek
3. Brian Nord


## How to contribute
I'm really glad you're reading this, because we need volunteer developers to help this project come to fruition.

### Testing

### Submitting changes

Please send a [GitHub Pull Request to simplephysicaliage](https://github.com/deepskies/SimplePhysicalImage/pull/new/master) with a clear list of what you've done (read more about [pull requests](http://help.github.com/pull-requests/)). When you send a pull request, we will love you forever if you include examples. We can always use more test coverage. Please follow our coding conventions (below) and make sure all of your commits are atomic (one feature per commit).

Always write a clear log message for your commits. One-line messages are fine for small changes, but bigger changes should look like this:

    $ git commit -m "A brief summary of the commit
    >
    > A paragraph describing what changed and its impact."

### Coding conventions

Start reading our code and you'll get the hang of it. We optimize for readability:

  * We indent using tabs
  * We ALWAYS put spaces after list items and method parameters (`[1, 2, 3]`, not `[1,2,3]`), around operators (`x += 1`, not `x+=1`), and around hash arrows.
  * This is open source software. Consider the people who will read your code, and make it look nice for them. It's sort of like driving a car: Perhaps you love doing donuts when you're alone, but with passengers the goal is to make the ride as smooth as possible.

