import re

from ..compose import pick


RATES_TEXT = (r"(?:once|twice)(?:\s+(?:a|per|each)\s+(?:hour|day|week|fortnight|month|year))?"
             r"|(?:(?:\d+|two|three|four|five|six|seven|eight)\s+times?)"
             r"\s+(?:a|per|each)\s+(?:hour|day|week|fortnight|month|year)"
             r"|every\s+(?:\d+|a|an|one|two|three|four|five|six|few)\s+"
             r"(?:hours?|minutes?|days?|weeks?|months?|nights?)"
             r"|every\s+(?:hour|day|week|morning|evening|night|weekend|other\s+day|monday|tuesday"
             r"|wednesday|thursday|friday|saturday|sunday)"
             r"|most\s+(?:days|weeks|mornings|evenings)")
RATES_END = r"(?![a-z])"
RATES_SAID = re.compile(r"\b(?P<how>" + RATES_TEXT + r")" + RATES_END, re.I)
RATES_SUBJECT = re.compile(
    r"^(?P<lead>and\s+|so\s+|also\s+|oh\s+|well\s+|but\s+|"
    r"actually\s+|no\s+|sorry\s+|make it\s+|i mean\s+|i meant\s+|rather\s+|instead\s+)*"
    r"(?P<subj>i|we|i'm|im|i've|ive|we're|were)\b(?P<rest>.*)$", re.I)
RATES_FIX_LEAD = frozenset(("actually", "no", "sorry", "make", "i mean", "i meant", "rather",
                           "instead"))
RATES_IGNORE = frozenset("""i we my our me the a an at on in to for of it that this and but so
just now only really still usually normally about around im ive were don't dont""".split())
RATES_ASK_LEAD = frozenset("""how what when where why who which whose should shall can could
would will do does did is are was were if whether whats hows remind tell""".split())
RATES_LEAD = re.compile(r"^(?:and|so|but|also|oh|well|then|just|now|ok|okay|plus)\s+", re.I)

RATES_CORRECTION_LEAD = (r"(?:actually|no\s+wait|no|sorry|wait|hang\s+on|make\s+it|i\s+mean"
                         r"|i\s+meant|rather|instead)")
RATES_CORRECTION_TAIL = r"(?:\s+(?:now|instead|actually|these\s+days|not))?\s*[.!]*\s*$"
A_BARE_COUNT = re.compile(
    r"^\s*" + RATES_CORRECTION_LEAD + r"\b[,\s:]*"
    r"(?P<num>\d+|two|three|four|five|six|seven|eight|nine|ten)\s+times?"
    r"(?:\s+(?:a|per|each)\s+(?P<period>day|week|fortnight|month|year))?"
    + RATES_CORRECTION_TAIL, re.I)
A_BARE_RATE = re.compile(r"^\s*" + RATES_CORRECTION_LEAD + r"\b[,\s:]*"
                         r"(?P<how>" + RATES_TEXT + r")" + RATES_CORRECTION_TAIL, re.I)
A_COUNT_AND_PERIOD = re.compile(
    r"^(?P<num>\d+|two|three|four|five|six|seven|eight|nine|ten)\s+times?"
    r"\s+(?:a|per|each)\s+(?P<period>day|week|fortnight|month|year)$", re.I)


def _the_rates(memory):
    held = memory.get("rates")
    return held if isinstance(held, list) else []


RATES_FILLER_LEAD = frozenset("""and so but also oh well then plus just still only now really
actually normally usually today tomorrow tonight yesterday""".split())


def _keep_a_rate_of_a_doing(said, rate, memory):
    words = said.split()
    if not words or words[0] in RATES_ASK_LEAD or RATES_ASK.search(said) \
            or RATES_ADVICE.search(said):
        return
    if words[0] in ("you", "your", "yours", "themselves"):
        return
    what = RATES_SAID.sub(" ", said)
    what = " ".join(what.split()).strip(" .,!;:-")
    lead = what.split()[:1]
    if lead and lead[0] in RATES_FILLER_LEAD:
        what = " ".join(what.split()[1:]).strip(" .,!;:-")
    if not what or not [w for w in re.findall(r"[a-z']+", what) if w not in RATES_IGNORE]:
        return
    _keep_a_rate(memory, what, rate.group("how"), said, own=False)


def _keep_a_rate(memory, what, how, said, own=True):
    what = " ".join(str(what or "").split()).strip(" .,!;:-")
    how = " ".join(str(how or "").split()).strip(" .,!;:-")
    if not what or not how:
        return
    held = _the_rates(memory)
    turn = len(memory.get("turns") or [])
    for item in held:
        if isinstance(item, dict) and item.get("what") == what:
            item["how"] = how
            item["said"] = said
            item["turn"] = turn
            item["own"] = bool(own)
            break
    else:
        held.append({"what": what, "how": how, "said": said, "turn": turn,
                     "own": bool(own)})
    memory["rates"] = held[-8:]


def _the_newest_recent_rate(memory, within=2):
    turn = len(memory.get("turns") or [])
    for item in reversed(_the_rates(memory)):
        if not isinstance(item, dict) or not item.get("how"):
            continue
        if turn - int(item.get("turn") or 0) <= within:
            return item
    return None


def _the_rate_put_right(text, memory):
    said = " ".join(str(text or "").split())
    if not said:
        return False
    count = A_BARE_COUNT.match(said)
    whole = None if count else A_BARE_RATE.match(said)
    if not count and not whole:
        return False
    item = _the_newest_recent_rate(memory)
    if item is None:
        return False
    if count:
        period = count.group("period")
        if not period:
            held = A_COUNT_AND_PERIOD.match(str(item.get("how") or "").strip())
            if held is None:
                return False
            period = held.group("period")
        item["how"] = count.group("num").lower() + " times a " + period.lower()
    else:
        item["how"] = " ".join(whole.group("how").lower().split())
    item["said"] = said.lower()
    item["turn"] = len(memory.get("turns") or [])
    memory["rates"] = _the_rates(memory)
    return True


def keep(text, memory):
    if not isinstance(text, str) or not isinstance(memory, dict):
        return
    if _the_rate_put_right(text, memory):
        return
    for clause in re.split(r"[.;!?,]|\band\b|\bbut\b", text.lower()):
        said = " ".join(clause.split())
        if not said:
            continue
        rate = RATES_SAID.search(said)
        if not rate:
            continue
        subject = RATES_SUBJECT.match(said)
        if not subject:
            _keep_a_rate_of_a_doing(said, rate, memory)
            continue
        if subject.group("subj").lower() not in ("i", "we", "i'm", "im", "i've",
                                                 "ive", "we're", "were"):
            _keep_a_rate_of_a_doing(said, rate, memory)
            continue
        rest = " ".join(subject.group("rest").split())
        inner = RATES_SAID.search(rest)
        what = (rest[:inner.start()] if inner else "").strip(" .,!;:-!")
        what = " ".join(word for word in what.split())
        words = [word for word in re.findall(r"[a-z']+", what) if word not in RATES_IGNORE]
        if not words:
            continue
        lead = (subject.group("lead") or "").strip().split()
        if lead and lead[0] in RATES_FIX_LEAD:
            held = _the_rates(memory)
            turn = len(memory.get("turns") or [])
            for item in reversed(held):
                if not isinstance(item, dict) or not item.get("how"):
                    continue
                mine = set(re.findall(r"[a-z']+", str(item.get("what") or "").lower()))
                theirs = set(re.findall(r"[a-z']+", what.lower()))
                if (mine & theirs) or turn - int(item.get("turn") or 0) <= 2:
                    item["what"] = item.get("what") or what
                    item["how"] = rate.group("how")
                    item["said"] = said
                    item["turn"] = turn
                    memory["rates"] = held
                    break
            else:
                _keep_a_rate(memory, what, rate.group("how"), said)
            continue
        _keep_a_rate(memory, what, rate.group("how"), said)


RATES_ADVICE = re.compile(r"\b(?:should|shall|ought|need(?:s)?|best|recommend\w*|advice)\b", re.I)
RATES_ASK = re.compile(
    r"^\s*(?:and |so |ok |okay |oh |also |then )*(?:remind me\s+)?"
    r"(?:(?P<a>how often|how many times)\b(?P<rest>.*)"
    r"|(?P<c>how (?:many|much)\b(?P<rest3>[^?]*))"
    r"|(?P<b>was|is|were|are)\s+(?:that|it|this)\s+(?P<how>" + RATES_TEXT + r")" + RATES_END +
    r"|what(?:'s|s| is| was)\s+the\s+(?:pattern|rate|schedule)\b(?P<rest2>.*))\s*[?.!]*\s*$", re.I)
COUNTS_A_PERIOD = re.compile(
    r"\b(?:a|per|each)\s+(?:hour|day|week|fortnight|month|year|morning|evening|night)\b", re.I)
RATES_PRONOUN = frozenset("""them they it its it's that this these those him her his hers me us
one ones thing stuff""".split())
RATES_ASK_FILLER = frozenset("""do does did was is were i we my our me the a an you go going
again then was that it this now still say said tell once twice a week day month year times
usually normally have has had get gets got take takes make makes use uses need needs
i'm im've""".split())


def is_a_rate_ask(text, memory):
    return bool(answer(text, memory))


def answer(text, memory):
    if not isinstance(text, str) or not isinstance(memory, dict):
        return None
    held = [item for item in _the_rates(memory) if isinstance(item, dict) and item.get("how")]
    if not held:
        return None
    asked = RATES_ASK.match(" ".join(text.split()))
    if not asked:
        return None
    if RATES_ADVICE.search(asked.group(0)):
        return None
    if asked.group("c") and not COUNTS_A_PERIOD.search(asked.group("c")):
        return None
    rest = (asked.group("rest") or asked.group("rest3") or asked.group("rest2") or "").lower()
    named = {word for word in re.findall(r"[a-z']+", rest) if word not in RATES_ASK_FILLER
             and word not in RATES_PRONOUN and len(word) > 2}
    item = None
    if named:
        for held_item in reversed(held):
            words = {word for word in re.findall(r"[a-z']+",
                                                 str(held_item.get("what") or "").lower())
                     if word not in RATES_PRONOUN}
            if named & words:
                item = held_item
                break
        if item is None:
            return None
    else:
        lean_back = re.search(
            r"\b(?:that|it|this|again|remind|said|say|told|tell)\b",
            asked.group(0).lower())
        if not lean_back and not asked.group("b") and not asked.group("c"):
            return None
        item = held[-1]
    what = " ".join(str(item.get("what") or "").split())
    how = " ".join(str(item.get("how") or "").split())
    if not what or not how:
        return None
    what = re.sub(r"\bmy\b", "your", what)
    what = re.sub(r"\bour\b", "your", what)
    if item.get("own") is False:
        return "You said " + what + " " + how + "."
    if pick([0, 1], memory) == 0:
        said = "You " + what + " " + how + "."
    else:
        said = how[:1].upper() + how[1:] + \
            " \u2014 you " + what + "."
    return said


