import re

ENDS_THE_ATTEMPT = frozenset("""
but though although however yet still whereas while because since
""".split())
STARTS_A_CLAUSE = frozenset("""
i we it he she they you that this there its im hes shes thatll even though
her him them me us my our
""".split())
NOT_A_CLAUSE_AFTER_AND = frozenset("""
still now nothing no none neither nor so then he she they it its i we you that this there
everything anything anymore
""".split())
NOT_A_THING = frozenset("""
a an the it them that this those these one ones thing stuff and or but so
already again twice once too also just even really very much more some any all lot lots bit
bits quite rather sort kind my our your his her their of to in on at for with off out up down
not no yeah ok okay well then now since yesterday today tonight morning afternoon evening night
week weeks month months year years hour hours day days time times earlier later sooner
everything anything something nothing anyone someone everyone
about around through over back away before after first last both either
""".split())
REPORT_SUBJECTS = frozenset("""i we ive i've weve we've id wed""".split())
LOOK_BACK = 4


def _tokens(norm):
    out = []
    for word in norm or ():
        if not isinstance(word, str):
            continue
        word = word.strip().lower()
        if word:
            out.append(word)
    return out


def _a_report(words, at):
    if at == 0:
        return True
    return any(word in REPORT_SUBJECTS for word in words[max(0, at - LOOK_BACK):at])


ONE_MORE = frozenset("""
another one more again instead
""".split())
HANDS_OVER = frozenset("""
write tell make give do sing rap read say come think have got need want
""".split())
STARTS_A_QUESTION = frozenset("""
what whats which how who where when why can could would shall should whether any anything
""".split())


def _where_the_attempt_ends(words, at):
    for index in range(at + 1, len(words)):
        word = words[index]
        if word in ENDS_THE_ATTEMPT or word in STARTS_A_CLAUSE:
            return index
        if word == "and" and (index + 1 == len(words)
                              or words[index + 1] in NOT_A_CLAUSE_AFTER_AND):
            return index
        if word in STARTS_A_QUESTION:
            before = words[index - 1] if index else ""
            if (index == at + 1
                    or before in ("and", "but", "so", "then", "now", "everything", "anything",
                                  "something", "that", "this", "it")
                    or any(other in ONE_MORE for other in words[index + 1:index + 5])):
                return index
        if word in HANDS_OVER and any(other in ONE_MORE
                                      for other in words[index + 1:index + 5]):
            return index
    return len(words)


def the_things_they_tried(norm):
    words = _tokens(norm)
    tried = []
    for at, word in enumerate(words):
        if word != "tried" or not _a_report(words, at):
            continue
        for index in range(at + 1, _where_the_attempt_ends(words, at)):
            word = words[index]
            if word in NOT_A_THING or len(word) < 3 or not word.isalpha():
                continue
            if word not in tried:
                tried.append(word)
    return tried


def the_rest_after_the_try(norm):
    words = _tokens(norm)
    for at, word in enumerate(words):
        if word != "tried" or not _a_report(words, at):
            continue
        return words[_where_the_attempt_ends(words, at):]
    return []


def asks_for_one_more(norm):
    rest = the_rest_after_the_try(norm)
    if not rest:
        return False
    if not any(word in ONE_MORE for word in rest):
        return False
    if any(word in HANDS_OVER for word in rest):
        return True
    joined = " ".join(rest)
    if re.search(r"\b(?:can|could|would|will)\s+(?:you|u)\b", joined):
        return True
    if any(word in STARTS_A_QUESTION for word in rest):
        return True
    if any(word in HANDS_OVER for word in rest) and re.search(r"\bfor (?:me|us)\b|\bplease\b",
                                                             joined):
        return True
    return False


MOST_WORDS = 24


def things_tried(text, norm=None):
    words = _tokens(norm) if norm is not None else _tokens(
        re.findall(r"[a-z']+", str(text or "").lower().replace("\u2019", "'")))
    if not words or len(words) > MOST_WORDS or "tried" not in words:
        return []
    return the_things_they_tried(words)
