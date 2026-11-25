from ..memory import doubt

PRIORITY = 400

SUBJECT_UNCLEAR = (
    "I'm not sure which {word} you mean - a word or two about it and I'll answer the right one.",
    "Which {word} do you mean? Tell me a bit more and I'll take it from there.",
    "There's more than one thing '{word}' could mean. What's the one you're asking about?",
)


def _the_question(text, word):
    at = sum(ord(letter) for letter in (text or "")) % len(SUBJECT_UNCLEAR)
    return SUBJECT_UNCLEAR[at].format(word=word)


def respond(text, memory):
    understood = memory.get("understood") if isinstance(memory, dict) else None
    if isinstance(understood, dict) and understood.get("subject_unclear"):
        return _the_question(text, understood["subject_unclear"])
    return doubt.reply_for(text, memory)
