import re

from ..memory import last_user
from .store_lines import CLOCK_SAID, ROUTINE_SAY_BACK, ROUTINE_SUBJECT

ROUTINE_CLAIM = re.compile(
    r"\b" + ROUTINE_SUBJECT + r"\b(?P<mid>[a-z' ,]{1,26}?)\b(?:at|around|about|round|by)\s+"
    r"(?P<at>" + CLOCK_SAID + r")\b", re.I)
ROUTINE_SHIFT = re.compile(
    r"\bmy (?P<thing>shift|work|job|hours)\s+(?P<verb>starts?|begins?|ends?|finishes?)\s+"
    r"(?:at|around|about)\s+(?P<at>" + CLOCK_SAID + r")\b", re.I)
ROUTINE_WORK_START = re.compile(
    r"\b(?:start|starts|started|starting|begin|begins|beginning|clock in|clocking in|"
    r"get in|gets in|arrive|arrives)\b")
ROUTINE_WORK_END = re.compile(
    r"\b(?:finish|finishes|finishing|leave|leaves|leaving|get off|getting off|clock out|"
    r"clocking out|end|ends|ending)\b")


def _a_routine(phrase, ask=False):
    low = " ".join(re.sub(r"[^a-z' ]", " ", phrase.lower()).split())
    if not low:
        return ""
    if re.search(r"\bbed\b|\bsleep\b|\bturn in\b", low):
        return "go to bed"
    work = "work" in low or "shift" in low or "job" in low
    if work and ROUTINE_WORK_END.search(low):
        return "finish work"
    if work and ROUTINE_WORK_START.search(low):
        return "start work"
    if re.search(r"\bhome\b", low):
        return "get home"
    if re.search(r"\bup\b", low):
        return "get up"
    if re.search(r"\b(?:leave|leaves|leaving|set off|head off|go out)\b", low):
        return "leave"
    if ask:
        if re.search(r"\b(?:start|starts|begin|begins)\b", low):
            return "start work"
        if re.search(r"\b(?:finish|finishes|end|ends|clock out)\b", low):
            return "finish work"
    return ""


def _the_times(memory):
    held = memory.get("times")
    if not isinstance(held, list):
        held = []
    return held


def _keep_a_time(memory, what, at, said):
    at = str(at or "").strip(" .,!;:-")
    if not what or not at:
        return
    held = _the_times(memory)
    turn = len(memory.get("turns") or [])
    for item in held:
        if isinstance(item, dict) and item.get("what") == what:
            item["at"] = at
            item["said"] = said
            item["turn"] = turn
            break
    else:
        held.append({"what": what, "at": at, "said": said, "turn": turn})
    memory["times"] = held[-8:]


ROUTINE_MORE = re.compile(
    r"^(?:and |it |that |then )*(?P<verb>ends?|finishes?|starts?|begins?)\s+(?:at|around|about)\s+"
    r"(?P<at>" + CLOCK_SAID + r")[\s.!]*$", re.I)


TIME_FIX = re.compile(
    r"^(?:(?:ok|okay|oh|sorry|no|nope|nah|wait|actually|rather|i mean|i meant|meant|i said"
    r"|make that|make it|hmm|erm)[ ,]+)*(?:at |more like |it's |its )?(?P<at>" + CLOCK_SAID + r")"
    r"(?:\s*(?:instead|o'clock|oclock|sorry|then))*"
    r"(?:\s+not\s+(?P<was>" + CLOCK_SAID + r"))?[\s.!?]*$", re.I)


def keep(text, memory):
    if not isinstance(text, str) or not isinstance(memory, dict):
        return
    said = " ".join(text.split())
    low = said.lower()
    filed = False
    for match in ROUTINE_SHIFT.finditer(low):
        start = match.group("verb").lower().startswith(("start", "begin"))
        _keep_a_time(memory, "start work" if start else "finish work", match.group("at"), said)
        filed = True
    for match in ROUTINE_CLAIM.finditer(low):
        what = _a_routine(match.group("mid"))
        if what:
            _keep_a_time(memory, what, match.group("at"), said)
            filed = True
    if filed:
        return
    held = _the_times(memory)
    more = ROUTINE_MORE.match(low.strip(" .,!;"))
    if more and held and isinstance(held[-1], dict):
        last = held[-1]
        if last.get("what") in ("start work", "finish work"):
            if len(memory.get("turns") or []) - int(last.get("turn") or 0) <= 1:
                which = ("finish work" if more.group("verb").lower().startswith(("end", "finish"))
                         else "start work")
                _keep_a_time(memory, which, more.group("at"), said)
                return
    held = _the_times(memory)
    fixed = TIME_FIX.match(low.strip(" .,!;"))
    if not held or not fixed:
        return
    last = held[-1]
    if not isinstance(last, dict):
        return
    if len(memory.get("turns") or []) - int(last.get("turn") or 0) > 1:
        if not answer(last_user(memory) or "", memory):
            return
    was = str(last.get("at") or "").strip()
    last["at"] = fixed.group("at").strip(" .,!;:")
    last["said"] = said
    last["turn"] = len(memory.get("turns") or [])
    memory["fixed_time"] = {"what": last.get("what"), "at": last["at"], "from": was,
                            "turn": last["turn"], "said": said}


ROUTINE_ASK = re.compile(
    r"^\s*(?:and |so |ok |okay |oh |but |also |then )*"
    r"(?:at what time|what time|what's the time|when)\b(?P<rest>.*)$", re.I)
ROUTINE_ASK_FILLER = frozenset("""do does did will am are is was were i we my the a an your our
usually normally generally tend tends to of for going go about around""".split())


def answer(text, memory):
    if not isinstance(text, str) or not isinstance(memory, dict):
        return None
    asked = ROUTINE_ASK.match(" ".join(text.split()))
    if not asked:
        return None
    rest = asked.group("rest")
    held = {item.get("what"): item.get("at") for item in _the_times(memory)
            if isinstance(item, dict) and item.get("at")}
    if not held:
        return None
    what = _a_routine(rest, ask=True)
    if not what:
        if re.search(r"\b(?:shift|work|job)\b", rest.lower()):
            start_at, end_at = held.get("start work"), held.get("finish work")
            if start_at and end_at:
                return "Your shift runs from " + start_at + " to " + end_at + "."
            what = "start work" if start_at else "finish work" if end_at else ""
        if not what:
            return None
    words = [word for word in re.sub(r"[^a-z' ]", " ", rest.lower()).split()
             if word not in ROUTINE_ASK_FILLER]
    if len(words) > 3:
        return None
    at = held.get(what)
    if not at:
        return None
    said_back = ROUTINE_SAY_BACK.get(what) or "You {what} at {at}."
    return said_back.format(at=at, what=what)


def is_a_time_ask(text, memory):
    if not answer(text, memory):
        return False
    asked = ROUTINE_ASK.match(" ".join(str(text or "").split()))
    if not asked:
        return False
    rest = asked.group("rest")
    what = _a_routine(rest, ask=True) or ""
    if not what and re.search(r"\b(?:shift|work|job)\b", rest.lower()):
        what = "start work"
    if not what:
        return False
    words = [word for word in re.sub(r"[^a-z' ]", " ", rest.lower()).split()
             if word not in ROUTINE_ASK_FILLER]
    return len(words) <= 2


