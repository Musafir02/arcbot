
import re
import string

from ..compose import pick

LEAD_IN = re.compile(r"^(?:ok(?:ay)?|so|right|well|then|hmm|oh|and|but)[, ]+", re.I)

SETTLING = (
    re.compile(r"^(?:(?:actually|instead|in the end|in that case|on second thoughts?|"
               r"on second thought)[,]?\s+)(?P<what>.+)$"),
    re.compile(r"\b(?:i|we|i've|ive|we've|weve)\s+(?:have\s+|had\s+)?(?:decided|settled)\s+"
               r"(?:on|for)?\s*(?P<what>.+)$"),
    re.compile(r"\b(?:i|we)\s+(?:picked|chose|landed on|ended up with)\s+(?P<what>.+)$"),
    re.compile(r"\b(?:i|we)\s+(?:go|went|goes)\s+with\s+(?P<what>.+)$"),
)

GOING = (
    re.compile(r"\b(?:i'?m|im|i am|we'?re|were)\s+(?:going|gonna)\s+(?:with|for)\s+"
               r"(?P<what>.+)$"),
    re.compile(r"\b(?:i'?m|im|i am|we'?re|were)\s+going to\s+go\s+(?:with|for)\s+"
               r"(?P<what>.+)$"),
)

ACTIVITY = frozenset("""run jog walk stroll hike swim shower bath drive ride cycle coffee
    drink pint curry dinner lunch breakfast supper nap kip sleep sit look wander shop shopping
    haircut massage break rest smoke fag wee pee leak""".split())
CORRECTING_LINE = (
    re.compile(r"^(?:no|nah|nope)[,:]\s*(?:i mean(?:t)?[, ]+)?(?P<what>.+)$"),
    re.compile(r"^(?:no|nah|nope)\s+i mean(?:t)?[, ]+(?P<what>.+)$"),
)
CHOOSING = (
    re.compile(r"\b(?:lets|let's|i'?ll|ill|we'?ll|well|i'?m going to|im going to|i'?m gonna|"
               r"im gonna|we'?re going to|were going to)\s+"
               r"(?:go|going|get|getting|have|having|take|taking|do|doing|pick|picking|choose|"
               r"choosing|book|booking|buy|buying)\s+(?:with|for)?\s*(?P<what>.+)$"),
    re.compile(r"\b(?:i|we)\s+went for\s+(?P<what>.+)$"),
    re.compile(r"^(?P<what>.{2,40}?),?\s+i (?:think|reckon|suppose)$"),
    re.compile(r"^(?P<what>(?:a|an|the|some)\s+[\w'’-]+(?:\s+[\w'’-]+)?)$"),
    re.compile(r"\bmake it\s+(?P<what>.+)$"),
    re.compile(r"\b(?:lets|let's|i'?ll|ill|we'?ll|well|i will|we will)\s+"
               r"(?:take|do|have)\s+(?P<what>.+)$"),
    re.compile(r"\b(?:i|we)\s+said\s+(?P<what>.+)$"),
)

OPTIONS = re.compile(r"\bor\b|\bbetween\b|\btorn\b|\bthinking of\b|\bthinking about\b|"
                     r"\bweighing up\b|\bshould i\b|\beither\b|\bwhich one\b|"
                     r"\bdecid(?:e|ed|ing)\b|cannot decide|can'?t decide|\bchoose\b|"
                     r"\bchoices?\b|\boptions\b|\bhelp me pick\b|\bvs\b", re.I)

NOT_A_THING = frozenset("""
i im i'm we we're you you're it its it's that this which what who they he she there here
me my our your his her their is are am was were do does did dont don't doesnt didn't
""".split())

CLAUSE_CHOICE = re.compile(
    r"^(?:actually|instead|in the end|turns out|it turns out)[,]?\s+"
    r"(?:i|we)(?:'ve|ve|'d|d)?\s+(?:have\s+|had\s+|just\s+)?"
    r"(?:booked|bought|got|ordered|chosen|chose|picked|reserved|taken|took|signed up for|"
    r"settled on|decided on|gone with|went with|landed on)\s+(?P<what>.+)$", re.I)

CORRECTING = re.compile(r"^(?:no|nah|nope|i mean|i meant|wait|sorry)[, ]+", re.I)

TAIL = re.compile(r"\s+(?:instead|after all|i think|i reckon|i suppose|then|actually|"
                  r"last night|last week|yesterday|today|this morning)$", re.I)

IDIOM = frozenset(
    ["the flow", "the grain", "the crowd", "thank you", "thanks", "the rest"]
    + """it that this them worries way idea chance problem doubt quick fast work happen up right
    better worse soon now snappy official count brief short clear easy fun nice worth cheaper
    bigger smaller louder quieter sense money""".split())

MOST_WORDS = 4

ASK = re.compile(
    r"\bwhat (?:did|do|have|had) (?:i|we) (?:decide|decided|settle(?:d)? on|choose|chose|"
    r"pick|picked|go for|went for|end up with)\b"
    r"|\bwhat (?:am|are) (?:i|we) (?:getting|going with|going for|ending up with|having)\b"
    r"|\bwhich (?:one|of (?:them|those))? (?:did (?:i|we) (?:pick|choose|go for|decide|"
    r"settle on|go with|end up with)|(?:am|are) (?:i|we) (?:getting|going with))\b"
    r"|\bwhich (?:one|of (?:them|those)) (?:i|we) (?:picked|chose|went with|went for|settled on|"
    r"decided on)\b"
    r"|\bwhere did (?:i|we) (?:decide|settle) (?:to go|on)\b"
    r"|\bso what (?:am|are) (?:i|we) (?:getting|going with|doing)\b"
    r"|\bwhat (?:i|we) (?:decided|chose|picked|settled on|went with|went for)\b"
    r"|\b(?:have|has|had|did) (?:i|we) (?:decide|decided|picked|chosen|chose|settled)\b"
    r"|\bare (?:we|you) decided\b"
    r"|\bwhat was (?:decided|chosen|picked|settled on)\b"
    r"|\bwhat (?:did|do) (?:i|we) (?:land|opt) (?:on|for)\b"
    r"|\bwhich did (?:i|we) (?:go for|pick|choose|decide on|settle on)\b"
    r"|\bwhat did (?:i|we) say (?:i|we)(?:'d| would) (?:get|choose|pick|go for|have)\b"
    r"|\bremind me (?:of|about) (?:the|our) choice\b"
    r"|\bdid (?:i|we) (?:go with|go for|settle on|pick|choose|decide on|end up with)\b")

GUESSING_ASK = re.compile(
    r"\bdid (?:i|we) (?:go with|go for|settle on|pick|choose|decide on|end up with)\s+"
    r"(?P<what>[^?.!,]+)", re.I)

TO_YOU = {"i": "you", "im": "you're", "i'm": "you're", "me": "you", "my": "your",
          "mine": "yours", "myself": "yourself", "we": "you", "our": "your", "ours": "yours",
          "ive": "you've", "i've": "you've"}


INNER_DECIDE = re.compile(
    r"^(?:i|we)(?:'ve|'d|ve|d| have| had)?\s+(?:decided|settled|chosen|chose|picked|gone|"
    r"went|going|go)\b\s*(?:on|with|for)?\s*", re.I)


def _the_thing(phrase):
    phrase = " ".join(str(phrase or "").split()).strip(" ,.;:!?")
    while True:
        trimmed = CORRECTING.sub("", phrase).strip(" ,.;:!?")
        if trimmed == phrase:
            break
        phrase = trimmed
    while True:
        trimmed = INNER_DECIDE.sub("", phrase).strip(" ,.;:!?")
        if trimmed == phrase:
            break
        phrase = trimmed
    while True:
        trimmed = TAIL.sub("", phrase).strip(" ,.;:!?")
        if trimmed == phrase:
            break
        phrase = trimmed
    if phrase.lower() in IDIOM:
        return None
    if re.fullmatch(r"[\d.,]+", phrase):
        return None
    words = phrase.split()
    verb_phrase = len(words) > 1 and words[0].lower() == "to"
    if not words or len(words) > (MOST_WORDS + 4 if verb_phrase else MOST_WORDS):
        return None
    if words[0].lower() in NOT_A_THING:
        return None
    if any(word.lower() in NOT_A_THING for word in words[1:]):
        return None
    return phrase


OPTION_FILLER = frozenset("""im i we you they should shall do does did get gets getting got
    go goes going gonna want wants wanted need needs like rather prefer thinking thought
    about of between torn pick picking choose choosing decide decided deciding help me if
    maybe well so and then also still just were was are is am been being cant can't cannot
    unsure whether if better best worse worth it to up weighing""".split())


def _two_things(said):
    low = " ".join(str(said or "").lower().split()).strip(" ?.!,")
    left = right = ""
    if " between " in low and " and " in low.split(" between ", 1)[1]:
        head = low.split(" between ", 1)[1]
        left, right = head.split(" and ", 1)
    elif " or " in low:
        cut = low.rfind(" or ")
        left, right = low[:cut], low[cut + 4:]
    else:
        return None
    left_words = left.split()
    while left_words and left_words[0].strip(",;:") in OPTION_FILLER:
        left_words.pop(0)
    right_words = right.split()[:3]
    while right_words and right_words[-1].strip(",;:") in OPTION_FILLER:
        right_words.pop()
    left = " ".join(left_words[-3:]).strip(" ,;:")
    right = " ".join(right_words).strip(" ,;:")
    if not left or not right:
        return None
    if left in IDIOM or right in IDIOM or left in NOT_A_THING or right in NOT_A_THING:
        return None
    return left + " or " + right


def _options_since(memory, line):
    turns = list((memory or {}).get("turns") or [])
    key = " ".join(str(line or "").lower().split())
    if not key:
        return None
    seen = False
    for turn in reversed(turns[-6:]):
        said = " ".join(str((turn or {}).get("user") or "").split())
        if not said:
            continue
        if said.lower() == key:
            seen = True
            break
        if asks(said) or not OPTIONS.search(said):
            continue
        pair = _two_things(said)
        if pair:
            return pair
    return None


def _the_pair_left_open(memory):
    for turn in reversed(list((memory or {}).get("turns") or [])[-3:]):
        said = str((turn or {}).get("user") or "")
        if not said or asks(said) or not OPTIONS.search(said):
            continue
        pair = _two_things(said)
        if pair:
            return pair
    return None


def _as_typed(text, thing):
    words = thing.split()
    if not words:
        return thing
    pattern = r"\b" + r"\s+".join(re.escape(word) for word in words) + r"\b"
    match = re.search(pattern, str(text or ""), re.I)
    return match.group(0) if match else thing


def read(text):
    line = " ".join(str(text or "").lower().split())
    if not line or "?" in line or len(line.split()) > 14:
        return None
    if asks(line):
        return None
    while True:
        trimmed = LEAD_IN.sub("", line)
        if trimmed == line:
            break
        line = trimmed
    clause = CLAUSE_CHOICE.search(line)
    if clause:
        thing = _the_thing(clause.group("what"))
        if thing and not _an_activity(thing):
            return {"what": _as_typed(text, thing), "settled": True}
    for pattern in CORRECTING_LINE:
        match = pattern.search(line)
        if match:
            thing = _the_thing(match.group("what"))
            if thing:
                return {"what": _as_typed(text, thing), "settled": False, "corrects": True}
    for pattern in GOING:
        match = pattern.search(line)
        if not match:
            continue
        thing = _the_thing(match.group("what"))
        if thing and not _an_activity(thing):
            return {"what": _as_typed(text, thing), "settled": True}
    for patterns, settled in ((SETTLING, True), (CHOOSING, False)):
        for pattern in patterns:
            match = pattern.search(line)
            if not match:
                continue
            thing = _the_thing(match.group("what"))
            if thing:
                return {"what": _as_typed(text, thing), "settled": settled}
    return None


def extract(text):
    reading = read(text)
    return reading["what"] if reading else None


def _an_activity(thing):
    words = [w.strip(" ,.;:!?").lower() for w in str(thing or "").split()]
    while words and words[0] in ("a", "an", "the", "some", "my", "our"):
        words = words[1:]
    return bool(words) and words[0] in ACTIVITY


def _a_bare_thing(said):
    line = " ".join(str(said or "").lower().split()).strip(" ,.;:!?")
    if not line or "?" in line:
        return False
    words = line.split()
    if len(words) > 2 or any(w in NOT_A_THING for w in words):
        return False
    return all(w.isalpha() for w in words) and len(words[-1]) > 2


def _options_on_the_table(memory):
    for turn in reversed(list((memory or {}).get("turns") or [])[-2:]):
        said = str((turn or {}).get("user") or "")
        if str((turn or {}).get("bot") or "") and not said:
            continue
        if _a_bare_thing(said):
            return True
        if asks(said):
            continue
        if OPTIONS.search(said):
            return True
    return False


REACHES_FOR_A_CHOICE = re.compile(
    r"\b(?:go|goes|going|went)\s+(?:with|for)\b"
    r"|\b(?:settled|decided|landed|ended up)\s+(?:on|for|with)\b"
    r"|\b(?:(?:going|gonna)\s+to\s+)?(?:take|taking|took|book|booking|pick|picked|choose|"
    r"chose|choosing)\s+(?:the|a|an|my|that|this)\b"
    r"|\b(?:picked|chose|choosing)\b", re.I)


OPENING_QUESTION = re.compile(r"^(?:is|are|was|were|should|shall|do|does|did|can|could|would|"
                              r"will|what|which|how|where|when|why|any|if)\b", re.I)


def _a_choice_reached_for(memory, kept_line=None):
    for turn in reversed(list((memory or {}).get("turns") or [])[-3:]):
        said = " ".join(str((turn or {}).get("user") or "").split())
        if not said or asks(said):
            continue
        if "?" in said or OPENING_QUESTION.match(said):
            continue
        if kept_line and said.lower() == str(kept_line).lower():
            return False
        return bool(REACHES_FOR_A_CHOICE.search(said))
    return False


DECIDING_WORD = re.compile(r"\b(?:decid|settl|pick|cho(?:o|s)|decided|deciding)\w*", re.I)


def _a_plan_since(memory):
    for turn in reversed(list((memory or {}).get("turns") or [])[-3:]):
        said = " ".join(str((turn or {}).get("user") or "").split())
        if not said or asks(said) or "?" in said:
            continue
        for pattern in GOING:
            match = pattern.search(said.lower())
            if match:
                return bool(_an_activity(_the_thing(match.group("what")) or ""))
        return False
    return False


def observe(text, memory):
    reading = read(text)
    if not reading or not isinstance(memory, dict):
        return None
    if reading.get("corrects") and not (the_decision(memory) or _options_on_the_table(memory)):
        return None
    if not reading["settled"] and not reading.get("corrects") and not _options_on_the_table(memory):
        return None
    memory["decided"] = {"what": reading["what"],
                          "line": " ".join(str(text or "").lower().split())}
    return memory["decided"]


PLAN_KEYS = ("plans", "plan")


def _the_plan_on_record(memory):
    user = (memory or {}).get("user") if isinstance(memory, dict) else None
    if not isinstance(user, dict):
        return None
    plans = [user.get("plan")] if user.get("plan") else []
    if isinstance(user.get("plans"), list):
        plans = list(user["plans"]) + plans
    for plan in reversed([p for p in plans if p]):
        plan = " ".join(str(plan or "").split())
        words = [w for w in plan.lower().replace(",", " ").split() if len(w) > 2]
        if words and said_back(memory, words):
            return plan
    return None


def said_back(memory, words):
    for turn in list((memory or {}).get("turns") or []):
        said = str((turn or {}).get("bot") or "").lower()
        if said and all(w in said for w in words):
            return True
    return False


def the_decision(memory):
    held = (memory or {}).get("decided") if isinstance(memory, dict) else None
    if isinstance(held, dict) and str(held.get("what") or "").strip():
        return held
    return None


def asks(text):
    low = " ".join(str(text or "").lower().split())
    return bool(ASK.search(low))


def the_guess(text):
    low = " ".join(str(text or "").lower().split()).strip(" ?.!,")
    match = GUESSING_ASK.search(low)
    if not match:
        return None
    return _the_thing(match.group("what"))


def _the_same_thing(said, held):
    one = " ".join(str(said or "").lower().split()).strip(" ?.!,")
    other = " ".join(str(held or "").lower().split()).strip(" ?.!,")
    if not one or not other:
        return False
    if one.startswith("to "):
        one = one[3:]
    if other.startswith("to "):
        other = other[3:]
    if one == other or one in other or other in one:
        return True
    first, second = one.split(), other.split()
    if len(first) > 2 and len(second) > 2 and first[1:] == second[1:]:
        verb_one, verb_two = first[0], second[0]
        return len(verb_one) > 2 and len(verb_two) > 2 and verb_one[:3] == verb_two[:3]
    return False


def _said_to_you(thing):
    words = []
    for word in str(thing or "").split():
        bare = word.strip(".,!?;:")
        swapped = TO_YOU.get(bare.lower())
        words.append(swapped if swapped else word)
    return " ".join(words)


def _a_verb_phrase(thing):
    words = str(thing or "").split()
    return len(words) > 1 and words[0].lower() == "to"


def _the_choice_said(thing):
    if _a_verb_phrase(thing):
        return "You decided " + thing + "."
    return "You went with " + thing + "."


def _at_the_start(thing):
    return thing[:1].upper() + thing[1:] if thing else thing


ASK_FRAME = frozenset("""what which one ones did do does have has had i we you me us my our
    decide decided deciding settle settled settling on choose chose chosen pick picked picking
    go went going for get gets getting got have having take took end ended up with am are was
    were so about of to the a an it that this them those remind remember again the choice
    our land landed opt opted for say said would will should and then there where when why
    how who whose much many long kind sort time place""".split())

NOT_A_SUBJECT = frozenset("""one ones one's best better worse right thing things way again now
    then really please just also still ever again""".split())

DOING = frozenset("""make makes made making cook cooks cooked cooking eat eats eating drink
    drinks drinking buy buys buying wear wears wearing watch watches watching learn learns
    learning study studies studying grow grows growing plant plants planting build builds
    building serve serves serving""".split())

COMPANION_VERBS = frozenset("""drink drinks drinking serve serves serving have has having
    order orders ordering pair pairs pairing pour pours pouring""".split())
COMPANION = re.compile(r"\b(?:%s)\s+(?:with|alongside)\b" % "|".join(sorted(COMPANION_VERBS)))


def _asks_about_another_thing(text, held):
    said = " ".join(str(text or "").lower().split())
    held_text = " ".join(str((held or {}).get("what") or "").lower().split())
    if COMPANION.search(said):
        return True
    words = [w.strip(string.punctuation) for w in said.split()]
    named = [w for w in words
             if w and w not in ASK_FRAME and w not in NOT_A_SUBJECT and w not in DOING
             and len(w) > 2 and not w.isdigit()]
    if not named:
        return False
    return not any(w in held_text or (len(w) > 3 and held_text.startswith(w[:4]))
                   for w in named)


def answer(text, memory):
    if not asks(text):
        return None
    held = the_decision(memory)
    if held:
        moved_on = _options_since(memory, held.get("line"))
        if moved_on and not _a_choice_reached_for(memory, held.get("line")):
            return pick(["Nothing settled yet: " + moved_on + ".",
                         "Not yet: " + moved_on + ".",
                         "Neither one yet: " + moved_on + "."], memory,
                        seed_text=str(text or ""))
    if held and not the_guess(text) and _asks_about_another_thing(text, held):
        return None
    if held and _a_choice_reached_for(memory, held.get("line")):
        return None
    if not held:
        if _asks_about_another_thing(text, held) and not the_guess(text):
            return None
        plan = _the_plan_on_record(memory)
        if (plan and DECIDING_WORD.search(str(text or ""))
                and not _asks_about_another_thing(text, {"what": plan})):
            return pick(["You settled on " + plan + ".",
                         "That's settled: " + plan + ".",
                         "The chat settled it: " + plan + "."], memory,
                        seed_text=str(text or ""))
        if _a_choice_reached_for(memory):
            if not (DECIDING_WORD.search(str(text or "")) and _a_plan_since(memory)):
                return None
        pair = _the_pair_left_open(memory)
        if pair:
            return pick(["Nothing settled yet: " + pair + ".", "Not yet: " + pair + ".",
                         "Neither one yet: " + pair + "."], memory,
                        seed_text=str(text or ""))
        return pick(["Nothing settled yet.", "You haven't picked one yet.",
                     "You haven't settled on one yet."], memory,
                    seed_text=str(text or ""))
    thing = _said_to_you(held.get("what"))
    guess = the_guess(text)
    if _a_verb_phrase(held.get("what")):
        if guess:
            if _the_same_thing(guess, held.get("what")):
                return pick(["That's right: you decided " + thing + ".",
                             "Yes - you decided " + thing + "."],
                            memory, seed_text=str(text or ""))
            return pick(["Not quite: you decided " + thing + ".",
                         "The other one: you decided " + thing + "."],
                        memory, seed_text=str(text or ""))
        return pick(["You decided " + thing + ".",
                     "You decided " + thing + ", in the end."],
                    memory, seed_text=str(text or ""))
    if guess:
        if _the_same_thing(guess, held.get("what")):
            return pick(["Yes - " + thing + ", in the end.",
                         "That's right: " + thing + ".",
                         "Yes, " + thing + "."],
                        memory, seed_text=str(text or ""))
        return pick(["No - " + thing + ", in the end.",
                     "Not quite: " + thing + ", in the end.",
                     "The other one: " + thing + "."],
                    memory, seed_text=str(text or ""))
    return pick([_at_the_start(thing) + ", in the end.",
                 "You settled on " + thing + ".",
                 _the_choice_said(thing)],
                memory, seed_text=str(text or ""))
