import copy
import random
import re

from . import fallback

NOTHING_SAID = re.compile(
    r"\b(?:i'?m listening|say more|not sure about that one|don'?t know enough|"
    r"beyond what i know|rather not guess|everything i have on that one|"
    r"not much (?:i can add|to go on)|which bit do you|tell me more|"
    r"i'?m here if you want|anything you'?d like a hand with|thanks for telling me)\b"
    r"|\u2014\s*noted\.|\s-\s*noted\."
    r"|^noted[:.]|,\s*good to know\.?\s*$", re.I)

OUT_OF_THEIR_HANDS = re.compile(r"out of your hands|when do you find out", re.I)

MISREAD_AS_GOOD_NEWS = re.compile(
    r"\b(?:good to hear|glad to hear|best bit|nice one|sounds alright|sounds good|"
    r"lovely|how lovely|brilliant)\b", re.I)


def what_the_composer_would_say(text, memory):
    probe = copy.deepcopy(memory)
    state = random.getstate()
    try:
        return fallback.reply_for(text, probe, verdict=False) or ""
    except Exception:
        return ""
    finally:
        random.setstate(state)


def only_a_shrug(text, memory, misreads=None):
    said = what_the_composer_would_say(text, memory)
    if not said:
        return True
    if NOTHING_SAID.search(said) or OUT_OF_THEIR_HANDS.search(said):
        return True
    if misreads is not None and misreads.search(said):
        return True
    return False
