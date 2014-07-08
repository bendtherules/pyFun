import base
import random
import sys
from base import pygame

tmp_fill_color = (156, 27, 210)
w = h = 200
is_test_ok = None
tmp_i = 0


class test_Game(base.fun_Game):

    def test_update(self):
        tmp_px_array = pygame.PixelArray(self.screen)
        is_test_ok = True
        global tmp_i
        self.screen.fill(tmp_fill_color)
        if tmp_i:
            while tmp_i < 1000 and tmp_i:
                tmp_i += 1
                tmp_w = random.randrange(0, w)
                tmp_h = random.randrange(0, h)
                if tmp_px_array[tmp_w][tmp_h] != self.screen.map_rgb(tmp_fill_color):
                    is_test_ok = False
                    break

            if is_test_ok:
                print "Test OK"
            else:
                print "Test Broken"
            sys.exit()
        tmp_i += 1

a = test_Game(w, h)
a.run()

# Test made so that on first frame, screen is filled with purple.
# Rest of the test loop occurs on second frame
