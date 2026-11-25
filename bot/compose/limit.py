import re

PART = re.compile(r"(?<=[.?!;:,])\s+")
CONTINUES = re.compile(r"^(?:and|or|then|but|plus|so|because|with|also|instead|though|which|"
                       r"that|to|for|in|on|at|of)\b", re.I)
COUNTED = re.compile(r"\b(?:all three|all four|all five|all of them|both of them|both|either|"
                     r"any of those|any of them|none of them|three of|the three)\b", re.I)
WORD = re.compile(r"[a-z0-9']*[a-z][a-z0-9']*")
FRAME = re.compile(r"^(?:same as before|same answer(?:, and it covers this)?|as i said|still|"
                   r"that is still the thing to do|nothing new to add on it|"
                   r"nothing more on it(?: i'm afraid)?|that is all i have on it|"
                   r"there is nothing further to add|same again for|it is the same for|"
                   r"same for|the same for|it is the same\b)", re.I)
BACK_REFERENCE = re.compile(r"^(?:the same|this|that|these|those|it|its|it's|they|them|their|"
                            r"both|either|which|such|the latter|the former)\b", re.I)
KEPT = (
    "Right — no {thing}, then. {kept}",
    "Then leave the {thing} out: {kept}",
    "No {thing}, then — {kept}",
    "Fair enough, no {thing}: {kept}",
)
NOTHING_LEFT = (
    "Right — no {thing}, then, and that changes the answer: what would you use instead?",
    "With no {thing} in it there is not much of that answer left — what would you rather use?",
    "Then {thing} out changes it. What should it be instead?",
)
LEAST_KEPT = 20
LEAST_WORDS = 4

RESTATED = re.compile(
    r"^(?:right\s*[-\u2014]\s*no\s+\S[^.]{0,40},\s*then[.\s,:\u2014-]|"
    r"no\s+\S[^.]{0,40},\s*then\s*[-\u2014]|"
    r"then leave the\s+\S[^.]{0,40}\s+out[:,]|"
    r"fair enough, no\s+\S[^.]{0,40}:|"
    r"with no\s+\S[^.]{0,40}\s+in it there is not much|"
    r"then\s+\S[^.]{0,30}\s+out changes it)", re.I)


def restates_the_answer(bot_line):
    return bool(RESTATED.match(str(bot_line or "").strip()))


A_STATE_IS_NOT_A_LIMIT = re.compile(
    r"^(?:feel|feels|felt|feeling|is|are|was|were|be|been|being|seems|seem|seemed|"
    r"i|im|i'm|ive|i've|me|my|we|we're|us)\b", re.I)


def forms_of(thing):
    words = [w for w in WORD.findall(thing.lower()) if w]
    if not words:
        return ()
    out = set()
    for word in words:
        out.add(word)
        if word.endswith("ing") and len(word) > 5:
            stem = word[:-3]
            out.update({stem, stem + "e"})
            if len(stem) > 2 and stem[-1] == stem[-2]:
                out.add(stem[:-1])
        if word.endswith("ies") and len(word) > 4:
            out.add(word[:-3] + "y")
        elif word.endswith("es") and len(word) > 3:
            out.add(word[:-2])
            out.add(word[:-1])
        elif word.endswith("s") and len(word) > 3:
            out.add(word[:-1])
        else:
            out.add(word + "s")
            out.add(word + "es")
    return tuple(sorted(out))


def _carries(part, forms):
    said = set(WORD.findall(part.lower()))
    return any(form in said for form in forms)


def _last_answer(memory):
    turns = memory.get("turns") if isinstance(memory, dict) else None
    if not isinstance(turns, list):
        return ""
    for last in reversed(turns):
        if not isinstance(last, dict):
            return ""
        if str(last.get("module") or "") in ("safety", "loss", "badnews"):
            return ""
        said = str(last.get("bot") or "").strip()
        if said:
            return said
    return ""


def _pick(pool, memory):
    last = _last_answer(memory)
    for line in pool:
        head = line.split("{")[0].strip()
        if head and last and head in last:
            continue
        return line
    return pool[0]


def _take_out(said, forms):
    kept, _dropped = _the_parts_left(said, forms)
    if not kept:
        return ""
    left = _joined(kept)
    if len(left) < LEAST_KEPT or len(left.split()) < LEAST_WORDS:
        return ""
    return left


def steps_left(understood, memory):
    if not isinstance(understood, dict) or not understood.get("constraint"):
        return []
    things = [str(thing).strip() for thing in (understood.get("excludes") or []) if str(thing).strip()]
    said = _last_answer(memory)
    if not things or not said:
        return []
    kept, _dropped = _the_parts_left(said, forms_of(things[0]))
    return [part.strip().rstrip(".,;:") for part in kept
            if part.strip() and not part.strip().endswith(":")]


def _the_parts_left(said, forms):
    parts = [part for part in PART.split(said) if part.strip()]
    kept = []
    dropped = 0
    after_a_colon = False
    for part in parts:
        if not kept and FRAME.match(part.strip()) and not _carries(part, forms):
            dropped += 1
            continue
        if _carries(part, forms) or (dropped and CONTINUES.match(part)) or after_a_colon:
            if kept and kept[-1].rstrip().endswith(":"):
                kept.pop()
            after_a_colon = part.rstrip().endswith(":")
            dropped += 1
            continue
        after_a_colon = False
        if dropped and COUNTED.search(part):
            dropped += 1
            continue
        kept.append(part.strip())
    if not dropped or not kept:
        return [], dropped
    if BACK_REFERENCE.match(kept[0]):
        return [], dropped
    return kept, dropped


def _joined(kept):
    out = []
    for part in kept:
        part = re.sub(r"^(?:and|or|then|but|plus|so|because|also|instead)\s+", "", part, flags=re.I)
        if not part:
            continue
        starts_a_sentence = part[:1].isupper() or part[:1] in "*\"'("
        if out:
            if starts_a_sentence and out[-1][-1] in ",;:":
                out[-1] = out[-1][:-1] + "."
            if out[-1][-1] in ".!?" and part[:1].islower():
                part = part[:1].upper() + part[1:]
        out.append(part)
    left = " ".join(out).rstrip(" ,;:")
    if left and left[-1] not in ".!?":
        left += "."
    if left[:1].islower():
        left = left[:1].upper() + left[1:]
    return left


def _a_fact_put_right(memory):
    if not isinstance(memory, dict):
        return False
    fixed = memory.get("correction")
    return isinstance(fixed, dict) and bool(fixed.get("value"))


NOTHING_THAT_LIMITS = re.compile(
    r"\bnothing\s+(?:with|that|too|but|except|without|involving|containing|featuring|before|"
    r"after|under|over|like)\b")
NO_LAUGH_OR_SCARES = re.compile(
    r"\b(?:no|not|without|except|minus)\s+(?:a\s+|the\s+|any\s+|too\s+|more\s+)?"
    r"(?:laugh\s?track|laughter|laughing|comedy|comedies|jokes?|funny|scares?|scary|horror|"
    r"gore|violence|subtitles|sad\s+ones?|sad\s+films?)\b")


def a_limit_on_the_answer(text):
    said = " " + " ".join(str(text or "").lower().split()) + " "
    return bool(NOTHING_THAT_LIMITS.search(said) or NO_LAUGH_OR_SCARES.search(said))


A_LIMIT_SHAPE = re.compile(
    r"\b(?:nothing|no|not|without|except|minus)\s+(?:with|that|too|more|any|much|a|the)?\s*"
    r"\S")
MISSED_LIMIT = (
    "Leave that out, then - which of those was nearest, and I'll find another in the same vein.",
    "Fair enough, that one's out. Tell me which of those you'd keep and I'll follow the thread.",
    "Then it's out. Which of them came closest, and what would you change about it?",
)


def a_limit_the_reading_missed(clean, memory):
    said = " " + " ".join(str(clean or "").lower().split()) + " "
    if not said.strip():
        return None
    if not A_LIMIT_SHAPE.match(said.strip()) or not a_limit_on_the_answer(said):
        return None
    above = _last_answer(memory)
    if not above or above.rstrip().endswith("?"):
        return None
    return _pick(MISSED_LIMIT, memory)


def reply_for(understood, memory):
    if not isinstance(understood, dict) or not understood.get("constraint"):
        return None
    if _a_fact_put_right(memory):
        return None
    things = [str(t).strip() for t in (understood.get("excludes") or []) if str(t).strip()]
    if not things:
        return None
    said = _last_answer(memory)
    if not said:
        return None
    thing = things[0]
    if A_STATE_IS_NOT_A_LIMIT.match(thing):
        return None
    left = _take_out(said, forms_of(thing))
    if not left:
        if not _carries(said, forms_of(thing)):
            return None
        reply = _pick(NOTHING_LEFT, memory).format(thing=thing)
    else:
        reply = _pick(KEPT, memory).format(thing=thing, kept=left)
    return reply
