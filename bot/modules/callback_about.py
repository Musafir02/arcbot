from ..memory import callback

PRIORITY = 260


ANSWERS = (
    "family-and-parenting",
    "friends-and-relationships",
    "health",
    "work",
    "school-and-study",
    "pets",
)


def respond(text, memory):
    return callback.reply_for(text, memory) or None


def CLAIMS_INSTEAD(text, memory):
    return callback.claims(text, memory)
