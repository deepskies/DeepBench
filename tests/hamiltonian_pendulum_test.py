import numpy as np
import pytest
from unittest import TestCase
from deepbench.physics_object import HamiltonianPendulum


class TestHamiltonianPendulum(TestCase):
    def test_init(self):
        # make sure people are passing all of
        # the required arguments:
        with self.assertRaises(AssertionError):
            # this raises an error for missing a_g:
            HamiltonianPendulum(
                pendulum_arm_length=10.0,
                starting_angle_radians=np.pi / 4,
                noise_std_percent={
                    "pendulum_arm_length": 0.1,
                    "starting_angle_radians": 0.1,
                    "acceleration_due_to_gravity": 0.0,
                },
            )

        # better raise an error if angle is too big
        with self.assertRaises(AssertionError):
            HamiltonianPendulum(
                pendulum_arm_length=10.0,
                starting_angle_radians=45,
                acceleration_due_to_gravity=10.0,
                noise_std_percent={
                    "pendulum_arm_length": 0.1,
                    "starting_angle_radians": 0.1,
                    "acceleration_due_to_gravity": 0.0,
                },
            )

        # raise error if missing required noise arg
        with self.assertRaises(AssertionError):
            HamiltonianPendulum(
                pendulum_arm_length=10.0,
                starting_angle_radians=2 * np.pi,
                acceleration_due_to_gravity=10.0,
                noise_std_percent={
                    "pendulum_arm_length": 0.1,
                    "starting_angle_radians": 0.1,
                },
            )
        # raise error if misspelled required noise arg
        with self.assertRaises(AssertionError):
            HamiltonianPendulum(
                pendulum_arm_length=10.0,
                starting_angle_radians=np.pi / 4,
                acceleration_due_to_gravity=10.0,
                noise_std_percent={
                    "ppendulum_arm_length": 0.1,
                    "starting_angle_radians": 0.1,
                    "acceleration_due_to_gravity": 0.0,
                },
            )

    def test_array_input_args(self):
        with self.assertRaises(TypeError):
            HamiltonianPendulum(
                pendulum_arm_length=10.0,
                starting_angle_radians=np.pi / 4,
                acceleration_due_to_gravity=[10.0, 11.0],
                noise_std_percent={
                    "pendulum_arm_length": 0.1,
                    "starting_angle_radians": 0.1,
                    "acceleration_due_to_gravity": 0.0,
                },
            )

    def test_zero_time(self):
        # it better not produce something
        # when you give it no time
        time = []
        with self.assertRaises(AssertionError):
            pendulum = HamiltonianPendulum(
                pendulum_arm_length=10.0,
                starting_angle_radians=np.pi / 4,
                acceleration_due_to_gravity=9.8,
                noise_std_percent={
                    "pendulum_arm_length": 0.1,
                    "starting_angle_radians": 0.1,
                    "acceleration_due_to_gravity": 0.0,
                },
            )
            pendulum.create_object(time)

    def test_one_time(self):
        with pytest.raises(AssertionError):
            # testing if it produces a one item output
            # when you only give it one moment in time
            time = 0.0
            pendulum = HamiltonianPendulum(
                pendulum_arm_length=10.0,
                starting_angle_radians=np.pi / 4,
                acceleration_due_to_gravity=9.8,
                noise_std_percent={
                    "pendulum_arm_length": 0.5,
                    "starting_angle_radians": 0.5,
                    "acceleration_due_to_gravity": 0.5,
                },
            )
            pendulum.create_object(time)
            # self.assertIsNotNone(output)
            # self.assertEqual(np.shape(time), np.shape(output))

    # @pytest.mark.skip(reason="Noise not included for gradients")
    def test_array_time(self):
        # output shape better match that of input time
        # when time is an array
        time = np.linspace(0, 3, 45)
        pendulum = HamiltonianPendulum(
            pendulum_arm_length=10.0,
            starting_angle_radians=np.pi / 4,
            acceleration_due_to_gravity=9.8,
            noise_std_percent={
                "pendulum_arm_length": 0.1,
                "starting_angle_radians": 0.1,
                "acceleration_due_to_gravity": 0.0,
            },
        )
        q, p, dqdt, dpdt, t_eval = pendulum.create_object(time)
        # [var is not None for var in [q, p, dqdt, dpdt, t_eval]]
        for var in [q, p, dqdt, dpdt, t_eval]:
            assert var.any() != None
            self.assertEqual(np.shape(time), np.shape(np.squeeze(var)))

    """
    def test_noise_one_time(self):
        # does noise work
        time = 0.
        pendulum = Pendulum(pendulum_arm_length=10.,
                            starting_angle_radians=np.pi/4,
                            acceleration_due_to_gravity=9.8,
                            noise_std_percent=
                            {'pendulum_arm_length': 0.5,
                             'starting_angle_radians': 0.5,
                             'acceleration_due_to_gravity': 0.5}
                            )
        out1 = pendulum.create_object(time)
        out2 = pendulum.create_object(time, destroynoise=False)
        print('out1', out1)
        print('out2', out2)
        assert out1 != out2, "not equal"
        pendulum.displayObject(time, destroynoise=False)
        #self.assertIsNotNone(output)
        #self.assertEqual(np.shape(time), np.shape(output))
        pendulum.displayObject(time, destroynoise=True,)
    """

    @pytest.mark.skip(reason="Noise not included for gradients")
    def test_noise_array(self):
        # does noise work for an array of times?
        time = np.array(np.linspace(0, 10, 20))
        pendulum = HamiltonianPendulum(
            pendulum_arm_length=10.0,
            starting_angle_radians=np.pi / 4,
            acceleration_due_to_gravity=9.8,
            noise_std_percent={
                "pendulum_arm_length": 0.0,
                "starting_angle_radians": 0.1,
                "acceleration_due_to_gravity": 0.1,
            },
        )
        # pendulum.displayObject(time)
        q, p, dqdt, dpdt, t_eval = pendulum.create_object(time, noiseless=False)
        q_noise, p_noise, dqdt_noise, dpdt_noise, t_eval_noise = pendulum.create_object(
            time, noiseless=True
        )
        # [var is not None for var in [q, p, dqdt, dpdt, t_eval]]
        for var in [
            q,
            p,
            dqdt,
            dpdt,
            t_eval,
            q_noise,
            p_noise,
            dqdt_noise,
            dpdt_noise,
            t_eval_noise,
        ]:
            assert var.any() != None
            self.assertEqual(np.shape(time), np.shape(np.squeeze(var)))


"""
    def test_noise_hierarchical(self):
        # does noise work for an array of times?
        time = np.array(np.linspace(0, 10, 20))
        pendulum = HamiltonianPendulum(
            pendulum_arm_length=10.0,
            starting_angle_radians=np.pi / 4,
            acceleration_due_to_gravity=None,
            big_G_newton=10.0,
            phi_planet=1.0,
            noise_std_percent={
                "pendulum_arm_length": 0.0,
                "starting_angle_radians": 0.1,
                "acceleration_due_to_gravity": None,
                "big_G_newton": 0.0,
                "phi_planet": 0.0,
            },
        )
        # pendulum.displayObject(time)
        pendulum_noisy = pendulum.create_object(time, noiseless=False)
        pendulum_noiseless = pendulum.create_object(time, noiseless=True)
        assert len(pendulum_noisy) == len(pendulum_noiseless) == len(time)
        assert pendulum_noisy.any() == pendulum_noiseless.any()


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
"""
