import pygame
import sprite_types
import inspect
import base
from utils import remove_from_list


class Img(object):

    map_class = "Img"

    def __init__(self, center=(None, None), file_name_or_obj=None, namehint="", collision_shape=None, container_obj=None):

        if not (len(center) == 2):
            raise TypeError("Center must be (x,y)")
        x = center[0]
        y = center[1]
        if not container_obj:
            if (x is None) or (y is None):
                raise TypeError("Center=(x,y) must be provided")
            else:
                self.container_obj = None
                self.center = (x, y)
        else:
            self.container_obj = container_obj  # Use weakrefs

        if (file_name_or_obj is None):
            raise TypeError(
                "file_name_or_obj must be filename, file_obj or surface")

        if not isinstance(file_name_or_obj, pygame.Surface):
            if namehint == "":
                self.surf = pygame.image.load(file_name_or_obj)
            else:
                self.surf = pygame.image.load(file_name_or_obj, namehint)
        else:
            # From surface
            # Todo: Some param for caching
            self._surf = file_name_or_obj

        if collision_shape:
            self._col_shape = collision_shape
        else:
            self._col_shape = self.bbox

    @property
    def col_shape(self):
        return self._col_shape

    @col_shape.setter
    def col_shape(self, value):
        self._col_shape = value

    def sync_col_shape(self):
        self.col_shape.center = self.center

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
        self.sync_col_shape()

    @classmethod
    def from_container_obj(cls, container_obj, file_name_or_obj, namehint=""):
        return cls(file_name_or_obj=file_name_or_obj, namehint=namehint, container_obj=container_obj)

    @classmethod
    def from_surface(cls, center, surf):
        return cls(center=center, file_name_or_obj=surf)

    @property
    def surf(self):
        return self._surf

    @surf.setter
    def surf(self, value):
        if isinstance(value, pygame.Surface):
            self._surf = value
        else:
            return TypeError("surf can only be set to anther pygame.Surface")

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
        '''Returns sprite_types.Rect copy of bounding box'''
        surf_rect = self.get_rect()
        return sprite_types.Rect.from_rect(surf_rect)

    def get_rect(self):
        '''Returns pygame.Rect copy of bounding box'''
        return self.surf.get_rect(center=self.center)

    def get_surface(self):
        ''' Returns a copy of internal surface '''
        return self.surf.copy()

    def __repr__(self):
        return "{0.__class__}( center={0.center}, size={0.size})".format(self)

    def __copy__(self):
        return self.__cls__.from_surface(self.center, self.surf.copy())

    def save_to_disk(self, filename):
        pygame.image.save(self.get_surface(), filename)
        return True

    @property
    def size(self):
        return self.surf.get_size()

    @size.setter
    def size(self, value):
        raise NotImplementedError(
            "Setting size is ambiguous, so not implemented")

    @property
    def width(self):
        return self.get_width()

    @width.setter
    def width(self, value):
        raise NotImplementedError(
            "Setting width is ambiguous, so not implemented")

    @property
    def height(self):
        return self.get_height()

    @height.setter
    def height(self, value):
        raise NotImplementedError(
            "Setting height is ambiguous, so not implemented")

    @property
    def w(self):
        return self.width

    @w.setter
    def w(self, value):
        self.width = value

    @property
    def h(self):
        return self.height

    @h.setter
    def h(self, value):
        self.height = value

    # Surface methods not provided, apply on self.surf
    def blit(self, surface, (x, y)=(None, None), clip_rect=None):

        if (x, y) == (None, None):
            (x, y) = self.center
        # pygame.Rect does this, which is used in clear_rect
        x, y = int(x), int(y)

        if clip_rect:
            # Set clip region
            surface.set_clip(clip_rect)

        surface.blit(self.surf, self.bbox.topleft)

        if clip_rect:
            # Remove clip region
            surface.set_clip(None)

    def draw(self):
        tmp_dirty_sprite = {
            "sprite": self,
            # later shape may be used for matching insted of sprites, as sprite
            # may be subclassed, changing "sprite" obj
            "shape": "Img",
            "bbox": self.get_rect(),
            "config": {
                "center": self.center,
                "file_name_or_obj": self.surf
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

        if not hasattr(other_obj, "__class__"):
            raise AttributeError(
                "other_obj must be a class or instance")

        # Handle instances
        if isinstance(other_obj, sprite_types.Circle):
            return self.collide_circle(other_obj, moved_center, from_container_obj)
        elif isinstance(other_obj, sprite_types.Rect):
            return self.collide_rect(other_obj, moved_center, from_container_obj)
        elif isinstance(other_obj, Img):
            # Todo: add img collision
            return self.collide_img(other_obj, moved_center, from_container_obj)
        else:
            pass

        # Handle classes
        if inspect.isclass(other_obj):
            if issubclass(other_obj,  sprite_types.Circle):
                return self.collide_list_circle(other_obj.list_instance, moved_center, from_container_obj)
            elif issubclass(other_obj, sprite_types.Rect):
                return self.collide_list_rect(other_obj.list_instance, moved_center, from_container_obj)
            elif issubclass(other_obj, Img):
                # Todo: add img collision
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
            remove_from_list(to_return, None, recursive=True)
            remove_from_list(to_return, False, recursive=True)
            return to_return
        if isinstance(other_obj, base.fun_Class):
            other_obj_sprite = other_obj.sprite
            to_return = self.collide(
                other_obj_sprite, moved_center, from_container_obj=True)
            # doesnt return list, so prev. case operations not done
            return to_return

    def collide_img(self, another_img, moved_center=(None, None), from_container_obj=False):
        ''' Checks if this img intersects with another_img. '''

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

    def collide_circle(self, another_circle, moved_center=(None, None), from_container_obj=False):
        ''' Checks if this circle intersects with another_circle. '''
        if not (len(moved_center) == 2):
            raise AttributeError("moved_center must be of the form (x,y)")
        _center = self.center
        moved_center = list(moved_center)
        if moved_center[0] is None:
            moved_center[0] = _center[0]
        if moved_center[1] is None:
            moved_center[1] = _center[1]
        # temporarily move self to moved_center and shift back later
        self.center = moved_center
        does_collide = another_circle.collide_img(self)
        self.center = _center
        if does_collide:
            if from_container_obj:
                to_return = another_circle.container_obj
            else:
                to_return = another_circle
        else:
            to_return = False
        return to_return

    def collide_point(self, (point_x, point_y)):
        ''' Checks if (point_x, point_y) is inside this circle. '''
        does_collide = self.col_shape.collide_point((point_x, point_y))
        if does_collide:
            return True
        else:
            return False

    def collide_list_circle(self, list_circle, moved_center=(None, None), from_container_obj=False):
        ''' Returns list of circles in list_circle which intersects with this circle. '''
        list_collided_circle = []
        for circle in list_circle:
            if self.collide_circle(circle, moved_center, from_container_obj):
                # Collide_circle itself takes container_obj into account, so no
                # need of post-processing
                list_collided_circle.append(circle)
        else:  # else of the for loop
            return False
        return list_collided_circle

    def collide_list_any_circle(self, list_circle, moved_center=(None, None), from_container_obj=False):
        ''' Checks if this circle intersects with any of the circles in circle_list. '''
        for circle in list_circle:
            if self.collide_circle(circle, moved_center, from_container_obj):
                return True
        else:  # else of the for loop
            return False

    def collide_list_all_circle(self, list_circle, moved_center=(None, None), from_container_obj=False):
        ''' Checks if this circle intersects with all of the circles in circle_list. '''
        for circle in list_circle:
            if not self.collide_circle(circle, moved_center, from_container_obj):
                return False
        else:  # else of the for loop
            return True

    def collide_rect(self, another_rect, moved_center=(None, None), from_container_obj=False):
        ''' Checks if this circle collides with another_rect. '''
        if not (len(moved_center) == 2):
            print "moved_center must be of the form (x,y)"
        _center = self.center
        moved_center = list(moved_center)
        if moved_center[0] is None:
            moved_center[0] = _center[0]
        if moved_center[1] is None:
            moved_center[1] = _center[1]

        self.center = moved_center
        does_collide = another_rect.collide_img(self)
        self.center = _center
        if does_collide:
            if from_container_obj:
                to_return = another_rect.container_obj
            else:
                to_return = another_rect
        else:
            to_return = False
        return to_return

    def collide_list_rect(self, list_rect, moved_center=(None, None), from_container_obj=False):
        ''' Returns list of rect in list_rect which intersects with this circle. '''
        list_collided_rect = []
        for rect in list_rect:
            if self.collide_rect(rect, moved_center, from_container_obj):
                list_collided_rect.append(rect)
        else:  # else of the for loop
            return False
        return list_collided_rect

    def collide_list_any_rect(self, list_rect, moved_center=(None, None), from_container_obj=False):
        ''' Returns True if collides with any of the rect in the list. '''
        for temp_rect in list_rect:
            if self.collide_rect(self, temp_rect, moved_center, from_container_obj):
                return True
        else:
            return False

    def collide_list_all_rect(self, list_rect, moved_center=(None, None), from_container_obj=False):
        ''' Returns True if collides with all the rect in the list. '''
        for temp_rect in list_rect:
            if not self.collide_rect(self, temp_rect, moved_center, from_container_obj):
                return False
            else:
                return True
