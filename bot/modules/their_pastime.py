import re

from ..compose import fallback
from ..compose import pick
from ..compose.remark import THEIR_PERSON, _the_job_in, fill_person, person_pronouns

PRIORITY = 300

THEIR_ANY = (r"(?:" + THEIR_PERSON + r"|father in law|mother in law|son in law|"
             r"daughter in law|sister in law|brother in law|friend|best friend|neighbour|"
             r"neighbor|mate|boss|aunty|auntie|boyfriend|girlfriend|other half|flatmate|"
             r"housemate|fella|missus|stepmum|stepdad|grandson|granddaughter)")
WHAT_THEY_ARE_INTO = (r"(?:loves|adores|likes|is obsessed with|is mad about|is nuts about)")
WHAT_THEY_DO = (r"(?:plays|does|collects|makes|teaches|runs|swims|sings|paints|draws|"
                r"bakes|cooks|gardens|reads|writes|dances)")
NOT_TAKEN_UP = frozenset((
    "smoking", "drinking", "gambling", "drugs", "cocaine", "heroin", "betting", "vaping",
    "the bottle", "fighting", "biting", "wetting", "stealing", "drink", "alcohol", "weed",
    "pills", "porn", "scratchcards", "debt", "self-harm", "harm", "cutting", "shouting",
    "bottle", "cans", "booze",
))
NOT_TAKEN_UP_PHRASES = (
    "another woman", "another man", "another bloke", "another person", "another fella",
    "another lad", "another girl", "someone else", "somebody else", "an affair", "an ex",
    "his ex", "her ex", "the ex", "a row", "rows", "arguing", "arguments", "a fight",
    "trouble", "the police", "a gang", "crime", "money he hasnt got", "the horses",
)
THEIR_INTO = re.compile(
    r"^my (?P<person>" + THEIR_ANY + r")(?:'?s)? (?:is|are) "
    r"(?:really |well |properly |totally |so )?into (?P<thing>[a-z][a-z' \-]{1,22})$")
THEIR_LOVES = re.compile(
    r"^my (?P<person>" + THEIR_ANY + r")(?:'?s)? " + WHAT_THEY_ARE_INTO +
    r" (?P<thing>[a-z][a-z' \-]{1,22})$")
THEIR_DOES = re.compile(
    r"^my (?P<person>" + THEIR_ANY + r")(?:'?s)? " + WHAT_THEY_DO +
    r" (?:in |with |for |at )?(?P<thing>[a-z][a-z' \-]{1,22})$")
THEIR_TOOK_UP = re.compile(
    r"^my (?P<person>" + THEIR_ANY + r")(?:'?s)? (?:has|have) (?:just |recently )?"
    r"(?:taken up|got into|started) (?P<thing>[a-z][a-z' \-]{1,22})$")
THEIR_KEEPS = re.compile(
    r"^my (?P<person>" + THEIR_ANY + r")(?:'?s)? keeps (?:some |a few |two |three )?"
    r"(?P<thing>[a-z]{2,12}s)$")
THEIR_GOOD_AT = re.compile(
    r"^my (?P<person>" + THEIR_ANY + r")(?:'?s)? (?:is|are) "
    r"(?:really |very |so |quite )?good at (?P<thing>[a-z][a-z' \-]{1,22})$")
THEIR_VISIT = re.compile(
    r"^my (?P<person>" + THEIR_ANY + r")(?:'?s)? (?:is|are) "
    r"(?:coming|visiting|staying) (?P<when>(?:on |at |this |next |for |in |over )"
    r"[a-z0-9' \-]{1,24})$")
THEIR_IS_A_ROLE = re.compile(
    r"^my (?P<person>" + THEIR_ANY + r")(?:'?s)? (?:is|works as) (?:a|an) "
    r"(?P<role>[a-z][a-z'\-]{2,20})$")

THEIRS_ROLE_LINES = (
    "{Job}. What does a normal day look like for {them}?",
    "{Job}. Is that what {they} always wanted to do?",
    "{Job} — how long {has} {they} been at it?",
)

THEIRS_INTO_LINES = (
    "How did {they} get into that?",
    "Is that a new thing, or {has} {they} always been into {it}?",
    "Are you into {it} too, or is that {their} thing?",
    "What got {them} started on {it}?",
)
THEIRS_LOVES_LINES = (
    "What {do} {they} like most about {it}?",
    "How did that start?",
    "Do you get roped in too?",
    "Did {they} get you into {it} as well?",
)
THEIRS_DOES_LINES = (
    "How long {has} {they} been doing that?",
    "How often {do} {they} do it?",
    "Do you ever go and watch?",
    "What is {their} favourite bit of it?",
)
THEIRS_GOOD_AT_LINES = (
    "How long {has} {they} been at that?",
    "Is it a class, or something {they} {do} at home?",
    "Where did {they} learn that?",
    "Do they get much chance to show it off?",
)
THEIRS_VISIT_LINES = (
    "{is} {they} staying with you, or nearby?",
    "Is it a flying visit, or a long one?",
    "Are you looking forward to it?",
    "How much of the week is that taking up?",
)

def _starts_a_sentence(line):
    said = str(line or "")
    return said[:1].upper() + said[1:] if said else said


def _the_turn_before_was_a_feeling(clean, memory):
    from ..memory import ack
    read = getattr(ack, "_after_a_feeling", None)
    return bool(read and read(clean, memory))


def _a_thing_nobody_is_into(thing):
    said = " ".join(str(thing or "").lower().split())
    if any(phrase in said for phrase in NOT_TAKEN_UP_PHRASES):
        return True
    parts = [word for word in re.split(r"[^a-z\-]+", said) if word]
    return any(word in NOT_TAKEN_UP for word in parts)


NOT_PLURAL = frozenset((
    "chess", "darts", "news", "gymnastics", "athletics", "bowls", "skittles", "billiards",
    "physics", "maths", "mathematics", "business", "class", "glass", "bass", "gas", "bus",
    "christmas", "tennis", "series", "species", "means", "this", "his", "hers", "its",
))


def _a_plural_thing(thing):
    words = [word for word in re.split(r"[^a-z\-]+", str(thing or "").lower()) if word]
    if not words:
        return False
    last = words[-1]
    if last in NOT_PLURAL or len(last) < 4:
        return False
    return last.endswith("s") and not last.endswith(("ss", "us", "is", "ous"))


def _it_word(thing):
    return "them" if _a_plural_thing(thing) else "it"





BEFORE_AN_AUDIENCE = frozenset((
    "football", "rugby", "cricket", "tennis", "netball", "hockey", "athletics", "racing",
    "races", "matches", "dancing", "ballet", "singing", "choir", "gigs", "bands", "drama",
    "theatre", "plays", "stand up", "swimming", "speedway", "boxing", "darts", "golf",
))


def _watched(thing):
    words = [word for word in re.split(r"[^a-z]+", str(thing or "").lower()) if word]
    if any(word in BEFORE_AN_AUDIENCE for word in words):
        return True
    return " ".join(words) in BEFORE_AN_AUDIENCE


def _does_pool(thing):
    if _watched(thing):
        return THEIRS_DOES_LINES
    return tuple(line for line in THEIRS_DOES_LINES if "watch" not in line)


def _fill_it(line, person_word, it_word="it"):
    they, them, their, do, are = person_pronouns(person_word)
    said = fill_person(line, person_word)
    said = (said.replace("{has}", "have" if do == "do" else "has")
                .replace("{is}", "are" if are == "are" else "is")
                .replace("{it}", it_word))
    said = (said.replace("has they", "have they").replace("Has they", "Have they")
                .replace("is they", "are they").replace("Is they", "Are they")
                .replace("does they", "do they").replace("Does they", "Do they"))
    return said[:1].upper() + said[1:] if said else said


def reading(clean, words, memory):
    if _the_turn_before_was_a_feeling(clean, memory):
        return None
    match = THEIR_IS_A_ROLE.match(clean)
    if match:
        job = _the_job_in(match.group("role"))
        if job:
            return _fill_it(pick(THEIRS_ROLE_LINES, memory, clean).replace("{Job}", job),
                            match.group("person"))
    match = THEIR_INTO.match(clean)
    if match and not _a_thing_nobody_is_into(match.group("thing")):
        return _fill_it(pick(THEIRS_INTO_LINES, memory, clean), match.group("person"),
                        _it_word(match.group("thing")))
    match = THEIR_LOVES.match(clean)
    if match and not _a_thing_nobody_is_into(match.group("thing")):
        return _fill_it(pick(THEIRS_LOVES_LINES, memory, clean), match.group("person"),
                        _it_word(match.group("thing")))
    match = THEIR_DOES.match(clean)
    if match and not _a_thing_nobody_is_into(match.group("thing")):
        return _fill_it(pick(_does_pool(match.group("thing")), memory, clean),
                        match.group("person"))
    match = THEIR_GOOD_AT.match(clean)
    if match and not _a_thing_nobody_is_into(match.group("thing")):
        return _fill_it(pick(THEIRS_GOOD_AT_LINES, memory, clean), match.group("person"))
    match = THEIR_KEEPS.match(clean)
    if match:
        return _fill_it(pick(THEIRS_DOES_LINES, memory, clean), match.group("person"))
    match = THEIR_TOOK_UP.match(clean)
    if match and not _a_thing_nobody_is_into(match.group("thing")):
        return _fill_it(pick(_does_pool(match.group("thing")), memory, clean),
                        match.group("person"))
    match = THEIR_VISIT.match(clean)
    if match:
        return _fill_it(pick(THEIRS_VISIT_LINES, memory, clean), match.group("person"))
    return None


PLACEHOLDER_OPENINGS = (
    "noted", "i'm listening", "i am listening", "got it", "ok.", "that's noted",
    "thanks for telling me", "i don't know enough", "i dont know enough",
    "that's beyond what i know", "thats beyond what i know", "i'm not sure about that one",
    "im not sure about that one",
)


def _is_a_placeholder(said):
    text = str(said or "").strip().lower()
    return any(text.startswith(opening) for opening in PLACEHOLDER_OPENINGS)


HEAVY_IN_THE_THREAD = re.compile(
    r"\b(?:bull(?:y|ied|ying)|bullies|ill|unwell|poorly|poorlier|sick|sicker|sickness|diagnos\w*|"
    r"cancer|tumou?r|chemo\w*|radiotherap\w*|dementia|alzheim\w*|parkinson\w*|stroke|sepsis|"
    r"pneumonia|surgery|operation|transplant|dialysis|hospice|palliative|terminal|sectioned|"
    r"sectioning|depress\w*|anxiety|anorexi\w*|bulimi\w*|addict\w*|relapse\w*|overdose\w*|"
    r"self[- ]harm|suicidal|miscarr\w*|stillborn|funeral|burial|cremat\w*|griev\w*|bereave\w*|"
    r"died|dying|death|passed away|lost (?:him|her|them|my)|hospital|icu|a&e|ambulance|"
    r"in pain|suffering|struggling|carer|carers|dementia)\b")


def _the_thread_is_heavy(memory):
    before = fallback._the_line_before(memory) if hasattr(fallback, "_the_line_before") else ""
    if not before:
        turns = [turn for turn in ((memory or {}).get("turns") or []) if isinstance(turn, dict)]
        before = str(turns[-1].get("user") or "") if turns else ""
    said = str(before or "").lower()
    if not said:
        return False
    if fallback._reads_as_heavy_news(said):
        return True
    return bool(HEAVY_IN_THE_THREAD.search(said))


def respond(text, memory):
    if not text or "?" in text:
        return None
    clean = re.sub(r"[^a-z0-9' ]+", " ", str(text).lower())
    clean = re.sub(r"\s+", " ", clean).strip()
    if not clean.startswith("my "):
        return None
    if _the_thread_is_heavy(memory):
        return None
    mine = reading(clean, clean.split(), memory)
    if not mine:
        return None
    theirs = None
    try:
        theirs = fallback.reply_for(text, memory)
    except Exception:
        theirs = None
    if theirs and not _is_a_placeholder(theirs):
        return None
    return mine
