from uniquelist import uniquelist


class StateClass(object):

    """State engine implementation"""

    def __init__(self):
        super(StateClass, self).__init__()
        self._list_state = uniquelist()
        self.add_state(None)
        self._current_state_name = None
        self._dict_switch_func = {}
        self._current_state_dict = {}

    def __getattribute__(self, name):
        try:
            return object.__getattribute__(self, name)
        except:
            try:
                return self._current_state_dict[name]
            except KeyError:
                raise AttributeError("'{self_class}' object has no attribute '{attr_name}'".format(
                    self_class=self.__class__, attr_name=name))

    def __setattr__(self, name, val):
        if name.startswith("_"):
            return object.__setattr__(self, name, val)
        else:
            self._current_state_dict[name] = val

    def add_state(self, state_name):
        self._list_state.append(str(state_name))

    def has_state(self, state_name):
        return str(state_name) in self._list_state

    def remove_state(self, state_name):
        state_name = str(state_name)
        self.check_state(state_name)

        self._list_state.remove(state_name)

    def check_state(self, state_name_or_list):
        if isinstance(state_name_or_list, list):
            for state_name in state_name_or_list:
                # todo: [bug] returns with element, doesnt return with list
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

        print self._dict_switch_func.get((from_, to_))
        return self._dict_switch_func.get((from_, to_))

    def switch_state(self, to_, from_=None, call_func=True):
        if from_ is None:
            from_ = self._current_state_name
        from_, to_ = str(from_), str(to_)
        self.check_state([from_, to_])

        # do call_func
        if call_func:
            switch_func = self.get_switch_func(from_, to_)
            old_dict = self._current_state_dict
            self._current_state_dict = {}
            if switch_func:
                switch_func(old_dict, self._current_state_dict)

        self._current_state_name = to_
        # remove below
