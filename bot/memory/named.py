import re

from . import holds as earlier
from .topics import carried_topic as the_carried_topic, is_ack, subject as the_subject
from ..compose import trouble
from ..compose.badnews import reads_as_bad_news
from ..understanding import kinds

CONTINUES = re.compile(r"^\s*(?:and|or|plus|also|but|then)\b", re.I)


def _answers_the_bot(text):
    return bool(is_ack(text)) and not CONTINUES.match(str(text or ""))


LEAD = re.compile(r"^\s*(?:(?:and|or|also|plus|ok|okay|then|so)\b[\s,]*)*"
                  r"(?:(?:what|how)\s+about\s+|and\s+what\s+about\s+|what\s+of\s+)?", re.I)
QUANT = re.compile(r"^\s*(?:a|an|the|some|any|another|one|two|three|more|other)\s+", re.I)
ASKING = re.compile(r"^\s*(?:(?:what|how|where|when|which|who|why)(?:'s|s)?\b|"
                    r"(?:can|could|should|do|does|did|is|are|was|were|have|has|will|would|"
                    r"shall|may|might)\b)", re.I)
POINTS_BACK = frozenset("""it its it's them they that this these those there one ones
him her his hers their theirs he she""".split())
ASKS_FOR_AN_ANSWER = frozenset("""tip tips advice suggestion suggestions pointer pointers
recommendation recommendations trick tricks guidance idea ideas hint hints""".split())
VERBS = frozenset("""is are was were am be been being have has had do does did done
will would shall should can could may might must
go going goes went come coming comes came get getting got make making made
take taking took need needs needed want wants wanted like likes liked
know knows knew think thinks thought feel feels felt hurt hurts hurting
eat eats eating ate drink drinks drinking work works working play plays playing
happen happens happened start starts started stop stops stopped try tries tried
give gives gave put puts keep keeps kept buy buys bought sell sells sold
live lives lived move moves moved stay stays stayed visit visits visited
rain rains raining snow snows snowing""".split())
TAKES_BACK = frozenset("""forget forgets forgot forgetting drop drops dropped dropping
scratch scratches scratched strike strikes struck remove removes removed delete deletes deleted
cancel cancels cancelled canceling bin bins binned ignore ignores ignored discard discards
discarded""".split())
ASKED_FOR_IDEAS = re.compile(
    r"\b(?:what|which)\s+(?:should|could|can|shall|would)\s+(?:i|we)\s+"
    r"(?:cook|make|do|have|eat|get|buy|watch|read|wear|give|bring|take|serve|bake|plan)\b|"
    r"\b(?:what|which)\s+(?:do|did)\s+(?:i|we)\s+(?:cook|make|have|eat)\b|"
    r"\bwhat\s+(?:can|could)\s+(?:i|we)\s+(?:cook|make|have|eat|do|get)\b|"
    r"\bany\s+(?:ideas?|suggestions?)\b|\bideas?\s+for\b|"
    r"\bwhat\s+would\s+you\s+(?:suggest|recommend|cook|make|do)\b|"
    r"\bsuggest(?:ions?)?\s+(?:for|something)\b", re.I)
MOST_WORDS = 4
SAID_NOT_A_FOOD = frozenset("""i me we us you he she they it its said says say saying meant
means mean asking asked told tell telling sorry actually really""".split())
A_THANK_YOU = frozenset("""thanks thank thankyou thank-you thx ta cheers mate love hun""".split())
PREP = frozenset(("of", "in", "on", "at", "for", "from", "with", "about", "to", "by"))


def _previous_ask(memory):
    turns = [t for t in (memory or {}).get("turns") or [] if isinstance(t, dict)]
    if not turns:
        return ""
    said = str(turns[-1].get("user") or "")
    return said if ASKED_FOR_IDEAS.search(said) else ""


TAKE_BACK_LEAD = re.compile(r"^\s*(?:(?:and|or|so|ok|okay|now|then)\b[\s,]*)*"
                            r"(?:(?:please|just|actually)\s+)*", re.I)
TAKE_BACK_WHOLE = ("take that back", "takes that back", "never mind", "scratch that", "forget it",
            "forget that", "forget about it", "drop it", "drop that")


def takes_back(text):
    said = " ".join(str(text or "").strip().lower().split())
    if not said:
        return False
    rest = TAKE_BACK_LEAD.sub("", said).strip(" .,;:!?")
    if not rest:
        return False
    if rest.startswith(TAKE_BACK_WHOLE):
        return True
    if len(rest.split()) > 6:
        return False
    first = re.split(r"[\s,]+", rest, 1)[0].strip(".,;:!?")
    return first in TAKES_BACK


THE_ASKING = (
    re.compile(r"^\s*(?:and|also|so|ok|okay|but|then|well|oh)\b[\s,]*", re.I),
    re.compile(r"^\s*(?:can|could|would)\s+you\s+(?:please\s+)?", re.I),
    re.compile(r"^\s*(?:please\s+)?(?:tell|remind|show)\s+me\s+(?:again\s+)?"
               r"(?:about|of|who|what)\s+", re.I),
    re.compile(r"^\s*(?:tell|remind)\s+me\s+", re.I),
    re.compile(r"^\s*(?:anything|something|more|a\s+bit)\s+about\s+", re.I),
    re.compile(r"^\s*(?:what|how)\s+about\s+", re.I),
    re.compile(r"^\s*same\s+(?:for|as)\s+", re.I),
    re.compile(r"^\s*what\s+of\s+", re.I),
    re.compile(r"^\s*(?:do|did)\s+you\s+(?:remember|know|recall)\s+(?:about\s+|the\s+)?", re.I),
    re.compile(r"^\s*(?:what\s+is|what's|whats|what)\s+", re.I),
    re.compile(r"^\s*who(?:'s|s| is| was)\s+", re.I),
)
THE_ASKING_TAIL = re.compile(
    r"\s+(?:again|then|though|please|now|too|already|anyway|honestly|is|was|are|were)\s*$", re.I)
WHO_X_IS = re.compile(r"^(?:(?:and|also|so|ok|okay|then)\s+)?who\s+(?P<thing>.+?)\s+(?:is|was)\s*$",
                      re.I)
MOST_WORDS_ASKED_ABOUT = 3
POINTED_AT = frozenset(("him", "her", "them", "they", "that one", "this one", "those two",
                        "the two of them", "both of them", "the pair of them"))


THE_ASKING_VERB = re.compile(
    r"^\s*(?:is|are|was|were|am|be|been|being|do|does|did|should|could|would|will|shall|can|may|"
    r"might|must|have|has|had)\b", re.I)


def the_one_asked_about(text):
    said = " ".join(str(text or "").replace("\u2019", "'").split()).strip(" ?!.,;:")
    if not said:
        return ""
    last_verb = WHO_X_IS.match(said)
    if last_verb:
        said = last_verb.group("thing").strip(" ?!.,;:")
    changed = True
    while changed:
        changed = False
        for frame in THE_ASKING:
            new = frame.sub("", said, count=1).strip(" ?!.,;:")
            if new and new != said:
                said = new
                changed = True
        trimmed = THE_ASKING_TAIL.sub("", said).strip(" ?!.,;:")
        if trimmed and trimmed != said:
            said = trimmed
            changed = True
    if said.lower() in POINTED_AT:
        return said
    if len(said.split()) > MOST_WORDS_ASKED_ABOUT:
        return ""
    if THE_ASKING_VERB.match(said):
        return ""
    if any(word.lower() in VERBS for word in said.split()):
        return ""
    if not _looks_like_a_thing(said):
        return ""
    return said


def thing(text):
    said = " ".join(str(text or "").strip().split())
    if not said or len(said.split()) > MOST_WORDS + 4:
        return ""
    if ASKING.match(said):
        if not re.match(r"^\s*(?:what|how)\s+about\b", said, re.I):
            return ""
    rest = LEAD.sub("", said)
    rest = QUANT.sub("", rest.strip(" .,;:!?"))
    rest = rest.strip(" .,;:!?")
    if not rest:
        return ""
    words = [w for w in re.split(r"[\s,]+", rest) if w]
    if len(words) > MOST_WORDS:
        return ""
    for word in words:
        bare = word.lower().strip(".,;:!?")
        if (bare in POINTS_BACK or bare in VERBS or bare in TAKES_BACK
                or bare in ASKS_FOR_AN_ANSWER
                or bare in ("what", "how", "why", "when")):
            return ""
        if not re.search(r"[a-z]", bare):
            return ""
    if not _looks_like_a_thing(" ".join(words)):
        return ""
    return " ".join(words)


def _looks_like_a_thing(phrase):
    words = phrase.split()
    if not words:
        return False
    if any(re.search(r"\d", word) for word in words):
        return False
    return any(len(re.sub(r"[^a-z]", "", word.lower())) >= 3 for word in words)


NAME_WORD = re.compile(r"\b(?:called|named|names?)\b|name'?s", re.I)
IN_FRONT_OF_THE_NAME = frozenset("is not was isnt aint it its really actually".split())
AFTER_THE_NAME = frozenset("instead now then actually please ok okay".split())


def carries_a_name(text):
    return bool(NAME_WORD.search(str(text or "")))


def the_name_in(value):
    text = " ".join(str(value or "").replace("\u2019", "'").split())
    if not carries_a_name(text):
        return ""
    words = text.split()
    for index, word in enumerate(words):
        bare = word.strip(".,!?;:").lower()
        if bare not in ("called", "named", "name", "names", "name's"):
            continue
        rest = [one for one in words[index + 1:]
                if one.strip(".,!?;:").lower() not in IN_FRONT_OF_THE_NAME]
        while rest and rest[-1].strip(".,!?;:").lower() in AFTER_THE_NAME:
            rest.pop()
        if rest:
            return " ".join(rest).strip(" .,!?;:")
        return ""
    return ""


A_NAME_ASK = re.compile(
    r"\bwhat(?:'s|s| is| are| was)?\s*(?:it|its|he|she|they|them|the|your|his|her|their)?\s*"
    r"(?:called|named)\b"
    r"|\bwhat(?:'s|s| is)?\s+(?:its|his|her|their|your)\s+names?\b"
    r"|\bwhat\s+do\s+(?:you|they)\s+call\b", re.I)
JUST_A_NAME = re.compile(
    r"^\W*(?:(?:its|it's|hes|he's|shes|she's|theyre|they're|just|actually|his|her)\s+)*"
    r"(?P<name>[A-Za-z][A-Za-z'-]{1,20})"
    r"(?:\s+(?:i think|we think|for now|so far|anyway|probably))*\W*$")
NOT_A_NAME = frozenset("""
no yes yeah nah not none nothing unknown undecided idea clue sure maybe dont dontnot doesnt
still deciding thinking undecided wait later him her them they it he she that this one
puppy dog cat kitten rabbit hamster boy girl friend mate son daughter baby kid
""".split())


def asked_for_a_name(memory):
    turns = memory.get("turns") if isinstance(memory, dict) else None
    for turn in reversed(turns or []):
        if isinstance(turn, dict) and str(turn.get("bot") or "").strip():
            return bool(A_NAME_ASK.search(" ".join(str(turn["bot"]).split())))
    return False


def the_name_given(text, memory=None):
    said = " ".join(str(text or "").replace("\u2019", "'").split())
    if not said or not asked_for_a_name(memory):
        return ""
    framed = the_name_in(said)
    if framed:
        return framed
    found = JUST_A_NAME.match(said)
    if not found:
        return ""
    name = found.group("name")
    if name.lower() in NOT_A_NAME:
        return ""
    return name


SPAN_WORDS = frozenset(("in", "for", "since", "over", "all"))
NOT_GOT = re.compile(
    r"^\s*(?:(?:and|but|also|plus|oh|sorry|actually)\b[\s,]*)?"
    r"(?:"
    r"(?:(?:i|we)\s+)?(?:dont|don't|do not|didnt|didn't|did not|havent|haven't|have not|"
    r"hasnt|hasn't|has not)\s+(?:(?P<holding>got|get|have|had|buy|bought)\s+)?"
    r"|(?:there\s+is\s+|theres\s+|there's\s+|i\s+have\s+|we\s+have\s+)?no\s+"
    r")"
    r"(?:any\s+|a\s+|the\s+|some\s+)?(?P<food>[a-z][a-z '-]{1,24}?)\s*(?:left|in|at all)?\s*$",
    re.I)


NOT_A_SHELF = frozenset("""
eat eats eating ate eaten like likes liked liking love loves loved fancy fancies enjoy enjoys
enjoyed want wants wanted need needs needed use uses used drink drinks drinking stomach stomachs
touch touches much many""".split())


def _not_got(text, memory=None):
    match = NOT_GOT.match(" ".join(str(text or "").split()))
    if not match:
        return ""
    food = match.group("food").strip()
    if carries_a_name(food):
        return ""
    if not _looks_like_a_thing(food):
        return ""
    from ..understanding.normalize import IRREGULAR_PARTICIPLES

    words = food.lower().split()
    if any(word in NOT_A_SHELF for word in words):
        return ""
    after = words[1] if len(words) > 1 else ""
    if (not (match.groupdict().get("holding") or "").strip()
            and words[0] in IRREGULAR_PARTICIPLES and (not after or after in SPAN_WORDS)):
        return ""
    if any(word in POINTS_BACK for word in words) or ASKING.match(food):
        return ""
    if any(word in SAID_NOT_A_FOOD for word in food.lower().split()):
        return ""
    if any(word in A_THANK_YOU for word in food.lower().split()):
        return ""
    if len(food.split()) > MOST_WORDS:
        return ""
    return food


def _said_the_food(memory, food):
    said = _last_reply(memory).lower()
    return bool(said) and bool(re.search(r"\b" + re.escape(food.lower()) + r"", said))


def _last_reply(memory):
    return earlier.last_reply(memory)
PART_WORDS = 4
PART_LEAD = re.compile(r"^\s*(?:the|its|it's|their|his|her|a|an|any|more|some|this|that|these|"
                       r"those)\b", re.I)


def the_thing_named(memory):
    return _the_thing_they_named(memory)


def about_the_thing(text, memory, owner=""):
    said = " ".join(str(text or "").strip().split()).strip(" .!?")
    if not said or len(said.split()) > PART_WORDS + 5:
        return ""
    if ASKING.match(said) and not re.match(r"^\s*(?:what|how)\s+about\b", said, re.I):
        return ""
    if follow_up(text, memory):
        return ""
    rest = LEAD.sub("", said).strip(" .,;:!?")
    if not PART_LEAD.match(rest):
        return ""
    rest = QUANT.sub("", rest).strip(" .,;:!?")
    words = [word.strip(".,;:!?") for word in re.split(r"[\s,]+", rest) if word.strip(".,;:!?")]
    if not words or len(words) > PART_WORDS:
        return ""
    part = []
    for word in words:
        bare = word.lower()
        if bare in POINTS_BACK:
            continue
        if bare in VERBS or bare in ("what", "how", "why", "when", "where", "which", "who"):
            return ""
        if not part and (bare in PREP or bare in ("another", "more", "other")):
            return ""
        part.append(word)
    if not part or not _looks_like_a_thing(" ".join(part)):
        return ""
    if set(part[0].lower().split()) & {"what", "how"}:
        return ""
    thing_said = str(owner or "").strip() or the_subject(memory)
    if not thing_said:
        return ""
    said_words = {word.lower() for word in " ".join(part).split()}
    if said_words & {word.lower().strip(".,;:!?") for word in thing_said.split()}:
        return ""
    return " ".join(part) + " of " + thing_said


A_MEASURE_AGAIN = re.compile(r"^\s*(?:and|or|also|plus|what\s+about|how\s+about)\b[\s,]*", re.I)
A_FITTING = re.compile(r"\b(?:fit|fits|fitting|fitted|swap|swaps|swapping|installs?|installed|"
                       r"installation|replac(?:e|es|ed|ing)|replacement)\b", re.I)
WANTS_A_NEW_ONE = re.compile(
    r"\b(?:a|an|the)\s+new\s+(?:one|boiler|machine|shower|radiator|oven|fridge|dishwasher|"
    r"washer|dryer|cooker|hob|combi|heating|system)\b|\bnew\s+one\b|\breplac\w+\b|"
    r"\b(?:fit|fits|fitting|fitted|swap|swaps|swapping|install|installs|installed)\b", re.I)
ASKED_THE_MEASURE = re.compile(r"\bhow\s+long\b", re.I)
_THE_LIFE = re.compile(r"\b(?:last|lasts|lasting|lasted|years?|old|lifespan|life\s*span|"
                       r"expectancy|cost|costs|price|much)\b", re.I)
NAMED_A_THING = re.compile(
    r"\b(?:my|our|the|his|her|this)\s+((?:[a-z][a-z-]*\s+){0,2}[a-z][a-z-]*)\s+"
    r"(?:is|was|are|were|keeps|kept|has|had|stopped|broke|breaks|failed|went|wont|won't|isnt|"
    r"doesnt|doesn't|needs|makes|sounds|smells)\b", re.I)
NOT_THE_THING_ITSELF = frozenset("""
broken broke dead leaking leak faulty failed failing cracked blocked jammed stuck gone kaput
dodgy unreliable stopped working old new bad worse better fine ok okay good rubbish
""".split())


def _the_thing_they_named(memory):
    turns = [row for row in (memory or {}).get("turns") or [] if isinstance(row, dict)]
    for turn in turns[-3:][::-1]:
        said = " ".join(str(turn.get("user") or "").lower().split())
        for match in NAMED_A_THING.finditer(said):
            words = [word for word in match.group(1).split()
                     if word not in NOT_THE_THING_ITSELF and len(word) > 2]
            if words:
                return " ".join(words[-2:])
    return ""


def a_measure_asked_again(text, memory):
    said = " ".join(str(text or "").strip().split()).strip(" .!?")
    if not said or len(said.split()) > 12:
        return ""
    if A_MEASURE_AGAIN.match(said) and len(said.split()) > 8:
        return ""
    if _THE_LIFE.search(said):
        return ""
    if not WANTS_A_NEW_ONE.search(said):
        return ""
    adds_on = bool(A_MEASURE_AGAIN.match(said))
    if adds_on and not (A_FITTING.search(said) or ASKED_THE_MEASURE.search(said)):
        return ""
    if not adds_on and not ASKED_THE_MEASURE.search(said):
        return ""
    turns = [row for row in (memory or {}).get("turns") or [] if isinstance(row, dict)]
    if not turns:
        return ""
    if adds_on:
        before = " ".join(str(turns[-1].get("user") or "").lower().split())
        if not ASKED_THE_MEASURE.search(before):
            return ""
    thing = _the_thing_they_named(memory)
    if not thing:
        return ""
    return "how long does it take to fit a new " + thing


A_GOAL = re.compile(
    r"^\s*(?:(?:so|ok|okay|and|also|well|right|yeah|hi|hello)[, ]+)*"
    r"(?:i'?m|im|i am|we'?re|we are|i'?ve been|ive been|i have been)\s+"
    r"(?P<how>trying|aiming|hoping|learning)\s+"
    r"(?P<what>(?:to\s+|for\s+)?[a-z0-9][a-z0-9 '\-]{2,60}?)\s*[.!]*$", re.I)

GOAL_VERB = {"trying": "", "aiming": "", "hoping": "", "learning": "learn to "}

OUTCOME_ASK = re.compile(
    r"\bhow\s+long\s+(?:until|till|before)\s+(?:i'?m|i\s+am)\s+(?P<state>[a-z][a-z '\-]{2,30})\s*[.!?]*$",
    re.I)
AIM_VERB = frozenset("get getting be been become becoming feel feeling look looking stay".split())

A_DEADLINE_CLAUSE = re.compile(
    r"\s+(?:before|by|until|till|ahead\s+of|in\s+time\s+for)\s+.*$", re.I)

LENGTH_WORDS = frozenset("""
how long soon many much weeks week months month days day years year hours hour will would does do
did it that this take takes taken be is till until before from now to see notice seeing a an the
difference differences result results normally usually roughly about actually and so but ok okay
then expect should could might start any go going i ill we
""".split())


DISTRESS = frozenset("""
cry crying cried sob sobbing weep weeping tears sad sadder unhappiest unhappy depressed
depression anxious anxiety anxiousness panic panicking grieve grieving grief bereaved bereavement
die dying died death dead funeral bury mourning mourn miss missing hurt hurting pain ache aching
suicide self lonely alone""".split())


def _a_length_ask(text):
    words = re.findall(r"[a-z']+", " ".join(str(text or "").lower().split()))
    if not words or len(words) > 8:
        return False
    if not re.search(r"\bhow\s+(?:long|soon|many\s+(?:weeks|months|days|hours|years))\b",
                     " ".join(words)):
        return False
    return all(word in LENGTH_WORDS for word in words)


ACTIVITY_WORDS = frozenset("""
training practise practice practices lesson lessons session sessions class classes study studying
revision revising prep preparation coaching drills workout workouts
""".split())


def _a_length_ask_of_the_aim(text):
    words = re.findall(r"[a-z']+", " ".join(str(text or "").lower().split()))
    if not words or len(words) > 10:
        return False
    if not re.search(r"\bhow\s+(?:long|soon|many\s+(?:weeks|months|days|hours|years))\b",
                     " ".join(words)):
        return False
    return all(word in LENGTH_WORDS or word in ACTIVITY_WORDS or word == "of" for word in words)


LENGTH_KEY_WORDS = frozenset("""
long soon weeks week months month years year hours hour days day minutes minute
""".split())

A_LENGTH_STATED = re.compile(
    r"\b(?:\d{1,4}|a|an|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|fifteen"
    r"|twenty|thirty|forty|fifty|sixty)\s+(?:to\s+\w+\s+)?"
    r"(?:seconds?|minutes?|hours?|days?|weeks?|months?|years?)\b", re.I)


A_PACE = re.compile(
    r"\b(?:a|an|one|two|three|four|five|half\s+a|\d[\d,]*(?:\s*to\s*\d[\d,]*)?)"
    r"\s+[a-z][\w-]*(?:\s+[a-z][\w-]*){0,2}?\s+(?:a|per|each)\s+"
    r"(?:week|month|day)\b", re.I)


def _answers_a_pace(ask, memory):
    found = _the_entry(ask, memory)
    if found is None:
        return False
    return bool(A_PACE.search(str(getattr(found, "reply", "") or "")))


def _the_entry(ask, memory):
    try:
        from ..knowledge.lookup import find
        from ..understanding import understand

        return find(understand(ask, memory))
    except Exception:
        return None


def _answers_a_length(ask, memory):
    found = _the_entry(ask, memory)
    if found is None:
        return False
    reply = str(getattr(found, "reply", "") or "")
    if not A_LENGTH_STATED.search(reply):
        return False
    for part in getattr(found, "key", ()) or ():
        for phrase in (part if isinstance(part, tuple) else (part,)):
            if set(str(phrase).lower().split()) & LENGTH_KEY_WORDS:
                return True
    return False


def _the_length_entry_about(ask, memory, aim_words):
    found = _the_entry(ask, memory)
    if found is None:
        return None
    if not A_LENGTH_STATED.search(str(getattr(found, "reply", "") or "")):
        return None
    keyed = set()
    for part in getattr(found, "key", ()) or ():
        for phrase in (part if isinstance(part, tuple) else (part,)):
            keyed |= set(str(phrase).lower().split())
    if not keyed & set(w for w in aim_words if len(w) > 1):
        return None
    return found


def _answers_a_length_about(ask, memory, aim_words):
    return _the_length_entry_about(ask, memory, aim_words) is not None


def _an_aim_before_the_side_question(turns, memory):
    said = " ".join(str((memory or {}).get("last_answer") or "").lower().split())
    if A_LENGTH_STATED.search(said) or A_PACE.search(said):
        return ""
    for row in reversed([r for r in turns[:-1] if isinstance(r, dict)][-3:]):
        line = " ".join(str(row.get("user") or "").strip().split())
        if line and A_GOAL.match(line):
            return line
    return ""


def _the_aim_and_its_length_question(text, memory):
    outcome = OUTCOME_ASK.search(" ".join(str(text or "").lower().split()))
    if not _a_length_ask(text) and not _a_length_ask_of_the_aim(text) and not outcome:
        return "", False
    turns = [row for row in (memory or {}).get("turns") or [] if isinstance(row, dict)]
    if not turns:
        return "", False
    before = " ".join(str(turns[-1].get("user") or "").strip().split())
    if not before:
        return "", False
    match = A_GOAL.match(before)
    if not match:
        before = _an_aim_before_the_side_question(turns, memory)
        if not before:
            return "", False
        match = A_GOAL.match(before)
        if not match:
            return "", False
    if re.search(r"\bhow\s+(?:long|soon|many)\b", before, re.I):
        return "", False
    verb = GOAL_VERB.get(match.group("how").lower(), "")
    what = re.sub(r"^to\s+", "", match.group("what"), flags=re.I)
    deadline = bool(A_DEADLINE_CLAUSE.search(what))
    goal = A_DEADLINE_CLAUSE.sub("", what).strip(" .,;:-")
    words = goal.split()
    if not 1 <= len(words) <= 6:
        return "", False
    if not re.search(r"[a-z]{3}", goal):
        return "", False
    if any(word in DISTRESS for word in re.findall(r"[a-z']+", goal.lower())):
        return "", False
    if outcome:
        state = re.sub(r"\s+", " ", outcome.group("state")).strip()
        if state != re.sub(r"^(?:" + "|".join(sorted(AIM_VERB)) + r")\s+", "", goal.lower()):
            return "", False
    aim = (verb + goal).lower().strip()
    activity = [w for w in re.findall(r"[a-z']+", " ".join(str(text or "").lower().split()))
                if w in ACTIVITY_WORDS]
    if activity:
        as_it_stands = " ".join(re.findall(r"[a-z']+", " ".join(str(text or "").lower().split())))
        if _answers_a_length_about(as_it_stands, memory, goal.lower().split()):
            return "", deadline
        said = str(turns[-1].get("bot") or "").strip().lower()
        for with_the_activity in ("how long does " + activity[0] + " for " + aim + " take",
                                  "how long does " + activity[0] + " for "
                                  + re.sub(r"^[a-z]+\s+", "", aim) + " take"):
            found = _the_length_entry_about(with_the_activity, memory, goal.lower().split())
            if found is None:
                continue
            reply = str(getattr(found, "reply", "") or "").strip().lower()
            if reply and reply[:70] in said:
                continue
            return with_the_activity, deadline
    asked = "how long does it take to " + aim
    if _answers_a_length(asked, memory):
        return asked, deadline
    paced = "how fast can i " + (verb + goal).lower()
    if _answers_a_pace(paced, memory):
        return paced, deadline
    if _answers_a_pace(asked, memory):
        return asked, deadline
    return "", deadline


def a_goal_measured(text, memory):
    return _the_aim_and_its_length_question(text, memory)[0]


def a_length_about_an_aim_on_a_deadline(text, memory):
    asked, deadline = _the_aim_and_its_length_question(text, memory)
    return asked if deadline else ""



NO_THANKS = re.compile(
    r"^\s*(?:no|nope|nah|not)\b[\s,]*(?:"
    r"th(?:anks|ank\s+you|anks\s+you|x)|ta|cheers|mate|love)\b"
    r"[\s,]*(?:(?:though|then|but|anyway|really|at\s+all|so|ok|okay|very\s+much|any)\b[\s,]*)*"
    r"[.!]*\s*$", re.I)


def _no_thanks(text):
    return bool(NO_THANKS.match(" ".join(str(text or "").split())))


def follow_up(text, memory):
    aim = a_goal_measured(text, memory)
    if aim:
        return aim
    again = a_measure_asked_again(text, memory)
    if again:
        return again
    missing = _not_got(text, memory)
    if missing:
        ask = _previous_ask(memory)
        if ask:
            if _said_the_food(memory, missing):
                return ask.rstrip(" .,!?") + " without " + missing
            return ""
        return "what can i make without " + missing
    if _answers_the_bot(text):
        return ""
    if _no_thanks(text):
        return ""
    if trouble.reads_as_trouble(text):
        return ""
    if BARE_ANOTHER.match(text or ""):
        return "ideas for anything else" if _previous_ask(memory) else ""
    said = thing(text)
    if not said:
        return ""
    if not _previous_ask(memory):
        return ""
    return "ideas for " + said


BARE_ANOTHER = re.compile(
    r"^\s*(?:(?:and|or|so|ok|okay|right|well|but|then|now|hmm|ha)\b[\s,]*)*"
    r"(?:(?:what|anything|something)\s+else|any\s+others?|"
    r"another\s+(?:one|idea|option|film|book|recipe|suggestion|pick|show))"
    r"(?:\s+(?:(?:is|are)\s+on|on|works?|then|tonight|now|please|for\s+me|"
    r"(?:would\s+)?you(?:'d)?\s*(?:would\s+)?(?:suggest|recommend|have|got)|do\s+you\s+have))*"
    r"\s*[.!?]*\s*$", re.I)


VIEW_FRAME = frozenset("""view opinion take takes thinking thoughts tuppence""".split())
VIEW_MANNER = frozenset("""honest real quick true actual blunt personal own full proper same
plain straight""".split())
VIEW_POSSESSIVE = frozenset("your my our the a an and also plus too then".split())


def names_nothing_to_be_about(said):
    words = [word for word in re.findall(r"[a-z']+", str(said or "").lower())
             if word not in VIEW_POSSESSIVE]
    return bool(words) and all(word in VIEW_FRAME or word in VIEW_MANNER for word in words)


FEELING_FILLER = frozenset("""
a an the just only bit little so really very quite too still today tonight now thanks thank
thankyou you im i m am is are was were be been feeling feel feels felt and but yeah well of
about kind sort
""".split())
FEELING_SAID_AS_A_PHRASE = (
    "wiped out", "done in", "dead on my feet", "run down", "no energy", "knackered out")


def _only_how_they_feel(text, memory):
    if not isinstance(memory, dict):
        return False
    read = memory.get("understood")
    if not isinstance(read, dict) or not read.get("emotion"):
        return False
    turns = memory.get("turns") or ()
    if turns and isinstance(turns[-1], dict) and turns[-1].get("module") == "answers":
        return False
    low = " ".join(str(text or "").lower().split())
    if not low or "?" in low or str(read.get("kind") or "") == "question":
        return False
    from ..compose.draft import FEELING as feeling_words, FEELING_PHRASES
    for phrase in tuple(FEELING_PHRASES) + FEELING_SAID_AS_A_PHRASE:
        low = low.replace(phrase, " ")
    words = re.findall(r"[a-z']+", low)
    if not words:
        return False
    return not [word for word in words
                if word not in FEELING_FILLER and word not in feeling_words]


def about_it(text, memory):
    if _answers_the_bot(text):
        return ""
    if trouble.reads_as_trouble(text):
        return ""
    from ..compose import fallback
    if fallback.reads_as_a_judgement(text):
        return ""
    if _only_how_they_feel(text, memory):
        return ""
    from . import facts
    corrected = facts.without_the_correction_opener(text) or text
    said = thing(corrected)
    if not said:
        return ""
    turns = [turn for turn in (memory or {}).get("turns") or [] if isinstance(turn, dict)]
    if not turns:
        return ""
    was = " ".join(str(turns[-1].get("user") or "").lower().split())
    if not was or was == " ".join(str(text or "").lower().split()):
        return ""
    if names_nothing_to_be_about(said):
        return ""
    return "what about " + said


MEASURE_ASK = re.compile(
    r"\b(?:how\s+(?:long|much|many|often|big|far|heavy|hot|warm|expensive)|"
    r"what\s+temperature)\b", re.I)
PROGRESS_ASK = re.compile(
    r"\bhow\s+long\b(?=[^.!?]*\b(?:until|till|before)\b)"
    r"|\bhow\s+long\s+(?:does\s+it\s+take\s+)?(?:to\s+)?(?:get|be|become)\s+"
    r"(?:good|any\s+good|decent|ok|okay|fluent|better)\b", re.I)
A_GERUND = re.compile(r"^[a-z]{4,}ing$")
A_DOING_NAMED = re.compile(
    r"\b(?:learn|learning|learnt)\s+to\s+(?P<doing>[a-z]{3,})\b"
    r"|\b(?:start|starting|started|try|trying|tried|practise|practising|practice|practicing|"
    r"how\s+to)\s+(?P<also>[a-z]{3,})\b", re.I)
A_FIGURE_ON_THE_END = re.compile(r"^\d+[a-z]{0,2}$", re.I)


def a_figure_on_the_doing(memory, word):
    if not word:
        return ""
    said = _the_plan_said(memory, word)
    if not said:
        return ""
    words = re.findall(r"[a-z0-9']+", said)
    for index, one in enumerate(words[:-1]):
        if one == word.lower() and A_FIGURE_ON_THE_END.match(words[index + 1]):
            return words[index + 1]
    return ""


def is_a_progress_ask(text):
    return bool(PROGRESS_ASK.search(str(text or "")))


def _the_doing(word, memory):
    said = _the_plan_said(memory, word)
    if not said or not word:
        return ""
    word = word.lower()
    named = False
    for found in A_DOING_NAMED.finditer(said):
        doing = found.group("doing") or found.group("also") or ""
        if doing == word:
            named = True
            break
        if doing.endswith("ing") and doing[:-3].rstrip("n") == word.rstrip("n"):
            named = True
            break
    if not named:
        named = the_doing_the_plan_named(word, memory)
    if not named:
        return ""
    return _the_ing(word)


A_PLAN_TO_THE_DOING = re.compile(
    r"\b(?:want|wants|wanting|wanted|hope|hoping|hoped|plan|planning|planned|aim|aiming|aimed|"
    r"intend|intending|learn|learning|learnt|try|trying|tried|would\s+like|would\s+love)"
    r"\s+to\s+%s\b", re.I)


A_HOW_GOOD = re.compile(
    r"\b(?:good|better|best|fluent|confident|comfortable|competent|proficient|capable|skilled|"
    r"decent|mastered|able\s+to|any\s+good)\b", re.I)


def the_doing_the_plan_named(word, memory):
    said = _the_plan_said(memory, word)
    if not said or not word:
        return False
    return bool(re.search(A_PLAN_TO_THE_DOING.pattern % re.escape(word.lower()), said, re.I))


def _the_plan_said(memory, word):
    turns = [row for row in ((memory or {}).get("turns") or []) if isinstance(row, dict)]
    said = []
    for row in turns[-4:]:
        line = " ".join(str(row.get("user") or "").lower().split())
        if line and word.lower() in re.findall(r"[a-z0-9']+", line):
            said.append(line)
    topic = " ".join(str(the_subject(memory) or "").lower().split())
    if topic:
        said.append(topic)
    return " | ".join(said)


def _the_ing(word):
    if not word or word.endswith("ing"):
        return word
    if len(word) > 3 and word.endswith("e") and word[-2] not in "aeiou":
        return word[:-1] + "ing"
    if len(word) <= 5 and re.search(r"[^aeiou][aeiou][bdgklmnprst]$", word):
        return word + word[-1] + "ing"
    return word + "ing"
PROGRESS_WORDS = frozenset("""
good any decent ok okay fine fluent confident comfortable competent proficient proficiently
better well able capable mastered skilled basics basic conversational conversation
play playing speak speaking read reading write writing hold manage manage use using
get getting become becoming at it to be can could will would until till before by
im i'm i am then actually really genuinely properly roughly about
""".split())
MEASURE_VERBS = frozenset("""
take takes taking took last lasts lasting cost costs costing
be being been get gets getting got happen happens happening""".split())
MEASURE_WORDS = frozenset("""
how what long much many often big far heavy hot warm expensive temperature time times
second seconds minute minutes hour hours day days week weeks month months year years
cost costs costing price prices charge charges worth pay pays spend spends need needs
a an the per
i me my mine we our us you your should would will shall can could do does did be is are was were
has have had having
it its them they that this these those there one ones
""".split())
A_FAULT = frozenset("""
broken broke bust busted stopped dead leaking leaky faulty failed failing cracked blocked
jammed stuck gone kaput dodgy unreliable""".split())
NOT_THE_THING = frozenset("""
worried worry worries worrying anxious anxiety scared afraid nervous stressed stress upset angry
annoyed sad unhappy happy excited tired exhausted confused unsure lost stuck glad pleased
thinking thought considering planning hoping wanting looking interested keen trying dreaming
weighing wondering
""".split())
A_GETTING = frozenset("""
buy buys buying get gets getting purchase purchases purchasing pick picks picking choose chooses
choosing order orders ordering
""".split())

ASPECT_ASKS = (
    (frozenset("cost costs price prices expense expenses upkeep costing".split()),
     "how much does the {thing} cost"),
    (frozenset("food feeding feed diet".split()), "what do i feed the {thing}"),
)
FED_THINGS = frozenset("""
dog dogs puppy puppies cat cats kitten kittens rabbit rabbits bunny bunnies guinea pig pigs hamster
hamsters gerbil gerbils rat rats mouse mice ferret ferrets parrot parrots budgie budgies bird birds
fish goldfish chicken chickens hen hens cockerel horse horses pony ponies tortoise tortoises
snake snakes lizard lizards gecko geckos tortoise degu degus chinchilla chinchillas
""".split())
ASPECT_FILLERS = frozenset("""
and so or but also then ok okay well what about how the a an any more of
""".split())
ASPECT_NOUNS = frozenset().union(*(nouns for nouns, _ in ASPECT_ASKS))


IN_PROGRESS = re.compile(
    r"\b(?:im|i'm|i am|we're|we are|hes|he's|shes|she's|theyre|they're|ive|i've)\b"
    r"(?:\s+(?:still|also|just|been|busy|now))*\s+"
    r"((?:[a-z']+\s+){0,6}?[a-z]{2,}ing\b[^.?!,]*)", re.I)
def _the_doing_in_hand(memory):
    for turn in reversed((memory or {}).get("turns") or []):
        if not isinstance(turn, dict):
            continue
        said = " ".join(str(turn.get("user") or "").split())
        if not said:
            continue
        found = IN_PROGRESS.search(said)
        return found.group(1).strip(" ,;:-") if found else ""
    return ""


THE_LENGTH_FOR_IT = re.compile(
    r"^(?:and\s+|so\s+|ok\s+|okay\s+|then\s+|also\s+|roughly\s+|about\s+)?"
    r"(?:how\s+long|how\s+much\s+time|how\s+many\s+(?:hours|minutes|days|weeks|months))"
    r"[^.?!]{0,24}$", re.I)
LENGTH_NOT = re.compile(r"\b(?:until|till|before|after|ago|since|between|every|each"
                        r"|\d+\s*(?:h|hr|hrs|hours?|minutes?|days?|weeks?))\b", re.I)
LENGTH_FILLERS = frozenset("""
supposed going go went spent took long should will would does do did i you we they it that this
is are be last for about of
""".split())


JOURNEY = re.compile(r"^(?:going|go|goes|heading|off|flying|travelling|traveling|visiting|moving|"
                     r"coming|leaving|driving|walking|cycling)\b", re.I)


def the_duration_for_the_doing(text, memory):
    said = " ".join(str(text or "").split()).strip(" .!?,")
    if not said or len(said.split()) > 8:
        return ""
    if not THE_LENGTH_FOR_IT.match(said) or LENGTH_NOT.search(said):
        return ""
    for word in re.findall(r"[a-z']+", said.lower()):
        if word in MEASURE_WORDS or word in MEASURE_VERBS or word in POINTS_BACK:
            continue
        if word in LENGTH_FILLERS or word in PLACE_WORDS:
            continue
        if word in PLACE_PREPOSITIONS or word in PLACE_ARTICLES:
            continue
        return ""
    doing = _the_doing_in_hand(memory)
    if not doing or len(doing.split()) > 7 or JOURNEY.match(doing):
        return ""
    if _the_place_belongs_to_the_doing(said, doing, memory):
        return ""
    return "how long does it take to " + doing


def _the_place_belongs_to_the_doing(said, doing, memory):
    from ..knowledge import by_topic
    from ..understanding import understand
    from .topics import _entry
    place = str((understand(said, memory) or {}).get("subject") or "")
    if not place:
        return False
    item = _entry("how long does it take to " + doing)
    if item is None:
        return False
    domain = str(getattr(item, "domain", "") or "")
    if not domain:
        return False
    kind = str((understand(place, memory) or {}).get("topic") or "")
    if not kind:
        return False
    return kind not in by_topic().get(domain, ())


def _the_aspect_asked(low, thing):
    rest = [word for word in low if word not in ASPECT_FILLERS]
    if len(rest) != 1:
        return ""
    for nouns, shape in ASPECT_ASKS:
        if rest[0] not in nouns:
            continue
        if "{thing}" in shape and shape.startswith("what do i feed") and thing not in FED_THINGS:
            continue
        return shape
    return ""


BEST_TIME_TO_DO = re.compile(
    r"^(?:when|what)(?:'s|s| is| was)?\s+(?:the\s+)?"
    r"(?:best|right|good|ideal|safest|cheapest|easiest)\s+"
    r"(?:time|month|week|season|day|part)\s+(?:to|for)\s+(?P<rest>.+)$", re.I)
POINTS_AT_A_THING = frozenset("it its them that this these those one ones".split())
A_VAGUE_JOB = frozenset("""do doing get getting go going make making start starting sort sorting
    prep prepare preparing deal dealing have""".split())
A_BARE_JOB = re.compile(r"\b(?:should|could|would|can|shall|will|to)\s+(?:i\s+|we\s+|you\s+)?"
                        r"([a-z]{3,})\b", re.I)
NOT_THE_JOB = frozenset("""i me my we you your the a an and but so if of for in on at it its
    that this them they he she there here not no yes please thanks need needs want wants have
    has had do did does am is are was were be been got get going want trying""".split())


def _the_job_before(memory):
    turns = [row for row in ((memory or {}).get("turns") or []) if isinstance(row, dict)]
    if not turns:
        return ""
    said = " ".join(str(turns[-1].get("user") or "").lower().split())
    for word in reversed(re.findall(r"[a-z']+", said)):
        if len(word) < 4 or word in NOT_THE_JOB:
            continue
        if word.endswith("ing") or (word.endswith("ed") and len(word) > 4):
            stem = word[:-3] if word.endswith("ing") else word[:-2]
            if len(stem) > 3 and stem[-1] == stem[-2] and stem[-1] not in "lsz":
                stem = stem[:-1]
            if len(stem) > 2 and stem not in NOT_THE_JOB:
                return stem
    found = A_BARE_JOB.search(said)
    if found and found.group(1) not in NOT_THE_JOB:
        return found.group(1)
    return ""


def the_best_time_to_do_it(text, understood, memory=None):
    said = " ".join(str(text or "").split()).strip(" .!?")
    if not said or len(said.split()) > 14:
        return ""
    found = BEST_TIME_TO_DO.match(said)
    if not found:
        return ""
    words = re.findall(r"[a-z']+", found.group("rest").lower())
    if not any(word in POINTS_AT_A_THING for word in words):
        return ""
    if any(word not in POINTS_AT_A_THING and word not in A_VAGUE_JOB and len(word) > 2
           for word in words):
        return ""
    ref = (understood or {}).get("ref") if isinstance(understood, dict) else None
    target = ""
    for word in ("it", "they", "them", "that", "this", "those", "these"):
        said_target = " ".join(str((ref or {}).get(word) or "").split())
        if said_target and said_target.lower() not in POINTS_AT_A_THING:
            target = said_target
            break
    if not target:
        return ""
    rest = found.group("rest")
    job = re.match(r"(\w+)", rest)
    if job and job.group(1).lower() in A_VAGUE_JOB:
        before = _the_job_before(memory)
        if not before:
            return ""
        if before:
            rest = rest[job.end():].strip()
            rest = re.sub(r"\b(?:it|its|them|that|this|those|these|one|ones)\b", target,
                          rest, count=1, flags=re.I)
            return "when is the best time to " + before + " " + rest
    head = said[:found.start("rest")]
    rest = re.sub(r"\b(?:it|its|them|that|this|those|these|one|ones)\b", target,
                  rest, count=1, flags=re.I)
    return head + rest


def _only_the_measure(low):
    return all(word in MEASURE_WORDS or word in LIGHT_DOING or word in PLACE_WORDS
               or word in PLACE_PREPOSITIONS or word in PLACE_ARTICLES
               or (index + 1 < len(low) and (word, low[index + 1]) in PLACE_PAIRS)
               for index, word in enumerate(low))


def about_the_subject(text, memory):
    said = " ".join(str(text or "").strip().split())
    said = said.strip(" .!?")
    said = _without_and_at_the_start(said)
    if not said or len(said.split()) > 12:
        return ""
    low = [word.lower().strip(".,;:!?") for word in said.split()]
    timed = the_duration_for_the_doing(said, memory)
    if timed:
        return timed
    said_the_thing = subject_word(memory)
    asked = _the_aspect_asked(low, said_the_thing)
    if asked:
        return asked.format(thing=said_the_thing) if said_the_thing else ""
    if not MEASURE_ASK.search(said):
        return ""
    place = _the_place_phrase(low)
    if not place and not any(word in POINTS_BACK for word in low) and not _only_the_measure(low):
        return ""
    faulty = a_faulty_thing(memory)
    while faulty and low and low[0] in _A_CONNECTIVE:
        low = low[1:]
    bare = not any(word in POINTS_BACK for word in low)
    progress = bool(PROGRESS_ASK.search(said))
    for index, word in enumerate(low):
        if word in MEASURE_WORDS or word in POINTS_BACK or (bare and word in LIGHT_DOING):
            continue
        if word in PLACE_WORDS:
            continue
        if faulty and word in MEASURE_VERBS:
            continue
        if progress and word in PROGRESS_WORDS:
            continue
        if word in PLACE_PREPOSITIONS or word in PLACE_ARTICLES:
            continue
        if index + 1 < len(low) and (word, low[index + 1]) in PLACE_PAIRS:
            continue
        return ""
    said_the_thing = subject_word(memory)
    if place:
        in_hand = _the_thing_in_hand(memory, said) or said_the_thing
        if not in_hand:
            return ""
        return _about_the_thing_in_the_place(low, place, in_hand, said, memory)
    if not said_the_thing:
        return ""
    if low and len(low) < len(said.split()):
        said = " ".join(said.split()[-len(low):])
    if not any(word in POINTS_BACK for word in low):
        return said + " " + said_the_thing
    written = "the " + said_the_thing
    doing = _the_doing(said_the_thing, memory) if progress else ""
    if (doing and not A_HOW_GOOD.search(said)
            and a_figure_on_the_doing(memory, said_the_thing)
            and re.search(r"\bhow\s+long\b", said, re.I)):
        return ""
    if doing or (progress and A_GERUND.match(said_the_thing)):
        written = doing or said_the_thing
    return re.sub(r"\b(?:it|that|this|they|them|those|these|one|ones)\b",
                  lambda found: written, said, count=1, flags=re.I)


_AND_AT_THE_START = re.compile(r"^(?:and|then|also|so)\s+", re.I)


def _without_and_at_the_start(said):
    return _AND_AT_THE_START.sub("", said, count=1)


PLACE_WORDS = frozenset("""
oven hob microwave grill grillpan airfryer fryer pan saucepan pot steamer slowcooker cooker kettle
toaster barbecue bbq fridge freezer dishwasher washingmachine dryer radiator sink bath
""".split())
PLACE_PAIRS = frozenset({("slow", "cooker"), ("air", "fryer"), ("grill", "pan"),
                         ("pressure", "cooker"), ("rice", "cooker"), ("tumble", "dryer")})
LIGHT_DOING = frozenset("""go goes going do does doing get take use try keep start""".split())
PLACE_PREPOSITIONS = frozenset("in on at into under over".split())
PLACE_ARTICLES = frozenset("the a an my our your their".split())
BASE_DOING = ("cook", "bake", "roast", "boil", "fry", "grill", "steam", "make", "prepare",
              "reheat", "heat", "store", "keep", "freeze", "defrost", "warm")


def _the_forms(base):
    forms = {base, base + "s", base + "ing", base + "ed"}
    if base[-1] in "aeiou":
        forms.add(base[:-1] + "ing")
    elif base.endswith("y"):
        forms |= {base[:-1] + "ies", base[:-1] + "ied"}
    elif base[-1] not in "aeiouwxy":
        forms |= {base + base[-1] + "ing", base + base[-1] + "ed"}
    return forms


DOING_BASE = {form: base for base in BASE_DOING for form in _the_forms(base)}
DOING = frozenset(DOING_BASE)


def _the_doing_word(text):
    for word in str(text or "").split():
        bare = word.lower().strip(".,;:!?")
        if bare in DOING_BASE:
            return DOING_BASE[bare]
    return ""


def _a_doing_word(text):
    return bool(_the_doing_word(text))


def _what_the_chat_is_on(memory, this_line):
    mine = " ".join(str(this_line or "").lower().split())
    for turn in reversed((memory or {}).get("turns") or []):
        if not isinstance(turn, dict):
            continue
        was = str(turn.get("user") or "")
        if not was.strip() or " ".join(was.lower().split()) == mine:
            continue
        return was
    record = (memory or {}).get("topic")
    if isinstance(record, dict) and record.get("text"):
        return str(record["text"])
    return ""


def _the_thing_in_hand(memory, this_line):
    was = _what_the_chat_is_on(memory, this_line)
    for word in reversed([part for part in re.split(r"[^a-z']+", was.lower()) if part]):
        if len(word) < 3 or word in MEASURE_WORDS or word in PLACE_WORDS:
            continue
        if word in DOING or word in POINTS_BACK or word in PLACE_PREPOSITIONS:
            continue
        return word
    return ""


def _the_place_phrase(low):
    for index, word in enumerate(low):
        if word not in PLACE_WORDS:
            continue
        first = index
        if index and (low[index - 1], word) in PLACE_PAIRS:
            first = index - 1
        start = first
        while start and (low[start - 1] in PLACE_PREPOSITIONS or low[start - 1] in PLACE_ARTICLES):
            start -= 1
        return " ".join(low[start:index + 1])
    return ""


def _about_the_thing_in_the_place(low, place, said_the_thing, this_line, memory):
    if said_the_thing in PLACE_WORDS:
        return ""
    doing = _the_doing_word(_what_the_chat_is_on(memory, this_line))
    if not doing:
        return ""
    measure = []
    for word in low:
        if word in PLACE_WORDS or word in PLACE_PREPOSITIONS or word in PLACE_ARTICLES:
            break
        if word in POINTS_BACK:
            break
        measure.append(word)
    if not measure or ("how" not in measure and "what" not in measure):
        return ""
    if measure != ["how", "long"]:
        return ""
    written = "how long does it take to " + doing + " " + said_the_thing + " " + place
    if not _the_rewrite_earns_its_place(" ".join(low), written, memory):
        return ""
    return written


def _the_rewrite_earns_its_place(alone, written, memory):
    from .topics import _entry
    was = _entry(alone)
    became = _entry(written)
    if was is None or became is None or became is was:
        return False
    last = (memory or {}).get("last_answer")
    if isinstance(last, dict) and last.get("id") and last.get("id") == getattr(became, "id", None):
        return False
    return True


STATE_WORDS = frozenset("""
still now already again left gone flat empty full broken dead stuck worse better okay ok
smells smell stinks stinking works working not never
""".split())
A_FIGURE = re.compile(r"\b(?:\d+(?:\.\d+)?\s*(?:%|percent|hours?|minutes?|days?|weeks?|litres?|"
                      r"liters?|kilos?|kg|metres?|miles?|pounds?))\b", re.I)
A_PLACE = re.compile(r"\b(?:at|in|on|under|behind)\s+(?:work|home|the office|the car|the garage|"
                     r"the kitchen|the shed|the loft|the shop|the hotel|my bag|my pocket|my desk)"
                     r"\b", re.I)


def _thing_in_hand(memory):
    topic = memory.get("topic") if isinstance(memory, dict) else None
    said = (topic or {}).get("words") if isinstance(topic, dict) else None
    if not isinstance(said, list) or not said:
        return subject_word(memory)
    answer = memory.get("last_answer") if isinstance(memory, dict) else None
    keys = [str(word).lower() for word in ((answer or {}).get("keys") or ())]
    subject_keys = _the_answers_own_subject(answer)
    found = []
    for wanted in (subject_keys, keys):
        for word in reversed(said):
            bare = str(word).lower().strip(".,;:!?")
            if len(bare) < 3 or bare in NOT_THE_THING or bare in STATE_WORDS:
                continue
            if bare in found:
                continue
            if _only_a_particle(bare, (topic or {}).get("text") or ""):
                continue
            if any(key[:4] == bare[:4] for key in wanted):
                found.append(bare)
    if not found:
        only = subject_word(memory)
        return [only] if only else []
    return found


def _only_a_particle(word, text):
    said = " " + " ".join(str(text or "").lower().split()) + " "
    found = list(re.finditer(r"\b" + re.escape(word) + r"\b", said))
    if not found:
        return False
    for match in found:
        before = said[:match.start()].split()
        if not before:
            return False
        last = before[-1].strip(".,;:!?()")
        if not (last in kinds.VERBISH or last in kinds.VERB_FORMS
                or last.endswith(("ing", "ed"))):
            return False
    return True


def _the_answers_own_subject(answer):
    entry_id = (answer or {}).get("id") if isinstance(answer, dict) else ""
    if not entry_id:
        return ()
    try:
        from ..knowledge import entries as all_entries
        for item in all_entries():
            if getattr(item, "id", "") == entry_id and item.key:
                first = item.key[0]
                parts = first if isinstance(first, (tuple, list, frozenset, set)) else (first,)
                return tuple(str(part).lower() for part in parts if isinstance(part, str))
    except Exception:
        return ()
    return ()


def reported_states(text, memory):
    said = " ".join(str(text or "").strip().split()).strip(" .!?")
    if not said or len(said.split()) > 16:
        return []
    low = [word.lower().strip(".,;:!?()") for word in said.split()]
    if not any(word in POINTS_BACK for word in low):
        return []
    if ASKING.match(said) or MEASURE_ASK.search(said):
        return []
    things = _thing_in_hand(memory)
    if not things:
        return []
    reported = bool(A_FIGURE.search(said) or A_PLACE.search(said)
                    or {word for word in low} & STATE_WORDS)
    if not reported:
        return []
    reads = []
    for thing in things:
        if thing in low:
            continue
        written = re.sub(r"\b(?:its|it's)\b", "my " + thing + " is", said, count=1, flags=re.I)
        written = re.sub(r"\b(?:it|they|them|their)\b", "my " + thing, written, count=1,
                         flags=re.I)
        if written not in reads:
            reads.append(written)
    return reads


CARE_VERBS = frozenset("""
feed feeds feeding fed water waters watering watered repot repotting repotted prune prunes
pruning pruned deadhead deadheading deadheaded stake staking staked mulch mulching mulched
mist misting misted thin thinning thinned aerate aerating
""".split())
A_HOW_OFTEN = re.compile(
    r"\b(?:every|each|once|twice|three times|a|per|daily|weekly|fortnightly|monthly|yearly|\
annually|regularly|sometimes|usually|often|january|february|march|april|may|june|july|august|\
september|october|november|december|spring|summer|autumn|winter)\b", re.I)
CARE_NOT_THE_THING = frozenset("""
baby babies child children kid kids toddler toddlers mum mom dad daddy mummy son sons daughter
family dog dogs cat cats puppy puppies kitten kittens fish rabbit hamster guinea bird birds
parrot chickens hen hens horse horses me myself us everyone everybody
""".split())


WHERE_IT_STANDS = frozenset("""
windowsill window sill shelf table bench desk worktop counter sideboard floor carpet rug patio
balcony garden greenhouse conservatory kitchen bathroom bedroom lounge hall hallway garage shed
attic loft cellar porch utility laundry nursery study room house home flat pot pots tub tray
basket fridge freezer oven hob grill cupboard cupboard drawer desk
""".split())


def _the_persons_own_words(memory):
    answer = memory.get("last_answer") if isinstance(memory, dict) else None
    wanted = list(_the_answers_own_subject(answer))
    turns = (memory or {}).get("turns") if isinstance(memory, dict) else None
    own = []
    for turn in reversed(turns or ()):
        for word in re.split(r"[^A-Za-z']+", str((turn or {}).get("user") or "").lower()):
            if len(word) > 3 and word not in own:
                own.append(word)
    found = []
    for source in (wanted, [str(word).lower() for word in _thing_in_hand(memory)]):
        for key in source:
            for word in own:
                if len(word) < 4 or word in found or word in _NOT_THE_PRACTICE:
                    continue
                if (word in NOT_THE_THING or word in MEASURE_WORDS or word in STATE_WORDS
                        or word in WHERE_IT_STANDS):
                    continue
                if key[:4] == word[:4]:
                    found.append(word)
        if found:
            break
    if found:
        return found
    return [str(word).lower() for word in _thing_in_hand(memory)
            if len(str(word)) > 3 and str(word).lower() not in _NOT_THE_PRACTICE
            and str(word).lower() not in WHERE_IT_STANDS]


_NOT_THE_PRACTICE = frozenset("""
every each once twice three times week weeks day days month months year years morning
mornings evening evenings night nights daily weekly fortnightly monthly regularly sometimes
usually often spring summer autumn winter january february march april may june july august
september october november december about around roughly usually also still just really
""".split()) | CARE_VERBS


PERSON_OPEN = re.compile(
    r"^\W*(?:(?:and|but|so|oh|also|well|yeah|yep|ok|okay|right|alright)\W+)*"
    r"(?:i|im|i'?m|i'?ve|ive|i'?d|id|we|we'?re|were|we'?ve|me|us|she|he|they|there"
    r"|it|its|it'?s|they're)\b",
    re.I)
FACT_OPEN = re.compile(
    r"^\W*(?:(?:and|but|so|oh|also|well|yeah|yep|ok|okay|right|alright|nothing|just)\W+)*"
    r"(?:for|with|on|in|at|by|near|from|about|only|mostly|usually|mainly|every|each)\b", re.I)
FACT_FILLER = frozenset("""the and but for with about only just even also very really quite
    still now then than that this these those there their them they she her his him its it
    was were been being have has had does did doing get got going make made more most some any
    im ive id you your my our me us we i am is are not no yes like want need know think""".split())
TIMES_ONLY = frozenset("""morning mornings evening evenings night nights afternoon afternoons
    weekend weekends weekday weekdays day days week weeks month months winter winters summer
    summers autumn spring springtime sometimes always usually mostly mainly normally lately
    recently today tonight tomorrow""".split())
JOINING = frozenset("""before after until till while when whenever since once if because cause
    though although whereas unless during without within between through across along around
    behind below beside beyond onto upon than""".split())
FACT_MOST_WORDS = 14
A_CHOICE = re.compile(
    r"\bwhether\b|\bwhat\s+to\b|\bhow\s+to\b|\bwhat\s+i\s+should\b|\bif\s+i\s+should\b|"
    r"\bnot\s+sure\s+(?:if|whether|what|how)\b", re.I)
COUNT_WORDS = frozenset("""one two three four five six seven eight nine ten eleven twelve
    couple few several many lot lots""".split())
PEOPLE_WORDS = frozenset("""kid kids child children boy boys girl girls son sons daughter
    daughters baby babies toddler toddlers teen teens teenager teenagers grandchild
    grandchildren person people adult adults flatmate flatmates housemate housemates""".split())
NOT_THE_SUBJECT = frozenset("""buy buying bought choose choosing chose pick picking want wanted
    wanted need needed get getting got looking look looked find finding""".split())

_NOT_A_PRONOUN = frozenset("""
he she him her his hers them they their theirs himself herself themselves
""".split())


def stated_about_the_person(text, memory):
    said = " ".join(str(text or "").strip().split()).strip(" .!?")
    if not said or len(said.split()) > FACT_MOST_WORDS:
        return []
    if "?" in str(text or "") or ASKING.match(said) or MEASURE_ASK.search(said):
        return []
    if A_CHOICE.search(said):
        return []
    if _a_place_of_its_own(memory):
        return []
    low = [word.lower().strip(".,;:!?()") for word in said.split()]
    if not (PERSON_OPEN.match(said) or FACT_OPEN.match(said) or A_FIGURE.search(said)):
        return []
    named = [word for word in low if len(word) > 2 and word not in TIMES_ONLY
             and word not in FACT_FILLER]
    if not named:
        return []
    if all(word in PEOPLE_WORDS or word in COUNT_WORDS for word in named):
        return []
    reads = []
    for word in subject_words(memory, text):
        if word in low:
            continue
        written = " ".join((word + " " + said).split())
        if written not in reads:
            reads.append(written)
    return reads


def _a_place_of_its_own(memory):
    read = memory.get("understood") if isinstance(memory, dict) else None
    if not isinstance(read, dict):
        return False
    for found in read.get("entities") or ():
        if isinstance(found, dict) and found.get("type") == "place":
            return True
    return False


def subject_words(memory, text=""):
    from ..understanding import kinds
    was = ""
    if text:
        record = the_carried_topic(memory, text)
        was = str((record or {}).get("text") or "") if isinstance(record, dict) else ""
    said = " ".join(str(was or the_subject(memory) or "").split()).lower()
    out = []
    for word in re.split(r"[^a-z0-9]+", said):
        if len(word) < 3 or word in out:
            continue
        if word in NOT_THE_THING or word in MEASURE_WORDS or word in STATE_WORDS:
            continue
        if word in _NOT_A_PRONOUN:
            continue
        if word in kinds.VERBISH or word in kinds.VERB_FORMS or word in NOT_THE_SUBJECT:
            continue
        out.append(word)
    return out[:4]


def care_reports(text, memory):
    said = " ".join(str(text or "").strip().split()).strip(" .!?")
    if not said or len(said.split()) > 12:
        return []
    low = [word.lower().strip(".,;:!?()") for word in said.split()]
    if not any(word in CARE_VERBS for word in low):
        return []
    if not A_HOW_OFTEN.search(said):
        return []
    if ASKING.match(said) or MEASURE_ASK.search(said):
        return []
    if any(word in CARE_NOT_THE_THING for word in low):
        return []
    rest = re.sub(r"^\s*(?:i|we|im|i'm|ive|i've)\s+", "", said, flags=re.I)
    for word in sorted(POINTS_BACK, key=len, reverse=True):
        rest = re.sub(r"\b" + re.escape(word) + r"\b", "", rest, count=1, flags=re.I)
    rest = " ".join(rest.split())
    if not rest:
        return []
    things = _the_persons_own_words(memory)
    if not things or things[0] in low:
        return []
    return [" ".join((things[0] + " " + rest).split())]


_A_CONNECTIVE = frozenset("and so but also then ok okay please".split())


def a_faulty_thing(memory):
    said = " ".join(str(the_subject(memory) or "").split()).lower()
    if not said:
        return False
    if _the_answer_gave_a_time(memory):
        return False
    return any(word in A_FAULT for word in re.split(r"[^a-z]+", said))


_A_TIME_IN_A_REPLY = re.compile(
    r"\b(?:\d+|an?|one|two|three|four|five|ten|fifteen|twenty|thirty|forty|forty-five|fifty|"
    r"sixty|ninety|half an|a couple of|a few)\s*"
    r"(?:second|seconds|minute|minutes|hour|hours|day|days|week|weeks|month|months|year|years)\b",
    re.I)


def _the_answer_gave_a_time(memory):
    turns = (memory or {}).get("turns") or []
    if not turns:
        return False
    return bool(_A_TIME_IN_A_REPLY.search(str(turns[-1].get("bot") or "")))


def the_thing(memory):
    said = " ".join(str(the_subject(memory) or "").split()).lower()
    if not said:
        return ""
    kept = [word for word in re.split(r"[^a-z0-9]+", said)
            if word and word not in A_FAULT and word not in NOT_THE_THING
            and word not in MEASURE_WORDS and word not in ("the", "and", "for", "with")]
    return " ".join(kept[:4])


def subject_word(memory):
    said = " ".join(str(the_subject(memory) or "").split()).lower()
    found = _the_noun_in(said)
    if found and all(word in A_GETTING for word in found):
        newest = (memory or {}).get("topic") if isinstance(memory, dict) else None
        own = str((newest or {}).get("text") or "") if isinstance(newest, dict) else ""
        found = _the_noun_in(" ".join(own.split()).lower())
    if found and found[-1] in PLACE_WORDS:
        before = _the_record_before(memory)
        if before:
            found = _the_noun_in(" ".join(str(before.get("text") or "").split()).lower()) or found
    return found[-1] if found else ""


def _the_noun_in(said):
    if not said:
        return []
    return [word for word in re.split(r"[^a-z]+", said)
            if len(word) > 2 and word not in NOT_THE_THING and word not in MEASURE_WORDS
            and word not in A_FAULT
            and word not in ("the", "and", "for", "with", "some", "any", "new")]


def _the_record_before(memory):
    records = [record for record in ((memory or {}).get("topics") or [])
               if isinstance(record, dict) and record.get("text")]
    newest = (memory or {}).get("topic")
    now = str((newest or {}).get("text") or "")
    for record in reversed(records):
        if str(record.get("text") or "") != now:
            return record
    return None


A_PURPOSE = re.compile(
    r"\b(?:it|that|this|they|them|he|she)\s+(?:would\s+be|is|are|was|were)\s+(?:for|to\s+be)\b|"
    r"\b(?:for|with)\s+(?:the|my|our|his|her|their|a|an)\b", re.I)
NOT_A_THING_END = frozenset("""
not never no yes ok okay thanks thank please too also very really much many more less
good bad fine same sure well now then again already still just today tomorrow yesterday
week month year morning evening night day weekend ever yet either
one two three four five six seven eight nine ten eleven twelve
""".split())


def a_newer_thing(memory, word):
    turns = [turn for turn in (memory or {}).get("turns") or [] if isinstance(turn, dict)]
    if not turns or not word:
        return ""
    last = " ".join(str(turns[-1].get("user") or "").lower().split()).strip(" .!?")
    if not last or A_PURPOSE.search(last):
        return ""
    tail = last.split()[-1].strip(".,;:!?")
    if (len(tail) < 4 or tail in VERBS or tail in NOT_A_THING_END or tail in POINTS_BACK
            or tail in A_FAULT):
        return ""
    if tail in ASPECT_NOUNS:
        return ""
    if tail == word or word in tail or tail in word:
        return ""
    return tail


A_TRIP_PART = (
    (re.compile(r"\b(?:stay|staying|hotel|hotels|accommodation|sleep|sleeping|hostel|hostels)\b"),
     "where should i stay in {place}"),
    (re.compile(r"\b(?:eat|eats|eating|food|restaurant|restaurants|dinner|lunch|breakfast|drink|"
                r"drinks|bar|bars|cafe|cafes|coffee|pizza|gelato)\b"),
     "where should i eat in {place}"),
    (re.compile(r"\b(?:see|sights|sightseeing|visit|visiting|museum|museums|gallery|galleries|"
                r"ruins|tour|tours)\b"),
     "what should i see in {place}"),
    (re.compile(r"\b(?:days?|long enough|enough time|how long)\b"),
     "how many days in {place}"),
    (re.compile(r"\b(?:when|month|months|season|weather|climate|temperature|"
                r"january|february|april|june|july|august|september|october|november|december|"
                r"spring|summer|autumn|winter)\b"),
     "when should i go to {place}"),
    (re.compile(r"\b(?:expensive|pricey|cost|costs|costing|afford|budget|spend|"
                r"how much)\b"),
     "is {place} expensive"),
)

_ASK_FILLER = frozenset("""
a an the and but or so also then too now ok okay please about for to in on at of it that this
i we you me us my our your there here any some much many more most best good worth should could
would can will do does did is are was were be been get got have has had going go stay stay
some anywhere somewhere place places area areas neighbourhood neighborhood part parts spot spots
nice pleasant decent good best spot
what where which how when why who whats like tell me info advice recommend recommends
recommendation recommendations suggest suggestion suggestions
need needs needed want wants wanted enough require required take takes give gives
one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen
sixteen seventeen eighteen nineteen twenty couple few several
""".split())

_GOING_AWAY = re.compile(
    r"\b(?:going|go|goes|off|heading|trip|trips|holiday|holidays|travel|travelling|traveling|"
    r"visit|visiting|fly|flying|flight|flights|weekend|weekends|break|away|abroad|booked|booking|"
    r"planning|thinking about|considering|looking at)\b", re.I)


def _the_trip_place(memory):
    known = (memory or {}).get("user")
    if not isinstance(known, dict):
        return ""
    places = [str(place).strip() for place in (known.get("places") or []) if str(place).strip()]
    if not places:
        return _the_place_the_bot_just_named(memory)
    place = places[-1]
    said = place.lower()
    turns = [turn for turn in (memory.get("turns") or []) if isinstance(turn, dict)]
    named_at = -1
    for index in range(len(turns) - 1, -1, -1):
        line = " ".join(str(turns[index].get("user") or "").lower().split())
        if not re.search(r"(?<![a-z])" + re.escape(said) + r"(?![a-z])", line):
            continue
        if not _GOING_AWAY.search(line):
            return ""
        named_at = index
        break
    if named_at < 0:
        plan = " ".join(str(known.get("plan") or "").lower().split())
        if not (said in plan and _GOING_AWAY.search(plan)):
            return ""
    card, card_at = _the_opening_place_at(memory)
    if card and card_at > named_at:
        return card
    return place
    card = _the_place_the_bot_just_named(memory)
    if card and said in card.lower():
        return place
    return ""


_LIVING_THERE = re.compile(
    r"\b(?:live|lives|lived|living|moved|moves|moving|relocate|relocated|relocating|grew up|"
    r"born|home|hometown|my flat|my house)\b", re.I)


_A_TIME_WORD = frozenset((
    "january", "february", "march", "april", "may", "june", "july", "august", "september",
    "october", "november", "december", "spring", "summer", "autumn", "winter", "the morning",
    "the evening", "the afternoon", "the end", "the meantime", "general", "fact", "short",
    "total", "terms", "the", "a", "an", "its", "their", "addition", "practice", "reality",
))


def _the_opening_place(memory):
    return _the_opening_place_at(memory)[0]


def _the_opening_place_at(memory):
    turns = (memory or {}).get("turns")
    if not isinstance(turns, list) or not turns:
        return "", -1
    for back, turn in enumerate(reversed(turns)):
        if not isinstance(turn, dict):
            continue
        opening = re.match(r"\s*in\s+(.{2,40}?)(?=[,:.!?]|\s(?:the|a|an|is|it|you|we)\b)",
                           str(turn.get("bot") or ""), re.I)
        if not opening:
            continue
        place = opening.group(1).strip()
        if place.lower() in _A_TIME_WORD:
            continue
        if re.match(r"(?i)(?:the|a|an|your|my|his|her|their|our|this|that)\b", place):
            continue
        if not place[:1].isupper():
            continue
        return place, len(turns) - 1 - back
    return "", -1


def _the_place_the_bot_just_named(memory):
    place = _the_opening_place(memory)
    if not place:
        return ""
    for turn in (memory or {}).get("turns") or []:
        if isinstance(turn, dict) and _LIVING_THERE.search(str(turn.get("user") or "")):
            return ""
    return place


def a_part_of_the_trip(text, memory):
    place = _the_trip_place(memory)
    if not place:
        return ""
    said = " ".join(str(text or "").lower().split()).strip(" .!?")
    if not said or len(said.split()) > 8:
        return ""
    part = ""
    words = set()
    earliest = None
    for pattern, asked in A_TRIP_PART:
        found = set(pattern.findall(said))
        if not found:
            continue
        at = min(found_.start() for found_ in pattern.finditer(said))
        if earliest is None or at < earliest:
            part = asked
            earliest = at
            words = set(re.split(r"[^a-z]+", " ".join(found))) | found
    if not part:
        return ""
    for matched in words:
        if re.search(r"\b(?:a|an)\s+" + re.escape(matched) + r"\b", said):
            return ""
    for word in re.split(r"[^a-z']+", said):
        if len(word) < 3 or word in _ASK_FILLER or word in words:
            continue
        if word in ("day", "days") and part.startswith("how many days"):
            continue
        return ""
    return part.format(place=place.lower() if place.isupper() else place)

def asks_a_part_of_the_trip(text, memory):
    if a_part_of_the_trip(text, memory):
        return True
    place = _the_trip_place(memory)
    said = " ".join(str(text or "").lower().split())
    name = place.lower()
    if not name or name not in said:
        return False
    return bool(a_part_of_the_trip(said.replace(name, " "), memory))


LIMIT = re.compile(
    r"\b(?:no|not|dont|doesnt|didnt|havent|isnt|without|ran out|run out|only got|only have|"
    r"short of|lacking|instead|left)\b", re.I)


def the_food_it_is_about(understood, memory):
    if not isinstance(understood, dict) or not isinstance(memory, dict):
        return ""
    record = understood.get("leans_on")
    if not isinstance(record, dict):
        return ""
    food = " ".join(str(record.get("subject") or "").split()).lower()
    if not food:
        return ""
    line = " ".join(str(understood.get("clean") or understood.get("text") or "").split()).lower()
    if not line or food in line:
        return ""
    raised = " ".join(str(record.get("text") or "").split()).lower()
    if raised and LIMIT.search(raised):
        return ""
    return food
