import re

ASKS = (
    ("time", re.compile(
        r"\b(?:what|which)\s+(?:time|hour)\b|\bthe\s+(?:time|hour)\b|"
        r"\b(?:what\s+time|the\s+time|the\s+hour)\s+(?:again|was\s+it|is\s+it|did\s+i)\b|"
        r"\bo'?clock\b", re.I)),
    ("day", re.compile(
        r"\b(?:what|which)\s+(?:day|date)\b|\bthe\s+(?:day|date)\b|"
        r"\b(?:what|which)\s+(?:day|date)\s+(?:again|was\s+it)\b", re.I)),
    ("when", re.compile(r"^\W*(?:and\s+|also\s+)?when\b|\bwhen\s+(?:again|was\s+it|is\s+it)\b",
                        re.I)),
    ("make", re.compile(
        r"\b(?:what|which)\s+(?:make|brand|model|manufacturer)\b|"
        r"\b(?:make|brand|model)\s+(?:again|is\s+it|was\s+it)\b", re.I)),
    ("price", re.compile(
        r"\bhow\s+much\b|\b(?:what|which)\s+(?:price|cost)\b|\bthe\s+(?:price|cost)\b|"
        r"\b(?:what|how\s+much)\s+did\s+(?:i|we|you)\s+pay\b|"
        r"\bhow\s+much\s+(?:again|was\s+it|did\s+i)\b", re.I)),
    ("duration", re.compile(r"\bhow\s+long\b", re.I)),
    ("size", re.compile(
        r"\b(?:what|which)\s+size\b|\bhow\s+(?:big|tall|wide|heavy|far)\b|"
        r"\b(?:what|which)\s+size\s+(?:again|was\s+it)\b", re.I)),
    ("age", re.compile(r"\bhow\s+old\b|\b(?:what|which)\s+age\b", re.I)),
    ("colour", re.compile(r"\b(?:what|which)\s+colou?r\b|\bcolou?r\s+(?:again|was\s+it|is\s+it)\b",
                          re.I)),
    ("place", re.compile(r"\bwhere\b|\b(?:what|which)\s+(?:place|town|city|airport)\b", re.I)),
    ("name", re.compile(
        r"\b(?:what|which)\s+(?:name|make\s+is\s+it\s+called)\b|\bwho\s+(?:made|makes|built)\b|"
        r"\bwhat'?s\s+it\s+called\b|\bwhat\s+was\s+it\s+called\b", re.I)),
)

GIVES = {
    "time": re.compile(
        r"\b(?:at|by|around|about|from|until|till|before|after)\s+\d{1,2}(?::\d\d)?"
        r"(?:\s*(?:am|pm|a\.m\.|p\.m\.))?\b|"
        r"\b\d{1,2}(?::\d\d)?\s*(?:am|pm)\b|\b(?:noon|midday|midnight)\b|"
        r"\b(?:half|quarter)\s+(?:past|to)\s+\w+|\bo'?clock\b", re.I),
    "day": re.compile(
        r"\b(?:monday|tuesday|wednesday|thursday|friday|saturday|sunday|"
        r"mon|tues|tue|weds|wed|thurs|thu|fri|sat|sun|tomorrow|today|tonight|"
        r"weekend|next\s+(?:week|month|year)|this\s+week|"
        r"the\s+\d{1,2}(?:st|nd|rd|th)|\d{1,2}(?:st|nd|rd|th)\s+(?:of\s+)?[a-z]+)\b", re.I),
    "make": re.compile(
        r"\b(?:it'?s|its|it\s+is|i\s+got|we\s+got|i\s+bought|we\s+bought|they\s+installed)\s+"
        r"(?:a|an)\s+[a-z][\w-]*(?:\s+[a-z][\w-]*)?", re.I),
    "price": re.compile(
        r"[£$€]\s*\d|\b\d[\d,.]*\s*(?:pounds?|quid|euros?|dollars?)\b|"
        r"\b(?:costs?|cost\s+me|paid|paying|charges?|quote[ds]?)\b|"
        r"\b\d[\d,.]*\s*(?:pounds?|quid|euros?|dollars?)\s+a\s+(?:month|week|year)\b", re.I),
    "size": re.compile(
        r"\b\d+(?:\.\d+)?\s*(?:mm|cm|m|metres?|meters?|feet|foot|ft|inches|inch|in|kg|kilos?|"
        r"grams?|g|stone|lb|lbs|litres?|liters?|miles?|ml)\b|\bsize\s+\w", re.I),
    "age": re.compile(
        r"\b(?:\d{1,3}|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|thirteen|"
        r"fourteen|fifteen|sixteen|seventeen|eighteen|nineteen|twenty)\s*(?:years?|months?|weeks?)"
        r"\s*(?:old)?\s*(?=$|[.,;!?]|\b(?:and|or|in|now|so)\b)|\baged\s+\d", re.I),
    "place": re.compile(
        r"\b(?:in|at|from|to|near|outside|inside|via)\s+(?!night|morning|afternoon|evening|"
        r"all|least|once|times?|moment|end|same|other|top|bottom|front|back|side|way|case|fact|"
        r"past|future|total|order|general|particular|short|full|half|the\s+(?:end|moment|same|"
        r"other|top|bottom|front|back|side|way|case|fact|total|order))[a-z][\w'-]+", re.I),
    "when": re.compile(
        r"\b(?:at|by|around)\s+\d{1,2}(?::\d\d)?(?!\d)|\b\d{1,2}\s*(?:am|pm)\b|"
        r"\b(?:monday|tuesday|wednesday|thursday|friday|saturday|sunday|tomorrow|today|tonight|"
        r"next\s+week|this\s+week)\b", re.I),
    "colour": re.compile(
        r"\b(?:red|blue|green|yellow|black|white|grey|gray|brown|pink|purple|orange|beige|"
        r"cream|navy|silver|gold|teal|turquoise|maroon|olive|grey|charcoal)\b", re.I),
    "name": re.compile(
        r"\b(?:called|named)\s+[a-z]|\bname'?s?\s+[a-z]|\b(?:it'?s|its)\s+[A-Z]", 0),
}

BACK_REF = re.compile(
    r"^\W*(?:(?:and|but|so|oh|also|well|yeah|yep|ok|okay|right|alright)\W+)*"
    r"(?:it'?s|its|it\s+is|they'?re|they\s+are|that'?s|there'?s|there\s+are|"
    r"it\s+was|was|is|are)\b", re.I)

LEAD = re.compile(
    r"^\W*(?:(?:and|but|so|oh|also|well|yeah|yep|ok|okay|right|alright|sorry|hmm|hi|hiya|hey|"
    r"hello|now|then|again|quick\s+one|mate)[ ,.!-]+)*", re.I)

FRAME = frozenset("""
a an the and but so or if my our your their his her its it this that these those of to in on at
for with from about again was were is are am be been being do does did done have has had
what which who whom whose when where why how much many long old big tall wide heavy far
time hour day date make brand model manufacturer price cost size age number place town city
airport name called colour color count weight height length say said tell told mention mentioned
pay paid paying cost costs costed charge charged spend spent buy bought
i we you me us them they he she
just only even ever before already first last next other another else more most still yet now
please pls can could would will shall may might should must cant cannot dont doesnt didnt
remember recall forget forgot know knew knews remind mind think thought reckon guess
go goes going went gone come comes coming came been
one ones thing things stuff kind sort like
""".split())


A_RECALL_SAID = re.compile(
    r"\b(?:again|before|earlier|was\s+(?:it|that)|did\s+(?:i|we|you)|have\s+i|you\s+know|tell\s+me|"
    r"remind(?:ed)?\s+me|the\s+(?:time|hour|day|date|make|model|brand|price|cost|size|name|"
    r"place|colour|color|number))\b", re.I)


A_QUESTION = re.compile(
    r"\?\s*$|^\W*(?:what|which|who|whom|whose|when|where|why|how|is|are|was|were|do|does|did|"
    r"can|could|should|would|will|shall|have|has|am|any|remind|tell\s+me)(?:'?s)?\b", re.I)


UNNAMED_KINDS = frozenset("price colour size age make".split())


AN_END = re.compile(r"\b(?:end|ends|ending|finish|finishes|finishing|last|lasts|leaves|leaving|"
                    r"close|closes|closing)\b", re.I)
A_START = re.compile(r"\b(?:start|starts|starting|started|begin|begins|beginning|began|"
                     r"open|opens|opening)\b", re.I)


def _the_other_end(ask, line):
    asking_end = bool(AN_END.search(ask))
    asking_start = bool(A_START.search(ask))
    if asking_end == asking_start:
        return False
    return bool(A_START.search(line)) if asking_end else bool(AN_END.search(line))


ASKS_WHAT_TO_DO = re.compile(
    r"\b(?:do|does|should|can|could|would|shall|will|might)\s+(?:i|we|you)\b", re.I)


def _flat(text):
    return " ".join(str(text or "").lower().split())


def _words(line, length=2):
    out = set()
    for word in re.findall(r"[a-z][a-z'\-]*", _flat(line)):
        word = word.strip("'-")
        if len(word) < 3 or word in FRAME:
            continue
        out.add(word)
        if len(word) > 4 and word.endswith("s"):
            out.add(word[:-1])
    return out


def _mentions(line, wanted):
    have = _words(line)
    flat = _flat(line)
    for word in wanted:
        if word in have or word in flat:
            return True
        if len(word) > 4 and word[:-1] in have:
            return True
    return False


def _their_lines(memory):
    turns = memory.get("turns")
    if not isinstance(turns, list):
        return []
    out = []
    for turn in turns:
        if isinstance(turn, str):
            continue
        if not isinstance(turn, dict):
            continue
        line = " ".join(str(turn.get("user") or "").split())
        if not line or A_QUESTION.match(line):
            continue
        out.append(line)
    return out


def the_kind_asked(text):
    low = _flat(text)
    return [kind for kind, pattern in ASKS if pattern.search(low)]


def the_line_that_gives(text, lines):
    kinds = the_kind_asked(text)
    if not kinds:
        return None
    lines = [line for line in (lines or []) if line and not A_QUESTION.match(line)]
    if not lines:
        return None
    low = LEAD.sub("", _flat(text))
    if not A_QUESTION.match(low):
        return None
    if ASKS_WHAT_TO_DO.search(low):
        return None
    named = {word for word in re.findall(r"[a-z][a-z'\-]*", low)
             if word not in FRAME and len(word) > 2}
    asking_again = bool(A_RECALL_SAID.search(low))
    if not named and not asking_again and not any(kind in UNNAMED_KINDS for kind in kinds):
        return None
    for kind in kinds:
        gives = GIVES.get(kind)
        if gives is None or (not named and not asking_again
                             and kind not in UNNAMED_KINDS):
            continue
        for index in range(len(lines) - 1, -1, -1):
            line = lines[index]
            if not gives.search(line):
                continue
            if _the_other_end(low, line):
                continue
            if not named or _mentions(line, named):
                return {"line": line, "kind": kind}
            if index and BACK_REF.match(line) and _mentions(lines[index - 1], named):
                return {"line": line, "kind": kind}
    return None
