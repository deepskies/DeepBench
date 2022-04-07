from unittest import TestCase
import numpy as np
import os
from src.deepbench.image.image import Image
from src.deepbench.image.image import ObjectForTesting
from src.deepbench import astro_object


class InitTestClass(Image):
    def __init__(self, objects, image_shape):
        super().__init__(objects, image_shape)


class TestImage(TestCase):
    def setUp(self):
        self.test_image_instance = InitTestClass([], ())

    def test_direct_init(self):
        with self.assertRaises(TypeError):
            objects = []
            image_shape = ()
            Image(objects, image_shape)

    def test_image_init(self):
        test_image = InitTestClass([], ())
        self.assertIsNone(test_image.image)

    def test_init_within_other_class(self):
        assert issubclass(InitTestClass, Image)

    def test_superinit_shape(self):
        objects = []
        image_shape = (14, 14)
        test_image = InitTestClass(objects, image_shape)

        self.assertEqual(image_shape, test_image.image_shape)

    def test_superinit_objects(self):

        objects = []
        image_shape = (14, 14)
        test_image = InitTestClass(objects, image_shape)

        self.assertEqual(objects, test_image.objects)

    def test_object_len(self):
        objects = []
        image_shape = (14, 14)
        test_image = InitTestClass(objects, image_shape)

        image_class_len = test_image.__len__()
        self.assertEqual(0, image_class_len)

    def test_multi_objects_len(self):
        objects = [{}, {}, {}]
        image_shape = (14, 14)
        test_image = InitTestClass(objects, image_shape)

        image_class_len = test_image.__len__()
        self.assertEqual(3, image_class_len)

    def test_image_parameters_no_init(self):
        with self.assertRaises(TypeError):
            objects = []
            image_shape = (14, 14)
            test_image = Image(objects, image_shape)
            test_image._image_parameters()

    def test_image_parameters_alt_init(self):
        objects = []
        image_shape = (14, 14)
        test_image = InitTestClass(objects, image_shape)

        image_class_parameters = test_image._image_parameters()
        self.assertEqual((image_shape, objects), image_class_parameters)

    def test_combined_not_init(self):
        with self.assertRaises(NotImplementedError):
            test_image = InitTestClass([], ())
            test_image.combine_objects()

    def test_combined_other_class(self):
        class TestCombined(Image):
            def __init__(self):
                super().__init__([1, 1, 1], ())

            def combine_objects(self):
                return sum(self.objects)

        expected_sum = 3
        actual_sum = TestCombined().combine_objects()
        self.assertEqual(expected_sum, actual_sum)

    def test_generate_noise_no_init(self):
        with self.assertRaises(NotImplementedError):
            test_image = InitTestClass([], ())
            test_image.generate_noise("noise")

    def test_generate_noise_init(self):
        class TestCombined(Image):
            def __init__(self):
                super().__init__([1, 1, 1], ())

            def generate_noise(self, noise_type):
                return noise_type

        expected_noise = "guassian"
        actual_noise = TestCombined().generate_noise(noise_type="guassian")
        self.assertEqual(expected_noise, actual_noise)

    def test_save_image_defaults(self):
        test_image = InitTestClass([], ())
        empty_image = np.zeros((10, 10))
        test_image.image = empty_image

        test_image.save_image()
        out_path = "results/image_1.jpg"

        image_exists = os.path.exists(out_path)

        if image_exists:
            os.remove(out_path)
            os.rmdir("results/")

        self.assertTrue(image_exists)

    def test_save_image_no_image(self):
        test_image = InitTestClass([], ())
        with self.assertRaises(AssertionError):
            test_image.save_image()

    def test_save_image_nodir(self):
        test_image = InitTestClass([], ())
        empty_image = np.zeros((10, 10))
        test_image.image = empty_image

        new_folder = "test_save_dir"
        test_image.save_image(save_dir=new_folder)
        out_path = f"{new_folder}/image_1.jpg"

        image_exists = os.path.exists(out_path)

        if image_exists:
            os.remove(out_path)
            os.rmdir(new_folder)

        self.assertTrue(image_exists)

    def test_save_existing_dir(self):
        test_image = InitTestClass([], ())
        empty_image = np.zeros((10, 10))
        test_image.image = empty_image
        new_save_dir = "test_save_dir"
        os.makedirs(new_save_dir)
        out_path = f"{new_save_dir}/image_1.jpg"
        test_image.save_image(save_dir=new_save_dir)

        image_exists = os.path.exists(out_path)

        if image_exists:
            os.remove(out_path)
            os.rmdir(new_save_dir)

        self.assertTrue(image_exists)

    def test_generate_astro_object_test_object(self):
        object_params = [{"object_type": "test_object", "object_parameters": {}}]
        image_shape = (14, 14)
        test_object = InitTestClass(object_params, image_shape)
        obj = test_object._generate_astro_object(
            "test_object", object_params[0]["object_parameters"]
        )

        # Test object is a debug object that "create_object" just makes a empty array for
        self.assertIsInstance(obj, ObjectForTesting)

    # def test_generate_astro_object_star(self):
    #     object_params = [{}]
    #     image_shape = (14, 14)
    #     one_image_sky = TestClass(object_params, image_shape)
    #     obj = one_image_sky.generate_astro_object("star", {})
    #
    #     self.assertIsInstance(obj, astro_object.Star)
    #
    # def test_generate_astro_object_strong_lens(self):
    #     object_params = [{}]
    #     image_shape = (14, 14)
    #     one_image_sky = TestClass(object_params, image_shape)
    #     obj = one_image_sky._generate_astro_object("strong_lens", {})
    #
    #     self.assertIsInstance(obj, astro_object.StrongLens)
    #
    # def test_generate_galaxy_object(self):
    #     object_params = [{}]
    #     image_shape = (14, 14)
    #     one_image_sky = TestClass(object_params, image_shape)
    #     obj = one_image_sky._generate_astro_object("galaxy", {})
    #
    #     self.assertIsInstance(obj, astro_object.Galaxy)
    #
    # def test_generate_spiral_galaxy_object(self):
    #     object_params = [{}]
    #     image_shape = (14, 14)
    #     one_image_sky = TestClass(object_params, image_shape)
    #     obj = one_image_sky._generate_astro_object("spiral_galaxy", {})
    #
    #     self.assertIsInstance(obj, astro_object.SpiralGalaxy)
    #
    # def test_generate_n_body_object(self):
    #     object_params = [{}]
    #     image_shape = (14, 14)
    #     one_image_sky = TestClass(object_params, image_shape)
    #     obj = one_image_sky._generate_astro_object("n_body", {})
    #
    #     self.assertIsInstance(obj, astro_object.NBody)
    #
    # def test_not_included_object(self):
    #     with self.assertRaises(NotImplementedError):
    #         object_params = [{}]
    #         image_shape = (14, 14)
    #         one_image_sky = TestClass(object_params, image_shape)
    #         one_image_sky._generate_astro_object("Fake Object", {})
