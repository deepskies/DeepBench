# What functionality do we need the simulator to have?
# Need to be able to draw from it at one point in time
# Need to animate

import numpy as np
import math
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


class pendulum:
    
    def __init__(self, theta, t, noise, m = None, b = None):

        self.theta = theta
        self.t = t
        self.noise = noise

        # Optional arguments: mass, friction
        self.m = m if m is not None else 10.
        self.b = b if b is not None else 0.
        # Other optional arguments could be ????
        # I'm not sure how to do this within theta because some of us have different thetas
        
        if not self.noise:
            # If it is not defined, then no noise
            self.noise = np.zeros(np.shape(theta))
    
    # I want to add a function that will give you a cute animated pendulum:
    def animate(self):

        # First you need to instatiate the simulator for x, y, dx/dt, dy/dt (simulate_q_p.())

        t = self.t
        x, y, mom_x, mom_y = self.simulate_q_p()
        #t, x, y, mom_x, mom_y = create_t_p_q_noise(theta_o, noise = [0.0,0.0,0.0])


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
        
    
    def simulate_x(self):
        theta = self.theta
        t = self.t
        noise = self.noise

        ts = np.repeat(t[:, np.newaxis], theta.shape[0], axis=1)


        if theta.ndim == 1:
            theta = theta[np.newaxis, :]

        # time to solve for position and velocity

        # nested for loop, there's probably a better way to do this
        # output needs to be (n,len(t))
        x = np.zeros((theta.shape[0],len(t)))
        
        for n in range(theta.shape[0]):

            # Draw parameter (theta) values from normal distributions
            # To produce noise in the thetas you are using to produce the position
            # and momentum of the pendulum at each moment in time
            # Another way to do this would be to just draw once and use that same noisy theta 
            # value for all moments in time, but this would be very similar to just drawing
            # from the prior, which we're already doing.

            gs = np.random.normal(loc=theta[n][0], scale=noise[0], size=np.shape(t))
            Ls = np.random.normal(loc=theta[n][1], scale=noise[1], size=np.shape(t))
            theta_os =  np.random.normal(loc=theta[n][2], scale=noise[2], size=np.shape(t))

            theta_t = np.array([theta_os[i] * math.cos(np.sqrt(gs[i] / Ls[i]) * t[i]) for i, _ in enumerate(t)])

            x[n,:] = np.array([Ls[i] * math.sin(theta_t[i]) for i, _ in enumerate(t)])
            
        return x

    # This needs to be fixed so that x, y, dx/dt, and dy/dt are all packaged together, also so mass is incorporated
    # into the momentum:
    def simulate_q_p(self):
        theta = self.theta
        t = self.t
        noise = self.noise

        ts = np.repeat(self.t[:, np.newaxis], self.theta.shape[0], axis=1)


        if theta.ndim == 1:
            theta = theta[np.newaxis, :]

        # time to solve for position and velocity

        # nested for loop, there's probably a better way to do this
        # output needs to be (n,len(t))
        x = np.zeros((theta.shape[0],len(t)))
        y = np.zeros((theta.shape[0],len(t)))

        # TO DO: I'm not strictly solving for momentum, just velocities:
        dx_dt = np.zeros((theta.shape[0],len(t)))
        dy_dt = np.zeros((theta.shape[0],len(t)))
        for n in range(theta.shape[0]):

            # Draw parameter (theta) values from normal distributions
            # To produce noise in the thetas you are using to produce the position
            # and momentum of the pendulum at each moment in time
            # Another way to do this would be to just draw once and use that same noisy theta 
            # value for all moments in time, but this would be very similar to just drawing
            # from the prior, which we're already doing.

            gs = np.random.normal(loc=theta[n][0], scale=noise[0], size=np.shape(t))
            Ls = np.random.normal(loc=theta[n][1], scale=noise[1], size=np.shape(t))
            theta_os =  np.random.normal(loc=theta[n][2], scale=noise[2], size=np.shape(t))

            theta_t = np.array([theta_os[i] * math.cos(np.sqrt(gs[i] / Ls[i]) * t[i]) for i, _ in enumerate(t)])

            x[n,:] = np.array([Ls[i] * math.sin(theta_t[i]) for i, _ in enumerate(t)])
            y[n,:] = np.array([-Ls[i] * math.cos(theta_t[i]) for i, _ in enumerate(t)])

            # Okay and what about taking the time derivative?
            dx_dt[n,:] = np.array([-Ls[i] * theta_os[i] * np.sqrt(gs[i] / Ls[i]) * math.cos(theta_t[i]) * math.sin( np.sqrt(gs[i] / Ls[i]) * t[i]) for i, _ in enumerate(t)])
            dy_dt[n,:] = np.array([-Ls[i] * theta_os[i] * np.sqrt(gs[i] / Ls[i]) * math.sin(theta_t[i]) * math.sin( np.sqrt(gs[i] / Ls[i]) * t[i]) for i, _ in enumerate(t)])





        return x, y, dx_dt, dy_dt

    # This is from Sree, simulates an image of the 
    def simulate_I(self):
        # Using Taylor series expansion to solve for position (theta1) and velocity (theta2)
        # output time, position and velocity as image i.e with dimenstions len(time) x 2: https://www.mackelab.org/sbi/tutorial/05_embedding_net/
        m = self.m
        l = self.theta[1]
        g = self.theta[0]
        b = self.b
        dt = self.time[-1] - self.time[0]

        # From here down this needs to be rewritten to work
        theta1 = theta1_0
        theta2 = theta2_0
        data = [[theta1, theta2]]
        for i, t_ in enumerate(time[:-1]):
            next_theta1 = theta1 + theta2 * dt
            next_theta2 = theta2 - (b/(m*l**2) * theta2 - g/l *
                np.sin(next_theta1)) * dt

            data.append([next_theta1, next_theta2])
            theta1 = next_theta1
            theta2 = next_theta2

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
        
    
    
