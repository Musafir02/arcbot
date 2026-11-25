import re

from ..memory import again as again_reply
from ..understanding.normalize import normalise
from . import A_STEP_ASK, pick, why
from ..memory import healing
try:
    from .goodnews import reads_as_good_news as _reads_as_good_news
except Exception:
    _reads_as_good_news = None
try:
    from .loss import a_thing_stopped as _a_thing_stopped
except Exception:
    _a_thing_stopped = None

BARE = re.compile(
    r"^(?:and |so )?(?:is|was|are|were|does|do|did) (?:that|this|it|all of that|all that)"
    r"(?: (?:really|actually|very|too|that))?"
    r"(?: (?:bad|normal|serious|dangerous|ok|okay|alright|all right|acceptable|fine|safe|common|"
    r"weird|odd|strange|a problem|"
    r"something to worry about|anything to worry about|worth worrying about|"
    r"(?:something|anything|a thing) (?:i should|to|that i should|worth) worry(?:ing)? about|"
    r"something (?:i should|to) be worried about))"
    r"(?: then| though| or not)?$"
    r"|^(?:and |so )?should i (?:be )?(?:worried|worry|worrying)(?: then| though)?$"
    r"|^(?:and |so )?when (?:should|do|would) i (?:be )?(?:worried|worry|worrying)"
    r"(?: about (?:it|that|this))?(?: then| though)?$"
    r"|^(?:and |so )?when (?:should|do) i (?:start|need) (?:to )?(?:be )?worry(?:ing)?$"
    r"|^(?:and |so )?is (?:that|it|this) (?:worrying|worrisome|a worry)(?: then| though)?$"
    r"|^(?:and |so )?(?:do|will|should|would) i (?:really |actually |honestly )?"
    r"(?:need|have) to (?:be )?worr(?:y|ied)"
    r"(?: about (?:it|that|this))?(?: then| though)?$"
    r"|^(?:and |so )?(?:is|was) (?:that|it|this)(?: (?:going to|gonna))? (?:get worse|"
    r"getting worse|spread|serious)$"
    r"|^(?:and |so )?(?:does|do|did) (?:that|this|it) matter(?: then| though)?$"
    r"|^(?:and |so )?(?:iz |is |s |z )?(?:that|it|this) "
    r"(?:ok|okay|fine|alright|bad|normal|serious)(?: then| though| or not)?$"
    r"|^(?:and |so |or )?(?:is|was) (?:that|it|this) (?:just|only) (?:old age|age|a phase|a stage|"
    r"the age|his age|her age|their age|tiredness|the tiredness)\??$"
    r"|^(?:and |so )?is (?:that|it|this) (?:a|much of a) (?:problem|worry|issue)(?: then| though)?$"
    r"|^(?:and |so )?(?:is|was|would|will|can|could) (?:that|this|it) (?:be )?"
    r"(?:bad|harmful|dangerous|unsafe|alright|ok|okay) for (?:me|us)(?: then| though)?$"
    r"|^(?:and |so )?(?:is|was|would|will|can|could) (?:that|this|it) (?:be )?"
    r"(?:harmful|dangerous|unsafe)(?: then| though)?$"
    r"|^(?:and |so )?(?:will|would|could) (?:that|this|it) hurt (?:me|us)(?: then| though)?$"
    r"|^(?:and |so )?(?:does|do|did|will) (?:that|this|it) (?:hurt|harmed|harm|make me ill"
    r"|make me sick)(?: then| though)?$"
    r"|^(?:and |so )?(?:am|was) i (?:ok|okay|alright|all right|normal|going mad|going crazy|"
    r"losing it|losing my mind)(?: then| though)?$"
    r"|^(?:and |so )?(?:do|would|will) i (?:really |actually )?(?:need|have) to (?:be )?"
    r"worr(?:y|ied)(?: about (?:it|that|this))?(?: then| though)?$"
    r"|^(?:and |so )?(?:should|do) i need to worry(?: then| though)?$"
)
HOW_MANY_PEOPLE = ("common", "for most people", "for most adults", "for most children",
                   "for most babies", "usual for", "is usual")

DENIES = ("harmless", "nothing to worry", "not serious", "nothing serious", "no need to",
          "nothing to be")
HARMLESS = ("harmless", "not serious", "nothing serious", "nothing to worry", "nothing to be",
            "no need to", "needs nothing doing", "does not need")
SAYS_NORMAL = ("normal", "nothing to worry", "not serious", "nothing serious", "nothing to be",
               "no need to", "harmless")
REASSURE = ("harmless", "nothing to worry", "not serious", "nothing serious", "usually",
            "normal", "no need to", "should settle", "usually settles", "will settle",
            "goes away", "just air", "nothing to be",
            "settles", "settle down", "clears up", "clears by itself", "goes by itself",
            "gets better on its own", "heals on its own", "resolves on its own",
            "does the job on its own", "is muscular",
            "is common", "common", "common in", "common at", "common for", "quite common",
            "for most people", "for most adults", "for most children", "for most babies",
            "usual for", "is usual")
CARE = ("get it checked", "get checked", "get it looked at", "get it seen", "see a doctor",
        "see your gp", "ring 111", "call 111", "999", "a&e", "get someone in",
        "get an engineer", "get a heating engineer", "call an engineer", "engineer out",
        "call out", "straight away", "as soon as you can", "urgent", "needs an engineer",
        "is an engineer's job", "stop using it", "stop and", "unplug", "turn it off",
        "switch it off", "turn the water off", "stop the cycle", "leave it off",
        "ring your vet", "ring the vet", "call your vet", "call the vet", "see a vet",
        "see your vet", "get to the vet", "vet today", "vet straight away", "ask your vet",
        "your vet will want", "phone the vet", "phone your vet",
        "gp visit", "worth a hearing test", "a referral", "for a referral",
        "health visitor", "111 line", "worth seeing", "worth getting looked at",
        "see a gp", "see the gp", "ring the gp", "phone the gp", "see a nurse",
        "ring the surgery", "call the surgery", "phone the surgery",
        "walk-in centre", "minor injuries", "out of hours", "urgent care",
        "111 line", "nhs 111", "111 will", "health visitor", "out of hours service",
        "urgent treatment centre", "ask your midwife", "ring your midwife",
        "worth a gp visit", "gp visit", "gp appointment", "doctor's appointment")
CONDITIONAL = re.compile(r"\b(?:if|unless|once|when) \w+[^.]{0,80}$")
CONDITIONAL_AFTER = re.compile(r"\b(?:if|unless|once|when|whenever)\b")
HARD_NEWS_LINES = (
    "There is no verdict to give on that one - some things are just hard, and that is not a "
    "judgement on you.",
    "I would not put that on a scale. What happened is heavy enough without working out where "
    "it sits.",
    "That is not something with a good or bad answer. It is a hard thing to carry, and you are "
    "allowed to just feel it.",
)
HARD_NEWS = re.compile(
    r"\b(?:died|dying|death|passed away|funeral|buried|cremated|hospice|"
    r"cancer|leuka?emia|lymphoma|myeloma|tumou?r|terminal|palliative|chemo|radiotherapy|"
    r"miscarriage|miscarried|stillborn|"
    r"dementia|alzheimers|motor neurone|multiple sclerosis|parkinsons|copd|"
    r"kidney failure|heart failure|liver failure|"
    r"stroke|heart attack|sepsis|"
    r"given months|not going to make it)\b", re.I)
SYMPATHY = re.compile(
    r"\b(?:i'm sorry|im sorry|so sorry|really sorry|sorry to hear|sorry for your loss|"
    r"sorry about (?:your|the)|sounds rough|that sounds rough|a real loss|how awful|that's awful|"
    r"that is awful|how sad|that's sad|that is sad|"
    r"frightening|scary|a lot to carry|no wonder|that's heavy|that is heavy|"
    r"nothing about that is a fault|hardest days?)\b", re.I)
COMPARATIVE = re.compile(r"\b(?:sooner|earlier|quicker|faster|more so|especially|particularly|"
                         r"above all)\b", re.I)
URGENT_TIME = re.compile(r"\b(?:today|tonight|now|straight away|right away|immediately|"
                         r"as soon as|first thing|urgent(?:ly)?|within \d+)\b")
A_SYMPTOM_WORD = re.compile(
    r"\b(?:skin|rash|itch|itching|eyes?|ears?|throat|chest|stomach|belly|temperature|fever|"
    r"vomit|vomiting|sick|diarrhoea|diarrhea|feeding|feeding|breath|breathing|breathless|cough|"
    r"poo|wee|blood|pain|hurts?|hurting|swelling|swollen|knee|joint|joints|mouth|teeth|tooth|"
    r"napp(?:y|ies)|nappy|wet(?:s|ting)? the bed|constipated|constipation|gums?)\b", re.I)
A_PERSON_THEY_KNOW = re.compile(
    r"\b(?:mums?|moms?|mother|father|dads?|son|daughter|kids?|child(?:ren)?|wife|husband|"
    r"partner|girlfriend|boyfriend|friend|friends|neighbours?|grans?|granny|nan|nana|"
    r"grandma|granddad|grandad|grandpa|sister|brother|aunt|uncle|cousin|bab(?:y|ies)|"
    r"in[- ]laws?|mother in law|father in law)\b", re.I)
A_RELATION_TROUBLE = re.compile(
    r"\b(?:lonely|loneliness|company|visit|visits|visiting|ring|rings|rang|call|calls|called|"
    r"speak|speaks|spoke|spoken|talk|talks|talked|talking|quiet|withdrawn|alone|"
    r"on (?:his|her|their|its) own|lives? on (?:his|her|their) own|"
    r"arguments?|arguing|row|rows|falling out|fallen out|ignores?|ignoring|"
    r"does not listen|doesnt listen|wont listen|wont say|wont go out|does not go out|"
    r"trust|trusts|jealous|suspicious|accuses?|accusing|controlling|keeps? checking|"
    r"checking (?:my|his|her|their)|"
    r"doesnt go out|birthday|anniversary|seen (?:him|her|them)|see (?:him|her|them))\b", re.I)
PERSON_ORDINARY = (
    "There is nothing there to watch for going wrong: it is an ordinary stretch, and the answer's "
    "own first step is what moves it. Do that for a few weeks - if it is the same after that, say "
    "it to them plainly rather than sitting on it.",
    "Nothing in that is a fault on either side. The small thing in the answer, done consistently, "
    "is what changes it, and if nothing has changed after a few weeks that is the point to say "
    "something out loud.",
)
PERSON_CALL = (
    "Yes - take up the first half of what I said now, and the second half is what to act on: if it "
    "is still like that after a few weeks, do the part about talking to somebody properly.",
    "Yes, that one is worth acting on rather than watching. Start with the simple step in the "
    "answer, and if nothing has moved in a few weeks, take the next step it names.",
)


NO_LINES = (
    "Nothing in that sounded like a warning sign. What would change it is the thing itself "
    "changing — getting worse, or not settling — and then it's worth getting looked at.",
    "That one is the ordinary kind, so no. Watch it rather than worry about it: if it's still "
    "the same in a week or two, or it gets worse, get someone to look at it.",
    "No — the part you asked about is the harmless kind. What to keep an eye on is change "
    "rather than the thing itself.",
)
BOTH_LINES = (
    "It's the common kind rather than a warning sign — and the check is still worth doing.",
    "Common enough, so no panic. Getting it looked at is worth doing all the same: that is what "
    "catches the less usual ones.",
    "Not a warning sign on its own, no. Common enough that mentioning it is enough rather than "
    "rushing — do that, and say what they tell you.",
)
DO_LINES = (
    "It's a job rather than a danger. Do it and see whether it holds — if it comes back, that's "
    "the point where it stops being a DIY thing.",
    "Not bad in itself, but not something to leave alone either. Do the job properly, and if it "
    "comes back after that, get someone in.",
    "Worth doing rather than worrying about. Sort it out; if it keeps coming back, that's when "
    "it's somebody else's job.",
)
FIX_ASKED_LINES = (
    "Give it a day or two and see whether it holds. If the same thing comes back, the step was "
    "not the fix and it wants a proper look.",
    "Do it and give it a few days. Coming back after that is the sign it is not something the "
    "step sorts out on its own.",
    "Try it and watch what happens next. If it stays away, that was the whole of it; if it "
    "does not, the thing behind it needs seeing to.",
)
FIX_ASKED_NOW_LINES = (
    "Do it now and check it the way you checked before. If nothing has changed at all, that step "
    "was not the fix and the next thing to look at is further in.",
    "Try it straight away. If it does what it should, that was the fix; if it behaves the same, "
    "the step was not the answer and something else is doing it.",
    "Do it and look again straight after. Unchanged means the step was not the fix, rather than "
    "that it needs longer.",
)
A_WAIT_IN_THE_STEP = re.compile(
    r"\b(?:after|within|for|over|in|another)\s+(?:a|an|the|two|three|four|five|six|few|couple|"
    r"several|\d+)\s+(?:day|days|week|weeks|night|nights|month|months)\b"
    r"|\bovernight\b|\bnext day\b|\bthe following (?:day|week)\b"
    r"|\bleave it (?:to|for)\b", re.I)
_ASKS_ABOUT_A_STEP = re.compile(
    r"\b(?:does|do|will|would|should|can|could|is|was)\b(?:\s+\w+){0,3}\s+(?:that|this|it)\b", re.I)
_ASKS_FOR_THE_STEP = re.compile(r"^\s*(?:how|what|where|when|which|who|why)\b", re.I)
_A_FIX_WORD = re.compile(
    r"\b(?:fix|fixes|fixed|sort|sorts|sorted|solve|solves|cure|cures|work|works|help|enough|"
    r"stop|stops|clear|clears|do the trick|make a difference)\b", re.I)


NOT_A_STEP_TO_WATCH = frozenset((
    "health", "pregnancy", "babyfood", "body", "caring", "complaints", "crisis_replies",
    "pharmacy", "pets", "animals", "family", "friends", "sleep",
))
NOT_A_STEP_TO_WATCH_WORDS = re.compile(
    r"\b(?:baby|babies|infant|newborn|toddler|pregnan\w*|napp(?:y|ies)|rash|fever|"
    r"vomit\w*|diarr\w*|breathless|symptom\w*|seizure|dehydrat\w*|allerg\w*|asthma|"
    r"inhaler|epipen|insulin|diabet\w*|medicin\w*|medication|antibiotic\w*|paracetamol|"
    r"ibuprofen|painkiller\w*|gp|gps|doctor|doctors|nurse|midwife|pharmac\w*|hospital|"
    r"a&e|ambulance|111|999|911|dentist|vet)\b", re.I)


def _a_job_somewhere(reply):
    flat = _flat(reply)
    if not flat:
        return False
    for clause in re.split(r"[:;.!?]|,?\s+and\s+", flat):
        words = _WORD.findall(clause.strip(" ,-"))
        if not words or words[0] not in IMPERATIVES:
            continue
        if len(words) > 1 and words[1] in ("me", "us"):
            continue
        if len(words) > 1 and words[1] in _AFTER_A_NOUN:
            continue
        return True
    return False


def the_fix_asked(clean, memory):
    flat = _flat(clean)
    if not flat:
        return ""
    words = flat.split()
    if len(words) > 10:
        return ""
    if not _ASKS_ABOUT_A_STEP.search(flat) or not _A_FIX_WORD.search(flat):
        return ""
    if _ASKS_FOR_THE_STEP.match(flat):
        return ""
    last = _last_reply(memory)
    if not last or not (opens_on_a_job(last) or _a_job_somewhere(last)):
        return ""
    if str((memory.get("last_answer") or {}).get("domain") or "").lower() in NOT_A_STEP_TO_WATCH:
        return ""
    if NOT_A_STEP_TO_WATCH_WORDS.search(last):
        return ""
    if A_WAIT_IN_THE_STEP.search(last):
        return _say(FIX_ASKED_LINES, memory, flat)
    return _say(FIX_ASKED_NOW_LINES, memory, flat)


CONDITION_LINES = (
    "Not the thing itself, no. It would stop being ordinary if {when} — that is the point to "
    "act on.",
    "Ordinary on its own, yes. It stops being ordinary if {when}, so that is what to watch.",
    "Nothing in that is a warning by itself. It becomes one if {when}: that is when it wants "
    "someone.",
)
GRIEF_FLOOR_LINES = (
    "Not something to be graded bad or not - it is a loss, and it deserves the room it takes. Be "
    "gentle with yourself, and let whoever is around you know how you are.",
    "That is not a thing to call bad, and not a thing to carry on your own. Take the help that is "
    "offered, and tell someone close how today actually went.",
    "Nothing about that is a fault in you. Give it the time it takes, and lean on the person who "
    "asks how you are.",
)
MET_CONDITION_LINES = (
    "Then you are already at the point it named, so that is the bit to act on rather than the bit "
    "to watch. Get it looked at, and say what you told me here when you do.",
    "That is the thing that answer said to act on, and it is what you are describing. Get it seen "
    "to rather than sitting with it.",
    "So it is past the watching stage: the answer's own next step is the one for now. Get that "
    "started today.",
)
WHEN_ASK = re.compile(
    r"^(?:and |so )?when (?:should|do|would) i (?:be )?(?:worried|worry|worrying)"
    r"(?: about (?:it|that|this))?(?: then| though)?$"
    r"|^(?:and |so )?when (?:should|do) i (?:start|need) (?:to )?(?:be )?worry(?:ing)?$")
WORRYING_ASK = re.compile(
    r"^(?:and |so )?is (?:that|it|this) (?:worrying|worrisome|a worry)(?: then| though)?$")
WHEN_LINES = (
    "This is the line: {when}. Short of that it is the ordinary kind, and worth watching rather "
    "than acting on.",
    "What makes it somebody else's job: {when}. Until then it is a watch-and-see.",
    "The point to act on is this: {when}. Before that it is the ordinary thing, so keep an eye on "
    "it rather than acting on it.",
)
WHEN_CALL_LINES = (
    "The line to act on: {when}. Short of that it is the watching stage, and the answer's own "
    "steps are the plan.",
    "This is where it stops being a wait-and-see: {when}. Before that, do what the answer said "
    "and keep an eye on it.",
    "What sends you to someone: {when}. Under that line the answer's steps are the whole of it.",
)
NEEDS_A_CALL = re.compile(
    r"(?P<list>[^.;:]*?)\s*(?:,\s*and\s+|\s+and\s+)?(?:needs?|wants?|want|means)\s+"
    r"(?:the\s+|your\s+|a\s+)?"
    r"(?:vet|gp|doctor|dentist|optician|pharmacist|physio|111|a&e|engineer|plumber|electrician)\b",
    re.I)
_LIST_JOIN = re.compile(r"\b(?:are|is|was|were)\s+not\s*,?\s*(?:and)?\s*$", re.I)


def _the_list_before_the_call(said):
    best = ""
    for m in NEEDS_A_CALL.finditer(str(said or "")):
        part = _LIST_JOIN.sub("", m.group("list").strip(" ,;:-"))
        part = part.strip(" ,;:-")
        words = part.split()
        if 3 <= len(words) <= 24 and len(part) > len(best):
            best = part
    if best and best.split()[0] in ("A", "An", "The"):
        best = best[0].lower() + best[1:]
    return best


CALLS_FOR = re.compile(
    r"\b(?:see|ring|call|contact|speak to|go to|get)\s+(?:a |your |the )?"
    r"(?P<who>gp|doctor|practice nurse|nurse|111|999|a&e|vet|dentist|optician|pharmacist|"
    r"surgery|midwife|physio(?:therapist)?|urgent care|out of hours)"
    r"(?P<quick>\s+(?:the same day|today|straight away|now|first thing|as soon as you can|"
    r"within \w+ hours))?\s+for\s+(?P<list>[^.;:]+)",
    re.I)
IS_A_NUMBER = re.compile(
    r"(?P<when>[^.;:]+?)\s+(?:is|are)\s+(?P<who>111|999|a&e)\b"
    r"(?P<quick>\s+(?:today|now|the same day|that day|straight away))?",
    re.I)


def _the_call_and_its_reason(said):
    found = []
    for m in CALLS_FOR.finditer(str(said or "")):
        sign = _no_hanging_end(m.group("list").strip(" ,;:-"))
        if not 2 <= len(sign.split()) <= 20:
            continue
        found.append((m.start(), sign, _the_person_for(m.group("who"), m.group("quick"))))
    for m in IS_A_NUMBER.finditer(str(said or "")):
        sign = _no_hanging_end(m.group("when").strip(" ,;:-"))
        if not 2 <= len(sign.split()) <= 20:
            continue
        found.append((m.start(), sign, _the_person_for(m.group("who"), m.group("quick"))))
    said_signs = []
    for _, sign, who in sorted(found):
        if any(sign in other for other in said_signs):
            continue
        said_signs = [s for s in said_signs if s not in sign]
        said_signs.append("%s (%s)" % (sign, who) if who else sign)
        if len(said_signs) == 2:
            break
    if not said_signs:
        return ""
    clause = "; ".join(said_signs)
    return clause[0].lower() + clause[1:] if clause[:1].isupper() else clause


_NOT_A_SIGN_WORD = frozenset((
    "about", "after", "again", "been", "before", "could", "doesnt", "from", "have", "into",
    "just", "like", "more", "much", "only", "over", "same", "should", "some", "than", "that",
    "their", "them", "then", "there", "these", "they", "thing", "this", "very", "want", "what",
    "when", "will", "with", "worried", "worry"))


def _the_sign_words(call):
    signs = re.sub(r"\([^)]*\)", " ", str(call or ""))
    return {w for w in re.findall(r"[a-z']+", signs.lower())
            if len(w) >= 3 and w not in _NOT_A_SIGN_WORD}


def _they_named_the_sign_themselves(call, memory):
    words = _the_sign_words(call)
    if not words:
        return False
    said = _flat(_the_line_behind(memory) or "")
    return bool(words & set(re.findall(r"[a-z']+", said)))


def _the_person_for(who, quick):
    trade = (who or "").strip().lower()
    if not trade:
        return ""
    trade = {"gp": "GP", "a&e": "A&E", "nhs": "NHS"}.get(trade, trade)
    if trade[0].isdigit() or trade in ("A&E", "NHS"):
        piece = trade
    elif trade in ("GP", "doctor", "practice nurse", "nurse", "surgery", "vet", "dentist",
                   "optician", "midwife", "physio", "physiotherapist"):
        piece = "your " + trade
    else:
        piece = "a " + trade
    hurry = re.sub(r"\s+", " ", str(quick or "")).strip(" ,")
    return (piece + " " + hurry).strip() if hurry else piece


A_PLAN = re.compile(
    r"\b(?:i'm|im|i am|we're|were|we are)\s+(?:going|off|flying|driving|sailing|heading|"
    r"travelling|traveling|moving|booking|booked|selling|buying|renting)\b"
    r"|\b(?:i|we)\s+(?:want|wanna|hope|plan|intend|need|'d like|would like)\s+to\b"
    r"|\b(?:i'm|im|i am|we're|were|we are)\s+(?:about to|planning to|thinking (?:of|about)|going to)\b")
A_HOW_TO_ASK = re.compile(
    r"\b(?:how|where|when)\s+(?:do|should|can|could|would|shall)\s+(?:i|we)\b"
    r"|\bhow\s+(?:do|can|would)\s+(?:i|we)\s+(?:stop|get|fix|clean|keep|make|put|sort|"
    r"deal|go|use|set|apply)\b")
A_DECISION_ASK = re.compile(
    r"\b(?:what|which)\s+(?:should|shall|do|would)\s+(?:i|we)\b"
    r"|\b(?:should|shall)\s+(?:i|we)\b")
SAID_YES = re.compile(
    r"\A\W*(?:yes|yep|yeah|yup|it does|that does|they can|it can|you can|both do)\b",
    re.IGNORECASE)


METHOD_DOUBT = re.compile(
    r"^(?:and |so |but |ok |okay |well )*(?:will|would|does|do|did|can|could) "
    r"(?:that|this|it) (?:actually |really |even |still )?"
    r"(?:work|help|be enough|do the job|do it)(?: then| though)?$")

METHOD_DOUBT = re.compile(
    r"^(?:and |so |but |ok |okay |well )*(?:will|would|does|do|did|can|could) "
    r"(?:that|this|it) (?:actually |really |even |still )?"
    r"(?:work|help|be enough|do the job|do it)(?: then| though)?$")
A_CHECK_ASK = re.compile(
    r"^(?:and |so |but |ok(?:ay)?[, ]+)?(?:do you think\s+)?"
    r"(?:will|would|does|do|did|should|shall|could|can|is|was)\s+(?:that|this|it|they|those)\s+"
    r"(?:actually |really |even )?(?:be\s+)?"
    r"(?:work|works|help|helps|fix it|fix that|do it|do the trick|do any good|"
    r"make a difference|sort it|be enough|enough|ok|okay|fine|right|worth it|worth doing|"
    r"worth a go|worth the money|the right thing|the right thing to do|the right way|"
    r"the done thing|the usual way)"
    r"(?: then| though| at all| for me| for us| for them| really)?\s*$"
    r"|^(?:and |so )?(?:shall|should|could|can|do)\s+i\s+(?:try|do|use|go with|give)\s+"
    r"(?:(?:that|this|it)\s+)?(?:a\s+)?(?:go|try|shot)"
    r"|^(?:and |so )?(?:shall|should|could|can|do)\s+i\s+(?:try|do|use|go with)\s+"
    r"(?:that|this|it)(?:\s+then)?\s*$"
    r"|^(?:and |so )?(?:do you think\s+)?(?:that|this|it)\s+(?:will|would|does|is|'s)?\s*"
    r"(?:be enough|enough|work|help|be worth it|be ok|be fine)\s*$"
    r"|^(?:and |so )?(?:is|was)\s+(?:that|this|it)\s+the\s+"
    r"(?:right|best|proper|usual|sensible|standard)\s+"
    r"(?:thing|way|way to do it|order|approach|method|call)(?:\s+to\s+do)?\s*$")

A_THINKING_ABOUT = re.compile(r"\bthinking (?:about|of)\b|\bwondering\b|\bconsidering\b|"
                              r"\bnot sure (?:if|whether)\b")

METHOD_OK_LINES = (
    "Nothing there is a problem - that is how I would do it too.",
    "That is how I would go about it, and there is nothing in it to worry about.",
    "Done that way, it needs no one else: that is the method I would use.",
)
CHECK_WORKS_LINES = (
    "It is the right thing to try first, and it works for most people. Give it a week or two and "
    "tell me how it goes.",
    "Yes - that is the standard way, so it is the one I would count on to start with. What changes "
    "after you have tried it is what tells us the next step.",
    "That is the usual way to go at it and it tends to do the job. If nothing has moved in a "
    "week, say so and we will go a step further.",
    "That is what I would do myself, so yes - it is worth a run. A fortnight of it is usually "
    "enough to know.",
)
CHECK_ONCE_LINES = (
    "That is the standard way of doing it and it works - tell me how it goes and we will take it "
    "from there.",
    "Yes, that is how it is done. Do it that way and tell me how you get on.",
    "That way of doing it is the right one, so go ahead - tell me if it does not do the trick.",
)
A_LENGTH_IN_THE_ANSWER = re.compile(
    r"(?<![a-z])(?:a|one|two|three|four)(?: or (?:more|so))? "
    r"(?:day|days|week|weeks|night|nights|hour|hours|fortnight|fortnights)(?![a-z])"
    r"|(?<![a-z])a few (?:days|weeks|nights)(?![a-z])|(?<![a-z])fortnight(?![a-z])")
CHECK_WATCH_LINES = (
    "That is the thing to try first, and most people do well on it. If it is no better in a week "
    "or two, that is when it wants someone to look rather than more of the same.",
    "Yes, that is worth doing first. If it stops helping, or it goes the wrong way, that is the "
    "point to get it looked at rather than wait.",
)
try:
    from .fallback_data import BODY_PARTS as _BODY_PARTS, SYMPTOM_WORDS as _SYMPTOM_WORDS
except Exception:
    _BODY_PARTS = _SYMPTOM_WORDS = frozenset()
_A_BODY_WORD = frozenset(_BODY_PARTS) | frozenset(_SYMPTOM_WORDS) | frozenset((
    "sick", "unwell", "ill", "nauseous", "sore", "soreness", "swollen", "swelling"))


def _about_a_body(*texts):
    for text in texts:
        words = re.findall(r"[a-z'-]+", str(text or "").lower())
        if any(word in _A_BODY_WORD for word in words):
            return True
    return False


CHECK_JOB_LINES = (
    "That is how I would go about it, and it is the right thing to do first. Tell me how you get "
    "on and I will pick it up from there.",
    "Yes, do it that way - it is the sensible order to do it in. Say how it goes.",
    "That is the right first move, and what comes back from it decides the next step.",
)
ASKS_FINE = re.compile(
    r"\b(?:ok|okay|alright|all right|fine|sensible|a good idea|worth it)\b", re.I)
ASKS_WRONG = re.compile(r"\b(?:bad|wrong|worrying|worry|a problem|dangerous|stupid)\b", re.I)
CHOICE_OK_LINES = (
    "Yes - that is a good call, and there is nothing in it I would change.",
    "Yes, go with it. It is a sensible thing to do and nothing in it is a problem.",
    "That one is fine as it stands. Nothing in it needs second-guessing.",
    "Nothing wrong with that choice. If it is the one that suits you, take it.",
    "Yes, I would. That is the pick I would make from where you are standing.",
)
NOTHING_WARNED_LINES = (
    "Nothing there is a warning sign - it is the ordinary thing to do. What would change it is "
    "the thing itself getting worse, or not settling.",
    "There is no warning in it: that is the everyday fix. What would matter is it getting worse "
    "or not shifting, so watch for that.",
    "Nobody needs to be called over it yet - it is the standard way to handle it. The point to "
    "get someone is if it does not settle.",
    "It is the usual handling of a thing like that rather than a warning about it. What would "
    "matter is it getting worse or not shifting.",
    "It is a job to do rather than a sign of how bad it is. Do that, and the thing to watch is it "
    "getting worse or not settling.",
)

MONEY_TROUBLE_LINES = (
    "Nothing here is broken - it is the money that does not stretch, and that is a thing letters "
    "and calls fix faster than waiting does. What is the first date you have to meet?",
    "It matters, and it is the sort of thing that shrinks as soon as somebody official is told "
    "about it. Ring the one the answer named before the next payment date, not after.",
    "That is a real hole in the month rather than a fault in you. Start with the one the answer "
    "named, and tell me what they say.",
    "It is a squeeze, not a sign that you have done something wrong, and it is the kind that gets "
    "smaller once it is written down. What is the number you cannot meet?",
)
MONEY_NOUN_WORDS = frozenset((
    "rent", "money", "bill", "bills", "debt", "debts", "owe", "owed", "arrears", "overdue",
    "loan", "loans", "credit", "card", "cards", "mortgage", "council", "tax", "fine", "fines",
    "energy", "electric", "electricity", "gas", "heating", "water", "payment", "payments",
    "payday", "wages", "pay", "savings", "overdraft", "afford"))
MONEY_NOT_MET = re.compile(
    r"\b(?:cant|can'?t|couldnt|couldn'?t|no|not|nothing|never|behind|missed|miss|late|overdue"
    r"|short|stuck|struggling|struggle|afford|owe|owed|debt|debts|arrears|skint|going down"
    r"|cut|reduced|behind on|fine|fines|fined|penalty|penalties|repossession|evicted|eviction"
    r"|bailiffs|declined|decline|refused|bounced|overdrawn|overdraft)\b")
NOT_MONEY_PAY = re.compile(r"\bpay(?:s|ing|ed)?\s+(?:attention|heed|respects?|tribute|homage|"
                           r"lip\s+service|a\s+visit|a\s+call|compliments)\b", re.I)
A_BODY_IN_THE_LINE = re.compile(
    r"\b(?:pain|ache|hurts?|hurting|sore|swollen|rash|bleeding|lump|cough|fever|temperature|"
    r"vomiting|sick|dizzy|breathless|doctor|gp|hospital|ambulance)\b", re.I)


_A_NUMBER = re.compile(r"\d")


def _a_doubt_about_money(memory):
    said = _flat(_last_person_line(memory) or "")
    if not said or len(said.split()) > 16:
        return ""
    words = set(_words(said))
    if not words & MONEY_NOUN_WORDS:
        return ""
    if not MONEY_NOT_MET.search(said):
        return ""
    if A_BODY_IN_THE_LINE.search(said):
        return ""
    if NOT_MONEY_PAY.search(said):
        return ""
    return said


MET_LINES = (
    "That answer put a timescale on watching it, and you are already past it. That is the point it "
    "meant, so get it looked at rather than sitting on it.",
    "The answer's own line on this is the timescale, and yours has been going on longer. That is "
    "the bit to act on, and it sounds like it is now.",
    "It said to watch it, and gave the timescale for doing that. You are past the timescale, so it "
    "is past watching - get it seen to.",
)
FIGURE_LINES = (
    "Same money every month adds up to a yearly figure, and that is the one to weigh: if a year of "
    "it still feels worth what you would otherwise do with the money, it is not too much.",
    "It is only ever a lot next to something. Put the year's total beside what else that money "
    "would do for you, and the answer usually picks itself.",
    "A monthly figure hides its size. Work out the year, then ask what you get for the year - to "
    "one budget it is loose change and to another it is the whole of the saving.",
)
A_FIGURE_ASK = re.compile(
    r"^(?:and |so )?is (?:that|this|it) "
    r"(?:a lot|a lot of money|too much|too much money|too expensive|expensive|cheap|good value|"
    r"about right|a fair price|that much|really that much)"
    r"(?: then| though| or not)?$", re.I)

MONEY_LINES = (
    "That is a figure to compare rather than a fault: the answer above gives the usual one, so put "
    "yours beside it, and if yours is the big one, that is what to change.",
    "Not bad so much as a number to check. The answer above quotes what is usual, and the gap "
    "between that and yours is the bit worth acting on.",
    "Nothing is broken there - it is your figure against the usual one the answer gave. If yours is "
    "the higher of the two, that is the thing to do something about.",
)
MONEY_WORD = frozenset((
    "bill", "bills", "invoice", "invoices", "rent", "owe", "owed", "owes", "owing", "debt",
    "debts", "tariff", "tariffs", "refund", "refunds", "fare", "fares", "price", "prices",
    "charge", "charges", "charged", "payment", "payments", "paying", "paid", "pay", "cost",
    "costs", "mortgage", "loan", "loans", "overdraft", "insurance", "premium", "premiums",
    "subscription", "subscriptions", "council", "tax", "vat", "fine", "fined", "money",
    "pennies", "quid", "pounds", "dollars", "euros", "pension", "salary", "wage", "wages",
    "budget", "savings", "saving",
))
A_FIGURE = re.compile(
    r"[\u00a3$\u20ac]\s?\d|"
    r"\b\d+(?:\.\d+)?\s*(?:p|quid|pounds?|dollars?|euros?|grand|k)\b|"
    r"\b\d[\d,.]*\s*(?:a|per|each)\s+(?:month|week|year|fortnight|day)\b",
    re.IGNORECASE)


A_COMPARISON = ("usual", "usually", "typical", "typically", "compare", "compares", "average",
                "on average", "benchmark")


def _is_a_comparison(said):
    if A_FIGURE.search(said or ""):
        return True
    return _first(said, A_COMPARISON) is not None


JUST_AGE = re.compile(
    r"\b(?:just|only)\b[^.!?]{0,24}\b(?:age|a phase|a stage|tiredness|the tiredness)\b",
    re.I)
AGE_LINES = (
    "Often it is age, and the thing that is not ordinary is a change: slower than before is usual, "
    "new or getting worse is the part to get looked at.",
    "Some of that is ordinary at that age. What is worth a word with the GP is a change - something "
    "that came on recently, or that keeps getting worse.",
    "Mostly age, as a rule, and it is the change that settles it rather than the thing itself: "
    "suddenly different, or worse each month, is the point to ask someone about it.",
)


def _a_figure_owed(line):
    if not line:
        return False
    words = [w.replace("'", "").lower() for w in re.findall(r"[A-Za-z\u00a3$\u20ac']+", line)]
    if any(word in BODY_WORD for word in words):
        return False
    if any(word in MONEY_WORD for word in words):
        return True
    return A_FIGURE.search(line) is not None


BODY_WORD = frozenset((
    "pain", "ache", "aches", "aching", "sick", "ill", "nauseous", "nausea", "dizzy", "headache",
    "temperature", "fever", "breathless", "throat", "chest", "stomach", "arm", "leg", "legs",
    "back", "knee", "hand", "foot", "feet", "head", "tooth", "toothache", "cough", "cold", "flu",
    "rash", "lump", "bleeding", "bleed", "blood", "itch", "itching", "swollen", "cramp",
    "period", "surgery", "pill", "pills", "tablet", "tablets", "dose",
))
SOMEONE_ELSE = frozenset((
    "son", "daughter", "child", "children", "kid", "kids", "baby", "mum", "mom", "dad", "mother",
    "father", "wife", "husband", "partner", "boyfriend", "girlfriend", "sister", "brother",
    "friend", "gran", "grandad", "grandma", "grandpa", "nan", "colleague", "boss", "dog", "cat",
))
FEELING_FAMILY = {
    "tired": "tired", "exhausted": "tired", "drained": "tired", "wiped": "tired",
    "knackered": "tired", "shattered": "tired", "worn": "tired", "burnt": "tired",
    "burnout": "tired",
    "anxious": "anxious", "anxiety": "anxious", "worried": "anxious", "stressed": "anxious",
    "stress": "anxious",
    "crying": "crying", "cry": "crying", "tearful": "crying",
    "low": "flat", "down": "flat", "flat": "flat", "miserable": "flat", "unhappy": "flat",
    "sad": "flat", "numb": "flat", "lonely": "flat", "hopeless": "flat",
    "overwhelmed": "heavy", "struggling": "heavy", "fed": "heavy", "useless": "heavy",
    "worthless": "heavy", "pointless": "heavy",
}
FEELING_DOUBT_LINES = {
    "tired": (
        "That is what running on empty feels like, and it is not a fault in you. Sleep and food "
        "come first - tiredness from a hard stretch lifts once those are back.",
        "Nothing about it is a sign something is broken. Tired like that is what carrying a lot "
        "does to a person, and it comes back up slowly rather than all at once.",
        "Being this worn out is ordinary for the run you have had, and it is allowed to be this "
        "heavy. If a couple of weeks pass with no better days in them, that is worth saying to a "
        "GP.",
    ),
    "anxious": (
        "That is worry doing its work, and it is not a sign something is wrong with you. It eases "
        "once the thing on your mind eases; until then, sleep and eating are the two worth "
        "guarding.",
        "Nothing about it is unusual, and nothing to be ashamed of. The part worth watching is "
        "whether it is there all day every day - weeks of that is worth saying to a GP.",
    ),
    "crying": (
        "That is tiredness and grief coming out of you, and it is not a weakness. It comes in "
        "waves, and the waves get further apart - they do not keep to a timetable.",
        "Nothing about crying like that is a sign something is broken. It usually eases within a "
        "few weeks of the thing that set it off; a month of it is worth saying to a GP.",
    ),
    "flat": (
        "That is what a low stretch does to a person, and it is not a fault in you. It lifts, "
        "slowly and not in a straight line - watch the good hours rather than the bad ones.",
        "Nothing there is a sign something is broken. Feeling flat is what a heavy few months "
        "looks like from the inside, and the way back is usually small and boring: sleep, food, "
        "one person who knows.",
        "That is ordinary for the run you have had, and it is allowed to be this heavy. If a "
        "couple of weeks go by with no better hours in them, that is the point to say it to a "
        "GP.",
    ),
    "heavy": (
        "That is a lot to carry, and it is not a measure of you. If a couple of weeks pass with "
        "no better hours in them, say it to a GP - that is what they are there for.",
        "Nothing there is a weakness. What you are describing is what too much for too long feels "
        "like, and the first thing that helps is usually a shorter list rather than more effort.",
    ),
}
ASKS_NORMAL = re.compile(
    r"\b(?:normal|abnormal|unusual|usual|typical|common|ordinary|standard)\b", re.I)
ASKS_OK = re.compile(r"\b(?:ok|okay|alright|all\s+right|acceptable|fine|safe)\b", re.I)
OK_LINES = (
    "Nothing in that sounded like a warning sign \u2014 so yes, it is fine. What would change it "
    "is the thing itself changing: getting worse, or not settling.",
    "Yes \u2014 that one is the ordinary kind. Watch it rather than worry about it: if it is still "
    "the same in a week or two, or it gets worse, get someone to look at it.",
    "Yes \u2014 the part you asked about is the harmless kind. What to keep an eye on is change "
    "rather than the thing itself.",
)
ORDINARY_NORMAL = (
    "Yes, that is the usual thing - what to keep an eye on is change rather than the thing "
    "itself.",
    "Yes, that is normal for most people. Watch it rather than worry about it: if it is the "
    "same in a week or two, or it gets worse, get someone to look at it.",
    "Yes, that is the ordinary thing, and it stays ordinary unless it changes. Getting worse, "
    "or not settling, is what would make it worth someone's look.",
)
CARE_NORMAL = (
    "Yes - common or not, that one is worth getting looked at properly. Say what you told me "
    "here when you do.",
    "Yes. That one needs a look rather than watching, and whether it is the usual thing is "
    "exactly what the look settles. Say what you told me here when you go.",
)
CARE_NORMAL_UNKNOWABLE = (
    "I could not call that usual or not from here, and it is one to have looked at: the check "
    "is cheap and it settles the question rather than the guessing.",
)
CARE_NOW = re.compile(
    r"\b(?:today|tonight|the same day|same day|straight away|right away|now|urgent|"
    r"within (?:a|one|two|three|\d+) (?:day|days|hour|hours))\b", re.I)
CARE_NOW_NORMAL = (
    "Don't sit on that one - it is a today thing, and whether it is the usual thing is what the "
    "look settles rather than the guessing.",
    "That wants seeing today. Whether it is the ordinary version or not is exactly what the "
    "visit is for, so ring and be seen.",
)
DO_NORMAL = (
    "That is the ordinary thing to do about it, and it is a job rather than a danger: do what I "
    "said and see whether it holds.",
    "Nothing in that is out of the ordinary - it is the everyday job, so do it and see whether "
    "it holds; if it comes back after that, get someone in.",
    "That is the usual way of dealing with it, and it is worth sorting rather than worrying "
    "about - do it and see whether it holds.",
)
CONDITION_NORMAL = (
    "Ordinary on its own, yes - and it stops being usual if {when}. That is the point to act on.",
    "That is the usual case on its own, and it becomes something else if {when}.",
    "Usual up to a point: what would make it something to act on is if {when}.",
)
NOTHING_WARNED_NORMAL = (
    "Yes, that is how it is normally handled. What would matter is a change in it.",
    "Yes, that is the ordinary job, and what would send you to someone is a change in it.",
    "Yes, ordinary - that is the everyday fix for it, and the thing to watch is it getting "
    "worse or not shifting.",
)
YES_LINES = (
    "Yes — it is worth acting on rather than sitting on. Asking costs very little and it stops "
    "the guessing.",
    "Yes, that one wants a proper look rather than watching it. Get it looked at properly, and "
    "say what you told me here when you do.",
    "Yes. Get it seen to — not an emergency, but not something to sit on either.",
)
A_THING_THEY_OWN = re.compile(
    r"\b(?:boilers?|radiators?|central heating|thermostat|washing machine|washer dryer|"
    r"tumble dryer|dishwashers?|fridge|freezer|fridge freezer|ovens?|hob|cooker|microwave|"
    r"kettles?|toaster|hoover|vacuum|lawnmower|mower|strimmer|pressure washer|shower tray|"
    r"showers?|taps?|toilets?|sinks?|drains?|plughole|gutters?|roof|fencing|fence|decking|"
    r"doors?|windows?|locks?|sockets?|fuse board|consumer unit|lights?|"
    r"cars?|vans?|bikes?|bicycles?|motorbike|scooter|tyres?|brakes?|clutch|exhaust|engine|"
    r"laptops?|computers?|pcs?|printers?|phones?|tablets?|monitors?)\b", re.I)
A_BODY_WORD = re.compile(
    r"\b(?:skin|rash|itch|itching|eyes?|ears?|throat|chest|stomach|belly|knee|knees|joint|"
    r"joints|hips?|shoulders?|neck|foot|feet|hands?|arms?|legs?|tooth|teeth|gums?|breath|"
    r"back(?! (?:door|doors|garden|gate|wall|bed|room|bit|passage))|"
    r"breathing|breathless|cough|poo|wee|blood|fever|temperature|hearing|sight|head|"
    r"headaches?|migraine)\b", re.I)
THING_ORDINARY = (
    "It is the everyday thing rather than a fault, and the job I described is what settles it. If "
    "it is still doing it after that, or it comes back, that is when it wants somebody who does "
    "this for a living.",
    "Nothing in that is a fault on its own: it is the ordinary thing with a job attached. Do the "
    "job, and if the noise or the mark is still there afterwards, get somebody in.",
    "That is the usual reason for it, and the fix I gave is the check. Do that first - if it "
    "holds, it was the everyday thing, and if it does not, that is a call to somebody with the "
    "trade.",
)
THING_CALL = (
    "Yes - that one is for somebody who does this for a living rather than a watch-and-see. "
    "Describe it as you did here when you book them in, and hold off using it until they have "
    "looked.",
    "Yes, get that looked at properly. It is a call to a trade rather than something to sit on, "
    "and the sooner they see it the less it usually costs.",
    "Yes. That is a job for somebody with the right tools, not a wait-and-see.",
)
BACKSTOP_LINES = (
    "Not bad, no. What would make it matter is how long it has been going on and what it is "
    "costing you — how do those two look?",
    "I wouldn't call it bad. It is worth a proper look rather than a shrug, though: what does it "
    "take out of your week?",
    "Not a fault, and nothing to be ashamed of. The question worth asking is whether it has a "
    "hold on your days rather than whether it is bad.",
)
PEOPLE_CARE = ("gp", "doctor", "nurse", "midwife", "health visitor", "physio", "therapist",
               "pharmacist", "optician", "dentist", "vet", "111", "referral", "hospital",
               "a&e", "urgent care", "out of hours", "specialist", "clinic")
FLOOR_LINES = (
    "How long has it been going on, and what does it cost you day to day?",
    "How long has it been like that, and is it getting in the way of your week?",
    "What would you like to do about it, and how long has it been like that?",
)
NEUTRAL_ASK_LINES = (
    "Say a bit more: how long has it been like that, and what does it cost you day to day?",
    "How long has it been going on, and what would you like to do about it?",
    "Tell me more and I will help you think it through: how long, and how is it affecting you?",
)
A_PLAN_DOUBT_LINES = (
    "Nothing in that sounds wrong: it is a plan rather than a fault to check. Which part of it are "
    "you unsure about?",
    "Say which part you are unsure about and we can weigh it up together.",
    "That is yours to decide rather than something to worry about. What is the bit you keep going "
    "over?",
)
SOON_LINES = (
    "Yes, that wants looking at - the answer named who, so book it rather than wait for it to "
    "settle.",
    "It is worth having it seen to, and that answer already said by whom. Get that booked, and "
    "say how long it has been going on when you do.",
    "Not an emergency by the sound of it, but not something to leave either: the person named in "
    "that answer is the one to see.",
)
HELPED_LINES = (
    "Then it is doing its job - keep it up and give it a few more days before you judge it.",
    "Good: that is the thing that worked, so stay with it. The point to get someone to look is if "
    "it stops helping.",
    "That is the answer then. Keep doing it, and tell me if it stops working.",
)
WORRIED_ASK = re.compile(
    r"^(?:and |so )?should i (?:be )?(?:worried|worry|worrying|concerned|see someone|see a doctor"
    r"|do anything|do something|get it checked|be checked|call someone|ring someone)(?: then"
    r"| though)?$")
HELPED = re.compile(
    r"\b(?:(?:that|it|this) (?:has )?(?:helped|worked|did the trick|did help|is helping"
    r"|is working)|both worked|they worked|it worked out|(?:much )?better (?:now|today)"
    r"|(?:its|it is) (?:helping|working)|on the mend)\b")
YES_SAID_LINES = (
    "Yes - that is why the call is the thing to do now rather than something to wait on. Do that "
    "first, and tell me what they say.",
    "Yes it is, and that is what the call is for. Make it now rather than tomorrow, and we can go "
    "through the rest once you have.",
    "Yes - ringing is not an overreaction here, it is the whole point of it. Do that first and "
    "come back to me after.",
    "Yes. Somebody needs to hear this today rather than next week, so make the call and then tell "
    "me what they say.",
)

THROW_AWAY = re.compile(
    r"\b(?:bin\s+(?:it|them|that)|throw\s+(?:it|them|that)\s+(?:away|out)|"
    r"chuck\s+(?:it|them|that)(?!\s+(?:\w+\s+){0,2}(?:in|on|into|with|to)\b)|"
    r"(?:get|getting)\s+rid\s+of\s+(?:it|them|that))\b", re.I)
NOT_TOLD_TO = re.compile(r"(?:\bdon'?t|\bdo not|\bnever|\bnot|\brather than|\binstead of|\bbefore you)\s*$", re.I)
ONE_OPTION = re.compile(r"\b(?:or|and|rather than|instead of)\s*$", re.I)
TESTING = re.compile(r"^[\s\"'(\u2018\u201c]*(?:if|unless|once|whenever|when|any ?time|should|whether)\b", re.I)
THROW_AWAY_LINES = (
    "{Action} \u2014 it is not worth the risk, and it is not a close call.",
    "Yes, really. {Action}. This is the one where guessing costs the most.",
    "{Action}, and do not talk yourself out of it: nothing you can see or smell makes it safe.",
)
TEST_LINES = (
    "{Action} once it has turned - that is the whole test, and I would not taste it to check.",
    "You do not need me to judge it. {Action} once it has turned, and that is the whole test.",
    "{Action} if it has actually turned. The test is the answer, and the thing itself is the judge.",
)
STATED_NO = re.compile(
    r"\bthere (?:is|are) no safe (?:number|amount|level|dose|limit|quantity|way)\b"
    r"|\bno amount of .{1,40} (?:is|was) safe\b"
    r"|\bnothing about .{1,40} (?:is|makes it) safe\b"
    r"|\bis not safe to (?:eat|drink|drive|take|use|give|leave|keep)\b"
    r"|\bare not safe to (?:eat|drink|take|use|give)\b"
    r"|\bnone of (?:it|them|these) is safe\b"
    r"|\byou cannot make .{1,40} safe\b",
    re.I)
NO_STATED_LINES = (
    "No \u2014 that is the answer's own line: {no} There is nothing in it for you to weigh up.",
    "That one is a no, and the answer said it plainly: {no} What to do instead is in the rest of "
    "what I said.",
    "No. {no} That is the whole of it, so it is not a thing for you to judge.",
    "No, and not a close call. {no}",
)
ENOUGH_ASK = re.compile(
    r"^(?:and |so )?(?:is|was|are|were) (?:that|this|it|all of that|all that)"
    r"(?: (?:really|actually|about|roughly))? enough(?: then| though)?$", re.I)
STATED_ENOUGH = re.compile(
    r"\bis (?:definitely |probably |easily |more than |plenty )?enough\b"
    r"|\bis plenty\b|\bmore than enough\b|\bthat will do\b|\bthat does it\b", re.I)
ENOUGH_STATED_LINES = (
    "Yes \u2014 {yes} That is the amount, and the rest of what I said is what makes it work.",
    "Yes: {yes} Nothing in the answer asks for more than that.",
    "It covers it as it stands. {yes}",
    "Yes, on the answer's own figures. {yes}",
)
STOP_DOING = ("stop driving", "don't drive", "dont drive", "don't eat", "dont eat", "don't use it",
              "dont use it", "don't touch", "dont touch", "don't drink", "dont drink",
              "leave the building", "get everyone away", "stop if it is safe")
DANGER = ("dangerous", "toxic", "poisonous", "poisoning", "can die", "could die", "may die",
          "can kill", "could kill", "fatal", "harmful", "not safe", "unsafe", "an emergency",
          "never give", "never use", "never take", "never leave")
NEGATED = re.compile(r"(?:\bnot|\bno|n't|\bnever|\bnon)[ -]\w*[ -]?$")
AGAIN = (
    "Same answer as a moment ago: nothing in what I said was a warning sign. It's the change "
    "to watch for, not the thing itself.",
    "Still no. If it would help, tell me what's actually worrying you about it and I'll be "
    "straight with you.",
)
_FILLER = (r"(?:(?:and|so|ok|okay|but|well|right|honestly|actually|basically|literally|simply|"
           r"truly|really|just) )")
_LEAD_FILLER = _FILLER + r"*"
_FILL = _FILLER + r"?"
STEP = re.compile(
    r"^(?:" + _LEAD_FILLER + r")"
    r"(?:(?:what|which) " + _FILL + r"(?:should|do|can) " + _FILL
    + r"i " + _FILL + r"do(?: now| next| first| about it)?"
    r"(?: then)?$"
    r"|what " + _FILL + r"now$"
    r"|what " + _FILL + r"(?:do|should) " + _FILL + r"i " + _FILL
    + r"(?:try|do) " + _FILL + r"(?:first|next)$"
    r"|how " + _FILL + r"do " + _FILL + r"i " + _FILL
    + r"(?:fix|sort|deal with) " + _FILL + r"(?:it|that|this)$"
    r"|what " + _FILL + r"(?:should|do|can|could) " + _FILL + r"i " + _FILL
    + r"(?:put|use|apply|try) " + _FILL + r"(?:on|to|for) " + _FILL
    + r"(?:it|that|this)(?: then)?$)"
)
SPEAK_VERBS = (r"(?:say|mention|bring (?:it|that|this|them) up|raise|tell|ask|text|call|"
               r"ring|email|write|speak|talk)")
SPEAK_UP = re.compile(
    r"^(?:and |so )?(?:(?:do you think|do you reckon|d'you reckon) )?"
    r"(?:should|shall|ought) i " + SPEAK_VERBS + r"\b"
    r"|^(?:and |so )?(?:do you think|do you reckon|d'you reckon) i should " + SPEAK_VERBS + r"\b")
EMERGENCY_CALL = re.compile(
    r"\b(?:ring|call|dial|phone|contact)\b[^.!?]{0,60}?\b(?:999|911|112)\b", re.I)
SEE = re.compile(
    r"^(?:and |so )?(?:should|do) i (?:need to )?(?:see|call|ring|go to) (?:a |the |my )?"
    r"(?:someone|somebody|doctor|gp|vet|dentist|engineer|plumber|doctor about it)(?: then)?$"
    r"|^(?:and |so )?do i need (?:to see )?(?:someone|a doctor|the doctor|the vet)(?: then)?$"
    r"|^(?:and |so )?is it worth (?:seeing|going to|ringing) (?:someone|a doctor|the vet)"
    r"(?: then)?$"
)
HOW_TO = re.compile(
    r"^(?:and |so |ok |okay |well )?how (?:do|should|can|would|might|will) i "
    r"(?P<doing>[a-z]+)"
    r"(?P<obj>(?: (?:[a-z]+ ){0,2}(?:it|that|this|them)"
    r"(?: (?:on (?:friday|monday|tuesday|wednesday|thursday|saturday|sunday)|then|now|first|"
    r"out|off|down|up|again|properly|safely))?)?)$")
DOING_WITH_NO_OBJECT = frozenset("""prepare practise practice rehearse revise study train
warm stretch""".split())
KNOWING_DOING = frozenset("""know tell check spot find see say guess recognise recognize""".split())
TIPS_AGAIN = re.compile(
    r"^(?:and |so |ok |okay |well )?(?:(?:any|some|got any|got some|need some|need any|"
    r"want some|more|any more|another|a few|any other)\s+)?"
    r"(?:tips?|advice|pointers?|tricks?|hints?|ideas?|suggestions?|thoughts?)"
    r"(?: (?:at all|then|please|too|now|really|anyway))*$"
)
ONE_THING_ADVERB = ("even", "actually", "really", "just", "possibly", "maybe", "instead",
                    "honestly", "normally")
_ONE_THING_ADVERB = r"(?:(?:%s) )?" % "|".join(ONE_THING_ADVERB)
A_HOW_ASK = re.compile(
    r"^(?:and |so |ok |okay |well )?(?:what|whats|what is|which is|whichs) the "
    r"(?:safest|best|quickest|fastest|easiest|simplest|surest|most reliable|right|"
    r"proper|correct) (?:way|method|bet|option|approach|route)"
    r"(?: (?:to (?:do|fix|sort|handle|treat|clean|stop|get rid of|deal with|go about) "
    r"(?:it|that|this)|to (?:start|begin|try|go about)(?: (?:it|that|this))?"
    r"|of doing (?:it|that|this)|of getting rid of (?:it|that|this)"
    r"|for (?:it|that|this)|here|then|now|at all|please))?$")
ONE_THING = re.compile(
    r"^(?:and |so |ok |okay |well |but )?(?:"
    r"just (?:one|the one|the first|1) (?:thing|step|move|bit)(?: to (?:start|begin|try|do)"
    r"(?: with)?(?: first)?)?"
    r"|(?:one|the one|the first) (?:thing|step|move) (?:to (?:start|begin|try|do)(?: with)?"
    r"(?: first)?|first)"
    r"|(?:what|which) (?:is|would be|should be) the (?:one|first) thing(?: to do)?"
    r"|(?:where|how) (?:do|should) i " + _ONE_THING_ADVERB + r"(?:start|begin)"
    r"(?: with it| with that| here| off)?"
    r"|(?:what|where) do i " + _ONE_THING_ADVERB + r"(?:start|begin)(?: with it| with that)?"
    r")(?: (?:then|please|though|now|really))*$"
)
AFTER = re.compile("[:;] | - | — | – ")
SPLIT = re.compile("([:;] | - | — | – )")
THEN_OPEN = re.compile(r"^(?:and\s+)?then[,]?\s+", re.I)
REFER = re.compile(
    r"\b(?:see|ring|call|contact) (?:a |your |the )?(?:gp|doctor|vet|dentist|nurse|someone|"
    r"surgery|physio|physiotherapist|pharmacist|optician|midwife|111|999|engineer|plumber)"
    r"|\b(?:have|get) (?:a |your |the )?(?:gp|doctor|vet|dentist|nurse|physio|physiotherapist|"
    r"pharmacist|optician|midwife)\s+(?:to\s+)?(?:look|check|see|take a look)\b"
    r"|\bask (?:a |your |the )?(?:gp|doctor|vet|dentist|nurse|physio|physiotherapist|"
    r"pharmacist|optician|midwife)\b"
    r"|\b(?:see|ring|call|contact) (?:a |your |the )?(?:(?!and\b|or\b|to\b|for\b|of\b|in\b|on\b"
    r"|at\b|from\b|with\b|that\b|if\b|when\b|it\b)[a-z-]+ ){0,3}(?:gp|doctor|vet|dentist|"
    r"nurse|someone|physio|physiotherapist|pharmacist|optician|midwife|111|999|engineer|plumber)"
    r"|get (?:it|that|this|him|her|them|someone|somebody)? ?(?:looked at|checked|seen)"
    r"|a&e|urgent care|out of hours"
    r"|\b(?:vet|doctor|gp|dentist) (?:visit|job|matter|appointment)\b"
    r"|\btake (?:it|this|that|them) (?:to|along to|back to|in to) (?:a |your |the )?"
    r"(?:gp|doctor|pharmacist|nurse|dentist|vet|physio|physiotherapist|optician|midwife)\b"
    r"|\bnot a wait-and-see\b|worth getting (?:it |them )?checked",
    re.I,
)
NAMES_A_CLINICIAN = re.compile(
    r"\b(?:gps?|doctors?|nurse|practice nurse|midwife|health visitor|pharmacist|vets?|"
    r"dentist|a&e|minor injuries|walk-in (?:centre|clinic)|urgent care|out of hours|111|999|nhs)\b",
    re.I,
)
DECLARATIVE_REFERRAL = re.compile(
    r"\b(?:vet|doctor|gp|dentist) (?:visit|job|matter|appointment)\b|\bnot a wait-and-see\b"
    r"|\b(?:checked|looked at|assessed|seen) by (?:a |your |the )?(?:gp|doctor|nurse|practice"
    r" nurse|physio|physiotherapist|dentist|vet|pharmacist|optician|midwife)\b"
    r"|\bneeds? (?:a |your |the )?(?:gp|doctor|nurse|vet|dentist|physio|pharmacist|optician)\b"
    r"|\bneeds? (?:to be )?(?:seen|checked|looked at)\b"
    r"|\bworth (?:a |an |your |the )?(?:gp|doctor|doctor's|vet|dentist|optician|pharmacist"
    r"|physio\w*|nurse|midwife|health visitor)\b"
    r"|\b(?:gp|doctor's|doctor|vet|dentist|optician|physio\w*|midwife|health visitor)"
    r" appointment\b"
    r"|\b(?:nhs 111|111 line|out of hours service|urgent treatment centre|health visitor)\b",
    re.I,
)
WHEN = frozenset("""about around roughly per couple once twice three four five six seven two
a an every each daily nightly
morning afternoon evening night day week month year hour minute second time times""".split())
HANGING = frozenset((
    "with", "in", "of", "to", "on", "for", "at", "and", "or", "the", "a", "an", "my", "your",
    "its", "it's", "from", "by", "as", "than", "but", "if", "so", "into", "about",
    "between", "among", "through", "under", "over", "without", "within", "against", "across",
    "behind", "beyond", "towards", "toward", "upon", "except", "despite", "unless", "until",
    "whether", "onto", "than",
))
IMPERATIVES = frozenset((
    "keep", "ease", "ice", "rest", "bleed", "put", "take", "stop", "swap", "use", "ring",
    "call", "check", "top", "wear", "cut", "leave", "unplug", "turn", "sit", "drink", "wrap",
    "raise", "prop", "wash", "rinse", "soak", "cover", "avoid", "try", "start", "do", "give",
    "pick", "choose", "compare", "buy", "order", "fill", "print", "ask", "tell", "move", "set",
    "open", "close", "save", "read", "write", "clean", "clear", "make", "budget", "shop",
    "cool", "reheat", "freeze", "drain", "store", "boil", "bake", "chill",
    "go", "get", "book", "phone", "add", "apply", "hold", "heat", "cook", "remove", "dig",
    "plant", "water", "measure", "log", "email", "text", "fill", "mix", "line", "air",
    "bathe", "blot", "dab", "sponge", "rub", "wipe", "dry", "pull", "empty", "hang", "lay",
    "press", "find", "look", "run", "work", "change", "split", "pat", "stir", "track",
    "iron", "serve", "roll", "fix", "follow", "build", "replace", "send", "stand", "draw",
    "rehearse", "practise", "practice", "recite",
    "tighten", "blend", "stretch", "skip", "practise", "watch", "learn", "offer", "report",
    "stay", "seal", "trim", "prime", "screw", "weigh", "scrape", "simmer", "roast",
    "grill", "shred", "mash", "chop", "begin", "feed", "place", "switch", "fit", "test",
    "brush", "scrub", "pour", "grate", "slice", "spray", "prune", "repot", "balance", "let",
    "be", "eat",
    "scour", "flush", "vacuum", "hoover", "peel", "fold", "loosen",
    "walk", "tuck", "settle", "swaddle",
    "treat", "pack", "pay", "photograph", "aim", "melt", "halve", "agree", "shut",
    "sort", "repair", "label", "install", "cancel", "plug", "restart", "reset", "scan", "reply",
    "spend", "bin", "tidy", "sell", "throw", "push", "answer", "mend", "rent",
    "bring",
    "separate",
))
LIST_STEP_LINES = (
    "Start with the first thing on that list: {step}.",
    "The first one on that list: {step}.",
)
STEP_LINES = (
    "{Step} first.",
    "{Step} - that is the first move.",
    "{Step}, before anything else.",
)
STEP_DETAIL_LINES = (
    "{Step}. That is the first move.",
    "{Step}. Start there.",
    "{Step}. Do that before anything else.",
)
FIRST_ITSELF = re.compile(r"\b(?:start|begin|first)\b", re.I)
STEP_ALREADY_FIRST_LINES = (
    "{Step}. Nothing else before it.",
    "{Step}, and only that to begin with.",
    "{Step}, in that order.",
)
SUBJECT_OPEN = re.compile(r"^(?:they|it|it's|its|he|he's|she|she's|this|that|that's|these|those"
                          r"|there|there's|we|we're)\b", re.I)
EXPLANATION_WORDS = 5


def _is_an_explanation(sentence):
    text = sentence.strip()
    if not SUBJECT_OPEN.match(text):
        return False
    head = re.split(r":|,|;| - | \u2014 ", text, 1)[0]
    return len(head.split()) > EXPLANATION_WORDS


STEP_ONE_LINES = (
    "{Step}, and take it from there.",
    "{Step}. That is the one to do today; the rest is waiting to see whether it shifts.",
    "{Step} - start with that, and tell me how it goes.",
)
STEP_KEPT_LINES = (
    "Still the same move, and nothing to add to it: it is small, and it is the one that counts today.",
    "That step stands - it is a thing to keep doing rather than a second thing to start.",
    "Nothing new from me on it. Do the first thing as I said it, and tell me how it goes.",
)
ALSO_LINES = (
    "There is more in what I said: {other}",
    "One more from that answer: {other}",
    "The other half of it: {other}",
)
ASKS_THEM = re.compile(r"\b(?:tell me|let me know|say which|what have you|how ready)\b", re.I)
ONE_TURN_LINES = (
    "Just this: {Step}.",
    "The one thing: {Step}.",
    "Start with this: {Step}.",
    "Just the one, then: {Step}.",
)
ONE_TURN_PLAIN_LINES = (
    "{Step}. That is the one I would start with.",
    "{Step}. Just that one, and the rest can wait.",
    "{Step} - the one to do today, and the rest will keep.",
)
ALL_OF_IT_LINES = (
    "That answer is the whole of what I have on it, and there is no single first move in it: tell "
    "me which bit you want and I will take that one further.",
    "Everything I know on that one is in the answer above, and none of it is one job to start "
    "with. Say which part matters most and I will come at it from there.",
)
QUESTION_BACK_LINES = (
    "Nothing to do on my side, honestly - whatever comes to mind about it first is the useful bit.",
    "No steps from me yet. Take the question in your own time, and start with whatever is loudest.",
    "There is nothing to do about it until we have looked at it - so start there, in your own time.",
)
ASKED_FIRST_LINES = (
    "I can be specific if you tell me this much: {q}? Even a line is enough.",
    "One thing and I can be concrete: {q}?",
    "Tell me this and I can say something useful: {q}?",
)
OFFER_TAKEN_LINES = (
    "Yes - the one thing that is bothering you most, in your own words, and I will start there.",
    "Then give me the thing itself. One sentence is enough, and I will pick the first step from it.",
    "Go on then: name the one part that is worst, and we will take it from there.",
)
SEE_NOW_LINES = (
    "See someone if {when}. Before that, what I said above is the plan.",
    "Not yet, unless {when}. If that happens, get it looked at rather than waiting.",
    "The point where it wants a person is if {when}. Until then, what I said above is the plan.",
)
SEE_ANYWAY_LINES = (
    "That one is a visit rather than a wait, so yes - get it looked at.",
    "Yes. Ring them rather than waiting on it, and say what you have noticed so far.",
    "Nothing to sit on there: that is one to get looked at.",
)
SEE_STATED_LINES = (
    "Nothing there needs anyone today. That changes with {when}.",
    "Not yet. The point where it wants a person: {when}. Short of that, what I said above is the "
    "plan.",
    "What would change that: {when}. Until then, what I said above is the plan.",
)
NOTHING_LINES = (
    "Nothing you need to do yet - it matters if {when}.",
    "Nothing to do for now. That changes if {when}.",
    "No steps to take: what I said only changes if {when}.",
)
SEE_NONE_LINES = (
    "Nothing in what I said needs anyone today. If it has not settled in a week or so, that "
    "changes.",
    "Not yet. Give what I described a few days; if it is no better, that is when to ask.",
)
POOLS = (NO_LINES, DO_LINES, YES_LINES)


OWN_LINES = tuple(
    line for pool in (NO_LINES, DO_LINES, YES_LINES, STEP_LINES, STEP_DETAIL_LINES,
                      STEP_ONE_LINES, STEP_ALREADY_FIRST_LINES, STEP_KEPT_LINES, SEE_NOW_LINES,
                      SEE_ANYWAY_LINES, SEE_STATED_LINES, SEE_NONE_LINES, NOTHING_LINES,
                      CONDITION_LINES, NOTHING_WARNED_LINES, ORDINARY_NORMAL, CARE_NORMAL,
                      CARE_NORMAL_UNKNOWABLE, CARE_NOW_NORMAL, DO_NORMAL,
                      NOTHING_WARNED_NORMAL)
    for line in pool
)


def _own_pattern(line):
    parts = re.split(r"\{[A-Za-z]+\}", line)
    return ".+?".join(re.escape(part) for part in parts)


OWN_PATTERN = re.compile("|".join(_own_pattern(line) for line in OWN_LINES),
                        re.IGNORECASE)


_ACK_PATTERN = None
ECHO_WORDS = 14


def takes_a_fact_back(said):
    global _ACK_PATTERN
    if _ACK_PATTERN is None:
        from ..memory import ack
        frames = ack.FRAMES + ack.HABIT_TAIL + ack.GOING_TAIL + ack.EXPLAIN_TAIL
        _ACK_PATTERN = re.compile("|".join(_own_pattern(line) for line in frames), re.IGNORECASE)
    text = " ".join(str(said or "").split())
    if not text or not _ACK_PATTERN.match(text):
        return False
    words = re.findall(r"[a-z']+", text.lower())
    return len(words) <= ECHO_WORDS and not any(word in IMPERATIVES for word in words)


def _say(pool, memory, flat, **gaps):
    rendered = list(pool)
    for name, value in gaps.items():
        for template, gap in ((name, "{%s}" % name),
                              (name[:1].upper() + name[1:], "{%s}" % (name[:1].upper() + name[1:]))):
            filled = value if gap == "{%s}" % name else value[:1].upper() + value[1:]
            rendered = [line.replace(gap, filled) for line in rendered]
    return pick(rendered, memory, flat)


def _a_report_line(said):
    try:
        from .fallback import is_a_report_reply
    except Exception:
        return False
    return bool(is_a_report_reply(said))


def _flat(text):
    return " ".join(str(text or "").lower().replace("\u2019", "'").split())


READABLE = frozenset(("answers", "chat", "trouble", "fallback", "greeting"))
UNREADABLE = frozenset(("safety", "urgent", "loss", "grief"))


COMPOSED = frozenset(("greeting", "fallback"))
RULED_BY_THE_COMPOSER = (
    ORDINARY_NORMAL, CARE_NORMAL, CARE_NORMAL_UNKNOWABLE, CARE_NOW_NORMAL, DO_NORMAL,
    CONDITION_NORMAL, NOTHING_WARNED_NORMAL, NO_LINES, BOTH_LINES, DO_LINES, CONDITION_LINES,
    MET_LINES, MET_CONDITION_LINES, METHOD_OK_LINES, YES_LINES, BACKSTOP_LINES, SOON_LINES,
    HELPED_LINES, MONEY_TROUBLE_LINES,
)


def rules_on_the_doubt(said):
    said = str(said or "").strip()
    if not said:
        return False
    head = said[:40].lower()
    return any(head == line[:40].lower() for pool in RULED_BY_THE_COMPOSER for line in pool)


RUN = 4
_WORD = re.compile(r"[a-z0-9']+")


_AFTER_A_NOUN = frozenset("at in on from of for to with by near under behind over into about".split())


def opens_on_a_job(reply):
    flat = _flat(reply)
    if not flat:
        return False
    head = re.split(r"[:;.!?]", flat, 1)[0].strip(" ,-")
    words = _WORD.findall(head)
    if not words or words[0] not in IMPERATIVES:
        return False
    if len(words) > 1 and words[1] in ("me", "us"):
        return False
    return len(words) == 1 or words[1] not in _AFTER_A_NOUN


def carries_the_answer(reply, memory):
    if _kept_step(reply):
        return True
    said = _WORD.findall(_flat(_last_reply(memory)))
    words = _WORD.findall(_flat(reply))
    if len(said) < RUN or len(words) < RUN:
        return False
    runs = {" ".join(said[i:i + RUN]) for i in range(len(said) - RUN + 1)}
    return any(" ".join(words[i:i + RUN]) in runs for i in range(len(words) - RUN + 1))

PUNT_START = re.compile(r"^(?:got it|noted|ok(?:ay)?|alright|all right|right|fair enough|"
                        r"i see|makes sense|understood|sure|cool)\b", re.I)
PUNT_OFFER = re.compile(r"\b(?:is there anything|anything else|what else|let me know|"
                        r"anything (?:i|we) can do)\b", re.I)


PUNT_CHAT = re.compile(r"\b(?:good luck|sounds good|fair enough|nice one|lovely|alright then|"
                      r"ok then|well then|makes sense|hope (?:it|that) (?:goes|works))\b", re.I)


def _a_punt(last):
    module = last.get("module")
    if module not in ("greeting", "fallback", "chat"):
        return False
    said = _flat(last.get("bot"))
    if not said or not PUNT_START.match(said):
        return False
    if module == "chat" and not PUNT_CHAT.search(said):
        return False
    if PUNT_OFFER.search(said):
        return True
    if "?" in said:
        return False
    return len(said.split()) <= 8


def _skip_the_derived(turns, memory):
    if not isinstance(memory, dict) or len(turns) <= 1:
        return turns
    if memory.get("frequency_reply") or healing.derived(memory):
        return turns[:-1]
    return turns


def answers_the_ask(clean, memory):
    if _last_module(memory, past_the_nod=True) != "answers":
        return False
    return reply_for(clean, memory) is not None


def _the_news_just_before(memory):
    if not isinstance(memory, dict):
        return False
    try:
        from .badnews import reads_as_bad_news
    except Exception:
        return False
    turns = memory.get("turns") or []
    turn = turns[-1] if turns and isinstance(turns[-1], dict) else {}
    said = " ".join(str(turn.get("user") or "").lower().split())
    return bool(said) and reads_as_bad_news(said)


def _last_reply(memory, past_the_nod=False, past_the_verdict=False):

    punt_line = ""
    turns = memory.get("turns") if isinstance(memory, dict) else None
    if not isinstance(turns, list) or not turns:
        return ""
    turns = _skip_the_derived(turns, memory)
    for index in range(len(turns) - 1, -1, -1):
        last = turns[index]
        before = turns[index - 1] if index else None
        if not isinstance(last, dict):
            return punt_line
        module = last.get("module")
        said = str(last.get("bot") or "")
        if module in UNREADABLE:
            return punt_line
        if module == "chat" and OWN_PATTERN.search(_flat(said)):
            continue
        if _a_report_line(said):
            continue
        if module in COMPOSED and why.is_a_reason_line(said):
            continue
        if module in READABLE and takes_a_fact_back(said):
            continue
        if A_STEP_ASK.match(_flat(last.get("user"))) and last.get("module") != "answers":
            continue
        if _a_punt(last):
            if not past_the_nod or punt_line:
                return said if not past_the_nod else punt_line
            punt_line = said
            continue
        if past_the_verdict and _only_a_verdict(last.get("user")):
            continue
        if _is_an_echo(last):
            continue
        if before is not None and _is_a_recap(last, before):
            continue
        if module in READABLE:
            if punt_line and module != "answers":
                return punt_line
            return said
        return punt_line
    return punt_line


ECHO_FILLER = frozenset("""
a an the and or so but then too that thats that's this it its it's is are was were be been
i we you he she they his her their our your yours mine theirs
my me us them him got get note noted right ok okay
sure yes yeah no not ah oh mm good fine well still just only also very really quite
know sounds thanks hope glad
have has had do did does for to of in on at with about from by as if
one two three four five six seven eight nine ten eleven twelve half twice both all some
""".split())


def _words(text):
    return [word.replace("'", "") for word in re.findall(r"[a-z0-9']+", str(text or "").lower())]


def _is_an_echo(turn):
    said = _words(turn.get("bot"))
    theirs = set(_words(turn.get("user")))
    if not said or not theirs or len(said) > 12:
        return False
    return all(word in ECHO_FILLER or word in theirs for word in said)


RECAP_FILLER = frozenset("""
thing things one ones first next step steps again before said same short version part bit
here that this it its is are was the a an and or of to for in on at with about from
""".split())


def _is_a_recap(turn, before):
    said = _words(turn.get("bot"))
    had = set(_words(before.get("bot")))
    if not said or not had or len(said) >= len(had):
        return False
    if before.get("module") != "answers":
        return False
    return all(word in had or word in RECAP_FILLER or word in ECHO_FILLER for word in said)


def _last_line_that_named_a_call(memory):
    turns = memory.get("turns") if isinstance(memory, dict) else None
    if not isinstance(turns, list) or not turns:
        return ""
    last = turns[-1]
    if not isinstance(last, dict):
        return ""
    if last.get("module") == "answers":
        return ""
    said = _flat(last.get("bot"))
    if not said or (_first(said, CARE) is None and REFER.search(said) is None):
        return ""
    return said


URGENT_CALL = re.compile(
    r"\b(?:999|911|112|a&e|accident and emergency|ambulance|111|out of hours|straight away"
    r"|right away|today|tonight|do not wait|dont wait|immediately)\b", re.I)


def _a_call_for_now(said):
    if _care_for_now(said):
        return True
    for sentence in re.split(r"(?<=[.!?]) ", str(said or "")):
        found = REFER.search(sentence)
        if not found:
            trade = TRADE.search(sentence)
            if trade is None:
                continue
            if LATER_CONDITION.search(sentence[:trade.start()]) is not None:
                continue
            if TIME_NOW.search(sentence) is not None:
                return True
            continue
        if not LATER_CONDITION.search(sentence[found.start():]):
            return True
        if TIME_NOW.search(sentence[found.start():]):
            return True
    return False


EMERGENCY_ORDER = re.compile(
    r"^\W*(?:that's|that is|this is|it's|it is)\s+(?:an?\s+)?(?:emergency|ambulance\b(?: job)?)"
    r"|^\W*treat (?:this|that) as (?:an? )?(?:emergency|ambulance)", re.I)
EMERGENCY_CALL_OPEN = re.compile(r"^\W*(?:ring|call|dial|phone)\s+(?:999|911|112|an ambulance)\b", re.I)


def _the_call_sentence(said):
    for sentence in re.split(r"(?<=[.!?]) ", str(said or "")):
        if EMERGENCY_ORDER.match(sentence) is not None:
            return sentence
        opening = EMERGENCY_CALL_OPEN.match(sentence)
        if opening is not None and LATER_CONDITION.search(sentence[opening.end():]) is None:
            return sentence
        if TIME_NOW.search(sentence) is None:
            continue
        found = REFER.search(sentence)
        if found is not None:
            tail = sentence[found.start():]
            if LATER_CONDITION.search(tail) is None or TIME_NOW.search(tail) is not None:
                return sentence
            continue
        trade = TRADE.search(sentence)
        if trade is None:
            continue
        if LATER_CONDITION.search(sentence[:trade.start()]) is not None:
            continue
        return sentence
    return ""


def _last_person_line(memory):
    turns = memory.get("turns") if isinstance(memory, dict) else None
    if not isinstance(turns, list) or not turns:
        return ""
    for last in reversed(turns):
        if not isinstance(last, dict):
            return ""
        said = _flat(last.get("user"))
        if not said:
            continue
        return said
    return ""


def _the_worst_thing_they_said(memory):
    turns = memory.get("turns") if isinstance(memory, dict) else None
    if not isinstance(turns, list):
        return ""
    for last in reversed(turns):
        if not isinstance(last, dict):
            return False
        said = _flat(last.get("user"))
        if said:
            return said if HARD_NEWS.search(said) else ""
    return ""


def _as_written(line):
    text = _flat(line)
    if not text:
        return "", ""
    try:
        read = normalise(text)
    except Exception:
        return "", ""
    return _flat(read.get("plain") or ""), _flat(read.get("norm_text") or "")


def _a_thing_they_own(memory):
    line = _the_line_behind(memory)
    if not line:
        return ""
    low = _flat(line)
    if A_BODY_WORD.search(low):
        return ""
    found = A_THING_THEY_OWN.search(low)
    return found.group(0).lower() if found else ""


def _a_person_they_know(memory, said):
    line = _the_line_behind(memory)
    if not line:
        return ""
    low = _flat(line)
    if A_SYMPTOM_WORD.search(low):
        return ""
    if not A_PERSON_THEY_KNOW.search(low) or not A_RELATION_TROUBLE.search(low):
        return ""
    return "person"


def _the_line_behind(memory):
    turns = memory.get("turns") if isinstance(memory, dict) else None
    if not isinstance(turns, list) or not turns:
        return ""
    turns = _skip_the_derived(turns, memory)
    for index in range(len(turns) - 1, -1, -1):
        last = turns[index]
        if not isinstance(last, dict):
            return ""
        module = last.get("module")
        if module in UNREADABLE:
            return ""
        if module == "chat" and OWN_PATTERN.search(_flat(last.get("bot"))):
            continue
        if _is_an_echo(last):
            continue
        if A_STEP_ASK.match(_flat(last.get("user")) or "") and module != "answers":
            continue
        if index and _is_a_recap(last, turns[index - 1]):
            continue
        if module in READABLE:
            return _flat(last.get("user"))
        return ""
    return ""

def _the_plan_they_brought(memory, back=2):
    turns = memory.get("turns") if isinstance(memory, dict) else None
    if not isinstance(turns, list):
        return ""
    seen = 0
    for turn in reversed(turns):
        if not isinstance(turn, dict):
            continue
        said = _flat(turn.get("user"))
        if not said:
            continue
        seen += 1
        if seen > back:
            break
        if A_PLAN.search(said) or CONSIDERING.search(said):
            return said
    return ""


A_CHECK_ON_A_PLAN_LINES = (
    "Say which part you are unsure about and we can weigh it up together.",
    "Tell me the bit that is nagging you and I will go through it with you.",
    "Which part of it is the one you keep coming back to? That is usually the part worth settling "
    "first.",
    "Put the two sides next to each other and the answer usually shows itself: what it costs you, "
    "and what it gives you. Which one is it for you?",
)
A_CHECK_ON_A_PLAN = re.compile(
    r"^(?:and |so |but )?(?:is|was|does|did|do) (?:that|this|it) "
    r"(?:be |sound |look |seem )?"
    r"(?:fair|ok|okay|alright|all right|fine|"
    r"make (?:any )?sense|sound (?:ok|okay|fine|fair))(?: then| though)?$")

CONSIDERING = re.compile(
    r"\b(?:thinking (?:of|about)|considering|planning (?:to|on)|looking to|hoping to|"
    r"(?:i|we) (?:really )?(?:want|need|fancy)|want(?:ing)? to)\b[^.]{0,30}?"
    r"\b(?:get|getting|buy|buying|adopt|adopting|rescue|rescueing|book|booking)\b", re.I)


def _considering(memory):
    turns = memory.get("turns") if isinstance(memory, dict) else None
    if not isinstance(turns, list):
        return False
    for turn in reversed(turns):
        if not isinstance(turn, dict):
            continue
        said = _flat(turn.get("user"))
        if said:
            return bool(CONSIDERING.search(said))
    return False


def _the_last_line_was_mine(memory):
    turns = memory.get("turns") if isinstance(memory, dict) else None
    if not isinstance(turns, list) or not turns:
        return False
    for last in reversed(turns):
        if not isinstance(last, dict):
            return False
        module = last.get("module")
        if not module:
            continue
        return module == "chat" or module in COMPOSED
    return False


def _last_module(memory, past_the_nod=False):
    punt_module = ""
    turns = memory.get("turns") if isinstance(memory, dict) else None
    if not isinstance(turns, list) or not turns:
        return ""
    turns = _skip_the_derived(turns, memory)
    for index in range(len(turns) - 1, -1, -1):
        last = turns[index]
        if not isinstance(last, dict):
            return punt_module
        module = last.get("module")
        if module in UNREADABLE:
            return punt_module
        if module == "chat" and OWN_PATTERN.search(_flat(last.get("bot"))):
            continue
        if _a_report_line(last.get("bot")):
            continue
        if module in COMPOSED and why.is_a_reason_line(_flat(last.get("bot"))):
            continue
        if module in READABLE and takes_a_fact_back(last.get("bot")):
            continue
        if A_STEP_ASK.match(_flat(last.get("user"))) and module != "answers":
            continue
        if _a_punt(last):
            if not past_the_nod or punt_module:
                return module if not past_the_nod else punt_module
            punt_module = module
            continue
        if _is_an_echo(last):
            continue
        if index and _is_a_recap(last, turns[index - 1]):
            continue
        if module in READABLE:
            if punt_module and module != "answers":
                return punt_module
            return module
        return punt_module
    return punt_module


OWN_DOING = re.compile(
    r"^i\s+(?!am\b|m\b|'m\b|have\b|had\b|havent\b|got\b|ve\b|need\b|want\b"
    r"|found\b|noticed\b|spotted\b|saw\b|seen\b|might\b|may\b|could\b|probably\b)"
    r"[a-z']+\b", re.I)


CAN_HURT = (
    ("carbon monoxide", re.compile(
        r"\b(?:car|engine|van|generator|mower|bbq|barbecue|charcoal|stove)\b"
        r"(?:\W+\w+){0,4}?\W+(?:running|left\s+on|on|lit|going|burning)\b", re.I),
     re.compile(r"\b(?:garage|shed|indoors?|inside|tent|room)\b", re.I)),
    ("a medicine", re.compile(
        r"\b(?:stop|stopping|quit|quitting|come\s+off|coming\s+off|double|doubling|halve|halving|"
        r"skip|skipping|cut\s+(?:it\s+)?(?:in\s+half|down)|take\s+more|up\s+the\s+dose)\b"
        r"(?!\s+(?:working|helping|hurting))"
        r"(?:\W+\w+){0,4}?\W+(?:insulin|antidepress\w*|antibiotic\w*|medication|medications|"
        r"meds|tablets?|pills?|statins?|steroids?|inhaler|epipen|epi\s*pen|"
        r"blood\s+pressure\s+(?:tablets?|meds?)|dose|dosage|prescription)\b", re.I), None),
    ("the mains", re.compile(
        r"\b(?:rewire|re-wire|wire\s+(?:it|up|the\s+socket|a\s+socket|the\s+lights?)|"
        r"fit\s+(?:a\s+|the\s+)?(?:socket|fuse\s*box|consumer\s+unit)|"
        r"move\s+(?:a\s+|the\s+)?(?:socket|fuse\s*box)|"
        r"(?:socket|fuse\s*box|consumer\s+unit|wiring|boiler)\b(?:\W+\w+){0,4}?\W+"
        r"(?:myself|ourselves|himself|herself))\b", re.I), None),
    ("that blade", re.compile(
        r"\b(?:angle\s+grinder|grinder|chainsaw|chain\s+saw|circular\s+saw|table\s+saw|"
        r"chop\s+saw|bench\s+saw|saw)\b", re.I),
     re.compile(r"\b(?:no\s+guard|without\s+(?:the\s+|a\s+|its\s+)?guard|guard\s+off|"
                r"took\s+(?:the\s+|its\s+)?guard\s+off|no\s+goggles|without\s+goggles)\b",
                re.I)),
    ("a job like that", re.compile(
        r"\b(?:take|taking|knock|knocking|pull|pulling|remove|removing)\s+(?:the\s+|my\s+|our\s+)?"
        r"(?:chimney|wall|ceiling|lintel)\b(?:\W+\w+){0,3}?\W+(?:out|down|off)\b"
        r"|\b(?:on\s+the\s+roof|up\s+(?:a|the)\s+ladder|on\s+(?:a|the)\s+ladder)\b"
        r"(?:\W+\w+){0,3}?\W+(?:myself|ourselves|alone|on\s+my\s+own|by\s+myself)\b"
        r"|\b(?:myself|ourselves)\b(?:\W+\w+){0,4}?\W+"
        r"(?:on\s+the\s+roof|up\s+(?:a|the)\s+ladder|off\s+the\s+ladder)\b", re.I), None),
)
NAMES_A_TRADE = re.compile(
    r"\b(?:electrician|plumber|builder|roofer|chimney\s+sweep|gas\s+safe|engineer|"
    r"handyman|scaffold\w*)\b", re.I)
A_KEEP_OR_STOP = re.compile(
    r"\b(?:keep|carry\s+on|stopping|stop|do\s+not|don\u2019t|dont|never|ask|check|review|"
    r"until|rather\s+than)\b", re.I)
THE_PLAN_CAN_HURT_LINES = {
    "carbon monoxide": (
        "Good that you checked. Not with the engine running in there, though - that is carbon "
        "monoxide, and it puts people to sleep before they notice it. Run it outside, and if the "
        "door has to stay shut, have somebody with you.",
        "Right to ask. That one gives off carbon monoxide, and a garage or a tent holds it: do it "
        "out in the open, or with the doors wide open and somebody knowing you are in there.",
        "Worth asking: an engine or a fire in a closed space is carbon monoxide, and that is the "
        "kind that takes people quietly. Move it outside before you start it.",
    ),
    "a medicine": (
        "Not without the person who prescribes it: stopping it, doubling it or cutting a tablet "
        "in half is the one change they want to hear about first. Ring the surgery, a pharmacist "
        "or 111 and ask what to do today.",
        "That one goes through whoever prescribes it - a change of dose or a stop is not "
        "something to work out alone. Ring the surgery or a pharmacist, and keep taking it as "
        "written until they say otherwise.",
        "Ask the prescriber before you change it, and carry on as written until then. A "
        "pharmacist will answer this the same day, and 111 will at night.",
    ),
    "the mains": (
        "Not by hand: that is mains, and it is not a thing to learn on. Get a registered "
        "electrician in - a socket or a fuse box done wrong is the sort of fault that waits.",
        "Not on your own. Mains wiring has to be done and signed off by somebody registered, and "
        "the part that goes wrong is inside the wall where you cannot see it.",
    ),
    "that blade": (
        "Not with the guard off. That guard is the part that comes between you and the blade, "
        "and a saw does not give you a second go: put it back, or get somebody who has one.",
        "Put the guard back on first, and goggles too - that is the half of the job that keeps "
        "your hands the shape they are.",
    ),
    "a job like that": (
        "Not from a ladder on your own, and not by taking it down yourself: that wants somebody "
        "who has done it before, and a second pair of hands. Get a builder or a chimney sweep "
        "round, and let them say what it is.",
        "A job like that is one to hand over rather than climb to - a ladder on your own is how "
        "people get hurt at home. Ring somebody who does it for a living.",
    ),
}


def _the_plan_can_hurt(said):
    if not said or NAMES_A_TRADE.search(said):
        return None
    for family, act, guard in CAN_HURT:
        if act.search(said) is None:
            continue
        if guard is not None and guard.search(said) is None:
            continue
        return family
    return None


def _the_answer_already_warned(said):
    if not said or not NAMES_A_CLINICIAN.search(said):
        return ""
    for sentence in re.split(r"(?<=[.!?])\s+", said):
        sentence = sentence.strip()
        if not 6 <= len(sentence.split()) <= 40:
            continue
        if NAMES_A_CLINICIAN.search(sentence) is None:
            continue
        if A_KEEP_OR_STOP.search(sentence) is None:
            continue
        return sentence.rstrip(" .") + "."
    return ""


def _a_plan_doubt(memory):
    said = _flat(_the_line_behind(memory))
    if not said or not A_PLAN.search(said):
        said = _the_plan_they_brought(memory)
    if not said:
        return None
    return pick(_round_robin(A_PLAN_DOUBT_LINES, said), memory, said)


def _about_the_person(memory):
    turns = memory.get("turns") if isinstance(memory, dict) else None
    if not isinstance(turns, list) or len(turns) < 1:
        return False
    for last in reversed(turns):
        if not isinstance(last, dict):
            return False
        if _is_an_echo(last):
            continue
        said = _flat(last.get("user"))
        if not said or len(said.split()) < 3:
            return False
        return re.match(r"(?:i\s|ive\s|i've\s|i\u2019ve\s)", said, re.I) is not None
    return False


def _own_doing(memory):
    turns = memory.get("turns") if isinstance(memory, dict) else None
    if not isinstance(turns, list) or len(turns) < 1:
        return False
    for last in reversed(turns):
        if not isinstance(last, dict):
            return False
        if _is_an_echo(last):
            continue
        said = _flat(last.get("user"))
        return bool(said) and len(said.split()) >= 3 and OWN_DOING.match(said) is not None
    return False


def _a_plan_or_a_choice(memory):
    said = _flat(_the_line_behind(memory))
    if not said or not (A_PLAN.search(said) or A_DECISION_ASK.search(said)):
        return False
    words = _words(said)
    return not any(word in BODY_WORD for word in words) and not any(
        word in SOMEONE_ELSE for word in words)


def _good_news(memory):
    if _reads_as_good_news is None:
        return False
    turns = memory.get("turns") if isinstance(memory, dict) else None
    if not isinstance(turns, list) or not turns:
        return False
    for last in reversed(turns):
        if not isinstance(last, dict):
            return False
        if _is_an_echo(last):
            continue
        said = _flat(last.get("user"))
        return bool(said) and _reads_as_good_news(said)
    return False


OVER_VERB = re.compile(
    r"\bi\s+(?:\w+ed|did|ran|got|went|came|made|took|won|bought|wrote|sent|met|found|gave|had|"
    r"kept|left|put|saw|spoke|sold|paid|drove|flew|finished|passed|booked|handed|signed|told|"
    r"started|stopped|began|broke|lost|held|built|caught|chose|felt)\b")
STILL_GOING = re.compile(
    r"\b(?:yet|still|again|every (?:day|night|week|morning|time)|keeps?|always|constantly|"
    r"anymore|any more|since|for (?:weeks|months|years|days)|all the time|at the moment|"
    r"now|these days|lately)\b")


def _an_event_that_is_over(memory):
    turns = memory.get("turns") if isinstance(memory, dict) else None
    if not isinstance(turns, list) or not turns:
        return False
    for last in reversed(turns):
        if not isinstance(last, dict):
            return False
        if _is_an_echo(last):
            continue
        said = _flat(last.get("user"))
        if not said or STILL_GOING.search(said):
            return False
        return OVER_VERB.search(said) is not None
    return False


def _nothing_to_be_long_about(memory):
    return _good_news(memory) or _an_event_that_is_over(memory)


def _first(text, words):
    text = str(text or "").lower()
    best = None
    for word in words:
        at = text.find(word)
        if at >= 0 and (best is None or at < best):
            best = at
    return best


def _a_throw_away(said):
    said = str(said or "")
    for match in THROW_AWAY.finditer(said):
        before = said[:match.start()]
        if NOT_TOLD_TO.search(before) or ONE_OPTION.search(before):
            continue
        sentence = before.split(".")[-1]
        action = match.group(0)
        action = action[0].upper() + action[1:]
        if TESTING.search(sentence) or CONDITIONAL.search(sentence.split(",")[-1]):
            return action, True
        return action, False
    return None, False


SIGN = re.compile(r"\b(?:sour|off|mouldy|moldy|curdled|smelly|smells|stinks|stinking|fizzy|"
                  r"rancid|turned|slimy|furry|green|black|gone bad|gone off|past it)\b", re.I)
ASKING_HOW_TO_TELL = re.compile(r"\b(?:how do i (?:know|tell|check)|how can i tell|how to tell|"
                               r"how do you tell|how do i spot|what should i look for|"
                               r"what do i look for|what should i check|is it still (?:ok|okay|fine))\b",
                               re.I)


def _the_person_line(memory, said):
    said = str(said or "").strip()
    for turn in reversed(list((memory or {}).get("turns") or [])):
        line = str(turn.get("user") or "").strip()
        if line and line != said:
            return line
    return ""


def _said_no(said):
    for sentence in re.split(r"(?<=[.!?])\s+", str(said or "")):
        if STATED_NO.search(sentence) is not None:
            sentence = sentence.strip().strip("\"'\u201c\u201d").strip()
            if sentence:
                return sentence.rstrip(".") + "."
    return None


def _said_enough(said):
    for sentence in re.split(r"(?<=[.!?])\s+", str(said or "")):
        if STATED_ENOUGH.search(sentence) is None:
            continue
        sentence = sentence.strip().strip("\"'\u201c\u201d").strip().rstrip(".")
        if len(sentence) > 90 and "," in sentence:
            head = sentence.split(",")[0].strip()
            if len(head) > 20 and STATED_ENOUGH.search(head) is not None:
                sentence = head
        if sentence:
            return sentence + "."
    return None


def _the_person_gave_the_sign(memory, said):
    line = _the_person_line(memory, said)
    if not line or ASKING_HOW_TO_TELL.search(line):
        return False
    return bool(SIGN.search(line))
LATER_CONDITION = re.compile(r"\b(?:if|unless|when|once|whenever|as soon as)\b", re.I)

TRADE = re.compile(
    r"\b(?:gp|doctor|midwife|health visitor|111|999|112|a&e|dentist|pharmacist|optician|"
    r"physio(?:therapist)?|nurse|vet|paramedic|district nurse|out of hours)\b", re.I)


def _care_for_now(said):
    for sentence in re.split(r"(?<=[.!?]) ", str(said or "")):
        found = _first(sentence, CARE)
        if found is None:
            continue
        cue = min((sentence.lower().find(word) for word in CARE if word in sentence.lower()),
                  default=-1)
        if (cue >= 0 and not LATER_CONDITION.search(sentence[cue:])
                and not LATER_CONDITION.search(sentence[:cue])):
            return True
    return False


def _sentence_at(text, at):
    begin = 0
    for found in re.finditer(r"(?<=[.!?]) ", text):
        if found.start() >= at:
            return text[begin:found.start()]
        begin = found.end()
    return text[begin:]


def _behind_a_description(said, at):
    sentence = _sentence_at(said, at)
    if len(sentence) <= len(said) - at - 1 and not sentence.endswith((".", "!", "?")):
        sentence = sentence + "."
    described = _a_described_condition(sentence)
    if not described:
        return False
    marker = None
    for found in re.finditer(r"\b(?:that|which|who)\s+", sentence, re.I):
        marker = found
    if marker is None or not sentence[:marker.start()].strip():
        return False
    cue = sentence.lower().find(said[at:at + 12].lower()) if at < len(said) else -1
    return cue > marker.start()

def _not_fenced(said, start, end=None):
    before = said[max(0, start - 90):start]
    if CONDITIONAL.search(before.split(".")[-1]):
        return False
    if end is not None:
        after = said[end:end + 90].split(".")[0]
        fence = CONDITIONAL_AFTER.search(after)
        if fence and not URGENT_TIME.search(said[start:end + 40]):
            rider = after[:fence.start()]
            if not COMPARATIVE.search(rider):
                return False
    return True


NEGATED_BEFORE = re.compile(r"(?:\bnot|\bnever|\bno|n't|\bless|\bhardly|\bexcept|\bwithout)"
                      r"\s+(?:\w+\s+){0,2}$")


def _said_without_a_not(text, at, length):
    if text[max(0, at - 2):at] == "un":
        return False
    before = text[at - 1] if at else " "
    after = text[at + length:at + length + 1]
    if before.isalnum() or after.isalnum():
        return False
    return NEGATED_BEFORE.search(text[max(0, at - 26):at]) is None


def _first_positive(text, words):
    text = str(text or "").lower()
    best = None
    for word in words:
        start = 0
        while True:
            at = text.find(word, start)
            if at < 0:
                break
            if _said_without_a_not(text, at, len(word)):
                if best is None or at < best:
                    best = at
                break
            start = at + 1
    return best


def _unconditional_care(said):
    said = str(said or "").lower()
    best = None
    for word in CARE:
        start = said.find(word)
        while start >= 0:
            if (_not_fenced(said, start, start + len(word))
                    and not _behind_a_description(said, start)):
                if best is None or start < best:
                    best = start
                break
            start = said.find(word, start + 1)
    for match in REFER.finditer(said):
        if not _not_fenced(said, match.start(), match.end()):
            continue
        if best is None or match.start() < best:
            best = match.start()
        break
    return best


def _the_fence_is_met(fence, said, memory):
    if not isinstance(memory, dict):
        return False
    line = (_the_line_it_answered(said, memory) or "").lower()
    if not line:
        turns = memory.get("turns") or []
        line = str((turns[-1] or {}).get("user") or "").lower() if turns else ""
    if not line:
        return False
    said = {word.rstrip("s") for word in re.findall(r"[a-z']{4,}", line)}
    for word in re.findall(r"[a-z']{4,}", str(fence or "").lower()):
        if word.rstrip("s") in said:
            return True
    return False


A_FREQUENCY_SAID = re.compile(
    r"\b(?:every|most|each|all) (?:\w+ )?(?:day|days|night|nights|morning|mornings|afternoon|"
    r"afternoons|evening|evenings|week|weeks|month|months)\b|"
    r"\ball the time\b|\balways\b",
    re.I)

A_FREQUENCY_ASKED = re.compile(
    r"\bmost days\b|\bmost nights\b|\bevery day\b|\bregularly\b|\bseveral times\b|"
    r"\bmore than (?:once|twice)\b|\bkeeps? (?:coming|happening|returning)\b|"
    r"\btime and again\b",
    re.I)


def _a_frequency_already_said(fence, said, memory):
    if not isinstance(memory, dict) or not A_FREQUENCY_ASKED.search(str(fence or "")):
        return False
    answered = _the_line_it_answered(said, memory)
    subject = {word.rstrip("s") for word in re.findall(r"[a-z']{4,}", answered)}
    for turn in memory.get("turns") or []:
        line = str((turn or {}).get("user") or "").lower()
        if not A_FREQUENCY_SAID.search(line):
            continue
        if not subject:
            return True
        words = {word.rstrip("s") for word in re.findall(r"[a-z']{4,}", line)}
        if words & subject:
            return True
    return False


def _condition_after_care(said, care_at, memory=None):
    if care_at is None or care_at < 0:
        return ""
    sentence = re.split(r"(?<=[.!?]) ", str(said or "")[care_at:])[0]
    fence = re.search(r"\b(?:if|unless|once|when) \w", sentence, re.I)
    if not fence:
        if _the_call_sentence(said):
            return ""
        if memory is not None and _past_the_timescale(said, memory):
            return ""
        later = _when(said)
        if later and _a_frequency_already_said(later, said, memory):
            return ""
        if later and _the_fence_is_met(later, said, memory):
            return ""
        return _cut_condition(later) if later else ""
    if TIME_NOW.search(sentence):
        return ""
    if COMPARATIVE.search(sentence[:fence.start()]):
        return ""
    return _cut_condition(_when(said))


TIME_NOW = re.compile(r"\btoday\b|\bnow\b|\btonight\b|straight away|as soon as|"
                      r"\btomorrow\b|\bthis (?:morning|afternoon|evening)\b|\bnext few hours\b|"
                      r"\bthe same day\b(?!\s+if\b)",
                      re.I)


CONDITION_CLAUSE = re.compile(r", (?:and |or |then |so )?| and | or ")


def _cut_condition(when, most=22):
    when = str(when or "").strip(" ,.")
    if len(when.split()) <= most:
        return when
    when = CONDITION_CLAUSE.split(when)[0].strip(" ,.")
    return when

def _first_sentence_end(said):
    found = re.search(r"[.!?](?:\s|$)", str(said or ""))
    return found.end() if found else len(str(said or ""))


def _told_to_act(said, at):
    said = str(said or "")
    if not DECLARATIVE_REFERRAL.match(said, at):
        return True
    return at <= _first_sentence_end(said)


def _referral(said):
    care = _unconditional_care(said)
    if care is None:
        stated = DECLARATIVE_REFERRAL.search(str(said or ""))
        if stated is not None and _not_fenced(said, stated.start(), stated.end()):
            return stated.start()
        return None
    if care <= _first_sentence_end(said):
        return care
    return care if _told_to_act(said, care) else None


GO_FROM = ("worth a gp", "gp visit", "worth a hearing test", "a referral",
           "for a referral", "worth getting looked at", "worth seeing")


def _a_plain_go(at, said):
    said = str(said or "").lower()
    window = said[max(0, at - 24):at + 24]
    return any(word in window for word in GO_FROM)


def _opening(said):
    parts = re.split(r"(?<=[.!?]) ", str(said or ""))
    return " ".join(parts[:2])


FENCED_IN_SENTENCE = re.compile(r"\b(?:if|unless|once|when|whenever|in case|most days)\b",
                                re.IGNORECASE)
THING_WORDS = frozenset("""about after again also always another anything around because been
before being both came cant could does doing done down during each even ever every from
getting give going good have having here just keep keeps know last like little long made make
many more most much must need needs never next only other over really right same should since
some something still such sure than that their them then there these thing things think this
those through time today tomorrow tonight under until very want wants well went were what when
where which while will with would your yours yourself""".split())


def _the_thing(line):
    return {word for word in re.findall(r"[a-z']{4,}", _flat(line)) if word not in THING_WORDS}


def _referral_about_the_thing(said, line):
    thing = _the_thing(line)
    if not thing:
        return False
    for sentence in re.split(r"(?<=[.!?]) ", str(said or "")):
        if not NAMES_A_CLINICIAN.search(sentence):
            continue
        if FENCED_IN_SENTENCE.search(sentence):
            continue
        if thing & set(re.findall(r"[a-z']{4,}", sentence.lower())):
            return True
    return False


def _echoes_the_person(step, memory):
    turns = memory.get("turns") if isinstance(memory, dict) else None
    if not isinstance(turns, list) or not turns:
        return False
    said = ""
    for turn in reversed(turns):
        if isinstance(turn, dict) and turn.get("user"):
            said = str(turn["user"])
            break
    if not said:
        return False
    from ..memory.topics import content
    want, have = set(content(step)), set(content(said))
    if not want or len(want) > 3:
        return False
    return not (want - have)


def _kept_step(reply):
    plain = _flat(reply).strip()
    return any(re.fullmatch(_own_pattern(line), plain, re.IGNORECASE)
               for line in STEP_KEPT_LINES)


def _only_a_verdict(line):
    text = _flat(line or "").strip()
    if not text:
        return False
    try:
        from .fallback import reads_as_a_verdict
    except Exception:
        return False
    try:
        return bool(reads_as_a_verdict(text))
    except Exception:
        return False


def _the_line_just_given(memory):
    turns = memory.get("turns") if isinstance(memory, dict) else None
    if not isinstance(turns, list):
        return ""
    for turn in reversed(turns):
        if isinstance(turn, dict) and turn.get("bot"):
            return str(turn["bot"])
    return ""


def _the_answer_before_that(memory):
    turns = memory.get("turns") if isinstance(memory, dict) else None
    if not isinstance(turns, list):
        return ""
    seen = 0
    for turn in reversed(turns):
        if isinstance(turn, dict) and turn.get("bot"):
            seen += 1
            if seen == 2:
                return str(turn["bot"])
    return ""


def _word_runs(text, size=5):
    words = _flat(text).split()
    return {tuple(words[at:at + size]) for at in range(max(0, len(words) - size + 1))}


def _says_it_again(line, said):
    return bool(_word_runs(line) & _word_runs(said))




def _already_asked_for_a_step(memory):
    turns = memory.get("turns") if isinstance(memory, dict) else None
    if not isinstance(turns, list):
        return False
    for turn in reversed(turns):
        if isinstance(turn, dict) and turn.get("user"):
            return bool(STEP.match(_flat(turn["user"])))
    return False


def _the_referral_sentence(said):
    text = str(said or "")
    at = _first(text.lower(), CARE)
    if at is None:
        at = 0
    start = max(text.rfind(". ", 0, at), text.rfind("? ", 0, at), text.rfind("! ", 0, at))
    return re.split(r"(?<=[.!?]) ", text[start + 1:].strip())[0]


def _the_line_is_the_threshold(stated, line):
    from ..memory.topics import content
    want, have = set(content(stated)), set(content(line))
    return len(want & have) >= 2


def _most_of_the_line(step, heard):
    from ..memory.topics import content
    want, have = set(content(step)), set(content(heard))
    if not want or not have:
        return False
    return len(want & have) / len(have) >= 0.8


def _step(said):
    found = [one for one in _steps(said) if not NEGATIVE_OPEN.match(one)]
    found = [one for one in found if not A_STATEMENT.match(one)]
    return found[0] if found else None


A_STATEMENT = re.compile(r"^(?:[a-z']+\s+)(?:is|are|was|were|has|have|had|can|cannot|will|would|"
                         r"should|takes?|gives?|means?|costs?|comes?|goes?|does|did|gets?|keeps?)\b",
                         re.I)


TARGET_SHAPE = re.compile(
    r"^(?:build|work|save|grow)\s+up\b"
    r"|^(?:build|work|save|aim|get|grow|reach)\b[^.!?]{0,24}?\b(?:towards|toward|up to)\b",
    re.I)


def _listed(said):
    for sentence in re.split(r"(?<=[.!?]) ", str(said or "")):
        if CONDITIONAL_OPEN.match(sentence.strip()):
            continue
        head, colon, tail = sentence.partition(": ")
        if not colon or tail.count(",") < 2:
            continue
        if HEAD_REFUSES.search(head) or not HELPS.search(head):
            continue
        for item in re.split(r",| and ", tail):
            item = " ".join(item.strip(" .:;,-").split())
            words = item.split()
            if not 3 <= len(words) <= STEP_WORDS:
                continue
            if NEGATIVE_OPEN.match(item) or CONDITIONAL_OPEN.match(item):
                continue
            if DESCRIBES.search(item):
                continue
            return item
    return None


TRIM = (" because ", " so it ", " so that ", " before ", " after ",
        " until ", " if ", " when ", " rather than ")
TRIM_INSTRUMENT = (" using ", " with ")
CONTRAST = re.compile(r"\b(?:rather than|instead of)\b", re.I)
STEP_WORDS = 16
LONG_STEP_WORDS = 24
STEP_LONG = 10
COPULA = re.compile(r"^(?:[\w,'-]+\s+){0,5}(?:is|are|was|were)\b")
DETAIL_STATEMENT = re.compile(r"\b(?:is|are|was|were)\b", re.I)
CONDITIONAL_OPEN = re.compile(r"^(?:if|unless|once|when|whenever|should|in case)\b",
                            re.IGNORECASE)
ABOUT_THE_TALK = re.compile(r"\b(?:let me know|keep me posted|tell me how (?:it|that) (?:goes|went)|"
                            r"how (?:it|that) goes|say more|tell me more|fair enough|"
                            r"thanks for telling me|i'?m listening|good to know|noted)\b", re.I)


def _cut_on(head, joins):
    best = ""
    for join in joins:
        at = head.find(join)
        while at > 0:
            cut = head[:at].strip(" ,;:-")
            cut_words = cut.split()
            if (4 <= len(cut_words) <= STEP_WORDS and cut_words[-1].lower() not in HANGING
                    and len(cut) > len(best)):
                best = cut
            at = head.find(join, at + 1)
    return best


NEGATIVE_OPEN = re.compile(r"^(?:do not|don't|dont|never)\b", re.IGNORECASE)

HELPS = re.compile(
    r"\b(?:things?|ones?|bits?|steps?|changes?|habits?|moves?|tips?|fixes|tricks|what|"
    r"everything|anything|these|those|the rest)\b[^:]{0,40}?"
    r"\b(?:works?|worked|helps?|helped|matters?|counts?|do|does|did|"
    r"worth (?:a|trying|doing|a go))\b"
    r"|\b(?:do|does|did) more than\b",
    re.IGNORECASE,
)
HEAD_REFUSES = re.compile(r"\b(?:not|n't|depends|depend|differ|if|whether|unless)\b", re.IGNORECASE)
DESCRIBES = re.compile(r"\b(?:who|whom|whose|which|that)\b", re.IGNORECASE)


def _shorten(head, words):
    if len(words) <= STEP_WORDS:
        return head
    best = _cut_on(head, TRIM)
    if best:
        return best
    if len(words) <= LONG_STEP_WORDS and words[-1].lower() not in HANGING:
        return head
    return _cut_on(head, TRIM_INSTRUMENT)


CONTINUES = re.compile(r"^\s*(?:or|but|so|yet|nor|otherwise)\b", re.IGNORECASE)
ORDER_CONTINUES = re.compile(r"^\s*(?:then|after\s+that|next)\b", re.IGNORECASE)


FRAME_AND = re.compile(r"\b(?:between|both)\b[^,;:.!?]*\band\b", re.I)


def _cut_at_a_join(part):
    keep_until = 0
    for frame in FRAME_AND.finditer(part):
        if frame.end() > keep_until:
            keep_until = frame.end()
    for at in re.finditer(r" and | then ", part):
        if at.start() < keep_until:
            continue
        return part[:at.start()]
    return part


def _first_clause(part, and_break=True):
    for at in (index for index, char in enumerate(part) if char == ","):
        if not and_break and ORDER_CONTINUES.match(part[at + 1:]):
            continue
        if not CONTINUES.match(part[at + 1:]):
            return part[:at]
    if not and_break:
        return part
    return _cut_at_a_join(part)


QUESTION_FRAME = re.compile(
    r"^(?:(?:so|and|but|or|ok|okay|right|well|then|now|look|listen|go on|go ahead|come on|"
    r"tell me)\b[\s,\u2014\u2013.:;-]*)*"
    r"(?:(?:do|did|does|would|will|can|could|shall|should|have|has|are|is|was|were)\s+"
    r"(?:you|i|we|they|he|she|it|there|that|this|anyone|anybody|someone)\b"
    r"|(?:what|why|how|where|who|which|whose)\b)", re.IGNORECASE)


OFFER_QUESTION = re.compile(
    r"\b(?:want (?:me to|a hand|me to)|would you like|shall i|can i help|may i help|"
    r"what would help|how can i help|anything (?:else )?i can do|where would you like|"
    r"do you want to (?:say|tell|talk)|where are you with|what(?:'s| is) it like|"
    r"is there (?:anyone|someone|anybody|somebody)|want to (?:say|tell|talk))\b",
    re.IGNORECASE)


def _an_offer_is_waiting(said):
    text = str(said or "").strip()
    if not text.endswith("?"):
        return False
    last = re.split(r"(?<=[.!?]) ", text)[-1]
    return bool(OFFER_QUESTION.search(last))


_INVITATION = re.compile(
    r"^(?:(?:do|would|will|can|could)\s+you\s+(?:want\s+to\s+"
    r"|like\s+to\s+|care\s+to\s+|mind\s+)?"
    r"(?:tell\s+me|talk\s+(?:me\s+through|about)|say|start)\s*(?:a\s+bit\s+)?(?:more\s+)?"
    r"(?:about\s+)?)", re.I)
THE_PLEA = re.compile(r"^(?:and |so )?what now$", re.I)
AN_OFFER = re.compile(
    r"\b(?:anything\s+(?:else\s+)?(?:you.?d|i\s+can|to\s+add)|anything\s+on\s+your\s+mind"
    r"|what\s+else|something\s+else|is\s+there\s+anything)\b", re.I)


def _after_a_comfort_line(memory):
    turns = memory.get("turns") if isinstance(memory, dict) else None
    if not isinstance(turns, list) or not turns or not isinstance(turns[-1], dict):
        return False
    said = str(turns[-1].get("bot") or "").lower()
    if not said:
        return False
    try:
        from .fallback import COMFORT_SAID
        from ..modules import chat as _chat
        lines = tuple(COMFORT_SAID) + tuple(getattr(_chat, "FEELING_SAID", ()))
    except Exception:
        return False
    return any(line and line.lower() in said for line in lines)


_A_DASH = re.compile(r"^(.*?)\s+[\u2014\u2013-]\s+(.*)$")
_AN_OPENER = re.compile(
    r"^(?:so|and|but|or|ok|okay|right|well|then|now|look|listen|go on|go ahead|come on|tell me)$",
    re.IGNORECASE)


def _the_question_asked(said):
    text = str(said or "").strip()
    if not text.endswith("?"):
        return ""
    last = re.split(r"(?<=[.!?]) ", text)[-1].strip()
    if not _is_a_question(last):
        return ""
    asked = last[:-1].strip(" ,;:-")
    split = _A_DASH.match(asked)
    if split:
        front = split.group(1).strip(" ,;:-")
        rest = split.group(2).strip(" ,;:-")
        if _AN_OPENER.match(front) and _is_a_question(rest + "?"):
            front = rest
        asked = front
    if _INVITATION.match(asked):
        return ""
    if not asked or len(asked.split()) > 14:
        return ""
    words = asked.split()
    if words[0] not in ("I", "I'm", "I've", "I'd", "I'll"):
        words[0] = words[0][:1].lower() + words[0][1:]
    return " ".join(words)


def _ends_on_a_question(said):
    text = str(said or "").strip()
    if not text.endswith("?"):
        return False
    last = re.split(r"(?<=[.!?]) ", text)[-1]
    return bool(QUESTION_FRAME.match(last) or QUESTION_FRAME.match(last.rsplit(", ", 1)[-1]))


def _is_a_question(sentence):
    text = str(sentence or "").strip()
    if not text.endswith("?"):
        return False
    if QUESTION_FRAME.match(text):
        return True
    return bool(QUESTION_FRAME.match(text.rsplit(", ", 1)[-1]))


def _steps(said):
    from ..memory.topics import RED_FLAG
    found = []
    parts = []
    for at_sentence, sentence in enumerate(re.split(r"(?<=[.!?]) ", str(said or ""))):
        if (CONDITIONAL_OPEN.match(sentence.strip()) or RED_FLAG.match(sentence.strip())
                or _is_a_question(sentence) or _is_an_explanation(sentence)):
            continue
        opened = THEN_OPEN.sub("", sentence.strip()) if not at_sentence else sentence
        if opened is not sentence:
            sentence = opened[:1].upper() + opened[1:]
            if not sentence:
                continue
        raw = SPLIT.split(sentence)
        kept = []
        for at, chunk in enumerate(raw):
            if at % 2 or not chunk.strip():
                continue
            kept.append((chunk.strip(), raw[at - 1] if kept else ""))
        if (len(kept) > 1 and CONTRAST.search(kept[0][0])
                and _doing_word(kept[1][0].split()) in IMPERATIVES):
            kept = kept[1:]
        if len(kept) > 1 and _doing_word(kept[0][0].split()) not in IMPERATIVES:
            kept = kept[1:]
        if len(kept) > 1 and all(sep == ": " for _, sep in kept[1:]):
            parts.append((": ".join(text for text, _ in kept), True))
        parts.extend((text, False) for text, _ in kept)
    for part, spread in parts:
        if RED_FLAG.match(part):
            continue
        part = re.sub(r"\([^)]*\)|\S*\.(?:com|co\.uk|org|net|gov)\S*", " ", part)
        part = " ".join(part.strip(" .:;,-").split())
        if not part:
            continue
        words = part.split()
        if _doing_word(words) not in IMPERATIVES or COPULA.match(part):
            continue
        if TARGET_SHAPE.match(part):
            continue
        if ABOUT_THE_TALK.search(part):
            continue
        protected = re.sub(r"(?<=\d) and (?=[\d.])", " \x00 ", part)
        if spread:
            opening, _, detail = protected.partition(": ")
            opening = _first_clause(opening, and_break=False).replace("\x00", "and")
            opening = opening.strip(" .:;,-")
            detail = detail.replace("\x00", "and").strip(" .:;,-")
            if DETAIL_STATEMENT.search(detail):
                detail = ""
            else:
                detail = _first_clause(detail).strip(" .:;,-")
            head = "%s: %s" % (opening, detail) if detail else opening
            if len(head.split()) > STEP_WORDS and "," in detail:
                detail = detail.split(",")[0].strip(" .:;,-")
                head = "%s: %s" % (opening, detail) if detail else opening
            if len(head.split()) > STEP_WORDS:
                head = _shorten(opening, opening.split()) or opening
        else:
            clause = _first_clause(protected).replace("\x00", "and").strip(" .:;,-")
            head = _shorten(clause, clause.split()) if len(clause.split()) >= 3 else ""
            if not head:
                trimmed = re.split(r",? then ", part)[0]
                head = _shorten(trimmed, trimmed.split()) if len(trimmed.split()) >= 2 else ""
            if not head:
                head = _shorten(part, words)
        if not head:
            return found
        words = head.split()
        if not words or words[-1] in HANGING or head in found:
            continue
        if _doing_word(words) not in IMPERATIVES:
            continue
        found.append(head)
    return found


def _doing_word(words):
    if words and words[0].strip("*_`(\"'[]").lower() in ("a", "an", "the"):
        return ""
    for index, word in enumerate(words[:5]):
        core = word.strip(",;:-\u2014\u2013").lower()
        if core in WHEN:
            continue
        return core
    return ""


def _action_count(said):
    said = " ".join(s for s in re.split(r"(?<=[.!?]) ", str(said or ""))
                    if not _is_a_question(s))
    total = 0
    for part in re.split(",| and | then |\\. |; |: | - | — | – ", said):
        words = part.strip(" .:;,-()").split()
        if words and _doing_word(words) in IMPERATIVES:
            total += 1
    return total


def _no_hanging_end(when):
    text = str(when or "").strip(" ,;:")
    while True:
        shorter = re.sub(r"(?:^|[ ,]+)(?:and|or|but|then|so|also|plus)$", "", text).strip(" ,;:")
        if shorter == text or not shorter:
            break
        text = shorter
    return text


CONDITION_VERBS = frozenset((
    "comes", "come", "gets", "get", "turns", "turned", "starts", "started", "goes", "went",
    "spreads", "spread", "wakes", "woke", "lasts", "lasted", "keeps", "kept", "has", "have",
    "develops", "developed", "bleeds", "bled", "swells", "swelled", "is", "are", "was", "were",
    "hurts", "stops", "stopped", "changes", "changed", "moves", "moved", "suddenly",
))
CONDITION_HANGING = frozenset("""
you i he she we they it or and but so if when with of the a an is are was were been t
""".split())
REFER_VERB = re.compile(
    r"\b(?:is|are|was|were|needs|needed|means|wants|should|must|will\s+need)\b", re.I)
RESTATED = re.compile(r",\s*(?:that|this|which|it)\s+(?:is|means|needs|wants|should)\b", re.I)


RELATIVE = re.compile(r"\b(?:that|which|who)\s+", re.I)


def _described_clause(sentence):
    referral = REFER.search(sentence)
    if referral is None:
        return None
    head = sentence[:referral.start()]
    marker = None
    for found in RELATIVE.finditer(head):
        marker = found
    if marker is None or not head[:marker.start()].strip():
        return None
    start = marker.end()
    clause = head[start:]
    cut = None
    for found in REFER_VERB.finditer(clause):
        rest = clause[found.end():].strip(" ,")
        if len(rest.split()) <= 4 and "," not in rest:
            cut = found.start()
    if cut is None:
        return None
    words = clause[:cut].strip(" ,;:-").split()
    if not 2 <= len(words) <= 26:
        return None
    if words[-1].strip(",;:").lower() in CONDITION_HANGING:
        return None
    if words[0].strip(",;:").lower() not in CONDITION_VERBS:
        return None
    return start, referral.start(), " ".join(words)


def _in_a_described_clause(sentence, at):
    found = _described_clause(sentence)
    return found is not None and found[0] <= at < found[1]


def _a_described_condition(sentence):
    found = _described_clause(sentence)
    if found is None:
        return ""
    return "it " + found[2]


def _an_if_that_is_a_condition(sentence):
    start = 0
    while True:
        at = sentence.find(" if ", start)
        if at < 0:
            return -1
        before = re.findall(r"[a-z']+", sentence[:at].lower())
        if not before or before[-1] not in LOOK_AND_SEE:
            return at
        start = at + 4


LOOK_AND_SEE = frozenset((
    "see", "check", "know", "wait", "tell", "find", "wonder", "decide", "guess", "ask",
    "notice",
))


def _a_judgement_fence(said):
    sentences = [s for s in re.split(r"(?<=[.!?]) ", said.strip()) if s.strip()]
    if not sentences:
        return ""
    last = sentences[-1]
    if NAMES_A_CLINICIAN.search(last) is None:
        return ""
    found = re.search(r"(?i)\b(?:anything|any [a-z-]+)\b(.*?)\b(?:needs?|should be|is worth|wants)\b",
                      last)
    if found is None:
        return ""
    clause = found.group(1).strip(" ,;:-")
    if "," not in clause and " or " not in clause:
        return ""
    words = clause.split()
    if not 2 <= len(words) <= 26:
        return ""
    return clause

def _after_the_if(sentence):
    opens = re.match(r"(?:so )?if ", sentence, re.I)
    if opens:
        when = sentence[opens.end():]
        when = re.split(r"(?:^|, |; | and | then | so )(?:and )?(?:get|see|ring|call|take|go|"
                        r"book|treat|watch|keep|check|apply|cover|use|rest|ice|put|give|try|"
                        r"test|monitor|stop|unplug|switch|leave|turn|have|ask|phone|contact|"
                        r"speak|mention)\b", when)[0]
    else:
        at = sentence.find(" if ")
        if at < 0:
            return ""
        when = sentence[at + 4:].rstrip(" .")
        when = re.split(r"(?:^|, | and | then )(?:and )?(?:get|see|ring|call|take|go|book|"
                        r"treat|watch|keep|check|apply|cover|use|rest|ice|put|give|try|test|"
                        r"monitor|have|ask|phone|contact|speak|mention)\b", when)[0]
    when = RESTATED.split(when)[0]
    when = _no_hanging_end(when.strip(" ,."))
    return when if len(when.split()) >= 2 else ""


def _when(said):
    for sentence in re.split(r"(?<=[.!?]) ", said):
        if not REFER.search(sentence):
            continue
        opens = re.match(r"(?:so )?if ", sentence, re.I)
        if opens or _an_if_that_is_a_condition(sentence) >= 0:
            when = _after_the_if(sentence)
            if when:
                return when
            continue
        when = _a_described_condition(sentence)
        if when:
            return when
    return ""


JUDGED_REFERRAL = re.compile(
    r"\b(?:is|are|was|were) (?:a|the|your) reason to (?:ring|call|see|ask|contact|speak|get)\b"
    r"|\btake (?:it|that|this|them|him|her) (?:to|along to|back to) (?:a |your |the )?"
    r"(?:pharmacist|gp|doctor|nurse|vet|dentist|optician)\b",
    re.I,
)
STATES_A_REFERRAL = re.compile(
    r"^(?P<when>.+?)\s+(?:is|are)\s+(?:high and |low and |still )?"
    r"(?:worth|a reason to|the point (?:at which|where))\b",
    re.I,
)
NAMES_NOTHING = frozenset((
    "it", "that", "this", "they", "there", "which", "either", "one", "both", "any", "all",
    "any of that", "any of those", "any of them", "either of those", "either of them",
    "one of those", "both of those", "some of that", "all of that", "the rest", "one or both",
    "none of that", "anything", "something", "much", "most of it",
))
STATED_LONGEST = 16


def _stated_before_the_judgement(sentence):
    frame = STATES_A_REFERRAL.match(sentence)
    if frame is None:
        return ""
    when = _no_hanging_end(frame.group("when").strip(" ,;:"))
    if not 2 <= len(when.split()) <= STATED_LONGEST:
        return ""
    if when.strip(" .,").lower() in NAMES_NOTHING:
        return ""
    if NAMES_A_CLINICIAN.search(when) or when.split()[0].lower() in ("only", "just"):
        return ""
    head = when.split()[0]
    if head[:1].isupper() and (head[1:].islower() or len(head) == 1) \
            and head.lower() not in ("i", "a&e", "nhs"):
        when = when[0].lower() + when[1:]
    return when


def _stated_referral(said):
    for sentence in re.split(r"(?<=[.!?]) ", said):
        if not (JUDGED_REFERRAL.search(sentence) or DECLARATIVE_REFERRAL.search(sentence)
                or REFER.search(sentence)):
            continue
        opens = re.match(r"(?:so )?if ", sentence, re.I)
        if opens or " if " in sentence:
            when = _after_the_if(sentence)
            if when:
                when = re.sub(r"\b(or|and) if\b", r"\1", when)
                when = _no_hanging_end(re.split(r"\s+-\s+|\s+--\s+", when)[0].strip(" ,.;:"))
                when = when.split(", ask ")[0].strip(" ,.;:")
                if len(when.split()) >= 2:
                    return when, "clause"
            continue
        when = _stated_before_the_judgement(sentence)
        if when:
            return when, "noun"
    return "", ""


DOING = IMPERATIVES | frozenset((
    "run", "cool", "warm", "heat", "wipe", "spray", "scrape", "sand", "drain", "vacuum",
    "replace", "tighten", "loosen", "unscrew", "test", "brush", "scrub", "soak", "fill",
    "pour", "freeze", "thaw", "reheat", "serve", "add", "mix", "stir", "grate", "slice",
    "chop", "cover", "wrap", "store", "label", "weigh", "measure", "book", "text", "email",
    "write", "plant", "water", "prune", "feed", "repot", "keep", "hang", "place", "swap",
    "switch", "fit", "fix", "seal", "paint", "install", "bleed", "balance", "ventilate",
    "insulate", "lag", "defrost", "descale", "replace", "trim", "sweep", "mop", "hoover",
    "eat", "drink", "sleep", "nap", "walk", "stretch", "rest", "sit", "stand", "try",
))


def _danger(said):
    best = None
    for word in DANGER:
        start = said.find(word)
        while start >= 0:
            before = said[max(0, start - 14):start]
            sentence = said[max(0, said.rfind(". ", 0, start)):start]
            condition = re.search(r"\b(?:if|unless|when|once)\b", sentence)
            if not NEGATED.search(before) and not condition:
                if best is None or start < best:
                    best = start
                break
            start = said.find(word, start + len(word))
    return best


def _a_how_to(said):
    for part in AFTER.split(said)[1:] + re.split(r"(?<=[.!?]) ", said):
        for clause in re.split(r",|;| and | then | so | but ", part.strip()):
            words = clause.strip(" .:;,-").split()
            if words and words[0].lower() in DOING:
                return True
    return False




def _round_robin(pool, said):
    if not pool or not said:
        return pool
    start = sum((i + 1) * ord(c) for i, c in enumerate(said)) % len(pool)
    return tuple(pool[start:]) + tuple(pool[:start])


def _says_what_it_is(said):
    for part in AFTER.split(said)[1:] + re.split(r"(?<=[.!?]) ", said):
        for clause in re.split(r",|;| and | then | so | but |:", part.strip()):
            words = clause.strip(" .:;,-").split()
            leads = [word.lower() for word in words[:2]]
            if len(words) >= 4 and not any(word in DOING for word in leads):
                return True
    return False


LONG_SPAN = re.compile(
    r"\b(?:two|three|four|five|six|seven|eight|nine|ten|\d+)\s+(?:days?|weeks?|fortnights?)\b|"
    r"\ba\s+fortnight\b|"
    r"\b\d+\s*(?:months|years)\b|\bmonths?\b|\byears?\b|\bfor\s+(?:a\s+long|ages)\b",
    re.I)
HEDGE_SPAN = re.compile(
    r"\b(?:in|for|after|within)\s+"
    r"(?:a few|a couple of|a|an|one|two|three|four|five|six|several|\d+)?\s*"
    r"(?:days?|weeks?|fortnights?)(?:\s+or\s+(?:two|three|four))?\b|"
    r"\b(?:two|three|four|five|six|seven|\d+)\s+(?:days?|weeks?)\s+of\s+(?:it|this|that)\b|"
    r"\b(?:lasts?|lasted|lasting|continues?|continued|continuing|goes? on|gone on|drags? on|"
    r"more than|longer than|over|beyond|past)\s+"
    r"(?:a|an|one|two|three|four|five|six|seven|several|\d+)?\s*"
    r"(?:days?|weeks?|fortnights?|months?)\b",
    re.I)


def _the_line_it_answered(said, memory):
    turns = memory.get("turns") if isinstance(memory, dict) else None
    if not isinstance(turns, list) or not said:
        return ""
    for last in reversed(turns):
        if not isinstance(last, dict):
            continue
        if _flat(last.get("bot")) == _flat(said):
            return _flat(last.get("user"))
    return ""


def _past_the_timescale(said, memory):
    if not said or HEDGE_SPAN.search(said) is None:
        return False
    line = _the_line_it_answered(said, memory) or ""
    if LONG_SPAN.search(line) is None:
        line = _the_span_further_up(said, memory) or line
    ours = LONG_SPAN.search(line)
    if ours is not None and re.search(r"\b(?:days?|weeks?)\s+ago\b", line, re.I):
        ours = None
    return ours is not None


def _subject_words(text):
    return {word[:5] for word in _words(text)
            if len(word) >= 5 and word not in FENCE_FILLER}


def _the_span_further_up(said, memory):
    turns = memory.get("turns") if isinstance(memory, dict) else None
    if not isinstance(turns, list) or len(turns) < 2:
        return ""
    here = _subject_words(said)
    if not here:
        return ""
    for turn in reversed(turns[:-1]):
        if not isinstance(turn, dict):
            continue
        line = _flat(turn.get("user"))
        if LONG_SPAN.search(line) is None:
            continue
        if _subject_words(turn.get("bot")) & here:
            return line
    return ""


FENCE_FILLER = frozenset("""
a an the it its this that these those there is are was were be been being am i you your he she
they we my mine our their his her them us of to in on at for with and or but so then than if
when while as by from up out off down not no any more very still just also both either own same
other thing things way lot lots bit does do did done gets get getting goes going come comes
coming keep keeps kept start starts started stop stops stopped carry carries carried turn turns
turned become becomes became make makes made up
""".split())


def _stems(text):
    words = set()
    for word in re.findall(r"[a-z']+", _flat(text).lower()):
        word = word.strip("'")
        if len(word) < 4 or word in FENCE_FILLER:
            continue
        for suffix in ("ing", "ed", "es", "s"):
            if word.endswith(suffix) and len(word) - len(suffix) >= 4:
                word = word[: -len(suffix)]
                break
        words.add(word)
    return words


def _the_fence_is_their_own_line(said, memory):
    when = _when(said)
    if not when:
        return False
    fence = _stems(when)
    theirs = _stems(_the_line_it_answered(said, memory))
    if not fence or not theirs:
        return False
    shared = fence & theirs
    return bool(shared) and len(shared) * 2 >= len(fence)


LOSS_WORDS = re.compile(
    r"\b(?:died|dies|death|dead|funeral|cremation|burial|passed away|miscarriage|miscarried"
    r"|stillborn|bereave\w*|lost (?:the|my) baby|took (?:his|her|their) own life)\b", re.I)


MOOD = re.compile(
    r"\b(?:feel(?:ing|s|t)?\s+(?:\w+\s+){0,2}(?:low|down|flat|numb|sad|anxious|worried|stressed"
    r"|overwhelmed|lonely|rubbish|awful|miserable|hopeless|empty|knackered|exhausted)"
    r"|depress\w*|anxi\w*|panick?\w*|miserable|lonely|burnt out|burned out|burnout"
    r"|can(?:'t|t|not)? be bothered|no energy|no motivation|dont want to go out"
    r"|dont want to see anyone)\b", re.I)


def _a_mood(memory):
    return any(MOOD.search(line) for line in _the_last_person_lines(memory, 2))


def _about_a_death(memory):
    for line in _the_last_person_lines(memory, 3):
        if not LOSS_WORDS.search(line):
            continue
        if _a_thing_stopped is not None and _a_thing_stopped(line):
            continue
        return True
    return False


def _the_last_person_lines(memory, count):
    turns = memory.get("turns") if isinstance(memory, dict) else None
    if not isinstance(turns, list):
        return ()
    lines = [_flat(turn.get("user")) for turn in turns if isinstance(turn, dict)]
    return [line for line in lines if line][-count:]


ADVICE_OK_LINES = (
    "Yes - go with that. {step}",
    "That is the right first move, and it is the one I would take: {step}",
    "Go with it. {step} If it feels wrong once you are in it, say so and we can change tack.",
)
ASKED_FOR_A_CALL = re.compile(
    r"^\s*(?:so\s+|ok(?:ay)?\s+)?(?:should|shall|do you think|would you|what would you do|"
    r"is it (?:a good idea|ok|okay|wise|worth it|fine) to|is it wrong to|am i (?:ok|okay|right) to)\b")


def _a_job_to_do(text):
    for piece in re.split(r"[.!?;:]\s+| \u2014 | \u2013 | - ", _flat(text)):
        words = _WORD.findall(piece.strip(" ,-"))
        if words and words[0] in _STEP_OPENERS:
            return True
    return False


def _the_advice_itself(said):
    for sentence in re.split(r"(?<=[.!?]) ", " ".join(str(said or "").split())):
        clean = sentence.strip()
        if clean.endswith(":"):
            clean = clean[:-1].strip()
        if len(clean.split()) >= 4:
            if not _a_job_to_do(clean):
                return ""
            return clean if clean.endswith((".", "!", "?")) else clean + "."
    return ""


A_REFUSAL = re.compile(
    r"\b(?:i can(?:no|')?t\b|i cannot\b|beyond what i know|not one i can call|i don't know "
    r"enough|i would not want to guess|that is not something i can|not mine to decide|not mine "
    r"to say|not for me to (?:decide|say|call)|(?:that|this|it) is your call|up to you whether)\b",
    re.I)


def _an_ask_for_a_call(memory):
    said = _flat(_last_person_line(memory)).strip()
    return bool(said) and ASKED_FOR_A_CALL.match(said) is not None


def _a_fix_with_no_warning(said):
    if not said or len(said) < 80:
        return False
    if not _says_what_it_is(said):
        return False
    if _first(said, CARE) is not None or REFER.search(said) is not None:
        return False
    if _first(said, REASSURE) is not None or _first(said, STOP_DOING) is not None:
        return False
    return _a_how_to(said)


DIRECTED_LINES = (
    "I wouldn't call it a warning sign - the answer above is about getting it sorted, and that "
    "is the part that matters. What has you asking?",
    "Nothing in that says how serious it is. The step above is what moves it, and what would "
    "change the answer is it getting worse or going on. Where is the worry?",
    "Hard to put a scale on it. Doing the thing above is what makes the difference, so start "
    "there and tell me what is behind the question.",
)
OWED_LINES = (
    "Then it is theirs to fix rather than yours. Put it in writing, keep a copy, and note the "
    "date it started \u2014 that is the thing that turns it from your complaint into their job.",
    "That one is their job, and the date is what makes it stick. Send it in writing, keep the "
    "reply, and say when it started: anyone who has to step in later asks for that first.",
    "Keep it in writing and keep the dates. A landlord, a council or a boss who has been told in "
    "writing is a different conversation from one who has only been told.",
)
OWED = re.compile(r"\b(?:landlord|landlady|letting agent|estate agent|council|housing "
                  r"association|housing officer|boss|manager|employer|supervisor|neighbour|"
                  r"neighbor|builder|contractor|freeholder|owner|letting|lettings)\b", re.I)


def _somebody_owes_them(memory, back=3):
    turns = memory.get("turns") if isinstance(memory, dict) else None
    if not isinstance(turns, list):
        return False
    for last in turns[-back:]:
        if not isinstance(last, dict):
            continue
        line = last.get("user") or last.get("clean") or last.get("text") or ""
        if isinstance(line, str) and OWED.search(line):
            return True
    return False


def _a_reading_of_the_feeling(memory, flat):
    behind = _the_line_behind(memory)
    family = _a_feeling_of_their_own(behind)
    if not family:
        return None
    seed = behind + " " + flat + " " + str(len(memory.get("turns") or []))
    return _round_robin(FEELING_DOUBT_LINES[family], seed)[0]


def _care_pool(said):
    flat = _flat(said)
    if CARE_NOW.search(flat) is not None:
        return CARE_NOW_NORMAL
    if _first_positive(flat, SAYS_NORMAL) is not None:
        return ORDINARY_NORMAL
    if _first_positive(flat, HOW_MANY_PEOPLE) is not None:
        return CARE_NORMAL[:1]
    if _first_positive(flat, REASSURE) is not None:
        return CARE_NORMAL
    return CARE_NORMAL + CARE_NORMAL_UNKNOWABLE


def _the_knowledge_has_this(clean, memory, above):
    try:
        from .safetyask import _the_answers_have_this
    except Exception:
        return None
    card = _the_answers_have_this(clean, memory)
    if not card:
        return None
    said = _flat(card)
    opening = _flat(above)[:60]
    if opening and opening in said:
        return None
    return card


def a_check_on_the_reply(reply):
    if not reply:
        return False
    text = reply.strip()
    return any(text in {line.strip() for line in pool}
               for pool in (CHECK_WORKS_LINES, CHECK_ONCE_LINES, CHECK_WATCH_LINES,
                            CHECK_JOB_LINES))


def _an_amount_asked(flat):
    return bool(ENOUGH_ASK.match(flat) or re.search(r"\bhow (?:much|many)\b|\bamount\b|"
                                                    r"\benough\b", flat or ""))


def _the_last_thing_said_is_a_nod(memory):
    turns = memory.get("turns") if isinstance(memory, dict) else None
    if not isinstance(turns, list) or not turns:
        return False
    last = turns[-1]
    return isinstance(last, dict) and _a_punt(last)


def _a_check_on_the_method(flat, memory):
    said = _last_reply(memory, past_the_nod=True)
    if not said or not _a_how_to(said):
        return None
    behind = _flat(_last_person_line(memory) or "")
    if A_THINKING_ABOUT.search(behind) or A_DECISION_ASK.search(behind):
        return None
    if A_PLAN.search(behind):
        return None
    if _last_module(memory) != "answers":
        return None
    if _the_last_thing_said_is_a_nod(memory):
        return None
    if _an_amount_asked(flat) and _the_knowledge_has_this(flat, memory, said):
        return None
    if not _about_a_body(behind):
        pool = CHECK_JOB_LINES
    else:
        warns = (REFER.search(said) is not None or NAMES_A_CLINICIAN.search(said) is not None
                 or _first(said.split(), STOP_DOING) is not None)
        if warns:
            pool = CHECK_WATCH_LINES
        elif A_LENGTH_IN_THE_ANSWER.search(_flat(said)):
            pool = CHECK_WORKS_LINES
        else:
            pool = CHECK_ONCE_LINES
    return pick(_round_robin(pool, flat + " " + said), memory, said)


A_DOUBT_ABOUT_THE_THING = re.compile(
    r"\b(?:safe|safely|unsafe|dangerous|danger|ok|okay|fine|risky|risk|bad|wrong|worried|"
    r"worry|worrying|problem|normal|harm|harmful)\b"
    r"|\b(?:can|could|may|should) i (?:still |even )?(?:use|keep using|leave|carry on using)\b")


def reply_for(clean, memory):
    flat = _flat(clean).strip(" .!?")
    from . import safetyask

    if (safetyask.the_bot_already_ruled(memory) and A_DOUBT_ABOUT_THE_THING.search(flat)
            and not any(word in flat for word in safetyask.A_RULING_ALREADY)):
        return pick(safetyask.A_SAFETY_ALREADY_RULED, memory, flat)
    if A_CHECK_ON_A_PLAN.match(flat):
        plan = _the_plan_they_brought(memory)
        if plan:
            return pick(_round_robin(A_CHECK_ON_A_PLAN_LINES, plan), memory, plan)
    if METHOD_DOUBT.match(flat):
        behind = _last_reply(memory, past_the_nod=True)
        line = _the_line_behind(memory)
        written, spoken = _as_written(line)
        if (not behind or not _a_how_to(behind)
                or not (A_HOW_TO_ASK.search(line) or A_HOW_TO_ASK.search(written)
                        or A_HOW_TO_ASK.search(spoken))):
            return _a_check_on_the_method(flat, memory)
        if _danger(behind) is not None:
            return None
        if REFER.search(behind) is not None or NAMES_A_CLINICIAN.search(behind) is not None:
            return _a_check_on_the_method(flat, memory)
        checked = _a_check_on_the_method(flat, memory)
        if checked:
            return checked
        return pick(_round_robin(METHOD_OK_LINES, behind), memory, behind)
    if A_FIGURE_ASK.match(flat):
        figure_line = _the_line_behind(memory)
        figure_said = _last_reply(memory, past_the_nod=True)
        if figure_line and _a_figure_owed(figure_line) and figure_said:
            if _first(figure_said, A_COMPARISON) is not None:
                return pick(MONEY_LINES, memory, figure_said)
            if A_FIGURE.search(figure_said):
                return pick(FIGURE_LINES, memory, figure_said)
        return None
    enough_ask = bool(ENOUGH_ASK.match(flat))
    if not BARE.match(flat) and not enough_ask:
        if A_CHECK_ASK.search(flat):
            return _a_check_on_the_method(flat, memory)
        return None
    normal_ask = bool(ASKS_NORMAL.search(flat))
    ok_ask = not normal_ask and bool(ASKS_OK.search(flat))
    said = _last_reply(memory, past_the_nod=True)
    plan = _the_line_behind(memory)
    family = _the_plan_can_hurt(_flat(plan))
    if family:
        warned = _the_answer_already_warned(_flat(said))
        if warned:
            return "Go with the answer above rather than around it: " + warned
        return pick(_round_robin(THE_PLAN_CAN_HURT_LINES[family], _flat(plan)), memory,
                    _flat(plan))
    if _about_a_death(memory) and _last_module(memory):
        return pick(_round_robin(GRIEF_FLOOR_LINES, _the_line_it_answered(said, memory) or flat),
                    memory, flat)
    if enough_ask:
        stated = _said_enough(said)
        if stated is None:
            if _last_module(memory) == "answers":
                checked = _a_check_on_the_method(flat, memory)
                if checked:
                    return checked
            return None
        return pick(_round_robin(ENOUGH_STATED_LINES, said + " " + flat), memory,
                    said).replace("{yes}", stated)
    if _considering(memory) or A_PLAN.search(_flat(_the_line_behind(memory))):
        return _a_plan_doubt(memory)
    worst = _the_worst_thing_they_said(memory)
    if worst and SYMPATHY.search(_flat(said)):
        seed = worst + " " + flat + " " + str(len(memory.get("turns") or []))
        return _round_robin(HARD_NEWS_LINES, seed)[0]
    money = _a_doubt_about_money(memory)
    if money and _last_module(memory, past_the_nod=True) in ("answers", "chat", "greeting",
                                                             "trouble"):
        if (not _about_a_death(memory) and not _the_worst_thing_they_said(memory)
                and not (_A_NUMBER.search(money) and _is_a_comparison(said))):
            return pick(_round_robin(MONEY_TROUBLE_LINES, said or money), memory, said or money)
    if not said or _last_module(memory, past_the_nod=True) != "answers":
        reading = _a_reading_of_the_feeling(memory, flat)
        if reading:
            return reading
        if HELPED.search(_flat(_last_person_line(memory))):
            return pick(_round_robin(HELPED_LINES, _flat(_last_person_line(memory))), memory,
                        _flat(_last_person_line(memory)))
        named = _last_line_that_named_a_call(memory)
        if named:
            if _a_call_for_now(named):
                call = _the_call_sentence(named)
                seed = flat + " " + call
                if call and URGENT_CALL.search(call):
                    return pick(_round_robin(YES_SAID_LINES, call), memory, seed)
                if TRADE.search(named) is None:
                    return pick(YES_LINES[:2], memory, flat)
                return pick(SOON_LINES, memory, flat)
            when = _when(named)
            if when:
                return pick(CONDITION_LINES, memory, flat).replace("{when}", when)
        if WORRIED_ASK.match(flat):
            return None
        if _last_module(memory) in ("chat", "greeting", "trouble"):
            reading = _a_reading_of_the_feeling(memory, flat)
            if reading:
                return reading
            if _own_doing(memory) and _a_mood(memory):
                return pick(_round_robin(BACKSTOP_LINES, said), memory, said)
            step = _the_advice_itself(said)
            if step and _an_ask_for_a_call(memory) and not A_REFUSAL.search(said):
                return pick(_round_robin(ADVICE_OK_LINES, said), memory, said).replace(
                    "{step}", step)
            if _own_doing(memory) and _a_fix_with_no_warning(said):
                return pick(_round_robin(NOTHING_WARNED_LINES, said), memory, said)
            if _own_doing(memory) and not _nothing_to_be_long_about(memory):
                return pick(_round_robin(FLOOR_LINES, said), memory, said)
            if _about_the_person(memory) and not _nothing_to_be_long_about(memory):
                return pick(_round_robin(NEUTRAL_ASK_LINES, said), memory, said)
            if _the_floor_asked_them_something(memory):
                return pick(_round_robin(ASKED_THEM_LINES, said + " " + flat), memory,
                            said + " " + flat)
        return _a_plan_doubt(memory)
    if WHEN_ASK.match(flat) or WORRYING_ASK.match(flat):
        when = (_when(said) or _the_list_before_the_call(said)
                or _stated_referral(said)[0])
        if when:
            return pick(WHEN_LINES, memory, flat).replace("{when}", when)
        call = _the_call_and_its_reason(said)
        if call and _they_named_the_sign_themselves(call, memory):
            call = ""
        if call:
            return pick(WHEN_CALL_LINES, memory, flat).replace("{when}", call)
        if WORRYING_ASK.match(flat):
            return None
    if _the_last_line_was_mine(memory) and OWN_PATTERN.search(_flat(said)):
        return pick(AGAIN, memory, flat)
    if any(line.lower() in _flat(said) for line in
           NO_LINES + DO_LINES + YES_LINES + ORDINARY_NORMAL + CARE_NORMAL
           + CARE_NORMAL_UNKNOWABLE + CARE_NOW_NORMAL + DO_NORMAL):
        return pick(AGAIN, memory, flat)
    if _first(said, AGAIN) is not None:
        return None
    if _a_person_they_know(memory, said):
        if _when(said) or REFER.search(said) is not None:
            return pick(PERSON_CALL, memory, flat + " " + _the_line_behind(memory))
        return pick(PERSON_ORDINARY, memory, flat + " " + _the_line_behind(memory))
    opening = _opening(said)
    thing = _a_thing_they_own(memory)
    yes_pool = THING_CALL if thing else YES_LINES
    action, tested = _a_throw_away(opening)
    if action is not None:
        pool = TEST_LINES if tested and not _the_person_gave_the_sign(memory, clean) else THROW_AWAY_LINES
        return pick(pool, memory, opening + " " + _the_person_line(memory, clean)).replace("{Action}", action)
    no_stated = _said_no(said)
    if no_stated is not None:
        return pick(_round_robin(NO_STATED_LINES, said + " " + flat), memory,
                    said).replace("{no}", no_stated)
    care = _referral(said)
    ordinary = _first_positive(opening, REASSURE)
    anywhere = care
    if _first(opening, STOP_DOING) is not None:
        return pick(_care_pool(said) if normal_ask else (THING_CALL if thing else YES_LINES[:2]),
                    memory, flat)
    when = _when(said)
    if when == "" and _danger(said) is not None:
        return pick(_care_pool(said) if normal_ask else (THING_CALL if thing else YES_LINES[:2]),
                    memory, flat)
    line = _the_line_behind(memory)
    written, spoken = _as_written(line)
    warns = (REFER.search(said) is not None or NAMES_A_CLINICIAN.search(said) is not None
             or _first(opening, STOP_DOING) is not None)
    if SAID_YES.search(_flat(said)) and _a_how_to(said) and not warns:
        return pick(_round_robin(METHOD_OK_LINES, said), memory, said)
    if ((A_HOW_TO_ASK.search(line) or A_HOW_TO_ASK.search(written)
         or A_HOW_TO_ASK.search(spoken))
            and _a_how_to(said) and not warns):
        return pick(_round_robin(METHOD_OK_LINES, said), memory, said)
    if A_PLAN.search(line) or A_PLAN.search(written) or A_PLAN.search(spoken):
        return _a_plan_doubt(memory)
    if (A_DECISION_ASK.search(line) or A_DECISION_ASK.search(written)
            or A_DECISION_ASK.search(spoken)):
        if ASKS_FINE.search(flat) and not ASKS_WRONG.search(flat):
            return pick(_round_robin(CHOICE_OK_LINES, line + " " + said), memory,
                        line + " " + said)
        opening = _opening(said)
        first_said = re.split(r"(?<=[.!?]) ", str(said or "").strip())[0]
        if (not warns or (_referral(first_said) is None
                          and NAMES_A_CLINICIAN.search(first_said) is None
                          and REFER.search(first_said) is None)):
            fenced = _condition_after_care(said, _first(str(said or "").lower(), CARE))
            if fenced:
                return pick(CONDITION_NORMAL if normal_ask else CONDITION_LINES,
                            memory, flat).replace("{when}", fenced)
            stated, kind = _stated_referral(said)
            sentence = _the_referral_sentence(said)
            if (stated and kind == "noun" and not TIME_NOW.search(sentence)
                    and not COMPARATIVE.search(sentence)
                    and not _the_line_is_the_threshold(
                        stated, _the_line_it_answered(said, memory))):
                if _past_the_timescale(said, memory):
                    return pick(_round_robin(MET_LINES, said), memory, said)
                return _say(SEE_STATED_LINES, memory, flat, when=stated)
            return None
        if _care_for_now(first_said):
            return pick(YES_SAID_LINES if URGENT_CALL.search(first_said) else SOON_LINES,
                        memory, flat)

        return None

    if JUST_AGE.search(flat):
        return pick(AGE_LINES, memory, said)
    if _a_figure_owed(line) and (_is_a_comparison(said)):
        return pick(MONEY_LINES, memory, said)
    care_at = _first(str(said or "").lower(), CARE)
    if care is not None and (care_at is None or care < care_at):
        care_at = care
    if _past_the_timescale(said, memory):
        return pick(_round_robin(MET_LINES, said), memory, said)
    if care_at is not None:
        fenced = _condition_after_care(said, care_at, memory)
        if fenced:
            return pick(CONDITION_NORMAL if normal_ask else CONDITION_LINES,
                        memory, flat).replace("{when}", fenced)
    denies = _first(opening, DENIES)
    if care is not None and (ordinary is None or care < ordinary
                             or _a_plain_go(care, said)):
        return pick(_care_pool(said) if normal_ask else yes_pool, memory, flat)
    if care is not None and (ordinary is None or care < ordinary):
        return pick(YES_LINES, memory, flat)
    if denies is None and anywhere is not None and ordinary is not None:
        return pick(_care_pool(said) if normal_ask else yes_pool, memory, flat)
    if ordinary is not None:
        if when and normal_ask:
            return pick(CONDITION_NORMAL, memory, flat).replace("{when}", when)
        if normal_ask and _first_positive(opening, SAYS_NORMAL) is None and _a_how_to(said):
            return pick(_round_robin(NOTHING_WARNED_NORMAL, said), memory, said)
        if _care_for_now(said):
            return pick(BOTH_LINES, memory, flat)
        fence = _a_judgement_fence(said)
        if fence:
            return pick(CONDITION_LINES, memory, flat).replace("{when}", fence)
        if warns and not _when(said) and _referral_about_the_thing(said, _the_line_behind(memory)):
            return pick(SEE_ANYWAY_LINES, memory, flat)
        if thing and not normal_ask:
            return pick(THING_ORDINARY, memory, flat + " " + thing)
        return pick(ORDINARY_NORMAL if normal_ask else (OK_LINES if ok_ask else NO_LINES),
                    memory, flat)
    when = _when(said)
    if when:
        if _the_fence_is_their_own_line(said, memory):
            if _a_call_for_now(said):
                return pick(YES_LINES, memory, flat)
            return pick(_round_robin(MET_CONDITION_LINES, said), memory, said)
        return pick(CONDITION_NORMAL if normal_ask else CONDITION_LINES,
                    memory, flat).replace("{when}", when)
    if care is not None or anywhere is not None:
        return pick(DO_NORMAL if normal_ask else DO_LINES, memory, flat)
    if _first(opening, CARE) is not None:
        if _first(opening, PEOPLE_CARE) is not None:
            return pick(YES_LINES, memory, flat)
        return pick(DO_NORMAL if normal_ask else DO_LINES, memory, flat)
    if _a_fix_with_no_warning(said):
        if _somebody_owes_them(memory):
            return pick(_round_robin(OWED_LINES, said), memory, said)
        pool = NOTHING_WARNED_NORMAL if normal_ask else NOTHING_WARNED_LINES
        return pick(_round_robin(pool, said), memory, said)
    if _an_instruction_and_nothing_else(said, memory):
        referral = _the_referral_it_closed_on(said)
        if referral:
            kept = _the_range_it_gave(said)
            said_back = referral + (f" {kept}" if kept else "")
            return pick(_round_robin(HANDED_BACK_LINES, said + " " + flat),
                        memory, said + " " + flat).replace("{referral}", said_back)
        return pick(_round_robin(DIRECTED_LINES, said + " " + flat), memory, said + " " + flat)
    return None


HANDED_BACK_LINES = (
    "That is worth acting on rather than watching: {referral}",
    "It needs sorting rather than waiting: {referral}",
    "Not one to sit on: {referral}",
)

_A_RANGE_OF_ITS_OWN = re.compile(
    r"\b(?:between|from) (\d+(?:\.\d+)?) (?:and|to) (\d+(?:\.\d+)?) ?([a-z]{2,10})\b", re.I)


_A_REFERRAL_OUT = re.compile(
    r"\b(?:get|have|call|ring|book) (?:a |an |your |the )?"
    r"(?:(?!and\b|or\b|to\b|it\b)[a-z-]+ ){0,3}"
    r"(?:engineer|plumber|electrician|mechanic|technician|specialist|someone) ?(?:out|round|in)\b",
    re.I)
_A_STOP = re.compile(r"\b(?:stop|don't|dont|do not) (?:[a-z]+ing|it|using it|driving|eating)\b",
                     re.I)


def _the_referral_it_closed_on(said):
    sentences = [s.strip() for s in re.split(r"(?<=[.!?]) +", _flat(said)) if s.strip()]
    if not sentences:
        return ""
    last = sentences[-1]
    if len(last.split()) < 5:
        return ""
    if not (REFER.search(last) or _A_REFERRAL_OUT.search(last) or _A_STOP.search(last)
            or _first(last, STOP_DOING) is not None):
        return ""
    unfenced = re.sub(r"^(?:but )?(?:if|once|when|whenever) [^,]{0,70}, ", "", last, flags=re.I)
    act = re.sub(r"^(?:stop|don't|dont|do not) [^,]{0,40}?,? (?:and|but) ", "", unfenced, flags=re.I)
    if len(act.split()) >= 4:
        return act
    return unfenced if len(unfenced.split()) >= 4 else last


def _the_range_it_gave(said):
    found = _A_RANGE_OF_ITS_OWN.search(_flat(said))
    if not found:
        return ""
    low, high, unit = found.group(1), found.group(2), found.group(3)
    if unit.lower() in ("and", "the", "for", "with"):
        return ""
    return f"Keep it between {low} and {high} {unit} in the meantime."


_STEP_OPENERS = DOING | frozenset(("say", "deal", "mention", "flag", "chase", "push", "insist"))


def _an_instruction_and_nothing_else(said, memory):
    flat = _flat(said)
    if len(flat.split()) < 12:
        return False
    head = re.split(r"[:;.!?]", flat, 1)[0].strip(" ,-")
    words = _WORD.findall(head)
    if not words or words[0].lower() not in _STEP_OPENERS:
        return False
    line = _flat(_last_person_line(memory))
    if not line or A_HOW_TO_ASK.search(line):
        return False
    return True


ASKED_THEM_LINES = (
    "Nothing you have told me makes it bad or fine on its own - that depends on how much it is "
    "getting to you. What is the bit that worries you most?",
    "No verdict from me on that one yet. Say what has you asking and I will tell you whether it "
    "is worth doing something about.",
    "That depends on something I have not heard yet. What is it that has you wondering?",
)


A_WORRY_IN_THE_LINE = re.compile(
    r"\b(?:keeps?|kept|wont|won't|refuses?|never|won't stop|hate|hates|hated|awful|horrible|"
    r"rude|nasty|unfair|upset|angry|annoyed|miserable|cry|crying|cried|stress|stressed|"
    r"worried|worry|worries|exhausted|knackered|drained|tired|hits?|hit me|shouts?|shouting|"
    r"yells?|yelling|ignores?|ignoring|off with|weird|odd|wrong|problem|falling out|fell out|"
    r"argument|arguing|argue|fights?|fighting|bully|bullied|bullying|debt|debts|skint|broke|"
    r"struggling|struggle|too much|fed up|sick of|dreading|scared|afraid|lonely|alone|"
    r"not talking|stopped talking|on top of me|getting on top|cant cope|can't cope|coping|"
    r"breaking point|drowning|shattered|rough week|bad week|a lot on|driving me|drives me|"
    r"nightmare|cant stand|can't stand|nagging|bossy|unbearable|hell|temper|disrespectful|"
    r"mean to me|picking on me|picks on me)\b",
    re.I)


_AN_OFFER = re.compile(
    r"\b(?:if you want|if it helps|i can help|happy to help|tell me more|say more|"
    r"i'm listening|i am listening|want to talk|would you like|do you want)\b", re.I)


def _the_floor_asked_them_something(memory):
    turns = memory.get("turns") if isinstance(memory, dict) else None
    if not isinstance(turns, list) or not turns:
        return False
    last = turns[-1]
    if not isinstance(last, dict):
        return False
    said = " ".join(str(last.get("bot") or "").split())
    if not (said.endswith("?") or _AN_OFFER.search(said)):
        return False
    line = _flat(_the_line_behind(memory))
    if not line or A_HOW_TO_ASK.search(line):
        return False
    return A_WORRY_IN_THE_LINE.search(line) is not None


def _a_feeling_of_their_own(line):
    words = [w.replace("'", "").lower() for w in re.findall(r"[A-Za-z']+", line or "")]
    if not words or len(words) > 14:
        return ""
    if words[0] not in ("i", "im", "ive", "id"):
        return ""
    if any(word in BODY_WORD for word in words) or any(word in SOMEONE_ELSE for word in words):
        return ""
    for word in words:
        if word in FEELING_FAMILY:
            return FEELING_FAMILY[word]
    return ""


HAND_OVER_WORDS = 42


def _the_other_thing_in_the_answer(said, step, memory):
    from ..memory.topics import RED_FLAG
    needle = " ".join(str(step or "").split()).lower().strip(" .!?,")
    mine = _flat(said)
    seen = [_flat(turn.get("bot") or "") for turn in
            ((memory.get("turns") if isinstance(memory, dict) else None) or [])
            if isinstance(turn, dict)]
    earlier = [heard for heard in seen[:-1] if heard and heard != mine]
    sentences = [one for one in re.split(r"(?<=[.!?]) ", str(said or ""))]
    starts = [i for i, one in enumerate(sentences)
              if needle and needle in one.lower().strip(" .!?,")]
    for sentence in sentences[starts[0] + 1 if starts else 1:]:
        text = " ".join(sentence.split()).strip()
        if len(text.split()) < 6 or _is_a_question(text):
            continue
        if needle and needle in text.lower():
            continue
        if RED_FLAG.match(text):
            continue
        if ASKS_THEM.match(text):
            continue
        if any(text.lower() in heard for heard in earlier):
            continue
        return text
    return ""


def _step_sentence(said, step):
    needle = " ".join(str(step or "").split()).lower().strip(" .!?,")
    if not needle:
        return ""
    for sentence in re.split(r"(?<=[.!?]) ", str(said or "")):
        text = " ".join(sentence.split())
        if needle and needle in text.lower():
            return text.strip(" .!?")
    return ""


def _up_to_a_break(said, step, within):
    words = str(said or "").split()
    if len(words) <= within:
        return said
    opening = " ".join(words).lower().find(" ".join(str(step or "").split()).lower())
    start = len(" ".join(words)[:opening].split()) if opening > 0 else 0
    if start and start < len(words) - 1:
        said = " ".join(words[start:])
        words = said.split()
        if len(words) <= within:
            return said
    best = ""
    for found in re.finditer(r"[,;:]|\s[-\u2013\u2014]\s", str(said or "")):
        head = str(said or "")[:found.start()].strip(" ,;:-\u2013\u2014")
        if len(head.split()) <= within and len(head.split()) > len(best.split()):
            best = head
    return best or " ".join(words[:within])


def _an_instruction_sentence(said):
    from ..memory.topics import RED_FLAG
    for sentence in re.split(r"(?<=[.!?]) ", str(said or "")):
        text = " ".join(sentence.split())
        if not text or CONDITIONAL_OPEN.match(text) or RED_FLAG.match(text) or _is_a_question(text):
            continue
        if A_STATEMENT.match(text):
            continue
        if _doing_word(re.findall(r"[A-Za-z'’-]+", text)[:5]) in IMPERATIVES:
            return text.strip(" .!?")
        head, colon, tail = text.partition(": ")
        if colon and tail and (_doing_word(re.findall(r"[A-Za-z'’-]+", tail)[:5])
                               in IMPERATIVES):
            return text.strip(" .!?")
        if FIRST_ITSELF.search(text) and not COPULA.match(text) and len(text.split()) >= 5:
            return text.strip(" .!?")
    return ""


def _the_answer_under_a_frame(memory):
    turns = memory.get("turns") if isinstance(memory, dict) else None
    if not isinstance(turns, list) or not turns or not isinstance(turns[-1], dict):
        return ""
    last = turns[-1]
    if last.get("module") in UNREADABLE:
        return ""
    return again_reply.unframed(last.get("bot")) or ""



FRONT_LEAD = frozenset(("a", "an", "the", "my", "your", "our", "their", "his", "her", "its",
                        "one"))
FRONT_THIS = frozenset(("it", "that", "this", "they", "these", "those", "there"))
FRONT_WHEN = frozenset(("when", "if", "once", "unless", "whenever", "till", "until"))
FRONT_SUBJECT_WORDS = 2


def _the_front_names_what_is_in_hand(head, line, memory):
    words = re.findall(r"[A-Za-z'’-]+", str(head or "").lower())
    if any(word in FRONT_WHEN for word in words):
        return False
    if words and words[0] in FRONT_THIS:
        return True
    subject = [word for word in words if word not in FRONT_LEAD][:FRONT_SUBJECT_WORDS]
    if not subject:
        return False
    in_hand = set(re.findall(r"[a-z'’-]+", str(line or "").lower()))
    for part in (memory or {},) if isinstance(memory, dict) else ():
        for topic in [part.get("topic")] + list(part.get("topics") or []):
            if isinstance(topic, dict):
                in_hand.update(str(word) for word in topic.get("words") or ())
        for turn in part.get("turns") or []:
            if isinstance(turn, dict):
                in_hand.update(re.findall(r"[a-z'’-]+", str(turn.get("user") or "").lower()))
    for word in subject:
        if word in in_hand:
            return True
    return False


def next_step(clean, memory):
    flat = _flat(clean).strip(" .!?")
    bare = bool(STEP.match(flat))
    someone_new = (memory.get("understood") or {}).get("someone_new") \
        if isinstance(memory, dict) else None
    asks_step = bare or (bool(SPEAK_UP.match(flat)) and not someone_new)
    asks_who = bool(SEE.match(flat))
    plea = bool(TIPS_AGAIN.match(flat) or ONE_THING.match(flat))
    tips = bool(TIPS_AGAIN.match(flat))
    how_to = HOW_TO.match(flat)
    how_to_asked = bool(how_to) and (
        how_to.group("doing") in DOING_WITH_NO_OBJECT
        or (how_to.group("obj") and how_to.group("doing") not in KNOWING_DOING))
    if how_to_asked:
        asks_step = True
    if plea and _last_module(memory) == "answers":
        asks_step = True
    if A_HOW_ASK.match(flat) and _last_module(memory) == "answers":
        asks_step = True
    if not (asks_step or asks_who):
        return None
    said = _last_reply(memory, past_the_verdict=True) or _the_answer_under_a_frame(memory)
    if not said:
        return None
    if _first(said, AGAIN) is not None:
        said = again_reply.unframed(said)
        if not said:
            return None
    if EMERGENCY_CALL.match(said.strip()):
        return None
    when = _when(said)
    if asks_who:
        if when:
            return _say(SEE_NOW_LINES, memory, flat, when=when)
        stated, kind = _stated_referral(said)
        if stated:
            pool = SEE_NOW_LINES if kind == "clause" else SEE_STATED_LINES
            return _say(pool, memory, flat, when=stated)
        if REFER.search(said):
            return pick(SEE_ANYWAY_LINES, memory, flat)
        if _first(said, CARE) is not None:
            return pick(SEE_NONE_LINES, memory, flat)
        return None
    step = _step(said)
    if not step and _ends_on_a_question(said):
        step = _step(_the_answer_before_that(memory))
    if step and _echoes_the_person(step, memory):
        step = None
    if tips:
        other = _the_other_thing_in_the_answer(said, step, memory)
        if other:
            return _say(ALSO_LINES, memory, flat, other=other)
        if not step:
            return pick(STEP_KEPT_LINES, memory, flat)
    if step and (_already_asked_for_a_step(memory)
                 or _most_of_the_line(step, _the_line_just_given(memory))
                 or tips):
        return pick(STEP_KEPT_LINES, memory, flat)
    if not step:
        if _an_offer_is_waiting(said):
            return None
        if bare and _ends_on_a_question(said):
            if _the_news_just_before(memory):
                return None
            asked = _the_question_asked(said)
            if asked and THE_PLEA.match(flat):
                return pick(QUESTION_BACK_LINES, memory, flat)
            if asked and _after_a_comfort_line(memory):
                return pick(QUESTION_BACK_LINES, memory, flat)
            if asked and AN_OFFER.search(asked):
                return pick(OFFER_TAKEN_LINES, memory, flat)
            if asked:
                return _say(ASKED_FIRST_LINES, memory, flat, q=asked)
            return pick(QUESTION_BACK_LINES, memory, flat)
        listed = _listed(said)
        if listed:
            return _say(LIST_STEP_LINES, memory, flat, step=listed)
        if when and not plea and _action_count(said) < 2:
            return pick(NOTHING_LINES, memory, flat).replace("{when}", when)
        if ONE_THING.match(flat) and _last_module(memory) == "answers":
            move = _an_instruction_sentence(said)
            if move:
                head = move.partition(": ")[0].strip(" .;:,-")
                if ": " in move and len(head.split()) >= 8:
                    move = head
                elif len(move.split()) > HAND_OVER_WORDS:
                    move = _first_clause(move).strip(" .;:,-") or move
                return _say(ONE_TURN_PLAIN_LINES, memory, flat, step=move)
            return _say(ALL_OF_IT_LINES, memory, flat)
        return None
    if step.lower().endswith(" first"):
        step = step[: -len(" first")].rstrip()
    if ONE_THING.match(flat):
        whole = _step_sentence(said, step)
        piece = _up_to_a_break(whole, step, HAND_OVER_WORDS) if whole else ""
        if len(piece.split()) > len(step.split()):
            return _say(ONE_TURN_PLAIN_LINES, memory, flat, step=piece)
        pool = ONE_TURN_PLAIN_LINES if (": " in step or FIRST_ITSELF.search(step)) else ONE_TURN_LINES
        return _say(pool, memory, flat, step=step)
    if how_to_asked:
        whole = _step_sentence(said, step)
        if whole and len(whole.split()) > len(step.split()):
            step = whole
        head, colon, tail = step.partition(": ")
        if (colon and tail and _doing_word(re.findall(r"[A-Za-z'’-]+", head)) not in IMPERATIVES
                and _the_front_names_what_is_in_hand(head, flat, memory)):
            step = tail.strip()
    if FIRST_ITSELF.search(step):
        return _say(STEP_ALREADY_FIRST_LINES, memory, flat, step=step)
    if ": " in step or len(step.split()) >= STEP_LONG:
        return _say(STEP_DETAIL_LINES, memory, flat, step=step)
    if _action_count(said) > 1:
        pool = STEP_ALREADY_FIRST_LINES if FIRST_ITSELF.search(step) else STEP_LINES
        if how_to_asked:
            pool = STEP_DETAIL_LINES
        return _say(pool, memory, flat, step=step)
    return _say(STEP_ONE_LINES, memory, flat, step=step)
