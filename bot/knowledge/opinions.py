import re

from .entertainment import the_book_is_a_reservation
from .lookup import asks_where_a_shop_answers, entry

ANSWERS = ("opinions",)

ASK_MARKERS = frozenset("""
    you your better rather which opinion pick recommend worth should would
    ok okay rude fine wrong right good bad
""".split())
OWN_OPINION = re.compile(
    r"\b(i think|i thought|i prefer|i'd prefer|id prefer|i believe|i reckon|i feel|"
    r"i'd say|id say|i say|in my opinion|personally|for me|to me)\b")
FIRST_PERSON = frozenset("i i'm im me my mine we we're were our ours us myself".split())
INTENT = ("want to", "wanted to", "wants to", "thinking of", "thinking about", "planning to",
          "plan to", "tempted to", "considering", "keen to", "hoping to", "too late",
          "at my age", "old age")
EXPLAINS = re.compile(r"^\s*(why|how come|what makes|what causes|explain|what's the reason)\b")


_A_PART = ("filter", "filters", "seal", "gasket", "drawer", "drum", "hose", "latch", "pump",
           "door", "lid", "tray", "paddle", "blade", "element", "shelf", "shelves", "basket",
           "spray arm", "cutting blade", "jug", "carafe", "pump filter")
_A_JOB = ("clean", "cleaning", "gunk", "blocked", "blocking", "smell", "smells", "mould",
          "mold", "broke", "broken", "torn", "split", "cracked", "leaking", "jam", "jammed",
          "will not", "wont", "won't", "fix", "replace", "stuck", "clogged", "descale",
          "scrub", "empty it", "get it out", "get the gunk out")
_BUYING = ("worth it", "worth buying", "should i buy", "is it worth", "buy a", "buying a")


def _worth_an_appliance(memory, understood):
    names = (("robot vacuum", "robot vacuums", "robot hoover"),
             ("dishwasher", "dishwashers"), ("tumble dryer", "tumble dryers", "dryer"),
             ("washing machine", "washing machines"), ("slow cooker", "slow cookers"),
             ("bread maker", "bread makers"), ("blender", "blenders"),
             ("food processor", "food processors"), ("pressure cooker", "pressure cookers"),
             ("vacuum", "vacuum cleaner"), ("hoover", "hoovers"), ("freezer", "freezers"))
    said = str((understood or {}).get("text") or (understood or {}).get("clean") or "").lower()
    if (any(part in said for part in _A_PART) and any(job in said for job in _A_JOB)
            and not any(buy in said for buy in _BUYING)):
        return ""
    if ("heat pump" in said and ("dryer" in said or "drier" in said)
            and any(buy in said for buy in _BUYING + ("any good", "good", "worth", "worth it",
                                                      "should i get", "should i buy", "get one"))):
        return None
    for other in ("hair dryer", "hair drier", "hairdryer", "nail dryer", "vacuum flask",
                  "flask", "thermos"):
        said = said.replace(other, " ")
    thing = None
    for forms in names:
        if any(form in said for form in forms):
            thing = forms[0]
            if forms[0] in ("vacuum", "hoover"):
                thing = "vacuum cleaner" if "vacuum" in said else "hoover"
            break
    article = "an" if thing and thing[0] in "aeiou" else "a"
    subject = f"{article} {thing}" if thing else "it"
    return (f"{subject.capitalize() if thing else 'It'} is worth it if you would use it three "
            "times a week or more and it saves a job you dislike; skip it otherwise, because it "
            "takes up a cupboard. Buy the cheap one first, because most of these are replaced by "
            "a better model you only learn you wanted after a year of using the first.")


_GADGET_TIPS = (
    (("slow cooker", "slow cookers", "crock pot", "crockpot"),
     "Brown the meat in a pan first and leave the lid on, because every lift of the lid is twenty "
     "minutes of heat gone: six to eight hours on low does what four on high cannot, and shin, "
     "shoulder and chicken thighs come out better than anything you would roast."),
    (("air fryer", "air fryers"),
     "Fill the basket no more than two-thirds and shake it halfway, because a crowded basket "
     "steams instead of crisping. Treat it as a fan oven twenty degrees cooler and a fifth less "
     "time: chips at 200C for eighteen minutes with one shake, chicken thighs at 190C for "
     "twenty-five."),
    (("bread maker", "bread makers", "bread machine", "bread machines"),
     "Use it for the dough and bake the loaf in the oven, because the machine's own bake gives a "
     "squat loaf with a pale top and a hard crust. Three-quarters of a teaspoon of yeast for a "
     "500g loaf is plenty when it proves slowly."),
    (("blender", "blenders", "smoothie maker", "smoothie makers", "nutribullet"),
     "Liquid in first, then the soft things, then anything frozen, and never more than half full "
     "of solids: start on the lowest speed and pulse, because full speed from cold throws the lot "
     "into the lid."),
    (("food processor", "food processors", "magimix"),
     "Pulse rather than hold, because pastry, mince and pesto are a series of short bursts and a "
     "long run turns them to paste. Add anything wet through the tube while it is running and it "
     "mixes in evenly instead of pooling at the bottom."),
    (("stand mixer", "stand mixers", "kitchenaid", "kenwood"),
     "Paddle for cakes, dough hook on the slowest speed for bread, whisk only for eggs and cream. "
     "Stop at the time in the recipe rather than watching the bowl, because an over-mixed cake "
     "comes out flat and tough."),
    (("pressure cooker", "pressure cookers", "instant pot"),
     "Never fill past two-thirds, and let meat drop from pressure on its own for ten minutes, "
     "because a quick release pulls the steam out of the middle and leaves it stringy. Soaked "
     "beans and stewing steak are where it beats the slow cooker on a weekday."),
    (("juicer", "juicers"),
     "Feed soft fruit in with the hard, and wrap leaves in a lettuce leaf so they go down instead "
     "of clogging the mesh. Rinse the basket straight away, before the pulp dries onto it."),
    (("coffee machine", "coffee machines", "bean to cup", "espresso machine", "sage barista"),
     "Weigh the beans rather than scooping - about 18g in for a double - and descale every couple "
     "of months, because scale is what drops the temperature and makes every cup taste flat."),
    (("sandwich toaster", "sandwich toasters", "toastie maker", "panini press"),
     "Butter the outside of the bread, not the inside, and keep the filling an inch from the "
     "edges: cheese in the hinge is what gets these thrown away."),
    (("rice cooker", "rice cookers"),
     "Rinse the rice until the water runs clear, then one part rice to one and a half parts "
     "water. Leave it on warm for an hour at most, because past that the bottom sets and it "
     "starts to smell."),
    (("ice cream maker", "ice cream makers"),
     "Chill the bowl overnight and the mix in the fridge as well, because a warm mix churns to "
     "slush. Take it out while it is still soft, since it sets hard once it is in the freezer."),
)

_VERDICT_ASK = ("think", "reckon", "opinion", "worth", "any good", "recommend", "like my",
                "regret", "good buy", "waste", "rate my", "should i keep")

_THE_VERDICT = ("The honest test is whether it earns its counter space: three uses a week and it "
                "was a good buy, once a month and it lives in a cupboard. Give it a month of "
                "proper use before you decide, and keep one recipe you like so it is not a "
                "project every time.")


def _gadget_view(memory, understood):
    said = " ".join(str(word) for word in ((understood or {}).get("words") or ())).lower()
    if not said:
        said = str((understood or {}).get("text") or "").lower()
    if any(ask in said for ask in _VERDICT_ASK):
        return _THE_VERDICT
    for forms, tip in _GADGET_TIPS:
        if any(form in said for form in forms):
            return tip
    return _THE_VERDICT


def _asked(reply):
    def answer(memory, understood):
        if not isinstance(understood, dict):
            return None
        words = set(understood.get("words") or ())
        text = str(understood.get("text") or "").lower()
        if EXPLAINS.match(text) and not words & {"you", "your", "yourself"}:
            return None
        def said():
            return reply(memory, understood) if callable(reply) else reply

        if understood.get("kind") == "question":
            return said()
        words = understood.get("words") or ()
        line = " ".join(understood.get("words") or ())
        full = str(understood.get("text") or "").lower()
        if any(marker in line for marker in INTENT) or any(
                marker in full for marker in INTENT):
            return said()
        if OWN_OPINION.search(full) and not set(words) & {"you", "your", "yourself", "yours"}:
            return None
        if set(words) & ASK_MARKERS:
            return said()
        if len(words) <= 6 and not set(words) & FIRST_PERSON:
            return said()
        return None
    return answer


CHOICE = frozenset((
    "or vs versus better prefer rather which either "
    "easier harder cheaper simpler quicker cleaner quieter calmer friendlier healthier "
    "more work less work more expensive less expensive").split())

TASTE = ("worth", "worth it", "buy", "buying", "get", "getting", "need", "recommend",
         "any good", "good", "think", "opinion", "reckon", "rate", "prefer", "better")


CHOICE_ASKS = ("should i", "shall i", "should we", "is it worth", "would i be better")

CHOICE_IN_WORDS = re.compile(r"(?:^|[^a-z])(?:or|vs|versus|rather than|instead of)(?:[^a-z]|$)")

CHOICE_ASK_WORDS = frozenset("should shall would which better rather worth recommend pick "
                             "choose prefer".split())


def _is_a_choice(understood):
    if set(understood.get("words") or ()) & CHOICE:
        return True
    text = " " + " ".join(understood.get("words") or ()).lower() + " "
    return any(phrase in text for phrase in CHOICE_ASKS)


def _names(understood, options):
    text = " ".join(understood.get("words") or ()) or str(understood.get("text") or "")
    text = " " + text.lower() + " "
    return any(option in text for option in options)


OWN_BUYING_ANSWER = ("new washing machine", "buying a washing machine", "washing machines",
                     "new dishwasher", "buying a dishwasher")

NOT_A_BUYING_ASK = ("which", "my new", "my old", "i bought", "i've bought", "i got", "i've got",
                    "we bought", "we got", "i own", "we own")
DISPOSAL = ("get rid of", "getting rid of", "got rid of", "throw away", "throwing away",
            "throw it out", "throwing it out", "throw out", "tip", "the tip", "recycling centre",
            "dump", "dumped", "dumping", "dispose", "disposal", "scrap", "scrapping", "scrapped",
            "recycle", "recycling", "bulky waste", "bulky collection", "collection", "collect it",
            "take it away", "taking it away", "unwanted", "no longer want", "dont want it",
            "don't want it", "getting a new one", "replace it")

A_JOB_ON_IT = ("how do i get", "how to get", "how do i clean", "how to clean", "how do i remove",
               "how to remove", "how do i clear", "how to clear", "how do i stop the",
               "hair out of", "lint out of", "fluff out of", "clean out", "cleaned out",
               "unblock", "clear the", "get the smell out", "get rid of the smell")
TRADES = ("plumber", "electrician", "gas safe", "have a go", "have a bash", "pay someone",
          "call someone", "call a man", "get someone in", "tradesman", "handyman", "diy",
          "myself", "or should i have a", "worth paying", "paying someone")

FAULT = ("wont", "won't", "isnt", "isn't", "doesnt", "doesn't", "cant", "can't", "cannot",
         "drain", "draining", "leak", "leaking", "leaked", "broken", "broke", "fault", "faulty",
         "error", "flashing", "not working", "stopped", "stop", "flood", "flooded",
         "water everywhere", "smell", "smells", "smelly", "repair", "repairs", "repairing",
         "fix", "fixing", "stuck", "noise", "noisy", "loud", "rattling", "grinding", "dead",
         "warranty", "guarantee",
         "not heating", "isnt heating", "wont heat", "no heat", "heat up", "not spinning",
         "wont spin", "not turning", "wont turn", "not drying", "wont dry", "takes ages",
         "still wet", "still damp", "engineer", "engineers", "call someone out")


def _either(id, a, b, reply, avoid=(), bias=0):
    def answer(memory, understood):
        if not isinstance(understood, dict):
            return None
        if not _is_a_choice(understood):
            return None
        if not (_names(understood, a) and _names(understood, b)):
            return None
        said = _asked(reply)(memory, understood)
        if said is not None:
            return said
        words = set(understood.get("words") or ())
        text = str(understood.get("text") or "").lower()
        if not re.search(CHOICE_IN_WORDS, text):
            return None
        if set(words) & FIRST_PERSON and not set(words) & CHOICE_ASK_WORDS:
            return None
        if OWN_OPINION.search(text) and not words & {"you", "your", "yourself", "yours"}:
            return None
        return reply(memory, understood) if callable(reply) else reply
    return entry(id, (a, b), answer, avoid=avoid, bias=bias + 1,
                 ask=tuple(sorted(CHOICE)) + CHOICE_ASKS)


def _already_on_instruments(memory):
    turns = memory.get("turns") if isinstance(memory, dict) else None
    if not isinstance(turns, list) or not turns:
        return False
    last = turns[-1] if isinstance(turns[-1], dict) else {}
    said = str(last.get("bot") or "").lower()
    return ("15–20 minutes" in said or "learning an instrument" in said
            or "four chords" in said)


TOO_LATE = ("too late", "too old", "am i too old", "at my age", "my age", "old age", "start at",
            "adult", "as an adult", "grown up", "40", "45", "50", "60", "70")

DRUMS = ("drum", "drums", "drum kit", "drumkit", "drumming", "percussion", "practice pad")

OTHER_INSTRUMENTS = ("guitar", "piano", "ukulele", "violin", "keyboard", "bass", "flute",
                     "sax", "saxophone", "cello", "banjo", "mandolin", "harmonica",
                     "trumpet", "clarinet", "choir", "singing", "practise singing")


def _on_drums(memory, understood):
    if _names(understood, DRUMS):
        return True
    if _names(understood, OTHER_INSTRUMENTS):
        return False
    turns = memory.get("turns") if isinstance(memory, dict) else None
    for turn in reversed(turns[-INSTRUMENT_LOOKBACK:] if isinstance(turns, list) else []):
        if not isinstance(turn, dict):
            continue
        if "practice pad" in str(turn.get("bot") or "").lower():
            return True
        said = str(turn.get("bot") or "").lower()
        if "basic beat" in said:
            return True
        if _names({"text": str(turn.get("user") or "")}, DRUMS):
            return True
        if _names({"text": str(turn.get("user") or "")}, OTHER_INSTRUMENTS):
            return False
    return False


HEALTH_ASK = ("healthier", "healthiest", "better for you", "better for me", "good for you",
              "caffeine", "healthy", "health")


def _tea_or_coffee(memory, understood):
    if isinstance(understood, dict) and _names(understood, HEALTH_ASK):
        return ("Neither is bad for you, and the health difference is small: tea has about half "
                "the caffeine of coffee, both count towards your fluids, and green tea and filter "
                "coffee have the most evidence behind them. What matters far more is how much "
                "sugar and milk goes in.")
    return ("Tea, most of the time: it's a better excuse to stop for five minutes. Coffee when "
            "you actually need to be awake in a hurry.")


INSTRUMENTS = {
    "guitar": {
        "names": ("guitar", "guitars", "ukulele", "uke", "banjo", "mandolin"),
        "hint": "four chords",
        "start": ("Start with four chords that fit a hundred songs — G, C, D and E minor — and the "
                  "strumming hand before the fretting one. Twenty minutes a day gets you a simple "
                  "song in two or three months, and six lessons at the start mean nobody has to "
                  "unlearn your hand position."),
        "practise": ("One song you actually like, in its easiest key: take the chord changes slowly, "
                     "in a loop, then put them in order. Speed comes last — clean and slow beats "
                     "fast and sloppy every time."),
        "how_long": ("With 15–20 minutes a day, four chords and a simple song come together in about "
                     "a month, and something recognisable with a few more chords in three to six "
                     "months."),
        "how_often": ("Fifteen to twenty minutes a day, five or six days a week, beats one long "
                      "session at the weekend: the chord changes are what need repeating, and your "
                      "fingertips need the odd rest day more than the extra minutes. Ten minutes is "
                      "enough on a busy day - the streak matters more than the length."),
    },
    "piano": {
        "names": ("piano", "pianos", "keyboard", "keyboards", "electric piano"),
        "hint": "right hand",
        "start": ("Start with the right hand alone on a song you already know, one note at a time, and the "
                  "left hand on two or three chords to go with it: hands separately for the first "
                  "few weeks is not cheating, it is how everyone does it. Twenty minutes a day, "
                  "and a teacher for the first month so your hand shape is right."),
        "practise": ("Right hand alone, slowly, on a tune you already know by ear — then the same "
                     "bars with the left hand, then both together much slower than either felt. "
                     "Five minutes of that daily beats an hour on Sunday."),
        "how_long": ("With 15–20 minutes a day, a simple tune with the right hand comes together in "
                     "a few weeks, and both hands in three to six months — faster than most people "
                     "expect, because the notes are laid out in front of you."),
        "how_often": ("Twenty minutes a day, five or six days a week, and shorter on a bad day "
                      "rather than skipping it: ten focused minutes of scales and one bar done "
                      "slowly is worth more than an hour on Sunday evening. Keep a day off."),
    },
    "violin": {
        "names": ("violin", "violins", "viola", "fiddle", "cello"),
        "hint": "open strings",
        "start": ("Start with the bow and the open strings: long, slow bow strokes on one string "
                  "are the first month, because a straight bow and a steady sound come before any "
                  "tune. Ten minutes a day, and a teacher from the first week — this is the "
                  "instrument where a bad habit is hardest to undo."),
        "practise": ("Open strings with a long, even bow, then one finger at a time on the D and A "
                     "strings: it sounds dreadful for a few weeks and that is the normal sound of "
                     "learning. A teacher's ear in the room is worth more here than on any other "
                     "instrument."),
        "how_long": ("Expect a few months of short tunes on one or two strings, and about a year "
                     "before something sounds like the tune you set out to play: the bow is the "
                     "slow part, not the fingers."),
        "how_often": ("Ten to fifteen minutes a day, every day if you can, because it is the bow "
                      "arm and the intonation that have to repeat - a week off costs you more on "
                      "the violin than on any other instrument. Stop while it still sounds good "
                      "rather than practising tired."),
    },
    "flute": {
        "names": ("flute", "flutes", "recorder", "piccolo"),
        "hint": "head joint",
        "start": ("Start with the mouth, not the tune: getting a clean sound out of the head joint "
                  "is the first week, then long notes on a few fingerings. Ten minutes a day, and "
                  "a teacher early, because the embouchure is the thing that is hard to fix "
                  "yourself."),
        "practise": ("Long notes on each fingering, from the easiest note upwards, listening for a "
                     "steady sound: five minutes of that a day before any tune. Then a short tune "
                     "in the easy keys, slowly."),
        "how_long": ("A clean sound takes a few weeks, a simple tune two or three months, and "
                     "something you would play for someone else six months to a year."),
        "how_often": ("Ten to fifteen minutes a day is plenty, most days: five of long notes and "
                      "the awkward fingering, then a short tune. Daily is what settles the "
                      "embouchure, and a day off now and then does no harm - a tired mouth is "
                      "where squeaks come from."),
    },
    "reed": {
        "names": ("clarinet", "sax", "saxophone", "trumpet", "oboe", "bassoon", "trombone",
                  "cornet", "horn", "french horn", "bugle"),
        "hint": "mouthpiece",
        "start": ("Start with the mouth: a clean, steady note on the mouthpiece alone is the first "
                  "week, and long notes on a few fingerings after that. Ten minutes a day, and a "
                  "teacher early, because the embouchure is the thing that is hard to fix "
                  "yourself."),
        "practise": ("Long notes, from the easiest note upwards, listening for a steady sound and a "
                     "clean start to each one: five minutes of that a day before any tune. Then a "
                     "short tune in the easy keys, slowly."),
        "how_long": ("A clean sound takes a few weeks, a simple tune two or three months, and "
                     "something you would play for someone else six months to a year."),
        "how_often": ("Ten to fifteen minutes a day, most days: long notes and a clean start to "
                      "each one first, then a tune. Daily repetition is what builds the "
                      "embouchure, and the mouth is what gives out first if you push it."),
    },
}

INSTRUMENT_GENERIC = {
    "start": ("Start with a teacher or a good app for the first month and ten or fifteen minutes a "
              "day on the basics: every instrument has its own awkward first fortnight, and one "
              "lesson early saves months of undoing. Pick one short piece you like as the target."),
    "practise": ("Whatever is awkward on it — the first clean note, the hand position, the "
                 "breathing — ten minutes a day, then a short piece slowly. Speed comes last."),
    "how_long": ("With 15–20 minutes a day, a simple tune is usually a few months and something "
                 "recognisable six months to a year, depending on the instrument."),
    "how_often": ("Short and often: ten to twenty minutes a day, most days of the week, beats one "
                  "long session at the weekend. Whatever is awkward in it gets the first five "
                  "minutes, and stopping while it is still going well is what keeps you coming "
                  "back to it."),
}


def _named_instrument(understood):
    for key, table in INSTRUMENTS.items():
        if _names(understood, table["names"]):
            return table
    return None


def _instrument_table(memory, understood):
    named = _named_instrument(understood)
    if named is not None:
        return named
    if _names(understood, OTHER_INSTRUMENTS):
        return INSTRUMENT_GENERIC
    turns = memory.get("turns") if isinstance(memory, dict) else None
    for turn in reversed(turns[-INSTRUMENT_LOOKBACK:] if isinstance(turns, list) else []):
        if not isinstance(turn, dict):
            continue
        said = str(turn.get("bot") or "").lower()
        for table in INSTRUMENTS.values():
            if table["hint"] in said:
                return table
        asked = str(turn.get("user") or "")
        if asked:
            for table in INSTRUMENTS.values():
                if _names({"text": asked}, table["names"]):
                    return table
    return INSTRUMENT_GENERIC


INSTRUMENT_WORDS = DRUMS + OTHER_INSTRUMENTS + tuple(
    name for table in INSTRUMENTS.values() for name in table["names"])
INSTRUMENT_LOOKBACK = 6


def _an_instrument_is_in_play(memory, understood):
    if _names(understood, INSTRUMENT_WORDS):
        return True
    turns = memory.get("turns") if isinstance(memory, dict) else None
    if not isinstance(turns, list):
        return False
    said = " "
    for turn in turns[-INSTRUMENT_LOOKBACK:]:
        if isinstance(turn, dict):
            said += str(turn.get("user") or "") + " " + str(turn.get("bot") or "") + " "
    said = said.lower()
    return any(word in said for word in INSTRUMENT_WORDS)


def _practise_first(memory, understood):
    if _on_drums(memory, understood):
        return ("Single strokes first, slow and even, ten minutes a day on a practice pad or a "
                "cushion: full strokes up to about a foot, then back down. Get that steady, then "
                "a basic beat — hi-hat on the eighths, snare on two and four, kick on one and "
                "three — and play along to a song you like. Speed comes last.")
    table = _instrument_table(memory, understood)
    if table is INSTRUMENT_GENERIC and not _an_instrument_is_in_play(memory, understood):
        return None
    return table["practise"]


def _drums_start(too_late):
    first = ("Not too late at all. " if too_late else "")
    return (first + "Ten minutes a day on a practice pad gets you a steady basic beat in about "
            "six weeks: single strokes slow and even, then hi-hat on the eighths, snare on two "
            "and four, kick on one and three. Play along to songs you like before you buy a kit, "
            "and take one lesson at the start so your grip is right — a pad, or a cushion and a "
            "pair of sticks, is enough to begin.")


def _start_instrument(memory, understood):
    if _on_drums(memory, understood):
        if _already_on_instruments(memory):
            return ("Then start this week: pad and sticks, ten minutes a day, one lesson at the "
                    "start, and one song you like to play along to. Speed comes last — slow and "
                    "even beats fast and ragged every time.")
        return _drums_start(_names(understood, TOO_LATE))
    table = _instrument_table(memory, understood)
    start = table["start"]
    if _already_on_instruments(memory) or not _names(understood, TOO_LATE):
        return start[0].upper() + start[1:]
    return ("Not too late at all: adults pick up the theory faster than children, they just need "
            "shorter and more regular practice. " + start[0].upper() + start[1:])


def _how_long_song(memory, understood):
    if _on_drums(memory, understood):
        return ("About six weeks of ten minutes a day for a steady basic beat, and three or four "
                "months before it holds together with a song at full speed. Play along to songs you "
                "like before you buy a kit.")
    return _instrument_table(memory, understood)["how_long"]


def _how_often_at_it(memory, understood):
    if _on_drums(memory, understood):
        return ("Ten minutes a day, five or six days a week, on a practice pad: single strokes "
                "slow and even first, then the basic beat played along to a song. The hands want "
                "the day off more than they want the extra twenty minutes.")
    table = _instrument_table(memory, understood)
    if table is INSTRUMENT_GENERIC and not _an_instrument_is_in_play(memory, understood):
        return INSTRUMENT_GENERIC["how_often"]
    return table["how_often"]


CANT_DECIDE = ("cant decide", "can't decide", "cannot decide", "undecided", "help me decide",
               "which should i", "what would you pick", "dont know which", "don't know which",
               "no idea which")


def _best_season(memory, understood):
    taste = ("Late spring for me: long evenings, everything green, and not hot enough to make "
             "excuses.")
    if _names(understood, CANT_DECIDE):
        return (taste + " Since you cannot settle on one, pick by what you would do in it: "
                        "autumn for walking, summer for eating outside, winter for staying in.")
    return taste


OUT_ALL_DAY = ("out all day", "out at work", "at work all day", "work all day", "out for work",
               "away all day", "long hours", "night shifts", "night shift", "travel for work",
               "always out", "rarely home", "small flat", "no garden", "in a flat", "renting",
               "landlord", "allergic", "allergy", "allergies")


CAT_WINS = ("easier", "easy", "less work", "less effort", "less hassle", "independent",
            "quiet", "quieter", "silent", "noise", "noisy", "noisier", "loud", "louder",
            "clean", "cleaner", "tidy", "smaller", "smell", "smells", "smelly",
            "low maintenance", "self sufficient")
DOG_WINS = ("affectionate", "loving", "loyal", "friendly", "playful", "fun", "company",
            "companionship", "clingy", "cuddly", "cuddles", "trainable", "obedient",
            "protective", "energetic", "good with kids", "good with children", "interactive")
TRAIN_WORDS = ("train", "trains", "trained", "training", "obedience", "obedient", "commands",
               "tricks")
TRAIN_COMPARE = (
    "A dog, on that one: dogs work for food and praise and will sit, stay and come in a few "
    "weeks, where a cat learns a few tricks on its own terms and will not be told. If training "
    "the animal is part of the fun for you, get the dog.")

CAT_ON_A_DIMENSION = (
    "A cat, on that one: it sleeps most of the day, does not bark at the postman and costs about "
    "£700 to £1,000 a year once insurance and a vet fund are in, where a dog is £1,500 and up "
    "before any vet bill. Pick the cat only because you want a cat, though, not just because it "
    "is the cheaper one.")
DOG_ON_A_DIMENSION = (
    "Dogs, by a whisker: daft, straightforward and pleased to see you, and they show it plainly - "
    "a dog greets you at the door where a cat may not. The trade is the walk every morning and "
    "£1,500 a year before any vet bill, and an adult rescue is far easier than a puppy.")


def _cats_or_dogs(memory, understood):
    if _names(understood, OUT_ALL_DAY):
        return ("A cat, if you're out all day: it sleeps through your shift and does not need a "
                "walk at seven in the morning. Get an adult cat rather than a kitten, and two if "
                "you are away a lot, so they have company.")
    if _names(understood, TRAIN_WORDS):
        return TRAIN_COMPARE
    if _names(understood, CAT_WINS):
        return CAT_ON_A_DIMENSION
    if _names(understood, DOG_WINS):
        return DOG_ON_A_DIMENSION
    return ("Dogs, by a whisker: daft, straightforward and pleased to see you. A cat is the kinder "
            "choice if you're out all day, though.")

DOG_TRADE = (
    "Want one only if the person who wants it is also the one who will walk it at seven on a wet "
    "Tuesday for the next twelve years. A dog costs £1,500 to £2,000 a year before any vet bill "
    "and needs someone home at lunchtime or a walker; an adult rescue is far easier than a "
    "puppy. If that sounds fine rather than like a sacrifice, get one.")
RABBIT_TRADE = (
    "A rabbit is an eight to ten year commitment and not a hutch pet: it needs a run it can stand "
    "up and stretch in, hay every day, another rabbit for company, and a vet who treats rabbits, "
    "because they hide illness until they are very ill. The daily work is the cleaning out and "
    "the company, and a rabbit kept alone in a small hutch is a miserable animal. A child can "
    "enjoy a rabbit but cannot be the one who cleans it out or notices it has stopped eating, so "
    "that job is an adult's. Get one because you want a rabbit for that long.")
GUINEA_PIG_TRADE = (
    "A guinea pig lives five to seven years and should never be kept alone - two of them, with a "
    "hutch and a run, hay all day because their teeth grow constantly, and vegetables with "
    "vitamin C in them because they cannot make their own. They are the friendliest of the small "
    "pets if they are handled from the start, and the daily work is hay, water and cleaning out.")
HAMSTER_TRADE = (
    "A hamster lives two to three years, sleeps through your day and is awake in the evening, so "
    "it is a pet to watch and handle gently rather than carry about. It wants the biggest cage "
    "you can give it with deep bedding to dig in, a wheel that does not bend its back, and a "
    "clean-out every week or so. Cheap to buy, not cheap to set up, and not a pet for a child on "
    "their own.")
CAT_TRADE = (
    "A cat costs about £700 to £1,000 a year once insurance and a vet fund are in, and unlike a "
    "dog it does not need you home at lunchtime: an adult cat sleeps through a working day, which "
    "is why people who cannot have a dog often do well with a cat. Get an adult rather than a "
    "kitten if you are out, two if the house is empty all day, a litter tray each plus one, and "
    "settle the landlord and who looks after it when you go away before you fall for one.")
CAT_WORDS = ("cat", "cats", "kitten", "kittens")
CAT_EQUIPMENT = ("flap", "litter", "tray", "trays", "scratching", "tree", "carrier",
                 "food", "foods", "treat", "treats", "toy", "toys", "brush", "claws",
                 "collar", "microchip", "harness", "bed", "bowl", "bowls", "catnip")
MOVE_TRADE = (
    "A move is decided by what you cannot change later: the commute, the noise, the light, and "
    "what you can walk to. Write the one thing each place gives you that the other cannot, then "
    "take the one you would miss on a bad day rather than the one that looks better on a good "
    "one. Move when the reason is still there in February.")
CAR_TRADE = (
    "A car is decided by the trips you actually make, not the ones you imagine: mostly short "
    "local miles with charging at home, electric; a long motorway run every month, petrol or a "
    "hybrid. Put insurance, tax and a service into the first-year budget, then only look at cars "
    "under that. The reliable boring one beats the fun one you cannot afford to fix.")
COURSE_TRADE = (
    "Pick the course by where you want to be at the end of it: a job, a licence, or the habit of "
    "studying. Ask two people who finished it what they do now, and count the hours a week it "
    "really takes. If the point is interest rather than a qualification, a short evening course "
    "tells you whether you like it before you pay for three years.")
QUALIFIED = ("which", "what model", "what kind", "what sort", "what breed", "what size",
             "how much", "how big", "how old", "how long", "used", "second hand", "secondhand",
             "lead", "leads", "harness", "breed", "breeds", "price", "prices", "cost", "cheap",
             "cheapest", "best", "insurance", "tax", "mot", "vet", "food", "train", "training",
             "name", "names", "age", "size",
             "survey", "surveys", "surveyor", "surveyors", "valuation", "snagging",
             "dealer", "dealership", "auction", "private seller")

TWO_WAYS = (("buy", "buying", "bought", "purchase", "purchasing", "mortgage", "owner"),
            ("rent", "renting", "rented", "rents", "tenant", "lease", "leasing"))

DECISION_SUBJECTS = (
    (("dog", "dogs", "puppy", "puppies", "rescue dog"), DOG_TRADE),
    (("rabbit", "rabbits", "bunny"), RABBIT_TRADE),
    (("guinea pig", "guinea pigs", "guinea-pig", "cavy"), GUINEA_PIG_TRADE),
    (("hamster", "hamsters", "gerbil", "gerbils", "degus", "chinchilla", "chinchillas"),
     HAMSTER_TRADE),
    (("flat", "flats", "house", "houses", "moving house", "move house", "moving in together",
      "rent", "renting", "landlord", "area", "neighbourhood", "commute"), MOVE_TRADE),
    (("car", "cars", "van", "second car"), CAR_TRADE),
    (("course", "courses", "degree", "degrees", "masters", "college", "university", "uni",
      "apprenticeship", "night class"), COURSE_TRADE),
)

STUCK_SHAPES = ("cant decide", "can't decide", "cannot decide", "cant choose", "can't choose",
                "torn between", "not sure which", "not sure whether", "not sure if", "unsure which",
                "unsure whether", "going back and forth", "back and forth", "two minds",
                "on the fence", "help me decide", "decide between", "deciding between",
                "should we get", "should i get", "should we buy", "should i buy",
                "thinking of getting", "thinking about getting", "thinking of moving",
                "thinking about moving", "thinking of buying", "whether to",
                "thinking of doing", "thinking about doing", "thinking of studying",
                "thinking about studying", "thinking of going back",
                "worth getting", "worth having")

DECIDE_WORDS = ("between", "whether", "torn", "unsure", "decide", "deciding", "decision",
                "choose", "choice", "option", "options", "stuck")

MADE_UP = re.compile(r"\b(?:i|we|they|she|he)\s+(?:have\s+|had\s+)?(?:decided|chose|picked|"
                     r"went with|bought|got|ordered|took)\b")


def _says_one_of(text, options):
    return any(re.search(r"\b" + re.escape(option) + r"\b", text) for option in options)


A_NEW_ONE = re.compile(
    r"\b(?:new|another|bigger|smaller|different|better|second|cheaper)\s+one\b"
    r"|\bone\s+instead\b|\bone\s+of\s+(?:those|them)\b", re.IGNORECASE)

_WHAT_TO_BUY = re.compile(
    r"\bwhat (?:do|should|shall|will|would) (?:i|we) (?:need|buy|get)\b"
    r"|\bwhat (?:do|should|shall) (?:i|we) (?:need|buy|get) (?:to|for)\b"
    r"|\b(?:need|needs) to (?:buy|get)\b|\bshopping list\b|\bchecklist\b"
    r"|\bwhat to (?:buy|get)\b|\bwhich (?:kit|supplies)\b", re.IGNORECASE)

_TWO_OF_THEM = re.compile(
    r"\btwo (?:cats|kittens)\b|\bsecond (?:cat|kitten)\b|\bpair of (?:cats|kittens)\b",
    re.IGNORECASE)


CAT_VERDICT_SHAPES = ("good idea", "worth it", "sensible", "wise", "a mistake",
                      "right for me", "right for us", "suit me", "suit us")

_ANOTHER_CATS_QUESTION = re.compile(
    r"\b(?:baby|babies|toddler|toddlers|child|children|kid|kids|newborn|pram|"
    r"flats?|rent|rents|rented|renting|landlord|rescue|rescued|"
    r"garden|outdoor|indoors?|dog|dogs|puppy|puppies|"
    r"cost|costs|price|prices|afford|how much)\b", re.IGNORECASE)


def _not_another_cats_question(understood):
    if not isinstance(understood, dict):
        return False
    said = understood.get("text") or understood.get("clean") or ""
    if not said:
        said = " ".join(understood.get("words") or ())
    return not _ANOTHER_CATS_QUESTION.search(str(said))


def _deciding(memory, understood):
    if not isinstance(understood, dict):
        return None
    text = " ".join(understood.get("words") or ()) or str(understood.get("text") or "")
    text = " " + " ".join(str(text).lower().split()) + " "
    if A_NEW_ONE.search(text):
        return None
    if _WHAT_TO_BUY.search(text) and _says_one_of(text, CAT_WORDS):
        return None
    if _TWO_OF_THEM.search(text) and not re.search(r"\bbetween\b", text):
        return None
    if MADE_UP.search(text) and not re.search(r"\b(cant|can't|cannot|whether|which|torn|unsure)\b",
                                              text):
        return None
    if _says_one_of(text, ("cat", "cats", "kitten", "kittens")) and _says_one_of(
            text, ("dog", "dogs", "puppy", "puppies")):
        return _cats_or_dogs(memory, understood)
    if _says_one_of(text, TWO_WAYS[0]) and _says_one_of(text, TWO_WAYS[1]):
        return None
    if _says_one_of(text, CAT_WORDS):
        if _says_one_of(text, CAT_EQUIPMENT):
            return None
        return CAT_TRADE
    if _says_one_of(text, QUALIFIED):
        return None
    for options, trade in DECISION_SUBJECTS:
        if _says_one_of(text, options):
            return trade
    return None

_NORMAL_ASK = ("is it normal", "is that normal", "is this normal", "isnt normal", "isn't normal",
               "not normal", "normal to", "normal for", "is it weird", "is that weird",
               "is this weird", "weird to", "weird that", "weird if", "am i weird",
               "am i strange", "is it strange", "is that strange", "is it odd", "is that odd",
               "odd that", "odd to", "is it unusual", "is that unusual", "is it ok that",
               "is it okay that", "is there something wrong with me")

_NORMAL_SUBJECTS = (
    (("live at home", "living at home", "live with my parents", "living with my parents",
      "live with your parents", "living with your parents", "moved back home",
      "moved back in", "still at home", "still live with my mum", "still live with my dad",
      "live with my mum", "live with my dad", "back with my parents"),
     "Living at home as an adult is common: about a quarter of 25 to 34 year olds in the UK still "
     "do, and more do wherever rents are high. What makes it work is agreed terms - what you pay, "
     "what you do round the house, and a date to look at it again - not how long it has been."),
    (("talk to myself", "talking to myself", "talk to yourself", "talking to yourself",
      "talk out loud", "talking out loud", "answer myself", "argue with myself"),
     "Nearly everyone does - surveys put it around 9 in 10 adults - and talking out loud on "
     "purpose is how people hold a task in mind, which is why athletes and surgeons do it. It is "
     "only worth a thought if the voice is not yours or it tells you what to do."),
    (("sleep with a teddy", "sleep with my teddy", "still have a teddy", "sleep with a soft toy",
      "teddy", "teddies", "comfort blanket", "blankie", "cuddly toy", "stuffed toy"),
     "About a third of adults in surveys still have a childhood soft toy, and plenty of them "
     "sleep with it: it is a sleep cue, and a sleep cue that works is worth keeping. It only "
     "matters if it is the only way you can settle at all."),
    (("not want children", "not want kids", "not wanting children", "not wanting kids",
      "not wanting a baby", "not want a baby", "childfree", "child free", "not having children",
      "not having kids", "no children by choice", "never want kids", "childless by choice"),
     "About one in five women in the UK reaches 45 without children, and choosing that is "
     "common enough that nobody owes anyone a reason. The thing worth doing is saying it out "
     "loud to a partner early, because the assumptions people make are where the trouble is."),
    (("cry at films", "cry at a film", "cry at movies", "cry at a movie", "crying at films",
      "cry at the cinema", "cry at adverts", "cry at tv", "cry at everything"),
     "That is being moved, and it is what a story is built to do: films pace the music, the "
     "close-ups and the pauses to make you feel for someone. Crying easily at a screen goes with "
     "empathy rather than fragility, and most people find it settles as the mood does."),
    (("broke up", "break up", "breakup", "break-up", "split up", "got dumped", "being dumped",
      "divorce", "divorced", "separation", "she left me", "he left me"),
     "Sad after a break-up is grief, not an illness: it comes in waves with good hours in "
     "between, and it eases over weeks rather than days. The line where it is worth a GP is low "
     "mood most of the day, most days, for two weeks, with nothing giving you pleasure any more."),
    (("dont drink", "don't drink", "not drinking", "i dont drink alcohol", "teetotal", "sober",
      "not a drinker", "stopped drinking", "gave up alcohol", "gave up drinking"),
     "About one in five adults in the UK does not drink at all, and the under-30s drink less "
     "than their parents did, so you are much less of an odd one out than a round of drinks "
     "makes it feel. 'Not for me, thanks' is a whole answer, and asking them something after it "
     "ends the conversation about your glass."),
    (("still single", "single at 30", "single at 40", "never had a girlfriend",
      "never had a boyfriend", "never have had a girlfriend", "never have had a boyfriend",
      "never had a partner", "never have had a partner", "never been in a relationship",
      "never dated", "not had a relationship", "never had a relationship",
      "no relationship at 30"),
     "Plenty of people get to 30 without a relationship, and the number is rising: the timing "
     "of a first relationship stretches over a decade, and none of it is a verdict on you. What "
     "makes the difference is meeting people in a place you would go anyway, rather than "
     "waiting to be picked."),
)

_NORMAL_WORDS = tuple(word for words, _ in _NORMAL_SUBJECTS for word in words)


def _the_normal_answer(memory, understood):
    text = " " + str((understood or {}).get("text") or (understood or {}).get("clean")
                     or "").lower() + " "
    for words, reply in _NORMAL_SUBJECTS:
        if any(word in text for word in words):
            return reply
    return None


def _a_table_bills_line(understood):
    text = " ".join(str(one) for one in ((understood or {}).get("words") or ())).lower()
    if not text:
        text = str((understood or {}).get("clean") or (understood or {}).get("text") or "").lower()
    if _A_SHARED_HOME.search(text):
        return False
    return bool(_A_MANNERS_WORD.search(text) or _A_TABLE_BILL.search(text))


_A_MANNERS_WORD = re.compile(
    r"\b(?:rude|ruder|politest|polite|impolite|cheeky|stingy|stingey|tight|mean|weird|strange"
    r"|normal|ok|okay|fine|wrong|right|fair|acceptable|unacceptable|awkward|etiquette|manners"
    r"|bad\s+form|selfish|generous|expected|allowed|supposed|unfair|annoying|greedy"
    r"|cheapskate)\b")
_A_TABLE_BILL = re.compile(
    r"\b(?:bill|tab|check|cheque|dinner|lunch|brunch|meal|restaurant|drinks|round"
    r"|takeaway|takeout|coffee|starter|dessert|menu)\b")
_A_SHARED_HOME = re.compile(
    r"\b(?:rent|flats?|houses?|housemates?|flatmates?|roommates?|household|landlord|tenancy"
    r"|mortgage|council\s+tax|utilit(?:y|ies)|electricity|energy|heating|broadband|wifi"
    r"|internet|partner|husband|wife|spouse|boyfriend|girlfriend|couple|income|earns?|salary"
    r"|pays?\s+(?:half|halves)|joint\s+account|bills?\s+between\s+us)\b")


ENTRIES = [
    entry("best-season", ("season", ("best", "favourite", "favorite", "think", "pick", "prefer",
                                     "like", "love", "better", "decide", "undecided")),
          _asked(_best_season),
          avoid=("visit", "travel", "holiday", "trip", "plant", "sow", "grow")),
    _either("air-fryer-or-oven", ("air fryer", "air fryers"), ("oven",),
            _asked("Oven for a big tray and anything wet; air fryer for a small, crisp batch "
                   "with less heat in the kitchen. If you already cook for one or two, the air "
                   "fryer earns its space.")),
    entry("pizza-topping", ("pizza", ("topping", "best", "favourite", "favorite", "think", "pick")),
          _asked("Pepperoni, hot out of the oven, is the one I'd pick. Mushroom and ham is the "
                 "better pizza when you want the whole thing rather than a slice.")),
    entry("pineapple-pizza", ("pineapple", "pizza"),
          _asked("For it, honestly. Sweet with salty ham and hot cheese works; people mostly "
                 "enjoy being angry about it.")),
    entry("rainy-sunday", (("rainy", "raining", "wet weekend"), ("sunday", "day", "weekend",
                                                                "afternoon", "think", "like")),
          _asked("I like them: a rainy Sunday is a good excuse to do something that needs a "
                 "whole afternoon — a long film, a proper cook, or a book with the phone in "
                 "another room."),
          avoid=("kid", "kids", "child", "children", "toddler", "baby", "teen", "family",
                 "film", "films", "movie", "movies", "watch", "watching", "something to watch",
                 "book", "books", "read", "reading", "recipe", "cook", "make",
                 "save", "saving", "savings", "money", "fund", "afford", "pay", "pounds",
                 "ideas", "idea", "things to do", "something to do", "what can i do",
                 "what can we do", "what should i do", "what to do", "bored",
                 "step", "steps",
                 "music", "album", "albums", "playlist", "playlists",
                 "podcast", "podcasts", "listen", "listening", "spotify", "tunes")),
    entry("cereal-soup", ("cereal", ("soup", "salad", "think")),
          _asked("Not a soup. Soup is cooked and served hot; cereal is assembled cold at the "
                 "last second, which makes it closer to a salad with milk.")),
    entry("air-fryer", (("air fryer", "air fryers"), TASTE),
          _asked("Worth it for one or two people who like crisp things: chips, roast vegetables "
                 "and chicken thighs in half the time. Skip it if you cook for four or already "
                 "have a good fan oven."),
          bias=2,
          avoid=NOT_A_BUYING_ASK + DISPOSAL + FAULT + TRADES + ("clean", "cleaning", "cleaner",
                                                     "wash",
                                                     "washing", "grease", "greasy", "crumbs",
                                                     "scrub", "dirty", "stain", "stains")),
    entry("opinion-on-my-gadget",
          (("blender", "food processor", "slow cooker", "bread maker", "smoothie maker",
            "juicer", "coffee machine", "stand mixer", "pressure cooker", "sandwich toaster",
            "ice cream maker", "air fryer"),
           ("my new", "my old", "my own", "do you like my", "think of my", "reckon of my",
            "i bought", "i've bought", "i just bought", "i got", "i've got", "we bought",
            "we got", "our new", "i have got", "ive got", "i have", "we have", "we have got",
            "i was given", "got given", "someone gave me", "i have been given", "was given a",
            "i have just bought", "have just got", "just got a", "i use my", "i use the")),
          _asked(_gadget_view),
          avoid=FAULT + TRADES + ("broken", "wont", "won't", "stinks", "smells", "leaking")),
    entry("worth-an-appliance",
          (("dishwasher", "tumble dryer", "dryer", "washing machine", "slow cooker", "bread maker",
            "blender", "food processor", "pressure cooker", "vacuum", "hoover", "freezer"),
           TASTE),
          _worth_an_appliance,
          bias=2,
          avoid=NOT_A_BUYING_ASK + DISPOSAL + FAULT + TRADES + OWN_BUYING_ANSWER + A_JOB_ON_IT
          + ("how long does", "how long do", "how long will", "how long to", "how long before",
             "take to get cold", "get cold", "heat up", "heats up", "preheat",
             "service", "services", "servicing", "serviced")
          + ("need a vent", "needs a vent", "need venting", "needs venting", "need to vent",
             "needs to vent", "vent for", "vent a tumble", "vent the dryer", "vent my dryer",
             "vent a dryer", "venting a", "outside vent", "wall vent", "vent hose", "hose keeps",
             "where can i put", "can i put my dryer", "can a tumble dryer go",
             "can a dryer go", "can i put a dryer")
          + ("scared", "scary", "afraid", "frightened", "frightens", "terrified", "terrifies",
             "panics", "hates", "hate", "hiding", "hides", "cowers", "trembles", "shakes",
             "shaking", "barks", "barking"),
          guard=lambda understood: not asks_where_a_shop_answers(understood)),
    entry("worth-solar",
          (("solar panel", "solar panels", "solar pv", "solar tiles", "pv panels", "solar"),
           ("worth", "worth it", "should i", "is it worth", "get", "getting", "buy", "buying",
            "any good", "reckon", "pay for itself", "payback", "pay back", "save money",
            "recommend", "recommended", "recommendation", "recommendations",
            "any point in", "point in solar", "waste of money", "do i need", "do i need solar",
            "savings", "roof", "battery", "install", "installing", "installed", "quote",
            "south facing", "shade", "kwh", "export", "feed in tariff")),
          "Worth it if the roof is roughly south facing, unshaded, and somebody is in during the "
          "day: a typical 4kW system costs about £5,000 to £7,000 fitted and pays back in 10 to 14 "
          "years on the avoided bill plus the export payment. A battery rarely pays for itself. "
          "Get two quotes with the yearly kWh in writing, and the MCS certificate.",
          avoid=("how do", "how does", "how is", "what is", "what are", "explain", "work",
                 "works", "working", "broken", "not working", "fault", "faulty", "panel is",
                 "panels are", "clean", "cleaning", "moss", "bird", "installer has", "already")),
    entry("is-that-normal", (_NORMAL_WORDS, _NORMAL_ASK), _the_normal_answer,
          avoid=("blood test", "blood tests", "period", "periods", "spotting", "discharge",
                 "lump", "lumps", "pregnant", "pregnancy", "miscarriage", "hiv", "std", "stis",
                 "pain", "pains", "hurts", "bleeding", "temperature", "rash", "itch", "itchy"),
          bias=4),
    entry("eat-alone", (("eat alone", "eating alone", "by myself", "by yourself", "on my own",
                         "on your own", "eating on your own", "eat on my own"),
                        ("restaurant", "cafe", "pub")),
          _asked("Not rude at all, and it gets easier with a book or a seat at the bar. Nobody "
                 "in there is thinking about you half as much as you fear.")),
    entry("out-on-your-own",
          (("cinema", "film", "films", "movie", "movies", "gig", "gigs", "concert", "theatre",
            "show", "museum", "gallery", "exhibition", "festival", "pub", "restaurant",
            "cafe", "meal", "brunch", "lunch", "dinner", "coffee", "eat", "eating", "class",
            "course", "gym", "swim", "match", "talk", "things", "going out", "go out",
            "night out", "day out", "weekend"),
           ("on my own", "on your own", "alone", "by myself", "by yourself", "solo",
            "single ticket", "no one to go with", "nobody to go with", "without anyone")),
          _asked("Go, and go once without talking yourself out of it: the hard part is the ten "
                 "minutes before you sit down, not the two hours after. Book one seat at the end "
                 "of a row for the cinema or the theatre so you are not climbing over people, "
                 "take a bar stool rather than a table in a pub or a restaurant, and arrive five "
                 "minutes late rather than half an hour early. Take something to do with your "
                 "hands the first time and pick a weekday evening - the second trip is easy."),
          avoid=("travel", "travelling", "traveling", "trip", "holiday", "holidays", "abroad",
                 "flight", "flights", "hostel", "backpacking", "swim", "swimming", "lengths",
                 "wedding", "lonely", "loneliness", "lonely",
                 "what can i eat", "what should i eat", "what to eat", "what can i have",
                 "meal ideas", "meal plan", "recipes", "recipe", "cooking", "cook",
                 "food shop", "batch",
                 "cat", "cats", "kitten", "kittens", "dog", "dogs", "puppy", "puppies", "pup",
                 "rabbit", "hamster", "budgie", "parrot", "pet", "pets", "tortoise", "ferret",
                 "guinea pig", "goldfish", "fish", "horse", "pony", "snake", "lizard"),
          bias=2),
    entry("phone-at-dinner", ("phone", ("dinner table", "at dinner", "at the table",
                                        "during dinner", "meal")),
          _asked("Face down and out of reach, at least while you're eating. A phone on the table "
                 "pulls attention even when it's silent; taking it out to show a photo is fine, "
                 "it's the checking that annoys people.")),
    entry("read-book-first", ("book", ("film", "movie"),
                         ("before", "first", "adaptation", "better", "worse", "which",
                          "as good as", "good as")),
          _asked("Read the book first if you care about the story, watch the film first if you "
                 "might not finish the book. An adaptation cuts, so the film rarely ruins a "
                 "good novel — the other way round happens more."),
          guard=lambda understood: not the_book_is_a_reservation(understood),
          avoid=("holiday", "holidays", "flight", "flights", "hotel", "hotels", "trip",
                 "travel", "accommodation", "airbnb", "villa", "restaurant", "table",
                 "train", "trains", "tickets", "ferry", "car hire", "hire car", "check in",
                 "check-in", "abroad")),
    entry("split-bill-etiquette", (("split the bill", "splitting the bill", "split the cost",
                          "go halves", "go halfs", "splitting a bill", "split the tab",
                          "split tabs", "split the check",
                          "split bills", "splitting bills",
                          "divide the bill", "dividing the bill", "divvy up the bill",
                          "share the bill", "sharing the bill"),
                         ("fair", "ok", "rude", "should", "right", "better", "how", "best",
                          "friends", "even",
                          "fine", "okay",
                          "etiquette", "manners", "awkward", "impolite", "polite", "cheeky",
                          "stingy", "tight", "mean", "rude", "weird", "strange", "wrong",
                          "acceptable", "normal", "expected",
                          "bad form", "selfish", "generous", "allowed", "supposed", "unfair",
                          "annoying", "greedy", "stingey", "cheapskate")),
          _asked("Even split is fine when everyone ordered roughly the same; ask for separate "
                 "bills when one person had the steak and the wine. Say it before the bill "
                 "arrives and nobody has to be awkward."),
          bias=1,
          guard=_a_table_bills_line,
          avoid=("housemate", "housemates", "flatmate", "flatmates", "roommate", "roommates",
                 "household", "flat share", "house share", "shared flat", "shared house",
                 "with my flat", "council tax", "electricity", "broadband",
                 "partner", "husband", "wife", "boyfriend", "girlfriend", "fiance", "fiancee",
                 "other half", "as a couple", "joint account", "our bills", "the rent",
                 "taxi", "taxis", "cab", "cabs", "uber", "ride", "fare", "fares", "petrol",
                 "diesel", "fuel", "parking", "toll", "tolls",
                 "hotel", "hotel room", "a room", "the room", "rooms", "cottage", "cottages",
                 "airbnb", "villa", "caravan", "holiday house", "holiday home", "apartment",
                 "present", "presents", "gift", "gifts", "collection", "whip round", "kitty",
                 "secret santa", "leaving present", "wedding present",
                 "holiday", "holidays", "vacation", "flight", "flights", "trip", "weekend away",
                 "week away", "weekend break", "city break", "abroad", "group holiday")),
    entry("regift", (("regift", "re-gift", "re gift", "give it away"),
                     ("ok", "rude", "fine", "should", "wrong")),
          _asked("Fine, with two rules: the person who gave it to you never finds out, and the "
                 "next person would actually use it. Take the original card out first.")),
    entry("learn-to-drive", (("learn to drive", "driving licence", "driving license",
                              "driving test", "driving lesson", "driving lessons"),
                             ("should", "worth", "need", "old", "late", "adult", "any point")),
          _asked("Yes, if you'll use it: the licence is much easier to get at 20 than at 40, and "
                 "it opens up jobs and weekends. In a city with good buses and trains the cost "
                 "rarely adds up, so decide on the next five years, not on the test."),
          avoid=("how many", "how long does it take", "how long until", "how often",
                 "fail", "failed", "failing", "fails", "flunked",
                 "renew", "renews", "renewing", "renewal", "expired", "expires", "runs out",
                 "replace", "replacement", "lost", "photocard")),
    entry("keep-a-diary", (("keep a diary", "write a diary", "start a diary", "keeping a diary",
                            "journal", "journaling"),
                           ("worth", "should", "start", "keep", "help", "good", "why")),
          _asked("Worth two weeks, then decide. Three lines at night is enough to show you "
                 "patterns you'd otherwise miss; if it starts to feel like homework, stop — "
                 "a diary you dread is worse than none.")),

    entry("instrument-adult", (("instrument", "piano", "guitar", "ukulele", "violin", "drums",
                                "keyboard", "flute", "cello", "sax", "saxophone", "trumpet",
                                "clarinet", "harmonica", "singing", "sing", "choir", "harp"),
                               ("adult", "learn", "learning", "learned", "learnt", "start",
                                "begin", "wanted", "always", "worth", "45", "40", "50", "60",
                                "age", "old age", "my age")),
          _asked(_start_instrument),
          avoid=("daughter", "son", "kid", "kids", "child", "children", "grandson",
                 "granddaughter", "nephew", "niece", "teenager", "toddler", "washing",
                 "laundry", "machine", "dryer", "tumble", "ear", "ears", "eardrum",
                 "boiler", "loud", "noisy", "computer", "laptop", "typing", "champagne",
                 "prosecco", "wine", "sparkling"),
          bias=1),
    entry("instrument-how-long", (("song", "tune", "piano", "guitar", "ukulele", "violin",
                                   "instrument", "music", "chords", "scales", "beat", "drum",
                                   "drums", "flute", "cello", "sax", "trumpet", "singing"),
                                  ("how long", "long", "months", "month", "weeks", "soon")),
          _how_long_song,
          avoid=("ear", "ears", "eardrum", "washing", "machine", "laundry", "brake", "brakes",
                 "cardrum", "tumble", "dryer", "open mic", "open mike", "gig", "gigs",
                 "concert", "recital", "audition", "performance", "performing", "on stage",
                 "nervous", "mc"),
          bias=1),
    entry("instrument-practise", (("practise", "practice"), ("first", "start", "begin", "what")),
          _practise_first,
          avoid=("driving", "exam", "test", "interview", "speech", "presentation", "football",
                 "singing", "language", "spanish", "french", "italian", "german", "amp", "buy",
                 "purchase", "shop", "pedal", "strings", "course", "app", "tutor", "teacher")),
    entry("instrument-how-often", (("practise", "practice", "practising", "practicing"),
                                   ("how often", "often", "how many times", "times a week",
                                    "a day", "per day", "how much should i practise",
                                    "how much practice", "every day", "daily", "minutes")),
          _how_often_at_it,
          avoid=("driving", "exam", "test", "interview", "speech", "presentation", "football",
                 "tennis", "golf", "singing", "language", "spanish", "french", "italian",
                 "german", "amp", "buy", "purchase", "shop", "pedal", "strings", "course",
                 "app", "tutor", "teacher", "rest", "stop", "hurt", "hurts", "pain", "sore",
                 "injury", "injured",
                 "serve", "serves", "toss", "tosses", "swimming", "swim", "running", "run",
                 "cycling", "cycle", "gym", "weights", "yoga", "dancing", "dance", "singing",
                 "boxing", "climbing", "skating", "skiing", "batting", "bowling", "cricket",
                 "golf", "putting", "netball", "hockey", "basketball", "rugby", "football",
                 "tennis", "badminton", "squash", "rowing", "sailing")),

    _either("cats-dogs", ("cat", "cats"), ("dog", "dogs"), _cats_or_dogs,
            avoid=("cheaper", "cheap", "cheapest", "cost", "costs", "costing", "afford",
                   "affordable", "money", "price", "prices", "expensive", "per year",
                   "a year", "a month", "insurance")),
    _either("tea-coffee", ("tea",), ("coffee",), _tea_or_coffee),
    _either("paper-ebook", ("paper", "paperback", "book", "books"),
            ("kindle", "ereader", "e-reader", "ebook", "ebooks"),
            "Paper for anything you want to remember, an e-reader for holidays and long queues. "
            "The real question is whether you're carrying it."),
    _either("tabs-spaces", ("tab", "tabs"), ("space", "spaces"),
            "Spaces: every editor shows them the same way, and nobody argues about how wide a "
            "tab is."),
    _either("android-iphone", ("android",), ("iphone", "apple"),
            "iPhone if you want the simplest five years of updates; Android if you want a "
            "cheaper phone or more choice of hardware. Neither is a mistake.",
            avoid=("android", "iphone")),
    _either("city-country", ("city", "town"), ("countryside", "country", "village", "rural"),
            "City for a week, countryside for a month. If I had to choose one for good it would "
            "be the countryside, with a town within reach."),
    _either("beach-mountains", ("beach", "coast", "sea"), ("mountain", "mountains", "hills"),
            "Mountains: you can always find shade and a view, and the walk earns the dinner. "
            "Beaches win with small children, though — sand keeps them busy for hours."),
    _either("sweet-savoury", ("sweet", "sugary"), ("savoury", "salty"),
            "Savoury on a normal day — eggs, or toast with something salty — because it keeps "
            "you going until lunch. Sweet is for weekends and holidays."),
    _either("hot-cold-weather", ("hot", "hot weather", "summer", "warm", "sunshine"),
            ("cold", "cold weather", "winter", "freezing", "snow"),
            "Cold, if I can wrap up: you can always add a layer, and a cold walk ends with a hot "
            "drink. Heat is harder to escape from.",
            avoid=("than", "because", "degrees", "radiator", "radiators", "boiler", "thermostat",
                   "bleed", "bleeding", "at the top", "at the bottom", "toes", "hands",
                   "bath", "shower", "showers", "swim", "swimming", "pool", "sauna",
                   "compress", "ice pack", "heat pack", "hot water bottle", "sore",
                   "muscle", "muscles", "back", "sprain", "sprained", "stiff", "stiffness",
                   "injury", "injured", "cramp", "ache", "aches", "fever", "chills")),
    _either("cinema-home", ("cinema", "big screen"), ("home", "streaming", "sofa", "netflix"),
            "Cinema for anything with scale or a big sound; home for comedies and anything you "
            "might pause. The cinema's real advantage is that nothing else asks for your "
            "attention for two hours."),
    _either("rent-buy", ("rent", "renting", "rented"), ("buy", "buying", "mortgage", "owning"),
            "Buy once you know where you want to be for five years or more and the mortgage is "
            "no more than a third of your take-home pay; rent until then, and keep the deposit "
            "growing. Renting is also the honest answer when the job might move.",
            avoid=("car", "van", "bike", "flat for the weekend", "holiday"),
            bias=1),
    _either("run-walk", ("run", "running", "jog", "jogging"), ("walk", "walking"),
            "Walk if you are starting out or carrying an injury, run if you want the same "
            "fitness in half the time. Walking is easier to keep up for a year, and a year is "
            "what changes anything."),
    _either("walk-cycle", ("walk", "walking", "on foot"), ("cycle", "cycling", "bike",
                                                             "bicycle"),
            "Cycle if the trip is more than about two miles and there is somewhere to lock a bike "
            "and change; walk if it is shorter and you want the thinking time. Under twenty "
            "minutes either way it comes down to which one you will still do in the rain."),
    _either("electric-petrol", ("electric", "electric car", "ev"), ("petrol", "diesel", "hybrid"),
            "Electric for the everyday car: cheaper to run, quieter, and charging at home beats "
            "a forecourt. Petrol still wins if you drive long distances weekly or cannot charge "
            "at home; a hybrid is the compromise that suits most people who cannot.",
            avoid=("won't", "wont", "charging point", "not charging", "battery", "repair",
                   "garage", "lease")),
    entry("remote-work", (("remote work", "remote working", "working from home", "wfh",
                           "hybrid working"),
                          ("think", "good", "better", "worth", "opinion", "prefer", "like")),
          _asked("Remote for the work that needs quiet, the office for the work that needs "
                 "people. Two or three days in is the arrangement most people end up "
                 "preferring, and it keeps you in the room when decisions get made."),
          avoid=("focus", "distracted", "routine", "procrastinating", "lonely", "isolated")),
    entry("decide-a-choice",
          (tuple(word for options, _ in DECISION_SUBJECTS for word in options) + CAT_WORDS,
           STUCK_SHAPES, DECIDE_WORDS),
          _deciding, ask=STUCK_SHAPES + ("decide", "deciding", "decision", "whether", "choice"),
          avoid=("step", "steps", "wont", "won't", "isnt", "isn't", "broken", "fault", "leak",
                 "leaking", "recipe", "recipes", "cook", "drain", "not working", "sick", "ill",
                 "vet", "insurance", "tax", "mot", "service", "repair", "error", "flashing",
                 "or", "vs", "versus", "either",
                 "name", "names", "naming", "called", "call it", "what to call",
                 "difference", "differences",
                 "neuter", "neutered", "neutering", "neuters", "spay", "spayed", "spaying",
                 "castrate", "castrated", "the snip",
                 "watch", "watching", "film", "films", "movie", "movies", "series", "tv",
                 "netflix", "read", "reading", "book", "books", "play", "game", "games")),
    entry("cat-decide",
          (CAT_WORDS, CAT_VERDICT_SHAPES),
          _deciding, ask=CAT_VERDICT_SHAPES, bias=1,
          avoid=("need", "needs", "need to", "buy", "buying", "bought", "shop", "shopping",
                 "list", "kit", "litter", "tray", "food", "feed", "name", "called", "call it",
                 "spay", "spayed", "spaying", "neuter", "neutered", "neutering", "the snip",
                 "scratch", "scratching", "hiss", "hissing", "vet", "ill", "sick", "unwell",
                 "wont", "won't", "isn't", "isnt", "broken", "difference", "vs", "versus",
                 "two", "second", "pair", "better than one", "another"),
          guard=_not_another_cats_question),
]



for _rule_of_thumb in ENTRIES:
    if _rule_of_thumb.id == "worth-an-appliance":
        _rule_of_thumb.avoid = _rule_of_thumb.avoid + (
            "sealer", "sealers", "vacuum sealer", "vacuum sealers", "food sealer", "food sealers")
