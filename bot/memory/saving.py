import re

SAVING = re.compile(r"\b(?:save|saves|saving|saved|savings|saving up|putting by|putting away|"
                    r"putting\b[^.?]{0,18}?\b(?:by|away|aside)|put\b[^.?]{0,18}?\b(?:by|away|aside)|"
                    r"setting aside|stashing|put by|put away|set aside|stash|pot|fund)\b", re.I)
SUM = re.compile(r"(?:£|\$|\u20ac)\s*(\d[\d,]*(?:\.\d+)?)\s*(k|grand|thousand)?"
                 r"|\b(\d[\d,]*(?:\.\d+)?)\s*(k|grand|thousand|pounds|quid|euros|dollars|bucks)\b",
                 re.I)
NOT_A_POT = re.compile(r"\s*(?:on|off|from|for)\s+(?:my|the|our|a|an|each|every|it)\b|"
                       r"\s*a\s+(?:month|week|year)\s+(?:on|off|from)\b", re.I)
BARE_FIGURE = re.compile(r"\b(\d{3,7})\b(?!\s*(?:k|grand|thousand|pounds|quid|euros|dollars|"
                         r"bucks)\b)(?!\s*(?:a|per|each)\s+(?:month|week|year|fortnight))", re.I)
MONTHS = ("january", "february", "march", "april", "may", "june", "july", "august",
          "september", "october", "november", "december")
NAMED_WHEN = (("christmas", "december"), ("xmas", "december"), ("new year", "december"),
              ("hogmanay", "december"), ("halloween", "october"), ("valentine", "february"),
              ("easter", "april"), ("black friday", "november"), ("spring", "march"),
              ("summer", "june"), ("autumn", "september"), ("fall", "october"),
              ("winter", "december"), ("the year", "december"))
WHEN_WORDS = "|".join(MONTHS) + "|" + "|".join(word for word, _month in NAMED_WHEN)
END_OF = r"(?:(?:at\s+)?the\s+end\s+of\s+|end\s+of\s+)?"
DATE = re.compile(r"\b(?:by|before|until|till|for|in|at the end of|end of)\s+" + END_OF +
                  r"(?:next\s+|this\s+|early\s+|late\s+)?(" + WHEN_WORDS + r")\b", re.I)
CORRECTING = re.compile(r"^\s*(?:(?:actually|no|sorry|nope|rather|instead|oh)\b[\s,]*"
                        r"(?:(?:its|it's|it\s+is|it\s+was|thats|that's|that\s+is)\b[\s,]*)?|"
                        r"(?:make|change)\s+(?:that|it)\s+(?:to\s+)?|i\s+mean\b[\s,]*)*", re.I)
END_OF_RELATIVE = re.compile(r"\b(?:by|before|until|till|in time for|for|in|at the end of|end of)"
                             r"\s+(?:at\s+)?the\s+end\s+of\s+(next\s+month|this\s+month|"
                             r"next\s+week|this\s+week|next\s+year|this\s+year|"
                             r"(?:the\s+)?(?:summer|winter|spring|autumn|fall))\b", re.I)
BARE_END_OF_RELATIVE = re.compile(r"^\s*(?:by|before|until|till|for|in)?\s*(?:at\s+)?the\s+end\s+of"
                                  r"\s+(next\s+month|this\s+month|next\s+week|this\s+week|"
                                  r"next\s+year|this\s+year)"
                                  r"\s*[.!,]?\s*$", re.I)
BARE_DATE = re.compile(r"^\s*(?:by|before|until|till|for|in)?\s*(?:at\s+|the\s+)?(?:end\s+of\s+)?"
                       r"(?:next\s+|this\s+|early\s+|late\s+)?(" + WHEN_WORDS + r")\s*[.!,]?\s*$",
                       re.I)
ALREADY = re.compile(r"\b(?:already|so far|to date|up to now|last (?:month|year|week)|"
                     r"this (?:month|year|week))\b", re.I)
INTENT = re.compile(r"\b(?:want|wants|wanted|need|needs|needed|hope|hoping|plan|planning|aim|aiming|"
                    r"going to|gonna|would like|like to|love to|trying to|goal|target)\b", re.I)
PAST_SAVING = re.compile(r"\b(?:saved|have\s+saved|had\s+saved|managed\s+to\s+save)\b", re.I)
HELD = re.compile(r"\b(?:in|into)\s+(?:(?:my|the|our|a|an)\s+)?(?:savings?|pot|fund|account)\b"
                  r"|\bin\s+it\b"
                  r"|\b(?:savings?|pot|fund)\b[^0-9]{0,14}\b(?:is|are|was|were|has|have|holds|"
                  r"sits\s+at|stood\s+at|sat\s+at|of)\b", re.I)


def _a_sum(text):
    line = text or ""
    for match in SUM.finditer(line):
        figure = match.group(1) or match.group(3) or ""
        unit = (match.group(2) or match.group(4) or "").lower()
        if not figure:
            continue
        if NOT_A_POT.match(line[match.end():]):
            continue
        try:
            value = float(figure.replace(",", ""))
        except ValueError:
            continue
        if unit in ("k", "grand", "thousand"):
            value *= 1000
        if value < 20:
            continue
        return int(round(value))
    for match in BARE_FIGURE.finditer(line):
        try:
            value = int(match.group(1))
        except ValueError:
            continue
        if value < 100 or 1990 <= value <= 2100:
            continue
        if NOT_A_POT.match(line[match.end():]):
            continue
        return value
    return None


def _a_date(text):
    relative = END_OF_RELATIVE.search(text or "")
    if relative:
        return "the end of " + " ".join(relative.group(1).lower().split())
    match = DATE.search(text or "")
    if not match:
        return ""
    word = match.group(1).lower()
    said = match.group(0).lower()
    if "end of" in said:
        return "the end of " + word
    return word


def _month_of(when):
    word = str(when or "").lower().strip()
    if word.startswith("the end of "):
        word = word[len("the end of "):].strip()
    if word in ("next month", "this month"):
        import datetime

        step = 1 if word == "this month" else 2
        return MONTHS[(datetime.date.today().month + step - 2) % 12]
    if word in MONTHS:
        return word
    for name, month in NAMED_WHEN:
        if name in word:
            return month
    return ""


TOGETHER = re.compile(r"(?:£\s*)?(\d[\d,]*(?:\.\d+)?)\s*(k|grand|thousand)?\s*(?:pounds?|quid)?\s*"
                      r"(?:on\s+top\s+of|plus|alongside|as\s+well\s+as|and\s+another|together\s+with)"
                      r"\s*(?:the\s+|my\s+|our\s+)?(?:£\s*)?(\d[\d,]*(?:\.\d+)?)\s*"
                      r"(k|grand|thousand)?", re.I)


def _two_sums_added(line):
    found = TOGETHER.search(str(line or ""))
    if not found:
        return 0
    total = 0
    for figure, unit in ((found.group(1), found.group(2)), (found.group(3), found.group(4))):
        try:
            value = float(figure.replace(",", ""))
        except (TypeError, ValueError):
            return 0
        if (unit or "").lower() in ("k", "grand", "thousand"):
            value *= 1000
        total += int(round(value))
    return total if total >= 20 else 0


HELD_SAID = re.compile(r"(?:£\s*)?(\d[\d,]*(?:\.\d+)?)\s*(k|grand|thousand)?\s*"
                       r"(?:pounds?|quid)?[^.!?]{0,40}?"
                       r"\b(?:saved|put\s+by|set\s+aside|put\s+aside|in\s+savings|in\s+the\s+pot)\b",
                       re.I)
FURTHER_SAID = re.compile(r"\b(?:another|a\s+further|an\s+extra|extra|more)\b\s*(?:£\s*)?"
                          r"(\d[\d,]*(?:\.\d+)?)\s*(k|grand|thousand)?", re.I)


def _pounds(figure, unit):
    try:
        value = float(str(figure or "").replace(",", ""))
    except (TypeError, ValueError):
        return 0
    if (unit or "").lower() in ("k", "grand", "thousand"):
        value *= 1000
    return int(round(value)) if value >= 20 else 0


def the_pot_and_the_rest(text):
    line = str(text or "")
    if not line.strip():
        return 0, 0
    further = FURTHER_SAID.search(line)
    held = HELD_SAID.search(line)
    if not further or not held:
        return 0, 0
    if further.start() < held.start():
        return 0, 0
    pot = _pounds(held.group(1), held.group(2))
    rest = _pounds(further.group(1), further.group(2))
    if not pot or not rest:
        return 0, 0
    return pot, rest


POT_REPORTED = re.compile(r"\b(?:this\s+(?:month|year|week)|last\s+(?:month|year|week)|so\s+far|"
                          r"to\s+date)\b", re.I)


ALREADY_HELD = re.compile(r"\b(?:already|so far)\b[^.!?]{0,24}?\b(?:have|has|got|hold|put)\b"
                          r"\s*(?:£\s*)?(\d[\d,]*(?:\.\d+)?)\s*(k|grand|thousand)?\b", re.I)
ALREADY_AFTER = re.compile(r"\b(?:have|has|got|hold)\b\s*(?:£\s*)?(\d[\d,]*(?:\.\d+)?)\s*"
                           r"(k|grand|thousand)?\s*(?:pounds?|quid)?\s+(?:already|so far)\b", re.I)


AIM_AT_A_SUM = re.compile(r"\b(?:want|wants|wanting|need|needs|hope|hoping|goal|aim|aiming|plan|"
                          r"planning|trying|like)\b[^.!?]{0,30}?"
                          r"\b(?:have|save|saved|set\s+aside|put\s+by|reach|get\s+to|afford)\b",
                          re.I)
BY_A_DATE = re.compile(r"\bby\s+(?:next\b|the\s+end\b|\d|january|february|march|april|may|"
                       r"june|july|august|september|october|november|december|christmas|"
                       r"spring|summer|autumn|winter|xmas|easter|payday|then\b)", re.I)


def the_pot_said_alone(text):
    line = str(text or "")
    if not line.strip() or FURTHER_SAID.search(line):
        return 0
    if AIM_AT_A_SUM.search(line) or BY_A_DATE.search(line):
        return 0
    held = HELD_SAID.search(line)
    if held and not POT_REPORTED.search(line):
        if INTENT.search(line) and not re.search(r"\b(?:have|has|got|got\s+\w+)\b", line, re.I):
            return 0
        return _pounds(held.group(1), held.group(2))
    for pattern in (ALREADY_HELD, ALREADY_AFTER):
        found = pattern.search(line)
        if not found:
            continue
        pot = _pounds(found.group(1), found.group(2))
        if pot >= 50:
            return pot
    return 0


AT_A_FIGURE = re.compile(
    r"\b(?:im|i'?m|i\s+am|we'?re|we\s+are|ive|i'?ve|i\s+have|we'?ve|we\s+have)\s+"
    r"(?:now\s+|only\s+|just\s+|already\s+)?"
    r"(?:on|at|up\s+to|got(?:\s+to)?|onto|standing\s+at)\s+"
    r"(?:about\s+|around\s+|nearly\s+|just\s+)?"
    r"(?:£\s*)?(\d[\d,]*(?:\.\d+)?)\s*(k|grand|thousand)?\b", re.I)


def the_pot_they_are_on(text):
    line = str(text or "")
    if not line.strip() or NOT_A_PRICE.search(line) or _a_rate(line):
        return 0
    match = AT_A_FIGURE.search(line)
    if not match:
        return 0
    if NOT_A_POT.match(line[match.end():]):
        return 0
    return _pounds(match.group(1), match.group(2))


A_RATE = re.compile(r"\b(?:a|per|each|every)\s+(?:month|week|year|fortnight|pay\s*day|"
                    r"payday|payslip)\b", re.I)


def _a_rate(line):
    return bool(A_RATE.search(str(line or "")))


def _the_pot_they_are_on(memory):
    turns = [t for t in ((memory or {}).get("turns") or []) if isinstance(t, dict)]
    for turn in reversed(turns[-6:]):
        pot = the_pot_they_are_on(str(turn.get("user") or ""))
        if pot:
            return pot
    return 0


HOW_FAR_OFF = re.compile(
    r"\bhow\s+far\s+(?:off|away)\b|"
    r"\bhow\s+much\s+(?:more\s+)?(?:do\s+i\s+need|have\s+i\s+(?:got\s+)?left|is\s+left)\b|"
    r"\bhow\s+much\s+(?:more|left)\s+to\s+go\b|"
    r"\bwhat'?s\s+left\s+(?:to\s+go|on\s+it)\b", re.I)


NEED_A_FIGURE = re.compile(
    r"\b(?:need|needs|need\s+to\s+(?:get\s+to|reach|have|save|find)|"
    r"have\s+to\s+(?:find|reach|save)|should\s+have|aiming\s+for|target\s+is)\b", re.I)


def _the_goal_they_need(memory):
    turns = [t for t in ((memory or {}).get("turns") or []) if isinstance(t, dict)]
    lines = [str(t.get("user") or "") for t in turns[-6:]]
    if not any(SAVING.search(line) and (not _a_sum(line) or _a_rate(line)) for line in lines):
        return 0
    for line in reversed(lines):
        if the_pot_they_are_on(line) or the_pot_said_alone(line) or _a_rate(line):
            continue
        if NEED_A_FIGURE.search(line):
            wanted = _a_sum(line)
            if wanted:
                return wanted
    return 0


def asks_how_far_off(text):
    return bool(HOW_FAR_OFF.search(str(text or "")))


def the_gap_left(text, memory):
    line = str(text or "")
    if not asks_how_far_off(line) or _a_sum(line) or _a_rate(line):
        return ""
    goal, pot = the_goal_and_the_pot(memory)
    if not goal:
        return ""
    if not pot or pot >= goal:
        return ""
    said = _the_gap_said(goal, pot)
    if _the_gap_was_just_said(said, memory):
        return _the_gap_again(goal, pot, memory)
    return said


def _the_gap_said(goal, pot):
    left = goal - pot
    share = int(round(100.0 * pot / goal))
    return ("£%s to go of £%s - you're £%s in, %d%% of the way there."
            % (format(left, ","), format(goal, ","), format(pot, ","), share))


def _the_gap_was_just_said(said, memory):
    turns = [t for t in ((memory or {}).get("turns") or []) if isinstance(t, dict)]
    if not turns:
        return False
    return " ".join(str(turns[-1].get("bot") or "").split()) == " ".join(said.split())


def _the_gap_again(goal, pot, memory):
    rate = _the_rate_in_the_chat(memory)
    if rate:
        said = _the_length_at_that_rate(goal - pot, rate, "month", pot)
        if said:
            return said
    return ("Still £%s to go - you've £%s of the £%s in the pot."
            % (format(goal - pot, ","), format(pot, ","), format(goal, ",")))


def the_goal_and_the_pot(memory):
    goal = (_the_goal_in_the_chat(memory) or _the_goal_said_as_a_price(memory)
            or _the_goal_they_need(memory))
    if not goal:
        return 0, 0
    pot = _the_money_already_held(memory) or _the_pot_they_are_on(memory)
    return goal, pot


def the_pot_position(text, memory):
    if not the_pot_they_are_on(text) or asks_how_far_off(text) or _a_sum_that_is_a_goal(text):
        return ""
    if the_pot_said_alone(text):
        return ""
    goal, pot = the_goal_and_the_pot(memory)
    pot = the_pot_they_are_on(text) or pot
    if not goal or not pot or pot >= goal:
        return ""
    return _the_gap_said(goal, pot)


def _a_sum_that_is_a_goal(text):
    line = str(text or "")
    if _a_rate(line):
        return False
    return bool(NEED_A_FIGURE.search(line) and _a_sum(line))


def rate_question_for(amount, when=""):
    if not amount or amount < 20:
        return ""
    if when:
        return ("How much do i need to put by a week to have %s pounds by %s?"
                % (format(amount, ","), _in_the_money_readers_words(when)))
    return "How much do i need to put by a week to have %s pounds?" % format(amount, ",")


def the_money_already_held(memory):
    return _the_money_already_held(memory)


def _the_money_already_held(memory):
    turns = [t for t in (memory or {}).get("turns") or () if isinstance(t, dict)]
    for turn in reversed(turns[-6:]):
        line = str(turn.get("user") or "")
        pot, _rest = the_pot_and_the_rest(line)
        if pot:
            return pot
        pot = the_pot_said_alone(line)
        if pot:
            return pot
        pot = the_pot_they_are_on(line)
        if pot:
            return pot
    return 0


POT_OPENER = re.compile(r"^For\s+£\s*[\d,]+:\s*")


def without_the_pot_opener(answer):
    return POT_OPENER.sub("", str(answer or ""), count=1)


def _names_a_goal(line):
    line = str(line or "")
    added = _two_sums_added(line)
    if added and SAVING.search(line):
        return added
    pot, rest = the_pot_and_the_rest(line)
    if pot and rest and SAVING.search(line):
        return pot + rest
    if INTENT.search(line) and SAVING.search(line):
        aim = _a_sum(line)
        if aim:
            return aim
    if not (SAVING.search(line) and _a_sum(line)):
        return 0
    if INTENT.search(line):
        return _a_sum(line)
    if ALREADY.search(line) or PAST_SAVING.search(line) or HELD.search(line):
        return 0
    return _a_sum(line)


HOW_LONG_ASK = re.compile(
    r"^\W*(?:(?:and|but|so|ok|okay|then|oh|right|yeah)\W+)*"
    r"(?:how\s+long"
    r"(?:\s+(?:will|would|does|do|did|is|to)\s+(?:that|it|this)"
    r"(?:\s+(?:take|be))?"
    r"(?:\s+to\s+(?:save|get)(?:\s+(?:that|it|there|the\s+money))?)?)?"
    r"|how\s+many\s+(?:months|years|weeks)(?:\s+is\s+(?:that|it|this))?"
    r"|how\s+much\s+time(?:\s+(?:will|would|does)\s+(?:that|it|this)\s+take)?)"
    r"\s*[?!.]*\s*$", re.I)


HOW_LONG_UNTIL = re.compile(
    r"^\W*(?:(?:and|but|so|ok|okay|then|oh|right|yeah)\W+)*how\s+long\s+"
    r"(?:until|till|til|before)\s+(?:i|we|you|it|its|it's|that|this|there)\b"
    r"|^\W*(?:(?:and|but|so|ok|okay|then|oh|right|yeah)\W+)*how\s+long\s+to\s+"
    r"(?:save|have|get|reach|afford|be there)\b", re.I)


WHEN_AT_THE_GOAL = re.compile(
    r"^\W*(?:(?:and|but|so|ok|okay|then|oh|right|yeah)\W+)*"
    r"when\s+(?:will|would|can|could|should|might)\s+(?:i|we|you|it|its|it's|that|this)\s+"
    r"(?:have|get|be|reach|afford|save|hit|make|manage)\b", re.I)


def asks_how_long(text):
    line = " ".join(str(text or "").lower().split())
    if not line or len(line.split()) > 8 or re.search(r"\d", line):
        return False
    return bool(HOW_LONG_ASK.search(line) or HOW_LONG_UNTIL.match(line)
                or WHEN_AT_THE_GOAL.match(line))


def how_long_it_takes(memory):
    if not memory:
        return ""
    previous = _the_line_before(memory)
    goal = _the_goal_in_the_chat(memory)
    priced = 0 if goal else _the_goal_said_as_a_price(memory)
    if not goal:
        goal = priced
    from_the_answer = False
    if not goal:
        goal = _the_goal_in_the_answer(memory)
        turns_said = [t for t in (memory.get("turns") or []) if isinstance(t, dict)]
        last_bot = str((turns_said[-1] or {}).get("bot") or "") if turns_said else ""
        from_the_answer = bool(goal) and "still to find" in last_bot.lower()
    pot = _the_money_already_held(memory) if not from_the_answer else 0
    if goal and 0 < pot < goal:
        goal = goal - pot
    else:
        pot = 0
    if not goal or goal < 100:
        return ""
    if previous and _a_length_was_asked(previous):
        return ""
    if _the_rate_in_the_chat(memory) or _the_date_in_the_chat(memory):
        rate = _the_rate_in_the_chat(memory)
        if rate and goal and priced and not _the_date_in_the_chat(memory):
            return _the_length_at_that_rate(goal, rate, "month", pot)
        if rate and rate < goal:
            months = -(-goal // rate)
            said_turns = [t for t in (memory.get("turns") or []) if isinstance(t, dict)]
            last = str((said_turns[-1] or {}).get("bot") or "") if said_turns else ""
            if not re.search(r"\b%d\s+months?\b" % months, last):
                return without_what_was_just_said(
                    _a_rate_against_the_goal(goal, rate, memory), memory)
        return ""
    rate, period = _a_rate_in_another_period(memory)
    if rate:
        return _the_length_at_that_rate(goal, rate, period, pot)
    slow = -(-goal // 100)
    fast = -(-goal // 250)
    income = _the_income_in_the_chat(memory)
    if income:
        said_goal = "the £%s still to find" % format(goal, ",") if pot else (
            "£%s" % format(goal, ","))
        return ("How much of the £%s can you put by each month? At £100 a month %s takes "
                "%s." % (format(income, ","), said_goal, _months(slow)))
    said = ("the £%s still to find takes " % format(goal, ",")) if pot else (
        "£%s takes " % format(goal, ","))
    if fast == slow:
        return ("At £100 a month, " + said
                + "%s. Pick the rate your pay can carry and set the "
                  "standing order for the day after payday." % _months(slow))
    return ("At £100 a month, " + said
            + "%s - or %s at £250 a month. Pick the one your pay can "
              "carry." % (_months(slow), _months(fast)))


def _only_a_date(text):
    bare = (text or "").strip()
    bare = CORRECTING.sub("", bare).strip()
    relative = BARE_END_OF_RELATIVE.match(bare)
    if relative:
        return "the end of " + " ".join(relative.group(1).lower().split())
    match = BARE_DATE.match(bare)
    if not match:
        return ""
    word = match.group(1).lower()
    if "end of" in match.group(0).lower():
        return "the end of " + word
    return word


def is_only_a_date(text):
    return bool(_only_a_date(text))


def _only_a_sum(text):
    bare = CORRECTING.sub("", str(text or "")).strip()
    if not bare or len(bare.split()) > 4:
        return 0
    aim = _a_sum(bare)
    rest = re.sub(r"[^a-z]", "", SUM.sub("", bare).lower()).strip()
    if rest:
        return 0
    if not aim:
        figure = re.sub(r"[^0-9]", "", bare)
        if len(figure) >= 3 and int(figure) >= 20:
            return int(figure)
        return 0
    return aim


def asks_about_saving(text):
    return bool(_names_a_goal(text))


def _the_money_still_to_find(memory):
    whole = _the_goal_in_the_chat(memory)
    held = _the_money_already_held(memory)
    if whole and 0 < held < whole:
        return whole - held
    return whole


def _the_goal_in_the_chat(memory):
    return _the_goal_named_in_a_line(memory)


def _the_goal_named_in_a_line(memory):
    turns = [t for t in (memory.get("turns") or []) if isinstance(t, dict)]
    for turn in reversed(turns[-6:]):
        line = str(turn.get("user") or "")
        corrected = _only_a_sum(line)
        if corrected:
            return corrected
        if the_pot_said_alone(line):
            continue
        aim = _names_a_goal(line)
        if aim:
            return aim
    return 0


PRICE_WORDS = re.compile(r"\b(?:is|are|was|were|costs?|cost|about|around|at|for|goes for)\b", re.I)
A_TRAILING_SUM = re.compile(r",\s*£?\s*\d")
NOT_A_PRICE = re.compile(r"\b(?:earn\w*|salary|wages?|income|payslip|paid|pension|"
                        r"before tax|after tax|take home|i'?m\s+\d+|i am\s+\d+|how old)\b", re.I)

def _the_goal_said_as_a_price(memory):
    turns = [t for t in ((memory or {}).get("turns") or []) if isinstance(t, dict)]
    recent = turns[-6:]
    if not any(SAVING.search(str(t.get("user") or ""))
               and (not _a_sum(str(t.get("user") or "")) or _a_rate(str(t.get("user") or "")))
               for t in recent):
        return 0
    for turn in reversed(recent):
        line = str(turn.get("user") or "")
        if not line or the_pot_said_alone(line):
            continue
        if the_pot_they_are_on(line):
            continue
        if A_RATE.search(line) or A_RATE_ANY_OTHER_PERIOD.search(line):
            continue
        if not (PRICE_WORDS.search(line) or A_TRAILING_SUM.search(line)):
            continue
        if NOT_A_PRICE.search(line):
            continue
        aim = _a_sum(line)
        if aim and aim >= 100:
            return aim
    return 0


A_GOAL_STATED = re.compile(r"(?:\bfor\s+)?£\s*(\d[\d,]*(?:\.\d+)?)\s*(k)?\s*"
                           r"(?::|\bat\s+£|\bis\s+(?:about\s+)?\d)", re.I)


A_LENGTH_WAS_ASKED = re.compile(
    r"\bhow\s+long\b|\bhow\s+many\s+(?:months|years|weeks)\b|\bhow\s+much\s+time\b", re.I)


A_LENGTH_SAID = re.compile(
    r"\b(?:in|within|over|inside)\s+(?:the\s+next\s+|the\s+coming\s+)?"
    r"(?:\d[\d,]*|a|an|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|eighteen|"
    r"twenty[-\s]?four|a\s+couple\s+of|a\s+few)\s*"
    r"(?:months?|years?|weeks?)\b"
    r"|\b(?:the\s+)?end\s+of\s+(?:the\s+)?(?:month|year|week)\b", re.I)


def a_length_was_said(line):
    return bool(A_LENGTH_SAID.search(str(line or "")))


def _a_length_was_asked(line):
    return bool(A_LENGTH_WAS_ASKED.search(str(line or "")))


def _the_line_before(memory):
    turns = [t for t in (memory or {}).get("turns") or () if isinstance(t, dict)]
    if not turns:
        return ""
    return str(turns[-1].get("user") or "")


def _the_goal_in_the_answer(memory):
    turns = [t for t in (memory.get("turns") or []) if isinstance(t, dict) and t.get("bot")]
    for turn in reversed(turns[-3:]):
        for found in A_GOAL_STATED.finditer(str(turn.get("bot") or "")):
            try:
                value = float(found.group(1).replace(",", ""))
            except ValueError:
                continue
            if (found.group(2) or "").lower() == "k":
                value *= 1000
            value = int(value)
            if value >= 100:
                return value
    return 0


ANOTHER_SUM = re.compile(
    r"^\s*(?:(?:and|but|so|then|ok|okay)\s+)?(?:(?:what|how)\s+about|and)\s+(?:£\s*)?"
    r"(\d[\d,]*(?:\.\d+)?)\s*(k|grand|thousand|pounds?|quid)?\s*[?!.]*\s*$", re.I)


A_GOAL_SUM = re.compile(r"^\s*(?:(?:and|but|so|then|ok|okay)\b[\s,]*)*"
                        r"(?:i(?:'d|'ll)?\s+)?(?:will\s+|just\s+|only\s+|need\s+to\s+|"
                        r"want\s+to\s+)?sav(?:e|es|ing)\s+(?:£\s*)?(\d[\d,]*(?:\.\d+)?)\s*"
                        r"(k|grand|thousand|pounds?|quid)?\s*[?!.]*\s*$", re.I)


def another_sum_asked(text, memory):
    found = ANOTHER_SUM.match(str(text or "")) or A_GOAL_SUM.match(str(text or ""))
    if not found:
        return ""
    turns = [t for t in (memory.get("turns") or []) if isinstance(t, dict)]
    talked_money = False
    for turn in turns[-2:]:
        line = str(turn.get("user") or "")
        if _only_a_sum(line) or _names_a_goal(line):
            talked_money = True
    if not talked_money:
        return ""
    figure = _a_sum(text)
    if not figure or figure < 100:
        return ""
    return "save £%s" % format(figure, ",")


A_RATE = re.compile(r"(?:£\s*)?(\d[\d,]*)\s*(?:pounds?\s+)?(?:[a-z]+\s+){0,2}?"
                    r"(?:a|per|each)\s+month\b", re.I)


def _a_rate_is_settled(memory):
    turns = [t for t in (memory.get("turns") or []) if isinstance(t, dict)]
    for turn in turns[-4:]:
        if A_RATE.search(str(turn.get("user") or "")):
            return True
    return False


A_RATE_ANY_OTHER_PERIOD = re.compile(r"(?:£\s*)?(\d[\d,]*)\s*(?:pounds?\s+)?(?:[a-z]+\s+){0,2}?"
                                     r"(?:a|per|each)\s+(week|fortnight|year)\b", re.I)


MONTHS_IN_A = {"week": 12 / 52.0, "fortnight": 12 / 26.0, "month": 1.0, "year": 12.0}


def _the_length_at_that_rate(goal, rate, period, pot=0):
    count = -(-goal // rate)
    said = ("the £%s still to find takes " % format(goal, ",")) if pot else (
        "£%s takes " % format(goal, ","))
    line = "At £%s a %s, %s%s %s" % (format(rate, ","), period, said, count,
                                    period if count == 1 else period + "s")
    if period == "year":
        return line + "."
    months = int(round(count * MONTHS_IN_A[period]))
    if period != "month" and months >= 2:
        line += " (about %s)" % _months(months)
    return line + "."


def _a_rate_in_another_period(memory):
    turns = [t for t in ((memory or {}).get("turns") or []) if isinstance(t, dict)]
    for turn in reversed(turns[-6:]):
        found = A_RATE_ANY_OTHER_PERIOD.search(str(turn.get("user") or ""))
        if not found:
            continue
        try:
            value = int(found.group(1).replace(",", ""))
        except ValueError:
            continue
        if value >= 5:
            return value, found.group(2).lower()
    return 0, ""

INCOME_FRAME = re.compile(
    r"\b(?:earn|earns|earning|earned|paid|salary|wages?|income|take[- ]home|brings?\s+in|"
    r"pension|benefits?|allowance)\b|\b(?:i|we)\s+(?:get|make|bring)\b", re.I)
OUTGOING_FRAME = re.compile(
    r"\b(?:rent|mortgage|bills?|childcare|nurser(?:y|ies)|loan|debt|overdraft|"
    r"council\s+tax|energy|electric(?:ity)?|gas|heating|insurance|commut(?:e|ing)|"
    r"transport|travel|groceries|food\s+shop|spend(?:ing)?|goes\s+on|paying\s+out|"
    r"outgoings|repayments?)\b", re.I)
CLAUSE_EDGE = re.compile(r"[,;.]|\band\b|\bbut\b|\bso\b")


def _is_an_income(line, found):
    before = CLAUSE_EDGE.split(str(line or "")[:found.start()])[-1]
    return bool(INCOME_FRAME.search(before))


def _is_an_outgoing(line, found):
    text = str(line or "")
    return bool(OUTGOING_FRAME.search(text[max(0, found.start() - 40):found.end() + 40]))


def _is_not_a_rate(line, found):
    return _is_an_income(line, found) or _is_an_outgoing(line, found)

def _the_income_in_the_chat(memory):
    turns = [t for t in (memory.get("turns") or []) if isinstance(t, dict)]
    for turn in reversed(turns[-6:]):
        line = str(turn.get("user") or "")
        for found in A_RATE.finditer(line):
            if not _is_an_income(line, found):
                continue
            value = _a_sum_named(found.group(1))
            if value:
                return value
    return 0


A_RATE_PUT_RIGHT = re.compile(r"\b(?:actually|sorry|i meant|meant|make it|make that|no wait|"
                              r"rather than|instead|not)\b", re.I)

A_CAN_CARRY_IT = re.compile(r"\b(?:can|could|able|afford|manage|put|save|saving|spare|stretch)\b",
                            re.I)

A_SUM_A_MONTH = re.compile(r"(?:£\s*)?(\d[\d,]*)\s*(?:pounds?\s+)?(?:a|per|each)\s+month\b",
                           re.I)

_OTHER_FIGURE_WORDS = re.compile(
    r"\b(?:need|needs|needed|owe|owes|owed|debt|debts|cost|costs|spend|spent|spending|"
    r"bill|bills|rent|goal|target|total|altogether|towards|toward|"
    r"week|weeks|day|days|year|years)\b",
    re.I)

A_LONE_SUM = re.compile(r"(?<![\d.,£$\u20ac])(\d[\d,]*)(?![\d.,])")

A_CORRECTION_AND_A_FIGURE = re.compile(
    r"^\W*(?:(?:actually|sorry|no|nope|wait|oh|well|ok|okay|right|hang\s+on)\b\W*){0,3}"
    r"(?:(?:it|its|it's|that|thats|that's|make\s+it|make\s+that|i\s+meant|meant)\b\W*){0,2}"
    r"(?:£\s*)?\d", re.I)

_NOT_THE_RATE = re.compile(
    r"\b(?:on|spent|spending|cost|costs|bill|bills|balance|owe|owes|owed|debt|debts|rent|"
    r"price|paid|pay|total|goal|target|week|weeks|day|days|year|years|times?|hours?)\b",
    re.I)

A_NO_THEN_A_RATE = re.compile(r"^\s*(?:no|nope|nah)\b[\s,.!\u2014-]*"
                              r"(?:i\s+(?:can|could)\s+(?:do|manage|put|save|spare)\s+)?"
                              r"(?:£\s*)?(\d[\d,]*)\s*(?:pounds?\s+)?(?:a|per|each)\s+month\b",
                              re.I)

A_SPENT_ON = re.compile(r"\b(?:on|spent|spending|costs?|bills?)\b", re.I)


A_MORE_LIKE = re.compile(
    r"\b(?:more\s+like|closer\s+to|call\s+it)\s*(?:£\s*)?\d"
    r"|\b(?:it'?s|its|that'?s)\s+(?:(?:more\s+like|about|only)\s+)?(?:£\s*)?\d[\d,]*\s+now\b",
    re.I)


def _is_a_rate_line(line):
    for found in A_RATE.finditer(str(line or "")):
        if not _is_not_a_rate(str(line or ""), found):
            return True
    return False


def a_rate_put_right(line, before=""):
    line = str(line or "")
    if (before and A_MORE_LIKE.search(line) and A_RATE_PUT_RIGHT.search(line)
            and _is_a_rate_line(before) and not _OTHER_FIGURE_WORDS.search(line)):
        figures = A_LONE_SUM.findall(line)
        if len(figures) == 1:
            return _a_sum_named(figures[0])
    after_a_no = A_NO_THEN_A_RATE.search(line)
    if after_a_no and not A_SPENT_ON.search(line[after_a_no.end():]):
        return _a_sum_named(after_a_no.group(1))
    if not A_RATE_PUT_RIGHT.search(line) or _OTHER_FIGURE_WORDS.search(line):
        return 0
    with_the_month = A_SUM_A_MONTH.search(line)
    if with_the_month:
        return _a_sum_named(with_the_month.group(1))
    figures = A_LONE_SUM.findall(line)
    if len(figures) != 1:
        return 0
    if not A_CAN_CARRY_IT.search(line):
        if not A_CORRECTION_AND_A_FIGURE.match(line.strip()) or _NOT_THE_RATE.search(line):
            return 0
    return _a_sum_named(figures[0])


def _a_sum_named(figure):
    try:
        value = int(str(figure).replace(",", ""))
    except (TypeError, ValueError):
        return 0
    return value if value >= 10 else 0


def _the_rate_in_the_chat(memory):
    turns = [t for t in (memory.get("turns") or []) if isinstance(t, dict)][-6:]
    settled = 0
    before = ""
    for turn in turns:
        line = str(turn.get("user") or "")
        for found in A_RATE.finditer(line):
            if _is_not_a_rate(line, found):
                continue
            value = _a_sum_named(found.group(1))
            if value:
                settled = value
            continue
        if settled:
            put_right = a_rate_put_right(line, before)
            if put_right:
                settled = put_right
        before = line
    return settled


HOW_MUCH = re.compile(r"\bhow\s+(?:much|many)\b[^?.!]{0,24}?\b(?:a|per|each)\s+(?:month|week)\b|"
                      r"\bhow\s+much\s+(?:should|do|would)\s+i\s+(?:put|save|need)\b", re.I)


def _the_date_in_the_chat(memory):
    turns = [t for t in (memory.get("turns") or []) if isinstance(t, dict)]
    for turn in reversed(turns[-6:]):
        line = str(turn.get("user") or "")
        when = _only_a_date(line) or _a_date(line)
        if when:
            return when
    return ""


def _months_left(when):
    import datetime

    today = datetime.date.today()
    word = str(when or "").lower()
    if "this month" in word or "this week" in word:
        return 0
    if "next month" in word:
        return 1
    month = _month_of(when)
    if not month:
        return 0
    number = MONTHS.index(month) + 1
    year = today.year + (1 if number <= today.month else 0)
    return max((year - today.year) * 12 + (number - today.month), 0)


def _months(n):
    said = "%s month%s" % (format(n, ","), "" if n == 1 else "s")
    if n < 12:
        return said
    years, months = divmod(n, 12)
    parts = []
    if years:
        parts.append("%s year%s" % (format(years, ","), "" if years == 1 else "s"))
    if months:
        parts.append("%s month%s" % (months, "" if months == 1 else "s"))
    return said + ", about " + " and ".join(parts)


def a_date_on_a_settled_rate(text, memory):
    when = _only_a_date(text)
    if not when or not _a_rate_is_settled(memory):
        return ""
    rate, goal = _the_rate_in_the_chat(memory), _the_money_still_to_find(memory)
    return _a_date_on_a_rate(goal, rate, when)


def _a_date_on_a_rate(goal, rate, when):
    left = _months_left(when)
    if not rate or not goal or goal <= rate or left < 1:
        return ""
    months = -(-goal // rate)
    name = when if when.startswith("the end of ") else when.capitalize()
    goal_text = "£%s" % format(goal, ",")
    rate_text = "£%s a month" % format(rate, ",")
    if months <= left:
        return ("%s at %s takes %s and %s is %s away, so that rate gets you there. Set the standing "
                "order for the day after payday and it looks after itself — a bonus or a refund "
                "just brings the date forward."
                % (goal_text, rate_text, _months(months), name, _months(left)))
    need = -(-goal // left)
    need = int(-(-need // 10) * 10)
    part = min(rate * left, goal)
    return ("%s at %s takes %s and %s is %s away, so it does not get you there — that would take "
            "about £%s a month. At %s you have £%s of it by then; a bonus, a bill that drops or a "
            "later date closes the gap."
            % (goal_text, rate_text, _months(months), name, _months(left), format(need, ","),
               rate_text, format(part, ",")))


A_WEEK_FIGURE = re.compile(r"£\s*(\d[\d,]*)\s*a\s+week", re.I)


ASKS_IF_ENOUGH = re.compile(
    r"^\s*(?:(?:and|but|so|ok|okay|right|well)\b[\s,]*)*"
    r"(?:is|will|would|does|do|am\s+i|are\s+we)\s+"
    r"(?:that|this|it|they|we|i|£?\s*\d[\d,]*\s*(?:a|per|each)\s+month|"
    r"(?:putting\s+by|saving|saved)\s+£?\s*\d[\d,]*\s*(?:a|per|each)\s+month)\s+"
    r"(?:be\s+)?(?:enough|do(?:\s+it)?|get\s+(?:me|us)\s+there|get\s+there|cover(?:\s+it)?"
    r"|be\s+enough)"
    r"(?:\s+(?:then|though|really|now|do\s+you\s+think|i\s+wonder))?\s*[.!?]*\s*$", re.I)


def asks_if_the_rate_is_enough(text):
    return bool(ASKS_IF_ENOUGH.match(str(text or "")))


def a_yes_no_about_the_rate(text, memory):
    if not asks_if_the_rate_is_enough(text) or not isinstance(memory, dict):
        return ""
    goal, rate = _the_money_still_to_find(memory), _the_rate_in_the_chat(memory)
    if not goal or not rate:
        return ""
    months = -(-goal // rate)
    when = _the_date_in_the_chat(memory)
    left = _months_left(when) if when else 0
    goal_text = "£%s" % format(goal, ",")
    rate_only = "£%s a month" % format(rate, ",")
    rate_text = "at %s" % rate_only
    if not when or not left:
        return ("%s %s takes %s. Name the month you want it by and I will tell you whether that "
                "is soon enough." % (goal_text, rate_text, _months(months)))
    if months <= left:
        spare = left - months
        room = ("%s month%s to spare" % (spare, "" if spare == 1 else "s")
                if spare else "nothing to spare")
        return ("Yes — %s gets you to %s by %s, %s. Leave the standing order where it is."
                % (rate_only, goal_text, str(when).capitalize(), room))
    part = min(rate * left, goal)
    return ("No — %s you have £%s of %s by %s. The whole %s takes %s at that rate, so the rest "
            "wants more a month or a later date."
            % (rate_text, format(part, ","), goal_text, str(when).capitalize(), goal_text,
               _months(months)))


ASKS_HOW_MUCH_MORE = re.compile(
    r"^\s*(?:(?:and|but|so|ok|okay|right|well)\b[\s,]*)*"
    r"(?:how\s+much\s+(?:more|extra)\s+(?:a|per|each)\s+month"
    r"|how\s+much\s+(?:more|extra)\s+(?:would|do|will)\s+(?:i|we)\s+(?:need|have\s+to))"
    r"\b", re.I)


def asks_how_much_more_a_month(text):
    return bool(ASKS_HOW_MUCH_MORE.match(str(text or "")))


def the_extra_a_month_asked(text, memory):
    if not asks_how_much_more_a_month(text) or not isinstance(memory, dict):
        return ""
    goal, rate = _the_money_still_to_find(memory), _the_rate_in_the_chat(memory)
    when = _the_date_in_the_chat(memory)
    if not goal or not rate or not when:
        return ""
    left = _months_left(when)
    if not left:
        return ""
    months = -(-goal // rate)
    if months <= left:
        spare = left - months
        return ("Nothing more — %s already gets you to £%s by %s with %s month%s to spare."
                % ("£%s a month" % format(rate, ","), format(goal, ","), str(when).capitalize(),
                   spare, "" if spare == 1 else "s"))
    need = -(-goal // left)
    need = int(-(-need // 10) * 10)
    more = max(need - rate, 0)
    left_text = "the month that is left" if left == 1 else "the %s left" % _months(left)
    return ("About £%s a month more: £%s a month for %s, rather than the £%s you have. Or give it "
            "longer — at £%s a month the whole £%s takes %s."
            % (format(more, ","), format(need, ","), left_text, format(rate, ","),
               format(rate, ","), format(goal, ","), _months(months)))


def the_same_figure_a_month(text, memory):
    if not HOW_MUCH.search(str(text or "")):
        return ""
    turns = [t for t in (memory.get("turns") or []) if isinstance(t, dict)]
    for turn in reversed(turns[-4:]):
        found = A_WEEK_FIGURE.search(str(turn.get("bot") or ""))
        if not found:
            continue
        try:
            a_week = int(found.group(1).replace(",", ""))
        except ValueError:
            return ""
        if a_week < 5:
            return ""
        a_month = int(round(a_week * 52 / 12.0 / 10.0)) * 10
        return ("£%s a week is about £%s a month. Set the standing order for the day after payday "
                "and it runs itself — a bonus or a refund only shortens the time."
                % (format(a_week, ","), format(a_month, ",")))
    return ""


A_NEW_RATE = re.compile(r"^\s*(?:(?:and|but|so|then|ok|okay|right)\b[\s,]*)*"
                        r"(?:(?:what|how)\s+about\s+|at\s+|make\s+it\s+)?(?:£\s*)?"
                        r"(\d[\d,]*(?:\.\d+)?)\s*(k)?\s*(?:pounds?\s+)?(?:a|per|each)\s+month"
                        r"\s*(?:then|now)?\s*[.!]*\s*$", re.I)


def a_rate_restated(text, memory):
    line = str(text or "")
    said = A_NEW_RATE.match(line)
    if not said:
        return ""
    if PAST_SAVING.search(line) or OTHER_POT.search(line):
        return ""
    if _only_a_date(line) or _a_date(line):
        return ""
    try:
        rate = float(said.group(1).replace(",", ""))
    except ValueError:
        return ""
    if said.group(2):
        rate *= 1000
    rate = int(round(rate))
    if rate < 20:
        return ""
    aim = _the_goal_in_the_chat(memory)
    if not aim or rate >= aim:
        return ""
    if rate == _the_rate_in_the_chat(memory):
        return ""
    return without_what_was_just_said(_a_rate_against_the_goal(aim, rate, memory), memory)


A_RATE_WITH_A_VERB = re.compile(
    r"^\s*(?:(?:and|but|so|then|ok|okay|right)\b[\s,]*)*"
    r"(?:(?:what|how)\s+about\s+|what\s+if\s+(?:i\s+)?|(?:and\s+)?if\s+i\s+)?"
    r"(?:only\s+)?(?:put|putting|set|setting|pay|paying)\s+(?:(?:away|by|aside|in|up)\s*)?"
    r"(?:£\s*)?(\d[\d,]*(?:\.\d+)?)\s*(k)?\s*(?:pounds?|quid)?\s*"
    r"(?:(?:instead|then|now)\b\s*)?[.!?]*\s*$", re.I)


def a_rate_put_in_with_a_verb(text, memory):
    line = str(text or "")
    if not line.strip() or A_RATE.search(line) or A_NEW_RATE.match(line):
        return ""
    if _only_a_date(line) or _a_date(line):
        return ""
    said = A_RATE_WITH_A_VERB.match(line)
    if not said:
        return ""
    if PAST_SAVING.search(line) or OTHER_POT.search(line):
        return ""
    if not _a_rate_is_settled(memory):
        return ""
    try:
        rate = float(said.group(1).replace(",", ""))
    except ValueError:
        return ""
    if said.group(2):
        rate *= 1000
    rate = int(round(rate))
    if rate < 20:
        return ""
    aim = _the_goal_in_the_chat(memory) or _the_goal_in_the_answer(memory)
    if not aim or rate >= aim:
        return ""
    if rate == _the_rate_in_the_chat(memory):
        return ""
    return without_what_was_just_said(_a_rate_against_the_goal(aim, rate, memory), memory)


ASKS_A_LENGTH = re.compile(
    r"\bhow\s+long\b|\bhow\s+many\s+(?:months|years|weeks)\b|"
    r"\bwhen\s+(?:will|would|can|do|should)\s+(?:i|we)\b", re.I)


def a_length_at_the_rate_in_the_chat(text, memory):
    line = str(text or "")
    if not line.strip() or not ASKS_A_LENGTH.search(line):
        return ""
    if A_RATE.search(line) or A_NEW_RATE.match(line) or A_RATE_WITH_A_VERB.match(line):
        return ""
    if _the_date_in_the_chat(memory):
        return ""
    said = _a_sum(line)
    if not said:
        return ""
    rate = _the_rate_in_the_chat(memory)
    if not rate or rate >= said:
        return ""
    return ("How long will it take to save %s at %s a month?"
            % (format(said, ","), format(rate, ",")))


def a_rate_with_no_date(text, memory):
    line = str(text or "")
    if not HOW_MUCH.search(line) or _a_sum(line) or _only_a_date(line) or _a_date(line):
        return ""
    aim = _the_goal_in_the_chat(memory)
    if not aim or _the_date_in_the_chat(memory):
        return ""
    return ("£%s is a different rate over six months than over a year, so name the month you want "
            "it by and I will work out what to put by each month — and whether a standing order "
            "gets you there." % format(aim, ","))


def asks_the_rate(text, memory):
    line = str(text or "")
    if not HOW_MUCH.search(line) or _a_sum(line):
        return False
    if _only_a_date(line) or _a_date(line):
        return False
    return bool(_the_goal_in_the_chat(memory))


_KNOWN_TO_THE_MONEY_ENTRY = ("christmas", "xmas")


def _in_the_money_readers_words(when):
    word = str(when or "").lower().strip()
    if not word or word in MONTHS or word in _KNOWN_TO_THE_MONEY_ENTRY:
        return word
    if word.startswith("the end of "):
        rest = word[len("the end of "):].strip()
        if rest in ("next year", "this year", "the year"):
            return word
        season = rest[4:] if rest.startswith("the ") else rest
        month = _THE_END_OF_A_SEASON.get(season) or _in_the_money_readers_words(rest)
        return "the end of " + month if month else word
    for name, month in NAMED_WHEN:
        if name in word:
            return month
    return word


_THE_END_OF_A_SEASON = {"spring": "may", "summer": "august", "autumn": "november",
                        "fall": "november", "winter": "february"}


def rate_question(text, memory):
    line = str(text or "")
    if not line.strip():
        return ""
    if HOW_MUCH.search(line) and not _a_sum(line):
        aim, when = _the_goal_in_the_chat(memory), _the_date_in_the_chat(memory)
        if not aim:
            return ""
        if when:
            return ("How much do i need to put by a week to have %s pounds by %s?"
                    % (format(aim, ","), _in_the_money_readers_words(when)))
        return "How much do i need to put by a week to have %s pounds?" % format(aim, ",")
    if _names_a_goal(line):
        aim, when = _names_a_goal(line), _a_date(line)
    else:
        when = _only_a_date(line)
        if not when or _a_rate_is_settled(memory):
            return ""
        aim = _the_goal_in_the_chat(memory)
    if not aim:
        return ""
    held = the_pot_and_the_rest(line)[0] or _the_money_already_held(memory)
    if held and 0 < held < aim:
        aim = aim - held
    if when:
        return ("How much do i need to put by a week to have %s pounds by %s?"
                % (format(aim, ","), _in_the_money_readers_words(when)))
    return ("How much do i need to put by a week to have %s pounds?" % format(aim, ","))


OTHER_POT = re.compile(r"\s*(?:into|in|towards|toward|for)\s+(?:a|an|my|our|the|his|her|their)\s+"
                       r"[a-z]", re.I)
RATE_GIVEN = re.compile(r"\b(?:putting by|putting away|put by|put away|setting aside|set aside|"
                        r"saving|saved|save|stashing|stash)\b", re.I)
RATE_VERB = re.compile(r"\b(?:putting|put|setting|set|stashing|stash|socking|sock|saving|save)\b",
                       re.I)
FILLER_LEAD = re.compile(r"^\s*(?:(?:and|but|so|then|also|ok|okay|well|if|maybe|what\s+if|how\s+about|"
                         r"i|we|i'd|we'd|could|can|would|will|shall|should|might|to|just|try|"
                         r"trying)\b[\s,]+)*", re.I)
BARE_RATE = re.compile(r"(?:£\s*)?(\d[\d,]*)\s*(?:pounds?|quid|aside|away|by|back)?", re.I)


SAVE_VERB = re.compile(r"^\s*sav(?:e|es|ing)\b", re.I)
CONDITIONAL = re.compile(r"\b(?:if|what\s+if|could|can|would|might)\b", re.I)


def _a_rate_said(line):
    found = A_RATE.search(line or "")
    if found:
        try:
            return int(found.group(1).replace(",", "")), True
        except ValueError:
            return 0, False
    if INTENT.search(line or "") or re.search(r"£|\bpounds?\b|\bquid\b", line or "", re.I):
        return 0, False
    rest = FILLER_LEAD.sub("", str(line or "")).strip(" ,.")
    verb = RATE_GIVEN.match(rest) or RATE_VERB.match(rest)
    if not verb:
        return 0, False
    if SAVE_VERB.match(rest) and not CONDITIONAL.search(line or ""):
        return 0, False
    rest = rest[verb.end():].strip(" ,.")
    match = BARE_RATE.fullmatch(rest)
    if not match:
        return 0, False
    try:
        return int(match.group(1).replace(",", "")), False
    except ValueError:
        return 0, False


def a_rate_for_the_goal(text, memory):
    line = str(text or "")
    if not isinstance(memory, dict) or not line.strip():
        return ""
    if not RATE_GIVEN.search(line) and not RATE_VERB.search(line):
        return ""
    if _only_a_sum(line) or _only_a_date(line):
        return ""
    if re.search(r"\bfor\s+(?:\d|a|an|two|three|four|five|six)", line, re.I):
        return ""
    rate, _period = _a_rate_said(line)
    if not rate:
        return ""
    found = A_RATE.search(line)
    if found:
        tail = line[found.end():]
        if NOT_A_POT.match(tail) or OTHER_POT.match(tail):
            return ""
    goal = _the_money_still_to_find(memory)
    if goal <= rate:
        return ""
    when = _the_date_in_the_chat(memory)
    if when:
        against = _a_date_on_a_rate(goal, rate, when)
        if against:
            return against
    months = -(-goal // rate)
    closing = _a_closer(memory)
    said = ("£%s at £%s a month is %s." % (format(goal, ","), format(rate, ","), _months(months)))
    return said + (" " + closing if closing else "")


ADDED = re.compile(r"\b(?:another|extra|plus|more|on\s+top)\b", re.I)
A_RESTATED_RATE = re.compile(r"^\s*(?:(?:and|but|so|then|ok|okay|right)\b[\s,]*)*"
                             r"(?:£\s*)?(\d[\d,]*)\s*(?:pounds?\s+)?(?:a|per|each)\s+month"
                             r"\s*(?:then|now)?\s*[.!]*\s*$", re.I)


def _the_added_sum(line):
    found = re.search(r"(?:£\s*)?(\d[\d,]*(?:\.\d+)?)\s*(k|grand|thousand)?", line or "")
    if not found:
        return 0
    try:
        value = float(found.group(1).replace(",", ""))
    except ValueError:
        return 0
    if (found.group(2) or "").lower() in ("k", "grand", "thousand"):
        value *= 1000
    value = int(value)
    if value < 5 or value > 5000:
        return 0
    return value


def a_rate_raised(text, memory):
    line = str(text or "")
    if not isinstance(memory, dict) or not line.strip():
        return ""
    goal = _the_money_still_to_find(memory) or _the_goal_in_the_answer(memory)
    rate = _the_rate_in_the_chat(memory)
    if not goal or not rate or goal <= rate:
        return ""
    restated = A_RESTATED_RATE.match(line)
    if restated:
        try:
            named = int(restated.group(1).replace(",", ""))
        except ValueError:
            return ""
        if named <= rate or named >= goal:
            return ""
        if _said_a_rate_at(named, memory):
            return ("That is the rate: put the standing order in for £%s the day after payday and "
                    "the £%s takes care of itself from there."
                    % (format(named, ","), format(goal, ",")))
        return _a_rate_against_the_goal(goal, named, memory)
    if not ADDED.search(line):
        return ""
    if _names_a_goal(line):
        return ""
    added = _the_added_sum(line)
    if not added:
        return ""
    raised = rate + added
    if raised >= goal:
        return ""
    return _a_rate_against_the_goal(goal, raised, memory)


def _said_a_rate_at(rate, memory):
    turns = [t for t in (memory.get("turns") or []) if isinstance(t, dict) and t.get("bot")]
    if not turns:
        return False
    last = str(turns[-1].get("bot") or "")
    return bool(re.search(r"£\s*%s\s*a\s+month" % format(rate, ",").replace(",", ",?"), last))


def _a_rate_against_the_goal(goal, rate, memory):
    months = -(-goal // rate)
    said = "£%s at £%s a month is %s." % (format(goal, ","), format(rate, ","), _months(months))
    closing = _a_closer(memory)
    return said + (" " + closing if closing else "")


SAVING_CLOSERS = (
    "A standing order the day after payday does it without you deciding again, and any interest or "
    "pay rise only shortens it.",
    "Set it up as a standing order for the day after payday, so the month cannot quietly spend what "
    "the plan needs.",
    "The day after payday is the day to move it, before the rest of the month gets a look at it.",
)


def _a_closer(memory):
    turns = [t for t in (memory.get("turns") or []) if isinstance(t, dict) and t.get("bot")]
    last = str(turns[-1].get("bot") or "").lower() if turns else ""
    said = set(re.findall(r"[a-z']+", last))
    for closing in SAVING_CLOSERS:
        words = [word for word in re.findall(r"[a-z']+", closing.lower()) if len(word) > 3]
        here = sum(1 for word in words if word in said)
        if words and here * 2 >= len(words):
            continue
        return closing
    return ""

def _a_said_sentence(sentence, said):
    words = [word for word in re.findall(r"[a-z']+", sentence.lower()) if len(word) > 3]
    if len(words) < 4:
        return False
    here = sum(1 for word in words if word in said)
    return here * 4 >= len(words) * 3


def said_already(reply, memory):
    first = re.split(r"(?<=[.!?])\s+", str(reply or "").strip())[0]
    if not first:
        return False
    turns = [t for t in (memory.get("turns") or []) if isinstance(t, dict) and t.get("bot")]
    if not turns:
        return False
    said = set(re.findall(r"[a-z']+", str(turns[-1].get("bot") or "").lower()))
    return bool(said) and _a_said_sentence(first, said)


A_WEEK_ASK = "how much should i put by each week"


def _weeks_left(when):
    import datetime

    month = _month_of(when)
    if not month:
        return 0
    today = datetime.date.today()
    number = MONTHS.index(month) + 1
    year = today.year + (1 if number <= today.month else 0)
    days = (datetime.date(year, number, 1) - today).days
    return max(-(-days // 7), 0)


A_MONTH_FIGURE = re.compile(r"£\s*(\d[\d,]*)\s*a\s+month", re.I)


def a_figure_each_week(memory):
    aim, when = _the_money_still_to_find(memory), _the_date_in_the_chat(memory)
    weeks = _weeks_left(when)
    if not aim or weeks < 2:
        return ""
    a_week = -(-aim // weeks)
    said = None
    turns = [t for t in (memory.get("turns") or []) if isinstance(t, dict) and t.get("bot")]
    found = A_MONTH_FIGURE.search(str(turns[-1].get("bot") or "")) if turns else None
    if found:
        said = "£%s a month is" % found.group(1)
    if not said:
        said = "£%s by %s is" % (format(aim, ","), str(when).capitalize())
    said += " about £%s a week over the %s weeks left" % (format(a_week, ","), format(weeks, ","))
    closing = _a_closer(memory)
    if closing:
        return said + " — " + closing[0].lower() + closing[1:]
    return said + "."


def the_figure_a_week(memory):
    if not _the_goal_in_the_chat(memory) or not _the_date_in_the_chat(memory):
        return ""
    return A_WEEK_ASK


def without_what_was_just_said(reply, memory):
    reply = str(reply or "")
    if not reply or not isinstance(memory, dict):
        return reply
    if "\n" in reply:
        return reply
    turns = [t for t in (memory.get("turns") or []) if isinstance(t, dict) and t.get("bot")]
    if not turns:
        return reply
    said = set(re.findall(r"[a-z']+", str(turns[-1].get("bot") or "").lower()))
    if not said:
        return reply
    parts = [part for part in re.split(r"(?<=[.!?])\s+", reply.strip()) if part.strip()]
    if len(parts) < 2:
        return reply
    kept = [parts[0]] + [part for part in parts[1:] if not _a_said_sentence(part, said)]
    return " ".join(kept)


ASKS_A_LENGTH_FOR_A_THING = re.compile(
    r"\bhow\s+(?:many|long)\b[^?.!,]{0,32}?\b(?:weeks?|months?|years?|days?)\b"
    r"|\bhow\s+long\b[^?.!,]{0,32}?\b(?:until|till|before|to\s+buy|to\s+afford|to\s+get)\b"
    r"|\bwhen\s+(?:can|will)\s+i\s+(?:afford|buy|get)\b", re.I)
THE_THING_WANTED = re.compile(
    r"\b(?:afford|buy|pay\s+for|save\s+up\s+for|have\s+enough\s+for)\b"
    r"|\bget\s+(?:it|one|ones|them|that|this|another)\b", re.I)
A_THING_NAMED = re.compile(r"\b(?:afford|buy|get|pay\s+for)\s+(?:a|an|the|my|our|another|some)?\s*"
                           r"([a-z][a-z'-]{2,})", re.I)
NOT_A_THING = frozenset(("it", "one", "ones", "them", "that", "this", "thing", "stuff", "something",
                         "anything", "enough", "there", "what", "which"))


PUT_BY = re.compile(
    r"\bsav(?:e|es|ed|ing|ings)\b"
    r"|\bput(?:ting)?\b[^.]{0,24}?\b(?:aside|by|away)\b"
    r"|\bset(?:ting)?\b[^.]{0,24}?\baside\b"
    r"|\bspar(?:e|es|ed|ing)\b"
    r"|\bsock(?:ing)?\b[^.]{0,12}?\baway\b"
    r"|\btuck(?:ing)?\b[^.]{0,12}?\baway\b"
    r"|\bsave\s+up\b", re.I)
MONEY_OUT = re.compile(
    r"\brent\b|\bmortgage\b|\bchildcare\b|\bnursery\b|\bwages?\b|\bsalary\b|\bpay\b|\bpaid\b"
    r"|\bbills?\b|\bloan\b|\binsurance\b|\bcouncil\s+tax\b|\belectricity\b|\bheating\b"
    r"|\bwater\s+bill\b|\bsubscriptions?\b|\bpayment\b|\bpayments\b|\bpaying\b"
    r"|\bcost(?:s|ing)?\b|\bfees?\b|\bfare\b|\bfares?\b|\btax\b", re.I)


def _the_rate_put_by(memory):
    turns = [t for t in (memory.get("turns") or []) if isinstance(t, dict)]
    window = turns[-6:]
    if not any(PUT_BY.search(str(turn.get("user") or "")) for turn in window):
        return 0
    for turn in reversed(window):
        line = str(turn.get("user") or "")
        found = A_RATE.search(line)
        if not found or MONEY_OUT.search(line):
            continue
        try:
            value = int(found.group(1).replace(",", ""))
        except ValueError:
            continue
        if value >= 10:
            return value
    return 0


def a_length_with_no_price(text, memory):
    line = " ".join(str(text or "").lower().split())
    if not isinstance(memory, dict) or not line:
        return ""
    if not ASKS_A_LENGTH_FOR_A_THING.search(line) or not THE_THING_WANTED.search(line):
        return ""
    if re.search(r"\d", line):
        return ""
    rate = _the_rate_put_by(memory)
    if rate < 10:
        return ""
    if _the_goal_in_the_chat(memory) or _the_goal_in_the_answer(memory):
        return ""
    six_months, a_year = rate * 6, rate * 12
    said = ("£%s a month is £%s every six months, £%s in a year."
            % (format(rate, ","), format(six_months, ","), format(a_year, ",")))
    named = A_THING_NAMED.search(line)
    thing = ""
    if named and named.group(1).lower() not in NOT_A_THING:
        thing = " " + named.group(1).lower()
    asked = ("What's the%s going for?" % thing) if thing else "What's the price on it?"
    if _already_asked_for_the_price(memory):
        return said + " Tell me the price and I'll do the weeks."
    return said + " " + asked


def _already_asked_for_the_price(memory):
    turns = [t for t in (memory.get("turns") or []) if isinstance(t, dict) and t.get("bot")]
    if not turns:
        return False
    above = str(turns[-1].get("bot") or "").lower()
    return bool(re.search(r"\bwhat(?:'s| is) (?:the |it |that )?(?:.* )?going for\b"
                          r"|\bwhat'?s the price\b|\bwhat does it cost\b|\bhow much is it\b", above))


def a_price_in_an_answer(text, memory):
    line = " ".join(str(text or "").lower().split())
    if not isinstance(memory, dict) or not line or len(line.split()) > 7:
        return ""
    price = _a_sum(line)
    if not price or _only_a_date(line) or _a_date(line):
        return ""
    rate = _the_rate_put_by(memory)
    if not rate or rate >= price:
        return ""
    if not _already_asked_for_the_price(memory):
        return ""
    months = -(-price // rate)
    return "£%s at £%s a month is %s." % (format(price, ","), format(rate, ","),
                                           _months(months))
