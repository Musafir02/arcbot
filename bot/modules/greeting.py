import re

from ..compose import breakup
from ..compose import fallback
from ..compose import findout, gap
from ..compose import moving
from ..compose import quantity
from ..compose import no_page
from ..compose import the_course_of_it
from ..compose import checking
from ..compose import goodnews
from ..compose import griefplea
from ..compose import hands
from ..compose import how_it_went
from ..compose import liveask
from ..compose import missing_half
from ..compose import onscreen
from ..compose import own_facts, plans
from ..compose import stretches
from ..compose import safety_doubt
from ..compose import only_they_know
from ..compose import rule
from ..compose import their_day
from ..compose import their_life
from ..compose import taste
from ..compose import the_turn_after
from ..compose import find_a_place
from ..compose import onmybehalf
from ..compose import a_document_lives_with_an_office
from ..compose import a_place_nobody_can_see
from ..memory import ack, detail, matters, obstacle, repeat, too_late
from ..compose import pleased
from ..compose import rotten_luck
from ..compose import said_about_me
from ..compose import nottheirbest
from ..compose import no_eyes
from ..compose import who_to_see
from ..compose import remark
from ..compose import setting_off
from ..memory import ack
from ..memory import back_again
from ..memory import their_feeling

PRIORITY = -1000

A_REFERS_BACK = re.compile(
    r"\b(?:you|u|yous)\s+(?:said|told me|mentioned|suggested|advised|recommended|agreed|"
    r"promised|told me to)\b"
    r"|^(?:(?:o+|oh|and|so|ok|okay|right|now|but|well|anyway|erm|um)\s+)*"
    r"(?:back|going back|return|coming back)\s+to\s+(?:what|that|it|this|where|our|the)\b"
    r"|^(?:(?:o+|oh|and|so|ok|okay|right|now|but|well|anyway|erm|um)\s+)*"
    r"(?:what|which)\s+(?:was|were)\s+we\b"
    r"|\bwhat we (?:were|was) (?:saying|talking about|on about)\b"
    r"|\b(?:the )?same (?:as )?(?:before|last time)\b"
    r"|\bthat thing i (?:told|mentioned|said to|asked) you\b"
    r"|\bas (?:we|you) (?:said|were saying|agreed|discussed)\b"
    r"|\bas i (?:said|mentioned|told you)\b")

NOTHING_BEFORE_IT = (
    "There's nothing before this line for me to go on - say what it was about and I'll pick it up.",
    "I haven't said anything yet, so give me the thing itself: what are we going back to?",
    "Nothing on my side yet - tell me what it was and I'll take it from there.",
    "That's the first thing you've said to me, so I'll need it in full: what was it about?",
)


def _a_line_pointing_back_at_nothing(clean, memory):
    if not isinstance(memory, dict):
        return None
    if [turn for turn in (memory.get("turns") or []) if isinstance(turn, dict)]:
        return None
    if not A_REFERS_BACK.search(clean or ""):
        return None
    return fallback._choose(NOTHING_BEFORE_IT, memory, clean)


def respond(text, memory):
    from ..memory import tried as not_moved
    going_on = not_moved.reply_for(text, memory)
    if going_on:
        return going_on
    who = who_to_see.reply_for(text, memory)
    if who:
        return who
    came_back = back_again.reply_for(text, memory)
    if came_back:
        return came_back
    about_them = their_feeling.reply_for(text, memory)
    if about_them:
        return about_them
    back_at_nothing = _a_line_pointing_back_at_nothing(
        " ".join(str(text or "").lower().split()), memory)
    if back_at_nothing:
        return back_at_nothing
    against = quantity.the_figure_against_the_answer(text, memory)
    if against:
        return against
    accepted = fallback.a_doable(text, memory)
    if accepted:
        return accepted
    verdict = (fallback.reads_as_a_verdict(text, memory)
               and not fallback.a_verdict_stands_down(memory))
    a_comment = fallback.reads_as_a_verdict(text, memory)
    carried = None if a_comment else detail.answer_for(text, memory)
    if carried:
        return carried
    objected = None if a_comment else obstacle.answer_for(text, memory)
    if objected:
        return objected
    described = no_eyes.what_they_described(text, memory)
    if described:
        return fallback._choose(described, memory, text) or ""
    reported = detail.a_report_about_the_thing(text, memory)
    if reported:
        return reported
    corrected = matters.a_corrected_age(text, memory)
    if corrected:
        return corrected
    off_to = None if a_comment else moving.reply_for(text, memory)
    if off_to:
        return off_to
    tasted = taste.reply_for(text, memory)
    if tasted:
        return tasted
    from ..compose.tone_again import retone
    retoned = retone(memory, text)
    if retoned:
        return retoned
    serious = safety_doubt.reply_for(text, memory)
    if serious:
        return serious
    reply = fallback.reply_for(text, memory)
    if not a_comment:
        in_the_room = no_eyes.a_thing_in_the_room_over_a_placeholder(text, reply)
        if in_the_room:
            return fallback._choose(in_the_room, memory, text) or ""
        if no_eyes._is_a_placeholder(reply) or fallback.is_a_hedge(reply):
            for pool in (no_eyes.a_contact_they_handed_over(text),
                         no_eyes.a_recording_they_offer(text)):
                if pool:
                    return fallback._choose(pool, memory, text) or ""
    if reply and (fallback._in_a_pool(reply, (fallback.A_SMALL_DAY,))
                  or ack.reads_as_a_receipt(reply)):
        of_mine = remark.a_thing_of_theirs_reply_for(text, text.split(), memory)
        if of_mine:
            return of_mine
    judged_line = said_about_me.reads_as_reported_judgement(text)
    nothing_yet = (not reply or fallback._nothing_to_stand_behind(reply)
                   or (judged_line and said_about_me.speaks_to_a_self_judgement(reply)))
    if not a_comment and nothing_yet:
        judged = said_about_me.answer_for(text, memory) or said_about_me.answer_followup(
            text, memory)
        if judged:
            return judged
    not_a_body = breakup.answer_for(text, reply, memory)
    if not_a_body:
        return not_a_body
    keeping_going = griefplea.reply_for(text, reply, memory)
    if keeping_going:
        return keeping_going
    reply = first_line_points_back_at_nothing(reply, memory)
    years_back = goodnews.reply_for_a_year_ago(text, reply, memory)
    if years_back:
        return years_back
    stretch = stretches.the_stretch_said_back(text, memory, reply)
    if stretch:
        return stretch
    if not a_comment and reply and fallback._nothing_to_stand_behind(reply):
        refused = obstacle.a_move_refused(text, memory)
        if refused:
            return refused
    if reply and (fallback._nothing_to_stand_behind(reply) or fallback._is_a_hedge(reply)):
        cannot_use = obstacle.answer_for_a_thing_they_cannot_use(text, memory)
        if cannot_use:
            return cannot_use
    rest = the_step_they_have_not_had(text, memory, reply)
    if rest:
        return rest
    if reply and (fallback._nothing_to_stand_behind(reply) or fallback._is_a_hedge(reply)
                  or fallback._in_a_pool(reply, (fallback.A_SMALL_DAY,))):
        from ..memory.the_verdict import answer_for as _verdict_for

        verdict_answer = _verdict_for(text, memory)
        if verdict_answer:
            return verdict_answer
    if reply and fallback._is_a_hedge(reply):
        again_asked = repeat.the_same_question_again(text, memory)
        if again_asked:
            return again_asked
        outcome = fallback.an_outcome_asked_about_someone(text, memory)
        if outcome:
            return outcome
        figure = repeat.the_figure_asked(text, memory)
        if figure:
            return figure
        figure = repeat.the_figure_they_gave(text, memory)
        if figure:
            return figure
        from ..compose import is_it_worth_it
        worth = is_it_worth_it.is_it_worth_it(text, memory, reply)
        if worth:
            return worth
    back = repeat.asked_back(text, memory)
    if back and not repeat.carries_the_figure(back, reply):
        return back
    if reply and fallback._is_a_hedge(reply):
        late = too_late.answer_for(text, memory)
        if late:
            return late
    if reply and (fallback._is_a_hedge(reply)
                  or fallback._in_a_pool(reply, (fallback.NEUTRAL,))):
        checks = checking.the_checks_already_named(text, memory)
        if checks:
            return checks
    if reply and fallback._is_a_hedge(reply):
        theirs = how_it_went.answer_for(text, memory)
        if theirs:
            return theirs
    if reply and fallback._is_a_hedge(reply):
        own = own_facts.answer_for(text, memory)
        if own:
            return own
    if reply and fallback._is_a_hedge(reply):
        past = own_facts.about_earlier_chats(text, memory)
        if past:
            return past
    if reply and fallback._is_a_hedge(reply):
        taught = own_facts.learns_from_the_chat(text, memory)
        if taught:
            return taught
    if reply and fallback._is_a_hedge(reply):
        plan = plans.answer_for(text, memory)
        if plan:
            return plan
    if reply and (fallback._is_a_hedge(reply) or fallback._nothing_to_stand_behind(reply)
                  or setting_off.is_a_pointer(reply)):
        off = setting_off.answer_for(text, memory)
        if off:
            return off
    if reply and (fallback._is_a_hedge(reply) or fallback._nothing_to_stand_behind(reply)):
        gave = (None if (fallback._thread_is_about_the_body(memory)
                         or fallback._the_thread_is_heavy(memory))
                else how_it_went.the_answer_they_gave(text, memory))
        if gave:
            return gave
    if reply and fallback._is_a_hedge(reply):
        owned = rule.answer_for(text, memory)
        if owned:
            return owned
    if reply and fallback._is_a_hedge(reply):
        named = checking.answer_for(text, memory)
        if named:
            return named
    if reply and fallback._is_a_hedge(reply):
        glad = pleased.answer_for(text, memory)
        if glad:
            return glad
    if reply and fallback._is_a_hedge(reply):
        thread = fallback.the_threads_answer(text, memory)
        if thread:
            return thread
    if reply and (fallback._is_a_hedge(reply) or reply.startswith(their_day.WHO_TO_ASK)):
        asked_back = their_day.pool_for(text, care=fallback._the_thread_is_heavy(memory))
        if asked_back:
            return fallback._choose(asked_back, memory, text)
    if reply and (fallback._is_a_hedge(reply) or fallback._nothing_to_stand_behind(reply)):
        after = the_turn_after.answer_for(text, memory)
        if after:
            return after
    if reply and fallback._is_a_hedge(reply):
        own = their_day.own_fact_for(text, memory)
        if own:
            return own
        parts = no_page.reply_for(text, memory)
        if parts:
            return parts
    if reply and (fallback._is_a_hedge(reply) or fallback._is_an_ask_which_bit(reply)):
        course = the_course_of_it.reply_for(text, memory)
        if course:
            return course
    deciding = liveask.answer_for(text, memory, reply)
    if deciding:
        return deciding
    if reply and fallback._is_a_hedge(reply):
        one_half = missing_half.the_missing_half(text, memory)
        if one_half:
            return one_half
    if reply and fallback._is_a_hedge(reply):
        if not a_comment:
            plain = detail.the_plain_ask(text, memory)
            if plain:
                return plain
        on_screen = onscreen.the_answer_on_screen(text, memory)
        if on_screen:
            return on_screen
    if reply and fallback._is_a_hedge(reply):
        from ..memory import asked_about

        asked = asked_about.the_answer_this_chat_gave(text, memory)
        if asked:
            return asked
    if reply:
        not_good = rotten_luck.answer_for(text, memory, reply)
        if not_good:
            return not_good
    low_day = nottheirbest.answer_for(text, reply, memory)
    if low_day:
        return low_day
    if reply and reply[:40] in [line[:40] for line in fallback.UNKNOWN]:
        only = only_they_know.answer_for(text, memory)
        if only:
            return only
    if reply and (fallback._is_a_hedge(reply)
                  or a_document_lives_with_an_office.a_map_app_line(reply)
                  or a_document_lives_with_an_office.a_lost_record(text, reply)):
        held = a_document_lives_with_an_office.answer_for(text, memory, reply)
        if held:
            return held
    if reply and (fallback._is_a_hedge(reply) or reply in find_a_place.A_NOD):
        here = (None if find_a_place.already_a_route(reply)
                else find_a_place.answer_for(text, memory))
        if here:
            return here
    if reply:
        handed = onmybehalf.answer_for(text, memory, reply)
        if handed:
            return handed

    if reply and fallback._is_a_hedge(reply):
        judged = a_place_nobody_can_see.answer_for(text, memory, reply)
        if judged:
            return judged
    if reply and fallback._is_a_hedge(reply):
        from ..compose import what_i_do_know
        known = what_i_do_know.reply_for(text, memory, reply)
        if known:
            return known

    if repeat.answers_nothing(reply):
        part = repeat.the_part_asked(text, memory)
        if part:
            return part
        if not repeat.the_advice_was_to_get_seen(memory):
            knows = repeat.what_it_knows(text, memory)
            if knows:
                return knows

    understood = memory.get("understood")
    clean = ((understood.get("clean") if isinstance(understood, dict) else None)
             or " ".join(text.lower().split()))
    thinner = bool(reply) and (fallback._in_a_pool(reply, (fallback.NEUTRAL,))
                               or (fallback._is_a_hedge(reply)
                                   and (findout.reads_as_busy(clean)
                                        or not findout.says_where_to_look(reply))))
    if thinner:
        elsewhere = findout.pool(clean, memory) or findout.more_about_the_journey(clean, memory)
        if not elsewhere and fallback._in_a_pool(reply, (fallback.NEUTRAL,)):
            elsewhere = findout.pool_over_a_receipt(clean)
        if elsewhere:
            return fallback._choose(elsewhere, memory, clean)
    if reply and fallback._is_a_hedge(reply):
        looked = findout.on_the_thing(text, memory, memory.get("understood"))
        if looked:
            return looked
    if reply and (fallback._is_a_hedge(reply) or gap.names_only_a_page(reply)) \
            and not gap.names_the_paper(reply):
        gap_lines = gap.pool(clean)
        if gap_lines:
            return fallback._choose(gap_lines, memory, clean)
    a_place = (fallback._is_a_hedge(reply)
               or fallback._in_a_pool(reply, (fallback.NEUTRAL, fallback.A_SMALL_DAY))
               or ack.reads_as_a_receipt(reply))
    if not a_place and hands.writes_the_words(text):
        a_place = fallback._in_a_pool(reply, (fallback.ACTS_FOR_ME,))
    if a_place:
        hands_reply = hands.reply_for(text, memory)
        if hands_reply:
            return hands_reply
    if reply and fallback._is_a_hedge(reply):
        own_life = their_life.reply_for(text, memory)
        if own_life:
            return own_life
    return reply


A_STEP_IN_IT = ("check", "clear", "tr", "us", "put", "add", "set", "switch", "turn", "leav",
                "keep", "ask", "tak", "replace", "restart", "update", "mov", "clean", "fix",
                "buy", "get", "call", "ring", "book", "look", "mak", "run", "wash", "charg",
                "delet", "start", "install", "plug", "test", "measur", "wip", "help", "need",
                "work", "cost", "sav")
PUSHING_BACK = re.compile(r"\b(?:though|but|actually|still|to be honest|honestly)\b", re.I)
SIGNING_OFF = ("hope", "good luck", "sorry", "take care", "all the best", "let me know",
               "good question", "that said")
SENTENCE = re.compile(r"(?<=[.!?])\s+")
QUOTE_MARK = re.compile(r"[\u2018\u2019\u201c\u201d\"]|(?<![A-Za-z])'|'(?![A-Za-z])")


_POINTS_BACK = re.compile(
    r"^(?:so[, ]+)?(?:where were we|where did we get to|what were you saying|"
    r"what were we saying|what were we talking about|what was i saying)[?.!]*$"
    r"|^(?:and )?back to (?:it|that|what we were saying|what we were talking about)[.!]*$"
    r"|^(?:as|like) (?:i|we) (?:said|were saying|mentioned)[.!]*$",
    re.I)
_GO_ON = "Go on - what has been happening?"


def first_line_points_back_at_nothing(reply, memory):
    if not isinstance(reply, str) or not reply.strip():
        return reply
    memory = memory if isinstance(memory, dict) else {}
    said_before = [one for one in (memory.get("turns") or []) if isinstance(one, dict)]
    if any(str(one.get("bot") or "").strip() for one in said_before):
        return reply
    sentences = [one for one in SENTENCE.split(reply.strip()) if one.strip()]
    if not sentences or not _POINTS_BACK.match(sentences[-1].strip()):
        return reply
    kept = " ".join(one for one in sentences[:-1] if one.strip())
    if not kept:
        return _GO_ON
    return kept if len(kept.split()) > 6 else kept + " " + _GO_ON


def sentences_of(answer):
    out, start = [], 0
    for match in SENTENCE.finditer(answer):
        piece = answer[start:match.start()]
        if len(QUOTE_MARK.findall(piece)) % 2:
            continue
        out.append(piece.strip())
        start = match.end()
    out.append(answer[start:].strip())
    return [one for one in out if one]
THEN_TAIL = re.compile(r"\bthen\b,?\s*", re.I)
PLAIN = frozenset("""about after again all already also and any are because been before being but
both can could did does doing done dont down each even ever every for from get got had has have
having her here hers him his how into its just know like made make many more most much must my
never not now off on once one only other our out over own said same says she should since some
still such than that the their them then there these they thing things think this those though
through time too took under until very was way were what when where which while who why will with
would yes yet you your youre ive im id ill youve weve theyre isnt dont cant didnt wasnt
havent hasnt wouldnt couldnt shouldnt thats whats lets okay ok min little bit lot thing
stuff""".split())
RESTART = re.compile(r"\b(?:turn\w*|switch\w*|restart\w*|reboot\w*|reset\w*|unplug\w*|"
                     r"plug\w*|power\w*|off)\b")


def _a_step_of_this_answer(text, answer):
    words = [word for word in re.findall(r"[a-z']+", str(text or "").lower())
             if len(word) > 2 and word not in PLAIN]
    theirs = {word[:5] for word in re.findall(r"[a-z']+", str(answer or "").lower())}
    restarting = bool(RESTART.search(str(text or "").lower())) and bool(
        RESTART.search(str(answer or "").lower()))
    for word in words:
        if word[:5] in theirs or (restarting and RESTART.search(word)):
            continue
        return False
    return bool(words)
A_DETAIL_OF_IT = re.compile(
    r"\b(?:in|on|at|by|near|under|over|behind|inside|outside|next to)\s+(?:the|a|an|my|our|his|her|their)?\s*[a-z]+"
    r"|\b(?:it|its|it's|they|theyre|they're|he|she|that|this|there)\s*"
    r"(?:'s|s| is| are| was| were| arent| isn't| isnt)\s+(?:a|an|the|not|quite|just|still|only)?\s*[a-z]+"
    r"|\b(?:they|he|she|we|you|it)\s+(?:only\s+|just\s+|already\s+|also\s+)?[a-z]+ed\b",
    re.I)
A_FACT_OF_THEIRS = re.compile(
    r"\b(?:my|our|his|her|their|the)\s+[a-z]+\s+(?:is|are|was|were)\s+[a-z0-9]+", re.I)
DONE_A_STEP = re.compile(
    r"\b(?:i|ive|i've|i've)\s*(?:have\s+)?(?:already\s+)?(?:[a-z]+ed|done|tried|did)\b"
    r"|\b(?:did|tried|done) (?:that|it|this)(?: already)?\b"
    r"|\balready (?:did|done|tried)\b", re.I)
A_TIME_AHEAD = re.compile(
    r"\b(?:monday|tuesday|wednesday|thursday|friday|saturday|sunday|tomorrow|tonight|later|soon|"
    r"weekend|next\s+(?:week|month|year|time)|this\s+(?:morning|afternoon|evening|week|month)|"
    r"in\s+the\s+(?:morning|afternoon|evening)|in\s+(?:a|an)\s+(?:bit|while|minute|hour)|"
    r"in\s+a\s+few\s+days|after\s+work|day\s+after\s+tomorrow)\b",
    re.I)
A_DOING_SOON = re.compile(
    r"\b(?:call\w*|ring\w*|phon\w*|get\w*|sort\w*|tak\w*|book\w*|do|doing|fix\w*|go|going|"
    r"see|seeing|bring\w*|order\w*|ask\w*|contact\w*|chas\w*|email\w*|messag\w*|text\w*|"
    r"arrang\w*|hir\w*|report\w*|pop\w*|drop\w*|look\w*)\b", re.I)
PAST_TENSE = re.compile(r"ed$", re.I)
A_NEW_FACT_ABOUT_SOMEONE = re.compile(
    r"\ballerg\w*|\bintoleran\w*|\bcoeliac|\bceliac|\blactose\b"
    r"|\b(?:is|im|i'm|are|we're|were)\s+(?:a\s+)?(?:vegetarian|vegan|pescatarian)\b"
    r"|\b(?:doesnt|does not|dont|do not|wont|will not|never|can'?t|cant)\s+"
    r"(?:eat|drink|have|touch)\b",
    re.I)


def _a_plan_for_later(text):
    if DONE_A_STEP.search(text):
        return False
    if not A_TIME_AHEAD.search(text):
        return False
    for doing in A_DOING_SOON.finditer(text):
        if not PAST_TENSE.search(doing.group(0)):
            return True
    return False


def _answers_the_line(text, answer, turns=()):
    if A_DETAIL_OF_IT.search(text) or DONE_A_STEP.search(text):
        return True
    if not A_FACT_OF_THEIRS.search(text):
        return False
    named = set(fallback.content_words(text))
    if named & set(fallback.content_words(answer)):
        return True
    asked_before = " ".join(str(one.get("user") or "") for one in turns[-1:])
    return not (named & set(fallback.content_words(asked_before)))


def _said_back(text, said):
    mine = fallback._the_words(text)
    theirs = fallback._the_words(said)
    if len(mine) < 2 or not theirs:
        return False
    if fallback._is_a_hedge(said):
        return False
    shared = mine & theirs
    return len(shared) >= 2 and len(shared) / len(mine) >= 0.6


def the_step_they_have_not_had(text, memory, said):
    said = str(said or "").strip()
    an_echo = _said_back(text, said)
    a_step_done = bool(DONE_A_STEP.search(text)) and fallback._a_small_day(text, memory)
    if not said or not (an_echo or a_step_done):
        return ""
    if fallback.is_a_forecast(said):
        return ""
    if fallback.is_a_forecast(said):
        return ""
    if "?" in said and not (a_step_done and not an_echo):
        return ""
    words = re.findall(r"[a-z']+", str(text or "").lower())
    if not words or len(words) > 12 or "?" in str(text or ""):
        return ""
    turns = [one for one in (memory.get("turns") or []) if isinstance(one, dict)]
    answer = str(turns[-1].get("bot") or "").strip() if turns else ""
    if not answer or not _answers_the_line(text, answer, turns):
        return ""
    if _the_answer_again(answer, turns):
        return ""
    if PUSHING_BACK.search(text):
        return ""
    if A_NEW_FACT_ABOUT_SOMEONE.search(text):
        return ""
    if _a_plan_for_later(text):
        return ""
    if fallback.reads_as_a_verdict(text, memory) or fallback.a_verdict_stands_down(memory):
        return ""
    if a_step_done and not an_echo and not _a_step_of_this_answer(text, answer):
        return ""
    sentences = sentences_of(answer)
    candidates = []
    if len(sentences) > 1 and not (a_step_done and not an_echo):
        candidates.append(" ".join(sentences[1:3]))
    did_a_step = bool(DONE_A_STEP.search(text))
    for match in THEN_TAIL.finditer(answer):
        if not did_a_step and not _said_back(text, answer[:match.start()]):
            continue
        after = answer[match.end():].strip()
        if after:
            candidates.append(after[0].upper() + after[1:])
        break
    for leftover in candidates:
        low = leftover.lower()
        if len(leftover.split()) < 6 or low.startswith(SIGNING_OFF):
            continue
        if not detail.stands_alone(leftover):
            continue
        if leftover.rstrip().endswith("?"):
            continue
        if not any(re.search(r"\b" + step + r"\w*", low) for step in A_STEP_IN_IT):
            continue
        return leftover
    return ""


def _the_answer_again(answer, turns):
    low = " ".join(str(answer or "").lower().split())
    for one in turns[:-1]:
        earlier = " ".join(str(one.get("bot") or "").lower().split())
        if len(earlier.split()) >= 6 and earlier in low:
            return True
    return False


def takes_as_it_comes(text, memory):
    return (fallback.reads_as_about_itself(text, memory)
            or fallback.reads_as_a_tight_week(text, memory)
            or fallback.a_continuation_of_the_tight_week(memory, text)
            or fallback.reads_as_small_talk(text, memory)
            or quantity.the_figure_against_the_answer(text, memory) is not None
            or moving.reads_as_a_move_cheered(text)
            or who_to_see.replies_to_a_who_to_see(text, memory)
            or fallback.TAKES_AS_IT_COMES(text, memory))


TAKES_AS_IT_COMES = takes_as_it_comes

from ..memory import again as _said_before

respond = _said_before.replied(respond)

from ..compose import a_detail_dropped as _a_detail_dropped

respond = _a_detail_dropped.turned(respond)
