from base import *
import pygame.locals as pygame_const
from sprite_types import Rect, Img, Circle
from finite_state_engine import StateClass
# import event

g = fun_Game(800, 200, fps=30)


class ball_fixed(fun_Class):

    sprite_defaults = {
        "type": Rect,
        "params": {
            "size": (80, 40),
            "color": None
            # "file_name_or_obj":r"C:\Users\Machine\Pictures\Flight by Twitter_2.jpg"
        }
    }

    def action_instance_create(self, ev):
        self.n = 0

    def action_begin_step(self, ev):
        self.n += 1
        if self.n>10:
            pass
        print self.n

    def action_key_press_s(self, ev):
        if ev.dict["key_name"] == "d":
            self.state_parent.switch_state("None")


@register_class(fun_Game)
class ball(StateClass):

    sprite_defaults = {
        "type": Rect,
        "params": {
            "size": (80, 40),
            "color": None
            # "file_name_or_obj":r"C:\Users\Machine\Pictures\Flight by Twitter_2.jpg"
        }
    }

    def __init__(self, *args, **kwargs):
        super(ball, self).__init__(*args, **kwargs)
        self.add_state("ball_fixed", ball_fixed)

    def action_begin_step(self, ev):
        self.next_x, self.next_y = self.center

    def action_key_press_s(self, ev):
        if ev.dict["key_name"] == "s":
            self.switch_state("ball_fixed", self.x, self.y)

    def action_key_press_right(self, ev):
        if ev.dict["key_name"] == "right":
            self.next_x += 5

        if ev.dict["key_name"] == "left":
            self.next_x -= 5

        if ev.dict["key_name"] == "up":
            self.next_y -= 5

        if ev.dict["key_name"] == "down":
            self.next_y += 5

    def action_end_step(self, ev):
# if not self.collide(b, moved_center=(self.next_x, self.next_y)):
# if hasattr(self, "next_x"):
        self.center = self.next_x, self.next_y

    def action_trIal(self, ev):
        print ev.ev_name, ev.dict

    def action_instance_create(self, ev):
        print "Instance created"


@register_class(fun_Game)
class wall(fun_Class):
    sprite_defaults = {
        "type": Rect,
        "params": {
            "size": (60, 40),
            "color": None
        }
    }

if __name__ == "__main__":
    a = ball(0, 80)
    b = wall(450, 60)
    g.run()
