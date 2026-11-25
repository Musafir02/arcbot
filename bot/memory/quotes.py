

import re


def left_open(said):
    said = str(said or "")
    if said.count('"') % 2:
        return True
    return said.count("\u201c") > said.count("\u201d")


def closed(said, rest, whole=""):
    said = str(said or "").strip()
    if not left_open(said):
        return said
    for part in rest:
        said = (said + " " + str(part or "").strip()).strip()
        if not left_open(said):
            return said
    return str(whole or said).strip()


NAME_END = re.compile(r"\b(?:no|nos|vol|vols|ch|pt|pp|fig|e\.g|i\.e|etc|vs|dr|mr|mrs|ms|prof|st|"
                      r"al|inc|ltd|co|dept|tel|ref)\.$", re.I)
OPENS_ON_A_FIGURE = re.compile(r"^[\d*\u00a3$\u20ac]")


def a_name(text, start, end):
    before = str(text[start:end]).strip()
    if not before.endswith("."):
        return False
    if not NAME_END.search(before):
        return False
    after = str(text[end:]).lstrip()
    return bool(OPENS_ON_A_FIGURE.match(after))


def sentences(text, splitter):
    text = str(text or "")
    if not hasattr(splitter, "finditer"):
        return [part.strip() for part in splitter.split(text) if str(part).strip()]
    parts, start = [], 0
    for end in splitter.finditer(text):
        if a_name(text, start, end.start()):
            continue
        parts.append(text[start:end.start()].strip())
        start = end.end()
    parts.append(text[start:].strip())
    parts = [part for part in parts if part]
    out = []
    for part in parts:
        if out and left_open(out[-1]):
            out[-1] = (out[-1] + " " + part).strip()
        else:
            out.append(part)
    return out
