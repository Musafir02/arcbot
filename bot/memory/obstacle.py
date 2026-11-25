import re

from ..understanding import understand
from . import ack, detail, repeat, topics

DISLIKE = (
    re.compile(r"^\W*(?:(?:and|but|so|oh|also|well|yeah|yep|ok|okay|right|alright)\W+)*"
               r"i\s+(?:(?:just|really|properly|actually|kind of|sort of)\s+)*"
               r"(?:hate|hates|dislike|dislikes)\s+(?P<thing>.+)$", re.I),
    re.compile(r"^\W*(?:(?:and|but|so|oh|also|well|yeah|yep|ok|okay|right|alright)\W+)*"
               r"i\s+(?:(?:just|really|properly|actually)\s+)*"
               r"(?:cant|cannot|can\s*not|can'?t)\s+stand\s+(?P<thing>.+)$", re.I),
    re.compile(r"^\W*(?:(?:and|but|so|oh|also|well|yeah|yep|ok|okay|right|alright)\W+)*"
               r"i\s*(?:'m|m|am)?\s*(?:not|n't)\s+(?:a\s+)?(?:fan|keen)\s+(?:of|on)\s+"
               r"(?P<thing>.+)$", re.I),
    re.compile(r"^\W*(?:(?:and|but|so|oh|also|well|yeah|yep|ok|okay|right|alright)\W+)*"
               r"i\s+(?:(?:just|really|properly|actually)\s+)*"
               r"(?:dont|do\s*not|don'?t)\s+(?:like|love|fancy)\s+(?P<thing>.+)$",
               re.I),
)
NOT_A_THING = frozenset("""it its it's that this these those them him her you me everything
    anything something stuff things thing more any all
    myself yourself himself herself itself ourselves themselves""".split())
MOST_WORDS = 12
STEP_WORDS = 16
SHORTER = 10
LEADS = (
    "Fair enough - this part doesn't need {thing}: {step}",
    "That's fine, this works without {thing}: {step}",
    "You can leave {thing} out of this one: {step}",
    "This one works without {thing}: {step}",
    "Then skip {thing} - the rest of it stands: {step}",
)
CANNOT_USE_ASKS = (
    "No {bare}, then - what could you do instead?",
    "So {thing} won't work - what else is there?",
    "Okay, so not {thing}: what could you do instead?",
)
REFUSAL = (
    re.compile(r"^\W*(?:(?:and|but|so|oh|also|well|yeah|yep|ok|okay|right|alright|honestly)\W+)*"
               r"i\W+(?:(?:just|really|actually|honestly|properly|definitely|absolutely|kind\s+of|"
               r"sort\s+of)\W+)*"
               r"(?:dont|do\s*not|don'?t|wouldnt|would\s*not|won'?t|wont)\s+"
               r"(?:want\s+(?:to\s+)?|wanna\s+)?(?P<move>[a-z].*)$", re.I),
    re.compile(r"^\W*(?:(?:and|but|so|oh|also|well|yeah|yep|ok|okay|right|alright|honestly)\W+)*"
               r"i(?:['\u2019]?d|\s+would)\s+(?:really\s+|much\s+)?rather\s+(?:not\s+)?"
               r"(?P<move>[a-z].*)$", re.I),
    re.compile(r"^\W*(?:(?:and|but|so|oh|also|well|yeah|yep|ok|okay|right|alright|honestly)\W+)*"
               r"i\s+(?:refuse\s+to|wouldnt\s+be\s+able\s+to|wont\s+be\s+able\s+to)\s+"
               r"(?P<move>[a-z].*)$", re.I),
)
_TREATMENT = ("spot on", "flea treatment", "flea product", "flea collar", "flea tablet",
              "flea drop", "wormer", "dewormer", "shampoo", "permethrin", "fipronil",
              "imidacloprid", "frontline", "advocate", "drops")
_MEDICINE = ("pill", "tablet", "medicine", "medication", "dose", "drug", "supplement",
             "paracetamol", "ibuprofen", "aspirin", "painkiller", "antibiotic", "antihistamine",
             "steroid", "inhaler", "melatonin")
THE_SAME_MOVE = {
    "kill": ("kill", "trap", "snap", "poison", "bait", "pest", "exterminat"),
    "trap": ("trap", "snap", "bait", "kill"),
    "poison": ("poison", "bait", "pesticide", "chemical", "spray", "fogger", "insecticide") + _TREATMENT,
    "bait": ("bait", "poison", "trap"),
    "chemical": ("chemical", "pesticide", "spray", "insecticide", "fogger", "poison") + _TREATMENT,
    "spray": ("spray", "pesticide", "chemical", "fogger", "insecticide") + _TREATMENT,
    "fogger": ("fogger", "spray", "pesticide", "chemical", "insecticide") + _TREATMENT,
    "pellet": ("pellet", "bait", "poison", "slug"),
    "pill": _MEDICINE,
    "tablet": _MEDICINE,
    "medicine": _MEDICINE,
    "medication": _MEDICINE,
    "drug": _MEDICINE,
    "take": _MEDICINE,
    "swallow": _MEDICINE,
}
REFUSAL_LEADS = (
    "You don't have to {move} to start. {step}",
    "Start with the part that does not need you to {move}. {step}",
    "That comes later, if at all - this first: {step}",
)
LEAD_ORDERS = re.compile(r"\bthis first\b", re.I)
STEP_ORDERS = re.compile(r"^(?:first|firstly|find|start|begin|sort)\b", re.I)
NOTHING_TO_DO_LEADS = (
    "You don't have to {move}. {step}",
    "None of this needs you to {move}. {step}",
    "Nobody is asking you to {move}. {step}",
)
REFUSAL_THING_LEADS = (
    "You don't have to start with the {thing}. {step}",
    "Start with the part that needs no {thing}. {step}",
)
NOTHING_THING_LEADS = (
    "None of this needs {thing}. {step}",
    "Nobody is asking for {thing}. {step}",
    "You can leave {thing} out of this: {step}",
)
THE_NOUN = re.compile(r"^(?:the|a|an|any|my|your|our|their|his|her|some|those|these)\s+", re.I)
FRAME_WORDS = frozenset("""i dont don't do not want wanna to really just actually honestly
    properly definitely absolutely kind of sort would much rather though tho too either at all as
    well anymore now any and but so oh also yeah yep ok okay right alright""".split())
REFUSAL_WORDS = 60
STOP = frozenset("""the a an my our your their his her its some any and but so of to for at on
    in with about really very quite just too""".split())


def _flat(text):
    return " ".join(str(text or "").split())


def _words(text):
    return re.findall(r"[a-z']+", _flat(text).lower())


def the_thing(text):
    said = _flat(text)
    if not said or "?" in said or len(said.split()) > MOST_WORDS:
        return None
    if not ack.only_a_dislike(said):
        return None
    for pattern in DISLIKE:
        found = pattern.match(said)
        if not found:
            continue
        thing = found.group("thing").strip(" .!,;:")
        if not thing or thing.lower() in NOT_A_THING:
            return None
        return thing
    return None

UNABLE_VERB = (r"do|use|afford|eat|have|get\s+to|go\s+to|join|manage|handle|attend|access|"
               r"buy|pay\s+for|reach|keep\s+up")
CANNOT_USE = (
    re.compile(r"^\W*(?:(?:and|but|so|oh|also|well|yeah|yep|ok|okay|right|alright)\W+)*"
               r"(?:the\s+problem\s+is\s+|its\s+just\s+that\s+)?"
               r"i\s+(?:(?:just|really|actually|properly|kind\s+of|sort\s+of)\s+)*"
               r"(?:cant|cannot|can\s*not|can'?t)\s+(?:" + UNABLE_VERB + r")\s+"
               r"(?P<thing>.+)$", re.I),
    re.compile(r"^\W*(?:(?:and|but|so|oh|also|well|yeah|yep|ok|okay|right|alright)\W+)*"
               r"(?:the\s+problem\s+is\s+|its\s+just\s+that\s+)?"
               r"(?:i|we)\s+(?:(?:just|really|actually)\s+)*"
               r"(?:dont|do\s*not|don'?t|havent|have\s*not|haven'?t)\s+(?:got\s+)?"
               r"(?:have\s+|own\s+)?(?P<thing>(?:a|an|any|the|my|our)\s+[a-z][a-z' ]{0,24})$",
               re.I),
)
NOT_A_LIMIT = frozenset("""time clue idea choice chance point reason way word answer option
    money cash budget it that this them those these""".split())


def the_thing_they_cannot_use(text):
    said = _flat(text)
    if not said or "?" in said or len(said.split()) > MOST_WORDS:
        return None
    for pattern in CANNOT_USE:
        found = pattern.match(said)
        if not found:
            continue
        thing = found.group("thing").strip(" .!,;:")
        core = " ".join(word for word in _words(thing) if word not in STOP)
        if not thing or not core or core in NOT_A_THING or core in NOT_A_LIMIT:
            return None
        if re.search(r"\b(?:because|since|as|though|although|but|unless|if|when)\b", thing.lower()):
            return None
        return thing
    return None


def the_move(text):
    said = _flat(text)
    if not said or "?" in said or len(said.split()) > MOST_WORDS:
        return None
    for pattern in REFUSAL:
        found = pattern.match(said)
        if not found:
            continue
        move = found.group("move").strip(" .!,;:")
        move = re.sub(r"^(?:be\s+|have\s+to\s+|keep\s+)", "", move)
        move = re.sub(r"[\s,]+(?:though|tho|too|either|really|honestly|at\s+all|as\s+well|"
                      r"any\s+more|now)$", "", move, flags=re.I)
        if not move:
            return None
        family = _the_family(move)
        if not family:
            return None
        return move
    return None


def _the_family(move):
    for word in _words(move):
        if word in STOP:
            continue
        for key, family in THE_SAME_MOVE.items():
            if word.startswith(key):
                return tuple(family)
    return ()


def _has_family(words, family):
    for word in words:
        for stem in family:
            if word.startswith(stem):
                return True
    return False


def _carries_a_move(sentence, family):
    if _has_family(_words(sentence), family):
        return True
    said = " " + re.sub(r"[^a-z0-9]+", " ", _flat(sentence).lower()) + " "
    return any(" " + stem + " " in said for stem in family if " " in stem)


_ANY_MOVE = tuple(sorted({stem for family in THE_SAME_MOVE.values() for stem in family}))


A_DOING = topics.IMPERATIVE | frozenset("""
empty vacuum hoover dust brush scrub bleach seal strip snip trap bait sprinkle hang launder soak
""".split())
REFUSED_VERBS = A_DOING | frozenset("""
kill trap bait poison spray use take put set call pay buy hire throw burn bury dig cut wash fill
""".split())
PREPOSITIONS = frozenset("""in on at round around under over by near behind inside outside from
    with about across through along""".split())


FRAME = re.compile(
    r"^(?:the things? that (?:work|help|matter)|what (?:works|helps)|the fix|the trick|the plan|"
    r"the short version|what i would do|the basics)\b[^:.!?]{0,40}:\s+\S", re.I)


def _opens_on_a_verb(move):
    words = _words(move)
    if len(words) < 2 or words[0] not in REFUSED_VERBS:
        return False
    return words[1] not in PREPOSITIONS


def _the_noun(move):
    return THE_NOUN.sub("", _flat(move)).strip(" .!,;:")


def _a_list_under_a_frame(one):
    said = " ".join(str(one or "").split())
    if "?" in said or not FRAME.match(said):
        return False
    tail = said.split(":", 1)[1]
    return tail.count(",") >= 2


def _a_doing(one):
    if detail._a_step(one):
        return True
    words = str(one or "").split()
    if not words:
        return False
    first = words[0].strip(",;:.-\u2014\u2013'\"").lower()
    if first in A_DOING:
        return True
    return _a_list_under_a_frame(one)


def _a_whole_step(sentence):
    said = " ".join(str(sentence or "").split())
    if not said:
        return ""
    if len(said.split()) <= REFUSAL_WORDS:
        return said if said.endswith(".") else said + "."
    cut = ""
    for piece in re.split(r"(?<=[,;:])\s+", said):
        trial = (cut + " " + piece).strip()
        if cut and len(trial.split()) > REFUSAL_WORDS:
            break
        cut = trial
    if len(cut.split()) > REFUSAL_WORDS:
        cut = " ".join(cut.split()[:REFUSAL_WORDS])
    cut = cut.strip(" ,;:-")
    return cut + "." if cut else ""


def a_move_refused(text, memory):
    if not isinstance(memory, dict):
        return None
    move = the_move(text)
    if not move:
        return None
    family = _the_family(move)
    if not family:
        return None
    about = (understand(_flat(text), {}) or {}).get("topic_own")
    mine = set(_words(move))
    only_the_move = not [w for w in _words(text) if w not in mine and w not in FRAME_WORDS]
    for back, asked, said in repeat._recent_answers(_before_this_turn(memory, text)):
        if back > 2:
            continue
        if back > 1 and not repeat._about_the_same_thing(asked, said, memory):
            continue
        there = (understand(_flat(asked), {}) or {}).get("topic_own")
        if about and there and about != there and not only_the_move:
            continue
        gives_it = _carries_a_move(said, family)
        step = ""
        sentence = ""
        for one in re.split(r"(?<=[.!?])\s+", _flat(said)):
            if _carries_a_move(one, family):
                continue
            if not gives_it and _carries_a_move(one, _ANY_MOVE):
                continue
            piece = _a_whole_step(one)
            if not piece:
                continue
            if not _a_doing(one):
                continue
            step, sentence = piece, one
            break
        if not step:
            continue
        if repeat._already_repeated(step, memory):
            step = detail._first_clause(step)
            if not step or repeat._already_repeated(step, memory):
                return None
        pool = REFUSAL_LEADS if gives_it else NOTHING_TO_DO_LEADS
        said_move = move
        if not _opens_on_a_verb(move):
            pool = REFUSAL_THING_LEADS if gives_it else NOTHING_THING_LEADS
            said_move = _the_noun(move) or move
        if STEP_ORDERS.match(step):
            pool = tuple(lead for lead in pool if not LEAD_ORDERS.search(lead)) or pool
        reply = repeat.pick(pool, memory, text).format(move=said_move, thing=said_move, step=step)
        if sentence:
            repeat._handed_back(memory, sentence)
        return repeat._handed_back(memory, reply)
    return None


FRAME_BREAK = re.compile(r"\s*(?::|\u2014|\u2013|--|;)\s*")


def _under_its_frame(one):
    said = " ".join(str(one or "").split())
    parts = FRAME_BREAK.split(said, 1)
    if len(parts) != 2:
        return ""
    head, tail = parts[0].strip(), parts[1].strip()
    if not head or not tail or len(head.split()) > REFUSAL_WORDS:
        return ""
    if not _a_doing(tail):
        return ""
    return _a_whole_step(tail)


def _the_frame(one):
    parts = FRAME_BREAK.split(" ".join(str(one or "").split()), 1)
    return parts[0].strip() if len(parts) == 2 else ""


def _steps(said):
    out = []
    for sentence in re.split(r"(?<=[.!?])\s+", _flat(said)):
        step = detail._a_step(sentence, questions_are_steps=True)
        if step:
            out.append((sentence, step, False))
            continue
        under = _under_its_frame(sentence)
        if under:
            out.append((sentence, under, True))
    return out


def _needs_it(step, thing):
    wanted = set(_words(thing)) - STOP
    return bool(wanted & set(_words(step)))


def _leans_on_it(said, thing, asked=None):
    wanted = set(_words(thing)) - STOP
    if not wanted:
        return False
    if wanted & set(_words(said)):
        return True
    there = (understand(_flat(thing), {}) or {}).get("topic_own")
    mine = (understand(_flat(asked or ""), {}) or {}).get("topic_own")
    return bool(there and mine and there == mine)


def _before_this_turn(memory, text):
    if not isinstance(memory, dict):
        return memory or {}
    turns = [turn for turn in (memory.get("turns") or []) if isinstance(turn, dict)]
    mine = _flat(text)
    while turns and _flat(str(turns[-1].get("user") or "")) == mine:
        turns.pop()
    if len(turns) == len(memory.get("turns") or []):
        return memory
    return dict(memory, turns=turns)


def _the_reply_for(text, memory, thing, limited):
    about = (understand(_flat(text), {}) or {}).get("topic_own")
    for back, asked, said in repeat._recent_answers(_before_this_turn(memory, text)):
        if back > 2:
            continue
        if back > 1 and not repeat._about_the_same_thing(asked, said, memory):
            continue
        if not limited:
            there = (understand(_flat(asked), {}) or {}).get("topic_own")
            if about and there and about != there:
                continue
            if not _leans_on_it(said, thing, asked):
                continue
        step = None
        sentence = ""
        framed = False
        for sentence, piece, under in _steps(said):
            if not _needs_it(piece, thing):
                step = piece
                framed = under
                break
        if not step:
            if limited:
                ask = repeat.pick(CANNOT_USE_ASKS, memory, text).format(
                    thing=thing, bare=THE_NOUN.sub("", thing))
                return repeat._handed_back(memory, ask)
            continue
        if repeat._already_repeated(step, memory):
            step = detail._first_clause(step)
            if not step or repeat._already_repeated(step, memory):
                return None
        if len(step.split()) > STEP_WORDS:
            step = detail._first_clause(step)
        reply = repeat.pick(LEADS, memory, text).format(thing=thing, step=step)
        if framed:
            repeat._handed_back(memory, step)
        elif sentence:
            repeat._handed_back(memory, sentence)
        return repeat._handed_back(memory, reply)
    return None


def answer_for(text, memory):
    if not isinstance(memory, dict):
        return None
    thing = the_thing(text)
    if not thing:
        return None
    return _the_reply_for(text, memory, thing, False)


def answer_for_a_thing_they_cannot_use(text, memory):
    if not isinstance(memory, dict):
        return None
    thing = the_thing_they_cannot_use(text)
    if not thing:
        return None
    return _the_reply_for(text, memory, thing, True)
