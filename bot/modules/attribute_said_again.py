import re

from ..memory import repeat

PRIORITY = 6900

THEIRS = ("size", "shoe size", "ring size", "weight", "height", "colour", "color", "budget",
          "age", "brand", "make", "model", "number", "plate", "breed", "name")

QUESTION_WORDS = frozenset("""best better option options chance chances odds next plan plans point
    problem issue deal story time day week month year""".split())

ASK = re.compile(r"\bwhat(?:\s+is|\s*'s|s)?\s+(?P<attr>" + "|".join(
    sorted(THEIRS, key=len, reverse=True)) + r")\s+(?:am\s+i)\b", re.I)
OF_MINE = re.compile(r"\bwhat(?:\s+is|\s*'s|s)?\s+my\s+(?P<attr>" + "|".join(
    sorted(THEIRS, key=len, reverse=True)) + r")\b", re.I)
FILLER = frozenset("""again now then today still also please again? so and but ok okay oh""".split())

A_FIGURE = re.compile(
    r"(?:[\u00a3$\u20ac]\s*\d[\d,.]*"
    r"|\b\d[\d,.]*\s*(?:a|per|each)\s+(?:month|week|year|fortnight|day|week|month)\b"
    r"|\b\d[\d,.]*\s*(?:quid|pounds?|dollars?|euros?|pm)\b)", re.I)
NOT_A_COST = re.compile(
    r"\b(?:earn|earns|earned|earning|salary|wage|wages|take[- ]home|save|saves|saved|saving"
    r"|work|works|worked|working|shift|shifts"
    r"|eat|eats|ate|eating|drink|drinks|drank|drinking"
    r"|run|runs|ran|running|walk|walks|walked|walking|swim|swims|swam|swimming"
    r"|sleep|sleeps|slept|sleeping|study|studies|studied|studying|read|reads|reading)\b", re.I)
PAY_ASK = re.compile(
    r"\b(?:what|how\s+much)\b[^.!?]*?\b(?:am|was|are|were|do|did)\s+i\b[^.!?]*?"
    r"\b(?:pay|paying|paid|cost|costs|costing)\b", re.I)
COST_ASK = re.compile(r"^\W*(?:and\s+|so\s+|ok\s+|okay\s+)?how\s+much\s+(?:is|was)\s+it\b", re.I)
WHATS_MY = re.compile(r"\bwhat(?:\s+is|\s*'s|s)?\s+my\s+(?P<attr>[a-z][a-z' -]{1,24}?)\b", re.I)


def _their_attribute(low):
    for pattern in (ASK, OF_MINE):
        match = pattern.search(low)
        if match:
            return " ".join(match.group("attr").lower().split())
    return ""


def _stem(word):
    word = str(word or "").lower().strip("'")
    for suffix in ("ing", "ed", "es", "s"):
        if len(word) > len(suffix) + 3 and word.endswith(suffix):
            return word[:-len(suffix)]
    return word


def _names(tokens, attribute):
    stems = {_stem(token) for token in tokens}
    return all(_stem(word) in stems for word in attribute.split())


def _the_phrase_of_theirs(attribute, memory, needs_a_figure=False):
    turns = (memory or {}).get("turns") if isinstance(memory, dict) else None
    if not turns:
        return ""
    for turn in reversed(turns):
        line = (turn or {}).get("user") or ""
        if not line:
            continue
        if not _names(re.findall(r"[a-z']+", line.lower()), attribute):
            continue
        if needs_a_figure and not (A_FIGURE.search(line) and not NOT_A_COST.search(line)):
            continue
        phrase = _phrase(line)
        if not phrase or not _names(re.findall(r"[a-z']+", phrase.lower()), attribute):
            continue
        return phrase
    return ""


def _a_cost_line(line):
    line = str(line or "")
    return bool(line) and bool(A_FIGURE.search(line)) and not NOT_A_COST.search(line)


def _the_newest_cost(memory):
    turns = (memory or {}).get("turns") if isinstance(memory, dict) else None
    if not turns:
        return ""
    for turn in reversed(turns):
        line = (turn or {}).get("user") or ""
        if _a_cost_line(line):
            return _phrase(line)
    return ""


def _the_cost_just_before(memory):
    turns = (memory or {}).get("turns") if isinstance(memory, dict) else None
    if not turns:
        return ""
    line = (turns[-1] or {}).get("user") or ""
    return _phrase(line) if _a_cost_line(line) else ""


def _phrase(line):
    from . import memory_store
    try:
        return memory_store._told_phrase(line)
    except Exception:
        return ""


CONTRACTIONS = (("you are", "you're"), ("you have", "you've"), ("it is", "it's"),
                ("that is", "that's"), ("i am", "i'm"))


def _the_value(phrase):
    for pattern in (r"^you(?:'re| are| were) (.+)$", r"^you(?:'ve| have) (.+)$",
                    r"^your .+? is (.+)$", r"^your (.+)$",
                    r"^it(?:'s|s) (.+)$", r"^you (?:pay|paid) (.+)$",
                    r"^(?:it )?costs? (.+)$"):
        match = re.match(pattern, phrase)
        if match:
            return match.group(1).strip().rstrip(".")
    return ""


WHEN_ASK = re.compile(
    r"\b(?:did|do)\s+(?:i|we)\s+say\s+when\b(?P<rest>.*)"
    r"|\bwhen\s+did\s+(?:i|we)\s+say\b(?P<rest2>.*)"
    r"|\bwhen\s+(?:was|is)\s+it\s+(?:that\s+)?(?:i|we)\s+said\b(?P<rest3>.*)", re.I)
WHERE_ASK = re.compile(
    r"\b(?:did|do)\s+(?:i|we)\s+say\s+where\b(?P<rest>.*)"
    r"|\bwhere\s+did\s+(?:i|we)\s+say\b(?P<rest2>.*)", re.I)

MONTHS = ("january february march april may june july august september october november "
          "december").split()
WEEKDAYS = "monday tuesday wednesday thursday friday saturday sunday".split()
TIME_WORDS = frozenset(MONTHS + WEEKDAYS + """weekend tonight tomorrow today morning
afternoon evening night midday noon christmas easter summer winter spring autumn""".split())
TIME_SPAN = re.compile(
    r"\b(?:next|last|this)\s+(?:week|month|year|summer|winter|spring|autumn)\b"
    r"|\bin\s+(?:about\s+)?\d+\s+(?:days?|weeks?|months?|years?)\b"
    r"|\b\d{1,2}(?:[.:]\d\d)?\s*(?:am|pm)\b|\bat\s+\d{1,2}\b", re.I)
PLACE = re.compile(
    r"\b(?:near|next to|close to|round the corner from|opposite)\s+"
    r"(?P<place>[a-z][a-z'\u2019]*(?:\s+[a-z][a-z'\u2019]*){0,3})", re.I)
SIZE_ASK = re.compile(
    r"\b(?:how\s+(?:big|large|wide|long|tall|high|deep)"
    r"|what\s+(?:size|dimensions?|measurements?)"
    r"|how\s+many\s+(?:metres|meters|feet|foot|ft|centimetres|centimeters|cm"
    r"|square\s+(?:metres|meters|feet)))\b(?P<rest>[^?.!]*)", re.I)
SIZE_ADVICE = re.compile(r"\b(?:should|shall|would|could|can|might|will|need|needs|enough"
                         r"|recommend|best)\b", re.I)
A_SIZE = re.compile(
    r"(?P<measure>\b\d+(?:[.,]\d+)?\s*(?:by|x|\u00d7)\s*\d+(?:[.,]\d+)?\s*"
    r"(?:m|metres?|meters?|ft|feet|foot|cm|centimetres?|centimeters?|inches|inch)\b"
    r"|\b\d+(?:[.,]\d+)?\s*(?:square|sq)\s*(?:metres?|meters?|feet|foot|ft|m)\b"
    r"|\b\d+(?:[.,]\d+)?\s*(?:m|metres?|meters?|cm|centimetres?|centimeters?|ft|feet|foot"
    r"|inches|inch|litres?|liters?|ml)\b)"
    r"(?P<after>\s+[a-z][a-z'-]*)?", re.I)
SALARY_WORDS = ("salary", "pay", "wage", "wages", "income", "earnings")
MONEY_WORDS = SALARY_WORDS + ("budget", "price", "cost", "rent", "savings", "deposit")
MONEY_QUALIFIER = (
    "current", "currently", "annual", "annually", "monthly", "weekly", "hourly", "yearly",
    "real", "actual", "actually", "basic", "gross", "net", "total", "usual", "normal",
    "present", "own",
)
MONEY_ASK = re.compile(
    r"\bwhat(?:'s| is| was|s)?\s+(?:my|our|their|his|her)\s+"
    r"(?:(?:" + "|".join(MONEY_QUALIFIER) + r")\s+)?(?P<what>" + "|".join(
        sorted(MONEY_WORDS, key=len, reverse=True)) + r")\b"
    r"|\bhow much\s+(?:was|is|were|did\s+(?:i|we)\s+say)\s+(?:my|our|the|their|his|her)\s+"
    r"(?:(?:" + "|".join(MONEY_QUALIFIER) + r")\s+)?(?P<what2>"
    + "|".join(sorted(MONEY_WORDS, key=len, reverse=True)) + r")\b", re.I)
A_PER_YEAR = re.compile(
    r"\b\d+(?:\.\d+)?\s*k\b(?:\s*(?:a|per)\s*(?:year|annum))?"
    r"|\u00a3?\s?\d[\d,]{3,}\s*(?:a|per)\s*(?:year|annum)\b", re.I)
A_MONEY = re.compile(
    r"(?:\u00a3\s?\d[\d,]*(?:\.\d\d)?"
    r"|\b\d[\d,]*(?:\.\d+)?\s*(?:pounds?|quid|dollars?|euros?|grand)\b"
    r"|\b\d[\d,]{2,}\b)"
    r"(?:\s*(?:a|per)\s*(?:month|week|year|fortnight))?", re.I)
SLOT_STOP = frozenset("""i we you me us my our it its the a an to be been being was were are is
am do did does say said about that this of for in on at and but so then just again please oh ok
okay actually""".split())

AGE_ASK = re.compile(
    r"\b(?:what|how\s+old)\b[^.?!]{0,40}?\b(?:did|do)\s+i\s+"
    r"(?:say|tell\s+you|told\s+you|think|thought|mention|mentioned)\b[^.?!]{0,30}?\b(?:age|old)\b"
    r"|\bwhat\s+(?:was|is)\s+(?P<whose>his|her|their|my|our|its)\s+age\b"
    r"|\bhow\s+old\s+(?:did|do)\s+i\s+(?:say|tell\s+you|told\s+you|think|mention)\b", re.I)
OFTEN_ASK = re.compile(
    r"\bhow\s+often\b[^.?!]{0,30}?\b(?:did|do)\s+i\s+(?:say|tell\s+you|told\s+you|mention)\b"
    r"|\bhow\s+many\s+times\b[^.?!]{0,30}?\b(?:did|do)\s+i\s+(?:say|tell\s+you|mention)\b"
    r"|\bhow\s+often\s+(?:was|is)\s+it\b[^.?!]{0,12}?\bagain\b", re.I)
AN_AGE_CLAUSE = re.compile(
    r"(?:^|[,;]|\bis\b|\bwas\b|\bim\b|\bi'm\b|\bam\b|\b-\s*)\s*(?P<n>\d{1,3})\s*"
    r"(?=$|[,.;!?]|\s+and\b|\s+but\b)",
    re.I)
SOMEBODY = re.compile(
    r"\b(?:i|im|i'm|me|myself|he|she|him|her|his|they|them|their|my|our"
    r"|son|daughter|lad|girl|boy|kid|kids|baby|toddler|mum|mom|dad|husband|wife|partner|brother"
    r"|sister|nan|gran|grandad|dog|cat|pup|puppy|labrador|retriever|terrier|shepherd|spaniel"
    r"|collie|hound|mutt|rabbit|hamster|horse)\b", re.I)
A_COUNT_OF_PEOPLE = re.compile(r"\b\d+\s+(?:of\s+us|people|adults)\b", re.I)

A_HABIT_SAID = re.compile(
    r"\b(?:(?:once|twice|three|four|five|six|seven|eight|nine|ten|\d+)\s+times?\s+"
    r"(?:a|per|each)\s+(?:day|week|month|year)"
    r"|(?:once|twice)\s+(?:a|per)\s+(?:day|week|month|year)"
    r"|every\s+(?:day|week|weekend|morning|evening|night)"
    r"|most\s+(?:days|weeks|mornings|evenings)|\bdaily\b)", re.I)

def _the_slot_ask(low):
    for slot, pattern in (("when", WHEN_ASK), ("where", WHERE_ASK)):
        match = pattern.search(low)
        if match:
            rest = next((group for group in match.groups() if group), "")
            return slot, _the_subject(rest)
    for slot, pattern in (("age", AGE_ASK), ("often", OFTEN_ASK), ("off_with", OFF_WITH_ASK)):
        if pattern.search(low):
            return slot, set()
    if _their_attribute(low):
        return "", set()
    match = SIZE_ASK.search(low)
    if match and not SIZE_ADVICE.search(low):
        return "size", _the_subject(match.group("rest"))
    match = MONEY_ASK.search(low)
    if match:
        what = next((group for group in match.groups() if group), "").lower()
        return "money:" + what, set()
    return "", set()


def _the_subject(rest):
    return {_stem(word) for word in re.findall(r"[a-z']+", rest.lower())
            if word not in SLOT_STOP}


def _a_time(line):
    low = line.lower()
    named = [word for word in re.findall(r"[a-z'\u2019]+", low) if word in MONTHS + WEEKDAYS]
    if named:
        return named[0].capitalize()
    span = TIME_SPAN.search(low)
    if span:
        return " ".join(span.group(0).split())
    for word in re.findall(r"[a-z'\u2019]+", low):
        if word in TIME_WORDS:
            return word
    return ""


def _a_place(line):
    match = PLACE.search(line)
    if not match:
        return ""
    place = " ".join(match.group("place").split())
    if not place or {_stem(word) for word in place.split()} <= SLOT_STOP:
        return ""
    return " ".join(match.group(0).split())


def _a_size(line, subject):
    for match in A_SIZE.finditer(line):
        measure = " ".join(match.group("measure").split())
        after = (match.group("after") or "").strip().lower()
        if after and subject and _stem(after) in subject:
            return measure + " " + after
        return measure
    return ""


PRONOUN_LINE = re.compile(r"^\s*(?:its|it is|it's|that's|thats|theres|there's|theyre|they are"
                          r"|hes|shes|were|we are)\b", re.I)


def _the_size_recall(subject, lines):
    for index in range(len(lines) - 1, -1, -1):
        line = lines[index]
        value = _a_size(line, subject)
        if not value:
            continue
        said = {_stem(word) for word in re.findall(r"[a-z']+", line.lower())}
        if subject:
            if said & subject:
                return value
            older = lines[index - 1] if index else ""
            if PRONOUN_LINE.match(line) and subject & {_stem(word)
                                                      for word in re.findall(r"[a-z']+", older.lower())}:
                return value
            continue
        if len(lines) - index <= 2:
            return value
    return ""


def _the_money_recall(what, lines):
    for line in reversed(lines):
        low = line.lower()
        said = {_stem(word) for word in re.findall(r"[a-z']+", low)}
        if what in SALARY_WORDS:
            match = A_PER_YEAR.search(line)
            if match:
                return " ".join(match.group(0).split())
            continue
        if _stem(what) not in said:
            continue
        match = A_MONEY.search(line)
        if match:
            return " ".join(match.group(0).split())
    return ""



SAID_ASK = re.compile(
    r"^(?:and\s+|so\s+|but\s+|also\s+|oh\s+|ok\s+|okay\s+)?"
    r"(?:(?:what|which)\s+(?P<attr>[a-z][a-z' -]{1,20}?)\s+"
    r"(?:did|do|have)\s+(?:i|we)\s+(?:say|give|mention|tell\s+you)"
    r"|how\s+(?P<how>[a-z]+)\s+did\s+(?:i|we)\s+say)"
    r"\b[^?.!]*$", re.I)

SIZE_VALUE = re.compile(
    r"(?:(?<![\w'])(?:xs|s|m|l|xl|xxl|xxxl)(?![\w'])"
    r"|\b(?:small|medium|large|extra\s+large"
    r"|size\s+\d{1,2}|(?:a\s+)?\d{1,2}\s*(?:-|to)\s*\d{1,2})\b)", re.I)
LENGTH_VALUE = re.compile(
    r"\b(?:long|short|shoulder[- ]length|past\s+(?:my\s+)?shoulders|bob|crop|pixie"
    r"|just\s+(?:above|below)\s+\w+|\d+\s*(?:cm|inches|inch))\b", re.I)
WEIGHT_VALUE = re.compile(
    r"\b\d+(?:[.,]\d+)?\s*(?:kg|kilo|kilos|kilograms|st|stone|stones|lbs?|pounds)\b", re.I)
AGE_VALUE = re.compile(
    r"\b(?:\d{1,2}\s*(?:years?\s*old|yr|yrs)?|aged\s+\d{1,2})\b", re.I)
COLOUR_VALUE = re.compile(
    r"\b(?:red|blue|green|black|white|grey|gray|brown|beige|cream|navy|pink|purple|orange"
    r"|yellow|gold|silver|teal|turquoise|burgundy|maroon|khaki|olive|charcoal)\b", re.I)

VALUE_KINDS = {
    "size": SIZE_VALUE, "shoe size": SIZE_VALUE, "ring size": SIZE_VALUE,
    "colour": COLOUR_VALUE, "color": COLOUR_VALUE,
    "weight": WEIGHT_VALUE, "age": AGE_VALUE,
    "length": LENGTH_VALUE, "hair": LENGTH_VALUE,
}
HOW_KINDS = {
    "short": LENGTH_VALUE, "long": LENGTH_VALUE, "tall": LENGTH_VALUE,
    "big": SIZE_VALUE, "large": SIZE_VALUE, "small": SIZE_VALUE,
    "heavy": WEIGHT_VALUE, "old": AGE_VALUE,
}


def _the_value_kind(attribute, how):
    attribute = " ".join(str(attribute or "").lower().split())
    if attribute:
        if attribute in VALUE_KINDS:
            return VALUE_KINDS[attribute]
        if attribute in ("time", "day", "date", "month", "year", "week"):
            return _a_time
        if attribute in MONEY_WORDS or attribute in ("price", "cost"):
            return lambda line: A_MONEY.search(line)
        return None
    return HOW_KINDS.get(" ".join(str(how or "").lower().split()))


THEIR_QUESTION = re.compile(
    r"^\W*(?:what|whats|what's|how|when|where|which|who|why|can|could|should|shall|would|will"
    r"|does|do|did|is|are|was|were|have|has|any|anything|tell\s+me|remind\s+me)\b", re.I)


def _the_line_that_says_it(text, memory):
    low = " ".join(str(text or "").lower().split())
    match = SAID_ASK.match(low)
    if not match:
        return ""
    kind = _the_value_kind(match.group("attr"), match.group("how"))
    if kind is None:
        return ""
    turns = (memory or {}).get("turns") if isinstance(memory, dict) else None
    if not turns:
        return ""
    for turn in reversed(turns):
        line = " ".join(str((turn or {}).get("user") or "").split())
        if not line or not (kind(line) if callable(kind) else kind.search(line)):
            continue
        if THEIR_QUESTION.match(line) or SAID_ASK.match(line.lower()):
            continue
        if _their_attribute(line.lower()):
            continue
        return line
    return ""


def _the_values_the_kind_takes(text, line):
    low = " ".join(str(text or "").lower().split())
    match = SAID_ASK.match(low)
    if not match:
        return []
    kind = _the_value_kind(match.group("attr"), match.group("how"))
    if kind is None:
        return []
    if callable(kind):
        value = " ".join(str(kind(line) or "").split())
        return [value] if value else []
    found, seen = [], set()
    for hit in kind.finditer(line or ""):
        value = " ".join(hit.group(0).split())
        key = _stem(value)
        if value and key not in seen:
            seen.add(key)
            found.append(value)
    return found


def _the_value_said(text, memory):
    line = _the_line_that_says_it(text, memory)
    if not line:
        return None
    from .memory_store import respond as _the_store_says
    if _the_store_says(text, memory):
        return None
    values = _the_values_the_kind_takes(text, line)
    said = values[0] if len(values) == 1 else line
    reply = 'You said: "' + said + '"' if len(values) != 1 else "You said " + said + "."
    last = _the_last_reply(memory)
    if reply.lower().rstrip(".") in last.lower():
        return "Still the same: " + said
    return reply


def _the_slot_recall(text, memory):
    low = " ".join(str(text or "").lower().split())
    if not low:
        return None
    slot, subject = _the_slot_ask(low)
    if not slot:
        return None
    turns = (memory or {}).get("turns") if isinstance(memory, dict) else None
    if not turns:
        return None
    if slot in ("age", "often", "off_with"):
        value = ""
        if slot == "age":
            value = _the_age_they_gave(turns, low)
        elif slot == "often":
            value = _the_habit_they_gave(turns)
        else:
            value = _the_off_with_they_gave(turns)
        return _the_slot_reply(value, memory) if value else None
    if slot.startswith("money:"):
        lines = [str((turn or {}).get("user") or "") for turn in turns]
        value = _the_money_recall(slot.split(":", 1)[1], lines)
        return _the_slot_reply(value, memory) if value else None
    if slot == "size":
        lines = [str((turn or {}).get("user") or "") for turn in turns]
        value = _the_size_recall(subject, lines)
        return _the_slot_reply(value, memory) if value else None
    for turn in reversed(turns):
        line = (turn or {}).get("user") or ""
        if not line:
            continue
        value = _a_time(line) if slot == "when" else _a_place(line)
        if not value:
            continue
        said = {_stem(word) for word in re.findall(r"[a-z']+", line.lower())}
        if subject and not (said & subject):
            continue
        return _the_slot_reply(value, memory)
    return None
OFF_WITH_ASK = re.compile(
    r"\bwhat\s+(?:was|is)\s+i\s+off\b|\bwhat\s+did\s+i\s+say\s+i\s+was\s+off\b"
    r"|\bwhat\s+was\s+i\s+off\s+(?:sick\s+)?with\b", re.I)
OFF_WITH_SAID = re.compile(
    r"\b(?:off\s+(?:sick|work|ill)|been\s+off|signed\s+off)\b[^.?!]*?\bwith\s+"
    r"(?P<thing>an?\s+)?(?P<what>[a-z][a-z' -]{3,30})\s*$", re.I)


def _the_age_they_gave(turns, low):
    whose = "their"
    named = re.search(r"\b(his|her|their|my|our|its)\b[^.?!]{0,12}?\b(?:age|old)\b", low, re.I)
    if named:
        whose = named.group(1).lower()
    else:
        said_of = re.search(r"\b(he|she|they)\b", low, re.I)
        if said_of:
            whose = {"he": "his", "she": "her", "they": "their"}[said_of.group(1).lower()]
    if whose == "my":
        whose = "your"
    for turn in reversed(turns):
        line = str((turn or {}).get("user") or "")
        if not line or A_COUNT_OF_PEOPLE.search(line) or not SOMEBODY.search(line):
            continue
        found = AN_AGE_CLAUSE.search(line)
        if not found:
            continue
        number = found.group("n")
        if not (0 < int(number) < 121):
            continue
        named_person = re.search(
            r"\b(?:my|our)\s+(?P<who>[a-z]+)\s+(?P<was>is|was)\s+" + re.escape(number) + r"\b",
            line, re.I)
        if named_person:
            return "your " + named_person.group("who").lower() + " " + named_person.group("was").lower() \
                + " " + number

        if whose in ("their", "its") and re.search(r"\b(?:i|im|i'm|am)\b", line, re.I):
            return "your age was " + number
        if whose == "your":
            return "your age was " + number
        return whose + " age was " + number
    return ""


def _the_off_with_they_gave(turns):
    for turn in reversed(turns):
        line = str((turn or {}).get("user") or "")
        if not line:
            continue
        found = OFF_WITH_SAID.search(line)
        if found:
            thing = " ".join(found.group("what").lower().split())
            article = "an " if (found.group("thing") or "").strip().lower() == "an" else "a "
            return "you were off with " + article + thing
    return ""


def _the_habit_they_gave(turns):
    for turn in reversed(turns):
        line = str((turn or {}).get("user") or "")
        if not line:
            continue
        found = A_HABIT_SAID.search(line)
        if found:
            return " ".join(found.group(0).lower().split())
    return ""


def _the_slot_reply(value, memory):
    reply = "You said " + value + "."
    if reply.lower() in _the_last_reply(memory).lower():
        return "Still " + value + "."
    return reply


def _the_last_reply(memory):
    turns = (memory or {}).get("turns") if isinstance(memory, dict) else None
    if not turns:
        return ""
    return str((turns[-1] or {}).get("bot") or "")


def _spoken(phrase):
    phrase = re.sub(r"^its\b", "it's", str(phrase or ""))
    for full, short in CONTRACTIONS:
        phrase = re.sub(r"\b" + full + r"\b", short, phrase)
    return phrase


PAY_ASK_WORDS = frozenset((
    "how", "what", "much", "many", "do", "did", "does", "i", "im", "my", "the", "a", "an", "is",
    "was", "are", "were", "for", "of", "to", "in", "on", "at", "it", "that", "this", "me", "you",
    "your", "get", "got", "getting", "pay", "paid", "pays", "paying", "payment", "payments",
    "wage", "wages", "salary", "salaries", "earn", "earns", "earned", "earning", "make", "makes",
    "made", "making", "take", "home", "takehome", "and", "or", "per", "plus", "now", "again",
    "current", "currently", "exact", "exactly", "actual", "actually", "latest", "today", "so",
    "far", "have", "has", "had", "been", "like", "think", "about", "guess", "roughly", "all",
    "just", "really", "total", "figure", "number", "amount", "sum", "much", "there", "then",
))


def _the_ask_names_something_new(low, memory):
    turns = (memory or {}).get("turns") if isinstance(memory, dict) else None
    said = set()
    for turn in turns or ():
        line = str((turn or {}).get("user") or "").lower()
        said |= {_stem(word) for word in re.findall(r"[a-z']+", line)}
    asked = {_stem(word) for word in re.findall(r"[a-z']+", low)}
    asked -= {_stem(word) for word in PAY_ASK_WORDS}
    return bool(asked - said)


def _the_recall(text, memory):
    low = " ".join(str(text or "").lower().split())
    if not low:
        return None
    said_value = _the_value_said(low, memory)
    if said_value is not None:
        return said_value
    slot = _the_slot_recall(low, memory)
    if slot is not None:
        return slot
    attribute = _their_attribute(low)
    wants_a_figure = False
    if not attribute:
        if PAY_ASK.search(low):
            wants_a_figure = True
        elif COST_ASK.match(low):
            wants_a_figure = True
        else:
            named = WHATS_MY.search(low)
            candidate = " ".join(named.group("attr").split()) if named else ""
            if not candidate or len(candidate.split()) > 3 or candidate.split()[0] in QUESTION_WORDS:
                return None
            attribute = candidate
            wants_a_figure = True
    if attribute:
        phrase = _the_phrase_of_theirs(attribute, memory, needs_a_figure=wants_a_figure)
    elif COST_ASK.match(low):
        phrase = _the_cost_just_before(memory)
    else:
        phrase = _the_newest_cost(memory)
    if not phrase:
        return None
    if (PAY_ASK.search(low) and _the_ask_names_something_new(low, memory)
            and not repeat.the_figure_they_gave(text, memory)):
        return None
    said = _spoken(phrase)
    value = _the_value(said)
    last = _the_last_reply(memory)
    if value and value.lower() in last.lower() and "you told me" in last.lower():
        return "Still " + value + "."
    return "You told me " + said + "."


def takes_as_it_comes(text, memory):
    low = " ".join(str(text or "").lower().split())
    slot, _ = _the_slot_ask(low)
    if slot in ("age", "often", "off_with"):
        return False
    return _the_recall(text, memory) is not None


TAKES_AS_IT_COMES = takes_as_it_comes


def respond(text, memory):
    return _the_recall(text, memory)
