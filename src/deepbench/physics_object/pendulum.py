from src.deepbench.physics_object.physics_object import PhysicsObject
import numpy as np
import numpy.random as rand
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from typing import Union, Optional, Tuple


class Pendulum(PhysicsObject):
    def __init__(self,
                 pendulum_arm_length: float,
                 starting_angle_radians: float,
                 noise_std_percent: dict = {'pendulum_arm_length': 0.0,
                                            'starting_angle_radians': 0.0,
                                            'acceleration_due_to_gravity':
                                                None,
                                            'big_G_newton': None,
                                            'phi_planet': None},
                 acceleration_due_to_gravity: Optional[float] = None,
                 big_G_newton: Optional[float] = None,
                 phi_planet: Optional[float] = None,
                 mass_pendulum_bob: Optional[float] = 10.0,
                 coefficient_friction: Optional[float] = 0.0
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
        if acceleration_due_to_gravity is not None and not \
                isinstance(acceleration_due_to_gravity, float):
            raise TypeError("acceleration_due_to_gravity should be a float")

        self.pendulum_arm_length = pendulum_arm_length
        self.starting_angle_radians = starting_angle_radians
        assert self.starting_angle_radians < np.pi, \
            "The angle better not be in degrees or else"
        self.big_G_newton = big_G_newton
        self.phi_planet = phi_planet
        if acceleration_due_to_gravity is None:
            assert self.big_G_newton is not None and self.phi_planet \
                is not None, "must define big_G_newton and phi_planet if \
                    acceleration_due_to_gravity is not provided"
            assert self._noise_level['big_G_newton'] is not None \
                and self._noise_level['phi_planet'] \
                is not None, "must define big_G_newton and phi_planet \
                    noise levels if acceleration_due_to_gravity \
                    is not provided"
            self.acceleration_due_to_gravity = self.big_G_newton * \
                self.phi_planet
            self.initial_parameters = {'pendulum_arm_length':
                                       self.pendulum_arm_length,
                                       'starting_angle_radians':
                                       self.starting_angle_radians,
                                       'acceleration_due_to_gravity':
                                       self.acceleration_due_to_gravity,
                                       'big_G_newton':
                                       self.big_G_newton,
                                       'phi_planet':
                                       self.phi_planet}
        else:
            self.acceleration_due_to_gravity = acceleration_due_to_gravity
            self.initial_parameters = {'pendulum_arm_length':
                                       self.pendulum_arm_length,
                                       'starting_angle_radians':
                                       self.starting_angle_radians,
                                       'acceleration_due_to_gravity':
                                       self.acceleration_due_to_gravity}
        self.mass_pendulum_bob = mass_pendulum_bob
        self.coefficient_friction = coefficient_friction

        # TODO verify the requested noise parameters are variables you can use

        for key, item in noise_std_percent.items():
            assert key in [key for key in self.__dict__.keys()]
            # key is a variable in the class
            assert type(item) in [np.array, float], "not in keys"

    def create_noise(self, seed: int = 42,
                     n_steps: Union[int, Tuple[int, int]] = 10) -> np.array:
        rs = rand.RandomState(seed)
        parameter_map = {
            'pendulum_arm_length': self.pendulum_arm_length,
            'starting_angle_radians': self.starting_angle_radians,
            'acceleration_due_to_gravity': self.acceleration_due_to_gravity,
            'big_G_newton': self.big_G_newton,
            'phi_planet': self.phi_planet
        }

        for key in self._noise_level.keys():
            if key not in parameter_map:
                raise ValueError(f"Invalid parameter name: {key}")

            attribute = parameter_map[key]
            noise_level = self._noise_level[key]

            attribute = rs.normal(
                loc=attribute,
                scale=attribute * noise_level,
                size=n_steps
            )
            setattr(self, key, attribute)
        return

    def destroy_noise(self):
        # Re-modify the global parameters to
        # have the original value
        parameter_map = {
            'pendulum_arm_length': self.pendulum_arm_length,
            'starting_angle_radians': self.starting_angle_radians,
            'acceleration_due_to_gravity': self.acceleration_due_to_gravity,
            'big_G_newton': self.big_G_newton,
            'phi_planet': self.phi_planet
        }
        for key in self._noise_level.keys():
            if key not in parameter_map:
                raise ValueError(f"Invalid parameter name: {key}")
            attribute = self.initial_parameters[key]
            setattr(self, key, attribute)
        '''
        self.pendulum_arm_length = \
            self.initial_parameters['pendulum_arm_length']
        self.starting_angle_radians = \
            self.initial_parameters['starting_angle_radians']
        self.acceleration_due_to_gravity = \
            self.initial_parameters['acceleration_due_to_gravity']
        if self.big_G_newton is not None and self.phi_planet is not None:
            # then you need to also reset these variables
            self.big_G_newton = \
                self.initial_parameters['big_G_newton']
            self.phi_planet = \
                self.initial_parameters['phi_planet']
        '''
        return

    def create_object(self, time: Union[float, np.array],
                      noiseless: bool = False,
                      destroynoise: bool = True,
                      seed: int = 42):
        time = np.asarray(time)
        assert time.size > 0, "you must enter one or more points in time"
        if isinstance(time, (float, int)):
            n_steps = 1
        else:
            time = np.asarray(time)
            n_steps = time.shape
        print('before noise', self.acceleration_due_to_gravity)
        self.create_noise(seed=seed, n_steps=n_steps)
        print('after noise', self.acceleration_due_to_gravity)
        if noiseless:
            self.destroy_noise()
        pendulum = self.simulate_pendulum_dynamics(time)
        if destroynoise:
            self.destroy_noise()
            print('after destroying noise', self.acceleration_due_to_gravity)
        return pendulum

    def simulate_pendulum_dynamics(self, time: Union[float, np.array]):
        assert time.size > 0, "you must enter one or more points in time"
        # Check if parameters are single values or arrays with the same length as time
        if isinstance(self.pendulum_arm_length, (float, int)):
            pendulum_arm_length_values = np.full_like(np.asarray(time), self.pendulum_arm_length)
        else:
            pendulum_arm_length_values = np.asarray(self.pendulum_arm_length)

        if isinstance(self.starting_angle_radians, (float, int)):
            starting_angle_values = np.full_like(np.asarray(time), self.starting_angle_radians)
        else:
            starting_angle_values = np.asarray(self.starting_angle_radians)

        if isinstance(self.acceleration_due_to_gravity, (float, int)):
            acceleration_values = np.full_like(np.asarray(time), self.acceleration_due_to_gravity)
        else:
            acceleration_values = np.asarray(self.acceleration_due_to_gravity)

        # Calculate theta_time based on the parameters
        theta_time = starting_angle_values * np.cos(np.sqrt(acceleration_values / pendulum_arm_length_values))

        # Calculate x using the modified parameters and time
        if isinstance(time, (float, int)):
            x = pendulum_arm_length_values * np.sin(theta_time * time)
        else:
            time = np.asarray(time)
            x = pendulum_arm_length_values * np.sin(theta_time * time)


        '''
        # Check if parameters are single values or arrays with the same length as time
        if isinstance(self.pendulum_arm_length, (float, int)):
            pendulum_arm_length_values = np.full_like(np.asarray(time), self.pendulum_arm_length)
            starting_angle_radians_values = np.full_like(np.asarray(time), self.starting_angle_radians)
            acceleration_due_to_gravity_values = np.full_like(np.asarray(time), self.acceleration_due_to_gravity)
        else:
            pendulum_arm_length_values = np.asarray(self.pendulum_arm_length)
            starting_angle_radians_values = np.asarray(self.starting_angle_radians)
            acceleration_due_to_gravity_values = np.asarray(self.acceleration_due_to_gravity)

        

        # Calculate theta_time based on the parameters
        print(starting_angle_radians_values)
        print(acceleration_due_to_gravity_values)
        print(pendulum_arm_length_values)
        print(time)
        theta_time = starting_angle_radians_values * np.cos(np.sqrt(acceleration_due_to_gravity_values / pendulum_arm_length_values))
        print('theta_time', theta_time)
        # Calculate x using the modified parameters and time
        if isinstance(time, (float, int)):
            x = pendulum_arm_length_values * np.sin(theta_time * time)
        else:
            time = np.asarray(time)
            x = pendulum_arm_length_values * np.sin(theta_time * time)

        # Calculate x using the modified parameters and time
        #x = pendulum_arm_length_values * np.sin(theta_time * time)
        '''
        '''
        theta_time = self.starting_angle_radians * \
            np.cos(np.sqrt(self.acceleration_due_to_gravity /
                           self.pendulum_arm_length))
        x = self.pendulum_arm_length * np.sin(theta_time * time)
        '''
        return x

    def displayObject(self, time: Union[float, np.array]):
        noisy = self.create_object(time, destroynoise=False)
        noise_free = self.create_object(time, destroynoise=True)
        plt.clf()
        plt.plot(time, noisy, color='#EF5D60')
        plt.scatter(time, noisy, label='noisy', color='#EF5D60')
        plt.plot(time, noise_free, color='#E09F7D')
        plt.scatter(time, noise_free, label='noise free', color='#E09F7D')
        plt.legend()
        plt.show()

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
