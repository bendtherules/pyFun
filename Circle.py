import pygame
from math_utils import distance
import math
import base
import inspect
import sprite_types
from utils import remove_from_list, rect_to_pygame_rect


class Circle(object):
    map_class = "Circle"

    def __init__(self, center=(None, None), radius=None, color=None, container_obj=None):
        if not (len(center) == 2):
            raise AttributeError("Center must be (x,y)")
        x = center[0]
        y = center[1]
        if (radius is None):
            raise AttributeError("radius must be provided")
        self.radius = radius
        self.color = color
        if not container_obj:
            if (x is None) or (y is None):
                raise AttributeError("Center=(x,y) must be provided")
            else:
                self.container_obj = None
                self.center = (x, y)
        else:
            self.container_obj = container_obj  # Use weakrefs

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
    def from_container_obj(cls, container_obj, radius, color=None):
        return cls(radius=radius, color=color, container_obj=container_obj)

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
        # left = self.center_x - self.radius
        # top = self.center_y - self.radius
        width = height = self.radius * 2
        return sprite_types.Rect(self.center, (width, height))
    # todo: remember about the colour. document - center is list unlike tuple
    # in case of rect.

    def __repr__(self):
        return "{0.__class__}( center={0.center}, radius={0.radius}, color={0.color})".format(self)

    def __copy__(self):
        return self.__class__(self.center, self.radius, self.color)

    def move(self, move_x, move_y):
        return Circle((self.center_x + move_x, self.center_y + move_y), self.radius, self.color)

    def move_ip(self, move_x, move_y):
        self.center_x += move_x
        self.center_y += move_y
        return self

    def inflate(self, inflate_radius):
        # check if resultant radius is -ve
        return Circle(self.center, self.radius + inflate_radius, self.color)

    def inflate_ip(self, inflate_radius):
        self.radius += inflate_radius
        return self

    def is_inside(self, another_circle):
        ''' Checks if this circle is fully inside another_circle '''
        if self.radius >= another_circle.radius:
            return None
        else:
            bigger_circle = another_circle
            smaller_circle = self
            return distance(bigger_circle.center, smaller_circle.center) + smaller_circle.radius < bigger_circle.radius

    def is_inside_mutual(self, another_circle):
        ''' Checks if this circle is fully inside another_circle or the opposite.'''
        radius_diff = self.radius - another_circle.radius
        if radius_diff > 0:
            bigger_circle = self
            smaller_circle = another_circle
        elif radius_diff == 0:
            # None of them can be inside the other
            return None
        else:
            smaller_circle = self
            bigger_circle = another_circle
        return distance(bigger_circle.center, smaller_circle.center) + smaller_circle.radius < bigger_circle.radius

    def collide(self, other_obj, moved_center=(None, None), from_container_obj=False):
        ''' Collision handler for any type of obj'''
        # todo: handle game_class=="all"
        # todo: point class
        if not hasattr(other_obj, "__class__"):
            raise AttributeError(
                "other_obj must be a class or instance")

        # Handle instances
        if isinstance(other_obj, Circle):
            return self.collide_circle(other_obj, moved_center, from_container_obj)
        elif isinstance(other_obj, sprite_types.Rect):
            return self.collide_rect(other_obj, moved_center, from_container_obj)
        elif isinstance(other_obj, sprite_types.Img):
            return self.collide_img(other_obj, moved_center, from_container_obj)
        else:
            pass

        # Handle classes
        if inspect.isclass(other_obj):
            if issubclass(other_obj, Circle):
                return self.collide_list_circle(other_obj.list_instance, moved_center, from_container_obj)
            elif issubclass(other_obj, sprite_types.Rect):
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
        ''' Checks if this circle intersects with another_img. '''

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
        does_collide = (distance(self.center, another_circle.center) <= (
            self.radius + another_circle.radius))
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
        does_collide = (
            distance(self.center, (point_x, point_y)) <= self.radius)
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
        does_collide = not ((self.center_x + self.radius) < another_rect.left or (self.center_x - self.radius) > another_rect.right or (
            self.center_y + self.radius) < another_rect.top or (self.center_y - self.radius) > another_rect.bottom)
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

    @classmethod
    def get_circumcircle_from_rect(cls, another_rect):
    # create a circle with same center and radius=sqrt(w^2+h^2)/2
        return cls(another_rect.center, math.sqrt(another_rect.width ** 2 + another_rect.height ** 2) / 2)

    @classmethod
    def get_incircle_from_rect(cls, another_rect):
    # radius of incircle is same as the (min of width and height)/2 (as it's not a
    # square)
        return cls(another_rect.center, min(another_rect.width, another_rect.height) / 2)

    # union -needs to be a circle *within* which the union of the bounding box of all the circles can be fit.
    # warning about all the union functions: The circles returned are not
    # necessarily the most optimum union circle, but it will surely contain
    # the others.
    def _union(self, circle_1, circle_2):
        ''' ??? self.__union((new_center_x,new_center_y),new_radius) -> ([x,y],radius) which are the resultant values. '''
        return self.circumcircle_from_rect(circle_1.bbox.union(circle_2.bbox))

    def union(self, new_circle):
        ''' Returns a new circle which is the union of these two circles '''
        return self._union(self, new_circle)

    def union_ip(self, new_circle):
        ''' Turns this circle into a circle which is a union of these two circles. '''
        temp_circle = self._union(self, new_circle)
        self.center, self.radius = temp_circle.center, temp_circle.radius
        return self

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
        return self

    # draw functions
    def blit(self, surface, (x, y)=(None, None), color=None, clip_rect=None, width=1, use_antialiasing=False):
        ''' Draws this Circle on surface. It must be of width and height greater than or equal to its bbox.
            (x,y)->co-ordinates whether the center of the Circle should be drawn on the surface.
            width argument doesnt work with antialiasing. width=0 makes it filled.
            antialiasing may break in later versions as the backend pygame.gfxdraw is experimental.
            color falls back first to Circle.color (if present) and then to blue color.'''
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
            pygame.draw.circle(surface, color, (x, y), self.radius, width)
        else:
            pygame.gfxdraw.aacircle(surface, x, y, self.radius, color)

        if clip_rect:
            # Remove clip region
            surface.set_clip(None)

    def draw(self):
        tmp_dirty_sprite = {
            "sprite": self,
            # later shape may be used for matching insted of sprites, as sprite
            # may be subclassed, changing "sprite" obj
            "shape": "Circle",
            # Very IMP: If using Rect for bbox, use rect_to_pygame_rect like
            # below.
            "bbox": rect_to_pygame_rect(self.bbox),
            "config": {
                "center": self.center,
                "radius": self.radius,
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
