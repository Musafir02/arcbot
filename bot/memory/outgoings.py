import re

SUM = re.compile(
    r"£\s*(?P<marked>\d[\d,]*(?:\.\d+)?)\s*(?P<marked_unit>k|grand|thousand)?"
    r"|(?P<bare>\d[\d,]*(?:\.\d+)?)\s*(?P<bare_unit>k|grand|thousand|pounds?|quid)\b",
    re.I,
)
BARE_NUMBER = re.compile(r"\d[\d,]*(?:\.\d+)?")

INCOME = re.compile(
    r"\b(?:i|we)(?:'m|m|'re| are)?\s+(?:on|earn|earns|make|makes|bring\s+in|brings\s+in|get|gets)\b"
    r"|\btake[\s-]?home\b"
    r"|\b(?:my|our)\s+(?:pay|wage|wages|salary|pension|income|earnings)\b"
    r"|\bafter\s+tax\b"
    r"|\b(?:partner|husband|wife)\s+(?:earns?|makes?|brings?\s+in|gets?|takes?\s+home)\b",
    re.I,
)
FIXED_COST = re.compile(
    r"\b(?:rents?|mortgage|childcare|child\s*care|childminder|nursery|nursery\s+fees|"
    r"school\s+(?:fees|dinners|clubs?)|breakfast\s+club|after[\s-]school\s+club|"
    r"council\s+tax|bills?|utility|utilities|energy|electric(?:ity)?|water|gas|heating|"
    r"broadband|internet|phone|mobile|tv\s+licen[cs]e|car\s+finance|car\s+payment|"
    r"car\s+insurance|loan|loans|repayments?|insurance|commut\w*|travel|fares?|transport|"
    r"petrol|diesel|fuel|parking|tolls?|train\s+fare|season\s+ticket|bus\s+pass|"
    r"subscriptions?|gym|clothes|uniforms?|nappies|food|groceries|shopping|"
    r"car|van|pets?|vets?|vet\s+bills?|medicines?|prescriptions?|dentist|"
    r"child\s+maintenance|maintenance)\b",
    re.I,
)
AFTER_THE_FIGURE = re.compile(
    r"^\s*(?:a\s+(?:month|week|year|fortnight)\s*)?(?:goes?|went|is\s+spent|are\s+spent)?\s*"
    r"(?:on|for|towards|into)\s+(?P<noun>[a-z][a-z'\-]*)",
    re.I,
)
NOT_A_COST_NAME = re.compile(
    r"^(?:a|an|the|it|them|that|this|me|us|him|her|his|my|our|their|its|and|or|so|but|if|when|"
    r"top|all|everything|nothing|stuff|things?)$",
    re.I,
)
MONTH = re.compile(
    r"\b(?:a|per|each|every)\s+month\b|\bmonthly\b|\bpcm\b|\b(?:a|per)\s+4\s+weeks\b", re.I)
WEEK = re.compile(r"\b(?:a|per|each|every)\s+week\b|\bweekly\b", re.I)
YEAR = re.compile(
    r"\b(?:a|per|each|every)\s+year\b|\byearly\b|\bannually\b|\ba\s+year\b|\bp\.?a\.?\b", re.I)

NOT_A_BUDGET_LINE = re.compile(
    r"\b(?:arrears?|behind|overdue|evict\w*|notice|can'?t\s+pay|cant\s+pay|couldn'?t\s+pay|"
    r"not\s+paid|unpaid|short\s+this\s+month|owing|owe|owed|debt|debts|default\w*|bailiff\w*|"
    r"due|going\s+up|went\s+up|go\s+up|gone\s+up|goes\s+up|rising|increas\w*|raise[sd]?|cheaper|"
    r"reduce|reducing|lower|negotiate|"
    r"landlord|housing\s+benefit|universal\s+credit)\b",
    re.I,
)
AN_ASK = re.compile(
    r"^\s*(?:should|could|can|do|does|is|are|was|were|what|how|when|where|which|why|would|will)\b"
    r"|[,;]\s*(?:should|could|can|do|does|is|are|was|were|what|how|when|where|which|why|would|"
    r"will)\s+\w"
    r"|\?\s*$",
    re.I,
)
A_MEASURE = re.compile(
    r"^\s*(?:mins?|minutes?|hours?|hrs?|days?|weeks?|months?|years?|miles?|km|kg|bed(?:room)?s?|"
    r"kids?|people|guests?|percent|%)",
    re.I,
)
A_CODE = re.compile(r"\b\d{3,}[A-Za-z]{1,2}\b")
A_HAND_HELD = re.compile(
    r"\b(?:put|set|stick)\s+(?:\u00a3?\d[\d,]*(?:\.\d+)?\s+)?(?:by|aside|away)\b"
    r"|\b(?:save[sd]?|saving|savings|pot|putting\s+by)\b",
    re.I,
)

_THE_COST = {"rents": "rent", "bills": "bills", "loans": "loan payments", "repayments": "repayment"}

LOW_SHARE = 0.10
HIGH_SHARE = 0.20

LEFT = (
    "That leaves {left} after the {named}. Food, travel and the rest come out of that, and whatever "
    "is over at the end is what you can put by.",
    "{left} left after the {named}, then. A standing order for the amount you want to keep, on the "
    "day after payday, takes it out before you can spend it.",
    "So {in_amount} in and {out_amount} out on the {named} leaves {left}. Pick the figure you want "
    "to keep and move it the day you are paid.",
)
A_YEAR_AND_A_MONTH = (
    "{in_amount} a year is about {a_month} a month, so the {named} leaves {left}.",
    "{in_amount} a year works out at {a_month} a month, and after the {named} there is {left}.",
)
FIRST_MOVE = (
    "Set the standing order first: choose the figure you want to keep and move it the day after you "
    "are paid, so the month runs on what is left rather than the other way round.",
    "Start with the standing order on payday for the figure you want to keep. Everything else in the "
    "month can move around it.",
)
A_FIRST_ASK = re.compile(
    r"\b(?:what|where)\s+(?:should|do|shall)\s+i\s+(?:do|start|begin)\b[^.?!]*\b"
    r"(?:first|next|now|start)\b"
    r"|\bhow\s+do\s+i\s+(?:start|begin)\b"
    r"|\bwhere\s+(?:do|should)\s+i\s+(?:even\s+)?(?:start|begin)\b"
    r"|\bwhat'?s\s+(?:the\s+)?first\s+(?:step|thing)\b",
    re.I,
)
A_LEFT_ASK = re.compile(
    r"\bwhat'?s\s+left\b|\bwhat\s+is\s+left\b|\bwhat'?s\s+left\s+over\b|"
    r"\bhow\s+much\s+(?:is\s+left|left|do\s+i\s+have\s+left|have\s+i\s+(?:got\s+)?left)\b",
    re.I,
)
LEFT_AGAIN = (
    "{left} {unit}, on the figures you gave.",
    "Same sum, on the figures you gave: {left} {unit}.",
)
A_STEP_ASK_POINTS_BACK = re.compile(
    r"\b(?:that|this|it|them|those|these|now|next|first|then|month|months|money|save|saves|saving|"
    r"savings|budget|budgeting|pay|paid|payday|salary|wage|income|rent|bills?|pot|aside|afford)\b",
    re.I,
)
A_SHARE = (
    "A tenth to a fifth of {in_amount} is {low} to {high} {period}, which is the usual amount to "
    "put by.",
    "Put by a tenth to a fifth of it: {low} to {high} {period}, out of {in_amount}.",
)


def _choice(shape, line, memory=None):
    was = ""
    if isinstance(memory, dict):
        turns = memory.get("turns") or ()
        if turns and isinstance(turns[-1], dict):
            was = str(turns[-1].get("bot") or "")
    start = sum(map(ord, str(line or ""))) % len(shape)
    for step in range(len(shape)):
        candidate = shape[(start + step) % len(shape)]
        opener = candidate.split("{")[0].strip()
        if not opener or opener[:28] not in was:
            return candidate
    return shape[start]


def _the_names(costs):
    names = []
    for name, _value in costs:
        name = _THE_COST.get(name, name)
        if name not in names:
            names.append(name)
    if len(names) == 1:
        return names[0]
    if len(names) == 2:
        return "%s and the %s" % (names[0], names[1])
    return "%s and the %s" % (", ".join(names[:-1]), names[-1])


def _sums(text):
    found = []
    taken = []
    for match in SUM.finditer(text):
        value = match.group("marked") or match.group("bare")
        unit = (match.group("marked_unit") or match.group("bare_unit") or "").lower()
        try:
            number = float(value.replace(",", ""))
        except (TypeError, ValueError):
            continue
        if unit in ("k", "grand", "thousand"):
            number *= 1000
        if text[match.end():match.end() + 1].isalpha() or A_MEASURE.match(text[match.end():]):
            continue
        if number >= 20:
            found.append((number, match.start(), match.end()))
            taken.append((match.start(), match.end()))
    for match in BARE_NUMBER.finditer(text):
        if any(start <= match.start() < end for start, end in taken):
            continue
        if text[match.end():match.end() + 1].isalpha() or A_MEASURE.match(text[match.end():]):
            continue
        try:
            number = float(match.group(0).replace(",", ""))
        except ValueError:
            continue
        if number >= 20:
            found.append((number, match.start(), match.end()))
    found.sort(key=lambda item: item[1])
    return found


def _period(text):
    if WEEK.search(text):
        return "a week"
    if YEAR.search(text):
        return "a year"
    if MONTH.search(text):
        return "a month"
    return ""


def _units_in(text):
    found = set()
    for pattern, unit in ((MONTH, "a month"), (WEEK, "a week"), (YEAR, "a year")):
        if pattern.search(text):
            found.add(unit)
    return found


def _pounds(value):
    if abs(value - round(value)) < 0.005:
        return "£%s" % format(int(round(value)), ",")
    return "£%s" % format(round(value, 2), ",.2f")


def _with_unit(value, unit):
    figure = _pounds(value)
    return "%s %s" % (figure, unit) if unit else figure


def _in_phrase(text, start, end, pattern, span=18):
    return bool(pattern.search(text[max(0, start - span):end + span]))


def _near(text, start, end, pattern, before=30, after=30):
    return bool(pattern.search(text[max(0, start - before):start])) or \
        bool(pattern.search(text[end:end + after]))


def _the_nearest(line, cue, sums, after=20, before=6):
    best = None
    for value, start, end in sums:
        gap = start - cue.end()
        if 0 <= gap <= after:
            distance = gap
        else:
            gap = cue.start() - end
            if not 0 <= gap <= before:
                continue
            distance = gap
        if best is None or distance < best[0]:
            best = (distance, value, start, end)
    return best


def _the_incomes_in_the_line(line, sums=None):
    if not line or not INCOME.search(line) or A_CODE.search(line):
        return []
    if sums is None:
        sums = _sums(line)
    found = []
    seen = []
    for cue in INCOME.finditer(line):
        nearest = _the_nearest(line, cue, sums, after=20, before=8)
        if not nearest:
            continue
        _distance, value, start, end = nearest
        if start in seen:
            continue
        seen.append(start)
        found.append((value, start, end))
    return found


def the_income_in_the_line(text):
    line = str(text or "")
    if not line:
        return None
    incomes = _the_incomes_in_the_line(line)
    if not incomes:
        return None
    return sum(value for value, _start, _end in incomes), _period(line)


def _the_cost_the_figure_is_for(line, start, end):
    before = line[max(0, start - 26):start]
    after = line[end:end + 26]
    best = None
    for match in FIXED_COST.finditer(before):
        distance = len(before) - match.end()
        if best is None or distance < best[0]:
            best = (distance, match.group(0).lower())
    for match in FIXED_COST.finditer(after):
        distance = match.start()
        if best is None or distance < best[0]:
            best = (distance, match.group(0).lower())
    if best:
        return best[1]
    on_shape = AFTER_THE_FIGURE.match(after)
    if on_shape and not NOT_A_COST_NAME.match(on_shape.group("noun")):
        return on_shape.group("noun").lower()
    return ""


def _the_unit_beside(line, end):
    tail = line[end:end + 16]
    for pattern, unit in ((MONTH, "a month"), (WEEK, "a week"), (YEAR, "a year")):
        match = pattern.search(tail)
        if match and not tail[:match.start()].strip(" ,-"):
            return unit
    return ""


def the_costs_with_units_in_the_line(text):
    line = str(text or "")
    if not line:
        return []
    sums = _sums(line)
    incomes = set(start for _value, start, _end in _the_incomes_in_the_line(line, sums))
    found = []
    for value, start, end in sums:
        if start in incomes:
            continue
        if _in_phrase(line, start, end, A_HAND_HELD):
            continue
        name = _the_cost_the_figure_is_for(line, start, end)
        if not name:
            return []
        found.append((name, value, _the_unit_beside(line, end)))
    return found


def the_outgoings_in_the_line(text):
    return [(name, value) for name, value, _unit in the_costs_with_units_in_the_line(text)]


def _there_is_memory(memory):
    if not isinstance(memory, dict):
        return False
    for turn in memory.get("turns") or []:
        if not isinstance(turn, dict):
            continue
        if str(turn.get("user") or "").strip() or str(turn.get("bot") or "").strip():
            return True
    return False


def _the_income_before(memory):
    if not isinstance(memory, dict):
        return None
    seen = 0
    for turn in reversed(list(memory.get("turns") or [])):
        line = turn.get("user") if isinstance(turn, dict) else None
        if not isinstance(line, str) or not line.strip():
            continue
        seen += 1
        if seen > 2:
            return None
        income = the_income_in_the_line(line)
        if income:
            return income
    return None


def _the_costs_before(memory):
    if not isinstance(memory, dict):
        return []
    found = []
    seen = 0
    for turn in reversed(list(memory.get("turns") or [])):
        line = turn.get("user") if isinstance(turn, dict) else None
        if not isinstance(line, str) or not line.strip():
            continue
        seen += 1
        if seen > 2:
            break
        found = the_outgoings_in_the_line(line) + found
    return found


def _remember(memory, left, unit):
    if isinstance(memory, dict):
        memory["the_month_set_out"] = {"left": left, "unit": unit}


def _the_pot_in_the_line(text):
    line = str(text or "")
    for value, start, end in _sums(line):
        if _in_phrase(line, start, end, A_HAND_HELD):
            return value
    return 0


def _the_left_again(line, memory):
    month = memory.get("the_month_set_out") if isinstance(memory, dict) else None
    if not isinstance(month, dict):
        return ""
    left = month.get("left")
    unit = month.get("unit") or "a month"
    if not left or left <= 0:
        return ""
    return _choice(LEFT_AGAIN, line, memory).format(
        left="\u00a3{:,}".format(int(round(float(left)))), unit=unit)


def _the_ask_points_back(line):
    if A_STEP_ASK_POINTS_BACK.search(line):
        return True
    return len(re.findall(r"[A-Za-z']+", line)) <= 4


def _the_month_was_just_set_out(memory):
    if not isinstance(memory, dict) or not memory.get("the_month_set_out"):
        return False
    turns = memory.get("turns") or ()
    if not turns or not isinstance(turns[-1], dict):
        return False
    said = str(turns[-1].get("bot") or "")
    return bool(re.search(r"\bleaves \u00a3|\bleft after the\b", said))


def _the_unit_in_the_chat(memory):
    if not isinstance(memory, dict):
        return ""
    for turn in reversed(list(memory.get("turns") or [])[-2:]):
        line = turn.get("user") if isinstance(turn, dict) else ""
        if isinstance(line, str):
            unit = _period(line)
            if unit:
                return unit
    return ""


def _the_chat_is_about_saving(memory):
    if not isinstance(memory, dict):
        return False
    said = []
    for turn in list(memory.get("turns") or [])[-2:]:
        if isinstance(turn, dict):
            said.append(str(turn.get("user") or ""))
            said.append(str(turn.get("bot") or ""))
    return bool(re.search(r"\b(?:save|saves|saving|savings|put\s+(?:by|aside|away)|budget|"
                          r"deposit|putting\s+by)\b", " ".join(said), re.I))


def reply_for(text, memory=None):
    line = str(text or "").strip()
    if not line or len(line) > 220:
        return ""
    if A_LEFT_ASK.search(line) and _the_month_was_just_set_out(memory):
        return _the_left_again(line, memory)
    if A_FIRST_ASK.search(line) and _the_month_was_just_set_out(memory) \
            and _the_ask_points_back(line):
        return _choice(FIRST_MOVE, line, memory)
    if NOT_A_BUDGET_LINE.search(line) or AN_ASK.search(line):
        return ""
    if len(_units_in(line)) > 1:
        return ""
    unit = _period(line)
    income = the_income_in_the_line(line)
    with_units = the_costs_with_units_in_the_line(line)
    costs = [(name, value) for name, value, _said in with_units]
    if not _there_is_memory(memory) and not (income and costs):
        return ""
    if income and not unit:
        income = (income[0], _the_unit_in_the_chat(memory))
    own_month = bool(income)
    if not income:
        earlier = _the_income_before(memory)
        if not earlier or not costs:
            return ""
        income = (earlier[0], earlier[1] or unit or _the_unit_in_the_chat(memory))
    value, unit = income
    if costs:
        before = []
        if not own_month:
            before = [cost for cost in _the_costs_before(memory)
                      if cost[0] not in [name for name, _value in costs]]
        costs = before + costs
        cost = costs[-1][1]
        named = _the_names(costs)
        cost_unit = with_units[-1][2] if with_units else ""
        if len(costs) == 1 and cost_unit and cost_unit != unit:
            return ""
        if unit == "a year" and cost_unit != "a year":
            a_month = round(value / 12.0)
            left = a_month - sum(cost for _name, cost in costs)
            if left <= 0 or left < a_month * 0.05:
                return ""
            _remember(memory, left, "a month")
            return _choice(A_YEAR_AND_A_MONTH, line, memory).format(
                in_amount=_pounds(value), a_month=_pounds(a_month), named=named,
                left=_with_unit(left, "a month"))
        left = value - sum(cost for _name, cost in costs)
        if left <= 0 or left < value * 0.05:
            return ""
        spent_all = sum(amount for _name, amount in costs)
        pot = _the_pot_in_the_line(line)
        reply = _choice(LEFT, line, memory).format(
            left=_with_unit(left, unit), named=named, in_amount=_pounds(value),
            out_amount=_pounds(spent_all))
        if pot:
            reply += " The %s you put by comes out of that." % _pounds(pot)
        _remember(memory, left, unit)
        return reply
    if not _the_chat_is_about_saving(memory):
        return ""
    if not unit:
        return ""
    return _choice(A_SHARE, line, memory).format(in_amount=_pounds(value),
                                         low=_pounds(value * LOW_SHARE),
                                         high=_pounds(value * HIGH_SHARE), period=unit)
