import base
import sys
import random
from base import pygame

tmp_fill_color = (156, 27, 210)
w = random.randint(0, 1336)
h = random.randint(0, 768)
is_test_ok = None
tmp_i = 0


class test_Game(base.fun_Game):

    def test_update(self):
        tmp_px_array = pygame.PixelArray(self.screen)
        is_test_ok = True
        global tmp_i
        self.screen.fill(tmp_fill_color)
        if tmp_i:
            for tmp_w in range(w):
                for tmp_h in range(h):
                    tmp_i += 1
                    if tmp_px_array[tmp_w][tmp_h] != self.screen.map_rgb(tmp_fill_color):
                        is_test_ok = False
                        break
                if not is_test_ok:
                    break

            print "Test run for %s pixels" % (tmp_i - 1)
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
