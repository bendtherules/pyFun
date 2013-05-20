# only for python 2.x
from uniquelist import * # imports uniquelist
import pygame
from pygame.locals import * # imports the constants
#Mouse constants
B_LEFT_CLICK=1
B_RIGHT_CLICK=3
B_MIDDLE_CLICK=2
B_SCROLLUP=4
B_SCROLLDOWN=5

# Direction constants
TOP=1
LEFT=2
BOTTOM=3
RIGHT=4

class fun_Game(object):
    list_class=uniquelist()
    list_event=[] # event_list of this step
    list_event_old=[] # event_list of the previous step
    list_state_all_buttons=[] # A sequence of boolean representing the state of every key
    list_state_all_buttons_old=[] # A sequence of boolean representing the state of every key of previous step
    def __init__(self,width,height,fps=30):
        pygame.init()
        self.fps=fps
        self.clock=pygame.time.Clock()
        self.width=width
        self.height=height

    def update_all_class(self):
        for temp_cls in fun_Game.list_class:
            for temp_count in temp_cls.list_instance:
                temp_count.update()

    def _cache_event_list(self):
        ''' Cache event_list in every step.
            All events in fun_Game.list_event have a "type" property which are the usual constants. '''
        fun_Game.list_event_old=fun_Game.list_event # move current list to old list
        fun_Game.list_state_all_buttons_old=fun_Game.list_state_all_buttons

        fun_Game.list_event=pygame.event.get()
        fun_Game.list_state_all_buttons=pygame.key.get_pressed() #Returns a sequence of boolean representing the state of every key. Use key constant values for indexing.
        #print fun_Game.list_event # debug message
    # control access to list_event
    # with getter, do something crazy for filtering
    # or a filtering function

    def run(self):
        self.screen=pygame.display.set_mode([self.width,self.height])
        while True:
            self._cache_event_list() # Todo: Add other update-related functions
            self.update_all_class()
            # VERY IMPORTANT: Do a spare first step so that every variable / list gets initialised well. Start instant creation and execution from second step.
            # IMPORTANT: First do all fun_Game related stuff before dealing with game objects.
            self.clock.tick(self.fps)
            self.screen.fill([50,100,150]) # Todo: Remove this debug statement
            pygame.display.flip() # debug statement
            #print(event)
            #print(fun_Game.list_event_old)
    # Todo - Add crazy functions to allow other objects and instances finding like GM

    #class fun_Game ends here

class meta_fun_Class(type):
    def __new__(cls,name,base,clsdict):
        temp_class=type.__new__(cls,name,base,clsdict)
        fun_Game.list_class.append(temp_class)
        cls.priority_order=cls.depth=len(fun_Game.list_class) #by default, priority_order and depth depends on "when class was defined"

        return temp_class

class fun_Class(object):
    __metaclass__=meta_fun_Class
    list_instance=uniquelist()
    #list_update_functions stores the list of functions to call in the given order.
    #It can be used for injecting custom user functions (remember order).
    list_update_functions=uniquelist() #action_draw not added as it depends on depth
    list_check_functions=uniquelist() # all the check functions added here. what they do: if event_<event_name>: action_<event_name>

    def __init__(self,x,y,img=None):
        self.x=0
        self.y=0
        self.img=img #img should be a fun_Image, but lets do that later
        fun_Class.list_instance.append(self)
        self.action_create()

    def update(self):
        '''calls all functions in list_update_functions in the given order'''
        temp=None
        for temp in fun_Class.list_update_functions:
            temp(self)

    def draw(self):
        # do some blitting depending on self.img
        pass

    def register(list_to_register=None):
        ''' Used as decorator: Adds the function to list_to_register '''
        def temp_func(what_to_register):
            list_to_register.append(what_to_register)
            return what_to_register
        return temp_func

    @register(list_update_functions)
    def action_begin_step(self):
        pass
    @register(list_update_functions)
    def action_step(self):
        tmp=self.event_mouse_click()
        if tmp:
            print tmp
        print(self.mouse_get_focused())
    @register(list_update_functions)
    def action_end_step(self):
        pass
    # creation and destroy event
    def action_create(self):
        ''' Better to use this function than overloading __init__() '''
        pass
    def action_destroy(self):
        ''' Executed when the instance is destroyed '''
        pass
    def destroy(self):
        action_destroy(self)

    # checks for all standard events -- functions named like check_<event>
    # what they do: if event_<event_name>: action_<event_name>
    # so lets define event_<event_name>,action_<event_name>,check_<event_name> for each <event_name>

    # keyboard handling (later move to keyboard module)

    # occurs if the key was held down continously since the last step
    def event_key_pressed(self,key_value):#check if it works
        if get_event_list(list_to_get=fun_Game.list_state_all_buttons)[key_value] \
        and get_event_list(list_to_get=fun_Game.list_state_all_buttons_old)[key_value]\
        and (not get_event_list(event_types=KEYUP,further_check_variable_name="key",further_check_value=key_value))\
        and (not get_event_list(event_types=KEYUP,further_check_variable_name="key",further_check_value=key_value,list_to_get=fun_Game.list_event_old)):
            return True

    def action_key_pressed(self,key_value):
        pass
    def check_key_pressed(self):
        pass # Todo: think about how to do it

    # occurs if the key is held at the moment (live)
    def event_key_pressed_live(self,key_value):#check if it works
        ''' Returns True if the key (represented by key_code) is currently pressed.
            Problem is that this function is live. Returns True if the key is pressed at that moment.
            So, for example, two calls in two consecutive steps may return True although the key has been left in the meantime. '''
        temp_all_buttons=get_event_list(list_to_get=fun_Game.list_state_all_buttons) #Returns a sequence of boolean representing the state of every key. Use key constant values for indexing.
        if temp_all_buttons[key_value]: # indexing by key_value
            return True
    def action_key_pressed_live(self,key_value):
        pass
    def check_key_pressed_live(self):
        temp_all_buttons=get_event_list(list_to_get=fun_Game.list_state_all_buttons) #Returns a sequence of boolean representing the state of every key. Use key constant values for indexing.
        for temp in range(len(temp_all_buttons)): # temp represents the key code in numbers as it is the index of list_state_all_buttons indirectly
            if temp_all_buttons[temp]:
                self.action_key_pressed_live(temp) #temp is the keycode

    # occurs if a key press occurs (i.e. pushed down)
    # key repetations may occur as the list is cached per step and there might be multiple (same key)press per step.
    def event_key_down(self,key=None):
        if key == None:
            return get_event_list(KEYDOWN)
        else:
            return get_event_list(KEYDOWN,"key",key)
    def action_key_down(self,key):
        pass
    def check_key_down(self):
        for temp in get_event_list(KEYDOWN):
                action_key_down(self,temp.key)


    #probably wierd thing to do - define all <>_key_down as equivalent to <>_key_press
    event_key_press = event_key_down
    action_key_press = action_key_down
    check_key_press = check_key_down

    # occurs if key is released
    def event_key_up(self,key=None):
        if key==None:
            return get_event_list(KEYUP)
        else:
            return get_event_list(KEYUP,"key",key)
    def action_key_up(self,key):
        pass
    def check_key_up(self):
        for temp in get_event_list(KEYUP):
                action_key_up(self,temp.key)
    # Todo: Do other key and keyboard related functions (look at GM for related functions)
    # Mouse handling (later move it to mouse module)
    #Mouse constants (defined at top - move them to a constants module, which will be imported in the global namespace)
    #mouse click
    def event_mouse_click(self,button=None):
        if button==None:
            return  get_event_list(event_types=MOUSEBUTTONDOWN)
        else:
            return get_event_list(event_types=MOUSEBUTTONDOWN,further_check_variable_name="button",further_check_value=button)
    def action_mouse_click(self,button):
        pass
    def check_mouse_click(self):
        list_temp=get_event_list(event_types=MOUSEBUTTONDOWN)
        for temp in list_temp:
            action_mouse_click(temp.button)
    #mouse get pressed
    def event_mouse_get_pressed(self,button=None):
        ''' event_mouse_get_pressed() -> tuple looking like (1,0,0) i.e. ( left_click_state, middle_click_state, right_click_state ).
            Use an index which is (corresponding_constant - 1). For eg event_mouse_get_pressed()[0] returns left click state.
            event_mouse_get_pressed(button) -> Returns 0 or 1 depending on pressed or not. '''
        if button==None:
            return pygame.mouse.get_pressed()
        else:
            return pygame.mouse.get_pressed()[button-1] # because the tuple returned has o-based indexing
    # end of mouse handling
    # other mouse-based functions
    def mouse_get_focused(self):
        return pygame.mouse.get_focused()
    def mouse_set_visible(self,bool_value):
        return pygame.mouse.set_visible(bool_value)
    def mouse_get_rel(self):
        ''' Returns relative movement of the mouse since the last call to this function.
            mouse_get_rel() -> (x,y) '''
        return pygame.mouse.get_rel()
    def mouse_set_cursor_image(self,image=None):
        pass # todo: complete after the image part is done
    # implement mouse_pos as variable
    @property
    def mouse_pos(self):
        ''' mouse_pos -> (x,y)
            mouse_pos = [x,y] -> Sets cursor position '''
        return pygame.mouse.get_pos()
    @mouse_pos.setter
    def mouse_pos(self,val):
        ''' val should be a list [x,y] '''
        if not isinstance(val,list):
            raise TypeError("val should be a list [x,y]")
        pygame.mouse.set_pos(val)

    # implement mouse_x as variable
    @property
    def mouse_x(self):
        ''' mouse_x -> x
            mouse_x = some_x -> Sets cursor x position '''
        return pygame.mouse.get_pos()[0] # get_pos -> (x,y)
    @mouse_x.setter
    def mouse_x(self,x):
        pygame.mouse.set_pos([x,mouse_y])

    # implement mouse_y as variable
    @property
    def mouse_y(self):
        ''' mouse_y -> y
            mouse_y = some_y -> Sets cursor y position '''
        return pygame.mouse.get_pos()[1] # get_pos -> (x,y)
    @mouse_y.setter
    def mouse_y(self,y):
        pygame.mouse.set_pos([mouse_x,y])
    # end of mouse-related function
    #other various events

    def event_intersect_room_boundary(self): # todo: test after image part is done
        ''' Checks if the object (its image bounding box) is intersecting the room boundary, but not totally outside the room.
            Returns direction constants like TOP, LEFT, BOTTOM, RIGHT. '''
        if (self.x+self.image.bbox.width/2)>fun_Game.room_width and not (self.x-self.image.bbox.width/2)>fun_Game.room_width:
            return RIGHT # all constants defined at global level
        elif (self.y+self.image.bbox.height/2)>fun_Game.room_height and not (self.y-self.image.bbox.height/2)>fun_Game.room_height:
            return BOTTOM
        elif (self.x-self.image.bbox.width/2)<0 and not (self.x+self.image.bbox.width/2)<0:
            return LEFT
        elif (self.y-self.image.bbox.height/2)<0 and not (self.y+self.image.bbox.height/2)<0:
            return TOP
    def action_intersect_room_boundary(self):
        pass
    def check_intersect_room_boundary(self):
        if event_intersect_room_boundary(self):
            action_intersect_room_boundary(self)

    def event_outside_room_boundary(self):
        ''' Checks if the object (its image bounding box) is totally outside room.
            Returns direction constants like TOP, LEFT, BOTTOM, RIGHT. '''
        if (self.x-self.image.bbox.width/2)>fun_Game.room_width:
            return RIGHT # all constants defined at global level
        elif (self.y-self.image.bbox.height/2)>fun_Game.room_height:
            return BOTTOM
        elif (self.x+self.image.bbox.width/2)<0:
            return LEFT
        elif (self.y+self.image.bbox.height/2)<0:
            return TOP

    # end of fun_Class
# Other classes
class Circle(object):
    def __init__(self,(x,y),radius,color=None):
        self.center=[x,y]
        self.radius=radius
        self.color=color
    @property
    def center_x(self):
        return self.center[0]
    @property
    def center_y(self):
        return self.center[1]
    @center_x.setter
    def center_x(self,new_x):
        self.center[0]=new_x
    @center_y.setter
    def center_y(self,new_y):
        self.center[1]=new_y
    @property
    def bbox(self):
        left=self.center_x-self.radius
        top=self.center_y-self.radius
        width=self.radius*2
        height=self.radius*2
        return pygame.Rect(left, top, width, height)

    def copy(self):
        return Circle((self.center_x,self.center_y),self.radius,self.color)

    def move(self,move_x,move_y):
        return Circle((self.center_x+move_x,self.center_y+move_y),self.radius,self.color)

    def move_ip(self,move_x,move_y):
        self.center_x+=move_x
        self.center_y+=move_y

    def inflate(self,inflate_radius):
        return Circle((self.center_x,self.center_y),self.radius+inflate_radius,self.color)

    def inflate_ip(self,inflate_radius):
        self.radius+=inflate_radius

    def __union(self,((x1,y1),radius_1),((x2,y2),radius_2)):
        ''' self.__union((new_center_x,new_center_y),new_radius) -> ([x,y],radius) which are the resultant values. '''
        temp_center_x = float(x1+x2)/2 # Does integer division, losses precision
        temp_center_y = float(y1+y2)/2
        temp_radius = float( radius_1 + radius_2 + distance( (x1,y1), (x2,y2) ) )/2
        return ([temp_center_x,temp_center_y],temp_radius)

    def is_inside(self,another_circle):
        ''' Checks if this circle is inside another_circle '''
        return  distance( self.center, another_circle.center )<self.radius

    def is_inside_mutual(self,another_circle):
        ''' Checks if this circle is inside another_circle and also the opposite.
            2x Faster than using is_inside for both of them. '''
        return (distance( self.center, another_circle.center ) < max( self.radius, another_circle.radius) )

    def collide_circle(self,another_circle):
        ''' Checks if this circle intersects with another_circle. '''
        return (distance( self.center, another_circle.center ) <= (self.radius + another_circle.radius) )

    def collide_point(self, (point_x, point_y)):
        ''' Checks if (point_x, point_y) is inside this circle. '''
        return (distance(self.center, (point_x,point_y) ) <= self.radius )

    def collide_list_circle(self, list_circle):
        ''' Checks if this circle intersects with any of the circles in circle_list. '''
        for circle in list_circle:
            if collide_circle(self,circle):
                return True
        else: #else of the for loop
            return False

    def collide_list_all_circle(self,list_circle):
        ''' Checks if this circle intersects with all of the circles in circle_list. '''
        for circle in list_circle:
            if not collide_circle(self,circle):
                return False
        else: #else of the for loop
            return True

    def collide_rect(self,another_rect):
        ''' Checks if this circle collides with another_rect. '''
        return not ( (self.center_x+self.radius)<another_rect.left or (self.center_x-self.radius)>another_rect.right or (self.center_y+self.radius)<another_rect.top or (self.center_y-self.radius)>another_rect.bottom )

    def collide_list_rect(self,list_rect):
        ''' Returns True if collides with any of the rect in the list. '''
        for temp_rect in list_rect:
            if collide_rect(self,temp_rect):
                return True
        else:
            return False

    def collide_list_all_rect(self,list_rect):
        ''' Returns True if collides with all the rect in the list. '''
        for temp_rect in list_rect:
            if not collide_rect(self,temp_rect):
                return False
            else:
                return True

    # union - do later. needs to be a circle *within* which the union of the bounding box of all the circles can be fit.
##    def union(self,new_circle):
##        ''' Returns a new circle which is the union of these two circles '''
##        temp_var=self.__union((self.center,self.radius),(new_circle.center,new_circle.radius))
##        return Circle(temp_var[0],temp_var[1])
##
##    def union_ip(self,new_circle):
##        ''' Turns this circle into a circle which is a union of these two circles. '''
##        self.center,self.radius=self.__union((self.center,self.radius),(new_circle.center,new_circle.radius))
##
##    def __unionall(self,seq_circle): # list_circle_params : [((x1,y1),radius_1), ((x2,y2),radius_2), ...]
##        ''' returns ([x,y],radius) for the resultant union of all circles.
##            sequence_circle must be a sequence of circles. '''
##        temp_union= (self.center,self.radius)
##        for temp_circle in seq_circle:
##            temp_union = self.__union(temp_union,(temp_circle.center,temp_circle.radius))
##        return temp_union
##    def unionall(self,seq_circle): #seq_circle: sequence of circles
##        temp_union=self.__unionall(seq_circle)
##        return Circle(temp_union[0],temp_union[1])
    # end of Circle class
# functions outside all classes
def get_event_list(event_types=None,further_check_variable_name=None,further_check_value=None,list_to_get=None):#list_to_get is attached to a constant list here
    ''' Get the required events from the event_list.
        get_event_list([event_types],[further_check_variable_name],further_check_value=None,list_to_get=fun_Game.list_event):
        event_types (optional): event_name|list[event_name]
        get_event_list() -> returns whole event_list(to be precise, list_to_get)
        get_event_list(events) -> returns event_list(to be precise, list_to_get) filtered to contain only "events"
        get_event_list([events],further_check_variable_name="var_name",further_check_value=value) ->
        returns sub-list containing those elements of get_event_list([events]) for which var_name=value
        Potential candidates for list_to_get -> fun_Game.list_event, fun_Game.list_event_old, fun_Game.list_state_all_buttons, fun_Game.list_state_all_buttons_old'''
    if list_to_get==None:
        list_to_get=fun_Game.list_event_old
    if further_check_variable_name:
        further_check_enabled=True
    else:
        further_check_enabled=False
    if event_types:
        if not hasattr(event_types,"__iter__"):
            event_types=[event_types] # if not iterable, make a list out of it
    def func_filter():
        list_return=[]
        if not event_types:
            return list_to_get
        for temp_1 in list_to_get: # all events in fun_Game.list_event have a "type" property
            for temp_2 in event_types:
                if temp_1.type==temp_2:
                    list_return.append(temp_1)
        return list_return
    def further_check_filter(temp_list): # returns part of temp_list which passes further_check
        list_return=[]
        if further_check_enabled:
            for temp in temp_list:
                    if getattr(temp,further_check_variable_name)==further_check_value:# may raise error if further_check_variable_name is not present for all members of the list
                        list_return.append(temp)
        else:
            list_return=temp_list
        return list_return
    return further_check_filter(func_filter()) # returns elements common in fun_Game.list_events and events which are accepted after further_check
# end of get_event_list()

def distance((x1,y1),(x2,y2)): # Maybe make a non-square rooted function for comparison (faster)
    import math
    return(math.sqrt((x2-x1)**2+(y2-y1)**2))

#following constants are required for the next function
UNION=1
INTERSECTION=2
DIFFERENCE=3
ADD=4
MAKE_IT_VARIABLE_LIST=5 # for each member (usually objects) in the list, it is replaced by one of its variables
def operation_on_lists(operation,list1,list2=None,variable_name=None):
    ''' operation_on_lists(operation, list1, list2) -> list
        Does operation involving list1 and list2.
        variable_name is required only for MAKE_IT_VARIABLE_LIST operation. It is a string representing the variable name
        Valid operations are UNION, INTERSECTION, DIFFERENCE, ADD, MAKE_IT_VARIABLE_list '''
    def intersection():
        if list2==None:
            raise TypeError("second argument i.e. list2 should be a list")
        list_return=[]
        for temp1 in list1:
            for temp2 in list2:
                if temp1==temp2:
                    list_return.append(temp1)
        return list_return
    def union():
        if list2==None:
            raise TypeError("second argument i.e. list2 should be a list")
        list_return = uniquelist()
        list_return.extend(list1)
        list_return.extend(list2)
        return list_return
    def add():
        if list2==None:
            raise TypeError("second argument i.e. list2 should be a list")
        list_return=[]
        list_return.append(list1)
        list_return.append(list2)
        return list_return
    def difference():
        if list2==None:
            raise TypeError("second argument i.e. list2 should be a list")
        list_return=[]
        list_intersection=intersection()
        for temp1 in list1:
            if temp1 not in list_intersection:
                list_return.append(temp1)
        return list_return
    def make_it_variable_list(): # for each member (usually objects) in the list, it is replaced by one of its variables
        if variable_name==None:
            raise TypeError("variable_name should be a string")
        if not list2==None:
            raise TypeError("list2 should be None")
        return_list=[getattr(temp,variable_name) for temp in list1]

    if operation==UNION:
        return union()
    elif operation==INTERSECTION:
        return intersection()
    elif operation==DIFFERENCE:
        return difference()
    elif operation==ADD:
        return add()
    elif operation==MAKE_IT_VARIABLE_LIST:
        return make_it_variable_list()
    else:
         raise ValueError("Invalid operation name. Valid operations are UNION, INTERSECTION, DIFFERENCE.")
# end of operation_on_lists()

# Design tips I will use later
# IMP: always derive classes from object. Else, in python 2.x, they become old-style class which sucks.
# named tuples, arrays are better. use more of them. named tuples can be accessed.
# refactor code into proper modules as-well-as use better named functions and variables
# use enumerate() for getting the index and value of elements while looping through lists. This mistake done atleast 1 time.
# use xrange instead of range. It produces one at a time. range is replaced by xrange in python 3.x
# use reversed() for backward loops, sorted() for sorted order.
# instead of zip(), use izip().
# use key instead of comparator
# use iter(iter_type,sentinel_value) instead of for loops
# partial() makes a function with more number of argument to less number of argument
# use for/else instead of exit based on flags
# look at dict.iteritems() and dict.setdefaults
# learn defaultdicts and collections module