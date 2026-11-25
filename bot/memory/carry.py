import re

from . import repair as a_repair
from . import topics

CONDITION = re.compile(
    r"^(?:but|and|though|although|however|only|except|also|plus|mind you|the thing is|thing is|"
    r"the problem is|problem is|the catch is|my worry is)\b")
MINE = re.compile(r"^(?:im|i'm|i am|i have|i've|ive|i only|i just|i usually|i always|i never|"
                  r"i work|i live|we have|we've|we live|we work|my \w+ is)\b")

A_PLAN = re.compile(r"^(?:going to|gonna|about to|planning to|planning on|off to)\s+"
                    r"(?!be\b|have\b|need\b|want\b)\w")

A_JOB = re.compile(
    r"\b(?:need|needs|have|has|got|want|wants|ought|must)\s+to\s+"
    r"(?:fix|mend|repair|replace|service|sort|clean|build|install|fit|change|bleed|adjust|tune|"
    r"patch|pump|oil|grease)\b")

DECIDING = re.compile(
    r"\b(?:cook|cooking|bake|baking|make|making|eat|eating|dinner|tea|supper|lunch)\b|"
    r"\b(?:thinking (?:of|about)|should i|shall i|do i want|considering|im after|i'?m after|"
    r"im going to|i'?m going to|im about to|i'?m about to|im planning|planning to|"
    r"going to get|i want to get|what should i get|which one|worth it|do i need)\b", re.I)

A_STATE = re.compile(r"^(?:im|i'm|i am|ive|i've)\s+(?:been|felt|feeling|still|not|so|really|"
                     r"like\b)", re.I)

A_DATE = re.compile(r"\b(?:january|february|march|april|may|june|july|august|september|october|"
                    r"november|december|monday|tuesday|wednesday|thursday|friday|saturday|"
                    r"sunday)\b", re.I)

A_FIGURE = re.compile(r"\d|\b(?:one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|"
                      r"twenty|thirty|forty|fifty|sixty|seventy|eighty|ninety|hundred|thousand|"
                      r"half|a few|a couple)\b")

ASKS = re.compile(r"\?|\b(?:can|could|should|would|will|do|does|did|is|are|was|were|what|how|"
                  r"why|when|where|which|who)\b")


def _flat(text):
    return " ".join(str(text or "").split())


def _the_thing_in_hand(text, memory):
    said = _flat(text).lower().rstrip(".")
    seen = []
    record = memory.get("topic")
    if isinstance(record, dict):
        seen.append(record)
    topics_seen = memory.get("topics")
    if isinstance(topics_seen, list):
        seen.extend(other for other in reversed(topics_seen) if isinstance(other, dict))
    for other in seen:
        words = _flat(other.get("text"))
        if not words or words.lower().rstrip(".") == said:
            continue
        thing = a_repair._the_thing_the_last_line_named(words)
        if thing:
            return words, thing
    return None, None


def _a_fresh_memory(memory):
    from ..understanding import understand

    fresh = {"turns": [], "aside": True}
    for key in ("user", "others", "facts_log"):
        if key in memory:
            fresh[key] = memory[key]
    return fresh


def _the_answer_without_the_condition(subject_text, memory):
    from ..modules import answers

    try:
        return answers.respond(subject_text, _a_fresh_memory(memory)) or ""
    except Exception:
        return ""


def _named_in(reply, thing, subject):
    said = _flat(reply).lower()
    if not said:
        return False
    for word in topics.keywords(subject):
        forms = topics.forms(word) or {word}
        if word == thing or topics.alike(word, thing):
            forms = set(forms) | set(topics.forms(thing) or ()) | {thing}
        for form in forms:
            if re.search(r"\b" + re.escape(form) + r"\b", said):
                return True
    return False


def _already_on_the_screen(reply, memory):
    turns = memory.get("turns")
    if not isinstance(turns, list) or not turns:
        return False
    said = _flat(reply).lower()
    opening = " ".join(said.split()[:10])
    if not opening:
        return False
    return any(opening in _flat((turn or {}).get("bot")).lower() for turn in turns)


NOT_A_THING = frozenset((
    "bit", "few", "good", "great", "little", "load", "lot", "many", "moment", "quick", "right",
    "same", "sort", "thing", "time", "while", "whole",
))


A_NAMED_THING = re.compile(
    r"\b(?:a|an|the|my|our|your|his|her|their|another|no|two|three)\s+([a-z][a-z'\-]{2,})")

THE_MOST_THINGS_A_VERDICT_TRIES = 2


def _a_verdict_on_the_other_thing(reply, condition, thing, subject):
    said = _flat(reply).lower()
    if not said:
        return False
    held = [str(word).lower() for word in topics.keywords(subject) or ()]
    for word in A_NAMED_THING.findall(_flat(condition).lower()):
        if word in NOT_A_THING or any(topics.alike(word, one) for one in held):
            continue
        if re.search(r"\b" + re.escape(word) + r"\b", said):
            return True
    return False


def _a_decision_in_the_chat(memory):
    said = []
    for turn in (memory.get("turns") or [])[-6:]:
        if isinstance(turn, dict) and turn.get("user"):
            said.append(str(turn["user"]))
    topic = memory.get("topic")
    if isinstance(topic, dict) and topic.get("text"):
        said.append(str(topic["text"]))
    return any(DECIDING.search(one) for one in said)


VERDICT = re.compile(
    r"\b(?:fair|ok|okay|alright|right|fine|enough|acceptable|reasonable|sensible|safe|legal|\n"
    r"    allowed|normal|typical|usual|weird|rude|polite|necessary|worth|expensive|cheap|\n"
    r"    bad|good|wise|risky|dangerous|healthy|a problem|an issue|a mistake|a good idea|\n"
    r"    a bad idea|too much|too many|too long|too short|too big|too small|too early|too late)\b".replace(
        "\n", ""), re.I)
VERDICT_FILLER = frozenset("""a an the that this it they these those there is are was were be
been being would will shall do does did should can could i we you me us my our your his her their
too so really very quite all then still just much many long short big small early late often
now good bad ok okay fine right thing one to of in on for with get getting have has had if what
how more less time way idea problem issue mistake deal worth going go at as by from up out and
the""".split())
ASKS_A_VERDICT = re.compile(
    r"^(?:is|are|was|were|would|will|shall|do|does|did|should|can|could|have|has)\b", re.I)


def _a_verdict_asked(clean):
    low = clean.lower().strip(" .!")
    if not low or not VERDICT.search(low):
        return False
    if "?" not in clean and not ASKS_A_VERDICT.match(low):
        return False
    for word in re.findall(r"[a-z']+", low):
        if word in VERDICT_FILLER or VERDICT.search(word):
            continue
        return False
    return True


def the_verdict_in_the_chat(text, memory):
    line = _flat(text)
    if len(line.split()) > 8 or not _a_verdict_asked(line):
        return None
    for subject_text, thing, since in _the_things_the_verdict_is_about(memory, line):
        reply = _the_verdict_answer(memory, line, subject_text, thing, since)
        if reply:
            return reply
    return None


def _the_verdict_answer(memory, line, subject_text, thing, since):
    if not subject_text or not thing:
        return None
    from ..modules import answers

    asked = ", ".join([one for one in since if one] + [subject_text, line])
    try:
        reply = answers.respond(asked, _a_fresh_memory(memory))
    except Exception:
        return None
    if not isinstance(reply, str) or not reply.strip():
        return None
    if not _named_in(reply, thing, subject_text):
        return None
    if _already_on_the_screen(reply, memory):
        if not _the_answer_just_given(reply, memory):
            try:
                from . import again as _again
                framed = _again.already_had(reply, memory)
            except Exception:
                framed = None
            if framed:
                return framed
        return None
    return reply.strip()


def _the_answer_just_given(reply, memory):
    turns = memory.get("turns")
    if not isinstance(turns, list) or not turns or not isinstance(turns[-1], dict):
        return False
    mine = _flat(reply).lower()
    last = _flat(turns[-1].get("bot")).lower()
    if not mine or not last:
        return False
    return mine == last or last.startswith(mine) or mine.startswith(" ".join(last.split()[:10]))


def _the_things_the_verdict_is_about(memory, line):
    said = _flat(line).lower().rstrip(".")
    order = []
    for other in _the_lines_of_the_chat(memory):
        words = _flat(other)
        if not words or words.lower().rstrip(".") == said:
            continue
        if order and order[-1].lower().rstrip(".") == words.lower().rstrip("."):
            continue
        order.append(words)
    found = []
    for index in range(len(order) - 1, -1, -1):
        one = order[index]
        thing = _the_thing_they_named(one)
        if thing:
            found.append((one, thing, order[index + 1:]))
            if len(found) >= THE_MOST_THINGS_A_VERDICT_TRIES:
                break
    return found


def _the_thing_they_named(line):
    found = [word for word in A_NAMED_THING.findall(_flat(line).lower())
             if word not in NOT_A_THING and word not in NOT_A_THING_AS_A_MEASURE]
    return found[-1] if found else None


NOT_A_THING_AS_A_MEASURE = frozenset((
    "day", "days", "week", "weeks", "month", "months", "year", "years", "hour", "hours",
    "minute", "minutes", "morning", "afternoon", "evening", "night", "nights", "weekend",
    "time", "times", "while", "moment", "second", "seconds", "chance", "lot", "lotta",
))


def _the_lines_of_the_chat(memory):
    order = []
    turns = memory.get("turns")
    if isinstance(turns, list):
        order.extend((turn or {}).get("user") for turn in turns if isinstance(turn, dict))
    return [one for one in (_flat(line) for line in order) if one]


def the_subject_in_the_condition(text, memory):
    line = _flat(text)
    if not line or ASKS.search(line):
        return None
    found = CONDITION.match(line.lower())
    mine = None
    if not found:
        mine = MINE.match(line.lower())
        if not mine or A_FIGURE.search(line.lower()):
            return None
        if A_STATE.match(line) or A_DATE.search(line):
            return None
        if A_PLAN.match(line.lower()[mine.end():].strip()):
            return None
        found = mine
    if not found:
        return None
    if not _a_decision_in_the_chat(memory):
        return None
    subject_text, thing = _the_thing_in_hand(text, memory)
    if not thing:
        return None
    from ..modules import answers

    condition = line[found.end():].strip(" ,.?!")
    if not condition:
        return None
    if A_JOB.search(condition):
        job_thing = a_repair._the_thing_the_last_line_named(condition)
        if job_thing and job_thing != _flat(thing):
            return None
    ask = "%s, %s" % (condition, subject_text)
    try:
        reply = answers.respond(ask, _a_fresh_memory(memory))
    except Exception:
        return None
    if not isinstance(reply, str) or not reply.strip():
        return None
    held = list(topics.keywords(condition) or ())
    own = _the_answer_without_the_condition(line, memory)
    if own and held and any(re.search(r"\b" + re.escape(word) + r"\b", own.lower())
                            for word in held[-1:]):
        return None
    if not _named_in(reply, thing, subject_text):
        return None
    if _a_verdict_on_the_other_thing(reply, condition, thing, subject_text):
        return None
    if _already_on_the_screen(reply, memory):
        return None
    return reply.strip()


QUALITY_LEAD = re.compile(
    r"^(?:(?:how|hows|what)\s+about\s+(?:a|an\s+)?|how\s+about\s+|whats\s+|what\s+is\s+"
    r"|and\s+|so\s+|ok(?:ay)?\s*,?\s*)*", re.I)
QUALITY_WORDS = frozenset("""
cold warm hot chilled filling fillin light lighter sweet savoury savory salty spicy mild creamy
cheesy quick quickish easy simple healthy fresher fresh veggie vegetarian vegan meaty
fishy hearty substantial summery wintery
""".split())
A_PUDDING = re.compile(r"\b(?:pudding|puddings|pud|dessert|desserts|afters|sweet\s+course)\b", re.I)
A_MEAL = re.compile(r"\b(?:dinner|supper|lunch|brunch|meal|meals|cook|cooking|cooked|"
                    r"bake|baking|baked|recipe|dish|dishes|food|eat|eating|roast|hob|oven|"
                    r"fryer)\b", re.I)


def _the_quality(line):
    said = re.sub(r"\s+", " ", line).strip(" ,.!?").lower()
    if not said:
        return None
    lead = QUALITY_LEAD.match(said)
    if lead:
        said = said[lead.end():].strip(" ,.!?")
    if not said.startswith(("something ", "anything ", "summat ")):
        return None
    words = said.split()
    if len(words) < 2 or len(words) > 4:
        return None
    if any(word not in QUALITY_WORDS for word in words[1:]):
        return None
    return "something " + " ".join(words[1:])


NOT_A_PUDDING = frozenset("spicy savoury salty meaty fishy hearty filling substantial ".split())


def _the_course(memory, quality=""):
    if not isinstance(memory, dict):
        return None
    lines = [str(turn.get("user") or "") for turn in (memory.get("turns") or [])[-4:]
             if isinstance(turn, dict)]
    record = memory.get("topic")
    if isinstance(record, dict):
        lines.append(str(record.get("text") or ""))
    if not lines or not any(line.strip() for line in lines):
        return None
    said = " ".join(lines)
    words = set(str(quality or "").split())
    if A_PUDDING.search(said) and not (words & NOT_A_PUDDING):
        return "pudding"
    if A_MEAL.search(said):
        return "dinner"
    return None


def _is_a_hedge(reply):
    from ..compose import fallback
    try:
        return bool(fallback.is_a_hedge(reply))
    except Exception:
        return False


def the_quality_in_the_chat(text, memory):
    line = _flat(text)
    if not line:
        return None
    quality = _the_quality(line)
    if not quality:
        return None
    course = _the_course(memory, quality)
    if not course:
        return None
    from ..modules import answers

    probe = dict(memory)
    try:
        direct = answers.respond(line, probe)
    except Exception:
        direct = None
    if direct and not _is_a_hedge(direct):
        return None
    ask = "%s for %s" % (quality, course)
    try:
        reply = answers.respond(ask, _a_fresh_memory(memory))
    except Exception:
        return None
    if not isinstance(reply, str) or not reply.strip():
        return None
    if _is_a_hedge(reply):
        return None
    if _already_on_the_screen(reply, memory):
        return None
    return reply.strip()


def _the_last_ask(lines, said):
    for line in reversed(lines):
        words = _flat(line).strip()
        if not words or words.lower().rstrip(".") == said:
            continue
        if len(words.split()) > 14:
            return None
        return words
    return None


FREE_FROM_FOODS = {
    "dairy": ("milk", "cheese", "butter", "cream", "yogurt", "yoghurt", "custard", "ghee",
              "fromage", "kefir", "buttermilk"),
    "gluten": ("bread", "pasta", "flour", "couscous", "barley", "rye", "wheat", "noodle",
               "noodles", "cracker", "pastry"),
    "wheat": ("bread", "pasta", "flour", "couscous", "barley", "noodle", "noodles", "pastry"),
    "nuts": ("almond", "almonds", "cashew", "cashews", "walnut", "walnuts", "pecan", "pecans",
             "hazelnut", "hazelnuts", "pistachio", "pistachios", "peanut", "peanuts",
             "praline", "marzipan"),
    "nut": ("almond", "almonds", "cashew", "cashews", "walnut", "walnuts", "pecan", "pecans",
            "hazelnut", "hazelnuts", "pistachio", "pistachios", "peanut", "peanuts"),
    "peanuts": ("peanut", "peanuts", "groundnut", "satay"),
    "peanut": ("peanut", "peanuts", "groundnut", "satay"),
    "eggs": ("egg", "eggs", "mayonnaise", "meringue", "custard"),
    "egg": ("egg", "eggs", "mayonnaise", "meringue", "custard"),
    "meat": ("chicken", "beef", "pork", "lamb", "bacon", "ham", "sausage", "sausages",
             "mince", "turkey", "chorizo", "steak"),
    "pork": ("bacon", "ham", "sausage", "sausages", "chorizo", "gammon", "prosciutto"),
    "beef": ("steak", "mince", "burger", "burgers", "brisket"),
    "fish": ("salmon", "tuna", "cod", "haddock", "prawn", "prawns", "anchovy", "anchovies",
             "sardine", "sardines", "mackerel", "trout"),
    "shellfish": ("prawn", "prawns", "crab", "mussel", "mussels", "lobster", "scallop",
                  "scallops", "prawn", "squid"),
    "soya": ("soy", "soya", "tofu", "edamame", "tempeh"),
    "soy": ("soy", "soya", "tofu", "edamame", "tempeh"),
    "sugar": ("honey", "syrup", "jam", "chocolate", "biscuit", "cake", "sweets"),
    "salt": ("salted", "crisps", "bacon", "soy", "soya", "stock cube"),
}


def _speaks_of(reply, things):
    said = _flat(reply).lower()
    for thing in things:
        forms = {thing} | set(topics.forms(thing) or ())
        for food in FREE_FROM_FOODS.get(thing.lower(), ()):
            forms |= {food} | set(topics.forms(food) or ())
        for form in forms:
            if form and re.search(r"\b" + re.escape(form) + r"\b", said):
                return True
    return False


FREE_FROM = frozenset("""
dairy gluten wheat nuts nut peanuts peanut eggs egg milk cheese butter cream meat pork beef fish
shellfish soya soy sugar salt spice spices chilli alcohol
""".split())


def _a_free_from(things):
    return all(any(topics.alike(word, known) for known in FREE_FROM) for word in things)


CARRY_STOP = frozenset("""
something anything cook cooking make making tonight dinner lunch tea supper idea ideas meal meals
have want need what can could should recipes recipe please
""".split())


def _the_subject_named(reply, base):
    said = _flat(reply).lower()
    for word in topics.keywords(base):
        if word in CARRY_STOP:
            continue
        for form in {word} | set(topics.forms(word) or ()):
            if form and re.search(r"\b" + re.escape(form) + r"\b", said):
                return True
    return False


def the_limit_in_the_chat(text, memory):
    if not isinstance(memory, dict):
        return None
    said = _flat(text).strip()
    read = memory.get("understood")
    if not isinstance(read, dict) or not read.get("constraint"):
        return None
    things = [str(thing).strip() for thing in (read.get("excludes") or []) if str(thing).strip()]
    if not things or len(said.split()) > 5 or not _a_free_from(things):
        return None
    lines = [str(turn.get("user") or "") for turn in (memory.get("turns") or [])[-3:]
             if isinstance(turn, dict)]
    base = _the_last_ask(lines, said.lower())
    if not base:
        return None
    from ..modules import answers

    asks = ["%s, no %s" % (base, " or ".join(things))]
    subject = [word for word in topics.keywords(base) if word not in CARRY_STOP]
    if subject:
        asks.append("what can i cook with %s, no %s"
                    % (" ".join(subject[:2]), " or ".join(things)))
    for ask in asks:
        try:
            reply = answers.respond(ask, _a_fresh_memory(memory))
        except Exception:
            continue
        if not isinstance(reply, str) or not reply.strip():
            continue
        if _is_a_hedge(reply) or _already_on_the_screen(reply, memory):
            continue
        if _speaks_of(reply, things):
            if not _cooks_around_it(reply):
                continue
        elif not _the_subject_named(reply, base):
            continue
        return reply.strip()
    return None


COOKS_AROUND_IT = re.compile(
    r"\b(?:in place of|instead of|swap(?:ped)?|replace|leave (?:it|that|them) out|"
    r"free[- ]from|free of|\w+[- ]free\b|without\b|use more|go easy on)\b")


def _cooks_around_it(reply):
    return bool(COOKS_AROUND_IT.search(_flat(reply).lower()))
