from src.deepbench.physics_object.pendulum import Pendulum

import autograd
import autograd.numpy as np
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

    def hamiltonian_fn(self, coords):
        q, p = np.split(coords, 2)
        kinetic_term = ((self.pendulum_arm_length**2) *
                        (p ** 2))/(2*self.mass_pendulum_bob)
        potential_term = (self.mass_pendulum_bob *
                          self.acceleration_due_to_gravity *
                          self.pendulum_arm_length) * (1 - np.cos(q))
        H = kinetic_term + potential_term
        return H

    def dynamics_fn(self, t, coords):
        # derives the gradient of the hamiltonian function
        dcoords = autograd.grad(self.hamiltonian_fn)(coords)
        dqdt, dpdt = np.split(dcoords, 2)
        S = np.concatenate([dpdt, -dqdt], axis=-1)
        return S

    def simulate_pendulum_dynamics(self, time):
        t_eval = np.linspace(time[0], time[1],
                             int(15 * (time[1] - time[0])))

        radius = np.random.rand() + 1.3

        # get initial state
        if self.starting_angle_radians is None:
            self.starting_angle_radians = np.random.rand(2) * 2. - 1

        y0 = self.starting_angle_radians / np.sqrt(
            (self.starting_angle_radians ** 2).sum()) * radius

        spring_ivp = solve_ivp(fun=self.dynamics_fn, t_span=time, y0=y0,
                               t_eval=t_eval, rtol=1e-10)
        q, p = spring_ivp['y'][0], spring_ivp['y'][1]
        dydt = [self.dynamics_fn(None, y) for y in spring_ivp['y'].T]
        dydt = np.stack(dydt).T
        dqdt, dpdt = np.split(dydt, 2)  # split the dydt into dqdt and dpdt

        return q, p, dqdt, dpdt, t_eval

    def get_field(self, xmin=-1.2, xmax=1.2, ymin=-1.2, ymax=1.2, gridsize=20):
        field = {'meta': locals()}

        b, a = np.meshgrid(np.linspace(xmin, xmax, gridsize),
                           np.linspace(ymin, ymax, gridsize))
        ys = np.stack([b.flatten(), a.flatten()])

        # get vector directions
        dydt = [self.dynamics_fn(None, y) for y in ys.T]
        dydt = np.stack(dydt).T
        field['x'] = ys.T
        field['dx'] = dydt.T
        return field