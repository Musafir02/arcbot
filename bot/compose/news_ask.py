
import re

A_FRAME = re.compile(
    r"^(?:so|and|ok|okay|well|but)?\s*"
    r"(?:any|anything|got|get|is\s+there|are\s+there|whats?|what\s+(?:is|are)|tell\s+me|"
    r"you\s+got|have\s+you\s+got|more|the|some)?\s*"
    r"(?:in\s+the\s+|from\s+the\s+|on\s+the\s+|the\s+)?"
    r"(?:news|headlines?)"
    r"(?:\s+(?:about|on|of|regarding)\s+.*"
    r"|\s+(?:today|tonight|this\s+(?:morning|afternoon|evening)|at\s+the\s+moment|"
    r"right\s+now|please|then)\b.*)?$")

A_NEWS_DOING = re.compile(
    r"\b(?:news|headlines?)\s+(?:is|are|was|were|has|have|had|gets?|got|makes?|made|keeps?|"
    r"puts?|bothered|upsets?|worries)\b")

A_VERDICT = re.compile(
    r"\b(?:no|some|good|bad|great|awful|sad|terrible|nice|exciting|brilliant|lovely|fantastic|"
    r"amazing|grim|big)\s+(?:news|headlines?)\b")

THEIR_OWN = re.compile(
    r"\b(?:i|we|my|our|his|her|their)\b.*\b(?:news|headlines?)\b|"
    r"\b(?:news|headlines?)\b.*\b(?:my|our|his|her|their)\b")

A_REPORT_VERB = re.compile(
    r"\b(?:watched|watching|read|reading|heard|hear|told|saw|seen|made|missed|followed|"
    r"caught)\b")

A_YEAR = re.compile(r"\b(?:19|20)\d\d\b")


def reads_as_an_ask_for_the_news(clean):
    said = (clean or "").strip().strip(" .!")
    if not A_FRAME.match(said):
        return False
    if A_NEWS_DOING.search(said) or A_VERDICT.search(said) or THEIR_OWN.search(said):
        return False
    if A_REPORT_VERB.search(said) or A_YEAR.search(said):
        return False
    return True
