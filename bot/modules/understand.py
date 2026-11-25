from ..memory import recall, the_thing_it_is
from ..understanding import understand

PRIORITY = 10000


def observe(text, memory):
    read = understand(text, memory)
    filled = the_thing_it_is(read, memory)
    if filled is None:
        from ..memory.topics import the_advice_ask_with_its_doing
        filled = the_advice_ask_with_its_doing(read, memory)
    memory["understood"] = filled if filled is not None else read
    memory["understood"]["looks_back"] = recall.the_earlier_turn(text, memory)
