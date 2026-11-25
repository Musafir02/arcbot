import re

from .fallback import A_CHILD_DIED, A_DEATH_IN_THE_LINE, A_SUICIDE_IN_THE_LINE

TELL_ASK = re.compile(
    r"\b(?:how|what)\s+(?:do|should|can|would|will)\s+(?:i|we)\s+"
    r"(?:tell|say|word|phrase|put it|put)\b"
    r"|\bhow do i put (?:it|this)\b|\bwhat do i tell\b")
A_CHILD_IN_THE_ASK = re.compile(
    r"\b(?:kid|kids|child|children|son|daughter|boy|boys|girl|girls|toddler|little one|"
    r"teenager|teen|baby|niece|nephew|grandson|granddaughter|"
    r"(?:two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|\d{1,2})[- ]"
    r"(?:year|yr)s?[- ]old)\b")
TAIL_FILLER = frozenset("""please now then too ok okay soon gently first properly exactly tonight
today tomorrow at bedtime the a an this that it and but so just really here you i we my""".split())
TAIL_ABOUT_THE_ONE_WHO_DIED = frozenset("""about his her their them of on with dad daddy mum mummy
mom mommy mother father gran granny grandma grandad grandpa nana nan brother sister uncle aunt dog
cat pet name what happened truth""".split())
_A_PERSON_IN_THE_TAIL = re.compile(
    r"\b(?:dad|daddy|mum|mummy|mom|mommy|mother|father|gran|granny|grandma|grandad|grandpa|nana|"
    r"nan|brother|sister|uncle|aunt|dog|cat|pet)\b")
A_DEATH_IN_THE_TAIL = re.compile(
    r"\b(?:died|dead|dying|dies|death|passed|passing|gone|killed|funeral|buried|cremated)\b")


def _the_tail_after_the_child(text):
    last = None
    for match in A_CHILD_IN_THE_ASK.finditer(text):
        last = match
    if last is None:
        return None
    return text[last.end():]


def _the_tail_is_about_the_death(tail):
    words = re.findall(r"[a-z']+", tail or "")
    if not words:
        return True
    if A_DEATH_IN_THE_TAIL.search(tail):
        return not _A_PERSON_IN_THE_TAIL.search(tail)
    for word in words:
        if word in TAIL_FILLER or word in TAIL_ABOUT_THE_ONE_WHO_DIED:
            continue
        return False
    return True

THE_WORDS_FOR_A_CHILD = (
    "Keep it to a sentence or two, with their name and the plain word: they died, and they are "
    "not coming back. Then answer whatever the child asks, in the same words, and if they ask "
    "again next week - they will - say the same thing again.",
    "Say it plainly and soon: their name, and that they died. Not asleep, not gone away, and not "
    "\"lost\" - a child takes those words literally, and then waits for them to wake up. What "
    "follows can come from their questions.",
    "The words are the ones you would use to an adult, just shorter: their name, that they died, "
    "and that they will not be coming back. It is all right for the child to see you cry - that "
    "is how they learn it is all right to be sad.",
)


def a_death_in_the_thread(memory, look_back=3):
    turns = [t for t in (memory.get("turns") or []) if isinstance(t, dict)]
    for turn in turns[-look_back:]:
        said = " ".join(str(turn.get("user") or "").lower().split())
        if said and A_DEATH_IN_THE_LINE.search(said):
            return True
    return False


def asks_the_words_for_a_child(clean, memory):
    text = " ".join(str(clean or "").lower().split())
    if not text:
        return False
    if not (TELL_ASK.search(text) and A_CHILD_IN_THE_ASK.search(text)):
        return False
    try:
        if not a_death_in_the_thread(memory):
            return False
        thread = _the_last_few_lines(memory)
    except Exception:
        return False
    if A_SUICIDE_IN_THE_LINE.search(thread) or A_SUICIDE_IN_THE_LINE.search(text):
        return False
    if A_CHILD_DIED.search(text):
        return False
    tail = _the_tail_after_the_child(text)
    if tail is None or not _the_tail_is_about_the_death(tail):
        return False
    return True


def _the_last_few_lines(memory, look_back=4):
    turns = [t for t in (memory.get("turns") or []) if isinstance(t, dict)]
    lines = []
    for turn in turns[-look_back:]:
        lines.append(str(turn.get("user") or ""))
        lines.append(str(turn.get("bot") or ""))
    return " ".join(lines).lower()
