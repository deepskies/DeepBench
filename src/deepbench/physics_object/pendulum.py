from src.deepbench.physics_object.physics_object import PhysicsObject
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from typing import Union, List, Optional


class Pendulum(PhysicsObject):
    def __init__(self,
                 pendulum_arm_length: float,
                 starting_angle_radians: float,
                 #noise_std_percent: dict = {},
                 noise_std_percent: Union[float, List[float]] = 0.0,
                 calculation_type: str = "x position",
                 acceleration_due_to_gravity: Optional[float] = None,
                 big_G_newton: Optional[float] = None,
                 phi_planet: Optional[float] = None,
                 mass_pendulum_bob: Optional[float] = 10.0,
                 coefficient_friction: Optional[float] = 0.0
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

            >>> pendulum_obj = Pendulum(pendulum_arm_length=10.,
                                        starting_angle_radians=np.pi/4,
                                        acceleration_due_to_gravity=9.8,
                                        noise_standard_percent = 0.1,
                                        calculation_type = 'x position'
                                        )
        """
        super().__init__(
            noise_level=noise_std_percent,
        )

        self.pendulum_arm_length = pendulum_arm_length
        self.starting_angle_radians = starting_angle_radians
        assert self.starting_angle_radians < np.pi, \
            "The angle better not be in degrees or else"
        self.big_G_newton = big_G_newton
        self.phi_planet = phi_planet
        if acceleration_due_to_gravity is None:
            assert self.big_G_newton is not None and self.phi_planet \
                is not None, "must define big_G_newton and phi_planet if \
                    acceleration_due_to_gravity is not provided"
            self.acceleration_due_to_gravity = self.big_G_newton * \
                self.phi_planet
        else:
            self.acceleration_due_to_gravity = acceleration_due_to_gravity
        self.mass_pendulum_bob = mass_pendulum_bob
        self.coefficient_friction = coefficient_friction
        self.initial_parameters = {'pendulum_arm_length':
                                   self.pendulum_arm_length,
                                   'starting_angle_radians':
                                   self.starting_angle_radians,
                                   'acceleration_due_to_gravity':
                                   self.acceleration_due_to_gravity}

        # TODO verify the requested noise parameters are variables you can use

        for key, item in noise_std_percent.items():
            assert key in [key for key in self.dict.keys()]
            # key is a variable in the class
            assert type(item) in [np.array, float]

    def create_noise(self, seed: int = 42, n_steps: int | tuple[int, int] = 10) -> np.array:
        # Make a list of parameters to add noise to
        # Here we add noise not just on the final measurement
        # but via adding it to each parameter and propagating
        # through to the final measurement (ie x position)
        parameter_list = [self.pendulum_arm_length,
                          self.starting_angle_radians,
                          self.acceleration_due_to_gravity]
        # Define the standard deviation of noise for each parameter
        if type(self.noise) is float:  # then its one number
            std_noise = [self.noise * p for p in parameter_list]
        else:
            for i, p in enumerate(parameter_list):
                std_noise = [self.noise[i] * p for p in parameter_list]
        # Add noise to global parameters
        self.pendulum_arm_length_noisy = np.random.normal(
            loc=self.pendulum_arm_length,
            scale=std_noise[0]
        )
        self.starting_angle_radians = np.random.normal(
            loc=self.starting_angle_radians,
            scale=std_noise[1]
        )
        self.acceleration_due_to_gravity = np.random.normal(
            loc=self.acceleration_due_to_gravity,
            scale=std_noise[2]
        )

    def destroy_noise(self):
        # Re-modify the global parameters to
        # have the original value
        self.pendulum_arm_length = \
            self.initial_parameters['pendulum_arm_length']
        self.starting_angle_radians = \
            self.initial_parameters['starting_angle_radians']
        self.acceleration_due_to_gravity = \
            self.initial_parameters['acceleration_due_to_gravity']
        return

    def create_object(self, time: np.array, noiseless: bool = False, seed: int = 42):

        self.create_noise(seed=seed, n_steps=time.shape)
        if noiseless:
            self.destroy_noise()

        pendulum = self.simulate_pendulum_dynamics(time)

        self.destroy_noise()
        return pendulum

    def simulate_pendulum_dynamics(self, time: Union[float, np.array[float]]):
        assert len(time) is not None, "Must enter a time"
        time = np.asarray(time)
        theta_time = self.starting_angle_radians * \
            np.cos(np.sqrt(self.acceleration_due_to_gravity /
                           self.pendulum_arm_length))
        x = self.pendulum_arm_length * np.sin(theta_time * time)
        return x

    def displayObject(self, time: Union[float, np.array[float]]):
        plt.clf()
        plt.scatter(time, self.create_object(time),
                    label='noisy')
        plt.scatter(time, self.simulate_pendulum_dynamics(time),
                    label='noise free')
        plt.legend()
        plt.show()

    def animateObject(self, time: Union[float, np.array[float]]):
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
        if isinstance(time, float):
            time = [time]
        anim = FuncAnimation(fig, update,
                             frames=range(1, len(time)),
                             interval=100)
        plt.show(anim)
        return
