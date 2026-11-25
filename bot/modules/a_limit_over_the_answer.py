
import re

PRIORITY = 500

_LEAD = re.compile(r"^(?:well|ok|okay|so|oh|ah|and|but|honestly|actually|yeah|sorry|"
                   r"anyway|course|of\s+course)\b[\s,]*", re.I)

_TAIL = re.compile(r"(?:\s+(?:tbh|tho|though|anyway|actually|really|literally|honestly|"
                   r"i\s+suppose|i\s+guess|still|also|too|by\s+the\s+way|btw|atm|"
                   r"at\s+the\s+moment|lol|ha|haha|so\s+yeah|though|mate|dude|sadly|"
                   r"unfortunately))+$", re.I)

_ASKS = re.compile(r"\?|^\s*(?:what|how|when|where|why|who|can|could|should|would|do|does|did|"
                   r"is|are|was|were|will|shall|any)\b", re.I)


def _clean(text):
    low = " ".join(str(text or "").replace("\u2019", "'").split()).strip(" .!,")
    for _ in range(3):
        before = low
        low = _LEAD.sub("", low)
        low = _TAIL.sub("", low)
        if low == before:
            break
    return low.lower().strip(" .,!")


_KINDS = (
    ("rent", (
        re.compile(r"^(?:we|i)\s*(?:just\s+)?rent(?:ing)?(?:\s+(?:a|an|the|our|this)\s+"
                   r"(?:flat|house|place|home|bungalow|room|council\s+flat))?$"),
        re.compile(r"^(?:we|i)\s*(?:are|re)\s+(?:renting|in\s+a\s+rented|renters?)$"),
        re.compile(r"^(?:its|it\s+is)\s+(?:a\s+)?(?:rented|rental|council|housing\s+association)"
                   r"(?:\s+(?:flat|house|place|home))?$"),
        re.compile(r"^(?:we|i)\s+(?:are|re)?\s*(?:just\s+)?tenants?$"),
        re.compile(r"^(?:we|i)\s+(?:dont|do\s+not)\s+own\s+(?:it|the\s+flat|the\s+house|our\s+home)$"),
    ), (
        "repair", "fix", "damp", "boiler", "radiator", "tap", "leak", "leaking", "dripping",
        "drip", "wall", "ceiling", "paint", "heating", "plumb", "roof", "floor", "fuse",
        "washer", "mould", "mold", "window", "door", "drains", "toilet", "shower", "bath",
        "landlord", "carpet", "electric", "socket", "gutter", "chimney",
    ), (
        "Then it's your landlord's to fix, not yours - but do the free bit first: {move}",
        "Renting puts that on them: report it in writing, and meanwhile {move_lower}",
        "Right, so it's their job. What you can do now: {move_lower}",
    )),
    ("no_car", (
        re.compile(r"^(?:we|i)\s*(?:have|ve)\s+(?:got\s+)?no\s+car$"),
        re.compile(r"^(?:there\s+is\s+)?no\s+car(?:\s+here)?$"),
        re.compile(r"^(?:we|i)\s*(?:dont|do\s+not|can\s*not|can't|cant)\s*drive$"),
        re.compile(r"^(?:we|i)\s*(?:dont|do\s+not)\s+have\s+(?:a\s+)?car$"),
        re.compile(r"^(?:its|it\s+is)\s+(?:a\s+)?no\s+car\s+(?:household|family)$"),
    ), (
        "drive", "driving", "car", "travel", "journey", "get there", "getting there", "route",
        "station", "bus", "train", "coach", "parking", "park", "trip", "visit", "ferry",
        "flight", "fly", "airport", "motorway",
    ), (
        "Then go by train or bus instead of driving - and the rest of it still holds: {move_lower}",
        "No car changes the how, not the plan: {move_lower}",
        "Then book the train rather than drive. Everything else stands: {move_lower}",
    )),
    ("only_a_balcony", (
        re.compile(r"^(?:we|i)\s*(?:only|just)\s+(?:have|ve\s+got|got)\s+(?:a\s+|one\s+)?"
                   r"(?:small\s+)?(?:balcony|windowsill|window\s+box|yard|patio|terrace|yard)$"),
        re.compile(r"^(?:its|it\s+is)\s+(?:just\s+)?(?:a\s+)?(?:balcony|windowsill|window\s+box)$"),
    ), (
        "plant", "sow", "sowing", "grow", "growing", "pot", "pots", "garden", "soil", "seed",
        "seeds", "compost", "bed", "patch", "allotment", "water", "sun", "shade", "herbs",
        "tomato", "tomatoes", "flower", "flowers", "bulb",
    ), (
        "Then keep it all in pots - that's the part that matters: {move_lower}",
        "A balcony is enough for that: {move_lower}",
        "Then it's pots on the balcony rather than a bed: {move_lower}",
    )),
    ("no_garden", (
        re.compile(r"^(?:we|i)\s*(?:dont|do\s+not)\s+have\s+(?:a\s+|any\s+)?"
                   r"(?:garden|outside\s+space|yard|plot|allotment)$"),
        re.compile(r"^(?:no|without\s+a)\s+(?:garden|outside\s+space|allotment)$"),
    ), (
        "plant", "sow", "sowing", "grow", "growing", "pot", "pots", "garden", "soil", "seed",
        "seeds", "compost", "bed", "patch", "allotment", "water", "sun", "shade", "herbs",
        "tomato", "tomatoes", "flower", "flowers", "bulb",
    ), (
        "Then keep it all in pots or a window box - that's the part that matters: {move_lower}",
        "No garden is fine for that: {move_lower}",
        "Then it's containers rather than a bed: {move_lower}",
    )),
    ("a_nervous_animal", (
        re.compile(r"^(?:hes|he\s+is|shes|she\s+is|its|it\s+is)\s+(?:a\s+)?(?:rescue|rescued)"
                   r"(?:\s+(?:and\s+)?(?:quite\s+|very\s+|really\s+)?(?:nervous|anxious|shy|"
                   r"scared|terrified|timid))?$"),
        re.compile(r"^(?:hes|he\s+is|shes|she\s+is|its|it\s+is)\s+(?:quite\s+|very\s+|really\s+)?"
                   r"(?:nervous|anxious|scared|terrified|timid|shy)$"),
        re.compile(r"^(?:hes|shes|its)\s+(?:a\s+)?rescue$"),
    ), (
        "dog", "dogs", "puppy", "cat", "cats", "kitten", "lead", "leash", "walk", "walks",
        "train", "training", "scratch", "scratching", "bark", "barking", "sofa", "litter",
        "collar", "harness", "garden", "vet", "animal", "rescue", "puppy",
    ), (
        "Then go slower than that and keep every go short: {move_lower}",
        "A nervous rescue needs that done in small doses: {move_lower}",
        "Then take it at their pace - the first step is the same: {move_lower}",
    )),
)

_INSTRUCTION = re.compile(r"^(?:sow|plant|prune|feed|mulch|pot|repot|thin|stake|tie|harvest|"
                          r"practise|practice|learn|watch|read|listen|repeat|spend|save|budget|"
                          r"compare|download|install|print|wear|cut|freeze|store|label|"
                          r"turn|put|take|use|keep|start|add|set|get|open|close|ask|book|"
                          r"check|try|make|give|water|clean|wash|report|write|stand|hold|"
                          r"cut|mix|place|leave|move|cover|wrap|soak|strip|sand|fill|fit|"
                          r"call|text|email|ring|go|walk|run|sit|lie|rest|eat|drink|buy|"
                          r"pick|choose|measure|weigh|boil|fry|bake|simmer|stir|season|"
                          r"remove|replace|tighten|loosen|unplug|switch|plug|drain|bleed)\b",
                          re.I)

_DANGLING = frozenset(("and", "or", "with", "a", "an", "the", "of", "to", "for", "in", "on",
                       "at", "plus", "then", "but", "so", "your", "my", "its"))

_JOINER = re.compile(r"^(?:so|and|then|but|just|really|also|first|afterwards?)\s+", re.I)

_LEAD_INS = re.compile(r"^(?:same\s+as\s+before|the\s+first\s+thing\s+to\s+do|"
                       r"first\s+thing|so|right|okay|ok|then)\s*:\s*", re.I)


def _a_limit(text):
    low = _clean(text)
    if not low or _ASKS.search(low):
        return None
    for kind, shapes, about, leads in _KINDS:
        for shape in shapes:
            if shape.match(low):
                return kind, about, leads
    return None


def _the_answer(memory):
    if not isinstance(memory, dict):
        return None
    record = memory.get("last_answer")
    if not isinstance(record, dict) or not isinstance(record.get("reply"), str):
        return None
    turns = memory.get("turns")
    if not isinstance(turns, list) or not turns:
        return None
    turn = record.get("turn")
    if not isinstance(turn, int) or turn < 0 or len(turns) - 1 - turn > 2:
        return None
    return record


def _what_the_answer_is_about(record):
    keys = record.get("keys") if isinstance(record, dict) else None
    if isinstance(keys, str):
        keys = keys.split()
    if not isinstance(keys, (list, tuple, set, frozenset)):
        return set()
    return {str(key).lower() for key in keys}


def _the_answer_is_about(record, about):
    if not about:
        return True
    if any(word in _what_the_answer_is_about(record) for word in about):
        return True
    low = record["reply"].lower()
    return len({word for word in about if word in low}) >= 2


_MOVE_WORDS = 45
_MOVE_CUT = 34


def _the_move(answer):
    text = " ".join(answer.replace("\u2014", "- ").split())
    text = _LEAD_INS.sub("", text)
    first = re.split(r"(?<=[.!?])\s", text)[0].strip(" .;:,-")
    if not first:
        return ""
    if ":" in first:
        head, tail = first.split(":", 1)
        if len(tail.split()) >= 4:
            first = tail.strip()
    parts = [part.strip() for part in re.split(r"[,;]\s", first) if part.strip()]
    if parts and not _INSTRUCTION.match(_JOINER.sub("", parts[0])):
        found = False
        for index, part in enumerate(parts[1:], 1):
            if _INSTRUCTION.match(_JOINER.sub("", part)):
                parts = parts[index:]
                found = True
                break
        if not found:
            return ""
    parts = [_JOINER.sub("", part) for part in parts]
    whole = [part for part in parts]
    out = []
    for part in whole:
        if out and len(" ".join(out + [part]).split()) > _MOVE_WORDS:
            break
        out.append(part)
    if len(out) > 1 and len(" ".join(out).split()) > _MOVE_CUT:
        kept = []
        for part in out:
            if kept and len(" ".join(kept + [part]).split()) > _MOVE_CUT:
                break
            kept.append(part)
        out = kept or out[:1]
    cut = ", ".join(out) if out else first
    cut = cut.strip(" ,;:-.")
    while cut and cut.split()[-1].lower().strip(" ,.;:-") in _DANGLING:
        cut = " ".join(cut.split()[:-1])
    cut = cut.strip(" ,;:-.")
    if cut.count("(") > cut.count(")"):
        cut = cut[:cut.index("(")].strip(" .;:-, ")
    if not cut:
        return ""
    return cut[0].upper() + cut[1:] + "."


def TAKES_AS_IT_COMES(text, memory):
    if not isinstance(text, str):
        return False
    return _a_limit(text) is not None and bool(_the_answer(memory))


def observe(text, memory):
    return None


def respond(text, memory):
    if not isinstance(text, str):
        return None
    read = _a_limit(text)
    if read is None:
        return None
    kind, about, leads = read
    record = _the_answer(memory)
    if record is None:
        return None
    answer = record["reply"]
    low = answer.lower()
    if not _the_answer_is_about(record, about):
        return None
    move = _the_move(answer)
    if not move:
        return None
    if kind == "rent" and "landlord" in low:
        return None
    turns = memory.get("turns") if isinstance(memory, dict) else None
    pick_from = len(turns) if isinstance(turns, list) else 0
    lead = leads[pick_from % len(leads)]
    reply = lead.format(move=move, move_lower=move[:1].lower() + move[1:])
    return " ".join(reply.split())
