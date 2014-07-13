import event


class Timer(object):

    def __init__(self, name, step_count=None):
        super(Timer, self).__init__()
        if step_count is None:
            step_count = name
            name = None
        self.name = name
        self.ori_step_count = step_count
        self.step_count = self.ori_step_count
        self.paused = False
        self.triggered = False

    @property
    def step_count(self):
        return self._step_count

    @step_count.setter
    def step_count(self, value):
        self._step_count = int(value)

    @property
    def ori_step_count(self):
        return self._ori_step_count

    @ori_step_count.setter
    def ori_step_count(self, value):
        self._ori_step_count = int(value)

    def trigger(self):
        if not self.triggered:
            self.triggered = True
            return event.Event("timer", dict_=self.get_props())

    def get_props(self):
        return {
            "name": self.name,
            "ori_step_count": self.ori_step_count,
            "step_count": self.step_count,
            "paused": self.paused,
            "triggered": self.triggered,
        }

    def check_trigger(self):
        if not self.step_count:
            return self.trigger()

    def process(self):
        self.reduce_step_count()
        return self.check_trigger()

    def reduce_step_count(self):
        if not self.paused:
            self._reduce_step_count()

    def _reduce_step_count(self):
        if self.step_count:
            self.step_count -= 1

    def pause(self):
        self.paused = True

    def resume(self):
        self.paused = False

    def reset_count(self):
        self.step_count = self.ori_step_count

    def reset(self):
        self.reset_count()
        self.resume()
        self.triggered = False
