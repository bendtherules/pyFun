from functools import partial
import inspect

class meta(type):
    def __new__(cls, name, base, clsdict):
        temp_cls = type.__new__(cls, name, base, clsdict)
        methods=inspect.getmembers(temp_cls,inspect.ismethod)
        print methods
        print "inspecting.."
        for tmp in methods:
            method=tmp[1]
            tmp_spec=inspect.getargspec(method)
            if "main_func" in tmp_spec.args:
                main_func=tmp_spec.defaults[1]
                tmp_spec.defaults[0]()
                main_func(50)
                f=method.im_func
                print f
                f.func_code,f.func_defaults,f.func_dict,f.func_doc,f.func_name=main_func.func_code, main_func.func_defaults,main_func.func_dict,main_func.func_doc,main_func.func_name
        return temp_cls

def doit(what_to_do, main_func):
    def asd(what_to_do=what_to_do,main_func=main_func):
        pass
    return asd

def pr5():
    print 5

do_pr5=partial(doit,pr5)

class A(object):
    __metaclass__=meta
    a=[]
    @do_pr5
    def abc(self,a=5):
        ''' hello'''
        print a+1
