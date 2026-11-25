import re

from ..compose import fallback, pick
try:
    from ..memory import obstacle as _obstacle
except Exception:
    _obstacle = None

PRIORITY = -960

_LIKES = (
    "Can't argue with {thing}. What do you like most?",
    "{Thing} - good taste. What is it about {thing} that you like?",
    "That is a good thing to like. What do you like most about {thing}?",
)

_DISLIKES = (
    "{Thing} - fair enough. What is it you don't like about {thing}?",
    "Nobody is going to talk you round on {thing}, and nobody needs to. What is it that puts "
    "you off?",
    "Plenty of people would say the same about {thing}. What is it you cannot take about {thing}?",
)

_LIKE_VERBS = (
    "really like", "do like", "love", "like", "adore", "am mad about", "m mad about",
    "am into", "m into", "can't get enough of", "cant get enough of", "can not get enough of",
    "am a fan of", "m a fan of", "am obsessed with", "m obsessed with", "have always loved",
)
_DISLIKE_VERBS = (
    "really don't like", "really dont like", "don't like", "dont like", "hate", "dislike",
    "can't stand", "cant stand", "can not stand", "am not a fan of", "m not a fan of",
    "am not keen on", "m not keen on", "have never liked", "have gone off",
)
_FAN_OF = re.compile(
    r"(?:am|m)\s+(?:a\s+)?(?:\w+\s+){0,2}fan\s+of", re.I)
_TONE = re.compile(
    r"(?:\s+(?:tbh|tho|though|really|honestly|actually|literally|so\s+much|a\s+lot|"
    r"as\s+well|too|now|anyway|i\s+suppose|i\s+guess|lol|ha|haha|btw|atm|lately|"
    r"these\s+days|at\s+the\s+moment|right\s+now|still|again))+$", re.I)
_LEAD = r"(?:(?:oh|god|god,|honestly|yeah|well|actually|man|christ|jesus|blimey)\s+)*"
_THING = re.compile(r"^(?P<thing>[a-z][a-z'\-]*(?:\s+[a-z][a-z'\-]*){0,4})$")
_NOT_A_THING = frozenset((
    "it", "that", "this", "them", "these", "those", "him", "her", "you", "me", "us", "here",
    "there", "everything", "anything", "nothing", "everyone", "someone", "it all", "that one",
    "this one", "one", "ones", "things", "stuff", "life", "my life", "myself", "my job",
    "my work", "people", "the world", "the news", "him too", "her too", "your advice", "advice",
    "your help", "this recipe", "the recipe", "your recipes", "this place", "this app",
    "chatting to you", "talking to you", "you too", "you both", "your voice",
    "much more of this", "more of this", "much more", "any more of this", "it any more",
    "it anymore", "this any more", "this anymore",
))
_A_PERSON = re.compile(
    r"\b(?:girl|boy|woman|man|guy|lad|lass|bloke|fella|someone|somebody|people|person|"
    r"her|him|them|she|he|they)\b", re.I)
_THEIRS_BUT_NOT_A_THING = re.compile(
    r"\b(?:mum|mom|mother|dad|father|son|daughter|kid|kids|child|children|wife|husband|partner|"
    r"baby|gran|grandma|grandmother|nan|nana|grandad|grandpa|grandfather|aunt|uncle|cousin|"
    r"sister|brother|parents|family|dog|cat|puppy|kitten|pets?|bird|horse|rabbit|hamster|"
    r"boss|friend|mate|neighbours?|self|life|job|work|body|looks|health|mind|sleep)\b", re.I)
_NOT_A_TASTE = re.compile(
    r"\b(?:my life|myself|my job|my work|my body|my looks|the world|people|mondays?\s+morning)\b",
    re.I)

_I_SAY = r"^(?:i|i'm|i've)\s+"
_TYPED = (("im ", "i am "), ("i m ", "i am "), ("ive ", "i have "))

_STORY = re.compile(
    r"\b(?:but|because|so|though|although|when|whenever|if|since|which|that|keeps?|"
    r"makes?|gets?|goes?|go|went|got|costs?|cost|is|are|was|were|will|would|can|could|"
    r"have|has|had|need|needs|want|wants|helps?|works?|tastes?|smells?)\b"
    r"|\band\s+(?:i|it|its|it's|they|we|you|he|she|there|thats|that's)\b", re.I)

_HEAVY = re.compile(
    r"\b(?:ill|unwell|poorly|sick|dying|died|death|passed away|funeral|bereave\w*|griev\w*|"
    r"cancer|chemo\w*|radiotherap\w*|tumou?r|dementia|alzheim\w*|stroke|sepsis|surgery|"
    r"operation|transplant|hospice|palliative|terminal|hospital|icu|ambulance|diagnos\w*|"
    r"bully\w*|bullied|depress\w*|suicid\w*|self harm|miscarr\w*|stillborn|addict\w*|"
    r"relapse\w*|overdose\w*|sectioned|in pain|suffering)\b", re.I)


_PLACEHOLDER_OPENINGS = (
    "noted", "got it", "i'm listening", "i am listening", "thanks for telling me",
    "that's noted", "thats noted", "ok.", "okay.", "i don't know enough",
    "i dont know enough", "that's beyond what i know", "thats beyond what i know",
    "i'm not sure about that one", "im not sure about that one",
)


def _the_composer_would_answer(text, memory):
    try:
        reply = fallback.reply_for(text, memory)
    except Exception:
        return False
    said = " ".join(str(reply or "").lower().split())
    if not said:
        return False
    if any(said.startswith(opening) for opening in _PLACEHOLDER_OPENINGS):
        return False
    return True


def _the_greeting_would_answer(text, memory):
    try:
        from . import greeting
    except Exception:
        return False
    try:
        reply = greeting.respond(text, memory)
    except Exception:
        return False
    said = " ".join(str(reply or "").lower().split())
    if not said:
        return False
    if any(said.startswith(opening) for opening in _PLACEHOLDER_OPENINGS):
        return False
    return True


def _the_line_before(memory):
    turns = [turn for turn in ((memory or {}).get("turns") or []) if isinstance(turn, dict)]
    return str(turns[-1].get("user") or "") if turns else ""


def _the_thread_is_heavy(memory):
    before = _the_line_before(memory)
    if not before:
        return False
    try:
        if fallback._reads_as_heavy_news(before):
            return True
    except Exception:
        pass
    return bool(_HEAVY.search(before))


def _said_plainly(clean):
    said = clean
    for typed, proper in _TYPED:
        if said.startswith(typed):
            said = proper + said[len(typed):]
    said = re.sub(r"^" + _LEAD, "", said)
    changed = True
    while changed:
        stripped = _TONE.sub("", said)
        changed = stripped != said
        said = stripped
    return said.strip()


def _a_taste(clean):
    if not clean or "?" in clean:
        return None
    for kind, verbs, pool in (("like", _LIKE_VERBS, _LIKES), ("dislike", _DISLIKE_VERBS, _DISLIKES)):
        for verb in verbs + (_FAN_OF.pattern,):
            head = _I_SAY + (verb if verb is _FAN_OF.pattern else re.escape(verb)) + r"\s+"
            match = re.match(head, clean, re.I)
            if not match:
                continue
            rest = clean[match.end():].strip()
            if not rest or _STORY.search(rest):
                continue
            thing = _THING.match(rest)
            if not thing:
                continue
            rest = thing.group("thing")
            if rest in _NOT_A_THING or _A_PERSON.search(rest):
                continue
            if kind == "dislike" and _NOT_A_TASTE.search(rest):
                continue
            first = rest.split()[0]
            if first in ("to", "your", "our", "it", "that", "this", "them", "here", "there"):
                continue
            if first == "my":
                held = rest[3:].strip()
                if not held or _THEIRS_BUT_NOT_A_THING.search(held):
                    continue
            if re.match(r"^(?:your|this|that|these|those)\s+", rest):
                continue
            return kind, rest
    return None


def _the_thing_said(thing):
    words = thing.split()
    if words and words[0] == "my":
        words[0] = "your"
    return " ".join(words)


def _pick(pool, memory, said):
    return pick(pool, memory, said or "")


def _the_reply(kind, thing, memory):
    thing = _the_thing_said(thing)
    pool = _LIKES if kind == "like" else _DISLIKES
    line = _pick(pool, memory, " ".join(str(thing).split()))
    return line.replace("{Thing}", thing[:1].upper() + thing[1:]).replace("{thing}", thing)


def respond(text, memory):
    if not isinstance(text, str):
        return None
    clean = _said_plainly(" ".join(text.lower().split()))
    if not clean or "?" in clean:
        return None
    taste = _a_taste(clean)
    if not taste:
        return None
    if not isinstance(memory, dict):
        memory = {}
    if _the_thread_is_heavy(memory):
        return None
    if _obstacle is not None:
        try:
            if _obstacle.answer_for(text, memory):
                return None
        except Exception:
            pass
    if _the_composer_would_answer(text, memory):
        return None
    if _the_greeting_would_answer(text, memory):
        return None
    kind, thing = taste
    return _the_reply(kind, thing, memory)
