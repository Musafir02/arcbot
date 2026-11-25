import re

from ..knowledge import units
from ..memory.spoken import _spoken_as_numbers
from ..memory.store_lines import (NUMBER_WORDS, _AMOUNTS, _AMOUNT_WORDS, _COUNT_WORD, _CONVERT,
                                  _UNIT_SAID, _WEEKLY)


ENOUGH_ASK = re.compile(
    r"\bis (?:that|this|it) (?:enough|too much|too little|too often|about right|alright|ok|okay"
    r"|fine|any good)\b"
    r"|\bam i (?:doing|getting|eating|drinking|having|sleeping) enough\b"
    r"|\bis that (?:a )?(?:good|healthy|normal|right) amount\b"
    r"|\b(?:will|would|does) that (?:be )?(?:enough|work|do|help)\b"
    r"|\bis\s+(?:\d[\d,]*(?:\.\d+)?|once|twice|one|two|three|four|five|six|seven|eight"
    r"|nine|ten|eleven|twelve)(?:[ -][a-z]{2,12}){0,2}\s+(?:enough|too much|too often"
    r"|too little|about right|alright|ok|okay|fine)\b",
    re.I,
)
HOW_MORE = re.compile(
    r"\bhow (?:much|many) (?:more|extra)\b|\bwhat (?:else|more) (?:do|should) i (?:need|add)\b",
    re.I,
)
_A_DOCTOR = re.compile(r"\b(?:see|talk to|speak to|ask|call)\s+(?:a|your|the|nhs|111)?\s*"
                       r"(?:gp|doctor|nurse|pharmacist|midwife|dentist|111)\b"
                       r"|\bworth (?:a |an |the )?(?:gp|doctor|nurse|check|visit|test|"
                       r"blood test|check-up|checking|seeing|getting|mentioning)\b"
                       r"|\bget (?:it|them|this) checked\b", re.I)
_A_LIMIT = re.compile(r"\blimits?\b|\bno more than\b|\bnot (?:more|much more) than\b"
                      r"|\bat most\b|\bcap(?:ped)?\b|\bcut (?:back|down)\b"
                      r"|\bkeep (?:it|them) (?:under|below)\b", re.I)
_A_TEMPERATURE = re.compile(r"\b\d{2,3}\s*(?:\u00b0\s*)?(?:c|degrees?|gas mark)\b"
                            r"|\buntil (?:the juices|it is cooked|browned|piping hot)\b", re.I)
def _a_value(word):
    word = (word or "").strip().lower()
    if re.fullmatch(r"\d+(?:,\d{3})*(?:\.\d+)?", word):
        return float(word.replace(",", ""))
    return float(_AMOUNT_WORDS.get(word, 0))


def _amount_family(unit):
    for family, pattern in _AMOUNTS:
        if re.fullmatch(pattern, unit.strip(), re.I):
            return family
    return ""


_HOURS_AND_MINUTES = re.compile(r"(" + _COUNT_WORD + r")\s*(?:hours?|hrs?)\s+(" + _COUNT_WORD
                                + r")\s*(?:minutes?|mins?)\b", re.I)


_A_PERIOD = re.compile(r"\s*(?:a|an|per|each|every|most)\s+(day|week|night|month)\b", re.I)


def _period_after(text, at):
    match = _A_PERIOD.match(text or "", at)
    if not match:
        return None
    return _WEEKLY if match.group(1).lower() == "week" else "a day"


def _a_period_near(text, phrase):
    at = (text or "").lower().find((phrase or "").lower())
    if at < 0 or not phrase:
        return None
    return _period_after(text, at + len(phrase))


def _the_period_of_the_answer(answer):
    for match in re.finditer(r"(?:a|per|each|every)\s+(day|week|night)\b", answer or "", re.I):
        return _WEEKLY if match.group(1).lower() == "week" else "a day"
    return None


def _the_periods_the_answer_says(answer):
    out = set()
    for match in re.finditer(r"(?:a|an|per|each|every)\s+(day|week|night|month|year)\b",
                             answer or "", re.I):
        word = match.group(1).lower()
        out.add({"week": _WEEKLY, "day": "a day", "night": "a day"}.get(word, "a " + word))
    return out


def _periods_disagree(mine, theirs, also=()):
    if mine is None:
        return False
    if mine in also:
        return False
    if theirs is None:
        return mine == _WEEKLY
    return mine != theirs


_TOO_FAR_ABOVE = 3.5
_TOO_FAR_BELOW = 20.0


def _too_far_to_compare(value, low, high):
    if not (value and low and high):
        return False
    if value > high and value > _TOO_FAR_ABOVE * high:
        return True
    if value < low and low > _TOO_FAR_BELOW * value:
        return True
    return False


def _amounts(text):
    text = _spoken_as_numbers(text)
    found = []
    spans = []
    for match in _HOURS_AND_MINUTES.finditer(text):
        hours, minutes = _a_value(match.group(1)), _a_value(match.group(2))
        if not (hours or minutes):
            continue
        found.append((hours * 60 + minutes, "minutes", match.group(0).strip(" .,!?")))
        spans.append((match.start(), match.end()))
    pattern = (r"(" + _COUNT_WORD + r")\s*(?:x\s*)?" + r"(" + "|".join(p for _, p in _AMOUNTS)
               + r")")
    for match in re.finditer(pattern, text, re.I):
        value = _a_value(match.group(1))
        if not value:
            continue
        if any(start <= match.start() and match.end() <= end for start, end in spans):
            continue
        found.append((value, _amount_family(match.group(2)), match.group(0).strip(" .,!?")))
    found.sort(key=lambda item: 0 if item[1] in ("a week", "a day") else 1)
    return found


def _target(answer, family, mine=None, bare_ok=False, period=None):
    answer = _spoken_as_numbers(answer)
    units = "|".join(p for _, p in _AMOUNTS)
    ranges, singles = [], []
    long_spans = [match.span() for match in _HOURS_AND_MINUTES.finditer(answer)]
    for match in re.finditer(r"(" + _COUNT_WORD + r")\s*(?:to|-|\u2013|and)\s*(" + _COUNT_WORD
                             + r")\s*(?:-\s*)?(" + units + r")", answer, re.I):
        if _amount_family(match.group(3)) != family:
            continue
        low, high = _a_value(match.group(1)), _a_value(match.group(2))
        if low and high and not _a_rate(answer, match.end()):
            ranges.append((match.start(), (low, high, match.group(0).strip(" .,!?"))))
    spans = [(match.start(), match.end()) for match, _ in
             ((m, None) for m in re.finditer(
                 r"(" + _COUNT_WORD + r")\s*(?:to|-|\u2013|and)\s*(" + _COUNT_WORD + r")\s*"
                 r"(?:-\s*)?(" + units + r")", answer, re.I))]
    for match in re.finditer(r"(" + _COUNT_WORD + r")\s*(" + units + r")\s*(?:to|-|\u2013|and)\s*"
                             r"(" + _COUNT_WORD + r")\s*(" + units + r")", answer, re.I):
        low_family, high_family = (_amount_family(match.group(2)),
                                   _amount_family(match.group(4)))
        if low_family == high_family:
            continue
        low, high = _a_value(match.group(1)), _a_value(match.group(3))
        if not (low and high):
            continue
        if family not in (low_family, high_family):
            continue
        low_in = low * _CONVERT.get((family, low_family), 1.0 if low_family == family else 0)
        high_in = high * _CONVERT.get((family, high_family),
                                      1.0 if high_family == family else 0)
        if not (low_in and high_in):
            continue
        said = "%s to %s %s" % (_the_number(int(low_in) if float(low_in).is_integer() else low_in),
                                 _the_number(int(high_in) if float(high_in).is_integer()
                                             else high_in),
                                 _UNIT_SAID.get(family, (family, family))[1])
        ranges.append((match.start(), (low_in, high_in, said)))
        spans.append((match.start(), match.end()))
    for match in re.finditer(r"(" + _COUNT_WORD + r")\s*(?:-\s*)?(" + units + r")", answer,
                             re.I):
        if _amount_family(match.group(2)) != family:
            continue
        if "-" in match.group(0):
            continue
        if any(start <= match.start() and match.end() <= end for start, end in spans + long_spans):
            continue
        value = _a_value(match.group(1))
        if value and not _a_rate(answer, match.end()):
            singles.append((match.start(), (value, value, match.group(0).strip(" .,!?"))))
    for match in _HOURS_AND_MINUTES.finditer(answer):
        hours, minutes = _a_value(match.group(1)), _a_value(match.group(2))
        if hours or minutes:
            total = hours * 60 + minutes
            singles.append((match.start(), (total, total, match.group(0).strip(" .,!?"))))
    ranges.sort(key=lambda item: item[0])
    singles.sort(key=lambda item: item[0])

    def is_their_number(figure):
        return mine is not None and figure[0] == figure[1] == mine

    useful = [(at, figure) for at, figure in singles if not (ranges and is_their_number(figure))]
    figures = [figure for _, figure in ranges] + [figure for _, figure in useful]
    if period and len({figure[:2] for figure in figures}) > 1:
        ranges_on = _the_periods_of(answer, ranges)
        useful_on = _the_periods_of(answer, useful)
        said_on = ranges_on + useful_on
        if (any(each == period for each in said_on)
                and any(each and each != period for each in said_on)):
            ranges = [pair for pair, each in zip(ranges, ranges_on) if each == period]
            useful = [pair for pair, each in zip(useful, useful_on) if each == period]
            figures = [figure for _, figure in ranges] + [figure for _, figure in useful]
    if len({figure[:2] for figure in figures}) > 1:
        if len({figure[:2] for figure in ranges}) == 1:
            best = ranges[0][1]
            if not is_their_number(best):
                return _with_its_period(answer, best, period)
        return None
    best = ranges[0][1] if ranges else (useful[0][1] if useful else None)
    if best is not None and not is_their_number(best):
        return _with_its_period(answer, best, period)
    bare = _near_bare_range(answer, mine, family) if bare_ok else None
    if bare is not None:
        return bare
    return _with_its_period(answer, best, period) if best is not None else None


_AIM_CUE = re.compile(r"\b(?:aim (?:for|at)|aims? (?:for|at)|target(?:s|ing)?\b|guideline|"
                      r"should (?:be|get|do|have)|try (?:for|to)|recommended|the idea is)\b", re.I)


def _the_aim_that_is_their_number(answer, family, mine):
    if not mine:
        return None
    units = "|".join(p for _, p in _AMOUNTS)
    for match in re.finditer(r"(" + _COUNT_WORD + r")\s*(?:-\s*)?(" + units + r")", answer or "",
                             re.I):
        if _amount_family(match.group(2)) != family:
            continue
        if _a_value(match.group(1)) != mine:
            continue
        before = (answer or "")[max(0, match.start() - 40):match.start()]
        if not _AIM_CUE.search(before):
            continue
        said = match.group(0).strip(" .,!?")
        period = _period_after(answer or "", match.end())
        if period:
            said += " " + ("a week" if period == _WEEKLY else "a day")
        return (mine, mine, said)
    return None


def _with_its_period(answer, figure, period):
    if not (period and figure):
        return figure
    at = (answer or "").find(figure[2])
    if at < 0:
        return figure
    match = _A_PERIOD.match(answer, at + len(figure[2]))
    if not match:
        return figure
    said = _WEEKLY if match.group(1).lower() == "week" else "a day"
    if said != period:
        return figure
    return (figure[0], figure[1], figure[2] + " " + match.group(0).strip(" .,!?"))


def _the_periods_of(answer, figures):
    out = []
    for at, figure in figures:
        match = _A_PERIOD.search(answer or "", at)
        if not match or match.start() > at + len(figure[2]) + 12:
            out.append(None)
            continue
        out.append(_WEEKLY if match.group(1).lower() == "week" else "a day")
    return out


def _aims_named(answer, mine, family):
    units = "|".join(p for _f, p in _AMOUNTS)
    found, spans = set(), []
    for match in re.finditer(r"(" + _COUNT_WORD + r")\s*(?:to|and|or|\u2013|-)\s*(" + _COUNT_WORD
                             + r")\s*(?:-\s*)?(" + units + r")?", answer, re.I):
        low, high = _a_value(match.group(1)), _a_value(match.group(2))
        if not (low and high and low < high):
            continue
        spans.append(match.span())
        said = match.group(3)
        if said and _amount_family(said) != family:
            continue
        found.add((low, high))
    for match in re.finditer(r"(" + _COUNT_WORD + r")\s*(?:-\s*)?(" + units + r")", answer,
                             re.I):
        if any(start <= match.start() and match.end() <= end for start, end in spans):
            continue
        spans.append(match.span())
        if _amount_family(match.group(2)) != family:
            continue
        value = _a_value(match.group(1))
        if value:
            found.add((value, value))
    for match in re.finditer(r"(" + _COUNT_WORD + r")", answer, re.I):
        if any(start <= match.start() and match.end() <= end for start, end in spans):
            continue
        value = _a_value(match.group(1))
        if not value or not (mine and mine / 3 <= value <= mine * 3):
            continue
        if _counts_things(answer, match.end()):
            continue
        found.add((value, value))
    return found


_PERIOD_WORDS = {"day", "days", "week", "weeks", "night", "nights", "month", "months", "year",
                 "years", "time", "times"}

_A_WORD_AFTER = re.compile(r"(?:\s+[a-z]+(?:-[a-z]+)?){1,4}")


def _counts_things(answer, at):
    match = _A_WORD_AFTER.match(answer or "", at)
    if not match:
        return False
    words = match.group(0).split()
    for at_word, word in enumerate(words):
        if _amount_family(word) is not None or word in _PERIOD_WORDS:
            return False
        if len(word) > 3 and word.endswith("s"):
            return not any(other in _PERIOD_WORDS or _amount_family(other) == "a week"
                           for other in words[at_word + 1:] + [""])
    return False


def _figures_in(answer):
    found = [value for value, _family, _said in _amounts(answer)]
    for match in re.finditer(r"(" + _COUNT_WORD + r")\s*(?:to|and|or|\u2013|-)\s*("
                             + _COUNT_WORD + r")\b", answer, re.I):
        low, high = _a_value(match.group(1)), _a_value(match.group(2))
        if low and high and low < high:
            found += [low, high]
    return found


def _a_rate(answer, end):
    return bool(re.match(r"\s*(?:%|per cent\b|percent\b|per (?:kilo|kg|kilogram|kilo of|pound|"
                         r"lb|100|head|person|day per)\b|g\s?/\s?kg\b|mg\s?/\s?kg\b)",
                         answer[end:end + 24], re.I))


def _another_kind_follows(answer, end, family):
    following = re.match(r"\s*(" + "|".join(p for _f, p in _AMOUNTS) + r")\b", answer[end:], re.I)
    return bool(following) and _amount_family(following.group(1)) != family


def _near_bare_range(answer, mine, family=None):
    for match in re.finditer(r"(" + _COUNT_WORD + r")\s*(?:to|and|or|\u2013|-)\s*("
                             + _COUNT_WORD + r")\b", answer, re.I):
        low, high = _a_value(match.group(1)), _a_value(match.group(2))
        if not (low and high and low < high):
            continue
        if mine is not None and not (low <= mine * 3 and mine <= high * 3):
            continue
        if family and _another_kind_follows(answer, match.end(), family):
            continue
        if _a_rate(answer, match.end()):
            continue
        return low, high, match.group(0).strip(" .,!?")
    return None


def _with_its_unit(aim, family, high, answer=""):
    pattern = dict(_AMOUNTS).get(family)
    if not pattern or re.search(pattern, aim, re.I):
        return aim
    if family in ("minutes", "hours") and re.search(r"\b(?:minutes?|mins?|hours?|hrs?)\b",
                                                    aim, re.I):
        return aim
    at = answer.find(aim)
    if at >= 0 and _another_kind_follows(answer, at + len(aim), family):
        return aim
    units = _UNIT_SAID.get(family)
    if not units:
        return aim
    return aim + " " + (units[0] if high == 1 else units[1])


def _the_number(value):
    whole = int(value) if float(value).is_integer() else value
    return str(whole)


def enough_reply(text, memory):
    if not isinstance(text, str):
        return None
    more = bool(HOW_MORE.search(text))
    if not more and not ENOUGH_ASK.search(text):
        return None
    turns = memory.get("turns") if isinstance(memory, dict) else None
    if not isinstance(turns, list) or not turns:
        return None
    last = turns[-1] if isinstance(turns[-1], dict) else {}
    if not (last.get("bot") or ""):
        return None
    too_much = bool(re.search(r"\btoo (?:much|often|many)\b", text, re.I))
    from ..memory import purse

    purse_reply = purse.against_the_bands(text, turns)
    if purse_reply:
        return purse_reply
    said = ""
    given = []
    for line_text in [text] + [str(t.get("user") or "") for t in reversed(turns)]:
        found = [item for item in _amounts(line_text) if item[1]]
        if found:
            given = found
            said = _spoken_as_numbers(line_text)
            break
    if not given:
        return _enough_bare(turns, text, more, too_much)
    mine_values = {value for value, _family, _said in given}
    reply = _enough_against(_candidate_answers(turns, mine_values), given, mine_values, said,
                            more, too_much)
    return reply


def _enough_bare(turns, text, more, too_much):
    mine = 0
    for line_text in [text] + [str(t.get("user") or "") for t in reversed(turns)]:
        bare = [value for value in _bare_figures(line_text) if value >= 100]
        if bare:
            mine = bare[0]
            break
    if not mine:
        return None
    for answer in _candidate_answers(turns, {mine}):
        found = _range_near(answer, mine)
        if not found:
            continue
        low, high = found[0], found[1]
        aim = found[2][0].lower() + found[2][1:]
        spoken = _the_number(mine)
        if spoken == "1":
            spoken = "one"
        if more:
            gap = low - mine
            if gap <= 0:
                return "None - %s is already at the %s that answer named." % (spoken, aim)
            return "%s more would put you at the %s that answer named." % (
                _the_number(round(gap, 1)), aim)
        if mine < low:
            return "%s is short of the %s that answer named." % (spoken, aim)
        if mine > high:
            return "%s is past the %s that answer named, so that side is worth watching." % (
                spoken, aim)
        return "No - %s is inside the %s that answer named, so you are fine." % (spoken, aim)


def _range_near(answer, mine):
    units = "|".join(pattern for _family, pattern in _AMOUNTS)
    for pattern in (r"(" + _COUNT_WORD + r")\s*(?:to|and|or|\u2013|-)\s*(" + _COUNT_WORD
                    + r")\s*(?:" + units + r")\b",
                    r"(" + _COUNT_WORD + r")\s*(?:to|and|or|\u2013|-)\s*(" + _COUNT_WORD
                    + r")\b"):
        for match in re.finditer(pattern, answer, re.I):
            low, high = _a_value(match.group(1)), _a_value(match.group(2))
            if not (low and high and low < high):
                continue
            if not (low <= mine * 3 and mine <= high * 3):
                continue
            return low, high, match.group(0).strip(" .,!?")
    return None


def _bare_figures(text):
    with_unit = [(match.start(), match.end()) for match in re.finditer(
        r"(" + _COUNT_WORD + r")\s*(?:-\s*)?(?:"
        + "|".join(pattern for _family, pattern in _AMOUNTS) + r")", text or "", re.I)]
    out = []
    for match in re.finditer(r"(" + _COUNT_WORD + r")", text or "", re.I):
        if any(start <= match.start() and match.end() <= end for start, end in with_unit):
            continue
        value = _a_value(match.group(1))
        if value:
            out.append(value)
    return out


def _candidate_answers(turns, mine_values):
    out = []
    for turn in reversed(turns[-3:]):
        answer = str(turn.get("bot") or "") if isinstance(turn, dict) else ""
        if not answer:
            continue
        if mine_values and not [figure for figure in _figures_in(answer)
                                if figure not in mine_values]:
            continue
        out.append(answer)
    return out


def _enough_against(answers, given, mine_values, said, more, too_much, quoted_ok=False):
    quoted = None
    for answer in answers:
        for value, family, spoken in given:
            if not family:
                continue
            if _periods_disagree(_a_period_near(said, spoken),
                                 _the_period_of_the_answer(answer),
                                 _the_periods_the_answer_says(answer)):
                continue
            if family in ("minutes", "hours") and _A_TEMPERATURE.search(answer):
                continue
            if _A_DOCTOR.search(answer):
                continue
            period = _a_period_near(said, spoken)
            read_family, read_value = family, value
            target = _target(answer, family, value, bare_ok=True, period=period)
            if not target:
                target = _the_aim_that_is_their_number(answer, family, value)
            if not target:
                for (mine, theirs), factor in _CONVERT.items():
                    if mine != family:
                        continue
                    other = _target(answer, theirs, period=period)
                    if not other:
                        other = _the_aim_that_is_their_number(
                            answer, theirs, round(value / factor, 4))
                    if other:
                        target = (other[0] * factor, other[1] * factor, other[2])
                        read_family, read_value = theirs, round(value / factor, 4)
                        break
            if not target:
                continue
            if (not quoted_ok and spoken and spoken.lower() in (target[2] or "").lower()
                    and abs(target[0] - value) < 1e-9 and abs(target[1] - value) < 1e-9
                    and not _AIM_CUE.search(answer)):
                if quoted is None:
                    quoted = (answer, [(value, family, spoken)])
                continue
            if len(_aims_named(answer, read_value, read_family)) > 2:
                continue
            if len(answer.split()) <= 12 and (target[2].lower() in said.lower()
                                             or spoken.lower() in answer.lower()):
                continue
            if mine_values and not [figure for figure in _figures_in(answer)
                                    if figure not in mine_values]:
                continue
            low, high = target[0], target[1]
            if _too_far_to_compare(value, low, high):
                continue
            aim = target[2][0].lower() + target[2][1:]
            aim = _with_its_unit(aim, family, high, answer)
            if more:
                gap = low - value
                if gap <= 0:
                    return "None - %s is already %s the %s that answer named." % (
                        spoken, "at" if value <= high else "past", aim)
                units = _UNIT_SAID.get(family)
                if not units:
                    continue
                said_unit = units[0] if gap == 1 else units[1]
                amount = _the_number(round(gap, 1))
                if amount == "1":
                    amount = "one"
                elif amount in ("2", "3", "4", "5", "6", "7", "8", "9", "10"):
                    amount = NUMBER_WORDS.get(int(amount), amount)
                if family in ("a week", "a day"):
                    return "%s more %s would put you at the %s that answer named." % (
                        amount[0].upper() + amount[1:], said_unit, aim)
                return "Another %s %s would put you at the %s that answer named." % (
                    amount, said_unit, aim)
            if too_much:
                if value > high:
                    if _A_LIMIT.search(answer):
                        return ("That is more than the %s that answer named, so trim it back "
                                "towards that." % aim)
                    return "That is more than the %s that answer named." % aim
                if low <= value <= high:
                    return "No - %s is inside the %s that answer named, so you are fine." % (
                        spoken[0].upper() + spoken[1:], aim)
                continue
            if value > high:
                return "%s is past the %s that answer named, so that side is worth watching." % (
                    spoken[0].upper() + spoken[1:], aim)
            if value >= high:
                at = "at the top of" if high > low else "at"
                return "%s is %s the %s that answer named, so you are there already." % (
                    spoken[0].upper() + spoken[1:], at, aim)
            if low <= value < high:
                return "%s is inside the %s that answer named, so you are fine." % (
                    spoken[0].upper() + spoken[1:], aim)
            if family in ("a week", "a day"):
                return "%s is under the %s that answer named - one more would put you there." % (
                    spoken[0].upper() + spoken[1:], aim)
            return "%s is short of the %s that answer named." % (
                spoken[0].upper() + spoken[1:], aim)
    if quoted:
        return _enough_against([quoted[0]], quoted[1], mine_values, said, more, too_much,
                               quoted_ok=True)
    return None
