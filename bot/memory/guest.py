import re

WORD = re.compile(r"[a-z0-9']+")
STOP = re.compile(r"\b(?:but|so|because|though|although|which|when|if|and then)\b|[,.;!?]")
DISLIKE = re.compile(
    r"\b(?:hates?|dislikes?|can'?t stand|cannot stand|"
    r"(?:do|does|did)(?:n'?t| not) (?:like|fancy|enjoy|want|wants?)|"
    r"(?:isn'?t|aren'?t|is not|are not|amn'?t) (?:(?:that|really|very|so) )?(?:much of )?"
    r"(?:a |the )?(?:(?:big|huge|massive|great) )?"
    r"(?:fan of|keen on|fond of|fussed on|my thing|my kind of thing)|"
    r"not (?:(?:that|really|very|so|all that) )?(?:much of )?(?:a |the )?"
    r"(?:(?:big|huge|massive|great) )?"
    r"(?:fan of|keen on|fond of|fussed on|my thing|my kind of thing)|avoids?|avoiding)\s+"
    r"(?:the\s+|any\s+)?(?P<food>[a-z][a-z' -]{1,40})", re.I)
NOT_MY_THING = re.compile(
    r"\b(?P<food>[a-z][a-z' -]{1,30}?)\s+(?:isn'?t|is not|aren'?t|are not)\s+"
    r"(?:(?:really|that|exactly|quite)\s+)?(?:my|our)\s+"
    r"(?:(?:kind|sort)\s+of\s+|cup\s+of\s+tea|thing)", re.I)
NO_FOR_ME = re.compile(
    r"\b(?:no|not|none of the)\s+(?:any\s+|more\s+|the\s+)?(?P<food>[a-z][a-z' -]{1,40}?)"
    r"\s+(?:for me|thanks|thank you|please|today|tonight|tomorrow|later)\b", re.I)
NO_FOOD_ALONE = re.compile(
    r"^\s*(?:no|not|none(?=[\s,])|nothing with|anything but)\s+"
    r"(?P<food>[a-z][a-z' ,-]{3,60}?\s+(?:or|and|,)\s+[a-z][a-z' ,-]{1,40})\s*$", re.I)
GENERIC = frozenset("""
cooking cook food dinner tea lunch breakfast eating eat meal meals work job school housework
cleaning shopping mornings mondays tuesdays wednesdays thursdays fridays saturdays sundays
winter summer rain traffic flying travel travelling exercise sport gym crowds spiders
everything anything nothing it that this them him her
""".split())
PRONOUN = frozenset("her his their my your our its it them him this that these those".split())
EXTRA = frozenset("""
olive feta couscous halloumi paneer quinoa avocado broccoli cauliflower cabbage leek celery
cucumber lettuce peas sweetcorn beetroot aubergine courgette pumpkin berries banana apple
orange lemon lime grape melon peach pear plum mango pineapple strawberry blueberry raspberry
walnut almond cashew peanut hazelnut pistachio sesame tofu prawn salmon tuna cod haddock
mackerel sardine anchovy sausage bacon ham chorizo steak mince turkey duck lamb pork beef
chicken fish egg eggs cheese butter milk cream yoghurt bread pasta rice potato tomato onion
garlic carrot pepper spinach mushroom lentil chickpea bean noodle soup curry lasagne pizza
cake chocolate sugar salt
""".split())

_KNOWN = None


def _fold(word):
    word = str(word).lower().strip(".,!?;:'\"")
    if len(word) > 4 and word.endswith("ies"):
        return word[:-3] + "y"
    if len(word) > 4 and word.endswith("oes"):
        return word[:-2]
    if len(word) > 3 and word.endswith("es") and word[-3] in "sxzh":
        return word[:-2]
    if len(word) > 3 and word.endswith("s") and not word.endswith("ss"):
        return word[:-1]
    return word


def _known():
    global _KNOWN
    if _KNOWN is not None:
        return _KNOWN
    words = set(EXTRA)
    try:
        from ..understanding.topics import STRONG
        for topic in ("cooking", "food-and-drink"):
            words.update(STRONG.get(topic, "").split())
    except Exception:
        pass
    try:
        from ..knowledge import cooking as knowledge
        for name, (aliases, _reply) in knowledge.PANTRY.items():
            words.add(name)
            words.update(aliases)
    except Exception:
        pass
    _KNOWN = {_fold(word) for word in words if word}
    return _KNOWN


_WHEN = re.compile(
    r"(?:\s+(?:(?:this|next|last|on)\s+"
    r"(?:week|weekend|friday|saturday|sunday|monday|tuesday|wednesday|thursday|morning|evening|"
    r"afternoon|night|weekday|birthday|christmas)"
    r"|today|tonight|tomorrow|tomorrow night|now|later|again|then|instead|"
    r"for (?:tea|dinner|lunch|breakfast|supper)|at (?:lunch|dinner|breakfast|tea)|"
    r"any\s?more))+$", re.I)


def _clean(item):
    item = " ".join(str(item or "").strip(" .,!?;:'\"").lower().split())
    item = re.sub(r"^(?:the|any|some|more|all|a|an)\s+", "", item).strip()
    item = re.sub(r"\s+(?:too|either|as well|much|really|actually|at all|though|tho|anyway)$",
                    "", item).strip()
    item = _WHEN.sub("", item).strip(" ,")
    return item


DRINK_PAIR = frozenset("""
tea coffee beer wine lager cider ale stout juice squash cordial water milk lemonade
""".split())


def _one_half(piece):
    if _is_food(piece):
        return True
    words = WORD.findall(piece)
    return bool(words) and all(_fold(word) in DRINK_PAIR for word in words)


def _is_food(item):
    if not item or item in GENERIC:
        return False
    words = WORD.findall(item)
    if not words or words[0] in PRONOUN:
        return False
    known = _known()
    return any(_fold(word) in known for word in words)


def plain(item, a_pair=False):
    item = _clean(item)
    item = re.sub(r"^(?:the\s+)?(?:taste|texture|smell|look|sight)\s+of\s+(?:the\s+)?", "",
                  item, flags=re.I).strip()
    if not (_is_food(item) or (a_pair and _one_half(item))) \
            or re.search(r"\b(?:on|with|of|in|at)\b", item, re.I):
        return None
    known = _known()
    if not all(_fold(word) in known for word in WORD.findall(item)):
        return None
    return item


def found(text):
    if not isinstance(text, str):
        return []
    out = []
    for pattern in (DISLIKE, NOT_MY_THING, NO_FOR_ME, NO_FOOD_ALONE):
        for match in pattern.finditer(text):
            chunk = STOP.split(match.group("food"))[0]
            pieces = [_clean(re.sub(r"^(?:no|not)\s+", "", piece.strip(), flags=re.I))
                      for piece in re.split(r",|\band\b|\bor\b", chunk)]
            pieces = [piece for piece in pieces if piece]
            a_pair = len(pieces) >= 2 and all(_one_half(piece) for piece in pieces)
            if pattern is NO_FOOD_ALONE and not a_pair:
                continue
            for item in pieces:
                if (_is_food(item) or a_pair) and item not in [food for food, _at in out]:
                    out.append((item, match.start("food")))
    return out


NO_X_ALONE = re.compile(
    r"^\s*(?:no|not|none of the|nothing with)\s+(?:any\s+|more\s+|the\s+)?"
    r"(?P<food>[a-z][a-z' -]{1,40}?)\s*(?:please|thanks|thank you)?\s*$", re.I)


def turned_down_alone(text):
    match = NO_X_ALONE.match(" ".join(str(text or "").split()))
    if not match:
        return []
    item = _clean(match.group("food"))
    if not item or re.search(r"\b(?:or|and)\b", item):
        return []
    return [item] if _is_food(item) else []


def _contains(text, food):
    root = _fold(food)
    return any(_fold(word) == root for word in WORD.findall(str(text or "")))


def _without_article(item):
    return re.sub(r"^(?:a|an|the)\s+", "", item.strip(), flags=re.I)


def _split_list(rest):
    parts = re.split(r",\s*|\s+or\s+", rest)
    items = [re.sub(r"^(?:or|and)\s+", "", part.strip(" .")) for part in parts
             if part.strip(" .")]
    if any(len(WORD.findall(item)) > 5 for item in items):
        return None
    return items


def _kept_phrase(items):
    if len(items) == 1:
        return items[0] + " still works"
    if len(items) == 2:
        return items[0] + " or " + items[1] + " both still work"
    return ", ".join(items[:-1]) + " or " + items[-1] + " all still work"


def revise(reply, foods):
    if not isinstance(reply, str) or not foods:
        return None
    for sentence in re.split(r"(?<=[.!?])\s+", reply.strip()):
        hit = [food for food in foods if _contains(sentence, food)]
        if not hit:
            continue
        head, sep, rest = sentence.partition(": ")
        if not sep:
            continue
        items = _split_list(rest)
        if not items:
            continue
        removed = [item for item in items if any(_contains(item, food) for food in hit)]
        kept = [item for item in items if item not in removed]
        if not removed or not kept:
            continue
        gone = "the " + " and the ".join(_without_article(item) for item in removed)
        gone += " is out" if len(removed) == 1 else " are out"
        return "Then " + gone + " — " + _kept_phrase(kept) + "."
    return None


def left_out(foods):
    items = list(dict.fromkeys(str(food).strip() for food in foods if str(food).strip()))
    said = " or ".join(items) if len(items) == 2 else ", ".join(items)
    if not said:
        return None
    return "Fair enough — no " + said + " in anything I suggest."
