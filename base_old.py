# only for python 2.x
# VERY IMP: Use weakrefs instead of list for fun_Game.list_class,\
# fun_Class.list_instance and fun_Class.list_update_func

from uniquelist import uniquelist  # imports uniquelist
import pygame
from pygame.locals import *  # imports the constants
import math
from utils import register_class, meta_accessor_class, register_event, selfie, KW_EVENTS_IB, sort_events, append_user_events, fuzzy_match_event_name, KW_EVENTS_ALL, rect_to_pygame_rect
# import utils
from functools import partial
from sprite_types import Circle, Rect
import logging
from copy import deepcopy
from math_utils import atan2_inv

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

    @property
    def w(self):
        return self.width

    @w.setter
    def w(self, val):
        self.width = val

    @property
    def h(self):
        return self.height

    @h.setter
    def h(self, val):
        self.height = val

# @classmethod
# def _register_class_(cls, class_to_register):
# ''' Registers class_to_register to its list_class '''
# cls.list_class.append(class_to_register)
    @classmethod
    def register_class(cls, cls_to_register):
        cls.list_class.append(cls_to_register)

    @classmethod
    def update_all_class(cls):
        for tmp_cls in cls.list_class:
            tmp_cls.update_instances(cls.list_event)

    @classmethod
    def process_event_list(cls, list_event_):
        append_user_events(list_event_)
        cls.list_event.sort(sort_events)

    @classmethod
    def _cache_event_list(cls):
        ''' Cache event_list in every step.
            All events in fun_Game.list_event have a "type" property which are the usual constants. '''
        cls.list_event_old = cls.list_event  # move current list to old list
        cls.list_state_all_buttons_old = cls.list_state_all_buttons

        cls.list_event = pygame.event.get()
        cls.process_event_list(cls.list_event)
        # Returns a sequence of boolean representing the state of every key.
        # Use key constant values for indexing.
        cls.list_state_all_buttons = pygame.key.get_pressed()
        # print cls.list_event  # debug message
    # control access to list_event
    # with getter, do something crazy for filtering
    # or a filtering function

    @classmethod
    def for_all_instance(cls, func_to_run, flatten):
        ''' Note: flatten can be "level-instance" or "level-class" or False'''
        return_list = []
        for tmp_cls in cls.list_class:
            return_item = tmp_cls.for_all_instance(
                func_to_run, flatten=flatten)
            if flatten == "level-instance" or flatten == "level-class":
                return_list.extend(return_item)
            else:
                return_list.append(return_item)
        return return_list

    @classmethod
    def for_all_class(cls, func_to_run, flatten):
        ''' Note: flatten can be True or False'''
        return_list = []
        for tmp_class in cls.list_class:
            return_item = func_to_run(tmp_class)
            if flatten:
                return_list.extend(return_item)
            else:
                return_list.append(return_item)
        return return_list

    @staticmethod
    def collect_self_clear_rect(self):
        _list_clear_rect = []
        _list_rendered_sprite = []
        # perf hog: search for better way to remove list items iteratively
        for tmp_old_sprite in self.list_rendered_sprite:
            if (not tmp_old_sprite.get("still_valid")):
                # returns bbox of all list_rendered_sprite that are not still_valid, after removing them from that list
                # so, list now contains only of the older sprites still_valid
                tmp_clear_rect_bbox = tmp_old_sprite["bbox"]
                _list_clear_rect.append(tmp_clear_rect_bbox)
            else:
                _list_rendered_sprite.append(tmp_old_sprite)
            if ("still_valid" in tmp_old_sprite):
                tmp_old_sprite.pop("still_valid")

        # in next step :
        # _list_rendered_sprite.append(self.list_dirty_sprite)
        # self.list_dirty_sprite=[]
        self.list_rendered_sprite = _list_rendered_sprite
        return _list_clear_rect

    @staticmethod
    def collect_self_rendered_sprite(self):
        return self.list_rendered_sprite

    @staticmethod
    def collect_self_dirty_sprite(self):
        return self.list_dirty_sprite

    @staticmethod
    def move_dirty_to_rendered(self):
        self.list_rendered_sprite.extend(self.list_dirty_sprite)
        self.list_dirty_sprite = []
        return None

    def blit_all_class(self):
        # step 1: collect all clear rects
        # i.e. remove last_rendered_rects which are not still_valid and return them
        # also move to_be_rendered_sprites into that list and clear dirty list
        list_clear_rect = self.for_all_instance(
            self.collect_self_clear_rect, flatten="level-instance")
        list_rendered_sprite = self.for_all_instance(
            self.collect_self_rendered_sprite, flatten="level-instance")
        list_dirty_sprite = self.for_all_instance(
            self.collect_self_dirty_sprite, flatten="level-instance")

        # step 2: check if any clear_rect intersects with last_rendered_rects,
        # return a list of dirty overlay for those last_rendered_rects.
        # also if it is contained (totally within), mark clear_rect for removal
        list_dirty_overlay_sprite = []
        list_cancelled_clear_rect = []
        for tmp_old_sprite in list_rendered_sprite:
            for tmp_clear_rect in list_clear_rect:
                tmp_intersect_rect = tmp_clear_rect.clip(
                    tmp_old_sprite["bbox"])
                if tmp_intersect_rect.w > 0 and tmp_intersect_rect.h > 0:
                    # make blit funcs capable of taking a clip rect, will be appplied before blitting
##                        print("explicit blit")
                    copy_old_sprite = deepcopy(tmp_old_sprite)
                    copy_old_sprite["clip_rect"] = tmp_intersect_rect
                    list_dirty_overlay_sprite.append(copy_old_sprite)

                    if tmp_old_sprite["bbox"].contains(tmp_clear_rect):
                        # Cancel clear rect
                        list_cancelled_clear_rect.append(tmp_clear_rect)

                else:
                    # No explicit blit
                    pass
        # step 3: for every clear_rect not marked for removal, do the
        # clear_rects.
# print "Clear_rects= ",len(list_clear_rect)-len(list_cancelled_clear_rect)
        i = 0
        for tmp_clear_rect in list_clear_rect:
            # convert to pygame rect
            if not (tmp_clear_rect in list_cancelled_clear_rect):
                self.screen.fill(pygame.Color(0, 0, 0, 1), tmp_clear_rect)
                i += 1
        print "i=", i

        # step 4: do blit for all dirty_sprite and dirty_overlay
        for tmp_dirty_sprite in list_dirty_sprite:
            tmp_dirty_sprite["sprite"].blit(self.screen)

# print "Dirty_overlays= ",len(list_dirty_overlay_sprite)
# print list_dirty_overlay_sprite
        for tmp_overlay_sprite in list_dirty_overlay_sprite:
            new_overlay_sprite = tmp_overlay_sprite[
                "sprite"].__class__(**tmp_overlay_sprite["config"])
            new_overlay_sprite.blit(
                self.screen, clip_rect=tmp_overlay_sprite["clip_rect"])

        # step 5: update display
        list_display_update = [tmp_dirty_sprite["bbox"]
                               for tmp_dirty_sprite in list_dirty_sprite] + list_clear_rect
        pygame.display.update(list_display_update)
# if not (list_dirty_sprite[0]["sprite"].bbox in list_display_update):
# print("problem")

        # step 6: cleaning jobs
        self.for_all_instance(self.move_dirty_to_rendered, flatten=False)
# pygame.display.flip()

    def test_init(self):
        ''' Empty function to be overloaded for extra init on test mode. '''
        pass

    def test_update(self):
        ''' Empty function to be overloaded for extra draw on test mode. '''
        pass

    def run(self):
        self.screen = pygame.display.set_mode([self.width, self.height])
        frame_no = 0
        while True:
            # Todo: Always exit on event_close : make it default behavior,
            # although override-able
            frame_no += 1
            # print frame_no
            self._cache_event_list()
            self.update_all_class()
            self.blit_all_class()
            self.test_update()
            # VERY IMPORTANT: Do a spare first step so that every variable / list gets initialized well.
            # Start instant creation and execution from second step.
            # IMPORTANT: First do all fun_Game related stuff before dealing
            # with game objects.
            self.clock.tick(self.fps)

    # Todo - Add crazy functions to allow other objects and instances finding
    # like GM
    # Todo - Easy way to take screenshot and save it as pic
    # Todo: Game testing module. Lets you compare screenshots and compare values with  pixelarray or surface.get_at
    # Also allows accessing different config values.


    # class fun_Game ends here
# print(fun_Game)

# global register_event cached,as it will also be used as classmethod
# should use register_event=_register_event at end of all class defn

meta_fun_Class = meta_accessor_class


@register_class(fun_Game)
class fun_Class(object):
    # think about this: priority_order and depth
    # by default, depends on "when class was defined"
    #    cls.priority_order = cls.depth = len(fun_Game.list_class)
    __metaclass__ = meta_fun_Class

    # Below lines moved to meta_fun_Class
    # list_instance = uniquelist()
    # list_check_func = uniquelist()
    # dict_action_func -> dict of action funcs, key=event_numb like KEYDOWN
    # dict_action_func = {}

    sprite_defaults = {
        "type": Rect,
        "params": {
            "size": (40, 40),
            "color": None
        }
    }

    def __init__(self, x=None, y=None):
        # use sprite as a general term, img->one kind of sprite, rect, circle
        self.x_start = x
        self.y_start = y
        self.x = x
        self.y = y
        self.x_prev = x
        self.y_prev = y
        self.vel_x, self.vel_y, self.accln_x, self.accln_y = 0, 0, 0, 0

        if (self.sprite_defaults and self.sprite_defaults.get("type")):
            if (x is None) or (y is None):
                raise AttributeError(
                    "fun_Class with sprite_defaults must have x,y")

            self.sprite = self.sprite_defaults.get("type").from_container_obj(
                container_obj=self, **self.sprite_defaults["params"])
            self.list_dirty_sprite = []
            # list_rendered_sprite => sprites that are effectively on the
            # screen now
            self.list_rendered_sprite = []
        else:
            self.sprite = None
        self.list_instance.append(self)
        # think about self.action_create()

    @property
    def vel(self):
        return math.sqrt(self.vel_x ** 2 + self.vel_y ** 2)

    @vel.setter
    def vel(self, val):
        self.vel_x = val * math.cos(math.radians(self.vel_direction))
        self.vel_y = val * math.sin(math.radians(self.vel_direction))

    @property
    def vel_direction(self):
        return atan2_inv(self.vel_y, self.vel_x)

    @vel_direction.setter
    def vel_direction(self, val):
        self.vel_x = self.vel * math.cos(math.radians(val))
        self.vel_y = self.vel * math.sin(math.radians(val))

    @property
    def accln(self):
        return math.sqrt(self.accln_x ** 2 + self.accln_y ** 2)

    @accln.setter
    def accln(self, val):
        self.accln_x = val * math.cos(math.radians(self.accln_direction))
        self.accln_y = val * math.sin(math.radians(self.accln_direction))

    @property
    def accln_direction(self):
        return atan2_inv(self.accln_y, self.accln_x)

    @accln_direction.setter
    def accln_direction(self, val):
        self.accln_x = self.accln * math.cos(math.radians(val))
        self.accln_y = self.accln * math.sin(math.radians(val))

    @classmethod
    def update_instances(cls, list_event):
        '''calls update_self for all instances.'''
        for tmp_instance in cls.list_instance:
            tmp_instance.update_self(list_event)

    def update_self(self, list_event):
        # print list_event
        for each_ev in list_event:
# print self.dict_action_func
            if each_ev.type in self.dict_action_func:
                for each_action in self.dict_action_func[each_ev.type]:
                    # similar as self.action_step()
                    each_action(self, each_ev)

    @classmethod
    def _check_event(cls, ev_name_or_type, new_or_old):
        ''' ev_name_or_type => name_or_type(numb)_of_event
            new_or_old => current_event_list or old_event_list '''
        matched_events = []
        if new_or_old == "new":
            list_to_check = cls.game_class.list_event
        elif new_or_old == "old":
            list_to_check = cls.game_class.list_event_old
        else:
            raise AttributeError("new_or_old must be 'new' or 'old'.")
        if type(ev_name_or_type) is int:
            ev_type = ev_name_or_type
        elif type(ev_name_or_type) is str:
            ev_name = fuzzy_match_event_name(ev_name_or_type, "event")
            ev_type = KW_EVENTS_ALL[ev_name]
        for ev in list_to_check:
            if ev.type == ev_type:
                matched_events.append(ev)
        return matched_events

    @classmethod
    def check_event(cls, ev_name_or_type):
        return cls._check_event(ev_name_or_type, "new")

    @classmethod
    def check_event_old(cls, ev_name_or_type):
        return cls._check_event(ev_name_or_type, "old")

    @classmethod
    def register_event(cls, event_name=None, func_to_register=None):
        global register_event
        register_event(event_name, func_to_register, cls)

    @classmethod
    def for_all_instance(cls, func_to_run, flatten):
        return_list = []
        for tmp_instance in cls.list_instance:
            return_item = func_to_run(tmp_instance)
            if flatten == "level-instance":
                return_list.extend(return_item)
            else:
                return_list.append(return_item)
        return return_list

    def collide(self, *args, **kwargs):
        return self.sprite.collide(*args, **kwargs)

# always use selfie,not selfie_depreceated most compatible
# make this classmethod,selfie-ridden register_events as test
# @register_event()
    def action_end_step_default(self, ev):
        if not(self.x is None) and not(self.y is None):
            # Set x_prev, y_prev
            self.x_prev = self.x
            self.y_prev = self.y
            # Accelerate velocity
            self.vel_x += self.accln_x
            self.vel_y += self.accln_y
            # Move x and y
            self.x += self.vel_x
            self.y += self.vel_y

    def action_begin_step(self, ev):
# print "Calling begin_step"
        pass

    def action_JOY_BUTTON_UP(self, ev):
        print "calling JOY_BUTTON_UP"

    def action_key_down(self, ev):
        print "Calling key_down"

    def action_end_step(self, ev):
# print "Calling end step"
        pass

    def action_draw_default(self, ev):
        # print "Drawing"
        self.sprite.draw()
    # end of fun_Class
# Other classes


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
        Potential candidates for list_to_get ->
        fun_Game.list_event, fun_Game.list_event_old, fun_Game.list_state_all_buttons, fun_Game.list_state_all_buttons_old'''
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

# Todo: see below
# Collision helper event_collision funcs (Done, for circle)
# Allow collision with "all"
# More collision func like GM
# More extended draw funcs
# Make img sprite
# Use rects retuned from blit to display.update
#
# 1. (Think) Allow rect-like and circle-like constructs wherever rect and circle are expected.
# 2. Do all sort of type-checking.
# 3. Use sprites and groups in pygame as containers
# Imp: Allow debugging with event handlers and others with @debug

# Design tips I will use later
# use weakrefs as much as possible
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
