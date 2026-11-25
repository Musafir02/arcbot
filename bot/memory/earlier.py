import re

from ..compose import pick

MONTHS = (r"january|february|march|april|may|june|july|august|september|october|november|"
          r"december|jan|feb|mar|apr|jun|jul|aug|sep|sept|oct|nov|dec")
DAYS = r"monday|tuesday|wednesday|thursday|friday|saturday|sunday|tomorrow|tonight|today"
UNITS = (r"kg|g|l|ml|kilo|kilos|kilogram|kilograms|gram|grams|lb|lbs|pound|pounds|ounce|ounces|"
         r"cm|mm|metre|metres|meter|meters|foot|feet|inch|inches|litre|litres|pint|pints")

KINDS = {
    "age": re.compile(r"(?<!year )(?<!size )\b\d{1,3}\b|\b(?:\d{1,2}|one|two|three|four|five|"
                      r"six|seven|eight|nine|ten|eleven|twelve|thirteen|fourteen|fifteen|sixteen|"
                      r"seventeen|eighteen|nineteen|twenty|thirty|forty|fifty|sixty|seventy|"
                      r"eighty|ninety)\s*(?:years? old|years?|yrs?|yo)\b|\baged?\s+\d", re.I),
    "name": re.compile(r"\b(?:called|named|calls|name(?:'s| is| was)?)\s+[a-z]", re.I),
    "when": re.compile(r"\b(?:" + MONTHS + "|" + DAYS + r"|\d{1,2}(?:st|nd|rd|th)\b|\d{1,2}"
                       r"(?:[:.]\d{2})?\s*(?:am|pm)\b|\d{1,2}[:.]\d{2})\b", re.I),
    "size": re.compile(r"\b(?:\d+(?:\.\d+)?\s*(?:" + UNITS + r")|size\s+\d+|\d+\s*(?:by|x)\s*\d+)",
                       re.I),
    "often": re.compile(r"\b(?:\d+\s+times|once|twice|three times|every\s+(?:day|week|month|"
                        r"morning|night|year)|a\s+(?:day|week|month)|most\s+(?:days|nights|"
                        r"weeks)|alternate)\b", re.I),
    "money": re.compile(r"£\s*\d|\b\d+(?:,\d{3})*\s*(?:pounds?|quid|k\b|grand)|\bbudget\b|"
                        r"\b\d{3,}\b", re.I),
    "duration": re.compile(r"\b(?:\d+(?:\.\d+)?|an?|one|two|three|four|five|six|seven|eight|"
                           r"nine|ten|twelve|fifteen|twenty|half an)\s*(?:hours?|hrs?|minutes?|"
                           r"mins?|days?|weeks?|months?|years?)\b", re.I),
    "count": re.compile(r"\b(?:\d+|one|two|three|four|five|six|seven|eight|nine|ten|eleven|"
                        r"twelve)\s+(?:(?:of|in)\s+)?(?:[a-z]{2,}s|people|children|men|women|"
                        r"us|them)\b", re.I),
    "place": re.compile(r"\b(?:in|at|to|from|live|living|moved)\s+[A-Za-z][a-z]{2,}", re.I),
}

ASKS = (
    (re.compile(r"\bhow old\b|\bage\b|\bhow many years\b"), "age"),
    (re.compile(r"\bwhat(?:'s|s| is| was)?\s+(?:it |they |he |she )?called\b|\bname\b|"
                r"\bcalled\b"), "name"),
    (re.compile(r"\bwhen\b|\bwhat day\b|\bwhat date\b|\bwhat time\b|\bwhich day\b|\bwhat month\b"),
     "when"),
    (re.compile(r"\bhow often\b|\bhow many times\b"), "often"),
    (re.compile(r"\bsize\b|\bhow big\b|\bhow tall\b|\bhow heavy\b|\bhow long is\b|\bhow wide\b|"
                r"\bhow deep\b|\bhow far\b"), "size"),
    (re.compile(r"\bhow much\b|\bbudget\b|\bhow much did i\b|\bwhat did i say i (?:paid|spent)\b"),
     "money"),
    (re.compile(r"\bhow long\b|\bhow many (?:days|weeks|months|years|hours|minutes)\b"), "duration"),
    (re.compile(r"\bhow many\b|\bhow many of\b"), "count"),
    (re.compile(r"\bwhere\b"), "place"),
)

CLAIM = re.compile(
    r"\b(?:you (?:haven'?t|have not) (?:told|said|mentioned|given)|you'?ve not (?:said|told|"
    r"mentioned)|you never (?:said|told|mentioned)|i don'?t have (?:your|the|their|his|her)\b[^.]*"
    r"\bfrom you|i (?:do not|don'?t) know (?:what|how|when|where|who)\b[^.]*\bsaid)",
    re.I)

VALUE_WORDS = frozenset((
    "heavy", "weigh", "weighs", "weight", "big", "tall", "height", "wide", "deep", "far", "long",
    "length", "size", "old", "age", "aged", "name", "called", "date", "day", "month", "time",
    "often", "times", "cost", "costs", "price", "paid", "spend", "spent", "much", "many", "number",
    "count", "amount", "budget", "how", "what",
))

PRONOUNS = frozenset((
    "i", "me", "my", "we", "us", "our", "you", "your", "he", "him", "his", "she", "her", "they",
    "them", "their", "it", "its", "the", "a", "an", "that", "this", "one", "there",
))
STOP = frozenset((
    "the", "a", "an", "and", "or", "but", "it", "its", "is", "was", "were", "are", "am", "be",
    "to", "of", "for", "in", "on", "at", "by", "with", "about", "again", "said", "say", "saying",
    "told", "tell", "you", "i", "me", "my", "have", "has", "had", "do", "did", "does", "not",
    "what", "when", "where", "which", "who", "how", "many", "much", "old", "size", "long",
    "often", "times", "time", "that", "this", "your", "yours", "called", "name", "names",
    "remember", "remind", "know", "think", "get", "got", "there", "their", "his", "her", "they",
    "them", "we", "our", "us", "one", "ones", "haven", "havent", "isnt", "wasnt", "didnt",
    "dont", "doesnt", "never", "mentioned", "given", "should", "would", "could", "will", "shall",
    "can", "any", "some", "just", "so", "if", "then", "than", "as", "from", "out", "up", "down",
))


def _a_word(word):
    return (word not in STOP and word not in PRONOUNS and word not in VALUE_WORDS
            and len(word) > 2 and "'" not in word)

HAND_BACK = (
    "You said: \"{line}\".",
    "That one you did say: \"{line}\".",
    "You told me: \"{line}\".",
)


def _turns(memory):
    turns = (memory or {}).get("turns")
    if not isinstance(turns, list):
        return []
    return [turn for turn in turns if isinstance(turn, dict)]


def said_lines(memory):
    said = []
    for number, turn in enumerate(_turns(memory), 1):
        line = str(turn.get("user") or "").strip()
        if not line or QUESTION.match(line) or line.endswith("?"):
            continue
        said.append((number, line))
    return said


def kind_of(text):
    low = " ".join(str(text or "").lower().replace("\u2019", "'").split())
    if not low:
        return None
    for pattern, kind in ASKS:
        if pattern.search(low):
            return kind
    return None


A_RATE = re.compile(r"\b(?:\d[\d,.]*|one|two|three|four|five|six|seven|eight|nine|ten|eleven|"
                    r"twelve)\s*(?:times?\s*)?(?:a|an|per|/|each|every)\s*(?:month|week|year|day|"
                    r"hour)\b|£?\s*\d[\d,.]*\s*(?:pounds?|quid|grand|k)?\s*(?:a|an|per|/|each|"
                    r"every)\s*(?:month|week|year|day|hour)\b", re.I)
A_TIMED_KIND = ("duration", "count")


def carries(kind, line):
    pattern = KINDS.get(kind or "")
    if not pattern:
        return False
    said = str(line or "")
    if kind in A_TIMED_KIND:
        said = A_RATE.sub(" ", said)
    return bool(pattern.search(said))


def _about(text):
    words = re.findall(r"[a-z']+", " ".join(str(text or "").lower().split()))
    return [word for word in words if _a_word(word)]


def _said_words(text):
    words = re.findall(r"[a-z']+", " ".join(str(text or "").lower().split()))
    out = []
    for word in words:
        if len(word) > 1 and word not in STOP and word not in PRONOUNS \
                and word not in VALUE_WORDS and "'" not in word and word not in out:
            out.append(word)
    return out


def _mentions(line, words):
    low = " ".join(str(line or "").lower().split())
    for word in words:
        if re.search(r"\b" + re.escape(word) + r"(?:s|es|'s|ing|ed)?\b", low):
            return True
    return False


def kinds_for(kind, ask):
    if kind == "money" and re.search(r"\bhow much\b", str(ask or ""), re.I):
        return ("money", "size")
    return (kind,)


def carried(memory, kind, about=(), window=None, prefer=(), after=0):
    lines = said_lines(memory)
    if window:
        lines = lines[-window:]
    if after:
        lines = [pair for pair in lines if pair[0] > after]
    hits = [(number, line) for number, line in lines if carries(kind, line)]
    if not hits:
        return None
    if about:
        for number, line in reversed(hits):
            if _mentions(line, about):
                return number, line
    if prefer:
        best, best_number, best_line = 0, None, None
        for number, line in hits:
            score = sum(1 for word in prefer if _mentions(line, (word,)))
            if score >= best:
                best, best_number, best_line = score, number, line
        if best:
            return best_number, best_line
    if about:
        return None
    return hits[-1]


def _pointing_back(memory, about):
    if not about:
        return False
    return any(_mentions(line, about) for _, line in said_lines(memory))


def carried_alone(memory, kind):
    hits = [line for _, line in said_lines(memory) if carries(kind, line)]
    return hits[0] if len(hits) == 1 else None


def hand_back(line, memory=None, text=""):
    low = " ".join(str(line or "").split())
    if not low:
        return None
    return pick(HAND_BACK, memory or {}, low + " " + str(text or "")).format(line=low)


def a_claim(reply):
    found = CLAIM.search(str(reply or ""))
    if not found:
        return None
    return str(reply)[found.start():]


RECALL = re.compile(r"\b(?:did i (?:say|tell|mention)|what did i say|what was it i said|"
                    r"remind me|what did we say|how did i say|again)\b", re.I)


def _values(kind, text):
    pattern = KINDS.get(str(kind or ""))
    if pattern is None:
        return set()
    low = " ".join(str(text or "").lower().split())
    out = set()
    for match in pattern.finditer(low):
        piece = " ".join(re.sub(r"[^a-z0-9. ]", " ", match.group(0)).split())
        if piece:
            out.add(piece)
    return out


def _the_line_the_ask_names(text, memory):
    low = " ".join(str(text or "").lower().replace("\u2019", "'").split())
    if not (RECALL.search(low) or their_own_words(low)):
        return None, (), None
    kind = kind_of(low)
    named = _said_words(low)
    if not kind or not named:
        return None, named, None
    return kind, named, carried(memory, kind, (), prefer=named)


def gives_the_named_value(text, memory, reply):
    kind, named, found = _the_line_the_ask_names(text, memory)
    if not found:
        return False
    return bool(_values(kind, reply) & _values(kind, found[1]))


def another_line_was_asked_for(text, memory, reply):
    kind, named, found = _the_line_the_ask_names(text, memory)
    if not found:
        return False
    if _mentions(str(reply or ""), named):
        return False
    return not gives_the_named_value(text, memory, reply)


HAND_BACKS = re.compile(r"^(?:You said|That one you did say|You told me)\b", re.I)


def a_misquoted_line(reply, memory, ask=""):
    text = str(reply or "")
    if not HAND_BACKS.match(text):
        return None
    quoted = re.search(r'"([^"]{2,300})"', text)
    kind = kind_of(ask)
    if not quoted or not kind:
        return None
    if _values(kind, quoted.group(1)):
        return None
    found = carried(memory, kind)
    if not found:
        return None
    if " ".join(found[1].lower().split()) == " ".join(quoted.group(1).lower().split()):
        return None
    return hand_back(found[1], memory, a_claim(text) or "")


def answer_for(text, memory):
    low = " ".join(str(text or "").lower().replace("\u2019", "'").split())
    if not low or not RECALL.search(low):
        return None
    kind = kind_of(low)
    if not kind:
        return None
    about = _about(low)
    named = _said_words(low)
    found = carried(memory, kind, about) if about else (
        carried(memory, kind, (), prefer=named)
        or (None if named else carried(memory, kind, (), window=3)))
    if not found and (not named or _pointing_back(memory, about)):
        alone = carried_alone(memory, kind)
        found = (len(said_lines(memory)), alone) if alone else None
    if not found:
        return None
    return hand_back(found[1], memory, low)


QUESTION = re.compile(r"^\s*(?:and|so|but|or|oh|also|then)?\s*(?:how|what|when|where|which|who|"
                      r"whose|why|do|does|did|is|are|was|were|am|can|could|should|would|will|"
                      r"shall|have|has|had|any)\b", re.I)


THEIR_OWN_WORDS = re.compile(r"\b(?:(?:did|do|does|have|had|was|were) i (?:say|tell|mention|said|"
                            r"go|use|have|had|get|got|buy|bought|pay|paid|book|pick|choose)|"
                            r"remind me|what was my|what did i|where did (?:i|we) say|again)\b", re.I)


def their_own_words(text):
    return bool(THEIR_OWN_WORDS.search(" ".join(str(text or "").lower().split())))


NOT_A_RECALL_ASK = re.compile(r"\b(?:should|could|would|will|shall|might|can|may|roughly|maybe|"
                             r"probably|need|needs|got to|have to|havent got|is it worth|better off|"
                             r"do you think|any (?:idea|chance)|recommend)\b", re.I)

NOT_A_PLAIN_ASK = ("when", "duration")


def from_the_line(text, memory):
    low = " ".join(str(text or "").lower().replace("\u2019", "'").split())
    if not low or not QUESTION.match(low):
        return None
    kind = kind_of(low)
    if not kind or kind in NOT_A_PLAIN_ASK:
        return None
    if NOT_A_RECALL_ASK.search(low):
        return None
    about = _about(low)
    named = _said_words(low)
    found = None
    for kind in kinds_for(kind, low):
        found = carried(memory, kind, about) if about else (
            carried(memory, kind, (), prefer=named)
            or (None if named else carried(memory, kind, (), window=3)))
        if found:
            break
        if not named or _pointing_back(memory, about):
            alone = carried_alone(memory, kind)
            found = (len(said_lines(memory)), alone) if alone else None
            if found:
                break
    if not found:
        return None
    return hand_back(found[1], memory, low)


def put_right(reply, memory, ask=""):
    claim = a_claim(reply)
    if not claim:
        return None
    asked = kind_of(claim) or kind_of(ask)
    kinds = (asked,) if asked else ("age", "name", "when", "size", "money", "often", "duration")
    named = _about(claim)
    subject = named or _about(ask)
    named_here = bool(named) and _mentions(str(ask or ""), named)
    window = None if subject else 3
    for kind in kinds:
        found = carried(memory, kind, subject, window=window)
        if found:
            return hand_back(found[1], memory, claim)
        if subject and not named:
            found = carried(memory, kind, (), window=3)
            if found:
                return hand_back(found[1], memory, claim)
        elif named:
            introduced = [number for number, line in said_lines(memory) if _mentions(line, named)]
            found = carried(memory, kind, ("she", "he", "they"),
                            after=max(introduced or [0]) if named_here else 0)
            if found:
                return hand_back(found[1], memory, claim)
    if named and not asked:
        for number, line in reversed(said_lines(memory)):
            if _mentions(line, named):
                return hand_back(line, memory, claim)
    return None
