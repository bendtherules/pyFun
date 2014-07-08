import base

# make fun_class with some action handlers, who just print for debug

# move to test
fun_Game.list_event.append(pygame.event.Event(KW_EVENTS_IB["JOY_BUTTON_UP"]))
fun_Game.list_event.append(pygame.event.Event(KW_EVENTS_IB["KEY_UP"]))
fun_Game.list_event.append(pygame.event.Event(KW_EVENTS_IB["KEY_DOWN"]))
fun_Game.process_event_list(fun_Game.list_event)
g = fun_Game(200, 200)
c = fun_Class(0, 0)
g.update_all_class()
