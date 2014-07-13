#!/bin/env python
import wx
import json
import load_map
import os
import room_sprite_panel as sprite_panel
from copy import deepcopy


class MyFrame(wx.Frame):

    def __init__(self):
        self.size = (500, 300)
        wx.Frame.__init__(self, None, -1, "My Frame", size=self.size)

        self.panel_ctrl = wx.Panel(
            self, -1, size=(-2, -1))
        self.panel_ctrl.SetBackgroundColour("aquamarine")
        self.panel_ctrl.SetMaxSize((250, -1))

        # load some images into an image list
        il = wx.ImageList(16, 16, True)
        il.Add(wx.EmptyBitmap(16, 16))

        # create the list control
        self.panel_ctrl.list_ctrl = wx.ListCtrl(
            self.panel_ctrl, -1, style=wx.LC_LIST, size=(200, 180))

        self.load_module_py()
        # assign the image list to it
        # self.panel_ctrl.list_ctrl.AssignImageList(il, wx.IMAGE_LIST_SMALL)
        self.panel_canvas = wx.Panel(
            self, -1, size=(-3, -1))
        self.panel_canvas.SetBackgroundColour("light blue")

        bxszr = wx.BoxSizer(wx.HORIZONTAL)
        bxszr.Add(self.panel_ctrl, 2, flag=wx.EXPAND)
        bxszr.Add(self.panel_canvas, 3, flag=wx.EXPAND)
        self.SetSizer(bxszr)
        # self.Fit()

        self.bind_events_default()

    def load_module_py(self):
        # Load map
        wildcard_py = "Python source (*.py)|*.py|" \
            "Compiled Python (*.pyc)|*.pyc|" \
            "All files (*.*)|*.*"
        dialog_file = wx.FileDialog(None, "Choose game.py file", os.getcwd(),
                                    "", wildcard_py, wx.OPEN)
        if dialog_file.ShowModal() == wx.ID_OK:
            self.module_path = dialog_file.GetPath()
            filename = os.path.basename(self.module_path)
            filename_without_ext = filename[:filename.rfind(".")]
            filepath = os.path.dirname(self.module_path)
            list_loaded_cls = load_map.load_module(
                filename_without_ext, filepath)
            self.dict_loaded_cls = {}
            for each_cls in list_loaded_cls:
                self.dict_loaded_cls[each_cls.__name__] = each_cls
            del list_loaded_cls
        else:
            raise TypeError("Enter a filename to proceed")

        self.sync_panel_ctrl(self.dict_loaded_cls.keys())

        dialog_file.Destroy()

    def sync_panel_ctrl(self, list_str):
        for index, str_ in enumerate(list_str):
            if index > self.panel_ctrl.list_ctrl.GetItemCount() - 1:
                method_ = self.panel_ctrl.list_ctrl.InsertStringItem
            else:
                method_ = self.panel_ctrl.list_ctrl.SetItemText
        # try:
            method_(index, str_)
            # self.panel_ctrl.list_ctrl.Refresh()
        # except:
        # pass

    def create_shape_panel(self, str_, default_center):
        tmp_game_cls = self.dict_loaded_cls[str_]
        tmp_dict = tmp_game_cls.sprite_defaults

        if "center" in tmp_dict:
            center = tmp_dict["center"]
        else:
            center = default_center

        tmp_shape_panel = tmp_dict["panel"](
            self.panel_canvas, center=center, **tmp_dict["params"])
        tmp_shape_panel.user_data = {"class": tmp_game_cls.__name__}
        tmp_shape_panel.Show()
        self.panel_canvas.Refresh()
        # self.list_shape.append(tmp_shape_panel)

    def action_key_press(self, ev):
        print self.__class__
        keyCode = ev.GetKeyCode()
        try:
            keyText = chr(keyCode).upper()
        except:
            keyText = None
        print keyText

        if keyText == "\r":
            focus_id = self.panel_ctrl.list_ctrl.FocusedItem
            focus_text = self.panel_ctrl.list_ctrl.GetItem(focus_id).GetText()
            self.create_shape_panel(focus_text, (0, 0))
        if keyText == "E":
            print self.export_data("map.json")

    def bind_events_default(self):
        print "binding"
        self.panel_ctrl.list_ctrl.Bind(wx.EVT_KEY_DOWN, self.action_key_press)

    @staticmethod
    def for_all_panel_class(func_):
        return_list = []
        for tmp_panel_cls in sprite_panel.CanvasPanel.dict_sprite_panel.values():
            val_return = func_(tmp_panel_cls)
            return_list.append(val_return)

        return return_list

    @staticmethod
    def for_all_panel_inst(func_, flatten=False):
        # todo: use for_all_panel_class
        list_return = []
        for tmp_panel_cls in sprite_panel.CanvasPanel.dict_sprite_panel.values():
            tmp_list = []
            for tmp_panel_inst in tmp_panel_cls.list_panel_inst:
                val_return = func_(tmp_panel_inst)
                tmp_list.append(val_return)
            if flatten:
                list_return.extend(tmp_list)
            else:
                list_return.append(tmp_list)

        return list_return

    @staticmethod
    def export_game_cls(game_cls):
        dict_return = {}
        dict_return["game_class"] = game_cls.__name__

        tmp_sprite_defaults = deepcopy(game_cls.sprite_defaults)
        dict_return["game_shape_class"] = tmp_sprite_defaults["type"].map_class
        dict_return["params"] = tmp_sprite_defaults["params"]

        return dict_return

    def for_all_game_cls(self, func_):
        list_return = []
        for tmp_game_cls in self.get_all_loaded_cls():
            val_return = func_(tmp_game_cls)
            list_return.append(val_return)
        return list_return

    def get_all_loaded_cls(self):
        return self.dict_loaded_cls.values()

    def export_data(self, file_=None, pprint_=True):

        class_data = self.for_all_game_cls(
            lambda game_cls: self.export_game_cls(game_cls))
        instance_data = self.for_all_panel_inst(
            lambda panel_inst: panel_inst.get_props(), flatten=True)

        data = {"class_data": class_data, "instance_data": instance_data}
        if pprint_:
            jsoned_data = json.dumps(data, indent=4)
            print jsoned_data
        else:
            jsoned_data = json.dumps(data)

        if file_ is None:
            return jsoned_data
        elif isinstance(file_, str):
            file_ = open(file_, "w")

        if isinstance(file_, file):
            file_.write(jsoned_data)
            file_.close()
        else:
            raise TypeError("file_ parameter must be of file or str type.")

if __name__ == '__main__':
    app = wx.PySimpleApp()
    frame = MyFrame()
    frame.Show(True)
    app.MainLoop()
