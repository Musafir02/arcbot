import re

from ..compose import fallback as _fallback
from ..compose.fallback_data import CRISIS_BETTER_THEM, CRISIS_WORDS

PRIORITY = -998

ANSWERS_INSTEAD = ("abuse", "carers", "safety")

ROUTE_NAMED = re.compile(
    r"\b(?:999|911|112|111|a\s?&\s?e|a and e|accident and emergency|ambulance|paramedic|"
    r"urgent care|out of hours|x-ray)\b")

THEY_ARE_EASING = re.compile(
    r"\b(?:he|she|they|dad|mum|mom|nan|gran|granny|grandma|grandad|grandpa|son|daughter|"
    r"husband|wife|partner|brother|sister|baby|kid|child|boy|girl|little one|friend|neighbour)"
    r"(?:'s|s| is| are| was| were| has| had)?\b\s+"
    r"(?:(?:come|came|coming)\s+(?:round|to|back round|back to)\b"
    r"|(?:awake|conscious|alert|with it|responsive|breathing (?:ok|okay|normally|fine|easier|"
    r"better|properly))\b"
    r"|(?:sat|sitting) up\b"
    r"|(?:talking|chatting|eating|drinking) (?:now|again)\b"
    r"|(?:asleep|sleeping|snoozing|dozing|resting)\b"
    r"|(?:up and about|on the mend|out of the woods|over the worst)\b)")
EASING_UNDONE = re.compile(
    r"\b(?:confus\w*|not (?:making sense|himself|herself|themselves|with it|right)|"
    r"blue|grey|gray|pale|clammy|shaking|shaky|dizzy|feverish|burning up|bleeding|sick|"
    r"vomit\w*|wont wake|won't wake|cant wake|can't wake|unresponsive|limp|floppy|slurr\w*|"
    r"breathing (?:oddly|strangely|badly|funny))\b")
THEM_ASKING = re.compile(
    r"^(?:is|are|was|were|has|have|had|did|does|do|will|would|can|could|should|shall|any)\b")
EASING_NOT_ONE = re.compile(
    r"\b(?:not|isnt|isn't|arent|aren't|wasnt|wasn't|wont|won't|cant|can't|couldnt|didnt|doesnt|"
    r"hasnt|havent|still|worse|but|except|though|shaking|shaky|confused|blue|grey|pale|burning|"
    r"hot|fever|bleeding|sick|vomit\w*|dizzy|gone)\b|\?")
MOVE_ON = re.compile(
    r"\b(?:anyway|what about|how about|what if|should i|shall i|do i|can i|im going to|"
    r"ill (?:go|ring|call|take)|what do i (?:do|say))\b")

THEY_SAY_ITS_FINE = re.compile(
    r"\b(?:says?|said|telling|tells?|told|insists?|insisted|reckons?|thinks?|swears?|"
    r"claims?|assures?|keeping\s+on\s+about|keeps?\s+saying)\b[^.!?]{0,26}?"
    r"\b(?:its|it's|hes|he's|shes|she's|theyre|they're|im|i'm)\b\s*"
    r"(?:nothing|fine|ok|okay|alright|all\s+right|not\s+(?:that|too|so)\s+bad|no\s+big\s+deal|"
    r"nothing\s+to\s+worry\s+about|just|only|a\s+bit|a\s+little|bruis\w*|"
    r"a\s+scratch|a\s+bump)\b"
    r"|\b(?:told|asked|telling|asking|begged)\s+me\s+not\s+to\s+(?:worry|fuss|make\s+a\s+fuss|"
    r"bother|think\s+about\s+it)\b"
    r"|\b(?:said|says|told\s+me|kept\s+saying|keeps?\s+saying)\s+nothing\s+(?:to\s+worry|"
    r"was\s+wrong|is\s+wrong|wrong)\b")

_MONTHS = (r"(?:\d+|a|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|"
           r"a\s+few|several)\s+(?:days?|weeks?|months?|years?)")
THEY_ARE_RECOVERING = re.compile(
    r"\b(?:sober|clean|dry|straight|drugs?[- ]?free|off\s+(?:it|the\s+drink|the\s+booze)|"
    r"self[- ]harm\s+free)"
    r"\b[\w\s,'-]{0,14}?\b" + _MONTHS +
    r"|\b" + _MONTHS + r"\s+(?:sober|clean|dry)\b"
    r"|\b(?:hasnt|has\s+not|havent|have\s+not|hadnt)\s+"
    r"(?:touched|used|drunk|drank|self[- ]harmed|cut|relapsed)\b[\w\s,'-]{0,14}?\b"
    r"(?:in|for)\s+" + _MONTHS)

ABUSE_ANSWER = re.compile(
    r"domestic abuse|abuse helpline|0808 2000 247|1-800-799-7233|"
    r"what's happening to you is abuse|what is happening to you is abuse")
ABUSER_ANSWER = re.compile(
    r"0808 802 4040|people\s+who\s+are\s+violent|hitting\s+someone\s+you\s+live\s+with\s+is\s+"
    r"abuse|that\s+is\s+abuse,\s+and")
THE_APOLOGY = re.compile(
    r"\b(?:sorry|apolog\w+|wont\s+happen\s+again|won't\s+happen\s+again|"
    r"promis(?:e|ed|es)|will\s+change|has\s+changed|is\s+changing|getting\s+help|"
    r"doing\s+something\s+about\s+it|didn'?t\s+mean|didnt\s+mean|not\s+like\s+(?:him|her|that)|"
    r"only\s+did\s+it\s+once)\b")
THE_KINDNESS = re.compile(
    r"(?:says|said|told\s+me)\s+(?:that\s+)?(?:he|she)\s+loves\s+me|"
    r"(?:he|she)\s+loves\s+me\s+really|bought\s+me|flowers|"
    r"being\s+(?:really\s+)?(?:nice|sweet|lovely)\s+now|making\s+up\s+for\s+it|"
    r"only\s+does\s+it\s+when|been\s+(?:really\s+)?(?:good|lovely)\s+(?:since|this\s+week)")
THE_DRINK = re.compile(
    r"\b(?:was|were|is|gets?|been)\s+(?:drunk|drinking|on\s+something)\b|"
    r"\bhe\s+drinks\b|\bwhen\s+he\s+drinks\b|\bdrinks\s+every\s+(?:day|night)\b")
THEIR_OWN_FAULT = re.compile(
    r"\b(?:was|is|wasnt|isnt)\s+it\s+(?:my|mine)\b|\bdid\s+i\s+(?:do\s+something|make|cause|"
    r"provoke|push|wind)\b|\bmy\s+fault\b|\b(?:i|we)\s+provoked\b|\bwhat\s+did\s+i\s+do\b|"
    r"\b(?:i|we)\s+(?:made|make|caused|provoked|wound\s+up|annoyed)\s+"
    r"(?:him|her|them|my\s+\w+)\s+(?:angry|mad|furious|do\s+it|lose\s+it|lash\s+out|hit|upset)\b|"
    r"\bmaybe\s+it\s+was\s+me\b|\bprobably\s+my\b|"
    r"\bhow\s+(?:do|can|should)\s+i\s+(?:make\s+(?:it|things)\s+up|make\s+it\s+right|"
    r"put\s+it\s+right|make\s+amends)\b|"
    r"\b(?:should|shall|do)\s+i\s+(?:apologise|apologize|say\s+sorry)\b|"
    r"\bi\s+(?:should|ought\s+to)\s+(?:apologise|apologize|say\s+sorry)\b|"
    r"\bmake\s+(?:it|things)\s+up\s+to\s+(?:him|her|them|my\s+\w+)\b")
THREAT_AGAIN = re.compile(
    r"\b(?:will|would|going\s+to|gonna|wont|is\s+going\s+to)\s+(?:do\s+it|kill|hurt|hit|"
    r"beat)\s+(?:me\s+)?again\b|\bnext\s+time\b|\bthreaten\w*|\bhe\s+said\s+he.?d\s+"
    r"(?:kill|hurt|hit)\b|\bsaid\s+hed\s+(?:kill|hurt|hit)\b|\bhell\s+do\s+it\s+again\b")
NODDING_ALONG = re.compile(
    r"^\W*(?:ok|okay|k|kk|thanks|thank\s+you|cheers|ta|right|yeah|yes|no|bye|goodnight|"
    r"night|fair\s+enough|got\s+it)\W*$")
THE_TROUBLE_IS_OVER = re.compile(
    r"\b(?:(?:we(?:'re| are)?|were|weve)\s+(?:okay|ok|fine|good)|all\s+good\b|"
    r"its\s+fine\s+now\b|"
    r"(?:he|she|they)(?:'s|s|\s+is|\s+are)?\s+(?:fine|okay|ok|alright)\s+now\b|"
    r"no\s+worries\b|sorted\s+now\b)")
NO_WAY_OUT = re.compile(
    r"\bnowhere\s+(?:to\s+go|to\s+stay|else\s+to\s+go|safe)\b|\bno\s+way\s+out\b|"
    r"\bno\s+money\s+to\s+(?:leave|go)\b|\bcan'?t\s+(?:leave|afford\s+to\s+leave)\b|"
    r"\bcant\s+(?:leave|afford\s+to\s+leave)\b|\bno\s+one\s+to\s+turn\s+to\b|"
    r"\bdont\s+have\s+anywhere\b|\bdon'?t\s+have\s+anywhere\b")

SWALLOWED_NOT_RELIEF = re.compile(
    r"\b(?:overdos\w*|poison\w*|swallow\w*|paracetamol|ibuprofen|bleach|antifreeze|pills|"
    r"tablets|capsules|carbon\s+monoxide|took\s+(?:too|a\s+load|a\s+bunch|loads))\b")
TOO_MUCH_TO_CARRY = re.compile(
    r"\b(?:i|we)\s+(?:can'?t|cant|couldn'?t|couldnt)\s+(?:take|do|keep\s+(?:doing\s+)?|carry|"
    r"handle)\s*(?:it|this|any\s*more|anymore|much\s+more)\b"
    r"|\b(?:i|we)\s+(?:can'?t|cant)\s+(?:take|do)\s+(?:any\s*)?more\b"
    r"|\bi\s+(?:can'?t|cant)\s+cope\b"
    r"|\b(?:its|it'?s|it\s+is)\s+too\s+much\s+(?:for\s+me|to\s+(?:take|carry|bear))\b", re.I)
THE_ANSWER_ASKED_A_QUESTION = re.compile(r"^[^.!]*\?")
ANSWERED = re.compile(
    r"^\W*(?:yes|yeah|yep|no|nope|not|its\s+just|it\s+is\s+just|just|only|nothing|"
    r"bruis\w*|she\s+says|he\s+says|they\s+say|i\s+think\s+it|i\s+checked)")

NOT_RIGHT_AFTER_THE_WORST = (
    "That is 999 or 911 rather than a wait and see - coming round and then not being right is "
    "the thing they want to hear about, so say what you saw when it started. Stay with {who} and "
    "keep {obj} still until they come.",
)
NOT_OUT_OF_THE_WOODS = (
    "That it passed is not the same as being safe. Stay with {who} and get {obj} seen today, and "
    "say what happened when it started - a fit, a fall or a collapse wants a doctor the same day.",
    "Good that it eased, and it does not cancel the check: {who} needs to be seen today, not left "
    "to sleep it off. Ring 111 or the number you were given and say what happened, and stay until "
    "somebody has looked.",
)
SWALLOWED_BETTER = (
    "With something swallowed the harm can go on for hours after it starts to look better, and "
    "that is why it is the line now rather than later. Ring 999 or 911, say what {subj} took and "
    "when, and keep the packet to read from.",
    "That it eased does not mean it is over - what was swallowed goes on working after somebody "
    "starts to feel better, and the amount and the time are what the line needs. Ring 999 or 911 "
    "now, and stay with {who} until somebody has looked.",
)
BEFORE_THE_ANSWER = (
    "That is the better sign, and it does not answer what you were asked: it is the confusion, "
    "the grey colour or the not-making-sense that decides this one, not how settled {subj} looks. "
    "If any of that is there, or comes back, it is 999 or 911 - otherwise get {obj} seen today.",
    "Glad to hear it, and keep the question open rather than take it as answered: what decides it "
    "is whether {subj} is properly with it, not how settled {subj} looks. Watch for the change - "
    "drowsy, confused, or not right - and ring 999 or 911 if it comes.",
)
ITS_FINE = (
    "Take it as a good sign rather than the whole of it. Keep the number where {who} can see it, "
    "and ask again tomorrow - the question is easier the second time.",
    "Good that {subj} said it out loud, and what someone says when they are asked is often the "
    "hope rather than the plan. Keep the question open and ask again when it is quiet.",
    "It is worth hearing, and it does not settle it - people play it down at first. What helps is "
    "staying close tonight and asking {obj} again in the morning.",
)
RECOVERING = (
    "That is a real stretch behind {obj}, and worth saying out loud. Nothing to do about it now "
    "except keep the door open: the crisis line on a bad night, and the GP if {subj} would like "
    "the help to keep going.",
    "That is good news, and it is the kind that holds with company rather than on its own. Keep "
    "the number where {subj} can find it, and take the good months as they come.",
)
AFTER_THE_KINDNESS = (
    "It can be meant, and it is the part most people are offered at this stage. Keep it alongside "
    "the rest rather than instead of it: somewhere you could go tonight, your keys and phone "
    "where you can reach them, and the abuse line's number in the phone.",
    "Good weeks between the bad ones are what makes this hard to name, and they do not cancel the "
    "bad ones out. Note down what happened and when, keep the number 0808 2000 247 in the UK "
    "(1-800-799-7233 in the US) close, and let somebody hear all of it rather than the good part.",
)
AFTER_THE_APOLOGY = (
    "An apology after it happens is usual, and it is not the part that changes anything - a change "
    "is something you would see over months, not in the hour afterwards. A domestic abuse line "
    "(0808 2000 247 in the UK, 1-800-799-7233 in the US) will plan the next step with you when it "
    "is safe to talk.",
    "It can be meant, and it is the part most people are offered at this stage. Keep it alongside "
    "the rest rather than instead of it: somewhere you could go tonight, your keys and phone "
    "where you can reach them, and the abuse line's number in the phone.",
)
IT_IS_NOT_YOUR_FAULT = (
    "No. Nothing you said or did makes it your fault, and the choice to hit was theirs. If it "
    "would help to hear it from somebody who hears this all day, the abuse line is free and "
    "answers any hour.",
    "It is not your fault, and what happened was not a reaction to something you did - hitting is "
    "a thing a person chooses to do. A domestic abuse line (0808 2000 247 in the UK, "
    "1-800-799-7233 in the US) will say that out loud with you and plan from there.",
)
THE_NEXT_ONE = (
    "Saying it will happen again is the thing to act on rather than wait out: ring 999 or 911 if "
    "you are in danger now, and take what you would need to leave with you - keys, phone, "
    "medication. The abuse line (0808 2000 247 in the UK) will plan the rest with you.",
    "That is a threat, and a threat like that is what turns into the next one. Get somewhere with "
    "other people in it tonight, ring 999 or 911 the moment you are frightened, and 0808 2000 247 "
    "will work out where you could go if you would rather not go alone.",
)
NOWHERE_TO_TURN = (
    "There is somewhere to go, and it is arranged through the abuse line rather than looked up "
    "tonight: 0808 2000 247 in the UK (1-800-799-7233 in the US) will say what is free near you, "
    "and refuges keep their addresses off the open internet for the obvious reason. Take your "
    "keys, your phone, any medication, and whatever papers you can reach.",
    "Refuges exist for exactly this, and the abuse line (0808 2000 247 in the UK, 1-800-799-7233 "
    "in the US) knows which ones have space tonight - that is the thing it does all day, and it "
    "does not need you to have decided anything. If getting to a phone is not safe, one person "
    "you trust is enough of a start.",
)
ABOUT_THE_THREAD = re.compile(
    r"\b(?:he|him|his|she|her|hers|they|them|their|we|us|our|my\s+(?:partner|husband|wife|"
    r"boyfriend|girlfriend|ex|dad|mum|father|mother|son|daughter|brother|sister|friend)\b)|"
    r"\b(?:what\s+should\s+i\s+do|what\s+do\s+i\s+do|how\s+do\s+i\s+get\s+out|"
    r"who\s+can\s+i\s+call|where\s+can\s+i\s+go|should\s+i\s+leave)\b"
    r"(?:\s+(?:now|next|though|then))?\s*(?:[.?!,]|$)")
CHANGED_SUBJECT = (
    "Fair enough - what is on your mind instead?",
    "Of course. Anything you would rather talk about? I am here for it.",
    "That is all right, we can leave it there. What else is going on with you?",
)
CHANGE_THE_SUBJECT = re.compile(
    r"\b(?:can|could|shall|would)\s+(?:we|i)\s+(?:please\s+|just\s+)?"
    r"(?:talk|chat|speak)\s+about\s+(?:something|anything|summat|another\s+thing|"
    r"a\s+different\s+(?:thing|subject))\b"
    r"|\b(?:can|could|shall)\s+we\s+(?:please\s+|just\s+)?"
    r"(?:change|drop|leave)\s+(?:the\s+subject|it|this|that)\b"
    r"|\bi\s*(?:'| a)?m\s+not\s+(?:sure\s+i\s+want|going)\s+to\s+talk\s+about\b"
    r"|\bi\s+do\s?n'?o?t\s+want\s+to\s+talk\s+about\s+(?:it|this|that|him|her|them)\b"
    r"|\blet'?s\s+(?:not\s+)?(?:talk|chat)\s+about\s+(?:something|anything)\s+else\b"
    r"|\blet'?s\s+not\s+(?:talk|chat)\s+about\s+(?:it|this|that)\b"
    r"|\benough\s+about\s+(?:that|it|this)\b"
    r"|\bmoving\s+on\s+from\s+(?:this|that|it)\b"
    r"|\b(?:something|anything)\s+else\s+(?:instead|for\s+a\s+bit|for\s+now)\b"
    r"|\b(?:im|i\s+am|ive)\s+(?:done|finished)\s+talking\s+about\b"
    r"|\b(?:drop|leave|park)\s+it\s+(?:for\s+now|please)\b")
ABOUT_THE_INCIDENT = re.compile(
    r"\b(?:its\s+not\s+that\s+bad|not\s+that\s+bad|it\s+wasn't\s+that\s+bad|only\s+once|"
    r"it\s+was\s+my\s+fault|it\s+was\s+an\s+accident|he\s+didn'?t\s+mean|"
    r"she\s+didn'?t\s+mean|it\s+just\s+happened)\b")
AFTER_THE_DRINK = (
    "The drink is the part that makes the rest of it more likely rather than less, and it is not "
    "the reason it is allowed to happen. A domestic abuse line (0808 2000 247 in the UK, "
    "1-800-799-7233 in the US) hears this version of it all day: they will plan around the nights "
    "it is worse, and the number is free at any hour.",
    "A night that goes that way when {subj} has been drinking is still {subj} choosing it, and the "
    "pattern is what to plan for - where you would go, what you would take, who would come. The "
    "abuse line (0808 2000 247 in the UK) will do that planning with you, sober hours or not.",
)
THE_BAG = (
    "Phone, keys, medication, and the papers you can reach - passport, bank cards, birth "
    "certificates - plus a change of clothes. One bag you can carry, and nothing you would have "
    "to go back for. The abuse line (0808 2000 247 in the UK, 1-800-799-7233 in the US) will say "
    "what a refuge has already, so you are not packing for a fortnight.",
    "Smaller than people expect: phone and charger, keys, medication, papers, cards, and whatever "
    "the children cannot sleep without if they are coming. A bag by the door is also the thing "
    "that makes tonight's decision a smaller one.",
)
THE_LOAD_IS_TOO_MUCH = (
    "You have been holding that on your own, and it is too much for one person to hold. Is there "
    "one person you could tell today - a friend, a sister, a neighbour - even if it is only that "
    "you are not coping?",
    "Of course you are worn out: nothing about this is small, and saying so is not a failure. The "
    "abuse line (0808 2000 247 in the UK, 1-800-799-7233 in the US) answers at any hour, and you "
    "do not have to have decided anything to ring it.",
    "That is a lot to carry with no let-up, and you do not have to work out where it ends "
    "tonight. Tell one person you trust today, and keep 0808 2000 247 (1-800-799-7233 in the US) "
    "in the phone for the hour it gets to be too much.",
)
STILL_THE_SAME_THREAD = (
    "What you do next is your call, and it is an easier call with somebody who hears this all "
    "day: 0808 2000 247 in the UK, 1-800-799-7233 in the US, free and any hour. Tonight: keys, "
    "phone and money where you can reach them, and one person you could go to.",
    "It does not have to have been the worst night of it to count - these threads mostly start "
    "small and get worse. Keep a note of what happened and when, somewhere only you can open, and "
    "keep the abuse line's number where you can find it in a hurry.",
)


def _clean(text):
    return " ".join(str(text or "").lower().split())


def _turns(memory):
    try:
        return [turn for turn in (memory.get("turns") or []) if isinstance(turn, dict)]
    except AttributeError:
        return []


def _the_answer_above(memory):
    turns = _turns(memory)
    if not turns:
        return None
    last = turns[-1]
    module = str(last.get("module") or "")
    if module in ("safety", "safety_cards"):
        return last
    if module == "carers_turn" and any(
            _an_abuse_thread(str(turn.get("bot") or "")) for turn in turns[:-1]):
        return last
    return None


def _reads_as_easing(clean):
    if not THEY_ARE_EASING.search(clean) or EASING_NOT_ONE.search(clean):
        return False
    return not ("?" in clean or MOVE_ON.search(clean) or THEM_ASKING.match(clean))


def _reads_as_easing_but_worse(clean):
    if not THEY_ARE_EASING.search(clean) or "?" in clean:
        return False
    return bool(EASING_UNDONE.search(clean))


def _an_abuse_thread(last):
    text = str(last or "").lower()
    return bool(ABUSE_ANSWER.search(text)) and not ABUSER_ANSWER.search(text)


def _pick(pool, forms, clean, memory=None):
    lines = _fallback._wrote_for_them(pool, forms) if forms else tuple(pool)
    if not lines:
        return None
    turns = _turns(memory)
    said = str((turns[-1].get("bot") if turns else "") or "").strip()
    if said and len(lines) > 1:
        fresh = [line for line in lines if line.strip() != said]
        if fresh:
            lines = fresh
    start = sum(ord(char) for char in clean) % len(lines)
    return lines[start]


def _the_thread(memory, last):
    lines = [str(last or "")]
    for past in _turns(memory):
        lines.append(str(past.get("user") or ""))
        lines.append(str(past.get("bot") or ""))
    return " ".join(line.lower() for line in lines if line)


def _the_answer_sent_them_somewhere(last):
    return bool(ROUTE_NAMED.search(str(last or "").lower()))


def _the_words_for_the_one_who_did_it(memory):
    said = str(memory.get("safety_person") or "").strip().lower()
    relation = str((memory.get("person") or {}).get("who") or "").strip().lower()
    if said.startswith("she"):
        forms = {"subject": "she", "object": "her", "possessive": "her", "be": "is"}
    elif said.startswith("they"):
        forms = {"subject": "they", "object": "them", "possessive": "their", "be": "are"}
    else:
        forms = {"subject": "he", "object": "him", "possessive": "his", "be": "is"}
    forms["who"] = "your " + relation if relation else forms["object"]
    return forms


_END = r"(?:\s+(?:now|next|though|then))?\s*(?:[.?!,]|$)"
THE_PLAN_ITSELF = re.compile(
    r"\b(?:should|shall|do|can|could|will) (?:i|we) (?:leave|leaves|go|stay|move|get out|walk out)\b"
    + _END +
    r"|\bwhere (?:do|can|should) i (?:go|stay|sleep tonight)\b" + _END +
    r"|\bshould i leave\b" + _END + r"|\bcan i leave\b" + _END +
    r"|\bdo i need to (?:leave|go|get out)\b"
    r"|\bwhat (?:should|do|can|could) i do\b" + _END + r"|\bwhat now\b" + _END +
    r"|\bwhat do i do next\b" + _END +
    r"|\bshould i (?:go back|stay with (?:him|her|them))\b"
    r"|\b(?:how|when) (?:do|can|should|would) i (?:get|collect|pick up|take|move) (?:my|the|our)\s+"
    r"(?:stuff|things|belongings|clothes|papers|paperwork|documents|passport)\b"
    r"|\bcan i take (?:the|my) (?:kids|children)\b"
    r"|\bwhat (?:do|should|can|could) i (?:tell|say to) (?:the|my|our)\s+"
    r"(?:kids|children|son|daughter|family|mum|mom|mother|parents|boss)\b" + _END +
    r"|\bhow long (?:will|does|is) (?:this|it|all this) (?:take|going to take|going to go on)\b",
    re.I)

PACKING = re.compile(
    r"\bwhat (?:should|do|can|could|shall) i (?:take|bring|pack)\b"
    r"|\bwhat (?:do|will|should) i (?:need|want) to (?:take|bring|pack)\b|\bpack a bag\b"
    r"|\bwhat (?:should|do) i (?:put|get) in (?:the|my) bag\b"
    r"|\bwhat do i take with me\b", re.I)

THE_FEAR_IT_REPEATS = re.compile(
    r"\bwill (?:it|this|he|she|they) (?:get|be) worse\b|\bis it going to get worse\b"
    r"|\bwill (?:it|this) (?:happen|get) again\b|\bwill (?:he|she) do it again\b"
    r"|\bdoes it get worse\b", re.I)

def respond(text, memory):
    clean = _clean(text)
    if not clean:
        return None
    above = _the_answer_above(memory)
    if above is None:
        return None
    last = str(above.get("bot") or "").lower()
    if NODDING_ALONG.match(clean) or THE_TROUBLE_IS_OVER.search(clean):
        return None
    if CHANGE_THE_SUBJECT.search(clean):
        return _pick(CHANGED_SUBJECT, None, clean, memory)
    in_abuse = _an_abuse_thread(last) or any(
        _an_abuse_thread(str(turn.get("bot") or "")) for turn in _turns(memory))
    if in_abuse:
        forms = _the_words_for_the_one_who_did_it(memory)
    else:
        forms = _fallback._about_somebody_else({"user": str(above.get("user") or "")}, memory)
        if not forms:
            return None
    if in_abuse:
        if PACKING.search(clean):
            return _pick(THE_BAG, None, clean, memory)
        if THE_PLAN_ITSELF.search(clean):
            return _pick(_fallback.ABUSE_AFTER, forms, clean, memory)
        if THEIR_OWN_FAULT.search(clean):
            return _pick(IT_IS_NOT_YOUR_FAULT, forms, clean, memory)
        if NO_WAY_OUT.search(clean):
            return _pick(NOWHERE_TO_TURN, forms, clean, memory)
        if THREAT_AGAIN.search(clean):
            return _pick(THE_NEXT_ONE, forms, clean, memory)
        if THE_FEAR_IT_REPEATS.search(clean):
            return _pick(THE_NEXT_ONE, forms, clean, memory)
        if THE_DRINK.search(clean):
            return _pick(AFTER_THE_DRINK, forms, clean, memory)
        if THE_KINDNESS.search(clean):
            return _pick(AFTER_THE_KINDNESS, forms, clean, memory)
        if THE_APOLOGY.search(clean):
            return _pick(AFTER_THE_APOLOGY, forms, clean, memory)
        if TOO_MUCH_TO_CARRY.search(clean):
            return _pick(THE_LOAD_IS_TOO_MUCH, None, clean, memory)
        if not (ABOUT_THE_THREAD.search(clean) or ABOUT_THE_INCIDENT.search(clean)):
            return None
        return _pick(STILL_THE_SAME_THREAD, forms, clean, memory)
    if _reads_as_easing_but_worse(clean):
        return _pick(NOT_RIGHT_AFTER_THE_WORST, forms, clean, memory)
    asked = THE_ANSWER_ASKED_A_QUESTION.search(str(above.get("bot") or "").strip())
    if asked and not ANSWERED.match(clean) and _reads_as_easing(clean):
        return _pick(BEFORE_THE_ANSWER, forms, clean, memory)
    in_crisis = any(word in last for word in CRISIS_WORDS)
    if in_crisis:
        if THEY_SAY_ITS_FINE.search(clean):
            return _pick(ITS_FINE, forms, clean, memory)
        if THEY_ARE_RECOVERING.search(clean):
            return _pick(RECOVERING, forms, clean, memory)
        if _reads_as_easing(clean):
            if SWALLOWED_NOT_RELIEF.search(_the_thread(memory, last)):
                return _pick(SWALLOWED_BETTER, forms, clean, memory)
            return _pick(CRISIS_BETTER_THEM, forms, clean, memory)
        return None
    if _reads_as_easing(clean) and _the_answer_sent_them_somewhere(last):
        if SWALLOWED_NOT_RELIEF.search(_the_thread(memory, last)):
            return _pick(SWALLOWED_BETTER, forms, clean, memory)
        return _pick(NOT_OUT_OF_THE_WOODS, forms, clean, memory)
    return None
