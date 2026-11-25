import re

from ..memory import last_bot
from . import pick

CURRENCY = ("£", "$", "\u20ac")

LEAD = frozenset((
    "its", "it's", "thats", "that's", "the", "about", "around", "roughly", "probably", "maybe",
    "only", "just", "like", "so", "and", "but", "plus", "well", "currently", "still", "now",
    "i", "have", "we", "got", "ive", "i've", "we've", "weve", "there", "is", "there's", "theres",
    "it", "of", "us", "them", "both", "looks", "works", "out", "at", "keeps", "costs", "cost",
    "pays", "paid", "uses", "takes", "spend", "spent", "save", "saved", "earn", "earns", "makes",
    "make", "means", "that", "this", "they", "he", "she", "my", "our", "his", "her", "was",
    "were", "will", "would", "be", "a", "an", "half", "for", "on", "over", "under", "being",
    "weigh", "weighs", "weighed", "weighing",
    "bring", "brings", "bringing", "brought", "take", "takes", "taking", "took", "home",
    "clears", "net", "nett",
    "put", "puts", "putting",
))

UNITS = {
    "minute": ("time", 1.0), "minutes": ("time", 1.0), "min": ("time", 1.0),
    "mins": ("time", 1.0), "hour": ("time", 60.0), "hours": ("time", 60.0),
    "hr": ("time", 60.0), "hrs": ("time", 60.0),
    "day": ("span", 1.0), "days": ("span", 1.0),
    "week": ("span", 7.0), "weeks": ("span", 7.0),
    "month": ("span", 30.0), "months": ("span", 30.0),
    "year": ("span", 365.0), "years": ("span", 365.0),
    "mile": ("distance", 1.0), "miles": ("distance", 1.0),
    "km": ("distance", 0.6214), "kilometre": ("distance", 0.6214),
    "kilometres": ("distance", 0.6214), "kilometers": ("distance", 0.6214),
    "pound": ("money", 1.0), "pounds": ("money", 1.0), "quid": ("money", 1.0),
    "euro": ("money", 1.0), "euros": ("money", 1.0), "dollar": ("money", 1.0),
    "dollars": ("money", 1.0), "grand": ("money", 1000.0), "k": ("money", 1000.0),
    "metre": ("size", 1.0), "metres": ("size", 1.0), "meter": ("size", 1.0),
    "meters": ("size", 1.0), "foot": ("size", 0.3048), "feet": ("size", 0.3048),
    "inch": ("size", 0.0254), "inches": ("size", 0.0254), "cm": ("size", 0.01),
    "stone": ("weight", 6.35029), "stones": ("weight", 6.35029),
    "kilo": ("weight", 1.0), "kilos": ("weight", 1.0), "kilogram": ("weight", 1.0),
    "kilograms": ("weight", 1.0), "kg": ("weight", 1.0), "kgs": ("weight", 1.0),
    "lb": ("weight", 0.4536), "lbs": ("weight", 0.4536),
}
NUMBERS = {
    "one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7, "eight": 8,
    "nine": 9, "ten": 10, "eleven": 11, "twelve": 12, "thirteen": 13, "fourteen": 14,
    "fifteen": 15, "sixteen": 16, "seventeen": 17, "eighteen": 18, "nineteen": 19,
    "twenty": 20, "thirty": 30, "forty": 40, "fifty": 50, "sixty": 60, "seventy": 70,
    "eighty": 80, "ninety": 90, "hundred": 100, "thousand": 1000, "dozen": 12, "couple": 2,
    "few": 3, "half": 0.5, "a": 1, "an": 1, "several": 4,
}
TENS = {"twenty": 20, "thirty": 30, "forty": 40, "fifty": 50, "sixty": 60, "seventy": 70,
        "eighty": 80, "ninety": 90}
PERIODS = (
    ("a month", "month"), ("per month", "month"), ("each month", "month"), ("monthly", "month"),
    ("a week", "week"), ("per week", "week"), ("each week", "week"), ("weekly", "week"),
    ("a year", "year"), ("per year", "year"), ("each year", "year"), ("yearly", "year"),
    ("a day", "day"), ("per day", "day"), ("each day", "day"), ("daily", "day"),
    ("a fortnight", "fortnight"), ("per fortnight", "fortnight"),
)
POINTING_BACK = frozenset(("for", "on", "about", "of", "at", "with", "in", "into", "to",
                           "towards", "toward", "from"))
A_PRONOUN = frozenset(("it", "that", "this", "them", "those", "these", "him", "her",
                       "everything", "anything", "something"))
HEDGES = frozenset(("think", "thought", "reckon", "guess", "suppose", "believe", "hope", "say",
                    "imagine", "assume"))
TRIP = re.compile(r"\b(each\s+way|each-way|one\s+way|round\s+trip|there\s+and\s+back|"
                  r"on\s+the\s+(?:bus|train|tube|tram|bike|bicycle)|in\s+the\s+car|"
                  r"by\s+(?:car|bus|train|bike)|commut\w*)\b")
PER_DAY = re.compile(r"\b(a\s+day|per\s+day|each\s+day|every\s+day|a\s+weekday)\b")
TAIL = frozenset((
    "each", "way", "one", "round", "trip", "there", "and", "back", "a", "an", "per", "every",
    "day", "days", "week", "weeks", "month", "months", "year", "years", "fortnight", "hour",
    "hours", "minute", "minutes", "weekday", "left", "now", "though", "today", "already", "more",
    "total", "altogether", "on", "in", "the", "bus", "train", "tube", "tram", "bike", "bicycle",
    "car", "to", "work", "at", "moment", "right", "so", "far", "max", "maximum", "ish", "or",
    "about", "around", "extra", "over", "under", "spare", "saved", "saving", "savings",
    "coming", "out", "roughly", "odd", "monthly", "weekly", "yearly", "daily", "currently",
    "between",
    "probably", "maybe", "only", "just", "like", "well", "still", ":",
    "is", "all", "what", "have", "has", "to", "play", "with", "spend", "by", "of", "it", "that",
    "i", "we", "they", "you", "off", "away", "wide", "long", "high", "tall", "deep", "square",
    "weeknight", "weeknights", "weekday", "weekdays", "morning", "mornings", "evening",
    "evenings", "night", "nights", "shift", "shifts", "tops", "plus", "minus", "if", "when",
))

DOUBT_ON_THE_FIGURE = re.compile(
    r"^(?:[a-z',\u2019]+\s+){0,3}(?:is|isnt|isn'?t|was|wasnt|wasn'?t|too|thats|that'?s)\b\s*"
    r"(?:that|this|it|they)?\s*(?:a\s+lot|too\s+much|too\s+dear|expensive|cheap|dear|pricey|"
    r"steep|normal|about\s+right|fair|reasonable|good\s+value|worth\s+it|okay?)\b", re.I)

SAVINGS_AFTER_A_RATE = re.compile(
    r"\b(?:savings?|save|saves|saving|saved)\b"
    r"|\b(?:put|puts|putting|set|setting|pay|paying)\b[^.!?]{0,14}\b(?:away|aside|by|in|into)\b")
SAVINGS = (
    "{q} {period} is {year} a year. That is the figure to plan with, not the weekly one.",
    "{q} {period} is {year} a year. Is it steady, or does it move with the month?",
    "{q} {period} is {year} a year - the yearly figure is the one that adds up to something.",
)

MONEY_MONTH = (
    "{q} a month is {year} a year. Put as a year it is easier to weigh against a one-off cost.",
    "{q} a month is {year} a year - the number that matters if it runs for a while.",
    "{q} a month is {year} a year. Would you pay {year} up front for the same thing?",
    "{q} a month is {year} a year, which is the figure to hold against the yearly price.",
)
MONEY_WEEK = (
    "{q} a week is {month} a month, about {year} a year. Weekly adds up faster than it feels.",
    "{q} a week is {month} a month and {year} a year. Is that steady or a bad patch?",
    "{q} a week - that is {year} a year, or {month} a month. Which one is it really?",
)
MONEY_YEAR = (
    "{q} a year is {month} a month, about {week} a week. That is how it lands.",
    "Put as a month, {q} a year is {month} - and a month is the number people plan on.",
    "{q} a year is {month} a month. Is the money coming in monthly or in lumps?",
)
MONEY_DAY = (
    "{q} a day is {month} a month. It is the small daily ones that get away from people.",
    "{q} a day is {year} a year. Would you notice it going out once a year?",
)
INCOME_MONTH = (
    "{q} a month is {year} a year. Is that what you were expecting, or are you working out where "
    "it goes?",
    "{q} a month is {year} a year before anything comes off it. What are you weighing it against?",
    "{q} a month comes to {year} a year, which is the figure to compare one job with another.",
)
INCOME_WEEK = (
    "{q} a week is {month} a month, about {year} a year. Is the work steady or up and down?",
    "{q} a week is {year} a year - that is what it comes to over the good and the quiet weeks.",
)
INCOME_YEAR = (
    "{q} a year is {month} a month, about {week} a week. Is that what it was before, or a change?",
    "{q} a year is {month} a month. Put as a month it is easier to see where it goes.",
)
INCOME_PLAIN = (
    "{q} - is that what you take home, or before anything comes off it?",
    "{q}. Does that have to cover everything, or is some of it spoken for already?",
)
INCOME = re.compile(
    r"\b(?:earn(?:s|ed|ing)?|salary|salaries|wages?|income|pension|take[- ]home|"
    r"get(?:s|ting)? paid|paid (?:me|us)|pays? me|my pay|a pay ?rise|pay ?rise|"
    r"bring(?:s|ing)? (?:it )?home|brought (?:it )?home)\b")
MONEY_PLAIN = (
    "{q} - is that the whole budget or what is left of a bigger one?",
    "{q} goes further as a plan than as a number. What does it need to cover?",
    "{q}. What does it have to stretch to?",
)
TIME_BUDGET = (
    "{q} is enough for one thing done properly and not two done badly.",
    "In {q} take the shortest version of it rather than the best one. What is it for?",
    "{q} goes faster than it looks, so decide before you start rather than halfway through.",
    "{q} is tight - one thing only. What are you fitting into it?",
    "{q}: get everything out before the clock starts and the time is all work, not looking.",
)
TIME_TRIP = (
    "{q} each way is {day} a day, {week} a week if it is five days. Worth a number first.",
    "{q} twice a day is {day}, and five days of it is {week}. Do you get to sit down for it?",
    "That is {day} of your day, {week} a week. It is the part of the job nobody pays you for.",
)
TIME_A_DAY = (
    "{q} a day is {week} a week - small enough to keep up, which is the point of it.",
    "{q} a day adds up to {week} a week. Enough to see a change if it is the right thing.",
    "{q} a day, so {week} a week. The trick is that it has to fit a day you actually have.",
)
TIME_LONG = (
    "{q} is a real chunk of a week. What has to fit inside it?",
    "{q} - is that what you have, or what you think it needs?",
    "{q} is enough to get somewhere with it. What is the first thing in there?",
)
TIME_WEEK = (
    "{q} a week is about {day} a day. That is what it has to fit into.",
    "{q} a week comes to {day} a day - doable, if nothing else takes that slot.",
)
AREA = (
    "{q} by {b} is {area} square metres - have the number before you buy anything.",
    "That is {area} square metres. What is going on it?",
    "{q} by {b} is {area} square metres. A tin or a roll never covers what the label claims.",
)
DISTANCE_NEAR = (
    "{q} is about {walk} minutes walking, or {bike} on a bike.",
    "{q} - {walk} minutes on foot, and no time at all on a bike ({bike} minutes).",
    "{q} is close enough to walk in {walk} minutes, or ride in {bike}.",
)
DISTANCE_MID = (
    "{q} is about {bike} minutes on a bike, or {drive} in the car.",
    "{q} - a ride of about {bike} minutes, or {drive} driving.",
    "{q} is close enough to cycle ({bike} minutes) and quick in the car ({drive}).",
)
DISTANCE_FAR = (
    "{q} is about {drive} of driving.",
    "{q} is {drive} behind the wheel.",
    "{q} - {drive} in the car, and a lot longer any other way.",
)
DISTANCE_DAY_OUT = (
    "{q} is about {drive} of driving - a day out rather than a hop.",
    "{q} is {drive} behind the wheel; a day out, with a stop on the way.",
)
DISTANCE_FAR_TRIP = (
    "{q} each way is {drive} in the car. Doable in a day if you leave early.",
    "{q} each way - {drive} behind the wheel, and that is before you turn round.",
)
SPAN_DAYS = (
    "{q} is long enough to know whether it is working and short enough to change course.",
    "{q} - what has it done in that time? Better, worse or the same?",
    "{q} is a while. Is it going the way you want?",
)
SPAN_WEEKS = (
    "{q} is usually where a thing either settles or needs a proper look. Which is it?",
    "{q} - what would have to change for you to be happy with it?",
    "{q} is enough time for something to show. What has shown?",
)
SPAN_MONTHS = (
    "{q} is long enough that the small bits add up. What is the biggest part of it?",
    "{q} - is that how long it has been, or how long it needs to last?",
)
WEIGHT_LOSS = (
    "{q} is {other} - at a pound or two a week that is {slow} to {fast} weeks, and the slow way "
    "is the one that stays off.",
    "{q} - {other}. Think in months rather than weeks: a pound or two a week is {slow} to {fast} "
    "weeks, and that is the pace that holds.",
    "{q} is {other}, so it is a few months of small changes rather than a push. What would you "
    "change first?",
)
WEIGHT_PLAIN = (
    "{q} is {other}. Is that you, or something you are carrying?",
    "{q} - {other}. What is it that weighs that?",
)
WEIGHT_OF_A_THING = (
    "{q} is {other}.",
    "{q} - {other}. Is that what you expected?",
)
WEIGHT_THEIR_OWN = (
    "{q} is {other}. Is there a number you are aiming for?",
    "{q} - {other}. What would you like to do about it?",
)
WEIGHT_ON_THE_TABLE = re.compile(
    r"\b(?:weight|weigh|weighing|weighed|lose|losing|lost|slim|slimming|diet|diets|dieting|"
    r"stone|stones|kilos?|kilograms?|kg|lbs?|bmi|calories|waist|dress size)\b")
WEIGHT_GOING_ON = re.compile(
    r"\bput (?:on|it on|a bit on|a few on|a little on|a couple on|some on|another on|"
    r"weight on|the weight on|a stone on|half a stone on)\b|\b(?:piling|piled|piling it) on\b")


def _number_at(words, at):
    first = _amount(words[at])
    if first is None:
        return None, 0
    if at + 1 < len(words):
        nxt = words[at + 1].lower().replace("-", "")
        if nxt == "hundred" and first < 100:
            return first * 100, 2
        if words[at].lower() in TENS and nxt in ("one", "two", "three", "four", "five", "six",
                                                "seven", "eight", "nine"):
            return first + NUMBERS[nxt], 2
    return first, 1


def _amount(word):
    plain = word.replace(",", "")
    for mark in CURRENCY:
        plain = plain.replace(mark, "")
    plain = plain.replace("-", "")
    if re.fullmatch(r"\d+(?:\.\d+)?", plain):
        return float(plain)
    if plain in NUMBERS:
        return float(NUMBERS[plain])
    for ten, base in TENS.items():
        if plain.startswith(ten) and plain[len(ten):] in NUMBERS:
            return float(base + NUMBERS[plain[len(ten):]])
    return None


def _fmt(value):
    if float(value).is_integer():
        return "{:,}".format(int(round(value)))
    return "{:.1f}".format(value).rstrip("0").rstrip(".")


def _minutes(total):
    total = int(round(total / 5.0)) * 5
    if total < 60:
        return "%d minutes" % total
    hours, minutes = divmod(total, 60)
    if not minutes:
        return "%d hour%s" % (hours, "" if hours == 1 else "s")
    return "%d hour%s %d" % (hours, "" if hours == 1 else "s", minutes)


SUBJECT = re.compile(r"\A(?:the|my|our|their|his|her|its|this|that|it|there)\s+\w+\s+"
                     r"(?:is|are|was|were|would be|will be)\s+", re.I)

MONEY_NOUN = {"tenner": 10, "fiver": 5}
SUM_IN_A_WORD = re.compile(r"\b(?:a|an)\s+(tenner|fiver)\b", re.I)


def _the_sum_inside_the_word(text):
    found = SUM_IN_A_WORD.search(text)
    if not found:
        return "", text
    said = "a %s" % found.group(1).lower()
    return said, (text[:found.start()] + "%d" % MONEY_NOUN[found.group(1).lower()]
                  + text[found.end():])


ON_THE_TABLE_DISTANCE = re.compile(
    r"\b(?:far|further|distance|miles?|km|kilometres?|kilometers?|kms|run|runs|running|ran|"
    r"walk|walked|walking|walks|cycle|cycled|cycling|drive|drove|driving|"
    r"commute|commuting|hike|hiked|hiking|swim|swam|swimming|journey|trip)\b")


ON_THE_TABLE_MONEY = re.compile(
    r"\b(?:budget|spend|spending|spent|cost|costs|afford|save|saving|savings|price|prices|buy|"
    r"buying|bought|paid|pay|rent|bill|bills|deposit|money|cash|quid|salary|wage|wages|"
    r"income|pension|£|\$|€)\b")


def _the_money_words(text):
    return bool(ON_THE_TABLE_MONEY.search(str(text or "").lower()))


def _about_a_distance(clean, memory):
    said = " ".join(str(clean or "").lower().split())
    elsewhere = [said]
    turns = memory.get("turns") if isinstance(memory, dict) else None
    for turn in [t for t in turns if isinstance(t, dict)][-2:] if isinstance(turns, list) else []:
        elsewhere += [str(turn.get(key) or "") for key in ("user", "bot")]
    if any(_the_money_words(text) for text in elsewhere):
        return False
    return any(ON_THE_TABLE_DISTANCE.search(text.lower()) for text in elsewhere)


A_BUDGET_THEY_SET = re.compile(r"\b(?:my|our)\s+(?:budget|limit|cap|ceiling|spending money)\b")


def _read(clean, memory=None):
    text = clean.strip().strip(".!,")
    text = re.sub(r"(?<=\d)(kilometres|kilometers|kilograms|kilogram|miles|mile|stones|kilos|"
                  r"kilo|stone|kms|km|mi|kgs|kg|lbs|lb)\b", r" \1", text, flags=re.I)
    named = bool(SUBJECT.search(text))
    a_budget = bool(A_BUDGET_THEY_SET.search(text))
    text = SUBJECT.sub("", text, count=1)
    sum_word, text = _the_sum_inside_the_word(text)
    words = text.split()
    at = 0
    while at < len(words) and _amount(words[at]) is None:
        if words[at].lower() not in LEAD:
            return (None,) * 6
        at += 1
    if at >= len(words):
        return (None,) * 6
    head = words[at]
    amount, took = _number_at(words, at)
    body = words[at + took:]
    if head.lower() == "half" and body[:1] and body[0].lower() in ("a", "an"):
        body = body[1:]
    unit = body[0].lower() if body and body[0].lower() in UNITS else ""
    if unit:
        body = body[1:]
    half_more = [word.lower() for word in body[:3]] == ["and", "a", "half"]
    if half_more:
        amount *= 1.5
        body = body[3:]
    body = _without_a_remark(body)
    body = _without_the_household(body)
    tail = " ".join(body).lower()
    period = None
    for said, name in PERIODS:
        if tail == said or tail.startswith(said):
            period = name
            body = body[len(said.split()):]
            break
    if period and DOUBT_ON_THE_FIGURE.match(" ".join(body).strip(" .,!?")):
        body = []
    for word in body:
        plain = word.lower().strip(".,!?:")
        if plain in TAIL or plain in UNITS or _amount(word) is not None:
            continue
        if _a_length_they_have_bounded(clean, unit, body, period):
            break
        return (None,) * 6
    phrase = head if head[:1].isdigit() or head[:1] in CURRENCY else _fmt(amount)
    if unit in ("k", "grand"):
        phrase = "%s %s" % (phrase, unit)
    if head.lower() == "half" and unit:
        phrase = "%s %s" % ("half an" if unit[:1] in "aeiouh" else "half a", unit)
    if head.lower() in ("a", "an") and unit:
        phrase = "%s %s" % ("an" if unit[:1] in "aeiouh" else "a", unit)
    if half_more:
        phrase = "%s and a half" % phrase
    if unit:
        family, factor = UNITS[unit]
        body_tail = " ".join(body).lower()
        if unit == "k" and not period and _about_a_distance(clean, memory):
            return (amount * UNITS["km"][1], "distance", "km", None,
                    phrase[:-2].strip() if phrase.endswith(" k") else phrase, body_tail)
        if family == "money" and unit in ("pound", "pounds", "quid", "euro", "euros", "dollar",
                                          "dollars") and TRIP.search(body_tail + " " + tail):
            return (None,) * 6
        if family == "money" and a_budget:
            return (None,) * 6
        if family == "span" and named:
            return (None,) * 6
        if family == "weight" and named:
            return (None,) * 6
        return amount * factor, family, unit, period, phrase, body_tail
    if _a_take_without_home(words[:at]) and not sum_word:
        return (None,) * 6
    if a_budget and not sum_word:
        return (None,) * 6
    if period:
        if not sum_word and _a_count_the_question_asked_for(clean, memory):
            return (None,) * 6
        phrase = sum_word or phrase
        return amount, "money", "money", period, phrase, " ".join(body).lower()
    if sum_word:
        return amount, "money", "money", None, sum_word, " ".join(body).lower()
    if head[:1] in CURRENCY:
        return amount, "money", "money", None, phrase, ""
    return (None,) * 6


def _q(phrase, unit):
    if unit in ("money", "k", "grand") or unit in phrase:
        return phrase
    return "%s %s" % (phrase, unit)


SPAN_FRAME = re.compile(
    r"\b(?:been|since|ago|started|start|had|having|took|taking|on it|so far|now)\b", re.I)
A_QUESTION_ABOUT_A_LENGTH = re.compile(
    r"\bhow (?:long|far|much|many|big|deep|hot)\b|\bhow soon\b|\bwhen will\b", re.I)
A_BUDGET_QUESTION = re.compile(
    r"\bhow (?:long|much time|often)\s+(?:should|shall|do|can|could|might|would) (?:i|we)\b",
    re.I)


A_BOUND = re.compile(r"\b(?:only|just|barely|no more than|at most|less than)\b", re.I)
BOUNDED_BY = frozenset((
    "before", "until", "till", "til", "to", "for", "free", "spare", "off", "left", "after",
    "between", "while", "then", "so", "if", "and", "but", "plus", "today", "tonight", "now",
))
THEY_HAVE_THE_TIME = re.compile(
    r"^\s*(?:(?:i|we|ive|i've|we've|weve)\s+(?:only\s+|just\s+)?(?:have|had|got)\b|"
    r"(?:only\s+|just\s+)?got\b)", re.I)
A_REMAINDER = re.compile(r"\b(?:left|to go|remaining|to run)\b", re.I)
THEY_HAVE_IT = re.compile(r"\b(?:have|has|had|got|left|spare|need|needs|gives? me)\b", re.I)


A_LIMIT_ON_A_LENGTH = (
    "{q} is short. What is on the other side of it?",
    "{q} is not much time to sit through. What would make it easier?",
    "{q} is nothing in the scheme of a day. What are you least looking forward to?",
    "{q} is short enough that it will be over before it has properly started. What do you want "
    "out of it?",
)
A_WHAT_IS_LEFT = (
    "{q} left - short enough now that what goes in it matters. What has to happen in it?",
    "{q} left - that is the room there is. What is the one thing that has to get done?",
    "{q} left, so it is time to decide what matters. What would you put first?",
)


def _a_length_they_have_bounded(clean, unit, body, period):
    family = UNITS.get(unit, (None, None))[0]
    if family != "time" or period:
        return False
    said = " ".join(str(clean or "").lower().split())
    if not THEY_HAVE_THE_TIME.search(said):
        return False
    if not body:
        return False
    return body[0].lower().strip(".,!?:") in BOUNDED_BY


def _a_bound_not_a_budget(clean):
    said = " ".join(str(clean or "").lower().split())
    return bool(A_BOUND.search(said) and not THEY_HAVE_IT.search(said))


def _the_turn_above(memory):
    turns = [turn for turn in (memory.get("turns") or []) if isinstance(turn, dict)]
    return turns[-1] if turns else {}


A_CHANGE_SAID = re.compile(
    r"\b(?:lose|losing|lost|shed|shedding|drop|dropping|shift|shifting|put on|putting on|"
    r"gained|gaining|gain|gained|lose off|off)\b")
A_CHANGE_IS_THIS_SMALL = 20.0

I_WEIGH = re.compile(r"\bi (?:weigh|weighed|weighs)\b|\bive (?:weighed|put)\b")


def _the_change_is_the_line(clean):
    return bool(A_CHANGE_SAID.search(" ".join(str(clean or "").lower().split())))


def _a_weight_they_mean_themselves(memory, clean=""):
    if I_WEIGH.search(" ".join(str(clean or "").lower().split())):
        return True
    turns = [turn for turn in (memory.get("turns") or []) if isinstance(turn, dict)][-2:]
    for turn in turns:
        for key in ("user", "bot"):
            said = " ".join(str(turn.get(key) or "").lower().split())
            if WEIGHT_ON_THE_TABLE.search(said) or WEIGHT_GOING_ON.search(said):
                return True
    return False


SOMETHING_WEIGHED = re.compile(
    r"\b(?:he|she|it|they|we|you|the|my|our|his|her|their|this|that)\b[^.?!]{0,24}"
    r"\bweighs?\b|\bweighs?\b[^.?!]{0,24}\b(?:the|my|our|his|her|their|this|that)\b")


def _a_thing_was_named(memory, clean=""):
    if SOMETHING_WEIGHED.search(" ".join(str(clean or "").lower().split())):
        return True
    above = _the_turn_above(memory).get("user")
    if not above:
        return False
    try:
        from ..understanding.topics import THINGS
    except Exception:
        return False
    words = re.findall(r"[a-z]+", str(above).lower())
    return any(word in THINGS for word in words)


def _a_span_they_are_in(clean, memory):
    said = [clean]
    above = _the_turn_above(memory).get("user")
    if above:
        said.append(above)
    return any(SPAN_FRAME.search(" ".join(str(one or "").lower().split())) for one in said)


A_COUNT_ASKED_FOR = re.compile(r"\bhow many\s+([a-z]+)")
A_WAY_OF_PAYING = re.compile(
    r"\b(?:money|pounds?|quid|euros?|dollars?|bucks?|pence|cost|costs|spend|spent|spending|pay|"
    r"paid|paying|price|priced|budget|rent|bill|bills|salary|wage|wages|income|save|saving|"
    r"savings|afford|cheap|expensive|earn|earned|overdraft|loan|subscription)\b|[\u00a3$\u20ac]")


def _a_count_the_question_asked_for(clean, memory):
    turns = [turn for turn in (memory.get("turns") or []) if isinstance(turn, dict)]
    above = turns[-1] if turns else {}
    said = [" ".join(str(above.get("user") or "").lower().split()),
            " ".join(str(above.get("bot") or "").lower().split()),
            " ".join(str(clean or "").lower().split())]
    if not any(A_COUNT_ASKED_FOR.search(one) for one in said[:2]):
        return False
    return not any(A_WAY_OF_PAYING.search(one) for one in said)


def _a_fact_about_a_length(memory):
    above = " ".join(str(_the_turn_above(memory).get("user") or "").lower().split())
    return bool(above and A_QUESTION_ABOUT_A_LENGTH.search(above)
                and not A_BUDGET_QUESTION.search(above))


def reply_for(clean, memory):
    value, family, unit, period, phrase, tail = _read(clean, memory)
    if family is None:
        return None
    if family == "span" and _the_turn_above(memory) and not _a_span_they_are_in(clean, memory):
        return None
    if family == "time" and not period and value <= 180 and _a_fact_about_a_length(memory):
        return None
    if family in ("time", "span") and not period and A_REMAINDER.search(
            " ".join(str(clean or "").lower().split())):
        left = pick(A_WHAT_IS_LEFT, memory, clean).format(q=_q(phrase, unit))
        return left[:1].upper() + left[1:]
    if family == "time" and not period and _a_bound_not_a_budget(clean):
        limit = pick(A_LIMIT_ON_A_LENGTH, memory, clean).format(q=_q(phrase, unit))
        return limit[:1].upper() + limit[1:]
    reply = _say(family, _q(phrase, unit), value, period, tail, memory, clean, unit)
    return reply[:1].upper() + reply[1:] if reply else None


THEIR_THING = re.compile(r"\b(?:my|our|the|his|her|their)\s+([a-z][a-z'-]{2,})")
NOT_A_THING = frozenset("""
month months week weeks year years day days fortnight quarter hour hours minute minutes time
times lot lots one ones thing things rest whole same other other's own money cash budget
first last next same top bottom bill bills price prices cost costs total monthly weekly yearly
""".split())


def the_thing_they_pay_for(clean):
    said = " ".join(str(clean or "").lower().split())
    for word in THEIR_THING.findall(said):
        if word not in NOT_A_THING:
            return word
    return None


def the_rate_they_asked_about(clean, memory=None):
    value, family, unit, period, phrase, tail = _read(clean, memory)
    if family != "money" or not period:
        return None
    from .prices import PRICE_JUDGEMENT
    said = " ".join(str(clean or "").lower().split())
    if not PRICE_JUDGEMENT.search(said):
        return None
    if SAVINGS_AFTER_A_RATE.search(said) and period in ("month", "week", "year"):
        year = value * {"month": 12, "week": 52, "year": 1}[period]
        said_period = {"month": "a month", "week": "a week", "year": "a year"}[period]
        reply = pick(SAVINGS, memory, clean).format(
            q=_q(phrase, unit), period=said_period, year=_fmt(year))
        return reply[:1].upper() + reply[1:]
    reply = _say(family, _q(phrase, unit), value, period, tail, memory, clean, unit)
    return reply[:1].upper() + reply[1:] if reply else None


def _without_a_pointing_tail(words):
    if len(words) >= 2:
        tail = [word.lower().strip(".,!?:;") for word in words[-2:]]
        if tail[0] in POINTING_BACK and tail[1] in A_PRONOUN:
            return words[:-2]
    return words


def _without_a_hedge(words):
    if len(words) >= 2:
        tail = [word.lower().strip(".,!?:;") for word in words[-2:]]
        if tail[0] in ("i", "id", "i'd") and tail[1] in HEDGES:
            return words[:-2]
    return words


THE_HOUSEHOLD = (("between", "us"), ("between", "the", "two", "of", "us"),
                 ("for", "the", "two", "of", "us"), ("for", "both", "of", "us"),
                 ("between", "the", "two", "of", "them"), ("together",), ("combined",),
                 ("in", "total"), ("altogether",), ("in", "all"))


def _without_the_household(words):
    plain = [word.lower().strip(".,!?:;") for word in words]
    for phrase in THE_HOUSEHOLD:
        if tuple(plain[:len(phrase)]) == phrase:
            return words[len(phrase):]
        if len(plain) > len(phrase) and tuple(plain[-len(phrase):]) == phrase:
            return words[:-len(phrase)]
    return words


TAKE = ("take", "takes", "taking", "took")


def _a_take_without_home(lead):
    said = [word.lower().strip(".,!?:;") for word in lead]
    return any(word in TAKE for word in said) and "home" not in said


def _without_a_remark(words):
    for _ in range(3):
        trimmed = _without_a_pointing_tail(_without_a_hedge(words))
        if trimmed == words:
            break
        words = trimmed
    return words


def _in_a_conversation(memory):
    return any(turn.get("user") for turn in (memory.get("turns") or []) if isinstance(turn, dict))


A_STRETCH_THAT_IS_NOT_SHORT = 120


def _not_short(pool, value):
    if value < A_STRETCH_THAT_IS_NOT_SHORT:
        return pool
    kept = tuple(line for line in pool
                 if "is tight" not in line and "faster than it looks" not in line)
    return kept or pool


def _without_a_question(pool):
    return tuple(line for line in pool if "?" not in line) or pool


def _say(family, q, value, period, tail, memory, clean, unit=None):
    if family is None:
        return None
    if family == "money":
        if INCOME.search(str(clean or "").lower()):
            if period == "month":
                return pick(INCOME_MONTH, memory, clean).format(q=q, year=_fmt(value * 12))
            if period in ("week", "fortnight"):
                weeks = value if period == "week" else value / 2.0
                return pick(INCOME_WEEK, memory, clean).format(
                    q=q, month=_fmt(round(weeks * 52 / 12.0)), year=_fmt(weeks * 52))
            if period == "year":
                return pick(INCOME_YEAR, memory, clean).format(
                    q=q, month=_fmt(round(value / 12.0)), week=_fmt(round(value / 52.0)))
            return pick(INCOME_PLAIN, memory, clean).format(q=q)
        if period == "month":
            return pick(MONEY_MONTH, memory, clean).format(q=q, year=_fmt(value * 12))
        if period == "week":
            return pick(MONEY_WEEK, memory, clean).format(
                q=q, month=_fmt(round(value * 52 / 12.0)), year=_fmt(value * 52))
        if period == "year":
            return pick(MONEY_YEAR, memory, clean).format(
                q=q, month=_fmt(round(value / 12.0)), week=_fmt(round(value / 52.0)))
        if period in ("day", "fortnight"):
            per_day = value / 14.0 if period == "fortnight" else value
            return pick(MONEY_DAY, memory, clean).format(
                q=q, month=_fmt(round(per_day * 30)), year=_fmt(round(per_day * 365)))
        return pick(MONEY_PLAIN, memory, clean).format(q=q)
    if family == "time":
        if period == "day" and not TRIP.search(str(tail or "")):
            return pick(TIME_A_DAY, memory, clean).format(
                q=q, week=_minutes(value * 7), month=_minutes(value * 30))
        if TRIP.search(tail):
            return pick(TIME_TRIP, memory, clean).format(
                q=q, day=_minutes(value * 2), week=_minutes(value * 10))
        if period == "week":
            return pick(TIME_WEEK, memory, clean).format(q=q, day=_minutes(value / 7.0))
        if value > 180:
            return pick(TIME_LONG, memory, clean).format(q=q)
        pool = TIME_BUDGET if not _in_a_conversation(memory) else _without_a_question(TIME_BUDGET)
        return pick(_not_short(pool, value), memory, clean).format(q=q)
    if family == "distance":
        if value <= 0:
            return None
        walk = int(round(value * 20))
        bike = int(round(value * 5))
        drive = int(round(value * 1.33 if value > 10 else value * 2.4))
        if value <= 3:
            return pick(DISTANCE_NEAR, memory, clean).format(q=q, walk=walk, bike=bike)
        if value <= 10:
            return pick(DISTANCE_MID, memory, clean).format(
                q=q, bike=bike, drive=_minutes(drive))
        if TRIP.search(str(tail or "")):
            pool = DISTANCE_FAR_TRIP
        elif value > 60:
            pool = DISTANCE_DAY_OUT
        else:
            pool = DISTANCE_FAR
        return pick(pool, memory, clean).format(q=q, drive=_minutes(drive))
    if family == "size":
        other = re.search(r"\bby\s+(\d+(?:\.\d+)?|" + "|".join(sorted(NUMBERS)) + r")\b", tail)
        if other is None:
            return None
        second = _amount(other.group(1))
        if not second or second <= 0:
            return None
        return pick(AREA, memory, clean).format(q=q, b=_fmt(second), area=_fmt(value * second))
    if family == "span":
        if value <= 3:
            return pick(SPAN_DAYS, memory, clean).format(q=q)
        if value <= 21:
            return pick(SPAN_WEEKS, memory, clean).format(q=q)
        if value <= 400:
            return pick(SPAN_MONTHS, memory, clean).format(q=q)
    if family == "weight":
        if value <= 0.2:
            return None
        kilos = "%s kilo%s" % (_fmt(round(value, 1)), "" if round(value, 1) == 1 else "s")
        pounds = value / 0.4536
        said_kilos = (unit or "") in ("kilo", "kilos", "kilogram", "kilograms", "kg", "kgs")
        other = "%s pound%s" % (_fmt(round(pounds, 1)), "" if round(pounds, 1) == 1 else "s") \
            if said_kilos else kilos
        slow = max(1, int(round(pounds / 2.0)))
        fast = max(1, int(round(pounds)))
        body = _a_weight_they_mean_themselves(memory, clean)
        if body and fast > 2 and (value <= A_CHANGE_IS_THIS_SMALL
                                  or _the_change_is_the_line(clean)):
            pool = WEIGHT_LOSS
        elif I_WEIGH.search(" ".join(str(clean or "").lower().split())):
            pool = WEIGHT_THEIR_OWN
        elif _a_thing_was_named(memory, clean):
            pool = WEIGHT_OF_A_THING
        else:
            pool = WEIGHT_PLAIN
        return pick(pool, memory, clean).format(q=q, other=other, slow=slow, fast=fast)
    return None


A_RANGE_WITH_A_UNIT = re.compile(
    r"\b(?P<lo>\d{1,4}(?:\.\d+)?|" + "|".join(sorted(NUMBERS, key=len, reverse=True)) + r")"
    r"\s*(?:to|and|-|\u2013|or)\s*"
    r"(?P<hi>\d{1,4}(?:\.\d+)?|" + "|".join(sorted(NUMBERS, key=len, reverse=True)) + r")"
    r"\s*(?P<unit>glasses?|litres?|liters?|hours?|minutes?|steps|portions?|servings?|"
    r"sessions?|workouts?|units?)\b"
    r"(?:\s*(?:a|per|each)\s*(?P<period>day|week|month))?", re.I)
UNIT_SAID = {"glasses": "glasses", "glass": "glasses", "litres": "litres", "litre": "litres",
             "liters": "litres", "liter": "litres", "hours": "hours", "hour": "hours",
             "minutes": "minutes", "minute": "minutes", "steps": "steps", "step": "steps",
             "portions": "portions", "portion": "portions", "servings": "portions",
             "serving": "portions", "sessions": "sessions", "session": "sessions",
             "workouts": "sessions", "workout": "sessions", "units": "units", "unit": "units"}
UNIT_IS = (
    (re.compile(r"glass|litre|liter", re.I), "water"),
    (re.compile(r"hour", re.I), "sleep"),
    (re.compile(r"minute|step|session|workout", re.I), "move"),
    (re.compile(r"portion|serving", re.I), "portion"),
)
A_SINGLE_RULE = re.compile(
    r"\b(?:about|around|roughly|at least|aim for|aim to|up to|no more than|no less than)\s+"
    r"(?P<num>\d{1,4}(?:\.\d+)?)\s*"
    r"(?P<unit>glasses?|litres?|liters?|hours?|minutes?|steps|portions?|servings?|sessions?|"
    r"workouts?|units?)\b(?:\s*(?:a|per|each)\s*(?P<period>day|week|month))?", re.I)
A_FIGURE_ALONE = re.compile(
    r"^(?:[a-z']+\s+){0,5}?(?P<num>\d{1,3}(?:\.\d+)?|" +
    "|".join(sorted(NUMBERS, key=len, reverse=True)) + r")\s*(?P<what>[a-z']*)\s*\.?$", re.I)
ABOUT_A_FIGURE = re.compile(
    r"\b(?:i (?:drink|get|sleep|do|walk|run|eat|have|take|manage|average|only get|usually get)"
    r"|about|around|roughly|maybe|only|just|probably|usually|average|like)\b", re.I)
AN_AGE = re.compile(r"\b(?:i'?m|im|i am)\b|\byears? old\b|\bage\b", re.I)
NOT_A_UNIT_ITSELF = re.compile(r"[£$€]|\b(?:k|kg|g|mg|ml|cm|mm|miles?|km|inches|feet|foot)\b",
                               re.I)
FIGURE_BELOW = (
    "{figure} {unit} is short of the {range} the answer named. {step}",
    "{figure} {unit} - that is under the {range} that answer gave, so the gap is the bit worth "
    "closing. {step}",
    "You are at {figure} {unit} against {range}. {step}",
)
FIGURE_INSIDE = (
    "{figure} {unit} is inside the {range} the answer named - that is the part that matters, so "
    "keep it there rather than adding to it.",
    "{figure} {unit} sits in the {range} the answer named. Steady is the whole of it at that "
    "level.",
)
FIGURE_ABOVE = (
    "{figure} {unit} is past the {range} the answer named. {step}",
    "You are already over the {range} the answer named at {figure} {unit}. {step}",
)
STEPS = {
    "water": {
        "below": "Put a glass by the kettle and have one with each meal, which is three before "
                 "you count anything else.",
        "above": "Past that, more is not better: pale straw is the check, and you are already "
                 "there.",
    },
    "sleep": {
        "below": "Half an hour earlier to bed, with the same wake-up time even after a bad "
                 "night, is what closes it.",
        "above": "Sleeping past it is not a gain - the steady wake-up time is what keeps the "
                 "good nights coming.",
    },
    "move": {
        "below": "Two ten-minute walks beat one long one, because they are easier to keep up.",
        "above": "Past it, the gain is in keeping it going rather than adding more.",
    },
    "portion": {
        "below": "One at breakfast and one at each main meal gets you to it without a plan.",
        "above": "Past it, the thing worth holding is the mix rather than the count.",
    },
}
A_STEP_EITHER_WAY = {
    "below": "Start at what you can keep up and add a little when it feels easy.",
    "above": "Being past it is not what needs fixing; keeping it steady is.",
}


PERIOD_NAMED = {"day": "a day", "week": "a week", "month": "a month"}

TEN_TIMES = 10


def _the_unit_of_one(unit):
    word = str(unit or "")
    if word.endswith("sses"):
        return word[:-2]
    if word.endswith("ies") and len(word) > 4:
        return word[:-3] + "y"
    if word.endswith("s") and not word.endswith("ss") and len(word) > 2:
        return word[:-1]
    return word


def _the_answer_range(above):
    rules = []
    for found in A_RANGE_WITH_A_UNIT.finditer(above):
        low = _amount(found.group("lo").lower())
        high = _amount(found.group("hi").lower())
        if not low or not high or low <= 0 or high <= 0:
            continue
        if high < low:
            low, high = high, low
        rules.append((found.start(), low, high, found.group("unit").lower(),
                      found.group("period")))
    for found in A_SINGLE_RULE.finditer(above):
        value = _amount(found.group("num").lower())
        if not value or value <= 0:
            continue
        rules.append((found.start(), value, value, found.group("unit").lower(),
                      found.group("period")))
    if not rules:
        return None
    _, low, high, unit, period = min(rules, key=lambda rule: rule[0])
    return (low, high, unit,
            _the_rule_said(low, None if low == high else high, unit, period))


def _the_rule_said(low, high, unit, period):
    figure = "%s to %s" % (_fmt(low), _fmt(high)) if high is not None else _fmt(low)
    said = "%s %s" % (figure, UNIT_SAID.get(str(unit).lower(), str(unit).lower()))
    when = PERIOD_NAMED.get(str(period or "").lower())
    return said + (" " + when if when else "")


def _the_family(unit):
    for pattern, family in UNIT_IS:
        if pattern.search(unit):
            return family
    return ""


def the_figure_against_the_answer(clean, memory):
    line = " ".join(str(clean or "").lower().split())
    if not line or NOT_A_UNIT_ITSELF.search(line) or AN_AGE.search(line):
        return None
    if not ABOUT_A_FIGURE.search(line):
        return None
    alone = A_FIGURE_ALONE.match(line)
    if alone is None:
        return None
    figure = _amount(alone.group("num"))
    if not figure or figure <= 0 or figure > 500:
        return None
    reading = memory.get("understood") if isinstance(memory, dict) else None
    if isinstance(reading, dict) and "maths" in (reading.get("asks") or ()):
        return None
    above = " ".join(str(last_bot(memory) or "").split())
    if not above:
        return None
    named = _the_answer_range(above)
    if not named:
        return None
    low, high, unit, said = named
    family = _the_family(unit)
    said_unit = UNIT_SAID.get(unit, unit)
    their_unit = (alone.group("what") or "").lower()
    if their_unit and (_the_family(their_unit) != family or not family):
        return None
    if figure * TEN_TIMES < low or figure > high * TEN_TIMES:
        return None
    figure_said = _fmt(figure)
    said_unit = _the_unit_of_one(said_unit) if figure == 1 else said_unit
    if figure < low:
        step = STEPS.get(family, A_STEP_EITHER_WAY)["below"]
        reply = pick(FIGURE_BELOW, memory, clean).format(
            figure=figure_said, unit=said_unit, range=said, step=step)
    elif figure > high:
        step = STEPS.get(family, A_STEP_EITHER_WAY)["above"]
        reply = pick(FIGURE_ABOVE, memory, clean).format(
            figure=figure_said, unit=said_unit, range=said, step=step)
    else:
        reply = pick(FIGURE_INSIDE, memory, clean).format(
            figure=figure_said, unit=said_unit, range=said)
    return reply[:1].upper() + reply[1:]
