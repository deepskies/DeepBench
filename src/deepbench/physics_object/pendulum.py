from src.deepbench.physics_object.physics_object import PhysicsObject
import numpy as np
import numpy.random as rand
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from typing import Union, Optional, Tuple
import logging
import os


class Pendulum(PhysicsObject):
    def __init__(
        self,
        pendulum_arm_length: float,
        starting_angle_radians: float,
        noise_std_percent: dict = {
            "pendulum_arm_length": 0.0,
            "starting_angle_radians": 0.0,
            "acceleration_due_to_gravity": 0.0,
            "big_G_newton": None,
            "phi_planet": None,
        },
        acceleration_due_to_gravity: Optional[float] = None,
        big_G_newton: Optional[float] = None,
        phi_planet: Optional[float] = None,
        mass_pendulum_bob: Optional[float] = 10.0,
        coefficient_friction: Optional[float] = 0.0,
    ):
        """
        The initialization function for the Pendulum class.

        Args:
            pendulum_arm_length (float): The length of the pendulum arm
            starting_angle_radians (float): The starting angle of the pendulum
                (angle from the 'ceiling')
            noise_std_percent (dict): A dictionary of the Gaussian noise
                level to be applied to each parameter. The default is no
                noise. Each number is the standard deviation when
                multiplied by the parameter. See create_noise().
            acceleration_due_to_gravity (float): little g, local gravity
                coefficient, optional if G and phi are defined,
                g = G * phi
            big_G_newton (float): Big G, the gravitational constant,
                optional if g is defined
            phi_planet (float): M/r^2, this changes based on the planet,
                optional if g is defined
            mass_pendulum_bob (float): Mass of the pendulum bob,
                this is optional if calculation_type is position only.
            coefficient_friction (float): Coefficient of friction,
                optional argument.

        Examples:

            >>> pendulum_obj = Pendulum(pendulum_arm_length=10.,
                                        starting_angle_radians=np.pi/4,
                                        acceleration_due_to_gravity=9.8,
                                        noise_std_percent=
                                        {'pendulum_arm_length': 0.1,
                                         'starting_angle_radians': 0.1,
                                         'acceleration_due_to_gravity': 0.1}
                                        )
        """
        super().__init__(
            noise_level=noise_std_percent,
        )
        if acceleration_due_to_gravity is not None and not isinstance(
            acceleration_due_to_gravity, float
        ):
            raise TypeError("acceleration_due_to_gravity should be a float")

        self.pendulum_arm_length = pendulum_arm_length
        self.starting_angle_radians = starting_angle_radians
        assert (
            self.starting_angle_radians < np.pi
        ), "The angle better not be in degrees or else"
        self.big_G_newton = big_G_newton
        self.phi_planet = phi_planet
        if acceleration_due_to_gravity is None:
            assert (
                self.big_G_newton is not None and self.phi_planet is not None
            ), "must define big_G_newton and phi_planet if \
                    acceleration_due_to_gravity is not provided"
            # assert self._noise_level['big_G_newton'] is not None \
            #    and self._noise_level['phi_planet'] \
            #    is not None, "must define big_G_newton and phi_planet \
            #        noise levels if acceleration_due_to_gravity \
            #        is not provided"
            self.acceleration_due_to_gravity = self.big_G_newton * self.phi_planet
            self.initial_parameters = {
                "pendulum_arm_length": self.pendulum_arm_length,
                "starting_angle_radians": self.starting_angle_radians,
                "acceleration_due_to_gravity": self.acceleration_due_to_gravity,
                "big_G_newton": self.big_G_newton,
                "phi_planet": self.phi_planet,
            }
        else:
            self.acceleration_due_to_gravity = acceleration_due_to_gravity
            self.initial_parameters = {
                "pendulum_arm_length": self.pendulum_arm_length,
                "starting_angle_radians": self.starting_angle_radians,
                "acceleration_due_to_gravity": self.acceleration_due_to_gravity,
            }
        self.mass_pendulum_bob = mass_pendulum_bob
        self.coefficient_friction = coefficient_friction

        # Verify the requested noise parameters are variables you can use
        for key, item in noise_std_percent.items():
            assert key in [key for key in self.__dict__.keys()]
        # If the acceleration_due_to_gravity is None,
        # then the accompanying noise parameter also needs to be none
        # otherwise the noise module will be confused
        # about if we're doing the hierarchical case
        if acceleration_due_to_gravity is None:
            assert (
                noise_std_percent["acceleration_due_to_gravity"] is None
            ), "if acceleration due to gravity is not defined (None) then \
                the accompanying noise term must be None as well so that \
                the noise model knows this is the hierarchical case"

        # Finally define the parameter map used to later modify parameters
        # in create_noise and destroy_noise:
        self.parameter_map = {
            "pendulum_arm_length": self.pendulum_arm_length,
            "starting_angle_radians": self.starting_angle_radians,
            "acceleration_due_to_gravity": self.acceleration_due_to_gravity,
            "big_G_newton": self.big_G_newton,
            "phi_planet": self.phi_planet,
        }
        # create logger to store the random seeds generated by noise
        # Erase log if already exists:
        log_file = "randomseeds.log"
        if os.path.exists(log_file):
            os.remove(log_file)
        # this will overwrite logger each time a new pendulum class
        # is initialized
        logger = logging.getLogger("randomseeds")
        logger.setLevel(logging.DEBUG)
        # create file handler which logs even debug messages
        fh = logging.FileHandler("randomseeds.log")
        logger.addHandler(fh)
        self.logfile = logger

    def create_noise(
        self,
        noiseless: bool = False,
        seed: int = None,
        n_steps: Union[int, Tuple[int, int]] = 10,
        verbose: bool = False,
    ) -> np.array:
        """
        Creates noise on top of simulate_pendulum_dynamics
        Also deals with the hierarchical case, where
        acceleration_due_to_gravity is defined via
        big_G_newton and phi_planet

        Args:
            seed (int): Random seed used to generate Gaussian noise
            n_steps (int or Tuple[int,int]): The shape of the noise to be
                created. This is specified in create_object using the shape
                of the input time array (or float).

        Examples (see create_object)
        """
        if seed:
            rs = rand.RandomState(seed)
        else:
            rs = rand.RandomState()
        # Save the random state only if noisy
        if noiseless is False:
            self.logfile.info(str(rs.get_state()[1][0]))
        for key in self._noise_level.keys():
            if key not in self.parameter_map:
                raise ValueError(f"Invalid parameter name: {key}")

            attribute = self.parameter_map[key]
            noise_level = self._noise_level[key]
            if verbose:
                print("key", key, "attribute", attribute, "noise level", noise_level)
            if noise_level is not None:
                attribute = rs.normal(
                    loc=attribute, scale=attribute * noise_level, size=n_steps
                )
                setattr(self, key, attribute)
        # Now, if this is the hierarchical case, we can redefine
        # the acceleration_due_to_gravity term
        if self._noise_level["acceleration_due_to_gravity"] is None:
            assert (
                self.big_G_newton is not None and self.phi_planet is not None
            ), "must define big_G_newton and phi_planet if \
                    acceleration_due_to_gravity is not provided"
            if self._noise_level["big_G_newton"] is not None:
                self.big_G_newton = rs.normal(
                    loc=self.big_G_newton,
                    scale=self.big_G_newton * self._noise_level["big_G_newton"],
                    size=n_steps,
                )
            if self._noise_level["phi_planet"] is not None:
                self.phi_planet = rs.normal(
                    loc=self.phi_planet,
                    scale=self.phi_planet * self._noise_level["phi_planet"],
                    size=n_steps,
                )
            # redefine:
            # acceleration_due_to_gravity = multiple of noisy G and phi
            if self.big_G_newton is not None and self.phi_planet is not None:
                self.acceleration_due_to_gravity = self.big_G_newton * self.phi_planet
            else:
                assert f"Either big G or phi_planet is None \
                    (G = {self.big_G_newton}, ø = {self.phi_planet}); \
                        this is not allowed with hierarchical noise"
        return

    def destroy_noise(self):
        # Re-modify the global parameters to
        # have the original value
        for key in self._noise_level.keys():
            if key not in self.parameter_map:
                raise ValueError(f"Invalid parameter name: {key}")
            attribute = self.initial_parameters[key]
            setattr(self, key, attribute)
        return

    def create_object(
        self,
        time: Union[float, np.array],
        noiseless: bool = False,
        seed: int = None,
        verbose: bool = False,
    ):
        """
        Given a single or array of times, simulates the pendulum position at
        each of these times and optionally adds Gaussian noise to each
        parameter.

        Args:
            time (Union[float, np.array]): A single moment in time, or
                an array of times (s)
            noiseless (bool): Enables a noise realization if True.
                Default is set to False
            seed (int): Random seed used to generate Gaussian noise

        Example:
            >>> pendulum = Pendulum(...SEE ABOVE...)
            >>> time = np.array(np.linspace(0, 10, 20))
            >>> pend_position = pendulum.create_object(time, noiseless=True)
        """
        time = np.asarray(time)
        assert time.size > 0, "you must enter one or more points in time"
        if isinstance(time, (float, int)):
            n_steps = 1
        else:
            time = np.asarray(time)
            n_steps = time.shape
        self.create_noise(seed=seed, noiseless=noiseless, n_steps=n_steps)
        if noiseless:
            self.destroy_noise()
        pendulum = self.simulate_pendulum_dynamics(time)
        self.destroy_noise()
        return pendulum

    def simulate_pendulum_dynamics(self, time: Union[float, np.array]):
        time = np.asarray(time)
        assert time.size > 0, "you must enter one or more points in time"
        # Check if parameters are single values
        # or arrays with the same length as time
        if isinstance(self.pendulum_arm_length, (float, int)):
            pendulum_arm_length_values = np.full_like(
                np.asarray(time), self.pendulum_arm_length
            )
        else:
            pendulum_arm_length_values = np.asarray(self.pendulum_arm_length)

        if isinstance(self.starting_angle_radians, (float, int)):
            starting_angle_values = np.full_like(
                np.asarray(time), self.starting_angle_radians
            )
        else:
            starting_angle_values = np.asarray(self.starting_angle_radians)

        if isinstance(self.acceleration_due_to_gravity, (float, int)):
            acceleration_values = np.full_like(
                np.asarray(time), self.acceleration_due_to_gravity
            )
        else:
            acceleration_values = np.asarray(self.acceleration_due_to_gravity)

        # Calculate theta_time based on the parameters
        assert (
            acceleration_values.any() > 0
        ), "f{acceleration_values} not greater than zero"
        assert (
            pendulum_arm_length_values.any() > 0
        ), "f{pendulum_arm_length_values} not greater than zero"
        theta_time = starting_angle_values * np.cos(
            np.sqrt(acceleration_values / pendulum_arm_length_values)
        )

        # Calculate x using the modified parameters and time
        return pendulum_arm_length_values * np.sin(theta_time * time)

    def displayObject(self, time: Union[float, np.array]):
        noisy = self.create_object(time)
        noise_free = self.create_object(time, noiseless=True)
        plt.clf()
        plt.plot(time, noisy, color="#EF5D60")
        plt.scatter(time, noisy, label="noisy", color="#EF5D60")
        plt.plot(time, noise_free, color="#0E131F")
        plt.scatter(time, noise_free, label="noise free", color="#0E131F")
        plt.legend()
        plt.show()

        # plot multiple noise draws and show the standard
        # deviation:
        noise_free = self.create_object(time, noiseless=True)
        plt.clf()
        num_random = 10
        noisy_ys = np.zeros((num_random, len(time)))
        for i in range(num_random):
            noisy = self.create_object(time)
            noisy_ys[i, :] = noisy
        ci_list = [np.std(abs(noisy_ys[:, t])) for t, _ in enumerate(time)]
        plt.fill_between(
            time,
            (noise_free - ci_list),
            (noise_free + ci_list),
            color="#EF5D60",
            alpha=0.5,
            edgecolor="None",
        )
        plt.plot(time, noise_free, color="#0E131F", zorder=100)
        plt.scatter(time, noise_free, label="noise free", color="#0E131F", zorder=100)
        plt.legend()
        plt.ylabel("x position")
        plt.xlabel("time [s]")
        plt.show()
        return noise_free, noisy_ys

    """
    def animateObject(self, time: Union[float, np.array]):
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
        if isinstance(time, float):
            time = [time]
        anim = FuncAnimation(fig, update,
                             frames=range(1, len(time)),
                             interval=100)
        plt.show(anim)
        return
    """
