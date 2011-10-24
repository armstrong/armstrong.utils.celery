import fudge
from fudge.inspector import arg
import random

from ._utils import SimpleModel
from ._utils import TestCase
from ..decorators import signal
from ..decorators import signal_task
from ..decorators import SignalWrapper
from .. import decorators


@signal
def simple(sender, instance, **kwargs):
    pass


def unwrapped_signal(sender, instance, **kwargs):
    pass


class SignalDecoratorTestCase(TestCase):
    def test_returns_SignalWrapper(self):
        self.assertIsA(simple, SignalWrapper)


class SignalWrapperTestCase(TestCase):
    def test_has_sync_property(self):
        self.assert_has_attr(simple, "sync")

    def test_has_sync_property(self):
        self.assert_has_attr(simple, "sync")

    def test_sync_property_is_the_same_as_the_decorated_function(self):
        def foo():
            pass

        decorated_foo = signal(foo)
        self.assertEqual(foo, decorated_foo.sync)

    def test_sync_can_be_run(self):
        r = random.randint(1000, 2000)
        fake = fudge.Fake()
        fake.is_callable().returns(r)
        fudge.clear_calls()

        foo = SignalWrapper(fake)
        self.assertEqual(r, foo.sync())

    def test_has_async_test_property(self):
        self.assert_has_attr(simple, "async")

    def test_async_property_is_not_the_same_as_the_decorated_function(self):
        def foo():
            pass

        decorated_foo = signal(foo)
        self.assertNotEqual(foo, decorated_foo.async)

    def test_async_passes_the_buck_to_signal_task(self):
        fake = fudge.Fake()
        fake.is_callable().expects_call()

        with fudge.patched_context(decorators, "signal_task", fake):
            @signal
            def foo():
                pass

            async_foo = foo.async

class signal_taskTestCase(TestCase):
    def setUp(self):
        super(signal_taskTestCase, self).setUp()
        self.sender = SimpleModel
        self.instance = self.sender()
        self.instance.pk = 1

        self.objects = fudge.Fake()
        self.objects.provides("get").with_args(pk=1).returns(self.instance)
        self.instance.objects = self.objects

    def mock_tasks(self, *args):
        delay = fudge.Fake().expects_call().with_args(*args)
        task = fudge.Fake().has_attr(delay=delay)
        tasks = fudge.Fake().has_attr(async_signal=task)
        return tasks

    def assertTaskReceivesArgs(self, *args):
        mock = self.mock_tasks(*args)
        with fudge.patched_context(decorators, "tasks", mock):
            signal_task(unwrapped_signal)(self.sender, self.instance)

    def test_sender_tuple_passed_to_task(self):
        sender_tuple = ("tests", "simplemodel")
        self.assertTaskReceivesArgs(sender_tuple, arg.any())

    def test_instance_tuple_passed_to_task(self):
        instance_tuple = ("tests", "simplemodel", 1)
        self.assertTaskReceivesArgs(arg.any(), instance_tuple)
