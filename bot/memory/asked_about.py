import re

from . import topics

SENTENCE = re.compile(r"(?<=[.!?])\s+")

RETURN = (
    "Back to {thing}: {reply}",
    "Back to {thing} then: {reply}",
    "It is the same answer on {thing}: {reply}",
    "As before on {thing}: {reply}",
)

RETURN_UNNAMED = (
    "Back to what I said: {reply}",
    "It is the same answer as before: {reply}",
    "As before: {reply}",
    "Back to it: {reply}",
)

SHORT = 5

MOST = 45


def _sentences(answer):
    return [one.strip() for one in SENTENCE.split(str(answer or "").strip()) if one.strip()]


_NOT_A_THING = frozenset("""
what which who whom whose how when where why whether whats
now then again left else next other same other another anything something nothing everything
please thanks ok okay well so and but
""".split())


def _the_words_asked(text):
    out = []
    for word in topics.keywords(text):
        if word in topics.ASK_ONLY or word in _NOT_A_THING or word in out:
            continue
        out.append(word)
    return out


_A_CONTINUATION = re.compile(
    r"^(?:if|and|or|but|so|then|also|because|when|while|though|although|plus|that said)\b", re.I)


def _the_part_that_answers(answer, wanted, said_before):
    parts = _sentences(answer)
    if not parts:
        return ""
    scored = []
    for index, part in enumerate(parts):
        here = {topics.stem(word) for word in topics.keywords(part)}
        score = len(here & set(wanted))
        stands = 0 if _A_CONTINUATION.match(part) else 1
        scored.append((score, stands, index))
    scored.sort(key=lambda triple: (-triple[0], -triple[1], triple[2]))
    best = scored[0]
    if best[0] and best[1]:
        index = best[2]
    elif best[0]:
        index = next((i for i, part in enumerate(parts) if not _A_CONTINUATION.match(part)), best[2])
    else:
        return ""
    out = parts[index]
    if len(out.split()) < SHORT and index + 1 < len(parts):
        out = out + " " + parts[index + 1]
    if len(out.split()) > MOST:
        out = " ".join(out.split()[:MOST]).rstrip(" ,;:") + "."
    flat_before = " ".join(str(said_before or "").lower().split())
    if flat_before and " ".join(out.lower().split())[:60] in flat_before:
        return ""
    return out


def the_answer_this_chat_gave(text, memory):
    if not isinstance(memory, dict):
        return None
    wanted = _the_words_asked(text)
    if not wanted:
        return None
    answer = topics.answer_about(text, memory)
    if not answer:
        return None
    turns = [turn for turn in (memory.get("turns") or []) if isinstance(turn, dict)]
    said_before = str(turns[-1].get("bot") or "") if turns else ""
    part = _the_part_that_answers(answer, wanted, said_before)
    if not part:
        return None
    said = " ".join(part.lower().split())
    just_said = " ".join(str(turns[-1].get("bot") or "").lower().split()) if turns else ""
    if said[:60] and said[:60] in just_said:
        return None
    frame = RETURN[len(turns) % len(RETURN)] if len(wanted) == 1 else RETURN_UNNAMED[
        len(turns) % len(RETURN_UNNAMED)]
    return frame.format(thing=wanted[0], reply=part)
