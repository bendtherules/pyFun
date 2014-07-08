import pygame
from utils import remove_from_list
import base
import sprite_types
import inspect


class Rect(object):

    """Pythonic rect wrapper, using in-built Rect for speed"""

    map_class = "Rect"

    def __init__(self, center=(None, None), size=(None, None), color=None, container_obj=None):
        if not (len(center) == 2):
            raise AttributeError("Center must be (x,y)")
        x = center[0]
        y = center[1]
        if (not (len(size) == 2)) or (None in size):
            raise AttributeError(
                "size must be provided and is of format (w,h)")
        self.color = color
        if not container_obj:
            if (x is None) or (y is None):
                raise AttributeError("Center=(x,y) must be provided")
            else:
                self.container_obj = None
                self.center = (x, y)
        else:
            self.container_obj = container_obj  # Use weakrefs

        tmp_left = self.center[0] - size[0] / 2
        tmp_top = self.center[1] - size[1] / 2
        self._rect = pygame.Rect((tmp_left, tmp_top), size)
        self.sync_self()

    @classmethod
    def from_rect(cls, rect):
        # Doesnt use the same rect, effectively makes a copy
        # As rects cant have extra props, it shouldnt impose any limitations.
        return cls(rect.center, rect.size)

    @classmethod
    def from_top_left(cls, top_left=(None, None), size=(None, None), color=None, container_obj=None):
        if not (None in top_left):
            tmp_center = top_left[0] + size[0] / 2, top_left[1] + size[1] / 2
        else:
            tmp_center = top_left
        return cls(tmp_center, size, color, container_obj)

    @property
    def center(self):
        if self.container_obj:
            return (self.container_obj.x, self.container_obj.y)
        else:
            return self._center

    @center.setter
    def center(self, val):
        if self.container_obj:
            self.container_obj.x, self.container_obj.y = val
        else:
            self._center = val

    @classmethod
    def from_container_obj(cls, container_obj, size, color=None):
        return cls(size=size, color=color, container_obj=container_obj)

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
    def x(self):
        return self.center_x

    @x.setter
    def x(self, val):
        self.center_x = val

    @property
    def y(self):
        return self.center_y

    @y.setter
    def y(self, val):
        self.center_y = val

    @property
    def bbox(self):
        return self.inner_rect.copy()

    @property
    def inner_rect(self):
        self.sync_inner_rect()
        return self._rect

    def sync_inner_rect(self):
        self._rect.center = self.center

    def sync_self(self):
        self.center = self._rect.center

    # misc. methods

    def __repr__(self):
        return "{0.__class__}( center={0.center}, size={0.size}, color={0.color})".format(self)

    def __copy__(self):
        return self.__class__(**self.get_props())

    def get_props(self):
        ''' Returns all of the constructor params, reqd for creationg a copy '''
        return {
            "center": self.center,
            "size": self.size,
            "color": self.color,
            "container_obj": self.container_obj,
        }

    def __eq__(self, another_rect):
        if self.get_props() == another_rect.get_props():
            return True
        else:
            return False

    # draw and blit func

    def blit(self, surface, (x, y)=(None, None), color=None, clip_rect=None, width=1, use_antialiasing=False):

        if (x, y) == (None, None):
            (x, y) = self.center
        # pygame.Rect does this, which is used in clear_rect
        x, y = int(x), int(y)
        if not color:
            if self.color:
                color = self.color
            else:
                color = pygame.Color("blue")

        if clip_rect:
            # Set clip region
            surface.set_clip(clip_rect)

        if not use_antialiasing:
            pygame.draw.rect(
                surface, color, self.bbox, width)
        else:
            # do later
            pass

        if clip_rect:
            # Remove clip region
            surface.set_clip(None)

    def draw(self):
        tmp_dirty_sprite = {
            "sprite": self,
            # later shape may be used for matching insted of sprites, as sprite
            # may be subclassed, changing "sprite" obj
            "shape": "Rect",
            # Very IMP: If using Rect for bbox, use rect_to_pygame_rect like
            # below.
            "bbox": self.bbox,
            "config": {
                "center": self.center,
                "size": self.size,
                "color": self.color
            }
        }
        for tmp_old_sprite in self.container_obj.list_rendered_sprite:
            # if any of them is eqv. to new dirty sprite, mark old one as
            # still_valid
            if tmp_old_sprite == tmp_dirty_sprite:
                # puts "still_valid" entry in the old_dirty_sprite_dict
                # quite good approach, wont match with anything again
                # but "still_valid" should be removed, before next step (tick), to allow
                # checks later
                tmp_old_sprite["still_valid"] = True
                break
        else:
            # i.e. if no match found, list it as dirty sprite
            self.container_obj.list_dirty_sprite.append(tmp_dirty_sprite)

    # collide func
    def collide(self, other_obj, moved_center=(None, None), from_container_obj=False):
        ''' Collision handler for any type of obj'''
        # todo: handle game_class=="all"
        # todo: point class
        if not hasattr(other_obj, "__class__"):
            raise AttributeError(
                "other_obj must be a class or instance")

        # Handle instances
        if isinstance(other_obj, sprite_types.Circle):
            return self.collide_circle(other_obj, moved_center, from_container_obj)
        elif isinstance(other_obj, Rect):
            return self.collide_rect(other_obj, moved_center, from_container_obj)
        elif isinstance(other_obj, sprite_types.Img):
            return self.collide_img(other_obj, moved_center, from_container_obj)
        else:
            pass

        # Handle classes
        if inspect.isclass(other_obj):
            if issubclass(other_obj, sprite_types.Circle):
                return self.collide_list_circle(other_obj.list_instance, moved_center, from_container_obj)
            elif issubclass(other_obj, Rect):
                return self.collide_list_rect(other_obj.list_instance, moved_center, from_container_obj)
            elif issubclass(other_obj, sprite_types.Img):
                return self.collide_list_img(other_obj.list_instance, moved_center, from_container_obj)
            else:
                pass

        # Handle fun_Game and fun_Class or their instances
        if isinstance(other_obj, base.fun_Game) or (inspect.isclass(other_obj) and issubclass(other_obj, base.fun_Game)):
            def instance_collide(other_obj):
                return self.collide(other_obj.sprite, moved_center, from_container_obj=True)
            to_return = other_obj.for_all_instance(
                instance_collide, flatten="level-class")
            remove_from_list(to_return, self.container_obj)
            remove_from_list(to_return, None, recursive=True)
            remove_from_list(to_return, False, recursive=True)
            return to_return
        if inspect.isclass(other_obj) and issubclass(other_obj, base.fun_Class):
            def instance_collide(other_obj):
                return self.collide(other_obj.sprite, moved_center, from_container_obj=True)
            to_return = other_obj.for_all_instance(
                instance_collide, flatten=False)
            remove_from_list(to_return, self.container_obj)
            remove_from_list(to_return, False, recursive=True)
            remove_from_list(to_return, None, recursive=True)
            remove_from_list(to_return, False, recursive=True)
            return to_return
        if isinstance(other_obj, base.fun_Class):
            other_obj_sprite = other_obj.sprite
            to_return = self.collide(
                other_obj_sprite, moved_center, from_container_obj=True)
            # doesnt return list, so prev. case operations not done
            return to_return

    # Rest are all synced props and methods
    # w, h, width, height
    # top, left, bottom, right
    # topleft, bottomleft, topright, bottomright
    # midtop, midleft, midbottom, midright
    # size
    # Getters first

    @property
    def width(self):
        return self.bbox.width

    @property
    def height(self):
        return self.bbox.height

    @property
    def w(self):
        return self.bbox.w

    @property
    def h(self):
        return self.bbox.h

    @property
    def top(self):
        return self.bbox.top

    @property
    def left(self):
        return self.bbox.left

    @property
    def bottom(self):
        return self.bbox.bottom

    @property
    def right(self):
        return self.bbox.right

    @property
    def topleft(self):
        return self.bbox.topleft

    @property
    def bottomleft(self):
        return self.bbox.bottomleft

    @property
    def topright(self):
        return self.bbox.topright

    @property
    def bottomright(self):
        return self.bbox.bottomright

    @property
    def midtop(self):
        return self.bbox.midtop

    @property
    def midleft(self):
        return self.bbox.midleft

    @property
    def midbottom(self):
        return self.bbox.midbottom

    @property
    def midright(self):
        return self.bbox.midright

    @property
    def size(self):
        return self.bbox.size

    # Then setters
    @width.setter
    def width(self, val):
        self.inner_rect.width = val
        self.sync_self()

    @height.setter
    def height(self, val):
        self.inner_rect.height = val
        self.sync_self()

    @w.setter
    def w(self, val):
        self.inner_rect.w = val
        self.sync_self()

    @h.setter
    def h(self, val):
        self.inner_rect.h = val
        self.sync_self()

    @top.setter
    def top(self, val):
        self.inner_rect.top = val
        self.sync_self()

    @left.setter
    def left(self, val):
        self.inner_rect.left = val
        self.sync_self()

    @bottom.setter
    def bottom(self, val):
        self.inner_rect.bottom = val
        self.sync_self()

    @right.setter
    def right(self, val):
        self.inner_rect.right = val
        self.sync_self()

    @topleft.setter
    def topleft(self, val):
        self.inner_rect.topleft = val
        self.sync_self()

    @bottomleft.setter
    def bottomleft(self, val):
        self.inner_rect.bottomleft = val
        self.sync_self()

    @topright.setter
    def topright(self, val):
        self.inner_rect.topright = val
        self.sync_self()

    @bottomright.setter
    def bottomright(self, val):
        self.inner_rect.bottomright = val
        self.sync_self()

    @midtop.setter
    def midtop(self, val):
        self.inner_rect.midtop = val
        self.sync_self()

    @midleft.setter
    def midleft(self, val):
        self.inner_rect.midleft = val
        self.sync_self()

    @midbottom.setter
    def midbottom(self, val):
        self.inner_rect.midbottom = val
        self.sync_self()

    @midright.setter
    def midright(self, val):
        self.inner_rect.midright = val
        self.sync_self()

    @size.setter
    def size(self, val):
        self.inner_rect.size = val
        self.sync_self()

    # in-place methods

    def move_ip(self, *args, **kwargs):
        self.inner_rect.move_ip(*args, **kwargs)
        self.sync_self()
        return self

    def inflate_ip(self, *args, **kwargs):
        self.inner_rect.inflate_ip(*args, **kwargs)
        self.sync_self()
        return self

    def clamp_ip(self, *args, **kwargs):
        self.inner_rect.clamp_ip(*args, **kwargs)
        self.sync_self()
        return self

    def normalize_ip(self):
        self.inner_rect.normalize()
        self.sync_self()
        return self

    def union_ip(self, *args, **kwargs):
        self.inner_rect.union_ip(*args, **kwargs)
        self.sync_self()
        return self

    def unionall_ip(self, *args, **kwargs):
        self.inner_rect.unionall_ip(*args, **kwargs)
        self.sync_self()
        return self

    # non in-place methods

    def copy(self, *args, **kwargs):
        return self.bbox.copy(*args, **kwargs)

    def move(self, *args, **kwargs):
        return self.bbox.move(*args, **kwargs)

    def inflate(self, *args, **kwargs):
        return self.bbox.inflate(*args, **kwargs)

    def clamp(self, another_rect):
        if hasattr(another_rect, "bbox"):
            tmp_rect = another_rect.bbox
        else:
            tmp_rect = another_rect

        return self.bbox.clamp(tmp_rect)

    def clip(self, another_rect):
        if hasattr(another_rect, "bbox"):
            tmp_rect = another_rect.bbox
        else:
            tmp_rect = another_rect
        return self.bbox.clip(tmp_rect)

    def union(self, another_rect):
        if hasattr(another_rect, "bbox"):
            tmp_rect = another_rect.bbox
        else:
            tmp_rect = another_rect
        return self.bbox.union(tmp_rect)

    def unionall(self, rect_sequence):
        new_rect_seq = []
        for another_rect in rect_sequence:
            if hasattr(another_rect, "bbox"):
                tmp_rect = another_rect.bbox
            else:
                tmp_rect = another_rect
            new_rect_seq.append(tmp_rect)
        return self.bbox.unionall(new_rect_seq)

    def fit(self, another_rect):
        if hasattr(another_rect, "bbox"):
            tmp_rect = another_rect.bbox
        else:
            tmp_rect = another_rect
        return self.bbox.fit(tmp_rect)

    def contains(self, another_rect):
        if hasattr(another_rect, "bbox"):
            tmp_rect = another_rect.bbox
        else:
            tmp_rect = another_rect
        return self.bbox.contains(tmp_rect)

    def collide_point(self, *args, **kwargs):
        ''' collide_point(x,y) -> return bool
            collide_point((x,y)) -> return bool '''
        return self.bbox.collidepoint(*args, **kwargs)

    def collide_rect(self, another_rect, moved_center=(None, None), from_container_obj=False):

        if not (len(moved_center) == 2):
            print "moved_center must be of the form (x,y)"
        _center = self.center
        moved_center = list(moved_center)
        if moved_center[0] is None:
            moved_center[0] = _center[0]
        if moved_center[1] is None:
            moved_center[1] = _center[1]

        self.center = moved_center

        # Real collision code starts
        if hasattr(another_rect, "bbox"):
            tmp_rect = another_rect.bbox
        else:
            tmp_rect = another_rect
        does_collide = self.bbox.colliderect(tmp_rect)
        # Ends

        self.center = _center
        if does_collide:
            if from_container_obj:
                to_return = another_rect.container_obj
            else:
                to_return = another_rect
        else:
            to_return = False
        return to_return

    def collide_list_rect(self, rect_sequence, moved_center=(None, None), from_container_obj=False):
        ''' Returns a list of rects, which collide; else empty list '''
        return_list = []
        for each_rect in rect_sequence:
            if self.collide_rect(each_rect, moved_center, from_container_obj):
                return_list.append(each_rect)
        return return_list

    def collide_list_all_rect(self, rect_sequence, moved_center=(None, None), from_container_obj=False):
        ''' Returns True if all rects in rect_sequence which collide,
            else False '''
        for each_rect in rect_sequence:
            if not self.collide_rect(each_rect, moved_center, from_container_obj):
                return False
        else:
            return True

    def collide_list_any_rect(self, rect_sequence, moved_center=(None, None), from_container_obj=False):
        '''Returns the first rect which collides, else False'''
        for each_rect in rect_sequence:
            if self.collide_rect(each_rect, moved_center, from_container_obj):
                return each_rect
        else:
            return False

    def collide_circle(self, another_circle, moved_center=(None, None), from_container_obj=False):

        if not (len(moved_center) == 2):
            print "moved_center must be of the form (x,y)"
        _center = self.center
        moved_center = list(moved_center)
        if moved_center[0] is None:
            moved_center[0] = _center[0]
        if moved_center[1] is None:
            moved_center[1] = _center[1]

        self.center = moved_center

        # Collision code (uses Circles collision method) starts
        does_collide = another_circle.collide_rect(self)
        # Ends

        self.center = _center
        if does_collide:
            if from_container_obj:
                to_return = another_circle.container_obj
            else:
                to_return = another_circle
        else:
            to_return = False
        return to_return

    def collide_list_circle(self, circle_sequence, moved_center=(None, None), from_container_obj=False):
        ''' Returns a list of Circles, which collide; else empty list '''
        return_list = []
        for each_circle in circle_sequence:
            if self.collide_circle(each_circle, moved_center, from_container_obj):
                return_list.append(each_circle)
        return return_list

    def collide_list_all_circle(self, circle_sequence, moved_center=(None, None), from_container_obj=False):
        ''' Returns True if all circles in circle_sequence which collide,
            else False '''
        for each_circle in circle_sequence:
            if not self.collide_circle(each_circle, moved_center, from_container_obj):
                return False
        else:
            return True

    def collide_list_any_circle(self, circle_sequence, moved_center=(None, None), from_container_obj=False):
        '''Returns the first circle which collides, else False'''
        for each_circle in circle_sequence:
            if self.collide_circle(each_circle, moved_center, from_container_obj):
                return each_circle
        else:
            return False

    def collide_img(self, another_img, moved_center=(None, None), from_container_obj=False):
        ''' Checks if this rect intersects with another_img. '''

        does_collide = self.collide(
            another_img.col_shape, moved_center, from_container_obj=False)
        if does_collide:
            if from_container_obj:
                to_return = another_img.container_obj
            else:
                to_return = another_img
        else:
            to_return = False
        return to_return

    def collide_list_img(self, list_img, moved_center=(None, None), from_container_obj=False):
        list_collided_img = []
        for each_img in list_img:
            if self.collide_img(each_img, moved_center, from_container_obj):
                # Collide_img itself takes container_obj into account, so no
                # need of post-processing
                list_collided_img.append(each_img)
        else:  # else of the for loop
            return False
        return list_collided_img
