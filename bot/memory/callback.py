import re

from . import facts, holds as earlier

THE_ASK = re.compile(
    r"^\s*(?:and\s+|so\s+|but\s+)?(?:"
    r"how(?:'s|\s+is|\s+are|\s+was|\s+were)\s+(?P<who>he|she|they|him|her|them)\s*"
    r"(?:doing|getting\s+on|going|coping|holding\s+up|been)?"
    r"|how\s+(?:has|have)\s+(?P<been>he|she|they)\s+been"
    r"|is\s+(?P<better>he|she|they)\s+(?:any\s+)?better"
    r")\s*(?:now|today|then|since|at\s+the\s+moment)?\s*\?*\s*$",
    re.I)
THE_NAMED_ASK = re.compile(
    r"^\s*(?:and\s+|so\s+)?(?:"
    r"how(?:'s|\s+is|\s+was)\s+(?:your\s+|my\s+)?(?P<who>[a-z]{2,})"
    r"|any\s+news\s+(?:about|on|of)\s+(?:your\s+|my\s+)?(?P<news>[a-z]{2,})"
    r"|how\s+did\s+it\s+go\s+with\s+(?:your\s+|my\s+)?(?P<went>[a-z]{2,})"
    r")\s*(?:doing|getting\s+on|now|then|today)?\s*\?*\s*$",
    re.I)
THE_RELATIONS = frozenset(facts.RELATIONS) | frozenset(
    "mum mom mam mother dad father gran granny grandma grandad grandpa nan nana pops".split())
AN_AGE = re.compile(r"^(?:is|was|turned|is\s+now|just\s+turned)\s+\d{1,3}\b", re.I)
MOST_WORDS_OF_NEWS = 9


def _the_person_held(memory):
    from . import others as the_others
    held = [one for one in (the_others(memory) or []) if isinstance(one, dict)]
    for one in reversed(held):
        relation = str(one.get("who") or "").strip().lower()
        if not relation:
            continue
        name = str(one.get("name") or "").strip()
        age = one.get("age")
        return relation, name, age
    named = []
    for line in earlier.lines(memory):
        for found in re.finditer(r"\b(?:my|our)\s+([a-z]{3,})\b", str(line).lower()):
            word = found.group(1)
            if word in THE_RELATIONS and word not in named:
                named.append(word)
    if len(named) == 1:
        return named[0], "", None
    if named:
        return named[-1], "", None
    return None


def _the_news_about(memory, relation, name):
    words = [relation] + ([name] if name else []) + list(_the_pronouns(relation))
    for line in reversed(earlier.lines(memory)):
        low = " ".join(str(line).lower().split())
        if "?" in low or not low:
            continue
        for word in words:
            found = re.search(r"\b(?:my|our|the)?\s*" + re.escape(word) + r"\b", low)
            if not found:
                continue
            rest = low[found.end():].strip(" ,.;:!-")
            if not rest or len(rest.split()) > MOST_WORDS_OF_NEWS:
                continue
            if AN_AGE.search(rest):
                continue
            if rest.split()[0] in ("is", "was", "had", "has", "have", "went", "got", "kept",
                                   "said", "wants", "wanted", "needs", "keeps", "lives",
                                   "does", "did", "came", "started", "turned", "seems"):
                return rest.rstrip(".")
    return ""


def _the_pronouns(relation):
    if relation in facts.HE:
        return ("he",)
    if relation in facts.SHE:
        return ("she",)
    return ("they",)


def _the_ask(text, memory):
    if not isinstance(memory, dict):
        return None
    said = " ".join(str(text or "").lower().split())
    match = THE_ASK.match(said)
    if match:
        held = _the_person_held(memory)
        if not held:
            return ""
        pointed = match.group("who") or match.group("been") or match.group("better") or ""
        if pointed in ("he", "she"):
            wanted = "he" if pointed == "he" else "she"
            if _the_pronouns(held[0])[0] != wanted:
                return ""
        return held
    match = THE_NAMED_ASK.match(said)
    if match:
        word = (match.group("who") or match.group("news") or match.group("went") or "").strip()
        if word not in THE_RELATIONS:
            return ""
        held = _the_person_held(memory)
        if not held:
            return ""
        if held[0] not in (word, word.rstrip("s")):
            return ""
        return held
    return ""


IN_A_MEDICAL_EPISODE = re.compile(
    r"\b(?:hospital|hospitalis\w*|hospitaliz\w*|surgery|surgical|operation"
    r"|a&?e|casualty|intensive care|icu|coronary care|hospice|care home|nursing home"
    r"|the ward|on a ward|in a ward)\b", re.I)
EPISODE_TURNS = 6


def _a_medical_episode(memory):
    for line in earlier.lines(memory)[-EPISODE_TURNS:]:
        if IN_A_MEDICAL_EPISODE.search(str(line)):
            return True
    return False


def reply_for(text, memory):
    if not isinstance(memory, dict) or not earlier.there_is_one(memory):
        return ""
    if _a_medical_episode(memory) or IN_A_MEDICAL_EPISODE.search(str(text or "")):
        return ""
    held = _the_ask(text, memory)
    if not held:
        return ""
    relation, name, age = held
    who = name.capitalize() if name else "your " + relation
    news = _the_news_about(memory, relation, name)
    if age and news and re.fullmatch(r"(?:is|was)\s+" + re.escape(str(age)) + r"(?:\s+years?\s+old)?", news):
        news = ""
    since = ("Any word since then?", "Any news since?", "Has there been any change?",
             "Anything new since?")
    if news:
        pool = ("You said {who} " + news + ". {since}",
                "Last you said, {who} " + news + ". {since}",
                "{who_cap} " + news + ", you said. {since}")
        return _choose([line.format(who=who, who_cap=who.capitalize(), since=ask)
                        for line in pool for ask in since], memory)
    if age:
        pool = ("{who_cap} is " + str(age) + " - what has {pronoun} been saying?",
                "{who_cap} is " + str(age) + ", and that is all I have. What is {pronoun} up to "
                "at the moment?",
                "{who_cap} is " + str(age) + " - has {pronoun} been in touch?")
        return _choose([line.format(who_cap=who.capitalize(), pronoun=_the_pronouns(relation)[0])
                        for line in pool], memory)
    return ""


def claims(text, memory):
    return bool(reply_for(text, memory))


def _choose(pool, memory):
    import random
    said = earlier.the_bot_lines(memory)
    fresh = [line for line in pool if line not in said]
    return random.choice(fresh or list(pool))
