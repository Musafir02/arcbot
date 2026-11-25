import re

from ..compose import pick
from ..compose.whole import a_whole_cut
from ..memory import topics
from . import named, repeat

OPTION_WORDS = frozenset("""
    else other others another alternative alternatives different ideas idea options option
    suggestion suggestions way ways thing things approach approaches trick tricks tip tips
    works work working help helps helping useful
""".split())

CONTINUATION_WORDS = frozenset("""
    go goes going on carry carries keep keeps continue continuing next more further then again
    deeper say telling
""".split())

SWAP_WORDS = frozenset("""
    swap swaps swapping swapped substitute substitutes substitution substituting
    replacement replacements replace replacing stand-in
""".split())

ASK = repeat.ASK | repeat.FILLER | OPTION_WORDS | CONTINUATION_WORDS | SWAP_WORDS

THE_MISSING_PART = frozenset("""
    include includes including included bring bringing add adding say saying mention mentioning
    cover covers covering know wear take expect prepare check forget forgetting forgot missed
    miss left put
""".split())
A_MISSING_PART = re.compile(
    r"\b(?:anything|what|which|is there|are there|something|all)\b[^.?!]{0,40}?\b"
    r"(?:include|includes|including|bring|bringing|add|adding|say|saying|mention|mentioning|"
    r"cover|covering|know|wear|take|expect|prepare|check|forget|forgetting|forgot|missed|"
    r"miss|left|put)\b", re.I)
SOFT_FILLER = frozenset("""
    defo deffo definitely probs prob probably tbh honestly basically totally literally
""".split())
ASK = ASK | THE_MISSING_PART | SOFT_FILLER

OTHER_OPTION = re.compile(
    r"\b(?:what|anything|any|something|is there|are there|got any|have you got|"
    r"else|other|others|another|different|alternative|alternatives)\b",
    re.I)
AN_OPTION = re.compile(
    r"\b(?:else|other|others|another|different|alternative|alternatives|"
    r"ideas?|options?|suggestions?|ways?|things?|approaches?|"
    r"swaps?|substitutes?|substitutions?|replacements?)\b", re.I)
CARRY_ON = re.compile(
    r"^(?:(?:go|carry)\s+on|keep\s+going|continue|and(?:\s+(?:then|after\s+that|on))?|"
    r"then\s+what|after\s+that|whats?(?:'s|\s+is)?\s+next|next|more|"
    r"tell\s+me\s+more|say\s+more|go\s+deeper|and\s+what\s+else)\b", re.I)
LEAD_IN = re.compile(
    r"^(?:ok(?:ay)?|right|so|yeah|yes|alright|well|please|ta|thanks|cheers|and)[\s,]+", re.I)

ANSWER_MODULES = ("answers", "chat", "knowledge")

HEDGE = repeat.HEDGE
STOCK = re.compile(
    r"\b(?:thanks for telling me|tell me more|say more if it helps|i'?m listening|"
    r"what would be most useful|anything you'?d like a hand with|noted)\b", re.I)

SENTENCE = re.compile(r"(?<=[.!?])\s+")
QUOTE_MARKS = "\"\u201c\u201d"
FRAME = re.compile(
    r"^(?:from just now|same as before|as i said|like i said|same answer|same answer i'?m afraid|"
    r"it'?s what i said a moment ago|you'?ve got it|that'?s the one)\s*[:\-]\s*", re.I)

LEADS = (
    "Of that, the bit that matters most: {rest}",
    "If you only do one thing from that answer: {rest}",
    "The part of that I would act on first: {rest}",
    "Of all of that, this is the bit I would not skip: {rest}",
    "The bit of that answer worth doing first: {rest}",
)

DO_THIS = re.compile(
    r"\b(?:if|so|then|try|use|keep|check|give|take|put|get|add|buy|swap|replace|clean|wash|"
    r"rinse|leave|stand|wrap|store|feed|water|encourage|bleed|call|ask|book|avoid|stop|start|"
    r"turn|run|set|hold|move|cover|cut|open|close|repeat|ring|email|text|worth|helps?|"
    r"worthwhile)\b", re.I)

A_COMMENT = re.compile(
    r"^\s*(?:it'?s|it is|it was|that'?s|that is|that was|this is|this was|there'?s nothing|"
    r"nothing|none of|both|all of)\b", re.I)

OFFERS_ANOTHER = re.compile(
    r"^\s*(?:something else|anything else|another (?:option|one|idea|way|thing|idea for)"
    r"|an? alternative|alternatively|otherwise|instead"
    r"|or (?:else )?(?:try|make|use|have|just|simply|do|go with)"
    r"|you could also|you can also|also try|you might also"
    r"|there(?:'s| is| are)\b"
    r"(?![^.]{0,70}\b(?:charge|fee|fees|cost|costs|price|deposit|catch|risk|downside|caveat|"
    r"trick|trouble|problem)\b)[^.]{0,70}\b(?:as well|too)\b)\b", re.I)

LENGTH_IDIOM = re.compile(r"\b(?:from\s+)?start\s+to\s+finish\b", re.I)


ABOUT_ANOTHER = re.compile(
    r"^(?!\s*(?:if|when|once|after|before|while|then|so|but|and|or|try|check|keep|give|take|"
    r"put|use|get|add|buy|swap|replace|clean|wash|rinse|leave|stand|wrap|store|feed|call|ask|"
    r"book|avoid|stop|start|turn|run|set|hold|move|cover|cut|open|close|repeat|ring|email|text|"
    r"pick|pinch|encourage|bleed)\b)\w+(?: [\w'\u2019()-]+){0,3} "
    r"(?:hates?|likes?|loves?|prefers?|needs?|wants?|is|are)\b", re.I)

A_PERSON = re.compile(
    r"\b(?:my|our|the)\s+(?:son|daughter|kids?|child|children|toddler|baby|boy|girl|mum|mom|"
    r"mother|dad|father|wife|husband|partner|boyfriend|girlfriend|brother|sister|friend|cat|"
    r"dog|puppy|kitten|rabbit|hamster|horse|nan|nana|granny|grandma|grandad|grandpa)\b", re.I)
THEM = frozenset("""
    he she him his her hers they them their themselves toddler baby boy girl son daughter kid
    kids child children cat dog puppy kitten rabbit hamster horse
""".split())

FILING = re.compile(
    r"^\s*(?:got it|noted|right|okay|fair enough|thanks|that'?s noted|i'?ll remember|"
    r"understood|sure)\b", re.I)

RULED_OUT = re.compile(
    r"\b(?:don'?t|do not|doesn'?t|didn'?t|can'?t|couldn'?t|won'?t|wouldn'?t|never)\s+"
    r"(?:really\s+|actually\s+)?(?:like|love|want|need|use|eat|drink|fancy|trust|stand|"
    r"have|bother with|go to)\b|"
    r"\b(?:hates?|hated|avoid|avoids|allergic to|not a fan of|sick of|tired of|gave up|"
    r"given up|stopped|quit|no time for|can'?t afford|too expensive|won'?t do)\b", re.I)

NOT_A_THING = topics.STOPWORDS | repeat.ASK | repeat.FILLER | frozenset("""
    dont do does doesnt didnt cant wont wouldnt never not anymore either too also any more
    actually really just very much such thing things stuff one ones going again
""".split())

A_CONDITION = re.compile(
    r"\b(?:what\s+)?if\b|\bunless\b|\bsuppose\b|\bin\s+case\b|\bwhat\s+happens\s+(?:if|when)\b",
    re.I)

LOOK_BACK = 3
MOST = 220
LEAST = 25


def names_nothing(text):
    said = str(text or "")
    asks_for_more = bool(CARRY_ON.match(said.strip())
                         or CARRY_ON.match(LEAD_IN.sub("", said.strip()))) or (
        bool(OTHER_OPTION.search(said)) and bool(AN_OPTION.search(said))) or bool(
        A_MISSING_PART.search(said))
    if not asks_for_more:
        return False
    if repeat.ABOUT_THE_BOT.search(said):
        return False
    if A_CONDITION.search(said):
        return False
    words = topics.words(said)
    left = [w for w in words if w not in ASK and w not in topics.STOPWORDS and not w.isdigit()]
    return bool(words) and not left


def ruled_out_words(text):
    if not RULED_OUT.search(text or ""):
        return set()
    return {word.rstrip("s") for word in topics.words(text)
            if len(word) > 2 and word not in NOT_A_THING and not word.isdigit()}


def _names_one(part, ruled_out):
    if not ruled_out:
        return False
    return bool(ruled_out & {word.rstrip("s") for word in topics.words(part)})


def _the_turn_to_lean_on(turns, memory=None):
    memory = memory or {}
    ruled_out = set()
    for back in range(1, LOOK_BACK + 1):
        if len(turns) < back:
            break
        turn = turns[-back]
        said = str(turn.get("bot") or "").strip()
        if said and not FILING.match(said) and not repeat.a_hand_back(said, memory):
            ruled_out |= ruled_out_words(str(turn.get("user") or ""))
            return turn, ruled_out, len(turns) - back
        ruled_out |= ruled_out_words(str(turn.get("user") or ""))
    return None, ruled_out, None


def split_sentences(said):
    said = str(said or "").strip()
    parts, start, opened, ended = [], 0, False, False
    for at, char in enumerate(said):
        if char in QUOTE_MARKS:
            if opened:
                opened = False
                if ended and at + 1 < len(said) and said[at + 1].isspace():
                    parts.append(said[start:at + 1])
                    start = at + 1
                ended = False
            else:
                opened = True
        elif char in ".!?":
            if opened:
                ended = True
                continue
            after = at + 1
            while after < len(said) and said[after] in QUOTE_MARKS:
                after += 1
            if after >= len(said) or said[after].isspace():
                parts.append(said[start:after])
                start = after
    parts.append(said[start:])
    return [part.strip() for part in parts if part.strip()]


def _sentences(said):
    said = str(said or "").strip()
    said = FRAME.sub("", said)
    return split_sentences(said)


def _said_before(memory, said, before=None):
    wanted = said.strip()[:50].lower()
    if not wanted:
        return False
    turns = [t for t in (memory.get("turns") or []) if isinstance(t, dict)]
    if before is None:
        before = len(turns) - 1
    for turn in turns[max(0, before - LOOK_BACK + 1):before]:
        if not isinstance(turn, dict):
            continue
        if wanted in str(turn.get("bot") or "").lower():
            return True
    return False


def _cut(said):
    said = said.strip()
    if len(said) <= MOST:
        return said
    return a_whole_cut(said, MOST).rstrip(" ,;:.") + "."

A_PROFESSIONAL = re.compile(
    r"\b(?:see|speak to|talk to|ring|call|contact|ask|visit|book in with)\s+(?:a|an|your|the)\s+"
    r"(?:gp|doctor|nurse|practice nurse|pharmacist|chemist|midwife|health visitor|"
    r"physio(?:therapist)?|dentist|optician|consultant|specialist)\b", re.I)
FRAME_WORDS = re.compile(
    r"\b(?:if|when|whenever|unless|once|should|in case|and|so|then|but|or|also|really|actually|"
    r"still|again|too|either|instead)\b", re.I)
URGENT_LINE = re.compile(r"\b(?:ring|call|phone)\s+(?:111|999|911|112|nhs 24)\b", re.I)


def _a_caveat_about_getting_help(part):
    if topics.RED_FLAG.match(part):
        return True
    if not (A_PROFESSIONAL.search(part) or URGENT_LINE.search(part)):
        return False
    left = A_PROFESSIONAL.sub(" ", URGENT_LINE.sub(" ", part))
    left = FRAME_WORDS.sub(" ", left)
    return not is_a_step(left)


def is_a_step(part):
    return bool(DO_THIS.search(LENGTH_IDIOM.sub(" ", part)))


def _the_rest(said, memory, ruled_out=(), at=None):
    parts = _sentences(said)
    if len(parts) < 2:
        return ""
    given = None
    for at, part in enumerate(parts):
        if is_a_step(part) and not _a_caveat_about_getting_help(part):
            given = at
            break
    if given is None:
        return ""
    def _is_the_rest(part, before):
        offers = bool(OFFERS_ANOTHER.match(part))
        return not (len(part) < LEAST or _a_caveat_about_getting_help(part)
                    or (not is_a_step(part) and not offers)
                    or A_COMMENT.match(part)
                    or (ABOUT_ANOTHER.match(part) and not offers)
                    or _names_one(part, ruled_out) or _said_before(memory, part, before))

    for here in range(given + 1, len(parts)):
        part = parts[here]
        if not _is_the_rest(part, at):
            continue
        if part[-1] in QUOTE_MARKS:
            for after in range(here + 1, len(parts)):
                if _is_the_rest(parts[after], at):
                    part = part + " " + parts[after]
                    break
        if OFFERS_ANOTHER.match(part) and len(part) <= MOST:
            return part[:1].upper() + part[1:]
        return _cut(part)
    return ""


def other_option(text, memory):
    if not names_nothing(text):
        return None
    if named.asks_a_part_of_the_trip(text, memory):
        return None
    turns = [t for t in (memory.get("turns") or []) if isinstance(t, dict)]
    if not turns:
        return None
    turn, ruled_out, at = _the_turn_to_lean_on(turns, memory)
    if turn is None:
        return None
    said = str(turn.get("bot") or "").strip()
    module = str(turn.get("module") or "")
    if module not in ANSWER_MODULES and not said:
        return None
    if not said or said.rstrip().endswith("?") or HEDGE.search(said) or STOCK.search(said):
        return None
    rest = _the_rest(said, memory, ruled_out, at)
    if not rest:
        return None
    asked_about = str(turn.get("user") or "")
    if A_PERSON.search(asked_about) and not THEM & set(topics.words(rest)):
        return None
    if OFFERS_ANOTHER.match(rest):
        return rest
    return pick(LEADS, memory, text).format(rest=rest)
