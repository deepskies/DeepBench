from src.deepbench.astro_object.astro_object import AstroObject
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from typing import Union, List, Optional


class Pendulum(AstroObject):
    def __init__(self,
                 pendulum_arm_length: float,
                 starting_angle_radians: float,
                 noise_std_percent: Union[float, List[float]] = 0.0,
                 calculation_type: str = "x position",
                 acceleration_due_to_gravity: Optional[float] = None,
                 big_G_newton: Optional[float] = None,
                 phi_planet: Optional[float] = None,
                 mass_pendulum_bob: Optional[float] = None,
                 coefficient_friction: Optional[float] = None
                 ):
        """
        The initialization function for the Pendulum class.

        Args:
            pendulum_arm_length (float): The length of the pendulum arm
            starting_angle_radians (float): The starting angle of the pendulum
                (angle from the 'ceiling')
            noise_std_percent (Union[float,List[float]]): The Gaussian noise
                level to be applied to the object. If this is one number,
                the standard deviation of the Gaussian noise for each
                parameter is taken to be this percent of each parameter value.
                If this is an array, the std is this percent of each number.
            calculation_type (str): Type of observation of the pendulum.
                Options are ["x position","position and momentum"]
            acceleration_due_to_gravity (float): little g, local gravity
                coefficient, optional if G and phi are defined,
                g = G * phi
            big_G_newton (float): Big G, the gravitational constant,
                optional if g is defined
            phi_planet (float): M/r^2, this changes based on the planet,
                optional if g is defined
            mass_pendulum_bob (float): Mass of the pendulum bob,
                this is optional if calculation_type is position only.
            coefficient_friction (float): Coefficient of friction,
            optional argument.

        Examples:

            >>> pendulum_obj = Pendulum()
        """
        super().__init__(
            image_dimensions=1,
            radius=None,
            amplitude=None,
            noise=noise_std_percent,
        )
        self.pendulum_arm_length = pendulum_arm_length
        self.starting_angle_radians = starting_angle_radians
        self.noise = noise_std_percent
        self.calculation_type = calculation_type
        self.big_G_newton = None if big_G_newton is None else big_G_newton
        self.phi_planet = None if phi_planet is None else phi_planet

        if acceleration_due_to_gravity is None:
            assert self.big_G_newton is not None and self.phi_planet \
                is not None, "must define big_G_newton and phi_planet if \
                    acceleration_due_to_gravity is not provided"
            self.acceleration_due_to_gravity = self.big_G_newton * \
                self.phi_planet
        else:
            self.acceleration_due_to_gravity = acceleration_due_to_gravity
        self.mass_pendulum_bob = 10. if mass_pendulum_bob \
            is None else mass_pendulum_bob
        self.coefficient_friction = 0. if coefficient_friction is None \
            else coefficient_friction

    # Currently just simulating the x position of the pendulum
    # for one or multiple moments in time
    def simulate_pendulum_position(self, time):
        assert len(time) is not None, "Must enter a time"
        assert self.starting_angle_radians > np.pi, \
            "The angle better not be in degrees or else"
        time = np.asarray(time)
        theta_time = self.starting_angle_radians * \
            np.cos(np.sqrt(self.g / self.pendulum_arm_length))
        x = self.pendulum_arm_length * np.sin(theta_time * time)
        return x

    # To be added by Omari
    def simulate_pendulum_position_and_momentum(self, time):
        return

    def create_noise(self, baseline, time):
        # Make a list of parameters to add noise to
        # Here we add noise not just on the final measurement
        # but via adding it to each parameter and propagating
        # through to the final measurement (ie x position)
        parameter_list = [self.pendulum_arm_length,
                          self.starting_angle_radians,
                          self.acceleration_due_to_gravity]
        # Define the standard deviation of noise for each parameter
        if type(self.noise) == 'float':  # then its one number
            std_noise = [self.noise * p for p in parameter_list]
        else:
            for p, i in enumerate(parameter_list):
                std_noise = [self.noise[i] * p for p in parameter_list]
        # Add noise to global parameters
        pendulum_arm_length_noisy = np.random.normal(
            loc=self.pendulum_arm_length,
            scale=std_noise[0]
        )
        starting_angle_radians_noisy = np.random.normal(
            loc=self.starting_angle_radians,
            scale=std_noise[1]
        )
        acceleration_due_to_gravity_noisy = np.random.normal(
            loc=self.acceleration_due_to_gravity,
            scale=std_noise[2]
        )
        # Run the baseline pendulum
        pendulum_baseline = Pendulum(
            pendulum_arm_length=self.pendulum_arm_length,
            starting_angle_radians=self.starting_angle_radians,
            calculation_type=self.calculation_type,
            acceleration_due_to_gravity=self.acceleration_due_to_gravity,
        ).simulate_pendulum_position(time)
        # Create new Pendulum object with noisy parameters
        pendulum_noisy = Pendulum(
            pendulum_arm_length=pendulum_arm_length_noisy,
            starting_angle_radians=starting_angle_radians_noisy,
            calculation_type=self.calculation_type,
            acceleration_due_to_gravity=acceleration_due_to_gravity_noisy,
        ).simulate_pendulum_position(time)
        return pendulum_noisy - pendulum_baseline

    def create_object(self, time: Union[float, list[float]]):
        assert self.calculation_type == "x position", f"{self.calculation_type} method is not yet implemented, sorry."
        pendulum = self.simulate_pendulum_position(time)
        pendulum += self.create_noise(pendulum, time)
        return pendulum

    def animate(self, time: list[float]):#Union[float, list[float]]
        # Right now this just plots x and t
        # Instantiate the simulator
        pendulum = self.create_object(time)
        plt.clf()
        # Create the figure and axis
        fig = plt.figure(figsize=(10, 3))
        ax1 = fig.add_subplot(111)
        def update(i):
            # Calculate the position and velocity at the current time step
            # Clear the previous plot
            # Plot the quantity output from the pendulum
            pendulum_now = pendulum[i]
            ax1.plot([time, 0], [pendulum_now, 1.4])
            ax1.scatter(time[i], pendulum_now)
            ax1.set_title(f'{self.calculation_type} = '
                          + str(round(pendulum_now, 1)))
        #assert type(time) == 'float', \
        #    "cannot run because only one moment in time"
        FuncAnimation(fig, update, frames=range(1, len(time)), interval=100)
        plt.show()
        return