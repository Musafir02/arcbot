from bot.compose import clause, fit, what_it_asks

PRIORITY = 9500


def observe(text, memory):
    if not isinstance(memory, dict):
        return
    read = memory.get("understood")
    if not isinstance(read, dict):
        return
    before = memory.get("intent_wants")
    want = what_it_asks.the_shape_it_asks(
        read, clause.shape(read, fit.wants(read, before if isinstance(before, str) else None)))
    memory["intent_wants"] = want
    if want:
        read["wants"] = want
    else:
        read.pop("wants", None)
