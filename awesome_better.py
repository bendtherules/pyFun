
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
    # Using metaclass and decorator to allow class access during class creation time
    # No method defined within the class should have "_process_meta" as arg
    # Potential problems: Using closures, function.func_globals is read-only
    # Doesnt get appropiate globals, maybe pass it (or the reqd global vars) as param on func defn
    def __new__(cls, name, base, clsdict):
        temp_cls = type.__new__(cls, name, base, clsdict)
        methods = inspect.getmembers(temp_cls, inspect.ismethod)
        for (method_name, method_obj) in methods:
            tmp_spec = inspect.getargspec(method_obj)
            if "__process_meta" in tmp_spec.args:
                what_to_do, main_func = tmp_spec.defaults[:-1]
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
def run_it(run_func):
        def what_to_do(cls, func):
            func(cls)
            return func
        return do_it(what_to_do=what_to_do,main_func=run_func)


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
    func.__doc__ = "This is a instance method"  # Can change func properties
    print "Calling original method decorator"
    return func


def decorator_to_classmethod(cls, func):
    cls.original_classmethod_decorator = classmethod(
        original_classmethod_decorator)
    return func

b=[]

class A(object):
    __metaclass__ = meta
    a = []
##    original_classmethod_decorator = classmethod(
##        original_classmethod_decorator)
##    original_method_decorator = classmethod(original_method_decorator)

    @classmethod
    @do_it(original_classmethod_decorator)
    def some_method(cls, x=1):
        ''' hello'''
        print "Calling original class method"

    @classmethod
    @run_it
    def register_class(cls):
        b.append(cls)


##
# @classmethod
# @do_it(decorator_to_classmethod)
# def original_classmethod_decorator(cls):
# pass

# @classmethod
# @do_it(decorator_to_classmethod)
# def original_method_decorator(cls):
# pass

    @do_it(original_method_decorator)
    def some_method_2(self, y=2):
        ''' hello again'''
        print "Calling original method"

# signature preserved
print(inspect.getargspec(A.some_method))
print(inspect.getargspec(A.some_method_2))
