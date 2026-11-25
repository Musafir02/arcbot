import re

PRIORITY = 6900

LEAD = r"^(?:and |so |but |also |oh |ok |okay )?"

DID_WITH = re.compile(LEAD + r"(?:what|which) (?P<thing>[a-z][a-z' ]{1,24}?)\s*"
                      r"(?:did i|have i)\s+"
                      r"(?!said?\b|tell\b|told\b|mention\b|mentioning\b)(?P<did>[a-z]+)"
                      r"\s*[?.!]*$")

WAS_IT_I = re.compile(LEAD + r"which (?P<thing>[a-z][a-z' ]{1,24}?)\s*"
                      r"(?:was it|is it|was that)\s+(?:that\s+)?i\s+"
                      r"(?!said?\b|tell\b|told\b|mention\b)(?P<did>[a-z]+)\s*[?.!]*$")

ATTRIBUTE = frozenset("""size colour color brand make model number price cost amount weight
length width height age year month day date time""".split())

NOT_A_THING = frozenset("""one thing things bit bits part parts point way kind sort time other
else lot lots""".split())


def _thing(low):
    for pattern in (WAS_IT_I, DID_WITH):
        match = pattern.match(low)
        if not match:
            continue
        words = [word for word in match.group("thing").split() if word]
        while len(words) > 1 and words[0] in ATTRIBUTE:
            words = words[1:]
        thing = " ".join(words).strip()
        if not thing or thing in ATTRIBUTE or thing in NOT_A_THING:
            return ""
        return thing
    return ""


def _did(low):
    for pattern in (WAS_IT_I, DID_WITH):
        match = pattern.match(low)
        if match:
            return match.group("did")
    return ""


def _stem(word):
    word = str(word or "").lower().strip("'")
    for suffix in ("ing", "ed", "es", "s"):
        if len(word) > len(suffix) + 3 and word.endswith(suffix):
            return word[:-len(suffix)]
    return word


def _says_it(tokens, thing):
    stems = {_stem(token) for token in tokens}
    return all(_stem(word) in stems for word in thing.split())


def _the_line(thing, did, memory):
    turns = (memory or {}).get("turns") if isinstance(memory, dict) else None
    lines = []
    for turn in reversed(turns or []):
        line = str((turn or {}).get("user") or "").strip()
        if not line:
            continue
        if not _says_it(re.findall(r"[a-z']+", line.lower()), thing):
            continue
        if line.endswith("?") or _thing(" ".join(line.lower().split())):
            continue
        lines.append(line)
    if not lines:
        return ""
    doing = _stem(did)
    for line in lines:
        tokens = {_stem(token) for token in re.findall(r"[a-z']+", line.lower())}
        if doing in tokens:
            return line
    return lines[0]


def _times_said(line, memory):
    turns = (memory or {}).get("turns") if isinstance(memory, dict) else None
    said = line.lower()
    return sum(1 for turn in (turns or [])[-4:]
               if said in str((turn or {}).get("bot") or "").lower())


def _the_recall(text, memory):
    low = " ".join(str(text or "").lower().split())
    if not low:
        return None
    thing = _thing(low)
    if not thing:
        return None
    line = _the_line(thing, _did(low), memory)
    if not line:
        return None
    quoted = '"' + line + '"'
    times = _times_said(line, memory)
    if times:
        return ("Still the same one: ", "Same line again: ")[times % 2] + quoted
    return "You said: " + quoted


def takes_as_it_comes(text, memory):
    return _the_recall(text, memory) is not None


TAKES_AS_IT_COMES = takes_as_it_comes


def respond(text, memory):
    from . import memory_store
    low = " ".join(str(text or "").lower().split()).strip(" ,.;:!?")
    if memory_store.respond(low, memory):
        return None
    return _the_recall(text, memory)
