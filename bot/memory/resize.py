import re

QUANTITY = re.compile(
    r"(?<![\w.])(\d+(?:\.\d+)?)\s*"
    r"(kg|kilos?|kilograms?|g|grams?|lb|lbs|pounds?|oz|litres?|liters?)\b", re.I)
COUNT = (r"(?:\d{1,3}|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve)")
HEADCOUNT = re.compile(
    r"(?<![\w.])(" + COUNT + r")\s+"
    r"(?:people|persons?|adults?|kids|children|guests?|lads|mates|friends|of us|of them|of you)\b", re.I)
ONLY_A_COUNT = frozenset("""
    a about actually and are for instead it it's its just make no not now of only please so
    sorry that the there too us wait we we're were
""".split())
_A_PORTION_ASK = re.compile(r"\bhow (?:much|many)\b", re.I)
RATE = re.compile(
    r"(?<![\w.])£?\s*(\d[\d,]*(?:\.\d+)?)\s*(?:pounds?|quid)?\s*"
    r"(a|per|each|every|/)\s*(month|week|fortnight|year)\b", re.I)
RATE_UNIT = {"month": "a month", "week": "a week", "fortnight": "a fortnight",
             "year": "a year"}
ONLY_A_RATE = frozenset("""
    a about actually afford and at be bump can could do for guess i if instead it just let lets
    make maybe manage more much now of only or please rather really say so still stretch that
    think to up want was we what would you
""".split())
A_REPLACEMENT = re.compile(r"\b(?:make|instead|actually|only|just|no|not|wait|sorry|now)\b", re.I)
SOMEONE_OUT = re.compile(
    r"\b(?:is|are|was|were|isn'?t|aren'?t|isnt|arent)\s+not\b"
    r"|\b(?:isn'?t|aren'?t|not)\s+(?:coming|eating|having|joining)\b"
    r"|\bcan'?t\b|\bcannot\b|\bwont\b|\bwon'?t\b|\bca\s*n'?t\b"
    r"|\b(?:doesn'?t|does not|dont|do not)\s+(?:eat|want|like|come)\b"
    r"|\bpulled out\b|\bdropped out\b|\bflaked\b|\bcancelled\b|\bcanceled\b"
    r"|\b(?:is|are)\s+(?:ill|unwell|sick|away)\b|\b(?:isnt|isn'?t)\s+(?:well|free)\b",
    re.I)
SOME_OF_THEM = re.compile(
    r"\b(?:\d+|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|a few|a couple)"
    r"\s+of\s+(?:them|those|us|you)\s+(?:is|are|was|were|has|have)\b",
    re.I)
STILL_AT_THE_TABLE = re.compile(
    r"\bof\s+(?:them|those|us|you)\s+(?:is|are|was|were)\s+(?:still\s+)?"
    r"(?:eating|having|coming|drinking|joining|there|in|here)\b",
    re.I)
_GROUP = (r"(?:people|persons?|adults?|kids?|children|guests?|lads?|mates?|friends?|boys?|girls?"
          r"|men|women|veg(?:etarian)?s?|veggies|teenagers?|toddlers?|grown-?ups?|of us|of them"
          r"|of you)")
_TWO_COUNTS = re.compile(
    r"(?<![\w.])(" + COUNT + r")\s+" + _GROUP + r"", re.I)
_WORD_VALUE = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6,
               "seven": 7, "eight": 8, "nine": 9, "ten": 10, "eleven": 11, "twelve": 12}
FAMILY = {"kg": "weight", "kilo": "weight", "kilos": "weight", "kilogram": "weight",
          "kilograms": "weight", "g": "weight", "gram": "weight", "grams": "weight",
          "lb": "weight", "lbs": "weight", "pound": "weight", "pounds": "weight",
          "oz": "weight", "litre": "volume", "litres": "volume", "liter": "volume",
          "liters": "volume"}


def quantity(text):
    said = " ".join(str(text or "").lower().split())
    found = QUANTITY.search(said)
    if not found:
        return None
    try:
        value = float(found.group(1))
    except ValueError:
        return None
    unit = found.group(2)
    return value, unit, found.span(), FAMILY.get(unit, "")


def _earlier_lines(memory, n=4):
    from . import recent

    lines = []
    for turn in recent(memory, n + 1):
        said = (turn.get("user") if isinstance(turn, dict) else "") or ""
        said = " ".join(str(said).split())
        if said:
            lines.append(said)
    return lines[:n]


def rate(text):
    said = " ".join(str(text or "").lower().split())
    found = RATE.search(said)
    if not found:
        return None
    try:
        value = float(found.group(1).replace(",", ""))
    except ValueError:
        return None
    return value, found.group(3), found.span(), "rate"


AIMS_AT_A_FIGURE = re.compile(r"\b(?:want|wants|need|needs|save|saving|target|aim|aiming)\b",
                             re.I)
A_CORRECTION = re.compile(r"\b(?:actually|instead|rather|only|just)\b", re.I)


def _a_bare_rate(text):
    said = " ".join(str(text or "").lower().split())
    if not said or len(said.split()) > 8:
        return None
    found = re.search(r"(?<![\w.])£?(\d[\d,]*(?:\.\d+)?)\s*(?:pounds?|quid)?", said)
    if not found:
        return None
    others = [w.strip(".,!?;:\"'") for w in said.split()]
    others = [w for w in others if w and w not in ONLY_A_RATE]
    if others != [found.group(0).strip()]:
        return None
    if AIMS_AT_A_FIGURE.search(said) and A_CORRECTION.search(said):
        return None
    try:
        return float(found.group(1).replace(",", ""))
    except ValueError:
        return None


def _with_a_new_rate(said, value, unit, memory):
    for earlier in _earlier_lines(memory):
        there = rate(earlier)
        if there is None or (unit is None and there[0] == value):
            continue
        period = unit or there[1]
        start, end = there[2]
        low = " ".join(earlier.lower().split())
        candidate = (low[:start] + ("%g " % value) + RATE_UNIT[period] + low[end:]).strip()
        if candidate != said.lower():
            return candidate
    return None


def _value(raw):
    raw = str(raw or "").strip().lower()
    if raw.isdigit():
        return int(raw)
    return _WORD_VALUE.get(raw)


def headcount(text):
    said = " ".join(str(text or "").lower().split())
    if not said:
        return None
    groups = list(_TWO_COUNTS.finditer(said))
    if len(groups) > 1:
        total = _value(groups[0].group(1)) or 0
        for more in groups[1:]:
            total += _value(more.group(1)) or 0
        if total:
            return (total, groups[0].start(1), groups[-1].end(1))
    found = HEADCOUNT.search(said)
    if found:
        value = _value(found.group(1))
        return (value, found.start(1), found.end(1)) if value else None
    if len(said.split()) > 6:
        return None
    number = re.search(r"(?<![\w.])(" + COUNT + r")\b", said)
    if not number:
        return None
    others = [w.strip(".,!?;:\"'") for w in said.split()]
    others = [w for w in others if w and w not in ONLY_A_COUNT]
    if len(others) != 1:
        return None
    value = _value(number.group(1))
    return (value, number.start(1), number.end(1)) if value else None


def _a_question(earlier):
    said = " ".join(str(earlier or "").lower().split())
    return bool(re.search(r"\b(?:how|what|which)\b", said) or said.endswith("?"))


def _the_ones_left(value, memory):
    for earlier in _earlier_lines(memory):
        there = headcount(earlier)
        if there is None:
            continue
        left = there[0] - value
        return left if left >= 1 else None
    return None


def _with_a_new_table(said, value, memory):
    for earlier in _earlier_lines(memory):
        if not _a_question(earlier):
            continue
        there = headcount(earlier)
        if there is None or there[0] == value:
            continue
        low = " ".join(earlier.lower().split())
        candidate = (low[:there[1]] + str(value) + low[there[2]:]).strip()
        if candidate != said.lower():
            return candidate
    earlier_ask = next((line for line in _earlier_lines(memory)
                        if _a_question(line) and _A_PORTION_ASK.search(line.lower())
                        and headcount(line) is None), None)
    if earlier_ask:
        return "%s for %d people" % (" ".join(earlier_ask.lower().split()).rstrip("?. "), value)
    return None


def _with_a_new_weight(said, value, memory):
    now = quantity(said)
    unit = None
    family = None
    if now is not None:
        value, unit, _span, family = now
    for earlier in _earlier_lines(memory):
        there = quantity(earlier)
        if there is None or there[0] == value:
            continue
        if unit is None:
            if not _a_question(earlier):
                continue
            unit, family = there[1], there[3]
        elif there[3] != family:
            continue
        start, end = there[2]
        low = " ".join(earlier.lower().split())
        candidate = (low[:start] + ("%g" % value) + unit + low[end:]).strip()
        if candidate != said.lower():
            return candidate
    return None


def rewritten(text, memory):
    said = " ".join(str(text or "").split())
    if not said or len(said.split()) > 10:
        return None
    now = rate(said)
    if now is not None:
        return _with_a_new_rate(said, now[0], now[1], memory)
    bare = _a_bare_rate(said)
    if bare is not None:
        resized = _with_a_new_rate(said, bare, None, memory)
        if resized:
            return resized
    if quantity(said) is not None:
        return _with_a_new_weight(said, None, memory)
    table = headcount(said)
    if table is not None:
        value = table[0]
        if SOMEONE_OUT.search(said):
            left = _the_ones_left(value, memory)
            return _with_a_new_table(said, left, memory) if left else None
        if SOME_OF_THEM.search(said) and not STILL_AT_THE_TABLE.search(said):
            return None
        if HEADCOUNT.search(said.lower()):
            return _with_a_new_table(said, value, memory)
        if not A_REPLACEMENT.search(said):
            return None
        return (_with_a_new_table(said, value, memory)
                or _with_a_new_weight(said, value, memory)
                or _with_a_new_rate(said, value, None, memory))
    return None
