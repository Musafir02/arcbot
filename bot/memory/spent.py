import re

_MONEY = r"(\d{1,7}(?:\.\d{1,2})?)"
_CURRENCY = r"(?:\s*(?:pounds?|quid|p\b|gbp))?"
SPENT = re.compile(
    r"\b(?:i|we|he|she|they)(?:'ve|'s|'d)?\s+(?:have\s+|had\s+|already\s+)*"
    r"(?:spent|paid|forked out|shelled out)\s+"
    r"(?:about|around|nearly|almost|just|only|maybe|like|over|under|another)?\s*"
    r"£?\s*" + _MONEY + _CURRENCY + r"\s*(?:(?:on|for|in)\s+)?(.*)$", re.I)
COST = re.compile(r"\b(?:it|that|this|the\s+[a-z]+)\s+cost\s+(?:me\s+)?(?:about\s+|around\s+|"
                  r"nearly\s+|just\s+|only\s+)?£?\s*" + _MONEY + _CURRENCY + r"\s*(.*)$", re.I)
BARE_ON = re.compile(r"^\s*(?:(?:and|then|also|so)\s+)*(?:another\s+)?£?\s*" + _MONEY +
                     _CURRENCY + r"\s+(?:on|for)\s+(.+)$", re.I)

_WHEN_TAIL = re.compile(
    r"\s*\b(?:this|last|next|the)\s+(?:morning|afternoon|evening|night|week|weekend|month|year)\b.*$"
    r"|\s*\b(?:today|yesterday|tonight|already|so far|altogether|in all|last night|"
    r"at the weekend|on saturday|on sunday|on monday|on tuesday|on wednesday|on thursday|"
    r"on friday)\b.*$", re.I)
_TAIL_OFF = re.compile(r"\s*\b(?:too|as well|also|again|though|now|anyway)\b\s*$", re.I)
_TRAILING = re.compile(r"[\s.,;:!?-]+$")

ASK = re.compile(
    r"\bhow\s+much\s+(?:have|has|did)\s+(?:i|we)\s+(?:spent|spend|pay|paid)\b"
    r"|\bwhat\s+(?:have|has|did)\s+(?:i|we)\s+spent\b"
    r"|\bhow\s+much\s+(?:has|did)\s+(?:it|that|this)\s+cost\b"
    r"|\bwhat\s+(?:have|did)\s+(?:i|we)\s+spend\b"
    r"|\bhow\s+much\s+(?:money\s+)?(?:have\s+i|did\s+i)\s+(?:spent|spend)\b", re.I)
ON_A_THING = re.compile(r"\b(?:on|for)\s+([a-z][a-z' -]{1,30}?)"
                        r"(?:\s+(?:this|last|so far|altogether|in all)\b.*)?\s*[?.!]*\s*$", re.I)
_ASK_FILLER = frozenset("""
so far altogether in all in total total now this month week year today all
""".split())


CATEGORIES = (
    ("food", ("food", "groceries", "grocery", "shopping", "supermarket", "takeaway", "takeaways",
              "restaurant", "eating out", "lunch", "dinner", "breakfast", "brunch", "coffee",
              "snack", "snacks", "meal", "meals", "pizza", "curry", "chinese", "milk", "bread",
              "veg", "fruit", "meat", "booze", "beer", "wine")),
    ("petrol", ("petrol", "fuel", "diesel", "petrol station", "gas")),
    ("travel", ("train", "trains", "bus", "buses", "travel", "transport", "taxi", "uber", "tube",
                "train fare", "flights", "flight", "coach", "parking")),
    ("bills", ("bills", "bill", "electric", "electricity", "water", "council tax", "rent",
               "mortgage", "broadband", "internet", "phone", "gas bill", "energy")),
    ("kids", ("kids", "children", "childcare", "school", "nursery", "childminder")),
)

def _amount(number):
    return (number or "").strip()


def _the_thing(rest):
    rest = (rest or "").strip()
    if not rest:
        return ""
    rest = re.split(r"[,;.]", rest)[0]
    rest = re.sub(r"^(?:at|in|on|for)\s+", "", rest, flags=re.I) if rest.lower().startswith(
        ("at ", "in ")) else rest
    rest = _WHEN_TAIL.sub("", rest)
    rest = _TAIL_OFF.sub("", rest)
    rest = _TRAILING.sub("", rest).strip()
    return rest if len(rest) > 1 else ""


_TWO_SPENDS = re.compile(r"(?=[,;]\s*(?:and\s+)?£?\d|\s+and\s+£?\d)", re.I)


_SAID_AS_A_COST = re.compile(
    r"\b(?:my|our|the)\s+([a-z][a-z' -]{1,24}?)\s+(?:is|are|comes? to|works out at)\s*"
    r"£?(\d[\d,]*(?:\.\d{1,2})?)\s*(k|p|pounds?|quid|gbp)?\b", re.I)
_PEOPLE = frozenset("""
kid kids child children baby babies toddler boy boys girl girls lad lass son sons daughter
daughters twin twins nephew niece grandchild grandchildren grandson granddaughter mum mom
dad stepson stepdaughter
""".split())
_TWO_FIGURES = re.compile(r"^\s*(?:,|and|&|or)\s*\d{1,3}\b")


_A_PERIOD = r"(?:a|an|per|each|every)\s+(?:month|week|fortnight|year)"
_PAY_FOR = re.compile(
    r"\b(?:i|we)\s+pay\s+(?:about|around|just|only|roughly|like\s+)?£?(\d[\d,]*(?:\.\d{1,2})?)"
    r"\s*(k|p|pounds?|quid|gbp)?\s+" + _A_PERIOD +
    r"\s+(?:for|on)\s+(?:my|our|the)?\s*([a-z][a-z' -]{1,24})", re.I)
_PAY_THING = re.compile(
    r"\b(?:i|we)\s+pay\s+(?:about|around|just|only|roughly|like\s+)?£?(\d[\d,]*(?:\.\d{1,2})?)"
    r"\s*(k|p|pounds?|quid|gbp)?\s+(?!a\s+|an\s+|the\s+|per\s+)([a-z][a-z' -]{2,24}?)\s+"
    + _A_PERIOD, re.I)


def _a_bill(text):
    for pattern, amount_group, thing_group, currency_group in (
            (_SAID_AS_A_COST, 2, 1, 3), (_PAY_FOR, 1, 3, 2), (_PAY_THING, 1, 3, 2)):
        match = pattern.search(text)
        if not match:
            continue
        thing = (match.group(thing_group) or "").strip(" .,")
        if not _family(thing):
            continue
        if not match.group(currency_group) and _an_age_not_a_bill(match, thing, pattern):
            continue
        return {"amount": _amount(match.group(amount_group)), "thing": thing}
    return None


def _an_age_not_a_bill(match, thing, pattern):
    if pattern is not _SAID_AS_A_COST:
        return False
    if set(thing.lower().split()) & _PEOPLE:
        return True
    return bool(_TWO_FIGURES.match(match.string[match.end():] or ""))


def _one(text):
    match = SPENT.search(text)
    if match:
        return {"amount": _amount(match.group(1)), "thing": _the_thing(match.group(2))}
    match = COST.search(text)
    if match:
        return {"amount": _amount(match.group(1)), "thing": _the_thing(match.group(2))}
    match = BARE_ON.match(text)
    if match:
        return {"amount": _amount(match.group(1)), "thing": _the_thing(match.group(2))}
    return _a_bill(text)


_PLAIN = re.compile(r"\b(ive|weve|theyve|youve|hes|shes|im)\b", re.I)
_PLAIN_BACK = {"ive": "i've", "weve": "we've", "theyve": "they've", "youve": "you've",
               "hes": "he's", "shes": "she's", "im": "i'm"}


def _plain(text):
    return _PLAIN.sub(lambda m: _PLAIN_BACK[m.group(1).lower()], text)


def readings(line):
    text = _plain(" ".join(str(line or "").split()))
    if not text or "?" in text:
        return []
    found = []
    for clause in _TWO_SPENDS.split(text):
        spend = _one(clause)
        if spend:
            found.append(spend)
    return found


def reading(line):
    found = readings(line)
    return found[0] if found else None


def the_lines(memory, text=None):
    lines = []
    turns = memory.get("turns") if isinstance(memory, dict) else None
    for turn in turns if isinstance(turns, list) else ():
        said = str((turn or {}).get("user") or "") if isinstance(turn, dict) else ""
        if said.strip():
            lines.append(said)
    if text and (not lines or lines[-1] != text):
        lines.append(str(text))
    return lines


def the_spends(memory, text=None):
    found = []
    for line in the_lines(memory, text):
        for spend in readings(line):
            spend["line"] = line
            found.append(spend)
    return found


PRESENT_ASK = re.compile(
    r"\bhow\s+much\s+(?:do|does)\s+(?:i|we)\s+(?:spend|pay)\b"
    r"|\bwhat\s+(?:do|does)\s+(?:i|we)\s+spend\b"
    r"|\bhow\s+much\s+(?:is|are|was|were)\s+(?:my|our)\b", re.I)
A_POSSESSIVE_ASK = re.compile(
    r"\bhow\s+much\s+(?:is|are|was|were)\s+(?:my|our)\s+([a-z][a-z' -]{1,30}?)\s*[?.!]*\s*$",
    re.I)


def _named(thing, wanted):
    thing, wanted = (thing or "").lower().strip(), (wanted or "").lower().strip()
    if not thing or not wanted:
        return False
    if wanted in thing or thing in wanted:
        return True
    return bool(wanted.rstrip("s")) and wanted.rstrip("s") in thing


def _about(thing, wanted):
    thing, wanted = thing.lower(), wanted.lower().strip()
    if not wanted:
        return True
    if not thing:
        return False
    if wanted in thing or thing in wanted or (
            wanted.rstrip("s") and wanted.rstrip("s") in thing):
        return True
    return not _family(thing).isdisjoint(_family(wanted))


def _family(thing):
    words = set()
    low = thing.lower()
    for name, members in CATEGORIES:
        if name in low or any(member in low for member in members):
            words.add(name)
            words.update(members)
    return words


def the_total(spends):
    total = 0.0
    for spend in spends:
        try:
            total += float(spend.get("amount") or 0)
        except (TypeError, ValueError):
            continue
    if not total:
        return ""
    if abs(total - round(total)) < 0.005:
        return str(int(round(total)))
    return "%.2f" % total


def _listed(spends):
    parts = []
    for spend in spends:
        thing = spend.get("thing")
        parts.append(spend["amount"] + (" on " + thing if thing else ""))
    if len(parts) == 1:
        return parts[0]
    return ", ".join(parts[:-1]) + " and " + parts[-1]


def answer(text, memory):
    said = " ".join(str(text or "").split())
    if not said:
        return None
    past = bool(ASK.search(said))
    present = bool(PRESENT_ASK.search(said)) and not past
    if not past and not present:
        return None
    wanted = ""
    on = ON_A_THING.search(said)
    if on:
        wanted = " ".join(word for word in on.group(1).split()
                          if word.lower() not in _ASK_FILLER)
    if present:
        if not wanted:
            mine = A_POSSESSIVE_ASK.search(said)
            if mine:
                wanted = " ".join(word for word in mine.group(1).split()
                                  if word.lower() not in _ASK_FILLER)
        if not wanted:
            return None
        spends = [spend for spend in the_spends(memory, said)
                  if _named(spend.get("thing") or "", wanted)]
        if not spends:
            return None
    else:
        spends = the_spends(memory, said)
    if wanted:
        spends = [spend for spend in spends if _about(spend.get("thing") or "", wanted)]
        if not spends:
            return ("You haven't told me what you spent on " + wanted +
                    ". Tell me and I'll keep a tally.")
        if len(spends) == 1:
            return "You told me " + _listed(spends) + "."
        return ("You've told me " + _listed(spends) + " - " + the_total(spends) +
                " on " + wanted + " in all.")
    if not spends:
        return ("You haven't told me what you've spent yet. Tell me the sums as they go out "
                "and I'll keep a tally.")
    if len(spends) == 1:
        return ("You've told me " + _listed(spends) + ". Tell me the rest and I'll keep a "
                "tally.")
    return ("You've told me " + _listed(spends) + " - " + the_total(spends) + " in all.")


_HELD_SCALE = r"(\s*(?:k\b|thousand\b|grand\b|p\b|pounds?|quid|gbp))?"

HELD = re.compile(
    r"\b(?:i|we)(?:'ve|'d|\s+have|\s+had)?\s+(?:only\s+|just\s+)?(?:got\s+|have\s+)?"
    r"(?:only\s+|just\s+|about\s+|around\s+|maybe\s+|like\s+)*£?\s*" + _MONEY +
    _HELD_SCALE + r"(.*)$", re.I)
BUDGET_HELD = re.compile(
    r"\b(?:my|our)\s+budget(?:\s+is|'?s|\s+of)?\s+(?:only\s+|just\s+|about\s+|around\s+|"
    r"maybe\s+)?£?\s*" + _MONEY + _HELD_SCALE, re.I)
SAVINGS_HELD = re.compile(
    r"\b(?:my|our)\s+(?:savings|saving)\s+(?:are|is|stand\s+at|come\s+to)\s+(?:only\s+|"
    r"just\s+|about\s+|around\s+|maybe\s+)?£?\s*" + _MONEY +
    r"(?!\s*(?:k|p)\b)", re.I)
ON_A_BUDGET = re.compile(
    r"\b(?:i|we)(?:'m|'re|'ve)?\s+(?:on|working\s+to|sticking\s+to|sticking\s+with)\s+a\s+"
    r"budget\s+of\s+(?:only\s+|just\s+|about\s+|around\s+|maybe\s+)?£?\s*" + _MONEY +
    r"(\s*(?:k\b|p\b|pounds?|quid|gbp))?", re.I)
THERE_LEFT = re.compile(
    r"\bthere(?:'s|s|\s+is|\s+are|\s+was)\s+(?:only\s+|just\s+|about\s+|around\s+|"
    r"maybe\s+|like\s+|still\s+|nearly\s+)*(?:a\s+)?£?\s*" + _MONEY +
    r"(\s*(?:k\b|p\b|pounds?|quid|gbp))?(?=\s*(?:left|remaining|to\s+last)\b)", re.I)
_A_COUNTED_NOUN = re.compile(r"\b\d+\s+([a-z]{3,}(?:s|es))\b", re.I)
_A_CURRENCY_PLURAL = ("pounds", "quid", "euros", "dollars", "bucks", "pence", "pennies",
                      "cents", "sterling")
_A_TIME_SCOPE = (r"(?![ \t]*(?:" + "|".join((r"week", r"weekend", r"month", r"day",
                                            r"days", r"year", r"fortnight", r"holiday",
                                            r"holidays", r"term", r"morning", r"evening",
                                            r"night", r"month\s+end")) + r")\b)")
_A_SCOPE_OF_A_THING = re.compile(
    r"\b(?:left|remaining)\s+(?:over\s+)?(?:of|in|on|from|at|for)\s+"
    r"(?:the|a|an|my|our|his|her|their|this|that)" + _A_TIME_SCOPE, re.I)
_A_MONEY_PLURAL = ("things", "days", "weeks", "months", "years", "minutes", "hours",
                   "pounds", "quid", "euros", "dollars", "pence", "savings", "notes",
                   "coins", "bills", "pennies", "payments", "leftovers")
_A_PLURAL = re.compile(r"\b([a-z]{4,}(?:s|es))\b", re.I)


def _a_count_of_a_thing(text):
    for noun in _A_COUNTED_NOUN.findall(text):
        if noun.lower() not in _A_CURRENCY_PLURAL:
            return True
    if _A_SCOPE_OF_A_THING.search(text):
        return True
    before = text.split("there", 1)[0] if "there" in text else ""
    for word in _A_PLURAL.findall(before):
        word = word.lower()
        if word in _A_MONEY_PLURAL or word.endswith("ss"):
            continue
        return True
    return False


_HELD_SCOPE = re.compile(
    r"^\s*(?:left|till|until|to\s+last|this\s+(?:week|month|payday)|for\s+the\s+(?:week|month)|"
    r"a\s+(?:week|month)\b|the\s+(?:week|month)\b|"
    r"saved|put\s+(?:by|away|aside)|set\s+aside|in\s+(?:the\s+bank|savings|an?\s+account)|"
    r"in\s+the\s+building\s+society)", re.I)

LEFT = re.compile(
    r"\bhow\s+much\s+(?:is\s+|was\s+)?(?:(?:have|has|do|does|did)\s+(?:i|we)\s+)?"
    r"(?:got\s+|have\s+)?(?:left|remaining)\b"
    r"|\bwhat(?:'s| is|s)\s+(?:left|remaining)\b"
    r"|\bwhat\s+(?:have|do)\s+(?:i|we)\s+(?:got\s+)?(?:left|remaining)\b"
    r"|\bhow\s+much\s+(?:of\s+)?(?:it|that|the\s+[a-z]+)\b[^?]{0,20}\b(?:left|remaining)\b"
    r"|\b(?:how\s+much|what)\s+did\s+(?:i|we)\s+(?:tell\s+you|say)\b[^?]{0,30}"
    r"\b(?:left|remaining)\b", re.I)
AFFORD = re.compile(
    r"\bcan\s+(?:i|we)\s+afford\s+(.*)$"
    r"|\bis\s+there\s+enough\s+(?:left\s+)?(?:for|to)\s+(.*)$"
    r"|\b(?:do|have)\s+(?:i|we)\s+(?:have|got)\s+enough\s+(?:left\s+)?(?:for|to)\s+(.*)$"
    r"|\benough\s+left\s+for\s+(.*)$"
    r"|\b(?:is|was|will|would)\s+(?:that|this|it)\s+(?:be\s+)?enough\s+(?:for|to)\s+(.*)$", re.I)


def _figure(value):
    value = float(value or 0)
    if abs(value - round(value)) < 0.005:
        return str(int(round(value)))
    return "%.2f" % value


def _with_scale(number, word):
    word = (word or "").strip().lower()
    if not (word.startswith("k") or word.startswith("thousand") or word.startswith("grand")):
        return number
    try:
        value = float(number) * 1000
    except (TypeError, ValueError):
        return number
    return str(int(round(value))) if abs(value - round(value)) < 0.005 else number


def _held_in(line):
    text = _plain(" ".join(str(line or "").split()))
    if not text or "?" in text:
        return None
    match = BUDGET_HELD.search(text) or ON_A_BUDGET.search(text) or SAVINGS_HELD.search(text)
    if match:
        return _with_scale(match.group(1), match.group(2))
    match = THERE_LEFT.search(text)
    if match and not _a_count_of_a_thing(text):
        return _with_scale(match.group(1), match.group(2))
    match = HELD.search(text)
    if match:
        currency, tail = (match.group(2) or "").strip(), match.group(3) or ""
        if not currency and "£" not in match.group(0) and not _HELD_SCOPE.match(tail):
            return None
        if not currency and "£" not in match.group(0) and _a_count_of_a_thing(text):
            return None
        return _with_scale(match.group(1), match.group(2))
    return None


def the_held(memory, text=None):
    found = None
    for line in the_lines(memory, text):
        amount = _held_in(line)
        if amount is not None:
            found = {"amount": amount, "line": line}
    return found


def _a_thing_to_buy(said):
    match = AFFORD.search(said)
    if not match:
        return ""
    thing = next((group for group in match.groups() if group), "")
    thing = re.split(r"[,.!?;]", " ".join(thing.split()))[0]
    thing = _TAIL_OFF.sub("", _TRAILING.sub("", thing)).strip()
    thing = re.sub(r"^(?:it|that|one|anything)\b", "", thing).strip()
    return thing if 1 < len(thing) < 40 else ""


A_PRICE = re.compile(
    r"£\s*(?P<sigil>\d[\d,]*(?:\.\d{1,2})?)"
    r"|(?P<word>\d[\d,]*(?:\.\d{1,2})?)\s*(?:pounds?|quid|gbp)\b"
    r"|(?:for|under|about|around)\s+(?P<ask>\d[\d,]*(?:\.\d{1,2})?)"
    r"|(?P<bare>\d[\d,]*(?:\.\d{1,2})?)\s+(?P<item>[a-z][a-z'-]*)\b", re.I)


def _the_price(thing):
    match = A_PRICE.search(str(thing or ""))
    if not match:
        return None
    for group in ("sigil", "word", "ask"):
        value = match.group(group)
        if value:
            return float(value.replace(",", ""))
    item = match.group("item") or ""
    if item.endswith("s") and not item.endswith("ss"):
        return None
    value = float((match.group("bare") or "0").replace(",", ""))
    return value if value >= 10 else None


def _bare_thing(thing):
    return re.sub(r"^(?:a|an|the|some|my|our|any)\s+", "", str(thing or "").strip(), flags=re.I)


_ASK_WORDS = frozenset("""a an and any afford affordt can could do does did enough for get got
have has how i is it its left me much my of much's remaining some that the there this to was we
what what's whats will would you your im i'm we're t left-over""".split())


def _only_the_ask(said):
    words = [word.strip(".,!?;:'\"").lower() for word in str(said or "").split()]
    return not [word for word in words if word and word not in _ASK_WORDS]


def _nothing_before(memory, text):
    return len(the_lines(memory, text)) <= 1


A_WHAT_IF = re.compile(
    r"\b(?:what\s+)?if\s+(?:i|we)\s+(?:spend|blow|use\s+up|spend\s+up)\s+"
    r"(?:another\s+|a\s+further\s+|just\s+)?£?\s*(?P<amount>\d[\d,]*(?:\.\d{1,2})?)"
    r"(?P<currency>\s*(?:k\b|p\b|pounds?|quid|gbp))?(?P<tail>.*)$", re.I)
A_LENGTH_NOT_MONEY = re.compile(
    r"^\s*(?:hours?|hrs?|minutes?|mins?|days?|weeks?|months?|years?|nights?|times?)\b", re.I)


def _the_what_if(match, memory):
    currency = (match.group("currency") or "").strip().lower()
    if currency in ("k", "p"):
        return None
    if A_LENGTH_NOT_MONEY.match(match.group("tail") or ""):
        return None
    amount = float((match.group("amount") or "0").replace(",", ""))
    held = the_held(memory)
    if held is None or amount <= 0:
        return None
    try:
        had = float(held["amount"])
    except (TypeError, ValueError):
        return None
    spends = the_spends(memory, None)
    left = had - (sum(float(spend.get("amount") or 0) for spend in spends) if spends else 0.0)
    if amount > left:
        return ("Spend " + _figure(amount) + " more and you are " + _figure(amount - left) +
                " over - " + _figure(left) + " is what is left now.")
    if not spends:
        return ("Spend " + _figure(amount) + " of the " + _figure(had) + " you told me you "
                "have and " + _figure(left - amount) + " is left.")
    return ("Spend " + _figure(amount) + " more and " + _figure(left - amount) + " is left.")


def what_is_left(text, memory):
    said = " ".join(str(text or "").split())
    if not said:
        return None
    what_if = A_WHAT_IF.search(said)
    if what_if:
        return _the_what_if(what_if, memory)
    if not (LEFT.search(said) or AFFORD.search(said)):
        return None
    if readings(said):
        return None
    held = the_held(memory)
    if held is None:
        if _nothing_before(memory, said) and _only_the_ask(said):
            if AFFORD.search(said) and not LEFT.search(said):
                return ("Afford what, and with what? Tell me the thing and what you've got to "
                        "spend, and I'll do the sum.")
            return ("Left of what? Tell me what you've got and what has gone out of it, and I'll "
                    "do the sum.")
        return None
    try:
        had = float(held["amount"])
    except (TypeError, ValueError):
        return None
    spends = the_spends(memory, None)
    if spends:
        out = sum(float(spend.get("amount") or 0) for spend in spends)
    else:
        out = 0.0
    left = had - out
    if AFFORD.search(said) and not LEFT.search(said):
        thing = _a_thing_to_buy(said)
        price = _the_price(thing)
        name = _bare_thing(thing)
        named = (thing if re.match(r"(?:a|an|the|some|my|our|any)\s", thing, re.I)
                 else ("the " + name if name else ""))
        cost = ("Tell me the price of " + named if named else "Tell me the price") + \
            " and I'll say whether it fits."
        if spends and left <= 0:
            return ("You had " + _figure(had) + " and " + _listed(spends) + " has gone, so you "
                    "are " + _figure(-left) + " over. " +
                    (thing.capitalize() + " needs more coming in first." if thing
                     else "Tell me if more comes in and I'll work it out again."))
        if price is not None:
            if spends:
                if price > left:
                    return ("No - " + thing + " is more than the " + _figure(left) +
                            " you have left. It wants " + _figure(price - left) + " more.")
                return ("Yes - " + thing + " comes out of the " + _figure(left) + " you have "
                        "left, with " + _figure(left - price) + " spare.")
            if price > had:
                return ("No - " + thing + " is more than the " + _figure(had) + " you told me "
                        "you have. It wants " + _figure(price - had) + " more.")
            return ("Yes - " + thing + " comes out of the " + _figure(had) + " you told me you "
                    "have, with " + _figure(had - price) + " spare.")
        if not spends:
            return ("You told me you have " + _figure(had) + " and nothing has gone out of it "
                    "yet, so anything up to " + _figure(had) + " is covered. " + cost)
        return ("You had " + _figure(had) + " and " + _listed(spends) + " has gone, so " +
                _figure(left) + " is left. " + cost)
    if not spends:
        return ("You told me you have " + _figure(had) + ", and you've not said that any of it "
                "has gone yet.")
    if left <= 0:
        return ("You had " + _figure(had) + " and " + _listed(spends) + " has gone, so you are " +
                _figure(-left) + " over.")
    return ("You had " + _figure(had) + " and " + _listed(spends) + " has gone, so " +
            _figure(left) + " is left.")
