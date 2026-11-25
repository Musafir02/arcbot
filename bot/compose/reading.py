import re

from ..memory import topics as _topics
from . import verdict as _verdict


NUMBER = re.compile(r"(?<![\w.,])(-?\d+(?:\.\d+)?)(?!\d|[.,]\d)")
UNIT = re.compile(r"(?:\d\s*)?(bar|bars|psi|c|f|celsius|centigrade|degrees|deg|mm|cm|kg|litres?"
                  r"|liters?|ml|watts?|volts?|hours?|hrs?|days?|weeks?|months?|years?|%)\b")
RANGE = re.compile(r"(?:between\s+)?(-?\d+(?:\.\d+)?)\s*(?:and|to|--|-|\u2013)\s*(-?\d+(?:\.\d+)?)"
                   r"\s*([a-z%]{1,10})?\b", re.IGNORECASE)
MEASURED = frozenset(("bar", "bars", "psi", "c", "f", "celsius", "centigrade", "degrees", "deg",
                      "mm", "cm", "kg", "litre", "litres", "liter", "liters", "ml", "watt",
                      "watts", "volt", "volts", "%"))
CARRIED = frozenset((
    "i", "im", "it", "its", "it's", "the", "my", "we", "is", "was", "were", "are", "be", "been",
    "says", "say", "said", "reads", "read", "shows", "shown", "showing", "gives", "gave", "gets",
    "has", "have", "had", "at", "about", "around", "roughly", "now", "still", "only", "just",
    "currently", "currently", "down", "up", "to", "of", "on", "in", "a", "an", "and", "but",
    "actually", "today", "tonight", "this", "morning", "afternoon", "evening", "gauge", "dial",
    "meter", "thermometer", "display", "screen", "number", "reading", "there", "that", "then",
    "so", "or", "they", "she", "he", "here", "sitting", "sits", "hovering", "by", "from", "door",
    "shelf", "fridge", "freezer", "boiler", "pressure", "temp", "temperature", "room", "house",
    "car", "tyre", "tyres", "tire", "tires", "oven", "probe", "water", "bar", "bars",
    "psi", "c", "f", "deg", "degree", "degrees", "centigrade", "celsius", "mm", "cm", "kg",
    "litre", "litres", "ml", "watt", "watts", "volt", "volts",
))
QUESTION = re.compile(r"\?|\b(?:should|shall|is it|is that|do i|does it|what|why|how|which|"
                      r"when|where|would|could|can)\b")


def _number(clean):
    if QUESTION.search(clean):
        return None
    found = NUMBER.findall(clean)
    if len(found) != 1:
        return None
    words = re.findall(r"[a-z']+", clean)
    if not words:
        return None
    for word in words:
        if word not in CARRIED:
            return None
    unit = UNIT.search(clean)
    return float(found[0]), (unit.group(1) if unit else "")


def _range(said):
    for found in RANGE.finditer(str(said or "")):
        low, high, unit = found.group(1), found.group(2), (found.group(3) or "").lower()
        if unit in MEASURED:
            low, high = float(low), float(high)
            if low == high:
                continue
            return (low, high, unit) if low < high else (high, low, unit)
    return None


def _say(value):
    return ("%g" % value)


def _unit(unit):
    if not unit:
        return ""
    if unit in ("c", "celsius", "centigrade"):
        return "C"
    if unit == "f":
        return "F"
    if unit in ("deg", "degree", "degrees"):
        return " degrees"
    return " " + unit


NUMBER_WORDS = {
    "one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7, "eight": 8,
    "nine": 9, "ten": 10, "eleven": 11, "twelve": 12, "thirteen": 13, "fourteen": 14,
    "fifteen": 15, "sixteen": 16, "seventeen": 17, "eighteen": 18, "nineteen": 19,
    "twenty": 20, "thirty": 30, "forty": 40, "fifty": 50, "sixty": 60, "seventy": 70,
    "eighty": 80, "ninety": 90,
}
WORD_NUMBERS = "|".join(sorted(NUMBER_WORDS, key=len, reverse=True))
WORD_RANGE = re.compile(r"(?:between\s+)?\b(" + WORD_NUMBERS + r")\b\s*"
                        r"(?:and|to|\u2013|-)\s*(" + WORD_NUMBERS + r")\b"
                        r"\s*([a-z%]{1,10})?\b", re.I)


def _word_number(word):
    text = str(word or "").lower()
    return float(NUMBER_WORDS[text]) if text in NUMBER_WORDS else None


PLURALS = {"hour": "hours", "minute": "minutes", "day": "days", "week": "weeks",
           "month": "months", "year": "years", "mile": "miles", "litre": "litres",
           "liter": "liters", "gram": "grams", "calorie": "calories", "step": "steps",
           "hr": "hrs", "min": "mins"}


def _plural(unit, high):
    if high is None or high <= 1:
        return unit
    return PLURALS.get(unit, unit)


STOP_AFTER = frozenset((
    "for", "of", "a", "an", "the", "in", "to", "and", "or", "at", "on", "with", "but",
    "so", "if", "when", "which", "that", "is", "are", "it", "you", "we", "they", "per",
    "each", "roughly", "about", "around", "plus", "max", "maximum", "minimum", "more",
    "less", "up", "down", "off", "out", "from", "by", "as", "than", "then", "there",
    "this", "these", "those", "his", "her", "their", "your", "my", "our", "its",
))


def _usual_unit(text, before=None):
    counts = {}
    for found in re.finditer(r"\b" + DOUBT_UNIT.pattern, str(text or "").lower()):
        if before is not None and found.start() > before:
            continue
        unit = UNIT_ALIAS.get(found.group(1), found.group(1))
        if unit and unit not in MONEY_WORDS:
            counts[unit] = counts.get(unit, 0) + 1
    if not counts:
        return ""
    return max(counts, key=lambda unit: counts[unit])


def _add_measured(spans, low, high, unit, usual, at=None, matched=""):
    if low is None or high is None:
        return
    if unit not in DOUBT_UNITS:
        unit = usual if usual in DOUBT_UNITS else ""
    if not unit:
        return
    if low == high:
        return
    low, high = min(low, high), max(low, high)
    span = {"low": low, "high": high, "mark": "", "money": False, "unit": unit,
            "text": "%s to %s%s" % (_say(low), _say(high), _unit(_plural(unit, high)))}
    if at is not None:
        span["at"] = at
        span["end"] = at + len(matched) if matched else at
    spans.append(span)


def _same_measure(left, right):
    warm = frozenset(("c", "celsius", "centigrade", "deg", "degree", "degrees"))
    cold = frozenset(("f", "fahrenheit"))
    span = frozenset(("deg", "degree", "degrees"))
    for group in (warm, cold, span):
        if left in group and right in group:
            return True
    return left[:3] == right[:3]


def _where(value, low, high, unit):
    if value < low:
        return "below"
    if value > high:
        return "above"
    return "inside"


def _step(said):
    try:
        return _verdict._step(said)
    except Exception:
        return None


SHORT = 6


def _said(memory, clean):
    text = _topics.entry_answer(memory, clean)
    if text:
        return str(text)
    turns = memory.get("turns")
    if not isinstance(turns, list) or not turns:
        return ""
    last = turns[-1] if isinstance(turns[-1], dict) else {}
    if last.get("module") != "answers":
        return ""
    if len(re.findall(r"[a-z']+", clean)) > SHORT:
        return ""
    said = str(last.get("bot") or "")
    record = memory.get("entry_answer") or {}
    kept = str((record or {}).get("text") or "")
    if kept and not (" ".join(kept.lower().split()[:6]) in " ".join(said.lower().split())):
        return ""
    return said


AN_AGE = re.compile(
    r"^(?:i'?m|im|i am|ive|i've|i just turned|i turned)\s+\d{1,3}"
    r"(?:\s*(?:years?|yrs?)(?:\s+old)?)?(?:\s+(?:now|this year))?\s*[.!]?$", re.I)



LEADING = ("and", "so", "but", "ok", "okay", "alright", "well", "hmm", "umm", "er")
ASKS = frozenset(("is", "was", "were", "are", "would", "will", "does", "do", "did", "should"))
SUBJECTS = ("that", "this", "it", "there", "they", "those")
MONEY_DOUBTS = frozenset((
    "a good price", "a fair price", "a good deal", "expensive", "cheap", "steep",
    "on the high side", "on the low side", "about the going rate", "the going rate",
))
QUANTITY_WORDS = frozenset((
    "a lot", "much", "too much", "too high", "too low", "too little", "about right",
    "about average", "enough", "a good price", "a fair price", "a good deal", "expensive",
    "cheap", "steep", "on the high side", "on the low side", "over the top",
    "about the going rate", "the going rate",
    "average", "above average", "below average",
    "too long", "too short",
))
TIME_DOUBT = frozenset(("too long", "too short"))
DOUBT_WORDS = QUANTITY_WORDS | frozenset(("normal", "reasonable", "ok", "okay", "fine", "fair",
                                          "right"))
BARE_DOUBTS = QUANTITY_WORDS - {"much", "about average"}
WORD_ALIAS = {
    "too expensive": "expensive", "too dear": "expensive", "too pricey": "expensive",
    "too cheap": "cheap", "a bit much": "too much", "bit much": "too much",
    "a bit steep": "steep", "a bit dear": "expensive", "a bit pricey": "expensive",
    "a bit expensive": "expensive", "quite a lot": "a lot", "loads": "a lot",
    "loads of money": "a lot",
    "overpriced": "expensive", "pricey": "expensive", "dear": "expensive",
    "a rip off": "expensive", "rip off": "expensive", "ripoff": "expensive",
    "a ripoff": "expensive", "ripped off": "expensive", "ripping me off": "expensive",
    "get ripped off": "expensive", "got ripped off": "expensive", "i get ripped off": "expensive",
    "i got ripped off": "expensive", "i was ripped off": "expensive",
    "i am being ripped off": "expensive", "overcharged": "expensive",
    "overcharging me": "expensive", "i was overcharged": "expensive",
    "been overcharged": "expensive", "get overcharged": "expensive",
    "get done": "expensive", "i got done": "expensive", "overpaying": "expensive",
    "paying too much": "too much", "over the odds": "expensive", "a con": "expensive",
    "excessive": "too much", "unreasonable": "too much", "exorbitant": "too much",
    "having a laugh": "expensive", "taking the mick": "expensive", "having me on": "expensive",
    "daylight robbery": "expensive", "a joke": "expensive",
    "how does that compare": "about right", "in the ballpark": "about right",
    "in line": "about average", "in line with what youd expect": "about average",
    "in line with what youd pay": "about average", "the normal price": "about average",
    "normal price": "about average", "a normal price": "about average",
    "price about right": "about right", "what it should cost": "about right",
    "sound about right": "about right", "sounds about right": "about right",
    "look about right": "about right", "looks about right": "about right",
    "cost that much": "too much", "that much": "too much", "this much": "too much",
    "acceptable": "about right", "alright": "about right", "all right": "about right",
    "sensible": "about right", "much good": "about right", "fair enough": "about right",
    "high": "too high", "low": "too low",
}
TAILS = ("really", "then", "though", "to me", "i think", "for that", "for it", "for one",
         "to pay", "to spend",
         "of money", "of it", "like that", "in total", "altogether", "for what it is",
         "for what they are", "for the size of it")
TAG_ASK = re.compile(
    r"[\s,]+(?:is(?:nt|n't)?\s+(?:it|that|this|they)|innit|aint\s+it|eh|"
    r"dont\s+(?:you|ya)\s+think|do\s+you\s+think|wouldnt\s+you\s+say)[\s?!.]*$")
FOR_THE_THING = re.compile(
    r"\s+(?:for|on)\s+(?P<thing>(?:(?:a|an|the|my|our) )?[a-z][a-z' -]{1,40})$", re.I)
FOR_THE_ARTICLE = re.compile(r"^(?:a|an|the|my|our) ", re.I)
POINTING_AT_SOMETHING = frozenset((
    "one", "ones", "them", "it", "that", "this", "those", "these", "same",
))
POINTING_ONE = re.compile(r"\b(?:one|ones)$")
FIGURE = re.compile(r"(?:(?P<mark>[£$€])\s?)?(?P<number>\d[\d,]*(?:\.\d+)?)")
DOUBT_UNITS = frozenset((
    "bar", "bars", "psi", "c", "f", "celsius", "centigrade", "degrees", "deg", "mm", "cm", "kg",
    "g", "grams", "litre", "litres", "liter", "liters", "ml", "watt", "watts", "volt", "volts",
    "%", "hour", "hours", "hr", "hrs", "minute", "minutes", "min", "mins", "day", "days",
    "week", "weeks", "month", "months", "year", "years", "mile", "miles", "km", "kcal",
    "calories", "steps", "degrees",
))
PLACES_A_FIGURE = QUANTITY_WORDS - {"enough"}

A_GAUGE_UNIT = frozenset((
    "c", "f", "celsius", "centigrade", "deg", "degree", "degrees", "bar", "bars", "psi"))

PER_UNIT = re.compile(r"(?:an?|per|each)\s+(?=(?:bar|psi|degrees?|hours?|hrs?|minutes?|mins?|"
                        r"days?|weeks?|months?|years?|miles?|km|kilos?|kg|litres?|steps)\b)")
DOUBT_UNIT = re.compile(
    r"(bar|bars|psi|c|f|celsius|centigrade|degrees|deg|mm|cm|kg|kilos?|kilograms?|grams?|g|"
    r"stone|stones|lb|lbs|litres?|liters?|ml|pints?|watts?|volts?|%|hours?|hrs?|minutes?|mins?"
    r"|days?|weeks?|months?|years?|miles?|km|k|kcal|calories?|steps|pounds?|quid|dollars?|"
    r"euros?|bucks?|pence)\b")
UNIT_ALIAS = {"kilo": "kg", "kilos": "kg", "kilogram": "kg", "kilograms": "kg", "k": "km",
              "stone": "stone", "stones": "stone", "lb": "lb", "lbs": "lb", "pint": "pints"}
MONEY_WORDS = frozenset(("pound", "pounds", "quid", "dollar", "dollars", "euro", "euros",
                         "buck", "bucks", "pence"))
MONEY_RANGE = re.compile(
    r"(?:(?P<mark>[£$€])\s?)?(?P<low>\d[\d,]*(?:\.\d+)?)\s*"
    r"(?:to|and|\u2013|-|--)\s*(?:(?P<mark2>[£$€])\s?)?(?P<high>\d[\d,]*(?:\.\d+)?)"
    r"\s*(?P<word>" + "|".join(sorted(MONEY_WORDS)) + r")?\b")
YEAR = 1900
NEXT_YEAR = 2100


def _the_figure_in_the_doubt(rest):
    found = FIGURE.match(rest)
    if not found:
        return None, False, "", rest, False
    value = float(found.group("number").replace(",", ""))
    rest = rest[found.end():].strip()
    unit = ""
    rate = bool(PER_UNIT.match(rest))
    if rate:
        rest = rest[PER_UNIT.match(rest).end():].strip()
    measured = DOUBT_UNIT.match(rest)
    if measured:
        unit = measured.group(1).lower()
        unit = UNIT_ALIAS.get(unit, unit)
        rest = rest[measured.end():].strip()
    money = bool(found.group("mark"))
    if unit in MONEY_WORDS:
        money, unit, rate = True, "", False
    return value, money, unit, rest, rate


def _doubt(text):
    line = " ".join(str(text or "").lower().split()).strip(" ?!.,;")
    line = re.sub(r"^(?:(?:good )?(?:hi|hiya|hey|hello|morning|afternoon|evening|yo)\b[ ,!.]*)+",
                  "", line)
    line = re.sub(r"^(?:(?:and|so|but|ok|okay|alright|well|hmm|umm|er)[ ,]+)+", "", line)
    line = TAG_ASK.sub("", line).strip(" ?!.,;")
    impression = re.match(r"(?P<figure>[£$€]?\s?\d[\d,]*(?:\.\d+)?)\s+"
                          r"(?:seems|seemed|feels|felt|looks|sounds)\s+(?P<rest>\S.*)$", line)
    if impression:
        line = "is %s %s" % (impression.group("figure").replace(" ", ""),
                             impression.group("rest").strip())
    turned = re.match(r"(?P<figure>[£$€]?\s?\d[\d,]*(?:\.\d+)?)\s*(?:pounds?|quid|euros?|"
                      r"dollars?)?\s*(?:for\s+(?!a\s+(?:day|week|month|year|hour)\b)"
                      r"(?P<thing>[a-z][\w' ]{0,40}?))?\s*[-,]?\s*(?:is|was|would)\s+"
                      r"(?:that|this|it)\s+(?P<word>a lot|too much|expensive|reasonable|ok|okay|"
                      r"alright|fine|fair|about right|steep|dear|pricey|cheap)\b", line)
    if turned:
        thing = (turned.group("thing") or "").strip()
        line = "is %s %s%s" % (turned.group("figure").replace(" ", ""), turned.group("word"),
                               (" for " + thing) if thing else "")
    opinion = re.search(r"(?P<figure>[£$€]?\s?\d[\d,]*(?:\.\d+)?)(?P<between>[^0-9]{0,24}?)"
                        r"\b(?:seems|seemed|feels|felt|looks|sounds)\s+(?P<word>"
                        r"high|low|steep|expensive|cheap|dear|pricey|a lot|too much|too high|"
                        r"too low|about right|about average|a rip off|loads)\b", line)
    if opinion:
        word = WORD_ALIAS.get(opinion.group("word"), opinion.group("word"))
        value = float(opinion.group("figure").replace(",", "").replace("£", "")
                      .replace("$", "").replace("€", "").strip())
        money = bool(re.search(r"[£$€]", opinion.group("figure")))
        if word in DOUBT_WORDS and not (
                value is not None and YEAR <= value <= NEXT_YEAR and value % 100
                and not money):
            return {"word": word, "value": value, "money": money, "unit": "", "subject": "",
                    "rate": False}
    verb = re.match(r"(?:is|was|were|are|would|will|does|do|did|should|isn'?t|isnt|aren'?t|arent|"
                    r"that's|that is|thats|it's|it is|its|this is|am i being|am i|are they|"
                    r"are we being|have i been|did i)\b", line)
    if not verb:
        bare = WORD_ALIAS.get(line, line)
        if bare in BARE_DOUBTS:
            return {"word": bare, "value": None, "money": False, "unit": "", "subject": "",
                    "rate": False}
        return None
    rest = line[verb.end():].strip()
    value, money, unit = None, False, ""
    stated = verb.group(0) in ("that's", "that is", "thats", "it's", "it is", "its", "this is",
                               "am i being", "am i", "are they", "are we being", "have i been")
    if stated or re.match(r"(?:that|this|it|there|they|those)\b", rest):
        rest = re.sub(r"^(?:that|this|it|there|they|those)\b", "", rest).strip()
        value, money, unit, rest, rate = _the_figure_in_the_doubt(rest) if stated else (
            None, False, "", rest, False)
    else:
        value, money, unit, rest, rate = _the_figure_in_the_doubt(rest)
    rest = re.sub(r"^(?:be|being|really|actually|roughly)\s+", "", rest).strip()
    changed = True
    while changed and rest:
        changed = False
        for tail in TAILS:
            if rest.endswith(" " + tail):
                rest = rest[: -len(tail)].strip()
                changed = True
    subject = ""
    for_thing = FOR_THE_THING.search(rest)
    if for_thing and value is not None:
        thing = " ".join(for_thing.group("thing").strip().lower().split())
        short_thing = FOR_THE_ARTICLE.sub("", thing)
        if short_thing not in POINTING_AT_SOMETHING and not POINTING_ONE.search(short_thing):
            subject = thing
        rest = rest[: for_thing.start()].strip()
    rest = WORD_ALIAS.get(rest, rest)
    if rest not in DOUBT_WORDS:
        return None
    if (value is not None and YEAR <= value <= NEXT_YEAR and value % 100
            and not money and not unit):
        return None
    return {"word": rest, "value": value, "money": money, "unit": unit,
            "subject": subject, "rate": rate}


def _doubt_ranges(said):
    text = str(said or "")
    money, measured = [], []
    for found in MONEY_RANGE.finditer(text):
        if not (found.group("mark") or found.group("mark2") or found.group("word")):
            continue
        low = float(found.group("low").replace(",", ""))
        high = float(found.group("high").replace(",", ""))
        if low == high:
            continue
        low, high = min(low, high), max(low, high)
        mark = found.group("mark") or found.group("mark2") or "£"
        money.append({"low": low, "high": high, "mark": mark, "money": True, "unit": "",
                      "at": found.start(),
                      "text": "%s to %s" % (_money(low, mark), _money(high, mark))})
    for found in RANGE.finditer(text):
        unit = (found.group(3) or "").lower()
        if unit not in DOUBT_UNITS:
            continue
        low = float(found.group(1).replace(",", ""))
        high = float(found.group(2).replace(",", ""))
        if low == high:
            continue
        low, high = min(low, high), max(low, high)
        measured.append({"low": low, "high": high, "mark": "", "money": False, "unit": unit,
                         "at": found.start(), "end": found.end(),
                         "text": "%s to %s%s" % (_say(low), _say(high), _unit(unit))})
    for found in WORD_RANGE.finditer(text):
        _add_measured(measured, _word_number(found.group(1)), _word_number(found.group(2)),
                      (found.group(3) or "").lower(), _usual_unit(text, found.start()),
                      at=found.start(), matched=found.group(0))
    measured = [span for span in measured if not _an_age(text, span)]
    measured.sort(key=lambda span: span.get("at", 0))
    return money, measured


AN_AGE_AFTER = re.compile(r"^[\s,|\-]{0,3}(?:years?|months?|weeks?|days?)?\s*olds?\b", re.I)


def _an_age(text, span):
    end = span.get("end")
    if not isinstance(end, int):
        return False
    return bool(AN_AGE_AFTER.match(text[end:end + 24]))


def _money(value, mark="£"):
    body = "{:,}".format(int(value)) if float(value).is_integer() else "{:,.2f}".format(value)
    return "%s%s" % (mark, body)


TOO_MUCH_WORDS = frozenset(("a lot", "much", "too much", "too high", "expensive", "steep",
                            "over the top", "on the high side"))
ABOUT_RIGHT = (
    "That is about right - {span} is the usual.",
    "That sits inside the {span} that is usual for it.",
    "Right in the usual range: {span}.",
)
NOT_TOO_LITTLE = (
    "No, that is about right - {span} is the usual.",
    "No, you are inside it: the usual is {span}.",
)
NOT_TOO_MUCH = (
    "No, that is about right - {span} is the usual.",
    "No, that is fine: the usual is {span}.",
    "No - {span} is the usual, so you are inside it.",
)
ON_THE_HIGH_SIDE = (
    "That is on the high side: the usual is about {span}.",
    "Yes, a bit much - {span} is the usual.",
)
NOT_TOO_LONG = (
    "No - {span} is the usual, and that is under it.",
    "No, that is short of the usual {span}.",
)
NOT_TOO_LONG_INSIDE = (
    "No, that is inside the usual {span}.",
    "No - {span} is the usual, and that sits inside it.",
)
NOT_TOO_SHORT = (
    "No, that is not too short - {span} is the usual.",
    "No - {span} is the usual, so there is plenty of room there.",
)
ON_THE_LONG_SIDE = (
    "Yes, that is on the long side - the usual is {span}.",
    "Yes, that is longer than the usual {span}.",
)
ON_THE_SHORT_SIDE = (
    "Yes, that is on the short side - the usual is {span}.",
    "Yes, that is shorter than the usual {span}.",
)
ABOVE_THE_USUAL = (
    "No, that is on the high side: the usual is about {span}.",
    "No - {span} is the usual, so that is above it.",
)
ENOUGH = (
    "Yes, that is enough - the usual is {span}.",
    "That is plenty: the usual is {span}.",
)
ON_THE_LOW_SIDE = (
    "That is on the low side - the usual is about {span}.",
    "Yes, a bit low - {span} is the usual.",
)
THE_LOW_SIDE_FOUND = (
    "That is on the low side - the usual is about {span}.",
    "No, that is under the {span} that is usual.",
)
UNDER_THE_USUAL = (
    "That is a little short - the usual is {span}.",
    "No, that is under the {span} it needs.",
)
MORE_THAN_ENOUGH = (
    "Yes, more than enough - the usual is {span}.",
    "That is plenty: {span} is the usual.",
)


_SAME_JOB = re.compile(r"\b(?:if|when|with|unless|once|where|should)\b", re.IGNORECASE)


_A_RATE = re.compile(r"^\s*(?:a|an|per|each)\s+(?:day|hour|week|month|visit|year|sq\s?m)\b",
                     re.IGNORECASE)

_SAYS_NOTHING_ABOUT_THE_TIER = frozenset("""
a an the and or but if when with without for of in on at to from by as so also plus than then
is are was were be been being it its this that these those there here his her their your our my
one ones some any more most less much many about around roughly usually normally typically per
each over under near up down out off just only too very quite really still even
""".split())


def _they_named_the_tier(qualifier, mine):
    if not mine:
        return False
    spoken = set(re.findall(r"[a-z']+", str(mine).lower()))
    for word in re.findall(r"[a-z']+", str(qualifier or "").lower()):
        if len(word) < 3 or word.isdigit() or word in _SAYS_NOTHING_ABOUT_THE_TIER:
            continue
        if word in spoken or word.rstrip("s") in spoken:
            return True
    return False


def _the_range_for(value, spans, said, mine=""):
    if value is None or len(spans) < 2:
        return None
    if spans[0]["low"] <= value <= spans[0]["high"]:
        return None
    text = str(said)
    apart = []
    for place, span in enumerate(spans[1:], 1):
        before = text[spans[place - 1]["at"] + len(spans[place - 1]["text"]):span["at"]]
        end = span["at"] + len(span["text"])
        after = text[end:spans[place + 1]["at"] if place + 1 < len(spans) else len(text)]
        after = re.split(r"[.;:!?]| - |\band\b", after, 1)[0]
        if not (_SAME_JOB.search(before) or _SAME_JOB.search(after)):
            apart.append((span, before + " " + after))
    for span, qualifier in apart:
        if not span["low"] <= value <= span["high"]:
            continue
        if (span["high"] > spans[0]["high"] and not _they_named_the_tier(qualifier, mine)
                and not _A_RATE.match(text[spans[0]["at"] + len(spans[0]["text"]):])):
            continue
        return [span]
    return None


def _the_person_words(memory, line=""):
    words = [str(line or "")]
    turns = memory.get("turns") if isinstance(memory, dict) else None
    for turn in list(turns or [])[-3:]:
        if isinstance(turn, dict):
            words.append(str(turn.get("user") or ""))
    return " ".join(words).lower()


def _the_span(doubt, said, mine=""):
    money, measured = _doubt_ranges(said)
    if doubt["money"]:
        spans = _the_range_for(doubt["value"], money, said, mine) or money
    elif doubt["unit"]:
        spans = [span for span in measured if _same_measure(doubt["unit"], span["unit"])]
        if doubt.get("rate"):
            priced = [span for span in money if re.search(
                re.escape(span["text"]) + r"\s*(?:an?|per|each)?\s*"
                + re.escape(doubt["unit"]) + r"s?\b", said, re.IGNORECASE)]
            if priced:
                spans = priced
    else:
        measured = [span for span in measured if span["unit"] not in A_GAUGE_UNIT]
        both = sorted(money + measured, key=lambda span: span["at"])
        inside = [span for span in both if doubt["value"] is not None
                  and span["low"] <= doubt["value"] <= span["high"]]
        if inside and money and measured:
            spans = [inside[0]]
        else:
            spans = _the_range_for(doubt["value"], both, said, mine) or money or measured
        if not money and doubt["value"] is not None and spans and (
                doubt["value"] > spans[0]["high"] * 10
                or doubt["value"] * 10 < spans[0]["low"]):
            return None
    if not spans:
        return None
    if len({(span["low"], span["high"]) for span in spans}) > 1 and \
            doubt["value"] is not None and doubt["value"] * 2 < spans[0]["low"] and \
            not any(span["low"] <= doubt["value"] <= span["high"] for span in spans):
        return None
    if doubt["value"] is not None and len(spans) > 1:
        value = doubt["value"]
        if value > max(span["high"] for span in spans) or \
                value < min(span["low"] for span in spans):
            return min(spans, key=lambda span: max(span["low"] - value, value - span["high"],
                                                  0.0))
    return spans[0]


TOO_LITTLE_WORDS = frozenset(("too low", "too little", "cheap", "on the low side"))


def _the_side_asked(word):
    word = str(word or "").strip().lower()
    if word in TOO_MUCH_WORDS:
        return "high"
    if word in TOO_LITTLE_WORDS:
        return "low"
    return None


def _the_side_decides(options, doubt, value, low, high, low_side, found_side):
    if doubt["word"] == "enough" or doubt["word"] in TIME_DOUBT:
        return options
    asked = _the_side_asked(doubt["word"])
    if low <= value <= high:
        return NOT_TOO_LITTLE if asked == "low" else options
    if value < low:
        return low_side if asked == "low" else found_side
    return options


def _judged(doubt, said, mine=""):
    value = doubt["value"]
    if value is None:
        return None
    span = _the_span(doubt, said, mine)
    if span is None:
        return None
    low, high, span_text = span["low"], span["high"], span["text"]
    if doubt["word"] in TIME_DOUBT:
        long = doubt["word"] == "too long"
        if low <= value <= high:
            options = NOT_TOO_LONG_INSIDE if long else NOT_TOO_SHORT
        elif value > high:
            options = ON_THE_LONG_SIDE if long else NOT_TOO_SHORT
        else:
            options = NOT_TOO_LONG if long else ON_THE_SHORT_SIDE
    elif low <= value <= high:
        if doubt["word"] == "enough":
            options = ENOUGH
        elif doubt["word"] in TOO_MUCH_WORDS:
            options = NOT_TOO_MUCH
        else:
            options = ABOUT_RIGHT
    elif value > high:
        if doubt["word"] == "enough":
            options = MORE_THAN_ENOUGH
        elif doubt["word"] in TOO_MUCH_WORDS:
            options = ON_THE_HIGH_SIDE
        else:
            options = ABOVE_THE_USUAL
    else:
        options = UNDER_THE_USUAL if doubt["word"] == "enough" else ON_THE_LOW_SIDE
    options = _the_side_decides(options, doubt, value, low, high,
                                ON_THE_LOW_SIDE, THE_LOW_SIDE_FOUND)
    line = _verdict.pick(list(options), {"turns": [{"bot": span_text}]}, span_text)
    line = line.format(span=span_text, value=_money(value, span["mark"] or "£"))
    aside = _the_band_aside(said, span_text)
    if aside:
        line = _with_the_aside(line, span_text, aside)
    return line


_BUYS = re.compile(
    r"^(?:buys|gets you|gets|gets a|pays for|fits|covers|includes|holds|lasts|makes|gives|"
    r"comes to|is|are|will)\b", re.I)
_ASIDE_ENDS = re.compile(r"[,.;:()]|\s+\band\s+(?:£|\d)|\s+\u2014\s+|\s+-\s+|\s+but\s+", re.I)


def _the_band_aside(said, span_text):
    said = " ".join(str(said or "").split())
    if not said or not span_text:
        return ""
    found = said.find(span_text)
    if found < 0:
        return ""
    after = said[found + len(span_text):]
    end = _ASIDE_ENDS.search(after)
    clause = (after[:end.start()] if end else after).strip()
    if not clause or len(clause) > 70:
        return ""
    if not _BUYS.match(clause):
        return ""
    return clause.rstrip(" .,;:")


def _with_the_aside(line, span_text, aside):
    body = line.rstrip()
    if not body.endswith(span_text + "."):
        return line
    return body[:-1] + ", which " + aside + "."


LOOK_BACK = 3


SAME_LEAGUE = 100.0


DAYS_IN = {"minute": 1 / 1440.0, "min": 1 / 1440.0, "hour": 1 / 24.0, "hr": 1 / 24.0,
           "day": 1.0, "week": 7.0, "month": 30.0, "year": 365.0}


def _in_the_unit(value, unit, wanted):
    mine = DAYS_IN.get(str(unit or "").lower().rstrip("s"))
    theirs = DAYS_IN.get(str(wanted or "").lower().rstrip("s"))
    if mine is None or not theirs:
        return None
    return value * mine / theirs


def _a_stretch_of_time(unit):
    return str(unit or "").lower().rstrip("s") in DAYS_IN


THE_USUAL_NO = (
    "No - {span} is the usual, so it depends how long yours has been going on.",
    "No, that is the usual: {span}. How long has yours been going on?",
    "No - {span} is the normal spread, so say how long yours has lasted and I'll place it.",
)


def _the_usual_is_the_answer(doubt, said):
    if doubt.get("word") not in TIME_DOUBT:
        return None
    span = _the_span(doubt, said)
    if span is None or span.get("money") or not _a_stretch_of_time(span.get("unit")):
        return None
    return _verdict.pick([line.format(span=span["text"]) for line in THE_USUAL_NO],
                         {"turns": [{"bot": said}]}, span["text"])


A_WORD_FIGURE = re.compile(
    r"\b(" + WORD_NUMBERS + r"|a|an|couple|few)\s+(" + "|".join(
        sorted((re.escape(unit) for unit in DOUBT_UNITS), key=len, reverse=True)) + r")\b", re.I)
WORD_FIGURE_COUNTS = {"a": 1.0, "an": 1.0, "couple": 2.0, "few": 3.0}


def _a_word_figure(said):
    found = None
    for found in A_WORD_FIGURE.finditer(said or ""):
        pass
    if found is None:
        return None
    word = found.group(1).lower()
    value = _word_number(word)
    if value is None:
        value = WORD_FIGURE_COUNTS.get(word)
    if value is None:
        return None
    unit = UNIT_ALIAS.get(found.group(2).lower(), found.group(2).lower())
    return {"value": value, "money": False, "unit": unit}


def _the_last_figure_in(said):
    said = str(said or "")
    found = list(FIGURE.finditer(said))
    if found:
        figure = _the_figure_in(said, found[-1])
        if figure:
            return figure
    return _a_word_figure(said)


def _in_the_same_league(value, said):
    if value is None:
        return True
    money, measured = _doubt_ranges(said)
    spans = money or measured
    if not spans:
        return True
    return any(span["low"] <= value * SAME_LEAGUE and value <= span["high"] * SAME_LEAGUE
               for span in spans)


def _answer_before(memory, value=None):
    turns = memory.get("turns")
    if not isinstance(turns, list) or not turns:
        return "", -1
    elsewhere = ("", -1)
    for back in range(1, min(LOOK_BACK, len(turns)) + 1):
        turn = turns[-back] if isinstance(turns[-back], dict) else {}
        if turn.get("module") != "answers":
            continue
        said = str(turn.get("bot") or "")
        if said and any(found.group(3) or "" for found in RANGE.finditer(said)) or \
                MONEY_RANGE.search(said) or WORD_RANGE.search(said):
            if value is None or _in_the_same_league(value, said):
                return said, len(turns) - back
            if elsewhere[1] < 0:
                elsewhere = said, len(turns) - back
    if elsewhere[1] >= 0 or value is not None:
        return elsewhere
    for back in range(1, min(LOOK_BACK, len(turns)) + 1):
        turn = turns[-back] if isinstance(turns[-back], dict) else {}
        if turn.get("module") != "answers":
            continue
        said = str(turn.get("bot") or "")
        if _a_lone_price(said):
            return said, len(turns) - back
    return elsewhere


def _figure_since(memory, after, narrow=False):
    turns = memory.get("turns") or []
    said_before = ""
    if not narrow and 0 <= after < len(turns) and isinstance(turns[after], dict):
        said_before = str(turns[after].get("user") or "")
    if said_before:
        figure = _the_last_figure_in(said_before)
        if figure:
            return figure
    for turn in reversed(turns[after + 1:]):
        said = turn.get("user") if isinstance(turn, dict) else ""
        figure = _the_last_figure_in(said)
        if figure:
            return figure
    if not narrow and after >= 1 and isinstance(turns[after - 1], dict):
        figure = _the_last_figure_in(str(turns[after - 1].get("user") or ""))
        if figure:
            return figure
    return None


A_CLOCK_TIME_BEFORE = re.compile(
    r"\b(?:at|by|until|till|til|before|after|past)\s*$", re.I)
A_CLOCK_TIME_AFTER = re.compile(r"^\s*(?:am|pm|a\.m|p\.m|o'?clock)\b", re.I)


def _a_clock_time(said, found, value):
    if A_CLOCK_TIME_AFTER.match(said[found.end():]):
        return True
    return 0 < value <= 24 and bool(A_CLOCK_TIME_BEFORE.search(said[:found.start()]))


def _the_figure_in(said, found):
    value = float(found.group("number").replace(",", ""))
    money = bool(found.group("mark"))
    unit = ""
    measured = UNIT.match(said[found.end():].strip())
    if measured:
        unit = measured.group(1).lower()
    if YEAR <= value <= NEXT_YEAR and value % 100 and not money and not unit:
        return None
    if AN_AGE.match(said.strip().lower()):
        return None
    if not unit and not money and _a_clock_time(said, found, value):
        return None
    return {"value": value, "money": money, "unit": unit}


ASKS_FOR_A_PRICE = (
    "What were you quoted? {span} is the usual, and then I can say whether yours is fair.",
    "What price have you got? {span} is the usual for that, so I can tell you where you sit.",
)
ASKS_FOR_A_FIGURE = (
    "What figure have you got? The usual is {span}, and I'll say which side of it you are on.",
    "What is yours? {span} is the usual for it, so I can tell you where it lands.",
)
NO_PRICE_SAID = (
    "I didn't give you a price there, so I can't call it cheap or dear yet. Tell me the figure you "
    "have in mind and what it is for, and I'll say whether it is fair.",
    "There was no price in what I said, so there is nothing to weigh up yet. Give me the number "
    "and what it is for.",
    "None of that was money, so I can't tell you expensive or not yet. Give me the figure and what "
    "it is for, and I'll say whether it is fair.",
)
A_LONE_PRICE = re.compile(
    r"(?P<mark>[£$€])\s?(?P<amount>\d[\d,]*(?:\.\d+)?)"
    r"|\b(?P<amount2>\d[\d,]*(?:\.\d+)?)\s*(?P<word>" + "|".join(sorted(MONEY_WORDS)) + r")\b")
THE_PRICE_IT_GAVE = (
    "{span} was the only price in that, so there is nothing to call dear yet. What have you been "
    "quoted?",
    "That answer named {span} and no range, so cheap or dear needs a second price. What figure are "
    "you weighing up?",
    "{span} is the figure I gave - one price, no range - so tell me the number you have in mind "
    "and I'll say where it sits.",
)


def _a_lone_price(said):
    text = str(said or "")
    money, measured = _doubt_ranges(text)
    if money:
        return ""
    for found in A_LONE_PRICE.finditer(text):
        amount = found.group("amount") or found.group("amount2") or ""
        if not amount:
            continue
        try:
            value = float(amount.replace(",", ""))
        except ValueError:
            continue
        if value <= 0:
            continue
        word = (found.group("word") or "").lower()
        if not (found.group("mark") or word) and YEAR <= value <= NEXT_YEAR:
            continue
        return found.group(0).strip()
    return ""


A_RANGE_THAT_IS_NOT_A_PRICE = (
    "That was a range of {unit}, not a price: {span} is what it said, so cheap or dear does not "
    "come into it. If you are weighing up a figure, tell me it and what it is for.",
    "{span} is a usual range, not a price, so there is nothing there to call expensive. Give me "
    "the figure you are judging and I'll say where it sits.",
)
UNIT_WORDS = {
    "hour": "hours", "hours": "hours", "hr": "hours", "hrs": "hours",
    "minute": "minutes", "minutes": "minutes", "min": "minutes", "mins": "minutes",
    "day": "days", "days": "days", "week": "weeks", "weeks": "weeks",
    "month": "months", "months": "months", "year": "years", "years": "years",
    "mile": "miles", "miles": "miles", "km": "kilometres", "calories": "calories",
    "kcal": "calories", "steps": "steps", "g": "grams", "grams": "grams",
    "kg": "kilos", "litre": "litres", "litres": "litres", "liter": "litres",
    "liters": "litres", "ml": "millilitres",
}
THE_RANGE_ITSELF = (
    "That is the range itself: {span} is what it says, so nothing in it is out of the ordinary. If "
    "you have a figure of your own, tell me and I'll say where it sits.",
    "{span} is the usual, so that is the figure to hold next to yours. Give me your own and I'll "
    "place it on the range.",
    "Nothing there was out of the ordinary - {span} is the usual, and that is the figure I gave "
    "you. Tell me your own and I'll judge that one instead.",
)
BELOW_THE_RANGE = (
    "Under {span} would be low, so the bottom of that is what to aim for. Tell me your figure and "
    "I'll say how far under it is.",
    "{span} is the usual, so anything under it is on the low side. What is yours?",
)
ABOVE_THE_RANGE = (
    "Over {span} would be high, so anything at the top of it is fine. Tell me your figure and I'll "
    "say how far over it is.",
    "{span} is the usual, so anything above that is on the high side. What is yours?",
)
SAID_LOW = frozenset(("too low", "on the low side", "below average", "too little", "not enough",
                      "enough"))
SAID_HIGH = frozenset(("too high", "on the high side", "above average", "too much",
                       "over the top"))


def asks_for_the_figure(doubt, said):
    if doubt["word"] not in QUANTITY_WORDS:
        return None
    money, measured = _doubt_ranges(said)
    if doubt["word"] in MONEY_DOUBTS:
        spans = money
        if not spans:
            spoken = [span for span in measured if UNIT_WORDS.get(span.get("unit"))]
            if spoken:
                span = spoken[0]
                unit = UNIT_WORDS[span["unit"]]
                return _verdict.pick([line.format(span=span["text"], unit=unit)
                                      for line in A_RANGE_THAT_IS_NOT_A_PRICE],
                                     {"turns": [{"bot": said}]}, said)
            single = _a_lone_price(said)
            if single:
                return _verdict.pick([line.format(span=single) for line in THE_PRICE_IT_GAVE],
                                     {"turns": [{"bot": said}]}, said)
            if measured and (doubt["word"] in SAID_LOW or doubt["word"] in SAID_HIGH):
                span = measured[0]["text"]
                options = BELOW_THE_RANGE if doubt["word"] in SAID_LOW else ABOVE_THE_RANGE
                return _verdict.pick([line.format(span=span) for line in options],
                                     {"turns": [{"bot": said}]}, said)
            if measured:
                return None
            return _verdict.pick(list(NO_PRICE_SAID), {"turns": [{"bot": said}]}, said)
    else:
        spans = money or measured
    if not spans:
        return None
    span = spans[0]
    if span["money"]:
        options = ASKS_FOR_A_PRICE
    elif doubt["word"] in SAID_LOW:
        options = BELOW_THE_RANGE
    elif doubt["word"] in SAID_HIGH:
        options = ABOVE_THE_RANGE
    else:
        options = THE_RANGE_ITSELF
    return _verdict.pick([line.format(span=span["text"]) for line in options],
                         {"turns": [{"bot": said}]}, said)


def _doubt_and_answer(clean, memory):
    if not isinstance(memory, dict):
        return None
    doubt = _doubt(clean)
    if not doubt:
        return None
    said, at = _answer_before(memory)
    if not said:
        return None
    if doubt.get("subject") and not _the_answer_is_about(said, doubt["subject"]):
        return None
    return doubt, said, at


def _the_answer_is_about(said, subject):
    words = [word for word in re.findall(r"[a-z']+", _the_opening_sentence(said).lower())
             if len(word) >= 3]
    for word in re.findall(r"[a-z']+", str(subject or "").lower()):
        if len(word) < 3:
            continue
        for there in words:
            if word in there or there in word:
                return True
    return False


def _only_says_that(doubt):
    return doubt.get("word") not in QUANTITY_WORDS


def _the_usuals(subject):
    short = FOR_THE_ARTICLE.sub("", " ".join(str(subject or "").split()))
    if not short or len(short.split()) > 4:
        return ()
    try:
        from ..knowledge import lookup
    except Exception:
        return ()
    for question in ("how much does a %s cost" % short, "how much does %s cost" % short,
                     "how much is a %s" % short):
        try:
            found = lookup.find({"clean": question, "words": question.split()})
        except Exception:
            continue
        if found is None:
            continue
        reply = getattr(found, "reply", None)
        if callable(reply):
            try:
                reply = reply({}, {"clean": question, "words": question.split()})
            except Exception:
                continue
        money, _ = _doubt_ranges(_the_opening_sentence(reply))
        if money:
            return tuple(money)
    return ()


def _the_opening_sentence(reply):
    text = " ".join(str(reply or "").split())
    for mark in (". ", "! ", "? "):
        cut = text.find(mark)
        if cut > 0:
            text = text[:cut]
    return text


RIGHT_FOR_THE_THING = (
    "That is about right for {thing} - {span} is the usual.",
    "Yes, that is in the normal range: {span} is the usual for {thing}.",
)
HIGH_FOR_THE_THING = (
    "That is on the high side for {thing}: the usual is about {span}.",
    "Yes, a bit much for {thing} - {span} is the usual.",
)
LOW_FOR_THE_THING = (
    "That is on the low side for {thing} - the usual is about {span}.",
    "Yes, a bit low for {thing} - {span} is the usual.",
)
ENOUGH_FOR_THE_THING = (
    "Yes, that is enough for {thing} - the usual is {span}.",
    "That is plenty for {thing}: {span} is the usual.",
)
SHORT_FOR_THE_THING = (
    "That is a little short for {thing} - the usual is {span}.",
    "No, that is under the {span} it needs for {thing}.",
)
THE_LOW_SIDE_FOUND_FOR_THE_THING = (
    "That is on the low side for {thing} - the usual is about {span}.",
    "No, that is under the {span} that {thing} usually costs.",
)


def _judged_on_its_subject(doubt):
    if not doubt or doubt.get("value") is None:
        return None
    if not doubt.get("subject"):
        return None
    if doubt.get("unit"):
        return None
    spans = _the_usuals(doubt["subject"])
    if not spans:
        return None
    span = spans[0]
    value, low, high = doubt["value"], span["low"], span["high"]
    enough = doubt["word"] == "enough"
    if low <= value <= high:
        options = ENOUGH_FOR_THE_THING if enough else RIGHT_FOR_THE_THING
    elif value > high:
        options = ENOUGH_FOR_THE_THING if enough else HIGH_FOR_THE_THING
    else:
        options = SHORT_FOR_THE_THING if enough else LOW_FOR_THE_THING
    options = _the_side_decides(options, doubt, value, low, high,
                                LOW_FOR_THE_THING, THE_LOW_SIDE_FOUND_FOR_THE_THING)
    return _verdict.pick([line.format(thing=doubt["subject"], span=span["text"])
                          for line in options], {"turns": [{"bot": span["text"]}]},
                         span["text"])


_POINTS_AT_IT = frozenset("""
    one ones it that this these those them they him her he she thing things
""".split())


def _the_thing_the_chat_is_on(memory):
    understood = (memory or {}).get("understood") if isinstance(memory, dict) else None
    if not isinstance(understood, dict):
        return ""
    ref = understood.get("ref")
    if isinstance(ref, dict):
        for key in ("it", "that", "they", "them"):
            thing = str(ref.get(key) or "").strip()
            if thing and thing.lower() not in _POINTS_AT_IT:
                return thing if FOR_THE_ARTICLE.match(thing) else "a " + thing
    return ""


def _the_doubt_with_its_thing(clean, memory):
    doubt = _doubt(clean)
    if not doubt or doubt.get("value") is None or not doubt.get("money"):
        return doubt
    subject = str(doubt.get("subject") or "").strip()
    if subject and subject.lower() not in _POINTS_AT_IT:
        return doubt
    thing = _the_thing_the_chat_is_on(memory)
    if thing:
        doubt = dict(doubt, subject=thing)
    return doubt


def _its_own_subject_judges_it(clean, memory):
    doubt = _the_doubt_with_its_thing(clean, memory)
    if not doubt or not doubt.get("subject") or doubt.get("value") is None:
        return False
    said, _ = _answer_before(memory if isinstance(memory, dict) else {})
    if said and _the_answer_is_about(said, doubt["subject"]):
        return False
    if _a_card_answers(str(clean or "")):
        return False
    return _judged_on_its_subject(doubt) is not None


def _a_card_answers(text):
    try:
        from ..knowledge import lookup
    except Exception:
        return False
    try:
        return lookup.find({"clean": text, "words": text.split()}) is not None
    except Exception:
        return False


def judges_a_figure(clean, memory):
    if not isinstance(memory, dict):
        return False
    return (judges_the_figure_on_the_table(clean, memory)
            or _its_own_subject_judges_it(clean, memory))


def judges_the_figure_on_the_table(clean, memory):
    return _the_verdict_for_the_table(clean, memory) is not None


A_RATE_OF_THEIRS = re.compile(
    r"\b(?:\d+|one|two|three|four|five|six|seven|eight|nine|ten)\s+"
    r"(?:times?|x|runs?|sessions?|workouts?)\s+(?:a|per|each|every)\s+(?:day|week|month|year)\b"
    r"|\btwice\s+(?:a|per|each|every)\s+(?:day|week|month|year)\b", re.I)


def _a_rate_of_theirs(memory):
    turns = memory.get("turns") if isinstance(memory, dict) else None
    if not isinstance(turns, list) or not turns:
        return False
    for turn in reversed(turns[-LOOK_BACK:]):
        said = turn.get("user") if isinstance(turn, dict) else ""
        if A_RATE_OF_THEIRS.search(str(said or "")):
            return True
    return False


def _the_verdict_for_the_table(clean, memory):
    read = _doubt_and_answer(clean, memory)
    if not read:
        return None
    doubt, said, at = read
    if doubt["value"] is None and doubt.get("word") in PLACES_A_FIGURE:
        held = _figure_since(memory, at, narrow=_only_says_that(doubt))
        if held and held["unit"]:
            figured = _figure_of_the_answer(memory, at)
            if figured:
                doubt = dict(doubt, **figured)
    if doubt["value"] is None:
        before = _figure_since(memory, at, narrow=_only_says_that(doubt))
        if not before:
            if doubt["word"] in MONEY_DOUBTS:
                asked = asks_for_the_figure(doubt, said)
                if asked:
                    return asked
            return _the_usual_is_the_answer(doubt, said)
        if before["unit"] and doubt["word"] in TIME_DOUBT:
            span = _the_span(doubt, said)
            converted = _in_the_unit(before["value"], before["unit"],
                                     span.get("unit") if span else "")
            if converted is not None:
                return _judged(dict(doubt, value=converted, money=False,
                                    unit=span.get("unit"), rate=False), said)
        if before["unit"]:
            return None
        doubt = dict(doubt, **before)
    moved = _the_answer_about_this_figure(doubt, memory, at)
    if moved is None:
        return None
    said, at = moved
    if not doubt.get("unit") and _a_rate_of_theirs(memory):
        span = _the_span(doubt, said)
        if span is not None and _a_stretch_of_time(span.get("unit")):
            return None
    mine = _judged(doubt, said, _the_person_words(memory, clean))
    if mine is None:
        return None
    return _the_price_verdict(clean, memory) or mine


def _the_price_verdict(clean, memory):
    try:
        from ..memory import price as a_price
    except Exception:
        return None
    try:
        said = a_price.judged(clean, memory) or None
    except Exception:
        return None
    if not said or not _the_store_found_it_outside(clean, memory, a_price):
        return None
    return said


def _the_store_found_it_outside(clean, memory, a_price):
    try:
        mine, _said = a_price._the_price_they_mean(clean, memory)
        if not mine:
            return True
        answers = a_price._answers_in(memory.get("turns"))
        aim = a_price._the_range_that_is_about_it(
            answers, mine, a_price._the_period_they_said(clean, memory))
        if aim is None:
            return True
        return not aim[0] <= mine <= aim[1]
    except Exception:
        return True


def reply_to_a_doubt(clean, memory):
    verdict = _the_verdict_for_the_table(clean, memory)
    if verdict:
        return verdict
    read = _doubt_and_answer(clean, memory)
    if not read:
        if not _its_own_subject_judges_it(clean, memory):
            return None
        return _judged_on_its_subject(_the_doubt_with_its_thing(clean, memory))
    doubt, said, at = read
    if doubt["value"] is not None:
        return None
    before = _figure_since(memory, at, narrow=_only_says_that(doubt))
    if not before or before["unit"]:
        return asks_for_the_figure(doubt, said) if not before else None
    return None


def _the_answer_about_this_figure(doubt, memory, at):
    value = doubt.get("value")
    if value is None:
        return None
    said, found_at = _answer_before(memory, value)
    if not said:
        return None
    if found_at == at:
        return said, at
    again = _figure_since(memory, found_at, narrow=_only_says_that(doubt))
    if again:
        doubt.update(again)
    return said, found_at



THEIR_FIGURE = re.compile(
    r"(?:(?P<mark>[\u00a3$\u20ac])\s?)?(?P<number>\d[\d,]*(?:\.\d+)?)\s*(?:a|an|per|each)?\s*"
    r"(?P<unit>bar|bars|psi|hours?|hrs?|minutes?|mins?|days?|weeks?|months?|years?|miles?|km|"
    r"kilos?|kg|grams?|g|steps|calories?|kcal|litres?|liters?|ml|pints?|watts?|volts?|degrees?|"
    r"deg|pounds?|quid|dollars?|euros?|bucks?)\b", re.IGNORECASE)
THEIR_NUMBER = re.compile(r"(?:(?P<mark>[\u00a3$\u20ac])\s?)?(?P<number>\d[\d,]*(?:\.\d+)?)(?!\d)")
A_BILL = frozenset((
    "bill", "bills", "electricity", "gas", "water", "heating", "rent", "mortgage", "insurance",
    "subscription", "subscriptions", "mobile", "broadband", "wifi", "council", "tax", "paying",
    "pay", "paid", "pays", "cost", "costs", "costing", "quote", "quoted", "price", "priced",
    "charged", "charge", "charging", "fee", "fees", "fare", "fares", "deposit", "debit",
    "invoice", "loan", "instalments", "installments", "monthly", "annual", "saving", "savings",
    "spend", "spends", "spending", "spent", "budget", "budgeting", "shop", "shopping",
))
A_PERIOD = frozenset(("month", "months", "week", "weeks", "year", "years"))
A_MONEY_PHRASE = re.compile(
    r"\b(?:the whole thing|the whole lot|for the lot|all in|altogether|in total|all told|the lot)\b",
    re.IGNORECASE)
A_STRETCH = frozenset(("hour", "hours", "hr", "hrs", "minute", "minutes", "min", "mins"))
A_DISTANCE = frozenset(("mile", "miles", "km"))
def _figure_words(number, unit, mark=""):
    text = "%s%s" % (mark, number)
    if not unit:
        return text
    if unit in A_PERIOD and unit in ("month", "week", "year", "day"):
        return "%s a %s" % (text, unit)
    return text + _unit(unit)


A_PRICE_NEXT_TO = (
    "{said} is only high or low next to another figure for the same thing: what you were paying "
    "before, or what somebody else pays for it. What was it before?",
    "{said} needs a second figure beside it - your last one, or what a friend pays - before anyone "
    "can call it a lot. What is the other one?",
)
A_JOURNEY_IS_TIME = (
    "{said} is a real journey. Whether it is too far is about the time it takes you and what you "
    "want to be able to do at the other end - how long does it take?",
    "{said} comes down to the time rather than the miles: easy for one person, a long trip for "
    "another. How long does it take you?",
)
A_STRETCH_OF_TIME = (
    "{said} is only too long against the rest of the day. What else has to fit into it?",
    "{said} - whether that is too much depends on what else the same time has to hold. What else "
    "is in the day?",
)
THE_REST_IS_UNSURE = (
    "{said} is not something I can call a lot from here. What are you comparing it with?",
    "{said} - too much against what? Name the thing you are measuring it against and I will take "
    "it from there.",
)


A_PRICE_VERB = re.compile(
    r"\b(?:was|were|is|cost|costs|cost me|paid|pay|spent|spend|charged|comes to|came to|"
    r"set me back)\s+(?:me\s+|us\s+)?[\u00a3$\u20ac]?\d", re.IGNORECASE)


def _their_figure(memory, back=1):
    turns = memory.get("turns")
    if not isinstance(turns, list):
        return None
    seen = 0
    for turn in reversed(turns):
        if not isinstance(turn, dict):
            continue
        said = str(turn.get("user") or "")
        if not said:
            continue
        seen += 1
        if seen > back:
            break
        found = None
        for found in THEIR_FIGURE.finditer(said):
            pass
        if not found:
            words = set(re.findall(r"[a-z']+", said.lower()))
            if not (words & A_BILL) and not A_MONEY_PHRASE.search(said) and not re.search(
                    r"[\u00a3$\u20ac]", said) and not A_PRICE_VERB.search(said.lower()):
                continue
            for found in THEIR_NUMBER.finditer(said):
                pass
            if not found:
                continue
        value = float(found.group("number").replace(",", ""))
        unit = (found.groupdict().get("unit") or "").lower()
        if YEAR <= value <= NEXT_YEAR and not found.group("mark") and unit not in ("miles", "km"):
            continue
        if AN_AGE.match(said.strip().lower()) or re.search(r"\b(?:years?|yrs?|months?)\s+old\b",
                                                          said.lower()):
            continue
        words = set(re.findall(r"[a-z']+", said.lower()))
        money = bool(found.group("mark")) or unit in MONEY_WORDS or bool(words & A_BILL) or \
            bool(A_MONEY_PHRASE.search(said)) or (not unit and bool(A_PRICE_VERB.search(said.lower())))
        text = _figure_words(found.group("number"), unit, found.group("mark") or "")
        return value, unit, text, money
    return None


A_MONEY_WORD = re.compile(r"[\u00a3$\u20ac]|\b(?:money|quid|pounds?|dollars?|euros?|bucks?|"
                          r"cost|costs|price|prices|pay|paying|spend|spending|afford)\b", re.I)
BARE_CEILING = re.compile(
    r"^(?:and |so |ok(?:ay)?,? )?(?:is|was|were|would|does|do)\s+(?:that|it|this|they|there)?\s*"
    r"(?:really\s+|actually\s+|still\s+)?(?P<word>too (?:far|long|many|much|high)|a lot|"
    r"about right|over the top|expensive|steep)\b", re.I)
A_CEILING = frozenset(("a lot", "much", "too much", "too high", "too many", "too far", "too long",
                       "expensive", "steep", "over the top", "about right", "a good price",
                       "a fair price", "the going rate", "about the going rate"))


ALREADY_JUDGED = re.compile(
    r"\b(?:about where|most people|any(?:thing|one) (?:over|above|past)|more than about|\
    no more than|up to about|past that|beyond that|on the high side|on the low side|\
    on the dear side|on the cheap side|cheaper than|dearer than|more expensive than|\
    about right|is a lot|isn't a lot|is not a lot|fair price|good price|the going rate|\
    the usual (?:is|rate|range)|the average is)\b", re.IGNORECASE)


def _already_judged(memory):
    turns = memory.get("turns") if isinstance(memory, dict) else None
    if not isinstance(turns, list):
        return False
    for turn in reversed(turns):
        if not isinstance(turn, dict):
            continue
        said = str(turn.get("bot") or "")
        if not said:
            continue
        return bool(ALREADY_JUDGED.search(said))
    return False


def _a_bare_doubt(clean, memory):
    if not isinstance(memory, dict):
        return None
    doubt = _doubt(clean)
    if doubt is None:
        said_line = str(clean or "").strip().lower().rstrip("?!. ")
        match = BARE_CEILING.match(said_line)
        if not match:
            return None
        doubt = {"word": match.group("word"), "value": None, "unit": "", "money": False}
    if doubt["word"] not in A_CEILING:
        return None
    if A_MONEY_WORD.search(str(clean or "")):
        return None
    said, _at = _answer_before(memory)
    if said:
        return None
    if doubt["value"] is not None:
        return None
    if _already_judged(memory):
        return None
    return _their_figure(memory)


def reply_to_a_bare_doubt(clean, memory):
    read = _a_bare_doubt(clean, memory)
    if not read:
        return None
    _value, unit, text, money = read
    if money:
        options = A_PRICE_NEXT_TO
    elif unit in A_DISTANCE:
        options = A_JOURNEY_IS_TIME
    elif unit in A_STRETCH:
        options = A_STRETCH_OF_TIME
    else:
        options = THE_REST_IS_UNSURE
    return _verdict.pick([line.format(said=text) for line in options],
                         {"turns": [{"t": text}]}, text)


def reply_for(clean, memory):
    if not isinstance(memory, dict):
        return None
    if AN_AGE.match(str(clean or "").strip()):
        return None
    judged = reply_to_a_doubt(clean, memory)
    if judged:
        return judged
    bare = reply_to_a_bare_doubt(clean, memory)
    if bare:
        return bare
    read = _number(clean)
    if read is None:
        return None
    value, unit = read
    said = _said(memory, clean)
    if not said:
        return None
    span = _range(said)
    if span is None:
        return None
    low, high, says_unit = span
    if unit and says_unit and not _same_measure(unit, says_unit):
        return None
    span_text = "%s to %s%s" % (_say(low), _say(high), _unit(says_unit))
    where = _where(value, low, high, says_unit)
    if where == "inside":
        return pick_inside(value, span_text, said)
    step = _step(said)
    if where == "below":
        line = "%s is under the %s it should be" % (_say(value), span_text)
        if step:
            return "%s: %s." % (line, step.rstrip("."))
        return line + " - that is the thing to put right."
    return "%s is over the %s it should be, which is the thing to put right." % (
        _say(value), span_text)


INSIDE = (
    "That is where it should be - {span}.",
    "{value} is in the {span} it wants, so nothing to do there.",
    "Spot on: {span} is right for it.",
)


def pick_inside(value, span_text, said):
    options = [line.format(value=_say(value), span=span_text) for line in INSIDE]
    return _verdict.pick(options, {"turns": [{"bot": said}]}, said)


def _figure_of_the_answer(memory, at):
    turns = memory.get("turns") if isinstance(memory, dict) else None
    if not isinstance(turns, list) or not 0 <= at < len(turns):
        return None
    turn = turns[at]
    if not isinstance(turn, dict):
        return None
    said = str(turn.get("user") or "")
    found = list(FIGURE.finditer(said))
    if not found:
        return None
    figure = _the_figure_in(said, found[-1])
    if not figure:
        return None
    money, measured = _doubt_ranges(turn.get("bot"))
    if figure["unit"]:
        if not any(span["unit"] == figure["unit"] for span in measured):
            return None
    elif figure["money"]:
        if not money:
            return None
    elif measured or not money:
        return None
    return figure
