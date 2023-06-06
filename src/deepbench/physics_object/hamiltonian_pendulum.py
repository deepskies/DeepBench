from src.deepbench.physics_object.pendulum import Pendulum

import autograd
import autograd.numpy as np
from scipy.integrate import solve_ivp
from typing import Union, Optional


class HamiltonianPendulum(Pendulum):
    def __init__(
        self,
        pendulum_arm_length: float,
        starting_angle_radians: float,
        acceleration_due_to_gravity: Union[float, None] = None,
        mass_pendulum_bob: Optional[float] = 10.0,
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

    def hamiltonian_fn(self, coords, m, L, g):
        q, p = np.split(coords, 2)
        # m = self.mass_pendulum_bob
        # L = self.pendulum_arm_length
        # g = self.acceleration_due_to_gravity
        # kinetic_term = ((self.pendulum_arm_length**2) * (p**2)) / (
        #     2 * self.mass_pendulum_bob
        # )
        # potential_term = (
        #     self.mass_pendulum_bob
        #     * self.acceleration_due_to_gravity
        #     * self.pendulum_arm_length
        # ) * (1 - np.cos(q))
        # H = kinetic_term + potential_term
        H = (m * g * L) * (1 - np.cos(q)) + ((L**2) * (p**2)) / (2 * m)
        return H

    def dynamics_fn(self, t, coords):
        # derives the gradient of the hamiltonian function
        # print(f'mass: {self.mass_pendulum_bob} length: {self.pendulum_arm_length} g: {self.acceleration_due_to_gravity}')
        dcoords = autograd.grad(self.hamiltonian_fn)(
            coords,
            self.mass_pendulum_bob,
            self.pendulum_arm_length,
            self.acceleration_due_to_gravity,
        )

        # dcoords = autograd.grad(self.hamiltonian_fn)(coords, 2, 10, 9.8)
        dqdt, dpdt = np.split(dcoords, 2)
        S = np.concatenate([dpdt, -dqdt], axis=-1)
        return S

    def create_object(self, time, noiseless=True):
        assert noiseless
        return super().create_object(time, noiseless)

    def simulate_pendulum_dynamics(self, time, **kwargs):
        assert time.size > 1, "you must enter more than one point in time"

        t_eval = np.array(time)
        t_span = np.array([time[0], time[-1]])

        radius = np.random.rand() + 1.3

        # get initial state
        if self.starting_angle_radians is None:
            self.starting_angle_radians = np.random.rand(2) * 2.0 - 1

        y0 = np.array([2, 0])
        y0 = y0 / np.sqrt((y0**2).sum()) * radius

        spring_ivp = solve_ivp(
            fun=self.dynamics_fn,
            t_span=t_span,
            y0=y0,
            t_eval=t_eval,
            rtol=1e-10,
            **kwargs
        )
        q, p = spring_ivp["y"][0], spring_ivp["y"][1]
        dydt = [self.dynamics_fn(None, y) for y in spring_ivp["y"].T]
        dydt = np.stack(dydt).T
        dqdt, dpdt = np.split(dydt, 2)  # split the dydt into dqdt and dpdt

        # add noise
        noise_std = 0.1
        q += (
            np.random.randn(*q.shape) * noise_std
        )  # creates a random array of size q.shape and is scaled with noise_std then adds to q for noise
        p += (
            np.random.randn(*p.shape) * noise_std
        )  # creates a random array of size p.shape and is scaled with noise_std then adds to p for noise
        return q, p, dqdt, dpdt, t_eval

    def get_field(self, xmin=-1.2, xmax=1.2, ymin=-1.2, ymax=1.2, gridsize=20):
        """get_field() is used to visualize the the gradiant vector field."""
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
