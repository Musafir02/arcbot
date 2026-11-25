from ..compose import fallback, habit
from ..memory import ack

PRIORITY = -999


def respond(text, memory):
    raised = habit.answer_for(text, memory)
    if not raised:
        return None
    said = fallback.reply_for(text, memory)
    if not said:
        return None
    if not (fallback._is_a_hedge(said)
            or fallback._in_a_pool(said, (fallback.NEUTRAL,))
            or ack.reads_as_a_receipt(said)):
        return None
    return raised
