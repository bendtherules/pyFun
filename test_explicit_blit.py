from base import *
import pygame.locals as pygame_const
from sprite_types import Rect, Img, Circle
import event

g = fun_Game(800, 200, fps=30)

event.register_event_name("trIal")


def gen_TRIAL():
    return event.Event("trial", dict_={"haha": "hihi"})
# event.register_custom_event_generator(gen_TRIAL)


@register_class(fun_Game)
class ball(fun_Class):

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

    def action_begin_step(self, ev):
        self.next_x, self.next_y = self.center

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

    def action_key_press_p(self, ev):
        if ev.dict["key_name"] == "p":
            self.push_event_local(gen_TRIAL())

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
