from src.deepbench.physics_object.pendulum import Pendulum

import autograd
import autograd.numpy as np
import scipy.integrate.solve_ivp as solve_ivp
from typing import Union


class HamiltonianPendulum(Pendulum):
    def __init__(
        self,
        pendulum_arm_length: float,
        starting_angle_radians: float,
        acceleration_due_to_gravity: Union[float, None] = None,
        mass_pendulum_bob: Union[float, None] = None,
        noise_std_percent: dict = {
            "pendulum_arm_length": 0.0,
            "starting_angle_radians": 0.0,
            "mass_pendulum_bob": 0.0,
            "acceleration_due_to_gravity": None,
        },
    ):
        """
        The initialization function for the Hamiltonian Pendulum class.

        Args:
            pendulum_arm_length (float): The length of the pendulum arm
            starting_angle_radians (float): The starting angle of the pendulum
                (angle from the 'ceiling')
            noise_std_percent (dict): A dictionary of the Gaussian noise
                level to be applied to each parameter. The default is no
                noise. Each number is the standard deviation when
                multiplied by the parameter. See create_noise().
            acceleration_due_to_gravity (float): little g, local gravity
                coefficient
            mass_pendulum_bob (float): Mass of the pendulum bob,
                this is optional if calculation_type is position only.

        Examples:

            >>> pendulum_obj = HamiltonianPendulum(pendulum_arm_length=10.,
                                        starting_angle_radians=np.pi/4,
                                        acceleration_due_to_gravity=9.8,
                                        noise_std_percent=
                                        {'pendulum_arm_length': 0.1,
                                         'starting_angle_radians': 0.1,
                                         'acceleration_due_to_gravity': 0.1}
                                        )
        """
        super().__init__(
            pendulum_arm_length=pendulum_arm_length,
            starting_angle_radians=starting_angle_radians,
            noise_std_percent=noise_std_percent,
            acceleration_due_to_gravity=acceleration_due_to_gravity,
            mass_pendulum_bob=mass_pendulum_bob,
        )

    def hamiltonian_fn(self, coords):
        q, p = np.split(coords, 2)
        kinetic_term = ((self.pendulum_arm_length**2) * (p**2)) / (
            2 * self.mass_pendulum_bob
        )
        potential_term = (
            self.mass_pendulum_bob
            * self.acceleration_due_to_gravity
            * self.pendulum_arm_length
        ) * (1 - np.cos(q))
        H = kinetic_term + potential_term
        return H

    def dynamics_fn(self, t, coords):
        # derives the gradient of the hamiltonian function
        dcoords = autograd.grad(self.hamiltonian_fn)(coords)
        dqdt, dpdt = np.split(dcoords, 2)
        S = np.concatenate([dpdt, -dqdt], axis=-1)
        return S

    def simulate_pendulum_dynamics(self, time):
        t_eval = np.linspace(time[0], time[1], int(15 * (time[1] - time[0])))

        radius = np.random.rand() + 1.3

        # get initial state
        if self.starting_angle_radians is None:
            self.starting_angle_radians = np.random.rand(2) * 2.0 - 1

        y0 = (
            self.starting_angle_radians
            / np.sqrt((self.starting_angle_radians**2).sum())
            * radius
        )

        spring_ivp = solve_ivp(
            fun=self.dynamics_fn, t_span=time, y0=y0, t_eval=t_eval, rtol=1e-10
        )
        q, p = spring_ivp["y"][0], spring_ivp["y"][1]
        dydt = [self.dynamics_fn(None, y) for y in spring_ivp["y"].T]
        dydt = np.stack(dydt).T
        dqdt, dpdt = np.split(dydt, 2)  # split the dydt into dqdt and dpdt

        return q, p, dqdt, dpdt, t_eval

    "get_field() is used to visualize the the gradiant vector field."

    def get_field(self, xmin=-1.2, xmax=1.2, ymin=-1.2, ymax=1.2, gridsize=20):
        field = {"meta": locals()}

        b, a = np.meshgrid(
            np.linspace(xmin, xmax, gridsize), np.linspace(ymin, ymax, gridsize)
        )
        ys = np.stack([b.flatten(), a.flatten()])

        # get vector directions
        dydt = [self.dynamics_fn(None, y) for y in ys.T]
        dydt = np.stack(dydt).T
        field["x"] = ys.T
        field["dx"] = dydt.T
        return field
