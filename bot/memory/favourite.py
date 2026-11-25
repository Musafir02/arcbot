import re

LEAD = re.compile(r"^\s*(?:(?:so|and|but|oh|ah|well|also|btw|right|ok|okay|hmm)[\s,.!;-]+)+", re.I)

SAYS = re.compile(
    r"^\s*(?:my|our)\s+(?:favou?rite|fav|best)\s+"
    r"(?P<thing>[a-z][a-z'\u2019-]*(?:\s+[a-z][a-z'\u2019-]*){0,2}?)"
    r"\s*(?:is|are|'s|was|will be|has to be|would be)\s+"
    r"(?P<value>[^?.!;]{1,60}?)\s*$", re.I)

SOMEONE_ELSE = re.compile(
    r"^\s*(?:my|our)\s+[a-z][a-z'\u2019-]*'?s?\s+(?:favou?rite|fav|best)\b"
    r"|\b(?:his|her|their|your)\s+(?:favou?rite|fav|best)\b", re.I)

BEST_PERSON = re.compile(
    r"\bbest\s+(?:friends?|mates?|man|buddy|bud|buddies|bestie|besties|pals?|friend's|mate's|"
    r"friendship)\b", re.I)

IS_MINE = re.compile(
    r"^\s*(?P<value>[a-z][a-z'\u2019 -]{1,40}?)\s+(?:is|are|has always been|'s)\s+"
    r"my\s+(?:favou?rite|fav|best)\s+"
    r"(?P<thing>[a-z][a-z'\u2019-]*(?:\s+[a-z][a-z'\u2019-]*){0,2})\s*$", re.I)

ASKS = re.compile(
    r"(?:\bwhat(?:'s|s| is| was| are| were)?|\bwho(?:'s|s| is| was| are| were)?|"
    r"\bwhich(?:\s+is|\s+one)?|\bdo you (?:know|remember)|"
    r"\bdid i (?:say|tell you)|\bcan you (?:remember|tell me))\b"
    r"[^?.!]{0,40}?\bmy\s+(?:favou?rite|fav|best)\s+"
    r"(?P<thing>[a-z][a-z'\u2019-]*(?:\s+(?!is\b|was\b|are\b|were\b)"
    r"[a-z][a-z'\u2019-]*){0,2})?"
    r"(?:\s+(?:is|was|again|then|though))?\s*[?.!]*\s*$", re.I)

WHICH_IS = re.compile(
    r"^\s*which\s+(?P<thing>[a-z][a-z'\u2019-]*(?:\s+[a-z][a-z'\u2019-]*){0,2})"
    r"\s+(?:is|was)\s+my\s+(?:favou?rite|fav|best)\b", re.I)

CORRECTS = re.compile(
    r"^\s*(?:no|nope|actually|sorry|wait|no wait|i mean|rather|scratch that|make that|"
    r"not that|that's wrong|thats wrong)\b[\s,.!-]+"
    r"(?:its|it's|it is|i mean|make it|i meant|just)\s+"
    r"(?P<value>[^?.!;]{1,60}?)\s*$", re.I)

PREFERS_NOW = re.compile(
    r"^\s*(?:i|we)\s+(?:prefer|like)\s+(?P<value>[^?.!,;]{1,40}?)\s*"
    r"(?:now|nowadays|these days|better now|more now|better these days|more these days|better|more)"
    r"\s*$", re.I)

ASKS_ALL = re.compile(
    r"\b(?:what|which)\b[^?.!]{0,30}?\bmy\s+(?:favou?rite|fav)s\b|"
    r"\bwhat\s+(?:have\s+i|did\s+i)\s+(?:told|said\s+to)\s+you\b[^?.!]{0,20}\b(?:like|love|prefer)\b|"
    r"\bwhat\s+do\s+you\s+know\s+about\s+my\s+(?:favou?rite|fav)s\b", re.I)

AN_ANSWER = re.compile(r"^\s*[a-z0-9][a-z0-9'\u2019 ,-]{0,40}\s*[.!]?\s*$", re.I)

TAIL = re.compile(r"[\s,]+(?:obviously|tbh|tho|though|really|lol|haha|i think|probably|"
                  r"at the moment|right now|for sure|of course)\s*$", re.I)

ACKNOWLEDGES = frozenset("""
thanks thank thankyou cheers ta ok okay k cool nice great lovely brilliant right alright fine
sure yes yeah yep no nope nah none nothing okthanks nothanks
""".split())

NO_VALUE_PHRASES = ("not sure", "no idea", "dont know", "don't know", "dunno", "hard to say",
                    "cant decide", "can't decide", "not really", "nothing really", "nothing much",
                    "i dont know", "i don't know", "a few", "loads")

A_STATE = frozenset("""
closed shut off over broken rubbish injured cancelled canceled finished sold bought delayed
dirty clean empty full busy open missing ill sick late early free full gone
""".split())
AN_EVENT = re.compile(
    r"(?:\b(?:right\s+now|for\s+now|now|today|tomorrow|tonight|again)\b"
    r"|\ball\s+the\s+time\b|\bat\s+the\s+(?:moment|minute)\b|\bthese\s+days\b"
    r"|\b(?:next|last|this)\s+[a-z]+)\s*$", re.I)

NO_VALUE = frozenset("""
nothing none no idea not sure unsure duno dunno dontknow whatever anything something everything
same hard difficult tricky easy impossible complicated tricky unclear
which what whats who whose when where why how
""".split())

A_CLAUSE = re.compile(r"^(?:to|when|if|that|because|so|how|why|what|whether)\b", re.I)

NOT_A_THING = frozenset("""
to be do have go going going get got make making take taking give giving see seeing say saying
think thinking know knowing want wanting need needing like liking love loving hate hating
""".split())


def _plain(value):
    text = " ".join(str(value or "").split())
    text = text.strip(" \t,.;:!-\u2014")
    text = TAIL.sub("", text)
    return text.strip(" \t,.;:!-\u2014")


def _a_value(value):
    text = _plain(value)
    if not text or len(text.split()) > 6:
        return ""
    low = text.lower().replace("'", "").replace("\u2019", "")
    if low in NO_VALUE or all(word in NO_VALUE for word in low.split()):
        return ""
    if any(low == phrase or low.startswith(phrase + " ") for phrase in NO_VALUE_PHRASES):
        return ""
    if A_CLAUSE.match(low):
        return ""
    if low in A_STATE and len(low.split()) == 1:
        return ""
    if AN_EVENT.search(low):
        return ""
    if not re.search(r"[a-z0-9]", low):
        return ""
    return text


ASK_TAIL = frozenset("""
again is was are were then though tho now please pls exactly already anyway
""".split())


def _a_thing(thing):
    text = " ".join(str(thing or "").split()).strip(" \t,.;:!-").lower()
    if not text or len(text.split()) > 3:
        return ""
    words = [word for word in text.split() if word not in ASK_TAIL]
    if not words:
        return ""
    text = " ".join(words)
    if words[0] in ASK_TAIL or words[0] in ("thing", "things", "one") \
            or words[0] in ("which", "what", "who"):
        return ""
    return text


ASKS_SOMETHING = re.compile(
    r"^(?:what|which|who|when|where|why|how|should|shall|can|could|would|will|do|does|did|"
    r"is|are|any|anything|someone|suggest|give|tell|help|recommend)\b", re.I)
STUCK = re.compile(
    r"\b(?:can'?t|cannot|can not|don'?t know|do not know|not sure|no idea|stuck|"
    r"cant|dont)\b[^,;.!?]{0,30}?"
    r"\b(?:decide|choose|pick|watch|cook|eat|drink|read|wear|do|get|make|start)\b", re.I)

SENTENCE_TOO = re.compile(r"\s*[,;]\s*|\s+[\u2014-]\s*|[.!?]+\s+")


A_QUESTION_AFTER = re.compile(
    r"[.!?]+\s+(?=(?:what|which|who|when|where|why|how|should|shall|can|could|would|will|"
    r"any|anything|do|does|did|is|are)\b)", re.I)


def _clauses(text):
    said = " ".join(str(text or "").split())
    out = [part.strip() for part in re.split(r"\s*[,;]\s*|\s+[\u2014-]\s+", said)]
    out = [part for part in out if part]
    if len(out) > 1:
        return out + [said]
    return [said]


def read(line):
    text = " ".join(str(line or "").split())
    if not text or "?" in text:
        return None
    if asked(text):
        return None
    if SOMEONE_ELSE.search(text):
        return None
    if BEST_PERSON.search(text):
        return None
    plain = LEAD.sub("", text)
    parts = _clauses(plain)
    before_the_question = A_QUESTION_AFTER.split(plain)[0].strip()
    if before_the_question and before_the_question != plain:
        parts = [before_the_question] + parts
    for said in parts:
        found = SAYS.match(said) or IS_MINE.match(said)
        if not found:
            continue
        thing = _a_thing(found.group("thing"))
        value = _a_value(found.group("value"))
        if thing and value:
            return {"thing": thing, "value": value}
    return None


def asks_something_too(line):
    text = " ".join(str(line or "").split())
    if not text:
        return False
    parts = [part.strip() for part in SENTENCE_TOO.split(LEAD.sub("", text)) if part.strip()]
    if len(parts) < 2:
        return False
    for part in parts:
        plain = LEAD.sub("", part).strip()
        if not plain:
            continue
        if SAYS.match(plain) or IS_MINE.match(plain):
            continue
        if "?" in plain or ASKS_SOMETHING.match(plain) or STUCK.search(plain):
            return True
    return False


def asked(line):
    text = " ".join(str(line or "").split())
    if not text:
        return None
    low = text.lower().replace("\u2019", "'")
    if "favourite" not in low and "favorite" not in low and " fav" not in low:
        return None
    if "your favourite" in low or "your favorite" in low:
        return None
    found = ASKS.search(LEAD.sub("", text))
    if not found:
        found = WHICH_IS.search(text)
    if not found:
        return None
    return _a_thing(found.group("thing")) or None


def _singular(thing):
    text = str(thing or "")
    if len(text) > 3 and text.endswith("s") and not text.endswith("ss"):
        return text[:-1]
    return text


def asks_all(line):
    text = " ".join(str(line or "").split())
    if not text:
        return False
    low = text.lower().replace("\u2019", "'")
    if "your favourite" in low or "your favorite" in low:
        return False
    return bool(ASKS_ALL.search(low))


def prefers_now(line):
    text = " ".join(str(line or "").split())
    if not text or "?" in text:
        return ""
    found = PREFERS_NOW.match(LEAD.sub("", text))
    if not found:
        return ""
    return _a_value(found.group("value"))


def an_answer(line, thing):
    text = " ".join(str(line or "").split())
    if not text or "?" in text or not thing:
        return ""
    plain = LEAD.sub("", text)
    if not AN_ANSWER.match(plain):
        return ""
    words = plain.lower().replace(".", "").replace("!", "").replace(",", "").split()
    if not words or any(word in ASK_TAIL or word in NOT_A_THING for word in words):
        return ""
    if all(word in ACKNOWLEDGES or word.startswith("thank") for word in words):
        return ""
    return _a_value(plain)


def corrected(line, thing):
    text = " ".join(str(line or "").split())
    if not text or "?" in text or not thing:
        return ""
    found = CORRECTS.match(text)
    if not found:
        return ""
    return _a_value(found.group("value"))


def kept(memory, thing):
    if not isinstance(memory, dict) or not thing:
        return ""
    held = (memory.get("user") or {}).get("favourites")
    if not isinstance(held, dict):
        return ""
    value = held.get(thing)
    if not isinstance(value, str):
        value = held.get(_singular(thing))
    return value if isinstance(value, str) else ""


def the_favourites(memory):
    if not isinstance(memory, dict):
        return []
    held = (memory.get("user") or {}).get("favourites")
    if not isinstance(held, dict):
        return []
    return [(thing, value) for thing, value in held.items() if isinstance(value, str)]


def store(memory, found):
    if not isinstance(memory, dict) or not isinstance(found, dict):
        return
    thing = found.get("thing")
    value = found.get("value")
    if not thing or not value:
        return
    known = memory.setdefault("user", {})
    held = known.get("favourites")
    if not isinstance(held, dict):
        held = {}
    held[thing] = value
    known["favourites"] = held


__all__ = ["read", "asked", "asks_all", "prefers_now", "an_answer", "corrected", "kept",
           "the_favourites", "store"]


KIN_APOSTROPHE = re.compile(
    r"\b(your (?:mum|mom|mam|mother|dad|father|son|daughter|sister|brother|wife|husband|partner"
    r"|nan|nana|granny|gran|grandma|grandad|grandpa|aunt|auntie|uncle|niece|nephew|cousin"
    r"|boyfriend|girlfriend|fiance|fiancee|mate|friend|boss))s\b", re.I)
MY_WORDS = {"myself": "yourself", "my": "your", "me": "you", "i": "you", "our": "your",
            "us": "you"}


def their_words(value):
    out = []
    for word in str(value or "").split():
        low = word.lower().strip(".,!?")
        swapped = MY_WORDS.get(low)
        if not swapped:
            out.append(word)
            continue
        tail = word[len(low):]
        out.append(swapped[:1].upper() + swapped[1:] if word[:1].isupper() else swapped)
        if tail:
            out[-1] += tail
    return KIN_APOSTROPHE.sub(r"\1's", " ".join(out))

def watch(text, memory):
    if not isinstance(memory, dict):
        return
    said = read(text)
    if not said:
        pending = memory.pop("favourite_asked", None) if isinstance(memory, dict) else None
        if isinstance(pending, str) and pending:
            answered = an_answer(text, pending)
            if answered:
                said = {"thing": pending, "value": answered}
                memory["favourite_told"] = dict(said)
    if not said:
        recent = memory.get("favourite_recent") if isinstance(memory, dict) else None
        if isinstance(recent, dict) and recent.get("thing") \
                and recent.get("turn") == len(memory.get("turns") or []) - 1:
            put_right = corrected(text, recent["thing"])
            if put_right:
                said = {"thing": recent["thing"], "value": put_right}
                memory["favourite_told"] = dict(said)
    if not said:
        recent = memory.get("favourite_recent") if isinstance(memory, dict) else None
        if isinstance(recent, dict) and recent.get("thing") \
                and len(memory.get("turns") or []) - int(recent.get("turn") or 0) <= 2:
            moved = prefers_now(text)
            if moved and moved != kept(memory, recent["thing"]):
                was = kept(memory, recent["thing"])
                said = {"thing": recent["thing"], "value": moved}
                memory["favourite_changed"] = {"thing": recent["thing"], "value": moved, "was": was}
    if said:
        store(memory, said)
        if isinstance(memory, dict):
            memory["favourite_recent"] = {"thing": said["thing"],
                                          "turn": len(memory.get("turns") or [])}
