import re

from ..compose import pick

A_PRICE_ASK = re.compile(
    r"\b(?:is|was)\s+(?:that|this|it|(?:that|this)\s+[a-z]+)\s+(?:a\s+lot|expensive|dear|cheap|"
    r"about\s+right|the\s+going\s+rate|the\s+right\s+price|the\s+normal\s+price|normal|"
    r"reasonable|fair|too\s+much|steep|a\s+rip[-\s]?off|overpriced|in\s+line)\b"
    r"|\b(?:does|do|did)\s+(?:that|this|it)\s+(?:sound|seem)\s+(?:about\s+)?(?:right|ok|okay|"
    r"reasonable|fair|normal|expensive)\b"
    r"|\b(?:is|was)\s+(?:that|this|it)\s+(?:the\s+)?(?:going\s+rate|normal|what\s+it\s+should\s+be)\b"
    r"|\bam\s+i\s+being\s+(?:ripped\s+off|overcharged|done)\b"
    r"|\bdid\s+i\s+(?:get|pay)\s+(?:a\s+)?(?:good|fair|bad)\s+(?:price|deal|rate)\b"
    r"|\b(?:is|was)\s+(?:that|this|it)\s+(?:a\s+)?(?:good|fair|bad)\s+(?:price|deal|rate|quote)\b"
    r"|\b(?:that|this|it)(?:'s|s|\s+is|\s+was)?\s+(?:sounds?|seems?|looks?)\s+(?:like\s+)?"
    r"(?:a\s+lot|expensive|dear|steep|a\s+rip[-\s]?off|too\s+much|about\s+right|"
    r"the\s+going\s+rate|the\s+right\s+price)\b"
    r"|\b(?:that|this|it)\s*(?:'s|s|is|was)\s+(?:(?:very|really|quite|a\s+bit|bit|so|pretty|"
    r"rather)\s+)?(?:a\s+lot|expensive|dear|steep|too\s+much|a\s+rip[-\s]?off|overpriced)\b"
    r"|\b(?:sounds?|seems?|looks?)\s+(?:like\s+)?(?:(?:very|really|quite|a\s+bit|bit|so|pretty)\s+)?"
    r"(?:a\s+lot|expensive|dear|steep|too\s+much|"
    r"about\s+right|the\s+going\s+rate)\b"
    r"|\bhow\s+does\s+that\s+(?:sound|compare)\b"
    r"|\b(?:is|was)\s+(?:that|this|it)\s+(?:more|less)\s+than\s+(?:usual|normal|it\s+should\s+be)\b",
    re.I)

_PRICE_SYMBOL = re.compile(r"£|\$|€")
_PRICE_WORD = re.compile(r"\b(?:quid|pounds?|pence|euros?|dollars?|grand|notes?|money|"
                         r"cost(?:s|ing)?|costs?|price[sd]?|quoted?|quote[sd]?|charge[ds]?|"
                         r"(?:pay|pays|paying|paid|payed)|wants?|wanting|asking|budget|spent|spend|"
                         r"cheapest|dearest|expensive|cheaper|dearer|fees?|bill|bills|"
                         r"invoice|estimate[d]?|rates?)\b", re.I)
_AFTER_A_RATE = re.compile(r"\s*(?:a|an|per|each|every)\s+(day|week|month|year|hour|visit|"
                           r"call[-\s]?out|session|night)\b", re.I)
_A_MONEY_CEILING = re.compile(r"\b(?:up\s+to|no\s+more\s+than|at\s+most|under|below|less\s+than|"
                              r"over|more\s+than|above|at\s+least)\s*$", re.I)
_PRICE_RANGE = re.compile(
    r"(?P<low>£|\$|€)?\s?(?P<low_n>\d[\d,]*(?:\.\d+)?)\s?"
    r"(?:(?:-|–|—|to)\s?|(?<![,])\s+and\s+)"
    r"(?:(?P<high>£|\$|€)\s?)?(?P<high_n>\d[\d,]*(?:\.\d+)?)"
    r"\s?(?P<unit>k\b|pounds?|quid|euros?|dollars?|grand)?", re.I)


def _money(value):
    if value >= 1000:
        return "{:,}".format(int(value)) if float(value).is_integer() else "{:,.2f}".format(value)
    return ("%d" % value) if float(value).is_integer() else ("%.2f" % value)


def _a_value(token):
    try:
        return float(str(token).replace(",", ""))
    except (TypeError, ValueError):
        return 0.0


def _the_money_said_back(said, text):
    said = str(said or "").strip()
    if re.match(r"[£$€]", said):
        return said
    for mark in ("£", "$", "€"):
        if mark in str(text or ""):
            return mark + said
    return "£" + said


def _the_price_said(value):
    return "£" + _money(value)


A_PRICE_SYMBOL_ONLY = re.compile(r"[£$€]")


def _the_figure_in_the_range_s_style(mine, said, range_said):
    figure = said or _money(mine)
    figure = re.sub(r"\d[\d,]*(?:\.\d+)?",
                    lambda one: _money(_a_value(one.group(0))), figure)
    mark = A_PRICE_SYMBOL_ONLY.search(str(range_said or ""))
    if mark and not A_PRICE_SYMBOL_ONLY.search(figure):
        return mark.group(0) + figure
    return figure


def _number_tokens(text):
    return [(match.group(0), match.start()) for match in
            re.finditer(r"\d[\d,]*(?:\.\d+)?", str(text or ""))]


def _prices_in(text):
    said = str(text or "")
    found = []
    for token, start in _number_tokens(said):
        value = _a_value(token)
        if not value:
            continue
        before = said[max(0, start - 24):start]
        after = said[start + len(token):start + len(token) + 20]
        marked = bool(_PRICE_SYMBOL.search(before + token + after[:1])) \
            or bool(_PRICE_WORD.search(before)) \
            or bool(re.match(r"\s?(?:quid|pounds|euros?|dollars?|grand|k)\b", after, re.I))
        if not marked:
            continue
        if _AFTER_A_RATE.match(after):
            continue
        thousands = re.match(r"\s?(k|grand|thousand)\b", after, re.I)
        spoken = token.strip(" ,")
        if thousands:
            value = value * 1000
            spoken = said[start:start + len(token) + len(thousands.group(0))].strip(" ,")
        found.append((value, spoken))
    return found


def _a_price_at_a_rate(text):
    said = str(text or "")
    figures = [match for match in re.finditer(
        r"(?:£|\$|€)?\s?\d[\d,]*(?:\.\d+)?(?:\s?(?:k|pounds|quid))?", said)]
    if not figures:
        return False
    for match in figures:
        if not _AFTER_A_RATE.match(said[match.end():match.end() + 20]):
            return False
    return True


def _price_ranges_in(text, period=None):
    said = str(text or "")
    found = []
    for match in _PRICE_RANGE.finditer(said):
        low_token, high_token = match.group("low_n"), match.group("high_n")
        try:
            low = _a_value(low_token)
            high = _a_value(high_token)
        except (TypeError, ValueError):
            continue
        if not low or not high or high <= low:
            continue
        tail = said[match.end():match.end() + 20]
        head = said[max(0, match.start() - 24):match.start()]
        unit = match.group("unit") or ""
        marked = bool(match.group("low") or match.group("high")) \
            or bool(unit and unit.lower() not in ("k",)) \
            or bool(_PRICE_SYMBOL.search(text[max(0, match.start() - 3):match.end() + 3])) \
            or bool(_PRICE_WORD.search(head)) \
            or bool(_PRICE_WORD.search(tail))
        if not marked:
            continue
        rate = _AFTER_A_RATE.match(tail)
        if rate and (period or "") != rate.group(1).lower():
            continue
        if unit.lower() == "k":
            low, high = low * 1000, high * 1000
        spoken = said[match.start():match.end()].strip()
        spoken = re.sub(r"\s+", " ", spoken).strip(" ,.;:")
        if _A_MONEY_CEILING.search(head):
            continue
        found.append((match.start(), match.end(), low, high, spoken))
    return found


def _the_price_they_gave(text, memory):
    turns = memory.get("turns") if isinstance(memory, dict) else None
    lines = [text] + [str(turn.get("user") or "") for turn in list(reversed(turns or []))[:3]
                      if isinstance(turn, dict)]
    for line in lines:
        marked = _prices_in(line)
        if marked:
            return marked[-1]
        bare = [(value, token) for value, token in
                ((_a_value(token), token.strip(" ,")) for token, _ in _number_tokens(line))
                if value >= 40]
        if not bare:
            continue
        if _PRICE_WORD.search(line):
            return bare[-1]
        return None, ""
    return None, ""


def _a_bare_price_in_the_thread(text, memory):
    turns = memory.get("turns") if isinstance(memory, dict) else None
    lines = [text] + [str(turn.get("user") or "") for turn in list(reversed(turns or []))[:3]
                      if isinstance(turn, dict)]
    for line in lines:
        if _prices_in(line):
            continue
        bare = [value for value in (_a_value(token) for token, _ in _number_tokens(line))
                if value >= 40]
        if bare:
            return bare[0], _the_price_said(bare[0])
    return None, ""


def _answers_in(turns):
    found = []
    for turn in reversed(list(turns or [])):
        if not isinstance(turn, dict):
            continue
        said = turn.get("bot") or turn.get("reply")
        if isinstance(said, str) and said.strip():
            found.append(said)
    return found


def _the_range_that_is_about_it(answers, price, period=None):
    for said in answers[:2]:
        found = _the_ranges_that_are_not_rates(said, _price_ranges_in(said, period))
        if not found:
            continue
        bands = [(item[2], item[3], item[4]) for item in found]
        if all(price < low for low, _, _ in bands):
            return min(bands)
        if all(price > high for _, high, _ in bands):
            return max(bands, key=lambda band: band[1])
        scored = []
        for low, high, spoken in bands:
            if low <= price <= high:
                distance = 0.0
            elif price > high:
                distance = price - high
            else:
                distance = low - price
            scored.append((distance, low, high, spoken))
        scored.sort()
        best = scored[0]
        if price > best[2] and price > best[2] * 3:
            continue
        if price < best[1] and price * 3 < best[1]:
            continue
        if len(scored) > 1:
            near, second = scored[0][0], scored[1][0]
            if near and second < near * 2:
                continue
        return best[1], best[2], best[3]
    return None


A_PRICE_INSIDE = (
    "That is about right. The usual range is {aim}, and {price} is inside it.",
    "Yes, {price} is in the right range - the answer there put it at {aim}.",
    "{price} sits inside the usual range of {aim}, so that is the going rate.",
)
A_PRICE_OVER = (
    "That is above the going rate of {aim}, so it is worth checking what is behind it.",
    "{price} is over the {aim} the usual price comes to, so it is worth a second quote.",
    "That is on the high side: the range is {aim}, and {price} is above it.",
)
A_PRICE_UNDER = (
    "That is below the usual {aim}, so check what it covers - a part, a deposit, or the "
    "whole job.",
    "{price} is under the {aim} it usually comes to, so check what the quote leaves out.",
    "That is cheap against the {aim} the answer named, so make sure the price covers the job.",
)


A_PRICE_BETWEEN = (
    "{price} is over the {below} and under the {above}, so it depends which of those you had.",
    "{price} falls between the {below} and the {above} - which of those you had decides whether "
    "it is fair.",
)


def _the_between_verdict(mine, said, below, above, memory):
    price = _the_figure_in_the_range_s_style(mine, said, below)
    line = pick(list(A_PRICE_BETWEEN), memory, "between" + str(mine))
    if not line:
        return None
    try:
        return line.format(price=price, below=below, above=above,
                           Price=price[:1].upper() + price[1:])
    except (KeyError, IndexError, ValueError):
        return None


def _the_verdict(mine, said, low, high, spoken, memory, own=False):
    price = _the_figure_in_the_range_s_style(mine, said, spoken)
    if low <= mine <= high:
        pool, told = A_PRICE_INSIDE, "inside"
    elif mine > high:
        pool, told = A_PRICE_OVER, "over"
    else:
        pool, told = A_PRICE_UNDER, "under"
    lines = list(pool)
    if own:
        stood = [line for line in lines if "the answer" not in line]
        lines = stood or lines
    line = pick(lines, memory, told + str(mine))
    if not line:
        return None
    try:
        return line.format(aim=spoken, price=price,
                           Price=price[:1].upper() + price[1:])
    except (KeyError, IndexError, ValueError):
        return None


A_PRICE_ASK_WITH_THE_THING = re.compile(
    r"\b(?:is|was)\s+(?P<figure>[^,.?!]{0,40}?)\s*(?:too\s+much|a\s+lot|expensive|dear|steep|"
    r"a\s+rip[-\s]?off|about\s+right|reasonable|fair|the\s+going\s+rate|the\s+normal\s+price|"
    r"the\s+right\s+price|(?:a|an)\s+(?:good|fair|reasonable|normal|ok|okay)\s+(?:price|deal|"
    r"rate|quote))\b",
    re.I)

_A_PRICE_FOR_THE_THING = re.compile(r"\b(?:for|on)\s+(?:a|an|the|my|our|your|his|her|their|this|"
                                    r"that)?\s*[a-z]", re.I)

_ASK_WORDS = {
    "much", "lot", "expensive", "dear", "steep", "rip", "off", "right", "reasonable", "fair",
    "going", "rate", "normal", "price", "prices", "good", "ok", "okay", "deal", "quote", "quoted",
    "cost", "costs", "costing", "charge", "charged", "charges", "paid", "pay", "paying", "payed",
    "was", "is", "did", "does", "do", "for", "to", "the", "a", "an", "and", "on", "of", "in",
    "it", "that", "this", "me", "my", "we", "i", "at", "just", "only", "about", "bit", "little",
    "total", "altogether", "bill", "quid", "pounds", "pound", "euro", "euros", "dollar", "dollars",
    "worth", "sound", "sounds", "seem", "seems", "again", "too", "get", "got", "all", "so",
}


def _the_thing_priced(text):
    left = _PRICE_SYMBOL.sub(" ", str(text or ""))
    left = re.sub(r"\d[\d,.]*", " ", left).lower()
    words = [word for word in re.findall(r"[a-z']+", left) if word not in _ASK_WORDS]
    return " ".join(words)


def _the_price_they_mean(text, memory):
    mine, said = _the_price_they_gave(text, memory)
    if not mine:
        mine, said = _a_bare_price_in_the_thread(text, memory)
    return mine, said


def _the_period_they_said(text, memory):
    turns = memory.get("turns") if isinstance(memory, dict) else None
    lines = [text] + [str(turn.get("user") or "") for turn in list(reversed(turns or []))[:3]
                      if isinstance(turn, dict)]
    for line in lines:
        found = re.search(r"\b(?:a|an|per|each|every|this|last)\s+"
                          r"(day|week|month|year|hour|night)\b", line, re.I)
        if found:
            return found.group(1).lower()
    return None


_A_MONEY_AFTER_THE_ASK = {
    "money", "quid", "pounds", "pound", "euros", "euro", "dollars", "dollar", "pence",
    "grand", "notes", "cash", "dosh", "price", "prices", "rate", "rates", "bill", "total",
}
_A_PHRASE_AFTER_THE_ASK = {
    "to", "for", "on", "in", "at", "by", "with", "per", "and", "or", "but", "if", "than",
    "compared", "when", "these", "those", "this", "that", "it", "now", "nowadays", "then",
    "though", "anyway", "honestly", "really", "actually", "do", "does", "did", "should",
    "would", "a", "an", "the", "so", "again", "altogether", "all", "any", "as", "from",
    "about", "worth", "sounds", "seems", "sound", "seem", "overall", "including",
}


def _a_price_ask(text):
    found = A_PRICE_ASK.search(text)
    if not found:
        return None
    tail = re.sub(r"^\s*of\b", "", text[found.end():], flags=re.I)
    words = re.findall(r"[a-z']+", tail.lower())
    if not words:
        return found
    first = words[0]
    if found.group(0).lower().endswith("a lot") and first == "of":
        return found if len(words) > 1 and words[1] in _A_MONEY_AFTER_THE_ASK else None
    if first in _A_MONEY_AFTER_THE_ASK or first in _A_PHRASE_AFTER_THE_ASK:
        return found
    return None


def _a_rate_is_all_the_answer_names(answers):
    for said in answers[:1]:
        found = _price_ranges_in(said)
        if found and not _the_ranges_that_are_not_rates(said, found):
            return True
    return False


def _a_second_quote_is_the_test(memory):
    from ..compose.prices import A_JOB_JUDGED
    return pick(list(A_JOB_JUDGED), memory, "jobjudged")


def judged(text, memory):
    if not isinstance(text, str) or not isinstance(memory, dict):
        return None
    if not _a_price_ask(text):
        return None
    turns = memory.get("turns")
    answers = _answers_in(turns)
    if not answers:
        return None
    mine, said = _the_price_they_mean(text, memory)
    if not mine:
        return None
    said = _the_money_said_back(said, text)
    period = _the_period_they_said(text, memory)
    aim = _the_range_that_is_about_it(answers, mine, period)
    if aim is None:
        if not period and _a_rate_is_all_the_answer_names(answers):
            return _a_second_quote_is_the_test(memory)
        return None
    low, high, spoken = aim
    return _the_verdict(mine, said, low, high, spoken, memory)


def judged_with_the_card(text, answer, memory):
    if not isinstance(text, str) or not isinstance(answer, str):
        return None
    asked = A_PRICE_ASK_WITH_THE_THING.search(text)
    if not asked:
        return None
    if not _the_thing_priced(text):
        return None
    tokens = _number_tokens(asked.group("figure"))
    if tokens:
        try:
            mine = _a_value(tokens[-1][0])
        except (TypeError, ValueError):
            return None
        if mine and _AFTER_A_RATE.match(text[tokens[-1][1]:tokens[-1][1] + 12] or ""):
            return None
    else:
        marked = _prices_in(text)
        mine = marked[-1][0] if marked else None
        if not mine:
            return None
        if not _A_PRICE_FOR_THE_THING.search(text):
            return None
    if not mine:
        return None
    said = _the_price_said(mine)
    verdict = _the_verdict_against_a_card(mine, said, answer, memory, definite_only=True)
    if verdict:
        return verdict
    opening = re.split(r"(?<=[.!?])\s", answer.strip(), maxsplit=1)[0]
    if opening != answer:
        verdict = _the_verdict_against_a_card(mine, said, opening, memory)
        if verdict:
            return verdict
    return _the_verdict_against_a_card(mine, said, answer, memory)


_A_RATE_IN_THE_SENTENCE = re.compile(
    r"\b(?:a|an|per|each)\s+(?:day|hour|week|month|night|visit|person|load)\b", re.I)


def _the_ranges_that_are_not_rates(answer, ranges):
    kept = []
    for item in ranges:
        start, end = item[0], item[1]
        left = max(answer.rfind(".", 0, start), answer.rfind("\n", 0, start))
        after = [at for at in (answer.find(".", end), answer.find("\n", end)) if at != -1]
        right = min(after) if after else len(answer)
        sentence = answer[left + 1:right]
        if _A_RATE_IN_THE_SENTENCE.search(sentence) \
                and not _AFTER_A_RATE.match(answer[end:end + 20]):
            continue
        kept.append(item)
    return kept


def _the_verdict_against_a_card(mine, said, answer, memory, definite_only=False):
    ranges = _the_ranges_that_are_not_rates(answer, _price_ranges_in(answer))
    if not ranges:
        return None
    holds = [item for item in ranges if item[2] <= mine <= item[3]]
    if holds:
        _, _, low, high, spoken = holds[0]
        return _the_verdict(mine, said, low, high, spoken, memory, own=True)
    if all(item[2] > mine for item in ranges):
        _, _, low, high, spoken = min(ranges, key=lambda item: item[2])
        return _the_verdict(mine, said, low, high, spoken, memory, own=True)
    if all(item[3] < mine for item in ranges):
        _, _, low, high, spoken = max(ranges, key=lambda item: item[3])
        return _the_verdict(mine, said, low, high, spoken, memory, own=True)
    if definite_only:
        return None
    under = [item for item in ranges if item[3] < mine]
    over = [item for item in ranges if item[2] > mine]
    if under and over:
        near = max(under, key=lambda item: item[3])
        far = min(over, key=lambda item: item[2])
        if far[2] - near[3] <= near[3] - near[2]:
            return _the_between_verdict(mine, said, near[4], far[4], memory)
        return _the_verdict(mine, said, near[2], near[3], near[4], memory, own=True)
    return None
