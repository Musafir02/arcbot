import re

from ..compose import pick
from ..understanding import breeds as breed_words
from . import history, others, user
from . import you as say_it_back
from . import facts as extract
from . import recall

TOLD_ABOUT = re.compile(
    r"^\W*(?:and\s+|also\s+|so\s+|but\s+|ok(?:ay)?\s+|wait\s+|quick\s+)?"
    r"(?:have|has|had|did)\s+(?:i|we)\s+(?:ever\s+|already\s+)?"
    r"(?:told|tell|mentioned|mention|said|say|talked|talk)\s+(?:you\s+)?"
    r"(?P<about>about\s+|of\s+)?(?P<what>[^?]+?)\s*\??$", re.I)
KNOW_ABOUT = re.compile(
    r"^\W*(?:and\s+|also\s+|so\s+|but\s+|ok(?:ay)?\s+|wait\s+|quick\s+|sorry\s+)?"
    r"(?:do|did|can|could)\s+(?:you|u)\s+(?:still\s+|actually\s+|even\s+|really\s+)?"
    r"(?:know|remember|recall)\s+"
    r"(?P<what>(?:anything\s+|something\s+|more\s+)?(?:about\s+|on\s+)?"
    r"(?:my|our)\s+\w[^?]*?|"
    r"(?:what|where|who|which|how\s+old)\s+(?:i|we)\s+[^?]*?)\s*\??$", re.I)
A_STATEMENT = re.compile(r"\b(?:is|are|was|were|am|will|would|can|could|have|has|had|"
                         r"do|does|did|i|we|you|im|i'm|ive|i've|id|i'd|ill|i'll|we're|we've|"
                         r"youre|you're|dont|don't|didnt|didn't|cant|can't|wont|won't)\b", re.I)
NOTHING_NAMED = re.compile(r"^what\s+(?:i|we)\s+(?:told|said)(?:\s+(?:you|u|me))?\s*$", re.I)
POINTING = frozenset("me it that this them us anything something everything".split())
IN_QUESTION = (
    (r"^(?:how old|what age)\s+(?:i|we)\s+(?:am|are|was|were)\b.*$", "my age"),
    (r"^what\s+(?:i|we)\s+(?:do|did)(?:\s+for (?:a living|work))?\b.*$", "what i do"),
    (r"^who\s+(?:i|we)\s+(?:am|are|was|were)\b.*$", "my name"),
    (r"^what\s+(?:i|we)(?:'m|'re| am|are|was|were)\s+(?:allergic|intolerant)\s+to\b.*$",
     "what im allergic to"),
    (r"^where\s+(?:i|we)\s+(?:live|lived|come from|was born|grew up|am from|'m from)\b.*$",
     "where i live"),
)
A_KIND = {"trip": "plan", "trips": "plan", "holiday": "plan", "holidays": "plan",
          "break": "plan", "travel": "plan", "flight": "plan", "flights": "plan",
          "hotel": "plan", "booking": "plan", "plan": "plan", "plans": "plan",
          "job": "job", "work": "job", "money": "budget", "budget": "budget",
          "broke": "budget", "skint": "budget", "cash": "budget", "savings": "budget",
          "car": "car", "vehicle": "car", "van": "car", "drive": "car",
          "driving": "car", "drove": "car", "mot": "car",
          "bike": "bike", "bicycle": "bike", "cycling": "bike", "cycle": "bike",
          "running": "running", "run": "running", "jogging": "running", "jog": "running",
          "runner": "running",
          "feelings": "feelings", "feeling": "feelings", "feel": "feelings", "felt": "feelings",
          "mood": "feelings", "emotions": "feelings", "emotion": "feelings",
          "flat": "flat", "house": "flat", "home": "flat", "landlord": "flat", "rent": "flat",
          "boiler": "flat", "heating": "flat", "mortgage": "flat",
          "age": "age", "name": "name", "diet": "diet",
          "allergy": "allergies", "allergies": "allergies",
          "kids": "kids", "kid": "kids", "children": "kids", "child": "kids"}
RELATION_WORDS = "|".join(sorted(extract.RELATIONS, key=len, reverse=True))
CHECK_OF_SOMEONE = re.compile(
    r"^\W*(?:is|are|was|were|does|do|did)\s+(?:my|our|your)\s+(?:" + RELATION_WORDS + r")"
    r"(?:'s|s)?\s+(?P<claim>[^?.!]{1,44})\s*[?.!]*$", re.I)
CORRECTION_WORDS = r"(?:and|also|so|actually|no|sorry|wait|oh|hmm|hold\s+on|correction|i\s+mean)"
CORRECTING = re.compile(r"^\W*(?:" + CORRECTION_WORDS + r"\b[,.!;:]?\s*){1,2}", re.I)
SAID_OF_SOMEONE = re.compile(
    r"^\W*(?:" + CORRECTION_WORDS + r"\b[,.!;:]?\s*){0,2}(?:my|our)\s+(?P<who>" + RELATION_WORDS + r")(?:'s|s)?\s+"
    r"(?:(?P<not>isnt|isn't|is not|wasnt|wasn't|was not|arent|aren't|are not|doesnt|doesn't|"
    r"does not|didnt|didn't|did not|hasnt|hasn't|has not|is n't)\s+(?P<pred>[^.,;!?]{1,40})"
    r"|(?P<verb>is|was|are|were|lives|works|has|got|goes|plays|studies|drives|does|did)\s+"
    r"(?P<pred2>[^.,;!?]{1,40}))", re.I)
SAID_OF_PRONOUN = re.compile(
    r"^\W*(?:" + CORRECTION_WORDS + r"\b[,.!;:]?\s*){0,2}(?P<pron>she|he|they)(?:'s|s)?\s+"
    r"(?:(?P<not>isnt|isn't|is not|wasnt|wasn't|was not|arent|aren't|are not|doesnt|doesn't|"
    r"does not|didnt|didn't|did not|hasnt|hasn't|has not)\s+(?P<pred>[^.,;!?]{1,40})"
    r"|(?P<verb>is|was|are|were|lives|works|has|got|goes|plays|studies|drives|does|did)\s+"
    r"(?P<pred2>[^.,;!?]{1,40}))", re.I)
BARE_DENIAL = re.compile(
    r"^\W*(?:" + CORRECTION_WORDS + r"\b[,.!;:]?\s*){0,2}(?:my|our)\s+(?P<who>" + RELATION_WORDS
    + r")?(?:'s|s)?\s*(?P<not>isnt|isn't|is not|wasnt|wasn't|was not|arent|aren't|are not|"
    r"doesnt|doesn't|does not|didnt|didn't|did not|hasnt|hasn't|has not)\s*"
    r"(?:either|at all|really|actually|any ?more|no)?\s*[.!]*$", re.I)
BARE_DENIAL_PRONOUN = re.compile(
    r"^\W*(?:" + CORRECTION_WORDS + r"\b[,.!;:]?\s*){0,2}(?:she|he|they)(?:'s|s)?\s*"
    r"(?P<not>isnt|isn't|is not|wasnt|wasn't|was not|arent|aren't|are not|doesnt|doesn't|"
    r"does not|didnt|didn't|did not|hasnt|hasn't|has not)\s*"
    r"(?:either|at all|really|actually|any ?more|no)?\s*[.!]*$", re.I)
A_NUMBER = re.compile(r"^\d+(?:\s*(?:years?|months?)(?:\s+old)?)?$", re.I)
A_NAME = re.compile(r"^(?:called|named)\s+\S+$", re.I)
WITH_AN_ARTICLE = re.compile(r"^(?:a|an)\s+\S+$", re.I)


def _the_shape(verb, pred):
    kind = "said"
    if A_NUMBER.match(pred.strip()):
        kind = "number"
    elif A_NAME.match(pred.strip()):
        kind = "called"
    elif WITH_AN_ARTICLE.match(pred.strip()):
        kind = "a"
    return (verb, kind)


def _the_verb(fact):
    verb = fact.group("verb")
    if verb:
        return verb.lower()
    said = (fact.group("not") or "").lower().replace(" n't", "nt")
    for one, plain in (("is", "is"), ("was", "was"), ("are", "are"), ("does", "does"),
                       ("did", "did"), ("has", "has")):
        if said.startswith(one):
            return plain
    return said


def _the_same_thing(fact, pred, claim):
    return _the_shape(_the_verb(fact), pred) == _the_shape("is", claim)
CLAIM_FILLER = frozenset("a an the some my our your of to in on at called is was are were be".split())
CHECKED_ELSEWHERE = re.compile(r"allerg|\beat|eats|eating|vegan|vegetarian|pescatarian|diet", re.I)


ANIMAL = re.compile(r"\b(?:dog|cat|puppy|kitten|rabbit|hamster|bird|fish|parrot|horse|"
                    r"tortoise|guinea pig|pet)s?\b", re.I)
WHERE_I_LIVE = re.compile(r"^\W*(?:where\s+(?:i|we)\s+(?:live|stay)|where\s+(?:i|we)'?re\s+"
                            r"based|my\s+(?:address|house|home|flat|place)|the\s+place\s+"
                            r"(?:i|we)\s+live)\W*$", re.I)
NOT_MINE = re.compile(r"\bmy\s+(?:mum|mom|dad|father|mother|sister|brother|son|daughter|"
                      r"husband|wife|partner|friend|boss|niece|nephew|aunt|uncle|"
                      r"grandma|grandad|grandmother|grandfather|cousin)\b", re.I)


ALREADY = re.compile(r"\s+(?:already|before|yet|so far|then|earlier)\b.*$", re.I)
ASKS = re.compile(r"^\W*(?:what|why|how|when|where|who|which|whose|did|do|does|is|are|was|"
                  r"were|can|could|should|would|will|have|has|am)\b", re.I)


REMEMBERED = re.compile(
    r"^\W*(?:oh\s+|and\s+|so\s+|but\s+|hey\s+|wait\s+|quick\s+|ok(?:ay)?\s+)?"
    r"remember\s+(?:when\s+|that\s+)?"
    r"(?:(?:i|we)\s+(?:said|say|told\s+you|tell\s+you|mentioned|mention|talked|spoken|spoke|"
    r"chatted|went\s+on|were\s+on)"
    r"|me\s+(?:saying|telling\s+you|mentioning))"
    r"\s*(?:about\s+|of\s+)?(?P<what>[^?]+?)\s*\??$", re.I)
CALLBACK_MISSED = ("I don't have that in this chat's notes — say it again and I'll keep it.",
                   "Nothing about that in what I've kept here — tell me and it's in.",
                   "I've only got this conversation to go on, and that isn't in it yet.")
A_DENIAL = re.compile(r"^\W*(?:i haven't kept a note|there's nothing on|nothing on)", re.I)


CLAIMED_ABOUT = re.compile(
    r"^\W*(?:and\s+|also\s+|so\s+|but\s+|ok(?:ay)?\s+|look\s+|listen\s+|hey\s+)?"
    r"(?:i|we)\s+(?:already\s+|just\s+|definitely\s+|did\s+|have\s+|had\s+)?"
    r"(?:told|tell|mentioned|mention|said|say|talked|talk|spoke)\s+"
    r"(?:you|u)\b\s*(?:(?:about|of|that)\s+)?(?P<what>[^?]+?)\s*[.?!]*$", re.I)
A_CLAIM_WITHOUT_YOU = re.compile(
    r"^\W*(?:and\s+|also\s+|so\s+|but\s+|ok(?:ay)?\s+|look\s+|listen\s+|hey\s+)?"
    r"(?:i|we)\s+(?:already\s+|just\s+|did\s+|have\s+|had\s+)?"
    r"(?:mentioned|mention|talked|talk|spoke)\s+(?:(?:about|of|that)\s+)?"
    r"(?P<what>[^?]+?)\s+(?:earlier|before|already|ages\s+ago|a\s+minute\s+ago|just\s+now|"
    r"last\s+(?:time|week|night))\s*[.?!]*$", re.I)
A_TIME_AGO = re.compile(r"\b(?:earlier|before|already|yesterday|last\s+(?:time|week|night)|"
                        r"ages\s+ago|a\s+minute\s+ago|just\s+now|"
                        r"in\s+the\s+(?:last|previous)\s+(?:chat|conversation))\b", re.I)
A_TRAILING_TIME = re.compile(r"\s+(?:earlier|before|already|yesterday|ages\s+ago|just\s+now|"
                             r"a\s+minute\s+ago|last\s+(?:time|week|night))\s*$", re.I)
REMEMBER_TELLING = re.compile(
    r"^\W*(?:and\s+|also\s+|so\s+|but\s+|ok(?:ay)?\s+|wait\s+|quick\s+)?"
    r"(?:do|did|can|could)\s+(?:you|u)\s+(?:remember|recall)\s+"
    r"(?:(?:that|when|me|i|us|we)\s+){0,2}"
    r"(?:told|telling|tell|talked|talking|talk|mentioned|mentioning|mention|said|saying|say)"
    r"(?:\s+(?:you|u))?\s*(?:about\s+|of\s+)?(?P<what>[^?]+?)\s*\??$", re.I)
A_CLAUSE = re.compile(r"^(?:i|we|im|i'm|ive|i've|id|i'd|he|she|they|you|it)\b\s*\w*", re.I)

_THE_STOP = r"(?:talk|speak|discuss|go\s+into|get\s+into)"
A_BOUNDARY = re.compile(
    r"^\W*(?:and\s+|but\s+|so\s+|ok(?:ay)?\s+|well\s+|look\s+|honestly\s+|"
    r"please\s+|just\s+)*"
    r"(?:(?:i|we)\s+(?:(?:really|just|honestly|actually|kind\s+of|sort\s+of)\s+)*"
    r"(?:don'?t|dont|do\s+not|wouldn'?t|wouldnt|would\s+not|never)\s+"
    r"(?:want|wanna|wish|like)\s+to\s+" + _THE_STOP + r"\s+(?:about|of)\s+"
    r"(?:it|that|this|that\s+one|this\s+one)"
    r"|(?:i|we)(?:'d|\s+would)\s+rather\s+not\s+" + _THE_STOP + r"\s+(?:about|of)?\s*"
    r"(?:it|that|this)?"
    r"|(?:can\s+we|can\s+i|let'?s|lets)\s+(?:not\s+" + _THE_STOP + r"\s+(?:about\s+)?"
    r"(?:it|that|this)|drop\s+(?:it|this\s+one)|leave\s+(?:it|that))"
    r"|(?:leave|drop)\s+(?:it|that|this))\s*(?:please|for\s+now|now|alright|ok|okay|thanks|"
    r"thank\s+you)?\W*$", re.I)
A_CLAIM_BEFORE = re.compile(
    r"^\W*(?:and\s+|but\s+|so\s+|ok(?:ay)?\s+|look\s+|listen\s+|hey\s+)?"
    r"(?:i|we)\s+(?:already\s+|just\s+|did\s+)?(?:told|tell|said|say|mentioned|mention)\s+"
    r"(?:(?:you|u)\b[^,;]*[,;]\s*|(?=i\s|we\s|im\s|i'm\s))", re.I)
LEFT_THERE = (
    "Fair enough - I'll leave that one alone.",
    "Of course. I won't bring it up again.",
    "Alright. That's the last I'll say on it.",
    "No problem - let's leave that one.",
    "Understood. Nothing more on it from me.",
    "That's fair. I'll not raise it again.",
)


A_LEADING_TIME = re.compile(r"^\W*(?:already|before|earlier|just|then|so\s+far)\b[,;:]?\s*", re.I)
A_TIME_ONLY = re.compile(r"^\W*(?:already|before|earlier|that|it|this|you\s+know|"
                         r"you\s+already\s+know|yes|yeah|right)\W*$", re.I)


A_BARE_CLAIM = re.compile(
    r"^\W*(?:and\s+|but\s+|so\s+|ok(?:ay)?\s+|look\s+|listen\s+|hey\s+)?"
    r"(?:i|we)\s+(?:already\s+|just\s+|did\s+)?(?:told|tell|said|say|mentioned|mention)\s+"
    r"(?:you|u)?\s*(?:about\s+)?(?:it|that|this|already|before|earlier|so\s+far|"
    r"you\s+already\s+know)?\W*$", re.I)


def _tells_nothing(text):
    line = str(text or "")
    if A_BARE_CLAIM.match(line):
        return True
    match = CLAIMED_ABOUT.match(line) or A_CLAIM_WITHOUT_YOU.match(line)
    if not match:
        return False
    what = A_TRAILING_TIME.sub("", " ".join(match.group("what").split()))
    what = A_LEADING_TIME.sub("", what).strip(" .,!")
    return not what or bool(A_TIME_ONLY.match(what))


def _handed_back(text, memory):
    mine = " ".join(str(text or "").lower().split())
    lines = []
    turns = memory.get("turns") if isinstance(memory, dict) else None
    for turn in turns if isinstance(turns, list) else []:
        if isinstance(turn, dict) and str(turn.get("user", "")).strip():
            lines.append(" ".join(str(turn["user"]).split()))
    for said in reversed(lines):
        if said.lower() == mine:
            continue
        quoted = _quote(said, memory)
        if not quoted:
            continue
        quoted = quoted[0].lower() + quoted[1:]
        return pick(["So you did - " + quoted,
                     "You're right - " + quoted,
                     "You did - " + quoted,
                     "Fair enough - " + quoted], memory)
    return None


def is_a_boundary(text):
    line = " ".join(str(text or "").split())
    if not line:
        return False
    if A_CLAIM_BEFORE.match(line):
        line = A_CLAIM_BEFORE.sub("", line, count=1)
    return bool(A_BOUNDARY.match(line))


def at_a_boundary(text, memory=None):
    if not is_a_boundary(text):
        return None
    return pick(list(LEFT_THERE), memory)


def _a_boundary_in_a_claim(text):
    return bool(A_CLAIM_BEFORE.match(" ".join(str(text or "").split())))


SOMETHING_ABOUT = re.compile(r"^(?:anything|something|much|any|more|else|stuff)\s+"
                             r"(?:about|on|regarding|to do with)\s+", re.I)


def _the_ask(text):
    line = str(text or "")
    if is_a_boundary(line):
        return None
    match = (TOLD_ABOUT.match(line) or KNOW_ABOUT.match(line)
             or CLAIMED_ABOUT.match(line) or A_CLAIM_WITHOUT_YOU.match(line)
             or REMEMBER_TELLING.match(line))
    if not match:
        return None
    said = A_TRAILING_TIME.sub("", " ".join(match.group("what").split())).strip(" .,!")
    if not said:
        return None
    if ((match.re in (CLAIMED_ABOUT, A_CLAIM_WITHOUT_YOU, REMEMBER_TELLING))
            and said.split()[0].lower() in POINTING):
        return None
    if match.re is TOLD_ABOUT and not match.group("about") and A_STATEMENT.search(said):
        return None
    return said


def ABOUT_THE_CHAT(text, memory=None):
    if _tells_nothing(text):
        return True
    if is_a_boundary(text):
        return True
    said = _the_ask(text)
    if not said:
        return False
    what = re.sub(r"^(?:the|my|our|a|an)\s+", "", said).strip(" .,!")
    what = ALREADY.sub("", what)
    return bool(what) and what.lower() not in POINTING


def answer(text, memory, facts=None, plain=None, claims=None):
    if is_a_boundary(text):
        return at_a_boundary(text, memory)
    if _tells_nothing(text):
        handed = _handed_back(text, memory)
        if handed:
            return handed
    if _a_claim_about_the_chat(text) and not _an_earlier_line(memory, text):
        return None
    checked = check(text, memory)
    if checked:
        return checked
    pointed = _a_claim_that_points(text, memory)
    if pointed:
        return pointed
    said = _the_answer(text, memory, facts, plain, claims)
    if said and A_DENIAL.match(said) and A_CLAUSE.match(_the_ask(text) or ""):
        return pick(list(CALLBACK_MISSED), memory)
    if not said or not SAID_AS_IT_IS.match(said):
        return _with_the_yes(said, text)
    return said


def a_denial(said):
    said = str(said or "")
    return bool(A_DENIAL.match(said) or A_QUOTE.search(said) or SAID_AS_IT_IS.match(said))


SAID_AS_IT_IS = re.compile(r"^(?:yes|no|nothing|you haven't|i haven't|there's nothing|"
                           r"there is nothing|not that i)\b", re.I)
LOWERABLE = frozenset("you your it its they the there that this we he she i".split())


def _lower_first(said):
    said = str(said or "")
    if not said:
        return said
    first = said.split(" ", 1)[0].strip(".,!?\"'—-").lower().split("'")[0]
    if first in LOWERABLE:
        return said[0].lower() + said[1:]
    return said


A_QUOTE = re.compile("[\"\u201c\u201d]")


def _with_the_yes(said, text):
    said = str(said or "")
    if not said or A_QUOTE.search(said) or not TOLD_ABOUT.match(str(text or "")):
        return said
    return "Yes — " + _lower_first(said)


def _the_remembered(text):
    match = REMEMBERED.match(str(text or ""))
    if not match:
        return None
    said = " ".join(match.group("what").split()).strip(" .,!")
    said = ALREADY.sub("", said).strip()
    if not said or said.lower() in POINTING:
        return None
    return said


def A_CALLBACK(text, memory=None):
    return bool(_the_remembered(text))


def a_callback_the_chat_has(text, memory):
    said = _the_remembered(text)
    if not said:
        return False
    what = re.sub(r"^(?:the|my|our|a|an)\s+", "", said).strip(" .,!")
    return bool(_line_about(memory, what or said, skip=text))


def _a_claim_about_the_chat(text):
    said = str(text or "")
    return bool(CLAIMED_ABOUT.match(said) or A_CLAIM_WITHOUT_YOU.match(said))


def _an_earlier_line(memory, text):
    return history.an_earlier_turn(memory, text)


def callback(text, memory, facts=None, plain=None, claims=None):
    said = _the_remembered(text)
    if not said:
        return None
    if is_a_boundary(text):
        return at_a_boundary(text, memory)
    if _a_claim_about_the_chat(text) and not _an_earlier_line(memory, text):
        return None
    recalled = answer("have i told you about " + said, memory, facts, plain, claims)
    if recalled and not A_DENIAL.match(str(recalled)):
        return recalled
    return pick(list(CALLBACK_MISSED), memory)


def _the_answer(text, memory, facts=None, plain=None, claims=None):
    said = _the_ask(text)
    if not said:
        return None
    bare = SOMETHING_ABOUT.sub("", said).strip()
    pointed = _the_proof_they_asked_for(bare, text, memory)
    if pointed:
        return pointed
    noframe = str(text or "")
    know = KNOW_ABOUT.match(noframe) and not NOTHING_NAMED.match(bare)
    if NOTHING_NAMED.match(bare):
        return None
    if know:
        for pattern, plain_ask in IN_QUESTION:
            if re.match(pattern, bare, re.I):
                bare = plain_ask
                break
    if plain and know and bare.lower() not in POINTING:
        kept = plain(bare)
        if kept:
            return kept
    what = re.sub(r"^(?:the|my|our|a|an)\s+", "", bare).strip(" .,!")
    what = ALREADY.sub("", what).strip()
    if not what or what.lower() in POINTING:
        return None
    known = user(memory)
    theirs = _about_a_person(memory, what)
    if theirs is not None:
        return theirs
    someone = _the_person_a_pronoun_points_at(memory, what)
    if someone:
        return _about_a_person(memory, someone)
    pet = _about_a_pet(memory, what, known, facts)
    if pet:
        return pet
    if WHERE_I_LIVE.match(what):
        said = ((facts or {}).get("places") or (lambda memory: ""))(memory)
        if said:
            return said
    if _names_only_a_kind(what):
        kept = _the_fact_of_that_kind(memory, what, known, facts)
        if kept:
            return kept
    kind_words = _the_words_of_the_kind(what)
    if kind_words:
        quoted = _line_about(memory, " ".join(sorted(kind_words)), whole_words=True, skip=text)
        if quoted:
            return _quote(quoted, memory)
    kept = _the_fact_of_that_kind(memory, what, known, facts)
    if kept:
        return kept
    named = _the_fact_that_names(memory, what, known, facts)
    if named:
        return named
    quoted = _line_about(memory, what, skip=text)
    if quoted:
        return _quote(quoted, memory)
    if know and claims is not None and not claims():
        return None
    dated = _the_property_of_the_thing(memory, bare, facts)
    if dated:
        return dated
    return _no_note(_yours(bare), memory)


A_DATE_PROPERTY = frozenset(("when", "what day", "what date", "what time", "which day",
                             "the day", "the date", "the time"))
A_PLACE_PROPERTY = frozenset(("where", "what place", "which place", "the place"))


def _the_property_of_the_thing(memory, what, facts):
    asked = " ".join(str(what or "").lower().split()).strip(" .,!?")
    if asked in A_DATE_PROPERTY:
        from .when import when_answer
        return when_answer("when is it", memory) or None
    if asked in A_PLACE_PROPERTY:
        said = ((facts or {}).get("places") or (lambda memory: ""))(memory)
        return said or None
    return None


def _a_clause_is_named(line):
    found = CLAIMED_ABOUT.match(str(line or "")) or A_CLAIM_WITHOUT_YOU.match(str(line or ""))
    if not found:
        return False
    return bool(A_CLAUSE.match(" ".join(str(found.group("what") or "").split())))


def _the_thing_the_chat_is_on(memory):
    from .store_replies import _the_thing_the_chat_is_on as about
    return about(memory) or ""


def _no_note(thing, memory):
    if _the_thing_is_a_clause(thing):
        return pick(["Nothing in my notes says \u201c" + thing + "\u201d yet — tell me and "
                     "I'll keep it.",
                     "I don't have \u201c" + thing + "\u201d in my notes — say it and I'll "
                     "hold on to it.",
                     "\u201c" + thing + "\u201d isn't in what I keep yet — tell me and I'll "
                     "remember it."],
                    memory)
    return pick(["I haven't kept a note of " + thing + " — tell me and I'll remember it.",
                 "There's nothing on " + thing + " in what I keep — say it and I'll hold "
                 "on to it.",
                 "Nothing on " + thing + " in my notes yet — tell me and I'll keep it."],
                memory)


A_CLAUSE_OPENING = re.compile(
    r"^(?:i|we|he|she|they|it|you|there|my|our)\b|\b(?:was|were|am|is|are|had|have|has|"
    r"did|do|does|will|would|can|could|should)\b", re.I)


def _the_thing_is_a_clause(thing):
    words = str(thing or "").split()
    if not words:
        return False
    if len(words) > 3:
        return True
    return bool(A_CLAUSE_OPENING.search(" ".join(words)))


REPORTED = re.compile(r"^\s*(?:and\s+|also\s+)?(?:i|we)\s+(?:did\s+)?(?:say|said|told\s+you|"
                      r"mentioned|was\s+saying|were\s+saying)\b[:,]?\s+(?P<clause>(?!about\b|of\b)"
                      r".+)$", re.I)


TELLING_ALREADY = re.compile(r"^you (?:told me|said to me|mentioned to me)\b")


def _quote(line, memory):
    reported = REPORTED.match(str(line or ""))
    if reported:
        line = reported.group("clause")
    opened = re.sub(r"\bi\s*m\b", "i'm", str(line or ""), flags=re.I)
    opened = re.sub(r"\bi\s*ve\b", "i've", opened, flags=re.I)
    said = say_it_back(opened).strip().rstrip(".")
    if not said:
        return pick(["You told me that already", "You did say that"], memory)
    said = said[0].lower() + said[1:]
    said += "."
    if TELLING_ALREADY.match(said):
        return said[0].upper() + said[1:]
    return pick(["You said " + said,
                 "You told me " + said,
                 "You did say " + said], memory)


def _the_words_of_the_kind(what):
    kinds = set()
    for word in re.split(r"[\s,]+", str(what or "").lower()):
        kind = _the_kind_of(word)
        if not kind:
            return set()
        kinds.add(kind)
    if len(kinds) != 1:
        return set()
    kind = kinds.pop()
    return {word for word, key in A_KIND.items() if key == kind}


MINE = re.compile(r"\b(my|our|me|mine|ours)\b", re.I)
YOURS = {"my": "your", "our": "your", "me": "you", "mine": "yours", "ours": "yours"}


A_VERB_IN_A_CLAUSE = re.compile(
    r"\b(?:was|were|am|is|are|had|have|has|did|do|does|will|would|can|could|should|going)\b",
    re.I)


def _yours(phrase):
    said = str(phrase or "")
    if A_VERB_IN_A_CLAUSE.search(said):
        return said
    return MINE.sub(lambda found: YOURS.get(found.group(1).lower(), found.group(1)), said)


def _the_person_a_pronoun_points_at(memory, what):
    word = str(what or "").strip().lower().rstrip(".,!?")
    if word not in ("her", "him", "them", "they"):
        return ""
    entry = None
    for kept in reversed(others(memory)):
        if isinstance(kept, dict) and kept.get("who"):
            entry = kept
            break
    if entry:
        return str(entry["who"]).lower().rstrip("s")
    for turn in reversed(memory.get("turns") or []):
        said = turn.get("user") if isinstance(turn, dict) else None
        if not isinstance(said, str):
            continue
        for other in re.findall(r"[a-z]+", said.lower()):
            if other.rstrip("s") in extract.RELATIONS:
                return other.rstrip("s")
    return ""


def _words_of(said):
    return {word for word in re.findall(r"[a-z0-9']+", str(said or "").lower())
            if word not in CLAIM_FILLER and len(word) > 1 or word.isdigit()}


def check(text, memory):
    found = CHECK_OF_SOMEONE.match(str(text or ""))
    if not found:
        return None
    claim = found.group("claim")
    if CHECKED_ELSEWHERE.search(claim):
        return None
    asked = _words_of(claim)
    if not asked:
        return None
    who = found.group(0).lower()
    who = next((word for word in re.findall(r"[a-z]+", who)
                if word in extract.RELATIONS), "")
    if not who:
        return None
    newer = None
    newer_said = ""
    taken_back = False
    for said in reversed(_their_lines(memory, who)):
        fact = SAID_OF_SOMEONE.match(said)
        by_pronoun = False
        if not fact:
            bare = BARE_DENIAL_PRONOUN.match(said) or BARE_DENIAL.match(said)
            if bare is not None:
                named = (bare.groupdict().get("who") or "").strip().lower().rstrip("s")
                if not named or named == who:
                    taken_back = True
                continue
            fact = SAID_OF_PRONOUN.match(said)
            by_pronoun = bool(fact)
        if not fact:
            continue
        pred = fact.group("pred") or fact.group("pred2") or ""
        if not asked <= _words_of(pred):
            if newer is None and _the_same_thing(fact, pred, claim):
                newer = " ".join(pred.split())
                newer_said = said
            continue
        if newer is not None and newer != " ".join(pred.split()):
            return ("You've told me your " + who + " is " + newer + ", and before that "
                    + " ".join(pred.split()) + ". Which is right?")
        denial = bool(fact.group("not")) != taken_back
        if by_pronoun:
            said_back = _names_in_capitals(_plain_contractions(
                "your " + who + " " + (fact.group("not") or fact.group("verb") or "")
                + " " + pred).strip())
        elif taken_back:
            said_back = _the_denial(who, _the_verb(fact), pred)
        else:
            said_back = _names_in_capitals(_plain_contractions(
                _your_own_clause(said).strip(" .,!")))
        if not said_back:
            continue
        opening = "No — " if denial != _claim_is_a_denial(claim) else "Yes — "
        return opening + said_back[0].lower() + said_back[1:] + "."
    if newer and newer_said and _the_shape("is", newer)[1] != "said":
        said_back = _names_in_capitals(_plain_contractions(
            _your_own_clause(newer_said).strip(" .,!")))
        if said_back:
            return said_back[0].upper() + said_back[1:] + "."
    return None


A_CLAUSE_OF_MINE = re.compile(r"^(my|our)\b", re.I)


def _your_own_clause(said):
    line = CORRECTING.sub("", str(said or "").strip())
    found = A_CLAUSE_OF_MINE.match(line)
    if not found:
        return line
    return YOURS.get(found.group(1).lower(), "your") + line[found.end():]


CONTRACTIONS = {("isnt",): "isn't", ("wasnt",): "wasn't", ("doesnt",): "doesn't",
                ("didnt",): "didn't", ("hasnt",): "hasn't", ("arent",): "aren't",
                ("dont",): "don't", ("cant",): "can't", ("wont",): "won't",
                ("is", "n't"): "isn't"}


def _plain_contractions(said):
    for words, joined in CONTRACTIONS.items():
        said = re.sub(r"\b" + r"\s+".join(words) + r"\b", joined, said, flags=re.I)
    return said


CALLED_NAME = re.compile(r"\b(?:called|named)\s+([a-z][a-z'\-]*)")


def _names_in_capitals(said):
    return CALLED_NAME.sub(lambda found: "called " + found.group(1)[:1].upper()
                           + found.group(1)[1:], said)


A_DENIAL = re.compile(r"^\W*(?:not\b|n't\b)", re.I)


def _claim_is_a_denial(claim):
    return bool(A_DENIAL.match(str(claim or "")))


def _their_lines(memory, who):
    lines = []
    for turn in memory.get("turns") or []:
        said = turn.get("user") if isinstance(turn, dict) else None
        if not isinstance(said, str):
            continue
        if re.search(r"\b" + re.escape(who) + r"s?\b", said.lower()):
            lines.append(_trim(said, limit=80))
        elif lines and _a_pronoun_for(who).search(said):
            lines.append(_trim(said, limit=80))
    kept = user(memory).get("person")
    if isinstance(kept, dict) and isinstance(kept.get("said"), str):
        lines.append(_trim(kept["said"], limit=80))
    return lines


def _about_a_person(memory, what):
    words = [word.strip(".,!?") for word in what.split()]
    for word in words:
        who = word.lower().rstrip("s")
        if who not in extract.RELATIONS:
            continue
        for entry in others(memory):
            if str(entry.get("who") or "").lower().rstrip("s") != who:
                continue
            fact = _their_fact(who, entry)
            if fact:
                return fact
        quoted = _line_about(memory, who, whole_words=True)
        if quoted:
            return _quote(quoted, memory)
        return _no_note("your " + who, memory)
    return None


def _their_fact(who, entry):
    if entry.get("allergies"):
        allergies = entry["allergies"]
        if not isinstance(allergies, (list, tuple)):
            allergies = [allergies]
        return "You said your " + who + " is allergic to " + ", ".join(
            str(item) for item in allergies) + "."
    if entry.get("diet"):
        return "You said your " + who + " is " + str(entry["diet"]) + "."
    if entry.get("no_meat"):
        return "You said your " + who + " doesn't eat meat."
    if entry.get("name"):
        name = " ".join(word[:1].upper() + word[1:] for word in str(entry["name"]).split())
        return "Your " + who + " is called " + name + "."
    if entry.get("condition"):
        return "You said your " + who + " has " + str(entry["condition"]) + "."
    return ""


def _about_a_pet(memory, what, known, facts=None):
    if NOT_MINE.search(what + " "):
        return None
    kind = ANIMAL.search(what)
    family = (facts or {}).get("family") or (lambda word: word)
    if kind:
        name = family(kind.group(0).lower().rstrip("s"))
    else:
        breed = breed_words.BREED_RE.search(what)
        name = breed_words.BREED_KIND.get(
            breed_words.the_breed_named(breed.group(0)), "") if breed else ""
        if not name:
            return None
    pets = [pet for pet in (known.get("pets") or []) if isinstance(pet, dict)]
    if not pets:
        return None
    if name in ("pet", "animal"):
        return _the_pets(memory, pets, facts)
    mine = [pet for pet in pets
            if family(str(pet.get("animal") or "").lower().rstrip("s")) == name]
    if not mine:
        return _no_note("a " + name, memory)
    said = ((facts or {}).get("pets") or (lambda memory, animal: ""))(memory, name)
    if said and any(pet.get("name") for pet in mine):
        return said
    pet = mine[-1]
    animal = str(pet.get("animal") or name)
    if pet.get("coming"):
        return "You're getting " + _many(pet) + "."
    return "You've got " + _many(pet) + "."


def _the_pets(memory, pets, facts=None):
    here = [pet for pet in pets if not pet.get("coming")]
    coming = [pet for pet in pets if pet.get("coming")]
    said = _the_pets_here(memory, here, facts)
    owed = _the_pets_here(memory, coming, facts)
    if owed:
        owed = owed.replace("You've got ", "You're getting ", 1)
    parts = [one for one in (said, owed) if one]
    return " ".join(parts) or None


def _the_pets_here(memory, pets, facts=None):
    family = (facts or {}).get("family") or (lambda word: word)
    kinds = []
    for pet in pets:
        animal = family(str(pet.get("animal") or "").lower().rstrip("s"))
        if animal and animal not in kinds:
            kinds.append(animal)
    if len(kinds) == 1:
        said = ((facts or {}).get("pets") or (lambda memory, animal: ""))(memory, kinds[0])
        if said:
            return said
    said = [_many([pet for pet in pets if str(pet.get("animal") or "").lower().rstrip("s")
                   in (kind, kind + "s")][-1]) for kind in kinds]
    said = [one for one in said if one]
    if not said:
        return None
    if len(said) == 1:
        return "You've got " + said[0] + "."
    return "You've got " + ", ".join(said[:-1]) + " and " + said[-1] + "."


COUNT_WORDS = {2: "two", 3: "three", 4: "four", 5: "five", 6: "six", 7: "seven", 8: "eight",
               9: "nine", 10: "ten"}


def _a(word):
    return ("an " if str(word)[:1].lower() in "aeiou" else "a ") + str(word)


def _many(pet):
    kind = str(pet.get("animal") or "pet")
    animal = kind if pet.get("breed_of_one") else str(pet.get("breed") or kind)
    many = kind if kind.endswith(("fish", "sheep", "deer")) else kind + "s"
    if pet.get("name"):
        name = str(pet["name"])
        return _a(animal) + " called " + name[:1].upper() + name[1:]
    try:
        count = int(pet.get("count") or 1)
    except (TypeError, ValueError):
        count = 1
    if count > 1:
        return COUNT_WORDS.get(count, str(count)) + " " + many
    return _a(animal)


ONLY_A_POINTING_TIME = re.compile(r"^\W*(?:already|before|earlier|yesterday|that|this|it|them|"
                                  r"just\s+now|ages\s+ago|a\s+minute\s+ago|"
                                  r"the\s+other\s+day|last\s+(?:time|night|week))\W*$", re.I)


POINTING_TAIL = re.compile(r"\s+(?:already|before|earlier|just\s+now|ages\s+ago|"
                            r"a\s+minute\s+ago|the\s+other\s+day|last\s+time)\W*$", re.I)


POINTING_SAID = re.compile(
    r"^\W*(?:and\s+|also\s+|so\s+|but\s+|ok(?:ay)?\s+|look\s+|listen\s+|hey\s+)?"
    r"(?:i|we)\s+(?:said|told\s+you|told\s+u)\s+(?:that|it|this|them)\s+"
    r"(?:already|before|earlier|just\s+now|ages\s+ago|a\s+minute\s+ago|the\s+other\s+day|"
    r"last\s+(?:time|week|night))\W*$", re.I)


def _the_newest_stated_line(memory, skip="", a_question_ok=False):
    asked = _flat(skip)
    for turn in reversed(memory.get("turns") or []):
        said = turn.get("user") if isinstance(turn, dict) else None
        if not isinstance(said, str) or not said.strip():
            continue
        if _flat(said) == asked:
            continue
        if not a_question_ok and (said.rstrip().endswith("?") or ASKS.match(said)):
            continue
        if _a_claim_about_the_chat(said):
            continue
        return " ".join(said.split())
    return ""


def _a_claim_that_points(text, memory):
    line = str(text or "")
    if POINTING_SAID.match(line):
        return _the_proof_they_asked_for("", text, memory)
    match = CLAIMED_ABOUT.match(line) or A_CLAIM_WITHOUT_YOU.match(line)
    if not match:
        return None
    said = A_TRAILING_TIME.sub("", " ".join(match.group("what").split())).strip(" .,!")
    if said and said.lower() not in POINTING:
        return None
    return _the_proof_they_asked_for(said, text, memory)


def _the_proof_they_asked_for(named, text, memory):
    said = " ".join(str(named or "").split())
    if said and not ONLY_A_POINTING_TIME.match(POINTING_TAIL.sub("", said).strip()):
        return None
    told_about = _the_thing_the_chat_is_on(memory)
    quoted = _line_about(memory, told_about, skip=text) if told_about else ""
    if not quoted:
        quoted = _the_newest_stated_line(memory, skip=text)
    if not quoted:
        asked_line = _the_newest_stated_line(memory, skip=text, a_question_ok=True)
        if not asked_line:
            return None
        return pick(['All I have from you so far is "' + asked_line + '" — tell me the rest and '
                     "I'll keep it.",
                     'What I have is "' + asked_line + '". Say it in your own words and it is in.'],
                    memory)
    return pick(['You did — "' + quoted + '" is what I kept.',
                 '"' + quoted + '" — that one I have.',
                 'I have it: "' + quoted + '".'], memory)


def _line_about(memory, what, whole_words=False, skip=""):
    words = [word for word in re.split(r"[\s,]+", what.lower()) if len(word) > 2]
    if not words:
        return ""
    asked = _flat(skip)
    for turn in reversed(memory.get("turns") or []):
        said = turn.get("user") if isinstance(turn, dict) else None
        if not isinstance(said, str) or not said.strip():
            continue
        if _flat(said) == asked:
            continue
        if said.rstrip().endswith("?") or ASKS.match(said):
            continue
        if _a_claim_about_the_chat(said) and not _a_clause_is_named(said):
            continue
        if recall.ask(said) == "me":
            continue
        if TOLD_ABOUT.match(said) or CLAIMS_TOLD.search(said) or REMEMBERED.match(said):
            continue
        low = said.lower()
        if whole_words:
            if any(re.search(r"\b" + re.escape(word) + r"s?\b", low) for word in words):
                return _trim(said)
        elif any(word in low for word in words):
            return _trim(said)
    return ""


A_TRIP = re.compile(r"\b(?:went|going|booked|flying|flight|holiday|trip|visiting|staying|"
                    r"travel(?:ling|ing)?)\b", re.I)


def _a_trip_line(memory):
    for turn in reversed(memory.get("turns") or []):
        said = turn.get("user") if isinstance(turn, dict) else None
        if not isinstance(said, str) or not said.strip() or said.rstrip().endswith("?"):
            continue
        if A_TRIP.search(said):
            return _trim(said)
    return ""


CLAIMS_TOLD = re.compile(r"\b(?:told|mentioned|said|talked)\s+(?:you|about|it)\b", re.I)


def _flat(line):
    return " ".join(str(line or "").lower().split()).strip(" .,!")


def _the_denial(who, verb, pred):
    word = {"is": "isn't", "was": "wasn't", "are": "aren't", "does": "doesn't",
            "did": "didn't", "has": "hasn't"}.get(verb, "isn't")
    return "your " + who + " " + word + " " + " ".join(str(pred or "").split())


def _a_pronoun_for(who):
    word = str(who or "").strip().lower()
    fits = ["they"]
    if word in extract.SHE:
        fits.append("she")
    if word in extract.HE:
        fits.append("he")
    return re.compile(r"^\W*(?:" + CORRECTION_WORDS + r"\b[,.!;:]?\s*){0,2}(?:"
                      + "|".join(fits) + r")(?:'s|s)?\s+\S", re.I)


def _trim(line, limit=100):
    text = " ".join(str(line or "").split()).strip(" .,!")
    if len(text) > limit:
        cut = text[:limit].rsplit(" ", 1)[0]
        text = cut + "\u2026"
    return text


NOTHING_SAID = re.compile(r"^\W*(?:you\s+(?:haven't|have not|don't|do not|'ve not|ve not|didn't)|"
                          r"nothing|no\b|not\b)", re.I)
THE_KINDS_KEPT = ("allergies", "budget", "diet", "dislikes", "tastes", "plan", "places",
                  "kids")


def _stem(word):
    word = re.sub(r"[^a-z]", "", str(word or "").lower())
    for _ in range(3):
        for ending in ("ings", "ing", "ies", "es", "ed", "s", "e", "y"):
            if len(word) > len(ending) + 2 and word.endswith(ending):
                word = word[:-len(ending)]
                break
        else:
            break
    return word


def _kept_words(value, into=None):
    into = set() if into is None else into
    if isinstance(value, str):
        into.update(word for word in re.split(r"[^a-z]+", value.lower()) if word)
    elif isinstance(value, dict):
        for item in value.values():
            _kept_words(item, into)
    elif isinstance(value, (list, tuple, set)):
        for item in value:
            _kept_words(item, into)
    return into


def _the_fact_that_names(memory, what, known, facts):
    if not facts:
        return None
    stems = {_stem(word) for word in re.split(r"[^a-zA-Z]+", str(what or "")) if len(word) > 2}
    stems.discard("")
    if not stems:
        return None
    for key in THE_KINDS_KEPT:
        reader = facts.get(key)
        value = known.get(key)
        if not reader or not value:
            continue
        kept = {_stem(word) for word in _kept_words(value)}
        if not (stems & kept):
            continue
        said = reader(memory)
        if said and not NOTHING_SAID.match(said):
            return said
    return None


def _the_kind_of(word):
    word = str(word or "").strip(".,!?").lower()
    for candidate in (word, word[:-1], word[:-2] if word.endswith("es") else word):
        key = A_KIND.get(candidate)
        if key:
            return key
    return ""


def _names_only_a_kind(what):
    words = [word.strip(".,!?") for word in re.split(r"[\s,]+", str(what or "").lower()) if word]
    return bool(words) and all(_the_kind_of(word) for word in words)


def _the_fact_of_that_kind(memory, what, known, facts=None):
    for word in re.split(r"[\s,]+", what.lower()):
        key = _the_kind_of(word)
        if not key:
            continue
        value = known.get(key)
        if not value:
            if key == "plan":
                for place in reversed([p for p in (known.get("places") or [])
                                       if isinstance(p, str)]):
                    said = _line_about(memory, place)
                    if said:
                        return _quote(said, memory)
                said = _a_trip_line(memory)
                if said:
                    return _quote(said, memory)
            return ""
        said = ((facts or {}).get(key) or (lambda memory: ""))(memory)
        if said:
            return said
        if key == "plan":
            return "You said: \"" + _trim(value) + "\""
        values = value if isinstance(value, list) else [value]
        return "You told me: " + ", ".join(str(v) for v in values) + "."
    return ""
