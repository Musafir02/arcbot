import re

MEASURES = {
    "much": re.compile(r"\b\d", re.I),
    "many": re.compile(r"\b\d|\b(?:one|two|three|four|five|six|seven|eight|nine|ten|dozen)\b",
                       re.I),
    "often": re.compile(r"\b(?:once|twice|thrice|every|each\s+(?:day|week|month|morning|night)|"
                        r"daily|weekly|monthly|hourly|times\s+a|a\s+day|a\s+week|a\s+month|"
                        r"\d\s*(?:-|to)?\s*\d*\s*times)\b", re.I),
    "long": re.compile(r"\b\d+\s*(?:second|minute|hour|day|week|month|year)s?\b|"
                       r"\b\d+\s*(?:-|to)\s*\d+\s*(?:second|minute|hour|day|week|month|year)s?"
                       r"\b|\bovernight\b|\ball\s+(?:day|night)\b", re.I),
    "far": re.compile(r"\b\d+\s*(?:mile|km|kilometre|kilometer|metre|meter|yard|foot|feet)s?\b",
                      re.I),
    "hot": re.compile(r"\b\d{2,3}\s*(?:\u00b0|c\b|f\b|degrees?)|\bgas\s*mark\s*\d", re.I),
    "deep": re.compile(r"\b\d+\s*(?:cm|centimetre|centimeter|inch|in|mm|metre|meter)s?\b", re.I),
    "big": re.compile(r"\b\d+\s*(?:cm|centimetre|centimeter|inch|in|mm|litre|liter|gram|kilo)s?"
                      r"\b", re.I),
}

LEAD = re.compile(r"^(?:(?:and|so|ok|okay|but|then|right|yeah|yes|well|oh|er|um|hmm)\b[\s,]*)+",
                  re.I)
TAIL = re.compile(r"[\s,]*(?:(?:again|then|exactly|please|thanks|though|for\s+that|for\s+one|"
                  r"for\s+each|per\s+(?:day|week|person|one)|roughly|about|or\s+so|"
                  r"is\s+that|was\s+that|would\s+that\s+be|does\s+that|do\s+i|did\s+i|"
                  r"would\s+i|should\s+i|will\s+i|of\s+that|there)\b[\s,]*)*$", re.I)

ASKED = re.compile(r"\bhow\s+(much|many|often|long|far|hot|deep|big)\b", re.I)

SENTENCE = re.compile(r"(?<=[.!?])\s+")


def the_measure_asked(line):
    text = str(line or "").strip()
    if not text:
        return ""
    text = LEAD.sub("", text)
    text = TAIL.sub("", text)
    text = text.strip(" ?.!,:;-")
    text = LEAD.sub("", text).strip(" ?.!,:;-")
    match = ASKED.fullmatch(text)
    if not match:
        return ""
    return match.group(1).lower()


KEEP_THEIR_TURN = frozenset(("loss", "grief", "safety", "safety_cards", "safety_phrases"))


def _the_card_said_last(memory):
    turns = memory.get("turns")
    if not isinstance(turns, list) or not turns:
        return ""
    last = turns[-1]
    if not isinstance(last, dict):
        return ""
    if str(last.get("module") or "") in KEEP_THEIR_TURN:
        return ""
    said = " ".join(str(last.get("bot") or "").lower().split())
    if not said:
        return ""
    records = memory.get("entry_answers")
    if not isinstance(records, list) or not records:
        records = [memory.get("entry_answer")]
    for record in reversed(records):
        if not isinstance(record, dict):
            continue
        text = str(record.get("text") or "").strip()
        if not text:
            continue
        opening = " ".join(text.lower().split()[:8])
        if said.startswith(opening) or " ".join(text.lower().split()[:5]) in said:
            return text
    return ""


A_NEW_CLAUSE = frozenset("""and so but or which is are was were then because when if that
it they there this these with plus while as""".split())


def _the_clause_that_carries(sentence, pattern=None):
    for boundary in re.finditer(r"[,;:]\s+", sentence):
        rest = sentence[boundary.end():]
        first = (re.split(r"\s+", rest.strip()) or [""])[0].strip(",.;:").lower()
        if first in A_NEW_CLAUSE:
            said = sentence[:boundary.start()].strip()
            if len(said.split()) >= 4:
                return said
    return sentence


def _the_sentence_with(text, measure):
    pattern = MEASURES.get(measure)
    if not pattern:
        return ""
    sentences = [part.strip() for part in SENTENCE.split(text) if part.strip()]
    for sentence in sentences:
        if pattern.search(sentence):
            return _the_clause_that_carries(sentence, pattern)
    return ""


THING_AFTER = re.compile(r"\bhow\s+(?:much|many|often|long|far|hot|deep|big)\s+"
                         r"(?:of\s+)?(?P<thing>[a-z][a-z\\s'&/-]{0,28})\b", re.I)
STOPS_THE_THING = frozenset("""should do can could would shall will did does is are was were
to for before when if after and or but in on at with by the a an my your his her their our
it them that this i we you they""".split())


def _the_thing_the_line_named(memory):
    said = ""
    for turn in reversed(memory.get("turns") or []):
        if isinstance(turn, dict) and str(turn.get("user") or "").strip():
            said = str(turn.get("user") or "")
            break
    match = THING_AFTER.search(said)
    if not match:
        return ""
    words = [word for word in re.split(r"\s+", match.group("thing").strip()) if word]
    kept = []
    for word in words:
        if word.lower().strip(",.;:") in STOPS_THE_THING:
            break
        kept.append(word.strip(",.;:"))
        if len(kept) == 3:
            break
    thing = " ".join(kept).strip(" ,.;:-")
    return thing if thing and thing.lower() not in THING_NOT_WORTH_SAYING else ""


THING_NOT_WORTH_SAYING = frozenset(("it", "that", "this", "them", "there", "one"))


A_CONTAINER = re.compile(r"\b(?:glasses|glass|cups|cup|pints|pint|slices|slice|portions|portion|"
                         r"pieces|piece|sachets|sachet|scoops|scoop|cloves|clove|tins|tin|"
                         r"cans|can|teaspoons|teaspoon|tablespoons|tablespoon|sprays|spray|"
                         r"doses|dose|wipes|wipe|sheets|sheet)\b", re.I)


def _with_the_thing(sentence, thing):
    found = A_CONTAINER.search(sentence)
    if not found:
        return ""
    head = sentence[:found.end()]
    tail = sentence[found.end():]
    return "%s of %s%s" % (head, thing, tail)


def _as_a_headline(thing, sentence):
    first = sentence[0]
    rest = sentence[1:]
    if first.isupper() and rest[:1].islower():
        sentence = first.lower() + rest
    return "%s: %s" % (thing[0].upper() + thing[1:], sentence)


def _as_a_sentence(text):
    if text and text[-1] not in ".!?":
        return text + "."
    return text


def reply_for(text, memory):
    measure = the_measure_asked(text)
    if not measure:
        return None
    card = _the_card_said_last(memory)
    if not card:
        return None
    sentence = _the_sentence_with(card, measure)
    if not sentence:
        return None
    thing = _the_thing_the_line_named(memory)
    if thing and thing.lower() not in sentence.lower():
        said = _with_the_thing(sentence, thing)
        if said:
            return _as_a_sentence(said)
        return _as_a_sentence(_as_a_headline(thing, sentence))
    return _as_a_sentence(sentence)
