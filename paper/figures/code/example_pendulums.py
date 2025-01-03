from deepbench.physics_object import HamiltonianPendulum, Pendulum
import matplotlib.pyplot as plt
import numpy as np


# Define the number of objects in the plot and the total figure size
fig, subplots = plt.subplots(1, 2, figsize=(int(19 * (3 / 4)), int(7 * 3 / 4)))

# Set the times to calculate the pendulum position over
# 1 point every second, for 0 to 25 seconds
time = np.array(np.linspace(0, 25, 25))

# Produce pendulum object
pendulum = Pendulum(
    pendulum_arm_length=10.0,
    starting_angle_radians=np.pi / 4,
    acceleration_due_to_gravity=9.8,
    noise_std_percent={
        "pendulum_arm_length": 0.0,
        "starting_angle_radians": 0.1,
        "acceleration_due_to_gravity": 0.1,
    },
)

# Use the noiseless argument to make the pendulum w/o noise
# Plot that against the time and with scatter and line options
pendulum_noiseless = pendulum.create_object(time, noiseless=True)
subplots[0].plot(time, pendulum_noiseless, color="black")
subplots[0].scatter(
    time, pendulum_noiseless, color="black", label="Noiseless", marker=">"
)

# Use the noiseless=False to do the same with a noiseless pendulum
pendulum_noisy = pendulum.create_object(time, noiseless=False)
subplots[0].plot(time, pendulum_noisy, color="red")
subplots[0].scatter(time, pendulum_noisy, color="red", label="Noisy")


# Produce noiseless pendulum object for the H
pendulum = HamiltonianPendulum(
    pendulum_arm_length=10.0,
    starting_angle_radians=np.pi / 4,
    acceleration_due_to_gravity=9.8,
    noise_std_percent={
        "pendulum_arm_length": 0.0,
        "starting_angle_radians": 0.0,
        "acceleration_due_to_gravity": 0.0,
    },
)

# Calculate the pendulum positions and energies
pendulum_data = pendulum.create_object(time)

# Plot the line and scatterplot versions of the position wrt time
subplots[1].plot(pendulum_data[4], pendulum_data[0], color="black")
subplots[1].scatter(
    pendulum_data[4], pendulum_data[0], color="black", label="Noiseless", marker=">"
)

# Repeat the process with the noisy pendulum
pendulum = HamiltonianPendulum(
    pendulum_arm_length=10.0,
    starting_angle_radians=np.pi / 4,
    acceleration_due_to_gravity=9.8,
    noise_std_percent={
        "pendulum_arm_length": 0.1,
        "starting_angle_radians": 0.0,
        "acceleration_due_to_gravity": 0.0,
    },
)

pendulum_data = pendulum.create_object(time)

subplots[1].plot(pendulum_data[4], pendulum_data[0], color="red")
subplots[1].scatter(pendulum_data[4], pendulum_data[0], color="red", label="Noisy")

# Set plot labels
subplots[0].set_title("Newtonian")
subplots[1].set_title("Hamiltonian")

# Set axices labels
for plot in subplots.ravel():
    # plot.set(xticks=[], yticks=[])

    plot.set_xlabel("Time (s)")
    plot.set_ylabel("X Position (m)")

# Assign legend location
subplots[1].legend(loc="center left", bbox_to_anchor=(1.02, 1))

plt.savefig("./pendulums.png")
