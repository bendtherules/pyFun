from base import fun_Class


def FakeNoneType():
    return None


class StateClass(fun_Class):

    """State engine implementation"""

    def __init__(self, *args, **kwargs):
        super(StateClass, self).__init__(*args, **kwargs)
        self.prepare_internal()

    @classmethod
    def monkey_patch(this_cls, other_cls):
        unpatched_init = other_cls.__init__

        def patched_init(self, *args, **kwargs):
            self.prepare_internal()
            unpatched_init(self, *args, **kwargs)
        other_cls.__init__ = patched_init

        # patch all functions - keep up-to-date
        other_cls.prepare_internal = this_cls.prepare_internal.im_func
        other_cls.__getattribute__ = this_cls.__getattribute__.im_func
        other_cls.add_state = this_cls.add_state.im_func
        other_cls.has_state = this_cls.has_state.im_func
        other_cls.remove_state = this_cls.remove_state.im_func
        other_cls.check_state = this_cls.check_state.im_func
        other_cls.add_switch_func = this_cls.add_switch_func.im_func
        other_cls.get_switch_func = this_cls.get_switch_func.im_func
        other_cls.switch_state = this_cls.switch_state.im_func

        return other_cls

    def prepare_internal(self):
        self._dict_state = {}
        self._dict_switch_func = {}
        self._current_state_name = str(None)
        self._current_state_obj = None
        self.add_state(str(None), FakeNoneType)
        # For testing
        self.switch_state(str(None))

    def __getattribute__(self, name):
        try:
            _current_state_obj = object.__getattribute__(
                self, "_current_state_obj")
        except:
            # should happen only few times at init
            _current_state_obj = None

        # decide try/else vs hasattr
        # if hasattr(_current_state_obj, name):
        try:
            return object.__getattribute__(_current_state_obj, name)
        except:
            try:
                return object.__getattribute__(self, name)
            except KeyError:
                raise AttributeError("'{self_class}' object and its state has no attribute '{attr_name}'".format(
                    self_class=self.__class__, attr_name=name))

    # def __setattr__(self, name, val):
    #     if name.startswith("_"):
    #         return object.__setattr__(self, name, val)
    #     else:
    #         self._current_dict[name] = val

    def add_state(self, state_name, state_class):
        state_name = str(state_name)
        self._dict_state[state_name] = state_class

    def has_state(self, state_name):
        return str(state_name) in self._dict_state

    def remove_state(self, state_name):
        state_name = str(state_name)
        self.check_state(state_name)

        self._dict_state.pop(state_name)

    def check_state(self, state_name_or_list):
        if isinstance(state_name_or_list, list):
            for state_name in state_name_or_list:
                self.check_state(state_name)
        else:
            state_name = state_name_or_list

        if self.has_state(state_name):
            return state_name
        else:
            raise ValueError("state {state_name} not registered".format(
                state_name=state_name))

    def add_switch_func(self, from_, to_, func_):
        from_, to_ = str(from_), str(to_)
        self.check_state([from_, to_])

        self._dict_switch_func[(from_, to_)] = func_

    def get_switch_func(self, from_, to_):
        from_, to_ = str(from_), str(to_)
        self.check_state([from_, to_])

        # print self._dict_switch_func.get((from_, to_))
        return self._dict_switch_func.get((from_, to_))

    def switch_state(self, to_, *args, **kwargs):
        from_ = self._current_state_name
        to_ = str(to_)
        self.check_state([from_, to_])

        # do call_func
        switch_func = self.get_switch_func(from_, to_)
        new_state = self._dict_state.get(
            to_)(*args, **kwargs)
        if switch_func:
            old_state = self._current_state_obj
            switch_func(old_state, new_state)

        self._current_state_obj = new_state
        self._current_state_name = to_
        try:
            self._current_state_obj.state_parent = self
        except:
            pass
        # remove below
