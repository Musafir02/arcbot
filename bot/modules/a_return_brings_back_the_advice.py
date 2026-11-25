import re

from ..memory import topics

PRIORITY = 7050

LEADS = (
    "Back to {thing}: {advice}",
    "Back on {thing}: {advice}",
    "On {thing}, then: {advice}",
)

A_RECEIPT = re.compile(
    r"^(?:got it|noted|ok|okay|sure|right|you said|you've told me|you told me|that's right|"
    r"that is right|makes sense|fair enough|understood|"
    r"i'm not sure|i am not sure|that's beyond|that is beyond|no number for that|"
    r"i can't|i cannot|i'd rather not|i would rather not|searching for it|a quick search)\b", re.I)

SUBSTANCE = 6

SENTENCE = re.compile(r"(?<=[.!?])\s+")


def _the_advice(answer):
    text = " ".join(str(answer or "").split())
    if not text:
        return ""
    parts = [part.strip() for part in SENTENCE.split(text) if part.strip()]
    if not parts:
        return ""
    kept = parts[:1]
    if len(parts[0].split()) < 5 and len(parts) > 1:
        kept = parts[:2]
    return " ".join(kept)


def _the_answers_for(memory, topic_text):
    kept = memory.get("entry_answers")
    if not isinstance(kept, list) or not kept:
        kept = [memory.get("entry_answer")]
    turns = memory.get("turns")
    if not isinstance(turns, list):
        return []
    wanted = {form for word in topics.keywords(topic_text)
              for form in (word, topics.stem(word))}
    wanted -= topics.STOPWORDS
    if not wanted:
        return []
    best_score = 0
    found = []
    for record in kept:
        if not isinstance(record, dict):
            continue
        text = str(record.get("text") or "").strip()
        if not text:
            continue
        opening = " ".join(text.lower().split()[:8])
        if not any(isinstance(turn, dict)
                   and " ".join(str(turn.get("bot") or "").lower().split()).startswith(opening)
                   for turn in turns[-topics.ANSWER_KEPT:]):
            continue
        forms = {form for key in set(record.get("keys") or ())
                 for form in (key, topics.stem(key))}
        score = len(wanted & (forms - topics.STOPWORDS))
        if score > best_score:
            best_score, found = score, [text]
        elif score and score == best_score:
            found.append(text)
    return found


def _the_turn_answers_for(memory, topic_text):
    turns = memory.get("turns")
    if not isinstance(turns, list):
        return []
    wanted = {form for word in topics.keywords(topic_text)
              for form in (word, topics.stem(word))}
    wanted -= topics.STOPWORDS
    if not wanted:
        return []
    best_score = 0
    found = []
    for turn in turns:
        if not isinstance(turn, dict):
            continue
        said = str(turn.get("user") or "")
        reply = str(turn.get("bot") or "").strip()
        if not said or not reply:
            continue
        score = len(wanted & {form for word in topics.keywords(said)
                              for form in (word, topics.stem(word))})
        if score > best_score:
            best_score, found = score, [reply]
        elif score and score == best_score:
            found.append(reply)
    return found


def _said_recently(advice, memory):
    opening = " ".join(advice.lower().split()[:6])
    if not opening:
        return False
    turns = memory.get("turns")
    if not isinstance(turns, list):
        return False
    return any(isinstance(turn, dict)
               and " ".join(str(turn.get("bot") or "").lower().split()).startswith(opening)
               for turn in turns[-2:])


def _has_substance(advice):
    if len(advice.split()) < SUBSTANCE:
        return False
    if A_RECEIPT.match(advice):
        return False
    if advice.rstrip().endswith("?"):
        return False
    return True


def _the_return_advice(memory):
    try:
        record = topics.resumed(memory)
        if not isinstance(record, dict) or record.get("asks"):
            return "", ""
        thing = " ".join(str(record.get("asked") or "").split())
        if not thing:
            return "", ""
        topic_text = str(record.get("text") or "")
        advice = ""
        answers = (_the_answers_for(memory, topic_text)
                   + _the_turn_answers_for(memory, topic_text)
                   + [_the_advice(topics.entry_answer(memory, topic_text))])
        for answer in answers:
            short = _the_advice(answer)
            if _has_substance(short) and not _said_recently(short, memory):
                advice = short
                break
    except Exception:
        return "", ""
    if not _has_substance(advice):
        return "", ""
    return thing, advice


def respond(text, memory):
    thing, advice = _the_return_advice(memory)
    if not thing:
        return None
    lead = LEADS[len(memory.get("turns") or []) % len(LEADS)]
    return lead.format(thing=thing, advice=advice)


def CLAIMS_INSTEAD(text, memory):
    thing, advice = _the_return_advice(memory)
    return bool(thing and advice)
