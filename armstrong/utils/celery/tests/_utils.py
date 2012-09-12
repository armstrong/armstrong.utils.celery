from armstrong.dev.tests.utils import ArmstrongTestCase
from django.db import models
import fudge


class SimpleModel(models.Model):
    pass


class TestCase(ArmstrongTestCase):
    def setUp(self):
        fudge.clear_calls()
        fudge.clear_expectations()
        super(TestCase, self).setUp()

    def tearDown(self):
        fudge.verify()
        super(TestCase, self).tearDown()

    def assert_has_attr(self, obj, attr):
        return self.assertTrue(hasattr(obj, attr))
