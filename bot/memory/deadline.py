import re

from . import topics

DEADLINE = re.compile(
    r"^\s*(?:(?:and|so|but|ok|okay|right|well|also|actually|probably|ideally|hopefully|"
    r"definitely|really|just|maybe)[ ,]+)*"
    r"(?P<lead>by|before|until|til|till|up\s+to|in\s+time\s+for|from)\s+"
    r"(?P<when>.+?)\s*[.!?]*$", re.I)

WHEN = re.compile(
    r"^(?:"
    r"(?:the\s+)?(?:end|start|beginning|middle)\s+of\s+(?:the\s+)?(?:month|year|week|summer)"
    r"|(?:this|next|the)\s+(?:month|year|week|summer|winter|spring|autumn|christmas|easter|"
    r"new\s+year|payday|weekend)"
    r"|(?:christmas|easter|payday|new\s+year|summer|winter|spring|autumn|nightfall|"
    r"then|tomorrow|tonight|today)"
    r"|(?:a|one)\s+(?:year|month|week|fortnight|couple\s+of\s+(?:weeks?|months?|years?))"
    r"|(?:\d{1,2}|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve)\s*"
    r"(?:days?|weeks?|months?|years?|hours?)"
    r"|(?:january|february|march|april|may|june|july|august|september|october|november|"
    r"december|jan|feb|mar|apr|jun|jul|aug|sep|sept|oct|nov|dec)"
    r"|(?:monday|tuesday|wednesday|thursday|friday|saturday|sunday)"
    r"|\d{1,2}(?:st|nd|rd|th)"
    r")$", re.I)

MONEY = re.compile(r"£\s?\d|\b\d+\s?(?:grand|pounds?|quid)\b|\b\d{3,}\b", re.I)

FILLER = frozenset("""and so ok okay right well also actually just maybe probably ideally
    hopefully definitely really then now too please thanks""".split())


def the_deadline(text):
    if not isinstance(text, str):
        return ""
    found = DEADLINE.match(text)
    if not found:
        return ""
    when = " ".join(found.group("when").lower().split())
    if not when or not WHEN.match(when):
        return ""
    return when


def _a_plan(said):
    said = " ".join(str(said or "").lower().split())
    if not said or said.endswith("?"):
        return False
    words = [word for word in topics.words(said) if word not in FILLER]
    if not words:
        return False
    return bool(MONEY.search(said))


def follow_up(text, memory):
    when = the_deadline(text)
    if not when:
        return ""
    turns = [turn for turn in (memory or {}).get("turns") or [] if isinstance(turn, dict)]
    for turn in reversed(turns[-3:]):
        said = str(turn.get("user") or "")
        if _a_plan(said):
            plan = " ".join(said.strip().rstrip(".!,").split())
            return plan + " by " + when
    return ""
