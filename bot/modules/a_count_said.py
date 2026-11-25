
from ..memory import amounts

PRIORITY = 7000


def observe(text, memory):
    return None


def respond(text, memory):
    if not isinstance(text, str):
        return None
    said = amounts.a_count_they_report(text)
    if said is None:
        return None
    turns = memory.get("turns") if isinstance(memory, dict) else None
    last = turns[-1].get("bot") if isinstance(turns, list) and turns else ""
    against = amounts.against_the_last_answer(said, last or "")
    if against is None:
        return None
    return amounts.the_comparison(against)
