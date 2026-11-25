import copy
import importlib
import random
import re

from ..compose import pick
from ..understanding import understand
from . import topics

STATE = re.compile(
    r"\b(?:i'?m|i am|i feel|i'?ve been|i have been|i'?ve had|i have had|i had|it'?s been|"
    r"its been|feel|feeling|been)\s+"
    r"(?:(?:so|very|really|proper|properly|totally|completely|absolutely|a bit|a little|well|"
    r"fairly|quite|pretty|dead|bloody|seriously|still|just|always|knackered|feeling)\s+)*"
    r"(?:(?:having|had)\s+)?(?:(?:a|an|the)\s+)?"
    r"([a-z']+(?:\s+up)?)\b", re.I)

STATE_WORDS = frozenset("""
tired knackered shattered exhausted drained worn weary stressed stressed-out anxious worried
nervous low down depressed miserable unhappy sad lonely bored fed up hacked off angry cross
annoyed upset rubbish awful terrible rough ill sick poorly unwell sore achy achey hurting
skint broke strapped poor lost stuck overwhelmed snowed swamped
flat empty numb crap
""".split())

STATE_PHRASES = (
    "in a state", "at the end of my tether", "at the end", "under the weather", "run down",
    "worn out", "fed up", "hacked off", "on my knees", "all over the place", "not sleeping",
    "not been sleeping", "short of money", "hard up", "out of work", "off sick",
    "bad day", "rough day", "hard day", "long day", "tough day", "off day",
    "down day", "flat day", "rubbish week", "bad week", "rough week", "hard week", "long week",
)

A_QUESTION_AT_THE_END = re.compile(r"\?\s*[\"'”’)]?\s*$")

A_THING = re.compile(
    r"^(?:(?:just|only|mostly|mainly|probably|definitely|honestly|mostly just|just the|"
    r"probably the|i think|i suppose|suppose|maybe)\s+)*"
    r"(?:the|my|our|his|her|their|this|that|a|an|no|not having|having|being|work|money|"
    r"sleep|kids|family|everything|it|me|us)?\s*"
    r"([a-z' ]{1,40})$", re.I)

A_GUESS_IN_FRONT = re.compile(
    r"^(?:(?:maybe|probably|likely|definitely|honestly|really|just|only|actually|possibly|"
    r"must be|its|it's|i think|i suppose|suppose|i reckon|reckon|though|but|and|also)\s+)+",
    re.I)

NOT_A_REASON = frozenset("""
everything everyone everybody anything nothing something life stuff things
""".split())
NOT_A_REASON_PHRASES = ("it all", "all of it", "the world", "the lot", "everything else",
                        "everything at once")


A_SWAP_TO_YOURS = ((re.compile(r"\bmy\b", re.I), "your"), (re.compile(r"\bour\b", re.I), "your"),
                   (re.compile(r"\bhis\b|\bher\b|\btheir\b", re.I), "your"),
                   (re.compile(r"\bme\b", re.I), "you"), (re.compile(r"\bi\b", re.I), "you"))

NO_IDEA = re.compile(
    r"\b(?:do(?:n'?t| not)|doesnt|doesn'?t|didnt|didn'?t|dunno|dun+o)\s+(?:really\s+)?know\b"
    r"|\bno idea\b|\bnot (?:sure|a clue)\b|\bwho knows\b|\bgod knows\b|\bbeats me\b"
    r"|\bno clue\b|\bsearch me\b|\bhaven'?t a clue\b|\bnot got a clue\b", re.I)

A_BODY_OR_A_PERSON = re.compile(
    r"\b(?:(?:my|his|her|their|the)\s+)?(?:head|heads|back|knee|knees|shoulder|shoulders|hip|"
    r"hips|neck|stomach|belly|gut|tooth|teeth|gum|gums|foot|feet|ankle|ankles|arm|arms|leg|legs|"
    r"hand|hands|wrist|elbow|ear|ears|throat|chest|skin|eye|eyes|migraine|migraines|cough|cold|"
    r"flu|toothache|backache|sciatica|arthritis)\b"
    r"|\b(?:my|our|his|her|their)\s+(?:husband|wife|partner|boyfriend|girlfriend|mum|mom|mam|"
    r"mother|dad|father|son|daughter|child|kid|kids|baby|brother|sister|friend|mate|boss|"
    r"colleague|nan|gran|grandma|grandad|aunt|uncle|cousin)\b", re.I)

NOT_A_THING = frozenset("""
yes yeh yeah yep ok okay k cool nice right sure no nope nah nothing none nothing much
thanks thank you ta cheers hi hello hey hmm mm mmm oh ah sorry alright fine definitely
maybe probably dont know dunno what why how who when where l don't know not sure
""".split())

A_NOD = topics.ACKS | topics.STOPWORDS | frozenset("""
good great brilliant brill ace excellent amazing wonderful lovely loverly luvly fab fabulous
super top sorted sound grand mint quality class legend star stuff things one
mate matey fella boss hun love dude bud pal thats that thank ta cheers much many lot lots
ha haha lol lols hehe x xx xxx aye yeh yep yes yeah ok okay kk alright then so well too anyway
anyhow though also still just only really honestly actually truly right fine
""".split())

NO_REASON = re.compile(
    r"^\W*(?:"
    r"(?:(?:i\s+)?(?:really|honestly|actually|genuinely)\s+)?(?:i\s+)?"
    r"(?:(?:dont|don'?t|do not)\s+(?:really\s+)?know"
    r"|(?:have\s+)?no\s+idea"
    r"|(?:i\s*(?:'m|m| am)\s+)?(?:not|cant|can'?t|cannot)\s+(?:really\s+)?"
    r"(?:sure|explain|say|tell)"
    r"|dunno)\s+why\b"
    r"|(?:but\s+|and\s+|so\s+)?(?:nothing|nowt)(?:\s+(?:much|really|at all))?\s+"
    r"(?:has\s+|had\s+)?happened\b"
    r"|(?:for\s+)?(?:no|not\s+any|without\s+a)\s+(?:particular\s+|real\s+|obvious\s+)?reason\b"
    r"|(?:i\s+)?(?:dont|don'?t|do not)\s+(?:really\s+)?know"
    r"|(?:have\s+)?no\s+idea"
    r"|dunno"
    r")"
    r"(?:\s+(?:really|at all|though|today|honestly|maybe|i suppose))*\s*[.!?]*\s*$", re.I)

A_VERB = re.compile(
    r"\b(?:is|are|was|were|be|been|am|do|does|did|have|has|had|will|would|can|could|should|"
    r"shall|may|might|must|need|needs|needed|want|wants|wanted|got|get|gets|getting|go|goes|"
    r"went|make|makes|made|take|takes|took|keep|keeps|kept|wake|wakes|woke|feed|feeds|"
    r"cries|cried|come|comes|came|start|starts|started|stop|stops|stopped|work|works|"
    r"working|left|leave|leaves|lost|lose|loses|hate|hates|love|loves|said|says|tell|told)\b",
    re.I)

A_QUESTION_WORD = re.compile(
    r"^\W*(?:what|whats|what's|why|how|hows|how's|when|whens|where|who|whos|which|whose|"
    r"do|does|did|is|are|was|were|can|could|would|should|will|shall|have|has|had|am)\b", re.I)

REPEATED_ON_PURPOSE = re.compile(
    r"^\W*(?:same (?:answer|as|one)|it'?s what i said|as i said|said already|"
    r"that is the same|the same as|again:)", re.I)

NOTHING_SAID = re.compile(
    r"\b(?:i'?m listening|say more|not sure about that one|don'?t know enough|"
    r"beyond what i know|rather not guess|everything i have on that one|"
    r"not much (?:i can add|to go on)|which bit do you|tell me more|"
    r"i'?m here if you want|anything you'?d like a hand with|thanks for telling me)\b"
    r"|\u2014\s*noted\.|\s-\s*noted\.", re.I)


def _flat(text):
    return " ".join(str(text or "").lower().replace("’", "'").split())


def _turns(memory):
    return [t for t in (memory.get("turns") or []) if isinstance(t, dict)]


def _the_state_they_reported(memory, back=4):
    for turn in reversed(_turns(memory)[-back:]):
        line = _flat(turn.get("user"))
        if not line:
            continue
        for phrase in STATE_PHRASES:
            if re.search(r"\b" + re.escape(phrase) + r"\b", line):
                return line, phrase
        found = STATE.search(line)
        if found and found.group(1).strip() in STATE_WORDS:
            return line, found.group(1).strip()
    return None, None


def _the_bot_just_spoke(memory):
    for turn in reversed(_turns(memory)[-2:]):
        said = str(turn.get("bot") or "").strip()
        if said:
            return said
    return ""


def _already_has_it(said, thing):
    if not said:
        return False
    line = " " + _flat(said) + " "
    words = [w for w in _flat(thing).split()
             if w not in ("the", "my", "our", "his", "her", "their", "a", "an", "this", "that",
                          "just", "only", "mostly", "mainly", "probably", "definitely")]
    return bool(words) and all(re.search(r"\b" + re.escape(w) + r"\b", line) for w in words)


A_HESITATION = re.compile(
    r"^\W*(?:i\s*(?:'m|m| am)\s+)?(?:not\s+(?:really\s+|too\s+|so\s+)?sure|unsure|"
    r"not\s+(?:really\s+)?certain|(?:i\s+)?(?:dont|don'?t|do not)\s+(?:really\s+)?know|"
    r"dunno|no\s+idea)\b", re.I)


def _only_a_nod(text):
    if topics.is_ack(text):
        return True
    words = [word.strip(".,!?'") for word in _flat(text).lower().split()]
    return bool(words) and all(word in A_NOD for word in words if word)


def _a_thing(text):
    low = _flat(text).strip(" .!,")
    if not low or low.endswith("?"):
        return None
    if A_HESITATION.match(low):
        low = A_HESITATION.sub("", low).strip(" .,:;-")
        if not low:
            return None
    if A_QUESTION_WORD.match(low):
        return None
    body = A_GUESS_IN_FRONT.sub("", low).strip() or low
    body = A_GUESS_IN_FRONT.sub("", body).strip() or body
    words = body.split()
    if len(words) > 4 or len(words) < 1:
        return None
    if body in NOT_A_THING or " ".join(words) in NOT_A_THING:
        return None
    if len(words) > 1 and A_VERB.search(body):
        return None
    if not A_THING.match(body):
        return None
    if _only_a_nod(body):
        return None
    low = body
    words = low.split()
    if not [w for w in words if w not in (
            "the", "my", "our", "his", "her", "their", "this", "that", "a", "an", "it", "just",
            "only", "mostly", "mainly", "probably", "definitely", "honestly", "maybe", "i",
            "think", "suppose")]:
        return None
    return low


def expand(text, memory):
    thing = _a_thing(text)
    if not thing:
        return None
    spoke = _the_bot_just_spoke(memory)
    if not spoke:
        return None
    if _already_has_it(spoke, thing):
        return None
    said, word = _the_state_they_reported(memory)
    if not said or not word:
        return None
    state = said if len(said.split()) <= 8 else "im " + word
    return state + ", " + thing


def _the_bot_would_only_shrug(line, memory):
    try:
        from ..compose import fallback
    except Exception:
        return False
    probe = copy.deepcopy(memory)
    state = random.getstate()
    try:
        said = fallback.reply_for(line, probe, verdict=False) or ""
    except Exception:
        return False
    finally:
        random.setstate(state)
    return bool(NOTHING_SAID.search(said))


def _asked(line, memory, names=("answers", "chat")):
    reading_memory = copy.deepcopy(memory)
    reading_memory["understood"] = understand(line, reading_memory)
    for name in names:
        try:
            module = importlib.import_module("..modules." + name, __package__)
            said = module.respond(line, reading_memory)
        except Exception:
            continue
        if isinstance(said, str) and said.strip() and not NOTHING_SAID.search(said):
            return said.strip()
    return None


A_REASON_TOOK = (
    "{reason} can do that to you. What is the worst of it at the moment?",
    "That is a lot to carry, and {reason} would wear anyone down.",
    "{reason} - that is the usual one. Is it worse now than it was a month ago?",
    "Anyone would be worn down by {reason}. What is the worst part of it just now?",
)


A_REASON_NOBODY_HAS = (
    "There's often no reason you could point at. It's still worth telling me.",
    "That's alright \u2014 a lot of it arrives without a why.",
    "You don't have to have the reason for it. Say what it's like and we'll go from there.",
    "Plenty of it has no cause you could name. It still counts.",
)


A_STOCK_LOW_POOLS = ("sad",)


def _a_stock_low_line(said):
    try:
        from ..modules import chat
    except Exception:
        return False
    line = _flat(said)
    for name in A_STOCK_LOW_POOLS:
        for pool_line in chat.REPLIES.get(name) or ():
            if isinstance(pool_line, str) and _flat(pool_line) == line:
                return True
    return False


def _says_the_reason(said, thing):
    words = [w for w in _flat(thing).split()
             if w not in ("the", "my", "our", "his", "her", "their", "a", "an", "this", "that",
                          "just", "only", "mostly", "mainly")]
    if not words:
        return True
    line = " " + _flat(said) + " "
    for word in words:
        stem = word[:5] if len(word) > 5 else word
        if re.search(r"\b" + re.escape(stem), line):
            return True
    return False


def _names_nothing(reason):
    line = " " + _flat(reason) + " "
    if any(" " + phrase + " " in line for phrase in NOT_A_REASON_PHRASES):
        return True
    said = [word for word in _flat(reason).split()
            if word not in ("the", "my", "our", "his", "her", "their", "a", "an", "this", "that")]
    return bool(said) and all(word in NOT_A_REASON for word in said)


def _the_persons_own_reason(reason):
    said = _flat(reason)
    for pattern, replacement in A_SWAP_TO_YOURS:
        said = pattern.sub(replacement, said)
    return said


def _asks_for_the_rest(text):
    try:
        from . import another as another_module
        return another_module.names_nothing(text)
    except Exception:
        return False


def _a_reason_for_how_they_are(thing, memory):
    words = [w for w in _flat(thing).split()
             if w not in ("the", "my", "our", "his", "her", "their", "a", "an", "this",
                          "that", "just", "only", "mostly", "mainly")]
    if not words or len(words) > 3:
        return None
    if _names_nothing(thing):
        return None
    if _asks_for_the_rest(thing):
        return None
    body = pick(A_REASON_TOOK, memory, thing)
    reason = _the_persons_own_reason(thing)
    said = body.replace("{reason}", reason[0].upper() + reason[1:] if body.startswith("{reason}")
                        else reason)
    said = said[0].upper() + said[1:]
    kept = memory.get("repeated")
    if isinstance(kept, list) and said in kept:
        return None
    for turn in reversed(_turns(memory)[-2:]):
        line = str(turn.get("bot") or "").strip()
        if line:
            if _flat(line) == _flat(said):
                return None
            break
    return said


def _without_what_was_just_said(said, last):
    seen = _flat(last)
    kept = []
    for sentence in re.split(r"(?<=[.!?])\s+", said.strip()):
        if sentence and _flat(sentence) not in seen:
            kept.append(sentence.strip())
    return " ".join(kept)


def _a_new_answer(said, memory):
    if not said:
        return None
    last = ""
    for turn in reversed(_turns(memory)[-3:]):
        last = str(turn.get("bot") or "").strip()
        if last:
            break
    if last and _flat(said) == _flat(last):
        return None
    if last:
        said = _without_what_was_just_said(said, last)
        if not said:
            return None
    if said in (memory.get("repeated") or []):
        return None
    if REPEATED_ON_PURPOSE.match(said):
        return None
    return said


def _the_feeling_without_a_reason(memory):
    said, word = _the_state_they_reported(memory)
    if not said or not word:
        return None
    state = said if len(said.split()) <= 8 else "im " + word
    answer = _a_new_answer(_asked(state + ", and i don't know why", memory,
                                  names=("answers", "chat")), memory)
    if answer:
        return answer
    return _the_reason_nobody_has(memory)


def _the_reason_nobody_has(memory):
    said = pick(A_REASON_NOBODY_HAS, memory, "no reason")
    kept = memory.get("repeated")
    if isinstance(kept, list) and said in kept:
        return None
    last = ""
    for turn in reversed(_turns(memory)[-3:]):
        last = str(turn.get("bot") or "").strip()
        if last:
            break
    if last and _flat(said) == _flat(last):
        pool = list(A_REASON_NOBODY_HAS)
        here = pool.index(said) if said in pool else 0
        said = pool[(here + 1) % len(pool)]
    return said


def _the_knowledge_base_answers_it(thing, memory):
    try:
        module = importlib.import_module("..modules.answers", __package__)
        reading_memory = copy.deepcopy(memory)
        reading_memory["understood"] = understand(thing, reading_memory)
        said = module.respond(thing, reading_memory)
    except Exception:
        return False
    return bool(isinstance(said, str) and said.strip())


def _asks_about_the_bot(text, memory):
    try:
        reading = understand(text, memory)
    except Exception:
        return False
    if not isinstance(reading, dict):
        return False
    if not (reading.get("topic") == "about-the-bot"
            and reading.get("kind") == "question"
            and not reading.get("entities")):
        return False
    try:
        from . import meant
        return bool(meant.answer_for(text, memory))
    except Exception:
        return False


def answer_for(text, memory):
    if _asks_about_the_bot(text, memory):
        return None
    if NO_REASON.match(_flat(text)):
        return _the_feeling_without_a_reason(memory)
    reading = expand(text, memory)
    if not reading:
        return None
    thing = _a_thing(text)
    if thing and _the_knowledge_base_answers_it(thing, memory):
        return None
    if thing and not _the_bot_would_only_shrug(thing, memory):
        return None
    said = _asked(reading, memory)
    plain = bool(thing) and not NO_IDEA.search(thing or "")
    if not said:
        return _a_reason_for_how_they_are(thing, memory) if plain else None
    if (plain and not A_BODY_OR_A_PERSON.search(thing)
            and _a_stock_low_line(said) and not _says_the_reason(said, thing)):
        warmer = _a_reason_for_how_they_are(thing, memory)
        if warmer:
            return warmer
    return _a_new_answer(said, memory)
