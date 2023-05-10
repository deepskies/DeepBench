import numpy as np
from unittest import TestCase
from src.deepbench.physics_object.pendulum import Pendulum


class TestPendulum(TestCase):
    def test_1d_init(self):
        with self.assertRaises(AssertionError):
            time = [0.]
            self.assertIsNone(Pendulum(pendulum_arm_length=10.,
                                       starting_angle_radians=np.pi/4,
                                       acceleration_due_to_gravity=9.8,
                                       noise_std_percent=
                                       {'pendulum_arm_length': 0.1,
                                        'starting_angle_radians': 0.1}
                                       )).create_object(time)

            '''
            pend_noisy = pend.create_object(time)
            pend_noise_free = pend.simulate_pendulum_dynamics(time)
            pend.displayObject(time)
            print(pend)
            '''

            '''
            {"pendulum_arm_length": 10,
                            "starting_angle_radians": np.pi/4,
                            "noise": 0}
            test_sky = SkyImage([{}], (14, 14))

        self.assertIsNone(test_sky.image)
        self.assertEqual([{}], test_sky.objects)
        self.assertEqual((14, 14), test_sky.image_shape)'''
'''
    def test_2d_init(self):
        image_shape = (12, 12)
        object_params = [{"object_type": "test_object"}]
        time_series = TimeSeriesImage(object_params, image_shape)

        self.assertEqual(image_shape, time_series.image_shape)

    def test_0d_init(self):
        with self.assertRaises(AssertionError):
            image_shape = ()
            object_params = [{"object_type": "test_object"}]
            TimeSeriesImage(object_params, image_shape)

    def test_no_object_init(self):
        with self.assertRaises(AssertionError):
            image_shape = (12, 12)
            object_params = []
            TimeSeriesImage(object_params, image_shape)

    def test_one_object_init(self):
        image_shape = (12, 12)
        object_params = [{"object_type": "test_object"}]
        time_series = TimeSeriesImage(object_params, image_shape)

        self.assertEqual(image_shape, time_series.image_shape)
        self.assertEqual(object_params, time_series.objects)

    def test_two_object_init(self):
        with self.assertRaises(AssertionError):
            image_shape = (12, 12)
            object_params = [
                {"object_type": "test_object"},
                [{"object_type": "test_object"}],
            ]
            TimeSeriesImage(object_params, image_shape)

    def test_combine_one_object(self):
        image_shape = (12, 12)
        object_params = [{"object_type": "test_object"}]
        time_series = TimeSeriesImage(object_params, image_shape)
        time_series.combine_objects()

        self.assertEqual(image_shape, time_series.image.shape)

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