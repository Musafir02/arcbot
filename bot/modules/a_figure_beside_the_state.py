import re

PRIORITY = 1000

_NUMBER = (r"(?:\d+(?:\.\d+)?|zero|one|two|three|four|five|six|seven|eight|nine|ten|eleven|"
           r"twelve|thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|nineteen|twenty|"
           r"thirty|forty|fifty|sixty|seventy|eighty|ninety|hundred)")
_UNIT = r"(?:degrees?|deg\b|°|celsius|centigrade|fahrenheit|c\b|f\b)"
_LEAD = (r"(?:its|it's|its\s+about|about|around|only|just|currently|still|nearly|almost|minus|"
         r"negative|plus|and|but|so|then|is|be)")
FIGURE = re.compile(rf"\b{_NUMBER}\s*{_UNIT}\b", re.I)
MINUS_FIGURE = re.compile(
    r"(?<![\w-])(?:minus\s+|[-\u2212]\s?)\d+\s*(?:degrees?)?"
    r"(?:\s*(?:outside|out\s+there|out|in\s+here|today|tonight|now))?", re.I)
MINUS_WORD = re.compile(r"(?<!\w)minus\s+\d+", re.I)
FIGURE_WITH_LEAD = re.compile(
    rf"\b(?:(?:{_LEAD})\s+)*{_NUMBER}\s*{_UNIT}\b(?:\s+(?:outside|out\s+there|in\s+here|here|"
    rf"today|tonight|now|outside|already|still))?", re.I)


def a_figure_of_heat(text):
    line = str(text or "")
    return bool(FIGURE.search(line) or MINUS_WORD.search(line) or MINUS_FIGURE.search(line))


def without_the_figure(text):
    line = FIGURE_WITH_LEAD.sub(" ", str(text or ""))
    line = MINUS_FIGURE.sub(" ", line)
    line = re.sub(r"\s+", " ", line)
    line = re.sub(r"^[\s,;:-]*(?:(?:its|it|it's|is|was|there|and|but|so|then|about|around|only|"
                  r"just|still|currently|be)\b[\s,;:-]*)+", "", line.strip())
    line = re.sub(r"[\s,;:-]+$", "", line.strip())
    line = re.sub(r"[\s,;:-]+(?:(?:its|it|it's|is|was|there|about|around|only|just|still|"
                  r"currently|and|but|so|then)\b[\s,;:-]*)+$", "", line.strip())
    return line.strip()


def a_state_said_with_a_figure(text):
    line = str(text or "")
    if not a_figure_of_heat(line):
        return None
    rest = without_the_figure(line)
    if not rest:
        return None
    from ..compose import fallback
    from ..compose.fallback_chain import _body_state
    try:
        return _body_state(rest)
    except Exception:
        return None


def respond(text, memory):
    understood = memory.get("understood") or {}
    clean = understood.get("clean") or text
    state = a_state_said_with_a_figure(clean)
    if not state:
        return None
    from ..compose import fallback
    from ..compose.fallback_chain import _choose
    from ..compose.fallback_data import BODY_POOLS
    pool = BODY_POOLS.get(state)
    if not pool:
        return None
    try:
        return _choose(pool, memory, clean)
    except Exception:
        return None


def takes_as_it_comes(text, memory):
    understood = memory.get("understood") or {}
    try:
        return bool(a_state_said_with_a_figure(understood.get("clean") or text))
    except Exception:
        return False


TAKES_AS_IT_COMES = takes_as_it_comes
