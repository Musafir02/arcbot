import importlib
import re

from ..compose import aboutness, badnews, facts, fallback, fit, leaving, onscreen
from ..compose import outlook as _outlook
from ..compose import limit as _limit
from ..memory import narrow as _narrow
from ..compose.goodnews import reads_as_a_detail_of_the_news, reads_as_the_detail_line
try:
    from ..memory import ack as _ack
except Exception:
    _ack = None
try:
    from ..memory import recall as _recall
    from ..memory import repeat as _repeat
except Exception:
    _recall = _repeat = None
try:
    from ..compose import loss as _loss
except Exception:
    _loss = None
try:
    from ..memory import dream as _dream
except Exception:
    _dream = None
try:
    from ..memory import already as _already
except Exception:
    _already = None
try:
    from ..compose import harm as _harm
except Exception:
    _harm = None
try:
    from ..memory import there_is_a_chat as _there_is_a_chat
except Exception:
    _there_is_a_chat = lambda _memory: False
try:
    from ..memory import repeat as _repeat
except Exception:
    _repeat = None
try:
    from ..memory import recall as _recall
except Exception:
    _recall = None
try:
    from ..memory import lineback as _lineback
except Exception:
    _lineback = None
try:
    from ..memory import named as _naming
except Exception:
    _naming = None
try:
    from ..compose.fallback import CARE_THREAD, PAUSE, THREAD
except Exception:
    THREAD, CARE_THREAD, PAUSE = "thread", "care-thread", "pause"
try:
    from ..compose import STEP_WHEN_LOW as _STEP_WHEN_LOW
except Exception:
    _STEP_WHEN_LOW = ()
try:
    from ..knowledge import cooking as _cooking
except Exception:
    _cooking = None
try:
    from ..compose import ruledout as _ruledout
except Exception:
    _ruledout = None

try:
    from ..memory import history as _history
except Exception:
    _history = None
try:
    from ..compose import reading as _reading
except Exception:
    _reading = None

DECLARED_TOPICS = "ANSWERS"
CHOICE = "choice"
DECLARED_INSTEAD = "ANSWERS_INSTEAD"
DECLARED_DEFERS = "DEFERS_TO"
DECLARED_AS_IT_COMES = "TAKES_AS_IT_COMES"
DECLARED_CLAIMS_INSTEAD = "CLAIMS_INSTEAD"
DECLARED_ABOUT_THE_CHAT = "ASKS_ABOUT_THE_CHAT"
OWN_ABOUT_THE_CHAT = "_about_this_chat"
SAFETY = 9000
CHATTER = 1000
RECALL = 7000
MOVE_WORDS = 26
MOVE_SHARE = 0.5
MOVE_WHOLE = 0.75
MOVE_ANSWER_WORDS = 30
WHOLE_LINE_BAND = 2000
WORD = re.compile(r"[a-z0-9]+(?:'[a-z]+)?")
LABEL_KEYS = ("id", "label", "topic", "name", "text")
READ = {}


def choose(text, memory, candidates):
    try:
        index = _choose(text, memory, candidates)
    except Exception:
        index = _seed(candidates)
    index = _a_past_that_is_not_there(index, candidates, text, memory)
    return _an_answer_it_already_gave(index, candidates, text, memory)


def _a_past_that_is_not_there(index, candidates, text, memory):
    if _history is None or not candidates:
        return index
    try:
        def speaks_of_a_past(reply):
            return _history.a_past_that_is_not_there(reply, memory, text)

        reply = candidates[index].get("reply") if 0 <= index < len(candidates) else ""
        if not speaks_of_a_past(reply):
            return index
        if _priority(candidates[index]) >= SAFETY:
            return index
        for other, candidate in enumerate(candidates):
            if _priority(candidate) < 0:
                continue
            if not speaks_of_a_past(candidate.get("reply")):
                return other
    except Exception:
        return index
    return index


_SAID_BEFORE_WORDS = 8


def _an_answer_it_already_gave(index, candidates, text, memory):
    if not candidates:
        return index
    try:
        if _priority(candidates[index]) >= SAFETY:
            return index
        heard = _said_before(memory, text)
        if not heard or _content(candidates[index].get("reply")) not in heard:
            return index
        last = _last_reply(memory)
        for other, candidate in enumerate(candidates):
            if other == index:
                continue
            if _priority(candidate) >= SAFETY:
                continue
            reply = candidate.get("reply")
            if _content(reply) in heard or _echoes(reply, last):
                continue
            if fallback.is_a_hedge(reply) or _points_back(reply):
                continue
            if len(_content(reply).split()) < _SAID_BEFORE_WORDS:
                continue
            return other
    except Exception:
        return index
    return index


MEMORY_MODULES = frozenset(("memory_store", "chat", "greeting", "said_back"))


def _a_recall_from_an_earlier_turn(text, memory):
    if not _there_is_a_chat(memory):
        return False
    try:
        if _recall is not None and _recall.ask(text):
            return True
    except Exception:
        pass
    try:
        if _repeat is not None and _repeat.asked_back(text, memory):
            return True
    except Exception:
        pass
    try:
        return bool(_lineback is not None and _lineback.an_earlier_turn(text, memory))
    except Exception:
        return False


def _the_kind_line_they_gave(text, memory):
    if _lineback is None or not _there_is_a_chat(memory):
        return None
    try:
        return _lineback.the_kind_they_gave(text, memory)
    except Exception:
        return None


def _seed(candidates):
    for index, candidate in enumerate(candidates):
        if _priority(candidate) >= 0:
            return index
    return 0


def _priority(candidate):
    priority = candidate.get("priority", 0)
    if isinstance(priority, bool) or not isinstance(priority, (int, float)):
        return 0
    return priority


_REFUSAL_UNDONE = frozenset((
    "no", "not", "without", "free", "avoid", "leave", "leaves", "leaving", "left", "out",
    "instead", "swap", "swaps", "swapped", "rather", "cant", "dont", "doesnt", "didnt",
    "refuse", "refused", "refuses", "allergic", "allergy", "intolerant", "allergen", "isnt",
    "arent", "wasnt", "wont", "cannot", "never", "none", "nothing", "off", "replace"))


_ALLERGY_LIFTED = re.compile(
    r"\b(?:not|isnt|arent|wasnt|werent|never)\s+(?:actually\s+)?(?:allergic|intolerant)\b"
    r"|\bno\s+(?:allerg(?:y|ies)|intolerance)\b")


def _the_food_the_line_refused(text, memory):
    if _cooking is None:
        return frozenset()
    understood = memory.get("understood") if isinstance(memory, dict) else None
    if not isinstance(understood, dict) or not understood:
        understood = {"clean": text}
    said = str(understood.get("clean") or understood.get("text") or text or "").lower()
    if _ALLERGY_LIFTED.search(said):
        return frozenset()
    if any(phrase in said for phrase in getattr(_cooking, "SHORTAGE_WORDS", ())):
        return frozenset()
    try:
        return frozenset(_cooking.refused_foods(understood))
    except Exception:
        return frozenset()


def _offers_the_food(reply, refused):
    first = re.split(r"(?<=[.!?])\s+", str(reply or "").strip(), maxsplit=1)[0].lower()
    words = [word.replace("'", "") for word in re.findall(r"[a-z']+", first)]
    for food in refused:
        names = {food, food + "s"}
        if food.endswith("y"):
            names.add(food[:-1] + "ies")
        if food.endswith("f"):
            names.add(food[:-1] + "ves")
        for place, word in enumerate(words):
            if word not in names:
                continue
            near = words[max(0, place - 5):place + 5]
            if not any(undone in _REFUSAL_UNDONE for undone in near):
                return True
            break
    return False


def _offers_what_the_line_ruled_out(candidate, text, memory):
    if _ruledout is None:
        return False
    try:
        thing, _kept, _opening = _ruledout._rules_out_what_i_never_said(text, memory)
    except Exception:
        return False
    if not thing:
        return False
    return _offers_the_food(candidate.get("reply") or "", frozenset((thing,)))


def _the_thing_the_line_ruled_out(text, memory):
    if _ruledout is None:
        return ""
    try:
        thing, _kept, _opening = _ruledout._rules_out_what_i_never_said(text, memory)
    except Exception:
        return ""
    return thing or ""


def _every_real_answer_offers(thing, candidates, index):
    others = [candidate for candidate in candidates
              if candidate is not candidates[index] and _priority(candidate) >= 0
              and _priority(candidate) < SAFETY
              and str(candidate.get("reply") or "").strip()]
    if not others:
        return False
    return all(_offers_the_food(candidate.get("reply") or "", frozenset((thing,)))
               for candidate in others)
A_CEILING = re.compile(
    r"\b(?:too much|too many|max(?:imum)?|limit|safe|how much can i (?:take|have|drink|eat)"
    r"|how many can i (?:take|have|drink|eat))\b", re.I)
GENERIC = frozenset("""
    about after again along another anything around before being better between could doing
    during enough every first found going great happy least leave might money month months never
    other people place point right should since something still take taken their there these
    thing things think those three through times today together under until usual wanted
    where which while without would wrong year years
""".split())


def _the_cut_the_line_asked_for(memory, candidates):
    understood = memory.get("understood") if isinstance(memory, dict) else None
    if not isinstance(understood, dict) or not understood.get("constraint"):
        return None
    try:
        wanted = _limit.reply_for(understood, memory)
    except Exception:
        return None
    if not wanted:
        return None
    wanted = str(wanted).strip()
    for index, candidate in enumerate(candidates):
        if str(candidate.get("reply") or "").strip() == wanted:
            return index


A_FIGURE = re.compile(r"\b\d[\d,]*(?:\.\d+)?\b")
A_WORKED_OUT = re.compile(
    r"\b(?:none|already|past|more|less|fewer|short|left|over|under|enough|comes to|works out)\b",
    re.I)
A_SUM_TO_WORK_OUT = re.compile(
    r"\b(?:left|remaining|remain|more|less|fewer|extra|another|needed|need|short|over|under|"
    r"enough|towards|altogether|in all|total)\b", re.I)


def _the_figures_they_gave(memory):
    if not isinstance(memory, dict):
        return frozenset()
    said = []
    turns = memory.get("turns")
    for one in (turns if isinstance(turns, list) else [])[-8:]:
        text = one.get("user") if isinstance(one, dict) else None
        if isinstance(text, str):
            said.extend(A_FIGURE.findall(text))
    return frozenset(said)


def _says_back_one_of(reply, figures):
    if not figures:
        return False
    return any(one in figures for one in A_FIGURE.findall(str(reply or "")))


def _the_candidates_with_a_figure(text, memory, candidates, pool):
    understood = memory.get("understood") if isinstance(memory, dict) else None
    if not isinstance(understood, dict) or understood.get("wants") != "amount":
        return pool
    line = str(text or "")
    if not re.search(r"\bhow much\b", line, re.I):
        return pool
    if A_CEILING.search(line):
        plain = [index for index in pool
                 if not _limit.FRAME.match(str(candidates[index].get("reply") or "").strip())]
        return plain or pool
    money = _narrow.SIGNALS.get("money")
    figure = (money, _narrow.SIGNALS.get("amount"))
    theirs = _the_figures_they_gave(memory)
    subject = {word for word in (set(WORD.findall(line.lower()))
                                 | _carried_words(memory))
               if len(word) >= 5 and word not in GENERIC}
    to_work_out = bool(A_SUM_TO_WORK_OUT.search(line))
    with_figure, says_it_back, bare_echo = [], [], []
    for index in pool:
        reply = str(candidates[index].get("reply") or "")
        has_figure = any(signal and signal.search(reply) for signal in figure)
        quotes = _says_back_one_of(reply, theirs)
        if not (has_figure or quotes):
            continue
        if quotes:
            new_figures = {one for one in A_FIGURE.findall(reply)} - theirs
            if new_figures and (money.search(reply) or A_WORKED_OUT.search(reply)):
                says_it_back.append(index)
            elif not new_figures and not to_work_out:
                bare_echo.append(index)
            continue
        if subject:
            said = {word for word in WORD.findall(reply.lower()) if len(word) >= 5}
            if not any(_the_same_word(word, one) for word in subject for one in said):
                continue
        with_figure.append(index)
    for best in (bare_echo, says_it_back, with_figure):
        if best and len(best) < len(pool):
            return best
    return pool


_AN_AMENDMENT = re.compile(
    r"^\s*(?:actually|no|nope|sorry|oh|hang on|wait|correction|scratch that|i mean|make that)\b",
    re.I)
_MONTHS = re.compile(
    r"\b(january|february|march|april|may|june|july|august|september|october|november|december)\b",
    re.I)


def _amends_a_detail(text, memory):
    said = str(text or "").strip()
    if not said or not _AN_AMENDMENT.search(said):
        return set()
    months = {month.lower() for month in _MONTHS.findall(said)}
    return months if len(months) == 1 and memory.get("turns") else set()


def _the_candidates_that_hand_the_detail_back(months, candidates, pool):
    holding = [index for index in pool
               if months & {month.lower() for month in _MONTHS.findall(
                   str(candidates[index].get("reply") or ""))}]
    if len(holding) != 1:
        return pool
    return holding + [index for index in pool if index != holding[0]]


def _asks_it_back(reply):
    said = str(reply or "").strip()
    if not said:
        return False
    last = said.replace("\n", " ").rstrip()
    cut = max(last.rfind(". "), last.rfind("! "), last.rfind("? "))
    return "?" in (last[cut + 2:] if cut >= 0 else last)


def _the_candidates_that_give_the_shape(text, memory, candidates, pool):
    understood = memory.get("understood") if isinstance(memory, dict) else None
    if not isinstance(understood, dict):
        return pool
    want = understood.get("wants")
    if not want:
        return pool
    if want == "amount":
        return _the_candidates_with_a_figure(text, memory, candidates, pool)
    if want in fit.SOFT:
        return pool
    if want == "yesno" and _names_the_answers_figure(str(candidates[pool[0]].get("reply") or ""),
                                                    memory):
        return pool
    if _a_check_on_the_answer(str(candidates[pool[0]].get("reply") or "")):
        return pool
    if not pool or fit.gives(str(candidates[pool[0]].get("reply") or ""), want, text) is not False:
        return pool
    words = set(WORD.findall(str(text or "").lower()))
    subject_known = _names_the_subject(candidates[pool[0]], memory, words) if pool else True
    giving = [index for index in pool[1:]
              if fit.gives(str(candidates[index].get("reply") or ""), want, text) is True
              and (not subject_known
                   or _names_the_subject(candidates[index], memory, words)
                   or not _asks_it_back(candidates[index].get("reply")))]
    if not giving:
        return pool
    return giving + [index for index in pool if index not in giving]


DOING_WANTS = frozenset(("steps", "options", "pick", "advice", "howto"))


def _the_line_asks_for_a_doing(memory):
    understood = (memory or {}).get("understood") if isinstance(memory, dict) else None
    want = understood.get("wants") if isinstance(understood, dict) else None
    return want in DOING_WANTS


SAID_BACK = re.compile(r"^(?:you said|you told me|you mentioned|as you said|still )\b", re.I)


def _says_what_they_already_said(reply):
    return bool(SAID_BACK.match(str(reply or "").strip()))


def _the_same_word(one, other):
    if one == other:
        return True
    short, long = sorted((one, other), key=len)
    return len(short) >= 5 and long.startswith(short) and len(long) - len(short) <= 2



_NUMBER_WORDS = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7,
                 "eight": 8, "nine": 9, "ten": 10, "eleven": 11, "twelve": 12, "fifteen": 15,
                 "twenty": 20, "thirty": 30, "forty": 40, "fifty": 50, "sixty": 60,
                 "hundred": 100, "thousand": 1000}
_FIGURES = re.compile(
    r"\b\d[\d,]*(?:\.\d+)?\b|\b(?:" + "|".join(sorted(_NUMBER_WORDS, key=len,
                                                             reverse=True)) + r")\b")


def _the_numbers_in(line):
    said = set()
    for word in _FIGURES.findall(str(line or "").lower()):
        if word in _NUMBER_WORDS:
            said.add(float(_NUMBER_WORDS[word]))
            continue
        try:
            said.add(float(word.replace(",", "")))
        except ValueError:
            continue
    return said


def _names_the_answers_figure(reply, memory):
    mine = _the_numbers_in(reply)
    return bool(mine) and bool(mine & _the_numbers_in(_last_reply(memory)))


def _explains_the_method(reply):
    flat = str(reply or "").lower()
    return " because " in flat and "work" in flat
def _the_figure_they_asked_back(candidates, real, memory, text):
    if _repeat is None or _recall is None:
        return None
    understood = memory.get("understood") if isinstance(memory, dict) else None
    if not isinstance(understood, dict) or not understood.get("looks_back"):
        return None
    try:
        figure = _repeat.the_figure_they_gave(text, memory)
    except Exception:
        return None
    if not figure:
        return None
    for index in real:
        if _repeat.carries_the_figure(figure, candidates[index].get("reply") or ""):
            return index
    return None


A_MY_OWN_REPORT = re.compile(
    r"\b(?:i|ive|i've|we|weve|we've)\s+(?:have|has|had|got|gotten)\b", re.I)
A_REPORT_ASKS = re.compile(
    r"\?|\b(?:what|whats|why|how|when|where|which|who|is|are|was|do|does|did|can|could|should"
    r"|would|will|tell|explain|mean|means|contagious|infectious|symptom|symptoms|sign|signs"
    r"|treat|treated|treatment|long|last|lasts|serious|dangerous|fatal|cause|causes|recover"
    r"|spread|catch|test|tests|vaccine|diet|food|foods|cure|help|worried|worry|advice|tips"
    r"|avoid|prevent|dose|better|worse|normal|common|painful)\b", re.I)
A_DEFINITION = re.compile(
    r"^\s*(?!(?:it|there|that|this|these|those|he|she|they|you|we|i|here|what)\b)"
    r"(?:a\s+|an\s+|the\s+|type\s+\d+\s+)?[\w'-]+(?:\s+[\w'-]+){0,3}\s+(?:is|are)\s+\S",
    re.I)
A_REPORT_NOD = re.compile(
    r"^\s*(?:noted|got it|okay|ok\b|right|sure|nice one|i'm listening|im listening|"
    r"that sounds|thanks|cheers)\b", re.I)
A_CONTENT_WORD = re.compile(r"[a-z][a-z'-]{2,}")
REPORT_STOP = frozenset("""i im i'm ive i've we we've weve me my mine myself have has had got gotten
    the a an and or but so that this it its it's of to in on at for with from about really very
    quite just now today again too also still some any been being am is are was were do does did
    not no yes feel feeling felt think thinks thought lot bit sort kind thing things""".split())


def _the_words_the_report_names(text):
    said = " ".join(str(text or "").lower().split())
    return tuple(word for word in A_CONTENT_WORD.findall(said) if word not in REPORT_STOP)


def _a_report_and_no_ask(text):
    said = " ".join(str(text or "").lower().split())
    return bool(A_MY_OWN_REPORT.search(said)) and not A_REPORT_ASKS.search(said)


def _is_advice_about(reply, words):
    said = " ".join(str(reply or "").split())
    if not said or A_REPORT_NOD.match(said) or A_DEFINITION.match(said):
        return False
    if len(said.split()) < 10:
        return False
    low = " " + re.sub(r"[^a-z0-9' ]+", " ", said.lower()) + " "
    return any(" " + word in low for word in set(words))


def _how_much_it_names(reply, words):
    low = " " + re.sub(r"[^a-z0-9' ]+", " ", str(reply or "").lower()) + " "
    return sum(1 for word in set(words) if " " + word in low)


def _the_advice_over_a_definition(candidates, pool, text, chosen):
    if len(pool) < 2 or not _a_report_and_no_ask(text):
        return None
    words = _the_words_the_report_names(text)
    if not words:
        return None
    won = candidates[chosen].get("reply") or ""
    low = " " + re.sub(r"[^a-z0-9' ]+", " ", str(won).lower()) + " "
    if not A_DEFINITION.match(won) or not any(" " + word in low for word in words):
        return None
    best_index, best_score, best_chat = None, 0, True
    for index in pool:
        if index == chosen:
            continue
        reply = candidates[index].get("reply")
        if not _is_advice_about(reply, words):
            continue
        score = _how_much_it_names(reply, words)
        is_chat = str(candidates[index].get("module") or "") == "chat"
        if score > best_score or (score == best_score
                                  and (best_index is None or (best_chat and not is_chat))):
            best_index, best_score, best_chat = index, score, is_chat
    return best_index


def _choose(text, memory, candidates):
    real = [index for index, candidate in enumerate(candidates) if _priority(candidate) >= 0]
    if not real:
        return 0
    last = _last_reply(memory)
    if last and _the_line_is_news(text):
        def _hears_the_news(index):
            return not _announces_a_repeat(candidates[index].get("reply"))

        hearing_it = [index for index in real if _hears_the_news(index)]
        if not hearing_it:
            hearing_it = [index for index in range(len(candidates)) if _hears_the_news(index)]
        if hearing_it and len(hearing_it) < len(candidates):
            real = hearing_it
    best = real[0]
    if _priority(candidates[best]) >= SAFETY:
        return best
    amended = _amends_a_detail(text, memory)
    if amended:
        every = list(range(len(candidates)))
        handed = _the_candidates_that_hand_the_detail_back(amended, candidates, every)
        if handed[0] != best:
            real = [handed[0]] + [index for index in real if index != handed[0]]
            best = handed[0]
    if not onscreen.earlier_turn(memory):
        fresh = [index for index in real
                 if not onscreen.talks_about_the_conversation(candidates[index].get("reply"))]
        if fresh:
            real = fresh
            best = fresh[0]
    if _a_check_on_the_answer(candidates[best].get("reply")):
        explained = [index for index in real
                     if index != best and _explains_the_method(candidates[index].get("reply"))]
        if not explained:
            return best
        best = explained[0]
    back = _the_figure_they_asked_back(candidates, real, memory, text)
    if back is not None:
        return back

    cause = _the_cause_asked_for(candidates, real, text, best)
    if cause is not None:
        return cause
    verdict = _verdict_reply(candidates, text, memory, last, clean=text, best=best)
    if verdict is not None:
        return verdict
    plainer = _a_plainer_reading_of_the_same_answer(candidates, best, text, memory)
    if plainer is not None:
        return plainer
    handed_back = _the_answer_handed_back(candidates, text, memory, last)
    if handed_back is not None:
        return handed_back
    if _the_kind_line_they_gave(text, memory):
        front = candidates[real[0]].get("module")
        for index in real:
            if candidates[index].get("module") == "said_back":
                if front in ("chat", "greeting", "answers") or index == real[0]:
                    return index
    held = _as_it_comes(text, memory, candidates, last)
    if held is not None:
        with_figure = _the_candidates_that_give_the_shape(
            text, memory, candidates, [held] + [index for index in real if index != held])
        if held not in with_figure:
            held = with_figure[0]
        elif (with_figure[0] != held
              and _the_line_asks_for_a_doing(memory)
              and _says_what_they_already_said(candidates[held].get("reply"))):
            held = with_figure[0]
        instead = _claims_instead(text, memory, candidates, last, _priority(candidates[held]))
        if instead is not None and _offers_what_the_line_ruled_out(candidates[instead], text, memory):
            instead = None
        return held if instead is None else instead
    pool = _the_candidates_that_give_the_shape(text, memory, candidates, real)
    real = pool
    answering = _the_candidates_that_answer_the_ask(text, candidates, pool)
    if answering is not None:
        pool = answering
        real = answering
    refused = _the_food_the_line_refused(text, memory)
    if refused:
        respecting = [index for index in pool
                      if not _offers_the_food(candidates[index].get("reply") or "", refused)]
        if respecting and len(respecting) < len(pool):
            pool = respecting
            real = respecting
    cut = _the_cut_the_line_asked_for(memory, candidates)
    if cut is not None:
        return cut
    if last:
        heard = _said_before(memory, text)
        cut = {}
        for index in pool:
            words = _content(candidates[index].get("reply")).split()
            if len(words) < 8:
                continue
            for line in heard:
                was = line.split()
                if len(words) < len(was) and _a_run_of(was, words):
                    cut[index] = was
                    break
        fresh = [index for index in pool
                 if _content(candidates[index].get("reply")) != last
                 and not _echoes(candidates[index].get("reply"), last)
                 and not fallback.is_a_hedge(candidates[index].get("reply"))
                 and not _points_back(candidates[index].get("reply"))]
        if cut:
            held = [index for index in fresh if index not in cut]
            if held and any(_a_run_of(cut[gone], _content(candidates[take].get("reply")).split())
                            for take in held for gone in cut):
                fresh = held
        if fresh and _content(candidates[pool[0]].get("reply")) not in heard:
            fresh = [index for index in fresh
                     if _content(candidates[index].get("reply")) not in heard] or fresh
        if (fresh and _a_repeat_to_hold(memory, text)
                and _echoes(candidates[pool[0]].get("reply"), last)):
            fresh = []
        if fresh:
            pool = fresh
        else:
            if len(pool) > 1:
                shortest = min(pool, key=lambda i: len(_content(candidates[i].get("reply"))))
                longest = max(len(_content(candidates[i].get("reply"))) for i in pool)
                if (_echoes(candidates[shortest].get("reply"), last)
                        and len(_content(candidates[shortest].get("reply"))) * 3 <= longest * 2):
                    return shortest
            shorter = _a_shorter_said_again(candidates, last)
            if shorter is not None:
                return shorter
            said = _said_it_already(candidates, text, memory, last)
            if said is not None:
                pool = [said]
            else:
                choice = _a_choice_the_answer_did_not_make(candidates, text, memory, last)
                if choice is not None:
                    pool = [choice]
                elif not [index for index in pool
                          if _content(candidates[index].get("reply")) == last]:
                    unheard = [index for index, candidate in enumerate(candidates)
                               if not _echoes(candidate.get("reply"), last)
                               and _answers_this_line(candidate.get("reply"))]
                    if unheard:
                        pool = unheard
                    if all(_points_back(candidates[index].get("reply")) for index in pool):
                        says = [index for index in range(len(candidates))
                                if not _points_back(candidates[index].get("reply"))
                                and not fallback.is_a_hedge(candidates[index].get("reply"))
                                and _carries_the_answer(candidates[index].get("reply"), memory)]
                        if says:
                            pool = says

    detail = _a_detail_added_to_the_news(candidates, pool, text, memory)
    if detail is not None:
        return detail
    named = _a_card_that_names_the_line(candidates, pool, text, memory)
    if named is not None:
        return named
    added = _the_answer_that_names_what_the_line_added(candidates, pool, text, last)
    if added is not None:
        return added
    best = pool[0]
    own, carried, words, clean = _about(text, memory)
    child_words = _the_words_for_the_child(candidates, clean, memory, last)
    if child_words is not None and not _a_whole_line_module_spoke(candidates):
        return child_words
    polite = _only_acknowledges(memory)
    here = _a_presence_check(memory)
    ask = _the_ask_about_a_child(candidates, clean, last)
    if ask is not None:
        return ask
    gave = _the_name_they_gave(candidates, text, memory)
    if gave is not None:
        return gave
    drafted = _draft_index(candidates, last, clean)
    if drafted is not None:
        return drafted
    about_them = _about_the_person_the_line_names(candidates, pool, clean, last)
    if about_them is not None:
        return about_them
    instead = _instead(text, candidates, last, own, clean)
    if instead is not None:
        return instead
    bye = _leaving_reply(candidates, own, carried, words, clean, text, memory, last)
    if bye is not None:
        return bye
    left = _a_leaving_said_plain(candidates, pool, clean, memory)
    if left is not None:
        return left
    sudden = _sudden_loss_reply(candidates, pool, clean)
    if sudden is not None:
        return sudden
    bot_answer = _about_the_bot(candidates, clean, last)
    if bot_answer is not None:
        return bot_answer
    hours = _the_venue_hours_turn(candidates, clean, last, text)
    if hours is not None:
        return hours
    own_taste = _the_bots_own_taste(candidates, clean, memory, last)
    if own_taste is not None:
        return own_taste
    corrected = _store_correcting(candidates, pool, memory, text, last)
    if corrected is not None:
        return corrected
    revised = _the_store_revises_the_answer(candidates, pool, memory, text, last)
    if revised is not None:
        return revised
    step = _the_move_in_hand(candidates, real, text, last)
    if step is not None and not _points_back(candidates[step].get("reply")):
        return step
    whole = _the_whole_move(candidates, real, text, last, _the_answer_written_out(memory))
    if whole is not None and not _points_back(candidates[whole].get("reply")):
        return whole
    more = _the_next_part(candidates, text, last)
    if more is not None and not _points_back(candidates[more].get("reply")):
        return more
    dated = _the_date_fact(candidates, real, text)
    if dated is not None:
        return dated
    hurt = _hurting_reply(candidates, pool, clean)
    if hurt is not None:
        return hurt
    story = _story_goes_on_reply(text, memory, candidates, last)
    if story is not None:
        return story
    paused = _pause_reply(candidates, pool, text, memory, last)
    if paused is not None:
        return paused
    kind, target = _composer_reading(text, memory)
    if not own and not carried and not words and kind not in (THREAD, CARE_THREAD):
        return best
    if kind in (THREAD, CARE_THREAD):
        keeping = _thread_index(candidates, real, _named_topics(memory), target, last,
                                care_about=clean if kind == CARE_THREAD else "", memory=memory,
                                line=text)
        if keeping is not None:
            return keeping
    if polite or here:
        return pool[0]
    fit_own, fit_carried = _fit(own, carried, memory, _priority(candidates[best]),
                                 candidates[best].get("reply") or "",
                                 candidates[best].get("module") or "", text)
    best_score = _match(candidates[best].get("module"), fit_own, fit_carried, words, clean)
    kept = _carries_the_answer(candidates[best].get("reply"), memory)
    named = _named_topics(memory)
    if _is_a_generic_step(candidates[best].get("reply")):
        for index in pool[1:]:
            entry = candidates[index].get("reply")
            if entry and not _is_a_generic_step(entry) and _opens_on_a_job(entry):
                return index
    recall_from_earlier = _a_recall_from_an_earlier_turn(text, memory)
    if _reads_the_doubt(candidates[pool[0]]):
        for index in pool[1:]:
            if _carries_the_answer(candidates[index].get("reply"), memory):
                return index
    for index in pool[1:]:
        if (recall_from_earlier
                and candidates[best].get("module") in MEMORY_MODULES):
            continue
        if (not _names_the_subject(candidates[index], memory, words)
                and _reads_the_doubt(candidates[pool[0]])):
            continue
        score = _match(candidates[index].get("module"), fit_own, fit_carried, words, clean)
        if score <= best_score:
            continue
        if (_about_the_line(candidates[best].get("reply"), words, clean)
                and not _says_only_the_line(candidates[best].get("reply"), words)
                and not _about_the_line(candidates[index].get("reply"), words, clean)):
            continue
        if (_already is not None
                and _already.tells_them_the_step_again(candidates[index].get("reply"), text, memory)
                and not _already.tells_them_the_step_again(candidates[best].get("reply"),
                                                           text, memory)):
            continue
        if kept and _match(candidates[index].get("module"), named, carried, words, clean) <= 0:
            entry = candidates[index].get("reply")
            if not (_carries_the_answer(entry, memory) or _opens_on_a_job(entry)):
                continue
        best, best_score = index, score
    front = candidates[best].get("reply")
    if (_hands_the_decision_back(front)
            or (candidates[best].get("module") == "chat"
                and _content(front) in _ack_lines())) \
            and (_asks_a_question(memory) or _asks_for_a_judgement(text, memory)):
        already_read = _said_before(memory, text)
        for index in range(len(candidates)):
            if index == best or _priority(candidates[index]) >= SAFETY:
                continue
            reply = candidates[index].get("reply")
            if (_content(reply) in already_read
                    or (last and _echoes(reply, last))):
                continue
            if _names_what_they_said(reply, text, memory):
                return index
    advice = _the_advice_over_a_definition(candidates, pool, text, best)
    if advice is not None:
        return advice
    return _the_card_that_places_the_figure(candidates, best, text, memory)


LONG_ENOUGH = 4


def _a_bare_doubt_reply(candidate, text, memory):
    reply = _content(candidate.get("reply"))
    if not reply or _reading is None:
        return False
    try:
        own = _content(_reading.reply_to_a_bare_doubt(text, memory))
    except Exception:
        return False
    return bool(own) and own == reply


def _places_the_figure(reply):
    said = str(reply or "")
    if not re.search(r"\d", said):
        return False
    return bool(re.search(r"[£$\u20ac]|\b(?:a|an|per|pounds?|quid|dollars?|euros?)\b", said))


def _the_card_that_places_the_figure(candidates, best, text, memory):
    if not _a_bare_doubt_reply(candidates[best], text, memory):
        return best
    for index in range(len(candidates)):
        if index == best or _priority(candidates[index]) >= SAFETY:
            continue
        reply = candidates[index].get("reply")
        if _places_the_figure(reply) and _names_what_they_said(reply, text, memory):
            return index
    return best


LETTERS = re.compile(r"[a-z]+")


def _says_only_the_line(reply, words):
    said = [word for word in LETTERS.findall(str(reply or "").lower()) if len(word) >= LONG_ENOUGH]
    if not said:
        return False
    had = set(word for word in (words or ()) if len(word) >= LONG_ENOUGH)
    if not had:
        return False
    fresh = [word for word in said
             if not any(word.startswith(one) or one.startswith(word) for one in had)]
    if len(said) > 8:
        return False
    return len(fresh) * 2 <= len(said)


def _about_the_line(reply, words, clean=""):
    said = _subject_words(reply)
    if not said:
        return False
    for word in words or ():
        stems = _subject_words(word)
        if not stems:
            if len(word) < LONG_ENOUGH:
                continue
            for one in WORD.findall(str(reply or "").lower()):
                if one.startswith(word) or word.startswith(one):
                    return True
            continue
        for stem in stems:
            for one in said:
                if one == stem:
                    return True
                if (len(stem) >= LONG_ENOUGH and len(one) >= LONG_ENOUGH
                        and (one.startswith(stem) or stem.startswith(one))):
                    return True
    return False


def _names_the_subject(candidate, memory, words):
    if not _a_bare_yes_no(memory):
        return True
    if _carries_the_answer(candidate.get("reply"), memory):
        return True
    subject = _carried_words(memory) - set(words) - DOUBT_WORDS
    if not subject:
        return True
    reply = candidate.get("reply") or ""
    for word in subject:
        if len(word) < 4:
            continue
        if _names_the_thing(word, reply, _carried_words(memory) | set(words)):
            return True
    return False


FIRST_VERB = frozenset("is are was were will can could should may might must does do did has have "
                       "had".split())
CARRIES_NO_SUBJECT = frozenset("""a an the and or but if of to in on at for with from by as it
its this that these those i me my we us our you your he she they them their not no yes so then than
just also very really quite some any all about there here out up down over under more most much
less""".split())


def _names_the_thing(word, reply, line_words):
    tokens = _content(reply).split()
    opening = []
    for token in tokens:
        if token in FIRST_VERB:
            break
        opening.append(token)
    for index, token in enumerate(tokens):
        if not _the_same_plain_word(word, token):
            continue
        if index >= len(opening) or token != word:
            return True
        for after in opening[index + 1:]:
            if len(after) >= 3 and after not in CARRIES_NO_SUBJECT and after not in line_words:
                break
        else:
            return True
    return False


def _the_same_plain_word(one, other):
    if one == other:
        return True
    for word, token in ((one, other), (other, one)):
        if not word or not token:
            continue
        if token.startswith(word) and token[len(word):] in INFLECTED_ENDS:
            return True
        if word.endswith("y") and token == word[:-1] + "ies":
            return True
        if word.endswith(("'s", "s'")) and token == word[:-2]:
            return True
        if word.endswith("s") and not word.endswith("ss") and token == word[:-1]:
            return True
    return False


INFLECTED_ENDS = frozenset(("s", "es", "'s", "s'", "ache"))


DOUBT_WORDS = frozenset("bad normal okay fine good safe right wrong better worse serious worry "
                        "worried thing things that this it is be to a an the for of".split())


def _reads_the_doubt(candidate):
    try:
        from ..compose import fallback as composer, verdict as opinions
        said = candidate.get("reply")
        return opinions.rules_on_the_doubt(said) or composer.is_said_it_already(said)
    except Exception:
        return False


def _a_bare_yes_no(memory):
    understood = memory.get("understood")
    if not isinstance(understood, dict):
        return False
    if _line_topics(memory):
        return False
    return "yesno" in _labels(understood.get("asks"))


def _carried_words(memory):
    topic = memory.get("topic")
    if isinstance(topic, dict):
        labels = _labels(topic.get("words"))
        if labels:
            return labels
        text = topic.get("text")
        if isinstance(text, str) and text.strip():
            return set(WORD.findall(text.lower().strip()))
    return set()


def _fit(own, carried, memory, best_priority, reply="", claimant="", text=""):
    if best_priority >= RECALL:
        repeat = _asks_for_the_answer_again(memory)
        if repeat and not _echoes(reply, _last_reply(memory)):
            return set(), set()
        if not repeat and claimant and _asks_about_the_chat(claimant, text, memory):
            return set(), set()
        if not _line_topics(memory):
            return set(), carried
    return own, carried


def _line_topics(memory):
    understood = memory.get("understood")
    if not isinstance(understood, dict):
        return set()
    return _labels(understood.get("topics"))


POINTS_BACK = re.compile(
    r"\b(?:did|do|does|were|was|have|had)\s+(?:you|u)\s+(?:say|said|tell|told|mention)\b"
    r"|\b(?:you|u)\s+(?:said|say|told|mentioned)\b|\bagain\b"
    r"|\b(?:explain|talk me through|walk me through)\s+(?:it|that|this|those|them)\b"
    r"|\bgo\s+(?:over|through)\s+(?:it|that|this)\b"
    r"|\brun\s+(?:it|that|this)\s+by\s+me\b"
    r"|\bthe\s+(?:last|final)\s+(?:bit|part)\b"
    r"|\b(?:once|one)\s+more\b|\bone\s+more\s+time\b"
    r"|\b(?:i|you)\s+(?:lost|lose)\s+(?:you|me)\b")
REPEAT_FRAME = frozenset("""
    a again already an and earlier before bit bits but by did do does exactly explain explained
    final for go going had has have how is it just last long lose lost many me mention mentioned
    more much now of okay once one over part parts please ran run said say sayd so sorry tell that
    the them then there this through to told u us walk talk walked talked was were what when which you
""".split())


_FRAME = None


THE_ANSWER_BANDS = frozenset(("answers", "memory_store"))


def _an_answer_behind_the_ask(memory):
    if not isinstance(memory, dict):
        return False
    turns = [one for one in (memory.get("turns") or []) if isinstance(one, dict)]
    said = [one for one in turns if str(one.get("bot") or "").strip()]
    if not said:
        return False
    return said[-1].get("module") in THE_ANSWER_BANDS


def _asks_for_the_answer_again(memory, text=""):
    understood = memory.get("understood")
    if not isinstance(understood, dict):
        return False
    text = str(text or understood.get("clean") or understood.get("text") or "").lower()
    if _repeat is not None and _repeat.asks_for_less(text):
        return False
    if _the_store_reads_a_repeat(text, memory):
        return True
    if _the_store_reads_an_explain_again_ask(text):
        return True
    if not POINTS_BACK.search(text):
        return False
    frame = _the_repeat_frame()
    return not [word for word in re.findall(r"[a-z']+", text) if word not in frame]


def _the_repeat_frame():
    global _FRAME
    if _FRAME is None:
        frame = set(REPEAT_FRAME)
        try:
            from . import memory_store as store
        except Exception:
            store = None
        frame |= set(getattr(store, "REPEAT_WORDS", ()) or ())
        _FRAME = frame
    return _FRAME


def _the_store_reads_a_repeat(text, memory):
    try:
        from . import memory_store as store
    except Exception:
        return False
    reader = getattr(store, "asks_again", None)
    if reader is None:
        return False
    try:
        return bool(reader(text, memory))
    except Exception:
        return False


def _the_store_reads_an_explain_again_ask(text):
    try:
        from ..memory import meant
    except Exception:
        return False
    line = str(text or "").strip().lower()
    if not line:
        return False
    for name in ("MEAN", "REPEAT"):
        reader = getattr(meant, name, None)
        try:
            if reader is not None and reader.match(line):
                return True
        except Exception:
            continue
    return False


def _a_repeat_to_hold(memory, text=""):
    return (_asks_for_the_answer_again(memory, text)
            and _an_answer_behind_the_ask(memory)
            and not _names_a_figure(text))


def _a_choice_the_answer_did_not_make(candidates, text, memory, last=""):
    understood = memory.get("understood")
    if not last or not isinstance(understood, dict):
        return None
    if CHOICE not in _labels(understood.get("asks")):
        return None
    for index, candidate in enumerate(candidates):
        if _priority(candidate) >= 0:
            continue
        reply = _content(candidate.get("reply"))
        if not reply or reply == last or _echoes(reply, last):
            continue
        if fallback.is_a_hedge(candidate.get("reply")) or _points_back(candidate.get("reply")):
            continue
        return index
    return None


def _a_shorter_said_again(candidates, last):
    if not last:
        return None
    for index, candidate in enumerate(candidates):
        if _priority(candidate) >= 0:
            continue
        if fallback.is_the_answer_shorter(candidate.get("reply"), last):
            return index
    return None


def _said_it_already(candidates, text, memory, last=""):
    if not last or not fallback.says_it_already(text, memory):
        return None
    real = [candidate for candidate in candidates if _priority(candidate) >= 0]
    if not real:
        return None
    first = _content(real[0].get("reply"))
    if not _echoes(first, last) or len(first.split()) >= len(last.split()) - 3:
        return None
    subject = str(text or "")
    for figure in getattr(_repeat, "FIGURE_ASKS", ()) or ():
        try:
            _name, ask, _says = figure
        except (TypeError, ValueError):
            continue
        try:
            if ask.search(str(text or "")):
                shorter = ask.sub(" ", str(text or ""))
                if len(shorter) < len(subject):
                    subject = shorter
        except AttributeError:
            continue
    if _repeat is not None:
        left = [word for word in re.findall(r"[a-z']+", subject)
                if word not in getattr(_repeat, "FIGURE_WORDS", ())
                and word not in getattr(_repeat, "FIGURE_SAYING", ())]
        if not left:
            return None
    last_words = set(last.split())
    asked = [word for word in fallback.content_words(subject)
             if word in last_words or word.rstrip("s") in last_words or word + "s" in last_words]
    if not asked:
        return None
    said = set(first.split())
    missing = [word for word in asked
               if word not in said and word.rstrip("s") not in said and word + "s" not in said]
    if len(missing) * 2 < len(asked):
        return None
    for index, candidate in enumerate(candidates):
        if _priority(candidate) < 0 and fallback.is_said_it_already(candidate.get("reply")):
            return index
    return None


ACK_POOL = None


def _ack_lines():
    global ACK_POOL
    if ACK_POOL is None:
        try:
            module = importlib.import_module(".chat", __package__)
            pools = getattr(module, "REPLIES", None) or {}
            ACK_POOL = frozenset(_content(line) for line in pools.get("ack", ()))
        except Exception:
            ACK_POOL = frozenset()
    return ACK_POOL


def _asks_a_question(memory):
    understood = (memory or {}).get("understood")
    if not isinstance(understood, dict):
        return False
    return understood.get("kind") == "question" or understood.get("intent") == "question"


def _asks_for_a_judgement(text, memory=None):
    try:
        from ..compose import judgement
        return bool(judgement.asks_for_a_judgement(text, memory))
    except Exception:
        return False


def _hands_the_decision_back(reply):
    try:
        module = importlib.import_module(".chat", __package__)
        return bool(module.hands_it_back(reply))
    except Exception:
        return False


def _the_reply_is_the_report(candidate, text, memory):
    reply = _content(candidate.get("reply"))
    if not reply:
        return False
    try:
        own = _content(fallback.the_report_reply(text, memory))
    except Exception:
        return False
    return bool(own) and own == reply


def _real_answers_besides(candidates, last=""):
    said = []
    for candidate in candidates:
        if _priority(candidate) <= 0:
            continue
        reply = _content(candidate.get("reply"))
        if not reply or (last and reply == _content(last)):
            continue
        if candidate.get("module") == "chat" and reply in _ack_lines():
            continue
        said.append(candidate)
    return said


POOL_MODULES = frozenset(("chat", "greeting"))


THE_ASK_OPENS = re.compile(
    r"^(?:and |so |but |also |then |please )*"
    r"(?:what|how|which|where|when|who|why|any|ideas|thoughts|suggestions|advice|tips|"
    r"recommend\w*|should|could|shall|can|do|is|are|help)\b")

ECHO_STOP = frozenset(("the", "and", "for", "you", "your", "with", "that", "this", "have", "has",
                       "was", "were", "are", "but", "not", "his", "her", "she", "him", "they",
                       "them", "its", "out", "about", "some", "from", "been", "what", "how",
                       "would", "will", "just", "one", "now", "day", "like"))

THEIR_VOICE = {"my": "your", "mine": "yours", "i": "you", "im": "youre", "me": "you",
               "myself": "yourself", "we": "you", "our": "your", "ours": "yours"}


def _the_ask_after_the_facts(text):
    low = (text or "").lower().rstrip(" .?!")
    cut = max(low.rfind(","), low.rfind(";"), low.rfind("."))
    if cut <= 0:
        return ""
    if len(WORD.findall(low[:cut])) < 3:
        return ""
    ask = low[cut + 1:].strip(" .?!")
    return ask if THE_ASK_OPENS.match(ask) else ""


def _only_says_the_line_back(reply, text):
    words = WORD.findall(_content(reply))
    if not words or len(words) > 14:
        return False
    said = set(WORD.findall((text or "").lower()))
    said |= {THEIR_VOICE.get(word, word) for word in said}
    body = [word for word in words if word not in ECHO_STOP and len(word) > 2]
    if not body:
        return False
    return all(word in said for word in body)


def _the_candidates_that_answer_the_ask(text, candidates, pool):
    if not _the_ask_after_the_facts(text):
        return None
    answering = [index for index in pool
                 if not _only_says_the_line_back(_content(candidates[index].get("reply")), text)]
    if not answering or len(answering) == len(pool):
        return None
    if not any(_priority(candidates[index]) >= 0 for index in answering):
        return None
    return answering


def _a_card_besides(candidates, index):
    for other, candidate in enumerate(candidates):
        if other == index:
            continue
        if candidate.get("module") in POOL_MODULES:
            continue
        if _content(candidate.get("reply")):
            return True
    return False


def _a_real_answer_besides(candidates, last=""):
    return bool(_real_answers_besides(candidates, last))



def _only_a_hand_back_besides(candidates, last=""):
    found = False
    for candidate in candidates:
        if _priority(candidate) < 0:
            continue
        reply = _content(candidate.get("reply"))
        if not reply or (last and reply == _content(last)):
            continue
        if candidate.get("module") == "chat" and reply in _ack_lines():
            continue
        if not _hands_the_decision_back(candidate.get("reply") or ""):
            return False
        found = True
    return found


A_SUBJECT_WORD = re.compile(r"[a-z']{3,}")

A_SUBJECT_PHRASE = re.compile(
    r"\b(?:my|our|your|his|her|their|the|this|that|these|those|a|an)\s+((?:[a-z']+\s+){0,2}[a-z']+)")


def _names_what_they_said(reply, text, memory):
    said = set(A_SUBJECT_WORD.findall(_content(text)))
    for turn in reversed((memory or {}).get("turns") or []):
        if isinstance(turn, dict):
            said.update(A_SUBJECT_WORD.findall(_content(turn.get("user"))))
        if len(said) > 80:
            break
    said -= NOT_A_SUBJECT_WORD
    words = set(A_SUBJECT_WORD.findall(_content(reply))) - NOT_A_SUBJECT_WORD
    if said & words:
        return True
    return any(_one_word(one, other) for one in said for other in words)


WORD_ENDINGS = ("s", "es", "ed", "d", "ing", "er", "ers", "est", "ly")


def _one_word(one, other):
    shorter, longer = (one, other) if len(one) <= len(other) else (other, one)
    if shorter == longer:
        return True
    if len(shorter) < 4:
        return False
    tail = longer[len(shorter):] if longer.startswith(shorter) else ""
    if tail in WORD_ENDINGS:
        if not (tail[0] in "aeiou" and shorter[-1] in "aeiou"):
            return True
        return False
    if tail[:1] == shorter[-1] and tail[1:] in WORD_ENDINGS:
        return True
    if shorter.endswith("e") and len(shorter) >= 5:
        for ending in ("ing", "ed"):
            if longer == shorter[:-1] + ending:
                return True
    return False


A_MEASURE_ASKED = re.compile(
    r"\bwhen\b|\bhow\s+(?:long|soon|much|many|hot|warm|old|far|big|often)\b"
    r"|\bwhat\s+(?:time|temperature|day|date)\b", re.I)


def _the_answer_handed_back(candidates, text, memory, last):
    if not last or not _a_repeat_to_hold(memory, text):
        return None
    band = [index for index, candidate in enumerate(candidates)
            if candidate.get("module") in MEMORY_MODULES and _priority(candidate) >= 0]
    for index in band:
        reply = _content(candidates[index].get("reply"))
        if reply and _echoes(reply, last):
            return index
    seen = set(_content(last).split())
    for index in band:
        reply = _content(candidates[index].get("reply"))
        if reply and _made_of_the_answer(reply, seen):
            return index
    return None


def _names_a_figure(text):
    line = str(text or "")
    if not line.strip():
        return False
    if A_MEASURE_ASKED.search(line):
        return True
    for figure in getattr(_repeat, "FIGURE_ASKS", ()) or ():
        try:
            _name, ask, _says = figure
        except (TypeError, ValueError):
            continue
        try:
            if ask.search(line):
                return True
        except AttributeError:
            continue
    return False


def _as_it_comes(text, memory, candidates, last=""):
    for index, candidate in enumerate(candidates):
        name = candidate.get("module")
        if not _declares_as_it_comes(name, text, memory):
            continue
        thing = _the_thing_the_line_ruled_out(text, memory)
        vetoed = bool(thing) and _every_real_answer_offers(thing, candidates, index)
        if _priority(candidate) < 0 and _a_real_answer_besides(candidates, last) and not vetoed:
            hand_back = (_only_a_hand_back_besides(candidates, last)
                         and _names_what_they_said(candidate.get("reply"), text, memory))
            report = (_the_reply_is_the_report(candidate, text, memory)
                      and (fallback.a_report_that_says_something(text, memory)
                           or not _a_card_besides(candidates, index))
                      and not _a_declaring_specialist_besides(candidates, index, memory, text))
            if not (hand_back or report):
                continue
        reply = _content(candidate.get("reply"))
        if not reply or (last and reply == last):
            continue
        if (not vetoed and _priority(candidate) < CHATTER
                and _a_declaring_specialist_besides(candidates, index, memory, text)):
            continue
        if _priority(candidate) < CHATTER and _a_card_names_the_line(candidates, index, text,
                                                                    memory):
            continue
        if (last and (_echoes(reply, last, announced=True)
                      or _the_answer_again_with_a_tail(reply, last))
                and _a_fresh_answer_besides(candidates, index, last)
                and not _a_repeat_to_hold(memory, text)):
            continue
        if (_the_ask_after_the_facts(text) and _only_says_the_line_back(reply, text)
                and _a_card_besides(candidates, index)):
            continue
        return index
    return None


NOT_A_SUBJECT = frozenset(("small talk",))


def _a_question_about_the_bot(text, memory):
    if not isinstance(text, str):
        return False
    try:
        return bool(fallback.reads_as_about_itself(text, memory))
    except Exception:
        return False


def _a_declaring_specialist_besides(candidates, index, memory, text=""):
    topics = _line_topics(memory) - NOT_A_SUBJECT
    if not topics:
        return False
    if text and _a_question_about_the_bot(text, memory):
        return False
    for other, candidate in enumerate(candidates):
        if other == index:
            continue
        if not (set(_declared(candidate.get("module"))) & topics):
            continue
        reply = _content(candidate.get("reply"))
        if not reply:
            continue
        if _already is not None and _already.tells_them_the_step_again(reply, text, memory):
            continue
        return True
    return False


def _a_fresh_answer_besides(candidates, index, last):
    for other, candidate in enumerate(candidates):
        if other == index or _priority(candidate) < 0:
            continue
        reply = _content(candidate.get("reply"))
        if reply and reply != last and not _echoes(reply, last, announced=True):
            return True
    return False


def _claims_instead(text, memory, candidates, last="", above=None):
    for index, candidate in enumerate(candidates):
        if _priority(candidate) < 0:
            continue
        if above is not None and _priority(candidate) <= above:
            continue
        name = candidate.get("module")
        if not _declares_claims_instead(name, text, memory):
            continue
        reply = _content(candidate.get("reply"))
        if not reply or (last and reply == last):
            continue
        return index
    return None


def _declares_claims_instead(module_name, text, memory):
    try:
        module = importlib.import_module("." + str(module_name), __package__)
        hook = getattr(module, DECLARED_CLAIMS_INSTEAD, None)
        return bool(callable(hook) and hook(text, memory))
    except Exception:
        return False


def _declares_as_it_comes(module_name, text, memory):
    try:
        module = importlib.import_module("." + str(module_name), __package__)
        hook = getattr(module, DECLARED_AS_IT_COMES, None)
        return bool(callable(hook) and hook(text, memory))
    except Exception:
        return False


def _asks_about_the_chat(module_name, text, memory):
    try:
        module = importlib.import_module("." + str(module_name), __package__)
        hook = getattr(module, DECLARED_ABOUT_THE_CHAT, None)
        if not callable(hook):
            hook = getattr(module, OWN_ABOUT_THE_CHAT, None)
        return bool(callable(hook) and hook(text, memory))
    except Exception:
        return False


def _the_move_in_hand(candidates, real, text, last):
    if not last or _repeat is None:
        return None
    try:
        if not _repeat.names_nothing(text) or not _repeat.MOVE_ASK.search(str(text or "")):
            return None
    except Exception:
        return None
    if len(real) < 2:
        return None
    said = last.split()
    seen = set(said)
    forms = []
    whole = False
    for index in real:
        words = _content(candidates[index].get("reply")).split()
        if not words:
            continue
        share = sum(1 for word in words if word in seen) / len(words)
        of_the_answer = share >= MOVE_SHARE
        re_tells = len(said) >= MOVE_ANSWER_WORDS and len(words) >= len(said) * MOVE_WHOLE
        if re_tells:
            whole = True
        if of_the_answer or re_tells:
            forms.append((len(words), index, of_the_answer))
    if not whole:
        return None
    sharing = [form for form in forms if form[2]]
    if len(forms) < 2 or not sharing:
        return None
    shortest, index, _ = min(sharing)
    longest = max(length for length, _, _ in forms)
    if shortest > MOVE_WORDS or shortest * 3 > longest * 2:
        return None
    return index


WHOLE_MOVE_WORDS = 60
CUT_MARKS = ",;:"
TOKEN = re.compile(r"[a-z0-9']+")


def _the_whole_move(candidates, real, text, last, written=""):
    if not last or _repeat is None or len(real) < 2:
        return None
    try:
        if not _repeat.names_nothing(text) or not _repeat.MOVE_ASK.search(str(text or "")):
            return None
    except Exception:
        return None
    answer = " ".join(str(written or last).split())
    tokens = [(match.group(0), match.end()) for match in TOKEN.finditer(answer.lower())]
    if len(tokens) < 4:
        return None
    seen = {word for word, _ in tokens}

    def _halves(skip_repeats):
        cut, whole = [], []
        for index in real:
            words = _content(candidates[index].get("reply")).split()
            if not words or len(words) > WHOLE_MOVE_WORDS:
                continue
            if skip_repeats and _echoes(str(candidates[index].get("reply") or ""), last):
                continue
            if sum(1 for word in words if word in seen) / len(words) < MOVE_SHARE:
                continue
            run = _run_in_the_answer(words, tokens, answer)
            if run and answer[run[1]:run[1] + 1] in CUT_MARKS and len(tokens) - run[2] >= 2:
                cut.append((words, run[0]))
            else:
                whole.append(words)
        return cut, whole

    cut, whole = _halves(True)
    if not cut and whole:
        absent = [index for index in real
                  if not _made_of_the_answer(candidates[index].get("reply"), seen)]
        if absent:
            for index in real:
                if _made_of_the_answer(candidates[index].get("reply"), seen):
                    return index
    if not cut or not whole:
        repeats = [index for index in real
                   if _echoes(str(candidates[index].get("reply") or ""), last)
                   and _made_of_the_answer(candidates[index].get("reply"), seen)]
        quiet = [index for index in repeats
                 if not _announces_a_repeat(candidates[index].get("reply"))]
        if quiet and len(quiet) < len(repeats):
            return quiet[0]
        return None
    for index in real:
        words = _content(candidates[index].get("reply")).split()
        if not words or words not in whole:
            continue
        if any(_carries_on(words, run) for _, run in cut):
            return index
    return None


def _made_of_the_answer(reply, seen):
    words = _content(reply).split()
    return bool(words) and sum(1 for word in words if word in seen) / len(words) >= MOVE_SHARE


def _the_line_is_news(text):
    try:
        from ..memory import returned
    except Exception:
        return False
    return returned.says_it_happened_again(text)


def _announces_a_repeat(reply):
    said = str(reply or "").strip().lower()
    if not said:
        return False
    return any(said.startswith(lead) for lead in _repeat_leads())


def _repeat_leads():
    leads = []
    try:
        from ..memory import topics as _topics
        for lead in getattr(_topics, "REPEAT_LEADS", ()):
            leads.append(" ".join(str(part) for part in lead))
    except Exception:
        pass
    try:
        from . import answers as _answers
        for frame in getattr(_answers, "AGAIN", ()):
            head = str(frame).split("{")[0].strip().lower()
            if head:
                leads.append(head)
    except Exception:
        pass
    return tuple(leads)


def _carries_on(words, run):
    length = len(run)
    for start in range(len(words) - length):
        if words[start:start + length] == run:
            return True
    return False


def _run_in_the_answer(words, tokens, answer):
    for length in range(min(8, len(words)), 2, -1):
        tail = words[-length:]
        for start in range(len(tokens) - length + 1):
            if all(tokens[start + offset][0] == tail[offset] for offset in range(length)):
                return tail, tokens[start + length - 1][1], start + length
    return None


THE_CAUSE = re.compile(r"\bwhy\b[^,.;?!]{0,60}\b(?:dying|wilting|drooping)\b"
                       r"|\bwhat (?:am i|are we) doing wrong\b"
                       r"|\bwhat(?:'s| is| are) (?:killing|causing)\b")
_PEOPLE = frozenset("""mum mom mother mum's dad father gran granny nan nana grandad grandpa
son daughter child baby wife husband partner boyfriend girlfriend brother sister friend mate
fiance fiancee aunt uncle cousin niece nephew he she him her his hers they them their people
person someone somebody anyone everyone""".split())
_CONDOLENCE = re.compile(r"^(?:oh\s+)?(?:(?:i'?m|i am|so|that'?s|that is)\s+)?"
                         r"(?:so\s+|really\s+|very\s+|truly\s+)?sorry\b"
                         r"|^that'?s (?:a real|such a|awful|terrible|heartbreaking)\b")
_THE_NAMELESS = frozenset("""about after again also been before being both could does doing down
even every from have here into just like made make many more most much must need never only other
ought over same should since some such than that their them then there these they thing things
this those through under until very were what when where which while will with would your yours
really actually still might shall upon got gets going gone want wants wanted know knows saying
said tells told feel feels felt look looks looked take takes took today yesterday tomorrow week
month year time days just""".split())


def _a_condolence(reply):
    said = _content(reply).lower()
    return bool(said) and bool(_CONDOLENCE.match(said))


def _says_the_subject(reply, line):
    said = {word for word in WORD.findall(_content(reply).lower()) if len(word) >= 4}
    if not said:
        return False
    for word in WORD.findall(line):
        if len(word) < 4 or word in _THE_NAMELESS:
            continue
        for other in said:
            if other.startswith(word) or word.startswith(other):
                return True
    return False


def _the_cause_asked_for(candidates, real, text, best):
    if not _a_condolence(candidates[best].get("reply")):
        return None
    line = _content(text).lower()
    if not THE_CAUSE.search(line):
        return None
    if _says_the_subject(candidates[best].get("reply"), line):
        return None
    if set(WORD.findall(line)) & _PEOPLE:
        return None
    for index in real:
        if index == best:
            continue
        if _says_the_subject(candidates[index].get("reply"), line):
            return index
    return None


def _the_date_fact(candidates, real, text):
    if not facts.asks_for_a_when(_content(text)):
        return None
    store = None
    for index in real:
        candidate = candidates[index]
        if candidate.get("module") != "memory_store":
            continue
        if _priority(candidate) < RECALL:
            continue
        if facts.the_fact_asked_for(_content(text), _content(candidate.get("reply"))):
            store = index
            break
    if store is None:
        return None
    said = _content(candidates[store].get("reply"))
    for index in real:
        if index == store:
            continue
        if facts.the_same_date(_content(candidates[index].get("reply")), said):
            return None
    return store


def _the_next_part(candidates, text, last):
    if not last or _repeat is None:
        return None
    try:
        if not _repeat.asks_for_more(text):
            return None
        leads = tuple(getattr(_repeat, "NEXT_LEADS", ())) + tuple(getattr(_repeat, "ALSO_LEADS", ()))
    except Exception:
        return None
    return _a_lead_line(candidates, leads, last)


def _a_lead_line(candidates, leads, last):
    openers = tuple(str(lead).split("{")[0].strip().lower() for lead in leads if str(lead))
    if not openers:
        return None
    found = []
    for index, candidate in enumerate(candidates):
        reply = str(candidate.get("reply") or "").strip()
        if not reply or not reply.lower().startswith(openers):
            continue
        if last and _content(reply) == last:
            continue
        found.append((len(_content(reply).split()), index))
    if not found:
        return None
    found.sort()
    return found[-1][1]
def _only_acknowledges(memory):
    understood = memory.get("understood") if isinstance(memory, dict) else None
    if not isinstance(understood, dict):
        return False
    if _labels(understood.get("topics")):
        return False
    if understood.get("kind") == "thanks":
        return True
    return (understood.get("intent") == "ack" and not understood.get("asks")
            and understood.get("kind") != "question")


def _a_presence_check(memory):
    understood = memory.get("understood") if isinstance(memory, dict) else None
    if not isinstance(understood, dict):
        return False
    if _labels(understood.get("topics")):
        return False
    if not understood.get("presence"):
        return False
    turns = memory.get("turns")
    if isinstance(turns, list) and turns and isinstance(turns[-1], dict):
        if str(turns[-1].get("module") or "") in ("loss", "safety"):
            return False
    return True


def _about_the_bot(candidates, clean, last=""):
    try:
        kind = fallback.about_the_bot(clean)
    except Exception:
        return None
    if kind not in _my_workings():
        return None
    if not candidates or not _declares_topics(candidates[0].get("module")):
        return None
    for index, candidate in enumerate(candidates):
        if _priority(candidate) >= 0 or _declares_topics(candidate.get("module")):
            continue
        reply = _content(candidate.get("reply"))
        if not reply or (last and reply == last):
            continue
        return index
    return None


def _the_venue_hours_turn(candidates, clean, last="", text=""):
    try:
        if not fallback.venue_hours(clean, None):
            return None
    except Exception:
        return None
    if not candidates or not _declares_topics(candidates[0].get("module")):
        return None
    try:
        lines = frozenset(_content(line) for line in fallback.venue_hours_lines())
    except Exception:
        return frozenset()
    if not lines:
        return None
    for index, candidate in enumerate(candidates):
        if _priority(candidate) >= 0 or _declares_topics(candidate.get("module")):
            continue
        reply = _content(candidate.get("reply"))
        if reply and reply in lines and not (last and reply == last):
            return index
    return None


def _the_bots_own_taste(candidates, clean, memory, last=""):
    if not candidates or not _declares_topics(candidates[0].get("module")):
        return None
    try:
        asked = fallback.reads_as_a_taste(clean, memory)
    except Exception:
        return None
    if not asked:
        return None
    try:
        lines = frozenset(_content(line) for line in (getattr(fallback, "TASTE_LINES", ()) or ()))
    except Exception:
        return None
    if not lines:
        return None
    for index, candidate in enumerate(candidates):
        if _priority(candidate) >= 0 or _declares_topics(candidate.get("module")):
            continue
        reply = _content(candidate.get("reply"))
        if not reply or (last and reply == last):
            continue
        if reply in lines:
            return index
    return None


def _my_workings():
    try:
        return frozenset(getattr(fallback, "MY_WORKINGS", ()) or ())
    except Exception:
        return frozenset()


def _declares_topics(module_name):
    try:
        module = importlib.import_module("." + str(module_name), __package__)
    except Exception:
        return False
    return bool(_labels(getattr(module, DECLARED_TOPICS, ())))


def _reads_as_a_verdict(text, memory=None):
    reader = getattr(fallback, "reads_as_a_verdict", None)
    if reader is None:
        return False
    try:
        return bool(reader(text, memory))
    except Exception:
        return False


def _verdict_lines():
    lines = set()
    for name in ("VERDICT_ANNOY", "VERDICT_LUCK", "VERDICT_SHAME", "VERDICT_ROUGH",
                 "VERDICT_HEAVY", "VERDICT_NUMB"):
        try:
            lines.update(getattr(fallback, name, ()))
        except Exception:
            continue
    return frozenset(_content(line) for line in lines)


def _the_verdict_turn(candidates, lines):
    for index, candidate in enumerate(candidates):
        if _content(candidate.get("reply")) in lines:
            return index
    return None


def _in_a_careful_thread(clean, memory):
    kind, _target = _composer_reading(clean, memory)
    if kind in (THREAD, CARE_THREAD):
        return True
    try:
        return bool(getattr(fallback, "in_a_safety_thread", lambda _memory: False)(memory))
    except Exception:
        return False


KEEPS_ITS_OWN_ANSWER = ("memory_store", "chat")
ANSWERS_THE_NEWS = ("answers",)
A_VERDICT_BACK = re.compile(
    r"^\W*(?:it\s+is|it'?s|it\s+does|it\s+doesn'?t|that\s+is|that'?s|that\s+would|that'?d|"
    r"that\s+kind|that\s+sounds|you'?re\s+right|you\s+are\s+right|yeah|yes|true|fair\s+enough|"
    r"of\s+course|same\s+here|i\s+know|i\s+don'?t\s+blame|anyone\s+would)\b")
NOT_A_SUBJECT_WORD = frozenset((
    "the", "and", "but", "for", "with", "you", "your", "yours", "they", "them", "their", "his",
    "her", "hers", "she", "him", "our", "ours", "us", "its", "it", "that", "this", "these",
    "those", "was", "were", "been", "are", "am", "is", "be", "does", "did", "done", "have",
    "has", "had", "can", "cant", "cannot", "will", "would", "should", "could", "may", "might",
    "must", "not", "nor", "off", "out", "down", "too", "very", "really", "much", "many", "some",
    "any", "all", "more", "most", "just", "only", "then", "there", "here", "now", "how", "what",
    "when", "where", "why", "who", "which", "about", "than", "into", "onto", "over", "under",
    "again", "still", "even", "ever", "never", "get", "got", "gets", "one", "two", "put", "say",
    "says", "said", "think", "know", "like", "want", "need", "make", "made", "take", "took",
    "going", "went", "gone", "come", "came", "keep", "keeps", "kept", "let", "lets"))


def _subject_words(text):
    words = set()
    for word in WORD.findall(str(text or "").lower()):
        if len(word) < 3 or word in NOT_A_SUBJECT_WORD:
            continue
        for ending in ("ies", "es", "s"):
            if word.endswith(ending) and len(word) > len(ending) + 2:
                word = word[:-len(ending)] + ("y" if ending == "ies" else "")
                break
        words.add(word)
    return words


def _about_the_news(reply, memory):
    news = set()
    turns = (memory or {}).get("turns") if isinstance(memory, dict) else None
    if isinstance(turns, list) and turns and isinstance(turns[-1], dict):
        news |= _subject_words(turns[-1].get("user"))
        news |= _subject_words(turns[-1].get("bot"))
    return bool(news & _subject_words(reply))


def _says_the_same_thing_again(reply, last):
    if not last:
        return False
    words = _subject_words(reply)
    said = _subject_words(last)
    if not words or not said:
        return False
    shared = words & said
    return len(shared) >= 2 and len(shared) * 2 >= len(words)


def _the_subject_was_answered(candidate, memory):
    turns = (memory or {}).get("turns") if isinstance(memory, dict) else None
    if not (isinstance(turns, list) and turns and isinstance(turns[-1], dict)):
        return False
    last = turns[-1]
    if str(last.get("module") or "") != str(candidate.get("module") or ""):
        return False
    said = {word for word in _subject_words(last.get("bot")) if len(word) >= 5}
    return len(said & {word for word in _subject_words(candidate.get("reply")) if len(word) >= 5}) >= 2


def _the_verdict_back(candidates, last="", memory=None):
    for module_name in KEEPS_ITS_OWN_ANSWER + ANSWERS_THE_NEWS:
        is_a_card = module_name in ANSWERS_THE_NEWS
        for index, candidate in enumerate(candidates):
            if str(candidate.get("module") or "") != module_name:
                continue
            if _priority(candidate) < 0:
                continue
            reply = _content(candidate.get("reply"))
            if not reply:
                continue
            if last and (reply == last or _echoes(candidate.get("reply"), last)):
                continue
            if _says_the_same_thing_again(candidate.get("reply"), last):
                continue
            if not is_a_card and A_VERDICT_BACK.match(reply):
                return index
            if _about_the_news(candidate.get("reply"), memory):
                if not _the_subject_was_answered(candidate, memory):
                    return index
                continue
    return None


def _verdict_reply(candidates, text, memory, last="", clean="", best=0):
    if not _reads_as_a_verdict(text, memory):
        return None
    if _priority(candidates[best]) >= WHOLE_LINE_BAND:
        return None
    if _in_a_careful_thread(clean or text, memory):
        return None
    back = _the_verdict_back(candidates, last, memory)
    if back is not None:
        return back
    return _the_verdict_turn(candidates, _verdict_lines())


def _instead(text, candidates, last="", own=(), clean=""):
    for index, candidate in enumerate(candidates):
        module = candidate.get("module")
        if not _declares_instead(module):
            continue
        if last and _content(candidate.get("reply")) == last:
            continue
        keeps = _defers(module, candidates, skip=index, last=last, own=own, clean=clean,
                        text=text)
        if keeps is not None:
            return keeps
        subject = aboutness.after_a_change_of_subject(text)
        if subject:
            closer = aboutness.the_better_answer(candidate.get("reply") or "", candidates, subject,
                                                 skip=index, need=1)
            if closer is not None:
                continue
        keeps = _the_entry_that_answers_the_ask(candidates, index, clean or text)
        if keeps is not None:
            return keeps
        return index
    return None


ASK_CLAUSE_SPLIT = re.compile(r",|\band\b|\bbut\b|\bsince\b|\bbecause\b|\bso\b", re.I)
ASKS_FOR_A_THING = re.compile(
    r"\b(?:what|which|where|who|whose|when|why|how|should|shall|can|could|do|does|did|is|are"
    r"|was|were|will|would)\b"
    r"|\b(?:need|needs|needed|want|wants|wanted|looking for|have to|has to|had to|got to|"
    r"gotta|after a|after some|in need of)\b")


def _the_ask_clause(line):
    text = str(line or "")
    if not text:
        return ()
    parts = [part.strip() for part in ASK_CLAUSE_SPLIT.split(text) if part.strip()]
    if len(parts) < 2:
        return ()
    last = parts[-1]
    if not ASKS_FOR_A_THING.search(last.lower()):
        return ()
    words = tuple(word for word in WORD.findall(last.lower()) if len(word) >= LONG_ENOUGH)
    if len(words) < 2:
        return ()
    return words


def _the_entry_that_answers_the_ask(candidates, skip, line):
    words = _the_ask_clause(line)
    if not words:
        return None
    for index, candidate in enumerate(candidates):
        if index == skip or _declares_instead(candidate.get("module")):
            continue
        if _priority(candidate) < 0:
            continue
        reply = candidate.get("reply")
        if not reply or not _about_the_line(reply, words):
            continue
        if _about_the_line(candidates[skip].get("reply"), words):
            return None
        return index
    return None


def _defers(module_name, candidates, skip, last="", own=(), clean="", text=""):
    test = _defers_to(module_name)
    if test is None:
        return None
    for index, candidate in enumerate(candidates):
        if index == skip or _declares_instead(candidate.get("module")):
            continue
        if int(candidate.get("priority") or 0) < 0:
            continue
        if own and _match(candidate.get("module"), own, (), (), clean) <= 0:
            continue
        if last and _content(candidate.get("reply")) == last:
            continue
        reply = candidate.get("reply") or ""
        try:
            if test(reply, text):
                return index
        except TypeError:
            try:
                if test(reply):
                    return index
            except Exception:
                continue
        except Exception:
            continue
    return None


def _defers_to(module_name):
    try:
        module = importlib.import_module("." + str(module_name), __package__)
    except Exception:
        return None
    test = getattr(module, DECLARED_DEFERS, None)
    return test if callable(test) else None


def _declares_instead(module_name):
    try:
        module = importlib.import_module("." + str(module_name), __package__)
    except Exception:
        return False
    return bool(_labels(getattr(module, DECLARED_INSTEAD, ())))


def _pause_reply(candidates, pool, text, memory, last=""):
    try:
        if _composer_reading(text, memory)[0] != PAUSE:
            return None
        said = {_content(line) for line in fallback.CAME_BACK}
        said |= {_content(line) for line in fallback.RETURNED_TO_IT}
        named = fallback.reads_as_a_return(text)
        if named:
            said |= {_content(line.format(thing=named))
                    for line in fallback.RETURNED_TO_A_THING}
    except Exception:
        return None
    kept = None
    for index in pool:
        if _priority(candidates[index]) >= WHOLE_LINE_BAND:
            return None
    for index, candidate in enumerate(candidates):
        said_back = _content(candidate.get("reply"))
        if said_back not in said:
            continue
        if not last or said_back != last:
            return index
        kept = index if kept is None else kept
    return kept


def _leaving_reply(candidates, own, carried, words, clean, text, memory, last=""):
    typed = " ".join(str(text or "").lower().split())
    try:
        if not leaving.reads_as_leaving(typed):
            return None
        said = {_content(line) for line in leaving.lines()}
    except Exception:
        return None
    try:
        if _composer_reading(text, memory)[0] == THREAD:
            return None
    except Exception:
        return None
    small_talk = _labels(("small-talk",))
    try:
        reasoned = leaving.pool(typed) is leaving.REASON_POOL
    except Exception:
        reasoned = False
    for index, candidate in enumerate(candidates):
        if _declared(candidate.get("module")) & small_talk and not _asks(candidate.get("reply")) \
                and (not reasoned or _a_sign_off(candidate.get("reply"))):
            return index
    spare = None
    for index, candidate in enumerate(candidates):
        said_back = _content(candidate.get("reply"))
        if said_back in said:
            if not last or said_back != last:
                return index
            spare = index if spare is None else spare
    if spare is not None:
        return spare
    for index, candidate in enumerate(candidates):
        if _priority(candidate) < 0:
            continue
        if _match(candidate.get("module"), own, carried, words, clean) <= 0:
            return index
    return None


def _asks(reply):
    return "?" in str(reply or "")


def _a_sign_off(reply):
    try:
        return leaving.reads_as_a_sign_off(reply)
    except Exception:
        return False


def _declared(module_name):
    try:
        module = importlib.import_module("." + str(module_name), __package__)
    except Exception:
        return ()
    return _labels(getattr(module, DECLARED_TOPICS, ()))


def _the_store_revises_the_answer(candidates, pool, memory, text, last=""):
    if not last or not isinstance(memory, dict):
        return None
    held = [memory.get("user")]
    others = memory.get("others")
    if isinstance(others, list):
        held.extend(others)
    dislikes = [str(thing).lower()
                for person in held if isinstance(person, dict)
                for thing in (person.get("dislikes") or []) if thing]
    if not dislikes:
        return None
    said = set(_content(text).split())
    if not said & set(dislikes):
        return None
    previous = last.split()
    for index in pool:
        if candidates[index].get("module") != "memory_store":
            continue
        reply = candidates[index].get("reply") or ""
        if _a_clause_was_cut_in_half(reply):
            continue
        words = _content(reply).split()
        for start in range(0, max(0, len(words) - 4)):
            run = words[start:start + 5]
            if len(run) == 5 and _a_run_of(previous, run):
                return index
    return None


def _a_clause_was_cut_in_half(reply):
    words = _content(reply).split()
    return any(word in ("which", "whose") for word in words)


def _store_correcting(candidates, pool, memory, text, last=""):
    fixed = memory.get("correction") if isinstance(memory, dict) else None
    if not isinstance(fixed, dict) or not fixed.get("value"):
        return None
    if str(fixed.get("said") or "") != " ".join(str(text or "").lower().split()):
        return None
    for index in pool:
        if candidates[index].get("module") != "memory_store":
            continue
        if last and _content(candidates[index].get("reply")) == last:
            return None
        return index
def _draft_index(candidates, last, clean=""):
    for index, candidate in enumerate(candidates):
        if candidate.get("module") != fallback.FALLBACK_MODULE:
            continue
        reply = candidate.get("reply")
        if not _content(reply) or _content(reply) == last:
            return None
        if fallback.draft.names_a_draft(reply):
            return index
        if (clean and fallback.draft.offers_a_draft(reply)
                and fallback.draft.reads_as_a_writing_ask(clean)
                and not any(fallback.draft.offers_a_draft(other.get("reply"))
                            or fallback.draft.hands_over_words(other.get("reply"))
                            or fallback.draft.hands_over_the_shape(other.get("reply"))
                            for other in candidates if other is not candidate)):
            return index
        return None
    return None


def _a_leaving_said_plain(candidates, pool, clean, memory):
    if not clean:
        return None
    try:
        if not (badnews.reads_as_the_leaving(clean)
                or badnews.reads_as_a_leaving_already_gone(clean)):
            return None
    except Exception:
        return None
    understood = memory.get("understood") or {}
    if (understood.get("kind") == "question"
            or understood.get("intent") in ("question", "request")
            or understood.get("help_ask") or understood.get("asks_a_verdict")):
        return None
    index = _is_loss_reply_in(candidates, pool,
                              pools=(fallback.LEFT_POOL, fallback.LEFT_POOL_GONE))
    if index is None:
        return None
    best = pool[0] if pool else None
    if best is None or not _opens_on_a_job(candidates[best].get("reply")):
        return None
    return index


def _sudden_loss_reply(candidates, pool, clean):
    try:
        if not clean:
            return None
        if not (badnews.reads_as_sudden_loss(clean)
                or badnews.reads_as_pregnancy_bleeding(clean)):
            return None
        if fallback.asks_what_to_tell_a_child(clean) and _a_knowledge_entry_has_it(candidates):
            return None
        pools = (fallback.SUDDEN_LOSS, fallback.PREGNANCY_BLEEDING,
                 fallback.THE_FIRST_HOUR_AND_A_CHILD)
    except Exception:
        return None
    return _is_loss_reply_in(candidates, pool, pools)


def _the_words_for_the_child(candidates, clean, memory, last=""):
    from ..compose import childwords
    try:
        if not clean or not childwords.asks_the_words_for_a_child(clean, memory):
            return None
    except Exception:
        return None
    for index, candidate in enumerate(candidates):
        if candidate.get("module") != fallback.FALLBACK_MODULE:
            continue
        reply = _content(candidate.get("reply"))
        if not reply or (last and reply == last):
            continue
        if reply in _the_words_for_a_child_pool():
            return index
    return None


def _a_whole_line_module_spoke(candidates):
    for candidate in candidates:
        if _priority(candidate) >= WHOLE_LINE_BAND and candidate.get("module") != fallback.FALLBACK_MODULE:
            return True
    return False


def _the_words_for_a_child_pool():
    from ..compose import childwords
    return tuple(_content(line) for line in childwords.THE_WORDS_FOR_A_CHILD)


def _the_ask_about_a_child(candidates, clean, last=""):
    try:
        if not fallback.asks_what_to_tell_a_child(clean):
            return None
    except Exception:
        return None
    for index, candidate in enumerate(candidates):
        if candidate.get("module") != "answers" or _priority(candidate) < 0:
            continue
        reply = _content(candidate.get("reply"))
        if not reply or (last and reply == last):
            continue
        return index
    return None


_A_HOW_TO = re.compile(
    r"^(?:how\s+(?:do|can|should|could|would)\s+(?:i|we|you)|how\s+to\b|"
    r"what(?:'?s|\s+is)\s+the\s+best\s+way\s+to|whats\s+the\s+best\s+way\s+to|"
    r"any\s+tips\s+(?:for|on)|what\s+should\s+i\s+do\s+(?:about|with))\b", re.I)
_THE_ONE_NAMED = re.compile(
    r"\b(?:my|our|his|her|their)\s+(?:teenager|teen|son|daughter|child|kid|boy|girl|mum|mom|"
    r"mother|dad|father|partner|husband|wife|boyfriend|girlfriend|flatmate|housemate|roommate|"
    r"friend|boss|manager|colleague|brother|sister|gran|granny|grandma|grandad|grandpa|baby|"
    r"toddler|nephew|niece|aunt|uncle|cousin)\b", re.I)
_A_PERSON_NAMED = re.compile(
    r"\b(?:(?:my|our|his|her|their)\s+(?:teenager|teen|son|daughter|child|kid|boy|girl|mum|mom|"
    r"mother|dad|father|partner|husband|wife|boyfriend|girlfriend|flatmate|housemate|roommate|"
    r"friend|boss|manager|colleague|brother|sister|gran|granny|grandma|grandad|grandpa|baby|"
    r"toddler|nephew|niece|aunt|uncle|cousin)|"
    r"(?:a|an|the|this|that|one)\s+(?:friend|mate|neighbour|neighbor|colleague|coworker|"
    r"co-worker|classmate|loved\s+one|relative|family\s+member))\b", re.I)
_ABOUT_SOMEONE_ELSE = re.compile(
    r"\b(?:they|them|their|theirs|themselves|he|she|him|his|hers)\b", re.I)


def _the_name_they_gave(candidates, text, memory):
    if _naming is None:
        return None
    name = _naming.the_name_given(text, memory)
    if not name:
        return None
    said = name.lower()
    for index, candidate in enumerate(candidates):
        if _priority(candidate) < 0:
            continue
        if said in str(candidate.get("reply") or "").lower():
            return index
    return None


def _about_the_person_the_line_names(candidates, pool, clean, last=""):
    if not clean or not _A_HOW_TO.match(clean):
        return None
    named = _THE_ONE_NAMED.search(clean)
    if named is None:
        return None
    first = _A_PERSON_NAMED.search(clean)
    if first is None or first.start() != named.start():
        return None
    word = named.group(0).split()[-1].lower()
    if _priority(candidates[pool[0]]) >= RECALL:
        return None
    front = _content(candidates[pool[0]].get("reply"))
    if not front:
        return None
    if re.search(r"\b%ss?\b" % re.escape(word.rstrip("s")), front, re.I) or \
            _ABOUT_SOMEONE_ELSE.search(front):
        return None
    for index in pool[1:]:
        candidate = candidates[index]
        if _priority(candidate) >= RECALL or candidate.get("module") != "answers":
            continue
        reply = _content(candidate.get("reply"))
        if not reply or (last and reply == last):
            continue
        if fallback.is_a_hedge(reply):
            continue
        if re.search(r"\b%ss?\b" % re.escape(word.rstrip("s")), reply, re.I) or \
                _ABOUT_SOMEONE_ELSE.search(reply):
            return index
    return None


def _a_knowledge_entry_has_it(candidates):
    for candidate in candidates:
        if int(candidate.get("priority") or 0) >= 0 and candidate.get("module") == "answers":
            return True
    return False


def _hurting_reply(candidates, pool, clean):
    if _harm is None or not clean:
        return None
    try:
        if not _harm.reads_as_hurting_someone(clean):
            return None
    except Exception:
        return None
    for index in list(pool) + list(range(len(candidates))):
        try:
            if _harm.reads_as_our_reply(candidates[index].get("reply")):
                return index
        except Exception:
            continue
    return None


def _story_goes_on_reply(text, memory, candidates, last=""):
    if _ack is None:
        return None
    try:
        if not _ack.carries_the_story_on(text, memory):
            return None
        if (not _a_story_opened(memory) and not _a_refusal(text)
                and any(_priority(candidate) >= 0 for candidate in candidates)):
            return None
        pools = (_ack.THE_STORY_GOES_ON,)
        for index, candidate in enumerate(candidates):
            if int(candidate.get("priority") or 0) >= SAFETY:
                continue
            reply = str(candidate.get("reply") or "").strip()
            if not reply or (last and _content(reply) == last):
                continue
            if any(reply in wanted for wanted in pools):
                return index
    except Exception:
        return None
    return None


def _a_story_opened(memory):
    if _loss is None:
        return True
    for turn in (memory.get("turns") or [])[-2:]:
        if not isinstance(turn, dict):
            continue
        said = str(turn.get("user") or "").strip().lower()
        if not said:
            continue
        if _dream is not None and _dream.named(said) and not _dream.a_death_came_first(said):
            continue
        if _loss.reads_as_loss(said):
            return True
        try:
            if badnews.reads_as_the_leaving(said) or badnews.reads_as_a_leaving_already_gone(said):
                return True
        except Exception:
            continue
    return False


REFUSAL = re.compile(r"\b(?:won'?t|wont|wouldn'?t|refus\w*|isn'?t eating|not eating|"
                     r"doesn'?t want|does not want|gives? up|gave up|stops? eating)\b")


def _a_refusal(text):
    return bool(REFUSAL.search(str(text or "").lower().replace("\u2019", "'")))


def _is_loss_reply_in(candidates, pool, pools):
    for index in list(pool) + list(range(len(candidates))):
        text = str(candidates[index].get("reply") or "").strip()
        if text and any(text in wanted for wanted in pools):
            return index
    return None


def _composer_reading(clean, memory):
    try:
        from ..compose import fallback as composer
        kind, target = composer.reading(clean, memory)
    except Exception:
        return "", ()
    return (kind, target) if kind else ("", ())


def _carries_the_answer(reply, memory):
    if not reply:
        return False
    try:
        from ..compose import verdict as composer
        return bool(composer.carries_the_answer(reply, memory))
    except Exception:
        return False


def _a_check_on_the_answer(reply):
    if not reply:
        return False
    try:
        from ..compose import verdict as composer
        return bool(composer.a_check_on_the_reply(reply))
    except Exception:
        return False


def _opens_on_a_job(reply):
    if not reply:
        return False
    try:
        from ..compose import verdict as composer
        return bool(composer.opens_on_a_job(reply))
    except Exception:
        return False


def _is_a_generic_step(reply):
    if not reply or not _STEP_WHEN_LOW:
        return False
    return reply.strip() in _STEP_WHEN_LOW


def _named_topics(memory):
    understood = memory.get("understood")
    if not isinstance(understood, dict):
        return set()
    return _labels(understood.get("topics")) - CHITCHAT


CHITCHAT = frozenset(("small talk",))


def _thread_index(candidates, real, own, target, last, care_about="", memory=None, line=""):
    text = target[0] if target else ""
    if not _content(text):
        return None
    asks = fallback.asks_about_a_care_answer(care_about, last, memory, own)
    pointed_at = _outlook.points_at_the_thread(line or text)
    if (not pointed_at and any(own and _labels(_answered(candidates[index].get("module"))) & own
                               for index in real) and not asks):
        return None
    for index, candidate in enumerate(candidates):
        if _priority(candidate) < 0 and candidate.get("module") == fallback.FALLBACK_MODULE:
            reply = _content(candidate.get("reply"))
            if not reply or reply == last:
                return None
            if asks:
                mine = fallback.how_much_of_the_answer_kept(candidate.get("reply"), memory)
                for other in real:
                    closer = fallback.how_much_of_the_answer_kept(
                        candidates[other].get("reply"), memory)
                    if closer > mine:
                        return other
            return index
    return None


def _answers_this_line(reply):
    if not reply or fallback.is_said_it_already(reply):
        return False
    return _opens_on_a_job(reply)


def _content(reply):
    return " ".join(WORD.findall(str(reply or "").lower()))


def _echoes(reply, last, announced=False):
    words = _content(reply).split()
    previous = _content(last).split()
    if len(previous) < 12 or len(words) < 12:
        return False
    for lead in range(0, min(6, len(words) - 12) + 1):
        run = words[lead:]
        if len(run) >= 12 and _a_run_of(previous, run):
            return True
    if announced:
        handed = _the_quoted_repeat(reply)
        if handed:
            run = handed.split()
            if len(run) >= 8 and _a_run_of(previous, run):
                return True
    return False


AGAIN_FIRST_WORDS = 16
AGAIN_TAIL_WORDS = 12


def _the_answer_again_with_a_tail(reply, last):
    words = _content(reply).split()
    previous = _content(last).split()
    if len(previous) < AGAIN_FIRST_WORDS:
        return False
    same = 0
    while same < len(words) and same < len(previous) and words[same] == previous[same]:
        same += 1
    return same >= AGAIN_FIRST_WORDS and len(words) - same <= AGAIN_TAIL_WORDS


def _the_quoted_repeat(reply):
    text = _content(reply)
    if not text:
        return None
    heads = [_content(lead) for lead in _repeat_leads()]
    try:
        heads.extend(_content(str(frame).split("{")[0]) for frame in getattr(_repeat, "LEADS", ()))
    except Exception:
        pass
    for head in heads:
        if head and text.startswith(head):
            return text[len(head):].strip()
    return None


A_POINTS_BACK = re.compile(
    r"\bis in what I said above\b|\bis in the answer above\b|\bis covered by the answer above\b"
    r"|\bwhat I said above is the whole of it\b|\bthan what I said above\b"
    r"|\bis the whole of what I have on it\b"
    r"|\bnothing separate on\b|\bnothing more on\b|\bno separate answer for\b",
    re.IGNORECASE)


def _points_back(reply):
    return bool(A_POINTS_BACK.search(str(reply or "")))


def _a_run_of(previous, run):
    size = len(run)
    return any(previous[start:start + size] == run
               for start in range(0, len(previous) - size + 1))


def _the_answer_written_out(memory):
    turns = memory.get("turns")
    if isinstance(turns, list) and turns and isinstance(turns[-1], dict):
        return str(turns[-1].get("bot") or "")
    return ""


def _last_reply(memory):
    turns = memory.get("turns")
    if isinstance(turns, list) and turns and isinstance(turns[-1], dict):
        return _content(turns[-1].get("bot"))
    return ""


def _said_before(memory, text):
    said = set()
    turns = memory.get("turns")
    if not isinstance(turns, list):
        return said
    asked = _content(text)
    for turn in turns:
        if not isinstance(turn, dict):
            continue
        if asked and _content(turn.get("user")) == asked:
            continue
        reply = _content(turn.get("bot"))
        if len(reply.split()) >= _SAID_BEFORE_WORDS:
            said.add(reply)
    return said


def _about(text, memory):
    understood = memory.get("understood")
    own = set()
    words = set()
    if isinstance(understood, dict):
        own |= _labels(understood.get("topics"))
        own |= _labels(understood.get("topic"))
        for word in _strings(understood.get("words")):
            words.update(WORD.findall(word.lower()))
    carried = _labels(memory.get("topic")) - own
    clean = " ".join(WORD.findall(str(text).lower()))
    words.update(clean.split())
    return own, carried, words, clean


def _strings(value):
    if isinstance(value, str):
        return [value]
    if isinstance(value, (list, tuple, set, frozenset)):
        return [item for item in value if isinstance(item, str)]
    return []


def _label(value):
    return " ".join(WORD.findall(str(value).lower()))


def _labels(value):
    found = set()
    if isinstance(value, str):
        found.add(_label(value))
    elif isinstance(value, dict):
        found |= _stored(value)
        for key in LABEL_KEYS:
            if isinstance(value.get(key), str):
                found.add(_label(value[key]))
                break
        else:
            if "topics" in value:
                found |= _labels(value.get("topics"))
            elif value and all(not isinstance(item, (dict, list, tuple))
                               for item in value.values()):
                for key in value:
                    if isinstance(key, str) and key not in LABEL_KEYS:
                        found.add(_label(key))
    elif isinstance(value, (list, tuple, set, frozenset)):
        for item in value:
            found |= _labels(item)
    found.discard("")
    return found


def _stored(record):
    text = record.get("text") if isinstance(record.get("text"), str) else ""
    if not text.strip():
        text = " ".join(_strings(record.get("words")))
    return _read_topic(text)


def _read_topic(text):
    key = " ".join(WORD.findall(str(text or "").lower()))
    if not key:
        return set()
    found = READ.get(key)
    if found is None:
        try:
            from ..understanding import topics as understood
            from ..understanding.normalize import normalise
            read = normalise(key)
            topic, score = understood.detect_topic(read, None, understood.detect_entities(read))
            found = {_label(topic)} if topic and score >= 2 else set()
        except Exception:
            found = set()
        READ[key] = found
    return set(found)


def _answered(module_name):
    try:
        module = importlib.import_module("." + str(module_name), __package__)
    except Exception:
        return set()
    return _labels(getattr(module, DECLARED_TOPICS, ()))


def _match(module_name, own, carried, words, clean):
    score = 0
    padded = " " + clean + " "
    for label in _answered(module_name):
        if label in own:
            score += 2
        elif label in carried:
            score += 1
        elif " " in label:
            if " " + label + " " in padded:
                score += 1
        elif label in words:
            score += 1
    return score


def _the_subject_words(text):
    words = set()
    for phrase in A_SUBJECT_PHRASE.findall(str(text or "").lower()):
        words.update(word for word in A_SUBJECT_WORD.findall(phrase)
                     if word not in NOT_A_SUBJECT_WORD)
    return words


def _the_lines_own_words(text, memory):
    understood = memory.get("understood") if isinstance(memory, dict) else None
    words = _the_subject_words(text)
    if isinstance(understood, dict) and understood:
        subject = understood.get("subject")
        if isinstance(subject, str) and subject:
            words.update(A_SUBJECT_WORD.findall(subject.lower()))
        words.update(word for word in _the_subject_words(subject or "")
                     if word not in NOT_A_SUBJECT_WORD)
    return {word for word in words if word not in NOT_A_SUBJECT_WORD}


def _the_forms_of(word):
    forms = {word}
    if word.endswith("s") and len(word) > 3:
        forms.add(word[:-1])
        if word.endswith("es") and len(word) > 4:
            forms.add(word[:-2])
    if word.endswith("ed") and len(word) > 4:
        forms.update((word[:-2], word[:-1]))
    if word.endswith("ing") and len(word) > 5:
        forms.update((word[:-3], word[:-3] + "e"))
    return {form for form in forms if len(form) >= 3}


def _the_same_word(said, word):
    return said in _the_forms_of(word)


def _names_a_word_of(a_reply, words):
    said = A_SUBJECT_WORD.findall(_content(a_reply))
    return any(_the_same_word(one, word) for one in said for word in words)


def _a_card_names_the_line(candidates, index, text, memory):
    words = _the_lines_own_words(text, memory)
    if not words:
        return False
    if _names_a_word_of(candidates[index].get("reply"), words):
        return False
    for other, other_candidate in enumerate(candidates):
        if other == index or _priority(other_candidate) < 0:
            continue
        if _names_a_word_of(other_candidate.get("reply"), words):
            return True
    return False


def _a_detail_added_to_the_news(candidates, pool, text, memory):
    if not reads_as_a_detail_of_the_news(text, memory):
        return None
    for index in pool:
        if _priority(candidates[index]) < 0:
            continue
        if reads_as_the_detail_line(candidates[index].get("reply")):
            return index
    return None


def _shares_a_stem(one, other):
    return len(one) >= 5 and len(other) >= 5 and one[:5] == other[:5]


NOT_A_NEW_WORD = frozenset("""
thanks thank sorry please pardon cheers again alright okay ok right really maybe perhaps actually
still even ever always whole little another other thing things lot stuff first next then step steps
""".split())


def _the_word_the_line_added(text, last):
    said = WORD.findall(str(last or "").lower())
    words = [word for word in A_SUBJECT_WORD.findall(str(text or "").lower())
             if len(word) >= 5 and word not in NOT_A_SUBJECT_WORD
             and word not in NOT_A_NEW_WORD]
    fresh = [word for word in words
             if not any(_shares_a_stem(word, one) for one in said)]
    return max(fresh, key=len) if fresh else ""


def _says_nothing_new(reply, last):
    said = set(WORD.findall(_content(last)))
    glue = NOT_A_SUBJECT_WORD | NOT_A_NEW_WORD
    loose = [word for word in WORD.findall(_content(reply))
             if len(word) >= 4 and word not in glue]
    fresh = [word for word in loose
             if word not in said and not any(_shares_a_stem(word, one) for one in said)]
    return len(fresh) <= 1


def _names_the_word(a_reply, word):
    return any(_shares_a_stem(said, word) for said in WORD.findall(_content(a_reply)))


def _the_answer_that_names_what_the_line_added(candidates, pool, text, last):
    if len(pool) < 2 or not last:
        return None
    added = _the_word_the_line_added(text, last)
    if not added:
        return None
    if not _says_nothing_new(candidates[pool[0]].get("reply"), last):
        return None
    if _names_the_word(candidates[pool[0]].get("reply"), added):
        return None
    if _priority(candidates[pool[0]]) >= RECALL:
        return None
    for index in pool[1:]:
        if _priority(candidates[index]) < 0:
            continue
        if _names_the_word(candidates[index].get("reply"), added):
            return index
    return None


def _a_card_that_names_the_line(candidates, pool, text, memory):
    if len(pool) < 2 or _priority(candidates[pool[0]]) >= CHATTER:
        return None
    if (candidates[pool[0]].get("module") in MEMORY_MODULES
            and _a_recall_from_an_earlier_turn(text, memory)):
        return None
    words = _the_lines_own_words(text, memory)
    if not words or _names_a_word_of(candidates[pool[0]].get("reply"), words):
        return None
    for index in pool[1:]:
        if _priority(candidates[index]) < 0:
            continue
        if _names_a_word_of(candidates[index].get("reply"), words):
            return index
    return None

A_PLAINER_ASK = re.compile(
    r"\b(?:explain(?:\s+(?:that|it|this))?|in plain (?:english|words)|plainer|plainly|"
    r"simpler|more simply|put (?:it|that) (?:another way|in other words)|in other words|"
    r"what (?:do you|does that) mean|i (?:don'?t|do not|didn'?t) (?:understand|get it|follow))",
    re.I)


PLAIN_ASK_FILLER = frozenset("""
a again and another ask can could did do does doing dont don't english explain explained explaining
follow following for get got how i in it just mean means meant me more not now of or plain plainer
plainly please put right say saying simpler simply so sorry that the then there this to understand
understandit want was way what word words would you your
""".split())


def _a_line_asking_for_plainer_words(text):
    clean = _content(text)
    if not clean or not A_PLAINER_ASK.search(clean):
        return False
    rest = A_PLAINER_ASK.sub(" ", clean)
    return not [word for word in A_SUBJECT_WORD.findall(rest.lower())
                if word not in PLAIN_ASK_FILLER]


def _says_the_answer_again(reply, last):
    if not reply or not last:
        return False
    said = _content(reply)
    if said and said == _content(last):
        return True
    if _the_quoted_repeat(reply) is not None:
        return True
    return bool(_echoes(reply, last, announced=True))


def _a_plainer_reading_of_the_same_answer(candidates, best, text, memory):
    if not _a_line_asking_for_plainer_words(text):
        return None
    last = _last_reply(memory)
    if not last or not _says_the_answer_again(candidates[best].get("reply"), last):
        return None
    about = _the_subject_words(last)
    if not about:
        return None
    order = sorted(range(len(candidates)), key=lambda index: -_priority(candidates[index]))
    for index in order:
        if index == best or _priority(candidates[index]) < 0:
            continue
        reply = candidates[index].get("reply")
        if not reply or _says_the_answer_again(reply, last):
            continue
        if fallback.is_a_hedge(reply) or _points_back(reply):
            continue
        if _names_a_word_of(reply, about):
            return index
    return None
