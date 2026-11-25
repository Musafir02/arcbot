import re

from ..compose import pick
from ..memory import last_bot

PRIORITY = 1200

ASKS_WORDS = re.compile(
    r"\b(?:what|how)\s+(?:should|do|would|shall|can|could|might)\s+i\s+"
    r"(?:say|text|email|message|write|reply|answer|word|phrase|tell|open|start)\b"
    r"|\b(?:what|how)\s+(?:should|do|would|shall|can|could|might)\s+i\s+put\s+"
    r"(?:it|this|that|these|those|them)\b"
    r"|\b(?:what|how)\s+(?:should|do|would|shall|can|could|might)\s+i\s+put\s+"
    r"(?:[^?.]{0,30}?\b(?:in|into|on)\s+)?(?:the|my|his|her|their|your|our|a|an)\s+"
    r"(?:e-?mail|letter|card|note|text|message|msg|reply|answer|application|invitation|"
    r"invite|whatsapp|bio|post|comment|review|essay|report)\b"
    r"|\bhow\s+(?:do|should|would|can|could)\s+i\s+(?:word|phrase|put)\s+(?:it|this|that)\b"
    r"|\bhow\s+(?:do|should|would|can|could)\s+i\s+ask\s+(?:for\s+)?"
    r"(?:it|that|this|them|him|her|someone|somebody)\b"
    r"|\b(?:can|could|should)\s+i\s+ask\s+(?:for\s+)?"
    r"(?:it|that|this|them|him|her)\b(?:\s+(?:back|again))?[\s.?!]*$"
    r"|\b(?:can|could|would)\s+you\s+(?:word|phrase)\s+(?:it|this|that)\b"
    r"|\b(?:give|gimme)\s+me\s+the\s+words\b|\bwhat\s+are\s+the\s+words\b"
    r"|\bwhat(?:'s| is)\s+the\s+wording\b"
    r"|\b(?:don'?t|do\s+not|dont|no\s+idea|not\s+sure|never\s+know\s+how|can'?t\s+work\s+out)"
    r"\s+(?:know\s+)?how\s+to\s+"
    r"(?:tell|say|word|phrase|put|ask|bring|raise|mention|open|start|write|text|email|message)\b"
    r"|\b(?:don'?t|do\s+not|dont|no\s+idea|not\s+sure)\s+what\s+to\s+"
    r"(?:say|text|write|reply|message|email|call|tell)\b", re.I)

QUOTED = re.compile(
    r"(?<![A-Za-z0-9])'((?:[^']|'(?=[A-Za-z])){12,300})'(?![A-Za-z0-9])"
    r"|(?<![A-Za-z0-9])\"((?:[^\"]|\"(?=[A-Za-z])){12,300})\"(?![A-Za-z0-9])"
    r"|\u201c([^\u201d]{12,300})\u201d"
    r"|\u2018([^\u2019]{12,300})\u2019")

LINES = (
    "{words} Say that, and leave it there - it gives them an easy way to answer.",
    "{words} That is the whole of it, so don't add a second explanation after it.",
    "{words} Say it once, early, and let the silence do the rest.",
    "{words} Keep to those words and let them reply in their own time.",
    "{words} The short version lands better than a speech, so stop there.",
)


EXAMPLED = re.compile(r"(?:\b(?:a|an|the|one|like|such\s+as|e\.g\.))\s*$", re.I)


def _quoted(said):
    text = str(said or "")
    for match in QUOTED.finditer(text):
        words = next((group for group in match.groups() if group), "").strip()
        if len(words.split()) < 3:
            continue
        if EXAMPLED.search(text[max(0, match.start() - 18):match.start()]):
            if not re.search(r"[?!.]$", words) and "," not in words:
                continue
        return match.group(0).strip()
    return ""


ASK_OBJECT = re.compile(
    r"^(?:"
    r"(?:it|this|that|them|those)\b"
    r"|(?:to|for|at|with|in|on)\s+(?:him|her|them|it|this|that|me|us|everyone|somebody|anybody)\b"
    r"|(?:to|for|at|with|in|on)\s+(?:my|his|her|their|our|your|the|a|an)\s+[a-z']+"
    r"|(?:him|her|them|everyone|somebody)\b"
    r"|(?:my|his|her|their|our|your|the)\s+[a-z']+"
    r")", re.I)
ASK_FILLER = re.compile(r"^(?:please|then|instead|just|really|up|out|loud|back)\b[,.]?", re.I)


def _names_its_own(line):
    match = ASKS_WORDS.search(line)
    if not match:
        return True
    rest = line[match.end():].strip()
    for step in range(2):
        rest = rest.strip(" ,.-")
        moved = ASK_OBJECT.match(rest)
        if moved:
            rest = rest[moved.end():].strip()
        for _ in range(3):
            filler = ASK_FILLER.match(rest)
            if not filler:
                break
            rest = rest[filler.end():].strip()
    return bool(re.sub(r"[^a-z0-9]", "", rest.lower()))


def _the_words(text, memory):
    line = str(text or "").strip()
    if not line or len(line.split()) > 14 or not ASKS_WORDS.search(line):
        return ""
    if _names_its_own(line):
        return ""
    return _quoted(last_bot(memory))


def TAKES_AS_IT_COMES(text, memory):
    return bool(_the_words(text, memory))


def respond(text, memory):
    line = str(text or "").strip()
    words = _the_words(text, memory)
    if not words:
        return None
    return pick(LINES, memory, line).format(words=words)
