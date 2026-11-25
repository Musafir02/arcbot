import re

OCCASIONS = (
    (re.compile(r"\b(?:weddings?|getting married|getting wed|married|marrying|bride|groom|"
                r"bridesmaid|best man|hen do|stag do)\b"), "wedding", "a wedding"),
    (re.compile(r"\b(?:interviews?|interviewing)\b"), "interview", "an interview"),
    (re.compile(r"\b(?:first day|new job|new role|job starts?|starting (?:work|the job)|"
                r"start(?:ing)? (?:on )?monday)\b"), "work", "my new job"),
    (re.compile(r"\b(?:part(?:y|ies)|birthdays?|anniversar(?:y|ies)|housewarmings?|retirement|"
                r"celebrations?|get together)\b"), "party", "a party"),
    (re.compile(r"\b(?:funerals?|burial|cremation|wake|memorial)\b"), "funeral", "a funeral"),
    (re.compile(r"(?=[\s\S]*\b(?:mum|mom|mother|dad|father|son|daughter|sister|brother|uncle|"
                r"aunt|nan|gran|granny|grandma|grandad|grandpa|cousin|niece|nephew|friend|mate|"
                r"colleague|boss|wife|husband|partner|girlfriend|boyfriend|neighbour)\b)"
                r"(?=[\s\S]*\b(?:died|dying|passed away|passed on|bereave\w*|death|buried)\b)"),
     "funeral", "a funeral"),
    (re.compile(r"\b(?:christenings?|baptisms?|naming ceremony)\b"), "christening",
     "a christening"),
    (re.compile(r"\b(?:graduations?|graduating|prom|leavers? do)\b"), "graduation",
     "a graduation"),
    (re.compile(r"\b(?:festivals?|gigs?|concerts?|gig\b)\b"), "gig", "a gig"),
    (re.compile(r"\b(?:barbecues?|bbqs?|cookout)\b"), "barbecue", "a barbecue"),
    (re.compile(r"\b(?:dinners? out|meal out|meal at|restaurant|night out|first date|"
                r"on a date|going on a date|date night)\b"), "meal out", "a meal out"),
    (re.compile(r"\bchurch\b"), "church", "church"),
)

RELATION = re.compile(
    r"\bmy\s+(sister|brother|mum|mom|mother|dad|father|son|daughter|niece|nephew|cousin|aunt|"
    r"uncle|friend|best friend|mate|colleague|boss|partner|wife|husband|girlfriend|boyfriend|"
    r"in laws?|mother in law|father in law|grandma|grandad|nan|gran|granny)\b")

WHAT_TO_WEAR = re.compile(
    r"\b(?:what|wat)\s+(?:to|should\s+i|do\s+i|can\s+i|shall\s+i)\s+"
    r"(?:wear|put\s+on|dress)\b|"
    r"\b(?:not?\s+sure|no\s+idea|dont\s+know|do\s*n'?t\s+know|havent\s+decided|"
    r"cant\s+decide|cannot\s+decide|stuck)\s+(?:about\s+)?what\s+"
    r"(?:to\s+|i\s+(?:should\s+)?)?(?:wear|put\s+on|wearing)\b"
)

PART = re.compile(
    r"\b(?:shoes?|heels?|trainers?|boots?|sandals?|flats?|dress|dresses|suit|suits|shirt|blouse|"
    r"top|jacket|coat|blazer|hat|fascinator|tie|bag|outfit|skirt|trousers|chinos|jumpsuit)\b")

PART_ASK = re.compile(
    r"\b(?:what|how)\s+about\b|\band\b|\bor\b|\bshould\s+i\s+(?:wear|go\s+for)\b|"
    r"\bwould\s+(?:flats|heels|boots|trainers|sandals)\b|\bis\s+it\s+ok\s+to\s+wear\b|"
    r"\bcan\s+i\s+(?:wear|get\s+away\s+with)\b|\bdo\s+i\s+need\b"
)

PUT_ON_A_THING = re.compile(
    r"\bput\s+on\s+(?:the|a|an|some|any|my|your|his|her|their|our|it)\s+([a-z']+)")

MONTHS = ("january february march april may june july august september october november december "
          "spring summer autumn winter christmas easter").split()

RECENT = 5

WORD = re.compile(r"[a-z']+")


def _recent(memory):
    if not isinstance(memory, dict):
        return []
    said = []
    for turn in reversed((memory.get("turns") or [])[-RECENT:]):
        if isinstance(turn, dict):
            text = " ".join(str(turn.get("user") or "").lower().split())
            if text:
                said.append(text)
    return said


def _an(phrase):
    return ("an " if phrase[:1] in "aeiou" else "a ") + phrase


PAST_OCCASION = re.compile(r"\b(?:had|went\s+to|been\s+to|was\s+at|were\s+at)\b")

_A_DEATH = re.compile(r"\b(?:died|dying|dead|passed\s+away|passed\s+on|death|bereave\w*|"
                      r"funerals?|buried|burial|cremation|memorial|wake)\b")


def the_occasion(memory):
    said = _recent(memory)
    for text in said:
        for pattern, _key, phrase in OCCASIONS:
            if not pattern.search(text):
                continue
            if PAST_OCCASION.search(text) and not _A_DEATH.search(text):
                continue
            who = RELATION.search(text)
            if who:
                return "my %s's %s" % (who.group(1),
                             phrase.split()[-1])
            return phrase
    return None


def _the_last_answer(memory):
    if not isinstance(memory, dict):
        return ""
    turns = [turn for turn in (memory.get("turns") or []) if isinstance(turn, dict)]
    if not turns:
        return ""
    return " ".join(str(turns[-1].get("bot") or "").lower().split())


CLOTHING_WORDS = re.compile(r"\b(?:wear|wearing|wore|clothes|outfit|dress|suit|shoes|boots|"
                           r"trainers|jacket|coat|tie|shirt|colours|colors|smart|comfortable|"
                           r"black|white|cream|navy|grey|dark)\b", re.I)


def _the_answer_already_gave_it(memory):
    last = _the_last_answer(memory)
    if not last:
        return False
    return len(set(word.lower() for word in CLOTHING_WORDS.findall(last))) >= 2


PERMISSION_ASK = re.compile(
    r"\b(?:alright|all right|ok|okay|fine|allowed|acceptable|a problem|too much)\b", re.I)

NOT_THIS = re.compile(r"\b(?:not|never|avoid|don'?t|doesn'?t|no|unless)\b", re.I)

A_COLOUR = re.compile(
    r"\b(?:black|white|cream|navy|grey|gray|blue|red|green|pink|beige|brown|charcoal|burgundy|"
    r"silver|gold|floral|patterned|light|dark)\b")


def the_sentence_answered(text, memory):
    if not isinstance(text, str):
        return None
    line = " ".join(text.lower().split()).strip(" .!,")
    if not line or len(line.split()) > 12:
        return None
    if not the_occasion(memory):
        return None
    if not (PART.search(line) or A_COLOUR.search(line)):
        return None
    if not (PART_ASK.search(line) or PERMISSION_ASK.search(line)):
        return None
    last = _the_last_answer(memory)
    if not last or len(last.split()) < 6:
        return None
    sentences = [one for one in re.split(r"(?<=[.!?])\s+", last) if one.strip()]
    if len(sentences) < 2:
        return None
    words = sorted(set(A_COLOUR.findall(line))) + sorted(set(PART.findall(line)))
    for word in words:
        if not re.search(r"\b" + re.escape(word) + r"\b", last):
            continue
        for sentence in sentences:
            if re.search(r"\b" + re.escape(word) + r"\b", sentence):
                sentence = sentence.strip()
                if not sentence:
                    continue
                if sentence[0].isalpha():
                    sentence = sentence[0].upper() + sentence[1:]
                if NOT_THIS.search(sentence):
                    lead = "Careful - "
                elif NOT_THIS.search(line):
                    lead = "Then "
                else:
                    lead = "Yes - "
                return lead + sentence[0].lower() + sentence[1:]
    return None


def _names_an_occasion(text):
    return any(pattern.search(text) for pattern, _key, _phrase in OCCASIONS)


GOING_SOMEWHERE = re.compile(
    r"\b(?:to|for|at)\s+(?:a\s+|an\s+|the\s+|my\s+|our\s+)?"
    r"(?:work|school|college|uni|university|office|gym|run|jog|walk|ride|cycle|swim|shops?|"
    r"supermarket|church|bed|pub|bar|interview|meeting|shift|flight|train|beach|hike|climb|"
    r"dance|class|lesson|lessons|tennis|football|golf|rugby|netball|yoga|gig|concert|"
    r"restaurant|dinner|lunch|brunch|date|funeral|wedding|christening|baptism)\b")


def _names_its_own_outing(text):
    found = GOING_SOMEWHERE.search(text)
    if not found:
        return False
    return not _names_an_occasion(text)


def written_out(text, memory):
    if not isinstance(text, str):
        return None
    line = " ".join(text.lower().split()).strip(" .!,")
    if not line or len(line.split()) > 12:
        return None
    worn = PUT_ON_A_THING.search(line)
    if worn and not CLOTHING_WORDS.search(worn.group(1)):
        return None
    shaped = WHAT_TO_WEAR.search(line) or (PART.search(line) and PART_ASK.search(line))
    if not shaped:
        return None
    occasion = the_occasion(memory)
    if not occasion:
        return None
    if _the_answer_already_gave_it(memory):
        return None
    if _names_an_occasion(line):
        return None
    if _names_its_own_outing(line):
        return None
    if WHAT_TO_WEAR.search(line):
        return "what should i wear to %s" % occasion
    part = PART.search(line)
    if part and PART_ASK.search(line):
        if part.group(0) not in _the_last_answer(memory):
            return None
        return "what %s should i wear to %s" % (part.group(0), occasion)
    return None
