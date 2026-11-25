import re
import string

from .badnews import reads_as_someones_death
from ..memory.setback import pool as _setback_pool, reading as _setback

OTHERS = frozenset((
    "he", "she", "him", "her", "his", "hers", "they", "them", "their", "theirs",
    "mum", "mam", "mom", "mummy", "mummy", "dad", "daddy", "father", "mother", "parent",
    "son", "daughter", "child", "kid", "kids", "baby", "toddler", "teenager", "boy", "girl",
    "husband", "wife", "partner", "boyfriend", "girlfriend", "fiance", "fiancee",
    "nan", "nana", "gran", "granny", "grandma", "grandad", "grandpa", "grandparents",
    "brother", "sister", "sibling", "aunt", "uncle", "cousin", "nephew", "niece",
    "friend", "mate", "flatmate", "housemate", "neighbour", "neighbor", "colleague",
    "boss", "manager", "landlord", "landlady", "tenant", "carer", "nurse", "vet",
    "dog", "cat", "puppy", "kitten", "pet", "pup",
))

THE_END_OF_A_THING = r"""
      | (?:its|it's|mine|ours)\s+had\s+(?:it|its\s+day)
      | (?:mine|ours)\s+(?:has|have|had)\s+had\s+(?:it|its\s+day)
      | (?:my|our|the|this|that|these|those)\s+(?:[\w']+\s+){0,3}
          (?:has|have|had)\s+had\s+(?:it|its\s+day)
      | (?:my|our|the|this|that|these|those)\s+(?:[\w']+\s+){0,3}
          (?:is|are|was|were)\s+done\s+for
"""

A_THING_PACKED_UP = r"""
      | (?:mine|ours)\s+(?:has|have|had)?\s*(?:packed\s+(?:up|in)|(?:gave|given)\s+up)
      | (?:the|my|our|this|that|his|her|their|it|its)\s+(?:[\w']+\s+){0,3}
          (?:has|have|had)?\s*(?:packed\s+(?:up|in)|(?:gave|given)\s+up)
"""

THING_STATE = r"""
    (?:has|have|had|is|are|was|were)\s+
      (?:(?:gone|got|become|turned)\s+)?
      (?:all\s+|a\s+bit\s+|a\s+lot\s+|really\s+|very\s+|quite\s+|so\s+|completely\s+
         |totally\s+|properly\s+|now\s+)?
      (?:a\s+|an\s+)?
      (?:
          black|brown|green|rusty|mouldy|moldy|mildewed|lumpy|soggy|slimy|sticky|greasy
        | furry|furred|scaled|pitted|warped|brittle|cracked|frayed|threadbare|bubbled
        | blistered|peeling|discoloured|discolored|crusty
        | burnt|burned|scorched|seized|rusted|corroded|perished|split|snapped|melted|bent
        | stuck|jammed|solid|knackered|kaput|buggered|stiff|dropped|flat
        | yellow|patchy|faded|bald|rip(?![\s-]+off\b)
        | crack|hole|tear|dent|patch
      )
      (?:\s+(?:on|up|through|off|shut|together|solid|apart|open|down|in|out))?
  | burnt\s+on
  | blown\s+(?:down|off|out|over|away)
  | (?:hanging|fell|fallen|come|coming|pulled)\s+(?:off|away|loose|apart|down|open)
  | conked\s+(?:out|off)
"""

GROWING = frozenset("""
    leaves leaf grass lawn lawns plants plant tree trees hedge hedges shrub shrubs bush bushes
    fruit veg vegetables tomatoes tomato potatoes crops flowers flower garden allotment ivy
    moss weeds weed field fields meadow hedgerow
""".split())

THING_STATE_ONLY = re.compile(r"\b(?:" + THING_STATE + r")\b", re.X)

THING = re.compile(r"""
    \b(?:
        wont | won't | doesn'?t\s+work | isnt\s+working | isn'?t\s+working
      | not\s+(?:working|responding|turning\s+on|charging|draining|connecting|booting)
      | stopped\s+working | stopped\s+charging
      | broke | broken | broke\s+down | bust | faulty | on\s+the\s+blink | playing\s+up
      | leak(?:s|ing|ed)? | drain(?:s|ing)? | soaking | dripping | blocked | clogged | jammed | stuck
      | keeps?\s+(?:freezing|crashing|cutting|dropping|stopping|going\s+off|calling|
                    restarting|turning\s+off|coming\s+up|showing|flashing)
      | cutting\s+out | crashing | froze | frozen | freezes | collapses? | collapsed
      | makes?\s+a\s+noise | making\s+a\s+noise | noisy | rattl(?:es|ing|ed)
      | die(?:s|d)? | dead | flat\s+(?:tyre|battery) | slow | sluggish | overheats? | overheating
      | error | glitch(?:y|es)? | corrupt(?:ed)? | wont\s+connect | no\s+signal
      | needs?\s+(?:a\s+)?(?:fixing|servicing)
      | on\s+its\s+way\s+out
      | on\s+(?:its|his|her|their)\s+last\s+legs
      | clapped\s+out | seen\s+better\s+days | knackered
      | went\s+bang | blew\s+(?:a\s+)?fuse
""" + THE_END_OF_A_THING + A_THING_PACKED_UP + r"""
      | """ + THING_STATE + r"""
    )\b
""", re.X)

CANT_GET = re.compile(r"""
    \b(?:can'?t|cannot|can\s+not|couldn'?t|could\s+not|unable\s+to|not\s+able\s+to)
      (?:\s+seem\s+to)?
      \s+(?:get|getting|make|making|keep|keeping|stop|stopping)\b
      (?:\s+[\w']+){1,4}?      # the thing: "my washing machine", "the app", "this printer"
      \s+(?:to\s+(?:work|job|run|go|start|stop|spin|turn|open|close|load|boot|charge
                      |connect|pair|sync|print|scan|save|drain|heat|light|fire|play|update
                      |install|download|upload|respond|unlock|switch|move|boil|cook|rise
                      |freeze|cool|record|log\s?in)
          |working|going|started|running|charged|connected|opening|booting)
""", re.X)

BODY = re.compile(r"""
    \b(?:
        hurt(?:s|ing)? | ach(?:e|es|ing|y) | sore(?:ness)? | pain(?:s|ful)? | stiff(?:ness)?
      | swell(?:s|ing|ings|en)? | tender(?:ness)? | numb | itch(?:y|es|ing)? | throbbing
      | migraines? | headaches? | toothaches? | cough(?:ing)? | rashes?
      | cramp(?:s|ing)? | bleeding | bled | sprain(?:s|ed)? | bruis(?:e|es|ed)
      | stubbed | burnt | burned | infection
    )\b
""", re.X)

FIGURATIVE = re.compile(r"\b(?:pain(?:s|ful)?|sore(?:ness)?|stiff(?:ness)?)\b")
NUISANCE = re.compile(r"\b(?:my|our)\s+\w+(?:\s+\w+){0,2}\s+(?:is|are|was|were|'s)\s+"
                      r"(?:(?:a|real|right|such|quite|so|very|bit\s+of|proper|little)\s+){0,2}"
                      r"(?:pain|pains|painful|sore|stiff)\b")

BODY_PART = frozenset((
    "back", "knee", "knees", "shoulder", "shoulders", "ankle", "ankles", "wrist", "wrists",
    "neck", "hip", "hips", "leg", "legs", "arm", "arms", "foot", "feet", "toe", "toes",
    "tooth", "teeth", "gum", "gums", "ear", "ears", "eye", "eyes", "chest", "stomach",
    "belly", "throat", "head", "skin", "hand", "hands", "finger", "fingers", "jaw",
    "sinus", "sinuses", "shoulder blade", "heart",
    "elbow", "elbows", "forearm", "forearms", "thigh", "thighs", "calf", "calves",
    "shin", "shins", "heel", "heels", "rib", "ribs", "collarbone", "collarbones",
    "hamstring", "hamstrings", "groin", "cheek", "cheeks", "chin", "eyebrow", "eyebrows",
    "knuckle", "knuckles", "tailbone", "spine", "tonsils",
))

ACUTE = re.compile(r"""
    \b(?:
        burn(?:s|ed|t)? | scald(?:s|ed)? | swell(?:s|ing|ed)? | swellings?
      | throat | lips? | tongue | breath(?:e|es|ing|less)? | choking | choked
      | bleed(?:s|ing)? | bled | numb | tingling | vision | sight | blurred
      | fell | fallen | fall(?:s|ing)? | collapsed | collapse | unconscious | dizzy | fainted
      | cut(?:s)? | gash | wound | crushed | twisted | sting(?:s|ing)?
      | rash(?:es|y)? | pois(?:on|oned|oning) | overdose | pill(?:s)? | seizure | sezure
      | can'?t\s+see | cant\s+see | can'?t\s+move | cant\s+move | can'?t\s+breathe
    )\b
""", re.X)

FRACTURE = re.compile(r"\b(?:broken|fractures?|fractured)\b")

BREAKS = re.compile(r"\b(?:broke|broken|broke\s+down|breaks|breaking|bust|busted)\b")
BONE = frozenset((
    "rib", "ribs", "collarbone", "collar", "pelvis", "spine", "shin", "thigh", "heel",
    "elbow", "elbows", "bone", "bones", "shoulder", "jaw", "skull", "tailbone", "wrist",
    "ankle", "hip", "kneecap", "knuckle", "knuckles",
    "nose", "cheekbone", "face", "cheek", "chin", "tooth", "teeth", "eyebrow", "brow",
    "temple", "mouth", "lip",
))

NOT_A_THING = frozenset((
    "heart", "marriage", "relationship", "trust", "body", "voice", "sleep", "life",
    "family", "friendship", "confidence", "spirit", "faith", "childhood", "career",
    "mind", "soul", "home", "week", "year", "day",
    "job", "work", "business", "mood",
))

KEEPS_AT_IT = re.compile(r"\b(?:keeps?|kept)\s+([a-z]{3,}ing)\b")

KEEPS_FINE = frozenset((
    "working", "works", "going", "goes", "running", "runs", "coming", "comes", "growing",
    "improving", "doing", "does", "getting", "gets", "making", "makes", "trying", "tries",
    "taking", "takes", "giving", "gives", "helping", "happening", "arriving", "waiting",
    "sitting", "standing", "walking", "talking", "thinking", "looking", "feeling", "eating",
    "drinking", "sleeping", "learning", "playing", "wanting", "needing", "asking", "saying",
    "telling", "buying", "selling", "sending", "bringing", "paying", "saving", "spending",
    "cooking", "baking", "cleaning", "washing", "wearing", "reading", "writing", "watching",
    "listening", "smiling", "laughing", "crying", "shouting", "fighting", "arguing",
    "worrying", "wondering", "hoping", "practising", "practicing", "scrolling", "charging",
    "lasts", "lives", "matters", "counts", "means", "sounds", "seems", "moving", "noticing",
    "visiting", "changing",
))

KEEPS_NOT_A_THING = frozenset((
    "people", "person", "someone", "somebody", "anyone", "everyone", "nobody", "guy", "man",
    "woman", "bloke", "fella", "lad", "lass", "boy", "girl", "teen", "teenager", "kid", "ex",
    "exes", "coworker", "co-worker", "workmate", "colleague", "colleagues", "staff", "team",
    "crew", "teacher", "nurse", "doctor", "carer", "client", "customer", "supplier", "boss",
    "manager", "old", "year", "years", "puppy", "kitten", "rabbit", "hamster", "budgie",
    "parrot", "horse", "pony", "spaniel", "retriever", "poodle", "beagle", "collie",
    "labrador", "terrier", "chihuahua", "guinea", "ferret", "tortoise", "goldfish", "bird",
    "birds", "squirrel", "squirrels", "fox", "foxes", "mouse", "mice", "rat", "rats",
    "dentist", "optician", "vet", "vet's", "landlord", "plumber", "mechanic", "electrician",
    "builder", "cleaner", "tutor", "hairdresser", "barber", "receptionist", "postie",
))

KEEPS_NOT_THEIR_THING = frozenset((
    "shop", "shops", "store", "stores", "supermarket", "pub", "pubs", "bar", "cafe",
    "café", "restaurant", "takeaway", "chippy", "bank", "pool", "gym", "library", "hotel",
    "school", "nursery", "council", "hospital", "surgery", "clinic", "pharmacy", "chemist",
    "garage", "station", "bus", "buses", "train", "trains", "tram", "tube", "taxi",
    "delivery", "post", "airport", "airline", "office", "market", "mall", "centre",
))

KEEPS_THEIRS = frozenset(("my", "our", "the", "this"))

KEEPS_POSSESSIVE = frozenset(("my", "our"))

KEEPS_OF_A_HOUSE = frozenset((
    "fridge", "freezer", "fridge-freezer", "boiler", "kettle", "oven", "hob", "cooker", "microwave",
    "toaster", "dishwasher", "washer", "dryer", "tumble", "machine", "appliance", "fan", "pump",
    "radiator", "thermostat", "heater", "heating", "shower", "tap", "taps", "toilet", "sink",
    "drain", "drains", "pipe", "pipes", "plug", "socket", "switch", "fuse", "bulb", "light",
    "lights", "lamp", "alarm", "smoke", "detector", "door", "doors", "window", "windows", "lock",
    "locks", "handle", "hinge", "hinges", "flap", "damp", "roof", "gutter", "guttering", "fence",
    "gate", "shed", "decking", "drive", "garage", "hoover", "vacuum", "mower", "lawnmower",
    "strimmer", "wifi", "router", "broadband", "internet", "connection", "signal", "tv",
    "television", "remote", "phone", "mobile", "landline", "laptop", "computer", "pc", "tablet",
    "ipad", "printer", "keyboard", "mouse", "screen", "monitor", "charger", "battery", "car",
    "van", "bike", "bicycle", "scooter", "engine", "brakes", "brake", "clutch", "gears", "tyre",
    "tyres", "wheel", "wheels", "headlight", "indicator", "wiper", "wipers", "exhaust", "radiator",
    "mattress", "bed", "shower", "cooker", "hob", "freezer", "washer-dryer", "blind",
    "blinds", "curtain", "curtains", "shutter", "shutters", "clothes", "dryer",
    "doorbell", "bell", "buzzer", "intercom", "extractor", "immersion", "cistern", "valve",
    "tank", "timer", "thermostat", "sensor", "meter", "socket", "adaptor", "lead", "cable",
    "speaker", "radio", "console", "wifi", "hub", "box", "unit", "system", "board", "panel",
))

NOT_THE_THING = frozenset((
    "i", "we", "you", "he", "she", "they", "it", "there", "what", "which", "who",
    "and", "but", "so", "if", "when", "that", "this", "then", "also", "always",
    "do", "does", "did", "should", "would", "could", "can", "cant", "cannot", "will",
    "wont", "might", "may", "must", "to", "not", "never", "up", "one", "any", "much",
    "no", "how", "why", "still", "just", "only", "is", "are", "was", "were", "all",
))

ASKS_TO_CHOOSE = re.compile(r"""\b(?:should\s+i|shall\s+i|is\s+it\s+worth|is\s+it\s+better|
    would\s+it\s+be\s+better|which\s+(?:one\s+)?should\s+i|do\s+you\s+think\s+i\s+should|
    what\s+would\s+you\s+do|worth\s+(?:repairing|fixing|it)|new\s+one|replace\s+it|
    get\s+rid\s+of\s+it|throw\s+it\s+(?:out|away))\b""", re.X)

FLAT = re.compile(r"\b(?:is|are|was|were|has|have|had|went|goes|just|all|now|so|really|completely|"
                  r"totally|kind\s+of|sort\s+of)?\s*(?:gone|went|died|dead|faded|fading|vanished|"
                  r"disappeared|dried\s+up|evaporated|left\s+me)\b"
                  r"(?!\s+(?:up|down)\b)")
FLAT_SUBJECT = frozenset((
    "spark", "hope", "hopes", "motivation", "patience", "appetite", "confidence", "humour",
    "humor", "laughter", "laugh", "libido", "mojo", "passion", "interest", "enthusiasm",
    "inspiration", "creativity", "energy", "buzz", "joy",
    "romance", "intimacy", "trust", "friendship", "marriage", "bubbliness", "zest",
))


JOINING = frozenset((
    "is", "are", "was", "were", "be", "been", "being", "has", "have", "had", "keeps",
    "keep", "kept", "just", "now", "still", "again", "always", "suddenly", "totally",
    "completely", "really", "all", "so", "very", "a", "an", "the", "and", "but", "then",
    "on", "off", "up", "it", "its", "it's", "there", "here", "one", "two", "twice",
    "kind", "sort", "bit", "little", "lot",
    "feel", "feels", "felt", "seem", "seems", "looks", "sounds", "gets", "got",
))
NOT_OWNED = frozenset((
    "the", "a", "an", "this", "that", "these", "those", "his", "her", "its", "their",
    "your", "in", "on", "at", "for", "to", "with", "from", "of", "and", "but", "or",
    "then", "when", "if", "as", "than", "like",
))

DEATHWISH = re.compile(r"\b(?:want|wanted|wanting|going|gonna|wish|wished|rather)\s+(?:to\s+)?"
                       r"(?:die|dead)\b|\b(?:die|dye)\s+my\s+hair\b")

ODD_MARK = string.punctuation + "\u2019"
DEAD_AS_VERY_AFTER = frozenset((
    "quiet", "tired", "easy", "good", "bad", "cheap", "slow", "boring", "cheerful", "glad",
    "lucky", "proud", "keen", "jealous", "happy", "sure", "tricky", "hard", "funny", "rude",
    "straight", "wrong", "serious", "certain", "ahead", "silent", "knackered", "shattered",
    "comfy", "comfortable", "soft", "cosy", "cozy", "warm", "cold", "nice", "sweet", "pretty",
    "smooth", "strong", "fussy", "broke", "skint", "fun", "obvious", "scary", "gentle", "relaxed",
    "bright", "dark", "loud", "chuffed", "mint", "annoying", "embarrassing",
    "quick", "fast", "clean", "simple", "smart", "friendly", "heavy",
))
PLEA = re.compile(r"\b(?:tips?|advice|suggestions?|recommendations?|what\s+should\s+i|"
                  r"how\s+(?:do|can|should)\s+i|any\s+ideas?|help\s+me)\b")

MINE = re.compile(r"^(?:i\b|i'm\b|im\b|i've\b|ive\b|my\b|our\b)")

OWNER_END = ("'s", "s'", "’s", "s")


def someone_elses(words):
    for word in words:
        word = str(word)
        if word in OTHERS:
            return True
        for ending in OWNER_END:
            if word.endswith(ending) and len(word) > len(ending) + 2:
                if word[:-len(ending)] in OTHERS:
                    return True
    return False

OWNS = re.compile(r"\b(?:my|our|mine|ours|the|this|that|it|its|it's)\b")

FAULT_FILLERS = frozenset((
    "is", "are", "was", "were", "am", "be", "been", "being", "still", "just", "also", "again",
    "always", "never", "keeps", "keep", "kept", "now", "then", "so", "too", "very", "really",
    "totally", "completely", "half", "a", "an", "the", "of", "and", "but", "its", "it", "has",
    "have", "had", "hasnt", "hadnt", "isnt", "not", "no", "getting", "gone", "went", "bit",
    "little", "properly", "partly", "mostly", "sometimes", "today", "yesterday", "again",
))


def _the_fault_hangs_on(text):
    heads = set()
    for match in (list(THING.finditer(text)) + list(CANT_GET.finditer(text))
                  + list(FLAT.finditer(text))):
        before = re.findall(r"[a-z']+", text[:match.start()])
        for word in reversed(before):
            if word in FAULT_FILLERS:
                continue
            heads.add(word)
            break
    return frozenset(heads)

DURATION = re.compile(r"""
    \b(?:
        for\s+(?:about\s+|nearly\s+|over\s+|almost\s+)?(?:\w+\s+){0,2}
            (?:days?|nights?|weeks?|months?|years?)
      | since\s+(?:\w+\s+){0,3}(?:days?|weeks?|months?|years?|monday|tuesday|wednesday|
            thursday|friday|saturday|sunday|christmas|january|february|march|april|may|june|
            july|august|september|october|november|december)
      | going\s+on\s+(?:\w+\s+){0,2}(?:days?|weeks?|months?|years?)
      | (?:started|began)\s+(?:\w+\s+){0,2}(?:yesterday|today|last\s+week|last\s+night|
            this\s+morning|on\s+monday|a\s+(?:week|month|few\s+days)\s+ago|
            (?:\d+|two|three|four|five|six|seven|eight|nine|ten)\s+days\s+ago)
      | \b(?:two|three|four|five|six|seven|eight|nine|ten|twenty|thirty|a\s+few|several|many)
            \s+(?:days?|weeks?|months?|years?)
      | \b\d+\s*(?:days?|weeks?|months?|years?)
    )\b
""", re.X)

BROKEN = (
    "That's a pain. What's it doing exactly, and when did it start?",
    "Annoying. Is it every time, or only now and then?",
    "Right. What have you tried so far?",
    "That would bother me too. Tell me what it does and I'll work out the next step with you.",
    "Ugh, those are fiddly. How long has it been like that?",
)

BROKEN_TIME = tuple(line for line in BROKEN if "How long" not in line)

A_DECLINE = re.compile(r"""\b(?:
    on\s+its\s+way\s+out
  | on\s+(?:its|his|her|their)\s+last\s+legs
  | clapped\s+out | seen\s+better\s+days
""" + THE_END_OF_A_THING + A_THING_PACKED_UP + r"""
)\b""", re.X)

DECLINE = (
    "That's a pain. What's it doing exactly, and when did it start?",
    "Annoying. What's it doing when it goes wrong?",
    "That would bother me too. Tell me what it does and I'll work out the next step with you.",
    "Right. What is it doing that makes you think it is on the way out?",
)
STILL_FAILING = re.compile(r"\b(?:on\s+its\s+way\s+out"
                          r"|on\s+(?:its|his|her|their)\s+last\s+legs"
                          r"|clapped\s+out|seen\s+better\s+days)\b")
DECLINE_TIME = (
    "Annoying. What's it doing when it goes wrong?",
    "That would bother me too. Tell me what it does and I'll work out the next step with you.",
    "Right. What is it doing that makes you think it is on the way out?",
)


def _only_the_decline(text):
    match = A_DECLINE.search(text)
    if not match:
        return False
    rest = text[:match.start()] + " " + text[match.end():]
    return not (THING.search(rest) or CANT_GET.search(rest) or BODY.search(rest)
                or FLAT.search(rest))

SORE = (
    "That sounds wearing. Is it getting better, worse, or about the same?",
    "Does it come and go, or is it there all the time?",
    "Right. What have you tried for it so far?",
    "That's a nuisance to be carrying round. How long has it been like that?",
)

SORE_TIME = ("That's a nuisance to be carrying round. What's it like at its worst?",) \
    + tuple(line for line in SORE if "How long" not in line)

STRAIN = (
    "That sounds wearing. What's gone wrong, do you think?",
    "Right, that is a lot to carry. What is it like at the moment?",
    "That would weigh on me too. What has changed?",
    "Ugh, that is a hard one. How long has it been like that?",
    "Right. What would make the most difference, if it changed?",
)
STRAIN_TIME = tuple(line for line in STRAIN if "How long" not in line)


SORE_NEXT = (
    "And what makes it worse - moving about, sitting still, or nothing in particular?",
    "Is it the same all day, or worse at certain times?",
    "Has anything helped - a warm bath, a painkiller, or just resting it?",
)
BROKEN_NEXT = (
    "Does it do it every time, or only now and then?",
    "Has anything you tried made a difference?",
    "What's it doing when it goes wrong?",
)
STRAIN_NEXT = (
    "Is it one part of it, or the whole thing?",
    "Has anything helped, even a little?",
    "What would better look like, if it came?",
)

DETAIL = re.compile(r"""\b(?:
    sore | sorer | hurting | hurts? | ache | aches | aching | achy | stiff | stiffness
  | swollen | swelling | tender | throb\w* | sharp | burning | numb | tight | bruised
  | worse | worst | better | eased? | eases | easier | helped | helps | relief
)\b""", re.X)
TRIGGER = re.compile(r"""\b(?:
    when\s+i | whenever\s+i | if\s+i | after\s+i | since\s+i
  | only\s+when | only\s+if | when\s+it | whenever\s+it | if\s+it
  | in\s+the\s+(?:morning|morning|evening|evenings|night)
  | first\s+thing | all\s+day | overnight
  | every\s+time | each\s+time | all\s+the\s+time | now\s+and\s+(?:then|again)
  | sometimes | most\s+(?:days|mornings|nights) | lately
  | sitting | standing | walking | running | lifting | bending | lying | sleeping | driving
)\b""", re.X)


_NOT_A_STRAIN_DETAIL = re.compile(
    r"^(?:so |and |but |well |ok |okay )*(?:how|what|why|when|where|which|who|should|can|could|"
    r"would|will|is|are|do|does|did|shall)\b"
    r"|\b(?:broke|broken|died|dead|ill|hospital|accident|leaking|not working|stopped working)\b")


def answers_a_strain_question(clean, memory=None):
    if _shape_on_the_table(memory) != "strain":
        return False
    return _answers_a_strain_question(_flat(clean), memory)


_A_SENTENCE = re.compile(
    r"\b(?:am|is|are|was|were|be|been|being|has|have|had|do|does|did|can|could|will|would|shall|"
    r"should|may|might|must|i'm|im|i've|ive|i'd|we're|we've|he's|she's|there's|get|gets|got|go|"
    r"cant|cannot|can't|dont|don't|didnt|didn't|wont|won't|isnt|isn't|wasnt|wasn't|havent|"
    r"haven't|hasnt|hasn't|couldnt|couldn't|wouldnt|wouldn't|doesnt|doesn't|arent|aren't|aint|"
    r"goes|going|went|keep|keeps|kept|want|wants|need|needs|feel|feels|felt|think|thinks|seem|"
    r"seems|seemed|know|knows|make|makes|made|work|works|worked|start|starts|started|stop|stops|"
    r"stopped|try|tries|tried|lost|lose|loses|die|died|broke|broken|hurt|hurts)\b")
_A_HEDGE = frozenset(("no", "idea", "dont", "don't", "do", "not", "know", "sure", "dunno", "idk",
                      "nothing", "whatever", "meh", "maybe", "i", "nothing's", "nothings"))


def _answers_a_strain_question(text, memory=None):
    words = text.split()
    if len(words) < 2 or len(words) > 9 or "?" in text:
        return False
    if _NOT_A_STRAIN_DETAIL.search(text) or _A_SENTENCE.search(text):
        return False
    if all(word.strip(",.") in _A_HEDGE for word in words):
        return False
    if _a_card_answers(text) or _a_length_of_time(text, memory):
        return False
    return not reads_as_trouble(text)


_A_LENGTH_OF_TIME = re.compile(
    r"\b(?:\d+|a|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|a couple of|"
    r"a few|several)\s+(?:days?|weeks?|months?|years?)\b"
    r"|\b(?:days|weeks|months|years|ages)\b(?:\s+(?:now|too|already))*\W*$"
    r"|\bsince\s+(?:yesterday|this morning|last night|the weekend|christmas|the summer|"
    r"last \w+|monday|tuesday|wednesday|thursday|friday|saturday|sunday|january|february|"
    r"march|april|may|june|july|august|september|october|november|december)\b"
    r"|\bfor\s+(?:years|months|weeks|ages|a long time)\b"
    r"|\b(?:ages|a long time|all (?:week|month|year))\b")


def _a_length_of_time(text, memory=None):
    if not _A_LENGTH_OF_TIME.search(text):
        return False
    try:
        import copy as _copy
        from ..modules import chat
        said = chat.respond(text, _copy.deepcopy(memory) if isinstance(memory, dict) else {})
    except Exception:
        return False
    if not said:
        return False
    said = str(said).lower()
    pools = []
    for name in ("STANDING_REPLIES", "STANDING_FEELING_REPLIES"):
        buckets = getattr(chat, name, None)
        if isinstance(buckets, dict):
            for lines in buckets.values():
                pools.extend(str(line) for line in lines)
    return any(line.lower()[:60] in said for line in pools if line)


def _a_card_answers(text):
    try:
        from ..knowledge import lookup
    except Exception:
        return False
    try:
        found = lookup.find({"clean": text, "words": text.split()})
    except Exception:
        return False
    return found is not None


def _flat(line):
    return " ".join(str(line or "").lower().split())


def _said_already(lines, memory):
    said = []
    for turn in (memory.get("turns") if isinstance(memory, dict) else None) or ():
        if isinstance(turn, dict):
            said.append(_flat(turn.get("bot")))
    said = [line for line in said if line]
    if not said:
        return tuple(lines)
    fresh = tuple(line for line in lines if _flat(line) not in said)
    if fresh:
        return fresh
    last = said[-1]
    return tuple(line for line in lines if _flat(line) != last) or tuple(lines)


ALREADY_TRIED = re.compile(
    r"\b(?:i|we|ive|i've|weve|we've|hes|he's|shes|she's|they|they've)\s+"
    r"(?:already\s+|just\s+|even\s+|also\s+)?(?:\w+ly\s+)?(?:tried|did|had a go|gave it a go|"
    r"used|\w+ed)\b")


def pool(shape, clean, memory=None):
    text = " " + str(clean or "").lower() + " "
    if shape == "vague":
        return _said_already(_setback_pool(clean), memory)
    stated = bool(DURATION.search(text))
    if shape == "sore":
        lines = SORE_TIME if stated else SORE
    elif shape == "strain":
        lines = STRAIN_TIME if stated else STRAIN
    elif _only_the_decline(text):
        lines = DECLINE_TIME if stated else DECLINE
        if not STILL_FAILING.search(text):
            lines = tuple(line for line in lines if "on the way out" not in line)
    else:
        lines = BROKEN_TIME if stated else BROKEN
    if ALREADY_TRIED.search(text):
        lines = tuple(line for line in lines if "tried so far" not in line)
    return _said_already(lines, memory)


def _shape_on_the_table(memory):
    turns = (memory.get("turns") if isinstance(memory, dict) else None) or ()
    if not turns or not isinstance(turns[-1], dict):
        return None
    last = _flat(turns[-1].get("bot"))
    if not last:
        return None
    for shape, lines in (("sore", SORE + SORE_TIME), ("thing", BROKEN + BROKEN_TIME),
                         ("strain", STRAIN + STRAIN_TIME),
                         ("sore", SORE_NEXT), ("thing", BROKEN_NEXT),
                         ("strain", STRAIN_NEXT)):
        for line in lines:
            if _flat(line) in last:
                return shape
    return None


IT = re.compile(r"\b(?:it|its|it's|this|that|these|those)\b")
MINE_AGAIN = re.compile(r"\bmy\s+([a-z']+)")


def _points_at_it(text, memory):
    if IT.search(text):
        return True
    turns = (memory.get("turns") if isinstance(memory, dict) else None) or ()
    said = _flat(turns[-1].get("user")) if turns and isinstance(turns[-1], dict) else ""
    if not said:
        return True
    for noun in MINE_AGAIN.findall(text):
        if re.search(rf"\b{re.escape(noun)}\b", said):
            return True
    return False


def _shape_answered(memory):
    turns = (memory.get("turns") if isinstance(memory, dict) else None) or ()
    if len(turns) < 1 or not isinstance(turns[-1], dict):
        return None
    last = _flat(turns[-1].get("bot"))
    if not last or last.rstrip().endswith("?"):
        return None
    said = _flat(turns[-1].get("user"))
    if not said:
        return None
    return _shape(said)


WHAT_IT_DOES = re.compile(r"what\s+it\s+does|what's\s+it\s+doing|what\s+is\s+it\s+doing",
                            re.I)


def carried_on(clean, words=None, memory=None):
    shape = _shape_on_the_table(memory)
    fuzzy = False
    if not shape:
        shape = _shape_answered(memory)
        fuzzy = bool(shape)
    if not shape:
        return None
    text = _flat(clean)
    if not text or "?" in text:
        return None
    if words is None:
        words = set(re.findall(r"[a-z']+", text))
    words = set(words)
    answers_the_strain = shape == "strain" and not fuzzy and _answers_a_strain_question(text,
                                                                                        memory)
    if someone_elses(words) and not _a_fault_of_a_thing(text) and not answers_the_strain:
        return None
    padded = " " + text + " "
    says_what = answers_the_strain or bool(DETAIL.search(padded) or TRIGGER.search(padded))
    if not (says_what or DURATION.search(padded)):
        return None
    if fuzzy and not _points_at_it(padded, memory):
        return None
    nexts = {"sore": SORE_NEXT, "strain": STRAIN_NEXT}.get(shape, BROKEN_NEXT)
    lines = list(_said_already(nexts, memory))
    for line in pool(shape, clean, memory):
        if line in STRAIN or line in lines:
            continue
        lines.append(line)
    lines = [line for line in lines if not WHAT_IT_DOES.search(line)]
    return tuple(lines) or None


def reads_as_trouble(clean, words=None, repaired=""):
    text = _without_a_dead_that_only_means_very(_without_wanting_or_praise(
        " ".join(str(clean or "").lower().split())))
    if not text or "?" in text:
        return None
    if reads_as_someones_death(text):
        return None
    shape = _shape(text, words)
    if shape is None and repaired and repaired != text:
        shape = _shape(_without_a_dead_that_only_means_very(
            _without_wanting_or_praise(repaired)))
    return shape


WANTING_OR_PRAISE = re.compile(r"""
    \b(?:
        to\s+die\s+for
      | worth\s+dying\s+for
      | (?:would|could|might|will)\s+(?:die|kill)\s+for
      | (?:i|you|we|they|he|she)'?d\s+(?:die|kill)\s+for
      | (?:would|could|will)?\s*die[sd]?\s+on\s+(?:that|this|a|the)\s+hill
      | dy(?:ing|in)\s+(?:for|to)\b
    )
""", re.X)


def _without_wanting_or_praise(text):
    return WANTING_OR_PRAISE.sub(" ", str(text or ""))


def _without_a_dead_that_only_means_very(text):
    words = str(text or "").split()
    if "dead" not in words:
        return text
    kept = []
    for index, word in enumerate(words):
        following = words[index + 1] if index + 1 < len(words) else ""
        if word == "dead" and following.strip(ODD_MARK) in DEAD_AS_VERY_AFTER:
            continue
        kept.append(word)
    return " ".join(kept)


ANIMAL_MODIFIERS = frozenset((
    "cat", "cats", "dog", "dogs", "puppy", "puppies", "kitten", "kittens", "pup", "pups",
    "pet", "pets", "bird", "birds", "fish", "rabbit", "rabbits", "hamster", "hamsters",
    "chicken", "chickens", "horse", "horses", "tortoise", "parrot", "budgie", "ferret",
    "snake", "lizard", "mouse", "rat", "rats", "guinea", "pig", "pigs",
))

NOT_A_MODIFIER = frozenset((
    "is", "are", "was", "were", "am", "be", "been", "being", "has", "have", "had", "will",
    "wont", "cant", "cannot", "could", "would", "should", "might", "may", "must", "needs",
    "need", "got", "get", "gets", "getting", "went", "goes", "going", "keeps", "keep", "kept",
    "died", "dies", "die", "dead", "ill", "sick", "old", "young", "small", "big", "little",
    "and", "but", "so", "that", "who", "which", "doesnt", "didnt", "isnt", "wasnt", "to",
))


def _someone_is_the_subject(text):
    words = re.findall(r"[a-z']+", text)
    for index, word in enumerate(words):
        if not someone_elses((word,)):
            continue
        following = words[index + 1] if index + 1 < len(words) else ""
        if word in ANIMAL_MODIFIERS and following and following not in NOT_A_MODIFIER:
            continue
        return True
    return False


def _the_noun_before(text, at):
    words = re.findall(r"[a-z']+", " " + str(text or "")[:at])
    while words and words[-1] in JOINING:
        words.pop()
    return words[-1] if words else ""


def _a_fault_of_a_thing(text):
    padded = " " + text + " "
    return bool(THING.search(padded) and OWNS.search(padded)
                and not _someone_is_the_subject(text))


def _names_a_body_part(text):
    return bool(set(re.findall(r"[a-z']+", text)) & BODY_PART)


def _figurative_passes(text):
    if _names_a_body_part(text):
        return True
    return not NUISANCE.search(text)


def _shape(clean, words=None):
    text = " ".join(str(clean or "").lower().split())
    if not text or "?" in text:
        return None
    words = set(words) if words else set(re.findall(r"[a-z']+", text))
    mine = " " + text + " "
    a_state = THING_STATE_ONLY.search(mine)
    growing_state = bool(a_state and _the_noun_before(mine, a_state.start()) in GROWING)
    if someone_elses(words) and not _a_fault_of_a_thing(text):
        return None
    if PLEA.search(text) or DEATHWISH.search(text):
        return None
    if ACUTE.search(text) and not (a_state and not growing_state
                                   and not words & BODY_PART):
        return None
    if FRACTURE.search(text) and (words & (BODY_PART | BONE)):
        return None
    hung_on = _the_fault_hangs_on(text)
    if BREAKS.search(text) and ((words & NOT_A_THING) or (hung_on & NOT_A_THING)):
        return None
    own = bool(MINE.match(text))
    body_word = BODY.search(mine)
    if a_state and not growing_state and not words & BODY_PART:
        body_word = None
    ache = body_word or (words & BODY_PART
                                 and re.search(r"\b(?:dead|killing|kills|hurts?|banging|"
                                               r"thumping|pounding|splitting|had\s+it|"
                                               r"done\s+for)\b", mine))
    if own and ache:
        if FIGURATIVE.search(mine) and not _figurative_passes(text):
            return None
        return "sore"
    flat = FLAT.search(mine)
    if flat and (_the_fault_hangs_on(mine) & FLAT_SUBJECT):
        return "strain"
    if _setback(text) and not words & BODY_PART:
        return "vague"
    thing = THING.search(mine)
    if thing and OWNS.search(mine):
        hangs_on = _the_thing_it_hangs_on(mine, thing.start())
        if hangs_on in NOT_A_THING:
            return "strain"
        if hangs_on in BODY_PART and a_state and a_state.start() == thing.start():
            return "sore"
        if growing_state and a_state.start() == thing.start():
            return None
        if hangs_on in BODY_PART and A_DECLINE.search(mine[thing.start():]):
            return None
        return "thing"
    if CANT_GET.search(mine) and OWNS.search(mine) and not words & BODY_PART:
        return "thing"
    if _keeps_doing_it(mine) and not words & BODY_PART:
        return "thing"
    return None


def _keeps_doing_it(text):
    if ASKS_TO_CHOOSE.search(text):
        return False
    for match in KEEPS_AT_IT.finditer(text):
        doing = match.group(1)
        if doing in KEEPS_FINE:
            continue
        before = re.findall(r"[a-z']+", text[:match.start()])
        if not KEEPS_THEIRS & set(before[-3:]):
            continue
        head = ""
        for word in reversed(before):
            if word in FAULT_FILLERS or word in NOT_THE_THING:
                continue
            head = word
            break
        if not head or head in OTHERS or head in NOT_A_THING or head in BODY_PART:
            continue
        if head in NOT_THE_THING or head in KEEPS_NOT_A_THING:
            continue
        if head in KEEPS_NOT_THEIR_THING:
            continue
        if not OWNS.search(text):
            continue
        phrase = set(word for word in before
                     if word not in FAULT_FILLERS and word not in NOT_THE_THING)
        if not phrase & KEEPS_POSSESSIVE and not phrase & KEEPS_OF_A_HOUSE:
            continue
        return True
    return False


def _the_thing_it_hangs_on(text, at):
    words = re.findall(r"[a-z']+", text[:at])
    while words and words[-1] in JOINING:
        words.pop()
    if not words:
        return ""
    noun = words[-1]
    back = words[:-1]
    for _ in range(3):
        if not back:
            break
        if back[-1] in ("my", "our"):
            return noun
        if back[-1] in NOT_OWNED:
            return ""
        back.pop()
    return ""
