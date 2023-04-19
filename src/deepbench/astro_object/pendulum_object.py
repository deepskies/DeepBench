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
                 J: float,
                 phi: float,
                 t: Union[float, List[float]],
                 noise: float,
                 calculation_type: str = "x position",
                 m: float = None,
                 b: float = None):
        """
        The initialization function for the Pendulum class.

        Args:
            L (float): The length of the pendulum arm
            theta_0 (float): The starting angle of the pendulum
                (angle from the 'ceiling')
            J (float): This is terrible, but the stand-in for big G,
                the gravitational constant
            phi (float): M/r^2, this changes based on the planet
            t (Union[float, List[float]]): moment(s) in time
                at which the pendulum is observed
            noise (float): The Poisson noise level to be applied to the object.
                This needs to be updated for the pendulum,
                currently it follows the Poisson prescription
                from astro_object.py
            calculation_type (str): Type of observation of the pendulum.
                Options are ["x position","position and momentum"]
            m (float): Mass of the pendulum bob,
                this is optional if calculation_type is position only.
            b (float): Coefficient of friction, optional argument.

        Examples:

            >>> pendulum_obj = Pendulum(image_dimensions=28, radius=5, amplitude=3, noise_level=0.7)
        """
        super().__init__(
            image_dimension=None,
            amplitude=None,
            noise_level=None,
        )
        self.eta = eta
        self.noise = noise
        # Optional arguments: mass, friction
        self.m = m if m is not None else 10.
        self.b = b if b is not None else 0.
        if not self.noise:
            # If it is not defined, then no noise
            self.noise = np.zeros(np.shape(eta)) 
    # I want to add a function that will give you a cute animated pendulum:
    # SUGGESTIONS FOR MAKING IT CUTER APPRECIATED :)

    def animate(self):
        # First you need to instatiate the simulator
        # for x, y, dx/dt, dy/dt (simulate_q_p.())
        t = self.t
        x, y, mom_x, mom_y = self.simulate_q_p()
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
        
    # This is the simulator, currently, just simulating the x position of the pendulum
    # for multiple moments in time
    def simulate_pendulum_position(self, time):
        eta = self.eta
        noise = self.noise
        t = time
        ts = np.repeat(t[:, np.newaxis], eta.shape[0], axis=1)
        if eta.ndim == 1:
            eta = eta[np.newaxis, :]
        # time to solve for position and velocity
        # nested for loop, there's probably a better way to do this
        # output needs to be (n,len(t))
        x = np.zeros((eta.shape[0],len(t)))  
        for n in range(eta.shape[0]):
            # Draw parameter (eta) values from normal distributions
            # To produce noise in the etas you are using to produce the position
            # and momentum of the pendulum at each moment in time
            # Another way to do this would be to just draw once and use that same noisy eta 
            # value for all moments in time, but this would be very similar to just drawing
            # from the prior, which we're already doing.
            gs = np.random.normal(loc=eta[n][0], scale=noise[0], size=np.shape(t))
            Ls = np.random.normal(loc=eta[n][1], scale=noise[1], size=np.shape(t))
            eta_os =  np.random.normal(loc=eta[n][2], scale=noise[2], size=np.shape(t))
            eta_t = np.array([eta_os[i] * math.cos(np.sqrt(gs[i] / Ls[i]) * t[i]) for i, _ in enumerate(t)])
            x[n,:] = np.array([Ls[i] * math.sin(eta_t[i]) for i, _ in enumerate(t)])
        return x

    # This needs to be fixed so that x, y, dx/dt, and dy/dt are all packaged together, also so mass is incorporated
    # into the momentum:
    def simulate_q_p(self):
        eta = self.eta
        t = self.t
        noise = self.noise
        ts = np.repeat(self.t[:, np.newaxis], self.eta.shape[0], axis=1)
        if eta.ndim == 1:
            eta = eta[np.newaxis, :]
        # time to solve for position and velocity

        # nested for loop, there's probably a better way to do this
        # output needs to be (n,len(t))
        x = np.zeros((eta.shape[0],len(t)))
        y = np.zeros((eta.shape[0],len(t)))

        # TO DO: I'm not strictly solving for momentum, just velocities:
        dx_dt = np.zeros((eta.shape[0],len(t)))
        dy_dt = np.zeros((eta.shape[0],len(t)))
        for n in range(eta.shape[0]):

            # Draw parameter (eta) values from normal distributions
            # To produce noise in the etas you are using to produce the position
            # and momentum of the pendulum at each moment in time
            # Another way to do this would be to just draw once and use that same noisy eta 
            # value for all moments in time, but this would be very similar to just drawing
            # from the prior, which we're already doing.

            gs = np.random.normal(loc=eta[n][0], scale=noise[0], size=np.shape(t))
            Ls = np.random.normal(loc=eta[n][1], scale=noise[1], size=np.shape(t))
            eta_os =  np.random.normal(loc=eta[n][2], scale=noise[2], size=np.shape(t))

            eta_t = np.array([eta_os[i] * math.cos(np.sqrt(gs[i] / Ls[i]) * t[i]) for i, _ in enumerate(t)])

            x[n,:] = np.array([Ls[i] * math.sin(eta_t[i]) for i, _ in enumerate(t)])
            y[n,:] = np.array([-Ls[i] * math.cos(eta_t[i]) for i, _ in enumerate(t)])

            # Okay and what about taking the time derivative?
            dx_dt[n,:] = np.array([-Ls[i] * eta_os[i] * np.sqrt(gs[i] / Ls[i]) * math.cos(eta_t[i]) * math.sin( np.sqrt(gs[i] / Ls[i]) * t[i]) for i, _ in enumerate(t)])
            dy_dt[n,:] = np.array([-Ls[i] * eta_os[i] * np.sqrt(gs[i] / Ls[i]) * math.sin(eta_t[i]) * math.sin( np.sqrt(gs[i] / Ls[i]) * t[i]) for i, _ in enumerate(t)])





        return x, y, dx_dt, dy_dt

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
