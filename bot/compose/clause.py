import re

from bot.compose import fit

WHAT_TO_LOOK = re.compile(
    r"\bwhat\s+(?:to|(?:do|should|shall|can|could|must)\s+(?:i|we))\s+(?:need to\s+|"
    r"have to\s+|ought to\s+)?(?:look(?!\s+like\b)(?:\s+(?:out\s+|around\s+)?for)?|"
    r"check(?:\s+for)?|watch\s+out\s+for|ask(?:\s+for)?|avoid)\b", re.I)

NOTHING_TO_A_THING = re.compile(
    r"\bnothing (?:to|for) (?:wear|put on|bring|take|pack|cook|make|eat|have|drink|watch|read|"
    r"give|buy|get|play)\b", re.I)

_OPENS_A_QUESTION = ("what", "which", "how")

_SHAPES_FROM_A_CLAUSE = ("pick", "options", "steps")


def _said(read):
    return " ".join(str(read.get("clean") or read.get("text") or "").lower().split())


def _focus(read, said):
    focus = read.get("focus")
    if isinstance(focus, (list, tuple)):
        focus = " ".join(str(word) for word in focus)
    if not isinstance(focus, str):
        return None
    focus = " ".join(focus.lower().replace("\u2019", "'").split())
    if not focus or focus == said:
        return None
    if len(focus) > 0.85 * max(len(said), 1):
        return None
    return focus


def the_clause_ask(read):
    if not isinstance(read, dict):
        return None
    said = _said(read)
    focus = _focus(read, said)
    if focus is None or not focus.startswith(_OPENS_A_QUESTION):
        return None
    focus = " " + focus + " "
    if fit.WHAT_TO_PICK.search(focus):
        return "pick"
    if fit.WHAT_I_NEED.search(focus) or fit.WHAT_YOU_TAKE.search(focus):
        return "options"
    if fit.WHAT_TO_STEPS.search(focus) or fit.WHAT_TO_DO.search(focus) or WHAT_TO_LOOK.search(focus):
        return "steps"
    return None


def shape(read, want):
    if want in _SHAPES_FROM_A_CLAUSE or want in ("time", "amount", "place", "person", "meaning",
                                                 "reason", "number", "clock", "price"):
        return want
    if not isinstance(read, dict):
        return want
    said = _said(read)
    if NOTHING_TO_A_THING.search(said) and "list" not in (read.get("asks") or ()):
        return "pick"
    if WHAT_TO_LOOK.search(" " + said + " "):
        return "steps"
    return the_clause_ask(read) or want
