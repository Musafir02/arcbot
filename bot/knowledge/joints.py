
from .lookup import entry

import re

ANSWERS = ("health",)

NOISY = ("click", "clicks", "clicked", "clicking", "pop", "pops", "popped", "popping",
         "creak", "creaks", "creaking", "grind", "grinds", "grinding", "snap", "snaps",
         "snapping", "crack", "cracks", "cracking", "cracked", "noisy", "noise",
         "clunk", "clunks", "clunking")

PARTS = ("knuckle", "knuckles", "jaw", "jaws", "wrist", "wrists", "elbow", "elbows",
         "shoulder", "shoulders", "hip", "hips", "ankle", "ankles", "thumb", "thumbs",
         "toe", "toes", "finger", "fingers", "joint", "joints", "neck", "spine")

ONE = {"knuckles": "knuckle", "jaws": "jaw", "wrists": "wrist", "elbows": "elbow",
       "shoulders": "shoulder", "hips": "hip", "ankles": "ankle", "thumbs": "thumb",
       "toes": "toe", "fingers": "finger", "joints": "joint"}

HURTS = ("hurt", "hurts", "hurting", "pain", "pains", "painful", "sore", "ache", "aches",
         "aching", "achy", "swollen", "swelling", "swelled", "stiff", "locked", "locking",
         "locks", "stuck", "sharp")

AVOID = ("knee", "knees", "kneecap",
         "jaw", "jaws", "jawbone", "jaw joint", "tmj",
         "car", "cars", "brake", "brakes", "engine", "clutch", "gearbox", "exhaust", "bike",
         "bicycle", "boiler", "radiator", "pipe", "pipes", "tap", "taps", "washing machine",
         "dishwasher", "tumble", "fridge", "freezer", "oven", "toaster", "kettle",
         "door", "doors", "gate", "window", "windows", "hinge", "floor", "floors",
         "floorboard", "floorboards", "decking", "stair", "stairs", "wall", "walls", "wood",
         "wooden", "tile", "tiles", "pavement", "road",
         "phone", "iphone", "laptop", "computer", "mouse", "keyboard", "headphones",
         "speaker", "speakers", "radio", "tv", "television", "printer", "camera", "app",
         "video", "audio", "volume", "hearing aid", "playstation", "xbox",
         "ear", "ears", "throat", "swallow", "swallowing", "hearing", "tinnitus",
         "chest", "heart", "breath", "breathing", "tooth", "teeth",
         "egg", "eggs", "shell", "boil", "boiling", "boiled", "mug", "cup", "glass",
         "screen", "voice", "whip", "meringue", "batter", "pastry", "dough", "bread", "cake",
         "sprain", "sprained", "sprains", "strain", "strained", "strains", "injury",
         "injuries", "injured", "hurt myself", "fall", "falls", "fell", "fallen", "accident",
         "surgery", "operation", "op", "operated", "replaced", "replacement", "physio",
         "physiotherapy", "cast", "crutches", "brace", "break", "broke", "broken",
         "fracture", "fractured", "dislocated", "dislocate", "torn", "tear", "tore",
         "arthroscopy", "keyhole",
         "gives way", "give way", "giving way", "gave way", "out of place", "popped out",
         "pops out", "numb", "numbness", "numbed", "tingling", "tingles", "tingle",
         "pins and needles", "weak", "weakness", "unstable", "catching", "catches",
         "my son", "my daughter", "my child", "my kid", "my kids", "my baby", "my toddler",
         "my husband", "my wife", "my partner", "my mum", "my mom", "my mother", "my dad",
         "my father", "my dog", "my cat", "my puppy")


SHOULDER_TIMELINE_CARD = (
    "A shoulder replacement is in a sling for the first 3 to 6 weeks, with gentle movement "
    "exercises started within days and the physio's programme once the sling comes off: driving "
    "again at about 6 to 8 weeks once you can turn the wheel and brake without pain, desk work at "
    "6 to 12 weeks, and full recovery 6 to 12 months. Hospital is usually one or two nights. Ring "
    "the ward or 111 if the wound starts leaking, the shoulder turns hot or red, or the pain "
    "suddenly gets worse.")

SHOULDER_IMPLANT_CARD = (
    "A shoulder replacement usually lasts 10 to 15 years, and a reverse shoulder about the same - "
    "it is not a countdown: the muscle you keep working and the load you put through it decide, so "
    "the exercises the physio gives you are what buy the time. If a shoulder that has been fine "
    "for years starts to ache, grind or give way, that is worth an X-ray rather than waiting, and a "
    "worn shoulder can be revised the way a hip can.")

SHOULDER_SORE_CARD = (
    "Yes - soreness and stiffness for months after a shoulder replacement is normal, and it eases "
    "with the exercises rather than with rest: it is at its stiffest in the first six weeks and "
    "keeps loosening for up to a year, and a warm, puffy shoulder after a session is the usual "
    "reaction to doing more. Build up slowly, ice it for 15 minutes after the exercises, and keep "
    "the daily ones going even on a bad day. Ring the ward or 111 if the shoulder is hot and red, "
    "the wound leaks, or the pain gets worse each week rather than better.")

SHOULDER_SLEEPING_CARD = (
    "Sleep is the awkward part for the first weeks after a shoulder replacement: sleep propped up "
    "on two or three pillows with the arm supported on one in front of you or on a pillow beside "
    "you, and not on the operated side. A cushion tucked under the elbow takes the pull off the "
    "shoulder, and most people find a recliner or the corner of a sofa easier than a bed at first. "
    "A bad night is normal rather than a sign of damage.")


def _timeline(memory, understood):
    if _joint(understood) == "shoulder":
        return SHOULDER_TIMELINE_CARD
    return TIMELINE_CARD


def _implant_life(memory, understood):
    if _joint(understood) == "shoulder":
        return SHOULDER_IMPLANT_CARD
    return IMPLANT_CARD


def _soreness(memory, understood):
    if _joint(understood) == "shoulder":
        return SHOULDER_SORE_CARD
    return SORE_CARD


def _sleeping(memory, understood):
    if _joint(understood) == "shoulder":
        return SHOULDER_SLEEPING_CARD
    return SLEEPING_CARD


def _words(understood):
    if not isinstance(understood, dict):
        return set()
    found = set()
    for key in ("words", "background"):
        for word in understood.get(key) or ():
            if isinstance(word, str):
                found.add(word.lower())
    return found


def _a(word):
    return ("an " if word[:1] in "aeiou" else "a ") + word


def _joint(understood):
    words = _words(understood)
    return "shoulder" if any(word in words for word in SHOULDER) else "replacement"


NEW_JOINT_NOISE = ("click", "clicks", "clicked", "clicking", "clunk", "clunks", "clunking",
                   "pop", "pops", "popped", "popping", "grind", "grinds", "grinding",
                   "creak", "creaks", "creaking", "catch", "catches", "catching", "noisy",
                   "noise")

NEW_JOINT_CARD = (
    "Clicking, clunking or a catching feeling around a new joint is usually the soft tissue "
    "moving over the new parts, and it is common while the muscles are still settling - keep up "
    "the exercises the team gave you and mention it at your next check. Ring the ward that did "
    "the operation, or 111, the same day if the joint is hot, red or more painful than it was, "
    "if you have a fever or the wound is weeping, or if the joint gives way or you cannot put "
    "your weight on it.")

ROAD_WORDS = ("road", "roads", "street", "streets", "kerb", "kerbs", "pavement", "pavements",
              "driveway", "driveways", "tarmac", "junction", "junctions", "carriageway",
              "footpath", "footpaths", "pothole", "potholes")


def _not_a_road(understood):
    words = _words(understood)
    if not any(word in words for word in ROAD_WORDS):
        return True
    return any(word in words for word in PARTS) or any(
        word in words for word in ("hip", "knee", "shoulder", "surgeon", "operation",
                                   "physio", "hospital", "nurse", "ward", "recovery",
                                   "physiotherapy"))


A_REPLACING_A_THING = re.compile(
    r"\breplac(?:e|ing|ed)\s+(?:(?:a|an|the|my|our|your|his|her|their)\s+)?(?P<thing>[a-z]+)")
THE_JOINT_WORDS = ("hip", "knee", "shoulder", "joint", "joints", "resurfacing", "implant",
                   "implanted", "replacement", "dressing", "dressings", "bandage", "bandages",
                   "cast", "plaster")


def _not_something_else_replaced(understood):
    said = str((understood or {}).get("clean") or "") if isinstance(understood, dict) else ""
    things = A_REPLACING_A_THING.findall(said.lower())
    if not things:
        return True
    return any(word in THE_JOINT_WORDS for word in things)


def _a_replacement(*args, **kwargs):
    asked = kwargs.pop("guard", None)
    if asked is None:
        kwargs["guard"] = lambda understood: (_not_a_road(understood)
                                              and _not_something_else_replaced(understood))
    else:
        kwargs["guard"] = lambda understood: (_not_a_road(understood)
                                              and _not_something_else_replaced(understood)
                                              and asked(understood))
    return entry(*args, **kwargs)


REPLACED_JOINT = ("replacement", "replaced", "new hip", "new knee", "new joint",
                  "new shoulder", "resurfacing", "resurfaced", "hip replacement",
                  "knee replacement", "shoulder replacement", "partial knee", "total knee",
                  "total hip", "had my hip done", "had my knee done", "reverse shoulder")

SHOULDER = ("shoulder", "shoulders", "new shoulder", "shoulder replacement",
            "reverse shoulder", "reverse shoulder replacement", "resurfaced shoulder")

HIP_KNEE = ("replacement", "replaced", "new hip", "new knee", "new joint", "resurfacing",
            "resurfaced", "hip replacement", "knee replacement", "partial knee", "total knee",
            "total hip", "had my hip done", "had my knee done")

TIMELINE = ("how long", "heal", "heals", "healing", "recover", "recovery", "recovering",
            "drive", "driving", "driven", "back to work", "go back to work", "return to work",
            "swim", "swimming", "hospital",
            "nights in", "how many days", "how many weeks", "when can i", "how soon",
            "how long before", "what can i do", "weeks", "months")

TIMELINE_CARD = (
    "Walking on it the day after the operation, off the sticks at about 6 weeks, driving again "
    "at 6 weeks once you can do an emergency stop without thinking, and back to desk work at 6 "
    "to 12 weeks: hospital is usually 2 to 4 nights for a hip and 1 to 3 for a knee, and full "
    "recovery is 6 to 12 months for a hip and up to a year for a knee. "
    "Kneeling after a knee replacement is uncomfortable for most people and may never come back "
    "fully. Ring the ward or 111 if the wound starts leaking, the joint turns hot or red, or the "
    "pain suddenly gets worse.")

SORE = ("stiff", "stiffness", "stiffen", "sore", "soreness", "hurts", "hurting", "pain",
        "painful", "swollen", "swelling", "normal", "expected", "should it", "is it")

SORE_CARD = (
    "Yes - soreness and stiffness for months after a joint replacement is normal, and it eases "
    "with the exercises rather than with rest: the joint is at its stiffest in the first six "
    "weeks and keeps loosening for up to a year, and a warm, puffy knee or hip after exercise is "
    "the usual reaction to doing more. Build up slowly, ice it for 15 minutes after the exercises, "
    "and keep the daily ones going even on a bad day. Ordinary swelling is around the joint; a "
    "calf or a whole leg that swells, goes hot or is tender to touch is not ordinary swelling - "
    "ring the ward or 111 the same day, because a clot is the thing to rule out. Ring about the "
    "joint too if it is hot and red, the wound leaks, or the pain gets worse each week rather "
    "than better.")

KNEEL = ("kneel", "kneeling", "kneel down", "on my knees", "get down on the floor",
         "get up off the floor")

KNEEL_CARD = (
    "Kneeling is the one thing many people never get back after a knee replacement: the new knee "
    "can take it, but the skin over it is numb and sore against a hard floor, so most people kneel "
    "on a cushion for a few minutes at a time rather than rule it out - try it on something soft "
    "once the wound is fully healed and the swelling has gone down. After a hip replacement you "
    "can kneel, but get down on the operated knee first and keep the new hip from bending past 90 "
    "degrees for the first few months. If kneeling is for gardening or a job, ask the physio to "
    "practise it with you rather than finding out on the day.")

IMPLANT_LIFE = ("how long does it last", "how long will it last", "how long do they last",
                "last", "lasts", "lifetime", "how many years", "wear out", "worn out",
                "wears out", "need another", "second replacement", "revision", "20 years",
                "second hip replacement", "second knee replacement", "another hip replacement",
                "another knee replacement", "needs doing again", "needs redone",
                "has worn out", "gone wrong after years")

IMPLANT_CARD = (
    "A hip or knee replacement usually lasts 15 to 25 years, and about 8 in 10 are still going "
    "at 20 years; when one does wear out, a second operation to replace the worn parts is a "
    "routine job - smaller than the first, with a similar recovery. It is not a countdown: "
    "weight, activity and the wear on it decide, so the muscles kept strong and a healthy weight "
    "are what buy the time. If a joint that has been fine for years starts to ache, grind or "
    "give way, that is worth an X-ray rather than waiting.")


WASH = ("shower", "showers", "bath", "baths", "washing", "wash", "get it wet", "get it wet",
        "wound", "wounds", "dressing", "dressings", "stitches", "staples", "scar", "scars",
        "waterproof", "sealed", "healed over")

WASH_CARD = (
    "A shower is usually fine once the dressing is off and the wound is dry and sealed, and most "
    "wards send people home with a waterproof dressing so it can happen sooner - but a bath, a "
    "hot tub or a swim waits until the wound is fully closed, around two to six weeks, because "
    "standing water is where infection gets in. Pat the wound dry rather than rubbing it, leave "
    "it open to the air when you can, and put nothing on it - no creams, oils or powders. Ring "
    "the ward or 111 if the wound turns hot or red, leaks or smells, or the edges start to open.")

STAIRS = ("stairs", "stair", "upstairs", "downstairs", "steps", "flight of stairs")

STAIRS_CARD = (
    "Stairs are fine from the day you get home, one stair at a time with a rail and the crutches "
    "in the other hand: the good leg goes up first and the operated leg comes down first - up "
    "with the good, down with the bad - and both feet land on each step rather than one leg per "
    "stair. Sit down on the bottom step to put the sticks and slippers on rather than bending. If "
    "you live alone and the stairs are steep, ask the ward to watch you do a flight before you go "
    "home; it is a normal part of the discharge check.")

SLEEPING = ("sleep", "sleeping", "slept", "lie on", "lying on", "lie down", "on my side",
            "side to sleep", "in bed")

SLEEPING_CARD = (
    "Sleep is the awkward part for the first few weeks, and the answer depends on the joint: "
    "after a hip, sleep on your back with a pillow between the knees, or on the unoperated side "
    "with the pillow still between the knees so the new hip cannot cross the middle - keep that "
    "up for the six weeks the ward tells you. After a knee, sleep on your back with the leg "
    "straight on a pillow, or on the good side with a pillow under the new knee. A pillow under "
    "the heels stops the sheet rubbing, and a bad night is normal rather than a sign of damage.")

SCAR = ("scar", "scars", "numb", "numbness", "no feeling", "lost feeling", "pins and needles",
        "tingling", "tingles", "itchy", "itches", "itching", "dead patch")

SCAR_CARD = (
    "A numb patch of skin around the scar is normal after a joint replacement and it often stays "
    "that way: the small nerves under the incision are cut on the way in, so the skin there feels "
    "wooden, tingly or dead to touch, and it usually softens over a year or two rather than "
    "meaning anything about the joint. An itchy scar is the same story - healing nerves - and so "
    "is a scar that pulls or feels tight. A scar that turns hot, red, weepy or spreads, or "
    "numbness that comes on suddenly or spreads up the leg, is the one to ring the ward or 111 "
    "about, the same day.")

LOOSE = ("feels loose", "feel loose", "loose", "wobble", "wobbles", "wobbly",
         "gives way", "give way", "giving way", "gave way", "gives out", "unstable",
         "not stable", "pops out")

SWOLLEN_LEG = ("leg is swollen", "leg swollen", "leg has swollen", "swollen leg",
               "leg is puffy", "puffy leg", "leg has puffed", "calf is swollen", "swollen calf",
               "calf hurts", "calf is sore", "calf is tender", "my calf", "leg went big",
               "leg swelled up", "leg is tight")

SWOLLEN_LEG_CARD = (
    "A leg that swells after a hip or knee replacement is not ordinary swelling and it is worth a "
    "phone call rather than a wait: a calf that is hot, tight, red or tender, or a whole leg that "
    "swells up, can be a clot, and clots are more common in the weeks after this operation than "
    "people expect - ring the ward that did the operation or 111 and say when the swelling "
    "started. If you are also short of breath, coughing or feeling faint, that is 999. Swelling "
    "around the joint itself is the ordinary sort, and that one goes down with ice and the leg "
    "raised.")

LOOSE_CARD = (
    "A new joint that feels loose, gives way or clunks hard when you put weight on it is one to "
    "have looked at rather than wait for the next appointment: ring the ward or your surgeon's "
    "team and tell them when it started and what it does. Sometimes it is weak muscle around a "
    "joint that is fine - the physio can tell you that in one visit - and sometimes the parts "
    "need checking, which is why it is a phone call rather than a wait. If it gives way and you "
    "fall, or the joint is hot and red with it, treat that as urgent: 111 the same day.")

def _noisy_joint(memory, understood):
    words = _words(understood)
    part = next((ONE.get(word, word) for word in PARTS if word in words), "joint")
    return (_a(part).capitalize() + " that clicks or pops and does not hurt is almost always harmless: a "
            "tendon flicking over a bump, or gas coming out of the joint fluid, and it needs "
            "nothing doing. Keep the muscles around it working, because clicking that turns "
            "into pain is usually a strength problem rather than the noise. If it starts to "
            "hurt, swell or lock, have a physio or your GP look at it.")


ENTRIES = [
    entry("noisy-joint", (NOISY, PARTS), _noisy_joint, avoid=AVOID + HURTS),
    _a_replacement("replaced-joint-noise", (REPLACED_JOINT, NEW_JOINT_NOISE), NEW_JOINT_CARD, bias=2,
          avoid=("hot", "red", "fever", "temperature", "wound", "weeping", "oozing", "pus",
                 "infection", "infected", "dislocated", "dislocate", "popped out",
                 "out of place", "fell", "fallen", "fall", "broke", "broken", "fracture",
                 "torn", "tore", "numb", "numbness", "tingling", "pins and needles",
                 "dog", "cat", "puppy")),
    _a_replacement("joint-implant-life", (REPLACED_JOINT, IMPLANT_LIFE), _implant_life, bias=2),
    _a_replacement("joint-kneeling", (REPLACED_JOINT, KNEEL), KNEEL_CARD, bias=2,
          avoid=("pray", "praying", "church", "garden", "weed", "weeds", "weeding")),
    _a_replacement("joint-replacement-timeline", (REPLACED_JOINT, TIMELINE), _timeline, bias=1,
          avoid=("cost", "costs", "private", "how much does", "how much is", "nhs waiting",
                 "waiting list", "dislocated", "dislocate", "popped out", "out of place",
                 "broke", "broken", "fracture", "fractured", "infected", "infection",
                 "hot and red", "red and hot", "pus", "oozing", "kneel", "kneeling",
                 "shower", "bath", "wound", "dressing", "stairs", "upstairs", "downstairs",
                 "sleep", "sleeping", "side",
                 "licence", "license", "passport", "photocard", "document", "documents",
                 "battery", "batteries", "phone", "laptop", "screen", "remote",
                 "bulb", "bulbs", "fuse", "fuses", "filter", "filters", "part", "parts",
                 "spare", "tyre", "tyres", "tire", "tires", "wheel", "wheels",
                 "boiler", "radiator", "washer", "washing machine", "dishwasher",
                 "fridge", "freezer", "oven", "kettle", "toaster", "door", "lock",
                 "handle", "zip", "zipper", "button", "buttons", "strap", "strap on",
                 "tile", "tiles", "roof", "fence", "key", "keys", "card", "cards")),
    _a_replacement("joint-replacement-washing", (REPLACED_JOINT, WASH), WASH_CARD, bias=2,
          avoid=("hot and red", "red and hot", "oozing", "pus", "smelly", "infected",
                 "infection", "fever", "temperature", "numb", "numbness", "no feeling",
                 "pins and needles", "tingling", "itches", "itching", "itchy",
                 "sore", "hurts", "hurting", "pain", "painful")),
    _a_replacement("joint-replacement-scar", (REPLACED_JOINT, SCAR), SCAR_CARD, bias=2,
          avoid=("hot and red", "red and hot", "oozing", "pus", "smelly", "infected",
                 "infection", "fever", "temperature", "weeping")),
    _a_replacement("joint-replacement-stairs", (HIP_KNEE, STAIRS), STAIRS_CARD, bias=2,
          avoid=("click", "clicks", "clicking", "clunk", "clunks", "clunking", "grind",
                 "grinds", "grinding", "creak", "creaks", "catch", "catches", "catch",
                 "pop", "pops", "loose", "wobble", "wobbly", "gives way", "giving way",
                 "hurt", "hurts", "hurting", "pain", "painful", "sore", "swollen",
                 "ache", "aches", "aching",
                 "shoulder", "shoulders", "arm", "elbow", "wrist", "hand")),
    _a_replacement("joint-replacement-sleeping", (REPLACED_JOINT, SLEEPING), _sleeping, bias=2),
    _a_replacement("joint-replacement-loose", (REPLACED_JOINT, LOOSE), LOOSE_CARD, bias=2,
          avoid=("hot and red", "red and hot", "dislocated", "popped out", "broke", "broken",
                 "fracture")),
    _a_replacement("joint-replacement-swollen-leg", (HIP_KNEE, SWOLLEN_LEG), SWOLLEN_LEG_CARD,
          bias=2),
    _a_replacement("joint-replacement-soreness", (REPLACED_JOINT, SORE), _soreness,
          avoid=("dislocated", "dislocate", "popped out", "out of place", "broke", "broken",
                 "fracture", "infected", "infection", "hot and red", "red and hot", "pus",
                 "oozing", "fever", "temperature",
                 "worth replacing", "worth repairing", "worth fixing", "repair or replace",
                 "fix or replace", "replace it", "replace the", "replacing it")),
]


LOCKED = ("locks", "locked", "locking", "lock up", "locks up", "locked up", "locking up",
          "catches", "catching", "caught on", "gets stuck", "get stuck", "got stuck",
          "will not straighten", "wont straighten", "cannot straighten", "cant straighten",
          "will not bend", "wont bend", "cannot bend", "cant bend", "jams", "jammed",
          "jamming", "in a locked")

LOCK_PARTS = PARTS + ("knee", "knees", "kneecap", "leg", "legs", "thumb", "hand", "hands")

TRIGGER_FINGER_CARD = (
    "A finger that locks or clicks and then catches as it straightens is trigger finger: the "
    "tendon that bends the finger runs through a sheath, the sheath swells, and the tendon has to "
    "jump through the tight spot - which is why it locks bent and then lets go with a click. "
    "Rest it from hard gripping for a few weeks, keep it straight at night with a finger splint "
    "from a chemist, and take ibuprofen if it is sore. See your GP if it stays locked, keeps "
    "locking during the day, or a second finger starts: a steroid injection into the sheath "
    "usually sorts it, and a small operation does if it does not.")

LOCKED_CARD = (
    "A {part} that locks, catches or will not straighten has something physically in the way, so "
    "it is worth being examined this week rather than waiting for it to settle: ring your GP and "
    "say which movement brings it on, whether it lets go on its own, and whether there was a twist "
    "or a knock before it started. A knee that locks is usually a torn cartilage or a loose piece "
    "of it catching in the joint, which a physio or doctor can tell apart by hand in one "
    "appointment, so keep off twisting sports and deep squats until then rather than testing it. "
    "Go to 111 the same day if the joint swells up, is hot, or you cannot put weight on it at all.")


def _locked_joint(memory, understood):
    words = _words(understood)
    part = next((ONE.get(word, word) for word in LOCK_PARTS if word in words), "joint")
    if part in ("finger", "fingers", "thumb", "thumbs"):
        return TRIGGER_FINGER_CARD
    return LOCKED_CARD.format(part=part)


ENTRIES.append(
    entry("locked-joint", (LOCKED, LOCK_PARTS), _locked_joint,
          avoid=("how do i lock", "lock out", "lock my knee", "lock your knee", "locking out",
                 "lock the knee", "jaw", "jaws", "jaw joint", "tmj", "dog", "cat", "door",
                 "doors", "gate",
                 "car", "cars", "bike", "bicycle", "phone", "laptop", "computer", "screen",
                 "window", "windows", "cupboard", "cupboards", "drawer", "drawers"),
          bias=2))
