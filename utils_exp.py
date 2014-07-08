# Utility functions
# ToDo: Put everything in a class as staticmethods  when imported, if
# name=__main__, keep them local
from pygame import locals as pygame_consts
from functools import partial
import inspect
import logging
import types


def register(list_to_register=None):
    ''' Used as decorator: Adds the function (or anything else) to list_to_register '''
    def temp_func(what_to_register):
        list_to_register.append(what_to_register)
        return what_to_register
    return temp_func

KW_EVENTS = {
    "QUIT": pygame_consts.QUIT,
    "ACTIVE_EVENT": pygame_consts.ACTIVEEVENT,
    "KEY_DOWN": pygame_consts.KEYDOWN,
    "KEY_UP": pygame_consts.KEYUP,
    "MOUSE_MOTION": pygame_consts.MOUSEMOTION,
    "MOUSE_BUTTON_UP": pygame_consts.MOUSEBUTTONUP,
    "MOUSE_BUTTON_DOWN": pygame_consts.MOUSEBUTTONDOWN,
    "JOY_AXIS_MOTION": pygame_consts.JOYAXISMOTION,
    "JOY_BALL_MOTION": pygame_consts.JOYBALLMOTION,
    "JOY_HAT_MOTION": pygame_consts.JOYHATMOTION,
    "JOY_BUTTON_UP": pygame_consts.JOYBUTTONUP,
    "JOY_BUTTOND_OWN": pygame_consts.JOYBUTTONDOWN,
    "VIDEO_RESIZE": pygame_consts.VIDEORESIZE,
    "VIDEO_EXPOSE": pygame_consts.VIDEOEXPOSE,
    "USER_EVENT": pygame_consts.USEREVENT,
    # think of begin_step, step and end_step
    "BEGIN_STEP": pygame_consts.USEREVENT + 1,
    "STEP": pygame_consts.USEREVENT + 2,
    "END_STEP": pygame_consts.USEREVENT + 3
}


def fuzzy_match_event_name(string):
# print(string)
    str_normalized = string.upper()
    for tmp_event in KW_EVENTS:
        # tmp event is the event_name, keys of KW_EVENTS
        tmp_event_normalized = tmp_event.replace("_", "")
        if (tmp_event in str_normalized) or (tmp_event_normalized in str_normalized):
            return tmp_event


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

    ''' This metaclass allows class access to any function (or as extended use, to metaclasses)'''
    # Using metaclass and decorator to allow class access during class creation time
    # No method defined within the class should have "_process_meta" as arg
    # Potential problems: Using closures, function.func_globals is read-only
    # Doesnt get appropiate globals, maybe pass it (or the reqd global vars)
    # as param on func defn
    def __new__(cls, name, base, clsdict):
        temp_cls = type.__new__(cls, name, base, clsdict)
        methods = inspect.getmembers(temp_cls, inspect.ismethod)
        for (method_name, method_obj) in methods:
            has_im_func = hasattr(method_obj, "im_func")
            has_func = hasattr(method_obj, "func")
            while has_im_func or has_func:
                if has_im_func:
                    method_obj = method_obj.im_func
                if has_func:
                    # cater for partials
                    method_obj = method_obj.func
                has_im_func = hasattr(method_obj, "im_func")
                has_func = hasattr(method_obj, "func")

            if hasattr(method_obj, "_process_meta"):
                method_obj._process_meta = True
                # method_obj should return itself after setting main_func
                if hasattr(method_obj,"selfie"):
                    method_obj = method_obj(method_obj)
                else:
                    method_obj = method_obj()
                what_to_do, main_func = method_obj.what_to_do, method_obj.main_func
                # as we have resolved all im_funcs in
                # partial,classmethod,boundmethods
                f = method_obj
                sync_func(f, main_func)
                # func_to_register hardcoded
                mod_func = what_to_do(f, cls=temp_cls)
                sync_func(f, mod_func)

        return temp_cls


@selfie
def run_dec_on_meta(self, what_to_do):
    '''Runs decorator (what_to_do) passed to it during meta with args, cls=>class and func=>function which this is used on'''
    # must be deepcopied bcoz multiple versions will edit main func
# syntax error to grab attention
    # make copies of this func and instead of params use .vars. Should accept
    # *args,*kwargs to main_func. Next step: multiple funcs, think.

    def inter_run_dec_on_meta(*args,**kwargs):
        # this intermediate func is used to produce func_process_meta for each time
        def func_process_meta(self, *args, **kwargs):
            if not hasattr(self, "_process_meta"):
                # changing own's state, should be restored at last step before
                # meta-return
                self._process_meta = False
            #(below) unneccesary here
            if not hasattr(self,"__old_args") and not hasattr(self,"__old_kwargs"):
                self.__old_args = None
                self.__old_kwargs = None
            if not self._process_meta:
                # as long as not being meta-processed
                # its not really main_func, really its just what_to_do's param
                if (self.__old_args or self.__old_kwargs):
                    self.what_to_do = partial(self.what_to_do, *(self.__old_args), **(self.__old_kwargs))
                self.__old_args = args
                self.__old_kwargs = kwargs
                return selfie(self)
            else:
                self.main_func = self.__old_args[0]
                return self

        func_process_meta.__old_args = args
        func_process_meta.__old_kwargs = kwargs
        func_process_meta.what_to_do = what_to_do
        func_process_meta.selfie=True
        func_process_meta = selfie(func_process_meta)
        return func_process_meta
    return inter_run_dec_on_meta

def run_func_on_meta(run_func):
    '''Runs func (run_func) passed to it during meta with arg, cls.
        run_func remains a method of the class.'''
    def what_to_do(func, cls):
        func(cls=cls)
        return func
    return run_dec_on_meta(what_to_do=what_to_do, main_func=run_func)


def register_event(event_name=None, func_to_register=None, cls=None):
    '''
        @fun_Class.register_event() # @fun_Class.register_event === @fun_Class.register_event()
        def event_key_down(ev):
            pass
        OR
        # event_name=KEYDOWN (or "key_down")
        @fun_Class.register_event(event_name)
        def whatever(ev):
            pass
        OR
        fun_Class.register_event(event_name,func)
    '''
    if (event_name is None) and (func_to_register is None):
            # i.e No param passed, used as decorator (1st step of ex. 1)
        logging.info("Nothing passed")
        return register_event
    elif (not(event_name is None)) and (func_to_register is None):
        # i.e. one param is passed, maybe func or (str or int)
        logging.info("Event Name only passed")
        if isinstance(event_name, int) or isinstance(event_name, str):
                # i.e. 1st parm-> str or int, is event name, acts as decorator
                # (2nd ex.)
                # dont hardcode func name- use metaclass
            logging.info("Event Name is event_name")
            return partial(cls.register_event, event_name)
        elif hasattr(event_name, "__call__"):
            # first param is func, actually func_to_register.
            # So get event_name from func_name (2nd step of 1st ex.)
            logging.info("Event Name is actually func")
            func_to_register = event_name
            event_name = fuzzy_match_event_name(func_to_register.func_name)
            return register_event(event_name=event_name, func_to_register=func_to_register, cls=cls)
        else:
            raise TypeError("event_name must be (str or int) or func")
    else:
        # Both params present
        logging.info("Both param passed")

        if isinstance(event_name, str):
            event_name = fuzzy_match_event_name(event_name)
            event_numb = KW_EVENTS[event_name]
        elif isinstance(event_name, int):
            event_numb = event_name
        else:
            raise TypeError("event_name should be str or int")

        logging.info("Registering func")
        if not (event_numb in cls.dict_action_func):
            cls.dict_action_func[event_numb] = []
        cls.dict_action_func[event_numb].append(func_to_register)

        return func_to_register



##_register_event_ = register_event
##del register_event
# so that register event is actually delegated register
##register_event = run_dec_on_meta(_register_event_)
