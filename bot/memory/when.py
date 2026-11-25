import datetime
import re

from .facts import (DAYS, DETERMINERS, FUTURE, MONTHS, a_date_put_right, a_moved_time,
                    the_date_put_right)
from .topics import content, forms

WHEN_ASK = re.compile(
    r"^\s*(?:and |so |but |oh |right |also |ok(?:ay)?[ ,]+)*"
    r"(?:when(?:'s|s| is| are| was| am| do| does| did| will| would)\b"
    r"|what (?:day|date)\b|which day\b)", re.I)

BARE_CALENDAR_ASK = re.compile(
    r"^\W*(?:(?:and|so|but|oh|right|also|ok|okay)\b[\s,]*)?"
    r"what(?:'s|s| is| was)?\s+(?:the\s+)?(?:day|date)"
    r"(?:\s+(?:is\s+it|it\s+is|is\s+that|it|today|now|please|then|already|again))*\W*$", re.I)

WHEN_SAID = re.compile(r"\bwhen did (?:i|we|you)\b[^.?!]*\b(?:say|said|tell|told|mention|mentioned|"
                       r"ask|asked|bring|brought|talk|talks|talked|discuss|discussed|"
                       r"cover|covered)\b|\bwhen (?:was|were) it (?:i|we) (?:said|told)\b",
                       re.I)

WORD = re.compile(r"[a-z0-9']+")

CALENDAR_NOW = re.compile(
    r"^\W*(?:(?:and|so|but|ok|okay|right|oh|also|hi|hey|quick|sorry|excuse me)\W+)*"
    r"what(?:'s|s| is| are| was)?\s+(?:the\s+)?(?:day|date)"
    r"(?:[\s,]*(?:is it|it is|today|now|tonight|tomorrow|this (?:week|morning|evening)|"
    r"right now))*\s*$", re.I)

ASK_THROWS = frozenset("""exactly again then just roughly about long before after tonight due
start starts starting end ends ending say said tell told know""".split())

WHAT_DAY_SAYS = frozenset(("day", "date"))

MONTH_NAMES = "|".join(sorted(MONTHS, key=len, reverse=True))
SHORT_DATE = re.compile(
    r"\b(?:for|in|on|by|until|till|around|from)\s+(?:the\s+)?"
    r"(?:(?:early|mid|late)\s+)?"
    r"(?:" + MONTH_NAMES + r"|"
    + "|".join(sorted(DAYS, key=len, reverse=True)) + r"|"
    r"(?:0?[1-9]|[12]\d|3[01])(?:st|nd|rd|th)?"
    r"(?!\s*(?:k|grand|thousand|hundred|million|billion|quid|pounds?|dollars?|euros?|"
    r"cents?|percent|%|per\b|a\s+(?:week|month|year|day)))"
    r"(?:\s+(?:of\s+)?(?:" + MONTH_NAMES + r"))?)\b"
    r"|\b(?:is|was|it's|its)\s+(?:in\s+|on\s+)?"
    r"(?:" + "|".join(sorted(MONTHS, key=len, reverse=True)) + r")", re.I)

BARE_DAY = re.compile(
    r"\b(?:start|starts|starting|begin|begins|beginning|finish|finishes|finishing|end|ends|"
    r"ending|leave|leaves|leaving|go|goes|going|come|comes|coming|return|returns|returning|"
    r"fly|flies|flying|arrive|arrives|arriving|land|lands|landing|move|moves|moving|"
    r"open|opens|opening|close|closes|closing|visit|visits|visiting|meet|meets|meeting|"
    r"submit|submits|hand|hands|deliver|delivers|book|booked|due|held|happens|happen|"
    r"is|are|was|were|have|has|got)\s+(?:on\s+|this\s+|next\s+)?"
    r"(?:(?!and\b|but\b|because\b|if\b|[.!?])[\w']+\s+){0,3}"
    r"(" + "|".join(sorted(DAYS, key=len, reverse=True)) + r")\b"
    r"(?!\s+(?:is|was|are|were)\b)", re.I)

PAST_WHEN = re.compile(
    r"\b(?:last|back in|this past)\s+(?:(?:early|mid|late)\s+)?"
    r"(?:" + MONTH_NAMES + r"|spring|summer|autumn|winter|year)\b", re.I)

TRIP_WORDS = frozenset("""holiday holidays trip break vacation getaway going go flying fly travel
travelling traveling leaving leave away""".split())
TRIP_LINE = re.compile(r"\b(?:go|going|goes|went|fly|flying|flies|flew|travel\w*|leave|leaving|"
                       r"left|trip|holiday|break|vacation|getaway|visiting|visit|abroad)\b", re.I)
TRIP_BOOKED = re.compile(r"\b(?:tickets?|flights?|ferry|plane|abroad|"
                         r"check(?:ed)?\s*-?\s?in|boarding)\b", re.I)
BOOKING = re.compile(r"\b(?:book(?:ed|ing)|reserv\w*)\b", re.I)
TRIP_BOOKED_ONLY_WITH_A_BOOKING = re.compile(r"\b(?:trains?|coach|coaches|seat|seats|hotel|"
                                             r"room|rooms|table)\b", re.I)


def _is_a_trip_line(said):
    if TRIP_LINE.search(said) or TRIP_BOOKED.search(said):
        return True
    return bool(TRIP_BOOKED_ONLY_WITH_A_BOOKING.search(said) and BOOKING.search(said))


POINTS_BACK = frozenset("""it that this them there then him her those these""".split())
BACK_TURNS = 3

EVENT_NAME = {
    "wedding": ("married", "marry", "wedding"),
    "birthday": ("birthday", "born", "turns"),
    "operation": ("operation", "surgery"),
}


def _names_that_event(word, other):
    for name, says in EVENT_NAME.items():
        if _same(word, name) and any(_same(one, other) for one in says):
            return True
    return False

NOT_A_DATE_TO_GIVE = re.compile(
    r"\b(?:died|dies|dying|dead|death|killed|passed\s+away|passed\s+on|funeral|burial|"
    r"buried|cremation|cremated|put\s+to\s+sleep|euthanis\w*|widow|widowed)\b", re.I)
THEIR_OWN_DEATH = re.compile(
    r"\b(?:kill\s+myself|killing\s+myself|kill\s+me(?!\s+a)|suicide|suicidal|end\s+my\s+(?:own\s+)?"
    r"life|take\s+my\s+(?:own\s+)?life|hang\s+myself|hang\s+myself|overdose|cut\s+myself|"
    r"done\s+with\s+living|better\s+off\s+dead|"
    r"(?:(?:do(?:es)?|did)\s+not|don'?t|dont|didn'?t)\s+want\s+to\s+"
    r"(?:be\s+here|live|carry\s+on|go\s+on)"
    r"(?=\s*(?:$|[.,!?;:]|and\b|any\s?more|anymore|at\s+all|like\s+this|like\s+that|"
    r"for\s+good|for\s+much\s+longer|much\s+longer|any\s+longer|tonight|today|"
    r"this\s+(?:week|month|year|time)|"
    r"(?:in|by|at|before|until|till|after)\s+(?:\d{4}|jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)))|"
    r"want\s+to\s+die|going\s+to\s+die|"
    r"(?:do(?:es)?\s+not|did\s+not|don'?t|dont|didn'?t)\s+want\s+to\s+(?:live|be\s+here)\s+"
    r"(?:forever|for\s+ever|in\s+this\s+world|on\s+this\s+earth))\b", re.I)


NO_DATE_YET = (
    "You haven't told me when — when is it?",
    "No date from you on that one. When is it?",
    "I don't have a date from you for that. When is it?",
)
NOT_A_DATE_ASK = re.compile(r"\b(?:should|ought|best|better|good|safe|easiest|cheapest|likely|"
                            r"worth|advice|tips?|look\w*|search\w*|appl\w*|think\w*|tr(?:y|ying)|"
                            r"plan\w*)\b", re.I)
EVENT_WORD = re.compile(
    r"\b(?:baby|babies|pregnan\w*|birth|scan|job|work|wedding|marri\w*|wed|move|moving|moved|"
    r"flat|house|trip|holiday|honeymoon|exam|exams|test|appointment|interview|operation|surgery|"
    r"course|term|flight|ferry|train|placement|retire\w*|start\w*|begin\w*|due|deadline|"
    r"due\s+date|results?|course)\b", re.I)
WANT_LINE = re.compile(r"\b(?:want|wanna|wanted|would\s+like|hope|hoping|trying|try|thinking\s+of|"
                       r"dream\w*|plan\s+to)\b", re.I)
PLAN_VERB_ASK = re.compile(
    r"^\W*(?:(?:and|so|but|ok|okay|right)\W+)*when(?:'s|s)?\s+(?:do|does|did|will|would|is|are|"
    r"was|were|am)\s+(?:i|we|it|that|this|they|he|she)\s+"
    r"(?:start|starts|begin|begins|finish|end|ends|go|going|leave|leaving|due|happen\w*|arrive\w*|"
    r"back|home|on)\b", re.I)


def asks_what_today_is(text):
    line = " ".join(str(text or "").split()).rstrip("?!. ")
    return bool(CALENDAR_NOW.match(line))


def _more_than_one_day(memory):
    dated = _dated(memory)
    if any(a_date_put_right(said) for said, spans in dated):
        return False
    return len({spans[-1][0] for said, spans in dated if spans}) > 1


def when_answer(text, memory):
    line = str(text or "")
    if CALENDAR_NOW.match(line):
        return None
    if not WHEN_ASK.search(line) or WHEN_SAID.search(line):
        return None
    if BARE_CALENDAR_ASK.match(" ".join(line.split())):
        return None
    words = [word for word in content(line) if word not in ASK_THROWS
             and word not in WHAT_DAY_SAYS]
    if NOT_A_DATE_TO_GIVE.search(line):
        return None
    if words and _points_back(line):
        dated = _dated(memory)
        if dated and a_date_put_right(dated[0][0]) and _said_in_the_last_few_turns(memory, dated[0][0]):
            joined = _a_day_and_a_month(dated[0][1][-1][0], dated[1][1][-1][0]) if len(dated) > 1 else ""
            if joined:
                return _sentence(joined)
        for said, spans in dated[:1]:
            if _said_in_the_last_few_turns(memory, said):
                return _sentence(spans[-1][0])
        return None
    asked = [word for word in words if word not in TRIP_WORDS]
    trip = asked != words
    if not asked:
        said_before = {word for said, spans in _dated(memory) for word in content(said)}
        anchors = [word for word in content(line) if word in said_before]
        if anchors:
            asked, trip = anchors, False
        elif _more_than_one_day(memory):
            return None
    put_right = ""
    for said, spans in _dated(memory):
        if NOT_A_DATE_TO_GIVE.search(said):
            continue
        if a_date_put_right(said):
            put_right = put_right or spans[-1][0]
            continue
        if trip and not _is_a_trip_line(said):
            continue
        when = _time_for(asked, said, spans)
        if when:
            said_date = _a_day_and_a_month(put_right, when) or put_right or when
            if _has_happened(said) and not AN_ASK_IN_THE_PAST.search(line):
                return _was_sentence(said_date)
            return _sentence(said_date)
        if asked and not _names_a_thing(said, spans):
            above = _the_thing_before_the_date(memory, said, asked)
            if above:
                return _sentence(_a_day_and_a_month(put_right, spans[-1][0])
                                 or put_right or spans[-1][0])
        put_right = ""
    return _no_date_yet(asked, line, memory)


ASK_OPENER = re.compile(
    r"^\W*(?:do|does|did|can|could|should|would|will|shall|is|are|was|were|have|has|had|am|"
    r"how|what|when|where|who|which|why|any|anyone)\b", re.I)


def _is_an_ask(line):
    text = str(line or "").strip()
    if not text:
        return False
    return text.endswith("?") or bool(ASK_OPENER.search(text))


def _backs_off(line):
    tokens = re.findall(r"[a-z']+", str(line or "").lower())
    while tokens and tokens[-1] in ASK_THROWS:
        tokens.pop()
    return bool(tokens) and tokens[-1] in POINTS_BACK


def _no_date_yet(asked, line, memory):
    if not isinstance(memory, dict) or NOT_A_DATE_ASK.search(line):
        return None
    turns = [" ".join(str(turn.get("user") or "").split())
             for turn in (memory.get("turns") or []) if isinstance(turn, dict)]
    plans = [str(p) for p in ((memory.get("user") or {}).get("plans") or []) if isinstance(p, str)]
    latest = (memory.get("user") or {}).get("plan")
    if isinstance(latest, str):
        plans.append(latest)
    recent = [said for said in turns if said][-BACK_TURNS:]
    for said in recent + list(reversed(plans)):
        if not said or NOT_A_DATE_TO_GIVE.search(said):
            continue
        if _is_an_ask(said):
            continue
        if (list(FUTURE.finditer(said)) or list(SHORT_DATE.finditer(said))):
            return None
        if asked:
            theirs = [word for word in content(said) if word not in ASK_THROWS]
            if not any(_same(word, other) for word in asked for other in theirs):
                continue
        else:
            if not (_backs_off(line) or PLAN_VERB_ASK.search(line)):
                return None
            if not EVENT_WORD.search(said) or WANT_LINE.search(said):
                continue
        return NO_DATE_YET[len(turns) % len(NO_DATE_YET)]
    return None


def _a_day_and_a_month(day, month):
    the_day = re.search(r"\b\d{1,2}(?:st|nd|rd|th)\b", str(day or ""))
    a_month = next((word for word in re.findall(r"[A-Za-z]+", str(month or ""))
                    if word.lower() in MONTHS), "")
    if not (the_day and a_month):
        return ""
    return "on the %s of %s" % (the_day.group(0), a_month.lower())


def _points_back(line):
    tokens = re.findall(r"[a-z']+", str(line or "").lower())
    return bool(tokens) and tokens[-1] in POINTS_BACK


def the_plan(memory):
    known = (memory.get("user") or {}) if isinstance(memory, dict) else {}
    if not isinstance(known, dict):
        return None
    plan = known.get("plan")
    if isinstance(plan, str) and plan.strip():
        return " ".join(plan.split())
    plans = [p for p in (known.get("plans") or []) if isinstance(p, str) and p.strip()]
    return " ".join(plans[-1].split()) if plans else None


def _said_in_the_last_few_turns(memory, said):
    turns = [" ".join(str(turn.get("user") or "").split())
             for turn in (memory.get("turns") or []) if isinstance(turn, dict)]
    key = " ".join(str(said or "").split())
    return key in turns[-BACK_TURNS:]


def _names_a_thing(text, spans):
    said = str(text or "")
    for when, _start in sorted(spans, key=lambda span: -span[1]):
        said = said.replace(when, " ", 1)
    left = [word for word in content(said) if word not in NOT_A_THING]
    return bool(left)


NOT_A_THING = frozenset("""
about actually also because been before day days going coming sorry wrong now still yet again
think thought said say told tell really surely maybe right okay ok well thanks thank got get
have has had was were is are be been being turn turns
""".split())


def _the_thing_before_the_date(memory, said, asked):
    turns = [" ".join(str(turn.get("user") or "").split())
             for turn in (memory.get("turns") or []) if isinstance(turn, dict)]
    key = " ".join(str(said or "").split())
    if key in turns:
        cut = len(turns) - 1 - turns[::-1].index(key)
    else:
        cut = len(turns)
    for line in reversed(turns[max(0, cut - BACK_TURNS * 2):cut]):
        if not line or line == key:
            continue
        spans = [found.group(0) for found in FUTURE.finditer(line)]
        spans += [found.group(0) for found in SHORT_DATE.finditer(line)]
        if a_date_put_right(line):
            continue
        if not _names_a_thing(line, [(span, 0) for span in spans]):
            continue
        if spans:
            break
        if any(_same(word, found) for word in asked for found in WORD.findall(line)):
            return line
    return ""


THE_MEAN_NOTE = re.compile(r"\s*\(\s*(?:i\s+|sorry,?\s+i\s+)?mean\s+([^)]*)\)\s*$", re.I)
JOINED_TO_A_DATE = re.compile(
    r"(?i)\s*(?:(?:for|is|was|it's|its|'s|in|on|at|by|next|this|last)\s+)*")


def _the_line_put_right(memory):
    record = (memory or {}).get("topic") if isinstance(memory, dict) else None
    text = " ".join(str(record.get("text") or "").split()) if isinstance(record, dict) else ""
    note = THE_MEAN_NOTE.search(text)
    if not note:
        return "", ""
    meant = " ".join(note.group(1).split()).strip(" .,")
    line = text[:note.start()].strip(" ,;")
    if not line or not meant:
        return "", ""
    if not a_moved_time(meant):
        return "", ""
    spans = list(FUTURE.finditer(line)) + list(SHORT_DATE.finditer(line))
    if not spans:
        return "", ""
    last = max(spans, key=lambda found: (found.start(), len(found.group(0))))
    joined = JOINED_TO_A_DATE.match(last.group(0)).group(0)
    swapped = line[:last.start()] + joined + meant + line[last.end():]
    old = JOINED_TO_A_DATE.sub("", last.group(0), count=1)
    return " ".join(swapped.split()), _plain(old)


def _dated(memory):
    out, seen = [], set()
    known = (memory.get("user") or {}) if isinstance(memory, dict) else {}
    plans = [p for p in (known.get("plans") or []) if isinstance(p, str)]
    latest = known.get("plan")
    if isinstance(latest, str) and latest not in plans:
        plans.append(latest)
    typed = [str(turn.get("user") or "") for turn in reversed(memory.get("turns") or [])
             if isinstance(turn, dict)]
    lines = typed
    fixed_sentence, replaced = _put_right(memory)
    if not fixed_sentence:
        fixed_sentence, replaced = _the_line_put_right(memory)
    if fixed_sentence:
        lines = [fixed_sentence] + lines
    theirs = {" ".join(line.split()).lower() for line in typed}
    for said in lines + list(reversed(plans)):
        said = " ".join(said.split())
        key = said.lower()
        if not said or key in seen:
            continue
        spans, places = [], set()
        for found in FUTURE.finditer(said):
            spans.append((_lead(_with_the_month_after(said, found)), found.start()))
            places.add(found.start())
        for found in SHORT_DATE.finditer(said):
            if found.start() in places:
                continue
            spans.append((_lead(found.group(0)), found.start()))
            places.add(found.start())
        for found in PAST_WHEN.finditer(said):
            if found.start() in places:
                continue
            spans.append((_lead(found.group(0)), found.start()))
            places.add(found.start())
        for found in BARE_DAY.finditer(said):
            if found.start(1) in places:
                continue
            spans.append((_lead("on " + found.group(1)), found.start(1)))
            places.add(found.start(1))
        if not spans and a_date_put_right(said):
            spans.append((_a_date_said(the_date_put_right(said)), 0))
        spans.sort(key=lambda span: span[1])
        if replaced and key in theirs:
            spans = [span for span in spans if replaced not in _plain(span[0]).split()]
        if not spans:
            continue
        seen.add(key)
        out.append((said, spans))
    return out


LEAD = ("for", "is", "was", "it's", "its", "'s")


def _lead(found):
    text = " ".join(str(found).split()).strip(" ,;.")
    words = text.split()
    if len(words) > 1 and words[0].lower() in LEAD:
        rest = " ".join(words[1:])
        if rest.lower().startswith(("in ", "on ", "at ", "by ", "next ", "this ", "last ")):
            return rest
        first = re.split(r"[\s,]", rest)[0].lower()
        if first in MONTHS or first in ("early", "mid", "late"):
            return "in " + rest
        return "on " + rest
    return text


def _time_for(asked, said, spans):
    if not asked:
        return spans[-1][0]
    hits, seen = [], set()
    for found in WORD.finditer(said):
        for word in asked:
            if word not in seen and (_same(word, found.group(0))
                                     or _names_that_event(word, found.group(0))):
                seen.add(word)
                hits.append(found.start())
    if len(seen) < len(asked) and (len(asked) < 3 or len(seen) < len(asked) - 1):
        return None
    best = None
    for when, start in spans:
        after = [start - hit for hit in hits if start >= hit]
        score = (min(after), 0) if after else (min(abs(start - hit) for hit in hits), 1)
        if best is None or score < best[0]:
            best = (score, when)
    return best[1]


MONTH_AFTER_THE_DAY = re.compile(
    r"^\s+(?:of\s+)?(?:" + "|".join(sorted(MONTHS, key=len, reverse=True)) + r")\b", re.I)
A_THING_NAMED = re.compile(r"\b(?:my|our|your|his|her|their|the|this|that|these|those|a|an)\s+"
                           r"([a-z][a-z'-]{1,19})", re.I)


def _with_the_month_after(said, found):
    text = found.group(0)
    if not re.search(r"\d{1,2}(?:st|nd|rd|th)$", text.strip()):
        return text
    after = MONTH_AFTER_THE_DAY.match(said[found.end():] or "")
    if not after:
        return text
    return text + after.group(0)


def _names_a_thing_of_its_own(line, said):
    found = UNTIL_COUNTDOWN.search(line)
    if not found:
        return False
    body = line[found.end():]
    if _POINTS_AT_IT.search(body):
        return False
    dated = set(WORD.findall(str(said or "").lower()))
    if (found.group(1) or "").lower() in UNTIL_NAMES_THE_EVENT:
        words = WORD.findall(body.lower())
        for index, word in enumerate(words):
            if word in UNTIL_THROWS or word in ASK_THROWS:
                continue
            if word in dated or any(_same(word, held) for held in dated):
                continue
            behind = words[index - 1] if index else ""
            if behind in DETERMINERS and not _a_doing_word(words[index + 1:]):
                continue
            return True
    for match in A_THING_NAMED.finditer(body):
        thing = match.group(1).lower()
        if thing in dated or any(_same(thing, word) for word in dated):
            continue
        if thing in UNTIL_THROWS:
            continue
        return True
    return False


def _a_doing_word(words):
    return any(word.endswith(("ed", "ing")) or (len(word) > 3 and word.endswith("s"))
               for word in words if word not in ("is", "are", "was", "were", "be", "been"))


def _plain(when):
    words = [word for word in str(when or "").lower().split()]
    while words and words[0] in LEAD:
        words.pop(0)
    return " ".join(words)


def _put_right(memory):
    fixed = (memory or {}).get("correction") if isinstance(memory, dict) else None
    if not isinstance(fixed, dict):
        return "", ""
    sentence = " ".join(str(fixed.get("sentence") or "").split())
    old = _plain(fixed.get("from"))
    if not sentence or not old:
        return "", ""
    found = list(FUTURE.finditer(sentence)) + list(SHORT_DATE.finditer(sentence))
    if not found:
        return "", ""
    return sentence, old


SAME_THING = {
    "wedding": frozenset("married marry marrying wed weddings".split()),
    "married": frozenset("wedding weddings marry marrying wed".split()),
    "marry": frozenset("wedding weddings married marrying".split()),
    "baby": frozenset("pregnant pregnancy birth born due babies".split()),
    "babies": frozenset("pregnant pregnancy birth born due baby".split()),
    "pregnant": frozenset("baby babies pregnancy birth due".split()),
    "pregnancy": frozenset("baby babies pregnant birth due".split()),
    "job": frozenset("work working career".split()),
    "work": frozenset("job career".split()),
}
def _a_date_said(value):
    phrase = " ".join(str(value or "").split()).strip(" .,!?")
    words = phrase.lower().split()
    if not words:
        return ""
    if len(words) >= 2 and re.fullmatch(r"\d{1,2}(?:st|nd|rd|th)?", words[0]) and (
            words[1] in MONTHS or (len(words) > 2 and words[1] == "of")):
        rest = " ".join(words[1:]) if words[1] in MONTHS else " ".join(words[2:])
        return "on the " + words[0] + " of " + rest
    if words[0] in MONTHS or words[0] in ("early", "mid", "late"):
        return "in " + phrase
    return "on " + phrase


def _same(word, other):
    word, other = word.lower(), other.lower()
    if word == other or forms(word) & forms(other):
        return True
    if _root(word) == _root(other):
        return True
    if _a_plural_stem(word) == other or word == _a_plural_stem(other):
        return True
    return other in SAME_THING.get(word, ()) or word in SAME_THING.get(other, ())


def _root(word):
    for ending in ("ing", "ed"):
        if word.endswith(ending) and len(word) - len(ending) >= 2:
            return word[:-len(ending)]
    return word


NOT_A_PLURAL = ("ss", "us", "is", "as", "ws")


def _a_plural_stem(word):
    if len(word) > 3 and word.endswith("s") and not word.endswith(NOT_A_PLURAL):
        return word[:-1]
    return ""


ASKS_WHERE = re.compile(r"\bwhere(?:abouts)?\b", re.I)
ASKS_WHEN = re.compile(r"\bwhen\b|\b(?:which|what) (?:month|day|week|date|time of year)\b", re.I)
ASKS_THE_MONTH = re.compile(r"\b(?:which|what) month\b", re.I)
ASKS_THE_DAY = re.compile(r"\b(?:which|what) (?:day|week)\b", re.I)
NO_PLACE = frozenset("""away out off back home there somewhere anywhere everywhere now soon
later today tomorrow tonight weekend week month year again then bed sleep work""".split())
A_VERB = frozenset("""move moving go going went fly flying drive driving travel travelling
traveling visit visiting start starting begin beginning take taking run running play playing work
working book booking sort sorting pack packing have having get getting see seeing meet meeting
buy buying sell selling pay paying do doing make making""".split())
GOES_TO = re.compile(
    r"\b(?:go|goes|going|went|gone|off|head|headed|heading|fly|flying|flies|flew|flown|move|moves|"
    r"moving|moved|travel|travelling|traveling|drive|driving|drove|back|booked|book|trip|tour|"
    r"visit|visiting|holiday|vacation|head(?:ing|ed)?|away)\b[^.;!?]*?\b(?:to|towards)\s+"
    r"([^,.;!?]+)$", re.I)
PLACE_PREP = re.compile(r"\b(?:to|towards|via)\s+(\S.*)$", re.I)
TRAILING_JOINER = re.compile(
    r"(?:[\s,]+\b(?:in|on|at|for|by|from|to|and|around|during|early|mid|late|the|of)\b)+$", re.I)


def the_part_asked(plan, low, line=None, is_a_place=None):
    text = " ".join(str(plan or "").split())
    ask = str(low or "")
    if not text or not ask:
        return ""
    spans = _the_dates_in(text)
    if ASKS_WHERE.search(ask):
        place = _the_place(text, line, is_a_place)
        if not place:
            return ""
        return _a_name(place) + "."
    if ASKS_WHEN.search(ask):
        when = _the_date_asked(ask, [said for _, _, said in spans])
        return _sentence(when) if when else ""
    return ""


def _the_place(plan, line, is_a_place=None):
    said = " ".join(str(line or "").split())
    if said:
        found = GOES_TO.search(said)
        if found:
            place = _without_the_date(found.group(1))
            place = TRAILING_JOINER.sub("", place).strip(" .,;:!?-")
            if _names_a_place(place):
                return place
    place = _without_the_date(plan)
    place = TRAILING_JOINER.sub("", place).strip(" .,;:!?-")
    cut = PLACE_PREP.search(place)
    if cut:
        place = cut.group(1).strip(" .,;:!?-")
    if not _names_a_place(place):
        return ""
    if is_a_place is not None and not is_a_place(place):
        return ""
    return place


def _a_name(place):
    small = frozenset("the a an of and in on at for to".split())
    words = place.split()
    title = len(words) > 1 and not any(word.lower() in small for word in words)
    out = []
    for turn, word in enumerate(words):
        if word[:1].isalpha() and (turn == 0 or title):
            word = word[:1].upper() + word[1:]
        out.append(word)
    return " ".join(out)


def _without_the_date(text):
    out = str(text or "")
    for start, end, _ in reversed(_the_dates_in(out)):
        out = out[:start] + " " + out[end:]
    return " ".join(out.split())


def _names_a_place(place):
    if not place or not re.search(r"[a-z]", place, re.I):
        return False
    plain = place.lower().strip(" .,;:!?-")
    if plain in NO_PLACE:
        return False
    words = re.findall(r"[a-z']+", plain)
    if not words or set(words) & A_VERB:
        return False
    return not re.search(r"\b(?:is|are|was|were|am|and|with|for|about)\b", plain)


def _the_dates_in(text):
    out = []
    for pattern in (FUTURE, SHORT_DATE, PAST_WHEN):
        for found in pattern.finditer(text):
            if any(found.start() < end and start < found.end() for start, end, _ in out):
                continue
            out.append((found.start(), found.end(), found.group(0)))
    out.sort()
    return out


def _the_date_asked(ask, dates):
    for when in reversed(dates):
        plain = _plain(when).lower()
        words = set(plain.split())
        if ASKS_THE_MONTH.search(ask) and not words & MONTHS:
            continue
        if ASKS_THE_DAY.search(ask) and not (words & DAYS or re.search(r"\d", plain)):
            continue
        return when
    return ""


SAYS_IT_IS_COMING = re.compile(
    r"\b(?:booked|reserved|arranged|scheduled|organi[sz]ed|planned)\b"
    r"|\b(?:got|bought|picked\s+up)\b[^.!?]{0,20}?\b(?:tickets?|flights?)\b", re.I)


GOING_ON = re.compile(r"\b(?:i|we|they|he|she)(?:'?m|'?re|'?s)?\s+[a-z]+ing\b", re.I)
WAS_GOING_ON = re.compile(r"\b(?:was|were|had|been)\b", re.I)


ALREADY_DONE_ASK = re.compile(
    r"\b(?:did|have|has|do)\s+(?:i|we|that|it)\b[^.?!]*?\b(?:already|yet|happen(?:ed)?|"
    r"been|go|gone|going|did)\b|\b(?:already|yet)\s+(?:go|gone|been|happen(?:ed)?)\b", re.I)


SAYS_IT_AGAIN = re.compile(
    r"\b(?:(?:where|what|when|why|who|how\s+often|how\s+many\s+times)\s+)?"
    r"did\s+(?:i|we)\s+(?:ever\s+)?(?:say|tell\s+you|mention)\b", re.I)
HOW_OFTEN = re.compile(r"\bhow\s+(?:often|many\s+times)\b", re.I)


def already_answer(text, memory):
    line = str(text or "")
    if not ALREADY_DONE_ASK.search(line) or WHEN_ASK.search(line):
        return None
    if SAYS_IT_AGAIN.search(line) or HOW_OFTEN.search(line):
        return None
    if NOT_A_DATE_TO_GIVE.search(line):
        return None
    words = [word for word in content(line) if word not in ASK_THROWS]
    asked = [word for word in words if word not in TRIP_WORDS]
    for said, spans in _dated(memory)[:2]:
        if NOT_A_DATE_TO_GIVE.search(said) or not _said_in_the_last_few_turns(memory, said):
            continue
        when = (_time_for(asked, said, spans) if asked else "") or (spans[-1][0] if spans else "")
        if not when:
            continue
        plain = _plain(when).split()
        if _has_happened(said):
            if plain and (plain[0] in MONTHS or plain[0] in DAYS):
                return "Yes - that was in " + _sentence(when)
            said_when = _sentence(when)
            return "Yes - that was " + said_when[:1].lower() + said_when[1:]
        if plain and (plain[0] in MONTHS or plain[0] in DAYS):
            return "No - that's in " + _sentence(when)
        said_when = _sentence(when)
        return "No - that's " + said_when[:1].lower() + said_when[1:]
    return None


AN_ASK_IN_THE_PAST = re.compile(r"\b(?:did|was|were|had|have\s+i|has\s+it)\b", re.I)


def _has_happened(said):
    said = str(said or "")
    if SAYS_IT_IS_COMING.search(said):
        return False
    if GOING_ON.search(said) and not WAS_GOING_ON.search(said):
        return False
    return _said_in_the_past(said)


def _was_sentence(when):
    plain = _plain(when).split()
    if plain and (plain[0] in MONTHS or plain[0] in DAYS):
        return "That was in " + _sentence(when)
    said = _sentence(when)
    return "That was " + said[:1].lower() + said[1:]


def _sentence(when):
    out = []
    for word in when.split():
        low = word.lower().strip(",;:")
        if low in MONTHS or low in DAYS:
            word = word[:1].upper() + word[1:]
        out.append(word)
    said = " ".join(out).rstrip(" .")
    return said[:1].upper() + said[1:] + "."


AN_INTERVAL_AHEAD = re.compile(
    r"\bin\s+(?P<n>\d+|a|an|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|"
    r"couple\s+of|a\s+couple\s+of|a\s+few|few|several)\s+"
    r"(?P<unit>days?|nights?|weeks?|fortnight|fortnights?|months?|years?)\b", re.I)

INTERVAL_JOINERS = frozenset("""is are was were will be gets get got has have had and so but
  only just now then again roughly about around nearly maybe probably ideally hopefully""".split())


def _the_interval_it_means(line, memory):
    said_lines = [_said_before_now(memory, turn) for turn in (memory.get("turns") or [])[-BACK_TURNS:]]
    said_lines = [said for said in said_lines if said]
    if not said_lines:
        return ""
    asked = [word for word in content(line) if word not in ASK_THROWS and word not in UNTIL_THROWS]
    named = [word for word in asked if word not in TRIP_WORDS]
    points_back = _points_back(line) or not asked
    for said in reversed(said_lines):
        found = AN_INTERVAL_AHEAD.search(said)
        if not found:
            continue
        if found.group("unit").lower().endswith(("day", "days")) and re.search(
                r"\b(?:ago|since)\b", said, re.I):
            continue
        if not points_back and named:
            line_words = set(content(said))
            if not any(_same(word, other) for word in named for other in line_words):
                continue
        length = " ".join(found.group(0).split()[1:])
        return f"You said {length}, so a little less than that by now."
    return ""


def _said_before_now(memory, turn):
    said = turn.get("user") if isinstance(turn, dict) else None
    return " ".join(said.split()) if isinstance(said, str) else ""


UNTIL_A_LEARNING = re.compile(
    r"\b(?:till|until|til)\s+i\s+(?:know|hear|find\s+out|learn|s\s*(?:out|back)|"
    r"get\s+(?:the\s+)?(?:results?|answer|news))", re.I)
UNTIL_ASK = re.compile(
    r"\bhow\s+(?:long|soon|far|many\s+(?:days?|weeks?|months?|nights?))\b"
    r"[^.?!]*?(?:\b(?:till|til|until|to\s+go|left|away|off|have\s+i\s+got|"
    r"do\s+(?:i|we)\s+have|does\s+that\s+leave|ago|since)\b"
    r"|\b(?:is|was|are)\s+(?:that|it|this)\b)", re.I)
AGO_ASK = re.compile(r"\b(?:ago|since|back\s+was|has\s+it\s+been)\b", re.I)
SAID_IN_THE_PAST = re.compile(
    r"\b(?:had|was|were|went|did|been|got|took|made|bought|brought|sold|lost|met|left|saw|"
    r"said|told|felt|broke|broke\s+up|came|died|kept|paid|ran|sat|stood|wrote|spoke|"
    r"\w+ed)\b", re.I)
NOT_IN_THE_PAST = re.compile(
    r"\b(?:will|going\s+to|next|upcoming|tomorrow|have|has|is|are|am)\b|'(?:re|m)\b", re.I)


def _said_in_the_past(line):
    said = str(line or "")
    if not said:
        return False
    return bool(SAID_IN_THE_PAST.search(said)) and not NOT_IN_THE_PAST.search(said)


UNTIL_COUNTDOWN = re.compile(r"\b(till|til|until|to\s+go|have\s+i\s+got|do\s+(?:i|we)\s+have)\b",
                             re.I)
UNTIL_NAMES_THE_EVENT = frozenset(("till", "til", "until"))
BARE_UNIT_ASK = re.compile(
    r"^\W*(?:(?:and|but|so|ok|okay|right|then|now|well|yeah)\W+)*"
    r"how\s+many\s+(?:days?|weeks?|months?|nights?)\b"
    r"(?:\W+(?:have\s+i\s+got|is\s+that|to\s+go|left|away|off|now|then|again))*\W*$", re.I)


A_LENGTH_IN_THE_LINE = re.compile(
    r"\bfor\s+(?:\d+|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|a|an|"
    r"a\s+couple|couple|few|several)\s+(?:days?|nights?|weeks?|months?|hours?)\b", re.I)
A_COUNT_TAIL = re.compile(
    r"\b(?:have\s+i\s+got|is\s+that|to\s+go|left|away|off|till|til|until)\b"
    r"|\bhow\s+(?:long|soon|far)\b", re.I)


A_TRIP_SAID = frozenset("""trip vacation honeymoon""".split())
A_GOING = frozenset("""going off flying travelling traveling heading driving""".split())
NOT_A_PLACE = frozenset("""be get go do try have see make take start stop need leave work bed school
    bed sleep the a an my our your their""".split())


def _a_trip_is_named(dated):
    words = re.findall(r"[a-z']+", " ".join(str(dated or "").lower().split()))
    if any(word in A_TRIP_SAID for word in words):
        return True
    for place, word in enumerate(words):
        if word in A_GOING and place + 2 < len(words) and words[place + 1] == "to":
            if words[place + 2] not in NOT_A_PLACE:
                return True
    return False


def _a_bare_unit_ask_wants_a_length(line, dated):
    said = str(line or "")
    if A_COUNT_TAIL.search(said):
        return False
    dated = str(dated or "")
    if A_LENGTH_IN_THE_LINE.search(dated):
        return True
    if not re.search(r"\bdays?\b", said):
        return False
    day, kind = _the_day(dated)
    if day is not None and kind != "month":
        return False
    return _a_trip_is_named(dated)


def until_ask_matches(line, again=None):
    if again is None:
        again = BARE_UNIT_ASK.match(str(line or ""))
    return bool(UNTIL_ASK.search(line) or again)


UNTIL_THROWS = frozenset("""how long soon far many much day days week weeks month months night
nights till til until to go going left away off have got do does did i we you it that this then
them there is was are be time left ago since""".split())

MONTH_NUMBER = {"january": 1, "february": 2, "march": 3, "april": 4, "may": 5, "june": 6,
                "july": 7, "august": 8, "september": 9, "october": 10, "november": 11,
                "december": 12}
MONTH_NAME = {number: name.capitalize() for name, number in MONTH_NUMBER.items()}
WEEKDAY_NUMBER = {"monday": 0, "tuesday": 1, "wednesday": 2, "thursday": 3, "friday": 4,
                  "saturday": 5, "sunday": 6}
WEEKDAY_NAME = {number: name.capitalize() for name, number in WEEKDAY_NUMBER.items()}


def _today():
    return datetime.date.today()


def until_answer(text, memory):
    line = str(text or "")
    again = BARE_UNIT_ASK.match(line)
    if not until_ask_matches(line, again) or WHEN_SAID.search(line):
        return None
    if NOT_A_DATE_TO_GIVE.search(line) or THEIR_OWN_DEATH.search(line):
        return None
    if UNTIL_A_LEARNING.search(line):
        return None
    when, dated = _the_date_it_means("how long until that" if again else line, memory)
    if not when:
        return _the_interval_it_means(line, memory) or None
    if again and _a_bare_unit_ask_wants_a_length(line, dated):
        return None
    if AN_INTERVAL_AHEAD.search(when):
        return _the_interval_it_means(line, memory) or None
    month = ""
    if _a_day_but_no_month(when):
        month = _the_month_in_play(when, memory)
    day, kind = _the_day((when + " " + month) if month else when)
    if day is None:
        return None
    if _said_in_the_past(dated):
        if not AGO_ASK.search(line):
            return None
        return _how_long_ago(day, kind, line)
    if AGO_ASK.search(line):
        return None
    return _how_long(day, kind, line)


def _the_date_it_means(line, memory):
    words = [word for word in content(line) if word not in ASK_THROWS and word not in UNTIL_THROWS]
    if not words or _points_back(line):
        return _the_newest_date(memory)
    asked = [word for word in words if word not in TRIP_WORDS]
    trip = asked != words
    for said, spans in _dated(memory):
        if NOT_A_DATE_TO_GIVE.search(said) or THEIR_OWN_DEATH.search(said):
            continue
        if trip and not _is_a_trip_line(said):
            continue
        when = _time_for(asked, said, spans)
        if when:
            return when, said
    if UNTIL_COUNTDOWN.search(line) and not NOT_A_DATE_ASK.search(line):
        newest, said = _the_newest_date(memory)
        if newest and _names_a_thing_of_its_own(line, said):
            return None, ""
        return newest, said
    return None, ""


def _the_newest_date(memory):
    fixed, _ = _put_right(memory)
    fixed = " ".join(fixed.split()) if fixed else ""
    for said, spans in _dated(memory):
        if NOT_A_DATE_TO_GIVE.search(said) or THEIR_OWN_DEATH.search(said):
            continue
        if _said_in_the_last_few_turns(memory, said) or (fixed and said == fixed):
            return spans[-1][0], said
        return None, ""
    return None, ""


def _a_day_but_no_month(when):
    words = _plain(when).replace(",", " ").split()
    if not words:
        return False
    if any(word in MONTH_NUMBER or word in WEEKDAY_NUMBER for word in words):
        return False
    if any(word in ("today", "tomorrow", "tonight", "weekend", "month", "week", "year")
           for word in words):
        return False
    return any(re.fullmatch(r"\d{1,2}(?:st|nd|rd|th)?", word) for word in words)


def _the_month_in_play(when, memory):
    month = ""
    for said, spans in _dated(memory):
        if not _said_in_the_last_few_turns(memory, said):
            break
        for span in spans:
            words = _plain(span[0]).replace(",", " ").split()
            if any(word in MONTH_NUMBER for word in words):
                named = [word for word in words if word in MONTH_NUMBER][-1]
                if _plain(span[0]).strip() != _plain(when).strip():
                    return named
                month = month or ""
    return month


A_DATE_WORD = (frozenset(MONTH_NUMBER) | frozenset(WEEKDAY_NUMBER)
               | frozenset(("early", "mid", "late", "end", "ends", "ending", "next", "this",
                            "month", "week", "the", "of", "in", "on", "at", "by", "start",
                            "beginning", "weekend", "a", "an", "for", "from", "to", "until",
                            "till", "around", "about")))
DAY_NUMBER = re.compile(r"^\d{1,2}(?:st|nd|rd|th)?$")

A_DATE_ITSELF = (frozenset(MONTH_NUMBER) | frozenset(WEEKDAY_NUMBER)
                 | frozenset(("early", "mid", "late", "end", "ends", "ending", "next", "this",
                              "month", "week")))
FILLER = frozenset(("the", "of", "in", "on", "at", "by", "a", "an", "for", "from", "to",
                    "until", "till", "around", "about"))


def _a_day_number(word):
    return bool(DAY_NUMBER.match(word))


def _the_day(when, today=None):
    today = today or _today()
    words = [word for word in _plain(when).replace(",", " ").split() if word]
    month = day = weekday = None
    early = has_end = has_next = has_this = has_month = has_week = False
    dated = False
    anchored = any(word in MONTH_NUMBER or word in WEEKDAY_NUMBER for word in words)
    for index, word in enumerate(words):
        if not dated:
            started = word in A_DATE_ITSELF
            if not started and _a_day_number(word):
                started = anchored or not [word for word in words[:index] if word not in FILLER]
            if not started:
                continue
        dated = True
        if word in MONTH_NUMBER:
            month = MONTH_NUMBER[word]
        elif word in WEEKDAY_NUMBER:
            weekday = WEEKDAY_NUMBER[word]
        elif word in ("early", "mid", "late"):
            early = True
            day = {"early": 1, "mid": 15, "late": 25}[word]
        elif word in ("end", "ends", "ending"):
            has_end = True
        elif word == "next":
            has_next = True
        elif word == "this":
            has_this = True
        elif word == "month":
            has_month = True
        elif word == "week":
            has_week = True
        elif re.fullmatch(r"\d{1,2}(?:st|nd|rd|th)?", word):
            day = int(re.match(r"\d{1,2}", word).group(0))
        elif word in ("the", "of", "in", "on", "at", "by", "start", "beginning", "weekend",
                      "a", "an", "for", "from", "to", "until", "till", "around", "about"):
            continue
        else:
            return None, None
    if has_month and has_next:
        return _add_months(today.replace(day=1), 1), "month"
    if has_month and has_this:
        return today.replace(day=1), "month"
    if has_end and day is None:
        if month is not None:
            return _last_day(_a_year_for(today, month, 1)), "end"
        if has_next:
            return _last_day(_add_months(today.replace(day=1), 1)), "end"
        return _last_day(today.replace(day=1)), "end"
    if has_week and has_next:
        return today + datetime.timedelta(days=7), "week"
    if month is not None:
        when_day = _a_year_for(today, month, day)
        return when_day, ("month" if day is None or early else "date")
    if weekday is not None:
        ahead = (weekday - today.weekday()) % 7 or 7
        return today + datetime.timedelta(days=ahead), "date"
    if day is not None:
        upcoming, kind = _this_month_or_next(today, day)
        return upcoming, ("month" if early else kind)
    return None, None


def _this_month_or_next(today, day):
    try:
        found = today.replace(day=day)
    except ValueError:
        return _a_year_for(today, today.month + 1, day), "date"
    if found >= today:
        return found, "date"
    return _a_year_for(today, today.month + 1, day), "date"


def _a_year_for(today, month, day):
    while month > 12:
        month -= 12
        today = today.replace(year=today.year + 1)
    day = day or 1
    for year in (today.year, today.year + 1):
        try:
            found = datetime.date(year, month, min(day, _days_in(year, month)))
        except ValueError:
            continue
        if found >= today:
            return found
    return datetime.date(today.year + 1, month, 1)


def _days_in(year, month):
    if month == 12:
        return 31
    return (datetime.date(year, month + 1, 1) - datetime.date(year, month, 1)).days


def _last_day(first_of_month):
    return first_of_month.replace(day=_days_in(first_of_month.year, first_of_month.month))


def _add_months(day, months):
    month = day.month + months
    year = day.year
    while month > 12:
        month -= 12
        year += 1
    return datetime.date(year, month, 1)


def _how_long(day, kind, line):
    today = _today()
    days = (day - today).days
    if days < 0:
        return None
    if days == 0:
        return "That's today."
    if days == 1:
        return "That's tomorrow."
    asked = str(line or "").lower()
    named = ""
    if re.search(r"\bweeks?\b", asked):
        named = unit = "week"
    elif re.search(r"\bdays?\b", asked):
        named = unit = "day"
    elif re.search(r"\bmonths?\b", asked):
        named = unit = "month"
    elif days <= 14:
        unit = "day"
    elif days <= 84:
        unit = "week"
    else:
        unit = "month"
    if unit == "day":
        head = "That's %d days away" % days
    elif unit == "week":
        weeks = int(round(days / 7.0))
        if weeks <= 1:
            head = "That's just over a week away"
        elif named == "week" or weeks <= 30:
            head = "That's about %d weeks away" % weeks
        else:
            unit = "month"
    if unit == "month":
        months = int(round(days / 30.44))
        head = "That's about a month away" if months <= 1 else "That's about %d months away" % months
    said = _the_day_said(day, kind)
    return head + " - " + said + "." if said else head + "."


def _how_long_ago(day, kind, line):
    today = _today()
    past = _a_day_in_the_past(day, today)
    if past is None:
        return None
    days = (today - past).days
    if days <= 0:
        return None
    asked = str(line or "").lower()
    if re.search(r"\bweeks?\b", asked):
        unit = "week"
    elif re.search(r"\bdays?\b", asked):
        unit = "day"
    elif re.search(r"\bmonths?\b", asked):
        unit = "month"
    elif days <= 14:
        unit = "day"
    elif days <= 84:
        unit = "week"
    else:
        unit = "month"
    if unit == "day":
        head = "That was %d days ago" % days
    elif unit == "week":
        weeks = int(round(days / 7.0))
        head = ("That was just over a week ago" if weeks <= 1
                else "That was about %d weeks ago" % weeks)
    else:
        months = int(round(days / 30.44))
        head = "That was about a month ago" if months <= 1 else "That was about %d months ago" % months
    if kind == "month":
        said = "in " + MONTH_NAME[past.month]
    elif kind == "end":
        said = "at the end of " + MONTH_NAME[past.month]
    else:
        said = _the_day_said(past, kind)
    return head + " - " + said + "." if said else head + "."


def _a_day_in_the_past(day, today):
    month, number = day.month, day.day
    for year in (day.year - 1, day.year - 2, day.year - 3):
        try:
            found = datetime.date(year, month, min(number, _days_in(year, month)))
        except ValueError:
            continue
        if found <= today:
            return found
    return None


def _the_day_said(day, kind):
    month = MONTH_NAME[day.month]
    if kind == "month":
        return "sometime in " + month
    if kind == "end":
        return "the end of " + month
    if kind == "week":
        return "around " + WEEKDAY_NAME[day.weekday()]
    return "%s %d %s" % (WEEKDAY_NAME[day.weekday()], day.day, month)

_DAY_NAMED = re.compile(
    r"\b(?:(?:mon|tues|wednes|thurs|fri|satur|sun)day|tomorrow|tonight|the weekend|next week|"
    r"next month)(?:\s+(?:night|morning|afternoon|evening|lunchtime|midday))?\b", re.I)
_MOVED = re.compile(
    r"\b(?:instead|move it|push it|put it off|leave it (?:till|until|to)|another day|a day later)\b",
    re.I)
_PLAN_VERB = re.compile(
    r"\b(?:make|cook|do|have|serve|eat|start|finish|go|come|meet|post|send|call|book|clean|"
    r"get|buy|pick|deliver|visit)\b", re.I)
_POINTS_AT_IT = re.compile(r"\b(?:it|that|this)\b", re.I)


def a_plan_moved_to_a_day(text):
    said = " ".join(str(text or "").lower().split()).strip(" .!?")
    if not said or len(said.split()) > 14:
        return None
    day = _DAY_NAMED.search(said)
    if not day:
        return None
    if not _MOVED.search(said) and not re.search(r"\b(?:on|till|until)\s+" + re.escape(day.group(0)),
                                                 said):
        return None
    if not _PLAN_VERB.search(said) or not _POINTS_AT_IT.search(said):
        return None
    line = _DAY_NAMED.sub("ahead of time", said, count=1)
    line = _MOVED.sub("", line)
    line = re.sub(r"\b(?:on|till|until)\s+ahead of time\b", "ahead of time", line)
    line = " ".join(line.split())
    if "ahead of time" not in line:
        return None
    return {"day": " ".join(day.group(0).split()), "line": line}


HOW_LONG_ASK = re.compile(
    r"\bhow\s+long\s+(?:have|has|had|did)\b"
    r"|\bhow\s+(?:many|much)\s+(?:months?|weeks?|years?|days?)\s+(?:has|have|had)\s+it\s+been\b",
    re.I)

NOT_A_LENGTH_ASK = re.compile(
    r"\bhow\s+long\s+(?:have|has|had)\s+(?:i|we|you|it|they)\s+"
    r"(?:got|get|to\s+wait|to\s+go|left|before)\b"
    r"|\bhow\s+long\s+(?:until|till|before|after)\b"
    r"|\bhow\s+long\s+(?:do|does|will|would|should|can|could|must)\b"
    r"|\bhow\s+long\s+(?:ago|is|was)\b"
    r"|\bhow\s+long\s+(?:have|has|had)\s+(?:i|we|you)\s+(?:got|got\s+to|to|need)\b"
    r"|\bhow\s+long\s+(?:have|has|had)\s+(?:you|it|that)\s+been\s+"
    r"(?:like\s+that|this|with\s+you|since|now)\b",
    re.I)

AGO_LENGTH = re.compile(
    r"\b(?P<n>\d+|a|an|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|fifteen|"
    r"twenty|a\s+couple\s+of|a\s+few|couple\s+of|few)\s+"
    r"(?P<unit>days?|weeks?|fortnights?|months?|years?)\s+ago\b", re.I)

LAST_LENGTH = re.compile(r"\blast\s+(?P<unit>week|fortnight|month|year)\b", re.I)

FOR_LENGTH = re.compile(
    r"\bfor\s+(?P<n>\d+|a|an|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|"
    r"fifteen|twenty|a\s+couple\s+of|a\s+few|couple\s+of)\s+"
    r"(?P<unit>days?|weeks?|fortnights?|months?|years?)\b", re.I)

WEEKDAY_SAID = re.compile(
    r"\bon\s+(?P<day>monday|tuesday|wednesday|thursday|friday|saturday|sunday)\b", re.I)

WEEKDAYS = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]

A_YEAR_SAID = re.compile(r"\b(?:19|20)\d\d\b")

BEGAN = re.compile(
    r"\b(?:started|start|began|begin|kicked\s+off|took\s+up|moved|stopped|quit|gave\s+up|joined|"
    r"arrived|switched|changed|since|ago|for\s+(?:\d+|a|an|one|two|three|four|five|six|seven|"
    r"eight|nine|ten|eleven|twelve)\s+(?:days?|weeks?|months?|years?)"
    r"|got\s+(?:married|engaged|together|a\s+dog|a\s+cat|a\s+puppy|a\s+kitten|the\s+keys)"
    r"|married|adopted|bought|got"
    r"|last\s+(?:week|fortnight|month|year))\b", re.I)

ASKED_ABOUT_THE_THING = frozenset("""it this that them there here doing done at it going on
been am is was long how lived living worked working gone many much month months week weeks year
years day days time now since already has have had did is are were was being like get got""".split())

NUMBER_WORDS = {"a": 1, "an": 1, "one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6,
                "seven": 7, "eight": 8, "nine": 9, "ten": 10, "eleven": 11, "twelve": 12,
                "fifteen": 15, "twenty": 20}

A_UNIT_OF_TIME = {"day": 1, "week": 7, "fortnight": 14, "month": 30, "year": 365}


def how_long_answer(text, memory):
    line = " ".join(str(text or "").split())
    if not HOW_LONG_ASK.search(line) or NOT_A_LENGTH_ASK.search(line):
        return None
    if CALENDAR_NOW.match(line) or WHEN_SAID.search(line):
        return None
    put_right = _a_day_put_right(memory)
    if put_right:
        return put_right
    words = [word for word in content(line) if word not in ASK_THROWS]
    named = [word for word in words if word not in ASKED_ABOUT_THE_THING]
    for said, said_words in _the_lines_that_began(memory):
        if named and not _names_it(named, said):
            continue
        answer = _the_length_from(said)
        if answer:
            return answer
    return None


DAY_PUT_RIGHT = re.compile(
    r"\b(?:no,?\s+|actually,?\s+|sorry,?\s+)?(?:it\s+was|it's|it is|i\s+meant|i\s+mean|"
    r"make\s+that)\b[^.,!?]*\b(?P<day>january|february|march|april|may|june|july|august|"
    r"september|october|november|december|(?:19|20)\d\d|last\s+(?:week|month|year)|"
    r"\d+\s+(?:days?|weeks?|months?|years?)\s+ago)\b", re.I)


A_DAY_FORM = re.compile(r"\b(?:\d+|last\s+(?:week|month|year))\b", re.I)


def _a_day_put_right(memory):
    turns = memory.get("turns") if isinstance(memory, dict) else None
    if not isinstance(turns, list) or len(turns) < 2:
        return None
    last = turns[-1] if isinstance(turns[-1], dict) else None
    before = turns[-2] if isinstance(turns[-2], dict) else None
    if not last or not before:
        return None
    said = " ".join(str(last.get("user") or "").split())
    earlier = " ".join(str(before.get("user") or "").split())
    if not said or not earlier or not BEGAN.search(earlier):
        return None
    found = DAY_PUT_RIGHT.search(said)
    if not found:
        return None
    day = found.group("day")
    return _the_length_from("it began in " + day if not A_DAY_FORM.search(day) else
                            "it began " + day)


def _the_lines_that_began(memory):
    turns = memory.get("turns") if isinstance(memory, dict) else None
    if not isinstance(turns, list):
        return []
    found = []
    for turn in reversed(turns):
        if not isinstance(turn, dict):
            continue
        said = " ".join(str(turn.get("user") or "").split())
        if not said or _is_an_ask(said):
            continue
        if not BEGAN.search(said):
            continue
        found.append((said, content(said)))
        if len(found) >= 4:
            break
    return found


def _names_it(named, said):
    said_words = content(said)
    for word in named:
        if not any(_same(word, other) for other in said_words):
            return False
    return True


def _the_length_from(said):
    ago = AGO_LENGTH.search(said)
    if ago:
        count = _a_count(ago.group("n"))
        unit = ago.group("unit").lower().rstrip("s")
        if not count:
            return None
        if unit == "couple":
            return _about("a couple of weeks", "")
        days = count * A_UNIT_OF_TIME.get(unit, 0)
        said_length = " ".join(ago.group(0).split()[:-1])
        when = ""
        if unit == "year":
            when = str(datetime.date.today().year - count)
        return _about(said_length, when) if days else None
    last = LAST_LENGTH.search(said)
    if last:
        unit = last.group("unit").lower()
        if unit == "week":
            return _about("a week", "")
        if unit == "fortnight":
            return _about("a fortnight", "")
        if unit == "month":
            return _about("a month", _the_month_back(1))
        if unit == "year":
            return _about("a year", str(datetime.date.today().year - 1))
    held = FOR_LENGTH.search(said)
    if held and not AGO_LENGTH.search(said):
        count = _a_count(held.group("n"))
        unit = held.group("unit").lower().rstrip("s")
        if count and unit in A_UNIT_OF_TIME:
            return _about("%s %s%s" % (_a_count_said(count), unit, "" if count == 1 else "s"), "")
    for span, _at in _dated(memory_of_one(said)):
        day = _the_day_a_span_names(span)
        if not day:
            continue
        return _about(_a_length_in_words((datetime.date.today() - day).days), _a_day_said(day))
    weekday = WEEKDAY_SAID.search(said)
    if weekday:
        day = _the_day_a_weekday_names(weekday.group("day"))
        if day:
            return _about(_a_length_in_words((datetime.date.today() - day).days),
                          _the_month_name(day.month) if day.day == 1 else
                          weekday.group("day").capitalize())
    year = A_YEAR_SAID.search(said)
    if year:
        day = _the_day_a_span_names(year.group(0))
        if day:
            return _about(_a_length_in_words((datetime.date.today() - day).days), year.group(0))
    return None


def memory_of_one(said):
    return {"turns": [{"user": said, "bot": ""}]}


def _a_count(said):
    word = str(said or "").strip().lower()
    if word.isdigit():
        return int(word)
    return NUMBER_WORDS.get(word, 0)


def _the_day_a_span_names(span):
    words = [word for word in re.split(r"[^a-z0-9]+", str(span or "").lower()) if word]
    month = 0
    day = 0
    year = 0
    for word in words:
        if word in MONTHS:
            month = _the_month_number(word)
        elif re.fullmatch(r"\d{4}", word):
            year = int(word)
        elif re.fullmatch(r"\d{1,2}(?:st|nd|rd|th)?", word):
            day = int(re.sub(r"\D", "", word))
        elif word in ("early", "mid", "late", "in", "on", "the", "of", "at", "since", "back"):
            continue
    today = datetime.date.today()
    if year:
        return datetime.date(year, month or 1, day or 1)
    if not month:
        return None
    for back in range(0, 3):
        try:
            found = datetime.date(today.year - back, month, day or 1)
        except ValueError:
            return None
        if found <= today:
            return found
    return None


def _the_day_a_weekday_names(word):
    try:
        back = (datetime.date.today().weekday() - WEEKDAYS.index(str(word or "").lower())) % 7
    except ValueError:
        return None
    return datetime.date.today() - datetime.timedelta(days=back)


def _the_month_number(word):
    order = ["january", "february", "march", "april", "may", "june", "july", "august",
             "september", "october", "november", "december"]
    try:
        return order.index(str(word or "").lower()) + 1
    except ValueError:
        return 0


def _the_month_back(months):
    today = datetime.date.today()
    year, month = today.year, today.month
    for _ in range(max(1, int(months or 1))):
        month -= 1
        if month < 1:
            month, year = 12, year - 1
    return _the_month_name(month)


def _the_month_name(number):
    order = ["January", "February", "March", "April", "May", "June", "July", "August",
             "September", "October", "November", "December"]
    return order[number - 1] if 1 <= number <= 12 else ""


def _a_day_said(day):
    if day.day == 1:
        return _the_month_name(day.month)
    return "the %d%s of %s" % (day.day, _an_ordinal_end(day.day), _the_month_name(day.month))


def _an_ordinal_end(number):
    if 10 <= number % 100 <= 20:
        return "th"
    return {1: "st", 2: "nd", 3: "rd"}.get(number % 10, "th")


SPELLED_COUNT = {1: "a", 2: "two", 3: "three", 4: "four", 5: "five", 6: "six", 7: "seven",
                 8: "eight", 9: "nine", 10: "ten", 11: "eleven", 12: "twelve"}


def _a_count_said(number):
    number = int(number or 0)
    return SPELLED_COUNT.get(number, str(number))


def _a_length_in_words(days):
    days = max(0, int(days or 0))
    if days < 1:
        return "a day"
    if days < 12:
        return "%s %s" % (_a_count_said(days), "day" if days == 1 else "days")
    if days < 60:
        return "%s weeks" % _a_count_said(int(round(days / 7.0)))
    if days < 730:
        return "%s months" % _a_count_said(int(round(days / 30.44)))
    years = days / 365.25
    halves = int(years * 2) / 2.0
    if halves == int(halves):
        return "%s %s" % (_a_count_said(int(halves)), "year" if halves == 1 else "years")
    return "%s and a half years" % _a_count_said(int(halves))


def _about(length, when):
    length = " ".join(str(length or "").split())
    if not length:
        return None
    if when:
        return "%s - since %s." % (_tidy(length), when)
    return "%s." % _tidy(length)


def _tidy(said):
    said = str(said or "").strip()
    return said[:1].upper() + said[1:] if said else said
