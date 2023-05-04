from src.deepbench.astro_object.astro_object import AstroObject
import autograd
import autograd.numpy as agnp
import scipy.integrate
import numpy as np
import math
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from typing import Union, List

solve_ivp = scipy.integrate.solve_ivp


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
        assert self.starting_angle_radians > np.pi, \
            "The angle better not be in degrees or else"
        time = np.asarray(time)
        theta_time = self.starting_angle_radians * \
            np.cos(np.sqrt(self.g / self.pendulum_arm_length))
        x = self.pendulum_arm_length * np.sin(theta_time * time)
        return x

    #------------------------------------------------ q and p Stuff Below!!!! ##### q and p Stuff Below!!!! ##### q and p Stuff Below!!!! ----------------------------------------------------#

    def hamiltonian_fn(self, coords):
        q, p = agnp.split(coords, 2)
        kinetic_term = ((self.pendulum_arm_length**2) * (p ** 2))/(2*self.mass_pendulum_bob)
        potential_term = (self.mass_pendulum_bob*self.acceleration_due_to_gravity*self.pendulum_arm_length)*(1 - agnp.cos(q))
        H = kinetic_term + potential_term # pendulum hamiltonian
        return H
    
    def dynamics_fn(self, t, coords):
        dcoords = autograd.grad(self.hamiltonian_fn)(coords) # derives the gradient of the hamiltonian function then computes the gradient values at coords
        dqdt, dpdt = agnp.split(dcoords, 2)
        S = agnp.concatenate([dpdt, -dqdt], axis=-1)
        return S
    
    # To be added by Omari
    def simulate_pendulum_position_and_momentum(self, time, **kwargs):
        t_eval = agnp.linspace(time[0], time[1], int(timescale * (time[1] - time[0])))  # may need to keep this depending on solve_ivp

        # get initial state
        if y0 is None:
            y0 = agnp.random.rand(2) * 2. - 1 # this returns a 1 x 2 array with values between -1 and 1
        if radius is None:
            radius = agnp.random.rand() + 1.3  # sample a range of radii between 1.3 and 2.3
        y0 = y0 / agnp.sqrt((y0 ** 2).sum()) * radius  ## set the appropriate radius

        spring_ivp = solve_ivp(fun=self.dynamics_fn, t_span=t_span, y0=y0, t_eval=t_eval, rtol=1e-10, **kwargs)
        q, p = spring_ivp['y'][0], spring_ivp['y'][1] # these are the future q and p values of the hamiltonian based on y0  
        dydt = [self.dynamics_fn(None, y) for y in spring_ivp['y'].T] # this computes the values of the gradient of the hamiltonian at each row from the transposed sprint_ivp['y']
        dydt = agnp.stack(dydt).T # stack the computed gradients in dydt as row vectors
        dqdt, dpdt = agnp.split(dydt, 2) # split the dydt into dqdt and dpdt

        # add noise
        q += agnp.random.randn(*q.shape) * self.noise  # creates a random array of size q.shape and is scaled with noise_std then adds to q for noise
        p += agnp.random.randn(*p.shape) * self.noise  # creates a random array of size p.shape and is scaled with noise_std then adds to p for noise
        return q, p, dqdt, dpdt, t_eval 
    
    def get_field(self, xmin=-1.2, xmax=1.2, ymin=-1.2, ymax=1.2, gridsize=20):
        field = {'meta': locals()}  # stores a dictionary of key value pairs of all local variables

        b, a = agnp.meshgrid(agnp.linspace(xmin, xmax, gridsize), agnp.linspace(ymin, ymax, gridsize)) # the meshgrid function returns two 2-dimensional arrays
        ys = agnp.stack([b.flatten(), a.flatten()]) # flattens the two 2-dimensional arrays and makes two row vectors which are stacked and stored in ys

        # get vector directions
        dydt = [self.dynamics_fn(None, y) for y in ys.T] # this computes the values of the gradient of the hamiltonian at each row from the transposed ys
        dydt = agnp.stack(dydt).T # stack the computed gradients in dydt as row vectors

        field['x'] = ys.T # convert ys into column vectors and store the values in the key 'x'
        field['dx'] = dydt.T # convert dydt into column vectors and store the values in the key 'dx'
        return field
    
    
    #------------------------------------------------ q and p Stuff Above!!!! ##### q and p Stuff Above!!!! ##### q and p Stuff Above!!!! ----------------------------------------------------#

    def create_noise(self):
        # We will modify this to be our own special
        # noise profile :)
        return super(self).create_noise()

    def create_object(self, time: Union[float, list[float]]):
        assert self.calculation_type == "x position", f"{self.calculation_type} method is not yet implemented, sorry."
        pendulum = self.simulate_pendulum_position(time)
        pendulum += self.create_noise()
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