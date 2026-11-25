from ..compose import pick
from ..knowledge import lookup
from ..memory import favourite
from ..memory.taste import read_all as read_tastes

PRIORITY = 7000


def observe(text, memory):
    try:
        favourite.watch(text, memory)
    except Exception:
        return


def TAKES_AS_IT_COMES(text, memory=None):
    if not isinstance(text, str) or not isinstance(memory, dict):
        return False
    try:
        return _said_back(text, dict(memory)) is not None
    except Exception:
        return False


def respond(text, memory):
    try:
        return _said_back(text, memory)
    except Exception:
        return None


def _said_back(text, memory):
    if not isinstance(text, str) or not isinstance(memory, dict):
        return None
    told = memory.pop("favourite_told", None) if isinstance(memory, dict) else None
    changed = memory.pop("favourite_changed", None) if isinstance(memory, dict) else None
    if favourite.asks_something_too(text):
        return None
    if isinstance(changed, dict) and changed.get("thing"):
        shown = favourite.their_words(changed.get("value"))
        shown = shown[:1].upper() + shown[1:]
        if changed.get("was"):
            return pick([shown + " now, then \u2014 I have your favourite " + str(changed["thing"])
                         + " as " + favourite.their_words(changed.get("value")) + ".",
                         "Changed: your favourite " + str(changed["thing"]) + " is "
                         + favourite.their_words(changed.get("value")) + " now, not "
                         + favourite.their_words(changed.get("was")) + "."],
                        memory, text)
        return shown + " for your favourite " + str(changed["thing"]) + ", then \u2014 noted."
    if isinstance(told, dict) and told.get("thing"):
        return ("Noted: your favourite " + str(told["thing"]) + " is "
                + favourite.their_words(told.get("value")) + ".")
    if favourite.asks_all(text):
        held = favourite.the_favourites(memory)
        if held:
            last = held[-4:]
            parts = ["your favourite " + str(thing) + " is " + str(value) for thing, value in last]
            if len(parts) == 1:
                said_all = "You have told me one: " + parts[0] + "."
            else:
                said_all = "You have told me " + ", ".join(parts[:-1]) + " and " + parts[-1] + "."
            return pick([said_all,
                         said_all.replace("You have told me ", "Here is what I have: ")], memory, text)
        return None
    asked = favourite.asked(text)
    if asked and not favourite.kept(memory, asked) and read_tastes(memory):
        return None
    if asked:
        value = favourite.kept(memory, asked)
        if not value:
            memory["favourite_asked"] = asked
            return pick(["You haven't told me your favourite " + asked + " \u2014 what is it?",
                         "I don't have a favourite " + asked + " for you yet. What is it?",
                         "Your favourite " + asked + " hasn't come up yet. What is it?"],
                        memory, text)
        value = favourite.their_words(value)
        shown = value[:1].upper() + value[1:]
        return pick(["Your favourite " + asked + " is " + value + ".",
                     "You said " + value + " \u2014 that is your favourite " + asked + ".",
                     shown + ", you said. That is your favourite " + asked + "."], memory, text)
    said = favourite.read(text)
    if not said:
        return None
    if isinstance(memory, dict) and isinstance(memory.get("understood"), dict):
        try:
            if lookup.find(memory["understood"]) is not None:
                return None
        except Exception:
            pass
    value = favourite.their_words(said["value"])
    options = ["Noted: your favourite " + said["thing"] + " is " + value + ".",
               "Favourite " + said["thing"] + ": " + value + ". Got it."]
    if len(value.split()) <= 2 and not value.lower().startswith(("my ", "the ")):
        options.append(value[:1].upper() + value[1:] + " for your favourite "
                       + said["thing"] + ", then \u2014 noted.")
    return pick(options, memory, text)
