import re

from ..compose import pick
from . import history

_SOFT_LEAD = r"(?:oh |aw+ |ah |ha+ |lol |tbh |honestly |ok |okay |well |and |but |still |even so )*"
_NO_LEAD = r"(?:(?:no+|nah|nope)(?:,)? )?"
_SOFT_TAIL = (
    r"(?:,? (?:too|also|lots|loads|honestly|tbh|really|so much|very much|you know|though|tho|"
    r"me|at all|at this|at that|ha+|lol))*"
    r"(?: [.!]+)?$"
)

_TIME_TAIL = (
    r"(?: (?:today|tonight|this morning|this afternoon|this evening|right now|at the moment|"
    r"now|lately|recently))?")

_LOVE = re.compile(
    r"^" + _SOFT_LEAD +
    r"(?:(?:i|we) (?:really |do |just |actually |so |still |truly )?)?"
    r"l(?:ove|uv) (?:you|u|ya)" + _SOFT_TAIL + r"$")
_LIKE = re.compile(
    r"^" + _SOFT_LEAD +
    r"(?:(?:i|we) (?:really |do |quite |actually |just |kind of |sort of )?)?"
    r"like (?:you|u)" + _SOFT_TAIL + r"$")
_FAVOURITE = re.compile(
    r"^" + _SOFT_LEAD +
    r"(?:you(?:'?re| are) )?(?:(?:my|me) )?(?:favourite|favorite)"
    r"(?: (?:bot|chatbot|one|thing|app))?" + _SOFT_TAIL + r"$")
_APPRECIATE = re.compile(
    r"^" + _SOFT_LEAD +
    r"(?:(?:i|we) (?:really |do |so much |just )?)?appreciate (?:you|u|ya)" + _SOFT_TAIL + r"$")

_ON_FORM = re.compile(
    r"^" + _SOFT_LEAD +
    r"(?:"
    r"you(?:'?re| are)(?: really| so| very| always| honestly| definitely)?"
    r" (?:on form|on fire|on a roll|in (?:good|great|fine|top) form|in a (?:good|great) mood|"
    r"a lifesaver|a gem|a trooper)"
    r"|you(?:'?re| are)(?: really| so| very| always| being)"
    r" (?:patient|helpful|good company)(?: (?:with|for) (?:me|us))?"
    r"|you(?:'?re| are| seem| look)(?: really| so| very| always| looking| seeming)?"
    r" (?:well|happy|cheerful|pleased|in good spirits)"
    r"|you seem(?: really| so| very)? (?:happy|cheerful|pleased|in a good mood|on form|well)"
    r")" + _TIME_TAIL + _SOFT_TAIL + r"$")

_GOT_IT_WRONG = re.compile(
    r"^" + _SOFT_LEAD +
    r"(?:you|u)(?:'?ve| have)? (?:just |really |actually |clearly |totally |completely )?"
    r"(?:got|get|had) (?:that|this|it) "
    r"(?:wrong|mixed up|back to front|the wrong way round)" + _SOFT_TAIL + r"$")
_THE_WRONG_THING = re.compile(
    r"^" + _SOFT_LEAD +
    r"(?:(?:that|this|it)(?:'?s| is| was)?|the) (?:the )?wrong "
    r"(?:one|address|day|time|name|number|answer|thing|word|date|price|place|person|direction|"
    r"link|order)" + _SOFT_TAIL + r"$")
_NOT_WHAT_I_MEANT = re.compile(
    r"^" + _SOFT_LEAD +
    r"(?:(?:that|this|it)(?:'?s| is| was)? |you )?"
    r"(?:not|isnt|isn'?t|wasnt|wasn'?t) (?:really |quite |at all |exactly )?"
    r"what i (?:meant|mean|was asking about|asked about|was after|wanted|needed)"
    + _SOFT_TAIL + r"$")
_MIXED_UP = re.compile(
    r"^" + _SOFT_LEAD +
    r"(?:you|u)(?:'?ve| have)? (?:just |really |clearly |totally |completely )?"
    r"(?:got (?:it|that|this|them) )?(?:mixed|muddled|confused) "
    r"(?:it|that|this|them|the two|two things)? ?up" + _SOFT_TAIL + r"$")
_THE_OTHER_ONE = re.compile(
    r"^" + _SOFT_LEAD +
    r"(?:no |nope |nah |sorry,? |actually )?(?:i )?(?:meant|mean) the other "
    r"(?:one|option|day|address|name|thing|number|person)" + _SOFT_TAIL + r"$")
_NO_NOT_THAT = re.compile(
    r"^" + _SOFT_LEAD +
    r"(?:no|nope|nah),? (?:not|no) (?:that|this) one" + _SOFT_TAIL + r"$")
_BARE_WRONG = re.compile(
    r"^" + _SOFT_LEAD + r"wrong(?: again| then| still)?" + _SOFT_TAIL + r"$")

_MACHINE = re.compile(
    r"^" + _SOFT_LEAD +
    r"(?:you(?:'?re| are)(?: just| only| really| basically)?(?: an?)? "
    r"(?:computer|machine|bot|chatbot|programme|program|ai|robot|script)(?: though| tho)?"
    r"|you (?:dont|do not|haven'?t|have not|havent) (?:have|got) (?:any )?"
    r"(?:feelings|a life|a body|a heart)"
    r"|you(?:'?re| are) not (?:a )?(?:real|person|human)(?: person)?)"
    r"(?:,? (?:though|tho|right|eh|arent you|are you not|arent ya|arent u|do you|dont you))?"
    + _SOFT_TAIL + r"$")

PRAISED_REPLIES = (
    "I'll take that. It's a good day for it.",
    "Ha - thank you. Let's see if I can keep it up.",
    "That's good to hear. I've no idea what I'm doing, but it's working.",
    "That's kind of you to say. I'll keep at it.",
    "Glad it's landing well. Half of it is you saying things plainly.",
)

MACHINE_REPLIES = (
    "That's right - no feelings to hurt and no life to get back to. I'm still glad of the chat.",
    "A program, yes. It suits me, and it's a good way to spend a few minutes.",
    "No person behind it, just rules doing their job. Ask me something and see how they do.",
    "True enough. I'd rather be useful than real, and I can be useful.",
)

WARM_REPLIES = (
    "That's kind of you. I like these chats too.",
    "You're good to me \u2014 I'm glad you're here.",
    "Thank you. It goes both ways, as far as a program can manage it.",
    "That's made my day. What shall we do with the rest of it?",
    "Kind of you. I'll keep the tea on.",
)

_NO_HELP = re.compile(
    r"^" + _SOFT_LEAD +
    r"(?:"
    r"you(?:'?re| are) (?:no help|not helping|useless|no use|hopeless|not listening|"
    r"not hearing me|just guessing|guessing again|making it worse|not on form|off your game|"
    r"a bit slow today|slower today|struggling today|not yourself today)"
    r"|you (?:dont|do not|don't) (?:understand|get it|listen|hear me|know what i mean)"
    r"|you(?:'?re| are) (?:rubbish|crap|useless|no good|hopeless)(?: at (?:this|it|all this))?"
    r"|(?:just )?listen to me(?: (?:for )?a (?:minute|second|sec))?"
    r"|you(?:'?ve|\s+have)?\s+(?:not|n't|havent|haven't|hasnt)\s+(?:not\s+)?"
    r"(?:helped|understood|listened|got it)\b"
    r"|(?:that|thats|that's|this) (?:was|is|isnt|isn't)? ?(?:no help|not helping|not helpful|"
    r"useless|no use|hopeless|a waste of time|rubbish|garbage)"
    r"|you(?:'?re| are|r) (?:not|n't) (?:really |quite |actually |even )?"
    r"(?:gett(?:ing|in) it|gett(?:ing|in) the point|getting what i mean|understanding(?: me)?|"
    r"following)"
    r"|your (?:not|n't) (?:really |quite |actually |even )?"
    r"(?:gett(?:ing|in) it|gett(?:ing|in) the point|getting what i mean|following)"
    r"|you (?:still )?(?:havent|haven't|have not|didnt|did not|didn't) (?:understood|got|followed|"
    r"grasped) (?:a word|any of that|any of it|the point|what i (?:said|meant))"
    r"|(?:forget it|never mind|nevermind),? (?:you (?:dont|do not|don't) (?:understand|get it))"
    r")" + _TIME_TAIL + _SOFT_TAIL + r"$")

_WRONG = re.compile(
    r"^" + _SOFT_LEAD + _NO_LEAD +
    r"(?:you(?:'?re| are)|that(?:'?s| is)?|this is|you(?:'?ve| have) got it)"
    r" (?:just |completely |totally |so )?(?:wrong|way off|not right|incorrect|making that up)"
    r"(?: about (?:it|that|this))?" + _SOFT_TAIL + r"$")
_INVENTED = re.compile(
    r"^" + _SOFT_LEAD +
    r"(?:you (?:just |only |really |must have |must've )?(?:made|make|invented|invent|guessed)"
    r" (?:that|this|it) up"
    r"|you (?:just |only |really )?(?:invented|invent|made up) (?:that|this|it)(?: up)?"
    r"|(?:that|this|it)(?:'?s| is| was)? (?:just )?(?:made|invented|made up|a guess)"
    r"|you(?:'?re| are) (?:just |only |really )?(?:guessing|making it up|making that up))"
    + _SOFT_TAIL + r"$")

FIRST_LINE_REPLIES = (
    "Nothing's come before this line, so there's nothing of yours I've dropped - tell me once and "
    "I'll keep it.",
    "We've only just started here - tell me what you need and I'll stay on it.",
    "I've no earlier line of yours to go back to. Put it in one line and I'll take it from there.",
    "That's the first thing you've said to me, so there's nothing before it to have got wrong - "
    "what do you need?",
)
FIRST_LINE_READING = (
    "I read every line, and this is the first one - say what you need and I'll take it from there.",
    "I'm reading, yes: this is your first line, so there's nothing in front of me to have missed. "
    "Tell me what you need.",
)


def _nothing_said_before(memory):
    for turn in memory.get("turns") or []:
        if str((turn or {}).get("user") or "").strip():
            return False
    return True


def _a_complaint_reply(pool, memory, text, first=None):
    if not _nothing_said_before(memory):
        return pick(pool, memory, seed_text=str(text or ""))
    return pick(first or FIRST_LINE_REPLIES, memory, seed_text=str(text or ""))


MISSED_REPLIES = (
    "Fair enough \u2014 tell me what you were after and I'll have another go.",
    "That's on me. Say the bit that was off and I'll try it again.",
    "I'd rather hear that than not. Point me at what you needed and I'll start there.",
    "Then let's start again. What would have helped?",
)

_MISS_TAIL = (r"(?: (?:sorry|again|then|honestly|really|still))?"
              r"(?: (?:mate|love|pal|dude|hon|fella))?" + _SOFT_TAIL)

_OFF_THE_ASK = re.compile(
    r"^" + _SOFT_LEAD +
    r"(?:"
    r"(?:that|this|it|thats|that's)(?: is| was|'s)? not (?:what|the thing) i asked"
    r"|(?:that|this|it|thats|that's)(?: is| was)? not (?:my|the) question"
    r"|(?:that|this|thats|that's)(?: is| was)? not what i (?:asked|said)"
    r"|not what i (?:asked|said)"
    r"|(?:that|this|it)(?: isnt| isn't| wasnt| wasn't| is not| was not) what i (?:asked|said)"
    r"(?: you)?(?: to do)?"
    r"|(?:im|i am) not asking (?:you )?(?:about )?(?:that|this)"
    r"|i (?:didnt|did not|don't|dont|never) ask (?:you )?(?:about )?(?:that|this|for that)"
    r"|(?:that|this|it|thats|that's)(?: is| was|'s)? (?:irrelevant|not relevant|"
    r"beside the point|missing the point|not the point)"
    r"|(?:that|this|it)? ?(?:is|was|isnt|isn't)? ?not relevant(?: at all)?"
    r")" + _MISS_TAIL)
_NO_ANSWER = re.compile(
    r"^" + _SOFT_LEAD +
    r"(?:"
    r"you (?:didnt|did not|don't|dont|never|havent|haven't|have not|hadnt|hadn't)"
    r" (?:answer|answered|reply|replied)(?: me| my questions?| the question| that| it)?"
    r"|you (?:still )?(?:havent|haven't|didnt|did not|never) (?:answered|replied to)"
    r" (?:my|the|that) questions?"
    r"|(?:that|this|it) (?:doesnt|does not|didnt|did not) answer (?:my|the|that) questions?"
    r"|you(?:'?re| are) not (?:even )?answering(?: me| my questions?| the question)?"
    r"|answer (?:my|the) questions?"
    r")" + _MISS_TAIL)
_REPEATED = re.compile(
    r"^" + _SOFT_LEAD +
    r"(?:"
    r"you (?:keep|kept|keeps|are|were) (?:saying|telling me|repeating|going on about)"
    r" (?:that|this|it|the same thing|the same)"
    r"|you(?:'?ve| have)?(?: already)? said (?:that|this|it)(?: already| before)?"
    r"|you(?:'?re| are) (?:just )?repeating (?:yourself|the same thing|the same)"
    r"|you (?:just |even |always )?repeat(?:ed|ing)? (?:yourself|the same thing|the same)"
    r"|same (?:answer|thing|line) (?:again|twice)"
    r"|you(?:'?ve| have)?(?: already)? told me(?: (?:that|this|it))?"
    r"(?: (?:already|before|twice))?"
    r"|you(?:'?ve| have)?(?: already)? asked (?:me )?(?:that|this|it)"
    r"(?: (?:already|before|twice))?"
    r"|you (?:keep|kept) asking (?:me )?(?:that|this|the same thing|the same)"
    r"|(?:please )?stop (?:saying|repeating|copying|parroting) (?:that|this|it|yourself|me)"
    r"|(?:that|this|it)(?:'?s| is| was)? (?:the )?same (?:thing|answer|line|reply)"
    r"|we(?:'?ve| have) been (?:through|over|round) (?:this|that|it) (?:before|already)"
    r"|we(?:'?ve| have) (?:done|had|covered) (?:this|that|it) (?:before|already)"
    r"(?: again| twice)?"
    r")" + _MISS_TAIL)
_TOLD_BEFORE = re.compile(
    r"^" + _SOFT_LEAD +
    r"(?:"
    r"i (?:already |just )?(?:told|told ya) (?:you|u|ya)(?: (?:that|this|it))?"
    r"(?: (?:already|before|twice))?"
    r"|i (?:already )+said (?:that|this|it)(?: (?:already|before|twice))?"
    r"|(?:ive|i've|i have)(?: already)? (?:told|said)(?: you| u)?(?: (?:that|this|it))?"
    r"(?: (?:already|before|twice))?"
    r"|i (?:just )?said (?:that|this|it)(?: (?:already|before|twice))?"
    r"|you (?:already )?(?:ignored|forgot|forgotten|lost|dropped|skipped) "
    r"(?:what|that) i (?:said|told you)"
    r"|you(?:'?d| had) (?:already )?(?:forgot|forgotten|lost|dropped) (?:what|that) i "
    r"(?:said|told you)"
    r"|you(?:'?ve| have)? (?:completely |totally |rather )?lost (?:the )?"
    r"(?:thread|plot|train of thought)"
    r")" + _MISS_TAIL)
_MUDDLED = re.compile(
    r"^" + _SOFT_LEAD +
    r"(?:"
    r"(?:are|r|were) (?:you|u) (?:even |really |actually )?(?:reading|listening)"
    r"(?: to (?:me|us|what i (?:type|typed|say|said|write|wrote|ask|asked))"
    r"| (?:what i|anything i) (?:type|typed|say|said|write|wrote|ask|asked))?"
    r"|do (?:you|u) (?:even |really |actually )?(?:read|listen to)"
    r" (?:what i|anything i) (?:type|typed|say|said|write|wrote|ask|asked)"
    r"|you(?:'?re| are)? ?(?:not|arent|aren'?t)(?:(?: even| really| actually))? "
    r"(?:reading|listening)(?: to (?:me|us|what i (?:say|type|write))"
    r"| (?:what i|anything i) (?:say|type|write)| this| that| it)?"
    r"|(?:youre|you are|you(?:'?ve| have)) (?:just |clearly |obviously )?"
    r"(?:ignoring|ignored) (?:me|us|what i (?:say|said|type|typed|write|wrote|ask|asked))"
    r"|(?:that|this|your answer|that answer)(?: all)? (?:makes|made|doesnt make|didnt make)"
    r" (?:any |no |much )?sense"
    r"|(?:that|this|it|thats|that's)(?: is| was)? not (?:really )?making (?:any |much )?sense"
    r"|what are (?:you|u) (?:even )?(?:on about|talking about|going on about|saying|writing)"
    r"|you(?:'?re| are) (?:not|n't) (?:really )?(?:making sense|making any sense)"
    r"|(?:that|this|it|thats|that's)(?: is| was|'s)? (?:just |all |complete |utter )?nonsense"
    r")" + _MISS_TAIL)

MISSED_ASK_REPLIES = (
    "You're right \u2014 that wasn't your question. Say it once more and I'll answer that one.",
    "Fair. I answered something else. What was the question I skipped?",
    "Then point me back at it, in one line, and I'll stick to that and nothing else.",
    "My mistake. Ask it once more and I'll take it as it stands.",
)
REPEATED_REPLIES = (
    "So I did. I've nothing new on that one \u2014 which bit is still unanswered?",
    "You're right, I said it twice. Tell me what's still open and I'll stay on it.",
    "Fair. I'll stop circling. What would help instead?",
    "I did repeat myself, sorry. Say the part that's still missing and I'll start there.",
)
TOLD_BEFORE_REPLIES = (
    "You did tell me, and I lost it. Say it once more and I'll use it this time.",
    "So you did. Put the key bit in one line and I'll go from there.",
    "Right, you said. I'll take it as given \u2014 what do you need on it?",
    "You did, and I should have kept hold of it. What was the bit I dropped?",
)
MUDDLED_REPLIES = (
    "I do read every line, and I still got that one wrong. Say it again and I'll go slowly.",
    "That came out muddled \u2014 my fault. Ask me once more and I'll keep it plain.",
    "Fair, that was a mess. One more go and I'll answer the part you asked about.",
    "I've read it, it just didn't land. Tell me again in the words you'd use to a friend.",
)
WRONG_REPLIES = (
    "Fair enough \u2014 which bit? I'd rather be put right than keep going.",
    "Then tell me what's right about it and I'll go with that.",
    "I can only go on what I have. What have I got wrong?",
)


_BACK_TO_SOMETHING = re.compile(
    r"^" + _SOFT_LEAD +
    r"(?:"
    r"(?:as|like) (?:i|you) (?:said|says|mentioned|told you)(?: (?:before|earlier|already))?"
    r"|(?:going|coming|back) (?:back )?to (?:it|that|this|the (?:first|last|other) one"
    r"|(?:one|stuff))(?: one)?"
    r"|(?:you|u) mentioned (?:it|that|this)? ?(?:before|earlier)"
    r"|(?:the|that) (?:one|thing|bit) (?:we|you and i) (?:discussed|talked about|mentioned)"
    r"|we (?:talked|spoke|went) (?:about|over|through) (?:this|that|it)"
    r"|we (?:spoke|talked|chatted)(?: (?:yesterday|today|earlier|before|last (?:night|week"
    r"|time|month)))?"
    r"|we(?:'?ve| have)(?: already)? (?:spoken|talked|chatted)(?: (?:about|over) (?:it|this|that))?"
    r"|we (?:were|have been|had been) (?:just )?(?:chatting|talking|speaking)"
    r"(?: (?:about (?:it|this|that)|earlier|before|yesterday|last (?:night|week)))?"
    r"|we(?:'?ve| have)? been (?:through|over|round) (?:this|that|it)"
    r"|(?:youve|you have|you(?:'?d| had)) (?:forgotten|lost|dropped) (?:what|that) i "
    r"(?:said|told you)"
    r"|(?:the )?(?:same|that same) (?:one|thing|again|answer|line)(?: (?:again|twice)"
    r"| as (?:before|last time))?"
    r"|same again(?: please)?"
    r"|(?:that|this) one(?: again)?"
    r"|again"
    r"|(?:and )?(?:anything|something) else"
    r"|i forgot(?: (?:it|that|this|now))?"
    r")" + _SOFT_TAIL)

FIRST_LINE_REPLIES = (
    "That's the first thing you've said to me, so there's nothing before it - what is it you want "
    "to go back over?",
    "You haven't said anything yet, so there's nothing there for me to have missed. Tell me the "
    "thing itself and I'll take it from there.",
    "This is the start of our chat - nothing has been said before this line. What did you want to "
    "ask?",
    "There's nothing earlier for me to go back to: this is your first line. Say what you need on "
    "it and I'll pick it up.",
)


def _nothing_said_yet(memory):
    return not history.an_earlier_turn(memory)


_TYPED_SHORT = {
    "u": "you", "ya": "you", "ur": "your", "r": "are", "iv": "ive", "wot": "what", "wat": "what",
    "dat": "that", "dis": "this", "thts": "thats", "tht": "that", "sayin": "saying",
    "gettin": "getting", "abt": "about",
}
_YOUR_NOT = re.compile(r"\byour (not|n't|being|making|repeating|saying|getting)\b")


def reply(text, memory):
    clean = " ".join(str(text or "").lower().replace("\u2019", "'").split())
    clean = " ".join(_TYPED_SHORT.get(word, word) for word in clean.split())
    clean = _YOUR_NOT.sub(r"youre \1", clean)
    clean = clean.strip(" \t")
    if not clean or len(clean.split()) > 8:
        return None
    if (_LOVE.match(clean) or _LIKE.match(clean) or _FAVOURITE.match(clean)
            or _APPRECIATE.match(clean)):
        return pick(WARM_REPLIES, memory, seed_text=str(text or ""))
    if _ON_FORM.match(clean):
        return pick(PRAISED_REPLIES, memory, seed_text=str(text or ""))
    nothing_before_it = not any(
        str((turn or {}).get("user") or "").strip() for turn in (memory.get("turns") or []))
    if not nothing_before_it and (
            _GOT_IT_WRONG.match(clean) or _THE_WRONG_THING.match(clean)
            or _NOT_WHAT_I_MEANT.match(clean) or _MIXED_UP.match(clean)
            or _THE_OTHER_ONE.match(clean) or _NO_NOT_THAT.match(clean)
            or _BARE_WRONG.match(clean)):
        return pick(WRONG_REPLIES, memory, seed_text=str(text or ""))
    if _MACHINE.match(clean):
        return pick(MACHINE_REPLIES, memory, seed_text=str(text or ""))
    first = _nothing_said_yet(memory)
    if first and (_BACK_TO_SOMETHING.match(clean) or _TOLD_BEFORE.match(clean)
                  or _REPEATED.match(clean) or _OFF_THE_ASK.match(clean)
                  or _NO_ANSWER.match(clean) or _MUDDLED.match(clean)
                  or _WRONG.match(clean) or _INVENTED.match(clean)
                  or _NO_HELP.match(clean)):
        return pick(FIRST_LINE_REPLIES, memory, seed_text=str(text or ""))
    if _WRONG.match(clean) or _INVENTED.match(clean):
        return pick(WRONG_REPLIES, memory, seed_text=str(text or ""))
    if _NO_HELP.match(clean):
        return _a_complaint_reply(MISSED_REPLIES, memory, text)
    if _REPEATED.match(clean):
        return _a_complaint_reply(REPEATED_REPLIES, memory, text)
    if _TOLD_BEFORE.match(clean):
        return _a_complaint_reply(TOLD_BEFORE_REPLIES, memory, text)
    if _OFF_THE_ASK.match(clean) or _NO_ANSWER.match(clean):
        return _a_complaint_reply(MISSED_ASK_REPLIES, memory, text)
    if _MUDDLED.match(clean):
        return _a_complaint_reply(MUDDLED_REPLIES, memory, text, FIRST_LINE_READING)
    return None
