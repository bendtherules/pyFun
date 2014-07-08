import wx


def register_sprite_panel(sprite_panel):
    CanvasPanel.dict_sprite_panel[sprite_panel.game_shape_class] = sprite_panel
    return sprite_panel


class CanvasPanel(wx.Panel):

    """Parent canvas panel"""

    dict_sprite_panel = {}

    def __init__(self, *arg, **kwargs):
        super(CanvasPanel, self).__init__(*arg, **kwargs)
        self.create_internal()
        self.init_start_var()
        self.perc = 5.0 / 100
        self.update = False
        self.delta = None

        self.bind_events_default()

    def init_start_var(self):
        if not hasattr(self, "_start_w"):
            self._start_w = self.w
        if not hasattr(self, "_start_h"):
            self._start_h = self.h
        if not hasattr(self, "_start_left"):
            self._start_left = self.left
        if not hasattr(self, "_start_top"):
            self._start_top = self.top

    def create_internal(self):
        self.w, self.h = self.GetSizeTuple()
        self.left, self.top = self.GetPositionTuple()
        size = self.GetClientSize()
        self.buffer = wx.EmptyBitmap(max(1, size.width), max(1, size.height))

    def bind_events_default(self):
        self.Bind(wx.EVT_KEY_DOWN, self.action_move)
        self.Bind(wx.EVT_CHAR_HOOK, self.action_inflate)
        self.Bind(wx.EVT_IDLE, self.action_idle)
        self.Bind(wx.EVT_LEFT_DOWN, self.action_mouse_left_down)
        self.Bind(wx.EVT_LEFT_UP, self.action_mouse_left_up)
        self.Bind(wx.EVT_SET_FOCUS, self.action_unfocused)
        self.Bind(wx.EVT_KILL_FOCUS, self.action_unfocused)
        self.Bind(wx.EVT_MOTION, self.action_dragged)

    def action_mouse_left_up(self, ev):
        if self.HasCapture():
            self.ReleaseMouse()
        self.delta = None

    def action_dragged(self, ev):
        if ev.Dragging() and ev.LeftIsDown() and self.delta:
            pos_wrt_self = ev.GetPosition()
            pos_wrt_screen = self.ClientToScreen(pos_wrt_self)
            pos_wrt_parent = self.GetParent().ScreenToClient(pos_wrt_screen)
            pos = pos_wrt_parent

            newPos = (pos.x - self.delta.x, pos.y - self.delta.y)
            self.Move(newPos)
            self.left, self.top = self.GetPositionTuple()
            self.update = True

    def action_move(self, ev):
        keyText = chr(ev.GetUnicodeKey()).upper()
        # print "keyText= " + str(keyText)
        if keyText == "W":
            self.top -= 5
            print "moving up"
        if keyText == "A":
            self.left -= 5
            print "moving left"
        if keyText == "S":
            self.top += 5
            print "moving down"
        if keyText == "D":
            self.left += 5
            print "moving right"

        self.update = True
        ev.Skip()
        return True

    def action_inflate(self, ev):
        keyText = ev.GetKeyCode()  # .upper()

        # print "char= " + str(keyText)
        tmp_perc = None
        if keyText == wx.WXK_ADD or keyText == wx.WXK_NUMPAD_ADD:
            tmp_perc = self.perc
            print "Inflating"
        if keyText == wx.WXK_SUBTRACT or keyText == wx.WXK_NUMPAD_SUBTRACT:
            tmp_perc = -self.perc
            print "Deflating"

        if not (tmp_perc is None):
            new_w = self.w * (1 + tmp_perc)
            new_h = self.h * (1 + tmp_perc)
            new_left = self.left - (new_w - self.w) / 2
            new_top = self.top - (new_h - self.h) / 2
            print "old_w, old_h" + str((self.w, self.h))
            print "new_w, new_h" + str((new_w, new_h))
            print "old_left, old_top" + str((self.left, self.top))
            print "new_left, new_top" + str((new_left, new_top))
            print ""
            self.left, self.top = new_left, new_top
            self.w, self.h = new_w, new_h

        self.update = True
        ev.Skip()
        return True

    @property
    def center(self):
        return (self.left + self.w / 2), (self.top + self.h / 2)

    def action_idle(self, ev):
        if self.update:
            self.SetPosition((self.left, self.top))
            self.SetSizeWH(self.w, self.h)
            size = self.GetClientSize()
            self.buffer = wx.EmptyBitmap(
                max(1, size.width), max(1, size.height))
            self.GetParent().Refresh()
            self.update = False

    def action_mouse_left_down(self, ev):
        self.SetFocus()
        self.CaptureMouse()
        pos_wrt_self = ev.GetPosition()
        pos_wrt_screen = self.ClientToScreen(pos_wrt_self)
        pos_wrt_parent = self.GetParent().ScreenToClient(pos_wrt_screen)
        pos = pos_wrt_parent
        origin = self.GetPosition()
        self.delta = wx.Point(pos.x - origin.x, pos.y - origin.y)

    def action_focused(self, ev):
        self.Refresh()

    def action_unfocused(self, ev):
        self.Refresh()


@register_sprite_panel
class RectPanel(CanvasPanel):

    """docstring for RectPanel"""

    game_shape_class = "Rect"
    list_panel_inst = []

    def __init__(self, *arg, **kwargs):
        tmp_center = kwargs["center"]
        tmp_size = kwargs["size"]
        kwargs.pop("center")
        kwargs.pop("color")
        kwargs["pos"] = (
            (tmp_center[0] - tmp_size[0] / 2), (tmp_center[1] - tmp_size[1] / 2))
        super(RectPanel, self).__init__(*arg, **kwargs)
        self.brush = wx.Brush("Green")
        self.list_panel_inst.append(self)

    def get_props(self):
        return {
            "game_class": self.user_data["class"],
            "game_shape_class": self.game_shape_class,
            "config": {
                "center": self.center,
                "size": (self.w, self.h),
                "color": None,
            }
        }

    def bind_events_default(self):
        super(RectPanel, self).bind_events_default()
        self.Bind(wx.EVT_PAINT, self.action_paint_rect)
        self.Bind(wx.EVT_ERASE_BACKGROUND, self.action_clear_none)

    @property
    def pen_focused(self):
        if not hasattr(self, "_pen_focused"):
            self._pen_focused = wx.Pen(
                "Blue", width=3, style=wx.PENSTYLE_LONG_DASH)
            self._pen_focused.SetCap(wx.CAP_BUTT)
            self._pen_focused.SetJoin(wx.JOIN_ROUND)
        return self._pen_focused

    @pen_focused.setter
    def pen_focused(self, val):
        self._pen_focused = val

    def action_paint_rect(self, ev):
        dc = wx.BufferedPaintDC(self, self.buffer)
        dc.SetBackground(wx.Brush(wx.Colour(150, 150, 150, 100)))
        dc.Clear()
        if self.HasFocus():
            self.pen = self.pen_focused
        else:
            self.pen = wx.NullPen

        dc.SetBrush(self.brush)
        dc.SetPen(self.pen)

        dc.DrawRectangle(0, 0, self.w, self.h)
        # self.SetBackgroundColour("green")

    def action_clear_none(self, ev):
        wx.BufferedDC(None, self.buffer)


@register_sprite_panel
class CirclePanel(CanvasPanel):

    """docstring for CirclePanel"""

    game_shape_class = "Circle"
    list_panel_inst = []

    def __init__(self, *arg, **kwargs):
        tmp_center = kwargs["center"]
        tmp_radius = kwargs["radius"]
        kwargs.pop("color")
        kwargs["pos"] = (
            (tmp_center[0] - tmp_radius), (tmp_center[1] - tmp_radius))
        kwargs.pop("center")
        kwargs["size"] = (tmp_radius * 2, tmp_radius * 2)
        kwargs.pop("radius")
        super(CirclePanel, self).__init__(*arg, **kwargs)
        self.brush = wx.Brush("Green")
        self.list_panel_inst.append(self)

    def bind_events_default(self):
        super(CirclePanel, self).bind_events_default()
        self.Bind(wx.EVT_PAINT, self.action_paint_circle)
        self.Bind(wx.EVT_ERASE_BACKGROUND, self.action_clear_none)

    @property
    def pen_focused(self):
        if not hasattr(self, "_pen_focused"):
            self._pen_focused = wx.Pen(
                "Blue", width=3, style=wx.PENSTYLE_LONG_DASH)
            self._pen_focused.SetCap(wx.CAP_BUTT)
            self._pen_focused.SetJoin(wx.JOIN_ROUND)
        return self._pen_focused

    @pen_focused.setter
    def pen_focused(self, val):
        self._pen_focused = val

    def action_paint_circle(self, ev):
        dc = wx.BufferedPaintDC(self, self.buffer)
        dc.SetBackground(wx.Brush(wx.Colour(150, 150, 150, 100)))
        dc.Clear()
        if self.HasFocus():
            self.pen = self.pen_focused
        else:
            self.pen = wx.NullPen

        dc.SetBrush(self.brush)
        dc.SetPen(self.pen)

        dc.DrawCircle(self.w / 2, self.h / 2, self.w / 2)

    def action_clear_none(self, ev):
        wx.BufferedDC(None, self.buffer)

    def get_props(self):
        return {
            "class": self.user_data["class"],
            "game_shape_class": self.game_shape_class,
            "config": {
                "center": self.center,
                "radius": self.w / 2,
                "color": None,
            }
        }

    def get_start_props(self):
        return {
            "class": self.user_data["class"],
            "game_shape_class": self.game_shape_class,
            "config": {
                "center": (self._start_left + self._start_w / 2, self._start_top + self._start_h / 2),
                "radius": self._start_w / 2,
                "color": None,
            }
        }
