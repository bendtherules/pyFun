# Utility functions
# ToDo: Put everything in a class as staticmethods  when imported, if
# name=__main__, keep them local
from functools import partial
import inspect
import logging
import types
import event
from uniquelist import uniquelist
from UncasedDict import UncasedDict


def register(list_to_register=None):
    ''' Used as decorator: Adds the function (or anything else) to list_to_register '''
    def temp_func(what_to_register):
        list_to_register.append(what_to_register)
        return what_to_register
    return temp_func


def fuzzy_match_event_name(string, event_or_action):
    str_upper = string.upper()
    if not (str_upper in event.dict_event_name):
        event_or_action = event_or_action.lower()
        if event_or_action.lower() == "event" or event_or_action.lower() == "action":
            # STR_STARTER becomes event_ or action_
            STR_STARTER = event_or_action.upper() + "_"
        else:
            raise AttributeError(
                "event_or_action arg must be 'event' or 'action'.")
        str_normalized = str_upper[
            str_upper.find(STR_STARTER) + len(STR_STARTER):]
        for tmp_event_name in event.dict_event_name:
            # tmp event is the event_name, keys of KW_EVENTS
            tmp_event_name = tmp_event_name.upper()
            tmp_event_name_normalized = tmp_event_name.replace("_", "")
            if str_normalized.startswith(tmp_event_name) or str_normalized.startswith(tmp_event_name_normalized):
                return tmp_event_name
    else:
        return str_upper


class Action(object):

    """ pygame.event.Action(type, dict): return Action
        pygame.Action.Action(type, **attributes): return Action
    """

    def __init__(self, type, *args, **kwargs):
        super(Action, self).__init__()
        self.type = type
        _dict = {}
        if len(args) == 1:
            _dict.update(args[0])
        elif len(args) > 1:
            raise TypeError(
                "Max one non-keyword argument allowed (which is set to dict)")
        if kwargs:
            _dict.update(kwargs)
        if _dict:
            self.dict = _dict


def copy_func(f, name=None):
    return types.FunctionType(f.func_code, f.func_globals, name or f.func_name,
                              f.func_defaults, f.func_closure)


def selfie_depreceated(f):
    """Decorate function `f` to pass a reference to the function
    as the first argument"""
    return partial(f, f)


def selfie(f):
    """Decorate function `f` to pass a reference to the function
    as the first argument"""
    return f.__get__(f, type(f))


def sync_func(func1, func2):
    '''Makes the 1st param (func) equivalent to 2nd param (func).'''
    func1.func_code = func2.func_code
    func1.func_defaults = func2.func_defaults
    func1.func_dict = func2.func_dict
    func1.func_doc = func2.func_doc
    func1.func_name = func2.func_name


class meta_accessor_class(type):

    def __new__(cls, name, base, clsdict):
        temp_cls = type.__new__(cls, name, base, clsdict)
        temp_cls.list_instance = uniquelist()
        temp_cls.list_check_func = uniquelist()
        # dict_action_func -> dict of action funcs, key=event_numb like KEYDOWN
        temp_cls.dict_action_func = UncasedDict()
        methods = inspect.getmembers(temp_cls, inspect.ismethod)
        for (method_name, method_obj) in methods:
            if fuzzy_match_event_name(method_name, "action"):
                temp_cls.register_action(method_obj)
        return temp_cls


@selfie
def run_dec_on_meta(self, what_to_do):
    '''Runs decorator (what_to_do) passed to it during meta with args, cls=>class and func=>function which this is used on'''
    # make copies of this func and instead of params use .vars. Should accept
    # *args,*kwargs to main_func. Next step: multiple funcs, think.

    def inter_run_dec_on_meta(*args, **kwargs):
        # this intermediate func is used to produce func_process_meta for each
        # time
        def func_process_meta(self, *args, **kwargs):
            if not hasattr(self, "_process_meta"):
                # changing own's state, should be restored at last step before
                # meta-return
                self._process_meta = False
            #(below) unneccesary here
            if not hasattr(self, "__old_args") and not hasattr(self, "__old_kwargs"):
                self.__old_args = None
                self.__old_kwargs = None
            if not self._process_meta:
                # as long as not being meta-processed
                # its not really main_func, really its just what_to_do's param
                if (self.__old_args or self.__old_kwargs):
                    self.what_to_do = partial(
                        self.what_to_do, *(self.__old_args), **(self.__old_kwargs))
                self.__old_args = args
                self.__old_kwargs = kwargs
                return selfie(self)
            else:
                self.main_func = self.__old_args[0]
                return self

        func_process_meta.__old_args = args
        func_process_meta.__old_kwargs = kwargs
        func_process_meta.what_to_do = what_to_do
        func_process_meta.selfie = True
        func_process_meta = selfie(func_process_meta)
        return func_process_meta
    return inter_run_dec_on_meta


def run_func_on_meta(run_func):
    '''Runs func (run_func) passed to it during meta with arg, cls.
        run_func remains a method of the class.'''
    run_func._run_meta = True
    return run_func


def register_action(event_name=None, func_to_register=None, cls=None):
    '''
        @fun_Class.register_action() # @fun_Class.register_action === @fun_Class.register_action()
        def event_key_down(ev):
            pass
        OR
        # event_name=KEYDOWN (or "key_down")
        @fun_Class.register_action(event_name)
        def whatever(ev):
            pass
        OR
        fun_Class.register_action(event_name,func)
    '''
    if (event_name is None) and (func_to_register is None):
            # i.e No param passed, used as decorator (1st step of ex. 1)
        logging.info("Nothing passed")
        return register_action
    elif (not(event_name is None)) and (func_to_register is None):
        # i.e. one param is passed, maybe func or (str or int)
        logging.info("Event Name only passed")
        if isinstance(event_name, str):
                # i.e. 1st parm-> str , is event name, acts as decorator
                # (2nd ex.)
                # dont hardcode func name- use metaclass
            logging.info("Event Name is event_name")
            return partial(cls.register_action, event_name)
        elif hasattr(event_name, "__call__"):
            # first param is func, actually func_to_register.
            # So get event_name from func_name (2nd step of 1st ex.)
            logging.info("Event Name is actually func")
            func_to_register = event_name
            event_name = fuzzy_match_event_name(
                func_to_register.func_name, "action")
            return register_action(event_name=event_name, func_to_register=func_to_register, cls=cls)
        else:
            raise TypeError("event_name must be str or func")
    else:
        # Both params present
        logging.info("Both param passed")

        if isinstance(event_name, str):
            event_name = fuzzy_match_event_name(event_name, "action")

        logging.info("Registering func")
        if not (event_name in cls.dict_action_func):
            cls.dict_action_func[event_name] = []
        list_ = cls.dict_action_func[event_name]
        if not (func_to_register in list_):
            list_.append(func_to_register)
        else:
            raise Exception("func_to_register was already rgistered, skipping")

        return func_to_register


def register_class(game_class, cls=None):
    ''' Register this class on mega_class.
    Calls _regitser_class_ on mega_class with arg cls'''
    if cls is None:
        return partial(register_class, game_class)
    game_class.register_class(cls)
    cls.game_obj = game_class
    return cls


def remove_from_list(list_, val, recursive=False):
    if val in list_:
        list_.remove(val)
    if recursive:
        while (val in list_):
            list_.remove(val)
    return list_


def rect_to_pygame_rect(rect):
    if hasattr(rect, "bbox"):
        rect = rect.bbox
    return rect


class updater_list(list):

    """list which also calls a updater func on data change"""

    def __init__(self, updater_func, *arg, **kwargs):
        super(updater_list, self).__init__(*arg, **kwargs)
        self.updater_func = updater_func

    def insert(self, *arg, **kwargs):
        to_return = super(updater_list, self).insert(*arg, **kwargs)
        self.updater_func(self)
        return to_return

    def pop(self, *arg, **kwargs):
        to_return = super(updater_list, self).pop(*arg, **kwargs)
        self.updater_func(self)
        return to_return

    def append(self, *arg, **kwargs):
        to_return = super(updater_list, self).append(*arg, **kwargs)
        self.updater_func(self)
        return to_return

    def extend(self, *arg, **kwargs):
        to_return = super(updater_list, self).extend(*arg, **kwargs)
        self.updater_func(self)
        return to_return

    def __getitem__(self, *arg, **kwargs):
        to_return = super(updater_list, self).__getitem__(*arg, **kwargs)
        self.updater_func(self)
        return to_return

    def __setitem__(self, *arg, **kwargs):
        to_return = super(updater_list, self).__setitem__(*arg, **kwargs)
        self.updater_func(self)
        return to_return
