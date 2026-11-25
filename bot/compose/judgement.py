
from .fallback_data import JUDGE_BARE_FACES
from .fallback import JUDGE_ASK, JUDGE_ASK_BARE, _matchable, _the_plan_on_the_table


def asks_for_a_judgement(text, memory=None):
    clean = " ".join(str(text or "").lower().split())
    try:
        said = _matchable(clean).rstrip(" ?.!,")
        if JUDGE_ASK.match(said):
            return True
        bare = JUDGE_ASK_BARE.match(said)
        if not bare:
            return False
        if not (bare.group("bare_noun") or bare.group("face") in JUDGE_BARE_FACES):
            return False
        return bool(_the_plan_on_the_table(memory or {}))
    except Exception:
        return False
