import re

from . import topics

FILLER = re.compile(r"^(?:(?:so|and|but|ok|okay|well|right|ah|oh|hmm|then|now|also|please)\b"
                    r"[\s,]+)*")

NOTHING_NAMED = re.compile(
    r"^(?:"
    r"(?:what|which)\s+(?:(?:else|kind|sort)\s+)*(?:can|could|should|may|shall|would)\s+(?:i|we)\s+"
    r"(?:take|use|have)\b"
    r"|(?:is\s+there\s+)?(?:anything|something)\s+(?:else\s+)?(?:that\s+)?(?:i|we)\s+"
    r"(?:can|could|should|may)\s+(?:take|use|have)\b"
    r"|(?:what|which)\s+is\s+(?:safe|ok|okay|best)\s+to\s+(?:take|use)\b"
    r")"
    r"(?:\s+for\s+(?:it|this|that|them|those|the pain|the ache|the soreness|the hurt|"
    r"any of it|any of that|any of those|the same))?"
    r"[\s!.,?]*$", re.I)

TRIP = re.compile(r"\b(?:flight|flights|flying|plane|airport|holiday|holidays|trip|travel|"
                  r"abroad|away|luggage|suitcase|bag|bags|hand luggage|carry on|packing|packed|"
                  r"passport|camping|campsite|hotel|ferry|cruise)\b", re.I)

THEIRS = re.compile(r"\b(?:i|im|i'm|ive|i've|id|i'd|my|me|we|we're|weve|our|us)\b", re.I)

NOT_A_THING = frozenset("""
ache aching bad badly better bit constantly really still sore tender terrible awful worse worst
keep keeps keeping get gets getting got gotten feel feels feeling felt hurt hurts hurting kill
kills killing make makes making made go goes going gone come comes coming give gives giving put
wont wont sleep sleeping woke wake waking too very lot lots much many every always sometimes
again anymore either though bother bothering last night morning evening day days week weeks
month months hour hours while since thing things stuff
""".split())

A_FORM_OF_A_VERB = re.compile(r"^(?:[a-z]{3,})(?:ing|ed)$")

FORMULAS = ("what can i take for %s", "what can i take for %s pain")

PAINKILLER_ASKS = ("what painkiller can i take",)

IN_PAIN = re.compile(r"\b(?:pain|pains|ache|aches|aching|achy|hurts?|hurting|sore|throbbing|"
                     r"killing|agony|stinging|burning|tender)\b", re.I)

FEEDING = re.compile(r"\b(?:breastfeeding|breast feeding|breastfeed|nursing|expressing|pumping)\b",
                     re.I)
PREGNANT = re.compile(r"\b(?:pregnan\w*|expecting|trimester|weeks gone|weeks along|midwife)\b",
                      re.I)
A_SENTENCE = re.compile(r"[^.!?]+(?:[.!?]+|$)")

A_CARD_IS_LONG = 120

THE_SUBJECTS_A_CHAT_HAS = 2
THE_WORDS_A_SUBJECT_HAS = 2
THE_ASKS_A_LINE_MAKES = 3


def _flat(text):
    return " ".join(str(text or "").split())


def _asks_what_to_take(text):
    said = FILLER.sub("", _flat(text).lower()).strip()
    if not said or not NOTHING_NAMED.match(said):
        return False
    return True


def _complaint_words():
    words = set()
    try:
        from ..knowledge import body
        words.update(body.HURT)
        words.update(body._SORE_ANYWHERE)
    except Exception:
        pass
    words.update("""
        heartburn indigestion reflux nausea migraine headache toothache earache backache stomachache
        cough coughing cold flu covid temperature fever cystitis thrush hayfever rash hives eczema
        psoriasis dandruff ulcer blister sunburn burn sprain cramp cramping constipation diarrhoea
        diarrea sick vomiting warts verruca sciatica gout arthritis ibs period swollen swelling
        infected infection throat tooth teeth gum gums ear ears stomach tummy belly chest queasy
        nauseous vomit vomiting dizzy faint fainted bleeding rash pregnancy pregnant
        """.split())
    return frozenset(word for word in words if word)


COMPLAINT = None
NOT_THEIRS = None


def _someone_else():
    try:
        from ..knowledge import body
        phrases = sorted(body.THIRD_PARTY, key=len, reverse=True)
        return re.compile(r"\b(?:" + "|".join(re.escape(phrase) for phrase in phrases) + r")\b",
                          re.I)
    except Exception:
        return None


def _a_complaint(subject):
    global COMPLAINT, NOT_THEIRS
    if COMPLAINT is None:
        COMPLAINT = re.compile(
            r"\b(?:" + "|".join(re.escape(word) for word in
                               sorted(_complaint_words(), key=len, reverse=True)) + r")\b", re.I)
        NOT_THEIRS = _someone_else()
    said = _flat(subject)
    if NOT_THEIRS is not None and NOT_THEIRS.search(said):
        return False
    return bool(COMPLAINT.search(said))


def _subjects(memory):
    if not isinstance(memory, dict):
        return []
    seen, out = [], []
    record = memory.get("topic")
    if isinstance(record, dict):
        seen.append(record)
    others = memory.get("topics")
    if isinstance(others, list):
        seen.extend(other for other in reversed(others) if isinstance(other, dict))
    for other in seen:
        said = _flat(other.get("text"))
        if said and said not in out:
            out.append(said)
    return out[:THE_SUBJECTS_A_CHAT_HAS]


def _the_things_to_take_for(subject):
    words = []
    for word in topics.keywords(subject):
        if len(word) < 3 or word in NOT_A_THING or not re.match(r"^[a-z]+$", word):
            continue
        if A_FORM_OF_A_VERB.match(word):
            word = word[:-3] if word.endswith("ing") else word[:-2]
            if len(word) > 3 and word[-1] == word[-2]:
                word = word[:-1]
            if len(word) < 3 or word in NOT_A_THING:
                continue
        if word not in words:
            words.append(word)
    return words[:THE_WORDS_A_SUBJECT_HAS]


def _a_trip_above(memory, text):
    if TRIP.search(_flat(text)):
        return True
    if not isinstance(memory, dict):
        return False
    turns = [turn for turn in (memory.get("turns") or []) if isinstance(turn, dict)]
    return any(TRIP.search(_flat(turn.get("user"))) for turn in turns[-2:])


def _the_answer(text, memory):
    from ..modules import answers

    fresh = {"turns": [], "aside": True}
    for key in ("user", "others", "facts_log"):
        if key in memory:
            fresh[key] = memory[key]
    try:
        return answers.respond(text, fresh) or ""
    except Exception:
        return ""


def _the_said_in_the_chat(memory):
    if not isinstance(memory, dict):
        return ""
    turns = [turn for turn in (memory.get("turns") or []) if isinstance(turn, dict)]
    return " ".join(_flat(turn.get("user")) for turn in turns)


def _the_last_reply(memory):
    if not isinstance(memory, dict):
        return ""
    turns = [turn for turn in (memory.get("turns") or []) if isinstance(turn, dict)]
    return _flat(turns[-1].get("bot")) if turns else ""


def _the_situation_this_chat_is_in(reply, memory):
    said = _the_said_in_the_chat(memory)
    if FEEDING.search(said) or not PREGNANT.search(said) or not FEEDING.search(reply):
        return reply
    kept = [sentence for sentence in A_SENTENCE.findall(reply) if not FEEDING.search(sentence)]
    if not kept or len(kept) == len(A_SENTENCE.findall(reply)):
        return reply
    return " ".join(" ".join(kept).split())


def _the_answer_today(text, memory):
    from ..modules import answers

    try:
        return answers.respond(text, dict(memory) if isinstance(memory, dict) else {}) or ""
    except Exception:
        return ""


def _the_same_answer(reply, text, memory, today):
    if not today:
        today.append(_the_answer_today(text, memory))
    return _flat(today[0]) == _flat(reply) and len(_the_last_reply(memory)) >= A_CARD_IS_LONG


def _names(reply, word):
    said = _flat(reply).lower()
    if not said:
        return False
    for other in re.findall(r"[a-z']+", said):
        if other == word or topics.alike(other, word):
            return True
    return False


def _the_answer_above(reply, memory):
    if not isinstance(memory, dict):
        return False
    turns = [turn for turn in (memory.get("turns") or []) if isinstance(turn, dict)]
    if not turns:
        return False
    opening = " ".join(_flat(reply).lower().split()[:10])
    if not opening:
        return False
    return opening in _flat(turns[-1].get("bot")).lower()


def _the_subjects_to_answer(memory, text):
    out = []
    for subject in _subjects(memory):
        if not THEIRS.search(subject) or "?" in subject:
            continue
        if not _a_complaint(subject):
            continue
        words = _the_things_to_take_for(subject)
        if words:
            out.append((subject, words))
    return out


def the_ask_and_the_subject(text, memory):
    try:
        if not _asks_what_to_take(text):
            return False
        if _a_trip_above(memory, text):
            return False
        return bool(_the_subjects_to_answer(memory, text))
    except Exception:
        return False


def reply_for(text, memory):
    if not _asks_what_to_take(text):
        return ""
    if _a_trip_above(memory, text):
        return ""
    asked = 0
    today = []
    already = ""
    in_pain = ""
    for subject in _subjects(memory):
        if not THEIRS.search(subject) or "?" in subject:
            continue
        if not _a_complaint(subject):
            continue
        for word in _the_things_to_take_for(subject):
            for formula in FORMULAS:
                if asked >= THE_ASKS_A_LINE_MAKES:
                    return ""
                asked += 1
                reply = _the_answer(formula % word, memory)
                if not reply or not _names(reply, word):
                    continue
                if _the_answer_above(reply, memory):
                    if not already:
                        already = reply
                        in_pain = subject
                    continue
                if _the_same_answer(reply, text, memory, today):
                    continue
                return _the_situation_this_chat_is_in(reply, memory)
    if in_pain and IN_PAIN.search(in_pain):
        reply = _the_answer(PAINKILLER_ASKS[0], memory)
        if (reply and not _the_answer_above(reply, memory)
                and not _the_same_answer(reply, text, memory, today)):
            return reply
    if already and _the_same_answer(already, text, memory, today):
        return ""
    return already
