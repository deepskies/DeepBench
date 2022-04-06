from unittest import TestCase
from src.deepbench.image.sky_image import SkyImage

from src.deepbench import astro_object


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
        object_params = [{"type": "star"}]
        image_shape = (14, 14)
        one_image_sky = SkyImage(object_params, image_shape)

        # Not testing that they're the right ones, only that they're made
        one_image_sky.combine_objects()

        self.assertEqual(image_shape, one_image_sky.image.shape)

    def test_combine_2_images(self):
        object_params = [{"object_type": "star"}, {"object_type": "star"}]
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
        one_image_sky.combine_objects()

        self.assertEqual(image_shape, one_image_sky.image.shape)
        self.assertEqual(0, one_image_sky.image.sum())

    # def test_generate_astro_object_star(self):
    #     object_params = [{}]
    #     image_shape = (14, 14)
    #     one_image_sky = SkyImage(object_params, image_shape)
    #     obj = one_image_sky._generate_astro_object("star")
    #
    #     self.assertIsInstance(obj, astro_object.Star)
    #
    # def test_generate_astro_object_strong_lens(self):
    #     object_params = [{}]
    #     image_shape = (14, 14)
    #     one_image_sky = SkyImage(object_params, image_shape)
    #     obj = one_image_sky._generate_astro_object("strong_lens")
    #
    #     self.assertIsInstance(obj, astro_object.StrongLens)
    #
    # def test_generate_galaxy_object(self):
    #     object_params = [{}]
    #     image_shape = (14, 14)
    #     one_image_sky = SkyImage(object_params, image_shape)
    #     obj = one_image_sky._generate_astro_object("galaxy")
    #
    #     self.assertIsInstance(obj, astro_object.Galaxy)
    #
    # def test_generate_spiral_galaxy_object(self):
    #     object_params = [{}]
    #     image_shape = (14, 14)
    #     one_image_sky = SkyImage(object_params, image_shape)
    #     obj = one_image_sky._generate_astro_object("spiral_galaxy")
    #
    #     self.assertIsInstance(obj, astro_object.SpiralGalaxy)
    #
    # def test_generate_n_body_object(self):
    #     object_params = [{}]
    #     image_shape = (14, 14)
    #     one_image_sky = SkyImage(object_params, image_shape)
    #     obj = one_image_sky._generate_astro_object("n_body")
    #
    #     self.assertIsInstance(obj, astro_object.NBody)
    #
    # def test_not_included_object(self):
    #     with self.assertRaises(NotImplementedError):
    #         object_params = [{}]
    #         image_shape = (14, 14)
    #         one_image_sky = SkyImage(object_params, image_shape)
    #         one_image_sky._generate_astro_object("Fake Object")

    def test_generate_gaussian_noise(self):
        object_params = [{}]
        image_shape = (14, 14)
        one_image_sky = SkyImage(object_params, image_shape)
        one_image_sky.combine_objects()
        one_image_sky.generate_noise("gaussian")

        self.assertIsNotNone(one_image_sky.image)
        self.assertEqual(image_shape, one_image_sky.image.shape)

    def test_generate_poisson_noise(self):
        object_params = [{}]
        image_shape = (14, 14)
        one_image_sky = SkyImage(object_params, image_shape)
        one_image_sky.combine_objects()
        one_image_sky.generate_noise("poisson")

        self.assertIsNotNone(one_image_sky.image)
        self.assertEqual(image_shape, one_image_sky.image.shape)

    def test_add_fake_noise(self):
        with self.assertRaises(NotImplementedError):
            object_params = [{}]
            image_shape = (14, 14)
            one_image_sky = SkyImage(object_params, image_shape)
            one_image_sky.combine_objects()
            one_image_sky.generate_noise("Fake Noise")

    def test_image_not_made(self):
        with self.assertRaises(AssertionError):
            object_params = [{}]
            image_shape = (14, 14)
            one_image_sky = SkyImage(object_params, image_shape)

            ##Go straight to noise instead of making objects first
            one_image_sky.generate_noise("gaussian")
