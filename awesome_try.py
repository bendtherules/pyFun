# Using metaclass and decorator to allow class access during class creation time
# No method defined within the class should have "_process_meta" as arg
# Potential problems: Using closures, function.func_globals is read-only
# => may cause problem
from functools import partial
import inspect


def sync_func(func1, func2):
    '''Makes the 1st param (func) equivalent to 2nd param (func).'''
    func1.func_code = func2.func_code
    func1.func_defaults = func2.func_defaults
    func1.func_dict = func2.func_dict
    func1.func_doc = func2.func_doc
    func1.func_name = func2.func_name


class meta(type):

    def __new__(cls, name, base, clsdict):
        temp_cls = type.__new__(cls, name, base, clsdict)
        methods = inspect.getmembers(temp_cls, inspect.ismethod)
        for (method_name, method_obj) in methods:
            tmp_spec = inspect.getargspec(method_obj)
            if "__process_meta" in tmp_spec.args:
                what_to_do, main_func = tmp_spec.defaults[:-1]
                # is_classmethod=False
                # if method_obj.__self__==temp_cls:
                #     is_classmethod=True
                f = method_obj.im_func
                sync_func(f, main_func)
                mod_func = what_to_do(temp_cls, f)
                sync_func(f, mod_func)

        return temp_cls


def do_it(what_to_do, main_func=None):
    if main_func is None:
        return partial(do_it, what_to_do)

    def whatever(what_to_do=what_to_do, main_func=main_func, __process_meta=True):
        pass
    return whatever


def original_classmethod_decorator(cls, func):
    # append default arg values to class variable "a"
    func_defaults = inspect.getargspec(func).defaults
    cls.a.append(func_defaults)
    func.__doc__ = "This is a class method"
    print "Calling original classmethod decorator"
    return func


def original_method_decorator(cls, func):
    # append default arg values to class variable "a"
    func_defaults = inspect.getargspec(func).defaults
    cls.a.append(func_defaults)
    func.__doc__ = "This is a instance method"
    print "Calling original method decorator"
    return func


class A(object):
    __metaclass__ = meta
    a = []

    @classmethod
    @do_it(original_classmethod_decorator)
    def some_method(cls, x=1):
        ''' hello'''
        print "Calling original class method"

    @do_it(original_method_decorator)
    def some_method_2(self, y=2):
        ''' hello again'''
        print "Calling original method"

print(inspect.getargspec(A.some_method))
print(inspect.getargspec(A.some_method_2))
