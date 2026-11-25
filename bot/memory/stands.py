import re

from ..compose import pick

UNITS = frozenset("""week month day year hour minute second mile km kilo stone pound percent
    session run portion time glass cup litre pint degree inch cm metre gram ml""".split())

NUMBERS = {word: value for value, word in enumerate(
    "zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen "
    "fifteen sixteen seventeen eighteen nineteen twenty thirty forty fifty sixty seventy eighty "
    "ninety hundred".split())}
NUMBERS["couple"] = 2
NUMBERS["few"] = 3
NUMBERS["once"] = 1
NUMBERS["twice"] = 2
NUMBERS["thrice"] = 3

FIGURE = re.compile(
    r"\b(\d[\d,]*(?:\.\d+)?|" + "|".join(sorted(NUMBERS, key=len, reverse=True)) + r")"
    r"(?:\s+(" + "|".join(sorted(UNITS, key=len, reverse=True)) + r")s?\b)?", re.I)

NOTHING_NAMED = frozenset("""so and but or then ok okay right still is are was were am that
    this it they those these the a an of in on at for to do does did will would can could should
    my i me you we our yeah yes no anymore any more both quite really actually true correct
    stand stands work works hold holds apply applies changed change mean means all that's its
    it's again now today currently nowadays even just also too much very bit little""".split())

QUESTION_OPENING = re.compile(
    r"^\W*(?:(?:so|and|but|ok|okay|then|right|oh|also|now)\W+)*"
    r"(?:is|are|was|were|does|do|did|will|would|should|can|could)\b", re.I)
ASKING = re.compile(r"\b(?:still|right|correct|true|ok|okay|the same|sure)\b|\?", re.I)

MOST_WORDS = 9

LOOK_BACK = 5
SHORTEST_REASON = 6
MOST_REASON_WORDS = 45

SENTENCE = re.compile(r"(?<=[.!?])\s+")

STANDS = (
    "Still right: {reason}",
    "That has not changed: {reason}",
    "Yes - and that is where it comes from: {reason}",
)

CONFIRMS = (
    "Still right - {figure}.",
    "Yes, {figure} is still the number.",
    "That holds: {figure}, as before.",
)


def _number(word):
    word = str(word or "").strip(".,").lower()
    if not word:
        return None
    if word.replace(",", "").replace(".", "").isdigit():
        return float(word.replace(",", ""))
    return float(NUMBERS[word]) if word in NUMBERS else None


def _figures(text):
    found = []
    for match in FIGURE.finditer(str(text or "")):
        value = _number(match.group(1))
        if value is None:
            continue
        unit = (match.group(2) or "").lower().rstrip("s")
        found.append((value, unit, match.start(), match.end()))
    return found


def _names_the_figure(text, value, unit):
    for other, other_unit, _, _ in _figures(text):
        if other != value:
            continue
        if unit and unit != other_unit:
            continue
        return True
    return False


def _the_line_asks_about_a_figure_and_elsewhere_nothing(text):
    line = " ".join(str(text or "").lower().replace("\u2019", "'").split())
    if not line or len(line.split()) > MOST_WORDS:
        return None
    if not (QUESTION_OPENING.search(line) or ASKING.search(line)) or not ASKING.search(line):
        return None
    figures = _figures(line)
    if len(figures) != 1:
        return None
    value, unit, start, end = figures[0]
    rest = (line[:start] + " " + line[end:]).split()
    for word in rest:
        word = word.strip(".,!?;:")
        if word in NOTHING_NAMED or word.rstrip("s") in UNITS or word in ("a", "an", "per",
                                                                          "each", "every"):
            continue
        if word.rstrip("'s") in NOTHING_NAMED:
            continue
        return None
    return value, unit, line[start:end].strip()


def _the_chat_gave_it(memory, value, unit):
    if not isinstance(memory, dict):
        return False
    turns = memory.get("turns")
    if not isinstance(turns, list):
        return False
    return any(_names_the_figure(str(turn.get("bot") or ""), value, unit)
               for turn in turns[-LOOK_BACK:] if isinstance(turn, dict))


def _the_reason_behind(memory, value, unit):
    if not isinstance(memory, dict):
        return ""
    turns = memory.get("turns")
    if not isinstance(turns, list):
        return ""
    for turn in reversed(turns[-LOOK_BACK:]):
        said = str(turn.get("bot") or "") if isinstance(turn, dict) else ""
        if not said or not _names_the_figure(said, value, unit):
            continue
        for sentence in SENTENCE.split(said):
            sentence = sentence.strip()
            words = sentence.split()
            if not (SHORTEST_REASON <= len(words) <= MOST_REASON_WORDS):
                continue
            if _names_the_figure(sentence, value, unit):
                return sentence
    return ""


def the_figure_asked_about(text, memory):
    asked = _the_line_asks_about_a_figure_and_elsewhere_nothing(text)
    if not asked:
        return None
    value, unit, phrase = asked
    if not _the_chat_gave_it(memory, value, unit):
        return None
    return value, unit, phrase, _the_reason_behind(memory, value, unit)



CHANGE_ASK = re.compile(
    r"\b(?:does|do|will|would|should|did)\b[^.?!]{0,24}?"
    r"\b(?:change|affect|alter|make (?:a|any) difference to|matter (?:to|for)|impact)\b", re.I)
ATTRIBUTES = {
    "time": ("minute", "hour", "day", "week", "month"),
    "long": ("minute", "hour", "day", "week", "month"),
    "temperature": ("degree",),
    "heat": ("degree",),
}
ATTRIBUTE_WORDS = re.compile(
    r"\b(?:the|my|our|its)\s+(" + "|".join(ATTRIBUTES) + r"|cooking time|oven time|time)\b",
    re.I)
A_SETTING = re.compile(r"\b(?:boiler|thermostat|programmer|clock|timer|heating|timer\s+on)\b", re.I)
FIGURED = re.compile(
    r"\b(\d[\d,.]*(?:\s*(?:to|or|-)\s*\d[\d,.]*)?)\s*(hours?|hrs?)\s+(\d[\d,.]*)\s*"
    r"(minutes?|mins?)?\b(?!\s*(?:g|kg|ml|cl|lb|lbs|oz|cm|degrees?)\b)"
    r"|\b(\d[\d,.]*(?:\s*(?:to|or|-)\s*\d[\d,.]*)?)\s*"
    r"(minutes?|mins?|hours?|hrs?|days?|weeks?|months?|degrees?|C\b|\u00b0C)", re.I)
UNIT_FAMILY = {"minute": "time", "min": "time", "hour": "time", "hr": "time", "day": "time",
               "week": "time", "month": "time", "degree": "temperature", "c": "temperature",
               "°c": "temperature"}

CHANGE_REPLIES = {
    "time": (
        "No - {figure} was the time and it stays that. What changed is what goes in it, not how "
        "long it takes.",
        "That does not move it: {figure}, same as before.",
        "Same time - {figure}. The swap changes what is in it, not how long it is in for.",
        "The time holds: {figure}. It is the dish that sets it, not the filling.",
        "No change there - {figure}, and that is the figure to cook to.",
    ),
    "temperature": (
        "The heat holds: {figure}, same as before.",
        "No change to the heat - {figure}, and that is the oven to cook it at.",
        "Same heat - {figure}. The swap changes what goes in the dish, not the oven.",
        "That does not move it: {figure}, the heat it was already to be cooked at.",
    ),
}


CHANGE_REPLIES_MOVED = {
    "time": (
        "That moves it: {figure} now, not the time from before.",
        "It does - {figure} for this version.",
        "Yes - {figure}. The swap changes how long it takes.",
        "It does move it: {figure}, so cook to that instead.",
    ),
    "temperature": (
        "The heat moves too: {figure} for this version.",
        "It does - {figure} now, not the oven from before.",
        "Yes, the heat changes: {figure}.",
    ),
}


def _in_minutes(number, unit):
    value = _number(number)
    if value is None:
        return 0.0
    unit = unit.lower().rstrip("s")
    if unit in ("hour", "hr"):
        return value * 60
    if unit == "day":
        return value * 1440
    if unit == "week":
        return value * 10080
    if unit == "month":
        return value * 43200
    return value


def _the_best(candidates, family):
    if not candidates:
        return ""
    if family == "temperature":
        return candidates[0][2]
    best = max(candidates, key=lambda found: _in_minutes(found[0].split()[0], found[1]))
    return best[2]


def _figures_in_answer(said, family):
    candidates = []
    for match in FIGURED.finditer(str(said or "")):
        if match.group(1):
            whole = (f"{match.group(1)} {match.group(2).lower()} {match.group(3)} "
                     f"{(match.group(4) or 'minutes').lower()}")
            minutes = (_in_minutes(match.group(1), "hour")
                       + _in_minutes(match.group(3), "minute"))
            if family != "time":
                continue
            candidates.append((str(minutes), "minute", whole))
            continue
        unit = match.group(6).lower().rstrip("s")
        if UNIT_FAMILY.get(unit) != family:
            continue
        figure = f"{match.group(5)} {match.group(6).lower()}"
        if unit in ("c", "\u00b0c"):
            figure = f"{match.group(5)}C"
        candidates.append((match.group(5), match.group(6).lower(), figure))
    return candidates


def _the_same_figure(one, other):
    return re.sub(r"\D", "", str(one or "")) == re.sub(r"\D", "", str(other or ""))


NOT_THE_SUBJECT = frozenset("""minute minutes hour hours second seconds day days week weeks
    month months degree degrees oven ovens tray tins pan pans tin dish dishes cook cooking cooked
    bake baked roast roasted about until when then they this that with from your yours each every
    before after while total same time times heat high medium low fan""".split())


def _subjects(said):
    return {word for word in re.findall(r"[a-z]{4,}", str(said or "").lower())
            if word not in NOT_THE_SUBJECT}


def _about_the_same_thing(one, other):
    return bool(_subjects(one) & _subjects(other))


A_METHOD_CHANGE = re.compile(
    r"\b(?:slow cooker|crock ?pot|pressure cooker|instant pot|air ?fryer|microwave|steam\w*|"
    r"sous ?vide|barbecue|bbq|grill\w*|poach\w*|deep[- ]?fr(?:y|ied|ying)|boil\w*|"
    r"on the hob|in the oven instead|oven instead)\b", re.I)


def _a_figure_for(memory, family):
    if not isinstance(memory, dict):
        return "", False
    turns = memory.get("turns")
    if not isinstance(turns, list):
        return "", False
    answers = [str(turn.get("bot") or "") for turn in turns[-2:] if isinstance(turn, dict)]
    if not answers:
        return "", False
    plan = _the_best(_figures_in_answer(answers[0], family), family)
    swapped = (_the_best(_figures_in_answer(answers[1], family), family)
               if len(answers) > 1 else "")
    if not swapped:
        return plan, False
    if not plan:
        return swapped, True
    if _the_same_figure(swapped, plan):
        return plan, False
    if _about_the_same_thing(answers[0], answers[1]):
        return swapped, True
    said = str(turns[-1].get("user") or "") if isinstance(turns[-1], dict) else ""
    if A_METHOD_CHANGE.search(said):
        return "", False
    return plan, False


A_CHANGE = re.compile(
    r"\b(?:instead|rather than|without|swap\w*|switch\w*|replace\w*|substitut\w*|veggie|"
    r"vegetarian|vegan|gluten|dairy|free from|omitted|skipped|cut out|left out|leave out|"
    r"made it with|no [a-z]+)\b", re.I)


def _a_change_was_made(memory):
    if not isinstance(memory, dict):
        return False
    said = [str(turn.get("user") or "") for turn in (memory.get("turns") or [])
            if isinstance(turn, dict)]
    return any(A_CHANGE.search(line) for line in said[-3:])


QUANTITY = (r"(?:one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|fifteen|"
            r"twenty|thirty|\d+)")
WHOSE = r"(?:of us|people|guests?|kids?|portions?|slices|servings?|adults?|children)"
A_SIZE_CHANGE = re.compile(
    r"\b(?:bigger|larger|smaller|double|doubled|halve|halved|batch|twice as|half as)\b"
    r"|\b(?:more|extra|less|fewer)\s+" + WHOSE + r"\b"
    r"|\bfor\s+" + QUANTITY + r"\b"
    r"|\bfor\s+(?:\w+\s+)?" + WHOSE + r"\b"
    r"|\b(?:feed|feeding|cooking for)\s+(?:" + QUANTITY + r"|" + WHOSE + r")\b"
    r"|\b" + QUANTITY + r"\s*" + WHOSE + r"\b"
    r"|\b(?:there will be|there are|its|it's|so its|so it's|now)\s+(?:one|two|three|four|five|"
    r"six|seven|eight|nine|ten|eleven|twelve|twenty|\d+)\b", re.I)


def _a_change_of_size(memory):
    if not isinstance(memory, dict):
        return False
    said = [str(turn.get("user") or "") for turn in (memory.get("turns") or [])
            if isinstance(turn, dict)]
    return any(A_SIZE_CHANGE.search(line) for line in said[-3:])


def the_change_asked_about(text, memory):
    line = " ".join(str(text or "").lower().replace("\u2019", "'").split())
    if not line or len(line.split()) > MOST_WORDS + 3:
        return None
    if not CHANGE_ASK.search(line) or A_SETTING.search(line):
        return None
    if _a_change_of_size(memory) or not _a_change_was_made(memory):
        return None
    named = ATTRIBUTE_WORDS.search(line)
    if not named:
        return None
    word = named.group(1).lower()
    if word in ("time", "cooking time", "oven time", "long"):
        attribute, family = "time", "time"
    elif word in ("temperature", "heat"):
        attribute, family = "temperature", "temperature"
    else:
        return None
    rest = line[:named.start(1)] + " " + line[named.end(1):]
    for word_ in rest.split():
        word_ = word_.strip(".,!?;:")
        if not word_ or word_ in NOTHING_NAMED or word_ in ("that", "this", "it", "which"):
            continue
        if word_ in ("change", "changed", "changes", "affect", "affects", "alter", "alters",
                     "impact", "matter", "difference", "make", "makes", "made", "a", "an",
                     "any", "to", "for", "the", "on", "of", "in", "with", "much", "long",
                     "time", "cooking", "oven"):
            continue
        return None
    figure, moved = _a_figure_for(memory, family)
    if not figure:
        return None
    return attribute, figure, moved


def change_reply(text, memory):
    found = the_change_asked_about(text, memory)
    if not found:
        return None
    attribute, figure, moved = found
    line = " ".join(str(text or "").lower().split())
    pools = CHANGE_REPLIES_MOVED if moved else CHANGE_REPLIES
    pool = pools.get(attribute) or pools["time"]
    return pick(pool, memory, line).format(figure=figure)


def reply_for(text, memory):
    found = the_figure_asked_about(text, memory)
    if not found:
        return None
    _, _, phrase, reason = found
    line = " ".join(str(text or "").lower().split())
    if not reason:
        return pick(CONFIRMS, memory, line).format(figure=phrase)
    return pick(STANDS, memory, line).format(reason=reason)

