import pyFun


class pong(pyFun.fun_Game):

    class bat(pyFun.fun_Class):

        def __init__(self, up_key, down_key, *args, **kwargs):
            super(bat, self).__init__(*args, **kwargs)
            self.up_key = up_key
            self.down_key = down_key
            self.img = pyFun.shapes.rect(w=24, h=96)

        def action_create(self):
            self.move_step = 3

        def action_key_press(self, key):
            if key == self.up_key:
                self.y -= self.move_step
            if key == self.down_key:
                self.y += self.move_step

        def action_touch_room_boundary(self):
            self.y = self.y_prev

game = pong(width=760, height=640, fps=60)
game.bat(up_key=k_up, down_key=k_down, x=80, y=game.h / 2)
game.bat(up_key=k_w, down_key=k_s, x=game.w - 80, y=game.h / 2)
game.run()
