import re

from . import history

_COUNT = (r"(?:\d{1,3}|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|dozen|"
          r"a dozen)")

A_PORTION_ASK = re.compile(
    r"\bhow many\b[^.?!]{0,30}?\b(?:does|do|would|will|can)\s+(?:that|it|this)\s+\w+"
    r"|\bhow many people (?:does|do|will|would)\s+(?:that|it|this)\b"
    r"|\b(?:that|it|this)\s+(?:feeds|serves|makes|does|will do)\s+(?:how many|how much)\b"
    r"|\bhow many(?: people| mouths)?\s+(?:is|are|will|would)\s+(?:that|it|this)\b"
    r"|\bhow many(?: people| mouths)?\s+(?:is|are)\s+(?:that|it|this)\s+\w+"
    r"|\b(?:that|it|this)\s+(?:is|are)\s+for\s+how many\b"
    r"|\b(?:enough|good)\s+for\s+how many\b", re.I)

FEEDS_A_COUNT = re.compile(r"\b(?:feeds|serves|makes)\s+(?P<n>" + _COUNT + r")\b", re.I)
FOR_A_COUNT = re.compile(r"\bfor\s+(?P<n>" + _COUNT + r")\b", re.I)
PER_PERSON = re.compile(r"\b(?:each|per person|apiece|a head|per head|each person|per serving)\b",
                        re.I)

AN_AMOUNT = re.compile(
    r"(?<![\d.])\d+(?:\.\d+)?\s*(?:g|grams?|kg|kilos?|ml|millilitres?|litres?|l|oz|ounces?|"
    r"lbs?|pounds?|cups?|tablespoons?|tbsps?|teaspoons?|tsps?)\b"
    r"|\bhalf a (?:cup|mug|kilo|pint)\b|\ba (?:cup|mug|kilo|pint)\b", re.I)
A_TIME_AFTER_A_COUNT = re.compile(
    r"\s*(?:seconds?|secs?|minutes?|mins?|hours?|hrs?|days?|weeks?|months?|years?)\b", re.I)


def _a_time_not_a_portion(said, found):
    return bool(A_TIME_AFTER_A_COUNT.match(said or "", found.end("n")))

_NUMBER_WORD = (r"(?:\d{1,3}|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|"
                r"thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|nineteen|twenty|thirty|"
                r"forty|fifty|sixty|seventy|eighty|ninety|a hundred|a dozen)")
A_COUNT_OF_PEOPLE = re.compile(
    r"\b(?:about\s+|around\s+|just\s+|only\s+|all\s+)?(?P<n>" + _NUMBER_WORD + r")\s+"
    r"(?:people|guests|of us|adults|coming|mouths)\b"
    r"|\b(?:theres|there are|there will be|we are|were|we have|weve got|make it|make that)\s+"
    r"(?:about\s+|around\s+)?(?P<m>" + _NUMBER_WORD + r")\b", re.I)

A_BARE_COUNT = re.compile(
    r"^\W*(?:and|so|ok|okay|right|then|but|no|yes|yeah)?[\s,]*"
    r"(?:how\s+much|how\s+many)?[\s,]*(?:is\s+that|would\s+that\s+be|does\s+that\s+make)?"
    r"[\s,]*(?:for|between)\s+(?P<n>" + _NUMBER_WORD + r")\b[\s.?!]*$", re.I)

A_FIGURE_AND_UNIT = re.compile(
    r"\b(?P<n>\d+(?:\.\d+)?)\s*(?P<u>kg|kilos?|g|grams?|ml|millilitres?|litres?|l|oz|ounces?|"
    r"lbs?|pounds?)\b", re.I)

CLAUSE_EDGE = re.compile(r",\s*so\s+|;\s+|,\s*(?:which|and that)\s+|\.\s+", re.I)


def _the_last_answer(memory):
    return history.the_last_answer(memory)


def _the_clause_with_the_count(said, start, end):
    left = 0
    for edge in CLAUSE_EDGE.finditer(said):
        if edge.end() <= start:
            left = edge.end()
        elif edge.start() >= end:
            return said[left:edge.start()].strip(" .")
    return said[left:].strip(" .")


def _the_number(word):
    return " ".join(str(word or "").split()).lower()


_WORDS_FOR_NUMBERS = {
    "one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7, "eight": 8,
    "nine": 9, "ten": 10, "eleven": 11, "twelve": 12, "thirteen": 13, "fourteen": 14,
    "fifteen": 15, "sixteen": 16, "seventeen": 17, "eighteen": 18, "nineteen": 19, "twenty": 20,
    "thirty": 30, "forty": 40, "fifty": 50, "sixty": 60, "seventy": 70, "eighty": 80,
    "ninety": 90, "a hundred": 100, "a dozen": 12, "dozen": 12,
}


def _as_a_count(word):
    word = _the_number(word)
    if word.isdigit():
        return int(word)
    return _WORDS_FOR_NUMBERS.get(word, 0)


def _in_grams(figure, unit):
    unit = unit.lower()
    if unit in ("kg", "kilo", "kilos"):
        return figure * 1000.0
    if unit in ("g", "gram", "grams"):
        return figure
    if unit in ("oz", "ounce", "ounces"):
        return figure * 28.35
    if unit in ("lb", "lbs", "pound", "pounds"):
        return figure * 453.6
    if unit in ("ml", "millilitre", "millilitres", "l", "litre", "litres"):
        return figure * (1000.0 if unit in ("l", "litre", "litres") else 1.0)
    return 0.0


def _counts_people(said, found):
    if found.group(0).lower() != "each":
        return True
    before = (said or "")[:found.start()].rstrip().lower()
    return not before.endswith(("of", "in", "for", "with"))


def _the_per_head_figure(said):
    said = said or ""
    for found in PER_PERSON.finditer(said):
        if not _counts_people(said, found):
            continue
        head = said[:found.start()]
        clause = head[max(head.rfind("."), head.rfind(","), head.rfind(";")) + 1:]
        for figure in reversed(list(A_FIGURE_AND_UNIT.finditer(clause))):
            grams = _in_grams(float(figure.group("n")), figure.group("u"))
            if grams:
                return grams
        for figure in A_FIGURE_AND_UNIT.finditer(said):
            grams = _in_grams(float(figure.group("n")), figure.group("u"))
            if grams:
                return grams
    return 0.0


def _a_total(grams):
    if grams >= 1000:
        kilos = round(grams / 1000.0, 1)
        text = ("%g" % kilos)
        return text + " kg"
    return "%g g" % round(grams)


def the_portion_answer(memory):
    said = _the_last_answer(memory)
    if not said:
        return ""
    if not (AN_AMOUNT.search(said) or PER_PERSON.search(said) or FEEDS_A_COUNT.search(said)):
        return ""
    return said


def an_ask(text, memory):
    if not A_PORTION_ASK.search(text or ""):
        return False
    said = the_portion_answer(memory)
    if not said:
        return False
    counted = FEEDS_A_COUNT.search(said) or FOR_A_COUNT.search(said)
    if counted and not _a_time_not_a_portion(said, counted):
        return True
    return bool(PER_PERSON.search(said) and _the_per_head_figure(said))


def reply_for(text, memory):
    if not A_PORTION_ASK.search(text or ""):
        return None
    said = the_portion_answer(memory)
    if not said:
        return None
    counted = FEEDS_A_COUNT.search(said) or FOR_A_COUNT.search(said)
    if counted and not _a_time_not_a_portion(said, counted):
        number = _the_number(counted.group("n"))
        clause = _the_clause_with_the_count(said, counted.start(), counted.end())
        amount = AN_AMOUNT.search(clause)
        if amount:
            return ("That is for " + number + " - the answer puts it at "
                    + " ".join(amount.group(0).split()) + " in total.")
        return "That is for " + number + "."
    if PER_PERSON.search(said):
        grams = _the_per_head_figure(said)
        if not grams:
            return ("That is per person, so it goes up with however many you are feeding.")
        memory["portion"] = {"grams": grams, "turn": len(history.turns_before(memory))}
        return ("That is per person, not a total - say how many you are feeding and I will work "
                "the total out for you.")
    return None


_A_NEW_COUNTS = (
    re.compile(r"\b(?:make it|make that|we are|were|we'll be|we will be|there are|theres|"
               r"there's)\s+(?P<n>" + _NUMBER_WORD + r")(?:\s+not\s+(?P<old>" + _NUMBER_WORD + r"))?",
               re.I),
    re.compile(r"\b(?P<n>" + _NUMBER_WORD + r")\s+not\s+(?P<old>" + _NUMBER_WORD + r")\b", re.I),
    re.compile(r"\b(?:actually|no|sorry|oh|hang on)\s+(?P<n>" + _NUMBER_WORD + r")\b", re.I),
    re.compile(r"^\W*(?:and\s+|so\s+)?(?P<n>" + _NUMBER_WORD + r")\s+"
               r"(?:people|of us|guests|adults)\b", re.I),
)


_A_NUMBER_ANYWHERE = re.compile(r"\b(?:" + _NUMBER_WORD + r")\b", re.I)
_A_UNIT_AFTER = re.compile(r"\s*(?:kg|kilos?|grams?|g\b|ml|millilitres?|litres?|l\b|oz|ounces?|"
                           r"lbs?|pounds?)", re.I)


def _is_an_amount_not_a_count(text, found):
    tail = (text or "")[found.end("n"):]
    return bool(_A_UNIT_AFTER.match(tail))


def _says_two_counts(text, found):
    if found.groupdict().get("old"):
        return False
    return len(_A_NUMBER_ANYWHERE.findall(text or "")) > 1


def _the_new_count(text):
    for pattern in _A_NEW_COUNTS:
        found = pattern.search(text or "")
        if found and _as_a_count(found.group("n")):
            if _is_an_amount_not_a_count(text, found) or _says_two_counts(text, found):
                return None
            return found
    return None


A_CONFIRMATION = re.compile(
    r"\b(?:confirmed|confirm|yes|yep|yeah|yup|exactly|right|correct|thats right|that's right|"
    r"spot on|sure|indeed|definitely|probably|maybe)\b", re.I)


def _is_a_digit(word):
    return str(word or "").strip().isdigit()


def _the_count_they_gave(text):
    text = text or ""
    found = A_COUNT_OF_PEOPLE.search(text)
    if found:
        word = found.group("n") or found.group("m")
        count = _as_a_count(word)
        if count and count <= 500:
            return count, word
    for found in _A_NUMBER_ANYWHERE.finditer(text):
        word = found.group(0)
        count = _as_a_count(word)
        if not count or count > 500:
            continue
        if _is_a_digit(word) and not A_CONFIRMATION.search(text):
            continue
        return count, word
    return 0, ""


def _the_said_total(grams, count, count_word, old_word=None):
    if old_word:
        return ("Not " + _the_number(old_word) + " - " + _the_number(count_word) + ": about "
                + _a_total(grams * count) + " in total, at " + _a_total(grams) + " a head.")
    return ("About " + _a_total(grams * count) + " in total for " + _the_number(count_word)
            + " - that is " + _a_total(grams) + " a head.")


def _a_total_for_a_bare_count(text, memory):
    found = A_BARE_COUNT.search(text or "") or _the_new_count(text)
    if not found or _is_an_amount_not_a_count(text, found) or _says_two_counts(text, found):
        return None
    said = _the_last_answer(memory)
    if not said or not any(_counts_people(said, found) for found in PER_PERSON.finditer(said)):
        return None
    grams = _the_per_head_figure(said)
    if not grams:
        return None
    count = _as_a_count(found.group("n"))
    if not count or count > 500:
        return None
    old_word = found.groupdict().get("old")
    return _the_said_total(grams, count, found.group("n"), old_word)


def a_bare_count_to_fill(text, memory):
    if not isinstance(memory, dict):
        return False
    found = A_BARE_COUNT.search(text or "") or _the_new_count(text)
    if not found or _is_an_amount_not_a_count(text, found) or _says_two_counts(text, found):
        return False
    said = _the_last_answer(memory)
    if not said or not any(_counts_people(said, found) for found in PER_PERSON.finditer(said)):
        return False
    if not _the_per_head_figure(said):
        return False
    count = _as_a_count(found.group("n"))
    return bool(count) and count <= 500


def a_count_to_fill(text, memory):
    if not isinstance(memory, dict):
        return False
    portion = memory.get("portion")
    if not isinstance(portion, dict) or not portion.get("grams"):
        return False
    if len(history.turns_before(memory)) - int(portion.get("turn") or 0) > 1:
        return False
    return bool(_the_count_they_gave(text)[0])


def the_total_for(text, memory):
    if not isinstance(memory, dict):
        return None
    portion = memory.get("portion")
    if not isinstance(portion, dict) or not portion.get("grams"):
        return _a_total_for_a_bare_count(text, memory)
    if len(history.turns_before(memory)) - int(portion.get("turn") or 0) > 1:
        memory.pop("portion", None)
        return None
    count, said = _the_count_they_gave(text)
    if not count:
        return None
    memory.pop("portion", None)
    corrected = _the_new_count(text or "")
    old_word = (corrected.groupdict().get("old") if corrected is not None else None)
    return _the_said_total(float(portion["grams"]), count, said, old_word)
