from ..compose import fit, loss, pick
from ..understanding import understand

PRIORITY = 2000
ANSWERS = ("loss", "grief")
ANSWERS_INSTEAD = ("loss", "grief")
def defers_to(reply, line):
    if (loss.acknowledges(reply) and loss.a_pet_died(line)
            and not loss.names_a_feeling(line)
            and loss.asks_for_a_decision(line)
            and loss.asks_about_the_remains(line)):
        return True
    if not loss.asks_the_administration(line) or loss.names_a_feeling(line):
        return False
    if not loss.is_about_the_paperwork(reply, line):
        return False
    want = fit.wants(understand(line))
    return bool(want and fit.gives(reply, want, line))


DEFERS_TO = defers_to


def respond(text, memory):
    understood = _reading(text, memory)
    if understood.get("about_bot"):
        return None
    clean = understood.get("clean")
    words = understood.get("words")
    if not isinstance(words, list):
        words = None
    options = _options(text, memory, clean, understood, words)
    if not options:
        return None
    reply = pick(options, memory, text)
    _the_missing_said(memory, reply)
    return reply


def _the_missing_said(memory, reply):
    if not isinstance(memory, dict) or reply not in loss.MISS_REPLIES:
        return
    turns = memory.get("turns")
    memory["heavy_reply"] = {"feeling": "missing",
                             "turn": len(turns) if isinstance(turns, list) else 0}


def _reading(text, memory):
    stored = memory.get("understood")
    if isinstance(stored, dict) and _same(stored.get("clean"), text):
        return stored
    try:
        read = understand(text, memory)
    except Exception:
        return {}
    return read if isinstance(read, dict) else {}


def _same(stored, text):
    if not isinstance(stored, str) or not stored.strip():
        return False
    return " ".join(loss.words_of(stored)) == " ".join(loss.words_of(text))


def _options(text, memory, clean, understood, words):
    try:
        if words is None:
            words = loss.words_of(text)
        return loss.reply_for(text, memory, clean, understood.get("topics"), _mood(words))
    except Exception:
        return None


def _mood(words):
    try:
        cues = _cues()
        if set(words) & cues:
            return "negative"
    except Exception:
        pass
    return None


def _cues():
    from ..compose.fallback import NEGATIVE_CUES
    return NEGATIVE_CUES
