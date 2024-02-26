from deepbench.image import SkyImage, ShapeImage
from deepbench.physics_object import HamiltonianPendulum, Pendulum
import matplotlib.pyplot as plt
import numpy as np


# Each image is 480,480
image_shape = (480, 480)

# Total images N and figure size
fig, subplots = plt.subplots(2, 4, figsize=(12, 6))

# Center of all images is at 480/2, 480/2
center = image_shape[0] / 2


# Parameters for each ellipse
ellipse_params = {
    "center": (center, center),
    "width": 100,
    "height": 200,
    "fill": True,
    "angle": 30,
}
shape_single = ShapeImage(image_shape, object_noise_level=0.0)
single_shape_noiseless = shape_single.combine_objects(
    ["ellipse"], object_params=[ellipse_params]
)

subplots[0, 0].imshow(single_shape_noiseless)

# Use the same parameters to make an ellipse with noise
shape_single = ShapeImage(image_shape, object_noise_level=0.4)
shape_single_noisy = shape_single.combine_objects(
    ["ellipse"], object_params=[ellipse_params]
)

subplots[0, 1].imshow(shape_single_noisy)

# Produce a rectangle with specified line widths
line_params = {
    "center": (center + int(center / 2), center),
    "width": 120,
    "height": 200,
    "line_width": 20,
}
shape_two = ShapeImage(image_shape, object_noise_level=0)
# Use the combine objects method to make ellipses and rectangles with the above prameters
shape_two_noiseless = shape_two.combine_objects(
    ["ellipse", "rectangle"], object_params=[ellipse_params, line_params]
)

subplots[0, 2].imshow(shape_two_noiseless)

# Do it with a noise argument now
shape_two = ShapeImage(image_shape, object_noise_level=0.2)
shape_two_noisy = shape_single.combine_objects(
    ["ellipse", "rectangle"], object_params=[ellipse_params, line_params]
)

subplots[0, 3].imshow(shape_two_noisy)

# Read the process with specifiations for astronomy objects
star_instance = {"radius": 100.0, "amplitude": 100.0}
star_params = {"center_x": center - int(center / 2), "center_y": center}

galaxy_instance = {"radius": 30.0, "amplitude": 200.0, "ellipse": 0.8, "theta": 0.2}
galaxy_params = {"center_x": center, "center_y": center + int(center / 2)}
subplots[1, 0].set_ylabel("Astronomy", labelpad=8.0)

one_image_sky = SkyImage(image_shape)
one_sky = one_image_sky.combine_objects(
    ["star"], instance_params=[star_instance], object_params=[star_params]
)

subplots[1, 0].imshow(one_sky)


one_sky_noise = SkyImage(image_shape, object_noise_level=0.4)
one_image_sky_noise = one_sky_noise.combine_objects(
    ["star"], instance_params=[star_instance], object_params=[star_params]
)

subplots[1, 1].imshow(one_image_sky_noise)

one_image_sky = SkyImage(image_shape)
one_sky = one_image_sky.combine_objects(
    ["star", "galaxy"],
    instance_params=[star_instance, galaxy_instance],
    object_params=[star_params, galaxy_params],
)

subplots[1, 2].imshow(one_sky)


one_sky_noise = SkyImage(image_shape, object_noise_level=0.4)
one_image_sky_noise = one_sky_noise.combine_objects(
    ["star", "galaxy"],
    instance_params=[star_instance, galaxy_instance],
    object_params=[star_params, galaxy_params],
)

subplots[1, 3].imshow(one_image_sky_noise)


one_sky_noise = SkyImage(image_shape, object_noise_level=0.4)
one_image_sky_noise = one_sky_noise.combine_objects(
    ["star", "galaxy"],
    instance_params=[star_instance, galaxy_instance],
    object_params=[star_params, galaxy_params],
)

subplots[1, 3].imshow(one_image_sky_noise)

# Y axis labels for each row
subplots[0, 0].set_ylabel("Geometry", labelpad=10.0)

# Remove unnecessary ticks, only put them on the 100 pixel marks
# Flip the images so it starts at 0.,0.
ticks = np.linspace(0, image_shape[0], int(image_shape[0] / 100))
for plot in subplots.ravel():
    plot.autoscale(tight=True)
    plot.set_yticks(ticks.tolist()[::-1])
    plot.invert_yaxis()
    plot.set_xticks(ticks)

# All object titles
subplots[0, 0].set_title("Noiseless Single Object")
subplots[0, 2].set_title("Noiseless Multi-Object")
subplots[0, 1].set_title("Noisy Single Object")
subplots[0, 3].set_title("Noisy Multi-Object")

# Scale information
fig.supxlabel("pixel")
fig.supylabel("pixel")

plt.savefig("../example_objects.png")
