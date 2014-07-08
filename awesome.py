# Using metaclass and decorator to allow class access during class creation time
from functools import partial
import inspect

class meta(type):
    def __new__(cls, name, base, clsdict):
        temp_cls = type.__new__(cls, name, base, clsdict)
        methods=inspect.getmembers(temp_cls,inspect.ismethod)
        for (method_name,method_obj) in methods:
            tmp_spec=inspect.getargspec(method_obj)
            if "main_func" in tmp_spec.args:
                what_to_do,main_func=tmp_spec.defaults
                f=method_obj.im_func
                f.func_code,f.func_defaults,f.func_dict,f.func_doc,f.func_name=main_func.func_code, main_func.func_defaults,main_func.func_dict,main_func.func_doc,main_func.func_name
                what_to_do(method_obj)

        return temp_cls

def do_it(what_to_do, main_func=None):
    if main_func is None:
        return partial(do_it,what_to_do)
    def whatever(what_to_do=what_to_do,main_func=main_func):
        pass
    return whatever

def original_decorator(func):
    func.im_class.a.append("so cool")
    print "Calling original decorator"


class A(object):
    __metaclass__=meta
    a=[]
    @do_it(original_decorator)
    def some_method(self,a=5):
        ''' hello'''
        print "Calling original method"

print("A.a is %s"%A.a)
print(inspect.getargspec(A().some_method))