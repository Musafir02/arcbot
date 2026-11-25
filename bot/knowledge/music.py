
from .lookup import entry

ANSWERS = ("entertainment", "creative")

STRINGS = ("guitar", "guitars", "ukulele", "uke", "violin", "violins", "fiddle", "cello",
           "double bass", "bass guitar", "banjo", "mandolin", "harp", "lute", "sitar",
           "bass")

KIT = STRINGS + ("piano", "pianos", "digital piano", "drum kit", "drum kits", "flute",
                 "saxophone", "sax", "trumpet", "clarinet", "accordion", "harmonica",
                 "recorder", "trombone", "tuba")

PLAYING = ("playing", "practising", "practicing", "practice", "rehearsing", "guitar",
           "guitars", "piano", "violin", "ukulele", "cello", "bass", "mandolin", "banjo",
           "chords", "strings", "fretboard", "fretting", "drum kit", "singing")

OVERHEARD = ("neighbours", "neighbors", "neighbour", "neighbor", "next door", "flat above",
             "people above", "landlord", "my mum", "my dad", "my family", "my partner",
             "everyone in the house")
MINE_HEARD = ("hear me", "hears me", "can hear me", "hear us", "hears us", "can hear us",
              "hear my", "hears my", "hear it when i", "hear me when i", "while i practise",
              "while i practice", "when i practise", "when i practice", "when i play",
              "about my playing", "about my practising", "about my practice", "about my music",
              "complain about me", "complaining about me", "complains about me",
              "moan about me", "moaning about me", "moans about me")

BROKEN = ("broke", "broken", "snapped", "snap", "snaps", "bust", "busted", "popped",
          "gone", "pinged", "off", "came off", "keeps breaking", "keeps snapping",
          "one string missing", "missing string", "missing a string", "a string short",
          "without a string")

NEW_STRINGS = ("change", "changing", "changed", "replace", "replacing", "new", "put on",
               "putting on", "how often", "when should i", "when do i", "every",
               "restring", "resting", "fit", "fitting",
               "sounds dull", "sounds dead", "sounds flat", "sounds rubbish", "no sustain",
               "lost its tone", "lost tone", "dull sound")

CLEANING = ("clean", "cleaning", "polish", "polishing", "dust", "dusty", "grime", "grimy",
            "sticky", "smelly", "smells", "sweat", "marks", "hygiene", "wipe", "disinfect")

QUIET = ("quieter", "quiet", "quietly", "loud", "headphones", "silent", "silence",
         "soundproof", "soundproofing",
         "hear me", "hear it", "hearing", "anyone hearing", "nobody hears", "no one hears",
         "complaining", "mute", "muted", "wake the house", "wake my family")

FINGERS = ("fingers", "fingertips", "finger tips", "fingertip", "sore", "hurts", "hurt",
           "painful", "blisters", "calluses", "callouses", "aching", "ache")


def _not_an_infection(understood):
    text = (understood.get("norm") or "") if isinstance(understood.get("norm"), str) else ""
    text = text or (understood.get("clean") or "")
    for word in ("red", "swollen", "swelling", "pus", "infection", "infected", "whitlow",
                 "abscess", "throbbing", "hot", "fever", "septic", "nail fold"):
        if word in text:
            return False
    return True


def _a_musical_line(understood):
    text = (understood.get("norm") or "") if isinstance(understood.get("norm"), str) else ""
    text = (text or "") + " " + (understood.get("clean") or "")
    for word in ("music", "practice", "practise", "practising", "practicing", "playing",
                 "play", "guitar", "piano", "violin", "drums", "singing", "sing", "band",
                 "instrument", "chords", "rehearsal", "rehearsing", "trumpet", "flute",
                 "saxophone", "cello", "ukulele", "bass", "clarinet"):
        if word in text.split() or (" " + word + " ") in (" " + text + " "):
            return True
    return False


_MUSIC_AROUND_STAFF = frozenset((
    "music", "musical", "stave", "clef", "clefs", "treble", "bass", "note", "notes", "dot",
    "dots", "line", "lines", "space", "spaces", "sheet", "score", "theory", "sight", "octave",
    "piano", "violin", "instrument", "sing", "song", "chord", "chords", "bar", "bars",
    "read", "reading", "learn", "learning",
))
_MUSIC_PHRASES = ("middle c", "note lengths", "sheet music", "sight read", "treble clef",
                  "bass clef")

_STAFF_MEANS_PEOPLE = (
    "my staff", "our staff", "two staff", "three staff", "four staff", "staff who",
    "staff member", "staff members", "members of staff", "staff are", "staff is", "staff not",
    "staff dont", "staff won't", "staff wont", "staff keep", "staff always", "staff never",
    "staff argue", "staff meeting", "staff rota", "staff turnover", "short staffed",
    "understaffed", "of staff",
)


_STAFF_TAILS = frozenset(("", "ed", "ing", "s", "er", "ers"))


def _staff_is_the_five_lines(understood):
    if not isinstance(understood, dict):
        return True
    clean = str(understood.get("clean") or understood.get("text") or "").lower()
    words = set(clean.replace("'", "").split())
    if not any(word.startswith("staff") and word[5:] in _STAFF_TAILS for word in words):
        return True
    if any(phrase in clean for phrase in _MUSIC_PHRASES):
        return True
    if any(phrase in clean for phrase in _STAFF_MEANS_PEOPLE):
        return False
    return bool(words & _MUSIC_AROUND_STAFF)


ENTRIES = [
    entry("instrument-string-broke", (STRINGS, BROKEN),
          ("That is a few pounds, not a new instrument: take the broken string off so the loose "
           "end does not scratch the top, then fit a new one - a single string or a full set is "
           "under a tenner from any music shop, and most will restring it for you for about ten "
           "pounds if you would rather not. Loosen it right off before you cut, and if the same "
           "string keeps going it is usually a sharp edge in the nut or the bridge, which a shop "
           "files smooth."),
          avoid=("car", "drawstring", "shoe", "shoes", "shoelace", "shoelaces", "bag", "hoodie",
                 "tracksuit", "curtain", "curtains", "neck", "headstock", "fretboard", "purse",
                 "scissors", "theatre", "gift", "present", "fish", "fishing", "sea", "lake",
                 "river", "pond", "loch", "speaker", "speakers", "sub", "subwoofer"),
          bias=1),
    entry("instrument-string-change", (STRINGS + ("my strings", "the strings", "these strings"),
                                      NEW_STRINGS),
          ("Dead strings are most of what makes a guitar sound dull. Change them every one to "
           "three months if you play often, or the moment they feel rough, look tarnished or stop "
           "holding tune. Fit them one at a time so the neck keeps its tension: thread the string, "
           "leave two or three windings round the post, tune up to pitch and pull each string "
           "gently away from the fretboard a few times, then tune again. Nylon strings take a few "
           "days to settle, so expect to retune the first three days."),
          avoid=("car", "drawstring", "shoe", "shoes", "shoelace", "shoelaces", "bag", "hoodie",
                 "curtain", "curtains", "purse", "scissors", "theatre", "gift", "present",
                 "bank", "insurance", "energy", "supplier", "fish", "fishing", "sea", "lake",
                 "river", "pond", "speaker", "speakers", "subwoofer",
                 "practice", "practise", "practising", "practicing", "rehearse", "rehearsing",
                 "practice pad"),
          bias=1),
    entry("instrument-clean", (KIT, CLEANING),
          ("Wipe the strings and the back of the neck with a dry microfibre cloth every time you "
           "put it down - the sweat and skin oil is what makes a neck sticky and kills strings. "
           "Once or twice a year, take the strings off a rosewood or ebony board, scrape the grime "
           "off with a plastic card, and put a few drops of lemon oil on it; a lacquered maple "
           "board only needs the dry cloth, and never use furniture polish on the body."),
          avoid=("car", "oven", "hob", "kitchen", "bathroom", "house", "room", "window",
                 "windows", "floor", "carpet", "fridge", "washing machine", "sofa", "gutter",
                 "damp", "mould", "mold", "tumble", "dryer", "wall", "ceiling", "smell",
                 "smells", "smelly"),
          bias=1),
    entry("instrument-play-quietly", (KIT + ("practice", "practise", "practising",
                                            "practicing", "playing music", "play music",
                                            "my instrument", "learning an instrument"), QUIET),
          ("For an electric, the whole fix is a headphone amp or an audio interface into your "
           "phone - a twenty pound plug-in amp is silent to everyone else. On an acoustic, stuff a "
           "cloth or a soundhole cover in the hole, play with a thin pick and a light touch, and "
           "put the instrument on a cushion in a small room rather than against a shared wall; a "
           "digital piano with headphones does the same for keys."),
          avoid=("television", "tv", "speaker", "speakers", "hi-fi", "hifi", "air conditioner",
                 "boiler", "fan", "extractor", "car", "engine", "motor", "kids", "children"),
          bias=1),
    entry("instrument-overheard", (OVERHEARD, MINE_HEARD),
          ("That is what headphones, a mute or a practice room are for, and most of it is cheaper "
           "than a row: a headphone amp for an electric guitar, a soundhole cover or a folded cloth "
           "in an acoustic, a practice mute for a violin or a brass instrument, and headphones on a "
           "digital piano. Pick the hours you would want quiet in yourself - not before nine and "
           "not after ten - and tell them once, cheerfully, that you play and when you stop."),
          guard=_a_musical_line, bias=1,
          avoid=("dog", "dogs", "barking", "tv", "television", "stereo", "hi-fi", "party",
                 "washing machine", "builders", "building work", "renovating", "children",
                 "toddler", "football", "car", "engine", "alarm", "council", "environmental")),
    entry("instrument-sore-fingers", (PLAYING, FINGERS),
          ("That is the callus building, and it passes: keep sessions to fifteen or twenty minutes "
           "and stop when they start to sting, rather than pushing through to blisters. Press just "
           "behind the fret with the lightest touch that makes a clean note, play with lighter "
           "strings (10s on an electric, extra-light on an acoustic) and have the action lowered "
           "by a shop if it is high - and take the day off if one is torn, because a broken "
           "blister sets you back a fortnight."),
          avoid=("wrist", "wrist pain", "carpal", "tingling", "numb", "pins and needles",
                 "arm", "elbow", "shoulder", "back", "neck", "typing", "keyboard at work",
                 "mouse", "tendonitis", "rsi"),
          guard=_not_an_infection, bias=2),
    entry("instrument-amp-noise", (("amp", "amplifier", "guitar amp", "combo", "valve amp"),
                                   ("buzz", "buzzing", "buzzes", "hum", "humming", "hums",
                                    "hiss", "hissing", "crackle", "crackling", "noise", "noisy",
                                    "rattle", "rattling")),
          ("Hiss with nothing plugged in is normal for a valve amp, and a buzz that stops when you "
           "touch the strings or turn down the guitar's volume is the room's wiring or a "
           "single-coil pickup, not a fault: stand further from the amp, turn your body, and keep "
           "a phone and a dimmer switch away from it. If it hums with a cable in and nothing else, "
           "swap the cable; if it crackles when you move the guitar lead, the jack is loose; if it "
           "buzzes only on one socket in the house, try another room before you blame the amp."),
          avoid=("car", "caravan", "fuse box", "boiler", "doorbell", "intercom", "buzzer",
                 "bee", "bees", "wasp", "fridge", "washing machine", "hearing aid", "ear",
                 "tinnitus", "speaker", "subwoofer", "hi-fi", "tv", "television", "phone"),
          bias=2),
    entry("instrument-pick", (("pick", "plectrum", "plectrums", "picks", "strumming", "strum",
                               "guitar pick", "picking hand"),
                              ("hold", "holding", "grip", "how do i hold", "thick", "thin",
                               "thickness", "size", "material", "lose", "losing", "drops",
                               "drop", "keep dropping", "my hand", "loose", "slipping", "slip",
                               "smoothly", "smooth", "evenly", "rhythm", "strum", "strumming",
                               "nylon", "tortex", "dunlop")),
          ("Hold it between the thumb and the side of the curled index finger, with just a few "
           "millimetres showing, and grip it as lightly as you can without it turning - most "
           "beginners squeeze and the pick fights back. A thin pick (0.5 to 0.6mm) is easier for "
           "strumming chords, a thicker one (1mm) for single notes, and if it keeps slipping, the "
           "ones with a textured or drilled grip are worth the extra pound. Strum from the wrist "
           "with the arm still, and let the pick pass across the strings at a slight angle rather "
           "than flat, which is what stops the catching and the dropping."),
          avoid=("nose", "spot", "spots", "pimple", "scab", "lock", "door", "car", "apple",
                 "berries", "strawberry", "blackberry", "lottery", "numbers", "football",
                 "fantasy", "bet", "betting", "choosy", "fussy", "pick up", "picking up"),
          bias=2),
    entry("instrument-get-faster", (PLAYING,
                                    ("faster", "speed", "quicker", "get fast", "speed up",
                                     "play fast", "shred", "alternate picking", "technique",
                                     "accuracy", "cleanly", "sloppy")),
          ("Speed is accuracy first: set a metronome or a drum loop well below the tempo you can "
           "just about manage, play the passage clean five times in a row, then add five beats a "
           "minute, and drop back the moment it gets sloppy - two weeks of that beats months of "
           "playing it fast and wrong. Keep the fretting fingers close to the strings, pick with a "
           "small movement from the wrist rather than the whole arm, and practise the hard two "
           "bars on their own instead of the whole song. Ten focused minutes a day is plenty; "
           "speed comes from the slow repetitions, not from trying harder."),
          avoid=("chord", "chords", "barre", "bar chord", "bar chords"), bias=3),

    entry("instrument-barre-chords", (("barre", "barre chord", "barre chords", "bar chord",
                                       "bar chords", "barring"),
                                      ("chord", "chords", "play", "ring", "buzz", "clear",
                                       "how do i", "learn", "hurt")),
          ("Roll the first finger slightly onto its bony outer edge rather than flat on the pad, "
           "keep the thumb low behind the neck and pull the elbow in towards your body - the "
           "pressure comes from the arm, not from squeezing. Start at the fifth fret where the "
           "strings are easier, get one clean barre there, then walk the same shape down a fret at "
           "a time; a guitar set up with high action will not let you barre cleanly, so that is the "
           "next thing to fix."),
          bias=2, avoid=("car", "bar", "pub", "restaurant", "drink", "cocktail", "salad")),
    entry("instrument-first-chords", (("chord", "chords", "chord shapes", "open chords"),
                                      ("learn", "learning", "first", "strum", "strumming",
                                       "change chords", "change between", "switch chords",
                                       "songs", "start", "beginner", "how do i", "play")),
          ("Learn four shapes first - G, C, D and E minor - because those four are most of the "
           "songs you already know, and practise moving between two of them rather than holding "
           "one well. Ten minutes a day: one minute of slow changes with a metronome or a steady "
           "count, then play a song with the same two chords in it, and add a third only when the "
           "change is clean."),
          bias=1, avoid=("barre", "bar chord", "bar chords")),
    entry("sing-better", (("sing", "singing", "voice", "vocals", "vocal", "pitchy"),
                          ("better", "improve", "in tune", "on pitch", "technique", "breath",
                           "breathing", "warm up", "warmup", "how do i", "tips", "practice",
                           "practise", "range", "high notes")),
          ("Sing along to something you can hear clearly and quietly - headphones at half volume - "
           "because most people cannot hear themselves and push too hard. Breathe low into the "
           "belly, keep the throat relaxed, warm up with lip trills or humming for two minutes, "
           "and record yourself on your phone once a week: the recording is the lesson. For range "
           "or a song that keeps going wrong, three or four lessons with a teacher do more than a "
           "year of videos."),
          avoid=("choir", "choir practice", "join a choir", "lessons", "lesson", "teacher",
                 "shaking", "shaky", "shake", "nervous", "nerves", "presentation", "speech",
                 "public speaking", "interview", "audience", "stage fright", "cracking",
                 "hoarse", "husky", "raspy", "voice going", "lost my voice",
                 "out of breath", "breathless", "wheeze", "wheezing", "asthma", "chest",
                 "dizzy", "faint", "cough",
                 "gig", "karaoke", "carol", "carols", "national anthem", "kids", "children",
                 "toddler", "baby", "nursery", "school", "happy birthday", "wedding",
                 "join", "joining", "group", "club", "class", "classes", "choir"),
          bias=2),
    entry("read-sheet-music", (("sheet music", "music theory", "read music", "reading music",
                                "sight read", "sight reading", "staff", "clef", "treble clef",
                                "bass clef", "music notes"),
                               ("learn", "reading", "read", "understand", "how do i", "start",
                                "beginner", "teach myself", "what are")),
          ("Start with the treble clef only: the five lines are E, G, B, D, F from the bottom up "
           "and the four spaces spell FACE, and ten minutes a day of naming notes off a page is "
           "how it sticks. Then the same for the bass clef (Good Boys Do Fine Always on the lines), "
           "then note lengths and rests; a beginner tutor book and a free app like Tenuto cover it, "
           "and playing each note on the instrument as you name it is the part that makes it real."),
          avoid=("essay", "exam", "revision", "revise", "study", "school", "homework", "child",
                 "reading to my", "bedtime story", "phonics", "dyslexia", "letter", "letters",
                 "book", "books", "novel", "read a book"),
          guard=_staff_is_the_five_lines,
          bias=2),
    entry("piano-keys-layout", (("piano", "piano keyboard", "keys on a piano",
                                 "keys of the piano", "keys on the piano"),
                                ("white keys", "black keys", "notes on", "which note",
                                 "layout", "the pattern", "middle c", "where is c", "find c",
                                 "which key")),
          ("The keys repeat a run of twelve, seven white and five black, and the black keys come "
           "in a group of two and then a group of three: the white key to the left of the pair of "
           "black ones is C, and the rest run D E F G A B up to the next C. So find any pair of "
           "black keys and the white key just left of them is C, one octave apart all the way up. "
           "Middle C is the C nearest the middle of the keyboard, and the tune you can pick out "
           "by ear - three blind mice, happy birthday - is a faster way to learn it than naming keys."),
          avoid=("spill", "spilt", "spilled", "drink", "coffee", "tea", "beer", "water",
                 "sticky", "sticking", "sticks", "jammed", "broken", "laptop", "computer",
                 "typing", "mechanical", "phone", "tablet", "wont type", "not working"),
          bias=2),
    entry("first-keyboard", (("piano", "keyboard", "digital piano", "electric piano"),
                             ("buy", "buying", "should i get", "should i buy", "worth it",
                              "cheap", "cheapest", "afford", "budget", "which", "recommend",
                              "what kind", "second hand", "secondhand", "rent", "renting",
                              "for a beginner", "for my kid", "for my child")),
          ("For a first piano, the thing that matters is weighted, full-size keys: a second-hand "
           "88-key digital piano from Yamaha, Roland or Casio is 200 to 350 pounds and is the "
           "cheapest thing that teaches real finger strength. A 61-key keyboard with plastic keys "
           "is fine for a month to see if you like it, but it will not teach you to play, so hire "
           "or borrow one first if the money is tight - shops rent them monthly."),
          avoid=("tune", "tuning", "broken", "not working", "repair", "stuck key", "car",
                 "computer", "laptop", "pc", "mac", "phone", "ipad", "typing", "wireless",
                 "bluetooth", "mechanical", "shortcut", "shortcuts", "work", "office",
                 "meeting", "game", "games", "controller"),
          bias=1),
]
