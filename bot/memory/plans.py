import re

from ..compose import pick
from ..knowledge import lookup
from ..understanding import understand
from .when import CALENDAR_NOW

_SELF = r"^(?:(?:so|ok|okay|and|also|well|right|hmm)[, ]+)*"
_WHO = (r"(?:i'm|im|i am|we're|we are|"
        r"(?:me|i) and [a-z]+ (?:are|'re)|[a-z]+ and i (?:are|'re))")
_PLANNING = re.compile(_SELF + _WHO + r"\s+"
                       r"(?:planning|sorting out|organising|organizing|arranging)\b"
                       r"(?:\s+(?:a|an|the|my|our|some))?\s+(?P<thing>[a-z][a-z ']{2,40})", re.I)
_MOVING = re.compile(_SELF + _WHO + r"\s+moving\s+"
                     r"(?:house|home|flat|out|in\b|to\s+[a-z]+|next|soon|this|in\s)", re.I)
_MARRYING = re.compile(_SELF + _WHO + r"\s+getting married\b", re.I)
_NEW_JOB = re.compile(_SELF + r"(?:i'm|im|i am|i|we're|we are|we)?\s*"
                      r"(?:start|starts|starting|begin|beginning)\s+"
                      r"(?:a |my |our )?(?:new )?(?P<what>job|work)\b(?P<after>.*)", re.I)


_WORK_WHEN = re.compile(r"^\s*(?:(?:on|by)\s+(?:the\s+)?(?:\d+|first|last|" + "|".join([
    "monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday",
    "mon", "tues", "tue", "weds", "wed", "thurs", "thu", "thur", "fri", "sat", "sun"]) +
    r")(?:st|nd|rd|th)?|next\s+(?:week|month|monday|tuesday|wednesday|thursday|friday|"
    r"saturday|sunday)|tomorrow|today|this\s+(?:week|month|monday|tuesday|wednesday|"
    r"thursday|friday|saturday|sunday))\b", re.I)


def _a_first_day(text):
    found = _NEW_JOB.search(text or "")
    if not found:
        return False
    if found.group("what").lower() == "job":
        return True
    after = re.sub(r"[\s.,!?;:'\"()]", "", found.group("after") or "")
    if not after:
        return True
    return bool(_WORK_WHEN.match(found.group("after") or ""))

_ASK_FOR = (
    (_MARRYING.search, "how do i plan a wedding"),
    (_MOVING.search, "what do i need to do to move house"),
    (_a_first_day, "first day at a new job"),
)

_ASKING = re.compile(r"\?|\b(?:what|how|when|where|which|who|why|should|shall|can|could|would|"
                     r"do i need|do we need|any (?:tips|ideas|advice))\b", re.I)
_TURNED = re.compile(r"\bbut\b|\bthough\b|\bexcept\b|\bonly\b|\bhowever\b", re.I)
_DENIED = re.compile(r"\b(?:not|never|no longer|arent|isnt|wasnt|dont|doesnt)\b|n't\b", re.I)
_ABOUT_A_DEATH = re.compile(
    r"\b(?:grave|graves|graveside|cemetery|ashes|funeral|funerals|burial|buried|cremation|"
    r"cremated|crematorium|memorial|hospice|dying|died|death|passed away|"
    r"say goodbye|last goodbye)\b", re.I)


def as_question(text):
    question, _ = _implied(text)
    return question


def _implied(text):
    clean = " ".join(str(text or "").lower().split())
    if (not clean or _ASKING.search(clean) or _TURNED.search(clean) or _DENIED.search(clean)
            or _ABOUT_A_DEATH.search(clean)):
        return None, False
    for test, ask in _ASK_FOR:
        if test(clean):
            return ask, True
    found = _PLANNING.search(clean)
    if found:
        thing = found.group("thing").strip(" .!,")
        if thing.startswith("to "):
            return None, False
        thing = re.sub(r"\s+(?:next|this|in|on|for)\s+\w+.*$", "", thing).strip()
        if thing:
            if thing.startswith(("my ", "our ", "the ")):
                return "how do i plan " + thing, False
            return "how do i plan a " + thing, False
    return None, False


def _the_reply(entry, question, memory):
    reply = getattr(entry, "reply", None)
    if callable(reply):
        try:
            reply = reply(memory if isinstance(memory, dict) else {},
                          understand(question, memory if isinstance(memory, dict) else {}))
        except Exception:
            return ""
    elif isinstance(reply, (list, tuple)):
        reply = pick(reply, memory if isinstance(memory, dict) else {})
    return reply if isinstance(reply, str) else ""


def answer(text, memory=None):
    question, by_hand = _implied(text)
    if not question:
        return None
    try:
        entry = lookup.find(understand(question, memory if isinstance(memory, dict) else {}))
    except Exception:
        return None
    if entry is None:
        return None
    if not by_hand and not _about_planning(entry):
        return None
    reply = _the_reply(entry, question, memory)
    if not isinstance(reply, str) or not reply.strip():
        return None
    if reply[:1].islower():
        return None
    return reply.strip()


PLANNING_KEYS = frozenset("""
plan plans planning planned prepare preparing preparation organise organises organising
organize organized organizing arrange arranging countdown checklist need needs booking book
budget budgeting
""".split())


def _about_planning(entry):
    words = set()
    for part in getattr(entry, "key", ()) or ():
        for piece in (part if isinstance(part, tuple) else (part,)):
            for word in str(piece).lower().replace("'", "").split():
                words.add(word)
    return bool(words & PLANNING_KEYS)


_PART_WORDS = frozenset("""
a an the and or but if so to of in on at for with about from by as is are was were be been do
does did doing done i im me my we our you your it its that this these those what which how when
where who why should could would can will shall may might must not no yes please just really
any some more most first next then now again also too very get got getting go going want need
need to know tell say said help good best way ways thing things
""".split())


_A_LENGTH_ASK = re.compile(r"\bhow long\b|\bhow soon\b|\bhow far ahead\b|"
                           r"\bhow many (?:weeks|days|months|hours)\b|\bwhat order\b|"
                           r"\bbefore i go\b|\btimeline\b", re.I)


_SPAN_HEAD = re.compile(r"\b(?:" + "|".join([
    r"\d+", r"a", r"an", r"one", r"two", r"three", r"four", r"five", r"six", r"seven", r"eight",
    r"nine", r"ten", r"eleven", r"twelve"]) +
    r")\s+(?:day|week|month|year)s?\s+(?:out|before|ahead)\b"
    r"|\bthe (?:day|week|month|year) before\b", re.I)


def _the_clauses(detail):
    return [part.strip(" .;") for part in re.split(r",\s*|;\s*|\s+and\s+", detail)
            if part.strip(" .;")]


def _the_step(detail, wanted, first_only=False):
    if first_only:
        clauses = _the_clauses(detail)
        return clauses[0] if clauses else detail.strip(" .")
    best, best_hit = None, 0
    for clause in _the_clauses(detail):
        hit = len(wanted & _part_words(clause))
        if hit > best_hit:
            best, best_hit = clause, hit
    clauses = _the_clauses(detail)
    return best or (clauses[0] if clauses else detail.strip(" ."))


_A_CLAUSE_BREAK = re.compile(r"(?:,|;|\s-\s|:\s)")


def _the_first_step(sentence):
    text = " ".join(str(sentence or "").split()).rstrip(".")
    if not text:
        return None
    parts = [part.strip() for part in _A_CLAUSE_BREAK.split(text) if part.strip()]
    step = ""
    for part in parts:
        step = (step + ", " + part) if step else part
        if len(step.split()) >= 4:
            break
    if not step:
        return None
    if len(step.split()) >= len(text.split()):
        step = text
    return "Start with this: " + step[0].lower() + step[1:] + "."


def _a_countdown_step(head, detail, wanted, about_the_start):
    step = _the_step(detail, wanted, about_the_start)
    if not step:
        return None
    said = head.strip().rstrip(":") + (":" if not about_the_start else " is when to start:")
    return said + " " + step[0].lower() + step[1:] + "."


_ASK_WORDS = frozenset("""long soon far ahead many much weeks week days day months month hours
    hour minutes minute time take takes last before order timeline go going get""".split())


def _another_thing(wanted, said_words):
    return any(word not in _ASK_WORDS and len(word) > 3 and word not in said_words
               for word in wanted)


_A_FIRST_ASK = re.compile(r"\b(?:what(?:'s|s| is)? (?:the )?(?:first|next)|"
                          r"what (?:should |will |does )?comes? first|"
                          r"what do i do(?: first)?|what should i do(?: first)?|"
                          r"where (?:do|should) i (?:start|begin)|how do i (?:start|begin)|"
                          r"first (?:thing|step|bit)|what first)\b", re.I)


_ORDER_WORDS = frozenset("""first comes start begin next thing things step steps order point
    anything else now again should could would can will might must the and then so about
    whats what come""".split())


def _part_words(text):
    return {word for word in re.findall(r"[a-z']+", " ".join(str(text or "").lower().split()))
            if word not in _PART_WORDS and len(word) > 2}


def _was_a_plan(line):
    clean = " ".join(str(line or "").lower().split())
    if not clean:
        return False
    if _implied(clean)[0]:
        return True
    return bool(_PLAN_ASK.search(clean))


_PLAN_ASK = re.compile(
    r"how\s+(?:do|can|should)\s+i\s+(?:plan|prepare for|get ready for|start planning)\b")


def follow_up(text, memory):
    if not isinstance(memory, dict) or not isinstance(text, str):
        return None
    if CALENDAR_NOW.match(" ".join(text.split()).strip(" .!?;,")):
        return None
    turns = memory.get("turns")
    if not isinstance(turns, list) or not turns or not isinstance(turns[-1], dict):
        return None
    last = turns[-1]
    said = ""
    reply = " ".join(str(last.get("bot") or "").lower().split())
    kept = memory.get("plan_answer")
    if isinstance(kept, dict) and _was_a_plan(kept.get("user")):
        announced = " ".join(str(kept.get("user") or "").lower().split())
        if announced and announced == " ".join(str(last.get("user") or "").lower().split()):
            said = " ".join(str(kept.get("text") or "").split())
    if not said:
        told = memory.get("entry_answer")
        said = str((told or {}).get("text") or "")
        whole = " ".join(said.lower().split())
        if not said or not reply or not (whole[:60] in reply or reply[:60] in whole):
            return None
        if last.get("module") != "memory_store" and not _was_a_plan(last.get("user")):
            return None
    if not (text.rstrip().endswith("?") or _ASKING.search(text) or _A_FIRST_ASK.search(text)):
        return None
    wanted = _part_words(text)
    sentences = [part.strip() for part in re.split(r"(?<=[.!?])\s+", said) if part.strip()]
    if _A_FIRST_ASK.search(text) and not _another_thing(wanted - _ORDER_WORDS, _part_words(said)):
        head, colon, detail = (sentences[0].partition(":") if sentences else ("", "", ""))
        if colon and _SPAN_HEAD.search(head) and detail.strip():
            return _a_countdown_step(head, detail, set(), False)
        return _the_first_step(sentences[0]) if sentences else None
    if not wanted:
        return None
    head, colon, detail = (sentences[0].partition(":") if sentences else ("", "", ""))
    span = bool(colon and _SPAN_HEAD.search(head))
    opening = None
    asked_about = []
    if colon and detail.strip():
        opening = detail.strip()[0].upper() + detail.strip()[1:]
        asked_about.append((opening, _part_words(detail) | _part_words(head)))
    asked_about += [(sentence, _part_words(sentence)) for sentence in sentences[1:]]
    best, best_hit = None, 0
    for sentence, words in asked_about:
        if reply.startswith(" ".join(sentence.lower().split())[:40]):
            continue
        hit = len(wanted & words)
        if hit and (best is None or hit >= best_hit):
            best, best_hit = sentence, hit
    if best is None:
        if (span and _A_LENGTH_ASK.search(text)
                and not _another_thing(wanted, _part_words(said))):
            return _a_countdown_step(head, detail, wanted, True)
        return None
    if best == opening and span:
        return _a_countdown_step(head, detail, wanted, bool(_A_LENGTH_ASK.search(text)))
    return best
