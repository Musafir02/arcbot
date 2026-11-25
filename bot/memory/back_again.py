
import random
import re

from . import facts, history, topics

AFTER_BACK = re.compile(
    r"^(?:\s*(?:again|already|now|too|so soon|as well|for the (?:\w+ )?time|"
    r"and (?:its|it is|its worse|worse|its back|the \w+ is|its the same|same as before)|"
    r"its worse|it is worse|worse than (?:before|last time)|same as before))*\s*[.!]*$", re.I)

PRONOUN_BACK = re.compile(
    r"^(?:and|so|well|oh|ok|okay|right)?\s*(?:its|it's|it is|theyre|they're|they are|"
    r"thats|that's|that is|these are|those are)\s+(?:come\s+|came\s+)?back\b(?P<tail>.*)$",
    re.I)

VERB_BACK = re.compile(
    r"^(?:(?P<cop>is|are|was|were|s|'s|has|have|had)\s+(?:come\s+)?back|"
    r"(?P<main>came|come|comes|returned|returns)\s+back|(?P<alone>returned|returns))"
    r"\b(?P<tail>.*)$", re.I)

DETERMINERS = ("the", "my", "our", "his", "her", "their", "this", "that")

BARE_BACK = re.compile(r"^(?:and|so|well|oh|ok|okay)?\s*back (?:again|already|now)\s*[.!]*$", re.I)

A_PERSON_OR_PET = re.compile(
    r"\b(?:" + "|".join(sorted(facts.RELATIONS)) + r"|dog|puppy|cat|kitten|rabbit|hamster|"
    r"parrot|goldfish|horse|tortoise|guinea)\b", re.I)

NAMED = (
    "{The thing}, back again - did {they} pass at all in between, or {has} {they} just been quiet?",
    "{The thing} came back. Same as before, or worse this time?",
    "{The thing} again. What did you do for {them} the first time, and how long did that hold?",
    "{The thing} being back usually means whatever set it off is still there - has anything "
    "changed since?",
)

UNNAMED = (
    "Back again - did it pass at all in between, or has it been there under the surface?",
    "So it eased off and came back. Is it the same as before, or worse this time?",
    "Back so soon. What did you do for it the first time, and how long did that hold?",
    "Something coming back usually means whatever set it off is still there - has anything "
    "changed since?",
)


AWAY_FROM_HOME = re.compile(
    r"\b(?:is|was|are|were|been|being|stayed|sent|took|taken|gone|went|dropped|left)\s+"
    r"(?:at|in|to|with|into|off to|round to)\s+(?:the|a|an|my|our|his|her|their|its)\b|"
    r"\b(?:came out|came round|coming out|booked in|in for a service|"
    r"getting (?:fixed|repaired|serviced|cleaned|mended|done))\b", re.I)

A_SYMPTOM = re.compile(
    r"\b(?:noise|noisy|banging|rumbling|knocking|squeaking|whistling|rattling|humming|buzzing|"
    r"grinding|clicking|dripping|hissing|scraping|leak|leaking|damp|mould|"
    r"mold|smell|smells|reek|sore|ache|aches|aching|pain|painful|hurts?|hurting|bleeding|rash|"
    r"cough|fever|swollen|broken|cracked|fault|faulty|stuck|jammed|stopped working|"
    r"not working|isnt working|wont work|wont start|slugs?|mice|rats|ants|flies|aphids|weeds?|"
    r"worse|chest|throat|head|stomach|back|knee|shoulder|ankle|ear|tooth|toothache)\b", re.I)


def _the_earlier_line(memory, thing, text=""):
    wanted = topics.keywords(thing) if thing else []
    record = topics.current(memory)
    words = list(wanted) or list((record or {}).get("words") or [])
    if not words:
        return ""
    now = " ".join(str(text or "").lower().split())
    for turn in reversed(list(memory.get("turns") or [])):
        if not isinstance(turn, dict):
            continue
        line = str(turn.get("user") or "")
        if " ".join(line.lower().split()) == now:
            continue
        have = topics.keywords(line)
        if any(topics.alike(word, other) for word in words for other in have):
            return line
    return ""


def _the_thing_went_away(memory, thing, text=""):
    earlier = _the_earlier_line(memory, thing, text)
    if not earlier:
        return False
    if A_SYMPTOM.search(earlier):
        return False
    return bool(AWAY_FROM_HOME.search(earlier))


def _the_words(plural):
    if plural:
        return {"they": "they", "them": "them", "has": "have"}
    return {"they": "it", "them": "it", "has": "has"}


def _filled(line, thing, plural):
    words = _the_words(plural)
    if thing:
        words["the thing"] = thing[0].upper() + thing[1:]
    else:
        words["the thing"] = "It"
    out = line
    for key, value in words.items():
        out = out.replace("{" + key + "}", value)
        out = out.replace("{" + key[0].upper() + key[1:] + "}", value[0].upper() + value[1:])
    if thing:
        return out
    return out[0].upper() + out[1:]


def _an_earlier_topic(memory, thing):
    wanted = topics.keywords(thing)
    if not wanted:
        return False
    here = len(memory.get("turns") or [])
    for record in reversed(memory.get("topics") or []):
        if record.get("turn") == here:
            continue
        have = record.get("words") or []
        if any(topics.alike(word, other) for word in wanted for other in have):
            return True
    return False


def _from_this_line(record, memory):
    return record.get("turn") == len(memory.get("turns") or [])


def _the_thing(text, memory):
    line = " ".join(str(text or "").lower().split())
    if not line or "?" in line:
        return None
    words = line.split()
    if words and words[0] in ("and", "so", "well", "oh", "ok", "okay", "right"):
        words = words[1:]
    found = []
    numbers = {}
    if words and words[0] in DETERMINERS:
        for count in range(min(3, len(words) - 1), 0, -1):
            thing = " ".join(words[:count])
            said = VERB_BACK.match(" ".join(words[count:]))
            if not said or not AFTER_BACK.match(said.group("tail") or ""):
                continue
            if A_PERSON_OR_PET.search(thing):
                return None
            if not _an_earlier_topic(memory, thing):
                continue
            if said.group("cop"):
                found.append((0, -count, thing))
            else:
                found.append((1, -count, thing))
            if said.group("cop"):
                number = said.group("cop").lower() in ("are", "were", "have")
            else:
                number = thing.split()[-1].endswith("s")
            numbers[thing] = number
        if found:
            found.sort()
            thing = found[0][2]
            return thing, numbers[thing]
        return None
    spoken = PRONOUN_BACK.match(line)
    if spoken:
        if not AFTER_BACK.match(spoken.group("tail") or ""):
            return None
        record = topics.current(memory)
        if not record or _from_this_line(record, memory):
            return None
        if A_PERSON_OR_PET.search(" ".join(record.get("words") or [])):
            return None
        plural = line.startswith(("theyre", "they're", "they are", "these", "those"))
        return None, plural
    if BARE_BACK.match(line):
        record = topics.current(memory)
        if not record or _from_this_line(record, memory):
            return None
        return None, False
    return None


def reply_for(text, memory):
    if not history.an_earlier_turn(memory, text):
        return None
    found = _the_thing(text, memory)
    if not found:
        return None
    thing, plural = found
    if _the_thing_went_away(memory, thing, text):
        return None
    line = random.choice(NAMED if thing else UNNAMED)
    return _filled(line, thing, plural)
