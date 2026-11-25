
import re

from . import facts

SENTENCE = re.compile(r"(?:(?:\d\.\d)|[^.!?])+[.!?]?")
OPENS = re.compile(r"^(?:if|when|unless|in case)\s+", re.I)
CONDITION_WORD = re.compile(r"\b(?:if|when|unless|in case)\b", re.I)
BREAK = re.compile(r"\s*(?:,|;|:|\u2014|\s-\s|\band then\b|\bthen\b)", re.I)
EMPTY = frozenset("""a an the i im you your youre we us our it its that this there
here to of in on at for with and or but if then so as is are was were be been am do does did
have has had got get all just really very too not no now some any my me him her his hers them
they their what which who whom whose how why when where""".split())
MOST_LETTERS = 90
MOST_CASE = 60
RUNS_ON = re.compile(r"\b(?:get|ring|call|take|keep|see|use|put|leave|buy|stop|go|try|"
                     r"check|ask|tell|give|make|book|contact|wash|clean|apply|move|add|"
                     r"rest|ice|eat|drink)\b", re.I)


PLACE = frozenset("""out outside away outdoors home house indoors inside office in""".split())


def _places(words):
    return {word for word in words if word in PLACE}


def _words(text):
    return re.findall(r"[a-z]+", str(text or "").lower().replace("\u2019", "'"))


def _pairs(words):
    return {first + " " + second for first, second in zip(words, words[1:])
            if first not in EMPTY or second not in EMPTY}


PERSON = frozenset(facts.RELATIONS) | frozenset("""neighbour neighbor friend boss manager
colleague coworker roommate flatmate housemate landlord partner kids kid child children baby
toddler twins sister brother son daughter""".split())
MY_PERSON = re.compile(r"\b(?:my|our)\s+([a-z]+)")
A_PERSON_IN_IT = frozenset(PERSON) | frozenset("""someone anyone somebody anybody child children
    baby toddler guest visitor family relatives""".split())
A_PLAN = re.compile(r"\b(?:i|we)(?:m|re| am| are)?\s+(?:want|wanna|need|plan|intend|have to|"
                    r"must|should|will|would like|am going|are going|going to|think i|ll|will)\b",
                    re.I)


def about_someone_else(text):
    low = str(text or "").strip().lower().replace("\u2019", "'")
    return any(word.rstrip("'s") in PERSON for word in MY_PERSON.findall(low))


def _sentences(said):
    return [part.strip() for part in SENTENCE.findall(str(said or "")) if part.strip()]


def _one_move(consequence):
    text = str(consequence or "").strip(" ,;:-\u2014.")
    kept = text
    if len(text) > MOST_LETTERS:
        kept = ""
        for piece in re.split(r",\s+|\s+-\s+|\s+\u2014\s+", text):
            trial = (kept + ", " + piece) if kept else piece
            if len(trial) > MOST_LETTERS and kept:
                break
            kept = trial
    kept = kept.strip(" ,;:-\u2014")
    kept = re.sub(r"(?:[\s,;:]+)(?:and|but|or|so|then|with|plus)$", "", kept, flags=re.I)
    return kept.strip(" ,;:-\u2014")


def conditions(said):
    found = []
    for sentence in _sentences(said):
        for opening in CONDITION_WORD.finditer(sentence):
            before = sentence[:opening.start()].strip(" ,;:-\u2014")
            if CONDITION_WORD.search(before):
                continue
            rest = sentence[opening.end():].strip()
            rest = OPENS.sub("", rest).strip()
            cut = BREAK.search(rest)
            if cut is None and before and RUNS_ON.search(rest):
                continue
            if cut is None and not before:
                opening_at = re.search(r"\s+(?=(?:a|an|the)\s)", rest)
                if opening_at:
                    cut = opening_at
            if before and re.search(r"[:;]", before):
                continue
            case = (rest[:cut.start()] if cut else rest).strip(" ,;:-\u2014.")
            after = rest[cut.start():] if cut else ""
            after = re.sub(r"^\s*(?:,|;|:|\u2014|\s-\s|\band\b|\bthen\b)\s*", "", after, flags=re.I)
            consequence = before if len(_words(before)) >= 2 else after.strip(" ,;:-\u2014.")
            if not case or not consequence:
                continue
            if len(case) > MOST_CASE:
                continue
            consequence = _one_move(consequence)
            if not consequence:
                continue
            found.append((case, consequence))
    return found


UNITS = frozenset("""year month week day hour minute mile km kilo stone pound percent""".split())
NUMBERS = {word: value for value, word in enumerate(
    "zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen "
    "fifteen sixteen seventeen eighteen nineteen twenty thirty forty fifty sixty seventy eighty "
    "ninety hundred".split())}
BELOW = ("under", "below", "less than", "fewer than", "up to", "at most", "no more than",
         "within", "younger than", "shorter than")
ABOVE = ("over", "above", "more than", "past", "older than", "longer than", "beyond",
         "at least", "from", "at")
MOST_WORDS_BEFORE = 3


def _number(word):
    word = str(word or "").strip(".,")
    if word.isdigit():
        return float(word)
    return float(NUMBERS[word]) if word in NUMBERS else None


def _measures(text):
    found = {}
    words = re.findall(r"[a-z0-9.]+", str(text or "").lower())
    for index, word in enumerate(words):
        unit = word.rstrip("s")
        if unit not in UNITS or not index:
            continue
        value = _number(words[index - 1])
        if value is None and index > 1 and words[index - 1] in ("a", "an"):
            value = 1.0
        if value is not None:
            found.setdefault(unit, value)
    return found


def _tests(case):
    found = []
    words = re.findall(r"[a-z0-9.]+", str(case or "").lower())
    for index, word in enumerate(words):
        unit = word.rstrip("s")
        value = _number(words[index - 1]) if index else None
        if unit not in UNITS or value is None:
            continue
        around = " ".join(words[max(0, index - 1 - MOST_WORDS_BEFORE):index - 1])
        side = ("below" if any(lead in around for lead in BELOW) else
                "above" if any(lead in around for lead in ABOVE) else "")
        if side:
            found.append((unit, value, side))
    return found


def _meets(case, text):
    mine = _measures(text)
    judged = False
    for unit, value, side in _tests(case):
        if unit not in mine:
            continue
        judged = True
        theirs = mine[unit]
        if side == "below" and not theirs < value:
            return False
        if side == "above" and not theirs > value:
            return False
    return True if judged else None


def chosen(text, said):
    for case, consequence in _candidates(text, said):
        if _meets(case, text) is False:
            continue
        return consequence
    return None


def refused(text, said):
    return any(_meets(case, text) is False for case, _ in _candidates(text, said))


def _carried(case_words, words):
    want = {w for w in case_words if w not in EMPTY}
    if not want:
        return False
    met = want & set(words)
    if not met:
        return False
    return len(met) == len(want) or (len(want) >= 3 and len(met) * 2 >= len(want))


def _about_a_person(case_words):
    return any(w.rstrip("'s") in A_PERSON_IN_IT for w in case_words)


def _candidates(text, said):
    if A_PLAN.search(str(text or "")):
        return []
    words = _words(text)
    if not words or len(words) > 8:
        return []
    mine = _pairs(words)
    found = []
    for case, consequence in conditions(said):
        case_words = _words(case)
        halves = [_words(one) for one in
                  re.split(r"\bor\b|\bwhen\b", case, flags=re.I) if one.strip()]
        hit = False
        for half in halves:
            if not (mine & _pairs(half) or _carried(half, words)):
                continue
            theirs, ours = _places(half), _places(words)
            if theirs and ours and not (theirs & ours):
                continue
            hit = True
            break
        if not hit:
            continue
        if about_someone_else(text) and not _about_a_person(case_words):
            continue
        found.append((case, consequence))
    return found
