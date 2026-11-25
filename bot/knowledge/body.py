
import re
import string

from .lookup import ASK_ABOUT, RING_AS_A_CALL, entry
from ..understanding.kinds import OTHER_PEOPLE, PERSON_NOUNS

TEMPERATURE_WORDS = frozenset((
    "temperature", "temperatures", "temp", "temps", "fever", "feverish", "fevered"))
WE_OUR_OURS = frozenset(("we", "us", "our", "ours"))
POSSESSIVE_OF_A_PERSON = frozenset(("my", "his", "her", "their", "our", "your"))
THING_AFTER_THE_WORD = frozenset((
    "probe", "probes", "thermometer", "thermometers", "gauge", "gauges", "gage", "gages",
    "sensor", "sensors", "dial", "dials", "knob", "knobs", "setting", "settings",
    "control", "controls", "thermostat", "thermostats", "stat"))


_WORKSHOP_NOUNS = (
    "wood", "wooden", "plank", "planks", "planking", "joist", "joists", "batten", "battens",
    "floorboard", "floorboards", "skirting", "moulding", "molding", "fence", "fencing", "gate",
    "shed", "decking", "worktop", "shelf", "shelves", "shelving", "cabinet", "wardrobe",
    "wall", "walls", "brick", "bricks", "plasterboard", "stud wall",
    "stud", "studs", "mirror", "mirrors", "bracket", "brackets", "picture", "pictures",
    "concrete", "masonry", "tile", "tiles", "block wall", "stone wall", "curtain rail",
    "curtain pole", "anchor", "anchors", "hollow wall", "cavity wall",
    "picture hook",
    "picture hooks", "picture frame", "hanging a picture", "hang a picture", "hang the picture",
    "hammer", "hammers", "hammering", "drill", "drills", "drilling", "screw", "screws",
    "screwed", "screwing", "rawlplug", "rawlplugs", "wall plug", "wall plugs", "carpentry",
    "diy", "doorframe", "door frame",
    "tyre", "tyres", "tire", "tires", "wheel", "wheels", "puncture", "punctured",
)
_WORKSHOP = re.compile(r"\b(?:" + "|".join(re.escape(word) for word in _WORKSHOP_NOUNS) + r")\b")


def _the_nail_is_a_persons(understood):
    reading = understood if isinstance(understood, dict) else {}
    said = str(reading.get("clean") or "").lower()
    if not said:
        words = reading.get("words") or ()
        said = " ".join(str(word) for word in words).lower()
    if "nail" not in said:
        return True
    return not _WORKSHOP.search(said)


def _the_part_is_a_persons(understood):
    return not _a_thing_owns_the_part(understood)


def the_body_is_the_persons(understood):
    if str((understood or {}).get("state_owner") or "") == "other":
        return False
    words = set((understood or {}).get("words") or ())
    if words & _THE_PERSONS_OWN_WORDS:
        return True
    return not (words & _SOMEONE_ELSE)


_CANNOT_USE_IT = re.compile(
    r"\b(?:can'?t|can ?not|couldn'?t|could ?not|unable to|not able to)\s+"
    r"(?:walk|stand|put|bear|weight|move|straighten|bend|use|lift|raise|reach)\b"
    r"|\b(?:put|bear)\s+(?:my\s+)?weight\b"
    r"|\b(?:gave|gives|giving) way\b")


def the_part_that_keeps_grumbling(understood):
    return the_body_is_the_persons(understood) and not _CANNOT_USE_IT.search(
        str((understood or {}).get("clean") or (understood or {}).get("text") or "").lower())


_THE_PERSONS_OWN_WORDS = frozenset(("i", "im", "i'm", "me", "my", "mine", "myself", "ive",
                                    "i've"))
_SOMEONE_ELSE = frozenset(("he", "hes", "he's", "she", "shes", "she's", "him", "her", "his",
                           "hers", "they", "theirs", "their", "them"))
_WEEKS_ALONG = re.compile(
    r"\b(?:im|i'?m|i am|am)\s+(?:about\s+|nearly\s+|almost\s+|just\s+|only\s+)?"
    r"\d{1,2}\s*(?:weeks?|wks?)\b"
    r"|\b\d{1,2}\s*(?:weeks?|wks?)\s+(?:pregnant|gone|along|in)\b"
    r"|\bweeks (?:gone|along)\b")


_SWELLING = re.compile(r"\b(?:swollen|swelling|swelled|swell|swells|puffy|puffiness"
                       r"|water retention|retaining water|fluid)\b")


_PREGNANCY_WORDS = ("pregnant", "pregnancy", "expecting", "weeks pregnant", "weeks gone",
                    "trimester", "my bump", "having a baby", "midwife", "due in", "due date")


def _names_a_pregnancy(understood):
    reading = understood if isinstance(understood, dict) else {}
    line = " ".join(str(reading.get("clean") or reading.get("text") or "").lower().split())
    return any(word in line for word in _PREGNANCY_WORDS)


def _dates_a_pregnancy_in_weeks(understood):
    reading = understood if isinstance(understood, dict) else {}
    line = " ".join(str(reading.get("clean") or reading.get("text") or "").lower().split())
    return _a_figure_in_weeks(line)


def _a_figure_in_weeks(words):
    line = (words or "").lower()
    return bool(_WEEKS_ALONG.search(line)) and bool(_SWELLING.search(line))


_PREGNANCY_SWELLING = ("swollen", "swelling", "swelled", "swell up", "swells", "swell",
                       "water retention", "retaining water")
_PREGNANCY_SWELLING_PARTS = ("ankles", "ankle", "feet", "foot", "legs", "leg", "toes", "toe",
                             "calves", "calf", "hands", "hand", "fingers", "finger")
_PREGNANCY_SWELLING_AVOID = (
    "sprain", "sprained", "twisted", "broke", "broken", "fell", "fall",
    "bandage", "crutches", "ibuprofen", "paracetamol", "painkiller", "painkillers",
    "overdose", "took too much", "allergic", "dog", "cat",
    "are fine", "is fine", "not swollen", "no swelling", "isnt swollen",
    "arent swollen", "no swelling at all", "nothing swollen",
    "not pregnant", "isnt pregnant", "no longer pregnant",
    "not expecting", "not been pregnant")

_PREGNANCY_SWELLING_REPLY = (
    "Swollen feet and ankles are ordinary in the last months: the extra blood and the weight "
    "of the bump slow the fluid back up your legs. Put your feet up above hip height for "
    "twenty minutes a few times a day, keep walking, wear the support tights, and drink "
    "normally rather than less. Ring your midwife the same day if it comes on over a day or "
    "two, if one ankle or one leg swells on its own, if a leg is hot or sore, or if you have "
    "a bad headache, blurry vision or swelling in your face or hands.")



def a_persons_temperature(understood):
    if not isinstance(understood, dict):
        return False
    words = [str(word).lower().strip(string.punctuation)
             for word in (understood.get("words") or ())]
    if any(one in TEMPERATURE_WORDS and other in THING_AFTER_THE_WORD
           for one, other in zip(words, words[1:])):
        return False
    if understood.get("body") == "temperature":
        return True
    if not any(word in TEMPERATURE_WORDS for word in words):
        return False
    if any(word in OTHER_PEOPLE or word in WE_OUR_OURS for word in words):
        return True
    return any(one in POSSESSIVE_OF_A_PERSON and other in TEMPERATURE_WORDS
               for one, other in zip(words, words[1:]))


def the_stomach_is_what_it_is_about(understood):
    return isinstance(understood, dict) and bool(
        understood.get("body") == "stomach" or understood.get("own_output") is not None)

HURT = ("hurt", "hurts", "hurting", "ache", "aches", "aching", "achy", "pain", "pains",
        "painful", "sore", "stiff", "killing me", "kills", "twinge", "twinges", "throbbing",
        "agony", "soreness",
        "thumping", "thumps", "pounding", "pounds",
        "playing up", "playing me up", "acts up", "acting up", "giving me jip", "giving me gyp",
        "giving me grief", "gives me jip", "gives me gyp", "gives me grief",
        "sprain", "sprained", "sprains", "strain", "strained", "strains", "twisted", "tweak",
        "tweaked", "pulled a muscle", "pulled my", "torn", "went over on", "rolled", "pulled", "tore", "ripped",
        "injured", "injury", "injuries", "done my", "did my", "done in", "did in",
        "put my back out", "put my shoulder out", "put my knee out",
        "a joke", "in bits", "wrecked", "banjaxed", "a nightmare", "torture", "is at me",
        "in a state", "a state", "hanging off me", "in agony", "giving me trouble",
        "because of my", "because of her", "because of his")

_OTHER_PEOPLE = ("my son", "my daughter", "my child", "my kid", "my kids", "my baby",
                 "my toddler", "my husband", "my wife", "my partner", "my mum", "my mom",
                 "my mother", "my dad", "my father", "my friend", "my dog", "my cat",
                 "my puppy", "my horse", "the dog", "the cat")
_PARTS = ("arm", "leg", "back", "knee", "foot", "feet", "hand", "shoulder", "neck", "hip",
          "ankle", "wrist", "elbow")
THIRD_PARTY = _OTHER_PEOPLE + tuple("%s %s" % (who, part) for who in ("his", "her")
                                    for part in _PARTS)

STANDING = ("for a week", "for two weeks", "for a fortnight", "for weeks", "for a month",
            "for months", "for ages", "weeks", "months", "a week now", "two weeks",
            "three weeks", "a few weeks")

FALL = ("fall", "a fall", "after a fall", "from a fall", "banged", "knocked", "bump", "bumped")

DECIDE = ("see someone", "see a doctor", "see the doctor", "see a gp", "go to the doctor",
          "should i see", "do i need to see", "or wait", "see a physio", "worth seeing",
          "get it looked at", "should i get it checked")

RED_FLAG = ("cant pee", "can't pee", "cannot pee", "cant wee", "can't wee", "cant pass urine",
            "can't pass urine", "cant pass water", "no urine", "cant urinate", "can't urinate",
            "cannot urinate", "numb", "numbness", "pins and needles", "cant feel my legs",
            "can't feel my legs", "cant feel my feet", "cant feel my foot", "legs give way",
            "leg gave way", "incontinent", "lost control of my bladder", "saddle",
            "hurts when i breathe", "hurts to breathe", "pain when i breathe",
            "worse at night", "wakes me at night", "wake me at night", "wakes me up",
            "woke me up", "hot and swollen", "swollen and hot", "swollen calf", "swollen leg",
            "hot calf", "red and hot", "after a flight", "after a long flight")
_SORE_ANYWHERE = ("back", "leg", "legs", "calf", "calves", "thigh", "shin", "arm", "arms",
                  "hip", "knee", "foot", "feet", "spine", "side", "shoulder", "neck",
                  "ankle", "wrist", "elbow", "hand", "pain", "pains", "hurts", "hurting",
                  "ache", "aches", "aching", "achey",
                  "ankles", "knees", "hands", "thighs", "shins", "hips", "wrists", "elbows",
                  "shoulders", "toes", "fingers", "thumbs", "heels")

EXERCISE_DAY = ("gym", "workout", "work out", "exercised", "weights", "next day", "day after")

MEDICINE = ("ibuprofen", "ibruprofen", "ibuprofin", "nurofen", "brufen", "painkiller",
            "painkillers", "pain killer", "pain killers")
_NOT_A_BODY_PART = (
    "hand luggage", "hand bag", "handbag", "hand luggage only", "hand cream", "hand wash",
    "hand soap", "hand sanitiser", "hand sanitizer", "hand dryer", "hand towel", "hand brake",
    "hand held", "handheld", "first hand", "second hand", "secondhand", "second-hand",
    "on the other hand", "helping hand", "hand me", "hand in hand", "hand made", "handmade",
    "hand whisk", "hand mixer", "hand warmer", "hand rail", "handrail", "hand print",
    "handwriting", "handwriting", "hands on",
    "back garden", "back door", "back seat", "back pay", "back up", "cashback", "back to school",
    "back of the car", "back page",
    "back of the fridge", "back of my throat", "in the back of",
    "on foot", "foot of the stairs", "foot of the bed", "foot of the garden", "six foot",
    "five foot", "foot long", "at the foot of",
    "arm chair", "armchair", "arm of the sofa", "arm of the chair", "leg of the table",
    "leg of the chair", "table leg", "chair leg", "door handle", "knee deep", "hip flask",
)

AVOID = ("chest", "heart", "throat", "tooth", "teeth", "gum", "gums", "ear", "ears",
         "stomach", "tummy", "belly", "period", "pregnant", "pregnancy", "jaw",
         "sick", "nauseous", "vomit", "dizzy", "faint", "breathless", "sweating",
         "smell", "smells", "smelly", "stink", "stinks", "stinking", "odour", "odor",
         "sweaty", "sweat", "mole", "moles", "rash", "rashes", "spot", "spots",
         "blister", "blisters", "wart", "warts", "bruise", "bruises", "birthmark",
         "ingrown", "athletes foot",
         "when its cold", "when it's cold", "when it is cold", "in the cold", "in this cold",
         "cold weather", "cold and damp", "when it rains", "when it rained", "in the rain",
         "when its damp", "when it's damp", "damp weather", "when the weather",
         "weather changes", "in the winter", "in winter", "before rain", "before it rains",
         ) + _NOT_A_BODY_PART + EXERCISE_DAY + STANDING + THIRD_PARTY + DECIDE + FALL + RED_FLAG + MEDICINE

REGIONS = (
    ("back", ("back", "lower back", "spine", "backache"),
     "Most back pain is muscular and settles in two to six weeks, and staying active is what "
     "helps most: keep walking and carry on with your usual jobs as far as you can rather than "
     "taking to your bed, and take paracetamol or ibuprofen if you can. See a GP if it is no "
     "better in a fortnight, or today if you cannot pass urine, have numbness between your legs, "
     "or it came on after a fall."),
    ("knee", ("knee", "kneecap"),
     "A sore knee is usually a strain or the kneecap tracking badly: ease off running, stairs and "
     "kneeling, ice it for 20 minutes at a time with a cloth round it for the first two days, then "
     "keep it moving gently. Get it looked at if it gives way, locks, or you cannot put your "
     "weight on it."),
    ("shoulder", ("shoulder", "shoulders", "shoulder blade", "rotator cuff"),
     "Most shoulder pain is a strained or trapped tendon, worse when you reach overhead or lie on "
     "that side: keep using the arm as far as is comfortable, warm it before you use it, and do "
     "the pendulum swing (lean forward, let the arm hang, circle it slowly) a few times a day. See "
     "a GP if you cannot lift the arm at all or it started after a fall."),
    ("neck", ("neck", "stiff neck"),
     "A stiff neck is usually muscular, from posture or sleeping awkwardly: heat, gentle stretches "
     "and a look at your screen height help, and a soft collar for a day or two is fine but not "
     "longer, because the muscles need to work. Get seen the same day if it comes with a fever, a "
     "bad headache, or light hurting your eyes."),
    ("hip", ("hip", "hips"),
     "Hip pain in an adult is usually the joint or the tendon over the outside of the hip bone: "
     "keep walking as far as is comfortable, sit with your knees lower than your hips, and take a "
     "painkiller before a walk rather than after. See a GP if it hurts when you are resting or at "
     "night, or you have started to limp."),
    ("ankle", ("ankle", "ankles"),
     "An ankle sprain wants ice for 20 minutes at a time for the first two days, a support wrap "
     "and the foot up when you sit, then gentle movement and a slow return to walking on it. Most "
     "settle in two to six weeks, and the swelling can take months. Get it looked at the same day "
     "if you cannot put any weight on it, it swells badly, or it looks crooked."),
    ("foot", ("foot", "feet", "heel", "heels", "arch", "plantar"),
     "Foot pain is often the plantar fascia, the band under the arch, worst on your first steps in "
     "the morning: stretch the calf against a wall before you stand up, roll the arch on a cold "
     "bottle, and wear shoes with a firm sole indoors too. A heel that hurts all day, or a foot "
     "that is red and hot, needs looking at."),
    ("wrist", ("wrist", "wrists", "hand", "hands", "thumb", "fingers"),
     "Wrist and hand pain is usually an overused tendon or a nerve pressed by the way you grip and "
     "type: take breaks, keep the wrist straight rather than bent, and try a support splint from "
     "the pharmacy at night. Pins and needles in the fingers that wake you is worth a GP visit."),
    ("elbow", ("elbow", "elbows", "tennis elbow"),
     "Elbow pain on the outside is tennis elbow, an overused tendon, and it settles over weeks to "
     "months once you rest from the gripping and lifting that sets it off: a strap just below the "
     "elbow and slow strengthening with a light weight help. See a GP if it is no better in six "
     "weeks."),
    ("arm", ("arm", "arms", "upper arm", "forearm"),
     "Most arm pain is a muscle strain or the ache a day after lifting, and some of it comes down "
     "from a sore shoulder or elbow: keep using it as far as is comfortable and take a painkiller if you "
     "can. See a GP if the arm is weak or numb, and treat a heavy left arm with tightness in the "
     "chest, sweating or breathlessness as an emergency."),
    ("ribs", ("rib", "ribs", "ribcage", "rib cage", "ribs hurt"),
     "A rib that hurts when you breathe in, cough or press it is usually bruised, not broken, and "
     "it mends the same way either way: keep breathing normally rather than in shallow sips, take "
     "paracetamol or ibuprofen, and press a cushion against that side when you cough. It eases "
     "over three to six weeks. Get seen the same day if you are breathless or coughing blood."),
    ("tailbone", ("tailbone", "tail bone", "coccyx", "sacrum"),
     "A sore tailbone is usually a knock from a fall or hours sitting on a hard chair, and it "
     "mends slowly - a few weeks, sometimes a couple of months. Sit on a soft or doughnut "
     "cushion, tilt forward a little rather than leaning back onto it, and take paracetamol or "
     "ibuprofen; a warm bath helps the muscles around it. See a GP if it is no better after a "
     "few weeks, or if there is numbness or bleeding."),
    ("toe", ("toe", "toes", "big toe"),
     "Most toe pain is a stub, a bruise under the nail or an ingrown edge: soak it in warm salty "
     "water, wear shoes with room in them and take paracetamol. A big toe that goes red, hot and "
     "swollen overnight, often at night, is gout - that one wants seeing this week, and sooner if "
     "you have diabetes and it looks infected."),
    ("collarbone", ("collarbone", "collar bone", "clavicle"),
     "A collarbone that hurts after a knock usually mends in a sling over four to six weeks, and "
     "the pain often eases before the bone has joined: keep the hand and elbow moving gently, "
     "sleep propped up a little and take paracetamol. Have it looked at with an X-ray if you "
     "cannot lift the arm, the bone looks out of line, or it hurts too much to sleep."),
    ("groin", ("groin", "adductor"),
     "A sore groin is usually a pulled muscle from twisting, kicking or turning quickly: give "
     "the sport that set it off a fortnight off, ice it for 20 minutes at a time for the first "
     "two days, then stretch and strengthen gently. Get a lump or a bulge that appears when you "
     "cough or lift looked at - that is a hernia - and get a sudden severe pain in one side "
     "seen the same day."),
    ("leg", ("leg", "legs", "calf", "calves", "thigh", "thighs", "hamstring", "shin"),
     "A pulled thigh or calf muscle, or the ache that lands a day after squats, wants the same "
     "start: rest it, ice it for 20 minutes at a time for two days, then gentle stretching and a "
     "slow return to what you were doing, with the leg kept up when you sit. Calf pain with a hot, "
     "swollen leg, or a shin that hurts to touch after a knock, needs looking at."),
)


EXTRA_AVOID = {
    "wrist": ("i fell", "fell over", "fell on", "fell down", "fell off", "fell and", "tripped",
              "slipped", "landed on my", "banged it", "knocked it", "crushed"),
    "arm": ("i fell", "fell over", "fell on", "fell down", "fell off", "fell and", "tripped",
            "slipped", "landed on my", "banged it", "knocked it", "crushed"),
    "leg": ("swollen", "swelling", "hot", "flight", "long sit", "red", "tender", "warm",
            "shin", "shins"),
    "back": tuple("back of %s %s" % (whose, part) for whose in ("my", "the", "your")
                  for part in ("knee", "knees", "neck", "throat", "hand", "hands", "ankle",
                               "calf", "heel", "head", "shin", "elbow", "wrist", "foot")) + (
        "bad back", "a bad back", "gives trouble", "on and off",
        "gardening", "after gardening", "digging", "after a day of lifting", "lifting",),
    "knee": ("stairs", "stair", "staircase", "steps", "climb", "climbing", "downstairs",
             "upstairs", "up steps", "down steps",
             "click", "clicks", "clicking", "creak", "creaks", "creaking", "grind",
             "grinding", "noise", "noisy", "popping", "crack", "cracks", "cracking"),
}

JOINTS = ("knee", "knees", "ankle", "ankles", "wrist", "wrists", "elbow", "elbows",
          "hip", "hips", "shoulder", "shoulders", "foot", "feet", "toe", "toes",
          "thumb", "thumbs", "joint", "joints")

HOT_SWELLING = ("swollen", "swelling", "swelled", "puffy", "hot", "red", "inflamed")

SEE_TODAY_BACK_AND_CALF = (
    "That is worth being seen today rather than waiting for it to settle. Pain in the back "
    "or side that hurts when you breathe, pain that wakes you at night, or a calf that is hot "
    "and swollen - especially after a flight or a long sit - are the shapes a doctor wants "
    "to look at the same day: ring 111 or your GP this morning. Go to A&E if your chest "
    "hurts suddenly or you are short of breath.")


CLOT_AND_CHEST = ("leg", "legs", "calf", "calves", "thigh", "thighs", "shin", "shins",
                  "back", "side", "spine", "rib", "ribs")

HOT_FLAGS = ("hot", "red", "inflamed", "burning", "went red", "gone red")


def _see_today(memory, understood):
    words = _words(understood)
    part = _part_named(words, understood)
    if not part or part in CLOT_AND_CHEST:
        return SEE_TODAY_BACK_AND_CALF
    if words & set(HOT_FLAGS):
        return ("A " + part + " that has gone hot and swollen wants looking at today rather "
                "than iced and waited on: ring 111 this morning, and go to A&E if there is a "
                "fever with it or you cannot put weight on it at all.")
    return ("A swollen " + part + " is usually fluid - from a knock or overuse, or from a tablet "
            "or the heart when it is on both sides - so have it looked at this week and keep it "
            "raised when you sit. Ring 111 today if it is hot, red and spreading, or painful on "
            "just one side.")


PART_ONE = {"feet": "foot", "calves": "calf", "thighs": "thigh", "shins": "shin", "hands": "hand",
            "ribs": "rib", "ribs hurt": "rib", "tail bone": "tailbone", "big toe": "toe",
            "collar bone": "collarbone",
            "fingers": "finger", "thumbs": "thumb", "heels": "heel", "toes": "toe",
            "knees": "knee", "ankles": "ankle", "elbows": "elbow", "wrists": "wrist",
            "shoulders": "shoulder", "hips": "hip", "legs": "leg", "arms": "arm"}


def _part_named(words, understood=None):
    if understood is not None and "back" in words and not _the_back_is_a_back(understood):
        words = set(words) - {"back"}
    for _name, spelled, _reply in REGIONS:
        for word in spelled:
            if word in words:
                return PART_ONE.get(word, word)
    for part in JOINTS:
        if part in words:
            return PART_ONE.get(part, part)
    return ""


LOWER_HALF = ("leg", "legs", "calf", "calves", "thigh", "thighs", "shin", "shins", "groin",
              "saddle", "bottom", "bum", "backside", "butt", "buttocks", "crotch",
              "genitals", "knickers", "undercarriage", "between my legs", "down there",
              "hips", "bladder", "wee", "wees", "peed", "pee", "urine", "urinate",
              "toilet", "catheter", "bowels", "waterworks")

SOMEWHERE_ELSE = ("arm", "arms", "hand", "hands", "finger", "fingers", "thumb", "thumbs",
                  "wrist", "wrists", "elbow", "elbows", "shoulder", "shoulders", "neck",
                  "tongue", "face", "cheek", "jaw", "head", "foot", "feet", "toe", "toes")

BACK_NAMES = ("back", "backs", "backache", "back ache", "spine", "spinal", "lower back",
              "slipped disc", "sciatica", "my back")
NUMB_ANYWHERE = ("numb", "numbness", "pins and needles", "tingling", "no feeling",
                 "lost feeling", "no sensation", "cant feel", "gone numb", "went numb",
                 "dead", "asleep")
NUMB_LOWER = ("foot", "feet", "toe", "toes", "sole", "soles", "heel", "heels", "ankle",
              "ankles", "leg", "legs", "calf", "calves", "thigh", "thighs", "shin", "shins",
              "hip", "hips", "buttock", "buttocks", "bottom", "bum", "backside", "groin",
              "saddle", "between my legs", "down there")
SPELLED_OUT = ("cant feel my feet", "cant feel my foot", "cant feel my toes",
               "cant feel my legs", "cant feel my leg")

SADDLE_PARTS = ("saddle", "saddle area", "saddle region",
                "groin", "genitals", "crotch", "undercarriage", "down there")
FLAG_WITH_IT = ("back", "backs", "leg", "legs", "calf", "calves", "thigh", "thighs", "shin",
                "shins", "spine", "both legs", "hips", "hip", "give way", "gave way",
                "cant pee", "cant wee", "cant pass urine", "cant go for a wee",
                "cant go for a pee", "cant go to the toilet", "cant do a wee", "bladder",
                "bowels", "incontinent", "no urine", "wetting myself", "ache", "aching",
                "pain", "pains", "hurts", "hurting", "sore", "hurts to", "both sides")

SADDLE_CARD = (
    "Numbness between the legs, in the saddle area or the groin, is usually pressure on the "
    "nerves there: a bike saddle, a long sit, tight jeans or a wallet in a back pocket. It "
    "lifts within an hour of standing up. Shorten the rides and the sits, stand up every 20 "
    "minutes, and set the bike saddle level and not too high. If it has not gone by the next "
    "day, or it comes with back pain, "
    "numbness down both legs, or any trouble weeing or opening your bowels, ring 111 the same "
    "day and say \"numbness in the saddle area\" - do not wait for that one to settle.")

RED_FLAG_CARD = (
    "Do not wait on that one. A sore back with no urine coming, numbness or pins and "
    "needles between your legs or in your feet, or a leg that gives way is the one back "
    "problem that has to be seen the same day: ring 999 or go to A&E now, and do not drive "
    "yourself. If you are not sure, ring 111 and say those words to them.")


def _names(text, words):
    for word in words:
        if " " + word + " " in text:
            return True
    return False


def _red_flag(memory, understood):
    if not isinstance(understood, dict):
        return RED_FLAG_CARD
    said = str(understood.get("text") or "").lower().replace("\u2019", "").replace("'", "")
    text = " " + re.sub(r"[^a-z]+", " ", said) + " "
    for key in ("words", "background"):
        for word in understood.get(key) or ():
            if isinstance(word, str):
                text += word.lower().replace("'", "") + " "
    if _names(text, SPELLED_OUT):
        return RED_FLAG_CARD
    own = " " + re.sub(r"[^a-z]+", " ", str(understood.get("text") or "").lower()) + " "
    ruled_out = own
    for phrase in ("no back pain", "no backache", "no back ache", "no pain in my back",
                   "without back pain", "no leg pain", "no pain in my legs", "no weakness",
                   "no trouble weeing", "no trouble going for a wee", "no problems weeing",
                   "no trouble peeing", "no numbness in my legs", "no pain",
                   "my back is fine", "my back is ok", "my back is okay", "back is fine",
                   "without a bad back", "no problems with my back"):
        ruled_out = ruled_out.replace(phrase, " ")
    if (_names(ruled_out, BACK_NAMES) and _names(ruled_out, NUMB_ANYWHERE)
            and _names(ruled_out, NUMB_LOWER)):
        return RED_FLAG_CARD
    if _names(ruled_out, SADDLE_PARTS) and not _names(ruled_out, FLAG_WITH_IT):
        return SADDLE_CARD
    if _names(text, LOWER_HALF) or not _names(text, SOMEWHERE_ELSE):
        return RED_FLAG_CARD
    return ""


def _words(understood):
    if not isinstance(understood, dict):
        return set()
    found = set()
    for key in ("words", "background"):
        for word in understood.get(key) or ():
            if isinstance(word, str):
                found.add(word.lower())
    return found


RING_NOT_ON_A_FINGER = RING_AS_A_CALL + (
    "putting it off", "keep putting off", "kept putting off",
    "keep meaning to", "meant to ring", "forgot to ring", "dreading ringing")


def _dose_for_the_drug_named(memory, reading):
    words = set(reading.get("words") or ())
    if words & {"aspirin", "disprin", "anadin", "naproxen", "diclofenac", "voltarol", "tramadol",
                "solpadeine", "veganin", "feminax", "migraleve", "dydramol", "paracodol",
                "dihydrocodeine"}:
        return None
    paracetamol = bool(words & {"paracetamol", "acetaminophen", "calpol", "panadol"})
    ibuprofen = bool(words & {"ibuprofen", "nurofen", "brufen"})
    codeine = bool(words & {"codeine", "co-codamol", "co codamol", "cocodamol", "codamol"})
    if codeine and not paracetamol:
        return ("Co-codamol is paracetamol and codeine together, so the paracetamol limit is what "
                "caps it: two 500/8mg tablets, four times in 24 hours at most, eight a day. The "
                "codeine is what makes it constipating and drowsy, so days rather than weeks, and "
                "don't drive until you know how it treats you. Don't add paracetamol on top: over "
                "4g a day from any mix of products is a liver emergency.")
    if ibuprofen and not paracetamol:
        return ("Ibuprofen for an adult is 200 to 400mg every four to six hours, up to three "
                "times a day, with food, and no more than 1200mg a day without a prescription - "
                "six of the 200mg tablets. Skip it "
                "if you have a stomach ulcer, kidney trouble or are on a blood thinner, and in the "
                "last three months of pregnancy. Use the lowest dose that works, and check a cold "
                "remedy does not already contain it.")
    return ("Two 500mg paracetamol tablets, four times in 24 hours at most, four hours apart - 4g, "
            "or eight tablets, a day, and less if you have liver trouble or drink heavily. "
            "Ibuprofen is 200 to 400mg every four to six hours with food, and no more than 1200mg "
            "a day without a prescription. The packet is the one to trust, and check a cold remedy "
            "does not already contain paracetamol.")


_PIERCING_TROUBLE = re.compile(
    r"\b(red|redness|swollen|swelling|hot|weeping|ooz|pus|yellow|green|feverish|fever|spreading|"
    r"streaking|throbbing|angry|infected|infection|smelly|smell|lump|lumps)\b", re.I)
_PIERCING_BUMP = re.compile(r"\b(bump|bumps|keloid|crusty|crust|scab|lump|stud sunk|embed)\b", re.I)


_PIERCING_PIECE = re.compile(
    r"\b(piercing|piercings|pierced|earring|earrings|ear ring|nose ring|nose stud|nose hoop|"
    r"septum|helix|tragus|daith|rook|conch|cartilage|industrial|barbell|labret|stud|hoop|"
    r"belly bar|belly button|eyebrow|nostril|lip ring|tongue bar|earlobe|ear lobe)\b", re.I)
_PIERCING_NOT_TROUBLE = re.compile(
    r"\b(how long|heal|heals|healing|take to heal|when can i change|change the jewellery|"
    r"aftercare|after care|keloid|crusty|crust|jewellery too tight|swollen in the morning|"
    r"when can i swim|can i swim|downsize|bump|bumps)\b", re.I)


def _a_piercing_in_trouble(understood):
    reading = understood if isinstance(understood, dict) else {}
    said = " ".join([str(reading.get("clean") or ""),
                     " ".join(str(word) for word in (reading.get("words") or ()))])
    if not (_PIERCING_PIECE.search(said) and _PIERCING_TROUBLE.search(said)):
        return False
    return not _PIERCING_NOT_TROUBLE.search(said)


def _piercing_infection(memory, understood):
    reading = understood if isinstance(understood, dict) else {}
    said = " ".join([str(reading.get("clean") or ""),
                     " ".join(str(word) for word in (reading.get("words") or ()))])
    lead = ("A piercing with spreading redness, heat, pus or swelling is infected, and it needs "
            "cleaning and often antibiotics rather than patience.")
    if re.search(r"\bfever\b", said, re.I):
        lead = ("An infected piercing with a fever is one to have looked at today - a fever means "
                "it is not staying local.")
    return (lead + " Leave the jewellery in unless a piercer takes it out: the hole closes over "
            "the infection and traps it, and a piercer can fit a longer bar if the swelling has "
            "outgrown the one you have. Clean it twice a day with sterile saline on a clean pad, "
            "let water run over it in the shower, and stop touching or turning it. Warm salty "
            "water soaks for ten minutes twice a day ease the soreness. See a piercer or a GP "
            "within a day or two if the redness spreads more than a centimetre a day, the skin "
            "round it is hot, there is pus that keeps coming, or the swelling swallows the "
            "jewellery - and go straight away if the redness streaks towards the body, or you have "
            "a fever with it. Cartilage piercings are the ones that go wrong: a hot, swollen "
            "helix or nose that is spreading is worth being seen rather than watched.")


def _a_healing_piercing_not_a_troubled_one(understood):
    reading = understood if isinstance(understood, dict) else {}
    said = " ".join([str(reading.get("clean") or ""),
                     " ".join(str(word) for word in (reading.get("words") or ()))])
    if _PIERCING_BUMP.search(said):
        return True
    return not _PIERCING_TROUBLE.search(said)


_CARTILAGE_PIERCING = re.compile(
    r"\b(nose|nostril|septum|helix|tragus|daith|rook|conch|cartilage|industrial|eyebrow|"
    r"bridge|forward helix)\b", re.I)
_PIERCING_ROUTINE = (
    " Clean it twice a day with sterile saline on a clean pad and let water run over it in the "
    "shower - no alcohol, tea tree or antibacterial gel, and do not twist or turn it, because "
    "that keeps tearing the healing channel. Do not take it out early: a new piercing can close "
    "in hours, and if you must, have the piercer swap it. No swimming for two weeks, no sleeping "
    "on it, and no makeup or hairspray near it. A red bump that keeps growing, spreading redness, "
    "pus or a fever is a piercer or GP question, not a cleaning one.")


def _piercing_healing(memory, understood):
    reading = understood if isinstance(understood, dict) else {}
    said = " ".join([str(reading.get("clean") or ""),
                     " ".join(str(word) for word in (reading.get("words") or ()))])
    if _CARTILAGE_PIERCING.search(said):
        return ("A cartilage piercing - a nose, a nostril, a septum, a helix - takes six to twelve "
                "weeks and often months to settle, where an earlobe is six to eight weeks."
                + _PIERCING_ROUTINE)
    return ("An earlobe takes six to eight weeks to heal and cartilage six to twelve weeks, though "
            "cartilage can take months to settle." + _PIERCING_ROUTINE)


ENTRIES = [
    entry("body-urgent",
          (("cant pee", "can't pee", "cannot pee", "cant wee", "can't wee", "cant pass urine",
            "can't pass urine", "cant pass water", "no urine", "cant urinate", "can't urinate",
            "cannot urinate", "numb", "numbness", "pins and needles", "cant feel my legs",
            "can't feel my legs", "cant feel my feet", "legs give way", "leg gave way",
            "incontinent", "saddle",
            "cant go for a wee", "can't go for a wee", "cant go for a pee", "can't go for a pee",
            "cant have a wee", "can't have a wee", "cant do a wee", "can't do a wee",
            "cant go to the toilet", "can't go to the toilet", "cant get to the toilet",
            "no feeling", "lost feeling", "lost all feeling", "no sensation", "cant feel",
            "can't feel", "gone numb", "went numb", "dont know when i need a wee",
            "numb", "numbness", "pins and needles", "tingling",
            "don't know when i need a wee",
            "numb groin", "groin is numb", "groin went numb", "groin has gone numb",
            "numb round my groin", "numbness in my groin"),
           ("back", "leg", "legs", "calf", "calves", "thigh", "shin", "spine", "side",
            "feet", "foot", "hip", "hips", "pain", "pains", "hurts", "hurting", "ache",
            "aching",
            "toe", "toes", "heel", "heels", "ankle", "ankles", "sole", "soles",
            "saddle", "groin", "genitals", "crotch", "undercarriage", "down there")),
          _red_flag,
          ask=("cant", "can't", "cannot", "no", "numb", "numbness", "pins", "needles", "give",
               "gave", "incontinent", "saddle", "feeling", "sensation", "know", "toilet",
               "urine", "going", "groin"),
          bias=4),
    entry("body-see-today",
          (("hurts when i breathe", "hurts to breathe", "pain when i breathe",
            "worse at night", "wakes me at night", "wake me at night", "wakes me up",
            "woke me up", "hot and swollen", "swollen and hot", "swollen calf", "swollen leg",
            "hot calf", "red and hot", "hot and red", "red and swollen", "swollen and red",
            "warm and red", "after a flight", "after a long flight",
            "swollen", "swelling", "swollen up", "gone hot", "hot to touch",
            "swelled", "swelled up", "swelling up", "puffy", "puffed up", "puffiness"),
           _SORE_ANYWHERE + ("swollen", "swelling", "hot")),
          _see_today,
          ask=("hurts", "hurts to", "pain", "worse", "wakes", "woke", "hot", "swollen", "red",
               "after", "breathe", "night", "swelled", "puffy", "puffed"),
          avoid=("sting", "stings", "stung", "bee", "bees", "wasp", "wasps", "hornet",
                 "insect", "insects", "bite", "bites", "bitten", "nettle", "nettles", "ant",
                 "ants", "mosquito", "mosquitos", "mosquitoes", "horsefly", "tick", "midge",
                 "midges", "gnat", "gnats"),
          guard=_the_part_is_a_persons),
    entry("crushed-finger",
          (("finger", "fingers", "thumb", "thumbs", "fingertip", "fingertips", "hand", "hands",
            "knuckle", "knuckles"),
           ("door", "doors", "drawer", "drawers", "window", "windows", "gate", "boot", "lid",
            "cupboard", "slammed", "slamming", "slam", "shut", "shutting", "closed", "trapped",
            "trapping", "caught", "catching", "jammed", "jamming", "crushed", "crushing",
            "squashed", "squashing",
            "came down on", "went between", "between the")),
          "That is a crush, so the first day is a cold pack - ice in a tea towel, ten minutes at a "
          "time, a few times - with the hand up, and paracetamol or ibuprofen for the ache. Take "
          "any ring off that finger now, before the swelling. Go to A&E the same day if the "
          "fingertip is split or the nail is torn, if blood is building up under the nail, if it "
          "throbs hard, if the finger will not straighten or looks the wrong shape, or if it is "
          "numb: a trapped fingertip can break the bone under the nail, and that needs an X-ray.",
          avoid=("hinge", "hinges", "oil", "oiling", "lock", "locks", "handle", "handles", "knob",
                 "creak", "squeak", "paint", "draught", "draft", "warped", "sticking", "adjust",
                 "marks", "mark", "smudge", "smudges", "fingerprint", "fingerprints", "clean",
                 "cleaning", "wipe", "stain", "stains", "glass", "panel", "install", "replace",
                 "fit a", "hang", "how do i get", "cat", "dog")),
    entry("black-nail",
          (("nail", "nails", "toenail", "toenails", "fingernail", "fingernails", "nail bed"),
           ("black", "went black", "gone black", "blue", "purple", "dark", "bruised", "bruise",
            "dropped", "slammed", "hammer", "banged", "knock", "knocked", "caught it", "trapped",
            "after football")),
          "A knock that turns the nail black is blood trapped under it. Ice it for ten minutes at "
          "a time for the first day, keep the hand or foot up, and take paracetamol or ibuprofen "
          "for the ache. A small dark patch fades over weeks as the nail grows out. Get it seen the "
          "same day if it throbs hard, the nail is lifting, half of it is dark, or the finger will "
          "not bend properly: a doctor can let the blood out, and draining it at home can infect it.",
          ask=("black", "blue", "purple", "bruise", "bruised", "dropped", "slammed", "hammer",
               "bang", "knock", "caught", "trapped", "dark", "throbbing", "sore"),
          avoid=("fungal", "fungus", "thrush", "yellow", "crumbly", "biting", "bite", "chew",
                 "polish", "gel", "acrylic", "manicure", "varnish")),
    entry("limb-went-black",
          (("toe", "toes", "foot", "feet", "ankle", "ankles", "heel", "heels", "leg", "skin",
            "bruise", "bruises",
            "legs", "shin", "shins", "calf", "calves", "thigh", "thighs", "knee",
            "knees", "hip", "hips", "arm", "arms", "forearm", "wrist", "wrists",
            "hand", "hands", "finger", "fingers", "thumb", "thumbs", "elbow", "elbows",
            "shoulder", "shoulders"),
           ("black", "black and blue", "gone black", "went black", "turned black",
            "turn black", "turning black", "going black", "gone blue", "went blue",
            "turned blue", "gone purple", "went purple", "turned purple", "purple")),
          "A bruise is blood under the skin from a knock: it looks black at first, then fades "
          "through purple, green and yellow over one to two weeks. A cold pack for twenty minutes "
          "with a cloth round it, a few times in the first two days, eases it. Get it seen the "
          "same day if it swells hard and fast, the skin is broken, the part will not take your "
          "weight, or a patch goes black with no knock you can remember.",
          guard=_the_part_is_a_persons,
          avoid=("mould", "mold", "mouldy", "moldy", "damp", "wall", "walls", "ceiling",
                 "numb", "numbness", "cold", "freezing", "tingling", "tingly", "pins and needles",
                 "grout", "sealant", "silicone", "tile", "tiles", "window", "frame",
                 "paint", "paintwork", "plaster", "skirting", "bathroom", "shower",
                 "nail", "nails", "toenail", "toenails", "fingernail", "fingernails",
                 "eye", "eyes", "eyelid", "gum", "gums", "tooth", "teeth", "tongue",
                 "lip", "lips", "mouth", "face", "cheek", "jaw",
                 "dog", "dogs", "puppy", "cat", "cats", "kitten", "vet", "horse",
                 "car", "bike", "boot", "boots", "shoe", "shoes", "sock", "socks",
                 "varnish", "polish", "screen", "phone", "kettle", "sink", "bath",
                 "bin", "bags", "tights", "leggings")),
    entry("white-spots-nails",
          (("nails", "nail", "fingernails", "fingernail", "toenails", "toenail"),
           ("white spots", "white marks", "white flecks", "white patches", "white lines",
            "white dots", "little white", "spots on my nails", "marks on my nails")),
          "White spots in a nail are usually small knocks to the nail bed while that part of the nail "
          "was "
          "forming, and they grow out over a few months - not a calcium or zinc shortage, which is "
          "what most people are told. Filing the surface will not shift them and nothing needs "
          "doing. White lines across every nail, or half a nail white with a darker band above "
          "it, is worth a GP look.",
          avoid=("tongue", "mouth", "thrush", "fungal", "fungus", "yellow", "black", "blue",
                 "purple", "bruise", "paint", "polish", "varnish", "gel", "acrylic",
                 "dog", "cat", "wall", "paintwork", "fence", "shirt")),
    entry("dry-skin",
          (("skin", "hands", "hand", "face", "cheeks", "legs", "arms", "elbows", "heels",
            "feet", "knuckles", "body", "moisturiser", "moisturizer", "emollient"),
           ("dry", "drier", "dryness", "flaky", "flakes", "flaking", "cracked", "cracking",
            "cracks", "rough", "itchy", "itching", "tight", "peeling", "chapped")),
          "Dry, tight skin in winter is mostly central heating and long hot showers washing the "
          "oils out: short lukewarm showers, pat dry rather than rub, and a thick unperfumed "
          "cream within three minutes while the skin is still damp. Cracked hands "
          "and heels want a cream with urea or lanolin and cotton gloves overnight. If the cracks "
          "bleed or the skin is red and itchy, a pharmacist can give you an emollient.",
          avoid=("lips", "lip", "mouth", "corner of my mouth", "eyes", "eye", "hair", "dandruff",
                 "my son", "my daughter", "my child", "my kid", "my kids", "my baby",
                 "my toddler", "my husband", "my wife", "my partner", "my mum", "my mom",
                 "my mother", "my dad", "my father", "my friend", "my dog", "my cat", "my puppy",
                 "my horse", "his skin", "her skin", "their skin",
                 "sore", "hurts", "hurt", "aching", "ache", "pain", "pains", "painful",
                 "stiff", "injury", "injured",
                 "egg", "eggs",
                 "knuckles crack", "knuckles cracking", "knuckle cracks", "knuckles click",
                 "knuckles clicking", "knuckles pop", "crack my knuckles",
                 "cracking my knuckles", "crack your knuckles", "cracking your knuckles"),
          guard=_the_part_is_a_persons),
    entry("face-wash",
          (("face", "facial"),
           ("wash", "washing", "washed", "clean", "cleanse", "cleanser", "temperature",
            "how hot", "hot water", "cold water", "lukewarm", "twice a day", "before bed")),
          "Lukewarm water and a gentle unperfumed cleanser, morning and evening: warm water and a "
          "flannel lift grime and make-up, while hot water strips the oils and leaves the skin "
          "tight. Pat dry rather than rub, and put moisturiser on while the skin is still damp; "
          "anything that stings is too harsh for a face.",
          avoid=("dry", "drier", "drying out", "dry out", "dry it out", "itchy", "spot",
                 "spots", "acne", "eczema", "flaky", "cracked",
                 "hands", "hand", "body", "hair", "baby", "child", "dishes", "clothes",
                 "laundry", "mask", "face mask", "beard", "shave", "shaving"),
          bias=2),
    entry("hands-wash",
          (("hands", "hand", "fingernails", "fingertips"),
           ("wash", "washing", "washed", "clean", "cleaning", "soap", "germs", "bacteria",
            "hygiene", "how long", "before eating", "after the toilet", "after gardening",
            "after diy", "hot water", "cold water", "sanitiser", "hand gel")),
          "Wet your hands, then soap for twenty seconds - about as long as singing Happy Birthday "
          "twice - and cover the backs of the hands, between the fingers, the thumbs and the "
          "fingertips under the nails. Rinse and dry on a clean towel, because wet hands pick up "
          "germs again, and use hand gel only when there is no sink.",
          avoid=("dry", "drier", "cracked", "cracking", "itchy", "eczema", "numb", "tingling",
                 "cold", "warm", "winter", "raynaud", "pain", "hurt", "swollen", "nails",
                 "nail polish", "paint", "oil", "grease", "bleach", "stain", "dishes",
                 "washing up", "laundry", "washing machine", "gloves", "mittens", "dog", "cat",
                 "car", "window", "face", "hair",
                 "jumper", "jumpers", "cardigan", "cardigans", "wool", "woollen", "woolens",
                 "notice", "notice in", "resign", "resigning", "resignation", "job", "boss",
                 "employer", "manager", "contract", "redundancy", "sacked", "promotion",
                 "knitwear", "knitted", "cashmere", "merino", "silk", "silky", "scarf", "scarves",
                 "dress", "dresses", "shirt", "shirts", "blouse", "sweater", "sweaters", "fleece",
                 "by hand", "hand wash", "hand washing", "hand-wash", "handwash", "hand washed",
                 "stitches", "stitch", "sutures", "suture", "staples", "wound", "wounds",
                 "gash", "gashes", "scab", "scabs", "bandage", "bandages", "dressing",
                 "dressings", "plaster cast", "graze", "grazes", "open wound", "cut on my hand",
                 "cut on the hand", "cut on my finger", "splinter", "ingrown"),
          bias=3),
    entry("dry-scalp",
          (("scalp", "scalp is", "head itches"),
           ("dry", "drier", "dryness", "flaky", "flakes", "flaking", "itchy", "itching",
            "scaly", "dandruff", "white bits", "snowy")),
          "A dry, flaky scalp is usually dandruff: a yeast that feeds on the oil on your head, so "
          "it is not the same thing as dry skin and body cream will not help it. Wash with an "
          "anti-dandruff shampoo - zinc pyrithione or ketoconazole, from any chemist - two or "
          "three times a week, work it into the scalp and leave it five minutes before rinsing, "
          "and give it a month. Do not scratch the flakes off, and keep washing your hair: a "
          "scalp left greasy feeds it. If it is red, sore, or hair is thinning in patches, see a "
          "pharmacist or your GP.",
          avoid=("hair", "shampoo", "conditioner", "dye", "coloured", "bleach")),
    entry("moisturiser",
          (("moisturiser", "moisturizer", "moisturise", "moisturize", "moisturising",
            "moisturizing", "face cream", "day cream", "night cream", "body lotion",
            "face lotion", "skin cream", "cream for my face", "cream for dry skin"),
           ("need", "needs", "should", "what", "which", "choose", "choosing", "best", "use",
            "worth", "buy", "type", "kind", "recommend", "looking for", "how do i", "how to",
            "good", "cheap", "expensive")),
          "A plain unperfumed cream is the whole job: thicker (an ointment, or a cream in a tub) "
          "for dry or flaky skin, a light lotion or gel for oily skin, and one with SPF 30 in it "
          "for the morning if you want to skip a step. Put it on damp skin within three minutes of "
          "a shower, buy the cheap own-brand - the price is packaging - and a pump is cleaner than "
          "a tub you dig your fingers into.",
          avoid=("dry", "drier", "dryness", "flaky", "flakes", "flaking", "cracked", "cracking",
                 "cracks", "rough", "itchy", "itching", "tight", "peeling", "chapped", "sore",
                 "rash", "eczema", "psoriasis", "red", "burning", "sunburn", "sun cream",
                 "sunscreen", "spf", "dog", "cat", "puppy", "baby", "babies", "nappy",
                 "my son", "my daughter", "my child", "my kid", "my kids")),
    entry("oily-skin",
          (("skin", "face", "forehead", "nose", "chin", "cheeks", "complexion", "t-zone",
            "t zone", "oily skin", "greasy skin", "shiny skin", "oily face", "greasy face"),
           ("greasy", "oily", "oil", "shiny", "shine", "gleam", "getting greasy",
            "gets greasy", "getting oily", "gets oily", "getting shiny", "by lunchtime",
            "during the day")),
          "Wash twice a day with a gentle foaming cleanser rather than soap, which strips the skin "
          "and leaves it making more oil, then use a light oil-free gel moisturiser - oily skin "
          "still needs one. Do not scrub or wash more than twice; blot the shine at lunchtime "
          "instead, and a niacinamide or salicylic acid product is the one extra step worth adding.",
          avoid=("dry", "drier", "flaky", "tight", "rash", "eczema", "psoriasis", "spot",
                 "spots", "spotty", "spotting", "acne", "hair", "scalp", "chip", "chips",
                 "sink", "sinks", "stainless", "stainless steel", "steel", "kitchen",
                 "bathroom", "tap", "taps", "worktop", "cutlery", "silver", "brass", "copper",
                 "metal", "floor", "floors", "window", "windows", "car", "shoes", "leather",
                 "pan", "frying", "food",
                 "oven", "ovens", "hob", "hobs", "cooker", "cookers", "grill", "griller",
                 "microwave", "extractor", "tray", "trays", "baking", "roasting", "tin", "tins",
                 "saucepan", "saucepans", "worktop", "worktops", "splashback", "cupboard",
                 "cupboards", "sink", "dishes", "dishwasher", "fridge", "freezer", "kettle",
                 "toaster", "barbecue", "bbq", "wall", "walls", "tiles",
                 "kitchen", "kitchens", "bathroom", "bath", "shower", "floor", "floors",
                 "garage", "surface", "surfaces", "counter", "counters", "unit", "units",
                 "car", "engine", "bike", "chain", "dog", "cat",
                 "kitchen", "kitchens", "hob", "hobs", "cooker", "oven", "worktop", "worktops",
                 "sink", "splashback", "extractor", "floor", "floors", "tiles", "dishes",
                 "cooking", "cooked", "bbq", "barbecue", "grill", "containers", "jars",
                 "suit", "suits", "jacket", "jackets", "blazer", "blazers", "trousers",
                 "shirt", "shirts", "skirt", "dress", "dresses", "coat", "coats", "sleeve",
                 "sleeves", "elbow", "elbows", "fabric", "leather", "sofa", "settee",
                 "table", "tables", "wooden", "furniture", "cupboard", "chair", "desk",
                 "shoe", "shoes", "boot", "boots", "polish", "polishing", "polished")),
    entry("skin-routine",
          (("skincare", "skin care", "cleanser", "cleansing", "face wash", "glowing skin",
            "skin routine", "face routine", "my skin looks tired", "look after my skin",
            "look after your skin", "good skin"),
           ("what", "which", "should", "how do i", "how to", "choose", "best", "need", "start",
            "simple", "good", "order", "daily", "routine", "use")),
          "Keep it to three steps: a gentle cleanser, a moisturiser, and a sunscreen in the "
          "morning - add one active, a retinoid or an acid, at night only once those three are a "
          "habit. Most routines fail because they are too long, and no jar beats sleep, water and "
          "not smoking.",
          avoid=("spot", "spots", "spotty", "acne", "blackhead", "blackheads", "dry", "drier",
                 "flaky",
                 "itching", "itchy", "rash", "eczema", "psoriasis", "mole", "wrinkles",
                 "botox", "sunburn", "dandruff", "hair", "foundation", "makeup", "make up",
                 "dog", "cat", "baby", "babies", "nappy", "child", "kid", "kids")),
]

BACK_WENT = ("put my back out", "put out my back", "put it out", "threw my back out",
             "threw it out", "my back went", "back went", "my back has gone", "my back is out",
             "my back went out", "my back gave way", "my back locked", "my back is in spasm",
             "my back went into spasm", "i tweaked my back", "i twisted my back", "my back slipped")

_THE_VISIT = {"appointment", "appointments", "checkup", "check-up", "check", "visit", "filling",
              "hygienist", "root canal"}
_THE_QUEUE = {"wait", "waits", "waiting", "soon", "sooner", "quickly", "book", "booking",
              "booked", "getting", "seen", "available", "weeks", "days", "months", "list"}
_REGISTERING_A_DENTIST = (
    "Look for practices near you that are taking on new patients, then ring rather than "
    "email: each practice keeps its own list and it opens and closes, and the phone gets "
    "you a straight answer. Ask on the call whether they take NHS adults and how long the "
    "first check-up wait is. If nobody near you has room, ring 111 and ask for the urgent "
    "dental service, which will see you and can tell you who is taking patients.")


_A_LENGTH_OF_A_VISIT = re.compile(
    r"\bhow long (?:does|do|will|would|should)\b[^?.!]*\b(?:take|last|wait)\b"
    r"|\bhow long (?:is|are|was)\b"
    r"|\bhow many (?:minutes|hours)\b",
    re.I)
_A_LIST_THAT_IS_LONG = re.compile(
    r"\bwaiting list\b|\bon the list for\b|\blist is (?:months|years|weeks|long|closed)\b",
    re.I)
_A_PRACTICE_ERRAND = re.compile(
    r"\b(?:register|registering|sign up|join|join up|find|finding|accepting|new patients?|"
    r"taking (?:on )?(?:new )?patients?|need (?:a|an|an nhs|a new) dentist|get a dentist|"
    r"looking for a dentist|near me|nearby|local dentist|none|no dentist|moved)\b", re.I)


_A_BECOMING_A_DENTIST = re.compile(
    r"\b(?:become|becoming|train as|training as|study|studying|degree|qualify as|qualifying as|"
    r"career|became)\b[^?.!]*\b(?:dentist|dentistry|dental school|dental surgeon)\b"
    r"|\b(?:dentist|dentistry|dental school|dental surgeon)\b[^?.!]*"
    r"\b(?:training|course|degree|qualify|career|school)\b", re.I)


def _an_errand_the_dentist_card_answers(understood):
    reading = understood if isinstance(understood, dict) else {}
    said = str(reading.get("clean") or reading.get("text") or "")
    if _A_BECOMING_A_DENTIST.search(said):
        return False
    if _A_PRACTICE_ERRAND.search(said) or _A_LIST_THAT_IS_LONG.search(said):
        return True
    return bool(_A_LENGTH_OF_A_VISIT.search(said))


_A_CHECK_UP = ("A check-up with a dentist is booked for about 15 to 20 minutes, and a first "
               "visit to a practice often gets half an hour because they take an X-ray and a "
               "history.")
_A_FILLING = "A filling takes 20 to 30 minutes."
_A_ROOT_CANAL = "A root canal takes 45 minutes to an hour."
_A_HYGIENIST = "A clean with the hygienist takes about 30 minutes."
_A_CROWN_VISIT = ("A crown is two visits of about an hour each, one to shape the tooth and one "
                  "to fit it.")
_AN_IMPLANT = ("An implant is two short visits and a long wait in between: about an hour to "
               "place it under the gum, three to six months for the bone to take to it, then "
               "about an hour to fit the crown on top.")
_THE_BOOKING = ("Say what it is for when you book, and ask for a double appointment if you have "
                "more than one thing to look at, so the slot fits.")
_THE_VISIT_IN_ORDER = (_A_CHECK_UP, _A_FILLING, _A_ROOT_CANAL, _A_HYGIENIST, _A_CROWN_VISIT)


def _the_lengths_of_the_visit(said, words):
    named = []
    if words & {"filling", "fillings"}:
        named.append(_A_FILLING)
    if words & {"canal"} or "root canal" in said:
        named.append(_A_ROOT_CANAL)
    if words & {"hygienist", "hygienist's", "clean", "cleaning"}:
        named.append(_A_HYGIENIST)
    if words & {"crown", "crowns"}:
        named.append(_A_CROWN_VISIT)
    if words & {"implant", "implants"}:
        named.append(_AN_IMPLANT)
    parts = named + [part for part in _THE_VISIT_IN_ORDER if part not in named]
    return " ".join(parts + [_THE_BOOKING])


def _the_dentist_errand(memory, understood):
    words = set(_line_words(understood))
    said = str(understood.get("clean") or understood.get("text") or "").lower()
    occasion = words & {"appointment", "appointments", "checkup", "check-up", "check", "visit",
                        "hygienist", "hygienist's"}
    done_to_a_tooth = words & {"filling", "fillings", "crown", "crowns", "canal"} or (
        "root canal" in said) or ("check up" in said)
    the_place = words & {"dentist", "dentists", "dental", "orthodontist", "tooth", "teeth",
                         "practice", "surgery"}
    how_long = re.search(r"\bhow (?:long|many (?:minutes|hours))\b", said)
    takes = words & {"take", "takes", "taking"}
    lasts = words & {"last", "lasts"}
    the_wait = bool(words & (_THE_QUEUE | {"see", "seen"}) or "to get" in said)
    registering = bool(words & {"register", "registering", "sign up", "join"})
    a_crown = bool(words & {"crown", "crowns"})
    if a_crown and lasts and not takes and not the_wait and not registering:
        return (
            "A crown lasts ten to fifteen years on average, and some go much longer. What wears "
            "it out is usually the tooth and the gum under it rather than the crown itself, so "
            "keep cleaning round the edge where it meets the gum, and tell the dentist if it "
            "starts to feel loose or the gum bleeds when you floss.")
    a_visit = ((occasion and (how_long or takes or lasts))
               or (done_to_a_tooth and (takes or re.search(r"how many (?:minutes|hours)", said)))
               or (the_place and how_long and (takes or lasts)))
    if a_visit and not the_wait and not registering:
        return _the_lengths_of_the_visit(said, words)
    if _A_LIST_THAT_IS_LONG.search(said) and not how_long:
        return _REGISTERING_A_DENTIST
    if words & (_THE_QUEUE | {"see", "seen"}) or "to get" in said:
        return _book_the_appointment(memory, understood)
    return _REGISTERING_A_DENTIST


ENTRIES = [
    entry("back-went",
          (("my back", "lower back", "my spine"),
           ("went", "gone", "put", "out", "threw", "twisted", "tweaked", "slipped", "locked",
            "spasm", "gave way", "went out", "is out",
            "goes", "go", "going", "seize", "seizes", "seized", "seizing",
            "done my back in", "done my back", "pulled my back", "back has gone", "backs gone",
            "back went", "in spasm")),
          "A back that goes like that is almost always a muscle strain, and it is at its worst in "
          "the first day or two: keep moving gently rather than taking to your bed, take "
          "paracetamol or ibuprofen if you can, and use a hot water bottle on the tight part. Most "
          "settle in two to six weeks. Ring 111 today if you cannot pass urine, have numbness "
          "between your legs, or the pain came on after a fall, and see a GP if it is no better in "
          "a fortnight.",
          avoid=tuple(w for w in AVOID if w not in EXERCISE_DAY)
          + ("deal", "contract", "wedding", "booking", "order", "offer", "agreement", "mortgage",
             "pull out", "pull out of", "going ahead", "hire purchase",
             "stiff", "stiffness", "stiffened", "stiffens", "stiffening")),

    entry("ring-stuck",
          (("ring", "rings", "wedding ring", "engagement ring", "band"),
           ("stuck", "swollen finger", "swollen", "off my finger", "off", "wont come off",
            "won't come off", "cut off", "tight", "too tight", "trapped")),
          "Work it off with soap and water or a little oil, twisting rather than pulling, hand "
          "raised above your head for a few minutes first to let the swelling go down. Wind a "
          "piece of thread or dental floss under the ring from the finger side and unwind it "
          "around the finger past the knuckle, tucking the ring along a loop at a time. Get help "
          "the same day if the finger goes numb, cold or blue: A&E or a jeweller can cut it off.",
          avoid=("hob", "cooker", "burner", "stove", "bath", "curtain", "doorbell", "bell",
                 "phone", "answering", "ear", "ears", "nose", "nose ring", "earring", "earrings",
                 "sound", "sounds", "noise", "circle", "tree",
                 "bite", "bites", "bitten") + RING_NOT_ON_A_FINGER,
          bias=2,
          ask=("ring", "rings")),
    entry("piercing-healing",
          (("piercing", "piercings", "pierced ear", "pierced ears", "ear piercing",
            "ear piercings", "nose piercing", "septum", "belly piercing", "belly button piercing",
            "cartilage piercing", "helix", "tragus", "daith", "industrial piercing",
            "lip piercing", "eyebrow piercing", "nipple piercing", "new piercing",
            "nose ring", "nose rings", "septum ring", "nose hoop", "ear hoop", "hoop earring",
            "nose stud", "stud earring", "ear stud", "belly bar", "ring in my nose",
            "ring in my ear"),
           ("how long", "heal", "heals", "healing", "take to heal", "sore", "red", "swollen",
            "aftercare", "clean", "cleaning", "clean it", "care", "infection", "bump", "keloid",
            "crusty", "weeping", "swimming", "sleep on", "change the jewellery", "take it out",
            "when can i change", "change it", "changing it", "swap it", "downsize", "shorter bar")),
          _piercing_healing,
          guard=_a_healing_piercing_not_a_troubled_one,
          avoid=("earring", "earrings", "ear ring", "tongue", "clit", "industrial estate",
                 "helix nebula", "engagement ring", "wedding ring", "ring finger", "ring main",
                 "ring final", "hob ring", "onion ring", "boxing ring", "circus ring",
                 "key ring", "keyring", "napkin ring", "curtain ring", "smoke ring")),
    entry("ring-stuck-blue",
          (("ring", "rings", "wedding ring", "engagement ring", "band"),
           ("gone blue", "turning blue", "blue", "cold", "black", "cutting in", "cut into")),
          "Get it off today, and get help if you cannot: a finger that has gone numb, cold, blue or "
          "black behind a ring needs the ring cut off, so go to A&E or ring 111 and they will tell "
          "you where. While you wait, keep the hand raised above your heart and run it under cool "
          "water, and do not keep twisting the ring. A jeweller can cut it off for a few pounds if "
          "the finger still looks normal.",
          avoid=("hob", "cooker", "burner", "stove", "bath", "curtain", "doorbell", "bell",
                 "phone", "answering", "ear", "ears", "nose", "sound", "circle",
                 "caller", "callers", "cold call", "cold calls", "nuisance", "spam",
                 "robocall", "robocalls", "unknown number",
                 "tree", "bite", "bites", "bitten") + RING_NOT_ON_A_FINGER,
          bias=4,
          ask=("ring", "rings")),
    entry("register-dentist",
          (("dentist", "dental practice", "dental surgery", "nhs dentist", "orthodontist",
            "filling", "fillings", "root canal", "hygienist", "check up", "check-up",
            "checkup",
            "crown", "crowns",
            "dental"),
           ("register", "sign up", "join", "find", "accepting", "new patients", "new patient",
            "taking patients", "patients", "taking", "on the list", "no dentist", "need a dentist",
            "looking for", "get one", "get a dentist", "near me", "nearby", "local", "none",
            "waiting",
            "how long", "how soon", "how many minutes", "last", "lasts", "take", "takes",
            "wait", "waits")),
          _the_dentist_errand,
          guard=_an_errand_the_dentist_card_answers,
          avoid=("toothache", "tooth", "teeth", "pain", "hurts", "hurting", "agony", "bleeding",
                 "abscess", "swollen", "broken", "chipped", "knocked out", "emergency", "today",
                 "child", "children", "kid", "kids", "baby", "toddler", "in pain", "wisdom",
                 "abroad", "holiday", "holidays", "travelling", "traveling", "expat", "spain",
                 "france", "greece", "turkey", "portugal", "america", "usa", "thailand",
                 "croatia", "italy",
                 "complain", "complaining", "complaint", "complaints"),
          bias=2),
    entry("register-gp",
          (("gp", "doctor", "doctor's", "doctors surgery", "doctors practice", "health centre",
            "medical centre", "surgery", "nhs"),
           ("register", "sign up", "join", "find", "new patient", "new patients", "on the list",
            "taking patients", "moved", "just moved", "change", "switch", "another", "different",
            "near me", "nearby", "local")),
          "Ring the surgeries near your new address and ask if their list is open: most take "
          "people from their own area, and a practice can say no if you live outside it, so try "
          "the next one rather than arguing. Take photo ID and something with the new address to "
          "the first appointment. If you are on regular medicine, ask for the repeat prescription "
          "to be set up that week, and tell them you have just moved so the old notes are asked "
          "for.",
          avoid=("appointment", "appointments", "refer", "referral", "sick note", "fit note",
                 "ignored", "dismissed", "sent me away", "waiting list", "results", "test"),
          bias=2),


] + ENTRIES

ENTRIES.append(entry(
    "a-dentist-career-length",
    (("become a dentist", "becoming a dentist", "be a dentist", "train as a dentist",
      "training as a dentist", "study dentistry", "studying dentistry", "dentistry degree",
      "dental school"),
     ("how long", "how many years", "years", "long does it take", "long does it")),
    "Five years at dental school, then a year of dental foundation training in a practice "
    "before you can work on your own, so six years from starting to being paid as a dentist. "
    "The entry grades are the thing that decides it: A-level chemistry and biology are wanted by "
    "most schools, and the UCAT test plus an interview come before any offer.",
    avoid=("toothache", "tooth", "teeth", "pain", "hurts", "emergency", "check up", "check-up",
           "filling", "crown", "root canal", "hygienist's", "appointment", "cost", "much",
           "how much", "salary", "paid", "pay", "worth it", "nhs"),
    bias=3))


def _what_can_i_take_pregnant_or_feeding(memory, reading):
    words = set(reading.get("words") or ())
    feeding = bool(words & {"breastfeeding", "breast", "feeding", "nursing", "chestfeeding"})
    pregnant = bool(words & {"pregnant", "pregnancy", "expecting", "trimester"})
    if feeding and not pregnant:
        return ("Paracetamol and ibuprofen are both fine while you are breastfeeding; avoid "
                "aspirin and go easy on codeine. Heartburn takes an antacid like Gaviscon, "
                "own-brand is the same. A pharmacist will check anything else for free, and see "
                "your GP if it lasts days rather than hours.")
    return ("In pregnancy, paracetamol at the lowest dose that works, for the shortest time, and "
            "no ibuprofen - especially after 20 weeks - or aspirin unless a doctor prescribed it. "
            "While breastfeeding, paracetamol and ibuprofen are both fine; avoid aspirin and go "
            "easy on codeine. Heartburn takes an antacid like Gaviscon, own-brand is the same. A "
            "pharmacist will check the rest, and ring your midwife if it lasts days or comes with "
            "bleeding or less movement.")


_DRUGS = ("paracetamol", "ibuprofen", "nurofen", "co codamol", "co-codamol", "co codrydamol",
          "codeine", "aspirin", "painkiller", "painkillers", "calpol", "neurofen")

ENTRIES += [
    entry("painkillers-pregnancy",
          (_DRUGS,
           ("pregnant", "pregnancy", "expecting a baby", "expecting", "weeks pregnant",
            "trimester", "while im pregnant", "having a baby")),
          "Paracetamol is the one to use in pregnancy: the lowest dose that works, for as short a "
          "time as you can. Avoid ibuprofen, especially after 20 weeks, and don't take aspirin "
          "unless a doctor has prescribed it for you. For anything else - a headache that keeps "
          "coming back, heartburn, a bad back - ask your midwife or a pharmacist, who will check "
          "it against your stage.",
          avoid=("overdose", "overdosed", "took too much", "whole packet", "allergic",
                 "reaction", "child", "kid", "baby is", "my baby", "son", "daughter",
                 "dog", "cat")),
    entry("painkillers-breastfeeding",
          (_DRUGS,
           ("breastfeeding", "breast feeding", "nursing", "feeding my baby", "chestfeeding",
            "while im feeding")),
          "Paracetamol and ibuprofen are both fine while you are breastfeeding - ibuprofen is the "
          "one usually suggested for pain with swelling, taken with food. Avoid aspirin, and go "
          "easy on co-codamol and other codeine tablets, which can make a baby drowsy. Check what "
          "else is in any cold remedy you take, and a pharmacist will check anything else for "
          "free.",
          avoid=("overdose", "overdosed", "took too much", "whole packet", "allergic",
                 "reaction", "son", "daughter", "dog", "cat")),
    entry("what-can-i-take-pregnant-or-feeding",
          (("what can i take", "can i take anything", "is there anything i can take",
            "anything safe", "is it safe to take", "what can i have", "whats safe to take",
            "whats safe"),
           ("pregnant", "pregnancy", "expecting", "weeks pregnant", "trimester", "while im pregnant",
            "breastfeeding", "breast feeding", "nursing", "while im feeding")),
          _what_can_i_take_pregnant_or_feeding,
          avoid=_DRUGS + ("antibiotic", "antibiotics", "heartburn", "indigestion", "reflux",
                          "antacid", "gaviscon", "sickness", "nausea", "vomiting",
                          "constipation", "laxative", "hayfever", "hay fever",
                          "antihistamine", "antihistamines", "thrush", "uti")),
    entry("painkillers-which-one",
          (("paracetamol or ibuprofen", "ibuprofen or paracetamol",
            "paracetamol and ibuprofen which", "which painkiller", "which is better paracetamol",
            "which one is better ibuprofen", "ibuprofen or paracetamol for a headache"),
           ("which", "better", "or", "should", "for a", "vs", "versus")),
          "Ibuprofen suits pain with swelling or inflammation - a sprain, period pain, toothache - "
          "taken with food. Paracetamol suits a plain headache or a temperature, and it is the one "
          "to use if ibuprofen upsets your stomach, you are pregnant, or you take a blood thinner. "
          "If one alone is not enough they can be taken together, on their own schedules.",
          avoid=("stomach", "ulcer", "kidney", "asthma", "blood thinner", "warfarin",
                 "alcohol", "drink", "drinking", "beer", "wine", "pint", "hangover",
                 "sleepy", "drowsy", "thin your blood", "how long",
                 "overdose", "took too much", "child", "kid", "baby", "dog", "cat",
                 "pregnant", "breastfeeding", "allergic", "hangover", "period pain not",
                 "newborn", "newborns", "new born", "neonate", "infant",
                 "month old", "months old", "week old", "weeks old")),
    entry("painkillers-dose",
          (_DRUGS,
           ("how much", "how many", "how often can i take", "dose", "dosage", "maximum",
            "max", "safe amount", "a day", "per day", "in 24 hours", "at a time")),
          _dose_for_the_drug_named,
          avoid=("child", "kid", "baby", "toddler", "year old", "son", "daughter",
                 "calpol", "calprofen", "nurofen for children", "childrens", "children's",
                 "junior", "give him", "give her", "give them", "give my", "shall i give",
                 "can i give", "do i give", "for my son", "for my daughter", "for my baby",
                 "dog", "cat", "overdose", "overdosed", "took too many", "too many",
                 "whole packet", "pregnant", "pregnancy", "breastfeeding", "allergic",
                 "reaction", "how many days", "how long can i take",
                 "newborn", "newborns", "new born", "neonate", "neonates", "infant",
                 "infants", "month old", "months old", "week old", "weeks old",
                 "under 3 months", "under three months", "breastfed", "formula fed")),
    entry("pregnant-swollen-ankles",
          (_PREGNANCY_SWELLING, _PREGNANCY_SWELLING_PARTS, _PREGNANCY_WORDS),
          _PREGNANCY_SWELLING_REPLY,
          avoid=_PREGNANCY_SWELLING_AVOID,
          bias=6,
          guard=_names_a_pregnancy),
    entry("pregnant-swollen-ankles-in-weeks",
          _PREGNANCY_SWELLING + _PREGNANCY_SWELLING_PARTS,
          _PREGNANCY_SWELLING_REPLY,
          avoid=_PREGNANCY_SWELLING_AVOID,
          bias=6,
          shape=(_a_figure_in_weeks,),
          guard=_dates_a_pregnancy_in_weeks),
]

def _bare_words(line):
    return [w for w in re.findall(r"[a-z']+", str(line or "").lower()) if len(w) > 2]


TOOTH_WORDS = {"tooth", "teeth", "toothache", "filling", "fillings", "crown", "crowns",
               "extraction", "extracted", "gum", "gums", "denture", "dentures", "wisdom",
               "brace", "braces", "root canal", "enamel", "abscess", "chipped", "chipped tooth"}

SEEN_ABOUT_IT = {"book", "booking", "booked", "appointment", "appointments", "ring", "ringing",
                 "call", "phone", "see", "seen", "register", "registering", "register", "get in",
                 "joined", "joining", "new", "urgent", "emergency", "pain", "hurts", "hurting"}


def _book_the_appointment(memory, understood):
    words = set(_line_words(understood))
    places = {"dentist", "dentists", "dental", "orthodontist"}
    doctors = {"doctor", "doctors", "gp", "gps", "surgery", "practice", "clinic", "nurse"}
    named = words & places
    if not named and not words & doctors:
        before = []
        turns = (memory.get("turns") or []) if isinstance(memory, dict) else []
        for turn in turns[-1:]:
            if isinstance(turn, dict) and isinstance(turn.get("user"), str):
                before.extend(_bare_words(turn["user"]))
        before = set(before)
        if before & TOOTH_WORDS:
            named = before & places or {"dentist"}
        elif before & places and before & SEEN_ABOUT_IT:
            named = before & places
    if words & {"long", "soon", "quickly", "wait", "waits", "waiting", "weeks", "days"}:
        if named:
            return (
                "Ask what the wait is when you ring: a routine dental check-up is usually a few "
                "days to a couple of weeks, depending on the practice, and a tooth that hurts is "
                "seen the same day or the next because most practices keep a few slots back each "
                "morning. Ring at opening time for one of those, and 111 can name an urgent NHS "
                "dentist if yours has nothing for days.")
        return (
            "Ask what the wait is when you ring: a routine GP appointment is usually a few days to "
            "a couple of weeks, and anything urgent is seen the same day because surgeries keep "
            "slots back each morning for it. Ring at the moment the lines open for one of those, "
            "and 111 can find an urgent dentist or a walk-in centre if your surgery has nothing.")
    if named:
        return (
            "Ring the dental practice as soon as it opens and ask for an urgent slot: most keep a "
            "few back each morning, and saying it hurts, or that a tooth has broken or a filling "
            "has come out, is what gets you one of them. Ask what they have sooner if the wait is "
            "weeks, and ring 111 for the out-of-hours dental service if your practice is shut or "
            "cannot see you within a few days - they can also name an urgent NHS dentist. Until "
            "then paracetamol or ibuprofen at the dose on the pack, and a pharmacist can help you "
            "hold on.")
    return (
        "Ring at the moment the lines open - 8am for most GP surgeries - and ask for the first "
        "appointment of the day: same-day slots go in the first half hour. Say in one sentence "
        "what it is for, because \"I need it looked at today\" books faster than \"I was "
        "wondering\", and ask to go on the cancellation list if the wait is weeks. Dentists are "
        "the same: say it hurts and ask what they have sooner, and 111 can find an urgent NHS "
        "dentist if yours cannot see you within a few days. If there is nothing at all, ask which "
        "day the next slots are released and whether the duty doctor can ring you back, and "
        "remember a pharmacist can treat a lot of everyday things the same day.")


_DECISION_ASK = re.compile(
    r"\b(?:should|shall|do|would|could)\s+i\b[^.?!]*\b(?:see|go|get|be seen|have it|"
    r"have this|bother|worry)\b|\bis it worth\b|\bworth (?:seeing|going|getting|a trip)\b|"
    r"\bdo i need to\b|\bneed i\b")
_THE_BOOKING_WORDS = frozenset((
    "book", "books", "booking", "booked", "appointment", "appointments", "register",
    "registering", "registration", "online", "app", "phone", "ring", "call", "surgery",
    "practice", "clinic", "cancellation", "cancellations", "slot", "slots", "reception",
    "receptionist", "walk in", "111"))


_A_RETURN_TO = ("back to", "back at", "going back", "go back", "went back", "come back",
                "coming back", "got back")


def _a_decision_is_not_a_booking(understood):
    clean = ((understood or {}).get("clean") or "").lower()
    if not _DECISION_ASK.search(clean):
        return True
    if any(phrase in clean for phrase in _A_RETURN_TO):
        return True
    return bool(set(re.findall(r"[a-z']+", clean)) & _THE_BOOKING_WORDS)


ENTRIES.append(entry(
    "book-an-appointment",
    (("appointment", "appointments", "doctor", "dentist", "gp", "surgery",
      "doctors practice", "doctor's practice", "doctors' practice", "gp practice",
      "medical practice", "the practice", "my practice", "our practice", "local practice",
      "clinic", "checkup", "check up"),
     ("book", "booking", "make", "made", "get", "arrange", "appointment", "see",
      "any appointments", "never has", "no appointments", "nothing available", "fully booked",
      "cant get in", "can't get in", "none left", "all booked")),
    _book_the_appointment, guard=_a_decision_is_not_a_booking,
    avoid=("often", "frequently", "regular", "regularly", "times", "interval",

           "register", "registering", "registration", "sign up", "signed up", "signup",
           "off", "leave", "holiday", "boss", "cover", "sick", "ill", "unwell", "chest pain",
           "bleeding", "cant breathe", "can't breathe", "111", "999", "a&e", "waiting room",
           "nervous", "scared", "dreading", "terrified", "terrifying", "frightened", "phobia",
           "afford", "cost", "how much",
           "free", "is it free", "do i pay", "do i have to pay",
           "haircut", "hair cut", "hair appointment", "barber", "barbers", "hairdresser",
           "salon", "nails", "manicure", "pedicure", "waxing", "massage", "facial",
           "hair colour", "colour", "restaurant", "table")))

SEA_WATER_ALARM = re.compile(
    r"\b(?:sick|sickness|throwing up|thrown up|threw up|vomit|vomiting|vomited|dizzy|dizziness|"
    r"confused|confusion|drowsy|lethargic|floppy|faint|fainted|fainting|unwell|poorly|"
    r"too much|lots|loads|plenty|gallons|whole bottle|a lot)\b")

SEA_WATER_ALARM_REPLY = (
    "Ring 111 now: being sick, dizzy or confused after swallowing sea water needs a doctor "
    "today, and 999 if they are drowsy, floppy or hard to wake. Never make anyone sick to get "
    "it out. A mouthful or two does no harm - the salt just makes you thirsty, so rinse your "
    "mouth and drink fresh water - and boiling it is no help, because the water steams off and "
    "the salt stays.")


def _said_already(opening, memory, keep=3):
    opening = opening.lower()
    for turn in (memory.get("turns") or [])[-keep:]:
        if isinstance(turn, dict) and opening in (turn.get("bot") or "").lower():
            return True
    return False


def _sea_water_reply(memory, understood):
    from .pets import _pet_in_the_talk, _pet_salt_water
    if _pet_in_the_talk(memory, understood):
        if _said_already("ring the vet now", memory):
            return ("Same as before, and it still stands: ring the vet now and say how much salt "
                    "water and when. Being sick, wobbly or drowsy in the next few hours is a "
                    "same-day visit, not a wait and see, and keep the fresh water away until the "
                    "vet has said otherwise.")
        return _pet_salt_water(memory, understood)
    line = ((understood or {}).get("clean") or "").lower()
    if SEA_WATER_ALARM.search(line):
        return SEA_WATER_ALARM_REPLY
    return (
        "A mouthful or two of sea water does no harm: the salt in it just makes you thirsty, so "
        "rinse your mouth out and drink some fresh water. Boiling it is no help - the water "
        "steams off and the salt stays, so it gets saltier. A child or an adult who has swallowed "
        "a lot of it - or who is being sick, dizzy or confused - needs 111, and 999 if they are "
        "drowsy or hard to wake. Never make anyone sick to get it out.")


ENTRIES.append(entry(
    "body-sea-water",
    (("sea water", "salt water", "saltwater", "seawater", "salty water", "sea"),
     ("drank", "drink", "drinking", "swallowed", "swallow", "mouthful", "gulp", "gulped",
      "sick", "vomiting", "thirsty", "sipped", "safe", "harm", "boil", "boiling", "boiled")),
    _sea_water_reply,
    avoid=("dog", "dogs", "cat", "cats", "puppy", "puppies", "kitten", "pup", "pet", "pets",
           "vet", "hamster", "rabbit", "horse", "pony", "livestock",
           "wash", "washing", "rinsed the", "soak", "gargle", "boil pasta", "boil potatoes",
           "boiled pasta", "cooking water", "for pasta", "to boil", "boiling pasta", "potatoes",
           "bath", "drown", "drowned",
           "swim", "swimming", "swimmer", "paddle", "paddling", "lido", "beach", "tide",
           "rip current", "wetsuit")))

REGION_BIAS = {"toe": 3}

EXTRA_AVOID["toe"] = ("run", "runs", "running", "jog", "jogging", "jogged", "ran", "miles",
                      "mileage", "after a run", "my run", "long run", "treadmill", "triathlon")

OBJECT_OWNERS = frozenset("""
table tables chair chairs desk desks bed beds sofa sofas couch couches settee settees stool
stools shelf shelves cupboard cupboards wardrobe wardrobes drawer drawers door doors gate
gates fence fences car cars bike bikes bicycle bicycles pram prams buggy buggies wheelchair
wheelchairs glasses sunglasses shoe shoes boot boots trainer trainers sandal sandals ladder
ladders machine machines printer printers laptop laptops phone phones window windows wall
walls floor floors ceiling ceilings roof roofs oven ovens fridge fridges
bag bags strap strap braces brace pillow pillows sleeve sleeves
chicken chickens turkey turkeys duck ducks goose lamb fish
bedroom bedrooms room rooms lounge kitchen bathroom loft attic landing hallway study office
garage garages garden gardens
""".split())
THING_PARTS = frozenset("""
leg legs back arm arms heel heels head foot feet toe toes knee knees hand hands finger
fingers thumb elbow shoulder hip shin spine joint neck sole
""".split())
_PERSON_OWNER = PERSON_NOUNS | frozenset("my your his her their our whose".split())
_DETERMINERS = frozenset("the a an this that these those".split())
HURT_WORDS = frozenset(word for word in HURT if " " not in word)
_POSSESSIVES = frozenset("my your his her its their our".split())


def _owner_word(word):
    word = word.strip(string.punctuation)
    if word.endswith("'s"):
        word = word[:-2]
    return word in OBJECT_OWNERS or (word.endswith("s") and word[:-1] in OBJECT_OWNERS)


def _a_thing_owns_the_part(understood):
    words = understood.get("words")
    if not isinstance(words, list):
        words = str(understood.get("clean") or "").lower().split()
    words = [str(word).lower() for word in words]
    for index, word in enumerate(words):
        if word.strip(string.punctuation) not in THING_PARTS:
            continue
        if index and _owner_word(words[index - 1]):
            return True
        nxt = [word.strip(string.punctuation) for word in words[index + 1:index + 4]]
        nxt = [word for word in nxt if word and word not in _DETERMINERS]
        if nxt and nxt[0] not in THING_PARTS and _owner_word(nxt[0]):
            return True
        between = [word.strip(string.punctuation) for word in words[index + 1:index + 5]]
        for preposition in ("in", "inside"):
            if preposition in between:
                cut = between.index(preposition)
                if not any(word in HURT_WORDS for word in between[:cut]):
                    rest = [word for word in between[cut + 1:] if word]
                    rest = [word for word in rest if word not in _DETERMINERS]
                    rest = [word for word in rest if word not in _POSSESSIVES]
                    if rest and _owner_word(rest[0]):
                        return True
                break
        after = words[index + 1:index + 5]
        if after and after[0].strip(string.punctuation) == "of":
            rest = [word.strip(string.punctuation) for word in after[1:]]
            rest = [word for word in rest if word and word not in _DETERMINERS]
            while len(rest) > 1 and rest[0] in _POSSESSIVES:
                rest = rest[1:]
            if rest and rest[0] not in _PERSON_OWNER and rest[0] not in THING_PARTS:
                return True
            if any(_owner_word(word) for word in rest):
                return True
    return False


def the_part_that_hurts(text):
    line = " ".join(str(text or "").lower().split())
    found = re.findall(r"[a-z']+", line)
    if not found:
        return None
    if not (set(found) & HURT_WORDS or "killing" in found):
        return None
    if _a_thing_owns_the_part({"clean": line, "words": found}):
        return None
    for name, parts, _reply in REGIONS:
        if any(part in found for part in parts):
            return name
    return None


ASKING_ABOUT_A_PART = ("what should i do about", "what should i do for",
                       "what can i do about", "what can i do for",
                       "what do i do about", "what do i do for",
                       "what can i do", "what should i do",
                       "whats the best thing for", "what is the best thing for",
                       "best thing for", "best thing to do for",
                       "anything i can do about", "anything i can do for",
                       "is there anything for", "is there anything i can do",
                       "what helps", "what helps with", "what helps a", "what helps my",
                       "what is wrong with", "whats wrong with", "what's wrong with",
                       "what could be wrong with", "what might be wrong with",
                       "whats the matter with", "what is the matter with",
                       "whats going on with", "what is going on with",
                       "whats good for", "what is good for",
                       "whats wrong with", "what is wrong with", "what could be wrong with",
                       "what might be wrong with", "what do you think is wrong with",
                       "any idea whats wrong with", "any idea what is wrong with",
                       "what have i done to", "what did i do to my", "whats up with my",
                       "is something wrong with my", "should i worry about my",
                       "how bad is my", "is it broken", "is it fractured", "is it dislocated",
                       "have i broken", "have i fractured", "did i break", "did i fracture",
                       "is it torn", "have i torn", "is it snapped",
                       "remedy for", "any tips for", "any advice for",
                       "how do i ease", "how do i relieve",
                       "what exercises", "which exercises", "any exercises",
                       "best exercises", "good exercises", "exercises for", "exercise for",
                       "exercises to", "exercises help", "exercises that help",
                       "what exercise", "which exercise", "best exercise", "any exercise",
                       "what stretches", "which stretches", "any stretches",
                       "best stretches", "good stretches", "stretches for")

ASKED_AGAIN = ("what about my", "how about my", "what about our", "how about our",
               "what about your", "how about your")


_BACK_VERB_BEFORE = frozenset((
    "come", "comes", "coming", "came", "go", "goes", "going", "went", "gone", "bring", "brings",
    "bringing", "brought", "send", "sends", "sending", "sent", "put", "puts", "putting", "get",
    "gets", "getting", "got", "take", "takes", "taking", "took", "taken", "give", "gives",
    "giving", "gave", "given", "keep", "keeps", "keeping", "kept", "hold", "holds", "holding",
    "held", "pay", "pays", "paying", "paid", "call", "calls", "calling", "called", "ring",
    "rings", "ringing", "rang", "phone", "phones", "phoning", "phoned", "text", "texts",
    "texting", "texted", "write", "writes", "writing", "wrote", "hand", "hands", "handing",
    "be", "is", "was", "are", "were", "being", "been", "way", "step", "steps", "far",
    "cut", "cuts", "cutting", "fight", "fights", "fighting", "hit", "hits", "hitting",
))


_ALSO_THE_BACK = frozenset(("backache", "back's", "spine", "lumbar", "sciatica", "pelvis",
                            "hips"))

_BACK_IS_A_NOUN_AFTER = frozenset(("pain", "aches", "ache", "trouble", "problems", "problem",
                                   "soreness", "strain", "spasms", "spasm"))


def _reading_words(reading):
    if not isinstance(reading, dict):
        return []
    said = reading.get("words")
    if said:
        return [str(word).lower().strip(string.punctuation) for word in said]
    line = reading.get("clean") or reading.get("text") or ""
    return re.findall(r"[a-z']+", str(line).lower())


def _the_back_is_a_back(understood):
    if not isinstance(understood, dict):
        return True
    words = _reading_words(understood)
    leaned = understood.get("leans_on") or {}
    if isinstance(leaned, dict):
        words += _reading_words(leaned)
    if not words:
        return True
    if _ALSO_THE_BACK.intersection(words):
        return True
    for index, word in enumerate(words):
        if word != "back":
            continue
        if words[index + 1:index + 2] and words[index + 1] in _BACK_IS_A_NOUN_AFTER:
            return True
        if index and words[index - 1] in _BACK_THEIRS:
            return True
        if index and words[index - 1] in _BACK_VERB_BEFORE:
            continue
        if index and words[index - 1] in _BACK_DESCRIBED:
            return True
        if words[index + 1:index + 2] and words[index + 1] in _BACK_IS_A_RETURN:
            continue
        if _a_verb_earlier_took_it(words, index):
            continue
        return True
    return False


_BACK_IS_A_RETURN = frozenset(("to", "into", "onto", "towards", "toward"))

_BACK_THEIRS = frozenset(("my", "his", "her", "their", "our", "your", "the", "a", "an", "its",
                          "this", "that", "these", "those", "mine", "hers", "theirs", "ours"))
_BACK_DESCRIBED = frozenset("""
stiff sore bad aching achy painful lower upper middle tight weak dodgy old broken fragile seized
knackered tired poor
""".split())
_BACK_TAKING_A_THING = frozenset("""
want wants wanted wanting need needs needed needing ask asks asked asking owe owes owed
get gets getting got give gives giving gave given send sends sending sent take takes taking
took taken pay pays paying paid bring brings bringing brought keep keeps keeping kept put puts
putting hand hands handing hold holds holding held call calls calling called ring rings ringing
rang text texts texting texted write writes writing wrote throw throws threw pull pulls pulled
""".split())
_BACK_CLAUSE_JOIN = frozenset(("and", "but", "then", "so", "because", "when", "if", "before",
                               "after", "until", "while", "or"))


def _a_verb_earlier_took_it(words, index):
    seen = 0
    for at in range(index - 1, -1, -1):
        word = words[at]
        if word in _BACK_CLAUSE_JOIN:
            return False
        if word in _BACK_TAKING_A_THING:
            return True
        seen += 1
        if seen > 4:
            return False
    return False


def _the_back_is_a_back_that_is_someones(understood):
    return _the_part_is_a_persons(understood) and _the_back_is_a_back(understood)


def _the_part_is_not_a_standing_trouble(understood):
    line = str((understood or {}).get("clean") or (understood or {}).get("text") or "").lower()
    if _REPORTED_COMPLAINT.search(line):
        return True
    return not any(w in line for w in _STANDING_TROUBLE)


def _a_region_guard(name):
    if name == "back":
        def _the_back_is_the_persons_and_not_a_standing_trouble(understood):
            return (_the_back_is_a_back_that_is_someones(understood)
                    and _the_part_is_not_a_standing_trouble(understood))

        return _the_back_is_the_persons_and_not_a_standing_trouble

    def _the_part_is_the_persons_and_not_a_standing_trouble(understood):
        return (_the_part_is_a_persons(understood)
                and _the_part_is_not_a_standing_trouble(understood))

    return _the_part_is_the_persons_and_not_a_standing_trouble

_KEPT_AWAKE = re.compile(
    r"\b(?:keeps?|kept|keeping|stops?|stopped|stopping|prevents?|prevented|preventing|held|holding)"
    r"\s+me\s+(?:up\b|awake\b|off\s+my\s+feet\b|from\s+\w+ing\b|from\s+sleep\b|"
    r"sleeping\b|walking\b|standing\b|sitting\b|driving\b|working\b|"
    r"lying\b|sleep\b)"
    r"|\b(?:wont|won t|wouldnt|would not|doesnt|does not|will not|didnt|did not)"
    r"\s+let\s+me\s+(?:sleep|sleeping|nap|rest|lie\s+down|lie\s+still|lie\s+flat|"
    r"sit\s+down|stand\s+up|walk|drive|get\s+up|get\s+out\s+of\s+bed|roll\s+over)\b"
)


_A_PART_IN_THE_TABLE = re.compile(
    r"\b(?:%s)\b" % "|".join(sorted({re.escape(p)
                                     for _n, parts, _r in REGIONS for p in parts},
                                    key=len, reverse=True)))


def _a_part_keeps_me_from_something(words):
    line = (words or "").lower()
    return bool(_KEPT_AWAKE.search(line) and _A_PART_IN_THE_TABLE.search(line))

BREAK_SAID = ("broken", "broke", "fractured", "fracture", "cracked", "crack", "snapped")
A_PART_NO_KNOCK_TEST = ("ribs", "tailbone", "groin")


def _the_breaks_it_says(name):
    return BREAK_SAID if name in A_PART_NO_KNOCK_TEST else ()


ENTRIES += [entry(f"sore-{name}",
                  (parts, HURT + ASKING_ABOUT_A_PART + ASKED_AGAIN + _the_breaks_it_says(name)),
                  reply,
                  avoid=AVOID + EXTRA_AVOID.get(name, ()),
                  bias=REGION_BIAS.get(name, 0),
                  guard=_a_region_guard(name),
                  shape=(_a_part_keeps_me_from_something,))
            for name, parts, reply in REGIONS]

SOFT_TISSUE = ("arm", "arms", "forearm", "leg", "legs", "thigh", "thighs", "calf",
               "calves", "shin", "shins", "wrist", "wrists", "hand", "hands", "elbow",
               "elbows", "shoulder", "shoulders", "knee", "knees", "ankle", "ankles",
               "foot", "feet", "thumb", "thumbs", "finger", "fingers", "collarbone")
_SOMEONE_ELSE = frozenset("""
he him his she her hers they them their theirs son daughter child kid kids baby toddler
husband wife partner boyfriend girlfriend mum mom mother dad father brother sister friend mate
nephew niece grandson granddaughter grandad grandma granny uncle aunt cousin
""".split())


_A_WHILE_AGO = re.compile(
    r"\b(?:last|past)\s+(?:week|month|year|summer|winter|christmas|autumn|spring)\b"
    r"|\b(?:a|one|two|three|four|five|six|seven|eight|nine|ten|\d+)\s*(?:days?|weeks?|months?|years?)\s+ago\b"
    r"|\b(?:a\s+)?(?:few|couple\s+of)\s+(?:weeks|months|years)\s+ago\b"
    r"|\b(?:weeks|months|years) ago\b|\byears back\b|\byears since\b"
    r"|\bwhen (?:he|she|they|my \w+) (?:was|were)\b|\bused to\b")


_IT_HAPPENED_TO = frozenset("""
fell fallen falling fell trip tripped tumbling tumbled landed hit smacked banged bashed
knocked injured sprained twisted cricked wrenched
""".split())
_TO_HURT_A_PART = frozenset("hurt hurting".split())


def _it_is_somebody_elses_part(understood):
    if not isinstance(understood, dict) or not _the_part_is_a_persons(understood):
        return False
    words = [str(word).lower() for word in understood.get("words") or ()
             if isinstance(word, str)]
    people = {word[:-2] if word.endswith("'s") else word for word in words}
    if not people & _SOMEONE_ELSE:
        return False
    said = str(understood.get("clean") or understood.get("text") or "").lower()
    if _A_WHILE_AGO.search(said):
        return False
    parts = [at for at, word in enumerate(words) if word in SOFT_TISSUE]
    if not parts:
        return False
    if any(word in _IT_HAPPENED_TO for word in words) or "went over" in said:
        return True
    return any(word in _TO_HURT_A_PART and at < parts[0] for at, word in enumerate(words))


ENTRIES.append(entry(
    "hurt-limb-someone",
    (("hurt", "hurts", "hurting", "injured", "banged", "knocked", "bashed",
      "fell", "fell off", "fell over", "fallen", "tripped", "tumbled",
      "landed on"),
     SOFT_TISSUE),
    "Check it where they are: whether it is swollen or bruising fast, whether they will use it "
    "at all, and whether it looks bent. Ice it for 15 minutes, keep it raised, and give "
    "children's paracetamol if their age allows. A limb they will not use or let you move, one "
    "that looks bent, or swelling that comes up fast is A&E the same day; a bang on the head with "
    "sickness, drowsiness or a knockout is 999.",
    guard=_it_is_somebody_elses_part,
    avoid=("dog", "cat", "puppy", "horse", "kitten")))

WEEKS = ("for a week", "for two weeks", "for a fortnight", "for three weeks", "for weeks",
         "for a month", "for months", "for a year", "for years", "for ages", "for a while",
         "all week", "all month", "a week now", "weeks now", "months now", "a few weeks",
         "a couple of weeks", "two weeks", "three weeks", "weeks", "months",
         "the last few months", "the past few months", "the last few weeks",
         "the past few weeks", "on and off for")

_SPORT_WORDS = ("run", "runs", "running", "ran", "jog", "jogging", "jogged", "miles", "treadmill",
                "gym", "workout", "work out", "weights", "cycling", "cycle", "swim",
                "swimming", "football", "rugby", "netball", "hockey", "tennis", "marathon",
                "half marathon", "parkrun", "training", "training for", "after every run")

_WEEKS_DRILL = {
    "back": "two short sessions a week of a slow bridge lying on your back, or standing and "
            "lifting one knee at a time",
    "spine": "two short sessions a week of a slow bridge lying on your back",
    "knee": "two short sessions a week of sit-to-stand from a chair, ten times each, plus a walk",
    "kneecap": "two short sessions a week of sit-to-stand from a chair, ten times each",
    "hip": "two short sessions a week of sit-to-stand from a chair and a walk",
    "shoulder": "two short sessions a week of a slow wall push-up, and the pendulum swing (lean "
                "forward, let the arm hang, circle it slowly)",
    "neck": "chin tucks, ten at a time, twice a day, and a look at where your screen sits",
    "foot": "a calf stretch against a wall before your first steps in the morning, and a rolled "
            "towel under the arch",
    "heel": "a calf stretch against a wall before your first steps, and shoes with a firm sole",
    "ankle": "heel raises holding a chair, ten at a time",
    "wrist": "a slow curl with a light weight, palm up and palm down, and breaks from gripping",
    "hand": "a slow curl with a light weight, and breaks from gripping",
    "thumb": "a slow curl with a light weight, and breaks from gripping",
    "elbow": "a light weight lifted slowly, palm down then palm up",
    "leg": "two short sessions a week of a slow squat to a chair, plus a walk",
    "calf": "two short sessions a week of a slow squat to a chair and heel raises",
    "thigh": "two short sessions a week of a slow squat to a chair, plus a walk",
    "hamstring": "a slow squat to a chair and a gentle hamstring stretch after a warm bath",
    "shin": "a walk, and calf raises holding a chair",
    "rib": "keeping your breathing normal rather than in shallow sips, and a cushion pressed "
           "against that side when you cough",
    "toe": "shoes with room in them, and a warm soak",
}


def _line_words(understood):
    if not isinstance(understood, dict):
        return set()
    return set(w.lower() for w in understood.get("words") or () if isinstance(w, str))


def _how_long(understood):
    said = str((understood or {}).get("clean") or (understood or {}).get("text") or "").lower()
    if re.search(r"\byear", said):
        return "for months or years"
    if re.search(r"\bmonth", said):
        return "for months"
    return "for a week or more"


_PREGNANT_WORDS = ("pregnant", "pregnancy", "expecting", "trimester", "baby due")

_BACK_AFTER_A_VERB = re.compile(
    r"\b(?:was|were|is|are|be|been|being|am|im|came|come|comes|coming|went|go|goes|going|gone|"
    r"get|gets|getting|got|give|gives|"
    r"giving|gave|given|takes?|took|taken|brings?|brought|sends?|sent|pays?|paid|calls?|"
    r"called|sits?|sat|cuts?|holds?|held|puts?|stepped|steps?|looks?|looked|turns?|turned|"
    r"fights?|fought|throws?|threw|pulls?|pulled|comes?|coming|"
    r"mov(?:e|es|ed|ing)|relocat(?:e|es|ed|ing))\s+"
    r"(?:(?:it|them|him|her|me|us|you|one)\s+)?back\b")


_BACK_BEFORE_A_PLACE = re.compile(
    r"(?<!\bmy )(?<!\bhis )(?<!\bher )(?<!\byour )(?<!\btheir )(?<!\bour )(?<!\bthe )"
    r"(?<!\bthis )(?<!\bthat )(?<!\ba )(?<!\ban )"
    r"\bback\s+(?:at|to|from|in|on)\s+(?:the\s+|my\s+|her\s+|his\s+)?"
    r"(?:work|school|home|college|uni|university|office|nursery|holidays?|shift|shifts|"
    r"placement|term|nights?|days?|monday|tuesday|wednesday|thursday|friday|saturday|sunday)\b")

_BACK_HOME = re.compile(
    r"(?<!\bmy )(?<!\bhis )(?<!\bher )(?<!\byour )(?<!\btheir )(?<!\bour )(?<!\bthe )"
    r"(?<!\bthis )(?<!\bthat )(?<!\ba )(?<!\ban )"
    r"\bback\s+(?:home|in\s+with|with\s+(?:my|her|his|our|the)\s+(?:parents|mum|dad|mother|"
    r"father|family|folks)|to\s+(?:my|her|his|our)\s+(?:parents|mum|dad|mother|father|home))\b")


def _back_is_a_direction(understood):
    text = str((understood or {}).get("clean") or (understood or {}).get("text") or "").lower()
    said = len(re.findall(r"\bback\b", text))
    seen = (len(_BACK_AFTER_A_VERB.findall(text)) + len(_BACK_BEFORE_A_PLACE.findall(text))
            + len(_BACK_HOME.findall(text)))
    return bool(said) and seen >= said


def _a_back_in_the_chat(memory):
    for turn in (memory or {}).get("turns") or []:
        if not isinstance(turn, dict):
            continue
        said = str(turn.get("user") or "")
        if re.search(r"\bback\b", said.lower()) and not _back_is_a_direction({"text": said}):
            return True
    return False


def _sore_weeks_reply(memory, understood):
    said = str((understood or {}).get("clean") or (understood or {}).get("text") or "").lower()
    parts = [said]
    for key in ("text", "plain"):
        value = (understood or {}).get(key)
        if isinstance(value, str):
            parts.append(value.lower())
    for key in ("words", "background"):
        for word in (understood or {}).get(key) or ():
            if isinstance(word, str):
                parts.append(word.lower())
    turns = (memory or {}).get("turns") or []
    if turns and isinstance(turns[-1], dict) and isinstance(turns[-1].get("user"), str):
        parts.append(turns[-1]["user"].lower())
    if any(word in " ".join(parts) for word in _PREGNANT_WORDS):
        return None
    part = (_part_named(_line_words(understood), understood)
            or _part_named(_words(understood), understood) or "part")
    if (part == "back" and _back_is_a_direction(understood)
            and not _a_back_in_the_chat(memory)):
        return None
    article = "An" if part[:1] in "aeiou" else "A"
    drill = _WEEKS_DRILL.get(part, "two short sessions a week of the movement you want to "
                                   "return to, stopping short of pain")
    return (article + " " + part + " that has been sore " + _how_long(understood) + " is usually "
            "a tendon or a joint asked for more than it is used to: keep going as far as is "
            "comfortable, and add " + drill + ". If it is no better after six weeks, wakes you "
            "up, or keeps coming back, ask your GP about physio. Ring 111 sooner for numbness, a "
            "part that gives way, or pain with a fever or weight loss.")


DECIDE_ASK = ("see someone", "see a doctor", "see the doctor", "see a gp", "see my gp",
              "go to the doctor", "go to a doctor", "go to my gp", "should i see",
              "do i need to see", "worth seeing", "see a physio", "see the physio",
              "get it looked at", "get it seen", "should i get it checked", "worth getting checked",
              "checked out", "get it checked", "get my checked",
              "should i go to the doctor", "do i need to get it checked", "worth going to the",
              "should i be worried", "is it worth going",
              "get it looked at", "get my", "looked at", "looked over", "get it seen to",
              "should i bother", "bother going", "bother seeing", "any point in",
              "worth it to", "worth a visit", "worth a trip", "worth making an appointment")

SEE_DOCTOR_AVOID = (
    "lump", "lumps", "gland", "glands", "node", "nodes", "breast", "lump on",
    "chest", "heart", "throat", "tooth", "teeth", "gum", "gums", "ear", "ears", "head",
    "headache", "headaches", "migraine", "cough", "cold", "flu", "sore throat", "stomach",
    "tummy", "belly", "toothache", "jaw", "period", "periods", "pregnant", "pregnancy",
    "son", "daughter", "child", "kid", "kids", "baby", "toddler", "husband", "wife",
    "partner", "mum", "mom", "mother", "dad", "father", "friend", "dog", "cat", "puppy",
    "sick", "nauseous", "vomit", "dizzy", "faint", "breathless", "sweating", "numb",
    "numbness", "pins and needles", "cant pee", "can't pee", "blood", "bleeding",
    "gave way", "gives way", "locked", "locks", "swollen", "swelling", "hot and swollen",
    "go back", "going back", "went back", "come back", "coming back", "back to", "back at",
    "nursing", "career", "careers", "retrain", "retraining", "job", "jobs", "degree",
    "university", "college", "course", "shift", "my old",
    ) + FALL

SEE_DOCTOR_PARTS = ("back", "leg", "legs", "knee", "knees", "hip", "hips", "shoulder",
                    "shoulders", "neck", "ankle", "ankles", "wrist", "wrists", "elbow",
                    "elbows", "foot", "feet", "arm", "arms", "hand", "hands", "joint",
                    "joints", "side", "spine", "thigh", "thighs", "shin", "shins", "calf",
                    "heels", "heel", "finger", "fingers", "thumb", "thumbs",
                    "pain", "pains", "hurts", "hurting", "ache", "aches", "aching", "sore")


ACHE_WORDS = ("ache", "aches", "aching", "achey", "achy", "sore", "soreness", "stiff",
              "stiffness", "tender")
EXERCISE_AFTER = ("after the gym", "after gym", "after weights", "after lifting", "after a workout",
                  "after my workout", "after the workout", "after exercise", "after exercising",
                  "after a session", "after a class", "after training", "after running",
                  "after a run", "after the run", "after a jog", "the next day", "day after",
                  "next day")


_SORENESS_WORDS = frozenset(("sore", "soreness", "aching", "achy", "achey", "ache", "aches",
                             "stiff", "stiffness", "tender", "hurt", "hurts", "hurting"))


def _the_day_after_new_exercise(understood):
    if not _line_words(understood) & _SORENESS_WORDS:
        return False
    clean = str((understood or {}).get("clean") or "").lower()
    return any(phrase in clean for phrase in EXERCISE_AFTER)


def _see_doctor_reply(memory, understood):
    if _the_day_after_new_exercise(understood):
        return None
    part = _part_named(_line_words(understood), understood)
    opening = "Go by how long it has been going: "
    if part:
        article = "An" if part[:1] in "aeiou" else "A"
        opening = article + " " + part + " like that: "
    return opening + (
        "give it two to six weeks if it is steady or easing, and book sooner if it is getting "
        "worse, waking you at night or stopping you doing normal things. Go today if it came on "
        "suddenly or after a fall, or comes with a fever, numbness or pins and needles. Ask "
        "about physio when you ring; in most areas you can refer yourself.")


def _a_part_in_a_decision_is_a_part(understood):
    words = set(_reading_words(understood))
    if "back" not in words or (words - {"back"}) & set(SEE_DOCTOR_PARTS):
        return True
    return _the_back_is_a_back(understood)


ENTRIES.append(entry("see-about-a-part", (DECIDE_ASK, SEE_DOCTOR_PARTS),
                     _see_doctor_reply, bias=2, avoid=SEE_DOCTOR_AVOID,
                     guard=_a_part_in_a_decision_is_a_part))

_DECISION_WORDS = frozenset("""
a about all also am an and any anything are as at be been being both but by can check checked
could did do does doing doctor doctors each even ever for from get gets getting go goes going got gp
gps had has have having he her here him his how i if in into is it its just look looked looking me
more most much must my myself need needed needs no nor not now of off on once one only or other our
out over own rather really same see seeing seen shall she should so some someone something still
first anyway
such sure than that the their them then there these they thing things this those through to too
under up us very wait waiting was we were what when where whether which while who why will with
worth worthwhile would yet you your
""".split())


def _a_bare_decision(understood):
    words = _line_words(understood)
    if not words:
        return False
    return all(word in _DECISION_WORDS for word in words)


def _see_doctor_decision(memory, understood):
    reply = _see_doctor_reply(memory, understood)
    if reply is None or _part_named(_line_words(understood), understood):
        return reply
    return reply.replace(
        " Ask about physio when you ring; in most areas you can refer yourself.", "")

ENTRIES.append(entry("see-about-it",
                     (DECIDE_ASK, ("doctor", "gp", "see someone", "someone about",
                                   "checked", "checked out", "looked at", "seen")),
                     _see_doctor_decision, bias=0, guard=_a_bare_decision,
                     ask=("should i", "do i", "can i", "could i", "would i", "shall i",
                          "is it", "any point", "worth"),
                     avoid=SEE_DOCTOR_AVOID + (
                         "appointment", "book", "booking", "register", "surgery",
                         "physio", "physiotherapy", "chiropractor",
                         "mental", "anxiety", "anxious", "depressed", "depression",
                         "counselling", "counselor", "counsellor", "therapy", "therapist",
                         "panic", "stress", "stressed", "self harm", "suicidal",
                         "dentist", "vet", "optician",
                         "wart", "warts", "verruca", "verrucas",
                         "weekend", "weekends", "saturday", "sunday", "bank holiday",
                         "out of hours", "evening", "evenings")))

ENTRIES.append(entry("see-a-dentist",
                     (DECIDE_ASK, ("dentist", "dentists", "dental", "nhs dentist",
                                   "dental practice", "dental surgery", "emergency dentist",
                                   "out of hours dentist", "dentist or a doctor")),
                     "Go by what the tooth is doing: a twinge with cold that settles, or a check-up "
                     "you are overdue, is an ordinary appointment. Ring the dentist today if it "
                     "aches at night or keeps you awake, if there is swelling in your face or "
                     "under the jaw, a fever, a lost filling or crown that hurts, or bleeding that "
                     "will not stop. A tooth knocked right out goes straight back into the socket, "
                     "by the crown and not the root, and you are seen within the hour; ring 111 "
                     "for the out-of-hours dental service if your practice is shut.",
                     ask=("should i", "do i", "can i", "could i", "would i", "shall i",
                          "is it", "any point", "worth"),
                     avoid=("register", "registering", "registration", "taking new",
                            "new patients", "nhs patients", "how do i get", "find a",
                            "find an", "nearest", "near me", "how often", "how long since",
                            "havent been", "haven't been", "never been", "years", "ages",
                            "scared", "nervous", "afraid", "terrified", "dreading", "phobia",
                            "embarrassed", "cost", "costs", "price", "how much", "private",
                            "nhs band", "band 1", "band 2", "band 3", "free", "afford",
                            "whitening", "whiten", "braces", "implant", "implants",
                            "denture", "dentures", "appointment at", "cancel", "check up",
                            "cold", "hot", "sweet", "bite", "biting", "chew", "chewing",
                            "sensitive", "bleeding", "bleeds", "swollen", "swelling", "chipped",
                            "broken", "hole", "decay", "abscess", "went", "knocked out", "fell out",
                            "came out", "wisdom", "gums", "gum", "mouth", "jaw", "ache")))

_GONE_BACK = ("went", "gone", "goes", "put my back out", "put it out", "pulled my back",
              "threw my back out", "thrown my back out", "in spasm", "locked", "did my back in")


_A_VERB_TOOK_THE_BACK = re.compile(
    r"\b(?:text|texts|texted|texting|message|messages|messaged|messaging|msg|dm|dm'd|"
    r"call|calls|called|calling|ring|rings|rang|ringing|phone|phones|phoned|phoning|"
    r"email|emails|emailed|emailing|write|writes|wrote|written|writing|reply|replies|replied|"
    r"replying|answer|answers|answered|answering|hear|hears|heard|hearing|get|gets|getting|got|"
    r"pay|pays|paid|paying|send|sends|sent|sending|bring|brings|brought|push|pushes|pushed|"
    r"hold|holds|held|look|looks|looked|turn|turns|turned|talk|talks|talked|take|takes|took|"
    r"step|steps|stepped|sit|sits|sat|lean|leans|leant|lie|lies|lay|fall|falls|fell|walk|walks|"
    r"walked|move|moves|moved|drive|drives|drove|run|runs|ran|hit|hits|fight|fights|fought|"
    r"come|comes|came|coming|go|goes|going|went|gone|"
    r"stretch|stretches|stretched|stretching|shrink|shrinks|shrank|shrunk|shrinking)"
    r"\s+(?:(?:me|him|her|us|them|you|it|myself|yourself|himself|herself|themselves)\s+)?back\b"
)
_THE_BACK_IS_THEIRS = re.compile(
    r"\b(?:my|your|his|her|our|their|the|this|that)\s+back\b"
    r"|\b(?:sore|bad|lower|upper|stiff|aching|soreness|painful)\s+back\b"
    r"|\bback\s+(?:pain|ache|aches|aching|hurts?|hurting|problem|trouble|spasm|went|gone)\b"
    r"|\bback\s+(?:is\s+)?(?:killing|kills)\b")


def _the_back_is_the_persons(understood):
    clean = str((understood or {}).get("clean") or "").lower().replace("\u2019", "'")
    if not _A_VERB_TOOK_THE_BACK.search(clean):
        return True
    return bool(_THE_BACK_IS_THEIRS.search(_A_VERB_TOOK_THE_BACK.sub("  ", clean)))


ENTRIES += [entry(f"sore-{name}-weeks", (parts, WEEKS),
                  _sore_weeks_reply,
                  avoid=tuple(w for w in AVOID if w not in STANDING) + _GONE_BACK
                  + _SPORT_WORDS
                  + ("pregnant", "pregnancy", "expecting", "trimester", "weeks pregnant",
                     "months pregnant"),
                  guard=_the_back_is_the_persons if name == "back" else None,
                  )
            for name, parts, reply in REGIONS]


_BAD_PART_MOVEMENT = ("exercises", "exercise", "stretches", "stretching", "physio")
_STANDING_TROUBLE = ("bad", "badly", "dodgy", "gammy",
                     "strengthen", "strengthening", "stronger", "build up", "building up",
                     "crap")
_BAD_PART_WORDS = _STANDING_TROUBLE + _BAD_PART_MOVEMENT
_CARRIES_WEIGHT = ("back", "spine", "knee", "kneecap", "hip", "ankle", "foot", "heel",
                   "leg", "calf", "thigh", "hamstring", "shin", "toe")

ENTRIES += [entry("bad-back",
                  (tuple(w for _name, parts, _r in REGIONS if _name == "back"
                         for w in parts), _BAD_PART_WORDS),
                  "A back that gives trouble on and off is usually muscular, and what keeps it "
                  "quiet is strength and movement rather than rest: walk most days, and add two "
                  "short sessions a week of a slow bridge lying down or sit-to-stand from a "
                  "chair. Ask your GP about physio if it is stopping you sleep or work, and ring "
                  "111 the same day if you cannot pass urine, have numbness between your legs, or "
                  "it came on after a fall.",
                  bias=3,
                  guard=_the_back_is_the_persons,
                  avoid=tuple(w for w in AVOID
                              if w not in STANDING and w not in EXERCISE_DAY) + _GONE_BACK
                  + _SPORT_WORDS
                  + WEEKS
                  + ("pregnant", "pregnancy", "expecting", "weeks pregnant",
                     "months pregnant"))]


def _the_part_is_named_today(understood):
    if not the_part_that_keeps_grumbling(understood):
        return False
    said = (understood or {}).get("text")
    if not isinstance(said, str) or _REPORTED_COMPLAINT.search(said):
        return False
    typed = set(re.findall(r"[a-z']+", said.lower().replace("\u2019", "'")))
    return bool(_part_named(typed))


_REPORTED_COMPLAINT = re.compile(
    r"\b(?:i (?:get|have|had|keep getting|keep|suffer from|live with)|"
    r"i(?:'ve|ve) (?:got|had|been having))\b", re.I)


def _bad_part_reply(memory, understood):
    part = _part_named(_line_words(understood)) or _part_named(_words(understood)) or "joint"
    article = "An" if part[:1] in "aeiou" else "A"
    drill = _WEEKS_DRILL.get(part, "two short sessions a week of the movement you want to keep, "
                                    "stopping short of pain")
    instead = ("Swimming, cycling and a flat walk are the kind ones on the other days."
               if part in _CARRIES_WEIGHT
               else "Keep the rest of you moving, and use it as far as is comfortable.")
    return (article + " " + part + " that gives trouble on and off is usually weak muscle round "
            "a joint that does not like one particular movement, and building it up is what "
            "keeps it quiet: " + drill + ". " + instead + " Get it looked at if it gives way, "
            "locks, or swells up after a knock.")


ENTRIES += [entry("bad-" + name, (parts, _BAD_PART_WORDS), _bad_part_reply,
                  guard=_the_part_is_named_today,
                  bias=-1,
                  avoid=tuple(w for w in AVOID
                              if w not in STANDING and w not in EXERCISE_DAY) + _GONE_BACK
                  + tuple(w for w in _SPORT_WORDS
                          if w not in ("swim", "swimming", "cycle", "cycling"))
                  + WEEKS
                  + ("pulled", "pull", "strained", "sprain", "sprained", "torn", "tear",
                     "injured", "injury")
                  + ("pregnant", "pregnancy", "expecting", "weeks pregnant",
                     "months pregnant"))
            for name, parts, _reply in REGIONS if name not in ("back", "knee")]

_PROTECT_ASK = ("protect", "protects", "protecting", "protection",
                "look after", "looking after", "looks after",
                "take care of", "taking care of", "takes care of", "care for", "caring for",
                "keep strong", "keep it strong", "keep them strong", "keep healthy",
                "keep it healthy", "keep supple", "keep flexible",
                "avoid injury", "avoid injuring", "prevent injury", "prevent a strain")
_ALL_PART_WORDS = tuple(w for _name, spelled, _r in REGIONS for w in spelled)


_PROTECT_FILLERS = frozenset("""
    a an the and or of to for in on at with my your me it them i we you
    how do does did can could should would whats what is are be been
    best way ways good better keep keeps keeping well healthy strong stronger
    supple flexible care careful carefully properly safely help home
""".split())
_PROTECT_ALLOWED = _PROTECT_FILLERS | set(_ALL_PART_WORDS) | set(
    w for phrase in _PROTECT_ASK for w in phrase.split())


def _the_ask_names_nothing_else(understood):
    said = (understood or {}).get("clean") or (understood or {}).get("text") or ""
    if not isinstance(said, str):
        return False
    words = set(re.findall(r"[a-z']+", said.lower().replace("\u2019", "'")))
    return all(_in_the_allow_list(w) for w in words)


def _in_the_allow_list(word):
    if word in _PROTECT_ALLOWED:
        return True
    for tail in ("ing", "es", "s", "ed", "d"):
        stem = word[:-len(tail)] if word.endswith(tail) else ""
        if len(stem) >= 3 and stem in _PROTECT_ALLOWED:
            return True
    return False


def _protect_reply(memory, understood):
    part = (_part_named(_line_words(understood), understood)
            or _part_named(_words(understood), understood) or "joint")
    article = "An" if part[:1] in "aeiou" else "A"
    drill = _WEEKS_DRILL.get(part, "two short sessions a week of the movement you want to keep, "
                                    "stopping short of pain")
    if part in _CARRIES_WEIGHT:
        instead = ("Swimming, cycling and a flat walk are the kind ones on the other days. Warm "
                   "up before a big job, keep the load close to you when you lift, and change "
                   "position every half hour rather than holding one.")
    else:
        instead = ("Keep it moving every day rather than resting it, and keep it in the middle of "
                   "where it moves - not locked straight, not at the end of its range.")
    return (article + " " + part + " is protected by the muscle round it and by how you use it "
            "more than by anything you wear or avoid: " + drill + ". " + instead)


ENTRIES += [entry("protect-a-part", (_PROTECT_ASK, _ALL_PART_WORDS), _protect_reply,
                  guard=_the_ask_names_nothing_else,
                  avoid=STANDING + EXERCISE_DAY + WEEKS + _GONE_BACK +
                  ("injury", "injured", "hurt", "hurts", "hurting", "pain", "painful", "ache",
                   "aches", "aching", "sore", "swollen", "swelling",
                   "sun", "sunburn", "sunburnt", "burn", "burnt", "burned", "suncream",
                   "sun cream", "sunscreen", "bites", "bitten", "graze", "gravel",
                   "burn", "sting", "stung",
                   "eyes", "eye", "hearing", "ears", "ear", "teeth", "tooth", "gums",
                   "feet", "foot", "heel", "toes", "toe", "plantar",
                   "pregnant", "pregnancy", "expecting"))]

KNEE_WORDS = ("knee", "knees", "kneecap", "patella")
_STANDING_KNEE = ("bad", "badly", "dodgy", "weak", "trouble", "troublesome", "sore", "aching",
                  "aches", "worn", "wear and tear", "arthritis", "arthritic", "stiff",
                  "stiffness", "exercises", "exercise", "strengthen", "strengthening")
ENTRIES += [entry("bad-knee",
                  (KNEE_WORDS, _STANDING_KNEE),
                  "A knee that gives trouble is helped most by the muscle above it: sit-to-stands "
                  "from a chair, step-ups onto a low step and straight-leg raises, two or three "
                  "times a week, which builds the thigh muscle that takes the load off the joint. "
                  "Keep walking on the flat and skip deep squats and running downhill; a physio "
                  "can set the pace. A knee that locks, gives way or swells hot needs a GP.",
                  avoid=("twisted", "twist", "twisting", "sprain", "sprained", "tore", "torn",
                         "pop", "popped", "swollen", "swelling", "swells", "locked", "locks",
                         "gave way", "gives way", "gave out", "gave in", "snapped", "fell",
                         "fall", "fallen", "stairs", "stair", "upstairs", "downstairs",
                         "running", "run", "runner", "marathon", "football", "rugby", "squat",
                         "squats", "operated", "operation", "replacement", "replaced", "keyhole",
                         "arthroscopy", "injection", "steroid", "pregnant", "pregnancy",
                         "how long", "recovery", "recover", "crutches", "brace", "support",
                         "click", "clicks", "clicking", "clicked", "creak", "creaks", "creaking",
                         "noise", "noisy", "grind", "grinds", "grinding", "crackle", "crackles",
                         "crackling", "pops", "popping", "rattle", "rattles",
                         "walk", "walking", "walked", "steps", "step count", "how far"))]

BACK_PREGNANCY_KEEP = ("pregnant", "pregnancy", "weeks", "months", "for weeks", "for months",
                       "for a month", "for a fortnight", "a few weeks", "two weeks",
                       "three weeks", "a week now", "for ages")
PREGNANT = ("pregnant", "pregnancy", "pregnancies", "weeks pregnant", "months pregnant",
            "expecting a baby", "expecting", "trimester", "due in", "due next month",
            "due in a few weeks")
ENTRIES += [entry("back-pain-pregnant",
                  (("back", "lower back", "spine", "backache", "hips", "pelvis", "sciatica"),
                   PREGNANT),
                  "Back pain is very common in the second half of pregnancy: the weight sits out "
                  "in front, and the hormone that loosens your ligaments for the birth loosens "
                  "them everywhere. Paracetamol is the painkiller to use; steer clear of ibuprofen "
                  "and the other anti-inflammatories unless your midwife or doctor has said they "
                  "are fine for you. A maternity support belt, flat shoes, a warm bath and sleeping "
                  "on your side with a pillow between your knees all take the strain off, and your "
                  "midwife can refer you to a physiotherapist who deals with exactly this. Ring "
                  "your midwife or maternity unit the same day if the pain comes with bleeding, any "
                  "waters, a bad headache, blurred vision or swelling in your hands and face, a "
                  "temperature, stinging when you pass urine, or the baby moving less than usual.",
                  avoid=tuple(w for w in AVOID if w not in BACK_PREGNANCY_KEEP)
                  + ("not pregnant", "not expecting", "no longer pregnant"),
                  bias=2,
                  ask=("back", "hurts", "hurt", "ache", "aching", "backache", "back ache",
                       "bad back", "pain", "painful", "sore", "sciatica", "killing me", "agony"),
                  guard=_the_back_is_a_back),
          ]
_FEVER_ADVICE = ("Treat how they seem, not the number: cool clothes and plenty to drink do more "
                 "than the thermometer, plus paracetamol or ibuprofen at the dose on the pack if it "
                 "is making them miserable. Don't sponge with cold water or use both to chase the "
                 "number. Get seen the same day for a baby under three months with 38C, a rash that "
                 "will not fade under a glass, a stiff neck, breathing trouble, a fit, or a child "
                 "floppy or not drinking; ring 111 if unsure.")


_TAKE_A_TEMPERATURE = (
    "Use a digital thermometer under the tongue or in the armpit: wait 20 minutes after a hot or "
    "cold drink, tuck the tip under the tongue and keep it there until it beeps. In the armpit, "
    "dry the skin first and hold the arm clamped to the body, which reads about half a degree "
    "lower than the mouth. An ear thermometer has to point across towards the other eye to read "
    "right, and write the number and the time down if you are watching a fever.")


def _take_a_temperature(memory, understood):
    said = str((understood or {}).get("clean") or (understood or {}).get("text") or "").lower()
    if "without" in said:
        return ("Without a thermometer there is no number to take, so go by how they seem: a hot "
                "back or neck, flushed cheeks, shivering, and a hand on the skin is a poor guide "
                "either way. Don't pile layers on or take them off to chase a guess, and get "
                "anyone seen the same day if a baby under three months feels hot, or they are "
                "floppy, breathing fast or not drinking.")
    return _TAKE_A_TEMPERATURE


def _fever_reply(memory, understood):
    said = str((understood or {}).get("clean") or (understood or {}).get("text") or "").lower()
    if "how long" in said or "last" in said or "how many days" in said:
        return ("Most fevers from a virus settle within two or three days, and the last day is "
                "usually lower than the first. Have it looked at if it has been there five days or "
                "is still climbing, or if it goes away and comes back. Treat how they seem rather "
                "than the number, and get seen the same day for a baby under three months with "
                "38C, a rash that will not fade under a glass, a stiff neck, breathing trouble or "
                "a fit.")
    return _FEVER_ADVICE


_CHICKENPOX_TIMELINE = ("They are infectious from about two days before the rash appears until "
                        "every spot has crusted over, usually five days after the rash first "
                        "shows, which is when they can go back to school.")


def _chickenpox_reply(memory, understood):
    said = str((understood or {}).get("clean") or (understood or {}).get("text") or "").lower()
    if "ibuprofen" in said or "nurofen" in said or "brufen" in said:
        return ("No - avoid ibuprofen with chickenpox, because it is linked to a serious skin "
                "infection in children who have it. Use paracetamol at the dose on the pack, "
                "calamine or a cool bath for the itch, and keep the nails short so the spots do not "
                "scar. They are infectious from two days before the rash until every spot has "
                "crusted over, usually five days, which is when they can go back to school.")
    return (_CHICKENPOX_TIMELINE + " Calamine or a cool bath eases the itch, paracetamol helps the "
            "temperature and short nails stop the spots scarring; avoid ibuprofen. Ring the GP if "
            "a newborn, a pregnant woman or anyone with a weak immune system has been in contact.")


ENTRIES += [
    entry("fever-rest", (("fever", "temperature", "high temperature", "burning up", "shivery"),
                    ("bring down", "lower", "reduce", "get rid", "what can i do", "what should i do",
                     "how do i", "should i worry", "worried", "how long", "when should i",
                     "see a doctor", "doctor", "gp", "hospital", "paracetamol", "ibuprofen",
                     "calpol", "medicine", "worry", "help")),
          _fever_reply,
          avoid=("oven", "thermostat", "heating", "room", "house", "home", "fridge", "freezer",
                 "cook", "bake", "set the", "washing", "hob", "air fryer", "boiler", "bedroom",
                 "weather", "outside", "garden", "how hot", "the sea", "pool", "chickenpox",
                 "hay fever", "hayfever", "hay-fever", "pollen", "allergy season",
                 "glandular fever", "glandular", "scarlet fever", "scarlet",
                 "rheumatic fever", "dengue", "typhoid", "malaria")),
    entry("take-a-temperature",
          (("thermometer", "thermometers", "temperature", "temps"),
           ("take", "takes", "taking", "read", "reading", "use", "using", "best way",
            "under the arm", "under my arm", "underarm", "armpit", "armpits", "ear", "mouth",
            "oral", "forehead", "accurate", "accurately")),
          _take_a_temperature,
          avoid=("meat", "chicken", "pork", "beef", "lamb", "turkey", "joint", "steak", "roast",
                 "cooked", "cooking", "doneness", "oven", "fan oven", "air fryer", "bake",
                 "baking", "bread", "cake", "sugar", "jam", "oil", "frying", "boiling water",
                 "without a thermometer", "no thermometer", "hay fever", "hayfever",
                 "room temperature", "room temp", "butter", "boiler", "flow temperature",
                 "radiator", "fridge", "freezer", "washing machine", "tumble dryer", "bath",
                 "bathing", "heating", "greenhouse", "wine", "beer", "water", "washing up",
                 "frying pan", "cooker", "hob", "kettle", "saucepan", "milk", "yogurt",
                 "dough", "yeast", "sourdough", "stock", "soup", "sauce", "sugar", "jam",
                 "homebrew", "aquarium", "fish tank", "pond", "compost", "kiln", "sauna",
                 "sterilis", "steriliz", "disinfect", "clean", "washing", "wash the",
                 "fever", "feverish", "chickenpox", "rash"),
          bias=3),
    entry("chickenpox", (("chickenpox", "chicken pox", "spots", "blisters", "scabs"),
                         ("chickenpox", "chicken pox", "how long", "contagious", "infectious",
                          "school", "nursery", "childminder", "child", "children", "kid", "kids",
                          "baby", "toddler", "son", "daughter", "little one", "last", "calamine",
                          "cream", "bath", "ibuprofen", "paracetamol", "back to school",
                          "off school", "catch")),
          _chickenpox_reply,
          avoid=("sun", "sunburn", "sunbed", "freckle", "freckles", "mole", "moles", "acne",
                 "face wash", "makeup", "wall", "paint", "grease", "brass", "stain", "stains",
                 "remove", "get out", "spot cream", "spot treatment", "best", "buy", "which",
                 "product", "products")),
]

NUMB_HANDS = (
    "Hands and fingers that go numb, often in bed or after holding a phone, or that cannot be "
    "felt at all, are usually a nerve being pressed, most often the median nerve at the wrist "
    "(carpal tunnel), which is why the thumb and first two "
    "fingers tingle and "
    "shaking the hand brings it back. Sleep with the wrist straight - a soft splint from a "
    "pharmacy keeps it that way - and take breaks from gripping and typing. See a GP if it "
    "starts happening in the day, the hand weakens or wastes, or it is numb all the time.")
NUMB_ASK = ("numb", "numbness", "pins", "needles", "tingling", "dead", "asleep", "wake",
            "wakes", "waking",
            "feel", "feeling", "cannot", "no feeling", "lost feeling")
NUMB_AVOID = ("leg", "legs", "feet", "foot", "toes", "back", "saddle", "pee", "urine")
HAND_PARTS = ("hand", "hands", "fingers", "finger", "thumb", "wrist", "wrists")
ENTRIES.append(entry("numb-hands-night",
    (("numb", "numbness", "pins and needles", "tingling"),
     HAND_PARTS + ("night", "nights", "in bed", "asleep", "wake me", "wakes me", "waking up",
                   "morning", "driving", "phone", "cycling")),
    NUMB_HANDS,
    ask=NUMB_ASK,
    avoid=NUMB_AVOID))
ENTRIES.append(entry("dead-hand",
    (("dead", "gone to sleep", "asleep",
      "cant feel", "can't feel", "cannot feel", "no feeling", "lost feeling",
      "lost the feeling", "feel nothing"),
     HAND_PARTS),
    NUMB_HANDS,
    ask=NUMB_ASK,
    avoid=NUMB_AVOID))

FOOT_PARTS = ("foot", "sole", "heel", "instep", "ankle")
NUMB_FOOT = (
    "A foot that has gone numb is usually a nerve being pressed - a tight shoe, a leg crossed "
    "over it, kneeling or sitting on it - and the feeling comes back over a few minutes as the "
    "pressure comes off. Shake it out, walk on it and change position rather than rubbing it. "
    "If it keeps happening, or both feet are numb, it is worth a GP visit for the usual causes: "
    "diabetes, a B12 or thyroid problem, a trapped nerve from the back, and narrow shoes. Both "
    "feet numb with back pain, or no feeling between the legs with trouble weeing, is the "
    "same-day one: ring 111, or 999 if the back has given way. A sudden cold, white or blue "
    "foot, or a foot that drags, is 999.")
NUMB_SHOE = ("shoe", "shoes", "boot", "boots", "sock", "socks", "laces", "tight", "sitting",
             "crossed", "kneeling", "sleep", "asleep", "cold", "white", "blue", "swollen",
             "broken", "sprained", "walking", "run", "running", "cycling", "bike", "driving",
             "work", "standing", "long")
ENTRIES.append(entry(
    "numb-foot",
    (FOOT_PARTS, ("numb", "numbness", "pins and needles", "tingling", "no feeling",
                  "cant feel", "can't feel", "gone numb", "went numb", "dead", "asleep")),
    NUMB_FOOT,
    ask=("numb", "numbness", "pins", "needles", "tingling", "no feeling", "gone numb",
         "went numb", "dead", "asleep", "feel"),
    avoid=("backache", "back ache", "back pain", "my back hurts", "my back is sore", "sore back",
           "aching back", "bad back", "my back went", "my back has gone", "my back is killing",
           "back is killing", "my back is bad", "back spasm", "lower back", "spine", "spinal",
           "slipped disc", "sciatica", "between my legs",
           "bladder", "wee", "weeing", "peed", "pee", "peeing", "urine", "urinate",
           "catheter", "incontinent", "bowels", "no urine", "wet myself", "wetting myself"),
    bias=1))
TIGHT_CHEST = (
    "A tight chest has three common causes and they feel much alike. Asthma: a wheeze, a cough "
    "at night or with cold air or exercise, which eases with a blue reliever inhaler. Anxiety: "
    "a fast heart, tingling hands, and it comes in waves of ten or twenty minutes, often when "
    "you are wound up. A chest infection: a fever, a wet cough and feeling rough, which needs "
    "seeing if you are breathless or it is going on. Sudden tightness with pain spreading to "
    "the jaw, neck or arm, sweating, or breathlessness while sitting still is 999. If it keeps "
    "coming back, see a GP and say when it happens - they may give you a peak flow meter or an "
    "inhaler to try.")
ENTRIES.append(entry(
    "tight-chest",
    (("chest", "in my chest", "my chest"),
     ("tight", "tightness", "tightening", "tightens", "constricted", "band", "pressure",
      "heavy", "weight")),
    TIGHT_CHEST,
    avoid=("heartburn", "acid", "reflux", "indigestion", "cough", "cold", "flu", "covid",
           "drawers", "fridge", "freezer", "box", "packing", "suitcase", "lift", "carry",
           "exercise", "running", "run", "gym", "when i run", "when i exercise",
           "dog", "cat", "baby", "child", "toddler", "muscle", "muscles", "gym"),
    bias=1))

ENTRIES.append(entry(
    "aching-joints",
    (("joints", "joint", "knuckles", "knuckle"),
     HURT),
    "Most aching joints are ordinary wear and tear - osteoarthritis - and keeping them moving is "
    "what helps most: walk, swim or cycle, strengthen the muscles around the joint, and lose a bit "
    "of weight if you can, which takes the load off knees and hips. Paracetamol or an ibuprofen "
    "gel eases a flare. A joint that is hot, red and swollen, or sore with a fever, needs seeing "
    "the same day; see a GP if it aches most days or your hands are stiff for more than half an "
    "hour in the morning.",
    guard=_the_part_is_a_persons,
    avoid=tuple(w for w in AVOID if w not in STANDING) + (
                   "dry", "dryness", "cracked", "cracking", "flaky", "chapped", "skin",
                   "fever", "feverish", "temperature", "shivery", "shivering", "chills",
                   "flu", "influenza", "virus"),
    bias=2,
))

ENTRIES.append(entry(
    "frozen-shoulder",
    (("shoulder", "shoulders"),
     ("frozen", "frozen shoulder", "locked", "cant lift", "can't lift", "cannot lift",
      "cant raise", "can't raise", "wont move", "won't move", "cant move it", "can't move it")),
    "A shoulder that stiffens up over weeks until you cannot lift the arm, especially turning it "
    "outwards, is usually a frozen shoulder: the capsule around the joint tightens, often for no "
    "clear reason. It eases in stages, and most people take 1 to 2 years to get most of the "
    "movement back. Keep using the arm as far as it goes, warm it before gentle stretches, and "
    "take paracetamol or ibuprofen if you can; a GP can refer you for physiotherapy and give a "
    "steroid injection early, which helps most in the painful first stage.",
    avoid=("lamb", "pork", "beef", "chicken", "meat", "roast", "cook", "cooking", "recipe",
           "oven", "freezer", "defrost", "joint of",
           "fell", "fall", "after a fall", "injury", "injured", "dislocated", "broken",
           "replacement", "operation", "surgery", "after the operation"),
))

_ARTHRITIS_TAIL = (
    "it aches after years of use, is stiff first thing and eases as you move, and the treatment "
    "is using the joint rather than sparing it. Walking, swimming or cycling and a little "
    "strength work a few times a week keep the muscles that support the joint strong, and "
    "paracetamol with an ibuprofen gel handles a flare better than most tablets sold for "
    "arthritis. Glucosamine and cod liver oil have not held up in trials, no diet cures it, and "
    "cold, damp weather can make it ache more without damaging the joint; losing weight if you "
    "are carrying extra takes real load off knees and hips. Stiffness that lasts more than an "
    "hour in the morning, or a joint that is hot, red and swollen, is the inflammatory kind and "
    "wants a GP soon - ask about physiotherapy, and about a steroid injection for one joint that "
    "keeps flaring.")

_ARTHRITIS_CURE = ("cure", "cured", "cures", "curable", "reverse", "reversed", "reversible",
                   "rid", "go away", "gone away", "permanent", "permanently")


def _arthritis_reply(memory, reading):
    words = set(reading.get("words") or ())
    if words & set(_ARTHRITIS_CURE):
        return ("Arthritis cannot be cured, but the ordinary wear-and-tear kind is managed "
                "well: " + _ARTHRITIS_TAIL)
    return "Ordinary arthritis - osteoarthritis - is the wear-and-tear kind: " + _ARTHRITIS_TAIL


ENTRIES.append(entry(
    "arthritis",
    (("arthritis", "osteoarthritis", "arthritic", "arthritus", "arthrosis", "arthrits"),
     ASK_ABOUT + ("pain", "pains", "painful", "hurts", "hurt", "ache", "aching", "aches",
                  "stiff", "stiffness", "hands", "hand", "fingers", "knees", "knee", "hips",
                  "hip", "thumb", "joint", "joints", "weather", "cold", "damp", "diet",
                  "food", "foods", "exercise", "exercising", "walking", "swimming",
                  "tablets", "glucosamine", "injection", "manage", "know", "cause")),
    _arthritis_reply,
    avoid=("cat", "cats", "kitten", "dog", "dogs", "puppy", "pet", "pets", "horse",
           "rabbit", "vet", "replacement", "replaced", "hip replacement", "knee replacement",
           "operation", "surgery"),
    bias=2,
))

ENTRIES.append(entry(
    "stiff-hands-morning",
    (("fingers", "finger", "hands", "hand", "knuckles", "knuckle", "thumbs", "thumb"),
     ("stiff", "stiffness", "stiffens", "stiffened", "stiffening", "gone stiff",
      "cant bend", "can't bend", "wont bend", "won't bend", "cant make a fist",
      "can't make a fist", "first thing", "in the morning", "feel tight")),
    "Stiff fingers in the morning are usually the small joints of the hands starting to wear - "
    "osteoarthritis - and that kind loosens within half an hour of moving them: run warm water "
    "over the hands first thing, do gentle finger and thumb circles, and keep using them, because "
    "rest is what makes a stiff hand stiffer. Paracetamol helps a sore spell and a pharmacist can "
    "suggest an ibuprofen gel. See a GP if the stiffness lasts more than an hour, the knuckles "
    "are swollen, or both hands are the same, because that pattern is the inflammatory kind and "
    "wants treating early.",
    avoid=("typing", "type", "keyboard", "mouse", "phone", "grip", "gripping", "wrist",
           "wrists", "tendon", "sprained", "sprain", "fell", "fall", "injury", "injured",
           "hot", "red", "swollen"),
    bias=2,
))

ENTRIES.append(entry(
    "rheumatoid-arthritis",
    (("rheumatoid", "rheumatism", "rheumatoid arthritis"),
     ("arthritis", "joints", "joint", "hands", "hand", "fingers", "flares", "flare", "pain",
      "hurts", "hurt", "medication", "methotrexate", "drugs", "treatment", "exercise",
      "tired", "stiff")),
    "Rheumatoid arthritis is the immune system attacking the lining of the joints, and it is "
    "treated early and hard because most of the damage happens in the first year or two: a "
    "rheumatology team starts disease-modifying drugs such as methotrexate, with a short course "
    "of steroids to settle a flare, and those are what keep the joints working. Keep moving "
    "between flares, take the tablets even when you feel well, and tell the team the same day "
    "if a joint is hot and swollen or you feel generally unwell, since that can be an "
    "infection rather than a flare and the two want opposite treatment.",
    bias=1,
))

ANSWERS = ("health",)

BROKEN_PARTS = ("ankle", "ankles", "wrist", "wrists", "arm", "arms", "foot", "feet", "toe",
                "toes", "finger", "fingers", "thumb", "hand", "hands", "leg", "legs", "knee",
                "knees", "elbow", "shoulder", "hip", "shin", "heel", "collarbone",
                "collarbones")
BROKEN_WORDS = ("broken", "broke", "fractured", "fracture", "cracked", "crack", "is it broken",
                "or broken", "or sprained", "or just sprained", "do i need an x-ray",
                "do i need an xray", "need an x-ray", "need an xray", "how do i know",
                "how can i tell", "how to tell", "is it a break", "a break or a sprain",
                "broken or sprained",
                "after a fall", "fell on it", "went over on it", "landed on it", "since i fell",
                "twisted it")

ON_YOUR_FEET = ("ankle", "ankles", "foot", "feet", "toe", "toes", "leg", "legs", "knee", "knees",
                "shin", "heel", "hip", "hips")
IN_YOUR_HANDS = ("wrist", "wrists", "hand", "hands", "finger", "fingers", "thumb", "elbow",
                 "elbows")
AT_YOUR_SHOULDER = ("shoulder", "shoulders", "arm", "arms", "collarbone")

FOUR_STEPS_REPLY = (
    "How much it hurts does not tell you - a bad sprain can hurt more than a small break. Stand "
    "on it and take four steps: if you cannot, or it is crooked, numb or swelling fast, go to a "
    "minor injuries unit or A&E today for an X-ray. If you can walk on it, treat it as a sprain - "
    "ice for 20 minutes, a support wrap, keep it up - and have it checked if it is no better in "
    "two days.")

IN_YOUR_HANDS_REPLY = (
    "How much it hurts does not tell you - a bad sprain can hurt more than a small break. Try to "
    "use it: make a fist, turn a door handle, lift something light. If you cannot, or the bone "
    "looks crooked, the fingers are numb or it is swelling fast, go to a minor injuries unit or "
    "A&E today for an X-ray. If you can use it with care, treat it as a sprain - ice for 20 "
    "minutes, a support wrap, keep it raised - and have it checked if it is no better in two days.")

AT_YOUR_SHOULDER_REPLY = (
    "How much it hurts does not tell you - a bad sprain can hurt more than a small break. Try to "
    "raise the arm sideways to shoulder height and reach across your chest: if you cannot move "
    "it, or the "
    "joint looks out of shape, the arm or hand is numb or it is swelling fast, go to a minor "
    "injuries unit or A&E today for an X-ray. If you can move it with care, treat it as a sprain "
    "- ice for 20 minutes, a support wrap, keep it up - and have it checked if it is no better in "
    "two days.")


def _broken_or_sprained(memory, understood):
    if _a_thing_owns_the_part(understood or {}):
        return None
    words = _words(understood)
    if words & set(IN_YOUR_HANDS):
        return IN_YOUR_HANDS_REPLY
    if words & set(AT_YOUR_SHOULDER):
        return AT_YOUR_SHOULDER_REPLY
    if words & set(ON_YOUR_FEET):
        return FOUR_STEPS_REPLY
    return FOUR_STEPS_REPLY


ENTRIES.append(entry(
    "broken-or-sprained",
    (BROKEN_PARTS, BROKEN_WORDS),
    _broken_or_sprained,
    avoid=("my son", "my daughter", "my child", "my kid", "my baby", "my toddler", "my husband",
           "my wife", "my partner", "my mum", "my mom", "my mother", "my dad", "my father",
           "my friend", "my dog", "my cat", "his", "her", "when i was", "years ago", "last year",
           "healed", "healing", "cast", "crutches", "boot", "physio", "physiotherapy",
           "recovery", "recover", "how long does it take", "sticking out", "through the skin",
           "when can i", "how soon", "again after", "play again", "back to work", "back to sport",
           "back to football", "back to the gym", "back to running",
           "i broke", "ive broken", "i've broken", "i fractured", "i cracked", "think i broke",
           "thinks he broke", "thinks she broke", "think ive broken", "think i've broken",
           "bone is showing", "999", "ambulance", "unconscious", "head injury",
           "egg", "eggs",
           "hit my head", "hit his head", "head injury", "knocked out", "unconscious",
           "blacked out", "cannot get up", "cant get up", "could not get up", "neck",
           "glasses", "spectacles", "specs", "sunglasses", "frame", "frames", "lenses",
           "watch", "watch strap", "watchstrap", "bracelet")))

ENTRIES += [
    entry("sweating", (("sweat", "sweats", "sweaty", "sweating", "perspire", "perspiring",
                        "perspiration", "clammy", "b.o.", "body odour", "body odor"),
                       ("stop", "less", "too much", "so much", "a lot", "excessive", "reduce",
                        "under my arms", "armpits", "always")),
          "Use an antiperspirant rather than a deodorant, put it on last thing at night on dry "
          "skin where it works, and choose one with aluminium in it. Loose cotton and a spare "
          "shirt help, spicy food and alcohol make it worse, and if you sweat buckets from one "
          "place or at night, that is worth a GP visit.",
          avoid=("fever", "hot flush", "hot flushes", "menopause", "night sweat", "night sweats",
                 "panic", "anxious", "anxiety", "withdrawal", "opiate", "gym", "workout",
                 "running", "hyperhidrosis", "my son", "my daughter", "my baby", "my child",
                 "my husband", "my wife", "my partner", "my mum", "my dad")),
    entry("whiten-teeth", (("whiten", "whiter", "whitening", "bleach", "stains", "stained",
                            "yellow", "yellowing", "brighter"),
                           ("teeth", "tooth", "smile", "my teeth")),
          "A dentist or a hygienist scale and polish first, because most yellowing is staining on "
          "the outside, and then whitening works: either a professional kit made for your teeth or "
          "a legal-strength high-street one, and expect it to take a couple of weeks. Charcoal and "
          "bicarbonate toothpastes scrub the enamel and do not whiten it.",
          avoid=("brush", "brushing", "toothbrush", "toothpaste", "my toddler", "my child",
                 "my kid", "my son", "my daughter", "baby", "teething baby", "teething ring",
                 "cutting teeth", "dentist appointment", "register", "toothache", "hurts",
                 "sensitive", "filling", "brace", "braces", "whitening strips are safe")),
    entry("nails-grow", (("nails", "nail", "fingernails", "fingernail", "toenails", "toenail"),
                         ("grow", "growing", "longer", "long", "stronger", "strong", "break",
                          "breaking", "brittle", "peel", "peeling", "split", "splitting",
                          "flaky", "weak",
                          "strengthen", "strengthening", "healthy", "healthier", "harder",
                          "faster", "thicker")),
          "Nails grow about 3mm a month, so a full nail takes six months and nothing speeds it up "
          "much: keep them filed rather than bitten, use a hand cream or cuticle oil daily, wear "
          "gloves for washing up, and take in enough protein and iron. Ridges and white spots are "
          "normal; a nail that changes colour or lifts is worth showing a pharmacist.",
          avoid=("biting", "bite", "cuticle", "gel", "acrylic", "acrylics", "polish", "paint",
                 "manicure", "pedicure", "hammer", "hangnail", "fungal", "infection",
                 "black", "bruised", "bruise", "purple", "dark", "slammed", "slam", "dropped",
                 "knocked", "knock", "stubbed", "smashed", "football", "door", "trapped",
                 "my dog", "my cat", "my baby", "my toddler", "my child"),
          guard=_the_nail_is_a_persons),
]

ENTRIES += [
    entry("physio-or-stretch",
          (("physio", "physiotherapy", "physiotherapist", "chiropractor", "osteopath"),
           ("see", "should i", "or just", "worth", "need", "go", "stretch", "gp", "refer")),
          "See a physio if the pain has lasted more than a fortnight, keeps coming back, or comes "
          "with numbness, weakness or pins and needles - and you can refer yourself on the NHS "
          "without seeing a GP first. If it is a recent strain that is already easing, gentle daily "
          "stretching plus some strength work (sit-to-stands, bridges, a short walk) is what a "
          "physio would give you anyway.",
          avoid=("knee", "shoulder", "ankle", "calf", "hamstring", "achilles", "cost", "how much",
                 "price", "private")),
]

ENTRIES.append(entry(
    "health-complaint",
    (("dentist", "dentists", "dental", "gp", "doctor", "doctors", "doctor's", "hospital",
      "hospitals", "nhs", "surgery", "clinic", "nurse", "midwife", "consultant", "surgeon",
      "care i got", "care i received", "care i had", "the care i"),
     ("complain", "complaining", "complaint", "complaints", "made a complaint",
      "make a complaint", "raise a complaint", "raised a complaint", "mistake", "mistakes",
      "misdiagnosed", "misdiagnosis", "negligence", "negligent", "botched", "wrong tooth",
      "wrong tooth out", "wrong medication", "wrong medicine", "hurt me", "caused harm",
      "bad treatment", "poor treatment", "did a bad job")),
    "Ask the practice or hospital for its complaints procedure and put it in writing: what "
    "happened, when, who you saw and what you want. Ask for a written reply and keep copies. "
    "Still unhappy? Ask for a deadlock letter and take it free to the NHS ombudsman - PALS at "
    "a hospital will help you word it, and private dental work has the free Dental Complaints "
    "Service. If someone was harmed, get the records and advice from AvMA before signing "
    "anything.",
    avoid=("bill", "billing", "invoice", "parking", "car park", "charge", "charges", "cost",
           "price", "how much", "register", "registering", "sign up", "appointment",
           "appointments", "book", "booking", "waiting list", "waiting time", "food", "meal",
           "cleanliness", "cleaning"),
    bias=2))

MOLE_CHANGE = ("change", "changed", "changes", "changing", "different", "bigger", "growing",
               "grown", "grew", "larger", "size", "shape", "edge", "edges", "border", "colour",
               "color", "colours", "colors", "darker", "dark", "black", "bleeding", "bled",
               "bleeds", "blood", "crusty", "crusting", "scab", "scabby", "itchy", "itching",
               "itches", "sore", "tender", "raised", "lumpy", "new", "suddenly", "worried",
               "worry", "worrying", "checked", "check", "checking", "dangerous", "cancer",
               "melanoma", "malignant", "normal", "looks", "look", "found", "keep an eye",
               "keep my eye", "monitor", "watch", "hair", "hairy",
               "catching on", "catches on", "catch on", "caught on", "rubs", "rubbing",
               "rubbed", "friction", "irritated", "appeared", "appears", "appearing")

MOLE_HAPPENING = ("change", "changed", "changes", "changing", "different", "bigger", "growing",
                  "grown", "grew", "larger", "size", "shape", "edge", "edges", "border",
                  "colour", "color", "colours", "colors", "darker", "dark", "black",
                  "bleeding", "bled", "bleeds", "blood", "crusty", "crusting", "scab",
                  "scabby", "itchy", "itching", "itches", "sore", "tender", "raised",
                  "lumpy", "dangerous", "cancer", "melanoma", "malignant",
                  "worried", "worry", "worrying", "anxious", "bad", "serious", "abnormal",
                  "cancerous",
                  "catching", "catches", "caught", "rubs", "rubbing", "rubbed", "friction",
                  "irritated", "appeared", "appears", "appearing")
_MOLE_CLEAR = frozenset("""
bleeding bled bleeds blood crusty crusting scab scabby itchy itching itches changed changing
change changes different bigger larger darker black sore tender lumpy
catching catches caught rubbing rubbing rubbed friction appeared appears appearing
""".split())
_MOLE_CHANGED_TEXT = (
    "Get it checked by a GP within two weeks. A mole that changes shape, edge, colour or size, "
    "or bleeds, itches or crusts on its own, wants a look rather than a wait, though almost all "
    "of them turn out to be nothing. The signs worth saying out "
    "loud are the ABCDE ones: not symmetrical, a ragged or blurry border, more than one colour, "
    "wider than about 6mm, or changing in any way. Photograph it beside a coin for scale and "
    "ring the surgery rather than waiting to see whether it settles.")
_MOLE_ORDINARY_TEXT = (
    "Almost all moles are harmless, so what matters is knowing what a change looks like rather "
    "than checking it every day: the ABCDE test is not symmetrical, a ragged or blurry border, "
    "more than one colour, wider than about 6mm, or anything that is changing. Photograph it "
    "beside a coin for scale and compare it every few months; a mole that changes, bleeds, itches "
    "or crusts on its own wants a GP within two weeks, and a hair growing out of one usually "
    "means it is an ordinary mole that has been there a long time.")
_CHECK_HOW_TO = re.compile(r"\bhow\s+(?:do|can|should|would)\s+(?:i|you|we)\s+(?:check|inspect)|"
                           r"how\s+to\s+check|what\s+(?:do\s+i\s+)?look\s+for", re.I)
_NEW_SUBJECT = ("new", "another", "child", "children", "kid", "kids", "son", "daughter",
                "baby", "wife", "husband", "partner", "friend", "mother", "father", "mum",
                "dad", "sister", "brother", "gran", "nan", "other")


def _a_bare_followup(said):
    words = re.findall(r"[a-z']+", str(said).lower())
    if not words or len(words) > 6:
        return False
    if any(word in words for word in ("mole", "moles", "birthmark", "birthmarks", "spot", "spots")):
        return False
    return not any(word in words for word in _NEW_SUBJECT)


MOLE_REMOVE = ("get rid", "rid of", "remove", "removing", "removal", "removed", "laser",
               "freeze", "freezing", "cut off", "cut it off", "tie it off", "shave off",
               "cut a mole", "cut my mole", "cut this mole", "get it cut")
_MOLE_REMOVE_TEXT = (
    "Most moles need no treatment at all, and one that bothers you - catching on clothes, or a GP "
    "wanting a closer look - is taken off on the NHS: a short excision under local anaesthetic, "
    "with the mole sent for a check. Don't cut, tie off or use a wart or skin-tag kit on it, and "
    "don't book a beauty clinic for something a GP should see first.")


def _mole_reply(memory, understood):
    words = _words(understood)
    said_words = str(understood.get("text") or understood.get("clean") or "") if isinstance(
        understood, dict) else ""
    if (any(phrase in said_words.lower() for phrase in MOLE_REMOVE)
            and not words & set(MOLE_HAPPENING)):
        return _MOLE_REMOVE_TEXT
    said = str(understood.get("text") or understood.get("clean") or "") if isinstance(
        understood, dict) else ""
    if words & {"hair", "hairy"} and not words & _MOLE_CLEAR:
        return _MOLE_ORDINARY_TEXT
    if _CHECK_HOW_TO.search(said):
        return _MOLE_ORDINARY_TEXT
    if words & set(MOLE_HAPPENING) or words & {"check", "checked", "checking"}:
        return _MOLE_CHANGED_TEXT
    if _a_bare_followup(said) and any(
            "get it checked by a gp" in str(turn.get("bot") or "").lower()
            for turn in (memory or {}).get("turns") or [] if isinstance(turn, dict)):
        return _MOLE_CHANGED_TEXT
    return _MOLE_ORDINARY_TEXT


ENTRIES.append(entry(
    "changing-mole",
    (("mole", "moles", "birthmark", "birthmarks", "beauty spot", "beauty spots", "skin spot"),
     MOLE_CHANGE + MOLE_REMOVE),
    _mole_reply,
    avoid=("garden", "gardens", "lawn", "lawns", "grass", "golf", "green", "molehill",
           "molehills", "mole hill", "hill", "hills", "tunnel", "tunnels", "trap", "traps",
           "trapping", "pest", "pests", "animal",
           "animals", "wildlife", "drain", "drains", "field", "fields", "farm", "farmer",
           "vole", "voles", "rodent", "rodents", "sauce", "recipe", "recipes", "cook",
           "cooking", "dish", "dish", "chilli", "chocolate", "poblano", "chicken",
           "acne", "pimple", "pimples", "blackhead", "blackheads", "spot cream",
           "spot treatment", "face wash", "cleanse", "cleanser", "routine", "product",
           "products", "best", "sunscreen", "sun cream", "sunbed", "sun tan", "fake tan",
           "tanned", "tanning", "sunless"),
    bias=1))

PAINKILLER_NAMES = ("paracetamol", "acetaminophen", "panadol", "calpol", "ibuprofen", "nurofen",
                    "brufen", "co codamol", "co-codamol", "painkiller", "painkillers",
                    "anti inflammatory", "nsaid", "nsaids")
_NOT_THE_TABLET = ("heartburn", "indigestion", "reflux", "antacid", "gaviscon", "rennie",
                   "omeprazole", "lansoprazole", "acid reflux")

_KIDNEY_WORDS = ("kidney", "kidneys", "renal", "water tablet", "water tablets", "diuretic",
                 "blood pressure tablet", "blood pressure tablets", "blood pressure medication",
                 "blood pressure pills", "only one kidney")


_NOT_AN_NSAID = ("paracetamol", "acetaminophen", "panadol", "calpol", "co codamol", "co-codamol")


def _the_organ_the_painkiller_upsets(memory, reading):
    line = " ".join(str((reading or {}).get("text") or "").split()).lower()
    holds_paracetamol = any(word in line for word in _NOT_AN_NSAID)
    holds_nsaid = any(word in line for word in ("ibuprofen", "nurofen", "brufen", "naproxen",
                                                "aspirin", "diclofenac", "nsaid", "anti "
                                                "inflammatory", "anti-inflammatory",
                                                "voltarol", "indomethacin"))
    if holds_paracetamol and not holds_nsaid:
        return ("Paracetamol is the painkiller to use here: it is not an anti-inflammatory, so it "
                "does not cut the blood flow the kidneys rely on or irritate the stomach the way "
                "ibuprofen does, and a blood pressure tablet or a water tablet is no reason to "
                "avoid it. Stay within the 4g a day limit (less if a GP has said so, and less if "
                "you have liver trouble or drink heavily), and space the doses out. If it is not "
                "touching the pain, that is worth a word with a pharmacist rather than more "
                "tablets.")
    if any(word in line for word in _KIDNEY_WORDS):
        return ("An anti-inflammatory cuts the blood flow the kidneys rely on, so it is the wrong "
                "choice if yours are already poor, if you are dehydrated, or if you take a water "
                "tablet or a blood pressure tablet - that mix is the one pharmacists watch for. "
                "Paracetamol is the painkiller to use instead, and it is worth asking a "
                "pharmacist or GP before starting ibuprofen at all if you have kidney disease or "
                "only one kidney.")
    return ("Ibuprofen and the other anti-inflammatories (naproxen, aspirin, diclofenac) can "
            "irritate the stomach lining, so take them with or after food rather than on an empty "
            "stomach, at the lowest dose that works and for the shortest time. Don't take them at "
            "all if you have had a stomach ulcer or a bleed, or if you are on a blood thinner - "
            "paracetamol is the one to use instead. Get seen the same day for a pain in the top of "
            "the stomach that is severe, for black tarry poo, or for vomiting blood or anything "
            "that looks like coffee grounds.")


ENTRIES.append(entry("painkiller-stomach",
          (PAINKILLER_NAMES,
           ("stomach", "tummy", "gut", "upset", "upsets", "upsetting", "empty stomach",
            "with food", "before food", "after food", "eat before", "eat something",
            "on food", "bad for my stomach", "bad for your stomach", "sore stomach",
            "irritate", "irritates", "irritating", "lining", "ulcer", "ulcers",
            "bleeding in my stomach", "stomach bleed", "does it upset",
            "kidney", "kidneys", "renal", "bad for my kidneys",
            "water tablet", "water tablets", "diuretic", "blood pressure tablet",
            "blood pressure tablets", "blood pressure medication", "blood pressure pills")),
          _the_organ_the_painkiller_upsets,
          avoid=_NOT_THE_TABLET + ("pregnant", "pregnancy", "breastfeeding", "breastfeed",
                                   "child", "kid", "baby", "toddler", "dog", "cat",
                                   "overdose", "took too many", "whole packet", "allergic",
                                   "reaction", "rash", "asthma")))

ENTRIES.append(entry("painkiller-and-alcohol",
          (PAINKILLER_NAMES,
           ("alcohol", "drink", "drinking", "drunk", "beer", "wine", "vodka", "gin", "pint",
            "pints", "booze", "a few drinks", "nights out", "night out")),
          "Paracetamol and drink is a liver question and ibuprofen and drink is a stomach one, "
          "and a normal dose of either with an occasional drink is fine. Paracetamol's warning "
          "is about drinking heavily or daily for years, because the liver handles both, and the "
          "ceiling stands whatever you have drunk: no more than 4g (eight 500mg tablets) in 24 "
          "hours, with no other paracetamol product on top. Ibuprofen mainly raises the risk of "
          "stomach irritation and bleeding, so eat something with it and keep to the lowest dose "
          "that works. If you drink heavily every day, ask a pharmacist before taking paracetamol "
          "at all.",
          avoid=_NOT_THE_TABLET + ("pregnant", "pregnancy", "breastfeeding", "child", "kid",
                                   "baby", "toddler", "dog", "cat", "overdose", "took too many",
                                   "whole packet", "alcoholic", "addiction", "stop drinking",
                                   "give up alcohol", "cut down")))

ENTRIES.append(entry("painkiller-how-fast",
          (PAINKILLER_NAMES,
           ("how long", "how quickly", "how fast", "how soon", "when does it work",
            "take to work", "kick in", "kicks in", "start working", "starts working",
            "how long to work", "how long until")),
          "Tablets taken by mouth start working in about 30 minutes and are at their best at one "
          "to two hours; a soluble or effervescent one is quicker, and ibuprofen lysine and the "
          "liquid capsules are faster than a plain tablet. Pain that has not shifted at all after "
          "two hours, at a proper dose, is a reason to ask a pharmacist rather than to take more "
          "sooner than the packet allows.",
          avoid=_NOT_THE_TABLET + ("child", "kid", "baby", "toddler", "pregnant", "pregnancy",
                                   "breastfeeding", "dog", "cat", "how long can i take",
                                   "how long should i take", "how many days", "how long does "
                                   "ibuprofen last", "how long does it last")))

ENTRIES.append(entry("painkiller-and-the-blood",
          (PAINKILLER_NAMES,
           ("thin your blood", "thins the blood", "thin the blood", "thinning", "blood thinner",
            "blood thinners", "warfarin", "clot", "clotting", "bleed more", "bleeding",
            "bruise", "bruises", "bruising", "before an operation", "before surgery",
            "before my operation", "dental work", "tooth out")),
          "Ibuprofen and the other anti-inflammatories make the blood a little slower to clot, "
          "which is why they are stopped before an operation or a tooth out - usually a few days "
          "before, on the surgeon's or dentist's word - and why they are not mixed with warfarin "
          "or a blood thinner without advice. Paracetamol has no effect on clotting at all, so "
          "if you bruise easily or bleed for longer than you used to, that is a question for a "
          "pharmacist or GP rather than a reason to keep taking it.",
          ask=("can i", "should i", "is it", "does it", "do i", "is", "does", "before", "with",
               "ok", "safe", "okay"),
          avoid=_NOT_THE_TABLET + ("pregnant", "pregnancy", "breastfeeding", "child", "kid",
                                   "baby", "toddler", "dog", "cat", "overdose", "took too many",
                                   "cut myself", "cut my", "wound", "nosebleed", "heavy period")))

ENTRIES.append(entry("painkiller-and-sleep",
          (PAINKILLER_NAMES,
           ("sleepy", "drowsy", "drowsiness", "make me tired", "makes me tired", "knock me out",
            "knocks me out", "can i drive", "drive after", "drowsy driving", "sleep",
            "keep me awake", "awake")),
          "Paracetamol and ibuprofen are not sedatives and neither is meant to make you sleepy - "
          "drowsiness is an uncommon side effect of ibuprofen, so if one does leave you dozy it is "
          "worth mentioning to a pharmacist. What does make people drowsy is the codeine in "
          "co-codamol, and the sleepy feeling is one of the reasons not to drive on it until you "
          "know how it treats you. Pain itself is often what stops people sleeping, so a dose at "
          "bedtime is fine.",
          avoid=_NOT_THE_TABLET + ("child", "kid", "baby", "toddler", "pregnant", "pregnancy",
                                   "breastfeeding", "dog", "cat", "cant sleep", "can't sleep",
                                   "insomnia", "sleep aid", "sleeping tablet", "melatonin",
                                   "nightmare")))

_WAX_FIRST_REPLY = (
    "Waxing wants hair about 5mm long, a patch test a day ahead and one firm pull against the "
    "growth with the skin held tight; take an antihistamine an hour before if you come up "
    "blotchy. Shaving is quicker: end of a warm shower, fresh blade, conditioner instead of "
    "foam, and with the hair rather than against it, which is what keeps the red bumps away. An "
    "ingrown hair wants a warm compress and an exfoliating glove every other day.")

_SHAVE_FIRST_REPLY = (
    "Shave at the end of a warm shower with a fresh blade and conditioner, rinsing the blade "
    "often, and on legs and bikini line go with the hair, not against it, which is what keeps "
    "the red bumps away. Waxing wants hair 5mm long, a patch test a day ahead and a firm pull "
    "against the growth, plus an antihistamine an hour before if you come up blotchy. An "
    "ingrown hair wants a warm compress and an exfoliating glove every other day.")

_WAX_WORDS = {"wax", "waxes", "waxing", "waxed", "wax strip", "wax strips", "strip", "strips",
              "sugaring", "hot wax", "cold wax", "bikini wax", "leg wax", "underarm wax",
              "sugar"}


def _hair_removal(memory, understood):
    if _words(understood) & _WAX_WORDS:
        return _WAX_FIRST_REPLY
    return _SHAVE_FIRST_REPLY


_BEARD_TRIM_WORDS = {"trim", "trims", "trimming", "trimmer", "trimmers", "shape", "shaping",
                     "line", "line up", "lining", "neckline", "guard", "guards", "shorten",
                     "tidy", "tidying", "beard", "beards", "moustache", "mustache", "goatee",
                     "stubble"}
_BLADE_WORDS = {"blade", "blades", "razor blade", "razor blades", "change", "changing",
                "rust", "rusty", "rusting", "going rusty", "sharpen", "sharp",
                "replace", "replacing", "how often", "blunt", "dull", "dragging", "drags",
                "last", "lasts", "how long", "wear out", "worn out", "how many shaves",
                "pulling", "pulls", "pull", "new razor", "cartridge", "cartridges"}
_SHAVE_BURN_WORDS = {"burn", "burns", "burning", "razor burn", "sore", "red", "redness",
                     "irritation", "irritated", "rash", "bumps", "spot", "spots", "sting",
                     "stings", "stinging", "stop razor burn", "prevent razor burn", "stop razor rash",
                     "prevent shaving rash", "avoid razor bumps", "stop the burn",
                     "stop it burning", "prevent the burn", "avoid the burn",
                     "stop the rash", "prevent the rash", "stop the redness",
                     "stop the irritation", "prevent irritation", "avoid irritation",
                     "stop the stinging", "stop the stinging", "avoid shaving rash"}

_BEARD_TRIM_REPLY = (
    "Trim it dry, on a guard a couple of steps longer than the length you want, and go with the "
    "hair first before tidying the edges against it. Take the neckline just above the Adam's "
    "apple and the cheeks along the jaw, then finish with the guard off and the blade flat so "
    "the lines are sharp.")
_STRAIGHT_SHAVE_REPLY = (
    "Warm the hair first - a shower or a flannel held on for two minutes - then use a sharp blade "
    "and proper cream, and take short strokes with the grain without pressing. Most nicks come "
    "from a blunt blade or going over the same patch again, so rinse and stop there.")
_RAZOR_BLADE_REPLY = (
    "Rinse the blade in hot water and stand it up to dry rather than leaving it in the shower, "
    "and change it after five to seven shaves, or the moment it drags and pulls instead of "
    "gliding: a blunt blade scrapes the skin, which is what most razor burn really is.")
_RAZOR_BURN_REPLY = (
    "Rinse with cool water, pat it dry and skip anything with alcohol in it; then a fresh blade, "
    "shaving with the grain and short strokes are what stop it coming back. If it stings for "
    "days or comes up in spots, shave every other day until it settles, and take anything "
    "blistered or spreading to a pharmacist.")


def _face_shaving(memory, understood):
    words = _words(understood)
    if words & _BLADE_WORDS:
        return _RAZOR_BLADE_REPLY
    if words & _SHAVE_BURN_WORDS:
        return _RAZOR_BURN_REPLY
    if words & _BEARD_TRIM_WORDS:
        return _BEARD_TRIM_REPLY
    return _STRAIGHT_SHAVE_REPLY


ENTRIES.append(entry("face-shaving",
          (("shave", "shaves", "shaving", "shaved", "razor", "razors", "beard", "beards",
            "moustache", "mustache", "goatee", "stubble", "beard trimmer", "trimmer",
            "razor blade", "razor blades", "wet shave", "close shave"),
           ("face", "neck", "chin", "jaw", "jawline", "cheek", "cheeks", "upper lip",
            "moustache", "mustache", "beard", "beards", "blade", "blades", "razor blade",
            "burn", "burns", "razor burn", "rash", "irritation", "cut", "cuts", "nick",
            "nicks", "trim", "trimming", "shave", "shaving", "stubble", "how often",
            "change", "replace", "closest", "smooth", "pulling", "pulls", "pull", "drag",
            "last", "lasts", "how long", "long does", "wear out", "worn out",
            "blunt", "dull", "rust", "rusty", "rusting", "cartridge", "cartridges",
            "drags", "dragging", "tugging", "look after", "care", "care for", "keep", "head",
            "scalp", "how do i", "how to", "best way", "what should i")),
          _face_shaving,
          avoid=("leg", "legs", "bikini", "underarm", "underarms", "armpit", "armpits",
                 "eyebrow", "eyebrows", "pubic", "ingrown", "ingrowing", "ingrown hair",
                 "razor bumps", "shaving rash", "shaving bumps", "wax", "waxes", "waxing",
                 "sunburn", "sun burn",
                 "scald", "scalded", "hot water", "iron", "oven", "hair removal",
                 "legs and bikini",
                 "parmesan", "cheese", "chocolate", "fennel", "truffle", "horseradish",
                 "clam", "clams", "razor clam", "razor clams", "razor shell", "razor shells",
                 "clean", "cleaning", "wash", "washing", "itch", "itchy", "itching",
                 "dandruff", "grow", "growing", "faster", "thicker", "patchy", "beard oil",
                 "beard balm",
                 "hedge", "hedges", "hedge trimmer", "hedge cutters", "garden", "gardening",
                 "lawn", "lawns", "lawnmower", "mower", "mowers", "strimmer", "strimmers",
                 "leaf blower", "chainsaw", "secateurs", "shears", "shed", "garage",
                 "topiary", "shrub", "shrubs", "bush", "bushes")))

ENTRIES.append(entry("hair-removal",
          (("wax", "waxes", "waxing", "waxed", "shave", "shaves", "shaving", "shaved",
            "hair removal", "hair remover", "epilator", "epilate", "epilating", "razor",
            "razors", "depilatory", "hair removal cream", "sugaring",
            "sugar my legs", "sugar legs", "sugar my bikini", "sugar my underarms",
            "sugar my armpits", "sugar wax", "sugar paste", "sugaring wax",
            "ingrown", "ingrowing", "ingrown hair", "ingrown hairs", "ingrowing hair",
            "razor bumps", "shaving rash", "shaving bumps"),
           ("leg", "legs", "bikini", "bikini line", "underarm", "underarms", "armpit",
            "armpits", "eyebrow", "eyebrows", "beard", "face", "upper lip", "chin", "pubic",
            "hair", "hairs", "stubble", "ingrown", "ingrowing", "bumps", "rash", "irritation",
            "redness", "smooth", "how do i", "best way", "how to", "sore", "hurts",
            "painful", "stings", "itchy",
            "sugaring", "sugar wax")),
          _hair_removal,
          avoid=("ear", "ears", "earwax", "ear wax", "blocked ear", "bunged up ear",
                 "table", "tables", "floor", "floors", "furniture", "car", "cars", "skirting",
                 "candle", "candles", "surfboard", "skis", "ski", "snowboard", "boots", "wood",
                 "wooden", "paintwork", "leather", "thread", "eyebrow pencil", "tweezers",
                 "tweeze", "threading", "bleach",
                 "tablecloth", "tablecloths", "cloth", "candle wax", "candle holder",
                 "wax off", "wax out of", "off the table", "off my table", "wax stain",
                 "beard", "beards", "shave my head", "shaving my head", "head shave",
                 "shave my face", "shaving my face",
                 "clam", "clams", "razor clam", "razor clams", "razor shell", "razor shells",
                 "oyster", "oysters", "mussel", "mussels", "shellfish",
                 "toenail", "toenails", "toe nail", "toe nails", "ingrown toenail",
                 "ingrowing toenail", "fingernail", "fingernails", "podiatrist", "chiropodist",
                 "blood sugar", "sugar crash", "crave", "craves", "craving", "cravings",
                 "stop wanting", "wanting sugar", "sugar addiction", "addicted to sugar",
                 "sugar out of my diet", "eating sugar", "eat sugar", "stop eating",
                 "warmer", "melt warmer", "wax pot", "melter", "clean the wax",
                 "clean a wax",
                 "cut down on sugar", "cut out sugar", "cutting out sugar", "cut sugar",
                 "eat less sugar", "less sugar", "so much sugar", "eating so much sugar",
                 "sugar habit", "sugar at night", "give up sugar", "quit sugar",
                 "too much sugar", "sugar in my diet", "sugar in your diet", "sugar cravings",
                 "sugar craving", "stop eating sugar", "added sugar",
                 "sugar free", "sugar-free", "reduce sugar", "reducing sugar", "how much sugar",
                 "sugar intake", "sugary", "fizzy drinks", "sweet tooth", "sweets",
                 "craving sugar", "crave sugar", "stop craving", "sugar rush", "sugar hit")))

_HEAL_PARTS = ("arm", "arms", "wrist", "wrists", "leg", "legs", "ankle", "ankles", "foot",
               "feet", "toe", "toes", "finger", "fingers", "thumb", "hand", "hands", "rib",
               "ribs", "collarbone", "clavicle", "shoulder", "elbow", "shin", "tibia", "fibula",
               "knee", "hip", "femur", "bone", "bones", "fracture", "fractured", "break",
               "broken", "cracked", "cast", "plaster")
_HEAL_TIME = ("how long", "how many weeks", "how long till", "how long until", "take to heal",
              "heal", "heals", "healing", "healed", "mend", "mends", "mending", "recover",
              "recovery", "back to normal", "back to work", "back to sport", "back to running",
              "back to football", "back to the gym", "in a cast", "off work", "how soon",
              "when can i", "play again", "playing again", "back to playing", "back on it",
              "again after")


_A_REST_NOT_A_BONE = re.compile(
    r"\b(?:my|your|our|their|his|her)\s+"
    r"(?:lunch|tea|coffee|dinner|toilet|rest|water|cigarette|fag)?\s*breaks?\b"
    r"|\b(?:lunch|tea|coffee|dinner|toilet)\s+breaks?\b"
    r"|\bbreaks?\s+(?:at|from|during|in)\s+(?:work|the shift|a shift|my shift|shift)\b"
    r"|\bbreaks?\s+between\s+shifts\b"
    r"|\bbreaks? at work\b"
    r"|\bshould (?:a|my|our) breaks? be\b")
_A_HEALING_WORD = re.compile(
    r"\b(?:heal|heals|healing|healed|mend|mends|mending|knit|knits|knitting|cast|plaster|"
    r"x-ray|xray|fracture|fractured|broken|pinned|pin|pins|physio|physiotherapy|set|setting)\b")
_A_PART_NAMED = (
    "arm", "arms", "wrist", "wrists", "leg", "legs", "ankle", "ankles", "foot", "feet",
    "toe", "toes", "finger", "fingers", "thumb", "hand", "hands", "rib", "ribs",
    "collarbone", "clavicle", "shoulder", "elbow", "shin", "tibia", "fibula", "knee",
    "hip", "femur", "bone", "bones", "fracture", "fractured", "surgery", "pinned",
    "metal plate", "screw", "screws")


_A_JOINT_OF_MEAT = re.compile(
    r"\b(?:lamb|beef|pork|chicken|turkey|duck|goose|brisket|gammon|veal|venison|meat|steak|"
    r"joint of|of lamb|of beef|of pork|roast)\b")


def _not_a_break_from_work(understood):
    said = str((understood or {}).get("text") or "").lower()
    if _A_JOINT_OF_MEAT.search(said):
        return False
    words = set(str(word).lower() for word in ((understood or {}).get("words") or ()))
    if words & set(_A_PART_NAMED):
        return True
    if _A_HEALING_WORD.search(said):
        return True
    return not _A_REST_NOT_A_BONE.search(said)


def _healing(memory, understood):
    words = set((understood or {}).get("words") or ())
    slow = words & {"leg", "legs", "shin", "tibia", "fibula", "femur", "ankle", "ankles",
                    "knee", "hip", "foot", "feet"}
    if slow:
        return ("Bones in the leg take the longest: about 12 weeks for a shin or ankle, and a "
                "thigh bone can be four months or more. The cast usually comes off before the "
                "bone is fully strong - it is the X-ray at each clinic visit that decides - and "
                "the muscles and joint need a few weeks after that to feel normal, so build back "
                "slowly rather than testing it early.")
    return ("About six weeks for most bones - six for a wrist or collarbone, six to eight for an "
            "arm, and longer for a leg or anything that had to be pinned, up to 12 weeks or more. "
            "Children heal faster, often in half the time. The cast comes off before the bone is "
            "fully strong and the joint takes a few more weeks to feel normal, and smoking slows "
            "bone healing a lot, so it is worth stopping while it knits.")


ENTRIES.append(entry(
    "bone-healing",
    (_HEAL_PARTS, _HEAL_TIME),
    _healing,
    guard=_not_a_break_from_work,
    avoid=("is it broken", "or broken", "or sprained", "do i need an x-ray",
           "do i need an xray", "how do i know", "how can i tell", "years ago", "last year",
           "when i was", "sticking out", "through the skin", "bone is showing", "999",
           "ambulance", "unconscious", "neck", "my back", "back pain", "lower back",
           "slipped disc", "spine", "my son", "my daughter",
           "my child", "my baby", "my dog", "my cat", "my mum", "my dad", "my husband",
           "my wife", "my partner",
           "cut", "cuts", "wound", "tattoo", "piercing", "burn", "scab", "sore", "gums",
           "tooth", "teeth", "wisdom tooth", "nail", "nails",
           "phone", "screen", "laptop", "tv", "telly", "washing machine", "car", "boiler",
           "hoover", "vacuum", "glasses", "heart", "heartbroken",
           "replacement", "knee replacement", "hip replacement", "resurfacing",
           "stock", "broth", "bouillon", "simmer", "carcass", "for stock", "for broth",
           "bone broth", "soup", "cook the bones", "roast the bones", "boil the bones",
           "beef bones", "chicken bones", "lamb bones", "ham bone", "bones for",
           "cook", "cooks", "cooking", "cooked", "boil", "boils", "boiled", "roast", "roasts",
           "roasted", "oven", "barbecue", "bbq", "grill", "grilled", "slow cooker", "recipe",
           "marinade", "marinate", "smoker", "air fryer")))

ACHE_WORDS = frozenset((
    "muscle", "muscles", "muscular", "sprain", "sprained", "strain", "strained", "pulled",
    "pull", "ache", "aches", "aching", "achy", "sore", "soreness", "stiff", "stiffness",
    "injury", "injured", "swollen", "swelling", "twinge", "cramp", "cramps", "tight",
    "back", "neck", "shoulder", "shoulders", "knee", "knees", "ankle", "ankles", "wrist",
    "wrist", "elbow", "hip", "hips", "thigh", "calf", "shin", "foot", "feet", "arm", "arms",
    "leg", "legs", "joint", "joints", "tendon", "ligament", "whiplash", "flaring", "flare"))
COMPRESS_WORDS = frozenset((
    "heat pack", "heat packs", "heat pad", "heat pads", "ice pack", "ice packs", "hot pack",
    "cold pack", "cold packs", "wheat bag", "wheat bags", "ice bath", "cold compress",
    "hot compress", "frozen peas", "ice cubes", "hot water bottle", "ice", "icing"))


_ON_A_BODY = ("ice it", "ice that", "ice my", "ice the", "icing it", "put ice", "use ice",
              "apply ice", "hold ice", "hold an ice", "ice pack on", "ice pack to", "pack on",
              "put a cold", "put heat", "use heat", "apply heat", "heat it", "heat that",
              "heat my", "heat the", "heat or ice", "ice or heat", "hot or cold", "cold or hot",
              "compress on", "should i ice", "should i heat", "frozen peas on", "peas on",
              "heat better than ice", "hot better than cold", "better than ice", "than ice",
              "better than heat", "than heat", "heat vs ice", "ice vs heat", "heat versus",
              "ice versus", "heat or cold", "cold or heat", "ice or hot", "heat and ice")
_HEAT_OR_ICE_THE_THING = re.compile(
    r"\b(?:heat|heating|ice|icing|hot|cold)\s+(?:the|my|our|that|this|a|an)\s+([a-z']+)")
_A_THING_THAT_IS_NOT_A_BODY = frozenset((
    "room", "rooms", "house", "houses", "home", "flat", "kitchen", "bedroom", "bathroom", "hall",
    "hallway", "lounge", "garage", "shed", "office", "conservatory", "loft", "attic", "cellar",
    "caravan", "car", "van", "bed", "bath", "shower", "pool", "greenhouse", "oven", "pan", "pot",
    "kettle", "mug", "cup", "bottle", "thermos", "cake", "buns", "bread", "milk", "wine", "beer",
    "water", "radiator", "radiators", "boiler", "heating", "thermostat", "air", "whole house",
    "place", "window", "windows", "door", "towel", "towel rail", "dehumidifier", "humidifier",
    "washing machine", "dryer", "tumble", "dishwasher", "microwave", "fridge", "freezer"))


_NOT_ON_A_BODY = ("cook", "cooks", "cooked", "cooking", "boil", "boils", "boiled", "boiling",
                  "oven", "bake", "baked", "baking", "recipe", "roast", "roasted", "fry",
                  "fried", "frying", "steam", "steamed", "steaming", "microwave", "defrost",
                  "defrosting", "thaw", "thawed", "saucepan", "freezer", "freeze", "freezes",
                  "freezing", "ice cube tray", "ice tray", "in the fridge",
                  "black ice", "gear", "pull away", "drive", "driving", "road", "roads", "tyre",
                  "tyres", "windscreen", "brake", "braking", "grit", "gritting", "pavement",
                  "pavements", "snow", "icy")


def _a_place_you_would_ice(understood):
    reading = understood if isinstance(understood, dict) else {}
    line = " " + " ".join(str(reading.get("clean") or reading.get("text") or "").lower().split()) + " "
    if any(" " + word + " " in line for word in _NOT_ON_A_BODY):
        return False
    for thing in _HEAT_OR_ICE_THE_THING.findall(line):
        if thing in _A_THING_THAT_IS_NOT_A_BODY and thing not in ACHE_WORDS:
            return False
    if any(" " + phrase + " " in line for phrase in _ON_A_BODY):
        return True
    for word in sorted(ACHE_WORDS, key=len, reverse=True):
        if " " + word + " " in line:
            return True
    return False


ENTRIES.append(entry(
    "heat-or-ice",
    (("heat", "ice", "hot", "cold", "warm", "warmth",
      "heat pack", "ice pack", "hot pack", "cold pack", "wheat bag", "heat pad",
      "hot water bottle", "ice bath", "cold compress", "frozen peas", "ice cubes"),
     ("should i use", "should i put", "should i apply", "do i use", "or heat", "or ice",
      "heat or ice", "ice or heat", "which is better", "which one", "better for", "good for",
      "better than", "rather than", "heat or cold", "cold or heat", "heat and cold",
      "what should i use", "help", "helps",
      "can i put", "can i use", "can i apply", "should i", "how long", "how often",
      "am i meant to")),
    "Cold for a fresh knock and heat for a stiff, old ache. Ice in the first 48 hours of a "
    "sprain, a bump or a pulled muscle: a bag of frozen peas or an ice pack wrapped in a tea "
    "towel, 15 to 20 minutes at a time, every two or three hours, never straight on the skin and "
    "never for longer, because that burns. After that, heat - a hot water bottle, a wheat bag or "
    "a warm bath, 15 to 20 minutes - loosens a muscle that has tightened up, so it is the one for "
    "a stiff neck or a back that has been bad for days. Never heat a fresh injury, a hot swollen "
    "joint or anywhere you cannot feel properly, and do not use either on broken skin. Heat on a "
    "sprain after two days is fine; ice on a stiff neck is not. If the joint is hot, very swollen "
    "or you cannot use it, that is a look-at-it-today rather than a compress.",
    guard=_a_place_you_would_ice,
    avoid=("stiff neck", "neck ache", "crick", "period", "periods", "cramps",
           "burn", "burned", "burnt", "scald", "scalded",
           "headache", "migraine", "temperature", "fever", "nappy rash", "toothache",
           "bruise", "bruises", "bruised", "hot bath", "bath", "sore muscles", "aching muscles",
           "dog", "cat", "baby", "pregnant", "pregnancy",
           "cheaper", "cheap", "cost", "costs", "expensive", "electricity", "energy", "bill",
           "bills", "tariff", "dehumidifier", "kilowatt", "kwh", "per hour", "running cost",
           "central heating", "heating on", "gas heating", "electric heating", "heat the house",
           "heating the house", "heating bill", "heating the flat", "radiator", "radiators",
           "boiler", "heat pump")))
_MUSCLE_PARTS = ("hamstring", "hamstrings", "pulled hamstring", "torn hamstring",
                 "hamstring strain", "hamstring injury", "calf", "calves", "calf muscle",
                 "pulled calf", "torn calf", "calf strain", "groin", "groin strain",
                 "pulled groin", "adductor", "thigh muscle", "quad", "quads", "quadriceps",
                 "torn muscle", "tore a muscle", "muscle tear")


def _muscle_healing(memory, understood):
    words = set((understood or {}).get("words") or ()) | set((understood or {}).get("background") or ())
    slow = words & {"hamstring", "calf", "calves", "tear", "tore", "torn", "badly",
                    "completely", "snapped"}
    if words & {"groin", "adductor"}:
        return ("A groin strain is usually two to six weeks, and the milder ones are back in a "
                "fortnight: the first week is ice and rest from the twisting and kicking, then "
                "gentle stretching, and back to football or five-a-side only when you can sprint "
                "and change direction without pain. A sudden sharp pain, or a lump that appears in "
                "the groin when you cough, wants a physio rather than time.")
    if slow:
        return ("A torn hamstring or calf is four to eight weeks, and the last third of that is "
                "the part people rush: run again only when you can move it through its full "
                "range without pain and it feels as strong as the other side. A sudden snap, a "
                "lot of bruising, or a dent in the muscle wants a physio this week rather than "
                "rest alone.")
    return ("A pulled thigh muscle is usually two to three weeks: ice it for 15 minutes every few "
            "hours for the first two days, then keep it gently moving, because gentle movement "
            "heals faster than total rest. Go back to sport when it moves fully without pain and "
            "feels as strong as the other side, and see a physio if it is no better after a "
            "fortnight.")


ENTRIES.append(entry(
    "muscle-healing",
    (_MUSCLE_PARTS, _HEAL_TIME),
    _muscle_healing,
    bias=2,
    avoid=("build muscle", "building muscle", "muscle mass", "gain muscle",
           "grow muscle", "put on muscle", "muscle tone", "bulk", "protein", "shakes",
           "sets and reps", "workout", "gym", "soreness", "doms",
           "day after", "next day", "delayed onset",
           "my dog", "my cat", "my puppy", "my horse", "my son", "my daughter", "my child",
           "my baby", "my husband", "my wife", "my partner", "my mum", "my dad",
           "pulled pork", "pulled beef", "pulled chicken", "pulled jackfruit", "pork",
           "beef", "chicken", "jackfruit", "cook", "cooks", "cooking", "cooked", "oven",
           "slow cooker", "recipe", "air fryer", "bake", "baked", "stock", "sieve",
           "drain", "juice", "yoghurt", "yogurt", "curds",
           "heart", "chest", "head", "eye", "eyes", "jaw", "stomach", "tummy",
           "swollen", "swelling", "hot", "red", "clot", "numb", "tingling", "one side",
           "pregnant", "pregnancy", "surgery", "operation", "replacement")))


ENTRIES.append(entry(
    "piercing-infection",
    (("piercing", "piercings", "pierced ear", "ear piercing", "nose piercing", "nose ring",
      "nose stud", "nose hoop", "septum", "helix", "tragus", "daith", "cartilage piercing",
      "earring hole", "earring", "belly piercing", "belly button piercing", "belly bar",
      "lip piercing", "eyebrow piercing", "industrial piercing", "earlobe"),
     ("red", "redness", "swollen", "swelling", "hot", "weeping", "oozing", "pus", "yellow",
      "green", "infected", "infection", "spreading", "streaking", "throbbing", "smelly",
      "fever", "angry", "sore and", "hurts")),
    _piercing_infection,
    guard=_a_piercing_in_trouble,
    bias=2,
    avoid=("how long", "aftercare", "keloid", "crusty", "crust", "when can i change",
           "downsize", "can i swim", "how do i clean", "how do i look after")))


_TAMPON_WORD = re.compile(r"\btampons?\b")
_NOT_A_TAMPON_LINE = re.compile(
    r"\b(bins?|bin it|dispose|disposal|throw (?:it|them) away|flush\w*|down the loo|"
    r"wrapper|applicator|recycl\w*|compost\w*|landfill)\b")


def _a_tampon_worn_too_long(understood):
    reading = understood if isinstance(understood, dict) else {}
    said = " ".join([str(reading.get("clean") or ""),
                     " ".join(str(word) for word in (reading.get("words") or ()))])
    return bool(_TAMPON_WORD.search(said)) and not _NOT_A_TAMPON_LINE.search(said)


ENTRIES.append(entry(
    "tampon-how-long",
    (("tampon", "tampons"),
     ("how long", "how often", "leave", "leaves", "stay in", "stays in", "staying in",
      "keep in", "keeps in", "keeping it in", "in for", "overnight", "sleep", "slept",
      "all night", "asleep", "fell asleep", "hours", "long can", "long should",
      "when should", "forgot", "forget", "change", "changed", "changing", "safe", "okay",
      "ok", "can i", "should i", "wear", "wearing", "use", "using", "put one in")),
    "Change a tampon every four to six hours and never leave one in for more than eight, so "
    "take it out before bed rather than sleep through with the same one. Use the lowest "
    "absorbency that still lasts four hours, wash your hands before and after, and if one has "
    "been in longer than that take it out now and watch for a fever, a rash like sunburn, "
    "vomiting, dizziness or a sore throat: that is toxic shock syndrome, which is rare but "
    "serious, so ring 111 for advice. Contact lenses and retainers have their own limits, and "
    "pads rather than tampons are the answer during pregnancy and for the first weeks after a "
    "baby.",
    guard=_a_tampon_worn_too_long,
    bias=1))


ENTRIES.append(entry(
    "the-wait-at-a-walk-in-centre",
    ("walk in centre", "walk-in centre", "walk in center", "walk in clinic",
     "walk-in clinic", "walk in service", "urgent care centre", "urgent care center",
     "urgent treatment centre", "minor injuries unit", "minor injuries",
     "out of hours gp", "out of hours doctor", "the walk in"),
    "Nobody can tell you before you go: a walk-in centre sees people in the order they need "
    "seeing rather than the order they arrived, so a queue of two hours can move in twenty "
    "minutes when something urgent comes in, and a quiet room can still mean a long wait. Ring "
    "the centre or look at its own site on the day for the wait it is running, and go early "
    "rather than late in the evening. Take a drink, a book and any medicines you take with you, "
    "and tell the desk if you get worse while you are sitting there rather than wait your turn.",
    ask=("wait", "waits", "waiting", "queue", "how long", "long will", "long do i",
         "how quick", "busy", "packed", "hours", "tonight", "this evening", "weekend"),
    avoid=("how do i get", "parking", "postcode", "address", "where is", "nearest",
           "walk up", "walk to", "how far", "open on christmas", "phone number")))


_OFF_A_THING = ("came off", "fell off", "fell from", "come off", "fall off", "went over the",
                "over the handlebars", "came a cropper")
_FALL_AVOID = ("chain", "chains", "derailleur", "gears", "gearset", "brake", "brakes", "pedal",
               "pedals", "wheel", "wheels", "tyre", "tyres", "tire", "tires", "saddle", "sprocket",
               "cassette", "handlebar", "mudguard", "rack", "pannier", "battery",
               "motor", "throttle", "exhaust", "spark plug", "clutch", "pill", "medication",
               "my meds", "wagon", "a lorry", "the back of a lorry", "radar", "the list",
               "diet", "my food", "the challenge", "bandwagon", "sales", "orders", "shares", "price",
               "prices", "paint", "button", "handle", "sticker", "label", "wallpaper", "tiles",
               "the map", "nearly fell", "nearly came",
               "hurt", "hurts", "hurting", "sore", "ache", "aches", "aching", "pain", "painful",
               "broken", "break", "fracture", "swelling", "swollen", "can't move", "cant move")

ENTRIES.append(entry(
    "came-off-a-thing",
    (_OFF_A_THING,
     ("bike", "bikes", "bicycle", "cycle", "horse", "pony", "scooter", "motorbike", "motorcycle",
      "moped", "ladder", "trampoline", "skateboard", "skates", "skis", "sled", "sledge",
      "roof", "wall", "stairs", "steps", "horse", "quad", "go kart", "swing", "climbing frame",
      "bruise", "bruised", "graze", "grazed", "gashed", "landed", "hit", "banged", "knocked",
      "arm", "wrist", "elbow", "shoulder", "collarbone", "knee", "hip", "ankle", "hand", "head",
      "ribs", "walk", "weight")),
    "Coming off is a fall, so check the head first: a bang that knocked them out, made them sick, "
    "left them confused or gave them a bad headache is A&E the same day, and so is anything they "
    "cannot remember. Most falls land on a hand or a shoulder, and a wrist that cannot take weight "
    "or an arm that cannot be lifted across the chest is worth an X-ray today - the collarbone is "
    "the break people miss. Grazes want cool running water, a dressing and no scrubbing. Ice a "
    "bruise for 20 minutes at a time with a cloth round it, take paracetamol or ibuprofen if you "
    "can, and expect it to be stiffer tomorrow than today. A helmet that took the hit is finished, "
    "even with no crack you can see.",
    avoid=_FALL_AVOID,
    bias=0))
