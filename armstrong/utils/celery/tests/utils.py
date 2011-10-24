from django.db import models

from ._utils import TestCase
from ..utils import model_to_tuple
from ..utils import tuple_to_model


class SimpleModel(models.Model):
    pass


class model_to_tupleTestCase(TestCase):
    def setUp(self):
        self.model = SimpleModel()
        self.result = model_to_tuple(self.model)

    def test_returns_a_tuple(self):
        self.assertIsA(self.result, tuple)

    def test_tuple_has_a_length_of_two(self):
        self.assertEqual(2, len(self.result))

    def test_first_parameter_is_the_app_label(self):
        self.assertEqual("tests", self.result[0])

    def test_second_parameter_is_the_model_name(self):
        self.assertEqual("simplemodel", self.result[1])


class tuple_to_modelTestCase(TestCase):
    def test_loads_model_from_tuple(self):
        result = tuple_to_model(("tests", "simplemodel"))
        self.assertEqual(result.__name__, SimpleModel.__name__)
