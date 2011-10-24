def signal_task(*args, **kwargs):
    return

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


