import random
import re

A_SURNAME_WORD = re.compile(
    r"\b(?:surname|sur-name|last\s*-?\s*name|family\s*-?\s*name|second\s*-?\s*name)\b", re.I)

SAYS_A_SURNAME = re.compile(
    r"\b(?:(?:my|our|the)\s+)?(?:surname|sur-name|last\s*-?\s*name|family\s*-?\s*name|"
    r"second\s*-?\s*name)\s*(?:is|was|'s|s|:|=)\s*"
    r"(?P<name>[A-Za-z][A-Za-z'\u2019\-]{1,30}(?:\s+[A-Za-z][A-Za-z'\u2019\-]{1,30}){0,3})", re.I)
NAME_PARTS = frozenset("van von der den de da di du dos das del della bin ibn al el la le mc mac "
                       "st saint o o' ap".split())

DESCRIBES_A_NAME = frozenset("""
hard difficult easy long short weird strange common rare unusual foreign hyphenated double
spelled spelt misspelled misspelt mispelled changed change changing wrong right same different
pronounced unpronounceable tricky silly complicated confusing correct incorrect spelled okay ok
also really actually just still not now too boring ugly nice lovely beautiful awful terrible funny
embarrassing stupid odd plain old big small
""".split())

NEVER_A_NAME = frozenset("""
on in at from of for to with about under over after before by into onto near above below
and or but if so that this it there when how why the a an
""".split())

LOWER_PARTS = frozenset("van von der den de da di du dos das del della bin ibn al el la le "
                        "st saint".split())

THE_NAME_WORD = r"(?:surname|sur-name|last\s*-?\s*name|family\s*-?\s*name|second\s*-?\s*name)"
ASKS_THE_SURNAME = tuple(re.compile(pattern, re.I) for pattern in (
    r"\b(?:what|whats|what's|which)\s+(?:is\s+|was\s+|were\s+)?(?:my|our|the)?\s*"
    + THE_NAME_WORD + r"\b",
    r"\b(?:which|what)\s+" + THE_NAME_WORD + r"\s+(?:is|was)\s+(?:mine|ours)\b",
    r"\b(?:do|did|can|could)\s+(?:you|u|ya)\s+(?:still\s+)?(?:know|remember)\s+(?:what\s+)?"
    r"(?:my|our)\s+" + THE_NAME_WORD + r"\b",
    r"\b(?:tell|remind)\s+(?:me|us)\s+(?:what\s+)?(?:my|our)\s+" + THE_NAME_WORD + r"\b",
    r"\b(?:my|our)\s+" + THE_NAME_WORD + r"\s+again\b",
    r"\bwhat\s+(?:did|do)\s+i\s+(?:say|tell\s+you)\s+(?:my|our)\s+" + THE_NAME_WORD + r"\b",
    r"^(?:and\s+|so\s+)?(?:my|our)?\s*" + THE_NAME_WORD + r"\s*\??$",
))
NOT_THE_ASK = re.compile(
    r"\b(?:how|change|changing|changed|deed\s+poll|register|registering|certificate|passport|"
    r"marri(?:ed|age|ying)|divorce|spell|spelt|spelled|pronounce|website|domain|form|online)\b",
    re.I)
THEIR_OWN = re.compile(r"\b(?:my|our|mine|ours|i|we|me)\b", re.I)


def _vary(options, memory):
    turns = memory.get("turns") or []
    recent = {turn.get("bot") for turn in turns[-5:] if isinstance(turn, dict)}
    fresh = [option for option in options if option not in recent] or list(options)
    return random.Random(len(turns)).choice(fresh)


def _the_name_they_said(word):
    parts = " ".join(str(word or "").split()).split()
    if not parts:
        return ""
    written = []
    for index, part in enumerate(parts):
        if part.lower() in LOWER_PARTS and index < len(parts) - 1:
            written.append(part.lower())
        else:
            written.append(part[:1].upper() + part[1:])
    said = " ".join(written)
    return re.sub(r"(['\u2019])([a-z])", lambda m: m.group(1) + m.group(2).upper(), said)


def the_surname(memory):
    held = memory.get("user") if isinstance(memory, dict) else None
    if not isinstance(held, dict):
        return ""
    said = held.get("surname")
    return said.strip() if isinstance(said, str) else ""


def _given_one(text):
    for match in SAYS_A_SURNAME.finditer(str(text or "")):
        name = match.group("name")
        first = name.split()[0]
        low = first.strip().lower()
        if not low or low in DESCRIBES_A_NAME or low in NEVER_A_NAME or len(low) < 2:
            continue
        parts = [first]
        for word in name.split()[1:]:
            if word.lower() in NAME_PARTS or word[:1].isupper() \
                    or (parts[-1].lower() in NAME_PARTS and word.isalpha()):
                parts.append(word)
                continue
            break
        return _the_name_they_said(" ".join(parts))
    return ""


def observe(text, memory):
    if not isinstance(memory, dict) or not isinstance(text, str):
        return False
    said = _given_one(text)
    if not said:
        return False
    held = memory.setdefault("user", {})
    if not isinstance(held, dict):
        return False
    held["surname"] = said
    return True


def _asks_for_it(text):
    said = " ".join(str(text or "").split())
    if not said or not A_SURNAME_WORD.search(said):
        return False
    if len(said.split()) > 12:
        return False
    if NOT_THE_ASK.search(said):
        return False
    return any(pattern.search(said) for pattern in ASKS_THE_SURNAME)


ASKS_THE_FIRST = re.compile(
    r"\b(?:what|whats|what's|which|do|does|did|know|remember|again|tell)\b[^?.!]*"
    r"\b(?:first\s*-?\s*name|given\s*-?\s*name)\b", re.I)
ASKS_THE_FULL = re.compile(
    r"\b(?:what|whats|what's|which|do|does|did|know|remember|again|tell)\b[^?.!]*"
    r"\bfull\s*-?\s*name\b", re.I)


def _the_first_name(memory):
    from . import name as their_name
    return their_name(memory) or ""


def a_note(text, memory):
    said = " ".join(str(text or "").split())
    if not said or not isinstance(memory, dict):
        return None
    match = SAYS_A_SURNAME.match(said)
    if not match or said[match.end():].strip(" .!?,;-"):
        return None
    if not _given_one(said):
        return None
    held = the_surname(memory)
    if not held:
        return None
    return _vary([held + " \u2014 noted.",
                  "Got it \u2014 " + held + ".",
                  held + ", I'll remember that."], memory)


ASKS_AGAIN = re.compile(r"\b(?:what|whats|what's|which|tell|remind|again|said)\b", re.I)
POINTS_BACK = re.compile(r"\b(?:it|that|them|those)\b", re.I)


def _the_lines_before(memory, back=3):
    turns = [turn for turn in (memory.get("turns") or [])
             if isinstance(turn, dict) and str(turn.get("user") or "").strip()]
    return " ".join(str(turn.get("user") or "") + " " + str(turn.get("bot") or "")
                    for turn in turns[-back:]).lower()


def a_follow_up(text, memory):
    said = _plain(text).lower()
    if not said or not the_surname(memory) or len(said.split()) > 7:
        return None
    if NOT_THE_ASK.search(said):
        return None
    if A_SURNAME_WORD.search(said):
        return None
    if not (ASKS_AGAIN.search(said) and POINTS_BACK.search(said)):
        return None
    if not A_SURNAME_WORD.search(_the_lines_before(memory)):
        return None
    held = the_surname(memory)
    return _vary(["It's " + held + ".", held + " \u2014 as you told me.",
                  "Still " + held + "."], memory)


def there_is_a_chat(memory):
    from . import there_is_a_chat as any_chat
    return any_chat(memory)


def reply_for(text, memory):
    if not isinstance(memory, dict):
        return None
    note = a_note(text, memory)
    if note:
        return note
    if not there_is_a_chat(memory):
        return None
    if ASKS_THE_FULL.search(_plain(text)):
        return _the_full_name(memory)
    if ASKS_THE_FIRST.search(_plain(text)):
        return _the_first_name_reply(memory)
    if not _asks_for_it(text):
        return a_follow_up(text, memory)
    if _given_one(text):
        return None
    held = the_surname(memory)
    if not held:
        memory["asked_for"] = "surname"
        return _vary(["You haven't told me your surname yet.",
                      "I don't have it \u2014 you've not said your surname.",
                      "You haven't given me a surname, so I'd only be guessing."], memory)
    return _vary(["It's " + held + ".",
                  held + " \u2014 that's the one you gave me.",
                  "Your surname's " + held + "."], memory)


def _plain(text):
    return " ".join(str(text or "").split())


def _the_full_name(memory):
    first, family = _the_first_name(memory), the_surname(memory)
    if first and family:
        return _vary([first + " " + family + ".", "You're " + first + " " + family + ".",
                      first + " " + family + " \u2014 that's both of the names you gave."], memory)
    if first:
        return "I have your first name, " + first + ", but you haven't given me a surname."
    if family:
        return "I have your surname, " + family + ", but you've not told me your first name."
    memory["asked_for"] = "name"
    return _vary(["You haven't told me your name yet.",
                  "I don't have a name from you \u2014 you've not said."], memory)


def _the_first_name_reply(memory):
    first = _the_first_name(memory)
    if first:
        return _vary([first + " \u2014 you told me.", "It's " + first + ".",
                      "Your first name's " + first + "."], memory)
    memory["asked_for"] = "name"
    return _vary(["You haven't told me your first name yet.",
                  "I don't have it \u2014 you've not said your first name."], memory)
