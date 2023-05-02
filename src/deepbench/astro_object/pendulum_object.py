from src.deepbench.astro_object.astro_object import AstroObject
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from typing import Union


class Pendulum(AstroObject):
    def __init__(self,
                 pendulum_arm_length: float,
                 starting_angle_radians: float,
                 noise: float,
                 calculation_type: str = "x position",
                 acceleration_due_to_gravity: Union[float, None] = None,
                 big_G_newton: Union[float, None] = None,
                 phi_planet: Union[float, None] = None,
                 mass_pendulum_bob: Union[float, None] = None,
                 coefficient_friction: Union[float, None] = None
                 ):
        """
        The initialization function for the Pendulum class.

        Args:
            pendulum_arm_length (float): The length of the pendulum arm
            starting_angle_radians (float): The starting angle of the pendulum
                (angle from the 'ceiling')
            noise (float): The Poisson noise level to be applied to the object.
                This needs to be updated for the pendulum,
                currently it folows the Poisson prescription
                from astro_object.py
            calculation_type (str): Type of observation of the pendulum.
                Options are ["x position","position and momentum"]
            acceleration_due_to_gravity (float): little g, local gravity coefficient,
                optional if G and phi are defined,
                g = G * phi
            big_G_newton (float): Big G, the gravitational constant,
                optional if g is defined
            phi_planet (float): M/r^2, this changes based on the planet,
                optional if g is defined
            mass_pendulum_bob (float): Mass of the pendulum bob,
                this is optional if calculation_type is position only.
            coefficient_friction (float): Coefficient of friction, optional argument.

        Examples:

            >>> pendulum_obj = Pendulum()
        """
        super().__init__(
            image_dimensions=1,
            radius=None,
            amplitude=None,
            noise=noise,
        )
        self.pendulum_arm_length = pendulum_arm_length
        self.starting_angle_radians = starting_angle_radians
        self.noise = noise
        self.calculation_type = calculation_type
        if big_G_newton is not None and phi_planet is not None:
            # This is if big_G_newton and phi_planet are defined
            self.big_G_newton = big_G_newton
            self.phi_planet = phi_planet
            self.acceleration_due_to_gravity = big_G_newton * phi_planet
        else:
            # This is if big_G_newton and phi_planet are not defined
            self.big_G_newton = None
            self.phi_planet = None
            self.acceleration_due_to_gravity = acceleration_due_to_gravity
        # Optional arguments: mass, friction
        self.mass_pendulum_bob = mass_pendulum_bob if \
            mass_pendulum_bob is not None else 10.
        self.coefficient_friction = coefficient_friction if \
            coefficient_friction is not None else 0.

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
        # produce noise on each parameter individually
        pendulum_arm_length = self.pendulum_arm_length
        starting_angle_radians = self.starting_angle_radians
        noise_multiple = self.noise
        calculation_type = self.calculation_type
        big_G_newton = self.big_G_newton
        phi_planet = self.phi_planet
        acceleration_due_to_gravity = self.acceleration_due_to_gravity
        mass_pendulum_bob = self.mass_pendulum_bob
        coefficient_friction = self.coefficient_friction
        

        # time to solve for position and velocity

        # nested for loop, there's probably a better way to do this
        # output needs to be (n,len(t))
        x = np.zeros((theta.shape[0],len(t)))

        gs = np.random.normal(loc=theta[n][0], scale=noise[0], size=np.shape(t))
        Ls = np.random.normal(loc=theta[n][1], scale=noise[1], size=np.shape(t))
        theta_os =  np.random.normal(loc=theta[n][2], scale=noise[2], size=np.shape(t))

        # FIX: THIS NO LONGER NEEDS TO BE A LOOP
        theta_t = np.array([theta_os[i] * math.cos(np.sqrt(gs[i] / Ls[i]) * t[i]) for i, _ in enumerate(t)])
        # FIX: WOULDNT IT BE AWESOME IF I COULD RUN EVERYTHING THROUGH THE
        # SIMULATION AGAIN FOR EACH NOISY PARAMETER
        x = np.array([Ls[i] * math.sin(theta_t[i]) for i, _ in enumerate(t)])
        # The output needs to be the same shape as the parameters
        # Okay now I'm confused because I actually think this creates 
        # noise plus baseline

        return noise - baseline

    def create_object(self, time: Union[float, list[float]]):
        assert self.calculation_type == "x position", f"{self.calculation_type} method is not yet implemented, sorry."
        pendulum = self.simulate_pendulum_position(time)
        pendulum += self.create_noise(pendulum, time)
        return pendulum

    def animate(self, time: Union[float, list[float]]):
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
        FuncAnimation(fig, update, frames=range(1, len(time)), interval=100)
        plt.show()
        return