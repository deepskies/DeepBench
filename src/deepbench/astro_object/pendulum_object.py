from src.deepbench.astro_object.astro_object import AstroObject
import numpy as np
import math
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from typing import Union, List


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
            self.phi = phi_planet
            self.acceleration_due_to_gravity = big_G_newton * phi_planet
        else:
            # This is if big_G_newton and phi_planet are not defined
            self.big_G_newton = None
            self.phi_planet = None
            self.acceleration_due_to_gravity = acceleration_due_to_gravity
        # Optional arguments: mass, friction
        self.mass_pendulum_bob = mass_pendulum_bob if mass_pendulum_bob is not None else 10.
        self.coefficient_friction = coefficient_friction if coefficient_friction is not None else 0.

    # Currently just simulating the x position of the pendulum
    # for one or multiple moments in time
    def simulate_pendulum_position(self, time):
        assert len(time) is not None, "Must enter a time"
        x = [self.pendulum_arm_length * math.sin(self.starting_angle_radians *
             math.cos(np.sqrt(self.acceleration_due_to_gravity / self.pendulum_arm_length) * t)) for t in time]
        return x

    # To be added by Omari
    def simulate_pendulum_position_and_momentum(self, time):
        return

    # I want to add a function that wil give you a cute animated pendulum:
    # SUGGESTIONS FOR MAKING IT CUTER APPRECIATED :)
    def animate(self, time):
        # First you need to instantiate the simulator
        # for x, y, dx/dt, dy/dt (simulate_q_p.())
        x, y, mom_x, mom_y = self.simulate_q_p(time)
        #t, x, y, mom_x, mom_y = create_t_p_q_noise(eta_o, noise = [0.0,0.0,0.0])
        plt.clf()
        # Create the figure and axis
        #fig, axs = plt.subplots(nrows = 1, ncols = 2)
        fig = plt.figure(figsize = (10,3))
        ax1 = fig.add_subplot(121)
        ax2 = fig.add_subplot(122)
        # Define the function to update the plot at each time step
        def update(i):
            # Calculate the position and velocity at the current time step
            # Clear the previous plot
            #ax1.clear()
            # Plot the position of the pendulum
            xnow = x[i]
            ynow = y[i]
            print('xnow', xnow)
            dxnow = mom_x[i]
            dynow = mom_y[i]
            ax1.plot([xnow,0],[ynow,1.4])
            ax1.scatter(xnow, ynow)#, markersize=10)
            ax1.set_title('x = '+str(round(xnow, 1))+', y = '+str(round(ynow, 1)))
            # Set the axis limits
            ax1.set_xlim(-5, 5)
            ax1.set_ylim(-7, 3)#0, 1.5)
            #ax2.plot([mom_x],[mom_y])
            ax2.set_title('mom_x = '+str(round(dxnow, 1))+', mom_y = '+str(round(dynow, 1)))
            ax2.scatter(dxnow, dynow)#, markersize=10)
            # Set the axis limits
            ax2.set_xlim(-10, 10)
            ax2.set_ylim(-3, 3)#0, 1.5)
            #ax.annotate('l = '+str())
            #plt.scatter(x, y, c = t,  alpha = 0.5)
        animation = FuncAnimation(fig, update, frames=range(1, len(t)), interval=100)
        plt.show()

    # This is from Sree, simulates an image of the position and momentum, think
    # of it as a summary statistic
    # This part currently is not updated.
    def simulate_I(self):
        return

    def create_noise(self):
        # We will modify this to be our own special
        # noise profile :)
        return super(self).create_noise()

    def create_object(self, time: Union[float, list[float]]):
        assert self.calculation_type == "x position", f"{self.calculation_type} method is not yet implemented, sorry."
        #assert len(marks) != 0,"list is empty."
        pendulum = self.simulate_pendulum_position(time)
        pendulum += self.create_noise()
        return pendulum

    def displayObject(self):

        # To be implemented. Check parent for details.

        print("Code Container.")
