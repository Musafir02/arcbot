import re

from ..compose import pick
from . import meant

DOUBT = re.compile(
    r"^\s*(?:and\s+|so\s+|but\s+|ok\s+|okay\s+|well\s+|right\s+|hmm+\s+|ah\s+|oh\s+)*"
    r"(?:"
    r"(?:is|isnt|isn'?t|would|will|was|does)\s+(?:it|that|this|there)\s+(?:be\s+)?"
    r"(?:too\s+(?:late|old|young)|"
    r"still\s+(?:worth\s+(?:it|doing|a\s+go)|possible|an?\s+option|on|fine|alright|ok|okay|"
    r"any\s+good)|"
    r"worth\s+(?:it|doing|a\s+go))|"
    r"(?:am|are|was|were)\s+(?:i|we|you)\s+too\s+(?:old|late|young|far\s+gone)|"
    r"(?:am|are|is|was|were)\s+(?:i|we|you|it|that|this)\s+too\s+(?:old|late|young)\s+to\s+"
    r"(?:get|be|become|do|learn|start)\s+(?:any\s+)?(?:good|better|decent|anywhere)"
    r"(?:\s+(?:at|with)\s+(?:it|that|this|[a-z'-]+))?\b|"
    r"(?:im|i'?m)\s+too\s+(?:old|late|young)\s+to\s+"
    r"(?:get|be|become|do|learn|start)\s+(?:any\s+)?(?:good|better|decent|anywhere)"
    r"(?:\s+(?:at|with)\s+(?:it|that|this|[a-z'-]+))?\b|"
    r"(?:can|could)\s+(?:i|we|you|she|he|they)\s+still\s+"
    r"(?:do|learn|start|join|try|manage|cope|go|take\s+it\s+up|get\s+into)\b(?:\s+(?:it|that|this))?|"
    r"(?:is|isnt|isn'?t)\s+there\s+(?:still\s+)?(?:time|a\s+chance|any\s+point|a\s+point)|"
    r"too\s+late(?:\s+(?:for\s+me|now|isnt\s+it|right))?|"
    r"(?:what|whats|what'?s)\s+the\s+point(?:\s+(?:now|of\s+it|in\s+(?:it|trying)))?|"
    r"any\s+point(?:\s+(?:now|in\s+(?:it|trying)))"
    r")"
    r"(?:\s+to\s+(?:learn|start|begin|try|catch\s+up|get\s+any\s+good|get\s+going|improve|"
    r"take\s+it\s+up|change|retrain|study|practise|practice|go\s+back))?"
    r"\s*[?.!]*\s*$", re.I)

ANYONE = re.compile(
    r"\b(?:complete\s+beginners?|beginners?|any\s+age|no\s+age|never\s+too\s+late|"
    r"at\s+your\s+own\s+pace|whatever\s+your\s+age|whatever\s+age|all\s+ages|"
    r"people\s+start|"
    r"just\s+as\s+at\s+\w+|the\s+same\s+at\s+\w+\s+as\s+at\s+\w+|"
    r"adults?\s+(?:who|pick|learn|learns|starting|start|started|take|took|can|could|are|do|"
    r"in\s+their|of\s+any|taught|like)\b)", re.I)

LEADS = (
    "Not too late — {said}",
    "Never too late: {said}",
    "It is not too late — {said}",
)

GET_ANY_GOOD = re.compile(
    r"\btoo\s+(?:old|late|young)\s+to\s+(?:get|be|become|do|learn|start)\s+"
    r"(?:any\s+)?(?:good|better|decent|anywhere)\b", re.I)
WITHOUT_A_SUBJECT = (
    "Not too late — what decides it is a regular slot in the week, not the year you start in",
    "Never too late: a short practice most days does more than a long one now and then",
    "It is not too late — adults who start later tend to know what they want from it",
)

SAYS_IT = re.compile(r"\b(?:not\s+too\s+late|never\s+too\s+late|no\s+age\s+limit|any\s+age)\b",
                     re.I)


def _the_sentence(said):
    for sentence in meant._sentences(said):
        if sentence.strip().endswith("?"):
            continue
        if not ANYONE.search(sentence):
            continue
        gist = meant._gist(sentence)
        if not ANYONE.search(gist):
            gist = _two_clauses(sentence) or gist
        if len(gist.split()) < 4:
            continue
        return gist
    return None


def _two_clauses(sentence):
    cuts = [match.start() for match in meant.CLAUSE.finditer(sentence)]
    if len(cuts) >= 2:
        return sentence[:cuts[1]].strip(" ,;:-.") + "."
    if len(cuts) == 1 and len(sentence.split()) <= 40:
        return sentence.strip().rstrip(" ,;:-.") + "."
    return ""


def _the_reply(sentence, memory, clean):
    body = sentence.rstrip(".!?")
    if SAYS_IT.search(body):
        return body[0].upper() + body[1:] + (sentence[len(body):] or ".")
    said = body[0].lower() + body[1:] + (sentence[len(body):] or ".")
    return pick(LEADS, memory, clean).format(said=said)


def answer_for(text, memory):
    if not isinstance(memory, dict):
        return None
    clean = (text or "").strip()
    if not DOUBT.match(clean):
        return None
    answers = meant._answers(memory)
    if answers and meant.repeat.HEDGE.search(answers[0][0]):
        return None
    for said, _asked in answers:
        if meant.repeat.HEDGE.search(said):
            continue
        sentence = _the_sentence(said)
        if sentence:
            return _the_reply(sentence, memory, clean)
    if GET_ANY_GOOD.search(clean):
        return pick(WITHOUT_A_SUBJECT, memory, clean)
    return None
