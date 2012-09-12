from celery.task import task, Task
from django.db.models.loading import get_model
from functools import wraps

from .utils import model_to_tuple
from .utils import tuple_to_model


def deserialize_sender_and_instance(kwargs):
    sender_tuple, instance_tuple = (kwargs.pop("sender_tuple"),
            kwargs.pop("instance_tuple", None))
    sender = tuple_to_model(sender_tuple)
    kwargs["sender"] = sender
    if instance_tuple is not None:
        instance_model = tuple_to_model(instance_tuple[:2])
        if instance_model is None:
            # Handle situtation where invalid data is sent across the wire
            return

        try:
            instance = instance_model.objects.get(pk=instance_tuple[-1])
            kwargs["instance"] = instance
        except instance_model.DoesNotExist:
            # TODO: retry?
            pass


class SignalTask(Task):
    abstract = True

    def execute(self, request, pool, loglevel, logfile, **kwargs):
        deserialize_sender_and_instance(request.kwargs)
        super(SignalTask, self).execute(request, pool, loglevel, logfile, **kwargs)

    @classmethod
    def apply(self, args=None, kwargs=None, **options):
        if kwargs:
            deserialize_sender_and_instance(kwargs)
        super(SignalTask, self).apply(args, kwargs, **options)

    @classmethod
    def apply_async(self, args=None, kwargs=None, **options):
        # TODO: Test this in an automated fashion.
        #       This has been tested manually, but there's no clean way to
        #       test it in an automated fashion.  Rather than delay the release,
        #       I'm getting it out there and we'll figure out the testing later.
        # We can't send the signal because we can't serialize the thread lock
        if "signal" in kwargs:
            del kwargs["signal"]

        sender, instance = kwargs.pop("sender"), kwargs.pop("instance", None)
        kwargs["sender_tuple"] = model_to_tuple(sender)
        if instance is not None:
            kwargs["instance_tuple"] = model_to_tuple(instance) + (instance.pk, )

        return super(SignalTask, self).apply_async([], kwargs, **options)


def async_signal(func):
    @task(base=SignalTask)
    @wraps(func)
    def signal(*args, **kwargs):
        return func(*args, **kwargs)
    return signal
