import fudge
import random

from ._utils import SimpleModel
from ._utils import TestCase
from ..decorators import signal
from ..decorators import SignalWrapper
from .. import decorators


@signal
def simple(sender, instance, **kwargs):
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
