import re

from ..compose import pick
from . import repeat, there_is_a_chat
from .warmth import FIRST_LINE_REPLIES

SUBJECT = r"(?:i|we|ive|i've|weve|we've|i have|we have|i had|we had)"
ALREADY = re.compile(r"^\W*(?:(?:ok|okay|so|well|yeah|yep|yes|and|but|oh|right|alright|no)\W+)*"
                     r"(?:" + SUBJECT + r"\W+)?already\W+(\w+)", re.I)
DID = re.compile(r"^\W*(?:(?:ok|okay|so|well|yeah|yep|yes|and|but|oh|right|alright|no)\W+)*"
                 r"(?:i|we|ive|i've|weve|we've|i have|we have)\W+did\W+(\w+)", re.I)
DID_STEPS = frozenset("""call ring phone email text message speak talk ask tell contact write
send pay go see make take put book order buy fix bleed clean reset turn change check clear
tighten replace restart unplug soak scrub defrost hoover paint apply cut start stop give
complain report cancel register fill submit""".split())
DID_TAIL = frozenset("""that this it them him her me us the a an one ones thing stuff though tho
although again already twice once too well just still even really very much more some any all
and but so oh ok okay yeah yep yes no not yet since yesterday today tomorrow morning afternoon
evening last night week month year now then before after first both either
off out on up down around round through over back away""".split())


def _the_step_after_did(low):
    match = DID.search(low)
    if not match:
        return None
    step = match.group(1)
    if step not in DID_STEPS:
        return None
    tail = re.findall(r"[a-z']+", low[match.end():])
    if any(word not in DID_TAIL for word in tail):
        return None
    return step

TRAILING = re.compile(r"^\W*(?:(?:ok|okay|so|well|yeah|yep|yes|and|but|oh|right|alright|no)\W+)*"
                      r"(?:i|we|ive|i've|weve|we've)\W+(\w+)\b.*\balready\W*$", re.I)

PAST = frozenset("""called rang phoned emailed texted messaged spoke talked asked told contacted
wrote sent paid went seen saw made took put booked ordered bought tried fixed bled
cleaned reset turned changed checked cleared tightened replaced restarted unplugged soaked
scrubbed defrosted hoovered painted applied cut started stopped gave complained reported
cancelled registered filled submitted""".split())
CONTACT = frozenset("""called rang phoned emailed texted messaged spoke talked asked told
contacted wrote complained reported""".split())
NOBODY_TO_ANSWER = frozenset("""booked ordered registered submitted cancelled filled sent
paid""".split())
AN_APOLOGY = re.compile(r"\b(?:sorry|apolog\w*)\b", re.I)
REPAIRED = frozenset("""fixed bled cleaned reset turned checked cleared tightened replaced
restarted unplugged soaked scrubbed defrosted hoovered painted applied""".split())
CHANGED = frozenset("""tried started stopped gave paid ordered bought made took put went
changed cut""".split())
CHANGED_OF_A_THING = frozenset(("changed",))
A_LIFE_OBJECT = frozenset("""job jobs shift shifts hours routine routines plan plans mind diet
school course habit habits career way ways approach lifestyle life body sleep mood name names
address phone number provider tariff deal supplier gym class club doctor dentist""".split())
CHANGED_NOTHING_BROKEN = frozenset("""baby babies boy girl kid kids child children little one
him her them me you us everyone everybody nappy nappies pad pads sheet sheets bedding bed cot
quilt duvet pillow pillowcase towel towels flannel bag bags bin bins water loo toilet roll tea
dog cat puppy kitten pup hamster rabbit guinea budgie bird birds fish pet pets""".split())
ASKING = re.compile(r"\b(?:what|whats|what's|how|when|where|which|who|why|should|shall|can|could|"
                    r"will|would|may|might|do|does|did|is|are|any|anything)\b", re.I)
TO_THE_BOT = re.compile(r"\b(?:you|u|your|yours|youse)\b", re.I)
MOST_WORDS = 9

SAID_TO_ME = frozenset(("answered", "asked", "discussed", "explained", "mentioned", "said",
                        "talked", "told"))
HARD = re.compile(r"\b(?:died|dying|death|passed away|funeral|burial|cremation|miscarriage|"
                  r"stillborn|hospital|hospice|cancer|diagnosis|suicide)\b", re.I)

CONTACT_REPLIES = (
    "Then it's with them now - what did they say?",
    "Right. Did they give you an answer?",
    "Fair enough. What did they say?",
    "Good. Have they said anything back yet?",
)
OVER_REPLIES = (
    "Good - that's the job done. Did somebody come out in the end, or did you sort it yourself?",
    "That's a relief. What was it in the end?",
    "Good to hear it. Is it holding, or is it one of those that comes back?",
    "Right - so that's out of the way. What did it take?",
)
OVER_A_JOB_DONE = frozenset(("done", "finished", "sorted"))

OVER_NAMED_REPLIES = (
    "Good to hear it. Is the {thing} holding, or is it one of those that comes back?",
    "Good - that is the {thing} sorted then. What was it in the end?",
    "That's a relief. What was wrong with the {thing}, in the end?",
    "Right - so the {thing} is out of the way. Did it take long?",
)
OVER_NAMED_JOB_REPLIES = (
    "Right - the {thing} done then. What was the fiddly part?",
    "Good. How long did the {thing} take?",
    "That's the {thing} out of the way. Was it as big a job as it looked?",
    "Nice one. What was the {thing} like to do?",
)
REPAIRED_REPLIES = (
    "Then that's the first thing done. Is it any better since?",
    "Right - has it made a difference?",
    "Good. If it's still the same tomorrow, say and we'll go a step further.",
    "Then give it a day and tell me if it settles.",
)
CHANGED_REPLIES = (
    "Right - has it made any difference yet?",
    "Early days, then - what has changed so far?",
    "Good. How are you finding it?",
)
REPORT_REPLIES = (
    "Right - how did that go?",
    "Good. What happened when you did?",
    "Then what came of it?",
)
SETTLED_REPLIES = (
    "Good \u2014 that's that sorted, then.",
    "Nice one. One less thing on the list.",
    "Good. That is that one off your mind.",
)


def _a_crisis_line_said(memory, words):
    turns = [t for t in (memory.get("turns") or []) if isinstance(t, dict)][-2:]
    for turn in reversed(turns):
        said = str(turn.get("bot") or "").lower()
        if said and any(word in said for word in words):
            return True
    return False


def _a_hard_thread(memory):
    turns = [t for t in (memory.get("turns") or []) if isinstance(t, dict)]
    for turn in turns[-2:]:
        if HARD.search(str(turn.get("bot") or "")) or HARD.search(str(turn.get("user") or "")):
            return True
    return False


FINISHED_ACT = re.compile(
    r"^\W*(?:(?:ok|okay|so|well|yeah|yep|yes|and|but|oh|right|alright|no)\W+)*"
    r"(?:i|we|ive|i've|weve|we've|i have|we have)\W+(?:just|already|finally|now|nearly)?\W*(\w+)\W+"
    r"(?:it|them|one|that|this|everything|the lot|all of it)\b", re.I)
FINISHED_ITSELF = re.compile(
    r"^\W*(?:(?:ok|okay|so|well|yeah|yep|yes|and|but|oh|right|alright|no)\W+)*"
    r"(?:it|its|it's|that|thats|that's|all)\W+(?:is\s+|was\s+|were\s+|got\s+|gets\s+|now\s+)?"
    r"(done|sorted|fixed|finished|working|mended|booked|ordered|paid|collected|replaced)\b", re.I)
BARE_DONE = re.compile(r"^\W*(?:all\s+)?(done|sorted|finished|fixed)\W*(?:,?\s*(?:thanks|ta))?\W*$", re.I)
DONE_THAT = re.compile(r"^\W*(?:(?:ok|okay|so|well|yeah|yep|yes|and|but|oh|right|alright)\W+)*"
                       r"(done|sorted|fixed|finished|tried)\W+(?:that|this|it|them)\b", re.I)
FINISHED_STEPS = frozenset("""
    fixed done finished sorted mended repaired replaced cleaned painted hoovered tidied
    found bought ordered booked returned collected installed cleared changed
    washed rang called emailed texted paid sent submitted filled cancelled cancelled
""".split())
SETTLED = frozenset("""
    done finished sorted found bought ordered booked returned collected sent submitted
    filled cancelled canceled paid
""".split())
BARE_COMPLETION = frozenset(("done", "finished"))


def _the_step(low):
    match = ALREADY.search(low) or TRAILING.search(low)
    if not match:
        return None
    thing_after = match.re is ALREADY
    step = match.group(1)
    if step in TELLING and APOLOGY.search(low):
        return APOLOGY_STEP
    if step not in PAST and not step.endswith("ed") and step not in A_STEP_TAKEN:
        return None
    if step in SAME_AS_PRESENT and thing_after:
        tail = [word for word in re.findall(r"[a-z0-9']+", low[match.end():])
                if word not in POINTS_AT]
        if not tail:
            return None
    return step


MORE_PADDING = DID_TAIL | frozenset("""thanks ta cheers brilliant great good nice lovely
perfect out off up properly""".split())
KEPT_UP = re.compile(r"\b(?:keep\s+(?:walking|going|doing|at\s+it|it\s+up|an?\s+eye)|"
                     r"carry\s+on|every\s+day|each\s+day|twice\s+a\s+(?:day|week)|"
                     r"a\s+day|a\s+week|stick\s+(?:with|to)|a\s+habit|"
                     r"one\s+day\s+at\s+a\s+time)\b", re.I)


def _nothing_more(low, match):
    tail = re.findall(r"[a-z']+", low[match.end():])
    return all(word in MORE_PADDING for word in tail)


def _a_job_with_an_end(answer):
    first = re.split(r"(?<=[.!?])\s+", str(answer or "").strip())[0]
    return not KEPT_UP.search(first)


def _the_finished_step(low, memory=None):
    step = None
    match = FINISHED_ACT.search(low)
    if match:
        found = match.group(1)
        if (found in FINISHED_STEPS or found == "did") and _nothing_more(low, match):
            step = "done" if found == "did" else found
    if not step:
        match = FINISHED_ITSELF.search(low) or BARE_DONE.match(low) or DONE_THAT.match(low)
        if match:
            if not _nothing_more(low, match):
                return None
            step = match.group(1).lower()
    if step in BARE_COMPLETION and not _a_job_with_an_end(_the_last_answer(memory or {})):
        return None
    return step


TELLING = frozenset(("told", "said", "spoken", "texted", "messaged", "written", "apologised"))
APOLOGY_STEP = "apologise"
APOLOGY = re.compile(r"\b(?:apolog\w*|sorry)\b")


def the_step_they_took(text, memory=None):
    low = " ".join(str(text or "").lower().split())
    if not low or "?" in low:
        return None
    words = low.split()
    if len(words) > MOST_WORDS:
        return None
    if TO_THE_BOT.search(low):
        return None
    over = the_trouble_is_over(low)
    if over:
        if _a_hard_thread(memory or {}):
            return None
        return over
    if ASKING.search(low) and not DID.search(low):
        return None
    step = _the_step(low) or _the_step_after_did(low) or _the_finished_step(low, memory)
    if not step:
        return None
    if _a_hard_thread(memory or {}):
        return None
    return step


POINTS_AT = frozenset("""it its it's them that this these those one ones him her all everything
    both lot""".split())
IRREGULAR = {"bled": "bleed", "tried": "try", "rang": "ring", "told": "tell", "paid": "pay",
             "made": "make", "took": "take", "went": "go", "saw": "see", "spoke": "speak",
             "wrote": "write", "sent": "send", "bought": "buy", "gave": "give", "put": "put",
             "ran": "run", "came": "come", "did": "do", "fed": "feed",
             "led": "lead", "set": "set", "cut": "cut", "read": "read", "hit": "hit"}
A_STEP_TAKEN = frozenset(IRREGULAR) - frozenset(("did", "said"))
SAME_AS_PRESENT = frozenset(word for word, now in IRREGULAR.items() if word == now)


AN_OUTCOME = frozenset("""fixed mended repaired sorted done finished""".split())


OVER_WORD = re.compile(r"\b(fixed|mended|repaired|sorted|done|working|works|up\s+and\s+running)\b", re.I)
OVER_STATE = re.compile(r"\b(?:is|are|was|were|'s|been|got|now|still|its|it's)\b", re.I)
OVER_GOT = frozenset(("got",))
OVER_PEOPLE = frozenset("""mates friends everyone everybody people kids children family folks
lads girls boys others us them they we i life lives""".split())
_NEGATION_STEM = r"(?:is|are|was|were|do|does|did|have|has|had|wo|ca|ai|nee|must|could|would|should)"
OVER_NOT = re.compile(
    r"\b(?:not|never|nothing|none|until|till|til|before|when|if|unless|once|yet|should|need|needs|"
    r"want|wants)\b|\b" + _NEGATION_STEM + r"n'?t\b", re.I)
OVER_ADJECTIVE = frozenset("""rate rates price prices term terms fee fees cost costs charge
charges nights night hours hours salary contract deal amount penalty budget rent appointment
time day week month year in up point order place""".split())
OVER_NOT_A_THING_NAMED = frozenset("""match matches game games race races fight fight vote votes
election elections draw draw lottery raffle bet bets trial trials contest competition fixture
competitions tournament score result results odds price prices""".split())
OVER_A_MEAL = frozenset("""dinner tea lunch breakfast supper brunch food meal meals roast cake
cakes bread pastry curry stew soup pizza""".split())
OVER_STYLED = frozenset("""hair hairs nails nail lashes brows eyebrows makeup make-up face
beard fringe colour color dye highlights""".split())
OVER_LEAD = frozenset("""my our your his her their its it's the a an this that these those both
whole old new little big other same own""".split())
OVER_NO_THING = frozenset("""i we he she they you me us them it its it's that thats that's this
everything all nothing something anything someone somebody""".split())
OVER_BETWEEN = frozenset("""is are was were s been got gets get now still finally again just
at last always never""".split())
OVER_STOP = frozenset("""and but so because after when if until since although though while
than then also plus with""".split())
NOT_A_THING_SAID_BACK = re.compile(
    r"^(?:s?he'?s|i'?m|i'?ve|they'?re|they'?ve|you'?re|you'?ve|we'?re|we'?ve|it'?s|that'?s|"
    r"there'?s|theres|whats|what'?s|we|us|there)\b", re.I)
OVER_NEVER_A_THING = frozenset("""is are was were be been being am do does did have has had will
would can cant could shall should may might must not never isnt arent wasnt werent dont doesnt
didnt havent hasnt hadnt wont wouldnt couldnt shouldnt mustnt aint""".split())


def _the_thing_said(low, at):
    words = low[:at].split()
    while words and (words[-1].strip(".,!'") in OVER_BETWEEN
                     or words[-1].strip(".,!'") in OVER_STOP):
        words.pop()
    if not words:
        return None
    thing = []
    for raw in reversed(words):
        bare = raw.strip(".,!'")
        if not thing and bare in OVER_NO_THING:
            return None
        if (bare in OVER_LEAD or bare in OVER_STOP or bare in OVER_BETWEEN
                or bare in OVER_NEVER_A_THING):
            break
        if bare in OVER_NO_THING:
            return None
        thing.append(bare)
        if len(thing) == 2:
            break
    if not thing:
        return None
    thing = " ".join(reversed(thing))
    if NOT_A_THING_SAID_BACK.match(thing) or "".join(thing.split()).isdigit():
        return None
    head = thing.split()[-1]
    if head in OVER_NOT_A_THING_NAMED or head in OVER_A_MEAL or head in OVER_STYLED:
        return False
    return thing


def the_thing_that_is_mended(text):
    word, at, low = _the_over_word(text)
    if not word:
        return None
    thing = _the_thing_said(low, at)
    return thing or None


OVER_ASKING = re.compile(r"^\W*(?:is|are|was|were|do|does|did|has|have|had|will|would|shall|"
                         r"can|could|should|may|might|when|what|whats|what's|how|why|where|who|"
                         r"which|if|isnt|isn't|wasnt|wasn't)\b", re.I)


_CLAUSE_BREAK = re.compile(
    r"[,;:\u2014\u2013]|\b(?:" + "|".join(sorted(OVER_STOP)) + r")\b", re.I)


def _the_clause(low, at):
    start, end = 0, len(low)
    for match in _CLAUSE_BREAK.finditer(low):
        if match.end() <= at:
            start = match.end()
        elif match.start() >= at:
            end = match.start()
            break
    return low[start:end]


def _the_over_word(text):
    low = " ".join(str(text or "").lower().split())
    if not low or "?" in low or len(low.split()) > MOST_WORDS:
        return None, -1, low
    if OVER_ASKING.search(low):
        return None, -1, low
    words = low.split()
    for match in OVER_WORD.finditer(low):
        word = match.group(1)
        at = len(low[:match.start()].split())
        after = words[at + 1] if at + 1 < len(words) else ""
        if after.strip(".,!") in OVER_ADJECTIVE:
            continue
        near = [w.strip(".,!'") for w in words[max(0, at - 4):at]]
        if any(w in OVER_GOT for w in near):
            first = next(i for i, w in enumerate(near) if w in OVER_GOT)
            near = [w for i, w in enumerate(near) if i >= first or w not in OVER_PEOPLE]
        window = " ".join(near)
        if any(w in OVER_PEOPLE for w in near):
            continue
        if OVER_NOT.search(_the_clause(low, match.start())):
            continue
        if OVER_STATE.search(window):
            if _the_thing_said(low, match.start()) is False:
                continue
            return word, match.start(), low
    return None, -1, low


def the_trouble_is_over(text):
    return _the_over_word(text)[0]


def _gave_a_step(answer):
    try:
        from ..compose import verdict
        return bool(verdict._an_instruction_sentence(answer))
    except Exception:
        return False


def _the_opening_of(answer):
    text = str(answer or "").strip()
    for index, char in enumerate(text):
        if char in ".!?" and index + 1 < len(text) and text[index + 1] == " ":
            return text[:index + 1]
    return text


def _says_the_step(step, answer):
    if step == APOLOGY_STEP or step.startswith("apolog"):
        return bool(SAYS_APOLOGY.search(str(answer or "").lower()))
    if step in AN_OUTCOME:
        return _gave_a_step(answer)
    word = IRREGULAR.get(step, step)
    if len(word) >= 4 and word.endswith("ed"):
        stem = word[:-2]
    elif len(word) >= 4 and word.endswith("e"):
        stem = word[:-1]
    else:
        stem = word
    for other in re.findall(r"[a-z]+", str(answer or "").lower()):
        if other.startswith(stem) or (len(other) >= 4 and word.startswith(other)):
            return True
    return False


def takes_as_it_comes(text, memory):
    try:
        if not reply_for(text, memory):
            return False
        step = the_step_they_took(text, memory)
        if not step:
            return False
        if the_trouble_is_over(text):
            return True
        return _says_the_step(step, _the_last_answer(memory or {}))
    except Exception:
        return False


STEPS_LEADS = (
    "Then {said}.",
    "Right - {said}.",
    "Then that part is out of the way: {said}.",
    "Next: {said}.",
)
NOT_A_THING_WORD = frozenset("""already i ive we ve have had the a an it them that this those these
and but so oh ok okay well yeah yep no nah right alright then my our your his her their of to in
on at for with off out up down just still even really very much more some any all""".split())
REPORT_FILLER = frozenset("""did done do does though tho although again twice once back away around
round through over really actually honestly literally anyway anyways too also even just still
yet since today yesterday tomorrow morning afternoon evening night last week month year now
then before after first both either one ones thing stuff much many lot bits bit little quite
rather sort kind suppose guess think know said says told tell mean meant""".split())
MOST_STEPS = 4
NOT_A_STEP_START = frozenset("""less though although but and or so plus with without unless
whereas while which that who also still both either neither than then-as-i""".split())
CONDITION_START = re.compile(r"^(?:if|when|once|should)\b", re.I)


SAYS_APOLOGY = re.compile(r"\b(?:apolog\w*|say sorry|says sorry|say you'?re sorry|"
                          r"i'?m sorry|i am sorry|sorry for)\b")


def _the_steps_after(step, answer, line=""):
    from . import limit as a_limit
    try:
        steps = [str(one).strip() for one, _ in a_limit._steps(answer) if str(one).strip()]
    except Exception:
        return []
    if not steps:
        return []
    word = IRREGULAR.get(step, step).lower()
    if len(word) > 4 and word.endswith("ed"):
        stem = word[:-2]
    elif len(word) > 3 and word.endswith("e"):
        stem = word[:-1]
    else:
        stem = word
    wanted = {other for other in re.findall(r"[a-z']+", str(line or "").lower())
              if other not in NOT_A_THING_WORD and other not in REPORT_FILLER
              and not other.startswith(stem) and len(other) > 1}
    best, best_score = None, 0
    for index, sentence in enumerate(steps):
        words = set(re.findall(r"[a-z']+", sentence.lower()))
        score = len(words & wanted)
        if stem in sentence.lower():
            score += 1
        if score > best_score:
            best, best_score = index, score
    if best is None or (wanted and best_score < 2):
        return []
    after = [_the_instruction_of(one.strip().rstrip(" .,;")) for one in steps[best + 1:]]
    kept = []
    in_condition = False
    for index, one in enumerate(after):
        if not one:
            break
        if not kept and one.split()[0].lower().strip(",:") in NOT_A_STEP_START:
            break
        if one[:1].isupper():
            if in_condition or not CONDITION_START.match(one):
                break
            in_condition = True
        kept.append(one)
        if len(kept) >= MOST_STEPS:
            break
    return kept


def _the_instruction_of(step):
    head, colon, tail = str(step or "").partition(":")
    if not colon or len(head.split()) < 2:
        return step
    return head.strip().rstrip(" .,;")


def _with_steps(after, memory):
    said = ", ".join(step[0].lower() + step[1:] if step[0].isupper() else step
                     for step in after)
    said = said.rstrip(" .")
    said = re.sub(r"^(?:and\s+)?then\s+", "", said, flags=re.IGNORECASE)
    from ..compose import fallback
    return fallback._choose(STEPS_LEADS, memory or {}, said).format(said=said)


def _the_last_answer(memory):
    turns = [t for t in (memory.get("turns") or []) if isinstance(t, dict) and t.get("bot")]
    last = str(turns[-1].get("bot")) if turns else ""
    from . import plan as plan_steps
    try:
        return plan_steps.the_answer_in_hand(memory) or last
    except Exception:
        return last


def tells_them_the_step_again(reply, text, memory):
    try:
        step = the_step_they_took(text, memory)
    except Exception:
        return False
    if not step:
        return False
    if the_trouble_is_over(text):
        return True
    try:
        return _says_the_step(step, reply)
    except Exception:
        return False


def _of_a_thing(step, text):
    if step not in CHANGED_OF_A_THING:
        return False
    words = re.findall(r"[a-z']+", str(text or "").lower())
    try:
        at = words.index(step)
    except ValueError:
        return False
    after = words[at + 1:]
    if any(word in CHANGED_NOTHING_BROKEN for word in after):
        return False
    return not any(word in A_LIFE_OBJECT for word in after)


def _only_finished(text):
    low = " ".join(str(text or "").lower().split())
    if _the_step(low) or _the_step_after_did(low):
        return False
    return bool(_the_finished_step(low))


def _the_part_after(answer, step_text):
    from . import limit as a_limit
    try:
        pieces = [str(one).strip() for one, _ in a_limit._steps(answer) if str(one).strip()]
    except Exception:
        return []
    if not pieces:
        return []
    wanted = {word for word in re.findall(r"[a-z']+", str(step_text or "").lower())
              if len(word) > 1 and word not in NOT_A_THING_WORD}
    best, best_score = None, 0
    for index, piece in enumerate(pieces):
        score = len(set(re.findall(r"[a-z']+", piece.lower())) & wanted)
        if score > best_score:
            best, best_score = index, score
    if best is None or best_score < 2:
        return []
    for piece in pieces[best + 1:]:
        piece = re.sub(r"^(?:and|then|but|so)\s+", "", piece, flags=re.I).strip().rstrip(" .,;")
        if not piece:
            continue
        if CONDITION_START.match(piece):
            return [piece]
        if piece[:1].isupper():
            break
    return []


def after_the_step_handed_back(text, memory):
    if not isinstance(memory, dict):
        return None
    turns = [t for t in (memory.get("turns") or []) if isinstance(t, dict)]
    if not turns:
        return None
    step = str(memory.get("handed_back_text") or "")
    answer = str(memory.get("handed_back_answer") or "")
    if not step or not answer or memory.get("handed_back_step") != len(turns) - 1:
        return None
    from . import tried
    try:
        if not tried.still_the_state(text, memory):
            return None
        after = _the_part_after(answer, step)
    except Exception:
        return None
    if not after:
        return None
    return _with_steps(after, memory)


def reply_for(text, memory):
    try:
        step = the_step_they_took(text, memory)
    except Exception:
        return None
    if not step:
        return after_the_step_handed_back(text, memory)
    if not _the_last_answer(memory or {}) and _only_finished(text):
        return None
    if the_trouble_is_over(text):
        from ..compose import fallback
        if _a_crisis_line_said(memory or {}, fallback.CRISIS_WORDS):
            return None
        thing = the_thing_that_is_mended(text)
        if thing:
            job = the_trouble_is_over(text) in OVER_A_JOB_DONE
            pool = OVER_NAMED_JOB_REPLIES if job else OVER_NAMED_REPLIES
            said = fallback._choose(pool, memory or {}, fallback.memory_bot(memory or {}),
                                    seed_text=text)
            return said.replace("{thing}", thing)
        return fallback._choose(OVER_REPLIES, memory or {}, fallback.memory_bot(memory or {}),
                                seed_text=text)
    if step in SAID_TO_ME and not there_is_a_chat(memory or {}):
        return pick(FIRST_LINE_REPLIES, memory or {}, seed_text=str(text or ""))
    try:
        if (step not in BARE_COMPLETION and repeat._tried(text)
                and repeat._later_part(text, _the_last_answer(memory or {}))):
            return None
    except Exception:
        pass
    try:
        if step in BARE_COMPLETION:
            after = []
        else:
            after = _the_steps_after(step, _the_last_answer(memory or {}), str(text or ""))
    except Exception:
        after = []
    if after:
        return _with_steps(after, memory)
    if (step in A_STEP_TAKEN and step not in CONTACT and step not in TELLING
            and _the_last_answer(memory or {})):
        if not _says_the_step(step, _the_opening_of(_the_last_answer(memory or {}))):
            return None
    if step in NOBODY_TO_ANSWER or (step in CONTACT and AN_APOLOGY.search(str(text or ""))):
        pool = REPORT_REPLIES
    elif step in CONTACT:
        pool = CONTACT_REPLIES
    elif step in REPAIRED or _of_a_thing(step, text):
        pool = REPAIRED_REPLIES
    elif step in CHANGED:
        pool = CHANGED_REPLIES
    elif step in SETTLED:
        pool = SETTLED_REPLIES
    else:
        pool = REPORT_REPLIES
    from ..compose import fallback
    last = fallback.memory_bot(memory or {})
    return fallback._choose(pool, memory or {}, last)
