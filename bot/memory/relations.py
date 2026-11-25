
from bot.compose import pick
from bot.memory import history
from bot.memory import facts as extract
from bot.memory import last_bot
from bot.memory import others
from bot.memory import stem
from bot.memory import user
from bot.memory.store_lines import CHILD
from bot.memory.store_lines import CHILD_OF
from bot.memory.store_lines import CHILD_RELATIONS
from bot.memory.store_lines import FAMILY_GROUP
from bot.memory.store_lines import GROUP_OF
from bot.memory.store_lines import HAVE_ANY_WORDS
from bot.memory.store_lines import HER_WORD
from bot.memory.store_lines import PERSON_GROUP
from bot.memory.store_lines import PET_WORDS
from bot.memory.store_lines import PRONOUN_PEOPLE
from bot.memory.store_lines import RELATION_ALIKE
from bot.memory.store_lines import _ABOUT_WHO
from bot.understanding import breeds
from bot.understanding.normalize import normalise
import re


CHAT_TAIL = re.compile(
    r"(?:[\s,]*\b(?:of|in|from|for|to)\s+(?:this|our|the)\s+"
    r"(?:chat|conversation|talk|session|thread|conversation so far)\b"
    r"(?:\s+(?:so far|today|here|with you|we have had))?)+")


def _folded(text, memory=None):
    low = " ".join(str(text or "").lower().split())
    if not low:
        return ""
    seen = memory.get("understood") if isinstance(memory, dict) else None
    if isinstance(seen, dict) and " ".join(str(seen.get("text") or "").lower().split()) == low:
        folded = seen.get("norm_text") or ""
        if folded:
            return CHAT_TAIL.sub("", " ".join(
                folded.replace(" | ", " ").lower().split())).strip(" ,.;:!?")
    try:
        folded = normalise(text).get("norm_text") or ""
    except Exception:
        folded = ""
    return CHAT_TAIL.sub("", " ".join(
        (folded or low).replace(" | ", " ").lower().split())).strip(" ,.;:!?")


def _person_from_pronoun(text, memory, named_here=()):
    low = text.lower()
    people = [who for who in (user(memory).get("people") or []) if isinstance(who, str)]
    people += [str(entry.get("who")) for entry in others(memory) if entry.get("who")]
    people = list(named_here) + people
    for pronoun, fits in (("she|her", extract.SHE), ("he|his", extract.HE)):
        if re.search(r"\b(?:" + pronoun + r")(?:'s|s)?\b", low):
            for who in _newest_first(people, memory):
                if who.endswith("s") and who not in fits:
                    continue
                if _pronoun_fits(who, fits):
                    return who
            return ""
    people = _newest_first(people, memory)
    return people[0] if people else ""


def _gender_of(who):
    word = str(who or "").strip().lower()
    if not word:
        return ""
    parts = [part for part in re.split(r"[-\s]+", word) if part]
    for part in [word] + parts:
        if part in extract.SHE and part in extract.HE:
            return ""
        if part in extract.SHE:
            return "she"
        if part in extract.HE:
            return "he"
    for roots, gender in ((extract.SHE, "she"), (extract.HE, "he")):
        for root in sorted((root for root in roots if len(root) > 2), key=len, reverse=True):
            if word.endswith(root):
                return gender
    return ""


def _pronoun_fits(who, fits):
    who = str(who or "").strip().lower()
    if who in fits:
        return True
    gender = _gender_of(who)
    if not gender:
        return True
    return (extract.SHE if gender == "she" else extract.HE) is fits


def _newest_first(people, memory):
    order = []
    for entry in reversed(memory.get("facts_log") or ()):
        if not isinstance(entry, dict):
            continue
        text = str(entry.get("text") or "").lower()
        for who in people:
            if who and who not in order and re.search(r"\b" + re.escape(who) + r"s?\b", text):
                order.append(who)
    for who in reversed(people):
        if who and who not in order:
            order.append(who)
    return order


PERSON_AFTER = re.compile(
    r"^(?:\s*$|\s*[?.!,;]|\s+(?:is|are|was|were|and|or|now|then|today|already|yet|turning|"
    r"turn|turns|aged|age|again|too)\b)", re.I)


def _named_person(low, memory=None):
    chained = extract.a_chained_person(low)
    if chained:
        return extract.a_person_word(chained)
    for relation in extract.KIN_WORDS + extract.ALONE_PERSON:
        for found in re.finditer(r"\b" + relation + r"(?:\s+in\s+laws?)?(?:'s|s)?\b", low, re.I):
            if not PERSON_AFTER.match(low[found.end():]):
                continue
            if (memory is not None and relation not in extract.RELATIONS
                    and not _a_person_in_the_store(memory, relation)):
                continue
            name = " ".join(found.group(0).lower().replace("'s", "").split())
            name = re.sub(r"\bin laws$", "in law", name)
            name = re.sub(r"s$", "", name) if not name.endswith("law") else name
            return relation if name == relation else name
    return ""


def _a_person_in_the_store(memory, who):
    who = str(who or "").lower()
    if not who:
        return False
    for entry in others(memory):
        if str(entry.get("who") or "").lower() == who:
            return True
    return who in [str(person).lower() for person in (user(memory).get("people") or [])]


ABOUT_PERSON_ASK = re.compile(
    r"\b(?:what|anything|everything|much)\b[^?]{0,30}?\b(?:know|knows|remember|learnt|learned|"
    r"told|tell|said|say|mention|mentioned|got|have|has|had)\b[^?]{0,20}?\b(?:about|on)\s+(?:"
    + _ABOUT_WHO + r")|"
    r"\btell me (?:a bit |a little |more |anything )?(?:more )?about\s+(?:" + _ABOUT_WHO + r")|"
    r"\b(?:do|did|can|could)\s+(?:you|i)\s+(?:ever\s+|already\s+)?(?:know|remember|recall|tell|"
    r"told|mention|mentioned|say|said|hear|heard)\b[^?]{0,30}?\b(?:about|on)\s+(?:"
    + _ABOUT_WHO + r")",
    re.I)


ANOTHER_PERSON = re.compile(r"^(?:(?:and|or|also|then|ok|okay|what about|and what about|"
                            r"how about)\s+)*(?:my|our|the|your)?\s*"
                            r"(?:little|big|older|younger|eldest|youngest|oldest|other|second|"
                            r"third)?\s*(?:" + "|".join(extract.RELATIONS) + r")s?\s*\?*$", re.I)


def _continues_an_about_ask(memory, low):
    line = str(low or "").strip()
    if not ANOTHER_PERSON.match(line) or not _named_person(line):
        return False
    users = [str(turn.get("user") or "") for turn in _every_line(memory) if turn.get("user")]
    here = line.lower()
    while users and users[-1].strip().lower() == here:
        users.pop()
    return bool(users and ABOUT_PERSON_ASK.search(users[-1].lower()))


AGE_ASK = re.compile(r"\bhow old (?:is|are|was|were)\b|\bwhat age(?:s)? (?:is|are|was|were)\b|"
                     r"\bwhat ages?\b|\bhow old\b")


AGE_RULE_WORD = re.compile(r"^(?:do|does|did|should|shall|can|could|will|would|must|may|might|"
                           r"need)\b", re.I)


AGE_YOU_SAY = re.compile(r"^(?:you|u|i)\s+(?:say|said|think|guess|remember|know|reckon)\b",
                         re.I)


AGE_COPULA = re.compile(r"^(?:is|are|was|were|be|am)\b", re.I)


AGE_ADVERB = re.compile(r"^(?:exactly|really|roughly|approximately|about|now|actually|again|"
                        r"already|even)\b", re.I)


AGE_DETERMINER = re.compile(r"^(?:my|our|your|their|his|her|the|a|an)\b", re.I)


AGE_PERSON_WORD = re.compile(
    r"^(?:kids?|children|child|family|i|you|u|we|they|them|he|she|everyone|both|little|one)\b",
    re.I)


def _a_word_the_store_knows(memory, word):
    word = str(word or "").lower()
    if not word:
        return False
    for entry in others(memory):
        if word in (str(entry.get("name") or "").lower(), str(entry.get("who") or "").lower()):
            return True
    for pet in user(memory).get("pets") or []:
        if isinstance(pet, dict) and str(pet.get("name") or "").lower() == word:
            return True
    return word in [str(person).lower() for person in (user(memory).get("people") or [])]


def _age_is_about_a_person(low, memory):
    if _the_place_end(low)[1]:
        return True
    ask = AGE_ASK.search(low)
    if not ask:
        return True
    if extract.a_chained_person(low):
        return True
    rest = low[ask.end():].strip()
    while True:
        adverb = AGE_ADVERB.match(rest)
        if not adverb:
            break
        rest = rest[adverb.end():].strip()
    rule = AGE_RULE_WORD.match(rest)
    if rule:
        if not AGE_YOU_SAY.match(rest[rule.end():].strip()):
            return False
        rest = rest[rule.end():].strip()
    copula = AGE_COPULA.match(rest)
    if copula:
        rest = rest[copula.end():].strip()
    determiner = AGE_DETERMINER.match(rest)
    if determiner:
        if determiner.group(0).lower() in ("a", "an"):
            return False
        rest = rest[determiner.end():].strip()
    word = re.match(r"[a-z']+", rest, re.I)
    if not word:
        return False
    subject = word.group(0)
    if AGE_PERSON_WORD.match(subject) or subject.lower() in extract.KIN_WORDS:
        return True
    if _PET_WORD.fullmatch(subject) or _PET_WORD.fullmatch(subject.rstrip("s")):
        return True
    return _a_word_the_store_knows(memory, subject)


AGE_AGAIN = re.compile(r"^(?:(?:and|or|also|ok|okay|what about|and what about)\s+)*"
                        r"(?:my|your|the|our)?\s*"
                        r"(?:little|big|older|younger|eldest|youngest|oldest|other)?\s*"
                        r"(" + "|".join(extract.KIN_WORDS + extract.ALONE_PERSON)
                       + r"|kids?|children)s?\s*$", re.I)


NAME_AGAIN = re.compile(
    r"^(?:(?:and|or|also|then|ok|okay|what about|and what about)\b[\s,]*)*"
    r"(?:my|our|your|the)?\s*(?:" + "|".join(extract.KIN_WORDS) + r")(?:'s|s)?\s+name\s*\?*$",
    re.I)


AGE_SAID = re.compile(r"\b(?:your|his|her|their)\s+\w+\s+is\s+\d+\b|^\w+\s+is\s+\d+\b", re.I)


THE_KIDS = re.compile(r"\b(?:kids?|children|child|family|everyone|both|they|them|their|"
                      r"boys?|girls?)\b", re.I)


CHILD_WORD = re.compile(r"\b(?:kids?|children|child|family|boys?|girls?)\b", re.I)


_IRREGULAR_PLURAL = {"child": "children", "grandchild": "grandchildren"}


AGE_WORD = re.compile(r"\b(?:my|our|the|their|his|her|your)\s+(?:\w+\s+)?ages?\b|"
                      r"\bages?\s+of\s+(?:my|our|the|their)\b", re.I)


AGE_AS_A_CAUSE = re.compile(
    r"\b(?:just|only|part of|down to|because of|normal for|usual for|expected at)\s+"
    r"(?:\w+\s+){0,2}(?:age|old age|getting old)\b|\bold age\b|\bat (?:her|his|their|my) age\b",
    re.I)


GROUP_ASK = re.compile(
    r"\b(?:my|the|his|her|their|our|your)\s+("
    + "|".join(sorted(FAMILY_GROUP, key=len, reverse=True)) + r")\b", re.I)


def _tidy_name(value):
    value = str(value or "").strip(" .,!?;:")
    return value[:1].upper() + value[1:] if value and value[:1].islower() else value


def _same_as_last(reply, memory):
    turns = memory.get("turns") or []
    for turn in reversed([turn for turn in turns if isinstance(turn, dict)]):
        said = turn.get("bot")
        if isinstance(said, str) and said.strip():
            return said.strip() == str(reply).strip()
    return False


def _animal_family(animal):
    word = str(animal or "").lower()
    return {"puppy": "dog", "dog": "dog", "kitten": "cat", "cat": "cat",
            "bunny": "rabbit", "rabbit": "rabbit", "goldfish": "fish", "fish": "fish",
            "pony": "horse", "horse": "horse", "bird": "parrot", "parrot": "parrot"}.get(
                word, word)


def _a(word):
    return ("an " if word[:1].lower() in "aeiou" else "a ") + word


THEIR_NAME = re.compile(
    r"\b(?:what|which)\b[^.?!]*\bname\b|"
    r"\bwhat (?:is|was) (?:my|our)\s+\w+'?s?\s+(?:called|named)\b|"
    r"\bwhat do (?:i|you) call my\b", re.I)


THEIR_AGE = re.compile(
    r"\bhow old (?:is|was|are|were)\b|\bwhat age (?:is|was)\b|"
    r"\b(?:what|which)(?:'s| is| was| are)?\s+"
    r"(?:(?:my|our)\s+\w+'?s?|her|his|their)\s+age\b", re.I)


GROUP_WORDS = "|".join(sorted(GROUP_OF, key=len, reverse=True))


GROUP_NAME_ASK = re.compile(
    r"\bwhat (?:are|were)\s+(?:my|our|the)\s+(?P<a>" + GROUP_WORDS + r")\s+called\b"
    r"|\bwhat (?:are|were)\s+(?:my|our|the)\s+(?P<b>" + GROUP_WORDS + r")['\u2019s]*\s+names?\b"
    r"|\b(?:names? of|name of)\s+(?:my|our|the)\s+(?P<c>" + GROUP_WORDS + r")\b"
    r"|\b(?:my|our|the)\s+(?P<d>" + GROUP_WORDS + r")['\u2019s]*\s+names\b"
    r"|\bwhat (?:are|were)\s+(?:they|their|them)\s+called\b"
    r"|\bwhat are their names\b|\btheir names\b", re.I)


THEIR_TASTE_WHAT = re.compile(
    r"\bwhat\s+(?:does|do|did)\s+"
    r"(?:(?:my|our)\s+(?P<who>[a-z][a-z'\u2019-]*)|(?P<pronoun>she|he|they))\s+"
    r"(?P<how>like|love|enjoy|hate|dislike|not like)\b", re.I)


THEIR_TASTE_INTO = re.compile(
    r"\bwhat\s+(?:is|was)\s+"
    r"(?:(?:my|our)\s+(?P<who>[a-z][a-z'\u2019-]*)|(?P<pronoun>she|he|they))\s+"
    r"(?:into|keen on|mad about|a fan of|big on|fussed on)\b", re.I)

THEIR_TASTE_NOT = re.compile(
    r"\bwhat(?:\s+[a-z']+){0,2}?\s+"
    r"(?:doesn'?t|doesn|does\s+not|don'?t|do\s+not|won'?t|will\s+not|can'?t|cannot|never)\s+"
    r"(?:(?:my|our)\s+(?P<who>[a-z][a-z'\u2019-]*)|(?P<pronoun>she|he|they))\s+"
    r"(?:really\s+|actually\s+|even\s+|ever\s+)?"
    r"(?:like|love|eat|drink|have|stand|touch|want|be\s+keen\s+on)\b"
    r"(?:\s+(?:eating|drinking|at\s+all|really|then|now|though))*\W*$", re.I)

THEIR_TASTE_NOT_INTO = re.compile(
    r"\bwhat(?:'s|s|\s+is|\s+was)?(?:\s+[a-z']+)?\s+"
    r"(?:(?:my|our)\s+(?P<who>[a-z][a-z'\u2019-]*)|(?P<pronoun>she|he|they))\s+"
    r"(?:not|isn'?t|is\s+not)\s+"
    r"(?:into|keen\s+on|mad\s+about|a\s+fan\s+of|big\s+on|fussed\s+on)\b\W*$", re.I)


THEIR_TASTE_A_YES_NO = re.compile(
    r"\b(?:does|do|did)\s+"
    r"(?:(?:my|our)\s+(?P<who>[a-z][a-z'\u2019-]*)|(?P<pronoun>she|he|they))\s+"
    r"(?P<how>like|love|enjoy|hate|dislike)\s+(?P<thing>[a-z][a-z'\u2019 ]*?)\W*$", re.I)


def _their_taste(memory, low):
    said = None
    how = ""
    thing = ""
    for pattern in (THEIR_TASTE_A_YES_NO, THEIR_TASTE_WHAT, THEIR_TASTE_INTO):
        match = pattern.search(low)
        if match:
            said = match
            break
    if said is None:
        for pattern in (THEIR_TASTE_NOT, THEIR_TASTE_NOT_INTO):
            match = pattern.search(low)
            if match:
                said = match
                how = "not like"
                break
    if said is None:
        return None
    how = how or (said.groupdict().get("how") or "").lower()
    thing = (said.groupdict().get("thing") or "").strip().lower()
    who = (said.groupdict().get("who") or "").lower()
    pronoun = (said.groupdict().get("pronoun") or "").lower()
    known = None
    if who:
        known = next((entry for entry in others(memory)
                      if (entry.get("who") or "").lower() == who), None)
    elif pronoun:
        fits = extract.SHE if pronoun in ("she", "her") else extract.HE
        known = next((entry for entry in reversed(others(memory))
                      if (entry.get("who") or "").lower() in fits
                      and (entry.get("likes") or entry.get("dislikes"))), None)
        if known is not None:
            who = (known.get("who") or "").lower()
    if known is None:
        return None
    likes = [str(item) for item in (known.get("likes") or []) if str(item).strip()]
    dislikes = [str(item) for item in (known.get("dislikes") or []) if str(item).strip()]
    if thing:
        for item in likes:
            if _same_thing(item, thing):
                return _they_like_sentence(who, [item], "yes", pronoun)
        for item in dislikes:
            if _same_thing(item, thing):
                return _they_like_sentence(who, [item], "no", pronoun)
        return None
    if how in ("hate", "dislike", "not like"):
        if not dislikes:
            if likes:
                said = _they_like_sentence(who, likes, "yes", pronoun)
                return "Nothing now \u2014 " + said[:1].lower() + said[1:]
            return ("You haven't told me what your " + who + " doesn't like yet.")
        return _they_like_sentence(who, dislikes, "no", pronoun)
    if not likes:
        return "You haven't told me what your " + who + " likes yet."
    return _they_like_sentence(who, likes, "yes", pronoun)


def _same_thing(one, other):
    one = str(one or "").lower().strip()
    other = str(other or "").lower().strip()
    if not one or not other:
        return False
    if one == other:
        return True
    return stem(one.split()[-1]) == stem(other.split()[-1])


_PLURAL = frozenset("""kids children sons daughters boys girls parents friends brothers sisters
grandchildren grandkids nieces nephews cousins grandparents in-laws""".split())


def _plural_person(who):
    who = str(who or "").lower()
    return who in _PLURAL or (who.endswith("s") and who not in ("boss", "christmas"))


def _they_like_sentence(who, things, how, pronoun=""):
    listed = " and ".join(things[:2])
    if who:
        head = "Your " + who + " "
        some = _plural_person(who)
    else:
        head = "They " if pronoun == "they" else "She " if pronoun == "she" else "He "
        some = pronoun == "they"
    if how == "no":
        return head + ("don't like " if some else "doesn't like ") + listed + "."
    return head + ("love " if some else "loves ") + listed + "."


THEIR_JOB = re.compile(
    r"\bwhat\s+(?:does|do|did)\s+"
    r"(?:(?:my|our)\s+(?P<who>[a-z][a-z'\u2019-]*)|(?P<pronoun>she|he|they))\s+do\b"
    r"(?:\s+(?:for (?:a living|work|their job)|as a job|exactly|all day|now))?\W*$|"
    r"\bwhat(?:'s|s| is| was)?\s+"
    r"(?:(?:my|our)\s+(?P<who2>[a-z][a-z'\u2019-]*)|(?P<pronoun2>she|he|they))"
    r"'?s?\s+(?:job|work)\b|"
    r"\bwhat\s+(?:(?:my|our)\s+(?P<who3>[a-z][a-z'\u2019-]*)|(?P<pronoun3>she|he|they))"
    r"\s+(?:does|do)\b\W*$", re.I)


def _their_job(memory, low):
    match = THEIR_JOB.search(low)
    if not match:
        return None
    groups = match.groupdict()
    who = (groups.get("who") or groups.get("who2") or groups.get("who3") or "").lower()
    pronoun = (groups.get("pronoun") or groups.get("pronoun2")
               or groups.get("pronoun3") or "").lower()
    known = None
    if who:
        known = _a_kept_person(memory, who)
        if known is not None:
            who = (known.get("who") or "").lower()
    elif pronoun and pronoun != "they":
        fits = extract.SHE if pronoun == "she" else extract.HE
        known = next((entry for entry in reversed(others(memory))
                      if (entry.get("who") or "").lower() in fits and entry.get("job")), None)
        if known is not None:
            who = (known.get("who") or "").lower()
    if known is None:
        who_kept = bool(who) and not pronoun and (who in extract.KIN
                                                 or _kin_forms(who) & set(extract.KIN))
        if who_kept:
            return "You haven't told me what your " + who + " does yet."
        return None
    job = str(known.get("job") or "").strip()
    if not job:
        return "You haven't told me what your " + who + " does yet." if who else None
    if who and _plural_person(who):
        return "Your " + who + " work as " + _a(job) + "."
    if who:
        return "Your " + who + " is " + _a(job) + "."
    return ("She's " if pronoun == "she" else "He's ") + _a(job) + "."


def _kin_forms(who):
    word = str(who or "").lower().strip()
    forms = {word}
    bare = re.sub(r"(?:'s|s'|s)$", "", word)
    if bare and bare != word:
        forms.add(bare)
    forms.add(word + "s")
    return forms


def _a_kept_person(memory, who):
    forms = _kin_forms(who)
    for entry in others(memory):
        if (entry.get("who") or "").lower() in forms:
            return entry
    return None


def _same_name_however_they_wrote_it(entry, line):
    if _same_name(entry.get("name") or "", line):
        return True
    return any(_same_name(old, line) for old in (entry.get("was") or []))


def _same_name(known, line):
    known = str(known or "").strip().lower()
    if not known:
        return False
    tokens = re.findall(r"[a-z']+", str(line or "").lower())
    for token in tokens:
        if token == known:
            return True
        folded = _folded(token)
        if folded == _folded(known):
            return True
    return False


def _more_than_one(who):
    return _plural_person(who)


def _canon_relation(word):
    word = str(word or "").strip(" .,").lower()
    word = RELATION_ALIKE.get(word, word)
    if word.endswith("s") and word[:-1] in RELATION_ALIKE:
        return RELATION_ALIKE[word[:-1]]
    if word.endswith("s") and word[:-1] in CHILD_RELATIONS:
        return word[:-1]
    return word


def _relations_of(who):
    found = []
    for word in re.split(r"\s+and\s+|\s+|,", str(who or "").strip().lower()):
        canon = _canon_relation(word)
        if not canon:
            continue
        if canon in ("child", "children", "kid", "kids"):
            found.extend(CHILD_RELATIONS)
        elif canon == "parent" or canon == "parents":
            found.extend(GROUP_OF["parents"])
        else:
            found.append(canon)
    return tuple(found)


def _in_the_group(who, group):
    return any(word in group for word in _relations_of(who))


def _a_list_of_names(names):
    said = [str(name) for name in names if str(name)]
    if len(said) < 3:
        return " and ".join(said)
    return ", ".join(said[:-1]) + " and " + said[-1]


def _mentioned_the_group(memory, group, word):
    held = user(memory)
    if word in ("children", "kids", "childs") and held.get("kids"):
        return True
    if any(_in_the_group(person, group) for person in (held.get("people") or [])):
        return True
    return _the_group_was_said(word, memory)


HAVE_ANY = re.compile(
    r"^(?:and\s+|so\s+|ok\s+|okay\s+|but\s+)?(?:do|have|did)\s+(?:i|we)\s+"
    r"(?:got|have|has)?\s*(?:(?:any|a|an)\s+)?"
    r"(?P<what>(?:" + "|".join(sorted(HAVE_ANY_WORDS, key=len, reverse=True)) + r")"
    r"(?:\s*(?:,|or|and)\s*(?:brothers|sisters|siblings|children|kids|parents|family)"
    r"|\s*(?:,|or|and)\s*(?:brother|sister|parent|child|kid))*)\b", re.I)


def _whether_they_have(memory, low):
    if not isinstance(low, str):
        return None
    match = HAVE_ANY.match(low.strip(" ,.!?;:"))
    if not match:
        return None
    words = [word for word in re.split(r"\s*(?:,|\bor\b|\band\b)\s*",
                                      match.group("what").lower()) if word]
    if not words:
        return None
    held = [entry for entry in others(memory) if isinstance(entry, dict)]
    plain = [str(word).lower() for word in (user(memory).get("people") or [])]
    counts = {}
    found = []
    said_without_a_name = []
    empty = []
    for word in words:
        group = (CHILD_RELATIONS + GROUP_OF["parents"] + GROUP_OF["siblings"]
                 + GROUP_OF["grandparents"]) if word == "family" else (
                     GROUP_OF.get(word) or (_canon_relation(word),))
        mine = [entry for entry in held if _in_the_group(entry.get("who"), group)]
        if mine:
            found.append((word, mine[0]))
            continue
        hinted = [_canon_relation(one) for one in plain if _in_the_group(one, group)]
        count = user(memory).get("kids")
        if hinted:
            said_without_a_name.extend(hinted)
            continue
        if (isinstance(count, int) and not isinstance(count, bool) and count == 0
                and _in_the_group("child", group)):
            said_without_a_name.append(word)
            counts[word] = count
            continue
        if isinstance(count, int) and count > 0 and _in_the_group("child", group):
            word = word if word in ("kids", "children", "childs") else "child"
            said_without_a_name.append(word)
            counts[word] = count
            continue
        empty.append(word)
    if not found and not said_without_a_name:
        asked = _a_plural_list(words)
        return pick(["You haven't told me about " + _a_or_any(words) + " yet.",
                     "Nothing on your " + asked + " yet - tell me and I'll keep it."], memory)
    said = []
    bare = list(dict.fromkeys(said_without_a_name))
    for word, entry in found:
        who = str(entry.get("who") or word).strip()
        name = str(entry.get("name") or "").strip()
        names = [str(one) for one in (entry.get("names") or []) if str(one).strip()]
        if not name and len(names) > 1:
            said.append("your " + who + " are called " + _a_list_of_names(names))
        elif name:
            said.append("your " + who + " " + _called(name))
        elif who not in bare:
            bare.append(who)
    line = ""
    if said:
        line = "You've mentioned " + _a_list_of_names(said)
    if bare:
        none_of_them = bool(counts) and not any(counts.values())
        how_many = next((value for value in counts.values() if value), 0)
        if none_of_them:
            line += (" " if line else "") + "You told me you don't have any " + \
                _a_list_of_words(bare) + "."
        else:
            if how_many:
                said_them = str(how_many) + " " + bare[0]
            else:
                said_them = _a_list_of_words([_with_article(word) for word in bare])
            names = ("their names" if len(bare) > 1 or how_many > 1
                     else HER_WORD.get(bare[0], "their") + " name")
            line += (" " if line else "") + "You've told me you have " + said_them + \
                ", but not " + names + " yet."
    if empty:
        tail = "no " + _a_list_of_words(empty) + " that you've told me about"
        if line:
            line = line.rstrip(".") + " - and " + tail + "."
        else:
            line = "You haven't mentioned any " + _a_list_of_words(empty) + " yet."
    return line if line.endswith(".") else line + "."


def _a_list_of_words(words):
    said = [str(word) for word in words if str(word)]
    if len(said) < 2:
        return "".join(said)
    if len(said) == 2:
        return said[0] + " and " + said[1]
    return ", ".join(said[:-1]) + " and " + said[-1]


def _more_than_one_word(word):
    word = str(word or "").strip().lower()
    return word.endswith("s") or word in ("children", "kids", "family")


def _with_article(word):
    word = str(word or "")
    return ("any " if _more_than_one_word(word) else "a ") + word


def _a_or_any(words):
    said = [str(word) for word in words if str(word)]
    if len(said) == 1:
        return _with_article(said[0])
    first = said[0]
    rest = " or ".join(said[1:])
    return ("any " if _more_than_one_word(first) else "a ") + first + " or " + rest


def _a_plural_list(words):
    said = [str(word) for word in words if str(word)]
    if not said:
        return ""
    if len(said) == 1:
        return said[0]
    if len(said) == 2:
        return said[0] + " or " + said[1]
    return ", ".join(said[:-1]) + " or " + said[-1]


GROUP_NAMES_TYPED = re.compile(
    r"\bmy (?P<who>" + "|".join(["kids", "children", "childs", "sons", "daughters", "boys",
                                 "girls", "parents", "brothers", "sisters", "grandchildren"])
    + r")\s+(?:are|is)\s+(?P<names>[^.!?]{3,60})", re.I)


def _the_group_names_typed(word, memory):
    said = []
    for turn in (memory or {}).get("turns") or []:
        if not isinstance(turn, dict):
            continue
        line = str(turn.get("user") or "")
        match = GROUP_NAMES_TYPED.search(line)
        if not match:
            names = _the_names_a_pronoun_gave(line)
            if names and ((memory or {}).get("user") or {}).get("kids"):
                said = names
            continue
        if not _in_the_group(match.group("who").lower(), GROUP_OF.get(word, ())):
            continue
        names = [one.strip(" .,") for one in re.split(r",|\band\b|&", match.group("names"))
                 if one.strip(" .,")]
        names = [one for one in names if 2 <= len(one) <= 14 and one.isalpha()
                 and one.lower() not in extract.KIN_WORDS]
        if 2 <= len(names) <= 3:
            said = names
    return said


THEY_ARE_NAMED = re.compile(
    r"^\W*(?:they|they're|theyre|those|these)\s+(?:are|were)\s+(?:called|named)\s+"
    r"(?P<names>[^.!?]{3,60})$", re.I)


def _the_names_a_pronoun_gave(line):
    match = THEY_ARE_NAMED.search(str(line or "").strip())
    if not match:
        return []
    return _the_names_from(match.group("names"))


def _the_names_from(said):
    names = [one.strip(" .,") for one in re.split(r",|\band\b|&", str(said or ""))
             if one.strip(" .,")]
    names = [one for one in names if 2 <= len(one) <= 14 and one.isalpha()
             and one.lower() not in extract.KIN_WORDS]
    return names if 2 <= len(names) <= 3 else []


PEOPLE_MANY = ("kids|children|childs|sons|daughters|boys|girls|brothers|sisters|twins|parents"
               "|grandchildren|grandparents|aunts|uncles|cousins|siblings|stepchildren|nieces"
               "|nephews|babies|teens|teenagers")

SEVERAL_PEOPLE_NAMED = re.compile(
    r"\b(?:one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|\d+"
    r"|a couple of|a few|both|the pair)\s+(?P<counted>" + PEOPLE_MANY + r")\b"
    r"|\b(?:my|our|the|his|her|their)\s+(?P<group>" + PEOPLE_MANY + r")\b"
    r"|\b(?P<bare>" + PEOPLE_MANY + r")\b", re.I)


TWO_OF_KIN = re.compile(
    r"\b(?:my|our|the|a|an)\s+(?P<a>" + "|".join(sorted(extract.KIN_WORDS)) + r")\s+and\s+"
    r"(?:my|our|the|a|an)?\s*(?P<b>" + "|".join(sorted(extract.KIN_WORDS)) + r")\b", re.I)


def _the_several_named_before(memory):
    for line in reversed(history.the_lines_before(memory)):
        if not history.is_their_news(line):
            continue
        found = SEVERAL_PEOPLE_NAMED.search(line)
        names = _the_names_from(_the_names_tail(line))
        pair = TWO_OF_KIN.search(line) if not found else None
        if not found and not pair and not names:
            continue
        word = ((found.group("counted") or found.group("group") or found.group("bare"))
                if found else "").lower()
        phrase = " ".join(found.group(0).split()) if found else ""
        if pair:
            one, other = pair.group("a").lower(), pair.group("b").lower()
            word = one + " and " + other
            phrase = "your " + one + " and your " + other
        return word, names, phrase
    return "", [], ""


def _the_names_tail(line):
    said = str(line or "")
    match = re.search(r"(?:\bcalled\b|\bnamed\b|,)\s*(?P<names>[^.!?]{3,60})$", said, re.I)
    if match:
        return match.group("names")
    match = re.search(r"\b(?:" + PEOPLE_MANY + r")\s+(?:are|were)\s+(?P<names>[^.!?]{3,60})$",
                      said, re.I)
    return match.group("names") if match else ""


def _the_names_of_them_all(memory):
    word, names, phrase = _the_several_named_before(memory)
    if names:
        return _a_list_of_names([_called(one) for one in names]) + "."
    if word:
        told = re.sub(r"^(?:my|our|the)\s+", lambda m: "your ", phrase, flags=re.I) or word
        return pick(["You told me about " + told + ", but not their names - what are they called?",
                     "I've got " + told + " from you, but not their names. Tell me and I'll keep "
                     "them."], memory)
    return None


def _the_names_they_typed(word, memory):
    said = _the_group_names_typed(word, memory)
    if not said:
        return None
    return _a_list_of_names([_called(one) for one in said]) + ", then - I'll keep those as your " \
        + word + "' names."


def _the_names_of_the_group(memory, low):
    if not isinstance(low, str):
        return None
    ask = GROUP_NAME_ASK.search(low)
    if not ask:
        return None
    word = next((ask.group(g) for g in ("a", "b", "c", "d") if ask.group(g)), "").lower()
    known = [entry for entry in others(memory) if isinstance(entry, dict)]
    if word:
        group = (CHILD_RELATIONS + GROUP_OF["parents"] + GROUP_OF["siblings"]
                 + GROUP_OF["grandparents"] + GROUP_OF["grandchildren"]
                 + GROUP_OF["aunts"] + GROUP_OF["uncles"] + GROUP_OF["cousins"])
        if word != "family":
            group = GROUP_OF.get(word, ())
        known = [entry for entry in known if _in_the_group(entry.get("who"), group)]
        if not known and not _mentioned_the_group(memory, group, word):
            return pick(["You haven't told me about your " + word + " yet.",
                         "I've got nothing about your " + word + " yet - tell me and I'll keep it."],
                        memory)
    else:
        if len(known) < 2:
            known = [entry for entry in known
                     if _more_than_one(entry.get("who"))
                     or len([one for one in (entry.get("names") or []) if str(one).strip()]) > 1
                     or int(entry.get("count") or 1) > 1]
    said = []
    for entry in known[:4]:
        who = str(entry.get("who") or "").strip()
        name = entry.get("name")
        names = [str(n) for n in (entry.get("names") or []) if str(n).strip()]
        if len(names) > 1:
            said.append((who, _a_list_of_names(names), True))
        elif isinstance(name, str) and name:
            said.append((who, _called(name), False))
    if not said:
        if not word:
            forgotten = _the_names_of_them_all(memory)
            if forgotten:
                return forgotten
            group = next((str(entry.get("who") or "").strip() for entry in known
                          if _more_than_one(entry.get("who"))), "")
            if group:
                return pick(["You haven't told me a name for your " + group + " yet - what are "
                             "they called?", "I've got your " + group + " but no names for them - "
                             "what are they called?"], memory)
        if _the_group_was_said(word, memory):
            typed = _the_names_they_typed(word, memory)
            if typed:
                return typed
            return pick(["What are your " + word + " called? I'll keep their names.",
                         "Tell me what your " + word + " are called and I'll keep it."], memory)
        if not word:
            return None
        return pick(["You haven't told me a name for your " + word + " yet.",
                     "I don't have a name for your " + word + " yet."], memory)
    grouped = []
    for who, value, paired in said:
        for at, (held_who, held_value, held_paired) in enumerate(grouped):
            if not paired and not held_paired and held_who == who:
                grouped[at] = (who, held_value + "\0" + value, paired)
                break
        else:
            grouped.append((who, value, paired))
    parts = []
    for who, value, paired in grouped:
        if paired:
            parts.append("you told me your " + who + " are called " + value)
        else:
            parts.append("your " + who + (" are" if _more_than_one(who) else " is")
                         + " called " + _a_list_of_names(value.split("\0")))
    if len(parts) == 1:
        one = parts[0]
        return (one[0].upper() + one[1:]) + "."
    if len(parts) == 2 and not any(paired for _, _, paired in said):
        return (parts[0][0].upper() + parts[0][1:]) + ", and " + parts[1] + "."
    return ". ".join(part[0].upper() + part[1:] for part in parts) + "."


def _did_you_mean(entry, property_, ask_gender=""):
    who = str(entry.get("who") or "")
    gender = _gender_of(who)
    pronoun = "She" if gender == "she" else "He" if gender == "he" else "They"
    plural = pronoun == "They"
    if property_ == "name":
        verb = "are called " if plural else "is called "
        fact = _called(str(entry.get("name") or ""))
    elif entry.get("turns"):
        verb = "turn " if plural else "turns "
        fact = str(entry.get("age") or "") + " " + str(entry["turns"])
    else:
        verb = "are " if plural else "is "
        fact = str(entry.get("age") or "")
    if ask_gender and gender and gender != ask_gender:
        him = "her" if gender == "she" else "him"
        return ("I've only got your " + who + " down, and " + pronoun.lower() + " " + verb
                + fact + ". Did you mean " + him + "?")
    return "Did you mean your " + who + "? " + pronoun + " " + verb + fact + "."


def _relation_reply(memory, low):
    tasted = _their_taste(memory, low)
    if tasted:
        return tasted
    worked = _their_job(memory, low)
    if worked:
        return worked
    have_any = _whether_they_have(memory, low)
    if have_any:
        return have_any
    grouped = _the_names_of_the_group(memory, low)
    if grouped:
        return grouped
    wants_name = bool(THEIR_NAME.search(low) or NAME_AGAIN.match(low))
    wants_age = bool(THEIR_AGE.search(low))
    by_name = ""
    if not (wants_name or wants_age):
        return None
    property_ = "name" if wants_name else "age"
    who = _named_person(low, memory)
    if (property_ == "age" and who and not who.endswith("s")
            and re.search(r"\b" + re.escape(who) + r"s\b", low)):
        return None
    known = None
    for entry in others(memory):
        if who and entry.get("who") == who:
            known = entry
            break
        if not who and _same_name_however_they_wrote_it(entry, low):
            known = entry
            by_name = entry.get("name") or ""
            who = entry.get("who") or ""
            break
    if (known is None and not who and property_ == "age" and
            re.search(r"\b(?:they|them)\b", low)):
        return None
    if known is None and not who and re.search(r"\b(?:she|he|her|his|they|them)\b", low):
        she = re.search(r"\b(?:she|her)\b", low) is not None
        fits = extract.SHE if she else extract.HE
        for entry in reversed(others(memory)):
            has_fact = entry.get(property_) or (property_ == "age" and entry.get("months"))
            if has_fact and _pronoun_fits(entry.get("who") or "", fits):
                known = entry
                who = entry.get("who") or ""
                break
    if known is None and not who and re.search(r"\b(?:she|he|her|his)\b", low):
        held = [entry for entry in others(memory) if isinstance(entry, dict)
                and (entry.get(property_) or (property_ == "age" and entry.get("months")))]
        if len(held) == 1:
            offered = _did_you_mean(held[0], property_, _ask_gender(low))
            if offered:
                return offered
    if known is None and who:
        for entry in others(memory):
            words = [w.strip() for w in str(entry.get("who") or "").split(" and ")]
            names = entry.get("names") or []
            grouped = _relations_of(entry.get("who"))
            if (len(names) > 1 and (who in words or _canon_relation(who) in grouped)):
                return ("You told me your " + str(entry["who"]) + " are "
                        + _a_list_of_names(names) + " - which one is your "
                        + who + "?")
    if known is None and wants_name and who:
        return "You haven't told me a name for your " + who + " yet."
    if known is not None and not known.get(property_) and property_ == "age" and known.get("name"):
        pronoun = _pronoun_for(who, known)
        return ("Your " + who + " is called " + _called(str(known["name"]))
                + ", but you haven't told me how old " + pronoun
                + (" are." if pronoun == "they" else " is."))
    if property_ == "age" and known and known.get("months") and not known.get("age"):
        pronoun = str(known.get("pronoun") or "")
        if who:
            name = "Your " + who
            plural = who.endswith("s")
        else:
            name = {"she": "She", "he": "He"}.get(pronoun, "They")
            plural = pronoun in ("", "they")
        return name + (" are " if plural else " is ") + str(known["months"]) + " months old."
    if known is None or not known.get(property_):
        return None
    said = _called(str(known[property_])) if property_ == "name" else str(known[property_])
    if not who:
        return ("Their " if re.search(r"\bthey\b", low) else "That's ") + said + "."
    if known.get("name") and (by_name or _same_name(str(known["name"]), low)):
        named_one = _called(str(known["name"]))
        return (named_one + (" is called " if property_ == "name" else " is ") + said + ".")
    mine = "Your " + who + " " + ("are " if _more_than_one(who) else "is ")
    if property_ == "name":
        return mine + "called " + said + "."
    if known.get("turns"):
        return _one_age(who, known["age"], str(known["turns"]), known.get("to_come"))
    return mine + said + "."


def _pronoun_for(who, known=None):
    name = str((known or {}).get("name") or "")
    title = name.split(" ")[0].strip(".").lower() if " " in name or name else ""
    if title in extract.TITLE_GENDER:
        return extract.TITLE_GENDER[title]
    if who in extract.SHE and who not in extract.HE:
        return "she"
    if who in extract.HE and who not in extract.SHE:
        return "he"
    return "they"


def _the_group_word(who):
    who = str(who or "").lower()
    for word in (who, who[:-2] if who.endswith("es") else "", who[:-1] if who.endswith("s") else "",
                 CHILD_OF.get(who, ""), who + "s"):
        if word and word in PERSON_GROUP:
            return word
    return ""


def _the_group_was_said(who, memory):
    word = _the_group_word(who)
    if not word:
        return False
    forms = {word, word + "s", word + "es", CHILD_OF.get(word, "")}
    forms = {one for one in forms if one and len(one) > 2}
    for turn in (memory or {}).get("turns") or []:
        if not isinstance(turn, dict):
            continue
        said = str(turn.get("user") or "").lower()
        if any(re.search(r"(?<![a-z])" + re.escape(one) + r"(?![a-z])", said) for one in forms):
            return True
    return False


def _ages_reply(memory, low, text=""):
    if not isinstance(low, str):
        return None
    if _continues_an_about_ask(memory, low):
        return None
    if not (AGE_ASK.search(low) or AGE_WORD.search(low)):
        said = str(text or low).strip().rstrip("?.!").lower()
        if not (_just_gave_an_age(memory) and AGE_AGAIN.match(said)):
            return None
    if AGE_AS_A_CAUSE.search(low) and not AGE_ASK.search(low):
        return None
    if AGE_ASK.search(low) and not _age_is_about_a_person(low, memory):
        return None
    if (not AGE_ASK.search(low)
            and re.search(r"\b(?:normal|typical|usual|common|expected)\b", low)
            and any(isinstance(entry.get("age"), int) or isinstance(entry.get("months"), int)
                    or entry.get("ages") for entry in others(memory))):
        return None
    told = []
    for entry in others(memory):
        who_said = str(entry.get("who") or "")
        turns = str(entry.get("turns") or "")
        held = str(entry.get("name") or "")
        to_come = entry.get("to_come")
        if isinstance(entry.get("age"), int):
            told.append((who_said, entry["age"], turns,
                         to_come if isinstance(to_come, int) else None, held))
        for age in entry.get("ages") or []:
            if isinstance(age, int):
                told.append((who_said, age, turns, None, ""))
        months = entry.get("months")
        if isinstance(months, int):
            told.append((who_said, str(months) + " months", turns, None, held))
    if not _named_person(low, memory):
        placed = _the_place_word_filed(memory, low)
        if placed:
            return placed
    who = _named_person(low, memory)
    asked_plural = bool(who) and (who.endswith("s")
                                  or bool(re.search(r"\b" + re.escape(who) + r"s\b", low)))
    group = GROUP_ASK.search(low)
    if group:
        word = group.group(1).lower()
        members = [entry for entry in told
                   if entry[0].split()[0] in FAMILY_GROUP[word]
                   or entry[0].split()[0] == word
                   or CHILD_OF.get(entry[0].split()[0]) in FAMILY_GROUP[word]]
        if members:
            return _ages_sentence(members)
        if word in ("kids", "children") and not told:
            return "You haven't told me how old they are."
        return "You haven't told me how old your " + word + " are."
    if not who and THE_KIDS.search(low):
        children = [entry for entry in told
                    if CHILD_OF.get(entry[0], entry[0].rstrip("s")) in CHILD]
        if CHILD_WORD.search(low):
            if not children:
                return "You haven't told me how old they are."
            return _ages_sentence(children)
        told = children or told
        if not told and not re.search(r"\b(?:kids?|children|child|family)\b", low):
            ages = _pet_ages(memory)
            if ages:
                return _pet_ages_sentence(ages)
        if not told:
            theirs = memory.get("their_age")
            if isinstance(theirs, dict) and theirs.get("age"):
                return _one_age("", theirs["age"], theirs.get("turns") or "")
            return "You haven't told me how old they are."
        return _ages_sentence(told)
    if not who and re.search(r"\b(?:she|her|hers|he|him|his)\b", low):
        who = _person_from_pronoun(low, memory)
        if not who:
            pronoun = "she" if re.search(r"\b(?:she|her)\b", low) else "he"
            for entry in others(memory):
                if str(entry.get("pronoun") or "") != pronoun:
                    continue
                age = entry.get("age")
                months = entry.get("months")
                if not isinstance(age, int) and not isinstance(months, int):
                    continue
                if isinstance(months, int):
                    return ("He is " if pronoun == "he" else "She is ") + str(months) + " months."
                when = str(entry.get("turns") or "")
                he = pronoun == "he"
                if when:
                    return ("He turns " if he else "She turns ") + str(age) + " " + when + "."
                return ("He is " if he else "She is ") + str(age) + "."
    if not who:
        pet = _pet_age_reply(memory, low)
        if pet:
            return pet
        return None
    for who_said, age, turns, to_come, held in told:
        if held and re.search(r"\b" + re.escape(held.lower()) + r"\b", low):
            return _one_age(who, age, turns, to_come, held)
    if asked_plural:
        word = who if who.endswith("s") else who + "s"
        family = [age for age in told if age[0].split()[0] == word]
        if len(family) > 1:
            return _ages_sentence(family)
    for who_said, age, turns, to_come, held in told:
        if who_said == who or (who.endswith("s") and who_said == who[:-1]):
            return _one_age(who, age, turns, to_come, held)
    family = [one for one in told
              if one[0].split()[0] in (who + "s", _IRREGULAR_PLURAL.get(who, who + "s"))]
    if family:
        return _ages_sentence(family)
    return "You haven't told me how old your " + who + (" are." if who.endswith("s") else " is.")


_THE_YOUNGER_END = frozenset(("youngest", "littlest", "baby", "toddler", "newborn", "little one",
                              "wee one", "little lad", "little girl", "little boy", "small one",
                              "younger one"))
_THE_OLDER_END = frozenset(("eldest", "oldest", "elder", "big one", "older one", "biggest"))
_A_PLACE_ASK = re.compile(
    r"\b(?:the|my|our|your)\s+(?P<who>"
    + "|".join(sorted(_THE_YOUNGER_END | _THE_OLDER_END, key=len, reverse=True)) + r")\b", re.I)


_THE_PLACE_STANDS_ALONE = frozenset((
    "now", "then", "there", "too", "though", "anyway", "please", "is", "was", "were", "are",
    "again", "still", "yet", "today", "nowadays", "here", "of", "in", "at", "on", "and", "or",
    "got", "has", "have", "had", "will", "would", "should", "can", "could", "might", "must",
    "turns", "turned", "just", "only", "already", "actually", "really"))


def _the_place_end(low):
    asked = _A_PLACE_ASK.search(str(low or ""))
    if not asked:
        return "", ""
    after = str(low)[asked.end():]
    after = re.split(r"[.,;:!?]", after, maxsplit=1)[0].strip()
    next_word = after.split()[0].lower() if after else ""
    if next_word and next_word not in _THE_PLACE_STANDS_ALONE:
        return "", ""
    word = " ".join(asked.group("who").lower().split())
    return ("young" if word in _THE_YOUNGER_END else "old"), word


def _the_child_ages_on_file(memory):
    found = []
    for entry in others(memory):
        if not isinstance(entry, dict):
            continue
        who = str(entry.get("who") or "").lower()
        if CHILD_OF.get(who, who.rstrip("s")) not in CHILD and who not in CHILD:
            continue
        turns = str(entry.get("turns") or "")
        if isinstance(entry.get("age"), int):
            found.append((who, entry["age"], turns))
        for age in entry.get("ages") or []:
            if isinstance(age, int):
                found.append((who, age, turns))
    return found


def _the_place_word_filed(memory, low):
    end, word = _the_place_end(low)
    if not end:
        return ""
    if not word:
        return ""
    ages = _the_child_ages_on_file(memory)
    if not ages:
        return ""
    ages.sort(key=lambda one: one[1])
    who, age, turns = ages[0] if end == "young" else ages[-1]
    if age in [one[1] for one in ages[:-1] if end == "old"]:
        return ""
    return _one_age(word, age, turns)


PET_ASK = re.compile(r"\b(?:my|our|the)\s+(" + PET_WORDS + r")s?\b", re.I)


BREED_ASK = re.compile(r"\b(?:my|our|the)\s+(?:" + breeds.BREED_RE.pattern + r")\b", re.I)


_PET_WORD = re.compile(r"\b(?:" + PET_WORDS + r")s?\b|" + breeds.BREED_RE.pattern, re.I)


def _pet_ages(memory):
    return [pet for pet in (user(memory).get("pets") or [])
            if isinstance(pet, dict) and isinstance(pet.get("age"), int)]


def the_pronoun_said_with_a_name(memory, age):
    if not isinstance(age, int):
        return None
    aged = [pet for pet in _pet_ages(memory) if pet.get("age") == age]
    if len(aged) != 1:
        return None
    return _pet_ages_sentence([aged[0]])


def _pet_age_reply(memory, low):
    pets = [pet for pet in (user(memory).get("pets") or []) if isinstance(pet, dict)]
    asked = []
    animal = PET_ASK.search(low)
    family = _animal_family(animal.group(1)) if animal else ""
    if not family:
        breed = BREED_ASK.search(low)
        if breed:
            family = _animal_family(breeds.the_kind_of(breed.group(0).split()[-1]))
    if family:
        asked = [pet for pet in pets if _animal_family(pet.get("animal")) == family]
        if not asked:
            return ("You haven't told me about "
                    + ("an" if family[:1] in "aeiou" else "a") + " " + family + ".")
    else:
        for pet in reversed(pets):
            name = str(pet.get("name") or "").strip()
            if len(name) > 2 and re.search(r"\b" + re.escape(name.lower()) + r"\b", low):
                asked.append(pet)
    if not asked and re.search(r"\b(?:she|he|it|they|his|her|its|their)\b", low):
        aged = _pet_ages(memory)
        if aged:
            asked = aged
    if not asked:
        return None
    aged = [pet for pet in asked if isinstance(pet.get("age"), int)]
    if not aged:
        family = _animal_family(asked[0].get("animal"))
        if len(asked) > 1 or int(asked[0].get("count") or 1) > 1:
            return "You haven't told me how old your " + family + "s are."
        return "You haven't told me how old " + _pet_named(asked[0]) + " is."
    said = _pet_ages_sentence(aged)
    if _same_as_last(said, memory):
        return "Still " + " and ".join(_a_pet_age(pet) for pet in aged[:4]) + "."
    return said


PLURAL_ANIMAL = re.compile(r"s$", re.I)


def _pet_named(pet):
    name = str(pet.get("name") or "").strip()
    if name:
        return _tidy_name(name)
    animal = str(pet.get("breed") or pet.get("animal") or "").strip()
    if animal and not PLURAL_ANIMAL.search(animal):
        return "your " + animal
    return "your " + _animal_family(animal)


def _a_pet_age(pet):
    unit = str(pet.get("unit") or "")
    return str(pet["age"]) + ((" " + unit + " old") if unit else "")


def _pet_ages_sentence(pets):
    parts = []
    for pet in pets[:4]:
        who = _pet_named(pet)
        verb = " are " if who.startswith("your ") and who.endswith("s") else " is "
        parts.append(who + verb + _a_pet_age(pet))
    said = parts[0]
    for part in parts[1:]:
        said += " and " + part
    return said[0].upper() + said[1:] + "."


def _one_age(who, age, turns="", to_come=None, held=""):
    if held:
        name = str(held)[:1].upper() + str(held)[1:]
    elif who in PRONOUN_PEOPLE:
        name = who
    else:
        name = ("your " + who) if who else "they"
    plural = not held and (who.endswith("s") or not who or who in ("they", "them"))
    if turns and isinstance(to_come, int) and to_come != age:
        said = name + (" are " if plural else " is ") + str(age) + ", and turns " + str(to_come) \
            + " " + turns
    elif turns:
        said = name + (" turn " if plural else " turns ") + str(age) + " " + turns
    else:
        said = name + (" are " if plural else " is ") + str(age)
    return said[0].upper() + said[1:] + "."


def _just_gave_an_age(memory):
    return bool(AGE_SAID.search(str(last_bot(memory) or "").strip()))


MANY_OF_THEM = {"child": "children", "grandchild": "grandchildren", "baby": "babies",
                "person": "people", "woman": "women", "man": "men"}
ALREADY_MANY = frozenset(MANY_OF_THEM.values())


def _the_many(who):
    word = str(who or "").strip().lower()
    if not word:
        return ""
    if word in MANY_OF_THEM:
        return MANY_OF_THEM[word]
    if word in ALREADY_MANY or word.endswith("s"):
        return word
    if word.endswith("y") and word[-2:-1] not in "aeiou":
        return word[:-1] + "ies"
    return word + "s"


def _ages_sentence(told):
    groups = []
    for who, age, turns, to_come, held in told[:4]:
        for group in groups:
            if group[0] == who and group[4] == held and not group[2] and not turns:
                group[1].append(age)
                break
        else:
            groups.append([who, [age], turns, to_come, held])
    parts = []
    for who, ages, turns, to_come, held in groups:
        if len(ages) == 1:
            parts.append(_one_age(who, ages[0], turns, to_come, held).rstrip("."))
            continue
        name = ("your " + _the_many(who)) if who else "they"
        said = ", ".join(str(age) for age in ages[:-1])
        parts.append(name + " are " + said + " and " + str(ages[-1]))
    parts = parts[:1] + [(part[:1].lower() + part[1:]) if not any(
        group[4] and part.startswith(str(group[4])[:1].upper()) for group in groups)
        else part for part in parts[1:]]
    if len(parts) == 1:
        return (parts[0][0].upper() + parts[0][1:]) + "."
    said = ", ".join(parts[:-1]) + " and " + parts[-1]
    return said[0].upper() + said[1:] + "."


def _ask_gender(low):
    if re.search(r"\b(?:she|her|hers)\b", str(low or "")):
        return "she"
    if re.search(r"\b(?:he|him|his)\b", str(low or "")):
        return "he"
    return ""


def _called(name):
    if not isinstance(name, str) or not name:
        return ""
    words = name.replace(".", " ").split()
    if not words:
        return ""
    if len(words) > 1:
        return " ".join(word[0].upper() + word[1:] for word in words)
    return words[0][0].upper() + words[0][1:]


def _every_line(memory):
    if not isinstance(memory, dict):
        return []
    return [turn for turn in (memory.get("turns") or []) if isinstance(turn, dict)]
