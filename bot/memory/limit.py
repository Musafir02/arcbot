import re

from ..understanding import understand as understanding
from ..compose import pick
from . import topics, tried

OUT_OF = re.compile(
    r"\b(?:i|we)(?:\s*(?:have|'ve|ve|had|'m|'re|am|are))?\s*(?:just\s+|now\s+|actually\s+)?"
    r"(?:ran out of|run out of|ran outta|am out of|are out of|m out of|'m out of|'re out of|"
    r"re out of|out of)\s+"
    r"(?:any\s+|a\s+|an\s+)?(?P<thing>[a-z][a-z' -]{1,24})"
    r"|\b(?:no|without)\s+(?:a\s+|an\s+|any\s+)?(?P<thing3>[a-z][a-z' -]{1,24})",
    re.I)

NOT_HAVE = re.compile(
    r"\b(?:i|we)\s+(?:(?:do|did|have)\s+not|do\s*n'?t|don'?t|dont|did\s*n'?t|didnt|"
    r"haven'?t|havent|hadn'?t|hadnt)\s+(?:(?:got|have|own|any)\s+)?"
    r"(?:any\s+|a\s+|an\s+)?(?P<thing2>[a-z][a-z' -]{1,24})", re.I)

A_DETAIL_OF_THE_FAULT = re.compile(r"^(?:(?:hot|cold|running)\s+water)$", re.I)

A_HEATING_FAULT = re.compile(
    r"boiler|heating|radiator|combi|immersion|cylinder|pilot light|"
    r"water pressure|thermostat", re.I)

A_LEAKING_FAULT = re.compile(
    r"leak|drip|burst|pour|flood|water everywhere|water coming|spray|seep|smok|fume|soot|"
    r"flame|on fire", re.I)

NOT_A_THING = re.compile(
    r"\b(?:idea|clue|time|money|the foggiest|chance|choice|room|option|ants anymore|anymore|"
    r"any more|no more|a life|a job|job|work|a car|"
    r"way|luck|bother|worries|worry|problem|doubt|wonder|rush|need|joke|point|sense|harm|"
    r"thanks|matter)\b", re.I)

IN_THE_HOUSE_WORDS = (r"cat|cats|kitten|kittens|dog|dogs|puppy|puppies|rabbit|rabbits|"
                       r"hamster|hamsters|guinea pig|budgie|parrot|tortoise|child|children|kid|"
                       r"kids|toddler|baby|son|daughter")
IN_THE_HOUSE = re.compile(
    r"\b(?:(?:i|we)(?:\s+have|'ve|ve|got)?\s+(?:got\s+|have\s+)?(?:a|an|two|three|our|my)\s+"
    r"(?P<who>" + IN_THE_HOUSE_WORDS + r")\b"
    r"|(?:there'?s|theres)\s+(?:a|an)\s+(?P<who2>" + IN_THE_HOUSE_WORDS + r")\s+"
    r"(?:in the house|here|at home))", re.I)

ALSO_THERE = re.compile(r"\s*(?:,|and|plus)\s+(?:a|an|the|my|our|two)\s+(?P<who3>"
                        + IN_THE_HOUSE_WORDS + r")\b", re.I)

NOT_WITH_A_PET = re.compile(
    r"\b(?:bait|baits|baited|poison|poisoned|pellets?|killer|insecticide|rodenticide|"
    r"spring ?traps?|mousetraps?|rat traps?|glue ?boards?|ant powder|ant spray|blue grains)\b",
    re.I)


ASKS = re.compile(r"\?|\b(?:how|what|why|when|which|should|can|could|would|do i|is there)\b", re.I)

ASKS_A_CHOICE = re.compile(
    r"\b(?:ideas?|dinners?|meals?|lunches?|suppers?|breakfasts?|recipes?|suggestions?)\b", re.I)

CLAUSE_STARTS = frozenset("""i im i'm ive iv we you it its it's that this there they he she
    meant mean wants want wanted needs need think thought know knew said say says told ask asked
    just really actually yes no thanks sorry""".split())

STEP = re.compile(
    r"^(?:start|begin|use|put|place|leave|let|keep|wipe|rub|mix|make|add|take|coat|scrub|brush|"
    r"soak|pour|drain|wash|rinse|blot|hang|air|open|close|undo|unscrew|pull|lift|fill|top|cut|"
    r"trim|cover|seal|spray|check|turn|hold|run|go|get|do|give|ask|book|call|wait|set|sit|"
    r"stand|watch|pick|dig|move|remove|replace|clean|unplug|vacuum|sweep|boil|simmer|bake|"
    r"rest|chill|store|freeze|test|look|try|screw|tighten|loosen|slide)\b", re.I)

AND_STEP = re.compile(
    r"\s+(?:and|then|so|but)\s+(?=(?:start|begin|use|put|place|leave|let|keep|wipe|rub|mix|make|"
    r"add|take|coat|scrub|brush|soak|pour|drain|wash|rinse|blot|hang|air|open|close|undo|unscrew|"
    r"pull|lift|fill|top|cut|trim|cover|seal|spray|check|turn|hold|run|go|get|do|give|ask|book|"
    r"call|wait|set|sit|stand|watch|pick|dig|move|remove|replace|clean|unplug|vacuum|sweep|boil|"
    r"simmer|bake|rest|chill|store|freeze|test|look|try|screw|tighten|loosen|slide)\b)", re.I)

LEADS = {"pet": "With {who} in the house, "}

LONGEST = 9

def words_of(text):
    return re.findall(r"[a-z']+", str(text or "").lower())


A_FAULT_IN_A_NAMED_THING = re.compile(
    r"\b(?:my|our|the|his|her|their|your|its|this|that|these|those)\s+"
    r"[a-z][a-z'-]*(?:\s+[a-z][a-z'-]*){0,2}\s+"
    r"(?:has|have|had|'s|is|are|was|were|gets?|got|does|do|keeps?|comes?|shows?|gives?|"
    r"leaves?|makes?|runs?)\s+$", re.I)


def _a_fault_in_the_thing(said, found):
    return bool(A_FAULT_IN_A_NAMED_THING.search(str(said or "")[:found.start()]))


def _shown(match):
    for group in ("thing", "thing2", "thing3"):
        if match.groupdict().get(group):
            raw = " ".join(match.group(group).split())
            said = re.sub(r"\s+(?:left|anyway|though|tho|either|now|anymore|for that|for it)$",
                          "", raw, flags=re.I).strip(" .,!?;:'\"")
            said = re.split(r"\s+(?:but|and|though|although|because|so|unless|whereas)\s+"
                            r"(?=(?:i|we|you|they|it|there|he|she)\b)", said, flags=re.I)[0]
            said = _without_a_reason(said)
            said = said.strip(" .,!?;:'\"")
            said = WHERE_IT_IS.sub("", said).strip(" .,!?;:'\"")
            return said, _bare(said), raw
    return "", "", ""


A_REASON = re.compile(r"\s+(?:because|cos|coz|cus|coz of|cos of|because of|seeing as)\b.*$", re.I)

WHERE_IT_IS = re.compile(r"\s+(?:in|at|on)\s+(?:the|my|our)\s+[a-z]+(?: [a-z]+)?$", re.I)


def _without_a_reason(said):
    return A_REASON.sub("", said).strip(" .,!?;:'\"")


A_PET_IN_THE_REASON = re.compile(
    r"\b(?:because|cos|coz|cus|since|with|of)\s+(?:it'?s\s+)?(?:the|my|our|a|an)\s+(?P<who>"
    + IN_THE_HOUSE_WORDS + r")\b", re.I)


def _a_pet_in_the_reason(said, found):
    rest = str(said or "")
    hit = A_PET_IN_THE_REASON.search(rest)
    return hit.group("who") if hit else ""


def _bare(said):
    words = [word for word in said.split() if word.lower() not in
             ("the", "a", "an", "any", "some", "my", "our", "of", "it")]
    return " ".join(words) or said


def _the_read(said, memory):
    read = (memory or {}).get("understood")
    if isinstance(read, dict) and " ".join(str(read.get("text") or "").split()).strip(" .,!;:") == said:
        return read
    return understanding(said, {}) or {}


def reads_as_a_limit(text, memory=None):
    said = " ".join(str(text or "").split()).strip(" .,!;:")
    if not said or len(words_of(said)) > LONGEST:
        return None
    if "recommend" in (_the_read(said, memory).get("asks") or ()):
        return None
    for kind, pattern in (("ran_out", OUT_OF), ("not_have", NOT_HAVE), ("pet", IN_THE_HOUSE)):
        found = pattern.search(said)
        if not found:
            continue
        if kind == "pet":
            who = _everyone_in_the_house(said, found)
            return ("pet", who, who)
        if ASKS.search(said.replace(found.group(0), " ")):
            return None
        if ASKS_A_CHOICE.search(said.replace(found.group(0), " ")):
            return None
        if _a_fault_in_the_thing(said, found):
            return None
        shown, bare, raw = _shown(found)
        if raw and raw.split()[0].lower().strip(".,!") in CLAUSE_STARTS:
            return None
        if re.search(r"\b(?:is|are|was|were|isn'?t|aren'?t)\b", bare or "", re.I):
            return None
        if not bare or NOT_A_THING.search(bare) or NOT_A_THING.search(raw):
            return None
        if ASKS.search(bare):
            return None
        who = _a_pet_in_the_reason(said, found)
        if who:
            answer = _last_answer(memory)[0] if isinstance(memory, dict) else ""
            if answer and NOT_WITH_A_PET.search(answer):
                said_as = who if who.endswith("s") or who == "children" else "a " + who
                return ("pet", said_as, said_as)
        return (kind, shown, bare)
    return None


_MOVE_WORDS = frozenset("""
tiring strenuous energetic demanding exhausting exhaustive walking walk walks hike hikes hiking
hill hills stair stairs steps standing stand climbing climb lifting lift far long running run
cycling cycle bike bikes swimming swim carrying carry bending bend kneeling kneel squat squats
""".split())
_LIMIT_FRAME = frozenset("""
no not nothing never nowt without too very much any more most lot lots really just only still
cant cannot can can't able manage do does did done get gets up down and or but the a an my our
your his her its it that this those these there here of for in on at with to i we im me us
be being is are was were have has had about even anymore either please thanks
""".split())


_LEAVES_IT_OUT = re.compile(r"^(?:and |also |but |so |then )*(?:no|nothing|not|never|nowt|without)\b",
                            re.I)


def only_a_limit(text, memory=None):
    try:
        from .facts import a_limit_on_the_plan
    except Exception:
        return False
    said = " ".join(str(text or "").split()).strip(" .,!;:")
    if not said or len(words_of(said)) > LONGEST:
        return False
    if not _LEAVES_IT_OUT.match(said):
        return False
    try:
        if a_limit_on_the_plan(said) != "move":
            return False
    except Exception:
        return False
    words = [word.strip("'") for word in re.findall(r"[a-z']+", said.lower())]
    return bool(words) and all(word in _MOVE_WORDS or word in _LIMIT_FRAME for word in words)


def _everyone_in_the_house(line, found):
    names = [found.groupdict().get("who") or found.groupdict().get("who2") or ""]
    rest = line[found.end():]
    while True:
        more = ALSO_THERE.match(rest)
        if not more:
            break
        names.append(more.group("who3"))
        rest = rest[more.end():]
    seen, out = set(), []
    for name in names:
        name = " ".join(name.split())
        if not name or name.lower() in seen:
            continue
        seen.add(name.lower())
        out.append(name if name.endswith("s") or name in ("children",) else "a " + name)
    return " and ".join(out)


def _pieces(answer):
    pieces = []
    for sentence in re.split(r"(?<=[.!?])\s+", str(answer or "")):
        sentence = sentence.strip()
        if not sentence:
            continue
        clauses = [clause.strip() for clause in re.split(r",\s+(?=[a-z])", sentence) if clause.strip()]
        pieces.append((sentence, clauses))
    return pieces


def _steps(answer):
    out = []
    for sentence, clauses in _pieces(answer):
        for clause in clauses:
            for step in re.split(AND_STEP, clause):
                step = step.strip(" .,;:")
                if step:
                    out.append((step, sentence))
    return out


JOINING = frozenset("of the a an my your our their its some any".split())


def _names(clause, thing):
    forms = topics.forms(thing)
    words = set(words_of(clause))
    if forms & words:
        return True
    want = [word for word in words_of(thing) if word not in JOINING]
    if len(want) < 2:
        return False
    got = [word for word in words_of(clause) if word not in JOINING]
    for start in range(len(got) - len(want) + 1):
        window = got[start:start + len(want)]
        if all(one == other or one in topics.forms(other)
               for one, other in zip(window, want)):
            return True
    return False


def _first_with(answer, thing):
    for clause, _ in _steps(answer):
        if _names(clause, thing):
            return clause
    return ""


SAID_OF_IT = re.compile(
    r"\b(?:is|are|was|were|be|been|has|have|had|does|do|did|will|can|makes?|keeps?|works?|"
    r"takes?|needs?|gives?|goes|go|comes?|gets?|stays?|holds?|sits?|starts?|ends?|means?|"
    r"sounds?|clears?|pulls?|dries?|helps?|turns?|leaves?|leaving|adding|mixing|cooks?|"
    r"removes?|kills?|stops?|lasts?)\b", re.I)


MEASURED = re.compile(
    r"\b\d+(?:[.,]\d+)?\s*(?:g|kg|ml|l|cl|oz|lb|grams?|kilos?|litres?|millilitres?|"
    r"tbsp|tsp|tablespoons?|teaspoons?|cups?|pints?|pinch(?:es)?|handfuls?)\b", re.I)
MEASURED_PARTS = re.compile(r",|\band\b", re.I)


AN_AMOUNT = frozenset("""
weight amount quantity part parts half quarter third fifth pinch splash dash drizzle
spoonful spoon spoons tablespoon tablespoons tbsp teaspoon teaspoons tsp cup cups gram grams g kg
ml litre litres ounce ounces oz pound pounds lb handful knob
""".split())


def _the_amount_of_it(clause, thing):
    words = words_of(clause)
    wanted = set(words_of(thing)) - JOINING
    for place, word in enumerate(words):
        if word not in wanted:
            continue
        before = words[max(0, place - 4):place]
        if any(one in AN_AMOUNT for one in before) or re.search(r"\d", " ".join(before)):
            return True
    return False


def _among_measured_things(clause, thing):
    words = str(clause or "").lower()
    if not thing or not MEASURED.search(words):
        return False
    parts = [part.strip() for part in MEASURED_PARTS.split(words) if part.strip()]
    if len(parts) < 3:
        return False
    return any(_names(part, thing) for part in parts)


def is_a_thing_on_a_list(clause, thing=""):
    said = str(clause or "").strip()
    tidied = _tidy(said)
    if tidied and not MEASURED.search(tidied):
        said = tidied
    if not said:
        return False
    if _among_measured_things(said, thing) or _the_amount_of_it(said, thing):
        return True
    return not STEP.match(said) and not SAID_OF_IT.search(said)


def after_an_answer(memory):
    return tried.after_an_answer(memory)


def _last_answer(memory):
    turns = [turn for turn in (memory.get("turns") or []) if isinstance(turn, dict)]
    if not turns:
        return "", ""
    last = turns[-1]
    asked = str(turns[-2].get("user") or "") if len(turns) > 1 else str(
        (memory.get("last_answer") or {}).get("question") or "")
    return str(last.get("bot") or ""), asked


def reads_the_answer(text, memory):
    if not after_an_answer(memory):
        return False
    limit = reads_as_a_limit(text, memory)
    if not limit:
        return False
    kind, _thing, bare = limit
    answer, _asked = _last_answer(memory)
    if not answer:
        return False
    if kind == "pet":
        return _with_a_pet(answer, bare) is not None
    named = _first_with(answer, bare)
    if named:
        return not is_a_thing_on_a_list(named, bare)
    if _without_the_appliance(bare, answer, memory):
        return True
    return bool(tried.asks_for_a_fix(memory)
                and (_about_the_job(bare, memory) or _a_fault_in_the_line_answered(memory))
                and not a_detail_of_a_fault(memory, bare))


def _the_line_answered(memory):
    for turn in reversed([turn for turn in (memory or {}).get("turns") or []
                          if isinstance(turn, dict)]):
        if turn.get("bot"):
            return str(turn.get("user") or "")
    return str(((memory or {}).get("last_answer") or {}).get("question") or "")


def _a_fault_in_the_line_answered(memory):
    reported = _the_line_answered(memory)
    return bool(reported) and bool(tried.FAULT.search(reported.lower()))


def _about_the_job(bare, memory):
    named_words = set()
    for word in words_of(_the_line_answered(memory)):
        if len(word) > 3 and word not in topics.STOPWORDS:
            named_words |= topics.forms(word)
    if not named_words:
        return False
    return any(named_words & topics.forms(word) for word in words_of(bare)
               if len(word) > 3 and word not in topics.STOPWORDS)


def reply_for(text, memory):
    reply = _limit_reply(text, memory)
    if reply:
        memory["limit"] = {"said": reply, "steps": _steps_the_limit_left(text, memory)}
    return reply


MOVE = re.compile(r"\b(?:first|start|begin|next|step|steps|change|try)\b", re.I)


def move_after_a_limit(text, memory):
    record = memory.get("limit")
    if not isinstance(record, dict):
        return None
    turns = [turn for turn in (memory.get("turns") or []) if isinstance(turn, dict)]
    if not turns or str(turns[-1].get("bot") or "").strip() != str(record.get("said") or "").strip():
        memory.pop("limit", None)
        return None
    line = str(text or "").strip()
    if not MOVE.search(line) or len(words_of(line)) > 8:
        return None
    if topics.pairing(line) or not _names_no_thing(line):
        return None
    steps = [step for step in (record.get("steps") or []) if step]
    if not steps:
        return None
    step = steps[0].strip().rstrip(". ")
    if not step:
        return None
    return "I would start here: " + step[0].lower() + step[1:] + "."


def _names_no_thing(line):
    words = [word for word in words_of(line)
             if word not in topics.STOPWORDS and word not in MOVE_ASKS and len(word) > 1]
    return not words


MOVE_ASKS = frozenset("""what whats where when which who why how first start begin next step steps
    change try do i we you should shall can could would the a an it that this there and then so
    now best thing things makes make much about on in to""".split())


def _steps_the_limit_left(text, memory):
    limit = reads_as_a_limit(text, memory)
    answer, _asked = _last_answer(memory)
    if not limit or not answer:
        return []
    kind, _thing, bare = limit
    if kind == "pet":
        return [step for step, _ in _steps(answer) if not NOT_WITH_A_PET.search(step)]
    return [step for step, _ in _steps(answer) if not _names(step, bare)]


def a_detail_of_a_fault(memory, bare):
    if not A_DETAIL_OF_THE_FAULT.match(" ".join(str(bare or "").split())):
        return False
    reported = ""
    for turn in reversed([t for t in (memory or {}).get("turns") or [] if isinstance(t, dict)]):
        if turn.get("bot"):
            reported = str(turn.get("user") or "")
            break
    if not reported:
        return False
    line = reported.lower()
    return (bool(A_HEATING_FAULT.search(line)) and bool(tried.FAULT.search(line))
            and not A_LEAKING_FAULT.search(line) and not tried.buying(memory))


APPLIANCES = ("oven", "hob", "microwave", "cooker", "stove")
NO_APPLIANCE = (
    "No {thing}, then. {answer}",
    "Right, no {thing}. {answer}",
    "Without a {thing}, then. {answer}",
)


def _without_the_appliance(thing, answer, memory):
    name = str(thing or "").strip().lower()
    if name not in APPLIANCES:
        return None
    from ..knowledge import cooking
    asked = "what can i cook with no " + name
    understood = {"clean": asked, "words": asked.split(), "excludes": [name],
                  "constraint": True}
    if not cooking.missing(understood):
        return None
    if not cooking.unusable(answer, understood):
        return None
    alternative = cooking.without(understood)
    if not alternative:
        return None
    alternative = alternative[:1].upper() + alternative[1:]
    return pick(NO_APPLIANCE, memory, name).format(thing=name, answer=alternative)


def _limit_reply(text, memory):
    if not after_an_answer(memory):
        return None
    limit = reads_as_a_limit(text, memory)
    if not limit:
        return None
    kind, thing, bare = limit
    answer, _asked = _last_answer(memory)
    if not answer:
        return None
    if kind == "pet":
        return _with_a_pet(answer, bare)
    if a_detail_of_a_fault(memory, bare):
        return None

    steps = _steps(answer)
    if not steps:
        return None
    named = _first_with(answer, bare)
    if not named:
        alternative = _without_the_appliance(bare, answer, memory)
        if alternative:
            return alternative
        if not _a_fault_in_the_line_answered(memory) or not tried.asks_for_a_fix(memory):
            return None
        return _say("You don't need " + thing + " for that: ", _up_to_words(_kept(answer, bare)))
    if is_a_thing_on_a_list(named, bare):
        return None
    if _names(steps[0][0], bare) and _holds_on(answer, bare):
        return _needs_it(thing, answer)
    kept = _without_a_repeated_time(_kept(answer, bare))
    if not kept:
        return None
    verbatim = thing if _names(named, thing) else _bare_phrase(named, bare)
    return _say("Skip the " + verbatim + ": ", _up_to_words(kept))


HOLDS_ON = re.compile(r"\b(?:it|them|this|that|these|those|the rest)\b", re.I)

WORDS_IN_A_REPLY = 30

WHO_TO_CALL = re.compile(
    r"\b(?:engineer|plumber|electrician|gas safe|corgi|professional|qualified|specialist|expert|"
    r"call (?:someone|somebody|out)|get (?:someone|somebody|an? [a-z]+ )?(?:in|out))\b", re.I)


def _kept(answer, bare):
    out = []
    for sentence, clauses in _pieces(answer):
        kept = []
        for clause in clauses:
            for step in re.split(AND_STEP, clause):
                step = step.strip(" .,;:")
                if step and not _names(step, bare):
                    kept.append(step)
        if kept:
            out.append(", ".join(kept))
    return out


TIME_TAIL = re.compile(
    r"^\d+(?:\s*(?:-|to)\s*\d+)?\s*(?:minutes?|mins?|hours?|hrs?|seconds?|secs?)"
    r"(?:\s*,?\s*(?:give or take|or so|roughly|about|max|at most))?[.!]?$", re.I)
A_TIME = re.compile(r"\b\d+(?:\s*(?:-|to)\s*\d+)?\s*(?:minutes?|mins?|hours?|hrs?|seconds?|secs?)\b",
                    re.I)


def _without_a_repeated_time(sentences):
    out = []
    for sentence in sentences:
        if out and TIME_TAIL.match(sentence.strip()) and A_TIME.search(" ".join(out)):
            continue
        out.append(sentence)
    return out


def _up_to_words(sentences):
    out, count = [], 0
    for sentence in sentences:
        words = len(words_of(sentence))
        if out and count + words > WORDS_IN_A_REPLY:
            break
        out.append(sentence)
        count += words
    return out


def _holds_on(answer, bare):
    kept = _kept(answer, bare)
    return bool(kept) and bool(HOLDS_ON.search(kept[0]))


def _needs_it(thing, answer):
    lead = ("You can't do the first step without the " + thing +
            ", and the rest of that answer is done after it. ")
    for sentence, _clauses in reversed(_pieces(answer)):
        if WHO_TO_CALL.search(sentence) and not _names(sentence, thing):
            return lead + sentence.strip()
    return lead.rstrip()


def _bare_phrase(named, bare):
    words = words_of(named)
    for word in words:
        if word in topics.forms(bare):
            return word
    return bare


def _with_a_pet(answer, who):
    steps = _steps(answer)
    hazard = [step for step, _ in steps if NOT_WITH_A_PET.search(step)]
    safe = [step for step, _ in steps if not NOT_WITH_A_PET.search(step)]
    if not hazard or not safe:
        return None
    named = NOT_WITH_A_PET.search(hazard[0]).group(0).lower()
    lead = LEADS["pet"].format(who=who) + "skip the " + named + ": "
    return _say(lead, safe)


def _say(lead, steps):
    said = _tidy(steps[0])
    if len(steps) > 1 and not said.endswith((".", "!", "?")):
        second = _tidy(steps[1])
        said += (". " + second) if second[:1].isupper() else (", " + second)
    said = said.rstrip(" ,;:")
    if not said.endswith((".", "!", "?")):
        said += "."
    return lead + said[0].lower() + said[1:] if lead else said[0].upper() + said[1:]


def _tidy(step):
    said = re.sub(r"^(?:and|then|so|but|also)\s+", "", step.strip(), flags=re.I)
    return said.strip()
