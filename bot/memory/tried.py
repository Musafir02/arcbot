import re

from . import you
from .facts import PEOPLE_AGED, RELATIONS as A_PERSON

ANSWER_MODULES = ("answers",)

NOT_WORKED = re.compile(
    r"\b(?:did(?:n'?t| not) (?:work|help|do (?:anything|much|the trick|it)|shift (?:it|them)|"
    r"budge|move|make (?:any |a )?difference|change anything|touch (?:it|them))|"
    r"has(?:n'?t| not) worked|is(?:n'?t| not) working|made (?:no|not much) difference|"
    r"no luck|nothing (?:happened|worked)|no (?:change|better|improvement)|"
    r"what if (?:that|it|this) (?:doesn'?t|didn'?t|isn'?t) work(?:ed|ing)?|"
    r"(?:it'?s|it is|they'?re|they are|its|there'?s) still there|"
    r"still (?:not (?:working|worked|fixed|shifted|moved|helped)|blocked|broken|stuck|"
    r"the same|doing it|coming back|leaking|clogged|dripping))\b"
)
STILL_ONLY = re.compile(
    r"^(?:it|its|it's|it is|they|theyre|they're|they are|that|thats|that's|that is|this|"
    r"this is|there|theres|there's|he|hes|he's|he is|she|shes|she's|she is)?\s*"
    r"still\s+(?P<tail>[a-z][a-z' -]*)$"
)
POINTS_AT_IT = frozenset(("there", "the same", "like that", "like this", "doing it", "at it",
                          "the same thing", "no better", "not working"))
TOO_COMMON = frozenset("""the and but for not still it its this that them they there here
out off now just very really again same doing like been being was were are had has have
one two three""".split())

TRIED = re.compile(
    r"\b(?:i|we|ive|i've|weve|we've|they)\s+(?:already\s+|just\s+)?(?:tried|did|used|gave)\s+"
    r"(?:that|this|it|them|those)\b|\btried (?:that|this|it|everything|all of it)\b|"
    r"\btried everything\b"
)

MADE_IT_WORSE = re.compile(
    r"\bnow\b[^.?!]{0,24}\b(?:worse|faster|slower|louder|stuck|jammed|seized|stripped|"
    r"snapped|broke|broken|leaking|dripping|spraying|sparking|dead|wont|won'?t|"
    r"stopped (?:working|moving|spinning|draining)|wobbl\w*|cracked|bent)\b"
)
POINTS_AT_THE_THING = re.compile(r"\b(?:it|its|it's|them|they|that|those)\b")

ELSEWHERE = re.compile(r"\b(?:find|finding|found|book|booking|booked|get hold of|reach|reaching|"
                       r"phone|phoning|ring|ringing)\b")

YET = re.compile(r"\byet\b\W*$")

IMPROVED = re.compile(
    r"\b(?:(?:it|that|this|they|its|thats) (?:has |have |is |are |'s |seems? )?"
    r"(?:actually |really |definitely |properly |much |a bit )?"
    r"(?:helped|helping|works|worked|working|done the trick|did the trick|sorted it)|"
    r"(?:a bit|lots|much|loads|far|slightly|no end) better|feeling better|on the mend|"
    r"clearing up|eased off)\b"
)
WORSE = re.compile(r"\b(?:made (?:it|things|me) (?:worse|sorer)|makes it worse|worse than before|"
                   r"sorer|in agony|unbearable)\b")

WORD = re.compile(r"[a-z0-9']+")

TRADES = (
    (("ant", "ants", "mouse", "mice", "rat", "rats", "wasp", "wasps", "wasp nest", "flea",
      "fleas", "moth", "moths", "cockroach", "cockroaches", "bedbug", "bedbugs", "bed bug",
      "bed bugs", "silverfish", "pest", "pests", "pigeon", "pigeons", "squirrel", "squirrels"),
     "a pest control firm, and the council's pest service is usually the cheapest way in", None),
    (("stain", "stains", "carpet", "sofa", "mattress", "curtain", "curtains", "upholstery",
      "dry clean", "dryclean"),
     "a dry cleaner, who will know what the mark is and say whether it will come out", "mark"),
    (("laptop", "laptop", "phone", "iphone", "android", "tablet", "printer", "router",
      "broadband", "wifi", "computer", "pc"),
     "the maker's support line, where they can watch it happen on a call", "fault"),
    (("car", "cars", "engine", "brake", "brakes", "clutch", "mot", "gearbox", "battery",
      "tyre", "tyres", "steering", "exhaust"),
     "a garage, and it is worth saying what you have already changed", "fault"),
    (("washing machine", "dishwasher", "fridge", "freezer", "oven", "tumble", "dryer",
      "vacuum", "hoover", "microwave", "kettle", "toaster", "appliance", "appliances"),
     "the maker's repair line, and five minutes on the phone settles whether it is worth "
     "fixing", "fault"),
    (("boiler", "boilers", "radiator", "radiators", "heating", "pilot", "thermostat", "flue",
      "pump", "gas", "combi", "immersion"),
     "a Gas Safe engineer, since anything on the gas side is theirs by law", "fault"),
    (("tap", "taps", "pipe", "pipes", "leak", "leaking", "joint", "washer", "valve", "drip",
      "dripping"),
     "a plumber, who can say whether it is a five-minute washer or a bigger job", "fault"),
    (("sink", "sinks", "drain", "drains", "plunger", "trap", "toilet", "waste", "sewer",
      "sewage", "overflow", "shower", "showers"),
     "a plumber, with the plunger and the trap already ruled out", "fault"),
    (("door", "doors", "window", "windows", "hinge", "hinges", "lock", "locks", "handle",
      "frame", "latch", "bolt", "draught", "draft"),
     "a joiner or a handyman, who will tell you whether it is the hinge or the frame", "fault"),
    (("dog", "dogs", "cat", "cats", "rabbit", "hamster", "guinea", "parrot", "puppy",
      "kitten"),
     "a vet, since an animal that is not mending is not something to wait on", "health"),
)

ASK_WHAT_TRIED = (
    "Which things have you tried? I'll skip those and go at what's left.",
    "Tell me what you've already done and I'll not send you round it again.",
)

STILL_GOING_ON = (
    "Still there, then. Any better than it was, or much the same?",
    "Still with you \u2014 has it eased at all since it started?",
    "So it hasn't gone. Is it the same as when it started, or worse?",
)
SAME_STILL = (
    "Right, so that hasn't shifted. What happens now when you try \u2014 nothing at all, or "
    "something different from before?",
    "So it's still going on, then. What have you noticed since \u2014 the same as before, or has "
    "it changed?",
    "Then it hasn't moved. Tell me what it does now and I'll take it from there.",
)
ASK_NEXT = (
    "Then the easy fixes have had their go. Tell me what it's doing now \u2014 still the same, "
    "different, or worse \u2014 and I'll see where that points.",
    "Right, so that's not it. What's it doing now: the same as before, or has it changed?",
    "So the usual thing hasn't touched it. What happens now when you try \u2014 nothing at all, "
    "or something different from before?",
)

STILL_ASK = (
    "Still {state}, then. What happens when you try it again \u2014 nothing at all, or something "
    "different?",
    "Right, still {state}. How long has it been going on, and is it all the time now?",
    "Still {state}, noted. What happens just before it goes like that?",
)

END = (
    "Then I'd stop spending on it and get someone in to look — that's the point where a "
    "home fix stops being the cheap option.",
    "Honestly, at that point I'd have someone look at it properly rather than try a fourth thing.",
    "Then it's past what a weekend and a how-to video can do. Get it looked at properly.",
)

LEADS = (
    "Then it's past a home fix: {trade}.",
    "That's where the home fix ends, I'm afraid \u2014 {trade}.",
    "Then it wants someone with the right kit: {trade}.",
    "So it needs {trade}.",
)

DOING = (
    r"(?:re-?start\w*|re-?boot\w*|re-?set\w*|clean\w*|chang\w*|replac\w*|ble[wd]|topp?\w*|"
    r"unblock\w*|plung\w*|wash\w*|vacuum\w*|hoover\w*|re-?install\w*|uninstall\w*|updat\w*|"
    r"plug\w*|switch\w*|check\w*|tried|us(?:e|ed|ing)\b|cut\w*|stop\w*|start\w*|took|taken|"
    r"drunk|drank|walk\w*|exercis\w*|stretch\w*|ice[ds]?|icing|elevat\w*|book\w*|air\w*|"
    r"vent\w*|rins\w*|soak\w*|scrub\w*|fit\w*|fix\w*|adjust\w*|turn\w*|drain\w*|empt\w*|"
    r"defrost\w*|descal\w*|brush\w*|pok\w*|twist\w*|tighten\w*|loosen\w*|tap\w*|seal\w*|"
    r"open\w*|clos\w*|mov\w*|put\w*|gave|given?|add\w*|reduc\w*|increas\w*|rais\w*|lower\w*)"
)
LEAD_IN = (r"^\W*(?:(?:and|but|so|oh|ok|okay|well|yeah|yep|no|nah|hmm|ah|right|alright|then)"
           r"\W+)*")
STEP_ALREADY = re.compile(
    LEAD_IN + r"(?:i\s*(?:'ve|ve|have)\s+|i\s+|ive\s+)?already\s+(?P<what>" + DOING +
    r"\b(?:[a-z0-9' -]|(?<=\d)\.(?=\d)){0,40})$", re.I)
STEP_TRIED = re.compile(
    LEAD_IN + r"(?:i\s*(?:'ve|ve|have)\s+|i\s+|ive\s+)?(?:already\s+|just\s+)?"
    r"(?:tried|used)\s+(?P<what>\S.*)$", re.I)
STEP_LAST = re.compile(
    LEAD_IN + r"(?:i\s*(?:'ve|ve|have)\s+|i\s+|ive\s+)?(?P<what>" + DOING +
    r"\b(?:[a-z0-9' -]|(?<=\d)\.(?=\d)){0,40})\s+already\W*$", re.I)
PARTICIPLE = (r"(?:" + DOING + r"|[a-z]{4,}ed|bled|wrung|swept|dug|spun|taken|done|ran|made|"
              r"left|held|shut|set|put|cut)")
STEP_DONE = re.compile(
    LEAD_IN + r"(?:(?:i|we)\s*(?:'ve|ve|have)|ive|weve)\s+(?P<what>" + PARTICIPLE +
    r"\b(?:[a-z0-9' -]|(?<=\d)\.(?=\d)){0,40})", re.I)
STEP_DID = re.compile(
    LEAD_IN + r"(?:i|we)\s+(?P<what>" + DOING + r"\b(?:[a-z0-9' -]|(?<=\d)\.(?=\d)){0,40})", re.I)
STEP_VAGUE = frozenset("""that this it them those these everything all anything something
    whatever lot one ones thing things stuff""".split())
STEP_EMPTY = frozenset("""a an the and but or so oh well yeah yep ok okay right alright already
    just really very quite still now again too much more some any of in on off out up down with
    for to at it its it's that this them those my our your his her their""".split())
STEP_LEADS = (
    "You've tried {thing}. Now {step}.",
    "Right, so {thing} is done. {Step}.",
    "Then {step}.",
)
ALREADY_LEADS = (
    "You've already {thing}. {Step}.",
    "Since you've already {thing}, {step}.",
    "Then {step}.",
)
PAST_WORD = re.compile(r"^[a-z]{2,}(?:ed|en|ght)$")
SHORT_PAST = frozenset("bled fled shed sped".split())
PAST_STEP_ED = re.compile(r"^[a-z]{3,}ed$")
PAST_IRREGULAR = frozenset("""ran did made took gave put set cut kept left found got went saw
    wrote sold sent spent built burnt read shot told brought bought thought caught taught""".split())
DONE_LEADS = (
    "You {thing}. Now {step}.",
    "Right, so you {thing}. Then {step}.",
    "Then {step}.",
)
PRESENT_LEADS = (
    "You already {thing}. Now {step}.",
    "Then {step}.",
)
DOING_WORD = re.compile(r"(?:" + DOING + r"|[a-z]{2,}ed)\b", re.I)
TAIL_WORD = re.compile(r"^(?:and|but|or|not|if|so|then|which|that|because|while|rather)\b", re.I)
PRONOUN_TAIL = re.compile(
    r"^(?:put|leave|check|try|give|keep|take|clean|run|top|set|turn|move|wipe|replace|change|"
    r"open|close|hold|press|unplug|switch|bleed|fill|repeat|do)\s+"
    r"(?:it|them|that|this|those|these)\b", re.I)
MORE_STEP_VERBS = frozenset("""undo unplug reinstall upgrade reboot restart reset force update
    wipe swap plug thaw rinse scrub polish vacuum hoover descale defrost sand trim scrape blot
    clamp loosen tighten snip shave share write print send take keep hold hang mount have mow
    scarify aerate reseed edge""".split())
STEP_WORDS = 22
CLAUSE = re.compile(r"\s*;\s*|:\s+|\s+then\s+|\s+-\s+|,\s+and\s+")


def words_of(text):
    return WORD.findall(str(text or "").lower().replace("\u2019", "'"))


def reads_as_not_worked(text):
    line = " ".join(words_of(text))
    if not line or len(line.split()) > 14:
        return False
    if ELSEWHERE.search(line):
        return False
    if IMPROVED.search(line) or WORSE.search(line):
        return False
    if YET.search(line):
        return False
    if NOT_WORKED.search(line):
        return True
    if MADE_IT_WORSE.search(line) and POINTS_AT_THE_THING.search(line):
        return True
    return bool(TRIED.search(line))


STILL_STATE = re.compile(r"\bstill\s+(?P<state>[a-z' ]{2,30})\W*$")
NOT_A_STATE = frozenset("""here there waiting hungry tired thirsty awake asleep up alive
hurts hurting hurt sore aching achy painful pain ill sick poorly unwell dizzy faint sickly
upset sad anxious stressed worried down low rough rubbish wobbly shaky weak numb
depressed miserable weepy tearful
going coming learning working trying looking thinking hoping planning deciding wondering
worse better ok okay fine good great bad nice rubbish
at work in bed on my way at it on it at home on hold in touch
a chance time young single busy late early on off out in the same""".split())
STILL_ASKS = re.compile(r"^(?:are|is|do|does|did|will|would|can|could|should|shall|have|has|"
                        r"why|how|what|when|where|who|which)\b")


def the_still_state(text, memory):
    said = " ".join(words_of(text))
    if not said or len(said.split()) > 7 or said.endswith("?"):
        return ""
    if STILL_ASKS.match(said):
        return ""
    found = STILL_STATE.search(said)
    if not found:
        return ""
    state = [word for word in words_of(found.group("state")) if word not in STEP_EMPTY]
    if not state or any(word in NOT_A_STATE for word in state):
        return ""
    named = {_stem(word) for word in words_of(person_said(memory))}
    named |= {_stem(word) for word in last_answer_words(memory)}
    if not any(_stem(word) in named for word in state):
        return ""
    if HEALTH.search(" ".join(state)):
        return ""
    return " ".join(state)


def still_the_state(text, memory):
    return bool(the_still_state(text, memory))


def might_be_a_report(text):
    said = " ".join(words_of(text))
    if not said or len(said.split()) > 20:
        return False
    return bool(NOT_WORKED.search(said) or MADE_IT_WORSE.search(said) or TRIED.search(said)
                or STILL_STATE.search(said) or STEP_DONE.search(said) or STEP_DID.search(said)
                or YET.search(said) or NAMED_TRY.search(said))


def names_a_trade(text):
    said = " ".join(words_of(text))
    for _entry_words, trade, _needs in TRADES:
        name = str(trade or "").split(",")[0].strip().lower()
        if name and name in said:
            return True
    return False


def after_an_answer(memory):
    turns = [t for t in (memory.get("turns") or []) if isinstance(t, dict)]
    if not turns:
        return False
    module = str(turns[-1].get("module") or "")
    if module in ANSWER_MODULES:
        return True
    if module != "chat":
        return False
    if memory.get("handed_back_step") == len(turns) - 1:
        return True
    return names_a_trade(turns[-1].get("bot")) or asked_what_its_doing(memory)


def last_answer_words(memory):
    said = [str(line or "") for line in _the_lines(memory)]
    last = memory.get("last_answer")
    if isinstance(last, dict):
        keys = last.get("keys")
        if isinstance(keys, (list, tuple, set, frozenset)):
            said.extend(str(key) for key in keys)
    return set(words_of(" ".join(said)))


PROBLEM_OR_FIX = re.compile(
    r"\b(?:how (?:do|can|should|would|could) i|how to|what (?:do|can|could) i do|"
    r"any (?:tips|advice)|what should i do)\b|"
    r"\b(?:is|are|keeps|keep|was|wont|won'?t|doesn'?t|doesnt|isn'?t|isnt|not) "
    r"(?:\w+ )?(?:working|worked|blocked|broken|stuck|sticking|jammed|jamming|dragging|"
    r"leaking|dripping|clogged|smelling|smells|"
    r"noisy|coming back|moving|rising)\b|"
    r"\b(?:blocked|broken|stuck|leaking|clogged)\b|"
    r"\bi (?:can'?t|cant|couldn'?t|couldnt)\b|"
    r"\b(?:wont|won'?t) (?:come|get|go away|stop|budge)\b|"
    r"\b(?:wont|won'?t|doesn'?t|doesnt|keeps? (?:on )?)\b"
)


def asks_for_a_fix(memory):
    turns = [t for t in (memory.get("turns") or []) if isinstance(t, dict)]
    if not turns:
        return False
    asked = " ".join(words_of(turns[-1].get("user")))
    if not asked:
        return False
    if PROBLEM_OR_FIX.search(asked):
        return True
    if len(turns) > 1:
        before = " ".join(words_of(turns[-2].get("user")))
        return bool(PROBLEM_OR_FIX.search(before))
    return False


FAULT = re.compile(
    r"\b(?:broke|broken|breaking|not working|stopped working|stopped|wont|won'?t|doesn'?t|"
    r"doesnt|isn'?t|isnt|leak|leaks|leaking|drip|dripping|noise|noisy|banging|knocking|"
    r"rattl\w*|blocked|blockage|unblock\w*|stuck|sticking|jammed|jamming|clogged|"
    r"dragging|not (?:shutting|opening|closing)|smell|smells|smelling|smelly|"
    r"smoke|"
    r"smoking|sparking|dead|fault|faulty|overheat\w*|flashing|damaged|gone wrong|packed in|"
    r"keeps? (?:cutting out|going off|stopping|tripping|switching off|playing up|packing in)|"
    r"cuts? out|cutting out|played up|playing up|on the blink|packing in|not firing|"
    r"drains? slowly|slow to drain)"
)
HEALTH = re.compile(
    r"\b(?:ill|sick|poorly|unwell|pain|hurt\w*|limp\w*|vomit\w*|swollen|swelling|"
    r"not eating|off (?:his|her|their|its) food|wont eat|won'?t eat|blood|pus|constipated|"
    r"breathing|wheez\w*|shaking|trembling|dying|discharge|losing (?:fur|weight))\b"
)
MARK = re.compile(r"\b(?:stain\w*|mark|marks|smudge|spill\w*|ink|wine|coffee|grease|scuff)\b")

EVIDENCE = {"fault": FAULT, "health": HEALTH, "mark": MARK}

BUYING = re.compile(
    r"\b(?:which one|which (?:\w+ )?(?:is|to|should)|recommend\w*|best|any good|"
    r"worth (?:buying|getting)|should i (?:buy|get)|need a new|needs a new|"
    r"thinking of (?:buying|getting)|going to (?:buy|get)|want to (?:buy|get)|"
    r"shopping for|looking (?:for|at) (?:a|some)|what should i (?:buy|get)|"
    r"how much (?:do|does|are|is) (?:they|it|these))\b"
)


def buying(memory):
    turns = [t for t in (memory.get("turns") or []) if isinstance(t, dict)]
    if not turns:
        return False
    return bool(BUYING.search(" ".join(words_of(turns[-1].get("user")))))


def person_said(memory):
    return " ".join(" ".join(words_of(line)) for line in _the_lines(memory) if line)


def _the_lines(memory):
    turns = [t for t in (memory.get("turns") or []) if isinstance(t, dict)]
    if not turns:
        return []
    said = [turns[-1].get("user")]
    if len(turns) > 1 and reads_as_not_worked(" ".join(words_of(turns[-1].get("user")))):
        said.append(turns[-2].get("user"))
    return said


def _names(said, blob, entry_words):
    if said.intersection(entry_words):
        return True
    for word in entry_words:
        if " " in word:
            if word in blob:
                return True
        elif len(word) >= 5 and any(token.startswith(word) for token in said):
            return True
    return False


STILL_SPECIFIC = re.compile(
    r"\bstill (?:blocked|leaking|dripping|clogged|stuck|broken|coming back|noisy|smelling|"
    r"jammed|squeaking|the same|not draining|wont|won'?t|there)\b"
)
NAMED_TRY = re.compile(r"\b(?:tried|used|gave)\s+(?:a|an|the|my|some|his|her|their|this new)\b")


def names_a_thing(memory):
    said = set(words_of(person_said(memory)))
    if not said:
        return False
    blob = " ".join(sorted(said))
    return any(_names(said, blob, entry_words) for entry_words, _, _ in TRADES)


def has_evidence(text, memory):
    turns = [t for t in (memory.get("turns") or []) if isinstance(t, dict)]
    if not turns:
        return False
    asked = " ".join(words_of(turns[-1].get("user")))
    if FAULT.search(asked) or MARK.search(asked) or NAMED_TRY.search(asked):
        return True
    report = " ".join(words_of(text))
    if STILL_SPECIFIC.search(report) or NAMED_TRY.search(report):
        return True
    return bool(MADE_IT_WORSE.search(report) and POINTS_AT_THE_THING.search(report))


def asked_what_its_doing(memory):
    turns = [t for t in (memory.get("turns") or []) if isinstance(t, dict)]
    if not turns:
        return False
    said = " ".join(words_of(turns[-1].get("bot")))
    return "doing now" in said or "happens now when you try" in said


def already_named(trade, memory):
    turns = [t for t in (memory.get("turns") or []) if isinstance(t, dict)]
    name = str(trade or "").split(",")[0].strip().lower()
    if not name:
        return False
    said = " ".join(" ".join(words_of(t.get("bot"))) for t in turns[-2:]
                    if str(t.get("module") or "") == "chat")
    return bool(name) and name in said


def _the_answered_line(memory):
    turns = [t for t in (memory.get("turns") or []) if isinstance(t, dict)]
    return str(turns[-1].get("user") or "") if turns else ""


def trade_for(memory):
    said = last_answer_words(memory)
    words = person_said(memory)
    blob = " ".join(sorted(said)) + " " + words
    worse = bool(MADE_IT_WORSE.search(words) and POINTS_AT_THE_THING.search(words))
    about_a_fault = bool(FAULT.search(" ".join(words_of(_the_answered_line(memory)))))
    for entry_words, trade, needs in TRADES:
        if not _names(said, blob, entry_words):
            continue
        if needs is None:
            return trade
        pattern = EVIDENCE.get(needs)
        if pattern is None:
            continue
        if pattern.search(words) or (needs == "fault" and worse and about_a_fault):
            return trade
    return None


ACTED_SAID = re.compile(
    r"^(?:i|we)\s+(?:(?:have|had|already|just|finally|actually)\s+)*"
    r"(?:told|done|did|sent|texted|messaged|emailed|called|rang|phoned|asked|"
    r"said\s+(?:(?:it|that)\s+)?to|spoke\s+(?:to|with)|talked\s+(?:to|with)|"
    r"said\s+what\s+you\s+(?:suggested|said)|"
    r"used\s+(?:it|that|your\s+(?:wording|words|line|suggestion|advice|text)))\b"
)
SAY_ADVICE = re.compile(
    r"\b(?:what|how|which)\s+(?:(?:should|shall|do|can|could|would)\s+)?(?:i|we)\s+"
    r"(?:say|tell|text|message|write|email|call|ask|talk|speak|word)\b"
    r"|\bwhat\s+to\s+(?:say|tell|text|message|write|email)\b"
    r"|\b(?:how|what)\s+(?:would|could|should)\s+you\s+(?:say|word|phrase)\b"
)
TOLD_THE_BOT = re.compile(r"\b(?:told|said|texted|messaged|emailed|called|asked)\s+you\b")
ACTED_REPLIES = (
    "How did it land?",
    "What did they say?",
    "Did it come across the way you meant?",
    "How did that go over?",
    "Did it help?",
)


def acted_pool(text, memory):
    line = " ".join(words_of(text))
    if not ACTED_SAID.match(line) or TOLD_THE_BOT.search(line):
        return None
    turns = [t for t in (memory.get("turns") or []) if isinstance(t, dict)]
    if not turns:
        return None
    last = turns[-1]
    if str(last.get("module") or "") == "safety":
        return None
    asked = " ".join(words_of(last.get("user")))
    if not SAY_ADVICE.search(asked):
        return None
    return ACTED_REPLIES


STEP_TAIL_NOUN = re.compile(
    r"^(?:the|a|an|my|its|their|our|your|his|her|this|that)\b", re.I)


def _up_to_the_contrast(what):
    pieces = re.split(r"\s+(but|and|though|although|yet)\s+", what, maxsplit=1, flags=re.I)
    if len(pieces) < 3:
        return what
    head, joint, tail = pieces
    if joint.lower() == "and" and STEP_TAIL_NOUN.match(tail.strip()):
        return what
    return head


def _read_step_tried(text):
    line = " ".join(str(text or "").lower().split()).strip().strip(".,!")
    if not line or "?" in line or len(line.split()) > 14:
        return None, None
    if NOT_WORKED.search(line) or IMPROVED.search(line) or WORSE.search(line):
        return None, None
    for pattern in (STEP_ALREADY, STEP_TRIED, STEP_LAST, STEP_DONE, STEP_DID):
        found = pattern.match(line)
        if not found:
            continue
        what = " ".join(found.group("what").split()).strip(" .,!'")
        what = re.sub(r"\s+already$", "", what)
        what = re.sub(r"^(?:tried|used)\s+", "", what)
        what = _up_to_the_contrast(what).strip(" .,!'")
        words = [w for w in words_of(what) if w not in STEP_EMPTY]
        if not words or set(words) <= STEP_VAGUE:
            continue
        return what, pattern
    return None, None


def the_step_tried(text):
    return _read_step_tried(text)[0]


PAST_STEP = re.compile(
    r"^\W*(?:(?:and|but|so|oh|ok|okay|well|yeah|yep|no|nah|hmm|ah|right|alright|then)\W+)*"
    r"(?:i|we)\s+(?P<what>[a-z0-9' ]{3,80})$", re.I)


def _the_past_step(text, said):
    line = " ".join(str(text or "").lower().split()).strip().strip(".,!")
    if not line or not said or "?" in line:
        return None
    if NOT_WORKED.search(line) or IMPROVED.search(line) or WORSE.search(line):
        return None
    found = PAST_STEP.match(line)
    if not found:
        return None
    what = " ".join(found.group("what").split()).strip(" .,!'")
    what = re.sub(r"\s+already$", "", what)
    what = re.split(r"\s+(?:but|and|though|although|yet)\s+", what)[0].strip(" .,!'")
    words = [w for w in words_of(what) if w not in STEP_EMPTY]
    if len(words) < 2:
        return None
    first = words[0]
    if first not in PAST_IRREGULAR and not (PAST_STEP_ED.match(first)
                                            or first in SHORT_PAST):
        return None
    if not in_the_answer(what, said):
        return None
    return what


def _the_last_answer(memory):
    turns = [t for t in ((memory or {}).get("turns") or []) if isinstance(t, dict)]
    if not turns:
        return ""
    last = turns[-1]
    if str(last.get("module") or "") != "answers":
        return ""
    return str(last.get("bot") or "")


def _stem(word):
    for ending in ("ing", "ed", "es", "s"):
        if len(word) - len(ending) >= 3 and word.endswith(ending):
            word = word[:-len(ending)]
            if ending in ("ing", "ed") and len(word) > 3 and word[-1] == word[-2]:
                word = word[:-1]
            break
    return word


def _step_stems(text):
    return {_stem(w) for w in words_of(text) if w not in STEP_EMPTY and w not in STEP_VAGUE}


SAME_STEP = frozenset(("", "s", "es", "ed", "d", "ing"))


def _names_it(part, stems):
    for word in words_of(part):
        got = _stem(word)
        for tried in stems:
            if got == tried:
                return True
            if len(got) >= 5 and tried.startswith(got) and tried[len(got):] in SAME_STEP:
                return True
            if len(tried) >= 5 and got.startswith(tried) and got[len(tried):] in SAME_STEP:
                return True
    return False


MOVES = re.compile(r",\s*|\s+so\s+|\s+and\s+", re.I)


def _the_move_after(part, stems):
    return _the_move_pieces(part, stems)[1]


def _the_move_pieces(part, stems):
    if A_CONDITION.match(str(part or "").strip()):
        return "", ""
    pieces = [p.strip(" .,;:") for p in MOVES.split(str(part or "")) if p.strip(" .,;:")]
    best, last = 0, None
    for i, piece in enumerate(pieces):
        words = set(words_of(piece))
        hits = sum(1 for tried in stems
                   if any(w == tried or (len(w) >= 5 and tried.startswith(w)
                                         and tried[len(w):] in SAME_STEP)
                          or (len(tried) >= 5 and w.startswith(tried)
                              and w[len(tried):] in SAME_STEP) for w in words))
        if hits and hits >= best:
            best, last = hits, i
    if last is None:
        return "", ""
    rest = pieces[last + 1:]
    if not rest:
        return pieces[last], ""
    left = " and ".join(rest)
    if PRONOUN_TAIL.match(left) or (TAIL_WORD.match(left) and not _opens_a_step(left)):
        return pieces[last], ""
    return pieces[last], (left if _opens_a_step(left) else "")


def _clauses(text):
    out, piece, depth = [], [], 0
    for chunk in CLAUSE.split(" ".join(str(text or "").split())):
        depth += chunk.count("(") - chunk.count(")")
        if piece and depth > 0:
            piece.append(chunk)
            continue
        if piece:
            out.append(", ".join(piece))
        piece = [chunk]
    if piece:
        out.append(", ".join(piece))
    return [p.strip(" .,;:") for p in out if p.strip(" .,;:")]


def _a_step(piece):
    piece = piece.strip(" .,;:")
    if len(piece.split()) > STEP_WORDS:
        head = piece.split(": ")[0].strip(" .,;:")
        if head and head != piece:
            piece = head
    if piece and len(piece.split()) > STEP_WORDS:
        head, comma, tail = piece.partition(", ")
        if comma and A_CONDITION.match(head):
            step = tail.split(", ")[0].strip(" .,;:")
            if step and _opens_a_step(step):
                piece = head + ", " + step
    if not piece or len(piece.split()) > STEP_WORDS or len(piece) > 180:
        return ""
    return piece


A_CONDITION = re.compile(r"^(?:if|when|once|unless|whenever|wherever)\b", re.I)


def _opens_a_step(part):
    from ..compose.verdict import IMPERATIVES

    words = words_of(part)
    if not words:
        return False
    first = words[0]
    if first in IMPERATIVES or first in MORE_STEP_VERBS:
        return True
    head, comma, tail = str(part or "").strip().partition(", ")
    if comma and A_CONDITION.match(head):
        rest = words_of(tail)
        if rest and (rest[0] in IMPERATIVES or rest[0] in MORE_STEP_VERBS):
            return True
    return False


def _the_step_after(thing, memory):
    turns = [t for t in (memory.get("turns") or []) if isinstance(t, dict)]
    if not turns:
        return ""
    last = turns[-1]
    if str(last.get("module") or "") != "answers":
        return ""
    return _walk_answer(str(last.get("bot") or ""), thing)


def _the_steps_of(said):
    from . import repeat

    if not said:
        return []
    parts = []
    for sentence in repeat.SENTENCE.split(str(said).strip()):
        for clause in _clauses(sentence):
            piece = _a_step(clause)
            if piece and piece not in parts:
                parts.append(piece)
    return parts


def _list_heads(said):
    from . import repeat

    heads = set()
    for sentence in repeat.SENTENCE.split(str(said or "").strip()):
        head, colon, rest = sentence.partition(":")
        if not colon or not rest.strip():
            continue
        for clause in _clauses(head):
            piece = _a_step(clause)
            if piece:
                heads.add(_flat(piece))
    return heads


STEP_TIMING = frozenset("""last week weeks month months year years today yesterday already now twice
    once again day days night morning time""".split())


def _object_stems(text):
    out = set()
    for w in words_of(text):
        if w in STEP_EMPTY or w in STEP_VAGUE or w in STEP_TIMING:
            continue
        if w in PAST_IRREGULAR or w in SHORT_PAST or PAST_STEP_ED.match(w):
            continue
        if DOING_WORD.match(w):
            continue
        out.add(_stem(w))
    return out


def in_the_answer(thing, said):
    stems = _step_stems(thing)
    if not stems:
        return False
    parts = _the_steps_of(said)
    if not any(_names_it(part, stems) for part in parts):
        return False
    objects = _object_stems(thing)
    if objects:
        return any(_names_it(part, objects) for part in parts)
    return True


KEEPS_IT_RIGHT = re.compile(
    r"\b(?:stops?|keeps?|prevents?|avoids?|is what|are what|helps?|means)\b", re.I)


def _flat(text):
    return " ".join(str(text or "").lower().split()).strip(" .,;:")


def _the_first_step_left(said, seen, after=""):
    from . import repeat

    heads = _list_heads(said)
    parts = _the_steps_of(said)
    if after:
        where = _flat(after)
        for i, part in enumerate(parts):
            flat = _flat(part)
            if where and (flat == where or where in flat or flat in where):
                parts = parts[i + 1:]
                break
    for part in parts:
        flat = _flat(part)
        if flat in heads:
            continue
        if any(flat == was or was in flat for was in seen):
            continue
        if _opens_a_step(part) and repeat._says_what_to_do(part):
            return part
        joined = re.sub(r"^(?:and|but|or)\s+", "", flat, flags=re.I)
        if A_CONDITION.match(joined) and repeat._says_what_to_do(joined):
            if joined != flat:
                joined = joined[:1].upper() + joined[1:]
            return joined
    if after:
        for part in parts:
            flat = _flat(part)
            if flat in heads or any(flat == was or was in flat for was in seen):
                continue
            if repeat.ASKING_THEM.search(part):
                continue
            if repeat._says_what_to_do(part):
                return part
    return ""


def _with_its_tail(part, parts, i):
    from . import repeat

    if i + 2 != len(parts):
        return part
    nxt = parts[i + 1]
    if not repeat._says_what_to_do(nxt) or repeat.ASKING_THEM.search(nxt):
        return part
    if A_CONDITION.match(nxt) or _flat(nxt) in _list_heads(nxt):
        return part
    if len(words_of(part)) + len(words_of(nxt)) > 40:
        return part
    return part.rstrip(" .,;:") + ", and " + nxt[:1].lower() + nxt[1:]


def _the_advice_after(parts):
    from . import repeat
    from . import topics

    for part in reversed(parts):
        if len(words_of(part)) < 5:
            continue
        if repeat.ASKING_THEM.search(part):
            continue
        if topics.RED_FLAG.match(part):
            continue
        if PRONOUN_TAIL.match(part) or (TAIL_WORD.match(part) and not _opens_a_step(part)):
            continue
        if KEEPS_IT_RIGHT.search(part):
            return part
    return ""


def _walk_answer(said, thing, wrap=True):
    from . import repeat
    from . import topics

    parts = _the_steps_of(said)
    stems = _step_stems(thing)
    if not parts or not stems:
        return ""
    heads = _list_heads(said)
    if not any(_names_it(part, stems) for part in parts):
        return ""
    start = 0
    theirs_is_a_step = False
    for i, part in enumerate(parts):
        if _names_it(part, stems):
            named, move = _the_move_pieces(part, stems)
            if move and repeat._says_what_to_do(move):
                return move
            theirs_is_a_step = _opens_a_step(part) or _opens_a_step(named)
            start = i + 1
            break
    if not theirs_is_a_step:
        return _the_advice_after(parts[start:]) if not wrap else ""
    for i, part in enumerate(parts[start:], start):
        if _names_it(part, stems):
            move = _the_move_after(part, stems)
            if move and repeat._says_what_to_do(move):
                return move
            continue
        if repeat.ASKING_THEM.search(part):
            continue
        if topics.RED_FLAG.match(part):
            continue
        if PRONOUN_TAIL.match(part) or (TAIL_WORD.match(part) and not _opens_a_step(part)):
            continue
        if _flat(part) in heads:
            continue
        if _opens_a_step(part):
            return _with_its_tail(part, parts, i)
    if not wrap:
        advice = _the_advice_after(parts[start:])
        if advice:
            return advice
        return ""
    for part in parts[:max(start - 1, 0)]:
        if PRONOUN_TAIL.match(part) or (TAIL_WORD.match(part) and not _opens_a_step(part)):
            continue
        if _flat(part) in heads:
            continue
        if _opens_a_step(part) and repeat._says_what_to_do(part):
            return part
    return ""


def reads_as_a_step_done(text, memory):
    if not isinstance(memory, dict) or not memory:
        return False
    thing, _shape = _read_step_tried(text)
    said = _the_last_answer(memory)
    if not thing:
        thing = _the_past_step(text, said)
        if not thing:
            return False
    elif said and not in_the_answer(thing, said):
        return False
    if not said:
        return False
    walk = _walk_answer(said, thing)
    if walk:
        return True
    return len(_the_steps_of(said)) <= 1


def _as_a_lead(lead, thing, step):
    thing = you(thing)
    step = step.strip(" .,;:")
    step = re.sub(r",?\s*\bthen$", "", step).rstrip(" ,;:")
    first = step.split()[0] if step.split() else ""
    if not (first in ("I", "I'm", "I've", "I'd") or (first.isupper() and len(first) > 1)):
        step = step[:1].lower() + step[1:]
    reply = lead.format(thing=thing, Thing=thing[:1].upper() + thing[1:], step=step,
                        Step=step[:1].upper() + step[1:])
    return reply.rstrip(" .") + "."


def next_step_pool(text, memory):
    if not memory:
        return None
    thing, shape = _read_step_tried(text)
    said_as_the_past = False
    if not thing:
        thing = _the_past_step(text, _the_last_answer(memory))
        if not thing:
            return None
        said_as_the_past = True
    elif _the_last_answer(memory) and not in_the_answer(thing, _the_last_answer(memory)):
        return None
    if buying(memory):
        return None
    step = _the_step_after(thing, memory)
    if not step:
        return None
    from ..compose import pick

    says_the_doing = bool(DOING_WORD.match(thing)) and shape is not STEP_TRIED
    first_word = (thing.split() or [""])[0].lower()
    as_a_habit = says_the_doing and not (PAST_WORD.match(first_word)
                                         or first_word in PAST_IRREGULAR)
    if said_as_the_past:
        leads = DONE_LEADS
    elif as_a_habit:
        leads = PRESENT_LEADS
    else:
        leads = ALREADY_LEADS if says_the_doing else STEP_LEADS
    reply = _as_a_lead(pick(leads, memory, text), thing, step)
    turns = [t for t in (memory.get("turns") or []) if isinstance(t, dict)]
    memory["handed_back_step"] = len(turns)
    memory["handed_back_text"] = step
    memory["handed_back_seen"] = list(memory.get("handed_back_seen") or []) + [_flat(step)]
    if turns:
        memory["handed_back_answer"] = str(turns[-1].get("bot") or "")
    return [reply]


NEXT_LEADS = (
    "Then {step}",
    "Next: {step}",
    "After that, {step}",
    "Then this: {step}",
)


NEXT_ASK_WORDS = frozenset("""what else anything next now other then after that and can could
    should would i we you me my it be is are there more one another again try do does done
    something new also help suggest recommend""".split())


def _asks_for_the_next_part(text):
    from . import repeat

    line = " ".join(str(text or "").lower().split()).strip().strip(".,!")
    if not line or len(line.split()) > 7:
        return False
    if not repeat.NEXT_ASK.match(line):
        return False
    return all(word in NEXT_ASK_WORDS for word in words_of(line))


def next_step_ask_pool(text, memory):
    if not memory or not _asks_for_the_next_part(text):
        return None
    step = str(memory.get("handed_back_text") or "").strip()
    said = str(memory.get("handed_back_answer") or "")
    if not step or not said:
        return None
    turns = [t for t in (memory.get("turns") or []) if isinstance(t, dict)]
    if memory.get("handed_back_step") != len(turns) - 1:
        return None
    seen = set(memory.get("handed_back_seen") or [])
    more = _walk_answer(said, step, wrap=False)
    if not more:
        more = _the_first_step_left(said, seen, after=step)
    if not more or " ".join(more.lower().split()) == " ".join(step.lower().split()):
        return None
    from ..compose import pick

    reply = _as_a_lead(pick(NEXT_LEADS, memory, text), "", more)
    memory["handed_back_step"] = len(turns)
    memory["handed_back_text"] = more
    memory["handed_back_seen"] = list(seen | {_flat(more)})
    memory["handed_back_answer"] = said
    return [reply]


def _somebody_is_the_subject(memory):
    from . import facts, named

    topic = (memory or {}).get("topic")
    if not isinstance(topic, dict):
        return False
    words = set(words_of(topic.get("text") or ""))
    words |= {str(word).lower() for word in (topic.get("words") or ()) if word}
    if not words:
        return False
    if words & set(facts.KIN) or words & set(named.PEOPLE_WORDS) or words & set(facts.PET_ANIMALS):
        return True
    user = (memory or {}).get("user") or {}
    names = set()
    for entry in user.get("pets") or ():
        if isinstance(entry, dict) and entry.get("name"):
            names.add(str(entry["name"]).lower())
    for entry in user.get("others") or ():
        if isinstance(entry, dict) and entry.get("name"):
            names.add(str(entry["name"]).lower())
        elif isinstance(entry, str):
            names.add(entry.lower())
    return bool(words & names)


def still_tail(text, memory):
    state = the_still_state(text, memory)
    if state:
        return state
    line = " ".join(words_of(text))
    if not line or len(line.split()) > 6:
        return ""
    match = STILL_ONLY.match(line)
    if not match:
        return ""
    tail = match.group("tail").strip()
    if tail not in POINTS_AT_IT:
        return ""
    if _somebody_is_the_subject(memory):
        return ""
    return tail


def a_card_is_not_the_answer(text, memory):
    tail = still_tail(text, memory)
    if not tail:
        return False
    if tail in POINTS_AT_IT:
        return after_an_answer(memory)
    return names_a_thing(memory) or after_an_answer(memory)


def still_going_on(text, memory):
    tail = still_tail(text, memory)
    if not tail or buying(memory):
        return None
    if tail in POINTS_AT_IT:
        if not after_an_answer(memory):
            return None
        if not names_a_thing(memory):
            return STILL_GOING_ON
    elif not names_a_thing(memory):
        return None
    pool = pool_for(text, memory)
    if pool is not None and pool is not ASK_WHAT_TRIED and pool is not SAME_STILL:
        return None
    return SAME_STILL


def reply_for(text, memory):
    from ..compose import pick

    pool = still_going_on(text, memory)
    if not pool:
        return None
    return pick(pool, memory, str(text or ""))


def pool_for(text, memory):
    care = in_care_pool(text, memory)
    if care:
        return care
    if not (reads_as_not_worked(text) or still_the_state(text, memory)
            or still_tail(text, memory)) or not after_an_answer(memory):
        step = next_step_pool(text, memory)
        if step:
            return step
        more = next_step_ask_pool(text, memory)
        if more:
            return more
        return None
    report = " ".join(words_of(text))
    made_it_worse = bool(MADE_IT_WORSE.search(report) and POINTS_AT_THE_THING.search(report))
    if made_it_worse and not asks_for_a_fix(memory):
        return None
    if buying(memory):
        return None
    if asked_what_its_doing(memory):
        return END
    trade = trade_for(memory)
    if trade:
        if already_named(trade, memory):
            return ASK_NEXT
        return [lead.format(trade=trade) for lead in LEADS]
    state = the_still_state(text, memory)
    if state and not (asks_for_a_fix(memory) and has_evidence(text, memory)):
        return [line.format(state=state) for line in STILL_ASK]
    if not asks_for_a_fix(memory) or not has_evidence(text, memory):
        if still_tail(text, memory) and (still_tail(text, memory) in POINTS_AT_IT
                                        or names_a_thing(memory)):
            return SAME_STILL
        return None
    if made_it_worse and not (NOT_WORKED.search(report) or TRIED.search(report)):
        return None
    if not names_a_thing(memory):
        return ASK_WHAT_TRIED
    return ASK_NEXT



IN_CARE = re.compile(
    r"\b(?:in|at|on) (?:the |a |an )?(?:hospital|infirmary|hospice|care home|nursing home|"
    r"residential home|ward|icu|itu|hdu|a&e|ae|rehab|clinic)\b"
)
SHE = frozenset("""mum mam mummy mom mother mummy nan nana gran granny grandma grandmother
                   nanny daughter sister wife aunt auntie girlfriend niece""".split())
HE = frozenset("""dad daddy father grandad granddad grandpa grandfather son brother husband
                  uncle boyfriend nephew""".split())
STILL_ABOUT_A_PERSON = frozenset("""there the same in now hospital ward home out yet better
                                    no not like that doing it again care""".split())
POINTING = frozenset("""it its it's she she's he he's they they're theyre that theres there's and
                        but so is are was were s""".split())

IN_CARE_ASK = (
    "Still in, then. How is {subj} doing today?",
    "No change yet, then. How has your {word} been today?",
    "Still there. The waiting is the worst of it, and no news is not bad news.",
    "Still in, then. Has anyone there said what happens next?",
    "Still in. How are you doing with all of it?",
    "Still in, then. Did you get to see {obj} today?",
)
IN_CARE_ASK_UNNAMED = (
    "Still in, then. How are they doing today?",
    "No change yet, then. How have they been today?",
    "Still there. The waiting is the worst of it, and no news is not bad news.",
    "Still in, then. Has anyone there said what happens next?",
    "Still in. How are you doing with all of it?",
    "Still in, then. Did you get to see them today?",
)
IN_CARE_SELF = (
    "Still in, then. How are you doing today?",
    "Still in. Is someone bringing you the things you need?",
    "Still in, then. Has anyone said how long they're keeping you in?",
)


def _the_person_word(token):
    word = token[:-2] if token.endswith("'s") else token
    if word.endswith("s") and word[:-1] in SHE | HE:
        word = word[:-1]
    return word if word in SHE or word in HE else ""


def _a_report_on_a_person(text):
    said = " ".join(words_of(text))
    tokens = said.split()
    if not tokens or len(tokens) > 6 or said.endswith("?"):
        return False
    if "still" not in tokens:
        return False
    at = tokens.index("still")
    after = tokens[at + 1:]
    return bool(after) and all(word in STILL_ABOUT_A_PERSON for word in after) \
        and all(word in POINTING for word in tokens[:at])


def _in_care(memory):
    turns = [t for t in (memory.get("turns") or []) if isinstance(t, dict)]
    lines = [t.get("user") for t in turns][-6:]
    for line in reversed([l for l in lines if l]):
        said = " ".join(words_of(line))
        if any(_names(set(said.split()), said, entry_words) for entry_words, _, _ in TRADES):
            return None
        if not IN_CARE.search(said):
            continue
        with_someone = re.search(r"\bwith\s+(?:my\s+|our\s+|the\s+)?([a-z']+)", said)
        person_with = _the_person_word(with_someone.group(1)) if with_someone else ""
        if not person_with and with_someone:
            word_with = with_someone.group(1).rstrip("'s")
            if word_with in A_PERSON or word_with.rstrip("s") in A_PERSON \
                    or word_with in PEOPLE_AGED:
                return ("", "they", "them")
        if person_with:
            return (person_with, "she" if person_with in SHE else "he" if person_with in HE else "they",
                    "her" if person_with in SHE else "him" if person_with in HE else "them")
        if re.search(r"\bi(?:'?m| am)\b.*\bin\b", said) or re.match(r"^im\b", said):
            return ("", "you", "you")
        for word in said.split():
            person = _the_person_word(word)
            if person:
                subj = "she" if person in SHE else "he" if person in HE else "they"
                obj = "her" if subj == "she" else "him" if subj == "he" else "them"
                return (person, subj, obj)
        return ("", "they", "them")
    return None


def in_care_pool(text, memory):
    if not memory or not _a_report_on_a_person(text):
        return None
    found = _in_care(memory)
    if not found:
        return None
    word, subj, obj = found
    if not word:
        if subj == "you":
            return IN_CARE_SELF
        return IN_CARE_ASK_UNNAMED
    filled = tuple(line.format(subj=subj, obj=obj, word=word) for line in IN_CARE_ASK)
    return tuple(line for line in filled if "{" not in line and "}" not in line) or IN_CARE_ASK_UNNAMED
