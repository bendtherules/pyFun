import inspect
def tryit(func):
    print func
    try:
        print func.im_class
    except:
        print("Failed")
    try:
        print func.im_func
    except:
        print("Failed")
    try:
        print func.im_self
    except:
        print("Failed")
    try:
        func.asd=8
    except:
        print("Failed again")
    return func

class meta_fun_Class(type):

    def __new__(cls, name, base, clsdict):
        temp_class = type.__new__(cls, name, base, clsdict)
        temp_class.__class__=cls
        l=inspect.getmembers(temp_class,inspect.ismethod)
        for l1 in l:
            l1[1].asd=4
        return temp_class

class A(object):
    __metaclass__=meta_fun_Class
    def b(cls):
        pass
    @classmethod
    def c(cls):
        pass
    @staticmethod
    def d(cls):
        pass


