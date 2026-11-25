import re
import string

from . import topics

PRONOUNS = {
    "it": ("it", "its", "itself"),
    "that": ("that", "this", "these", "those", "one", "ones"),
    "they": ("they", "them", "their", "theirs"),
    "there": ("there",),
    "he": ("he", "him", "his", "himself"),
    "she": ("she", "her", "hers", "herself"),
}
FOLLOWUP_STARTS = (
    "and", "also", "but", "so", "what about", "how about", "what if", "and what", "then",
    "why", "how long", "how much", "how many", "how often", "when", "where", "which",
    "same", "another", "more", "else", "other", "instead", "so that", "ok and", "ok so",
    "even if", "does it", "is it", "can it", "will it", "does that", "is that", "can that",
    "will that", "would it", "should it", "what else", "anything else", "and then",
)
POINTING_BACK = frozenset("""on in at with to for from by under over near into onto around
    inside outside about off through across behind beside""".split())
ASK_OPENERS = frozenset("""will would shall should can could do does did may might must""".split())
WHERE_WORDS = frozenset("there where place city area town country".split())
CLAUSE_SUBJECTS = frozenset("""i you we they he she it there its im ive dont cant thats""".split())
TIME_RE = re.compile(r"^(and|also|but|so)\b")


def _target(prev_line, prev_entities, prev_topic):
    things = [entity for entity in prev_entities if entity["type"] == "thing"]
    if things:
        words, at = [things[0]["text"]], things[0]["at"]
        for later in things[1:]:
            if later["at"] == at + 1:
                words.append(later["text"])
                at = later["at"]
        return " ".join(words).lower(), "thing"
    for kind in ("title", "name", "place", "person"):
        for entity in prev_entities:
            if entity["type"] == kind:
                return entity["text"].lower(), kind
    if prev_topic:
        return prev_topic.replace("-", " "), "topic"
    return None, None


def _person(prev_entities, fallback):
    for kind in ("name", "title", "person"):
        for entity in prev_entities:
            if entity["type"] == kind:
                return entity["text"].lower()
    return fallback


def _place(prev_entities, prev_topic):
    for entity in prev_entities:
        if entity["type"] == "place":
            return entity["text"].lower()
    return prev_topic.replace("-", " ") if prev_topic == "geography-and-travel" else None


OWN_THINGS = ("title", "name", "person", "place", "thing")
OWN_PERSONS = ("title", "name", "person")


def _moved(read, prev_topic):
    topic = read.get("topic")
    if not topic or not prev_topic:
        return False
    return topic != prev_topic


def _has_moved(line, prev_topic):
    if not prev_topic:
        return False
    own, _ = topics.detect_topic(line, None, topics.detect_entities(line))
    return bool(own) and own != prev_topic


DETERMINERS = frozenset("""a an the this these those that my your his her its our their
    some any each every another""".split())
COORDINATORS = frozenset("and but so then".split())
POSSESSIVE_PRONOUNS = frozenset("its their".split())
PRONOUN_WORDS = frozenset(word for forms in PRONOUNS.values() for word in forms)
CLAUSE_STOPS = frozenset("""is was are were be been am do does did have has had will would can
    could should to of in on at for from with by if when because so that which who""".split())


def _a_thing_of_its_own(norm, at, word):
    opened = _last_noun_phrase(norm, at)
    if opened is None:
        return False
    if word in POSSESSIVE_PRONOUNS:
        return True
    return any(other in COORDINATORS for other in norm[opened:at])


def _last_noun_phrase(norm, at):
    for index in range(at - 2, max(-1, at - 12), -1):
        word = norm[index]
        if word in DETERMINERS and index + 1 < at:
            return index
        if word in PRONOUN_WORDS:
            return None
    return None


def _named_before(line, names, moved=True):
    norm = line["norm"]
    people = [entity.get("at", 0) for entity in topics.detect_entities(line)
              if entity.get("type") in OWN_PERSONS]
    found = []
    for name in names:
        at = next((i for i, word in enumerate(norm) if word in PRONOUNS[name]), None)
        if at is None:
            continue
        if at and norm[at - 1] in POINTING_BACK:
            continue
        if _asks_about(line, (name,)):
            continue
        named = any(spot < at for spot in people)
        if not named and moved:
            named = _a_thing_of_its_own(norm, at, norm[at])
        if not named:
            continue
        found.append(name)
    return found


def _asks_about(line, names):
    aliases = set()
    for name in names:
        aliases.update(PRONOUNS[name])
    for clause in line.get("clauses") or ():
        if clause and clause[0] in ASK_OPENERS and aliases & set(clause[:3]):
            return True
    return False


ONE_PERSON = ("he", "him", "his", "she", "her", "hers")


def person_is_new(line, prev_entities):
    people_here = bool(topics.person_names(line)) or any(
        entity.get("type") == "person" for entity in topics.detect_entities(line))
    if not people_here and not set(line.get("norm") or ()) & set(ONE_PERSON):
        return False
    return not any(entity.get("type") == "person" for entity in prev_entities or ())


def _only_the_purpose(line):
    norm = line["norm"]
    if len(norm) < 2 or norm[0] != "to":
        return False
    return not (set(norm[1:]) & CLAUSE_SUBJECTS)


PLACEHOLDER_IT = re.compile(
    r"^(?:is|was|would|will|does|did|can|could|should)(?:n'?t)?\s+it\s+"
    r"(?:[a-z']+\s+){0,3}?to\s+[a-z]+")
NAMES_A_THING = re.compile(
    r"\b(?:a|an|the|some|any|my|your|our|their|his|her|its|another)\s+[a-z]", re.I)
STANDS_FOR_SOMETHING = frozenset("""it its them they that this these those him her one ones
    there""".split())
LEAVES_SOMETHING_OUT = frozenset("""after before then while during since until till instead
    without with on in at for to from about when if and but or that""".split())


def _a_placeholder_it(line):
    said = " ".join(line["norm"])
    frame = PLACEHOLDER_IT.match(said)
    if not frame:
        return False
    rest = said[frame.end():]
    if NAMES_A_THING.search(rest):
        return False
    if set(rest.split()) & STANDS_FOR_SOMETHING:
        return False
    tail = rest.split()[-1:]
    return not (tail and tail[0] in LEAVES_SOMETHING_OUT)


ANIMALS_IN_HAND = re.compile(
    r"\b(dogs?|pupp(?:y|ies)|cats?|kittens?|rabbits?|bunn(?:y|ies)|hamsters?|guinea\s+pigs?"
    r"|parrots?|budgies?|goldfish|fish|tortoises?|turtles?|snakes?|lizards?|geckos?|horses?"
    r"|pon(?:y|ies))\b", re.I)
OWN_SUBJECT = frozenset("""i im ive id ill we weve wed""".split())
WITHOUT_THE_APOSTROPHE = {"he": ("hes", "hed", "hisself"), "she": ("shes", "shed"),
                          "they": ("theyre", "theyd", "theyll")}
ANIMAL_NAMES = frozenset("""dog dogs puppy puppies cat cats kitten kittens""".split())


def _the_breed_in(text):
    from .breeds import BREED_KIND, the_animal_a_breed_is
    whole = str(text or "").strip().lower()
    if BREED_KIND.get(whole):
        return BREED_KIND[whole]
    said = re.findall(r"[a-z']+", str(text or "").lower())
    if not said:
        return ""
    filled = the_animal_a_breed_is(list(said))
    if not isinstance(filled, list) or len(filled) <= len(said):
        return ""
    index = 0
    for piece in filled:
        if index < len(said) and piece == said[index]:
            index += 1
            continue
        return str(piece).lower()
    return ""


def _the_pronouns(name):
    return frozenset(PRONOUNS[name]) | frozenset(WITHOUT_THE_APOSTROPHE.get(name, ()))


THIRD_PERSON = frozenset(word for name in PRONOUNS for word in PRONOUNS[name])
MINE = frozenset("""my mine our ours""".split())


def the_animal_the_chat_is_on(words, last_read):
    if not isinstance(last_read, dict):
        return ""
    animal = str(last_read.get("animal_in_hand") or "").lower()
    if not animal:
        return ""
    bare = set()
    for word in words or ():
        bare.add(str(word).lower().strip(string.punctuation + "\u2019").split("'")[0])
    if bare & ANIMAL_NAMES or bare & MINE:
        return ""
    if not bare & THIRD_PERSON:
        return ""
    return animal


def the_animal_in_hand(ref, words):
    if not isinstance(ref, dict) or not ref.get("followup"):
        return ""
    bare = set()
    for word in words or ():
        bare.add(str(word).lower().strip(string.punctuation + "\u2019").split("'")[0])
    if bare & OWN_SUBJECT or bare & ANIMAL_NAMES:
        return ""
    for name in PRONOUNS:
        if not bare & _the_pronouns(name):
            continue
        said = str(ref.get(name) or "")
        animal = ANIMALS_IN_HAND.search(said)
        if animal:
            return animal.group(0).lower()
        breed = _the_breed_in(said)
        if breed:
            return breed
    return ""


def resolve(line, read, prev_line=None, prev_entities=None, prev_topic=None):
    prev_entities = prev_entities or []
    words = set(line["norm"])
    used = {name: next((p for p in aliases if p in words), None)
            for name, aliases in PRONOUNS.items()}
    ref = {"it": None, "that": None, "they": None, "there": None, "he": None, "she": None,
           "kind": None, "followup": False}
    if prev_line is None:
        return ref

    target, kind = _target(prev_line, prev_entities, prev_topic)
    person = _person(prev_entities, target)
    reference = bool(used["it"] or used["that"] or used["they"] or used["there"]
                     or used["he"] or used["she"])
    placeholder = _a_placeholder_it(line)
    starts = " ".join(line["norm"][:4])
    opens_like_followup = any(starts == phrase or starts.startswith(phrase + " ")
                              for phrase in FOLLOWUP_STARTS) or _only_the_purpose(line)
    if placeholder and not (used["that"] or used["they"] or used["there"]
                            or used["he"] or used["she"]):
        opens_like_followup = False
        asks_without_topic = False
    short = len(line["norm"]) <= 3 and read["kind"] not in ("greeting", "thanks")
    adds_topic = topics.subject_topic(line, topics.detect_entities(line)) is not None
    asks_without_topic = read["kind"] == "question" and not adds_topic

    ref["kind"] = kind
    if reference and placeholder and not (used["that"] or used["they"] or used["there"]
                                          or used["he"] or used["she"]):
        reference = False
    if reference:
        ref["it"] = target
        ref["that"] = target
        ref["they"] = target
        ref["he"] = person
        ref["she"] = person
    ref["there"] = _place(prev_entities, prev_topic)
    ref["followup"] = bool(reference or opens_like_followup or short or asks_without_topic)
    named_first = _named_before(line, ("it", "that", "they", "there"),
                                moved=_moved(read, prev_topic) or _has_moved(line, prev_topic))
    for name in named_first:
        ref[name] = None
        if name in ("they", "that"):
            ref["he"] = ref["she"] = None
    pointed_back = [name for name in ("it", "that", "they", "there") if used[name]]
    if pointed_back and set(pointed_back) == set(named_first) and not (used["he"] or used["she"]):
        ref["followup"] = bool(opens_like_followup or short or asks_without_topic)
    return ref
