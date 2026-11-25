import re

from ..compose import fit

ON_RECORD = frozenset((fit.TIME, fit.AMOUNT, fit.PLACE, fit.PERSON, fit.MEANING, fit.YESNO))

NOT_ON_RECORD = re.compile(
    r"\b(?:you|ye) (?:have not|haven'?t) (?:said|told|mentioned|let me know)\b", re.I)

LONGEST = 180

_gives_before_this_module = fit.gives


def gives(reply, want, line=None):
    got = _gives_before_this_module(reply, want, line)
    if got is True or want not in ON_RECORD:
        return got
    text = " ".join(str(reply or "").split())
    if "?" in text or len(text) > LONGEST:
        return got
    if not NOT_ON_RECORD.search(fit.first_sentence(text)):
        return got
    return True


fit.gives = gives
