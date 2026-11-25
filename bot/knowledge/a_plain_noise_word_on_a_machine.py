from .lookup import entry

ANSWERS = ("home-and-diy", "technology")

_NOISE = ("clatter", "clatters", "clattering", "racket", "racketing", "din", "drone", "droning",
          "thunderous", "deafening", "palaver", "rattling", "roaring", "howling")

_PIPES = ("Ticking and clicking is the pipes expanding as they heat, which is normal and stops "
          "once the system is warm. Banging or gurgling means air or trapped water: bleed the "
          "radiators and check the boiler pressure sits between 1 and 1.5 bar. If a radiator "
          "clatters or drones while the heating is running, the valve may be part open or the "
          "pump set too fast: open the valve fully and turn the pump down a step.")

_VENTS = ("It is cooling itself because it is hot, so clear the vents with a can of air and check "
          "what is using the processor in Task Manager or Activity Monitor. A four-year-old laptop "
          "often just needs the dust out and new thermal paste (about £40 at a repair shop); if "
          "the noise continues at idle, the fan bearing is going.")

ENTRIES = [
    entry("radiator-plain-noise", (("radiator", "radiators"), _NOISE),
          _PIPES,
          avoid=("leak", "leaks", "leaking", "leaked", "cold", "colder", "bleed", "bleeding",
                 "bled", "thermostat", "valve", "valves", "pressure", "bar", "not working",
                 "doesnt work", "doesn't work", "wont heat", "won't heat", "radiator paint",
                 "painting", "remove", "take off", "replace", "size", "how many")),

    entry("laptop-fan-plain-noise", (("laptop", "laptops", "macbook", "notebook"), _NOISE),
          _VENTS,
          avoid=("my fan", "fan heater", "ceiling", "desk fan", "pedestal", "floor fan",
                 "tower fan", "box fan", "wall fan", "room fan", "bathroom", "kitchen",
                 "extractor", "cooker hood", "oven", "fridge", "freezer", "boiler", "radiator",
                 "washer", "washing machine", "dishwasher", "tumble", "dryer", "car", "van",
                 "engine", "console", "playstation", "ps5", "ps4", "xbox", "nintendo",
                 "computer fan", "pc fan", "desktop", "tower", "not charging", "won't turn on",
                 "wont turn on", "black screen", "slow", "overheat")),
]
