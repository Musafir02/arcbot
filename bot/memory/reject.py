import re

from ..compose import pick
from . import choice, recent

MEMORY_STORE = "memory_store"

FILLER = frozenset("""
    ok okay oh ah well right so then but and just really sorry ta thanks thank you thx cheers
    hmm erm uh um like actually honestly tbh though tho anyway ha haha lol x xx please pls
    i im ive id ill we youre you u us for of about at in too either also still yet neither
""".split())

NEGATION = frozenset("""
    nah no nope none not dont do not doesnt didnt didnt never aint already meh rather
""".split())

OBJECT = frozenset("""
    that this it those these them one ones both either neither any all every everything
    thing things one either list two three
""".split())

JUDGED = frozenset("""
    seen saw watch watched read tried had have ate eaten got get fancy fancied like liked keen
    bother bothered feel feeling want wanted sound sounds sounded appeal appeals my me kind
    cup tea sort thing things type sort my mine thanks ta taste tastes
""".split())

DONE = frozenset("seen saw watched read tried had ate eaten got heard done".split())

POSSESSION = frozenset(("got", "get"))
A_HAVE_ALREADY = re.compile(
    r"\b(?:already|before|once|one|ones|last|year|years|since|when|ever|yet|ages?)\b", re.I)
_I_HAVE = re.compile(r"^\s*(?:i\s+have|ive|i\s+got|we\s+have|weve|we\s+got)\b", re.I)

KNOWN = FILLER | NEGATION | OBJECT | JUDGED | DONE

_ASKS_THE_BOT = frozenset("""
    have has do does did can could would will shall is are was were am any anything
""".split())

_WHOLE_LIST = re.compile(
    r"\b(?:all|those|them|these|both|every|everything|any|list|three|two)\b", re.I)

_OFFER_NOT_A_LIST = re.compile(r"\?\s*$")

ANOTHER = (
    "Fair enough \u2014 then how about {option}?",
    "Then {option} instead.",
    "Right, {option} is the other one worth a go.",
    "Not that one, then \u2014 {option}?",
)

PICK_AGAIN = (
    "Fair enough, none of those then. What did you enjoy last? I'll pick something in that vein.",
    "Right, that list is out. Tell me one you did like and I'll go from there.",
    "Fair enough. What have you enjoyed lately? I'll keep clear of these three.",
)

ALL_OF_THEM = (
    "{which} then: {names}.",
    "All of them: {names}.",
    "Then take {which}: {names}.",
    "Good \u2014 {which}: {names}.",
)
ONE_LEFT = (
    "That leaves one: {option}.",
    "Two of those are out, so it comes down to {option}.",
    "Then there is just {option} left.",
)
ONE_TAKEN = (
    "Then take {option}.",
    "Then it is {option}.",
    "Go with {option}, then.",
)

_THE_LOT = re.compile(r"\b(?:all|every|everything|both)\b", re.I)
THE_MOST_A_LIST = 5


def _words(text):
    low = " ".join(str(text or "").lower().replace("\u2019", "'").split())
    if not low or "?" in low:
        return None
    low = low.strip(".,;:!-\u2026 ")
    low = re.sub(r"\b(?:do not|did not|does not)\b", "dont", low)
    low = re.sub(r"n['\u2019]t\b", " not", low)
    words = [w.strip(".,;:!-") for w in low.split()]
    words = [w for w in words if w]
    kept = []
    for word in words:
        if word == "all" and kept and kept[-1] == "at":
            kept.pop()
            continue
        kept.append(word)
    return [w for w in kept if w not in FILLER]


_SOMEONE_ELSE_HAS_IT = re.compile(
    r"(?<!\bi )(?<!\bwe )(?<!\byou )(?<!\bive )(?<!\bweve )(?<!\byouve )"
    r"(?<!\balready )\b(?:has|have|got)\s+(?:everything|it all|the lot)\b", re.I)


def refusal(text, offer=""):
    words = _words(text)
    if not words or len(words) > 7 or len(words) < 2:
        return False
    if _SOMEONE_ELSE_HAS_IT.search(text):
        return False
    unknown = [w for w in words if w not in KNOWN]
    if unknown:
        named = set(re.findall(r"[a-z']+", str(offer or "").lower()))
        if not named or len(unknown) > 3 or not all(w in named for w in unknown):
            return False
    if words[0] in _ASKS_THE_BOT:
        return False
    judged = {w for w in words if w in DONE}
    if (judged and judged <= POSSESSION and not any(w in NEGATION for w in words)
            and not A_HAVE_ALREADY.search(" ".join(words)) and not _I_HAVE.match(str(text or ""))):
        return False
    if not any(w in NEGATION or w in DONE for w in words):
        points_at_the_whole = (_WHOLE_LIST.search(" ".join(words))
                               and all(w in OBJECT for w in words))
        if not points_at_the_whole:
            return False
    return any(w in OBJECT or w in JUDGED for w in words)


STOPS_ON_AN_INITIAL = re.compile(r"(?:^|\s)[A-Z]\.?$")
NAME_GOES_ON = re.compile(r"\.?\s+((?:[A-Z]\.\s*)*(?:[A-Z][a-z'\u2019-]+)(?:\s+[A-Z][a-z'\u2019-]+)?)")


def _the_whole_name(option, reply):
    option = str(option or "").strip()
    if not STOPS_ON_AN_INITIAL.search(option):
        return option
    core = option.split()[-1].rstrip(".")
    found = re.search(r"\b" + re.escape(core) + NAME_GOES_ON.pattern, reply)
    if not found:
        return option
    rest = found.group(1).strip().rstrip(".")
    return (option if option.endswith(".") else option + ".") + " " + rest


def _tidy(option):
    option = re.sub(r"\s*\([^)]*$", "", str(option or "")).strip()
    if re.match(r"^(?:\d|[£$€]\s*\d)", option):
        return ""
    option = re.sub(r"^(A|An|The) (?=[a-z])", lambda m: m.group(1).lower(), option)
    if not (2 < len(option) and len(option.split()) <= 10):
        return ""
    words = option.lower().split()
    if words[0] in _STEP_START or any(w in _CLAUSE_VERB for w in words[1:3]):
        return ""
    return option


_NOT_A_NAME = re.compile(r"[()\[\];:!?]")

_STEP_START = frozenset("""
    take put use add cook roast boil fry bake grill heat mix stir cut chop peel wash rinse spray
    wipe clean soak leave cover simmer drain season salt rest cool freeze store keep serve pour
    toss brush line preheat check test break slice grate whisk knead roll spread fill top drizzle
    sprinkle reduce blend mash layer wrap seal tie trim dry hang iron vacuum dust scrub hoover
""".split())

_CLAUSE_VERB = frozenset("""
    is are was were has have had does do did will would can could make makes keep keeps help
    helps work works come comes go goes run runs give gives take takes last lasts win wins beat
    beats fit fits hold holds protect protects save saves cost costs sound sounds look looks
    taste tastes feel feels crisp crisps promise promises mean means sit sits stand stands need
    needs seem seems turn turns stay stays
""".split())


_TITLE = re.compile(r"\*([^*\n]{2,40})\*")


def _by_title(titles, options):
    if len(titles) < 2:
        return options
    ordered, seen = [], set()
    for title in titles:
        low = title.lower()
        said = next((o for o in options if o.lower().startswith(low)), "")
        if said and said.lower() != low:
            rest = said[len(title):].strip()
            if re.match(r"^(?:,|or\b|and\b|\*)", rest, re.I):
                said = said[:len(title)].strip()
        if not said:
            said = next((o for o in options if low in o.lower()), "")
        said = said or title
        if said.lower() in seen:
            continue
        seen.add(said.lower())
        ordered.append(said)
    return ordered if len(ordered) >= 2 else options


def _a_choice_of_things(reply):
    reply = " ".join(str(reply or "").split())
    return len({title.lower() for title in _TITLE.findall(reply)}) >= 2 \
        or bool(_OR_CHOICE.search(reply))


TRIED_THE_LOT = re.compile(
    r"\btried\b[^.!?]{0,24}?"
    r"\b(?:everything|all of it|all of them|them all|it all|every one|the lot)\b", re.I)


def _the_offer_reply(memory):
    for turn in reversed(recent(memory, 4)):
        reply = str((turn or {}).get("bot") or "")
        if reply and len(_options(reply)) >= 2:
            return reply
    return ""


def _options(reply):
    reply = " ".join(str(reply or "").split())
    if not reply or _OFFER_NOT_A_LIST.search(reply):
        return []
    titles = [_tidy(t) for t in _TITLE.findall(reply)]
    titles = [t for t in titles if t and not _NOT_A_NAME.search(t)]
    options = [_tidy(_the_whole_name(o, reply)) for o in choice.options_in(reply)]
    options = [o for o in options if o and not _NOT_A_NAME.search(o)]
    options = _by_title(titles, options)
    known = {t.lower() for t in titles}
    options = [o for o in options if len(o.split()) > 1 or o.lower() in known]
    short = [o for o in options if len(o.split()) <= 8]
    options = short or options
    if len(options) < 2:
        return []
    if len(titles) < 2 and not _OR_CHOICE.search(reply):
        if not (":" in reply and len(options) >= 3 and all(_a_noun_phrase(o) for o in options)):
            return []
    if _a_list_of_causes(reply, options):
        return []
    return options


_NOT_A_THING_START = frozenset("""
    most more less least too very so quite much many few little enough only even also still yet
    just then now and or but if when while as because than that this these those it they we you
    he she i is are was were be been being do does did done have has had will would can could
    should may might must not no never always usually often sometimes there here
""".split())


_A_REASON = re.compile(
    r"(?:\bbecause\b|\bthe reason\b|\bwhich is why\b|\bthat'?s why\b|\bwhy\b|"
    r"\bsomewhere\b|\bcauses?\b|\bcaused by\b|\bis down to\b|\bcomes down to\b)"
    r"[^.;!?]{0,70}$", re.I)


def _a_list_of_causes(reply, options):
    flat = " ".join(str(reply or "").split())
    for option in options:
        at = flat.lower().find(str(option).lower())
        if at < 0:
            continue
        before = flat[:at]
        for stop in (". ", "! ", "? ", "; "):
            cut = before.rfind(stop)
            if cut > 0:
                before = before[cut + len(stop):]
        if _A_REASON.search(before):
            return True
    return False


def _a_noun_phrase(option):
    words = str(option or "").lower().split()
    return bool(words) and words[0] not in _NOT_A_THING_START


_OR_CHOICE = re.compile(
    r",\s*or\s+(?!(?:it|they|i|you|we|he|she|that|this|there|those)\b)", re.I)


def _said_by_them(option, text):
    option = re.sub(r"\s+in\s+\d+\s*(?:minutes?|mins?|min)?\s*$", "", str(option or ""))
    said = set(re.findall(r"[a-z']+", str(text or "").lower()))

    def every_word(name):
        words = [w for w in re.findall(r"[a-z']+", name.lower()) if w not in ("a", "an", "the")]
        return bool(words) and all(w in said for w in words)

    if every_word(option):
        return True
    name = re.split(r"\s+(?:for|if|which|when|that|to|in|about)\s+", option, maxsplit=1)[0]
    return len(name.split()) > 1 and every_word(name)


def _offered(memory):
    turns = [turn if isinstance(turn, dict) else {} for turn in recent(memory, 4)]
    start = None
    for index in range(len(turns) - 1, -1, -1):
        if len(_options(turns[index].get("bot") or "")) >= 2:
            start = index
            break
    if start is None:
        return None
    if any(str(turn.get("module") or "") != MEMORY_STORE for turn in turns[start + 1:]):
        return None
    left = list(_options(turns[start].get("bot") or ""))
    for turn in turns[start + 1:]:
        line = str(turn.get("user") or "")
        named = [option for option in left if _said_by_them(option, line)]
        left = [option for option in left if option not in named] if named else left[1:]
    return left


_FENCE = re.compile(
    r"\b(?:not|no|never|without|except|anything but)\s+(?:a|an|the|any|too much|more)?\s*"
    r"([a-z][a-z'\-]{3,})", re.I)
_HELD_THE_FENCE = re.compile(r"\b(?:without|no|not|nothing|non)\b", re.I)

FENCED_OUT = (
    "Fair enough, nothing {kind} then. What do you fancy instead?",
    "Right, no {kind} ones. Tell me what you do want and I'll aim at that.",
    "Fair enough - {kind} is out. What sort of thing would you go for?",
)


def _the_fence(memory):
    turns = [turn if isinstance(turn, dict) else {} for turn in recent(memory, 3)]
    offer, options, request = "", [], ""
    for index in range(len(turns) - 1, -1, -1):
        offer = str(turns[index].get("bot") or "")
        options = _options(offer)
        if len(options) >= 2:
            request = str(turns[index].get("user") or "")
            break
    else:
        return None
    ruled_out = [word for word in _FENCE.findall(request) if word not in KNOWN]
    if not ruled_out:
        return None
    started = [offer.find(option) for option in options if offer.find(option) > 0]
    lead = offer[:min(started)] if started else offer[:80]
    if _HELD_THE_FENCE.search(lead):
        return None
    words = [word for word in re.findall(r"[a-z']+", lead.lower()) if len(word) > 3]
    for fence in ruled_out:
        for word in words:
            if word[:4] == fence[:4]:
                return fence
    return None


def _the_whole_lot(options):
    count = len(options or [])
    if count == 2:
        return "both"
    return "all " + {3: "three", 4: "four", 5: "five"}.get(count, "of them")


def offers_a_choice(memory):
    if len(_offered(memory) or []) < 2:
        return False
    reply = _the_offer_reply(memory)
    return _a_choice_of_things(reply) if reply else False


def _the_names(options):
    said = [str(o) for o in options if o]
    if len(said) < 2:
        return said[0] if said else ""
    return ", ".join(said[:-1]) + " and " + said[-1]


def _the_lot_and_the_verb(lines):
    the_lot = bool(_THE_LOT.search(" ".join(lines)))
    return the_lot and any(w in DONE for w in lines), the_lot


def reply_for(text, memory):
    if not isinstance(memory, dict):
        return None
    answer = ""
    for turn in reversed(recent(memory, 2)):
        answer = str((turn or {}).get("bot") or "")
        if answer:
            break
    if not refusal(text, answer):
        return None
    offered = _offered(memory)
    if offered is None:
        return None
    if TRIED_THE_LOT.search(str(text)) and not _a_choice_of_things(_the_offer_reply(memory)):
        return None
    fence = _the_fence(memory)
    if fence:
        said = pick(FENCED_OUT, memory, str(text)).format(kind=fence)
        return said[:1].upper() + said[1:]
    left = list(offered)
    named_by_them = [o for o in left if _said_by_them(o, text)]
    left = [o for o in left if o not in named_by_them] if named_by_them else left[1:]
    lines = _words(text)
    had_them_all, wants_them_all = _the_lot_and_the_verb(lines or [])
    if len(offered) > THE_MOST_A_LIST:
        had_them_all = wants_them_all = False
    if len(offered) < 2:
        if had_them_all or not (left or wants_them_all):
            return pick(PICK_AGAIN, memory, str(text))
        pool = ONE_TAKEN if wants_them_all else ONE_LEFT
        said = pick(pool, memory, str(text)).format(option=(left or offered)[0])
        return said[:1].upper() + said[1:]
    which, names = _the_whole_lot(offered), _the_names(offered)
    if had_them_all:
        return pick(PICK_AGAIN, memory, str(text))
    if wants_them_all:
        said = pick(ALL_OF_THEM, memory, str(text)).format(which=which, names=names)
        return said[:1].upper() + said[1:]
    if not left or (lines and _WHOLE_LIST.search(" ".join(lines))):
        return pick(PICK_AGAIN, memory, str(text))
    option = left[0]
    said = pick(ANOTHER, memory, str(text)).format(option=option)
    return said[:1].upper() + said[1:]
