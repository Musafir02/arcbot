import re

KIN = (r"(?:dad|daddy|father|mum|mummy|mother|mam|nan|nanna|gran|granny|grandma|grandad|"
       r"grandpa|granddad|son|daughter|child|kid|boy|girl|baby|little one|husband|wife|"
       r"partner|other half|boyfriend|girlfriend|brother|sister|niece|nephew|cousin|aunt|"
       r"uncle|friend|mate|neighbour|carer|flatmate|housemate|in laws|in-law)")
NAMED_SOMEBODY = re.compile(
    rf"\b(?:my|our|his|her|their)\s+(?:poor\s+|little\s+|eldest\s+|youngest\s+|old\s+|older\s+|"
    rf"elderly\s+|grown\s*up\s+)?{KIN}\b", re.I)
PRONOUN_BODY = re.compile(
    r"\b(?:he|she|they|hed|shed|theyd)(?:'s|s|\s+is|\s+has|\s+had|\s+got|\s+has\s+got|"
    r"\s+keeps\s+getting|\s+was|\s+been)\b[^.!?]{0,26}?"
    r"\b(?:bad|sore|dodgy|gammy|weak|dicky|knackered|broken|cracked|twisted|swollen|stiff|"
    r"aching|hurting|hurts?|soreness|pain|stiffness|giving\s+him\s+trouble)\b"
    r"|\b(?:his|her|their)\s+(?:[a-z]+\s+){0,2}(?:hip|knee|back|shoulder|leg|arm|foot|feet|"
    r"hand|wrist|ankle|neck|stomach|chest|head|eye|ear|joints?)\b[^.!?]{0,18}?"
    r"\b(?:is|are|feels?|has\s+been|keeps)\b", re.I)
OWN_BODY = re.compile(r"\b(?:my|our)\s+(?:[a-z]+\s+){0,2}(?:hip|knee|back|shoulder|leg|arm|"
                      r"foot|feet|hand|wrist|ankle|neck|stomach|chest|head|eye|ear|joints?)\b",
                      re.I)


PET = re.compile(r"\b(?:dog|dogs|puppy|pup|cat|cats|kitten|rabbit|bunny|hamster|guinea\s+pig|"
                 r"horse|pony|budgie|parrot|bird|fish|tortoise|snake|lizard|ferret|gerbil)\b",
                 re.I)


def somebody_was_named(memory):
    try:
        turns = memory.get("turns") if isinstance(memory, dict) else None
    except AttributeError:
        return False
    if not isinstance(turns, list):
        return False
    for turn in reversed(turns[-4:]):
        if not isinstance(turn, dict):
            continue
        said = str(turn.get("user") or "")
        if PET.search(said):
            return False
        if NAMED_SOMEBODY.search(said):
            return True
    return False


def a_body_of_a_pronoun(clean):
    text = str(clean or "")
    if OWN_BODY.search(text):
        return False
    return bool(PRONOUN_BODY.search(text))


def somebody_elses_body(clean, memory):
    return a_body_of_a_pronoun(clean) and somebody_was_named(memory)
