
from ..memory import earlier
from ..memory import lineback
from ..memory.store_lines import ANSWERS

PRIORITY = 7050


def observe(text, memory):
    return None


def _the_store_would_say(text, memory):
    from . import memory_store
    try:
        return memory_store.respond(text, memory)
    except Exception:
        return None


def _nothing_to_give(reply):
    from ..compose import fallback
    from ..compose import fit
    try:
        return bool(fallback.is_a_hedge(reply) or fit.is_a_punt(reply))
    except Exception:
        return False


def _someone_answers_it(text, memory):
    from . import answers
    try:
        said = answers.respond(text, memory)
    except Exception:
        return False
    return bool(isinstance(said, str) and said.strip())


def _another_module_gives_the_value(text, memory):
    try:
        from . import attribute_said_again
        said = attribute_said_again.respond(text, memory)
    except Exception:
        return False
    if not (isinstance(said, str) and said.strip()):
        return False
    return bool(earlier.gives_the_named_value(text, memory, said))


def _said_back_already(text, memory):
    try:
        return bool(lineback.reply_for(text, memory))
    except Exception:
        return False


def TAKES_AS_IT_COMES(text, memory):
    if not isinstance(text, str) or not isinstance(memory, dict):
        return False
    if not earlier.RECALL.search(" ".join(text.lower().split())):
        return False
    theirs = _the_store_would_say(text, memory)
    if not (isinstance(theirs, str) and theirs.strip()):
        return False
    put = earlier.put_right(theirs, memory) or earlier.a_misquoted_line(theirs, memory, text)
    if put and put != theirs:
        return True
    return earlier.another_line_was_asked_for(text, memory, theirs)


def respond(text, memory):
    if not isinstance(text, str) or not isinstance(memory, dict):
        return None
    theirs = _the_store_would_say(text, memory)
    if isinstance(theirs, str) and theirs.strip():
        put = earlier.put_right(theirs, memory) or earlier.a_misquoted_line(theirs, memory, text)
        if put:
            return put
        if earlier.another_line_was_asked_for(text, memory, theirs) and not _another_module_gives_the_value(text, memory):
            pass
        elif not _nothing_to_give(theirs):
            return None
    if _said_back_already(text, memory):
        return None
    if not earlier.their_own_words(text) and _someone_answers_it(text, memory):
        return None
    return earlier.answer_for(text, memory) or earlier.from_the_line(text, memory)
