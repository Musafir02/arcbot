
import re

TASTE = re.compile(
    r"^(?:(?:i|we)\s+)?(?:really\s+|do\s+|just\s+)?"
    r"(?:like|love|enjoy|prefer|am into|'m into|im into|am a fan of|'m a fan of|im a fan of)\s+"
    r"(.+)$"
)
WANTS = re.compile(
    r"^(?:(?:i|we)\s*)?(?:'?m|'?re|am|are)?\s*"
    r"(?:in\s+the\s+mood\s+for|in\s+the\s+humou?r\s+for|keen\s+on|up\s+for|"
    r"in\s+the\s+market\s+for|fancy|fancied|fancying|'?d\s+go\s+for|would\s+go\s+for)\s+(.+)$",
    re.I)
SOMETHING = re.compile(r"^(?:something|anything)\s+(\S.*)$", re.I)
_VAGUE_LEAD = re.compile(r"^(?:something|anything|some|any|a|an|the)\s+", re.I)
_ASKS_SOMETHING = re.compile(r"\?|^(?:what|how|why|when|where|which|who|can|could|should|do|does)\b")
REFUSED = re.compile(
    r"\b(?:not|no|never|none|nope|hate|hates|dislike|dislikes|instead|rather|except|apart|prefer|prefers|"
    r"can'?t stand|cannot stand|stood|sick of|bored of|tired of|over|without|anything but)\b"
)
MEDIUM = (
    ("books", re.compile(r"\b(?:book|books|novel|novels|read|reading|author|paperback)\b")),
    ("films", re.compile(r"\b(?:film|films|movie|movies|watch|watching|series|tv|cinema)\b")),
)
_TITLE = re.compile(r"\*[^*\n]{2,}\*")
_LEAD = re.compile(r"^(?:a|an|the|good|nice|great)\s+")
POINTS_BACK = ("you", "me", "it", "that", "this", "them", "him", "her")
MOST_WORDS = 4


def _offered_choices(reply):
    return len(_TITLE.findall(str(reply or ""))) >= 2


def _said_the_medium(said):
    low = " ".join(str(said or "").lower().split())
    if not low:
        return ""
    best, at = "", None
    for medium, pattern in MEDIUM:
        found = pattern.search(low)
        if found and (at is None or found.start() < at):
            best, at = medium, found.start()
    return best


def _last_turn(memory):
    turns = [t for t in (memory or {}).get("turns") or [] if isinstance(t, dict)]
    if not turns:
        return "", ""
    return str(turns[-1].get("user") or ""), str(turns[-1].get("bot") or "")


def _taste(text):
    said = " ".join(str(text or "").lower().split()).strip(" .,!?")
    if not said or len(said.split()) > 8:
        return ""
    if _ASKS_SOMETHING.search(said):
        return ""
    found = TASTE.match(said) or WANTS.match(said) or SOMETHING.match(said)
    if not found:
        return ""
    taste = found.group(1).strip(" .,!?")
    if REFUSED.search(said):
        return ""
    while _LEAD.match(taste):
        taste = _LEAD.sub("", taste)
    while _VAGUE_LEAD.match(taste):
        taste = _VAGUE_LEAD.sub("", taste)
    words = [w for w in taste.split() if w]
    if not words or len(words) > MOST_WORDS:
        return ""
    for word in words:
        if word in POINTS_BACK:
            return ""
    if _said_the_medium(taste):
        return ""
    return taste


MEDIUM_WORDS = {
    "books": re.compile(r"\b(?:books?|novels?|read(?:ing|s)?|author|paperback|stor(?:y|ies))\b", re.I),
    "films": re.compile(r"\b(?:films?|movies?|watch(?:ing)?|series|tv|cinema|documentar(?:y|ies))\b",
                        re.I),
}


def about_the_medium(answer, memory):
    asked, answered = _last_turn(memory)
    medium = _said_the_medium(asked) or _said_the_medium(answered)
    pattern = MEDIUM_WORDS.get(medium) if medium else None
    if pattern is None:
        return True
    said = str(answer or "")
    return bool(_TITLE.search(said) or pattern.search(said))


def served_already(text, memory):
    taste = _taste(text)
    if not taste:
        return False
    asked, answered = _last_turn(memory)
    return _taste(asked) == taste and _offered_choices(answered)


def follow_up(text, memory):
    taste = _taste(text)
    if not taste:
        return ""
    if served_already(text, memory):
        return ""
    asked, answered = _last_turn(memory)
    if not _offered_choices(answered):
        return ""
    medium = _said_the_medium(asked) or _said_the_medium(answered)
    if not medium:
        return ""
    return "any good " + taste + " " + medium
