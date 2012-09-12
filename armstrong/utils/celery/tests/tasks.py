from celery.task import Task
import fudge
from fudge.inspector import arg

from ._utils import SimpleModel
from ._utils import TestCase

from .. import tasks
from ..tasks import async_signal
from ..tasks import SignalTask


class deserialize_sender_and_instance_TestCase(TestCase):
    def test_can_handle_a_failed_instance_lookup(self):
        a = SimpleModel()
        sender_tuple = (a._meta.app_label, a._meta.module_name)
        instance_tuple = (None, None)

        fake = fudge.Fake()
        fake.is_callable().returns(None)
        with fudge.patched_context(tasks, 'tuple_to_model', fake):
            tasks.deserialize_sender_and_instance({
                'sender_tuple': sender_tuple,
                'instance_tuple': instance_tuple,
            })


class async_signalTestCase(TestCase):
    def test_is_a_celery_task(self):
        def foo():
            pass
        self.assertIsA(async_signal(foo), Task)

    def _test_is_a_signal_task(self):
        def foo():
            pass
        self.assertIsA(async_signal(foo), SignalTask)
