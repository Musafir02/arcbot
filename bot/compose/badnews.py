import re
try:
    from ..memory import dream as _dream
except Exception:
    _dream = None

from ..understanding.normalize import LEXICON, without_the_figure_of_speech

LIVING = (r"(?:mum|mom|mother|dad|father|gran|granny|grandma|grandad|grandpa|nana|nan|"
          r"brother|sister|son|daughter|child|baby|wife|husband|partner|boyfriend|girlfriend|"
          r"friend|mate|uncle|aunt|cousin|neighbour|neighbor|colleague|boss|teacher|ex|"
          r"dog|cat|pet|horse|rabbit|puppy|kitten|bird)")

CONDITION_OWNER = LIVING[:-1] + (r"|nephew|niece|stepson|stepdaughter|stepmum|stepdad|"
                                 r"stepmother|stepfather|grandson|granddaughter|"
                                 r"mother in law|father in law|son in law|daughter in law|"
                                 r"grandchild|grandchildren)")

_HOW_IT_IS_SAID = (
    r"died(?!\s+(?:laughing|giggling|smiling|of\s+(?:embarrassment|boredom|shame|laughter|"
    r"fear)|inside|a\s+(?:little|bit)|and\s+gone|"
    r"(?:her|his|their|my|our|your|its)\s+hair))"
    r"|dead(?!\s+(?:funny|good|nice|cheap|easy|serious|certain|jealous|tired|right|wrong|set|"
    r"on\b|beat|last\b|chuffed|proud|pleased|happy|keen|excited|thrilled|impressed|lucky|"
    r"jammy|buzzing|gutted|made\s+up|against|ahead|centre|straight|silence|giveaway|heat|calm|"
    r"in\s+(?:the\s+middle|a\s+row)|ringer|"
    r"to\s+(?:the\s+world|rights|me|us|him|her|them)\b))")
_DEATH_WORDS = (
    _HOW_IT_IS_SAID + r"|passed away|killed himself|killed herself|killed themselves|"
    r"hanged himself|hanged herself|hanged themselves|took his own life|took her own life|"
    r"took their own lives|committed suicide|suicid\w*|found dead|"
    r"passed on(?!\s+(?:the|a|an|my|his|her|their|our|your|its|it|this|that|these|those|some|all|both)\b)|"
    r"didn'?t make it(?!\s+(?:(?:to|for)\s+\w|in\s+time|on\s+time))|"
    r"did not make it(?!\s+(?:(?:to|for)\s+\w|in\s+time|on\s+time))")
_NEARLY = re.compile(r"\b(?:nearly|almost|practically|might\s+have|could\s+have|would\s+have|"
                     r"like\s+to\s+have)\b", re.I)
_AFTER_IT = re.compile(r"^\s*(?:laughing|giggling|smiling|of\s+(?:embarrassment|boredom|shame|"
                       r"laughter|fear)|to\s+(?:me|us|him|her|them)\b)", re.I)
DEATH_SAID = re.compile(rf"\b(?:{_DEATH_WORDS})\b")
OTHERS = (r"(?:boy|girl|lad|lass|kid|child|man|woman|person|someone|anyone|classmate|"
          r"schoolmate|teammate|workmate|student|pupil|neighbour|neighbor|friend|mate|fella|"
          r"guy|colleague|he|she|they|everyone|everybody)")
_CARRIES = frozenset("""is was were are am be been being has had have just also nearly almost
still of in at on to for with that who which my his her their our your its the a an and but so
then today yesterday now last this from like about after before when while if sadly tragically
unexpectedly peacefully suddenly quietly finally recently apparently presumably unfortunately
honestly basically literally obviously definitely really very""".split())
_PLACE = frozenset("""class classes year school work office team family ward house hospital
floor street town village college uni university club gym shop company firm site shift course
group nursery classroom road estate""".split())
_PERSON = frozenset(LIVING.lstrip("(?:").rstrip(")").split("|")) | frozenset(
    OTHERS.lstrip("(?:").rstrip(")").split("|"))
_WORD = re.compile(r"[a-z']+")

NEARLY = frozenset((
    "seizure", "unconscious", "overdose", "choking", "breathing", "collapsed", "hospital",
    "ambulance", "cancer", "stroke", "bleeding", "diagnosed",
))

LOST_CHANCE = (r"jobs?|work|role|position|match(?:es)?|games?|deals?|contracts?|shift|hours|"
               r"clients?|customers?|accounts?|bids?|bets?|elections?|deposits?|offers?|"
               r"interviews?|places?|spots?|funding|grants?|appeals?|races?|finals?|trials?|"
               r"orders?|bookings?|tenanc(?:y|ies)|tenders?|placement|promotion|apprenticeship")
LOST_PATTERN = (r"\b(?:i|we|he|she|they|ive|i've|my [a-z]+|our [a-z]+)\s+"
                r"(?:have\s+|had\s+)?(?:lost|losing)\s+(?:out on\s+)?"
                r"(?:the |my |our |his |her |their |your |that |this |a |an )?"
                r"(?:" + LOST_CHANCE + r")\b")

LEFT_ME = (r"(?:\b(?:he|she|they|my (?:wife|husband|partner|boyfriend|girlfriend|fianc\w*|ex))"
           r"[^.!?]{0,24}\b(?:left me|leaving me|leave me|left and|walked out|dumped me|"
           r"cheated on me)\b"
           r"(?!\s+(?:her|his|their|the|a|an|this|that|alone|be)\b))")

LEFT_ME_RE = re.compile(LEFT_ME, re.I)

PARTNER_LEFT = (
    r"\b(?:my (?:wife|husband|partner|boyfriend|girlfriend|fianc\w*|ex)|my marriage)\b"
    r"[^.!?]{0,30}?\b(?:has|have|had|just|recently|already|suddenly|now|then|finally)?\s*\bleft\b"
    r"(?=\s*(?:$|[.!?,;]|\b(?:me|us|and|but|because|so|now|already|again|too|last|this|"
    r"yesterday|today|tonight|morning|evening|week|month|year|night|day|suddenly|recently|"
    r"at\s+(?:christmas|new\s+year|the\s+weekend|easter)|in\s+\w+|"
    r"after\s+\w+|before\s+\w+|since\s+\w+)\b))")

PARTNER_LEFT_RE = re.compile(PARTNER_LEFT, re.I)


PARTNER_LEAVING = (
    r"\b(?:my (?:wife|husband|partner|boyfriend|girlfriend|fianc\w*|ex)|my marriage)\b"
    r"[^.!?]{0,30}?\b(?:is|are|was|were|keeps?|kept|been|got|has|have|says?|said|told me|"
    r"tells me|wants?|wanted|might|may|will|would|thinks?|thinking)\b[^.!?]{0,26}?"
    r"\bleav(?:e|es|ing)\b"
    r"(?!\s+(?:me\b|for\b|to\b|on\b|at\b|in\b|early\b|home\b|work\b|school\b|the\b|"
    r"her\b|his\b|their\b|a\b|an\b|this\b|that\b"
    r"|approved\b|booked\b|due\b|owing\b|remaining\b|allowance\b|entitlement\b|days?\b|"
    r"pay\b|request\b|year\b|starts?\b|begins?\b|ends?\b|cancell?ed\b|denied\b|"
    r"refused\b|pending\b|confirmed\b|carried\b|unused\b|balance\b))")

PARTNER_LEAVING_RE = re.compile(PARTNER_LEAVING, re.I)


REPORTED_LEAVING = (
    r"\b(?:he|she|they|hes|shes|theyre)\b[^.!?]{0,24}?\b(?:said|says|told me|tells me|"
    r"reckons|thinks|"
    r"keeps saying)\b"
    r"(?:\s+(?:that|he|she|they|hes|shes|theyre|he is|she is|they are))?"
    r"(?:\s+(?:is|are))?"
    r"(?:\s+(?:going|planning|thinking|wants?|wanted|wanted to|might|may|will|would|ready|"
    r"about|seriously)\b(?:\s+(?:to|of|about))?)?"
    r"\s+\bleav(?:e|es|ing)\b"
    r"(?!\s+(?:me\b|for\b|to\b|on\b|at\b|in\b|early\b|home\b|work\b|school\b|the\b|"
    r"her\b|his\b|their\b|him\b|a\b|an\b|this\b|that\b|soon\b|now\b|tonight\b|tomorrow\b|"
    r"today\b|next\b|after\b|before\b|hospital\b|care\b|rehab\b|prison\b|jail\b|"
    r"army\b|navy\b|force\b|uni\b|university\b|college\b|again\b))")

REPORTED_LEAVING_RE = re.compile(REPORTED_LEAVING, re.I)


LEFT_GONE = (r"\b(?:left me|left and|walked out|dumped me|moved out|"
             r"packed (?:her|his|their) (?:things|bags)|gone|"
             r"broke up|broken up|split up|separated|divorced)\b")
STILL_COMING = (r"\b(?:is|are|was|were|keeps?|kept|said|says|told|tells|wants?|wanted|might|"
                r"may|will|would|going|planning|thinking|decided)\b[^.!?]{0,26}?"
                r"\bleav(?:e|es|ing)\b")
STILL_HERE = (r"\b(?:still (?:live|living|here|in the house|together)|lives? with me|"
              r"under the same roof|separated but)\b")


MARRIAGE_ENDED = (
    r"\b(?:my|the)\s+(?:marriage|relationship)\b[^.!?]{0,24}?"
    r"\b(?:is|are|was|were|has|have|seems?|looks?)\b[^.!?]{0,16}?"
    r"\b(?:over|done|finished|ended)\b"
    r"(?!\s+(?:the|it|with|there|here|that|this|to|by|at|and)\b)"
    r"|\b(?:we|me\s+and\s+my\s+\w+)\b[^.!?]{0,20}?"
    r"\b(?:split\s+up|broke\s+up|broken\s+up|separated|divorced)\b"
    r"(?!\s+(?:the|a|into|over|it)\b)"
    r"|\b(?:getting|got|had|filed\s+for|asked\s+for|asking\s+for|wants?|wanted)\s+"
    r"(?:a\s+)?divorce\w*\b"
    r"(?!\s+(?:lawyer|solicitor|court|papers|settlement|money|bill|forms?)\b)")

MARRIAGE_ENDED_RE = re.compile(MARRIAGE_ENDED, re.I)

NOT_THEIRS = re.compile(
    r"\bmy\s+(?:mate|mates|friend|friends|best\s+friend|brother|sister|colleague|boss|cousin|"
    r"neighbour|neighbor|aunt|uncle|son|daughter|mum|mom|dad|mother|father|nan|gran|grandad|"
    r"parents?|family|in[-\s]?laws?|step\w+|grand\w+|landlord)\b")
PARTNER = re.compile(r"\b(?:wife|husband|partner|boyfriend|girlfriend|fianc\w*|ex)\b")

_LEAVE_THE_NOUN = re.compile(
    r"\b(?:his|her|their|my|our|your|its|the|some|any|no|annual|maternity|paternity|parental|"
    r"shared|sick|paid|unpaid|compassionate|study|garden|special|sabbatical|holiday)\s+leave\b")


def _without_the_noun_leave(said):
    return " ".join(_LEAVE_THE_NOUN.sub(" ", said).split())


def _a_leaving_at_all(said):
    said = _without_the_noun_leave(said)
    if not (LEFT_ME_RE.search(said) or PARTNER_LEAVING_RE.search(said)
            or PARTNER_LEFT_RE.search(said) or MARRIAGE_ENDED_RE.search(said)):
        return bool(REPORTED_LEAVING_RE.search(said) and not NOT_THEIRS.search(said))
    return not (NOT_THEIRS.search(said) and not PARTNER.search(said))

def reads_as_a_leaving_already_gone(clean):
    said = " ".join(str(clean or "").lower().split())
    if not _a_leaving_at_all(said):
        return False
    if re.search(STILL_HERE, said):
        return False
    return bool(re.search(LEFT_GONE, said)) and not re.search(STILL_COMING, said)


def reads_as_a_reported_leaving(clean):
    said = _without_the_noun_leave(" ".join(str(clean or "").lower().split()))
    if not REPORTED_LEAVING_RE.search(said) or NOT_THEIRS.search(said):
        return False
    return not (LEFT_ME_RE.search(said) or PARTNER_LEAVING_RE.search(said)
                or MARRIAGE_ENDED_RE.search(said))


def reads_as_the_leaving(clean):
    said = " ".join(str(clean or "").lower().split())
    return _a_leaving_at_all(said)


LEFT_PLAN = (r"\b(?:thinking (?:of|about)|thought (?:of|about)|want(?:s|ed)? to|wanting to|"
             r"going to|planning (?:on|to)|plan to|decided to|ready to|about to|meant to|"
             r"should i|shall i|do i)\s+(?:just\s+|actually\s+|really\s+)?"
             r"(?:leave|leaving|walk out on|end)\s+"
             r"(?:(?:my|our) (?:wife|husband|partner|boyfriend|girlfriend|fianc\w*|marriage|"
             r"ex|other half)|him|her|them|us)\b"
             r"|\b(?:i'?m|im|i am|we'?re|were|we are)\s+(?:just\s+|actually\s+)?"
             r"(?:leaving|walking out on)\s+"
             r"(?:my (?:wife|husband|partner|boyfriend|girlfriend|fianc\w*|ex|other half)|"
             r"him|her|them)\b(?!\s+(?:a|an|the|some|his|her|my|our)\b)")

OWN_PLAN = tuple(re.compile(pattern) for pattern in (
    r"\b(?:i'?m|im|i am|we'?re|were|we are)\s+(?:just\s+|actually\s+|finally\s+)?"
    r"(?:going to|gonna|planning to|plan to|decided to|ready to|about to|wanting to|"
    r"thinking (?:of|about)|want to)\s+(?:just\s+|actually\s+|really\s+)?"
    r"(?:leave|leaving|walk out on|end it with)\s+",
    r"\b(?:i'?m|im|i am|we'?re|were|we are)\s+(?:just\s+|actually\s+|finally\s+)?"
    r"(?:leaving|walking out on)\s+",
    r"\b(?:i|we)\s+(?:have|'ve|ve)\s+(?:decided|made up my mind)\b",
    r"\bwe(?:'?re| are)?\s+(?:going to|gonna)\s+(?:split|separate|divorce)\b",
))

SACKED_FIRED = (
    r"\b(?:i|we|he|she|they|my [a-z]+|our [a-z]+)\s*(?:just\s+|only\s+|then\s+|now\s+|today\s+)?"
    r"(?:'?ve|have|has|had|was|were|been|being|got|get|gets|getting|is|are|am)\s+"
    r"(?:been\s+|being\s+)?"
    r"(?:sacked|fired(?!\s+up\b)|dismissed)\b"
    r"|\b(?:they|he|she|the company|the firm|the shop|work|my boss|my manager|my employer)\s+"
    r"(?:just\s+)?(?:sacked|fired(?!\s+up\b)|dismissed)\s+(?:me|him|them|us)\b"
    r"|\b(?:they|the company|the firm|the shop|work|my boss|my manager|my employer)\s+"
    r"let\s+(?:me|him|her|them)\s+go\b(?!\s+(?:home|early|out|to|and|for a)\b)"
    r"(?!\s+on\s+(?:holiday|strike|leave|a\b|the\b|maternity|paternity|benefit|tour|safari))"
    r"|\b(?:got|gotten|gave me|handed me|give me)\s+the (?:sack|boot|push)\b(?!\s+of\b)")

ADOPTION_WORDS = r"\b(?:adopt\w*|adoption)\b"

BAD_NEWS_ITSELF = tuple(re.compile(pattern) for pattern in (
    r"\b(?:diagnos\w+|cancer|chemo\w*|tumou?r|biopsy)\b",
    r"(?<!\bwork )(?<!\bworks )(?<!\bworked )\bin (?:the )?hospitals?\b",
    r"\b(?:a&e|icu|ambulances?|overdose|surgery|operation|anaesthetic)\b",
    r"\b(?:strokes?|heart attacks?|seizures?|chest pains?)\b",
    r"\bcan'?t keep (?:anything|any food|food|fluids?|liquids?|water|solids?) down\b",
    rf"\b{LIVING}\b[^.!?]{{0,16}}\bcut (?:her|his|their|its)self\b",
    rf"\b{LIVING}\b[^.!?]{{0,16}}\b(?:has|had|got) (?:a |an )?(?:\w+ )?(?:cut|wound|gash|burn)\b",
    rf"\b{LIVING}\b[^.!?]{{0,16}}\b(?:cut|burnt|burned|bleeding|bled)\b[^.!?]{{0,12}}"
    r"\b(?:her|his|their)\b",
    rf"\b{LIVING}\b[^.!?]{{0,24}}\b(?:collaps(?:e|ed|ing)|fainted|passed out|blacked out|"
    r"not breathing|can'?t breathe|choking|bleeding badly)\b",
    r"\bi\b[^.!?]{0,16}\b(?:collapsed|fainted|passed out|blacked out|threw up|"
    r"vomited|was sick all|been sick all)\b",
    r"\b(?:kill myself|killing myself|end my life|take my own life|want to die|"
    r"better off dead)\b(?!\s+(?:my|your|his|her|their|our|the|a|an|this|that|it)\b)",
    r"\b(?:won'?t let me leave|hits me|hit me|hurts? me|hurting me|threatened me|"
    r"took my phone|takes my phone)\b",
    r"\b(?:on fire|smoke in|gas leak|smell(?:s)? (?:of )?gas)\b",
    r"\b(?:took|taken) (?:all|too many|the rest of) (?:my|his|her|their|the) pills\b",
    r"\b(?:broke up|split up|divorce\w*|redundant|laid off|evicted|stolen|robbed|scammed)\b",
    SACKED_FIRED,
    LEFT_ME,
    LEFT_PLAN,
    r"\b(?:in debt|arrears|behind on (?:the )?(?:rent|mortgage|payments|bills)|"
    r"can'?t afford|can not afford)\b",
    r"\b(?:didn't get|didn't work out|didn't make it|turned down|turned it down|no luck|"
    r"wasn't picked|not chosen)\b",
    LOST_PATTERN,
    r"\bmiscarriage(?:s)?\b(?! of justice)|\bmiscarried\b",
    r"\bstill ?born\b|\bstill ?birth\b",
    r"\b(?:lost|losing|we lost) (?:the|our|her|his|their) baby\b"
    r"(?!\s+(?:weight|belly|tummy|fat|pounds?|stones?|kilos?|inches|clothes|things|stuff|"
    r"room|pram|toys?|seat|carrier|monitor|name|bag|book)\b)",
    rf"\b{LIVING}\b[^.!?]{{0,24}}\bkilled (?:him|her|them)sel(?:f|ves)\b"
    r"(?!\s+(?:laughing|giggling))",
    r"\b(?:took|taken|taking) (?:his|her|their) own life\b|\bcommitted suicide\b",
    r"\bpregnan\w+\b[^.!?]{0,24}\b(?:spotting|bleeding|cramping)\b",
    r"\b(?:spotting|bleeding)\b[^.!?]{0,24}\bpregnan\w+\b",
))

AWARD_LOST = tuple(re.compile(pattern) for pattern in (
    r"\b(?:pip|dla|esa|universal credit|housing benefit|child benefit|tax credits?|"
    r"benefits?|allowance|pension|pay|wages|hours)\b[^.!?]{0,24}"
    r"\b(?:stopped|cancell?ed|cut|suspended|frozen|refused|sanctioned|withdrawn|reduced|"
    r"turned down|taken away|not renewed)\b",
    r"\b(?:stopped|cancell?ed|cut|suspended|frozen|sanctioned|withdrawn|refused|reduced)\b"
    r"[^.!?]{0,20}\b(?:my|our)\s+(?:pip|dla|esa|universal credit|benefits?|pay|wages|pension|"
    r"allowance|hours)\b",
    r"\b(?:got|gotten|been|being|was|were|just|now)\s+sanctioned\b"
    r"(?!\s+(?:leave|holiday|absence|time off|day off|overtime|pay rise)\b)",
))

NEWS_WITH_A_NAME = tuple(re.compile(pattern) for pattern in (
    rf"\b{CONDITION_OWNER}\b[^.!?]{{0,20}}\b(?:has|have|had|got|is|was|were|been|being)\b"
    rf"[^.!?]{{0,24}}"
    r"\b(?:dementia|alzheim\w*|altzheim\w*|parkinson\w*|motor neurone|"
    r"huntington\w*|multiple sclerosis|muscular dystrophy|leuka?emia|lymphoma|myeloma|"
    r"mesothelioma|pancreatitis|copd|emphysema|cirrhosis|kidney failure|heart failure|"
    r"brain (?:damage|injury)|cerebral palsy|terminal)\b",
    rf"\b{CONDITION_OWNER}\b[^.!?]{{0,24}}\b(?:is|are|was|were|has been|have been|had been|"
    rf"got|getting|become|becoming|been)\b[^.!?]{{0,16}}"
    r"\b(?:ill|poorly|unwell|not well|off (?:it|colour|their food)|in a bad way|"
    r"taken ill|gone downhill|deteriorat\w+)\b",
    rf"\b{CONDITION_OWNER}\b[^.!?]{{0,24}}\bd(?:iagnos\w+|x\b)",
    r"\b(?:been|being|just|newly|recently)\s+(?:diagnos(?:ed|is)\w*)\b",
    r"\b(?:not allowed|no longer allowed|allowed|banned|barred|stopped|prevented)\b"
    r"[^.!?]{0,24}\b(?:see|seeing|visit|visiting|contact(?: with)?)\b[^.!?]{0,20}"
    r"\b(?:kids?|children|child|son|daughter|grandchild\w*|baby)\b",
    *AWARD_LOST,
    r"\b(?:have|has|had|having|got|gotten|getting|being (?:forced|made))\s*(?:to\s+)?"
    r"(?:sell|give up|hand back|move out of)\b[^.!?]{0,24}"
    r"\b(?:the|our|my|his|her)\s+(?:house|home|flat|bungalow|place)\b",
    rf"(?!.*{ADOPTION_WORDS})\b(?:got|gotten|had|received|been sent|sent me|sending me|came through|arrived)\b"
    r"[^.!?]{0,28}\b(?:court (?:date|letter|order|summons|hearing)|summons|notice to quit|"
    r"eviction notice|possession (?:claim|order)|letter before (?:claim|action))\b",
    r"\bbailiffs?\b",
    rf"(?!.*{ADOPTION_WORDS})\b(?:going|have to go|has to go|got to go|due|off)\s+(?:in |to |before )?court\b",
    r"\b(?:taking|took|taken|summoned|prosecuting|suing)\s+(?:me|us|him|her|them)\s+to court\b",
    r"\b(?:i'?m|im|i am|we'?re|we are|i was|we were)\s+(?:being\s+)?(?:taken|summoned|"
    r"prosecuted|sued)\s+(?:to|into|before)\s+court\b",
    r"\b(?:hearing|trial|case)\s+(?:is |was )?(?:next|this)\s+(?:week|month|monday|tuesday|"
    r"wednesday|thursday|friday|morning|afternoon)\b",
    r"\b(?:going|went|moved|transferred|have to go|has to go|got to go|off|sent|"
    r"sentenced|remanded|due)\b"
    r"[^.!?]{0,16}\b(?:to |in |into )?(?:prison|jail|young offenders)\b"
    r"(?!\s+(?:to\s+(?:visit|see|meet)|visiting|museum|tour|open\s+day))",
    r"\b(?:is|are|was|were|been|being|stays?|sits?|sitting|kept|held|locked)\s+"
    r"(?:up\s+|inside\s+|away\s+)?(?:in|at|inside)\s+(?:the\s+)?"
    r"(?:prison|jail|jailhouse|young offenders|pentonville|wormwood scrubs|brixton|wandsworth)\b",
    r"\bsent down\b[^.!?]{0,16}\b(?:for|to)\s+(?:\d+|two|three|four|five|six|seven|eight|"
    r"nine|ten|twelve|eighteen|twenty|a\s+(?:year|month|stretch|while)|life)\b",
    r"\b(?:was|were|is|are|been|being|got|gets|getting|keeps being)\s+sent down\b",
    r"\b(?:taken|took|put|puts|removed|removes)\b[^.!?]{0,20}\b(?:into care|in care)\b",
    rf"\b(?:taken|took|removed)\b[^.!?]{{0,24}}\b(?:my|our|the)\s+"
    rf"(?:kids?|children|child|son|daughter|baby)\b[^.!?]{{0,16}}\baway\b",
    r"\bsocial services\b[^.!?]{0,24}\b(?:took|taken|removed|involved|came)\b",
    r"\b(?:losing|lose|lost|going to lose|about to lose|might lose|will lose|going to be losing)\b"
    r"[^.!?]{0,12}\b(?:the|our|my)\s+(?:house|home|flat|bungalow)\b",
    r"\b(?:got|get|getting|been|being|was|were)\s+sacked\b",
    r"\b(?:bad|sad|awful|terrible|dreadful|grim|rotten|horrible|horrid)\s+(?:news|tidings)\b",
))

BAD_NEWS = BAD_NEWS_ITSELF + NEWS_WITH_A_NAME


def reads_as_an_award_lost(clean):
    return any(pattern.search(clean) for pattern in AWARD_LOST)


def reads_as_a_sacking(clean):
    return bool(re.search(SACKED_FIRED, clean))


def reads_as_news_with_a_name(clean):
    return any(pattern.search(clean) for pattern in NEWS_WITH_A_NAME)


def reads_as_heavy_news(clean):
    return any(pattern.search(clean) for pattern in BAD_NEWS_ITSELF)


CLOSED_DOOR_LINES = (
    r"\b(?:nobody|no\s?one|none of them|not one)\s+(?:will|would|wants? to|is willing to|"
    r"has|have|ever)\s+(?:\w+\s+){0,3}?(?:hire|employ|interview|"
    r"take (?:me|him|her|us|them) on|give (?:me|him|her|us|them) a (?:chance|look|shot|start))\b"
    r"(?=\s*(?:$|[,.!?]|(?:me|him|her|us|them|someone|anyone|people|at my age)\b))",
    r"\b(?:nobody|no\s?one)\s+(?:(?:gets?|has|have|ever)\s+(?:got|gotten)?\s*back to)\s*(?:me|him|her|us)\b",
    r"\b(?:nobody|no\s?one)\s+(?:ever\s+)?(?:gives?|gave|will give|would give)\s+(?:me|him|her|us)\s+(?:a\s+)?(?:chance|look|shot|start|break)\b",
    r"\b(?:can'?t|cannot|cant|struggling to|never)\s+(?:get|land|find|even get)\s+"
    r"(?:an? )?(?:interview|job|work|reply|response|answer|call ?back)\b",
    r"\btoo old\b[^.!?]{0,40}\b(?:job|jobs|work|hire|hired|interview|employ|employer)\b",
    r"\b(?:job|jobs|work|hire|hired|interview|employer)\b[^.!?]{0,30}\btoo old\b",
    r"\b(?:turned down|rejected|knocked back)\b[^.!?]{0,20}\b(?:again|for (?:the|a) "
    r"(?:job|role|position|interview))\b",
)

CLOSED_DOOR_WORK = re.compile(
    r"\b(?:job|jobs|work|working|hire|hiring|hired|interview|interviews|application|applications|"
    r"applied|apply|applying|role|roles|position|positions|employer|employers|employ|employed|"
    r"recruit\w*|career|careers|shift|shifts|cv|vacanc\w*|prospects?)\b")

CLOSED_DOOR = tuple(re.compile(pattern) for pattern in CLOSED_DOOR_LINES)

CLOSED_DOOR_WORK_OWN = re.compile(
    r"\b(?:take|takes|took|taken|taking)\s+(?:me|him|her|us|them)\s+on\b"
    r"(?=\s*(?:$|[,.!?]|(?:again|as|at|last|this|for|because|but|and)\b))")

CLOSED_DOOR_ELSEWHERE = re.compile(
    r"\b(?:he|she|they|him|her|them|his|their|"
    r"my (?:son|daughter|child|kid|husband|wife|partner|boyfriend|girlfriend|mum|mom|mam|dad|"
    r"father|mother|brother|sister|friend|mate|flatmate|neighbour|neighbor|colleague|carer))\b")
CLOSED_DOOR_ELSE_OWN = (False, False, False, True, False, False, False)


def reads_as_a_closed_door(clean):
    if not (CLOSED_DOOR_WORK.search(clean) or CLOSED_DOOR_WORK_OWN.search(clean)):
        return False
    for pattern, else_owns_it in zip(CLOSED_DOOR, CLOSED_DOOR_ELSE_OWN):
        if not pattern.search(clean):
            continue
        if else_owns_it and CLOSED_DOOR_ELSEWHERE.search(clean):
            continue
        return True
    return False


JOKED = re.compile(r"\b(?:seizures?|choking|strokes?|heart attacks?|collapsed|passed out)\b"
                   r"[^.!?]{0,14}\b(?:laughing|giggl\w*|cracking up|in stitches)\b")


VOWELS = frozenset("aeiou")

NOT_A_TYPO = frozenset(("strike", "stroked", "strokes", "stroking", "collapse"))


def _nearly(word):
    if len(word) < 6 or word in NOT_A_TYPO:
        return False
    for target in NEARLY:
        if word == target or abs(len(word) - len(target)) > 1:
            continue
        if word in LEXICON:
            continue
        if _one_edit(word, target):
            return True
    return False


LUMP_NOT_A_LUMP = (r"(?![\s-]+(?:sums?|of|sugar)\b)"
                   r"(?!\s+in\s+(?:my|your|his|her|their|our|the)\s+throat\b"
                   r"(?![^.!?]*\b(?:swallow|swallowing|voice|breath|breathing|breathe)\b))")

BODY = (r"(?:head|throat|ear|ears|eye|eyes|tooth|teeth|back|knee|shoulder|arm|leg|legs|foot|feet|"
        r"hand|hands|stomach|tummy|chest|neck|hip|ankle|wrist|elbow|toe|finger|skin|nose|sinus|"
        r"jaw|jaws|cheek|cheeks|chin|lips?|tongue|gums?|mouth|face|forehead|temple|temples|"
        r"scalp|spine|ribs?|shins?|calf|calves|thighs?|groin|kidneys?|bladder|nails?|heels?|"
        r"palms?|soles?|thumbs?|")
BODY = BODY[:-1] + ")"

HURTS = (r"(?:back|knee|knees|hip|hips|shoulder|shoulders|arm|arms|leg|legs|foot|feet|ankle|"
         r"ankles|wrist|wrists|elbow|elbows|neck|hand|hands|rib|ribs|shin|shins|calf|calves|"
         r"thigh|thighs|spine|jaw|heel|heels|thumb|thumbs|toe|toes|finger|fingers|"
         r"hip|knees|joints?)")
ILL_PART = (r"(?:chest|throat|stomach|tummy|head|ear|ears|earache|tooth|teeth|toothache|nose|"
            r"sinus|eye|eyes|gums?|mouth|cheek|cheeks)")
SICK = (r"(?:sore|cough|coughing|headache|migraine|toothache|earache|rash|itchy|itching|"
        r"infection|infected|cramps?|nauseous|nausea|dizzy|swollen|swelling|aching|aches?|"
        r"throw up|throws up|threw up|throwing up|vomit\w*|constipated|bloated|diarrhoea|"
        r"diarrhea|unwell|poorly|sick|temperature|flu|"
        r"migraines|"
        r"lumps?" + LUMP_NOT_A_LUMP + r"|growths?)")
IWE = r"\b(?:i|we)(?:'ve|ve|'m|m| have| am| feel| felt| got| keep| woke up with)\b"
HURT = (r"hurts?|hurting|aches?|aching|sore|pain|painful|agony|agonising|agonizing|"
        r"killing me|is killing me|are killing me|tender|raw|"
        r"swollen|swelling|puffy|stiff|throbbing|itchy|itches|"
        r"burning|on fire|hot|bad")
SYMPTOM = (
    re.compile(IWE + r"[^.!?]{0,25}?\b" + SICK, re.I),
    re.compile(r"\bmy " + BODY + r"\b[^.!?]{0,15}?\b(?:" + HURT + r")\b", re.I),
    re.compile(r"\b(?:i|we)\s+(?:throw\w* up|vomit\w*|(?:am|are|'m|'re)?\s*being sick)\b", re.I),
    re.compile(r"\b(?:my|a|the)\s+(?:stiff|sore|bad|dodgy|aching|swollen|gammy|sore)\s+" + BODY,
               re.I),
    re.compile(IWE + r"[^.!?]{0,30}?\b(?:the runs|the trots|the squits|bad guts|bad belly|"
               r"dicky (?:tummy|stomach)|dodgy (?:tummy|stomach)|upset (?:tummy|stomach)|"
               r"(?:tummy|stomach|sick) bug|food poisoning|being sick|keep(?:t|s)? being sick|"
               r"can'?t? keep anything down|loose stools|runny (?:tummy|bottom)|"
               r"running to the (?:loo|toilet))\b", re.I),
    re.compile(r"\bmy (?:stomach|tummy|belly|guts)\s+(?:is |feels |has been )?"
               r"(?:off|queasy|bad|dodgy|playing up)\b", re.I),
    re.compile(r"\b(?:i|we)\s+(?:found|felt|noticed|spotted)\b[^.!?]{0,20}?"
               r"\b(?:lumps?|growths?)\b" + LUMP_NOT_A_LUMP, re.I),
    re.compile(r"\b(?:i|we)(?:'ve|ve|'m|m| have| am)?\s*(?:got|had|been|felt|feel)?\s*"
               r"(?:a|an|the)\s+(?:bad |nasty |chesty |sore )?"
               r"(?:cold|cough|temperature|sore throat|rash|migraine|headache|infection)\b",
               re.I),
)
BARE_ACHE = re.compile(r"\b\w*aches?\b", re.I)
BARE_ILL = re.compile(r"\b(?:migraines?|heartburn|indigestion|tonsillitis|sciatica|cystitis|"
                      r"gout|sinusitis)\b", re.I)
BARE_BODY = re.compile(r"\b" + BODY + r"\b", re.I)
BARE_HURTS = re.compile(r"\b(?:" + HURT + r"|dodgy|constant|dull)\b", re.I)
BARE_FILLER = frozenset("""
oh ugh urgh god gosh really very so proper right left both top lower upper my me a an the this
that and but also still now just actually honestly awful terrible nasty bad little bit of on off
im i ive had got since yesterday today tonight morning night all day days weeks week now too
the worst ever
""".split())
BARE_WORD_ONLY = re.compile(r"\b(?:is|are|was|were|have|has|had|got|get|feel|feeling|been|do|does|"
                            r"did|can|could|should|would|will|helps?|stop|stopping|cure|treat|"
                            r"remedy|remedies|take|need|want|make|makes|go|going|come|came|"
                            r"keep|keeps|said|says|tell|think|know|why|what|how|when)\b", re.I)


def reads_as_a_bare_ailment(clean):
    if not isinstance(clean, str) or not clean.strip() or "?" in clean:
        return False
    if BARE_WORD_ONLY.search(clean):
        return False
    words = re.findall(r"[a-z']+", clean.lower())
    if not words or len(words) > 5:
        return False
    named = bool(BARE_ACHE.search(clean) or BARE_ILL.search(clean))
    if not named and not (BARE_BODY.search(clean) and BARE_HURTS.search(clean)):
        return False
    for word in words:
        if word in BARE_FILLER:
            continue
        if (BARE_ACHE.fullmatch(word) or BARE_ILL.fullmatch(word)
                or BARE_BODY.fullmatch(word) or BARE_HURTS.fullmatch(word)):
            continue
        return False
    return True


AGE_CHILD = (r"(?:(?:\d+|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|"
             r"thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|nineteen|a|an)"
             r"[\s-]+(?:month|months|week|weeks|year|years)[\s-]+old"
             r"(?:[\s-]+(?:baby|boy|girl|son|daughter|child|kid|toddler|little one))?)")
KIN = (r"(?:mum|mom|mother|mam|dad|father|gran|granny|grandma|grandad|grandpa|nana|nan|"
       r"son|daughter|child|kid|baby|boy|girl|toddler|teenager|little one|wife|husband|"
       r"partner|boyfriend|girlfriend|fiance|fiancee|brother|sister|uncle|aunt|" + AGE_CHILD + r")")
PETS = (r"(?:dog|puppy|cat|kitten|horse|pony|rabbit|hamster|guinea pig|gerbil|ferret|budgie|"
        r"parrot|bird|tortoise|snake|lizard|chicken|hens?|goat|sheep|pig|pet)")
CARED_SIGN = (r"pale|pallid|flushed|clammy|listless|lethargic|washed out|off colou?r|"
              r"out of sorts|peaky|groggy|doughy|waxy|sallow|not (?:himself|herself|themselves)|"
              r"clingy|whinge?y|fractious|"
              r"not sleeping|sleep(?:ing (?:a lot|more|all the time)|ier)|"
              r"off (?:his|her|their) (?:food|bottle|drink)")
CARED_SICK = (r"(?:sore\s+(?:throat|head|tummy|ear|ears|back|arm|leg|legs|foot|feet|hand|"
              r"knee|chest|neck|tooth|mouth)|cough|coughing|headache|migraine|toothache|"
              r"earache|rash|itchy|itching|"
              r"infection|infected|cramps?|nauseous|nausea|dizzy|swollen|swelling|aching|aches?|"
              r"throw\w* up|throw up|vomit\w*|being sick|diarrhoea|diarrhea|unwell|poorly|"
              r"sick(?!\s+(?:note|pay|days?|leave|of|bag|joke|sense))|temperature|fever|flu|"
              r"bugs?|"
              r"cold(?!\s+(?:sore|sores|feet|hands|fingers|toes|air|weather|room|drink|water|"
              r"days?|morning|night|outside|shoulder|call))|chickenpox|chicken pox|croup|"
              r"colic|teething|eczema|conjunctivitis|hand foot and mouth|runny nose|blocked nose|"
              r"chesty|sniffles?|nits|head lice|worms|thrush|migraines|" + CARED_SIGN + r")")
PET_NAMED_CONDITION = (
    r"(?:kidney|liver|heart|lung|thyroid)\s+(?:failure|disease|problems?|trouble|condition)"
    r"|renal failure|diabet\w*|epilep\w*|heart murmur|cushing\w*|addison\w*"
    r"|pancreatitis|blocked bladder|urinary tract")


def _someone_elses_symptoms(who, sick=CARED_SICK, owner=r"my|our", named=None,
                            generic=True, body_only=False, part=None):
    shapes = []
    if generic and not body_only:
        shapes.extend([
        re.compile(rf"\b(?:{owner})\s+(?:poor\s+|little\s+|eldest\s+|youngest\s+|old\s+)?"
                   rf"{who}(?:'s|s)?\s+(?:has|have|had|got|has got|keeps getting|keeps|kept|"
                   rf"keep|came down with|come down with|is|was|been|looks|seems)\b"
                   rf"[^.!?]{{0,30}}?\b(?:{sick})\b", re.I),
        re.compile(rf"\b(?:{owner})\s+{who}\s+(?:{sick})\b", re.I),
        ])
    if generic:
        shapes.extend([
        re.compile(rf"\b(?:my|our)\s+{who}(?:'s|s)\s+{BODY}\b[^.!?]{{0,18}}?\b"
                   r"(?:" + HURT + r"|infected|playing up)\b", re.I),
        re.compile(rf"\b(?:{owner})\s+{who}(?:'s|s)?\s+(?:has|have|had|got)(?:\s+got)?\s+(?:a|an)?\s*"
                   r"(?:bad|sore|dodgy|gammy|weak|dicky|knackered|broken|cracked|twisted|swollen|"
                   rf"stiff|aching)\s+{part or BODY}\b", re.I),
        ])
    if named:
        shapes.append(
            re.compile(rf"\b(?:{owner})\s+(?:poor\s+|little\s+|eldest\s+|youngest\s+|old\s+)?"
                       rf"{who}(?:'s|s)?\b[^.!?]{{0,24}}?\b(?:{named})\b", re.I)
        )
    return tuple(shapes)


AGE_NUMBER = (r"(?:\d{1,3}|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|"
              r"thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|nineteen|twenty|thirty|"
              r"forty|fifty|sixty)")
CHILD_BY_AGE = re.compile(
    rf"\b(?:my|our|the|his|her|their)\s+(?:little\s+|poor\s+|tiny\s+|new\s+)?{AGE_NUMBER}"
    rf"\s*-?\s*(?:month|months|mth|mths|week|weeks|wk|wks|year|years|yr|yrs)\s*-?\s*old\s+"
    rf"(?:has|have|had|got|keeps\s+getting|came\s+down\s+with|is|was|been|looks|seems)\b"
    rf"[^.!?]{{0,30}}?\b(?:{CARED_SICK})\b", re.I)

CARER_SYMPTOM = (_someone_elses_symptoms(KIN) + (CHILD_BY_AGE,)
                 + _someone_elses_symptoms(KIN, generic=False, body_only=True, part=ILL_PART))
CARER_BODY = _someone_elses_symptoms(KIN, body_only=True, part=HURTS)
PET_SYMPTOM = _someone_elses_symptoms(PETS, CARED_SICK + "|" + PET_NAMED_CONDITION,
                                       owner=r"my|our|the", named=PET_NAMED_CONDITION)
PET_LOW = (r"(?:depressed|sad|unhappy|miserable|withdrawn|lethargic|listless|moping|mopey|"
           r"not\s+(?:him|her|them)sel(?:f|ves)|off\s+(?:his|her|their)\s+food|"
           r"gone\s+quiet|hiding|not\s+eating|won'?t\s+eat)")
PET_LOW_SYMPTOM = _someone_elses_symptoms(PETS, PET_LOW, owner=r"my|our|the")
PET_CONDITION = _someone_elses_symptoms(PETS, PET_NAMED_CONDITION, owner=r"my|our|the",
                                        named=PET_NAMED_CONDITION, generic=False)
TROUBLE_OVER = re.compile(
    r"\b(?:has|have|had)\s+gone(?:\s+now)?\s*$"
    r"|\b(?:has|have|had)\s+(?:cleared(?:\s+up)?|eased(?:\s+off)?|settled(?:\s+down)?)\s*$"
    r"|\b(?:got|getting)\s+over\s+\w+"
    r"|\b(?:is|are|was|were|feels?|feeling)\s+(?:better|fine|ok|okay|under\s+control)\b",
    re.I)


def reads_for_a_carer(clean, memory=None):
    if TROUBLE_OVER.search(clean):
        return False
    if any(pattern.search(clean) for pattern in CARER_SYMPTOM):
        return True
    return False


def reads_as_a_carer_body(clean, memory=None):
    if TROUBLE_OVER.search(clean):
        return False
    if any(pattern.search(clean) for pattern in CARER_BODY):
        return True
    if memory is not None:
        from ..memory import whose_body
        return whose_body.somebody_elses_body(clean, memory)
    return False


def reads_for_a_pet(clean):
    if TROUBLE_OVER.search(clean):
        return False
    if any(pattern.search(clean) for pattern in PET_LOW_SYMPTOM):
        return True
    return any(pattern.search(clean) for pattern in PET_SYMPTOM)


def reads_as_a_pet_low(clean):
    if TROUBLE_OVER.search(clean):
        return False
    return any(pattern.search(clean) for pattern in PET_LOW_SYMPTOM)


def reads_as_a_pet_condition(clean):
    if TROUBLE_OVER.search(clean):
        return False
    return any(pattern.search(clean) for pattern in PET_CONDITION)


def reads_like_a_symptom(clean):
    clean = without_the_figure_of_speech(clean)
    if any(pattern.search(clean) for pattern in SYMPTOM):
        return True
    return reads_as_a_bare_ailment(clean)


def _one_edit(left, right):
    if left == right:
        return False
    if len(left) == len(right):
        different = [(a, b) for a, b in zip(left, right) if a != b]
        return (len(different) == 1 and different[0][0] in VOWELS
                and different[0][1] in VOWELS)
    short, long = (left, right) if len(left) < len(right) else (right, left)
    for index in range(len(long)):
        if long[:index] + long[index + 1:] == short:
            return True
    return False


SUICIDE = re.compile(
    rf"\b(?:{LIVING}|{OTHERS})\b[^.!?]{{0,26}}"
    r"\b(?:killed (?:him|her|them)sel(?:f|ves)|hanged (?:him|her|them)sel(?:f|ves)|"
    r"took (?:his|her|their) own life|committed suicide)\b"
    r"(?!\s+(?:laughing|giggling))", re.I)
SUDDEN_LOSS = tuple(re.compile(pattern) for pattern in (
    r"\bmiscarriage(?:s)?\b(?! of justice)|\bmiscarried\b",
    r"\bstill ?born\b|\bstill ?birth\b",
    r"\b(?:lost|losing|we lost) (?:the|our|her|his|their) baby\b"
    r"(?!\s+(?:weight|belly|tummy|fat|pounds?|stones?|kilos?|inches|clothes|things|stuff|"
    r"room|pram|toys?|seat|carrier|monitor|name|bag|book)\b)",
    rf"\b{LIVING}\b[^.!?]{{0,24}}\bkilled (?:him|her|them)sel(?:f|ves)\b"
    r"(?!\s+(?:laughing|giggling))",
    r"\b(?:took|taken|taking) (?:his|her|their) own life\b|\bcommitted suicide\b",
))
PREGNANCY_BLEEDING = tuple(re.compile(pattern) for pattern in (
    r"\bpregnan\w+\b[^.!?]{0,24}\b(?:spotting|bleeding|cramping)\b",
    r"\b(?:spotting|bleeding)\b[^.!?]{0,24}\bpregnan\w+\b",
))


def reads_as_sudden_loss(clean):
    text = " ".join(str(clean or "").lower().split())
    if _dream is not None and _dream.a_dream_is_not_happening(text) \
            and not _dream.a_death_came_first(text):
        return False
    return (any(pattern.search(text) for pattern in SUDDEN_LOSS) or bool(SUICIDE.search(text))
            or reads_as_someones_death(text))


def reads_as_someones_death(clean):
    text = " ".join(str(clean or "").lower().split())
    if text in ("died", "dies", "she died", "he died"):
        return True
    for found in DEATH_SAID.finditer(text):
        if _NEARLY.search(text[:found.end()]):
            continue
        if _AFTER_IT.match(text[found.end():]):
            continue
        if _subject_before(text, found.start(), found.group(0)):
            return True
    return False


_NAMES_ITS_SUBJECT = re.compile(
    r"^(?:killed|hanged)\s+(?:him|her|them)sel(?:f|ves)\b"
    r"|^took\s+(?:his|her|their)\s+own\s+li(?:fe|ves)\b"
    r"|^committed\s+suicide\b|^found\s+dead\b", re.I)


def _subject_before(text, start, said=""):
    if said and _NAMES_ITS_SUBJECT.match(said):
        return True
    clause = text[:start]
    for mark in (".", "!", "?"):
        cut = clause.rfind(mark)
        if cut != -1:
            clause = clause[cut + 1:]
    words = _WORD.findall(clause)
    for word in reversed(words):
        if word in _CARRIES or word in _PLACE:
            continue
        return word in _PERSON
    return False


def reads_as_pregnancy_bleeding(clean):
    return any(pattern.search(clean) for pattern in PREGNANCY_BLEEDING)


def reads_as_the_speakers_own_plan(clean):
    return any(pattern.search(clean) for pattern in OWN_PLAN)


def _the_result_came_back_well(clean):
    from .goodnews import reads_as_a_clear_result
    return reads_as_a_clear_result(clean)


def reads_as_bad_news(clean):
    if _the_result_came_back_well(clean):
        return False
    if any(pattern.search(JOKED.sub(" ", clean)) for pattern in BAD_NEWS):
        return True
    words = re.findall(r"[a-z']+", clean)
    return any(_nearly(word) for word in words)


if __name__ == "__main__":
    import sys

    for line in sys.argv[1:]:
        low = line.lower()
        print(f"{reads_as_bad_news(low)!s:5} {reads_like_a_symptom(low)!s:5} {line}")
