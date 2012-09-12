from celery.task import Task
import fudge

from ._utils import SimpleModel
from ._utils import TestCase

from .. import tasks
from ..tasks import async_signal
from ..tasks import SignalTask


class async_signalTestCase(TestCase):
    def test_is_a_celery_task(self):
        def foo():
            pass
        self.assertIsA(async_signal(foo), Task)

    def _test_is_a_signal_task(self):
        def foo():
            pass
        self.assertIsA(async_signal(foo), SignalTask)
