import re

GUILT = frozenset(("guilt", "guilty", "regret", "remorse", "bad"))
SHAME = frozenset(("ashamed", "shame", "shamed", "embarrassed", "humiliated"))
FEAR = frozenset(("panic", "panicking", "panicky", "anxious", "anxiety", "scared", "afraid",
                  "fear", "frightened", "terrified", "dread", "worried", "worry", "nerves",
                  "nervous", "stress", "stressed"))
ANGER = frozenset(("angry", "anger", "rage", "furious", "resentful", "resentment", "bitter",
                   "irritated", "annoyed", "cross"))
LOW = frozenset(("sad", "sadness", "low", "miserable", "down", "empty", "hopeless", "lonely",
                 "loneliness", "numb", "flat", "tearful", "upset"))
SELF = GUILT | SHAME | FEAR | ANGER | LOW

THE_ASK = re.compile(
    r"\bhow\s+(?:do|can|could|should|would)\s+i\s+(?:stop|stops|deal\s+with|cope\s+with|"
    r"get\s+rid\s+of|handle|manage|forgive|blame|get\s+over|move\s+on\s+from|let\s+go\s+of|"
    r"live\s+with|make\s+(?:it|this|that|things)\s+up|fix|change|shake|beat|calm|settle)"
    r"\b|\bhow\s+(?:do|can|could|should|would)\s+i\s+(?:stop|keep|start)\s+(?:feeling|being|"
    r"getting)\b"
    r"|\bwhat\s+(?:can|could|should|do)\s+i\s+do\s+(?:about|with|for)\b"
    r"|\bwhat\s+(?:can|could|should)\s+i\s+do\b(?!\s+(?:about\s+)?(?:a|an|the|my)\b)"
    r"|\bwhat\s+do\s+i\s+do\s+(?:now|next|about)\b"
    r"|\bwhy\s+(?:do|am|did|does|is)\s+(?:i|it)\b"
    r"|\bwhat\s+(?:is|was)\s+(?:wrong|up)\s+with\s+me\b"
    r"|\bi\s+(?:just\s+|really\s+|still\s+|keep\s+)?(?:feel|feeling)\b(?!\s+(?:like|as\s+if)\b)"
    r"|\bi\s+(?:[a-z]+\s+){0,2}feel\s+like\s+(?:a\s+|an\s+|such\s+a\s+|a\s+total\s+|"
    r"a\s+complete\s+|an\s+absolute\s+){1,2}(?:failure|mess|fraud|idiot|burden|loser|wreck|"
    r"joke|nothing)\b",
    re.I)

WRONG_WITH_ME = re.compile(
    r"\bwhat(?:'s|\s+is|\s+was)?\s+(?:wrong|up|the\s+matter|the\s+problem)\s+with\s+me\b", re.I)

ASK_WORDS = frozenset("""
how do does did can could should would i me my mine myself im i'm am is was are be been being
what why when now next about with for of to in on at this that these those it its it's
feel feels feeling felt like as if so very really just still always never ever much more most
some any the a an and but or then there here wrong up matter problem
stop stops stopped deal cope get rid handle manage forgive get over move on from let go live
make made fix change shake beat calm settle keep start being getting bad worse better again
way ways blame blaming forgive forgiving less more
anymore today lately always sometimes ok okay well please help tell know thing things something
anything nothing lot bit
failure mess fraud idiot burden loser wreck joke useless worthless stupid pathetic hopeless
""".split()) | SELF


ABOUT_WORDS = frozenset(("about", "over", "regarding", "concerning", "around", "because"))

APPRAISAL = frozenset(("failure", "mess", "fraud", "idiot", "burden", "loser", "wreck", "joke",
                       "useless", "worthless", "stupid", "pathetic", "hopeless"))


def _words(clean):
    return [w for w in re.split(r"[^a-z']+", str(clean or "").lower()) if w]


def _named_thing(clean):
    feeling_seen = False
    for word in _words(clean):
        if word.endswith("'s"):
            word = word[:-2]
        if word in SELF or word in APPRAISAL:
            feeling_seen = True
            continue
        if feeling_seen and word in ABOUT_WORDS:
            return None
        if word in ASK_WORDS:
            continue
        if len(word) < 3 and word not in ("me", "my", "im"):
            continue
        return word
    return None


GUILT_LINES = (
    "There is no fact I can look up here - nobody can tell you whether you ought to feel guilty, "
    "and the feeling itself is a poor guide. What helps is smaller and more concrete: the one "
    "thing you would have done differently, and whether any part of it can still be said or put "
    "right. What was it?",
    "Guilt is about something you did, and it usually lifts when the thing is dealt with rather "
    "than when you argue with it. I can't tell you whether you should still feel it - nobody can "
    "check that - but I can help you find the part that is still open. What happened?",
    "I can't settle whether you deserve to feel bad about it, and a search would only find "
    "somebody else's opinion. The useful question is what you would want to have done instead, "
    "and whether that is still possible in some smaller form. What would it be?",
)
SHAME_LINES = (
    "Shame is heavier than guilt - guilt is about a thing you did, shame is about who you are - "
    "and there is nothing to look up that settles it. What shrinks it is being said out loud to "
    "one person who won't flinch, which is the step most people are given. Is there anyone you "
    "could say it to?",
    "Nothing on a screen will make this better, and I would be making it up if I said otherwise. "
    "The thing that helps with shame is specific and hard: telling one person, in your own words, "
    "and letting them still be there afterwards. Who could that be?",
)
FEAR_LINES = (
    "I can't tell you why it comes for you - that needs somebody who can ask you questions. What "
    "does help while it is happening is the oldest trick there is: breathe out longer than you "
    "breathe in, and stay where you are until it passes, because it does pass. Do you know what "
    "sets it off?",
    "There's nothing to search that will tell you why this is happening to you, and anyone who "
    "says they can do it from a webpage is guessing. Two things worth having: while it is "
    "happening, slow the out-breath and don't fight it; if it keeps coming back, tell your GP, "
    "because that is a conversation worth having. How often is it happening?",
    "I can't check what is going on inside you, so I won't pretend to. What I can say is the "
    "usual first step for this: keep it small while it is happening - long breaths out, feet on "
    "the floor, one thing at a time - and then write down what came just before it, because the "
    "pattern is usually the useful part. What came before the last one?",
)
ANGER_LINES = (
    "Anger usually has something underneath it - hurt, or a line that someone crossed - and there "
    "is no fact I can look up that gets to it. The question worth asking is what it is protecting. "
    "What happened just before you felt it?",
    "I can't tell you whether you are right to be this angry; that depends on things only you "
    "know. What I can say is that anger is usually the second feeling, and the first one is what "
    "to look for. What was it that got to you?",
)
LOW_LINES = (
    "I can't tell from out here why you feel like this, and nothing I could look up would know "
    "either. What usually helps is naming the part that is heaviest and when it started - a GP or "
    "a friend would ask the same first question. When did it start?",
    "There's no fact to find on this one, and I'd be guessing if I gave you a reason. The part "
    "worth having is small and concrete: what has changed lately - sleep, work, somebody, your "
    "health - because a low patch usually has one of those behind it. Which of them is nearest?",
    "Why you feel like this isn't something anyone can check from outside, me least of all. But "
    "it is worth saying out loud: if it has been like this for more than a couple of weeks, that "
    "is the point where a GP is the right person rather than a website. How long has it been?",
)
WHAT_IS_WRONG_LINES = (
    "Nothing about you is a fact I can look up, and 'what's wrong with me' is usually a question "
    "about one part of your life rather than all of you. Which part is it?",
    "I can't tell you that, and I'd be inventing something if I tried. What I can do is take it "
    "apart with you - there is usually one thing that is actually wrong, and it is smaller and "
    "more fixable than the question makes it sound. Where would you start?",
)

POOLS = (
    (GUILT, GUILT_LINES),
    (SHAME, SHAME_LINES),
    (FEAR, FEAR_LINES),
    (ANGER, ANGER_LINES),
    (LOW, LOW_LINES),
)


def _family(clean):
    words = set(_words(clean))
    if WRONG_WITH_ME.search(str(clean or "")):
        return WHAT_IS_WRONG_LINES
    for feelings, lines in POOLS:
        if words & feelings:
            return lines
    if re.search(r"\b(?:forgive|blame)\s+(?:myself|me)\b", str(clean or ""), re.I):
        return GUILT_LINES
    if words & APPRAISAL:
        return SHAME_LINES
    if words & {"feel", "feels", "feeling", "felt"}:
        return LOW_LINES
    return None


def answer(clean, memory=None):
    text = str(clean or "").strip()
    if not text:
        return None
    if not (THE_ASK.search(text) or WRONG_WITH_ME.search(text)):
        return None
    if _named_thing(text):
        return None
    lines = _family(text)
    if not lines:
        return None
    import random
    return random.choice(lines)
