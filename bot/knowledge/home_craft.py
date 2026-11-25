
import re


_A_DEPOSIT_COMING_BACK = re.compile(
    r"\b(?:tenancy|scheme|landlord|letting agent|deposit protection|moved out|end of tenancy|"
    r"deposit back|deposit returned|deposit return|deposit paid|paid a deposit)\b")


def _a_deposit_coming_back(understood):
    read = understood if isinstance(understood, dict) else {}
    said = " ".join(str(read.get("clean") or read.get("text") or "").lower().split())
    return bool(_A_DEPOSIT_COMING_BACK.search(said))


import re

from ..understanding.topics import the_bin_is_on_a_machine
from .costs import A_AGE_OWNED

_FOOD_OWN_SMELL = re.compile(
    r"\b(?:milk|yoghurt|yogurt|cream|soured cream|sour cream)\b[^.?!]{0,30}?"
    r"\b(?:smells|smell|smelt|smelled|stinks|stink|gone off|went off|is off|has turned|turned|"
    r"curdled|sour)\b")


def _not_the_food_in_the_fridge(understood):
    text = " ".join(str(one) for one in ((understood or {}).get("words") or ())).lower()
    if not text:
        text = str((understood or {}).get("clean") or (understood or {}).get("text") or "").lower()
    return not _FOOD_OWN_SMELL.search(text)

STOPPED_ALTOGETHER = (
    "stopped working", "stops working", "stopped work", "not working", "isnt working",
    "isn't working", "doesnt work", "doesn't work", "wont work", "won't work", "no longer works",
    "broken", "broke", "broken down", "broke down", "packed in", "packed up", "gave up",
    "dead", "no power", "wont come on", "won't come on", "wont turn on", "won't turn on",
    "wont switch on", "won't switch on", "faulty", "gone wrong", "went wrong")

FIXTURE_FIRST_CHECKS = (
    (("power shower", "electric shower", "shower", "showers"),
     "Start at the switch that feeds it: the pull cord or the wall switch, then the fuse in the "
     "unit, because a dead shower is usually that. If the unit lights up but no water runs, it is "
     "the solenoid valve or scale in the head, and on a mixer run the other hot taps first."),
    (("mixer tap", "monobloc", "tap", "taps", "faucet", "faucets"),
     "Look for a small screw slot on the pipe under the sink or the bath, because a tap that will "
     "not run at all is usually an isolator someone turned off or a valve that has seized. If the "
     "water comes but only trickles, unscrew the spout end and soak the aerator in vinegar."),
    (("toilet", "toilets", "loo", "cistern"),
     "Turn the isolation screw off, lift the lid and watch the cistern fill: a float arm stuck or "
     "an inlet valve furred up with scale is the usual reason the loo has stopped. A button with "
     "no resistance is the flush valve or its link, which is a cheap part."),
    (("doorbell", "doorbells", "chime", "chimes", "bell push", "bell"),
     "Start with the power to it: a wired bell has a transformer near the consumer unit, and a "
     "wireless one has a battery in the push and another in the chime. A push that is stuck, wet "
     "or corroded is the next thing."),
    (("garage door", "up and over door", "roller door", "sectional door"),
     "Use the manual release first - usually a red cord or a handle on the mechanism - so the car "
     "is not stuck in, then check the power, the remote's battery and the safety sensors at the "
     "bottom of the tracks. A door that opens a foot and stops is the travel limits or a broken "
     "spring, and a spring is not a DIY job."),
    (("heated towel rail", "towel rail", "towel radiator", "ladder rail",
      "radiator", "radiators", "rad", "rads"),
     "Bleed it, then take the head off the thermostatic valve and press the pin: one cold radiator "
     "is air or a pin stuck down. If every radiator is cold it is the boiler, the programmer or a "
     "zone valve, and one that is cold at the bottom wants a flush."),
)


def _the_fixture_that_stopped(understood):
    reading = understood if isinstance(understood, dict) else {}
    said = " ".join(str(one) for one in (reading.get("words") or ())).lower()
    if not said:
        said = str(reading.get("clean") or reading.get("text") or "").lower()
    if not said or not any(word in said for word in STOPPED_ALTOGETHER):
        return None
    for names, check in FIXTURE_FIRST_CHECKS:
        if any(re.search(r"\b" + re.escape(name) + r"s?\b", said) for name in names):
            return check
    return None


A_FIXTURE_IS_NOT_A_DECORATING_JOB = ("leak", "leaks", "leaking", "drip", "dripping", "blocked", "blockage",
                     "wont drain", "won't drain", "not draining", "wont flush", "won't flush",
                     "smell", "smells", "smelly", "noise", "noisy", "banging", "rattling",
                     "cold", "hot water", "pressure", "limescale", "scale", "mould", "mold",
                     "buy", "buying", "worth", "cost", "price", "cheaper", "rent", "landlord",
                     "install", "installing", "fit a new", "replace", "replacing", "replacement",
                     "paint", "painting", "tile", "tiling", "decorate", "decorating",
                     "how do i", "how to", "should i",
                     "shower door", "shower doors", "shower screen", "shower tray", "door seal",
                     "upstairs", "downstairs", "top floor", "first floor")

def _a_fixture_that_stopped_was_the_question(understood):
    return _the_fixture_that_stopped(understood) is not None


def _the_stopped_fixture_entries(entry):
    for _names, _check in FIXTURE_FIRST_CHECKS:
        yield entry("a-fixture-that-stopped-" + _names[0].replace(" ", "-"),
                    (_names, STOPPED_ALTOGETHER),
                    lambda memory, reading: _the_fixture_that_stopped(reading),
                    avoid=A_FIXTURE_IS_NOT_A_DECORATING_JOB,
                    guard=_a_fixture_that_stopped_was_the_question, bias=3)

BOILER_DIY = ("myself", "own", "diy", "legal", "allowed")

SERVICE_WORDS = ("service", "services", "servicing", "serviced", "annual", "yearly", "certificate")


def _an_ask_about_servicing_my_own(understood):
    words = {str(one).lower() for one in ((understood or {}).get("words") or ())}
    text = str((understood or {}).get("clean") or (understood or {}).get("text") or "").lower()
    return bool(words & set(SERVICE_WORDS)) or any(one in text for one in SERVICE_WORDS)


_A_FLY_THAT_TRAVELS = re.compile(
    r"\b(?:fly|flys|flies|flew|flown|flying)\s+"
    r"(?:"
    r"(?:to|into|over|via)\s+"
    r"|"
    r"(?:out|back|home|abroad|from|off|at|with)\b"
    r"|"
    r"(?:[a-z']+\s+){0,3}(?:on|next|this)\s+"
    r"(?:monday|tuesday|wednesday|thursday|friday|saturday|sunday|weekend|week|month|"
    r"morning|afternoon|evening|night|\d)"
    r")")


def _the_fly_is_not_a_verb(understood):
    text = " ".join(str(one) for one in ((understood or {}).get("words") or ())).lower()
    if not text:
        text = str((understood or {}).get("clean") or (understood or {}).get("text") or "").lower()
    return _A_FLY_THAT_TRAVELS.search(text) is None


_A_BAR_WITH_A_FIGURE = re.compile(
    r"\b(?:\d+(?:\.\d+)?|half|quarter|one|two|three)\s+(?:a\s+)?bars?\b")
_PRESSURE_WORDS = frozenset(("pressure", "psi", "gauge", "boiler", "boilers", "combi",
                             "radiator", "radiators", "heating", "central"))


def _a_gauge_reading(understood):
    reading = understood or {}
    text = str(reading.get("clean") or reading.get("text") or "").lower()
    words = set(str(one).lower() for one in (reading.get("words") or ()))
    if words & _PRESSURE_WORDS:
        return True
    return _A_BAR_WITH_A_FIGURE.search(text) is not None


_WILL_NOT_EMPTY = re.compile(
    r"\b(block|blocks|blocked|blockage|blocking|clog|clogs|clogged|clogging|jam|jams|jammed|"
    r"stuff|stuffed|bunged|plugged)\b"
    r"|\b(backed|backing)\s+up\b"
    r"|\b(water\s+(is\s+)?(sitting|standing|left|stuck|pooling|pooled|trapped)|standing water|"
    r"full of water|water in the drum|water in the bottom|water inside the drum|pool of water|"
    r"water\s+(wont|won't|not)\s+(go|going|leave|leaving|drain|draining))\b"
    r"|\b(no|not|n't|cant|can\s+t|cannot|can\s*['\u2019]?\s*t|couldnt|couldn't|could not|"
    r"unable|wont|won't|wouldnt|wouldn't|doesnt|doesn't|didnt|didn't|isnt|isn't|wasnt|wasn't|"
    r"never|stopped|fail|fails|failed|failing|struggling|struggles)\b[^.]{0,45}?"
    r"\b(drain|drains|draining|drained|empty|empties|emptying|emptied|pump|pumps|pumping)\b"
    r"|\b(drain\w*|pump\w*|emptying)\b[^.]{0,18}?\b(blocked|clogged|jammed|stuck|slow|slowly|"
    r"sluggish|not working|broken)\b"
    r"|\b(slow|slowly|sluggish)\b[^.]{0,18}?\b(drain|drains|draining|empty|emptying)\b"
    r"|\b(empty|emptying|drain|draining)\s+(the|my|its|this)\s+(machine|washer|drum|water)\b"
    r"|\b(get|getting|got)\s+(the|my|its|this)\s+(water|machine|washer|drum|washing|clothes)\b"
    r"[^.]{0,22}?\b(out|to drain|to empty)\b"
    r"|\b(to\s+(get\s+it\s+)?(drain|empty))\b")


_WATER_LEAVING = re.compile(
    r"\b(leak|leaks|leaked|leaking|leaky|puddle|puddles|drip|drips|dripping|dribble|"
    r"flood|floods|flooded|flooding|pour|pours|pouring|seep|seeps|seeping|seeped|"
    r"spill|spills|spilling|spilt)\b"
    r"|\b(coming out|came out|running out|spilling out|working its way out|"
    r"water under|water on the|water in the bottom|water all over|underneath|"
    r"under\s+(the\s+|my\s+)?(machine|washing machine|washer|drum)|under it|"
    r"on the floor|all over the floor|wet floor|damp patch)\b")


A_WASH_NAMED = frozenset((
    "wash", "washes", "washed", "washing", "laundry", "load", "loads", "cycle", "cycles",
    "machine", "washer", "tumble", "drum", "eco"))


A_TEMPERATURE_SAID = re.compile(
    r"\b(?:20|30|40|60)\s*(?:c|degrees?|deg)\b"
    r"|\b(?:twenty|thirty|forty|sixty)\s+degrees?\b")
A_BARE_TEMPERATURE = re.compile(r"\b(?:20|30|40|60)\b")


def _a_wash_is_named(understood):
    text = " ".join(str(one) for one in ((understood or {}).get("words") or ())).lower()
    if not text:
        text = str((understood or {}).get("clean") or (understood or {}).get("text") or "").lower()
    words = text.replace(",", " ").split()
    if any(word in A_WASH_NAMED for word in words):
        return True
    if A_TEMPERATURE_SAID.search(text):
        return True
    return len(set(A_BARE_TEMPERATURE.findall(text))) > 1


def _it_is_water_leaving(understood):
    text = " ".join(str(one) for one in ((understood or {}).get("words") or ())).lower()
    if not text:
        text = str((understood or {}).get("clean") or (understood or {}).get("text") or "").lower()
    return bool(_WATER_LEAVING.search(text))


_A_WASHER = frozenset(("washer", "washers", "washing machine", "washer dryer"))
_ANOTHER_KIND_OF_WASHER = frozenset((
    "tap", "taps", "faucet", "faucets", "mixer", "monobloc", "ball valve", "ballcock",
    "bolt", "bolts", "nut", "nuts", "screw", "screws", "rawlplug", "rawlplugs", "anchor",
    "anchors", "rivet", "rivets", "dowel", "dowels", "valve", "valves",
    "radiator", "radiators", "banjo"))
_THE_MACHINE_ITSELF = frozenset(("washing machine", "washer dryer", "tumble dryer", "dryer",
                                 "drum", "laundry", "clothes"))


_A_WASHER_ALREADY_CHANGED = re.compile(
    r"\b(?:changed|change|replaced|replacing|swapped|swapping|new)\b[^.?!]{0,20}\bwasher\b"
    r"|\bwasher\b[^.?!]{0,20}\b(?:changed|replaced|swapped|done)\b", re.I)
_THE_NEXT_TAP_STEP = (
    "Then it is the seat rather than the washer. Take the head off again and look at the brass "
    "ring the washer presses on: if it is pitted or scored it can be re-ground with a seat tool, "
    "and if the tap turns a quarter turn it has a ceramic cartridge instead, which is replaced "
    "whole and matched by the maker's name stamped on the tap. A cartridge is a ten-minute swap "
    "and stops it for good; until then, turn the water off at the isolating valve when you leave "
    "the house.")
_THE_DRIPPING_TAP = (
    "A dripping tap is nearly always a worn washer or cartridge: turn the water off at the "
    "isolating valve under the sink, take the handle off, and take the old part to a hardware "
    "shop to match it. It's a 20-minute job and saves a lot of water.")


def _a_dripping_tap(memory, understood):
    said = str((understood or {}).get("clean") or (understood or {}).get("text") or "")
    if _A_WASHER_ALREADY_CHANGED.search(said):
        return _THE_NEXT_TAP_STEP
    return _THE_DRIPPING_TAP


def _not_a_washer_of_another_kind(understood):
    words = set((understood or {}).get("words") or ())
    if not (_A_WASHER & words):
        return True
    if _THE_MACHINE_ITSELF & words:
        return True
    return not (_ANOTHER_KIND_OF_WASHER & words)


_A_WASHER_DONE = re.compile(
    r"\b(?:already|changed|changing|replaced|replacing|swapped|swapping|fitted|fitting|"
    r"sorted|done|did|tried|trying)\b", re.I)


def _a_washer_with_no_other_subject(understood):
    words = set((understood or {}).get("words") or ())
    if not (_A_WASHER & words):
        return False
    if _THE_MACHINE_ITSELF & words or _ANOTHER_KIND_OF_WASHER & words:
        return False
    said = str((understood or {}).get("clean") or (understood or {}).get("text") or "")
    return not _A_WASHER_DONE.search(said)


_WASHER_TWO_THINGS = (
    "Two things in a house are called a washer. The ring inside a tap costs pennies: turn the "
    "water off at the isolating valve, take the tap apart and take the old ring to a hardware "
    "shop to match - half an inch fits most taps, three quarters the older big bath taps. If it "
    "is the machine, the fix depends on what it is doing: water on the floor is usually the door "
    "seal or a hose, clothes that come out wet is the spin, and no heat is the element. All three "
    "are cheap parts, so a machine with a sound drum is worth repairing rather than replacing.")
_THE_TAP_WASHER = (
    "Good - then you have what you need. Turn the water off at the isolating valve under the sink "
    "or the small screw on the pipe, take the handle off and unscrew the head, then pick the old "
    "washer out with a small screwdriver. Match it at a hardware shop: half an inch fits most "
    "taps, three quarters the older big bath taps. A smear of silicone grease on the new one and "
    "it goes back the same way, and the spanner is for the big nut under the handle.")
_A_TAP_TALK = re.compile(r"\b(?:tap|taps|faucet|dripping|drip|drips|spout|cistern)\b", re.I)


def _the_chat_is_about_a_tap(memory, understood):
    turns = (memory or {}).get("turns") if isinstance(memory, dict) else None
    if not isinstance(turns, list):
        return False
    said_now = str((understood or {}).get("text") or (understood or {}).get("clean") or "")
    said_now = said_now.strip().lower()
    seen = 0
    for turn in reversed(turns):
        if not isinstance(turn, dict):
            continue
        text = str(turn.get("user") or "").strip().lower()
        if not text or text == said_now:
            continue
        if _THE_MACHINE_ITSELF & set(text.split()):
            return False
        if _A_TAP_TALK.search(text):
            return True
        seen += 1
        if seen >= 2:
            break
    return False


def _a_washer_two_things(memory, understood):
    if _the_chat_is_about_a_tap(memory, understood):
        return _THE_TAP_WASHER
    return _WASHER_TWO_THINGS


def _the_leak_is_a_machines(understood):
    return _it_is_water_leaving(understood) and _not_a_washer_of_another_kind(understood)


def _a_machine_that_will_not_empty(understood):
    text = " ".join(str(one) for one in ((understood or {}).get("words") or ())).lower()
    if not text:
        text = str((understood or {}).get("clean") or (understood or {}).get("text") or "").lower()
    return bool(_WILL_NOT_EMPTY.search(text))


def _the_bed_for_paving_or_blocks(memory, reading):
    line = (reading.get("clean") or reading.get("text") or "").lower()
    words = set(reading.get("words") or ())
    if words & {"block", "blocks", "setts", "pavers"} or any(
            phrase in line for phrase in ("block paving", "block paved", "block paver",
                                          "block paving drive", "paved drive",
                                          "paving the drive")):
        return ("Blocks are not bedded on a sand-and-cement mix: they go down on 30 to 40mm "
                "of sharp sand alone, compacted with a wacker plate, and the joints are "
                "brushed full of kiln-dried sand afterwards - so there is no cement to "
                "measure. For 20 square metres reckon on about one tonne of sharp sand for "
                "the bed and two or three 25kg bags of kiln-dried sand for the joints, plus "
                "an edge restraint on any open side, which is what stops the blocks "
                "spreading.")
    return ("Patio slabs go on a full bed of 5:1 sharp sand and cement, 30 to 40mm thick, "
            "never on five dabs: a 25kg bag of cement with five 25kg bags of sharp sand "
            "beds about 2 to 2.5 square metres, so a 20 square metre patio wants nine or "
            "ten bags of cement and two bulk bags of sand. The mix should be crumbly-damp "
            "- squeeze a ball and no water runs - and the joints are pointed afterwards "
            "with a 4:1 mix, not the bed mix.")
_LOOSE_STOOL = re.compile(
    r"\b(?:stools|poos?|faeces|feces|bowels?)\b[^.?!]{0,24}?"
    r"\b(?:loose|runny|watery|soft|sloppy)\b"
    r"|\b(?:loose|runny|watery|sloppy)\s+(?:stools|poos?|faeces|feces)\b", re.I)
_FURNITURE_WORDS = re.compile(
    r"\b(?:chair|chairs|table|tables|bench|benches|desk|desks|leg|legs|glue|screw|screws|"
    r"tighten|joint|joints|wood|wooden|seat|furniture|varnish|paint|repair|fix|wobbl\w*|"
    r"rock\w*|rickety)\b", re.I)


def _a_chair_and_not_a_body(understood):
    from .body import the_stomach_is_what_it_is_about

    understood = understood if isinstance(understood, dict) else {}
    if the_stomach_is_what_it_is_about(understood):
        return False
    text = str(understood.get("clean") or understood.get("text") or "").lower()
    if _LOOSE_STOOL.search(text) and not _FURNITURE_WORDS.search(text):
        return False
    return True


def _the_fan_stopped(memory, understood):
    text = str((understood or {}).get("clean") or (understood or {}).get("text") or "").lower()
    if re.search(r"\b(?:fan|fans|blade|blades)\b", text):
        return ("A fan that rocks is usually the base or a bent blade: tighten the nut under the "
                "base, then take the blade off and sight along it, because one blade out of line "
                "is the whole wobble and a new blade is a few pounds. Stand it on a hard, level "
                "floor rather than a rug, and wind out the feet if it has them.")
    return ("A wobble is a loose base or an uneven floor rather than a fault: wind the feet out "
            "until it sits flat on all of them, tighten what holds the base to the body, and take "
            "it off a rug or a soft board, which is what most of them are standing on. If it is "
            "still rocking it wants shimming on one corner.")


_PACKING_VERB = frozenset((
    "pack", "packs", "packing", "packed", "box", "boxes", "boxed", "boxing", "packup"))


def _the_kitchen_stuff_is_a_take_up(understood):
    reading = understood or {}
    said = str(reading.get("clean") or reading.get("text") or "").lower()
    if set(re.findall(r"[a-z]+", said)) & _PACKING_VERB:
        return True
    return bool(reading.get("followup"))


_HEAT_PUMP_USE = ("dryer", "drier", "tumble dryer", "tumble drier", "dehumidifier", "radiator",
                  "radiators", "hot water tank", "cylinder", "shower", "pool", "swimming pool",
                  "air conditioning", "hot tub", "underfloor", "boiler")
_HEAT_PUMP_ASK = ("fix", "fixing", "repair", "repairing", "not working", "broken", "fault",
                  "faulty", "any good", "worth", "worth it", "cost", "costs", "price", "cheap",
                  "cheaper", "run", "running", "buy", "buying", "recommend", "noise", "noisy",
                  "loud", "install", "installed", "installation", "smell", "smells",
                  "efficient", "good")


def _the_explainer_keeps_the_explainer(understood):
    text = " " + (understood.get("clean") or understood.get("text") or "").lower() + " "
    if not any(word in text for word in _HEAT_PUMP_USE):
        return True
    return not any(word in text for word in _HEAT_PUMP_ASK)


def _hair_dryer(memory, reading):
    words = set(str(one).lower() for one in (reading.get("words") or ()))
    dead = {"dead", "stopped", "stop", "wont", "won't", "wont.", "turn", "turns", "start",
            "starts", "switch", "switches", "power", "fuse", "buzzing", "buzzes", "nothing"}
    if words & dead:
        return ("A hair dryer that is completely dead is nearly always the plug or the flex, not "
                "the element: try another socket, check the fuse in the plug, and look at the "
                "point where the flex meets the handle, because a cable that is wound up every "
                "day is what breaks. If a fresh fuse blows again, stop using it - that is a short "
                "in the element, and a new dryer is cheaper than the repair.")
    return ("Check the air intake first: a hair dryer that blows cold usually has the grille at "
            "the back furred up with hair and fluff, and the thermal cut-out trips before the "
            "element ever fails. Unplug it, pull the hair off the grille and out of the vent, let "
            "it cool for ten minutes and try it again on the high setting. If it still runs cold "
            "it is the element or the cut-out, and on a cheap dryer that is a new one rather than "
            "a repair - do not open the case, the element is a live part.")


def _to_a_figure(value):
    return round(float(value), 1)


def _counted(value, unit):
    return "%g %s" % (value, unit if _to_a_figure(value) == 1 else unit + "s")


PAINT_WITH_NO_SIZE = (
    "One litre of emulsion covers about 10 to 12 square metres, and you need two coats, so "
    "count the wall area and double it: add the walls up as perimeter times ceiling height "
    "(a 4m by 4m room with 2.4m ceilings is about 38 square metres), take off roughly 1.7 "
    "square metres for a door and 1.2 for a window, and that room wants about 7 litres - two "
    "5 litre tins, or a 10 to leave some for touching up. Ceilings and a second colour are "
    "extra, and a dark colour over a light wall often takes three coats.")


def _paint_for_the_room(memory, understood):
    from .home import _wall_area
    area, ceiling, what = _wall_area(understood, memory)
    if not area:
        return PAINT_WITH_NO_SIZE
    litres = max(1.0, int(area * 2 / 11.0 * 2 + 0.999) / 2.0)
    area = _to_a_figure(area)
    coats = "%g" % _to_a_figure(area * 2)
    if what == "ceiling":
        count = ("A ceiling that size is %s, two coats makes %s, and a litre of "
                 "emulsion covers 10 to 12." % (_counted(area, "square metre"), coats))
    elif ceiling is None:
        count = ("That's %s, two coats makes %s, and a litre of emulsion "
                 "covers 10 to 12." % (_counted(area, "square metre"), coats))
    else:
        count = ("A room that size is %s round and %s to the ceiling, so about %s of wall, and "
                 "two coats makes %s."
                 % (_counted(_to_a_figure(area / ceiling), "metre"), _counted(ceiling, "metre"),
                    _counted(area, "square metre"), coats))
    if what == "ceiling":
        tail = ("Give the walls their own sum, and go a coat further when a white ceiling is "
                "going over a colour rather than over white.")
    elif ceiling is None:
        tail = ("Allow a third coat when a dark colour goes over a light one, and give the ceiling "
                "and any second colour their own sum.")
    else:
        tail = ("Take off roughly 1.7 square metres for a door and 1.2 for a window if they are in "
                "it, allow a third coat when a dark colour goes over a light one, and give the "
                "ceiling and any second colour their own sum.")
    return "About %s: %s %s" % (_counted(litres, "litre"), count, tail)


WALLPAPER_WITH_NO_SIZE = (
    "Count drops, not floor: divide the room's perimeter by the 52cm width of a standard roll and "
    "round up (a 4m by 4m room is 16m round, so 31 drops), then divide a roll's 10m by the ceiling "
    "height plus the pattern repeat to see how many drops each gives - usually three - and 31 drops "
    "is about 11 rolls. Buy one extra for a mistake and matching, and keep the batch number the "
    "same on every roll.")


def _wallpaper_for_the_room(memory, understood):
    from .home import _wall_area, _wall_width_and_height
    area, ceiling, what = _wall_area(understood, memory)
    if not area:
        return WALLPAPER_WITH_NO_SIZE
    if what == "wall":
        width, height = _wall_width_and_height(understood, memory)
        if not width or not height:
            return WALLPAPER_WITH_NO_SIZE
        across = int(-(-width / 0.52 // 1))
        plain = max(1, int(10 // height))
        patterned = max(1, int(10 // (height + 0.3)))
        plain_rolls = int(-(-across / plain // 1))
        patterned_rolls = int(-(-across / patterned // 1))
        return ("About %s: a wall %s wide and %s high takes %s at the 52cm width of a standard "
                "roll, and a 10m roll gives %s of a plain paper or %s of one with a big repeat - "
                "so %s plain and %s patterned. Buy one extra for a mistake and matching, and keep "
                "the same batch number on every roll."
                % (_counted(plain_rolls, "roll"), _counted(_to_a_figure(width), "metre"),
                   _counted(_to_a_figure(height), "metre"), _counted(across, "drop"),
                   _counted(plain, "drop"), _counted(patterned, "drop"),
                   _counted(plain_rolls, "roll"), _counted(patterned_rolls, "roll")))
    if what != "room" or not ceiling:
        return WALLPAPER_WITH_NO_SIZE
    round_the_room = area / ceiling
    drops = int(-(-round_the_room / 0.52 // 1))
    plain = max(1, int(10 // ceiling))
    patterned = max(1, int(10 // (ceiling + 0.3)))
    rolls_plain = int(-(-drops / plain // 1))
    rolls_patterned = int(-(-drops / patterned // 1))
    return ("About %d rolls: a room that size is %g metres round and %g metres to the ceiling, so "
            "%d drops at the 52cm width of a standard roll, and a 10m roll gives %d drops of a "
            "plain paper or %d of one with a big repeat - so %d rolls plain and %d patterned. Buy "
            "one extra for a mistake and matching, and keep the same batch number on every roll."
            % (rolls_plain, round_the_room, ceiling, drops, plain, patterned,
               rolls_plain, rolls_patterned))


_A_NAIL_COMES_OUT = ("remove", "removing", "removed", "out", "puller", "pincers", "pull",
                     "pulling", "pulled", "old", "stuck", "left", "loose", "snapped", "broke",
                     "broken", "half")


def _a_nail_in_the_wall(memory, reading):
    words = set(str(one).lower() for one in (reading.get("words") or ()))
    if words & set(_A_NAIL_COMES_OUT):
        return ("Grip the head with pincers and slide a scrap of wood under them so the plaster "
                "does not crush, then ease it out with a slight twist rather than levering "
                "against the wall. A nail that turns but will not come has lost its grip: punch "
                "it below the surface with another nail, fill the dent with filler, sand it flat "
                "and touch up the paint.")
    return ("Tap it in at a slight downward angle so the weight hangs on the wall instead of "
            "pulling the head out, and put it into something solid - a stud, found by tapping, "
            "or brick under the plaster. On plasterboard with nothing behind it a bare nail or "
            "a picture hook pulls out: use a plasterboard plug or a self-drilling fixing, and "
            "keep the load light.")


_A_SIZE_ASK = ("size", "sizes", "what size", "which size", "what length", "how long", "how big", "how thick", "which nail",
               "what nail", "what nails", "how many mm", "mm", "gauge", "best nail", "should i use")
_A_SPLIT_ASK = ("split", "splits", "splitting", "crack", "cracks", "cracking", "splinter",
                "splinters", "splintering", "snapped")


def _the_wood_and_the_nail(memory, reading):
    words = set(str(one).lower() for one in (reading.get("words") or ()))
    said = " " + " ".join(str(one).lower() for one in (reading.get("words") or ())) + " "
    if (any(ask in said for ask in _A_SIZE_ASK)) and not (words & set(_A_SPLIT_ASK)):
        return ("Size the nail to the job, not to the room: 40mm to 50mm lost-head or oval nails "
                "for skirting and architrave, 50mm to 65mm for a floorboard, 30mm for a 6mm "
                "batten, and thin panel pins for beading and a back panel. As a rule the nail "
                "wants to be about two and a half times as long as the piece it is holding, and "
                "the top third of it has to bite into something solid behind.")
    return ("Drill a pilot hole first, about three quarters as wide as the nail, and keep it at "
            "least 25mm in from the end of the board, because that is where a split starts. "
            "Blunt the point by tapping it once on a hard surface so it cuts the grain instead "
            "of wedging it apart, and clamp a scrap of wood behind the far face when the board "
            "is thin. A split that has already opened wants wood glue worked into it and a "
            "clamp overnight, not another nail.")


_A_CHILD_IN_A_MOVE = re.compile(
    r"\b(?:kid|kids|child|children|son|sons|daughter|daughters|teenager|teenagers|teen|teens|"
    r"toddler|toddlers|baby|babies|boy|boys|girl|girls|schoolchild|schoolchildren|"
    r"stepson|stepdaughter|stepchildren|little one|little ones|the youngest|the eldest)\b")

_A_TELLING_THE_LINE_ASKS_FOR = re.compile(
    r"\b(?:tell|tells|telling|told|explain|explains|explaining|explained|break the news|"
    r"let them know|lets them know|prepare them|preparing them|reassure|reassuring)\b")


def _a_child_or_a_telling(understood):
    said = understood if isinstance(understood, dict) else {}
    text = " ".join(str(said.get("norm_text") or said.get("plain") or said.get("text") or "")
                    .lower().split())
    return bool(_A_CHILD_IN_A_MOVE.search(text) or _A_TELLING_THE_LINE_ASKS_FOR.search(text))
_DRY_IT_INDOORS = (
    "inside", "indoors", "indoor", "in the house", "in the flat", "bathroom", "radiator",
    "airer", "rack", "maiden", "tumble dryer", "tumble drier", "tumbledryer", "dryer",
    "drier", "dehumidifier", "no garden", "no line", "nowhere to hang", "condensation",
)
_DRYING_WORD = re.compile(r"\bdry(?:ing|s|er|d)?\b|\bhang(?:ing)?\b|\bwashing\b|\blaundry\b",
                          re.I)
_THE_WEATHER = re.compile(
    r"\b(?:rain|rains|raining|rainy|showers?|forecast|wind|winds|windy|sun|sunny|sunshine|"
    r"weather|frost|frosty|drizzle|damp|fog|line|outside|out there|today|tomorrow|dry out)\b",
    re.I)


_A_LOAD_NAMED = re.compile(
    r"\b(?:washing|laundry|clothes|clothing|load|jeans|trousers|shirts|sheets|bedding|"
    r"towels?|duvets?|jumpers?|coats?|jackets?|wool|knitwear|uniform|school uniform)\b", re.I)
_A_ROOM = re.compile(
    r"\b(?:room|rooms|bedroom|kitchen|bathroom|cellar|loft|hallway|hall|utility|"
    r"flat|house|home|studio|caravan)\b", re.I)
_WEATHER_NOT_A_ROOM = re.compile(
    r"\b(?:rain|rains|raining|rainy|showers?|forecast|wind|winds|windy|sun|sunny|sunshine|"
    r"weather|frost|frosty|drizzle|fog|line|outside|out there|today|tomorrow)\b", re.I)


def _not_a_drying_inside_question(understood):
    text = " " + str(understood.get("clean") or understood.get("text") or "").lower() + " "
    if not _DRYING_WORD.search(text):
        return True
    if _A_LOAD_NAMED.search(text) and _A_ROOM.search(text):
        return bool(_WEATHER_NOT_A_ROOM.search(text))
    if not any(word in text for word in _DRY_IT_INDOORS):
        return True
    return bool(_THE_WEATHER.search(text))


def entries():
    from .home import not_a_sound
    from .home import (
    APPLIANCE_DOOR_WORDS, BODY_WORDS, COST_WORDS, EXTRACTOR_GREASE_FILTER, FIRST_NIGHT_BOX,
    FITTING_SHARED_STANDDOWN, JOB_GUARD, LANDLORD_JOB_FITTINGS, LANDLORD_REPAIR_LETTER,
    LETTING, LIFE_ASK, LIFE_GUARD, LIFE_NAMES, MACHINE_BURNING, MACHINE_DEAD, MACHINE_LEAKING,
    MACHINE_SOUNDS, NOISE_WORDS, NORMAL_CUTOUT, NOT_A_FENCE_JOB, NOT_A_TRADE_WORDS, RUNNING_WORDS,
    TAKES_THINGS, THING_PARTS, TUMBLE_DRYER_FILTER, WASHING_MACHINE_FILTER, _BATH_CITY,
    _DIY_AVOID, _SMOKING_THING, _TAKING_PAINT_OFF, _a_dryer_is_not_a_washer, _a_fence_is_named,
    _not_a_size_of_a_home, _a_machine_consumable,
    _a_mark_that_is_live, _a_room_being_heated, _a_safety_ask, _a_thing_owns_the_part,
    _alarm_nuisance,
    _appliance_cutting_out, _appliance_noise, _asks_the_ceiling_colour, _bath_length,
    _boiler_noise, _the_boiler_is_not_the_fault, _a_visit_not_a_purchase, _broken_window, _chemical_safety, _colour_advice, _consumer_unit, _diy,
    _door_lock_stiff, _dryer_heat, _fitting_repair, _furniture_upstairs, _going_to_the_loo,
    _heating_goes_cold, _heat_pump_answer, _a_person_not_a_hob, _hob_heat, _iron_fault, _kettle_will_not_stop,
    _lifespan, _lost_keys, _machine_fault,
    _machine_takes, _mould, _not_a_cook_ask, _not_a_machine_that_has_gone, _paint_brush_care,
    _pipes, _place_smell,
    _the_black_is_not_a_body,
    _pressure_weak, _radiator_not_hot, _repair_judgement, _roof_leak, _running,
    _small_appliance_not_heating, _smoking_appliance, _soft_smell, _the_paper_is_in_the_line,
    _washer_price, _washer_sound_fault, _water_off, _where_the_consumable_goes, entry,
    the_fault, the_filter_of,
    the_stomach_is_what_it_is_about, the_trade_to_call,
    )
    from .lookup import not_the_heat_of_an_argument
    from .lookup import RING_AS_A_CALL, a_sanding_job, asks_where

    THE_APPLIANCE_ITSELF = (
        "my fridge", "the fridge", "our fridge", "fridge is", "fridge not", "fridge too",
        "fridge door", "fridge keeps", "in the fridge", "fridge cold",
        "my freezer", "the freezer", "our freezer", "freezer is", "freezer not", "freezer cold",
        "in the freezer", "freezer door",
        "my oven", "the oven", "our oven", "oven is", "oven not", "oven too", "oven on",
        "in the oven", "oven door", "fan oven", "oven cold",
    )

    return [
        entry(
            "stair-gate",
        (("stair gate", "stair gates", "stairgate", "stairgates", "baby gate", "baby gates",
          "safety gate", "safety gates", "child gate", "child gates", "pressure gate"),
         ("fit", "fits", "fitting", "fitted", "install", "installing", "put up", "putting up",
          "fix", "fixing", "mount", "mounting", "buy", "need", "which", "best", "top", "bottom",
          "stairs", "staircase", "newel", "banister", "bannister", "wall", "doorway", "toddler",
          "baby", "measure", "measuring", "remove", "take down")),
        "At the top of the stairs use a screw-fixed gate, never a pressure-fit one: a pressure gate "
        "grips between two surfaces and a determined toddler can push it out of the opening, and the "
        "top of the stairs is the one place that matters. A pressure gate is fine in a doorway or at "
        "the bottom of the stairs, where it needs no drilling, but check it by hand every week or so "
        "as the pads work loose. Measure the opening at its widest and buy a gate whose stated range "
        "covers it, and add a banister or newel-post adaptor, or an extension, when one side is a "
        "post rather than a flat wall. Look for a gate to BS EN 1930, at least 73cm high, with a door "
        "that swings away from the stairs, and no bottom bar across a step because it is a trip.",
        ask=("how", "what", "which", "do i need", "should i", "best", "fit", "install", "buy"),
        avoid=("dog", "dogs", "puppy", "cat", "cats", "pet", "pets", "rabbit", "chicken",
               "chickens", "hens", "goat", "garden", "driveway", "field", "fence", "gate post",
               "gatepost", "wooden gate", "front gate", "back gate", "side gate", "airport",
               "departure", "boarding", "flight", "concierge", "number", "digits", "decimal"),
        bias=2),

        entry("a-trade-is-not-tipped",
              (("tip", "tips", "tipping", "tipped", "gratuity"),
               ("plumber", "electrician", "builder", "decorator", "joiner", "carpenter", "plasterer",
                "tiler", "mechanic", "fitter", "engineer", "gas engineer", "boiler man", "handyman",
                "roofer", "scaffolder", "tradesman", "workman")),
              "No: a plumber, an electrician or a builder quotes a price for the job, and that price "
              "is the whole of it. A tip is not expected and can read as odd, so the thing worth "
              "doing instead is offering a tea and paying on time.",
              avoid=("how much does", "how much is", "cost", "costs", "charge", "charges",
                     "quote", "hourly", "day rate"),
              bias=4),

        entry("who-to-call",
              (("who", "who to", "which engineer", "which tradesman", "what kind of engineer",
                "anyone i can call", "someone to call",
                "who do i call", "who should i call", "who do i ring", "who should i ring",
                "who do i get"),
               ("call", "ring", "get", "get in", "tradesman", "engineer", "come out", "phone",
                "fix")),
              the_trade_to_call,
              avoid=NOT_A_TRADE_WORDS),

        entry("lighting-a-fire",
              (("wood burner", "woodburner", "wood burning stove", "woodburning stove",
                "log burner", "logburner", "log fire", "open fire", "wood stove", "wood fire",
                "multifuel stove", "multi fuel stove", "fireplace", "woodburner stove",
                "coal fire", "stove"),
               ("light", "lighting", "lit", "start", "starting", "kindle", "kindling",
                "get it going", "get going", "get the fire going", "fire going", "light the fire",
                "start the fire", "going out", "goes out", "gone out", "keeps going out",
                "wont light", "won't light", "wont stay in", "smokes", "smoking", "smoulders",
                "damper", "air control", "vent", "going", "get it lit", "burner going",
                "stove going", "fire lit",
                "lay a fire", "lay the fire", "lay it")),
              "Open the air control fully, clear the grate but leave an inch of ash, and lay eight or "
              "ten sticks of kindling in a loose criss-cross with a firelighter or a twist of "
              "newspaper in the middle. Light it low down and leave the door on the latch rather than "
              "shut, so air can get in, and wait until the kindling is properly caught before you add "
              "one or two split logs - a big log laid on a small flame is how a fire goes out. Once "
              "the fire is going and the glass has cleared, shut the door and close the air down to "
              "about a finger's width; that is what stops it burning through a load in an hour. If it "
              "smokes into the room on a cold day the flue is cold, so hold a lit twist of newspaper "
              "up near the throat of the stove for a minute first. Dry wood and a swept flue are the "
              "two things that keep it easy: fit a carbon monoxide alarm in the same room, have the "
              "chimney swept once a year, and never use petrol, meths or barbecue fluid to start it, "
              "because a sooted flue is what turns a stove into a chimney fire.",
              bias=1,
              avoid=("sweep", "sweeps", "sweeping", "swept", "chimney sweep", "flue liner",
                     "install", "installation", "fitter", "buy", "best one", "which one", "cost",
                     "price", "cheap", "worth it", "how much", "how many", "broken", "not working",
                     "wont work", "no heat",
                     "smoke alarm", "carbon monoxide", "alarm going off", "chimney fire",
                     "caught fire", "on fire", "bonfire", "fire pit", "garden fire", "barbecue",
                     "bbq", "grill", "charcoal", "smoker", "pizza oven", "candle", "hob", "pilot",
                     "boiler", "oven",
                     "gas", "gas stove", "gas fire", "gas fireplace", "gas hob", "ignition",
                     "clicking", "spark", "electric", "electric fire",
                     "outdoor", "allotment", "campfire", "stove top", "cook on", "cooking",
                     "glass", "paint", "rust", "door seal", "rope seal", "replace the")),

        entry("bleach-on-mould", (("bleach", "bleach solution", "thin bleach", "milton",
                                   "mould spray", "vinegar"),
                                  ("mould", "mold", "mildew", "kill", "kills", "killing", "dying")),
              "Yes: vinegar is the gentler of the two and bleach at about one part to four of water is "
              "the stronger, and either kills the mould it reaches on tiles, grout, glass and the "
              "sealant round a bath - gloves on, window open, never mixed with another cleaner. On "
              "plaster, paint, wood or fabric neither does more than lift the colour, because it "
              "cannot get at mould that has grown in, so those want a mould spray, or the sealant cut "
              "out and replaced. And it is the damp that brings it back, so that is the part to fix.",
              avoid=("stain", "stains", "my whites", "the whites", "in with the whites",
                     "white wash", "colors", "colours",
                     "towels", "washing machine", "in the wash",
                     "drain", "sink", "bin", "bread", "cheese", "food", "jam", "the fridge",
                     "nail", "toe", "finger",
                     "ceiling", "ceilings", "wall", "walls", "wardrobe", "skirting",
                     "behind the", "under the window")),
        entry("mould-bathroom", (("mould", "mold", "mildew", "mouldy", "moldy",
                                  "black mould", "black mold", "black spots", "black patch",
                                  "black patches", "black marks", "black staining", "black on the",
                                  "gone black", "going black", "turned black", "turning black",
                                  "black in the corner", "black behind the", "black round the",
                                  "black around the",
                                  "going mouldy", "going moldy", "gone mouldy", "gone moldy",
                                  "gets mouldy", "gets moldy", "getting mouldy", "getting moldy",
                                  "keeps going mouldy", "keeps getting mouldy", "mouldy again",
                                  "moldy again"),
                                 ("bathroom", "ceiling", "ceilings", "wall", "walls", "wallpaper",
                                  "remove", "get rid", "stop", "shower", "showers", "shower cubicle",
                                  "sealant", "silicone", "grouting", "tile", "tiles", "window",
                                  "windows", "window frame", "frame", "windowsill", "corner",
                                  "corners", "bedroom", "bedrooms", "kitchen", "hall", "hallway",
                                  "loft", "attic", "cupboard", "wardrobe", "skirting", "paint",
                                  "dangerous", "harmful", "unhealthy", "bad for", "smell", "smells",
                                  "smelly", "damp", "flat", "house", "home", "room", "rooms",
                                  "keeps coming back", "keep coming back", "comes back",
                                  "coming back", "keeps returning", "keeps coming",
                                  "screen", "screens", "monitor", "monitors", "laptop", "laptops",
                                  "phone", "phones", "handset", "keyboard", "keyboards", "headset",
                                  "headsets", "headphones", "earbuds", "earphones", "airpods",
                                  "gasket", "gaskets", "door seal",
                                  "returns", "returning", "again", "spreading", "spread",
                                  "getting worse", "getting bigger", "keeps growing",
                                  "black",
                                  "behind", "behind the", "above the", "under the", "underneath",
                                  "under it", "next to", "beside", "around the", "along the",
                                  "behind it", "above it",
                                  "do about the mould", "do about mould", "deal with the mould",
                                  "deal with mould", "about the mould", "about mould",
                                  "with the mould", "of the mould", "the mould problem",
                                  "handle mould", "sort out mould", "the mould keeps")),
              _mould,
              guard=_the_black_is_not_a_body,
              avoid=("bread", "food", "cheese", "jam", "fruit", "veg", "vegetables", "milk", "meat",
                     "leftovers", "the fridge", "a fridge",
                     "nail", "nails", "finger", "thumb", "toe", "banged", "slammed", "bruised",
                     "dropped", "knocked", "hit it",
                     "avocado", "avocados", "guacamole", "apple", "apples", "banana", "bananas",
                     "pear", "pears", "potato", "potatoes", "aubergine", "aubergines",
                     "went black", "went dark", "vision", "sight",
                     "tomato", "tomatoes", "tomato plant", "rose", "roses", "plant", "plants",
                     "leaves", "leaf", "blossom end", "courgette", "courgettes", "cucumber",
                     "cucumbers", "seedling", "seedlings", "cutting", "cuttings", "greenhouse",
                     "charger", "charging", "windows update", "reboot", "battery",
                     "grout", "grouting",
                     "landlord wont", "landlord won't", "landlords wont", "landlords won't",
                     "landlord refuses", "landlord refused", "landlord is refusing",
                     "landlord ignores", "landlord is ignoring", "landlord not fixing",
                     "landlord hasnt fixed", "landlord hasn't fixed", "landlord does nothing",
                     "letting agent wont", "letting agent won't", "letting agent ignores",
                     "withhold rent", "withholding rent", "rent arrears", "tenancy", "deposit",
                     "housing officer",
                     "the law", "law say", "law says", "legal", "legally", "am i allowed",
                     "is it legal", "obliged", "duty to")),
        entry("damp-or-condensation",
              (("damp", "damp patch", "damp wall", "damp walls", "rising damp"),
               ("condensation", "or condensation", "condensation or", "difference between",
                "which one", "what kind")),
              "Condensation is water out of the air landing on a cold surface: the windows and the outer "
              "corners are wet in the morning, it clears when the room is aired, and it comes back on "
              "cold days. A leak is a patch that grows and stays wet whatever the weather, and rising "
              "damp only runs along the bottom metre of a wall, usually with a tide mark. To tell them "
              "apart, dry a patch with a hairdryer, tape a square of cling film over it tight and leave "
              "it three days: water on the room side of the film is condensation, a wall still wet "
              "behind it is water coming through.",
              avoid=("cloth", "cloths", "dishcloth", "washing", "laundry", "clothes", "towel",
                     "towels", "cake", "bread", "tent", "shed")),
        entry("condensation", (("condensation", "damp", "walls are wet", "wet walls", "walls get wet",
                                "windows are wet", "wet windows",
                                "wet in the morning", "wet every morning", "wet each morning",
                                "wet in the mornings",
                                "steaming up", "steamed up", "steamy", "condensating", "condensing",
                                "misting up", "misted up", "wet inside", "running with water",
                                "fogging up", "fogged up", "fog up", "fogs up",
                                "foggy windows", "windows fog", "window fog",
                                "frost on the windows", "frost on my windows", "frost on windows",
                                "frost on the inside", "frost inside", "frosty windows",
                                "frosted up", "windows are frosted", "windows frosted",
                                "ice on the inside", "ice on the windows", "ice inside the windows",
                                "ice on my windows"),
                               ("window", "windows", "walls", "wall", "bedroom", "stop", "inside",
                                "wet", "winter", "misty", "glass", "running down",
                                "loft", "attic", "garage", "shed", "landing", "hall",
                                "hallway", "basement")),
              "Condensation comes from warm wet air hitting cold surfaces, so ventilate and keep the "
              "place a bit warmer: use the extractor fan, open a window for 10 minutes a day, dry "
              "clothes outside or in a vented dryer, and leave the heating on low rather than off and "
              "on. A dehumidifier helps in a bedroom that gets it badly.",
              avoid=("glasses", "spectacles", "goggles", "car", "cars", "van", "windscreen",
                     "motorbike", "helmet", "pot", "pan", "saucepan", "kettle", "cooker",
                     "mirror", "mirrors",
                     "spreading up", "spreading across", "up the wall", "up the walls",
                     "double glazing", "double glazed", "double-glazed", "window pane",
                     "panes", "the pane", "between the panes", "sealed unit")),
        entry("misted-double-glazing",
              (("misted", "misting", "misty", "mist", "misted up", "fogged up inside",
                "fogging up inside", "fogged up between", "fogging between",
                "condensation between", "cloudy", "gone cloudy", "hazy", "blown", "seal has failed",
                "seal failed", "seals have failed", "water between the panes", "wet between",
                "inside the glass", "inside the pane", "inside the panes"),
               ("double glazing", "double glazed", "double-glazed", "glazing", "window pane",
                "window panes", "the pane", "panes", "unit", "units", "window", "windows",
                "conservatory", "door", "doors", "sealed unit")),
              ("That is a failed seal, not condensation: the unit has taken in damp and the "
               "desiccant inside it is full, so no amount of ventilating, heating or a dehumidifier "
               "will clear it. The glass unit is replaced, not repaired - a glazier measures the unit "
               "and swaps it, and the frame and the handles stay, which is why it is a much smaller "
               "job than new windows, usually £80-£200 a pane fitted depending on size and glass. "
               "Some firms now drill and dry a misted unit in place for less; it works on a mild "
               "case, but a unit that has been cloudy for years is a swap. If the mist is on the room "
               "side of the glass and wipes off, that is ordinary condensation and the ventilating "
               "answer is the right one - check with a dry cloth first."),
              avoid=("spectacles", "goggles", "windscreen", "car", "cars", "van",
                     "motorbike", "helmet", "mirror", "mirrors", "kettle", "saucepan",
                     "steam", "shower", "bathroom",
                     "cook", "cooking", "cooked", "kitchen", "boiling", "boil", "pan", "pans",
                     "casserole", "oven", "washing", "drying clothes",
                     "stop", "stops", "stopping", "prevent", "preventing", "wipe", "wipes",
                     "wiping", "morning", "mornings", "every morning", "always", "every day",
                     "every night", "each morning",
                     "single glazed", "single glazing", "skylight", "velux"),
              bias=1),
        entry("damp",
              (("damp", "damp patch", "damp patches", "damp wall", "damp walls", "damp corner",
                "damp in", "damp problem", "rising damp", "damp proof", "damp course"),
               ("deal", "get rid", "stop", "cure", "fix", "treat", "sort", "coming back", "keeps",
                "why", "how", "cause", "room", "house", "flat", "hallway", "corner", "wall",
                "have", "got", "real", "signs", "sign", "what", "mean", "means", "look", "looks",
                "like", "serious", "worry", "worried",
                "rising damp",
                "getting worse", "getting bigger", "bigger", "growing", "spreading", "spread",
                "keeps coming back", "coming back", "returns", "returning")),
              "Find the water before you treat the wall: a leaking gutter or downpipe, an overflow "
              "running, ground above the damp course, or a slow leak near the patch. Feel whether the "
              "wall is wet high up (a leak) or only at the bottom (rising damp). Warm it and ventilate "
              "it while you look, don't paint over it, and in a rented flat ask the landlord in "
              "writing.",
              avoid=("cloth", "cloths", "dishcloth", "washing", "laundry", "clothes", "towel",
                     "towels", "cake", "bread", "tent", "shed",
                     "condensation", "winter", "window", "windows", "bedroom", "steam",
                     "wardrobe", "wardrobes", "cupboard", "cupboards", "drawer", "drawers",
                     "closet", "suitcase", "mattress", "bedding", "sofa", "settee", "armchair",
                     "car", "van", "boot", "camper")),
        entry("damp-smell", (("damp", "musty", "mustiness", "mildew", "dampness", "damp and musty",
                              "musty and damp", "musty smell"),
                             ("smell", "smells", "smelling", "smelly", "whiff", "reek", "stinks",
                              "room", "house", "flat", "home", "bedroom", "living room", "spare room",
                              "sitting room", "dining room", "box room", "utility room", "en suite",
                              "wet room", "shower room", "wash room",
                              "loft", "attic", "basement", "cellar", "hallway", "landing", "stairs",
                              "wardrobe", "cupboard", "closet", "drawer", "mattress", "sofa", "settee",
                              "armchair", "carpet", "rug", "garage", "shed")),
              "A musty smell is usually damp rather than dirt: check for a leak or a cold outside wall, "
              "air the room properly and dry it out before covering anything up. Don't paint over damp "
              "patch, because it comes straight back.",
              avoid=("hotel", "hotels", "hotel room", "guest house", "guesthouse", "bed and breakfast",
                     "b and b", "airbnb", "holiday let", "villa", "cottage", "reception",
                     "check in", "check out", "booking", "the room we booked",
                     "washing", "laundry", "clothes", "shirt", "shirts", "sheets", "towel", "towels",
                     "machine", "dryer", "car", "van", "boot", "fridge", "freezer", "oven", "bin",
                     "bins", "dustbin", "dishwasher", "sink", "drain", "plughole",
                     "shoe", "shoes", "trainer", "trainers", "boots", "dog", "dogs", "cat", "cats",
                     "pet", "pets", "puppy", "puppies", "kitten", "kittens", "urine", "pee", "poo",
                     "sick", "vomit", "smoke", "smoking", "cigarette", "cigarettes", "cigar",
                     "fire", "burnt", "burning", "paint", "painting", "cooking", "curry", "fish",
                     "food", "garlic", "onion", "baby", "nappy", "nappies", "milk", "diesel",
                     "petrol", "exhaust", "fuel", "gas", "sewage", "chemical", "formaldehyde",
                     "wee", "wet patch",
                     "shower", "tiles", "grout", "toilet", "loo", "condensation",
                     "mould", "mold", "mouldy", "moldy", "damp patch", "rising damp",
                     "damp course", "landlord", "council", "letting agent", "environmental health",
                     "nice", "nicer", "good", "better", "fresh", "fresher", "lovely", "pleasant",
                     "smell nice", "smells nice", "smell good", "smells good", "smell fresh",
                     "smells fresh", "smell better", "smells better", "smell lovely")),
        entry("roof-leak",
              (("roof", "roofs", "loft", "attic", "ceiling", "tiles", "slates", "roof tiles",
                "flat roof", "roof space", "chimney", "light fitting", "ceiling light", "lights",
                "landing", "hallway"),
               ("leaking", "leak", "leaks", "coming in", "coming through", "pouring", "dripping",
                "water", "rain", "raining", "wet", "soaked", "damp coming", "buckets",
                "go up", "get up", "getting up there", "get on the roof", "climb", "ladder", "safe",
                "storm", "blew off", "blown off", "missing tiles", "damaged", "tarp", "tarpaulin",
                "bulging", "sagging", "bowed", "belly")),
              _roof_leak,
              avoid=("boiler", "radiator", "washing machine", "dishwasher", "tap", "taps", "faucet",
                     "toilet", "sink", "shower", "bath", "overflow", "drain", "drains", "gutter",
                     "gutters", "downpipe", "window", "windows", "condensation", "mould", "mold",
                     "musty", "car", "van", "boat", "tent", "sofa", "roof box", "moss", "caravan",
                     "bathroom", "kitchen", "wall", "walls", "floor", "floors", "grout",
                     "grouting",
                     "dried", "drying out", "old"),
              guard=_a_mark_that_is_live),
        entry("damp-patch-ceiling",
              (("ceiling", "ceilings", "plaster", "paint", "skirting"),
               ("damp", "patch", "wet", "brown", "yellow", "stain", "stains", "dripping", "peeling",
                "water coming", "coming through", "blistering",
                "mark", "marks", "water mark", "water marks")),
              "A brown or yellow patch on a ceiling is water, and the first job is to find where it "
              "comes in rather than paint over it. Look at what is above: a bathroom or a radiator "
              "pipe means a leak at the sealant, the trap or the joint, and an outside wall or the "
              "roof means it only grows after rain, so note whether it does. Press it with a finger - "
              "soft, crumbly plaster or a slow drip means it is live and worth turning the water off; "
              "a hard dry ring that has not moved in weeks is an old stain, which you seal with a "
              "stain block and then paint. Photograph it with the date and tell the landlord or your "
              "insurer in writing, because a patch painted over with no record is one you cannot "
              "claim for.",
              avoid=("mould", "mold", "mildew", "smell", "musty", "condensation", "window", "windows",
                     "steam", "damp proof", "rising damp", "basement", "cellar floor",
                     "fence", "fences", "shed", "decking", "gate", "patio")),

        entry("broken-window",
              (("window", "windows", "pane", "panes", "pane of glass", "glass", "double glazed",
                "sealed unit", "glazing"),
               ("broken", "broke", "broken glass", "cracked", "crack", "cracks", "cracking", "smashed",
                "shattered", "shatters", "came out", "come out", "fell out", "blown", "gone",
                "replace", "replacing", "repair", "repairing", "fix", "fixing", "cost", "costs",
                "how much", "myself", "diy", "glazier", "board up", "make safe", "what do i do",
                "who do i call", "quote", "reglaze", "reseal", "putty")),
              _broken_window,
              ask=("window", "windows", "pane", "panes", "double glazed", "double-glazing",
                   "sealed unit", "glazing", "front door", "back door", "patio door", "sash",
                   "window frame", "french door"),
              avoid=("windscreen", "windshield", "car", "cars", "van", "drinking glass",
                     "juice", "sugar", "caffeine", "calorie", "calories", "coke", "cola", "wine",
                     "beer", "water", "milk", "drink", "drinking", "drank", "pint", "whisky",
                     "whiskey", "gin", "vodka", "tea", "coffee", "glass of", "tumbler", "mug",
                     "wrap it", "bin it", "cut myself", "in my hand", "in the sink", "washer",
                     "spectacles", "optician", "mirror", "phone", "screen", "shower screen", "shower",
                     "oven", "hob", "cooker", "stove", "log burner", "splashback", "picture",
                     "tv", "telly", "watch", "table", "fish tank", "aquarium", "shelf", "cupboard",
                     "draught", "draft", "condensation", "steam", "mould", "mold", "streaky",
                     "misted", "misting", "misty", "mist", "cloudy", "hazy", "fogged", "fogging",
                     "smear", "smears", "clean", "cleaning", "paint", "painting", "handle", "hinge",
                     "catch", "lock", "latch", "blind", "curtain", "insulation", "double glazing quote",
                     "how much do double glazing", "windows are wet",
                     "sticking", "sticks", "stuck", "jammed", "jams", "painted shut", "swollen",
                     "swelled", "hard to open", "hard to close", "wont open", "won't open",
                     "wont shut", "won't shut", "wont close", "won't close", "rubs", "dragging"),
              bias=1),
        entry("sink-blocked", ("sink", ("blocked", "blockage", "slow", "draining", "drain", "water",
                                         "unblock", "unblocking", "plunger",
                                         "clog", "clogs", "clogged", "clogging", "clogged up",
                                         "unclog", "unclogging", "unclogged")),
              "Start with a plunger over the plughole with a little water in the bowl, then undo the "
              "trap underneath (bucket first) and pull the gunk out. A kettle of hot water with a "
              "spoonful of bicarbonate and vinegar clears the rest; chemical drain cleaner is the last "
              "resort, not the first.",
              avoid=("under the sink", "under my sink", "behind the sink", "underneath",
                     "under the unit", "under the cupboard",
                     "wet patch", "damp patch", "puddle", "puddles", "leak", "leaks", "leaking",
                     "dripping", "flood", "flooded", "soaked", "ceiling"),
              bias=1),
        entry("toilet-blocked", (("toilet", "loo", "bog"), ("blocked", "blockage", "unblock", "flush",
                                                           "overflow", "overflowing", "plunger",
                                                           "clog", "clogs", "clogged", "clogging",
                                                           "clogged up", "unclog", "unclogging",
                                                           "unclogged")),
              "Use a plunger with a good seal, and pour a bucket of water in from waist height rather "
              "than flushing again. If the water is rising, turn off the stopcock or lift the ball "
              "valve so it can't overflow, and never pour chemical cleaner into a blocked toilet.",
              bias=2,
              avoid=("wont stop", "won't stop", "keeps running", "stop running", "running", "runs",
                     "keeps filling", "trickling", "trickle", "hissing", "keeps topping",
                     "after flushing",
                     "how much water", "much water", "litres", "litre", "water use", "per flush",
                     )),
        entry("rattle-stop",
              (("shutter", "shutters", "blind", "blinds", "loo seat", "toilet seat", "window",
                "windows", "pipe", "pipes", "chimney", "flue", "gate", "gates", "fence", "fences",
                "panel", "panels", "vent", "grille"),
               ("banging", "bang", "bangs", "rattling", "rattle", "rattles", "clattering", "knocking",
                "flapping", "vibrating", "buzzing", "humming", "noisy", "noise")),
              "A bang is a part with play in it, so press and shake each end to find what moves before "
              "you buy anything. A loo seat bangs because the rubber bumpers under it have gone hard: "
              "tighten the two bolts through the hinges and fit new bumpers, which cost a couple of "
              "pounds. A blind bangs on the wall or the window when the bottom rail has nothing to "
              "rest against, so shorten the pull cord onto a cleat. A shutter or a gate in the wind "
              "wants a hook and eye or a magnetic catch holding it open. Banging in a chimney is birds "
              "or a flue that has no cowl on top, a banging pipe is water hammer, which wants the "
              "clips tightened and a clip or two more, and a fence or a gate that rattles in the "
              "wind wants the post fixing or a second bolt through the hinge.",
              avoid=("clean", "cleaning", "wash", "washing", "dust", "dusty", "mould", "damp",
                     "bleed", "bleeding", "cold", "boiler", "sweep", "sweeping",
                     "draught", "draft", "slam", "slamming", "shut", "open", "broken", "cracked",
                     "won't close", "wont close")),
        entry("curtain-rail",
              (("curtain rail", "curtain pole", "curtain rod", "curtain track", "rail", "pole"),
               ("put up", "hang", "hanging", "fit", "fitting", "fitted", "install", "fix",
                "how high", "what height", "drill", "bracket", "brackets", "level",
                "coming off", "came off", "come off", "keeps coming off", "coming away",
                "came away", "pulled out", "pulling out", "ripped out", "torn out", "fallen",
                "fell", "fell down", "falling down", "came down", "come down", "sagging",
                "dropping", "loose", "wobbly", "won't stay", "wont stay", "not holding",
                "what fixing", "what fixings", "rawl plug", "rawlplug", "hollow wall")),
              "Mark both ends before you drill: the rail sits 10 to 15cm above the window recess and "
              "15 to 20cm past each side, so the curtains clear the glass, and check it with a spirit "
              "level because a rail two people can see is crooked. Fix into masonry or a timber stud "
              "rather than the plasterboard alone - a rail hangs all its weight on two points and "
              "pulls downwards - so find the studs with a magnet dragged along the wall, which sticks "
              "at the screw heads, or drill and use a masonry plug. Hang the curtains on the rail "
              "before it goes up, and use the last eyelet at each end.",
              avoid=("iron", "wash", "washing", "clean", "shower",
                     "broken", "tv", "television", "picture", "shelf", "coat", "towel")),
        entry("curtains-drag",
              (("curtain", "curtains"),
               ("sticking", "sticks", "stick", "dragging", "drag", "stiff", "jerky", "scraping",
                "wont slide", "won t slide", "wont pull", "won t pull", "hard to pull",
                "hard to open", "hard to close", "squeaking", "squeak")),
              "Rub the rod with a candle end or furniture wax, or spray it with silicone, and the rings "
              "will run again: the squeak is the rod and the ring, not the fabric. Plastic gliders go "
              "chalky and grip after a few years, so replace them, and check the brackets are not "
              "sagging in the middle, which pinches the two curtains against each other. A track gets "
              "the same treatment plus a vacuum along the slot, because fluff in the runners does most "
              "of the sticking.",
              avoid=("shower", "bath", "liner", "iron", "ironing", "wash", "washing", "clean",
                     "cleaning", "mould", "mold", "fade", "fading", "blackout", "put up", "hang",
                     "hanging", "fit", "fitting", "fallen", "fell", "came down", "buy", "length",
                     "shorten", "hem", "sew", "sewing", "blinds"),
              bias=2),
        entry("tap-drip", (("tap", "faucet"), ("drip", "drips", "dripping", "leak", "leaks", "leaky",
                                              "leaking", "washer")),
              _a_dripping_tap),
        entry("a-washer-two-things",
              (("washer", "washers"),
               ("new", "need", "needs", "replace", "replacing", "change", "changing", "fit",
                "fits", "size", "what size", "which size", "right size",
                "have", "has", "got", "ive", "i've", "bought", "buy", "buying", "should",
                "which")),
              _a_washer_two_things,
              guard=_a_washer_with_no_other_subject,
              bias=-1),
        entry("toilet-running",
              (("toilet", "loo", "loos", "lav", "lavatory", "wc", "bog", "cistern", "pan",
                "flush button", "flush", "flushes",
                "ball valve", "ballcock", "fill valve", "flush valve", "float valve", "float"),
               ("running", "runs", "keeps running", "wont stop", "wont stop running", "stop running",
                "keeps filling", "filling", "trickling", "trickle", "constantly", "all the time",
                "hissing", "keeps topping", "stuck", "jammed", "wont go down", "wont push",
                "broken", "gone", "seized", "worn")),
              "Turn the water off at the isolation valve under the cistern, take the lid off and "
              "watch where it goes. Trickling down the back of the pan means the flush valve is not "
              "seating: feel the rubber seal for grit, and a new flapper is a couple of pounds and "
              "clips straight on. Water into the overflow or up the side means the fill valve is too "
              "high or its float has gone, so screw the level down and replace the valve if that does "
              "not stop it. A button that stays down or does nothing is the button or the syphon "
              "under it, and those are a few pounds at a hardware shop and clip in without any "
              "plumbing.",
              avoid=("blocked", "blockage", "overflowing", "smell", "clean", "cleaning", "stain",
                     "limescale ring", "brush",
                     "hot flush", "hot flushes", "flushes at night", "sweats", "menopause",
                     "perimenopause",
                     "need the loo", "need a loo", "needing the loo", "need to loo",
                     "need the toilet", "needing the toilet", "keep needing",
                     ),
              guard=_going_to_the_loo),
        entry("toilet-leak",
              (("toilet", "loo", "loos", "lav", "lavatory", "wc", "cistern", "pan", "bog"),
               ("leak", "leaks", "leaking", "leaky", "drip", "drips", "dripping", "pool", "puddle",
                "puddles", "floor", "seal", "seals", "joint", "joints", "fix", "repair", "water",
                "wet")),
              "Where the water shows tells you which seal has gone. Water on the floor at the base "
              "means the wax or rubber seal between the pan and the soil pipe - the pan has to come "
              "up, so an hour of a plumber's time. A trickle from under the cistern is the inlet "
              "connection or the coupling washer, a quarter turn with a spanner. Water in the bowl "
              "that will not stop is the flush valve. Turn the water off at the isolation valve "
              "beside the cistern first, dry everything, and watch again - and if you rent, tell the "
              "landlord in writing rather than taking the pan off yourself.",
              avoid=("blocked", "blockage", "unblock", "plunger", "smell", "smells", "smelly", "clean",
                     "cleaning", "stain", "stains", "limescale", "brush", "brown", "brownish", "rusty",
                     "yellow", "yellowish", "green", "cloudy", "murky", "discoloured", "black",
                     "colour", "color", "taste", "tastes", "drink", "drinking", "constipated",
                     "constipation")),
        entry("tap-pressure-low",
              (("tap", "taps", "faucet", "shower", "showers", "shower head", "water"),
               ("low pressure", "no pressure", "pressure is low", "pressure has dropped", "weak",
                "weedy", "trickle", "trickling", "barely", "hardly", "dribble", "slow flow",
                "pressure", "rubbish", "poor", "useless", "hardly any", "no force")),
              _pressure_weak,
              avoid=("boiler pressure", "boiler", "radiator", "tyre", "car", "blood", "oil pressure",
                     "pressure washer", "gas",
                     "drink", "drinking", "drank", "thirsty", "hydrate", "hydrated", "dehydrated",
                     "bill", "bills", "water the", "cuppa", "brew")),
        entry("tap-no-water",
              (("tap", "taps", "faucet", "faucets", "mixer tap", "kitchen tap", "bathroom tap",
                "hot tap", "cold tap", "the water", "water supply", "water"),
               ("not working", "doesnt work", "doesn't work", "stopped working", "no water", "none coming", "nothing comes out", "nothing coming", "wont run",
                "won't run", "wont come on", "wont turn on", "won't turn on", "cant turn on",
                "no flow", "stopped", "stops", "spits", "sputters", "splutters", "airlock",
                "dry", "dry tap", "barely", "suddenly")),
              "If it is one tap and the rest of the house runs, it is that tap's own supply: the "
              "isolation valve on the pipe under the sink is a slot-head screw, and a half turn the "
              "other way is the usual answer. With the valve open, unscrew the spout aerator and "
              "soak it in vinegar - a scaled-up aerator stops a tap dead. If every tap is dry, it is "
              "the stopcock where the mains comes in, or the supply itself, so check the water "
              "company's postcode status before you pay anyone. A tap that runs and then stops is an "
              "airlock: hold your palm over the spout and open it fully for a few seconds, or "
              "back-fill it with a jug from another tap. And if the pipe is in a cold wall in "
              "freezing weather, warm it gently with a hairdryer - never a blowtorch - with the tap "
              "left open.",
              avoid=("drip", "drips", "dripping", "leak", "leaks", "leaking", "washer",
                     "pressure", "low pressure", "weak", "trickle", "limescale", "scale",
                     "shower", "showers", "loo", "toilet", "cistern", "boiler", "radiator",
                     "radiators", "washing machine", "dishwasher", "immersion", "cylinder",
                     "hot water", "cold water", "drink", "drinking", "water bill", "meter",
                     "outside tap", "garden tap", "hosepipe", "hose",
                     "tap to pay", "tap and pay", "to pay", "apple pay", "google pay",
                     "contactless", "card machine", "phone", "wallet", "debit card",
                     "credit card", "bank card",
                     "tap water")),
        entry("limescale", (("kettle", "limescale", "scale", "tap", "shower head", "showerhead"),
                            ("descale", "clean", "white", "fur", "build", "rid", "remove",
                             "blocked", "blocking",
                             "clogged", "clogging", "spray", "holes", "weak",
                             "what can i do", "do about", "what can i use", "anything for",
                             "anything to", "how do i stop", "how to stop", "keeps coming",
                             "coming back", "comes back", "get it off", "get rid of it",
                             "what do i do", "what should i do", "deal with", "get rid",
                             "anything i can do", "do about it", "cope with")),
              "Soak the scaled part in half water, half white vinegar, or a spoonful of citric acid in "
              "water: boil it in the kettle and leave it an hour, or tie a bag of it round a shower "
              "head or tap for an hour. Rinse twice afterwards, and do it again whenever it furs up.",
              avoid=("drip", "drips", "dripping", "dripped", "leak", "leaks", "leaking", "leaked",
                     "washer", "washers", "cartridge", "cartridges", "plumber", "valve",
                     "no hot water", "water pressure", "blocked drain", "drains",
                     "kettle", "kettles", "boiler", "boilers", "steam iron", "washing machine",
                     "dishwasher", "coffee machine",
                     "plant", "plants", "garden", "gardening", "insects", "aphids", "leaves",
                     "leaf", "soil", "compost", "lawn", "houseplant", "houseplants",
                     "orchid", "orchids", "fern", "fern fronds")),
        entry("limescale-why", (("limescale", "scale", "scaled", "scaling", "fur",
                                 "furred", "furry", "white stuff", "white marks", "chalky marks",
                                 "chalky", "hard water",
                                 "water is hard", "water hard", "water is so hard",
                                 "water is very hard", "water tastes hard",
                                "hard water stain", "hard water stains"),
                                ("tap", "taps", "shower", "shower head", "showerhead",
                                 "iron", "steam iron", "washing machine", "dishwasher", "water",
                                 "prevent")),
              ("Hard water is the reason: it carries dissolved calcium and magnesium, and they are "
               "left behind as a chalky scale whenever the water boils away or dries on a surface. "
               "Soak the scaled part in half water, half white vinegar, or a spoonful of citric acid "
               "in water - boil it in the kettle and leave it an hour, or tie a bag of it round a "
               "shower head or tap for an hour - then rinse twice. A filter jug or a scale reducer "
               "cuts down how often it comes back."),
              avoid=("kettle", "kettles", "boiler", "heating", "radiator", "radiators", "fish", "skin",
                     "weigh", "weight", "muscle", "diet", "recipe", "flour", "sugar",
                     "hair", "shampoo", "conditioner", "scalp",
                     "bad for you", "bad for me", "good for you", "safe to drink", "is it safe",
                     "harmful", "dangerous", "kidney", "kidneys", "drink it", "drinking",
                     "health", "healthy", "formula", "baby", "babies", "softener")),
        entry("rust-marks",
              (("rust", "rusty", "rusted", "rust stain", "rust stains", "rust marks"),
               ("shower", "bath", "sink", "basin", "toilet", "glass",
                "screen", "bathroom", "plughole", "plug hole", "patio", "paving", "paving slabs",
                "drive")),
              ("Brown marks are iron rather than the calcium of scale, from a steel screw or fitting, "
               "a chip in the enamel, or iron in the water, and the acid that lifts scale lifts rust "
               "too: white vinegar or a citric acid paste, left ten minutes and rinsed. Never bleach, "
               "because it sets rust into the surface, and never wire wool, which leaves specks of "
               "steel behind to rust again. If it keeps coming back, find the steel that stays wet - "
               "a screw, a shower rose, the frame of the screen - and dry it or replace it."),
              avoid=("tray", "trays", "tin", "tins", "knife", "knives", "cutlery", "pan", "pans",
                     "bike", "bicycle", "chain", "car", "van", "gate", "nail", "nails", "screwdriver",
                     "tools", "tool", "garden furniture", "barbecue", "bbq",
                     "washing machine", "washer", "drum", "seal", "laundry", "clothes", "shirt",
                     "shirts", "fabric", "whites", "white shirt")),

        entry("kettle-boil-time",
              (("kettle", "kettles"),
               ("how long", "long does", "minutes", "take", "takes", "time", "quick",
                "quickly", "fast", "how many")),
              "About 45 seconds for one mug and around 3 minutes for a full 1.7-litre kettle in a 3kW "
              "one, so boiling only what you are going to drink is both quicker and cheaper. A 2kW "
              "kettle takes roughly half as long again.",
              ask=("how long", "minutes", "take", "takes", "time", "quick", "quickly", "fast",
                   "how many"),
              avoid=("last", "lasts", "lasting", "lifespan", "life span", "life expectancy", "years",
                     "descale", "descaleing", "limescale", "scale", "scaled", "fur", "furred",
                     "noise", "noisy", "boiler", "heating", "cost", "costs",
                     "pence", "electricity", "energy", "bill", "cheaper", "leak", "leaking",
                     "broken", "not working", "switch", "element", "fill", "capacity",
                     "lifetime", "life", "replace", "replacement", "new kettle", "worth it",
                     "how long do they", "how long should", "keep going", "buy") + JOB_GUARD,
              bias=2),
        entry("kettle-smell",
              (("kettle", "kettles", "boiled water", "water in the kettle"),
               ("smell", "smells", "smelly", "smelling", "stink", "stinks", "odour", "odor",
                "taste", "tastes", "tasting", "musty", "earthy", "metallic", "plastic",
                "chemical", "fusty")),
              "A smell from a kettle is nearly always scale or water left standing in it: fill it "
              "with equal parts water and white vinegar, boil it, leave it half an hour, then boil "
              "fresh water and tip it away twice. A new kettle's plastic smell fades after a few "
              "boils; a musty one means water has sat in it, so empty it each night. If the taste "
              "still comes through, filter the water.",
              avoid=("how long", "minutes", "cost", "costs", "electricity", "bill", "noise",
                     "noisy", "boiler", "burn", "burnt", "scald", "spilled", "spilt",
                     "descale", "limescale", "scale", "fur", "leak", "leaking"),
              bias=2),
        entry("kettle-slow",
              (("kettle", "kettles"),
               ("slow", "slowly", "slower", "taking so long", "takes so long", "takes ages",
                "taking ages", "forever", "why")),
              "The element has to heat through limescale before it reaches the water, so a badly "
              "scaled kettle can take twice as long - vinegar or citric acid brings it back to speed. "
              "Past that, a full kettle takes longer than a mugful, a 2kW kettle is about half the "
              "speed of a 3kW one, and very cold water is slower than water that has stood.",
              ask=("why", "slow", "slowly", "slower", "long", "ages", "forever", "takes"),
              avoid=("boiler", "noise", "noisy", "bang", "banging", "rumbling",
                     "broken", "not working", "switch", "element", "cost", "costs", "cheaper",
                     "energy", "bill", "descale", "descaleing", "limescale", "scaled", "scale",
                     "removing", "rid of", "fur", "furred", "furry", "white stuff", "chalky",
                     "smell", "smells", "smelly", "smelling", "stink", "stinks", "odour", "odor",
                     "taste", "tastes", "tasting", "funny", "metallic", "plastic"),
              bias=3),
        entry("pipes-freezing", (("pipe", "pipes", "plumbing", "stopcock"),
                                 ("freeze", "frozen", "freezing", "froze", "freeze up",
                                  "froze up", "frozen solid", "thaw", "burst", "lagging",
                                  "lag", "split", "stop tap", "stop valve", "water off")),
              _pipes,
              avoid=("boiler", "radiator", "central heating", "car", "windscreen", "screen wash",
                     "freezer", "food", "vegetable", "veg", "meat", "bread", "cake", "bake",
                     "baking", "shoulder", "fingers", "hands", "feet", "paddling pool")),
        entry("water-shutoff",
              (("stopcock", "stop tap", "stop valve", "isolating valve", "water main", "mains water",
                "water supply", "water off", "shut the water", "shutting the water",
                "shut off the water", "shutting off the water", "turn the water", "turning the water",
                "turn off the water", "turning off the water", "switch the water off",
                "drain the pipes", "draining the pipes", "drain the system", "draining the system",
                "isolate the water", "stop the water",
                "water keeps running", "water keeps coming", "water wont stop", "water won't stop",
                "water wont stop running", "water won't stop running", "water is running",
                "water runs", "water running", "running water", "pipes keep running"),
               ("where", "find", "locate", "how", "turn", "turning", "shut", "shutting", "off",
                "on", "drain", "draining", "wont", "won't", "keeps", "still", "stop", "running",
                "leaking", "flood", "flooded", "valve", "mains", "supply", "house", "flat",
                "kitchen", "sink")),
              _water_off,
              bias=3,
              avoid=("drink", "drinking", "safe to drink", "taste", "tastes", "brown", "smelly",
                     "boiler", "radiator", "heating", "filtr", "filter", "softener", "limescale",
                     "rinse", "rinsing", "rinsed", "rice", "pasta", "lentils", "quinoa",
                     "chickpeas", "beans", "noodles", "spinach", "greens",
                     "hot water", "hot tap", "hot taps", "immersion", "cylinder",
                     "heater", "immersion", "cylinder", "hot water tank",
                     "pool", "swimming", "paddling", "fish tank", "aquarium", "water butt", "garden",
                     "plants", "lawn",
                     "phone", "phones", "app", "apps", "storage", "memory", "battery", "laptop",
                     "computer", "tablet", "printer", "software", "update", "download", "wifi",
                     "draining", "drains", "drain", "drainage", "plughole", "plug hole",
                     "u bend", "blocked", "unblock",
                     "internet", "screen", "data", "background",
                     "toilet", "toilets", "loo", "loo", "cistern", "ballcock", "flush", "flushing",
                     "dripping", "drips", "drip", "shower", "bath", "bathroom")),
        entry("water-less",
              (("use less water", "using less water", "uses less water", "save water", "saving water",
                "water saving", "reduce water", "reduce my water", "reduce our water",
                "cut water use", "cut my water use", "cut our water use", "wasting water",
                "waste water", "water waste", "water use", "water usage", "using so much water",
                "waste less water", "wasting less water", "waste less water at home",
                "use so much water", "less water at home", "save on water"),
               ("how", "ways", "tips", "help", "stop", "much", "home", "house", "household",
                "family", "flat", "ours", "we use", "reduce", "cut", "save", "saving", "less")),
              "A shower of five minutes rather than ten saves about 40 litres a time, and a dripping "
              "tap wastes around 5,500 litres a year - both are a washer or a shorter timer, not a new "
              "bathroom. After those, run the washing machine and the dishwasher only when they are "
              "full (a half load uses nearly the same water as a full one), put a water butt on the "
              "downpipe for the garden instead of a hose, and drop a cistern bag in an old loo, which "
              "saves a litre or two a flush. A water meter is free to have fitted in most of the UK "
              "and usually cuts a bill for one or two people, though a big family can pay more on one.",
              avoid=("drink", "drinking", "thirsty", "thirst", "safe to drink", "plants", "plant",
                     "lawn", "water the", "water my", "water butt", "rain barrel",
                     "sprinkler", "irrigation", "hose", "pool", "swimming", "fish tank", "aquarium",
                     "garden", "gardening", "allotment", "flowerbed", "flower bed", "hanging basket",
                     "a bath or a shower", "bath or a shower", "bath or shower", "a shower or a bath",
                     "shower or a bath", "shower or bath", "bathtub", "a bath", "hot bath",
                     "leak", "leaking", "burst", "flood", "flooded", "blocked", "drain", "drains",
                     "boiler", "radiator", "hot water", "softener", "hard water", "limescale",
                     "rice", "pasta", "dough", "bread", "pastry", "baking", "cake", "sauce", "stock",
                     "simmer", "boil", "boiling", "kettle", "recipe", "cook", "cooking", "pan",
                     "washer", "dripping", "drip", "drips", "eye", "eyes",
                     "dishwasher", "dishwashers", "washing machine", "washing machines",
                     "washer", "washers", "tumble dryer", "tumble drier", "toilet", "toilets",
                     "flush", "flushes", "cistern", "shower", "showers", "a shower of",
                     "bathtub", "hose", "hosepipe")),

        entry("gas-shut-off",
              (("gas", "gas meter", "gas supply", "gas valve", "meter box", "gas pipe",
                "gas shut off valve", "gas shutoff valve", "gas stop valve", "gas stopcock"),
               ("turn off", "turn it off", "turning off", "shut off", "shutting off", "isolate",
                "switch off", "turn", "off", "where", "valve", "handle", "emergency switch",
                "leaking gas", "smell gas", "smelling gas", "stop the gas")),
              "The gas shut-off is the lever on the pipe beside the meter, usually in a box outside "
              "or under the stairs: a quarter turn so the lever sits across the pipe rather than "
              "along it turns the gas off. If you can smell gas, do not touch a switch, a light or a "
              "phone indoors - open the windows, get everyone out and ring the gas emergency line "
              "from outside: 0800 111 999 in England, Scotland and Wales, 0800 002 001 in Northern "
              "Ireland, 911 in the US. Only a Gas Safe engineer turns it back on.",
              avoid=("bill", "bills", "price", "tariff", "cheaper", "cost", "usage", "boiler",
                     "cooker", "hob", "oven", "fire", "fireplace", "cylinder", "bottle", "bbq",
                     "barbecue", "car", "central heating", "supplier", "reading", "standing charge",
                     "back on", "turn on", "turning on", "turned on", "switch on", "switching on",
                     "gas on", "gas back on", "turn the gas on", "turning the gas on",
                     "relight", "re-light", "pilot light", "pilot",
                     "gas safe", "gas safety", "find a", "find me a")),
        entry("boiler-pressure", ("boiler", ("pressure", "low", "drop", "dropped", "bar", "gauge")),
              "Top the pressure up to between 1 and 1.5 bar using the filling loop, then bleed the "
              "radiators and check it again the next day. The pressure falls because water is escaping "
              "somewhere: a radiator valve, a joint, or the pressure relief pipe outside. If it keeps "
              "dropping, stop topping it up and get a heating engineer out.",
              outcomes=(("next",
                         "Get a heating engineer out and tell them how often it has dropped since "
                         "you topped it up: a system that loses pressure twice is losing water at a "
                         "valve, a joint or the relief pipe, and each top-up only hides it."),)),
        entry("heating-pressure", (("pressure", "bar", "psi", "gauge"),
                                   ("down", "low", "lowest", "dropped", "drop", "dropping", "half",
                                    "zero", "under", "below", "fallen", "falling", "topped",
                                    "top up", "topping up", "filling loop", "what should",
                                    "sort", "sorts", "sort it out", "sort out",
                                    "fix", "fix it", "fixes it", "how do i fix")),
              "Top the pressure up to between 1 and 1.5 bar using the filling loop, then bleed the "
              "radiators and check it again the next day. The pressure falls because water is escaping "
              "somewhere: a radiator valve, a joint, or the pressure relief pipe outside. If it keeps "
              "dropping, stop topping it up and get a heating engineer out.",
              guard=_a_gauge_reading,
              avoid=("under pressure", "feel the pressure", "feeling the pressure",
                     "peer pressure", "stressed", "stress", "anxious", "anxiety",
                     "pressure at work", "pressure at school",
                     "will bleeding", "would bleeding", "does bleeding", "do i bleed",
                     "will bleeding them", "bleeding fix", "bleeding sort", "bleeding help",
                     "bleed them", "bleeding the radiators fix",
                     "too high", "high", "higher", "over 2", "over 3", "above 2", "above 3",
                     "rising", "climbing", "2 bar", "2.5 bar", "3 bar", "overpressure",
                     "boiler", "boilers", "combi")),
        entry("bleed-and-pressure", (("pressure", "bar", "gauge", "top up", "top it up"),
                                    ("fix", "fixes", "cure", "cures", "sort", "sorts",
                                     "does that", "will that", "would that", "that fix",
                                     "help the pressure", "helps the pressure",
                                     "help the gauge", "helps the gauge", "worth it")),
              "Bleeding does not put pressure back in - it lets air out, and it can drop the "
              "gauge a little. Top it up at the filling loop to 1 to 1.5 bar with the system "
              "cold, then check it the next day; if it is low again there is a leak somewhere "
              "and that is an engineer's job.",
              guard=_a_gauge_reading,
              avoid=("too high", "high", "higher", "over 2", "over 3", "above 2", "above 3",
                     "rising", "climbing", "2 bar", "2.5 bar", "3 bar", "overpressure",
                     "under pressure", "peer pressure", "pressure at work", "pressure at school",
                     "how do i sort", "how to sort", "how can i sort", "how do you sort",
                     "how do i fix", "how to fix", "how do i top", "what do i do about the pressure",
                     "without pressure", "putting pressure", "pressure myself", "pressure from",
                     "pressure her", "pressure him", "pressure them", "sats", "exams", "revision",
                     "blood pressure", "tyre", "tyres", "tire", "tires",
                     "cost", "costs", "costing", "price", "prices", "priced", "quote", "quotes",
                     "quoted", "charge", "charges", "£")),
        entry("boiler-noise", (("boiler", "heating", "central heating", "heat pump"),
                               MACHINE_SOUNDS + NOISE_WORDS),
              _boiler_noise),
        entry("boiler-kettling", (("kettling", "kettle", "kettles", "limescale", "scale", "descale",
                                   "sludge"),
                                  ("boiler", "boilers", "combi", "heating", "central heating",
                                   "hot water", "radiator", "radiators")),
              ("Kettling - a noise like a kettle boiling as it fires - is limescale on the heat "
               "exchanger, not air in the pipes, so bleeding the radiators will not stop it. Get a "
               "heating engineer to power-flush or descale the system and fit a scale reducer or a "
               "magnetic filter; turn the boiler flow temperature down a notch meanwhile, because "
               "kettling gets worse the hotter it runs."),
              avoid=("how long", "how many minutes", "minutes to boil", "take to boil",
                     "does it take", "tea", "coffee", "cup of"),
              bias=1),
        entry("radiator-noise", ("radiator", ("noise", "noisy", "banging", "clicking", "gurgling",
                                              "ticking", "loud")),
              ("Ticking and clicking is the pipes expanding as they heat, which is normal and stops "
               "once the system is warm. Banging or gurgling means air or trapped water: bleed the "
               "radiators and check the boiler pressure sits between 1 and 1.5 bar.")),
        entry("heating-goes-cold",
              (("heating", "the heating", "my heating", "our heating", "central heating",
                "hot water", "my hot water", "hot tap", "hot taps", "boiler",
                "immersion", "hot water cylinder", "cylinder", "hot bath", "bath water"),
               ("keeps going cold", "keeps running cold", "keeps coming out cold",
                "goes cold", "going cold", "runs cold", "running cold", "comes out cold",
                "cold after", "goes cold after", "cools down", "keeps cooling", "hot then cold",
                "comes on then goes off", "hot and cold", "lukewarm", "never really hot")),
              _heating_goes_cold,
              bias=2,
              avoid=("radiator", "radiators", "rads", "bill", "bills", "cheaper", "cost", "save",
                     "tariff", "insulation", "energy", "kettle", "shower", "washing machine",
                     "dishwasher", "drink", "drinks", "beer", "wine", "milk", "oven", "microwave",
                     "hob", "air fryer", "toaster", "iron", "food", "bath water")),
        entry("radiator-bleed", (("radiator", "towel rail", "towel radiator", "heated towel rail",
                                  "ladder rail", "ladder radiator", "chrome rail"),
                                 ("bleed", "bled", "bleeding", "bledding", "cold",
                                  "bottom", "noise", "hot",
                                  "cold at the top", "hot at the bottom", "warm at the top",
                                  "cold at the top of the radiator")),
              "Radiators that are hot at the bottom and cold at the top have air in them: open the bleed "
              "valve at the top with a radiator key, a quarter turn at a time, with a cloth under it, "
              "until water trickles out steadily. Two minutes a radiator is all it takes, and a whole "
              "house takes ten to fifteen minutes. Then check the boiler pressure and top it up if it's "
              "below 1 bar.",
              avoid=("cold at the bottom", "cold at the botto", "cold bottom", "hot at the top",
                     "warm at the top", "cold along the bottom", "filling loop",
                     "not hot at the bottom", "not warm at the bottom", "not getting hot at the "
                     "bottom", "isnt hot at the bottom", "isn't hot at the bottom",
                     "lukewarm at the bottom", "cool at the bottom"),
              guard=_the_boiler_is_not_the_fault),
        entry("radiator-bleed-key",
              (("radiator key", "bleed key", "bleeding key", "key for the radiator",
                "key for a radiator", "radiator valve key", "special key", "little key", "small key",
                "key", "keys"),
               ("radiator", "radiators", "rad", "rads", "bleed", "bled", "bleeding", "bleed them",
                "bleed it", "valve", "valves", "towel rail")),
              "Yes - a radiator bleed key: a little square or half-moon spanner, about two or three "
              "pounds from a hardware shop or a big supermarket, and a cloth under the valve to catch "
              "the drips. Some newer valves take a small flat screwdriver instead, so look at the slot "
              "before you buy. A quarter turn is enough, and you stop when water runs steadily rather "
              "than hissing air.",
              avoid=("door", "doors", "front door", "back door", "lock", "locks", "lockout", "locked",
                     "snapped", "snap", "lost my keys", "lost the key", "spare key", "keyboard",
                     "keyboards", "keypad", "keyring", "key fob", "fob", "car key", "bike lock",
                     "padlock", "ignition", "remote", "opener", "cylinder lock", "euro cylinder",
                     "cold at the bottom", "hot at the top", "sludge", "noise", "banging",
                     "pressure", "thermostat", "trv")),
        entry("radiator-cold-bottom",
              ("radiator", ("cold at the bottom", "cold along the bottom", "cold bottom",
                            "hot at the top", "warm at the top", "bottom is cold",
                            "bottom stays cold", "half cold", "never gets hot",
                            "not getting hot at the bottom", "not hot at the bottom",
                            "not warm at the bottom", "wont get hot at the bottom",
                            "won't get hot at the bottom", "doesnt get hot at the bottom",
                            "doesn't get hot at the bottom", "getting hot at the bottom",
                            "lukewarm at the bottom", "cool at the bottom",
                            "cold at the bottom of", "cold along the bottom of")),
              "Hot at the top and cold at the bottom is sludge sitting in the radiator, not air, so "
              "bleeding it will not help: the water cannot get round the bottom. Ask a heating engineer "
              "to power-flush the system or add a chemical cleaner, and have a magnetic filter fitted "
              "so it does not come back. Turning the other radiators off to push water through the cold "
              "one is a five-minute test that shows whether it is sludge or a stuck valve."),
        entry("radiator-not-hot",
              (("radiator", "radiators", "rad", "rads", "central heating", "the heating",
                "heating"),
               ("upstairs", "downstairs", "landing", "first floor", "ground floor",
                "not getting", "not warming", "not heating", "isnt getting", "isn't getting",
                "arent getting", "aren't getting", "isnt warming", "isn't warming", "isnt heating",
                "isn't heating", "wont heat", "won't heat", "wont warm", "won't warm",
                "not hot", "not warm", "stays cold", "staying cold", "still cold", "still not hot",
                "radiator is cold in", "rad is cold in",
                "radiator in my", "radiator in the", "rad in my", "rad in the",
                "never gets hot", "never gets warm", "never warms", "cold radiator",
                "one radiator is cold", "rads are cold", "radiators are cold",
                "thermostat is stuck", "thermostat stuck", "valve is stuck", "valve stuck",
                "trv stuck", "stuck on")),
              _radiator_not_hot,
              bias=2,
              avoid=("at the top", "at the bottom", "cold at the top", "hot at the bottom",
                     "top half", "bottom half", "bill", "bills", "cheaper", "cost", "save",
                     "tariff", "insulation", "bleed a radiator", "how do i bleed", "bleed valve",
                     "radiator key",
                     "hot water", "shower", "immersion", "cylinder", "hot tap", "hot taps",
                     "tank", "no hot",
                     "boiler", "oven", "water", "hob", "washing machine", "dishwasher",
                     "tumble dryer", "towel rail", "airing cupboard",
                     "microwave", "microwaves", "kettle", "kettles", "toaster", "toasters",
                     "iron", "air fryer", "airfryer", "air-fryer", "coffee machine",
                     "washer dryer", "deep fat fryer", "slow cooker", "pressure cooker",
                     "dryer", "dryers", "drier", "driers", "tumbler", "heat pump dryer",
                     "heat pump drier", "heat-pump dryer", "hair dryer", "hairdryer",
                     "compost", "composts", "heap", "heaps", "pile", "piles", "allotment",
                     "garden", "gardening", "manure", "muck")),
        entry("no-hot-water",
              (("no hot water", "hot water gone", "hot water has gone", "hot water not working",
                "hot water isnt working", "hot water isn't working", "hot water is not working",
                "hot water has stopped", "hot water stopped", "hot water has stopped working",
                "hot water comes and goes", "hot water is cold", "hot water is off",
                "hot water is lukewarm", "only cold water", "no hot water anywhere",
                "no heating and no hot water",
                "running out of hot water", "run out of hot water", "ran out of hot water",
                "runs out of hot water", "running out of hot water in the mornings",
                "hot water runs out", "hot water runs out fast", "hot water running out",
                "get hot water back", "hot water back", "hot water working again",
                "keeps running out of hot water", "hot water keeps running out",
                "hot water is not heating up", "hot water isn't heating up",
                "hot water isnt heating up", "hot water not heating up",
                "hot water is not heating", "hot water isn't heating",
                "hot water is not getting hot", "hot water isn't getting hot",
                "hot water isnt getting hot", "hot water not getting hot",
                "hot water is not hot", "hot water isn't hot", "hot water is never hot",
                "hot water is not hot enough", "hot water won't heat up", "hot water wont heat up",
                "hot water won't get hot", "hot water wont get hot",
                "water is not heating up", "water isn't heating up", "water isnt heating up",
                "water not heating up", "water is not heating", "water isn't heating",
                "water is not getting hot", "water isn't getting hot", "water isnt getting hot",
                "water won't heat up", "water wont heat up", "water is not warming up",
                "water isn't warming up", "hot water is not warming up",
                "water not hot enough", "water is not hot enough", "water isn't hot enough",
                "water isnt hot enough", "the water is not hot enough",
                "water is never hot enough", "why is my water not hot enough",
                "hot water is not hot enough for a bath",
                "hot tap is not hot", "hot tap isn't hot", "hot tap is cold",
                "hot tap water is cold", "water from the hot tap is not hot",
                "water from the hot tap is cold", "water from the hot tap runs cold",
                "why is my hot water cold", "why is the hot water cold",
                "why is our hot water cold", "why is hot water cold",
                "why is my hot water not hot", "why is the hot water not hot",
                "why is my hot water warm", "why is my hot water lukewarm",
                "why is my hot water tepid", "hot water comes out cold",
                "water comes out of the hot tap cold", "cold water comes out of the hot tap",
                "why is my water cold", "why is the water cold", "why is my tap water cold",
                "why is the tap water cold", "my tap water is cold", "the tap water is cold",
                "why is my cold water warm", "why is the cold water warm",
                "cold tap runs warm", "cold water is warm", "cold tap is warm",
                "why is the heating not warming the water", "heating is not warming the water",
                "not warming the water", "heating works but the water",
                "radiators are hot but the water", "radiators hot but no hot water"),
               ("hot water", "water", "tap", "taps", "shower", "bath", "kitchen", "bathroom",
                "flat", "house", "home", "heating", "morning", "mornings", "why", "fix", "check")),
              ("Start at the programmer: it is usually on a timer that has slipped, or on 'water "
               "only' when you wanted heating too. A combi with no hot water but working heating is "
               "nearly always low pressure or a stuck diverter valve, so look at the gauge (1 to 1.5 "
               "bar cold) and try the reset. If there is a hot water cylinder, look for the immersion "
               "switch and the thermostat on the side, and check the little header tank has water in "
               "it. Anything inside a gas boiler, or gas you can smell, is a Gas Safe engineer."),
              bias=1,
              avoid=("boiler", "boilers", "gas", "cylinder", "immersion", "pressure", "gauge",
                     "error code", "flame", "pilot", "condensate", "gas safe",
                     "bottle", "abroad", "hotel", "camping", "kettle",
                     "pool", "pools", "swimming pool", "swim", "sea", "beach", "lake", "river",
                     "glass of", "glass", "drinking", "ice", "ice cube", "cubes", "freezer",
                     "fridge", "cool box", "cooler", "flask", "gym", "hot tub", "jacuzzi",
                     "after one shower", "after a shower", "after two showers", "after a few minutes",
                     "halfway through", "half way through", "mid shower", "mid-shower", "goes cold",
                     "turns cold", "runs cold")),
        entry("shower-cold",
              (("shower", "showers", "power shower", "electric shower", "mixer shower", "shower head",
                "shower is cold", "shower is not hot", "shower is lukewarm", "shower isnt hot",
                "shower isn't hot", "shower runs cold", "shower running cold",
                "shower goes lukewarm", "why is my shower cold", "why is the shower cold",
                "why is my shower not hot"),
               ("cold", "cool", "lukewarm", "not hot", "warm", "temperature", "running cold",
                "runs cold", "cold water")),
              "If the shower runs cold but the hot taps elsewhere are fine, it is the shower: an "
              "electric shower usually wants the pull cord or a tripped switch in the consumer unit "
              "checked, and a mixer shower is often a stuck thermostatic cartridge, which frees up if "
              "you take the head off and work the temperature knob from cold to hot a few times. If "
              "the hot taps are cold too, the fault is the boiler or the cylinder rather than the "
              "shower.",
              bias=1,
              avoid=("blocked", "drain", "smell", "mould", "clean", "limescale", "buy", "best",
                     "which", "cheapest", "install", "bathroom", "tile", "leak", "boiler", "curtain",
                     "screen", "tray", "no hot water", "hot water", "house", "anywhere", "heating",
                     "goes cold", "going cold", "gone cold", "went cold", "keeps going cold",
                     "kept going cold", "turns cold", "turned cold", "hot then cold",
                     "warm then cold", "cold after a few minutes", "after a few minutes",
                     "cold quickly", "cuts out",
                     "a cold shower", "cold showers", "cold shower good", "cold shower bad",
                     "have a cold shower", "having a cold shower", "take a cold shower",
                     "taking a cold shower", "cold shower after", "cold shower every",
                     "cold shower in the morning", "cold water therapy", "cold plunge", "ice bath",
                     "sauna", "contrast shower", "bracing")),
        entry("hot-water-temperature",
              (("hot water temperature", "temperature of the hot water", "hot water be",
                "hot water hotter", "make the water hotter", "make my hot water hotter",
                "turn up the hot water", "turn up my hot water", "turn the hot water up",
                "hot water thermostat", "cylinder thermostat", "hot water setting",
                "how hot should hot water", "how hot should the hot water",
                "how hot should my water", "what temperature should the hot water",
                "what temperature should my hot water", "what should the hot water be set to",
                "how hot should the water be", "hot water too hot", "hot water is too hot"),
               ("hot", "hotter", "temperature", "setting", "thermostat", "turn up", "dial",
                "degrees", "how hot", "what", "should", "celsius", "too hot", "scald")),
              "Sixty degrees on the cylinder thermostat is the number to aim for. A stored "
              "cylinder is held at 60 to 65C because below about 50C the bacteria behind "
              "Legionnaires' disease can multiply in the tank, and a thermostatic mixing valve on "
              "the outlet then brings it down to about 48C at the tap so nobody scalds. A combi "
              "has no tank, so set its hot water to 50 to 55C - hotter only burns gas and scales "
              "the plate heat exchanger faster. If the water comes out warm rather than cold, the "
              "setting is the thing to raise; if it starts hot and cools, the setting is fine and "
              "the fault is flow rate or a scaled exchanger.",
              avoid=("oven", "chicken", "meat", "pork", "turkey", "beef", "lamb", "sausages",
                     "roast", "bake", "bread", "dough", "sourdough", "yeast", "yoghurt", "yogurt",
                     "baby", "babies", "bath for the baby", "bottle", "formula", "breast milk",
                     "milk", "washing machine", "wash", "washing", "radiator", "radiators",
                     "heating", "kettle", "hot tub", "jacuzzi", "pool", "swimming", "thermometer",
                     "fever", "temperature of my child", "child", "children", "greenhouse",
                     "propagator", "germinate", "seeds", "compost", "room", "bedroom", "bed"),
              bias=1),
        entry("cold-tap-warm",
              (("cold tap", "cold taps", "cold water", "the cold water", "cold supply",
                "cold water is warm", "cold water runs warm", "cold water comes out warm",
                "cold water goes warm", "cold water is hot", "cold tap is warm",
                "cold tap runs warm", "cold tap is hot", "why is my cold tap warm",
                "why is the cold tap warm", "why is my cold water warm",
                "why is the cold water warm", "why is my cold water hot"),
               ("warm", "hot", "warmish", "lukewarm", "tepid", "not cold", "warm up", "warms up",
                "comes out", "runs", "why", "heating up", "boiling")),
              "A cold tap that runs warm is nearly always warm water getting into the cold pipe: a "
              "mixer tap or shower cartridge letting by, or a non-return valve that has failed, and "
              "in a house with a hot water cylinder a faulty mixing valve does the same. Feel the "
              "pipe under the sink - if it turns cold after a minute or two it is just the pipe run "
              "sitting warm in a cupboard, which is harmless; if it stays warm, have the check valve "
              "or cartridge replaced. If it is only the one tap, that tap is the culprit; if it is "
              "every cold tap, look at the cylinder, the mixing valve or the shared supply.",
              avoid=("shower", "showers", "pool", "swimming", "sea", "beach", "lake", "river",
                     "glass", "drink", "drinking", "bottle", "flask", "kettle", "hot water bottle",
                     "ice", "freezer", "fridge", "cooler", "hot tub", "jacuzzi", "radiator",
                     "radiators", "heating", "boiler", "overflow", "leak", "dripping",
                     "tap is dripping", "no hot water", "hot water", "hot tap", "hot taps",
                     "bath water", "washing"),
              bias=3),
        entry("heat-pump",
              (("heat pump", "heat pumps", "air source", "ground source", "heat pump work",
                "heat pump works", "what is a heat pump", "how do heat pumps work"),
               ("work", "works", "working", "how", "what", "explain", "worth", "idea", "good",
                "cost", "costs", "running", "cheaper", "replace", "boiler", "install", "noise",
                "loud", "cold", "any")),
              _heat_pump_answer,
              guard=_the_explainer_keeps_the_explainer,
              avoid=("car", "engine", "air conditioning", "fridge", "freezer", "microwave",
                     "washing machine", "dishwasher", "shower pump", "pool")),
        entry("batteries-in-the-bin",
              (("batteries", "battery", "old batteries", "used batteries", "aa", "aaa", "button cell",
                "lithium", "vape", "vapes", "disposable vape", "e-bike battery", "phone battery"),
               ("bin", "bins", "the rubbish", "rubbish bin", "in the rubbish", "trash",
                "throw", "throw away", "throwing", "dispose",
                "disposal", "recycle", "recycling", "kerbside", "where do i put", "get rid",
                "do with", "where do i take", "where can i take", "drop off", "chuck", "toss",
                "the tip", "to the tip", "recycling centre", "scrap")),
              ("Not the bin: batteries are a fire risk in a lorry and in the tip. Most supermarkets and "
               "every council recycling centre have a battery box by the door, and button cells and "
               "lithium ones go in those too, with the ends taped. Vapes, e-bike and scooter batteries "
               "and power banks are the ones that actually start fires, so take them to a shop that "
               "sells them or to the tip, never the kitchen bin."),
              avoid=("car battery", "car", "laptop wont charge", "phone wont charge", "remote",
                     "smoke alarm", "hearing aid", "flat battery")),
        entry("stopcock", (("stopcock", "stop cock", "stop tap", "stop valve", "shut off valve",
                            "shutoff valve", "water valve", "mains valve", "isolation valve",
                            "water main", "mains water", "water meter", "turn the water off",
                            "turn off the water", "turn the water back on", "shut the water off"),
                           ("where", "find", "located", "how", "what", "turn", "shut", "off", "water",
                            "under the sink", "outside", "emergency", "leak", "leaking")),
              "It is usually under the kitchen sink where the cold main comes up, or in a box near the "
              "boundary outside, and it is a brass tap that closes clockwise: turn it a quarter turn at "
              "a time, run the cold tap to check it has stopped, and turn it back anti-clockwise "
              "afterwards. If it is seized, don't force it with a wrench - a rounded stopcock means "
              "turning the water off at the road, which is the water company's job.",
              avoid=("worth", "worth it", "cheaper", "save", "saves", "saving", "expensive", "cost",
                     "costs", "how much", "should i", "should we", "leak", "leaks", "leaking",
                     "recommend", "recommended", "recommendation", "recommendations",
                     "any point in", "any point to", "waste of money", "worth having",
                     "leaked", "drip", "dripping", "broken", "faulty", "frozen", "read my meter",
                     "meter reading", "smart meter",
                     "gas shut off", "gas shutoff", "gas valve", "gas stop", "gas meter",
                     "gas supply", "gas pipe", "gas leak", "smell gas",
                     "get a water meter", "get a meter", "getting a meter", "have a meter fitted",
                     "fit a meter", "fit a water meter", "install a meter", "free meter",
                     "switch to a meter", "ask for a meter", "water meter save",
                     "water heater", "water heaters", "immersion", "immersion heater",
                     "hot water tank", "hot water cylinder", "water tank", "heater", "heaters",
                     "cylinder", "hot water"),
              bias=1),
        entry("radiator-off",
              (("radiator", "radiators", "rad", "rads", "trv", "thermostatic valve",
                "radiator valve", "towel rail"),
               ("turn off", "turning off", "switch off", "switching off", "shut off",
                "shutting off", "turn it off", "switch it off", "turn them off",
                "off for the summer",
                "off for summer", "off in the summer", "not using that room", "spare room",
                "radiator off", "radiators off", "rad off", "rads off",
                "turn a radiator off", "turn the radiator off", "turn my radiator off",
                "switch a radiator off", "switch the radiator off", "shut a radiator off",
                "turn both radiators off")),
              "Turn the thermostatic head on the radiator down to 0 or to the snowflake, which is "
              "frost protection rather than fully off, and leave it there: that closes the valve "
              "against the room and the radiator goes cold the next time the heating runs. If it has "
              "an old wheel valve instead of a numbered head, turn it clockwise until it stops - the "
              "same valve a plumber would close - and turn both ends if you are taking the radiator "
              "off the wall. Don't shut the valves on a radiator in a room that gets damp or near "
              "freezing, because that is the one that needs the frost setting.",
              bias=1,
              avoid=("leak", "leaking", "leaked", "drip", "dripping", "puddle", "bleed", "bled",
                     "cold", "noise", "noisy", "banging", "gurgling", "paint", "painting",
                     "strip", "removing", "bill", "bills", "save", "cheaper", "cost", "boiler",
                     "how long", "radiator key", "hot water")),
        entry("radiator-leak",
              (("radiator", "radiators", "rad valve", "trv", "thermostatic valve", "towel rail",
                "valve", "valves", "lockshield", "bleed valve"),
               ("leak", "leaks", "leaking", "leaked", "leaky", "drip", "dripping", "weeping",
                "water", "puddle", "wet", "rusted", "rusty", "seeping")),
              "Turn both radiator valves off and put a towel and a bowl under it, then see whether the "
              "water comes from the valve nut or the radiator itself: a drip at the nut often stops "
              "with a quarter turn of a spanner on the gland, while water from the panel or a rusty "
              "seam means the radiator has gone and wants replacing. Don't overtighten a joint that is "
              "held by plastic pipe, and if the water is coming through the ceiling, turn the heating "
              "off and ring a plumber today.",
              bias=1,
              avoid=("buy", "best", "which", "cheapest", "size", "how many", "bleed", "bled", "cold",
                     "bottom", "noise", "banging", "boiler", "landlord", "tenant",
                     "water heater", "immersion", "immersion heater", "hot water tank",
                     "hot water cylinder", "water tank", "cylinder", "tank",
                     "hot water is on", "hot water comes on", "comes on when", "by itself")),
        entry("outside-drain", (("outside", "gully", "yard", "driveway", "pavement", "garden"),
                                ("drain", "blocked", "smell", "overflowing", "flooding")),
              ("Lift the drain cover and clear the gully of leaves and silt with gloves and a trowel, "
               "then flush it with a bucket of water. If it's still slow or smells after that, or it's "
               "the main sewer, ring your water company: blocked public sewers are usually their job and "
               "free to clear.")),
        entry("sharpening-scissors",
              (("scissors", "scissor", "kitchen scissors", "paper scissors", "safety scissors"),
               ("sharpen", "sharpening", "sharpened", "blunt", "dull", "wont cut", "won't cut",
                "doesnt cut", "doesn't cut", "dont cut", "don't cut", "not cutting", "cut properly",
                "jamming", "sticks", "tight")),
              "Look at the edge first: a serrated kitchen pair cannot be sharpened at all, and a "
              "smooth pair is done with a fine diamond file or a small whetstone, five or six light "
              "strokes along the bevelled side only, at the angle the bevel already has, then wipe the "
              "burr off with the flat of the stone. A stiff screw is usually the pivot, not the blade: "
              "a drop of oil and a quarter turn on the nut frees it. If the two blades no longer meet "
              "along their length, a repair shop re-grinds them for a few pounds, which is cheaper "
              "than a good new pair.",
              avoid=("hair", "haircut", "cut my hair", "cut my own hair", "fringe", "topiary",
                     "hedge", "hedges", "lawn", "garden", "shears", "secateurs", "burglar",
                     "run with")),

        entry("paddling-pool",
              (("paddling pool", "paddling pools", "inflatable pool",
                "blow up pool", "blow-up pool", "paddling"),
               ("empty", "emptying", "emptied", "drain", "draining", "get rid", "tip", "tip out",
                "pour away", "water", "clean", "cleaning", "clean out", "store", "storing",
                "put away", "chlorine", "chlorinated", "how often", "change the water", "fill",
                "filling", "fill up")),
              "A paddling pool holds 300 to 800 litres, so buckets are the hard way: pull the drain plug "
              "if it has one, or lift one side and let it run into a drain or a big bucket, or hook a "
              "short hose over the lowest edge and syphon it out. Water that has only had children in "
              "it can go on the flower beds rather than the lawn, but water with chlorine or soap in it "
              "should go down a drain, since it scorches grass. Scrub the inside with hot soapy water, "
              "rinse, dry it in the sun and store it folded and dry, because a pool put away wet comes "
              "out black and slimy next summer.",
              avoid=("swimming pool", "hotel", "lido", "leisure centre", "pool table", "pool cue",
                     "gene pool", "pool car", "football pool", "car pool")),
        entry("hot-tub-care",
              (("hot tub", "hot tubs", "hottub", "jacuzzi", "spa bath"),
               ("empty", "emptying", "emptied", "drain", "draining", "drained", "pump out",
                "pump it out", "siphon", "syphon", "change the water", "changing the water",
                "how often", "clean", "cleaning", "cleaned", "clean out", "flush", "flush out",
                "water out", "get the water out", "wont drain", "won't drain", "not draining",
                "change the water in a hot tub", "change the water in my hot tub",
                "change the water in the hot tub", "change the hot tub water",
                "empty the hot tub", "drain the hot tub")),
              "Change the water every three to four months, or after about thirty uses, whichever "
              "comes first: a 4 to 6 person tub holds 1,000 to 1,500 litres, so check the level weekly "
              "with the hose and the chemicals, and do a full change when the water stops holding "
              "chlorine. To empty, hook a hose on the drain valve at the bottom into a drain, or drop a "
              "sump pump in, because a tub of chlorinated water kills the lawn and burns a border. "
              "Then flush the pipes with a line cleaner, wipe the shell with bicarbonate of soda rather "
              "than a detergent, and refill through the filter.",
              avoid=("bath", "baths", "bathtub", "shower", "paddling pool", "swimming pool",
                     "too hot", "how hot", "temperature", "pregnant", "pregnancy", "safe",
                     "safety", "heat rash", "warms up", "warm up time", "electrics", "electric",
                     "buying", "buy a", "worth it", "cost to run", "running cost", "cheap to run",
                     "cover", "lid", "steps", "chemcial", "chlorine level")),
        entry("empty-a-big-container",
              (("water butt", "water butts", "rain barrel", "rain butt",
                "pond", "ponds", "garden pond", "wildlife pond", "swimming pool", "swimming pools"),
               ("empty", "emptying", "emptied", "drain", "draining", "drained", "get the water out",
                "water out", "tip out", "tip it", "pump out", "pump it out", "siphon", "syphon",
                "get rid of the water", "hose out", "flush out",
                "empty a water butt", "empty the water butt", "empty my water butt",
                "drain a water butt", "drain the water butt", "empty a pond", "empty the pond",
                "empty my pond", "drain a pond", "drain my pond", "empty a swimming pool",
                "empty the swimming pool", "empty my swimming pool", "drain a swimming pool")),
              "Run it to a bed or a drain, never the road, and let the size decide how: a water butt "
              "goes out of the tap at the bottom onto a hose, and a barrel with no tap is tipped on "
              "its side or syphoned with a hose kept full of water. A pond is emptied in autumn, not "
              "spring, when frogs and newts are in it: net the fish into buckets of pond water, keep "
              "the filter media wet in that water, and put the plants in a tray, because it goes back "
              "within a day. A swimming pool is "
              "20,000 litres or more, so it is a hired pump and a drain or a tanker, never the garden "
              "hose, and never the road drain without asking the council first.",
              avoid=("watering can", "irrigation", "sprinkler", "hose pipe ban", "fill", "filling",
                     "fill it", "install", "installing", "fit a", "fitting a", "diverter",
                     "lengths", "lanes", "front crawl", "backstroke", "breaststroke", "lessons",
                     "learnt to swim", "learn to swim", "swim for fitness", "times a week",
                     "pool table", "pool cue", "hotel", "lido", "leisure centre", "gene pool",
                     "car pool", "fish tank", "aquarium", "toilet", "cistern", "radiator",
                     "boiler", "central heating", "header tank", "oil tank", "septic tank",
                     "caravan", "motorhome", "camper", "boat", "yacht", "narrowboat", "canal",
                     "van", "campervan")),
        entry("drain-blocked", (("drain", "shower", "shower tray", "bath", "plughole", "plug hole",
                                "sink", "basin", "handbasin", "washbasin", "tub", "bathtub"),
                                ("blocked", "blockage", "slow",
                                 "slowly", "draining", "drains", "drain", "clogged", "clog",
                                 "clogs", "clogging", "clogged up", "unclog", "unclogging",
                                 "unclogged",
                                 "so long to drain", "long to drain", "takes ages",
                                 "taking ages", "takes ages to drain", "ages to drain",
                                 "smells", "smell", "clear", "unblock",
                                 "choked", "choking", "chokes",
                                 "backed up", "not draining", "won't drain", "wont drain",
                                 "isnt draining", "isn't draining", "doesnt drain", "doesn't drain",
                                 "fills with water", "filling with water", "fills up", "filling up",
                                 "keeps filling", "keeps filling with water", "water sits",
                                 "sits in the", "pooling", "pools", "puddle in", "wont empty",
                                 "won't empty", "not emptying", "goes down slowly",
                                 "drains slowly", "slow to drain", "standing water",
                                "hair", "hairs",
                                "smelly", "stinks", "stink", "put down", "pour down",
                                "drain cleaner", "through the drain", "down the drain")),
              ("Pull the hair and soap out of the trap first (a bent wire or tweezers does it), then "
               "pour a kettle of hot water down with a spoonful of bicarbonate of soda and vinegar; a "
               "plunger over the plughole clears the rest. Skip the chemical cleaner until last, and "
               "fill the trap with a hair collector so it does not come back. The reason is hair, "
               "soap and grease caught in the trap and the bend."),
              avoid=("outside", "gully", "driveway", "street", "pavement", "machine",
                     "washing machine", "dishwasher", "dryer", "washer", "freezer", "fridge",
                     "toilet", "toilets", "cistern", "ball valve", "ballcock", "tank", "loft",
                     "boiler", "radiator", "radiators", "central heating", "header tank",
                     "paddling pool", "swimming pool", "hot tub", "water butt", "garden pond")),
        entry("down-the-drain",
              (("down the drain", "down the sink", "down the plughole", "down the plug hole",
                "down the toilet", "down our drain", "down my drain", "into the drain",
                "into the sink", "flush", "flushed", "flushing", "down the loo"),
               ("can i", "could i", "should i", "is it ok", "is it okay", "ok to", "okay to",
                "safe", "safe to", "allowed", "what can i", "what should i", "what shouldnt i",
                "what should not", "anything", "never", "not to", "which things", "what things")),
              "Four things never go down a drain: fat, oil and grease (they cool, set and make "
              "fatbergs), wet wipes even the ones marked flushable, anything that swells or sets - "
              "rice, pasta, potatoes, flour, eggshells and pastry scraps go down soft and pack hard "
              "a metre along - and paint, thinner and the chemicals that go with them. Fat goes into "
              "a jar or the bin, wipes and grounds into the bin, rice and peelings into the food "
              "waste with a sieve in the plug for the last rinse. A toilet takes the three Ps and "
              "nothing else: pee, poo and paper. Soapy water, tea, milk and small crumbs are fine.",
              avoid=("blocked", "blockage", "backed up", "wont drain", "won't drain",
                     "not draining", "smells", "smelly", "clear", "unblock", "plunger",
                     "washing machine", "dishwasher", "dryer", "machine", "boiler", "radiator",
                     "freezer", "fridge", "oil out", "pour old", "old oil", "recycle",
                     "bleach", "bleaches", "caustic", "coffee ground", "used coffee",
                     "spent coffee", "coffee grouts",
                     "keeps flushing", "constantly", "all night", "all day", "wont stop",
                     "won't stop", "keeps running", "running", "dripping",
                     "roasting tin", "roasting tray", "roasting pan", "baking tray",
                     "kitchen paper", "wipe the fat", "fat from the"),
              bias=3),
        entry("wash-cycle-time",
              (("washing machine", "washer", "washing", "wash"),
               ("how long", "take so long", "takes so long", "so long", "hours", "an hour",
                "cycle", "cycle time", "wash cycle", "washing cycle", "long cycle", "eco",
                "quick wash", "30 minute", "15 minute", "how many minutes", "duration",
                "length of a cycle", "normal wash", "cotton wash", "eco wash", "express wash",
                "spin", "spin cycle", "rinse cycle", "drain cycle", "programme", "program")),
              "Most cycles are two to three hours on eco and about an hour on a normal 40C cotton "
              "wash, and nothing is wrong: eco runs the drum slowly and heats the water slowly so it "
              "uses less electricity, which is why the eco label says 3 hours plus. The quick washes "
              "are 15 to 30 minutes and are meant for a small, lightly worn load. A cycle that runs "
              "longer than the dial says is usually a cold fill taking ages, a blocked filter, or "
              "extra rinses switched on, so check the filter and the rinse setting before calling "
              "anyone.",
              avoid=("dishwasher", "tumble dryer", "dryer", "oven", "last", "lasts", "lasting",
                     "lifespan", "life span", "life expectancy", "replace", "often",
                     "car", "cars", "van", "bike", "bicycle", "motorbike", "dog", "dogs", "pet",
                     "hair", "hands", "face", "dishes", "windows", "walk", "run", "running",
                     "swim", "swimming", "gym", "exercise", "ill", "sick", "cold", "flu",
                     "cycle to work", "cycle ride", "bike ride", "ride to work",
                     "pan", "pans", "wok", "skillet", "saucepan", "pots", "cookware",
                     "washing up", "wash the pan", "before washing",
                     "washing machine repair", "washer repair", "machine repair",
                     "repair man", "repairman", "engineer", "call out", "callout",
                     "spare part", "spare parts",
                     "to dry", "dry indoors", "dry inside", "drying indoors", "drying inside",
                     "to dry it", "hang out", "hanging out", "on the line", "air dry"),
              ask=("how long", "so long", "hours", "cycle", "take", "takes", "duration"),
              guard=_not_a_machine_that_has_gone,
              bias=4),
        entry("washing-outside",
              (("washing", "washing line", "laundry", "clothes", "wash", "the whites",
                "my whites", "our whites", "whites dry", "whites out", "sheets",
                "towels", "the bedding", "my bedding", "bedding dry"),
               ("hang", "hanging", "out", "outside", "line", "dry", "drying", "dried", "today",
                "tomorrow", "outside today", "put out", "airing", "airer", "weather", "rain",
                "raining", "wind", "windy", "sun", "sunny", "frost", "cold", "winter", "summer",
                "dryer", "tumble")),
              "A dry, breezy day dries a normal load outside in two to four hours, and a cold sunny "
              "day with wind is nearly as good as a warm one, so 8C and breezy beats 20C and still. "
              "Rain, fog and damp evening air put the water back, so bring it in before dusk. In "
              "winter, spin it an extra five minutes, then dry it indoors on an airer with a window "
              "open a crack: the water has to go somewhere, and an open window is cheaper than the "
              "heating.",
              avoid=("stain", "stains", "stained", "staining", "spot", "spots", "marked",
                     "blood", "grass", "red wine", "wine", "coffee", "tea", "ink", "mud",
                     "vomit", "sick", "bleach", "bleached", "yellow", "yellowed", "sweat",
                     "grease", "oil", "curry", "tomato", "chocolate", "pen", "marker",
                     "out of a white", "out of my white", "out of the white", "out of whites",
                     "washing machine", "washer", "not spinning", "wont spin", "won't spin",
                     "smell", "smells", "smelly", "musty", "mould", "mold", "leak", "leaking",
                     "drain", "filter", "cycle", "programme", "program", "eco wash", "spin speed",
                     "broken", "repair", "error code", "fault",
                     "come out", "comes out", "came out", "coming out", "get out", "got out",
                     "getting out", "remove", "removing", "dirty", "smell out",
                     "stain", "stains", "stained", "sweat", "sweaty", "ink", "blood", "grass",
                     "grease", "oil", "sauce", "coffee", "tea stain", "wine", "mud", "makeup",
                     "deodorant", "bleach mark"),
              guard=_not_a_drying_inside_question,
              bias=3),
        entry("washing-machine-smell", ("washing machine", ("smell", "musty", "smelly", "clean",
                                                            "smells")),
              "Run a hot 60C or 90C service wash with a washing-machine cleaner or a cup of "
              "bicarbonate of soda, and clean the filter and the detergent drawer while it runs. The "
              "smell lives in damp lint and detergent trapped in the seal, the drawer and the filter. "
              "The wash itself is about two hours. Leaving the door and drawer open between washes "
              "is what stops the smell coming back."),
        entry("washing-machine-mould",
              (("washing machine", "washer", "washing mashine", "washer dryer", "tumble",
                "laundry", "drum", "detergent drawer", "door seal"),
               ("mould", "mold", "mouldy", "moldy", "mildew", "black mould", "black mold",
                "smells of mould", "smell of mould", "smells mouldy", "spores", "drawer",
                "detergent drawer", "seal", "door seal", "rubber",
                "get rid", "rid of", "remove", "removing", "kill", "coming back",
                "keeps coming back")),
              ("The black comes back because it lives in the fold of the rubber door seal, so that is "
               "the bit to clean: pull the seal open, wipe the fold with a cloth and a little white "
               "vinegar or a mould spray, and dry it. Then run the hottest empty wash the machine has "
               "with a machine cleaner or a cup of bicarbonate of soda, clean the detergent drawer and "
               "the filter out, and leave the door and the drawer open between washes so the drum "
               "dries. Use liquid detergent rather than powder at low temperatures and stop leaving "
               "wet washing in the drum. A seal that is black right through and slimy will not clean "
               "up: it is a cheap part and an easy swap."),
              avoid=("leak", "leaking", "puddles", "wont drain", "won't drain", "not draining",
                     "wont spin", "banging", "noisy", "error code",
                     "fridge", "freezer", "oven", "dishwasher", "microwave", "fridge freezer",
                     "damp", "musty", "damp smell", "smells of damp", "smells musty",
                     "clean the filter", "cleaning the filter", "clean out the filter",
                     "empty the filter", "unblock the filter", "clear the filter"),

              bias=1),
        entry("washing-machine-not-heating",
              (("washing machine", "washer", "washer dryer", "washing mashine", "wash cycle",
                "wash", "machine"),
               ("not heating", "isnt heating", "isn't heating", "not heat", "doesnt heat",
                "doesn't heat", "didnt heat", "didn't heat", "wont heat", "won't heat",
                "not getting hot", "isnt getting hot", "isn't getting hot", "wont get hot",
                "won't get hot", "cold wash", "stays cold", "water stays cold", "stone cold",
                "no hot water", "heat", "heating")),
              "Check the programme first: a 30C or a cold wash never heats much, and many machines "
              "have a cold-only option that stops the element coming on. If it is a hot programme and "
              "the door glass is still cold after twenty minutes, the element is the usual cause - a "
              "cheap part that an engineer swaps in half an hour - and the thermostat that reads the "
              "water or the relay on the board are the next two. A machine that heats on some "
              "programmes but not others is a board fault, not the element.",
              avoid=("tumble dryer", "tumble drier", "dryer", "drier", "dishwasher", "dish washer",
                     "radiator", "radiators", "boiler", "central heating", "house", "shower",
                     "tap", "taps", "immersion", "hot tub", "not draining", "wont drain",
                     "won't drain", "blocked", "clogged", "full of water", "smells", "smelly",
                     "buy", "which", "best", "cheapest", "price", "worth it", "filter")),
        entry("washing-machine-leak",
              (("washing machine", "washer", "washer dryer", "washing mashine"),
               ("leak", "leaking", "leaks", "leaked", "puddle", "puddles", "water", "dripping",
                "flooding", "on the floor", "all over the floor", "under the machine",
                "underneath the machine", "under it")),
              "Stop the cycle, unplug it and turn the water off at the valve behind it, and leave it off "
              "until the leak has stopped. Water at the front is usually the door seal or the filter cap, "
              "water underneath is the pump or a loose inlet or drain hose, so check the hose "
              "connections before you call anyone. A leak from inside the machine itself is an "
              "engineer's job.",
              guard=_the_leak_is_a_machines,
              bias=2,
              avoid=("buy", "which", "best", "cheapest", "washing machine buy",
                     "wont drain", "won't drain", "not draining", "empty", "emptying",
                     "wont empty", "won't empty", "full of water", "water in the bottom",
                     "standing water", "sitting in the bottom", "sitting in", "sitting water",
                     "holding water", "holds water", "filter", "pump")),
        entry("boiler-age",
              (("boiler", "boilers", "combi", "central heating"),
               ("how long", "last", "lasts", "how old", "old", "years", "15 years", "age", "die",
                "dying", "on its way out", "end of its life", "replace", "replacing", "replacement",
                "new boiler", "worth", "efficient", "efficiency", "lifespan", "life span",
                "how much longer", "keep going", "go on for")),
              ("A boiler is built for about 10 to 15 years, so at 15 it is at the end of its life even "
               "if it is working today - the useful thing now is to have the money ready rather than "
               "be without heat in January. Get it serviced, keep the service record, and start "
               "collecting two or three quotes in the quieter months, because a combi swap is roughly "
               "2,000 to 3,000 pounds fitted and it is the same job whether you are desperate or not. "
               "A modern condensing boiler is around 90 per cent efficient against 70 to 80 for an "
               "old non-condensing one, which is the part of the bill you get back; a well-kept "
               "boiler that still works does not have to be replaced on age alone, but plan for it "
               "rather than wait for the morning it dies."),
              avoid=("broken", "broke", "leak", "leaking", "pressure", "no hot water", "no heating",
                     "noise", "noisy", "kettling", "error", "fault", "reset", "not firing",
                     "wont fire", "service", "serviced", "servicing", "annual", "insurance", "cover",
                     "radiator", "radiators", "thermostat", "timer", "smart",
                     "heat pump", "heat pumps", "air source", "ground source") + JOB_GUARD,
              bias=1),
        entry("swap-time",
              (("boiler", "boilers", "combi", "central heating", "fridge", "fridge freezer",
                "freezer", "washing machine", "washer dryer", "tumble dryer", "dishwasher",
                "oven", "cooker", "hob", "radiator", "radiators", "shower", "shower pump"),
               ("new", "new one", "fit", "fits", "fitting", "fitted", "swap", "swaps", "swapping",
                "replace", "replaces", "replacing", "replacement", "install", "installs",
                "installed", "installation")),
              "Fitting a new one is the long job, not the short one: an hour or two for a washing "
              "machine or a dishwasher, about an hour a radiator once the system is drained, and a "
              "boiler is the big one - usually a full day plus the gas check at the end. Ask when you "
              "book whether the price includes taking the old one away, the gas safety check and any "
              "making good, because those are the parts that turn a quote into a bigger bill.",
              ask=("how long", "long does", "how many days", "how many hours", "days", "hours",
                   "wait", "time", "take", "takes", "taking", "long will"),
              avoid=("last", "lasts", "lasting", "years", "lifespan", "how old", "cost", "costs",
                     "much", "price", "prices", "quote", "quotes", "cheap", "cheaper", "expensive",
                     "worth", "pay", "broken", "broke", "dead", "leak", "leaking", "no hot water",
                     "no heating", "pressure", "fault", "error", "not working", "stopped", "reset",
                     "noise", "noisy", "kettling", "service", "serviced", "servicing", "annual") ,
              bias=1),
        entry("repair-time",
              (("boiler", "boilers", "combi", "central heating", "fridge", "fridge freezer",
                "freezer", "washing machine", "washer dryer", "tumble dryer", "dishwasher",
                "oven", "cooker", "hob", "radiator", "radiators", "shower", "shower pump",
                "hot water", "heating", "electrics", "electrician", "plumber", "tradesman"),
               ("repair", "repairs", "repaired", "fix", "fixes", "fixed", "fixing", "install",
                "installs", "installed", "installation", "engineer", "plumber", "call out",
                "callout", "call-out", "come out", "coming out", "swap", "swapping", "job")),
              "Most jobs are done in one visit: an hour or two on site for a repair, and the wait is "
              "usually the part, so if something has to be ordered expect a few days between the "
              "first call and the fix. Ask when you book whether the price covers the first hour and "
              "whether the part is included, and get the call-out fee before anyone comes out. A "
              "boiler swap is the long one - usually a full day, plus the gas check afterwards.",
              ask=("how long", "long does", "how many days", "how many hours", "days", "hours",
                   "wait", "time", "take", "takes", "taking", "long will"),
              avoid=("service", "serviced", "servicing", "annual", "cost", "costs", "much", "price",
                     "prices", "quote", "quotes", "cheap", "cheaper", "expensive", "worth", "pay",
                     "broken", "broke", "dead", "leak", "leaking", "no hot water", "no heating",
                     "pressure", "fault", "error", "not working", "stopped", "reset", "noise",
                     "noisy", "kettling", "last", "lasts", "lasting", "years", "lifespan"),
              bias=1),
        entry("boiler-broken", ("boiler", ("broken", "break", "breaks", "broke", "dead", "not working",
                                            "packed in", "packed up", "packing in", "has packed",
                                            "given up", "gave up", "conked out", "conk out",
                                            "on the blink", "gone wrong", "playing up", "acting up",
                                            "knackered", "has died",
                                            "stopped", "repair", "repairing", "repairs", "fixing",
                                            "no hot water", "no heating", "noise", "noisy",
                                            "kettling", "reset", "not firing", "wont fire", "wont start",
                                            "wont come on", "firing", "cutting out", "cuts out",
                                            "cutting off", "locks out", "lockout", "shutting",
                                            "not responding", "thermostat", "morning", "fault",
                                            "error", "cold",
                                            "not heating", "isnt heating", "isn't heating",
                                            "heating the water", "heating water", "not hot",
                                            "switches itself off", "switching itself off",
                                            "turns itself off", "turning itself off",
                                            "keeps switching off", "keeps turning itself off",
                                            "not heating", "isnt heating", "isn't heating",
                                            "not getting hot", "not warming", "heating water",
                                            "heat water",
                                            "nothing happens", "does nothing", "nothing at all")),
              "Check the pressure gauge (1 to 1.5 bar), the thermostat and the boiler's reset button, "
              "and make sure the programmer is on the hour you think it is; a pressure top-up or a reset "
              "fixes a lot of no-heat mornings. The checks take ten minutes. In a cold snap, the white "
              "condensate pipe outside can "
              "freeze and stop the boiler, so pour warm water along it. If it locks out twice, or you "
              "smell gas, stop and call a Gas Safe engineer: gas is not a DIY job.",
              avoid=("landlord", "tenant", "letting agent", "rent", "deposit",
                     "quote", "quoted", "quotes", "estimate", "estimated", "invoice",
                     "kettle", "kettles", "boil a kettle", "tea", "coffee"),
              ask=("boiler", "heating", "hot water", "radiator", "radiators")),
        entry("no-heating",
              (("no heating", "heating is off", "heating gone off", "heating has gone off",
                "heating not working", "heating isnt working", "heating isn't working",
                "heating has stopped", "heating stopped", "heating wont come on",
                "heating won't come on", "heating wont fire", "heating won't fire",
                "heating is broke", "heating broke", "radiators are cold", "radiators cold",
                "radiators not hot", "radiators wont heat", "radiators won't heat",
                "heating is broken", "heating broken down", "heating has broken down",
                "heating is dead", "heating has died", "heating is bust",
                "heating is not working", "heating not coming on", "heating is not coming on",
                "heating isnt coming on",
                "heating isn't coming on", "heating wont turn on", "heating won't turn on",
                "central heating is not working", "central heating isnt working",
                "central heating has stopped working", "central heating has packed up",
                "thermostat is not working", "thermostat not working", "thermostat is broken",
                "thermostat broken", "room thermostat is not working",
                "no heat", "heating keeps going off",
                "heating keeps cutting out", "heating cuts out", "heating keeps turning off",
                "heating comes on and off", "heating has packed up",
                "heating has been broken", "heating has been off", "heating has been out",
                "heating has been dead", "heating has been cut off", "heating has been turned off",
                "heating is off", "heating hasnt worked", "heating hasn't worked",
                "heating has not worked", "heating hasnt been working", "heating hasn't been working",
                "heating has not been working", "heating stopped working", "heating isnt heating",
                "hot water has been off", "hot water has been out", "hot water has gone off",
                "hot water is off", "no hot water for", "no heating for", "no heating since",
                "heating has not come back on", "heating hasn't come back on"),
               ("heating", "radiator", "radiators", "boiler", "thermostat", "central heating",
                "room thermostat", "winter", "morning", "why", "fix", "check",
                "hot water",
                "rights", "what can i do", "who do i call", "get it sorted", "get it fixed")),
              ("Check the thermostat and the programmer first: a timer slipped to water only, a room "
               "stat turned down, or flat batteries in a wireless one are the commonest cold houses. "
               "Then look at the boiler's pressure gauge (1 to 1.5 bar cold) and top it up at the "
               "filling loop, and press reset once. In a cold snap the condensate pipe outside can "
               "freeze, so pour warm water along it. If it still will not fire, or you smell gas, "
               "that is a Gas Safe engineer."),          bias=1,
              avoid=("food", "reheat", "heatwave", "hot weather", "sun", "sunburn", "hayfever",
                     "my rights", "what are my rights", "my legal rights", "am i entitled",
                     "heating bill", "energy bill", "bill", "cost", "price", "cheap", "tariff",
                     "quote", "insulation", "car", "cars", "van", "engine", "microwave", "oven",
                     "saucepan", "water bottle", "hot water bottle", "electric blanket",
                     "microwave",
                     "motorhome", "camper", "caravan", "office", "workplace", "heating pad",
                     "heat pad", "underfloor", "greenhouse", "fish tank", "seat heater", "hot tub",
                     "car heater",
                     "baby", "babies", "newborn", "months old", "weeks old", "toddler",
                     "disabled", "disability", "carer", "frail", "elderly", "pensioner",
                     "health visitor", "in her 80s", "in his 80s", " is 85", " is 90", " is 95",
                     "over 80", "over 85", "over 90",
                     "turn off", "turning off", "turn it off", "turning it off", "off first",
                     "bleed", "bleeding", "bleed it", "radiator key",
                     "at the top", "at the bottom", "cold at the top", "hot at the bottom",
                     "top half", "boiler", "combi", "pressure", "gauge", "locks out", "lockout",
                     "fault code",
                     "how often", "how many times")),
        entry("boiler-callout", (("boiler", "heating", "hot water", "radiator", "radiators", "combi"),
                                 ("someone out", "someone in", "get someone", "call someone",
                                  "an engineer", "engineer", "callout", "call out", "tradesman",
                                  "worth getting", "worth paying", "worth a call")),

              "Yes for anything on the gas side, and the pressure gauge (1 to 1.5 bar) and the reset "
              "button are worth trying first. A Gas Safe engineer's callout is usually £60 to £120, "
              "and it is worth paying once a fault repeats rather than for a one-off reset. Note the "
              "make and model, the error code and what happens when it cuts out, because that is what "
              "turns a second visit into a first fix. If you smell gas, or water is leaking near the "
              "electrics, turn it off and call the emergency line.",
              avoid=("quote", "quoted", "estimate", "landlord", "tenant", "deposit", "how much",
                     "cost", "price", "cheapest", "install", "new boiler", "replace", "replace it",
                     "service", "serviced", "servicing", "safety check"),
              bias=2,
              guard=_a_visit_not_a_purchase,
              ask=("boiler", "heating", "hot water", "radiator", "radiators", "combi")),
        entry("landlord-damp",
              (("landlord", "landlady", "letting agent", "housing association", "council", "my fault"),
               ("damp", "damp patch", "damp patches", "damp walls", "mould", "mold", "mouldy", "moldy",
                "black mould", "black mold", "mildew", "condensation")),
              "Put it in writing with photos and dates, and ask them to find the cause rather than paint "
              "over it: a coat of paint is the one repair that makes damp come back. If they will not "
              "act, your council's environmental health team can inspect damp and mould as a hazard to "
              "health and make the landlord deal with it, and Shelter or Citizens Advice will help you "
              "write the letter free. Keep paying the rent and keep copies of everything you send. A "
              "window open for ten minutes a day and a dehumidifier hold it while you wait.",
              avoid=("evict", "evicted", "evicting", "eviction", "evictions", "section 21", "section 8",
                     "s21", "revenge", "kick me out", "kick us out", "throw me out", "throw us out",
                     "get rid of me", "notice to quit"),
              bias=1),
        entry("landlord-repairs", (("landlord", "landlady", "letting agent", "tenant", "tenants",
                                   "i rent", "im renting", "i'm renting", "we rent", "renting",
                                   "in my flat", "in the flat", "in our flat", "in my rented",
                                   "rented flat", "rented house", "rented home", "my rented",
                                   "the flat came with", "my rights", "what are my rights",
                                   "as a tenant", "my tenancy"),
                                   ("fix", "repair", "broken", "boiler", "refuse", "refuses", "ignore",
                                    "ignoring", "rights", "wont", "won't", "not fixing",
                                    "heating", "hot water", "oven", "washing machine", "washer",
                                    "dishwasher", "fridge", "freezer", "shower", "toilet",
                                    "does nothing", "doesnt do anything", "doesn't do anything",
                                    "not doing anything", "isnt fixing", "isn't fixing",
                                    "called back", "call back", "called me back", "hasnt called",
                                    "hasn't called", "havent called", "haven't called", "never called",
                                    "not called back", "still waiting", "chased", "chasing",
                                    "calls back", "phoned back", "not called", "no reply", "reply",
                                    "replied", "answers", "respond", "responded", "get back to me",
                                    "got back to me", "chase", "emails", "emailed", "email",
                                    "heard nothing", "ignores", "waiting", "keeps saying",
                                    "fobbed off",
                                    "has been broken", "have been broken", "be been broken",
                                    "broken for", "broken since", "broken weeks",
                                    "not been fixed", "hasnt fixed", "hasn't fixed", "not fixed",
                                    "not working", "stopped working",
                                    "responsibilities", "responsibility", "obligations",
                                    "obligation", "should fix", "has to fix", "have to fix",
                                    "must fix", "supposed to fix", "supposed to repair",
                                    "what must", "what do they have to", "what does he have to",
                                    "what does she have to")),          the_fault(
                  "Landlords have to do most repairs in a reasonable time, and anything that came with "
                  "the flat counts, appliances included, while something you brought with you is "
                  "yours to fix. Put it in writing, a text or email is fine, and keep a copy: \"Hi - "
                  "I reported the {fault} on [date] and nothing has been done. Please arrange a "
                  "repair within 14 days.\" If they ignore you, your council's environmental health "
                  "team or Shelter can push it along.",
                  "Put it in writing, a text or email is fine, and keep a copy. Name what is wrong "
                  "and when it started, say what you want done and ask for a date, then keep the "
                  "messages: landlords have to do most repairs in a reasonable time, and anything that "
                  "came with the flat, appliances included, counts, while something you brought with "
                  "you is yours to fix. If they ignore you, your council's "
                  "environmental health team or Shelter can push it along."),
              avoid=("deposit", "deposits", "selling", "sells", "sell", "sale", "sold",
                     "selling up", "on the market", "new owner", "new landlord",
                     "damp", "damp patch", "damp patches", "damp walls", "mould", "mold", "mouldy",
                     "moldy", "mildew", "condensation",
                     "flight", "flights", "plane", "airline", "airport", "overbooked", "train",
                     "trains", "rail", "railway", "bus", "coach", "hotel", "holiday", "package",
                     "restaurant", "parcel", "delivery", "concert", "festival", "gig", "ticket",
                     "tickets", "mobile contract", "phone contract", "broadband", "insurance",
                     "sacked", "redundancy", "dismissed", "employer", "boss",
                     "travel agent", "travel agents", "holidays", "insurance broker", "recruiter",
                     "recruiters", "interview", "estate agent", "sublet", "subletting", "guest",
                     "guests")),
        entry("withhold-rent",
              (("withhold", "withholding", "withheld", "hold back", "stop paying", "stopped paying",
                "refuse to pay", "refusing to pay", "not paying", "skip the rent", "skip a payment",
                "take it off the rent", "deduct", "deduct it", "rent reduction", "reduce the rent",
                "pay less rent", "rent free", "rent strike"),
               ("rent", "landlord", "landlady", "letting agent", "tenancy", "tenant", "repair",
                "repairs", "fixed", "fix", "damp", "mould", "boiler", "heating", "hot water")),
              "Not on your own, and not by simply stopping: stopping the rent is a breach of the "
              "tenancy, and the arrears are what gets tenants evicted, whatever the state of the "
              "boiler. Keep paying and do what does work - "
              "report it in writing with dates and photos, and ask the council's environmental health "
              "team to inspect, since for a serious hazard they can order the repair. Shelter or "
              "Citizens Advice will say free whether yours is one of the rare exceptions; get that in "
              "writing before you hold back a penny.",
              avoid=("deposit", "deposits", "rent increase", "raise the rent", "raise my rent",
                     "selling", "sell", "sale", "sold", "evict", "evicted", "eviction",
                     "section 21", "section 8", "buying", "mortgage", "car", "van", "garage",
                     "hire", "student loan", "mortgage payment",
                     "flatmate", "flatmates", "flat mate", "flat mates", "housemate", "housemates",
                     "house share", "house-share", "houseshare", "roommate", "roommates",
                     "lodger", "lodgers", "my tenant", "my tenants", "tenant", "tenants",
                     "sublet", "subtenant", "subtenant", "room to let"),
              ask=("withhold", "withholding", "withheld", "hold back", "stop paying", "stopped paying",
                   "refuse to pay", "refusing to pay", "not paying", "skip the rent",
                   "take it off the rent", "deduct it", "rent reduction", "reduce the rent",
                   "pay less rent", "rent strike"),
              bias=1),
        entry("landlord-says-fix-it-yourself",
              (("landlord", "landlords", "landlady", "letting agent", "letting agents",
                "letting agency", "housing association", "my tenancy"),
               LANDLORD_JOB_FITTINGS),
              LANDLORD_REPAIR_LETTER,
              bias=3,
              avoid=("deposit", "deposits", "selling", "sells", "sell", "sale", "sold", "evict",
                     "evicted", "eviction", "section 21", "notice to quit", "kick me out",
                     "throw me out", "rent increase", "raise the rent", "arrears",
                     "glass", "pane", "panes", "smashed", "shattered", "shards",
                     "broken window", "window is broken", "window was broken", "broke my window",
                     "broke the window", "put through", "board up", "boarded up"),
              ask=("fix", "fixed", "fixing", "repair", "repairs", "broken", "broke", "wont", "won't",
                   "will not", "refuses", "refusing", "refused", "ignores", "ignoring", "ignore",
                   "not fixing", "does nothing", "deal with", "sort out", "get it sorted")),
        entry("landlord-selling",
              (("landlord", "landlady", "letting agent"),
               ("selling", "sells", "sell", "sale", "sold", "selling up", "on the market",
                "new owner", "new landlord", "move out", "moving out", "leave", "leaving")),
              "A sale does not end your tenancy: the buyer takes the flat with you in it, your "
              "agreement carries on and your deposit stays protected. Keep paying the rent to your "
              "current landlord until they give you the new owner's details in writing, and keep the "
              "receipts. If they want you out for the sale, they still have to give you the notice "
              "your agreement and the law require - a sale is not notice - and a court order if you "
              "do not leave. Do not sign anything or hand back the keys without advice; Shelter or "
              "Citizens Advice will check the notice free.",
              avoid=("repair", "broken", "boiler", "damp", "mould", "deposit", "rent increase",
                     "raise the rent", "arrears", "buying", "buy", "mortgage", "house price",
                     "should i sell"),
              ask=("selling", "sells", "sell", "sale", "sold", "selling up", "on the market",
                   "new owner", "new landlord"),
              bias=2),
        entry("dishwasher", (("dishwasher", "dishwashers", "dish washer", "dish washers"),
                             ("smell", "clean", "greasy", "filter", "cloudy", "streaks",
                              "salty", "white film", "white marks", "white spots", "film",
                              "marks")),
              "Clean the filter at the bottom, wipe round the door seal, and run an empty hot cycle "
              "with a dishwasher cleaner or a bowl of white vinegar on the top rack. The problem is "
              "usually food and grease sitting in the filter and the door seal. Check the salt and "
              "rinse aid too: running out of either makes everything come out cloudy.",
              avoid=("my glasses", "spectacles", "specs", "frames", "lenses", "lens",
                     "prescription", "reading glasses")),

        entry("energy-use-up", (("energy", "electricity", "gas", "bill", "bills"),
                                 ("used more", "more than", "gone up", "doubled", "higher", "so high",
                                  "increased", "went up", "why so",
                                  "why is my", "why has my", "why did my", "why are my",
                                  "why does my", "why is the", "why has the")),
              ("Compare the reading on the bill with the numbers on your meter first: an estimated "
               "reading, often after a supplier change, is the commonest cause of a shock bill, and "
               "sending a real reading puts it right. After that it's usually the season (heating), the "
               "immersion or a heater left on, or a fridge or freezer seal failing, so read the meter "
               "once a day for a week with everything off and see what still ticks up."),
              avoid=("cut", "save", "reduce", "cheaper", "lower", "switch", "tariff", "deal",
                     "what can i do", "what do i do", "what should i do", "how can i", "how do i",
                     "spend less", "keep warm", "help",
                     "council tax", "tax", "water", "phone", "mobile", "broadband", "tv licence",
                     "licence", "rent", "insurance",
                     "sky", "sky tv", "sky bill", "satellite", "tv", "telly", "virgin", "virgin media",
                     "subscription", "subscriptions", "netflix", "spotify", "package",
                     "landline",
                     "split", "splitting", "split the bill", "earns", "earn", "income",
                     "salary", "wage", "wages", "50 50", "60 40", "more than me", "moved in")),
        entry("read-a-meter",
              (("gas meter", "electricity meter", "electric meter", "meter reading", "meter readings",
                "read the meter", "read my meter", "read our meter",
                "prepayment meter", "key meter", "token meter", "meter", "meters"),
               ("read", "reading", "how do i read", "how to read", "take", "taking", "submit",
                "send", "give", "which numbers", "which number", "digits", "numbers", "wrong",
                "estimated", "units", "how much")),
              "Read the black digits only and ignore anything after the decimal point or in red - those "
              "are the fractions of a unit, and a supplier only wants the whole numbers. A gas meter "
              "counts cubic metres if it says m3, or hundreds of cubic feet if it says ft3 on an older "
              "one, and the bill needs to agree which. An electricity meter may show one row of numbers, "
              "or two for day and night if you are on Economy 7: send both. Take a photo on the first of "
              "the month and send it in, because a reading you send beats an estimate.",
              avoid=("gone up", "so high", "higher", "expensive", "tariff", "switch", "cheaper",
                     "moving", "move out", "moving house", "landlord", "leak", "leaking", "smell",
                     "gas leak", "fault", "not working", "broken", "smart", "smart meter", "in credit",
                     "debt", "arrears", "pay", "payment", "how much do i owe", "top up", "topup"),
              ask=("read", "reading", "how", "take", "submit", "send", "which", "numbers", "digits",
                   "wrong", "units", "where"),
              bias=1),
        entry("smoke-alarm-number",
              (("smoke alarm", "smoke alarms", "detector", "detectors", "fire alarm"),
               ("how many", "number", "one per", "where", "need", "needed", "fit", "fitted", "install",
                "put up", "floors", "bedroom", "bedrooms", "hallway")),
              "One on every floor, one in the hallway outside the bedrooms, and one in the room with the "
              "boiler or the open fire - the hallway one matters most, because smoke in the stairs is "
              "what cuts off the way out. Fit sealed ten-year alarms so there is no battery to "
              "remember, and check the test button on each once a month.",
              avoid=("beep", "beeping", "chirp", "chirping", "noise", "keeps going off")),

        entry("smoke-alarm-test",
              (("smoke alarm", "smoke alarms", "detector", "detectors", "fire alarm"),
               ("check", "test", "testing", "how often", "monthly", "battery", "batteries", "replace")),
              "Press the test button once a month and change the battery once a year - the easy date is "
              "when the clocks change. Vacuum the dust out of the vents twice a year, and replace the "
              "whole alarm every ten years, because the sensor ages. Fit one on every floor and one in "
              "the hallway outside the bedrooms.",
              avoid=("beep", "beeping", "chirp", "chirping", "noise", "keeps going off", "smell",
                     "smoke coming", "fire started", "on fire", "burnt", "burning",
                     "how many", "number", "one per", "where should")),
        entry("smoke-alarm-beep", (("smoke alarm", "detector"), ("beep", "beeping", "chirp", "chirping",
                                                                 "noise", "keeps")),
              "A single chirp every minute or so means a low battery: change it now, don't wait. If it's "
              "a sealed ten-year alarm, replace the whole unit, and vacuum the dust out of the vents "
              "either way.",
              avoid=("cook", "cooking", "cooked", "toast", "toasting", "grill", "grilling",
                     "oven", "hob", "fry", "frying", "roast", "roasting", "bake", "baking",
                     "shower", "steam", "kitchen", "burning", "burnt")),
        entry("machine-takes", (TAKES_THINGS, ("how long", "take", "takes", "taking", "long", "time",
                                                "quick", "quickly")),
              _machine_takes,
              avoid=("last", "lasts", "lasting", "years", "lifespan", "life expectancy", "life span",
                     "repair", "repairing", "replace", "replacing", "broken", "not working", "fixed",
                     "engineer", "cost", "price", "electricity", "energy",
                     "cheapest", "cheaper", "cheap time", "best time", "what time", "off peak",
                     "off-peak", "economy 7", "tariff", "in the morning", "in the evening",
                     "during the day", "time of day",
                     "keep", "keeps", "keeping", "store", "stores", "storing", "stored", "storage",
                     "shelf life", "shelf-life", "go off", "goes off", "gone off", "still ok",
                     "still good"),
              bias=2),
        entry("fridge-not-cold",
              (("fridge", "freezer"), ("cold", "not cold", "not very cold", "not that cold",
                                       "wont get cold", "won't get cold", "warm", "freezing",
                                       "door seal", "door seals", "seal", "seals", "rubber seal",
                                                          "cool", "cooling",
                                                          "chill", "chilled", "chilling",
                                                          "stopped cooling", "not cooling",
                                                          "stopped getting cold", "not getting cold")),
              "Stand a fridge thermometer in a glass of water on the middle shelf and leave it "
              "overnight: the fridge wants 3 to 5C and the freezer -18C, and the dial's numbers are not "
              "degrees. A fridge that will not reach it wants the door seals checked - close the door "
              "on a sheet of paper and see if it slides out easily - and the coils at the back dusted. "
              "Don't overfill it either, because cold air needs space to move.",
              avoid=("how does", "how do fridges", "how it works", "explain",
                     "stopped working", "not working", "has stopped working", "have stopped working",
                     "stopped altogether", "dead",
                     "wont start", "won't start", "will not start", "not turning on", "no power",
                     "wont turn on", "won't turn on", "keeps tripping", "tripping the",
                     "the pot", "a pot", "the pan", "a pan", "the stew", "a stew", "the curry",
                     "the soup", "the casserole", "leftovers", "cool it down", "let it cool",
                     "let the pot", "let the pan", "before it goes in", "before putting it",
                     "cool right down", "cool down before",
                     "without a fridge", "without a freezer", "without refrigeration", "no fridge",
                     "no freezer", "power cut", "power outage", "camping", "cool box", "coolbox",
                     "ice box", "picnic",
                     "door not shut", "door not shutting", "door not close", "door not closing",
                     "door wont shut", "door wont close", "door wont stay shut", "wont stay shut",
                     "door keeps opening", "door keeps popping open", "door pops open",
                     "door swings open", "door gap",
                     "claim", "claims", "refund", "money back", "compensat", "who pays", "insurance",
                     "insured", "money back",
                     "not much else", "nothing else", "nothing much", "only", "dinner", "tea",
                     "supper", "lunch", "recipe", "recipes", "what can i make", "what can i cook",
                     "what should i make", "to cook"), bias=1),
        entry("cool-box-cold",
              (("cool box", "coolbox", "cooler box", "cool bag", "cooler bag", "ice box",
                "picnic bag", "picnic box", "chiller bag", "chiller box",
                "ice packs", "ice pack", "freezer blocks", "freezer block", "freezer packs",
                "freezer pack", "cool blocks", "cool pack"),
               ("cold", "cool", "keep", "keeps", "keeping", "stay", "stays", "warm", "all day",
                "picnic", "picnics", "drinks", "food", "beers", "milk", "day out", "beach", "trip",
                "car", "camping")),
              "A cool box only holds the cold you put in it. Freeze a couple of water bottles or "
              "ice packs the night before, because they do the work, and pack them around the food "
              "rather than on top. Fill the empty space with more cold drinks or a rolled-up towel: "
              "a half-empty box warms up fastest. Keep it out of the sun, out of a parked boot that "
              "gets hot, and put a towel or a folded blanket over the lid. Open it as little as you "
              "can and shut it straight after. Cold drinks and fruit keep all day like that; cooked "
              "food, milk and anything with mayonnaise is the one to throw away if it has sat warm "
              "for more than about two hours.",
              bias=1,
              avoid=("buy", "buying", "best", "which", "cheapest", "cheap", "price", "size",
                     "how big", "electric", "plug in", "recommend", "worth it",
                     "smell", "smells", "smelly", "stinks", "mould", "mold", "dirty", "wash")),
        entry("fridge-first-cold",
              (("fridge", "freezer", "fridge freezer", "refrigerator", "icebox"),
               ("get cold", "gets cold", "get colder", "getting cold", "cool down", "cools down",
                "cooling down", "get to temperature", "get down to temperature",
                "come down to temperature", "come to temperature", "reach temperature",
                "first switched on", "switched on", "switch it on", "putting food in",
                "put food in", "putting things in", "loading it", "how long before",
                "how long should i wait", "how long to wait", "wait before")),
              "A fridge comes down to temperature in about 4 hours empty and is steady at 4C after 24, "
              "so switch it on, let it run empty, then load it - a freezer wants about 24 hours to hold "
              "-18C. A thermometer in a glass of water tells you when it is ready, not the dial.",
              avoid=("not cold", "wont get cold", "won't get cold", "stopped getting cold",
                     "not getting cold", "not cooling", "stopped cooling", "broken"),
              ask=("how long", "long to", "how many hours", "how much time", "how long before",
                   "how long should", "how long do i"),
              bias=1),
        entry("oven-heat-up",
              (("oven", "ovens", "fan oven", "range cooker"),
               ("heat up", "heats up", "heating up", "warm up", "warms up", "warming up",
                "preheat", "pre-heat", "preheating", "come up to temperature",
                "get to temperature", "reach temperature", "long to heat", "takes to heat")),
              "Most ovens reach 180C in 10 to 15 minutes from cold, and a fan oven is quicker than a "
              "conventional one, so a 20-minute preheat covers nearly everything. Trust an oven "
              "thermometer over the dial - they are often 10 to 20C out.",
              avoid=("clean", "cleaning", "self cleaning", "pyrolytic", "smell", "smells", "smoke",
                     "pizza", "chips", "roast", "bake", "baking", "cake", "air fryer",
                     "not heating", "not heating up", "isnt heating", "isn't heating", "not working",
                     "wont heat", "won't heat", "stopped heating", "broken", "fault", "fuse"),
              ask=("how long", "long to", "how many minutes", "how much time", "how long before"),
              bias=1),
        entry("fridge-water-inside",
              (("fridge", "freezer", "refrigerator", "fridge freezer", "salad drawer", "crisper"),
               ("water", "wet", "puddle", "pools", "pooling", "collecting", "collects", "ice", "icy",
                "dripping", "drips", "leaking", "leak", "drawer", "bottom", "inside")),
              "Water in the bottom of a fridge is nearly always the drain hole at the back: it clogs "
              "with bits of food, so push a pipe cleaner or a piece of stiff wire down it and flush "
              "warm water through. Ice on the back wall means the fridge is running too cold, so turn "
              "the dial up a notch and let it defrost. If the water keeps coming back, check the door "
              "seal by closing the door on a sheet of paper - if it slides out easily, the seal is the "
              "fault.",
              bias=1,
              avoid=("buy", "best", "which", "cheapest", "size", "smells", "smell", "not cold",
                     "clean", "cleaning", "cleaned", "clean out", "wipe", "wipe out", "scrub",
                     "shelves", "shelf", "racks", "spills",
                     "not freezing", "noisy", "noise", "defrost", "frost free", "on the floor",
                     "outside", "washing machine", "dishwasher", "boiler", "kettle", "toilet",
                     "hot water bottle", "ice cubes", "ice tray", "drinking",
                     "keep water", "keeps water", "keep a jug", "jug", "bottle", "bottles",
                     "water bottle", "water bottles", "keep drinks", "keep juice", "cans",
                     "layer of ice", "ices up", "iced up", "ice builds up", "ice build up",
                     "ice build-up",
                     "ice on the walls", "walls of ice", "full of ice", "lots of ice",
                     "so much ice", "thick ice", "ice everywhere", "ice in the freezer",
                     "freezer has ice", "freezer with ice", "build up of ice",
                     "cost", "costs", "costing", "money", "bill", "bills",
                     "energy", "efficient", "efficiency")),
        entry("oven-door",
              (("oven", "cooker", "range cooker", "oven door"),
               ("door", "hinge", "hinges", "stiff", "sticking", "sticks", "hard to shut",
                "hard to close", "wont shut", "won't shut", "wont close", "won't close", "not closing",
                "drops", "dropped", "spring", "loose", "rub", "rubbing", "squeak", "squeaks")),
              "An oven door that is stiff or will not shut is nearly always the hinge: open it and "
              "look at the two arms at the bottom, because a bent arm or a hinge that has dropped "
              "makes the door rub on the frame. Check nothing inside has slipped forward first - a "
              "shelf or a tray stops the door a centimetre short - and wipe the burnt grease off the "
              "hinge area. If it still will not sit shut, hinges are a cheap part for most makes: take "
              "the model number off the sticker and order a pair.",
              bias=1,
              avoid=("clean", "cleaning", "glass", "smell", "burning", "not heating", "temperature",
                     "finger", "fingers", "thumb", "my hand", "hand in", "trapped", "caught",
                     "slammed", "burned", "burnt", "scalded",
                     "lock", "childlock", "child lock", "fan", "element", "pizza", "bread", "cake",
                     "how long", "how hot", "what temperature", "shelf position",
                     "landlord", "landlords", "landlady", "letting agent", "letting agency",
                     "my tenancy", "wont fix", "won't fix", "refuses to fix", "refusing to fix",
                     "grease", "greasy", "burnt", "burnt on", "food", "spill", "spilled",
                     "splatter", "splatters", "stain", "stains", "smear", "smears",
                     "rise", "rises", "risen", "rising", "prove", "proves", "proved", "proving",
                     "proof", "proofed", "dough", "sourdough", "loaf", "loaves", "yeast", "sponge",
                     "batter", "souffle", "soufflé", "pastry", "croissant", "meringue", "bake",
                     "bakes", "baked", "baking", "recipe")),
        entry("fridge-clean", (("fridge", "freezer"), ("clean", "cleaning", "cleaned", "wash", "wipe",
                                                      "shelves", "shelf", "scrub", "freshen", "hygiene")),
              "Empty it into a cool bag first, then wipe every shelf, drawer and the door seals with hot "
              "soapy water and dry them. Clear the drain hole at the back with a cotton bud and warm "
              "water, and leave a bowl of bicarbonate of soda on a shelf between cleans: it absorbs "
              "smells instead of covering them. Once or twice a year is enough if nothing has spilled."),
        entry("fridge-seal",
              (("seal", "seals", "rubber", "gasket", "magnet", "magnetic strip",
                "door not shut", "door not shutting", "door not close", "door not closing",
                "door not shut properly", "door not closing properly", "door doesnt shut",
                "door doesnt close", "door does not shut", "door does not close",
                "door wont shut", "door wont close", "door wont stay shut", "door wont stay closed",
                "door keeps opening", "door keeps popping open", "door pops open", "door swings open",
                "door swings back open", "wont stay shut", "door gap", "gap round the door"),
               ("fridge", "freezer", "refrigerator")),
              "Close the door on a sheet of paper and pull it out: it should drag, and a note that "
              "slides out easily at that spot is a gap. Wipe the seal with hot soapy water and dry it, "
              "because a sticky or crumpled seal often shuts fine once it is clean, then check the door "
              "hinge has not dropped. A split or hardened seal is a part: the model number is on a "
              "sticker inside the fridge, and a new one is usually £20 to £40 and pushes into the "
              "channel by hand.",
              avoid=("clean", "cleaning", "smell", "smells", "smelly", "stink", "ice", "frost",
                     "defrost", "freezing", "not cold", "warm", "noise", "humming", "rattling",
                     "slam", "hinge"),
              bias=2),

        entry("fridge-noise", (("fridge", "freezer", "refrigerator"),
                               ("hum", "hums", "humming", "buzz", "buzzing",
                                "rattl", "vibrat", "clunk", "gurgl", "ticking",
                                "clicking", "knock") + NOISE_WORDS),
              "The steady hum is the compressor, which switches on and off to hold the temperature: "
              "it is normal, and it gets louder when the room is warm or the door has just been shut "
              "on warm food. A rattle or a buzz is usually the fridge not sitting level, so wind the "
              "front feet down until it stands firm, and check nothing is touching the back. A clunk "
              "every few minutes, or a fridge that hums but never gets cold, is gas or the compressor "
              "and needs an engineer.",
              bias=1,
              avoid=("smell", "smells", "smelly", "stink", "stinks", "odour", "clean", "ice",
                     "frost", "defrost", "freezing", "food", "chicken")),
        entry("appliance-hum", (("washing machine", "washer", "dishwasher"),
                                ("hum", "hums", "humming", "whirr", "whirring", "whine", "whining",
                                 "buzz", "buzzing")),
              "A steady hum is the motor or the pump doing its job, and every machine has one. A hum "
              "that is new or louder is usually the machine standing uneven, something loose touching "
              "the case, or a filter or drain pump half blocked: level the feet, take the filter out "
              "and clean it, and check the drum or spray arm turns freely with the power off. A whine "
              "that rises with the speed is a bearing, which is a repair rather than a service.",
              bias=1,
              avoid=("tinnitus", "my ears", "in my ears", "ringing", "hearing", "smell", "smells",
                     "buy", "replace", "best", "worst", "wet", "dirty", "not draining", "wont drain",
                     "won't drain", "squeal", "squeals", "squealing", "rattle", "rattling", "bang",
                     "bangs", "banging", "shaking", "wont spin", "won't spin", "not spinning",
                     "boiler", "radiator", "puddle", "leak", "leaking")),

        entry("washer-noise", (("washing machine", "washer", "washer dryer", "spin"),
                               ("shake", "shakes", "shaking", "bang", "bangs", "banging",
                                "rattl", "vibrat", "walk", "walks", "jump",
                                "jumps", "thump", "thumping", "screech", "squeal",
                                "rattle", "rattles", "rattling", "vibrate", "vibrates")
                               + NOISE_WORDS),
              "A machine that bangs or walks across the floor is almost always an uneven load: stop "
              "it, undo the tangle, and put a couple of towels in with a single heavy thing like a "
              "duvet. If it does it on every spin, take the transport bolts out of the back (they stay "
              "in on a new machine and must come out), level the feet so it cannot rock, and check it "
              "is not touching a cupboard. A screech or a burning smell means the drum bearings or the "
              "belt, which is a repair.",
              avoid=("smell", "smells", "smelly", "musty", "drain", "drains", "empty", "water",
                     "filter", "buy", "replace", "worst", "best", "drum",
                     "grind", "grinds", "grinding", "scrap", "scrapes", "scraping",
                     "rumble", "rumbles", "rumbling", "roar", "roaring",
                     "screech", "screeching", "squeal", "squeals", "squealing",
                     "squeak", "squeaks", "squeaking", "rattle", "rattles", "rattling",
                     "clunk", "clunks", "clunking", "shriek", "shrieking")),

        entry("washer-sound",
              (("washing machine", "washer", "washer dryer", "washer-dryer", "drum", "spin"),
               ("grind", "grinds", "grinding", "scrap", "scrapes", "scraping", "rumble", "rumbles",
                "rumbling", "roar", "roaring",
                "squeak", "squeaks", "squeaking", "squeal", "squeals", "squealing", "screech",
                "screeching", "shriek", "shrieking",
                "rattle", "rattles", "rattling", "clunk", "clunks", "clunking")),
              _washer_sound_fault,
              bias=1,
              guard=_a_dryer_is_not_a_washer),

        entry("oven-fan-runs-on", (("oven", "cooker", "fan oven"),
                                   ("fan", "fans")),
              "A fan oven usually runs its cooling fan on after you switch off, sometimes for ten or "
              "twenty minutes, to pull the heat out of the casing: that is normal and it stops by "
              "itself. If it never stops, or starts again while the oven is cold, the thermostat or the "
              "fan switch has failed and it needs an engineer, and it is worth switching off at the "
              "wall until then.",
              bias=4,
              ask=("never", "stops", "stop", "keeps", "keeping", "runs", "running", "all the time",
                   "stays", "wont", "won't", "cold"),
              avoid=("clean", "cleaning", "gas mark", "bake", "cake", "roast", "bread", "temperature",
                     "dial", "degrees", "how long", "how hot")),

        entry("oven-glass",
              (("oven glass", "oven door glass", "glass door", "oven window", "oven door",
                "the glass on the oven", "inside of the oven door", "door of the oven"),
               ("clean", "cleaning", "cleaned", "greasy", "grease", "dirty", "smear", "smears",
                "streak", "streaks", "marks", "scrub", "wipe", "wash", "filthy", "stained")),
              "Spread a paste of bicarbonate of soda and water on the glass, leave it twenty minutes "
              "and wipe it off with a damp cloth; burnt specks lift with a plastic scraper or a razor "
              "blade held almost flat to the glass. Keep caustic oven cleaner off the rubber seal, and "
              "wipe the inside of the door too, because most of the brown film sits between the panes.",
              avoid=("hand", "hands", "finger", "fingers", "thumb", "arm", "arms", "wrist", "skin",
                     "scald", "scalded", "blister", "butter", "myself", "shelf", "shelves", "rack",
                     "racks", "stiff", "wont close", "won't close", "wont shut", "hinge", "smoke",
                     "smells", "smoking")),
        entry("oven-grill",
              (("oven grill", "the grill", "grill pan", "grill tray", "grill plate", "grills",
                "grill"),
               ("clean", "cleaning", "cleaned", "grease", "greasy", "scrub", "soak", "wash",
                "burnt", "stuck", "filthy", "dirty")),
              "Soak the grill pan and its rack in hot water with washing-up liquid and a couple of "
              "tablespoons of bicarbonate of soda, then lift the burnt bits with a nylon scourer. "
              "The element above it is not a thing to scrub: switch it off, let it cool, and wipe it "
              "with a damp cloth, and leave the self-clean lever for the whole oven.",
              avoid=("barbecue", "barbecues", "barbeque", "bbq", "bbqs", "barbie", "charcoal",
                     "coals", "garden", "outdoor", "outside", "steak", "steaks", "burger",
                     "burgers", "sausage", "sausages", "kebab", "halloumi", "how long", "recipe",
                     "marinade", "temperature", "cook", "cooking", "which", "buy", "buying",
                     "dishwasher filter", "oven racks", "oven shelves"),
              ask=("clean", "cleaning", "cleaned", "grease", "greasy", "scrub", "soak", "wash",
                   "burnt", "stuck", "filthy", "dirty"),
              bias=1),
        entry("oven-racks",
              (("oven racks", "oven rack", "oven shelves", "oven shelf", "wire racks", "wire rack",
                "grill rack", "grill racks", "rack in the oven", "racks in the oven",
                "shelves in the oven", "shelf in the oven"),
               ("clean", "cleaning", "cleaned", "grease", "greasy", "scrub", "wash", "soak",
                "burnt", "stuck", "filthy", "dirty")),
              "Lift them out and soak them in the bath or a big sink in hot water with a good squirt "
              "of washing-up liquid and a couple of tablespoons of bicarbonate of soda, for an hour "
              "or overnight: the burnt-on grease then comes off with a nylon scourer or foil. If they "
              "fit, a dishwasher does most of it, and a bin bag with a splash of ammonia left outside "
              "overnight lifts the worst without scrubbing.",
              avoid=("hand", "hands", "finger", "fingers", "thumb", "arm", "wrist", "scald",
                     "blister", "burnt my", "burned my", "wont fit", "won't fit", "broken",
                     "sagging", "wobbly", "wont sit", "won't sit", "fell", "falls", "loose",
                     "dishwasher not draining", "dishwasher filter", "wine", "spice", "spices"),
              ask=("clean", "cleaning", "cleaned", "grease", "greasy", "scrub", "wash", "soak",
                   "burnt", "stuck", "filthy", "dirty"),
              bias=1),
        entry("oven-clean", ("oven", ("clean", "cleaning", "grease", "greasy", "burnt", "smoke",
                                      "filthy", "dirty", "dirt", "grime", "grimy", "grubby",
                                      "stained", "stains", "scrub", "wipe", "ick", "disgusting")),
              "Make a paste of bicarbonate of soda and water, coat the inside (not the elements), leave "
              "it overnight and wipe it out with a damp cloth and a little vinegar. It takes some "
              "scrubbing but doesn't fill the kitchen with fumes like caustic oven cleaner. The racks "
              "soak in hot water with a dishwasher tablet while the paste works.",
              avoid=("hand", "hands", "finger", "fingers", "thumb", "arm", "arms", "wrist", "skin",
                     "scald", "scalded", "blister", "butter", "myself",
                     "fire", "fire risk", "catch fire", "dangerous", "danger", "safe", "unsafe",
                     "hazard", "a risk",
                     "glass", "panes", "pane", "window", "door glass"),
              ask=("clean", "cleaning", "cleaned", "cleaner", "grease", "greasy", "scrub", "wipe",
                   "smoke", "smokes", "smoking", "smells", "smell", "get off",
                   "burnt bits", "burnt on", "burnt stuff", "burnt grease", "use to clean",
                   "marks", "stains", "black", "stuck on", "scorched", "charred",
                   "filthy", "dirty", "grime", "filth", "grubby", "ick", "disgusting",
                   "is burnt", "burnt on the bottom", "burnt bottom", "burnt floor",
                   "oven floor", "inside is burnt", "is black", "burnt inside",
                   "burnt off", "off the bottom", "off the floor", "get rid of")),
        entry("oven-grease-risk",
              (("oven", "cooker", "grill", "hob", "air fryer", "cooker hood"),
               ("fire", "fire risk", "catch fire", "dangerous", "danger", "risk", "risky",
                "safe", "unsafe", "hazard", "hazardous")),
              "Yes, if it is greasy: a thick layer of grease and burnt crumbs on the base, the "
              "door seal or the grill pan is what catches, and it usually starts when a spill or a bit "
              "of foil drops onto the element the next time the oven is on. It does not go up on its "
              "own, so it is not an emergency tonight: clean the base and the seal when it is cold, "
              "keep the grill pan clear, and never leave a grill or a chip pan unattended. If it does "
              "catch, close the door, switch it off at the wall and smother the pan with a lid or a "
              "fire blanket - never water on a fat fire.",
              bias=2,
              ask=("dirty", "grease", "greasy", "greasy bits", "filthy", "grime", "grimy", "grubby",
                   "crumbs", "burnt", "stains", "stained", "disgusting")),
        entry("appliance-smoking",
              (_SMOKING_THING, ("smoke", "smokes", "smoking", "smoky", "smokey", "sparks",
                                "sparking", "scorch", "scorched",
                                "smells like burning", "smell of burning", "smells of burning",
                                "burning smell", "smells burning", "smell burning",
                                "smelt of burning", "smelt like burning", "smelt burning",
                                "smelled of burning", "smelled like burning", "smelling of burning")),
              _smoking_appliance,
              avoid=("hand", "hands", "finger", "fingers", "thumb", "arm", "arms", "wrist",
                     "skin", "scald", "scalded", "blister", "myself", "the house", "the flat",
                     "the kitchen", "hallway", "stairs", "bonnet", "chimney", "exhaust",
                     "barbecue", "bbq", "cigarette", "cigarettes", "joint", "weed",
                     "chiminea", "firepit", "fire pit",
                     "flames", "on fire", "caught fire", "alight", "ablaze", "blazing",
                     "pouring out", "billowing", "everywhere"),
              ask=("smoke", "smokes", "smoking", "smoky", "smokey", "sparks", "sparking",
                   "scorch", "scorched", "smells like burning", "smell of burning",
                   "smells of burning", "burning smell", "smells burning", "smell burning",
                   "smelt of burning", "smelt like burning", "smelt burning",
                   "smelled of burning", "smelled like burning", "smelling of burning"),
              bias=1),
        entry("smoke-alarm-nuisance",
              (("smoke alarm", "smoke detector", "fire alarm", "heat alarm", "alarm"),
               ("going off", "goes off", "keeps going off", "set off", "setting off", "triggered",
                "sounds", "sounding", "stop it", "silence it", "wont stop", "won't stop",
                "went off", "gone off")),
              _alarm_nuisance,
              avoid=("chirp", "chirping", "chirps", "battery", "batteries", "beep every",
                     "every few minutes", "test", "real fire", "flames", "smoke in the",
                     "landlord", "rent",
                     "burglar", "burglary", "house alarm", "car alarm", "vehicle alarm",
                     "phone alarm", "alarm clock", "intruder", "security alarm",
                     "security system", "panic alarm", "shop alarm", "office alarm"),
              ask=("cook", "cooking", "cooked", "toast", "toasting", "grill", "grilling", "oven",
                   "hob", "fry", "frying", "roast", "roasting", "bake", "baking", "shower",
                   "steam", "kitchen", "burning", "burnt",
                   "for no reason", "for no apparent reason", "for no obvious reason",
                   "no reason", "no reason at all", "nothing burning", "nothing was burning",
                   "nothing is burning", "nothing on fire", "no smoke",
                   "no fire", "was no fire", "nothing caught fire", "nothing cooking",
                   "nothing was cooking", "nothings cooking", "wasnt cooking", "wasn't cooking",
                   "not cooking", "randomly", "out of nowhere", "middle of the night",
                   "at 3am", "at 2am", "last night"),
              bias=1),
        entry("slow-cooker-clean", (("slow cooker", "slow cookers", "slow cooker pot", "crock pot",
                                     "crockpot", "ceramic pot", "slow cooker bowl"),
                                    ("clean", "cleaning", "cleaned", "wash", "washing", "scrub",
                                     "burnt", "burnt on", "baked on", "stuck", "crusted",
                                     "stained", "inside", "pot", "bowl", "dishwasher")),
              "Scrape it out and let the pot cool before anything cold touches it, because a hot "
              "ceramic pot can crack under cold water, and the pot and lid are then usually "
              "dishwasher safe. A crusted pot lifts clean if you soak it overnight with hot water and "
              "a dishwasher tablet or a tablespoon of bicarbonate of soda and wipe it with a sponge, "
              "with nothing abrasive on the glaze. The base is the part you do not wash: unplug it and "
              "wipe it out with a damp cloth.",
              avoid=("recipe", "recipes", "meal", "meals", "curry", "chilli", "stew", "soup",
                     "should i buy", "worth it", "buy", "broken", "not heating", "wont heat",
                     "slow cook", "how long", "what can i make"),
              ask=("clean", "cleaning", "cleaned", "wash", "scrub", "burnt", "stuck", "crusted",
                   "stained", "smells", "smell", "dishwasher")),
        entry("toaster-clean", (("toaster", "toasters"),
                                ("clean", "cleaning", "cleaned", "wash", "crumbs", "crumb tray",
                                 "burnt", "stuck", "dirty", "greasy")),
              "Unplug it and tip the crumbs out over the bin, then brush the inside with a dry pastry "
              "brush or an old toothbrush: never put water in a toaster. Wipe the outside with a damp "
              "cloth once it is cold, and empty the crumb tray every week or so, since that is what "
              "smells when it burns.",
              avoid=("buy", "worth it", "best", "tripping", "not working", "broken", "pale",
                     "uneven", "how long", "browns", "fuse", "smells like burning", "smell of burning",
                     "smells of burning", "burning smell", "smells burning", "smoking", "smoke",
                     "sparks", "sparking"),
              ask=("clean", "cleaning", "cleaned", "wash", "crumbs", "crumb", "burnt", "dirty",
                   "greasy", "inside")),
        entry("appliance-tripping", (("tripping", "trips", "trip", "blowing", "blows", "cuts out",
                                      "knocking off", "keeps going off"),
                                     ("electrics", "electric", "power", "fuse box", "circuit", "rcd",
                                      "breaker", "trip switch", "mains", "socket")),
              "An appliance that trips the power is usually the appliance itself: unplug it, try it in "
              "a socket on another circuit, and if it trips again stop using it and get it repaired. "
              "Anything that takes the RCD out the moment it is plugged in has a fault to earth, so "
              "don't keep resetting the switch to check - that one needs an electrician.",
              ask=("kettle", "washing", "washer", "dryer", "tumble", "oven", "dishwasher", "fridge",
                   "freezer", "appliance", "toaster", "microwave", "hoover", "vacuum", "iron",
                   "heater", "shower", "immersion", "machine", "tv", "lamp", "extension",
                   "air fryer", "airfryer", "slow cooker", "pressure cooker", "rice cooker",
                   "bread maker", "blender", "food processor", "coffee machine", "kettle"),
              bias=2),
        entry("kitchen-machine-fault",
              (("air fryer", "airfryer", "air-fryer", "slow cooker", "pressure cooker", "instant pot",
                "multi cooker", "rice cooker", "bread maker", "bread machine", "blender",
                "food processor", "stand mixer", "kettle", "toaster", "sandwich toaster",
                "microwave", "coffee machine", "soup maker", "waffle maker", "deep fat fryer",
                "griddle", "panini", "machine", "appliance"),
               MACHINE_BURNING + MACHINE_DEAD + MACHINE_LEAKING),
              _machine_fault,
              ask=("my", "our", "the", "is", "wont", "won't", "keeps", "and", "stopped", "stopping",
                   "why", "what", "how", "should", "smoke", "smokes", "smoking", "spark", "sparks",
                   "heating", "heat", "working", "leaking", "dead", "power", "switch", "on"),
              avoid=("fuse box", "rcd", "breaker", "circuit", "guilt",
                     "washing machine", "washer", "dryer", "tumble dryer", "laundry", "spin",
                     "drum", "dishwasher", "oven", "fridge", "freezer", "boiler", "hoover",
                     "vacuum", "iron", "pan", "oil", "bbq",
                     "barbecue", "smoker", "cigarette", "vape", "candle", "fire alarm", "chimney",
                     "burnt my", "burnt the", "when it boils", "as it boils"),
              bias=1),
        entry("appliance-normal-cutout",
              (("kettle", "microwave", "oven", "washing machine", "washer", "dishwasher", "dryer",
                "tumble dryer", "toaster", "appliance", "boiler"),
               NORMAL_CUTOUT),
              "A kettle cutting out as the water boils, a microwave stopping when the door opens, an "
              "oven stopping when its timer ends or it reaches temperature, a washer or dryer "
              "finishing at the end of the programme: that is the machine working as designed, and "
              "there is nothing to fix. A fault looks different - it gives up part way through a job "
              "with work left to do, or it stops sooner each time it is used.",
              bias=1),
        entry("appliance-cutting-out",
              (("switches off", "switching off", "switches itself off", "switching itself off",
                "turns itself off", "turning itself off", "cuts out", "cutting out", "stops mid",
                "stopping mid", "stops halfway", "stopped mid", "keeps stopping", "keeps cutting out",
                "keeps switching off", "keeps turning itself off", "wont stay on", "won't stay on",
                "switching off before", "pops up", "popping up", "pops", "popping", "pop up",
                "stops after", "stopped after", "stops every", "stops early", "stops suddenly"),
               ("kettle", "microwave", "washing machine", "washer", "dishwasher", "toaster", "oven",
                "dryer", "tumble dryer", "coffee machine", "iron", "appliance", "hoover", "vacuum",
                "boils", "cycle", "mid cycle", "halfway", "toast")),
              _appliance_cutting_out,
              bias=1,
              avoid=("trip", "trips", "tripping", "fuse", "fuse box", "rcd", "breaker", "mains",
                     "power cut", "laptop", "computer", "pc", "phone", "iphone", "tv", "router",
                     "hair dryer", "hairdryer", "hair drier")
                    + NORMAL_CUTOUT),
        entry("kettle-will-not-switch-off",
              (("boils dry", "boiled dry", "boiling dry", "boils away", "boiled away",
                "keeps boiling", "kept boiling", "keeps bubbling", "wont stop boiling",
                "won't stop boiling", "doesnt stop boiling", "never stops boiling",
                "wont switch off", "won't switch off", "doesnt switch off", "never switches off",
                "wont switch itself off", "never switches itself off", "wont turn off",
                "won't turn off", "doesnt turn off", "wont shut off", "doesnt shut off",
                "wont stop", "doesnt stop"),
               ("kettle", "kettles", "boil", "boils", "boiling", "spout", "steam switch")),
              _kettle_will_not_stop,
              bias=2,
              avoid=("pan", "pans", "saucepan", "pot", "pots", "hob", "hobs", "ring",
                     "rings", "oven", "ovens", "grill", "microwave", "toaster", "air fryer",
                     "slow cooker", "washer", "washing machine", "dishwasher", "dryer", "iron",
                     "boiler", "immersion", "radiator", "heating", "tv", "telly", "light", "lights",
                     "lamp", "phone", "laptop", "fan", "heater",
                     "boils over", "boiled over", "boiling over", "overflow", "too full", "too long",
                     "takes ages", "slow to boil", "boils slowly",
                     "smell", "smells", "smelt", "smelled", "smelly", "burnt", "burning", "scorch",
                     "soup", "soups", "stew", "stews", "casserole", "curry", "chilli", "chili",
                     "bolognese", "sauce", "sauces", "gravy", "stock", "broth", "porridge",
                     "pasta", "rice", "risotto", "lentils", "beans", "chickpeas", "milk",
                     "hotpot", "tagine", "goulash", "daal", "dal", "dhal"),
              ),
        entry("consumer-unit",
              (("fuse box", "fuse board", "consumer unit", "trip switch", "trip switches", "rcd",
                "breaker", "breakers", "mcb", "main switch", "electricity", "power", "power supply",
                "electricity supply"),
               ("where", "find", "locate", "reset", "resetting", "tripped", "trips", "keeps", "kept",
                "turn off", "turn the power", "turn the power off", "turning off", "switch off",
                "switching off", "switch the power off", "switching the power off", "off", "on",
                "the power", "house", "home", "flat", "lights", "everything", "down")),
              _consumer_unit,
              bias=2,
              avoid=("plug", "plugs", "appliance", "appliances", "kettle",
                     "washing machine", "washer", "dryer", "dishwasher", "oven", "toaster", "shower",
                     "boiler", "pump", "immersion", "laptop", "macbook", "computer", "phone", "tablet",
                     "charger", "charging", "battery", "tripping over", "trips over", "trip over",
                     "tripped over", "over my feet", "over her feet", "over his feet", "feet", "foot",
                     "stairs", "rug", "carpet", "pavement", "kerb", "fell", "fallen", "falls",
                     "falling", "guilt tripping", "guilt trip", "guilt trips", "guilt-tripping",
                     "guilt-trip", "tripping me",
                     "cut", "cuts", "outage", "blackout", "attorney", "station", "solar", "wind",
                     "nuclear", "horsepower", "powerful", "washing",
                     "plant", "plants", "factory", "factories", "grid", "pylon", "pylons",
                     "closure", "power station", "power stations")),
        entry("fuse-tripping", (("fuse", "plug", "socket", "rcd", "trip", "tripping"),
                                ("blown", "change", "keeps", "not working", "keeps tripping", "stopped",
                                 "dead")),
              "If one socket has stopped working, switch it off at the wall, open the plug and replace "
              "the fuse with one of the same rating (13A for most appliances, 3A for lamps). If the RCD "
              "or a breaker keeps tripping, unplug everything on that circuit and get an electrician: "
              "that's not a DIY job.",
              avoid=("laptop", "macbook", "computer", "phone", "tablet", "charger", "charging",
                     "battery", "mains", "overnight",
                     "road trip", "day trip", "long trip", "on a trip", "school trip",
                     "camping trip", "trip to ", "trip with", "travelling", "traveling",
                     "tripping over", "trips over", "trip over", "tripped over", "over my feet",
                     "over her feet", "over his feet", "feet", "foot", "stairs", "rug", "carpet",
                     "pavement", "kerb", "doorstep", "walking", "fell", "fallen", "falls", "falling",
                     "guilt tripping", "guilt trip", "guilt trips", "guilt-tripping", "guilt-trip",
                     "tripping me")),
        entry("fuse-box-trip",
              (("fuse box", "fuse board", "fuse", "consumer unit", "trip switch", "breaker",
                "breakers", "rcd", "rcbo", "circuit", "electrics"),
               ("tripped", "trip", "trips", "tripping", "reset", "gone off", "gone down", "off",
                "keeps", "blown", "board", "consumer unit", "circuit")),
              ("Look at which switch is down before you reset it: a single breaker is one circuit, a "
               "wider switch marked RCD or RCBO is a fault to earth. Unplug everything on that circuit, "
               "push the switch fully down and then back up, and if it holds, plug things back one at a "
               "time until it trips again - that appliance is the fault. If it will not reset with "
               "nothing plugged in, or it is the RCD that keeps going, leave it up and get an "
               "electrician. Never tape a breaker up or fit a bigger one."),
              bias=1,
              avoid=("kettle", "washing", "washer", "dryer", "tumble", "oven", "dishwasher", "fridge",
                     "freezer", "toaster", "microwave", "hoover", "vacuum", "iron", "heater",
                     "shower", "immersion", "machine", "plug", "13a", "3a", "13 amp", "3 amp")),
        entry("loft-insulation",
              (("loft", "attic", "roof space", "roof insulation", "loft insulation",
                "attic insulation"),
               ("insulate", "insulated", "insulation", "lagging", "lag", "wool", "rolls", "roll",
                "cheap", "cheapest", "cost", "much", "how much", "grant", "draught", "draft")),
              ("Lay mineral wool 270mm deep, which is two layers of 100mm plus one of 70mm criss-crossed, "
               "and it costs about £300 to £600 for a typical semi if you do it yourself: it is the "
               "cheapest thing a house can do to its bills and pays back in a few years. Keep the "
               "eaves clear at the edge for ventilation, do not squash the wool down, and leave a gap "
               "round downlights unless they are marked fire-rated. Bigger jobs - a flat roof, a "
               "dormer, spray foam - want someone registered, and there are often grants."),
              avoid=("clear out", "clearout", "declutter", "clear the loft", "tidy", "junk",
                     "conversion", "convert", "dormer", "extension", "storage", "store things",
                     "board out", "floor it",
                     "leak", "leaking", "leaks", "leaked", "replace", "replacing", "replacement",
                     "repair", "repairs", "tile", "tiles", "slate", "slates", "felt", "flat roof",
                     "repoint", "repointing", "fix", "fixing", "damp", "gutter", "gutters",
                     "chimney", "ridge", "moss")),

        entry("paint-quantity",
              (("paint", "emulsion", "paint tin", "undercoat", "gloss"),
               ("how much paint", "much paint", "how many litres", "litres of paint", "liters of paint",
                "how many tins", "tins of paint",
                "enough paint", "quantity of paint", "how much do i need")),
              _paint_for_the_room,
              avoid=("what colour", "what color", "which colour", "which color", "colour scheme",
                     "mark", "marks", "scuff", "stain", "stains", "peeling", "bubbling", "blistering",
                     "damp", "mould", "mold", "woodchip", "wallpaper", "fence", "shed", "door",
                     "radiator", "kitchen cabinet", "cupboard", "car", "bike", "model", "art",
                     "paint a picture", "nails", "makeup",
                     "cost", "costs", "price", "prices", "cheap", "cheapest", "expensive",
                     "how much is", "how much does",
                     "store", "storing", "stored", "part used", "part-used", "partly used",
                     "half a tin", "leftover", "left over", "lid on", "keep it",
                     "between coats", "how long between", "how long after", "wait between",
                     "second coat", "third coat", "recoat", "re-coat")),
        entry("wallpaper-quantity",
              (("wallpaper", "wall paper", "wallcovering", "lining paper"),
               ("how much", "much wallpaper", "how many rolls", "many rolls", "rolls of wallpaper",
                "need", "needs", "buy", "quantity", "enough")),
              _wallpaper_for_the_room,
              avoid=("strip", "stripping", "remove", "removing", "woodchip", "paint over", "paint",
                     "damp", "mould", "mold", "crack", "cracked", "peel", "peeling", "feature wall",
                     "which wallpaper", "what wallpaper", "choose", "border", "phone", "laptop",
                     "screen", "wallpaper app", "windows wallpaper",
                     "cost", "costs", "price", "prices", "cheap", "cheapest", "expensive",
                     "how much is", "how much does"),
              bias=1),
        entry("bulk-quantity",
              (("gravel", "gravels", "shingle", "pea gravel", "pea shingle", "pebbles",
                "slate chippings", "chippings", "bark", "bark chippings", "mulch", "topsoil",
                "top soil", "compost", "soil", "sand", "sharp sand", "builder's sand", "grit",
                "ballast", "hardcore", "sub base", "type 1", "concrete", "postcrete", "turf",
                "grass seed"),
               ("how much", "how many", "how deep", "how thick", "depth of", "depth should",
                "much do i need", "much will i need", "many bags", "many tonnes", "many tons",
                "bags of", "tonnes of", "tons of", "cubic", "cubic metres", "cubic feet",
                "square metres of", "coverage", "cover the", "need for", "do i need")),
              "Work it out as a volume: length times width times depth, all in metres. Gravel and slate "
              "chippings go down about 5cm deep, or 10cm if a car drives on them, so a 5m by 3m drive "
              "at 5cm is 0.75 cubic metres - about 1.2 tonnes, or fifty 25kg bags. Bark and mulch are "
              "the same sum at 5 to 7cm over the soil. Topsoil is the deep one: 10 to 15cm for a new "
              "bed, and a 20cm fill in a 3m by 1m raised bed wants 0.6 cubic metres. A cubic metre is "
              "roughly 1.5 tonnes of gravel and about a tonne of soil or compost, and a builder's bulk "
              "bag is about 0.8 of a cubic metre, so check which one the price is for. Turf and grass "
              "seed are sold by area instead: measure the lawn and add 5 per cent for the cuts.",
              avoid=("cost", "costs", "price", "prices", "cheap", "cheapest", "expensive",
                     "how much is", "how much does", "how much would", "laid", "fitted", "quote",
                     "quotes", "hire", "rent", "which", "what type", "what sort", "best type",
                     "what kind", "what colour", "what color",
                     "how do i lay", "how to lay", "lay a", "laying a", "laying the", "install",
                     "installing", "membrane", "weed", "weeds", "weeding", "level", "edge",
                     "leave filler", "before sanding", "sanding down", "sand it", "sanding filler",
                     "wait before sanding", "filler before",
                     "sand down", "sandpaper", "sand paper", "sand pit", "sandpit", "play sand",
                     "kinetic sand", "sand castle", "sandwich", "sandwiches",
                     "dog", "dogs", "puppy", "bark at", "why does my dog",
                     "neighbour", "neighbor", "boundary", "who owns",
                     "pay half", "who pays", "cake", "potting bench", "houseplant", "indoor",
                     "pot", "pots", "potting", "container", "containers", "tub", "tubs",
                     "window box", "hanging basket", "hanging baskets", "seed tray", "seed trays",
                     "houseplants",
                     "water", "watering", "watered", "sow", "sowing", "sowed", "plant", "planting",
                     "planted", "per square metre", "per sq m", "sandbox", "sand box",
                     "chicken", "chickens",
                     "fence post", "fence posts", "post hole", "post holes", "posthole", "postholes",
                     "postcrete", "concrete post", "concrete posts",
                     "mortar", "mortar mix", "sand and cement", "sharp sand and cement",
                     "building sand and cement", "cement mix", "how much cement", "bags of cement"),
              bias=1,
              guard=lambda u: not a_sanding_job(u)),

        entry("sanding-before-painting",
              (("sand", "sanding", "sanded", "sandpaper", "sand paper", "sander",
                "rub it down", "rub down", "rubbed down", "key the surface", "key it"),
               ("before paint", "before painting", "before the paint", "before undercoat",
                "before a primer", "before the primer", "before gloss", "before the gloss",
                "do i need to sand", "should i sand", "need to sand", "have to sand",
                "do i need to rub", "should i rub", "do i need to key", "should i key",
                "sand it first", "sand first", "sand it down", "sanding before",
                "is sanding needed", "is it sanded", "does it need sanding",
                "sand the wall", "sand the walls", "sand the door", "sand the doors",
                "sand the woodwork", "sand the ceiling", "sand the trim",
                "do i have to sand", "should i sandpaper", "need sanding",
                "does it need sanding first",
                "before the next coat", "before the second coat", "before a second coat",
                "before another coat", "before recoating", "between coats", "coats")),
              "Yes, give it a sand first: 120 grit on a block for painted woodwork and 80 to 100 on a "
              "filler patch, with the grain and light enough to take the shine off rather than the "
              "paint, then dust it down and wipe it over with a damp cloth. Old gloss has to be "
              "keyed or the new coat slides off it, and a filled patch has to be flatter than the "
              "wall around it or it shows through. Bare wood wants 120 grit, then 180, and the dust "
              "off before the first coat.",
              avoid=("how much", "how many", "cost", "costs", "price", "prices", "cheap",
                     "expensive", "bags of", "tonnes", "tons", "cubic", "square metres",
                     "coverage", "between", "how long", "leave filler", "leave it to",
                     "filler take", "filler set", "drying", "wait",
                     "plaster", "plastered", "plastering", "skim", "mist coat",
                     "or fill", "fill first", "filler first", "before i fill", "before filling"),
              guard=lambda u: not re.search(r"\bor\b[^.?]*\bfirst\b|\bfirst\b[^.?]*\bor\b",
                                            str((u or {}).get("clean") or (u or {}).get("text") or ""),
                                            re.I),
              bias=3),
        entry("which-paint",
              (("paint", "painting", "repaint", "emulsion", "gloss", "eggshell", "satinwood",
                "satin", "silk", "undercoat", "primer", "priming", "matt", "matte"),
               ("what paint", "which paint", "what kind", "what type", "what sort", "kind of paint",
                "type of paint", "sort of paint", "best paint", "best", "should i get",
                "should i buy", "should i use", "do i need", "need for", "for walls", "for wall",
                "for the walls", "for the wall", "for ceilings", "for a ceiling", "for the ceiling",
                "for woodwork", "for the woodwork", "for skirting", "for doors", "for a door",
                "for plaster", "new plaster", "for a bathroom", "for the bathroom",
                "for a kitchen", "for the kitchen", "for a hallway", "for the hallway",
                "for a radiator", "for kids", "kids room", "washable", "what is", "whats",
                "what's", "eggshell paint for", "gloss or", "or satinwood", "matt or", "silk or")),
              "Emulsion for walls and ceilings: matt for a bedroom or a living room, and a washable "
              "matt or eggshell where it has to take scrubbing, such as a hallway, a kitchen or a "
              "kids' room. Woodwork wants eggshell or satinwood rather than gloss, because gloss "
              "shows up every lump and brush mark. Bare wood or metal gets a primer then an "
              "undercoat; plastic, melamine and old gloss need an adhesion primer first or the paint "
              "peels; anything that gets hot, like a radiator or a pipe, wants a heat-resistant "
              "paint made for metal. New plaster wants a mist coat - emulsion thinned by about a "
              "fifth with water, no vinyl - to soak in and seal the dust. Buy a sample pot before the "
              "big tin, because colour on a wall is not colour on a card.",
              avoid=("how much paint", "much paint", "how many litres", "litres of paint",
                     "how many tins", "how many coats", "coats of paint", "second coat",
                     "between coats", "how long", "dry", "drying", "how many days", "how much",
                     "how many", "cost", "costs", "price", "prices", "cheap", "expensive",
                     "what colour", "what color", "which colour", "which color", "colour scheme",
                 "neutral", "good colour", "best colour", "colour choice", "colour to paint",
                 "colour for", "which white",
                     "mark", "marks", "scuff", "stain", "stains", "peeling", "bubbling",
                     "blistering", "wallpaper", "fence", "shed", "car", "bike", "model", "art",
                     "paint a picture", "nails", "makeup", "store", "storing", "leftover",
                     "left over", "dispose", "get rid of", "thin", "white spirit",
                     "bathroom", "kitchen", "radiator", "ceiling first",
                     "paint a room", "paint the room", "paint my room", "paint a bedroom",
                     "ceiling", "ceilings", "ceiling first",
                     "paint the walls", "paint the wall", "paint a wall", "to paint a room",
                     "matt or silk", "silk or matt", "decorate", "decorating", "decorated",
                     "door", "doors", "front door", "back door", "skirting", "skirting boards",
                     "gate", "gates", "garden gate", "metal gate", "metal", "railings")),
        entry("paint-over-a-colour",
              (("paint", "painting", "repaint", "go over", "going over", "paint over"),
               ("dark", "darker", "darkest", "strong colour", "strong color", "bright colour",
                "bright color", "bright red", "red wall", "dark green", "dark blue",
                "old colour", "old color", "previous colour", "previous color", "dark paint",
                "block the colour", "hide the colour", "cover the wall", "over the top",
                "grimy white", "yellowed")),
              "Two coats of a decent emulsion usually cover a dark wall, and going much lighter "
              "than the old colour can need three; sand and wipe the wall down first and do not "
              "thin the paint. If the old colour is a strong red or a dark green, ask for a "
              "combined primer and undercoat tinted towards the new colour - it saves a coat and "
              "stops the old shade grinning through.",
              bias=1),
        entry("paint-room", (("paint", "painting"), ("room", "wall", "walls", "living", "need",
                                                    "before", "prepare",
                                                    "bedroom", "bedrooms", "lounge", "living room",
                                                    "front room", "dining room", "spare room",
                                                    "nursery", "whole flat", "whole house")),
              "Before paint you need filler for the holes, fine sandpaper, masking tape, a dust sheet, "
              "a roller and tray, a brush for edges and an old screwdriver to open the tin. One litre "
              "of emulsion covers about 12 square metres, so measure the walls and buy two coats' "
              "worth.",
              avoid=("what colour", "what color", "which colour", "which color", "colour", "colours",
                     "color", "colors",
                     "mark", "marks", "marked", "scuff", "scuffs", "stain", "stains",
                     "fingerprint", "fingerprints", "smudge", "smudges",
                     "how much paint", "much paint", "how many litres", "litres of paint",
                     "how many coats", "coats of paint",
                     "what paint", "which paint", "what kind of paint", "what type of paint",
                     "best paint", "washable", "washable paint", "kids room"),
              ),
        entry("paint-drying-time",
              (("paint", "painting", "repaint", "repainting", "filler", "filling", "undercoat",
                "gloss", "emulsion", "primer", "silicone", "sealant", "caulk", "wood filler"),
               ("how long", "wait", "waiting", "dry", "dries", "drying", "cure", "curing",
                "overnight", "hours", "before painting", "before i paint", "before sanding")),
              "Emulsion takes a second coat in 2 to 4 hours and is properly hard in about a day; "
              "undercoat and gloss want overnight, 16 to 24 hours, and longer in a cold room. A "
              "small hole of filler is hard in about an hour, so it can be sanded and painted the "
              "same day, but a deep fill wants overnight or it shrinks back and shows. Silicone has "
              "to be a paintable one - most sanitary silicones cannot be painted at all - and it "
              "wants 24 hours to cure before a brush goes near it.",
              avoid=("how long does it take to paint", "how long to paint", "take to paint",
                     "paint a room", "paint the room", "paint my room", "paint the walls",
                     "how many coats", "how much paint", "how many litres", "much paint",
                     "cost", "costs", "price", "prices", "cheap", "expensive", "how much is",
                     "how much does", "what colour", "what color", "which colour", "which color",
                     "peeling", "peeling off", "flaking", "bubbling", "blistering", "strip",
                     "stripping", "wallpaper", "last", "lasts", "goes off", "shelf life",
                     "between coats", "how many coats", "coats of paint", "recoat", "re-coat",
                     "second coat", "third coat",
                     "drying too fast", "drying too quickly", "dries too fast", "dry too fast",
                     "from drying", "keeps drying", "before it dries", "open time", "wet edge")),
        entry("filler-drying-time",
              (("filler", "wood filler", "polyfilla", "filling", "filled", "skim", "skimming"),
               ("how long", "leave", "wait", "dry", "dries", "drying", "set", "sets", "harden",
                "hardens", "sand", "sanding", "sanded", "rub down", "rubbing down", "before")),
              "A thin skim of filler is hard in about an hour and can be sanded the same day; a deep "
              "fill wants overnight, because it shrinks back if the middle is still soft when you rub "
              "it down. Rub it with 120 grit on a block rather than with your fingers, and stop when "
              "the edge blends into the wall - two thin fills are quicker than one thick one that has "
              "to be dug out. Give it a coat of watered-down emulsion before the paint, or the patch "
              "drinks the first coat and shows as a dull spot.",
              avoid=("how much", "how many", "bags", "cost", "costs", "price", "prices",
                     "quid", "pounds", "£", "fuel", "petrol", "diesel", "radiator",
                     "car", "pipe", "sink", "bath", "cake", "sandwich", "sandpaper",
                     "what is", "what are", "what's", "meaning", "recipe",
                     "first", "which one first", "before that", "order", "order to"),
              bias=2),
        entry("paint-drying-fast",
              (("paint", "painting", "emulsion", "gloss", "undercoat", "eggshell", "satin",
                "roller", "brush", "wet edge", "paint tin", "tin of paint", "tray"),
               ("drying too fast", "drying too quickly", "dries too fast", "dries too quickly",
                "dry too fast", "dry too quickly", "keeps drying", "from drying", "stop it drying",
                "before it dries", "going off the brush", "drying out", "wet edge", "open time",
                "workable", "flash", "dry so fast", "dries so fast", "dry so quick", "dries so quick",
                "drying so fast", "so fast", "too hot", "in this heat"),),
              "Heat and moving air are what dry a paint too fast, so keep the room cool and out of "
              "direct sun, shut the window and turn any fan off. Lid the tin and decant only what you "
              "will use in ten minutes, because a wide tray is all surface; a smaller tub keeps it "
              "workable. Water-based paint can take a splash of water, no more than one part in ten, "
              "or a paint conditioner from a decorator's shop. Then work to a wet edge: do one wall at "
              "a time in one go, roll into the bit you just did rather than next to it, and do not "
              "stop halfway across. A brush or roller you are coming back to in a few minutes goes in "
              "a damp cloth or a bag, and a skin on the paint in the tin gets lifted off, not stirred "
              "back in.",
              avoid=("how long", "how many hours", "overnight", "second coat", "between coats",
                     "how many coats", "get rid", "dispose", "throw", "bin", "tip", "recycle",
                     "leftover", "old paint", "how much paint", "cost", "price", "cheap",
                     "peeling", "flaking", "cracking", "bubbling", "blistering", "strip",
                     "wallpaper", "smell", "smells", "fume", "fumes", "colour", "color",
                     "which paint", "best paint", "nail polish", "spray")),
        entry("paint-keeping",
              (("paint", "painting", "emulsion", "gloss", "undercoat", "eggshell", "satin",
                "tin of paint", "paint tin", "part used paint", "part-used paint"),
               ("store", "storing", "storage", "keep", "keeping", "kept", "lumpy", "lumps",
                "lumpy paint", "skin", "skinned over", "skinning over", "skin on the paint",
                "gone thick", "gone hard", "thickened", "separated", "frozen", "gone off",
                "between coats", "between jobs", "over winter", "in the garage", "in the shed")),
              ("Paint keeps for years if the lid is sealed: wipe the rim clean, press the lid down "
               "with a block of wood until it clicks, and store the tin upside down so any skin forms "
               "at the bottom rather than on top. Keep it somewhere frost-free, because paint that has "
               "frozen is never right again. A tin that has gone lumpy or thick can often be saved: "
               "lift the skin off, strain it through a pair of tights or a paint strainer into a clean "
               "tub, and stir it well - water-based paint takes a splash of water, oil-based takes "
               "white spirit, no more than one part in ten. When it is full of hard lumps, or it "
               "smells sour, it is past saving and goes to the tip."),
              avoid=("brush", "brushes", "paintbrush", "paintbrushes", "roller", "rollers",
                     "get rid", "dispose", "throw", "bin", "the tip", "to the tip", "recycle",
                     "how long does it take", "how long to paint", "how many coats", "how much paint",
                     "second coat", "between coats of", "drying too fast", "dries too fast",
                     "thin", "thins", "thinning", "thin it", "thin the", "thinner", "water it down",
                     "wet edge", "peeling", "flaking", "bubbling", "strip", "wallpaper", "smell",
                     "smells", "fumes", "colour", "color", "which paint", "nail polish", "spray"),
              bias=1),
        entry("paint-too-dark",
              (("paint", "painted", "painting", "emulsion", "gloss", "undercoat", "eggshell",
                "satin", "satinwood", "varnish", "lacquer", "wood stain", "stain", "wood dye",
                "fence stain", "decking stain", "paint tin", "tin of paint", "roller"),
               ("too dark", "come out dark", "came out dark", "came up dark", "darker than",
                "much darker", "so dark", "dried dark", "dries dark", "goes dark", "went dark",
                "too strong", "too bright", "too intense", "too deep", "too orange", "too yellow",
                "too red", "lighten", "lightening", "lighter", "pale it down", "palest",
                "hate the colour", "wrong colour", "wrong color", "not the colour", "regret",
                "darker sample", "the sample")),
              "Give it a day before you judge it: paint reads about a shade lighter while it is wet, "
              "so a wall that looks too strong tonight has usually settled by tomorrow, and the light "
              "you look at it in changes it as much as the paint does. If it is still too dark once it "
              "is hard, nothing can be added to a coat to lighten it - so the fix is either one coat "
              "of the colour you wanted over the top (a pale colour covers a dark one in two or three "
              "coats, and a test patch on a scrap of plasterboard or lining paper will tell you how "
              "many before you buy another tin), or a glaze of white emulsion wiped over it while it "
              "is tacky to lift it a shade. If the tin was a match to a sample, take a photo in "
              "daylight and the tin back to the shop: most will retint or exchange one they mixed "
              "wrong. A wood stain that went too dark sands back to bare wood and starts again with a "
              "pale one, since stain sinks in rather than sitting on top.",
              avoid=("streak", "streaks", "streaky", "patchy", "patchy coverage", "blotchy",
                     "uneven", "roller marks", "brush marks", "lap marks",
                     "mark", "marks", "scuff", "scuffs", "smudge", "spill", "spilled", "drip",
                     "drips", "carpet", "sofa", "shirt", "clothes", "fabric", "curtain", "hands",
                     "skin", "nail", "nails", "hair",
                     "how much", "how many litres", "litres", "tins of", "cost", "costs", "price",
                     "prices", "cheap", "expensive", "how much is", "how much does",
                     "how long", "drying time", "dry between", "second coat", "how many coats",
                     "which paint", "what paint", "best paint", "what colour should",
                     "which colour should", "what color should", "strip", "stripping", "remove",
                     "removing", "peel", "peeling", "flaking", "bubbling", "blistering",
                     "wallpaper", "woodchip", "fence up", "shed", "car", "bike", "model", "canvas",
                     "picture", "art", "nails", "makeup", "printing", "printer", "photo"),
              bias=2),
        entry("woodchip-off",
              (("woodchip", "wood chip", "woodchip paper", "anaglypta", "textured wallpaper"),
               ("strip", "strips", "stripping", "remove", "removing", "off", "get off",
                "come off", "take down", "steam", "steamer", "scrape", "scraping", "soak",
                "soaking", "stuck", "peel", "peeling", "paint", "painting", "over", "cover")),
              "Woodchip comes off in two goes: lift the top layer dry with a wide scraper first (it "
              "comes away in sheets), then score and soak the backing paper for 10 to 15 minutes and "
              "scrape that off. Do not wet it before the top is off, or the chips turn to mush and "
              "smear across the wall.",
              avoid=("buy", "buying", "selling", "sell", "price", "cost", "how much is",
                     "wood chip boiler", "boiler", "biomass")),
        entry("wallpaper-peeling",
              (("wallpaper", "wall paper", "lining paper", "paper"),
               ("peel", "peels", "peeled", "peeling", "lifting", "lifts", "loose", "bubble",
                "bubbles", "bubbling", "blister", "blistering", "corner", "corners", "seam",
                "seams", "coming away", "came away", "flapping", "repair")),
              "Paste it back rather than strip it: lift the loose edge with a knife, scrape the old "
              "paste off the wall behind it with a filling knife, spread a thin even coat of overlap "
              "adhesive (border and overlap adhesive) on the wall, press the paper back and smooth it "
              "out from the middle with a damp sponge. A bubble in the middle gets a slit with a "
              "stanley knife, paste, and the same press. Damp patches that keep coming back are not a "
              "paper problem.",
              avoid=("how long", "strip", "stripping", "remove all", "whole room", "damp", "mould",
                     "mold", "wet", "leak", "what colour", "which colour", "paint over"),
              bias=1),
        entry("paint-over-wallpaper",
              (("paint", "painting", "repaint", "emulsion", "undercoat"),
               ("wallpaper", "wall paper", "lining paper", "paper", "walls", "wall", "over")),
              "Not over woodchip or any textured paper: the pattern shows through, every seam lifts, "
              "and a thinned first coat will not hold it down. Smooth, sound lining paper can be "
              "painted with a mist coat (emulsion thinned by about a tenth) and then two ordinary "
              "coats, and any bubble or lifted seam comes off before the roller comes out.",
              ask=("wallpaper", "wall paper", "lining paper", "paper", "over"),
              avoid=("what colour", "what color", "which colour", "which color", "colour",
                     "colours", "color", "colors", "toilet paper", "newspaper", "exam paper",
                     "printer paper", "wrapping paper", "sandpaper", "paint stripper",
                     "paintbrush", "paint brush", "fence", "door", "doors", "radiator",
                     "ceiling")),
        entry("wallpaper-off",
              (("wallpaper", "wall paper", "wallpapers", "lining paper", "paper"),
               ("strip", "strips", "stripping", "remove", "removing", "off", "get off",
                "come off", "comes off", "take down", "steam", "steamer", "scrape", "scraping",
                "soak", "soaking", "stuck", "peel", "peeling", "old")),
              "Score it all over, soak it, then scrape it: a paper tiger (or a fork) gives the water "
              "somewhere to go, warm water with a splash of washing-up liquid needs 10 to 15 minutes "
              "to do its work, and a scraper held almost flat lifts the paper without gouging the "
              "plaster. A steamer is quicker than a sponge for a whole room, and an old papered room "
              "is a weekend's job.",
              avoid=("peel", "peels", "peeled", "peeling", "lifting", "bubble", "bubbles",
                     "bubbling", "corner", "corners", "phone", "iphone", "android", "mobile",
                     "tablet", "ipad", "laptop",
                     "computer", "pc", "desktop", "screen", "lock screen", "home screen",
                     "background", "download", "app", "print", "printer", "printing", "exam",
                     "essay", "newspaper", "toilet paper", "damp", "mould", "mold",
                     "condensation", "woodchip",
                     "mark", "marks", "stain", "stains", "dirty", "clean", "cleaning", "wash",
                     "washed", "scuff", "scuffs", "smudge", "smudges", "grease", "greasy",
                     "fingerprints", "fingerprint", "spot", "spots", "wipe")),
        entry("wallpaper-mark",
              (("wallpaper", "wall paper", "papered wall", "papered walls", "lining paper",
                "vinyl wallpaper", "flocked wallpaper", "woodchip"),
               ("mark", "marks", "stain", "stains", "dirty", "clean", "cleaning", "wash",
                "washable", "scuff", "scuffs", "smudge", "smudges", "grease", "greasy",
                "fingerprints", "fingerprint", "spot", "spots", "wipe")),
              "Go at it dry first and test a hidden corner: a soft pencil rubber or a clean, barely "
              "damp cloth with a drop of washing-up liquid lifts most marks off paper, working from "
              "the bottom up so drips do not streak. Water is what ruins wallpaper, so keep the "
              "cloth as dry as it can be - a washable vinyl paper takes a mild soap, a printed or "
              "flocked one usually will not, and a mark that will not lift is better patched or "
              "covered than scrubbed.",
              avoid=("strip", "stripping", "remove the paper", "remove the wallpaper", "take down",
                     "hang", "hanging", "hanging paper", "paste", "repaste", "put up", "putting up",
                     "put wallpaper", "put the wallpaper", "put paper", "putting paper", "paper the",
                     "paper a wall", "papering", "ceiling", "ceilings", "size", "sizing", "how much",
                     "how much do i need", "choose", "which wallpaper", "what colour", "what color",
                     "border", "borders", "peel", "peeling", "lifting", "bubble", "bubbling",
                     "seam", "seams", "repair", "replace", "paint", "painting", "paint over",
                     "damp", "mould", "mold", "condensation", "phone", "iphone", "laptop",
                     "screen"),
              bias=1),
        entry("paint-over-gloss", (("paint over", "painting over", "paint on top of", "over gloss",
                                    "over the gloss", "over old paint", "gloss paint",
                                    "paint gloss", "paint a gloss", "undercoat", "primer",
                                    "priming"),
                                   ("gloss", "glossy", "satin", "sheen", "undercoat", "primer",
                                    "cupboard", "cupboards", "kitchen", "door", "doors",
                                    "woodwork", "skirting", "banister", "radiator")),
              "Sand it dull first: new paint needs a key to grip, so take the shine off old gloss with "
              "120 grit, wipe off the dust, then one coat of undercoat and your topcoat. A water-based "
              "satin goes on after the sanding alone and dries in a couple of hours; oil gloss straight "
              "onto old gloss is the way to get peeling in a year.",
              avoid=("what colour", "what color", "which colour", "which color", "colour",
                     "colours", "color", "colors", "peeling off") + _TAKING_PAINT_OFF),
        entry("paint-bathroom", (("paint", "painting", "repaint", "emulsion"),
                                 ("bathroom", "kitchen", "shower room", "steamy", "steam",
                                  "mould resistant", "mould-resistant", "mould proof")),
              "Use a mid-sheen, eggshell or bathroom paint rather than matt emulsion: it shrugs off "
              "steam and can be wiped, where matt goes patchy over a bath. Two coats is a day's work "
              "for a kitchen or bathroom. Paint does not stop mould on its own, so sort the extractor "
              "fan or open a window while you steam.",
              avoid=("what colour", "what color", "which colour", "which color", "colour",
                     "colours", "color", "colors", "mould on", "mould in", "black mould")
                    + _TAKING_PAINT_OFF),
        entry("paint-time", (("paint", "painting", "repaint", "decorate", "decorating",
                               "decorated", "emulsion", "walls"),
                              ("how long", "how many days", "how many hours", "time", "take",
                               "takes", "long", "day", "days", "weekend", "afternoon")),
              "A normal room is a day's work with two coats: an hour or two to cut in and roll, then "
              "about four hours before the second coat, so most people do the first coat in the "
              "evening and the second the next morning. A whole flat or house is roughly a day per "
              "room, plus a day for the ceilings and woodwork. A single door, a run of skirting or a "
              "radiator is a morning: an hour or two a coat, with overnight between the coats.",
              avoid=("how many coats", "coats of paint", "coat of paint", "between coats",
                     "recoat", "drying time", "how long to dry", "how long does paint take",
                     "how long does it last", "how long will it last", "last", "lasts",
                     "mould", "how much", "cost", "price", "pricey",
                     "to dry", "dry", "drying",
                     "old paint", "take old paint", "leftover paint", "left over paint",
                     "part used tin", "unused paint", "dispose", "disposal", "get rid of",
                     "getting rid of", "tip", "the tip", "recycling centre", "recycling center",
                     "household waste", "waste centre", "skip", "throw away", "throw out",
                     "throwing out", "goes", "where can i take", "where do i take",
                     "filler", "filling", "filled", "silicone", "sealant", "caulk",
                     "undercoat", "primer", "priming", "before painting", "before i paint",
                     "before sanding", "before i sand", "wait", "waiting", "to dry", "till it dries",
                     "before the second coat", "between coats"),
              ask=("how long", "how many", "time", "take", "takes", "day", "days", "hours",
                   "decorate", "decorating", "decorated"),
              bias=1),
        entry("paint-life",
              (("how long", "how many years", "how often", "lifespan", "life of", "last", "lasts",
                "lasted", "recoat"),
               ("paint", "painting", "painted", "repaint", "repainting", "emulsion", "gloss",
                "satin", "eggshell", "walls", "woodwork", "exterior", "outside")),
              "Interior emulsion on a sound wall is good for about five to ten years, and gloss on "
              "woodwork about the same; a steamy bathroom sits at the shorter end because the steam "
              "lifts the edges first. Pale colours fade slowly and dark ones show scuffs, so most "
              "rooms get a refresh coat at five years rather than a full repaint.",
              avoid=("to dry", "drying", "take to", "between coats", "how many coats", "coats",
                     "how long to dry", "mould", "cost", "price", "much does", "how long does it take")),
        entry("paint-coats", (("how many coats", "coats of paint", "coat of paint", "second coat",
                               "two coats", "how long between coats", "between coats", "recoat",
                               "drying time", "how long to dry", "how long does paint take",
                               "to dry", "take to dry", "long to dry"),
                              ("paint", "painting", "coat", "coats", "wall",
                               "walls", "emulsion", "door", "woodwork")),
              "Two coats on bare or patched plaster, and two whenever the colour changes; a pale wall "
              "going a pale colour can take one. Leave about two to four hours between coats, and a "
              "full day before you push furniture back against it. Touch the wall first: hard and not "
              "tacky means it is ready."),
        entry("plaster-dries", (("plaster", "plasters", "plastering", "plastered", "skim",
                                 "skims", "skimmed", "skimming", "render", "rendering",
                                 "plasterboard", "backing coat"),
                                ("dry", "dries", "drying", "to dry", "dried", "fully dry",
                                 "before i paint", "before painting", "before i can paint",
                                 "paint over it", "paint on it", "paint it", "mist coat",
                                 "when can i paint", "how long before", "wait", "cure",
                                 "curing")),
              "A thin skim is ready for a mist coat after two to four days and painted properly "
              "after about a week. A backing coat, or a wall taken back to brick, is roughly a "
              "week for every 10mm of thickness, so a fortnight or more. The colour is the best "
              "gauge - pale, chalky and the same all over means dry, and a patch that is still "
              "dark and cool has not finished, which wants a day or two more. Painting it before "
              "it has gone pale traps the water and blows the paint within a month.",
              avoid=("in plaster", "plaster on", "plaster cast", "cast", "surgery", "arm", "arms",
                     "leg", "legs", "wrist", "ankle", "knee", "bone", "bones", "broken",
                     "broke", "break", "fracture", "fractured", "hospital", "cut", "cuts",
                     "wound", "graze", "blister", "tooth", "teeth",
                     "what colour", "what color", "which colour", "which color", "colour",
                     "colours", "color", "colors", "how much", "cost", "price", "how many",
                     "wallpaper", "hang", "hanging", "strip", "stripping", "tiles", "tiling",
                     "tile the", "mould", "mold", "black mould", "condensation",
                     "damp", "dampness", "damp patch", "wet patch", "wet", "water", "leak",
                     "leaking", "stain", "stains", "yellow marks", "brown patch"),
              bias=2),
        entry("paint-streaks",
              (("paint", "painting", "painted", "repaint", "emulsion", "gloss", "satin", "eggshell",
                "undercoat", "topcoat", "roller", "brush", "decorating", "decorate",
                "the walls", "wall", "walls", "woodwork"),
               ("streak", "streaks", "streaky", "streaking", "patchy", "patchiness",
                "roller marks", "roller mark", "brush marks", "brush mark", "lap marks",
                "lap mark", "lines", "smooth", "smooth finish", "even finish", "finish",
                "uneven", "blotchy", "flashing", "shiny patches", "shiny patch",
                "without streaks", "without streak", "no streaks", "not streaky",
                "without brush marks", "no brush marks", "without roller marks",
                "no roller marks", "without lap marks", "no lap marks", "without lines",
                "no lines", "not patchy", "no patches", "without patches")),
              "Streaks are an uneven coat, not a bad paint: roll in strips a roller wide and lap the "
              "last strip while it is still wet so no edge dries alone, with a light even load rather "
              "than pressing the roller dry. Brush slowly, one way, and don't go back over paint that "
              "is setting. On a wall already patchy, a second full coat cures it; touching up spots "
              "makes it worse.",
              avoid=_TAKING_PAINT_OFF + (
                     "off", "clean", "cleaning", "wipe", "scrub", "scuff", "scuffs", "fingerprint",
                     "fingerprints", "stain", "stains", "stained", "crayon", "pencil", "pen",
                     "marker", "dirty", "grease",
                     "door", "doors", "ceiling", "ceilings", "skirting", "radiator", "radiators",
                     "tiles", "cupboard", "cupboards", "kitchen unit", "kitchen units", "shed",
                     "fence", "fencing", "deck", "decking", "garden", "furniture", "wardrobe",
                     "table", "chair", "chairs", "bathroom", "wallpaper", "woodchip",
                     "nails", "nail", "my nails", "toenails", "fingernails", "manicure",
                     "nail polish", "nail varnish", "polish", "pedicure")),
        entry("paint-brush-care",
              (("brush", "brushes", "paintbrush", "paintbrushes", "paint brush", "paint brushes",
                "brush bristles", "bristles", "bristle", "roller", "roller sleeve", "paint roller",
                "sleeve", "sleeves"),
               ("between coats", "between the coats", "overnight", "over night",
                "keep", "keeps", "keeping", "kept", "clean", "cleaning", "cleaned",
                "wash", "washing", "washed", "wash out", "washing out", "rinsed", "rinse",
                "gone hard", "went hard", "hard", "stiff", "dried out", "drying out", "dry out",
                "wrap", "wrapped", "cling film", "clingfilm", "carrier bag", "plastic bag",
                "save", "saved", "reuse", "re-use", "next coat", "tomorrow", "lunchtime",
                "white spirit", "turps", "brush restorer", "soak", "soaking",
                "out of", "get out", "got out", "get the paint out", "get paint out", "remove",
                "removing", "cleaned up", "clean up", "after painting", "once i have finished",
                "off a brush", "off my brush", "off the brush", "off a paintbrush",
                "off my paintbrush", "out of a brush", "out of my brush", "out of the brush",
                "out of my paintbrush", "out of a paintbrush", "out of the bristles",
                "off a roller", "out of a roller", "out of the sleeve", "get it off",
                "get the paint off", "paint off",
                "losing bristles", "loses bristles", "lose bristles", "lost bristles",
                "keeps losing", "keep losing", "losing hair", "sheds", "shedding", "shed",
                "falling", "falling out", "coming out", "keeps coming out",
                "bristles falling out", "bristles coming out", "loose bristles", "moulting",
                "falling apart", "falls apart", "coming apart", "comes apart")),
              _paint_brush_care, bias=3,
              ask=("how do i", "how to", "what do i do", "can i", "should i", "between coats",
                   "overnight", "store", "keeping", "keeping it", "clean", "cleaning", "wash",
                   "washing", "save", "reuse", "gone hard", "went hard", "hard", "stiff",
                   "dried", "dry", "wrap",
                   "losing", "loses", "lose", "lost", "sheds", "shedding", "shed", "moulting",
                   "falling", "coming out", "keeps coming out", "keeps losing", "keep losing",
                   "falling apart", "coming apart"),
              avoid=("hair", "my hair", "hairbrush", "hair brush", "curling", "straighteners",
                     "teeth", "toothbrush", "tooth", "gums", "makeup", "make up", "make-up",
                     "foundation", "blush", "eyebrow", "eyeliner", "nail brush", "nails",
                     "bbq", "barbecue", "grill brush", "chimney", "sweep", "yard", "broom",
                     "snow brush", "dog", "cat", "pet", "grooming", "canvas", "watercolour",
                     "watercolor", "sketch", "draw", "drawing", "brush up", "brush off",
                     "brush past", "brushed off", "paintbrush plant", "shaving brush",
                     "toilet brush", "bottle brush", "bottlebrush", "basting", "pastry brush",
                     "blind", "blinds", "curtain", "curtains", "shirt", "shirts", "jumper",
                     "jumpers", "cardigan", "fabric", "upholstery", "sofa", "settee", "carpet",
                     "carpets", "duvet", "bedding", "stain", "stains", "clothes", "clothing",
                     "shiny", "shine", "shines", "shone", "shininess", "scorch", "scorched",
                     "scotch", "jacket", "jackets", "blazer", "trousers", "skirt", "skirts",
                     "seat of my trousers")),
        entry("paint-spilt-on-a-soft-thing",
              (("paint", "paints", "emulsion", "gloss", "undercoat", "primer", "varnish",
                "gloss paint", "emulsion paint", "spilt paint", "spilled paint"),
               ("carpet", "carpets", "rug", "rugs", "sofa", "sofas", "settee", "couch", "cushion",
                "cushions", "mattress", "upholstery", "armchair", "stair carpet", "spilt", "spilled",
                "spill", "knocked over", "tipped over", "out of", "remove", "get out", "blot")),
              "Blot what is still wet with kitchen paper and do not rub it, because rubbing pushes the "
              "paint into the pile. Emulsion and the water-based satins lift with cold water and a "
              "little washing-up liquid worked in with your fingertips and blotted out again; oil "
              "gloss and varnish need a cloth damped with white spirit, dabbed from the edge of the "
              "mark inwards so it does not spread. Try white spirit on a corner you cannot see first, "
              "since on a wool carpet it can lift the dye.",
              avoid=("too dark", "darker", "too strong", "too bright", "too pale", "too orange",
                     "lighten", "lighter",
                     "wall", "walls", "ceiling", "door", "doors", "radiator", "skirting", "banister",
                     "window", "frame", "floor", "floors", "floorboards", "wood", "wooden",
                     "wallpaper", "clothes", "shirt", "jeans", "jumper", "trousers", "fabric",
                     "hand", "hands", "skin", "hair", "brush", "brushes", "paintbrush",
                     "paintbrushes", "paint brush", "paint brushes", "roller", "sleeve", "tray",
                     "thin",
                     "thinning", "dilute", "colour", "what colour", "which colour", "peeling",
                     "bubbling", "drying", "how long", "coats", "two coats",
                     "old paint", "leftover", "left over", "tin", "tins", "bin", "bins", "tip",
                     "household waste", "recycling", "recycle", "dispose", "disposal", "shed",
                     "garage", "store", "storing", "keeping",
                     "car", "cars", "van", "vans", "bodywork", "paintwork", "bumper",
                     "bonnet", "scratch", "scratches", "scratched", "scuff", "scuffs",
                     "lacquer", "alloy", "alloys", "wheel", "wheels"),
              bias=2),

        entry("paint-thin",
              (("thin", "thinning", "thinned", "water down", "watering down", "watered down",
                "dilute", "diluting", "diluted", "white spirit", "white spirit in"),
               ("paint", "painting", "emulsion", "gloss", "satin", "eggshell", "undercoat",
                "topcoat", "varnish", "primer", "matt", "matt emulsion", "oil based", "oil-based",
                "water based", "water-based")),
              "Emulsion thins with water, about one part to ten of paint; oil-based gloss thins with "
              "white spirit at much the same rate. Add it a little at a time and stir until the paint "
              "runs off the stick in a steady ribbon. A first mist coat on new plaster is thinner "
              "still, about 20 to 30 per cent water. Don't thin to stretch a tin: it covers less, and "
              "that is where streaks come from.",
              avoid=("hair", "thinning hair", "my hair", "gravy", "sauce", "soup", "blood",
                     "trees", "tree", "apples", "hedge", "hedges", "seedlings", "paint stripper",
                     "stripper", "remove", "stripping")),
        entry("paint-ceiling", (("paint", "painting", "repaint", "mist coat"),
                                ("ceiling", "ceilings", "ceiling rose", "ceiling.", "roller",
                                 "emulsion", "white", "cover", "two coats")),
              "Do the ceiling first and the walls after. Cut in round the edges with a brush and a 2cm "
              "band, then roll in strips about a metre wide with a long-handled roller, overlapping "
              "the last strip while it is still wet so the edges do not dry into lines. Work away from "
              "the window and towards the light so you can see where you have been, and roll the last "
              "metre without reloading to feather it out. Put a dust sheet down because a ceiling "
              "always drips. Matt emulsion, two coats, and a ceiling that is already white may need "
              "only one: if it is a bare or patched ceiling, thin the first coat by about a tenth as a "
              "mist coat.",
              avoid=_TAKING_PAINT_OFF + ("damp", "leak", "leaking", "water", "stain", "stains",
                                         "crack", "cracked", "crumbling", "flaking", "peeling",
                                         "coming off", "coming away", "come off", "comes off",
                                         "fell off", "falling off", "blown",
                                         "mould", "mold", "asbestos", "skim", "plaster",
                                         "insulate", "loft", "bulb", "light", "fan",
                                         "smoke alarm", "dryer", "colour", "color")),
        entry("paint-door", (("paint", "painting", "repaint", "gloss"),
                             ("door", "doors", "front door", "back door", "panelled door")),
              "Take the door off and lay it flat if you can, and paint the top and bottom edges first so "
              "it still fits after. Then the panels, then the frame parts, brushing with the grain. "
              "Lightly sand between coats and give gloss about 16 hours to harden before it goes back "
              "on its hinges.",
              avoid=("paint a room", "painting a room", "what colour", "which colour", "colour",
                     "sticking", "stiff", "squeak", "squeaking", "lock", "key", "handle",
                     "old paint", "hands", "hand", "fingers", "skin") + _TAKING_PAINT_OFF),
        entry("paint-radiator", (("paint", "painting", "repaint"),
                                 ("radiator", "radiators", "heated towel rail")),
              "Turn the heating off and let it go cold, then brush or roller it with a water-based "
              "satin, painting in the same colour as the wall if you want it to disappear. An old "
              "cast-iron radiator wants a metal primer first. Leave it a day to dry before the heat "
              "goes back on, or the paint softens.",
              avoid=_TAKING_PAINT_OFF),
        entry("paint-floor", (("paint", "painting", "repaint", "floor paint", "sand"),
                              ("floor", "floors", "floorboard", "floorboards", "floor boards",
                               "stairs", "staircase", "stair treads", "steps", "wooden floor")),
              "Sand a wooden floor back to bare wood, vacuum the dust off, then a primer and two thin "
              "coats of floor paint, keeping a wet edge so the overlaps do not show. Ordinary "
              "emulsion will scuff off in weeks, so use a paint made for floors, and leave it a full "
              "24 to 48 hours before anything walks on it - a stair run wants that on both sides of "
              "each tread.",
              bias=1,
              avoid=("squeak", "squeaks", "creak", "creaks", "clean", "cleaning", "mop", "mopping",
                     "laminate", "tile", "tiles", "tiling", "carpet", "underlay",
                     "sanding machine", "hire", "sander") + _TAKING_PAINT_OFF),

        entry("paint-concrete-floor", (("paint", "painting", "repaint", "floor paint", "etch",
                                        "seal", "epoxy"),
                                       ("concrete floor", "concrete floors", "garage floor",
                                        "garage floors", "concrete slab", "concrete steps",
                                        "concrete stairs")),
              "A concrete floor wants an etch and a paint made for it, not gloss: sweep and degrease "
              "it first, let it dry, then etch it with a weak acid or a floor etch from the paint "
              "shop so the paint has something to grip. Two coats of a garage-floor paint or a "
              "two-pack epoxy, rolled in one direction, with 12 to 24 hours between them, and keep "
              "feet and tyres off it for two or three days. Fresh concrete needs a month to cure "
              "before any of it, and a damp floor needs a damp-proof coat first.",
              bias=1,
              avoid=("squeak", "squeaks", "creak", "laminate", "tile", "tiles", "tiling", "carpet",
                     "floorboard", "floorboards", "wooden floor") + _TAKING_PAINT_OFF),
        entry("varnish-floor", (("varnish", "varnishing", "re-varnish", "revarnish", "lacquer",
                                 "stain", "staining"),
                                ("floor", "floors", "floorboard", "floorboards", "floor boards",
                                 "wooden floor", "stairs", "staircase", "stair treads", "steps")),
              "Sand the boards back to bare wood, vacuum and tack the dust off, then thin the first "
              "coat of varnish as the tin says and brush it with the grain. Three coats, with a "
              "light sand and a dust-off between each, and a full 24 hours between coats. A "
              "water-based varnish dries clear and does not yellow, so it suits pale wood; an "
              "oil-based one stands up better in a hall or on stairs but darkens pine. Keep the "
              "room ventilated and leave it two or three days before anything heavy walks on it.",
              bias=1,
              avoid=("squeak", "squeaks", "creak", "laminate", "tile", "tiles", "tiling", "carpet",
                     "concrete") + _TAKING_PAINT_OFF),
        entry("paint-skirting", (("paint", "painting", "repaint", "gloss", "satin"),
                                 ("skirting", "skirting board", "skirting boards", "architrave",
                                  "door frame", "banister", "banisters",
                                  "woodwork", "windowsill", "windowsills", "window sill",
                                  "window sills", "picture rail", "dado rail", "handrail",
                                  "window frame", "window frames", "sash", "sash window", "window",
                                  "windows", "casement")),
              "Sand them, wipe the dust off and run masking tape along the carpet, then brush with the "
              "grain in long strokes and a light load on the brush so it does not run onto the wall. "
              "Two thin coats beat one thick one, and satin or eggshell is easier to wipe than gloss. "
              "If you are doing the walls too, do the woodwork first.",
              ask=("how", "what", "which", "should", "can", "best", "way", "sand", "sanding",
                   "prep", "prepare", "method", "start", "need to", "give"),
              avoid=("clean", "cleaning", "dust", "dusty", "wipe") + _TAKING_PAINT_OFF),
        entry("paint-window", (("paint", "painting", "repaint", "gloss", "satin", "undercoat",
                                "primer"),
                               ("window", "windows", "sash", "sash window", "sash windows",
                                "casement", "casement window", "window frame", "window frames",
                                "frame", "frames", "sill", "window sill", "window sills")),
              "Mask the glass with tape, or cut in at a shallow angle with a 25mm brush and keep the "
              "brush lightly loaded so it does not run onto the pane, and paint the frame before the "
              "sliding parts. On a sash window do the staff beads and the pulley recess first, then "
              "the sashes. Run a knife round the join and open the window a crack while the paint is "
              "still soft, or it dries shut; outside wants an undercoat and two coats of gloss on a "
              "dry day.",
              avoid=("room", "rooms", "wall", "walls", "ceiling", "ceilings", "bedroom",
                     "living room", "hallway", "hall", "kitchen", "bathroom", "no window",
                     "no windows", "without windows", "windowless", "no natural light",
                     "clean", "cleaning", "cleaner", "dust", "dusty", "wipe", "condensation",
                     "misted", "leak", "leaks", "leaking", "damp", "draught", "draft", "cold",
                     "broken", "cracked", "crack", "shattered", "replacement", "replace", "tint",
                     "film", "frost", "blind", "blinds", "curtain", "curtains", "shutter",
                     "shutters", "stuck", "painted shut", "wont open", "won't open", "wont close",
                     "won't close", "acrylic", "acrylics", "watercolour", "canvas", "picture",
                     "painting of", "a painting") + _TAKING_PAINT_OFF,
              bias=2),


        entry("wallpaper-hang", (("hang", "hanging", "put up", "how do i paper", "paste the",
                                  "wallpaper", "wallpapering", "papering", "paper a", "paper the"),
                                 ("wallpaper", "wall paper", "lining paper", "a wall", "the wall",
                                  "wall", "walls", "ceiling", "ceilings", "room")),
              "Size the wall and let it dry, then cut each drop with an extra 5cm top and bottom, paste "
              "the paper (not the wall) and let it soak for the time the roll says, and hang the first "
              "drop plumb from a pencil line rather than from a corner. Smooth it outwards from the "
              "middle with a paper smoother, and butt the joins rather than overlapping them. A "
              "ceiling is the same paper on a bigger job: paper it before the walls, and work away "
              "from the window.",
              guard=_the_paper_is_in_the_line,
              avoid=("cheap", "which", "best", "bathroom", "mould", "mold",
                     "picture", "pictures", "frame", "frames", "photo", "photos",
                     "mirror", "mirrors",
                     "shelf", "shelves", "bracket", "brackets", "tv", "television", "telly",
                     "curtain", "curtains", "rail", "pole", "blind", "blinds", "coat", "coats",
                     "coat hook", "hook", "hooks", "light", "lights", "light fitting", "radiator",
                     "door",
                     "plasterboard", "plaster board", "stud", "studs", "rawlplug", "rawplug",
                     "hollow wall", "drill", "drilling", "fixings", "fixing",
                     "doors", "skim", "skimming", "damp", "stain", "paint", "painting", "painted",
                     "paint over", "paint on top",
                     "stripping", "remove", "removing", "off")),
        entry("paint-tiles", (("paint", "painting", "repaint"),
                              ("tile", "tiles", "tiling", "bathroom tiles", "kitchen tiles")),
              "Tiles take paint if you use a tile-specific primer and two coats of tile paint, and it "
              "holds up well on a splashback or a wall above a bath. Sand the glaze dull and clean off "
              "any grease first, or the paint peels in sheets. Not worth it on a shower floor or "
              "anywhere a foot or a scouring pad goes: re-tiling is the honest fix there.",
              avoid=("grout", "clean", "cleaning", "mould", "black", "cracked", "crack", "loose",
                     "tile a", "how do i tile", "floor") + _TAKING_PAINT_OFF),
        entry("paint-garden-wood", (("paint", "painting", "repaint", "stain", "varnish", "preserve",
                                     "preserver", "treat", "wood stain"),
                                    ("fence", "fences", "shed", "sheds", "gate", "gates", "trellis",
                                     "decking", "pergola", "garden furniture", "garden table",
                                     "garden bench", "greenhouse", "greenhouses")),
              "Wait for two dry days above about 10C and get the surface clean and bone dry before you "
              "start, because paint on damp timber peels within a season. Then two thin coats rather "
              "than one fat one: fence panels want a shed-and-fence stain, a shed or a wooden gate a "
              "preservative and a topcoat, and a metal gate a rust primer and a gloss made for metal. "
              "Brush or spray along the grain on wood.",
              bias=1,
              avoid=("garden table", "weed", "lawn", "grow") + _TAKING_PAINT_OFF),
        entry("paint-furniture", (("paint", "painting", "repaint", "gloss"),
                                  ("cupboard", "cupboards", "wardrobe", "table", "tables", "dresser",
                                   "chest of drawers", "sideboard", "bookcase", "shelves", "shelf",
                                   "furniture", "kitchen cabinets", "kitchen cupboard",
                                   "cabinet", "cabinets", "kitchen unit", "kitchen units",
                                   "unit", "units", "chair", "chairs", "stool", "stools",
                                   "bench", "benches", "desk", "desks", "bed", "beds",
                                   "bed frame", "cot", "cots", "crib", "cribs", "toy", "toys",
                                   "toy box", "chest", "trunk", "picture frame", "photo frame",
                                   "mirror frame", "dressing table", "bedside table", "drawers")),
              "Sand or de-gloss the surface, wipe the dust off, then a stain-blocking primer, then two "
              "thin coats of a water-based satin with a light sand between them. Take the doors and "
              "handles off if it has them, and let it harden a good 24 hours before anything goes back "
              "on: furniture paint that is rushed stays soft and sticks.",
              avoid=("clean", "cleaning", "smell", "musty", "grease", "polish", "wax", "dust",
                     "undercoat", "satin") + _TAKING_PAINT_OFF),
        entry("paint-flaking",
              (("flaking", "flaky", "flaking off", "flake off", "flakes off", "peeling off",
                "bubble", "bubbles", "bubble up", "bubbles up",
                "peels off", "peeled off", "peeling", "blistering", "blistered", "bubbling",
                "bubbled", "blown plaster", "coming off the wall", "coming off the ceiling",
                "coming away from the wall", "paint is flaking", "paint flaking",
                "paint is peeling", "paint peeling",
                "paint coming off", "paint is coming off", "paint come off",
                "paint comes off", "paint came off", "paint has come off",
                "paint coming away", "paint is coming away", "paint came away",
                "paint falling off", "paint is falling off", "paint fell off",
                "paint has fallen off"),
               ("paint", "painted", "painting", "emulsion", "gloss", "ceiling", "wall", "walls",
                "woodwork", "wood", "skirting", "door", "doors", "radiator", "plaster", "bathroom",
                "kitchen", "why", "what causes", "cause")),
              ("Find the reason before you repaint, or it comes back: feel the patch for damp (a "
               "bathroom, a kitchen or a ceiling under a cold roof is the usual one), and press the "
               "plaster - if it crunches or sounds hollow it has blown and needs cutting back to "
               "sound plaster and filling. Paint flakes off a ceiling most often because an old "
               "distemper or silk finish was painted over without a primer, or bare plaster was "
               "painted without a mist coat, so scrape back to the firm edge, sand the edge flat, "
               "and prime the bare patch before you paint. Then two coats of the same finish, and "
               "deal with the steam or the leak, because paint cannot hold on a wet wall."),
              bias=1,
              avoid=("remove", "removing", "removal", "strip", "stripping", "get off", "take off",
                     "my hands", "hands", "hand", "fingers", "skin", "nails", "brush", "brushes",
                     "roller", "tin", "tins", "clothes", "carpet", "splash", "spilled", "spilt",
                     "sand off", "scrape off", "how do i get", "nail polish", "nail varnish",
                     "old paint", "layers of paint", "years of paint",
                     "wallpaper", "wall paper", "skin", "hands", "brush", "nail", "nails",
                     "car", "cars", "metal", "gate", "fence", "shed", "boat", "kerb", "wheel",
                     "tile", "tiles", "tiling", "grout")),

        entry("paint-strip", (("remove", "removing", "strip", "stripping", "get off", "take off",
                               "sand off", "sanding off", "peel", "peeling", "flaking", "flaky",
                               "old paint", "layers of paint",
                               "off"),
                              ("paint", "painted", "gloss", "varnish", "emulsion", "woodwork", "wood",
                               "door", "doors", "skirting", "banister", "door frame",
                               "radiator", "tiles", "stair")),
              "Work out which paint it is first: a heat gun or a chemical stripper lifts old oil gloss "
              "in a few minutes, while a water-based paint softens under a warm damp cloth. Sandpaper "
              "alone clogs in seconds on a thick layer, so strip the bulk and sand only the last film. "
              "Test anything painted before about 1960 for lead - a kit costs a few pounds - and never "
              "sand that one.",
              avoid=("wallpaper", "wall paper", "stain", "stains", "nail polish", "nail varnish",
                     "why is", "why does", "why has", "why are", "what causes", "blistering",
                     "blistered", "bubbling", "bubbled", "keeps flaking", "keeps peeling",
                     "flaking off the wall", "flaking off the ceiling", "peeling off the wall",
                     "brush", "brushes", "roller", "hands", "hand", "fingers", "skin", "carpet",
                     "clothes", "shirt", "washing machine",
                     "off white", "off-white", "white", "colour",
                     "off to paint", "to paint it", "when painting", "before painting",
                     "before you paint", "to paint the",
                     "what do i do", "should i do", "what should i do", "do with", "get rid",
                     "in the bin", "put it in the bin", "where do i take", "throw", "throwing",
                     "chuck", "chucking", "bin it",
                     "dispose", "household waste", "recycling centre", "leftover", "tins", "pots",
                     "tin", "tins", "dispose", "disposal", "recycling centre", "tip",
                     "scratch", "scratches", "scratched", "scratching", "scuff", "scuffs",
                     "scuffed", "mark", "marks", "marked", "dent", "dents", "dented",
                     "chip", "chips", "chipped", "ring", "rings", "water mark", "heat mark",
                     "turn off", "turning off", "switch off", "switching off", "shut off",
                     "shutting off", "turn it off", "turn them off", "switch it off",
                     "turn the radiator off", "turn a radiator off", "turn a rad off",
                     "turn the heating off", "turn them down"),
              bias=1,
              ask=(("paint", "gloss", "varnish", "woodwork", "wood", "skirting", "banister",
                    "emulsion", "undercoat", "primer", "lacquer",
                    "finish", "finishes", "paintwork", "bare wood",
                    "strip", "strips", "stripping", "stripped", "sand", "sanding", "sandpaper"),)),
        entry("paint-on-hands", (("paint", "painting", "painted", "gloss", "emulsion", "varnish",
                                  "undercoat",
                                  "wood stain", "woodstain", "wood dye", "wood stain on"),
                                 ("hands", "hand", "fingers", "skin", "nails", "fingernails",
                                  "arms", "arms and hands")),
              "Warm water and washing-up liquid takes water-based paint off skin while it is still "
              "tacky, and a soft nail brush lifts it out of the ridges. Oil gloss wants a little white "
              "spirit or baby oil on a cloth, then soap, then a moisturiser, because both dry the skin "
              "out. Keep white spirit off your face, a cut or a child, and let the last flecks wear off "
              "rather than scrubbing at them.",
              avoid=("wall", "walls", "car", "furniture", "nails painted", "paint my nails",
                     "paint your nails", "paint a", "painting a"),
              bias=2),
        entry("red-wine-carpet", (("red wine", "wine"), ("carpet", "stain", "remove", "out", "spill")),
              "Blot it, don't rub, with kitchen paper, then pour on cold water and blot again, repeating "
              "until the water runs clear. A paste of bicarbonate of soda left on it for an hour pulls "
              "the rest out; white wine or salt are the old tricks and both work better than hot water.",
              ask=("carpet", "rug", "sofa", "couch", "cloth", "shirt", "dress", "tablecloth",
                   "spill", "spilt", "spilled", "stain", "stained"),
              avoid=("shirt", "shirts", "dress", "dresses", "blouse", "top", "tops", "jeans", "trousers",
                     "skirt", "sweater", "jumper", "sofa", "couch", "settee", "armchair", "upholstery",
                     "chair", "cushion", "cushions", "rug", "curtain", "curtains", "tablecloth",
                     "napkin", "duvet", "pillow", "bedsheets", "linen")),
        entry("rug-not-slipping",
              (("rug", "rugs", "mat", "mats", "runner", "runners", "doormat", "doormats",
                "carpet runner", "throw", "throws"),
               ("slip", "slips", "slipping", "slide", "slides", "sliding", "move", "moves", "moving",
                "shift", "shifting", "curl", "curls", "curling", "curled", "bunch", "bunching",
                "crease", "creases", "flat", "stay put", "stays put", "wont stay")),
              "Put a proper anti-slip underlay under it, the open-weave rubber sort, cut a couple of "
              "centimetres smaller than the rug, or run double-sided carpet tape along the edges: on a "
              "shiny floor the sticky corner pads do the job too. A rug that curls wants the curled end "
              "face down on the floor with something heavy on it overnight, or warmed with a hairdryer "
              "while you press it flat.",
              avoid=("clean", "cleaning", "wash", "washing", "shampoo", "stain", "stains", "stained",
                     "vacuum", "hoover", "smell", "smells", "smelly", "moth", "moths", "fade",
                     "faded", "colour", "color", "buy", "buying", "which", "best", "how much", "cost",
                     "price", "underlay", "new one", "shed", "sheds", "shedding", "underfloor",
                     "heating", "bath mat", "bathroom", "shower", "place mat", "placemat", "yoga",
                     "gym", "exercise", "mouse mat", "table mat", "towel", "iron", "ironing"),
              bias=1),
        entry("clean-furnishing",
              (("carpet", "carpets", "rug", "rugs", "mat", "mats", "sofa", "sofas", "couch", "settee",
                "armchair", "upholstery"),
               ("clean", "cleaning", "shampoo", "shampooing", "wash", "washing", "vacuum", "hoover",
                "dirty", "dirt", "freshen", "spring clean")),
              "Vacuum it first, then test any shampoo or foam cleaner on a hidden patch: a carpet wants a "
              "carpet shampoo worked in with a brush and rinsed, or a hired machine once or twice a year, "
              "and a sofa wants a foam cleaner and a soft brush with as little water as you can manage. "
              "Open the windows and dry it with the heating low, because anything left damp smells.",
              avoid=("red wine", "wine", "coffee", "tea", "cola", "juice", "nail polish", "nail varnish",
                     "blood", "paint", "oil", "petrol", "pet", "dog", "cat", "wee", "urine", "vomit",
                     "ink", "candle", "wax", "mark", "marks", "stain", "stains", "stained", "buy",
                     "buying", "which", "best", "underlay", "fitting", "fitted", "how much", "quote",
                     "leather", "suede", "new one", "cost", "price") + LETTING,
              bias=1),
        entry("carpet-stain",
              (("carpet", "carpets", "rug", "rugs", "mat", "mats"),
               ("stain", "stains", "stained", "mark", "marks", "spill", "spilled", "spillage",
                "remove", "get out", "get off", "mud", "blood")),
              "Blot, don't rub, with kitchen paper, then dab with cool water and a drop of washing-up "
              "liquid from the outside in, and blot dry with a towel; repeat until nothing more comes "
              "up. Work in small patches and never soak it, or the backing and underlay stay damp and "
              "start to smell. Grease wants neat washing-up liquid first, and a stain that survives all "
              "that is a job for a carpet cleaner.",
              avoid=("red wine", "wine", "coffee", "tea", "cola", "juice", "nail polish", "nail varnish",
                     "paint", "oil", "petrol", "pet", "dog", "cat", "wee", "urine", "vomit",
                     "ink", "candle", "wax", "turmeric", "buy", "buying", "which", "best", "underlay",
                     "fitting", "fitted", "how much", "quote", "vacuum", "hoover") + LETTING,
              bias=1),
        entry("sofa-stain",
              (("sofa", "sofas", "couch", "settee", "armchair", "upholstery", "footstool", "ottoman"),
               ("stain", "stains", "stained", "mark", "marks", "spill", "spilled", "spillage",
                "remove", "get out", "get off", "blood")),
              "Blot, don't rub, then dab with cool water and a drop of washing-up liquid from the "
              "outside in, and dry it with a towel rather than a hairdryer. Use as little water as you "
              "can, because a sofa takes days to dry and a damp one smells. A loose cover that unzips "
              "is better washed on its own; leather wants a barely damp cloth and saddle soap.",
              avoid=("coffee", "tea", "cola", "juice", "red wine", "wine", "nail polish", "nail varnish",
                     "buy", "buying", "which", "best", "new one", "replacement", "leather", "suede",
                     "how much", "cost", "price", "delivery", "second hand") + LETTING,
              bias=1),
        entry("grout-clean", (("grout", "tiles", "tile grout", "grouting"),
                              ("clean", "black", "mould", "dirty", "white", "whiten", "whitening",
                               "brighten", "yellow", "yellowed", "stained", "stain", "grimy", "grime",
                               "grout sealer", "sealer", "seal the grout", "sealing the grout",
                               "seal grout", "seal the tiles", "sealing the tiles", "seal tiles",
                               "seal my tiles", "sealing my tiles", "seal these tiles",
                               "scrub", "scrubbing", "brush", "steam", "steam cleaner",
                               "bathroom grout", "shower grout", "grout in the bathroom",
                               "grout in the shower",
                               "cracking", "cracked", "cracks", "crumbling", "crumbly",
                               "missing", "falling out", "falls out", "come out", "coming out")),
              "Scrub the grout with a paste of bicarbonate of soda and water and an old toothbrush, then "
              "rinse. For black mould in the grout, use a mould spray and leave it 10 minutes. To whiten "
              "grey grout, a paste of bicarbonate and a little white vinegar left on for ten minutes "
              "lifts most of it, and an oxygen bleach (the laundry stain remover kind) left overnight "
              "takes the rest. Sealing the grout once it is dry keeps it that way for a year or two, "
              "and a grout pen is the quick fix if it is only the colour that bothers you.",
              avoid=("paint tiles", "paint the tiles", "cover the tiles", "tile the",
                     "cracked tile", "cracked tiles", "tile cracked", "tiles cracked",
                     "tile is cracked", "tiles are cracked", "cracked wall tile",
                     "replace a cracked tile", "remove a cracked tile")),

        entry("loose-tile",
              (("tile", "tiles", "wall tile", "wall tiles", "floor tile", "floor tiles"),
               ("loose", "loosening", "loosened", "coming loose", "came loose", "comes loose",
                "come off", "came off", "coming off", "falling off", "fell off", "fallen off",
                "lifting", "lifted", "hollow", "drummy", "wobbly", "popping", "popped",
                "move when i press", "moves when i press", "adrift",
                "cracked", "crack", "cracks", "split", "smashed", "broken tile")),
              "Tap it with the handle of a screwdriver: a hollow ring means the adhesive has let go, "
              "so the tile has to come off and go back properly rather than be patched. Score the "
              "grout round it, ease a thin scraper behind a corner and lift it out, then scrape the "
              "old adhesive off both the tile and the wall, spread flexible tile adhesive over the "
              "whole back with a notched trowel, press it home with a slight twist and tape it in "
              "place overnight before you regrout the joints.",
              avoid=("lay", "laying", "tile a", "tiling a", "how do i tile", "start tiling",
                     "drill", "drilling", "screw", "hole", "hang", "hanging", "shelf", "mirror",
                     "clean", "cleaning", "cleaner", "grout pen", "mould", "mold", "black",
                     "whiten", "whitening", "paint", "painting", "cut", "cutting",
                     "chip", "chipped", "choose", "buy", "buying", "which", "best", "cost",
                     "price", "underfloor", "heat mat", "splashback")),
        entry("floor-scratch", (("floor", "wood", "laminate"), ("scratch", "scratched", "scuffs",
                                                                "marks")),
              "Rub a light scratch on a wooden floor with a walnut (really), or use a wax repair stick "
              "in a matching colour for deeper ones. On laminate, a scratch repair pen hides it, but "
              "only replacing the board fixes a deep gouge."),
        entry("hole-in-wall",
              (("hole", "holes", "dent", "dents", "crack", "cracks", "chunk", "gouge"),
               ("wall", "walls", "ceiling", "plaster", "plasterboard", "drywall", "skirting",
                "paper", "paint", "painted", "filler", "fill", "patch", "repair", "fix", "nail",
                "nails", "screw", "screws", "rawplug", "rawl plug")),
              "Push a bit of filler into the hole with a filling knife, leave it a little proud, and "
              "sand it flat once it is hard - two thin coats dry faster and sand better than one thick "
              "one. Anything bigger than a 50p piece, or a hole through plasterboard, wants a plasterboard "
              "patch stuck behind it and filled over before you paint. A crack wider than a couple of "
              "millimetres, or one that keeps coming back, is a builder's job rather than yours.",
              avoid=("jeans", "jumper", "sock", "socks", "shirt", "cardigan", "knee", "tights", "garment",
                     "darn", "sew", "sewing", "stitch", "fabric", "trousers", "pocket", "coat",
                     "phone", "screen", "mobile", "iphone", "laptop", "tablet", "tv", "telly",
                     "windscreen", "window", "glass", "car", "van",
                     "roof", "roofs", "tyre", "tyres", "tube", "inner tube", "bike", "bicycle"),
              bias=1),

        entry("fitting-repair",
              (("oven", "cooker", "cupboard", "cupboards", "cabinet", "cabinets", "wardrobe", "unit",
                "units", "shelf", "shelves", "shelving", "drawer", "drawers", "window", "windows",
                "sash", "casement", "tap", "taps", "faucet", "mixer"),
               ("hanging off", "hangs off", "hanging", "hang", "came off", "come off", "came loose",
                "come loose", "loose", "loosely", "wobbly", "wobbles", "rocks", "snapped", "snap",
                "broken", "broke", "cracked", "fell off", "fallen off", "sagging", "sags", "dropped",
                "wont shut", "won't shut", "wont close", "won't close", "doesnt shut", "doesn't shut",
                "wont stay shut", "won't stay shut", "wont stay closed", "won't stay closed",
                "swings open", "pops open", "keeps opening", "crooked", "out of line", "wont slide",
                "won't slide", "doesnt slide", "jammed", "adjust", "fix")),
              _fitting_repair,
              bias=2,
              avoid=("squeak", "squeaks", "squeaky", "squeaking", "creak", "creaks", "creaking",
                     "oil", "oiling", "rubbing", "rubs", "rattle", "rattles", "wind", "draught",
                     "draft", "sticking", "sticks",
                     "recipe", "recipes", "dinner", "lunch", "tea", "cook", "cooking", "meal", "meals",
                     "eat", "food", "fridge", "freezer", "microwave", "kettle", "dishwasher",
                     "washing machine", "tumble dryer", "dryer", "car", "van", "wheel", "wheels",
                     "pram", "pushchair", "trolley", "bike", "bicycle", "gate", "garage door",
                     "car door", "shower", "toilet", "bath", "boiler", "radiator", "my back",
                     "my knee", "my shoulder", "my neck", "my tooth", "my wrist", "my ankle",
                     "my hip",
                     "broken window", "window is broken", "window was broken", "broke my window",
                     "broke the window", "someone broke", "somebody broke", "smashed", "shattered",
                     "put through", "pane", "panes", "glass broke", "board up", "boarded up",
                     "expensive",
                     "rise", "rises", "risen", "rising", "prove", "proves", "proved", "proving",
                     "proof", "proofed", "dough", "sourdough", "loaf", "loaves", "yeast", "sponge",
                     "batter", "souffle", "soufflé", "pastry", "croissant", "meringue", "bake",
                     "bakes", "baked", "baking") + FITTING_SHARED_STANDDOWN),
        entry("drawer-runners-rub",
              (("drawer", "drawers", "cutlery drawer", "kitchen drawer", "bedside drawer",
                "chest of drawers", "dresser drawer", "bedroom drawer"),
               ("squeak", "squeaks", "squeaky", "squeaking", "rattle", "rattles", "rattling",
                "stiff", "sticking", "sticky", "sticks", "jammed", "jamming", "jams", "grind",
                "grinds", "grinding", "dragging", "drags", "rough", "wobble", "wobbles",
                "wobbly", "loose", "hard to open", "hard to pull", "hard to push", "wont open",
                "won't open", "stuck")),
              "Rub a candle, a dry bar of soap or a little beeswax along the wooden runners or the "
              "plastic slides, and never oil or grease - those hold the dust that makes it worse. "
              "If it rattles or grinds, tighten the runner screws at the back, one turn past "
              "finger-tight. A drawer that sticks only at the end is usually the side swelling in "
              "damp weather, so sand the top edge of the drawer side lightly and it stops catching.",
              avoid=("off the runner", "off the runners", "off its runner", "come off",
                     "came off", "replace", "replacement", "new runner", "fridge", "freezer",
                     "washing machine", "dishwasher", "microwave", "oven", "lock", "locked",
                     "key", "child lock", "hinge", "hinges"),
              bias=1),
        entry("door-creak",
              (("squeak", "squeaks", "squeaky", "squeaking", "creak", "creaks", "creaking",
                "sticking", "sticks", "stiff", "rubbing", "rubs", "drags", "dragging", "jammed",
                "jamming", "shut", "shuts", "closing", "hard to shut", "hard to close",
                "oil", "oils", "oiling", "oiled", "lubricate", "grease"),
               ("door", "doors", "hinge", "hinges", "latch", "window", "windows",
                "cupboard door", "gate", "front door")),
              "Oil the hinges: a drop of 3-in-1 or a spray of silicone on each hinge pin, then open and "
              "close the door a few times so it works in. If it sticks or rubs rather than squeaks it "
              "has usually dropped on its top hinge, so tighten the hinge screws - loose ones let the "
              "door drop - and if they spin, push matchsticks dipped in wood glue into the holes and "
              "screw back in. Rub a candle or a dry bar of soap on the latch plate or the top edge if "
              "that is the part catching.",
              avoid=("chat window", "chat box", "chat pane", "browser", "browser window",
                     "browser tab", "this chat", "the chat", "the app window",
                     "floorboard", "floorboards", "floor", "bed", "beds", "shoe", "shoes", "brake",
                     "brakes", "kettle", "bang", "bangs", "banging", "slam", "slams", "slamming",
                     "rattle", "rattles", "rattling", "wind", "windy", "draught", "trainer",
                     "trainers", "boot", "boots", "sandal", "flip flop", "chair", "chairs", "stairs",
                     "bike", "bicycle", "car", "van", "wheel", "wheels", "trolley", "pram",
                     "pushchair", "voice", "squeaky clean", "toy", "toys", "clean", "cleaning",
                     "grimy", "sticky", "grease off", "grease from", "grease out",
                     "paint", "painted", "washing machine", "dryer", "fridge", "freezer", "oven",
                     "dishwasher",
                     "locked", "lock", "cannot open", "cant open", "can't open", "slammed",
                     "broke in", "burglar", "forced", "off its hinges", "fell off", "get out",
                     "trapped", "inside", "fire", "smoke", "cant get out", "can't get out",
                     "sagging", "sagged", "sags", "sag", "hanging off", "hanging by",
                     "come off its hinge", "came off its hinge", "off its hinge", "loose hinge",
                     "loose hinges", "wont shut", "won't shut",
                     "mail", "junk", "junk mail", "leaflet", "leaflets", "flyer", "flyers",
                     "letter", "letters", "letterbox", "post", "postman", "delivery", "menu",
                     "cold callers", "salesman", "salesmen",
                     "wont stay shut", "won't stay shut", "wont stay closed", "won't stay closed",
                     "swings open", "hanging off", "hangs off", "cupboard shelf", "shelf has snapped"),
              bias=1),
        entry("floorboard-creak",
              (("floorboard", "floorboards", "floor", "stairs", "stair", "step", "landing"),
               ("creak", "creaks", "creaking", "creaky", "squeak", "squeaks", "squeaking",
                "squeaky", "noisy")),
              "Find the noisy board and work talcum powder, french chalk or graphite powder into the "
              "gaps between the boards - it stops the wood rubbing on the nail. If it still creaks, "
              "screw the board down again from above instead of nailing it, and on stairs check the "
              "treads are tight.",
              avoid=("clean", "cleaning", "mop", "scratch", "scratches", "polish", "paint"),
              bias=1),
        entry("carpet-clean",
              (("carpet", "carpets", "rug", "rugs"),
               ("smell", "smells", "smelly", "odour", "odors", "stink", "deep clean",
                "shampoo", "dirty", "stairs", "stair",
                "best way", "steam")),
              "Vacuum it twice, slowly, then work at any mark from the outside in with a little carpet "
              "shampoo on a cloth and blot it dry - a carpet that stays damp is what starts a smell. "
              "For a whole room or a set of stairs, a hired shampoo machine is worth it once a year, and "
              "open the windows while it dries.",
              avoid=("red wine", "wine", "coffee", "vomit", "pet", "dog", "cat", "car", "car mat",
                     "floor", "floorboards",
                     "musty", "damp"),
              bias=1),
        entry("wood-polish",
              (("table", "furniture", "sideboard", "cabinet", "chair", "desk", "dresser"),
               ("polish", "wax", "shine", "dull", "dullness", "restore", "oak", "wood", "wooden")),
              "Dust it, then work a hard wax polish or a beeswax-and-oil mix into the grain with a "
              "soft cloth, along the grain, and buff it off after ten minutes. Little and often beats "
              "a thick coat, which goes sticky and picks up dust.",
              avoid=("floor", "floorboards", "scratch", "wobble", "wobbly", "dent", "dents",
                     "gouge", "gouges", "chip", "chipped", "stain", "stained",
                     "off", "remove", "removing", "spilled", "spilt", "spillage", "marks",
                     "paint", "painting", "painted", "repaint"),
              bias=1),
        entry("wood-stain",
              (("table", "tables", "tabletop", "furniture", "sideboard", "cabinet", "desk", "dresser",
                "worktop", "wood", "wooden", "oak", "pine", "mahogany", "teak", "veneer"),
               ("stain", "stains", "stained", "water mark", "water marks", "watermark",
                "water ring", "water rings", "white ring", "white rings", "cup ring", "cup mark",
                "heat mark", "heat marks", "heat ring", "ring", "rings", "mark", "marks",
                "bloom", "milky")),
              "A white water ring or a heat bloom lifts with mayonnaise or petroleum jelly left on "
              "overnight, or with a hairdryer held 15 cm away for a few minutes. A cloth laid over a "
              "white ring with a warm iron pressed on it for a few seconds at a time does the same job "
              "when the first try does not. A dark stain has gone into the wood and wants sanding back "
              "and re-oiling, and ink lifts with a little methylated spirit on a cloth, along the "
              "grain, before you polish the whole top so the shine matches.",
              avoid=("floor", "floors", "floorboard", "floorboards", "laminate", "scratch",
                     "scratches", "scratched", "scuff", "scuffs", "scuffed",
                     "dent", "dents", "gouge", "chip", "chipped", "wobble",
                     "wobbly", "loose", "car", "van", "phone", "screen", "shirt", "clothes", "clothing",
                     "carpet", "rug", "sofa", "upholstery", "wall", "paint", "gravy", "wine", "coffee",
                     "tea", "oil", "varnish", "remove the wax", "wax off",
                     "hands", "hand", "fingers", "skin", "nails", "arms",
                     "glass", "glasses", "glass table", "glass top", "glass tabletop", "marble",
                     "stone", "granite", "quartz", "slate"),
              bias=1),
        entry("wood-chip-fill",
              (("chip", "chips", "chipped", "gouge", "gouged", "chunk", "splinter", "splintered"),
               ("wood", "wooden", "woodwork", "table", "tables", "dresser", "sideboard", "desk", "oak",
                "pine", "walnut", "mahogany", "teak", "veneer", "furniture", "door", "worktop")),
              "A chipped edge or a gouge in wood is a filler job: press a two-part wood filler or a wax "
              "repair stick into it, a little proud of the surface, and sand or shave it flat once it is "
              "hard, then colour it with a touch of wax or stain. Keep the sanding to the filler - "
              "sanding the finish around it leaves a pale patch you cannot hide.",
              avoid=("potato", "potatoes", "fries", "fry", "oven", "pan", "oil", "air fryer", "airfryer",
                     "fish", "supper", "takeaway", "tooth", "teeth", "filling", "dentist", "dental",
                     "phone", "screen", "glasses", "windscreen", "window", "paint", "nail", "nails",
                     "varnish", "paintwork", "car", "cars", "mug", "cup", "plate", "bowl",
                     "bbq", "barbecue", "barbeque", "smoker", "smoking", "smoked", "smoke",
                     "wood chips", "woodchips", "chips for", "pellet", "pellets", "fire pit",
                     "chiminea", "pizza oven", "grill", "grilling", "burn", "burning"),
              bias=2),
        entry("wood-dent",
              (("dent", "dents", "dinked", "gouge", "gouged"),
               ("wood", "wooden", "woodwork", "table", "dresser", "sideboard", "desk", "oak", "pine",
                "floorboard", "floor")),
              "A shallow dent in bare wood comes back up with water and heat: wet the spot, lay a damp "
              "cloth over it and press a hot iron on for a few seconds at a time, checking as you go. "
              "Once the wood has a finish on it a dent cannot be raised, so the repair is filler, sand "
              "and a matching wax or varnish.",
              avoid=("car", "cars", "van", "bumper", "wing", "bonnet", "door", "panel", "phone",
                     "screen", "fridge", "freezer", "washing machine", "drum")),
        entry("chair-wobble",
              (("chair", "chairs", "table", "tables", "desk", "desks", "stool", "bench",
                "furniture", "leg"),
               ("wobble", "wobbly", "wobbles", "loose", "rock", "rocks", "rocking", "rickety", "fix")),
              "Turn it over and find the loose joint: usually one leg has worked free of the seat. "
              "Squeeze wood glue into the joint, push it home and clamp it - a strap or a rope round "
              "all four legs works - and leave it overnight. Tighten any screws and add a bracket if "
              "the same joint keeps going.",
              ask=("wobble", "wobbly", "wobbles", "wobbling", "loose", "rock", "rocks",
                   "rocking", "rickety"),
              avoid=("chair for", "garden chair", "high chair", "wheelchair", "office chair"),
              guard=_a_chair_and_not_a_body),
        entry("a-fan-that-rocks",
              (("fan", "fans", "ceiling fan", "desk fan", "pedestal fan", "floor fan", "tower fan",
                "standing fan", "extractor fan", "heater", "fan heater", "fridge", "freezer",
                "appliance", "appliances"),
               ("wobble", "wobbles", "wobbling", "wobbly", "shakes", "shaking", "shaky", "rocks",
                "rocking", "walks", "walking", "jumps", "jumping", "vibrates", "vibrating",
                "moves about", "not level", "off balance", "uneven", "unsteady", "wonky",
                "tilts", "leaning")),
              _the_fan_stopped,
              ask=("wobble", "wobbles", "wobbling", "wobbly", "shakes", "shaking", "rocks",
                   "rocking", "walking", "jumps", "vibrates", "unsteady", "wonky", "tilts",
                   "stop it", "stop the", "why does", "fix"),
              avoid=("hands", "hand", "fingers", "arms", "voice", "feel shaky", "shaky hands",
                     "chair", "chairs", "table", "tables", "stool", "stools", "bench",
                     "sofa", "wardrobe", "door", "gate", "shelf", "shelves", "washing machine",
                     "washer", "dryer", "laptop", "computer", "pc", "phone", "car", "bike",
                     "steering", "baby", "dog", "cat", "puppy", "noise", "noisy", "rattle",
                     "rattles", "rattling", "grind", "grinding", "hum", "humming", "buzz",
                     "click", "clicks", "clicking", "squeak", "squeaks", "squeaking", "whine",
                     "whirr", "knock", "knocks", "knocking", "bang", "bangs", "banging",
                     "thump", "thumping", "scrape", "scraping",
                     "leak", "leaking", "smell", "smells", "not cold", "no power",
                     "how much", "cost", "electricity", "petrol"),
              bias=1),
        entry("chair-broken",
              (("chair", "chairs", "table", "tables", "desk", "desks", "stool", "stools", "bench",
                "benches", "furniture", "bed", "beds", "sofa", "sofas", "couch", "couches",
                "settee", "settees", "shelf", "shelves", "cupboard", "cupboards", "drawer",
                "drawers", "wardrobe", "wardrobes"),
               ("broken", "broke", "snapped", "cracked", "split", "hurts", "hurting", "sore",
                "aching", "aches",
                "is broken", "is cracked", "is snapped", "is split", "has broken", "has snapped",
                "has cracked", "has split")),
              "Turn it over or open it up and see what has gone: a leg that has snapped wants the old "
              "glue drilled out, a wooden dowel or a longer screw and wood glue in the joint, clamped "
              "overnight. A cracked seat, back or shelf wants a bracket underneath and a screw through "
              "the split, and a split frame is usually cheaper to replace than to mend. Take the "
              "weight off it until the glue has set.",
              ask=("broken", "broke", "snapped", "cracked", "split", "hurts", "hurting", "sore",
                   "aching", "aches"),
              avoid=("chair for", "garden chair", "high chair", "wheelchair", "office chair",
                     "my leg", "my back", "my arm", "my wrist", "my ankle", "my knee", "my neck",
                     "my shoulder", "my hip", "hurts my",
                     "refund", "return", "returns", "money back", "shop", "store", "retailer",
                     "receipt", "guarantee", "warranty", "bought", "i paid", "reject",
                     "months old", "weeks old", "under a year", "still under",
                     "after a week", "after a month", "after two weeks", "after 2 weeks",
                     "after a few days", "after 3 weeks", "last week", "last month",
                     "hurt", "hurts", "hurting", "sore", "aching", "aches",
                     "booked a table", "book a table", "booking a table", "reserved a table",
                     "reserve a table", "table for two", "table for four", "table for 4",
                     "table for six", "table for 6", "restaurant", "reservation",
                     "dinner reservation"),
              guard=lambda understood: not the_stomach_is_what_it_is_about(understood),
              bias=4),
        entry("thing-part-hurts",
              (tuple(sorted(THING_PARTS)),
               ("hurt", "hurts", "hurting", "ache", "aches", "aching", "achy", "sore", "stiff",
                "pain", "pains", "painful", "twinge", "twinges", "throbbing")),
              "A part that hurts rather than has snapped is usually loose at its joint: tighten the "
              "screws or bolts, check the bracket and the glue line, and keep the weight off it until "
              "it feels firm. If it moves when you lean on it, treat it as a break - drill out the old "
              "glue, fit a wooden dowel or longer screw, and clamp it overnight.",
              bias=3,
              guard=lambda understood: (_a_thing_owns_the_part(understood)
                                        and not the_stomach_is_what_it_is_about(understood)),
              avoid=("pipe", "pipes", "wire", "wires", "wiring", "boiler", "radiator", "radiators",
                     "drain", "drains", "tap", "taps", "socket", "sockets", "toilet", "sink",
                     "washing machine", "fridge", "freezer", "oven", "hob", "shower", "door",
                     "window", "lock", "locks")),
        entry("bath-seal",
              (("bath", "baths", "bathtub", "bath tub", "shower tray", "shower base", "bath panel",
                "bathroom seal", "silicone", "silicon", "sealant", "mastic"),
               ("seal", "sealing", "sealed", "reseal", "re seal", "re-seal", "silicone", "sickaflex",
                "mould", "mold", "black", "gaps", "gap", "water getting behind", "leaking", "leak",
                "coming away", "peeling", "replace", "replacing", "strip", "stripping", "around",
                "along", "edge", "edges")),
              "Cut the old silicone out and scrub the joint back to dry, grease-free tile and bath "
              "before anything else, because fresh silicone will not stick to the old. Fill the bath "
              "with water first, so the bead is made at the weight it has to carry, then run anti-mould "
              "silicone along it and smooth it with a wet finger or a tool. Leave it 24 hours before "
              "you let the water out, and it will not part from the bath in a month.",
              avoid=("fill", "filling", "filler", "drain", "draining", "slow", "blocked", "hot water",
                     "cold", "not hot", "boiler", "tap", "taps", "shower", "shower not working",
                     "paint", "painting", "bath bomb",
                     "tile the", "tiling the", "tiling a", "how do i tile", "grout the",
                     "regrout", "re-grout", "grouting the")),

        entry("toilet-seat-wobble",
              ("toilet seat", ("wobble", "wobbles", "wobbly", "loose", "loosening", "coming loose",
                               "moves", "moving", "slides", "sliding", "not tight", "fix", "tighten",
                               "broken", "cracked")),
              "Tighten the two bolts under the seat where the hinges meet the pan: they are usually "
              "plastic nuts you can turn by hand from underneath, and a quarter turn each side takes "
              "the movement out. If the seat still slides it is the hinge, and a replacement seat with "
              "a top-fix kit is about £10 to £20 and fits in ten minutes without getting under the "
              "pan. If the holes in the hinge have gone oval, a wipe of plastic wood in them holds the "
              "screws again.",
              bias=1),
        entry("washer-wobble",
              (("washing machine", "washer"),
               ("wobble", "wobbles", "wobbly", "shaking", "shakes", "vibrating", "vibration",
                "walking", "moves", "moving", "banging", "noisy", "noise", "spinning", "loud")),
              "Level it first: the machine must not rock on the floor, so turn the front feet out until "
              "it sits flat on all four and lock the nuts. If it is new, the four transport bolts at "
              "the back have to come out or the drum is still locked to the frame. After that, an even "
              "load stops most of it - mix towels with lighter things rather than washing one heavy "
              "item - and check the shipping bolts are the right length for a laminate floor.",
              avoid=("tumble dryer", "tumble dryers", "dryer", "dryers", "washer dryer",
                     "washer-dryer", "condenser",
                     "move house", "moving house", "moving flat", "move flat", "new flat",
                     "new house", "new home", "upstairs", "downstairs", "van", "removals",
                     "take it with me", "moving it", "moving the machine", "moving my",
                     "isnt spinning", "isn t spinning", "not spinning", "no spin", "wont spin",
                     "won t spin", "wont turn", "won t turn", "drum isnt", "drum not")),
        entry("curtain-measure",
              (("curtain", "curtains", "blind", "blinds", "drapes"),
               ("measure", "measuring", "how wide", "how long", "buy", "size", "sized", "fit",
                "hanging", "hang")),
              "Measure the pole or track, not the window, and add 10 to 20cm either side so the "
              "curtains cover the edges when closed. For the length, measure from the pole to where "
              "you want them to finish, then double the width for a full gather: one and a half times "
              "the width looks skimped.",
              bias=1),

        entry("hang-picture", (("picture", "mirror", "shelf", "shelves", "shelf unit",
                                "floating shelf", "brackets",
                                "tv", "television", "telly", "coat hook", "coat hooks", "frame",
                                "frames", "picture rail",
                                "tv on the wall", "tv on a wall", "wall mounted tv", "wall-mount tv",
                                "mount a tv", "mount the tv", "tv bracket", "television on the wall",
                                "wall bracket",
                                "nail", "nails", "rawlplug", "rawlplugs", "rawl plug", "rawl plugs",
                                "rawplug", "rawplugs", "wall plug", "wall plugs", "anchor",
                                "anchors", "fixing", "fixings"),
                               ("hang", "hanging", "wall", "drill", "heavy",
                                "plaster wall", "plaster walls", "plasterboard wall", "brick wall",
                                "brick", "chimney breast", "lath and plaster", "no studs",
                                "put up", "putting up", "fixings", "fixing", "fix", "mount",
                                "attach", "level", "stud", "studs", "plasterboard",
                                "need", "needs", "needed", "buy", "buying", "should i get",
                                "what size", "which one",
                                "for", "into", "in a wall")),
              "It is the fixing that matters, not the drill: find the studs with a stud finder or by "
              "tapping, and screw into one where you can. On plasterboard use proper hollow-wall "
              "fixings, not a bare rawl plug, for anything over a couple of kilos, and a shelf wants a "
              "bracket every 60cm or so. Two hooks 10cm apart keep a picture level far better than "
              "one. Check for pipes and wires before you drill, and check it with a spirit level "
              "before you tighten anything up.",
              avoid=("writing", "sentence", "sentences", "sentenced", "essay", "essays", "grammar",
                     "punctuation", "comma", "commas", "paragraph", "paragraphs", "spell",
                     "spelling", "english", "algebra", "algebraic", "maths", "math", "equation",
                     "equations", "expand", "expanding", "simplify", "multiply", "x", "xy",
                     "tax", "taxed", "income", "salary", "wage", "wages", "band", "bands",
                     "percentage", "percent", "40k", "20k", "50k",
                     "file", "files", "clippers", "clipper", "polish", "varnish", "manicure",
                     "pedicure", "gel", "acrylic", "bitten", "biting", "cut my", "trim my",
                     "grow", "growing", "grew", "peeling", "ridges", "ridged", "fungus", "fungal",
                     "toenail", "toenails", "fingernail", "fingernails", "thumbnail", "toe", "toes",
                     "finger", "fingers", "nail fold", "ingrown")),
        entry("energy-bill", (("energy", "electric", "electricity", "gas", "heating", "utility",
                               "fuel",
                               "bill", "bills",
                               "hot water", "hot-water",
                               "boiler", "thermostat", "radiator", "radiators", "flow temperature"),
                              ("bill", "bills", "cheaper", "reduce", "lower", "save", "cost",
                               "expensive", "price", "tariff", "spend less", "keep warm", "warm",
                               "massive", "huge", "enormous", "sky high", "through the roof",
                               "so big", "big", "bigger", "high",
                               "waste", "wasting", "wasted", "stop wasting",
                               "turn down", "turn it down", "turn up", "turn it up", "how low",
                               "pay", "paying", "paid", "payment", "direct debit", "instalments",
                               "installments",
                               "save on", "save money on", "cut my", "cut the",
                               "cheap to heat", "cheaper to heat", "get it cheaper",
                               "spend less", "spend less on")),
              "Heating and hot water are most of the bill, so start there: on gas, turn the boiler flow "
              "temperature down to 55 to 60C and heat only the rooms someone is in; all electric, put "
              "the immersion and any room heaters on a timer for the hours you actually use. Then "
              "standby and lighting, which is about a quarter, so switch off at the wall. Ask your "
              "supplier in writing for the standing charge and unit rate of their cheapest tariff; a "
              "fixed deal usually beats the standard variable one.",
              avoid=("smell", "leak", "leaking", "fumes", "carbon monoxide", "myself", "baby",
                     "turn down a radiator", "turn down the radiator", "one radiator",
                     "rad valve", "radiator valve", "trv", "thermostatic valve",
                     "turn my heating", "turn down my heating", "turn up my heating",
                     "turn our heating", "turn down our heating", "turn up our heating",
                     "toddler", "child", "clammy", "flue", "pilot light",
                     "car", "vehicle", "blanket", "shower", "bike", "bicycle", "scooter",
                     "heater to buy", "which",
                     "hob", "hobs", "induction", "oven", "ovens", "cooker", "cook", "cooking",
                     "can't pay", "cant pay", "afford", "debt", "arrears", "final notice",
                     "wrong", "mistake", "council tax", "tax", "water", "water bill", "phone",
                     "why is my", "why has my", "why did my", "why are my", "why does my", "why so",
                     "haggle", "haggling", "haggled", "better price", "lower price",
                     "leaving it on", "leaving the heating on", "leaving the boiler on",
                     "left on all day", "on all the time", "on all day", "does it save",
                     "point of leaving",
                     "restaurant", "restaurants", "waiter", "waitress", "split the bill",
                     "split bill", "the bill at the", "meal out", "card slip", "takeaway",
                     "cafe", "pub", "bistro", "pizzeria",
                     "mobile", "broadband", "tv licence", "licence", "rent", "insurance",
                     "switch", "switching", "tariff", "tariffs", "standing charge", "fixed deal",
                     "fixed tariff", "fixed rate", "worth",
                     "pay", "paying", "paid", "payment", "direct debit", "debit", "payment plan",
                     "how do i pay", "way to pay")),
                entry("heating-all-day",
              (("heating", "central heating", "boiler", "radiators", "radiator", "hot water",
                "thermostat", "heating system"),
               ("all day", "all evening", "leave it on", "leave on", "leaving on", "left on",
                "leave the heating on", "leaving the heating on", "left the heating on",
                "leave my heating on", "keep the heating on", "keeping the heating on",
                "heating on all day", "heating on all the time", "heating on low", "heating on at night",
                "on low", "all the time", "constant", "always on", "overnight", "timer",
                "programmer", "time clock", "when im out", "when i am out", "out at work",
                "out all day", "turn it off", "turn off", "switch it off", "switching it off",
                "come home", "coming home")),
              "No, it is not cheaper, for the heating or the hot water: keeping a house warm all day "
              "costs more than heating it when you are in it, and it shows on the bill. Every degree "
              "the rooms are held at is heat leaking out through the walls, so the timer wins - on an hour before you get up, off half an hour before bed, 18C in "
              "the living room and 16C in the bedrooms while you are up. Coming home to a cold house "
              "is a comfort problem rather than a cost one, and it is cheaper to warm the room you "
              "sit in for an hour than to keep the whole house up from midday. Hot water is the same "
              "story: heat the cylinder for an hour morning and evening with a jacket on it rather "
              "than leaving the immersion on. The exception is a well-insulated house on a heat "
              "pump, which is cheaper held at a steady low temperature than pushed up and down.",
              avoid=("broken", "not working", "isnt working", "isn't working", "fault", "faulty",
                     "no hot water", "cold water", "pressure", "bleed", "bleeding", "cold at the",
                     "radiator is cold", "radiators are cold", "noise", "noisy", "banging", "kettle",
                     "leak", "leaking", "smell", "carbon monoxide", "frost", "frozen", "condensation",
                     "mould", "damp",
                     "what temperature", "how warm", "degrees", "what should i set", "set the",
                     "set my", "set it to", "how hot",
                     "bill", "bills", "tariff", "supplier", "standing charge", "price cap", "switch",
                     "switching", "smart meter", "can't pay", "cant pay", "afford", "debt",
                     "arrears", "council tax", "which boiler", "new boiler", "buy", "buying",
                     "worth getting", "service", "servicing",
                     "a cold", "my cold", "got a cold", "with a cold", "bad cold", "cold and flu",
                     "sore throat", "sneezing", "cough", "flu", "unwell", "sick", "chesty",
                     "cat", "cats", "dog", "dogs", "puppy", "kitten", "pet", "pets",
                     "baby", "babies", "baby's", "newborn", "toddler", "cot", "nursery",
                     "why is my heating", "why does my heating", "why is the heating",
                     "why does the heating", "comes on by itself", "coming on by itself",
                     "on by itself", "keeps coming on", "wont go off", "won't go off",
                     "why is my boiler", "why does my boiler", "why is the boiler",
                     "why does the boiler", "why has my boiler", "why is my boiler on",
                     "boiler is always on", "boiler is on all", "boiler always on",
                     "boiler keeps", "boiler wont turn off", "boiler won't turn off",
                     "wont turn off", "won't turn off", "wont switch off", "won't switch off",
                     "will not turn off", "will not switch off", "does not turn off",
                     "doesnt turn off", "doesn't turn off", "can not turn", "cannot turn",
                     "cant turn it off", "can't turn it off", "cant turn off", "can't turn off",
                     "cant switch it off", "cant switch it off", "cant switch off",
                     "cant turn the heating off", "cant get it to go off",
                     "stuck on", "is stuck", "has stuck", "programmer is wrong",
                     "wrong time", "wrong times",
                     "go away", "going away", "gone away", "away for", "when im away",
                     "when i am away", "when were away", "while im away", "while i am away",
                     "while were away", "on holiday", "holiday", "empty house", "house is empty",
                     "nobody in", "no one in", "not at home for",
                     "pipe", "pipes")),
        entry("heating-while-away",
              (("heating", "central heating", "boiler", "radiators", "radiator", "hot water",
                "thermostat", "heating system", "immersion", "pipes"),
               ("go away", "going away", "gone away", "away for", "when im away",
                "when i am away", "when were away", "while im away", "while i am away",
                "while were away", "on holiday", "holiday", "empty house", "house is empty",
                "nobody in", "no one in", "not at home for", "leave it on when",
                "leave the heating on when", "leave my heating on when", "turn it off when",
                "pipe", "pipes")),
              "Leave it on low rather than off if it will be cold: 12 to 15C, or the thermostat's "
              "frost setting, costs a few pounds a week and is far cheaper than a burst pipe, which "
              "is what a hard frost does to a cold house. Turn the water off at the stopcock before "
              "you go as well, and hot water can be switched off entirely. For a summer trip, or a "
              "house that will not drop below about 5C, off is fine.",
              avoid=("broken", "not working", "fault", "faulty", "leak", "leaking", "noise",
                     "noisy", "banging", "kettle", "carbon monoxide", "smell", "bleed",
                     "bleeding", "pressure", "condensation", "mould", "damp", "bill", "bills",
                     "tariff", "switch", "supplier", "standing charge", "price cap", "afford",
                     "debt", "arrears", "what temperature", "how warm", "degrees",
                     "what should i set", "how hot", "baby", "babies", "newborn", "toddler",
                     "cat", "cats", "dog", "dogs", "puppy", "kitten", "pet", "pets",
                     "why is my boiler", "why does my boiler", "stuck on", "wont turn off",
                     "will not turn off", "comes on by itself", "on by itself")),
        entry("cheapest-hours", (("electricity", "energy", "power", "electric", "washing machine",
                                  "washer", "washers", "dishwasher", "tumble dryer", "dryer",
                                  "drier", "oven", "cooker", "appliance", "appliances",
                                  "immersion", "hot water", "economy 7", "economy7", "off peak",
                                  "off-peak", "time of use",
                                  "laundry", "washing", "the washing", "put the washing",
                                  "a wash", "the wash", "wash a load", "a load of washing",
                                  "load of laundry", "clothes wash",
                                  "do laundry", "laundry overnight", "washing overnight"),
                                 ("cheapest", "cheaper", "cheap", "cheaply", "night", "overnight",
                                  "at night", "off peak", "off-peak", "economy 7", "economy7",
                                  "time of use", "best time", "what time", "delay", "timer", "timed",
                                  "low rate",
                                  "morning", "in the morning", "evening", "in the evening",
                                  "afternoon", "in the afternoon", "during the day")),
              "Night is cheaper only on a two-rate tariff such as Economy 7 or an EV one; on a "
              "single rate the hour makes no difference at all, so check the tariff name on your "
              "bill. Where there is a cheap window, usually about half past midnight to half seven "
              "and charged at roughly a third to a half of the day rate, put the washing machine and "
              "the dishwasher on a delay. Whatever the tariff, never leave the tumble dryer running "
              "overnight, because of the fire risk.",
              guard=lambda understood: not asks_where(understood),
              avoid=("tired", "tiredness", "tiring", "exhausted", "drained", "knackered",
                     "sluggish", "flagging", "sleepy", "no energy", "low on energy",
                     "low in energy", "energy levels", "my energy", "afternoon slump",
                     "cant keep my eyes open", "keep falling asleep", "always tired", "so tired",
                     "feel flat", "feeling flat", "run down", "worn out", "burned out",
                     "burnt out",
                     "car", "vehicle", "blanket", "shower", "bike", "bicycle", "buy", "buying",
                     "best washing machine", "best dishwasher", "best dryer", "best tumble dryer",
                     "best oven", "best appliance", "best brand", "best buy", "best value",
                     "which washing machine", "which dishwasher", "which dryer", "which appliance",
                     "which", "boiler", "radiator",
                     "pay", "paying", "paid", "payment", "direct debit", "debit", "standing charge",
                     "how do i pay", "way to pay", "supplier", "bill", "bills",
                     "hob", "hobs", "induction", "cook with", "cooking with", "gas or electric",
                     "electric or gas", "gas hob", "gas oven", "electric oven",
                     "gas or electricity", "electricity or gas", "cheaper than electricity",
                     "cheaper than gas", "cheaper to heat", "cheapest way to heat",
                     "which is cheaper", "compare gas", "gas vs", "gas versus",
                     "put a chicken", "put the chicken", "chicken in", "turkey", "chicken",
                     "roast", "roasting", "joint of", "casserole", "cake", "baking", "bake",
                     "scones", "biscuits", "pizza", "lasagne", "how long", "how many minutes",
                     "gas mark", "preheat", "at 180", "at 190", "at 200", "at 220",
                     "smell", "smells", "smelling", "smelly", "musty", "stink", "stinks",
                     "stinky", "mouldy", "mildew", "damp wash", "service wash", "fluff", "lint",
                     "stain", "stains", "stained", "shrunk", "shrink", "shrinking", "gone grey",
                     "gone greyish", "went grey", "yellowed", "bobbled", "pilling", "oil stain",
                     "grease stain", "sweat", "blood", "sick", "nappy", "nappies"),
              bias=1),
        entry("cold-house-even-with-the-heating-on",
              (("cold", "colder", "freezing", "chilly", "perishing", "never gets warm",
                "never warms up", "wont get warm", "won't get warm", "not getting warm",
                "not warming up", "wont warm up", "won't warm up", "doesnt get warm",
                "doesn't get warm", "lukewarm"),
               ("house", "home", "flat", "room", "rooms", "bedroom", "living room", "sitting room",
                "kitchen", "heating on", "heating is on", "heatings on", "radiators are on",
                "radiator is on", "the heating", "central heating", "upstairs", "downstairs",
                "shed", "sheds", "cellar", "cellars", "basement", "basements", "workshop",
                "workshops", "garage", "garages", "conservatory", "loft", "attic", "outbuilding",
                "outbuildings", "hallway", "porch", "caravan", "bungalow", "cottage")),
              ("Usually one of four things, and the cheap checks come first. Feel the radiator in "
               "the cold room: cold at the top is air, so bleed it; hot at the top and cold at the "
               "bottom is sludge; and a thermostatic valve turned right down or stuck shut does the "
               "same. Then look at where the thermostat sits - in a cold hall, or near a radiator "
               "or a window, it reads the wrong room and stops the heating before the bedrooms get "
               "warm. Then the boiler's flow temperature: 55 to 60C suits a condensing boiler, and "
               "set much lower than that the radiators never get hot enough on a cold day. If all "
               "that is right the heat is leaving - draughts under the doors, an open chimney, the "
               "loft hatch, and loft insulation under 270mm - and that is what to spend on next."),
              bias=1,
              ask=("even with", "with the heating", "heating is on", "heating on", "heatings on",
                   "heating is running", "heating is going", "radiators are on", "radiator is on",
                   "turned up", "turn it up", "on full", "full blast", "all day", "all the time",
                   "never gets warm", "never warms up", "not getting warm", "why is", "why are",
                   "why does", "why do", "why wont", "why won't", "why am i"),
              avoid=("should i put the heating on", "should i turn the heating on",
                     "shall i put the heating on", "shall i turn the heating on",
                     "do i need to put the heating on", "do i need the heating on",
                     "is it worth putting the heating on", "worth putting the heating on",
                     "what temperature", "what should i set", "how warm should",
                     "no heating", "heating is off", "heating off", "heating not working",
                     "heating isnt working", "heating isn't working", "heating has stopped",
                     "heating stopped", "heating wont come on", "heating won't come on",
                     "heating broken", "heating is broken", "broken boiler", "boiler is broken",
                     "pressure", "gauge", "fault code", "locks out", "wont fire", "won't fire",
                     "cold at the top", "cold at the bottom", "at the top", "at the bottom",
                     "bleed", "bleeding", "radiator key", "thermostatic valve",
                     "insulation", "loft insulation", "cavity wall", "double glazing",
                     "draught", "draughts", "draft", "drafts",
                     "i am", "im ", "i feel", "always cold", "my feet", "my foot", "my hands",
                     "my hand", "fingers", "toes", "baby", "babies", "newborn", "toddler",
                     "disabled", "elderly", "pensioner", "old", "sick", "ill",
                     "car", "cars", "van", "engine", "washing machine", "oven", "microwave",
                     "food", "reheat", "leftovers", "tea", "coffee", "bath", "shower",
                     "pool", "greenhouse", "shed", "caravan", "hot tub",
                     "bill", "bills", "cost", "cheap", "cheaper", "cheapest", "afford",
                     "price", "quote", "tariff", "energy")),
        entry("heat-a-room", (("heat", "heating", "warm", "warmer", "warmth", "cold", "freezing",
                               "chilly", "perishing",
                               "like a fridge", "like a freezer", "like an ice box", "ice box",
                               "icebox", "like the arctic", "colder than a fridge",
                               "like a cold store",
                               "no heating", "heating off", "without heating",
                               "keep warm", "keeping warm", "stay warm", "staying warm"),
                              ("room", "rooms", "one room", "house", "home", "flat", "bedroom",
                               "living room", "sitting room", "tonight",
                               "kitchen", "bathroom", "garage", "conservatory", "shed",
                               "hall", "hallway", "spare room", "loft", "attic", "office",
                               "cellar", "basement", "outbuilding", "outbuildings", "workshop",
                               "porch", "caravan",
                               "in here", "in this room", "this room"),
                              ("without heating", "without the heating", "without central heating",
                               "heating off", "no heating", "without putting the heating on",
                               "keep warm", "keeping warm", "stay warm", "staying warm",
                               "warm the", "warm my", "warm our", "warm this", "warm a",
                               "warm this room", "warm that room", "warm up the room",
                               "warm up the house", "warm up the flat", "warm up my",
                               "warm up our",
                               "heat the", "heat my", "heat our", "heat a", "heat this",
                               "heating the", "heating my", "heating our", "heating a",
                               "cheaply", "cheaper", "cheapest", "afford")),
              "Heat the room you are sitting in and shut the door: a 1kW electric radiator warms a "
              "small room for about 25p an hour, usually less than running the whole boiler for one "
              "person, and a heated throw costs about 3p an hour. Then stop the losses, a few pounds "
              "each: a brush strip on the door, a chimney balloon, foil behind the radiator. If the "
              "central heating is on, keep the flow at 55 to 60C and heat only the rooms you use.",
              avoid=("lonely", "loneliness", "empty", "miss him", "miss her",
                     "since he", "since she", "passed away", "died", "funeral", "boiler", "radiator",
                     "bill", "bills", "mould", "damp", "carbon monoxide",
                     "have a cold", "has a cold", "had a cold", "having a cold", "ive got a cold",
                     "i ve got a cold", "got a cold", "my cold", "his cold", "her cold",
                     "with a cold", "bad cold", "down with a cold", "a cold coming", "cold coming on",
                     "cold and flu",
                     "sore throat", "sneezing", "cough", "flu", "temperature", "unwell", "sick",
                     "cool", "cooler", "cooling", "keep cool", "keep it cool", "stay cool",
                     "heatwave", "heat wave", "hot weather", "hot day", "hot nights",
                     "keep the heat out", "heat out", "stop the sun", "sun heating", "block the sun",
                     "the sun coming in", "sun comes in", "sun through",
                     "cycling", "cycle", "bike", "bicycle", "motorbike", "motorcycle",
                     "scooter", "ride", "riding", "commute", "commuting", "run", "running",
                     "jog", "jogging", "walk", "walking", "hike", "hiking", "football",
                     "rugby", "match", "watching", "touchline", "sidelines", "fishing",
                     "golf", "ski", "skiing", "camping", "festival", "outdoors", "outside",
                     "dog walk", "school run",
                     "car", "cars", "van", "vehicle", "motorhome", "caravan", "washing machine",
                     "washer", "dishwasher", "tumble dryer", "dryer", "drier", "cooker",
                     "shower", "bath", "hot tub", "pool", "swimming", "greenhouse", "hot water",
                     "immersion", "water", "kettle",
                     "leftover", "leftovers", "soup", "reheat", "reheating", "microwave",
                     "warm up before", "warming up before", "warm up prevent", "warming up prevent",
                     "before a run", "before exercise", "prevent injury", "prevent injuries",
                     "bedroom", "bedrooms", "bed room", "for sleep", "sleeping", "sleep in",
                     ) + THE_APPLIANCE_ITSELF,
              guard=lambda u: _a_room_being_heated(u)
              and not_the_heat_of_an_argument(u)),
        entry("tap-loose",
              (("tap", "faucet", "mixer tap", "monobloc"),
               ("loose", "wobble", "wobbles", "wobbly", "moves", "moving", "swivels", "spins",
                "spinning", "swinging", "not fixed", "come away", "came away", "lifted")),
              "A tap that wobbles is held by one nut underneath: get under the sink and tighten the "
              "back nut on the threaded shank with a basin wrench or a long spanner, or the fixing "
              "plate on a monobloc. Once it is tight, check the two flexible tails have not started "
              "to weep. If the nut has pulled the thread through a thin worktop, a repair plate costs "
              "a few pounds and spreads the load.",
              avoid=("drip", "dripping", "leak", "leaking", "pressure", "hot water", "cold",
                     "scale", "limescale")),
        entry("cupboard-door-hinge",
              (("cupboard door", "cupboard doors", "cabinet door", "kitchen door", "kitchen doors",
                "hinge", "hinges", "door hanging", "door dropped"),
               ("hanging off", "hang off", "hangs off", "hanging", "loose", "dropped", "sagging",
                "sag", "came off", "come off", "falling off", "screws", "screw", "pulled out",
                "stripped", "wont close", "won't close", "rubbing")),
              "Tighten the screws holding the hinge plate first, and if they spin, take them out and "
              "pack the holes with two broken matchsticks and wood glue before driving them back in. "
              "For a door that has dropped, the two screws nearest the door edge lift it: slacken the "
              "outer ones and turn the inner ones to raise the front. Move the plate 20mm up or down "
              "only if the wood has gone."),
        entry("heating-on-by-itself",
              (("heating", "boiler", "radiators", "radiator", "central heating"),
               ("by itself", "on its own", "comes on", "come on", "came on", "turns on", "turned on",
                "random times", "middle of the night", "at night", "when i havent", "even when its off",
                "when its off",
                "always on", "always hot", "always running", "on all the time",
                "running all the time", "wont turn off", "won't turn off", "wont go off",
                "won't go off", "wont switch off", "won't switch off", "wont shut off",
                "never turns off", "never goes off", "not turning off", "keeps running",
                "keeps firing", "keeps going", "stays on", "staying on", "on in the summer",
                "hot in the summer", "stuck on", "jammed on", "still on", "left on",
                "on all day", "on all night",
                "will not turn off", "will not go off", "will not switch off",
                "will not shut off", "will not stop", "doesnt turn off", "doesn't turn off",
                "doesnt go off", "doesn't go off", "never off", "never stops", "non stop")),
              "Check the programmer first: a light on ADVANCE or ON rather than AUTO is a button "
              "pressed by accident, and a room thermostat left high keeps the heating running. If "
              "the radiators heat up when the hot water is on, the diverter valve has stuck and wants "
              "replacing - about 150 to 250 pounds fitted, and worth doing before winter. A frost "
              "stat firing on a cold night is normal.",
              avoid=("not working", "broken", "cold", "no heating", "pressure", "noise", "noisy",
                     "bleed", "banging", "kettling", "thermostat setting", "how much",
                     "cost", "costs", "expensive", "bill", "bills", "cheaper", "save",
                     "saving", "money", "efficient", "efficiency", "how long", "every day",
                     "safe", "safety", "unsafe", "dangerous", "risk", "carbon monoxide",
                     "smell gas", "yellow flame", "leave it on"),
              bias=3),
        entry("door-rubbing", (("door", "doors", "front door", "back door", "shed door",
                                "bedroom door", "bathroom door", "internal door", "cupboard door"),
                               ("sticking", "sticks", "stuck", "rubbing", "rubs", "dragging", "drags",
                                "scrapes", "swollen", "swelling", "swelled", "warped", "wont close",
                                "won't close", "wont shut", "won't shut", "hard to close", "catching",
                                "jammed", "have to slam", "has to be slammed")),
              "A door that drags or will not shut is usually swollen from damp in winter, or has "
              "dropped on its hinges because a screw pulled out. Give the season a fortnight first, "
              "with the heating on or a dehumidifier in the room, because many free up on their own. "
              "If it has dropped, tighten the top hinge screws, or replace them with longer ones. "
              "Otherwise take a millimetre at a time off the edge where the paint has rubbed bright, "
              "and seal the bare wood afterwards so it does not take in water and swell again.",
              bias=3,
              avoid=("lock", "locks", "key", "keys", "car", "cars", "van", "fridge", "freezer",
                     "oven", "microwave", "dishwasher", "washing machine", "washer", "dryer",
                     "drawer", "drawers", "cupboard", "wardrobe", "glass", "window", "windows",
                     "dog", "dogs", "puppy", "barking", "bark", "barks", "cat", "cats", "meowing",
                     "neighbour", "neighbours", "neighbor", "neighbors", "next door", "upstairs",
                     "downstairs", "shut up",
                     "key", "keys", "lock", "locks", "keyhole", "barrel", "handle", "latch")),
        entry("door-lock-stiff", (("lock", "locks", "door lock", "barrel", "deadlock", "yale",
                                   "latch", "key", "keys", "front door",
                                   "key in the lock", "key into the lock", "key in my lock",
                                   "key wont go in", "key won't go in", "key does not go in",
                                   "get my key in", "get the key in"),
                                  ("stiff", "sticky", "stuck", "sticking", "sticks", "jammed",
                                   "hard", "wont turn",
                                   "won't turn", "grinding", "tight", "difficult", "gritty",
                                   "wont go in", "won't go in", "turning",
                                   "stiffen", "stiffens", "stiffened",
                                   "seizing", "seized", "grates", "grating", "rough",
                                   "in the lock", "into the lock", "in my lock", "into my lock",
                                   "get my key in", "get the key in")),
              _door_lock_stiff,
              bias=2,
              avoid=("car", "cars", "van", "bike", "bicycle", "suitcase", "case", "padlock", "safe",
                     "lost", "lost my keys", "locked out", "locked in", "keys locked", "cut a key",
                     "laptop", "keyboard", "password", "account", "windows", "drawer", "lockbox",
                     "post box", "postbox")),
        entry("key-broken-in-lock",
              (("key", "keys", "door key", "front door key", "spare key", "piece of key",
                "half a key", "broken key", "key blade"),
               ("snapped", "snap", "snapped off", "snapped in", "broke off", "broken off",
                "broke in", "broken in", "sheared", "twisted off", "bent", "stuck", "jammed",
                "stuck in the lock", "stuck in my lock", "jammed in", "half in", "get it out",
                "get out", "remove", "removing",
                "out of the lock", "out of my lock", "out of the door", "out of the barrel",
                "pull out", "pull it out", "dig out", "extract", "extracting", "out of")),
              "Stop turning it: the piece in the barrel is what the pins are holding, and every "
              "extra turn pushes it further in. Put a drop of WD-40 or graphite at the keyway, then "
              "grip whatever is proud with needle-nose pliers or thin side cutters, pull straight "
              "out rather than sideways, and jiggling the door handle while you pull helps. A short "
              "piece just inside can be walked out with the thin blade of a jigsaw or a coping saw "
              "slid alongside it. If it is in past the face of the barrel, it is a locksmith: about "
              "\u00a360 to \u00a3120 to drill and replace the cylinder, and keep the door on the "
              "latch until they come. Do not glue anything to it and do not push a second key in.",
              avoid=("car", "cars", "van", "bike", "bicycle", "motorbike", "suitcase", "padlock",
                     "safe", "laptop", "keyboard", "password", "account", "phone", "lost",
                     "lost my keys", "mislaid", "locked out", "locked in", "cut a key", "spare key",
                     "cut a spare", "piano", "map", "answer", "code"),
              bias=3),
        entry("lost-house-keys",
              (("keys", "key", "keyring", "key ring", "house keys", "door key", "front door key",
                "keys to the house", "set of keys"),
               ("lost", "lose", "losing", "mislaid", "misplaced", "missing", "gone",
                "cant find", "cannot find", "can't find", "no idea where", "nowhere",
                "without the key", "without a key", "without my keys", "without keys",
                "without the keys", "no key", "dont have the key", "don't have the key",
                "not got the key", "havent got the key", "haven't got the key")),
              _lost_keys,
              avoid=("stiff", "sticky", "jammed", "wont turn", "won't turn", "hard to turn",
                     "grinding", "piano", "keyboard", "laptop", "computer", "password",
                     "account", "map", "answer", "code", "locked in", "locked out",
                     "cut a key", "cut a spare", "car battery", "remote", "fob battery",
                     "in the house", "in my house", "in the flat", "in my flat", "at home",
                     "somewhere in", "in my bag", "in my pocket", "in the car", "in the office",
                     "down the back of"),
              bias=2),

        entry("change-a-lock", (("lock", "locks", "door lock", "cylinder", "euro cylinder",
                                 "barrel", "mortice", "mortise", "deadlock", "night latch", "yale"),
                                ("change", "changing", "replace", "replacing", "fit", "fitting",
                                 "new", "broken", "broke", "snapped", "put on", "install", "myself",
                                 "upgrade", "key", "keys", "how"),
                                ("change a lock", "change the lock", "change my lock",
                                 "change the lock", "change the locks", "replace a lock",
                                 "replace the lock", "new lock", "fit a lock", "fit a new lock",
                                 "broken lock", "lock broken", "change the barrel",
                                 "change the cylinder")),
              "Measure the old cylinder before you buy one: the length each side of the fixing screw, "
              "and whether it sits flush with the door or sticks out. Undo the retaining screw on the "
              "door edge, put the key in and turn it slightly, and the cylinder slides out; the new one "
              "goes in the same way, with the key in it. Fifteen minutes with a screwdriver, the door "
              "left open while you work, and about fifteen to thirty pounds for a kite-marked one.",
              bias=2,
              avoid=("car", "cars", "van", "bike", "bicycle", "suitcase", "padlock", "safe",
                     "locked out", "locked in", "keys locked", "cut a key", "spare key", "laptop",
                     "phone", "keyboard", "password", "account", "windows", "drawer", "lockbox",
                     "post box", "postbox", "stiff", "jammed", "wont turn", "won't turn",
                     "sticking", "sticks", "stuck", "hard to turn", "gritty", "grinding",
                     "screen", "sim", "pin", "app",
                     "locked myself out", "lock myself out", "locks myself out", "locking myself out",
                     "locked out of", "lost my keys", "lost the keys", "open a locked", "locked door",
                     "wont open", "won't open",
                     "who do i call", "who should i call", "who can i call", "who could i call",
                     "who do i ring", "who should i ring", "who to call", "who to ring",
                     "who do i get", "someone to call", "someone to ring", "locksmith",
                     "sticking", "sticks", "stuck in the lock", "stuck in my lock",
                     "get my key in", "get the key in", "cant get my key", "can't get my key",
                     "key wont go in", "key won't go in", "key does not go in", "key in",
                     "key stuck", "key snapped", "key broke", "key broke off", "broken key",
                     "snapped off", "snapped in", "broke off in", "broke in the lock",
                     "half a key", "piece of key", "jammed in the lock", "key jammed")),
        entry("stop-locking-yourself-out",
              (("locked myself out", "locking myself out", "lock myself out", "locks myself out",
                "locked out again", "lock myself out again", "keys locked inside",
                "keys locked in the house", "keys locked in my flat", "keys are locked inside",
                "keep locking myself out", "always locking myself out", "keys locked in",
                "leave my keys", "left my keys", "forget my keys", "forgot my keys"),
               ("stop", "again", "keep", "keeps", "always", "how do i", "how can i", "prevent",
                "avoid", "happen", "happening", "trick", "not do it")),
              "Put the key in one place that you walk past on the way out - a hook inside the front "
              "door - and nowhere else, because the pockets, the bag and the coat are what lose it. A "
              "spare with a neighbour or family is free and saves the locksmith, and a key safe by the "
              "door (about twenty pounds, screwed on, with a code) covers the rest. If you rent, ask "
              "the landlord for a second key: yours to pay for, and almost always allowed.",
              bias=1,
              ask=("stop", "stops", "prevent", "avoid", "keep on", "keep", "keeps", "always",
                   "never again", "trick", "habit", "how do i not", "how can i not"),
              avoid=("car", "cars", "van", "vehicle", "boot", "phone", "screen", "sim", "pin",
                     "password", "account", "email", "facebook", "laptop", "change the lock",
                     "new lock", "broken lock", "lost my keys", "lost the keys", "cant find",
                     "can't find")),
        entry("door-handle-loose", (("handle", "handles", "door handle", "knob", "knobs",
                                     "door knob", "latch", "spindle", "grub screw"),
                                    ("loose", "wobbly", "wobbles", "wobble", "rattles", "rattle",
                                     "spins", "spinning", "fallen off", "fell off", "came off",
                                     "come off", "dropped")),
              "The grub screw on the neck of the handle has worked loose: there is a small screw there, "
              "sometimes under a cap you can flick off, and tightening it onto the spindle takes two "
              "minutes with a small screwdriver or an Allen key. If it keeps coming loose, put a dab of "
              "thread-lock on the spindle, or a sliver of tape. A handle that spins without opening the "
              "door has lost or snapped its spindle, and a new handle is about ten pounds.",
              avoid=("suitcase", "bag", "case", "pan", "saucepan", "frying pan", "pot", "cup", "mug",
                     "tap", "taps", "kettle", "oven", "fridge", "freezer", "drawer", "window",
                     "wheelbarrow", "lawnmower", "drill", "tool", "bike", "car", "doorbell",
                     "knife", "saw", "umbrella")),
        entry("window-painted-shut", (("window", "windows", "sash", "sash window", "casement",
                                       "upvc window", "upvc windows"),
                                      ("painted", "stuck", "seized", "jammed", "swollen",
                                       "stiff")),
              "It is paint gluing the sash to the frame: run a sharp knife, held flat, round the join "
              "between the frame and the opening sash to cut the paint film, then work a thin scraper "
              "or a wide chisel gently into the gap and ease the window open rather than forcing the "
              "handle. Once it is open, sand the paint off the meeting faces and rub a candle or "
              "silicone spray along them. Never lever against the glass.",
              bias=1,
              avoid=("car", "cars", "van", "screen", "phone", "laptop", "computer", "software",
                     "browser", "windscreen", "shower", "clean", "cleaning", "curtain", "curtains",
                     "blind", "blinds",
                     "paint a room", "painting a room", "paint the room", "painting the room",
                     "paint a wall", "paint a ceiling", "decorating", "decorate", "roller",
                     "undercoat", "emulsion", "paint the walls", "no window", "no windows",
                     "without a window", "windowless",
                     "paint a window", "painting a window", "paint my window", "paint the window",
                     "paint window", "painting the windows", "paint the windows", "repaint",
                     "painting a window frame", "paint a window frame", "brushes", "brush",
                     "paint a sash", "painting a sash", "paint the sash", "paint a casement",
                     "paint the frame")),
        entry("door-slam-wind", (("door", "doors", "front door", "back door", "porch", "gate"),
                                 ("slam", "slams", "slamming", "bangs", "banging", "bang", "rattles",
                                  "rattling", "wind", "blows")),
              "A door that slams in the wind wants a holder or a closer, not a shut window: a "
              "hook-and-eye or a door holder on the frame keeps it open, and an overhead closer set to "
              "slow the last few inches stops it banging shut. Rubber bumpers on the stop take the "
              "rattle out of the catch, and a wedge under the bottom holds a door that swings. A front "
              "door that rattles is usually the latch plate, and a wrap-around striker plate or a strip "
              "of foam behind it stops that.",
              bias=2,
              avoid=("car", "cars", "van", "garage", "cupboard", "fridge", "oven", "microwave",
                     "washing machine", "dishwasher", "drum", "tumble dryer", "doorbell", "baby",
                     "toddler", "child",
                     "swollen", "swelling", "swelled", "warped", "sticking", "stuck", "rubbing",
                     "drags", "dragging", "have to slam", "has to be slammed",
                     "draught", "draughts", "draft", "drafts", "draughty", "drafty", "cold air",
                     "cold coming", "lets in", "letting in", "coming under the door",
                     "under the door", "around the door", "round the door", "draught excluder",
                     "excluder",
                     "my finger", "my fingers", "my thumb", "my hand", "my toe", "my foot",
                     "fingernail", "fingernails", "toenail", "toenails", "nail", "nails",
                     "black", "bruise", "bruised", "purple", "blood",
                     "slammed the door", "slams the door", "door on me", "door in my face")),
        entry("door-wont-open", (("wont open", "won't open", "will not open", "wont budge",
                                  "won't budge", "cant open", "can't open", "cannot open",
                                  "stuck", "stuck shut", "jammed", "jammed shut", "locked",
                                  "locked in", "locked in my flat", "locked in my house",
                                  "locked in the house", "locked in my room", "trapped in my flat",
                                  "shut in my room", "swollen", "swelled", "warped",
                                  "cant get out", "can't get out", "wont turn", "won't turn",
                                  "wont close", "won't close",
                                  "cant get in", "can't get in", "cannot get in", "wont let me in",
                                  "won't let me in", "key wont work", "key won't work"),
                                 ("door", "doors", "front door", "back door", "door lock",
                                  "the lock", "latch", "handle", "deadlock", "mortice", "yale",
                                  "shed door", "porch")),
              "Start with the lock: press the door inwards while you turn the handle, and try "
              "lifting the handle up, because plenty of doors lock that way and half a turn frees "
              "them. If the handle turns loosely and nothing clicks, the spindle inside has gone "
              "and that is a locksmith. A door swollen by damp usually frees with a firm push at "
              "shoulder height while someone turns the handle, or with a thin card slid in on the "
              "latch side; if it will not shut at all, plane a millimetre off the edge that rubs. "
              "If it is rented, ring the landlord or a locksmith who quotes on the phone - and if a "
              "child or anyone is shut in, ring 999 rather than fight the door.",
              avoid=("squeak", "squeaks", "squeaky", "squeaking", "creak", "creaks", "creaking",
                     "key in the", "key into the", "get my key", "getting my key", "keyway",
                     "key wont go", "key won't go", "wont go in", "won't go in",
                     "oil", "oiling", "hinge oil", "draught", "draughts", "draft", "paint",
                     "painting", "painted", "decorate", "decorating", "letterbox", "letter box",
                     "childproof", "child proof", "cat flap", "pet flap", "car door", "van door",
                     "garage door", "keypad", "porch light", "doorbell", "door bell", "camera",
                     "handle a", "difficult", "slam", "slamming", "bang", "bangs",
                     "oven", "cooker", "fridge", "freezer", "microwave", "washing machine",
                     "dishwasher", "tumble dryer", "cupboard", "wardrobe", "cabinet"),
              bias=1),
        entry("hinge-sag",
              (("hanging off", "hanging by", "hanging open", "sagging", "sag", "sags",
                "has dropped", "had dropped", "is dropping", "keeps dropping", "drooping", "loose",
                "loosened", "wobbly", "wobbling", "wobble",
                "coming off", "came off", "fallen off", "fell off", "pulled out", "ripped off",
                "blown down", "blew down", "blown off", "knocked down", "snapped", "broken",
                "breaks", "broke", "split"),
               ("gate", "gates", "garden gate", "side gate", "gate post", "shed door", "shed",
                "door", "doors", "cupboard", "cupboards", "cupboard door", "cabinet",
                "cabinet door", "wardrobe", "wardrobe door", "hinge", "hinges", "gate post",
                "gatepost")),
              "Nine times in ten a sagging gate, shed door or cupboard door is a hinge screw that has "
              "pulled out of the wood, not the hinge wearing out. Take the weight off the free "
              "corner, pack the old screw holes with glued matchsticks or a sliver of dowel and screw "
              "back in, or move the hinge 10cm along with longer screws. If the wood round the hinge "
              "is rotten or the hinge is torn, fit a new hinge onto sound timber - and if the post "
              "moves in the ground, brace or replace the post.",
              ask=("hinge", "hinges", "hinged", "gate", "gates", "garden gate", "side gate",
                   "shed door", "shed", "door", "doors", "cupboard", "cabinet", "wardrobe",
                   "gate post", "gatepost"),
              avoid=("roof", "roofs", "leaking", "leak", "leaks", "glass", "glazing", "window",
                     "windows", "lock", "locks", "key", "keys", "handle", "handles", "knob",
                     "latches", "latch", "squeak", "squeaks", "squeaky", "creak", "creaks",
                     "creaking", "draught", "draughts", "draft", "paint", "painted", "paintwork",
                     "swollen", "swelling", "warped", "damp", "garage door", "car door",
                     "van door", "car", "van", "fridge", "freezer", "oven", "drawer", "drawers",
                     "cat flap", "pet flap", "letterbox", "letter box", "doorbell", "door bell",
                     "phone", "phones", "mobile", "wallet", "purse", "glasses", "keys", "keyring",
                     "dropped my", "dropped it", "dropped a", "dropped her", "dropped his",
                     "next door", "nextdoor")),
        entry("fence-panel",
              (("blew down", "blown down", "blew out", "blown out", "came off", "come off",
                "came out", "come out", "fell out", "fallen out", "fell down", "fallen down",
                "knocked down", "knocked out", "loose", "loosened", "wobbly", "wobbling",
                "broken", "broke", "snapped", "split", "damaged", "rotten", "rotted",
                "repair", "fix", "mend", "replace", "put back", "falling out",
                "keeps falling", "keeps coming", "blew over", "blown over", "fell over",
                "fallen over", "blowing down", "blowing over", "blow down", "blow over",
                "blew off", "blown off"),
               ("fence panel", "fence panels", "panels", "panel of fence", "panel of the fence",
                "fence", "fencing", "fence boards", "fence board", "feather edge", "closeboard",
                "gravel board", "gravel boards", "arris rail", "fence rail", "picket fence",
                "trellis")),
              "A blown-down panel is usually the panel, not the posts: lift it back between the posts "
              "and screw it to the rails through the post, two 65mm galvanised screws per rail, "
              "rather than just slotting it in - or fit a new panel of the same width. If boards have "
              "come off, feather-edge boards go back on with galvanised nails, each overlapping the "
              "last by about 25mm, and check the gravel board the panel sits on first, because a "
              "rotted one lets the whole panel drop. If panels keep going in wind, leave a 25mm gap "
              "under the panel so the wind passes through instead of pushing.",
              ask=("fence", "fencing", "fence panel", "fence panels", "panel", "panels",
                   "gravel board", "feather edge", "closeboard", "picket", "trellis"),
              bias=1,
              avoid=NOT_A_FENCE_JOB + ("how tall", "how high", "tall can", "high can", "maximum height",
                     "max height", "height limit", "planning", "planning permission",
                     "boundary", "who owns", "whose", "who is responsible", "who pays",
                     "who has to pay", "deeds", "title plan", "my neighbour", "my neighbor",
                     "neighbour says", "neighbor says", "neighbours fence", "neighbor's fence",
                     "neighbour's fence", "neighbours fence", "how much", "cost", "costs",
                     "price", "prices", "quote", "cheapest", "treat", "treating", "treatment",
                     "stain", "staining", "paint", "painting", "painted", "preserver",
                     "preservative", "creosote", "fence spray", "spray",
                     "stop my fence blowing", "stop the fence blowing", "stop it blowing",
                     "stop blowing down", "keeps blowing down", "keeps blowing over",
                     "blowing down again", "windproof", "wind proof", "keep the fence up",
                     "stop my fence rotting", "stop it rotting", "stop the fence rotting",
                     "prevent rot", "rotting again")),
        entry("fence-post",
              (("rotted", "rotten", "rot", "rotting", "wobbly", "wobbling", "leaning",
                "leaned", "loose", "loosened", "sinking", "sunk", "moves", "moving",
                "rocking", "broke", "broken", "snapped", "replace", "repair", "fix",
                "strengthen", "concrete"),
               ("fence post", "fence posts", "gate post", "gatepost", "fence", "fencing",
                "post", "posts")),
              "A post that has rotted or gone loose at the bottom wants replacing, not bracing: dig it "
              "out and set a new 100mm post 600mm into the ground, prop it plumb, and fill the hole "
              "with Postcrete poured dry and watered. If only the bottom has gone, cut the post off "
              "above the rot and bolt a galvanised repair spur onto the sound timber. Line the new "
              "post up with its neighbour before the concrete sets, and stand it on a gravel board or "
              "a slate so the base is not sitting in wet soil.",
              ask=("fence post", "fence posts", "gate post", "gatepost", "fence", "fencing",
                   "post", "posts"),
              bias=1,
              avoid=NOT_A_FENCE_JOB + ("post office", "post a letter", "letter", "parcel", "delivery", "mail",
                     "blog", "logged", "job", "position", "applying", "apply", "instagram",
                     "facebook", "tiktok", "photo", "photos", "comment", "review", "how tall",
                     "how high", "planning", "boundary", "who owns", "whose", "how much",
                     "cost", "costs", "price", "quote", "treat", "treating", "stain",
                     "staining", "paint", "painting", "preserver", "creosote")),
        entry("fence-treat",
              (("treat", "treating", "treatment", "stain", "staining", "paint", "painting",
                "painted", "preserver", "preservative", "creosote", "weatherproof",
                "waterproof", "protect", "protecting", "seal", "sealing", "varnish",
                "oil it", "last", "how often", "how long",
                "rot", "rotting", "rown", "gone soft", "soggy"),
               ("fence", "fencing", "fence panels", "fence panel", "feather edge", "closeboard",
                "gravel board", "trellis", "shed")),
              "Treat bare fence timber every two or three years, on a dry day with no rain forecast "
              "for 24 hours, and brush it on along the grain rather than flooding it. A water-based "
              "shed-and-fence preserver is fine for most fences and dries in a couple of hours; a "
              "solvent one soaks deeper but smells for days. Do the bottom edge of the boards and the "
              "cut ends, which is where the water gets in, and replace a rotted gravel board instead "
              "of treating it. A stain sinks in and does not peel, which is why it beats paint on a "
              "fence.",
              ask=("fence", "fencing", "fence panel", "fence panels", "trellis", "shed",
                   "feather edge", "closeboard", "gravel board"),
              bias=2,
              avoid=NOT_A_FENCE_JOB + ("how tall", "how high", "planning", "boundary", "who owns", "whose",
                     "how much", "cost", "costs", "price", "quote", "blew down", "blown down",
                     "blew out", "blown out", "came off", "fell down", "fell out", "rotted post",
                     "fence post", "gate post", "paint a room", "paint the room", "painting a room",
                     "decorating", "wall", "walls", "door", "doors",
                     "gravel board", "dropped", "dropping", "sagging", "fallen", "fell out")),
        entry("fence-height",
              (("how tall", "how high", "tall can", "high can", "tallest", "highest",
                "maximum height", "max height", "height limit", "planning permission",
                "planning", "can i build", "can i put", "can i put up", "put up a fence",
                "put a fence up", "allowed", "legal",
                "metres high", "metre high", "metres tall", "metre tall", "feet high",
                "foot high", "2 metres", "2m high", "six foot"),
               ("fence", "fencing", "fence panels", "fence panel", "wall", "garden wall")),
              "In England and Wales a fence or a garden wall can be 2 metres high without planning "
              "permission, or 1 metre where it is next to a road, footpath or driveway; conservation areas, listed "
              "buildings and some new estates have stricter rules, so ring the council's planning "
              "desk before going higher. On a boundary you also want the neighbour's agreement, "
              "because a fence over 2 metres can be complained about as a nuisance even where the "
              "height itself is allowed.",
              ask=("fence", "fencing", "fence panel", "fence panels", "wall", "garden wall"),
              avoid=NOT_A_FENCE_JOB + ("how much", "cost", "costs", "price", "quote", "blew down", "blown down",
                     "blew out", "blown out", "came off", "fell down", "repair", "fix", "replace",
                     "treat", "treating", "stain", "staining", "paint", "painting", "preserver",
                     "creosote", "rotten", "rotted", "wobbly", "loose", "boundary fence is",
                     "who owns", "whose", "who pays", "who has to pay", "deeds",
                     "how many blocks", "how many bricks", "how many slabs", "how many tiles",
                     "how many panels", "how many posts", "how many boards", "how many sheets",
                     "how many bags", "how many rolls", "how many metres of")),
        entry("fence-gravel-board",
              (("gravel board", "gravel boards", "gravelboard", "gravelboards", "gravel boarding",
                "gravelboard height", "gravel boards keep"),
               ("what", "whats", "why", "for", "need", "use", "useful", "high", "height",
                "ground", "panel", "panels", "post", "posts", "fence", "fences", "sit", "sits",
                "fit", "fitted", "rot", "replace")),
              "A gravel board is the timber along the bottom of the run, and its job is to hold the "
              "panel up out of the wet ground so the bottom rail does not rot: it sits on the soil or "
              "in a slotted concrete board, with the panel fixed above it. Set the top of a timber "
              "board about 25mm above the ground and leave the panel 50mm clear of it, so air gets "
              "between the two. A slotted concrete gravel board lets you slide a rotten board out "
              "without taking the panel down.",
              bias=1,
              avoid=NOT_A_FENCE_JOB + (
                     "how much", "cost", "costs", "price", "quote", "how many", "how long",
                     "who owns", "whose", "deeds", "planning", "how tall", "how high can",
                     "how deep", "depth", "postcrete", "how far apart", "spacing", "how thick",
                     "put up", "build", "install", "treat", "treating", "stain", "paint",
                     "painting", "blew", "blown", "fell", "fallen", "leaning", "wobbly")),
        entry("fence-build",
              (("how do i put up a fence", "how to put up a fence", "how do i put up my fence",
                "put up a fence myself", "put a fence up myself", "how do i build a fence",
                "how to build a fence", "how do i fence", "fence my garden", "fencing my garden",
                "how do i fence off",
                "where do i start with a fence", "where do i start on a fence",
                "where do i start with my fence", "where do i start on my fence",
                "where do i start with the fence", "where do i start on the fence",
                "where do i start with the fencing", "where do i start with fencing",
                "where do i begin with a fence", "where do i begin with my fence",
                "where do i begin with the fence", "where to start with a fence",
                "where to start with my fence", "where do i start with a new fence",
                "where do i start with fence panels",
                "build a fence", "build my fence", "build the fence", "building a fence",
                "put up a fence", "putting up a fence", "put a fence up", "putting a fence up",
                "erect a fence", "install a fence", "installing a fence", "new fence",
                "want a fence", "put in a fence", "putting in a fence",
                "how long does it take to put up a fence", "how long to put up a fence",
                "how long does it take to build a fence", "how long does building a fence take",
                "what do i need to put up",
                "what do i need for a fence", "can i put up a fence", "can i build a fence",
                "can i put a fence up", "how do i install a fence", "how do i erect a fence",
                "how do i put a fence up", "do it myself", "is it hard to put up a fence",
                "is it hard to build a fence", "is it easy to put up a fence",
                "hard to put up a fence"),
               ("fence", "fences", "fencing", "garden", "panel", "panels", "closeboard",
                "boundary", "posts"),
               ("how do i", "how to", "how long", "how much time", "can i", "what do i",
                "is it hard", "is it easy")),
              "Set the posts first: a string line between the two end posts keeps the run straight, "
              "then each post goes 600mm deep and 1.8m apart in concrete, braced for a day. The gravel "
              "boards go on next and the panels screw through their rails into the posts, one post's "
              "worth at a time. Two people with an auger do 20 metres in a weekend; on a boundary, "
              "check the deeds and the 2 metre rule before you dig.",
              bias=1,
              guard=_a_fence_is_named,
              avoid=NOT_A_FENCE_JOB + (
                     "how much", "cost", "costs", "price", "quote", "who owns", "whose", "deeds",
                     "planning permission", "treat", "treating", "stain", "paint", "painting",
                     "how tall", "how high", "blew", "blown", "fell", "fallen", "repair", "replace",
                     "rotten", "rotted", "wobbly", "loose", "leaning", "came off", "panel has",
                     "my neighbour", "my neighbor", "neighbour", "neighbor", "next door",
                     "fence post", "fence posts", "gate post", "post hole", "posts go",
                     "metres high", "metre high", "metres tall", "metre tall", "feet high",
                     "foot high", "planning permission", "permission", "allowed", "legal",
                     "how deep", "depth", "how far apart", "spacing", "how thick", "what size",
                     "postcrete", "concrete a post", "concrete it in", "bags of")),
        entry("fence-owner",
              (("who owns", "whose", "who is responsible", "who pays", "who has to pay",
                "who should pay", "my neighbour", "my neighbor", "neighbour says", "neighbor says",
                "neighbours fence", "neighbor's fence", "neighbour's fence", "neighbours fence",
                "next door say", "boundary", "deeds", "title plan", "t mark", "shared fence",
                "pay half", "half the cost", "have to pay", "split the cost", "go halves",
                "shared boundary",
                "took the fence down", "removed the fence", "replaced the fence", "put up a fence"),
               ("fence", "fencing", "fence panels", "fence panel", "boundary fence", "wall")),
              "Who owns a boundary fence is in the deeds, not in who mows the grass: the title plan "
              "marks the owner's side with a T, and where there is no mark it is usually shared, each "
              "side looking after the fence on their own side. Almost no property has to have a fence "
              "at all, so a neighbour taking down one that is theirs is usually within their rights. "
              "If it is theirs you cannot paint it, fix your side of it or hang anything on it without "
              "asking, and if it is shared the fair split is half the cost each.",
              ask=("fence", "fencing", "fence panel", "fence panels", "boundary fence", "hedge",
                   "wall"),
              bias=1,
              avoid=NOT_A_FENCE_JOB + ("how much", "cost", "costs", "price", "quote", "blew down", "blown down",
                     "blew out", "blown out", "came off", "fell down", "repair", "fix it",
                     "replace", "treat", "treating", "stain", "staining", "paint it", "painting",
                     "preserver", "creosote", "rotten", "rotted", "wobbly", "loose",
                     "how tall", "how high", "tall can", "high can", "planning",
                     "metres high", "metre high", "metres tall", "metre tall", "feet high",
                     "foot high", "ft high", "m high", "2m", "6ft", "planning permission",
                     "can i put up a fence", "can i build a fence", "am i allowed",
                     "how do i put up", "how to put up", "how do i build", "how to build",
                     "how do i fence", "fence my garden", "where do i start",
                     "how long does it take", "how long to put up", "what do i need to put up",
                          "put up a fence myself", "put a fence up myself", "erect a fence",
                     "install a fence", "do it myself", "how do i begin", "where do i begin",
                     "blocking my light", "blocks my light", "blocking the light", "blocks the light",
                     "my light", "too tall", "too high", "overhanging", "overhangs", "branches")),
        entry("neighbour-hedge-light",
              (("too tall", "too high", "blocking my light", "blocks my light", "blocking the "
                "light", "blocks the light", "blocking light", "blocks light", "block my light",
                "no light", "my light", "overhanging", "overhangs", "hanging over", "hangs over",
                "branches over", "branch over", "trees over",
                "cut back over my", "cut over my", "cut my branches", "cut back my branches",
                "cut branches", "cut a branch", "cut back branches", "cut the branches",
                "cut back the branches", "trim branches", "trim the branches", "branches off",
                "high hedge", "hedges", "complaining about", "complain about",
                "hedge too tall", "hedge too high"),
               ("hedge", "hedges", "tree", "trees", "branches", "branch", "fence", "fencing",
                "wall", "neighbour", "neighbours", "neighbour's", "neighbors", "next door",
                "next-door")),
              "A hedge or a wall that shuts out the light is the council's job, not a court's: if it "
              "is an evergreen hedge over 2 metres and it blocks your light, you can complain to the "
              "council under the high-hedges rules, but only after you have written to the neighbour "
              "and kept a copy, and there is a fee of a few hundred pounds. Branches that overhang "
              "your side you can cut back to the boundary without asking, though you must offer the "
              "cuttings back and you cannot lean into their garden to do it, and you must not cut a "
              "tree under a tree preservation order or in a conservation area without checking with "
              "the council first. Right to light through an old window is a separate legal claim and "
              "a solicitor's job.",
              ask=("hedge", "hedges", "tree", "trees", "branches", "branch", "fence", "fencing",
                   "wall"),
              avoid=NOT_A_FENCE_JOB + ("how much", "cost", "costs", "price", "quote", "blew down", "blown down",
                     "blew out", "blown out", "repair", "fix", "replace", "treat", "treating",
                     "stain", "staining", "paint", "painting", "creosote", "rotten", "rotted",
                     "wobbly", "loose", "how tall can", "how high can", "planning permission for",
                     "who owns", "whose", "deeds", "fell down", "died", "dead", "dying", "diseased",
                     "looks dead", "brown", "not growing", "bare patch",
                     "patchy", "yellow", "yellowing", "yellowed", "gone brown", "brown at the base",
                     "brown at the bottom", "bare at the bottom", "bare at the base", "thin",
                     "sparse", "gaps", "gap", "looking sorry", "sorry for itself", "looks ill",
                     "looks bad", "looks sad", "bald", "shrubs", "shrub", "feed", "feeding",
                     "fertiliser", "fertilizer", "compost", "mulch", "watering", "water it",
                     "poison", "fruit", "apple", "pear", "plum", "cherry tree", "prune",
                     "pruning", "plant a tree", "plant a hedge", "how do i trim")),
        entry("locked-in-a-room", (("locked in", "locked inside", "shut in", "stuck inside"),
                                   ("flat", "house", "home", "room", "bedroom", "bathroom",
                                    "toilet", "garage", "shed", "cellar", "loft", "hallway")),
              "If a child is shut in, ring 999 straight away and stay on the line. Otherwise get a "
              "window open and shout to a neighbour, or ring someone who has a spare key - "
              "someone is nearly always in. If nobody is, the landlord or letting agent first, then "
              "a locksmith who quotes on the phone; a stuck lock is worth one firm push with the "
              "handle held up before you pay anyone. If there is fire, smoke or someone unwell, "
              "ring 999 and say you are locked in.",
              bias=1),
        entry("draughts", (("draught", "drafts", "draughts", "cold air", "under the door",
                            "under the front door", "gap under"),
                           ("door", "window", "cold", "stop", "keep", "front")),
              "Stick a brush strip or foam seal round the doors and windows, and put a weighted "
              "draught excluder at the bottom of the front door. A chimney balloon and a letterbox "
              "flap are cheap and stop the worst of it; seal up the gaps before spending money on "
              "heating."),

        entry("door-banging", (("door", "doors", "gate"),
                               ("banging", "bangs", "bang", "slamming", "slams", "slam", "rattling",
                                "rattles", "rattle", "wind", "windy", "shutting", "swinging")),
              "A door that bangs is a latch that isn't holding or a gap that lets the wind push it: "
              "check the strike plate first — a card's thickness of movement is enough, and moving it "
              "2mm further in with a chisel or a file fixes most of them. If it still swings, a hook "
              "and eye or a magnetic catch holds it open or shut, and a foam strip on the stop takes "
              "the noise out.",
              avoid=("frozen", "freezing", "froze", "iced", "ice", "frost", "car door", "car doors",
                     "stuck shut",
                     "paint", "painting", "sticking", "creaking", "hinge", "hinges", "lock", "key",
                     "keys", "handle", "front door lock", "burglar", "shed", "garage door",
                     "cupboard", "cupboards", "cabinet", "cabinets", "wardrobe", "wardrobes",
                     "kitchen", "kitchen door", "drawer", "drawers",
                     ) + APPLIANCE_DOOR_WORDS + (

                     "nail", "nails", "fingernail", "fingernails", "toenail", "toenails", "finger",
                     "fingers", "thumb", "toe", "toes", "hand", "jammed",
                     "slammed the door", "slams the door", "door on me", "door in my face")),


        entry("moving-pack", (("move house", "moving house", "moving home", "move home",
                               "moving flat", "move flat", "moving out", "move out",
                               "moving in", "move in", "for moving", "before moving",
                               "moving office", "move office", "moving offices", "move offices",
                               "office move", "moving the office", "moving shop", "moving studio",
                               "to move", "to be moved", "to move house",
                               "pack", "packing", "packed", "unpack", "unpacking"),
                              ("too much", "so much", "lots", "loads", "plenty", "things",
                               "boxes", "clutter")),
              "Pack what you use least first - books, spare bedding, the cupboard under the stairs - "
              "and keep a 'first night' box out of the van: kettle, mugs, chargers, loo roll, bedding "
              "and a change of clothes. Label boxes by room, do one room an evening for the last "
              "three weeks, and get rid of anything you have not touched in a year rather than "
              "paying to move it.",
              avoid=BODY_WORDS),

        entry("moving-cheap", (("move", "moving", "moved", "removals", "man with a van"),
                               ("cheap", "cheaper", "cheapest", "cheaply", "cost", "costly",
                                "price", "prices", "pricey", "expensive", "budget", "hire", "van",
                                "money", "save", "afford")),
              ("For one sofa and a bed, hire a man with a van for a couple of hours or borrow a van and "
               "two friends; book the van for the whole morning rather than by the hour. Measure the "
               "doorways and the stairwell first, because a sofa that doesn't fit costs you the day."),
              avoid=("stressed", "stress", "worried", "nervous", "anxious", "sad", "upset", "feeling",
                     "kids", "children", "child", "tell", "doctor", "gp", "dentist", "council",
                     "council tax", "school", "care home", "piano", "landlord", "deposit", "tenancy",
                     "register")),
        entry("moving-admin",
              (("move", "moving", "moved", "moving house", "moving flat", "new address", "new house",
                "new flat", "move house", "move out"),
               ("council", "council tax", "doctor", "gp", "dentist", "school", "register", "utilities",
                "redirect", "meter", "tenancy", "admin", "paperwork", "notify", "need to do",
                "tell", "what do i need", "checklist")),
              ("Do the paper trail in one afternoon: tell the council tax office for the old and the "
               "new address, register with a GP near the new place and ask for your notes to move with "
               "you, and read the meters on the day you leave and arrive. Set up a Royal Mail redirect "
               "for three months, because it catches the accounts you forget, and take photos of the "
               "meters as proof."),
              avoid=("buy", "first night", "sofa", "van", "cheap", "cost", "price", "hire", "removal",
                     "phone", "laptop",
                     "tell my landlord", "tell the landlord", "my landlord", "the landlord",
                     "landlord", "landlady", "letting agent", "notice period", "give notice",
                     "who do i tell about my new address", "who do i tell about my address",
                     "who do i tell about my new adress", "who do i tell about my new place",
                     "change the name", "name on", "in my name", "not on the bill",
                     "computer", "city", "job", "office", "desk", "company", "files", "apps",
                     "contacts", "care home", "piano", "abroad", "country", "kids", "kid",
                     "children", "child", "son", "daughter", "explain", "upset",
                     "appointment", "appointments", "rescheduled", "postponed",
                     "brought forward", "cancelled", "canceled", "moved to", "moved it",
                     "shift", "shifts", "rota", "boss", "manager", "overtime")),
        entry("moving-packing-plan",
              (("move house", "moving house", "moving flat", "move flat", "house move", "moving home",
                "move home", "moving out", "moving in", "removals", "before moving", "when moving",
                "after moving", "moving office", "move office", "moving offices", "move offices",
                "office move", "moving the office", "moving shop", "moving studio",
                "for a move", "a house move", "the move", "for the move"),
               ("packing", "pack", "packed", "boxes", "box", "declutter", "unpack")),
              bias=1,
              reply=("Start with one room and one deadline: pack the things you use least first, label every "
               "box by room and keep one box for the first night - bedding, toilet roll, kettle, mugs, "
               "chargers, a torch and any medication. Anything you have not used in a year, sell, "
               "donate or bin it now rather than paying to move it; a bag a day from the back of a "
               "cupboard gets rid of most of it. Book the van for the whole morning rather than by the "
               "hour, and measure the doorways and stairwell before the day. As a guide, a one-bed "
               "flat is about twenty boxes and a couple of weekends of packing; a three-bed house is "
               "two or three times that."),
              avoid=("council", "council tax", "doctor", "gp", "dentist", "register", "tenancy",
                     "deposit", "landlord", "kids", "children", "child", "son", "daughter",
                     "piano", "abroad", "country", "city", "job", "phone", "laptop", "computer",
                     "contacts", "apps", "care home", "pet", "cat", "dog", "trip", "holiday",
                     "flight", "hotel", "camping", "suitcase", "weekend away",
                     "start", "started", "starting", "plan", "planning", "organise", "organize",
                     "organised", "sorted", "checklist", "advice", "break up", "breakup",
                     "girlfriend", "boyfriend", "ex", "stressed", "stress", "worried", "nervous",
                     "anxious", "sad", "upset", "feeling", "overwhelmed", "exhausted", "dreading",
                     "manager", "boss", "meeting",
                     "glasses", "plates", "mugs", "crockery", "glassware", "china", "bowls")
              + BODY_WORDS),
        entry("packing-time",
              (("pack", "packing", "packed", "boxes"),
               ("flat", "house", "home", "1 bed", "one bed", "2 bed", "two bed",
                "how long", "how many boxes", "bedsit", "moving day")),
              ("Pack what you use least first and give it a date: a one-bed flat is about twenty boxes "
               "and two weekends if you do it evenings and one weekend if you take a day off; a "
               "three-bed house is two or three times that. Every box labelled by the room it goes to, "
               "one first-night box kept out of the van, and anything you have not used in a year "
               "goes to the charity shop rather than into a box."),
              ask=("how long", "how many", "tips", "advice", "how much", "best way", "how do i",
                   "where do i", "what do i need", "should i"),
              avoid=("suitcase", "holiday", "trip", "flight", "airport", "camping", "abroad",
                     "weekend away", "hand luggage", "carry on", "school bag", "nappy bag",
                     "council", "council tax", "doctor", "gp", "dentist", "register", "tenancy",
                     "deposit", "landlord", "kids", "children", "child", "piano", "van", "cost",
                     "price", "cheap", "removal", "stressed", "stress", "worried", "nervous",
                     "anxious", "sad", "upset", "feeling", "overwhelmed", "dreading",
                     "flat pack", "flat-pack", "furniture", "assemble", "assembling",
                     "wardrobe", "sofa", "mattress", "bookcase", "bed frame", "dining table",
                     "glasses", "plates", "mugs", "crockery", "glassware", "china", "bowls",
                     "wine glasses", "tumblers", "ornaments", "vases")
              + BODY_WORDS),
        entry("packing-breakables",
              (("pack", "packing", "packed", "wrap", "wrapping", "box up", "boxes", "box"),
               ("plates", "glasses", "crockery", "mugs", "dishes", "bowls", "china", "fragile",
                "wine glasses", "ornaments", "vases", "picture frames", "mirrors", "tumblers")),
              ("Wrap each plate in paper or a tea towel and stand it on its edge in the box, like "
               "records in a crate, never stacked flat: that is what stops them cracking. A crumpled "
               "paper or towel cushion in the bottom and on top, small boxes that one person can lift, "
               "and FRAGILE written on the sides. Glasses and mugs go upright with paper pushed inside, "
               "a mug handle never takes the weight, and wine glasses travel best one inside a sock. A mirror "
               "or a framed picture travels standing on its edge too, with card on the corners and "
               "tape across the glass in an X so a crack stays put."),
              ask=("how", "what", "tips", "advice", "best way", "should i", "so they dont break",
                   "so they don't break", "wont break", "won't break", "without breaking",
                   "not break", "safely"),
              avoid=("spectacles", "contact lenses", "contact lens", "lenses", "prescription",
                     "glasses prescription", "eyes", "sight",
                     "weekend", "weekend away", "trip", "holiday", "holidays", "abroad", "flight",
                     "hotel", "suitcase", "carry on", "hand luggage", "days")),
        entry("packing-a-kitchen",
              (("kitchen", "kitchens", "kitchen stuff", "kitchen things", "kitchen cupboards",
                "kitchen drawers", "cupboards in the kitchen"),
               ("pack", "packs", "packing", "packed", "box", "boxes", "box up", "pack up",
                "packing up",
                "stuff", "the rest")),
              ("Leave the kitchen to the second-to-last day, because it is the room you still "
               "need, and keep one box open until the morning: kettle, two mugs, tea, a tea towel, "
               "washing-up liquid, a sharp knife, a tin opener and a corkscrew. Do it one cupboard "
               "at a time and set a box down on the counter as you empty it, so nothing gets "
               "carried across the room; plates and glasses go on edge in small boxes with a towel "
               "round them, never stacked flat. Anything out of date or never used goes in the bin "
               "bag rather than the van, the fridge wants emptied, defrosted and dried out a day "
               "before, and it travels upright. Write KITCHEN - OPEN FIRST on the boxes you will "
               "want that night, and put the food and the cleaning stuff in their own two boxes so "
               "you are not hunting for the bin bags."),
              guard=_the_kitchen_stuff_is_a_take_up,
              avoid=("unpack", "unpacking", "unpacked",
                     "clean", "cleaning", "cleaned", "grease", "greasy", "smell", "smells",
                     "oven", "fridge", "freezer", "hob", "cooker", "microwave", "bin", "dishwasher",
                     "leak", "tap", "taps", "mould", "limescale", "floor", "floors", "wall", "walls",
                     "paint", "painting", "decorate", "plan", "planning", "design", "layout",
                     "fit", "fitted", "fitting", "install", "installing", "renovate", "refurb",
                     "quote", "quotes", "builder", "extension", "buy", "buying", "shop", "shopping",
                     "cheap", "cheapest", "price", "prices", "cost", "where can i get",
                     "plates", "glasses", "crockery", "china", "bowls", "mugs", "wine glasses")),
        entry("moving-with-kids",
              (("move", "moving", "moved", "moving house", "house move", "new house", "new home"),
               ("kids", "kid", "children", "child", "son", "daughter", "teenager", "toddler",
                "baby", "babies",
                "tell", "explain", "upset", "worried", "nervous", "sad", "cope", "settle")),
              ("Tell them as soon as it is certain, and keep it concrete: which room is theirs, where "
               "the school or nursery is, and what stays the same. Let them pack a box of their own "
               "things and choose the paint or the posters, because control is what they are missing. "
               "Say goodbye to the old place properly on the last day, and expect a wobble a few weeks "
               "in, when the novelty wears off and they miss their friends."),
              guard=_a_child_or_a_telling,
              avoid=("council", "council tax", "gp", "doctor", "dentist", "register", "piano",
                     "van", "cheap", "cost", "price", "abroad", "country", "care home",
                     "move out", "left home", "has left", "wants to move",
                     "a home", "the home", "nursing home", "residential home", "home too")),
        entry("piano-move",
              (("piano",), ("move", "moving", "moved", "cost", "hire", "removers", "stairs",
                            "upstairs", "quote")),
              ("Hire a piano remover rather than a general removal firm: it takes two people who know "
               "the handholds, a proper trolley and straps, and a knocked soundboard is a repair bill. "
               "Keep it upright and never on its side, take the legs off an upright only if the maker's "
               "instructions say so, and let it settle in the new room for a few weeks before it is "
               "tuned. Stairs and narrow turns are what make a quote go up, so send a photo of the "
               "route when you ask for one."),
              avoid=("learn", "lessons", "practise", "practice", "tune", "buy", "worth", "grade")),
        entry("first-night", (("first night", "moving in", "moving into", "new flat", "first flat"),
                              ("need", "do", "before", "buy", "keep out", "keep aside",
                               "keep back", "put aside", "put by", "pack last", "open first",
                               "have ready", "ready", "get ready")),
              FIRST_NIGHT_BOX,
              avoid=("stressed", "stress", "worried", "nervous", "anxious", "sad", "upset", "feeling",
                     "sofa", "couch", "settee", "bed", "mattress", "wardrobe", "table", "chairs",
                     "fridge", "freezer", "piano", "van", "removals", "removal", "hire", "hiring",
                     "stairs", "upstairs", "doorways", "doors", "carry", "carrying", "lifting",
                     "move my", "moving my", "shift my")),
        entry("just-moved-in",
              (("just moved", "moved in", "moved into"),
               ("new flat", "new house", "new home", "new place", "first flat", "our own place",
                "moved in", "moved into", "last week", "last weekend", "last month", "this week",
                "this month")),
              FIRST_NIGHT_BOX,
              bias=1,
              avoid=("guilty", "care home", "nursing home", "a home", "the home", "home too",
                     "residential home", "stressed", "stress", "worried",
                     "nervous", "anxious", "sad", "upset", "feeling", "kids", "children", "child",
                     "council", "council tax", "doctor", "gp", "dentist", "school", "landlord",
                     "deposit", "tenancy", "address", "register", "job", "city", "country", "abroad",
                     "damp", "mould", "mold", "leak", "piano", "boiler", "heating", "hot water",
                     "radiator", "broken", "repair", "washing machine", "fridge", "noise", "noisy",
                     "neighbour", "neighbours", "cold",
                     "tomorrow", "next week", "next month", "on saturday", "on sunday",
                     "with my", "boyfriend", "girlfriend", "partner", "husband", "wife", "parents",
                     "flatmate", "housemate", "together"),
              guard=lambda understood: not the_stomach_is_what_it_is_about(understood)),
        entry("keep-room-cool",
              (("house", "home", "flat", "room", "bedroom", "living room", "kitchen", "windows",
                "heatwave", "heat wave", "heat", "summer", "sun", "indoors", "inside", "upstairs",
                "downstairs",
                "office", "in here", "in this room", "this room", "this place", "my place",
                "our place"),
               ("cool", "cooler", "cooling", "cool down", "keep cool", "hot", "boiling", "stuffy",
                "stifling", "roasting", "shade", "sun", "keep the sun out", "windows",
                "baking", "baking hot", "an oven",
                "sauna", "like a sauna", "like an oven", "like a greenhouse", "like a furnace",
                "sweltering", "melting", "boiling hot", "hot as an oven", "stifling hot",
                "a furnace", "furnace",
                "keep the heat out", "heat out", "stop the sun", "sun heating", "block the sun",
                "the sun coming in", "sun comes in", "sun through")),
              ("Shut the windows and pull the curtains on the sunny side in the morning, then open "
               "everything wide once it is cooler outside than in, usually after 9pm. A fan in an open "
               "window pulling air through the flat beats one blowing at you. Keep the oven off and "
               "cook early, and put a bowl of water out if the air is dry."),
              avoid=THE_APPLIANCE_ITSELF + ("hob", "boiler", "radiator", "heating on",
                     "radiators", "washing machine", "tumble dryer", "laptop", "computer", "pc",
                     "phone", "tablet", "car", "engine", "dog", "cat", "puppy", "kitten", "baby",
                     "babies", "toddler", "pregnant", "fan cheaper", "cheaper", "cost",
                     "electricity", "bill", "keep warm", "keep the house warm", "draught",
                     "draughts", "drink", "beer", "wine", "food", "milk", "leftovers",
                     "hot water", "no water", "cold water", "shower", "bath", "immersion",
                     "heating on", "thermostat",
                     "no window", "no windows", "without a window", "windowless",
                     "bigger", "bigger window", "enlarge", "enlarging", "widen", "widening",
                     "larger", "new window", "window fitter", "glazier")),
        entry("room-no-window",
              (("room", "bedroom", "living room", "kitchen", "hallway", "office", "study", "flat",
                "cellar", "basement"),
               ("no window", "no windows", "without a window", "without windows", "windowless",
                "no natural light", "no light", "get light", "air", "ventilation", "ventilate",
                "airflow", "stuffy", "damp")),
              ("Light it in layers and move the air with a fan. One bright lamp in each corner beats a "
               "single ceiling light, an LED around 4000K reads closest to daylight, and a mirror or "
               "pale wall opposite the door bounces it about. For the air, prop the door open with a "
               "fan pulling air through to another room, or run a small dehumidifier: a windowless "
               "room goes damp before it goes stuffy."),
              avoid=("mould", "mold", "mildew", "condensation", "cool", "cooler", "hot", "heatwave",
                     "heat", "radiator", "boiler", "heating", "paint", "curtain",
                     "curtains", "blind", "blinds", "bigger", "enlarge", "widen", "door", "lock",
                     "smell", "smells", "smelling", "smelly", "musty", "whiff", "reek", "stinks")),
        entry("window-bigger",
              (("window", "windows", "window opening"),
               ("bigger", "enlarge", "enlarging", "enlarged", "widen", "widening", "larger",
                "more light", "knock through", "new window", "replace the window",
                "replacement window", "big window")),
              ("Widening a window opening is a builder's job, not a window fitter's: taking out "
               "brickwork under a new lintel is structural, where a swap of the same size is a fitter's "
               "morning. Ask a builder to price it, and a structural engineer if the wall carries the "
               "floor above; in a flat or a conservation area you may need permission too. Cheaper "
               "first: a mirror opposite the window and paler walls."),
              avoid=("curtain", "curtains", "blind", "blinds", "draught", "drafts", "draft",
                     "measure", "measuring", "clean", "cleaner", "cleaning", "wash", "replace the "
                     "glass", "cracked", "broken", "stuck", "leaking", "condensation", "no window")),
        entry("window-wont-open",
              (("window", "windows", "sash window", "sash", "casement", "frame", "upvc"),
               ("wont open", "won't open", "will not open", "cant open", "can't open", "cannot open",
                "painted shut", "painted over", "stuck", "stuck shut", "jammed", "seized",
                "swollen", "swelled", "warped", "budge", "wont move", "won't move", "wont shut",
                "won't shut", "wont close", "won't close", "sticking", "sticks", "doesnt close",
                "doesn't close", "hard to open", "hard to close", "hard to shut", "easier to open",
                "rubs", "dragging", "stiff")),
              ("Run a knife round the join first, because paint gluing the frame to the sill is the "
               "usual cause: score the line all the way round, then press on the frame and lift the "
               "handle. If it is a sash, check the cords - a snapped cord drops the weights and the "
               "window wedges. A tap with the heel of your hand and a dry bar of soap on the runners "
               "frees most of the rest."),
              avoid=("door", "doors", "windscreen", "car", "clean", "cleaning", "cleaner", "wash",
                     "condensation", "draught", "draft", "drafts", "leaking", "leak", "cost", "price",
                     "replace", "double glazing", "curtain", "curtains", "blind", "blinds", "bigger",
                     "widen", "enlarge", "no window", "no windows", "storage",
                     "paint a window", "painting a window", "paint my window", "paint the window",
                     "paint window", "painting the windows", "paint the windows", "repaint",
                     "painting a window frame", "paint a window frame", "brushes", "brush"),
              bias=2),
        entry("sleep-hot-night",
              (("sleep", "sleeping", "slept", "bed", "bedroom", "night"),
               ("hot", "heat", "heatwave", "heat wave", "warm", "sweating", "sticky", "sweaty",
                "cool", "cooler", "cooling", "cool down", "too hot")),
              ("Cool the room before you get in, not after: windows open and a fan on for half an hour, "
               "then a lukewarm shower and dry off properly. Cotton sheets, one light layer rather "
               "than a duvet, and a damp flannel on your neck or feet. Sweating is how your body dumps "
               "heat, so give it moving air instead of covering up."),
              avoid=("baby", "babies", "toddler", "child", "children", "dog", "cat", "puppy",
                     "kitten", "pregnant", "fridge", "freezer", "boiler", "radiator", "heating on",
                     "laptop", "phone", "computer", "car", "mattress", "buy", "best", "which",
                     "wake up", "waking", "woke", "nap", "nightmare", "dream", "snore",
                     "snoring", "teeth", "grind"),
              ask=("how", "what", "tips", "tip", "advice", "should", "can i", "can you", "help",
                   "too hot", "cant", "can't", "cannot", "struggling", "keep", "cool down")),
        entry("lumpy-pillow",
              (("pillow", "pillows", "pillowcase", "pillow case", "filling"),
               ("lumpy", "lumps", "bunched", "bunched up", "flat", "too flat", "saggy", "sags",
                "gone flat", "worn out", "old", "replace", "uncomfortable")),
              "A lumpy pillow has usually just bunched its filling: unzip it, pull the filling apart "
              "with your hands, shake it down to the corners and bash it flat. If it still lumps, or "
              "it folds in half and stays folded when you lay it on your arm, the filling has gone "
              "and a new one is the fix - hollowfibre costs about £10 to £25 and a pillow over two "
              "years old is usually past it. A duvet that has gone lumpy is the same job, and a wash "
              "on a hot cycle with two tennis balls in the tumble dryer evens the filling out again.",
              bias=2,
              avoid=("mattress", "mattresses", "topper", "bed frame", "sprung", "squeak", "hot",
                     "wash", "washing", "dryer", "smell", "smelly",
                     "sweat", "sweaty", "insomnia", "wake up", "waking up", "cant sleep",
                     "hotel", "baby", "babies", "toddler", "cot", "pram", "buy", "which",
                     "should i get", "look for", "best")),
        entry("bed-uncomfortable",
              (("bed", "beds", "mattress", "mattresses", "bedding"),
               ("uncomfortable", "too soft", "too hard", "too firm", "sagging", "sags",
                "sag", "dip", "dipped", "hurts", "hurt", "sore back", "stiff back", "wake up sore",
                "waking up sore", "bad back", "not comfortable", "kill my back", "kills my back",
                "topper", "springs")),
              ("Try a mattress topper before a new mattress. A 5cm memory-foam or latex one costs about "
               "£40 to £100 and softens a firm bed or fills the dip in a soft one. If the mattress is "
               "over eight years old, sagging in the middle or you can feel the springs, it is the "
               "mattress and a topper only postpones it. A slipped pillow under your knees takes the "
               "strain off a sore lower back, and a too-soft bed is worth trying with a board under it "
               "first."),
              avoid=("should i buy", "should i get", "to buy", "buy a new mattress", "buy a mattress",
                     "buy a new bed", "new mattress", "new bed", "cost", "price", "how much", "cheap", "cheaper",
                     "budget", "which", "choose", "choosing", "best", "shop", "deal", "sale",
                     "look for", "looking for", "recommend", "recommendation", "worth it", "review",
                     "back pain", "my back hurts", "killing my back", "bad back pain",
                     "clean", "cleaning", "stain", "stains", "wash", "washing", "bedbugs", "bed bugs",
                     "hot", "heat", "sweating", "sweaty", "wet", "wee", "accident", "hotel",
                     "breakfast", "holiday", "baby", "babies", "toddler", "child", "my son",
                     "my daughter", "my dog", "the dog", "my cat", "the cat", "sick", "vomit",
                     "hospital", "care home")),
        entry("fan-vs-aircon",
              (("fan", "aircon", "air con", "air conditioning", "air conditioner"),
               ("cheaper", "cheap", "cost", "run", "running", "expensive", "electricity", "worth")),
              "A fan costs a penny or two an hour; a portable air conditioner is more like 30 to 50p, "
              "and a fitted one more again. A fan only cools you, not the room, so put it in front of "
              "an open window at night with another window open across the room. A bowl of ice in front "
              "of a fan helps in dry heat, not in humidity.",
              avoid=("laptop", "computer", "pc", "console", "playstation", "xbox", "car", "engine",
                     "oven", "extractor", "boiler", "server"),
              ask=("cheaper", "cheap", "cost", "expensive", "electricity", "air con", "aircon",
                   "air conditioning", "hot", "cool", "cooling", "heatwave", "summer", "worth")),
        entry("appliance-life", (LIFE_NAMES, LIFE_ASK),
              _lifespan, ask=LIFE_ASK,
              avoid=LIFE_GUARD + JOB_GUARD + ("broken", "quote", "worth it", "worth buying",
                                              "worth the money", "worth paying", "cool", "cooling",
                                              "cool it", "cool the pan", "before washing",
                                              "washing it", "wash the pan", "before i wash"), bias=4),
        entry("bedding-finished", (("mattress", "mattresses"),
                                   ("replace", "replacing", "replacement", "replaced",
                                    "when to replace", "time to replace", "new one",
                                    "need a new", "need a new one")),
              _lifespan, bias=2,
              avoid=("buy", "buying", "bought", "cost", "costs", "price", "prices", "cheap",
                     "cheaper", "budget", "spend", "shop", "shops", "store", "topper",
                     "protector", "clean", "cleaning", "wash", "washing", "stain", "stains",
                     "smell", "smells", "turn", "turning", "flip", "flipping", "rotate",
                     "rotating", "cover", "covers", "sheet", "sheets", "pillow", "pillows",
                     "duvet", "duvets",
                     "choose", "choosing", "chose", "pick", "picking", "which one",
                     "what should i look for", "how do i choose", "help me choose"),
              ask=("replace", "replacing", "replacement", "replaced", "when to", "new")),
        entry("running-cost", (RUNNING_WORDS, COST_WORDS), _running,
              avoid=("broken", "break", "repair", "install", "frost", "iced", "ice", "defrost",
                     "fix", "fixing", "fixed", "mend", "mending", "engineer", "call out", "spare",
                     "won't", "wont", "doesn't", "doesnt", "does not", "stopped", "spin", "hair",
                     "smell", "smells", "leak", "noise", "noisy", "not working", "cold", "filter",
                     "clean", "car", "engine", "laptop", "phone", "tablet", "pc", "console",
                     "playstation", "xbox", "extractor", "buy", "buying", "getting",
                     "service", "servicing", "serviced", "repair",
                     "replace", "replaces", "replacing", "replaced", "replacement",
                     "swap", "swaps", "swap out", "swapping", "swapped", "rip out",
                     "ripping out", "fit a", "fitting a", "fitted a",
                     "get one", "worth getting", "cups", "water for", "fill", "best", "new",
                     "good", "a good", "good cheap", "good and cheap", "recommend", "recommended",
                     "worth", "worth it", "which one", "which one to", "should i buy",
                     "should i get", "what to buy", "to buy",
                     "air con", "aircon", "air conditioning", "air conditioner",
                     "what time", "cheapest time", "time of day", "off peak", "off-peak",
                     "in the morning", "in the evening", "during the day",
                     "leave on", "leaving on", "left on", "all day", "all the time", "overnight",
                     "leave the heating on", "leaving the heating on", "left the heating on",
                     "keep the heating on", "keeping the heating on", "heating on all day",
                     "heating on all the time", "heating on low", "heating on at night",
                     "timer", "timed", "thermostat", "flow temperature",
                     "hotel", "hotels", "bath bomb", "bath bombs", "bath mat", "bath mats",
                     "bath towel", "bath towels", "bird bath", "swim", "swimming", "baby", "babies",
                     "dog", "dogs", "cat", "cats"),
              ask=COST_WORDS, bias=2),
        entry("freezer-defrost",
              (("freezer", "freezer drawer", "icebox", "fridge", "fridges", "refrigerator"),
               ("defrost", "defrosting", "ice", "icing", "iced", "frost", "frosting", "froze",
                "frozen", "icy", "thick", "needs")),
              "Defrost it when the ice is more than about 5mm thick: switch it off at the wall, move "
              "the food into a cool box, and leave bowls of hot water inside with the door shut. Budget "
              "two to three hours, or overnight leave it with the door open and towels down. Never "
              "chip at the ice with a knife, because a pierced pipe writes the freezer off. The "
              "reason is moist air getting in every time the door opens.",
              avoid=("rice", "pasta", "bread", "milk", "meat", "chicken", "eggs", "butter",
                     "cheese"),
              bias=2),

        entry("fridge-frost",
              (("fridge", "fridge freezer", "ice box", "freezer box", "freezer compartment"),
               ("frost", "frosts", "frosting", "frosted", "icing", "icing up", "ices up", "iced up",
                "ice", "icy", "ice building up", "build up of ice", "frozen up", "freezing up",
                "thick ice", "snow", "back wall", "back of the fridge", "icicles")),
              "Ice in a fridge that is meant to look after itself comes from one of three things: a "
              "door seal that no longer grips (shut a strip of paper in the door and pull - it should "
              "drag), the drain hole at the back of the fridge blocked so the water freezes there, or "
              "food pushed against the back wall. Fix the seal and clear the drain and the ice stops "
              "coming back. Get rid of what is there by defrosting it properly with the door open "
              "overnight, and never chip at it with a knife.",
              avoid=("defrost", "defrosting", "not cold", "warm", "noise", "noisy", "smell", "smells",
                     "clean", "cleaning", "repair", "replace", "buy", "cost", "broken", "dead",
                     "leaking", "drain hole", "water", "freezer", "chest freezer", "freezer drawer",
                     "temperature", "setting", "worth"),
              bias=2),


        entry("frost-free-freezer",
              (("frost free", "frost-free", "frostfree", "no frost", "auto defrost", "auto-defrost",
                "self defrosting", "never needs defrosting"),
               ("freezer", "freezers", "icebox", "fridge freezer", "frost", "frosts", "frosting",
                "frosting up", "frosts up", "ice", "ices", "icing", "iced", "one", "it", "that",
                "needs", "defrost", "defrosting")),
              "A frost-free freezer never needs defrosting by hand: it clears its own frost, so ice "
              "building up means the door seal has gone or the vent behind it is blocked. Check the "
              "gasket all round the door with a sheet of paper (it should grip), and a new seal is a "
              "cheap fix.",
              avoid=("buy", "buying", "worth", "cheaper", "cheapest", "best", "which", "recommend"),
              bias=1),
        entry("how-often-to-defrost",
              (("defrost a freezer", "defrosting a freezer", "best way to defrost", "way to defrost",
                "should i defrost it", "shall i defrost it", "do i defrost it", "needs defrosting",
                "needs a defrost", "needs defrosting out", "how often should i defrost",
                "how often do i defrost", "how often to defrost", "when should i defrost",
                "defrost the freezer", "defrost my freezer", "defrost it now"),
               ("freezer", "freezers", "icebox", "fridge freezer", "ice", "icing", "frosting",
                "how often", "often", "how many times", "once a year", "twice a year", "yearly",
                "frequency", "every few months")),
              "At about 5mm of ice, switch it off at the wall and move the food into a cool box: "
              "budget two to three hours, or overnight with bowls of hot water inside and the door "
              "shut."
              " Most freezers need this once or twice a year. Never chip at the ice, because a "
              "knife can pierce a pipe and write the freezer off, and a frost-free one never needs "
              "it at all, so ice in one means the door seal has gone.",
              avoid=("chicken", "meat", "mince", "turkey", "fish", "prawns", "sausages", "beef",
                     "pork", "lamb", "bread", "pastry", "cake", "food", "the food", "from frozen",
                     "thaw", "thawing", "thawed", "for dinner", "before cooking", "cook it"),
              bias=2),
        entry("appliance-broken",
              (("washing machine", "washer", "washer dryer", "tumble dryer", "dryer", "dishwasher",
                "fridge", "freezer", "fridge freezer", "oven", "cooker", "hob", "microwave", "kettle",
                "toaster", "vacuum", "hoover", "blender", "extractor fan", "telly", "television",
                "appliance", "white goods"),
               ("broken", "broke", "dead", "died", "has died", "packed in", "packing in", "given up",
                "stopped working", "stopped", "wont come on", "won't come on", "wont turn on",
                "won't turn on", "wont switch on", "won't switch on", "wont start", "won't start",
                "not working", "isnt working", "isn't working", "faulty", "nothing happens",
                "what can i do", "what do i do")),
              "A dead appliance is usually the plug, the fuse or a door switch: swap the fuse, try "
              "another socket, shut the door firmly and look the fault code up in the manual. If it "
              "stays dead, take the model number off the sticker and ask the maker or a local repairer "
              "for a fixed-price quote, because under six years old a repair is usually the cheaper "
              "way.",
              avoid=("leak", "leaks", "leaking", "drain", "drains", "draining", "wont drain",
                     "not draining", "smell", "smells", "smelly", "musty", "damp", "tripping",
                     "trips", "trip", "fuse box", "rcd", "cuts out", "cutting out", "keeps stopping",
                     "switches itself off", "switching itself off", "noise", "noisy", "banging",
                     "rumbling", "beep", "beeping", "cold", "not cold", "warm", "freezing", "ice",
                     "frost", "defrost", "condenser", "dry properly", "takes ages",
                     "boiler", "the heating", "central heating", "radiator", "radiators",
                     "landlord", "letting agent", "rent", "worth", "repair", "repairing", "replace",
                     "replacing", "new one", "buy a new one", "buy new", "scrap", "scrapping",
                     "engineer", "phone", "laptop", "computer", "tablet", "console", "car", "van",
                     "bike", "bicycle", "cook it", "recall",
                     "full", "full up", "too full", "packed", "overfull", "no room", "no space",
                     "stuffed"),
              guard=_not_a_cook_ask),
        *list(_the_stopped_fixture_entries(entry)),
        entry("repair-or-replace",
              (("washing machine", "washer", "tumble dryer", "dryer", "dishwasher", "fridge", "freezer",
                "oven", "cooker", "hob", "microwave", "vacuum", "hoover", "boiler", "kettle", "toaster",
                "mower", "lawnmower", "strimmer", "hedge trimmer", "leaf blower", "blender",
                "hair dryer", "hairdryer", "appliance", "machine", "white goods"),
               ("worth repairing", "worth fixing", "worth mending", "worth replacing", "repair or replace",
                "replace or repair", "fix it or", "repair it or", "buying new", "buy new", "worth",
                "repair", "repairing", "fix", "fixing", "replace", "replacing", "mend", "mending",
                "scrap", "scrapping", "broken", "broke", "engineer", "call someone",
                "not heating", "isnt heating", "isn't heating", "wont heat", "won't heat", "heat up",
                "not spinning", "wont spin", "won't spin", "not turning", "wont turn", "won't turn",
                "not draining", "wont drain", "won't drain", "not drying", "takes ages", "still wet",
                "new one", "buy a new one",
                "myself", "my self", "diy", "my own", "on my own", "have a go", "give it a go",
                "can i fix", "can i repair", "can i replace", "can i change", "could i fix",
                "need a new", "need new", "needs a new")),
              _repair_judgement,
              ask=("worth", "replace", "replacing", "repair or", "or repair", "new one", "buying new",
                   "buy new", "scrap", "scrapping", "mend or", "fix it or", "repair it or", "either",
                   "repair it", "fix it", "replace it", "should i repair", "should i fix",
                   "should i replace", "mend it",
                   "worth fixing", "worth mending", "fixed or", "fixing or", "get it fixed",
                   "get a new one", "get a replacement",
                   "fix this one", "repair this one", "mend this one", "or fix this", "or repair this",
                   "or fix that", "or repair that",
                   "engineer", "engineers", "call someone out", "call someone", "call out",
                   "get someone in", "someone in",
                   "can i fix", "could i fix", "can i repair", "could i repair", "can i replace",
                   "can i change", "myself", "my self", "diy", "diy job", "have a go",
                   "give it a go",
                   "need a new", "need new", "needs a new"),
              avoid=("jumper", "wool", "shrank", "shrink", "clothes", "shirt", "coat", "curtains",
                     "car", "bike", "bicycle", "laptop", "phone", "computer", "rent", "landlord",
                     "flat", "radiator", "boiler service",
                     "the heating", "central heating",
                     "worth getting", "worth buying", "shop for", "choose", "choosing", "slow cooker",
                     "pressure cooker", "rice cooker", "air fryer", "dishwasher tablets",
                     "noise", "noisy", "banging", "leak", "leaking", "mould", "musty", "smell",
                     "smells",
                     "drain", "drains", "draining", "wont drain", "won't drain", "pump", "filter",
                     "water everywhere", "not emptying",
                     "belt", "belts", "drive belt", "brush bar", "brushbar", "brush roll",
                     "impeller", "beater bar"),
              bias=2),
        entry("extractor-fan-noisy",
              (("extractor", "cooker hood", "extractor hood", "kitchen hood", "range hood", "hob",
                "grease filter", "filter", "filters"),
               ("noisy", "loud", "noise", "rattling", "rattle", "vibrating", "buzzing", "humming",
                "grinding", "sucking", "suck", "weak", "clean", "filter", "filters", "grease filter",
                "smells")),
              avoid=("bathroom", "loo", "toilet", "shower", "bath", "fan oven", "car", "cars", "engine",
                     "bonnet", "truck", "van", "bike", "loft", "tumble dryer", "dryer", "heating",
                     "radiator", "air vent", "air conditioning", "aircon"),
              reply=the_filter_of(("extractor", "cooker hood", "extractor hood", "kitchen hood",
                                   "range hood", "hob", "grease filter"),
                                  EXTRACTOR_GREASE_FILTER)),
        entry("place-smell",
              (("smell", "smells", "smelly", "smelling", "stink", "stinks", "stinking", "reek",
                "reeks", "reeking", "odour", "odor", "smells like",
                "smell in", "smells in", "smell from", "smells from", "smell of", "stink in",
                "stinks in", "get rid of the smell", "how do i get rid of the smell"),
               ("shed", "garage", "loft", "attic", "cellar", "basement", "cupboard",
                "wardrobe", "spare room", "conservatory", "porch", "hall", "hallway", "utility",
                "utility room", "outhouse", "bin store", "storage room", "room", "rooms", "house",
                "flat", "empty house", "holiday let", "under the stairs", "stair cupboard",
                "bathroom", "bedroom", "kitchen", "landing", "cloakroom", "guest room",
                "wet room", "shower room", "en suite", "ensuite", "wash room",
                "car boot", "boot of the car", "boot of my car", "the boot of", "boot of a car")),
              _place_smell,
              avoid=("fridge", "freezer", "bin", "bins", "bin day", "wheelie", "car", "cars", "van",
                     "washing machine", "dishwasher", "drain", "drains", "plughole", "toilet", "loo",
                     "sink", "shower", "bath", "mould", "mold", "mildew", "damp", "condensation",
                     "smoke", "gas", "carbon monoxide",
                     "petrol", "petrol fumes", "diesel", "fuel", "oil", "paraffin", "kerosene",
                     "paint", "paint fumes", "painting", "painted", "thinner", "white spirit",
                     "solvent", "bleach", "ammonia", "chlorine", "sewage", "rotten", "rot",
                     "sweat", "sweaty", "mice", "mouse", "vomit", "sick", "urine", "pee",
                     "curry", "cabbage", "weed", "fish",
                     "musty", "damp smell", "smells of damp", "smell of damp", "dog", "cat", "pet", "my breath", "breath",
                     "feet", "foot", "body", "armpit", "mouth", "kettle", "oven", "microwave",
                     "food", "cooking", "fish", "fridge freezer", "tap", "water", "hoover", "vacuum",
                     "washing", "clothes", "mattress", "sofa", "carpet",
                     "my boots", "my shoes", "my trainers", "these boots", "these shoes",
                     "pair of boots", "football boots", "work boots", "walking boots",
                     "hiking boots", "shoes", "shoe", "trainers", "slippers", "sandals",
                     "wellies", "welly",
                     "cabbage", "burnt", "burning", "burn", "fried", "frying", "bacon", "curry",
                     "garlic", "spices", "boiled", "drains smell", "nice", "nicer", "lovely",
                     "fresh", "fresher", "freshen", "pleasant", "good", "better"),
              bias=2),
        entry("soft-thing-smell",
              (("soft furnishing", "carpet", "carpets", "rug", "rugs", "sofa", "sofas", "settee",
                "settees", "armchair", "armchairs", "cushion", "cushions", "curtain", "curtains",
                "car seat", "car seats", "car", "cars", "mattress",
                "carpet smells of", "carpet smells like", "carpets smell of", "rug smells of",
                "rug smells like", "sofa smells of", "sofa smells like", "settee smells of",
                "settee smells like", "armchair smells of", "cushion smells of", "cushions smell of",
                "curtains smell of", "car smells of", "car smells like", "seat smells of",
                "mattress smells of", "mattress smells like"),
               ("smells of", "smells like", "smells", "smell of", "stinks of", "stinks", "stink",
                "reeks of", "reeks", "reeking", "pong", "whiffs", "whiff", "scent")),
              _soft_smell,
              avoid=("damp", "musty", "mould", "mouldy", "mold", "moldy", "mildew", "condensation",
                     "smoke", "smoky", "cigarette", "gas", "petrol", "diesel", "fuel", "paint",
                     "bleach", "bin", "bins", "washing machine", "washer", "dryer", "dishwasher",
                     "fridge", "freezer", "oven", "microwave", "kettle", "drain", "drains",
                     "sink", "toilet", "loo", "new car", "nice", "fresh", "freshen", "clean",
                     "remove", "get out", "how do i clean", "wash", "shampoo", "vacuum",
                     "sick", "vomit", "vomited", "vomiting", "milk", "wine", "coffee", "tea",
                     "juice", "spilt", "spilled", "spilling", "stain", "stains", "stained",
                     "burning", "burnt", "burn", "scorching", "scorched", "hot smell",
                     "smells hot", "overheating", "overheated", "brakes", "brake pads", "clutch",
                     "exhaust", "burning rubber", "electrical", "smoke", "fumes")),
        entry("fridge-smell",
              (("fridge", "freezer", "fridge freezer"),
               ("smell", "smells", "smelly", "stink", "stinks", "odour", "odor", "reek")),
              "Throw out whatever has gone off, then wash the shelves and drawers with hot soapy water "
              "and dry them. The usual hiding places are the door seal, which needs wiping in the folds, "
              "and the drain hole at the back, which you can clear with a cotton bud or a bit of wire. A "
              "small bowl of bicarbonate of soda on a shelf takes out what's left; change it monthly.",
              guard=_not_the_food_in_the_fridge),

        entry("appliance-noise",
              (("fridge", "refrigerator", "freezer", "fridge freezer", "washing machine", "washer",
                "dishwasher", "dish washer", "tumble dryer", "dryer", "oven fan", "oven", "kettle",
                "microwave", "vacuum", "hoover",
                "fan", "fans", "ceiling fan", "desk fan", "pedestal fan", "floor fan"),
               ("hum", "hums", "humming", "buzz", "louder",
                "buzzing", "rattle", "rattles", "rattling", "click", "clicks", "clicking",
                "knock", "knocks", "knocking", "bang", "bangs", "banging", "squeak", "squeaks",
                "squeaking", "squeal", "squeals", "squealing", "grind", "grinds", "grinding",
                "screech", "screeches", "screeching", "shriek", "shrieks", "shrieking",
                "scream", "screams", "screaming", "clunk", "clunks", "clunking",
                "clank", "clanks", "clanking",
                "gurgle", "gurgles", "gurgling", "whirr", "whirring", "scrape", "scraping",
                "vibrate", "vibrating", "shaking", "thump", "thumping", "whine", "whining",
                "tick", "ticking", "whistling") + NOISE_WORDS),
              _appliance_noise,
              avoid=("fridge", "freezer", "refrigerator", "washing machine", "washer", "boiler",
                     "radiators", "radiator", "heating", "laptop", "computer", "pc",
                     "playstation", "ps5", "ps4", "xbox", "console", "games console", "nintendo",
                     "phone", "car", "engine", "mot", "neighbour", "neighbours", "music", "tv",
                     "radio", "fan heater", "smell", "smells", "smelling", "smelly", "stink",
                     "stinks", "burning", "burnt", "burn", "smoke", "smoking", "smoky", "fire",
                     "spark", "sparks", "sparking", "gas", "fumes", "leak", "leaks", "leaking",
                     "leaked", "flood", "flooding", "wiring", "sockets",
                     "ref", "referee", "crowd", "stadium", "terrace", "sang", "seat", "seats",
                     "extractor", "extractor fan", "cooker hood", "extractor hood", "range hood",
                     "kitchen hood", "hood", "hoods", "hob", "grease filter",
                     "bathroom", "loo", "toilet", "shower", "shower room", "wet room", "en suite",
                     "ensuite")),
        entry("washing-machine-wont-stop",
              (("washing machine", "washer", "washer dryer", "washing mashine", "drum"),
               ("keeps running", "keep running", "kept running", "runs forever", "running forever",
                "running for hours", "wont stop", "won't stop", "wont stop filling", "wont stop beeping",
                "keeps filling", "keep filling", "doesnt stop", "doesn't stop", "never stops",
                "wont turn off", "won't turn off", "keeps going", "stuck on a cycle",
                "stuck on the same cycle")),
              "A machine that will not stop is waiting for something it cannot do: switch it off at the "
              "wall and turn the water off at the valve behind it, then clean the filter behind the kick "
              "plate and check the drain hose is not kinked. Set it to drain or spin only and start it "
              "again. If it fills even with the water off, the water-level pressure switch has failed, "
              "which is an engineer's job.",
              bias=2,
              avoid=("door", "doors", "locked", "lock", "wont open", "won't open", "smell", "smells",
                     "leak", "leaking", "noise", "noisy", "banging", "rattling", "which", "best",
                     "buy", "sort", "colours", "colors", "whites", "darks")),
        entry("washing-machine-wont-drain",
              (("washing machine", "washer", "drum", "spin cycle", "wash cycle"),
               ("drain", "draining", "wont drain", "won't drain", "empty", "water", "pump",
                "blocked", "blockage", "clogged", "not emptying", "backed up", "backing up")),
              "The filter is the usual culprit, behind the little kick plate at the bottom front: put a "
              "shallow bowl and a towel down, unscrew it slowly and pull out the coins and hair. Then "
              "check the drain hose behind the machine isn't kinked or pushed too far into the standpipe. "
              "If it still won't empty, the pump needs replacing, which is a cheap part and a half-hour "
              "job for an engineer.",
              bias=2,
              guard=_a_machine_that_will_not_empty,
              avoid=("buy", "which", "best", "door", "doors", "locked", "lock", "shut", "open",
                     "leak", "leaks", "leaked", "leaking", "coming out", "pouring out", "pouring",
                     "flooded", "flooding", "underneath",
                     "jet", "jets", "nozzle", "nozzles", "windscreen", "windshield",
                     "screen wash", "washer fluid", "washer jet", "washer jets")),
        entry("washing-machine-filter",
              (("washing machine", "washer", "washer dryer", "washing mashine", "filter", "filters"),
               ("filter", "filters", "filter cap", "pump filter",
                "drain pump", "pump cap", "clean the pump", "clear the pump")),
              bias=3,
              reply=the_filter_of(("washing machine", "washer", "washer dryer", "washing mashine"),
                                  WASHING_MACHINE_FILTER)),
        entry("washing-machine-drawer",
              (("washing machine", "washer", "washer dryer", "washing mashine", "laundry",
                "detergent drawer", "soap drawer", "powder drawer", "dispenser drawer",
                "fabric softener drawer"),
               ("drawer", "drawers", "dispenser", "compartment", "detergent", "soap", "powder",
                "trap", "gunk", "slimy", "sticky", "scrub")),
              "Pull the drawer right out until it stops, press the release catch in the middle of the "
              "softener compartment, and take it to the sink. Lift out the cap and the siphon tube, "
              "soak everything in hot water with a little washing-up liquid or a dishwasher tablet for "
              "half an hour, then scrub the corners with an old toothbrush. Reach into the housing left "
              "in the machine and scrub the top and the back of it too, because that is where the black "
              "grows, and run an empty hot rinse before the next load. Use powder now and then and "
              "leave the drawer open between washes: softener is what feeds it.",
              avoid=("door seal", "rubber", "seal", "mould in the seal", "black around the door",
                     "kitchen", "bedside", "desk", "chest of drawers", "cutlery", "sock", "socks",
                     "fridge", "freezer", "wardrobe", "bathroom cabinet",
                     "where do i put", "where do the", "where does", "where should i put",
                     "which compartment", "what compartment", "where do the tablets",
                     "dishwasher", "dish washer", "tumble dryer", "tumble drier"),
              bias=3),
        entry("washing-machine-descale",
              (("washing machine", "washer", "washer dryer", "washing mashine", "washing",
                "laundry", "drum"),
               ("descale", "descaling", "descaler", "limescale", "scale", "scaled", "scaling",
                "calcium", "hard water", "chalky", "white flakes", "flakes on the washing")),
              "Run a descaler through an empty drum on the hottest cycle: a 500g bag of citric acid "
              "from a hardware shop, or a washing-machine descaler, straight into the drum rather than "
              "the drawer, at 60C or 90C, then a rinse cycle with nothing in it. In a hard water area "
              "that is every three months; where the water is soft, once a year is enough. White "
              "flakes on dark washing and a machine that takes longer to heat are the two signs it is "
              "due, and a filter full of grit after the cycle is normal. Skip vinegar: it is hard on "
              "the rubber and the seals, and citric acid does the job better.",
              avoid=("kettle", "coffee machine", "coffee", "dishwasher", "shower head", "shower",
                     "iron", "steam iron", "tap", "taps", "boiler", "dehumidifier", "humidifier",
                     "water softener", "hot tub", "pool", "fish tank", "aquarium", "toilet",
                     "buy", "best", "which", "brand", "price", "cheap", "worth it"),
              bias=3),
        entry("tumble-dryer-filter",
              (("tumble dryer", "tumble drier", "tumble", "dryer", "drier", "filter", "filters"),
               ("filter", "filters", "fluff", "lint", "blocked", "clogged", "clean", "cleaning",
                "full",
                "hair", "pet hair", "dog hair", "cat hair", "fur")),
              avoid=("hairdryer", "hair dryer", "hair drier", "washing machine", "washer", "dishwasher",
                     "worth", "worth it", "should i", "do i need", "need a",
                     "buy", "which", "best", "price", "repair", "not heating", "wont heat",
                     "not spinning", "makes a noise", "squeak"),
              bias=3,
              reply=the_filter_of(("tumble dryer", "tumble drier", "tumble", "dryer", "drier"),
                                  TUMBLE_DRYER_FILTER)),
        entry("washing-machine-door-stuck",
              (("washing machine", "washer", "dryer", "tumble dryer"),
               ("door", "stuck", "wont open", "won't open", "locked", "shut", "open")),
              "Give it three or four minutes: the lock holds until the drum has stopped and the water has "
              "drained. If there's water inside, run a drain or spin cycle first. When it's empty and "
              "still locked, most machines have an emergency release: a small plastic tag or cord behind "
              "the filter hatch that you pull down while pushing the door. Don't force the handle, "
              "because the catch breaks before the door does.",
              avoid=("buy", "which", "best")),
        entry("dishwasher-wont-drain",
              (("dishwasher", "dish washer", "dishdrawer", "dish drawer"),
               ("drain", "draining", "wont drain", "won't drain", "not draining", "emptying",
                "not emptying", "wont empty", "won't empty", "full of water", "water in the bottom",
                "water left in", "standing water", "puddle", "left in the bottom",
                "sitting in the bottom",
                "blocked", "blocked up", "blockage", "clogged")),
              "Start with the filter: it twists out of the bottom of the drum, and a rinse under the hot "
              "tap with a check for glass or a label in the sump usually fixes it. Then look at the drain "
              "hose where it joins the waste under the sink, because a kink or a blockage there leaves "
              "exactly that water in the bottom. If it hums and still won't empty with both clean, the "
              "drain pump needs swapping, which is a cheap part and a quick job for a repairer.",
              avoid=("smell", "smells", "clean", "cleaning", "cloudy", "streaks", "salt", "rinse aid",
                     "buy", "which", "best", "leak", "leaking", "fill", "fills", "filling",
                     "how much water", "uses", "use a lot", "efficient",
                     "empty the dishwasher", "emptied", "unload", "unloading", "quickly")),
        entry("dishwasher-leak",
              (("dishwasher", "dish washer", "dishdrawer", "dish drawer"),
               ("leak", "leaking", "leaks", "leaked", "puddle", "puddles", "dripping", "flooding",
                "water coming out", "water coming from", "water coming", "water under",
                "water underneath", "water all over", "water on the floor", "on the floor",
                "all over the floor", "coming out of the bottom", "underneath it", "under it",
                "wont stop leaking", "won't stop leaking")),
              "Turn it off at the wall and shut the water off at the little isolator tap under the "
              "sink, then get the water up - a shallow tray and a towel is enough for a slow one. "
              "Water at the front of the door is usually the door seal or the filter, so twist the "
              "filter out and check the seal for food or a split; water underneath is the inlet or "
              "drain hose where it joins the machine or the waste, so check those joints first. "
              "Leave it off until that seal or joint is fixed: a leak from inside the machine "
              "itself is a repairer's job.",
              avoid=("buy", "which", "best", "cheapest", "price", "cost",
                     "wont drain", "won't drain", "not draining", "not emptying", "wont empty",
                     "won't empty", "full of water", "water in the bottom", "standing water",
                     "left in the bottom", "filter", "pump", "empty", "emptying",
                     "smell", "smells", "smelly", "cloudy", "streaks", "salt", "tablet",
                     "rinse aid", "still wet", "wont dry", "won't dry", "how much water",
                     "uses", "use a lot", "install", "installing", "fit a", "fitting"),
              bias=1),
        entry("machine-consumables",
              (("salt", "tablet", "tablets", "powder", "detergent", "liquid", "pod", "pods",
                "capsule", "capsules", "rinse aid", "rinse-aid", "softener", "conditioner",
                "dishwasher cleaner"),
               ("where do i put", "where do the", "where do i add", "where do i fill",
                "where does", "where should i put", "where to put", "where in the",
                "which compartment", "what compartment", "top up", "topup", "how much",
                "which bit", "run out", "ran out", "refill", "where", "put", "fill", "go",
                "goes",
                "and the", "what about the", "and what about the", "how about the")),
              _where_the_consumable_goes,
              avoid=("cloudy", "streaks", "white marks", "film", "smell", "smells", "smelly",
                     "wont dry", "won't dry", "still wet", "wet dishes", "drain", "draining",
                     "leak", "leaking", "buy", "which", "best", "price", "cost", "how often",
                     "repair", "broken", "not working", "error"),
              guard=_a_machine_consumable, bias=1),
        entry("dishwasher-wet",
              (("dishwasher", "dish washer", "dishdrawer", "dish drawer"),
               ("dishes are wet", "dishes still wet", "dishes come out wet", "leaves the dishes wet",
                "leaves everything wet", "not drying", "isnt drying", "isn't drying", "wont dry",
                "won't dry", "still wet", "wet dishes", "wet after", "water on the dishes",
                "water left on", "comes out wet", "everything is wet"),
               ("dishes", "dish", "plates", "glasses", "crockery")),
              "Rinse aid and salt first: without rinse aid the water clings in drops, so fill the "
              "rinse-aid compartment and set it to 4 or 5, and top up the salt. Use the hottest "
              "programme you have and open the door an inch when it finishes so the steam escapes; "
              "plastic always dries worse than china. If the load is still soaked, clean the filter "
              "and check the spray arms turn freely.",
              ask=("wet", "drying", "dry", "damp", "water", "soaked"),
              avoid=("wont drain", "won't drain", "not draining", "drain", "draining",
                     "full of water", "water in the bottom", "standing water", "leak", "leaking",
                     "smell", "smells", "smelly", "cloudy", "white marks", "streaks", "clean",
                     "cleaning", "worth", "replace", "repair", "quote", "cost", "buy", "which",
                     "best",
                     "hum", "hums", "humming", "hummed", "noise", "noisy", "loud", "louder",
                     "rattle", "rattles", "rattling", "squeak", "squeaks", "squeaking",
                     "bang", "bangs", "banging", "knock", "knocks", "knocking", "grind",
                     "grinding", "vibrate", "vibrating", "clunk", "clunks", "clunking")),
        entry("heating-programmer", (("boiler", "heating", "thermostat", "boiler timer",
                                      "timer on the boiler",
                                      "boiler programmer", "heating programmer", "heating timer",
                                      "programmer", "programmer on the boiler", "timer for the "
                                      "heating", "heating times", "heating clock",
                                      "thermostat schedule", "thermostat times", "thermostat timer",
                                      "time on the thermostat", "thermostat clock",
                                      "clock on the thermostat", "heating schedule",
                                      "heating programme", "heating program"),
                                     ("timer", "set", "setting", "change", "times", "time",
                                      "programme", "program", "adjust", "clock", "am", "pm")),
              "Set the clock and the day on the programmer first, because every on and off time you "
              "enter is measured from it. Then give each channel two blocks: heating on about half an "
              "hour before you get up and off when you leave, then on again before you come back and "
              "off at bedtime, and the hot water channel set to a morning and an evening block. Put "
              "the room thermostat at 18 to 19C while you are in and 15 to 16C overnight, and let the "
              "thermostat do the switching rather than turning the programmer up and down. A combi "
              "boiler with a smart thermostat wants the heating channel left on constant, because the "
              "thermostat is doing the timing.",
              ask=("time", "times", "clock", "clocks", "schedule", "schedules", "programme",
                   "program", "programmer", "timer", "timing", "am", "pm", "on and off",
                   "what time", "the time", "change the time", "set the time"),
              avoid=("phone", "app", "oven", "washing machine", "dishwasher", "sprinkler", "light",
                      "christmas", "fault", "error", "not working", "broken", "temperature",
                      "flow", "pressure", "leak", "leaking", "noise", "noisy", "smell")),
        entry("boiler-flow",
              (("boiler flow", "boiler flow temperature", "flow temperature", "flow temp",
                "boiler temperature", "boiler thermostat", "boiler dial", "boiler setting",
                "temperature on the boiler", "temperature of the water in the boiler",
                "boiler", "boilers"),
               ("temperature", "hot", "hotter", "cooler", "lower", "turn down", "turn it down",
                "flow", "what temperature", "how hot", "number", "what number",
                "set", "setting", "should", "what", "how hot", "change", "adjust", "efficient",
                "efficiency", "55", "60", "condensing", "combi")),
              "Set the flow temperature on the boiler dial to 55 to 60C. That is the temperature of "
              "the water going round the radiators, and the lower it is the less gas each hour costs, "
              "because a condensing boiler only recovers its waste heat with a cool return. If the "
              "house is slow to warm, go to 65C and turn the room thermostat down again rather than "
              "going higher than that. A hot water cylinder stays at 60C whatever the heating is set "
              "to, so the two numbers are not the same dial.",
              avoid=("pressure", "leak", "leaking", "fault", "error", "not working", "broken",
                     "turn down a radiator", "turn down the radiator", "one radiator",
                     "rad valve", "radiator valve", "trv", "thermostatic valve",
                     "too hot", "very hot", "overheat", "overheating", "scald", "scalding",
                     "noise", "noisy", "smell", "fumes", "carbon monoxide", "pilot light",
                     "service", "serviced", "servicing", "engineer", "install", "replace",
                     "how much", "price", "bill", "tariff", "cost"),
              guard=not_a_sound),
        entry("where-is-the-model-number",
              (("model number", "model no", "model num", "serial number", "serial no",
                "rating plate", "data plate", "data badge", "spec plate", "type plate",
                "product number", "benchmark sheet", "benchmark logbook", "benchmark"),
               ("boiler", "boilers", "combi", "washing machine", "washer", "dishwasher",
                "fridge", "freezer", "fridge freezer", "oven", "cooker", "dryer",
                "tumble dryer", "microwave", "vacuum", "hoover", "kettle", "toaster",
                "appliance", "appliances", "the machine", "my machine", "white goods",
                "manual", "user guide", "sticker", "rating plate", "data plate")),
              "It is on a plate or sticker you can read without moving the machine: on a boiler, "
              "under the case near the pipes, behind the drop-down flap or on the side panel, and "
              "the Benchmark sheet in the manual carries the same serial. On a washing machine or "
              "dishwasher it is on the rim inside the door, on a fridge or freezer inside on a "
              "side wall or the inner door, on an oven on the frame or the door edge, and on a "
              "kettle, toaster or microwave underneath. The model number is the short code and "
              "the serial is the longer one - the parts shop or the maker's site wants both, so "
              "photograph the plate once you have found it.",
              avoid=("which boiler", "what boiler", "new boiler", "buy", "buying", "replace",
                     "replacing", "price", "cost", "how much", "quote", "efficiency", "size",
                     "kw", "output", "fault", "error", "not working", "broken", "leak",
                     "leaking", "noise", "noisy", "pressure", "service", "serviced")),
        entry("radiator-turn-down",
              (("radiator", "radiators", "rad valve", "radiator valve", "trv", "thermostatic valve",
                "valve on the radiator", "towel rail"),
               ("turn down", "turn it down", "turning down", "lower", "too hot", "hot", "cooler",
                "adjust", "set", "setting", "one radiator", "in the bedroom", "in a bedroom",
                "which way", "number",
                "down", "full", "on full", "full blast", "max", "maximum", "on high",
                "roasting", "scorching", "boiling", "overheating", "cant sleep", "cannot sleep",
                "up", "turn up", "turn it up", "turning up", "turn", "turning", "turned",
                "off", "turn off", "turn it off", "switch off", "switched off", "off position",
                "numbers", "dial", "trv", "thermostatic", "snowflake", "frost setting",
                "frost mark", "what setting")),
              "Turn the numbered head at one end of the radiator down a notch or two - that is the "
              "valve that sets the room, and the numbers are roughly 2 for 16C, 3 for 18C and "
          "4 for 21C. A bedroom "
              "wants 16 to 18C for sleep, so 2 is usually the setting there, and turning it down is "
              "the way to cool a room that a radiator has made too warm. Leave the plain "
              "valve at the other end alone; it is the balance for the whole system. Turn it to the "
              "snowflake - frost protection, about 7C - in a room nobody uses, and give it until "
          "the next morning, because a radiator takes an hour to show a change. If the head does "
          "not click and the radiator stays as "
              "hot, the pin under it is stuck: take the head off and work the pin free with pliers.",
              avoid=("leak", "leaking", "drip", "puddle", "bleed", "bled",
                 "pressure", "bar", "psi", "gauge", "filling loop", "top up", "topping up",
                 "cold at the top",
                     "cold at the bottom", "not heating", "stays cold", "noise", "banging", "kettling",
                     "buy", "which radiator", "which rad", "which boiler", "which one", "which type",
                     "best", "how many", "size", "boiler", "install", "replace")),
        entry("thermostat-battery",
              (("thermostat", "thermostats", "room thermostat", "boiler thermostat", "hive", "nest",
                "tado", "smart thermostat", "heating controls", "thermostat display"),
               ("battery", "batteries", "low battery", "battery low", "battery flat", "change the "
                "batteries", "replace the batteries", "new batteries", "cell", "cells",
                "goes blank", "blank screen", "keeps losing the signal", "flashing")),
              "Take the front off the thermostat and change the cells: most take two AA or AAA, and "
              "the battery cover is either the whole front pulling off its wall plate, as on a Hive, "
              "or a small slide-out tray at the side. Use alkalines rather than rechargeables, because "
              "a rechargeable cell sits at 1.2V and the unit reads that as low. After new cells give "
              "it five minutes to find the hub again, then check the time and schedule, which is what "
              "a dead battery loses.",
              avoid=("bin", "recycle", "recycling", "dispose", "disposal", "phone", "iphone", "watch",
                     "car", "key fob", "smoke alarm", "doorbell", "camera")),
        entry("heating-temperature",
              (("heating", "radiator", "radiators", "thermostat", "house", "flat", "home", "room",
                "rooms", "bedroom", "bedrooms", "living room", "sitting room"),
               ("temperature", "how warm", "how hot", "warm enough", "too cold", "freezing", "cold",
                "keep it at", "set it at", "set the", "keep the heating", "all day", "overnight",
                "at night", "timer",
                "put the heating on", "put the heating", "turn the heating on", "turn the heating off",
                "turn the heating", "switch the heating", "heating on yet", "heating off",
                "my heating up", "my heating down", "our heating up", "our heating down",
                "turn my heating up", "turn my heating down", "turn our heating up",
                "turn our heating down", "turn down my heating", "turn up my heating",
                "turn down our heating", "turn up our heating",
                "turn it on", "turn it off", "have the heating",
                "set my thermostat", "set the thermostat", "change my thermostat",
                "bedroom thermostat", "thermostat at night", "set my bedroom",
                "what should i set my", "what should i set the",
                "change the thermostat", "thermostat setting", "thermostats", "what temperature",
                "what temp", "what should i set", "how should i set", "set it to", "set the heating",
                "set the heating times", "set the heating timer", "heating timer", "heating times",
                "programme the heating", "program the heating")),
              "18C is the usual living-room setting and 16C for bedrooms, with 20C to 21C for a baby's "
              "room, for someone ill or elderly, or for anyone who feels the cold. Go by the room, not "
              "the calendar: put it on when the living room drops below about 18C, or when you are "
              "sitting still and feel cold, and then set it and leave it, turning it down at night or "
              "when you're out rather than running it low all day. If the rooms never get to 18C with "
              "the heating on, that's a boiler or radiator problem rather than a thermostat one.",
              avoid=("bleed", "bleeding", "bottom", "top", "noise", "noisy", "bang", "banging", "kettle",
                     "leak", "leaking", "drip", "dripping", "pressure", "boiler", "landlord", "bill",
                     "bills", "cheaper", "cost", "price", "money", "saving", "save", "feel", "feeling",
                     "always", "hands", "feet", "shivering", "tired", "thyroid",
                     "flu", "cough", "stuck", "company", "greece", "spain", "holiday", "raining",
                     "rain", "sun", "heatwave", "work all day", "out all day",
                     "go away", "going away", "away for", "when im away", "when i am away",
                     "while im away", "on holiday", "empty house", "house is empty", "nobody in",
                     "keep the heat out", "heat out", "stop the sun", "sun heating", "block the sun",
                     "the sun coming in", "sun comes in", "sun through",
                     "pipes", "pipes freeze", "pipes dont freeze", "pipes from freezing",
                     "room temperature is", "39", "40", "41", "42", "fever",
                     "oven", "cook", "cooking", "roast", "bake", "chicken", "meat", "bath", "water",
                     "egg", "eggs", "butter", "milk", "cheese", "dough", "yeast", "batter",
                     "chocolate", "cake", "yoghurt", "yogurt", "defrost", "thaw",
                     "not working", "broken", "fault", "error", "thermometer", "sick", "unwell",
                     "garage",
                     "wont", "won't", "come on", "coming on", "wont come on", "stuck on",
                     "not coming on", "no heating",
                     "change the time", "set the time", "the time on", "clock", "clocks",
                     "clock is wrong", "clock wrong", "schedule", "schedules", "set the schedule",
                     "the schedule for", "programmer",
                     "battery", "batteries", "low battery", "blank screen", "display blank",
                     "keeps losing the signal"),
              ask=("temperature", "how warm", "how hot", "warm enough", "keep it at", "set it at",
                   "keep the heating", "leave the heating", "leave it on", "heating on", "thermostat",
                   "degrees", "timer", "overnight", "too cold",
                   "put the heating", "turn the heating", "switch the heating", "heating off",
                   "heating on yet", "turn it on", "turn it off", "have the heating",
                   "turn my heating", "turn our heating", "my heating up", "my heating down",
                   "our heating up", "our heating down", "turn down my heating", "turn up my heating",
                   "turn down our heating", "turn up our heating")),
        entry("boiler-leak",
              ("boiler", ("drip", "dripping", "drips", "leak", "leaking", "leaks", "puddle",
                          "underneath", "overflow", "water under", "water coming", "water everywhere",
                          "water all over", "spraying", "spurting",
                          "water is coming", "water coming out", "water out", "water is dripping",
                          "water leaking", "water pouring", "water is pouring", "water coming from")),
              "Turn the boiler off at the wall switch (not at the fuse board, you want the pump to run on "
              "for a minute first), put a bowl under it and turn the water off at the stopcock if it's "
              "more than a drip. A leak from the boiler casing itself is a Gas Safe engineer's job: don't "
              "take the cover off, and don't keep resetting it. Water running from the pressure relief "
              "pipe outside means the pressure is too high, which needs looking at too.",
              avoid=("buy", "best", "cost", "price", "install", "new", "landlord", "tenant",
                     "not heating", "isn't heating", "isnt heating", "heating the water", "no hot water",
                     "no heating")),
        entry("leak-under-sink",
              (("sink", "under the sink", "waste", "trap", "u-bend", "ubend", "pipe"),
               ("leak", "leaking", "drip", "dripping", "water", "puddle", "fix", "wet patch",
                "wet", "soaked", "pool", "pooling", "spreading", "damp patch", "damp")),
              "Dry everything, put a bowl under the trap and run the tap to see where the water appears. "
              "A drip at a plastic joint is nearly always a hand-tight nut: give it another quarter turn, "
              "no more, because overtightened plastic splits. If it's the trap, unscrew it, clean out the "
              "gunge, check the rubber washer is seated and put it back. Wrapping PTFE tape on a plastic "
              "thread makes it worse, not better.",
              avoid=("blocked", "smell", "slow", "drain",
                     "ear", "ears",
                     "less water", "save water", "saving water", "wasting water", "waste less",
                     "water use", "water usage", "water bill", "use so much water")),
        entry("flooded-room",
              (("flood", "flooded", "flooding", "under water", "water everywhere",
                "ankle deep", "inches of water", "deep in water", "swimming in water"),
               ("bathroom", "kitchen", "flat", "house", "room", "rooms", "floor", "floors",
                "carpet", "carpets", "hall", "hallway", "cellar", "basement", "bedroom",
                "utility", "downstairs", "upstairs", "everywhere", "lino", "floorboards")),
              "Turn the water off first: the stopcock is usually under the kitchen sink, and if "
              "water is near a socket or a light, switch that circuit off at the consumer unit. "
              "Then stop whatever is running, bail and mop, and get air moving with a fan and an "
              "open window - a floor or skirting that stays wet a day warps and grows mould. "
              "Photograph it before you clear up, and ring the insurer and whoever owns the "
              "building today if it came through the ceiling.",
              avoid=("garden", "lawn", "greenhouse", "shed", "car", "van", "road", "street",
                     "village", "river", "field", "fields", "warning", "risk",
                     "rain", "rains", "raining", "rainwater", "storm", "storms", "winter",
                     "groundwater", "water table", "cellar", "basement", "outside", "drain",
                     "drains", "back door", "under the door", "doorway",
                     "insurance quote", "washing machine", "dishwasher", "toilet",
                     "loo", "radiator", "boiler", "tap", "taps", "sink")),
        entry("water-coming-in",
              (("flood", "flooded", "flooding", "floods", "water", "wet", "seeping", "seeps",
                "rising", "inches deep", "ankle deep", "filling", "coming in", "coming under",
                "coming through", "getting in"),
               ("cellar", "basement", "rain", "rains", "raining", "rainwater", "storm", "storms",
                "outside", "groundwater", "water table", "drain", "drains", "back door",
                "under the door", "doorway", "up through the floor")),
              "Water coming in from outside is not a stopcock: it stops taps, not rain or a "
              "rising water table. Stay out of a cellar with sockets in it, or switch the whole "
              "supply off at the consumer unit first, and pump or wet-vac the water out rather "
              "than mopping it about. Sandbags or a flood door across the doorway help tonight, "
              "photographs help the insurer, and a drain that backs up in a storm is the water "
              "company's to clear.",
              avoid=("stopcock", "washing machine", "dishwasher", "toilet", "loo", "radiator",
                     "boiler", "tap", "taps", "sink", "pipe", "pipes", "burst", "car", "van",
                     "road", "street", "village", "river", "lawn", "greenhouse", "shed",
                     "garden", "yard", "insurance quote", "warning", "risk", "sandbag"),
              bias=2),
        entry("fruit-flies",
              (("fruit fly", "fruit flies", "fruitfly", "gnats", "flies", "fly"),
               ("kitchen", "bin", "get rid", "rid", "stop", "bananas", "everywhere", "plague",
                "sink", "drain", "fruit", "bowl", "traps", "around", "how do i",
                "house", "home", "flat", "room", "rooms", "bedroom", "landing", "land", "lands",
                "on me", "keep", "keeps", "buzzing", "buzz", "swarming", "swarm", "air",
                "window", "windows", "in here", "indoors", "coming in")),
              "Put a little cider vinegar or red wine in a glass with a drop of washing-up liquid: they "
              "fly in and sink. Then take away what they are breeding in - the ripe fruit (into the "
              "fridge for a week), the bottles and the bin, and the plughole, which gets a kettle of "
              "boiling water at night. The glass catches the rest in a day or two.",
              avoid=("fly to", "flight", "flights", "when flying", "by plane", "on a plane",
                     "checked in", "suitcase", "suitcases", "luggage", "checked bag", "hold bag",
                     "holiday", "airport", "insect bite", "butterfly", "butterflies", "dragonfly",
                     "flight home", "fly tip", "fly tipping", "fly-tip", "fly-tipping", "tipping",
                     "tipped", "dumped", "dumping", "mattress", "lay-by", "fly poster",
                     "fear of flying", "scared of flying", "afraid of flying",
                     "zip", "zips", "zipper", "zippers", "zip fly",
                     "am flying", "flying at", "flying out", "flying home", "flying back",
                     "flying off", "flying from", "flying into", "flying tomorrow",
                     "flying next", "flying this", "flying in the morning", "flying on",
                     "fly out", "fly back", "fly home", "fly at", "flying with", "flying over",
                     "anxiety about flying", "nervous about flying",
                     "kite", "kites",
                     "dog", "dogs", "cat", "cats", "puppy", "puppies", "kitten", "kittens",
                     "pet", "pets", "rabbit", "ferret", "hamster", "parrot", "budgie"),
              guard=_the_fly_is_not_a_verb,
              report=True),
        entry("house-smell-nice",
              (("house", "flat", "home", "room", "living room", "hallway", "bedroom"),
               ("smell nice", "smell nicer", "smelling nice", "smell good", "smell fresh",
                "nice smell", "nicer smell", "fresh smell", "smell better", "nice scent", "fresh",
                "freshen", "smells", "smell", "smelly", "stinks")),
              "Open windows at both ends of the flat for ten minutes; that shifts more than anything you "
              "spray. Then wash the things that hold smell: bedding, cushions, the bath mat, the bin lid. "
              "Bicarbonate of soda on the carpet, left an hour and vacuumed, lifts stale air, and a pan "
              "of water with lemon peel and a cinnamon stick simmered for ten minutes does the rest. "
              "Air fresheners mask it; the fix is finding the source, often the bin, the drain or damp.",
              avoid=("damp", "musty", "mould", "mold", "drain", "gas", "burning", "smoke"),
              ask=("nice", "nicer", "fresh", "freshen", "home", "house", "flat", "bedroom")),
        entry("gutters",
              (("gutter", "gutters", "downpipe", "downpipes", "fascia"),
               ("clean", "cleaning", "blocked", "overflowing", "often", "leaves", "sagging", "drip")),
              "Twice a year, after the leaves fall and again in spring: scooped out by hand in gloves "
              "from a stable ladder, with the rubbish into a bag rather than down the drain. Then flush "
              "each downpipe with a hose to check it runs. If water still spills over the edge on a wet "
              "day, the run of the gutter has dropped or the downpipe is blocked at the bottom, not the top.",
              avoid=("buy", "cost", "install", "replace", "quote")),
        entry("gutter-leak",
              (("gutter", "gutters", "downpipe", "downpipes", "fascia"),
               ("leak", "leaks", "leaky", "leaking", "drip", "dripping", "drips", "joint", "joints",
                "seal", "sealing", "sealant", "hole", "holes", "crack", "cracked", "fix", "repair",
                "water", "waterfall", "pouring")),
              "A leak is nearly always a joint or a hole, and it is a dry-day job: a leaking joint at "
              "the stop end or between two lengths is cleaned out, dried and sealed with gutter "
              "sealant; a hole or crack is covered with a self-adhesive flashing strip pressed on "
              "over a clean, dry surface, which lasts a few years. Before any of that, check the "
              "downpipe is not blocked - water backing up finds the weakest joint and pours out "
              "there - and re-clip a run that has sagged so it falls towards the downpipe, about "
              "1cm in 3 metres. Never do it off a ladder in the wind or on your own: a ladder on "
              "wet ground is the fall that puts people in hospital.",
              avoid=("clean", "cleaning", "clear", "clear out", "scoop", "leaves", "blocked",
                     "overflowing", "cost", "costs", "price", "quote", "install", "replace",
                     "new gutters")),
        entry("fence-repair",
              (("fence is falling down", "fence has fallen down", "fence fell down", "fence blew down",
                "fence has blown down", "fence panel", "fence panels", "broken fence",
                "fence is broken", "fence is leaning", "wobbly fence", "fence is wobbly",
                "fence post", "fence posts", "post has rotted", "posts have rotted",
                "fence is sagging", "fence sagging", "fence has sagged",
                "gate is hanging", "gate has dropped"),
               ("fence", "garden", "wind", "storm", "repair", "fix", "replace", "rotten", "rotted",
                "concrete", "blown", "fell", "leaning", "gate", "put back", "again")),
              "A panel that came out in the wind is usually a post that has moved, not the panel, so "
              "check the posts are upright with a spirit level before you fix it back: a new panel on "
              "a rotten post goes over again. Replace a rotted post base with a concrete repair spur, "
              "or set a new post 600mm into the ground in Postcrete, and brace it until it is solid.",
              avoid=("cost", "quote", "how much", "neighbour", "neighbor", "who owns", "boundary",
                     "fence paint", "paint it", "stain", "creosote",
                     "deep", "depth", "deep enough", "foot down", "feet down")),
        entry("fence-post-depth",
              (("how deep", "deep enough", "deep should", "deep do", "deep to", "deep for",
                "depth", "how far down", "how far in", "foot down", "feet down", "two foot",
                "2 foot", "two feet", "2 feet", "three foot", "3 foot", "three feet",
                "buried", "in the ground", "into the ground", "how much of"),
               ("fence post", "fence posts", "gate post", "gatepost", "pergola post",
                "deck post", "deck posts", "posts", "post", "fence", "fencing", "pergola")),
              "About a third of the post in the ground: 600mm (two foot) under a standard 1.8m panel, "
              "and 750 to 900mm on an exposed, windy corner or in sandy soil. Two foot is enough if "
              "the hole is about 250 to 300mm across and set in Postcrete or a 3:1 ballast and cement "
              "mix, with the concrete sloping away from the post so water runs off - check it plumb "
              "before the mix goes off, because a post only 300 to 400mm down leans within a winter.",
              ask=("how deep", "deep enough", "deep should", "deep do", "deep to", "deep for",
                   "depth", "how far down", "how far in", "foot down", "feet down", "buried",
                   "in the ground", "into the ground", "how much of"),
              bias=1,
              avoid=NOT_A_FENCE_JOB + (
                     "post office", "post a letter", "parcel", "delivery", "mail",
                     "letter", "blog", "job", "position", "apply", "applying", "instagram",
                     "facebook", "comment", "review", "how tall", "how high", "planning",
                     "max height", "boundary", "who owns", "whose", "who pays", "my neighbour",
                     "my neighbor", "cost", "costs", "price", "prices", "quote", "cheapest",
                     "treat", "treating", "stain", "staining", "paint", "painting",
                     "preserver", "creosote", "blew down", "blown down", "fell down",
                     "repair", "replace", "rotten", "rotted", "wobbly", "loose", "leaning",
                     "hanging", "plant", "plants", "bulb", "bulbs", "seed", "seeds",
                     "grave", "graves", "coffin", "ashes",
                     "the tip", "to the tip", "tip run", "rubbish", "skip", "landfill", "dispose",
                     "disposing", "instead of", "dumping", "get rid")),
        entry("fence-post-set",
              (("set a fence post", "set the post", "set a post", "set a new post",
                "set", "setting", "put up", "putting up", "install", "installing", "erect",
                "erecting", "fit", "fitting", "concrete", "concreting", "concreted",
                "concrete a fence post", "concrete it in", "concrete the post",
                "postcrete", "cement", "dig", "digging", "hole", "gravel", "ballast",
                "put gravel", "gravel in the bottom", "gravel in the hole", "bottom of the hole",
                "plumb", "straight", "level", "brace", "bracing", "how many bags",
                "how much postcrete", "how much concrete", "help it stand"),
               ("fence post", "fence posts", "gate post", "gatepost", "deck post", "posts",
                "post", "fence", "fencing", "panel", "panels")),
              "Dig the hole 250 to 300mm across and two foot (600mm) deep, stand the post on about "
              "50mm of gravel so the cut end never sits in water, and get it plumb on two faces with "
              "a spirit level before anything goes in. One 20kg bag of Postcrete does one post: pour "
              "it dry around the post, water it as the bag says, brace the post and leave it a day "
              "before a panel goes on. A 100mm square or 75mm round post is right for a 1.8m panel; "
              "in soft soil, or on a windy corner, go deeper rather than wider.",
              bias=1,
              avoid=NOT_A_FENCE_JOB + (
                     "post office", "post a letter", "parcel", "delivery", "mail", "letter",
                     "blog", "job", "position", "apply", "applying", "instagram", "facebook",
                     "neighbour", "neighbor", "next door",
                     "lamp post", "lamppost", "lamp", "post box", "postbox", "goal post",
                     "goalpost", "sign post", "signpost", "postcard", "postcard", "postcode",
                     "post code", "carrier", "courier",
                     "comment", "review", "how tall", "how high", "planning", "boundary",
                     "metres high", "metre high", "metres tall", "metre tall", "feet high",
                     "foot high", "2 metres", "2m high", "six foot", "height limit",
                     "who owns", "whose", "who pays", "my neighbour", "my neighbor", "cost",
                     "costs", "price", "prices", "quote", "cheapest", "treat", "treating",
                     "stain", "staining", "paint", "painting", "preserver", "creosote",
                     "blew down", "blown down", "fell down", "repair", "replace", "rotten",
                     "rotted", "rot", "rotting", "wobbly", "loose", "leaning", "sagging",
                     "plant", "plants", "bulb", "bulbs", "ashes",
                     "the tip", "to the tip", "rubbish", "skip", "instead of", "get rid",
                     "how far apart", "spacing", "spaced", "centres", "centers",
                     "how deep", "depth", "deep enough", "foot down", "feet down")),
        entry("fence-post-spacing",
              (("how far apart", "how far between", "spacing", "spaced", "centres", "centers",
                "distance between", "how many posts", "how many panels", "how wide"),
               ("fence post", "fence posts", "posts", "post", "fence", "fencing", "panel",
                "panels", "gate post", "gate")),
              "Fence posts go 1.8m apart, centre to centre, for a standard 1.8m (6ft) panel, and 2.4m "
              "for a 2.4m panel - a gravel board and a panel are sold to that width, so measure the "
              "panel before you dig. On a slope, keep the tops level and let the bottom of each panel "
              "follow the ground, stepped one post at a time rather than raked.",
              bias=1,
              avoid=NOT_A_FENCE_JOB + (
                     "post office", "post a letter", "parcel", "delivery", "mail", "letter",
                     "lamp post", "lamppost", "lamp", "post box", "postbox", "goal post",
                     "goalpost", "sign post", "signpost", "postcard", "postcode", "post code",
                     "blog", "job", "position", "apply", "cost", "costs", "price", "quote",
                     "treat", "treating", "stain", "paint", "painting", "how tall", "how high",
                     "planning", "boundary", "who owns", "whose", "how deep", "depth",
                     "deep enough", "how far down", "buried", "in the ground", "repair",
                     "replace", "rotten", "rotted", "wobbly", "loose", "leaning")),
        entry("fence-post-size",
              (("how thick", "how big", "what size", "which size", "what width", "how wide",
                "whats the best fence post", "best fence post", "best post", "what post",
                "which post", "what sort of post", "what kind of post", "what timber",
                "4 inch", "four inch", "3 inch", "three inch", "100mm", "75mm", "125mm",
                "square or round", "round or square", "concrete or wooden post"),
               ("fence post", "fence posts", "gate post", "gatepost", "deck post", "posts",
                "post", "fence", "fencing", "panel", "panels", "gate")),
              "A 100mm (4 inch) square post carries a 1.8m panel, and 75mm round is enough for a "
              "light closeboard fence; a gate wants a 125 to 150mm post of its own, not a panel post "
              "with a gate hung on it. Buy posts marked for ground contact (UC4) rather than plain "
              "treated timber, because a post rots at the soil line, and on an exposed corner a "
              "concrete post outlasts wood.",
              bias=1,
              avoid=NOT_A_FENCE_JOB + (
                     "post office", "post a letter", "parcel", "delivery", "mail", "letter",
                     "lamp post", "lamppost", "lamp", "post box", "postbox", "goal post",
                     "goalpost", "sign post", "signpost", "postcard", "postcode", "post code",
                     "blog", "job", "position", "apply", "applying", "cost", "costs", "price",
                     "prices", "quote", "how many do i need", "how far apart", "spacing",
                     "how deep", "depth", "deep enough", "how far down", "buried",
                     "in the ground", "dig", "digging", "hole", "concrete in", "postcrete",
                     "repair", "replace", "fix", "rotten", "rotted", "wobbly", "loose",
                     "leaning", "blew", "blown", "fell", "fallen", "treat", "treating",
                     "stain", "paint", "painting", "how tall", "how high", "planning",
                     "boundary", "who owns", "whose", "my neighbour", "my neighbor")),
        entry("fence-paint",
              (("fence", "fences", "fence panels", "shed", "garden gate"),
               ("paint", "painting", "paint it", "stain", "staining", "treat", "treating",
                "treatment", "creosote", "preserver", "preservative", "protect", "weatherproof")),
              "Clean it and let it dry: paint on a dirty or damp fence flakes within a year. Brush or "
              "spray a water-based fence stain rather than a film-forming paint, two coats on a dry day "
              "above 10C, keeping the bottom of the panel clear of the soil. A shed wants an oil or "
              "wood preserver, not a fence stain.",
              avoid=("neighbour", "neighbor", "boundary", "cost", "how much", "blew down", "rotted",
                     "fallen", "leaning", "replace")),
        entry("fence-windproof",
              (("stop my fence blowing down", "fence keeps blowing down", "fence blowing down again",
                "blown down every", "windproof", "wind proof", "keep the fence up"),
               ("fence", "fences", "garden", "wind", "storm", "gale", "again", "strong")),
              "A solid fence is a sail, so the wind pulls on the posts rather than passing through: "
              "slatted panels, or a gap under the gravel board, let it through. Set the posts 600mm "
              "into the ground in concrete, keep the panel out of the soil, and brace the end posts. A "
              "trellis strip along the top takes most of the load off a windy corner."),
        entry("patio-slab-loose",
              (("patio slab", "patio slabs", "paving slab", "paving slabs", "slab", "slabs",
                "paving", "patio", "paving stones"),
               ("loose", "wobble", "wobbles", "wobbly", "rocking", "rocks", "sunken", "sunk",
                "cracked", "moved", "lift", "relay", "re-lay", "dip", "uneven")),
              "Lift the slab, scrape off the old bedding and re-bed it on 30 to 40mm of 5:1 sharp sand "
              "and cement, tapping it level with its neighbours with a rubber mallet and checking with "
              "a straight edge. A slab that rocks after rain is usually a hollow bed or ants. Point the "
              "joints with dry sand and cement, not soil, and leave it a day."),
        entry("bricklaying-mortar",
              (("mortar", "mortar mix", "sand and cement", "building sand and cement",
                "cement", "cement mix", "cement and sand", "what mix", "what ratio", "mix ratio",
                "mix do i use", "mix should i use", "how much sand", "how much cement",
                "how many bags of sand", "how many bags of cement", "bags of sand",
                "bags of cement", "5 to 1", "5:1", "4 to 1", "4:1"),
               ("brick", "bricks", "bricklaying", "brickwork", "block", "blocks", "blockwork",
                "breeze block", "breezeblock", "cinder block", "wall", "walls", "garden wall",
                "render", "rendering", "pointing", "repointing", "re-point", "point the",
                "screed", "floor", "slab of concrete", "concrete base", "footing", "footings")),
              "Bricklaying mortar is 5:1 building sand to cement, or 4:1 for a wall that takes the "
              "weather, mixed soft and buttery rather than wet. A 25kg bag of cement with five bags of "
              "building sand lays roughly 150 bricks or 40 blocks, so measure the wall first - a 10m "
              "single-skin wall 1m high is about 600 bricks. Pointing and rendering are both a 4:1 "
              "mix, and a footing or a small concrete base is 6 parts ballast to 1 of cement.",
              avoid=("cost", "costs", "price", "prices", "cheap", "cheapest", "expensive",
                     "how much is", "how much does", "how much would", "quote", "quotes",
                     "which", "what type", "what sort", "best type", "what colour", "what color",
                     "how many bricks", "how many blocks", "many square metres",
                     "how do i lay", "how to lay", "clean", "cleaner", "stain", "stains",
                     "algae", "moss", "seal", "sealer", "paint", "render crack", "cracked",
                     "patio", "paving", "paving slab", "paving slabs", "flag", "flags",
                     "flagstone", "flagstones", "setts", "joints", "paving joints",
                     "mixer", "hire", "borrow", "wheelbarrow", "shovel", "board",
                     "how long", "how deep", "how thick", "depth", "thickness", "cure", "dry",
                     "damp", "damp proof", "insulation", "cavity", "lintel", "planning",
                     "get off", "getting off", "off a", "off the", "off my", "off bricks",
                     "off the wall", "off walls", "remove", "removing", "removal", "scrub",
                     "scrubbing", "pressure washer", "jet wash", "stubborn"),
              bias=1),
        entry("block-paving-bed",
              (("block paving", "block paved", "block paver", "block pavers", "paving blocks",
                "driveway blocks", "setts", "block paving drive", "paved drive", "paving the drive"),
               ("sand", "cement", "mortar", "mix", "much", "need", "how much", "how many",
                "bed", "bedding", "joint", "joints", "brush in", "kiln dried", "kiln-dried",
                "how deep", "depth", "wacker", "compact")),
              "Blocks are not bedded on sand and cement: they go down on 30 to 40mm of sharp sand "
              "alone, compacted with a wacker plate, and the joints are brushed full of kiln-dried "
              "sand afterwards, so there is no cement to measure at all. For 20 square metres "
              "reckon on about a tonne of sharp sand for the bed and two or three 25kg bags of "
              "kiln-dried sand for the joints, plus an edge restraint on every open side, which is "
              "the part that stops the blocks spreading.",
              avoid=("cost", "costs", "price", "prices", "cheap", "cheapest", "expensive",
                     "how much is", "how much does", "how much would", "quote", "quotes",
                     "which", "what type", "what sort", "best type", "what colour", "what color",
                     "how do i lay", "how to lay", "laying", "lay the blocks", "do i lay",
                     "clean", "cleaner", "stain", "stains", "algae", "moss", "weeds", "weed",
                     "seal", "sealer", "slippery", "oil", "paint", "get off", "getting off",
                     "off a", "off the", "off my", "remove", "removing", "removal", "scrub",
                     "patio slab", "paving slab", "paving slabs", "flag", "flags", "flagstone",
                     "wall", "walls", "brick", "bricks", "brickwork", "render", "rendering",
                     "screed", "floor", "concrete base", "footing", "footings", "mixer", "hire"),
              bias=3),
        entry("too-much-rubbish",
              (("bin", "bins", "rubbish", "trash", "garbage", "wheelie", "wheelie bin", "bin bag",
                "bin bags", "recycling", "waste"),
               ("always", "overflowing", "overfull", "too much", "every week", "each week", "full",
                "loads", "so much", "less", "reduce", "cut down", "keep filling")),
              "Most of it is air and packaging: flatten cartons, crush cans and squash bottles with the "
              "lid off, and the same bag holds twice as much. Put a smaller bin by the counter and take "
              "it out every night rather than waiting for the big one to fill, and keep a caddy beside "
              "it for peelings, which is often a third of the weight. Then buy the biggest pack you will "
              "actually use, loose veg instead of trays, and one refill bottle instead of a new one. If "
              "the wheelie bin is full by day five, half of what is in it belongs in the recycling.",
              avoid=("smell", "smells", "smelly", "stink", "stinks", "bin day", "collection",
                     "collected", "council", "where do i take", "tip",
                     "dump", "neighbour", "neighbor", "next door", "compost", "garden", "food caddy",
                     "seagull", "fox", "rat", "mouse", "mice", "broke", "broken", "lid", "lock",
                     "when is", "what day",
                     "money", "wages", "cash", "salary", "payday", "food", "groceries",
                     "time", "water", "electricity", "energy", "gas", "fuel", "petrol",
                     "paint", "wood", "ink", "data", "battery", "heat")),
        entry("empty-the-kitchen-bin",
              (("bin", "bins", "wheelie bin", "kitchen bin", "bin bag", "bin bags", "bin liner",
                "rubbish", "trash"),
               ("empty", "emptied", "emptying", "needs emptying", "need emptying",
                "needs taking out", "need taking out", "wants taking out", "clear", "clearing",
                "cleared", "empty it")),
              "Tie the bag at the top and take it straight out to the wheelie bin: a tied bag left "
              "by the door still smells, and the bin is what wants emptying, not the kitchen. While "
              "it is empty, wipe the inside with hot soapy water and a splash of bleach, let it dry, "
              "then fit the liner before anything goes back in - that once-a-week wipe is what keeps "
              "the flies off in summer. A bag that split on the way out wants a rinse in the garden "
              "rather than a scrub, and the wheelie bin gets the same wash twice a year.",
              guard=lambda read: not the_bin_is_on_a_machine(read),
              avoid=("row", "rows", "argument", "argue", "arguing", "flatmate", "housemate",
                     "landlord", "neighbour", "neighbors", "council", "collected", "collection",
                     "missed", "write", "letter", "report", "small bin", "tiny", "too small",
                     "put the bins out", "put the bin out", "put them out", "put it out",
                     "i emptied", "ive emptied", "i took the", "ive taken", "already emptied",
                     "already done", "did it")),
        entry("boiler-service-duration",
              (("boiler", "boilers", "combi", "gas boiler"),
               ("how long", "how many hours", "how much time", "long does", "long will",
                "how long to", "length of")),
              "About an hour for a straightforward boiler, and up to ninety minutes if it is the "
              "first service in a while or the engineer has to check the flue and the safety "
              "devices. It is a set of checks rather than a strip-down: they run the boiler, test "
              "the flue and the gas pressure, clean what they can reach, and leave you the service "
              "record. Book it for late summer if you can, because the wait is longer once the cold "
              "weather starts.",
              avoid=("cost", "price", "much", "worth", "worthwhile", "often", "annual", "yearly",
                     "new", "install", "installation", "replace", "fit", "fits", "fitted",
                     "fitting", "life", "lifespan", "good for",
                     "how many years", "years", "bleed", "pressure", "broken", "fault",
                     "repair", "repairs", "repairing", "fix", "fixes", "fixing",
                     "noise", "noisy", "banging", "rumbling", "knocking", "whistling", "hissing",
                     "leak", "leaks", "leaking", "hot water", "not heating")
              + A_AGE_OWNED,
              ask=("service", "services", "serviced", "servicing"),
              bias=3),

        entry("boiler-service",
              ("boiler", ("service", "servicing", "serviced", "annual", "yearly", "every year",
                          "certificate", "cost", "much", "price", "landlord")),
              "Once a year, yes: a gas boiler service is usually \u00a360 to \u00a3120 depending on "
              "where you are. It keeps the warranty valid, catches a failing part before it strands "
              "you in winter, and landlords are legally required to have one. Book it in late "
              "summer, when engineers are quiet and the price is lower.",
              avoid=("new", "install", "installation", "replace", "replacement", "buy"),
              ask=("service", "servicing", "serviced", "annual", "yearly", "certificate", "cost",
                   "much", "price", "often")),

        entry("boiler-service-diy",
              (("boiler", "boilers", "combi", "gas boiler"),
               BOILER_DIY + ("can i service", "service my own", "service it myself",
                             "service the boiler myself", "legal to service")),
              ("Not the service itself: it means opening the case and checking the gas side, and "
               "a gas boiler is Gas Safe work by law, so the annual service is an engineer's job "
               "at about \u00a360 to \u00a3120. Yours is the bit around it: keep the pressure "
               "at 1 to 1.5 bar, keep the flue and the vents clear, bleed the radiators - and the "
               "warranty usually needs the engineer's service anyway."),
              avoid=("new boiler", "install", "buy"),
              bias=4,
              ask=BOILER_DIY + ("service", "servicing", "serviced", "annual", "yearly"),
              guard=_an_ask_about_servicing_my_own),

        entry("damage-deduction",
              (("stain", "stains", "stained", "mark", "marks", "damage", "damaged", "scuff", "scuffs",
                "burn", "burns", "chip", "chips"),
               ("letting agent", "landlord", "landlords", "deduct", "deducted", "deducting", "deduction",
                "deductions", "withheld", "withhold", "withholding", "wear and tear", "deposit",
                "refund", "end of tenancy")),
              ("Ask in writing for an itemised list of what was taken and why, and say which deductions "
               "you disagree with. Fair wear and tear - a carpet going thin where you walk, a worktop "
               "faded by sunlight - is not chargeable; a burn or a paint mark is. If the deposit went "
               "into a protection scheme, use its free dispute service rather than arguing with the "
               "agent, and keep the photos from the day you moved in."),
              bias=1),

        entry("deposit-back", (("deposit", "deposits", "deposit scheme", "tenancy deposit",
                                "holding deposit", "security deposit", "damage deposit",
                                "deposit protection", "deposit protection scheme"),
                               ("back", "returned", "return", "not", "unfair", "withheld", "landlord",
                                "landlords", "claim", "getting", "move out", "moved out",
                                "moving out", "end of tenancy", "tenancy", "renting", "rented",
                                "letting agent", "deductions", "deducted", "deducting",
                                "money", "money back", "get it", "how do i get")),
              ("Ask in writing for an itemised list of what was taken and why, and say which of the "
               "deductions you disagree with. If your deposit was in a protection scheme, use its free "
               "dispute service rather than arguing with the landlord; you can also raise it with the "
               "council. Photos from the day you moved in are the evidence that wins this."),
              avoid=("flat", "house", "saving", "save", "rent", "buy", "first home",
                     "says i owe", "they say i owe", "say i owe", "owe money", "i owe"),
              bias=3),

        entry("washing-machine-size",
              (("washing machine", "washer", "washer dryer", "tumble dryer", "dryer", "drum",
                "drum size",
                "7kg", "8kg", "9kg", "10kg", "11kg", "12kg"),
               ("size", "sizes", "sized", "capacity", "kg", "kgs", "kilo", "kilos", "kilogram",
                "kilograms", "litre", "litres", "liter", "liters", "big", "bigger", "biggest",
                "big enough", "how big", "what size", "how many kg", "how much can", "enough",
                "or 7kg", "or 8kg", "or 9kg", "or 10kg", "or 11kg", "or 12kg")),
              "Roughly: 7kg for one or two people, 8kg for three, 9kg for four and 10 to 12kg if you "
              "wash duvets and bedding in it. The figure is the dry weight of a full load, so a 9kg "
              "drum is not gentler, it just holds more; a bigger one costs more to run per wash but "
              "you run it less often. Measure the gap and the doorway first, because depth is what "
              "usually rules a machine out, and match the dryer to the washer or slightly bigger "
              "than it.",
              avoid=("wont spin", "won't spin", "not spinning", "no spin", "wont turn", "won't turn",
                     "spin cycle", "soaking", "soaking wet", "still wet", "dripping", "wringing",
                     "wont drain", "won't drain", "packed in", "broke", "broken", "faulty",
                     "leaking", "smell", "smells", "smelly", "noise", "noisy", "banging", "hot",
                     "overheating", "not heating", "wont heat", "won't heat", "wont start",
                     "won't start", "error", "door", "locked", "buy", "buying", "worth it",
                     "cheap", "cheapest", "best", "which one", "recommend",
                     "turkey", "chicken", "lamb", "beef", "pork", "joint", "roast", "compost",
                     "potatoes", "spuds", "dumbbell", "dumbbells", "barbell", "weights",
                     "suitcase", "luggage", "package", "parcel", "barbecue", "bbq"),
              guard=_not_a_washer_of_another_kind),
        entry("deposit-return-days",
              (("deposit", "tenancy deposit", "deposit scheme", "protection scheme",
                "deposit protection"),
               ("how long", "how many days", "how many weeks", "how soon", "take", "takes",
                "wait", "waiting", "when")),
              ("Ten days is the rule: the deposit has to come back within ten days of the day you "
               "and the landlord agree the amount, and interest can come with it. If you have not "
               "agreed, the landlord has to return the undisputed part within those ten days and "
               "put in a claim for the rest, and a disputed amount goes to the protection scheme, "
               "whose free dispute service usually decides within 28 days. So ask the scheme which "
               "one holds your money, and chase the agent in writing, because the deadline is "
               "counted from the agreement and not from the day you moved out."),
              bias=2,
              guard=_a_deposit_coming_back,
              avoid=("save", "saving", "savings", "put away", "towards", "a month",
                     "each month", "per month", "afford", "first home", "first time",
                     "house", "flat", "moving", "move", "mortgage", "buy", "rent",
                     "renting", "damage", "damaged", "unfair", "withheld", "deduct",
                     "deductions", "cleaning", "checkout", "inspection")),

        entry("washing-machine-spin",
              (("washing machine", "washer", "washer dryer",
                "clothes", "washing", "wash load", "laundry"),
               ("wont spin", "won't spin", "not spinning", "no spin", "wont turn", "won't turn",
                "isnt spinning", "isn t spinning", "aint spinning", "isnt turning",
                "isn t turning", "isnt going round", "drum isnt turning", "drum not turning",
                "drum", "spin cycle", "spin only", "to spin", "get it to spin",
                "clothes are wet", "clothes come out wet", "soaking", "soaking wet",
                "wringing wet", "wringing", "still wet after", "still wet when", "sopping",
                "sopping wet",
                "dripping wet", "come out wet", "comes out wet", "come out soaking",
                "comes out soaking", "come out dripping", "comes out dripping", "come out wringing",
                "comes out wringing", "wet after the wash", "wet after a wash",
                "wet after washing", "wet after wash", "come out still wet",
                "comes out still wet", "leaves the clothes wet", "leaves clothes wet",
                "leaves them wet", "leaves it wet",
                "leaving the clothes", "leaving clothes", "leaving them", "leaving it",
                "leaving my clothes", "left the clothes", "left clothes",
                )),
              "One heavy thing is the usual cause: a duvet or a bath mat balls up on one side and the "
              "machine refuses to spin, so shake it flat and run a spin only cycle. Still soaked? Clear "
              "the filter behind the kick plate, because a machine that can't drain won't spin. On an "
              "older machine the belt can slip off, which is a cheap part.",
              avoid=("buy", "which", "best", "door", "doors", "locked", "lock", "wont open",
                     "size", "sizes", "sized", "drum size", "capacity", "kg", "kgs", "kilo",
                     "kilos", "kilogram", "kilograms", "litre", "litres", "liter", "liters",
                     "big", "bigger", "biggest", "big enough", "how big", "how many kg",
                     "7kg", "8kg", "9kg", "10kg", "11kg", "12kg", "how much can",
                     "won't open", "smell", "smells", "smelly", "musty", "leak", "leaking",
                     "noise", "noisy", "loud", "squeak", "squeaks", "squeaking", "squeal",
                     "squeals", "squealing", "grind", "grinds", "grinding", "bang", "bangs",
                     "banging", "rattle", "rattles", "rattling", "knock", "knocks", "knocking",
                     "whine", "whining",
                     "rain", "rained", "raining", "rainy", "weather", "storm", "puddle", "puddles",
                     "leak", "leaks", "leaking", "wet room", "wet wipes", "wet wipe",
                     "marks", "mark", "stains", "stain", "black marks", "dark marks", "streaks",
                     "hot", "warm", "overheating", "overheated", "burning",
                     "smell of burning",
                     "sitting", "standing", "sitting water", "standing water", "water sitting",
                     "water standing", "wont drain", "won't drain", "not draining", "didnt drain",
                     "didn't drain", "wont empty", "won't empty", "not emptying"),
              bias=2),

        entry("hob-scratch",
              (("hob", "hobs", "ceramic hob", "induction hob", "cooker top", "cooker plate",
                "hotplate", "electric hob", "gas hob"),
               ("scratch", "scratches", "scratched", "scuff", "scuffs", "scuffed", "gouge",
                "gouged", "chipped", "chip")),
              ("Nine times in ten the mark that looks like a scratch is metal, sugar or limescale "
               "burnt onto the glass: scrape the cold hob with a hob scraper held almost flat, then "
               "rub ceramic hob cleaner over it with a cloth, and it comes away. A real scratch - "
               "you feel it catch a fingernail - cannot be polished out of a glass top, so a fine "
               "one is something to live with and a deep one means a new top, which on a built-in "
               "hob is often most of the price of a new one. Never use an abrasive powder or a "
               "scouring pad; they make more of them."),
              avoid=("floor", "floors", "wood", "laminate", "worktop", "worktops", "table",
                     "tables", "furniture", "desk", "door", "doors", "car", "cars", "van",
                     "windscreen", "screen", "phone", "mobile", "glasses", "spectacles", "watch",
                     "bath", "bathroom", "sink", "shower", "wall", "walls", "paint", "painted",
                     "leather", "sofa", "shoe", "shoes", "boot", "boots", "cd", "dvd", "vinyl",
                     "record", "records", "lens", "camera", "clean", "cleaning", "grease",
                     "burnt on", "burnt", "burned", "burning", "baked on", "limescale",
                     "buy", "best", "which", "worth", "cost", "price", "cheap", "cheapest")),
        entry("hob-ring-price",
              (("hob ring", "hob rings", "ring", "rings", "burner", "burners", "burner cap",
                "solid plate", "hotplate", "element", "cooker ring", "gas ring"),
               ("cost", "costs", "much", "price", "prices", "buy", "replace", "replacement", "new",
                "cheap", "cheapest", "spare", "spares", "part", "parts", "fit")),
              ("About £10 to £25 for a solid plate or a gas burner cap, and £25 to £50 for an "
               "induction zone's part, so it is worth fixing rather than replacing the cooker. Buy "
               "by the cooker's model number rather than by eye - the same size ring is not always "
               "the same fitting. An electric one is usually two screws and a spade connector; a "
               "gas ring has to be fitted by a Gas Safe engineer."),
              bias=1,
              avoid=("clean", "cleaning", "grease", "stain", "stains", "scrub", "phone", "mobile",
                     "ringtone", "engagement", "wedding", "gold", "silver", "diamond", "jewellery",
                     "spend", "spent", "spending", "budget", "afford", "salary", "propose",
                     "proposal", "carat",
                     "what ring", "which ring", "ring should", "rings should", "pick a ring",
                     "rings cost", "ring cost", "much do rings", "much are rings", "ring prices",
                     "choose a ring", "ring shopping", "wear", "wearing", "worn", "rings to wear",
                     "necklace", "earring", "bracelet", "tarnish", "finger", "ear", "ears",
                     "wood burner", "woodburner", "wood burning", "woodburning", "log burner",
                     "logburner", "multi fuel", "multifuel", "stove", "stoves", "chimney",
                     "flue", "fireplace", "solid fuel",
                     "bath", "bathtub", "sink", "onion", "calamari", "pineapple", "doorbell",
                     "door bell", "curtain", "smoke", "ow", "hurt", "swollen", "sting")),
        entry("fitting-a-wood-burner",
              (("wood burner", "woodburner", "wood burning", "woodburning", "wood stove",
                "log burner", "logburner", "log burning", "multi fuel", "multifuel",
                "solid fuel", "stove", "stoves", "fireplace", "flue", "chimney"),
               ("fit", "fits", "fitting", "fitted", "install", "installing", "installation",
                "put in", "putting in", "need", "needed", "regulations", "regs",
                "regulation", "building control", "hetas", "legal", "allowed", "sign off",
                "hearth", "clearance", "distance", "ventilation", "liner", "lining", "line it",
                "what size", "how big", "position", "where can i put", "too close")),
              ("Get it signed off rather than doing the flue yourself: a Hetas-registered installer, "
               "or a fitter whose work building control inspects, is what the regs ask for, and an "
               "unsigned stove is a problem when you sell the house as well as a fire risk. Size "
               "the stove to the room - roughly 1kW for every 14 cubic metres, and no more, because "
               "a big stove turned right down smokes and soots the flue. It needs a non-combustible "
               "hearth (12mm of slate or stone is the usual, and 300mm in front of the door), the "
               "flue swept and lined if the chimney is old, and a carbon monoxide alarm in the same "
               "room, which the law has required for a solid-fuel stove since 2022. In a smoke "
               "control area the stove must be DEFRA-exempt, so check that before you buy it."),
              avoid=("how much", "much does", "much is", "cost", "costs", "price", "prices",
                     "cheap", "cheapest", "expensive", "worth it", "save", "saving", "savings",
                     "bill", "quote", "budget",
                     "clean", "cleaning", "cleaner", "glass", "soot", "sooty", "smoke", "smoky",
                     "dirty", "sweep", "sweeping", "swept", "paint", "painting", "repaint",
                     "rust", "rusty", "not drawing", "wont light", "won't light", "keeps going out",
                     "light", "lighting", "light it", "banging", "bang", "noise", "noisy",
                     "bird", "birds", "damper", "stop the", "smell"),
              bias=3),
        entry("hob-heat",
              (("hob", "hobs", "ring", "rings", "burner", "burners", "hotplate", "hotplates",
                "cooker plate", "cooker top", "induction", "ceramic hob", "gas ring", "gas hob",
                "electric hob", "solid plate"),
               ("slow", "slower", "slowly", "ages", "forever", "long", "longer", "takes", "taking",
                "heats", "heating", "heat up", "warms", "warming", "warm up", "not heating",
                "isnt heating", "isn't heating", "wont heat", "won't heat", "not hot", "cold",
                "not working", "doesnt work", "doesn't work", "stopped working", "stopped",
                "dead", "gone", "weak", "barely", "packed up", "stopped heating", "one ring",
                "wont light", "won't light", "wont ignite", "won't ignite", "wont spark",
                "won't spark", "not lighting", "doesnt light", "doesn't light", "clicks but",
                "no flame", "wont stay lit", "won't stay lit", "goes out", "keeps going out")),
              _hob_heat,
              avoid=("clean", "cleaning", "grease", "greasy", "burnt on", "stain", "stains", "scrub",
                     "gym", "gyms", "new job", "first day", "at work", "the office", "staff",
                     "orientation", "hospital", "ward", "antenatal", "new starter", "volunteer",
                     "shiny", "oven", "grill", "microwave", "kettle", "wood burner", "log burner",
                     "buy", "best", "which", "worth", "cost", "price", "cheap", "cheapest",
                     "how do i use", "setting", "simmer", "boil", "wok", "season", "seasoning",
                     "pressure cooker", "slow cooker", "air fryer", "boiler", "pilot",
                     "pilot light", "candle", "candles", "fire", "fireplace", "barbecue", "bbq",
                     "phone", "phones", "mobile", "mobiles", "ringtone", "voicemail", "landline",
                     "missed call", "missed calls",
                     "ear", "ears", "tinnitus", "hearing", "my ears", "in my ears", "in my ear",
                     "ringing in my ears", "ringing in the ears",
                     "gold", "silver", "jewellery", "jewelry", "necklace", "bracelet", "earring",
                     "earrings", "engagement ring", "wedding band", "diamond", "tarnish",
                     "tarnished", "green", "gone green", "finger green", "clean my ring",
                     "dull", "dulled", "polish", "polishing",
                     ) + RING_AS_A_CALL,
              bias=1, guard=_a_person_not_a_hob),
        entry("iron-fault",
              (("iron", "irons", "steam iron", "steam generator", "soleplate"),
               ("spits", "spitting", "spit", "spat", "spits out", "spitting out", "spitting water",
                "drips", "dripping", "drips water", "leaks", "leaking", "leaky", "water",
                "wet patches", "wet patch", "marks", "white marks", "brown marks", "streaks",
                "spraying water", "sprays water", "water on the clothes", "damp clothes",
                "wont heat", "won't heat", "wont heat up", "won't heat up", "not heating",
                "isnt heating", "isn't heating", "no heat", "stopped heating", "cold", "dead",
                "wont get hot", "won't get hot", "not hot", "wont turn on", "won't turn on",
                "wont switch on", "won't switch on")),
              _iron_fault,
              avoid=("crease", "creases", "ironing board",
                     "scorch", "scorched", "burn", "burnt", "buy", "best", "which", "worth",
                     "cost", "price", "cheap", "travel iron", "hair", "hair straighteners",
                     "curling", "fabric", "shiny", "clothes are",
                     "cord", "plug", "fuse", "water tank", "limescale in the kettle"),
              bias=1),

        entry("dryer-not-heating",
              (("tumble dryer", "tumble drier", "dryer", "drier", "tumbler", "washer dryer"),
               ("not heating", "isnt heating", "isn't heating", "no heat", "wont heat", "won't heat",
                "heat up", "heating up", "cold", "takes ages", "takes forever", "not drying",
                "wont dry", "won't dry", "doesn't dry", "doesnt dry", "still wet", "still damp",
                "clothes are damp", "clothes are wet", "long time to dry",
                "two goes", "two cycles", "goes", "go", "cycles", "cycle", "come out damp",
                "comes out damp", "still damp after", "damp after", "takes two",
                "leaves the clothes damp", "leaves clothes damp", "leaves them damp",
                "clothes damp", "clothes still wet", "clothes are still wet",
                "taking ages", "taking so long", "takes so long", "taking hours", "takes hours",
                "taking three hours", "taking two hours", "taking a long time", "takes a long time",
                "hours to dry", "long to dry", "slow to dry", "drying slowly")),
    _dryer_heat,
              avoid=("buy", "which", "best", "worth", "cost", "cheap", "cheapest", "running",
                     "noise", "noisy", "loud", "squeak", "squeaks", "squeaking", "bang", "bangs",
                     "banging", "rattle", "rattles", "grind", "grinds", "grinding", "smell",
                     "smells", "smelly", "fire", "fires", "lint fire", "condensation", "mould",
                     "mold", "damp walls", "hair dryer", "hairdryer")),

        entry("dryer-smells",
              (("tumble dryer", "tumble drier", "dryer", "drier", "tumbler", "washer dryer",
                "heat pump dryer", "heat pump drier", "heat pump tumble dryer", "vented dryer",
                "condenser dryer"),
               ("smells", "smell", "smelly", "stinks", "stink", "stinking", "musty", "fusty",
                "damp smell", "damp", "mouldy", "moldy", "mildew", "sour", "whiff", "reek",
                "reeking", "pongs", "pong", "funky", "off smell", "smells off")),
              "Nearly always the fluff and the water: empty the fluff filter and wash it, pull the "
              "condenser out and rinse it under the tap if the machine has one, and tip out the "
              "water tank or check the drain hose. On a heat pump or condenser dryer the smell is "
              "usually the condenser left damp, so run a rinse cycle and leave the door and the "
              "drawer open afterwards. A vented dryer wants the vent hose cleared and the outside "
              "flap checked, and once a year wipe the drum and the seal with a hot damp cloth.",
              avoid=("burning", "burnt", "scorched", "singed", "smoking", "fire", "smells hot",
                     "smells really hot", "too hot", "oven", "kitchen", "room", "fridge",
                     "freezer", "washing machine", "dishwasher", "sink", "drain", "drains",
                     "bin", "bins", "cooker", "hob", "microwave", "hair dryer", "hairdryer",
                     "takes ages", "not drying", "still wet", "not heating", "not working",
                     "buy", "worth", "cost", "running")),

        entry("hair-dryer-not-hot",
              (("hair dryer", "hairdryer", "hair drier", "blow dryer", "blowdryer"),
               ("not heating", "isnt heating", "isn't heating", "not heating up", "no heat",
                "no heat coming out", "blowing cold", "blows cold", "cold air", "cold",
                "stopped heating", "wont heat", "won't heat", "wont heat up", "won't heat up",
                "not hot", "isnt hot", "isn't hot", "wont get hot", "won't get hot",
                "keeps cutting out", "cuts out", "cut out", "stopped working", "dead",
                "takes ages", "smells hot", "buzzing")),
              _hair_dryer,
              avoid=("buy", "buys", "buying", "best", "which", "worth", "cost", "price", "cheap",
                     "how long", "last", "lasts", "lasting", "curlers", "straighteners",
                     "straightener", "diffuser", "brush", "bristles", "dry my hair", "dry hair",
                     "hairdryer brush", "styling", "frizz", "curly", "curls")),

        entry("dryer-vent",
              (("tumble dryer", "tumble drier", "dryer", "drier", "tumbler", "washer dryer",
                "heat pump dryer", "heat pump drier", "heat pump tumble dryer", "vented dryer",
                "condenser dryer"),
               ("vent", "vents", "vented", "venting", "ventilation", "hose", "hoses", "duct",
                "ducting", "flue", "out of the window", "outdoors", "outside wall", "wall vent",
                "needs a vent", "need a vent", "need venting", "no vent", "without a vent",
                "tumble dryer vent", "dryer vent",
                "where does the water go", "where does the water", "water go",
                "water tank", "empty the water", "condenser water", "the water goes")),
              "A heat pump or condenser dryer needs no outside vent at all - the water goes into a "
              "tank you empty, or down a hose to the drain - so it can sit in a cupboard or a "
              "bedroom. Only a vented dryer needs the duct, and then it wants the hose out through "
              "a wall vent or an open window with no kinks and no crushed section behind the "
              "machine; a short straight run to outside is the whole job. Never duct one into a "
              "loft or a chimney: that puts the damp and the lint back into the house, and fluff "
              "round a hot duct is a fire.",
              avoid=("not heating", "isnt heating", "isn't heating", "not drying", "takes ages",
                     "still wet", "still damp", "smells", "smell", "burning", "fire", "sparks",
                     "wont turn", "won't turn", "not spinning", "cuts out", "stopped working",
                     "buy", "best", "which", "worth", "cost", "cheap", "running cost",
                     "hair dryer", "hairdryer", "condensation", "mould", "mold", "damp walls")),

        entry("dryer-smells-of-burning",
              (("tumble dryer", "tumble drier", "dryer", "drier", "tumbler", "washer dryer"),
               ("burning smell", "smells of burning", "smells like burning", "smell of burning",
                "smells burnt", "smells scorched", "smells singed", "smells hot", "burning",
                "scorching", "smoking")),
              "Stop it and unplug it, and do not run another load until you have looked: a dryer fire "
              "starts with lint round the heater or a vent hose full of fluff, and the smell is the "
              "warning. Empty the fluff filter and clear the hose. Still there after that? Get an "
              "engineer out, and never leave a dryer running while you are out.",
              avoid=("buy", "which", "best", "worth", "cost", "running", "noise", "noisy", "heating",
                     "not heating", "takes ages", "hair dryer", "hairdryer", "oven", "room", "kitchen",
                     "fridge", "freezer", "washing machine", "damp", "mould", "mold")),

        entry("dryer-drum-not-turning",
              (("tumble dryer", "tumble drier", "dryer", "drier", "tumbler", "washer dryer"),
               ("wont turn", "won't turn", "not turning", "isnt turning", "isn't turning",
                "drum isnt turning", "drum not turning", "drum wont turn", "drum not moving",
                "wont spin", "won't spin", "not spinning", "no spin", "drum dead")),
              "The belt has almost certainly slipped off or snapped: it is a rubber band round the drum "
              "and the motor pulley, a few pounds, reached through the back panel with a screwdriver. "
              "Turns by hand but not under power? Belt or door switch. Will not turn by hand either? "
              "Something is jammed or the bearings have gone, which usually means a new machine.",
              avoid=("buy", "which", "best", "worth", "cost", "cheap", "running", "noise",
                     "noisy", "loud", "squeak", "squeaks", "squeaking", "bang", "bangs",
                     "banging", "rattle", "rattles", "grind", "grinds", "grinding", "smell",
                     "smells", "smelly", "fire", "fires", "heating", "heat up", "not heating",
                     "takes ages", "still wet", "still damp", "hair dryer", "hairdryer")),

        entry("vacuum-suction",
              (("vacuum", "vacuum cleaner", "hoover", "henry", "dyson", "vax"),
               ("suction", "lost suction", "no suction", "not picking up", "wont pick up",
                "won't pick up", "not sucking", "weak", "blocked", "clogged", "full",
                "picking", "pick", "picked", "picks", "picking up", "pick up", "picks up",
                "unblock", "unblocking", "clearing", "bunged", "bunged up", "jammed", "stuck",
                "unclog", "unclogging", "clogging", "fix", "fixing", "stopped picking up")),
              "Follow the air path: take the hose off both ends and drop a coin through it, shake the bag "
              "or empty the bin, wash the filter (most are washable, and it has to be bone dry before it "
              "goes back) and cut the hair off the brush bar. A blocked hose, a full bag or a matted "
              "filter is the answer nearly every time, and all three are free to fix.",
              bias=2,
              avoid=("buy", "which", "best", "cheapest", "worth", "cordless",
                     "wont turn on", "won't turn on", "wont switch on", "wont start", "wont come on",
                     "no power", "dead", "fuse", "stopped dead", "smell", "burning",
                     "robot",
                     "choose", "choosing", "recommend", "recommendation", "shop", "shopping",
                     "help me pick", "pick a", "pick the", "picking a", "pick one", "pick out")),

        entry("toaster-one-side",
              (("toaster", "toast", "sandwich toaster"),
               ("one side", "one side only", "only one side", "one end", "uneven", "unevenly",
                "patchy", "halfway", "one half", "half cooked", "not browning")),
              "One side not browning means the element on that side has gone, or the wire that feeds "
              "it: unplug it, and if you look in while it is cold and one element never glows while "
              "the others do, that is the fault. On an ordinary toaster that is a new toaster, not a "
              "repair. If it browns at one END instead, the bread is sitting proud of the slots and "
              "the elements are fine.",
              avoid=("buy", "best", "which", "cheapest", "worth", "recipe", "recipes", "idea",
                     "ideas", "dinner", "lunch", "breakfast", "sandwich", "topping", "toppings")),

        entry("pilot-light",
              (("pilot light", "pilot", "pilot flame"),
               ("going out", "goes out", "gone out", "wont stay lit", "won't stay lit", "keeps going",
                "blows out", "not staying", "wont light", "won't light", "wont stay on",
                "won't stay on", "flame")),
              "Hold the knob in for twenty seconds after the flame catches, then let it go: a pilot that "
              "won't hold is nearly always the thermocouple, a small part a Gas Safe engineer swaps in "
              "ten minutes. A draught or a dirty jet does it too, and both mean taking the case off, so "
              "that is their job as well. If you smell gas, turn it off at the meter, open the windows "
              "and ring the gas emergency line on 0800 111 999.",
              avoid=("buy", "best", "cost", "price")),

        entry("fix-it-myself",
              (("myself", "my own", "diy", "have a go", "having a go", "have a bash",
                "give it a go", "giving it a go", "by myself", "on my own"),
               ("fix", "fixing", "fixed", "repair", "repairing", "mend", "mending", "install",
                "installing", "fit it", "fitting", "replace", "replacing", "unblock",
                "unblocking", "do it", "go at it", "at it", "sort it", "sort that",
                "take it apart", "take apart", "plumb", "plumbing",
                "wire", "wiring", "rewire", "rewiring", "electric", "electrics", "bleed", "service",
                "seal", "belt",
                "tap washer", "tap washers", "washer", "part")),
              _diy,
              ask=("can i", "can we", "could i", "should i", "should we", "shall i", "is it worth",
                   "worth", "easy", "easier", "hard", "difficult", "safe", "able to", "dare",
                   "do i need", "possible", "any point"),
              avoid=_DIY_AVOID,
              bias=2),

        entry("tradesperson-check",
              (("tradesperson", "tradesman", "plumber", "electrician", "builder", "roofer",
                "gas engineer", "handyman", "boiler engineer",
                "decorator", "decorators", "painter", "painters", "plasterer", "plasterers",
                "tiler", "tilers", "joiner", "joiners", "carpenter", "carpenters", "glazier",
                "locksmith", "gardener", "gardeners", "landscaper", "fencer", "chimney sweep",
                "roof tiler", "bricklayer",
                "company", "companies", "firm", "business", "supplier", "installer",
                "installation company", "contractor", "contractors", "man with a van",
                "removals", "tradesperson", "tradespeople"),
               ("check", "reputable", "trust", "trustworthy", "cowboy", "avoid", "rip off",
                "rip-off", "how do i know", "vet", "choose", "find a good", "insurance", "quote",
                "reliable", "careful", "decent", "honest", "find a", "find someone", "who can",
                "good one", "good company", "good firm", "pick a", "picking a",
                "spot a", "how do i spot", "how to spot", "spotting",
                "legit", "legitimate", "genuine", "registered", "look up", "look them up", "verify",
                "vetted", "references")),
              "Start with Companies House, which is free: search the name or the number on their quote "
              "and you can see whether the company exists, when it was formed and whether the "
              "registered address is a real place rather than a mail drop - a limited company has to "
              "put its number and registered address on its website and its invoices. Then the trade "
              "checks: a written quote rather than a verbal one, proof of insurance, and for gas, oil "
              "or electrical work the registration number you can check yourself on the Gas Safe, "
              "OFTEC or NICEIC register. A neighbour who has used them beats any review site, and pay "
              "by card rather than bank transfer so there is a chargeback if it goes wrong. Never pay "
              "the whole price up front - a deposit for materials is normal, the rest when it is done.",
              avoid=("cheap", "cheapest", "cost", "how much", "price", "hourly", "emergency",
                     "no hot water", "leak", "leaking", "broken",
                     "rip off", "ripped off", "ripping off", "overcharged", "refund",
                     "small claims", "trading standards", "botched", "bad job", "rubbish job",
                     "took my money", "never came back", "complain", "complaint", "guarantee",
                     "warranty", "rights", "did a runner",
                     "website", "websites", "online shop", "link", "click", "clicked", "login",
                     "password", "email", "text message", "phishing", "invoice for", "paypal",
                     "bank details", "account details")),

        entry("first-aid-kit",
              (("first aid kit", "first aid box", "first aid", "medical kit", "first-aid kit",
                "medicine cupboard", "medicine cabinet", "medicine box", "first aid supplies"),
               ("have", "need", "keep", "put", "got", "get", "buy", "stock", "include", "contents",
                "what", "at home", "for the car", "should")),
              ("A home kit is a box you can use one-handed in the dark: plasters in a few sizes, sterile "
               "gauze and tape, a crepe bandage, small scissors, tweezers, disposable gloves, a "
               "thermometer, and children's paracetamol with the dose worked out by weight. Add an ice "
               "pack, antiseptic cream and the 111 number, then check it once a year and replace "
               "anything past its date."),
              avoid=("burn", "burns", "burnt", "scald", "scalded", "cut", "cuts", "bleeding", "bled",
                     "nosebleed", "sprain", "sprained", "choking", "choked", "swallowed", "overdose",
                     "rash", "fever", "temperature", "allergic", "anaphylaxis", "seizure", "fit",
                     "course", "training", "certificate", "qualification")),

        entry("paint-smell-curing", (("paint", "painting", "repainted", "paintwork", "gloss", "emulsion",
                                "undercoat"),
                               ("smell", "smells", "smelling", "smelly", "smells of", "smelt",
                                "fumes", "fume", "stink", "stinks", "lingering")),
              "Keep the windows open and let it cure: water-based paint stops smelling within a day or "
              "two, and oil-based gloss takes a week or so to stop off-gassing. A bowl of water with a "
              "chopped onion in the room overnight, or a dish of bicarbonate of soda, takes the edge "
              "off. Don't mask it with candles. If it is still strong after a week, the paint may be "
              "old or the room under-ventilated.",
              bias=1,
              avoid=("tin", "tins", "leftover", "dispose", "bin", "recycle", "tip", "gas",
                     "carbon monoxide", "burning", "smoke")),
        entry("paint-tins",
              (("paint", "paint tin", "paint tins", "tins of paint", "paint pot", "paint pots",
                "leftover paint", "old paint",
                "drying out in the tin", "dries out in the tin", "dried out in the tin",
                "drying out in the can", "gone hard in the tin", "skinned over", "a skin on"),
               ("old", "leftover", "dispose", "get rid", "throw", "bin", "recycle", "the tip",
                "to the tip", "recycling centre", "tins", "pots", "half a tin", "dried out", "store",
                "keep", "what do i do")),
              "A tin of paint has to dry out before it can go anywhere. Stir sand, sawdust or cat "
              "litter into it, leave the lid off somewhere safe until it is hard, then take it to the "
              "household waste recycling centre, where nearly every site takes paint. To keep a "
              "part-used tin, wipe the rim, press the lid down with a block of wood and store it upside "
              "down so no skin forms. A few inches left is worth offering on Freecycle.",
              avoid=("wall", "walls", "ceiling", "woodwork", "paint the", "repaint", "colour",
                     "nail polish", "spray", "smell", "smells", "smelling", "smelly", "smells of",
                     "fumes", "fume", "stink", "stinks",
                     "drying too fast", "drying too quickly", "dries too fast", "dry too fast",
                     "from drying", "keeps drying", "before it dries", "going off the brush",
                     "wet edge", "open time", "workable")),

        entry("second-hand-washer",
              (("washing machine", "washer", "tumble dryer", "dishwasher"),
               ("second hand", "second-hand", "used", "refurbished", "reconditioned", "cheap",
                "cheaper", "fair price", "how much", "private sale", "facebook", "gumtree",
                "gum tree", "dealer", "nearly new")),
              _washer_price,
              avoid=("bleach", "mould", "mold", "mildew",
                     "fix", "repair", "broken", "leaking", "error", "wont spin", "won't spin",
                     "not draining", "smells", "install", "plumbing in")),
        entry("furniture-upstairs",
              (("wardrobe", "chest of drawers", "sideboard", "bookcase", "bookshelf", "sofa",
                "couch", "settee", "armchair", "table", "bed frame", "divan", "furniture", "dresser",
                "mattress", "bed"),
               ("upstairs", "up the stairs", "stairwell", "landing", "narrow stairs", "on my own",
                "by myself", "get it up", "move it up", "carry it up", "one person", "two people",
                "up a floor", "second floor", "top floor",
                "move", "moving", "moved", "new flat", "new house", "downstairs", "front door",
                "through the door", "doorway", "doorways", "van", "hire", "hiring", "removals",
                "removal", "too big", "wont fit", "won't fit", "get it to", "get it in")),
              _furniture_upstairs, bias=2,
              avoid=("assemble", "flat pack", "build", "ikea", "squeak", "hinge", "slide", "rail",
                     "mirror", "sell", "buy", "choose", "paint",
                     "cheap", "cheaper", "cheapest", "cheaply", "cost", "costs", "price",
                     "how much", "man with a van", "hire a van",
                     "my back", "my backs", "bad back", "sore back", "killing me", "back hurts",
                     "pulled my back", "hurt my back", "done my back", "in agony"),
              guard=_not_a_size_of_a_home),
        entry("wash-at-30",
              (("30", "30c", "30 c", "30 degrees", "thirty", "20c", "40", "40c", "40 degrees",
                "wash", "washing", "laundry", "wash cycle"),
               ("cheaper", "cheap", "cost", "costs", "save", "saves", "saving", "worth",
                "money", "bill", "bills", "pence", "expensive", "add up")),
              "About 15p a wash at 30C in electricity, against 25p at 40C: heating the water is most "
              "of what a wash costs, so 30C is the cheapest cycle that still cleans everyday clothes, "
              "shirts and jeans properly with a modern detergent. Go to 40C for heavily soiled work "
              "clothes and 60C for towels, bedding and anything with a stomach bug or a cold, because "
              "that is about killing germs rather than shifting dirt. A cold or 20C cycle saves a few "
              "pence more but struggles with grease.",
              avoid=("savings", "in savings", "have saved", "i have saved", "how much saved",
                     "by 40", "at 40", "by 50", "at 50", "by 60", "at 60", "pension", "pensions",
                     "retire", "retirement", "salary", "income", "put by", "put aside",
                     "how much should i have", "by now", "at my age",
                     "university", "uni", "degree", "college", "college course", "a level",
                     "gcse", "apprenticeship", "masters", "phd", "exam", "exams",
                     "car", "cars", "van", "bike", "bicycle", "motorbike", "vehicle", "car wash",
                     "jet wash", "driveway", "patio", "bin", "bins", "wheelie", "dog", "dogs",
                     "puppy", "cat", "horse", "hair", "face", "hands", "shower", "bath", "window",
                     "windows", "brush", "brushes", "paint", "dishwasher", "dishes", "washing up",
                     "washing-up", "machine not", "not draining", "wont drain", "won't drain",
                     "smell", "smells", "mould", "mold", "drain", "hose", "filter", "wool",
                     "woollen", "woolen", "silk", "cashmere", "dry clean", "dryer", "tumble",
                     "iron", "stain", "stains", "shrink", "shrunk", "bleach", "whites", "darks",
                     "towel", "towels", "bedding", "sheets", "sheet", "linen", "pillow", "pillows",
                     "duvet", "nappy", "nappies", "gym kit", "sports kit", "dishcloth", "tea towel",
                     "flannel", "blanket", "throws", "curtains", "mop",
                     "mins", "minute", "minutes", "miles", "further", "journey", "commute",
                     "commuting", "travel", "travelling"),
              guard=_a_wash_is_named),
        entry("cats-garden", (("cat", "cats", "kitten", "kittens", "neighbours cat", "neighbour's cat"),
                              ("garden", "gardens", "lawn", "flowerbed", "flower bed", "flowerbeds",
                               "borders", "vegetable patch", "sandpit", "poo", "poos", "pooing",
                               "toilet", "dig", "digging", "seedlings")),
              "Cats dig in bare, dry soil, so the reliable fix is to take that away: mulch the beds, lay "
              "chicken wire just under the surface, or plant through a membrane. Citrus peel, coffee "
              "grounds and a scattering of holly leaves or pine cones make the surface unpleasant, and a "
              "water pistol or a motion-triggered sprinkler teaches one cat to go elsewhere fast - "
              "renew it after rain, because scents fade.",
              avoid=("litter", "litter tray", "toilet training", "my cat is", "my cat wont",
                     "my cat won't", "pregnant", "fleas", "worms", "scratch", "scratching",
                     "waking me", "wakes me", "woke me", "woken me", "wake me up", "waking us",
                     "wakes us", "woke us", "waking the baby", "waking my baby", "waking my partner",
                     "waking my husband", "waking my wife", "waking my child", "waking my kids",
                     "keeping me awake", "keeps me awake", "kept me awake", "keeping us awake",
                     "keeps us awake",
                     "sleeps on my bed", "sleeping on my bed", "sleeps in my bed",
                     "sleeping in my bed", "sleeps on the bed", "sleeping on the bed",
                     "sleeps on our bed", "sleeping on our bed", "sleeps with me", "in bed with me",
                     "my pillow", "duvet", "bedroom",
                     "on the bed", "on my bed", "on our bed", "in the bed", "in my bed",
                     "on the carpet", "on the rug", "on the sofa", "on the settee", "on the couch",
                     "on the floor", "on the mat", "indoors", "in the house", "in the hall",
                     "in the kitchen", "in the bathroom", "in the bath", "litter",
                     "bite", "bites", "biting", "bit", "bit me", "nip", "nips", "nipping",
                     "scratches", "sofa", "couch", "furniture", "curtains", "spraying", "spray",
                     "mouse", "mice", "rat", "rats", "vole", "voles", "prey", "dead", "bird",
                     "birds", "pigeon", "pigeons", "brought", "brings", "bringing", "caught",
                     "dragged", "drops off")),
        entry("colour-choice",
              (("colour", "colours", "color", "colors", "palette", "scheme"),
               ("choose", "choosing", "pick", "picking", "decide", "deciding", "help me", "stuck",
                "no idea", "go for", "paint", "room", "rooms", "hall", "hallway", "walls",
                "bedroom", "kitchen", "lounge", "living room",
                "bathroom", "bathrooms", "nursery")),
              ("Pick the thing you cannot change - the floor, the tiles, the worktop, the sofa - and "
               "take the wall "
               "colour out of it in a paler version of itself. Then add one deeper tone from the same "
               "family for a rug or cushions and a wood or a metal to warm it: three colours, one of "
               "them a near-neutral. Paint a sample patch you can watch in the morning and again under "
               "the lamp before you buy a tin, because a colour on a small card lies."),
              ask=("choose", "choosing", "pick", "picking", "decide", "deciding", "help me", "stuck",
                   "no idea", "how do i go for", "what colour should i paint",
                   "which colour should i paint",
                   "what colour to", "what colour for", "what colour walls", "what colour goes",
                   "colour to paint", "which paint", "which white", "colour for a room",
                   "colour for my",
                   "which colour for", "which color for",
                   "neutral", "good colour", "good paint", "best colour", "best paint",
                   "what paint colour", "what colour paint", "paint colour for"),
              avoid=("blue", "navy", "grey", "gray", "green", "sage", "teal", "black", "brown",
                     "beige", "cream", "white", "yellow", "mustard", "pink", "red", "terracotta",
                     "purple", "orange", "silver", "charcoal", "gold", "peel", "peeling", "bubbling",
                     "stain", "tin", "tins", "brush", "roller", "how do i paint", "spill", "spilled",
                     "ceiling", "ceilings")),
        entry("ceiling-colour",
              (("ceiling", "ceilings"),
               ("colour", "color", "paint", "painting", "white", "which", "what colour",
                "what color")),
              "Matt white, or the palest tint of the wall colour, and one shade lighter than the walls "
              "if you want a tint at all: a ceiling painted as deep as the walls comes down on you and "
              "makes a small room feel lower. White bounces light back into the room, which is why a "
              "dark hallway or a north-facing room looks better with a warm white than a cool one, "
              "and a sunlit south room can take a cool white. In a kitchen or a bathroom use a "
              "moisture-resistant matt emulsion, because ordinary emulsion flakes over the steamy "
              "half of the room. Two coats of matt, rolled on a pole in strips, and paint the ceiling "
              "before the walls.",
              avoid=("stain", "stains", "leak", "leaking", "damp", "mould", "mold", "crack",
                     "cracks", "cracked", "peel", "peeling", "flake", "flaking", "spot", "spots",
                     "water", "fan", "fans", "light", "lights", "bulb", "insulation", "height"),
              guard=_asks_the_ceiling_colour,
              bias=1),
        entry("colour-pairing",
              (("colour", "colours", "color", "colors", "goes with", "go with", "go together",
                "match", "matches", "matching", "pairs with", "pair with", "compliment", "scheme",
                "together", "clash", "clashes"),
               ("blue", "navy", "grey", "gray", "green", "sage", "teal", "black", "brown", "beige",
                "cream", "white", "yellow", "mustard", "pink", "red", "terracotta", "purple",
                "orange", "silver", "charcoal", "gold")),
              _colour_advice,
              avoid=("paint brush", "paintbrush", "roller", "undercoat", "primer", "emulsion",
                     "dulux", "farrow", "tin", "tins", "stain", "mould", "peel", "peeling",
                     "bubbling", "screen", "phone", "nail varnish", "hair dye", "dye",
                     "how do i paint", "how to paint",
                     "salad", "plate", "plateful", "cheese", "recipe", "sauce", "cook", "cooking",
                     "eat", "eating", "food", "bread", "dish", "meal", "menu", "cake", "icing",
                     "curry", "pasta", "wine", "cocktail", "smoothie", "cocktail",
                     "tie", "suit me", "suits me", "a suit", "grey suit", "navy suit", "black suit",
                     "blue suit", "suit jacket", "suit and tie", "dress", "outfit", "shoes", "boots",
                     "shirt", "jacket", "coat", "chinos", "trousers", "skirt", "jumper", "to wear",
                     "wearing", "what colours suit", "what colors suit", "what colour suits",
                     "what colour should i wear"),
              bias=1),
        entry("shower-goes-cold",
              (("shower", "showers", "shower head"),
               ("goes cold", "gone cold", "runs cold", "turns cold", "going cold", "cold after",
                "cold quickly", "not hot", "warm then cold", "hot then cold", "cuts out", "heat up",
                "hot water runs out", "boiler",
                "is cold", "is lukewarm", "stays cold", "never hot", "never gets hot",
                "wont get hot", "won't get hot", "not getting hot", "runs lukewarm",
                "goes lukewarm", "is freezing", "water is cold", "runs hot")),
              "A shower that goes cold after a few minutes is usually the hot water, not the shower: "
              "a combi boiler only heats what you draw, so check whether the hot tap is still hot. If "
              "the tap is fine, the shower valve is scaled or failing, and cleaning the head in "
              "vinegar is the first free test. If the tap runs cold too, look at the boiler: its "
              "pressure gauge wants 1 to 1.5 bar while cold, and its fault code when it cuts out says "
              "what it is unhappy about.",
              ask=("cold", "hot", "cuts", "heat", "boiler", "gone", "goes", "runs", "turns",
                   "lukewarm", "freezing", "warm", "stays", "never"),
              avoid=("mould", "mold", "leak", "leaking", "drip", "dripping", "smell", "drain",
                     "blocked", "pressure", "weak", "install", "fit a", "buy", "replace")),
        entry("stripped-screw",
              (("screw", "screws", "screw head", "screwdriver", "bolt", "nut"),
               ("stripped", "rounded", "rounded off", "wont come out", "won't come out",
                "stuck", "seized", "sheared", "chewed", "no grip", "spinning", "removed",
                "remove", "undo", "loosen", "stuck screw",
                "get this screw out", "get the screw out", "get it out", "cant get")),
              "Once the cross is rounded there is no grip, so give it grip or give it something else "
              "to hold: press a wide rubber band or a steel-wool pad into the head and turn slowly "
              "with real downward force, or tap a slightly larger Torx or Phillips bit in with a "
              "hammer for a bite. If the head stands proud, cut a slot with a hacksaw and use a flat "
              "blade. Last resorts are pliers on the head, or drilling it out and using a screw "
              "extractor.",
              ask=("stripped", "rounded", "stuck", "seized", "chewed", "remove", "undo", "out"),
              bias=1,
              avoid=("shelf", "wall plug", "raw plug", "rawlplug", "plasterboard", "stud", "hinge",
                     "drill bit", "anchor")),
        entry("small-appliance-not-heating",
              (("microwave", "microwaves", "microwave oven", "kettle", "kettles", "toaster",
                "toasters", "sandwich toaster"),
               ("not heating", "not heating up", "isnt heating", "isn't heating", "isnt heating up",
                "isn't heating up", "wont heat", "won't heat", "wont heat up", "won't heat up",
                "doesnt heat", "doesn't heat", "doesnt get hot", "stays cold", "stays cold food",
                "food stays cold", "food is cold", "cold food", "no heat", "not getting hot",
                "stopped heating", "heats nothing", "wont warm", "won't warm", "not warm",
                "cold in the middle", "lukewarm", "takes ages", "stone cold")),
              _small_appliance_not_heating,
              avoid=("oven", "ovens", "cooker", "hob", "ring", "iron", "irons", "dryer",
                     "tumble dryer", "air fryer", "airfryer", "air-fryer", "boiler", "radiator",
                     "radiators", "immersion", "water", "shower",
                     "spark", "sparks", "sparking", "sparked", "smoke", "smokes", "smoking",
                     "flames", "caught fire", "on fire", "smell", "smells", "burning",
                     "metal", "foil", "tinfoil", "tin foil", "cutlery", "fork", "forks",
                     "clean", "cleaning", "descale", "limescale", "scale", "furred", "furring",
                     "noisy", "noise", "loud", "rattling", "humming",
                     "thanks", "thank you", "worked", "sorted", "perfect", "glad", "helped",
                     "worth replacing", "worth fixing", "worth repairing", "fix or replace",
                     "cheaper to buy", "should i buy", "which one", "best"),
              bias=1,
              fault=True),
        entry("oven-bakes-unevenly",
              (("oven", "cooker", "fan oven", "fan"),
               ("uneven", "unevenly", "cooks unevenly", "one side", "one half", "in patches",
                "patchy", "browns unevenly", "burns on one side", "burns on the top",
                "burns at the back", "takes longer", "front of",
                "burn the bottom", "burns the bottom", "burning the bottom", "burns on the bottom",
                "burns underneath", "bottom burns", "burnt bottom", "burned bottom",
                "burns the base", "soggy bottom")),
              "Fill the middle of the shelf, not the edges: a fan oven runs hottest near the door "
              "and the sides, so keep tins in the middle third with a gap of two fingers between "
              "them, and turn the tray round halfway through. Give it 15 minutes to preheat and "
              "check the dial with a cheap oven thermometer - most ovens are out by 10 to 20C, and "
              "an oven that reads 20C low browns the back before the front. If it is always the "
              "bottom that catches, the tin is too low or it is a dark one: move it up a shelf, "
              "use a lighter tin and drop the heat 10C. If the same side is always pale while the "
              "other catches, that is the element or the fan, not your baking.",
              avoid=("not heating", "not heating up", "isnt heating", "isn't heating", "not hot",
                     "wont heat up", "won't heat up", "gas", "smell", "smells", "clean",
                     "cleaning", "oven chips", "recipe", "how long", "what temperature",
                     "gas mark", "turkey", "roast"),
              fault=True),
        entry("oven-not-heating",
              (("oven", "cooker"),
               ("not heating", "not heating up", "not hot", "not getting hot", "isnt heating",
                "isn't heating", "takes ages", "slow to heat", "cold", "warm up", "not warming",
                "temperature", "thermostat", "element", "uneven", "unevenly", "isnt getting hot",
                "isnt hot", "wont heat up", "won't heat up")),
              "On an electric oven the heating element is almost always the fault, and it fails in the "
              "way you can see: heat the oven for ten minutes in the dark and look for the element to "
              "glow red - a dull patch or a cold half is a broken element, about £20 to £40 for the part "
              "and £60 to £90 for an engineer. A fan oven that runs cold is often the fan motor or the "
              "thermostat instead. Turn the power off at the wall before you touch anything, and a gas "
              "oven that will not light is a gas-safe job, not a DIY one.",
              avoid=("fan oven", "roast", "roasting", "bake", "baking", "bread", "cake", "chicken",
                     "pizza", "chips", "recipe", "how long", "minutes", "turkey", "yorkshire",
                     "temperature for", "what temperature", "gas mark",
                     "thanks", "thank you", "perfect", "worked", "sorted", "glad", "helped",
                     "delicious", "came out", "was lovely", "brilliant", "spot on"),
              fault=True),
        entry("weak-flow",
              (("tap", "taps", "mixer", "hot water", "cold water"),
               ("pressure", "low pressure", "weak", "dribble", "dribbles", "trickle", "low flow",
                "not strong", "losing pressure")),
              "A weak flow is almost always at the outlet, not in the boiler: unscrew the tap nozzle "
              "and soak it in descaler, open the isolator under the sink all the way, and check the "
              "stopcock has not been half shut. A combi only gives full flow at one tap at a time, so "
              "if the pressure drops when a second tap runs that is normal. If it is weak on every tap "
              "in the house, the stopcock or the mains is the place to look, not the plumbing.",
              bias=1,
              avoid=("bar", "gauge", "boiler pressure", "dropping", "radiators", "heating",
                     "shower", "showers", "showerhead", "shower head", "electric shower",
                     "power shower")),
        entry("hot-water-slow",
              (("hot water", "tap", "shower"),
               ("takes ages", "slow", "slowly", "come through", "waiting", "hot then cold")),
              "On a combi boiler, about 20 to 30 seconds is normal: you are waiting for the boiler to "
              "fire and for the hot water to travel down the pipe from it. If it is minutes, or the "
              "water runs hot then cold, the plate heat exchanger is scaled (a typical 5 to 10 year "
              "service item) or the boiler is undersized for two taps at once. If the flow is weak as "
              "well, check the isolator under the sink is fully open and unscrew the tap nozzle to "
              "clear the scale.",
              avoid=("dropping", "bar", "gauge", "radiator", "radiators")),
        entry("floor-gone-dull",
              (("floor", "flooring", "floorboards"),
               ("dull", "dullness", "shiny", "shine", "worn", "wear", "scratched", "grey", "greyish",
                "tired", "restore", "polish")),
              "A dull wooden floor has worn through its finish, not its wood, so clean it with a "
              "diluted wood floor soap rather than a polish or a steam mop, then put a maintenance coat "
              "of the same hard wax oil or lacquer back on - one coat on the traffic lanes every year or "
              "two. Sanding is only for deep scratches; a whole-room sand and re-finish is £20 to £30 "
              "a square metre if you have it done.",
              avoid=("deep scratch", "scratches down", "scuffed", "laminate", "click", "install", "worktop",
                     "worktops", "counter", "countertop", "sink", "bath", "table")),
        entry("mice-in-the-house",
              (("mice", "mouse"),
               ("loft", "attic", "kitchen", "house", "flat", "garage", "shed", "cupboard", "droppings",
                "scratching", "noise", "noises", "get rid", "rid of", "infestation", "coming in",
                "getting in", "get in", "got in", "get into", "getting into", "coming into",
                "keep out", "keep them out", "stopping", "stop")),
              "Find the way in first: mice follow pipes and cables, so check the gap round the pipework "
              "under the sink, the air brick, and any gap wider than a pencil behind kitchen units, and "
              "block those with wire wool and filler. Then bait two or three traps along the wall, "
              "because mice run against edges, and clear the food source - a sealed bin and nothing left "
              "out overnight. Skip poison in a loft if there are pets or children, and the council pest "
              "control team is usually cheaper than a private firm.",
              avoid=("cat", "cats", "kitten", "dog", "hamster", "pet", "rat", "rats", "rodent",
                     "garden", "outside", "compost", "bird feeder", "bird seed", "field mouse"), report=True),

        entry("woodlice",
              (("woodlice", "woodlouse", "wood lice", "slaters", "sow bugs", "pill bugs", "pillbugs",
                "isopods"),
               ("get rid", "rid of", "kill", "killing", "coming in", "come in", "in the house",
                "in my house", "in the kitchen", "in my kitchen", "in the bathroom", "everywhere",
                "keep finding", "finding", "remove", "stop", "why", "damp", "in the corner")),
              "Woodlice eat rotting wood and need damp, so drying the damp out is the whole job: fix "
              "the leak, clear wet leaves and timber away from the outside walls, and ventilate the "
              "room they keep appearing in. They do not damage anything in a dry house and they die "
              "within days indoors. Find the wet wood or the damp corner they are living under, and a "
              "dehumidifier or a line of salt buys you time while you sort it.",
              avoid=("bite", "bites", "bitten", "itch", "itching", "rash", "head lice", "nits",
                     "cat", "dog", "pet", "eat", "eating", "poison", "harmful", "dangerous",
                     "get in my hair"), report=True),

        entry("rats-outside",
              (("rat", "rats", "rodent", "rodents"),
               ("garden", "shed", "outside", "outdoors", "compost", "bin", "bins", "bird feeder",
                "bird feeders", "bird seed", "decking", "garage", "drive", "greenhouse", "pond",
                "scratching", "droppings", "get rid", "rid of", "house", "loft", "under the",
                "in the day", "daytime", "getting in", "get in", "coming in", "keep out", "stop")),
              "Cut the food and the cover before you bait: take the bird feeders down or use a seed "
              "tray, keep the compost heap closed and stop putting cooked food in it, and clear the "
              "long grass and rubbish they are running behind. Then use two lockable bait stations "
              "along the wall where you have seen them and check them every couple of days - loose "
              "poison is a real risk to cats, dogs and children. If they are in the house, the "
              "council's pest control team is usually cheaper than a private firm.",
              avoid=("cat", "cats", "kitten", "dog", "dogs", "hamster", "pet", "pets", "gerbil",
                     "ferret", "road", "attic"), report=True),

        entry("chemicals-and-a-child-or-pet",
              (("bait", "rat bait", "mouse bait", "bait box", "bait station",
                "rat poison", "mouse poison", "rodenticide", "slug pellet", "slug pellets",
                "ant powder", "ant killer", "ant bait", "insect powder", "weedkiller", "weed killer",
                "pesticide", "mouse trap", "mouse traps", "rat trap", "rat traps",
                "flea bomb", "flea bombs", "fogger", "bug bomb", "oven cleaner", "drain cleaner",
                "bleach", "paint thinner", "turps", "turpentine", "antifreeze", "air freshener",
                "air fresheners", "diffuser", "reed diffuser", "plug in air freshener", "chemical",
                "chemicals",
                "spray", "sprays", "aerosol", "fly spray", "insect spray", "ant spray",
                "wasp spray", "flea spray", "bug spray", "mosquito spray", "room spray",
                "fly killer", "insect killer"),
               ("toddler", "toddlers", "baby", "babies", "newborn", "child", "children", "kid",
                "kids", "grandchild", "grandchildren", "pregnant", "pregnancy", "expecting",
                "cat", "cats", "kitten", "kittens", "dog", "dogs", "puppy", "puppies", "pet",
                "pets", "hamster", "rabbit", "bird", "birds", "parrot", "fish", "safe", "unsafe",
                "dangerous", "harmful", "poisonous", "risky", "ok around", "get at",
                "breathe", "breathing", "breathe in", "breathing in", "fumes", "inhale",
                "in the room", "same room", "the room", "ventilate",
                "safe with", "safe around", "safe for", "safe to use", "is it safe",
                "ok with", "ok around", "harmful to", "harmful for", "dangerous to",
                "dangerous for", "bad for")),
              _chemical_safety,
              avoid=("chocolate", "onion", "onions", "garlic", "grape", "grapes", "raisin",
                     "raisins", "sultana", "sultanas", "xylitol", "lily", "lilies", "poinsettia",
                     "avocado", "alcohol", "caffeine", "whites", "white cotton", "cotton",
                     "laundry", "washing", "nappies", "nappy", "stain", "stains", "toilet",
                     "mould", "limescale", "descale", "drain", "blocked", "smell in", "how do i clean",
                     "how to clean",
                     "plant", "plants", "houseplant", "houseplants", "bulb", "bulbs", "flowers",
                     "shrub", "shrubs", "tree", "trees", "mushroom", "mushrooms", "berries",
                     "cat grass", "ivy", "holly", "oak", "acorn", "acorns",
                     "stain", "stains", "carpet", "carpets", "mattress", "sofa", "odour",
                     "smell", "smells", "stinks", "flea collar", "bite", "bites",
                     "bitten", "itch", "itching", "marking", "litter",
                     "ate", "eaten", "eating", "swallowed", "swallowing", "poisoned",
                     "keeps spraying", "is spraying", "spraying indoors", "cat spraying")),

        entry("damp-bathroom",
              (("bathroom", "shower room", "ensuite", "en suite", "wet room", "loo", "toilet"),
               ("damp", "damper", "damp patch", "steamy", "steam", "condensation", "wet walls",
                "sweating", "always wet", "stays wet")),
              ("Run the extractor while you shower and for twenty minutes after, or open a window, and "
               "keep the door shut so the wet air stays in one room. Wipe the walls down, dry washing "
               "outside rather than over a radiator, and keep the heating on low: warm air holds the "
               "water, a cold bathroom drops it on the walls. If it carries on, the fan is "
               "under-powered or the duct is blocked."),
              avoid=("leak", "leaks", "leaking", "dripping", "water coming", "from above", "roof",
                     "pipe", "burst", "remove mould", "get rid of the mould", "black mould", "kill")),
        entry("bath-length",
              (("bath", "baths", "bathtub", "shower", "showers", "showering", "shower gel"),
               ("how long", "how often", "every day", "daily", "too long", "how many times",
                "need to shower", "need to bathe", "should i shower", "should i bathe",
                "yes or no", "length of", "much time")),
              _bath_length,
              avoid=("clean", "cleaning", "cleaner", "scum", "limescale", "mould", "drain", "blocked",
                     "dog", "dogs", "cat", "cats", "baby", "babies", "newborn", "toddler", "plug",
                     "boiler", "leak", "before bed", "help me sleep",
                     "or a shower", "or a bath", "bath or shower", "shower or a bath",
                     "better than", "which is better",
                     "morning", "evening", "at night", "before work", "after work") + _BATH_CITY),

        entry("bath-water-heat",
              (("bath", "baths", "bathtub", "bath tub", "bath water", "bathwater", "baby bath",
                "baby's bath", "babys bath", "babies bath", "toddler bath", "a bath", "the bath",
                "baby bath be", "baby bath temperature", "bath be for a toddler",
                "bath be for a baby", "bath for a toddler", "bath for a baby"),
               ("how hot", "how warm", "too hot", "temperature", "degrees", "warm enough",
                "hot enough", "what temperature", "right temperature", "37c", "38c", "40c")),
              "A bath is right at 37 to 38C - the elbow test is the reliable one, because a hand "
              "that has been in the water stops being a judge. Run the cold in first and top it up "
              "with hot, never the other way round, and never add hot water with a child already "
              "in it. For a baby or a toddler it is the same 37 to 38C and only up to the waist "
              "when they are sitting, with the cold tap run last, and a bath above 40C is too hot "
              "for anyone to sit in for long.",
              avoid=("clean", "cleaning", "cleaner", "scum", "limescale", "stain", "stains",
                     "mould", "drain", "blocked", "dog", "dogs", "cat", "cats", "plug",
                     "boiler", "leak", "hot tub", "jacuzzi", "sitz", "bath salts", "bath bomb",
                     "bath mat", "bathroom", "before bed", "help me sleep",
                     "or a shower", "or a bath", "bath or shower", "shower or a bath",
                     "which is better", "better than", "how long", "how often", "how deep",
                     "swimming", "swim", "pool", "spa") + _BATH_CITY,
              bias=1),

        entry("baby-bath",
              (("bath", "bathtub", "bathe", "bathing", "top and tail",
                "wash a baby", "wash the baby", "wash my baby", "wash your baby",
                "washing a baby", "washing the baby", "washing my baby", "washing your baby",
                "wash a newborn", "wash the newborn", "wash my newborn", "washing a newborn",
                "washing the newborn", "washing my newborn", "wash babys hair", "wash baby hair",
                "wash the babys hair", "wash the baby's hair", "wash my babys hair",
                "wash my baby's hair"),
               ("baby", "babies", "newborn", "infant", "toddler", "how hot", "temperature",
                "how often", "how deep", "safe", "first bath", "umbilical", "cord")),
              "Fill it to about 5 to 8 cm with water at 37 to 38C - elbow or wrist temperature, which "
              "feels neither warm nor cool - and have the towel, nappy and clean clothes within reach "
              "before you start, because you never leave a baby alone in water, not for a second. "
              "Support the head and shoulders with one forearm, wash with plain water for the first "
              "month or so, and keep the room warm since a wet baby loses heat fast. Twice or three "
              "times a week is enough for a newborn; top and tail in between.",
              avoid=("clean the bath", "cleaning", "scum", "limescale", "mould", "drain", "blocked",
                     "dog", "cat", "hot tub", "jacuzzi", "sitz", "bath salts", "bath bomb",
                     "pregnant", "pregnancy", "trimester", "weeks pregnant",
                     "clothes", "laundry", "wash clothes", "washing clothes", "load of washing",
                     "washing machine", "colours", "colors", "darks", "whites", "lights",
                     "bedding", "sheets", "duvet", "towels",
                     "bottle", "bottles", "sterilise", "sterilising", "sterilize", "formula", "pump",
                     "baby clothes", "babygrow", "baby grow", "vest", "muslin", "nappy", "nappies",
                     "hand", "hands", "dishes", "dish", "plates", "pots", "pans", "face", "hair",
                     "shower", "washing up", "car", "car wash",
                     "pillow", "pillows", "pillowcase", "pillowcases", "mattress", "bath towel",
                     "bath towels", "linen", "flannel", "flannels", "face cloth", "bath mat",
                     "curtain", "curtains")
                     + _BATH_CITY),

        entry("bath-or-shower",
              (("bath", "baths", "bathtub", "shower", "showers", "showering"),
               ("better", "best", "worse", "prefer", "rather", "or a bath", "or a shower",
                "bath or shower", "bath or a shower", "shower or bath", "shower or a bath",
                "instead of", "worth it",
                "less water", "more water", "uses less")),
              "Showering wins on time and water - five minutes with a normal head is about 40 to 50 "
              "litres against 80 or so for a full bath - so if it is the water you are asking about, "
              "shower and keep it short. Neither is better for your skin; long hot water is what "
              "leaves it tight and itchy, so keep it warm rather than hot and pat dry instead of "
              "rubbing. If a bath leaves you light-headed, get out slowly and drink some water.",
              avoid=("clean", "cleaning", "cleaner", "scum", "limescale", "stain", "stains", "mould",
                     "drain", "blocked", "dog", "dogs", "cat", "cats", "baby", "babies", "newborn",
                     "toddler", "plug", "water pressure", "boiler", "leak",
                     "before bed", "help me sleep", "aches", "ache", "relax", "unwind", "sore",
                     "stiff", "muscles",
                     "how long", "how often", "every day", "daily", "too long", "how many times")
                     + _BATH_CITY),

        entry("bath-for-sleep",
              (("bath", "baths", "bathtub", "hot bath", "warm bath", "long bath", "deep bath",
                "shower", "showers"),
               ("before bed", "before bedtime", "help me sleep", "help you sleep", "to sleep",
                "sleep", "aches", "ache", "aching", "relax", "unwind", "sore", "stiff", "muscles",
                "winding down", "cant sleep", "can't sleep")),
              "Yes - a warm bath 10 to 15 minutes long, an hour or two before bed, is one of the few "
              "home things that reliably helps you drop off: the water warms you and the climb back "
              "down afterwards is what makes you sleepy. Keep it warm rather than hot, which leaves "
              "skin tight and can make you light-headed, and get out slowly if the room spins. The "
              "same bath eases aching muscles for the same reason.",
              avoid=("clean", "cleaning", "cleaner", "scum", "limescale", "stain", "mould", "drain",
                     "blocked", "dog", "dogs", "cat", "cats", "baby", "babies", "newborn", "toddler",
                     "plug", "boiler", "leak", "less water", "more water", "uses less")
                     + _BATH_CITY),

        entry("bath-dizzy",
              (("bath", "hot bath", "bathtub", "shower", "hot shower", "jacuzzi", "hot tub"),
               ("dizzy", "dizziness", "light headed", "light-headed", "faint", "fainted", "spins",
                "spinning", "woozy", "sick", "nausea", "head rush", "stand up", "standing up")),
              "Hot water opens up the blood vessels near the skin, so blood pressure drops and standing "
              "up quickly leaves you light-headed - it is common, and it is not a sign of anything "
              "wrong in a healthy person. Get out slowly, sit down on the edge for a minute, keep the "
              "water warm rather than hot, drink some water and eat beforehand. If you actually faint, "
              "or it happens every time, or it comes with chest pain or palpitations, get it checked.",
              avoid=("clean", "cleaning", "scum", "limescale", "mould", "blocked", "drain", "dog",
                     "cat", "baby", "babies", "newborn", "toddler", "before bed", "help me sleep",
                     "less water", "more water") + _BATH_CITY),

        entry("bathroom-fan-wont-stop",
              (("fan", "extractor", "extractor fan", "ventilation"),
               ("runs all the time", "runs on", "wont turn off", "won't turn off",
                "wont switch off", "won't switch off", "wont go off", "won't go off",
                "never stops", "never turns off", "keeps running", "stays on", "left on",
                "all night", "all the time", "after the light goes off", "timer")),
              "Ten or fifteen minutes of running on after the light goes off is the timer doing its "
              "job, and it is what keeps the damp out. A fan that never stops has an overrun set too "
              "long, a stuck timer, or a humidistat turned up too high: take the cover off and look "
              "for the overrun screw or a dial inside, set the overrun to about fifteen minutes, and "
              "turn the humidistat down to around 60% - if neither is there, or it will not change, "
              "the module is a swap, around £25 to £60. A fan that runs only when nobody is in the "
              "room, or one that is still going after the isolator is off, is a wiring job.",
              avoid=("drip", "drips", "dripping", "water", "leak", "leaks", "leaking",
                     "condensation", "cold", "black mould", "bathroom is damp", "steam",
                     "laptop", "lap top", "computer", "pc", "desktop", "macbook", "mac book",
                     "phone", "console", "playstation", "ps4", "ps5", "xbox", "gpu",
                     "graphics card", "car", "van", "motorbike", "engine", "overheating",
                     "overheat", "oven", "fridge", "freezer", "tumble dryer"),
              bias=3),
        entry("bathroom-fan-noisy",
              (("bathroom", "shower", "loo", "toilet", "wet room", "ensuite"),
               ("fan", "extractor", "ventilation", "vent", "humming", "rattling", "buzzing", "whirring",
                "noisy", "loud", "noise", "weak")),
              "Clean the cover and the blades first: a dust-clogged fan in a steamy room is both weak "
              "and loud, and the grille usually comes off with a push and the blades wipe with a damp "
              "cloth once the isolator is off. A rattle is normally the cover or the backdraught flap in "
              "the duct; a buzz or a grind means the bearing has gone, and a new fan is £25 to £60 for "
              "the part with about an hour of an electrician. A fan that runs on for ten or fifteen "
              "minutes after the light goes off is the timer doing its job and is what actually stops "
              "the damp; one that never stops has a stuck timer or a humidistat set too high, and the "
              "module is a swap.",
              avoid=("kitchen", "hob", "cooker", "grease", "oven", "cost", "costs", "price",
                     "runs all the time", "runs on", "wont turn off", "won't turn off",
                     "wont switch off", "won't switch off", "wont go off", "won't go off",
                     "never stops", "keeps running", "stays on", "after the light goes off",
                     "drip", "drips", "dripping", "water", "leak", "leaks", "leaking",
                     "condensation",
                     "how much", "cheap", "cheapest", "buy", "buying", "which", "best", "install",
                     "installing", "installation", "fitter", "fitted", "fit one", "replace",
                     "replacing", "replacement", "new fan", "new bathroom fan", "quote",
                     "electric shower", "power shower", "shower pressure", "shower is weak",
                     "shower dribbles", "shower head", "showerhead")),
    entry(
        "radiator-drain",
        (("drain", "draining", "drained", "empty", "emptying", "take off", "taking off",
          "take out", "remove", "removing", "come off", "swap", "replace",
          "off the wall", "to decorate", "decorating", "for decorating",
          "fill", "filling", "fill up", "fill it up", "refill", "refilling", "top up",
          "topping up", "back up"),
         ("radiator", "radiators", "rad", "rads",
          "central heating", "the heating", "heating system", "the system")),
        "Turn the heating off and let it go cold, then close the valve at both ends: the wheelhead on "
        "the flow and the lockshield on the return, and count the turns on the lockshield so you can "
        "set it back the same, because that is what balances the house. Put a shallow tray and old "
        "towels under the bottom union and open the bleed valve at the top to let air in - the water "
        "comes out of the nut slowly and it is filthy black, so do it in short goes. Take the bracket "
        "off, and when you refit it open the bleed valve and top the pressure up at the filling loop "
        "to about 1.2 bar, then bleed every radiator once more. If it is a sealed combi system and the "
        "pressure will not hold, that is a plumber's job. For the whole house rather than one "
        "radiator, do the same at the lowest drain cock with every bleed valve open, because one "
        "radiator holds only a bucket or two.",
        avoid=("cold", "colder", "not heating", "not getting hot", "cold at the top", "cold at the "
               "bottom", "bleed", "bleeding", "bleed it", "noisy", "banging", "knocking", "gurgling",
               "leak", "leaking", "dripping", "towel rail not", "boiler", "no pressure",
               "lost pressure", "pressure is low", "electric", "oil filled", "oil-filled",
               "oil radiator",
               "clothes", "dry clothes", "car", "van", "engine", "phone",
               "laptop", "battery", "pasta", "sink", "bath", "pond", "pool", "garden", "account",
               "bank", "pool of water",
               "scuff", "scuffs", "mark", "marks", "crayon", "ink", "stain", "stains", "dirty",
               "clean", "cleaning", "wipe", "wash", "paint", "painting", "repaint", "repainting",
               "rust", "rusty", "rusting"),
        bias=3),

    entry(
        "radiator-clean",
        (("clean", "cleaning", "dust", "dusty", "hoover", "hoovering", "vacuum", "vacuuming",
          "wash", "wipe", "wipe down", "fins"),
         ("radiator", "radiators", "rad", "rads", "behind the radiator")),
        "Dust between the fins does more to cut the heat than anything you can do on the outside: run "
        "a vacuum cleaner's crevice tool down each gap with the heating off, and a long flexible "
        "duster gets the space behind without moving the radiator. For the paintwork plain warm water "
        "with a drop of washing-up liquid is enough - skip anything abrasive, which takes the enamel "
        "off - and keep water away from the valves and away from an electric one. Once before the "
        "heating goes on in autumn, and again in mid-winter if a room is slower to warm than it used "
        "to be.",
        avoid=("drain", "draining", "bleed", "bleeding", "leak", "leaking", "dripping", "cold",
               "not heating", "noisy", "banging", "gurgling", "paint", "painting", "decorate",
               "decorating", "rust", "rusty", "clothes", "towel rail", "boiler", "car", "van",
               "engine", "oven", "kitchen", "phone", "laptop", "floor", "carpet", "pond",
               "wall", "walls", "skirting", "behind the wall", "the wall behind"),
        bias=2),

    entry(
        "radiator-foil",
        (("foil", "tin foil", "reflector", "reflective", "reflect", "insulate", "insulation"),
         ("radiator", "radiators", "rad", "behind")),
        "Worth it only on an outside wall with no cavity insulation: a sheet of radiator foil behind "
        "the radiator, shiny side facing the room, pushed back so it does not touch the brackets, "
        "gives you a few percent rather than the half the adverts claim. Keep the gap under the "
        "radiator clear, because that is where the cold air comes in and the warm air goes out - a "
        "shelf or a curtain hanging over the top cancels the gain. Foil on an inside wall, or over a "
        "cavity, does nothing at all.",
        avoid=("loft", "roof", "cavity wall", "wall insulation", "shed", "greenhouse", "drain",
               "bleed", "bleeding", "leak", "leaking", "cold", "noisy", "boiler", "cooker", "oven",
               "food", "garden", "pond", "cake", "chicken"),
        bias=2),

    entry(
        "carpet-ruck",
        (("carpet", "carpets", "rug", "rugs", "carpet tile", "carpet tiles", "underlay",
          "gripper", "grippers", "flooring"),
         ("rucking", "rucked", "ruck", "rucks", "ripple", "ripples", "rippled", "wrinkle",
          "wrinkles", "wrinkled", "bubble", "bubbles", "bubbling", "baggy", "puckered",
          "puckering", "lifting", "come up", "coming up", "creased", "creases", "wavy",
          "sliding", "slides", "slipping", "moves", "moving", "loose")),
        "A carpet that ripples or wrinkles has stretched, and the fix is a re-stretch rather than "
        "an iron: the pile gives over the years, and a wet clean, a hot radiator or a heavy chair "
        "in one spot speeds it up. A fitter lifts the carpet off the gripper along one or two "
        "walls, pulls it tight with a knee kicker or a power stretcher and hooks it back on, which "
        "is an hour or two of work and far cheaper than a new carpet. One small bubble can be "
        "worked towards the nearest wall by hand and taken out the same way, and a bump that comes "
        "back after a day means the underlay has gone, not the carpet. A rug that slides on a "
        "wooden floor is the other problem: a rubber or felt underlay pad, or a strip of double-"
        "sided carpet tape, stops it without marking the boards.",
        bias=1),

        entry("workshop-edge",
              (("chisel", "chisels", "wood chisel", "bevel edge chisel", "mortise chisel",
                "plane iron", "plane blade", "hand plane", "block plane",
                "drill bit", "drill bits", "masonry bit", "masonry bits", "hss bit", "spade bit",
                "auger bit", "forstner bit", "hole saw", "utility knife", "stanley knife",
                "craft knife"),
               ("sharpen", "sharpening", "sharpened", "sharper", "blunt", "dulled", "dull",
                "hone", "honing", "whetstone", "oilstone", "grind", "grinding", "file", "filing",
                "wont cut", "won't cut", "doesnt cut", "doesn't cut", "not cutting", "burr",
                "rounded", "chipped", "nicks", "nicked")),
              "Chisel and plane iron: the bevel is 25 degrees off the flat back, so a honing guide "
              "set to 25 and a strip of wet-and-dry on a flat tile does it - 240 grit if the edge "
              "is nicked, then 600 and 1200, ten strokes on the bevel, then lay the back flat on "
              "the finest paper and pull it back a few times to take the burr off. A blunt chisel "
              "crushes the wood and takes more force to steer, so it is the sharp one that is "
              "safer. A masonry bit is blunt when the tip is rounded: a few strokes of a diamond "
              "file on the wings either side of the point, at the angle they already have, brings "
              "it back. An HSS bit filed by hand is slow going and a new one costs a few pounds, so "
              "buy a bit rather than an afternoon; a Drill Doctor type jig, about \u00a330, earns "
              "its place only if you go through a lot of them. In a utility knife, swap the blade: "
              "a snap-off blade is sharper than anything you can dress at home.",
              avoid=("knife", "knives", "kitchen", "cooking", "chef", "scissors", "shears",
                     "secateurs", "hedge", "hedges", "axe", "chainsaw", "mower", "lawn", "pencil",
                     "pencil sharpener", "image", "photo", "picture quality", "sound", "pain",
                     "eyes", "vision", "glasses", "tooth", "teeth", "sharply"),
              bias=2),
        entry("wood-splits-when-nailed",
              (("wood", "wooden", "plank", "planks", "timber", "batten", "battens", "board",
                "boards", "mdf", "hardwood", "softwood", "decking", "board end",
                "floorboard", "floorboards", "skirting", "skirting board", "skirting boards",
                "architrave", "beading", "joist", "joists", "stud", "studs", "door frame",
                "doorframe", "fence", "fencing", "shed"),
               ("split", "splits", "splitting", "crack", "cracks", "cracking", "splinter",
                "splinters", "splintering", "nail", "nails", "nailed", "nailing", "hammer",
                "pilot hole", "screw")),
              _the_wood_and_the_nail,
              avoid=("glue two", "join", "joining", "dowel", "sanding", "sand it", "sandpaper",
                     "firewood", "fire wood", "log", "logs", "log burner", "stove", "season",
                     "seasoned", "kiln",
                     "fence panel", "fence panels", "panel", "panels", "post", "posts",
                     "gate", "back up"),
              bias=2),
        entry("a-nail-in-a-wall",
              (("nail", "nails", "nailing", "nailed", "picture hook", "picture hooks",
                "rawlplug", "rawlplugs", "rawl plug", "rawl plugs", "wall plug", "wall plugs"),
               ("wall", "walls", "brick", "plasterboard", "stud", "studs", "picture",
                "pictures", "put up", "putting up", "hang", "hanging", "remove", "removing",
                "out", "pull", "old", "stuck", "left in")),
              _a_nail_in_the_wall,
              avoid=("fingernail", "fingernails", "toenail", "toenails", "my nail", "my nails",
                     "cut my nails", "bite", "biting", "polish", "varnish", "manicure",
                     "tyre", "tyres", "tire", "tires", "puncture", "wood", "plank", "timber",
                     "door", "doors", "decking", "fence", "fencing",
                     "plasterboard", "plaster board", "hollow wall", "hollow walls",
                     "stud finder", "plasterboard fixing", "plasterboard fixings"),
              bias=2),
    ]

