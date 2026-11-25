import random
import re

from ..memory import history

NEGATORS = frozenset((
    "not", "no", "never", "hardly", "barely", "nothing", "without", "cant", "cannot", "dont",
    "doesnt", "didnt", "isnt", "wasnt", "arent", "werent", "wont", "wouldnt", "couldnt",
    "shouldnt", "havent", "hasnt", "aint",
))

NEARLY = frozenset(("nearly", "almost"))
SAYS_IT_HAS_LINGERED = re.compile(
    r"\b(?:wont|won'?t|not)\s+(?:go|shift|clear|budge|settle)\w*|"
    r"\bfor\s+(?:\d+|a\s+couple\s+of|a\s+few|a|an|two|three|four|five|six|seven|eight|nine|"
    r"ten)\s+(?:days?|weeks?|months?|years?)\b|\b(?:been going|going on|dragging on)\b", re.I)
STILL_AT_IT = re.compile(r"\bstill\b", re.I)


_SHORT_RUN = re.compile(r"\b(?:(?:one|two|a\s+couple\s+of)\s+days?|day\s+(?:one|two|three|1|2|3))\b",
                        re.I)


def says_it_has_lingered(clean, illness=False):
    return bool(SAYS_IT_HAS_LINGERED.search(clean) and not _SHORT_RUN.search(clean))


LINGERED_LINE = (
    "Anything that has hung on is worth getting looked at — a pharmacist will see you quicker "
    "than a GP, and they'll tell you if it needs one.",
    "That is long enough to be worth a proper look rather than another stretch of waiting: a "
    "pharmacist today, and a GP if it is still there after that.",
    "Sorry it is still going. Note when it is worst and what eases it, then take that to a "
    "pharmacist — a thing that has lasted this long is worth putting a name to.",
)
AUX = frozenset(("can", "could", "do", "does", "did", "is", "was", "were", "are", "would",
                 "should", "have", "has", "had", "wo", "ai", "must", "need", "might"))


CONTRACTED_AUX = frozenset(("do", "did", "ca", "wo", "ai", "is", "are", "was", "were", "has",
                            "have", "had", "could", "would", "should", "must", "need", "dare",
                            "does", "am", "might"))


def negator(word):
    plain = word.replace("'", "").replace("\u2019", "")
    if plain in NEGATORS:
        return True
    return len(plain) > 3 and plain.endswith("nt") and plain[:-2] in CONTRACTED_AUX


def turned(words):
    for i, word in enumerate(words):
        if negator(word):
            return True
        if word == "t" and i and words[i - 1] in AUX:
            return True
    return False


DOUBT = frozenset(("believe", "believed", "imagine", "imagined", "thought", "think"))
CANNOT = frozenset(("cant", "cannot", "couldnt", "never", "always"))


def turns_round(words):
    if not turned(words):
        return False
    plain = [word.replace("'", "").replace("\u2019", "") for word in words]
    if any(word in DOUBT for word in plain) and any(word in CANNOT for word in plain):
        return False
    return True


def negated(clean, phrase, window=3):
    parts = phrase.split()
    if parts and negator(parts[0]):
        return False
    for match in re.finditer(r"\b" + re.escape(phrase) + r"\b", clean):
        if turns_round(clean[:match.start()].split()[-window:]):
            return True
    return False


def nearly(clean, phrase, window=2):
    parts = phrase.split()
    if parts and parts[0] in NEARLY:
        return False
    for match in re.finditer(r"\b" + re.escape(phrase) + r"\b", clean):
        if set(clean[:match.start()].split()[-window:]) & NEARLY:
            return True
    return False


SURE = frozenset(("think", "thought", "know", "knew", "reckon", "guess", "suppose", "sure",
                  "expect", "imagine", "say", "believe", "believed", "certain"))
DOUBTED = frozenset(("doubt", "doubts", "doubted", "doubting", "unsure", "uncertain"))
BELIEVE_IT = frozenset(("believe", "believed"))


def doubted(clean, window=4):
    plain = [word.strip(".,!?;:\"'").replace("\u2019", "") for word in str(clean).split()]
    if any(word in DOUBTED for word in plain):
        return True
    for i, word in enumerate(plain):
        if word not in SURE or not turns_round(plain[max(0, i - window):i]):
            continue
        if plain[i] in DOUBT and any(word in CANNOT for word in plain[max(0, i - window):i]):
            continue
        if plain[i] in BELIEVE_IT and i + 1 < len(plain) and plain[i + 1] == "it":
            continue
        return True
    return False


_PERSON_WORD = re.compile(
    r"\b(?:he|she|they|him|her|them|his|hers|their|himself|herself|themselves)\b", re.I)


def said_again(text):
    return _PERSON_WORD.sub("@", " ".join(str(text or "").lower().split()))


_CAPITAL_I = re.compile(r"I(?:'|’|\b)")


_HELLO_OPENS = ("hi ", "hi,", "hello", "hey", "morning", "afternoon", "evening",
                "nice to meet", "good to meet")

_ONE_WORD_THEN_A_BREAK = re.compile(r"^([A-Za-z'\u2019-]{1,20})\s*(?:\u2014|--|-|\?|!|:|,)")
_OPENS_A_SENTENCE = frozenset("""
    a an the and but or nor so yet if then when while with without for from to of in on at by
    it its it's i i'm im you you're ur your yours he she they we us them there here this that
    these those what whats why how who whom where which yes no not never always often usually
    sometimes maybe perhaps probably honestly actually really just only also still even too
    one two three four five few some any all each both most many more less least enough
    good bad best worst great fine okay ok right well now today tonight tomorrow first next last
    check try keep stop start put take give get go going let leave look make use ask call add
    avoid buy clean cook cover cut drink eat drive hold pick raise read ring run say see set sit
    sort speak stick tell turn walk wash wear write fill fix top find change wait watch worth
    sounds looks seems sorry thanks thank please sorry glad sadly luckily hopefully
""".split())


def _opens_with_a_name(body):
    match = _ONE_WORD_THEN_A_BREAK.match(str(body or "").strip())
    if not match:
        return False
    return match.group(1).lower().strip("'\u2019") not in _OPENS_A_SENTENCE


def greet_with(name, reply):
    if not name or not isinstance(reply, str) or not reply.strip():
        return reply
    body = reply.strip()
    plain = body.lower()
    if plain.startswith(_HELLO_OPENS) or plain.startswith("i'm " + str(name).lower()):
        return body
    name = str(name).strip()
    if _CAPITAL_I.match(body):
        return "Hi " + name + " — " + body
    if _opens_with_a_name(body):
        return "Hi " + name + ". " + body
    return "Hi " + name + " — " + body[0].lower() + body[1:]


OPENS_ON_A_FRAGMENT_QUESTION = re.compile(r"^\s*([A-Z][\w'\u2019]*(?:\s+[\w'\u2019]+){0,3})\?\s")
_NOT_A_FRAGMENT = frozenset("""what who why when where which how whatever honestly really
    sorry right ok okay so then and but well anyway""".split())


def _asks_about_a_thing_nobody_said(option, last, said):
    if last and str(last).strip().endswith("?"):
        return False
    match = OPENS_ON_A_FRAGMENT_QUESTION.match(str(option or ""))
    if not match:
        return False
    fragment = match.group(1)
    words = {w for w in re.findall(r"[a-z']+", fragment.lower()) if len(w) > 2}
    if not words or words & _NOT_A_FRAGMENT:
        return False
    heard = set(re.findall(r"[a-z']+", f"{last or ''} {said or ''}".lower()))
    return not (words & heard)


def pick(options, memory, seed_text=""):
    turns = memory.get("turns") or []
    last = turns[-1].get("bot") if turns and isinstance(turns[-1], dict) else None
    standing = [o for o in options if not _asks_about_a_thing_nobody_said(o, last, seed_text)]
    if standing and len(standing) < len(options):
        options = standing
    if not history.an_earlier_turn(memory):
        backed = [o for o in options if not history.a_past_that_is_not_there(o, memory)]
        if backed:
            options = backed
    fresh = [o for o in options if o != last] or list(options)
    said = {}
    for position, turn in enumerate(turns):
        if isinstance(turn, dict):
            said.setdefault(said_again(turn.get("bot")), position)
    unsaid = [o for o in fresh if said_again(o) not in said]
    if unsaid:
        fresh = unsaid
    else:
        oldest = min(said.get(said_again(o), -1) for o in fresh)
        fresh = [o for o in fresh if said.get(said_again(o), -1) == oldest]
    if seed_text:
        seed = len(turns) * 7919 + sum(ord(c) for c in str(seed_text))
    else:
        seed = len(turns)
    return random.Random(seed).choice(fresh)



def _name_just_given(memory):
    if memory.get("aside"):
        return ""
    log = memory.get("facts_log")
    if not isinstance(log, list):
        return ""
    turns = memory.get("turns")
    now = len(turns) if isinstance(turns, list) else 0
    for entry in reversed(log):
        if not isinstance(entry, dict) or entry.get("turn") != now:
            continue
        if entry.get("key") != "name":
            continue
        value = entry.get("value")
        if isinstance(value, str) and value.strip():
            return value.strip()
    return ""


def with_name(reply, memory):
    if not isinstance(reply, str) or not reply.strip():
        return reply
    name = _name_just_given(memory)
    if not name:
        return reply
    plain = " ".join(name.split())
    if not plain.isalpha() or len(plain) > 20:
        return reply
    if re.search(r"\b" + re.escape(plain.lower()) + r"'?s?\b", reply.lower()):
        return reply
    return greet_with(plain.capitalize(), reply)


STEP_WHEN_LOW = (
    "Start with the smallest thing that would help: something to eat, a shower, ten minutes "
    "outside. One of those, and that is today's job.",
    "Write down the three things on your mind, then do the smallest one. The other two can wait "
    "an hour.",
    "Tell one person today \u2014 a friend, family, whoever is easiest \u2014 that it is a rough one. "
    "It weighs less once somebody else knows.",
    "If it has been like this for weeks rather than days, the GP is the practical step: that is "
    "what they are there for, and you do not have to explain it well.",
    "Do the small thing in front of you \u2014 the dishes, a walk, a shower. The push to do the next "
    "one comes after the first, not before.",
)
A_STEP_ASK = re.compile(
    r"^\s*(?:so\s+|and\s+|ok(?:ay)?\s+|right\s+|well\s+)?"
    r"(?:what|where|how)\s+(?:should|do|can|could|shall|would)\s+(?:i|we)\s+"
    r"(?:do|start|begin|try|go|handle|sort|fix|deal)"
    r"(?:\s+(?:now|then|next|first|it|this|that|about it|about that|from here|today|tonight|at all))?"
    r"\s*[?.!]*\s*$"
    r"|^\s*(?:so\s+|and\s+|ok(?:ay)?\s+|right\s+)?what\s+(?:now|next)\s*[?.!]*\s*$"
    r"|^\s*(?:so\s+|and\s+|ok(?:ay)?\s+|right\s+)?now\s+what\s*[?.!]*\s*$"
    r"|^\s*(?:so\s+|and\s+|ok(?:ay)?\s+|right\s+)?(?:what|anything)\s+"
    r"(?:helps|would\s+help|can\s+help|might\s+help)\s*[?.!]*\s*$"
    r"|^\s*(?:so\s+|and\s+)?how\s+(?:do|can|could|should)\s+i\s+"
    r"(?:feel|get|make\s+myself\s+feel)\s+better\b[^?.!]*[?.!]*\s*$",
    re.IGNORECASE)


def _says_one_of(text, said):
    flat = text.lower()
    return any(line and line.lower() in flat for line in said)


def step_when_low(clean, memory, comfort_said):
    if not A_STEP_ASK.match(str(clean or "").strip()):
        return None
    turns = memory.get("turns") or []
    turn = turns[-1] if turns and isinstance(turns[-1], dict) else {}
    last = (turn.get("bot") or "").strip()
    if not last or not _says_one_of(last, comfort_said):
        return None
    try:
        from .badnews import (reads_as_a_leaving_already_gone, reads_as_a_reported_leaving,
                              reads_as_a_sacking, reads_as_bad_news, reads_as_the_leaving)
        said = " ".join(str(turn.get("user") or "").lower().split())
        if reads_as_a_reported_leaving(said):
            return None
        if (reads_as_bad_news(said)
                and not reads_as_the_leaving(said)
                and not reads_as_a_leaving_already_gone(said)
                and not reads_as_a_sacking(said)):
            return None
    except Exception:
        pass
    return pick(list(STEP_WHEN_LOW), memory, clean)
