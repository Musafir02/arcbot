import re

LEAVING = "leaving"

_A_SIGN_OFF = re.compile(
    r"\b(?:(?:catch|see)\s+(?:you|ya|u)\b|(?:talk|speak|chat)(?:ing)?\s+"
    r"(?:to\s+)?(?:you|ya|u)\b|(?:c\s*u|c\s*ya)\b)")
_A_LEAVE_TIME = re.compile(
    r"\b(?:(?:at|around|about)\s+(?:about\s+|around\s+|half\s+)?\d{1,2}(?::\d{2})?\s*"
    r"(?:am|pm|o'?clock)?"
    r"|(?:at|around|about)\s+(?:about\s+|around\s+|half\s+)?(?:one|two|three|four|five|six|seven|"
    r"eight|nine|ten|eleven|twelve)\b"
    r"|at\s+(?:lunch|lunchtime|teatime|breakfast|break)\b"
    r"|after\s+(?:work|school|college|uni|university|lunch|tea|dinner|the\s+school\s+run)\b"
    r"|on\s+(?:monday|tuesday|wednesday|thursday|friday|saturday|sunday|mon|tues|weds|thurs"
    r"|fri|sat|sun)\b"
    r"|this\s+(?:evening|afternoon|weekend)\b|next\s+week\b|at\s+the\s+weekend\b"
    r"|in\s+the\s+(?:morning|afternoon|evening)\b"
    r"|in\s+(?:a\s+)?(?:bit|while|minute|sec|second|mo|moment)\b)")


_GOING_VERB = (r"(?:go|get\s+off|get\s+going|be\s+off|be\s+going|head\s+off|shoot|shoot\s+off"
               r"|run|dash|fly)")

_LEAVE = re.compile(
    r"\b(?:"
    r"(?:got|gotta|have|has|need|needs|better|best|must|ought|should)\s+(?:to\s+)?"
    + _GOING_VERB +
    r"|(?:i'?m|im|i\s+am|we'?re|we\s+are|i'?ll|ill)\s+(?:gonna|going\s+to)\s+"
    r"(?:go|be\s+off|head\s+off|shoot(?:\s+off)?|get\s+off)\b"
    r"|(?:i'?m|im|i\s+am|we'?re|we\s+are)\s+(?:just\s+)?(?:gonna\s+|going\s+to\s+)?"
    r"(?:turn(?:ing)?\s+in|going\s+up\s+to\s+bed|signing\s+off|up\s+to\s+bed)\b"
    r"|(?:i'?m|im|i\s+am)\s+(?:gonna\s+|going\s+to\s+|just\s+)?"
    r"(?:get|getting)\s+(?:some\s+)?(?:kip|kips|shut\s?eye|shuteye|sleep)\b"
    r"|(?:i'?m|im|i\s+am|we'?re|we\s+are)\s+(?:just\s+|probably\s+)?"
    r"(?:having|going\s+to\s+have|off\s+for|going\s+for)\s+an\s+early\s+(?:night|one)\b"
    r"|(?:(?:an\s+)?early\s+night)\b"
    r"|(?:time\s+for\s+an\s+early\s+night)\b"
    r"|(?:^just\s+having\s+an\s+early\s+(?:night|one))\b"
    r"|(?:i'?m|im|i\s+am|we'?re|we\s+are)\s+(?:just\s+)?(?:going\s+to\s+|gonna\s+)?"
    r"(?:get|getting)\s+my\s+head\s+down\b"
    r"|(?:i'?m|im|i\s+am)\s+(?:just\s+)?(?:heading|going)\s+up\s+to\s+(?:my\s+)?bed\b"
    r"|(?:i'?m|im|i\s+am)\s+(?:just\s+)?(?:going\s+to\s+|gonna\s+)?try\s+(?:and\s+|to\s+)"
    r"(?:sleep|get\s+some\s+sleep)\b"
    r"|(?:time\s+to\s+turn\s+in)\b"
    r"|(?:bed\s*o'?\s*clock)\b"
    r"|(?:(?:it'?s|its)\s+)?sleep\s*time\b"
    r"|(?:i'?m|im|i\s+am|we'?re|we\s+are|i'?ll|ill)\s+"
    r"(?:be\s+)?(?:off|going|head(?:ing)?\s+off|shoot(?:ing)?\s+off|out\s+of\s+here"
    r"|get\s+(?:off|going))\b"
    r"|(?:i'?m|im|i\s+am|we'?re|we\s+are)\s+(?:away|out)\b"
    r"|(?:off\s+to\s+(?:bed|sleep|kip|nap|work|school|the\s+shop))\b"
    r"|(?:going\s+for\s+a\s+(?:kip|nap|lie\s+down))\b"
    r"|(?:hitting\s+the\s+hay)\b"
    r"|(?:(?:bed|bed\s*time)\s+for\s+(?:me|us))\b"
    r"|(?:bed\s*time)\b"
    r"|(?:call(?:ing)?\s+it\s+a\s+night)\b"
    r"|(?:^going\s+up\s+to\s+(?:my\s+)?bed)\b"
    r"|(?:^just\s+going\s+up\s+to\s+(?:my\s+)?bed)\b"
    r"|(?:\bgood\s?night\b|\bgood\s?nite\b|\bnite\b|\bnight\b)"
    r"|(?:get(?:ting)?\s+out\s+of\s+your\s+hair)\b"
    r"|(?:time\s+(?:for\s+me\s+)?to\s+(?:go|head\s+off|be\s+off|shoot(?:\s+off)?))\b"
    r"|(?:(?:that'?s|thats)\s+me\s+(?:away|off|out|done))\b"
    r"|(?:let\s+you\s+go|leave\s+you\s+to\s+it|leave\s+you\s+be|let\s+you\s+get\s+on"
    r"|let\s+you\s+get\s+back|stop\s+bothering\s+you)\b"
    r"|(?:talk|speak|chat)(?:ing)?\s+(?:to\s+you\s+)?(?:later|soon|tomorrow)\b"
    r"|(?:talk|speak|chat)(?:ing)?\s+(?:to\s+you\s+)?(?:" + _A_LEAVE_TIME.pattern + r")"
    r"|(?:catch|see)\s+(?:you|ya)\b"
    r"|(?:time\s+(?:for\s+me\s+)?to\s+go)\b"
    r"|(?:that'?s|thats)\s+(?:me\s+)?done\b"
    r"|(?:that'?s|thats)\s+it\s+from\s+me\b"
    r"|(?:i'?m|im|i\s+am)\s+done\s+for\s+(?:the\s+)?(?:day|today|now)\b"
    r"|(?:time\s+(?:i\s+was\s+off|(?:for\s+)?(?:my\s+)?bed))\b"
    r"|(?:need|needs)\s+my\s+bed\b"
    r"|(?:my\s+bed'?s?\s+calling)\b"
    r")")

_A_DAY_AHEAD = re.compile(
    r"\b(?:tomorrow|tonight|on\s+(?:monday|tuesday|wednesday|thursday|friday|saturday|sunday|mon"
    r"|tues|weds|thurs|fri|sat|sun)\b|next\s+(?:week|weekend|month|monday|tuesday|wednesday"
    r"|thursday|friday|saturday|sunday)|this\s+(?:evening|afternoon|weekend)|in\s+the\s+"
    r"(?:morning|afternoon|evening)|later\b|after\s+(?:work|school|college|uni|university"
    r"|lunch|tea|dinner|the\s+school\s+run)\b)")

_WISH = re.compile(
    r"^(?:ok |okay |right |well |and |so |cheers |thanks |thank you |nice |great |bye )*"
    r"(?:"
    r"(?:i )?hope (?:you )?(?:have )?(?:a |an )?"
    r"(?:really |very |lovely |nice |great |good |safe |smashing |brilliant |restful )*"
    r"(?:day|evening|weekend|week|night|one|time|holiday|christmas|break|rest|trip|journey)\b"
    r"|(?:you )?have (?:a |an )?"
    r"(?:really |very |lovely |nice |great |good |safe |smashing |brilliant |restful )*"
    r"(?:day|evening|weekend|week|night|one|time|holiday|christmas|break|rest|trip|journey)\b"
    r"|(?:i )?hope (?:that )?(?:you\b[^.!?,;]{0,30}?"
    r"|your (?:day|evening|weekend|week|night|lunch|dinner|meal|shift|rest|break|time|one|trip"
    r"|journey|holiday)\b[^.!?,;]{0,30}?)"
    r"(?:well|better|good|great|lovely|nice|fine|okay|smoothly|easily|restful|fun)\b"
    r"|(?:you )?have (?:a )?(?:good )?fun\b"
    r"|(?:you )?enjoy (?:a |an )?(?:good|great|nice|lovely|fun|happy) "
    r"(?:day|evening|weekend|week|night|time|one|trip|journey|holiday|break|shift|lunch|dinner"
    r"|meal|party)\b"
    r"|(?:you )?enjoy (?:your|the) "
    r"(?:day|evening|weekend|night|lunch|dinner|meal|party|trip|holiday|break|shift|rest|"
    r"bath|walk|flight)\b"
    r"|get well soon\b"
    r"|(?:you )?feel better(?: soon)?\b"
    r"|(?:you )?sleep (?:well|tight)\b"
    r"|(?:you )?take care\b"
    r"|all the best\b"
    r"|best wishes\b|best regards\b|(?:kind|warm) regards\b"
    r"|best of luck\b"
    r"|(?:good )?luck\b"
    r"|look after yourself\b"
    r"|laters\b|laterz\b"
    r")")
_WISH_ALLOWED = frozenset((
    "then", "now", "too", "both", "all", "and", "you", "thanks", "thank", "cheers", "bye",
    "byebye", "goodbye", "ok", "okay", "right", "well", "so", "x", "xx", "xxx", "mate", "guys",
    "folks", "everyone", "of", "yourself", "it", "to", "for", "the", "a", "have", "nice", "one",
    "at", "with", "in", "on", "work", "school", "class", "shift", "tonight", "tomorrow",
    "today", "soon", "away", "party", "interview", "meeting", "appointment", "exam", "test",
    "flight", "drive", "game", "match", "christmas", "new", "year", "your", "both", "as",
    "well", "everything", "feeling", "day", "night", "weekend", "trip", "journey", "home",
    "break", "lunch", "dinner", "meal", "rest", "sleep", "fun", "safe", "early", "late",
))

_ALLOWED = frozenset((
    "ok", "okay", "right", "well", "anyway", "anyways", "alright", "oh", "so", "yeah", "yes",
    "and", "but", "sorry", "thanks", "thank", "ta", "hi", "hey", "listen", "look", "mm", "mhm",
    "i", "im", "ill", "id", "we", "us", "me", "you", "my", "the", "a", "an", "to", "for", "bit",
    "little", "while", "second", "minute", "sec", "now", "then", "soon", "later", "tonight",
    "today", "tomorrow", "morning", "night", "nite", "bed", "sleep", "work", "shop", "it",
    "home", "early", "one", "think",
    "day", "the", "that", "should", "gonna",
    "i'd", "i'll", "i'm", "i've", "we'd", "we'll", "we're", "it's", "that's",
    "love", "luv", "hun", "honey", "sweetheart", "mate", "folks", "xx", "x", "xxx",
    "kip", "nap", "let",
    "just", "about", "off",
))

_OPENS_QUESTION = re.compile(
    r"^(?:can|could|should|shall|do|does|did|is|are|was|were|will|would|may|might|must|"
    r"what|when|where|why|how|who|which|whose|if|whether)\b")
_ASKS = re.compile(r"\b(?:what|whats|why|whys|how|hows|when|whens|where|wheres|who|whos|"
                   r"which|should|do|does|did|can|could|would|will)\b")
_ASKS_ANYWHERE = re.compile(
    r"\b(?:any\s+(?:idea|ideas|tips?|advice|suggestions?|chance|thoughts?|clue|pointers?)"
    r"|is\s+there|are\s+there|tell\s+me|do\s+you\s+know|can\s+you|could\s+you"
    r"|what\s+do\s+you|how\s+do\s+i|what\s+should\s+i|wondering\s+if|if\s+you\s+could"
    r"|what\s+about|how\s+about)\b")
_ASKS_OPENER = re.compile(
    r"^(?:can|could|should|shall|do|does|did|is|are|was|were|will|would|may|might|must|"
    r"what|whats|when|where|why|how|hows|who|whos|which|whose)\b")
_KEEPS = re.compile(r"\b(?:dont|don't|doesnt|doesn't|didnt|didn't|not|wont|won't|never)\b"
                    r"[^,.;]{0,24}\b(?:go|going|leave|off)\b")
_SPLIT = re.compile(r"\s*(?:[,;!?]|(?<!\d)\.|\.(?!\d)| - | -- |\bbut\b)\s*")

POOL = (
    "Go well, and see you when you're back.",
    "Right, take it easy. Look after yourself.",
    "No worries at all. Mind yourself.",
    "Bye for now — mind how you go.",
    "All the best — talk soon.",
)
NIGHT_GOODBYE_POOL = (
    "Night then. Sleep well.",
    "Goodnight - sleep well.",
    "Night night. Sleep well.",
    "Right - goodnight, and sleep well.",
    "Night. Sleep well, and I'll be here tomorrow.",
)
_NOT_A_BEDTIME = re.compile(r"\b(?:shift|shifts|bus|buses|duty|class|classes|out|club|feeds?|"
                            r"mare|terrors?|nurse|nursing|porter|stock)\b")
_NITE = re.compile(r"\b(?:good\s?night|good\s?nite|nite|night|bed|bedtime|kip|hay|"
                   r"sleep|sleeping|turn(?:ing)?\s+in|head\s+down|shut\s?eye|\blie\s+down)\b")
REASON_POOL = (
    "Go on then — that comes before me. Take care.",
    "Fair enough, that matters more. Look after yourself.",
    "Of course. Go and see to it, and mind yourself.",
    "That first, definitely. Come back when you have a minute.",
)


def _clauses(clean):
    return [part.strip() for part in _SPLIT.split(clean) if part.strip()]


_THANKS_WORDS = frozenset((
    "thanks", "thank", "you", "for", "listening", "listened", "that", "helps", "helped", "so",
    "much", "a", "lot", "the", "chat", "talk", "talking", "it", "all", "help", "again", "was",
    "really", "useful", "advice", "everything", "mate", "and", "i", "appreciate", "means",
))


_RUN_UP = _ALLOWED | _THANKS_WORDS | frozenset(("ok", "okay", "right", "then", "your", "my",
                                                 "our", "much"))


_SIGN_OFF_WORDS = frozenset((
    "bye", "byebye", "goodbye", "later", "laters", "laterz", "night", "goodnight", "nite",
    "cheers", "ttfn", "ttyl", "cheerio", "tara", "adios", "nighty", "nites",
    "ok", "okay", "right", "well", "thanks", "thank", "you", "ta", "so", "and", "now", "then",
    "anyway", "anyways", "alright"))


_SIGN_OFF_VOCATIVE = frozenset((
    "all", "everyone", "everybody", "folks", "guys", "love", "luv", "hun", "honey",
    "sweetheart", "mate", "xx", "x", "xxx", "too", "bella", "pet", "duck", "chick", "pal",
))


def _is_sign_off(clause):
    words = [word for word in re.findall(r"[a-z']+", clause)
             if word not in _SIGN_OFF_VOCATIVE]
    return bool(words) and all(word in _SIGN_OFF_WORDS for word in words)


_END_SIGN_OFF = re.compile(r"\b(?:bye|byebye|goodbye|cheerio|tara|night|goodnight|nite|laters"
                           r"|night\s+night|nite\s+nite|ttfn|ttyl|adios|nighty|nites)\b\s*"
                           r"(?:all|everyone|everybody|folks|guys|too|love|hun|mate|bella|pet"
                           r"|duck|chick|pal)?\s*$")
_END_SIGN_OFF_KEEP = frozenset((
    "ok", "okay", "right", "well", "so", "and", "then", "now", "for", "all", "everyone",
    "love", "luv", "hun", "honey", "sweetheart", "mate", "guys", "folks", "xx", "x", "xxx",
    "night", "nite", "good", "bye", "byebye", "goodbye", "cheerio", "tara", "laters", "you",
    "your",
    "i", "im", "we", "us", "me", "my", "the", "a", "an", "is", "be", "to", "have", "had",
))


def _ends_in_a_sign_off(clause):
    match = _END_SIGN_OFF.search(clause)
    if not match:
        return False
    head = clause[:match.start()].strip()
    words = re.findall(r"[a-z']+", head)
    return all(word in _END_SIGN_OFF_KEEP for word in words)


def _is_thanks_clause(clause):
    words = re.findall(r"[a-z']+", clause)
    return bool(words) and all(word in _THANKS_WORDS for word in words)


_UNWELL = re.compile(
    r"\b(?:"
    r"sick|ill|poorly|unwell|hurts?|hurting|ached?|aches|aching|pain(?:ful)?|sore|stiff"
    r"|headache|migraines?|toothache|cramps?|cramping|fever|temperature|vomit(?:ing|ed)?"
    r"|throwing\s+up|threw\s+up|nausea|nauseous|dizzy|faint|flu|infection|cough(?:ing)?"
    r"|rash|swollen|swelling|bleed(?:ing)?|blister(?:s|ed)?|stomach|diarr?hoea"
    r")\b")
_HURTING = re.compile(r"\b(?:kill(?:s|ing)?(?:\s+(?:me|my))?|agony|agonis(?:ing)?|agoniz(?:ing)?"
                     r"|throbbing|thumping|banging|pounding|hammering|splitting|stinging|burning"
                     r"|on\s+fire|in\s+bits|hurts?|hurting|aching|aches?|sore|stiff|tender"
                     r"|twinge|swollen|killing\s+me)\b")
_BODY = re.compile(r"\b(?:head|heads|throat|ear|ears|eye|eyes|tooth|teeth|back|backs|knee|knees"
                   r"|shoulder|shoulders|arm|arms|leg|legs|foot|feet|ankle|ankles|wrist|wrists"
                   r"|neck|hip|hips|toe|toes|hand|hands|finger|fingers|chest|stomach|belly|skin"
                   r"|jaw|sinus|sinuses|gum|gums|elbow|elbows|shin|shins|thigh|thighs)\b")


def _reads_as_a_body_complaint(clause):
    return bool(_BODY.search(clause) and _HURTING.search(clause))


def _reads_as_unwell(clause):
    return bool(_UNWELL.search(clause)) or _reads_as_a_body_complaint(clause)


_CONTRAST = re.compile(r"\b(?:but|though|although)\b")
_COMES_BACK = re.compile(
    r"\b(?:keep|keeps|keeping|kept|cant|cannot|can'?t|still|always)\b")
_MIND = re.compile(
    r"\b(?:think|thinks|thinking|thought|thoughts|worry|worried|worrying|fret|fretting|"
    r"overthink|overthinking|sleep|sleeping|asleep|awake|wake|wakes|waking|woke|dream|dreams|"
    r"dreaming|night|nights|head|heads|headache|headaches|migraine|migraines|mind|brain|"
    r"cry|crying|cried|tears|panic|panicking|stress|stressed|anxious|switching|switch)\b")
_OVERWHELM = re.compile(
    r"\b(?:i'?m|i am|i feel|im feeling|feeling|i've been feeling|ive been feeling)\s+"
    r"(?:so |really |a bit |very |totally |completely |proper )?overwhelm(?:ed|ing)\b"
    r"|\b(?:i|we) can'?t (?:keep up|take any ?more|cope any ?more|manage any ?more)\b"
    r"|\b(?:i'?m|i am|im) not coping\b|\bnot coping (?:at all|any ?more|right now)\b"
    r"|\bit'?s more than i can (?:handle|take|cope with|manage|deal with)\b"
    r"|\bmore than i can (?:handle|take|cope with|manage|deal with)\b")
_ADVERB = r"(?:still|just|really|actually|genuinely|very|so|pretty|quite|proper|sort of|kind of)"
_FEELS_ROTTEN = re.compile(
    r"\b(?:i|we)\s+(?:" + _ADVERB + r"\s+)*"
    r"feel(?:ing)?\s+(?:" + _ADVERB + r"\s+)*(?:like\s+)?(?:rubbish|rough|awful|terrible|"
    r"dreadful|poorly|crap|lousy|ill|sick|low|down|knackered|exhausted)\b")


def _a_trouble_behind_a_contrast(clean):
    if not _CONTRAST.search(clean):
        return False
    tail = " ".join(_CONTRAST.split(clean, 1)[1].split())
    if not tail:
        return False
    if _is_thanks_clause(tail) or _is_sign_off(tail) or _is_wish_clause(tail):
        return False
    if _names_their_own_trouble(tail):
        return True
    return bool(_COMES_BACK.search(tail) and _MIND.search(tail))


def _names_their_own_trouble(text):
    return bool(_OVERWHELM.search(text or "") or _FEELS_ROTTEN.search(text or ""))


_SIGN_OFF = re.compile(r"""\b(?:
    take\s+(?:it\s+easy|care)|mind\s+(?:yourself|how\s+you\s+go|out)
    |look\s+after\s+yourself|see\s+(?:you|ya)|bye|good\s+luck|all\s+the\s+best
    |go\s+(?:well|safely|on\s+then|gently)|talk\s+(?:soon|later|tomorrow)|catch\s+you
    |come\s+back|be\s+safe|get\s+home\s+safe|on\s+your\s+way|off\s+you\s+go
    |(?:let|leave)\s+you\s+(?:to\s+it|go)|safe\s+home|enjoy\s+(?:it|yourself|the\s+\w+)
    |have\s+(?:a|an)\s+(?:good|nice|great|lovely)\s+\w+
    |hope\s+(?:it|that|work|the\s+\w+)\s+(?:goes|went|is)\s+well
)\b""", re.X)


def reads_as_a_sign_off(reply):
    return bool(_SIGN_OFF.search(" ".join(str(reply or "").lower().split())))


def _is_wish_clause(clause):
    match = _WISH.search(clause)
    if not match:
        return False
    rest = re.findall(r"[a-z']+", clause[match.end():])
    return all(word in _WISH_ALLOWED for word in rest)


_LEAVE_SHORTHAND = frozenset(("ttyl", "talklater", "gtg", "g2g", "cya", "l8r", "l8tr", "n8",
                              "xx", "xxx"))


def _is_leave_clause(clause):
    if _is_wish_clause(clause):
        return True
    if _ends_in_a_sign_off(clause):
        return True
    if not _LEAVE.search(clause):
        return False
    if _AWAY_OUT.search(clause) and _AWAY_PLAN.search(clause):
        return False
    if _BED_LEAVE.search(clause) and _NEXT_DAY.search(clause):
        return False
    rest = _LEAVE.sub(" ", clause)
    downs = _ALLOWED | _SIGN_OFF_WORDS | _LEAVE_SHORTHAND | _SIGN_OFF_VOCATIVE
    if all(word in downs for word in re.findall(r"[a-z']+", rest)):
        return True
    if not _A_SIGN_OFF.search(clause):
        return False
    trimmed = _A_LEAVE_TIME.sub(" ", rest)
    return trimmed != rest and all(word in downs for word in re.findall(r"[a-z']+", trimmed))


def reads_as_leaving(clean, words=None):
    return _reads_as_leaving(clean, words)


def reads_as_a_leave_with_a_body_in_it(clean, words=None):
    return not reads_as_leaving(clean, words) and _reads_as_leaving(clean, words, unwell_blocks=False)


def reads_as_a_leave_with_a_trouble_in_it(clean, words=None):
    return (not reads_as_leaving(clean, words)
            and _reads_as_leaving(clean, words, trouble_blocks=False))


def _reads_as_leaving(clean, words=None, unwell_blocks=True, trouble_blocks=True):
    clean = " ".join(str(clean or "").lower().split())
    if not clean or "?" in clean:
        return False
    if _OPENS_QUESTION.match(clean) or _KEEPS.search(clean):
        return False
    if trouble_blocks and _a_trouble_behind_a_contrast(clean):
        return False
    clauses = _clauses(clean)
    if not clauses:
        return False
    if len(clauses) == 1:
        return _is_leave_clause(clauses[0])
    if any(_asks_something(clause) for clause in clauses):
        return False
    first, last = clauses[0], clauses[-1]
    if _is_leave_clause(first):
        rest = " ".join(clauses[1:])
        return (not _ASKS.search(rest) and not (unwell_blocks and _reads_as_unwell(rest))
                and not (trouble_blocks and _names_their_own_trouble(rest)))
    if _is_leave_clause(last):
        return True
    for index, clause in enumerate(clauses[1:-1], start=1):
        if not _is_leave_clause(clause):
            continue
        before = " ".join(clauses[:index])
        after = " ".join(clauses[index + 1:])
        if _ASKS.search(after) or (unwell_blocks and _reads_as_unwell(after)):
            continue
        if before and not (_is_filler(before) or _is_thanks_clause(before)):
            continue
        return True
    return False


_AWAY_OUT = re.compile(r"\b(?:i'?m|im|i\s+am|we'?re|we\s+are)\s+(?:off|away|out)\b")
_AWAY_PLAN = re.compile(
    r"\b(?:next\s+(?:week|month|year|weekend)|this\s+(?:weekend|evening|afternoon)"
    r"|tonight|tomorrow|on\s+(?:monday|tuesday|wednesday|thursday|friday|saturday|sunday)"
    r"|at\s+the\s+weekend|for\s+the\s+weekend|in\s+(?:june|july|august|september|october"
    r"|november|december|january|february|march|april|may))\b")


_BED_LEAVE = re.compile(r"\b(?:early\s+(?:night|one)|head\s+down|heading\s+up\s+to\s+bed"
                        r"|try\s+(?:and\s+|to\s+)sleep)\b")

_NEXT_DAY = re.compile(
    r"\b(?:tomorrow|tomorra|tmrw|tmoz|next\s+(?:week|month|year|weekend)"
    r"|on\s+(?:monday|tuesday|wednesday|thursday|friday|saturday|sunday))\b")


_AWAY = re.compile(r"\b(?:i'?m|im|i am|we'?re|were|we are)\s+(?:off|away)\b"
                   r"|\b(?:i'?m|im|i am)\s+(?:heading|setting) off\b")


def _asks_something(clause):
    clause = " ".join(str(clause or "").lower().split())
    if not clause:
        return False
    if "?" in clause:
        return True
    return bool(_ASKS_OPENER.match(clause) or _ASKS_ANYWHERE.search(clause))


def _is_filler(clause):
    words = re.findall(r"[a-z']+", clause)
    return bool(words) and all(word in _RUN_UP for word in words)


WISH_POOL = (
    "Thanks — that's kind. Same to you.",
    "Ta. You too — look after yourself.",
    "Thanks, and the same back to you.",
    "Cheers. Hope it goes well for you too.",
    "Thank you — you too.",
)
WELL_POOL = (
    "Thanks — that's kind of you. I'm well, and I hope you are too.",
    "Nothing wrong with me, but thank you. Look after yourself.",
    "That's kind. I'm fine — and I hope you are too.",
)
CRISIS_POOL = (
    "That's kind of you — but you're the one I'm thinking about. How are you doing right now?",
    "Thank you, and I mean it. Never mind me — how is it now?",
    "That's kind. I'm all right, and I'd rather stay with you. What is happening right now?",
)
KINDER_POOL = (
    "Thanks — and I hope it eases soon.",
    "Ta. Same to you — and I hope you feel better soon.",
    "Thank you — and I hope whatever it is lets up a bit.",
    "Thanks, and I hope you are feeling better soon.",
)
NIGHT_POOL = (
    "Thanks — and the same to you. Sleep well.",
    "Ta. You too — get a good night.",
    "Thank you. And I hope you sleep well too.",
)
OWN_NEWS_POOL = (
    "Never mind me — what's happening with you?",
    "Ah, that matters more than me. Tell me about it.",
    "Then the wish can wait — what's going on?",
    "Forget the wish for a second. How is it going?",
)
_NIGHT = re.compile(r"\b(?:sleep|sleeping|bed|bedtime|night's sleep|goodnight)\b|\bnight\b")
_WELL = re.compile(r"\b(?:get well|feel better|well soon)\b")
_WISH_THING = re.compile(
    r"\b(?:day|evening|weekend|week|night|lunch|dinner|meal|party|trip|journey|holiday|break|"
    r"shift|rest|bath|walk|flight|fun|well|better|tomorrow|tonight|today|sleep|tight|bed)\b"
    r"|\bwith (?:the|your|it|that)\b")


def _thread_is_an_emergency(memory):
    if not isinstance(memory, dict) or not memory.get("safety_case"):
        return False
    turns = [turn for turn in (memory.get("turns") or []) if isinstance(turn, dict)]
    return bool(turns) and turns[-1].get("module") == "safety"


_UNWELL_FEELING = re.compile(
    r"\b(?:awful|terrible|dreadful|rough|rubbish|lousy|miserable|cold|chills?|sniffles"
    r"|sore throat|under the weather|poorly|poor thing)\b")


def _thread_is_unwell(memory):
    turns = [turn for turn in ((memory or {}).get("turns") or []) if isinstance(turn, dict)]
    for turn in reversed(turns[-2:]):
        line = str(turn.get("user") or "")
        if _reads_as_unwell(line) or _UNWELL_FEELING.search(line.lower()):
            return True
    return False


def _wish_pool(clean, memory=None):
    line = " ".join(str(clean or "").lower().split())
    if _thread_is_an_emergency(memory):
        return CRISIS_POOL
    if _thread_is_unwell(memory):
        return KINDER_POOL
    if _WELL.search(line):
        return WELL_POOL
    if _NIGHT.search(line):
        return NIGHT_POOL
    return WISH_POOL


def pool(clean, words=None, unwell_blocks=True, memory=None, trouble_blocks=True):
    if not _reads_as_leaving(clean, words, unwell_blocks, trouble_blocks):
        return None
    clauses = _clauses(" ".join(str(clean or "").lower().split()))
    wishes = [clause for clause in clauses if _is_wish_clause(clause)]
    if wishes and not _WISH_THING.search(" ".join(wishes)):
        wishes = []
    leaving_too = any(_is_leave_clause(clause) and not _is_wish_clause(clause)
                      for clause in clauses)
    own_news = [clause for clause in clauses
                if not _is_wish_clause(clause) and not _is_leave_clause(clause)
                and not _is_filler(clause) and not _is_thanks_clause(clause)
                and not _is_sign_off(clause)]
    opens_with_a_wish = bool(clauses) and bool(wishes) and _is_wish_clause(clauses[0]) \
        and bool(_WISH_THING.search(clauses[0]))
    going_away = any(_AWAY.search(clause) for clause in own_news)
    if wishes and not leaving_too and not going_away:
        if own_news and opens_with_a_wish:
            return OWN_NEWS_POOL
        if own_news:
            return None
        return _wish_pool(" ".join(wishes), memory)
    for index, clause in enumerate(clauses):
        if not _is_leave_clause(clause):
            continue
        leave_pool = NIGHT_GOODBYE_POOL if _is_a_bedtime(clause) else POOL
        after = " ".join(clauses[index + 1:])
        rest = clauses[index + 1:]
        if rest and any(not (_is_thanks_clause(part) or _is_sign_off(part)
                             or _is_wish_clause(part) or _is_leave_clause(part))
                        for part in rest):
            if _A_DAY_AHEAD.search(clause):
                return leave_pool
            if _a_state_not_an_errand(rest):
                return leave_pool
            return REASON_POOL
        return leave_pool
    return NIGHT_GOODBYE_POOL if _is_a_bedtime(" ".join(clauses)) else POOL


_OWN_STATE = re.compile(
    r"\b(?:tired|shattered|knackered|exhausted|worn\s+out|done\s+in|wrecked|cream\s+crackered|"
    r"dead\s+on\s+my\s+feet|sleepy|drowsy|sleepless|no\s+sleep|broken\s+night|up\s+since|"
    r"early\s+start|up\s+early|early\s+shift|work\s+in\s+the\s+morning|work\s+tomorrow|"
    r"on\s+early|long\s+day|long\s+shift|busy\s+day\s+tomorrow|school\s+run|"
    r"need\s+my\s+sleep|need\s+an\s+early\s+night)\b")
_ANOTHER = re.compile(r"\b(?:he|she|they|him|her|them|his|hers|their|theirs|my\s+(?:son|daughter|"
                      r"boy|girl|kids?|child|children|mum|mom|dad|husband|wife|partner|nan|"
                      r"grandma|grandad|dog|cat|baby|mate|friend|boss)|our\s+\w+)\b")


def _a_state_not_an_errand(clauses):
    said = [clause for clause in clauses if not (_is_thanks_clause(clause)
                                                 or _is_sign_off(clause)
                                                 or _is_wish_clause(clause)
                                                 or _is_leave_clause(clause))]
    if not said:
        return False
    for clause in said:
        if not _OWN_STATE.search(clause) or _ANOTHER.search(clause):
            return False
    return True


def _is_a_bedtime(clause):
    if not clause or _NOT_A_BEDTIME.search(clause):
        return False
    return bool(_NITE.search(clause))


def lines():
    return (frozenset(POOL) | frozenset(NIGHT_GOODBYE_POOL) | frozenset(REASON_POOL)
            | frozenset(WISH_POOL)
            | frozenset(WELL_POOL) | frozenset(KINDER_POOL) | frozenset(NIGHT_POOL)
            | frozenset(CRISIS_POOL) | frozenset(OWN_NEWS_POOL))
