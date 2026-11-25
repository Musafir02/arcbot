import re

from ..compose import fallback

ASKS = re.compile(
    r"^\W*(?:how|what|whats|what's|which|when|where|who|why)\b"
    r"|^\W*(?:is|are|was|were|do|does|did|can|could|should|would|will|have|has|had|am)\s+"
    r"(?:i|you|we|they|it|that|this|there|he|she|any|my|your|his|her|their|the|a|an)\b"
    r"|\b(?:what|how|which|who|when|where) about\b", re.I)

DIET_WORD = re.compile(
    r"\b(?P<diet>vegan|vegetarian|coeliac|celiac|dairy[- ]free|gluten[- ]free|pescatarian)\b", re.I)
COUNT = re.compile(
    r"\b(?:there(?:'?s| is| are)\s+)?(?P<n>\d+|one|two|three|four|five|six|seven|eight|nine|ten)"
    r"\s+(?:of us|people|adults|kids|children|guests|coming|more|extra|others|mouths)\b", re.I)
NUMBER = {"one": "one", "two": "two", "three": "three", "four": "four", "five": "five", "six": "six",
          "seven": "seven", "eight": "eight", "nine": "nine", "ten": "ten"}
GOING = re.compile(
    r"\b(?:off|going|heading|away|flying|driving|travelling|traveling)\s+to\s+"
    r"(?P<place>[a-z][a-z' -]{2,24}?)(?:\s+(?:in|on|for|next|at)\b|$)", re.I)
MONTH = re.compile(
    r"\b(january|february|march|april|may|june|july|august|september|october|november|"
    r"december|spring|summer|autumn|winter)\b", re.I)
CONSIDERING = re.compile(
    r"\b(?:looking at|thinking (?:of|about)|considering|about to (?:buy|get|order)|"
    r"going to (?:buy|get|order)|planning (?:to get|on getting))"
    r"\s+(?:an\s+|the\s+|some\s+|a\s+)?"
    r"(?P<thing>[a-z][a-z' -]{2,30}?)(?:\s+(?:for|in|because|to|but)\b|[.,!?]|$)", re.I)


FOOD_WORDS = re.compile(
    r"\b(?:food|cook|cooking|cooked|eat|eats|eating|dish|recipe|meal|meals|menu|portion|"
    r"portions|serves|serving|dinner|roast|bake|baking|ingredient|ingredients|"
    r"cheese|chicken|pasta|rice|soup|salad)\b", re.I)


def _about_food(memory):
    said = []
    last = memory.get("last_answer") if isinstance(memory, dict) else None
    if isinstance(last, dict) and last.get("reply"):
        said.append(str(last["reply"]))
    for turn in reversed((memory or {}).get("turns") or []):
        if isinstance(turn, dict) and turn.get("bot"):
            said.append(str(turn["bot"]))
            break
    return any(FOOD_WORDS.search(one.lower()) for one in said)


def _asked(kind, detail, line):
    if kind == "dietword":
        return "what can i cook for a %s" % detail
    if kind == "count":
        if detail == "one more":
            return "how much food for one more person"
        return "how much food for %s people" % detail
    if kind == "going":
        month = MONTH.search(line)
        if month:
            return "what should i know before a trip to %s in %s" % (detail, month.group(1).lower())
        return "what should i know before a trip to %s" % detail
    if kind == "considering":
        return "what do i need to know before buying %s" % detail
    return None


def _the_read(clean):
    if not clean or "?" in clean or ASKS.search(clean.split(",")[0]):
        return None, None
    if len(clean.split()) > 16:
        return None, None
    match = DIET_WORD.search(clean)
    if match:
        return "dietword", match.group("diet").lower()
    match = COUNT.search(clean)
    if match:
        number = match.group("n").lower()
        if re.search(r"\b(?:more|extra|another)\b", clean):
            return "count", "one more"
        return "count", NUMBER.get(number, number)
    match = GOING.search(clean)
    if match:
        return "going", match.group("place").strip()
    match = CONSIDERING.search(clean)
    if match:
        thing = re.sub(r"^(?:(?:buying|getting|ordering)\s+)?(?:a|an|the)\s+", "",
                       match.group("thing").strip())
        return "considering", thing
    return None, None


def _a_real_answer(reply):
    said = " ".join(str(reply or "").split())
    if len(said) < 40:
        return False
    return not (fallback._is_a_hedge(said) or fallback._in_a_pool(said, (fallback.NEUTRAL,)))


def _said_already(memory):
    turns = (memory or {}).get("turns") if isinstance(memory, dict) else None
    said = []
    for turn in turns or []:
        if isinstance(turn, dict) and turn.get("bot"):
            said.append(" ".join(str(turn.get("bot")).split()))
    return said


def reply_for(text, memory):
    clean = " ".join(str(text or "").lower().split())
    kind, detail = _the_read(clean)
    if not kind:
        return None
    if kind == "count" and not _about_food(memory):
        return None
    question = _asked(kind, detail, clean)
    if not question:
        return None
    from ..modules import answers
    try:
        reply = answers.respond(question, {})
    except Exception:
        return None
    if not _a_real_answer(reply):
        return None
    if kind in ("going", "considering"):
        words = [word for word in re.findall(r"[a-z']{4,}", detail)]
        said = str(reply).lower()
        if words and not any(word in said for word in words):
            return None
    if " ".join(str(reply).split()) in _said_already(memory):
        return None
    return reply
