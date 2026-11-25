import re

from ..compose import fallback
from ..compose import a_wait_about_a_body

PRIORITY = -999

GENERIC = (
    "that sounds rough",
    "ugh, that's a lot to carry",
    "i'm sorry \u2014 that's frustrating",
    "i'm sorry - that's frustrating",
    "i'm sorry, that's frustrating",
    "sorry to hear that",
    "i'm sorry to hear that",
    "i'm listening",
    "that's a lot to carry",
)
NOTED = "noted: "
GOT_IT = ("got it \u2014 ", "got it - ", "got it, ", "got it: ")


SAID_AGAIN = "same as before: "


def is_generic(reply):
    said = str(reply or "").strip().lower().replace("\u2019", "'")
    if said.startswith(SAID_AGAIN):
        said = said[len(SAID_AGAIN):].strip()
    if not said:
        return False
    return said.startswith(NOTED) or any(said.startswith(opener) for opener in GENERIC)


def _words(line):
    said = str(line or "").lower().replace("\u2019", "'")
    said = re.sub(r"[^a-z0-9' ]+", " ", said)
    words = [w for w in said.split() if w]
    return tuple("your" if w == "my" else "our" if w == "our" else w for w in words)


def said_back(reply, text):
    said = str(reply or "").strip().lower().replace("\u2019", "'")
    for wrapper in GOT_IT + (NOTED,):
        if said.startswith(wrapper):
            said = said[len(wrapper):]
            break
    else:
        return False
    return bool(_words(said)) and _words(said) == _words(text)


def respond(text, memory):
    memory = memory if isinstance(memory, dict) else {}
    said = fallback.reply_for(text, memory)
    if not (is_generic(said) or said_back(said, text)):
        return None
    return a_wait_about_a_body.reply_for(text, memory)
