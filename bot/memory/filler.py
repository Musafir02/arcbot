
TAIL_OFF = frozenset("""tho though lol lmao haha ha hehe tbh ngl imo idk innit x xx xxx
    actually btw""".split())

TAIL_PHRASES = ("by the way", "out of interest", "while im at it", "whilst im at it",
                "as it happens", "if thats ok", "if that's ok", "if you dont mind",
                "if you don't mind", "come to think of it", "now i think of it",
                "now that i think of it")

IN_THE_WAY = frozenset("actually really honestly literally genuinely basically".split())


def without_filler(said):
    words = str(said or "").split()
    while len(words) > 1 and words[-1].lower().strip(".,;:!?") in TAIL_OFF:
        words.pop()
    text = " ".join(words)
    changed = True
    while changed and text:
        changed = False
        stripped = text.rstrip(" .,;:!?")
        low = stripped.lower()
        for phrase in TAIL_PHRASES:
            if low.endswith(" " + phrase) or low == phrase:
                cut = stripped[:len(stripped) - len(phrase)].rstrip(" ,;:-")
                if cut:
                    text = " ".join(cut.split())
                    changed = True
                break
    return text


ASK_TAIL = ("by the way", "btw", "out of interest", "while im at it", "whilst im at it",
            "as it happens", "if thats ok", "if that's ok", "if you dont mind", "if you don't mind",
            "come to think of it", "now i think of it", "now that i think of it", "actually")


def without_the_end_shrug(said):
    text = " ".join(str(said or "").split())
    changed = True
    while changed and text:
        changed = False
        stripped = text.rstrip(" .,;:!?")
        low = stripped.lower()
        for phrase in sorted(ASK_TAIL, key=len, reverse=True):
            if low.endswith(" " + phrase) or low == phrase:
                cut = stripped[:len(stripped) - len(phrase)].rstrip(" ,;:-")
                if cut:
                    text = " ".join(cut.split())
                    changed = True
                break
    return text


def without_the_shrug(said):
    words = str(said or "").split()
    kept = [word for word in words if word.lower().strip(".,;:!?") not in IN_THE_WAY]
    return " ".join(kept) if kept else " ".join(words)
