import re

from . import pick, verdict

ASK = re.compile(
    r"(?:do|should|shall|must|need|will|would|can|could|have)\s+"
    r"(?:i|we|you)\s+"
    r"(?:(?:need|have|got|want)\s+to\s+|really\s+|actually\s+|even\s+|just\s+)?"
    r"(?:see|ring|call|visit|contact|speak\s+to|talk\s+to|go\s+(?:to|and\s+see)|get\s+seen\s+by|"
    r"book\s+(?:in\s+with|an?\s+appointment\s+with)|get\s+(?:an?\s+)?appointment\s+with)\s+"
    r"(?:somebody|someone|anybody|anyone|a\s+professional|"
    r"a\s+(?:doctor|vet|dentist|nurse|gp|pharmacist|optician|midwife|lawyer|plumber|"
    r"electrician|specialist)|the\s+(?:doctor|vet|dentist|nurse|gp|pharmacist|optician))\b"
    r"\s*[?.!]*$")

A_PERSON = re.compile(
    r"\b(?:your|the|a|an|their|his|her)?\s*"
    r"(vet|doctor|gp|dentist|nurse|pharmacist|optician|midwife|health visitor|paramedic|"
    r"physio(?:therapist)?|practice nurse|a&e|111|999)\b", re.IGNORECASE)

A_PLACE = re.compile(
    r"(?:a&e|the\s+emergency\s+department|walk-?in\s+centre|minor\s+injuries(?:\s+unit)?|"
    r"urgent\s+care|out\s+of\s+hours|999|911|111|112)\b", re.IGNORECASE)

SOMEONE_LINES = (
    "Yes - {person}. {call}",
    "Yes, {person} - {call_lower}",
    "The answer named one: {person}. {call}",
    "Yes: {person}. {call}",
)

PLACE_LINES = (
    "Yes - {call_lower}",
    "{call}",
    "Yes, that one: {call_lower}",
)

ON_THE_PHONE_LINES = (
    "{call}",
    "Yes - {call_lower}",
    "The answer said it plainly: {call_lower}",
)

A_LONG_CALL = 16


def _clean(text):
    return " ".join(str(text or "").lower().split())


def _the_answer_in_hand(memory):
    turns = (memory or {}).get("turns")
    if not turns:
        return ""
    for turn in reversed(turns):
        said = turn.get("bot") if isinstance(turn, dict) else None
        if isinstance(said, str) and said.strip():
            return said
    return ""


A_SIGN_MEANS = re.compile(
    r"\b(?:if|unless|when|whenever|means|would\s+mean|otherwise|in\s+case)\b",
    re.IGNORECASE)
ANYBODY = re.compile(r"\b(?:someone|somebody|anyone|anybody|a\s+professional)\b", re.IGNORECASE)

AN_OBJECT_OF = re.compile(
    r"\b(?:see|ring|call|contact|visit|ask|speak\s+to|talk\s+to|say\s+to|saying\s+to|go\s+to|"
    r"book\s+in\s+with|appointments?\s+with|with|to)\s*$", re.IGNORECASE)

CONDITION_LINES = (
    "Not always. {clause}",
    "It depends. {clause}",
    "Go by this. {clause}",
    "Only if it comes to that. {clause}",
)


def _the_condition(said):
    for sentence in re.split(r"(?<=[.!?]) ", str(said or "")):
        person = A_PERSON.search(sentence) or ANYBODY.search(sentence)
        if not person or not (verdict.NAMES_A_CLINICIAN.search(sentence)
                              or ANYBODY.search(sentence)):
            continue
        if not (A_SIGN_MEANS.search(sentence) or _a_sign_not_a_step(sentence, person)):
            continue
        clause = sentence.strip()
        cut = clause.rfind(", but ")
        if cut > 0 and _a_sign_not_a_step(clause, person):
            clause = clause[cut + len(", but "):]
            clause = clause[:1].upper() + clause[1:]
        return clause
    return ""


def _the_question(said, clause=""):
    for sentence in re.split(r"(?<=[.!?]) ", str(said or "")):
        said_now = sentence.strip()
        if said_now and said_now not in clause and (
                said_now.endswith("?") or "? " in said_now):
            if "?" in said_now:
                return said_now[:said_now.index("?") + 1]
    return ""


def _the_condition_reply(said, memory):
    clause = _the_condition(said)
    if not clause:
        return ""
    written = clause.rstrip(" .") + "."
    reply = pick(CONDITION_LINES, memory, clause).replace("{clause}", written)
    question = _the_question(said, clause)
    if question and question not in reply:
        reply = reply.rstrip() + " " + question
    return reply


A_SUBSET_OF_TIME = re.compile(r"\b(?:that|which|who)\b", re.IGNORECASE)

SAYS_TO_DO = re.compile(r"\b(?:worth|should|needs?|must|ring|call|see|speak|talk|book|get|go|"
                        r"make an appointment|appointment|check(?:ed)?|look(?:ed)? at)\b", re.I)


def _a_sign_not_a_step(said, person):
    if person is None:
        return False
    before = str(said or "")[:person.start()]
    return bool(A_SIGN_MEANS.search(before) or A_SUBSET_OF_TIME.search(before))


def _a_sentence_that_names_someone(said):
    for sentence in re.split(r"(?<=[.!?]) ", str(said or "")):
        if not verdict.NAMES_A_CLINICIAN.search(sentence):
            continue
        if verdict.FENCED_IN_SENTENCE.search(sentence):
            continue
        if _a_sign_not_a_step(sentence, A_PERSON.search(sentence)):
            continue
        if SAYS_TO_DO.search(sentence):
            return sentence
    return ""


def _the_call(said):
    sentence = verdict._the_referral_sentence(said)
    person_in_it = A_PERSON.search(sentence) if sentence else None
    if sentence and (person_in_it is None or _a_sign_not_a_step(sentence, person_in_it)):
        sentence = ""
    if not sentence or verdict._referral(said) is None:
        sentence = _a_sentence_that_names_someone(said)
        if not sentence:
            return "", None
    text = str(sentence).strip()
    call = text
    head = text.split(";")[0].strip()
    if A_PERSON.search(head):
        call = head
    if len(call.split()) > A_LONG_CALL:
        person = A_PERSON.search(call)
        tail = call[person.end():] if person else ""
        breaks = [tail.index(mark) for mark in (",", ":", ";") if mark in tail]
        if breaks:
            call = call[:person.end() + min(breaks)].strip()
    call = call.rstrip(" .;:,")
    if not call or not A_PERSON.search(call):
        return "", None
    return call[0].lower() + call[1:], A_PERSON.search(call)


def reply_for(text, memory):
    if not ASK.match(_clean(text)):
        return None
    said = _the_answer_in_hand(memory)
    if not said:
        return None
    call, person = _the_call(said)
    if not call or person is None:
        return _the_condition_reply(said, memory) or None
    named = " ".join(person.group(0).split())
    on_the_phone = named.strip("the ").lower() in ("999", "911", "111", "112")
    a_place = on_the_phone or bool(A_PLACE.match(named))
    if a_place:
        said_again = call
    elif not AN_OBJECT_OF.search(call[:person.start()]):
        said_again = call
    else:
        after = call[person.end():]
        place = re.match(r"\s*(appointments?|visits?|checks?)\b", after)
        if place:
            noun = place.group(1)
            pronoun = ("an appointment" if noun.startswith("appointment")
                       else "a " + noun.rstrip("s"))
            said_again = (call[:person.start()].rstrip() + " " + pronoun
                          + after[place.end():].rstrip()).strip()
        else:
            said_again = (call[:person.start()].rstrip() + " them "
                          + after.lstrip()).strip()
    pool = ON_THE_PHONE_LINES if on_the_phone else PLACE_LINES if a_place else SOMEONE_LINES
    line = pick(pool, memory, call).replace("{person}", named)
    said_again = said_again[:1].upper() + said_again[1:] + "."
    return line.replace("{call}", said_again).replace("{call_lower}", said_again[:1].lower()
                                                       + said_again[1:])


def replies_to_a_who_to_see(text, memory):
    try:
        return bool(reply_for(text, memory))
    except Exception:
        return False
