import re

from ..compose import pick
from . import current, last_user
from . import facts as extract
from .topics import answer_in_hand, keywords

REPAIR = re.compile(
    r"^\W*(?:(?:no|nah|nope|sorry|actually|oh|wait|hmm|well|ok|okay|right|yes)[,\s]+)*"
    r"(?:i\s+(?:meant|mean)|i\s+did\s+mean|we\s+meant|meant|rather)\b[,\s:]+"
    r"(?P<thing>\S.*?)\W*$", re.I)

BARE_REPAIR = re.compile(
    r"^\W*(?:(?P<frame>no|nah|nope|sorry|actually|oh|wait)[,\s]+)+"
    r"(?P<thing>[^.!?]+?)\W*$", re.I)
NOT_A_SWAP = frozenset("""
    thanks thank worries worry problem problems idea matter matters clue doubt chance way luck
    bother hurry rush need point sense reason question questions bother drama fault apologies
    apology offence offense harm damage wonder need boat idea lot bit little
""".split())
A_POSSESSION_REPAIR = re.compile(
    r"^\W*(?:(?P<frame>no|nah|nope|sorry|actually|oh|wait)[,\s]+)+"
    r"(?:i|we)(?:'ve|ve|\s+have|\s+have\s+got|\s+got)\s+(?:got\s+)?"
    r"(?P<thing>[^.!?]+?)\W*$", re.I)
A_VERB_IN_THE_THING = frozenset("""
    is are was were am be been being do does did done doing have has had having
    can could should would will shall may might must
    want wants wanted need needs needed got get gets got make makes made take takes took
    give gives gave go goes went gone like likes liked love loves loved hate hates hated
    feel feels felt hurt hurts hurt think thinks thought know knows knew said says say
    tell tells told see sees saw seen try tries tried use uses used work works worked
    live lives lived play plays played eat eats ate drink drinks drank buy buys bought
    sell sells sold pay pays paid find finds found lose loses lost break breaks broke
    fix fixes fixed start starts started stop stops stopped keep keeps kept put puts
    run runs ran walk walks walked cook cooks cooked clean cleans cleaned
""".split())

AN_INTENTION = re.compile(r"\b(?:i|we)\s+meant\s+to\s+(?!say\b)", re.I)

A_VALUE = re.compile(r"\d", re.I)
A_CONTRAST = re.compile(r"\b(?:not|instead|isn'?t|wasn'?t|isnt|wasnt)\b", re.I)

AN_ASK = frozenset("""
    should shall can could would will may might must do does did is are was were am
    have has had what whats how when where which who why whose
""".split())

NOT_A_THING = frozenset("""
    it that this these those them one other the a an something anything nothing whatever thing
    things what which same more less first second last next another both all here there
""".split())

A_REMARK = frozenset("""
    i im id ill ive we you he she they it its that there this just only also really very so
    whatever anyway honestly
""".split())

NOT_THE_THING = frozenset("""
    a an the my our your his her their its some any this that these those it them
    is are was were am be been being do does did done doing have has had having
    can could should would will shall may might must
    and or but so then than too also just very really quite more most less least
    for with without about at in on of to from by into onto over under again
    what whats how when where which who why whose way much many long
    good best great nice better bad worse ok okay please thanks thank
    today tomorrow tonight yesterday now soon later weekend weekends weekday weekdays
    this weekend next weekend last weekend
    one ones thing things stuff lot lots bit little
""".split())


A_DETERMINER = re.compile(
    r"^(?:a|an|the|my|our|your|his|her|their|this|that|these|those)\b", re.I)


def _the_thing(text):
    said = " ".join(str(text or "").split())
    if AN_INTENTION.search(said):
        return None
    if A_CONTRAST.search(said):
        return None
    match = REPAIR.match(said)
    bare = False
    if not match:
        match = A_POSSESSION_REPAIR.match(said)
        if not match:
            match = BARE_REPAIR.match(said)
            if match:
                bare = True
        if not match:
            return None
    thing = re.sub(r"^to\s+(?:say\s+|mean\s+)?", "", match.group("thing").strip())
    thing = thing.strip(" ,.!?;:\"'")
    if not thing or A_VALUE.search(thing):
        return None
    words = [word.strip("'") for word in re.findall(r"[a-z0-9']+", thing.lower())]
    if not words or all(word in NOT_A_THING for word in words):
        return None
    if words[0] in A_REMARK:
        return None
    if bare and not A_DETERMINER.match(thing):
        return None
    if bare and all(word in NOT_A_SWAP for word in words if word not in NOT_THE_THING):
        return None
    if bare and any(word in A_VERB_IN_THE_THING for word in words):
        return None
    if words[0] in AN_ASK:
        return None
    if words[-1] in NOT_A_THING and words[-1] != words[0]:
        return thing if not all(word in NOT_A_THING | NOT_THE_THING for word in words) else None
    return thing


def _a_different_thing(old, thing):
    held = _content_words(old)
    said = _content_words(thing)
    if not said:
        return False
    return bool(said - held)


def _content_words(text):
    words = [word.strip("'") for word in re.findall(r"[a-z0-9']+", str(text or "").lower())]
    return {word for word in words
            if word and word not in ("a", "an", "the", "my", "our", "your", "his", "her",
                                     "their", "its", "some", "any", "this", "that")}


_READINGS = {}


def _the_reading(line):
    said = str(line or "")
    if said in _READINGS:
        return _READINGS[said]
    from ..understanding import understand
    try:
        read = understand(said, {"turns": []})
    except Exception:
        read = {}
    if not isinstance(read, dict):
        read = {}
    if len(_READINGS) > 12:
        _READINGS.clear()
    _READINGS[said] = read
    return read


def _the_thing_the_reading_named(line):
    read = _the_reading(line)
    found = []
    for one in read.get("entities") or ():
        if not isinstance(one, dict):
            continue
        if str(one.get("type") or "") not in ("thing", "animal", "food", "place"):
            continue
        text = " ".join(str(one.get("text") or "").lower().split())
        if not text:
            continue
        at = one.get("at")
        at = at if isinstance(at, int) else None
        found.append((at, text))
    if not found:
        return ""
    found.sort(key=lambda pair: (pair[0] is None, pair[0]))
    one = found[0][1]
    for index, (at, text) in enumerate(found[1:], start=1):
        before = found[index - 1]
        if at is not None and before[0] is not None \
                and at == before[0] + len(before[1].split()):
            one = one + " " + text
        else:
            return ""
    said = " ".join(str(line or "").lower().split())
    return one if one in said else ""


def _the_thing_the_last_line_named(line):
    words = [word.strip("'") for word in
             re.findall(r"[a-z0-9']+", str(line or "").lower())]
    for word in reversed(words):
        if len(word) < 3 or word in NOT_THE_THING or word in NOT_A_THING:
            continue
        if word in extract.MONTHS or word in extract.DAYS or word.isdigit():
            return None
        if keywords(word):
            return word
        return None
    return None


A_POINTER = frozenset(("one", "ones"))


def _the_noun_the_line_named(line):
    words = [word.strip("'") for word in
             re.findall(r"[a-z0-9']+", str(line or "").lower())]
    for word in reversed(words):
        if len(word) < 3 or word in NOT_THE_THING or word in NOT_A_THING:
            continue
        if word in A_VERB_IN_THE_THING or word in extract.MONTHS or word in extract.DAYS:
            continue
        if keywords(word):
            return word
        return None
    return None


def _the_pointer_refines(thing, line):
    words = [word.strip("'") for word in re.findall(r"[a-z0-9']+", str(thing or "").lower())]
    if not words or words[-1] not in A_POINTER:
        return None
    mods = [word for word in words[:-1]
            if len(word) >= 2 and word not in NOT_THE_THING and word not in NOT_A_THING]
    if not mods:
        return None
    noun = _the_noun_the_line_named(line)
    if not noun:
        return None
    return noun, " ".join(mods) + " " + noun


def _the_relation(word):
    plain = str(word or "").strip().lower().strip("'")
    if plain in extract.RELATIONS:
        return plain
    if plain.endswith("'s"):
        plain = plain[:-2]
    elif plain.endswith("s"):
        plain = plain[:-1]
    if plain in extract.RELATIONS:
        return plain
    if plain.endswith("'"):
        plain = plain[:-1]
    return plain if plain in extract.RELATIONS else None


def _the_person_the_line_named(line, thing):
    named = {person for person in (_the_relation(word)
                                   for word in re.findall(r"[a-z']+", str(thing or "").lower()))
             if person}
    if not named:
        return None
    for word in re.findall(r"[a-z']+", str(line or "").lower()):
        person = _the_relation(word)
        if person and person not in named:
            return person
    return None


def _swapped(line, old, thing):
    said = " ".join(str(line or "").split())
    new = str(thing or "").strip()
    tail = r"(?:'s|s)?" if old in extract.RELATIONS else ""
    match = re.search(r"\b" + re.escape(str(old)) + tail + r"\b", said, re.I)
    if not match:
        return ""
    before = said[:match.start()].split()
    if before and re.match(r"^(?:a|an|the|my|our|your|his|her|their|this|that|these|those)\b",
                           new, re.I):
        new = re.sub(r"^(?:a|an|the|my|our|your|his|her|their|this|that|these|those)\s+", "",
                     new, count=1, flags=re.I)
    out = said[:match.start()] + new + said[match.end():]
    out = _no_repeat(" ".join(out.split()))
    return "" if out.lower() == said.lower() else out


def _no_repeat(line):
    words = line.split()
    out = []
    for word in words:
        if out and word.lower() == out[-1].lower():
            continue
        out.append(word)
    return " ".join(out)


def _the_answer(line, memory):
    from ..modules import answers
    from ..understanding import understand

    fresh = {"turns": [], "aside": True, "understood": understand(line, {"turns": []})}
    for key in ("user", "others", "facts_log"):
        if key in memory:
            fresh[key] = memory[key]
    try:
        reply = answers.respond(line, fresh)
    except Exception:
        return None
    if isinstance(reply, str) and reply.strip():
        for key in ("entry_answer", "entry_answers"):
            if key in fresh:
                memory[key] = fresh[key]
        return reply.strip()
    return None


def _the_plain_answer(text, memory):
    from ..modules import answers

    try:
        reply = answers.respond(text, memory)
    except Exception:
        return None
    said = " ".join(str(reply or "").split())
    return said or None


def _about_the_same_thing(first, second):
    left = {word for word in keywords(str(first or "")) if len(word) > 3}
    right = {word for word in keywords(str(second or "")) if len(word) > 3}
    return bool(left & right)


def _the_shape_the_swap_had(memory, line, old, thing):
    last = str(last_user(memory) or "")
    tail = _the_thing_the_last_line_named(last) if last else ""
    if tail and _a_state_not_a_thing(last, tail):
        return line
    if tail and tail != old and _a_different_thing(tail, thing):
        older = _swapped(last, tail, thing)
        if older:
            return older
    return line


def _a_state_not_a_thing(line, tail):
    pattern = (r"\b(?:is|are|was|were|isn'?t|aren'?t|wasn'?t|weren'?t|feels?|seems?|looks?|gets?"
               r"|got|goes|went|has|have|had|keeps?|stays?|stops?)\s+" + re.escape(str(tail)) + r"\b")
    return bool(re.search(pattern, str(line or ""), re.I))


def _keep_the_swap(memory, line, old, thing):
    line = _the_shape_the_swap_had(memory, line, old, thing)
    record = current(memory)
    if isinstance(record, dict):
        record["text"] = line
        record["words"] = keywords(line)
        record["corrected"] = thing
        topics = memory.get("topics")
        if isinstance(topics, list) and topics and topics[-1] is not record:
            topics[-1] = record
    known = memory.get("user")
    if not isinstance(known, dict):
        return
    for key in ("plan", "plans"):
        held = known.get(key)
        if isinstance(held, str):
            moved = _swapped(held, old, thing)
            if moved:
                known[key] = moved
        elif isinstance(held, list):
            known[key] = [_swapped(str(one), old, thing) or str(one) for one in held]
    for entry in reversed(list(memory.get("facts_log") or [])[:6]):
        if not isinstance(entry, dict) or entry.get("key") not in ("plan", "plans"):
            continue
        value = entry.get("value")
        if isinstance(value, str):
            moved = _swapped(value, old, thing)
            if moved:
                entry["value"] = moved


def _the_paragraph_already_given(answer, memory, old, thing):
    said = set(re.findall(r"[a-z0-9']+", " ".join(str(answer or "").lower().split())))
    if len(said) < 25:
        return False
    turns = memory.get("turns")
    if not isinstance(turns, list):
        return False
    for turn in reversed(turns[-4:]):
        earlier = str((turn or {}).get("bot") or "")
        if len(earlier.split()) < 20:
            continue
        other = set(re.findall(r"[a-z0-9']+", " ".join(earlier.lower().split())))
        if not other:
            continue
        shared = len(said & other) / float(len(said | other))
        if shared < 0.8:
            continue
        if not (keywords(thing) and keywords(old)):
            continue
        if not _names(said, keywords(thing)) or not _names(other, keywords(old)):
            continue
        if _names(said, keywords(old)):
            continue
        return True
    return False


def _names(words, wanted):
    for one in wanted:
        one = str(one or "").lower()
        if not one:
            continue
        for word in words:
            if word == one or word == one + "s" or word.rstrip("s") == one:
                return True
    return False


def _without_the_repeat_lead(answer):
    said = REPEAT_LEAD.sub("", " ".join(str(answer or "").split()))
    return said if len(said) >= 40 else answer


def _still_the_old_thing(answer, old, thing):
    said = " ".join(str(answer or "").lower().split())
    if not old:
        return False
    words = set(re.findall(r"[a-z']+", said))
    if not any(str(word).lower() in words for word in keywords(old) or ()):
        return False
    opening = set(re.findall(r"[a-z']+", " ".join(said.split()[:12])))
    for word in keywords(thing) or ():
        if str(word).lower() in opening:
            return False
    return True


def _bare(thing):
    words = " ".join(str(thing or "").split()).strip(" .,").split()
    if len(words) > 1 and words[0].lower() in ("a", "an", "the", "my", "our", "your", "his",
                                               "her", "their"):
        return " ".join(words[1:])
    return " ".join(words)


def _said_before(answer, memory):
    turns = memory.get("turns")
    if not isinstance(turns, list) or not turns:
        return False
    opening = " ".join(" ".join(answer.lower().split()).split()[:10])
    if not opening:
        return False
    return any(opening in " ".join(str((turn or {}).get("bot") or "").lower().split())
               for turn in turns)


A_FIGURE_REPAIR = re.compile(
    r"^\W*(?:(?:no|nah|nope|sorry|actually|oh|wait|hmm|well|ok|okay|right|yes)[,\s]+)*"
    r"(?:i\s+(?:meant|mean)|i\s+did\s+mean|we\s+meant|meant)\b[\s,:-]+"
    r"(?P<figure>\d+(?:\.\d+)?)\s*(?P<unit>[a-z]{0,10})\W*$", re.I)

FIGURE_UNITS = frozenset("""
    kg kilo kilos g gram grams lb lbs oz litre litres liter liters ml pint pints
    pound pounds quid hours hour mins minutes min days day weeks week months month years year
    people person guests adults kids children degrees degree percent
""".split())

A_FIGURE = re.compile(r"\b(?P<figure>\d+(?:\.\d+)?)\s*(?P<unit>[a-z]{0,12})", re.I)

FIGURE_OR_WORD = re.compile(
    r"(?<![\d.])\d+(?:\.\d+)?(?![\d])"
    r"|\b(?:one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|fifteen|twenty)\b",
    re.I)

SENTENCE_END = re.compile(r"(?<=[.!?])\s+")


def _the_same_words(one, other):
    def stemmed(sentence):
        words = FIGURE_OR_WORD.sub("#", str(sentence or "").lower()).split()
        return [word[:-1] if len(word) > 3 and word.endswith("s") else word for word in words]

    return stemmed(one) == stemmed(other)


def _the_figure_in(line):
    found = None
    for match in A_FIGURE.finditer(str(line or "")):
        unit = (match.group("unit") or "").lower()
        found = (match, unit if unit in FIGURE_UNITS else "")
    return found


def _the_figure_they_meant(text, memory):
    match = A_FIGURE_REPAIR.match(" ".join(str(text or "").split()))
    if not match:
        return ""
    figure = match.group("figure")
    unit = (match.group("unit") or "").lower()
    if unit and unit not in FIGURE_UNITS:
        return ""
    before = " ".join(str(last_user(memory) or "").split())
    if not before:
        return ""
    found = _the_figure_in(before)
    if not found:
        return ""
    held, held_unit = found
    if held.group("figure") == figure:
        return ""
    if unit and unit != held_unit:
        return ""
    line = before[:held.start("figure")] + figure + before[held.end("figure"):]
    said = answer_in_hand(memory) or {}
    said = str((said or {}).get("bot") or "") if isinstance(said, dict) else ""
    if not said or not _the_answer_says(said, held.group("figure")):
        return ""
    scratch = dict(memory)
    redone = _the_answer(line, scratch)
    if not redone:
        return ""
    changed = _the_figures_that_moved(said, redone)
    if not changed:
        return ""
    _keep_the_corrected_answer(memory, scratch, line)
    return changed


THE_WORD_FOR = {number: word for word, number in extract.FIGURE_WORDS.items()}


def _the_answer_says(said, figure):
    for spelling in (str(figure), THE_WORD_FOR.get(str(figure), "")):
        if not spelling:
            continue
        if re.search(r"(?<![\d.])" + re.escape(spelling) + r"(?![\d])", said, re.I):
            return True
    return False


def _the_figures_that_moved(said, redone):
    before = [one for one in SENTENCE_END.split(" ".join(str(said or "").split())) if one]
    after = [one for one in SENTENCE_END.split(" ".join(str(redone or "").split())) if one]
    if not before or len(before) != len(after):
        return ""
    changed = []
    for old, new in zip(before, after):
        if not _the_same_words(old, new):
            return ""
        if old != new:
            changed.append(new)
    if not changed:
        return ""
    said = " ".join(changed).strip()
    return said[:1].upper() + said[1:]


def _keep_the_corrected_answer(memory, scratch, line):
    for key in ("entry_answer", "entry_answers"):
        if key in scratch:
            memory[key] = scratch[key]
    record = current(memory)
    if isinstance(record, dict):
        record["text"] = line
        record["words"] = keywords(line)


SWAPPED = (
    "{thing}, then.",
    "Got it \u2014 {thing}.",
    "{thing} it is.",
)

AN_ASK_OPENS = re.compile(
    r"^(?:how|what|why|when|where|which|who|whose|whom)\b"
    r"|^(?:can|could|should|would|will|shall|do|does|did|is|are|was|were|have|has|had|am|may"
    r"|might|must|need)\s+(?:i|we|you|they|it|he|she|that|this|there)\b", re.I)

HEDGE = re.compile(r"\b(?:beyond what i know|don'?t know enough|a quick search|i'?d rather not "
                   r"guess|not sure about that|i don'?t know that one)\b", re.I)

A_REAL_ANSWER = 80

REPEAT_LEAD = re.compile(
    r"^[^:]{0,90}\b(?:same goes for|same advice (?:as|for|as for)|same as (?:for |the |as )?)\b"
    r"[^:]{0,90}:\s*", re.I)

SAME_AGAIN = (
    "{said}, then \u2014 the same advice as for the {old}: {answer}",
    "Got it \u2014 {thing}. The same advice as for the {old} holds: {answer}",
    "{said}, then. Same advice as the {old}: {answer}",
)

SAME_ADVICE = (
    "{said}, then \u2014 the same advice as for the {old}.",
    "Got it \u2014 {thing}. The same advice as for the {old} applies.",
    "{said}, then. Same advice as the {old}.",
)

THE_FACT_MOVED = (
    "Got it \u2014 your {new}'s {fact}, not your {old}.",
    "Noted \u2014 your {new} is the one who's {fact}.",
    "Your {new}, then, not your {old} \u2014 your {new}'s {fact}.",
)


_KEEP = True


def _a_fact_of_the_person(entry):
    age = entry.get("age")
    if age:
        return str(age)
    allergies = entry.get("allergies")
    if allergies:
        return "allergic to " + _a_list_of(allergies)
    return ""


def _a_list_of(things):
    said = [str(one).strip() for one in things if str(one).strip()]
    if not said:
        return ""
    if len(said) == 1:
        return said[0]
    return ", ".join(said[:-1]) + " and " + said[-1]


def _the_fact_moved_to_the_person_they_meant(memory, old, thing, text):
    from . import others, remember_other

    wanted = extract.a_person_word(_bare(thing))
    if not wanted or wanted == extract.a_person_word(old):
        return ""
    for entry in list(others(memory)):
        if extract.a_person_word(entry.get("who")) != extract.a_person_word(old):
            continue
        fact = _a_fact_of_the_person(entry)
        if not fact:
            return ""
        others(memory).remove(entry)
        moved = {key: value for key, value in entry.items() if key != "who"}
        moved["who"] = wanted
        remember_other(memory, moved, str(text))
        return fact
    return ""


def _the_fact_moved_line(fact, old, thing, text, memory):
    if not fact:
        return None
    said = pick(THE_FACT_MOVED, memory, str(text)).format(
        new=_bare(thing), old=_bare(old), fact=fact)
    return said if said.endswith((".", "!", "?")) else said + "."


def _the_swap_in_the_line(text, memory):
    if not isinstance(memory, dict):
        return None
    thing = _the_thing(text)
    if not thing or AN_ASK_OPENS.match(thing) or thing.rstrip().endswith("?"):
        return None
    last = str(last_user(memory) or "")
    if not last:
        return None
    refined = _the_pointer_refines(thing, last)
    if refined:
        old, thing = refined
        return last, [old], thing, refined
    old = _the_person_the_line_named(last, thing)
    olds = [old] if old else []
    for one in (_the_thing_the_reading_named(last), _the_thing_the_last_line_named(last)):
        if one and one not in olds:
            olds.append(one)
    if not olds:
        return None
    return last, olds, thing, None


def keep_the_correction(text, memory):
    found = _the_swap_in_the_line(text, memory)
    if not found:
        return
    last, olds, thing, _refined = found
    for one in olds:
        if not _a_different_thing(one, thing):
            continue
        swapped = _swapped(last, one, thing)
        if swapped:
            _keep_the_swap(memory, swapped, one, thing)
            return


def the_thing_they_meant(text, memory):
    if not isinstance(memory, dict):
        return None
    figure = _the_figure_they_meant(text, memory)
    if figure:
        return figure
    thing = _the_thing(text)
    if not thing:
        return None
    if AN_ASK_OPENS.match(thing) or thing.rstrip().endswith("?"):
        answer = _the_answer(thing, memory)
        if not answer:
            return None
        answer = _without_the_repeat_lead(answer)
        if _said_before(answer, memory):
            return None
        return answer if answer.endswith((".", "!", "?")) else answer + "."
    last, olds, thing, refined = _the_swap_in_the_line(text, memory)
    held = olds[0]
    fact = _the_fact_moved_to_the_person_they_meant(memory, held, thing, text)
    answer, line, old = "", "", ""
    for one in olds:
        if not _a_different_thing(one, thing):
            continue
        swapped = _swapped(last, one, thing)
        if not swapped:
            continue
        found = _the_answer(swapped, memory)
        if found:
            answer, line, old = found, swapped, one
            break
    if not answer:
            return _the_fact_moved_line(fact, held, thing, text, memory)
    answer = _without_the_repeat_lead(answer)
    plain = _the_plain_answer(text, memory)
    if plain and not (_about_the_same_thing(plain, thing)
                      or _about_the_same_thing(plain, answer)):
        plain = None
    if plain and _without_the_repeat_lead(plain) == answer:
        _keep_the_swap(memory, line, old, thing)
        return None
    if plain and len(plain) > A_REAL_ANSWER and not HEDGE.search(plain) \
            and not _still_the_old_thing(plain, old, thing):
        if _said_before(plain, memory):
            return None
        _keep_the_swap(memory, line, old, thing)
        return plain if plain.endswith((".", "!", "?")) else plain + "."
    if plain == answer:
        _keep_the_swap(memory, line, old, thing)
        return None
    _keep_the_swap(memory, line, old, thing)
    if refined and not _said_before(answer, memory):
        return answer if answer.endswith((".", "!", "?")) else answer + "."
    shown = thing[:1].upper() + thing[1:]
    if _the_paragraph_already_given(answer, memory, old, thing):
        held = _bare(thing)
        if shown.split()[0].lower() in ("the", "a", "an", "my", "our", "your", "his", "her"):
            held = shown[:1].lower() + shown[1:]
        said = pick(SAME_ADVICE, memory, str(text)).format(
            said=shown, thing=held, old=_bare(old))
        return said if said.endswith((".", "!", "?")) else said + "."
    if _said_before(answer, memory):
        held = _bare(thing)
        if shown.split()[0].lower() in ("the", "a", "an", "my", "our", "your", "his", "her"):
            held = shown[:1].lower() + shown[1:]
        said = pick(SAME_AGAIN, memory, str(text)).format(
            said=shown, thing=held, old=_bare(old), answer=answer[:1].lower() + answer[1:])
        return said if said.endswith((".", "!", "?")) else said + "."
    shape = pick(SWAPPED, memory, str(text))
    if not shape.startswith("{thing}"):
        if shown.split()[0].lower() in ("the", "a", "an", "my", "our", "your", "his", "her"):
            shown = shown[:1].lower() + shown[1:]
    said = shape.format(thing=shown)
    return (said + " " + answer).strip()
