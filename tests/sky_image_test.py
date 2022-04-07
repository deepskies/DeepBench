from unittest import TestCase
from src.deepbench.image.sky_image import SkyImage


class TestSkyImage(TestCase):
    def test_init(self):
        test_sky = SkyImage([{}], (14, 14))

        self.assertIsNone(test_sky.image)
        self.assertEqual([{}], test_sky.objects)
        self.assertEqual((14, 14), test_sky.image_shape)

    def test_1dim_size(self):
        with self.assertRaises(AssertionError):
            im_shape = (12,)
            SkyImage([{}], im_shape)

    def test_0dim_size(self):
        with self.assertRaises(AssertionError):
            im_shape = ()
            SkyImage([{}], im_shape)

    def test_3dim_size(self):
        im_shape = (14, 14, 3)
        test_sky = SkyImage([{}], im_shape)

        self.assertIsNone(test_sky.image)
        self.assertEqual([{}], test_sky.objects)
        self.assertEqual(im_shape, test_sky.image_shape)

    def test_combine_one_image(self):
        object_params = [{"object_type": "test_object"}]
        image_shape = (14, 14)
        one_image_sky = SkyImage(object_params, image_shape)

        # Not testing that they're the right ones, only that they're made
        one_image_sky.combine_objects()

        self.assertEqual(image_shape, one_image_sky.image.shape)

    def test_combine_2_images(self):
        object_params = [{"object_type": "test_object"}, {"object_type": "test_object"}]
        image_shape = (14, 14)
        one_image_sky = SkyImage(object_params, image_shape)

        # Not testing that they're the right ones, only that they're made
        one_image_sky.combine_objects()

        self.assertEqual(image_shape, one_image_sky.image.shape)

    def test_combine_no_images(self):
        object_params = [{}]
        image_shape = (14, 14)
        one_image_sky = SkyImage(object_params, image_shape)

        # Not testing that they're the right ones, only that they're made
        with self.assertWarns(UserWarning):
            one_image_sky.combine_objects()

        self.assertEqual(image_shape, one_image_sky.image.shape)
        self.assertEqual(0, one_image_sky.image.sum())

    def test_generate_gaussian_noise(self):

        object_params = [{"object_type": "test_object", "object_parameters": {}}]

        image_shape = (14, 14)
        one_image_sky = SkyImage(object_params, image_shape)
        one_image_sky.combine_objects()
        one_image_sky.generate_noise("gaussian")

        self.assertIsNotNone(one_image_sky.image)
        self.assertEqual(image_shape, one_image_sky.image.shape)

    def test_generate_poisson_noise(self):

        object_params = [{"object_type": "test_object", "object_parameters": {}}]

        image_shape = (14, 14)
        one_image_sky = SkyImage(object_params, image_shape)
        one_image_sky.combine_objects()
        one_image_sky.generate_noise("poisson")

        self.assertIsNotNone(one_image_sky.image)
        self.assertEqual(image_shape, one_image_sky.image.shape)

    def test_add_fake_noise(self):
        with self.assertRaises(NotImplementedError):

            object_params = [{"object_type": "test_object", "object_parameters": {}}]

            image_shape = (14, 14)
            one_image_sky = SkyImage(object_params, image_shape)
            one_image_sky.combine_objects()
            one_image_sky.generate_noise("Fake Noise")

    def test_image_not_made(self):
        with self.assertRaises(AssertionError):

            object_params = [{"object_type": "test_object", "object_parameters": {}}]

            image_shape = (14, 14)
            one_image_sky = SkyImage(object_params, image_shape)

            ##Go straight to noise instead of making objects first
            one_image_sky.generate_noise("gaussian")
