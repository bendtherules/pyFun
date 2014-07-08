import inspect

def original_decorator(func):
    # need to access class here
    # for eg, to append the func itself to class variable "a", to register itself
    # or say, append their default arg values to class variable "a"
    return func

class A(object):
    a=[]

    @classmethod
    @original_decorator
    def some_method(self,a=5):
        ''' hello'''
        print "Calling some_method"
    @original_decorator
    def some_method_2(self):
        ''' hello again'''
        print "Calling some_method_2"

##print("A.a is %s"%A.a)
##print(inspect.getargspec(A.some_method))