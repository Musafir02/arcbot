import re

from .fallback_data import BODY_PARTS

A_STATE = frozenset((
    "long", "overgrown", "dirty", "filthy", "grimy", "mucky", "tatty", "shabby", "scruffy",
    "worn out", "worn", "messy", "untidy", "dusty", "faded", "rusty", "grim", "cluttered",
    "piled up", "manky", "minging", "grubby",
))

A_PERSON = frozenset("""
mum mom mam dad father mother son daughter child children kid kids baby toddler boy girl husband
wife partner boyfriend girlfriend brother sister mate mates friend friends nan granny grandma
grandad grandpa aunt uncle cousin neighbour neighbor boss colleague client cat dog puppy kitten
puppies rabbit hamster horse hens chickens bird birds fish
""".split())

A_FEELING = frozenset("""
sick tired fed up had enough annoyed angry cross sad upset stressed worried depressed
embarrassed ashamed guilty lonely done exhausted shattered
""".split())

THE_THING_IS = re.compile(
    r"^(?:the|my|our|your|his|her|their)\s+(?P<thing>[a-z]+(?:\s+[a-z]+)?)\s+"
    r"(?:is|are|looks|seems|gets|got)\s+(?:a bit |a little |really |very |so |quite |"
    r"proper |right |pretty |well )?(?P<state>worn out|piled up|[a-z]+)\s*$", re.I)

A_THING_WANTS_DOING = (
    "How bad is it — something you can do in an hour, or has it got away from you?",
    "What's the job on it? I'll work the next step out with you.",
    "Tell me how bad it is and I'll work out where to start.",
    "Right. How long has it been like that?",
    "Where would you start with it?",
)


def reads(text, memory=None):
    flat = " ".join(str(text or "").lower().split())
    if not flat or len(flat.split()) > 8:
        return None
    if any(word in A_FEELING for word in flat.split()):
        return None
    found = THE_THING_IS.match(flat)
    if not found:
        return None
    state, thing = found.group("state"), found.group("thing")
    if state not in A_STATE:
        return None
    if any(word in A_PERSON or word in BODY_PARTS for word in thing.split()):
        return None
    return thing


def pool(text, memory=None):
    if not reads(text, memory):
        return None
    return A_THING_WANTS_DOING
