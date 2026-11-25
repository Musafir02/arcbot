
import re

from .lookup import a_thing_has_stopped, entry
from .wording import screens_are_somebody_elses

PET_SUBJECT = ("dog", "dogs", "puppy", "puppies", "pup", "pups", "cat", "cats", "kitten",
               "kittens", "rabbit", "rabbits", "bunny", "bunnies", "hamster", "hamsters",
               "guinea pig", "guinea pigs", "gerbil", "gerbils", "ferret", "ferrets",
               "parrot", "parrots", "bird", "birds", "horse", "horses", "pony", "ponies",
               "tortoise", "tortoises", "pet", "pets", "litter tray")

_PET_ANY = re.compile(r"\b(?:" + "|".join(re.escape(word) for word in PET_SUBJECT) + r")\b")


def _about_a_pet(understood):
    if not isinstance(understood, dict):
        return False
    said = []
    remembered = understood.get("ref")
    if isinstance(remembered, dict):
        said.extend(value for value in remembered.values() if isinstance(value, str))
    leans = understood.get("leans_on")
    if isinstance(leans, dict):
        subject = leans.get("subject")
        if isinstance(subject, str):
            said.append(subject)
        text = leans.get("text")
        if isinstance(text, str):
            said.append(text)
    return bool(said) and bool(_PET_ANY.search(" ".join(said).lower()))


MOUTH_TIP = ("Give the mouth or the fingers a stand-in: gum, a straw to chew, a pen you cannot "
             "bite to pieces, a bead on a chain. It happens at a desk or in front of a screen, so "
             "put the substitute where you sit and move the pen or the mirror out of reach.")


def _pet_row_answers_before_it(memory, understood):
    from . import entries as all_entries
    from .lookup import score, _forms
    if not isinstance(understood, dict):
        return False
    leans = understood.get("leans_on")
    carried = []
    if isinstance(leans, dict) and isinstance(leans.get("words"), list):
        carried = [word for word in leans["words"] if isinstance(word, str)]
    words = [word for word in (understood.get("words") or []) if isinstance(word, str)]
    together = [_forms(word) for word in carried + words]
    if not together:
        return False
    try:
        for item in all_entries():
            if getattr(item, "domain", "") == "pets" and score(item, together, carried + words):
                return True
    except Exception:
        return False
    return False


def _mouth_tip(memory, understood):
    if _about_a_pet(understood) and _pet_row_answers_before_it(memory, understood):
        return None
    return MOUTH_TIP

_ANOTHER_ADULT = (
    r"(?:mum|mom|mam|mother|dad|father|parent|parents|husband|wife|partner|spouse|"
    r"other half|nan|nana|gran|granny|grandma|grandad|grandpa|grandmother|grandfather|"
    r"son|daughter|child|kid|brother|sister|aunt|auntie|uncle|cousin|in law|"
    r"mother in law|father in law|friend|neighbour|neighbor|boss|colleague|coworker|"
    r"flatmate|housemate|landlord|carer|pal|chum|mate|nephew|niece|grandchild|grandson|"
    r"granddaughter|fiance|fiancee|stepmum|stepdad|sister in law|brother in law|missus|"
    r"other half|girlfriend|boyfriend)")
_FORGOTTEN = (r"(?:forget|forgets|forgetting|forgot|forgotten|forgetful|forgetfulness|"
              r"memory|remember|remembers|repeating|repeats|confused|confusion|"
              r"getting confused|scatty|absent[- ]minded|away with it)")
_SOMEONE_ELSE_FORGETTING = re.compile(
    r"\b(?:my|his|her|our|their|the)\s+(?:\w+\s+){0,2}" + _ANOTHER_ADULT + r"\b"
    r"[^.!?]{0,30}?\b" + _FORGOTTEN + r"\b|"
    r"\b(?:he|she|they)\s+(?:keeps?|is|are|has|have|always|never|used to)\b"
    r"[^.!?]{0,25}?\b" + _FORGOTTEN + r"\b")


_MY_AGE = re.compile(
    r"\b(?:im|i am|i'm)\s+(?:nearly |almost |just |only )?"
    r"(?:\d{2}|forty|fifty|sixty|seventy|eighty|ninety)\b|\bat my age\b|\bmy age\b|"
    r"\bgetting older\b|\bas i get older\b|\bsince i turned\b")
_FORGETTING = re.compile(
    r"\b(?:forget|forgets|forgetting|forgot|forgotten|forgetful|memory|remember)\b")


def _my_own_memory_and_my_age(understood):
    from ..compose.repair import line_of
    said = line_of(understood)
    if not said:
        return False
    text = " ".join(str(said).lower().replace("\u2019", "'").split())
    return bool(_MY_AGE.search(text) and _FORGETTING.search(text))


def _words_of(understood):
    from ..compose.repair import line_of
    said = [line_of(understood)]
    if isinstance(understood, dict):
        for key in ("leans_on", "ref", "topic"):
            value = understood.get(key)
            if isinstance(value, dict):
                said.extend(str(item) for item in value.values() if isinstance(item, (str, int)))
                words = value.get("words")
                if isinstance(words, (list, tuple)):
                    said.extend(word for word in words if isinstance(word, str))
            elif isinstance(value, (list, tuple)):
                said.extend(word for word in value if isinstance(word, str))
    return " ".join(" ".join(said).lower().replace("\u2019", "'").split())


def _someone_else_is_forgetting(understood):
    text = _words_of(understood)
    if not text:
        return False
    return bool(_SOMEONE_ELSE_FORGETTING.search(text)
                or _MY_AGE.search(text))


_A_RELATIVE = re.compile(
    r"\b(?:my|his|her|their|our)\s+(?:mum|mom|mother|dad|father|parents|gran|granny|nan|nana|"
    r"grandma|grandmother|grandad|grandpa|grandfather|grandparents?|wife|husband|partner|spouse|"
    r"other half|son|daughter|brother|sister|aunt|auntie|uncle|cousin|boyfriend|girlfriend|"
    r"friend|mate|neighbour|neighbor|mother in law|father in law)\b")
_SOMEBODY_ELSE = re.compile(
    r"\b(?:he|she|they)\s+(?:keeps?\s+forgetting|forgets|is\s+forgetful|"
    r"cant\s+remember|can't\s+remember|cant\s+recall|can't\s+recall|repeats|is\s+confused)")
_SOMETHING_FORGOTTEN = re.compile(
    r"\b(?:forgett?ing|forgets|forgetful|remember|remembers|recall|repeat(?:s|ing)?|"
    r"confused|gets lost|losing|loses)\b")


def _the_writer_is_the_one_forgetting(understood):
    if not isinstance(understood, dict):
        return True
    said = " ".join(str(understood.get("clean") or understood.get("text") or "").split()).lower()
    if not said:
        return True
    if _SOMEBODY_ELSE.search(said):
        return False
    relative = _A_RELATIVE.search(said)
    if relative and _SOMETHING_FORGOTTEN.search(said[relative.end():]):
        return False
    return True


FEEL_BAD = ("feel awful", "feel terrible", "feel horrible", "feel like giving up",
            "i feel rubbish", "feel so low", "feel depressed")

THIRD_PARTY = ("my husband", "my wife", "my partner", "my boyfriend", "my girlfriend",
               "my mum", "my dad", "my parents", "my son", "my daughter", "my brother",
               "my sister", "my friend", "my friends", "my nan", "my gran", "my granny",
               "my grandma", "my grandad", "my grandpa", "my grandparent",
               "my uncle", "my aunt", "my auntie", "my cousin", "my colleague", "my mate",
               "my mother in law", "my father in law", "my flatmate", "help my",
               "he wants to", "she wants to", "he keeps", "she keeps")

STOP = ("quit", "quitting", "quit for good", "stop", "stopping", "give up", "giving up",
        "cut down", "cutting down",
        "cut back", "cutting back", "cut back on", "cutting back on", "ease off", "easing off",
        "pack in", "packed in", "cant stop", "can't stop",
        "quit smoking", "stop smoking", "give up smoking", "quit cigarettes",
        "stop drinking", "quit drinking", "cut down on drinking", "cut down on alcohol",
        "quit vaping", "stop vaping")


SMALL_HABITS = (
    ("skin", ("skin picking", "picking my skin", "pick my skin", "picking at my skin",
              "picking spots", "picking at spots", "picking my spots", "picking at my face",
              "picking my face", "picking at scabs", "picking scabs", "picking a scab",
              "picking", "picking at"),
     "Picking is a hand habit, so give the hand something else: moisturise so the spot feels "
     "different, keep a fidget toy or a ring where your fingers go, and cover it with a plaster "
     "for the first week so your fingers stop there. Mirrors and screens are where it starts, so "
     "keep them out of reach."),
    ("knuckles", ("knuckles", "cracking my knuckles", "crack my knuckles", "cracking knuckles",
                  "fidgeting", "fidget", "jiggling my leg", "shaking my leg",
                  "bouncing my leg"),
     "Cracking and fidgeting are how the body burns off a wriggle, so the fix is a quieter outlet "
     "rather than sitting still: a stress ball in your pocket, a foot pressed to the floor, or a "
     "short walk every hour. It happens most in meetings and while waiting."),
    ("temper", ("anger", "angry", "temper", "irritable", "irritated", "irritability",
                "rage", "raging", "losing my temper", "lose my temper", "lost my temper",
                "short fuse", "snappy", "snapping at", "snapped at", "lashing out",
                "blowing up", "blow up at"),
     "Anger is mostly a physical build-up, so catch it early rather than arguing with it: notice "
     "the first sign - jaw, shoulders, a louder voice - and leave the room for five minutes, "
     "breathing out for longer than you breathe in. Say \"I need a minute\" rather than the thing "
     "you are about to say. Then look at the fuel: too little sleep, no lunch, four coffees and a "
     "hangover will do more to your temper than any argument. If the fuse has been short for weeks "
     "rather than days, see a GP: anxiety, depression and a thyroid problem all arrive as "
     "irritability, and talking therapy works on anger."),
    ("worry", ("worry", "worrying", "worried", "anxiety", "anxious", "panicky", "dread",
               "overwhelmed",
               "nerves", "my nerves", "on edge", "wound up", "keyed up", "butterflies",
               "racing heart", "nervous",
               "calm down", "calm myself down", "worked up", "shaky", "jittery",
               "stop worrying", "worrying about", "worry about", "worries about", "worries me",
               "worrying me", "keep worrying", "always worrying", "worrying all the time",
               "how do i relax", "relax", "relaxing", "cant relax", "can't relax"),
     "Give the worry a time and a page: fifteen minutes in the evening when you write down "
     "everything on your mind, then ask of each one what you would actually do if it happened, "
     "and what the next step is. When it turns up at three in the afternoon, write one line to "
     "bring to the slot and go back to what you were doing - postponing is the part that trains "
     "it. Ten slow breaths out, longer than the in, settle the body enough to do that. If it is "
     "most days for six months or more, that is worth the GP and talking therapy, which works "
     "well on this."),
    ("swearing", ("swearing", "swear", "bad language", "foul language", "cursing"),
     "Pick one substitute word and use it out loud for a week - 'sugar', 'flip', whatever you can "
     "say at work - because the habit is in the sound, not the meaning. It spikes with pain and "
     "frustration, so slow your breath for a second before you answer."),
    ("snooze", ("snooze", "snoozing", "hitting snooze", "my alarm", "alarm"),
     "Put the alarm across the room and take the first one for a week, even when you are tired: "
     "the nine extra minutes cost you the deep sleep at the end of the night and leave you "
     "groggier. If mornings are brutal, go to bed half an hour earlier that week."),
    ("hair", ("pulling my hair", "pull my hair", "pulling my hair out", "twirling my hair",
              "twirl my hair", "twirling hair", "chewing my hair", "biting my hair",
              "playing with my hair", "hair twirling", "trichotillomania"),
     "Keep it up and back - a bobble, a clip, a hat - so there is nothing loose for your fingers to "
     "find, and give them a ring to reach for instead. It happens most when you are bored or "
     "thinking hard. If you are pulling hair out in patches, see a GP: it is a known condition, "
     "not something you do on purpose."),
    ("mouth", ("chewing my pen", "chew my pen", "biting my pen", "chewing gum", "chewing",
               "chewing my fingers", "chew my fingers", "biting my fingers",
               "biting my cheeks", "biting my lips", "chewing my lips", "licking my lips"),
     _mouth_tip),
)

STOP_SMALL = ("stop", "stopping", "quit", "quitting", "kick", "kicking", "give up", "giving up",
              "cut down", "cutting down", "cut back", "get out of", "cant stop", "can't stop",
              "how do i stop", "i keep", "keep", "i always",
              "how do i control", "how can i control", "how do i manage", "how do i handle",
              "how do i deal with", "how do i get rid of", "how can i stop", "how can i quit",
              "help me stop", "what can i do about")

HABIT_WORDS = ("habit", "habits", "routine", "routines", "streak", "willpower", "resolution")

HABIT_TIME_WORDS = ("how long", "how many days", "how many weeks", "take", "takes", "took",
                    "days", "weeks", "months", "21 days", "three weeks", "66 days", "really",
                    "how long does it take", "how long to break", "how long to stop",
                    "how many days", "how many weeks")

NOT_A_SMALL_HABIT = ("tyre", "tire", "puncture", "scratch", "screw", "hammer", "polish",
                     "hoover", "vacuum", "dyson", "mower", "lawnmower", "crumbs", "crumb",
                     "varnish", "manicure", "salon", "split", "splitting", "peel", "peeling",
                     "chipping", "brittle", "strengthen", "grow", "growing", "fake", "acrylic",
                     "extensions", "dentist", "tooth", "teeth", "guitar", "piano",
                     "data", "battery", "storage", "signal", "contract", "sim", "bill",
                     "network", "wifi", "hacked", "stolen", "lost my phone", "screen",
                     "smoking", "smoke", "cigarette", "cigarettes", "vape", "vaping",
                     "alcohol", "drinking", "drink", "beer", "wine", "hangover",
                     "bet", "betting", "gambling", "porn", "drugs",
                     "breaking out", "breakout", "break outs", "acne",
                     "brittle", "snapping", "splitting", "split end", "split ends", "frizzy",
                     "frizz", "dry", "dryness", "greasy", "itchy", "itching", "rash",
                     "eczema", "dermatitis", "thinning", "hair loss", "bald", "dandruff",
                     "colour", "dye", "dyeing", "heartburn", "reflux", "indigestion",
                     "acid", "bloating", "hiccups", "cough", "snoring", "snore",
                     "picky eater", "picky eaters", "fussy eater", "fussy eaters",
                     "faddy eater", "picky husband")

SMALL_HABIT_EXTRA_AVOID = {
    "temper": ("kid", "kids", "child", "children", "son", "daughter", "toddler", "baby",
               "my mum", "my mom", "my dad", "my brother", "my sister", "my boss", "my manager",
               "neighbour", "neighbor", "dog", "puppy", "cat", "traffic", "driver", "road",
               "computer", "laptop", "phone", "game", "football", "referee",
               "shouting at my kids", "at my kids", "at the kids", "at my children",
               "at my partner", "at my husband", "at my wife", "snapping at my partner",
               "his temper", "her temper", "their temper", "your temper",
               "loses his temper", "loses her temper", "lost his temper", "lost her temper",
               "losing his temper", "losing her temper", "his rag", "her rag",
               "temper with me", "loses it with me", "lost it with me"),
    "worry": ("dog", "dogs", "cat", "puppy", "kitten", "pet", "pets", "money", "rent", "bill",
              "bills", "job", "work", "office", "boss", "deadline", "shift", "interview", "exam", "exams", "test", "results", "health",
              "cancer", "lump", "pregnant", "pregnancy", "mum", "mom", "dad", "son", "daughter",
              "child", "children", "kid", "kids", "baby", "flight", "flying", "wedding",
              "party", "speech", "presentation", "the future", "the news",
              "puppies", "pup", "cats", "kittens", "rabbit", "bird", "parrot", "horse",
              "toddler", "toddlers", "palpitations", "racing heart when", "chest pain",
              "short of breath", "nervous system", "nerve pain", "trapped nerve", "sciatica",
              "pinched nerve", "root canal", "tooth nerve", "nerves in my", "afraid of the dark",
              "customer", "customers", "patient", "patients", "passenger", "client", "clients",
              "colleague", "colleagues", "staff", "crew", "someone else", "the other one"),
    "mouth": ("dog", "dogs", "puppy", "pup", "cat", "cats", "kitten", "kittens", "pet", "pets",
              "rabbit", "hamster", "parrot", "bird", "horse", "teething", "sleeve", "collar",
              "nail", "nails", "nail biting", "cuticles",
              "clothes", "clothing", "shirt", "shirts", "trousers", "jeans", "dress", "dresses",
              "skirt", "jumper", "jumpers", "cardigan", "coat", "jacket", "hoodie", "leggings",
              "shorts", "towel", "bedding", "sheet", "sheets", "duvet", "fabric", "wool",
              "carpet", "carpets", "rug", "rugs", "sofa", "settee", "couch", "mattress",
              "upholstery", "floor", "floors", "tiles", "pavement", "path", "wall", "walls",
              "shoe", "shoes", "trainer", "trainers", "boot", "boots", "table", "chair",
              "washing machine", "dryer", "tumble dryer", "car seat", "car", "seats"),
    "snacks": ("sugar", "sugary", "sugar in", "sugars",
               "night", "at night", "in the evening", "evening", "after dinner", "late",
               "before bed", "night time", "nighttime"),
    "snooze": ("burglar", "burglars", "intruder", "intruders", "house alarm",
               "security alarm", "security system", "alarm system", "alarm panel",
               "control panel", "the panel", "sensor", "sensors", "cctv", "smoke",
               "smoke alarm", "smoke detector", "carbon monoxide", "car alarm",
               "alarm on my car", "van", "vehicle", "fob", "key fob", "immobiliser",
               "siren", "car park", "mechanic", "pendant", "pendant alarm", "falls alarm",
               "fall alarm", "personal alarm", "telecare", "careline", "lifeline",
               "care alarm", "panic alarm", "panic button", "medical alarm"),
}

WORRY_ASK = STOP_SMALL + (
    "calm", "calming", "calm down", "calm myself down", "how do i calm", "how can i calm",
    "settle", "settle myself", "how do i settle", "chill out", "wind down", "feel better",
    "get through")

WORRY_ASK = WORRY_ASK + (
    "how do i", "how can i", "what helps", "what helps with", "what can i do", "helps",
    "help", "helping", "what should i do", "any tips", "tips")

SMALL_HABIT_EXTRA_AVOID["worry"] = SMALL_HABIT_EXTRA_AVOID.get("worry", ()) + (
    "hair", "hairs", "my hair", "relaxer", "relaxers", "relax my hair", "relaxing my hair",
    "beard", "braids",
    "doctor", "gp", "gp appointment", "appointment", "surgery", "nurse", "practice nurse",
    "headache", "headaches", "migraine", "symptom", "symptoms", "pain", "ache", "aches",
    "spot", "spots", "mole", "lump", "bleeding", "fever", "temperature", "test results",
    "scan", "x-ray", "results")

SMALL_HABIT_ASK = {"worry": WORRY_ASK}

_ANOTHER_PERSONS_MEMORY = re.compile(
    r"\b(?:mum|mom|mother|dad|father|parent|parents|grandma|grandmother|grandad|grandfather|"
    r"gran|nan|nana|granny|wife|husband|partner|spouse|other half|mother in law|father in law|"
    r"aunt|auntie|uncle|brother|sister)\b[^.?!]{0,40}"
    r"\b(?:forgets?|forgetting|forgetful|forgot|keeps forgetting|repeats|repeating|confused|"
    r"confusion)\b")


def _the_errand_is_the_speakers_own(understood):
    said = str(understood.get("clean") or "").lower()
    if not _ANOTHER_PERSONS_MEMORY.search(said):
        return True
    return bool(re.search(r"\bto\b", said))


SMALL_HABIT_ENTRIES = [
    entry("stop-" + name, (keys, SMALL_HABIT_ASK.get(name, STOP_SMALL)), tip,
          avoid=NOT_A_SMALL_HABIT + THIRD_PARTY + FEEL_BAD
                + SMALL_HABIT_EXTRA_AVOID.get(name, ()), bias=1)
    for name, keys, tip in SMALL_HABITS
]


EXTRA_ENTRIES = [
    entry("habit-time", (HABIT_WORDS, HABIT_TIME_WORDS),
          "About two months, not the three weeks people quote: in the study that measured it the "
          "median was 66 days, and the easy ones (a glass of water with breakfast) settled in a "
          "few weeks while the hard ones took most of a year. Missing one day made no difference "
          "to how long it took, so a slip is not a restart - the rule is never miss twice.",
          avoid=("work break", "shift", "rest between", "holiday", "annual leave", "routine "
                 "blood test", "morning routine for school",
                 "gym", "gyms", "workout", "workouts", "exercise", "training", "run", "running",
                 "walk", "commute", "morning routine", "bedtime routine", "evening routine",
                 "school run",
                 "breaking my streak", "broke my streak", "breaks my streak",
                 "keep breaking my streak", "streak keeps breaking", "losing my streak",
                 "lost my streak", "ruined my streak", "missed my streak", "keep breaking the",
                 "my streak", "the streak", "missed a day", "miss a day"),
          bias=3),

    entry("habit-build", (HABIT_WORDS + ("something new", "something every day"),
                          ("build", "start", "make it stick", "make a habit", "make it a habit",
                           "form", "stick", "sticking", "keep up", "new", "begin",
                           "get into", "get back into", "every day", "daily")),
          "Attach it to something you already do every day - after the kettle boils, after you "
          "brush your teeth - because a new habit needs an old one to hang on. Make the first "
          "version almost too small to fail (one page, one glass, two minutes), keep it in the "
          "same place and time, and put a tick on a wall calendar: the streak is what carries it "
          "past the first fortnight, when the novelty has gone.",
          avoid=("work break", "shift", "holiday", "salary", "job", "interview", "pan",
                 "oven", "recipe", "sauce", "bake"),
          bias=1),
    entry("retired-and-at-a-loss",
          (("retire", "retires", "retiring", "retired", "retirement", "gave up work",
            "given up work", "stopped working", "no longer working", "finished work",
            "left work", "packed in work", "last day at work", "not working any more",
            "not working", "no work to go to", "stopped work", "given up work"),
           ("lost", "at a loss", "feel lost", "normal", "strange", "odd", "weird", "adjust",
            "adjusting", "get used to", "getting used to", "cope", "coping", "struggling",
            "what do i do", "what do people do", "what to do with myself", "know what to do",
            "what now", "bored", "boredom", "lonely", "loneliness", "miss", "missing",
            "structure", "routine", "purpose", "with myself", "nothing to do", "keep busy",
            "keep occupied", "how do i", "tips", "advice")),
          "That lost feeling is the usual thing and it has a shape: the first few months are the "
          "holiday, the flat part comes next, and by a year most people have a week they like "
          "again. What went with the job was not only the money - it was the diary, the reason to "
          "be up, and the people you saw without arranging it. So rebuild those three on purpose "
          "and small: one fixed thing a week that somebody expects you at (a class, a shift at a "
          "charity shop, a badminton game, a regular coffee), one reason to be dressed and out by "
          "nine on a weekday, and one afternoon a week that is properly yours. Say yes to the "
          "first invitation even when staying in is easier, because the invitations thin out when "
          "you stop going. If the mornings are still heavy all day after six months, mention it to "
          "the GP - low mood after a big change is common and treatable - but drift at the start "
          "is not a warning sign, it is the gap between one life and the next.",
          avoid=("pension", "pensions", "state pension", "pot", "savings", "money", "afford",
                 "tax", "annuity", "drawdown", "lump sum", "ni", "national insurance",
                 "how much", "how many years", "when can i", "at 55", "at 60", "at 65", "at 66",
                 "at 67", "early retirement", "retire early", "my husband", "my wife",
                 "my partner", "my mum", "my dad", "my colleague", "my boss", "he ", "she ",
                 "party", "parties", "retirement party", "leaving do", "leaving party",
                 "celebrate", "celebration", "send off", "guest list", "invitations",
                 "invite people", "venue", "catering", "speech", "toast", "present", "gift"),
          bias=3,
          guard=lambda understood: not a_thing_has_stopped(understood)),

    entry("always-late", (("always late", "im always late", "i am always late",
                           "i'm always late", "stop being late", "keep being late",
                           "keeps being late", "never on time", "not on time", "punctual",
                           "timekeeping", "time keeping", "late again", "late for everything",
                           "late every day", "always rushing", "running out of time in the morning"),
                          ("how", "why", "stop", "help", "advice", "tips", "time", "morning",
                           "better", "fix", "always", "keep", "what", "should")),
          "Lateness is nearly always the plan rather than the person: time one real journey at the "
          "hour you actually travel and add ten minutes, then set an alarm for leaving rather than "
          "only for waking. Lay out clothes, bag and keys the night before, and book the one "
          "earlier train instead of telling yourself you will hurry. If it is the last five "
          "minutes that keep going, drop the one job you do on the way out: being five minutes "
          "early costs nothing.",
          avoid=("parcel", "parcels", "delivery", "deliveries", "train", "trains", "bus", "buses",
                 "flight", "flights", "payment", "rent", "bill", "bills", "fee", "fees",
                 "my pay", "our pay", "the pay", "wages", "wage", "salary", "payslip",
                 "payslips", "payday", "payroll", "pay packet", "paid me", "refund", "invoice",
                 "period", "periods", "pregnant", "baby", "midwife", "deadline", "tax return",
                 "boss", "manager", "interview", "school run", "night shift", "late for work?",
                 "sorry im late", "tell my boss", "what do i say"),
          bias=1),

    entry("meditate-start",
          (("meditation", "meditate", "meditating", "meditates", "meditated", "mindfulness",
            "mindful", "breathing exercise", "breathing exercises", "headspace", "mbsr", "mbct",
            "guided meditation"),
           ("start", "begin", "learn", "how", "long", "often", "work", "works", "worth",
            "help", "helps", "better", "app", "apps", "beginners", "beginner", "every day",
            "daily", "routine", "habit", "should", "try", "anxiety", "anxious", "stress",
            "stressed", "calm", "panic", "relax"),
           ("wander", "wanders", "wandering", "wandered", "wandering mind", "mind wanders",
            "distracted", "distraction", "drift", "drifts", "drifting", "monkey mind")),
          "Five minutes sitting still with your attention on your breathing is the whole of it: "
          "the mind wanders, you notice and come back, and the coming back is the exercise, not a "
          "failure. Same time each day, for two weeks before you judge it. The eight-week "
          "courses, MBSR and MBCT, are the ones that have been tested, for low mood and for "
          "anxiety, and an app like Headspace teaches the same thing.",
          avoid=("pray", "prayer", "praying", "bible", "church", "yoga", "pilates",
                 "cough", "asthma", "inhaler", "peak flow", "baby", "toddler", "child",
                 "children", "kids", "kid", "school", "sleep", "insomnia"),
          bias=1),

    entry("meditation-what-it-is",
          (("meditation", "meditating", "meditate", "mindfulness", "mindful", "mbsr", "mbct"),
           ("what", "whats", "is", "are", "mean", "means", "meaning", "definition",
            "define", "explain", "explained", "difference", "different", "actually")),
          "Meditation is paying attention to one thing on purpose - usually the breath - and coming "
          "back to it each time you notice you have drifted; an empty mind is not the aim, and the "
          "noticing is the skill. The tested versions are the eight-week courses, MBSR and MBCT, "
          "mainly for low mood and anxiety.",
          avoid=("pray", "prayer", "praying", "bible", "church", "yoga", "pilates",
                 "cough", "asthma", "inhaler", "peak flow", "baby", "toddler", "child",
                 "children", "kids", "kid", "school", "sleep", "insomnia"),
          bias=1),
] + SMALL_HABIT_ENTRIES

_PUTTING_A_CHARGE_UP = (
    "putting the rent up", "putting my rent up", "putting our rent up", "putting up the rent",
    "putting up my rent", "puts the rent up", "puts my rent up", "put the rent up",
    "put my rent up", "rent going up", "rent went up", "rent keeps going up",
    "putting the price up", "putting prices up", "putting up the price", "putting up prices",
    "puts the price up", "puts prices up", "put the price up", "put prices up",
    "putting the price of", "putting up the price of",
    "putting the tax up", "putting taxes up", "putting up taxes", "putting the council tax up",
    "putting the fares up", "putting fares up", "putting up fares", "putting the bills up",
    "putting up the bills", "putting the charges up", "putting the fees up",
    "putting the rates up", "putting the cost up", "putting costs up",
)

ENTRIES = EXTRA_ENTRIES + [

    entry("putting-things-off", (("procrastinat", "procrastinating", "putting off", "put off",
                                  "put things off", "put it off", "cant start", "can't start",
                                  "cannot start", "keep putting",
                                  "keep procrastinating", "keep putting off",
                                  "keep putting things off", "always putting things off",
                                  "procrastinate",
                                  "lazy at work", "lazy at my job", "lazy with work",
                                  "lazy at home", "lazy at the moment", "lazy lately",
                                  "so lazy", "am lazy", "im lazy", "feeling lazy",
                                  "no motivation at work", "no motivation at my job",
                                  "no motivation for work", "no motivation to work",
                                  "no motivation at home",
                                  "cant be bothered to start",
                                  "do nothing all day", "doing nothing all day",
                                  "get nothing done", "gets nothing done",
                                  "nothing gets done"),
                                 ("stop", "always", "constantly", "keep", "keeps", "everything",
                                  "anything", "stuck", "help", "how",
                                  "at work", "work", "my job", "job", "office", "shift", "desk",
                                  "at home", "chores",
                                  "housework", "uni", "school", "revising", "the gym",
                                  "putting it off", "kept putting it off", "keeps putting it off",
                                  "putting off this", "putting off that", "putting off going",
                                  "putting off making", "putting off ringing",
                                  "putting off calling", "putting off booking")),
          "Shrink the job until it is almost silly: name the very next physical action — open the "
          "letter, put the shoes by the door — and do only that one, for five minutes, with "
          "permission to do it badly. Putting things off is usually about the task feeling too big "
          "to begin, and it stops the moment you are in it. Decide tonight what tomorrow's first "
          "step is, so it is an instruction rather than a choice.",
          avoid=("study", "studying", "revise", "revising", "revision", "homework", "essay",
                 "exam", "exams", "gcse", "a-level", "mocks", "uni", "university", "college",
                 "school", "coursework", "dissertation", "thesis", "assignment", "deadline",
                 "project due", "has a project", "project about", "project on", "school project",
                 "poster about",
                 "put me down", "puts me down", "putting me down", "put down",
                 "husband", "wife", "partner", "boyfriend", "girlfriend", "fiance",
                 "fiancee", "son", "daughter", "child", "children", "teenager", "teen",
                 "flatmate", "housemate", "his share", "her share", "doesnt help", "doesn't help",
                 "work from home", "working from home", "wfh", "from home",
                 ) + _PUTTING_A_CHARGE_UP,
          guard=_the_writer_is_the_one_forgetting),

    entry("quit-vaping", (("vaping", "vape", "vapes", "vaper", "e cigarette", "e cigarettes",
                           "e cig", "elf bar", "nic salt"),
                          STOP),
          "Staying on the vape beats going back to cigarettes, so if it is the only thing keeping you "
          "off tobacco, the win is not to stop. To come off it: drop the nicotine strength a step "
          "every two weeks, keep it out of sight rather than in your hand, and set a date "
          "instead of drifting down. The hand-to-mouth habit outlasts the nicotine, so keep a straw "
          "or gum where the vape used to live. Feeling low or snappy for a week is withdrawal, and "
          "it passes.",
          avoid=("coil", "coils", "battery", "charger", "shop", "cheapest", "price", "flavour",
                 "flavor", "illegal", "law", "underage", "ban") + THIRD_PARTY + FEEL_BAD),

    entry("cut-down-drinking", (("drinking", "drink", "alcohol", "beer", "wine", "booze",
                                 "units", "pint", "pints", "vodka", "whisky", "gin"),
                                STOP + ("less", "reduce", "reducing", "too much", "every day",
                                        "every night", "how much is too much",
                                        "a night", "every evening", "a bottle a night",
                                        "a bottle every night", "a pint a day", "each night")),
          "Write down what you really drink for a fortnight - most people are surprised - then take "
          "three drink-free days a week as the first change, since days off are easier than smaller "
          "measures. Alternate each drink with a glass of water, keep nothing in the house on the "
          "days you are off it, and tell one person you are doing it. If you drink every day and "
          "shake or sweat when you stop, see a GP first: coming off alcohol suddenly can be "
          "dangerous.",
          avoid=("stain", "stains", "spill", "spilled", "spilt", "shirt", "sofa", "carpet",
                 "coffee", "tea", "water", "juice", "milk", "fizzy", "thirsty", "kebab",
                 "miss a", "miss the", "miss my", "missing a", "craving", "crave", "craves",
                 "alcohol free", "alcohol-free", "alcoholfree", "non alcoholic",
                 "non-alcoholic", "nonalcoholic", "zero alcohol", "booze free", "no alcohol",
                 "energy", "energy drink", "energy drinks", "red bull", "monster",
                 "relentless", "lucozade", "sports drink", "sports drinks", "protein shake",
                 "caffeine", "espresso", "cola", "coke",
                 "chocolate", "sauce", "recipe", "braised", "marinade",
                 "good for you", "good for me", "healthy", "healthier", "benefit", "benefits",
                 "hangover", "hungover", "drank too much", "last night", "so hard",
                 "dog", "dogs", "puppy", "pup", "pups", "cat", "cats", "kitten", "kittens",
                 "pet", "pets", "vet",
                 "rabbit", "rabbits", "bunny", "bunnies", "hamster", "hamsters", "guinea pig",
                 "guinea pigs", "gerbil", "gerbils", "rat", "rats", "hamster's", "chinchilla",
                 "ferret", "horse", "horses", "pony", "ponies", "kitten", "kittens",
                 "litter tray", "water bottle") + THIRD_PARTY + FEEL_BAD),

    entry("their-phone-habit",
          (("phone", "phones", "his phone", "her phone", "their phone", "screens", "screen",
            "scrolling", "scroll", "instagram", "tiktok", "facebook", "social media", "tablet",
            "ipad", "youtube"),
           ("always on", "on his phone", "on her phone", "on their phone", "addicted", "glued to",
            "too much", "never puts", "wont put", "won't put", "cant put", "can't put", "all day",
            "all the time", "ignores me", "stuck on")),
          "Say the thing you miss rather than a number of minutes, because a limit argued about in "
          "the moment is a row about the phone and a request is something they can answer: \"I "
          "miss talking at dinner\" works where \"you are on that thing again\" does not. Ask for "
          "one phone-free slot a day, a meal is the easy one, and put your own phone face down for "
          "it, because a rule that covers both of you holds and one imposed on them does not. If "
          "the scrolling is new, or they seem flat as well as glued to it, the phone is the "
          "symptom and a chat about how they are is the better move.",
          ask=("how", "what", "any", "help", "should", "can i", "says", "told me", "wont",
               "won't", "always", "spends", "is on", "on his", "on her", "on their", "glued",
               "addicted", "never puts", "ignores me"),
          avoid=("kid", "kids", "child", "children", "toddler", "son", "daughter", "teen",
                 "teens", "teenager", "year old", "homework", "school", "screen time",
                 "contract", "bill", "tariff", "price", "cost", "upgrade", "battery", "charge",
                 "cracked", "repair", "replace", "lost", "stolen", "storage"),
          guard=screens_are_somebody_elses),
    entry("forgotten-errand",
          (("keep forgetting", "keeps forgetting", "keep forgetting to", "keeps forgetting to",
            "always forgetting", "i forget to", "forget to", "forgetting to", "forgot to",
            "keep missing", "stop forgetting", "keep forgetting about", "remember to do",
            "remember to"),
           ("to", "ring", "call", "phone", "book", "pay", "renew", "post", "send", "email",
            "collect", "pick up", "buy", "order", "do", "make", "take", "go", "appointment",
            "appointments", "dentist", "doctor", "gp", "optician", "bill", "bills",
            "errand", "errands", "job", "jobs", "chore", "chores",
            "renewal", "form", "parcel", "parcels", "things", "stuff", "shopping", "return",
            "returns")),
          "Set the reminder the moment you think of it, while the phone is in your hand: \"remind "
          "me to ring the dentist at nine tomorrow\" into Siri or Google, or an alarm labelled with "
          "the job. Anything with a date - dentist, MOT, renewal, a birthday - goes in the calendar "
          "now, with an alert the day before and a yearly repeat for birthdays. A job that takes "
          "under two minutes is quicker done than remembered, so do it there and then; for the "
          "rest, leave the note where you will trip over it - the door keys, the kettle, the front "
          "door.",
          ask=("how", "stop", "keep", "keeps", "always", "help", "better", "tips", "tip",
               "remind", "reminder", "reminders", "system"),
          avoid=("tablet", "tablets", "medication", "medicine", "pill", "pills", "prescription",
                 "water", "drink", "drinking", "where i put", "where i left", "where ive put",
                 "keys", "glasses", "wallet", "phone number", "password", "pin", "name of",
                 "names", "word", "spelling", "what i read", "book i", "reading", "revise",
                 "revision", "study", "exam", "exams", "coursework", "someone", "somebody",
                 "my ex", "grief", "died", "passed away", "birthday card", "present",
                 "gift",
                 "birthday", "birthdays", "anniversary", "anniversaries",
                 "why", "what causes", "what makes", "is it normal"),
          guard=lambda reading: (_the_errand_is_the_speakers_own(reading)
                                 and not _someone_else_is_forgetting(reading)
                                 and not _my_own_memory_and_my_age(reading)))
]

ANSWERS = ("health",)
ENTRIES.append(entry(
    "a-worry-about-me",
    (("worrying about me", "worries about me", "worry about me", "worried about me",
      "anxious about me", "fussing about me", "fusses about me", "fussing over me",
      "stop worrying about me", "stop fussing about me",
      "my parents worry", "parents worrying", "my mum worries", "my mom worries",
      "my dad worries", "mum worrying", "mom worrying", "dad worrying", "they worry",
      "she worries", "he worries", "overprotective", "over protective", "smothering",
      "keeps checking on me", "keep checking on me", "always checking on me",
      "worries too much", "worry too much", "worrying too much",
      "worries about me all the time", "worrying about me all the time",
      "always worrying about me", "parents are overprotective", "overprotective parents",
      "controlling parents",
      "get my mum to stop worrying", "get my mom to stop worrying",
      "get my dad to stop worrying", "get my parents to stop worrying",
      "get her to stop worrying", "get him to stop worrying", "mum to stop worrying",
      "dad to stop worrying", "parents to stop worrying", "to stop worrying about me"),
     ("how do i", "how can i", "what can i do", "what do i do", "stop", "help", "deal with",
      "get them to", "make them stop", "reassure", "calm", "tell them", "explain to them",
      "get her to", "get him to", "handle", "why does", "why do", "are", "always", "all the time",
      "every day", "constantly", "too much", "so much", "keeps", "keep")),
    "Give them a fact rather than a reassurance: \"I'll text you when I'm on the train\" works "
    "where \"don't worry\" does not, because a worry needs something to hold. Ask what exactly "
    "they are afraid of, answer that one thing once, and then stop explaining - saying it a "
    "second and third time is what teaches them the worry is worth asking about.",
    ask=("how", "what", "can", "should", "do", "i", "my", "help", "stop", "deal", "get",
         "make", "reassure", "calm", "tell", "explain", "to", "why", "they", "she", "he"),
    avoid=("dog", "dogs", "cat", "cats", "puppy", "kitten", "pet", "pets", "horse", "rabbit",
           "baby", "toddler", "child", "children", "son", "daughter", "money", "rent", "bills",
           "debt", "doctor", "gp", "appointment", "headache", "symptom", "results", "exam",
           "exams", "revision", "interview", "wedding", "flight", "flying"),
    bias=3))
