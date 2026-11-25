import re

from .aboutness import is_a_hedge as _a_hedge, restates_the_line, unlike_the_line

_VERBING = (r"(?:work\w*|show\w*|connect\w*|pair\w*|charg\w*|turn\w*|start\w*|boot\w*|"
           r"open\w*|load\w*|sync\w*|respond\w*|detect\w*|heat\w*|drain\w*|fill\w*|"
           r"print\w*|spin\w*|run\w*|play\w*|record\w*|boil\w*|flush\w*|close\w*|lock\w*|"
           r"los\w*|drop\w*|cut\w*|jamm\w*|fall\w*|slip\w*|stall\w*|stall?|squeal\w*|whistl\w*|"
           r"smell\w*|smoke|smoking|overheat\w*|beep\w*|go\w*|going|gone|drip\w*|clog\w*)")

A_TROUBLE = re.compile(
    r"(?:"
    r"\b(?:is\s+not|isn'?t|are\s+not|aren'?t|was\s+not|wasn'?t|does\s+not|doesn'?t|"
    r"do\s+not|don'?t|did\s+not|didn'?t)\s+" + _VERBING +
    r"|\b(?:wont|won'?t|will\s+not|wouldn'?t|refuses?\s+to)\s+" + _VERBING +
    r"|\b(?:keeps?|kept|stopped|stops)\s+" + _VERBING +
    r"|\b(?:is|are|it'?s)\s+(?:broken|bust|busted|dead|faulty|knackered|on\s+the\s+blink)\b"
    r"|\b(?:mak\w*|made)\s+(?:a\s+|an\s+|that\s+)?(?:noise|racket|din|humming|buzzing|whirring|clicking)\b"
    r"|\b(?:broke|broken|leaks?|leaking|leaked|stuck|sticking|noisy|noise|rattl\w*|slow|sluggish|"
    r"laggy|freez\w*|crash\w*|error|glitch\w*|bug|bugs|buggy|acting\s+up|playing\s+up|"
    r"gone\s+wrong|doing\s+something\s+weird)\b"
    r")", re.I)

NOT_A_MACHINE = re.compile(
    r"\b(?:son|daughter|child|kid|baby|mum|mom|mother|dad|father|wife|husband|partner|"
    r"boyfriend|girlfriend|brother|sister|friend|mate|nan|gran|grandad|grandma|aunt|uncle|"
    r"cousin|family|relationship|marriage|heart|trust|friendship|things)\b.{0,20}?"
    r"\b(?:is|are|was|were|it'?s)\s+(?:broken|bust|busted|dead|gone|over|finished|ruined)\b",
    re.I)

FIRE_WORD = re.compile(
    r"\b(?:spark\w*|scorch\w*|burn(?:s|ing|t)?|catch(?:es|ing)?\s+fire|flames?|"
    r"melt(?:s|ing|ed)?|fizz\w*|smoulder\w*)\b", re.I)

_NOT_THE_THING = frozenset("""
working work works worked showing show shows shown connecting connected pairing paired
charging charged turning turned booting booted starting started opening opened loading loaded
syncing synced updating updated playing played running ran doing done going stuck slow
wrong broken bust faulty weird strange dead fine better worse again still always never
keep keeps kept isnt arent wasnt doesnt dont didnt wont wont stop stops stopped making makes
noise leaking leak making enough too quite really
today tonight tomorrow yesterday morning afternoon evening night daytime weekend now later
meantime outside indoors upstairs downstairs somewhere anywhere nowhere everywhere here there
""".split())

ITS_THE_WEATHER = re.compile(
    r"^\s*(?:oh\s+)?(?:it'?s|its|it\s+is)\s+(?:so\s+|very\s+|really\s+|properly\s+|"
    r"absolutely\s+|bloody\s+|still\s+|turned\s+|got\s+)?(?:freezing|boiling|roasting|baltic|"
    r"chilly|nippy|pouring|raining|snowing|sleeting|hailing|blowing|howling|mild|warm|hot|cold|"
    r"wet|dry|damp|dark|grey|gray|grim|miserable|lovely|nice|glorious)\b"
    r"|\bchucking\s+it\s+down\b|\bblowing\s+a\s+gale\b"
    r"|\brain(?:ing|y)\s+(?:again|all\s+day|now)\b", re.I)

_REPLIES = (
    "%s - every time, or only sometimes?",
    "Has anything changed since %s last worked - an update, a new one, a move?",
    "%s - how long has it been doing that?",
)

_DETERMINERS = ("my", "our", "the", "this", "that", "your", "his", "her", "their", "its")

_FUNCTION = frozenset("""
the a an my our your his her their its this that these those that's thats some any something
anything nothing everything all most more less very just really quite still always never again
there here out up off down over back with without from than then about into onto and but so
when since while if or of to in on at for as it is are was were be been being got have has had
""".split())

_STOP = frozenset("""
is are was were has have had wont will does doesnt didnt not never keeps kept still always
in on at to of for with and but so when since about all just really very much more less
isnt arent wasnt dont wont cant couldnt shouldnt wouldnt
""".split())


def the_thing(clean):
    clean = str(clean or "")
    words = clean.split()
    spans = [(one.start(), one.end()) for one in A_TROUBLE.finditer(clean)]
    trouble_words = set()
    for start, end in spans:
        trouble_words.update(clean[start:end].split())
    found = [word for word in words
             if len(word) >= 3 and word not in _FUNCTION and word not in _NOT_THE_THING
             and word not in trouble_words
             and word.isalpha()]
    if not found:
        return ""
    return _named(clean, words, found, spans)


def _named(clean, words, found, spans):
    best = found[0]
    at = words.index(best)
    name = best
    after = words[at + 1] if at + 1 < len(words) else ""
    if (after and after.isalpha() and len(after) >= 4 and after in found
            and after not in _STOP):
        name = "%s %s" % (best, after)
    before = words[at - 1] if at else ""
    if before in _DETERMINERS:
        return "%s %s" % (before, name)
    return "the %s" % name


def _heavy(memory):
    from . import fallback as _fallback
    turns = list((memory or {}).get("turns") or [])
    if not turns:
        return False
    return bool(_fallback.reads_as_heavy_news(" ".join(str(turns[-1].get("user") or "").split()))
                or _fallback._the_thread_is_heavy({"turns": turns}))


def trouble_pool(clean, memory):
    clean = " ".join(str(clean or "").lower().split())
    if _heavy(memory):
        return None
    from . import fallback as _fallback
    if _fallback.reads_as_heavy_news(clean):
        return None
    if NOT_A_MACHINE.search(clean) or FIRE_WORD.search(clean):
        return None
    if ITS_THE_WEATHER.search(clean):
        return None
    if not clean or "?" in clean or len(clean.split()) < 3:
        return None
    if not A_TROUBLE.search(clean):
        return None
    thing = the_thing(clean)
    if not thing:
        return None
    pool = tuple((line % thing)[0].upper() + (line % thing)[1:] for line in _REPLIES)
    return pool if all(2 < len(line.split()) < 22 for line in pool) else None


_STOCK_LENGTH = 14

_ALREADY_NARROWING = re.compile(
    r"\b(?:every\s+time|now\s+and\s+then|now\s+and\s+again|when\s+did\s+it\s+start|"
    r"how\s+long\s+has|what\s+does\s+it\s+do|what'?s\s+it\s+doing|what\s+happens\s+when|"
    r"what\s+were\s+you\s+doing|since\s+when|what\s+it\s+does|what\s+have\s+you\s+tried|"
    r"tell\s+me\s+what|say\s+more)\b", re.I)


_A_BARE_OFFER = re.compile(
    r"^\s*(?:got it[.,]?\s*|okay[.,]?\s*|right[.,]?\s*)?"
    r"(?:is\s+there\s+anything|anything\s+else|what\s+else|can\s+i\s+help)", re.I)


def _a_bare_offer(reply):
    return bool(_A_BARE_OFFER.search(str(reply or "")))


STALL = re.compile(
    r"(?:\bi'?m listening\b|\bsay more if it helps\b|\btell me more\b|"
    r"\banything you'?d like a hand with\b|\bwhat'?s on your mind\b|"
    r"\bi'?m here if you want to\b)", re.I)


def says_nothing_about_the_line(reply, text):
    reply = str(reply or "").replace("\u2019", "'")
    if not reply.strip():
        return True
    if STALL.search(reply):
        return True
    if len(reply.split()) > _STOCK_LENGTH:
        return False
    if reply.rstrip().endswith("?") and not _a_bare_offer(reply):
        return False
    if _ALREADY_NARROWING.search(reply):
        return False
    if _a_hedge(reply) or restates_the_line(reply, text):
        return True
    about, said = unlike_the_line(reply, text)
    return bool(about) and not said
