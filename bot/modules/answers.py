import copy
import difflib
import re
import string

from .. import memory as mem
from ..compose import NEGATORS, goodnews, lead, pick, with_name
from ..compose import fit as shapes
from ..compose.repair import amends_to
from ..compose import trouble as trouble_reading
from ..knowledge import (by_topic, cooking, dishes, entertainment, entries as all_entries,
                         freshness, home, meat_in_a_card, pets, shopping, topics, work)
from ..knowledge.lookup import (EXPLAIN_FILLER, EXPLAIN_LEADS, about_the_chat,
                                about_the_topic, find, leans_on_a_subject,
                                names_its_own_subject, names_nothing_of_its_own)
from ..knowledge.lookup import entry as lookup_entry
from ..memory import (ack, deadline, healing, named, narrow as length, onset, prefer, repeat,
                      taste, when)
from ..memory import hope as a_wish, matters
from ..memory import topics as memory_topics
from ..knowledge.maths import solve
from ..understanding.kinds import ANSWERING_A_QUOTED_ASK, SUMMONS_WHO
from ..memory import a_year_of_birth
from ..memory import baking, doing_it, trips
from ..memory import repeat
from ..memory import outfit
from ..memory import (followup_reading, keywords, recall, remember_answer, resize,
                     same_as_before, the_ask_about_the_thing_it_points_at)
from ..memory import stuck as stuck_line
from ..memory import again as same_again
from ..memory.again import NOTHING_MORE
from ..memory.again import AGAIN_HELP, DETAIL_AGAIN, SAME_ADVICE
from ..memory import repeat
from ..memory import topics as said_topic
from ..memory.topics import AMOUNT, ASK_ONLY, already_said, pairing, stem
from ..understanding import kinds
from ..memory.ack import VAGUE
from ..memory.topics import current as the_topic, is_follow_up
from ..memory import repeat, tried, more, returned
from ..memory import returns as went_back
from ..memory import limit
from ..memory import whereabout
from ..memory import price as a_price
from ..memory import (a_detail_of_the_thing_we_hold, answers_about_another_creature,
                      followup_reading, keywords, remember_answer, resize, same_as_before, swap,
                      the_animal_the_subject_is, the_thing_a_detail_belongs_to)
from ..memory import repeat
from ..memory.narrow import (CAUSE, RATE, SIGNALS, asks_a_part, flat, kind_of as asked_kind,
                             narrow, the_outcome_asked, the_part_asked, words_of)
from ..understanding import understand

PRIORITY = 0

GENERIC_KEEPING = ("fridge-life", "fridge-life-cooked")

ANSWERS = topics()


REFERRING = frozenset("it its that this them they one ones there these those".split())

ABOUT_YOU = re.compile(r"^\s*(?:do|does|did|are|is|can|could|would|will|have|has|were)\s+you\b",
                       re.IGNORECASE)


def _the_new_part(reply, memory, keep=3):
    said = str(reply or "").strip()
    mine = flat(said)
    if not mine:
        return None
    for turn in (memory.get("turns") or [])[-keep:]:
        if not isinstance(turn, dict):
            continue
        before = str(turn.get("bot") or "").strip()
        opening = flat(before)
        if not opening or not mine.startswith(opening) or len(mine) <= len(opening) + 15:
            continue
        if not said.startswith(before):
            continue
        added = said[len(before):].strip()
        if added[:1].isupper() and added.endswith((".", "!", "?")):
            return added
    return None


_BARE_VERDICT = re.compile(
    r"^[^.?!]{0,40}[.?!]\s+(?=.)", re.S)


def _without_the_verdict(text):
    said = " ".join(str(text or "").split())
    found = _BARE_VERDICT.match(said)
    if not found:
        return said
    head = found.group(0).strip().lower()
    if len(head.split()) > 6:
        return said
    if not re.search(r"\b(?:yes|no|not|never|always|usually|often|sometimes|normally|depends"
                     r"|mostly|generally|rarely|seldom)\b", head):
        return said
    return said[found.end():].lstrip()


_CARD_OPENINGS = None


def _card_openings():
    global _CARD_OPENINGS
    if _CARD_OPENINGS is None:
        heads = set()
        try:
            from ..knowledge import entries as _all_entries
            for item in _all_entries():
                said = getattr(item, "reply", None)
                if isinstance(said, str):
                    flat = " ".join(said.split())
                    if flat:
                        heads.add(flat[:40].lower())
        except Exception:
            heads = set()
        _CARD_OPENINGS = heads
    return _CARD_OPENINGS


def _without_a_lead(text):
    said = " ".join(str(text or "").split())
    found = _BARE_VERDICT.match(said)
    if not found:
        return said
    rest = said[found.end():].lstrip()
    if not rest or rest[:40].lower() not in _card_openings():
        return said
    head = _without_the_verdict(said)
    return head if head and head != said else said


def _opening(text, words=8):
    said = _without_the_verdict(text) or ""
    parts = re.split(r"(?<=[.!?])\s+", said.strip())
    while len(parts) > 1 and lead._CAUSE_SENTENCE.match(parts[0]):
        parts.pop(0)
    return " ".join(" ".join(parts).lower().split()[:words])


def _most_of_it_said(reply, memory, keep=3, least=40):
    said = " ".join(str(turn.get("bot") or "") for turn in (memory or {}).get("turns", ())[-keep:]
                    if isinstance(turn, dict))
    if not said:
        return False
    said = _flat(said)
    for sentence in re.split(r"(?<=[.;!?])\s+", str(reply or "")):
        for part in (sentence, re.split(r"[:;]\s+|\s+[-—]\s+", sentence)[-1]):
            if len(part) >= least and _flat(part) and _flat(part) in said:
                return True
    return False


def _said_before(reply, memory, keep=3):
    turns = memory.get("turns") or []
    mine = _opening(reply)
    if not mine:
        return False
    for turn in turns[-keep:]:
        if not isinstance(turn, dict):
            continue
        if _opening(turn.get("bot")) == mine:
            return True
    return False


AGAIN = tuple(memory_topics.REPEAT) + same_again.LIKE_I_SAID
WORD = re.compile(r"[a-z0-9']+")
NOT_A_DETAIL = frozenset("""
think thinks thinking thought know knows knowing say says saying tell tells telling ask asks
asking wonder wonders wondering guess guesses guessing consider considers considering decide
decides deciding choose chooses choosing
# "reckon" is what a lot of people say for "think", and it is an ordinary word, so the repeat
# lead-in named it: "why am i always tired do u reckon" after the tiredness card came back
# "Nothing separate for reckon - it is the same advice: ...", which is a sentence about a word
# nobody asked about, and it reads worse than the plain "same answer" because "reckon" is not a
# part of anything. The line still carries the word - it is how the opinion is asked for, and the
# readers that answer one key on it - so it is dropped here, where the lead-in is chosen, and not
# from the reading.
reckon reckons reckoned reckoning rekon rekons reckin
""".split()) | frozenset("""
# Nor is the word a negation hangs on: "i dont know why" after the low-mood card came back
# "There is nothing separate for dont - it is the same advice", and "i have no idea why" named
# "idea". A line that says where the person has got to is not naming a part of the answer, so
# the words of not-knowing name nothing here.
dont doesnt didnt cant cannot couldnt wouldnt wont shant sure idea explain explains explained clue
""".split()) | frozenset("""
# The same verb said the other ways people say it: how somebody regards the thing is the asking,
# whatever verb carries it. "i want to start running but i find it boring" reached this lead-in as
# "Nothing separate for find - it is the same advice", where the word named is the person's own
# verb and the answer says nothing about it. The line is a repeat ask and gets the plain lead-in.
find finds finding found reckon reckons reckoning suppose supposes supposing imagine imagines
imagining feel feels feeling felt hope hopes hoping wish wishes wishing
""".split()) | frozenset("""
# How somebody hopes it will go is not a part of the thing either: "i want to start running but i
# hope it gets easier" came back "Nothing separate for easier - it is the same advice", which names
# a comparison the answer was never about. A comparative is the shape of the wish, not a subject.
easier easy better worse harder faster slower quicker sooner longer cheaper dearer
""".split()) | frozenset("""
# Nor is the opinion itself a part of the thing, and it is the word people reach for: covering
# the verb of thinking left the adjective behind, so "i want to start running but i find it dull"
# still came back "Nothing separate for dull - it is the same advice" while its nearest synonym
# "boring" was answered. How they regard the thing is not a part of the answer, whichever word
# they regard it with.
boring dull tedious pointless rubbish repetitive monotonous uninteresting
""".split()) | frozenset("""
# A time is not a part of the thing either: "she had a fall a week ago" came back "Nothing
# separate for ago - it is the same advice", which names a word nobody was asking about. The
# lead-in that says the answer covers it is the honest one for a line that only adds when.
ago today yesterday tomorrow tonight recently lately
week weeks month months year years day days
""".split()) | frozenset("""
# And a person nobody named is not a part of the thing: "someone else got the promotion" after
# the promotion answer came back "Same answer for someone: ...", which reads as a mistake. The
# plain repeat lead-in says the same thing without pretending it has narrowed anything.
someone somebody anyone anybody everyone everybody nobody none else another others other
""".split()) | frozenset("""
# Nor is how often: "is it ok to run every day" after another answer came back "Nothing separate
# for every - it is the same advice: <the answer before>", which names a word nobody asked about
# and reads as a sentence about nothing. A frequency says when the answer applies, not a part of
# the thing the answer is about.
every each once twice daily weekly monthly hourly yearly always never often sometimes
usually regularly rarely seldom
""".split())
BACK_POINTS = frozenset("""there it its that those these them they this one ones him her""".split())
ASK_VERB = re.compile(
    r"\b(?:how\s+(?:do|can|should|would|could)\s+(?:i|we)|how\s+to|"
    r"what\s+(?:do|can|should|would|could|will)\s+(?:i|we)|what\s+to|"
    r"where\s+(?:do|can|should|would|could)\s+(?:i|we)|"
    r"can\s+i|should\s+i|do\s+i)\s+([a-z']+)", re.I)
DETERMINER_BEFORE_DETAIL = frozenset(
    """the my his her their your our a an some both""".split())
DETERMINERS = DETERMINER_BEFORE_DETAIL
STOP_BEFORE_A_PART = frozenset("""
    for and of in on at with about to from or the a an my his her their your our some both
    """.split())
SENTENCE = re.compile(r"(?<=[.!?])\s+")
PRAISE_WORD = frozenset("""
    helpful useful handy helpful great brilliant brill perfect lovely nice good sound sorted works
    worked working spot on exactly right clearer clear helpful interesting amazing fab fabulous
    wonderful excellent super ace wicked grand neat tidy
""".split())


NOTHING_WORD = frozenset("""
    else anything something nothing everything different instead anyway anyhow otherwise
""".split())

SUBJECT_WORD = frozenset("""
    i im we us you he she they them theres thats it its one people
""".split())

FILLER_WORD = frozenset("""
    actually really honestly seriously literally basically obviously definitely absolutely
    certainly clearly surely probably perhaps maybe quite rather even only just still again
    though although anyway anyhow then ok okay right please sure well so yes yeah
    hmm hmmm hm mhm mm um umm uhm uh er erm ah ahh oh ohh eh
""".split())

A_QUALITY_WORD = frozenset("""
    new newer newest old older oldest young younger youngest
    cheap cheaper cheapest expensive pricey costly dear
    best better worst worse decent proper secondhand latest
    big bigger biggest small smaller smallest large larger huge tiny
    long longer longest short shorter shortest tall heavy light
""".split())

A_PLACE_IN_IT = frozenset("""
    end start beginning top bottom middle rest side front back corner last first
""".split())
A_JOINING_WORD = frozenset("""
    until till before after then when whenever while whilst during since once
    about if unless because than and or but so
""".split())
A_PLEA_FOR_TIPS = re.compile(
    r"^(?:and |so |ok |okay |well )?(?:(?:any|some|got any|got some|need some|need any|"
    r"want some|more|any more|another|a few|any other)\s+)?"
    r"(?:tips?|advice|pointers?|tricks?|hints?)"
    r"(?: (?:at all|then|please|too|now|really|anyway))*[.!?]*$", re.I)


NOT_IN_A_NAME = A_JOINING_WORD | frozenset("""
    am is are was were be been being do does did done have has had having should would could can
    will shall may might must not
""".split())


def _in_short(reply):
    reply = _without_a_lead(reply)
    parts = same_again.quoted.sentences(reply, SENTENCE)
    if not parts:
        return str(reply or "")
    if len(parts[0]) >= 60 or len(parts) == 1:
        return parts[0].strip()
    return (parts[0] + " " + parts[1]).strip()



def _same_as_the_last_answer(text, memory):
    last = mem.last_bot(memory) or ""
    if not last:
        return False
    if _flat(text) == _flat(last):
        return True
    named_now = set(PICKED.findall(text))
    return bool(named_now) and named_now == set(PICKED.findall(last))


PICKED = re.compile(r"\*([^*\n]{2,60})\*")


def _the_same_answer_in_other_words(text, memory):
    last = mem.last_bot(memory) or ""
    if not last:
        return False
    return difflib.SequenceMatcher(None, _flat(text), _flat(last)).ratio() >= 0.7


def _flat(text):
    return " ".join(WORD.findall(str(text or "").lower()))


A_SENTENCE_BREAK = re.compile(r"(?<=[.!?])\s+")
A_CLAUSE_FINE = re.compile(r"[,;:]\s+|\s+\u2014\s+")
A_CLAUSE_BREAK = re.compile(r";\s+|:\s+|\s+\u2014\s+|,\s+(?:and|plus|but|so|which|then|with)\s+")
A_OPENS_A_CLAUSE = re.compile(r"^(?:and|plus|but|so|which|then|with|also|also\s)\b", re.I)
A_SAYS_NOTHING = frozenset(("it", "this", "that", "they", "them", "one", "ones"))


A_SAYS_SOMETHING = re.compile(
    r"\b(?:is|are|was|were|be|been|has|have|had|does|did|do|can|could|will|would|should|must|"
    r"need|needs|cost|costs|keep|keeps|want|wants|get|gets|give|gives|use|uses|take|takes|book|"
    r"books|buy|buys|put|puts|try|tries|ask|asks|check|checks|avoid|avoids|work|works|help|"
    r"helps|last|lasts|make|makes|mean|means|come|comes|go|goes|say|says|pay|pays|save|saves|"
    r"hold|holds|fit|fits|wear|wears|eat|eats|drink|drinks|start|starts|set|sets|add|adds|mix|"
    r"stir|stirs|cook|cooks|freeze|freezes|leave|leaves|order|orders|ring|rings|call|calls|wait|"
    r"waits|run|runs|sit|sits|stand|stands|open|opens|close|closes|clean|cleans|wash|washes|"
    r"dry|dries|walk|walks|feed|feeds|soak|soaks|cover|covers|worth)\b", re.I)


def _says_something(clause):
    return bool(A_SAYS_SOMETHING.search(clause) or re.search(r"\d", clause))


def _the_part_in_the_answer(answer, detail):
    last = (detail.split() or [""])[-1].lower()
    if len(last) < 3:
        return ""
    words = WORD.findall(str(answer or "").lower())
    if len(words) < 5:
        return ""
    for splitter in (A_CLAUSE_BREAK, A_CLAUSE_FINE):
        for sentence in A_SENTENCE_BREAK.split(str(answer or "")):
            for clause in splitter.split(sentence):
                clause = clause.strip(" ,;:-\u2014")
                if not clause:
                    continue
                body = WORD.findall(clause.lower())
                if not any(_names_it(word, last) for word in body):
                    continue
                if len(body) < 4 or len(body) > 18:
                    continue
                if A_OPENS_A_CLAUSE.match(clause):
                    continue
                if body[0] in A_SAYS_NOTHING:
                    continue
                if not _says_something(clause):
                    continue
                clause = clause[0].upper() + clause[1:]
                if clause[-1] not in ".!?":
                    clause += "."
                return clause
    return ""


def _names_it(word, last):
    if word == last:
        return True
    if len(word) < 4 or len(last) < 4:
        return False
    return word.startswith(last) or last.startswith(word)


SAID_ABOVE = (
    "Everything about {detail} is in what I said above \u2014 there is no more than that.",
    "All there is on {detail} is in the answer above, and nothing beyond it.",
    "{detail} is covered by the answer above; I have nothing to add to it.",
)
NOTHING_SEPARATE = (
    "There is nothing separate on {detail} \u2014 what I said above is the whole of it.",
    "Nothing more on {detail} than what I said above: it all comes under the one answer.",
    "There is no separate answer for {detail}: what is above is the whole of it.",
)


ASKS_ABOUT_HOW_IT_TURNED_OUT = re.compile(
    r"\b(?:will|would|does|do|did|can|could|should|is|are|was|were|might)\s+"
    r"(?:it|that|this|they|them|those|these|i|we|you|he|she)\b", re.I)


def _a_part_named_in_the_line(text, memory, answer):
    raw = WORD.findall(str(text or "").lower())
    wanted = {word for word in keywords(text) if len(word) > 2 and word not in ASK_ONLY}
    already = _said_before_now(text, memory)
    for index in range(len(raw) - 1, -1, -1):
        word = raw[index]
        if word in already or word in PRAISE_WORD or word in NOTHING_WORD:
            continue
        if len(word) < 4 or not word.endswith("s"):
            continue
        stem = word[:-1]
        if stem not in wanted:
            continue
        if not _named_in(answer, word):
            continue
        words = [word]
        before = index - 1
        while (before >= 0 and len(words) < 3 and raw[before] not in DETERMINERS
               and raw[before] not in ASK_ONLY and raw[before] not in STOP_BEFORE_A_PART
               and raw[before] not in PRAISE_WORD and raw[before] not in NOT_IN_A_NAME
               and raw[before] not in A_QUALITY_WORD):
            words.insert(0, raw[before])
            before -= 1
        if any(word in SUBJECT_WORD for word in words):
            continue
        name = " ".join(words)
        if before >= 0 and raw[before] in DETERMINERS:
            return raw[before] + " " + name
        return name
    return ""


def _short_form_of_the_last(answer, memory):
    last = str(mem.last_bot(memory) or "").strip()
    mine = _flat(answer)
    if not last or not mine or mine == _flat(last):
        return ""
    if not _flat(last).startswith(mine):
        return ""
    return last


def _answer_said(plan, memory):
    mine = _flat(plan)
    if not mine:
        return 0
    count = 0
    for turn in reversed(memory.get("turns") or []):
        if not isinstance(turn, dict) or mine not in _flat(turn.get("bot")):
            break
        module = turn.get("module")
        if isinstance(module, str) and module and module != "answers":
            continue
        count += 1
    return count


BARE = set("the a an i me my mine we our you your it its is are was were be do does did can could "
           "should would will shall may might to for of and or but in on at with about from that "
           "this these those there here what how when which why who whom whose if then so not no "
           "have has had get got make made much many more most some any".split())


def _carries(text):
    return {word for word in WORD.findall(str(text or "").lower())
            if len(word) > 2 and word not in BARE}


def _the_sentence_asked(reply, text):
    sentences = [part for part in SENTENCE.split(str(reply or "")) if part.strip()]
    if len(sentences) < 2:
        return None
    wanted = _carries(text)
    best, best_score, best_length = None, 0, len(sentences[0])
    for sentence in sentences:
        score = len(wanted & _carries(sentence))
        if score and (score > best_score or (score == best_score and len(sentence) < best_length)):
            best, best_score, best_length = sentence, score, len(sentence)
    if best is None:
        return None
    joined = _JOINED_ON.match(best.strip())
    if joined:
        best = best.strip()[joined.end():]
        best = best[:1].upper() + best[1:]
    return best


def _the_sentence_naming(reply, text, memory=None):
    detail = _the_detail_named(text, memory)
    if not detail:
        return None
    sentences = [part.strip() for part in SENTENCE.split(str(reply or "")) if part.strip()]
    if len(sentences) < 2:
        return None
    word = detail.split()[-1]
    for sentence in sentences[1:]:
        if any(similar(word, other) for other in WORD.findall(sentence.lower())):
            return sentence
    return None


def _repeat_short(reply, text, memory=None):
    reply = _without_a_lead(reply)
    part = _the_sentence_asked(reply, text) if asked_kind(text) else None
    return part or _the_sentence_naming(reply, text, memory) or _in_short(reply)


NO_FIGURE = {
    "time": "I can't put a time on that one, sorry - ",
    "clock": "I can't put a time on that one, sorry - ",
    "heat": "I can't put a temperature on that one, sorry - ",
    "money": "I can't put a price on that one, sorry - ",
    "amount": "I can't put a figure on that one, sorry - ",
    "pressure": "I can't put a pressure on that one, sorry - ",
    "distance": "I can't put a distance on that one, sorry - ",
}
STEP_END = re.compile(r";\s+|,\s+(?:and|then|but)\s+|\.\s+|\.$")
SPOKEN = re.compile(r"\b(?:fortnight\w*|overnight|all day|an hour|half an hour|a day|a week"
                    r"|a month|a year|a minute|a couple of (?:minutes|hours|days|weeks))\b", re.I)
TIMEISH = re.compile(r"\b\d+\s*(?:seconds?|secs?|minutes?|mins?|hours?|hrs?|days?|weeks?"
                     r"|months?|years?)\b", re.I)


NO_STEP = "what I said there is the steps, not how long they take."


_JOINED_ON = re.compile(r"^(?:and|then|so|but|also|now|next)(?:\s*,\s*|\s+)", re.I)


def _first_step(reply):
    opening = SENTENCE.split(str(reply or "").strip())[0].strip()
    joined = _JOINED_ON.match(opening)
    if joined:
        opening = opening[joined.end():]
        opening = opening[:1].upper() + opening[1:]
    if not opening:
        return ""
    if len(opening.split()) <= 16:
        return opening if opening[-1:] in ".!?" else opening + "."
    first = next((one.strip(" ,;:") for one in STEP_END.split(opening) if one.strip(" ,;:")), "")
    for piece in (first, first.split(": ")[-1]):
        if 4 <= len(piece.split()) <= 20:
            return piece if piece[-1:] in ".!?" else piece + "."
    return ""


def _figure_missing(reply, text):
    kind = asked_kind(text)
    if kind not in NO_FIGURE:
        return None
    if _answers_the_figure(text, reply):
        return None
    if kind in ("time", "clock") and (SPOKEN.search(str(reply or ""))
                                       or TIMEISH.search(str(reply or ""))):
        return None
    step = _first_step(reply)
    if not step:
        return NO_FIGURE[kind] + NO_STEP
    return NO_FIGURE[kind] + step[:1].lower() + step[1:]


def _figures_changed(reply, said):
    mine = set(NUMBER_IN_TEXT.findall(str(reply or "")))
    theirs = set(NUMBER_IN_TEXT.findall(str(said or "")))
    return bool(mine and theirs and mine - theirs)


def _same_answer(reply, said):
    mine = _flat(reply)
    theirs = _flat(said)
    if not mine or not theirs:
        return False
    if _opening(mine) in theirs:
        return not _figures_changed(reply, said)
    for sentence in SENTENCE.split(str(reply or "")):
        part = _flat(sentence)
        if len(part) > 20 and part in theirs:
            return not _figures_changed(reply, said)
    for clause in str(said or "").split(":"):
        cut = _flat(clause)
        if len(cut.split()) >= 6 and cut in mine:
            return True
    return False


def _asks_of_another_subject(text, understood):
    if not isinstance(understood, dict) or not str(text or "").strip():
        return False
    alone = understand(text, {}) or {}
    own = alone.get("topic") or ""
    held = (understood.get("leans_on") or {}).get("topic") or ""
    return bool(own) and bool(held) and own != held
def _asked_again(text, reply, memory):
    wanted = _flat(text)
    mine = _opening(_flat(reply))
    if not wanted or not mine:
        return 0
    count = 0
    for turn in reversed(memory.get("turns") or []):
        if not isinstance(turn, dict):
            break
        if _flat(turn.get("user")) != wanted:
            break
        if not _same_answer(reply, turn.get("bot")):
            break
        count += 1
    return count

def _ask_verb(text):
    match = ASK_VERB.search(str(text or ""))
    return str(match.group(1) or "").lower() if match else ""


def _the_outcome_owed(item, text):
    which = the_outcome_asked(text)
    if not which or item is None:
        return None
    for shape, sentence in getattr(item, "outcomes", ()) or ():
        if shape == which and str(sentence or "").strip():
            return sentence
    return None


def _said_before_now(text, memory):
    seen = set()
    for turn in (memory or {}).get("turns") or []:
        if isinstance(turn, dict):
            seen.update(WORD.findall(str(turn.get("user") or "").lower()))
    return seen


A_CORRECTION_WORD = frozenset("""
    instead actually only just make again now please sorry wait really exactly still anyway
""".split())


def _a_fact_about_the_person(memory):
    understood = memory.get("understood") if isinstance(memory, dict) else None
    if not isinstance(understood, dict):
        return False
    return (understood.get("kind") == "statement" and not understood.get("asks")
            and bool(understood.get("first_person")))


def _the_detail_named(text, memory=None, with_quality=False):
    named = _the_part_named(text, memory, with_quality)
    if named and _a_restatement_of_the_answer(memory) and _all_of_it_in_the_answer(named, memory):
        return ""
    return named


def _a_restatement_of_the_answer(memory):
    understood = memory.get("understood") if isinstance(memory, dict) else None
    if not isinstance(understood, dict):
        return False
    return understood.get("kind") == "statement" and not understood.get("asks")


def _all_of_it_in_the_answer(named, memory):
    said = WORD.findall(str(mem.last_bot(memory if isinstance(memory, dict) else {}) or "").lower())
    words = [word for word in WORD.findall(str(named or "").lower())
             if len(word) > 2 and word not in A_JOINING_WORD]
    return bool(words) and all(word in said or stem(word) in said for word in words)


CLAUSE_OPENER = frozenset("when whenever if once after before while until as".split())
CLAUSE_SUBJECT = frozenset("i you he she it we they u".split())
NUMBER_OR_OWNER = frozenset("the my your his her their our this that a an".split())


def _the_clause_s_verb(raw, index):
    if index >= 2 and raw[index - 2] in CLAUSE_OPENER and raw[index - 1] in CLAUSE_SUBJECT:
        return True
    return bool(index >= 3 and raw[index - 3] in CLAUSE_OPENER
                and raw[index - 2] in NUMBER_OR_OWNER)


def _the_part_named(text, memory=None, with_quality=False):
    if went_back.a_bare_return(text, memory if isinstance(memory, dict) else None):
        return ""
    raw = WORD.findall(str(text or "").lower())
    if raw and all(word in ONLY_THE_ASK for word in raw):
        return ""
    wanted = {word for word in keywords(text)
              if len(word) > 2 and word not in ASK_ONLY and word not in NOT_A_DETAIL
              and word not in A_CORRECTION_WORD}
    if not wanted:
        return ""
    verb = _ask_verb(text)
    already = _said_before_now(text, memory)
    for index in range(len(raw) - 1, -1, -1):
        word = raw[index]
        if word in A_JOINING_WORD:
            continue
        if word not in wanted and stem(word) not in wanted:
            continue
        if (word in PRAISE_WORD or word in NOTHING_WORD or word in FILLER_WORD
                or (word in A_QUALITY_WORD and not with_quality)):
            continue
        if verb and (word == verb or word.startswith(verb) or verb.startswith(word)):
            continue
        if raw[index - 1] not in DETERMINER_BEFORE_DETAIL and (
                word in kinds.VERBISH
                or word in kinds.VERB_THIRD
                or _the_clause_s_verb(raw, index)
                or (len(word) > 4 and word.endswith(("ed", "ing")))):
            continue
        if word in already:
            continue
        if index + 1 < len(raw) and raw[index + 1] == "to":
            continue
        behind = raw[index - 1] if index else ""
        if (word in A_PLACE_IN_IT and index + 2 < len(raw) and raw[index + 1] == "of"
                and raw[index + 2] in BACK_POINTS):
            return ""
        if behind in ("the", "my", "his", "her", "their", "your", "a", "this", "that"):
            return behind + " " + word
        whole = _named_whole(raw, index)
        if whole:
            return whole
        if word not in wanted and not _named_in(mem.last_bot(memory or {}), word):
            return ""
        return word
    return ""


def _only_a_quality_name(text, memory=None):
    named = _the_detail_named(text, memory, with_quality=True)
    if not named:
        return False
    words = [word for word in named.split() if word not in DETERMINERS]
    return bool(words) and all(word in A_QUALITY_WORD for word in words)


MODIFIER_WORDS = 2


def _named_whole(raw, index):
    if index + 1 < len(raw) and raw[index + 1] in BACK_POINTS:
        return ""
    head = raw[index]
    if (head in kinds.VERBISH or head in NEGATORS
            or (len(head) > 4 and head.endswith(("ed", "ing", "s")))):
        return ""
    if any(word in NEGATORS for word in raw[max(index - MODIFIER_WORDS - 1, 0):index]):
        return ""
    for back in range(index - 1, max(index - 1 - MODIFIER_WORDS, -1), -1):
        word = raw[back]
        before = raw[back - 1] if back else ""
        if before in DETERMINER_BEFORE_DETAIL:
            return " ".join(raw[back - 1:index + 1])
        if (word in STOP_BEFORE_A_PART or word in BACK_POINTS or word in NOT_A_DETAIL
                or word in FILLER_WORD or word in NOTHING_WORD or word in PRAISE_WORD
                or word in NOT_IN_A_NAME or word in A_QUALITY_WORD):
            return ""
        if word in kinds.VERBISH or (len(word) > 4 and word.endswith(("ed", "ing"))):
            return ""
    return ""


FIRST_PERSON = frozenset("""i im ive id ill i'm i've i'd""".split())


def _their_own_state(text):
    text = str(text or "")
    if ASKS_ABOUT_HOW_IT_TURNED_OUT.search(text) or _ask_verb(text):
        return False
    raw = WORD.findall(text.lower())
    return bool(raw) and raw[0] in FIRST_PERSON


def _named_in(part, detail):
    last = (detail.split() or [""])[-1]
    if len(last) < 3:
        return False
    for word in WORD.findall(str(part or "").lower()):
        if word == last:
            return True
        if len(word) >= 4 and len(last) >= 4 and (
                word.startswith(last[:4]) or last.startswith(word[:4])):
            return True
    return False


def similar(word, other):
    if word == other:
        return True
    if len(word) < 4 or len(other) < 4:
        return False
    return word.startswith(other) or other.startswith(word)


def _entry_words(memory):
    kept = []
    answer = (memory or {}).get("entry_answer")
    if isinstance(answer, dict):
        kept.append(answer)
    others = (memory or {}).get("entry_answers")
    if isinstance(others, list):
        kept.extend(record for record in others if isinstance(record, dict))
    words = set()
    for record in kept:
        for key in record.get("keys") or ():
            words.update(WORD.findall(str(key).lower()))
    return words


def _what_they_typed(text, memory):
    if not isinstance(memory, dict) or not memory.get("joined_read"):
        return text
    read = memory.get("understood") if isinstance(memory.get("understood"), dict) else {}
    topic = str(((read.get("leans_on") or {}).get("text")) or "").strip()
    line = str(text or "").strip()
    if topic and line.lower().startswith(topic.lower()):
        return line[len(topic):].strip()
    return text


def _covered(text, reply, memory=None, understood=None):
    said = set(WORD.findall(str(reply or "").lower()))
    read = understood
    if not isinstance(read, dict):
        read = (memory or {}).get("understood") if isinstance(memory, dict) else None
    typed = _what_they_typed(text, memory)
    detail = "" if _asks_of_another_subject(typed, read) else _the_detail_named(typed, memory)
    words = WORD.findall(str(text or "").lower())
    if any(word in BACK_POINTS for word in words):
        return True
    verb = _ask_verb(text)
    entry = _entry_words(memory)
    for word in keywords(text):
        if len(word) < 3 or word in ASK_ONLY or word in detail.split():
            continue
        if verb and (word == verb or word.startswith(verb) or verb.startswith(word)):
            continue
        if word in ASKING_VERBS:
            continue
        if any(similar(word, other) for other in said):
            continue
        if any(similar(word, other) for other in entry):
            continue
        return False
    return True


def _a_question_about_another_thing(text, reply, understood, memory, own=None, item=None):
    if own:
        return False
    if not isinstance(understood, dict) or understood.get("kind") != "question":
        return False
    if not isinstance(reply, str) or not reply.strip():
        return False
    typed = _what_they_typed(text, memory)
    if not _asks_of_another_subject(typed, understood):
        return False
    thing = _the_detail_named(typed, memory)
    if len(thing.split()) != 2:
        return False
    word = thing.split()[-1]
    if any(similar(word, other) for other in WORD.findall(reply.lower())):
        return False
    held = set(_entry_words(memory))
    if item is not None:
        held |= _key_words(item)
    if any(similar(word, other) for other in held):
        return False
    named = [one for one in keywords(typed) if len(one) > 2 and one not in ASK_ONLY]
    if any(similar(one, other) for one in named for other in held):
        return False
    return True


A_SMALL_OPENER = frozenset("""
    the a an this that these those they it there he she we you and but if so or then both most
    some many all any each other another not no
    # ...and the verb an answer opens with when it tells somebody what to do. "Same for
    # floorboards: Sand a wooden floor back to bare wood" and "The same goes for the bathroom:
    # Use a mid-sheen" both read as two sentences with the capital on, which is the fault
    # STYLE.md names; the verb is a common word, so it loses it.
    add allow apply ask avoid bake baste beat begin boil bring brush buy catch change check
    choose clean clear close cook cool cover cut defrost do drain drink dry empty fill find
    finish fit fix freeze get give go hang heat hold keep lay leave let lift line look make
    measure mix open paint peel pick place plug pour prepare press pull put rinse roll rub
    run sand scrape seal set shake shut simmer sit soak sort spray spread stand start stay
    steam stir stop store switch take talk tell test thaw think throw tidy tip try turn use
    wait wash watch wear wipe work wrap
""".split())


def _small_letter(body):
    first, _, rest = body.partition(" ")
    bare = first.rstrip(string.punctuation)
    if bare.lower() in A_SMALL_OPENER:
        return first[:1].lower() + body[1:]
    if bare[:1].isupper() and re.search(r"(?<![A-Za-z])%s(?![A-Za-z])" % re.escape(bare.lower()),
                                       rest):
        return first[:1].lower() + body[1:]
    return body


def _times_the_answer_was_said(reply, memory):
    times = 0
    for turn in reversed((memory.get("turns") or [])[-4:]):
        if not isinstance(turn, dict) or not _same_answer(reply, turn.get("bot")):
            break
        times += 1
    return times


def _with_detail(detail, part, times, text="", memory=None, card=""):
    body = str(part or "").strip()
    if not detail or not body:
        return ""
    underneath = same_again.the_same_thing_underneath(text, body, times, memory)
    if underneath:
        return underneath
    if detail.split()[-1] in NOT_A_DETAIL:
        return same_again.AGAIN[min(times, len(same_again.AGAIN)) - 1].format(reply=body)
    named = same_again.the_name_the_answer_says(body, detail, card=card)
    if not named and _a_yes_no_ask(memory):
        return same_again.AGAIN[min(times, len(same_again.AGAIN)) - 1].format(reply=body)
    pool = DETAIL_AGAIN if named else SAME_ADVICE
    return pool[min(times, len(pool)) - 1].format(detail=named or detail,
                                                  reply=_small_letter(body))


def _a_yes_no_ask(memory):
    understood = memory.get("understood") if isinstance(memory, dict) else None
    if not isinstance(understood, dict):
        return False
    return "yesno" in (understood.get("asks") or ())




MORE_ASK = frozenset("""
    else more other others another anything something nothing everything different instead
    anyway anyhow otherwise
""".split())


def _asks_for_more(text):
    return any(word in MORE_ASK for word in keywords(text))


def _nothing_more_said_again(reply, text, memory):
    if not _asks_for_more(text):
        return ""
    times = 0
    for turn in reversed((memory.get("turns") or [])[-4:]):
        if not isinstance(turn, dict) or not _same_answer(reply, turn.get("bot")):
            break
        times += 1
    if not times:
        return ""
    short = _in_short(reply) or reply
    underneath = same_again.the_same_thing_underneath(text, short, times, memory)
    if underneath:
        return underneath
    return NOTHING_MORE[min(times, len(NOTHING_MORE)) - 1].format(reply=short)


def _the_detail_said_again(reply, text, memory):
    detail = _the_detail_named(text, memory)
    if not detail:
        picked = _the_sentence_asked(reply, text) if asked_kind(text) else None
        if isinstance(picked, str) and picked.strip() and flat(picked) != flat(reply):
            times = _times_the_answer_was_said(reply, memory)
            if times:
                underneath = same_again.the_same_thing_underneath(text, picked, times, memory)
                if underneath:
                    return underneath
                return same_again.AGAIN[min(times, len(same_again.AGAIN)) - 1].format(
                    reply=picked)
        return _nothing_more_said_again(reply, text, memory)
    times = _times_the_answer_was_said(reply, memory)
    if not times:
        return None
    short = narrow(reply, text) or ""
    if not isinstance(short, str) or not short.strip() or flat(short) == flat(reply):
        short = _repeat_short(reply, text, memory) or reply
    return _with_detail(detail, short, times, text, memory, card=reply)


def _detail_lead_in(text, part, memory):
    detail = _the_detail_named(text, memory)
    if not detail or not isinstance(part, str) or not part.strip():
        return ""
    said = flat(part)
    times = 0
    for turn in reversed((memory.get("turns") or [])[-4:]):
        if not isinstance(turn, dict):
            break
        if said and said in flat(turn.get("bot")):
            times += 1
            continue
        break
    if not times:
        return ""
    return _with_detail(detail, part, times, text, memory, card=_the_answer_on_screen(memory))


def _the_answer_on_screen(memory):
    turns = memory.get("turns") if isinstance(memory, dict) else None
    for turn in reversed(list(turns or ())[-2:]):
        if isinstance(turn, dict) and isinstance(turn.get("bot"), str) and turn["bot"].strip():
            return turn["bot"]
    return ""


def _the_part_said_again(part, text, understood, memory):
    if isinstance(part, str) and part.strip() and a_detail_of_the_thing_we_hold(understood, memory):
        lead = _detail_lead_in(text, part, memory)
        if lead:
            return lead
    return part


def _already_said(reply, memory, keep=3):
    mine = " ".join(str(reply or "").lower().split())
    if not mine:
        return False
    for turn in (memory.get("turns") or [])[-keep:]:
        if not isinstance(turn, dict):
            continue
        bot = " ".join(str(turn.get("bot") or "").lower().split())
        if bot and (bot == mine or bot.endswith(mine) or _the_same_sentences(bot, mine)):
            return True
    return False


def _the_same_sentences(said, mine):
    if not said or not mine or said == mine:
        return False
    parts = [part.lower() for part in re.split(r"(?<=[.!?])\s+", said) if part]
    others = [part.lower() for part in re.split(r"(?<=[.!?])\s+", mine) if part]
    return len(parts) > 1 and len(parts) == len(others) and sorted(parts) == sorted(others)


WHO_IS_THE_BOT = re.compile(
    r"^\s*(?:so\s+|and\s+|ok\s+|okay\s+|but\s+|sorry\s+)?"
    r"(?:who|what|where)\s+(?:are|r)\s+(?:you|u)\s*[?.!]*$"
    r"|^\s*(?:what\s+can\s+you\s+do|what\s+do\s+you\s+do|who\s+made\s+you"
    r"|tell\s+me\s+about\s+yourself)\s*[?.!]*$",
    re.IGNORECASE)


def _asks_who_the_bot_is(understood, text):
    text = text or ""
    if ANSWERING_A_QUOTED_ASK.search(text) and not WHO_IS_THE_BOT.search(text):
        return False
    if isinstance(understood, dict) and understood.get("about_bot"):
        return True
    return bool(WHO_IS_THE_BOT.search(text))


LENGTH_WORDS = frozenset((
    "long", "soon", "months", "month", "years", "year", "weeks", "week",
    "hours", "hour", "days", "day", "minutes", "minute"))

_A_LENGTH = re.compile(
    r"(?<![\u00a3$\u20ac\d.,])\b(?:\d{1,4}|a|an|one|two|three|four|five|six|seven|eight|nine|ten"
    r"|eleven|twelve|fifteen|twenty|thirty|forty|fifty|sixty)\s+"
    r"(?:to\s+\w+\s+)?(?:seconds?|minutes?|hours?|days?|weeks?|months?|years?)\b", re.I)

_A_DURATION = re.compile(r"\b(?:minutes?|mins?|hours?|hrs?)\b", re.I)


_DEFINES_THE_UNIT = re.compile(
    r"^\W*(?:a|an|one|the)\s+(?:second|minute|hour|day|week|month|year|decade|century)s?\b"
    r"\W+(?:is|are|has|have|takes|lasts|means)\b", re.I)


def _answers_a_length(item, reply):
    reply = str(reply or "")
    if not reply or any(mark in reply for mark in ("\u00a3", "$", "\u20ac")):
        return False
    if _DEFINES_THE_UNIT.match(reply):
        return False
    if not _A_LENGTH.search(reply):
        return False
    for part in getattr(item, "key", ()) or ():
        for phrase in part:
            if set(str(phrase).lower().split()) & LENGTH_WORDS:
                return True
    return False


def _written_ask_with_an_answer(text, memory):
    written = mem.written_out(text, memory)
    if not written:
        return None
    try:
        asked = understand(written, memory)
        found, found_reply = _offer(lambda reject: find(asked, reject=reject), memory, asked)
        if not _answers_a_length(found, found_reply):
            return None
    except Exception:
        return None
    return written


def _the_article(subject, memory):
    head = (subject.split() or [""])[0].strip(".,!?;:'\"").lower()
    if not head:
        return "the "
    user = memory.get("user") if isinstance(memory, dict) else None
    if not isinstance(user, dict):
        return "the "
    names = set()
    for key in ("name", "city"):
        value = user.get(key)
        if isinstance(value, str) and value.strip():
            names.update(word.lower() for word in value.split())
    for key in ("places", "people", "pets"):
        found = user.get(key)
        if isinstance(found, (list, tuple)):
            for value in found:
                if isinstance(value, str) and value.strip():
                    names.update(word.lower() for word in value.split())
    return "the " if head not in names else ""


def _with_subject(text, memory, about=None):
    written = _written_ask_with_an_answer(text, memory)
    if written:
        return written
    words = text.split()
    if len(words) > 14:
        return text
    if ABOUT_YOU.search(text):
        return text
    subject = mem.subject(memory) if about is None else about
    if not subject:
        return text
    wanted = [w.strip(".,!?;:").lower() for w in subject.split()]
    said = [w.strip(".,!?;:").lower() for w in words]
    if any(word in said for word in wanted):
        return text
    for i, word in enumerate(said):
        if word in REFERRING:
            words[i] = _the_article(subject, memory) + subject
            return " ".join(words)
    return text


PROPERTY = re.compile(r"\b(?:temperature|oven|gas mark|degrees|how long|how much|how many|"
                      r"minutes?|hours?|cost|price|expensive|when|how early|how hot)\b",
                      re.IGNORECASE)


def _about_subject(text, memory, about=None):
    asks_which_one = mem.KIND_ASK.search(text)
    if len(text.split()) > 14 or not (PROPERTY.search(text) or asks_which_one):
        return text
    subject = mem.subject(memory) if about is None else about
    if not subject or not mem.current(memory):
        return text
    wanted = [word.strip(".,!?;:").lower() for word in subject.split()]
    if any(word in text.lower() for word in wanted):
        return text
    return text.rstrip("?.! ") + " for " + _the_article(subject, memory) + subject + "?"


SOMETHING_FOR = re.compile(
    r"\b(?:something|anything|somef?in\w*|anyf\w*|summat|sommat|stuff)\s+"
    r"(?:for|to\s+(?:take|help|ease|soothe|settle|stop|calm|clear|put\s+on|rub\s+on|"
    r"drink|eat|use))\b\s*(.+)", re.I)
SOMETHING_FOR_PEOPLE = frozenset("""
mum mom dad mother father husband wife partner boyfriend girlfriend son daughter kid kids child
children baby brother sister friend friends gran granny grandma grandad grandpa nan aunt uncle
cousin nephew niece boss colleague neighbour neighbor her him them they us we people someone
anybody somebody everyone my his their our
""".split())
SOMETHING_FOR_FILLER = frozenset("""
do doing use using later now anything something nothing else other general
""".split())
SOMETHING_FOR_TAIL = frozenset("""
please pls fast quickly quick now asap soon
""".split())
_OCCASION_WORDS = frozenset("""
birthday birthdays bday anniversary anniversaries wedding weddings christening retirement
graduation leaving housewarming
""".split())
SOMETHING_FOR_STATE = frozenset("""
breastfeeding breast-feeding breast feeding trimester expecting
""".split())


SOMETHING_FOR_GIVEN_TO = re.compile(
    r"\b(?:give|gives|giving|gave|given|feed|feeds|feeding|dose|dosing|treat|treating|use|using"
    r"|used)\s+(?:it to\s+|them\s+|him\s+|her\s+)?"
    r"(?:my|the|your|his|her|their|our|this|that|a|an)?\s*"
    r"(baby|babies|newborn|toddler|child|children|kid|kids|son|daughter|boy|girl|child|"
    r"teenager|teen|patient|mum|mom|dad|father|mother|partner|husband|wife|friend)\b")


def _keyed_on_the_person(item, who):
    if not who:
        return False
    keys = _key_words(item)
    person = who.rstrip("s")
    if person in keys:
        return True
    child = {"baby", "toddler", "child", "kid", "son", "daughter", "newborn", "boy", "girl"}
    return bool(keys & child) and (person in child or person in ("teenager", "teen"))


def _something_for(text):
    match = SOMETHING_FOR.search(_flat(text))
    if not match:
        return ""
    rest = [word for word in re.split(r"\s+", match.group(1).strip(" ?.!")) if word]
    while rest and rest[-1] in SOMETHING_FOR_TAIL:
        rest = rest[:-1]
    while rest and rest[0] in ("my", "your", "his", "her", "their", "our"):
        rest = rest[1:]
    if not 1 <= len(rest) <= 6:
        return ""
    if all(word in _OCCASION_WORDS or re.fullmatch(r"\d{1,3}(?:st|nd|rd|th)?", word)
           for word in rest):
        return ""
    if {word for word in rest} & SOMETHING_FOR_PEOPLE:
        return ""
    if [word for word in rest if "pregnan" in word or word in SOMETHING_FOR_STATE]:
        return ""
    if not [word for word in rest if word not in SOMETHING_FOR_FILLER]:
        return ""
    return " ".join(rest)


PLAN_RECALL = re.compile(r"\bwhat (?:was|were|am|are) (?:i|we) (?:planning|up to)\b|"
                         r"\bwhat did i say i (?:was|am) (?:planning|up to)\b|"
                         r"\bwhere (?:are|were|was|am) (?:we|i) (?:going|off|headed|heading|away)\b|"
                         r"\bwhen (?:are|were|was|am) (?:we|i) (?:off|going|away|moving|flying|travelling)\b|"
                         r"\b(?:which|what) (?:month|day|week|date) (?:are|am|is) (?:we|i)\b|"
                         r"\b(?:which|what) (?:month|day|week|date) (?:is|was) that\b",
                         re.IGNORECASE)


def _keeps_a_plan(memory):
    known = (memory or {}).get("user") or {}
    return bool(known.get("plan") or known.get("plans"))


RECALL = re.compile(r"\bremind me (?:what|when|where|which|who|how much|how many|that|again)\b|"
                    r"\bdo you remember\b|"
                    r"\bwhat did (?:i|you|we) (?:call|name|say|tell|mention|order|ask)\b|"
                    r"\bwhat (?:do|did) (?:i|you|we) (?:call|name)\b|"
                    r"\bwhat did (?:i|you|we) order\b|"
                    r"\bwhat (?:was|were) (?:i|we) (?:saying|talking about)\b|"
                    r"\bwhat have i (?:told|said|mentioned)(?: you)?(?: so far| again)?\b|"
                    r"\bwhat (?:do|would) you know about me\b|"
                    r"\bhow (?:did|do) (?:we|you and i) (?:start|begin|open)\b|"
                    r"\bhow did (?:this|it|the (?:chat|conversation|talk)) (?:start|begin|open)\b",
                    re.IGNORECASE)


WHEN_AM_I = re.compile(
    r"\bwhen\s+(?:(?:am|are|was|were)\s+(?:i|we)\b|"
    r"(?:do|does|did|will)\s+(?:i|we)\s+(?:go|goes|going|leave|leaves|leaving|fly|head off|"
    r"set off|get back|be back)\b)", re.IGNORECASE)


ASKS_MEMORY = re.compile(r"\b(?:what|where|who|when|which|how old|how much|how many)\s+"
                         r"(?:am|was|were|is)\s+(?:i|we)\b|"
                         r"\bwhere (?:do|did|does) (?:i|we) (?:live|work|come from|belong)\b|"
                         r"\bwhat (?:do|did) you know about (?:me|us|my)\b|"
                         r"\bwhat(?:'s| is| was) (?:on|coming up)\b", re.IGNORECASE)


def _with_subject_tail(text, memory, understood=None):
    tails = _subject_tails(text, memory, understood)
    return tails[0] if tails else ""


def _subject_tails(text, memory, understood=None):
    subject = mem.subject(memory)
    if not isinstance(understood, dict):
        understood = memory.get("understood")
    if not isinstance(understood, dict):
        understood = {}
    if not subject or len(text.split()) > 10 or len(subject.split()) > 4:
        return []
    if understood.get("kind") == "statement" or not understood.get("asks"):
        return []
    if understood.get("about_bot") or ABOUT_YOU.search(text):
        return []
    if re.match(r"\s*(?:what|which|how|who|when|where|why)\b", subject, re.IGNORECASE):
        return []
    if RECALL.search(text) or ASKS_MEMORY.search(text):
        return []
    said = {word.strip(".,!?;:").lower() for word in text.split()}
    if said & {word.lower() for word in subject.split()}:
        return []
    words = subject.split()
    if len(words) == 1:
        return [text.rstrip("?.,! ") + " " + words[0]]
    tails = []
    for start in range(0, max(len(words) - 1, 0)):
        tail = " ".join(words[start:])
        if len(tail.split()) < 2:
            break
        tails.append(text.rstrip("?.,! ") + " " + tail)
    return tails

CHOOSING = re.compile(r"(?:what|which|where)\s+(?:should|could|can|would|do|shall)\s+(?:i|we)\s+"
                      r"(?:[a-z]+\s+){0,2}?(?P<verb>see|visit|watch|play|do|eat|drink|try|wear|"
                      r"take|bring|pack|get|buy|cook|make|give|order|book)\s*"
                      r"(?:her|him|them|there)?\s*\??$", re.I)
CHOOSING_PRONOUN = re.compile(r"\s+(?:her|him|them|there)\s*\??$", re.I)
PREPOSITION_OF = {}
for _prep, _verbs in (("in", "see visit watch play do eat drink try"),
                      ("to", "wear take bring pack"),
                      ("for", "get buy cook make give order book")):
    for _verb in _verbs.split():
        PREPOSITION_OF[_verb] = _prep
HOLDING_A_NUMBER = re.compile(r"^\d+(?:st|nd|rd|th)?$")
WHEN_WORDS = frozenset("""january february march april may june july august september october
november december jan feb mar apr jun jul aug sep sept oct nov dec monday tuesday wednesday
thursday friday saturday sunday next this last tonight today tomorrow weekend week month year
morning afternoon evening""".split())


def _bare_subject(subject):
    words = [word for word in (subject or "").split()
             if word.lower() not in WHEN_WORDS and not HOLDING_A_NUMBER.match(word)]
    return " ".join(words) or (subject or "")


MODAL = re.compile(r"\b(?:should|could|can|would|shall|do)\b", re.I)
MODALS = ("should", "can", "could")
MONTH = re.compile(r"\b(january|february|march|april|may|june|july|august|september|october|"
                   r"november|december)\b", re.I)
TIME_WORD = re.compile(r"^(?:january|february|march|april|may|june|july|august|september|october|"
                       r"november|december|jan|feb|mar|apr|jun|jul|aug|sep|sept|oct|nov|dec|"
                       r"spring|summer|autumn|fall|winter|"
                       r"monday|tuesday|wednesday|thursday|friday|saturday|sunday|"
                       r"today|tonight|tomorrow|yesterday|week|weekend|month|year|"
                       r"(?:next|this|last) (?:week|weekend|month|year|christmas|summer|winter|"
                       r"spring|autumn|fall))$", re.I)


def _the_month(text):
    match = MONTH.search(text or "")
    return match.group(1).lower() if match else ""


TRIP_TOPICS = ("geography-and-travel", "travel", "holidays-and-trips")


def _a_trip(memory):
    lines = [((mem.current(memory) or {}).get("text") or "")]
    recent = mem.last_user(memory, 5)
    lines.extend(recent if isinstance(recent, (list, tuple)) else [recent])
    for text in lines:
        if not text or not isinstance(text, str):
            continue
        if any(topic in TRIP_TOPICS for topic in understand(text, memory).get("topics") or ()):
            return True
    return False


FINITE = frozenset("""is are was were am be been being do does did dont doesnt didnt wont cant
couldnt shouldnt wouldnt isnt arent wasnt aint not never always keep keeps kept will would
should can could may might must have has had""".split())


def _a_clause(subject):
    return any(word.strip(string.punctuation).lower() in FINITE for word in str(subject or "").split())


def _choosing(text, memory):
    match = CHOOSING.search(text.strip())
    if not match:
        return None
    subject = _bare_subject(mem.subject(memory) or "")
    if not subject:
        return None
    if TIME_WORD.match(subject.strip()):
        return None
    a_clause = _a_clause(subject)
    prep = PREPOSITION_OF[match.group("verb").lower()]
    shapes = [prep + " {s}"]
    if prep == "to":
        shapes.append("to a {s}")
    recent_user = mem.last_user(memory, 3)
    recent_user = " ".join(recent_user) if isinstance(recent_user, list) else str(recent_user or "")
    month = _the_month(text) or _the_month(mem.topic_text(memory) or "") or _the_month(recent_user)
    if month and _a_trip(memory):
        shapes = [shape + " in " + month for shape in shapes] + shapes
    stem = CHOOSING_PRONOUN.sub("", text.strip()).rstrip("?").strip()
    declined = set()
    said = None
    for modal in MODALS:
        asked = MODAL.sub(modal, stem)
        for fuller in (asked + " " + shape.format(s=subject) for shape in shapes):
            reading = understand(fuller, memory)
            item = find(reading)
            if item is None or item.id in declined:
                continue
            if not (_is_about(item, subject) or (month and _a_trip(memory) and _is_about(item, month))):
                continue
            if a_clause and not about_the_topic(item, reading):
                continue
            reply = _payload(item, memory, reading)
            if not reply.strip():
                declined.add(item.id)
                continue
            if _said_before(reply, memory):
                part = narrow(reply, text)
                if (isinstance(part, str) and part.strip() and flat(part) != flat(reply)
                        and not _said_before(part, memory)):
                    return reading, item, part
                if said is None:
                    said = (reading, item, reply)
                continue
            return reading, item, reply
    if said is not None and _asked_again(text, said[2], memory):
        reading, item, reply = said
        if _asks_only_the_length(text):
            honest = _figure_missing(reply, text)
            if honest:
                return reading, item, honest
        return reading, item, AGAIN[0].format(reply=_in_short(reply))
    return None


def _only_a_size_of(item, text):
    words = _key_words(item)
    for word in mem.topics.keywords(text):
        if mem.topics.AMOUNT.search(word) or word in words:
            continue
        return False
    return True


QUALIFIER_OPEN = re.compile(r"^(?:something|anything|nothing|everything)\b")
QUALIFIER_MAX_WORDS = 9


def _choice_words(text, memory):
    line = " ".join(str(text or "").split()).lower()
    earlier = [one for one in mem.context(memory, 3)
               if " ".join(str(one).split()).lower() != line]
    topic = earlier[-1] if earlier else ""
    if not topic:
        return None, []
    found = []
    item = find(understand(topic, memory))
    for part in getattr(item, "key", ()) or ():
        options = (part,) if isinstance(part, str) else part
        for option in options:
            if isinstance(option, str):
                for word in option.split()[:1]:
                    if word.lower() not in found:
                        found.append(word.lower())
        break
    domain = item.domain if item is not None else None
    return domain, [word for word in found if len(word) > 2]


def _qualifier_rewrites(text, memory):
    clean = " ".join(text.split())
    if len(clean.split()) > QUALIFIER_MAX_WORDS or not QUALIFIER_OPEN.match(clean.lower()):
        return []
    if not mem.current(memory):
        return []
    domain, words = _choice_words(text, memory)
    said = {word.strip(".,!?;:").lower() for word in clean.split()}
    rewrites = []
    for word in words:
        if word not in said:
            rewrites.append((clean.rstrip("?.! ") + " " + word, word, domain))
    return rewrites


REFUSE_OPEN = re.compile(r"^(?:nothing|no|not)\b(?:\s+(?:a|an|too|very|really))*\s+([a-z']+)", re.I)
REFUSE_CHOICE = re.compile(
    r"^(?:anything|something|everything)\s+(?:but|except|apart from|other than|besides)\s+"
    r"(?:not\s+)?(?:a\s+|an\s+|the\s+|any\s+)?([a-z']+)", re.I)

REFUSE_WISH = re.compile(
    r"^(?:i|we)\s+(?:(?:just|really|actually|honestly)\s+)*"
    r"(?:don'?t|do\s+not|didn'?t|wouldn'?t|won'?t|hate|dislike|loathe|"
    r"can'?t\s+stand|don'?t\s+like|not\s+into|"
    r"(?:im|am|'m)\s+not\s+(?:keen\s+on|a\s+fan\s+of)|not\s+a\s+fan\s+of)"
    r"(?:\s+(?:want|wants|wanting|need|needs|fancy|feel\s+like|like))?"
    r"(?:\s+(?:a|an|the|any|anything|something|everything|nothing|too|very|really|more|"
    r"another|much|lots|of|as))*"
    r"\s+(?!(?:to|be|have|go|get|do|see|watch|read|eat|cook|make|talk|hear|listen|work|"
    r"know|understand|remember|recall|decide|think|believe|reckon|guess|say|tell|imagine|"
    r"it|this|that|one|ones|thing|things|stuff|me|us|them|him|her|my|your|our|their|"
    r"feel|feels|felt|feeling|want|wants|need|needs|fancy|like|likes|care)\b)"
    r"([a-z']+)", re.I)

REFUSAL_ACK = re.compile(
    r"\b(?:skip|avoid|steer clear|stay away from|without|instead of|rather than|except|nothing)\b")
WEAK_ACKS = frozenset(("rather than",))


CHOICE_NOUNS = frozenset(
    "film films movie movies show shows series programme programmes book books game games "
    "music song songs thing things one ones stuff food meal meals recipe recipes".split())
SAID_POLITELY = frozenset("please thanks ta though".split())


def _a_lack_not_a_refusal(flat, end):
    for word in flat[end:].strip(" .,!?;:'\"").split():
        word = word.strip(".,!?;:'\"").lower()
        if word and word not in CHOICE_NOUNS and word not in SAID_POLITELY:
            return True
    return False


def _refused(text):
    flat = " ".join(str(text or "").split())
    match = REFUSE_CHOICE.match(flat)
    if not match:
        match = REFUSE_OPEN.match(flat)
        if match:
            if _a_lack_not_a_refusal(flat, match.end()):
                return ""
        else:
            match = REFUSE_WISH.match(flat)
            if match and _a_lack_not_a_refusal(flat, match.end()) \
                    and not _ASKS_AFTER_A_TASTE.search(flat[match.end():]):
                return ""
    if not match:
        return ""
    word = match.group(1).strip(".,!?;:").lower()
    return word if len(word) > 2 else ""


_ASKS_AFTER_A_TASTE = re.compile(
    r"\b(?:what|which|anything|something|suggest|suggestions?|recommend|ideas?|instead|else|"
    r"can i|could i|should i|shall i|do i)\b", re.IGNORECASE)


def _says_it_leaves_it_out(reply, refused):
    text = " ".join(str(reply or "").lower().split())
    word = str(refused or "").strip().lower()
    if not text or not word:
        return False
    named = re.compile(r"\b%s\w*\b" % re.escape(word))
    for found in REFUSAL_ACK.finditer(text):
        if found.group(0) not in WEAK_ACKS:
            return True
        if named.search(text[found.end():found.end() + 40]):
            return True
        if named.search(text[max(0, found.start() - 30):found.start()]):
            return True
    return False


def _hands_back_the_refusal(item, refused):
    if not refused or not _is_about(item, refused):
        return False
    if _about_a_lack(item):
        return False
    reply = getattr(item, "reply", "")
    if callable(reply):
        return False
    return not _says_it_leaves_it_out(reply, refused)


LACK_OPEN = re.compile(r"^(?:no|not|nothing|without)\b", re.I)


def _about_a_lack(item):
    for part in getattr(item, "key", ()) or ():
        options = (part,) if isinstance(part, str) else part
        for option in options:
            if isinstance(option, str) and LACK_OPEN.match(option.strip()):
                return True
    return False


def _key_words(item):
    found = set()
    for part in getattr(item, "key", ()) or ():
        options = (part,) if isinstance(part, str) else part
        for option in options:
            for word in str(option).lower().split():
                found.add(word.rstrip("s") or word)
    return found


OWN_THING_AT = 3

OWN_THING_SCAN = 12

POSSESSIVE = frozenset("my our his her their".split())

PERSON_WORDS = frozenset("""son daughter husband wife mum mom dad father mother partner
    boyfriend girlfriend brother sister kid kids child children baby toddler friend mate
    neighbour neighbor colleague boss teacher nan grandma grandad granny grandchild flatmate
    housemate lodger guest visitor landlord tenant aunt auntie uncle cousin nephew niece
    grandparent parents folks family
dog cat puppy kitten pet""".split())


def _names_a_thing(understood):
    for ent in understood.get("entities") or []:
        if isinstance(ent, dict) and str(ent.get("type") or "") not in ("person", ""):
            return True
    return False


def _own_thing(understood):
    person = ""
    for ent in understood.get("entities") or []:
        if not isinstance(ent, dict):
            continue
        at = ent.get("at")
        if isinstance(at, int) and 0 <= at <= OWN_THING_AT:
            text = str(ent.get("text") or "")
            if str(ent.get("type") or "") == "person":
                person = person or text
                continue
            return text
    if person:
        return "" if _names_a_thing(understood) else person
    boilerplate = str(understood.get("clean") or understood.get("text") or "").split()
    for at, word in enumerate(boilerplate[:OWN_THING_SCAN]):
        if word.strip(".,!?;:").lower() not in POSSESSIVE:
            continue
        if at + 1 >= len(boilerplate):
            break
        span = [w.strip(".,!?;:").lower() for w in boilerplate[at + 1:at + 4]]
        if not span or span[0] in REFERRING:
            continue
        named = _thing_named_in(understood, span)
        if named:
            return named
        second = boilerplate[at + 1].strip(".,!?;:")
        if second.lower() in PERSON_WORDS and _names_a_thing(understood):
            continue
        if second:
            return second.lower()
    return ""


def _thing_named_in(understood, span):
    for ent in understood.get("entities") or []:
        if not isinstance(ent, dict):
            continue
        text = [w.lower() for w in str(ent.get("text") or "").split()]
        if not text or len(text) > len(span):
            continue
        for i in range(len(span) - len(text) + 1):
            if span[i:i + len(text)] != text:
                continue
            if str(ent.get("type") or "") == "person" and _names_a_thing(understood):
                return ""
            return text[-1]
    return ""


def _new_thing(own, answer):
    if not own:
        return False
    words = {word.strip(".,!?;:").lower() for word in str(answer).split()}
    return not any(word.rstrip("s") in words or word in words for word in own.lower().split())

def _the_run_said(memory, extra=""):
    turns = memory.get("turns")
    said = [str(extra or "")]
    answered = 0
    if isinstance(turns, list):
        for turn in reversed(turns):
            if not isinstance(turn, dict):
                break
            if turn.get("module") != "answers":
                if answered:
                    break
                continue
            said.append(str(turn.get("bot") or turn.get("reply") or ""))
            answered += 1
            if answered >= 4:
                break
    return " ".join(part for part in said if part)


def _head_thing(subject):
    return _own_thing(understand(subject)) if subject else ""


DESCRIBING = frozenset("""
fresh frozen cooked raw uncooked leftover leftovers ripe open opened unopened whole sliced cut
peeled dried dried-out tinned canned stale
""".split())


def _the_same_kind_of_thing(item, memory, text=""):
    try:
        domain = str(getattr(item, "domain", "") or "")
        if not domain:
            return False
        record = (mem.topics.carried_topic(memory, text) if text else None) or the_topic(memory)
        said = str((record or {}).get("text") or "")
        if not said:
            return False
        about = str((understand(said, {}) or {}).get("topic") or "")
        return bool(about) and about in by_topic().get(domain, ())
    except Exception:
        return False


def _reaches_another_subject(text, item, memory):
    try:
        if not is_follow_up(text, memory):
            return False
        if str((understand(text, {}) or {}).get("topic") or ""):
            return False
        if not (memory.get("turns") if isinstance(memory, dict) else None):
            return False
        around = {str(word).lower() for word in ((the_topic(memory) or {}).get("words") or ())}
        around |= {str(word).lower() for word in keywords(mem.subject(memory) or "")}
        if not around:
            return False
        keys = set(keywords(" ".join(str(word) for word in _key_words(item))))
        around = {word for word in around if word not in VAGUE}
        keys = {word for word in keys if word not in VAGUE}
        if _the_same_kind_of_thing(item, memory, text):
            return False
        if _a_definition_of_the_entry(text, item):
            return False
        return bool(keys) and not (keys & around)
    except Exception:
        return False
DETAIL_OF = re.compile(
    r"^\s*(?:and\s+|so\s+|also\s+)?(?:i|we)\s+(?:also\s+|just\s+|still\s+)?(?:[a-z']+\s+)?"
    r"(?:it|them|they|him|her|these|those)\b", re.I)
ASK_OF = re.compile(
    r"^\s*(?:and\s+|so\s+)?(?:how|what|when|where|which|who|should|shall|can|could|do|does|"
    r"did|will|would|is|are|was|were|if|any)\b", re.I)
OBJECT_PRONOUN = re.compile(r"\b(?:it|them|that|this|those|these|one)\b", re.I)
DO_VERBS = frozenset("""
water feed clean wash trim cut prune mow repot mist move cover drain bleed charge replace change
check add give take put turn leave run walk play use paint sand oil service tidy hoover dust
eat drink make cook bake freeze reheat serve store keep need want get buy pay sell work go come
""".split())
REPORT_WORDS = frozenset("""
day days week weeks month months year years morning evening night time times once twice daily
weekly monthly yearly every each a an all the at in on of and but to for with it them they him
her these those i we my our just still also really always never usually sometimes about
much many lot little bit twice three four five six two one few several
last next ago past
""".split())
ASK_WORDS = frozenset("""
how what when where which who why should shall can could would will do does did is are was were
if any ok okay please before after since until tonight tomorrow today again too soon often long
take need want have has keep use get put make cook freeze reheat serve store prepare
it that this these those them they him her one ones
""".split())

SAID_OF_THE_THING = frozenset("""
red blue green yellow white black grey gray brown pink purple orange cream beige navy teal
turquoise lilac mauve magenta gold silver bronze ivory charcoal
""".split())


def _off_the_topic(understood, memory):
    if not isinstance(understood, dict) or not isinstance(memory, dict):
        return frozenset(), "", False
    text = understood.get("clean") or understood.get("text") or ""
    detail = "?" not in text and bool(DETAIL_OF.search(text))
    asking = bool(ASK_OF.search(text) and OBJECT_PRONOUN.search(text))
    if not (detail or asking):
        return frozenset(), "", False
    allowed = (REPORT_WORDS | DO_VERBS | (ASK_WORDS if asking else frozenset())
               | (SAID_OF_THE_THING if detail else frozenset()))
    says_what_it_is = False
    for word in said_topic.words(text):
        if word.isdigit() or word in allowed or (said_topic.forms(word) - {word}) & allowed:
            if detail and word in SAID_OF_THE_THING:
                says_what_it_is = True
            continue
        return frozenset(), "", False
    leans_on = understood.get("leans_on")
    if not isinstance(leans_on, dict):
        return frozenset(), "", False
    said = str(leans_on.get("text") or "")
    if not said:
        return frozenset(), "", False
    last = memory.get("last_answer") if isinstance(memory.get("last_answer"), dict) else {}
    domain = str(last.get("domain") or "")
    if not domain:
        home = find(understand(said, memory))
        domain = str(getattr(home, "domain", "") or "")
    words = {word for word in said_topic.keywords(said)
             if word not in REPORT_WORDS and word not in DO_VERBS and word not in ASK_WORDS}
    return frozenset(words), domain, says_what_it_is


def _from_another_domain(item, off_topic):
    words, domain = off_topic[0], off_topic[1]
    if domain and str(getattr(item, "domain", "") or "") == domain:
        return False
    return not _names_a_topic_word(item, words)


def _names_a_topic_word(item, wanted):
    keys = {str(key).lower() for key in _key_words(item)}
    for word in wanted:
        if word in keys or said_topic.stem(word) in keys:
            return True
    return False



BARE_GENERIC = frozenset("""first next best else last thing things way ways part bit most least
    change changing start starting stop stopping more right now then again still only just""".split())


ASKING = frozenset("""look looking wear wearing do does get getting pick choose need buy
    prepare bring bring take taking use check expect know say tell ask want find worth""".split())


SPEECH = frozenset("""say saying tell telling ask asking talk talking phrase wording word
    mention explain explaining""".split())


TIME_WORDS = frozenset("""january february march april may june july august september october
november december jan feb mar apr jun jul aug sep sept oct nov dec monday tuesday wednesday
thursday friday saturday sunday weekend weekday morning afternoon evening night tonight today
tomorrow yesterday week weeks month months year years next this last first soon""".split())


def _topic_words(line, memory):
    said = set(mem.content(line))
    record = mem.topics.carried_topic(memory or {}, line) or {}
    return [word for word in mem.content(record.get("text") or "")
            if word not in said and word not in BARE_GENERIC and word not in TIME_WORDS]


def _lent_words(reading, memory):
    line = str(reading.get("clean") or reading.get("text") or "")
    said = set(mem.content(line))
    wider = mem.followup_reading(reading, memory or {})
    added = str(wider.get("clean") or wider.get("text") or "") if isinstance(wider, dict) else ""
    words = [word for word in mem.content(added) if word not in said]
    if not words:
        return _topic_words(line, memory)
    return [word for word in words if word not in BARE_GENERIC and word not in TIME_WORDS]


def _same_word(word, said):
    if word == said:
        return True
    if len(word) < 4 or len(said) < 4:
        return False
    return word.startswith(said) or said.startswith(word)


def _writes_its_own_reply(item):
    return callable(getattr(item, "reply", None))


ASKING_VERBS = frozenset("""help helps helped helping work works worked working fix fixes fixing
                         sort sorts sorted deal deals coping cope handle handles try tries""".split())


def _leans_on(reading, item, memory=None):
    line = reading.get("clean") or reading.get("text") or ""
    line_words = mem.content(line)
    own = [word for word in line_words
           if word not in ASKING and word not in BARE_GENERIC and word not in ASKING_VERBS
           and word not in mem.topics.MONTH_NAMES and word not in mem.topics.SEASONS]
    vague = not own and any(word in BARE_GENERIC for word in line_words)
    keyed = _key_words(item)
    says = set(keyed)
    reply = getattr(item, "reply", "")
    if isinstance(reply, str):
        says |= {word.strip(string.punctuation).rstrip("s") for word in reply.lower().split()}
    topic = _topic_words(line, memory)
    carried = (mem.topics.carried_topic(memory or {}, line) or {}).get("text") or ""
    topic_text = " ".join(str(carried).lower().split())
    subject_of_the_topic = ([str(word).lower() for word in mem.key_subject(carried, memory)]
                            if carried else [])
    about = subject_of_the_topic or topic
    about_text = " ".join(subject_of_the_topic) or topic_text
    lent = _lent_words(reading, memory)
    hits = {word for word in lent if any(_same_word(word, other) for other in says)}
    avoid = getattr(item, "avoid", ()) or ()
    named = [word for word in own if word not in PROPERTY_WORDS] or own
    names_it = any(_same_word(word, said) for word in named for said in keyed)
    def _it_says_it_is_not(phrase):
        phrase = phrase.strip().lower()
        if not phrase or phrase in FEELINGS:
            return False
        return phrase in about or (" " in phrase and phrase in about_text)
    if any(_it_says_it_is_not(word) for word in avoid if isinstance(word, str)):
        return False
    if not own:
        return len(hits) >= (2 if vague else 1)
    ask_side = [word for word in own if word not in PROPERTY_WORDS]
    if not ask_side:
        return bool(hits)
    if not any(_same_word(word, said) for word in own for said in says):
        if not _a_money_question(own, keyed):
            return False
    if (not hits and not _writes_its_own_reply(item)
            and mem.topics.next_slot_reading(reading, memory or {}) is None):
        return False
    if set(line.lower().split()) & SPEECH and not says & SPEECH:
        return False
    return True



def _is_about(item, subject):
    words = [word for word in subject.split() if word not in DESCRIBING] or subject.split()
    head = (words or [""])[-1]
    head = head.rstrip("s") or head
    if not head or head not in _key_words(item):
        return False
    if head in kinds.VERBISH or (len(head) > 4 and head.endswith(("ed", "ing"))):
        named = [word for word in words if word not in kinds.VERBISH
                 and not (len(word) > 4 and word.endswith(("ed", "ing")))]
        keys = _key_words(item)
        return any(word.rstrip("s") in keys or word in keys for word in named)
    return True


PLACE_WORDS = frozenset("""
fridge freezer oven grill hob microwave pan pans pot pots tray tin tins dish dishes shelf
cupboard counter worktop sink kettle toaster air fryer barbecue bbq fridge-freezer larder
room kitchen outside indoors
""".split())


SUM_TABLE = re.compile(r"£[\d,]+ a month is \d")

FEELINGS = frozenset("""stressed stress stressed-out worried worry anxious anxiety nervous sad
    upset feeling feelings scared afraid frightened terrified angry cross annoyed frustrated
    happy glad excited relieved tired exhausted shattered overwhelmed guilty ashamed embarrassed
    lonely fed-up down low rubbish awful terrible horrible upset gutted excited keen fuming
    panicking panic crying upset""".split())


PROPERTY_WORDS = frozenset("""long time times minute minutes hour hours day days much many far often temperature temp temps
degrees centigrade fahrenheit heat
hot warm cold size price cost spend pressure bar psi
spending pay paying per kilo kilos kg gram grams start finish last first take takes need needs
one ones
rest resting hard soft runny jammy medium rare fan gas thick thin large small whole skimmed semi
cook cooking bake baking roast roasting boil boiling fry frying grill grilling leave leaving
sit sitting wait waiting cool cooling chill chilling set setting
causing caused cause causes why reason worth worths valued value
# A date is a property of the answer too: after a dated answer, "when did that happen" and
# "what year was that" name the part they want and no subject of their own.
year years date happen happened done
""".split())


def _only_a_property(words):
    return bool(words) and not [word for word in words if word not in PROPERTY_WORDS]


PROPERTY_WORD_THAT_NAMES_A_THING = re.compile(
    r"\b(?:a|an|the|my|your|his|her|their|our|this|that|these|those|any|no)\s+"
    r"(?:colds?|heats?|lights?|darks?|prices?|costs?|sizes?|times?|dates?|years?|days?"
    r"|starts?|finishes?)\b"
    r"|\b(?:colds|lights|prices|costs|sizes|dates|starts|finishes)\b",
    re.I,
)


def _a_property_word_names_a_thing(text):
    return bool(PROPERTY_WORD_THAT_NAMES_A_THING.search(str(text or "")))


MONEY_ASK = frozenset("""
cheap cheaper cheapest expensive pricey costly dear affordable cost costs costing price prices
priced charge charges fee fees
""".split())


def _a_money_question(own, keyed):
    return bool(set(own) & MONEY_ASK) and bool(set(keyed) & MONEY_ASK)


def _remember_answer(memory, item, reply, keys=()):
    if not isinstance(reply, str) or not reply.strip():
        return
    turns = memory.get("turns")
    memory["last_answer"] = {
        "reply": reply,
        "keys": sorted(_key_words(item) | set(keys)),
        "id": getattr(item, "id", None),
        "domain": getattr(item, "domain", "") or "",
        "turn": len(turns) if isinstance(turns, list) else 0,
    }


def _last_answer(memory):
    record = memory.get("last_answer")
    if not isinstance(record, dict) or not record.get("reply"):
        return None
    turns = memory.get("turns")
    if not isinstance(turns, list):
        return None
    turn = record.get("turn")
    if not isinstance(turn, int) or turn < 0 or turn >= len(turns):
        return None
    if len(turns) - 1 - turn > 4:
        return None
    said = turns[turn] if isinstance(turns[turn], dict) else {}
    if said.get("module") != "answers":
        return None
    topic = mem.current(memory)
    if not isinstance(topic, dict) or not isinstance(topic.get("turn"), int):
        return None
    if topic["turn"] > turn:
        here = set(keywords(topic.get("text") or ""))
        if not here & set(record.get("keys") or ()):
            return None
    return record


def _asks_part(text):
    if asked_kind(text) == "cause" and not keywords(text):
        return True
    if asked_kind(text) is not None:
        return _only_a_property(keywords(text))
    return asks_a_part(text)


YES_NO_ABOUT_A_THING = re.compile(
    r"^\s*(?:will|would|does|do|did|can|could|should|shall|is|are|was|were|has|have|must|might)\b",
    re.I)

ASKING_FRESH = frozenset("""
what which how why when where who whose should would could can will shall do does did is are
was were need needs must if
""".split())

OPTION_TIMING = re.compile(r"\bin\s+\d+\b", re.I)

DIGIT_OR_SPAN = re.compile(
    r"\d|\b(?:an?|one|two|three|four|five|six|seven|eight|nine|ten|twelve|fifteen|twenty|thirty|"
    r"forty|fifty|sixty|ninety|hundred)\s+(?:seconds?|secs?|minutes?|mins?|hours?|hrs?|days?|"
    r"weeks?|months?|years?)\b", re.I)

DEPENDENT_SENTENCE = re.compile(
    r"^\s*(?:there|it|this|that|these|those|also|and|so|then|plus|but)\b", re.I)

ABOUT_THE_ANSWER = frozenset("""
work works working help helps helped use using used try trying need needs needed
better best good good idea worth right wrong okay ok actually really still just also
instead thing things way ways method enough any more much option
""".split())


def _the_sentence_about(text, memory):
    earlier = _last_answer(memory)
    if not earlier:
        return None
    reply = earlier.get("reply") or ""
    if not reply.strip() or len(text.split()) > 7:
        return None
    if DIGIT_OR_SPAN.search(text):
        return None
    said_so_far = words_of(text)
    asked_fresh = ASKING_FRESH.intersection(re.findall(r"[a-z']+", flat(text)))
    if not (YES_NO_ABOUT_A_THING.search(flat(text))
            or (len(said_so_far) <= 3 and not asked_fresh)):
        return None
    said = set(words_of(reply)) | set(earlier.get("keys") or ())
    named, other = [], False
    for word in words_of(text):
        if word in ABOUT_THE_ANSWER or len(word) < 3:
            continue
        if word in said:
            named.append(word)
        else:
            other = True
    if not named or other:
        return None
    sentences = same_again.quoted.sentences(reply, SENTENCE)
    holding = [one for one in sentences if all(word in set(words_of(one)) for word in named)]
    if len(holding) != 1 or len(sentences) < 2:
        return None
    part = holding[0]
    if flat(part) == flat(reply):
        return None
    if len(OPTION_TIMING.findall(part)) >= 2:
        return None
    if DEPENDENT_SENTENCE.match(part) or len(part) < 40:
        return None
    return _part_not_repeated(part, reply, memory)


WHO_TO_CALL = re.compile(
    r"^\s*(?:(?:so|and|but|ok|okay|then|also|right|now|sorry|hmm)[\s,]+)*"
    r"(?:who|which)\b(?:(?!\?).){0,40}?"
    r"\b(?:call|ring|phone|contact|get\s+(?:in|out|somebody|someone|a\\s)|ask|speak\s+to|"
    r"talk\s+to|come\s+out|do\s+i\s+get)\b", re.I)
A_TRADE = frozenset("""
engineer plumber electrician roofer locksmith glazier builder surveyor landlord
landlady letting agent council insurer insurance vet doctor gp dentist nurse optician
pharmacist mechanic garage sweep decorator plasterer joiner drain drains
""".split())
CONDITIONS_THE_LINE = re.compile(r"^\s*(?:if|when|unless|where|in\s+case)\b", re.I)
OPENING_CONNECTIVE = re.compile(r"^(?:then|and|so|but|now|next|first|also)[\s,]+", re.I)
SAYS_TO_GET_SOMEBODY = re.compile(
    r"^\s*(?:then|so|and|now|next|first)?[\s,]*"
    r"(?:get|call|ring|phone|contact|ask|book|hire|find|use|see|tell|speak\s+to|talk\s+to)\b",
    re.I)
SOMEONE_TO_GET = re.compile(
    r"\b(?:call|ring|phone|get|ask|tell|book|find|hire|contact|use)\b", re.I)
STOCK_ACKNOWLEDGEMENT = re.compile(
    r"^\s*(?:got\s+it|noted|right|ok|okay|thanks|thank\s+you|of\s+course|sure|understood|"
    r"no\s+problem|fair\s+enough)\b", re.I)
ACK_MODULES = frozenset({"greeting", "memory_store"})
MOST_ACKS = 2
MOST_WORDS_OF_AN_ACK = 24


def _a_stock_acknowledgement(turns, back):
    turn = turns[-1 - back]
    if not isinstance(turn, dict):
        return False
    reply = str(turn.get("bot") or "").strip()
    if not reply:
        return False
    if turn.get("module") in ACK_MODULES and len(reply.split()) <= MOST_WORDS_OF_AN_ACK:
        if STOCK_ACKNOWLEDGEMENT.match(reply):
            return True
    before = turns[-2 - back] if len(turns) > 1 + back else None
    if isinstance(before, dict):
        earlier = flat(str(before.get("bot") or ""))
        said = flat(reply)
        if earlier and said and len(said.split()) >= 4 and said in earlier:
            return True
    return False


def _the_person_to_call(text, memory):
    if not WHO_TO_CALL.search(flat(text)):
        return None
    spare = [word for word in words_of(text) if word not in WHO_ASK_WORDS and len(word) > 2]
    if spare:
        return None
    turns = memory.get("turns") if isinstance(memory, dict) else None
    if not isinstance(turns, list) or not turns or not isinstance(turns[-1], dict):
        return None
    last = turns[-1]
    if last.get("module") != "answers":
        skipped = 0
        while (skipped < MOST_ACKS and len(turns) - 1 - skipped >= 0
               and _a_stock_acknowledgement(turns, skipped)):
            skipped += 1
        if not skipped or len(turns) - 1 - skipped < 0:
            return None
        last = turns[-1 - skipped]
        if last.get("module") != "answers":
            return None
    reply = str(last.get("bot") or "").strip()
    if not reply:
        return None
    sentences = [one.strip() for one in SENTENCE.split(reply) if one.strip()]
    if len(sentences) < 2:
        return None
    holding = [one for one in sentences
               if A_TRADE.intersection(re.findall(r"[a-z']+", one.lower()))]
    if not holding:
        return None
    getting = [one for one in holding if SOMEONE_TO_GET.search(one)]
    pool = getting or holding
    stating = [one for one in pool if not CONDITIONS_THE_LINE.match(one)]
    pool = stating or pool
    up_front = [one for one in pool if SAYS_TO_GET_SOMEBODY.match(one)]
    ordered = up_front + [one for one in pool if one not in up_front]
    named = [one for one in ordered
             if A_TRADE.intersection(re.findall(r"[a-z']+", one.lower()))]
    if not named:
        return None
    part = named[0]
    stripped = OPENING_CONNECTIVE.sub("", part).strip()
    if stripped != part and stripped:
        part = stripped[:1].upper() + stripped[1:]
    if len(part) < 25 or not part[:1].isupper() or DEPENDENT_SENTENCE.match(part):
        return None
    part = _the_clause_that_says_who(part)
    return _part_not_repeated(part, reply, memory)


CLAUSE_BREAK = re.compile(r"\s*[,;:]\s*|\s+(?:and|but|then|so)\s+", re.I)
LONG_SENTENCE_WORDS = 24


def _the_clause_that_says_who(part):
    if len(part.split()) <= LONG_SENTENCE_WORDS:
        return part
    pieces = [one.strip() for one in CLAUSE_BREAK.split(part) if one.strip()]
    for piece in reversed(pieces):
        named = A_TRADE.intersection(re.findall(r"[a-z']+", piece.lower()))
        if named and SOMEONE_TO_GET.search(piece):
            piece = OPENING_CONNECTIVE.sub("", piece).strip() or piece
            return piece[:1].upper() + piece[1:]
    return part


WHO_ASK_WORDS = frozenset("""
who which what should shall do does can could would will might i we you they me my our
call ring phone contact get ask speak talk to about now then also just really
somebody someone anybody anyone person people trade tradesman professional expert
kind sort type best good right one out in come
""".split())

CHOICE_ASK = re.compile(
    r"^\s*(?:so |ok |okay |right |and |then )*(?:"
    r"which (?:one|ones|of those|of them|of these)"
    r"|which should i (?:get|buy|pick|choose|go for)"
    r"|which would you|which do you"
    r"|what (?:should|would) (?:i|you) (?:get|buy|pick|choose|go for)"
    r"|what do you recommend|what would you recommend"
    r"|any recommendations?|any suggestions?)\s*[?.!]*\s*$")
CHOICE_CONTEXT = re.compile(
    r"\b(?:buy|buying|bought|get|getting|purchase|recommend|recommendation|best|worth|"
    r"choose|choosing|pick|picking|upgrade|look for|looking for|which|new)\b")
A_SPEC = re.compile(
    r"\d|\b(?:gb|tb|mb|ghz|mah|kg|litres?|litre|ml|cm|mm|inch|inches|watt|watts|hours?|"
    r"minutes?|percent|pounds?|quid|years?|months?|weeks?|degrees?|spin|speed|drum|size|"
    r"tog|thread|bar|btu)\b")
CHOICE_TAIL = (
    "That is the bit that decides it.",
    "That is the one I would go for.",
    "That is what to go by.",
)


CHOICE_CUT = re.compile(r",?\s+(?:and |but |so |which |because )|;\s+")
CHOICE_SHORTEST = 60


def _the_clause_that_picks(sentence):
    if len(sentence) <= 150:
        return sentence
    for found in CHOICE_CUT.finditer(sentence):
        start = found.start()
        if start >= CHOICE_SHORTEST:
            return sentence[:start].strip(" ,;")
    return sentence


CHOICE_FIGURE = re.compile(
    r"\d|\b(?:gb|tb|mb|ghz|mah|kg|litres?|ml|cm|mm|inch|inches|watt|watts|tog)\b", re.I)
CHOICE_LIST_HEAD = re.compile(r"\b(?:get|buy|make|go|choose|take|pick|spend|aim|look for|opt for)"
                              r"\b", re.I)
CHOICE_ITEM = re.compile(r",\s+")
CHOICE_LEAD_VERB = re.compile(r"^(?:get|buy|choose|take|go for|pick|look for|aim for|spend|opt for"
                              r"|go with)\s+", re.I)
CHOICE_CONDITION = re.compile(r"\s+(?:if|unless|when)\s+")
CHOICE_COST = re.compile(r"[£$€]\s*\d[\d,.]*|\b\d[\d,.]*\s*(?:pounds?|quid|dollars?|euros?)\b", re.I)
CHOICE_PRICE_OPENS = re.compile(
    r"^(?:about|around|roughly|approx(?:imately)?|maybe|somewhere|up to|over|under)?\s*"
    r"(?:[£$€]\s*\d[\d,.]*|\d[\d,.]*\s*(?:pounds?|quid|dollars?|euros?))\b"
    r"(?=\s*(?:[a-z]+\s+){0,4}?(?:is|are|was|were)\b)", re.I)
CHOICE_PRICE_ONLY = re.compile(
    r"(?:about|around|roughly|approx(?:imately)?|maybe|somewhere|up to|over|under|less than|more"
    r" than|between)?\s*(?:[£$€]\s*\d[\d,.]*|\d[\d,.]*\s*(?:pounds?|quid|dollars?|euros?))"
    r"(?:\s*(?:to|-|and)\s*(?:[£$€]\s*)?\d[\d,.]*)?", re.I)


def _a_list_of_things(tail):
    items = [one.strip(" .!?") for one in re.split(r",\s*|\s+and\s+", tail)]
    items = [re.sub(r"^(?:or|and)\s+", "", one) for one in items if one]
    return (len(items) >= 3
            and all(2 <= len(one.split()) <= 11 for one in items))


def _the_thing_that_picks(sentence):
    span = sentence.strip()
    listed = sized = False
    if ": " in span:
        head, tail = span.split(": ", 1)
        head, tail = head.strip(), tail.strip()
        if len(tail.split()) >= 3:
            if (CHOICE_LIST_HEAD.search(head) and not CHOICE_FIGURE.search(head)
                    and _a_list_of_things(tail)):
                span, listed = tail, True
            elif len(CHOICE_FIGURE.findall(head)) > len(CHOICE_FIGURE.findall(tail)):
                span, sized = head, True
            elif len(CHOICE_FIGURE.findall(tail)) > len(CHOICE_FIGURE.findall(head)):
                span, sized = tail, True
            else:
                span = head
    first = CHOICE_ITEM.split(span, 1)
    takes_the_figure = (len(first) == 2 and CHOICE_FIGURE.search(span)
                        and not CHOICE_FIGURE.search(first[0]))
    if len(first) == 2:
        if len(first[0].split()) < 2:
            return None
        if takes_the_figure:
            pass
        else:
            span = first[0]
    span = CHOICE_LEAD_VERB.sub("", span)
    conditional = CHOICE_CONDITION.search(span)
    if conditional and conditional.start() >= 8:
        span = span[:conditional.start()]
    span = _the_clause_that_picks(span).strip(" ,;:.!?")
    if len(span.split()) < 2:
        return None
    if _a_price_and_nothing_else(span):
        return None
    if listed:
        return span
    if sized or CHOICE_FIGURE.search(span):
        return span
    return None


CHOICE_NOT_A_THING = frozenset("""
    about around roughly approx approximately maybe perhaps somewhere between up over under less
    more than to and or the a an it its that this these those is are was were be being been of
    for per at in on with without plus altogether total totals overall usually usual typical
    typically average norm normally going rate price prices cost costs cheap cheaper cheapest
    expensive budget spend spending paying pay paid altogether cheaper worth pounds quid dollars
    euros notes coins roughly
""".split())


def _a_price_and_nothing_else(span):
    rest = CHOICE_PRICE_ONLY.sub(" ", span)
    if not any(word not in CHOICE_NOT_A_THING for word in re.findall(r"[a-z]{2,}", rest.lower())):
        return True
    bare = span.rstrip(" .!?")
    if CHOICE_PRICE_OPENS.match(bare):
        return True
    ends = CHOICE_COST.search(bare)
    if ends and bare[ends.end():].strip(" .,!?"):
        ends = None
    return bool(ends)


def _the_composer_has_options(memory):
    try:
        from ..compose import fallback as composer
        return bool(composer._offered(memory))
    except Exception:
        return False


_AN_ALTERNATIVE = re.compile(r"\b(?:or|vs\.?)\b", re.I)
_NOT_AN_OPTION = frozenset("""a an the i we you it that this these those and but so if for to of
in on at by is are was were be been do does did would could should can will go get got one
both either neither""".split())


def _the_option_that_decides(said, reply):
    head = re.split(r"[.!?\u2014:;]", str(reply or "").strip(), 1)[0]
    in_the_question = set(re.findall(r"[a-z][a-z'\u2019-]*", said.lower()))
    for word in re.findall(r"[A-Za-z][A-Za-z'\u2019-]*", head)[:5]:
        low = word.lower()
        if low in in_the_question and low not in _NOT_AN_OPTION:
            return word
    return ""


def _the_answer_to_a_choice_behind(memory):
    turns = memory.get("turns") if isinstance(memory, dict) else None
    for row in reversed(turns if isinstance(turns, list) else ()):
        if not isinstance(row, dict):
            continue
        said = " ".join(str(row.get("user") or "").lower().split())
        reply = str(row.get("bot") or "").strip()
        if not said or not reply or len(said.split()) > 16:
            continue
        if not _AN_ALTERNATIVE.search(said):
            continue
        option = _the_option_that_decides(said, reply)
        if not option:
            continue
        return f"{option[:1].upper()}{option[1:]}. That is the one I would go for."
    return None


def _the_one_to_pick(text, memory):
    clean = " ".join(str(text or "").lower().split())
    if not CHOICE_ASK.match(clean):
        return None
    if " or " in f" {clean} " or " vs " in f" {clean} " or "better" in clean:
        return None
    earlier = _last_answer(memory)
    if not earlier:
        return _the_answer_to_a_choice_behind(memory)
    turns = memory.get("turns") or []
    turn = earlier.get("turn")
    before = ""
    if isinstance(turn, int) and 0 <= turn < len(turns) and isinstance(turns[turn], dict):
        before = str(turns[turn].get("user") or turns[turn].get("text") or "").lower()
    if not CHOICE_CONTEXT.search(before):
        return None
    if _the_composer_has_options(memory):
        return None
    reply = str(earlier.get("reply") or "").strip()
    if not reply:
        return None
    sentences = [one.strip() for one in SENTENCE.split(reply) if one.strip()]
    if not sentences:
        return None
    choose_from = [one for one in sentences if not one.rstrip().endswith("?")]
    if not choose_from:
        return None
    best = choose_from[0]
    if not A_SPEC.search(best):
        for sentence in choose_from[1:]:
            if A_SPEC.search(sentence):
                best = sentence
                break
    said = _flat(best)
    if not said or said == _flat(mem.last_bot(memory) or ""):
        return None
    pick = _the_thing_that_picks(best)
    if not pick or len(pick.split()) < 2 or _flat(pick) == _flat(mem.last_bot(memory) or ""):
        return None
    tail = CHOICE_TAIL[len(said) % len(CHOICE_TAIL)]
    pick = pick.rstrip('. ') or pick.rstrip()
    return f"{pick[:1].upper()}{pick[1:]}. {tail}"
_DISH_TIME = re.compile(r"\(\s*(\d+)\s*(minutes?|mins?|hours?|hrs?)\s*\)")
_WORD_NUMBER = (r"\d+|an?|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|fifteen"
                r"|twenty|thirty|forty|fifty|sixty|ninety|twenty[-\s]five|twenty[-\s]ten"
                r"|thirty[-\s]five|forty[-\s]five")
_A_WHOLE_TIME = re.compile(r"(__N__)(?:\s*(?:to|or|-|and a half)\s*(__N__))?\s*"
                           r"(minutes?|mins?|hours?|hrs?)\b".replace("__N__", _WORD_NUMBER), re.I)
_A_BARE_TIME = re.compile(r"^\s*(?:about\s+|roughly\s+|around\s+)?(?:%s)"
                          % _A_WHOLE_TIME.pattern, re.I)
_A_LABELLED_TIME = re.compile(r"^\s*[A-Z][\w' -]{0,40}:\s*([^:.;\n]{0,90})")
_RATE = re.compile(r"\b(?:per|each)\b|\ba\s+\d+(?:\.\d+)?\s*(?:g|kg|lb|oz)\b", re.I)
_TIME_TAIL = re.compile(r"^(?:give or take|in all|altogether|from scratch|start to finish|or so"
                        r"|no packet needed|flat|to make|total)?$", re.I)

_HOW_LONG_ONLY = frozenset((
    "how", "long", "many", "much", "does", "do", "did", "will", "would", "that", "it", "this",
    "them", "take", "takes", "then", "so", "roughly", "about", "and", "to", "cook", "make",
    "minute", "minutes", "mins", "hour", "hours", "time", "the", "a", "is", "are", "s", "for",
    "of", "altogether", "total", "start", "finish", "from", "scratch"))


def _one_total(rest, whole_sentence=False):
    rest = " ".join(str(rest or "").strip(" .,;:!?-").split())
    if rest[:1].isdigit() or _RATE.search(rest):
        return False
    if re.search(r"\b\d+(?:\.\d+)?(?![\w\u00b0])", rest.split(";")[0]):
        return False
    if whole_sentence:
        return bool(_TIME_TAIL.match(rest))
    return True


def _the_dish_time(understood, memory):
    text = str((understood or {}).get("clean") or "")
    if asked_kind(text) != "time":
        return None
    words = [str(word).lower() for word in (understood or {}).get("words") or ()]
    if not words or [word for word in words if word not in _HOW_LONG_ONLY]:
        return None
    earlier = _last_answer(memory)
    if not earlier:
        return None
    reply = str(earlier.get("reply") or "")
    whole = None
    bracketed = {"%s %s" % (one.group(1), one.group(2).lower())
                 for one in _DISH_TIME.finditer(reply)}
    if len(bracketed) == 1:
        whole = bracketed.pop()
    if whole is None:
        sentences = set()
        for part in re.split(r"(?<=[.!?])\s+", reply.strip()):
            bare = _A_BARE_TIME.match(part)
            if bare and _one_total(part[bare.end():], whole_sentence=True):
                sentences.add(" ".join(bare.group(0).lower().split())
                              .replace("about ", "").replace("roughly ", "").replace("around ", ""))
        if len(sentences) == 1:
            whole = sentences.pop()
    if whole is None:
        labelled = _A_LABELLED_TIME.match(reply.strip())
        if labelled:
            first = _A_BARE_TIME.match(labelled.group(1))
            if first and _one_total(labelled.group(1)[first.end():]):
                whole = (" ".join(first.group(0).lower().split())
                         .replace("about ", "").replace("roughly ", "").replace("around ", ""))
    if whole is None:
        return None
    for food in cooking.ingredients(understood):
        if str(food).lower() not in reply.lower():
            return None
    return "About %s for that one, start to finish." % whole


CORRECTION_FRAME = re.compile(
    r"^\s*(?:(?:no|nope|sorry|actually|wait|hold\s+on|oops|oh|and|so|right|ok|okay)\b[\s,]*)*"
    r"(?:i\s+(?:mean|meant)(?:\s+to\s+say)?|make\s+that|sorry|no|nope|actually|wait)\b[\s,]*",
    re.I)
A_BARE_FIGURE = re.compile(r"^\s*(\d+(?:\.\d+)?)\s*([a-z]{0,6})?\s*[.!]?\s*$", re.I)
A_UNIT = re.compile(
    r"\b\d+(?:\.\d+)?\s*(kg|kgs|kilos?|kilograms?|g|grams?|lb|lbs|pounds?|litres?|liters?"
    r"|l|ml|pints?)\b", re.I)
UNIT_WORDS = {"kilo": "kg", "kilos": "kg", "kilogram": "kg", "kilograms": "kg",
              "kgs": "kg", "gram": "g", "grams": "g", "pound": "lb", "pounds": "lb", "lbs": "lb",
              "litre": "litres", "liter": "litres", "liters": "litres", "pint": "pints"}


def _the_unit_last_said(memory, reply):
    turns = memory.get("turns") if isinstance(memory, dict) else None
    for said_turn in reversed(turns or []):
        said = A_UNIT.search(str(said_turn.get("user") or ""))
        if said:
            return said.group(1).lower()
    for said in A_UNIT.finditer(reply or ""):
        before = (reply or "")[:said.start()].rstrip().lower()
        if before.endswith("per"):
            continue
        return said.group(1).lower()
    return None


def _the_figure_they_meant(text, memory, reply):
    said_line = str(text or "")
    body = CORRECTION_FRAME.sub("", said_line)
    if body.strip() == said_line.strip():
        return None
    found = A_BARE_FIGURE.match(body)
    if not found:
        return None
    figure, unit = found.group(1), (found.group(2) or "").lower()
    if unit not in ("kg", "g", "lb", "l", "ml", "cm", "mm"):
        unit = _the_unit_last_said(memory, reply)
        if not unit:
            return None
    return "and for {} {}".format(figure, UNIT_WORDS.get(unit, unit))


def _amount_asked(text, memory):
    earlier = _last_answer(memory)
    if not earlier:
        return None
    reply = earlier.get("reply") or ""
    corrected = _the_figure_they_meant(text, memory, reply)
    if corrected:
        text = corrected
    elif asked_kind(text) != "time" and not RATE.search(reply):
        return None
    clean = lambda found: {re.sub(r"\s+", "", one.group(0).lower()) for one in found}
    amounts = [one.group(0) for one in AMOUNT.finditer(text)]
    wanted = clean(AMOUNT.finditer(text))
    if not wanted or wanted <= clean(AMOUNT.finditer(reply)):
        return None
    subject = mem.subject(memory)
    if not subject:
        return None
    replaced = bool(SIZE_REPLACED.search(text)) and asked_kind(text) != "time" and RATE.search(reply)
    if replaced:
        fuller = "how long for {} {}?".format(amounts[0], subject)
    else:
        fuller = _with_subject(text, memory)
        if fuller.strip() == str(text).strip():
            fuller = _about_subject(text, memory)
        if fuller.strip() == str(text).strip():
            fuller = str(text).rstrip("?.! ") + " for the " + subject + "?"
    reading = understand(fuller, memory)
    item = find(reading)
    if item is None or not _is_about(item, subject):
        return None
    own = None if replaced else find(understand(text, memory))
    if own is not None and own is not item:
        return None
    fresh = _payload(item, memory, reading)
    sized = mem.sized_reply(fresh, text, memory, _key_words(item))
    if sized:
        return sized
    part = narrow(fresh, fuller) or narrow(fresh, "how long for " + amounts[0])
    if isinstance(part, str) and part.strip() and flat(part) != flat(fresh):
        return _part_not_repeated(part, fresh, memory)
    return None


SIZE_REPLACED = re.compile(r"\b(?:instead|now|this\s+time)\b", re.I)


def _the_amount_they_named_again(text, memory):
    earlier = _last_answer(memory)
    reply = str((earlier or {}).get("reply") or "").strip()
    if not reply:
        return None
    amounts = [one.group(0) for one in AMOUNT.finditer(text)]
    if len(amounts) != 1:
        return None
    if not SIZE_REPLACED.search(text):
        return None
    if not re.search(r"(?:^|[^\w])" + re.escape(amounts[0]) + r"(?:[^\w]|$)", reply, re.I):
        return None
    if swap.thing(text):
        return None
    if _own_thing(understand(text, memory)):
        return None
    sentences = [one for one in SENTENCE.split(reply) if one.strip()]
    carrying = [one for one in sentences if re.search(re.escape(amounts[0]), one, re.I)]
    if not carrying:
        return None
    best = min(carrying, key=lambda one: len(one)).strip()
    for lead in (": ", ", so ", " so ", ", which means ", " \u2014 ", ", then ", "; "):
        cut = best.rfind(lead)
        if cut < 0:
            continue
        tail = best[cut + len(lead):].strip()
        if re.search(re.escape(amounts[0]), tail, re.I):
            best = tail
            break
    return best[:1].upper() + best[1:] if best else None

MACHINE_ASKING = re.compile(
    r"\b(?:worth|should|shall|is it|is that|would|could|can i|do i|who|whom|what|how|where|when|"
    r"why|or new|or replace|fix|fixing|repair|repairing|replace|replacing|salvage|scrap)\b")


def _the_machine_follow_up(text, reading, memory):
    line = _flat(text)
    if home.machine_named(line):
        return None
    if not MACHINE_ASKING.search(line):
        return None
    asks = home.CALLING_SOMEONE.search(line) or (
        home.FOLLOWING_IT.search(line) and home.DECIDING_NOW.search(line))
    if not asks:
        return None
    earlier = home.machine_before(memory)
    if not earlier:
        return None
    part = narrow(mem.last_bot(memory) or "", text)
    if part:
        return part
    reply = home.the_machine_decision(memory, earlier, line)
    return reply if isinstance(reply, str) and reply.strip() else None


WHEN_OF_THE_DAY = re.compile(
    r"\b(?:when|what\s+time)\b[^.?!]*\b(?:take|taking|use|using|eat|eating|have|having|do|doing|"
    r"put|apply|give)\s+(?:it|them|this|these|those|one|mine|the\s+\w+)\b", re.I)


def _part_asked(text, memory):
    if _a_property_word_names_a_thing(text):
        return None
    if WHEN_OF_THE_DAY.search(str(text or "")) and asked_kind(text) == "date":
        return None
    earlier = _last_answer(memory)
    if not _asks_part(text):
        if earlier is None or asked_kind(text) is None:
            return None
        said = set(words_of(earlier.get("reply") or "")) | set(earlier.get("keys") or ())
        named = set(words_of(text)) - PROPERTY_WORDS - NOT_NEW
        if named and not named & said:
            return None
    if mem.left_for_a_blank(memory, text):
        return None
    if RATE.search(text):
        return None
    if not earlier:
        return None
    reply = earlier.get("reply") or ""
    if (COOK_VERB.search(text) and not KEEPS_ASK.search(text)
            and KEEPS_ANSWER.search(reply) and not COOK_VERB.search(reply)):
        return None
    if len(SUM_TABLE.findall(reply)) > 1 and asked_kind(text) == "time":
        return None
    own_named = set(words_of(text)) - PROPERTY_WORDS - NOT_NEW
    earlier_keys = set(earlier.get("keys") or ())
    if own_named and earlier_keys:
        reading = understand(text, memory)
        same_item = [one for one in all_entries() if _key_words(one) == earlier_keys]
        if same_item and own_named & _key_words(same_item[0]):
            fresh = _payload(same_item[0], memory, reading)
            if not (fresh or "").strip() or (
                    flat(fresh) != flat(reply) and own_named & set(words_of(fresh))):
                return None

    named = (set(words_of(text)) - PROPERTY_WORDS - PLACE_WORDS - set(words_of(reply))
             - set(earlier.get("keys") or ()))
    reading = understand(text, memory)
    own = find(reading)
    if own is not None and getattr(own, "id", None) != earlier.get("id"):
        theirs = _key_words(own) - set(earlier.get("keys") or ())
        hit = (set(words_of(text)) - PROPERTY_WORDS) & theirs
        if hit and not (hit & set(words_of(reply))):
            fresh = _payload(own, memory, reading)
            if (isinstance(fresh, str) and fresh.strip()
                    and hit & set(words_of(fresh))):
                return None
        if (hit and asked_kind(text) is None
                and getattr(own, "domain", "") != str(earlier.get("domain") or "")):
            fresh = _payload(own, memory, reading)
            if (isinstance(fresh, str) and fresh.strip() and flat(fresh) != flat(reply)
                    and hit & set(words_of(fresh))):
                return None
    if named:
        if own is not None and named & _key_words(own):
            if getattr(own, "id", None) != earlier.get("id"):
                return None
            fresh = _payload(own, memory, reading)
            if isinstance(fresh, str) and fresh.strip() and flat(fresh) != flat(reply):
                return None
        elif (own is not None and getattr(own, "id", None) != earlier.get("id")
                and _keyed_on_the_line(own, text)):
            fresh = _payload(own, memory, reading)
            if isinstance(fresh, str) and fresh.strip() and flat(fresh) != flat(reply):
                return None
        if (own is not None and getattr(own, "id", None) != earlier.get("id")
                and AMOUNT.search(text) and not AMOUNT.search(reply)
                and _keyed_on_the_line(own, text)):
            return None

        if own is not None and _keyed_on_the_line(own, text):
            mine = getattr(own, "domain", "") or ""
            theirs = str(earlier.get("domain") or "")
            if mine and theirs and mine != theirs:
                return None

    shared = (_key_words(own) & set(earlier.get("keys") or ()) & set(words_of(text))
              if own is not None else set())
    if (shared and getattr(own, "id", None) != earlier.get("id")
            and _keyed_on_the_line(own, text)):
        mine = getattr(own, "domain", "") or ""
        theirs = str(earlier.get("domain") or "")
        if mine and theirs and mine != theirs:
            fresh = _payload(own, memory, reading)
            if (isinstance(fresh, str) and fresh.strip()
                    and flat(fresh) != flat(reply)):
                return None

    same = own if own is not None else find(reading)
    if same is not None and getattr(same, "id", None) == earlier.get("id"):
        named = set(words_of(text)) - PROPERTY_WORDS - PLACE_WORDS - set(words_of(reply))
        if named & _key_words(same) or _figures(text) - _figures(reply):
            fresh = _payload(same, memory, reading)
            if isinstance(fresh, str) and fresh.strip() and flat(fresh) != flat(reply):
                return None
    other = find(understand(text, memory))
    if other is not None and getattr(other, "id", None) != earlier.get("id"):
        newly = set(words_of(text)) - PROPERTY_WORDS - PLACE_WORDS - set(words_of(reply))
        if newly & _key_words(other):
            fresh = _payload(other, memory, understand(text, memory))
            if isinstance(fresh, str) and fresh.strip() and flat(fresh) != flat(reply):
                return None
    if asked_kind(text) == "time" and re.search(r"\bleav(?:e|ing)\b", text):
        for sentence in re.split(r"(?<=[.!?])\s+", reply.strip()):
            if re.match(r"\s*(?:if|unless)\b", sentence, re.I) and re.search(r"\d|\ban?\b", sentence):
                return sentence.strip()
    sized = mem.sized_reply(reply, text, memory, set(earlier.get("keys") or ()))
    if sized:
        return sized
    own_price = find(understand(text, memory))
    if (own_price is not None and getattr(own_price, "id", None) != earlier.get("id")
            and _only_a_figure(narrow(reply, text))):
        return None
    if own_price is not None and getattr(own_price, "id", None) != earlier.get("id"):
        theirs = _key_words(own_price) - set(earlier.get("keys") or ())
        hit = set(words_of(text)) & theirs
        fresh = _payload(own_price, memory, understand(text, memory))
        if (hit and isinstance(fresh, str)
                and _a_figure_apart(narrow(reply, text), fresh)):
            return None
    about = " ".join(str(key) for key in (earlier.get("keys") or ()))
    part = the_part_asked(reply, text, about)
    if not (isinstance(part, str) and part.strip()):
        part = _sentence_naming_the_part(reply, text)
    if isinstance(part, str) and part.strip():
        said = KIND_SAID.get(asked_kind(text))
        if said is not None and not said.search(part):
            part = None
        elif (asked_kind(text) == "time" and not re.search(r"\bbefore\b", text, re.I)
              and A_LEAD_TIME.search(_sentence_with(reply, part) or "")):
            part = None
    if asked_kind(text) == "cause" and isinstance(part, str) and part.strip():
        return _reason_again(_cause_part(part), mem.last_bot(memory) or "")
    return _part_not_repeated(part, mem.entry_answer(memory, text) or reply, memory)


PROPORTION = re.compile(r"\b(?:same weight|same amount|equal|half as much|twice|double\b|"
                        r"three times|two parts|one part)\b|\d", re.I)
MEASURE = re.compile(r"\d|\b(?:mug|mugs|cup|cups|spoon|spoons|teaspoons?|tablespoons?"
                     r"|grams?|kilograms?|kilos?|ml|litres?|liters?|pints?|ounces?|oz"
                     r"|pounds?|handfuls?|pinch(?:es)?)\b", re.I)


_AMOUNT_BEFORE = (r"\d+(?:\.\d+)?\s*(?:g|kg|ml|cl|l|oz|lb|cm)?|one|two|three|four|five|six|"
                  r"seven|eight|nine|ten|eleven|twelve|half|quarter|dozen|mugs?|cups?|spoons?|"
                  r"teaspoons?|tablespoons?|grams?|kilograms?|kilos?|litres?|liters?|pints?|"
                  r"ounces?|pounds?|handfuls?|pinch(?:es)?")
_PROPORTION_PHRASE = (r"same weight|same amount|equal weight|equal amount|half as much|twice|"
                      r"double|three times")


def _amount_for_the_name(clause, named):
    text = " " + re.sub(r"[^a-z0-9. ]+", " ", str(clause).lower()) + " "
    for name in {str(one).lower() for one in named}:
        thing = re.escape(name.rstrip("s")) + r"s?"
        if re.search(r"\b(?:" + _AMOUNT_BEFORE + r")\s+(?:[a-z]+\s+){0,2}" + thing + r"\b",
                     text):
            return True
        if re.search(r"\b(?:" + _PROPORTION_PHRASE + r")\s+(?:[a-z]+\s+){0,3}" + thing
                     + r"\b", text):
            return True
    return False


CLAUSE_SEAM = re.compile(r"(?:(?<=\D)[:,;]|[:,;](?=\D))|\bthen\b")

KIND_SAID = {
    "time": re.compile(r"\d|\b(?:an?|one|two|three|four|five|six|seven|eight|nine|ten|twelve|"
                       r"fifteen|twenty|thirty|forty|fifty|sixty|ninety|hundred)\s+"
                       r"(?:seconds?|secs?|minutes?|mins?|hours?|hrs?|days?|weeks?|months?|years?)\b"
                       r"|\bovernight\b|\ba few (?:hours?|days?|weeks?|months?)\b", re.I),
    "money": re.compile(r"£\s*\d|\b\d[\d,.]*\s*(?:pounds?|quid|dollars?|euros?)\b", re.I),
    "heat": re.compile(r"\d\s*(?:°|degrees?|gas mark|C\b|F\b)", re.I),
    "distance": re.compile(r"\d\s*(?:miles?|km|kilometres?|kilometers?|metres?|meters?|yards?|"
                           r"feet|foot)\b", re.I),
    "clock": re.compile(r"\b\d{1,2}(?:[:.]\d{2})?\s*(?:am|pm|o'clock)\b|\b\d{1,2}[:.]\d{2}\b",
                        re.I),
}
JOINING_WORD = re.compile(r"^\s*(?:which|that|who|whom|whose|where|because|though|although"
                          r"|whereas|while|yet|however|instead|plus|as well)\b", re.I)


def _sentence_naming_the_part(reply, text):
    kind = asked_kind(text)
    if kind is None or kind in ("cause", "order"):
        return None
    named = set(words_of(text)) - PROPERTY_WORDS - NOT_NEW - WHERE_WORDS
    if not named:
        return None
    sentences = [one.strip() for one in SENTENCE.split(str(reply or "").strip()) if one.strip()]
    if not sentences:
        return None
    flat_reply = _flat(reply)
    for sentence in sentences:
        for clause in CLAUSE_SEAM.split(sentence):
            clause = clause.strip(" .,")
            if not clause or not named & set(words_of(clause)):
                continue
            if not _amount_for_the_name(clause, named):
                continue
            if len(clause.split()) < 4 and not re.search(r"\b(?:of|to|per)\b", clause):
                continue
            if JOINING_WORD.match(clause):
                clause = sentence.strip().rstrip(",;: ")
                if len(clause.split()) > 40:
                    continue
            elif clause[0].islower():
                clause = clause[0].upper() + clause[1:]
            part = clause + ("" if clause.endswith((".", "!", "?")) else ".")
            if _flat(part) == flat_reply:
                return None
            return part
    return None


COUNTS_THE_CAUSES = re.compile(
    r"^\s*(?:(?:it|that|this|there)\s+(?:is|are|s)\s+)?"
    r"(?:(?:usually|often|mostly|nearly always|probably)\s+)?"
    r"(?:one|ones|a few|a couple|several|a number|a combination|a mix|many|most|some|two|three|"
    r"a lot|a range|nothing|everything)\b", re.I)
NAMES_NO_CAUSE = frozenset("""cause causes reason reasons usual usually common commonest main
mostly often likely probably real whole only most thing things something anything everything
one ones part parts bit couple few number several combination mix lot lots many some""".split())


def _names_no_cause(head):
    head = str(head or "")
    if COUNTS_THE_CAUSES.match(head):
        return True
    return not (set(keywords(head)) - NAMES_NO_CAUSE)


def _cause_part(part):
    part = str(part or "").strip()
    if ":" not in part:
        return part
    head, tail = part.split(":", 1)
    for candidate in (head, tail):
        if candidate is head and _names_no_cause(head):
            continue
        if CAUSE.search(candidate):
            candidate = candidate.strip().rstrip(",;")
            if candidate and candidate[0].islower():
                candidate = candidate[0].upper() + candidate[1:]
            return candidate + ("" if candidate.endswith((".", "!", "?")) else ".")
    return part


def _reason_again(reason, last):
    reason = str(reason or "").strip()
    match = re.match(r"^(.*?)\b(?:is|are|was|were)\s+(usually|commonly|often)\s+(.+)$",
                     reason, re.IGNORECASE)
    if match:
        short = "{} {}".format(match.group(2).capitalize(), match.group(3))
        if _flat(short) != _flat(reason):
            if _flat(reason) == _flat(last):
                return short
            if _flat(short) == _flat(last):
                return reason
    if _flat(reason) == _flat(last) and re.search(r",\s*so\b", reason, re.I):
        short = re.split(r",\s*so\b", reason, 1, flags=re.I)[0].strip().rstrip(",;")
        short += "" if short.endswith((".", "!", "?")) else "."
        if _flat(short) != _flat(reason):
            return short
    return reason


ASKS_A_MEASURE = re.compile(
    r"\b(?:how\s+(?:much|many|long|often|far|big|old)|when|what\s+time|price|cost|cheapest)\b",
    re.I)
A_MEASURE = re.compile(r"[\d\u00a3$\u20ac]|\b(?:one|two|three|four|five|six|seven|eight|nine|"
                       r"ten|twenty|thirty|forty|fifty|hundred|thousand)\b", re.I)


A_LEAD_TIME = re.compile(
    r"\d[\d.,]*\s*(?:to\s*\d[\d.,]*\s*)?(?:minutes?|mins?|hours?|hrs?)\s+"
    r"(?:before|ahead of)\b", re.I)
ASKS_A_SPAN = re.compile(r"\bhow\s+(?:long|many\s+(?:minutes|hours|days|weeks))\b", re.I)
WHEN_IS_A_CONDITION = re.compile(
    r"\bwhen\s+(?!'s|s\b|\?|should\b|shall\b|do\b|does\b|did\b|will\b|would\b|can\b|could\b|"
    r"is\b|are\b|was\b|were\b|am\b|must\b|to\b)\w+", re.I)
A_WARNING = re.compile(
    r"\b(?:see|speak to|talk to|ring|call|contact|visit|go to)\s+"
    r"(?:a|an|your|the|nhs|111|999)?\s*"
    r"(?:gp|doctor|dentist|midwife|health visitor|pharmacist|a&e|ae|casualty|hospital|"
    r"111|999|out of hours)\b"
    r"|\bget (?:it|them|that) (?:checked|looked at|seen)\b"
    r"|\b(?:urgent|urgently|straight away|same day|a&e|casualty)\b", re.I)


def _asked_figure(text, reply, other_reply):
    if not ASKS_A_MEASURE.search(str(text or "")):
        return ""
    condition = bool(WHEN_IS_A_CONDITION.search(str(text or "")))
    if A_MEASURE.search(str(other_reply or "")):
        return ""
    for sentence in SENTENCE.split(str(reply or "").strip()):
        if not A_MEASURE.search(sentence):
            continue
        if condition and A_WARNING.search(sentence):
            continue
        return sentence.strip()
    return ""


def _the_figure(text, reply):
    return _asked_figure(text, reply, "")


def _sentence_with(reply, part):
    wanted = _flat(part)
    for sentence in same_again.quoted.sentences(reply, SENTENCE):
        if wanted and wanted in _flat(sentence):
            return sentence.strip()
    return ""


def _part_not_repeated(part, whole, memory):
    if not isinstance(part, str) or not part.strip():
        return None
    if _flat(part) != _flat(mem.last_bot(memory) or ""):
        return part.strip()
    whole = whole if isinstance(whole, str) and whole.strip() else part
    if _flat(whole) == _flat(mem.last_bot(memory) or ""):
        return None
    sentence = _sentence_with(whole, part)
    if sentence and _flat(sentence) != _flat(part):
        return sentence
    if _flat(whole) != _flat(part):
        return whole.strip()
    return None


GENERIC_ASK = frozenset("""
long time times minute minutes hour hours day days take takes will start finish
cook cooking bake baking roast roasting boil boiling fry frying grill grilling
""".split())


WHERE_WORDS = frozenset("""
go goes going went gone put puts putting get gets getting set sets use uses using
in into on at for to of with it them they that this there here
""".split())


NOT_NEW = frozenset("""
next again tonight today tomorrow yesterday now soon later still just once twice another other
bit lot lots week weeks month months year years time times future onwards onward
""".split())


def _names_a_property(text):
    return bool(set(keywords(text)) & (PROPERTY_WORDS - GENERIC_ASK))


BARE_ASK = re.compile(r"^\s*(?:so\s+|and\s+|ok\s+|okay\s+)?"
                      r"(?:what|which|where|who|when|how)\b[^?]{0,40}"
                      r"\b(?:see|do|eat|visit|book|buy|pack|take|wear|cook|make|get|try|"
                      r"recommend|suggest|start)\b\s*[?.!]*\s*$", re.IGNORECASE)


def _with_bare_subject(text, memory):
    if not BARE_ASK.match(text):
        return text
    subject = mem.subject(memory)
    if not subject or TIME_WORD.match(subject.strip()):
        return text
    wanted = [word.strip(".,!?;:").lower() for word in subject.split()]
    if any(word in text.lower() for word in wanted):
        return text
    return text.rstrip("?.! ") + " " + subject


def _the_things_to_try(understood, memory):
    things = []
    leans = understood.get("leans_on") if isinstance(understood, dict) else None
    if isinstance(leans, dict):
        for word in leans.get("words") or []:
            if isinstance(word, str) and len(word.strip()) > 2:
                things.append(word.strip().lower())
    ref = understood.get("ref") if isinstance(understood, dict) else None
    if isinstance(ref, dict):
        for word in ("that", "it", "this"):
            value = ref.get(word)
            if isinstance(value, str) and value.strip():
                things.append(value.strip())
                break
    if mem.subject(memory):
        things.append(mem.subject(memory))
    seen, out = set(), []
    for thing in things:
        if thing and thing not in seen:
            seen.add(thing)
            out.append(thing)
    return out


def _the_answer_from_thing(text, thing, memory):
    if not thing:
        return None, None
    fuller = (_with_subject(text, memory) if thing == mem.subject(memory)
              else _with_the_thing(text, thing))
    if fuller.strip() == str(text).strip():
        return None, None
    wider = understand(fuller, memory)
    found, said = _offer(lambda reject: find(wider, reject=reject), memory, wider)
    if found is None or not _is_about(found, thing) or _said_before(said, memory):
        return None, None
    return found, said


def _with_the_thing(text, thing):
    words = str(text).split()
    said = [word.strip(".,!?;:").lower() for word in words]
    if not thing:
        return text
    for i, word in enumerate(said):
        if word in REFERRING:
            words[i] = "the " + thing
            return " ".join(words)
    return text


def _care_holds(text, memory):
    try:
        from ..compose import fallback as composer
        return bool(composer.careful(text, memory))
    except Exception:
        return False


def _named_by(item, subject):
    keys = _key_words(item)
    low = " " + subject.lower() + " "
    phrases = set()
    for part in getattr(item, "key", ()) or ():
        options = (part,) if isinstance(part, str) else part
        for option in options:
            option = str(option).lower().strip()
            if " " in option and option in low:
                phrases.add(option)
    if phrases:
        return True
    subject_keys = set()
    for part in (getattr(item, "key", ()) or ())[:1]:
        options = (part,) if isinstance(part, str) else part
        for option in options:
            for word in str(option).lower().split():
                subject_keys.add(word.rstrip("s") or word)
    if len(low.split()) == 1:
        return bool(subject_keys)
    found = 0
    for word in low.split():
        word = word.strip(".,!?;:").rstrip("s")
        if len(word) > 2 and word in subject_keys:
            found += 1
    return found >= 2


def _the_answer_was_about_the_subject(memory):
    subject = str(mem.subject(memory) or "").lower()
    if not subject:
        return False
    last = memory.get("entry_answer")
    keys = getattr(last, "get", lambda *_: None)("keys") if isinstance(last, dict) else None
    if not keys:
        return True
    words = {word.strip(".,!?;:").rstrip("s") for word in subject.split()}
    return bool(words & {str(key).lower().rstrip("s") for key in keys})


ADDING_TO_THE_SUBJECT = re.compile(
    r"^\s*(?:and\s+)?(?:what|how)\s+about\b|^\s*(?:and\s+)?what\s+if\b|"
    r"^\s*and\s+(?:for|at|on|with|in)\b", re.IGNORECASE)
A_MEASURE_OF_THE_SUBJECT = re.compile(
    r"^\s*(?:and\s+)?(?:what|how)\s+about\s+(?:a|an|one|two|three|four|\d+)?\s*"
    r"(?:bowl(?:ful)?|cup(?:ful)?|plate(?:ful)?|mug(?:ful)?|glass(?:ful)?|servings?|portions?|"
    r"slices?|pieces?|handfuls?|spoons?|spoonfuls?|tablespoons?|teaspoons?)\b", re.IGNORECASE)

GENERIC = {"should", "would", "could", "how", "what", "when", "where", "which", "about", "tomorrow",
           "today", "tonight", "them", "they", "have", "need", "want", "much", "many", "does",
           "did", "will", "this", "that", "there", "then", "with", "your", "mine", "some",
           "thing", "things", "please", "thanks", "maybe", "really", "also", "just", "like"}


_HOURS_AND_MINUTES = re.compile(
    r"\b(\d+)\s*(?:hours?|hrs?)\s*(\d+)\s*(?:minutes?|mins?)", re.I)


def _minutes_in(text):
    if not isinstance(text, str) or not text:
        return []
    stated = _HOURS_AND_MINUTES.sub(
        lambda m: "%d minutes" % (int(m.group(1)) * 60 + int(m.group(2))), text)
    found = []
    for match in re.finditer(
            r"\b(\d+)(?:\s*(?:to|-|\u2013)\s*(\d+))?\s*(minutes?|mins?|hours?|hrs?)\b",
            stated, re.I):
        unit = 60 if match.group(3).lower().startswith(("h",)) else 1
        low = int(match.group(1)) * unit
        high = int(match.group(2) or match.group(1)) * unit
        found.append((low, high))
    return found


def _a_figure_apart(mine, theirs):
    mine_spans = _minutes_in(mine)
    their_spans = _minutes_in(theirs)
    if not mine_spans or not their_spans:
        return False
    return any(high_other < low or high < low_other
               for low, high in mine_spans for low_other, high_other in their_spans)


def _only_a_figure(part):
    if not isinstance(part, str) or not part.strip():
        return False
    words = words_of(part)
    return bool(re.search(r"[\u00a3$\u20ac]|\bpounds?\b|\bquid\b", part)) and len(words) <= 6


FIGURE = re.compile(r"\d[\d,]*(?:\.\d+)?")


def _figures(text):
    return {one.replace(",", "") for one in FIGURE.findall(str(text or ""))}


_NAME_WORDS = None
_NAME_DOMAINS = {}
FEW_ENTRIES = 12


WHEN_NOT_A_THING = frozenset("""
until till since while during before after within ago
""".split())


def _name_words():
    global _NAME_WORDS
    if _NAME_WORDS is None:
        counted = {}
        domains = {}
        try:
            for one in all_entries():
                field = getattr(one, "domain", None)
                for word in _key_words(one):
                    counted[word] = counted.get(word, 0) + 1
                    if field:
                        domains.setdefault(word, set()).add(field)
        except Exception:
            counted = {}
            domains = {}
        _NAME_WORDS = {word for word, seen in counted.items() if seen <= FEW_ENTRIES}
        _NAME_DOMAINS.clear()
        _NAME_DOMAINS.update({word: domains.get(word, set()) for word in _NAME_WORDS})
    return _NAME_WORDS


def _filler(word):
    if word in GENERIC or word in mem.topics.STOPWORDS or word in NOT_NEW:
        return True
    if word in PROPERTY_WORDS or word in WHEN_NOT_A_THING:
        return True
    for tail in ("re", "ve", "ll", "d", "m"):
        if word.endswith(tail) and word[:-len(tail)] in mem.topics.STOPWORDS:
            return True
    return False


def _left_out(item, text):
    keys = _key_words(item)
    names = _name_words()
    for word in re.findall(r"[a-z']+", str(text or "").lower()):
        word = word.rstrip("'")
        if len(word) < 4 or _filler(word):
            continue
        bare = word.rstrip("s") or word
        if bare in keys or word in keys:
            continue
        if bare in names or word in names:
            field = getattr(item, "domain", None)
            if not any(field in _NAME_DOMAINS.get(form, ()) for form in (word, bare)):
                return True
    return False


def _keyed_on_the_line(item, text):
    keys = _key_words(item)
    for word in re.findall(r"[a-z']+", str(text).lower()):
        if len(word) < 3 or word in GENERIC or word in NOT_NEW or word in PROPERTY_WORDS:
            continue
        if (word.rstrip("s") or word) in keys:
            return True
    return False


def _shares_a_word(item, subject):
    keys = _key_words(item)
    for word in subject.lower().split():
        word = word.strip(".,!?;:")
        if len(word) > 2 and (word.rstrip("s") or word) in keys:
            return True
    return False


FIGURE_ASKS = ("money", "amount", "time", "clock", "heat", "distance", "pressure")


def _answers_the_figure(text, reply):
    if not isinstance(reply, str) or not reply.strip():
        return True
    kind = asked_kind(text)
    if kind not in FIGURE_ASKS:
        return True
    wanted = {kind}
    if kind in ("amount", "money"):
        wanted.add("money")
    for one in wanted:
        pattern = SIGNALS.get(one)
        if pattern is not None and pattern.search(reply):
            return True
    return False


SAY_IT = re.compile(
    r"\bhow (?:do|should|can|could|would) i (?:raise|broach|word|phrase|put)"
    r"\s+(?:it|this|that|the subject|the issue)\b"
    r"|\bhow (?:do|should|can|could|would) i (?:say|tell)\b(?!\s+(?:if|whether|the difference"
    r"|when|what))"
    r"|\bbring (?:it|this|that) up\b|\bbroach (?:it|this|that)\b"
    r"|\bwithout sounding\b|\bnot sounding\b|\bnot wanting to sound\b"
    r"|\bwithout (?:being|coming across|upsetting|offending|hurting)\b"
    r"|\bwhat (?:should|do) i say to\b",
    re.IGNORECASE)


def _asks_how_to_say_it(text):
    return bool(SAY_IT.search(text or ""))


def _in_the_subjects_field(item, subject):
    field = (understand(subject) if subject else {}).get("topic")
    if not field:
        return True
    return getattr(item, "domain", None) == field

_ASKING_ONLY = frozenset("""how much many long far often soon old big large small hot cold warm
fast slow quick heavy light high deep thick thin wide tall low early late few more less most least
time times cost costs price worth take takes last lasts
do does did can could would should shall will may might must need needs want wants
get gets got make makes made use uses using put
i me my we our you your a an the it its that this they them there
and or but for of to in on at with from about than then too also just really very
good nice best better worse right wrong new
one ones thing things kind type sort way part bit
lol lmao haha hahaha hmm hm mmm ah oh yeah yep ok okay
today tomorrow tonight week weekend month year day night morning evening
away around back down up out over any some all
""".split())


def _own_thing_words(text, memory):
    understood = understand(text, memory)
    subject = str(mem.subject(memory) or "").lower()
    out = []
    for word in understood.get("keywords") or []:
        low = str(word).lower()
        if low in _ASKING_ONLY or low in subject or low.isdigit() or len(low) < 3:
            continue
        out.append(low)
    return tuple(out)


def _about_the_talk(item, text, memory, reading):
    read = (memory or {}).get("understood") if isinstance(memory, dict) else None
    if isinstance(read, dict) and read.get("change_of_subject"):
        return True
    subject = mem.subject(memory)
    record = mem.current(memory)
    if not isinstance(record, dict) or record.get("turn") == len(memory.get("turns") or []):
        return True
    thing = _head_thing(subject)
    if not thing:
        return True
    if _is_about(item, thing):
        return True
    turns = memory.get("turns") if isinstance(memory, dict) else None
    if not turns:
        return True
    if _names_the_entry(text, item):
        return True
    if _a_definition_of_the_entry(text, item):
        return True
    if _names_the_thing_apart_from_the_talk(item, text, subject, reading):
        return True
    if _a_why_line_that_names(item, reading):
        return True
    if _the_field_on_the_screen(item, text, reading, memory):
        return True
    if _says_the_ask_whole(text, item):
        return True
    if _names_its_own_thing(text, memory) and _agrees_with_its_own_field(item, reading):
        return True
    return about_the_topic(item, reading)


def _agrees_with_its_own_field(item, reading):
    if getattr(item, "topic", None) is None:
        return True
    return about_the_topic(item, reading)


def _the_field_on_the_screen(item, text, reading, memory):
    if not isinstance(reading, dict) or reading.get("kind") != "question":
        return False
    last = memory.get("last_answer") if isinstance(memory, dict) else None
    domain = str(last.get("domain") or "") if isinstance(last, dict) else ""
    if not domain or domain != str(getattr(item, "domain", "") or ""):
        return False
    if _last_turn_answered_from_the_field(memory):
        return False
    return _says_a_subject_phrase(item, text)


def _last_turn_answered_from_the_field(memory):
    if not isinstance(memory, dict):
        return False
    turns = memory.get("turns")
    if not isinstance(turns, list) or not turns:
        return False
    last = memory.get("last_answer")
    reply = last.get("reply") if isinstance(last, dict) else last
    said = turns[-1].get("bot") if isinstance(turns[-1], dict) else None
    if not isinstance(reply, str) or not isinstance(said, str):
        return False
    return _same_answer(reply, said)


def _says_a_subject_phrase(item, text):
    key = getattr(item, "key", ()) or ()
    if not key:
        return False
    first = key[0]
    said = " " + " ".join(re.findall(r"[a-z0-9']+", str(text or "").lower())) + " "
    for option in (first if not isinstance(first, str) else (first,)):
        phrase = " ".join(str(option).lower().split())
        if " " in phrase and (" " + phrase + " ") in said:
            return True
    return False


OPENS_WITH_AN_AUXILIARY = frozenset(
    "is are was were can could should do does did will would".split())

NAMING = re.compile(
    r"\b(?:a|an|the|another|my|our|your|his|her|their|this|that|these|those|one|two|three)\s+"
    r"((?:[a-z-]+[\s,]+){1,3}|[a-z-]+)")


def _names_the_entry(text, item):
    first = getattr(item, "key", ()) or ()
    things = first[0] if first and not isinstance(first[0], str) else ()
    heads = set()
    for option in things:
        words = str(option).lower().split()
        if words:
            heads.add(words[-1].rstrip("s") or words[-1])
    if not heads:
        return False
    for found in NAMING.finditer(" ".join(str(text or "").lower().split())):
        for word in re.findall(r"[a-z-]+", found.group(1)):
            if word.rstrip("s") in heads:
                return True
    said = " ".join(str(text or "").lower().split())
    mine = said.split()
    for _ in range(2):
        if mine and mine[0] in OPENS_WITH_AN_AUXILIARY:
            mine = mine[1:]
    for word in re.findall(r"[a-z-]+", " ".join(mine[:2])):
        if word.rstrip("s") in heads:
            return True
    return False


DEFINITION_WORD_AT = 6


def _a_definition_of_the_entry(text, item):
    words = [word.strip(".,!?;:") for word in
             (" ".join(str(text or "").lower().split())).split()]
    if not words or len(words) > DEFINITION_WORD_AT + 1:
        return False
    first = getattr(item, "key", ()) or ()
    things = first[0] if first and not isinstance(first[0], str) else ()
    subject = set()
    for option in things:
        for word in str(option).lower().split():
            subject.add(word.rstrip("s") or word)
    if not subject:
        return False
    for at, word in enumerate(words):
        if (word.rstrip("s") or word) not in subject:
            continue
        before = words[:at]
        if not before or not any(one in EXPLAIN_LEADS for one in before):
            continue
        if all(one in EXPLAIN_FILLER for one in before):
            return True
    return False


HANDOVER_FILLER = frozenset("""
a an the some any another one more then now again please pls just
so ok okay and but also even really
""".split())


def _says_the_ask_whole(text, item):
    said = [word for word in WORD.findall(str(text or "").lower())
            if word not in HANDOVER_FILLER]
    if len(said) < 2:
        return False
    for part in getattr(item, "key", ()) or ():
        options = (part,) if isinstance(part, str) else part
        for option in options:
            phrase = [word for word in WORD.findall(str(option).lower())
                      if word not in HANDOVER_FILLER]
            if len(phrase) >= 2 and phrase == said:
                return True
    return False


def _a_why_line_that_names(item, reading):
    if not isinstance(reading, dict) or "why" not in (reading.get("asks") or ()):
        return False
    return names_its_own_subject(item, reading)


def _names_the_thing_apart_from_the_talk(item, text, subject, reading):
    if not isinstance(reading, dict) or reading.get("kind") != "question":
        return False
    if not names_its_own_subject(item, reading):
        return False
    said = said_topic.words(text)
    if not said:
        return False
    if not _is_about(item, said[-1]):
        return False
    if PRONOUN_OBJECTS.intersection(WORD.findall(str(text or "").lower())):
        return False
    thing = _head_thing(subject)
    if not thing:
        return False
    words = {word.rstrip("s") or word for word in WORD.findall(str(text or "").lower())}
    return (thing.rstrip("s") or thing) not in words


CHOICE_KINDS = frozenset("""film films movie movies series show shows programme programmes
    book books novel novels game games music song songs album albums meal meals dinner food
    recipe recipes takeaway takeaway""".split())


def _a_choice_with_one_thing_left_out(text):
    flat_words = set(re.findall(r"[a-z']+", " ".join(str(text or "").split()).lower()))
    if not flat_words & CHOICE_KINDS:
        return False
    return bool(_refused(text))


THING_AFTER = frozenset("""a an the my your our their his her this that these those another
    any some every each""".split())
AFTER_A_PLACE = frozenset("""in on at into inside onto unto under underneath near by through
    across behind beside below above outside around round aboard throughout within past
    toward towards via along off upon""".split())
NO_THING_NAMED = frozenset("""idea ideas point points sense question questions matter deal
    problem problems chance chances clue guess guesses example examples option options choice
    choices answer answers lot lots bit bits time times while moment minute second hour day days
    week weeks month months year years difference change reason reasons dangerous risky noisy
    pricey dodgy faulty broken safe spare fortune mint bomb packet ton
    man men woman women person people guy guys lady ladies bloke child kid adult teenager""".split())
_AUXILIARY = frozenset("""wont cant doesnt dont didnt isnt wasnt arent shouldnt wouldnt couldnt
    mustnt will would can could should may might must shall do does did have has had be been
    being is are was were am""".split())
_ADJECTIVE_ENDINGS = ("ous", "ful", "less", "able", "ible", "ive", "ish", "ary")
ASKS_A_QUANTITY = re.compile(r"\bhow (?:much|many)\b|\bhow (?:long|far|often)\b", re.I)


def _describes_the_thing(word):
    if word in NO_THING_NAMED:
        return True
    return any(word.endswith(ending) and len(word) > len(ending) + 2
               for ending in _ADJECTIVE_ENDINGS)


DESCRIBES_ONE = frozenset("""new old another different same other else more less much many few
    lot lots best better worse easiest hardest first second last next right wrong kind sort type
    way ways thing things stuff one ones bit bits worth safe ok okay normal bad legal possible
    fine allowed hard easy too still someone something anything everything nothing everyone
    everybody nobody anybody""".split())


def _said_in_the_talk(memory):
    said = set()
    for turn in (memory or {}).get("turns") or []:
        if not isinstance(turn, dict):
            continue
        for side in ("user", "bot"):
            said.update(WORD.findall(str(turn.get(side) or "").lower()))
    return said


def _already_in_the_talk(word, said):
    if not said:
        return False
    if word in said or word + "s" in said:
        return True
    if word.endswith("s") and word[:-1] in said:
        return True
    return any(one.startswith(word) for one in said)


def _names_its_own_thing(text, memory=None):
    said = _said_in_the_talk(memory) if memory is not None else set()
    if ASKS_A_QUANTITY.search(str(text or "")):
        return False
    words = re.findall(r"[a-z0-9']+", str(text or "").lower())
    for index, word in enumerate(words):
        if re.fullmatch(r"\d+(?:s|st|nd|rd|th)?", word):
            continue
        if word in DESCRIBES_ONE or word in kinds.VERB_FORMS or word in _AUXILIARY:
            continue
        if word.endswith("e") and word[:-1] + "ing" in DESCRIBES_ONE:
            continue
        if _describes_the_thing(word):
            continue
        if any(word in ("one", "ones") for word in words[index + 1:index + 3]):
            continue
        if _already_in_the_talk(word, said):
            continue
        before = words[max(0, index - 2):index]
        if before[-1:] and before[-1] in THING_AFTER:
            if len(before) == 2 and before[0] in AFTER_A_PLACE:
                continue
            return True
        if (len(before) == 2 and before[0] in THING_AFTER
                and before[1] not in THING_AFTER
                and before[1] not in _AUXILIARY
                and not _describes_the_thing(before[1])):
            return True
    return False


def _the_topic_rules_it_out(item, memory):
    topic = mem.topics.topic_text(memory) if isinstance(memory, dict) else ""
    if not topic:
        return False
    return bool(mem.topics.keeps_away(topic, topic, item))


def _in_context(text, memory, reject=None):
    subject = mem.subject(memory)
    thing = _head_thing(subject)
    refused = _refused(text)
    if refused:
        inner = reject
        reject = (lambda one: _hands_back_the_refusal(one, refused)
                  or (inner is not None and inner(one)))
    understood = memory.get("understood")
    if not isinstance(understood, dict):
        understood = understand(text, memory)
    if understood.get("intent") == "ack":
        return None
    if _asks_how_to_say_it(text):
        return None
    if not leans_on_a_subject(understood):
        return None
    if _names_its_own_thing(text, memory):
        return None
    fuller = _with_subject(text, memory)
    if fuller.strip() == text.strip() and not _own_thing_words(text, memory):
        fuller = _about_subject(text, memory)
    if fuller.strip() == text.strip():
        fuller = _with_bare_subject(text, memory)
        for rewrite, added, domain in _qualifier_rewrites(text, memory):
            item = _from_rewrite(rewrite, text, memory, reject, added, domain)
            if item is not None:
                if _hands_back_the_refusal(item, _refused(text)):
                    continue
                return item
    if (fuller.strip() == text.strip()
            and _the_answer_was_about_the_subject(memory)
            and (not _own_thing_words(text, memory) or ADDING_TO_THE_SUBJECT.match(text))):
        skip = set()
        after_used = False
        for fuller in _subject_tails(text, memory, understand(text, memory)):
            reading = understand(fuller, memory)
            after_used = False
            while True:
                item = find(reading, reject=lambda one: one.id in skip
                            or (reject is not None and reject(one)))
                if item is None:
                    break
                skip.add(item.id)
                if not _named_by(item, subject):
                    continue
                if thing and not _is_about(item, thing):
                    continue
                reply = _payload(item, memory, reading)
                if not reply.strip():
                    continue
                if _said_before(reply, memory):
                    after_used = True
                    continue
                if not _answers_the_figure(text, reply):
                    return None
                if after_used and not _keyed_on_the_line(item, text):
                    return None
                if _left_out(item, text):
                    return None
                if _the_topic_rules_it_out(item, memory):
                    return None
                return item
        return None
    if not fuller or fuller.strip() == text.strip():
        return None
    reading_here = understand(fuller, memory)
    inner = reject
    want = thing or subject
    fits = lambda one: _is_about(one, want) and about_the_topic(one, reading_here)
    about = lambda one: _is_about(one, subject) and about_the_topic(one, reading_here)
    strict = (lambda one: not fits(one) or (inner is not None and inner(one)))
    loose = (lambda one: not about(one) or (inner is not None and inner(one)))
    item = find(reading_here, reject=loose)
    if item is None or not _in_the_subjects_field(item, subject):
        better = find(reading_here, reject=strict)
        if better is not None and (item is None or _in_the_subjects_field(better, subject)):
            item = better
    if item is None:
        return None
    own = None if mem.KIND_ASK.search(text) else _own_thing(understand(text, memory))
    if own and not _is_about(item, own):
        return None
    if _left_out(item, text):
        return None
    reply = item.reply
    if isinstance(reply, (list, tuple)) or callable(reply):
        held = reading_here
        if _said_before(_payload(item, memory, reading_here), memory):
            here = understand(text, memory)
            own_words = _payload(item, memory, here)
            if own_words.strip() and not _said_before(own_words, memory):
                held = here
        return item, held
    if _said_before(reply, memory):
        return None
    if not _answers_the_figure(text, reply):
        return None
    return item, reading_here


def _from_rewrite(fuller, text, memory, reject, added="", domain=None):
    item = find(understand(fuller, memory), reject=reject)
    if item is None:
        return None
    if domain is not None and item.domain != domain:
        return None
    if not (_is_about(item, mem.subject(memory)) or (added and _is_about(item, added))):
        return None
    own = _own_thing(understand(text, memory))
    if own and not _is_about(item, own):
        return None
    reply = item.reply
    if isinstance(reply, (list, tuple)) or callable(reply):
        return item
    if _said_before(reply, memory):
        return None
    return item

KEEPS = re.compile(r"\b(?:keep|keeps|keeping|fridge|freezer|freeze|lasts?)\b", re.I)
FIGURE = re.compile(r"\b(?:\d+|a|an|one|two|three|four|five|six|seven|eight|nine|ten|a couple of|a few)"
                    r"(?:\.\d+)?\s*(?:-|to\s+\d+\s*)?(?:hour|hours|day|days|week|weeks|month|"
                    r"months|year|years)\b", re.I)
_NOT_THE_FRIDGE = re.compile(
    r"\b(?:never\s+(?:in\s+)?the\s+fridge|not\s+(?:in\s+)?the\s+fridge|out\s+of\s+the\s+fridge"
    r"|room\s+temperature|dry,\s+dark|in\s+a\s+cupboard|in\s+the\s+cupboard)\b", re.I)


STORING = frozenset("""
store stores stored storing keep keeps kept keeping
""".split())


def _asks_storing(memory):
    words = (mem.subject(memory) or "").split()
    return bool(words) and words[0] in STORING


def _keeping_thing(memory):
    words = (mem.subject(memory) or "").split()
    while words and (words[0] in STORING or words[0].rstrip("s") in STORING):
        words.pop(0)
    return " ".join(words)


def _the_plan_keeps(understood, memory):
    if not isinstance(understood, dict) or not isinstance(memory, dict):
        return None
    words = {str(word).lower() for word in (understood.get("words") or ())}
    if dishes.ask_kind(understood) != "keep" or not words & {"it", "that", "this", "them", "they"}:
        return None
    if _own_thing(understood):
        return None
    return dishes.follow_up(memory, understood)


def _keeping_entry(text, memory, thing=None, storing=False):
    fuller = _with_subject(text, memory, thing)
    if fuller.strip() == text.strip():
        fuller = _about_subject(text, memory)
    if fuller.strip() == text.strip():
        return None
    reading = understand(fuller, memory)
    item = find(reading)
    if item is None or not _is_about(item, mem.subject(memory)):
        return None
    reply = _reply_of(item, reading, memory)
    if not isinstance(reply, str) or not reply.strip():
        return None
    said_already = bool(storing and _said_before(reply, memory))
    if not KEEPS.search(reply) and not said_already:
        return None
    subject = mem.subject(memory)
    if subject and len(cooking.ingredients(understand(subject, memory))) > 1:
        return None
    if said_already:
        figures = [part.strip() for part in SENTENCE.split(reply) if FIGURE.search(part)]
        if figures:
            return " ".join(figures)
    return reply


def _in_this_conversation(reject, reading):
    def veto(item):
        if not about_the_topic(item, reading):
            return True
        return bool(reject is not None and reject(item))
    return veto


def _in_bare_context(text, memory, reject=None):
    if _names_its_own_thing(text, memory):
        return None
    fuller = _with_bare_subject(text, memory)
    if fuller.strip() == text.strip():
        return None
    reading = understand(fuller, memory)
    item = find(reading, reject=_in_this_conversation(reject, reading))
    if item is None or not _is_about(item, mem.subject(memory)):
        return None
    reply = getattr(item, "reply", None)
    if not (isinstance(reply, (list, tuple)) or callable(reply)):
        if _said_before(reply, memory):
            return None
    return item, reading


def _reply_of(item, reading, memory):
    reply = getattr(item, "reply", None)
    if callable(reply):
        try:
            reply = reply(memory, reading)
        except Exception:
            return ""
    elif isinstance(reply, (list, tuple)):
        reply = " ".join(one for one in reply if isinstance(one, str))
    return reply if isinstance(reply, str) else ""


A_FIGURE = re.compile(r"\d|\b(?:one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve)\b",
                      re.I)


NUMBER_IN_TEXT = re.compile(r"\d+(?:\.\d+)?")


def _figures_of(said):
    return set(NUMBER_IN_TEXT.findall(flat(said or "")))


def _new_figure(fresh, before):
    return bool(_figures_of(fresh) - _figures_of(before))


def _adds_a_figure(text):
    said = flat(text)
    if not said or "?" in said:
        return False
    return bool(A_FIGURE.search(said))


A_PUT_RIGHT = re.compile(r"\b(?:make\s+(?:it|that|them)|instead|rather\s+than|i\s+meant|no\s+wait|"
                         r"change\s+(?:it|that|them)|put\s+(?:it|that)\s+(?:to|up|down)|"
                         r"bump\s+(?:it|that)|let'?s\s+say)\b", re.I)


def _a_figure_put_right(text):
    text = str(text or "")
    return bool(A_PUT_RIGHT.search(text) and re.search(r"\d", text))


def _without_the_figures(line):
    return " ".join(re.sub(r"[£$]?\b\d[\d,.]*\b", "", str(line or "")).split())


def _the_entry_asked_again(text, memory):
    record = _last_answer(memory)
    if not record:
        return None
    entry_id = record.get("id")
    if not entry_id:
        return None
    item = None
    for candidate in all_entries():
        if getattr(candidate, "id", None) == entry_id:
            item = candidate
            break
    if item is None:
        return None
    turns = memory.get("turns")
    turn = record.get("turn")
    if not isinstance(turns, list) or not isinstance(turn, int) or not 0 <= turn < len(turns):
        return None
    said = turns[turn] if isinstance(turns[turn], dict) else {}
    line = str(said.get("user") or "").strip()
    if not line:
        return None
    earlier = _without_the_figures(line) if _a_figure_put_right(text) else line
    reading = understand(earlier + " " + text, memory)
    fresh = _payload(item, memory, reading)
    if not isinstance(fresh, str) or not fresh.strip():
        return None
    if flat(fresh) == flat(record.get("reply") or ""):
        return None
    new_part = _the_part_a_longer_variant_adds(fresh, record.get("reply"))
    if new_part is not None:
        return new_part
    return fresh


def _the_part_a_longer_variant_adds(fresh, said):
    said = flat(said)
    mine = flat(fresh)
    if not said or not mine.startswith(said):
        return None
    rest = mine[len(said):]
    if not rest.startswith(" "):
        return None
    words = len(said.split())
    added = " ".join(str(fresh).split()[words:]).strip()
    if len(added.split()) < 3:
        return None
    return added


def _payload(item, memory, reading):
    reply = getattr(item, "reply", None)
    if callable(reply):
        reply = reply(memory, reading)
    elif isinstance(reply, (list, tuple)):
        reply = pick(reply, memory)
    return reply if isinstance(reply, str) else ""


def _the_sentence_owed(text, reply, memory):
    understood = memory.get("understood") if isinstance(memory, dict) else None
    if not isinstance(understood, dict):
        return None
    try:
        item = find(understood)
    except Exception:
        return None
    if item is None or not getattr(item, "lead", None):
        return None
    said = getattr(item, "reply", None)
    if not isinstance(said, str):
        try:
            said = _payload(item, memory, understood)
        except Exception:
            return None
    plain = " ".join(str(said or "").split())
    here = " ".join(str(reply or "").split())
    if not plain or not here:
        return None
    at = here.find(plain[:50])
    if at != 0:
        return None
    return item.lead


STAND_IN_WORDS = frozenset("""
substitute substitutes substitution swap swaps swapping replace replaces replacing replacement
""".split())
STAND_IN_PHRASES = ("what can i use", "what do i use", "what should i use", "what else can i use",
                    "what can i substitute", "in place of",
                    "instead", "what can i have", "what could i have", "what else can i have",
                    "leave it out", "leave them out", "leave out", "skip it")


STAND_IN_TARGET = re.compile(r"\b(?:instead of|in place of|substitute for|swap (?:it )?for)\b",
                             re.I)


def _wants_a_stand_in(reading):
    if not isinstance(reading, dict):
        return False
    clean = " ".join(str(reading.get("clean") or "").split()).lower()
    if not clean or STAND_IN_TARGET.search(clean):
        return False
    asked = any(phrase in clean for phrase in STAND_IN_PHRASES)
    if not asked:
        words = reading.get("words")
        if not isinstance(words, (list, tuple)):
            words = clean.split()
        asked = any(str(word).lower() in STAND_IN_WORDS for word in words)
    if not asked:
        return False
    return bool(REFUSE_OPEN.match(clean) or REFUSE_WISH.match(clean)) \
        and not REFUSE_CHOICE.match(clean)


def _a_swap_row(item):
    return str(getattr(item, "id", "") or "").startswith("swap-")

PRICE_LIMIT = re.compile(
    r"\b(?:under|below|less than|no more than|not more than|up to|max(?:imum)?(?: of)?|"
    r"budget(?: of| is| around| about)?|spend(?: up to)?)\s*\u00a3?\s*(\d{1,4})(?:\.\d\d?)?\b",
    re.IGNORECASE)
PRICE_NOT_OVER = re.compile(
    r"\b(?:nothing|not|no|nowt)\s+(?:more\s+than|over|above|past)\s*\u00a3?\s*(\d{1,4})(?:\.\d\d?)?\b",
    re.IGNORECASE)
PRICE_BARE = re.compile(r"\b(\d{1,4})(?:\.\d\d?)?\s*(?:pounds?|quid|\u00a3)\b",
                        re.IGNORECASE)
PRICE_OVER = re.compile(r"\b(?:over|above|more\s+than|past)\s*\u00a3?\s*(\d{1,4})(?:\.\d\d?)?\b",
                        re.IGNORECASE)
PRICE_WORDS = (("a tenner", 10), ("tenner", 10), ("a fiver", 5), ("fiver", 5))
CHEAPER = re.compile(r"\b(?:cheaper|more affordable|less expensive)\b", re.IGNORECASE)
LIMIT_SHAPE = re.compile(r"\d|\btenner\b|\bfiver\b|\bcheaper\b|affordable", re.IGNORECASE)
LIMIT_ONLY = frozenset("""
    nothing not no over above more than nowt
    what about anything something cheaper cheap please then so ok okay could we go bit a an the is
    my budget max maximum under below less than more no not up to spend pounds pound quid tenner
    fiver that this it for on do i can you any if but else maybe just around roughly sort kind of
    thing things price prices cost costs money how much will would should get buy gets go for
    """.split())
INTEREST_ALIASES = {"garden": "gardening", "plants": "gardening", "allotment": "gardening",
                    "tackle": "fishing", "angling": "fishing", "fish": "fishing",
                    "books": "reading", "book": "reading"}


def _price_limit(text):
    if not isinstance(text, str) or not text.strip():
        return None, False
    flat = " ".join(text.lower().split())
    cheaper = bool(CHEAPER.search(flat))
    if (PRICE_OVER.search(flat) and not PRICE_NOT_OVER.search(flat)
            and not PRICE_LIMIT.search(flat)):
        return None, cheaper
    match = PRICE_NOT_OVER.search(flat) or PRICE_LIMIT.search(flat) or PRICE_BARE.search(flat)
    if match:
        try:
            return int(float(match.group(1))), cheaper
        except (TypeError, ValueError):
            return None, cheaper
    for phrase, amount in PRICE_WORDS:
        if phrase in flat:
            return amount, cheaper
    return None, cheaper


GIFT_WORD = re.compile(r"\b(?:present|presents|gift|gifts)\b")


def _only_a_limit(text):
    words = [word for word in WORD.findall(" ".join(str(text or "").lower().split()))
             if not word.isdigit()]
    return bool(words) and all(word in LIMIT_ONLY for word in words)


def _a_gift_entry(reading):
    item = find(reading)
    return item if str(getattr(item, "id", "")).startswith("gift-") else None


def _a_gift_just_answered(memory):
    turns = memory.get("turns") if isinstance(memory, dict) else None
    if not isinstance(turns, list):
        return None
    for turn in reversed(turns[-3:]):
        said = str((turn or {}).get("user") or "") if isinstance(turn, dict) else ""
        if not said:
            continue
        item = _a_gift_entry(understand(said, memory))
        if item is not None:
            return item
    return None


def _asks_what_to_give(reading):
    from ..understanding import topics as present_reading
    return present_reading.gift_ask(reading)


def _the_interests(text, memory, item):
    from ..knowledge import shopping
    said = []
    lines = []
    turns = memory.get("turns") if isinstance(memory, dict) else None
    if isinstance(turns, list):
        lines = [str((turn or {}).get("user") or "") for turn in turns[-3:]
                 if isinstance(turn, dict)]
    for line in lines + [str(text or "")]:
        for word in WORD.findall(line.lower()):
            name = INTEREST_ALIASES.get(word, word)
            if name in shopping.INTEREST_GIFTS and name not in said:
                said.append(name)
    if said:
        return said
    for part in getattr(item, "key", ()) or ():
        for word in (part if isinstance(part, (list, tuple, set)) else (part,)):
            name = INTEREST_ALIASES.get(str(word).lower(), str(word).lower())
            if name in shopping.INTEREST_GIFTS and name not in said:
                said.append(name)
    return said


def _the_entry_reply(item, memory, reading):
    reply = getattr(item, "reply", None)
    try:
        said = reply(memory, reading) if callable(reply) else reply
    except Exception:
        return ""
    return said if isinstance(said, str) else ""


def _the_present_with_a_price(text, reading, memory):
    money, cheaper = _price_limit(text)
    if money is None and not cheaper:
        return None
    item = _a_gift_entry(reading)
    if item is not None and "\u00a3" in _the_entry_reply(item, memory, reading):
        return None
    only_a_limit = _only_a_limit(text)
    interests = _the_interests(text, memory, item)
    if item is None:
        if only_a_limit:
            item = _a_gift_just_answered(memory)
            if item is None:
                return None
        elif not GIFT_WORD.search(str(text or "").lower()) \
                and not (interests and _asks_what_to_give(reading)):
            return None
    if item is not None and not only_a_limit and not interests \
            and str(getattr(item, "id", "")) != "gift-generic":
        return None
    from ..knowledge import shopping
    if money is None:
        return shopping.present_less(interests)
    return shopping.present_within(money, interests)

_HOW_TO_SHAPES = (r"\bhow\s+(?:do|can|should|would|could|to)\b|\bhow to\b"
                r"|\bwhat\s+(?:do|can|should|shall)\s+i\s+do\s+about\s+(?:my|our|the|this|that)\b")
HOW_TO = re.compile(_HOW_TO_SHAPES)

MONEY_SAID = re.compile(
    r"£|\$|€|\bquid\b|\bpounds?\b|\bcosts?\b|\bcosting\b|\bprice[ds]?\b|\bpric(?:ey|ier)\b"
    r"|\bexpensive\b|\bcheap(?:er|est)?\b|\bfree\b|\bcharges?\b|\bfees?\b|\bpay\b"
    r"|\b\d+\s?(?:p|quid|pence)\b", re.I)
PRICE_FILLER = frozenset("""
roughly approximately approx about around maybe usually normally possibly just exactly to for it
that this them those be is are was were do does did would will should can could i you we they he
she my our me us a an the
""".split())
PRICE_VERBS = frozenset("""
fix repair replace get buy hire rent install book cost costs charge pay spend make do take put
sort service deliver fit mend
""".split())


def _asks_a_price(text):
    low = flat(text)
    if re.search(r"\bhow much (?:does|do|is|are|will|would|should|can|could)\b.*"
                 r"\b(?:cost|pay|price|spend|budget)\b|\bwhat(?:'s| is) the price\b"
                 r"|\bhow much for\b", low):
        return True
    found = re.search(r"\bhow much\b(.*)$", low)
    if not found:
        return False
    for word in re.findall(r"[a-z']+", found.group(1)):
        if word in PRICE_FILLER:
            continue
        return word in PRICE_VERBS
    return True


def _names_what_it_wants_priced(text):
    found = re.search(r"\bhow much\b(.*)$", flat(text))
    if not found:
        return False
    for word in re.findall(r"[a-z']+", found.group(1)):
        if word in PRICE_FILLER:
            continue
        if word in PRICE_VERBS:
            continue
        return True
    return False


SAME_WHERE = "The same goes for {thing}: {said}"
LEAD_PREPOSITION = frozenset("""in at on inside into for with about to of from by without after
                                before like using around near over under between""".split())
MOST_SAME = 220


DETERMINER = frozenset("the a an my our your his her its their this that these those".split())


NOT_A_THING = frozenset("again pardon sorry eh huh".split())
ONLY_THE_ASK = NOT_A_THING | frozenset("""
    what about again say said come then please it that this you was just now one more time
    """.split())

CLAUSE_START = frozenset("""
he hes she shes it its i im ive ill id you youre youve we weve were they theyre theyve
that thats this these those there nothing something anything everything nobody somebody
anybody everybody
""".split())
SAME_PLAIN = "Then the same holds: {said}"


def _same_where_they_asked(text, said):
    thing = swap.thing(text)
    if not thing:
        return ""
    if all(word in NOT_A_THING for word in re.findall(r"[a-z']+", thing.lower())):
        return ""
    from ..compose import fallback
    if fallback.reads_as_a_judgement(text):
        return ""
    clause = bool(re.findall(r"[a-z']+", thing.lower())[:1]
                  and re.findall(r"[a-z']+", thing.lower())[0] in CLAUSE_START)
    words = thing.split()
    if len(words) > 1 and words[0].lower() in LEAD_PREPOSITION:
        words = words[1:]
    if (not clause and words[0].lower() not in DETERMINER
            and not (len(words) == 1 and words[0].endswith("ing"))):
        words = ["the"] + words
    thing = " ".join(words)
    room = next((word for word in re.findall(r"[a-z']+", thing.lower())
                 if word.rstrip("s") in ROOMS), "")
    parts = [part.strip() for part in re.split(r"(?<=[.!?])\s+", str(said or "")) if part.strip()]
    asked = {word.rstrip("s") or word for word in re.findall(r"[a-z']+", thing.lower())}
    for part in parts:
        for piece in _the_method_in(part):
            if len(piece.split()) < 5 or len(piece) < 30 or len(piece) > MOST_SAME:
                continue
            if not _holds_where_they_asked(piece, asked):
                continue
            line = _mid_sentence(piece.rstrip(" ."))
            line = _room_they_asked_about(line, asked, room)
            if not line.endswith((".", "!", "?")):
                line += "."
            if clause:
                return SAME_PLAIN.format(said=_small_letter(line))
            return SAME_WHERE.format(thing=thing, said=_small_letter(line))
    return ""


def _mid_sentence(part):
    tokens = re.findall(r"[A-Za-z']+", part)
    if len(tokens) < 2 or not part[0].isupper():
        return part
    if tokens[0].lower() in [word.lower() for word in tokens[1:]]:
        return part[0].lower() + part[1:]
    return part


ROOMS = frozenset("""room kitchen bathroom bedroom loo toilet ensuite hall hallway landing lounge
living dining garage shed garden conservatory study nursery attic loft cellar basement porch patio
balcony utility laundry cloakroom downstairs upstairs flat house home""".split())


NAMED_PLACES = ROOMS | frozenset("""lawn grass flowerbed patio path gravel drive yard plot
allotment greenhouse""".split())


def _holds_where_they_asked(part, asked):
    named = {word.rstrip("s") or word
             for word in re.findall(r"[a-z']+", str(part or "").lower())} & NAMED_PLACES
    if not named or named & asked:
        return True
    return bool(named & ROOMS) and bool(asked & ROOMS)


def _the_method_in(part):
    pieces = [part]
    if ": " in part:
        pieces.append(part.split(": ", 1)[1])
    return pieces


def _room_they_asked_about(line, asked, room):
    if not room or not asked:
        return line
    found = {word.rstrip("s") or word
             for word in re.findall(r"[a-z']+", str(line or "").lower())} & ROOMS
    others = found - asked
    if len(others) != 1:
        return line
    other = others.pop()
    name = room.rstrip("s") or room
    return re.sub(r"\b%s(s?)\b" % re.escape(other), lambda m: name + (m.group(1) or ""),
                  line, flags=re.I)


def _a_place_of_the_same_kind(earlier, text):
    if not isinstance(earlier, dict):
        return False
    asked = {word.rstrip("s") or word
             for word in re.findall(r"[a-z']+", (swap.thing(text) or "").lower())}
    keys = {str(word).lower() for word in (earlier.get("keys") or ())}
    return bool(asked & ROOMS) and bool(keys & ROOMS)


def _a_place_they_asked(text):
    words = (swap.thing(text) or "").split()
    return bool(words) and words[0].strip("?.!,;:").lower() in swap.PREPOSITION


def _key_terms(item):
    def walk(node):
        if isinstance(node, str):
            return [node]
        try:
            children = list(node)
        except TypeError:
            return []
        out = []
        for child in children:
            out.extend(walk(child))
        return out
    return walk(getattr(item, "key", None) or ())


def _written_for(item, thing):
    if item is None:
        return False
    words = set(re.findall(r"[a-z']+", str(thing or "").lower()))
    if not words:
        return False
    for term in _key_terms(item):
        own = set(re.findall(r"[a-z']+", term.lower()))
        if own and (words <= own or own <= words):
            return True
    return False


def _more_than_the_thing(item, rest):
    if item is None:
        return False
    rest_words = set(re.findall(r"[a-z']+", str(rest or "").lower()))
    if not rest_words:
        return False
    for term in _key_terms(item):
        own = set(re.findall(r"[a-z']+", term.lower()))
        if own and own <= rest_words and not own <= swap.STOP:
            return True
    return False


def _about_the_rest_of_the_question(item, question, new):
    key = getattr(item, "key", None) or ()
    subject = key[0] if key else ()
    if not subject:
        return False
    new_words = re.findall(r"[a-z']+", str(new or "").lower())
    if not new_words or new_words[0] not in swap.PREPOSITION:
        return False
    asked = set(re.findall(r"[a-z']+", str(question or "").lower()))
    left = asked - set(new_words)
    for term in subject:
        words = re.findall(r"[a-z']+", str(term or "").lower())
        if words and all(word in left for word in words):
            return True
    return False


def _offer(reader, memory, reading):
    text_here = reading.get("text") if isinstance(reading, dict) else ""
    names_it = _names_what_it_wants_priced(text_here)

    def price_asked(held):
        return _asks_a_price((held or {}).get("text") if isinstance(held, dict) else text_here)

    declined = set()
    refused = _refused(text_here)
    fallback = None
    here = str((reading or {}).get("plain") or "").strip().lower()
    now = str((memory or {}).get("understood", {}).get("plain") or "").strip().lower() \
        if isinstance(memory, dict) else ""
    words_wanted = (_the_ask_is_for_words(reading)
                    if not here or not now or here == now else False)
    words_fallback = None
    words_declines = 0
    while True:
        got = reader(lambda one: one.id in declined)
        if got is None:
            kept = fallback or words_fallback
            if kept is None:
                return None, None
            item, held = kept
            reply = _payload(item, memory, held)
            return (item, reply) if reply.strip() else (None, None)
        item, held = got if isinstance(got, tuple) else (got, reading)
        if price_asked(held):
            reply = _payload(item, memory, held)
            if reply.strip() and not MONEY_SAID.search(reply):
                if names_it and fallback is None and not _said_before(reply, memory):
                    fallback = (item, held)
                declined.add(item.id)
                continue
        if not (_wants_a_stand_in(reading) and _a_swap_row(item)) \
                and _hands_back_the_refusal(item, refused):
            declined.add(item.id)
            continue
        reply = _payload(item, memory, held)
        if (reply.strip() and refused
                and not (_wants_a_stand_in(reading) and _a_swap_row(item))
                and _is_about(item, refused)
                and not _says_it_leaves_it_out(reply, refused)):
            declined.add(item.id)
            continue
        if (reply.strip() and words_wanted and words_declines < 3 and held is reading
                and not _said_before(reply, memory)
                and not SAID_OUT_LOUD.search(reply)
                and not _puts_it_to_someone(reply)):
            if words_fallback is None:
                words_fallback = (item, held)
            declined.add(item.id)
            words_declines += 1
            continue
        if reply.strip():
            return item, reply
        declined.add(item.id)


KEEPING_FROM_THE_ANSWER = "keeping-from-the-answer"


def _keeping_in_the_answer_before(memory):
    said = str(mem.last_bot(memory) or "").strip()
    if not said:
        return ""
    for sentence in SENTENCE.split(said):
        sentence = sentence.strip()
        if not (cooking.speaks_of_keeping(sentence) and KEEPS_A_FIGURE.search(sentence)):
            continue
        keep_at = KEEPING_CLAUSE.search(sentence)
        if keep_at and keep_at.start() > 0:
            lead = sentence[:keep_at.start()].rstrip(" ,;:-")
            if lead and ("," in lead or " and" in lead.lower()):
                sentence = sentence[keep_at.start():]
                sentence = sentence[:1].upper() + sentence[1:]
        if sentence.strip() == said.strip():
            continue
        return sentence.strip()
    return ""


KEEPING_CLAUSE = re.compile(r"\b(?:it|they|that|this|these|those)\s+(?:keeps?|lasts?|freez(?:e|es))\b",
                            re.I)
KEEPS_A_FIGURE = re.compile(
    r"\b\d+\s*(?:-|to)?\s*\d*\s*(?:day|days|week|weeks|month|months|year|years)\b"
    r"|\ba (?:day|week|month|year)\b|\bcouple of (?:days|weeks|months)\b", re.I)


def _keeping_reader(reading, memory):
    if not cooking.keeping_ask(reading):
        return lambda reject: find(reading, reject=reject)

    own = _own_thing(reading)

    def keeps(of, reject):
        def not_about_keeping(one):
            if reject(one):
                return True
            return not cooking.speaks_of_keeping(_payload(one, memory, of))
        return find(of, reject=not_about_keeping)

    def in_the_fridge(of):
        cold = dict(of)
        cold["clean"] = (str(of.get("clean") or of.get("text") or "") + " in the fridge")
        cold["words"] = list(of.get("words") or ()) + ["in", "the", "fridge"]
        return cold

    def with_the_thing(of):
        said = str(of.get("text") or of.get("clean") or "")
        fuller = _with_subject(said, memory)
        if not fuller.strip() or fuller.strip() == said.strip():
            return None
        return understand(fuller, memory)

    def reader(reject):
        found = keeps(reading, reject)
        if found is None:
            thing = with_the_thing(reading)
            if thing is not None:
                found = keeps(thing, reject)
        if found is None and not own and mem.last_module(memory) == "answers":
            kept = _keeping_in_the_answer_before(memory)
            if kept:
                return lookup_entry(KEEPING_FROM_THE_ANSWER, ("keep", "keeps", "last", "lasts"),
                                    kept)
        if found is None and mem.last_module(memory) == "answers":
            cold = keeps(in_the_fridge(reading), reject)
            if cold is not None and own and not _is_about(cold, own):
                cold = None
            found = cold
        return found or find(reading, reject=reject)

    return reader


DEGREES = re.compile(r"\b(\d{2,3})\s*(?:c\b|degrees)", re.I)


COOKED_THING = frozenset("""
cooked cook roast roasted bake baked fry fried grill grilled boil boiled poach poached steam
steamed leftover leftovers made reheat reheated rest rested
""".split())


def _cooked_thing(memory):
    return bool(set((mem.subject(memory) or "").split()) & COOKED_THING)


def _the_plan_for(text, memory, understood):
    if not _the_plan_answers_this(memory):
        return None
    answer = dishes.follow_up(memory, understood)
    if isinstance(answer, str) and answer.strip():
        return answer
    return None


COOK_VERB = re.compile(r"\b(?:cook|boil|bake|roast|fry|grill|simmer|steam|reheat|air-?fry|"
                       r"poach|braise|pressure cook)\b", re.I)
KEEPS_ANSWER = re.compile(r"\b(?:keeps?|lasts?|freezes?|fridge|freezer|cooler)\b", re.I)
KEEPS_ASK = re.compile(r"\b(?:keep|keeps|keeping|last|lasts|lasting|fridge|freezer|freeze|"
                       r"frozen|leftover|leftovers|left over|store|stored)\b", re.I)
PRONOUN_OBJECTS = frozenset(("it", "them", "that", "this", "one", "these", "those", "him",
                             "her", "his", "hers", "the rest", "some"))
REHEAT_ASK = re.compile(r"\b(?:re-?heat|re-?heating|heat (?:it|them|that|this) up|heat up|"
                        r"warm (?:it|them|that|this) up|warm up|microwave)\b", re.I)
REHEAT_REPLY = ("No fixed time: reheat it until it is piping hot right through, not just warm. "
                "A portion takes 2 to 4 minutes in the microwave with a splash of water, "
                "stirring halfway; a whole joint or a big tub needs 15 to 25 minutes covered in "
                "the oven at 180C. Piping hot means steaming all the way through, and reheat it "
                "once only.")


def _names_another_food(understood, subject):
    if not subject:
        return False
    words = set(subject.split())
    for ent in understood.get("entities") or []:
        if not isinstance(ent, dict) or str(ent.get("type") or "") == "person":
            continue
        text = str(ent.get("text") or "").lower().strip()
        if not text:
            continue
        if text in PRONOUN_OBJECTS or COOK_VERB.search(text):
            continue
        if words & set(text.split()):
            return False
        return True
    return False


KEEPING_WORD = re.compile(r"^(?:keep|keeps|keeping|kept|last|lasts|lasting|store|stored|"
                          r"storage|freeze|freezes|frozen|fridge|freezer|long)$", re.I)


def _the_food_named(subject):
    return " ".join(word for word in str(subject or "").split()
                    if not KEEPING_WORD.match(word))


def _a_cooking_ask_after_a_keeping_answer(understood, memory):
    line = str(understood.get("clean") or understood.get("text") or "")
    if not line or not COOK_VERB.search(line) or KEEPS_ASK.search(line):
        return None
    said = str((mem.answer_in_hand(memory) or {}).get("bot") or "")
    if not said or not KEEPS_ANSWER.search(said):
        return None
    subject = str(mem.subject(memory) or "").lower()
    if _names_another_food(understood, subject):
        return None
    if REHEAT_ASK.search(line):
        return REHEAT_REPLY
    food = _the_food_named(mem.subject(memory)) or None
    fuller = _with_subject(line, memory, about=food)
    if fuller.strip() == line.strip():
        fuller = _about_subject(line, memory, about=food)
    readings = [fuller, line] if fuller.strip() != line.strip() else [line]
    readings = [re.sub(r"\b(cooked|leftover|left over|roast|roasted)\s+(?=[\w' ]+\bfor\b)", "",
                       reading, count=1) for reading in readings]
    fallback = None
    for written in readings:
        reading = understand(written, memory)
        item, answer = _offer(lambda reject: find(reading, reject=reject), memory, reading)
        if item is None or not isinstance(answer, str) or not answer.strip():
            continue
        if answer.strip() == said.strip():
            continue
        if _minutes_in(answer):
            return answer
        fallback = fallback or answer
    return fallback


def _the_plan_answers_this(memory):
    said = str(mem.last_bot(memory) or "")
    if "air fryer" in said.lower() or "airfryer" in said.lower():
        return False
    return bool(DEGREES.search(said) or mem.has_time(said))


def _the_plan_said_again(understood, text, memory):
    if not (mem.asks_only(understood) and mem.last_module(memory) == "answers"):
        return None
    if not _the_plan_answers_this(memory):
        return None
    plan = dishes.follow_up(memory, understood)
    if not isinstance(plan, str) or not plan.strip():
        return None
    said = 0 if pairing(text) else _answer_said(plan, memory)
    if said >= 3:
        return AGAIN_HELP.format(reply=plan)
    if said:
        return AGAIN[said - 1].format(reply=_repeat_short(plan, text, memory))
    return None



def _filling_in_an_emergency(understood, memory):
    if not isinstance(memory, dict):
        return False
    said = [turn for turn in mem.recent(memory, 1) if isinstance(turn, dict)]
    if not said or said[-1].get("module") != "safety":
        return False
    if not isinstance(understood, dict):
        return True
    signals = understood.get("signals") or {}
    return not (understood.get("kind") == "question" or signals.get("question_mark"))


def _usable(item, reading, memory):
    if getattr(item, "fault", False):
        return True
    return not cooking.unusable(_reply_of(item, reading, memory), reading)


def _next_usable(item, reading, memory):
    kept = [one for one in all_entries() if one is not item and _usable(one, reading, memory)]
    return find(reading, entries=kept) if kept else None


def _without_names(reading):
    names = [name for name in (reading.get("person_names") or ()) if isinstance(name, str)]
    if not names:
        return reading
    drop = set(names)
    narrowed = dict(reading)
    words = reading.get("words")
    if isinstance(words, list):
        narrowed["words"] = [word for word in words
                             if not (isinstance(word, str) and word.lower() in drop)]
    clean = reading.get("clean")
    if isinstance(clean, str) and clean:
        narrowed["clean"] = " ".join(word for word in clean.split()
                                     if word.lower().strip(".,!?;:") not in drop)
    return narrowed
REWORD_ASKS = (
    "make this sound", "make that sound", "make it sound", "make mine sound",
    "make this a bit", "make this more", "make this less", "make that more", "make that less",
    "make it more", "make it less", "can you make this", "could you make this",
    "can you make it", "could you make it", "rewrite this", "rewrite that", "rewrite it",
    "can you rewrite", "could you rewrite", "reword this", "reword that", "reword it",
    "can you reword", "rephrase this", "rephrase that", "can you rephrase",
    "how do i word this", "how would you word", "how should i word", "how do i phrase this",
    "word this better", "say this more", "say it more", "say that more", "say this less",
    "say it less", "put this more", "put it more", "so it sounds", "so it doesnt sound",
    "so it doesn't sound", "so it sounds", "so that it sounds", "make this shorter",
    "make it shorter", "shorter please", "cut this down", "make this briefer",
    "make it a bit", "make this a little", "make it a little", "make this sound a bit",
    "check this sounds", "check that sounds", "check how this sounds", "check this reads",
    "does this sound", "does this read", "check this email", "check this message",
    "check this text", "check this note", "check this letter", "look over this",
    "check over this", "read this over", "read it over", "does this come across",
)

CHECK_ASKS = (
    "check this", "check that", "check how this", "does this sound", "does this read",
    "look over this", "check over this", "read this over", "read it over",
    "does this come across", "sounds all right", "sounds alright", "sound all right",
)

TONE_WORDS = {
    "warm": ("friendl", "nice", "nicer", "warm", "polite", "politer", "kind", "gentler",
             "gentle", "softer", "soft", "tactful", "diplomatic", "angry", "harsh", "rude",
             "aggressive", "blunt", "cross", "snappy"),
    "formal": ("formal", "professional", "businesslike", "official"),
    "casual": ("casual", "informal", "less stiff"),
    "short": ("short", "shorter", "brief", "concise", "punchy"),
}

TONING_WORDS = frozenset(word for words in TONE_WORDS.values() for word in words)
JOINING_WORDS = frozenset("""
and but or also plus then so just please bit little really very quite rather still too as well
less more much slightly now thanks thank you for me mate ok okay
to be sound sounds read reads look looks come comes across
""".split())
TONE_DESCRIPTORS = frozenset("""
joke jokes jokey jokingly jokier funny funnier fun silly serious light lighter cheery cheerful
breezier breezy flowery salesy pushy needy desperate posh chatty direct firm sweary swearing
angry cross snappy blunt harsh rude
""".split())


def _only_the_tone(rest):
    words = [word.strip(".,!?;:'\"") for word in str(rest or "").lower().split()]
    words = [word for word in words if word and word not in JOINING_WORDS]
    if not words:
        return True
    for word in words:
        if word in TONE_DESCRIPTORS or CONTINUED.search(word):
            continue
        if any(stem in word for stem in TONING_WORDS):
            continue
        return False
    return True

DEMANDS = (
    (re.compile(r"\bi want\b", re.I), "I'd like"),
    (re.compile(r"\bi need you to\b", re.I), "Could you"),
    (re.compile(r"\bi demand\b", re.I), "I'd ask for"),
    (re.compile(r"\bgive me\b", re.I), "could I have"),
    (re.compile(r"\byou need to\b", re.I), "could you"),
    (re.compile(r"\byou must\b", re.I), "would you be able to"),
    (re.compile(r"\byou never\b", re.I), "it sometimes feels like you don't"),
    (re.compile(r"\byou always\b", re.I), "it sometimes feels like you always"),
    (re.compile(r"\bi'm sick of\b", re.I), "I'm fed up with"),
    (re.compile(r"\bi am sick of\b", re.I), "I'm fed up with"),
    (re.compile(r"\bi'm fed up of\b", re.I), "I'm fed up with"),
    (re.compile(r"\bsort it out\b", re.I), "look into it"),
    (re.compile(r"\bright now\b", re.I), ""),
    (re.compile(r"\bimmediately\b", re.I), "as soon as you can"),
)


def _reword_ask(text):
    flat = _flat(text)
    lowered = " ".join(str(text or "").lower().split())
    asked = any(phrase in flat for phrase in REWORD_ASKS)
    tone = any(word in flat for group in TONE_WORDS.values() for word in group)
    if not (asked and (tone or ":" in lowered)):
        return None
    head, sep, tail = lowered.rpartition(":")
    if sep and len(tail.split()) >= 2 and any(phrase in _flat(head) for phrase in REWORD_ASKS):
        return tail.strip(" .\"'")
    at, found = len(flat) + 1, ""
    for phrase in REWORD_ASKS:
        where = flat.find(phrase)
        if where >= 0 and (where < at or (where == at and len(phrase) > len(found))):
            at, found = where, phrase
    rest = flat[at + len(found):] if found else flat
    rest = re.sub(r"\bso (it|that) (sounds?|reads?) (more |less )?.*$", "", rest)
    rest = re.sub(r"\bso (it|that) does ?n[o']?t sound .*$", "", rest)
    rest = re.sub(r"^\s*(a bit |abit |a little |alittle )?(sound|sounds|read|look)?\s*"
                  r"(less|more|softer|warmer|friendlier|nicer|politer|politelier|formal|"
                  r"professional|casual|shorter|briefer|blunt|harsh|rude|angry|aggressive|"
                  r"gentle|tactful|diplomatic|kind)\b\s*(angry|harsh|blunt|rude|aggressive|"
                  r"formal|polite)?",
                  "", rest)
    for _ in range(3):
        rest = re.sub(r"^\s*(a bit|a little|please|thanks|thank you|for me|mate)\b[ ,]*",
                      "", rest)
    rest = rest.strip(" .,:;\"'")
    if len(rest.split()) < 3 or _only_the_tone(rest):
        return ""
    return rest


def _tone_of(text):
    flat = _flat(text)
    tones = set()
    for tone, words in TONE_WORDS.items():
        if any(word in flat for word in words):
            tones.add(tone)
    if "less formal" in flat:
        tones.add("casual")
    if any(phrase in flat for phrase in CHECK_ASKS) and not tones:
        tones.add("check")
    return tones


def _softened(sentence, tones):
    out = sentence.strip()
    for pattern, better in DEMANDS:
        out = pattern.sub(better, out)
    out = out.replace("!", ".")
    out = re.sub(r"\bnow\b(?=\s*(?:[.,;!?]|$|or\b|and\b))", "", out)
    out = re.sub(r"\s+", " ", out).strip(" ,;")
    out = re.sub(r"\bi\b", "I", out)
    for bare, proper in (("cant", "can't"), ("dont", "don't"), ("wont", "won't"),
                         ("doesnt", "doesn't"), ("didnt", "didn't"), ("couldnt", "couldn't"),
                         ("wouldnt", "wouldn't"), ("isnt", "isn't"), ("im", "I'm"),
                         ("ive", "I've"), ("ill", "I'll")):
        out = re.sub(r"\b%s\b" % bare, proper, out)
    if out and out[0].islower():
        out = out[0].upper() + out[1:]
    if "formal" in tones:
        for short, long in (("I'm", "I am"), ("I've", "I have"), ("I'd", "I would"),
                            ("I'll", "I will"), ("don't", "do not"), ("doesn't", "does not"),
                            ("can't", "cannot"), ("won't", "will not"), ("it's", "it is"),
                            ("couldn't", "could not"), ("wouldn't", "would not")):
            out = re.sub(re.escape(short), long, out)
            cap_short, cap_long = short[0].upper() + short[1:], long[0].upper() + long[1:]
            out = out.replace(cap_short, cap_long)
    if "casual" in tones:
        for long, short in (("I would", "I'd"), ("I am", "I'm"), ("do not", "don't"),
                            ("cannot", "can't"), ("will not", "won't")):
            out = out.replace(long, short)
    for name in ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday",
                 "January", "February", "March", "April", "May", "June", "July", "August",
                 "September", "October", "November", "December"):
        out = re.sub(r"\b%s\b" % name.lower(), name, out)
    out = re.sub(r"\b(Hi|Hello|Dear|Hey|Thanks|Thank you|Morning|Afternoon)\s+([a-z])",
                 lambda m: m.group(1) + " " + m.group(2).upper(), out)
    if out and out[-1] not in ".?!":
        out += "."
    return out


CONTINUED = re.compile(r"\b(more|less|softer|friendlier|friendly|nicer|polite|politer|shorter|"
                       r"briefer|formal|casual|tone|warmer|pushy|rude|blunt|harsh|strong|needy|"
                       r"desperate|unprofessional)\b")


def _last_rewrite(memory):
    turns = memory.get("turns") or []
    for turn in reversed(turns[-4:]):
        if not isinstance(turn, dict):
            continue
        said = turn.get("user")
        asked = _reword_ask(said) if isinstance(said, str) else None
        if asked:
            return asked, _tone_of(said)
    return None


HARD_TO_SAY = (
    (re.compile(r"\b(quit|quits|resign|resigning|resigned|hand in my notice|leave my job)\b"),
     "I've decided to move on, and I'd like to agree a leaving date.",
     "Say it out loud first and keep to that one line: the date and a thank you are the parts "
     "they remember, and the reasons are for the exit interview."),
    (re.compile(r"\b(pay me|owe me|my money|the money back|refund|invoice)\b"),
     "I'd like to sort out what I'm owed, please.",
     "Put the amount and the date in the message, and say what you will do next if it is not "
     "settled, once, without heat."),
)


def _hard_to_say(asked):
    flat = " ".join(asked.lower().split())
    for pattern, sentence, tail in HARD_TO_SAY:
        if pattern.search(flat):
            return sentence, tail
    return None


def _rewritten(asked, tones, from_followup=False):
    body = _softened(asked, tones)
    known = _hard_to_say(asked)
    if from_followup:
        known = None
    if known is not None and ("warm" in tones or "short" in tones):
        body, tail = known
        return 'Softer, same point: "%s" %s' % (body, tail)
    if tones == {"check"}:
        return 'Reads all right: "%s" Nothing needs fixing: it is short, it says what you want, and ' \
               'it leaves them an easy way to say yes. Add the date you need an answer by if there ' \
               'is one.' % body
    polite = any(t in tones for t in ("warm", "formal"))
    asking = bool(re.search(r"\b(want|need|give|send|pay|refund|back|fix|sort|complain|explain|"
                            r"ask|book|change|cancel|return|replace|stop|reply|respond|"
                            r"could|would|can)\b", body.lower()))
    if re.search(r"\bneed to (tell|say|let)\b", body.lower()):
        asking = False
    if polite and asking and "please" not in body.lower() and not body.endswith("?"):
        body = body[:-1] + ", please." if body.endswith(".") else body + "?"
    if "short" in tones:
        body = re.sub(r"\b(just|really|actually|basically|obviously|literally)\b ?", "", body)
        body = re.sub(r"\s+", " ", body).strip()
    tail = ("Ask for what you want and a date, and leave out the anger: a short, specific message "
            "gets answered more often than a hot one.")
    if not asking:
        tail = ("Say it plainly, name the date, and stop there: the calmer and shorter it is, the "
                "better it lands.")
    if "formal" in tones:
        tail = ("Formal but human works best: the request, the date, and one line of reason, with no "
                "apology for asking.")
    elif "casual" in tones:
        tail = ("Keep it short and say it as you would out loud; the subject still has to be clear.")
    elif "short" in tones:
        tail = ("Cut everything that is not the request: the ask and the date are the whole message.")
    return 'Softer, same point: "%s" %s' % (body, tail)


THEIR_EAT = re.compile(r"\b(?:eat|eats|eating|diet|diets|vegetarian|vegan|pescatarian|meat"
                       r"|gluten|dairy|halal|kosher)\b", re.I)
COOK_WORD = re.compile(r"\b(?:cook|cooks|cooking|cooked|make|makes|making|recipe|recipes|meal"
                       r"|meals|dinner|lunch|tea|supper|dish|dishes|serve|serving|menu|feed"
                       r"|buy|shop"
                       r"|bake|bakes|baking|baked|roast|roasts|roasting|grill|grills|grilling"
                       r"|fry|fries|frying|breakfast|breakfasts|snack|snacks|pudding|puddings"
                       r"|dessert|desserts|cake|cakes|biscuit|biscuits|bread|packed lunch)\b",
                       re.I)
SAID_WORD = re.compile(r"\b(?:say|said|saying|tell|told|ask|asked|mention|mentioned|remember"
                       r"|remind)\b", re.I)

EAT_VERB = re.compile(r"\b(?:eat|eats|eating|have|has|having|drink|drinks|drinking|try|trying"
                      r"|tuck)\b")
DIET_WORDS = frozenset("""
meat dairy gluten nut nuts egg eggs fish pork wheat soya soy lactose halal kosher vegetarian
vegan pescatarian cheese milk sugar carbs alcohol shellfish peanut peanuts seafood chicken beef
lamb bacon ham butter cream yoghurt yogurt bread pasta rice potato chips
""".split())
NOT_THE_THING = frozenset("""
a an the some any this that it my your his her their our at on in for with too as well again
today tonight now though really then there here and but or so
""".split())


def _asks_about_a_food(low):
    found = EAT_VERB.search(low)
    if not found:
        return False
    words = [word.strip(".,!?;:'\"") for word in low[found.end():].split()]
    words = [word for word in words if word and word not in NOT_THE_THING]
    if not words:
        return False
    return words[0] not in DIET_WORDS


def _someones_else_diet(text, memory, understood):
    low = " ".join(str(text or "").lower().split())
    if not low or COOK_WORD.search(low):
        return False
    if not THEIR_EAT.search(low) or not isinstance(understood, dict):
        return False
    if not _names_someone_else(low):
        return False
    if not memory.get("others"):
        return False
    if understood.get("kind") != "question" and _a_guest_restriction(text, memory, understood):
        return False
    if understood.get("kind") == "question":
        if SAID_WORD.search(low):
            return True
        if _asks_about_a_food(low):
            return False
        return not _about_them_alone(low)
    if MEAT_FREE.search(low):
        return False
    return True


def _a_guest_restriction(text, memory, understood):
    try:
        from bot.knowledge import dishes
    except Exception:
        return False
    return bool(dishes.has_a_diet_reply(memory, understood)
                or dishes.has_a_veggie_reply(memory, understood))

MEAT_FREE = re.compile(
    r"\b(?:vegetarian|vegetarians|veggie|veggies|vegan|vegans|meat\s?free|flexitarian)\b|"
    r"\b(?:doesn'?t|doesnt|don'?t|dont|won'?t|wont|can'?t|cant|never|refuses to|hates)\s+"
    r"(?:eat|eats|eating|touch|touches)\s+(?:any\s+)?meat\b|"
    r"\b(?:no|without|off)\s+meat\b", re.I)


def _names_someone_else(low):
    for relation in mem.facts.RELATIONS:
        if re.search(r"\b" + relation + r"\b", low):
            return True
    return bool(re.search(r"\b(?:he|she|they|him|her|them|his|their)\b", low))


WRITE_OBJECT = frozenset("""
letter letters card cards note notes message messages text texts email emails wording words
verse poem speech toast
""".split())


def _a_writing_job(understood):
    norm = list((understood or {}).get("norm") or ())
    for at, word in enumerate(norm):
        if word not in ("thank", "thanks", "thankyou", "thank you", "thx", "ta"):
            continue
        rest = [w for w in norm[at + 1:] if w != "you"]
        if rest and rest[0] in WRITE_OBJECT:
            return True
    return False


A_TASTE_OF_THEIRS = re.compile(
    r"\b(?:what|which)\s+(?:does|do|did)\s+"
    r"(?:(?:my|our)\s+[a-z][a-z'\u2019-]*|he|she|they)\s+(?:not\s+)?"
    r"(?:like|love|enjoy|hate|dislike|mind|prefer|fancy)\b", re.I)


def _asks_about_their_taste(text):
    return bool(A_TASTE_OF_THEIRS.search(" ".join(str(text or "").lower().split())))


def _about_them_alone(low):
    theirs = "|".join(mem.facts.RELATIONS)
    if re.search(r"\b(?:my|our)\s+(?:" + theirs + r")\b", low):
        return False
    return bool(re.search(r"\b(?:i|im|i'm|me|my|we|us|our)\b", low))


COMPLAINT = re.compile(r"\b(?:i (?:get|have|had|keep getting|keep|suffer from|live with)|"
                       r"i(?:'ve|ve) (?:got|had|been having))\b", re.I)
HEALTH_DOMAINS = frozenset(("body", "science", "fitness"))
_HEALTH = []


def _health_entries():
    if not _HEALTH:
        _HEALTH.extend(one for one in all_entries()
                       if (getattr(one, "domain", "") or "") in HEALTH_DOMAINS)
    return _HEALTH


def _names_a_typed_word(item, text):
    said = {word.strip(".,!?;:").lower() for word in _flat(text).split()}
    return bool(said & _key_words(item))


DETAIL_LINE = re.compile(r"\b(?:worse|better|only|mostly|mainly|usually|always|hurts|aches|sore)\b"
                         r"[^.!?]{0,30}?\b(?:when|if|at|after|before|in the|during|while)\b|"
                         r"\b(?:when|if|whenever) (?:i|we)\b", re.I)
CIRCUMSTANCE = (
    ("bed", "lie", "lying", "lay", "sleep", "sleeping", "night", "nights", "overnight",
     "pillow", "reclining", "wake", "waking", "morning", "mornings"),
    ("sit", "sitting", "sat", "chair", "desk", "seated", "screens", "screen", "computer", "work"),
    ("stand", "standing", "stood", "feet", "upright"),
    ("eat", "eating", "meal", "meals", "food", "dinner", "lunch", "breakfast", "swallow"),
    ("walk", "walking", "run", "running", "stairs", "steps", "climb", "climbing", "kneel"),
    ("bend", "bending", "stoop", "lift", "lifting", "carry", "carrying"),
    ("cold", "chilly", "damp", "winter", "weather", "rain"),
    ("stress", "stressed", "anxious", "worry", "worried", "tension", "busy"),
)


def _circumstances(text):
    words = {word.strip("'") for word in re.findall(r"[a-z']+", str(text).lower())}
    found = set()
    for family in CIRCUMSTANCE:
        if words & set(family):
            found |= set(family)
    return found


DETAIL_FRAMES = ("Then this is the part that helps: {part}",
                 "That's the bit to work on: {part}",
                 "This is the part for that: {part}")


def _detail_frame(part):
    return DETAIL_FRAMES[len(part) % len(DETAIL_FRAMES)].format(part=part)


def _a_figure_the_answer_has(text, memory):
    from ..memory import detail as detail_reading
    try:
        return detail_reading.the_fact_the_answer_has(text, memory)
    except Exception:
        return None


def _a_detail_answered(text, memory):
    line = str(text or "")
    if not DETAIL_LINE.search(line):
        return None
    reply = str(mem.last_bot(memory) or "")
    if not reply:
        return None
    want = _circumstances(line)
    known_first = None
    said = {stem(word) for word in keywords(line) if len(word) > 2}
    best, best_score, known = "", 0, False
    sentences = [part.strip() for part in re.split(r"(?<=[.!?])\s+", reply) if part.strip()]
    for index, sentence in enumerate(sentences):
        if len(sentence.split()) < 6:
            continue
        if index == 0 and known_first is None and already_said(memory, sentence):
            known_first = sentence
        shared = want & _circumstances(sentence)
        if not shared:
            continue
        there = {stem(word) for word in keywords(sentence) if len(word) > 2}
        score = 2 * len(shared) + len(said & there)
        if score > best_score:
            best, best_score = sentence, score
            known = already_said(memory, sentence)
    if best and best == known_first:
        return None
    if not best:
        return None
    if len(best.split()) * 2 >= len(str(reply).split()):
        return None
    part = best[0].lower() + best[1:] if best[:1].isupper() else best
    return _detail_frame(part)


def _a_complaint_answered(text, understood, memory):
    if not COMPLAINT.search(_flat(text)):
        return None
    if trouble_reading.reads_as_trouble(_flat(text), (understood or {}).get("words")):
        return None
    if find(understood) is not None:
        return None
    again = dict(understood)
    again["clean"] = "what can i do about " + str(understood.get("clean") or _flat(text))
    again["words"] = [word for word in re.findall(r"[a-z']+", again["clean"].lower()) if word]
    item, reply = _offer(lambda reject: find(again, entries=_health_entries(), reject=reject),
                         memory, again)
    if item is None or not isinstance(reply, str) or not reply.strip():
        return None
    if not _names_a_typed_word(item, text):
        return None
    remember_answer(memory, reply, _key_words(item))
    _remember_answer(memory, item, reply)
    return reply


def _a_dish_was_offered(memory):
    if not isinstance(memory.get("meal"), dict):
        return False
    turns = memory.get("turns") or ()
    return bool(turns) and (turns[-1] or {}).get("module") == "answers"


def observe(text, memory):
    understood = memory.get("understood")
    if not isinstance(understood, dict):
        understood = understand(text, memory)
    try:
        a_year_of_birth.observe(text, memory)
    except Exception:
        pass
    try:
        plan = cooking.remembered(understood, memory)
    except Exception:
        return
    if plan:
        memory["meal"] = plan


LENGTH_SAID = frozenset("""
    how long much many it that this these those them they he she you i
    do does did is are was were be been will would should can could
    a an the of to for in on at about more time day days week weeks month months
    hour hours minute minutes last lasts lasted going gone left
    take takes taking me us mine
""".split())


def _asks_only_the_length(text):
    words = [re.sub(r"[^a-z']", "", word.lower()) for word in str(text or "").split()]
    words = [word for word in words if word]
    if not words or not set(words) & {"long", "many", "much"}:
        return False
    return set(words) <= LENGTH_SAID


def TAKES_AS_IT_COMES(text, memory=None):
    if not isinstance(text, str) or not isinstance(memory, dict):
        return False
    return bool(repeat.asks_for_less(text) and repeat.shorter_for(text, memory))


def claims_instead(text, memory=None):
    if not isinstance(text, str) or not ANSWERING_A_QUOTED_ASK.search(text):
        return False
    if WHO_IS_THE_BOT.search(text) or not isinstance(memory, dict):
        return False
    try:
        return respond(text, memory) is not None
    except Exception:
        return False


CLAIMS_INSTEAD = claims_instead


def _a_limit_on_the_plan(text, memory):
    try:
        from ..memory import ack as _ack
    except Exception:
        return False
    try:
        return bool(_ack.a_limit_on_the_plan(text) and _ack.a_limit_reply(text, memory))
    except Exception:
        return False


THEIR_OWN_ASK = re.compile(
    r"\b(?:did|have|had)\s+i\s+(?:just\s+)?(?:say|said|tell|told|mention|mentioned)\b", re.I)


def _a_bare_thanks(understood):
    return (isinstance(understood, dict) and understood.get("kind") == "thanks"
            and not _a_writing_job(understood))


def _a_judgement_of_the_figure_on_the_table(text, memory):
    try:
        from ..compose import reading as _reading
        return _reading.judges_the_figure_on_the_table(text, memory)
    except Exception:
        return False


_AN_ANSWER = frozenset(("answers", "memory_store"))


def _the_bot_has_something_to_go_over(memory):
    from ..memory import meant as _meant
    from ..memory import repeat as _repeat
    turns = memory.get("turns") if isinstance(memory, dict) else None
    for turn in reversed((turns or [])[-_meant.LOOK_BACK_FAR:]):
        if not isinstance(turn, dict):
            break
        said = str(turn.get("bot") or "").strip()
        if not said:
            continue
        if str(turn.get("module") or "") in _meant.NOT_TO_REPEAT:
            break
        asked = str(turn.get("user") or "").strip()
        if (_repeat.HEDGE.search(said) or _meant.CONDOLENCE.match(said)
                or _meant.RECEIPT.search(said)):
            continue
        if str(turn.get("module") or "") in _AN_ANSWER or _meant._thick_enough(said, asked):
            return True
    return False


def _the_line_asks_what_this_one_meant(memory):
    if not isinstance(memory, dict):
        return False
    understood = memory.get("understood")
    if not (isinstance(understood, dict) and understood.get("asks_what_was_meant")):
        return False
    return _the_bot_has_something_to_go_over(memory)


def respond(text, memory):
    from ..memory import not_this as _ruled_out
    from ..memory import portions as _portions
    from ..memory import size as another_size
    from ..memory import trips as _trips
    from ..memory.thread import only_the_arrival as _only_the_arrival
    from ..compose import said_about_me
    if isinstance(memory, dict):
        memory["asked_now"] = text
    if _only_the_arrival(text):
        return None
    if said_about_me.answer_followup(text, memory):
        return None
        return None
    if _trips.THE_JOURNEY_ASK.search(text or "") and _trips.reply_for(text, memory):
        return None
    if _the_line_asks_what_this_one_meant(memory):
        return None
    if _a_judgement_of_the_figure_on_the_table(text, memory):
        return None
    if THEIR_OWN_ASK.search(text or ""):
        return None
    if repeat.A_PAY_WORD.search(" ".join(str(text or "").lower().split())) \
            and repeat.the_figure_they_gave(text, memory if isinstance(memory, dict) else {}):
        return None
    if (_portions.an_ask(text or "", memory) or _portions.a_count_to_fill(text or "", memory)
            or _portions.a_bare_count_to_fill(text or "", memory)):
        return None
    understood = memory.get("understood") if isinstance(memory, dict) else None
    if isinstance(understood, dict) and understood.get("subject_unclear"):
        return None
    if _a_bare_thanks(understood) and not (isinstance(text, str)
                                          and repeat.after_an_ack(text)):
        return None
    from ..compose import fallback as _the_composer
    if _the_composer.the_day_remarked(text):
        return None
    if _ruled_out.the_place_ruled_out(text, memory):
        return None
    try:
        if repeat.asks_what_that_costs(text, memory):
            return None
    except Exception:
        pass
    if mem.facts.a_name_picked(text, memory):
        return None
    dog_feed = pets.the_dog_feed_follow_up(text, memory)
    if dog_feed:
        _remember_answer(memory, pets.DOG_FEED_AMOUNT_ENTRY, dog_feed)
        return dog_feed
    limit = _a_limit_on_the_plan(text, memory)
    judged = a_price.judged(text, memory)
    if judged:
        _keep_the_answer(text, judged, memory)
        return judged
    resized = another_size.answer_for(text, memory)
    if resized:
        _keep_the_answer(text, resized, memory)
        return resized
    if tried.a_card_is_not_the_answer(text, memory):
        return None
    reply = with_name(_the_dish_by_name(a_year_of_birth.reply(text, memory)
                                       or _answer(text, memory), memory), memory)
    judged = a_price.judged_with_the_card(text, reply, memory)
    if judged:
        _keep_the_answer(text, judged, memory)
        return judged
    placed = _the_question_with_the_place_on_it(text, memory, reply)
    if placed:
        _keep_the_answer(text, placed, memory)
        return placed
    if reply:
        reply = _fitted_to_what_they_eat(reply, text, memory)
    if reply:
        reply = _the_sentence_it_names(reply, text, memory)
    if reply:
        reply = lead.answer_first(
            reply, memory.get("understood") if isinstance(memory, dict) else None, text)
    if reply:
        reply = lead.shape(reply, memory.get("understood")
                           if isinstance(memory, dict) else None, text)
    if reply:
        reply = lead.the_sentence_owed(reply, memory.get("understood")
                                       if isinstance(memory, dict) else None,
                                       _the_sentence_owed(text, reply, memory))
    if not reply and limit:
        return None
    if not reply:
        card = shopping.the_card_after_a_present(None, memory, line=text)
        if card and shopping.a_present_was_answered(memory):
            reply = card
    if not reply:
        reply = _the_one_to_pick(text, memory)
    _keep_the_answer(text, reply, memory)
    return healing.vetted(text, memory, reply, step_of=_first_step)


def _the_question_with_the_place_on_it(text, memory, reply):
    question = whereabout.the_question_with_the_place(text, memory)
    if not question:
        return ""
    from ..compose import fallback as composer
    said = str((memory.get("last_answer") or {}).get("reply") or "")
    placed = with_name(_the_dish_by_name(_answer(question, _of_its_own(memory)), memory), memory)
    if not placed or placed in composer.UNKNOWN:
        return ""
    for other in (said, reply):
        if other and placed.strip() == str(other).strip():
            return ""
    flat_placed = _flat(placed)
    for other in (said, reply):
        flat_other = _flat(str(other or ""))
        if flat_other and flat_other in flat_placed:
            return ""
        if flat_other and flat_other[:60] in flat_placed:
            return ""
    return placed


_TURN_ONLY = ("understood", "entry_answer", "entry_answers", "frequency_answer",
              "frequency_reply", "last_answer", "topics", "topic", "return_to", "correction",
              "denial", "replies")


def _of_its_own(memory):
    own = copy.deepcopy(memory) if isinstance(memory, dict) else {}
    for key in _TURN_ONLY:
        own.pop(key, None)
    return own


def _keep_the_answer(text, reply, memory):
    if not isinstance(memory, dict) or not isinstance(reply, str) or not reply.strip():
        return
    turns = memory.get("turns")
    here = len(turns) if isinstance(turns, list) else 0
    kept = memory.get("last_answer")
    if isinstance(kept, dict) and kept.get("turn") == here and kept.get("reply"):
        return
    _remember_answer(memory, None, reply, keys=keywords(text))



def _the_sentence_it_names(reply, text, memory):
    mine = _flat(reply)
    if not mine or not isinstance(memory, dict):
        return reply
    said_before = any(isinstance(turn, dict) and _flat(turn.get("bot")) == mine
                      for turn in memory.get("turns") or [])
    if not said_before:
        return reply
    named = set(keywords(text)) - _said_before_now(text, memory)
    named &= set(words_of(reply))
    if not named:
        return reply
    parts = [sentence.strip() for sentence in SENTENCE.split(str(reply).strip())
             if sentence.strip() and named & set(words_of(sentence))]
    if not parts:
        return reply
    cut = " ".join(parts[:2])
    if len(cut.split()) < 4 or len(cut) >= len(str(reply).strip()):
        return reply
    return cut


def _fitted_to_what_they_eat(reply, text, memory):
    if not isinstance(reply, str) or not reply.strip():
        return reply
    avoided = cooking.avoids(memory)
    reply = meat_in_a_card.swapped_out(reply, text, avoided)
    fitted = cooking.fits_the_diet(reply, avoided, text)
    if fitted is None:
        return ""
    fitted = cooking.fitted_for_the_one_talked_about(
        fitted, cooking.avoids_for_the_one_talked_about(memory), text)
    if fitted is None:
        return ""
    return fitted


_DISH_NAME_IN_TEXT = re.compile(r"^\s*(?:(?:one|two)[- ]pan\s+|a\s+|an\s+|the\s+)?"
                                r"([^:.,]{3,40}?)\s*:", re.I)


def _the_dish_by_name(answer, memory):
    if not isinstance(answer, str) or " that one" not in answer.lower():
        return answer
    plan = cooking.plan_recent(memory) or {}
    offered = [name for name in (plan.get("offered") or ()) if name]
    if not offered:
        return answer
    dishes = {dish["id"]: dish for dish in cooking.DISHES}
    said = _DISH_NAME_IN_TEXT.match(str((dishes.get(offered[-1]) or {}).get("text") or ""))
    name = ""
    if said and len(said.group(1).split()) <= 5:
        name = said.group(1).lower()
    if not name:
        shown = _last_answer(memory)
        shown = shown.get("reply") if isinstance(shown, dict) else shown
        screen = _DISH_NAME_IN_TEXT.match(str(shown or ""))
        if screen and len(screen.group(1).split()) <= 5:
            name = screen.group(1).lower()
    if not name:
        return answer
    return re.sub(r"\bthat one\b", "the " + name, answer, count=1, flags=re.I)


def _the_same_answer_again(answer, memory):
    was = _flat(mem.last_bot(memory) or "")
    now = _flat(_without_lead_in(answer))
    if not was or not now:
        return False
    return now.startswith(was[:60]) or was.startswith(now[:60])
def _the_figure_the_thing_we_are_on_holds(text, memory):
    understood = memory.get("understood") if isinstance(memory, dict) else None
    if not isinstance(understood, dict):
        return ""
    wider = followup_reading(understood, memory)
    if not isinstance(wider, dict) or wider is understood:
        return ""
    if _flat(str(wider.get("clean") or "")) == _flat(str(understood.get("clean") or "")):
        return ""
    item, reply = _offer(lambda reject: find(wider, reject=reject), memory, wider)
    reply = str(reply or "").strip()
    if item is None or not reply:
        return ""
    return "" if _figure_missing(reply, text) else reply


def _a_length_ask_with_no_figure(text, memory, answer=""):
    if not _asks_only_the_length(text) or mem.last_module(memory) != "answers":
        return None
    earlier = _last_answer(memory)
    last = str((earlier or {}).get("reply") or "")
    if not last.strip():
        return None
    if answer:
        opening = _flat(last)[:60]
        if not opening or opening not in _flat(answer):
            return None
    honest = _figure_missing(last, text)
    if not honest or _flat(honest) == _flat(answer):
        return None
    return _the_figure_the_thing_we_are_on_holds(text, memory) or honest

def _a_city_card_asks_which_first(text, memory):
    from ..knowledge import travel as travel_cards
    return (travel_cards.asks_which_one_first(text)
            and travel_cards.a_city_card_is_in_front(_the_answer_in_front(memory)))


def _the_answer_in_front(memory):
    if not isinstance(memory, dict):
        return ""
    turns = memory.get("turns")
    if not isinstance(turns, list) or not turns:
        return ""
    said = turns[-1] if isinstance(turns[-1], dict) else {}
    if said.get("module") != "answers":
        return ""
    return str(said.get("bot") or "")
TAKEN_BACK_OPENER = re.compile(
    r"^\s*(?:(?:please|ok|okay|right)\s+)?(?:forget|forgot|ignore|scratch|disregard|drop|"
    r"never\s+mind|no)\s+(?:that|this|it|the|my|our|your|a|an|about|all)\b", re.I)


LEAD_ASK = re.compile(
    r"\bhow\s+(?:long|far|soon)\s+(?:before|ahead\s+of)\s+(?P<event>[^.?!]{1,60}?)\s*"
    r"\b(?:should|shall|ought\s+to|do)\s+(?:i|we|you|one)\s+(?P<act>[^.?!]{0,60})"
    r"|\bhow\s+(?:long|far|soon|early)\s+in\s+advance\s+(?P<act2>[^.?!]{0,60})"
    r"|\bhow\s+early\s+(?:should|shall|do)\s+(?:i|we|you)\s+(?P<act3>[^.?!]{0,60})")
LEAD_ROWS = (
    (("cake",), "Order a decorated one four to six weeks ahead: the bakery wants the number of "
                "people and the design about a month out, and the week itself it can turn round. "
                "A fruit cake is the exception: it is baked well before and fed brandy as it "
                "sits, and it only gets better."),
    (("turkey", "goose", "bird"), "Order it by the middle of December, and collect it on the 22nd "
                                  "or 23rd so it has two days in the fridge. Free-range and big "
                                  "birds go first, so the middle of the month is the real deadline."),
    (("invitation", "invite", "save"), "Six to eight weeks before the day, with the reply-by four "
                "weeks out - eight to twelve if people have to travel or fly. The venue and any "
                "rooms are the things that go a year ahead, not the cards."),
    (("passport",), "Ten weeks is the honest allowance for a standard renewal, and quicker costs "
                    "extra. Check the country you are going to as well: many want six months left "
                    "on it at the date you arrive, not the date you leave."),
    (("parking",), "Two to four weeks ahead is plenty and the price is the reason: the on-the-day "
                   "rate at an airport is several times the booked one, and the cheap car parks go "
                   "first. The date and the flight time are all they need."),
    (("hotel", "accommodation", "cottage", "campsite", "room"), "As soon as the dates are fixed. A "
                "hotel needs nothing from you but a card, and the cheap rooms are the ones that "
                "sell out first - a refundable rate booked early beats a dearer one late."),
    (("table", "restaurant"), "Two to four weeks ahead for a Friday or Saturday, and a week or two "
                              "for a weeknight. Somewhere small or famous you book when you think "
                              "of it, and a set menu also wants the numbers a few days before."),
    (("flight", "ferry", "train", "ticket", "travel"), "Six to twelve weeks ahead is the cheapest "
                "window: a flight is dearest in the last fortnight and a train is best booked the "
                "day the tickets release, about twelve weeks out. After that the price only climbs."),
    (("venue", "hall", "church", "marquee"), "A year or more for a Saturday in summer, and two "
                "years for the popular ones. The venue sets the date, so it is the first thing "
                "booked and everything else fits round it."),
    (("flower", "delivery", "bouquet", "gift", "present"), "Three to five days ahead for a delivery "
                "on a set day, and a fortnight for anything made to order or for Valentine's and "
                "Mother's Day. Same-day is a different, dearer price."),
)
LEAD_VERB = re.compile(r"\b(?:order|orders|ordering|book|books|booking|reserve|reserving|hire|"
                       r"hiring|send|sends|sending|renew|renews|renewing|apply|applying|"
                       r"arrange|arranging|sort|sorting|pay|paying|buy|buying|collect|"
                       r"collecting|pick|picking)\b")
LEAD_ANY = "Sooner than you would think: the price only goes up and the good slots go first, so " \
           "book it as soon as the date is fixed. Tell me which booking and I will be exact."


def _a_lead_time(text):
    if not isinstance(text, str):
        return None
    found = LEAD_ASK.search(text.lower())
    if not found:
        return None
    act = " ".join(part for part in found.groups() if part)
    if not LEAD_VERB.search(act):
        return None
    words = {word.rstrip("s") for word in WORD.findall(text.lower())}
    for needles, answer in LEAD_ROWS:
        if any(needle.rstrip("s") in words for needle in needles):
            return answer
    return LEAD_ANY




def _the_thing_has_got_better(text, memory):
    clean = " ".join(str(text or "").lower().split())
    if not clean or "?" in clean:
        return False
    got_better = goodnews.reads_as_recovery(clean) or (
        goodnews.reads_as_settled(clean) and goodnews.worry_on_the_table(memory or {}))
    return bool(got_better) and goodnews.the_news_is_the_whole_of_it(clean)


A_CASE_ASK = re.compile(
    r"^(?:and|or|what|how|which|then)\b[^?.]{0,40}\b(?:one|ones|other|another|"
    r"hard|soft|big|small|large|little|medium|old|young|dark|light|cheap|quick|slow)\b", re.I)
A_CASE_STOP = frozenset("""about and another any are can could for from have how i if is it
    its just like long many much my of one ones or other the then to what when which who why
    will with would you your""".split())


def _a_case_of_the_answer_in_hand(text, memory):
    line = " ".join(str(text or "").split())
    if not line or len(line.split()) > 8:
        return ""
    if not A_CASE_ASK.match(line.lower()):
        return ""
    wanted = {word for word in WORD.findall(line.lower())
              if len(word) > 2 and word not in A_CASE_STOP}
    if not wanted:
        return ""
    answers = [str(turn.get("bot")) for turn in reversed(memory.get("turns") or ())
               if isinstance(turn, dict) and turn.get("bot") and turn.get("module") == "answers"]
    after_a_case = bool(answers) and len(answers[0].split()) <= 12
    for answer in answers[:3]:
        try:
            part = length.narrow(answer, text)
        except Exception:
            part = ""
        if not isinstance(part, str) or not part.strip():
            part = ""
        uncut = not part or (" ".join(part.lower().split())
                             == " ".join(answer.strip().lower().split()))
        if uncut:
            part = answer.strip() if len(answer.split()) <= 30 else ""
        if not part:
            continue
        if not re.search(r"\d", part):
            continue
        if len(part.split()) > (30 if after_a_case else 14):
            continue
        if after_a_case and len([s for s in re.split(r"(?<=[.!?])\s+", part.strip())
                                 if s.strip()]) > 1:
            continue
        said = {word.rstrip("s") for word in WORD.findall(part.lower())}
        if not any(word.rstrip("s") in said for word in wanted):
            continue
        part = part.strip()
        if part[-1:] not in ".!?":
            part += "."
        return part[:1].upper() + part[1:]
    return ""


def _answer(text, memory):

    if isinstance(memory, dict) and memory:
        from ..memory.when import asks_what_today_is

        if asks_what_today_is(text):
            return _answer(text, {})
    if isinstance(memory, dict) and stuck_line.pool(text, memory) \
            and not repeat.answer_for(text, memory):
        return None
    understood = memory.get("understood") if isinstance(memory, dict) else None
    if A_PLEA_FOR_TIPS.match(str(text or "").strip().lower()) \
            and mem.last_module(memory) == "answers":
        return None
    if isinstance(understood, dict) and understood.get("intent") == "farewell":
        return None
    if isinstance(understood, dict):
        written = named.the_best_time_to_do_it(text, understood, memory)
        if written:
            said = _ask_a_rewritten_line(written, memory)
            if said and not _said_before(_without_lead_in(said), memory):
                return said
    if isinstance(memory, dict) and _the_thing_has_got_better(text, memory):
        return None
    if isinstance(memory, dict):
        the_moan = _the_ask_behind_a_moan(text, memory)
        if the_moan:
            return the_moan
    led = _a_lead_time(text)
    if led:
        return led
    if isinstance(memory, dict):
        own = find(understand(text))
        own_answers_the_length = False
        if own is not None:
            own_said = _payload(own, memory, understand(text))
            own_answers_the_length = bool(_answers_a_length(own, own_said)
                                          and _A_DURATION.search(str(own_said or "")))
        for written in doing_it.written_out(text, memory):
            if own_answers_the_length:
                break
            reading = understand(written)
            reached = find(reading)
            if reached is None:
                continue
            if own is not None and reached is own:
                continue
            written_reply = _payload(reached, memory, reading)
            if not _answers_a_length(reached, written_reply):
                continue
            if _said_before(_without_lead_in(written_reply), memory):
                short = length.narrow(written_reply, text)
                if short and not _said_before(short, memory):
                    return short
                continue
            return written_reply
    if a_wish.reading(text):
        return None
    if isinstance(memory, dict) and prefer.served_already(text, memory):
        return ""
    agreed = repeat.agreement_with_the_answer(text, memory)
    if agreed:
        return agreed
    if isinstance(text, str) and BARE_SAY_NO.search(text):
        return _the_line_again(text, memory) or work.SAY_NO_POLITELY
    shorter = repeat.shorter_for(text, memory) if isinstance(memory, dict) else None
    if shorter:
        return shorter
    dated = deadline.follow_up(text, memory) if isinstance(memory, dict) else ""
    if dated:
        answer = _ask_a_rewritten_line(dated, memory)
        if answer and _the_same_answer_again(answer, memory):
            answer = None
        if answer:
            return answer
    animal = the_animal_the_subject_is(understood, memory) if isinstance(memory, dict) else None

    back_to = said_topic.the_thing_asked_again(memory, text) if isinstance(memory, dict) else ""
    if back_to:
        thing = said_topic.the_thing_went_back_to(memory)
        reached = find(understand(back_to, memory))
        if reached is not None and any(_the_entry_names(reached, word)
                                       for word in thing.split() if len(word) > 3):
            answer = _ask_a_rewritten_line(back_to, memory)
            if answer:
                return same_again.instead(answer, text, memory) or answer
    if repeat.asks_which_part(text) and not _a_city_card_asks_which_first(text, memory):
        step = repeat.the_move(text, _the_answer_in_front(memory), memory)
        if step:
            return step
    case = _a_case_of_the_answer_in_hand(text, memory) if isinstance(memory, dict) else ""
    if case:
        return case
    if limit.reads_the_answer(text, memory):
        return None
    if TAKEN_BACK_OPENER.match(str(text or "")) and "?" not in str(text or "") \
            and len(str(text or "").split()) <= 5:
        return None
    back_to = went_back.a_return_to_the_topic(text, memory) if isinstance(memory, dict) else ""
    if back_to:
        answer = _ask_a_rewritten_line(back_to, memory)
        if answer:
            if _said_before(_without_lead_in(answer), memory):
                return went_back.as_the_same_answer(
                    answer, text, short=_repeat_short(answer, back_to))
            return answer
    again = named.a_measure_asked_again(text, memory) if isinstance(memory, dict) else ""
    if again:
        answer = _ask_a_line_of_its_own(again, memory)
        if answer and not _the_same_answer_again(answer, memory):
            return answer
    trip = named.a_part_of_the_trip(text, memory) if isinstance(memory, dict) else ""
    if trip:
        answer = _ask_a_rewritten_line(trip, memory)
        if answer:
            if not _A_YES_NO_ASK.match(str(text or "").strip()):
                again_told = same_again.instead(answer, text, memory)
                if again_told:
                    return again_told
            if not _said_before(_without_lead_in(answer), memory):
                return answer
    moved = when.a_plan_moved_to_a_day(text) if isinstance(memory, dict) else None
    if moved:
        answer = _ask_a_rewritten_line(moved["line"], memory)
        if answer and not _said_before(_without_lead_in(answer), memory):
            day = moved["day"]
            return day[:1].upper() + day[1:] + " works. " + answer
    if tried.reads_as_a_step_done(text, memory):
        return None

    part_owned = _the_part_of_the_thing_they_named(text, memory)
    if part_owned:
        return part_owned
    animal_line = pets.the_animal_follow_up_line(text, memory)
    if animal_line:
        animal_answer = _ask_a_rewritten_line(animal_line, memory)
        if animal_answer:
            return animal_answer
    answer = _respond(text, memory)
    if animal is not None and (
            not answer or answers_about_another_creature(answer, animal.get("clean") or "")):
        filled = _ask_a_rewritten_line(animal.get("clean") or "", memory)
        if filled and not _the_same_answer_again(filled, memory):
            answer = filled
    if _asks_only_the_length(text):
        honest = _a_length_ask_with_no_figure(text, memory, answer or "")
        if honest:
            return honest
    measure = named.about_the_subject(text, memory) if isinstance(memory, dict) else ""
    if measure:
        said_about_it = _a_measure_about_the_subject(measure, text, memory, answer)
        if said_about_it:
            return said_about_it
    if answer:
        if (isinstance(text, str) and _A_BARE_MEASURE.fullmatch(text)
                and re.search(r"\d", str(answer))
                and (SIGNALS["amount"].search(answer) or SIGNALS["money"].search(answer))):
            return answer
        said = _answer_said(answer, memory) if _flat(answer) == _flat(mem.last_bot(memory)) else 0
        if said:
            if said >= 3:
                return AGAIN_HELP.format(reply=_repeat_short(_without_lead_in(answer), text, memory))
            return AGAIN[said - 1].format(reply=_repeat_short(_without_lead_in(answer), text, memory))
        short_of_it = _short_form_of_the_last(answer, memory)
        fact = bool(short_of_it) and _a_fact_about_the_person(memory)
        detail = ""
        if short_of_it and not ASKS_ABOUT_HOW_IT_TURNED_OUT.search(text):
            detail = (_a_part_named_in_the_line(text, memory, short_of_it)
                      or ("" if fact else _the_detail_named(text, memory)))
        if detail:
            if _named_in(short_of_it, detail):
                part = _the_part_in_the_answer(short_of_it, detail)
                if part:
                    return part
            return NOTHING_SEPARATE[0].format(detail=detail)
        if fact and _only_a_quality_name(text, memory):
            return AGAIN[0].format(reply=_repeat_short(short_of_it, text, memory))
        if fact:
            return None
        if short_of_it and _their_own_state(text):
            return None
        return answer
    carried_on = more.reply_for(text, memory) if isinstance(memory, dict) else None
    if carried_on:
        return carried_on
    if tried.might_be_a_report(text) and tried.pool_for(text, memory):
        return None
    understood = memory.get("understood")
    if not isinstance(understood, dict):
        understood = understand(text, memory)
    if (understood or {}).get("kind") == "statement":
        told = _a_complaint_answered(text, understood, memory)
        if told is not None:
            return told
    carried = named.follow_up(text, memory) if isinstance(memory, dict) else ""
    from_a_taste = False
    if not carried:
        carried = prefer.follow_up(text, memory) if isinstance(memory, dict) else ""
        from_a_taste = bool(carried)
    if carried:
        answer = _ask_a_rewritten_line(carried, memory)
        if answer and (_same_as_the_last_answer(answer, memory)
                      or _the_same_answer_in_other_words(answer, memory)):
            answer = None
        if answer and from_a_taste and not prefer.about_the_medium(answer, memory):
            answer = None
        if answer:
            return answer
    if isinstance(memory, dict):
        for in_hand in named.reported_states(text, memory):
            reached = find(understand(in_hand, memory))
            if not _the_report_is_answered(text, reached):
                continue
            answer = _ask_a_rewritten_line(in_hand, memory)
            if answer and not _said_before(_without_lead_in(answer), memory):
                return same_again.instead(answer, text, memory) or answer
    if isinstance(memory, dict):
        for stated in named.stated_about_the_person(text, memory):
            reached = find(understand(stated, memory))
            if not _the_fact_is_what_is_answered(text, stated, reached, memory):
                continue
            answer = _ask_a_rewritten_line(stated, memory)
            if answer and _most_of_it_said(answer, memory):
                continue
            if answer and not _said_before(_without_lead_in(answer), memory):
                return same_again.instead(answer, text, memory) or answer
    if isinstance(memory, dict):
        for practice in named.care_reports(text, memory):
            reached = find(understand(practice, memory))
            if not _the_practice_is_answered(practice, reached):
                continue
            answer = _ask_a_rewritten_line(practice, memory)
            if answer and not _said_before(_without_lead_in(answer), memory):
                return same_again.instead(answer, text, memory) or answer
    bare = named.about_it(text, memory) if isinstance(memory, dict) else ""
    if bare:
        answer = _ask_a_rewritten_line(bare, memory)
        if answer:
            short = _the_sentence_about(text, memory) or _the_sentence_about(bare, memory)
            if short and _flat(short) != _flat(answer):
                return short
            if not _said_before(_without_lead_in(answer), memory):
                return same_again.instead(answer, text, memory) or answer
    part = named.about_the_thing(text, memory) if isinstance(memory, dict) else ""
    if part and _the_part_is_what_answers(part, memory):
        answer = _ask_a_rewritten_line(part, memory)
        if answer and not _said_before(answer, memory):
            return answer
    person = matters.about_them(text, memory) if isinstance(memory, dict) else ""
    if person:
        answer = _ask_a_rewritten_line(person, memory)
        if answer and not _said_before(answer, memory):
            return answer
    said_on_the_table = _the_answer_on_the_table(understood, memory)
    if said_on_the_table:
        return said_on_the_table
    return _the_line_again(text, memory)


_A_CLAUSE_OF_THE_ANSWER = 14


def _a_measure_about_the_subject(measure, text, memory, alone=""):
    if (alone and re.fullmatch(r"\s*how (?:much|many)\s*[?.!]*", str(text or ""), re.I)
            and asked_kind(text) == "amount"
            and SIGNALS["amount"].search(str(alone))):
        return ""
    word = named.subject_word(memory)
    if not word:
        return ""
    if named.a_newer_thing(memory, word):
        return ""
    reached = None
    faulty = named.a_faulty_thing(memory)
    if faulty and not _A_HOW_LONG.search(measure):
        faulty = False
    if faulty:
        thing = named.the_thing(memory)
        phrased = measure
        if thing and word and ("the " + word) in measure and thing != word:
            phrased = measure.replace("the " + word, "the " + thing, 1)
        asked_lines = [phrased.replace("the " + thing, "the " + thing + " repair", 1)
                       if thing and ("the " + thing) in phrased else phrased + " repair",
                       phrased + " repair"]
        if thing:
            asked_lines.append("how many days for a " + thing + " repair")
        for said in asked_lines:
            asked = find(understand(said, memory))
            if not (asked is not None and _the_entry_names(asked, word)
                    and _names_a_repair(asked)):
                continue
            told = _ask_a_rewritten_line(said, memory)
            if not told or _flat(told) == _flat(alone):
                continue
            measure, reached = said, asked
            break
    if reached is None:
        reached = find(understand(measure, memory))
    if faulty and _A_HOW_LONG.search(measure) and not _names_a_repair(reached):
        return ""
    if reached is None or not _the_entry_names(reached, word):
        if named.is_a_progress_ask(text) and named.a_figure_on_the_doing(memory, word):
            told = _ask_a_rewritten_line(measure, memory)
            if told:
                return told
        plan = _the_plan_said(memory)
        if not plan:
            return ""
        measure = measure + " " + plan
        reached = find(understand(measure, memory))
    if reached is None or not _the_entry_names(reached, word):
        return ""
    if _the_entry_names(find(understand(text, memory)), word) and not (
            faulty and _names_a_repair(reached)):
        return ""
    if alone and word in _flat(alone):
        return ""
    answer = _ask_a_rewritten_line(measure, memory)
    if not answer:
        return ""
    if _the_line_already_has_its_answer(alone, text) and not (
            faulty and _names_a_repair(reached)):
        return ""
    if same_again.unframed(answer):
        return ""
    last_said = _flat((mem.last_bot(memory) or ""))
    whole_amount = (asked_kind(text) == "amount"
                    and SIGNALS["amount"].search(str(answer or "")) is not None)
    if (last_said and _flat(answer) in last_said
            and len(_flat(answer).split()) < _A_CLAUSE_OF_THE_ANSWER and not whole_amount):
        return same_again.instead(str(mem.last_bot(memory) or ""), text, memory) or ""
    again_said = same_again.instead(answer, text, memory)
    if again_said and not whole_amount:
        return again_said
    if _said_before(_without_lead_in(answer), memory):
        return ""
    return answer


_A_SHORT_ANSWER = 12


def _the_line_already_has_its_answer(alone, text):
    if not _asks_only_the_length(text):
        return False
    said = _flat(alone or "")
    if not said or not A_FIGURE.search(said):
        return False
    return len(said.split()) <= _A_SHORT_ANSWER


_A_HOW_LONG = re.compile(r"\bhow\s+long\b", re.I)
_A_REPAIR = re.compile(
    r"\b(?:repair|repairs|repaired|fix|fixes|fixed|fixing|install|installs|installed|"
    r"installation|engineer|plumber|electrician|callout|call-out|call out|swap|swapping|job|"
    r"visit)\b", re.I)


def _names_a_repair(entry):
    if entry is None:
        return False
    flat = " ".join(str(group) for group in (getattr(entry, "key", ()) or ()))
    return bool(_A_REPAIR.search(flat))


def _the_entry_names(entry, word):
    if entry is None or not word:
        return False
    flat = " ".join(str(group) for group in (getattr(entry, "key", ()) or ())).lower()
    return bool(re.search(r"\b" + re.escape(word) + r"\w*", flat))


def _the_plan_said(memory):
    known = memory.get("user") if isinstance(memory.get("user"), dict) else {}
    return " ".join(str(known.get("plan") or "").split())


_PART_OF = re.compile(r"^\s*(?P<part>[a-z][a-z -]{1,24}?)\s+of\s+", re.I)


def _the_part_is_what_answers(part, memory):
    named_part = _PART_OF.match(part or "")
    if not named_part:
        return True
    wanted = {word for word in _PART_OF_WORDS.findall(named_part.group("part"))}
    if not wanted:
        return True
    item = find(understand(part, memory))
    if item is None:
        return True
    said = _key_words(item)
    return bool(wanted & said)


_PART_OF_WORDS = re.compile(r"[a-z]{3,}")

_ATTACHED_TO_THE_LAST_TURN = re.compile(
    r"\b(?:and|also|plus|too|what about|how about|its|it's|their|his|her)\b", re.I)


def _the_part_of_the_thing_they_named(text, memory):
    if not isinstance(memory, dict):
        return ""
    owner = named.the_thing_named(memory)
    if not owner:
        return ""
    part = named.about_the_thing(text, memory, owner=owner)
    on_its_own = named.about_the_thing(text, memory)
    if not part or not on_its_own or part == on_its_own:
        return ""
    if not _ATTACHED_TO_THE_LAST_TURN.search(text):
        return ""
    if _the_part_is_what_answers(on_its_own, memory):
        return ""
    if not _the_part_is_what_answers(part, memory):
        return ""
    filled = _ask_a_rewritten_line(part, memory)
    if not filled or _said_before(filled, memory):
        return ""
    return filled


def _the_report_is_answered(text, entry):
    if entry is None:
        return False
    said = " ".join(str(text or "").lower().split())
    keys = []
    for part in getattr(entry, "key", ()) or ():
        for alternative in (part if isinstance(part, (tuple, list, frozenset, set)) else (part,)):
            if isinstance(alternative, str):
                keys.extend(alternative.lower().split())
    if not keys:
        return False
    figures = re.findall(r"\d+(?:\.\d+)?\s*(?:%|percent|hours?|minutes?|days?|weeks?|litres?|"
                         r"liters?|kilos?|kg|metres?|miles?|pounds?)", said)
    if figures:
        for shape in getattr(entry, "shape", ()) or ():
            try:
                if shape(said):
                    return True
            except Exception:
                continue
        units = {word for figure in figures for word in re.findall(r"[a-z%]+", figure)}
        if units & set(keys):
            return True
    said_words = {word.strip(".,;:!?()") for word in said.split()}
    states = said_words & named.STATE_WORDS
    return any(any(key[:4] == state[:4] for key in keys) for state in states)


A_DEGREE = frozenset("""too very really quite rather so such more most less least much many
                        enough plenty lots lot bit little slightly far""".split())


def _the_fact_is_what_is_answered(text, stated, entry, memory=None):
    if entry is None:
        return False
    low = " ".join(str(text or "").lower().split())
    try:
        said = [str(turn.get("user") or "").lower() for turn in (memory or {}).get("turns", ())[-3:]]
    except (AttributeError, TypeError):
        said = []
    low = " ".join(said + [low])
    for hold in getattr(entry, "avoid", ()) or ():
        if isinstance(hold, str) and hold and hold.lower() in low:
            return False
    keys = []
    for part in getattr(entry, "key", ()) or ():
        for alternative in (part if isinstance(part, (tuple, list, frozenset, set)) else (part,)):
            if isinstance(alternative, str):
                keys.append(" ".join(alternative.lower().split()))
    if not keys:
        return False

    def tells(word):
        return any(re.search(r"\b" + re.escape(word) + r"(?:s|es)?\b", key) for key in keys)

    said = [word for word in re.findall(r"[a-z0-9']+", str(text or "").lower())
            if len(word) > 2 and word not in named.FACT_FILLER
            and word not in named.JOINING]
    told = [word for word in said if tells(word)]
    if not told or all(word in A_DEGREE for word in told):
        return False
    subject = str(stated or "").lower().split()
    subject = subject[0] if subject else ""
    return bool(said) and tells(subject)


def _ask_a_line_of_its_own(line, memory):
    spoke = {key: value for key, value in memory.items()
             if key not in ("topic", "topics", "entry_answer", "entry_answers", "last_answer")}
    return _ask_a_rewritten_line(line, spoke)


def _the_entry_key_words(entry):
    keys = []
    for part in getattr(entry, "key", ()) or ():
        for alternative in (part if isinstance(part, (tuple, list, frozenset, set)) else (part,)):
            if isinstance(alternative, str):
                keys.extend(alternative.lower().split())
    return keys


def _the_practice_is_answered(practice, entry):
    if entry is None:
        return False
    words = re.split(r"[^a-z]+", " ".join(str(practice or "").lower().split()))
    verbs = [word for word in words if word in named.CARE_VERBS]
    if not verbs:
        return False
    at = words.index(verbs[0])
    thing = [word for word in words[:at] if len(word) > 2]
    keys = _the_entry_key_words(entry)
    if not keys or not thing:
        return False
    same = any(_same_word(key, word) for key in keys for word in thing)
    if not same:
        return False
    return any(_same_word(key, verb) for key in keys for verb in verbs)


_A_YES_NO_ASK = re.compile(
    r"^(?:is|are|was|were|would|will|do|does|did|can|could|should|shall|have|has)\b", re.I)


MOAN_STOP = frozenset("""a an the my our your his her their its me i we you it that this these
those and or of to for in on at with from by up down out about right wrong""".split())


def _the_ask_behind_a_moan(text, memory):
    written = doing_it.the_ask_behind_a_moan(text)
    if not written:
        return ""
    said = _ask_a_rewritten_line(written, memory)
    if not said:
        return ""
    thing = written[len("how do i "):].rsplit(" right?", 1)[0]
    named = [word for word in WORD.findall(thing.lower())
             if len(word) > 2 and word not in MOAN_STOP and word not in MOAN_VERB_WORDS]
    if not named:
        return ""
    head = said_topic.stem(named[-1])
    answered = {said_topic.stem(word) for word in WORD.findall(said.lower())}
    if head not in answered:
        return ""
    if _said_before(_without_lead_in(said), memory):
        return ""
    return said


MOAN_VERB_WORDS = frozenset("get do make cook pick find manage".split())


def _ask_a_rewritten_line(line, memory):
    was = memory.get("understood")
    want = was.get("wants") if isinstance(was, dict) else None
    try:
        fresh = understand(line, memory)
        if want and isinstance(fresh, dict):
            fresh["wants"] = want
        memory["understood"] = fresh
        return _respond(line, memory)
    finally:
        if was is None:
            memory.pop("understood", None)
        else:
            memory["understood"] = was


_A_PERIOD = re.compile(
    r"\b(?:a|per|each|every|one)\s+(?:day|week|month)\b|\b(?:daily|weekly|monthly)\b", re.I)

BARE_SAY_NO = re.compile(
    r"^(?:how\s+(?:do|can|could|should)\s+i\s+"
    r"(?:say\s+no|refuse|turn\s+(?:something|it|that)\s+down)"
    r"|what\s+do\s+i\s+say\s+when\s+i\s+say\s+no)"
    r"(?:\s+without\s+feeling\b[^.!?,;:]*)?\s*[.!?]*\s*$", re.I)


def _turns_on_this_line(text, memory):
    wanted = _flat(text)
    if not wanted:
        return 0
    count = 0
    for turn in reversed(memory.get("turns") or []):
        if not isinstance(turn, dict):
            break
        if _flat(turn.get("user")) != wanted:
            break
        count += 1
    return count


def _without_lead_in(answer):
    for frame in AGAIN + (AGAIN_HELP,):
        head = frame.split("{reply}")[0]
        if answer.startswith(head):
            return answer[len(head):].strip()
    return same_again.unframed(answer) or answer


A_CALL_ASK = frozenset("""see seeing ring call contact phone gp doctor surgery nurse hospital
    dentist vet 111 999""".split())


def _the_line_again(text, memory):
    if not isinstance(memory, dict):
        return None
    if memory.get("frequency_reply"):
        behind = str(memory.get("frequency_answer") or "").strip()
        read = memory.get("understood")
        if (behind and isinstance(read, dict) and read.get("followup")
                and not read.get("change_of_subject") and not read.get("subject")
                and "recommend" not in (read.get("asks") or ())
                and not (A_CALL_ASK & set(read.get("words") or ()))):
            return AGAIN[0].format(reply=_repeat_short(behind, text, memory))
    if mem.last_module(memory) != "answers":
        return None
    said = _turns_on_this_line(text, memory)
    answer = _without_lead_in(str(mem.last_bot(memory) or "").strip())
    if not said or not answer:
        return None
    if said >= 3:
        return AGAIN_HELP.format(reply=answer)
    return AGAIN[said - 1].format(reply=_repeat_short(answer, text, memory))


_FRAME = frozenset("my our i the a an is was be been it its of on about and but so also then "
                   "now ok okay right well again too".split())
_MINE = frozenset("my our i me mine ours".split())
_SLOT_KEYS = frozenset(key for key, _ in recall.SUBJECTS)
_STORED_VALUE = {"budget": frozenset(("budget-how", "budget-split", "budget-rule"))}
_HOW_TO = re.compile(r"\b(?:how|help|make|sort|fix|plan|start|do)\b")
_COPULA = frozenset("is are was were s".split())


def _stated_with_copula(text, value):
    words = _flat(text).split()
    value_words = _flat(str(value)).split()
    if not words or not value_words:
        return False
    for start in range(len(words) - len(value_words) + 1):
        if words[start:start + len(value_words)] == value_words:
            return start > 0 and words[start - 1] in _COPULA
    return False


def _nothing_but_the_slot(said, value_words, about):
    rest = list(said)
    for word in value_words:
        if word in rest:
            rest.remove(word)
    left = [word for word in rest if word not in _FRAME]
    return bool(left) and all(word in about for word in left)


_COOKING_DOMAIN = frozenset(("cooking", "dishes", "meals", "food", "drink", "drinks"))


def _the_food_they_do_not_eat(text, understood):
    if not isinstance(text, str) or _HOW_TO.search(_flat(text)):
        return False
    reading = understood if isinstance(understood, dict) else {}
    if reading.get("asks") or reading.get("kind") == "question":
        return False
    stated = mem.facts.extract(text, question=False)
    if not mem.facts.foods_ruled_out(stated):
        return False
    item = find(understood)
    return item is not None and item.domain not in _COOKING_DOMAIN


def _store_keeps_the_line(text, understood):
    if not isinstance(text, str):
        return False
    item = find(understood)
    if item is None:
        return False
    about = _key_words(item)
    if not about:
        return False
    reading = understood if isinstance(understood, dict) else {}
    if reading.get("kind") == "statement":
        stated = mem.facts.extract(text, question=False)
        said = _flat(text).split()
        if isinstance(stated, dict):
            for slot, value in stated.items():
                words = _flat(str(value)).split()
                if item.id not in _STORED_VALUE.get(slot, ()):
                    continue
                if words and words != said and len(words) < len(said) \
                        and (_stated_with_copula(text, value)
                             or _nothing_but_the_slot(said, words, about)):
                    return True
    asked = recall.ask(text)
    if asked and not _HOW_TO.search(_flat(text)):
        return asked in about
    said = [word for word in _flat(text).split() if word not in _FRAME]
    if not said or not all(word in about for word in said):
        return False
    if not any(word in _MINE for word in _flat(text).split()):
        return False
    return all(word in _SLOT_KEYS for word in said)


_OVEN_CHECK_WORDS = ("check", "checking", "thermometer", "accurate", "runs hot", "running hot",
                     "too hot", "overheat", "overheats", "gone wrong", "be wrong",
                     "not heating", "not heat", "wont heat", "won't heat", "cold", "not working",
                     "broken", "fault", "smell", "smoke", "stays on", "stay on", "won't turn off",
                     "wont turn off", "keeps running", "noisy", "noise", "loud", "rattl",
                     "grinding", "squeak", "bulb", "element", "door", "seal", "hinge", "light")


_OVEN_WORDS = ("oven", "fan oven")


_PROPERTY_WORDS = ("temperature", "temp", "heat", "degrees", "gas", "gas mark", "how hot")


def _says_line(text, words):
    return any(phrase in text for phrase in words)
PICK_FRAME = re.compile(
    r"\b(?:what|which)\b[^?.!]{0,30}?\b(?:should|could|can|shall|would|do|might)\s+"
    r"(?:i|we|you)\s+(?:watch|read|listen\b|stream|binge)\b"
    r"|\b(?:recommend|suggest)\b[^?.!]{0,40}?\b(?:to watch|to read|to listen|podcast|podcasts|"
    r"film|films|movie|movies|book|books|album|albums|show|shows|series)\b",
    re.I)


def _a_pick_is_asked(text):
    return bool(PICK_FRAME.search(str(text or "")))


def _the_line_as_said(text):
    if not isinstance(text, str):
        return text
    from ..understanding.normalize import _a_leading_like_is_a_filler
    return _a_leading_like_is_a_filler(" ".join(text.lower().split()))


OFFICE_WHO = frozenset(SUMMONS_WHO) | frozenset("""
    social services health visitor home tax job centre jobcentre letting agent the
""".split())
OFFICE_ASKING = frozenset("""
    word words meeting meetings appointment appointments letter letters written wrote write
    writing rang ring ringing phoned phone called call calls message messages email emailed
    note notes see saw talk talks speak speaking discuss discussing chat meet come came coming
    quick asked ask asks asking want wants wanted need needs needed like would got receive
    received had saying told
""".split())


def _only_the_office(memory):
    understood = memory.get("understood") if isinstance(memory, dict) else None
    if not isinstance(understood, dict) or not isinstance(understood.get("summons"), dict):
        return False
    if understood.get("asks") or understood.get("kind") == "question":
        return False
    item = find(understood)
    if item is None:
        return False
    said = {str(word).lower().rstrip("s") for word in _key_words(item)}
    typed = {str(word).lower().rstrip("s") for word in (understood.get("keywords") or ())}
    shared = said & typed
    return bool(shared) and not (shared - OFFICE_WHO - OFFICE_ASKING)

def _a_food_named_of_its_own(understood, food):
    held = set(str(food or "").lower().split())
    if not held:
        return False
    for name in cooking.ingredients(understood) or ():
        if not set(str(name).lower().split()) & held:
            return True
    return False


def _keeping_about_the_food_there(memory, understood):
    if not isinstance(memory, dict) or not isinstance(understood, dict):
        return None
    if dishes.ask_kind(understood) != "keep":
        return None
    if not dishes.dish_for(memory, understood):
        return None
    if cooking.ingredients(understood):
        return None
    food = named.the_food_it_is_about(understood, memory)
    if not food or dishes.dish_in(food):
        return None
    if _a_food_named_of_its_own(understood, food):
        return None
    if not cooking.ingredients(understand(food, memory)):
        return None
    asked = understand("how long does cooked " + food + " keep in the fridge", memory)
    item, reply = _offer(lambda reject: find(asked, reject=reject), memory, asked)
    if getattr(item, "id", "") in GENERIC_KEEPING:
        return None
    return reply if isinstance(reply, str) and reply.strip() else None


def _the_answer_on_the_table(understood, memory):
    if not isinstance(memory, dict) or not isinstance(understood, dict):
        return None
    if dishes.ask_kind(understood) != "keep":
        return None
    food = named.the_food_it_is_about(understood, memory)
    if not food or food.lower() not in str(mem.last_user(memory) or "").lower():
        return None
    if _a_food_named_of_its_own(understood, food):
        return None
    turns = memory.get("turns")
    last = turns[-1] if isinstance(turns, list) and turns and isinstance(turns[-1], dict) else None
    if not last or last.get("module") != "answers":
        return None
    said_back = str(last.get("bot") or "")
    if not said_back.strip():
        return None
    trouble = (_carries(mem.last_user(memory)) - {word.lower() for word in food.split()}
               - _carries(food)) & _carries(said_back)
    if not trouble:
        return None
    return AGAIN[0].format(reply=_in_short(said_back))


def _already_on_the_screen(reply, memory, turns=4):
    mine = " ".join(str(reply or "").split()).lower()
    if not mine:
        return True
    seen = memory.get("turns") if isinstance(memory, dict) else None
    if not isinstance(seen, list):
        return False
    for turn in seen[-turns:]:
        if isinstance(turn, dict):
            said = " ".join(str(turn.get("bot") or "").split()).lower()
            if said and said == mine:
                return True
    return False


_READ_AGAIN = re.compile(
    r"\b(?:read|say|tell|sing)(?: it| that| this)?(?: again| once more)\b"
    r"|\bread it (?:back|to me again)\b"
    r"|\b(?:again|once more) please\b", re.I)
_VERSE_FORM_WORD = re.compile(
    r"\b(story|stories|tale|tales|poem|poems|rhyme|rhymes|rap|song|verse|limerick|haiku|"
    r"couplet|ode|sonnet)\b", re.I)


def _the_verse_said_again(text, memory):
    if not isinstance(text, str) or not _READ_AGAIN.search(text):
        return None
    turns = [turn for turn in ((memory or {}).get("turns") or []) if isinstance(turn, dict)]
    for turn in reversed(turns):
        said = str(turn.get("bot") or "")
        if not said:
            continue
        asked = str(turn.get("user") or "")
        if not (_VERSE_FORM_WORD.search(asked) or said.startswith("Once more")) or "\n" not in said:
            return None
        said = said[said.index("\n") + 1:] if said.startswith("Once more") else said
        lead, lines = said.split("\n", 1)
        if lead.rstrip().endswith(":"):
            return "Once more.\n" + lines
        return "Once more, then:\n" + said
    return None


_REPEAT_OPENS = re.compile(r"^(?:same as before|same answer|as i said|you've got it|you have it|"
                           r"i said|still)\b", re.I)

_A_BARE_MEASURE = re.compile(
    r"^\s*(?:(?:and|so|then|ok|okay)\s+)?how (?:much|many)"
    r"(?:\s+(?:is it|is that|does it cost|does that cost|again))?\s*[?.!]*$", re.I)


def _the_sentence_around(fragment, text):
    fragment = str(fragment or "").strip()
    text = str(text or "")
    if not fragment or not text:
        return ""
    flat_fragment = " ".join(fragment.split()).rstrip(".")
    lowered = " ".join(text.split())
    where = lowered.lower().find(flat_fragment.lower())
    if where < 0:
        return ""
    start = 0
    for match in re.finditer(r"(?<=[.!?])\s+", lowered[:where]):
        start = match.end()
    end = len(lowered)
    match = re.search(r"[.!?](?=\s|$)", lowered[where + len(flat_fragment):])
    if match:
        end = where + len(flat_fragment) + match.end()
    return lowered[start:end].strip()


def _the_sentence_with_a_figure(text):
    for sentence in SENTENCE.split(str(text or "")):
        said = sentence.strip()
        if (said and re.search(r"\d", said)
                and (SIGNALS["amount"].search(said) or SIGNALS["money"].search(said))):
            return said
    return ""

SAID_OUT_LOUD = re.compile(
    r"[\"“][^\"”]{6,}[\"”]|'[^']{8,}'"
    r"|^\s*(?:say|tell|ask|put it|word it|lead with|start with|open with|write)\b"
    r"|\b(?:ask|say|tell|raise)\b[^.?!]{0,40}\b(?:question|questions|sentence|words|wording)\b",
    re.I)


A_PERSON = (r"(?:gp|doctor|doctors|dentist|school|college|university|instructor|examiner|teacher"
            r"|tutor|head of year|manager|boss|employer|hr|personnel|union|careers|adviser"
            r"|advisor|consultant|council|citizens advice|solicitor|landlord|letting agent|vet"
            r"|pharmacist|midwife|health visitor|social worker|ombudsman|registrar|therapist)")
SAYING_IT_TO = re.compile(
    r"\b(?:ask|asked|asking|tell|telling|speak|speaking|talk|talking|ring|phone|call|email|write"
    r"|raise it|mention|sit down|take it|bring it up|have a word|report|complain)"
    r"\b[^.!?]{0,60}?\b" + A_PERSON
    + r"\b(?!['\u2019]s)",
    re.I)
YOUR_PERSON = re.compile(r"\byour\s+" + A_PERSON + r"\b(?!['\u2019]s)", re.I)
_TWO_SENTENCES = re.compile(r"\s*(?:[^.!?]*[.!?]){1,2}")


def _puts_it_to_someone(reply):
    words = " ".join(str(reply or "").split())
    if not words:
        return False
    found = _TWO_SENTENCES.match(words)
    opening = found.group(0) if found else words
    return bool(SAYING_IT_TO.search(opening) or YOUR_PERSON.search(opening))


def _the_ask_is_for_words(reading):
    try:
        return shapes.asks_for_words(reading)
    except Exception:
        return False


def _respond(text, memory):
    if isinstance(text, str):
        verse = _the_verse_said_again(text, memory)
        if verse:
            return verse
    if isinstance(text, str):
        baked = baking.written_out(text, memory)
        if baked and baked != text:
            asked = understand(baked, memory)
            item, reply = _offer(lambda reject: find(asked, reject=reject), memory, asked)
            if item is not None and reply and not _already_on_the_screen(reply, memory):
                return reply
        covered = outfit.the_sentence_answered(text, memory)
        if covered:
            return covered
        outfitted = outfit.written_out(text, memory)
        if outfitted and outfitted != text:
            asked = understand(outfitted, memory)
            item, reply = _offer(lambda reject: find(asked, reject=reject), memory, asked)
            if item is not None and reply and not _already_on_the_screen(reply, memory):
                return reply
        attributed = said_topic.attribute_of_the_thing(text, memory)
        if attributed and attributed != text:
            asked = understand(attributed, memory)
            item, reply = _offer(lambda reject: find(asked, reject=reject), memory, asked)
            if item is not None and reply:
                if _already_on_the_screen(reply, memory):
                    return repeat.pick(same_again.SHORT_AGAIN, memory,
                                       text).format(reply=reply)
                return reply[:1].upper() + reply[1:]
    if isinstance(text, str) and trips.the_bag_beats_the_list(text, memory):
        return None
    if _only_the_office(memory):
        return None
    if isinstance(text, str):
        verdict = shopping.the_verdict_on_a_present(memory, understand(text, memory))
        if verdict:
            return verdict
        longer = entertainment.the_verse_longer(text, memory)
        if longer:
            return longer
        another = entertainment.the_next_verse(text, memory)
        if another:
            return another
    if isinstance(text, str) and LIMIT_SHAPE.search(text):
        priced = _the_present_with_a_price(text, understand(text, memory), memory)
        if priced:
            return priced
    if (isinstance(memory, dict) and mem.last_module(memory) == "answers"
            and isinstance(memory.get("understood"), dict)
            and mem.asks_only(memory["understood"])
            and not memory["understood"].get("change_of_subject")
            and asked_kind(text) in ("amount", "money")
            and re.search(r"\bhow much\b", str(text or ""), re.I)
            and not re.search(r"\b(?:cost|costs|costing|price|prices|charge|charges)\b",
                              str(text or ""), re.I)):
        stated = same_as_before(memory["understood"], memory)
        if (stated and re.search(r"\d", str(stated))
                and flat(stated) != flat(mem.last_bot(memory) or "")
                and (SIGNALS["money"].search(stated) or SIGNALS["amount"].search(stated))):
            if _REPEAT_OPENS.match(str(stated)):
                stated = _REPEAT_OPENS.sub("", str(stated)).lstrip(" :,-")
            whole = _the_sentence_around(stated, mem.last_bot(memory) or "")
            if (whole and re.search(r"\d", whole[len(stated):])
                    and not _REPEAT_OPENS.match(whole)):
                return whole
            return stated
        same = (_the_sentence_with_a_figure(mem.last_bot(memory))
                if _A_BARE_MEASURE.fullmatch(str(text or "").strip()) else "")
        if same and not _REPEAT_OPENS.match(same):
            return same
    if _asks_who_the_bot_is(memory.get("understood"), text):
        return None
    if isinstance(text, str) and PLAN_RECALL.search(text) and _keeps_a_plan(memory):
        return None
    if limit.reads_the_answer(text, memory):
        return None
    if tried.might_be_a_report(text) and tried.pool_for(text, memory):
        return None
    if returned.pool_for(text, memory):
        return None
    if length.only_a_length(text) and ack.reply(text, memory):
        return None
    if mem.facts.a_name_picked(text, memory):
        return None
        return None
    if about_the_chat(text):
        return None
    if taste.asks_about_a_taste(_the_line_as_said(text)):
        return None
    if recall.ask(text) and not HOW_TO.search(_flat(text)):
        return None
    if taste.only_a_taste(_the_line_as_said(text)) and not _a_pick_is_asked(text):
        read = memory.get("understood") if isinstance(memory, dict) else None
        if not isinstance(read, dict):
            read = understand(text, memory)
        if not (dishes.has_a_diet_reply(memory, read)
                or dishes.has_a_dislike_reply(memory, read)
                or _a_choice_with_one_thing_left_out(text)):
            return None
    understood = memory.get("understood")
    if not isinstance(understood, dict):
        understood = understand(text, memory)
    introduction = mem.introduction_question(text, memory)
    if introduction:
        intro = understand(introduction, memory)
        item, reply = _offer(lambda reject: find(intro, reject=reject), memory, intro)
        if item is not None:
            return reply
    if _the_food_they_do_not_eat(text, understood):
        return None
    if _store_keeps_the_line(text, understood):
        return None
    if isinstance(text, str) and RECALL.search(text) and not recall.asks_for_a_word(text):
        return None
    if _a_bare_thanks(understood):
        rest = repeat.after_an_ack(text) if isinstance(text, str) else ""
        reread = understand(rest) if rest else None
        if (not isinstance(reread, dict) or reread.get("agrees_to_try")
                or reread.get("kind") in (None, "thanks", "greeting", "empty")):
            return None
        text, understood = rest, reread
    left_out = freshness.says_a_food_was_left_out(text)
    if not left_out:
        verdict = freshness.the_still_ok_follow_up(text, memory)
        if verdict:
            return verdict
    if not left_out and dishes.ask_kind(understood or {}) == "done":
        readied = dishes.follow_up(memory, understood)
        if isinstance(readied, str) and readied.strip():
            return readied
    if not left_out and _a_dish_was_offered(memory):
        planned = cooking.follow_up(understood, memory)
        if isinstance(planned, str) and planned.strip():
            return planned
    if _someones_else_diet(text, memory, understood):
        return None
    if _asks_about_their_taste(text):
        return None
    calculated = solve(text, understood, memory)
    if isinstance(calculated, str) and calculated.strip():
        return calculated
    if _filling_in_an_emergency(understood, memory):
        return None
    began = onset.reply(text, memory)
    if began:
        return began
    helped = _something_for(text)
    if helped:
        again = understand("what helps " + helped, memory)
        other, said = _offer(lambda reject: find(again, reject=reject), memory, again)
        if other is not None and isinstance(said, str) and said.strip():
            given_to = SOMETHING_FOR_GIVEN_TO.search(_flat(text).lower())
            if given_to:
                own, own_said = _offer(lambda reject: find(understood, reject=reject), memory,
                                       understood)
                if (own is not None and own is not other and isinstance(own_said, str)
                        and own_said.strip() and _keyed_on_the_person(own, given_to.group(1))):
                    return own_said
            return said
    planned = (None if left_out else
               cooking.follow_up(understood, memory) or cooking.first_plan(understood, memory))
    if isinstance(planned, str) and planned.strip():
        return planned
    reading = _without_names(understood)
    asked = _reword_ask(text)
    if asked is not None:
        if not asked:
            before = _last_rewrite(memory)
            if before is None:
                return ("Paste the words you want to send and I'll soften them: who it is going "
                        "to helps too.")
            asked, tones = before
            return _rewritten(asked, tones | _tone_of(text), from_followup=True)
        return _rewritten(asked, _tone_of(text))
    short_line = len(_flat(text).split()) <= 4
    if short_line and CONTINUED.search(_flat(text)):
        before = _last_rewrite(memory)
        if before is not None:
            asked, tones = before
            return _rewritten(asked, tones | _tone_of(text), from_followup=True)
    own = _own_thing(understood)
    cooked_ask = _a_cooking_ask_after_a_keeping_answer(understood, memory)
    if cooked_ask:
        return cooked_ask
    pointed = cooking.pointed(memory, understood)
    if (pointed is not None and pairing(text)
            and cooking.SIDE_ASKS.search(_flat(text).lower())):
        side = cooking.side_for(memory, _flat(text))
        if side:
            return side
    if pointed is not None:
        said = tuple(text for text in (cooking.recent_replies(memory) or (mem.last_bot(memory) or "",))
                     if text)
        picked = (cooking.dish(pointed, avoid=said)
                  or cooking.meal(pointed, avoid=said, pointed_back=True))
        if not (isinstance(picked, str) and picked.strip()) and not pointed.get("new_dish_only"):
            picked = cooking.dish(pointed)
            if not (isinstance(picked, str) and picked.strip()):
                again = cooking.meal(pointed)
                if isinstance(again, str) and again.strip():
                    picked = (("The one I'd go back to: " + again[0].lower() + again[1:])
                              if again in said else again)
        if (isinstance(picked, str) and picked.strip()
                and not cooking.unusable(picked, pointed)):
            return picked
    suits = cooking.suits_them(understood, memory)
    if isinstance(suits, str) and suits.strip():
        return suits
    without = cooking.a_dinner_without(understood, memory)
    if isinstance(without, str) and without.strip():
        return without
    named_foods = cooking.ingredients(reading)
    if len(named_foods) > 1 and not cooking.asks_a_food_fact(understood):
        cooked = (cooking.dish(understood, memory)
                  or cooking.meal(understood, memory=memory))
        if isinstance(cooked, str) and cooked.strip() and not cooking.unusable(cooked, understood):
            return cooked
    about_the_food = _keeping_about_the_food_there(memory, understood)
    if about_the_food:
        return about_the_food
    amount = _amount_asked(text, memory)
    if amount:
        return amount
    again = _the_amount_they_named_again(text, memory)
    if again:
        return again
    if cooking.keeping_ask(understood) and _asks_storing(memory):
        specific = _keeping_entry(text, memory, _keeping_thing(memory), storing=True)
        if isinstance(specific, str) and specific.strip():
            planned = _the_plan_keeps(understood, memory)
            if planned and _opening(planned) != _opening(specific):
                return planned
            return specific
    kept = cooking.keeping_followup(understood, memory)
    if isinstance(kept, str) and kept.strip():
        specific = _keeping_entry(text, memory)
        if isinstance(specific, str) and specific.strip():
            return specific
        planned = _the_plan_keeps(understood, memory)
        if planned:
            return planned
        return kept
    ours = _the_dish_time(understood, memory)
    if ours:
        return ours
    timed = cooking.timing_followup(understood, memory)
    if isinstance(timed, str) and timed.strip():
        return timed
    repaired = _the_machine_follow_up(text, reading, memory)
    if repaired:
        return repaired
    if not _care_holds(text, memory):
        announced = dishes.announced_part(memory, understood)
        if announced:
            return announced
    meal = mem.meal_follow_up(understood, memory)
    if meal is not None:
        _meal_entry, _meal_reply = _offer(lambda reject: find(meal, reject=reject), memory, meal)
        if _meal_reply:
            return _meal_reply
    if _A_PERIOD.search(str(text or "")):
        asks_a_part = False
    else:
        asks_a_part = not (own and _new_thing(own, _the_run_said(memory, mem.last_bot(memory) or ""))
                           and not mem.asks_only(understood))
    if asks_a_part and named.asks_a_part_of_the_trip(text, memory):
        asks_a_part = False
    if asks_a_part and mem.answer_about(text, memory):
        asks_a_part = False
    if asks_a_part and find(understood) is not None and understood.get("entities"):
        asks_a_part = False
    part = _part_asked(text, memory) if asks_a_part else None
    if part and cooking.keeping_ask(understood) and not FIGURE.search(part):
        part = None
    if part:
        return _the_part_said_again(part, text, understood, memory)
    again = _the_plan_said_again(understood, text, memory)
    if again:
        return again
    earlier = _last_answer(memory)
    if (earlier and asked_kind(text) and _names_a_property(text)
            and _only_a_property(keywords(text))
            and not _a_property_word_names_a_thing(text)
            and not RATE.search(text)):
        plan = _the_plan_for(text, memory, understood)
        if plan:
            return plan
        subject = mem.subject(memory)
        found, said = _the_answer_from_thing(text, subject, memory) if earlier else (None, None)
        if found is not None:
            for thing in _the_things_to_try(understood, memory):
                if thing == subject:
                    break
                newer, newer_said = _the_answer_from_thing(text, thing, memory)
                if newer is not None:
                    return newer_said
            return said
        words = set(keywords(text))
        keys = set(earlier.get("keys") or ())
        if not words or not words <= keys:
            if not _asks_only_the_length(text):
                return None
            part = same_as_before(understood, memory)
            if part:
                return part
            honest = _figure_missing(earlier.get("reply") or "", text)
            if honest:
                return honest
            return None
        fuller = _with_subject(text, memory)
        if fuller.strip() == text.strip():
            fuller = text if mem.written_out(text, memory) else _about_subject(text, memory)
        same = find(understand(fuller, memory)) if fuller.strip() != text.strip() else None
        if same is None or not _is_about(same, mem.subject(memory)):
            written = _written_ask_with_an_answer(text, memory)
            if written:
                fuller = written
            else:
                if not _asks_only_the_length(text):
                    return None
                part = same_as_before(understood, memory)
                if part:
                    return part
                honest = _figure_missing(earlier.get("reply") or "", text)
                if honest:
                    return honest
                return None
        reading = understand(fuller, memory)
    PLAN_FIRST = ("ahead", "fill", "sides")
    kind = dishes.ask_kind(understood)
    words = {str(word).lower() for word in (understood.get("words") or ())}
    if kind == "keep" and words & {"it", "that", "this", "them", "they"}:
        if _the_plan_answers_this(memory) or _cooked_thing(memory):
            PLAN_FIRST += ("keep",)
    if (kind == "temp" and _the_plan_answers_this(memory) and _says_line(text, _OVEN_WORDS)
            and not _says_line(text, _OVEN_CHECK_WORDS)):
        PLAN_FIRST += ("temp",)
        if own and str(own).lower() in _PROPERTY_WORDS:
            own = None
    if not own and kind in PLAN_FIRST and not _care_holds(text, memory):
        plan = dishes.follow_up(memory, understood)
        if plan:
            return plan
    off_topic = _off_the_topic(understood, memory)

    def _guard(reject):
        if not off_topic[1] and not off_topic[2]:
            return reject
        return lambda one: reject(one) or _from_another_domain(one, off_topic)

    keeping = _keeping_reader(reading, memory)
    item, reply = _offer(lambda reject: keeping(_guard(reject)), memory, reading)
    if item is not None and item.id == KEEPING_FROM_THE_ANSWER:
        return reply
    if not own and (understood or {}).get("kind") == "statement":
        detail = _a_detail_answered(text, memory)
        if detail is not None:
            return detail
        figure = _a_figure_the_answer_has(text, memory)
        if figure is not None:
            return figure
    if not own:
        beside = the_thing_a_detail_belongs_to(understood, memory)
        if beside is not None:
            vouched = find(beside)
            other, said = _offer(_keeping_reader(beside, memory), memory, beside)
            if (other is not None and vouched is not None
                    and getattr(other, "key", None) != getattr(vouched, "key", None)):
                other, said = None, ""
            if other is not None:
                if _said_before(said, memory) or _already_said(said, memory):
                    again = _the_detail_said_again(said, text, memory)
                    if again:
                        remember_answer(memory, said, _key_words(other))
                        _remember_answer(memory, other, said)
                        return again
                if getattr(other, "id", None) != getattr(item, "id", None):
                    item, reply, reading = other, said, beside
    if item is not None and not own:
        head = _head_thing(mem.subject(memory))
        other_food = _names_another_food(understood, str(mem.subject(memory) or "").lower())
        defined = _a_definition_of_the_entry(text, item)
        if head and not other_food and not defined and not _is_about(item, head):
            other, said = _offer(lambda reject: _in_context(text, memory, reject=_guard(reject)),
                                 memory, reading)
            if other is not None:
                item, reply = other, said
    if item is not None and not own and not _about_the_talk(item, text, memory, reading):
        item, reply = None, None
    follow_up = False
    if item is None:
        resized = resize.rewritten(text, memory)
        if resized:
            again = understand(resized, memory)
            calculated = solve(resized, again, memory)
            if (isinstance(calculated, str) and calculated.strip()
                    and flat(calculated) != flat(mem.last_bot(memory) or "")):
                return calculated
            item, reply = _offer(lambda reject: find(again, reject=_guard(reject)), memory, again)
            if item is not None:
                reading, own = again, _own_thing(again)
        if item is None:
            if (ADDING_TO_THE_SUBJECT.match(text)
                    and not A_MEASURE_OF_THE_SUBJECT.match(text)
                    and _the_answer_was_about_the_subject(memory)):
                other, said = _offer(
                    lambda reject: _in_context(text, memory, reject=_guard(reject)),
                    memory, reading)
                if other is not None:
                    item, reply = other, said
        if item is None:
            older = swap.rewritten(text, memory)
            readings = swap.candidates(text, memory) if swap.is_repair(text) else []
            if older and all(read[0] != older[0] for read in readings):
                readings.append(older)
            if not readings and older:
                readings = [older]
            handed = None
            for swapped in readings:
                again = understand(swapped[0], memory)
                other, said = _offer(lambda reject: find(again, reject=_guard(reject)), memory, again)
                same_answer = (_already_said(said, memory)
                               and _written_for(other, swapped[1]))
                thing = swap.thing(text)
                thing_words = set(re.findall(r"[a-z']+", str(thing or "").lower()))
                rest = " ".join(word for word in swapped[0].split()
                                if set(re.findall(r"[a-z']+", word.lower())) - thing_words)
                kept = _written_for(other, thing) and _more_than_the_thing(other, rest)
                if other is not None and (same_answer or kept
                                          or swap.names(swapped[1], said, text, memory,
                                                        question=swapped[0])
                                          or _about_the_rest_of_the_question(
                                              other, swapped[0], swap.thing(text))):
                    if same_answer or _already_said(said, memory):
                        said = _same_where_they_asked(text, said) or said
                    item, reply, reading = other, said, again
                    handed = (other, said, again)
                    break
            if handed is None and _a_place_they_asked(text) and _a_place_of_the_same_kind(
                    earlier, text):
                parting = _same_where_they_asked(text, mem.last_bot(memory) or "")
                if parting:
                    return parting

        if item is None:
            about_someone = swap.rewritten_person(text, memory)
            if about_someone:
                again = understand(about_someone[0], memory)
                other, said = _offer(lambda reject: find(again, reject=reject), memory, again)
                if other is not None and swap.names_person(about_someone[1], said, text,
                                                           mem.last_bot(memory)):
                    item, reply, reading = other, said, again
    PLAN_KINDS = ("fill", "sides", "done", "keep", "fix")
    care = item is None and _care_holds(text, memory)
    if item is None and not care:
        if dishes.ask_kind(understood) in PLAN_KINDS:
            plan = dishes.follow_up(memory, understood)
            if plan:
                return plan
        if mem.asks_only(understood) and mem.last_module(memory) == "answers":
            cooked = _a_cooking_ask_after_a_keeping_answer(understood, memory)
            if cooked:
                return cooked
            other_food = _names_another_food(understood, str(mem.subject(memory) or "").lower())
            if mem.has_time(mem.last_bot(memory)) and not other_food:
                said = same_as_before(understood, memory)
                if said and said != mem.last_bot(memory):
                    return said
            again = _the_entry_asked_again(text, memory)
            if again:
                return again
        if not care and mem.last_module(memory) == "answers" and _adds_a_figure(text):
            again = _the_entry_asked_again(text, memory)
            if again and _new_figure(again, mem.last_bot(memory)):
                return again
            if _the_plan_answers_this(memory) and not pairing(text):
                plan = dishes.follow_up(memory, understood)
                if plan:
                    said = 0 if pairing(text) else _answer_said(plan, memory)
                    if said >= 3:
                        return AGAIN_HELP.format(reply=plan)
                    if said:
                        return AGAIN[said - 1].format(reply=_repeat_short(plan, text, memory))
                    return plan
        follow_up = True
        if WHEN_AM_I.search(text):
            return None
        meal = mem.meal_follow_up(understood, memory)
        if meal is not None:
            reading = meal
        other_food = _names_another_food(understood, str(mem.subject(memory) or "").lower())
        own_thing = _names_its_own_thing(text, memory)
        item, reply = _offer(
            lambda reject: find(reading, reject=_guard(reject),
                                use_context=not other_food and not own_thing),
            memory, reading)
        if item is not None:
            owed = _the_outcome_owed(item, text)
            if owed and (_said_before(reply, memory)
                         or names_nothing_of_its_own(reading)):
                return owed
        if item is not None and _said_before(reply, memory):
            wider = mem.followup_reading(understood, memory)
            if isinstance(wider, dict) and wider is not understood:
                wider_item, wider_reply = _offer(
                    lambda reject: find(wider, reject=_guard(reject)), memory, wider)
                if wider_item is not None and wider_item.key != item.key:
                    reading, item, reply = wider, wider_item, wider_reply
        if item is not None and not _about_the_talk(item, text, memory, reading):
            item, reply = _offer(
                lambda reject: find(reading,
                                    reject=_in_this_conversation(_guard(reject), reading),
                                    use_context=not other_food and not own_thing),
                memory, reading)
        if item is None:
            item, reply = _offer(lambda reject: _in_context(text, memory, reject=_guard(reject)),
                                 memory, reading)

            chosen = _choosing(text, memory)
            if chosen is not None:
                reading, item, reply = chosen
    if item is None:
        item, reply = _offer(lambda reject: _in_bare_context(text, memory, reject=_guard(reject)),
                             memory, reading)
        follow_up = item is not None
    bare = False
    if item is None and not care:
        wider = followup_reading(understood, memory)
        if wider is not understood:
            reading = wider
            item, reply = _offer(lambda reject: find(reading, reject=_guard(reject)), memory, reading)
            bare = mem.bare_question(understood, memory)
            if item is not None and bare:
                figure = _asked_figure(text, reply, None)
                if figure:
                    reply = figure
            if item is not None and own and not _is_about(item, own):
                item, reply, reading = None, None, understood
            written_out = (understood is not reading
                           and mem.topics.the_prognosis_the_line_asks(understood, memory) is not None)
            if (item is not None and not written_out and not _leans_on(understood, item, memory)
                    and understood.get("kind") == "question"):
                someone = _the_person_to_call(text, memory)
                if someone:
                    return someone
                return None
            follow_up = item is not None
    if item is None and not care:
        written = _written_ask_with_an_answer(text, memory)
        if written:
            asked = understand(written, memory)
            item, reply = _offer(lambda reject: find(asked, reject=reject), memory, asked)
            if item is not None and not _is_about(item, mem.subject(memory)):
                item, reply = None, None
            if item is not None and not _answers_a_length(item, reply):
                item, reply = None, None
            if item is not None:
                reading, follow_up = asked, True
    if item is None and not care and mem.written_out(text, memory) \
            and not same_as_before(understood, memory):
        return None
    if item is None:
        about = _the_sentence_about(text, memory)
        if about:
            return about
        someone = _the_person_to_call(text, memory)
        if someone:
            return someone
        use_up = any(phrase in text.lower() for phrase in dishes.USE_UP_PHRASES)
        followed = None if (use_up or bare) else same_as_before(understood, memory)
        if isinstance(followed, str) and followed.strip() and not _new_thing(own, followed):
            return _the_part_said_again(followed, text, understood, memory)
        thinking = cooking.considered(understood, memory)
        if thinking:
            return thinking
        meal = None if amends_to(text) else cooking.meal(understood, text=text, memory=memory)
        if isinstance(meal, str) and meal.strip() and not cooking.unusable(meal, understood):
            return meal
        pointed = the_ask_about_the_thing_it_points_at(understood, memory)
        if pointed is not None:
            item, reply = _offer(lambda reject: find(pointed, reject=reject), memory, pointed)
            if item is not None and isinstance(reply, str) and reply.strip():
                return reply
        return cooking.without(understood)
    if getattr(item, "fault", False):
        kitchen = cooking.without(reading)
        if isinstance(kitchen, str) and kitchen.strip():
            return kitchen
    if not _usable(item, reading, memory):
        kitchen = cooking.without(reading)
        if isinstance(kitchen, str) and kitchen.strip():
            return kitchen
        item = _next_usable(item, reading, memory)
        if item is None:
            return kitchen
        reply = _payload(item, memory, reading)
        if not (isinstance(reply, str) and reply.strip()) and isinstance(kitchen, str):
            if kitchen.strip():
                return kitchen
    if isinstance(reply, str) and reply.strip():
        if not own and _reaches_another_subject(text, item, memory):
            return None
        said = (_answer_said(reply, memory)
                if mem.asks_only(understood) and not pairing(text) else 0)
        if (not own or _is_about(item, own)) and _only_a_size_of(item, text):
            sized = mem.sized_reply(reply, text, memory, _key_words(item))
            if sized:
                remember_answer(memory, reply, _key_words(item))
                return sized
        if not said and not follow_up and _said_before(reply, memory):
            part = narrow(reply, text)
            if isinstance(part, str) and part.strip() and flat(part) != flat(reply):
                part = _part_not_repeated(part, reply, memory)
                if part:
                    again = _the_detail_said_again(reply, text, memory)
                    if again:
                        return again
                    return part
        if CHOICE_ASK.match(" ".join(str(text or "").lower().split())):
            picked = _the_one_to_pick(text, memory)
            if picked:
                return picked
        same_line = _asked_again(text, reply, memory)
        if (not own and not same_line and _said_before(reply, memory)
                and not _names_another_food(understood, str(mem.subject(memory) or "").lower())
                and (not mem.written_out(text, memory) or same_as_before(understood, memory))):
            part = same_as_before(understood, memory)
            if (isinstance(part, str) and part.strip()
                    and flat(part) != flat(mem.last_bot(memory) or "")):
                return part
        if said and mem.written_out(text, memory) and not same_as_before(understood, memory):
            return None
        asked = max(same_line, said)
        if asked and _said_before(reply, memory):
            move = repeat.the_move(text, reply, memory)
            if move:
                return move
            if asked >= 3:
                return AGAIN_HELP.format(reply=reply)
            honest = _figure_missing(reply, text)
            if honest:
                return honest
            return AGAIN[asked - 1].format(reply=_repeat_short(reply, text, memory))
        framed = mem.said_again(reply, memory, line=None if said_topic.names_nothing(text) else text)
        if framed:
            return framed
        added = _the_new_part(reply, memory) if follow_up and _said_before(reply, memory) else None
        if added:
            remember_answer(memory, reply, _key_words(item))
            _remember_answer(memory, item, reply)
            return added
        if follow_up and _said_before(reply, memory):
            if _a_question_about_another_thing(text, reply, understood, memory, own, item):
                return None
            figure = _the_figure(text, reply)
            if figure:
                return figure
            chosen = _choosing(text, memory)
            if chosen is not None and not _said_before(chosen[2], memory):
                return chosen[2]
            same = same_as_before(understood, memory)
            if same:
                return same
            sentence = _the_sentence_about(text, memory)
            if sentence:
                return sentence
            if (isinstance(understood, dict) and understood.get("kind") == "question"
                    and _covered(text, reply, memory, understood)
                    and not _asks_of_another_subject(text, understood)):
                bare_ask = (not mem.topics.YES_NO.search(str(understood.get("clean") or ""))
                            and not [word for word in mem.content(str(understood.get("clean") or ""))
                                     if word not in ASKING and word not in BARE_GENERIC
                                     and word not in ASKING_VERBS and word not in PROPERTY_WORDS])
                if (bare_ask and isinstance(understood, dict)
                        and understood.get("kind") == "question"
                        and not _asks_of_another_subject(text, understood)):
                    return (same_again.instead(reply, text, memory)
                            or mem.said_again(reply, memory, line=text))
                return mem.said_again(reply, memory, line=text)
            return repeat.the_move(text, reply, memory)
        if not asked and follow_up and _already_said(reply, memory):
            figure = _the_figure(text, reply)
            if figure:
                return figure
            same = same_as_before(understood, memory)
            if same:
                return same
            if (isinstance(understood, dict) and understood.get("kind") == "question"
                    and not _asks_of_another_subject(text, understood)):
                return mem.said_again(reply, memory, line=text)
            return repeat.the_move(text, reply, memory)
        if asked >= 3:
            return AGAIN_HELP.format(reply=reply)
        if asked:
            honest = _figure_missing(reply, text)
            if honest:
                return honest
            return AGAIN[asked - 1].format(reply=_repeat_short(reply, text, memory))
        if not own and _said_before(reply, memory) and _covered(text, reply, memory, understood):
            again = _the_detail_said_again(reply, text, memory)
            if again:
                return again
            framed = mem.said_again(reply, memory)
            if framed:
                return framed
        if _a_question_about_another_thing(text, reply, understood, memory, own, item):
            return None
        remember_answer(memory, reply, _key_words(item))
        _remember_answer(memory, item, reply)
        return same_again.instead(reply, text, memory) or reply
    return None

from ..memory import again as _never_twice

respond = _never_twice.replied(respond)

from ..memory import paragraph

respond = paragraph.then_framed(respond)
