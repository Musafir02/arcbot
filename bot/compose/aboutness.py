import re

FRAME = frozenset("""
about after again all also and any anything are around because been before being both but can
could did does doing done down each even ever every for from get gets getting give given go goes
going gone got had has have having here him his her how into its just keep kept know knew like
long made make many may might more most much must need needed not now off once one only other our
out over own said same say says she should since some something still such take taken tell than
that thats the their them then there these they thing things think this those through time times
today told tomorrow tonight too took under until very want wanted was way well went were what
when where which while who whom why will with wont would yeah yes yet you your yours yourself
im ive ill id youre dont doesnt didnt cant couldnt wont isnt arent wasnt werent havent hasnt
hello hi hey thanks thank please sorry ok okay right sure fine good nice bad lot bit put puts
knows mean means meant seem seems felt feel feels look looks looking sound sounds
really stopping
anyway anyways btw honestly seriously basically literally actually whatever
""".split())

HEDGE = re.compile(r"beyond what i know|i don't know enough|not sure about that one|a search should",
                   re.I)
STEM = 5
RESTATEMENT = 0.6

_WORDS = re.compile(r"[a-z0-9']+")


CHANGES_THE_SUBJECT = re.compile(
    r"\b(?:anyway|anyways|any\s+way|back\s+to|on\s+a\s+different\s+note|"
    r"on\s+another\s+note|changing\s+the\s+subject|change\s+of\s+subject|changing\s+tack|"
    r"while\s+i'?m\s+here|unrelated\s+but|that\s+aside|moving\s+on|by\s+the\s+way|btw|"
    r"different\s+question|other\s+thing)\b", re.I)


def after_a_change_of_subject(text):
    line = str(text or "")
    tail = ""
    for found in CHANGES_THE_SUBJECT.finditer(line):
        tail = line[found.end():]
    tail = tail.strip(" \t,.;:!-\u2014-")
    if len(tail.split()) < 2:
        return ""
    return tail


def subject_words(text):
    return {word for word in _WORDS.findall(str(text or "").lower())
            if len(word) >= 4 and word not in FRAME}


def names_the_subject(reply, about):
    said = _WORDS.findall(str(reply or "").lower())
    found = set()
    for word in about:
        for other in said:
            if len(other) >= 4 and other[:STEM] == word[:STEM]:
                found.add(word)
                break
    return found


def restates_the_line(reply, text):
    said = set(_WORDS.findall(str(reply or "").lower()))
    mine = set(_WORDS.findall(str(text or "").lower()))
    return bool(mine) and len(said & mine) / len(mine) >= RESTATEMENT


def is_a_hedge(reply):
    return bool(HEDGE.search(str(reply or "")))


def unlike_the_line(reply, text):
    about = subject_words(text)
    if not about:
        return about, set()
    if restates_the_line(reply, text) or is_a_hedge(reply):
        return about, set()
    return about, names_the_subject(reply, about)


def the_better_answer(reply, candidates, text, skip=None, need=2):
    about, said = unlike_the_line(reply, text)
    if not about or said:
        return None
    best = None
    best_named = need - 1
    for index, candidate in enumerate(candidates or ()):
        if index == skip:
            continue
        other = str(candidate.get("reply") or "")
        if int(candidate.get("priority") or 0) < 0:
            continue
        if restates_the_line(other, text) or is_a_hedge(other):
            continue
        count = len(names_the_subject(other, about))
        if count > best_named:
            best, best_named = index, count
    return best
