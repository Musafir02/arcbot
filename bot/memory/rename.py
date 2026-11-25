
import re

from . import facts as extract

RENAMING = re.compile(
    r"\brenam(?:e|ed|es|ing)\b"
    r"|\bchang(?:e|ed|es|ing)\b[^.?!]{0,24}?\bnames?\b"
    r"|\bchang(?:e|ed|es|ing)\s+(?:it|him|her|them)\s+(?:to|into)\b"
    r"|\bcall\s+(?:him|her|it|them)\b[^.?!]*\bnow\b"
    r"|\banswers?\s+to\b|\bgoes?\s+by\b"
    r"|\bnow\s+(?:called|named)\b"
    r"|\b(?:he|she|it|they)(?:'s|s| is| are)\s+[a-z'-]{2,}\s+now\b"
    r"|\bnow\s+(?:he|she|it|they)(?:'s|s| is)\b", re.I)
AFTER_A_NEW_NAME = frozenset("""now instead please ok okay tbh tho though then actually too also
from onwards today anyway honestly like""".split())
NOT_A_NEW_NAME = frozenset("""it him her them the to as called named name rename renamed
they we i you us me dog cat puppy kitten pet animal""".split())
A_THING_IN_FRONT = frozenset("""the a an this that these those my our his their your its
some any another one""".split())
A_PERSON_IN_THE_LINE = re.compile(
    r"\b(?:son|daughter|mum|mom|mother|father|dad|wife|husband|partner|boyfriend|girlfriend|"
    r"brother|sister|friend|boss|colleague|neighbour|neighbor|child|kid|baby|gran|grandma|"
    r"grandad|grandpa|nan|nana|aunt|uncle|cousin|mate|flatmate|housemate|carer|teacher|"
    r"people|someone|somebody)\b", re.I)
THE_PERSONS_OWN_NAME = re.compile(r"\b(?:my|our)\s+names?\b", re.I)


def moves(low):
    return bool(RENAMING.search(" ".join(str(low or "").split())))


def the_name_it_gave(low):
    words = [word.strip(".,!?;:'\"") for word in str(low or "").split()]
    while words and words[-1].lower() in AFTER_A_NEW_NAME:
        words.pop()
    if not words:
        return ""
    word = words[-1]
    if len(word) < 2 or word.lower() in NOT_A_NEW_NAME:
        return ""
    if len(words) > 1 and words[-2].lower() in A_THING_IN_FRONT:
        return ""
    return word if extract.a_name_could_be(word) else ""


def the_name_a_line_moved_on(low, pets, animal_named):
    low = " ".join(str(low or "").split())
    if not low or A_PERSON_IN_THE_LINE.search(low) or THE_PERSONS_OWN_NAME.search(low):
        return ""
    pets = [pet for pet in (pets or ()) if isinstance(pet, dict)]
    if not pets:
        return ""
    if not animal_named and len([pet for pet in pets if pet.get("name")]) != 1:
        return ""
    return the_name_it_gave(low)
