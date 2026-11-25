import re

try:
    from ..compose import pick
except Exception:
    pick = None

WHO_IS_IT = (
    "Who do you mean?",
    "Who's that, then?",
    "Who are we talking about?",
)

PRIORITY = 7300

A_THIRD_PARTY = re.compile(
    r"\b(?:he|she|him|her|his|hers|they|them|their|theirs)\b", re.I)

SOMEBODY_IN_THE_LINE = re.compile(
    r"\b(?:i|i'm|im|me|my|mine|myself|we|us|our|ours|you|your|yours|yourself|yourselves|"
    r"someone|somebody|anyone|anybody|everyone|everybody|people|nobody|no one)\b", re.I)

NAMES_THEM = re.compile(r"\b(?:my|our|the|this|that|these|those)\s+[a-z][a-z'-]{1,}", re.I)

A_FACT_ABOUT_THEM = re.compile(
    r"\bhow (?:old|tall|big|heavy|far|long)\b"
    r"|\b(?:what|whats|what's)\b[^?]*\b(?:name|age|job|birthday|number|address)\b"
    r"|\bwhere (?:does|do|did|is|was)\b[^?]*\b(?:live|work|come from|from|stay|based)\b"
    r"|\b(?:is|are|was|were)\s+(?:he|she|they)\b"
    r"|\bhow (?:is|are|was|were)\s+(?:he|she|they)\b",
    re.I)

AN_ASK = re.compile(
    r"^\s*(?:how|what|whats|what's|where|when|which|why|is|are|was|were|does|do|did|has|have|"
    r"can|could|would|will)\b", re.I)


def _there_is_a_chat(memory):
    turns = memory.get("turns") if isinstance(memory, dict) else None
    for turn in turns or ():
        if isinstance(turn, dict) and str(turn.get("user") or "").strip():
            return True
    return False


def _flat(text):
    return " ".join(str(text or "").lower().replace("\u2019", "'").split())


def about_somebody_unnamed(text, memory):
    if _there_is_a_chat(memory):
        return False
    said = _flat(text)
    if not said:
        return False
    if not AN_ASK.search(said) and "?" not in said:
        return False
    if not A_THIRD_PARTY.search(said) or not A_FACT_ABOUT_THEM.search(said):
        return False
    return not SOMEBODY_IN_THE_LINE.search(said) and not NAMES_THEM.search(said)


def respond(text, memory):
    if not isinstance(memory, dict):
        return None
    if not about_somebody_unnamed(text, memory):
        return None
    if pick is not None:
        try:
            return pick(WHO_IS_IT, memory, _flat(text))
        except Exception:
            pass
    return WHO_IS_IT[0]
