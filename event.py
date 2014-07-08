import pygame
import pygame.locals as pygame_consts
from UncasedDict import UncasedDict

DICT_EVENT_IB = {
    "QUIT": pygame_consts.QUIT,
    "ACTIVE_EVENT": pygame_consts.ACTIVEEVENT,
    "KEY_DOWN": pygame_consts.KEYDOWN,
    "KEY_UP": pygame_consts.KEYUP,
    "MOUSE_MOTION": pygame_consts.MOUSEMOTION,
    "MOUSE_BUTTON_UP": pygame_consts.MOUSEBUTTONUP,
    "MOUSE_BUTTON_DOWN": pygame_consts.MOUSEBUTTONDOWN,
    "JOY_AXIS_MOTION": pygame_consts.JOYAXISMOTION,
    "JOY_BALL_MOTION": pygame_consts.JOYBALLMOTION,
    "JOY_HAT_MOTION": pygame_consts.JOYHATMOTION,
    "JOY_BUTTON_UP": pygame_consts.JOYBUTTONUP,
    "JOY_BUTTOND_OWN": pygame_consts.JOYBUTTONDOWN,
    "VIDEO_RESIZE": pygame_consts.VIDEORESIZE,
    "VIDEO_EXPOSE": pygame_consts.VIDEOEXPOSE,
    # "USER_EVENT": pygame_consts.USEREVENT,
    # think of begin_step, step and end_step
}


DICT_KEYS = {
    r"BACKSPACE": pygame_consts.K_BACKSPACE,
    r"TAB": pygame_consts.K_TAB,
    r"CLEAR": pygame_consts.K_CLEAR,
    r"RETURN": pygame_consts.K_RETURN,
    r"PAUSE": pygame_consts.K_PAUSE,
    r"ESCAPE": pygame_consts.K_ESCAPE,
    r"SPACE": pygame_consts.K_SPACE,
    r"EXCLAIM": pygame_consts.K_EXCLAIM,
    r"QUOTEDBL": pygame_consts.K_QUOTEDBL,
    r"HASH": pygame_consts.K_HASH,
    r"DOLLAR": pygame_consts.K_DOLLAR,
    r"AMPERSAND": pygame_consts.K_AMPERSAND,
    r"QUOTE": pygame_consts.K_QUOTE,
    r"LEFTPAREN": pygame_consts.K_LEFTPAREN,
    r"RIGHTPAREN": pygame_consts.K_RIGHTPAREN,
    r"ASTERISK": pygame_consts.K_ASTERISK,
    r"PLUS": pygame_consts.K_PLUS,
    r"COMMA": pygame_consts.K_COMMA,
    r"MINUS": pygame_consts.K_MINUS,
    r"PERIOD": pygame_consts.K_PERIOD,
    r"SLASH": pygame_consts.K_SLASH,
    r"0": pygame_consts.K_0,
    r"1": pygame_consts.K_1,
    r"2": pygame_consts.K_2,
    r"3": pygame_consts.K_3,
    r"4": pygame_consts.K_4,
    r"5": pygame_consts.K_5,
    r"6": pygame_consts.K_6,
    r"7": pygame_consts.K_7,
    r"8": pygame_consts.K_8,
    r"9": pygame_consts.K_9,
    r"COLON": pygame_consts.K_COLON,
    r"SEMICOLON": pygame_consts.K_SEMICOLON,
    r"LESS": pygame_consts.K_LESS,
    r"EQUALS": pygame_consts.K_EQUALS,
    r"GREATER": pygame_consts.K_GREATER,
    r"QUESTION": pygame_consts.K_QUESTION,
    r"AT": pygame_consts.K_AT,
    r"LEFTBRACKET": pygame_consts.K_LEFTBRACKET,
    r"BACKSLASH": pygame_consts.K_BACKSLASH,
    r"RIGHTBRACKET": pygame_consts.K_RIGHTBRACKET,
    r"CARET": pygame_consts.K_CARET,
    r"UNDERSCORE": pygame_consts.K_UNDERSCORE,
    r"BACKQUOTE": pygame_consts.K_BACKQUOTE,
    r"a": pygame_consts.K_a,
    r"b": pygame_consts.K_b,
    r"c": pygame_consts.K_c,
    r"d": pygame_consts.K_d,
    r"e": pygame_consts.K_e,
    r"f": pygame_consts.K_f,
    r"g": pygame_consts.K_g,
    r"h": pygame_consts.K_h,
    r"i": pygame_consts.K_i,
    r"j": pygame_consts.K_j,
    r"k": pygame_consts.K_k,
    r"l": pygame_consts.K_l,
    r"m": pygame_consts.K_m,
    r"n": pygame_consts.K_n,
    r"o": pygame_consts.K_o,
    r"p": pygame_consts.K_p,
    r"q": pygame_consts.K_q,
    r"r": pygame_consts.K_r,
    r"s": pygame_consts.K_s,
    r"t": pygame_consts.K_t,
    r"u": pygame_consts.K_u,
    r"v": pygame_consts.K_v,
    r"w": pygame_consts.K_w,
    r"x": pygame_consts.K_x,
    r"y": pygame_consts.K_y,
    r"z": pygame_consts.K_z,
    r"DELETE": pygame_consts.K_DELETE,
    r"KP0": pygame_consts.K_KP0,
    r"KP1": pygame_consts.K_KP1,
    r"KP2": pygame_consts.K_KP2,
    r"KP3": pygame_consts.K_KP3,
    r"KP4": pygame_consts.K_KP4,
    r"KP5": pygame_consts.K_KP5,
    r"KP6": pygame_consts.K_KP6,
    r"KP7": pygame_consts.K_KP7,
    r"KP8": pygame_consts.K_KP8,
    r"KP9": pygame_consts.K_KP9,
    r"KP_PERIOD": pygame_consts.K_KP_PERIOD,
    r"KP_DIVIDE": pygame_consts.K_KP_DIVIDE,
    r"KP_MULTIPLY": pygame_consts.K_KP_MULTIPLY,
    r"KP_MINUS": pygame_consts.K_KP_MINUS,
    r"KP_PLUS": pygame_consts.K_KP_PLUS,
    r"KP_ENTER": pygame_consts.K_KP_ENTER,
    r"KP_EQUALS": pygame_consts.K_KP_EQUALS,
    r"UP": pygame_consts.K_UP,
    r"DOWN": pygame_consts.K_DOWN,
    r"RIGHT": pygame_consts.K_RIGHT,
    r"LEFT": pygame_consts.K_LEFT,
    r"INSERT": pygame_consts.K_INSERT,
    r"HOME": pygame_consts.K_HOME,
    r"END": pygame_consts.K_END,
    r"PAGEUP": pygame_consts.K_PAGEUP,
    r"PAGEDOWN": pygame_consts.K_PAGEDOWN,
    r"F1": pygame_consts.K_F1,
    r"F2": pygame_consts.K_F2,
    r"F3": pygame_consts.K_F3,
    r"F4": pygame_consts.K_F4,
    r"F5": pygame_consts.K_F5,
    r"F6": pygame_consts.K_F6,
    r"F7": pygame_consts.K_F7,
    r"F8": pygame_consts.K_F8,
    r"F9": pygame_consts.K_F9,
    r"F10": pygame_consts.K_F10,
    r"F11": pygame_consts.K_F11,
    r"F12": pygame_consts.K_F12,
    r"F13": pygame_consts.K_F13,
    r"F14": pygame_consts.K_F14,
    r"F15": pygame_consts.K_F15,
    r"NUMLOCK": pygame_consts.K_NUMLOCK,
    r"CAPSLOCK": pygame_consts.K_CAPSLOCK,
    r"SCROLLOCK": pygame_consts.K_SCROLLOCK,
    r"RSHIFT": pygame_consts.K_RSHIFT,
    r"LSHIFT": pygame_consts.K_LSHIFT,
    r"RCTRL": pygame_consts.K_RCTRL,
    r"LCTRL": pygame_consts.K_LCTRL,
    r"RALT": pygame_consts.K_RALT,
    r"LALT": pygame_consts.K_LALT,
    r"RMETA": pygame_consts.K_RMETA,
    r"LMETA": pygame_consts.K_LMETA,
    r"LSUPER": pygame_consts.K_LSUPER,
    r"RSUPER": pygame_consts.K_RSUPER,
    r"MODE": pygame_consts.K_MODE,
    r"HELP": pygame_consts.K_HELP,
    r"PRINT": pygame_consts.K_PRINT,
    r"SYSREQ": pygame_consts.K_SYSREQ,
    r"BREAK": pygame_consts.K_BREAK,
    r"MENU": pygame_consts.K_MENU,
    r"POWER": pygame_consts.K_POWER,
    r"EURO": pygame_consts.K_EURO,
}

LIST_EVENTS_GAME_PRE = ["BEGIN_STEP"]
# Custom events to be registered here
LIST_EVENTS_GAME_POST = ["STEP", "DRAW", "END_STEP"]
LIST_EVENTS_CUSTOM = [
    "KEY_PRESS", "MOUSE_PRESS", "Instance_Create", "Instance_Destroy"]


dict_event_name = UncasedDict()
list_event = []
list_event_old = []
list_state_key = []
list_state_key_old = []
list_state_mouse, list_state_mouse_old = [], []


def register_event_name(ev_name, ev_id=None):
    if (ev_name in dict_event_name):
        raise TypeError(
            "ev_name={0} is already registered".format(ev_name))
    if (ev_id is None):
        ev_id = max(
            pygame_consts.USEREVENT + 1, max(dict_event_name.values()) + 1)
    dict_event_name[ev_name] = ev_id


def add_each_event(ev):
    if not (ev.ev_name in dict_event_name):
        return TypeError("ev_name not registered")
    else:
        # make list_event_accessible
        list_event.append(ev)


def add_returned_events(ev_or_ev_list):
    # fix below cond
    if hasattr(ev_or_ev_list, "__iter__"):
        # list of events
        for each_ev in ev_or_ev_list:
            add_each_event(each_ev)
    else:
        # single event
        add_each_event(ev_or_ev_list)


def get_event_name(ev_id):
    for ev_name in dict_event_name:
        if dict_event_name[ev_name] == ev_id:
            return ev_name


def get_event_id(ev_name):
    return dict_event_name.get(ev_name)


def get_key_name(key_id):
    for key_name in DICT_KEYS:
        if DICT_KEYS[key_name] == key_id:
            return key_name


def get_key_id(key_name):
    return DICT_KEYS.get(key_name)


def get_mouse_btn_name(btn_id):
    # btn_id can be 0, 1 or 2
    if btn_id == 0:
        return "left"
    elif btn_id == 1:
        return "middle"
    elif btn_id == 2:
        return "right"
    else:
        raise ValueError("btn_id must be 0, 1 or 2")

# No sort_events, event_generators should be pushed in correct order


def fuzzy_match_event_name(string_, event_or_action):
    str_upper = string_.upper()
    if not (str_upper in dict_event_name):
        event_or_action = event_or_action.lower()
        if event_or_action == "event" or event_or_action == "action":
            # STR_STARTER becomes event_ or action_
            STR_STARTER = event_or_action.upper() + "_"
        else:
            raise TypeError(
                "event_or_action arg must be 'event' or 'action'.")
        str_normalized = str_upper[
            str_upper.find(STR_STARTER) + len(STR_STARTER):]
        for tmp_event_name in dict_event_name:
            # tmp event is the event_name, keys of KW_EVENTS
            tmp_event_name_normalized = tmp_event_name.upper().replace("_", "")
            if str_normalized.startswith(tmp_event_name) or str_normalized.startswith(tmp_event_name_normalized):
                return tmp_event_name
    else:
        return str_upper


def add_ev_name_GAME_PRE():
    for ev_name in LIST_EVENTS_GAME_PRE:
        register_event_name(ev_name)


def add_ev_name_IB():
    for ev_name in DICT_EVENT_IB:
        register_event_name(ev_name, DICT_EVENT_IB[ev_name])


def add_ev_name_GAME_POST():
    for ev_name in LIST_EVENTS_GAME_POST:
        register_event_name(ev_name)


def add_ev_name_CUSTOM():
    for ev_name in LIST_EVENTS_CUSTOM:
        register_event_name(ev_name)

# event_generators


def gen_event_GAME_PRE():
    return [Event(ev_name) for ev_name in LIST_EVENTS_GAME_PRE]


def gen_event_IB():
    # move current list to old list
    list_event_IB = pygame.event.get()
    # Above list contains pygame_events, cant be modified
    # But need to replace type with ev_name
    new_list_ev = []
    for each_ev in list_event_IB:
        ev_name = get_event_name(each_ev.type)
        tmp_ev = Event(ev_name, each_ev.dict)
        new_list_ev.append(tmp_ev)

    return new_list_ev


def gen_event_GAME_POST():
    return [Event(ev_name) for ev_name in LIST_EVENTS_GAME_POST]


def gen_event_KEY_PRESS():
    global list_state_key, list_state_key_old
    list_state_key_old = list_state_key
    list_state_key = pygame.key.get_pressed()
    list_key_press_event = []
    for tmp_key_id, bool_pressed in enumerate(list_state_key):
        if bool_pressed:
            tmp_key_name = get_key_name(tmp_key_id)
            list_key_press_event.append(
                Event("KEY_PRESS", {"key_name": tmp_key_name.lower(), "key_id": tmp_key_id}))
    return list_key_press_event


def gen_event_MOUSE_PRESS():
    global list_state_mouse, list_state_mouse_old
    list_state_mouse_old = list_state_mouse
    list_state_mouse = pygame.mouse.get_pressed()
    list_mouse_press_event = []
    for tmp_mouse_btn_id, bool_pressed in enumerate(list_state_mouse):
        if bool_pressed:
            tmp_btn_name = get_mouse_btn_name(tmp_mouse_btn_id)
            list_mouse_press_event.append(
                Event("MOUSE_PRESS", {"btn_name": tmp_btn_name.lower(), "btn_id": tmp_mouse_btn_id}))
    return list_mouse_press_event

# pygame.mouse.get_pressed

# add ev_names
# Ordered list of name adders
LIST_ADDER_EV_NAME = [
    add_ev_name_IB, add_ev_name_GAME_PRE, add_ev_name_GAME_POST, add_ev_name_CUSTOM]
for each_adder_func in LIST_ADDER_EV_NAME:
    each_adder_func()


# add event generators
# Ordered list of generators
list_ordered_custom_generator = [gen_event_KEY_PRESS, gen_event_MOUSE_PRESS]

list_ordered_generators = [
    gen_event_GAME_PRE, gen_event_IB, list_ordered_custom_generator, gen_event_GAME_POST]


def register_custom_event_generator(ev_func):
    ''' ev_func will be run in each step before step event and after begin step event and should return a / a list of dicts
        each with ev_name (to be registered beforehand) and other props'''
    global list_ordered_custom_generator
    list_ordered_custom_generator.append(ev_func)


def get_event_generators():
    return_list = []
    for gen_or_list in list_ordered_generators:
        if hasattr(gen_or_list, "__iter__"):
            return_list.extend(gen_or_list)
        else:
            return_list.append(gen_or_list)
    return return_list


# Todo: Howto programatically register at the right position of generator list
# Event collector


def collect_events():
    # First, clear the old ev list
    global list_event, list_event_old
    list_event_old = list_event
    list_event = []
    for each_gen in get_event_generators():
        add_returned_events(each_gen())

# Event dispatcher
# To be used by appr. classes


def dispatch_events_class(cls):
    # cls.list_class must be available
    for each_class in cls.list_class:
        each_class.dispatch_events_instance(list_event)


def dispatch_events_instance(cls, list_event):
    for each_instance in cls.list_instance:
        each_instance.dispatch_events_self(list_event)


def dispatch_events_self(self, list_event):
    for each_ev in list_event:
        if each_ev.ev_name.upper() in self.dict_action_func:
            self.dispatch_events_local()
            for each_action in self.dict_action_func[each_ev.ev_name]:
                # similar as self.action_step(each_ev)
                each_action(self, each_ev)


def dispatch_events_local(self):
    for each_ev in self.list_event_local:
        if each_ev.ev_name.upper() in self.dict_action_func:
            for each_action in self.dict_action_func[each_ev.ev_name]:
                # similar as self.action_step(each_ev)
                each_action(self, each_ev)
    self.clear_event_local()


def push_event_local(self, ev_or_ev_list):
    if hasattr(ev_or_ev_list, "__iter__"):
        # list of events
        for each_ev in ev_or_ev_list:
            self._push_event_local_single(each_ev)
    else:
        # single event
        self._push_event_local_single(ev_or_ev_list)


def clear_event_local(self):
    self.list_event_local = []


def _push_event_local_single(self, ev):
    self.list_event_local.append(ev)


class Event(object):

    def __init__(self, ev_name, dict_=None):
        super(Event, self).__init__()
        self.ev_name = ev_name
        self.dict = dict_


def _check_event(ev_name, new_or_old):
    ''' ev_name_or_type => name_or_type(numb)_of_event
        new_or_old => current_event_list or old_event_list '''
    global list_event, list_event_old
    matched_events = []
    if new_or_old == "new":
        list_to_check = list_event
    elif new_or_old == "old":
        list_to_check = list_event_old
    else:
        raise AttributeError("new_or_old must be 'new' or 'old'.")

    ev_name = fuzzy_match_event_name(ev_name, "event")

    for ev in list_to_check:
        if ev.ev_name == ev_name:
            matched_events.append(ev)
    return matched_events


def check_event(ev_name):
    return _check_event(ev_name, "new")


def check_event_old(ev_name):
    return _check_event(ev_name, "old")


def _get_key_press(key_name=None, new_or_old=None):
    ''' Returns list of dict with key_name and key_id, if key_name matches.
        If key_name is None, all key preeses are allowed.'''
    global list_state_key, list_state_key_old
    if new_or_old == "new":
        list_to_check = list_state_key
    elif new_or_old == "old":
        list_to_check = list_state_key_old
    else:
        raise TypeError("new_or_old must be 'new' or 'old', CANT be None")
    list_key_press_event = []
    for tmp_key_id, bool_pressed in enumerate(list_to_check):
        if bool_pressed:
            tmp_key_name = get_key_name(tmp_key_id)
            if (key_name is None) or (tmp_key_name.lower() == key_name.lower()):
                # Todo: Cant match event_name directly, need a fuzzy key name
                # search func
                list_key_press_event.append(
                    {"key_name": tmp_key_name.lower(), "key_id": tmp_key_id})
    return list_key_press_event


def _get_mouse_press(btn_name=None, new_or_old=None):
    global list_state_mouse, list_state_mouse_old
    if new_or_old == "new":
        list_to_check = list_state_mouse
    elif new_or_old == "old":
        list_to_check = list_state_mouse_old
    else:
        raise TypeError("new_or_old must be 'new' or 'old', CANT be None")

    list_mouse_press_event = []
    for tmp_mouse_btn_id, bool_pressed in enumerate(list_to_check):
        if bool_pressed:
            tmp_btn_name = get_mouse_btn_name(tmp_mouse_btn_id)
            if (btn_name is None) or (btn_name.lower() == tmp_btn_name.lower()):
                list_mouse_press_event.append(
                    {"btn_name": tmp_btn_name.lower(), "btn_id": tmp_mouse_btn_id})
    return list_mouse_press_event


def get_key_press(key_name=None):
    return _get_key_press(key_name, "new")


def get_key_press_old(key_name=None):
    return _get_key_press(key_name, "old")


def get_mouse_press(btn_name=None):
    return _get_mouse_press(btn_name, "new")


def get_mouse_press_old(btn_name=None):
    return _get_mouse_press(btn_name, "old")
