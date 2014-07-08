# only for python 2.x
# VERY IMP: Use weakrefs instead of list for fun_Game.list_class,\
# fun_Class.list_instance and fun_Class.list_update_func

from uniquelist import uniquelist  # imports uniquelist
import pygame
from pygame.locals import *  # imports the constants
import math
from utils import register, KW_EVENTS, fuzzy_match_event_name
from functools import partial
import logging

logging.basicConfig(level=logging.DEBUG)

IS_TEST_MODE = True

# Mouse constants
B_LEFT_CLICK = 1
B_RIGHT_CLICK = 3
B_MIDDLE_CLICK = 2
B_SCROLLUP = 4
B_SCROLLDOWN = 5

# Direction constants
TOP = 1
LEFT = 2
BOTTOM = 3
RIGHT = 4


class fun_Game(object):
    list_class = uniquelist()
    list_event = []  # event_list of this step
    list_event_old = []  # event_list of the previous step
    # A sequence of boolean representing the state of every key
    list_state_all_buttons = []
    # A sequence of boolean representing the state of every key of previous
    # step
    list_state_all_buttons_old = []

    def __init__(self, width, height, fps=30):
        pygame.init()
        self.fps = fps
        self.clock = pygame.time.Clock()
        self.width = width
        self.height = height
        self.test_init()

    def update_all_class(self):
        for temp_cls in fun_Game.list_class:
            for temp_count in temp_cls.list_instance:
                temp_count.update()

    def _cache_event_list(self):
        ''' Cache event_list in every step.
            All events in fun_Game.list_event have a "type" property which are the usual constants. '''
        fun_Game.list_event_old = fun_Game.list_event  # move current list to old list
        fun_Game.list_state_all_buttons_old = fun_Game.list_state_all_buttons

        fun_Game.list_event = pygame.event.get()
        # Returns a sequence of boolean representing the state of every key.
        # Use key constant values for indexing.
        fun_Game.list_state_all_buttons = pygame.key.get_pressed()
        # print fun_Game.list_event # debug message
    # control access to list_event
    # with getter, do something crazy for filtering
    # or a filtering function

    def test_init(self):
        ''' Empty function to be overloaded for extra init on test mode. '''
        pass

    def test_update(self):
        ''' Empty function to be overloaded for extra draw on test mode. '''
        pass

    def run(self):
        self.screen = pygame.display.set_mode([self.width, self.height])
        while True:
            # Todo: Add other update-related functions, there should be separate render_all_class()
            # Todo: Always exit on event_close : make it default behavior,
            # although override-able
            self._cache_event_list()
            self.update_all_class()
            self.test_update()
            # VERY IMPORTANT: Do a spare first step so that every variable / list gets initialized well. Start instant creation and execution from second step.
            # IMPORTANT: First do all fun_Game related stuff before dealing
            # with game objects.
            self.clock.tick(self.fps)
            # Should do display.update()
            pygame.display.flip()  # debug statement, should use display.update

    # Todo - Add crazy functions to allow other objects and instances finding
    # like GM
    # Todo - Easy way to take screenshot and save it as pic
    # Todo: Game testing module. Lets you compare screenshots and compare values with  pixelarray or surface.get_at
    # Also allows accessing different config values.


    # class fun_Game ends here


class meta_fun_Class(type):

    def __new__(cls, name, base, clsdict):
        temp_class = type.__new__(cls, name, base, clsdict)
        temp_class.__class__ = type
        fun_Game.list_class.append(temp_class)
        # by default, priority_order and depth depends on "when class was
        # defined"
        cls.priority_order = cls.depth = len(fun_Game.list_class)

        return temp_class


class fun_Class(object):
    __metaclass__ = meta_fun_Class
    list_instance = uniquelist()
    # list_update_func stores the list of functions to call in the given order.
    # It can be used for injecting custom user functions (remember order).
    # action_draw not added as it depends on depth
    list_update_func = uniquelist()
    # all the check functions added here. what they do: if event_<event_name>:
    # action_<event_name>

    list_check_func = uniquelist()
    # dict_action_func -> dict of action funcs, key=event_numb like KEYDOWN
    dict_action_func = {}

    def __init__(self, x, y, img=None):
        self.x = x
        self.y = y
        self.img = img  # img should be a fun_Image, but lets do that later
        fun_Class.list_instance.append(self)
        self.action_create()

    def update(self):
        '''calls all functions in list_update_func in the given order'''
        tmp_func = None
        for tmp_func in fun_Class.list_update_func:
            tmp_func(self)

    def draw(self):
        # do some blitting depending on self.img
        pass

    @classmethod
    def register_event(cls, event_name=None, func_to_register=None):
        '''
            @fun_Class.register_event() # @fun_Class.register_event === @fun_Class.register_event()
            def event_key_down(ev):
                pass
            OR
            @fun_Class.register_event(event_name) # event_name=KEYDOWN (or "key_down")
            def whatever(ev):
                pass
            OR
            fun_Class.register_event(event_name,func)
        '''
        if (event_name is None) and (func_to_register is None):
            # i.e No param passed, used as decorator (1st step of ex. 1)
            logging.info("Nothing passed")
            return cls.register_event
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
                return cls.register_event(event_name, func_to_register)
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

    @register(list_update_func)
    def action_begin_step(self):
        pass

    @register(list_update_func)
    def action_step(self):
        tmp = self.event_mouse_click()
        if tmp:
            print tmp
        print(self.mouse_get_focused())

    @register(list_update_func)
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
    # so lets define event_<event_name>,action_<event_name>,check_<event_name>
    # for each <event_name>

    # keyboard handling (later move to keyboard module)

    # occurs if the key was held down continously since the last step
    def event_key_pressed(self, key_value):  # check if it works
        if get_event_list(list_to_get=fun_Game.list_state_all_buttons)[key_value] \
                and get_event_list(list_to_get=fun_Game.list_state_all_buttons_old)[key_value]\
                and (not get_event_list(event_types=KEYUP, further_check_variable_name="key", further_check_value=key_value))\
                and (not get_event_list(event_types=KEYUP, further_check_variable_name="key", further_check_value=key_value, list_to_get=fun_Game.list_event_old)):
            return True

    def action_key_pressed(self, key_value):
        pass

    def check_key_pressed(self):
        pass  # Todo: think about how to do it

    # occurs if the key is held at the moment (live)
    def event_key_pressed_live(self, key_value):  # check if it works
        ''' Returns True if the key (represented by key_code) is currently pressed.
            Problem is that this function is live. Returns True if the key is pressed at that moment.
            So, for example, two calls in two consecutive steps may return True although the key has been left in the meantime. '''
        temp_all_buttons = get_event_list(
            list_to_get=fun_Game.list_state_all_buttons)  # Returns a sequence of boolean representing the state of every key. Use key constant values for indexing.
        if temp_all_buttons[key_value]:  # indexing by key_value
            return True

    def action_key_pressed_live(self, key_value):
        pass

    def check_key_pressed_live(self):
        # Returns a sequence of boolean representing the state of every key.
        # Use key constant values for indexing.
        temp_all_buttons = get_event_list(
            list_to_get=fun_Game.list_state_all_buttons)
        # temp represents the key code in numbers as it is the index of
        # list_state_all_buttons indirectly
        for temp in range(len(temp_all_buttons)):
            if temp_all_buttons[temp]:
                self.action_key_pressed_live(temp)  # temp is the keycode

    # occurs if a key press occurs (i.e. pushed down)
    # key repetations may occur as the list is cached per step and there might
    # be multiple (same key)press per step.
    def event_key_down(self, key=None):
        if key is None:
            return get_event_list(KEYDOWN)
        else:
            return get_event_list(KEYDOWN, "key", key)

    def action_key_down(self, key):
        pass

    def check_key_down(self):
        for temp in get_event_list(KEYDOWN):
            action_key_down(self, temp.key)

    # probably wierd thing to do - define all <>_key_down as equivalent to
    # <>_key_press
    event_key_press = event_key_down
    action_key_press = action_key_down
    check_key_press = check_key_down

    # occurs if key is released
    def event_key_up(self, key=None):
        if key is None:
            return get_event_list(KEYUP)
        else:
            return get_event_list(KEYUP, "key", key)

    def action_key_up(self, key):
        pass

    def check_key_up(self):
        for temp in get_event_list(KEYUP):
            action_key_up(self, temp.key)
    # Todo: Do other key and keyboard related functions (look at GM for related functions)
    # Mouse handling (later move it to mouse module)
    # Mouse constants (defined at top - move them to a constants module, which will be imported in the global namespace)
    # mouse click

    def event_mouse_click(self, button=None):
        if button is None:
            return get_event_list(event_types=MOUSEBUTTONDOWN)
        else:
            return get_event_list(event_types=MOUSEBUTTONDOWN, further_check_variable_name="button", further_check_value=button)

    def action_mouse_click(self, button):
        pass

    def check_mouse_click(self):
        list_temp = get_event_list(event_types=MOUSEBUTTONDOWN)
        for temp in list_temp:
            action_mouse_click(temp.button)
    # mouse get pressed

    def event_mouse_get_pressed(self, button=None):
        ''' event_mouse_get_pressed() -> tuple looking like (1,0,0) i.e. ( left_click_state, middle_click_state, right_click_state ).
            Use an index which is (corresponding_constant - 1). For eg event_mouse_get_pressed()[0] returns left click state.
            event_mouse_get_pressed(button) -> Returns 0 or 1 depending on pressed or not. '''
        if button is None:
            return pygame.mouse.get_pressed()
        else:
            # because the tuple returned has o-based indexing
            return pygame.mouse.get_pressed()[button - 1]
    # end of mouse handling
    # other mouse-based functions

    def mouse_get_focused(self):
        return pygame.mouse.get_focused()

    def mouse_set_visible(self, bool_value):
        return pygame.mouse.set_visible(bool_value)

    def mouse_get_rel(self):
        ''' Returns relative movement of the mouse since the last call to this function.
            mouse_get_rel() -> (x,y) '''
        return pygame.mouse.get_rel()

    def mouse_set_cursor_image(self, image=None):
        pass  # todo: complete after the image part is done
    # implement mouse_pos as variable

    @property
    def mouse_pos(self):
        ''' mouse_pos -> (x,y)
            mouse_pos = [x,y] -> Sets cursor position '''
        return pygame.mouse.get_pos()

    @mouse_pos.setter
    def mouse_pos(self, val):
        ''' val should be a list [x,y] '''
        if not isinstance(val, list):
            raise TypeError("val should be a list [x,y]")
        pygame.mouse.set_pos(val)

    # implement mouse_x as variable
    @property
    def mouse_x(self):
        ''' mouse_x -> x
            mouse_x = some_x -> Sets cursor x position '''
        return pygame.mouse.get_pos()[0]  # get_pos -> (x,y)

    @mouse_x.setter
    def mouse_x(self, x):
        pygame.mouse.set_pos([x, mouse_y])

    # implement mouse_y as variable
    @property
    def mouse_y(self):
        ''' mouse_y -> y
            mouse_y = some_y -> Sets cursor y position '''
        return pygame.mouse.get_pos()[1]  # get_pos -> (x,y)

    @mouse_y.setter
    def mouse_y(self, y):
        pygame.mouse.set_pos([mouse_x, y])
    # end of mouse-related function
    # other various events

    # todo: test after image part is done
    def event_intersect_room_boundary(self):
        ''' Checks if the object (its image bounding box) is intersecting the room boundary, but not totally outside the room.
            Returns direction constants like TOP, LEFT, BOTTOM, RIGHT. '''
        if (self.x + self.image.bbox.width / 2) > fun_Game.room_width and not (self.x - self.image.bbox.width / 2) > fun_Game.room_width:
            return RIGHT  # all constants defined at global level
        elif (self.y + self.image.bbox.height / 2) > fun_Game.room_height and not (self.y - self.image.bbox.height / 2) > fun_Game.room_height:
            return BOTTOM
        elif (self.x - self.image.bbox.width / 2) < 0 and not (self.x + self.image.bbox.width / 2) < 0:
            return LEFT
        elif (self.y - self.image.bbox.height / 2) < 0 and not (self.y + self.image.bbox.height / 2) < 0:
            return TOP

    def action_intersect_room_boundary(self):
        pass

    def check_intersect_room_boundary(self):
        if event_intersect_room_boundary(self):
            action_intersect_room_boundary(self)

    def event_outside_room_boundary(self):
        ''' Checks if the object (its image bounding box) is totally outside room.
            Returns direction constants like TOP, LEFT, BOTTOM, RIGHT. '''
        if (self.x - self.image.bbox.width / 2) > fun_Game.room_width:
            return RIGHT  # all constants defined at global level
        elif (self.y - self.image.bbox.height / 2) > fun_Game.room_height:
            return BOTTOM
        elif (self.x + self.image.bbox.width / 2) < 0:
            return LEFT
        elif (self.y + self.image.bbox.height / 2) < 0:
            return TOP

    # end of fun_Class
# Other classes


class Circle(object):

    def __init__(self, (x, y), radius, color=None):
        self.center = [x, y]
        self.radius = radius
        self.color = color

    @property
    def center_x(self):
        return self.center[0]

    @property
    def center_y(self):
        return self.center[1]

    @center_x.setter
    def center_x(self, new_x):
        self.center[0] = new_x

    @center_y.setter
    def center_y(self, new_y):
        self.center[1] = new_y

    @property
    def bbox(self):
        left = self.center_x - self.radius
        top = self.center_y - self.radius
        width = self.radius * 2
        height = self.radius * 2
        return pygame.Rect(left, top, width, height)
    # todo: remember about the colour. document - center is list unlike tuple
    # in case of rect.

    def __repr__(self):
        return "{0.__class__}( center={0.center}, radius={0.radius}, color={0.color})".format(self)

    def copy(self):
        return Circle((self.center_x, self.center_y), self.radius, self.color)

    def move(self, move_x, move_y):
        return Circle((self.center_x + move_x, self.center_y + move_y), self.radius, self.color)

    def move_ip(self, move_x, move_y):
        self.center_x += move_x
        self.center_y += move_y

    def inflate(self, inflate_radius):
        return Circle((self.center_x, self.center_y), self.radius + inflate_radius, self.color)

    def inflate_ip(self, inflate_radius):
        self.radius += inflate_radius

    def is_inside(self, another_circle):
        ''' Checks if this circle is fully inside another_circle '''
        return distance(self.center, another_circle.center) < self.radius

    def is_inside_mutual(self, another_circle):
        ''' Checks if this circle is fully inside another_circle and also the opposite.
            2x Faster than using is_inside for both of them. '''
        return (distance(self.center, another_circle.center) < max(self.radius, another_circle.radius))

    def collide_circle(self, another_circle):
        ''' Checks if this circle intersects with another_circle. '''
        return (distance(self.center, another_circle.center) <= (self.radius + another_circle.radius))

    def collide_point(self, (point_x, point_y)):
        ''' Checks if (point_x, point_y) is inside this circle. '''
        return (distance(self.center, (point_x, point_y)) <= self.radius)

    def collide_list_circle(self, list_circle):
        ''' Checks if this circle intersects with any of the circles in circle_list. '''
        for circle in list_circle:
            if collide_circle(self, circle):
                return True
        else:  # else of the for loop
            return False

    def collide_list_all_circle(self, list_circle):
        ''' Checks if this circle intersects with all of the circles in circle_list. '''
        for circle in list_circle:
            if not collide_circle(self, circle):
                return False
        else:  # else of the for loop
            return True

    def collide_rect(self, another_rect):
        ''' Checks if this circle collides with another_rect. '''
        return not ((self.center_x + self.radius) < another_rect.left or (self.center_x - self.radius) > another_rect.right or (self.center_y + self.radius) < another_rect.top or (self.center_y - self.radius) > another_rect.bottom)

    def collide_list_rect(self, list_rect):
        ''' Returns True if collides with any of the rect in the list. '''
        for temp_rect in list_rect:
            if collide_rect(self, temp_rect):
                return True
        else:
            return False

    def collide_list_all_rect(self, list_rect):
        ''' Returns True if collides with all the rect in the list. '''
        for temp_rect in list_rect:
            if not collide_rect(self, temp_rect):
                return False
            else:
                return True

    @classmethod
    # create a circle with same center and radius=sqrt(w^2+h^2)
    def get_circumcircle_from_rect(cls, another_rect):
        import math
        return cls(another_rect.center, math.sqrt(another_rect.width ** 2 + another_rect.height ** 2) / 2)

    @classmethod
    # radius of incircle is same as the min of width and height (as it's not a
    # square)
    def get_incircle_from_rect(cls, another_rect):
        import math
        return cls(another_rect.center, min(another_rect.width, another_rect.height))

    # union -needs to be a circle *within* which the union of the bounding box of all the circles can be fit.
    # warning about all the union functions: The circles returned are not
    # necessarily the most optimum union circle, but it will surely contain
    # the others.
    def _union(self, circle_1, circle_2):
        ''' self.__union((new_center_x,new_center_y),new_radius) -> ([x,y],radius) which are the resultant values. '''
        return self.circumcircle_from_rect(circle_1.bbox.union(circle_2.bbox))

    def union(self, new_circle):
        ''' Returns a new circle which is the union of these two circles '''
        return self._union(self, new_circle)

    def union_ip(self, new_circle):
        ''' Turns this circle into a circle which is a union of these two circles. '''
        temp_circle = self._union(self, new_circle)
        self.center, self.radius = temp_circle.center, temp_circle.radius

    # list_circle_params : [((x1,y1),radius_1), ((x2,y2),radius_2), ...]
    def _unionall(self, circle_1, seq_circle):
        ''' returns ([x,y],radius) for the resultant union of all circles.
            sequence_circle must be a sequence of circles. '''
        return self.circumcircle_from_rect(circle_1.bbox.unionall([temp_circle.bbox for temp_circle in seq_circle]))

    def unionall(self, seq_circle):  # seq_circle: sequence of circles
        return self._unionall(self, seq_circle)

    def unionall_ip(self, seq_circle):
        ''' Turns this circle into a circle which is a union of this circles with all circles in seq_circle'''
        temp_circle = self._unionall(self, seq_circle)
        self.center, self.radius = temp_circle.center, temp_circle.radius

    # draw functions
    def draw(self, surface, (x, y)=(None, None), color=None, width=1, use_antialiasing=False):
        ''' Draws this Circle on surface. It must be of width and height greater than or equal to its bbox.
            (x,y)->co-ordinates whether the center of the Circle should be drawn on the surface.
            width argument doesnt work with antialiasing. width=0 makes it filled.
            antialiasing may break in later versions as the backend pygame.gfxdraw is experimental.
            color falls back first to Circle.color (if present) and then to blue color.'''
        if (x, y) == (None, None):
            (x, y) = self.center
        if not color:
            if self.color:
                color = self.color
            else:
                color = pygame.Color("blue")

        if not use_antialiasing:
            pygame.draw.circle(surface, color, (x, y), self.radius, width)
        else:
            pygame.gfxdraw.aacircle(surface, x, y, self.radius, color)

    def get_surface(self, surface=None, flags=0):
        ''' Returns a new surface with dimensions of (Circle.bbox.width,Circle.bbox.width) and other properties as surface.
            This Circle can be safely drawn on it.'''
        if surface:
            return pygame.Surface((self.bbox.width, self.bbox.height), flags, surface)
        else:
            return pygame.Surface((self.bbox.width, self.bbox.height), flags)

    def get_surface_drawn(self, (x, y)=(None, None), color=None, width=1, use_antialiasing=False, surface=None, flags=0):
        ''' Returns a surface which has the tiltedRect drwan on it. '''
        temp_surf = self.get_surface(surface, flags)
        self.draw(temp_surf, (x, y), color, width, use_antialiasing)
        return temp_surf

    # end of Circle class
    # start of tiltedRect class


class tiltedRect(pygame.Rect):
    # make a metaclass which wraps a lot of functions just like move is defined below.
    # functions to be wrapped - move,inflate
    # Think about them - clamp,clip,union,fit,contains,collide
    # the metaclass can probably also change the __str__ of the class.
    # About drawing - use pygame.transform.rotate to get a rotated surface to
    # be drawed.

    def __init__(self, (left, top), (width, height), angle, centered_coords=False, color=None):
        ''' Angle in degrees.
            centered_coords -> whether the (left,top) is actually intended to be (center_x,center_y) or not.
            I.e. if centered_coords==True the (left,top) co-ordinates are used as (center_x,center_y) co-ordinates of the tiltedRect'''
        self.angle = angle
        self.color = color
        if centered_coords:
            left = left - width / 2
            top = top - height / 2
        super(tiltedRect, self).__init__((left, top), (width, height))

    def __copy__(self):
        return tiltedRect((self.left, self.top), (self.width, self.height), self.angle)

    def __repr__(self):
        return "{0.__class__.__name__}((top={0.top}, left={0.left}), (width={0.width}, height={0.height}), angle={0.angle}, color={0.color})".format(self)

    @classmethod
    def create_from_rect(cls, another_rect, angle):
        return cls((another_rect.left, another_rect.top), (another_rect.width, another_rect.height), angle)

    def get_rect(self):
        return pygame.Rect((left, top), (width, height))

    def move(self, x, y):
        return self.create_from_rect(super(tiltedRect, self).move(x, y), self.angle)

    def inflate(self, x, y):
        return self.create_from_rect(super(tiltedRect, self).inflate(x, y), self.angle)

    def normalize(self):  # not sure what this one does - ask others
        return self.create_from_rect(super(tiltedRect, self).normalize(), self.angle)

    def rotate(self, some_angle):
        temp_return = self.__copy__()
        temp_return.angle += some_angle
        return temp_return

    def rotate_ip(self, some_angle):
        self.angle += some_angle

    # generalise the parameters to accept x1,y1,x2,y2,rot_angle
    def rotate_point_relative(self, x, y, theta=None):
        ''' x,y -> Absolute co-ords of the point to be rotated wrt to the rectangles center. self.centerx,self.centery are internally substracted from them.
            theta -> angle (in degrees) by which the point is to be rotated. Default value is self.angle.
            Returns absolute positions of the points after rotation. '''
        if theta is None:
            theta = self.angle
        return self.rotate_point(x, y, self.centerx, self.centery, theta)

    @classmethod
    # to be allowed as rotate_point(class)
    def rotate_point(cls, x, y, origin_x, origin_y, theta):
        ''' x,y -> Absolute co-ords of the point to be rotated. origin_x,origin_y are internally substracted from them.
            (origin_x,origin_y) -> Absolute co-ords of the origin wrt to which the point will be rotated
            theta -> angle (in degrees) by which the point is to be rotated.
            Returns absolute positions of the points after rotation. '''
        import math
        x_diff = x - origin_x
        y_diff = y - origin_y
        # -y_diff because of the inverted nature of y co-ordinate system in pygame
        y_diff = -y_diff
        r = math.sqrt(x_diff ** 2 + y_diff ** 2)
        initial_angle = math.atan2(y_diff, x_diff)
        final_angle = initial_angle + math.radians(theta)
        rotated_x_diff = r * math.cos(final_angle)
        rotated_y_diff = r * math.sin(final_angle)
        rotated_y_diff = -rotated_y_diff  # - used for same reason as above
        rotated_x = rotated_x_diff + origin_x
        rotated_y = rotated_y_diff + origin_y
        return (rotated_x, rotated_y)

    def rotate_point_polar(self, r, initial_angle, theta=None):
        ''' theta and initial_angle in radians.
            initial_angle ->angle r makes with horizontal.
            theta -> angle to be rotated by. '''
        if theta is None:
            theta = self.angle
        final_angle = initial_angle + theta
        rotated_x = r * math.cos(final_angle)
        rotated_y = r * math.sin(final_angle)
        return (rotated_x, rotated_y)

    @property
    def bottomleft_rotated(self):
        temp = self.bottomleft
        return self.rotate_point_relative(temp[0], temp[1])

    @property
    def topleft_rotated(self):
        temp = self.topleft
        return self.rotate_point_relative(temp[0], temp[1])

    @property
    def bottomright_rotated(self):
        temp = self.bottomright
        return self.rotate_point_relative(temp[0], temp[1])

    @property
    def topright_rotated(self):
        temp = self.topright
        return self.rotate_point_relative(temp[0], temp[1])

    @property
    def midleft_rotated(self):
        temp = self.midleft
        return self.rotate_point_relative(temp[0], temp[1])

    @property
    def midright_rotated(self):
        temp = self.midright
        return self.rotate_point_relative(temp[0], temp[1])

    @property
    def midtop_rotated(self):
        temp = self.midtop
        return self.rotate_point_relative(temp[0], temp[1])

    @property
    def midbottom_rotated(self):
        temp = self.midbottom
        return self.rotate_point_relative(temp[0], temp[1])

    # related to bounding box
    @property
    def bbox(self):
        list_x = [self.topleft_rotated[0], self.topright_rotated[0],
                  self.bottomleft_rotated[0], self.bottomright_rotated[0]]
        list_y = [self.topleft_rotated[1], self.topright_rotated[1],
                  self.bottomleft_rotated[1], self.bottomright_rotated[1]]
        min_x = floor(min(list_x))
        max_x = ceil(max(list_x))
        min_y = floor(min(list_y))
        max_y = floor(max(list_y))
        return pygame.Rect((min_x, min_y), (max_x - min_x, max_y - min_y))
    # corners

    @property
    def corners(self):
        ''' List of actual (rotated) corners. '''
        return [self.topleft_rotated, self.topright_rotated, self.bottomright_rotated, self.bottomleft_rotated]

    @property
    def corners_relative(self):
        return [(temp[0] - self.centerx, temp[1] - self.centery) for temp in self.corners]

    # circles related to the rect
    def get_circumcircle(self):
        Circle.get_circumcircle_from_rect(self.bbox)

    def get_incircle(self):
        Circle.get_incircle_from_rect(self.bbox)

    # collision events
    def collide_point(self, *args):
        ''' collidepoint(x,y) ->
            collidepoint((x,y)) -> '''
        temp_len = len(args)
        temp_x = None
        temp_y = None
        if temp_len == 2:
            temp_x = args[0]
            temp_y = args[1]
        elif temp_len == 1:
            if len(args[0]) == 2:
                temp_x, temp_y = args[0]
            else:
                raise TypeError("Arguments are of incorrect type")
        else:
            raise TypeError("Arguments are of incorrect type")
        if temp_x is None or temp_y is None:
            raise TypeError("argument must contain two numbers")
        return pygame.Rect((self.left, self.top), (self.width, self.height)).collidepoint(self.rotate_point_relative(temp_x, temp_y))

    def collide_rect(self, rect):
        ''' Tests if it collides with rect, which should be instance of rect class. '''
        # First test:whether bbox collides with rect. If not, no collision.
        if not self.bbox.colliderect(rect):
            return False
        else:
        # Todo: Else sure test: Need to do line class first. Test if any line
        # of titedRect collides with any line of (instead, the whole) rect.
            pass

    # draw functions
    def draw(self, surface, (x, y)=(None, None), color=None, width=1, use_antialiasing=False, blend=True):
        ''' Draws this tiltedRect on surf_to_draw_on. It must be of width and height greater or equal to its bbox.
            (x,y)->co-ordinates whether the lefttop point of its bbox should be drawn on the surface.
            width argument doesnt work with antialiasing. width=0 makes it filled.
            blend argument works only with antialiasing. The boolean blend argument set to true will blend the shades with existing shades instead of overwriting them.
            color falls back first to tiltedRect.color (if present) and then to blue color.'''
        if (x, y) == (None, None):
            (x, y) = (0, 0)
        if not color:
            if self.color:
                color = self.color
            else:
                color = pygame.Color("blue")
        iter_corners = [(temp[0] + x, temp[1] + y)
                        for temp in self.corners_relative]
        if not use_antialiasing:
            pygame.draw.polygon(surface, color, iter_corners, width)
        else:
            pygame.draw.aalines(surface, color, True, iter_corners, blend)

    def get_surface(self, surface=None, flags=0):
        ''' Returns a new surface with dimensions of (tiltedRect.bbox.width,tiltedRect.bbox.width) and other properties as surface.
            This tiltedRect can be safely drawn on it.'''
        if surface:
            return pygame.Surface((self.bbox.width, self.bbox.height), flags, surface)
        else:
            return pygame.Surface((self.bbox.width, self.bbox.height), flags)

    def get_surface_drawn(self, (x, y)=(None, None), color=None, width=1, use_antialiasing=False, blend=True, surface=None, flags=0):
        ''' Returns a surface which has the tiltedRect drwan on it. '''
        temp_surf = self.get_surface(surface, flags)
        self.draw(temp_surf, (x, y), color, width, use_antialiasing, blend)
        return temp_surf

    def collide_tiltedRect(self, another_tiltedRect):
        '''Checks whether this tiltedRect collides with another_titltedrect, which must be a instance of titledRect. '''
        # Rotates both tiltedRect by -another_tiltedRect.angle. So, another_tiltedRect becomes a Rect called temp_Rect.
        # Then check if the rotated version of this tiltedRect
        # (temp_tiltedRect) collides with the obtained Rect.
        temp_tiltedRect = self.rotate(-another_tiltedRect.angle)
        temp_Rect = another_tiltedRect.get_rect()
        return temp_tiltedRect.colliderect(temp_Rect)

# functions outside all classes


# list_to_get is attached to a constant list here
def get_event_list(event_types=None, further_check_variable_name=None, further_check_value=None, list_to_get=None):
    ''' Get the required events from the event_list.
        get_event_list([event_types],[further_check_variable_name],further_check_value=None,list_to_get=fun_Game.list_event):
        event_types (optional): event_name|list[event_name]
        get_event_list() -> returns whole event_list(to be precise, list_to_get)
        get_event_list(events) -> returns event_list(to be precise, list_to_get) filtered to contain only "events"
        get_event_list([events],further_check_variable_name="var_name",further_check_value=value) ->
        returns sub-list containing those elements of get_event_list([events]) for which var_name=value
        Potential candidates for list_to_get -> fun_Game.list_event, fun_Game.list_event_old, fun_Game.list_state_all_buttons, fun_Game.list_state_all_buttons_old'''
    if list_to_get is None:
        list_to_get = fun_Game.list_event_old
    if further_check_variable_name:
        further_check_enabled = True
    else:
        further_check_enabled = False
    if event_types:
        if not hasattr(event_types, "__iter__"):
            # if not iterable, make a list out of it
            event_types = [event_types]

    def func_filter():
        list_return = []
        if not event_types:
            return list_to_get
        # all events in fun_Game.list_event have a "type" property
        for temp_1 in list_to_get:
            for temp_2 in event_types:
                if temp_1.type == temp_2:
                    list_return.append(temp_1)
        return list_return

    # returns part of temp_list which passes further_check
    def further_check_filter(temp_list):
        list_return = []
        if further_check_enabled:
            for temp in temp_list:
                # may raise error if further_check_variable_name is not present
                # for all members of the list
                if getattr(temp, further_check_variable_name) == further_check_value:
                    list_return.append(temp)
        else:
            list_return = temp_list
        return list_return
    # returns elements common in fun_Game.list_events and events which are
    # accepted after further_check
    return further_check_filter(func_filter())
# end of get_event_list()


# Maybe make a non-square rooted function for comparison (faster)
def distance((x1, y1), (x2, y2)):
    import math
    return(math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2))

# following constants are required for the next function
UNION = 1
INTERSECTION = 2
DIFFERENCE = 3
ADD = 4
# for each member (usually objects) in the list, it is replaced by one of
# its variables
MAKE_IT_VARIABLE_LIST = 5


def operation_on_lists(operation, list1, list2=None, variable_name=None):
    ''' operation_on_lists(operation, list1, list2) -> list
        Does operation involving list1 and list2.
        variable_name is required only for MAKE_IT_VARIABLE_LIST operation. It is a string representing the variable name
        Valid operations are UNION, INTERSECTION, DIFFERENCE, ADD, MAKE_IT_VARIABLE_list '''
    def intersection():
        if list2 is None:
            raise TypeError("second argument i.e. list2 should be a list")
        list_return = []
        for temp1 in list1:
            for temp2 in list2:
                if temp1 == temp2:
                    list_return.append(temp1)
        return list_return

    def union():
        if list2 is None:
            raise TypeError("second argument i.e. list2 should be a list")
        list_return = uniquelist()
        list_return.extend(list1)
        list_return.extend(list2)
        return list_return

    def add():
        if list2 is None:
            raise TypeError("second argument i.e. list2 should be a list")
        list_return = []
        list_return.append(list1)
        list_return.append(list2)
        return list_return

    def difference():
        if list2 is None:
            raise TypeError("second argument i.e. list2 should be a list")
        list_return = []
        list_intersection = intersection()
        for temp1 in list1:
            if temp1 not in list_intersection:
                list_return.append(temp1)
        return list_return

    # for each member (usually objects) in the list, it is replaced by one of
    # its variables
    def make_it_variable_list():
        if variable_name is None:
            raise TypeError("variable_name should be a string")
        if not list2 is None:
            raise TypeError("list2 should be None")
        return_list = [getattr(temp, variable_name) for temp in list1]

    if operation == UNION:
        return union()
    elif operation == INTERSECTION:
        return intersection()
    elif operation == DIFFERENCE:
        return difference()
    elif operation == ADD:
        return add()
    elif operation == MAKE_IT_VARIABLE_LIST:
        return make_it_variable_list()
    else:
        raise ValueError(
            "Invalid operation name. Valid operations are UNION, INTERSECTION, DIFFERENCE.")
# end of operation_on_lists()

# Todo: see below
# 1. Allow rect-like and circle-like constructs wherever rect and circle are expected.
# 2. Do all sort of type-checking.
# 3.Use sprites and groups in pygame as containers
# Imp: Allow debugging with event handlers and others with @debug

# Design tips I will use later
# IMP: always derive classes from object. Else, in python 2.x, they become old-style class which sucks.
# use tuples instead of lists wherver possible because they are usually faster to create
# learn about generators
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
