import re

from ..memory import topics as _topics

PRIORITY = 6900

A_DONENESS_ASK = re.compile(
    r"\b(?:how (?:will|would|do|can|should) (?:i|you) (?:know|tell)|when (?:will|do) (?:i|you) know|"
    r"when (?:is|will) it(?: be)?|is it|are they|will it be|how long (?:do|should) (?:i|you) "
    r"(?:cook|leave|bake|roast|boil|fry|grill|simmer))", re.I)
DONENESS_WORDS = re.compile(
    r"\b(?:done|dones|cooked|uncooked|overdone|undercooked|overcooked|ready)\b", re.I)
DONENESS_KEYS = ("done", "cooked", "cooked through", "ready", "how can i tell",
                 "how do i tell", "how do you tell", "when is it done", "when its done",
                 "temperature", "temp", "thermometer")


def _entry(text):
    from ..knowledge.lookup import find
    said = " ".join(str(text or "").lower().split())
    if not said:
        return None
    return find({"clean": said, "words": _topics.words(said)})


def _the_answer_to_lean_on(memory):
    for one in reversed((memory or {}).get("turns") or ()):
        said = str((one or {}).get("bot") or "")
        if said:
            return said
    return ""


def _the_topics_on_the_chat(memory):
    out = []
    for one in reversed((memory or {}).get("topics") or ()):
        said = str((one or {}).get("text") or "")
        if said and said not in out:
            out.append(said)
    record = (memory or {}).get("topic")
    said = str(record.get("text") or "") if isinstance(record, dict) else ""
    if said in out:
        out.remove(said)
    if said:
        out.insert(0, said)
    return out


def _key_groups(item):
    groups = []
    for part in getattr(item, "key", ()) or ():
        if isinstance(part, str):
            groups.append((part,))
        elif isinstance(part, (tuple, list)):
            groups.append(tuple(one for one in part if isinstance(one, str)))
    return groups


def _keys_the_word(phrases, word):
    word = str(word or "")
    if not word:
        return False
    said = set()
    for phrase in phrases:
        said.update(_topics.words(phrase))
    if word in said:
        return True
    for one in said:
        try:
            if word in _topics.forms(one) or one in _topics.forms(word):
                return True
        except Exception:
            continue
    return False


def _about_the_thing(item, word):
    groups = _key_groups(item)
    return bool(groups) and _keys_the_word(groups[0], word)


def _says_how_it_turns_out(item):
    for group in _key_groups(item):
        said = set()
        for phrase in group:
            said.update(_topics.words(phrase))
        for one in DONENESS_KEYS:
            if set(_topics.words(one)) <= said:
                return True
    return False


def _the_thing_words(memory, said_words):
    out = []
    for topic in _the_topics_on_the_chat(memory):
        for word in _topics.keywords(topic):
            if word in said_words or word in _topics.MEASURE_WORDS or word in out:
                continue
            out.append(word)
    return out


def _the_chat_has_moved_on(found, memory):
    said = " ".join(str((memory or {}).get("understood", {}).get("clean") or "").split())
    mine = str(getattr(found, "domain", "") or "")
    if not mine:
        return False
    for topic in _the_topics_on_the_chat(memory):
        topic = " ".join(str(topic or "").split())
        if not topic or topic == said:
            continue
        here = _entry(topic)
        if here is None:
            continue
        theirs = str(getattr(here, "domain", "") or "")
        return bool(theirs) and theirs != mine
    return False


def the_done_state_of_the_thing_in_hand(line, memory):
    said = " ".join(str(line or "").lower().split())
    if not said or not A_DONENESS_ASK.search(said) or not DONENESS_WORDS.search(said):
        return ""
    if not _the_answer_to_lean_on(memory):
        return ""
    said_words = set(_topics.words(said))
    for word in _the_thing_words(memory, said_words):
        for filled in (word + " " + said, said.rstrip("?.! ") + " " + word):
            found = _entry(filled)
            if found is None:
                continue
            if not _about_the_thing(found, word):
                continue
            if not _says_how_it_turns_out(found):
                continue
            if _the_chat_has_moved_on(found, memory):
                return ""
            return filled
    return ""


def observe(line, memory):
    if not isinstance(memory, dict):
        return
    read = memory.get("understood")
    if not isinstance(read, dict):
        return
    said = str(read.get("clean") or read.get("text") or line or "")
    filled = the_done_state_of_the_thing_in_hand(said, memory)
    if not filled:
        return
    reading = dict(read)
    reading["clean"] = filled
    reading["words"] = _topics.words(filled)
    if "norm_text" in reading:
        reading["norm_text"] = filled
    memory["understood"] = reading
