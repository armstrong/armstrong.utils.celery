from armstrong.dev.tests.utils import ArmstrongTestCase


class TestCase(ArmstrongTestCase):
	def assert_has_attr(self, obj, attr):
		return self.assertTrue(hasattr(obj, attr))