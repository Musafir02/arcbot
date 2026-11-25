import re

TAIL = frozenset("""
tho though lol lmao haha hehe tbh ngl imo idk innit tbf anyhow anyway really actually
right now today tonight tomorrow weekend week weekday evening morning afternoon night
either at all any more anymore yet still too also as well
and or but with so much very loads lots lot quite pretty
a an the of to for from in on at by about than then
monday tuesday wednesday thursday friday saturday sunday christmas birthday
""".split())

THING_STOP = frozenset("""
i we me us he she they you it them that this these those there
what how why when where which who whose whatever
is are was were am be been being will would should can could shall may might
do does did dont doesn't doesn't isn't aren't have has had got
so if because since though although while until
like loves loved love adore adores prefer prefers hate hates hated dislike dislikes
loathe loathes detest detests enjoy enjoys
""".split())

THING = (r"([A-Za-z][A-Za-z'\u2019-]*(?:\s+(?:[A-Za-z][A-Za-z'\u2019-]*"
         r"|and|or|of|to|the|a|my|our|your|their|his|her)){0,4})")

UNSURE = re.compile(
    r"\b(?:not sure|not certain|unsure|don'?t know|do not know|dunno|no idea)\s+"
    r"(?:if|whether|that)\s+(?:i|we)(?:'d|\s+would)?\s+(?:actually\s+|really\s+|even\s+)?"
    r"(?:like|love|enjoy|be into|get on with)\s+" + THING, re.I)
NO = re.compile(
    r"\b(?:i|we)\s+(?:really\s+|just\s+|actually\s+)?(?:don'?t|do not|dont|never)\s+"
    r"(?:think\s+(?:i|we)\s+|really\s+)?(?:like|love|eat|drink|want)\s+" + THING, re.I)
NOT_KEEN = re.compile(
    r"(?:\b(?:i'?m|i am|we'?re|we are)|^)\s*not\s+"
    r"(?:(?:that|really|very|so|all that|quite)\s+)?(?:much\s+of\s+)?(?:a\s+|the\s+)?"
    r"(?:(?:big|huge|massive|great)\s+)?"
    r"(?:keen on|fan of|into|mad about|fussed on|bothered about)\s+" + THING, re.I)
HATE = re.compile(
    r"\b(?:i|we)\s+(?:really\s+|just\s+|actually\s+|absolutely\s+|properly\s+)?"
    r"(?:hate|hates|dislike|dislikes|loathe|loathes|detest|detests|"
    r"can'?t stand|cannot stand|really can'?t stand)\s+" + THING, re.I)
MY_THING = re.compile(
    r"\b" + THING + r"\s+(?:isn'?t|is not|aren'?t|are not)\s+"
    r"(?:(?:really|that|exactly|quite)\s+)?(?:my|our)\s+"
    r"(?:(?:kind|sort)\s+of\s+|cup\s+of\s+tea|thing)", re.I)
YES = re.compile(
    r"\b(?:i|we)\s+(?:do\s+|really\s+|absolutely\s+|just\s+|actually\s+)?"
    r"(?:like|love|adore|prefer)\s+" + THING, re.I)

NOT_A_THING = frozenset("""
it that this these those them him her you me us one ones a an the to when if how why what
which who there here so such being doing having
myself yourself himself herself itself ourselves yourselves themselves oneself
way
""".split())

DISLIKE_IN = re.compile(
    r"\b(?:(?:really|just|actually|absolutely|properly|simply)\s+)*"
    r"(?:hate|hates|hated|dislike|dislikes|disliked|loathe|loathes|loathed|detest|detests|"
    r"detested|can'?t stand|cannot stand)\b.*$", re.I)
LIKING_BEFORE = re.compile(
    r"\b(?:like|likes|liked|love|loves|loved|adore|adores|adored|hate|hates|hated|prefer|"
    r"prefers|preferred|keen on|a fan of|fan of|fond of|into|can'?t stand|cant stand|"
    r"crazy about|big on|dislike|dislikes|disliked|loathe|loathes|loathed|detest|detests|"
    r"detested|not\s+(?:\w+\s+)?(?:a fan of|keen on|into|fond of|big on))\s+(?:\w+\s+){0,2}$",
    re.I)
OWNED_BEFORE = re.compile(r"\b(?:my|our|his|her|their|the|this|that)\s+$", re.I)


def _kept(thing):
    words = str(thing or "").split()
    kept = []
    for index, raw in enumerate(words):
        word = raw.strip(".,;:!?")
        if not word:
            continue
        if kept and (word.lower() in THING_STOP
                     or word.lower() in ("my", "our", "his", "her", "their", "your")):
            break
        if not kept and word.lower() in TAIL:
            continue
        kept.append((index, word))
    while kept and kept[-1][1].lower() in TAIL:
        kept.pop()
    if not kept or kept[0][1].lower() in NOT_A_THING:
        return []
    return kept


def _clean(thing):
    kept = _kept(thing)
    if not kept:
        return None
    words = [word for _, word in kept]
    if words[0].lower() in ("my", "our"):
        words[0] = "your"
    return " ".join(words)


def _thing_end(text, match):
    took = text[match.start(1):match.end(1)]
    kept = _kept(took)
    if not kept:
        return match.start(1)
    last = took.split()[kept[-1][0]]
    return match.start(1) + took.rfind(last) + len(last)


_QUANTITY = re.compile(r"^(?:enough|too much|too little|much|any|more|less|loads of|lots of|"
                       r"plenty of|a lot of|as much)\b", re.I)
_SHORTFALL_TAIL = re.compile(r"\b(?:at\s+all|any\s?more)\s*$", re.I)
_SHORTFALL_VERB = re.compile(r"\b(?:eat|drink)\s+$", re.I)


def _read_clause(text):
    text = " ".join(str(text or "").split())
    if not text or text.endswith("?"):
        return None, None
    for pattern, how in ((UNSURE, "unsure"), (NO, "no"), (NOT_KEEN, "no"), (MY_THING, "no"),
                         (YES, "yes")):
        match = pattern.search(text)
        if match:
            raw = match.group(1)
            if re.match(r"\s*to\b", raw):
                return None, None
            thing = _clean(raw)
            shortfall = _SHORTFALL_VERB.search(text[:match.start(1)])
            if thing and not _QUANTITY.match(thing) and not _QUANTITY.match(raw.strip()) \
                    and not (shortfall and _SHORTFALL_TAIL.search(raw)):
                return {"thing": thing, "how": how}, _thing_end(text, match)
    match = HATE.search(text)
    if match:
        raw = match.group(1)
        thing = _clean(raw)
        if thing and not re.match(r"\s*(?:my|our)\b", raw, re.I):
            return {"thing": thing, "how": "no"}, _thing_end(text, match)
    return None, None


def read(line):
    return _read_clause(line)[0]


_TASTE_VERB = (r"(?:(?:i|we|he|she|they)\s+)?(?:do\s+|really\s+|absolutely\s+|just\s+|"
               r"actually\s+|properly\s+)?"
               r"(?:like|love|adore|prefer|hate|hates|dislike|dislikes|loathe|detest|enjoy|"
               r"eat|drink|want|can'?t stand|cannot stand)\b")
_CLAUSE_SPLIT = re.compile(r"\s*;\s*|\s+(?:but|and|though|whereas)\s+(?=" + _TASTE_VERB + r")",
                           re.I)


_ASK_FORM = re.compile(r"\b(?:how (?:do|can|should|could) i|how to|what should i|"
                       r"what can i|what could i|any (?:tips|advice|ideas|suggestions)?"
                       r"|where (?:do|should) i start|is there a way)\b", re.I)
_ASKS_FOR_A_THING = re.compile(
    r"\b(?:recommend|recommendations?|suggest|suggestions?)\b"
    r"|\b(?:any|got any|have you got any)\s+good\b"
    r"|\bgive me (?:a|an|some|a few|your)\b"
    r"|\bwhat should i (?:watch|read|listen to|see|get|buy|cook|make for|eat|play|do with)\b"
    r"|\bhelp me (?:pick|choose|find|decide)\b"
    r"|\bi(?:'m| am) looking for\b"
    r"|\bi need (?:a|an|some|a few|new|ideas?|advice|help)\b"
    r"|\bi(?:'d| would)? want (?:a|an|some) (?:new |good |different )?"
    r"(?:film|movie|series|show|boxset|book|novel|podcast|audiobook|album|playlist|song)\b"
    r"|\bwhere can i (?:get|buy|find)\b", re.I)


_HATED_CHORE = re.compile(r"\b(?:hate|hates|dislike|dislikes|loathe|detest|can'?t stand|"
                          r"cannot stand|don'?t like|do not like)\s+(?:to\s+)?"
                          r"(?:cook|cooking|bake|baking|prep|prepping|meal prep|exercise|"
                          r"exercising|the gym|working out|run|running|clean|cleaning|iron|"
                          r"ironing|tidy|tidying|shop|shopping|wash|washing|diet|dieting)\b", re.I)


def read_all(line):
    text = " ".join(str(line or "").split())
    found = []
    for clause in _CLAUSE_SPLIT.split(text):
        clause = clause.strip()
        if not clause:
            continue
        if re.match(_TASTE_VERB, clause, re.I) and not re.match(r"(?:i|we|he|she|they)\b",
                                                               clause, re.I):
            clause = "i " + clause
        taste = read(clause)
        if taste and taste not in found:
            found.append(taste)
    return found


def only_a_taste(text):
    text = " ".join(str(text or "").split())
    if not text or "?" in text:
        return False
    if _ASK_FORM.search(text) and _HATED_CHORE.search(text):
        return False
    if _ASKS_FOR_A_THING.search(text):
        return False
    seen = False
    for clause in _CLAUSE_SPLIT.split(text):
        clause = clause.strip()
        if not clause:
            continue
        said = clause
        bare = re.match(_TASTE_VERB, said, re.I) and not re.match(r"(?:i|we|he|she|they)\b",
                                                                 said, re.I)
        if bare:
            said = "i " + said
        taste, end = _read_clause(said)
        if not taste:
            return False
        left = said[end:] if not bare else said[end:]
        if set(re.findall(r"[a-z']+", left.lower())) - TAIL:
            return False
        seen = True
    return seen


def said_about(text, position):
    before = text[max(0, position - 30):position]
    if not LIKING_BEFORE.search(before):
        return False
    return not OWNED_BEFORE.search(text[max(0, position - 12):position])


_ASK_START = r"^\W*(?:(?:so|and|but|ok|okay|hmm|oh|well|wait)\b[,.]?\s+)*"
_ASK_ADVERB = r"(?:(?:still|really|actually|even|now|just|ever)\s+)*"
ASKS_ABOUT_A_TASTE = re.compile(
    _ASK_START + r"(?:(?:do|did|does)\s+(?:i|we)\s+" + _ASK_ADVERB +
    r"(?:like|love|enjoy|eat|drink|want)\b"
    r"|am\s+i\s+" + _ASK_ADVERB + r"(?:a fan of|into|keen on|mad about|fussed on)\b"
    r"|did\s+i\s+say\s+i\s+(?:like|liked|love|loved|hate|hated)\b)", re.I)
TASTE_ASKED_ABOUT = re.compile(
    _ASK_START + r"(?:(?:do|did|does)\s+(?:i|we)\s+" + _ASK_ADVERB +
    r"(?:like|love|enjoy|eat|drink|want)\s+"
    r"|am\s+i\s+" + _ASK_ADVERB + r"(?:a fan of|into|keen on|mad about|fussed on)\s+"
    r"|did\s+i\s+say\s+i\s+(?:like|liked|love|loved|hate|hated)\s+)", re.I)


def asks_about_a_taste(line):
    return bool(ASKS_ABOUT_A_TASTE.search(str(line or "")))


ASKS_FOR_TASTES = re.compile(
    _ASK_START + r"(?:(?:what|which)\b[^?.!]*?\bdo\s+(?:i|we)\s+" + _ASK_ADVERB +
    r"(?:like|love|enjoy|eat|drink)\b"
    r"|(?:what|which)\s+(?:are|were)\s+my\s+(?:favou?rite|best)\s+\w+"
    r"|do\s+you\s+(?:know|remember)\s+what\s+(?:i|we)\s+(?:like|love)\b"
    r"|what\s+do\s+you\s+know\s+(?:that\s+)?i\s+(?:like|love)\b)", re.I)


_OTHER_OWNER = re.compile(
    r"^(?:(?:my|our)\s+(?P<who>[a-z][a-z'\u2019-]{1,20})"
    r"|(?P<pronoun>she|he|they))"
    r"(?:'?s|'?re)?"
    r"\s+(?P<rest>.*)$", re.I)
_OTHER_SAYS = (
    (r"(?:isn'?t|is\s+not|wasn'?t|was\s+not)\s+(?:that\s+|really\s+|very\s+|all\s+that\s+)?"
     r"(?:into|keen\s+on|a\s+fan\s+of|mad\s+about|fussed\s+on|big\s+on)", "don't like"),
    (r"(?:doesn'?t|does\s+not|doesnt|won'?t|will\s+not|never|can'?t|cannot|can\s+not)\s+"
     r"(?:really\s+|actually\s+|ever\s+)?(?:like|love|eat|drink|stand|touch|want|have|"
     r"be\s+keen\s+on)", "don't like"),
    (r"(?:hates?|loathes?|detests?|dislikes?|can'?t\s+stand|cannot\s+stand)", "hate"),
    (r"is\s+(?:really\s+|absolutely\s+|just\s+|very\s+)?"
     r"(?:into|keen\s+on|mad\s+about|a\s+fan\s+of|big\s+on|fussed\s+on|fond\s+of)", "like"),
    (r"(?:loves?|likes?|adores?|prefers?|enjoys?)", "love"),
)
_OTHER_VERB = "|".join("(?:%s)" % pattern for pattern, _ in _OTHER_SAYS)

_OTHER_CLAUSE = re.compile(
    r"\s*;\s*|\s*,\s*|\s+(?:but|and|so|though|whereas|while)\s+"
    r"(?=(?:[a-z][a-z'\u2019-]{1,20}\s+)?(?:" + _OTHER_VERB + r")\b)", re.I)
_A_CLAUSE_AFTER = re.compile(
    r"^\s*[,;:]?\s*(?:so|but|and|because|cos|cause|though|although|whereas|yet|if|then|"
    r"when|while|as)\b", re.I)
_ASKS_SOMETHING = re.compile(
    r"\b(?:what|how|why|when|where|which|who|whose|whats|what's|should|shall|could|would|"
    r"any ideas|any tips|recommend)\b", re.I)
_OTHER_TASTE = re.compile(
    r"^(?:really |absolutely |just |actually |properly |simply |still )?(?:" + _OTHER_VERB
    + r")\b", re.I)


def read_other(line):
    text = " ".join(str(line or "").split())
    if not text or text.endswith("?"):
        return []
    found = []
    person = None
    for clause in _OTHER_CLAUSE.split(text):
        clause = clause.strip()
        if not clause:
            continue
        match = _OTHER_OWNER.match(clause)
        if match:
            person = ({"who": match.group("who").lower()} if match.group("who")
                      else {"pronoun": match.group("pronoun").lower()})
            clause = match.group("rest")
        if person is None:
            continue
        said = _OTHER_TASTE.match(clause)
        if not said:
            continue
        tasted = _their_taste_in(clause, said)
        if tasted:
            found.append({**tasted, **person})
    return found


def _their_taste_in(rest, said):
    verb = said.group(0).strip()
    thing = rest[said.end():].strip()
    as_own = "love"
    for pattern, rewritten in _OTHER_SAYS:
        if re.fullmatch(pattern, verb, re.I):
            as_own = rewritten
            break
    if not thing:
        return None
    clause = "i " + as_own + " " + thing
    taste, end = _read_clause(clause)
    if not taste:
        return None
    left = clause[end:]
    words = set(re.findall(r"[a-z']+", left.lower()))
    if words - TAIL:
        if not _A_CLAUSE_AFTER.match(left) or _ASKS_SOMETHING.search(left):
            return None
    tasted = {"thing": taste["thing"], "how": taste["how"]}
    if re.search(r"\b(?:eat|eats|ate|drink|drinks|drank)\b", verb, re.I):
        tasted["eaten"] = True
    return tasted
