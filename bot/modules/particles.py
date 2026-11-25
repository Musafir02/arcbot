import re

A_PARTICLE = frozenset("up down in out off over away along through round back".split())

A_VERB_TAIL = frozenset("""
taken took taking put putting let letting thrown threw given gave done doing made making
fixed fixing mended mending altered altering hemmed hemming patched darned
repaired repairing cleaned cleaning washed washing cut cutting painted painting
cleared clearing tidied tidying mowed mowing serviced servicing trimmed pruning
swept hoovered vacuumed dusted walked boarded shortened lengthened
""".split())


def a_thing_without_its_tail(said):
    words = str(said or "").split()
    while len(words) > 1 and words[-1].lower().strip(".,!?") in (A_PARTICLE | A_VERB_TAIL):
        words.pop()
    return " ".join(words)


def a_job_word(word):
    return str(word or "").lower().strip(" .,!?;:'\"()") in (A_VERB_TAIL | A_PARTICLE)
