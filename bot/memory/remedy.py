import random
import re

ATTEMPT = re.compile(
    r"^\W*(?:(?:and|but|so|oh|ok|okay|well|right|alright)\s+)?"
    r"(?:i|i've|ive|i'd|we|we've|weve)\s*"
    r"(?:have\s+|had\s+|just\s+|already\s+|also\s+|finally\s+)?"
    r"(?P<verb>tried|took|used|gave|been using|been trying)\s+(?P<thing>.+)$")

A_THING_LEADS = re.compile(
    r"^(?:a|an|the|some|my|his|her|their|our|that|this|one|two|three)\b", re.I)

VERDICT = re.compile(
    r"\b(?:did\s?n'?t|does\s?n'?t|not|no|never|helped|helps|worked|works|better|worse|"
    r"relief|eased|eases|nothing|useless|pointless|yet|again|still)\b", re.I)

POINTING = frozenset("""that this it them those these everything all anything something
nothing""".split())

A_PROBLEM = frozenset("""hurt hurts hurting hurtful pain painful ache aches aching achy achey sore
ill sick illness unwell cough coughing cold flu headache migraine fever temperature back knee
shoulder neck ankle wrist hip throat stomach belly tooth toothache ear earache rash itch itchy burn
burnt sprain sprained stiff stiffness swelling swollen dizzy faint sleep
sleeping slept insomnia wake waking wakes sneeze sneezing blocked stuffy running congestion
bleeding bleed cut bruise bruised lump dizzy nausea sick vomit diarrhoea constipated constipation heartburn
reflux bloat bloated cramp cramps period contractions
dripping drips leaking leaks leaked leak broken broke cracked squeaks squeaking squeak clogged
blocked banging rattling stuck jammed seized mould mildew damp stains stained smell smells
wont won'ts starts start starting
freezing freezes frozen slow slowly crashing crashes crashed glitching lagging laggy dropping
drops disconnects restart reboots overheating""".split())

ADVICE_MODULES = frozenset(("answers", "safety"))

ASK_IF_IT_HELPED = (
    "Did the {thing} take the edge off, or nothing?",
    "{Thing} - did that do anything?",
    "And did the {thing} make a difference?",
    "{Thing} - any help at all?",
    "How did the {thing} go - anything, or no difference?",
)

LEADS = re.compile(
    r"^(?:and|but|so|oh|ok|okay|well|right|alright)\s+", re.I)

NOT_THE_THING = frozenset("""to for at in on with about of it that this""".split())


def reply_for(text, memory):
    said = " ".join(str(text or "").lower().split())
    if not said:
        return ""
    match = ATTEMPT.match(said)
    if not match:
        return ""
    thing = _the_thing(match.group("thing"), match.group("verb"))
    if not thing:
        return ""
    if VERDICT.search(match.group("thing")[len(thing):] or ""):
        return ""
    if not _a_problem_was_spoken_of(memory) or not _advice_was_given(memory):
        return ""
    options = [_fill(template, thing) for template in ASK_IF_IT_HELPED]
    return _fresh(options, memory)


def _the_thing(rest, verb):
    said = str(rest or "").lower()
    said = re.split(r"\b(?:but|so|then|though|because|again|twice|afterwards)\b", said)[0]
    said = re.split(r"\band\b(?=\s+(?:it|its|it's|they|i|we|now|still|nothing|didnt|doesnt|"
                    r"no\b|the\s+\w+\s+(?:did|helped|worked)))", said)[0]
    words = re.findall(r"[a-z0-9']+", said)
    if not words or words[0] in POINTING or words[0] in NOT_THE_THING or words[0] == "to":
        return ""
    if verb == "gave":
        if words[-2:] != ["a", "go"] and words[-2:] != ["a", "try"]:
            return ""
        words = words[:-2]
    words = words[:5]
    while words and words[-1] in ("a", "an", "the", "some", "my", "our", "their"):
        words.pop()
    while words and words[0] in ("a", "an", "the", "some", "my", "our", "their", "his", "her",
                                 "of", "that", "this"):
        if len(words) < 2:
            return ""
        words = words[1:]
    if words and words[0] in ("of",):
        words = words[1:]
    return " ".join(words)


def _advice_was_given(memory):
    turns = [turn for turn in (memory.get("turns") or []) if isinstance(turn, dict)] \
        if isinstance(memory, dict) else []
    for turn in turns[-4:][::-1]:
        module = str(turn.get("module") or "")
        if module in ADVICE_MODULES:
            return True
        reply = str(turn.get("bot") or "").strip()
        if re.search(r"\b(?:try|trying|keep|rest|ice|see (?:a|your) (?:gp|doctor))\b",
                     reply.lower()):
            return True
        if reply.endswith("?"):
            return True
    return False


def _a_problem_was_spoken_of(memory):
    turns = [turn for turn in (memory.get("turns") or []) if isinstance(turn, dict)] \
        if isinstance(memory, dict) else []
    words = set()
    for turn in turns[-3:]:
        words.update(re.findall(r"[a-z']+", str(turn.get("user") or "").lower()))
    return bool(words & A_PROBLEM)


def _fill(template, thing):
    return template.format(thing=thing, Thing=thing[:1].upper() + thing[1:])


def _fresh(options, memory):
    said = " ".join(str(turn.get("bot") or "") for turn in (memory.get("turns") or [])
                    if isinstance(turn, dict)) if isinstance(memory, dict) else ""
    unseen = [option for option in options if option.lower() not in said.lower()]
    pool = unseen or list(options)
    return random.Random(len(memory.get("turns") or []) if isinstance(memory, dict) else 0).choice(pool)
