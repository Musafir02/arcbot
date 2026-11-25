import re

from . import pick

_FRONT = (r"(?:(?:and|oh|ooh|ok|okay|so|right|ah|er|um|umm|hmm|sorry|also|just|plus|hey|ta|"
          r"anyway|anyways|first|then|actually|also)\b[\s,]+)*")
BACK = (r"(?:\s+(?:actually|too|as well|then|now|first|ok|okay|sorry|thanks|tho|though|"
        r"i think|i suppose|i reckon))?")
_CORE = (
    r"(?:one|two|three|a couple|a few|couple)(?: more| other| final| last)"
    r" (?:things?|questions?|qs?|asks?|quer(?:y|ies)|bits?|points?|ones?)"
    r"|another (?:things?|questions?|qs?|asks?|ones?|points?|quer(?:y|ies))"
    r"|(?:one |the |a )?(?:last|final|next|other|second) "
    r"(?:things?|questions?|qs?|asks?|ones?|bits?)"
    r"|a? ?quick (?:ones?|questions?|qs?|asks?|things?|quer(?:y|ies))"
    r"|(?:a |one |an )?(?:different|separate|unrelated|side) "
    r"(?:questions?|ones?|asks?|things?|quer(?:y|ies))"
    r"|one thing more"
    r"|before i forget"
    r"|while (?:im|i am) (?:here|at it)"
)

HANDOFF = re.compile(
    "^" + _FRONT + "(?:" + _CORE + ")" + BACK + r"[\s.?!,]*$", re.IGNORECASE)

ABOUT = re.compile(
    "^" + _FRONT + "(?:" + _CORE + ")" + BACK + r"[\s,:-]*(?:about|on|to do with|regarding|"
    r"around)\s+(?P<thing>(?:(?:the|my|our|your|his|her|their|its|a|an|this|that)\s+)?"
    r"[\w'-]+(?:\s+[\w'-]+){0,3})[\s.?!,]*$", re.IGNORECASE)
_POINTS_AT_NOTHING = frozenset((
    "it", "that", "this", "them", "they", "us", "you", "me", "him", "her", "there", "things",
    "thing", "stuff", "everything", "nothing", "something", "anything", "it all", "the lot",
))

_NOT_A_SUBJECT = frozenset((
    "whether", "if", "how", "what", "when", "why", "where", "who", "whom", "which", "that",
    "because", "so", "but", "and",
))

ABOUT_THE_THING = (
    "Go on — what about {thing}?",
    "Ask away about {thing}.",
    "{Thing} — right. What do you want to know?",
    "What about {thing}? I'm listening.",
)


def reads_as_handoff_about_a_thing(text):
    clean = " ".join(str(text or "").lower().split())
    found = ABOUT.match(clean)
    if not found:
        return None
    thing = found.group("thing").strip(" ,.?!:-")
    if not thing or thing.split()[0] in _POINTS_AT_NOTHING:
        return None
    if thing in _POINTS_AT_NOTHING or thing.split()[0] in _NOT_A_SUBJECT:
        return None
    return thing

_NAMES_A_QUESTION = re.compile(r"\b(?:question|questions|q|qs|ask|asks|query|queries)\b",
                               re.IGNORECASE)

ASK_AWAY = (
    "Ask away.",
    "Sure — what is it you want to know?",
    "Go on, I'm listening.",
    "Yes, ask away — I'm here.",
)

GO_ON = (
    "Go on — what is it?",
    "Sure, go ahead.",
    "I'm listening — tell me.",
    "Yes, what else?",
    "Go ahead, I'm here.",
)


def reads_as_handoff(text):
    return bool(HANDOFF.match(" ".join(str(text or "").lower().split())))


def takes_as_it_comes(text, memory):
    return reads_as_handoff(text) or bool(reads_as_handoff_about_a_thing(text))


def reply_for(text, memory):
    clean = " ".join(str(text or "").lower().split())
    thing = reads_as_handoff_about_a_thing(clean)
    if thing:
        lines = tuple(line.format(thing=thing, Thing=thing[0].upper() + thing[1:])
                      for line in ABOUT_THE_THING)
        return pick(lines, memory, clean)
    if not HANDOFF.match(clean):
        return None
    return pick(ASK_AWAY if _NAMES_A_QUESTION.search(clean) else GO_ON, memory, clean)
