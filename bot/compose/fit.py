import re

TIME = "time"
AMOUNT = "amount"
PLACE = "place"
PERSON = "person"
MEANING = "meaning"
YESNO = "yesno"
PICK = "pick"
COMPARE = "compare"
STEPS = "steps"
OPTIONS = "options"
REASON = "reason"
OPINION = "opinion"
ADVICE = "advice"
COMFORT = "comfort"
ANSWER = "answer"

WANTS = (TIME, AMOUNT, PLACE, PERSON, MEANING, YESNO, PICK, COMPARE, STEPS, OPTIONS, REASON,
         OPINION, ADVICE, COMFORT, ANSWER)

SOFT = frozenset((OPINION, ADVICE, COMFORT, ANSWER))

ASKED_FOR = (
    (PICK, frozenset(("choice", "compare", "which"))),
    (MEANING, frozenset(("definition",))),
    (PLACE, frozenset(("where",))),
    (PERSON, frozenset(("who",))),
    (REASON, frozenset(("why",))),
    (TIME, frozenset(("how_long",))),
    (AMOUNT, frozenset(("how_much", "how_often"))),
    (AMOUNT, frozenset(("maths",))),
    (OPTIONS, frozenset(("list",))),
    (STEPS, frozenset(("steps", "how"))),
    (PICK, frozenset(("recommend",))),
    (YESNO, frozenset(("yesno",))),
)


A_RULE_THAT_SETTLES_IT = re.compile(
    r"\b(?:if|when|whenever|whether|once|until|unless|as long as)\b", re.I)


AN_OFFER_NOT_A_TEST = re.compile(
    r"\b(?:here|happy|around|about|available|back|on hand)\s+if\b"
    r"|\b(?:say|tell me|tell us|let me know|ask|shout|message|write|reply|try)\b[^.]{0,24}?\bif\b"
    r"|\b(?:what|as)\s+if\b", re.I)
A_STANDING_AFTER_THE_TEST = re.compile(
    r"\b(?:is|are|was|were|means|counts as|needs?|should|worth|too|enough|fine|ok|okay|safe|"
    r"normal|risky|a problem|gets?|lasts?|keeps?|stays?|throw|bin|toss|see (?:a|the|your)|"
    r"ring|call|matters|turns on|decides|depends)\b", re.I)


def _the_rule_settles_it(opening, line, reply=None):
    text = " ".join(str(reply or opening).split())
    if "?" in text:
        return False
    if AN_OFFER_NOT_A_TEST.search(opening):
        return False
    found = A_RULE_THAT_SETTLES_IT.search(opening)
    if not found:
        return False
    if found.group(0).lower() in ("once", "until", "unless") and \
            re.search(r"[:;]", opening[:found.start()]):
        return False
    if not opening[:found.start()].strip() and \
            found.group(0).lower() in ("if", "when", "whenever", "whether"):
        return False
    return A_STANDING_AFTER_THE_TEST.search(opening[found.end():]) is not None

A_FEW_THINGS = re.compile(
    r"\b(?:tips?|ideas?|suggestions?|recommendations?|pointers?|hacks?|options)\b", re.I)


def _said(understood):
    parts = []
    for key in ("norm", "norm_text", "clean", "text"):
        value = understood.get(key)
        if isinstance(value, (list, tuple)):
            value = " ".join(str(word) for word in value)
        if isinstance(value, str) and value:
            parts.append(value)
    return " ".join(" ".join(parts).lower().replace("\u2019", "'").split())


def _a_who_a_person_owns(understood):
    words = understood.get("words")
    entities = understood.get("entities")
    if not isinstance(words, (list, tuple)) or not isinstance(entities, (list, tuple)):
        return False
    for entity in entities:
        if not isinstance(entity, dict) or entity.get("type") != "person":
            continue
        at = entity.get("at")
        if not isinstance(at, int) or at < 0:
            continue
        after = at + len(str(entity.get("text") or "").split())
        word = str(words[after]).lower().strip("'\u2019") if 0 < after < len(words) else ""
        if word.startswith("who") or word == "that":
            return True
    return False


PICK_SIDES = frozenset(("choice", "compare", "which"))
DIFFERENCE = re.compile(
    r"\bwhat(?:['\u2019]?s| is| are| was| were)?\b(?:\s+[\w'-]+){0,3}\s+differences?\b"
    r"|\bhow (?:is|are|does)\b[^.?!]{0,40}\b(?:different|differ)\b\s*(?:from|to)\b"
    r"|^[\W]*(?:the )?differences? between\b", re.I)
SPECIFIC_ASKS = frozenset((
    "choice", "compare", "which", "definition", "where", "who", "why", "how_long",
    "how_much", "how_often", "list", "steps"))
KINDS_OF = re.compile(
    r"\b(?:what|which) (?:kinds?|types?|sorts?|varieties|styles|brands|makes|models)"
    r"(?: of (?:[\w'-]+ ){0,4})?"
    r"(?:are there|are available|is there|exist|do you|would you|can|could)\b"
    r"|\bwhat (?:are|were) the (?:kinds?|types?|sorts?|varieties|styles)\b"
    r"|\bwhat (?:are|were) (?:my|the|our) (?:options|choices)\b"
    r"|\bwhat (?:options|choices) (?:do i|do we|have i|are there)\b"
    r"|\b(?:any|other|more) (?:options|choices|alternatives)\b"
    r"|\bwhat else (?:is|are) (?:there|out there)\b"
    r"|\bwhat (?:is|are) available\b", re.I)
NOT_KINDS_OF = re.compile(
    r"\bwhat (?:kind|type|sort) of (?:a )?(?:[\w'-]+ ){0,3}(?:is|was|are|were) "
    r"(?:that|this|it|those|these|he|she)\b"
    r"|\bwhat (?:kind|type|sort) of (?:[\w'-]+ ){0,3}(?:would|will|should|could|might|suits?|fits?)\b",
    re.I)

STEPS_ASK = re.compile(
    r"\bwhat (?:are|is) the steps\b|\bsteps (?:to|for|in)\b|\bstep[- ]by[- ]step\b"
    r"|\bwalk me through\b|\bwhat(?:'s| is) the process\b|\bthe process (?:for|of|to)\b"
    r"|\bhow do i go about\b|\bwhat order\b|\bin what order\b"
    r"|\b(?:the )?(?:best|right|correct|proper) order (?:to|for|in)\b", re.I)
COUNTED_STEPS = re.compile(
    r"\bhow many steps\b|\bsteps? per\b|\bsteps? in (?:a|one) (?:mile|km|day)\b"
    r"|\bstep count\b|\b\d{3,} steps\b", re.I)
MEMBERS_ASK = re.compile(
    r"\bwhat (?:are|were) the (?:early |first |main |usual |common |classic |key |warning |"
    r"typical |initial )?(?:signs?|symptoms?|stages?|phases?)\b"
    r"|\bwhat (?:signs?|symptoms?|stages?)\b[^.?!]{0,30}\b(?:should|would|do|can|might) "
    r"(?:i|you|we) (?:look|watch|expect|see)\b"
    r"|\bwhat are the (?:warning|telltale) signs\b", re.I)

COMPARISON = re.compile(
    r"\bcompare[ds]?\b|\bcomparing\b|\bvs\.?(?=\s|$)|\bversus\b"
    r"|\bdifferences? between\b"
    r"|\bhow (?:is|are|does|do|did) [^.?!]{0,40}\b(?:different|differ|compare)\b"
    r"|\bwhat sets? [^.?!]{0,30}\bapart\b|\bsets? [^.?!]{0,30} apart\b", re.I)
COMPARED = re.compile(
    r"\b(?:better|worse|cheaper|dearer|quieter|louder|faster|slower|easier|harder|healthier|"
    r"safer|simpler|tastier|stronger) than\b", re.I)
NOT_A_COMPARISON = re.compile(
    r"\b(?:should i|shall i|worth (?:it|doing|the)|for me|which should i|which one should i|"
    r"is it better to|would you)\b"
    r"|\b(?:i|we) (?:always |still |keep |often |just )?compare\b"
    r"|\bhow (?:do|can|should|would|could) (?:i|we)\b"
    r"|\b(?:better|worse) than (?:i|we|you|they|she|he) (?:expected|thought|hoped|feared|looked)\b",
    re.I)

_SIDE = r"([\w'-]+(?: (?!and\b|from\b|than\b|vs\b|versus\b)[\w'-]+)?)"
_THE = r"(?:a |an |the )?"
SIDE_PAIRS = (
    re.compile(r"\bbetween " + _THE + _SIDE + r" and " + _THE + _SIDE, re.I),
    re.compile(r"\bcompare[sd]? " + _THE + _SIDE + r" (?:and|with|to) " + _THE + _SIDE, re.I),
    re.compile(_SIDE + r" apart from " + _THE + _SIDE, re.I),
    re.compile(_SIDE + r" (?:vs\.?|versus) " + _THE + _SIDE, re.I),
    re.compile(_SIDE + r" compar(?:e|ed) (?:with|to) " + _THE + _SIDE, re.I),
    re.compile(_SIDE + r" (?:is |are |was |were )?(?:comparable to) " + _THE + _SIDE, re.I),
    re.compile(_SIDE + r" (?:is |are |was |were )?(?:different|differs?) (?:from|to) "
               + _THE + _SIDE, re.I),
    re.compile(_SIDE + r" (?:better|worse|cheaper|dearer|quieter|louder|faster|slower|easier|"
               r"harder|healthier|safer|simpler|tastier|stronger) than " + _THE + _SIDE, re.I),
)
EXPLICIT_COMPARE = re.compile(
    r"\bcompare[ds]?\b|\bcomparing\b|\bvs\.?(?=\s|$)|\bversus\b|\bdifferences? between\b",
    re.I)


def _names_a_pair(said):
    return any(pattern.search(said or "") for pattern in SIDE_PAIRS)


def _asks_about_them(understood, said):
    if understood.get("intent") == "news":
        return False
    return EXPLICIT_COMPARE.search(said or "") or understood.get("kind") == "question"


OPEN_WHO_HELP = re.compile(r"^\W*who\b[^.!?]{0,40}\bhelp\b", re.I)
HELP_ME = re.compile(r"\b(?:can|could|would|will) you help me\b|\bhelp me (?:with|to|out)\b", re.I)
FIX_ASK = re.compile(
    r"\b(?:what(?:'?s| is| was)?|any|the|a)\s+(?:quick |easy |simple |cheap |good |real )?"
    r"(?:fix|cure|remedy)\s+(?:for|to)\b"
    r"|\b(?:fix|cure|remedy) for (?:my|the|a|an|this|that)\b"
    r"|\b(?:what(?:'?s| is| was)|any)\s+(?:the\s+)?(?:quick |easy |simple |cheap |good |real )?"
    r"(?:fix|cure|remedy)\s*[?.!]*\s*$", re.I)

HELP_ASK_ANY = re.compile(
    r"^\W*(?:(?:hi|hey|hello|ok|okay|so|right|please|sorry|and)\b[ ,]*)*"
    r"(?:(?:can|could|would|will) you\s+)?"
    r"(?:help (?:me|us)|i need help|i could do with (?:some )?help|give me a hand)\b"
    r"(?!\s+(?:choose|choosing|pick|picking|decide|deciding|select|selecting|compare|comparing"
    r"|name|naming|word|wording|come up with)"
    r"\b|\s+between\b|\s+which\b)", re.I)
HELP_ASK_NO_TASK = re.compile(
    r"^[\s,.;:!?\-]*(?:(?:with|about|on)\s+(?:something|anything|stuff|it|this|that)\b)?"
    r"[\s,.;:!?\-]*$"
    r"|\b(?:dont|don'?t|do not) know (?:what|where|how)\b|\bnot sure what\b", re.I)
HELP_WORD = re.compile(
    r"\b(?:help(?: me| us)?|i need help|i could do with (?:some )?help|give me a hand)\b", re.I)


def _a_help_ask_that_names_nothing(said):
    match = HELP_ASK_ANY.search(said or "") or HELP_WORD.search(said or "")
    rest = (said or "")[match.end():] if match else (said or "")
    return bool(HELP_ASK_NO_TASK.search(rest))
HOW_I = re.compile(r"\bhow (?:do|can|could|should|would) i\b", re.I)
COMPARE_MYSELF = re.compile(
    r"\bcompar(?:e|ing)\b[^.?!]{0,14}\b(?:myself|ourselves)\b"
    r"|\bcompare\s+(?:to|with)\s+(?:me|my|us|our|him|her|them|others)\b", re.I)
HOW_SOON = re.compile(r"\bhow (?:soon|early|quickly|long)\b", re.I)
METHOD_OPENS = re.compile(r"^how (?:do|does|did) (?:i|we|you)\b", re.I)
HOW_MEASURE = re.compile(
    r"\bhow (?:tall|old|big|far|heavy|wide|deep|high|fast|hot|cold|warm|hard|loud|cheap|expensive|"
    r"thick|thin|narrow|broad|shallow|steep|fine|coarse|tight|loose|"
    r"many|much|often)\b", re.I)
HOW_MEASURE_HEAD = re.compile(
    r"^how (?:tall|old|big|far|heavy|wide|deep|high|fast|hot|cold|warm|hard|loud|cheap|expensive|"
    r"thick|thin|ripe|tight|loose|full|low|slow|quick|short|small|large|near|soft|firm|dark|"
    r"bright|sharp|rough|smooth|fine|coarse|steep|cool|fresh|dry|wet|salty|sweet|spicy|sour|mild|"
    r"strong|weak|light|stiff)\b", re.I)
WHAT_DOES_MEASURE = re.compile(
    r"\bwhat (?:does|do)\b(?:(?!\bwhat\b)[^?]){0,30}?"
    r"\b(?:cost|costs|charge|charges|weigh|weighs)\b"
    r"|\bwhat (?:does|do)\b(?:(?!\bwhat\b)[^?]){0,30}?\bcome(?:s)? (?:to|out at|out as)\b"
    r"|\bwhat (?:do|does|would|will|should|can|could|did) .{0,40}?\b(?:charge|charges|cost|"
    r"costs)\b",
    re.I)

PRICE_IDIOM = re.compile(
    r"\bwhat(?:'s|s| is| was)?\s+the (?:going|current|average|typical|usual) rate\b"
    r"|\bset (?:me|us|you) back\b"
    r"|\bexpect(?:ing)? to (?:pay|spend|be paying)\b"
    r"|\b(?:usually|normally|typically|roughly|about) run(?:s)? to\b", re.I)
COSTS_NOTHING = re.compile(
    r"\bcosts? (?:nothing|free|nowt)\b|\bfor free\b|\bthat (?:is|are|will be) free\b"
    r"|\b(?:doesn'?t|does not|didn'?t|did not|don'?t|do not|won'?t|will not) costs?\b"
    r"|\bcosts? (?:much|a lot|more|less|too much)\b", re.I)
CONVERSION = re.compile(
    r"\bhow long (?:is|are|was)\b[^?]{0,30}?\b(?:in|to|as|into) "
    r"(?:feet|foot|metres?|meters?|miles?|kilometres?|kilometers?|km|yards?|inches|inch|cm|mm)\b",
    re.I)
CONVERTED_FIGURE = re.compile(
    r"\b(?:what(?:'s| is|s)|whats)\s*\d+(?:\.\d+)?\s*"
    r"(?:c|f|degrees?|deg|gas|ml|l|g|kg|oz|lb|lbs|cm|mm|in|inches|pints?|litres?|liters?|"
    r"ft|feet|foot|metres?|meters?|m|miles?|mi|yards?|yd|km|stone|st)\b"
    r"[^?]{0,25}?\b(?:in|to|into|as)\b"
    r"|\bconvert\s+\d+(?:\.\d+)?\s*(?:c|f|degrees?|deg|ml|g|kg|oz|lb|lbs|cm|mm|in)\b"
    r"[^?]{0,20}?\b(?:in|to|into)\b"
    r"|\bwhat(?:'s| is|s)?\s*\d+(?:\.\d+)?\s+\w+(?:\s+\w+)?\s+(?:in|to)\s+"
    r"(?:grams?|g|kg|ml|millilitres?|milliliters?|litres?|liters?|ounces?|oz|pounds?|lb|cups?|"
    r"tablespoons?|teaspoons?|degrees?|c|f)\b", re.I)
LEADING_JOIN = re.compile(r"^(?:(?:and|so|but|then|also|ok|okay|right|now|well)\b[ ,]*)+", re.I)
WHEN_ASKS = re.compile(
    r"^(?:when'?s|when|what time|what day|what date|what month|what year|which day|what weekday) "
    r"(?:should|shall|is|are|was|were|will|would|does|do|did|can|could|to|am|has|have|of|had)\b",
    re.I)
ASKS_WHEN = re.compile(
    r"^[\W]*(?:and |so |but |then )?(?:when|what time|what day|what date|what month|what year|"
    r"which day)\b", re.I)
WHICH_DAY_IS_BEST = re.compile(r"\b(?:best|better|rather|prefer|do you think|recommend)\b", re.I)
GOOD_THING = re.compile(
    r"\bwhat(?:'s|s| is| are)\s+(?:a|an|the|some)?\s*(?:really |actually |bit of a )?"
    r"(?:good|great|nice|decent|cheap|budget|quick|easy|simple|sensible|healthy)\b", re.I)
GOOD_WAY = re.compile(r"\b(?:way|method|approach|routine)\b", re.I)
GOOD_FIGURE_WORD = re.compile(
    r"\b(?:time|timeframe|rate|age|price|cost|number|amount|weight|height|length|salary|wage|"
    r"dose|dosage|percentage|temperature|speed|distance|size|pressure|humidity|mileage|"
    r"voltage|rent)\b", re.I)
WHAT_ARE_TIMES = re.compile(
    r"^\W*(?:(?:so|and|ok|okay|oh|also|right)\s+)*what(?:'s| is| are|s)\b[^?]{0,60}?"
    r"\b(?:opening|visiting|closing|trading|check ?in|check ?out|business|office|term|school|"
    r"library|swimming|bus|train|ferry|flight|shop|bank|tip|pool|gym|leisure|surgery|pharmacy|"
    r"restaurant|pub|museum) ?(?:times|hours|dates)\b", re.I)

VERDICT_FRAME = re.compile(
    r"^\W*(?:is|was|are|were|does|do|did)\s+(?:that|this|it|these|those|they)\s+"
    r"(?:a|an|the|too|really|actually|still|about|much)?\s*"
    r"(?:good|normal|average|typical|usual|fair|ok|okay|alright|right|fine)\b", re.I)
GOOD_FIGURE = re.compile(
    r"\b(?:good|average|normal|typical|usual|best) (?:\w+ ){0,3}(?:time|age|price|number|amount|"
    r"cost|salary|wage|rate|temperature|weight|height|speed|distance|size|dose|percentage)\b",
    re.I)
JUDGED_MEASURE = re.compile(
    r"\b(?:good|average|normal|typical|usual|best|safe|right|ideal|healthy|cheap|correct|"
    r"recommended|sensible|maximum|minimum|perfect|decent|acceptable)\s+(?:\w+\s+){0,3}"
    r"(?:rate|age|price|cost|number|amount|weight|height|length|salary|wage|dose|dosage|"
    r"percentage|temperature|speed|distance|size|pressure|humidity|mileage|rent|voltage)\b",
    re.I)
ON_THE_CLOCK = re.compile(r"\b(?:time|times|hour|hours|minute|minutes)\b", re.I)
ASKS_YES_OR_NO = re.compile(
    r"^\W*(?:is|are|was|were|am|do|does|did|should|shall|can|could|would|will|may|might|"
    r"have|has|had)\b", re.I)
A_GOOD_TIME = re.compile(
    r"(?:^|[,;]\s*|\b(?:and|so|but|then|also)\s+)"
    r"(?:is|are|was|were|would|could|will|do you think it is|do you think its)\b[^.?!]{0,60}?"
    r"\b(?:a|an)\s+(?:good|bad|better|best|ok|okay|fine|safe|alright|decent|terrible|awful|busy|"
    r"quiet)\s+time\b", re.I)
LONG_TIME = re.compile(r"\blong time (?:no (?:see|speak|hear|talk)\b|since\b)", re.I)
HOW_IT_WORKS = re.compile(
    r"\bhow (?:does|do|did) (?:(?!\b(?:i|you|we|im|me)\b)[\w']+ ){1,4}(?:work|works|working)\b",
    re.I)
WRITTEN_THING = re.compile(
    r"\bhow long (?:should |would |will |does |do |can )?(?:a|an|my|our|your|the|this|that)\s+"
    r"(?:[a-z]+\s+){0,2}(?:personal statement|statement|essay|dissertation|thesis|coursework|"
    r"assignment|cover(?:ing)? letter|letter|cv|resume|blog post|post|article|abstract|summary|"
    r"report|review|answer|paragraphs?|chapter|book|story|speech|presentation|email|text|message|"
    r"comment|description|bio|application|proposal|synopsis|blurb|poem|script|personal profile|"
    r"profile)\s+be\b", re.I)
THING_THAT_EXTENDS = re.compile(
    r"\bhow long (?:is|are|was|were|will be|would be) "
    r"(?:(?:the|a|an|my|our|your|this|that)\s+)?(?:[a-z'-]+\s+){0,2}?"
    r"(?:rivers?|nile|amazon|thames|severn|danube|rhine|mississippi|walls?|pitch(?:es)?|"
    r"playing fields?|marathons?|bridges?|tunnels?|canals?|motorways?|roads?|runways?|"
    r"coastlines?|coast|borders?|beaches?|whales?|snakes?|crocodiles?|sharks?|string|"
    r"ropes?|hose|cables?|pools?|tracks?|corridors?|driveways?)\b"
    r"(?=\s*(?:[.?!,;:]|$|\s+(?:of|in|on|at|from|to|by)\b))"
    r"(?!\s+(?:pregnant|old|big|tall|wide|deep|long|away|till|until|now)\b)", re.I)
HOW_TO_DO = re.compile(
    r"\bhow (?:do|can|could|should|would|will) (?:i|we|you) (?:explain|answer|say|tell|word|"
    r"respond|reply|put it|break it|approach|handle)\b|\bhow to (?:explain|answer|say|tell|"
    r"word|respond|reply|approach|handle)\b", re.I)
HOW_ARE_YOU = re.compile(
    r"^(?:(?:hey|hi|hiya|heya|hello|yo)(?: there)?[ ,]+)?how(?:'?s| is| are)?[ ,]+"
    r"(?:you|u|ya|things|tricks|life|are you|are things|is it going|s it going|have you been|"
    r"are we|your (?:day|week|evening|morning|night|head|family))\b"
    r"(?!\s+(?:work|works|worked|working|go|goes|went|change|changes|changed|happen|happens|"
    r"happened|fit|fits|seem|seems)\b)",
    re.I)
HOW_IT_WENT = re.compile(
    r"\bhow\s+(?:did|does|was|were|is|are|'s)\s+"
    r"(?:(?!\b(?:i|you|we|me|us)\b)\w+\s+){0,4}"
    r"(?:go|goes|went|get on|got on|getting on|get along|turn out|turned out|work out|"
    r"worked out)\b(?!\s+\w)"
    r"|\bhow (?:it|that|this|things|everything) (?:goes|went|go|turns out|turned out)\b"
    r"(?!\s+\w)"
    r"|\bhow (?:was|were) (?:it|that|this|things|everything)\b(?!\s+\w)"
    r"|\bhow goes it\b",
    re.I)
HOW_IT_HAPPENED = re.compile(
    r"\bhow\s+(?:did|does|do)\s+(?:it|that|this)\s+(?:happen|happens|happened|come about|"
    r"came about)\b", re.I)
ASKS_OUT_LOUD = re.compile(
    r"^(?:what|which|who|whose|when|where|why|how|is|are|was|were|do|does|did|can|could|should|"
    r"shall|would|will|any|anything|anyone|recommend|suggest|name|give me|tell me|got any)\b",
    re.I)
COST_ASK = re.compile(
    r"\bwhat (?:does|do|will|would|did|is it going to) .{0,40}\bcosts?\b"
    r"|\bwhat .{0,40}\bcosts?\b"
    r"|\b(?:price|cost|charge|fee)s? (?:of|for)\b", re.I)
WHAT_IS_PER = re.compile(
    r"\bwhat(?:'s|s| is)\b[^?]{0,40}\b(?:a|an|per|each|every) "
    r"(?:month|week|year|day|hour|litre|liter|kg|kilo|pint|mile|gb|gigabyte|night|visit|session|"
    r"person|head|class|lesson)\b", re.I)
COST_STANDS_IN = frozenset(("what", "definition", "list", "opinion", "recommend", "question"))
A_FIGURE_OF_A_MONEY_VERB = re.compile(
    r"\bwhat\s+(?:should|shall|do|does|would|can|could|will)\s+(?:i|we|you|they|he|she)\s+"
    r"(?:be\s+)?(?:pay|paying|spend|spending|earn|earning|budget)\b(?!\s+off\b)", re.I)
MONEY_VERB_NOT_A_PRICE = re.compile(
    r"\bpay(?:ing)?\s+attention\b"
    r"|\b(?:pay|paying|spend|spending)\s+(?:it|them|this|that|the\s+money|the\s+rest|"
    r"the\s+lot)\b"
    r"|\b(?:pay|paying)\s+off\b"
    r"|\bspend(?:ing)?\s+(?:(?:my|our|your|the)\s+)?(?:time|attention|effort|trouble|energy|"
    r"evening|day|weekend|morning|afternoon|night|holiday|summer|hours|years|life)\b", re.I)
SUM_OUT_LOUD = re.compile(
    r"^(?:subtract|add|multiply|divide|solve|factorise|factorize|work out|convert|split|minus|"
    r"plus|double|halve|times)\b|\bhow much is\b", re.I)
SUM_ASKS = re.compile(
    r"\b(?:\d+|half|quarter|third|two thirds|three quarters|a few)\b.{0,30}\bin "
    r"(?:grams?|gms?|kg|kilos?|kilograms?|ml|millilitres?|litres?|liters?|cups?|ounces?|oz|"
    r"pounds?|lbs?|tablespoons?|tbsp|teaspoons?|tsp|pints?|centimetres?|cm|inches|feet|metres?)\b"
    r"|\b(?:half|a quarter|a third|two thirds|three quarters|three quarters|a fifth) of \d+"
    r"|\bas a percentage\b|\bpercent (?:off|on top)\b|\b\d+\s*(?:%|percent)\b"
    r".{0,25}\b(?:off|tip|on top|between|split)\b"
    r"|\bsplit (?:the )?(?:bill|cost|rent|fare|total|it|\d|\u00a3)", re.I)
NOT_A_FIGURE = re.compile(
    r"\bhow (?:much|many) (?:do|did|can|could|would|have) you "
    r"(?:know|remember|understand|recall)\b|"
    r"\bhow (?:much|often) (?:does|do) (?:it|that|this|they) matter\b|"
    r"\bhow much (?:should|do) (?:i|we) (?:worry|care|mind)\b", re.I)
WHAT_ELSE_WITH = re.compile(
    r"\bwhat else (?:can|could|should|shall|do|would) (?:i|we|you)\b[^.!?]{0,25}?\bwith\b", re.I)
WHAT_ELSE_STEPS = re.compile(
    r"\bwhat else (?:can|could|should|shall|do|would) (?:i|we|you) (?:do|try)\b", re.I)
PICK_ONE = re.compile(
    r"\bwhat (?:do|should|shall|can|could) (?:i|we|he|she|they) (?:cook|make|eat|have|drink|watch|"
    r"read|listen to|wear|get|buy|order|play|study|plant|visit|do with|give|bring)\b"
    r"|\bwhat (?:do|should|shall|can|could) (?:my|our|his|her|their) \w+ (?:cook|make|eat|have|"
    r"drink|watch|read|wear|get|buy|order|play|study|plant|visit|give|bring)\b", re.I)
PAIRING_ASK = re.compile(
    r"\bwhat (?:[\w'-]+ )?go(?:es)? (?:with|alongside|nicely with)\b"
    r"|\bwhat (?:[\w'-]+ )?(?:wine|beer|drink|drinks|food|music|songs?|salad|sides?|dessert|"
    r"cheese|bread|pudding|starter|sauce|film|book|present|gift)s? (?:for|with)\b"
    r"|\bwhat should (?:i|we) name\b"
    r"|\bwhat should (?:i|we) call (?:my|our|the|his|her|their)\b"
    r"(?![^\n]*?\b(?:about|for|to|if|when)\b)", re.I)
PICK_ONE_OF_A_KIND = re.compile(
    r"\bwhat (?!else\b|about\b|of\b|in\b|on\b|at\b|to\b|from\b|for\b|with\b|by\b|between\b|"
    r"age\b|time\b|date\b|month\b|year\b|day\b|size\b|temp\b|temperature\b|price\b|cost\b|"
    r"amount\b|number\b|help\b|support\b|percentage\b|share\b|"
    r"spf\b|budget\b|salary\b|wage\b|dose\b|dosage\b|calorie\w*\b|weight\b|length\b|height\b|"
    r"depth\b|speed\b|rate\b|fee\b|charge\b|rent\b|tip\b|discount\b|voltage\b|wattage\b|"
    r"qualifications?\b|pets?\b|rights?\b|entitlements?\b|apr\b|interest\b|deposit\b|"
    r"savings?\b)"
    r"(?:(?:kind|sort|type|brand|make) of (?!price\b|cost\b|amount\b|salary\b|budget\b|"
    r"time\b|size\b|weight\b))?"
    r"(?:[\w'-]+ ){1,2}(?:should|shall) (?:i|we) "
    r"[a-z]+\b", re.I)
PRICE_ADJECTIVE = re.compile(
    r"\b(?:is|are|was|were|isn'?t|aren'?t|wasn'?t|weren'?t)\b[^?.!]{0,30}?\b(?:expensive|"
    r"costly|pricey)\b"
    r"|\b(?:will|would|won'?t|wouldn'?t)\b[^?.!]{0,24}?\bbe\b[^?.!]{0,14}?\b(?:expensive|"
    r"costly|pricey)\b", re.I)
PRICE_ADJECTIVE_KEEPS = re.compile(
    r"\b(?:than|or|instead|versus|vs|worth|whether|rather)\b", re.I)
PRICE_ADJECTIVE_THE_ASK_IS_LATER = re.compile(
    r"\b(?:expensive|costly|pricey)\b[^?.!]{0,30}?\b(?:can|could|should|shall|would|will|do|does|"
    r"did|am|is|are)\s+(?:i|we|you|he|she|they|it)\b", re.I)
PRICE_ADJECTIVE_WHY = frozenset(("why",))
WHAT_TO_DO = re.compile(
    r"\bwhat (?:do|should|shall|can|could|would) (?:i|we) "
    r"(?:do|say|take|try|check|avoid|ask|tell|help|start|stop|keep)\b", re.I)
WHAT_YOU_DO = re.compile(
    r"\bwhat (?:do|does|would|should|can|could) (?:you|one) (?:do|try)\s+"
    r"(?:about|with|if|when|for|to)\b", re.I)
WHAT_YOU_TAKE = re.compile(
    r"\bwhat (?:do|does|would|should|can|could|shall) (?:you|one) "
    r"(?:take|bring|pack|give|get|need|buy)\b"
    r"(?! (?:for|to do|to get|to make)\b)"
    r"|\bwhat (?:do|does|would|should|can|could|shall) (?:i|we) (?:take|bring|pack)\b"
    r"(?! (?:for|to do|to get|to make)\b)", re.I)
WHAT_I_NEED = re.compile(
    r"\bwhat (?:do|does|will|would|should|shall|might|can) (?:i|we) "
    r"(?:actually |really |even |truly |possibly |then |now )*(?:need|require)\b"
    r"(?!\s+(?:to\s+)?(?:do|know|say|ask|tell|learn|understand|work|watch|avoid|stop|prevent|"
    r"fix|deal|look|sort|handle|word|phrase)\b)", re.I)
NEED_TO_DO = re.compile(
    r"\bwhat (?:do|does|will|would|should|shall|might|can) (?:i|we) (?:need|require) to\s+"
    r"(?:do|know|say|ask|tell|learn|understand|work|watch|avoid|stop|prevent|fix|deal|look|"
    r"sort|handle|prepare|plan)\b", re.I)
WHAT_FIGURE = re.compile(
    r"\bwhat (?:temperature|temp|heat|gas mark|setting|speed|depth|size|weight|voltage)\b",
    re.I)
WHAT_AGE = re.compile(r"\bwhat age\b", re.I)
WHAT_THING_FRAGMENT = re.compile(
    r"(?:^|[,;]\s*)what (?!about\b|is\b|are\b|was\b|were\b|if\b|else\b|next\b|now\b|"
    r"size\b|time\b|colour\b|color\b|kind\b|sort\b|type\b|age\b|happens\b|went\b|works\b)"
    r"([a-z]{3,}s)\b\s*[.!?]*\s*$", re.I)
WHAT_HELPS = re.compile(
    r"\bwhat (?:helps|can help|might help|will help|would help|works)\b", re.I)
WHAT_TO_BAKE = re.compile(
    r"\bwhat (?:do|should|shall|can|could) (?:i|we|he|she|they) (?:bake|roast)\b"
    r"|\bwhat (?:do|should|shall|can|could) (?:my|our|his|her|their) \w+ (?:bake|roast)\b"
    r"|\bwhat to (?:bake|roast)\b", re.I)
WHAT_TO_OPENS = re.compile(
    r"^(?:so |and |ok |okay |now |also |please |but )?what to\b"
    r"|\b(?:i (?:don'?t|do not) know|not sure|no idea|dunno) what to\b", re.I)
WHAT_TO_PICK = re.compile(
    r"\bwhat to (?:cook|make|eat|have|drink|watch|read|listen to|wear|get|buy|order|play|study|"
    r"plant|visit|give|bring|pack)\b", re.I)
WHAT_TO_STEPS = re.compile(
    r"\bwhat to (?:do|say|write|text|reply|feed|serve|take|try|check|avoid|ask|tell|keep)\b",
    re.I)
WHAT_I_WRITE = re.compile(
    r"\bwhat (?:do|should|shall|can|could|would) (?:i|we) "
    r"(?:write|say|text|reply|word|phrase|sign)\b", re.I)
WHAT_I_GROW = re.compile(
    r"\bwhat (?:do|should|shall|can|could|would) (?:i|we) "
    r"(?:grow|sow|plant|batch|bake|roast)\b", re.I)
REPORTED = re.compile(
    r"\b(?:she|he|they|mum|dad|mom|someone|somebody|my \w+)\b.{0,25}"
    r"\b(?:asked|told|wonder\w*|wants to know|keeps asking)\b\s*"
    r"(?:(?:me|us|him|her|them|that|about|to)\s*){0,2}(?:what|whether|if)\b", re.I)
SUBSTITUTE = re.compile(
    r"\bwhat (?:do|should|shall|can|could) (?:i|we) use\b(?! (?:for|on|to)\b)"
    r"|\bwhat (?:else )?(?:do|should|shall|can|could) (?:i|we) (?:use|try|have|make)\b"
    r".{0,25}\binstead\b", re.I)
A_RECALL_ASK = re.compile(
    r"\bremind me (?:of |about |that |if |whether )"
    r"|\bremind me (?:what|when|where|who|which|how) (?!to\b)"
    r"|\bwhat (?:did|have) (?:i|we) (?:say|said|ask|asked|tell|told|mention|mentioned)\b"
    r"|\bwhat (?:was|were) (?:my|our) (?:first|last|earlier|original)\b"
    r"|\b(?:what|which) (?:was|is) the (?:first|last) (?:thing|line|question|message) i\b", re.I)
HAVE_RECALL = re.compile(r"^\W*what (?:do|did) i have\b"
                         r"(?! (?:for|on|in the|tonight|to eat|to wear|to drink))", re.I)
NOT_STEPS = re.compile(r"\bwhat (?:do|does|did) (?:i|you|we|he|she|they) do for (?:a )?living\b|"
                       r"\bwhat (?:do|does|did) (?:i|you|he|she|they) do for work\b", re.I)
OTHER_QUESTION = re.compile(r"^\W*(?:where|when|who|whose|which|why|how|is|are|was|were|can|could|"
                            r"should|shall|would|will|does|did)\b(?!\s+not\b)", re.I)
NEED_TO = re.compile(
    r"\bi (?:need|have|'ve|have got|got|'ll need|will need) to (?:"
    r"(?:sort|register|ring|call|fill|send|tell|book|apply|arrange|cancel|close|write|deal)\b"
    r"(?:\s+(?:out|up|off|in|on|with|for|about))?\s+[\w'-]+"
    r"|(?:get|find|move|do|work|set|change)\b"
    r"(?:\s+(?:out|up|off|in|to|with|for|about))?\s+"
    r"(?:the|my|his|her|their|our|a|an|this|that|these|those|it|them|him|us|me)\b"
    r")", re.I)
NEED_TO_ASKED = re.compile(
    r"\b(?:do|does|did|will|would|should|shall|can|could|might|may|must|have)\s+(?:i|we)\s+"
    r"(?:need|have|got|'ve)\s+to\b"
    r"|\b(?:what|which|how|when|where|who|why)\s+(?:\w+\s+)?(?:do|does|did|will|would|should|"
    r"shall|can|could)\s+(?:i|we)\s+(?:need|have|got|'ve)\s+to\b", re.I)
MEASURE_LABELS = frozenset(("how_long", "how_much", "how_often"))
QUESTION_IN_THE_LINE = re.compile(
    r"\b(?:what|which|where|when|who|whom|whose|why|how)"
    r"\s+(?:do|does|did|should|shall|can|could|will|would|must|is|are|am)\b"
    r"|\bhow (?:long|often|many|much)\s+(?:do|does|did|should|shall|can|could|will|would|must)\b",
    re.I)
WHERE_START = re.compile(
    r"\bwhere (?:do|does|should|shall|can|could|would|will|to) (?:\w+ ){0,3}(?:start|begin)\b"
    r"|\bwhere to (?:begin|start)\b", re.I)
ORIGIN_ASK = re.compile(r"\bwhere (?:does|do|did) (?:\w+ ){0,3}(?:come from|grow)\b", re.I)
MADE_OF = re.compile(r"\bwhat (?:is|are) (?:\w+ ){0,3}made (?:of|from|out of)\b", re.I)
ORIGIN_PERSON = re.compile(r"\bwhere (?:does|do|did) (?:you|they|we|i|he|she|u)\b", re.I)
ASKS_ITS_OWN_YES_NO = re.compile(
    r"\b(?:does|do|will|would|can|could|should|did|is|are|was|were) "
    r"(?:it|that|this|they|these|those)\b", re.I)
WHERE_POINT = re.compile(
    r"\bwhere(?:'s|s| is| was)\b[^?]{0,20}\b(?:the|any) point\b", re.I)
WHERE_RECALL = re.compile(
    r"\bwhere (?:am|was) i\b|\bwhere (?:were|are) we\b|\bwhere we (?:left|were|are)\b"
    r"|\bremind me where\b"
    r"|\b(?:know|knows|known|tell me|told me|remind|remember|forgot|forget|said)\b[^?]{0,25}\b"
    r"where (?:i|we|you) (?:live|work|are|were|went|put)\b"
    r"|\b(?:know|knows|known|tell me|told me|remind|remember|forgot|forget|said)\b[^?]{0,25}\b"
    r"where (?:he|she|they) (?:live|lives|work|works|stay|stays)\b"
    r"|\bwhere (?:does|did) (?!a |an |the )[a-z]{2,}(?: [a-z]{2,})? (?:live|work|stay)\b"
    r"|\bwhere (?:do|does|did) (?:i|you|he|she|we|they) (?:live|work|stay)\b"
    r"|\bwhere (?:do|does|did) (?:my|our|your|his|her|their) \w+(?: \w+)? (?:live|work|stay)\b"
    r"|\bwhere (?:do|does|did) i (?:decide|say|tell|mean|think|go\b[^?]{0,12}\b(?:last|before))"
    r"|\bwhere did we (?:leave off|left off|leave it|left it|get to|got to)\b"
    r"|\bwhere (?:did|do) we (?:get up to|got up to)\b"
    r"|\bwhere(?:'s|s| is| are| did i put| have i put| can i find)\b[^?]{0,20}\b"
    r"(?:my|me|our|the)\s+(?:phone|keys|key|wallet|purse|glasses|bag|bags|parcel|nappy|nappies|"
    r"coat|remote|passport|documents|bus pass|ticket|tickets)\b", re.I)
WHERE_ALONE = re.compile(
    r"^(?:and |so |ok |okay )?where(?:'s|s| is| are) (?:it|that|this)$"
    r"|^(?:and |so |ok |okay )?where (?:i|we|you) (?:live|work)$"
    r"|^where (?:do|does|did) i (?:live|work)$", re.I)


def _whole(understood):
    for key in ("plain", "text"):
        value = understood.get(key)
        if isinstance(value, str) and value.strip():
            return " ".join(value.lower().replace("\u2019", "'").split())
    return ""

HOW_TO_ANSWER = re.compile(
    r"\b(?:how|what) (?:do|should|can|could|would) i (?:answer|reply to|explain|word|phrase)\b"
    r"|\b(?:what|how) (?:do|should|would) you say when they ask\b", re.I)
WHO_AND_MEASURE = re.compile(r"\bwho\b[^?]{0,40}\b(?:what|how much|how many)\b", re.I)
WHO_OF_A_PRONOUN = re.compile(r"\bwho (?:i|you|we|they|he|she|it) (?:am|are|is|was|were)\b", re.I)
WHO_OF_A_NOUN = re.compile(
    r"\b(?:the|a|an|this|that|these|those|someone|somebody|anyone|anybody|everyone|everybody|"
    r"no one|nobody|person|people|man|woman|boy|girl|child|kid|friend|colleague|neighbour|"
    r"neighbor|boss|manager|teacher|nurse|doctor|carer|minder|babysitter)\s+who\b", re.I)

WHO_OPENS = re.compile(r"^\W*(?:(?:and|so|but|then|or|also|now|ok|okay)\s+)?who(?:'s|s|se)?\b", re.I)
BEST_WAY = re.compile(
    r"\b(?:the )?(?:best|good|right|proper|easiest|quickest|simplest|safest|cheapest|fastest) "
    r"(?:way|method|approach) (?:to|of|for)\b", re.I)
GOOD_MEASURE = re.compile(
    r"\bwhat(?:'s|s| is)\s+(?:a |an |the )?(?:really |actually |roughly |sensible |sort of )?"
    r"(?:good|decent|normal|typical|average|usual|realistic|fair)\s+(?:\w+\s+){0,2}"
    r"(?:salary|wage|wages|pay|income|rate|deposit|budget|score|pension|pot|percentage|percent"
    r"|tip(?!\s+(?:for|on|to|about)\b))\b", re.I)


GOOD_ONE = re.compile(r"\bwhat(?:'s|s| is) (?:a |an )?good\b", re.I)
GIVE_ME_ONE = re.compile(
    r"\b(?:gimme|give me|show me|send me)\s+(?:a|an|one|another)\s+([a-z][a-z'-]*)", re.I)
GIVE_ME_A_FEW = re.compile(
    r"\b(?:gimme|give me|show me|send me)\s+(?:some|a few|couple of|a couple|any)\s+"
    r"([a-z][a-z'-]*)", re.I)
GIVE_ME_NOT_A_THING = re.compile(
    r"\b(?:human|person|somebody|someone|real person|operator|manager)\b", re.I)
GIVE_ME_AN_IDIOM = re.compile(
    r"\b(?:a|an|one)\s+(?:rough\s+idea|minute|minutes|second|seconds|sec|secs|mo|moment|break|"
    r"chance|ring|rings|shout|call|lift|ride|hand|hands|hint|clue|tip|tips|way|method|reason|"
    r"sign|excuse|rest|try|kiss|discount|picture|photo|image)\b", re.I)
GIVE_ME_MADE_UP = re.compile(
    r"\b(?:limerick|poem|haiku|riddle|joke|story|tale|rhyme|tongue twister|fun fact|"
    r"fact|quiz question|trivia question|general knowledge question|question|example|"
    r"routine|prompt|toast|speech|plan|itinerary|list|recipe)\b", re.I)
GIVE_ME_LEAD_IN = frozenset((
    "ok", "okay", "so", "and", "now", "then", "just", "please", "also", "but", "you", "could",
    "can", "would", "will", "hi", "hey", "gimme", "me", "of", "if", "maybe", "alright"))


def _the_give_is_to_the_bot(said, at):
    before = said[:at].split()
    return not before or before[-1] in GIVE_ME_LEAD_IN

A_THING_TO_GIVE = re.compile(r"\b(?:gift|gifts|present|presents|pressie|pressies|"
                             r"stocking filler|secret santa)\b", re.I)
A_PERSON_TO_GIVE = (r"(?:my|our|his|her|their|him|them|mum|mam|mom|dad|mother|father|sister|"
                    r"brother|son|daughter|nan|nana|grandma|grandad|granny|grandpa|gran|aunt|"
                    r"uncle|cousin|friend|mate|bestie|teacher|colleague|boss|partner|wife|"
                    r"husband|boyfriend|girlfriend|neighbours?|baby|newborn|toddler|child|kid|"
                    r"boy|girl|teenager|nephew|niece|in-laws?|flatmate|housemate|carer|"
                    r"\d+\s*(?:year|yr)s?\s*old)")
GIVING_FRAME = re.compile(
    r"\b(?:for|to)\s+(?:a|an|the)?\s*" + A_PERSON_TO_GIVE + r"\b"
    r"|\bwhat (?:should i |shall i |do i |can i |would you |to )?(?:get|buy|make|give)\b"
    r"|\b(?:idea|ideas|suggest|suggestion|suggestions|recommend|recommendation)\b", re.I)
NOT_A_GIVING_THING = re.compile(
    r"\bgift (?:card|cards|voucher|vouchers|wrap|wrapping|box|boxes|receipt|set)\b"
    r"|\bpresent (?:tense|day|perfect)\b|\bgift (?:aid|tax|taxable)\b"
    r"|\b(?:letter|note|thanks|thank you|receipt|return|returns)\b"
    r"|\b(?:keeps?|kept|always)\b[^?]{0,25}\b(?:gift|present)s?\b"
    r"|\b(?:buys|bought|gives|gave|brings|brought|receives|received)\b[^?]{0,20}\b(?:gift|present)s?\b",
    re.I)
HOW_COME = re.compile(r"\bhow come\b|\bhow is it that\b", re.I)
BEST_OF_MANY = re.compile(
    r"\bwhat (?:are|were) (?:the )?(?:best|main|top|nicest|cheapest|better)\b"
    r"|\bwhat (?:are|were) (?:some|a few|any)\b"
    r"|\bwhat (?:are|were) (?:the )?\w+ (?:to|for)\b", re.I)
A_PRICE_ASK = re.compile(
    r"\b(?:is|are|was|were)\s+(?:it|that|this|these|those|they|there|one)\s+"
    r"(?:(?:too|so|really|actually|very|quite)\s+)?"
    r"(?:expensive|pricey|dear|cheap|costly)\b", re.I)
NOT_A_PRICE_ASK = re.compile(r"\bworth\b|\bcheaper than\b|\bmore expensive than\b|\bafford", re.I)
WHAT_ARE_MINE = re.compile(
    r"\bwhat(?:'s| is| are|s)\b[^?]{0,40}?\b(?:my|our) (?:[a-z]+ ){0,2}"
    r"(?:rights?|entitlements?|obligations?)\b", re.I)

MY_THING_CALLED = re.compile(
    r"\bwhat (?:are|is|were|was) (?:my|our)\b[^?]{0,30}?\b(?:called|named)\b", re.I)
RECALL_OF_MINE = re.compile(
    r"\bremind(?:ing)? me (?:what|who|which|where|when)\b"
    r"|\bwhat (?:did|do) i (?:say|told you|tell you|tell u|ask|asked|decide|choose)\b"
    r"|\bwhat (?:was|am) i (?:saying|doing|about to say)\b", re.I)

ASKS_FOR_MEANING = re.compile(
    r"\bwhat (?:is|are|was|were|'s)\b"
    r"|\bwhat (?:does|do)\b(?:(?!\bwhat\b)[^?]){0,30}?"
    r"\b(?:do|does|include|includes|cover|covers|contain|contains|show|shows|sound like)\b"
    r"|\bwhat do you call\b|\b(?:mean|means|meaning|stand for|stands for|short for)\b"
    r"|\bdifference between\b", re.I)
STEPS_ARE_COUNTED = re.compile(
    r"\b\d[\d,]*\s*(?:k\s+)?steps?\b"
    r"|\bsteps? count\b"
    r"|\bsteps? (?:a|per|each|every) (?:day|week|month|hour|mile|km|kilometre)\b", re.I)
STEPS_AS_A_DISTANCE = re.compile(
    r"\bsteps? (?:in|into|to|per|versus|vs)\s+(?:a |one )?(?:mile|miles|km|kilometre|kilometres|"
    r"kilometer|kilometers)\b"
    r"|\b(?:mile|miles|km|kilometre)s? (?:in|to|from|of) (?:a |one )?\d[\d,]*\s*(?:k\s+)?steps?\b",
    re.I)


HOW_ASK_FORM = re.compile(
    r"\bhow (?:much|many|long|often|soon|far|tall|big|heavy|old|hot|cold)\s+"
    r"(?:is|are|was|were|does|do|did|will|would|can|could|should|shall|much|many|far)\b", re.I)
HOW_MANY_TIME = re.compile(
    r"\bhow (?:many|much) (?:more |longer )?(?:seconds?|secs?|minutes?|mins?|hours?|hrs?|days?|"
    r"weeks?|months?|years?|nights?|time)\b", re.I)
A_SIZE_LONG = re.compile(
    r"\b\d+(?:\.\d+)?\s*(?:mm|cm|m|km|metres?|meters?|feet|foot|ft|inches?|in|yards?|yds?)\s+"
    r"(?:long|wide|high|deep|tall|thick)\b", re.I)
A_DURATION_WORD = re.compile(
    r"\b(?:take|takes|took|taking|last|lasts|lasted|lasting|keep|keeps|kept|stay|stays|sit|sits|"
    r"wait|waiting|seconds?|secs?|minutes?|mins?|hours?|hrs?|days?|weeks?|months?|years?|"
    r"overnight|fortnight|fortnightly)\b", re.I)


REASON_ASK = re.compile(
    r"\bhow come\b|\bwhat (?:causes|caused|causing|is causing)\b|"
    r"\bwhat(?:'?s| is| was)?\s+(?:causing|making|the cause|the reason)\b|"
    r"\bwhat (?:makes|made) (?:you|me|us|people|him|her|them|it|this|that|someone|"
    r"my|your|our|their|his|its)\b|"
    r"\bwhat (?:makes|made) (?:the |a |an )?[a-z']+(?:(?: and| or) (?:the |a |an )?[a-z']+)*\s*$",
    re.I)
DOING_WRONG = re.compile(
    r"\bwhat(?:'?s| is| was)?\s+(?:going\s+|gone\s+)?wrong\b"
    r"|\bwhat (?:went|had gone|has gone|have gone) wrong\b"
    r"|\bwhat (?:could|might|may|would) be (?:wrong|making|causing)\b"
    r"|\bwhat (?:am i|are we|did i|did we|have i|have we) (?:do|doing|done|did|get|getting|got|"
    r"have|having|had)\b.{0,25}\bwrong\b"
    r"|\bwhat (?:do i|do we|does he|does she|do they) do wrong\b"
    r"|\bwhere (?:am i|are we|did i|did we|do i|do we) going wrong\b"
    r"|\bwhat(?:'?s| is| was)?\s+(?:the|my|our|his|her|their)\s+(?:problem|trouble|issue|fault)\s+"
    r"(?:with|in)\b", re.I)
WRONG_ASKED_ABOUT = re.compile(r"\b(?:mean|means|meaning|meant|called|spell|spelled|word)\b", re.I)
WRONG_RECALL = re.compile(
    r"\bremind me\b|\bwhat (?:was|were)\b[^?]{0,30}\b(?:wrong|problem|trouble|issue|fault)\b"
    r"|\b(?:wrong|problem|trouble|issue|fault)\b[^?]{0,20}\bagain\b", re.I)

POINT_ASK = re.compile(
    r"\bwhat(?:'?s| is| was)?\s+the point (?:of|in)\s+(\w+(?: \w+){0,2})"
    r"|^(?:any )?point (?:of|in)\s+(\w+(?: \w+){0,2})", re.I)
POINT_NOT_A_THING = frozenset("""
    it this that these those anything everything nothing any all carrying carry continuing going
    living life you me us them anymore honestly really now boiling freezing melting smoke
    """.split())


FOLLOWUP = re.compile(
    r"^\s*(?:and|so|then|but|ok(?:ay)?[,\s]+(?:and|so)|what\s+about|how\s+about|what\s+if|"
    r"would\s+that|does\s+that|same\s+(?:for|with))\b", re.I)
NEW_ASK = re.compile(r"\bwhat (?:do|does|should|shall|can|could|will|would) (?:i|we|you)\b", re.I)
RECALL_SAID = re.compile(
    r"\b(?:did|do)\s+(?:i|you)\s+(?:say|said|told|tell|mention|remember)\b", re.I)
RECALL_NOT = re.compile(
    r"\b(?:what|anything|something)\s+(?:do|does|should|can|could)\s+(?:i|you)\s+(?:say|tell)\b"
    r"|\bhow\s+(?:do|does|can|could|should|would)\s+(?:i|you|we|u|ya)\s+tell\b", re.I)
RECALL_TIME = re.compile(
    r"^(?:when|what\s+time|what\s+date|what\s+day|how\s+(?:long|soon|often)"
    r"|how\s+many\s+(?:weeks|days|months|years|hours|minutes|nights|times))\b", re.I)
RECALL_AMOUNT = re.compile(
    r"^(?:how\s+(?:much|many|old|heavy|tall|far|big)|what\s+age|what\s+size)\b", re.I)
RECALL_PLACE = re.compile(r"^where\b", re.I)
RECALL_PERSON = re.compile(r"^(?:who|what\s+name|(?:her|his|their|my|our)\s+name)\b", re.I)
RECALL_KIND_NOUN = {
    "budget": AMOUNT, "rent": AMOUNT, "hours": AMOUNT, "shift": AMOUNT, "salary": AMOUNT,
    "wage": AMOUNT, "target": AMOUNT, "apr": AMOUNT, "age": AMOUNT, "size": AMOUNT,
    "name": PERSON, "day": TIME, "date": TIME, "time": TIME,
}
RECALL_PRONOUN = re.compile(r"^(?:you|me|us|it|that|then)\s+", re.I)
RECALL_KIND_NOUN_ASK = re.compile(
    r"^(?:my|our)\s+(budget|rent|hours|shift|salary|wage|target|apr|age|size|name|day|date|time)\b",
    re.I)


def _recall_wants(said, line=""):
    whole = " ".join((line or said).lower().replace("\u2019", "'").split())
    if not whole or not RECALL_SAID.search(whole) or RECALL_NOT.search(whole):
        return None
    for match in RECALL_SAID.finditer(whole):
        after = RECALL_PRONOUN.sub("", whole[match.end():].strip())
        kind = (_recall_kind_in_front(after) or _recall_kind_named(after)
                or _recall_kind_behind(whole[:match.start()]))
        if kind:
            return kind
    return None


def _recall_kind_in_front(after):
    for pattern, kind in ((RECALL_TIME, TIME), (RECALL_AMOUNT, AMOUNT),
                          (RECALL_PLACE, PLACE), (RECALL_PERSON, PERSON)):
        if pattern.match(after):
            return kind
    return None


def _recall_kind_named(after):
    noun = RECALL_KIND_NOUN_ASK.match(after)
    return RECALL_KIND_NOUN[noun.group(1).lower()] if noun else None


RECALL_SHAPE_BEFORE = re.compile(
    r"(?:\bwhen|\bwhat\s+time|\bwhat\s+date|\bwhat\s+day|\bhow\s+(?:long|soon|often)"
    r"|\bhow\s+many\s+(?:weeks|days|months|years|hours|minutes|nights|times)"
    r"|\bhow\s+(?:much|many|old|far)|\bwhat\s+age|\bwhat\s+size|\bwhere|\bwho"
    r"|\bwhat\s+name)\s*$", re.I)
RECALL_SHAPE_BEFORE_KIND = (
    (("when", "what time", "what date", "what day", "how long", "how soon", "how often"), TIME),
    (("how many weeks", "how many days", "how many months", "how many years", "how many hours",
      "how many minutes", "how many nights", "how many times"), TIME),
    (("how much", "how many", "how old", "how far", "what age", "what size"), AMOUNT),
    (("where",), PLACE),
    (("who", "what name"), PERSON),
)


def _recall_kind_behind(before):
    match = RECALL_SHAPE_BEFORE.search(before)
    if not match:
        return None
    named = " ".join(match.group(0).lower().split())
    for words, kind in RECALL_SHAPE_BEFORE_KIND:
        for word in words:
            if named == word or named.startswith(word + " "):
                return kind
    return None


def asks_a_follow_up(understood):
    if not isinstance(understood, dict) or understood.get("asks_a_verdict"):
        return False
    said = _said(understood)
    if not FOLLOWUP.search(said):
        return False
    if set(understood.get("asks") or ()) - {"what", "yesno"}:
        return False
    if NEW_ASK.search(said):
        return False
    kind = understood.get("kind")
    if kind == "question" or said.rstrip().endswith("?"):
        return True
    line = str(understood.get("plain") or understood.get("text") or "")
    return kind == "statement" and bool(understood.get("followup")) and len(line.split()) <= 6


_ASK_CLAUSE_SPLIT = re.compile(r"\s*(?:[,;:]|\band\b|\bbut\b|\bso\b|\bthen\b)\s*", re.I)
_TRAILING_MEASURE = re.compile(
    r"\b(?:how long|how soon|what time)\s*[.?!]*$", re.I)
_MEASURE_THEN_VERB = re.compile(
    r"\b(?:how long|how soon|what time)\s+"
    r"(?:do|does|did|will|would|should|shall|can|could|is|are|was|were|to|till|until|before|"
    r"in|on|for|per|at|with|by|after|into|under|over|about|from)\b",
    re.I)
_TALKING_ABOUT_A_LENGTH = re.compile(
    r"\b(?:i|we|you|they|he|she)\s*(?:did ?n[o']t|do ?n[o']t|does ?n[o']t|never)?\s*"
    r"(?:know|knew|realise|realize|remember|wonder|wondered|sure|idea)\b"
    r"|\b(?:amazing|surprising|interesting|funny|odd|strange) how (?:long|soon|much|many|often)\b"
    r"|\bno idea how\b|\bhow long it (?:takes|took|would take|will take)\b", re.I)


def _a_fragment_asks_for_a_time(said):
    if _TALKING_ABOUT_A_LENGTH.search(said or ""):
        return False
    return bool(_TRAILING_MEASURE.search(said or "") or _MEASURE_THEN_VERB.search(said or ""))


_ASK_CLAUSE_OPENS = re.compile(
    r"^(?:when|what|which|how|where|who|why|whom|whose|should|shall|can|could|do|does|did|will|"
    r"would|is|are|was|were|am|have|has|had)\b", re.I)


def _the_ask_clause(said):
    parts = [part.strip() for part in _ASK_CLAUSE_SPLIT.split(said or "") if part.strip()]
    if len(parts) < 2:
        return ""
    last = parts[-1]
    return last if _ASK_CLAUSE_OPENS.match(last) else ""


def wants(understood, before=None):
    if not isinstance(understood, dict):
        return None
    if A_RECALL_ASK.search(_said(understood) or ""):
        return None
    own = _wants_alone(understood)
    own = _the_shape_named_outside_the_reading(understood, own)
    if own:
        return own
    if _a_bare_definition(understood):
        return MEANING
    if before and asks_a_follow_up(understood):
        return before
    return None

CONFIRM_CAUSE = re.compile(
    r"(?:^|[;,.]\s*|\b(?:and|so|but|then)\s+)(?:is|was) (?:that|this|it) why\b", re.I)
IF_IT_HAPPENS = re.compile(r"^\W*(?:and\s+|so\s+|but\s+|then\s+)?if\b", re.I)
ASK_TO_ASK = re.compile(r"\bshould i (?:ask|explain|check|say|mention|bring up)\s+why\b", re.I)
A_FIGURE_NAMED = re.compile(
    r"\bwhat (?:age|price|cost|number|salary|pay|wage|rate|fee|dose|dosage|amount|percentage|"
    r"percent|discount|charge|quote|score|mark|grade|figure|budget)\b", re.I)
WHAT_TIME_NAMED = re.compile(r"\bwhat time\b", re.I)


def _the_shape_named_outside_the_reading(understood, own):
    said = _said(understood) or ""
    if not said:
        return own
    if IF_IT_HAPPENS.match(said):
        return own
    if own == REASON and CONFIRM_CAUSE.search(said):
        return YESNO
    if own in (None, REASON, MEANING) and ASK_TO_ASK.search(said):
        return YESNO
    if own is None and A_FIGURE_NAMED.search(said):
        return TIME if WHAT_TIME_NAMED.search(said) else AMOUNT
    return own



def wanted(memory):
    if not isinstance(memory, dict):
        return None
    read = memory.get("understood")
    if isinstance(read, dict):
        want = read.get("wants")
        if want in WANTS:
            return want
    want = memory.get("intent_wants")
    return want if want in WANTS else None


def _wants_alone(understood):
    asked_back = _recall_wants(_said(understood), _whole(understood))
    if asked_back:
        return asked_back
    if understood.get("about_bot"):
        return None
    if understood.get("asks_a_verdict"):
        return YESNO
    if OPEN_WHO_HELP.search(_said(understood)):
        return PERSON
    said = _said(understood)
    typed = _whole(understood) or said
    if understood.get("help_ask"):
        return None if _a_help_ask_that_names_nothing(typed) else STEPS
    asks = understood.get("asks")
    asks = set(asks) if isinstance(asks, (list, tuple, set)) else set()
    if understood.get("intent") == "news":
        dropped = {"choice"}
        if not (SUM_OUT_LOUD.search(said) or SUM_ASKS.search(said)):
            dropped.add("maths")
        asks -= frozenset(dropped)
    asking = (understood.get("kind") == "question"
              or understood.get("intent") in ("question", "request")
              or bool(HOW_ASK_FORM.search(said))
              or (bool(QUESTION_IN_THE_LINE.search(said))
                  and not REPORTED.search(said)))
    if HOW_ARE_YOU.match(said):
        return None
    if HOW_IT_WENT.search(said):
        return None
    if HOW_IT_HAPPENED.search(said):
        return REASON
    if HELP_ME.search(said):
        return STEPS
    if HELP_ASK_ANY.search(typed):
        return None if _a_help_ask_that_names_nothing(typed) else STEPS
    if asking and not REPORTED.search(said) and DOING_WRONG.search(said) \
            and not WRONG_ASKED_ABOUT.search(said) and not WRONG_RECALL.search(said):
        return REASON

    if FIX_ASK.search(said) and not re.match(r"\s*(?:is|are|can|could|will|would|do|does)\b", said):
        return STEPS
    if WHERE_START.search(said) or BEST_WAY.search(said):
        return STEPS
    if NEED_TO.search(said) and not NEED_TO_ASKED.search(said) \
            and not (asks - {"maths", "choice", "write"}):
        return STEPS
    if WHERE_POINT.search(said):
        return None
    if WHERE_RECALL.search(said) or WHERE_ALONE.search(_whole(understood)):
        return None
    if HOW_TO_ANSWER.search(said):
        return STEPS
    if (PRICE_IDIOM.search(said) and asking
            and re.search(r"\b(?:what|how much)\b", said)):
        return AMOUNT
    if HOW_COME.search(said):
        return REASON
    if ("steps" in asks and HOW_I.search(said) and not COMPARE_MYSELF.search(said)
            and not (("maths" in asks or "how_much" in asks) and re.search(r"[0-9]", said))):
        return STEPS
    if STEPS_ASK.search(said) and not (COUNTED_STEPS.search(said)
                                       and not re.search(r"\bhow (?:do|can|should) i\b", said)):
        return STEPS
    if MEMBERS_ASK.search(said):
        return OPTIONS
    if KINDS_OF.search(said) and not NOT_KINDS_OF.search(said):
        return OPTIONS
    if (COMPARISON.search(said) or COMPARED.search(said)) \
            and not NOT_A_COMPARISON.search(said) \
            and _names_a_pair(said) and _asks_about_them(understood, said):
        return COMPARE
    if (ORIGIN_ASK.search(said) and not ORIGIN_PERSON.search(said)) or MADE_OF.search(said):
        return MEANING
    if BEST_OF_MANY.search(said) and not (COST_ASK.search(said) and asks <= COST_STANDS_IN):
        return OPTIONS
    if ("definition" in asks and WHAT_ARE_MINE.search(said)
            and not re.search(r"\b(?:called|mean|means|meaning|stand for|stands for)\b", said)):
        return STEPS
    if MY_THING_CALLED.search(said):
        return None
    if ("definition" in asks and re.search(r"\bwhat does\b", said)
            and not ASKS_FOR_MEANING.search(said)):
        asks.discard("definition")
    if "definition" in asks and not asking and not ASKS_FOR_MEANING.search(said):
        asks.discard("definition")
    if GOOD_MEASURE.search(said):
        return AMOUNT
    if GOOD_THING.search(said) and "definition" in asks and not GOOD_FIGURE_WORD.search(said):
        return STEPS if GOOD_WAY.search(said) else OPTIONS
    if HOW_IT_WORKS.search(said) and not re.search(r"\bhow do i\b", said, re.I):
        return MEANING
    if "who" in asks and not WHO_OPENS.match(said) and _a_who_a_person_owns(understood):
        asks.discard("who")
    if "who" in asks and (WHO_AND_MEASURE.search(said) or WHO_OF_A_PRONOUN.search(said)
                          or (WHO_OF_A_NOUN.search(said) and not WHO_OPENS.match(said))):
        asks.discard("who")
    if "where" in asks and WHERE_MONEY_GOES.search(said):
        return STEPS
    if "where" in asks and (asks & frozenset(("yesno", "recommend"))) \
            and WHERE_RELATIVE.search(said) and not ASKS_TO_BE_TOLD_WHERE.search(said):
        asks.discard("where")
    if LONG_TIME.search(said):
        asks.discard("how_long")
        asks.discard("how_often")
    if CONVERSION.search(said) or CONVERTED_FIGURE.search(said):
        return AMOUNT
    if NOT_A_FIGURE.search(said):
        return None
    if asks & MEASURE_LABELS and asking:
        if "how_long" in asks and WRITTEN_THING.search(said):
            return AMOUNT
        if "how_long" in asks and THING_THAT_EXTENDS.search(said):
            return AMOUNT
        if "how_long" in asks and "steps" in asks and METHOD_OPENS.match(LEADING_JOIN.sub("", said)):
            return STEPS
        if "how_long" in asks and A_SIZE_LONG.search(said) and not A_DURATION_WORD.search(said):
            if "how_much" in asks or "how_many" in asks or re.search(r"\bhow (?:much|many)\b", said):
                asks.discard("how_long")
                return AMOUNT
            return None
        return TIME if "how_long" in asks or HOW_MANY_TIME.search(said) else AMOUNT
    if (WHAT_DOES_MEASURE.search(said) and not ASKS_FOR_MEANING.search(said)
            and not COSTS_NOTHING.search(said)):
        return AMOUNT
    if WHAT_IS_PER.search(said):
        return AMOUNT
    if "how" in asks:
        if HOW_SOON.search(said):
            return TIME
        if HOW_MEASURE.search(said):
            return AMOUNT
        if HOW_MEASURE_HEAD.match(LEADING_JOIN.sub("", said)):
            return AMOUNT
        if HOW_TO_DO.search(said):
            asks.discard("definition")
    if _a_fragment_asks_for_a_time(said):
        return TIME
    asked = LEADING_JOIN.sub("", said)
    focus = understood.get("asking") or understood.get("focus")
    focus_said = (" ".join(str(w) for w in focus) if isinstance(focus, (list, tuple))
                  else focus if isinstance(focus, str) else "")
    if (WHEN_ASKS.match(asked) or WHEN_ASKS.match(LEADING_JOIN.sub("", focus_said.strip()))) \
            and not WHICH_DAY_IS_BEST.search(said):
        return TIME
    ask_clause = _the_ask_clause(said) if asking else ""
    if (ask_clause and WHEN_ASKS.match(LEADING_JOIN.sub("", ask_clause))
            and not WHICH_DAY_IS_BEST.search(said)):
        return TIME
    if WHAT_ARE_TIMES.match(said) and not REPORTED.search(said) and not re.search(
            r"\b(?:called|mean|means|meaning|stand for)\b", said):
        return TIME
    if A_GOOD_TIME.search(said):
        return YESNO
    if GOOD_FIGURE.search(said) and not VERDICT_FRAME.match(said):
        return TIME if re.search(r"\b(?:time|timeframe)\b", said) else AMOUNT
    if JUDGED_MEASURE.search(said) and asking and not ON_THE_CLOCK.search(said) \
            and not REPORTED.search(said) and not ASKS_YES_OR_NO.match(LEADING_JOIN.sub("", said)):
        return AMOUNT
    if GOOD_ONE.search(said):
        return OPTIONS
    if asking and not GIVE_ME_NOT_A_THING.search(said) and not GIVE_ME_MADE_UP.search(said) \
            and not GIVE_ME_AN_IDIOM.search(said) and "list" not in asks:
        found = GIVE_ME_A_FEW.search(said)
        if found and _the_give_is_to_the_bot(said, found.start()):
            return OPTIONS
        found = GIVE_ME_ONE.search(said)
        if found and _the_give_is_to_the_bot(said, found.start()):
            return PICK
    if (A_THING_TO_GIVE.search(said) and GIVING_FRAME.search(said)
            and "yesno" not in asks and not NOT_A_GIVING_THING.search(said)):
        return OPTIONS
    if WHAT_FIGURE.search(said) or WHAT_AGE.search(said):
        return AMOUNT
    if NEED_TO_DO.search(said):
        return STEPS
    if WHAT_HELPS.search(said) or WHAT_YOU_TAKE.search(said) or WHAT_I_NEED.search(said):
        return OPTIONS
    if WHAT_YOU_DO.search(said):
        return STEPS
    if not REPORTED.search(said) and not OTHER_QUESTION.match(said):
        if WHAT_I_WRITE.search(said):
            return STEPS
        if WHAT_I_GROW.search(said):
            return OPTIONS
    if WHAT_TO_BAKE.search(said):
        return OPTIONS
    if WHAT_THING_FRAGMENT.search(said) and not SUBSTITUTE.search(said):
        return PICK
    if DO_WITH_A_PERSON.search(said):
        return None
    if asking and (WHAT_CAN_I_DO_WITH.search(said) or WHAT_SHOULD_I_DO_WITH.search(said)):
        if asks & PICK_SIDES:
            return PICK
        if WHAT_SHOULD_I_DO_WITH.search(said):
            return STEPS
        return OPTIONS
    if WHAT_ELSE_WITH.search(said):
        return OPTIONS
    if WHAT_ELSE_STEPS.search(said):
        return STEPS
    if (PICK_ONE.search(said) or PICK_ONE_OF_A_KIND.search(said)
            or (WHAT_TO_OPENS.search(said) and WHAT_TO_PICK.search(said))):
        return None if HAVE_RECALL.match(said) else PICK
    if SUBSTITUTE.search(said):
        return OPTIONS
    if PAIRING_ASK.search(said) and not REPORTED.search(said):
        return OPTIONS
    if ((WHAT_TO_DO.search(said)
         or (WHAT_TO_OPENS.search(said) and WHAT_TO_STEPS.search(said)))
            and not REPORTED.search(said) and not NOT_STEPS.search(said)
            and not OTHER_QUESTION.match(said)):
        return STEPS
    if asking and not REPORTED.search(said) and REASON_ASK.search(said):
        return REASON
    found = POINT_ASK.search(said)
    if found and not ASKS_ITS_OWN_YES_NO.search(said):
        thing = (found.group(1) or found.group(2) or "").split()
        if thing and thing[0] not in POINT_NOT_A_THING:
            return REASON
    if (asks <= ({"recommend"} | MEASURE_LABELS) and not said.rstrip().endswith("?")
            and not ASKS_OUT_LOUD.match(said)
            and not TAIL_VERDICT_ASK.search(_whole(understood))):
        return None
    if DIFFERENCE.search(said):
        return MEANING
    if asks & PICK_SIDES:
        return PICK
    if STEPS_ARE_COUNTED.search(said) or STEPS_AS_A_DISTANCE.search(said):
        asks.discard("steps")
        if STEPS_AS_A_DISTANCE.search(said):
            return AMOUNT
    if (PRICE_ADJECTIVE.search(said) and not PRICE_ADJECTIVE_KEEPS.search(said)
            and not PRICE_ADJECTIVE_THE_ASK_IS_LATER.search(_line_text(understood.get("text")))
            and not asks & PRICE_ADJECTIVE_WHY):
        return AMOUNT
    if PRICE_ADJECTIVE.search(said) and asks & PRICE_ADJECTIVE_WHY:
        return REASON
    if A_PRICE_ASK.search(said) and not NOT_A_PRICE_ASK.search(said):
        return AMOUNT
    if RECALL_OF_MINE.search(said):
        asks.discard("yesno")
    if "yesno" in asks and not (asks & SPECIFIC_ASKS):
        return YESNO
    if COST_ASK.search(said) and asks <= COST_STANDS_IN:
        return AMOUNT
    if A_FIGURE_OF_A_MONEY_VERB.search(said) and not MONEY_VERB_NOT_A_PRICE.search(said):
        return AMOUNT
    if WHAT_CAN_I_DO.search(said) and not asks & PICK_SIDES:
        return STEPS
    for shape, labels in ASKED_FOR:
        if (asks - (frozenset() if asking else MEASURE_LABELS)) & labels:
            if (shape == PICK and "recommend" in labels
                    and A_FEW_THINGS.search(said)):
                return OPTIONS
            if shape == AMOUNT and "maths" in asks and "how_much" not in asks and \
                    understood.get("kind") != "question" and \
                    not (SUM_OUT_LOUD.search(said) or SUM_ASKS.search(said)):
                continue
            return shape
    if TAIL_VERDICT_ASK.search(_whole(understood)):
        return YESNO
    return None


TAIL_VERDICT_ASK = re.compile(
    r"\b(?:is|was|are)\s+(?:it|that|this)\s+(?:worth it|worth|ok|okay|fine|right|normal|bad|"
    r"a good (?:idea|plan|buy|choice))[\s.?!]*$", re.I)


NOT_A_VERB_HEAD = re.compile(
    r"^(?:a|an|the|it|it's|its|there|this|that|these|those|they|them|we|you|i|he|she|both|all|"
    r"some|most|many|one|two|three|four|five|six|seven|eight|nine|ten|from|in|at|on|for|to|with|"
    r"without|after|before|about|around|once|if|when|until|roughly|up|down|by|as|of|no|not|"
    r"nothing|nobody|never|always|usually|often|your|my|our|his|her|their|every|each|another|"
    r"any|much|little|few|several|such|what|who)\b", re.I)


I_OFFER = re.compile(
    r"\b(?:i'll|i will|i can|i'd|we'll|we can|let me|i've|i would)\b", re.I)

ASKS_THE_BOT = re.compile(r"\b(?:can|could|would|will)\s+(?:you|u)\b|\bdo you\b|\bare you\b", re.I)


A_UNIT = re.compile(
    r"\d|\b(?:mg|g|kg|ml|l|litres?|liters?|cm|mm|metres?|meters?|feet|foot|inches?|degrees?|c|f|"
    r"hours?|hrs?|minutes?|mins?|seconds?|days?|weeks?|months?|years?|nights?|p|pence|pounds?|"
    r"quid|grams?|calories|kcal|watts?|kw|kwh|amps?|volts?|per\s+cent|%)\b", re.I)


def _an_amount_with_a_unit(opening):
    return bool(_an_amount(opening)) and bool(A_UNIT.search(opening))


POINTS_BACK = re.compile(r"^(?:it|it's|this|that|these|those|they|them|there|its)\b", re.I)

NOT_A_THING = frozenset((
    "the", "and", "for", "you", "not", "but", "all", "any", "one", "two", "are", "was", "has",
    "had", "how", "why", "who", "did", "may", "can", "its", "our", "per", "via", "yet", "own",
    "off", "out", "too", "get", "put", "use", "let", "now", "far", "lot", "bit", "way", "she",
    "him", "her", "his", "new", "old", "few", "yes", "them", "they", "their", "there", "then",
    "that", "this", "with", "from", "your", "have", "what", "when", "will", "would", "could",
    "should", "about", "into", "over", "just", "only", "even", "still", "much", "many", "some",
    "very", "also", "been", "being", "does", "done", "more", "most", "less", "like", "need",
    "want", "make", "made", "going", "were", "than", "such", "each", "both", "else", "said",
))


def _about_the_thing_the_line_named(opening, said):
    words = _words(opening)
    wide = bool(POINTS_BACK.match(opening)) or _an_instruction(opening)
    head = set(words) if wide else set(words[:5])
    for word in set(_words(said)):
        if len(word) < 3 or word in _EMPTY or word in NOT_A_THING:
            continue
        if word in head:
            return True
        for stem in (word[:-1], word[:-2]):
            if len(stem) < 3 or stem in _EMPTY or stem in NOT_A_THING:
                continue
            if stem in head:
                return True
    return bool(set(re.findall(r"\d+", opening)) & set(re.findall(r"\d+", said)))


METHOD_VERBS = re.compile(
    r"^(?:lower|brown|mash|crush|sprinkle|grease|steam|blend|scatter|lay|shake|score|chill|thaw|"
    r"reheat|serve|strain|sieve|portion|layer|arrange|thread|screw|hammer|nail|clamp|level|"
    r"preheat|dust|wring|drape|tuck|loop|knot|peg|hoover|vacuum|mop|air|cure|rest)\b", re.I)


def _an_instruction(opening):
    if (INSTRUCTS.match(opening) or JOB.match(opening) or METHOD_VERBS.match(opening)
            or MEANS_OF.search(opening)):
        return True
    words = _words(opening)
    if len(words) < 2 or NOT_A_VERB_HEAD.match(opening):
        return False
    second = words[1]
    return not (second.endswith("s") and not second.endswith("ss"))


OPTIONS_ASK = re.compile(
    r"\b(?:what|wat|wot|wats)\s+(?:are|r)\s+(?:my|the|our|his|her|their)\s+"
    r"(?:other\s+|main\s+)?options?\b", re.I)
WHAT_CAN_I_DO = re.compile(r"\bwhat (?:can|could) (?:i|we) do\b", re.I)
WHAT_CAN_I_DO_WITH = re.compile(r"\bwhat (?:(?:can|could) (?:i|we)|to) do with\b", re.I)
WHAT_SHOULD_I_DO_WITH = re.compile(
    r"\bwhat (?:should|shall|do|did|would|might) (?:i|we) do with\b", re.I)
ANY_DO_WITH = re.compile(r"\bwhat (?:to|(?:can|could|should|shall|do|did) (?:i|we)) do with\b", re.I)
DO_WITH_A_PERSON = re.compile(
    r"\b(?:do|does|doing) with (?:myself|yourself|himself|herself|ourselves|yourselves|"
    r"themselves|him|her|each other)\b", re.I)


def _do_with_ask(said):
    return bool(ANY_DO_WITH.search(said))

CHOICE = re.compile(r"\bor\b", re.I)

WORDS_ASK = re.compile(
    r"\bhow (?:do|can|could|should|would) (?:i|we|you) "
    r"(?:tell|say|ask|word|phrase|put it|bring (?:it|this|that) up|raise (?:it|this|that)|mention|approach)\b"
    r"|\bhow to (?:tell|say|ask|word|phrase|bring (?:it|this|that) up|raise (?:it|this|that))\b"
    r"|\bwhat (?:should|shall|do|can|could|would) (?:i|we) "
    r"(?:say|tell|text|write|ask|reply|answer|word it|phrase it)\b"
    r"|\bwhat to (?:say|tell)\b|\bwhat should be said\b"
    r"|\b(?:dont|don't|do not|didnt|didn't|never|no idea) (?:know )?(?:quite |really )?"
    r"(?:how|what) to (?:say|tell|word|phrase|ask)\b"
    r"|\b(?:idk|dunno|no idea) (?:how|what) to (?:say|tell|word|phrase|ask)\b"
    r"|\bhow (?:should|do) i (?:break|ease) it to\b|\bbreak it to\b"
    r"|\b(?:cant|cannot|can't|dont|don't|struggling to) (?:find|think of) (?:the )?(?:right |proper )?words\b"
    r"|\b(?:find|finding|choose|need|want) (?:the |some )?(?:right |proper |good )?words\b"
    r"|\bwords to (?:say|tell|use)\b|\bhelp me (?:word|phrase|put it)\b",
    re.I)
TELLS_A_TEST = re.compile(
    r"\b(?:tell|saying) (?:if|whether|when|apart|the difference|which|how|what|why|where|who)\b"
    r"|\btell me\b|\btell us\b|\btell (?:you|ya)\b"
    r"|\btell (?:\w+ ){0,4}\bfrom\b|\btell (?:\w+ ){0,3}\boff\b"
    r"|\btell (?:\w+ ){0,2}\bapart\b"
    r"|\bhow (?:do|can|could|would) (?:i|we|you) tell\s*[?.!]*$"
    r"|\bhow (?:do|can|could|should|would) (?:i|we|you) ask (?:for|about)\b", re.I)

NOT_WORDS_ANYWAY = re.compile(
    r"\b(?:in|into) (?:french|spanish|italian|german|welsh|irish|gaelic|japanese|chinese|portuguese|"
    r"dutch|polish|russian|arabic|hindi|greek|turkish|latin)\b"
    r"|\bbreak (?:the ice|a habit|the bank|a record)\b", re.I)
WRITES_A_FORM = re.compile(
    r"\b(?:writ(?:e|ing)|fill(?:ed)? in) (?:(?:\w+) ){0,4}"
    r"(?:form|forms|declaration|customs|invoice|receipt|application|claim\b|return\b|"
    r"questionnaire|box|boxes|field)\b", re.I)
WRITES_IN_A_DOCUMENT = re.compile(
    r"\bwrit(?:e|ing|ten)\b[^.!?]{0,30}\b(?:cv|curriculum vitae|cover(?:ing)? letter|journal|diary"
    r"|essay|report|thesis|dissertation|blog|article|minutes|form|declaration|invoice|receipt"
    r"|application|claim|questionnaire|statement|record)\b", re.I)
WRITES_TO_A_MESSAGE = re.compile(
    r"\b(?:card|letter|note|message|e-?mail|text|reply|comment|speech|toast|eulogy"
    r"|announcement|invitation|post)\b", re.I)
A_COVER_LETTER = re.compile(r"\bcover(?:ing)? letter\b", re.I)
BARE_WRITE = re.compile(
    r"\bwhat (?:should|shall|do|can|could|would) (?:i|we) write\s*[?.!]*$"
    r"|\bwrite (?:about|next|something|anything|more)\b", re.I)
NOT_WORDS_ASK = re.compile(
    TELLS_A_TEST.pattern + "|" + NOT_WORDS_ANYWAY.pattern + "|" + WRITES_A_FORM.pattern + "|"
    + BARE_WRITE.pattern + "|" +
    r"\b(?:tell|talk to|speak to|say to) (?:\w+ ){1,3}about\b", re.I)


NAMED_WORDS = re.compile(
    r"\bwords to (?:say|use|tell)\b|\bwords for (?:telling|saying|asking)\b"
    r"|\b(?:give|send|hand) (?:me )?(?:the )?words\b"
    r"|\bfind (?:me )?(?:the )?(?:right |proper )?words\b"
    r"|\bput (?:it|this) in(?:to)? words\b|\bhelp me (?:word|phrase|put it)\b", re.I)


def asks_for_words(understood):
    if not isinstance(understood, dict):
        return False
    said = str(understood.get("plain") or "").strip().lower() or _said(understood)
    if not said or not WORDS_ASK.search(said):
        return False
    if NAMED_WORDS.search(said):
        return not (TELLS_A_TEST.search(said) or NOT_WORDS_ANYWAY.search(said))
    if not understood.get("subject") and understood.get("followup"):
        return False
    if WRITES_IN_A_DOCUMENT.search(said) and not (
            WRITES_TO_A_MESSAGE.search(said) and not A_COVER_LETTER.search(said)):
        return False
    return not NOT_WORDS_ASK.search(said)


def gives(reply, want, line=None):
    answer = _the_shape_a_reply_gives(reply, want, line)
    if answer is True and is_a_question_back(reply, line):
        return False
    return answer


def _the_shape_a_reply_gives(reply, want, line=None):
    if want not in WANTS or want in SOFT:
        return None
    if isinstance(line, dict):
        line = line.get("text") or line.get("clean") or line.get("plain") or ""
    opening = first_sentence(reply)
    if not opening:
        return None
    repeat = REPEAT_LEAD.match(opening) if want == YESNO else None
    if repeat and opening[repeat.end():].strip():
        opening = opening[repeat.end():].strip()
        repeated = True
    else:
        repeated = False
    if is_a_punt(opening):
        head = reply[:400] or ""
        return None if (DIRECTED.search(head) or A_HOLDER.search(head)) else False
    if want == YESNO and _a_sign_off(opening):
        return None if _A_SOCIAL_OPEN.match(_line_text(line) or "") else False
    check = _CHECKS.get(want)
    if want == TIME and _a_money_rate(opening):
        stripped = _without_a_money_rate(opening)
        if stripped != opening:
            return bool(_a_time(stripped))
    if want == STEPS:
        if _steps_in(reply):
            return True
        if _imperative(opening):
            return True
    elif want == TIME and line and (STAGE_WHEN.search(opening) or SEASON_WHEN.search(opening)) \
            and ASKS_WHEN.search(_line_text(line)):
        return True
    elif want == REASON:
        if _a_reason(opening, line):
            return True
        if line and _names(_opening_two(reply), _line_text(line)) \
                and _a_reason(_opening_two(reply), line):
            return True
    elif want == YESNO:
        if _the_rule_settles_it(opening, line, reply):
            return True
        if _a_yesno(opening, line):
            return True
    elif want == AMOUNT and line and ASKS_AN_AGE.search(_line_text(line)):
        if _an_age_is_given(opening):
            return True
    elif check and check(opening):
        if (want == AMOUNT and line and _a_price_asked(line)
                and _a_time(opening) and not PRICE_GIVEN.search(opening)):
            return False
        return True
    elif want == TIME and _a_time_a_sentence_on(reply):
        return True
    if want == YESNO and line and ASKS_THE_BOT.search(_line_text(line)):
        if I_OFFER.search(opening) and _about_the_thing_the_line_named(
                opening, _line_text(line)):
            return True
    if (want == YESNO and line and not _an_outcome_of_their_own_doing(_line_text(line))
            and _about_the_thing_the_line_named(opening, _line_text(line))):
        if (_a_meaning(opening) or _a_reason(opening) or _a_time(opening)
                or _an_amount_with_a_unit(opening)):
            return True
    if want == YESNO and line and _the_quality_it_was_asked_about(
            opening, _line_text(line)):
        return True
    if want == YESNO and not repeated and _the_job_answers(opening, line):
        return True
    if (want == YESNO and not repeated and line and ASKS_IF_SERIOUS.search(_line_text(line))
            and SEEKS_HELP.search(reply)):
        return True
    if want == YESNO and line and _the_thing_is_named_as_what_it_usually_is(opening, line):
        return True
    if (want == YESNO and line and VERDICT_ABOUT_IT.search(opening)
            and _names_what_the_line_named(opening, _line_text(line))):
        return True
    if want == YESNO and VERDICT_RULE.search(reply):
        return True
    if want == YESNO and _says_no_about_the_asked_thing(opening, line):
        return True
    if want == YESNO and line and _the_side_wins(opening, line):
        return True
    if want == YESNO and _an_echoed_no(opening, line):
        return True
    if (want == YESNO and line
            and _the_figure_against_the_standard(opening, _line_text(line))):
        return True
    if want == YESNO and _a_figure_then_the_verdict(opening, reply):
        return True
    if want == TIME and line and EXTENT.search(opening) and LENGTH_ASKED.search(_line_text(line)):
        return True
    if want == PICK and line and _names_a_side(opening, _line_text(line)):
        return True
    if want == PICK and line and _an_instruction(opening) and _names(opening, line):
        return True
    if want == OPTIONS and line:
        said = _line_text(line)
        if OPTIONS_ASK.search(said) and (INSTRUCTS.match(opening) or JOB.match(opening)):
            return True
    both = _names_both_sides(reply, _line_text(line)) if want == COMPARE and line else None
    if both:
        return True
    if want == COMPARE and both is None:
        return None
    if want == REASON and _head_explains(opening):
        return True
    if want == MEANING and line and _defines_the_thing(opening, _line_text(line)):
        return True
    if (want == MEANING and line and _a_past_definition(opening)
            and _names_what_the_line_named(opening, _line_text(line))):
        return True
    if want == MEANING and line and (ORIGIN_ASK.search(_line_text(line))
                                    or MADE_OF.search(_line_text(line))) and _an_origin(opening):
        return True
    if want == OPTIONS and not _imperative(opening) and not VERDICT_OPEN.match(opening) \
            and not LIST_AFTER_COLON.search(opening) \
            and (_a_pick(opening) or CHOICE.search(opening) or _marked_things(opening) >= 2):
        return True
    if want == OPTIONS and COUNTED_LIST.search(opening) and not A_TIME_COUNT.search(opening) \
            and not _an_instruction(opening) and _a_list_of_things(opening):
        return True
    if want == STEPS and line:
        said = _line_text(line)
        if _options(opening) and _names_what_the_line_named(opening, said):
            return True
    if want in (OPTIONS, STEPS) and line and _do_with_ask(_line_text(line)):
        if _options(opening) or _steps_in(reply) or _an_instruction(opening):
            return True
    if want in (YESNO, PICK) and _the_rule_names_both_sides(reply):
        return True
    if want == OPTIONS and not _an_instruction(opening) \
            and not VERDICT_OPEN.match(opening) and _three_names(_opening_two(reply)):
        return True
    if want == YESNO and _the_same_subject(opening, line):
        return None
    for other, strong in _CLEAR:
        if other == want or (want == STEPS and other in _FIGURES):
            continue
        if other == MEANING and want in (PICK, OPTIONS):
            continue
        if other == MEANING and FIGURE_HEAD.match(opening):
            continue
        if other == AMOUNT and want == YESNO:
            continue
        if other == REASON and want in (STEPS, YESNO):
            continue
        if strong(opening):
            if is_directed(opening):
                return None
            return False
    return None


TELL_ASK = re.compile(
    r"\bhow (?:do|can|could|would|will) (?:i|you|we|someone) (?:tell|know|check|spot|test)\b"
    r"[^.!?]{0,30}\b(?:if|whether|when)\b"
    r"|\bhow to (?:tell|know|check|test)\b[^.!?]{0,20}\b(?:if|whether|when)\b"
    r"|\bhow (?:do|can) (?:i|you|we) know when\b",
    re.I)

IS_IT_DONE = re.compile(
    r"\b(?:is|are|will)\b[^?]{0,40}\b(?:done|cooked|ready|risen|proved|proven|set|thickened|"
    r"browned|defrosted|thawed)\b",
    re.I)

THE_SIGN = re.compile(
    r"\b\d+(?:\.\d+)?\s*(?:°\s*c|c\b|degrees|°\s*f)\b"
    r"[^.!?]{0,80}\b(?:thickest|centre|center|middle|inside|core|internal|juices|clear|firm|"
    r"soft|springy|opaque|no longer|done|cooked|ready|set)\b"
    r"|\b(?:the|that)\b[^.!?]{0,30}\bis the (?:tell|sign|test|clue|giveaway)\b"
    r"|\bthat is how\b[^.!?]{0,40}\b(?:reads|looks|feels)\b"
    r"|\b(?:when|until|once|by the time)\b[^.!?]{0,90}\b(?:browned|golden|clear|firm|soft|"
    r"springy|opaque|thick|risen|doubled|separat\w*|cracked|loose|tender|flaky|hollow)\b"
    r"|\bsounds? (?:hollow|right|done)\b",
    re.I)


def _a_sign_answers(want, line, reply):
    said = str(line or "")
    if want == STEPS:
        if not TELL_ASK.search(said):
            return False
    elif want == YESNO:
        if not IS_IT_DONE.search(said):
            return False
    else:
        return False
    opening = first_sentence(reply)
    if not opening or is_a_punt(opening):
        return False
    return bool(THE_SIGN.search(opening))


_gives_as_read = gives


def gives(reply, wants_, line=None):
    read = _gives_as_read(reply, wants_, line)
    if read is False and _a_sign_answers(wants_, line, reply):
        return True
    return read


def missing(reply, wants_, line=None):
    if isinstance(wants_, str):
        wants_ = [wants_]
    gone = []
    for want in wants_ or ():
        if gives(reply, want, line) is False:
            gone.append(want)
    return gone


def second_sentence(reply):
    text = " ".join(str(reply or "").split())
    parts = re.split(r"(?<=[.!?])\s+", text, maxsplit=2)
    return parts[1].strip() if len(parts) > 1 else ""


BARE_WHAT_AS_IS = re.compile(r"^what(?:'s|s)\b", re.I)
BARE_WHAT_IS_PLAIN = re.compile(r"^what\s+(?:is|are|was)\s+(?P<thing>[^\s,;:]+.*)$", re.I)
BARE_NOT_A_THING_AT_THE_START = re.compile(
    r"^(?:you|u|ur|your|yours|i|im|i'm|my|mine|our|ours|we|us|me|it|this|that|these|those|there|here"
    r"|her|hers|his|their|theirs|its"
    r"|up|on|at|for|with|under|inside|outside|behind|near|next|around|about|in"
    r"|new|nice|good|great|better|best|cheap|cheapest|expensive|wrong|missing|left|leftover"
    r"|easy|easiest|hard|hardest|quick|quickest|simple|simplest|safe|safest|healthy|healthiest"
    r"|popular|common|normal|usual|fast|fastest|slow|slowest|big|biggest|small|smallest"
    r"|right|going|doing|showing|happening|playing|coming|open"
    r"|one|two|three|four|five|six|seven|eight|nine|ten|hundred|thousand|million|half|double)\b"
    r"|^the\s+(?:\w+est|best|worst|most|least|furthest)\b"
    r"|^the\s+(?:new|newest|latest|current|next|other|same|main|real)\b"
    r"|^the\s+(?:time|date|day|capital|price|cost|charge|fee|number|address|name|answer|way"
    r"|point|difference|matter)\b", re.I)
BARE_VALUE_NOUN = re.compile(
    r"^(?:the\s+)?(?:\w+\s+){0,3}(?:rate|rates|price|prices|cost|costs|charge|charges|fee|fees"
    r"|number|numbers|phone|telephone|address|addresses|email|website|opening\s+hours"
    r"|point|points"
    r"|allowance|temperature|password|postcode|pin|score|limit|deadline|budget|balance|total"
    r"|amount|figure|percentage|salary|wage|wages|weight|height|length|width|depth|distance|speed"
    r"|age|population|capacity|mileage)\b", re.I)
BARE_NOT_A_THING_ANYWHERE = re.compile(
    r"\d|\bcalled\b|\bname of\b|\bmeaning of\b|\blike\b|\bwrong\b|\bpower\s+of\b|\btimes\b"
    r"|\bplus\b|\bminus\b|\bdivided\b|\bmultiplied\b|\bpercent\s+of\b|\bsquared\b|\bcubed\b"
    r"|\btodays?\b|\btonights?\b|\btomorrows?\b|\bthis\s+(?:week|weekend|month|year)\b", re.I)
BARE_A_SECOND_QUESTION = re.compile(r"\b(?:why|how|where|when|who|which)\b", re.I)
BARE_A_RECALL = re.compile(r"\b(?:again|earlier|before|yesterday)\s*$|\b(?:i|you)\s+said\b", re.I)
BARE_NOTHING_ASKED = frozenset(("up", "on", "it", "that", "new", "happening", "going on"))


def _a_thing_to_define(phrase, whole):
    if not phrase or not phrase.strip():
        return False
    if phrase.strip().lower() in BARE_NOTHING_ASKED:
        return False
    if BARE_NOT_A_THING_AT_THE_START.match(phrase):
        return False
    if BARE_VALUE_NOUN.match(phrase) and not re.search(r"\b(?:mean|means|work|works)\b", phrase, re.I):
        return False
    if BARE_NOT_A_THING_ANYWHERE.search(whole):
        return False
    if BARE_A_SECOND_QUESTION.search(phrase):
        return False
    if BARE_A_RECALL.search(phrase):
        return False
    if phrase.rstrip().lower().endswith(" for"):
        return False
    return True


def _a_bare_definition(understood):
    if understood.get("about_bot"):
        return False
    whole = BARE_WHAT_AS_IS.sub("what is", LEADING_JOIN.sub("", _whole(understood)))
    plain = BARE_WHAT_IS_PLAIN.match(whole)
    return bool(plain and _a_thing_to_define(plain.group("thing"), whole))


ABBREVIATION_END = re.compile(
    r"\b(?:e\.g|i\.e|approx|incl|etc|vs|cf|fig|dept|est|ref|tel|mr|mrs|ms|dr|prof)\.$", re.I)
SENTENCE_END = re.compile(r"(?<=[.!?])\s+")


TIME_LEAD_IN = frozenset((
    "within", "about", "around", "roughly", "approximately", "every", "by", "up", "least", "most",
    "after", "before", "for", "takes", "take", "lasts", "last", "lasted", "keeps", "keep", "needs",
    "need", "expected", "allow", "allows"))


def _a_time_a_sentence_on(reply):
    text = " ".join(str(reply or "").split())
    opening = first_sentence(text)
    if not opening:
        return False
    rest = text[len(opening):].lstrip(" .!?")
    following = first_sentence(rest) if rest else ""
    if not following:
        return False
    for pattern in (DURATION, CLOCK, STAGE, NAMED_CLOCK):
        for found in pattern.finditer(following):
            lead_in = following[:found.start()].split()[-4:]
            if any(re.sub(r"[^a-z]", "", word.lower()) in TIME_LEAD_IN for word in lead_in):
                return True
    return False


def first_sentence(reply):
    text = " ".join(str(reply or "").split())
    if not text:
        return ""
    for end in SENTENCE_END.finditer(text):
        before = text[:end.start()]
        if ABBREVIATION_END.search(before):
            continue
        return before.strip()
    return text


def _opening_two(reply):
    text = " ".join(str(reply or "").split())
    if not text:
        return ""
    seen = 0
    for end in SENTENCE_END.finditer(text):
        if ABBREVIATION_END.search(text[:end.start()]):
            continue
        seen += 1
        if seen == 2:
            return text[:end.start()].strip()
    return text


NAME_STOP = re.compile(
    r"\b(?:i|you|your|yours|we|our|us|me|my|it|its|they|them|their|he|she|his|her|is|are|was|"
    r"were|be|been|being|do|does|did|have|has|had|can|could|will|would|should|shall|may|might|"
    r"must|if|then|so|but|that|this|these|those|there|here|when|while|because|about|from|with)\b",
    re.I)
STEPS_INSIDE_A_LIST = re.compile(
    r",\s*(?:then|next|after that|afterwards|finally|lastly)\b", re.I)


def _three_names(text):
    plain = " ".join(str(text or "").split())
    if not plain:
        return False
    for clause in re.split(r"(?<=[.!?;:])\s+", plain):
        if clause.count(",") < 2:
            continue
        opened = re.sub(r"^[\W]*(?:then|next|after that|afterwards|finally|lastly)\b", "",
                        clause, flags=re.I)
        if STEPS_INSIDE_A_LIST.search(opened):
            continue
        for run in NAME_STOP.split(opened):
            items = [item.strip() for item in re.split(r"\s*,\s*|\s+(?:and|or|plus)\s+", run)]
            items = [re.sub(r"^(?:and|or|plus)\s+", "", item) for item in items if item]
            items = [item for item in items if item]
            if "(" in run:
                continue
            short = [item for item in items if len(item.split()) <= 4]
            trailing = len(items) - len(short) == 1 and len(items[-1].split()) > 4
            if len(short) >= 3 and (len(short) == len(items) or trailing):
                return True
    return False



_WORD_NUMBER = (r"(?:\d+(?:[.,]\d+)?|one|two|three|four|five|six|seven|eight|nine|ten|eleven|"
                r"twelve|thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|nineteen|twenty|"
                r"thirty|forty|fifty|sixty|seventy|eighty|ninety|hundred|thousand|million|"
                r"a couple|couple|a few|half|a quarter|a third|a fifth|double|dozen)")
_DURATION_QUALIFIER = (r"(?:(?:working|clear|business|banking|bank|calendar|school|full|whole|"
                       r"solid|straight|extra|more|further)\s+)?")
DURATION = re.compile(
    r"(?:" + _WORD_NUMBER + r"|\ba\b|\ban\b)[\s-]*(?:" + _WORD_NUMBER + r"[\s-]*)?"
    + _DURATION_QUALIFIER +
    r"(?:sec|second|min|minute|hr|hour|day|week|fortnight|month|year|night|morning|"
    r"afternoon|evening)s?\b"
    r"|\bovernight\b|\ball day\b|\ball night\b|\bfor a bit\b|\bwithin the hour\b|\bsoon\b|"
    r"\b(?:for|in) (?:days|weeks|months|years)\b|"
    r"\ba (?:full|whole) (?:hour|day|week|month|year)s?\b|"
    r"\b(?:a couple of|a pair of|a number of|a handful of|several|many|numerous)\s+"
    r"(?:sec|second|min|minute|hr|hour|day|week|fortnight|month|year|night|morning|"
    r"afternoon|evening)s?\b|"
    r"\bten minutes\b|\bnext day\b"
    r"|\b(?:a )?couple of (?:secs?|seconds?|mins?|minutes?|hours?|days?|weeks?|months?|years?|"
    r"nights?)\b", re.I)
LENGTH_ASKED = re.compile(
    r"\bhow (?:long|wide|tall|deep|high|far) (?:is|are|was|were)\b"
    r"|\bhow (?:long|wide|tall|deep|high|far) (?:does|do|did) (?:[\w'-]+ ){0,3}"
    r"(?:run|runs|stretch|stretches|measure|measures|reach|reaches|extend|extends|go|goes)\b",
    re.I)
EXTENT = re.compile(
    r"(?:" + _WORD_NUMBER + r"|\ba\b|\ban\b)[\s-]*(?:[a-z]+[\s-]+){0,3}"
    r"(?:km|kilometres?|kilometers?|miles?|metres?|meters?|yards?|feet|foot|inches?|cm|mm|"
    r"centimetres?|centimeters?|millimetres?|millimeters?|pages?|words?|lines?|songs?|tracks?|"
    r"episodes?|chapters?|metres?|m)\b", re.I)

CLOCK_SURE = re.compile(
    r"\b(?:mon|tues|wednes|thurs|fri|satur|sun)day\b"
    r"|\b(?:january|february|april|june|july|august|september|october|november|december"
    r"|jan|feb|mar|apr|jun|jul|aug|sept|sep|oct|nov|dec)\b\.?"
    r"|\b(?-i:May|March)\b\.?"
    r"|\b(?:may|march)\b\.?\s+\d{1,2}\b"
    r"|\b\d{1,2}\s*(?:am|pm)\b|\bo'clock\b|\bmidday\b|\bmidnight\b|\btonight\b|\btomorrow\b"
    r"|\b(?:same|next|this|that) (?:morning|afternoon|evening|night)\b"
    r"|\b(?:at|by|until|till|before|after|from) \d{1,2}[.:]\d{2}(?![.:]?\d)"
    r"|\b(?:in|since|until|till|from|by|during|after|before) "
    r"(?:\d{3,4}s?\b|the \d{3,4}s?\b)"
    r"(?!\s*(?:g|kg|ml|l|p|pence|%|bar|cm|mm|km|m|ft|lb|oz|st|deg|grit|uses?|pages?|words?|"
    r"steps?|calories|kcal|people|guests?|servings?|slices?|eggs?|metres?|meters?|miles?|"
    r"yards?|feet|foot|litres?|liters?|grams?|kilos?|acres?|square|long|wide|tall)\b)"
    r"|\b\d{3,4}\s*(?:ad|bc|b\.c\.)\b"
    r"|\b(?:1[0-9]{3}|20[0-9]{2})\s*(?:-|to|or|and)\s*(?:1[0-9]{3}|20[0-9]{2})\b"
    r"|\bthe \d{1,2}(?:st|nd|rd|th)\b|\b\d{1,2}(?:st|nd|rd|th) of (?:jan|feb|mar|apr|may|jun|"
    r"jul|aug|sep|oct|nov|dec)",
    re.I)
SEASON = re.compile(r"\b(?:spring|summer|autumn|winter)\b", re.I)
CLOCK = re.compile(CLOCK_SURE.pattern + r"|" + SEASON.pattern, re.I)
NOT_A_YEAR = (
    r"(?!\s*(?:cal|kcal|calorie|step|mile|km|kilomet|metre|meter|gram|g\b|kg|ml|litre|liter|"
    r"watt|lumen|gb|mb|megabyte|pound|dollar|euro|per cent|%)\w*)"
    r"(?!\s+[a-z]{2,}s\b)")
DATE = re.compile(
    r"(?:\b(?:in|from|since|until|till|by|of|during|between|after|before|around|about|circa|"
    r"early|late|mid|and|to)\s+(?:the\s+)?|^)(?:1[0-9]{3}|20[0-2][0-9])\b" + NOT_A_YEAR +
    r"|\b(?:in|from|since|during|of|the|by|until|early|late|mid)\s+(?:\d{4}s|\d{1,2}(?:st|nd|"
    r"rd|th) century)\b", re.I)
HOUR_WORD = (r"(?:one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve)"
             r"(?:\s*(?:am|pm|a\.m|p\.m))?")
CLOCK_ANYWHERE = (
    r"(?:\d{1,2}[:.]\d{2}"
    r"|\d{1,2}\s*(?:am|pm|am\.|pm\.|a\.m|p\.m|o'clock)"
    r"|(?:the\s+)?\d{1,2}(?:st|nd|rd|th)\b"
    r"|(?:the\s+)?\d{1,2}\s+of\s+(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)"
    r"|(?:half|quarter|ten|twenty|five|twenty-five)\s+(?:past|to)\s+" + HOUR_WORD + r")"
)
_HOUR_24 = (r"(?:[01]?\d|2[0-4])(?![\d:])(?!\.\d)"
            r"(?!\s*[-\u2013\u2014]\s*\d)"
            r"(?!\s*(?:%|percent|per cent|g|kg|ml|l|p|pence|bar|cm|mm|km|m|ft|lb|oz|st|deg|"
            r"metres?|meters?|miles?|yards?|feet|foot|litres?|liters?|grams?|kilos?|calories|"
            r"kcal|acres?|grit|uses?|square|long|wide|tall)\b)")
NAMED_CLOCK = re.compile(
    r"(?:\b(?:at|by|from|until|till|before|after|around|about|on)\s+" + CLOCK_ANYWHERE +
    r"|\b(?:at|by|from|until|till|before|after)\s+(?:" + HOUR_WORD + r"(?!\s+of\b)|" +
    _HOUR_24 + r")"
    r"|(?:half|quarter|ten|twenty|five|twenty-five)\s+(?:past|to)\s+" + HOUR_WORD + r")", re.I)
FIGURE = re.compile(r"\d|\b(?!one of\b)" + _WORD_NUMBER + r"\b", re.I)
MONEY = re.compile(
    r"[£$€]|\b(?:pence|pounds?|quid|dollars?|euros?|cents?|free)\b"
    r"|^(?:nothing|nil|nowt)\b|\bnothing (?:at all|extra|much|to pay|else|on top)\b"
    r"|\bcosts? nothing\b", re.I)


def _a_figure(opening):
    return bool(FIGURE.search(opening))


BARE_RANGE = re.compile(
    r"^[^\w]{0,3}(?:about |around |roughly )?(?:\d{1,3}|" + _WORD_NUMBER + r")"
    r"\s*(?:-|to|or|\u2013)\s*(?:\d{1,3}|" + _WORD_NUMBER + r")\b", re.I)

STAGE = re.compile(
    r"\b(?:for|in|over|through|during) the first (?:few |couple of |several )?"
    r"(?:days|weeks|months|year|bit)\b|\bthe first (?:few |couple of )?(?:days|weeks|months)\b"
    r"|\b(?:first|1st) birthday\b|\buntil (?:they|he|she) (?:are|is) \w+\b", re.I)
NEVER = re.compile(
    r"\b(?:indefinitely|(?:does not|doesn't|do not|don't|will not|won't|never) "
    r"(?:go(?:es)? off|expire|spoil|perish)|(?:last|lasts|keep|keeps|stay|stays|good) "
    r"(?:good )?(?:for ever|forever|indefinitely))\b", re.I)

RATE_PHRASE = re.compile(
    r"^(?:once|twice|(?:three|four|five|six|\d+)\s+times|"
    r"every (?:\w+ )?(?:day|week|month|year|morning|evening|night)|"
    r"daily|weekly|monthly|yearly|nightly)"
    r"(?:\s+(?:a|an|per|each|every)\s+(?:day|week|month|year|morning|evening|night))?", re.I)


STAGE_WHEN = re.compile(
    r"(?:(?:\bwhen|\bas soon as)\s+(?:the|it|its|they|they're|there|a|your|their)\b"
    r"|\bonce\s+(?:the|it|its|they|they're|there|your|their)\b)"
    r"[^.?!]{0,70}?\b(?:has|have|had|is|are|was|were|shows?|showing|sets?|set|starts?|started|"
    r"reaches?|reached|begins?|begun|appears?|emerges?|sprouts?|sprouted|flowered|flowers|"
    r"warms?|warmed|workable|cooled|cools|dried|dries|firm|ready|grown|thickened|risen)\b",
    re.I)

EDGED_PART_OF_DAY = re.compile(
    r"\b(?:mid|early|late)[- ]?(?:morning|afternoon|evening|night)\b"
    r"|\b(?:first|last) thing\b(?!\s+(?:a|an|the|it|i|you|we|they|he|she|that|this|of|about)\b)"
    r"|\bfirst light\b|\bdaytime\b"
    r"|\b(?:at|by|before|after|until|till|around|about) (?:dawn|dusk|nightfall|sunset|sunrise|"
    r"daybreak)\b|\bend of the (?:day|afternoon|evening)\b", re.I)

SEASON_WHEN = re.compile(
    r"\b(?:in|during|through|throughout|into|over)\s+(?:the\s+)?"
    r"(?:growing|dormant|bare|planting|flowering|nesting|mating|wet|dry|rainy)\s+season\b"
    r"|\b(?:the\s+)?growing months?\b"
    r"|\b(?:in|during)\s+(?:a\s+|the\s+)?(?:dry|wet|cold|warm)\s+spells?\b",
    re.I)

NAMED_TIME = re.compile(
    r"\b(?:before|after|until|till|by|at|on|from|in|over|during)\s+(?:the\s+)?"
    r"(?:first|second|third|next|last|that|their|his|her)?\s*"
    r"(?:birthday|christmas|easter|new year|weekend|weekday|morning|afternoon|evening|night|"
    r"breakfast|lunch|teatime|tea|dinner|supper|bedtime|school|school night|work|the day|"
    r"arrival|takeoff|checkout|check-in)\b", re.I)
DAY_NAME = re.compile(
    r"\b(?:christmas|easter|new year'?s?|bank holiday|birthday|half term|term time|"
    r"the weekend)\b", re.I)

RATE_OF_A_COUNT = re.compile(
    r"\b\d[\d,.]*\s*(?:cal|kcal|calorie|step|rep|unit|mile|km|kilomet|metre|meter)s?\b"
    r"(?:\s+\w+){0,2}\s+"
    r"(?:a|an|per|each|every)\s+(?:day|week|month|year|morning|evening|night)\b", re.I)


MINUTES_AS_A_LENGTH = re.compile(
    r"\b(?:within|for)\s+(?:a few|a couple of|several|a|one|two|three|four|five|ten)\b"
    r"[\s-]*(?:min|minute)s?\b"
    r"|\ba few (?:min|minute)s\b|\bwithin (?:a few |a couple of )?(?:min|minute)s\b", re.I)


NO_FIXED_TIME = re.compile(
    r"^(?:no|there'?s no|there is no) (?:fixed|set|exact|hard and fast) (?:time|length|deadline)\b",
    re.I)


def _a_time(opening):
    if NAMED_CLOCK.search(opening):
        return True
    if EDGED_PART_OF_DAY.search(opening):
        return True
    said = RATE_PHRASE.sub("", opening, count=1) if RATE_PHRASE.match(opening) else opening
    said = RATE_OF_A_COUNT.sub(" ", said) if RATE_OF_A_COUNT.search(said) else said
    if NO_FIXED_TIME.match(said):
        return True
    if (DURATION.search(said) or CLOCK.search(said) or BARE_RANGE.match(said)
            or STAGE.search(said) or NEVER.search(said) or NO_FIXED_TIME.match(said)
            or MINUTES_AS_A_LENGTH.search(said)):
        return True
    if INSTRUCTS.match(opening):
        return False
    first_clause = re.split(r"[,;:]", said, maxsplit=1)[0]
    return bool(NAMED_TIME.search(first_clause) or DAY_NAME.search(first_clause)
                or DATE.search(first_clause))


def _a_clear_time(opening):
    return bool(DURATION.search(opening) or CLOCK_SURE.search(opening)
                or BARE_RANGE.match(opening))



RATE = re.compile(
    r"\b(?:every (?:day|week|month|year|morning|evening|night|"
    r"other (?:day|morning|evening|night))|every few (?:days|weeks)|"
    r"most (?:days|mornings|evenings|nights|weekends)|once|twice|"
    r"three times|daily|weekly|monthly|yearly|nightly|\d+ times)\b", re.I)


ASKS_AN_AGE = re.compile(r"\bwhat age\b|\bhow old\b", re.I)

_AN_AGE_YEARS = re.compile(
    r"(?:\d+|" + _WORD_NUMBER + r")\s*(?:-\s*)?years?\s*(?:old|of age)\b"
    r"|\b(?:age|aged)\s+(?:of\s+)?(?:\d+|" + _WORD_NUMBER + r")\s*years?\b"
    r"|^(?:\d+|" + _WORD_NUMBER + r")\s*years?\b", re.I)
_AN_AGE_MONTHS = re.compile(
    r"(?:\d+|" + _WORD_NUMBER + r")\s*(?:-\s*)?(?:months?|weeks?)\s*old\b"
    r"|\b(?:about|around|at|by|from|until|till|under|over|aged?)\s+(?:\d+|" + _WORD_NUMBER +
    r")\s*(?:months?|weeks?)\b"
    r"|^(?:\d+|" + _WORD_NUMBER + r")\s*(?:months?|weeks?)\b", re.I)
_AN_AGE_BIRTHDAY = re.compile(r"\b(?:\d+(?:st|nd|rd|th)|[a-z]+(?:st|nd|rd|th))\s+birthday\b",
                              re.I)
_AN_AGE_NAMED = re.compile(r"\b(?:age|aged)\s+(?:\d+|" + _WORD_NUMBER + r")\b", re.I)
_AN_AGE_BARE = re.compile(
    r"(?<![£$€\d.,])\b\d{1,2}\b(?![.,]?\d)"
    r"(?!\s*(?:%|minutes?\b|mins?\b|hours?\b|hrs?\b|days?\b|pounds?\b|pence\b|quid\b|"
    r"times?\b|per\b|each\b|of them\b))", re.I)
_AN_AGE_SPELLED_OPENS = re.compile(
    r"^(?:" + _WORD_NUMBER + r")\b(?=\s*(?:,|to\b|is\b|or\b|and\b|-|\u2013))", re.I)


def _an_age_is_given(opening):
    return bool(_AN_AGE_YEARS.search(opening) or _AN_AGE_MONTHS.search(opening)
                or _AN_AGE_BIRTHDAY.search(opening) or _AN_AGE_NAMED.search(opening)
                or _AN_AGE_BARE.search(opening) or _AN_AGE_SPELLED_OPENS.match(opening))


def _an_amount(opening):
    return bool(FIGURE.search(opening) or MONEY.search(opening) or RATE.search(opening))


PRICE_ASKED = re.compile(
    r"\b(?:cost|costs|priced?|prices?|pay|pays|paid|charged|charges? for|afford|fees?|quote|"
    r"salary|rent)\b|[\u00a3$\u20ac]|\b(?:pounds|quid|euros?|dollars?|pence|tenner)\b", re.I)
PRICE_GIVEN = re.compile(
    r"[\u00a3$\u20ac]|\b\d+p\b|\b(?:pounds|quid|pence|euros?|dollars?|cents?|free|costs?|"
    r"prices?|charges?|fees?|paid|pay|spend|budget|afford|quote|refund|salary|rent|tenner)\b",
    re.I)


def _a_price_asked(line):
    return bool(PRICE_ASKED.search(_line_text(line)))

MEASURED = re.compile(
    r"(?:\d|\b" + _WORD_NUMBER + r")\s*-?\s*(?:minutes?|mins?|hours?|hrs?|days?|weeks?|"
    r"months?|years?|seconds?|secs?|mugs?|cups?|tablespoons?|tbsps?|teaspoons?|tsps?|grams?|"
    r"kilograms?|kg|litres?|liters?|ml|pints?|quarts?|per cent|percent|degrees?|miles?|km|"
    r"metres?|meters?|feet|foot|inches?|times?|pence|pounds?|quid|each|people|servings?)\b",
    re.I)


A_BARE_NUMBER = re.compile(r"^(?:\d+|" + _WORD_NUMBER + r")\.?$", re.I)


def _a_figure_that_counts(opening):
    return bool(_an_amount_to_read(opening) or A_BARE_NUMBER.match(opening.strip()))


def _an_amount_to_read(opening):
    if re.search(r"\d", opening) or MONEY.search(opening) or RATE.search(opening):
        return True
    return bool(MEASURED.search(opening))


_FIGURE_HEAD = 5


def _figure_at_the_head(opening, pattern):
    match = pattern.search(opening)
    return match is not None and len(opening[:match.start()].split()) < _FIGURE_HEAD


def _a_clear_time_at_the_head(opening):
    return (_figure_at_the_head(opening, DURATION)
            or _figure_at_the_head(opening, CLOCK_SURE)
            or bool(BARE_RANGE.match(opening)))


_MEASURE_AFTER = re.compile(
    r"\s*-?\s*(?:minutes?|mins?|hours?|hrs?|days?|weeks?|months?|years?|seconds?|secs?|mugs?|"
    r"cups?|tablespoons?|tbsps?|teaspoons?|tsps?|grams?|kilograms?|kg|litres?|liters?|ml|pints?|"
    r"quarts?|per cent|percent|centigrade|degrees?|miles?|km|metres?|meters?|feet|foot|inches?|"
    r"times?|pence|pounds?|quid|each|people|servings?)\b", re.I)


def _an_amount_at_the_head(opening):
    if _figure_at_the_head(opening, MONEY) or _figure_at_the_head(opening, RATE):
        return True
    match = FIGURE.search(opening)
    if match is None or len(opening[:match.start()].split()) >= _FIGURE_HEAD:
        return False
    if match.group(0)[0].isdigit():
        return True
    return bool(_MEASURE_AFTER.match(opening, match.end()))



PLACE_WORD = re.compile(
    r"\b(?:shop|store|supermarket|chemist|pharmac|post office|bank|building society|council|"
    r"\bgp\b|doctor'?s|surgery|dentist|library|garage|station|market|website|web site|site|app|"
    r"online|branch|office|centre|center|clinic|hospital|recycling|tip\b|dump|high street|"
    r"department|service desk|desk|reception|kiosk|counter|aisle|dealer|showroom|garden centre|"
    r"petrol station|airport|bus stop|platform|address|tesco|asda|sainsbury|aldi|lidl|morrisons|"
    r"co-op|boots|argos|screwfix|ikea|amazon|ebay|gov\.uk|passport office|dvla|jobcentre|"
    r"citizens advice|charity shop|car boot|facebook marketplace|freecycle|wherever|"
    r"downstairs|upstairs|outside|indoors|in the garden|in the kitchen|in the loft|in the shed|"
    r"drawer|cupboard|cabinet|wardrobe|shelf|shelves|rack|hook|peg|locker|safe|"
    r"pocket|handbag|backpack|rucksack|suitcase|glove ?box|boot of the car|"
    r"hallway|corridor|landing|garage|shed|loft|attic|basement|cellar|balcony|porch|"
    r"kitchen|bedroom|bathroom|toilet|utility room|airing cupboard|under the sink|"
    r"in the cupboard|in the drawer|on the shelf|in the fridge|in the freezer|in the bin|"
    r"on the wall|on the door|in the hall|by the door|at the back of|at the front of|"
    r"on top of|behind the|under the|next to the|beside the|inside the)"
    r"(?:s|es)?\b",
    re.I)
PLACE_AS_EVIDENCE = re.compile(
    r"\b(?:shop|store|supermarket|chemist|pharmac|post office|bank|building society|council|"
    r"\bgp\b|doctor'?s|surgery|dentist|library|garage|station|market|website|web site|site|app|"
    r"online|branch|office|centre|center|clinic|hospital|recycling|tip\b|dump|high street|"
    r"department|service desk|desk|reception|kiosk|counter|aisle|dealer|showroom|garden centre|"
    r"petrol station|airport|bus stop|platform|address|tesco|asda|sainsbury|aldi|lidl|morrisons|"
    r"co-op|boots|argos|screwfix|ikea|amazon|ebay|gov\.uk|passport office|dvla|jobcentre|"
    r"citizens advice|charity shop|car boot|facebook marketplace|freecycle|wherever|"
    r"downstairs|upstairs|outside|indoors|in the garden|in the kitchen|in the loft|in the shed)"
    r"(?:s|es)?\b",
    re.I)


WHERE_MONEY_GOES = re.compile(
    r"\bwhere (?:does|do|did) (?:it all |all )?(?:my|our|the|his|her|your) "
    r"(?:money|pay|wages|salary|income|budget|earnings|time)\b[^?]{0,20}\b(?:go|goes|went)\b"
    r"|\bwhere (?:my|our|the|his|her|your) (?:money|pay|wages|salary|income|budget|time) "
    r"(?:goes|go|went)\b", re.I)

WHERE_RELATIVE = re.compile(
    r"\bwhere\s+(?:i|we|you|he|she|they|it|my|your|our|his|her|their)\b[^?.]{0,20}?"
    r"\b(?:am|is|are|was|were|live|lives|stay|stays|sit|sits|work|works|go|goes)\b", re.I)
ASKS_TO_BE_TOLD_WHERE = re.compile(
    r"\b(?:tell (?:me|us)|know|knows|say|says|shows?|explain|remind|remember|any idea|wonder|"
    r"find|check)\b[^?]{0,25}\bwhere\b", re.I)
PLACE_NAME = re.compile(r"\b(?:in|at|to|from|near|of|round|around|towards)\s+"
                        r"(?:(?:the\s+)?[A-Z]{2,4}(?![A-Za-z])|(?:the\s+|a\s+)?[A-Z][a-z]{2,})")

PLACE_KIND = re.compile(
    r"\b(?:shops|stores|supermarkets|pharmacies|station|stations|markets|cafes|cafés|"
    r"booths|branches|clinics|charities|tip|depots|counters|showrooms|kiosks|"
    r"market hall|market halls|food court|food courts|bakery|bakeries|street food|"
    r"food van|food vans|multi storey|multistorey|multi-storey)\b", re.I)
PLACE_AT_HOME = re.compile(
    r"\b(?:room|bedroom|bathroom|kitchen|utility|hall|hallway|landing|corridor|garage|loft|"
    r"shed|porch|doorstep|doormat|doorway|door|stairs|staircase|step|floor|corner|"
    r"wardrobe|cupboard|drawer|shelf|shelves|bookcase|bookshelf|mantelpiece|"
    r"windowsill|window sill|bedside|nightstand|bed|sofa|settee|couch|cushion|chair|"
    r"table|desk|hook|peg|pocket|bag|handbag|rucksack|backpack|glovebox|glove box|"
    r"footwell|boot|bin|washing machine|tumble dryer|airing cupboard|"
    r"street|side street|back street|road|car park|park and ride|lay-by|lay by|"
    r"cul-de-sac|estate|alley|alleyway|walkway|underpass|carpark)s?\b"
    r"|\b(?:on|in|under|behind|beside|next to|top of|bottom of|end of)\s+"
    r"(?:the\s+|your\s+|my\s+)?"
    r"(?:sofa|bed|table|desk|stairs|fridge|freezer|counter|shelf|cupboard|wardrobe|"
    r"radiator|window|door|mat|hook|hall|car|boot|pushchair|pram|buggy)s?\b"
    r"|\b(?:behind|under|underneath|beside|next to|on top of|in front of|at the bottom of|"
    r"at the back of|at the front of|at the side of)\s+(?:the\s+|your\s+|my\s+|a\s+)?[a-z]{3,}"
    r"|\b(?:in the open|up high|off the floor|in the middle of|away from the (?:wall|floor|heat))",
    re.I)
PLACE_NAME_ANY = re.compile(r"(?:(?<=[:;,]\s)|(?<=\bor\s)|(?<=\band\s))[A-Z][a-z]{2,}")
CALENDAR_WORD = re.compile(
    r"\b(?:in|on|of|by|until|till|from|during|after|before|early|late|mid|and|to)\s+"
    r"(?:the\s+)?(?:january|february|april|june|july|august|september|october|november|december"
    r"|jan|feb|mar|apr|jun|jul|aug|sept|sep|oct|nov|dec)\b\.?"
    r"|\b(?:in|on|of|by|until|till|from|during|after|before|early|late|mid)\s+(?-i:May|March)\b\.?"
    r"|\b(?:mon|tues|wednes|thurs|fri|satur|sun)day\b\.?"
    r"|\b\d{1,2}\s*(?:st|nd|rd|th)\b",
    re.I)


PERSON_WORD = re.compile(
    r"\b(?:vet|veterinar|doctor|gp|nurse|pharmacist|chemist|dentist|plumber|electrician|"
    r"gas safe|engineer|mechanic|solicitor|lawyer|adviser|advisor|accountant|broker|"
    r"landlord|letting agent|employer|hr|union|citizens advice|council|police|"
    r"someone|somebody|a professional|specialist|consultant|technician|builder|roofer|"
    r"physio|optician|midwife|health visitor|social services|ombudsman|registrar|"
    r"witness|referee|teacher|tutor|your bank|the bank|neighbour|neighbor)(?:s|es)?\b", re.I)
PERSON_NAME = re.compile(r"(?<=[a-z,;(]\s)[A-Z][a-z]{2,}")
PERSON_RELATION = re.compile(
    r"\b(?:mum|mom|mam|dad|mother|father|son|daughter|sister|brother|wife|husband|partner|"
    r"friend|mate|boyfriend|girlfriend|fianc\w*|neighbou?r|boss|colleague|"
    r"manager|supervisor|team leader|line manager|head of (?:year|department|team)|"
    r"child|kid|baby|"
    r"gran|grandma|grandad|granny|nan|aunt|uncle|cousin|step(?:son|daughter|mum|dad)|"
    r"in-laws?|twins?)\b", re.I)
_ROLE_ENDS = r"[a-z]{3,}(?:er|or|ist|ian|ant|smith|minder|wright)"
_ROLE_OFFICES = r"(?:council|company|authority|agency|department|office|service|board|team)"
_NOT_A_ROLE = frozenset((
    "power", "water", "answer", "number", "other", "order", "letter", "paper", "dinner", "offer",
    "cover", "corner", "member", "record", "filter", "computer", "calendar", "character",
))
_PARTY = re.compile(
    r"\b(?:a|an|the|your|our|their|his|her|my)\s+(?:[a-z-]+\s+){0,2}?" + _ROLE_ENDS
    + r"(?=\s*(?:,|'s|:))"
    r"|\b(?:a|an|the|your|our|their)\s+(?:[a-z-]+\s+){0,2}?" + _ROLE_OFFICES + r"\b", re.I)


def _a_party(opening):
    for found in _PARTY.finditer(opening):
        if found.group(0).split()[-1].lower() not in _NOT_A_ROLE:
            return True
    return False


PERSON_NAMED = re.compile(
    r"^[A-Z][a-z]{2,}\s+(?:is|was|'s)\s+(?:your|our|his|her|their)\s+[a-z]+", re.I)
PERSON_FULL_NAME = re.compile(r"^[A-Z][a-z]{2,}\s+(?:[A-Z][a-z]{2,}|[IVXLC]{2,})\b")

MEANS = re.compile(
    r"\b(?:means|meaning|stands for|is short for|refers to|is when|is what|"
    r"is (?:a|an|the)\s+\w+|are (?:a|an|the)\s+\w+|is called|called|is basically|"
    r"is just|is simply|is the (?:name|word|yearly|total|amount|cost|price|process))\b"
    r"|\b(?:is|are|means)\s+(?:\w+\s+)?for\s+[\"'\u201c\u2018]", re.I)


MEANS_ARTICLE = re.compile(r"^(?:is|are) (?:a|an|the)\s+\w+", re.I)


MEANS_INFINITIVE = re.compile(r"^to\s+\w+\s+(?:is|means)\s+to\s+\w+", re.I)


SETTLED_ON = re.compile(
    r"\byou (?:settled on|decided on|went for|opted for|chose|picked|plumped for|said|mentioned|"
    r"told me)\b", re.I)


SPOT_ON_THE_THING = re.compile(
    r"\b(?:in|on|under|underneath|behind|inside|beneath|beside|alongside|next to|on top of|"
    r"just under|just behind|halfway up|partway up)\s+"
    r"(?:the|a|an|its|your|each|either|one)\s+([\w'-]+)", re.I)
SPOT_PART = frozenset("""
plate plates sticker stickers label labels badge case casing housing shell body flap lid cover
panel door doors seal seals drawer box compartment slot port socket plug valve hose pipe tube
drum filter cartridge cap knob handle handles shelf rack tray trays wand bag packaging manual
leaflet screen dial switch button hinge underside underside base bottom top side sides back
front rear corner edge middle centre center bracket clamp nut bolt screw seam cord cable wire
spout nozzle brush blade bar rim trim guard grille vent clip strap tie
""".split())


SPOT_OF_THE_THING = re.compile(
    r"\b(?:on|at|in|under|near)\s+the\s+(?:back|front|top|bottom|side|underside|base|rear|"
    r"middle|centre|center|corner)\s+of\s+(?:the|a|an|its|your)\s+[\w'-]+", re.I)


def _the_spot_a_thing_has(found):
    if not found:
        return None
    return found.group(1).lower().strip("'-")


def _names_a_spot(opening):
    if SPOT_OF_THE_THING.search(opening or ""):
        return True
    for found in SPOT_ON_THE_THING.finditer(opening or ""):
        if _the_spot_a_thing_has(found) in SPOT_PART:
            return True
    return False


def _a_place(opening):
    opening = CALENDAR_WORD.sub(" ", opening)
    return bool(PLACE_WORD.search(opening) or PLACE_NAME.search(opening)
                or len(PLACE_NAME_ANY.findall(opening)) >= 2 or SETTLED_ON.search(opening)
                or _names_a_spot(opening)
                or PLACE_KIND.search(opening) or PLACE_AT_HOME.search(opening))


def _a_person(opening):
    opening = CALENDAR_WORD.sub(" ", opening)
    if PERSON_RELATION.search(opening):
        return True
    if _a_party(opening) or PERSON_NAMED.search(opening) or PERSON_FULL_NAME.match(opening):
        return True
    return bool(PERSON_WORD.search(opening) or PERSON_NAME.search(opening))


A_JUDGEMENT = re.compile(
    r"^\s*(?:it|that|this|they|these|those|there|he|she|you|we|i)\s+(?:is|are|was|were)\s+"
    r"(?:a|an|the)\s+(?:real|good|nice|fine|great|bad|big|small|awful|lovely|honest|fair|"
    r"decent|brilliant|rubbish|terrible|wonderful|amazing|perfect|silly|daft|sad|happy|"
    r"serious|proper|big|tough|hard|easy|common|rare)\s+\w+", re.I)


DEFINES = re.compile(
    r"^(?!\s*(?:it|that|this|they|these|those|there|he|she|i|we|you|what|which|here|so|and|but|"
    r"do|did|does|don'?t|doesn'?t|didn'?t)\b)"
    r"(?:[\w'\u2019-]+(?:\s+[\w'\u2019-]+){0,4}\s+(?:is|are|mean|means)\b"
    r"|[\w'\u2019-]+(?:\s+[\w'\u2019-]+){0,4}\s+(?:has|have)\b(?!\s+to\b))", re.I)


MEANS_BY_DOING = re.compile(
    r"^(?:\w+ ){0,3}(?:give|gives|provide|provides|let|lets|allow|allows|help|helps|names)\s+"
    r"(?:you|a|an|some|free|people|anyone)\b", re.I)


MECHANISM = re.compile(
    r"\bis how\b|\bworks? by\b|\bworks? like\b|\bworks? because\b|"
    r"^(?:(?:the|a|an)\s+[\w'\u2019-]+(?:\s+[\w'\u2019-]+){0,3}\s+|it\s+)"
    r"(?:has|have)(?!\s+to\b)|(?:uses|consists of|contains|comes from|breaks|pulls|pushes|turns|"
    r"carries|draws|"
    r"sucks|lifts|heats|cools|reacts|sends|absorbs|filters|"
    r"moves|moved|stores|dumps|spins|tumbles|bends|drives|releases|fills|pumps|blows|burns|"
    r"melts|freezes|bounces|blocks|traps|spreads|grows|charges|recharges|squeezes|stretches|"
    r"swings|shakes|rotates|grinds|crushes|mixes|separates|holds|held|takes in|gives out)\b",
    re.I)


SOURCE_MAKES = re.compile(
    r"^(?:\w[\w'\u2019-]*[ ,]+){1,6}(?:make|makes|made|lay|lays|laid|grow|grows|produce|produces|"
    r"give|gives)\s+(?:it|them)\b", re.I)
SOURCE_COLON = re.compile(r"^(?!\s*(?:it|that|this|there|they|you|we|i)\b)"
                          r"[\w'\u2019,()/-]+(?:\s+[\w'\u2019,()/-]+){1,7}:\s*\w", re.I)
SOURCE_MADE = re.compile(
    r"^[\w'\u2019,()-]+(?:\s+[\w'\u2019,()-]+){0,12},\s*(?:boiled|crushed|heated|picked|shorn|"
    r"wilted|dried|melted|grown|laid|dug|pressed|cooked|washed|cut|made|then|and then)\b", re.I)


SOURCE_DOES = re.compile(
    r"^[\w'\u2019-]+(?:\s+[\w'\u2019-]+){0,3}\s+(?:soaks|runs|flows|comes|grows|forms|makes|"
    r"gives|produces|holds|carries|falls|melts|boils|ferments|rots|breaks|builds|lays)\b", re.I)


SOURCE_LIST = re.compile(
    r"^(?!\s*(?:it|that|this|there|they|you|we|i)\b)[\w'\u2019-]+(?:,\s*[\w'\u2019-]+){2,}"
    r"(?:\s+and\s+[\w'\u2019-]+)?\b", re.I)


def _an_origin(opening):
    return bool(SOURCE_MAKES.match(opening) or SOURCE_COLON.match(opening)
                or SOURCE_MADE.match(opening) or SOURCE_DOES.match(opening)
                or SOURCE_LIST.match(opening))


_OPINION_OF_THE_THING = re.compile(
    r"^(?:that|this|it|they|these|those|he|she|you|we)(?:'s|\u2019s| is| are| was| were)\s+"
    r"(?:a|an)\s+(?:real|proper|genuine|right|good|great|big|small|huge|little|nice|fair|tough|"
    r"hard|easy|lovely|brilliant|terrible|awful|total|complete|classic|common|usual|rare|"
    r"dangerous|safe|useful|useless|important|serious|key|major|minor|main|whole|full|"
    r"big|decent|solid|mucky|filthy|messy)\b", re.I)

PAST_DEFINES = re.compile(r"\b(?:was|were)\s+(?:a|an|the)\s+[a-z][\w'\u2019-]*", re.I)
NOT_A_SUBJECT = re.compile(
    r"(?:^|[^\w'\u2019-])(?:it|that|this|there|these|those|he|she|they|we|you|i|who|which|"
    r"what|one|none|everyone|someone|anyone|nobody|nothing|something|anything|everything|"
    r"my|your|his|her|its|our|their|mine|yours|theirs)$", re.I)


def _a_past_definition(opening):
    found = PAST_DEFINES.search(opening)
    if not found:
        return False
    subject = re.split(r"[.;:!?,()\u2014]", opening[:found.start()])[-1].strip()
    if NOT_A_SUBJECT.search(subject):
        return False
    return not re.match(r"(?:my|your|his|her|its|our|their|mine|yours|theirs)\b", subject, re.I)


def _a_meaning(opening):
    if _OPINION_OF_THE_THING.match(str(opening or "").strip()):
        return False
    if MECHANISM.search(opening):
        return True
    if MEANS_BY_DOING.match(opening) or MEANS_INFINITIVE.match(opening):
        return True
    if DEFINES.match(opening):
        return True
    hit = MEANS.search(opening)
    if hit is None:
        return False
    if MEANS_ARTICLE.match(hit.group(0)) and A_JUDGEMENT.match(opening):
        return False
    return True



VERDICT_OPEN = re.compile(
    r"^(?:yes|yeah|yep|yup|no|nope|nah|not|never|don'?t|do not|doesn'?t|avoid|skip|sure|"
    r"definitely|absolutely|probably|usually|generally|normally|often|mostly|sometimes|"
    r"better|best|fine|safe|okay|ok|"
    r"it'?s|it is|that'?s|that is|they'?re|there'?s no|you'?re|you (?:can|could|should|don'?t|"
    r"do not|does not|did not|won'?t|can'?t|shouldn'?t|need|want|have to|must)|"
    r"bin|throw|chuck|toss|dump|discard|refrain|"
    r"none|nothing|straight|warm|cold|plain|just|"
    r"private|confidential|anonymous|between us)\b", re.I)
FIRST_PERSON_VERDICT = re.compile(
    r"^i (?:would|wouldn'?t|do|don'?t|will|won'?t)\b(?!\s+(?:only|just|rather|say that))"
    r"|^i'?d (?:say|skip|wait|hold off|bother|not bother|avoid|keep|leave|go for|get|change|"
    r"stick with|try)\b", re.I)


ECHO_VERDICT = re.compile(
    r"^(?:(?:still|that'?s|that is|you'?re|you are|absolutely|dead) right|correct|exactly|"
    r"spot on)\b", re.I)
VERDICT_BAND = re.compile(
    r"(?:inside|within|outside)\s+(?:the\s+|well\s+)?"
    r"(?:normal|usual|average|expected|recommended|accepted|healthy)\b"
    r"(?!\s*(?:use|uses|conditions?|circumstances?|operation|working|service|wear|load))"
    r"|(?:inside|within|outside|above|below|over|under)\s+the\s+"
    r"(?:range|band|limits?)\b"
    r"|(?:above|below|over|under)\s+the\s+(?:normal|usual|recommended|expected)\b"
    r"|within reach\b", re.I)
VERDICT_INSIDE = re.compile(
    r"\b(?:yes|no need|not really|not worth|worth it|isn'?t worth|a bad idea|a good idea|"
    r"\bworth (?:repairing|fixing|doing|buying|getting|having|paying|spending|keeping|servicing|"
    r"replacing|renewing|hiring|installing|the money|the effort|a go)\b"
    r"|\bmeans (?:no|yes|not)\b|"
    r"\b(?:keeps?|lasts?) (?:for|until|about|roughly|easily|well|a couple|a few|a good|\d)\b|"
    r"harmless|safe|fine|okay|avoid|go ahead|of course|by law|make sure|only|"
    r"is (?:normal|common|usual|typical|expected|ordinary|fine|safe|okay|harmless|allowed|legal)|"
    r"is (?:good|fine|ok|okay|great|safe|bad) (?:with|at|for|in)\b|"
    r"is (?:usually|normally|generally|probably|often) (?:just |fine|normal|harmless|safe|okay)|"
    r"\bis (?:almost |nearly )?(?:always |usually )?the (?:cheaper|cheapest|better|best|quicker|"
    r"quickest|easier|easiest|safer|safest|simpler|simplest) (?:way|option|choice|bet|buy|route|"
    r"one)\b|\b(?:works? out|comes? out|turns? out) (?:cheaper|cheapest|better|best|quicker|"
    r"easier|safer)\b|"
    r"suits|works well|works fine|no harm|nothing wrong|nothing to worry|"

    r"you'?ll be fine|it depends|not (?:a problem|necessary|needed|allowed)|"
    r"(?:do not|does not|don'?t|doesn'?t) need\b|"
    r"(?:is|are|does) not\b|\b(?:isn'?t|aren'?t|doesn'?t)\b|"
    r"harmful|unhealthy|healthy|bad for|good for|not good for|risky|dangerous|unsafe|not safe|"
    r"a lot|too much|too late|not enough|plenty|worth (?:a go|doing)|the one to (?:pick|avoid))\b"
    r"|" + VERDICT_BAND.pattern + r"",
    re.I)
A_HARM_IS_WHAT_IT_IS = re.compile(
    r"\b(?:is|are|was|were) (?:a|an) (?:real|serious|genuine|proper|major|big|known|health|"
    r"significant|grave) (?:risk|hazard|danger|problem|no-no)\b", re.I)
QUALITY_IS = re.compile(
    r"\bis (?:really |very |always |usually )?(?:great|good|fine|perfect|brilliant|lovely|ideal|"
    r"free|cheap|easy|worth it|worthwhile)\b", re.I)
IT_HELPS = re.compile(r"\b(?:it|this) (?:really |usually |often )?(?:helps?|works?)\b", re.I)
_WORKING = re.compile(r"\b(?:work|works|working|worked|help|helps|helping|use|using|used|worth|bother|good)\b", re.I)
_PRONOUN_SUBJECT = frozenset(("it", "this", "that", "they", "these", "those", "he", "she"))


def _the_quality_is_about_the_thing(clause, line):
    found = QUALITY_IS.search(clause)
    if not found:
        return False
    subject = clause[:found.start()].strip()
    if not subject:
        return True
    words = _words(subject)
    if words and words[-1] in _PRONOUN_SUBJECT:
        return True
    said = _line_text(line)
    if not said:
        return True
    named = {w for w in words if len(w) >= 4 and w not in _EMPTY}
    return not named or any(w in said for w in named)


def _the_tail_says_what_it_is_about(clause, line):
    found = VERDICT_INSIDE.search(clause)
    if not found:
        return False
    subject = clause[:found.start()].strip()
    if not subject:
        return False
    words = _words(subject)
    if words and words[-1] in _PRONOUN_SUBJECT:
        return True
    said = _line_text(line)
    if not said:
        return True
    named = {w for w in words if len(w) >= 3 and w not in _EMPTY}
    return bool(named) and any(_the_same_word(w, said) for w in named)


ASKS_ABOUT_A_QUALITY = re.compile(r"\b(?:is|are|was|were|isn'?t|aren'?t)\b", re.I)
_QUALITIES = ("worth it", "worthwhile", "normal", "typical", "ordinary", "common", "okay", "ok",
              "safe", "alright", "legal", "allowed", "healthy", "necessary", "essential", "fine")
_QUALITY_SAID = {q: re.compile(r"\b%s\b" % re.escape(q), re.I) for q in _QUALITIES}
_THE_VERDICT_IS_EARLY = 12


def _the_quality_it_was_asked_about(opening, said):
    named = {w for w in _words(said)
             if len(w) >= 4 and w not in _EMPTY and w not in NOT_A_THING
             and w not in {x for q in _QUALITIES for x in q.split()}}
    if not named and said and ASKS_ABOUT_A_QUALITY.search(said):
        asked = " ".join(_words(opening)[:_THE_VERDICT_IS_EARLY])
        return any(_QUALITY_SAID[q].search(asked) for q in _QUALITIES)
    if not said or not ASKS_ABOUT_A_QUALITY.search(said):
        return False
    head = " ".join(_words(opening)[:_THE_VERDICT_IS_EARLY])
    for quality in _QUALITIES:
        found = _QUALITY_SAID[quality].search(head)
        if not (found and _QUALITY_SAID[quality].search(said)):
            continue
        if quality in _QUALITY_OF_A_THING and not _the_quality_is_said_of_the_thing(
                head, found.start(), said):
            continue
        return True
    return False


_QUALITY_OF_A_THING = frozenset(q for q in _QUALITIES if q not in ("worth it", "worthwhile"))
_COPULA = frozenset(("is", "are", "was", "were", "isnt", "arent", "wasnt", "werent", "be", "feels",
                     "feel", "looks", "look", "seems", "seem", "sounds", "sound", "gets", "stays"))


def _the_quality_is_said_of_the_thing(head, at, said):
    words = head[:at].split()
    if not words or words[-1] not in _COPULA:
        return True
    subject = [w for w in words[:-1] if w.isalpha()]
    if not subject:
        return True
    if subject[-1] in _PRONOUN_SUBJECT:
        return bool(said) and _about_the_thing_the_line_named(head, said)
    if not said:
        return True
    return any(w in said for w in subject[-2:])


VERDICT_INSIDE_QUALITY = re.compile(
    r"\bis (?P<q>normal|common|usual|typical|expected|fine|safe|okay|harmless|allowed|legal)\b",
    re.I)


def _the_verdict_is_inside(clause, line):
    found = VERDICT_INSIDE_QUALITY.search(clause)
    if found is None:
        return bool(VERDICT_INSIDE.search(clause))
    at = clause.index(found.group("q"), found.start())
    if _the_quality_is_said_of_the_thing(clause, at, line or ""):
        return True
    rest = clause[:found.start()] + " " + clause[found.end():]
    return bool(VERDICT_INSIDE.search(rest))


def _the_quality_answers(clause, line):
    if _the_quality_is_about_the_thing(clause, line):
        return True
    return bool(IT_HELPS.search(clause) and _WORKING.search(_line_text(line)))


PUNT = re.compile(
    r"^(?:i'?m not sure|i am not sure|i don'?t know|i do not know|i can'?t|i cannot|can'?t call|"
    r"that'?s beyond|that is beyond|that'?s all|that is all|there is no more|"
    r"beyond what i know|not mine to|not a call|not one i can call|a quick search|searching for|"
    r"i'?d rather not|"
    r"you haven't told me|that'?s a good question|good question|no idea|not something i|"
    r"no (?:figure|number|price|answer|idea|verdict|view|opinion|guess) from me|"
    r"say (?:what (?:you(?:'?re| are)? (?:asking|after|on about|worried about|unsure)|"
    r"you mean|you want to know|has you (?:asking|wondering))|which|that again|more|me more|"
    r"a bit more)\b|"
    r"tell me (?:what|which|more) (?:you|has|is|part)\b|"
    r"no (?:first[- ]hand )?(?:knowledge|idea|clue) (?:of|on|about|here|from me)\b|"
    r"^nothing (?:in|about) (?:that|this|it|what you (?:said|told me|described))\b"
    r"[^.!?]{0,60}?\b(?:say|says|said|tell|tells|told|show|shows|showed|suggest|suggests|"
    r"indicate|indicates|go on)\b|"
    r"^nothing here (?:to go on|that (?:says|tells))\b|"
    r"^hard to (?:put a (?:scale|number) on|say how|judge|tell how|gauge)\b|"
    r"i'?m not sure (?:what|how|which|whether|where) to|i'?m not sure without)", re.I)
HANDOFF = re.compile(
    r"^(?:(?:that'?s|that is|it'?s|it is) (?:your|a) call(?![a-z])|"
    r"not (?:a )?call (?:i|we) (?:can|could|would)|"
    r"(?:that'?s|that is) (?:one|a question|something) for (?:your|a|the)\b|"
    r"(?:that'?s|that is) (?:everything|all) i (?:have|know)\b|"
    r"(?:that'?s|that is|it'?s|it is) not (?:mine|for me) to (?:answer|say|tell|call|judge)\b|"
    r"i would only repeat myself|nothing more i can (?:say|add|tell)\b|"
    r"(?:that'?s|that is) not for me to|"
    r"whether (?:it|that|they|this|[0-9]+|[a-z]+) (?:is|are|was|will be|would be) "
    r"(?:worth|a lot|too much|too long|too far|any good|safe|normal|fine)\b|"
    r"hold (?:it|that|this|the price|[0-9]+)\b[^.]{0,30}\bagainst (?:one|another|a|other)\b|"
    r"only you can (?:weigh|judge|say|decide|call)\b|"
    r"(?:that'?s|that is|it'?s|it is) yours to (?:weigh|say|decide|call|judge)\b|"
    r"that part(?:'?s| is) (?:yours|up to you)\b|"
    r"(?:i'?ll|i will) leave (?:that|this|it) to (?:your|a|the|somebody|someone)\b)", re.I)


REFERS_BACK = re.compile(
    r"^\s*(?:i wouldn'?t call|i would not call|nothing in that|hard to|no way to|not something i "
    r"can)\b[^.!?]{0,80}?\b(?:answer|step|thing|doing) above\b", re.I)


def is_a_punt(opening):
    return bool(PUNT.match(opening) or HANDOFF.match(opening)
                or REFERS_BACK.match(opening))

SOURCE = (r"(?:page|web ?site|site|app|account|portal|label|packet|packaging|manual|instructions|"
          r"leaflet|paperwork|statement|bill|letter|receipt|booking|policy|schedule|timetable|"
          r"council|gp|doctor|dentist|vet|surgery|pharmacy|provider|supplier|landlord|employer|"
          r"insurer|bank|met office|forecast|meter)")
DIRECTED = re.compile(
    r"\b(?:your|their|its|the)\b[^.!?]{0,40}\b" + SOURCE + r"\b[^.!?]{0,60}\b(?:will|would|"
    r"should|can|does)\s+(?:say|tell|show|give|have|confirm|list|explain)\b"
    r"|\b" + SOURCE + r"\b[^.!?]{0,40}\b(?:has|have|carries|lists|shows|gives)\s+"
    r"(?:it|them|you|the (?:day|date|time|figure|price|number|amount|answer|rate))\b", re.I)


A_HOLDER = re.compile(
    r"\b(?:your|their|its|the|a|an)\b[^.!?]{0,30}\b(?:app|e-?mail|bill|statement|account|page|"
    r"web ?site|site|letter|receipt|label|packet|packaging|manual|instructions|paperwork|booking|"
    r"confirmation|tracking|policy|meter|portal|reference number)\b", re.I)


def is_directed(opening):
    return bool(DIRECTED.search(opening))


_A_QUOTE = "\"\u201c\u201d"
_NOT_A_WORD = frozenset(("you", "your", "yours", "yourself", "yourselves"))
_WORD = re.compile(r"[a-z0-9']+")


def _the_first_sentence(reply):
    quoted = False
    for index, char in enumerate(reply):
        if char in _A_QUOTE:
            quoted = not quoted
        elif not quoted and char in ".!?":
            after = reply[index + 1:index + 2]
            if not after or after.isspace():
                return reply[:index + 1]
    return reply


_NO_WAY_TO_KNOW = re.compile(
    r"(?:you'?ve not said|you haven'?t said|you have not said|only you know|"
    r"tell me and i'?ll remember|i only get what you type|no way for me to know)", re.I)


def _the_echo_question(opening, line):
    said = _WORD.findall((line or "").lower())
    if not said:
        return False
    mine = [word for word in _WORD.findall(opening.lower())
            if len(word) > 3 and word not in _NOT_A_WORD]
    return bool(mine) and all(word in said for word in mine)


def is_a_question_back(reply, line=None):
    text = (reply or "").strip()
    if not text:
        return False
    opening = _the_first_sentence(text)
    if not opening.rstrip().endswith("?"):
        return False
    if not _the_echo_question(opening, line):
        return True
    rest = text.strip()[len(opening):].strip()
    if not rest:
        return True
    return bool(is_a_punt(first_sentence(rest)) or _NO_WAY_TO_KNOW.search(rest))
HYPOTHETICAL = re.compile(r"\bif (?:i|we|you)\b", re.I)
OUTCOME_ASK = re.compile(r"^(?:and )?(?:will|would|does|do|did)\b|^if\b", re.I)


def _an_outcome_of_their_own_doing(line):
    said = str(line or "")
    return bool(HYPOTHETICAL.search(said) and OUTCOME_ASK.search(said))


NEGATES = re.compile(r"\b(?:not|n't|never|no longer|nothing|none|nowhere)\b", re.I)
SAYS_NO = re.compile(
    r"(?:^|[,;:\u2014-]\s*)(?P<subject>[^,;:.!?]{1,40}?)\s+(?:is|are|was|were|does|do|did|"
    r"will|would|can|could|has|have|needs?|takes?)\s+(?:not|never|n't)\b", re.I)
NO_JOB = re.compile(r"\b(?:don'?t|do not|never|avoid|skip|stop|no need to)\s+([a-z]{3,})", re.I)
NOT_A_THING = frozenset((
    "not", "never", "nothing", "none", "does", "doesn", "dont", "don", "did", "didn", "isn",
    "aren", "wasn", "weren", "can", "can’t", "cant", "cannot", "won", "would", "should",
    "could", "have", "has", "had", "need", "needs", "want", "wants", "why", "how", "what",
    "when", "where", "which", "that", "this", "these", "those", "they", "them", "there",
    "their", "your", "you", "and", "but", "for", "with", "into", "from", "about", "just",
    "like", "much", "more", "less", "than", "then", "only", "really", "still", "even"))


def _names_the_lines_thing(opening, said):
    reply = set(_words(opening))
    for word in set(_words(said)):
        if len(word) < 3 or word in _EMPTY or word in NOT_A_THING:
            continue
        if word in reply or (len(word) > 4 and word[:-1] in reply):
            return True
    return False


def _says_no_about_the_asked_thing(opening, line):
    said = _line_text(line)
    if not said:
        return False
    if opening.rstrip('"\u201d ').endswith("?"):
        return False
    for match in SAYS_NO.finditer(opening):
        if _names_the_lines_thing(match.group("subject"), said):
            return True
    asked = set(_words(said))
    for match in NO_JOB.finditer(opening):
        verb = match.group(1)
        if verb in asked or (len(verb) > 4 and verb[:-1] in asked):
            return True
    return False


TRAILING_VERDICT = re.compile(
    r"[,\-\u2013\u2014]\s*(?:so|then|but|which means|that means|meaning)\s+"
    r"(?:no|yes|nope|not really|definitely not|probably not|of course|not worth it)\b", re.I)

SEEKS_HELP = re.compile(
    r"\b(?:see|ring|call|contact|visit|speak to|talk to|get seen by|book (?:an appointment )?with)\s+"
    r"(?:a|an|the|your|nhs|out of hours)?\s*"
    r"(?:gp|doctor|dentist|vet|111|999|urgent care|walk-in cent(?:re|er)|midwife|health visitor|"
    r"pharmacist|optician|nurse|surgery|hospital)s?\b", re.I)
ASKS_IF_SERIOUS = re.compile(
    r"\b(?:dangerous|serious|a problem|a worry|worrying|worry about|something to worry|"
    r"should i worry|normal|abnormal|a sign of|a concern)\b", re.I)


TEST_IS_THE_VERDICT = re.compile(
    r"comes? out clean|is done when|is ready when|is cooked when|"
    r"when it'?s? (?:firm|golden|clean|set|done)|"
    r"if it (?:looks|feels|comes|smells) (?:done|cooked|firm|golden|clean|set|right)", re.I)


PERMISSION_RULE = re.compile(
    r"\b(?:can|cannot|can'?t|could|couldn'?t|may|must|should|need(?:s)? to) be [a-z]+ed\b"
    r"|\bcosts? nothing\b", re.I)

THEIR_OWN = re.compile(
    r"\b(?:is|are)\s+(?:yours|your own|for you to|one for you|a (?:diy|weekend|home|simple) job)\b"
    r"|\b(?:you|yourself) (?:can|could) (?:do|change|replace|fit|swap|fix|service|repair)\b"
    r"|\byourself\b", re.I)
A_TRADE = re.compile(
    r"\b(?:engineer|electrician|plumber|gas safe|registered|qualified|competent|specialist|"
    r"professional|trade)\w*\b", re.I)
MUST_BE_A_TRADE = re.compile(
    r"\b(?:has|have|needs?|must|should)\s+to\s+(?:be\s+)?(?:done\s+)?by\b"
    r"|\bnot a (?:diy|home) job\b|\b(?:by|get) an? (?:gas safe|registered|qualified)\b", re.I)


def _the_job_is_split(opening):
    if MUST_BE_A_TRADE.search(opening):
        return True
    return bool(THEIR_OWN.search(opening) and A_TRADE.search(opening))


RULE_CONDITION = re.compile(
    r"\b(?:if|when|while|once|until|unless|over about|under about|more than about|"
    r"less than about|half (?:of )?the price)\b", re.I)
RULE_KEEP_IT = re.compile(r"\b(?:fix|repair|keep|mend|service)\s+it\b", re.I)
RULE_DROP_IT = re.compile(r"\b(?:bin|replace|scrap|chuck|throw)\s+it\b", re.I)
RULE_GO_NEW = re.compile(
    r"\b(?:put (?:the |that )?money towards|go for|buy|get|fit|have|bring in)\b[^.;:]{0,24}"
    r"\b(?:a |the )?new\b|\bbuy new\b", re.I)


VERDICT_ECHO = re.compile(
    r"^(?:it|that|this|they|these|those|he|she) "
    r"(?:does|do|did|will|would|can|could|should|doesn'?t|don'?t|didn'?t|won'?t|can'?t|"
    r"shouldn'?t)\b"
    r"|^(?:you|we) (?:would|will|do|did|can|could|should) not\b", re.I)
VERDICT_RULE = re.compile(
    r"\byou(?:'?re| are) (?:owed|entitled|covered|allowed|within your rights)\b"
    r"|\byou (?:qualify|are owed|are entitled|can claim|claim|can apply|apply for|are covered|"
    r"do not need|don't need|get it|can get one|can have one)\b"
    r"|\bgets? (?:\d[\d,.]*|a|the|half|a third|one) (?:per cent|percent|%)\b"
    r"|\bis the wrong (?:choice|one|thing|call)\b"
    r"|\bthere is no (?:table service|need|charge|fee|cost)\b"
    r"|\bnothing to (?:tip|pay|declare|owe|worry about)\b", re.I)
VERDICT_AFTER_A_CASE = re.compile(
    r"^(?:for|in|on|with|at|if|when|unless|after|before)\b[^,.;:!?]{1,40},\s*"
    r"(?:yes|yeah|yep|yup|no|nope|nah|not|never|definitely|absolutely|probably|usually|generally|"
    r"normally|mostly|it'?s|it is|that'?s|that is|you'?re|you (?:can|could|should|don'?t))\b", re.I)
THE_WINNER_NAMED = re.compile(
    r"\bis the (?:cheaper|better|worse|cheapest|best|worst|safer|safest|healthier|healthiest|"
    r"stronger|weaker|easier|harder) (?:one|option|choice|bet|buy|of the two)\b", re.I)


VERDICT_ABOUT_IT = re.compile(
    r"\b(?:is|are|was|were) (?:the|one of the|a) (?:better|best|safest|kindest|cheapest|healthiest|"
    r"easiest|simplest|nicest|worst|strongest|tastiest|kinder|safer|cheaper|healthier|easier)\b"
    r"|\bis a good (?:way|idea|choice|bet|pick|option|buy|start|investment)\b"
    r"|\bis the one (?:to|for|that|you)\b"
    r"|\bworth (?:reading|knowing|having|checking|watching|visiting|seeing|a look|a read)\b"
    r"|\b(?:if|unless|when)\b[^.;]{0,90},\s*(?:then\s+)?(?:go|go ahead|go for it|yes|no|fine|okay|"
    r"safe|skip|skip it|leave it|let it go|do it|take it|avoid it|worth it|try it|"
    r"it'?s (?:fine|okay|safe|worth it)|that'?s (?:fine|okay|safe)|you'?re (?:fine|okay|safe))\b",
    re.I)
_NAMING_WORD = re.compile(r"[a-z]{4,}")
NAMING_STOP = frozenset("""
that this with have your them when what just like then than also make need from into over been
were will would could should about there their some more most much very only even still well
good best fine time times day days year years work works thing things home back down know want
take keep give goes going said says here where while which whose these those being does doing
done made many each both after before again always never often sometimes usually really quite
rather around without within because since until during other another same different little
small large""".split())


def _the_same_word(word, text):
    if not word:
        return False
    return bool(re.search(r"\b" + re.escape(word) + r"(?:s|es)?\b", text))


def _names_what_the_line_named(opening, said):
    words = set(_NAMING_WORD.findall(said.lower())) - NAMING_STOP
    if not words:
        return False
    first_clause = re.split(r"[,;:]", opening, maxsplit=1)[0]
    return any(_the_same_word(w, first_clause.lower()) for w in words)


def _the_rule_names_both_sides(reply):
    if not reply or not RULE_CONDITION.search(reply):
        return False
    drop = RULE_DROP_IT.search(reply) or RULE_GO_NEW.search(reply)
    return bool(RULE_KEEP_IT.search(reply) and drop)


REPEAT_LEAD = re.compile(
    r"^(?:same as before|same answer(?:,? and it covers this)?|same as i said|as before|as i said|"
    r"like i said|same thing|same again)\s*[:,]?\s+", re.I)


SIGN_OFF_LEAD = re.compile(
    r"^(?:(?:that'?s|it'?s|this is)\s+)?(?:nice|great|lovely|wonderful|perfect|brilliant|"
    r"excellent|fantastic|amazing|awesome|glad|sorry|fair enough|no rush|no worries|sounds? good|"
    r"got it|understood|alright then|good luck|hope|thanks|thank you|of course|cheers)\b", re.I)


_A_SOCIAL_OPEN = re.compile(
    r"^(?:have|enjoy|hope|good luck|take care|cheers|thanks|thank you|hi|hello|hey|morning|"
    r"goodnight|bye)\b", re.I)


def _a_sign_off(opening):
    match = SIGN_OFF_LEAD.match(opening)
    if not match:
        return False
    rest = opening[match.end():].strip(" \t.,;:!?-\u2014")
    rest = re.sub(r"^(?:but|and|so|though|however|yet|although|still)\b[\s,]*", "", rest, flags=re.I)
    if not rest:
        return True
    return not (_a_yesno(rest) or VERDICT_INSIDE.search(rest) or VERDICT_ECHO.match(rest)
                or VERDICT_RULE.search(rest) or TEST_IS_THE_VERDICT.search(rest)
                or TRAILING_VERDICT.search(rest) or PERMISSION_RULE.search(rest))


VERDICT_ON_A_SCALE = re.compile(
    r"\b(?:inside|within|outside|past|beyond|above|below|at the top of|at the bottom of)\s+"
    r"(?:the\s+|its\s+)?(?:normal|usual|typical|expected|average|recommended|healthy)"
    r"(?:\s+(?:range|band|limits?|age|window|spread|side))?\b"
    r"|\bon the (?:late|early|young|old|small|large|big|high|low|heavy|light|slow|fast|short|long|"
    r"tricky|tight|generous|easy) side\b"
    r"|\bborderline\b|\bexactly on time\b|\bnothing (?:unusual|abnormal|out of the ordinary)\b"
    r"|\bstill (?:inside|within|in)\b.{0,20}\b(?:normal|range)\b", re.I)


def _a_yesno(opening, line=None):
    if is_a_punt(opening):
        return False
    if FIRST_PERSON_VERDICT.match(opening) or VERDICT_OPEN.match(opening) \
            or ECHO_VERDICT.match(opening) or VERDICT_AFTER_A_CASE.match(opening):
        return True
    if PERMISSION_RULE.search(opening):
        return True
    if _the_job_is_split(opening):
        return True
    if VERDICT_ECHO.match(opening) or VERDICT_RULE.search(opening):
        return True
    first_clause = re.split(r"[,;:]", opening, maxsplit=1)[0]
    if _the_verdict_is_inside(first_clause, line) or TEST_IS_THE_VERDICT.search(opening) \
            or TRAILING_VERDICT.search(opening) or THE_WINNER_NAMED.search(first_clause) \
            or A_HARM_IS_WHAT_IT_IS.search(first_clause) \
            or VERDICT_ON_A_SCALE.search(first_clause):
        return True
    if _the_quality_answers(first_clause, line):
        return True
    if _a_rule_of_its_use(opening, line):
        return True
    tail = ""
    if ":" in opening:
        tail = opening.split(":", 1)[1]
    else:
        found = re.search(r",?\s+so\b", opening)
        if found:
            tail = opening[found.end():]
    tail = re.split(r"[,;]", tail, maxsplit=1)[0] if tail else ""
    return bool(tail and (_the_tail_says_what_it_is_about(tail, line)
                          or _the_quality_answers(tail, line)))


A_LIMIT_ON_ITS_USE = re.compile(
    r"\b(?:keeps?|lasts?|stays?|stored?|freezes?)\b[^.\d]{0,20}\b"
    r"(?:\d[\d.,]*\s*(?:to|-|or)\s*)?\d[\d.,]*\s*"
    r"(?:days?|hours?|weeks?|months?|years?|fortnights?)\b"
    r"|\b(?:keep|keeps|kept|take|takes|move|put|leave|shut|block)\b[^.]{0,45}?\b(?:out of|"
    r"away from|well away)\b"
    r"|\b\w+\b[^.]{0,30}\bunless\b"
    r"|\b(?:up to|no more than|at most|not more than|until about|until they|under about)\b"
    r"[^.]{0,12}?\b\d[\d.,]*\s*(?:kg|kgs|g|grams?|cm|mm|ml|litres?|inches?|years?|months?|"
    r"weeks?|days?|hours?|minutes?|mins?|seconds?|decibels|db|degrees?)\b"
    r"|\b\d[\d.,]*\s*(?:to|-|or)\s*\d[\d.,]*\s*(?:minutes?|mins?|hours?|seconds?)\b"
    r"[^.]{0,12}?\bat a time\b"
    r"|\b(?:within|inside|reheat(?:ed)?\b[^.]{0,15}?until)\b[^.]{0,20}?"
    r"(?:\d[\d.,]*\s*(?:hours?|minutes?|days?)|steaming|piping hot|boiling)\b"
    r"|\b(?:it|they|that|this)\b[^.]{0,12}?\b(?:is|are)\b[^.]{0,12}?"
    r"\b(?:fine|safe|ok|okay|alright|harmless)\b", re.I)


A_BOUND_THAT_IS_THE_ANSWER = re.compile(
    r"\b(?:keeps?|lasts?|stored?)\b[^.\d]{0,20}\b(?:\d[\d.,]*\s*(?:to|-|or)\s*)?\d[\d.,]*\s*"
    r"(?:days?|hours?|weeks?|months?|years?|fortnights?)\b"
    r"|\b(?:use|eat|drink|keep|finish|consume)\b[^.]{0,25}?\bwithin\b[^.]{0,15}?"
    r"\d[\d.,]*\s*(?:days?|hours?|weeks?)\b"
    r"|\b(?:no more than|up to|at most)\b[^.]{0,12}?\b\d[\d.,]*\s*(?:kg|kgs|g|grams?|ml|"
    r"units?|decibels|db|degrees?|hours?|minutes?)\b"
    r"|\b\d[\d.,]*\s*(?:to|-|or)\s*\d[\d.,]*\s*(?:minutes?|mins?|hours?|seconds?)\b"
    r"[^.]{0,12}?\bat a time\b"
    r"|\b\w+\b[^.]{0,25}\bunless\b", re.I)


def _a_rule_of_its_use(opening, line):
    if A_BOUND_THAT_IS_THE_ANSWER.search(opening):
        return True
    found = A_LIMIT_ON_ITS_USE.search(opening)
    if not found:
        return False
    said = _line_text(line)
    if not said:
        return True
    if _names(found.group(0), said) or _names(opening, said):
        return True
    return not [w for w in set(_words(said)) if _long_enough_a_name(w, 4) and w not in _EMPTY]


NEGATED_AUX = re.compile(
    r"\b(?:is|are|was|were|do|does|did|have|has|had|can|could|will|would|should|must|need|"
    r"needs|kills?|harm|hurt|matter|work|works)\s*(?:not|n'?t)\b|\b(?:isn'?t|aren'?t|wasn'?t|"
    r"weren'?t|don'?t|doesn'?t|didn'?t|haven'?t|hasn'?t|can'?t|cannot|won'?t|wouldn'?t|"
    r"shouldn'?t)\b", re.I)

USUALLY_IS = re.compile(
    r"\b(?:is|are|was|were)\s+(?:usually|often|nearly always|almost always|mostly|generally|"
    r"typically|most likely|in most cases)\b", re.I)


def _the_thing_is_named_as_what_it_usually_is(opening, line):
    said = _line_text(line)
    if not said:
        return False
    found = USUALLY_IS.search(opening)
    if not found:
        return False
    rest = opening[found.end():]
    for word in set(re.findall(r"[a-z][a-z']*", said)):
        if len(word) < 4 or word in _EMPTY or word in NOT_A_THING:
            continue
        if re.search(r"\b%s" % re.escape(word), rest):
            return True
    return False


def _an_echoed_no(opening, line):
    said = _line_text(line)
    if not said or not NEGATED_AUX.search(opening):
        return False
    words = set(re.findall(r"[a-z][a-z']*", said))
    named = {w for w in words if len(w) >= 4 and w not in _EMPTY}
    return any(w in opening for w in named)


def _the_job_answers(opening, line):
    if not line or _an_outcome_of_their_own_doing(line):
        return False
    if JOB.match(opening):
        return True
    if _imperative(opening):
        return True
    return _the_job_named(opening, _line_text(line))


PREFERS = re.compile(
    r"^(?:replace|repair|rebuild|service|swap|install|keep|buy|rent|hire|book|order|get|go for|"
    r"go with|take|choose|pick|stick with|read|watch|visit|try|start with|hold off|wait)\b"
    r"|\b(?:better|best|rather|instead|go for|go with|opt for|choose|pick|stick with|"
    r"you (?:mentioned|said|named|had)|you'?re on|"
    r"\b(?:buy|get|fit|install|replace|repair|swap|go for|go with) (?:the|a|an|one|it)\b|"
    r"i'?(?:d| would) (?:go|do|make|cook|have|take|get|pick|choose|suggest|recommend|buy|wear|"
    r"watch|read|order|book|serve|use|say|stay|leave|keep|skip|cancel|wait|ring|call)|"
    r"worth (?:the extra|it)|"
    r"either .{0,40}\bor\b|"
    r"\bworth (?:repairing|replacing|fixing|doing|keeping|buying|getting|upgrading|waiting|"
    r"swapping|having|sticking with)\b|"
    r"both are|both work|depends on|for (?:a|the) .{0,30}\band\b.{0,30}\bfor\b)\b", re.I)


BALD = re.compile(r"^(?:the|a|an|this|that|[A-Z][a-z]+)\b")
BALD_VERB = re.compile(
    r"\b(?:is|are|was|were|has|have|holds?|works?|comes?|goes?|keeps?|takes?|lasts?|costs?|"
    r"means|does|do|will|can)\b", re.I)
REASON_OPENS = re.compile(
    r"^(?:because|cos|'cause|that'?s why|that is why|since|so that|which is why)\b", re.I)
A_VERB_THEN_THE_THING = re.compile(
    r"^(?!(?:the|a|an|this|that|these|those|your|my|our|their|his|her|its|some|any|each|every|"
    r"one|two|both)\b)[a-z]+\s+(?:it|them|the|a|an|your|this|that)\b", re.I)


def _undecorated(head):
    return head.strip().strip("*_\"\u201c\u201d'").strip()


NAMED_HEAD = re.compile(r"^(.{2,70}?):\s", re.S)
ASKS_HEAD = re.compile(r"^(?:how|what|why|when|where|which|who|steps?|first|firstly|then|next|to|"
                       r"tldr|quick tips?)\b", re.I)
LABEL_HEAD = re.compile(r"^(?:quick|best|cheapest|easiest|fastest|faster|fast|simplest|simple|"
                        r"cheap|easy|options?|ideas?|while you [a-z]+|bonus|top|also|first|firstly|"
                        r"then|next|tip|tips|note|tl;?dr|answer|short answer|in short|verdict|"
                        r"my pick|worth it)\s*$", re.I)
SET_LABEL = re.compile(
    r"^(?:quick|best|cheapest|easiest|fastest|faster|fast|simplest|simple|cheap|easy|options?|"
    r"ideas?|while you [a-z]+|bonus|top|also|first|firstly|then|next|tip|tips|note|worth it)\s*$",
    re.I)
ECHO_HEAD = re.compile(r"^(?:same as (?:before|last time)|as (?:before|above)|like before|"
                       r"as i said|same|same again|still|unchanged|no change)\s*$", re.I)
BACK_HEAD = re.compile(
    r"^(?:you'?ve got it|you got it|i (?:like|liked|love|prefer) (?:it|them|that|those)|"
    r"that'?s (?:it|right|the one)|this one|as i said|like before|"
    r"same as (?:before|last time))\b", re.I)
STATES_HEAD = re.compile(r"\b(?:is|are|was|were|means|sounds?|seems?)\b|"
                         r"\b(?:it|that|here|there|what)'s\b", re.I)
FRAME_HEAD = re.compile(r"^(?:here'?s|think of it|imagine|to be fair|the (?:truth|thing|point|"
                        r"trick|catch|problem|issue|trouble|trouble is)|honest\w*|"
                        r"the way i see it|what you want)\b", re.I)


PICKS_BY_COMPARISON = re.compile(
    r"\b(?:is|are|was|were) (?:the )?(?:longer|shorter|bigger|smaller|taller|wider|deeper|"
    r"heavier|lighter|faster|slower|quicker|cheaper|dearer|pricier|warmer|colder|hotter|newer|"
    r"older|nicer|easier|harder|safer|stronger|thicker|thinner)\b"
    r"|\b(?:is|are) (?:exactly |about |nearly |roughly )?twice as\b"
    r"|\bis the (?:one|answer|pick|choice|setting|winner|default)\b"
    r"(?!\s+(?:that|which|who)\b)"
    r"|\bare the thing\b|\bthe thing to (?:get|buy|have|do|go for)\b", re.I)
PICK_BY_CASE = re.compile(
    r"\bif\b[^:]{0,90}\b(?:for (?:anything|everything) else|otherwise|else)\b"
    r"|\bif not\b", re.I)
QUOTED_NAME = re.compile(r"'[^'\n]{2,40}'|\u2018[^\u2019\n]{2,40}\u2019")


WOULD = re.compile(
    r"\bi'd (?:do|make|cook|have|wear|say|keep|buy|book|order|get|take|go|try|use|put)\b", re.I)

LABEL = re.compile(r"^([^:]{1,90}):\s+(\S.+)$")
NOT_A_LABEL = re.compile(
    r"\b(?:is|are|was|were|means?|reason|cause|because|depends?|you'?ve got|same as|as before|"
    r"good question|it'?s|that'?s|there'?s|here'?s|"
    r"^i (?:like|liked|love|prefer) (?:it|them|that|those)|^both|^same)\b", re.I)


def _listed_after(label_lead):
    if re.search(r"\bor\b", label_lead, re.I) or ";" in label_lead:
        return True
    return len(re.findall(r",\s+\S", label_lead)) >= 2


def _marked_things(opening):
    return len(re.findall(r"\*[^*\n]{2,60}\*", opening)) + len(
        re.findall(r"\u201c[^\u201d\n]{2,60}\u201d|\B\"[^\"\n]{2,60}\"", opening))


NAMES_IN_EMPHASIS = re.compile(
    r"^\*{1,2}[^*\n]{2,70}\*{1,2}(?!\*)(?!\s*(?:is|are|was|were|means|refers|describes|comes)\b)"
    r"(?!\s*:)")


def _a_pick(opening):
    if PREFERS.search(opening) or PICKS_BY_COMPARISON.search(opening) or WOULD.search(opening):
        return True
    lead = LABEL.match(opening)
    if lead and not NOT_A_LABEL.search(lead.group(1)) \
            and not SET_LABEL.match(lead.group(1).strip()) and _listed_after(lead.group(2)):
        return True
    if re.search(r"\b(?:is|are|was|were) (?:almost |nearly |usually |often |always |generally |probably |still |"
                 r"quite |about )?(?:the )?(?:(?!(?:request|interest|honest|guest|test|rest|nest|"
                 r"west|east|forest|harvest|protest|suggest|arrest|contest|digest|invest|earnest|"
                 r"chest|crest|tempest|midwest|northwest|southwest|northeast|southeast)\b)"
                 r"[a-z]{3,}est|most [a-z]+|least [a-z]+)\b|"
                 r"\bis the (?:cheapest|dearest|worst|easiest|quickest|safest|hardest|"
                 r"cheaper|better)\b|\bwins?\b(?: on| over| for| by)\b|"
                 r"\b(?:has|have|holds|gets) (?:the )?(?:most|highest|lowest|fewest|best)\b",
                 opening, re.I):
        return True
    if NAMES_IN_EMPHASIS.match(opening):
        return True
    if len(QUOTED_NAME.findall(opening)) >= 2 and PICK_BY_CASE.search(opening):
        return True
    if is_a_punt(opening) or VERDICT_OPEN.match(opening):
        return False
    head = NAMED_HEAD.match(opening)
    if head:
        named = _undecorated(head.group(1).strip())
        if (ECHO_HEAD.match(named) or BACK_HEAD.match(named) or STATES_HEAD.search(named)
                or FRAME_HEAD.match(named)
                or (bool(re.search(r"\d", named)) and (_a_time(named) or _an_amount(named)))):
            return False
    if (head and not INSTRUCTS.match(_undecorated(head.group(1)))
            and not ASKS_HEAD.match(_undecorated(head.group(1)))
            and not SET_LABEL.match(_undecorated(head.group(1)).strip())):
        return True
    words = opening.rstrip(".!").split()
    return (len(words) <= 6 and bool(BALD.match(opening))
            and not BALD_VERB.search(opening)
            and not INSTRUCTS.match(opening) and not REASON_OPENS.match(opening)
            and not A_VERB_THEN_THE_THING.match(opening)
            and not _a_clear_time(opening) and not _a_figure_that_counts(opening))


DOES = re.compile(
    r"\b(?:first|firstly|then|next|after that|afterwards|finally|lastly|start by|start with|"
    r"begin by|once (?:it|that|you)|step one|step 1|before you|while you|leave it|put it|"
    r"take it|turn it|give it|run it|use a|use the|you (?:could|can|should|need to) (?:try|use|"
    r"start|put|take|run|give|leave|set|check))\b", re.I)
INSTRUCTS = re.compile(
    r"^(?:open|book|ring|call|phone|top|wipe|soak|give|leave|put|take|turn|run|use|set|check|"
    r"clean|wash|rinse|melt|stir|mix|fry|boil|bake|roast|grill|simmer|add|pour|spread|cut|chop|"
    r"slice|peel|grate|whisk|beat|knead|roll|press|heat|cook|drain|freeze|cool|cover|store|keep|"
    r"throw|bin|recycle|replace|repair|fit|fix|install|service|bleed|flush|tie|wrap|apply|ask|tell|"
    r"send|email|visit|go|start|finish|stop|avoid|make|buy|order|measure|weigh|label|file|"
    r"register|report|complain|sign|write|read|watch|listen|carry|hold|stand|sit|wait|test|"
    r"taste|smell|look|choose|pick|swap|follow|keep|get|bring|put|note|note down|squeeze|rub|"
    r"scrape|buff|dab|blot|scoop|trim|mist|sweep|pat|fold|split|delay|aim|try|hook|wedge|prop|"
    r"secure|tape|glue|batch|preheat|defrost|pick over|sort out|go through|block|treat|air|"
    r"cancel|renew|practise|practice)\b",
    re.I)
A_CALCULATION = re.compile(
    r"^(?:multiply|divide|subtract|convert|work out|work back|add up|share out|multiply out)\b",
    re.I)
DOES_NOT = re.compile(r"^(?:don'?t|do not|never|avoid|skip|stop|no need to)\b", re.I)
JOB = re.compile(INSTRUCTS.pattern.replace(
    r")\b", r"|see|strap|warm|wear|feed|water|brush|rest|drink|eat|sleep|walk|save|pay|spend|charge|"
    r"plug|reset|update|download|print|scan|iron|sand|paint|screw|seal|glue|tape|hang|fold|dry|"
    r"find|"
    r"air|bath|shower|talk|say|reply|text|answer|freeze|chill|cool|defrost|thaw|soak|rinse|"
    r"change|adjust|"
    r"scrub|boil|bake|roast|fry|cook|chop|slice|peel|stir|mix|whisk|season)\b"), re.I)
SAYS_WHAT_IT_DOES = frozenset((
    "is", "are", "was", "were", "am", "makes", "make", "made", "helps", "help", "needs",
    "need", "seems", "happens", "takes", "gives", "keeps", "does", "comes", "goes", "looks",
    "sounds", "stops", "starts", "works", "hurts", "depends", "matters", "causes", "means",
    "prevents", "beats", "lowers", "raises", "reduces", "improves", "eases", "dries", "warms",
    "cools", "stays", "gets",
    "matter", "build", "builds", "vary", "varies", "cost", "costs", "change", "changes",
    "depend"))
MEANS_NAMED = re.compile(
    r"^[^:]{0,40}\b(?:routes?|ways?|options?|methods?|approaches?|choices?)\b\s*:", re.I)

MEANS_OF = re.compile(
    r"\b(?:with|using) (?:a|an|some|the)\b.{0,40}\b(?:takes? (?:off|out|away)|lifts?|removes?|"
    r"cleans?|works|does it|gets? (?:rid of|it off))\b"
    r"|:\s*(?:follow|put|take|give|get|ask|ring|call|send|keep|check|book|use|do|start|run|"
    r"leave|try|add|make|go)\b", re.I)


WANTS_INFO = re.compile(r"^(?:tell me|say which|let me know|say more)\b", re.I)


def _asks_the_person(said):
    said = " ".join(str(said or "").split())
    if not said:
        return False
    if WANTS_INFO.match(said):
        return True
    return "?" in re.split(r"(?<=[.?!])\s", said, 1)[0]
NOT_A_VERB = frozenset((
    "the", "a", "an", "this", "that", "these", "those", "it", "its", "it's", "they",
    "you", "your", "we", "our", "i", "my", "me", "he", "she", "his", "her", "there",
    "here", "what", "which", "who", "why", "how", "when", "where", "if", "once", "after",
    "before", "for", "with", "on", "in", "to", "of", "at", "by", "from", "so", "but",
    "and", "or", "also", "then", "never", "always", "most", "some", "all", "every", "any",
    "no", "not", "one", "two", "both", "each", "few", "many", "more", "less", "very"))
IMPERATIVE = re.compile(
    r"^([A-Za-z']+)\s+(?:a|an|the|your|their|its|it|them|these|those|some|one|two|each|every|"
    r"both|all|him|her|me|us|my|out|in|up|down|off|on|away)\b", re.I)


THINGS_VERB = re.compile(r"^[^\w]*(?:take|bring|pack|get|buy|grab|carry|put in)\b", re.I)


def _an_instruction(sentence):
    return bool(_imperative(sentence)) and not bool(THINGS_VERB.match(sentence or ""))


def _imperative(sentence):
    m = IMPERATIVE.match(sentence or "")
    if not m:
        return False
    word = m.group(1).lower().strip("'")
    return word not in NOT_A_VERB and not word.endswith("ing")


def _opens_on_a_job(sentence):
    m = JOB.match(sentence or "")
    if not m:
        return False
    first = re.split(r"[,;:]", (sentence or "")[m.end():], 1)[0]
    words = re.findall(r"[A-Za-z']+", first)[:3]
    if not words:
        return False
    return not any(word.lower() in SAYS_WHAT_IT_DOES for word in words)



_NOT_THE_SUBJECT = NOT_A_VERB | frozenset((
    "does", "did", "can", "could", "should", "would", "will", "shall", "was", "were", "are",
    "have", "has", "had", "get", "got", "make", "made", "need", "needs", "want", "wants",
    "like", "likes", "good", "bad", "better", "best", "okay", "fine", "worth", "still",
    "really", "think", "know", "sure", "same", "keep", "keeps", "take", "takes", "mean"))


def _stem(word):
    for end in ("ing", "ed", "es", "s"):
        if word.endswith(end) and len(word) - len(end) >= 4:
            return word[:-len(end)]
    return word


def _subject_words(text):
    said = str(text or "")
    words = set()
    for match in re.finditer(r"[A-Za-z']+", said):
        word = match.group(0)
        low = word.lower().strip("'")
        if len(low) < 4 or low in _NOT_THE_SUBJECT:
            continue
        if word[:1].isupper() and match.start() and said[match.start() - 1] not in ".!?":
            continue
        words.add(_stem(low))
    return words


def _the_same_subject(opening, line):
    if not line:
        return False
    return bool(_subject_words(line) & _subject_words(opening))


def _steps(opening, after=""):
    if (DOES_NOT.match(opening) or DOES.search(opening) or MEANS_OF.search(opening)
            or MEANS_NAMED.match(opening) or _opens_on_a_job(opening)
            or A_CALCULATION.match(opening)):
        return True
    for part in re.split(r"[:;]", opening)[1:]:
        part = part.strip()
        if part and (INSTRUCTS.match(part) or DOES.search(part) or _imperative(part)):
            return True
    if after and not _asks_the_person(after):
        if INSTRUCTS.match(after) or DOES.search(after) or _imperative(after):
            return True
    return False


INSTRUCTS_CLAUSE = re.compile(
    r"(?:^|[.:;!?]\s+|,\s+(?:then|so|and|but|just|or)\s+|,\s+)(?P<verb>be|"
    + INSTRUCTS.pattern.split("(?:", 1)[1], re.I)


def _instruction_after_a_clause(text):
    for m in INSTRUCTS_CLAUSE.finditer(text):
        if _asks_the_person(text[m.start("verb"):]):
            continue
        if m.start() == 0 and not _opens_on_a_job(text):
            continue
        return True
    return False


def _steps_in(reply):
    text = " ".join(str(reply or "").split())
    if not text:
        return False
    if _steps(first_sentence(text), second_sentence(text)):
        return True
    return _instruction_after_a_clause(text)


NEXT_IDEA = re.compile(
    r"\b(?:something|anything) else\b|\banother (?:one|option|idea|way|approach|thing)\b"
    r"|\balternatively\b|\botherwise\b|\bthe other (?:option|idea|one)|\boption (?:two|2)\b"
    r"|\bsecond option\b", re.I)
LIST_AFTER_COLON = re.compile(r":\s*\w[^:]*,\s*\w")
FOR_A_LIST = re.compile(r"\bfor\b[^,.;:]{2,70},\s*[^,.;:]{0,70}\bfor\b", re.I)
FOR_A_TIME = re.compile(
    r"\bfor\s+(?:about\s+|around\s+|roughly\s+|just\s+|another\s+|a good\s+|"
    r"at least\s+|up to\s+|half an?\s+)?"
    r"(?:\d+|one|two|three|four|five|six|seven|eight|nine|ten|fifteen|twenty|thirty|forty|"
    r"fifty|sixty|ninety|a|an|each|every)\s*-?\s*"
    r"(?:seconds?|secs?|minutes?|mins?|hours?|hrs?|days?|nights?|weeks?|months?|years?|"
    r"while|bit|moment|spell)\b", re.I)
SEQUENCES = re.compile(r"\b(?:then|after that|afterwards|next|finally|once|first)\b", re.I)


CONTRAST = re.compile(
    r"\b(?:whereas|unlike|both|either|but|while|the difference|differs?|compared|comparison|"
    r"on the other hand|the other way|instead|rather than)\b"
    r"|\b(?:cheaper|dearer|quieter|louder|faster|slower|easier|harder|bigger|smaller|"
    r"longer|shorter|better|worse|more|less|stronger|weaker|heavier|lighter)\b"
    r"|\bthan\b", re.I)


def _a_comparison(opening):
    return bool(CONTRAST.search(opening))


COUNTED_LIST = re.compile(
    r"\b(?:two|three|four|five|six|a few|several|a couple of|pair of)\b", re.I)
A_TIME_COUNT = re.compile(
    r"\b(?:two|three|four|five|six|a few|several|a couple of)\s+"
    r"(?:seconds?|minutes?|hours?|days?|weeks?|months?|years?|times|per cent|percent)\b", re.I)
_LIST_OF_THINGS = re.compile(r"[^:]{0,200}:\s*[^.]{0,300}", re.I)


def _a_list_of_things(opening):
    found = _LIST_OF_THINGS.search(opening or "")
    if not found:
        return False
    after = found.group(0).split(":", 1)[1]
    return after.count(",") >= 2 or (after.count(",") >= 1 and re.search(r"\band\b", after, re.I))


def _options(opening):
    if re.search(r"\b(?:1\.|1\)|first option|option one|one idea)\b", opening, re.I):
        return True
    if re.search(r"\bor\b", opening, re.I):
        return True
    if ";" in opening:
        return True
    if NEXT_IDEA.search(opening):
        return True
    if (FOR_A_LIST.search(opening) and not FOR_A_TIME.search(opening)
            and not SEQUENCES.search(opening)):
        return True
    if LIST_AFTER_COLON.search(opening) and not SEQUENCES.search(opening):
        return True
    if LIST_AFTER_COLON.search(opening) and _three_things_after_the_colon(opening):
        return True
    return _two_things_to_do(opening)


PLAN_VERB = re.compile(r"^(?:plan|block|book|aim)", re.I)


def _two_things_to_do(opening):
    head = re.split(r"\.\s", opening, maxsplit=1)[0].rstrip(".")
    if SEQUENCES.search(head):
        return False
    found = 0
    for part in re.split(r",?\s+and\s+", head):
        part = part.strip()
        if len(part.split()) < 2 or not (INSTRUCTS.match(part) or PLAN_VERB.match(part)):
            break
        found += 1
    return found >= 2


def _three_things_after_the_colon(opening):
    parts = re.split(r":", opening, maxsplit=1)
    if len(parts) < 2:
        return False
    after = parts[1].strip()
    if INSTRUCTS.match(after) or SEQUENCES.search(parts[1]):
        return False
    return len(re.findall(r",\s+\S", parts[1])) >= 2


CAUSE = re.compile(
    r"\b(?:because|that'?s why|which is why|the reason|reason is|since|so that|due to|"
    r"comes? from|caused by|it happens|the cause|as a result|is down to|thanks to|"
    r"which means|means that|at which|stems? from|leads? to|that'?s what|"
    r"that is what|this is what|is what makes)\b|, so\b"
    r"|\b(?:goes?|gets?|turns?|becomes?|comes? out|feels?)\b.{0,40}\b(?:when|if|because)\b"
    r"|\b(?:is|are) (?:usually|often|nearly always|mostly|generally|really|just) the\b"
    r"|\b(?:often|usually|sometimes|mostly|generally|nearly always|probably)\s+means?\b"
    r"|\bso\b.{0,40}\bthat\b"
    r"|\b(?:is|are|was|were) (?:the|a|an) .{0,50}\b(?:rather than|not)\b"
    r"|\b(?:which |that )?happens? (?:when|if|because)\b"
    r"|\b(?:especially|particularly) (?:when|if|in)\b"

    r"|\b(?:is|are|was|were)\s+\w+ed\s+rather than\b"
    r"|\b(?:sticks?|stuck|smells?|smelt|tastes?|fades?|squeaks?|clicks?|wobbles?|sags?|leaks?|"
    r"cracks?|burns?|turns?|goes?|gets?|comes? out|feels?|looks?|sounds?|happens?|builds? up|"
    r"collects?|gathers?|settles?|clings?|pools?|spreads?|grows?|stops?|dies?|fails?|drops?|"
    r"floats?|sinks?|rises?|falls?|heats?|cools?|shrinks?|expands?|swells?|warps?|splits?|"
    r"melts?|freezes?|curdles?|separates?|wears?|rots?|wilts?|droops?|curls?)\b"
    r".{0,25}\b(?:when|if|because|with|from)\b"
    r"|\b(?:is|are|was|were|has|have|had)\s+(?:usually|often|normally|mostly|generally|probably|"
    r"most likely|nearly always|just|really|only|simply)?\s*(?:(?:under|over|un)\w+|"
    r"\btoo\b|\bnot\b)\s*\w*\b"
    r"|\b(?:has|have|had|did|does|do|is|are|was|were)\s+not\s+\w+\s+(?:long\s+)?enough\b"
    r"|,\s*which\s+(?:is|was|means)\b"
    r"|\b(?:is|are|was|were)\s+(?:\w+\s+)?\w+\s*,\s*\w+\s+or\s+(?:both|so|else)\b"
    r"|\b(?:is|are|was|were)\b[^.;:!?]{0,40}\brather than\b"
    r"|\b(?:is|are|was|were)\s+(?:the|a|an)\s+\w+(?:\s+\w+){0,4}\s+(?:(?<!to )\w+ing|\w+ed)\b"
    r"|\b(?:is|are|was|were)\s+(?:\w+ly\s+)?\w+\s*,\s*not\b"
    r"|,\s*(?:making|leaving|causing|giving|sending|turning|setting|which\s+(?:makes|causes|leaves|gives))\b"
    r"|\b(?:which|that)\s+causes?\b"
    r"|\b(?:one|two|three|four|five|\d+)\s+(?:things|reasons|causes|factors|suspects)\s+\w"
    r"|\b(?:is|are|was|were)\s+(?:the|a|an)\s+\w+(?:\s+\w+)?\s+or\s+(?:the|a|an)\b"
    r"|\b(?:is|are|was|were)\s+(?:\w+\s+)?\w+\s+[-\u2013\u2014]\s+\w"
    r"|\b(?:is|are|was|were)\s+(?:nearly always|usually|often|mostly|always|almost always)?\s*"
    r"(?:the|a|an)?\s*\w+(?:\s+\w+){0,2}\s+or\s+(?:the|a|an)\b"
    r"|\binstead of\b|\bpoints? (?:at|to)\b"
    r"|\b\w+ing\s+(?:from|off|through)\b|\bfrom\s+(?:too|not|lack of|a lack)\b", re.I)


CAUSE_IS = re.compile(
    r"\b(?:is|are|was|were)\s+(?:usually\s+|often\s+|mostly\s+|nearly always\s+|generally\s+)?"
    r"(?:(?:a|an|the)\s+)?[a-z][a-z-]*(?:\s+[a-z][a-z-]*){0,3}\s+"
    r"(?:of|that|which|from|turning|sitting|going|coming|leaving|building|"
    r"(?<!than )(?<!more )(?<!less )\b(?:in|on|at|under))\b", re.I)


CAUSE_WHEN = re.compile(
    r"\b(?:\w+s|\w+ed|is|are|was|were|gets?|got|goes|go|came|comes)\b\s+(?:when|if|because)\b",
    re.I)


WANTS_THE_CAUSE = re.compile(
    r"\b(?:wants?|needs?|craves?|is asking for|is crying out for|is begging for)\b", re.I)
WANTS_OF_THE_PERSON = re.compile(
    r"^(?:you|i|we|they|he|she|one|people|somebody|someone)\s+(?:just\s+|really\s+|only\s+)?"
    r"(?:want|wants|need|needs|will want|will need)\b", re.I)


A_COUNT_OF_THINGS = re.compile(
    r"\b(?:on|down to)\s+(?:two|three|four|five|several|a few)\s+"
    r"(?:things|reasons|factors|parts|steps|rules)\b", re.I)

PURPOSE = re.compile(
    r"\bthe point of (?:it |them |this |that )?(?:is|was)\b"
    r"|\b(?:its|their|his|her) (?:job|point|purpose|use) is\b"
    r"|\bthe (?:point|purpose|job|use) is (?:to|that)\b", re.I)
PURPOSE_TO = re.compile(r"^(?:it is |its |the )?(?:to|for) [a-z]+", re.I)
MERIT = re.compile(
    r"\bworth it\b|\bworth having\b|\bworth doing\b|\bworthwhile\b|\bworth the\b"
    r"|\b(?:usually|generally|probably|mostly) (?:yes|no|worth)\b"
    r"|\b(?:yes|no)\b[^.!?]{0,40}\b(?:if|when|unless|for|in a|as long as)\b", re.I)


def _a_reason(opening, line=None):
    if CAUSE.search(opening):
        return True
    if (PURPOSE.search(opening) or PURPOSE_TO.match(opening) or MERIT.search(opening)
            or (UNSETTLED.search(opening) and EVIDENCE_SAYS.search(opening))):
        return True
    if INSTRUCTS.match(opening) or DOES_NOT.match(opening):
        return False
    if SENDS_THEM_ON.search(opening):
        return False
    if CAUSE_WHEN.search(opening):
        return True
    if (line is not None and WANTS_THE_CAUSE.search(opening)
            and not WANTS_OF_THE_PERSON.match(opening) and _names(opening, line)):
        return True
    if A_COUNT_OF_THINGS.search(opening):
        return True
    return bool(CAUSE_IS.search(opening)) and (line is None or _names_the_subject(opening, line))


UNSETTLED = re.compile(
    r"\b(?:(?:nobody|no one|no-one) (?:really )?(?:knows|is sure|can say|agrees)|"
    r"it is not (?:known|certain|settled|clear)|(?:unclear|unsettled|still debated?|"
    r"a matter of debate|not fully understood))\b", re.I)
EVIDENCE_SAYS = re.compile(
    r"\b(?:evidence|studies|research|the work on it|experts|biologists|historians|"
    r"economists|scientists)\b[\w\s,'\u2019-]{0,40}?"
    r"\b(?:points? (?:at|to)|suggests?|shows?|indicates?|thinks?|suspects?|"
    r"leans? (?:to|towards)|is that)\b|\bbest (?:guess|evidence)\b", re.I)


EXPLAINS = re.compile(
    r"\b(?:is|are|was|were|means?|comes? from|happens? (?:when|if|because)|because|"
    r"the reason|"
    r"causes?|caused|brings?|brought|leads? to|led to|sets? off|triggers?|gives? you|"
    r"is behind|is down to|stems? from|comes? down to)\b", re.I)


SENDS_THEM_ON = re.compile(
    r"\b(?:one|something|a thing|the kind of thing)\s+(?:worth|to (?:have|get|see|go|ring|call|book|"
    r"check|ask|look|speak|talk|keep|take|make|do|be|try|use|buy|find|stop|fix|start|wait|leave|"
    r"stay|read|watch|wash|clean|test|measure|move|change|put|give|send|pay|see))\b|"
    r"\b(?:book|ring|call|see|visit)\s+(?:a|the|your)\s+(?:gp|doctor|vet|dentist|nurse)\b|"
    r"\bappointment\b|\blooked at\b|\bchecked out\b", re.I)


def _head_explains(opening):
    head = opening.split(":", 1)
    if len(head) < 2:
        return False
    if SENDS_THEM_ON.search(head[0]):
        return False
    return bool(EXPLAINS.search(head[0])) and not _imperative(head[0])


_PREFERS_STATED = re.compile(PREFERS.pattern.replace("|rather|", "|", 1), re.I)

FIGURE_HEAD = re.compile(
    r"^[£$\u20ac]?\s?\d|^[\u00bd\u00bc\u00be]|^(?:one|two|three|four|five|six|seven|eight|nine|ten|"
    r"eleven|twelve|fifteen|twenty|thirty|forty|fifty|sixty|seventy|eighty|ninety|hundred|"
    r"a hundred|half a)\b", re.I)


_CLEAR = (
    (TIME, _a_clear_time_at_the_head),
    (AMOUNT, _an_amount_at_the_head),
    (STEPS, _steps),
    (PLACE, lambda opening: bool(PLACE_AS_EVIDENCE.search(opening))),
    (PERSON, lambda opening: bool(PERSON_WORD.search(opening))),
    (MEANING, lambda opening: bool(MEANS.search(opening))),
    (YESNO, lambda opening: bool(VERDICT_OPEN.match(opening))),
    (PICK, lambda opening: bool(_PREFERS_STATED.search(opening))),
    (REASON, lambda opening: bool(REASON_OPENS.match(opening))),
)
_FIGURES = frozenset((TIME, AMOUNT))

def _a_meaning_or_a_statement(opening):
    if SAYS_NOTHING_ABOUT_IT.match(opening or ""):
        return False
    if _a_meaning(opening):
        return True
    return _a_statement_answers_it(opening)


def _a_statement_answers_it(opening):
    if not opening or opening.rstrip().endswith("?"):
        return False
    if (is_a_punt(opening) or NOTHING_TO_GO_ON.match(opening)
            or SAYS_NOTHING_ABOUT_IT.match(opening) or _an_opening_job(opening)):
        return False
    if _an_origin(opening):
        return False
    words = re.findall(r"[A-Za-z0-9'\u2019-]+", opening)
    if len(words) <= 10 and _a_figure(opening) and not COPULA.search(opening):
        return False
    return len(words) >= 5


NOTHING_TO_GO_ON = re.compile(
    r"^(?:nothing (?:from me|on my side|more from me|in hand|"
    r"to (?:add|say|cut|shorten|go on))\b|"
    r"there (?:is|'?s|isn'?t|'?s not) nothing (?:from me|on my side|more|in hand|"
    r"to (?:add|say|cut|shorten))\b|"
    r"there'?s nothing (?:from me|on my side|more|in hand|to (?:add|say|cut|shorten))\b|"
    r"'?(?:that|it)'? could be (?:a lot|anything|many|loads|one of|several)\b)", re.I)


SAYS_NOTHING_ABOUT_IT = re.compile(
    r"^(?:"
    r"(?:honestly,? |well,? )?(?:i|we) (?:have|'?ve) no idea\b|"
    r"(?:honestly,? |well,? )?(?:i|we) (?:do not|don'?t|dont|could not|couldn'?t|can'?t|cannot) "
    r"(?:know|say|tell you|help with (?:that|this|it))\b|"
    r"(?:nobody|no one|no-one|not many people) (?:really )?(?:knows|could say)\b|"
    r"(?:it|that|this) (?:depends|all depends) "
    r"(?:on (?:the person|the individual|who you ask|each person|the person concerned)|, honestly)\b|"
    r"(?:it|that|this) (?:varies|changes|differs) "
    r"(?:a lot |a great deal |a bit )?(?:from person to person|from one person to another|"
    r"between people|by person)\b|"
    r"(?:it|that|this) (?:is|'?s) (?:different|not the same|much the same) "
    r"(?:for everyone|for everybody|for each|for most people)\b|"
    r"(?:it|that|this) (?:is|'?s) (?:a|such a) big question\b|"
    r"(?:it|that|this) (?:is|'?s) not something (?:i|we) can help\b|"
    r"(?:it|that|this) (?:is|'?s|was) beyond (?:me|what i know|my knowledge)\b|"
    r"(?:(?:you|we) (?:should|could|might) |(?:i would |i'?d )?)?(?:ask|speak to|talk to|see|"
    r"check with) (?:an?|your|the) \w+(?: \w+)? about (?:that|this|it)\b|"
    r"(?:it|that) (?:was|has been|is) a (?:long|busy|hard|tough|rough|hectic) "
    r"(?:day|week|morning|night)\b|"
    r"there (?:is|'?s) a lot (?:to say|said)\b|"
    r"(?:it|that) (?:is|'?s) hard to say\b|"
    r"(?:this|that|it) (?:is|'?s) (?:one of those|the kind of) (?:questions|things)\b|"
    r"(?:a|the) (?:quick |short |little )?(?:search|google|look it up)\b"
    r"[^.]{0,30}?\b(?:should|will|would|can)\b|"
    r"(?:no|not a|there'?s no) (?:straight|simple|clear|easy) answer\b"
    r")", re.I)


COPULA = re.compile(r"\b(?:is|are|was|were|means|equals|measures|amounts to)\b", re.I)


A_JOB_LANDS = re.compile(r"^([A-Za-z']+)\s+(?:with|by|at|for|from|into|to|about|through|round|"
                         r"around|over|under|back|\d+|three|four|five|six|seven|eight|nine|ten|"
                         r"a few|several)\b", re.I)


AN_ORDINAL_OPENING = re.compile(r"^(?:(?:first|firstly|then|next|after that|finally|lastly|"
                                r"to start|to begin|start by|begin by|step one|step 1)"
                                r"\b[,:]?\s*)", re.I)


def _an_opening_job(opening):
    if _an_instruction(opening):
        return True
    rest = AN_ORDINAL_OPENING.sub("", opening or "")
    if rest != (opening or "") and _an_instruction(rest):
        return True
    match = A_JOB_LANDS.match(rest)
    if not match:
        return False
    word = match.group(1).lower().strip("'")
    return word not in NOT_A_VERB and not word.endswith("ing")


_CHECKS = {
    TIME: _a_time,
    COMPARE: _a_comparison,
    AMOUNT: _an_amount,
    PLACE: _a_place,
    PERSON: _a_person,
    MEANING: _a_meaning_or_a_statement,
    YESNO: _a_yesno,
    PICK: _a_pick,
    STEPS: _steps,
    OPTIONS: _options,
    REASON: _a_reason,
}


def fits(reply, want, line=None):
    return gives(reply, want, line)


_EMPTY = frozenset((
    "about", "after", "again", "before", "being", "could", "doing", "first", "going", "have",
    "just", "like", "make", "much", "need", "only", "really", "should", "still", "than", "that",
    "their", "them", "then", "there", "these", "they", "thing", "this", "those", "want", "what",
    "when", "where", "which", "while", "will", "with", "would", "your", "yours", "from", "into",
))
PERMISSION = re.compile(
    r"\b(?:can|could|should|shall|may|do|does|did|is it|are they|am i) (?:i|we|you|it|they|my|"
    r"i have to|i need to|we need to)\b|\bdo i need\b|\bis it ok\b|\bis it safe\b|"
    r"\bam i allowed\b|\bi (?:should|must|need to|have to)\b", re.I)
JOB_ANY = re.compile(INSTRUCTS.pattern.replace("^(?:", "(?:", 1).replace(
    r")\b", r"|double|halve|split|scale|reheat|refreeze)\b"), re.I)
SIDES = re.compile(r"([a-z0-9']+(?: [a-z0-9']+)?) or ([a-z0-9']+(?: [a-z0-9']+)?)", re.I)
COMPARATIVE_THAN = re.compile(
    r"([^?.!,;:]{1,40}?)\s+(?:much |a bit |a lot |far |way |any |still )?"
    r"(?:\b(?!rather\b|other\b|fewer\b)\w+er\b|more \w+|less \w+|worse)"
    r"((?:\s+(?!than\b)(?!(?:\w+er|more|less|worse)\b)\w+){0,2})\s+than\b\s*"
    r"([^?.!,;:]{1,40})", re.I)
SIDES_VS = re.compile(r"([a-z']+(?: [a-z']+)?)\s+vs\.?\s+([a-z']+(?: [a-z']+)?)", re.I)
SIDE_FILLER = frozenset((
    "a", "an", "the", "is", "are", "was", "were", "would", "will", "do", "does", "did", "which",
    "what", "and", "or", "but", "so", "then", "that", "this", "these", "those", "it", "its",
    "your", "my", "our", "their", "his", "her", "me", "us", "them", "be", "being", "been", "get",
    "gets", "got", "buy", "buying", "have", "has", "had", "should", "shall", "could", "can"))
A_SIDE_WINS = re.compile(
    r"\b(?:is|are|was|were) (?:still |usually |often |much |far |a bit )?(?:the )?(?:better|best|"
    r"kinder|healthier|cheaper|safer|stronger|quicker|smarter|more useful)\b"
    r"|\bthe (?:better|best|kinder|healthier|cheaper|safer|stronger|quicker|smarter|easier) "
    r"(?:choice|buy|option|bet|value|start|one|bowl|loaf|plan|pick|of the two)\b"
    r"|\b(?:wins?|won)\b"
    r"|\b(?:take|get|go for|pick|choose|buy|stick with) (?:the|a|an) \w+"
    r"|\bnothing (?:[a-z]+ ){0,4}comes close\b|\bcomes? close\b"
    r"|\bif you (?:want|need|have|are)\b"
    r"|\b(?:much|far|by far|a lot|still|easily) the (?:better|best|cheapest|healthiest|easiest)\b"
    r"|\bon (?:that|this) one\b|\btwice (?:as|the)\b|\bhalf the (?:price|cost|time|weight|size)\b"
    r"|\b(?:is|are|was|were) (?:much |far )?(?:further|longer|bigger|heavier|lighter|warmer|"
    r"colder|stronger|quicker|faster|cheaper|worse|better) than\b"
    r"|\bthe one (?:to|that|for|I would|id)\b"
    r"|^both\b|\bboth, and\b", re.I)


LINE_TEXT_FIELDS = ("plain", "clean", "text", "norm_text", "norm")


def _line_text(line):
    if isinstance(line, dict):
        for field in LINE_TEXT_FIELDS:
            value = line.get(field)
            if isinstance(value, str) and value.strip():
                line = value
                break
        else:
            line = ""
    return " ".join(str(line or "").lower().replace("\u2019", "'").split())


def _words(text):
    return re.findall(r"[a-z']+", str(text or "").lower().replace("\u2019", "'"))


THE_THING_ASKED = re.compile(
    r"^(?:what'?s|what is|what are|what was|what were|what does|what do|what did|"
    r"how does|how do|tell me about|what about)\s+(?:(?:an|a|the)\b\s*)?(.+)$", re.I)
_ENDS_THE_THING = frozenset("""
    and or but for in on at to with of from about when while if that which who whom whose how
    why where do does did is are was were be been being mean means meant cost costs worth
    make makes made need needs want wants go goes get gets come comes work works help helps
    take takes give gives happen happens feel feels look looks sound sounds include includes
    cover covers contain contains show shows sit sits stand stands say says called call
    used using made based known named supposed said done grown kept sold eaten worn driven written
    built filled meant
""".split())
_ARTICLE = re.compile(r"^(?:a|an|the|your|my|his|her|their|our|its|this|that|these|those|"
                      r"any|some)\s+", re.I)


_NOT_A_THING = frozenset("""
    i you we they it that this there one someone anyone everyone nobody everything anything
    something nothing people
""".split())


def _the_thing_asked(said):
    match = THE_THING_ASKED.match(said or "")
    if not match:
        return ""
    words = []
    for word in re.findall(r"[a-z0-9']+", match.group(1).lower().replace("\u2019", "'")):
        if word in _ENDS_THE_THING or word in _EMPTY:
            break
        words.append(word)
        if len(words) == 3:
            break
    if not words or words[0] in _NOT_A_THING:
        return ""
    if max(len(w) for w in words) < 2:
        return ""
    return " ".join(words)


_JUDGES_THE_THING = re.compile(
    r"^(?:is|are|was|were|should|must|ought|needs?)?\s*(?:be\s+)?(?:not\s+)?(?:good|bad|great|"
    r"fine|okay|ok|"
    r"safe|worth|better|worse|best|worst|useless|rubbish|lovely|nice|amazing|brilliant|terrible|"
    r"awful|really|usually|often|always|never|definitely|probably|a (?:good|bad|great|waste|rip|"
    r"must)|the (?:best|worst|only)|your|a waste|the wrong)\b", re.I)
_ADVISES_THE_THING = re.compile(
    r"^(?:should|must|ought|needs? to|need to|has to|have to|had to)\b", re.I)
_SAYS_WHAT_IT_IS = re.compile(
    r"^(?:is|are|was|were|has|have|had|can|cannot|do|does|did|give|gives|provide|provides|let|"
    r"lets|allow|allows|help|helps|mean|means|refers|comes|runs|works|starts|ends|takes|costs|"
    r"keeps|contains|restarts|pays|holds|covers|makes|sits|stands|forms|happens|moves|lubricates|"
    r"carries|spreads|turns|shows|includes|protects|needs)\b", re.I)


_A_DOING = re.compile(
    r"^\w+s\s+(?:how|what|which|when|where|whether|who|you|it|them|him|her|us|me|the|a|an|"
    r"your|their|its|some|any|each|every|all|only|just)\b", re.I)


_PUTS_THE_THING_TO_USE = re.compile(
    r"^(?:use|put|add|place|stick|tie|clip|screw|wear|keep|hold|ride|apply|spread|slide|hang)\b",
    re.I)


def _uses_the_thing(opening, thing):
    if not thing or not _PUTS_THE_THING_TO_USE.match(opening):
        return False
    low = opening.lower()
    at = low.find(thing)
    if at < 0:
        return False
    return bool(re.search(r"\b(?:to|for|so)\b", low[at:]))


def _defines_the_thing(opening, said):
    thing = _the_thing_asked(said)
    if not thing:
        return False
    if _uses_the_thing(opening, thing):
        return True
    head = _ARTICLE.sub("", opening.strip()).lower()
    if not head.startswith(thing + " ") and not head.startswith(thing + "'"):
        return False
    rest = head[len(thing):].strip()
    if _JUDGES_THE_THING.match(rest) or _ADVISES_THE_THING.match(rest):
        return False
    if " " not in thing and not (_SAYS_WHAT_IT_IS.match(rest) or _A_DOING.match(rest)):
        return False
    return len(rest.split()) >= 3


def _name_words(text):
    return re.findall(r"[a-z0-9']+", str(text or "").lower().replace("\u2019", "'"))


def _long_enough_a_name(word, least=3):
    return len(word) >= least or any(ch.isdigit() for ch in word)


def _names(opening, said):
    reply = set(_words(opening))
    for word in set(_words(said)):
        if not _long_enough_a_name(word, 4) or word in _EMPTY:
            continue
        if word in reply or word[:-1] in reply or word[:-2] in reply:
            return True
    return False


def _names_the_subject(opening, said):
    reply = set(_words(opening))
    for word in set(_words(said)):
        if not _long_enough_a_name(word, 3) or word in _EMPTY:
            continue
        if len(word) == 3:
            if word in reply:
                return True
            continue
        if word in reply or word[:-1] in reply or word[:-2] in reply:
            return True
        for said_word in reply:
            if said_word.startswith(word):
                return True
    return False


def _opens_on_the_lines_verb(opening, said):
    words = opening.split()
    if not words or len(words) > 5:
        return False
    first = _words(opening)
    if not first or len(first[0]) < 3:
        return False
    stem = first[0]
    for match in re.finditer(r"\b(?:should|must|need to|have to)\b\s+(?:i\s+)?([a-z]{3,})",
                             said, re.I):
        verb = match.group(1).lower()
        if verb == stem or (verb.startswith(stem[:-1]) and len(stem) > 3):
            return True
    return False


def _trimmed(words):
    start, end = 0, len(words)
    while start < end and words[start] in SIDE_FILLER:
        start += 1
    while end > start and words[end - 1] in SIDE_FILLER:
        end -= 1
    return words[start:end]


def _the_pair_up(text):
    clean = " ".join(str(text or "").split())
    found = COMPARATIVE_THAN.search(clean)
    if found:
        left = _trimmed(_words(found.group(1)))
        right = _trimmed(_words(found.group(3)))
        spent = set(_words(found.group(2)))
        while left and left[-1] in spent:
            left = left[:-1]
        if not left or not right:
            return None
        return (left[-2:], right[:2])
    found = SIDES.search(clean) or SIDES_VS.search(clean)
    if found:
        return (_words(found.group(1)), _words(found.group(2)))
    return None


def _a_side_said_in_the_reply(side, ordered, words):
    for word in side:
        if not _long_enough_a_name(word) or word in _EMPTY:
            continue
        if _a_side_word_is_named(word, ordered, words):
            return True
    return False


def _the_side_wins(opening, line):
    pair = _the_pair_up(_line_text(line))
    if not pair:
        return False
    sides = [side for side in pair if side]
    if not sides:
        return False
    ordered = _words(opening)
    words = set(ordered)
    named = any(_a_side_said_in_the_reply(side, ordered, words) for side in sides)
    if not (named or re.match(r"^both\b", opening, re.I)):
        return False
    return bool(A_SIDE_WINS.search(opening))


def _names_a_side(opening, said):
    sides = SIDES.search(said or "")
    if not sides:
        return False
    reply = _name_words(opening)[:3]
    side_words = [word for side in sides.groups() if side for word in _name_words(side)]
    return _a_side_said_in_the_reply(side_words, reply, set(reply))


_SIDE_EMPTY = frozenset((
    "the", "and", "but", "not", "for", "with", "your", "you", "our", "its", "it's", "this", "that",
    "these", "those", "what", "which", "from", "into", "than", "then", "are", "was", "were", "has",
    "have", "had", "one", "two", "any", "all", "much", "more", "less", "same",
))


def _a_side_word_is_named(word, ordered, words):
    for reply_word in words:
        if reply_word == word:
            return True
        shorter, longer = sorted((reply_word, word), key=len)
        if len(longer) > 4 and longer.startswith(shorter) and shorter[-1:] not in ("s",):
            return True
        if len(shorter) >= 3 and shorter.rstrip("s") == longer.rstrip("s"):
            return True
    for index in range(len(ordered) - 1):
        if ordered[index] + ordered[index + 1] == word:
            return True
    return _initials_named(word, ordered)


def _initials_named(word, reply_words):
    if not 2 <= len(word) <= 4 or not word.isalpha():
        return False
    for start in range(len(reply_words)):
        pos = 0
        for spoken in reply_words[start:start + len(word)]:
            if pos < len(word) and spoken[:1] == word[pos]:
                pos += 1
        if pos == len(word):
            return True
    return False


def _names_both_sides(reply, said):
    said = (said or "").lower().replace("\u2019", "'")
    sides = None
    for pattern in SIDE_PAIRS:
        sides = pattern.search(said)
        if sides:
            break
    pairs = [sides.groups()[:2]] if sides else []
    if not pairs:
        pair = _the_pair_up(said)
        if pair and all(pair):
            pairs = [[" ".join(side) for side in pair]]
    if not pairs:
        return None
    ordered = _words(reply)
    words = set(ordered)
    named, missing = 0, []
    for side in pairs[0]:
        side_words = {word for word in _words(side)
                      if len(word) >= 3 and word not in _SIDE_EMPTY}
        if not side_words:
            continue
        if any(_a_side_word_is_named(word, ordered, words) for word in side_words):
            named += 1
        else:
            missing.append(min(side_words, key=len))
    if named + len(missing) < 2:
        return None
    if named >= 2:
        return True
    if any(len(word) <= 3 for word in missing):
        return None
    return False


def _the_job_named(opening, said):
    if not PERMISSION.search(said or ""):
        return False
    if not _names(opening, said):
        return _opens_on_the_lines_verb(opening, said)
    if _steps(opening):
        return True
    if JOB_ANY.search(" ".join(opening.split()[:12])):
        return True
    if len(opening.split()) > 9:
        return False
    first = _words(opening)
    if not first or len(first[0]) < 4:
        return False
    stem = first[0]
    for word in _words(said):
        if len(word) >= 4 and (word == stem or word.startswith(stem) or stem.startswith(word)):
            return True
    return False

PATH_THEN_VERB = re.compile(
    r"(?:>|\u2192|->)\s*\S.{0,120}\b(?:find|choose|select|click|tap|press|open|set|switch|turn|"
    r"tick|untick|check|uncheck|change|remove|delete|add|enable|disable|toggle)\b", re.I)


GARDEN = re.compile(
    r"(?:sow|plant|prune|dig|mow|scarify|weed|mulch|repot|stake|harvest|deadhead|sprinkle|hammer|"
    r"grout|caulk|unblock|unplug)\b", re.I)



DOES_NOT_ANYWHERE = re.compile(
    r"(?:^|[.:;!?]\s+|,\s+(?:then|so|and|but|just|or)\s+|:\s+)"
    r"(?:don'?t|do not|never|avoid|skip|no need to)\s+"
    r"(?P<after>[^.;:!?]{0,40})", re.I)
NOT_A_STEP_BUT_REASSURANCE = re.compile(
    r"^(?:worry|panic|fret|stress|beat yourself|mind|bother|overthink|"
    r"be (?:too )?(?:hard|afraid|scared|embarrassed|guilty|silly|worried|shy)|"
    r"feel (?:bad|guilty|silly|stupid)|feel like|let (?:it|that|them)\b)",
    re.I)


def _a_step_told_as_what_not_to_do(text):
    for m in DOES_NOT_ANYWHERE.finditer(text or ""):
        after = m.group("after").strip()
        if not after:
            continue
        if NOT_A_STEP_BUT_REASSURANCE.match(after):
            continue
        return True
    return False

_STEPS_IN = _steps_in


def _steps_in(reply):
    if _STEPS_IN(reply):
        return True
    text = " ".join(str(reply or "").split())
    if _a_step_told_as_what_not_to_do(text):
        return True
    for sentence in re.split(r"(?<=[.!?])\s+", text):
        if GARDEN.match(sentence) or PATH_THEN_VERB.search(sentence):
            return True
    return _words_handed_over(text)


SAID_WORDS = re.compile(
    r"^(?:just |only |maybe |perhaps |something like:? |try:? |say:? |start with:? |"
    r"open with:? |how about:? )?"
    r"\s*[\"'\u201c\u2018\u00ab][^\"'\u201d\u2019\u00bb]{8,}[.!?,]?[\"'\u201d\u2019\u00bb]",
    re.I)


def _words_handed_over(text):
    return bool(SAID_WORDS.match(text or ""))

_MONEY = (r"(?:[£$€]\s*\d[\d,.]*"
          r"|\b\d[\d,.]*\s*(?:p|pence|pennies|quid|pounds?|bucks?|dollars?|euros?|cents?|gbp)\b)")
MONEY_RATE = re.compile(
    _MONEY + r"(?:\s*(?:to|-)\s*(?:[£$€]\s*)?\d[\d,.]*\s*(?:p|pence)?)?"
    r"\s*(?:a|an|per|each)\s+"
    r"(?:sec\w*|min\w*|hour|hr|hrs|day|week|month|year|night|visit|call|session|unit)s?\b", re.I)


def _a_money_rate(opening):
    return bool(MONEY_RATE.search(opening))


def _without_a_money_rate(opening):
    return MONEY_RATE.sub(" ", opening)


A_QUANTITY_ASK = re.compile(
    r"\b(?:enough|too (?:much|many|far|often|long|hot|cold|big|small|old|young|late|soon|heavy|"
    r"short|thick|thin|deep|tall|high|low|expensive|dear))\b", re.I)
_A_QUANTITY_NUMBER = (r"(?:\d[\d.,]*|one|two|three|four|five|six|seven|eight|nine|ten|eleven|"
                      r"twelve|fifteen|twenty|thirty|forty|fifty|sixty|ninety|hundred|half|"
                      r"a couple|a few|an|a)")
_A_QUANTITY_UNIT = (r"(?:sec|second|minute|min|hour|hr|day|week|month|year|night|kg|kilo|pound|"
                    r"mile|km|litre|pint|cup|gram|ounce|stone|cm|inch|foot|feet|metre|session|"
                    r"time|portion|serving|slice|step|dose|tablet|degree|celsius|unit|item|"
                    r"episode|page|p)s?\b")
_A_QUANTITY_RELATION = (r"(?:under|over|above|below|inside|within|short of|past|at|less than|"
                        r"more than|on the line|clear of|off the|away from)")
_A_FIGURE_AGAINST_THE_STANDARD = re.compile(
    r"\A\s*(?:[^:]{1,45}:\s*)?(?:about|around|just|only|nearly|almost|well|roughly)?\s*"
    r"(?:£\s*\d[\d.,]*|\$\s*\d[\d.,]*|€\s*\d[\d.,]*|"
    + _A_QUANTITY_NUMBER + r"[\s-]*(?:" + _A_QUANTITY_NUMBER + r"[\s-]*)?-?\s*"
    + _A_QUANTITY_UNIT + r")"
    r"(?:\s+(?:a|an|per|each)\s+(?:week|day|month|year|night|hour|session))?"
    r"\s+(?:is|are|comes|sits|lands)\s+(?:the\s+|well\s+|just\s+|a bit\s+|a little\s+)?"
    + _A_QUANTITY_RELATION + r"\b", re.I)


def _the_figure_against_the_standard(opening, said):
    if not A_QUANTITY_ASK.search(said or ""):
        return False
    return bool(_A_FIGURE_AGAINST_THE_STANDARD.match(opening or ""))

VERDICT_AFTER_A_FIGURE = re.compile(
    r"\A(?:that|it|this) (?:is|'s|would be|should be) (?:a |an |quite a |quite |a bit of a )?"
    r"(?:fair|fine|easy|doable|manageable|sensible|reasonable|safe|risky|all right|alright|okay|"
    r"ok|worthwhile|worth it|no bother)\b"
    r"|\A(?:doable|fine|fair|easy|sensible|reasonable|manageable|worth it|worth doing|workable|"
    r"sound|just the job|no bother|all right|alright)\b"
    r"|\b(?:doable|easy to|easy|manageable|sensible|reasonable|no bother|just the job|"
    r"all right|alright|worth it)\b"
    r"|\bfine (?:to|for|in|if|on|as)\b", re.I)


def _a_figure_then_the_verdict(opening, reply):
    if not opening or not (_a_time(opening) or _an_amount_with_a_unit(opening)):
        return False
    two = _opening_two(reply)
    if not two.startswith(opening):
        return False
    second = two[len(opening):].strip()
    return bool(second and (VERDICT_AFTER_A_FIGURE.search(second)
                            or VERDICT_BAND.search(second)))

AN_INSTRUCTION = re.compile(
    r"^[A-Za-z']+\s+(?:a|an|the|your|their|its|some|one|two|each|every|both|all|my|these|those)"
    r"(?=\s+[A-Za-z0-9'\u2019\"\u00a3$])"
    r"|^[A-Za-z']+\s+(?:it|them|him|her|me|us)\s+(?:off|on|out|in|up|down|away|over|back|"
    r"through|aside|together|to|into|onto|under|with|for|at|inside|across|around|along|near|"
    r"behind|beside|against)\b", re.I)
CONTRACTION_OPENER = re.compile(r"^[A-Za-z]+['\u2019](?:s|re|ll|ve|d|m)\b", re.I)
A_WELL_WISHING = re.compile(
    r"^(?:and\s+|so\s+)?(?:enjoy|hope (?:you|it|that)|all the best|take care|good luck|"
    r"sleep well|get well|have (?:a|an) (?:nice|good|great|lovely|brilliant|fab|wonderful|happy|"
    r"safe|quiet|lazy|restful|easy|better|fun|relaxing|peaceful))\b", re.I)
A_SUBORDINATE_FRAGMENT = re.compile(
    r"^(?:because|since|although|though|unless|whereas|while|if|when|after|before|as|where)\b",
    re.I)
NOT_AN_OPENER = frozenset((
    "still", "sorry", "even", "maybe", "perhaps", "honestly", "actually", "obviously",
    "apparently", "probably", "really", "quite", "please", "thanks", "ok", "okay", "well",
    "oh", "ah", "yes", "yeah", "no", "nope", "sure", "fine", "anyway",
    "love",
    "nice", "good", "great", "lovely", "brilliant", "perfect", "glad", "congratulations",
    "congrats", "cheers", "smashing", "fab", "wonderful", "grand", "ace", "decent", "super",
    "agreed", "yay", "hurrah", "hooray",
    "about", "as", "only", "around", "over", "under", "after", "before", "with", "from", "than",
    "like", "at", "in", "on", "to", "of", "for", "by", "up", "down", "out"))

HALF_A_UNIT = re.compile(
    r"^half\s+(?:a|an|the)?\s*(?:hour|hours|minute|minutes|second|seconds|day|days|week|weeks|"
    r"month|months|year|years|cup|cups|glass|glasses|pint|pints|litre|litres|liter|liters|"
    r"kilo|kilos|kilogram|kilograms|pound|pounds|mile|miles|metre|metres|meter|meters|"
    r"inch|inches|teaspoon|teaspoons|tablespoon|tablespoons|tsp|tbsp|degree|degrees)\b", re.I)


def _opens_on_a_job_to_do(sentence):
    text = str(sentence or "")
    if not AN_INSTRUCTION.match(text) or WANTS_INFO.match(text):
        return False
    if CONTRACTION_OPENER.match(text) or A_WELL_WISHING.match(text.strip()):
        return False
    if A_SUBORDINATE_FRAGMENT.match(text) and "," not in text:
        return False
    if HALF_A_UNIT.match(text):
        return False
    word = re.match(r"[A-Za-z']+", text).group(0).lower().strip("'")
    return (word not in NOT_A_VERB and word not in NOT_AN_OPENER
            and not word.endswith("ing"))

_steps_by_the_verb_list = _steps


def _steps(opening, after=""):
    return _steps_by_the_verb_list(opening, after) or _opens_on_a_job_to_do(opening)


_CHECKS[STEPS] = _steps
_CLEAR = tuple((want, _steps) if want == STEPS else (want, check) for want, check in _CLEAR)
