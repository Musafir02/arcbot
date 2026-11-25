import re


def turns(memory):
    held = memory.get("turns") if isinstance(memory, dict) else None
    if not isinstance(held, list):
        return []
    return [one for one in held if isinstance(one, dict)]


def there_is_one(memory):
    return bool(turns(memory))


def lines(memory):
    said = []
    for turn in turns(memory):
        line = " ".join(str(turn.get("user") or "").split())
        if line:
            said.append(line)
    return said


def the_bot_lines(memory):
    said = []
    for turn in turns(memory):
        line = " ".join(str(turn.get("bot") or "").split())
        if line:
            said.append(line)
    return said


def last_reply(memory):
    held = the_bot_lines(memory)
    return held[-1] if held else ""


def last_module(memory):
    held = turns(memory)
    return str(held[-1].get("module") or "") if held else ""


def recent(memory, n=3):
    said = []
    for turn in turns(memory)[-n:]:
        for key in ("user", "bot"):
            part = " ".join(str(turn.get(key) or "").split())
            if part:
                said.append(part)
    return " ".join(said)


def says(memory, word):
    word = str(word or "").strip().lower()
    if not word:
        return False
    pattern = re.compile(r"\b" + re.escape(word) + r"\b", re.I)
    return any(pattern.search(line) for line in lines(memory))


def the_line(memory, pattern):
    for line in lines(memory):
        if pattern.search(line):
            return line
    return ""


def the_last_line(memory, pattern):
    for line in reversed(lines(memory)):
        if pattern.search(line):
            return line
    return ""
