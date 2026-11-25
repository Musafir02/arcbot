import re

from .lookup import entry

ANSWERS = ("home-and-diy",)

_MACHINE_IN_THE_CHAT = ("washing machine", "washer", "washer dryer", "dishwasher", "washing")
_A_SMELLY_MACHINE = ("smell", "smells", "smelly", "stink", "stinks", "damp", "musty",
                     "mould", "mold", "mildew", "fusty", "whiff", "sour")


def _a_damp_machine_and_its_door(memory, understood):
    text = " " + str((understood or {}).get("clean") or (understood or {}).get("text") or "").lower() + " "
    if re.search(r"cant|cannot|can not|won'?t|will not|does not|doesn'?t|hard to|stuck|swings?|"
                 r"swinging|on its own|itself|hanging|off|lock|keyhole|slam|bang|squeak|squeal|"
                 r"rub|paint|draught|draft|dragging|dropped|measure|door is not|door isnt|"
                 r"door isn'?t|door is broken|door is stiff|door is loose|door is stuck|"
                 r"door is jamming|door was broken|door was stiff|door was loose", text, re.I):
        return None
    said = [str((memory.get("topic") or {}).get("text") or "")]
    said += [str(one.get("text") or "") for one in (memory.get("topics") or [])[-4:]]
    chat = " ".join(said).lower()
    if not any(word in chat for word in _MACHINE_IN_THE_CHAT):
        return None
    if not any(word in chat for word in _A_SMELLY_MACHINE):
        return None
    return ("Then that is very likely the cause: the inside of the machine stays wet between "
            "washes, and the smell grows in water that cannot dry. Leave the door and the "
            "detergent drawer open between washes, wipe the rubber seal round the door, and run "
            "one hot 60C or 90C wash with a machine cleaner or a cup of bicarbonate of soda to "
            "clear what has already built up.")


ENTRIES = [
    entry(
        "damp-machine-door",
        (("door", "doors"),
         ("shut", "shuts", "closed", "closing", "left shut", "keep it shut")),
        _a_damp_machine_and_its_door,
        bias=3,
        avoid=("stiff", "sticking", "sticks", "tight", "hard to shut", "hard to close", "rubbing",
               "rubs", "drags", "dragging", "squeak", "squeaks", "squeaking", "squeal", "creak",
               "creaks", "hinge", "hinges", "latch", "lock", "locked", "keyhole", "slam", "slams",
               "bang", "bangs", "banging", "swings", "swinging", "swung", "on its own", "itself",
               "hanging", "off", "dropped", "draught", "draft", "measure", "paint", "cant shut",
               "cant close", "cannot shut", "cannot close", "can not shut", "can not close",
               "wont shut", "wont close", "will not shut", "will not close", "does not shut",
               "does not close", "doesnt shut", "doesnt close", "fridge", "freezer", "oven",
               "microwave", "cooker", "car door", "front door",
               "back door", "car", "van", "bedroom door", "shower", "curtain", "blinds", "window",
               "gate", "key", "lock", "house", "flat", "landlord", "neighbour", "neighbor"),
    ),
]
