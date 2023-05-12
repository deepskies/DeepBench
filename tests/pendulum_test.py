import numpy as np
from unittest import TestCase
from src.deepbench.physics_object.pendulum import Pendulum


class TestPendulum(TestCase):
    def test_init(self):
        # make sure people are passing all of
        # the required arguments:
        with self.assertRaises(AssertionError):
            # this raises an error for missing a_g:
            pendulum = Pendulum(pendulum_arm_length=10.,
                            starting_angle_radians=np.pi/4,
                            noise_std_percent=
                            {'pendulum_arm_length': 0.1,
                             'starting_angle_radians': 0.1,
                             'acceleration_due_to_gravity': 0.0}
                            )
            pendulum = Pendulum(pendulum_arm_length=10.,
                            starting_angle_radians=np.pi/4,
                            big_G_newton=10.,
                            noise_std_percent=
                            {'pendulum_arm_length': 0.1,
                             'starting_angle_radians': 0.1,
                             'acceleration_due_to_gravity': 0.0}
                            )

    def test_zero_time(self):
        # it better not produce something
        # when you give it no time
        time = []
        pendulum = Pendulum(pendulum_arm_length=10.,
                            starting_angle_radians=np.pi/4,
                            acceleration_due_to_gravity=9.8,
                            noise_std_percent=
                            {'pendulum_arm_length': 0.1,
                             'starting_angle_radians': 0.1,
                             'acceleration_due_to_gravity': 0.0}
                            )
        output = pendulum.create_object(time)
        self.assertIsNotNone(output, f"output = {output}")
        self.assertEqual(np.shape(time), np.shape(output))

    def test_one_time(self):
        # testing if it produces a one item output
        # when you only give it one moment in time
        time = 0.
        pendulum = Pendulum(pendulum_arm_length=10.,
                            starting_angle_radians=np.pi/4,
                            acceleration_due_to_gravity=9.8,
                            noise_std_percent=
                            {'pendulum_arm_length': 0.1,
                             'starting_angle_radians': 0.1,
                             'acceleration_due_to_gravity': 0.0}
                            )
        output = pendulum.create_object(time)
        self.assertIsNotNone(output)
        self.assertEqual(np.shape(time), np.shape(output))

    def test_array_time(self):
        # output shape better match that of input time
        # when time is an array
        time = np.array(np.linspace(0, 100, 100))
        pendulum = Pendulum(pendulum_arm_length=10.,
                            starting_angle_radians=np.pi/4,
                            acceleration_due_to_gravity=9.8,
                            noise_std_percent=
                            {'pendulum_arm_length': 0.1,
                             'starting_angle_radians': 0.1,
                             'acceleration_due_to_gravity': 0.0}
                            )
        output = pendulum.create_object(time)
        self.assertIsNotNone(output)
        self.assertEqual(np.shape(time), np.shape(output))


'''
    def test_generate_gaussian_noise(self):
        object_params = [{"object_type": "test_object"}]
        image_shape = (14, 14)
        one_image_sky = TimeSeriesImage(object_params, image_shape)
        one_image_sky.combine_objects()
        one_image_sky.generate_noise("gaussian")

        self.assertIsNotNone(one_image_sky.image)
        self.assertEqual(image_shape, one_image_sky.image.shape)

    def test_generate_poisson_noise(self):
        object_params = [{"object_type": "test_object"}]
        image_shape = (14, 14)
        one_image_sky = TimeSeriesImage(object_params, image_shape)
        one_image_sky.combine_objects()
        one_image_sky.generate_noise("poisson")

        self.assertIsNotNone(one_image_sky.image)
        self.assertEqual(image_shape, one_image_sky.image.shape)

    def test_add_fake_noise(self):
        with self.assertRaises(NotImplementedError):
            object_params = [{"object_type": "test_object"}]
            image_shape = (14, 14)
            one_image_sky = TimeSeriesImage(object_params, image_shape)
            one_image_sky.combine_objects()
            one_image_sky.generate_noise("Fake Noise")

    def test_image_not_made(self):
        with self.assertRaises(AssertionError):
            object_params = [{"object_type": "test_object"}]
            image_shape = (14, 14)
            one_image_sky = TimeSeriesImage(object_params, image_shape)

            ##Go straight to noise instead of making objects first
            one_image_sky.generate_noise("gaussian")
'''