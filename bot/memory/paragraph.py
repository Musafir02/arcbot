from . import again


A_LEAD_ALREADY = tuple(frame.split("{")[0].strip().lower()
                       for frame in again.FRAMES if frame.split("{")[0].strip())


def a_paragraph_the_chat_has_had(reply, text, memory):
    if not isinstance(reply, str) or not reply.strip():
        return reply
    try:
        if reply.lower().startswith(A_LEAD_ALREADY):
            return the_same_paragraph_again(reply, memory) or reply
        framed = again.instead(reply, text, memory) or again.already_had(reply, memory)
    except Exception:
        return reply
    if not framed:
        return reply
    return the_same_paragraph_again(framed, memory) or framed


def the_same_paragraph_again(reply, memory):
    body = again.unframed(reply)
    if not body:
        return None
    mine = again._flat(reply)
    said = 0
    for turn in memory.get("turns") or []:
        if isinstance(turn, dict) and again._flat(turn.get("bot")) == mine:
            said += 1
    if not said:
        return None
    short = again._short(body)
    if not short or again._flat(short) == again._flat(body):
        short = body
    if said >= len(again.SHORT_AGAIN):
        return again.AGAIN_HELP.format(reply=short)
    return again.SHORT_AGAIN[said - 1].format(reply=short)


def then_framed(respond):
    def a_reply_framed_as_the_repeat_it_is(text, memory):
        return a_paragraph_the_chat_has_had(respond(text, memory), text, memory)
    return a_reply_framed_as_the_repeat_it_is
