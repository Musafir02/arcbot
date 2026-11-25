import re

BREED_KIND = {
    "labrador": "dog", "lurcher": "dog", "greyhound": "dog", "whippet": "dog",
    "terrier": "dog", "spaniel": "dog", "retriever": "dog", "collie": "dog",
    "poodle": "dog", "beagle": "dog", "bulldog": "dog", "pug": "dog", "husky": "dog",
    "chihuahua": "dog", "dachshund": "dog", "dalmatian": "dog", "mastiff": "dog",
    "rottweiler": "dog", "doberman": "dog", "dobermann": "dog", "alsatian": "dog",
    "corgi": "dog", "staffie": "dog", "mongrel": "dog", "cockapoo": "dog",
    "labradoodle": "dog", "cavapoo": "dog", "pomeranian": "dog", "papillon": "dog",
    "schnauzer": "dog", "weimaraner": "dog", "vizsla": "dog", "samoyed": "dog",
    "akita": "dog", "shar pei": "dog", "lhasa apso": "dog", "afghan hound": "dog",
    "basset hound": "dog", "border collie": "dog", "cocker spaniel": "dog",
    "golden retriever": "dog", "labrador retriever": "dog", "jack russell": "dog",
    "german shepherd": "dog", "shih tzu": "dog", "staffordshire bull terrier": "dog",
    "bull terrier": "dog", "yorkshire terrier": "dog", "westie": "dog",
    "west highland terrier": "dog",
    "siamese": "cat", "ragdoll": "cat", "moggy": "cat", "tabby": "cat",
    "tortoiseshell": "cat", "sphynx": "cat", "maine coon": "cat",
    "british shorthair": "cat", "scottish fold": "cat",
}
MONEY = frozenset("""
money quid tenner tenners grand odds punter winnings bet bets betting stake stakes
""".split())
LOOSE_FRAME = frozenset("the a an that these those this".split())
NOT_A_CREATURE_NEXT = frozenset("""
bus buses coach coaches station stations line lines service services depot depots ticket
tickets terminal terminals timetable timetables racing race races derby stadium track kennel
kennels club breeder breeders rescue glasses frames sunglasses sofa sofas rug rugs curtains
upholstery twin twins person people
""".split())
FRAME_BEFORE = frozenset("""my our his her their the a an another this that these those
got get gets have has had having keep keeps kept kept buy buys bought take takes took rescue
rescued adopt adopted rehome rehomed""".split())
FRAME_REACH = 4
BY_WORD = re.compile(r"^[a-z][a-z'-]*$")


def _singular(word):
    if word in BREED_KIND:
        return word
    if word.endswith("ies") and word[:-3] + "y" in BREED_KIND:
        return word[:-3] + "y"
    if word.endswith("es") and word[:-2] in BREED_KIND:
        return word[:-2]
    if word.endswith("s") and word[:-1] in BREED_KIND:
        return word[:-1]
    return ""


def the_animal_a_breed_is(words):
    if not isinstance(words, list) or not words:
        return words
    low = [word.lower() if isinstance(word, str) else "" for word in words]
    filled = []
    index = 0
    while index < len(low):
        found = ""
        span = 1
        for length in (4, 3, 2):
            phrase = " ".join(low[index:index + length])
            if len(phrase.split()) == length and BREED_KIND.get(_singular(phrase)):
                found, span = BREED_KIND[_singular(phrase)], length
                break
        if not found:
            found = BREED_KIND.get(_singular(low[index]), "")
        after = low[index + span] if index + span < len(low) else ""
        reachable = low[max(0, index - FRAME_REACH):index]
        frame_words = [word for word in reachable if word in FRAME_BEFORE]
        framed = bool(frame_words)
        if found and framed:
            if after in NOT_A_CREATURE_NEXT:
                framed = False
            elif (all(word in LOOSE_FRAME for word in frame_words)
                  and any(word in MONEY for word in low)):
                framed = False
        if found and framed:
            filled.extend(words[index:index + span])
            filled.append(found)
            index += span
            continue
        filled.append(words[index])
        index += 1
    if len(filled) == len(words):
        return words
    return filled

def a_frame_before(text, start):
    before = re.findall(r"[a-z']+", text[:max(0, start)].lower())[-FRAME_REACH:]
    return any(word in FRAME_BEFORE for word in before)


def the_breed_named(text):
    word = " ".join(str(text or "").lower().split())
    return _singular(word)


def the_kind_of(word):
    return BREED_KIND.get(the_breed_named(word), "")


def _alternation():
    names = sorted(BREED_KIND, key=lambda name: (-len(name.split()), -len(name)))
    return "|".join(name.replace(" ", r"\s+") for name in names)


BREED_RE = re.compile(r"\b(?:" + _alternation() + r")(?:s|es)?\b", re.I)
