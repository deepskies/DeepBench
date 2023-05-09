from src.deepbench.physics_object.pendulum import Pendulum

import autograd
import autograd.numpy as agnp
import scipy.integrate.solve_ivp as solve_ivp
from typing import Union


class HamiltonianPendulum(Pendulum):
    def __init__(self,
                 pendulum_arm_length: float,
                 starting_angle_radians: float,
                 noise: float,
                 acceleration_due_to_gravity: Union[float, None] = None,
                 mass_pendulum_bob: Union[float, None] = None
                 ):
        super().__init__(
                        pendulum_arm_length=pendulum_arm_length,
                        starting_angle_radians=starting_angle_radians,
                        noise=noise,
                        acceleration_due_to_gravity=acceleration_due_to_gravity,
                        mass_pendulum_bob=mass_pendulum_bob,
                        )
        self.pendulum_arm_length = pendulum_arm_length
        self.starting_angle_radians = starting_angle_radians
        self.noise = noise
        self.acceleration_due_to_gravity = acceleration_due_to_gravity
        self.mass_pendulum_bob = mass_pendulum_bob

    def hamiltonian_fn(self, coords):
        q, p = agnp.split(coords, 2)
        kinetic_term = ((self.pendulum_arm_length**2) *
                        (p ** 2))/(2*self.mass_pendulum_bob)
        potential_term = (self.mass_pendulum_bob *
                          self.acceleration_due_to_gravity *
                          self.pendulum_arm_length) * (1 - agnp.cos(q))
        H = kinetic_term + potential_term
        return H

    def dynamics_fn(self, t, coords):
        # derives the gradient of the hamiltonian function
        dcoords = autograd.grad(self.hamiltonian_fn)(coords) 
        dqdt, dpdt = agnp.split(dcoords, 2)
        S = agnp.concatenate([dpdt, -dqdt], axis=-1)
        return S

    def simulate_pendulum_dynamics(self, time, **kwargs):
        timescale = 15
        t_eval = agnp.linspace(time[0], time[1],
                               int(timescale * (time[1] - time[0])))

        # get initial state
        if y0 is None:
            y0 = agnp.random.rand(2) * 2. - 1
        if radius is None:
            radius = agnp.random.rand() + 1.3
        y0 = y0 / agnp.sqrt((y0 ** 2).sum()) * radius

        spring_ivp = solve_ivp(fun=self.dynamics_fn, t_span=time, y0=y0, t_eval=t_eval, rtol=1e-10, **kwargs)
        q, p = spring_ivp['y'][0], spring_ivp['y'][1]
        dydt = [self.dynamics_fn(None, y) for y in spring_ivp['y'].T]
        dydt = agnp.stack(dydt).T
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