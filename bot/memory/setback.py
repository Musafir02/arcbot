import re

VAGUE = re.compile(r"""\b(?:
        went\s+wrong | gone\s+wrong
      | (?:was|were|has\s+been|have\s+been|turned\s+out)\s+(?:a\s+|an\s+)?
        (?:(?:bit\s+of\s+a|total|complete|real|proper|right|absolute|utter|huge|massive|
             big)\s+)?
        (?:disaster|catastrophe|flop|washout|shambles|nightmare)
      | went\s+badly | went\s+pear[\s-]?shaped | came\s+out\s+wrong
    )\b""", re.X)

NOW = re.compile(r"""\b(?:is|are|'s|'re)\s+(?:really\s+|properly\s+|still\s+|just\s+)?
    (?:
        killing\s+me | doing\s+my\s+(?:head|nut)\s+in
      | driving\s+me\s+(?:mad|crazy|nuts|insane|up\s+the\s+wall|round\s+the\s+bend)
    )
  | \b(?:is|are|'s|'re)\s+(?:really\s+|still\s+|all\s+|just\s+)?going\s+wrong\b
  # The same thing said as a gradual decline rather than a fault: "the training is going
  # badly", "the lessons are not going well", "its going badly". Read as a fact to file, each of
  # these was answered "Got it - the training is going badly", which is the coldest reply in
  # STYLE.md on a line that has just handed over something going wrong.
  | \b(?:isn['\u2019]?t|aren['\u2019]?t|is\s+not|are\s+not|not)
    \s+going\s+(?:well|great|smoothly|to\s+plan|right)\b
  | \b(?:is|are|'s|'re|was|were)\s+(?:really\s+|still\s+|all\s+|just\s+)*
    going\s+(?:badly|awfully|terribly|wrong)\b
  | \bits\s+(?:all\s+|really\s+|still\s+|just\s+)?
    (?:not\s+going\s+(?:well|great|smoothly|to\s+plan|right)|going\s+(?:badly|awfully|terribly|wrong))\b
  | \b(?:is|are|'s|'re)\s+(?:a\s+|an\s+)?
    (?:(?:bit\s+of\s+a|total|complete|real|proper|right|absolute|utter|huge|massive|big)\s+)?
    (?:disaster|catastrophe|nightmare|shambles)\b
  # A thing of theirs wearing them down over time: "work has been getting me down lately",
  # "the commute is getting me down", "my job gets me down". The auxiliary is optional because
  # people leave it out ("work gets me down"), and "has been"/"have been" is how the same
  # thing is said when it has gone on a while. A person is not a thing here - "my boss gets me
  # down" names somebody, and `_refused` leaves those to bot/compose/harm.py.
  | \b(?:(?:is|are|was|were|'s|'re)\s+)?(?:(?:has|have|had)\s+been\s+|been\s+)?
    (?:getting|gets|got|wearing|wears|wore)\s+(?:me|us)\s+down\b
""", re.X)

HELPLESS = re.compile(r"""\s*(?:,|\band\b|\bbut\b|\bso\b)\s*
    (?:\w+\s+){0,3}?
    (?:i\s+)?(?:don['\u2019]?t|do\s+not|dont|can['\u2019]?t|cannot|cant)\s+
    (?:really\s+|even\s+|honestly\s+)?
    (?:know\s+what\s+to\s+do|know\s+where\s+to\s+start|cope|keep\s+going|take\s+it\s+any\s+more)
  | \s*(?:,|\band\b|\bbut\b)\s*
    (?:\w+\s+){0,3}?i\s*(?:['\u2019]m|m\b|am)\s*(?:at\s+my\s+wits['\u2019]?\s*end|at\s+the\s+end\s+of\s+my\s+tether)
""", re.X)

BLAME = re.compile(r"""\b(?:i|we)\s+(?:really\s+|totally\s+|completely\s+|properly\s+|just\s+)*
    (?:messed|screwed|balls(?:ed)?|buggered|wrecked)\s+(?:it\s+)?up\b
    |\b(?:i|we)\s+(?:really\s+|totally\s+|completely\s+)?(?:ruined|wrecked)\b""", re.X)

OWNER = re.compile(r"\b(my|our|the|this|that|his|her|their)\s+(?:whole\s+|entire\s+)?"
                   r"([a-z][a-z'-]{1,18})(?:\s+([a-z][a-z'-]{1,18}))?")
MODIFIER = frozenset("""
    first second third last next previous other own new old little big huge favourite favorite
    front back spare cheap expensive birthday christmas driving washing running first
""".split())
YOURS = frozenset(("my", "our"))

NOT_A_THING = frozenset("""
    day week month year weekend morning evening night time life everything anything it all
    whole world lot bit thing way start begin end minute hour afternoon
""".split())

PEOPLE = frozenset("""
    he she him her his hers they them their mum mam mom mummy dad daddy father mother parent
    son daughter child kid kids baby toddler teenager boy girl husband wife partner boyfriend
    girlfriend fiance fiancee nan nana gran granny grandma grandad grandpa grandparents brother
    sister sibling aunt uncle cousin nephew niece friend mate flatmate housemate neighbour
    neighbor colleague boss manager landlord landlady tenant carer nurse vet dog cat puppy
    kitten pet
""".split())

GOES_ON = frozenset(("and", "but", "because", "cos", "cause", "so", "then", "when", "after",
                     "before", "while", "which"))
MORE_THAN = 4

ABOUT_THING = (
    "Oh no \u2014 what happened with {thing}?",
    "Ah, that's a shame. What went wrong with {thing}?",
    "That's rotten \u2014 what happened with {thing}?",
    "Ah no. What went wrong with {thing}?",
    "Oh no. How did {thing} go wrong?",
)
ABOUT_OCCASION = tuple(line for line in ABOUT_THING if "what happened with" in line
                       or "what went wrong with" in line) + \
                 ("Oh no. What went wrong with {thing}?",)
ONGOING = (
    "Ugh \u2014 {thing} sounds relentless. What's the worst bit of it?",
    "That's a lot to be carrying. What's the hardest part of {thing}?",
    "Ah no. What's the worst of {thing} at the moment?",
    "I bet. What is it about {thing} that's wearing you down?",
)
WHOLE = (
    "Sounds like one of those days. What went wrong?",
    "Oh no \u2014 what happened?",
    "Ouch. What went wrong?",
    "Ah, everything at once? What happened?",
)
WHOLE_NOW = (
    "Ugh, that sounds relentless. What's the worst bit of it?",
    "That's a lot at the moment. What's the hardest part?",
    "Ah no. What is it that's wearing you down?",
)
JOINERS = frozenset(("to", "for", "at", "in", "on", "onto", "into", "with", "and", "or", "but",
                     "because", "since", "after", "before", "while", "when", "that", "which",
                     "who", "is", "was", "were", "are", "am", "be", "been", "being", "went",
                     "goes", "going", "gone", "has", "have", "had", "keeps", "kept", "makes",
                     "made", "turned", "turns", "came", "comes", "last", "next", "this", "the",
                     "a", "an", "of", "about", "from", "by", "so", "as", "then", "now", "today",
                     "yesterday", "again", "too", "really", "still", "just", "all", "totally",
                     "completely", "absolutely", "properly"))
NOT_A_DOER = frozenset(("interview", "exam", "test", "party", "meeting", "date", "holiday",
                        "essay", "presentation", "wedding", "birthday", "appointment", "shift",
                        "lesson", "class", "review", "application", "audit", "trial", "day"))


def _flat(text):
    return " ".join(str(text or "").lower().replace("\u2019", "'").split())


def _thing(text):
    for match in reversed(list(OWNER.finditer(text))):
        qualifier, word, after = match.group(1), match.group(2), match.group(3) or ""
        if word in ("whole", "entire") and after:
            word, after = after, ""
        elif word in MODIFIER and after:
            word, after = word + " " + after, ""
        elif after in JOINERS:
            after = ""
        if word in NOT_A_THING:
            return ""
        owner = "your" if qualifier in YOURS else "the"
        return (owner + " " + word + (" " + after if after else "")).strip()
    return ""


def _named_after(text):
    match = re.search(r"\b(?:the|my|our|this|that)\s+(?:whole\s+)?"
                      r"([a-z][a-z'-]{1,18})(?:\s+([a-z][a-z'-]{1,18}))?", text)
    if not match:
        return ""
    word, after = match.group(1), match.group(2) or ""
    if word in MODIFIER and after:
        word, after = word + " " + after, ""
    elif after in JOINERS:
        after = ""
    if word in NOT_A_THING:
        return ""
    return "your " + word + (" " + after if after else "")


def _bare_subject(head):
    words = [word for word in head.split() if word]
    while words and words[-1] in ("is", "are", "was", "were", "been", "has", "have",
                                  "had", "really", "just"):
        words.pop()
    if not words:
        return ""
    word = words[-1]
    if word in NOT_A_THING or word in ("i", "im", "it", "that", "this", "there", "he",
                                      "she", "they", "we", "you"):
        return ""
    return word


def _refused(name):
    return bool(name) and name.split()[-1] in PEOPLE


def reading(text):
    clean = _flat(text)
    if not clean or "?" in clean:
        return None
    for pattern, tense in ((VAGUE, "past"), (NOW, "now"), (BLAME, "past")):
        match = pattern.search(clean)
        if not match:
            continue
        after = clean[match.end():].split()
        rest = HELPLESS.sub("", clean[match.end():]).split() if after else []
        if len(rest) > MORE_THAN or any(word.strip(".,!") in GOES_ON for word in rest):
            return None
        name = _thing(clean[:match.start()])
        if not name and pattern is BLAME:
            name = _named_after(clean[match.end():])
        if not name and pattern is NOW:
            name = _bare_subject(clean[:match.start()])
        if _refused(name):
            return None
        return (name, tense)
    return None


_NOT_A_PLURAL_ENDING = ("ss", "us", "is", "ws")


def _a_plural_thing(name):
    words = str(name or "").split()
    if not words:
        return False
    last = words[-1].lower().strip(".,!?;:")
    if not last.endswith("s"):
        return False
    return not last.endswith(_NOT_A_PLURAL_ENDING)


def _agrees_with_the_thing(line, name):
    if _a_plural_thing(name):
        return line.replace(" sounds ", " sound ").replace(" it sounds ", " they sound ")
    return line


def pool(text):
    said = reading(text)
    if not said:
        return ()
    name, tense = said
    if not name:
        return WHOLE_NOW if tense == "now" else WHOLE
    if tense == "now":
        return tuple(_agrees_with_the_thing(line.format(thing=name), name) for line in ONGOING)
    last = name.split()[-1]
    lines = ABOUT_OCCASION if last in NOT_A_DOER else ABOUT_THING
    return tuple(line.format(thing=name) for line in lines)
