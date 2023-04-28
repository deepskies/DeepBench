# What functionality do we need the simulator to have?

# We need to be able to draw from it at one or multiple moments in time

# Maggie: time needs to be adjustable, as an input to simulate_x
# Becky: I still haven't done this, I will also need to add some sort of external
# check here because the pendulum MCMC currently assumes that the data and the
# model are using all the same points in time

# Becky: I'm confused about how this works with the hierarchy of the inference
# do we need to modify this class so that it can accept arrays and matrices
# of eta values? This needs to happen for the hierarchy, where we have multiple
# moments in time, multiple pendulii, and multiple different planets that 
# we're running the experiment on.
# OR do we just need to make this external, where the science (inference) module
# will call the simulator multiple times within an iterable?

# I would like it to have a nice animation / plotting utility, but lmk if this 
# should be implemented separately and I'll take it out
from astro_object import AstroObject

import numpy as np
import math
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from typing import Union, List


class Pendulum(AstroObject):
    def __init__(self,
                 L: float,
                 theta_0: float,
                 #t: Union[float, List[float]],
                 noise: float,
                 calculation_type: str = "x position",
                 g: float = None,
                 J: float = None,
                 phi: float = None,
                 m: float = None,
                 b: float = None):
        """
        The initialization function for the Pendulum class.

        Args:
            L (float): The length of the pendulum arm
            theta_0 (float): The starting angle of the pendulum
                (angle from the 'ceiling')
            t (Union[float, List[float]]): moment(s) in time
                at which the pendulum is observed
            noise (float): The Poisson noise level to be applied to the object.
                This needs to be updated for the pendulum,
                currently it follows the Poisson prescription
                from astro_object.py
            calculation_type (str): Type of observation of the pendulum.
                Options are ["x position","position and momentum"]
            g (float): Little g, local gravity coefficient, 
                optional if J and phi are defined,
                g = J * phi
            J (float): This is terrible, but the stand-in for big G,
                the gravitational constant, 
                optional if g is defined
            phi (float): M/r^2, this changes based on the planet,
                optional if g is defined
            m (float): Mass of the pendulum bob,
                this is optional if calculation_type is position only.
            b (float): Coefficient of friction, optional argument.

        Examples:

            >>> pendulum_obj = Pendulum(image_dimensions=28, radius=5, amplitude=3, noise_level=0.7)
        """
        super().__init__(
            image_dimensions=1,
            radius=None,
            amplitude=None,
            noise=noise,
        )
        self.L = L
        self.theta_0 = theta_0
        self.noise = noise
        self.calculation_type = calculation_type
        if J is not None and phi is not None:
            # This is if J and phi are defined
            self.J = J
            self.phi = phi
            self.g = J * phi
        else:
            # This is if J and phi are not defined
            self.J = None
            self.phi = None
            self.g = g
        # Optional arguments: mass, friction
        self.m = m if m is not None else 10.
        self.b = b if b is not None else 0.

    # Currently just simulating the x position of the pendulum
    # for one or multiple moments in time
    def simulate_pendulum_position(self, time):
        x = [self.L * math.sin(self.theta_0 *
             math.cos(np.sqrt(self.g / self.L) * t)) for t in time]
        return x

    # I want to add a function that will give you a cute animated pendulum:
    # SUGGESTIONS FOR MAKING IT CUTER APPRECIATED :)

    def animate(self, time):
        # First you need to instatiate the simulator
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
            #ax.annotate('L = '+str())
            #plt.scatter(x, y, c = t,  alpha = 0.5)
        animation = FuncAnimation(fig, update, frames=range(1, len(t)), interval=100)
        plt.show()

    # This is from Sree, simulates an image of the position and momentum, think
    # of it as a summary statistic
    # This part currently is not updated.
    def simulate_I(self):
        # Using Taylor series expansion to solve for position (eta1) and velocity (eta2)
        # output time, position and velocity as image i.e with dimenstions len(time) x 2: https://www.mackelab.org/sbi/tutorial/05_embedding_net/
        m = self.m
        l = self.eta[1]
        g = self.eta[0]
        b = self.b
        dt = self.time[-1] - self.time[0]

        # From here down this needs to be rewritten to work
        # BROKEN FROM HERE DOWN
        eta1 = eta1_0
        eta2 = eta2_0
        data = [[eta1, eta2]]
        for i, t_ in enumerate(time[:-1]):
            next_eta1 = eta1 + eta2 * dt
            next_eta2 = eta2 - (b/(m*l**2) * eta2 - g/l *
                np.sin(next_eta1)) * dt

            data.append([next_eta1, next_eta2])
            eta1 = next_eta1
            eta2 = next_eta2

        data = torch.as_tensor(data) #shape : (len(time), 2)

        nx = len(time)
        ny = 2
        I = torch.zeros(nx,ny)
        for i in range(len(time)):
            for j in range(2):
                I[i,j] = data[i][j]
        I = I.T
        I = I.reshape(1,-1)
        if return_points:
            return I, data
        else:
            return I  

    def create_noise(self):
        noise = self.noise
        return noise.noise(self.noise)

    def create_object(self, time):
        assert self.calculation_type == "x position", f"{self.calculation_type} method is not yet implemented, sorry."
        #assert len(marks) != 0,"List is empty."
        pendulum = self.simulate_pendulum_position(time)
        pendulum += self.create_noise()
        return pendulum

    def displayObject(self):

        # To be implemented. Check parent for details.

        print("Code Container.")


print('initializing the pendulum class')
pend = Pendulum(10., np.pi/4, 1, "x position", g=1)
print('pend', pend)
x = pend.create_object([0])
x = pend.simulate_pendulum_position([0,1,2])
print('x', x)

'''
def __init__(self,
                L: float,
                theta_0: float,
                noise: float,
                calculation_type: str = "x position",
                g: float = None,
                J: float = None,
                phi: float = None,
                m: float = None,
                b: float = None):
'''