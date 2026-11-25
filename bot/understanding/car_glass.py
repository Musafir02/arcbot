import re


A_WINDOW_ON_A_CAR = re.compile(
    r"\bcar windows?\b|\bwindows? (?:on|of|in) (?:the|my|our|a) car\b", re.I)
_SOMEBODY_DID_IT = ("keyed", "keying", "smashed", "smash", "shattered", "knocked off",
                    "knocked out", "broke", "broken into", "break in", "steal", "stolen",
                    "nicked", "damaged", "vandalised", "vandalized", "reversed into", "took it",
                    "taken", "gone", "missing", "someone", "somebody", "thief", "thieves",
                    "burglary", "attempted")
_THE_GLASS_ITSELF = ("tan", "tanned", "tanning", "suntan", "sun tan", " uv", " uva", " uvb",
                    "sunlight", "sun ", "sunny", "tint", "tints", "tinted", "tinting", "tint film",
                    "clean", "cleaning", "cleaner", "wash", "washing", "dirty", "smear", "smears",
                    "smudged", "squeak", "squeaky", "mist", "misted", "misting", "misty", "steam",
                    "steamed", "steaming", "steamy", "fog", "foggy", "fogged", "condensation",
                    "demist", "demister", "defrost", "frost", "frosted", "frosty", "frozen",
                    "ice", "iced", "icing", "wiper", "wipers", "reflection", "glare", "blind spot")
_A_FAULT = _THE_GLASS_ITSELF + (
    "crack", "cracked", "cracks", "chip", "chipped", "chips", "stone chip", "star chip",
    "wont open", "wont close", "wont go", "wont wind", "wont shut", "doesnt open", "doesnt close",
    "does not open", "does not close", "stuck", "sticking", "jammed", "jam", "off its runner",
    "water", "leak", "leaks", "leaking", "letting in", "coming in", "seal", "seals", "rubber",
    "regulator", "switch", "handle", "whistle", "whistling", "noise",
    "rattles", "rattling", "squeaks", "squeaking", "repair", "repairs", "replace", "replacement",
    "how much", "cost", "price", "cheap", "cheapest", "fix")


def _names_one_of(said, parts):
    return any(" %s" % part in " %s" % said for part in parts)


def a_window_on_a_car_is_not_a_damage(understood):
    if not isinstance(understood, dict):
        return True
    said = " ".join(str(part) for part in (
        understood.get("text"), understood.get("clean"), understood.get("raw"),
        " ".join(str(word) for word in (understood.get("words") or ()))) if part).lower()
    if not said.strip() or not A_WINDOW_ON_A_CAR.search(said):
        return True
    if _names_one_of(said, _SOMEBODY_DID_IT):
        return True
    return not _names_one_of(said, _A_FAULT)
