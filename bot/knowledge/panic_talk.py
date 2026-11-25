
from .lookup import NOT_A_NOSE, entry

ANSWERS = ("health",)

SOMEONE_ELSE = (
    "Stay with them and say it will pass, because it does: an attack peaks in about ten "
    "minutes. Sit them down, loosen anything tight at the neck, and breathe out loud with them "
    "- out for longer than in, so they have something to follow rather than an instruction. Do "
    "not argue with what they are frightened of and do not leave them alone to fetch anything. "
    "If they have never had one before, or there is chest pain with it, get medical advice "
    "rather than assuming it is panic.")

BEHIND_YOU = (
    "Then it is behind you, and getting through one is the thing to be pleased about rather "
    "than something to keep watch on. If one starts again, the out-breath is what helps - out "
    "for longer than in - and leaving the place it started rather than fighting it. If they "
    "come back often enough to shape your week, ask your GP about CBT: it is the treatment with "
    "the best evidence for panic.")

_ATTACK = ("panic attack", "panic attacks", "panicking", "panicky", "panics", "panicked",
           "cant breathe", "heart racing", "hyperventilating")

_ANXIETY = ("anxiety attack", "anxiety attacks")

_THEM = ("my mum", "my mom", "my dad", "my sister", "my brother", "my son", "my daughter",
         "my friend", "my mate", "my husband", "my wife", "my partner", "my boyfriend",
         "my girlfriend", "my colleague", "my boss", "my nan", "my nana", "my grandma",
         "my grandad", "my neighbour", "he is", "she is", "hes having", "shes having",
         "theyre having", "they are having", "someone", "somebody", "him", "her",
         "he had", "she had", "they had")

_BEHIND = ("last year", "last month", "last week", "last summer", "yesterday", "last night",
           "years ago", "a year ago", "months ago", "weeks ago", "ages ago", "a while ago",
           "in the past", "when i was", "used to", "have had", "had one before", "had a few",
           "had a panic", "has had", "was having", "kept having", "got them", "get them")

_MINE = ("im having a panic", "i am having a panic", "i think im having", "im panicking",
         "i am panicking", "ive been having panic", "im about to have a panic",
         "my panic attack")

_WORRY_ABOUT = ("about the", "about this", "about that", "about her", "about his",
                "about their", "about work", "about money", "about exams", "about tomorrow")

_THEIR_OWN_PAST = ("he had", "she had", "they had", "he has", "she has", "they have",
                   "he gets", "she gets")

_BEHIND_THEM = ("years ago", "last year", "last month", "last week", "last summer",
                "in the past", "when i was", "when he was", "when she was", "used to",
                "months ago", "weeks ago", "a while ago")

_DIAGNOSIS = ("or is he just", "or is she just", "or is it just", "or is that just",
              "or am i just", "or just shy", "just shy", "or attention")

_PATTERN = ("when he has to", "when she has to", "when they have to", "when i have to",
            "whenever", "every time", "each time")

_ATTACK_NAMES = ("panic attacks", "anxiety attacks", "panics")
_HABIT_VERBS = tuple(f"{verb} {name}" for name in _ATTACK_NAMES
                     for verb in ("has", "have", "gets", "get", "had", "having"))
_HABIT_MARKERS = ("panics", "panicked", "every day", "every week", "every few days", "usually",
                  "tends to", "at school", "before exams", "on the tube", "at work",
                  "in meetings", "a lot")
_HABIT_ONCE = (" had ", " panicked", " was having", " kept having", " last ", " on the way")
_HABIT = _HABIT_VERBS + _HABIT_MARKERS
_ADVICE_ASK = ("what can i do", "what do i do", "what should i do", "how do i help",
               "how can i help", "how do i calm", "how do i talk", "what can i say",
               "how do i support", "what helps", "any advice", "what can we do")


LIVING_WITH = (
    "Ask them, on a calm day, what helps when one starts - most people know, and being asked is "
    "worth more than being managed. What helps most between attacks is not avoiding the places "
    "they happen: the list of avoided things grows, and the fear with it. Panic disorder is "
    "treatable, so it is worth a GP conversation: CBT has the best evidence, and an SSRI helps "
    "some people alongside it. If the attacks are getting more frequent, or they start avoiding "
    "work, shops or travel, say so to the GP rather than waiting. And if one ever comes with "
    "chest pain, or it is their first, get it checked rather than assuming panic.")


def _a_flat_habit(understood):
    return not _a_habit_is_not_a_minute(understood)


def _the_attack_is_the_speakers_own(understood):
    low = " " + _text(understood) + " "
    if any((" " + mine + " ") in low for mine in _MINE):
        return True
    if any((" " + own + " ") in low for own in
           ("i had", "ive had", "i have had", "i get", "i used to", "i was having")):
        return True
    if any((" " + back + " ") in low for back in _BEHIND_THEM):
        return True
    return not any((" " + them + " ") in low for them in _THEM + _THEIR_OWN_PAST)


def _the_line_asks_what_to_do(understood):
    low = " " + _text(understood) + " "
    return any((" " + phrase + " ") in low or low.strip().startswith(phrase)
               for phrase in _ADVICE_ASK)


def _a_habit_is_not_a_minute(understood):
    low = " " + _text(understood) + " "
    habit = any((" " + phrase + " ") in low for phrase in _HABIT_VERBS)
    if not habit:
        once = any(phrase in low for phrase in _HABIT_ONCE)
        habit = (not once) and any((" " + phrase + " ") in low for phrase in _HABIT_MARKERS)
    return (not habit) or _the_line_asks_what_to_do(understood)


def _text(understood):
    words = understood.get("words") if isinstance(understood, dict) else None
    if isinstance(words, (list, tuple)) and words:
        return " ".join(str(word) for word in words).lower()
    return str((understood or {}).get("clean") or "").lower()


ENTRIES = [
    entry("panic-someone-else", (_ATTACK, _THEM), SOMEONE_ELSE, bias=2,
          avoid=_MINE + _DIAGNOSIS + _PATTERN + _WORRY_ABOUT + _BEHIND_THEM + NOT_A_NOSE,
          guard=_a_habit_is_not_a_minute),
    entry("panic-attack-in-the-past", (_ATTACK, _BEHIND), BEHIND_YOU, bias=2,
          avoid=("im having a panic", "i am having a panic", "right now"),
          guard=_the_attack_is_the_speakers_own),
    entry("panic-someone-else-habit", (_ATTACK + _ANXIETY, _THEM), LIVING_WITH, bias=1,
          avoid=_MINE + _DIAGNOSIS + _PATTERN + _WORRY_ABOUT + _BEHIND_THEM + NOT_A_NOSE,
          guard=_a_flat_habit),
]
