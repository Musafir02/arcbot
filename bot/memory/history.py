import re

from . import topics

TALKED_ABOUT = re.compile(
    r"\bwhat (?:else )?(?:have|did|were) (?:we|you and i|you and me) "
    r"(?:been )?(?:talking|talked|talk|chatting|chatted|on|covering|covered|go over|through|about|discussed|discussing)\b"
    r"|\bwhat (?:topics|things|stuff) (?:have|did) we\b"
    r"|\bwhat did we (?:cover|discuss|mention|go over)(?:\s+(?:so far|today|just now|again))?\s*[?.!]*$"
    r"|\bremind me (?:what|of what) (?:we|you and i|you and me)(?:'ve|'d)? (?:have )?(?:been )?"
    r"(?:talked|spoken|chatted|discussed|covered|been on|gone over|been over)\b"
    r"|\bwhat did we go over(?:(?:\s+so far|\s+today|\s+just now))?\s*[?.!]*$")

FIRST_THING = re.compile(
    r"\bwhat (?:was|were|is) (?:the|my) first (?:thing|question|topic|bit|line|message|words?)"
    r"(?:\s+(?:i|we)\b|\s*[?.!]*$)"
    r"|\bwhat did (?:i|we) (?:say|ask|mention|talk about) first\b"
    r"|\b(?:where|how) did (?:we|i|you and i) (?:start|begin)\s*[?.!]*$"
    r"|\b(?:where|how) did (?:this|our|the) (?:chat|conversation|talk) (?:start|begin|go)\b"
    r"|\bhow did we (?:get|come) (?:on|to) (?:to )?(?:this|that|it)\b"
    r"|\bwhat did (?:i|we) (?:open|start) with\b")

FIRST_SAID_BY_BOT = re.compile(
    r"\bwhat (?:was|were|is) the first (?:thing|question|line|message|words?|answer|reply) "
    r"(?:that )?you\b"
    r"|\bwhat (?:was|were|is) your first (?:thing|question|line|message|words?|answer|reply)\b"
    r"|\bwhat did you (?:say|ask) first\b"
    r"|\bhow did you start\b"
    r"|\bwhat did you (?:say|tell me|answer|ask)(?: \w+){0,2} (?:at the (?:very )?(?:start|beginning)"
    r"|in the beginning|early on)\b")

RECALL_ABOUT = re.compile(
    r"\bwhat (?:did|have|do) (?:i|we) (?:say|said|tell you|told you|mention|mentioned)"
    r"(?: to you)? about\b"
    r"|\b(?:remind me|tell me again) (?:what|of what) (?:i|we)(?:'ve)? (?:said|told you|"
    r"mentioned|talked about|been on about)\b[^?.!]*\babout\s+\w")

SAID_ABOUT_HEAD = re.compile(
    r"^(?:and |so |ok |okay |also |but |oh )*"
    r"(?:what did you (?:say|tell me|mention|suggest|recommend)"
    r"|remind me what you (?:said|told me|mentioned)"
    r"|what was (?:it|that) you (?:said|told me|mentioned)"
    r"|what was your (?:answer|advice|reply|take)"
    r"|what did you tell me)\s*(?:about|on|regarding|for)\s+(?P<thing>.+)$")

CHAT_QUESTION = re.compile(
    r"\b(?:what|which|anything) (?:else )?(?:have|did|were|do) (?:we|i|you and i|you and me)\b"
    r"[^?.!]*\b(?:talk|talked|talking|chat|chatted|chatting|discuss|discussed|discussing|"
    r"cover|covered|covering|say|said|mention|mentioned|go over|been on|spoken)\b"
    r"|\b(?:remind me|tell me again|recap)\b[^?.!]*"
    r"\b(?:talked|talk|spoken|spoke|chatted|discussed|covered|said|been on|conversation|chat)\b"
    r"|\bsummar(?:y|ise|ize)\b.*\b(?:chat|conversation|talk|said)\b"
    r"|\bwhere (?:did|do) (?:we|i) (?:start|begin|get to|leave off|started)\b"
    r"|\bwhat (?:was|is) (?:the )?(?:first|last) (?:thing|question|topic|bit|line|message|words?)\b")

REMIND_ME_RECAP = re.compile(
    r"\bremind me (?:what|of what) (?:we|you and i|you and me)(?:'ve|'d)? (?:have )?(?:been )?"
    r"(?:covered|been on about|been on|discussed)\b")

WHERE_WE_WERE = re.compile(
    r"\bwhat (?:were|are|was) (?:we|i|you) (?:talking|chatting|on) about\b"
    r"|\bwhere were we\b|\bwhat was i saying\b")


STORE_SUMMARY = re.compile(
    r"\bsummar(?:y|ise|ize)\b"
    r"|\brecap\b"
    r"|\bcatch me up\b"
    r"|\bwhere (?:did|do) we (?:leave|left|get|got)\b")

RECALL_SHAPE = re.compile(
    r"\bwhat (?:does|do|did|is|are|was|were) (?:my|his|her|our|their)\b"
    r"|\b(?:what|where|who|when|how many) (?:do|did|am|is|are) (?:i|we)\b"
    r"|\bam i\b|\bdo i (?:have|live|work|need|eat)\b")


def _flat(text):
    return " ".join(str(text).lower().replace("’", "'").split()).strip(" ?.!,")


def the_thing_named(text):
    low = _flat(text).strip(" ?.!,")
    match = SAID_ABOUT_HEAD.match(low)
    if not match:
        return ""
    thing = match.group("thing").strip(" ?.!,")
    if not thing or thing in ("it", "that", "this", "them", "those", "these"):
        return ""
    return thing


MY_SAID_ABOUT_HEAD = re.compile(
    r"^(?:and |so |ok |okay |also |but |oh )*"
    r"(?:what did (?:i|we) (?:say|tell you|mention)"
    r"|(?:what|anything) have (?:i|we) (?:said|told you|mentioned)"
    r"|remind me what (?:i|we) (?:said|told you|mentioned)"
    r"|what was (?:it|that) (?:i|we) (?:said|told you|mentioned)"
    r"|did (?:i|we) (?:say|mention))\s*(?:anything\s+)?(?:about|on|regarding|for)\s+(?P<thing>.+)$")


def the_thing_they_named(text):
    low = _flat(text).strip(" ?.!,")
    match = MY_SAID_ABOUT_HEAD.match(low)
    if not match:
        return ""
    thing = match.group("thing").strip(" ?.!,")
    thing = re.sub(r"\s+", " ", thing)
    if not thing or thing in ("it", "that", "this", "them", "those", "these"):
        return ""
    return thing


def asked(text, memory=None):
    low = _flat(text)
    if WHERE_WE_WERE.search(low) or STORE_SUMMARY.search(low):
        return None
    if REMIND_ME_RECAP.search(low):
        return None
    if RECALL_ABOUT.search(low):
        return None
    if the_thing_named(low):
        return "said_about"
    if FIRST_SAID_BY_BOT.search(low):
        return "first_bot"
    if FIRST_THING.search(low):
        return "first"
    if TALKED_ABOUT.search(low):
        return "topics"
    return None


NOTHING_SAID = re.compile(
    r"\s*(?:hi|hiya|hello|hey|yo|morning|evening|good (?:morning|afternoon|evening)|\s*"
    r"how (?:are you|r you|are u)(?:\s+doing)?(?:\s+today)?|how(?:'s| is|s) it going|how are things|"
    r"what(?:'s| is|s) up|thanks?|thank you|cheers|ta|nice(?: one)?|great|lovely|ok(?:ay)?|cool|wow|"
    r"tell me (?:a|another) (?:joke|story|fact)|tell me something|say something|sing me\b[^?.!]*|"
    r"give me a joke)\s*[.!?]*\s*")


GREETING_WITH_AN_ADDRESS = re.compile(
    r"\s*(?:hi|hiya|hello|hey|yo|morning|evening|good (?:morning|afternoon|evening))"
    r"(?:\s+(?:there|all|everyone|everybody|guys|folks|mate|team|both|you|y'all))+\s*[.!?]*\s*")


def _nothing_said(text):
    low = _flat(text)
    return bool(NOTHING_SAID.fullmatch(low) or GREETING_WITH_AN_ADDRESS.fullmatch(low))


def about_the_chat(text):
    low = _flat(text)
    return bool(asked(low) or RECALL_ABOUT.search(low) or CHAT_QUESTION.search(low))


def not_a_subject(text):
    return about_the_chat(text) or _nothing_said(text) or bool(RECALL_SHAPE.search(_flat(text)))


CLAIMS_A_PAST = re.compile(
    r"\b(?:where\s+we\s+(?:were|left\s+off|got\s+to)|what\s+were\s+we\s+(?:saying|on\s+about|up\s+to)"
    r"|what\s+were\s+you\s+saying"
    r"|as\s+(?:i|we)\s+said|as\s+before|same\s+as\s+before|you\s+mentioned|earlier\s+(?:you|we)"
    r"|last\s+time\s+(?:we|you|i)\b|what\s+did\s+i\s+say|remind\s+me\s+(?:what|where|which|how)"
    r"|carry\s+on\s+where|before\s+we\s+(?:broke\s+off|stopped)|still\s+here\s*,?\s+(?:if|so)"
    r"|what\s+(?:are|were)\s+we\s+(?:working\s+on|on|talking\s+about)"
    r"|whatever\s+you(?:'ve|\s+have)\s+been\s+(?:doing|up\s+to)"
    r"|(?:a\s+)?break\s+does\s+(?:a\s+lot\s+of\s+|you\s+)?good"
    r"|keep\s+it\s+going\s+(?:for\s+)?another|since\s+we\s+last\s+spoke|last\s+we\s+spoke"
    r"|(?:we|i)\s+(?:talked|spoke)\s+about\s+(?:it|that|this)"
    r"|where\s+(?:were\s+we|did\s+we\s+get\s+to|did\s+we\s+leave"
    r"|have\s+we\s+got\s+to))\b", re.I)

GREETS_A_RETURN = re.compile(
    r"^\s*(?:(?:oh|ah|well|hello|hi|hey|right|ok|okay|and|so)\s*[,!.]?\s*)?"
    r"(?:welcome\s+back|you(?:'re|\s+are)\s+back|back\s+again|"
    r"(?:good|nice)\s+to\s+(?:see|have)\s+you\s+(?:again|back)|(?:hello|hi|hey)\s+again)\b",
    re.I)


ANSWERS_AN_EARLIER_TURN = (
    "good to hear", "glad to hear", "sounds alright", "sounds good", "nice one",
    "thanks for telling me", "thanks for that", "say more", "tell me more about that",
    "how did the rest of it go", "anything good in it", "same as before", "same answer",
    "same again", "nothing new to add", "that is still the thing to do", "as i said",
    "as you said", "like i said", "you said", "you told me", "you mentioned", "back to what we",
    "where we were", "where were we", "the same goes for", "how did that go", "what was the best",
)
NO_CONTENT_WORDS = frozenset("""
a an the as i we you he she it they me my our your us them and or but so if then than that this
these those is was were be been being am are do does did done have has had got get gets go goes
going went gone on off up down out back again please sorry said say saying says tell told earlier
before after now still just really very fine ok okay right well yes no yeah nope hi hey hello
thanks thank nothing new same add to for of in at with about what where when who how why which
carry carrying never again anyway anyways so oh ah hmm um eh sort kind lot bit one cut
missed missed replies reply replied message messages quiet silence paused pause interrupted
distracted resume continue thread thought half unfinished midway apologise apologize apologies
gone away mid
""".split())


def brings_nothing_of_its_own(text):
    words = re.findall(r"[a-z0-9']+", str(text or "").lower())
    if not words:
        return True
    return all(word in NO_CONTENT_WORDS for word in words)


def an_earlier_turn(memory, text=""):
    return bool(_earlier_turns(memory, text))


def a_past_that_is_not_there(reply, memory, said=None):
    if an_earlier_turn(memory):
        return False
    low = " ".join(str(reply or "").lower().split())
    if not low:
        return False
    if CLAIMS_A_PAST.search(low) or GREETS_A_RETURN.match(low):
        return True
    if said is None:
        return False
    if not brings_nothing_of_its_own(said):
        return False
    return any(frame in low for frame in ANSWERS_AN_EARLIER_TURN)


def first_bot_line(memory):
    turns = memory.get("turns")
    if isinstance(turns, list):
        for turn in turns:
            if isinstance(turn, dict) and str(turn.get("bot", "")).strip():
                return " ".join(str(turn["bot"]).split())
    return ""


def _earlier_turns(memory, text=""):
    mine = " ".join(str(text or "").split()).lower()
    out = []
    for row in (memory.get("turns") if isinstance(memory, dict) else None) or []:
        if not isinstance(row, dict):
            continue
        line = " ".join(str(row.get("user") or "").split())
        if line and line.lower() != mine:
            out.append(row)
    return out


A_THEY_ASKED = re.compile(
    r"\?\s*$|^(?:what|when|where|who|why|how|which|do|does|did|can|could|should|would|is|are|"
    r"was|were|have|has|will|remind|tell me|any idea|any chance)\b", re.I)


def _a_line_they_asked(row):
    return bool(A_THEY_ASKED.search(" ".join(str((row or {}).get("user") or "").split())))


def _the_forms(words):
    out = set()
    for word in words or ():
        out |= topics.forms(word)
    return out


def the_earlier_turn(memory, text="", about=""):
    earlier = _earlier_turns(memory, text)
    if not earlier:
        return None
    told = [row for row in earlier if not _a_line_they_asked(row)]
    if told:
        earlier = told
    thing = about or the_thing_they_named(text) or the_thing_named(text)
    wanted = _the_forms(topics.content(thing)) if thing else set()
    if not wanted:
        return earlier[-1]
    scored = [(len(wanted & _the_forms(topics.content(row.get("user") or ""))), row)
              for row in earlier]
    best = max(hit for hit, _row in scored)
    if not best:
        return earlier[-1]
    return [row for hit, row in scored if hit == best][-1]


def first_line(memory):
    turns = memory.get("turns")
    if isinstance(turns, list):
        for turn in turns:
            if isinstance(turn, dict) and str(turn.get("user", "")).strip():
                return " ".join(str(turn["user"]).split())
    return ""


def topic_lines(memory, limit=3):
    seen, out = set(), []
    records = memory.get("topics")
    for record in records if isinstance(records, list) else []:
        if not isinstance(record, dict):
            continue
        text = " ".join(str(record.get("text", "")).split())
        if not text or text.lower() in seen or not_a_subject(text):
            continue
        seen.add(text.lower())
        out.append(text)
    turns = memory.get("turns")
    last = ""
    for turn in reversed(turns if isinstance(turns, list) else []):
        if not isinstance(turn, dict) or not str(turn.get("user", "")).strip():
            continue
        if turn.get("module") == "memory_store":
            continue
        last = " ".join(str(turn["user"]).split())
        break
    if last and last.lower() not in seen and not not_a_subject(last):
        out.append(last)
    return out[-limit:]


LOOK_BACK = 8

THEIR_NEWS = re.compile(r"\b(?:i|we|my|our|me|mine|us)\b|\bive\b|\bim\b", re.I)
A_QUESTION = re.compile(r"^\W*(?:what|where|when|who|why|how|which|do|does|did|is|are|was|were"
                        r"|can|could|should|would|will|shall|have|has|any)\b", re.I)
A_WANT = re.compile(r"\b(?:want|wants|wanting|need|needs|needed|hoping|hope to|planning|plan to"
                    r"|going to|thinking of|thinking about)\b", re.I)
A_BARE_YES = re.compile(r"^\W*(?:yes|yeah|yep|no|nope|ok|okay|sure|thanks|thank you|ta|right"
                        r"|cool|nice|hmm+|ah+|oh+)\W*$", re.I)


def turns_before(memory):
    if not isinstance(memory, dict):
        return []
    turns = memory.get("turns")
    if not isinstance(turns, list):
        return []
    return [turn for turn in turns if isinstance(turn, dict)]


def the_turn_before(memory):
    turns = turns_before(memory)
    return turns[-1] if turns else None


def nothing_said_before(memory):
    return not turns_before(memory)


def the_lines_before(memory, look_back=LOOK_BACK):
    said = [str(turn.get("user") or "").strip() for turn in turns_before(memory)[-look_back:]]
    return [line for line in said if line]


def the_line_before(memory, look_back=LOOK_BACK):
    lines = the_lines_before(memory, look_back)
    return lines[-1] if lines else ""


def is_their_news(line, words=3):
    said = " ".join(str(line or "").split())
    if len(said.split()) < words:
        return False
    low = said.lower()
    if said.endswith("?") or A_QUESTION.match(low) or A_BARE_YES.match(low):
        return False
    if A_WANT.search(low):
        return False
    return bool(THEIR_NEWS.search(low))


def the_news_turn_before(memory, words=3):
    for line in reversed(the_lines_before(memory)):
        if is_their_news(line, words):
            return line
    return ""


def the_earlier_line(memory, pattern, look_back=LOOK_BACK):
    if isinstance(pattern, str):
        pattern = re.compile(pattern, re.I)
    for line in reversed(the_lines_before(memory, look_back)):
        if pattern.search(line):
            return line
    return ""


def the_earlier_lines_that(memory, pattern, look_back=LOOK_BACK):
    if isinstance(pattern, str):
        pattern = re.compile(pattern, re.I)
    return [line for line in the_lines_before(memory, look_back) if pattern.search(line)]


def only_with_an_earlier_turn(reader):

    def guarded(memory, *args, **kwargs):
        if nothing_said_before(memory):
            return None
        return reader(memory, *args, **kwargs)

    guarded.__name__ = getattr(reader, "__name__", "guarded")
    return guarded


def the_last_answer(memory):
    said = [one.get("bot") for one in turns_before(memory) if str(one.get("bot") or "").strip()]
    return " ".join(str(said[-1]).split()) if said else ""


def _a_note_not_an_answer(said):
    from ..compose import fallback, verdict

    return verdict.takes_a_fact_back(said) or fallback.is_said_it_already(said)


def _a_hedge(said):
    from ..compose import fallback

    flat = said.lower()
    return fallback._is_a_hedge(said) or any(punt in flat for punt in fallback.PUNT)


def the_answer_on_screen(memory, within=3, modules=("answers", "safety")):
    seen = 0
    for turn in reversed(turns_before(memory)):
        said = str(turn.get("bot") or "").strip()
        if not said:
            continue
        seen += 1
        if seen > within:
            break
        if _a_note_not_an_answer(said):
            continue
        if str(turn.get("module") or "") not in modules:
            return ""
        if _a_hedge(said):
            return ""
        return " ".join(said.split())
    return ""


def the_turn_the_answer_came_from(memory, within=3):
    answer = the_answer_on_screen(memory, within)
    if not answer:
        return None
    for turn in reversed(turns_before(memory)):
        if " ".join(str(turn.get("bot") or "").split()) == answer:
            return turn
    return None


def the_answer_is_a_card(memory, within=3):
    turn = the_turn_the_answer_came_from(memory, within)
    return bool(turn) and str(turn.get("module") or "") == "safety"
