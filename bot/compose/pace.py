import re

from . import pick

PACE_ASK = re.compile(r"\bhow (?:slowly|fast|quickly|soon)\b", re.I)

KEEP_UP_ASK = re.compile(
    r"\bhow long (?:should|shall|do|can|could|would) (?:i|we) (?:keep|carry on|go on|stick|stay|"
    r"continue|persist)\b"
    r"|\bhow long (?:should|shall|do|can|could|would) (?:i|we) keep \w+ing\b", re.I)


_A_LENGTH = re.compile(
    r"\b(?:\d+|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|thirteen|fourteen|"
    r"fifteen|sixteen|eighteen|twenty|thirty|forty|fifty|sixty|a few|a couple of|several|a)\s+"
    r"(?:(?:or|to)\s+(?:\d+|two|three|four|five|six|seven|eight|ten|twelve|fifteen|twenty)\s+)?"
    r"(?:weeks?|months?|days?|hours?|minutes?|fortnights?)\b", re.I)

_A_RATE_LEAD = re.compile(
    r"\b(?:\d+|one|two|three|four|five|six|seven|eight|nine|ten|twelve|a|an|once|twice|half)\s+"
    r"(?:runs?|times|sessions?|days?|weeks?|months?|hours?|minutes?|miles?|km|kms|kilometres?|"
    r"reps?|sets?|walks?|workouts?|feeds?|charges?|meals?|nights?)\s+$", re.I)

_ALLOWED = frozenset("""
a an the this that these it i you we me my our
should shall can could would will do does did be is was are am
go going do doing now then again first next too so much more
add build start push increase work step up at on in to of for
run runs running walk walks walking jog jogging going train training slower faster easy harder
slow fast
""".split())

_KEEP_ALLOWED = frozenset("""
looking searching waiting trying watching going at it tonight today now longer long for doing
this that the same way
""".split())

_STEP = re.compile(
    r"\b(?:add|increase|build(?:ing)? up|work(?:ing)? up|step(?:ping)? up|extend|progress)\b"
    r"[^.;]{0,70}\b(?:a|an|each|every|per)\s+(?:week|day|session|run|month|fortnight)\b",
    re.I)

_PACE = re.compile(
    r"\b(?:add|increase|build(?:ing)? up|work(?:ing)? up|step(?:ping)? up|extend|progress|"
    r"no more than|only)\b[^.;]{0,70}\b(?:a|an|each|every|per)\s+"
    r"(?:week|day|session|run|month|fortnight)\b"
    r"|\b(?:one|two|three|four|five|six|\d+)\s+times?\s+a\s+(?:week|day)\b"
    r"|\bevery other day\b"
    r"|\bweek by week\b"
    r"|\ba (?:minute|day|session|week)\s+(?:at a time|more|longer)\b"
    r"|\b(?:a|an|one)\s+\w+(?:\s+\w+)?\s+at a time\b"
    r"|\ba little at a time\b"
    r"|\bgradually\b",
    re.I)

_TEST = re.compile(
    r"[^.;]{0,60}\b(?:slow enough to talk|hold a conversation|talk test|conversational|"
    r"can still talk|able to talk)\b[^.;]{0,60}", re.I)

_LEADS = {
    "slowly": ("Slowly, a step at a time", "Slowly, and only as the plan steps up",
               "Slowly - less than you think"),
    "fast": ("No faster than the plan says", "Only as fast as the answer above says",
             "Not fast - by the plan's own step"),
    "quickly": ("Only as quickly as the plan steps up", "As quickly as the plan says, and no more"),
    "soon": ("No sooner than the answer above says", "Only when the plan says you are ready"),
}

_REST = ("That is the pace the plan sets: {rest}.",
         "The rest of the plan is the check on it: {rest}.",
         "The plan above already says the rest of it: {rest}.")

_NEXT = ("The rest of it is as the answer says: {next}.",
         "Then carry on as the answer says: {next}.",
         "Nothing else changes after that: {next}.")

_TESTED = ("The test is the plan's own - {test}.",
           "Judge it by the one the answer already gives - {test}.",
           "And keep the plan's own check - {test}.")


def _clean(text):
    return " ".join(str(text or "").lower().split())


def asks_the_pace(text, answer=""):
    said = _clean(text).strip(" ?!.,;:'\"")
    found = PACE_ASK.search(said)
    if not found:
        return False
    rest = (said[:found.start()] + " " + said[found.end():]).replace("'s", " ").split()
    words = [re.sub(r"[^a-z0-9]", "", w) for w in rest]
    words = [w for w in words if w]
    if not words:
        return True
    in_the_answer = set(re.findall(r"[a-z']+", str(answer or "").lower()))
    return all(w in _ALLOWED or w in in_the_answer for w in words)


def _last_answer(memory):
    turns = (memory or {}).get("turns") or []
    for turn in reversed(turns):
        if isinstance(turn, dict):
            said = str(turn.get("bot") or "").strip()
            if said:
                return said
    return ""


def _clauses(answer):
    pieces = re.split(r"(?<=[.;!?])\s+|;\s*|,\s*|:\s+|\s+-\s+", str(answer or ""))
    out = []
    for piece in pieces:
        text = " ".join(piece.strip(" ,.;").split())
        text = re.sub(r"^(?:and|but|then|so)\s+", "", text, flags=re.I)
        if text:
            out.append(text)
    return out


def _trim(text, most=96):
    if len(text) <= most:
        return text
    cut = text[:most]
    comma = cut.rfind(",")
    if comma > most // 2:
        cut = cut[:comma]
    else:
        space = cut.rfind(" ")
        if space > most // 2:
            cut = cut[:space]
    return " ".join(cut.split()).rstrip(",;:")


def _parts(answer):
    clauses = _clauses(answer)
    stepped, timed, test, after = [], [], "", ""
    for index, clause in enumerate(clauses):
        if _STEP.search(clause) and len(stepped) < 2:
            stepped.append(_trim(clause))
        elif _PACE.search(clause) and len(timed) < 2:
            timed.append(_trim(clause))
        elif not test and _TEST.search(clause):
            test = _trim(_TEST.search(clause).group(0).strip())
        if (stepped or timed) and not after and not _a_lead_in(clause):
            after = _the_next_step(clauses[index + 1:])
    pace = stepped + timed
    if after in pace:
        after = ""
    return pace, test, after


_CONTINUES = re.compile(r"^(?:for\s|\w+ing\b|until\b|then\s|and\b|so\b|which\b|that\b|"
                        r"it\b|this\b|about\b)", re.I)


def _the_next_step(clauses):
    for clause in clauses:
        clause = _trim(clause)
        if not clause or _a_lead_in(clause) or _CONTINUES.match(clause):
            continue
        if _PACE.search(clause) or _STEP.search(clause):
            continue
        return clause
    return ""


def _a_lead_in(clause):
    return bool(re.match(r"^(?:to start with|first|first of all|for a start)\b", clause, re.I))


def _a_pace_reply(answer):
    opening = " ".join(str(answer or "").split())[:80].lower()
    for leads in _LEADS.values():
        for lead in leads:
            if opening.startswith(lead.lower()[:24]):
                return True
    return False


def asks_the_keep_up(text, answer=""):
    said = _clean(text).strip(" ?!.,;:'\"")
    found = KEEP_UP_ASK.search(said)
    if not found:
        return False
    rest = (said[:found.start()] + " " + said[found.end():]).replace("'s", " ").split()
    words = [re.sub(r"[^a-z0-9]", "", w) for w in rest]
    words = [w for w in words if w]
    if not words:
        return True
    in_the_answer = set(re.findall(r"[a-z']+", str(answer or "").lower()))
    return all(w in _ALLOWED or w in _KEEP_ALLOWED or w in in_the_answer for w in words)


_NOT_A_TAIL = re.compile(
    r"^(?:and|but|so|it|they|them|this|that|the|a|an|after|before|since|until|once|when|while)\b",
    re.I)


def _the_doing(after):
    after = re.sub(r"^(?:of|in|on|for|at)\s+", "", after.strip(" ,.;"))
    cut = re.split(r"\b(?:is|are|was|were|turns?|helps?|makes?|works?|should|will|but)\b",
                   after, maxsplit=1)[0]
    cut = _DANGLES.sub("", cut)
    if cut.count("(") > cut.count(")"):
        cut = cut[:cut.rfind("(")]
    cut = _trim(" ".join(cut.split()).strip(" ,.;-"), 80)
    if len(cut.split()) < 2 or _NOT_A_TAIL.match(cut):
        return ""
    return cut


_DANGLES = re.compile(
    r"\b(?:until|till|because|so that|so|which|that|when|where|if|while|unless|than|and|or|but|"
    r"to|of|in|on|at|for|with|by|from|as|into|about|after|before)[^,;:.!?]*$", re.I)


_A_PORTION = re.compile(r"\b(?:for each|for every|a time|per|twice|once a|\d+ times)\b", re.I)


def _the_length(answer, asked=frozenset()):
    first = ("", "")
    for clause in _clauses(answer):
        found = _A_LENGTH.search(clause)
        if not found:
            continue
        if _A_PORTION.search(clause) or _A_RATE_LEAD.search(clause[:found.start()]):
            continue
        length, doing = found.group(0).strip(), _the_doing(clause[found.end():])
        if asked and _names_it(clause, asked):
            return length, doing
        if not first[0]:
            first = (length, doing)
    return first


def _names_it(clause, asked):
    words = _stems(clause)
    return bool(words & asked)


def _stems(text):
    out = set()
    for word in re.findall(r"[a-z]{4,}", str(text or "").lower()):
        if word in _STOPPED:
            continue
        for ending in ("ing", "ed", "es", "s"):
            if len(word) > len(ending) + 3 and word.endswith(ending):
                word = word[:-len(ending)]
                break
        out.add(word)
    return out


_STOPPED = frozenset("""
a an the and or but if then so of to in on at for with from by is are was were be been being it
its this that these those i you we they he she them him her your our my me us do does did done
not no as than there here what which who when where how why can could should would will just
one two three keep keeps keeping go going get gets got make makes made say says said
""".split())


def _content(answer):
    return {w for w in re.findall(r"[a-z]{4,}", str(answer or "").lower()) if w not in _STOPPED}


def _about_the_same_thing(one, other):
    return len(_content(one) & _content(other)) >= 2


def _the_advice_length(memory, answers=3, asked=frozenset()):
    said = []
    for turn in reversed(_bot_turns(memory)):
        said.append(turn)
        if len(said) >= answers:
            break
    if not said:
        return "", ""
    length, action = _the_length(said[0], asked)
    if length:
        return length, action
    for older in said[1:]:
        length, action = _the_length(older, asked)
        if length and _about_the_same_thing(older, said[0]):
            return length, action
    return "", ""


def _asked_stems(text):
    return frozenset(_stems(text) - _ASK_WORDS)


_ASK_WORDS = frozenset("""
keep keeps keeping going long longer how should shall could would can do does did i we
much many time times more again this that it thing things
""".split())


def _bot_turns(memory):
    out = []
    for turn in (memory or {}).get("turns") or []:
        if not isinstance(turn, dict):
            continue
        said = str(turn.get("bot") or "").strip()
        if said and not _a_pace_reply(said) and not _a_keep_reply(said):
            out.append(said)
    return out


_KEEP_LEADS = ("Keep it up for {length}", "Stay with it for {length}",
               "Give it {length}")
_KEEP_MARK = ("the answer's own mark for it", "the answer's own length for it",
              "what the answer says to allow")


def _a_keep_reply(answer):
    opening = " ".join(str(answer or "").split())[:60].lower()
    return any(opening.startswith(lead.split("{length}")[0].strip().lower())
               for lead in _KEEP_LEADS)


def the_keep_up_line(text, memory):
    if not KEEP_UP_ASK.search(_clean(text)):
        return False
    answer = _last_answer(memory)
    if not answer or _a_pace_reply(answer) or _a_keep_reply(answer):
        return False
    if not asks_the_keep_up(text, answer):
        return False
    length, _action = _the_advice_length(memory, asked=_asked_stems(text))
    return bool(length)


def _keep_up_reply_for(text, memory):
    if not the_keep_up_line(text, memory):
        return None
    length, action = _the_advice_length(memory, asked=_asked_stems(text))
    if not length:
        return None
    first = "%s - %s" % (pick(_KEEP_LEADS, memory, text).format(length=_as_clause(length)),
                         pick(_KEEP_MARK, memory, text))
    if action:
        return "%s, %s." % (first, _as_clause(action))
    return first + "."


def the_pace_line(text, memory):
    if not PACE_ASK.search(_clean(text)):
        return False
    answer = _last_answer(memory)
    if _a_pace_reply(answer) or not asks_the_pace(text, answer):
        return False
    pace, test, after = _parts(answer)
    return bool(pace) and bool(test or len(pace) > 1 or after)


def reply_for(text, memory):
    if KEEP_UP_ASK.search(_clean(text)):
        return _keep_up_reply_for(text, memory)
    if not PACE_ASK.search(_clean(text)):
        return None
    answer = _last_answer(memory)
    if not answer or _a_pace_reply(answer) or not asks_the_pace(text, answer):
        return None
    pace, test, after = _parts(answer)
    if not pace:
        return None
    said = _clean(text)
    word = "slowly" if "slowly" in said else "fast" if "fast" in said else \
        "soon" if "soon" in said else "quickly"
    lead = pick(_LEADS[word], memory, text)
    first = "%s: %s." % (lead, _as_clause(pace[0]))
    if test:
        opening = _as_clause(test).split()[:1]
        opening = opening[0].lower().strip(",.;:") if opening else ""
        frames = [f for f in _TESTED
                  if opening not in [w.lower().strip(",.;:") for w in f.split("{test}")[0].split()]]
        second = pick(frames or list(_TESTED), memory, text).format(test=_as_clause(test))
    elif len(pace) > 1:
        second = pick(_REST, memory, text).format(rest=_as_clause(pace[1]))
    elif after:
        second = pick(_NEXT, memory, text).format(next=_as_clause(after))
    else:
        return None
    return first + " " + second


def _as_clause(text):
    said = str(text).strip().rstrip(".").strip()
    if said[:2] != "I " and said[:2] != "I'":
        said = said[:1].lower() + said[1:]
    return said
