import base
import random
import sys
from base import pygame

tmp_fill_color = (156, 27, 210)
w = h = 200
is_test_ok = None
tmp_i = 0


class test_Game(base.fun_Game):

    def __init__(self, *arg, **kwarg):
        super(test_Game, self).__init__(*arg, **kwarg)
        self.fps = 100000  # max_fps

    def test_update(self):
        self.screen.fill(tmp_fill_color)
        tmp_px_array = pygame.PixelArray(self.screen)
        is_test_ok = True
        global tmp_i
        if tmp_i < 1000:
            tmp_i += 1
            tmp_w = random.randrange(0, w)
            tmp_h = random.randrange(0, h)
            if tmp_px_array[tmp_w][tmp_h] != self.screen.map_rgb(tmp_fill_color):
                is_test_ok = False
        else:
            if is_test_ok:
                print "Test OK"
            else:
                print "Test Broken"
            sys.exit()

a = test_Game(w, h)
a.run()

# Should display a purple window
