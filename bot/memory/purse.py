import re

_A_MONEY = re.compile(
    r"\u00a3\s*(?P<mark>\d+(?:,\d{3})*(?:\.\d+)?)"
    r"|(?P<word>\d+(?:,\d{3})*(?:\.\d+)?)\s*(?:pounds?|quid|gbp)\b",
    re.I,
)
_A_MONEY_BAND = re.compile(
    r"\u00a3\s*(?P<a1>\d+(?:,\d{3})*(?:\.\d+)?)\s*(?:to|and|or|-|\u2013)\s*\u00a3?\s*"
    r"(?P<a2>\d+(?:,\d{3})*(?:\.\d+)?)"
    r"|(?P<b1>\d+(?:,\d{3})*(?:\.\d+)?)\s*(?:to|and|or|-|\u2013)\s*"
    r"(?P<b2>\d+(?:,\d{3})*(?:\.\d+)?)\s*(?:pounds?|quid)\b",
    re.I,
)
_A_CLAUSE_END = re.compile(r"[.!?;]|\s+-\s+|\u2014|,\s+(?:and|or|but|so)\s+|,\s+")
_A_VERB_FIRST = re.compile(
    r"^(?:buys?|covers?|gets?|is|are|was|were|will|goes?|holds?|pays?|takes?|does|fits?|lasts?|"
    r"means|comes?|makes?|gives?|finds?)\b", re.I)
_A_RATE_BAND = re.compile(
    r"^\s*(?:\(?\s*)?(?:a|per|each|every)\s+(?:day|night|week|month|person|head|hour)\b", re.I)


def _a_number(word):
    word = (word or "").strip().lower()
    if re.fullmatch(r"\d+(?:,\d{3})*(?:\.\d+)?", word):
        return float(word.replace(",", ""))
    return 0.0


def _money_in(text):
    found = []
    for match in _A_MONEY.finditer(text or ""):
        value = _a_number(match.group("mark") or match.group("word"))
        if value:
            found.append(value)
    return found


def _the_money(value):
    if float(value).is_integer():
        return "\u00a3{:,}".format(int(value))
    return "\u00a3%.2f" % value


def _the_words_after(answer, at):
    rest = (answer or "")[at:]
    cut = _A_CLAUSE_END.search(rest)
    words = (rest[:cut.start()] if cut else rest).strip(" ,;:-")
    if not words or len(words.split()) > 12:
        return ""
    if "\u00a3" in words or any(re.fullmatch(r"\d[\d,]*\.?\d*", one) for one in words.split()):
        return ""
    return words


def _money_bands(answer):
    bands = []
    for match in _A_MONEY_BAND.finditer(answer or ""):
        first = match.group("a1") or match.group("b1")
        second = match.group("a2") or match.group("b2")
        low, high = _a_number(first), _a_number(second)
        if not (low and high) or low >= high:
            continue
        if _A_RATE_BAND.match((answer or "")[match.end():]):
            continue
        bands.append((low, high, _the_words_after(answer, match.end())))
    return bands


def against_the_bands(text, turns):
    theirs = _money_in(text)
    if not theirs:
        for turn in reversed(list(turns or [])[-3:]):
            if not isinstance(turn, dict):
                continue
            theirs = _money_in(str(turn.get("user") or ""))
            if theirs:
                break
    if not theirs:
        return None
    mine = theirs[-1]
    for turn in reversed(list(turns or [])[-2:]):
        answer = str(turn.get("bot") or "") if isinstance(turn, dict) else ""
        bands = _money_bands(answer)
        if bands:
            break
    else:
        return None
    spoken = _the_money(mine)
    inside = [band for band in bands if band[0] <= mine <= band[1]]
    if inside:
        low, high, after = inside[0]
        said = "%s to %s" % (_the_money(low), _the_money(high))
        if not after:
            return "%s is inside the %s that answer named." % (spoken, said)
        if _A_VERB_FIRST.match(after):
            return "%s is inside the %s that answer named, and that %s." % (spoken, said, after)
        return "%s is inside the %s that answer named: %s." % (spoken, said, after)
    above = sorted((band for band in bands if band[0] > mine), key=lambda band: band[0])
    if not above:
        return None
    return "%s is under the %s that answer named." % (
        spoken, "%s to %s" % (_the_money(above[0][0]), _the_money(above[0][1])))
