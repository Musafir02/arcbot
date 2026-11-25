import re

_ANOTHER_SIZE = re.compile(r"\b(?:big|bigger|large|larger|small|smaller|little|littler|thicker|"
                           r"thinner|wider|narrower)\b", re.I)
_SIZE_WORD = r"(?:bigger|larger|smaller|littler|thicker|thinner|wider|narrower)"
_POINTS_BACK = re.compile(
    _SIZE_WORD + r"\s+(?:one|ones|version|size|sized|that|it|them|those|batch|tin|pot|dish|"
    r"piece|bird|cut|joint|loaf|pan|mug|cup|glass|portion|helping)\b"
    r"|\b(?:what about|and|how about|what if|or|then)\s+(?:a|an|the)?\s*"
    r"(?:bit\s+|little\s+|much\s+|whole\s+)?(?:a|an|the)?\s*" + _SIZE_WORD + r"\s*[?.!]*$",
    re.I)
_A_TIME = re.compile(r"\b\d+\s*(?:-|to)?\s*\d*\s*(?:minutes?|mins?|hours?|hrs?)\b|\b\d+\s*(?:per|a)\b|"
                     r"\b(?:an?|one|two|three|four|five|ten|twenty|thirty|forty|half an)\s+"
                     r"(?:minutes?|mins?|hours?|hrs?)\b", re.I)
_RULE_STOPS = re.compile(r",\s*(?:so|which) |; |\s-\s|\s\u2014\s")
_A_RATE = re.compile(r"\bper\s+(?:\d+\s*)?(?:g|kg|gram|grams|kilo|kilos|pound|pounds|lb|lbs|"
                     r"centimetre|centimetres|cm|inch|inches|litre|litres|person)\b|"
                     r"\bfor every\b|\beach\s+\d+", re.I)
_SENTENCE = re.compile(r"[^.!?]+[.!?]?")
BIGGER = ("Same rule, just a bigger sum: {rule}", "The rule works at any size: {rule}",
          "Same as before, and the sum does the work: {rule}")
SMALLER = ("Same rule, just a smaller sum: {rule}", "The rule works at any size: {rule}",
           "Same as before, and the sum does the work: {rule}")
SAID_BIGGER = ("That rule is the whole of it - the size goes into it and the time comes out.",
               "Same rule, still: nothing changes with a bigger one except the figure you put "
               "into it.",
               "It does not change with the size - put your figure into that rule and it holds.")
SAID_SMALLER = ("That rule is the whole of it - the size goes into it and the time comes out.",
                "Same rule, still: nothing changes with a smaller one except the figure you put "
                "into it.",
                "It does not change with the size - put your figure into that rule and it holds.")
MORE = ("A bigger one wants a few minutes more than that - same method, just check it later.",
        "Give a bigger one longer than those times: a few minutes more, and check it.",
        "Those times are for a normal one, so a bigger one takes a few minutes longer.")
LESS = ("A smaller one wants a few minutes less than that - same method, just check it earlier.",
        "Give a smaller one less time than that: a few minutes fewer, then check it.",
        "Those times are for a normal one, so a smaller one takes a few minutes less.")


def _flat(text):
    return " ".join(str(text or "").rstrip(".").split()).lower()


_OUR_SHORT_LINES = frozenset(_flat(shape)
                             for shape in MORE + LESS + SAID_BIGGER + SAID_SMALLER)
_OUR_RULE_LEADS = ("same rule, just a bigger sum:", "same rule, just a smaller sum:",
                   "the rule works at any size:", "same as before, and the sum does the work:")


def _one_of_ours(answer):
    flat = _flat(answer)
    if flat in _OUR_SHORT_LINES:
        return True
    return any(flat.startswith(lead) for lead in _OUR_RULE_LEADS)


_BY_WEIGHT = re.compile(r"\bper\s+(?:\d+\s*)?(?:g|kg|gram|grams|kilo|kilos|pound|pounds|lb|lbs)\b",
                        re.I)
_FOOD = (r"chickens?|birds?|turkeys?|duck|lamb|beef|pork|ham|roasts?|steaks?|chops?|fillets?|fish|"
         r"salmon|cod|trout|eggs?|potatoes|potato|onions?|carrots?|tomatoes|tomato|peppers?|"
         r"courgettes?|aubergines?|cabbage|squash|melon|sausages?|cakes?|loaf|loaves|bread|pizza|"
         r"pastry|pies?|tarts?|sponge|scones?|buns?|pancakes?")
_SIZED_THING = re.compile(r"\b(?:" + _FOOD + r")\b", re.I)
_SIZED_ASKED = re.compile(
    r"\b(?:" + _FOOD + r"|joints?|breasts?|thighs?|legs?|cuts?|tins?|pots?|pans?|dishes|trays?|"
    r"batches?|portions?|helpings?|mugs?|cups?|glasses)\b", re.I)


def _the_thing_asked(memory, text):
    here = _flat(text)
    turns = memory.get("turns") if isinstance(memory, dict) else None
    for turn in reversed(list(turns or [])):
        if not isinstance(turn, dict):
            continue
        asked = " ".join(str(turn.get("user") or "").split())
        if not asked or _flat(asked) == here:
            continue
        if _one_of_ours(str(turn.get("bot") or "")):
            continue
        return asked
    return ""


def _the_last_line(memory):
    turns = memory.get("turns") if isinstance(memory, dict) else None
    for turn in reversed(list(turns or [])):
        if isinstance(turn, dict) and turn.get("bot"):
            return str(turn.get("bot") or "").strip()
    return ""


def _the_answer(memory):
    turns = memory.get("turns") if isinstance(memory, dict) else None
    for turn in reversed(list(turns or [])):
        if not isinstance(turn, dict) or not turn.get("bot"):
            continue
        answer = str(turn.get("bot") or "").strip()
        if _one_of_ours(answer):
            continue
        if _A_TIME.search(answer):
            return answer
        return ""
    return ""


def _the_rule(answer):
    for sentence in _SENTENCE.finditer(answer or ""):
        said = sentence.group(0).strip()
        if not (_A_RATE.search(said) and _A_TIME.search(said)):
            continue
        after = said.rsplit(": ", 1)[1].strip() if ": " in said else ""
        for piece in (after, said):
            if not (_A_RATE.search(piece) and _A_TIME.search(piece)):
                continue
            stop = _RULE_STOPS.search(piece)
            if stop:
                piece = piece[:stop.start()].strip()
            if piece:
                return piece
    return ""


def answer_for(text, memory=None):
    if not isinstance(memory, dict):
        return None
    said = " ".join(str(text or "").strip().split())
    if not said or len(said.split()) > 8:
        return None
    if not (_ANOTHER_SIZE.search(said) and _POINTS_BACK.search(said)):
        return None
    answer = _the_answer(memory)
    if not answer:
        return None
    if not (_BY_WEIGHT.search(answer) or _SIZED_THING.search(answer)
            or _SIZED_ASKED.search(_the_thing_asked(memory, said))):
        return None
    bigger = not re.search(r"\b(?:small|smaller|little|littler|thinner|narrower)\b", said, re.I)
    which = int(memory.get("size_said") or 0)
    memory["size_said"] = which + 1
    rule = _the_rule(answer)
    if rule:
        if _one_of_ours(_the_last_line(memory)):
            answer_shapes = SAID_BIGGER if bigger else SAID_SMALLER
            return answer_shapes[which % len(answer_shapes)]
        shapes = BIGGER if bigger else SMALLER
        said = rule.rstrip(".")
        first = said.split()[0] if said.split() else ""
        if first and not (first.isupper() or first[:1].isdigit()):
            said = said[:1].lower() + said[1:]
        reply = shapes[which % len(shapes)].format(rule=said)
        return reply[:1].upper() + reply[1:] + "."
    shapes = MORE if bigger else LESS
    return shapes[which % len(shapes)]
