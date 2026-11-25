import re

from ..memory import holds as earlier
from ..understanding import understand

from . import pick

EXPERTS = (
    ("health visitor", re.compile(r"\bhealth visitors?\b", re.I),
     ("ring them and they will talk it through with you today",
      "ring them and describe what you have seen: they would rather hear from you than not")),
    ("vet", re.compile(r"\bvets?\b|\bvet's\b|\bveterinary\b", re.I),
     ("ring the practice and say how long it has been going and what you have already tried",
      "book an appointment and take a note of what you have seen and any treatment they are on")),
    ("dentist", re.compile(r"\bdentists?\b|\bhygienist\b|\bdental (?:practice|surgery)\b", re.I),
     ("ring the practice and ask for the earliest appointment",
      "ring the practice and ask for an urgent slot")),
    ("GP", re.compile(r"\bgp\b|\bgp's\b|\bdoctors?\b|\bfamily doctor\b", re.I),
     ("ring the surgery and ask for the earliest appointment",
      "book in and take a note of when it started and what makes it worse")),
    ("physio", re.compile(r"\bphysios?\b|\bphysiotherapist\b", re.I),
     ("you can usually book with one directly, without going through a GP",
      "book an appointment and take a note of when the pain comes on")),
    ("optician", re.compile(r"\bopticians?\b|\boptometrist\b", re.I),
     ("book an eye test, and say if anything has changed suddenly",
      "ring them and say what has changed, and they will say how soon to come in")),
    ("pharmacist", re.compile(r"\bpharmacists?\b|\bchemist\b", re.I),
     ("they can advise today without an appointment",
      "ask at the counter, and take the packet of anything you already take")),
    ("midwife", re.compile(r"\bmidwives?\b|\bmaternity unit\b", re.I),
     ("ring your midwife or the maternity unit and they will say how soon to be seen",
      "ring the maternity unit rather than waiting for the next appointment")),
    ("nurse", re.compile(r"\bpractice nurse\b|\bnurse\b", re.I),
     ("ring the surgery and ask whether the practice nurse can see you",
      "ask at the desk for the practice nurse")),
)

LEAD = {
    "health visitor": "Your health visitor",
    "vet": "A vet",
    "dentist": "A dentist",
    "GP": "Your GP",
    "physio": "A physio",
    "optician": "An optician",
    "pharmacist": "A pharmacist",
    "midwife": "Your midwife",
    "nurse": "The practice nurse",
}

WHO_ASK = re.compile(
    r"^(?:(?:and|so|ok|okay|but|right|then|well)\s+)*"
    r"(?:"
    r"who\s+(?:should|shall|do|can|could|would|must|might|am\s+i)\s+(?:i|we)\s+"
    r"(?:see|call|ring|contact|ask|book|speak\s+to|talk\s+to|go\s+and\s+see|go\s+to|"
    r"get\s+in\s+touch\s+with|be\s+seeing|need\s+to\s+see)"
    r"|who\s+(?:to\s+(?:see|call|ring|ask|contact|speak\s+to|talk\s+to))"
    r"|who\s+do\s+i\s+need\s+to\s+(?:see|call)"
    r"|which\s+(?:doctor|dentist|vet|specialist|professional|person|one)\s+"
    r"(?:should|do|would)\s+i\s+(?:see|call|ring|go\s+to)"
    r"|where\s+do\s+i\s+go\s+for\s+(?:it|that|this)"
    r")"
    r"(?:\s+(?:about|for|with)\s+(?:it|that|this|them|someone))?"
    r"(?:\s+(?:then|now|instead|first|please|again|next))?"
    r"[\s,.!?]*$",
    re.I,
)

PREAMBLE = re.compile(r"(?:,\s*(?:and|but|so)\s+|;\s*|\.\s+)", re.I)

EARLY = 45

BY_TOPIC = (
    ("pets", "vet"),
    ("health", "GP"),
    ("feelings", "GP"),
)

THREAD = (
    ("dentist", re.compile(r"\btooth\b|\bteeth\b|\bgums?\b|\bdental\b|\bdentist\b|\bmolar\b|"
                           r"\babscess\b|\bbraces?\b", re.I)),
    ("optician", re.compile(r"\beyes?\b|\beyesight\b|\bvision\b|\boptician\b|\bblurry\b|"
                            r"\bblurred\b|\bcontact lenses?\b", re.I)),
    ("midwife", re.compile(r"\bpregnan|\bmidwife\b|\bmaternity\b|\bunborn\b", re.I)),
)

QUIET = frozenset(("safety", "urgent", "grief", "loss"))

CARE_TOPICS = frozenset(("health", "feelings", "family-and-parenting"))


def _flat(text):
    text = str(text or "").strip().lower()
    text = text.replace("\u2019", "'").replace("\u2018", "'")
    return re.sub(r"\s+", " ", text)


def asks_who(text):
    return bool(WHO_ASK.match(_flat(text).strip(" .!?")))


def _last_module(memory):
    return earlier.last_module(memory)


def _last_reply(memory):
    return earlier.last_reply(memory)


def _names_no_subject(line):
    if asks_who(line):
        return True
    read = understand(_flat(line), {})
    return not [word for word in (read.get("keywords") or []) if len(word) > 2]


def _the_subject(memory):
    turns = memory.get("turns") if isinstance(memory, dict) else None
    if not isinstance(turns, list) or not turns:
        return None
    for index in range(len(turns) - 1, -1, -1):
        turn = turns[index]
        if not isinstance(turn, dict):
            continue
        line = str(turn.get("user") or "")
        if not line or _names_no_subject(line):
            continue
        return index, str(turn.get("bot") or ""), line
    return None


def _thread_text(memory, answer=""):
    said = [answer]
    for turn in earlier.turns(memory)[-3:]:
        if not isinstance(turn, dict):
            continue
        said.append(str(turn.get("user") or ""))
    return " ".join(part for part in said if part)


def _sentence_at(text, at):
    begin = 0
    for found in re.finditer(r"(?<=[.!?]) ", text):
        if found.start() >= at:
            return text[begin:found.start()], begin
        begin = found.end()
    return text[begin:], begin


def _person_in(said):
    best = None
    for name, words, _way in EXPERTS:
        found = words.search(said)
        if not found:
            continue
        if best is not None and found.start() >= best[3]:
            continue
        sentence, start = _sentence_at(said, found.start())
        best = (name, sentence, max(0, found.start() - start), found.start())
    if best is None:
        return None
    return best[0], best[1], best[2]


def _cut_the_preamble(sentence, at):
    start = 0
    for found in PREAMBLE.finditer(sentence):
        if found.end() > at:
            break
        if at - found.end() <= 80:
            start = found.end()
    return sentence[start:].strip(), start


def _tidy(clause):
    clause = clause.strip().strip('"').strip().rstrip(" ,;:")
    if clause and not clause.endswith((".", "!", "?")):
        clause += "."
    if clause[:1].islower():
        clause = clause[0].upper() + clause[1:]
    return clause


def _lead_of(name):
    return LEAD.get(name, name)


def _the_way_in(name, memory, said, clause=""):
    ways = ()
    for other, _words, options in EXPERTS:
        if other == name:
            ways = options
    if not ways:
        return ""
    said_flat = _flat(clause)
    fresh = [way for way in ways if not _says_it_again(way, said_flat)]
    return pick(fresh or list(ways), memory, said)


def _says_it_again(way, said):
    words = _flat(way).split()
    for at in range(0, max(0, len(words) - 2)):
        if " ".join(words[at:at + 3]) in said:
            return True
    return False


def _person_for_the_topic(memory, said="", subject=""):
    read = memory.get("understood") if isinstance(memory, dict) else None
    topics = []
    if isinstance(read, dict):
        topics = [str(t).lower() for t in (read.get("topics") or [])]
        one = str(read.get("topic") or "").lower()
        if one:
            topics.append(one)
    if subject:
        theirs = understand(_flat(subject), {})
        if isinstance(theirs, dict) and theirs.get("topics"):
            topics = [str(t).lower() for t in theirs["topics"]]
    care = [topic for topic in topics if topic in CARE_TOPICS]
    if care:
        thread = _thread_text(memory, said)
        for name, words in THREAD:
            if words.search(thread):
                return name
    for topic, name in BY_TOPIC:
        if topic in topics:
            return name
    return ""


def _from_the_answer(name, sentence, at, memory, said, repeat=True):
    clause, start = _cut_the_preamble(sentence, at)
    way = _the_way_in(name, memory, said, clause)
    if not way:
        return None
    if repeat and at - start <= EARLY:
        body = _tidy(clause)
        if way and not _says_it_again(way, _flat(body)):
            body = body + " " + way[0].upper() + way[1:] + "."
        return body
    return _lead_of(name) + ": " + way + "."


def reply_for(text, memory):
    memory = memory if isinstance(memory, dict) else {}
    if not asks_who(text):
        return None
    if _last_module(memory) in QUIET:
        return None
    answer = _last_reply(memory)
    if not answer:
        return None
    found = _person_in(answer)
    if found:
        reply = _from_the_answer(*found, memory=memory, said=text)
        if reply:
            return reply
    subject = _the_subject(memory)
    turns = memory.get("turns") or []
    if subject and subject[1] and subject[0] != len(turns) - 1:
        found = _person_in(subject[1])
        if found:
            reply = _from_the_answer(*found, memory=memory, said=text, repeat=False)
            if reply:
                return reply
    name = _person_for_the_topic(memory, text, subject[2] if subject else "")
    if not name:
        return None
    way = _the_way_in(name, memory, text)
    if not way:
        return None
    return _lead_of(name) + ": " + way + "."


def takes_as_it_comes(text, memory):
    try:
        return reply_for(text, memory) is not None
    except Exception:
        return False


TAKES_AS_IT_COMES = takes_as_it_comes
