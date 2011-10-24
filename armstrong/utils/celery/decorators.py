from django.db.models.loading import get_model

from . import tasks
from .utils import model_to_tuple


def signal_task(*args, **kwargs):
    def signal(sender, instance, **kwargs):
       sender_tuple = model_to_tuple(sender)
       instance_tuple = model_to_tuple(instance) + (instance.pk, )
       return tasks.async_signal.apply_async(
                args=[sender_tuple, instance_tuple], kwargs=kwargs)
    return signal


class SignalWrapper(object):
    def __init__(self, func):
        self.func = func

    @property
    def sync(self):
        return self.func

    @property
    def async(self):
        return signal_task(self.func)



def signal(func):
    return SignalWrapper(func)


