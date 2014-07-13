# only for python 2.x
# VERY IMP: Use weakrefs instead of list for fun_Game.list_class,\
# fun_Class.list_instance and fun_Class.list_update_func

from uniquelist import uniquelist  # imports uniquelist
import pygame
from pygame.locals import *  # imports the constants
import math
from utils import register_class, meta_accessor_class, register_action
# import utils
import logging
from copy import deepcopy
from math_utils import atan2_inv, distance, vel_add, direction
import event
import sys

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

    dispatch_events_class = classmethod(event.dispatch_events_class)

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
                    # make blit funcs capable of taking a clip rect, will be
                    # appplied before blitting
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
        # i = 0
        for tmp_clear_rect in list_clear_rect:
            # convert to pygame rect
            if not (tmp_clear_rect in list_cancelled_clear_rect):
                self.screen.fill(pygame.Color(0, 0, 0, 1), tmp_clear_rect)
                # i += 1
        # print "i=", i

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
            event.collect_events()
            self.dispatch_events_class()
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

    def __init__(self, x=None, y=None):
        # use sprite as a general term, img->one kind of sprite, rect, circle
        self.x_start = x
        self.y_start = y
        self.center = [x, y]
        self.x_prev = x
        self.y_prev = y
        self.vel_x, self.vel_y, self.accln_x, self.accln_y = 0, 0, 0, 0

        if (hasattr(self, "sprite_defaults") and self.sprite_defaults.get("type")):
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
        self.push_event_local(event.Event("Instance_create"))

    @property
    def center(self):
        return self._center

    @center.setter
    def center(self, val):
        if not hasattr(self, "_center"):
            self._center = [None, None]
        self._center[0] = val[0]
        self._center[1] = val[1]

    @property
    def x(self):
        return self.center[0]

    @x.setter
    def x(self, val):
        self.center[0] = val

    @property
    def y(self):
        return self.center[1]

    @y.setter
    def y(self, val):
        self.center[1] = val

    @property
    def vel(self):
        return math.hypot(self.vel_x, self.vel_y)

    @vel.setter
    def vel(self, val):
        self.vel_x = val * math.cos(math.radians(self.vel_direction))
        self.vel_y = -val * math.sin(math.radians(self.vel_direction))

    @property
    def vel_direction(self):
        return atan2_inv(self.vel_y, self.vel_x)

    @vel_direction.setter
    def vel_direction(self, val):
        self.vel_x = self.vel * math.cos(math.radians(val))
        self.vel_y = -self.vel * math.sin(math.radians(val))

    @property
    def accln(self):
        return math.sqrt(self.accln_x ** 2 + self.accln_y ** 2)

    @accln.setter
    def accln(self, val):
        self.accln_x = val * math.cos(math.radians(self.accln_direction))
        self.accln_y = -val * math.sin(math.radians(self.accln_direction))

    @property
    def accln_direction(self):
        return atan2_inv(self.accln_y, self.accln_x)

    @accln_direction.setter
    def accln_direction(self, val):
        self.accln_x = self.accln * math.cos(math.radians(val))
        self.accln_y = -self.accln * math.sin(math.radians(val))

    def distance(self, x, y):
        point_ = (x, y)
        return distance(self.center, point_)

    def vel_add(self, vel_mag, vel_direction):
        ''' vel_mag -> Magnitude of vel.
            vel_direction -> direction in degrees.
            Adds to current velocity and also returns new (vel_mag,vel_dir).'''

        new_vel_mag, new_vel_dir = vel_add(
            (self.vel, self.vel_direction), (vel_mag, vel_direction))
        self.vel_set(new_vel_mag, new_vel_dir)
        return self

    def vel_set(self, vel_mag, vel_dir):
        self.vel_x = vel_mag * math.cos(math.radians(vel_dir))
        self.vel_y = -vel_mag * math.sin(math.radians(vel_dir))
        return self

    def direction(self, x, y):
        point_ = (x, y)
        return direction(self.center, point_)

    @property
    def list_event_local(self):
        if not hasattr(self, "_list_event_local"):
            self._list_event_local = []
        return self._list_event_local

    @list_event_local.setter
    def list_event_local(self, value):
        self._list_event_local = value

    dispatch_events_instance = classmethod(event.dispatch_events_instance)
    dispatch_events_self = event.dispatch_events_self
    push_event_local = event.push_event_local
    _push_event_local_single = event._push_event_local_single
    dispatch_events_local = event.dispatch_events_local
    clear_event_local = event.clear_event_local

    @classmethod
    def register_action(cls, event_name=None, func_to_register=None):
        global register_action
        register_action(event_name, func_to_register, cls)

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
# make this classmethod,selfie-ridden register_actions as test
# @register_action()
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
        pass

    def action_draw_default(self, ev):
        # print "Drawing"
        self.sprite.draw()

    def action_quit(self, ev):
        # should be made better / overloaded
        # IMP: will crash unless weakrefs are used
        # pygame.quit()
        sys.exit()
    # end of fun_Class
# Other classes



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
