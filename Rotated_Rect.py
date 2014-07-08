import pygame
from math_utils import distance
import math
import base
from Circle import Circle

# start of Rotated_Rect class


class Rotated_Rect(pygame.Rect):
    # make a metaclass which wraps a lot of functions just like move is defined below.
    # functions to be wrapped - move,inflate
    # Think about them - clamp,clip,union,fit,contains,collide
    # the metaclass can probably also change the __str__ of the class.
    # About drawing - use pygame.transform.rotate to get a rotated surface to
    # be drawed.

    def __init__(self, leftTop_or_center, w_h, angle, centered_coords=False, color=None):
        ''' Angle in degrees.
            leftTop_or_center, w_h -> both are 2-element tuples or list
            centered_coords -> whether the (left,top) is actually intended to be (center_x,center_y) or not.
            I.e. if centered_coords==True the (left,top) co-ordinates are used as (center_x,center_y) co-ordinates of the Rotated_Rect'''
        self.angle = angle
        self.color = color
        try:
            left = leftTop_or_center[0]
            top = leftTop_or_center[1]
        except:
            raise AttributeError(
                "leftTop_or_center must be of format (left,top)")
        try:
            width = w_h[0]
            height = w_h[1]
        except:
            raise AttributeError("w_h must be of format (width,height)")

        if centered_coords:
            left = left - width / 2
            top = top - height / 2
        super(Rotated_Rect, self).__init__((left, top), (width, height))

    def __copy__(self):
        return Rotated_Rect((self.left, self.top), (self.width, self.height), self.angle)

    def __repr__(self):
        return "{0.__class__.__name__}((top={0.top}, left={0.left}), (width={0.width}, height={0.height}), angle={0.angle}, color={0.color})".format(self)

    @classmethod
    def create_from_rect(cls, another_rect, angle):
        return cls((another_rect.left, another_rect.top), (another_rect.width, another_rect.height), angle)

    def get_rect(self):
        return pygame.Rect((self.left, self.top), (self.width, self.height))

    # most in_place versions retained from super-class

    def move(self, x, y):
        return self.__copy__().move_ip(x, y)

    def inflate(self, x, y):
        return self.__copy__().inflate_ip(x, y)

    def normalize(self):
        # not sure what this one does - ask others
        return self.__copy__().normalize_ip()

    def rotate_ip(self, some_angle):
        self.angle += some_angle

    def rotate(self, some_angle):
        return self.__copy__().rotate_ip(some_angle)

    # generalise the parameters to accept x1,y1,x2,y2,rot_angle
    def rotate_point_about_center(self, x, y, theta=None):
        ''' x,y -> Absolute co-ords of the point to be rotated wrt to the rectangles center.
            self.centerx,self.centery are internally substracted from them.
            theta -> angle (in degrees) by which the point is to be rotated. Default value is self.angle.
            Returns absolute positions of the points after rotation. '''
        if theta is None:
            theta = self.angle
        return self.rotate_point(x, y, self.centerx, self.centery, theta)

    @staticmethod
    # to be allowed as rotate_point(class)
    def rotate_point(x, y, origin_x, origin_y, theta):
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
        return self.rotate_point_about_center(temp[0], temp[1])

    @property
    def topleft_rotated(self):
        temp = self.topleft
        return self.rotate_point_about_center(temp[0], temp[1])

    @property
    def bottomright_rotated(self):
        temp = self.bottomright
        return self.rotate_point_about_center(temp[0], temp[1])

    @property
    def topright_rotated(self):
        temp = self.topright
        return self.rotate_point_about_center(temp[0], temp[1])

    @property
    def midleft_rotated(self):
        temp = self.midleft
        return self.rotate_point_about_center(temp[0], temp[1])

    @property
    def midright_rotated(self):
        temp = self.midright
        return self.rotate_point_about_center(temp[0], temp[1])

    @property
    def midtop_rotated(self):
        temp = self.midtop
        return self.rotate_point_about_center(temp[0], temp[1])

    @property
    def midbottom_rotated(self):
        temp = self.midbottom
        return self.rotate_point_about_center(temp[0], temp[1])

    # related to bounding box
    @property
    def bbox(self):
        list_x = [self.topleft_rotated[0], self.topright_rotated[0],
                  self.bottomleft_rotated[0], self.bottomright_rotated[0]]
        list_y = [self.topleft_rotated[1], self.topright_rotated[1],
                  self.bottomleft_rotated[1], self.bottomright_rotated[1]]
        min_x = math.floor(min(list_x))
        max_x = math.ceil(max(list_x))
        min_y = math.floor(min(list_y))
        max_y = math.ceil(max(list_y))
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
        # get_rect used as incircle doesnt depend upon theta, same for rot and
        # non-rot rect
        Circle.get_incircle_from_rect(self.get_rect())

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
        return self.get_rect().collidepoint(self.rotate_point_about_center(temp_x, temp_y, -self.angle))

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
    def blit(self, surface, (x, y)=(None, None), color=None, clip_rect=None, width=1, use_antialiasing=False, blend=True):
        ''' Draws this Circle on surface. It must be of width and height greater than or equal to its bbox.
            (x,y)->co-ordinates whether the center of the Rotated_Rect should be drawn on the surface.
            width argument doesnt work with antialiasing. width=0 makes it filled.
            antialiasing may break in later versions as the backend pygame.gfxdraw is experimental.
            color falls back first to Circle.color (if present) and then to blue color.'''
        if not ((x, y) == (None, None)):
            sprite_to_draw = self.__copy__()
            sprite_to_draw.center = (x, y)
        else:
            sprite_to_draw = self
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

        iter_corners = [(temp[0] + x, temp[1] + y)
                        for temp in sprite_to_draw.corners_relative]
        if not use_antialiasing:
            pygame.draw.polygon(surface, color, iter_corners, width)
        else:
            pygame.draw.aalines(surface, color, True, iter_corners, blend)

        if clip_rect:
            # Remove clip region
            surface.set_clip(None)

    def draw(self):
        tmp_dirty_sprite = {
            "sprite": self,
            "shape": "Rotated_Rect",
            "bbox": self.bbox,
            "config": {
                "leftTop_or_center": (self.left, self.top),
                "w_h": (self.w, self.h),
                "angle": self.angle,
                "color": self.color
            }
        }
        for tmp_old_sprite in self.container_obj.list_rendered_sprite:
            # if any of them is eqv. to new dirty sprite, mark old one as
            # still_valid
            if tmp_old_sprite == tmp_dirty_sprite:
                # puts "still_valid" entry in the old_dirty_sprite_dict
                tmp_old_sprite["still_valid"] = True
                break
        else:
            # i.e. if no match found, list it as dirty sprite
            self.container_obj.list_dirty_sprite.append(tmp_dirty_sprite)

    def get_surface(self, surface=None, flags=0):
        ''' Returns a new surface with dimensions of (Rotated_Rect.bbox.width,Rotated_Rect.bbox.width) and other properties as surface.
            This Rotated_Rect can be safely drawn on it.'''
        if surface:
            return pygame.Surface((self.bbox.width, self.bbox.height), flags, surface)
        else:
            return pygame.Surface((self.bbox.width, self.bbox.height), flags)

    def get_surface_drawn(self, (x, y)=(None, None), color=None, width=1, use_antialiasing=False, blend=True, surface=None, flags=0):
        ''' Returns a surface which has the Rotated_Rect drwan on it. '''
        temp_surf = self.get_surface(surface, flags)
        self.draw(temp_surf, (x, y), color, width, use_antialiasing, blend)
        return temp_surf

    def collide_Rotated_Rect(self, another_Rotated_Rect):
        '''Checks whether this Rotated_Rect collides with another_titltedrect, which must be a instance of titledRect. '''
        # Rotates both Rotated_Rect by -another_Rotated_Rect.angle. So, another_Rotated_Rect becomes a Rect called temp_Rect.
        # Then check if the rotated version of this Rotated_Rect
        # (temp_Rotated_Rect) collides with the obtained Rect.
        temp_Rotated_Rect = self.rotate(-another_Rotated_Rect.angle)
        temp_Rect = another_Rotated_Rect.get_rect()
        return temp_Rotated_Rect.colliderect(temp_Rect)
