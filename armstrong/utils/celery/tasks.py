from celery.task import task, Task
from django.db.models.loading import get_model
from functools import wraps

from .utils import model_to_tuple
from .utils import tuple_to_model


class SignalTask(Task):
    abstract = True

    def execute(self, request, pool, loglevel, logfile, **kwargs):
        sender = tuple_to_model(request.kwargs["sender_tuple"])
        instance_model = tuple_to_model(request.kwargs["instance_tuple"][:2])
        try:
            instance = instance_model.objects.get(pk=request.kwargs["instance_tuple"][-1])
        except instance_model.DoesNotExist:
            # TODO: retry
            return
        del request.kwargs["sender_tuple"]
        del request.kwargs["instance_tuple"]
        request.kwargs["sender"] = sender
        request.kwargs["instance"] = instance
        super(SignalTask, self).execute(request, pool, loglevel, logfile, **kwargs)

    @classmethod
    def apply_async(self, args=None, kwargs=None):
        # TODO: Test this in an automated fashion.
        #       This has been tested manually, but there's no clean way to
        #       test it in an automated fashion.  Rather than delay the release,
        #       I'm getting it out there and we'll figure out the testing later.
        sender, instance = kwargs.pop("sender"), kwargs.pop("instance")
        sender_tuple = model_to_tuple(sender)
        instance_tuple = model_to_tuple(instance) + (instance.pk, )

        # We can't send the signal because we can't serialize the thread lock
        if "signal" in kwargs:
            del kwargs["signal"]
        kwargs.update({
            "sender_tuple": sender_tuple,
            "instance_tuple": instance_tuple,
        })
        return super(SignalTask, self).apply_async([], kwargs)


def async_signal(func):
    @task(base=SignalTask)
    @wraps(func)
    def signal(*args, **kwargs):
        return func(*args, **kwargs)
    return signal
