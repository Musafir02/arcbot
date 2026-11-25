import re
import string

from ..understanding import lexicon
from . import topics
from . import quotes as quoted

SHORT = 14

SENTENCE = re.compile(r"(?<=[.!?])\s+")

AGAIN = (
    "Same answer, and it covers this: {reply}",
    "That is still the thing to do: {reply}",
    "Nothing new to add on it: {reply}",
)
SHORT_AGAIN = (
    "Same as before: {reply}",
    "As I said: {reply}",
    "Still: {reply}",
)


AGAIN_HELP = "Same answer I'm afraid: {reply} If that hasn't worked for you, tell me what went wrong and I'll take it from there."

DETAIL_AGAIN = (
    "Same for {detail}: {reply}",
    "Same answer for {detail}: {reply}",
    "It is the same for {detail}: {reply}",
    "Same again for {detail}: {reply}",
)
SAME_ADVICE = (
    "Nothing separate for {detail} - it is the same advice: {reply}",
    "Nothing different for {detail} I'm afraid: the same answer covers it - {reply}",
    "No separate fix for {detail} - the same advice as before: {reply}",
    "Nothing more for {detail}: the same answer covers it - {reply}",
)
RETURN = (
    "Back to {detail}: {reply}",
    "Back to {detail} then: {reply}",
    "Back on {detail} again: {reply}",
    "As we said about {detail}: {reply}",
)

UNDERNEATH_SAID = (
    "{said} is the same thing underneath, and the step is the same: {reply}",
    "{said} is the same thing again, so the step has not changed: {reply}",
)
UNDERNEATH_CLAUSE = (
    "{said} - that is the same thing underneath, and the step is the same: {reply}",
    "{said}, and it comes to the same thing: {reply}",
)

NOTHING_MORE = (
    "Nothing more on it I'm afraid: {reply}",
    "That is all I have on it: {reply}",
    "There is nothing further to add: {reply}",
)

LIKE_I_SAID = ("Like I said: {reply}",)

FRAMES = tuple(dict.fromkeys(
    AGAIN + SHORT_AGAIN + (AGAIN_HELP,) + DETAIL_AGAIN + SAME_ADVICE + RETURN
    + UNDERNEATH_SAID + UNDERNEATH_CLAUSE + NOTHING_MORE + LIKE_I_SAID + topics.REPEAT))
FOR_THE_PERSON = {
    "i": "you", "me": "you", "my": "your", "mine": "yours", "myself": "yourself", "am": "are",
    "i'm": "you're", "im": "you're", "i've": "you've", "i'll": "you'll", "i'd": "you'd",
    "we": "you", "our": "your", "us": "you", "was": "were",
}

SLOT = re.compile(r"\{[a-z_]+\}")


FEELING = re.compile(r"^(?:i\s+feel|i\s+felt|i'?m\s+feeling|i\s+am\s+feeling|feeling)\s+(.+)$", re.I)
CANNOT = re.compile(r"^(?:i\s+can'?t|i\s+cannot|i\s+can\s+not|i'?m\s+not\s+able\s+to)\s+(.+)$", re.I)
BEING = re.compile(r"^(?:i'?m|i\s+am)\s+(?:so\s+|really\s+|very\s+|still\s+|just\s+|quite\s+)?(.+)$", re.I)
NOTHING = re.compile(r"^nothing\s+(\w+)\s+me$", re.I)
CLAUSE_ONLY = re.compile(r"^(?:everything|nobody|nothing|life|things|it|this)\s+\S", re.I)
OPENING_FILLER = re.compile(r"^(?:so|and|but|yeah|yeah|well|honestly|tbh|idk|dunno|just|ok|okay|"
                            r"hi|hey)\b[ ,]*", re.I)
A_PHRASE = 8


def the_name_the_answer_says(answer, detail, card=""):
    said = topics.words(str(answer or ""))
    if not said:
        return ""
    words = str(detail or "").split()
    while words:
        last = words[-1].lower()
        if last not in _NOT_THE_END and (last in said or (
                len(last) > 3 and any(word.startswith(last) for word in said))):
            return " ".join(words)
        words = words[:-1]
    whole = topics.words(str(card or ""))
    phrase = str(detail or "").split()
    last = phrase[-1].lower() if phrase else ""
    led = len(phrase) > 1 and any(word.lower() in _NOT_THE_END for word in phrase[:-1])
    if led and last not in _NOT_THE_END and last in whole:
        return str(detail or "").strip()
    return ""


_NOT_THE_END = frozenset(
    "a an the my your our his her their its this that these those some any".split())


def as_a_phrase(text):
    if not isinstance(text, str):
        return None
    whole = _a_phrase_of(text)
    if whole:
        return whole
    clauses = [part for part in re.split(r"[,;]|\band\b|\bbut\b|\bso\b", text) if part.strip()]
    for clause in reversed(clauses[1:] if len(clauses) > 1 else []):
        made = _a_phrase_of(clause)
        if made:
            return made
    return None


def _a_phrase_of(text):
    if not isinstance(text, str):
        return None
    line = OPENING_FILLER.sub("", text.strip().rstrip(".!,")).strip()
    if not line or len(line.split()) > A_PHRASE or "?" in line:
        return None
    found = NOTHING.match(line)
    if found:
        verb = found.group(1).lower()
        if verb.endswith("s") and verb not in ("is", "was", "has"):
            return ("clause", "Nothing " + verb + " you")
        return None
    for pattern in (FEELING, CANNOT):
        found = pattern.match(line)
        if found:
            rest = _for_the_person(found.group(1))
            if not rest or len(rest.split()) > A_PHRASE - 1:
                return None
            if "," in rest or ";" in rest or _says_i(found.group(1)):
                return None
            if rest.split()[0].lower() in ("to", "that", "like", "as", "so"):
                return None
            if pattern is CANNOT:
                return ("said", "Not being able to " + rest)
            return ("said", "Feeling " + rest)
    found = CLAUSE_ONLY.match(line)
    if found:
        turned = _for_the_person(line)
        return ("clause", turned[:1].upper() + turned[1:])
    found = BEING.match(line)
    if found:
        rest = _for_the_person(found.group(1))
        if "," in rest:
            return None
        words = rest.split()
        if not words or len(words) > 3:
            return None
        if words[-1].lower().endswith("ing") or words[0].lower() in ("going", "gonna", "about", "not"):
            return None
        if any(word.lower() in ("to", "the", "a", "an", "my", "your") for word in words):
            return None
        return ("said", "Being " + rest)
    return None


def _says_i(text):
    return any(word.strip(string.punctuation).lower() in FOR_THE_PERSON
               for word in str(text or "").split())


def _for_the_person(text):
    words = []
    for word in str(text or "").split():
        bare = word.strip(string.punctuation).lower()
        ending = word[len(word.rstrip(string.punctuation)):]
        head = word[:len(word) - len(ending)] if ending else word
        if bare in FOR_THE_PERSON:
            turned = FOR_THE_PERSON[bare]
            if word[:1].isupper():
                turned = turned.capitalize()
            words.append(turned + ending)
        else:
            words.append(word)
    return " ".join(words)


def the_same_thing_underneath(text, reply, times, memory=None):
    if not isinstance(reply, str) or not reply.strip() or not times or times < 2:
        return ""
    if _carries_a_lead_in(_flat(reply)) or unframed(reply):
        return ""
    made = as_a_phrase(text)
    if not made:
        return ""
    kind, said = made
    pool = UNDERNEATH_SAID if kind == "said" else UNDERNEATH_CLAUSE
    turns = len(memory.get("turns") or []) if isinstance(memory, dict) else times
    return pool[turns % len(pool)].format(said=said, reply=reply.strip())


SEPARATOR = re.compile(r"\s*(?::|\u2014|\u2013|-)\s*$")
ANY_SEPARATOR = r"\s*(?::|\u2014|\u2013|-)\s*"


def _lead(frame):
    head = str(frame).split("{reply}")[0]
    tail = ""
    stripped = SEPARATOR.sub("", head.rstrip())
    if stripped != head.rstrip():
        head, tail = stripped, ANY_SEPARATOR
    return re.compile("^" + ".+?".join(re.escape(part) for part in SLOT.split(head)) + tail)


LEADS = tuple(str(frame).split("{reply}")[0] for frame in FRAMES)
PATTERNS = tuple(_lead(frame) for frame in FRAMES)

LEAD_WORDS = tuple(
    lead for lead in (
        tuple(topics.words(str(frame).split("{")[0])) for frame in FRAMES
    ) if len(lead) > 1
)
COLON_LEADS = tuple(
    lead[0] for lead in (
        tuple(topics.words(str(frame).split("{")[0])) for frame in FRAMES
    ) if len(lead) == 1
)
ONE_WORD_LEAD = re.compile(
    r"^(%s)\s*[:,]\s" % "|".join(re.escape(word) for word in COLON_LEADS),
    re.IGNORECASE,
) if COLON_LEADS else None


def unframed(reply):
    mine = str(reply or "")
    for pattern in PATTERNS:
        match = pattern.match(mine)
        if match and mine[match.end():].strip():
            return mine[match.end():].strip()
    return None


def _flat(text):
    return " ".join(topics.words(text or ""))


def the_cause_said_again(reply, memory=None):
    from ..compose import why
    understood = memory.get("understood") if isinstance(memory, dict) else None
    if not isinstance(understood, dict) or understood.get("wants") != "reason":
        return None
    named = getattr(why, "NAMED_CAUSE", None)
    if named is None:
        return None
    for said in (reply, _the_answer_in_hand(reply, memory), _a_card_behind(memory)):
        parts = [part.strip() for part in quoted.sentences(said, SENTENCE) if part.strip()]
        for at, part in enumerate(parts):
            found = named.search(part)
            if not found or found.start() > 2 or len(part.split()) < 6:
                continue
            if at == 0:
                if len(parts) > 1 and _led_an_earlier_answer(part, memory):
                    return " ".join(parts[1:])
                return None
            move = [other for other in parts[:at] if other]
            if _led_an_earlier_answer(part, memory):
                return " ".join(parts[1:]) if len(parts) > 1 else None
            return part + (" " + move[0] if move else "")
    return None


def _a_card_behind(memory):
    from ..compose import why
    named = getattr(why, "NAMED_CAUSE", None)
    if named is None or not isinstance(memory, dict):
        return ""
    seen = 0
    for turn in reversed(list(memory.get("turns") or ())):
        if not (isinstance(turn, dict) and turn.get("bot")):
            continue
        said = str(turn["bot"])
        for part in quoted.sentences(said, SENTENCE):
            found = named.search(part.strip())
            if found and found.start() <= 2 and len(part.split()) >= 6:
                return said
        seen += 1
        if seen >= 3:
            break
    return ""


def _led_an_earlier_answer(sentence, memory):
    said = " ".join(str(sentence or "").lower().split())
    if not said or not isinstance(memory, dict):
        return False
    for turn in reversed(list(memory.get("turns") or ())):
        if isinstance(turn, dict) and turn.get("bot"):
            if " ".join(str(turn["bot"]).lower().split()).startswith(said):
                return True
    return False


def _the_answer_in_hand(reply, memory):
    mine = " ".join(str(reply or "").lower().split()[:8])
    if len(mine) < 25 or not isinstance(memory, dict):
        return ""
    seen = 0
    for turn in reversed(list(memory.get("turns") or ())):
        if not (isinstance(turn, dict) and turn.get("bot")):
            continue
        said = str(turn["bot"])
        if mine in " ".join(said.lower().split()):
            return said
        seen += 1
        if seen >= 3:
            break
    return ""


def _short(reply, memory=None):
    cause = the_cause_said_again(reply, memory)
    if cause:
        return cause
    parts = quoted.sentences(reply, SENTENCE)
    if not parts:
        return str(reply or "")
    if len(parts[0].split()) >= SHORT or len(parts) == 1:
        kept = parts[:1]
    else:
        kept = parts[:2]
    return quoted.closed(" ".join(part.strip() for part in kept), parts[len(kept):], reply)


def _the_first_sentence(reply, memory=None):
    cause = the_cause_said_again(reply, memory)
    if cause:
        return cause
    parts = quoted.sentences(reply, SENTENCE)
    if not parts:
        return str(reply or "")
    kept = parts[:1]
    if len(parts[0].split()) < 5 and len(parts) > 1:
        kept = parts[:2]
    return quoted.closed(" ".join(part.strip() for part in kept), parts[len(kept):], reply)


def _carries_a_lead_in(mine):
    said = " ".join(topics.words(mine))
    if not said:
        return False
    for lead in tuple(topics.REPEAT_LEADS) + LEAD_WORDS:
        if said.startswith(" ".join(lead) + " "):
            return True
    if ONE_WORD_LEAD is not None and ONE_WORD_LEAD.match(str(mine or "").lstrip()):
        return True
    return False


def carries_a_lead_in(reply):
    return _carries_a_lead_in(str(reply or ""))


def _times_on_the_screen(mine, memory):
    turns = memory.get("turns")
    if not isinstance(turns, list):
        return 0
    times = 0
    for turn in reversed(turns):
        if not isinstance(turn, dict):
            break
        said = turn.get("bot")
        if _flat(said) != mine:
            body = _flat(unframed(said) or "")
            if not body or not mine.startswith(body):
                break
        times += 1
    return times


def _said_earlier(mine, memory):
    return _said_earlier_text(mine, memory) != ""


def _said_earlier_text(mine, memory):
    if len(mine.split()) <= SHORT:
        return ""
    turns = memory.get("turns")
    if not isinstance(turns, list) or not turns:
        return ""
    for turn in turns:
        if not isinstance(turn, dict):
            continue
        said = _flat(turn.get("bot"))
        if said == mine:
            return said
        if said.startswith(mine + " "):
            return said
    return ""


def _names_something_the_answer_says(text, mine):
    said = {word for word in topics.words(str(text or ""))
            if len(word) > 2 and word not in topics.STOPWORDS
            and word not in topics.ASK_ONLY}
    if not said:
        return False
    return bool(said & set(mine.split()))


def _returned_thing(memory, text):
    record = topics.resumed(memory)
    if not isinstance(record, dict):
        return ""
    thing = " ".join(str(record.get("asked") or "").lower().split())
    if not thing or len(thing.split()) > 4:
        return ""
    if thing not in _flat(text):
        return ""
    return thing


def _the_line_asks(memory, text):
    record = topics.resumed(memory)
    if isinstance(record, dict) and record.get("asks") is not None:
        return bool(record.get("asks"))
    said = memory.get("understood") if isinstance(memory, dict) else None
    if isinstance(said, dict):
        return said.get("kind") == "question" or bool(said.get("asks"))
    return bool(AN_ASK.search(_flat(text)))


def _adds_nothing_the_answer_did_not_say(thing, text, said, memory):
    if not _the_line_asks(memory, text):
        return False
    said_as_typed = memory.get("understood") if isinstance(memory, dict) else None
    typed = said_as_typed.get("text") if isinstance(said_as_typed, dict) else None
    asked = _flat(typed if isinstance(typed, str) and typed.strip() else text)
    thing = set(str(thing or "").lower().split())
    added = {word for word in asked.split()
             if word.isalpha() and len(word) > 2 and word not in FRAME_WORDS
             and word not in thing and word not in lexicon.CORE_WORDS}
    return not (added & set(_flat(said).split()))


AN_ASK = re.compile(
    r"\b(?:what|whats|which|why|how|when|where|who|whose|should|shall|could|would|can|do|does|"
    r"did|is|are|was|were|any|anything)\b|\?")

FRAME_WORDS = frozenset("""back again then about as said return returning goes going go to a an the
    of in on at for and or but so also just still now it its this that these those i me my we our
    you your they them their he she him her please thanks thank""".split())


def _places():
    try:
        from ..understanding.topics import PLACES
    except ImportError:
        return frozenset()
    return PLACES


def _as_a_name(thing):
    places = _places()
    return " ".join(word[:1].upper() + word[1:] if word in places else word
                    for word in str(thing or "").split())


def _without_the_thing_in_front(short, thing):
    said = str(short or "").strip()
    for pattern in (r"^(?:in|at|on|for|about|with|around)\s+%s\s*[:,]?\s+",
                    r"^%s\s*[:,]\s+"):
        found = re.match(pattern % re.escape(str(thing or "").lower()), said, re.I)
        if found and said[found.end():]:
            rest = said[found.end():]
            return rest[0].upper() + rest[1:]
    return said


def _said_recently(mine, memory, look=3):
    turns = memory.get("turns")
    if not isinstance(turns, list):
        return 0
    said = [one for one in (_flat(turn.get("bot")) for turn in turns if isinstance(turn, dict))
            if one]
    return 1 if mine in said[-look:] else 0


A_DETAIL = re.compile(r"\bhow\s+(?:long|much|many|often|far|hot|old|quickly)\b", re.I)


def _says_it_came_back(text):
    try:
        from . import returned
    except Exception:
        return False
    says = getattr(returned, "says_it_happened_again", None)
    return bool(says and says(text))


ANOTHER_ONE = re.compile(
    r"\b(?:what|how) about\b|\b(?:bigger|smaller|larger|heavier|lighter|cheaper|dearer|pricier|"
    r"costlier|older|younger|worse|better|other|different|longer|shorter|higher|lower|faster|"
    r"nearer|further|farther|easier|harder|stronger|weaker|hotter|colder|warmer|quicker|"
    r"newer|smarter|richer|poorer|nicer|simpler|tougher|thicker|thinner|slower)\b", re.I)


A_MONEY_ASK = re.compile(
    r"\bhow much\b|\bhow many (?:pounds|dollars|euros)\b", re.I)
MONEY_SAID = re.compile(
    r"\b(?:owe|owes|owed|pay|paid|pays|cost|costs|price|prices|afford|spend|spent|bill|bills|"
    r"budget|save|saved|earn|earns|salary|wage|wages|rent|money|card|loan|mortgage|debt|"
    r"deposit|refund|quote|quoted)\b", re.I)
AN_AMOUNT = re.compile(
    r"[\u00a3$\u20ac]|\b\d+(?:\.\d+)?\s?(?:pounds?|quid|dollars?|euros?|bucks|pence|cents)\b|"
    r"\b\d+(?:,\d{3})+\b|\b[bB]\d{2,}\b", re.I)


def _a_figure_asked_that_the_answer_does_not_hold(text, reply):
    line = " ".join(str(text or "").split())
    if not line or not A_MONEY_ASK.search(line) or not MONEY_SAID.search(line):
        return False
    return not AN_AMOUNT.search(str(reply or ""))


def _asks_for_a_detail(text):
    return bool(A_DETAIL.search(str(text or "")))


A_REPORT = re.compile(r"\b(?:i|im|i'm|i've|ive|we|we're|we've|my|our|he|he's|hes|she|she's|"
                      r"shes|they|they're|they've)\s+\w", re.I)
AN_ASK = re.compile(r"\b(?:what|which|how|why|when|where|who|can|could|should|would|shall|is|"
                    r"are|do|does|did|any|anything|anyone|remind|tell|told|worth)\b|\?", re.I)


A_STILL_GOING_ON = re.compile(
    r"\b(?:keeps?|kept|keeps on|still|again|always|every|each|wont|won't|never|constantly|"
    r"over and over|every time|all the time)\b", re.I)


def _a_report(text):
    line = str(text or "")
    if not line or not A_REPORT.search(line) or AN_ASK.search(line):
        return False
    return not A_STILL_GOING_ON.search(line)


A_SCRIPT = re.compile(r"(?:\"[^\"]{8,}\"|\u201c[^\u201d]{8,}\u201d"
                      r"|(?<![\w])'[^']{8,}'(?![\w]))")


def _has_a_script(reply):
    return bool(A_SCRIPT.search(str(reply or "")))


def _the_line_that_got_it(mine, memory, look=3):
    turns = memory.get("turns")
    if not isinstance(turns, list):
        return ""
    for turn in reversed(turns[-look:]):
        if isinstance(turn, dict) and _flat(turn.get("bot")) == mine:
            return " ".join(str(turn.get("user") or "").split())
    return ""


def _said_and_more(mine, memory):
    turns = memory.get("turns")
    if not mine or not isinstance(turns, list) or not turns:
        return False
    last = turns[-1] if isinstance(turns[-1], dict) else {}
    raw = str(last.get("bot") or "").strip()
    said = _flat(raw)
    if not said or not said.startswith(mine + " ") or not raw.endswith("?"):
        return False
    return True
FACT_RECALL = re.compile(
    r"^(?:you(?:'ve| have) (?:got|had)|you (?:live|'re|are)|your \w[\w' -]{0,20}? (?:is|was)|"
    r"i have you as|you told me (?:you|your|it))\b", re.I)
SAID_BACK = re.compile(r"^(?:you said\b|you told me\b|i have you as\b)", re.I)


def already_had(reply, memory):
    mine = _flat(reply)
    if not mine or not isinstance(memory, dict):
        return None
    if _carries_a_lead_in(mine) or len(mine.split()) <= SHORT:
        return None
    if not _said_earlier(mine, memory):
        return None
    return AGAIN[0].format(reply=str(reply or "").strip())


def _as_said(text):
    seen = []
    for word in topics.words(str(text or "")):
        if len(word.rstrip("s")) > 2 and word not in topics.STOPWORDS \
                and word not in topics.ASK_ONLY:
            if word not in seen:
                seen.append(word)
    return seen


def _content_words_in_order(text):
    return [word.rstrip("s") or word for word in _as_said(text)]


_RULED_OUT = re.compile(r"\b(?:no|not|without|instead|except|never|other\s+than)\b", re.I)


def _the_run_they_said_both_times(text, earlier):
    said = str(text or "")
    stop = _RULED_OUT.search(said)
    if stop:
        said = said[:stop.start()]
    best, run = [], []
    for word in topics.words(said):
        if (word.rstrip("s") or word) in earlier:
            if word not in run:
                run.append(word)
            if len(run) > len(best):
                best = list(run)
        elif len(word.rstrip("s")) > 2 and word not in topics.STOPWORDS \
                and word not in topics.ASK_ONLY:
            run = []
    return " ".join(best) if len(best) > 1 else ""


def _the_same_question_asked_again(mine, text, memory):
    asked = set(_content_words_in_order(text))
    if len(asked) < 2:
        return ""
    turns = memory.get("turns") if isinstance(memory, dict) else None
    if not isinstance(turns, list):
        return ""
    for turn in turns:
        if not isinstance(turn, dict):
            continue
        said = _flat(turn.get("bot"))
        if said != mine and not said.startswith(mine + " "):
            continue
        earlier = set(_content_words_in_order(turn.get("user")))
        if len(earlier) < 2:
            continue
        if len(asked & earlier) * 4 < len(asked | earlier) * 3:
            continue
        return _the_run_they_said_both_times(text, earlier)
    return ""


def _the_subject_on_the_screen(memory):
    if not isinstance(memory, dict):
        return ""
    returned = memory.get("returned")
    if isinstance(returned, dict):
        turn = returned.get("turn")
        if isinstance(turn, int) and turn >= len(memory.get("turns") or []) - 2:
            subject = " ".join(str(returned.get("asked") or "").split())
            if subject:
                return _as_your(subject)
    record = memory.get("topic")
    subject = str(record.get("subject") or "").strip() if isinstance(record, dict) else ""
    return _as_your(subject)


def _as_your(subject):
    if subject.lower().startswith("my "):
        return "your " + subject[3:]
    return subject


def replied(respond):
    def respond_once(text, memory):
        reply = respond(text, memory)
        if not isinstance(reply, str) or not reply.strip():
            return reply
        try:
            return instead(reply, text, memory) or reply
        except Exception:
            return reply

    respond_once.__name__ = getattr(respond, "__name__", "respond_once")
    respond_once.__doc__ = respond.__doc__
    respond_once.checks_earlier_turns = True
    return respond_once


def instead(reply, text, memory):
    mine = _flat(reply)
    if not mine or not isinstance(memory, dict):
        return None
    if _carries_a_lead_in(mine):
        return None
    said_back = str(reply or "").strip()
    if SAID_BACK.match(said_back) and len(mine.split()) <= SHORT:
        return None
    times = _times_on_the_screen(mine, memory)
    if not times:
        times = _said_recently(mine, memory)
    if not times and _said_and_more(mine, memory):
        times = 1
    if not times and _said_earlier(mine, memory):
        thing = _returned_thing(memory, text)
        if not thing:
            asked = _the_same_question_asked_again(mine, text, memory)
            if asked:
                detail = _the_subject_on_the_screen(memory) or asked
                frame = RETURN[len(memory.get("turns") or []) % len(RETURN)]
                return frame.format(detail=_as_a_name(detail),
                                    reply=_the_first_sentence(reply, memory))
            return None
        said = _said_earlier_text(mine, memory)
        if said and not _adds_nothing_the_answer_did_not_say(thing, text, said, memory):
            return None
        thing = _as_a_name(thing)
        frame = RETURN[len(memory.get("turns") or []) % len(RETURN)]
        body = _without_the_thing_in_front(str(reply or "").strip(), thing)
        return frame.format(detail=thing, reply=body)
    if not times:
        return None
    return _framed_as_a_repeat(reply, mine, memory, times, text)


def a_thing_of_the_answer(reply, text, memory):
    mine = _flat(reply)
    if not mine or not isinstance(memory, dict):
        return None
    if _carries_a_lead_in(mine):
        return None
    if not _said_earlier(mine, memory):
        return None
    if not _names_something_the_answer_says(text, mine):
        return None
    from . import returned
    if returned.the_next_step(str(reply or "")):
        return None
    return _framed_as_a_repeat(reply, mine, memory, 1, text)


def _another_stand_down(reply, memory):
    from ..compose import fallback
    mine = _flat(reply)
    if not mine:
        return None
    for line in fallback.UNKNOWN:
        if _flat(line) != mine:
            continue
        others = [o for o in fallback.UNKNOWN if _flat(o) != mine]
        if not others:
            return None
        turns = memory.get("turns") or []
        return others[len(turns) % len(others)]
    return None


def _framed_as_a_repeat(reply, mine, memory, times, text=""):
    if _says_it_came_back(text):
        return None
    if len(mine.split()) <= SHORT:
        return SHORT_AGAIN[min(times, len(SHORT_AGAIN)) - 1].format(reply=reply.strip())
    if _a_report(text):
        return None
    from ..compose import fallback
    if ((fallback.WORDING_ASKS.search(text) or fallback.WORDING_SOMEONE.search(text)
         or fallback.WORDING_SAYS.search(text)) and not _has_a_script(reply)):
        return None
    from . import repeat
    if repeat.asks_for_the_move(text):
        return None
    if _a_figure_asked_that_the_answer_does_not_hold(text, reply):
        return None
    underneath = the_same_thing_underneath(text, _short(reply, memory), times, memory)
    if underneath:
        return underneath
    short = _short(reply, memory)
    if _flat(short) != mine and _times_on_the_screen(_flat(short), memory):
        short = reply
    if ((_asks_for_a_detail(text) or ANOTHER_ONE.search(str(text or "")))
            and not _asks_for_a_detail(_the_line_that_got_it(mine, memory))):
        short = reply
    said_twice = _another_stand_down(reply, memory)
    if said_twice:
        return said_twice
    lead = AGAIN[min(times, len(AGAIN)) - 1]
    if ":" in short:
        lead = lead.replace(": {reply}", " \u2014 {reply}")
    return lead.format(reply=short)
