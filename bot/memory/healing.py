import re

ASKS = re.compile(
    r"\bhow long\b[^.?!]{0,40}?"
    r"\b(?:heal|heals|healing|mend|mends|mending|recover|recovers|recovering|"
    r"get better|gets better|getting better|get over|gets over|getting over|"
    r"clear up|clears up|clearing up|go away|goes away|going away|die down|dies down|"
    r"settle down|settles down|stop hurting|ease off|eases off|get well|be better|"
    r"feel better|feels better|feel normal|back to normal|"
    r"be like this|stay like this|stays like this|be gone|keep me off my feet|"
    r"last|lasts|lasted)\b", re.I)


NAMES_ITS_OWN = re.compile(
    r"\bhow long (?:does|do|will|would|should|is|are|can|could)\b", re.I)

CARE = re.compile(
    r"\b(?:ice it|ice for|rest it|rest the|raise it|keep it up|wrap it|press a clean|"
    r"cool running water|paracetamol|ibuprofen|antihistamine|hydrocortisone|"
    r"see a gp|ring the surgery|get it looked at|get it checked|have it looked at|"
    r"ease off|keep it moving|keep moving|plenty of (?:fluids|water)|drink plenty|"
    r"prop yourself up|a spoonful of honey|warm drinks|early night|stay off it)\b", re.I)

_SPAN = (r"(?:\d+|an?|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|a couple of"
         r"|a few|several)(?:\s*(?:to|or|-)\s*(?:\d+|one|two|three|four|five|six|seven|eight"
         r"|nine|ten|eleven|twelve|a few))?\s*"
         r"(?:hours?|days?|weeks?|fortnights?|months?|years?)")

_TIMELINE = re.compile(
    r"\b(?P<verb>settles?|settled|eases?|eased|heals?|healed|mends?|mended|recovers?|recovered|"
    r"lasts?|lasted|clears? up|cleared up|fades?|faded|dies down|die down|goes away|go away|"
    r"gets? better|get better|getting better|is properly better|are properly better|"
    r"properly better|is better|are better|feels? normal|back to normal|takes|took|"
    r"hangs? on|hang on|lingers?|settling|easing|healing|mending)\b"
    r"(?:[^.?!;:]{0,30}?)\b(?:in|within|after|for|about|around)?\s*"
    r"(?P<span>" + _SPAN + r")", re.I)

_BARE_SPAN = re.compile(r"^\s*(?:about|around|roughly|usually)?\s*(?P<span>" + _SPAN + r")\s*[.!]?\s*$",
                        re.I)

_ONLY_A_SPAN = re.compile(r"^\s*(?:about|around|roughly|usually)?\s*" + _SPAN + r"\s*[.!]?\s*$", re.I)

NO_TIMELINE = (
    "I know what helps with it, but not how long it takes to mend - I'd rather not guess at a "
    "number. If it's no easier after a few days, that's the point to get it looked at.",
    "How long it takes is the part I would be guessing at. What I have is what helps in the "
    "meantime, and if there's no change in a few days, that's when to get it looked at.",
    "I'd rather say I don't have a time than make one up. Keep doing what's in the card above and "
    "give it a few days - if it's no better by then, get it looked at.",
)

NO_TIME_THEN_STEP = (
    "{step} How long it takes is the part I would be guessing at.",
    "{step} I can't say how long it will take - the care is the part I know.",
    "{step} Past that I can't put a time on it, sorry.",
)

HEDGE = re.compile(
    r"\b(?:i'm not sure about that one|i don't know|beyond what i know|i'd rather not guess|"
    r"a quick search|search online|can't put a time on|would be guessing at|up to date on that"
    r"|beyond me)\b", re.I)

SENTENCE = re.compile(r"(?<=[.!?])\s+")
WORD = re.compile(r"[a-z']+")


def asks(text):
    line = str(text or "")
    if not line.strip() or not ASKS.search(line):
        return False
    return True


def the_timeline(answer):
    text = str(answer or "")
    if not text.strip():
        return ""
    for sentence in SENTENCE.split(text):
        match = _TIMELINE.search(sentence)
        if not match:
            continue
        end = match.end("span")
        clause = sentence[:end].rstrip(" ,;:-")
        if not clause:
            continue
        return clause[:1].upper() + clause[1:] + "."
    return ""


def _the_same_length(reply, timeline):
    said = _ONLY_A_SPAN.match(str(reply or ""))
    if not said:
        return False
    if not timeline:
        return False
    return said.group(0).strip(" .!").lower() in timeline.lower()


_ASK_WORDS = frozenset((
    "how", "long", "will", "would", "should", "could", "does", "take", "takes", "took", "get",
    "gets", "getting", "got", "heal", "heals", "healing", "mend", "mends", "mending", "recover",
    "recovers", "recovering", "better", "clear", "clears", "clearing", "away", "away", "goes",
    "going", "gone", "settle", "settles", "settling", "down", "ease", "eases", "easing", "time",
    "till", "until", "before", "after", "much", "many", "usually", "normal", "back", "stop",
    "feel", "feels", "well", "this", "that", "there", "then", "than", "them", "they", "their",
))


def _stem(word):
    for ending in ("ing", "ed", "es", "s"):
        if word.endswith(ending) and len(word) - len(ending) >= 4:
            return word[:-len(ending)]
    return word


def _carries(text):
    return {_stem(word) for word in WORD.findall(str(text or "").lower())
            if len(word) > 2 and word not in _ASK_WORDS}


def _said_before(memory, keep=2):
    lines = []
    for turn in reversed(list((memory or {}).get("turns") or ())):
        if isinstance(turn, dict) and turn.get("user"):
            lines.append(str(turn.get("user")))
            if len(lines) >= keep:
                break
    return lines


def derived(memory):
    if not isinstance(memory, dict):
        return False
    at = memory.get("healing_at")
    turns = memory.get("turns")
    if not isinstance(at, int) or not isinstance(turns, list):
        return False
    return at == len(turns) - 1


def _no_timeline(memory, step=""):
    turns = len(list((memory or {}).get("turns") or ()))
    step = str(step or "").strip()
    if step:
        step = step[:1].upper() + step[1:]
        return NO_TIME_THEN_STEP[turns % len(NO_TIME_THEN_STEP)].format(step=step)
    return NO_TIMELINE[turns % len(NO_TIMELINE)]


def _a_hedge(reply):
    return bool(HEDGE.search(str(reply or "")))


def _the_card(memory):
    said = [str(turn.get("bot")) for turn in (memory or {}).get("turns") or ()
            if isinstance(turn, dict) and turn.get("bot")]
    if derived(memory) and len(said) > 1:
        return said[-2]
    return said[-1] if said else ""


def vetted(text, memory, reply, step_of=None):
    if not asks(text):
        return reply
    card = _the_card(memory)
    if not card.strip() or not CARE.search(card):
        return reply
    timeline = the_timeline(card)
    said = str(reply or "")
    if not said.strip() and not timeline:
        return reply
    step = ""
    if callable(step_of):
        try:
            step = str(step_of(card) or "").strip()
        except Exception:
            step = ""
    vetted_reply = _the_healing_line(said, timeline, card, memory, step)
    if vetted_reply != said and isinstance(memory, dict):
        turns = memory.get("turns")
        memory["healing_at"] = len(turns) if isinstance(turns, list) else 0
    return vetted_reply


_REPEAT_LEAD = re.compile(r"^(?:same as before|as i said|same again)\s*[:,]?\s*", re.I)


def _the_same_as_the_card(said, card):
    said = str(said or "").strip().lower()
    card = str(card or "").strip().lower()
    if len(said) < 20 or len(card) < 40:
        return False
    body = _REPEAT_LEAD.sub("", said)
    return body in card or card in body


def _the_healing_line(said, timeline, card, memory, step=""):
    if not said.strip():
        return timeline or _no_timeline(memory, step)
    if _the_same_as_the_card(said, card):
        return timeline or _no_timeline(memory, step)
    if _a_hedge(said):
        return timeline or said
    if _ONLY_A_SPAN.match(said):
        return said if _the_same_length(said, timeline) else (timeline or _no_timeline(memory, step))
    if len(said.split()) > 10:
        before = _said_before(memory)
        subject = _carries(" ".join(before)) if before else set()
        if subject & _carries(said):
            return said
        if timeline and _carries(timeline) & _carries(said):
            return said
        return timeline or _no_timeline(memory, step)
    return said
