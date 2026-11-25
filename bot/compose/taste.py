import re

from . import fallback

_A_PERSON = re.compile(
    r"\b(?:my|his|her|their|our|your)\s+(?:mum|mom|mam|dad|father|mother|wife|husband|partner|"
    r"boyfriend|girlfriend|son|daughter|kid|kids|child|children|sister|brother|nan|nana|gran|"
    r"granny|grandma|grandad|grandpa|aunt|uncle|cousin|friend|friends|mate|mates|boss|landlord|"
    r"neighbours?|neighbors?|colleague|colleagues|coworker|in-laws?|family|stepson|"
    r"stepdaughter|ex)\b",
    re.I)
_A_SOMEONE = re.compile(r"\b(?:her|him|them|his|hers|theirs)\b", re.I)
_A_PERSON_DESCRIBED = re.compile(
    r"\b(?:a|an|the|this|that|some)\s+(?:girl|boy|man|woman|bloke|guy|lad|lady|fella|"
    r"person|someone|somebody|child)\b",
    re.I)
_ABOUT_WORK = re.compile(r"\bmy\s+(?:job|work|shift|shifts|career|line\s+of\s+work)\b", re.I)
_ABOUT_ME = re.compile(
    r"\b(?:myself|my\s+life|my\s+body|my\s+own\s+body|being\s+me|my\s+(?:arms?|legs?|thighs?|"
    r"tummy|belly|waist|hips?|shape|weight|looks|face|nose|teeth|smile|skin|hair|neck|chin|"
    r"chest|shoulders?|hands?|feet|knees?|reflection)\b)",
    re.I)
_A_SYMPTOM = re.compile(
    r"\b(?:feeling\s+like\s+this|feeling\s+this\s+way|being\s+ill|being\s+sick|"
    r"the\s+way\s+i\s+feel|how\s+i\s+feel)\b",
    re.I)
_A_ASK = re.compile(
    r"\b(?:what|which|how|why|when|where|who|instead|should|could|would|recommend|suggest|"
    r"else|any\s+ideas?)\b",
    re.I)
_A_DEED = re.compile(r"^(?:when|that|it\s+when|the\s+way|how)\b", re.I)
_A_SECOND_CLAUSE = re.compile(
    r"\b(?:because|but|although|though|and\s+i|and\s+then|so\s+i)\b", re.I)

_LEAD_SUBJECT = (r"(?P<subj>i|im|i'm)\s+"
                 r"(?:(?:really|just|absolutely|totally|honestly|actually|properly|still|also|"
                 r"kind\s+of|sort\s+of)\s+)?")
_LEAD = (r"(?:i|im|i'm)\s+"
         r"(?:really\s+|just\s+|absolutely\s+|honestly\s+|actually\s+|totally\s+|seriously\s+|"
         r"properly\s+|kind\s+of\s+|sort\s+of\s+)?")

_A_STANCE = re.compile(
    "^" + _LEAD_SUBJECT +
    r"(?P<verb>hate|hating|love|loving|like|liking|adore|adoring|dislike|prefer|"
    r"can'?t\s+stand|cannot\s+stand|can\s+not\s+stand|couldn'?t\s+stand|"
    r"(?:am\s+)?not\s+a\s+(?:big\s+)?fan\s+of|"
    r"don'?t\s+(?:really\s+)?like|do\s+not\s+(?:really\s+)?like|never\s+liked)\s+"
    r"(?P<thing>.+)$",
    re.I)
_A_STANCE_NO_SUBJECT = re.compile(
    r"^(?P<verb>not\s+(?:2|too|that|very|terribly|overly|really|a\s+bit|a\s+lot|much\s+of\s+a|"
    r"a\s+big)?\s*(?:keen|fussed|bothered)\s+(?:on|about|with)|"
    r"never\s+(?:been\s+)?(?:that|too|very|really|overly)\s+keen\s+(?:on|about|with)|"
    r"not\s+(?:really\s+|usually\s+)?(?:much\s+of\s+)?(?:a\s+)?"
    r"(?:(?:big|huge|massive|great|the\s+biggest)\s+)?fan\s+of|"
    r"never\s+(?:been\s+)?(?:really\s+|actually\s+)?(?:a\s+)?(?:big\s+|huge\s+)?fan\s+of|"
    r"never\s+(?:really\s+|actually\s+)?liked|"
    r"can'?t\s+stand|cannot\s+stand|can\s+not\s+stand|couldn'?t\s+stand|can'?t\s+stick|"
    r"do\s+not\s+(?:really\s+)?like|don'?t\s+(?:really\s+)?like)\s+"
    r"(?P<thing>.+)$",
    re.I)
_A_DREAD = re.compile("^" + _LEAD + r"(?:am\s+)?(?:dreading|dread)\s+(?P<thing>.+)$", re.I)
_A_WAIT = re.compile(
    "^" + _LEAD + r"(?:can'?t\s+wait\s+for|cannot\s+wait\s+for|counting\s+down\s+to)\s+"
    r"(?P<thing>.+)$",
    re.I)

_TWO_STANCES = re.compile(
    r"\b(?:but|and|though|although)\s+(?:i|im|i'm)\s+"
    r"(?:really\s+|just\s+|also\s+)?(?:hate|love|like|prefer|adore|can'?t\s+stand|"
    r"don'?t\s+like|dont\s+like|do\s+not\s+like)\b",
    re.I)
_DISLIKE_VERBS = frozenset((
    "hate", "hating", "dislike", "can't stand", "cant stand", "cannot stand", "can not stand",
    "couldn't stand", "couldnt stand", "not a fan of", "am not a fan of", "not a big fan of",
    "am not a big fan of", "don't like", "dont like", "do not like", "don't really like",
    "dont really like", "do not really like", "never liked",
))
_LIKE_VERBS = frozenset(("love", "loving", "like", "liking", "adore", "adoring", "prefer"))

A_DISLIKE = (
    "{thing} - I'm with you on that. What is the worst bit of it?",
    "{thing} would get to anyone. What is it that gets you about it?",
    "{thing}, yeah. That one gets a lot of people. What is it about it?",
    "You are not on your own there. What is it about {thing} that does your head in?",
    "Fair enough. What is it about {thing}?",
)
A_LIKE = (
    "{thing} - good taste. What is it you like about that?",
    "Ah, {thing}. What got you into that?",
    "{thing}, nice one. What is the draw for you?",
    "Good choice. What is it about {thing} that you love?",
    "{thing} - that is a good thing to like. What do you like most about it?",
)
A_LIKE_OWN = (
    "{thing} - I can see why. What do you like most about it?",
    "{thing}, that is a good thing to have. What is the best of it?",
    "{thing} - fair enough. What is it about it that you like?",
)
A_LIKE_PET = (
    "{thing} - I can see why. What do they get up to?",
    "{thing}, that is a good thing to have. How long have you had them?",
    "{thing} - fair enough. What is it about them that you love?",
    "{thing}, lovely. What is the best thing about them?",
)
A_LIKE_DOING = (
    "{thing} - good one. How often do you get to do it?",
    "{thing}, nice. What got you into it?",
    "{thing} - I can see why. What is the best part?",
)
A_DISLIKE_DOING = (
    "{thing} - I'm with you on that. What is the worst bit?",
    "{thing}, fair enough. What do you do instead?",
    "{thing} - honestly, same. How do you get out of it?",
)
A_DISLIKE_PET = (
    "{thing} - fair enough. What is it about them?",
    "{thing}, yeah. What do they do that gets you?",
)
A_DREAD = (
    "{thing} - I do not blame you. What is the part you are least looking forward to?",
    "Fair enough - nobody looks forward to {thing}. What is the worst of it going to be?",
    "{thing}, yeah. What would make it easier?",
)
A_LIKE_MANNER = (
    "{manner}, then. What is it about {thing} that you like?",
    "{thing}, {manner} - that is the only way. What is the best of it?",
    "Good - {manner} it is. What do you like most about it?",
    "{thing}, {manner} - that is the right answer. What got you that way?",
)
A_DISLIKE_MANNER = (
    "{manner} - no wonder. What is it about {thing} that gets you?",
    "{thing}, {manner} - I am with you. What is the worst bit of it?",
    "Fair enough - nobody wants {thing} {manner}. What do you have instead?",
)
A_THE_BOT_LIKED = (
    "That is kind - thank you. What is it about it you like?",
    "Ha - thanks. What do you like most about it?",
    "Thank you - nice of you to say. What is it that works for you?",
)
A_THE_BOT_DISLIKED = (
    "Fair enough - point taken. What would land better?",
    "Sorry about that. How would you put it instead?",
)
A_WAIT = (
    "{thing} cannot come soon enough. What have you got planned?",
    "Not long now. What are you looking forward to most about {thing}?",
    "{thing} - good. Anything nice lined up?",
)
_BY_KIND = {"dislike": A_DISLIKE, "like": A_LIKE, "like_own": A_LIKE_OWN,
            "like_pet": A_LIKE_PET, "dislike_pet": A_DISLIKE_PET,
            "like_doing": A_LIKE_DOING, "dislike_doing": A_DISLIKE_DOING,
            "like_manner": A_LIKE_MANNER, "dislike_manner": A_DISLIKE_MANNER,
            "the_bot_liked": A_THE_BOT_LIKED, "the_bot_disliked": A_THE_BOT_DISLIKED,
            "dread": A_DREAD, "wait": A_WAIT}

_THE_BOTS = re.compile(r"^(?:your|you|ur|yours|yourself)\b", re.I)

_MANNER_WORDS = frozenset((
    "strong", "weak", "runny", "firm", "hard", "soft", "milky", "creamy", "sweet", "hot",
    "cold", "warm", "tepid", "flat", "fizzy", "sparkling", "thick", "thin", "crispy", "crunchy",
    "smooth", "black", "plain", "spicy", "mild", "salty", "sour", "bitter", "dry", "ripe",
    "rare", "tender", "tough", "loud", "quiet", "bright", "pale", "bold", "baggy", "tight",
    "loose", "short", "long", "heavy", "light", "soggy", "mushy", "lumpy", "gritty", "chewy",
    "rubbery", "juicy", "burnt", "raw", "fluffy", "dense", "chunky", "frothy", "sharp",
    "stodgy", "greasy",
))
_A_MANNER_PHRASE = re.compile(r"\b(?:well done|well-done|medium rare|over easy)\b", re.I)
_A_LINKING_WORD = frozenset(("of", "in", "with", "and", "on", "for", "at", "to", "from",
                             "that", "when", "but", "as", "by", "into", "over", "under"))


def _split_manner(thing):
    words = thing.split()
    if (len(words) == 2 and words[-1].lower() in _MANNER_WORDS
            and words[0].lower() not in ("my", "our", "the", "a", "an", "your", "his", "her",
                                         "their", "it", "that", "this")):
        return words[0], words[-1].lower()
    if len(words) < 3 or words[0].lower() not in ("my", "our"):
        return thing, ""
    said = " ".join(words[1:])
    phrase = _A_MANNER_PHRASE.search(said)
    if phrase:
        head = said[:said.lower().index(phrase.group(0))].strip()
        if head and not any(word.lower() in _A_LINKING_WORD for word in head.split()):
            return words[0] + " " + head, phrase.group(0).lower()
        return thing, ""
    last = words[-1].lower().strip(".,!;:")
    if last not in _MANNER_WORDS:
        return thing, ""
    if any(word.lower().strip(".,!;:") in _A_LINKING_WORD for word in words[1:-1]):
        return thing, ""
    return " ".join(words[:-1]), last


def _a_manner_kind(kind):
    return {"like": "like_manner", "like_own": "like_manner",
            "dislike": "dislike_manner"}.get(kind, kind)

_THEIR_OWN = re.compile(r"^(?:my|our)\b", re.I)

_AN_ANIMAL = frozenset((
    "dog", "cat", "puppy", "kitten", "rabbit", "bunny", "hamster", "gerbil", "guinea", "pig",
    "horse", "pony", "donkey", "bird", "parrot", "budgie", "fish", "tortoise", "turtle",
    "snake", "lizard", "gecko", "chicken", "duck", "goat", "ferret", "rat", "mouse",
    "hedgehog", "chinchilla", "canary", "cockatiel",
))


_AN_INFINITIVE = re.compile(r"^to\s+(?P<verb>[a-z']+)(?:\s+(?P<rest>[a-z' ]+))?$", re.I)
_A_CLAUSE_WORD = frozenset(("i", "im", "i'm", "me", "you", "he", "she", "it", "we", "they",
                            "that", "this", "these", "those", "my", "your", "his", "her",
                            "their", "our", "there", "if", "when", "about", "of"))
_NOT_A_DOING = frozenset(("think", "know", "believe", "remember", "forget", "be", "have",
                          "seem", "suppose", "guess", "imagine", "feel", "want", "need",
                          "say", "tell", "ask", "hear", "see", "understand", "mean", "hope",
                          "wish", "expect", "assume", "pretend", "decide", "hesitate"))
_DOUBLING = frozenset(("swim", "run", "sit", "shop", "stop", "get", "put", "cut", "hit",
                       "dig", "plan", "chat", "jog", "nap", "hop", "win", "drop", "trim",
                       "rub", "knit", "shut", "swing", "begin", "forget", "travel", "snorkel"))
_IRREGULAR_DOING = {"be": "being", "die": "dying", "lie": "lying", "tie": "tying",
                    "see": "seeing", "agree": "agreeing", "ski": "skiing", "free": "freeing"}


def _a_doing(verb):
    verb = verb.lower()
    if verb in _IRREGULAR_DOING:
        return _IRREGULAR_DOING[verb]
    if verb.endswith("ie"):
        return verb[:-2] + "ying"
    if verb.endswith("e") and not verb.endswith(("ee", "ye", "oe")):
        return verb[:-1] + "ing"
    if verb in _DOUBLING:
        return verb + verb[-1] + "ing"
    return verb + "ing"


def _the_doing(thing):
    match = _AN_INFINITIVE.match(thing or "")
    if not match:
        return ""
    verb = match.group("verb").lower()
    rest = (match.group("rest") or "").strip()
    if verb in _NOT_A_DOING or not verb:
        return ""
    if rest and (len(rest.split()) > 2 or any(w in _A_CLAUSE_WORD for w in rest.split())):
        return ""
    doing = _a_doing(verb)
    return (doing + (" " + rest if rest else "")).capitalize()


def _is_an_animal(thing):
    if not _THEIR_OWN.match(thing or ""):
        return False
    words = [w for w in thing.lower().split() if w not in ("my", "our")]
    if not words:
        return False
    last = words[-1]
    if last in _AN_ANIMAL:
        return True
    return last.endswith("s") and last[:-1] in _AN_ANIMAL


def _the_stance(thing, liked):
    doing = _the_doing(thing)
    if doing:
        return ("like_doing" if liked else "dislike_doing"), doing
    if re.match(r"^to\s+[a-z]", thing or "", re.I):
        return None
    if _is_an_animal(thing):
        return ("like_pet" if liked else "dislike_pet"), thing
    if liked and _THEIR_OWN.match(thing):
        return "like_own", thing
    return ("like" if liked else "dislike"), thing


def _clean(text):
    said = " ".join(str(text or "").lower().split())
    said = re.sub(r"^(?:hi|hey|hello|yo|so|well|oh|god|honestly|anyway)[,!\s]+", "", said)
    return said.strip(" .!,")


_A_PRONOUN = frozenset(("it", "that", "this", "them", "these", "those", "things", "everything",
                        "anything", "stuff"))


_NOT_A_THING = re.compile(
    r"^(?:the\s+|this\s+|that\s+|your\s+|my\s+|our\s+|his\s+|her\s+|their\s+)?"
    r"(?:sound|idea|thought|look|smell|taste|prospect|notion|plan|suggestion|thinking|point"
    r"|much|more|lots|plenty)\b",
    re.I)


_TAIL_FILLER = re.compile(
    r"[\s,]*\b(?:btw|tbh|lol|tho|though|anyway|anyways|honestly|i\s+guess|as\s+well|"
    r"so\s+much|very\s+much|a\s+lot|to\s+bits|heaps|loads|right\s+now|at\s+the\s+moment)\b"
    r"[\s.!?]*$",
    re.I)


_DEMONSTRATIVE = frozenset(("this", "that", "these", "those"))


def _a_pointed_at_thing(thing):
    words = (thing or "").lower().split()
    return (len(words) > 1 and words[0] in _DEMONSTRATIVE
            and words[1] not in ("one", "ones", "sort", "kind", "type"))


def _the_thing(raw):
    thing = " ".join(str(raw or "").split()).strip(" .!,;:")
    thing = _TAIL_FILLER.sub("", thing).strip(" .!,;:")
    if not thing or len(thing.split()) > 5:
        return ""
    if thing.lower().split()[0] in _A_PRONOUN and not _a_pointed_at_thing(thing):
        return ""
    if _A_DEED.match(thing) or _A_SECOND_CLAUSE.search(thing):
        return ""
    if _NOT_A_THING.match(thing):
        return ""
    return _split_manner(thing)[0]


def _the_manner(raw):
    thing = " ".join(str(raw or "").split()).strip(" .!,;:")
    thing = _TAIL_FILLER.sub("", thing).strip(" .!,;:")
    if not thing or len(thing.split()) > 5:
        return ""
    return _split_manner(thing)[1]


def reads_as_a_taste(text):
    read = _read(text)
    return (read[0], read[1]) if read else None


def _read(text):
    said = _clean(text)
    if not said or "?" in said:
        return None
    if fallback._loves_someone(said):
        return None
    if (_A_PERSON.search(said) or _A_SOMEONE.search(said) or _ABOUT_ME.search(said)
            or _A_PERSON_DESCRIBED.search(said) or _A_SYMPTOM.search(said)
            or _ABOUT_WORK.search(said) or _TWO_STANCES.search(said)):
        return None
    for pattern, kind in ((_A_STANCE, None), (_A_STANCE_NO_SUBJECT, None),
                          (_A_DREAD, "dread"), (_A_WAIT, "wait")):
        match = pattern.match(said)
        if not match:
            continue
        if not _the_thing(match.group("thing")):
            return None
        if _A_ASK.search(match.group("thing")):
            return None
        raw = " ".join(match.group("thing").split()).strip(" .!,;:")
        if _THE_BOTS.match(raw):
            if kind:
                return ("the_bot_liked" if kind == "wait" else "the_bot_disliked"), "", ""
            verb = " ".join(match.group("verb").lower().split())
            return (("the_bot_liked" if verb in _LIKE_VERBS else "the_bot_disliked"), "", "")
        manner = _the_manner(raw)
        if kind:
            return kind, _the_thing(raw), ""
        if pattern is _A_STANCE_NO_SUBJECT:
            read = _the_stance(_the_thing(raw), False)
            if not read:
                return None
            return (_a_manner_kind(read[0]) if manner else read[0]), read[1], manner
        verb = " ".join(match.group("verb").lower().split())
        subject = " ".join(match.group("subj").lower().split())
        if subject in ("im", "i'm") and verb in ("like", "liking"):
            return None
        thing = _the_thing(raw)
        if verb in _DISLIKE_VERBS:
            read = _the_stance(thing, False)
        elif verb in _LIKE_VERBS:
            if verb == "prefer" and re.search(r"\bto\b", thing):
                return None
            read = _the_stance(thing, True)
        else:
            return None
        if not read:
            return None
        return (_a_manner_kind(read[0]) if manner else read[0]), read[1], manner
    return None


_PROPER = frozenset((
    "monday", "mondays", "tuesday", "tuesdays", "wednesday", "wednesdays", "thursday",
    "thursdays", "friday", "fridays", "saturday", "saturdays", "sunday", "sundays",
    "january", "february", "march", "april", "may", "june", "july", "august", "september",
    "october", "november", "december", "christmas", "xmas", "easter", "halloween", "new year",
    "new years", "valentines", "valentine's", "boxing day",
))


def _as_a_name(thing):
    words = thing.split(" ", 1)
    head = words[0].lower().strip(",.")
    if head not in _PROPER:
        return thing
    return words[0][0].upper() + words[0][1:] + ((" " + words[1]) if len(words) > 1 else "")


def _in_a_sentence(thing):
    if not thing or _as_a_name(thing) == thing and thing.split(" ")[0].lower().strip(",.") in _PROPER:
        return thing
    return thing[0].lower() + thing[1:]


def _as_yours(thing):
    return re.sub(r"^(my|our)\b", "your", thing, flags=re.I)


def _at_the_front(thing):
    return thing[0].upper() + thing[1:] if thing else ""


def reply_for(text, memory=None):
    read = _read(text)
    if not read:
        return None
    kind, thing, manner = read
    thing = _as_a_name(_as_yours(thing))
    options = [
        line.format(thing=_at_the_front(thing) if line.startswith("{thing}")
                    else _in_a_sentence(thing),
                    manner=_at_the_front(manner) if line.startswith("{manner}")
                    else manner)
        for line in _BY_KIND[kind]
    ]
    return fallback._choose(options, memory or {}, _clean(text), seed_text=_clean(text))
