import importlib
import sys
import os
import inspect
import room_sprite_panel
import json

dict_shape_panel = room_sprite_panel.CanvasPanel.dict_sprite_panel


def create_fake_cls(cls_name):
    class fake_cls(object):
        pass

    # cls_name is unicode, so str() it
    fake_cls.__name__ = str(cls_name)
    return fake_cls


class obj_ext(object):
    pass


def append_filepath(filepath):
    if filepath:
        sys.path.append(filepath)


def import_module(filename, filepath=None):
    append_filepath(filepath)
    module_ = importlib.import_module(filename)
    return module_


def import_file(filename, filepath=None):
    if not (filepath is None):
        full_filename = os.path.join(filepath, filename)
        print full_filename
    else:
        full_filename = filename
    file_ = open(full_filename, "r")
    return file_


def filter_class_with_panel(module_):
    list_class = inspect.getmembers(module_, inspect.isclass)
    list_filtered_cls = []
    for (cls_name, cls_obj) in list_class:
        if hasattr(cls_obj, "sprite_defaults"):
            tmp_sprite = cls_obj.sprite_defaults["type"]
            if tmp_sprite.map_class in dict_shape_panel.keys():
                cls_obj.sprite_defaults["panel"] = dict_shape_panel[
                    tmp_sprite.map_class]
                list_filtered_cls.append(cls_obj)

    return list_filtered_cls


def load_module(filename_or_module, filepath=None):
    if isinstance(filename_or_module, str) or isinstance(filename_or_module, unicode):
        module_ = import_module(filename_or_module, filepath)
    elif inspect.ismodule(filename_or_module):
        if filepath is None:
            module_ = filename_or_module
        else:
            raise TypeError("filepath must be None if first param is module")

    return filter_class_with_panel(module_)


def load_json(filename_or_file, filepath=None):
    if isinstance(filename_or_file, str) or isinstance(filename_or_file, unicode):
        file_ = import_file(filename_or_file, filepath)
    elif isinstance(filename_or_file, file):
        file_ = filename_or_file

    data_json = json.load(file_)
    if isinstance(file_, file):
        file_.close()

    list_class_data = data_json["class_data"]
    list_inst_data = data_json["instance_data"]
    list_loaded_cls = []

    for each_cls in list_class_data:
        tmp_cls = create_fake_cls(each_cls["game_class"])

        tmp_type = obj_ext()
        tmp_type.map_class = each_cls["game_shape_class"]
        tmp_cls.sprite_defaults = {
            # "panel": each_cls["pygame_class"],
            "params": each_cls["params"],
            "type": tmp_type
        }

        # add panel to sprite_defaults
        if each_cls["game_shape_class"] in dict_shape_panel.keys():
            tmp_cls.sprite_defaults["panel"] = dict_shape_panel[
                each_cls["game_shape_class"]]

        list_loaded_cls.append(tmp_cls)

    return (list_loaded_cls, list_inst_data)
