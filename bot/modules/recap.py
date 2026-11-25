import re

from . import memory_store

PRIORITY = 7000

WANTED_AGAIN = re.compile(
    r"\bwhat (?:were|are|was) (?:we|i|you) (?:just )?(?:talking|chatting|saying|on) about\b|"
    r"\bwhat (?:were|are|was) (?:we|i|you) (?:just )?saying\b|"
    r"\bwhat we were (?:just )?(?:talking|chatting|saying) about"
    r"(?=\s*(?:[?.!,]|$|again\b|earlier\b|before\b|just now\b))|"
    r"\bwhat we were (?:just )?saying(?=\s*(?:[?.!,]|$|again\b|earlier\b|before\b))|"
    r"\bwhere (?:were we|are we)(?=\s*(?:[?.!,]|$|up to\b|now\b|at\b))|"
    r"\bwhere (?:i|we) (?:were|was|are|got to|left off|ended up)\b"
    r"(?=\s*(?:[?.!,]|$|up to\b|now\b|again\b))|"
    r"\bwhat (?:were|was) (?:we|i) (?:looking at|doing)\b"
    r"(?=\s*(?:[?.!,]|$|again\b|earlier\b|before\b))|"
    r"\bwhat we were (?:just )?(?:looking at|doing)\b"
    r"(?=\s*(?:[?.!,]|$|again\b|earlier\b|before\b))|"
    r"\bback to (?:my|your|the) question\b(?=\s*(?:[?.!,]|$))")


def _recap_shape(text, memory):
    try:
        low = memory_store._folded(text, memory)
    except Exception:
        return ""
    if not low or not WANTED_AGAIN.search(low):
        return ""
    return low


def ASKS_ABOUT_THE_CHAT(text, memory):
    return bool(_recap_shape(text, memory))


def _not_a_recap(text, memory):
    try:
        return bool(memory_store._about_this_chat(text, memory)) or bool(
            _recap_shape(text, memory))
    except Exception:
        return False


def _the_recap(memory, low):
    from ..memory import thread
    said = thread.last_said(memory, _not_a_recap)
    thing = thread.about(memory, _not_a_recap)
    if thing and not memory_store._a_thing(thing):
        thing = None
    ask = thread.last_ask(memory, _not_a_recap,
                          not_before=thread.topic_index(memory, _not_a_recap))
    if thing and ask:
        options = ["We were on " + thing + " \u2014 you asked " + ask + ". Want to carry on?",
                   "Still on " + thing + ": you asked " + ask + ".",
                   "The last thing we got into was " + thing + ", and you asked " + ask + "."]
    elif ask and said:
        options = ["You said " + said + ". You asked " + ask + ". Want to carry on?",
                   "You said " + said + " - and you asked " + ask + ".",
                   said[:1].upper() + said[1:] + ". Your question was " + ask + "."]
    elif ask:
        options = ["You asked " + ask + ". Want to carry on?", "You were asking " + ask + "."]
    elif said:
        options = ["You said " + said + ". Want to carry on?", "You last said " + said + ".",
                   "You'd told me " + said + ".", "Last thing you said was " + said + "."]
    elif thing:
        options = ["We were on " + thing + ".", "Still " + thing + "."]
    else:
        return ""
    return _fresh(options, memory)


def _fresh(options, memory):
    try:
        last = str(memory_store.last_bot(memory) or "").strip()
    except Exception:
        last = ""
    fresh = [option for option in options if option.strip() != last] or options
    return memory_store._vary(fresh, memory)


def respond(text, memory):
    low = _recap_shape(text, memory)
    if not low:
        return None
    try:
        if memory_store._about_the_bot_here(memory):
            return None
        said = _the_recap(memory, low)
    except Exception:
        return None
    return said or None
