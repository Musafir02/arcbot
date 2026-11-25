
import re

_COUNT = (r"(?:\d[\d,]*(?:\.\d+)?|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve)")

_THINGS = (
    ("glasses", r"glasses?"),
    ("steps", r"steps?"),
    ("minutes", r"minutes?|mins?"),
    ("hours", r"hours?|hrs?"),
    ("grams", r"grams?|grammes?|g"),
    ("milligrams", r"milligrams?|mg"),
    ("micrograms", r"micrograms?|mcg"),
    ("kilometres", r"kilometres?|kilometers?|kms?"),
    ("miles", r"miles?"),
    ("sessions", r"sessions?"),
)

A_THEIR_OWN = re.compile(r"\b(?:i|we)\b[^.?!]{0,24}?\b(?:have|had|get|got|do|eat|drink|walk|run"
                         r"|take|use|manage|average|track|log|hit|only|now|usually|normally"
                         r"|still|am on)\b", re.I)

A_AN_ASK = re.compile(r"\?|^\s*(?:how|what|which|why|when|where|who|should|can|could|do|does|did"
                      r"|is|are|was|were|will|would|any|got any)\b", re.I)

A_A_LENGTH_OF = re.compile(r"\b" + _COUNT + r"\s*(?:hours?|hrs?|minutes?|mins?)\s+of\s+\w", re.I)

_COUNT_WORDS = {1: "one", 2: "two", 3: "three", 4: "four", 5: "five", 6: "six", 7: "seven",
                8: "eight", 9: "nine", 10: "ten", 11: "eleven", 12: "twelve"}


def _a_value(word):
    word = (word or "").strip().lower().replace(",", "")
    try:
        return float(word)
    except ValueError:
        pass
    return float(list(_COUNT_WORDS.values()).index(word) + 1) if word in _COUNT_WORDS.values() \
        else None


def _a_number(value):
    if value == int(value) and int(value) in _COUNT_WORDS:
        return _COUNT_WORDS[int(value)]
    return "{:,}".format(int(value)) if value == int(value) else str(value)


def _counts(text):
    found = []
    for thing, pattern in _THINGS:
        for match in re.finditer(r"(" + _COUNT + r")\s*(?:-\s*)?(?:" + pattern + r")\b",
                                 text or "", re.I):
            value = _a_value(match.group(1))
            if value is None:
                continue
            found.append({"at": match.start(), "value": value, "thing": thing,
                          "said": match.group(0).strip(" .,!?"),
                          "period": _the_period_at(text, match.end())})
    found.sort(key=lambda item: item["at"])
    return found


def _the_period_at(text, at):
    match = re.match(r"\s*(?:a|an|per|each|every|most)\s+(day|week|night|month)\b",
                     (text or "")[at:], re.I)
    if not match:
        return None
    return "a week" if match.group(1).lower() in ("week", "month") else "a day"


def a_count_they_report(text):
    if not isinstance(text, str) or not text.strip():
        return None
    if A_AN_ASK.search(text) or not A_THEIR_OWN.search(text):
        return None
    if A_A_LENGTH_OF.search(text):
        return None
    found = _counts(text)
    if len(found) != 1:
        return None
    return found[0]


def _the_figure_named(answer, thing, mine):
    pattern = dict(_THINGS).get(thing)
    if not pattern or not answer:
        return None
    ranges = list(re.finditer(r"(" + _COUNT + r")\s*(?:to|-|\u2013|and|or)\s*(" + _COUNT + r")"
                              r"\s*(?:-\s*)?(?:" + pattern + r")\b", answer, re.I))
    spans = [match.span() for match in ranges]
    singles = [match for match in re.finditer(r"(" + _COUNT + r")\s*(?:-\s*)?(?:" + pattern
                                              + r")\b", answer, re.I)
               if not any(start <= match.start() and match.end() <= end for start, end in spans)]
    figures = []
    for match in ranges:
        low, high = _a_value(match.group(1)), _a_value(match.group(2))
        if low is None or high is None or low >= high:
            continue
        figures.append({"low": low, "high": high, "said": match.group(0).strip(" .,!?"),
                        "period": _the_period_at(answer, match.end())})
    for match in singles:
        value = _a_value(match.group(1))
        if value is None:
            continue
        figures.append({"low": value, "high": value, "said": match.group(0).strip(" .,!?"),
                        "period": _the_period_at(answer, match.end())})
    named = len(figures)
    figures = [figure for figure in figures
               if not (figure["low"] == figure["high"] == mine)]
    if named > 1 and figures:
        return None
    if len(figures) != 1:
        return None
    return figures[0]


def _the_periods_disagree(mine, theirs):
    if mine is None or theirs is None:
        return False
    return mine != theirs


def against_the_last_answer(said, answer):
    if not isinstance(said, dict):
        return None
    figure = _the_figure_named(answer, said.get("thing"), said.get("value"))
    if figure is None:
        return None
    if _the_periods_disagree(said.get("period"), figure.get("period")):
        return None
    if figure["low"] <= 0:
        return None
    return {"thing": said["thing"], "mine": said["value"], "mine_said": said["said"],
            "low": figure["low"], "high": figure["high"], "figure": figure["said"],
            "figure_period": figure.get("period"),
            "a_ceiling": bool(A_CEILING.search(answer or ""))}


def _the_figure_said(against):
    said = "the " + _a_mid_sentence(against["figure"])
    period = against.get("figure_period")
    if period and period not in said:
        said += " " + period
    return said


def _a_mid_sentence(figure):
    word = (figure or "").split(" ")[0]
    if word[:1].isupper() and word.lower() in _COUNT_WORDS.values():
        return figure[0].lower() + figure[1:]
    return figure


A_CEILING = re.compile(r"\blimits?\b|\bno more than\b|\bat most\b|\bcap(?:ped)?\b"
                       r"|\bsafe (?:limit|amount|upper)\b|\bdo not (?:go )?(?:over|exceed)\b",
                       re.I)


def _the_aim_said(against):
    said = _a_mid_sentence(against["figure"])
    aim = "the " + said
    period = against.get("figure_period")
    if period and aim.endswith(" " + period):
        aim = aim[: -len(period) - 1]
    return aim


def the_comparison(against):
    mine, low, high = against["mine"], against["low"], against["high"]
    aim, said = _the_aim_said(against), against["mine_said"]
    if against.get("a_ceiling"):
        if mine > high:
            return "That is over {}, which is worth trimming back.".format(aim)
        if mine < low:
            return "That is under {}, which is where you want to be.".format(aim)
        return "That is inside {}, which is fine - that is a ceiling, not a target.".format(aim)
    if mine < low:
        return "That is a fair way under {} most people need.".format(aim)
    if mine > high:
        return "That is past {}, which is fine - more than that is no problem.".format(aim)
    return "That is inside {} most people need.".format(aim)
