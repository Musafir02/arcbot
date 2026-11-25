import re

from ..understanding import kinds
from . import again, condition, repeat

JOIN_OPEN = re.compile(
    r"^(?:(?:and|but|so|oh|also|plus|then|well|yeah|yep|ok|okay|right|alright)\b[\s,]+)+", re.I)
COPULA_OPEN = re.compile(
    r"^\W*(?:(?:and|but|so|oh|also|well|yeah|yep|ok|okay|right|alright)\W+)*"
    r"(?:it'?s|it\s+is|its|they'?re|they\s+are|there'?s|there\s+is|there\s+are|"
    r"that'?s|this\s+is)\b\s*",
    re.I)
ABOUT_OPEN = re.compile(
    r"^\W*(?:(?:and|but|so|oh|also|well|yeah|yep|ok|okay|right|alright)\W+)*"
    r"(?:what|how)\s+about\b\s*", re.I)
PRONOUN_OPEN = re.compile(
    r"^\W*(?:(?:and|but|so|oh|also|well|yeah|yep|ok|okay|right|alright)\W+)*"
    r"(?:i\s*m|im|i\s+am|we\s*re|were|we\s+are)\b\s*", re.I)
PREPOSITION_OPEN = re.compile(
    r"^\W*(?:(?:and|but|so|oh|also|well|yeah|yep|ok|okay|right|alright)\W+)*"
    r"(?:with|for|on|in|at|by|near|from|like)\b\s*", re.I)
LIKE_OPEN = re.compile(
    r"^\W*(?:(?:and|but|so|oh|also|well|yeah|yep|ok|okay|right|alright)\W+)*like\b\s*", re.I)
TIME_WORDS = frozenset("""every each once twice thrice all most couple few several
    time times day days daily night nights nightly morning mornings afternoon afternoon
    evening evenings week weeks weekly month months monthly year years yearly hour hours
    minute minutes second seconds yesterday today tomorrow tonight lunch lunchtime teatime
    bedtime weekend weekends sometimes often always usually rarely never again ago since
    hourly sort of kind""".split())
A_PERSON_BODY = re.compile(
    r"^(?:my|our|his|her|their|your|the)\s+(?:mum|mom|dad|mother|father|sister|brother|son|"
    r"daughter|wife|husband|partner|boyfriend|girlfriend|friend|mate|colleague|boss|neighbour|"
    r"neighbor|nan|gran|grandma|grandad|grandpa|aunt|uncle|cousin|kid|kids|child|children|"
    r"baby|boy|girl|dog|cat|puppy|kitten|parents|family)\b", re.I)
AND_A_CLAUSE = re.compile(r"\band\s+(?:i|we|he|she|they|it|you|there)\s+\w", re.I)
DETAIL_BODY = re.compile(
    r"^(?:on|in|at|near|by|from|for|with|about|the|a|an|this|that|these|those|both|just)\b",
    re.I)
COUNT = (r"(?:\d+|one|two|three|four|five|six|seven|eight|nine|ten|a\s+few|couple\s+of|"
         r"several)")
QUANTITY_BODY = re.compile(
    r"^(?:" + COUNT + r")\s+(?:of\s+(?:us|them|you)|days?|weeks?|months?|nights?|hours?|"
    r"minutes?|people|adults|kids?|children|guests)\b", re.I)
MEASURE_BODY = re.compile(
    r"^(?:" + COUNT + r")\s*"
    r"(?:kg|kgs|kilo|kilos|kilogram|kilograms|g|gram|grams|lb|lbs|pound|pounds|oz|ounce|ounces|"
    r"stone|stones|litre|litres|liter|liters|ml|cl|cm|mm|metre|metres|meter|meters|inch|inches|"
    r"feet|foot|ft|miles?|km|degrees?|hours?|hrs?|minutes?|mins?|seconds?|days?|weeks?|months?)\b",
    re.I)
HAVE_COUNT = re.compile(
    r"^\W*(?:(?:and|but|so|oh|also|well|yeah|yep|ok|okay|right|alright)\W+)*"
    r"(?:we|i|weve|ive)\s+(?:(?:only|just)\s+)*(?:have|got|ve\s+got)\s+(?P<count>.+)$",
    re.I)
VAGUE = frozenset("""it its that this these those one ones thing things stuff
    the a an and but so oh also well yeah yep ok okay right alright
    really very quite just mainly mostly only also too as well now today later soon again""".split())
STATE = frozenset("""better worse ok okay fine sore stiff swollen tender aching painful easier
    harder bigger smaller good bad rubbish awful great healing improving recovered the same
    bit lot little much slightly more less worse off""".split())
MOST_WORDS = 9
STEP_WORDS = 14
SHORT_STEP = 8
JOIN_LEAD = re.compile(r"^(?:so|and|but|then|also|or|plus|because)\b[\s,]+", re.I)
LEADS_LEAD = (
    "{detail_cap} - same answer: {step}",
    "{detail_cap}, then. {step}",
    "{detail_cap}: {step}",
)
LEADS_FOR = (
    "Same answer for {thing}: {step}",
    "Same for {thing}: {step}",
    "For {thing}, the same: {step}",
)
PREPOSITION = re.compile(r"^(?:on|in|at|near|by|from|for|with|about|along|across|round|"
                         r"around|under|down)\b\s*", re.I)
A_SUBJECT_OF_ITS_OWN = re.compile(
    r"\b(?:i|im|i'm|ive|i've|id|i'd|he|hes|he's|she|shes|she's|they|theyre|they're|we|you|"
    r"it|its|it's)\b", re.I)
NAMES_NOTHING = re.compile(
    r"^(?:(?:the|a|an|this|that|these|those)\s+)?"
    r"(?:end|ends|beginning|start|meantime|meanwhile|moment|whole|same|fact|facts|case|cases|"
    r"point|first|last|least|most|main|long|short|past|future|addition|total|average|balance|"
    r"purpose|way|ways|sense|practice|theory|hindsight|conclusion|contrast|order|mind|own|"
    r"once|now|ages|while|time|times)\b"
    r"|(?:my|your|his|her|their|our|its)\s+(?:case|part|opinion|view|mind|experience|defence|"
    r"book|own|shoes|honour)\b"
    r"|(?:general|particular|large|all|once|now|ages)\b", re.I)
A_WHEN = re.compile(
    r"^(?:in|on|at|by|before|after|until|till|within|during)\s+(?:the\s+|a\s+|an\s+)?"
    r"(?:\d+|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|few|couple|"
    r"monday|tuesday|wednesday|thursday|friday|saturday|sunday|weekday|weekend|"
    r"january|february|march|april|may|june|july|august|september|october|november|december|"
    r"morning|afternoon|evening|night|week|fortnight|month|year|day|hour|minute|"
    r"tomorrow|tonight|today)\w*", re.I)

A_PLACE = (r"(?:front|back|rear|bottom|top|inside|outside|underneath|under|side|corner|edge|"
           r"middle|floor|door|seal|hose|filter|drum|pump|tank|pipe|valve|tap|wheel|tyre|tire|"
           r"chimney|gutter|roof|celling|wall|window|sill|radiator|boiler|toilet|basin|shower|"
           r"socket|switch|handle|lid|drawer|join|connection)")
SHOWS_OUT = re.compile(
    r"\b(?:com(?:e|es|ing)|comin|leak(?:s|ing|ed)?|drip(?:s|ping|ped)?|seep(?:s|ing|ed)?|"
    r"run(?:s|ning)?|pour(?:s|ing|ed)?|spray(?:s|ing|ed)?|blow(?:s|ing)?)\s+out(?:\s+of)?\s+"
    r"(?=(?:the\s+)?" + A_PLACE + r"\b)", re.I)
SHOWS_FROM = re.compile(
    r"\b(?:com(?:e|es|ing)|comin|leak(?:s|ing|ed)?|drip(?:s|ping|ped)?|seep(?:s|ing|ed)?|"
    r"run(?:s|ning)?|pour(?:s|ing|ed)?|spray(?:s|ing|ed)?|blow(?:s|ing)?)\s+"
    r"(?=from\s+(?:the\s+)?" + A_PLACE + r"\b)", re.I)


FALTER = re.compile(
    r"^\W*(?:(?:and|but|so|oh|also|well|yeah|yep|ok|okay|right|alright)\W+)*"
    r"(?:it|its|it'?s|they|they'?re|he|she|that|this|the\s+\w+|my\s+\w+|our\s+\w+)\s+"
    r"[a-z']+\s+(?=(?P<place>(?:at|on|in|along|across|round|around|near|by|under|down)\s+"
    r"(?:(?:the|my|its|their|your)\s+)?" + A_PLACE + r"\b))", re.I)

DETERMINER = frozenset("""a an the my our your their his her its some this that these those
    two three few both""".split())


def _a_verb(word, before=""):
    if before in DETERMINER:
        return False
    return word in kinds.VERBISH or word in kinds.VERB_FORMS


def _flat(text):
    return " ".join(str(text or "").split())


def _the_same_answer_as_the_one_it_narrows(step, said):
    here, there = _flat(step).lower()[:60], _flat(said).lower()[:60]
    return bool(here) and here == there


def _words(text):
    return re.findall(r"[a-z']+", _flat(text).lower())


SPAN_ONLY = re.compile(
    r"^\W*(?:(?:and|but|so|oh|also|well|yeah|yep|ok|okay|right|alright)\W+)*"
    r"(?:it'?s|it\s+is|its|it\s+has|thats|that'?s|that\s+is|ive|i\s+have)\s+"
    r"(?:been\s+)?(?P<span>(?:(?:about|around|nearly|almost|over|just\s+over)\s+)?"
    r"(?:\d+|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|"
    r"a\s+few|couple\s+of|a|several)\s+"
    r"(?:day|week|month|year|fortnight|hour|minute)s?"
    r"(?:\s+(?:now|or\s+so|or\s+more|already))?)\s*$", re.I)


def the_detail(text):
    said = _flat(text)
    if not said or "?" in said:
        return None
    said = " ".join(SHOWS_OUT.sub("from ", SHOWS_FROM.sub("", said)).split())
    joined = JOIN_OPEN.sub("", said).strip()
    if joined and joined != said and PREPOSITION.match(joined):
        said = joined
    if PREPOSITION.match(said) and (
            _names_nothing(said) or A_SUBJECT_OF_ITS_OWN.search(said)):
        return None
    words = said.split()
    if len(words) > MOST_WORDS:
        return None
    span = SPAN_ONLY.match(said)
    if span:
        return "for " + " ".join(span.group("span").split())
    counted = HAVE_COUNT.match(said)
    counted_rest = None
    if counted and QUANTITY_BODY.match(counted.group("count")):
        counted_rest = counted.group("count").strip()
    falter = FALTER.match(said)
    if falter:
        return falter.group("place").strip()
    body_words = [w for w in _words(said) if w not in ("is", "are", "was", "were", "be", "been")]
    like_head = LIKE_OPEN.match(said)
    if like_head:
        body_words = [w for w in _words(said[like_head.end():])
                      if w not in ("is", "are", "was", "were", "be", "been")]
    if counted_rest is None and any(
            _a_verb(w, before) for before, w in zip([""] + body_words, body_words)):
        return None
    opener = None
    rest = None
    for opener in (ABOUT_OPEN, LIKE_OPEN, COPULA_OPEN, PRONOUN_OPEN):
        stripped = opener.sub("", said).strip()
        if not stripped or stripped == said:
            continue
        if opener is not PRONOUN_OPEN and opener is not LIKE_OPEN and not (
                DETAIL_BODY.match(stripped)
                or (opener is COPULA_OPEN and (QUANTITY_BODY.match(stripped)
                                               or MEASURE_BODY.match(stripped)))):
            return None
        rest = stripped
        break
    if rest is None:
        if counted_rest is not None:
            opener = HAVE_COUNT
            rest = counted_rest
        elif not PREPOSITION_OPEN.match(said):
            return None
        else:
            rest = said
            if LIKE_OPEN.match(rest):
                rest = LIKE_OPEN.sub("", rest).strip(" .,;:")
                if not rest:
                    return None
    if opener is PRONOUN_OPEN and not PREPOSITION.match(rest):
        return None
    rest = rest.strip(" .,!;:")
    if not rest or AND_A_CLAUSE.search(rest):
        return None
    content = [w for w in _words(PREPOSITION.sub("", rest)) if w not in VAGUE]
    if not content:
        return None
    if all(word in TIME_WORDS for word in content):
        return None
    if A_PERSON_BODY.match(rest):
        return None
    if all(word in STATE for word in content):
        return None
    return rest


A_FIGURE = re.compile(
    r"\b\d+(?:[.,]\d+)?\s*(?:k|km|kms|kilometres?|kilometers?|miles?|mi|metres?|meters?|m|"
    r"mins?|minutes?|hours?|hrs?|h|kg|kilos?|lb|lbs|stone|st|litres?|liters?|degrees?|"
    r"secs?|seconds?|days?|weeks?)\b", re.I)
THE_PERSON = re.compile(r"\b(?:i|im|i'm|ive|i've|we|we're|we've|my|our)\b", re.I)
ASKING_ME = re.compile(
    r"^\W*(?:(?:and|but|so|oh|also|well|yeah|yep|ok|okay|right|alright)\W+)*"
    r"(?:can|should|could|would|do|does|did|is|are|will|shall)\s+(?:i|we)\b", re.I)
FACT_SENTENCE_WORDS = 5


def _a_figure(word):
    return re.sub(r"\s+", "", word.lower()).rstrip(".,")


def the_fact_the_answer_has(text, memory):
    if not memory:
        return None
    said = _flat(text)
    if not said or "?" in said or len(said.split()) > MOST_WORDS:
        return None
    if not THE_PERSON.search(said) or ASKING_ME.match(said):
        return None
    wanted = {_a_figure(found.group(0)) for found in A_FIGURE.finditer(said)}
    if not wanted:
        return None
    reply = ""
    for back, _asked, answer in repeat._recent_answers(memory):
        if back > 1:
            break
        if answer:
            reply = str(answer)
            break
    if not reply:
        return None
    sentences = [part.strip() for part in re.split(r"(?<=[.!?])\s+", reply) if part.strip()]
    if len(sentences) < 2:
        return None
    for sentence in sentences:
        if len(sentence.split()) < FACT_SENTENCE_WORDS:
            continue
        there = {_a_figure(found.group(0)) for found in A_FIGURE.finditer(sentence)}
        if there & wanted:
            said_back = sentence if sentence.endswith((".", "!", "?")) else sentence + "."
            return said_back[:1].upper() + said_back[1:]
    return None


def the_step_for(text, memory):
    if not memory:
        return None
    detail = the_detail(text)
    if not detail:
        return None
    from ..compose import trouble
    if trouble.reads_as_trouble(_flat(text)):
        return None
    own = None
    own_read = False
    for back, asked, said in repeat._recent_answers(memory):
        if back > 2:
            continue
        if back > 1 and not repeat._about_the_same_thing(asked, said, memory):
            continue
        plain = _without_branches(said)
        if not plain:
            if not own_read:
                own = _the_thing_itself(detail, memory)
                own_read = True
            if own:
                return detail, said, own, True
            if _another_thing(detail, said):
                worth = _what_it_is_worth(detail, memory)
                if worth:
                    return detail, said, worth, True
            continue
        step = _step_about(plain, detail)
        if _a_count(detail):
            step = _the_figure(plain) or step
        if not step:
            if not own_read:
                own = _the_thing_itself(detail, memory)
                own_read = True
            if own:
                return detail, said, own, True
            if _another_thing(detail, said):
                worth = _what_it_is_worth(detail, memory)
                if worth:
                    return detail, said, worth, True
            if _asks_about_a_new_thing(text, detail, said):
                continue
            if _is_a_span(detail):
                step = (_a_span_step(plain, detail) or _first_instruction(plain)
                        or _opening_said(plain))
            else:
                step = _a_step(plain)
                if not step and _says_where(detail):
                    step = _first_instruction(plain) or _opening_said(plain)
        if not step:
            continue
        if repeat._already_repeated(step, memory):
            step = _first_clause(step)
            if not step or repeat._already_repeated(step, memory):
                return None
        return detail, said, step, False
    return None


TIME_OF_DAY = frozenset("""morning mornings afternoon afternoons evening evenings night nights
    night-time nighttime daytime bedtime lunchtime teatime weekend weekends weekday weekdays
    monday tuesday wednesday thursday friday saturday sunday""".split())
FREQUENCY = frozenset("""every each once twice thrice couple few several most usually often
    sometimes always daily nightly weekly monthly""".split())
A_QUALIFIER = frozenset("""mostly mainly usually generally especially worse worst better
    particularly right first thing late early""".split())
A_GREETING = re.compile(r"^(?:good\s+)?(?:morning|afternoon|evening|night|night night|"
                        r"gnight|nighty night)$", re.I)
A_DANGLING = frozenset("""in on at by of to from for with about the a an and or than as""".split())
A_COUNT_WORD = frozenset("""one two three four five six seven eight nine ten eleven twelve
    thirteen fourteen fifteen sixteen seventeen eighteen nineteen twenty thirty forty fifty
    hundred thousand""".split())
A_TIME_IDIOM = ("first thing", "first thing in the morning", "middle of the night",
                "all day", "all night", "an odd night", "every so often")
A_SMALL_WORD = frozenset("""in on at by of to from and or the a an this that these those
    thing things time times""".split())
LEADS_FOR_A_TIME = (
    "{detail_cap}, then. {step}",
    "{detail_cap} - the same steps: {step_low}",
)


def the_time_in_the_line(text):
    said = _flat(text)
    if not said or "?" in said or len(said.split()) > MOST_WORDS:
        return None
    said = " ".join(SHOWS_OUT.sub("from ", SHOWS_FROM.sub("", said)).split())
    body = said
    for opener in (ABOUT_OPEN, LIKE_OPEN, COPULA_OPEN, PRONOUN_OPEN):
        stripped = opener.sub("", body).strip()
        if stripped and stripped != body:
            body = stripped
            break
    body = re.sub(r"^(?:but|and|so|oh|also|well|yeah|yep|ok|okay|right|alright)[\s,]+", "", body,
                  flags=re.I).strip()
    words = _words(body)
    if not words or len(words) > MOST_WORDS:
        return None
    if any(_a_verb(word, before) for before, word in zip([""] + words, words)):
        return None
    if A_GREETING.match(body.strip(" .,!;:")):
        return None
    if words[-1] in A_DANGLING:
        return None
    if any(word in A_COUNT_WORD or word.isdigit() for word in words):
        return None
    for idiom in A_TIME_IDIOM:
        if body.strip().lower() == idiom:
            return body.strip(" .,!;:")
    content = [word for word in words if word not in VAGUE and word not in STATE
               and word not in A_QUALIFIER and word not in A_SMALL_WORD]
    if not content or not all(word in TIME_WORDS for word in content):
        return None
    if not any(word in TIME_OF_DAY or word in FREQUENCY for word in content):
        return None
    return body.strip(" .,!;:")


def _a_time_step(said, detail):
    named = [word for word in _words(detail) if word in TIME_WORDS]
    if not named:
        return None
    for sentence in re.split(r"(?<=[.!?])\s+", _flat(said)):
        here = _words(sentence)
        if any(word in here for word in named):
            sentence = sentence.strip()
            if sentence and len(sentence.split()) >= 3:
                return sentence
    return None



def _the_answer_before(memory, text):
    turns = (memory or {}).get("turns") if isinstance(memory, dict) else None
    if not isinstance(turns, list):
        return ""
    here = _flat(text).lower().rstrip(".!?, ")
    for turn in reversed(turns):
        if not isinstance(turn, dict):
            continue
        said = _flat(turn.get("user")).lower().rstrip(".!?, ")
        if not said or (here and said == here):
            continue
        reply = _flat(turn.get("bot"))
        if reply:
            return reply
    return ""


def the_step_for_a_time(text, memory):
    if not memory:
        return None
    detail = the_time_in_the_line(text)
    if not detail:
        return None
    from ..compose import trouble
    if trouble.reads_as_trouble(_flat(text)):
        return None
    said = _the_answer_before(memory, text)
    if not said:
        return None
    if repeat.NEXT_STEP_EMERGENCY.search(said):
        return None
    plain = _without_branches(said) or _flat(said)
    step = _a_time_step(plain, detail) or _first_instruction(plain) or _a_step(plain)
    if not step:
        return None
    if repeat._already_repeated(step, memory):
        step = _first_clause(step)
        if not step or repeat._already_repeated(step, memory):
            return None
    return detail, said, step, False


COUNTED_DETAIL = re.compile(
    r"^(?:" + COUNT + r")" + r"\s+(?:of\s+(?:us|them|you)|people|adults|kids?|children|"
    r"guests|portions|slices|days|weeks?|months?|nights?|hours?|minutes?)\b", re.I)
FIGURED = re.compile(r"\d")


def _a_count(detail):
    return bool(COUNTED_DETAIL.match(_flat(detail)))


def _the_figure(said):
    for sentence in re.split(r"(?<=[.!?])\s+", _flat(said)):
        sentence = sentence.strip()
        if sentence and FIGURED.search(sentence):
            return sentence
    return None


ASKS_A_PART = re.compile(
    r"^(?:(?:and|but|so|also|oh|well|yeah|yep|ok|okay|right|alright)\s+)*"
    r"(?:what|which|how much|how many|how long|how often|when|where|why|do|does|did|should|"
    r"shall|can|could|would|will|is|are|was|were|the|that|those|these)\b", re.I)
ASKING = frozenset("""what which how much many long often when where why who whom whose do does
    did should shall can could would will is are was were i me my we our us you your they them
    their it its that this these those the a an and but so also too oh well yeah yep ok okay
    right alright now then just really very please
    need needs needed want wants like get gets got have has had there here one any some
    again more""".split())
A_PART_WORDS = 26


def _the_carrying_words(text):
    if not any(len(word) > 3 for word in _words(text) if word not in ASKING):
        return []
    return [word.rstrip("s") for word in _words(text)
            if word not in ASKING and len(word) > 2]


def _the_clause_that_holds(words, said):
    wanted = set(words)
    for sentence in re.split(r"(?<=[.!?])\s+", _flat(said)):
        here = {word.rstrip("s") for word in _words(sentence)}
        if not wanted & here:
            continue
        clauses = [piece.strip(" ,;:-") for piece in _clauses(sentence) if piece.strip(" ,;:-")]
        best = max(clauses, key=lambda piece: len(wanted & {w.rstrip("s") for w in _words(piece)}),
                   default="")
        held = wanted & {word.rstrip("s") for word in _words(best)}
        if not held or not best:
            continue
        best = JOIN_LEAD.sub("", best).strip()
        if len(best.split()) < 4:
            best = JOIN_LEAD.sub("", _flat(sentence)).strip(" ,;:-")
        if not best or len(best.split()) > A_PART_WORDS:
            continue
        return best[:1].upper() + best[1:]
    return ""


def the_part_of_the_answer(text, memory):
    said = _flat(text)
    if not said or len(said.split()) > MOST_WORDS or not ASKS_A_PART.match(said):
        return ""
    carrying = _the_carrying_words(said)
    if not carrying:
        return ""
    from ..compose import trouble
    if trouble.reads_as_trouble(said):
        return ""
    answer = ""
    for back, _asked, said_before in repeat._recent_answers(memory):
        if back > 1:
            break
        if said_before:
            answer = str(said_before)
            break
    if not answer:
        return ""
    there = {word.rstrip("s") for word in _words(answer)}
    if any(word not in there for word in carrying):
        return ""
    clause = _the_clause_that_holds(carrying, answer)
    if not clause:
        return ""
    if repeat._already_repeated(clause, memory):
        return ""
    return clause if clause.endswith((".", "!", "?")) else clause + "."


def answers_the_line(text, memory):
    return the_step_for(text, memory) is not None or the_step_for_a_time(text, memory) is not None


def answer_for(text, memory):
    found = the_step_for(text, memory)
    a_time = False
    if found is None:
        found = the_step_for_a_time(text, memory)
        a_time = found is not None
    if found is None:
        a_part = the_part_of_the_answer(text, memory)
        if a_part:
            return repeat._handed_back(memory, a_part)
        return None
    detail, said, step, whole = found
    if whole and _the_same_answer_as_the_one_it_narrows(step, said):
        return None
    if whole:
        framed = again.a_thing_of_the_answer(step, text, memory)
        repeat._handed_back(memory, step)
        return framed or step
    thing = PREPOSITION.sub("", detail).strip() or detail
    if a_time:
        reply = repeat.pick(LEADS_FOR_A_TIME, memory, text).format(
            detail_cap=_capital(detail), thing=thing, step=_capital(step),
            step_low=step[:1].lower() + step[1:])
        return repeat._handed_back(memory, reply)
    leads = LEADS_LEAD if thing != detail else LEADS_FOR
    reply = repeat.pick(leads, memory, text).format(
        detail_cap=_capital(detail), thing=thing, step=_capital(step))
    return repeat._handed_back(memory, reply)


PLAIN_ASK = re.compile(
    r"^(?:(?:ok|okay|so|and|but|then|right|yeah|yes|hmm)[\s,]+)*"
    r"(?:what|whats|what's|where|wheres|which|how|hows|how's)\b", re.I)

ASK_ONLY = frozenset("""what whats what's where wheres which how hows how's do does did should would could can shall will i we you
me us it that this these those them they he she one ones the a an my our your their his her its
best good right next first thing things bit bits way ways time put use add get buy need want take
clean start make there in on for to with of about at from into more else other any some all
now tonight today tomorrow evening weekend afternoon morning week month please just tell again
honestly actually really still also even lets let go on ok okay so right yeah yes hmm then but
and though well""".split())

A_QUANTITY_ASK = re.compile(r"\b(?:how\s+(?:much|many|long|often)|much|many|long|often)\b", re.I)

A_WHEN = re.compile(r"\b(tonight|today|tomorrow|now|this evening|this weekend|this afternoon|"
                    r"first|next)\b", re.I)

PLAIN_LEADS = ("For that, {step}",
               "That's the bit that matters: {step}",
               "What I would start with: {step}",
               "For that one, {step}")

STEP_ANSWERS = ("answers", "memory_store", "safety")
A_STEP_ANSWER = 50


def _the_answer_just_given(memory):
    turns = [turn for turn in (memory.get("turns") or []) if isinstance(turn, dict)]
    if not turns:
        return ""
    last = turns[-1]
    if last.get("module") not in STEP_ANSWERS:
        return ""
    said = str(last.get("bot") or "").strip()
    if len(said) < A_STEP_ANSWER or said.rstrip().endswith("?"):
        return ""
    return said


def _bare_step(step):
    if len(step) > 1 and step[:2] == step[:2].upper():
        return step
    return step[:1].lower() + step[1:]


def the_plain_ask(text, memory):
    if not memory:
        return None
    said = _flat(text)
    words = said.lower().split()
    if not words or len(words) > MOST_WORDS or not PLAIN_ASK.match(said):
        return None
    if A_QUANTITY_ASK.search(said):
        return None
    for word in words:
        if word.strip("?,.!;:") not in ASK_ONLY:
            return None
    answer = _the_answer_just_given(memory)
    if not answer:
        return None
    step = _a_step(answer) or _first_instruction(answer)
    if not step or len(step.split()) < 2:
        return None
    if repeat._handed_back_already(step, memory):
        return None
    when = A_WHEN.search(said)
    if when:
        reply = _capital(when.group(1)) + " - " + _bare_step(step)
    else:
        reply = repeat.pick(PLAIN_LEADS, memory, text).format(step=_bare_step(step))
    return repeat._handed_back(memory, reply)


CLAUSE = re.compile(r"[,;:]\s+|\s+-\s+")


def _clauses(move):
    out, piece, depth = [], [], 0
    for chunk in CLAUSE.split(move):
        depth += chunk.count("(") - chunk.count(")")
        if piece and depth:
            piece.append(chunk)
            continue
        if piece:
            out.append(", ".join(piece))
            piece = []
        piece = [chunk]
    if piece:
        out.append(", ".join(piece))
    return out


def _first_clause(step):
    pieces = [p.strip(" ,;:-.") for p in _clauses(step.rstrip(".")) if p.strip(" ,;:-.")]
    if not pieces:
        return ""
    return pieces[0] + "."


NAME_ONLY = frozenset("""a an the my our your their his her its some this that these those and
    or with without for of in on at to it them they both two three few""".split())

NOT_A_THING = frozenset("""
think thinks thinking thought know knows knowing say says saying tell tells telling ask asks
asking wonder wonders wondering guess guesses guessing consider considers considering decide
              decides deciding choose chooses choosing help helps helping do does doing work works
want wants wanting need needs needing like likes liking get gets getting make makes making
""".split())


def _one_of_a_list(clauses, groups, at):
    return len(clauses) > 1 or at + 1 < len(groups)


def _head_word(detail):
    words = [w for w in _words(PREPOSITION.sub("", detail)) if w not in VAGUE]
    return words[-1] if words else ""


def _subject_words(memory):
    from . import topics
    turns = [t for t in (memory.get("turns") or []) if isinstance(t, dict)]
    asked = str(turns[-1].get("user") or "") if turns else ""
    said = str(turns[-1].get("bot") or "") if turns else ""
    out = []
    for source in (topics.subject(memory) or "", asked):
        for word in source.split():
            word = re.sub(r"[^a-z]", "", word.lower())
            if len(word) > 2 and word not in VAGUE and word not in topics.STOPWORDS:
                out.append(word)
    seen, both, rest = set(), [], []
    for word in out:
        if word in seen:
            continue
        seen.add(word)
        (both if re.search(r"\b" + re.escape(word) + r"\b", said.lower()) else rest).append(word)
    return (both + rest)[:6]


def _the_entry_reply(found):
    reply = getattr(found, "reply", "") if found is not None else ""
    return reply if isinstance(reply, str) else ""


def _another_thing(detail, said):
    if not _head_word(detail) or _head_word(detail) in NOT_A_THING:
        return False
    if PREPOSITION.match(_flat(detail)):
        return False
    want = {word.rstrip("s") or word for word in _words(detail) if word not in VAGUE}
    have = {word.rstrip("s") or word for word in _words(said)}
    if not want or want & have:
        return False
    return True


def _what_it_is_worth(detail, memory):
    head = _head_word(detail)
    if not head:
        return None
    try:
        from ..understanding import understand
        from ..knowledge import lookup as lookup_mod
        from ..modules import answers
        understood = understand("should i get " + detail, {}) or {}
        found = lookup_mod.find(understood)
        reply = answers._payload(found, memory, understood)
    except Exception:
        return None
    if not _says_about(reply, head):
        return None
    if repeat._already_repeated(reply, memory):
        return None
    return reply


def _says_about(reply, head):
    if not isinstance(reply, str) or len(reply) < 40:
        return False
    first = re.split(r"(?<=[.!?])\s+", reply.strip())[0]
    return head in first.lower()


def _the_thing_itself(detail, memory):
    head = _head_word(detail)
    if not head or head in NOT_A_THING:
        return None
    try:
        from ..understanding import understand
        from ..knowledge import lookup as lookup_mod
    except Exception:
        return None
    for word in _subject_words(memory):
        if word == head:
            continue
        try:
            understood = understand(word + " " + head, {}) or {}
            reply = _the_entry_reply(lookup_mod.find(understood))
        except Exception:
            continue
        first = re.split(r"(?<=[.!?])\s+", reply.strip())[0]
        if len(reply) < 40 or head not in first.lower():
            continue
        if repeat._already_repeated(reply, memory):
            continue
        return reply
    return None


def _asks_about_a_new_thing(text, detail, said):
    opened = ABOUT_OPEN.match(_flat(text))
    if not opened:
        return False
    if not re.match(r"(?:a|an|some)\b", _flat(text)[opened.end():], re.I):
        return False
    from .topics import stem

    want = {stem(word) for word in _words(detail) if word not in VAGUE and word not in NAME_ONLY}
    if not want:
        return True
    have = {stem(word) for word in _words(said)}
    return not (want & have)


def _step_about(said, detail):
    want = {w for w in _words(detail) if w not in VAGUE and w not in NAME_ONLY}
    if not want:
        return None
    if _is_a_span(detail):
        return None
    sentences = [one.strip() for one in
                 re.split(r"(?<=[.!?])\s+", _flat(said)) if one.strip()]
    for sentence in sentences:
        groups = [one.strip() for one in re.split(r"\s+-\s+|\s+\u2014\s+", sentence)]
        for at, group in enumerate(groups):
            clauses = [one.strip() for one in group.split(",") if one.strip()]
            for pos, clause in enumerate(clauses):
                have = set(_words(clause))
                met = have & want
                if not (want <= have or len(met) * 2 > len(want)):
                    continue
                if not _one_of_a_list(clauses, groups, at):
                    continue
                if pos == len(clauses) - 1 and at + 1 < len(groups):
                    qualifier = groups[at + 1].strip(" .,;:-")
                    if 2 <= len(qualifier.split()) <= STEP_WORDS:
                        return qualifier + "."
                if have <= want | NAME_ONLY and pos + 1 < len(clauses):
                    clause = clauses[pos] + ", " + clauses[pos + 1]
                clause = JOIN_LEAD.sub("", clause.strip(" .,;:-"))
                if not clause or len(clause.split()) > STEP_WORDS:
                    return None
                return clause + "."
    return None


def _a_branch(sentence):
    return bool(condition.conditions(sentence))


def _without_branches(said):
    sentences = [one.strip() for one in
                 re.split(r"(?<=[.!?])\s+", _flat(said)) if one.strip()]
    return " ".join(one for one in sentences if not _a_branch(one))


def _the_move_itself(move):
    head = move.split(":", 1)[0].strip(" ,;.-")
    return head if len(head.split()) >= 2 else move

SPAN_WORDS = frozenset("""day days week weeks month months year years fortnight fortnights
                          hour hours minute minutes""".split())
SPAN_WORDS_ABOUT = frozenset("""for in after since over within about now already past last next
                               been it its thats that and but so oh well yeah yep ok okay right
                               like that""".split())
NUMBER_WORDS = frozenset("""one two three four five six seven eight nine ten eleven twelve
                            couple few several half""".split()) | frozenset(
                                str(digit) for digit in range(0, 100))
LEAD_AND = re.compile(r"^(?:and|then|but|or|also|so|plus)\s+", re.I)

HEADING = re.compile(r"^(?!(?:the|a|an|my|your|our|their|his|her|it|they)\b)"
                     r"[^:!?.;]{1,24}:\s+(?=\S)", re.I)
HEADING_WORDS = 2
CLAUSE_WORDS = frozenset("""is are was were be been am not no yes for and or but so of in on at
    with to from by as that which who what when how why""".split())


def _the_heading(said):
    text = str(said or "").strip()
    found = HEADING.match(text)
    if not found:
        return ""
    label = found.group(0).rstrip().rstrip(":")
    words = label.split()
    if not words or len(words) > HEADING_WORDS:
        return ""
    if any(word.lower().strip("*_\"',") in CLAUSE_WORDS for word in words):
        return ""
    return label


def _is_the_label_itself(text, label):
    return _flat(text).strip(" .,;:") == _flat(label).strip(" .,;:")


def _without_the_heading(said):
    label = _the_heading(said)
    if not label:
        return str(said or "")
    return str(said).strip()[len(label):].lstrip().lstrip(":").lstrip()


A_DURATION = re.compile(
    r"\b(?:\d+|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|a\s+few|couple\s+of|"
    r"several|a)\s+(?:day|week|month|year|fortnight)s?\b", re.I)


def _first_instruction(said):
    from ..compose.verdict import IMPERATIVES
    for sentence in re.split(r"(?<=[.!?])\s+", _flat(said)):
        clauses = [one.strip(" ,;:.-") for one in _clauses(sentence)]
        first = next((one for one in clauses if one), "")
        if not first or first.split()[0].lower() not in IMPERATIVES:
            continue
        if len(first.split()) > STEP_WORDS:
            bare = " ".join(re.sub(r"\s*\([^)]*\)", "", first).split())
            first = bare or first
        if 2 <= len(first.split()) <= STEP_WORDS:
            return first + "."
    return ""


def _opening_said(said):
    first = re.split(r"(?<=[.!?])\s+", _flat(said))[0].strip()
    if not first:
        return ""
    if len(first.split()) <= STEP_WORDS:
        return first if first.endswith((".", "!", "?")) else first + "."
    return _first_clause(first)


def _is_a_span(detail):
    want = {w for w in _words(detail) if w not in VAGUE and w not in NAME_ONLY}
    return bool(want) and not (want - SPAN_WORDS - NUMBER_WORDS - SPAN_WORDS_ABOUT)


def _a_span_step(said, detail):
    if not set(_words(detail)) & SPAN_WORDS:
        return ""
    for sentence in reversed(re.split(r"(?<=[.!?])\s+", _flat(said))):
        if not A_DURATION.search(sentence):
            continue
        for piece in _clauses(sentence):
            piece = LEAD_AND.sub("", piece.strip(" ,;:.-")).strip(" ,;:.-")
            if 2 <= len(piece.split()) <= STEP_WORDS:
                return piece + "."
    return ""


def _opening_of(said):
    parts = [p.strip() for p in repeat.SENTENCE.split(str(said).strip()) if p.strip()]
    if len(parts) < 2:
        return ""
    clauses = [one.strip(" ,;:.-") for one in _clauses(parts[0])]
    first = next((one for one in clauses if one), "")
    if first and len(first.split()) > STEP_WORDS:
        bare = " ".join(re.sub(r"\s*\([^)]*\)", "", first).split())
        if bare:
            first = bare
    if not first or len(first.split()) < 2 or len(first.split()) > STEP_WORDS:
        return ""
    from ..compose.verdict import IMPERATIVES
    if first.split()[0].lower() not in IMPERATIVES:
        return ""
    return first + "." if not first.endswith((".", "!", "?")) else first


def _names_nothing(detail):
    flat = _flat(detail)
    opening = PREPOSITION.match(flat)
    if not opening:
        return False
    return bool(NAMES_NOTHING.match(flat[opening.end():].strip()))


def _says_where(detail):
    flat = _flat(detail)
    return (bool(PREPOSITION.match(flat)) and not A_WHEN.match(flat)
            and not _names_nothing(flat) and not A_SUBJECT_OF_ITS_OWN.search(flat))


def _a_step(said, questions_are_steps=False):
    move = (repeat._a_move(said, questions_are_steps=questions_are_steps)
            or "").strip(" ,;:.-")
    if not move:
        return ""
    label = _the_heading(said)
    opening = _opening_of(said)
    if opening and not (label and _is_the_label_itself(opening, label)):
        move = opening
    if label:
        move = _without_the_heading(move) or move
        if _is_the_label_itself(move, label):
            move = _the_move_itself(_without_the_heading(said)) or move
    pieces = [p.strip() for p in _clauses(_the_move_itself(move)) if p.strip()]
    kept = pieces[0] if pieces else move
    for piece in pieces[1:]:
        if len(kept.split()) >= SHORT_STEP:
            break
        trial = kept + ", " + piece
        if len(trial.split()) > STEP_WORDS:
            break
        kept = trial
    kept = kept.strip(" ,;:-.")
    label = _the_heading(said)
    if kept and label and _is_the_label_itself(kept, label):
        body = _without_the_heading(said)
        if body and body != said:
            return _a_step(body, questions_are_steps=questions_are_steps)
    return kept + "." if kept else ""


def _capital(said):
    said = said.strip()
    if not said:
        return said
    return said[:1].upper() + said[1:]


REPORT_SENTENCE = re.compile(r"(?<=[.!?])\s+")

REPORT_OPENS_ON_THE_THING = re.compile(
    r"^\W*(?:(?:and|but|so|then|also|now|well|ok|okay|right)\b[\s,]*)*"
    r"(?:it'?s|its|it|they'?re|they|there'?s|there|that'?s|that|this)\b", re.I)

REPORT_ASKS = re.compile(
    r"\?|^\W*(?:(?:and|but|so|then|also|now|well|ok|okay|right)\b[\s,]*)*"
    r"(?:what|why|how|when|where|who|which|is|are|was|were|do|does|did|can|could|should|would|"
    r"will|shall|may|might)\b", re.I)

REPORT_BEHAVIOUR = re.compile(
    r"\b(?:if|when|whenever|unless|until|keeps?|kept|usually|often|always|every|tends?|starts?|"
    r"stops?)\b", re.I)

REPORT_NEGATES = re.compile(
    r"\b(?:not|never|nothing|none|without|hardly|isn'?t|isnt|aren'?t|arent|doesn'?t|doesnt|"
    r"didn'?t|didnt|don'?t|dont|won'?t|wont|can'?t|cant|couldn'?t|couldnt)\b", re.I)

A_REFERRAL = re.compile(
    r"\b(?:ring|call|phone|contact|see|visit|go\s+to|get\s+to|get\s+seen)\b[^.!?]*"
    r"\b(?:111|999|911|112|999|nhs|gp|doctor|nurse|a\s*&\s*e|casualty|hospital|pharmacy|"
    r"midwife|health\s+visitor|emergency)\b|"
    r"\b(?:should|needs?|ought)\s+(?:to\s+)?be\s+(?:looked\s+at|seen|checked|assessed)\b",
    re.I)
REPORT_WORDS = 14

REPORT_FILLER = frozenset("""
a an the and or but if then so to of in on at by for with from about as is are was were be been
being am do does did doing have has had having it its they them their this that these those there
here i me my we us our you your he she his her him one ones very really quite just now still
again too also only even not no yes yeah yep ok okay well right then than
""".split())

NOT_AN_ANSWER = ("i don't know enough", "i dont know enough", "beyond what i know", "no live ",
                 "i'm not sure what you mean", "can't help with that", "searching for it",
                 "a search should", "better sources")
OPENS_MID_THOUGHT = re.compile(
    r"^\W*(?:and|but|so|then|if|unless|when|whenever|while|because|though|although|which|"
    r"also|plus|otherwise|either|instead|or|yet|nor|whereas|even so|in that case|as well|"
    r"a search|searching for it|the search|(?:a|the) quick search)\b", re.I)


def stands_alone(sentence):
    said = str(sentence or "").strip()
    return bool(said) and not OPENS_MID_THOUGHT.match(said)


def _report_stem(word):
    for ending in ("ing", "ed", "es", "s"):
        if word.endswith(ending) and len(word) > len(ending) + 2:
            word = word[:-len(ending)]
            break
    if len(word) > 3 and word[-1] == word[-2] and word[-1] not in "aeiou":
        word = word[:-1]
    return word


def _report_content(text):
    return [_report_stem(w) for w in _words(text)
            if w not in REPORT_FILLER and len(w) > 2]


def a_report_about_the_thing(text, memory):
    said = _flat(text).lower()
    if not said or len(said.split()) > REPORT_WORDS:
        return ""
    if REPORT_ASKS.search(said) or not REPORT_OPENS_ON_THE_THING.match(said):
        return ""
    if REPORT_NEGATES.search(said):
        return ""
    turns = [t for t in (memory.get("turns") or []) if isinstance(t, dict)]
    if not turns:
        return ""
    answer = str(turns[-1].get("bot") or "")
    if len(answer) < 60:
        return ""
    lowered = answer.lower()
    if any(hedge in lowered for hedge in NOT_AN_ANSWER):
        return ""
    about = {w for w in _report_content(said) if len(w) > 3}
    if not about:
        return ""
    best = ""
    best_shared = 0
    for sentence in REPORT_SENTENCE.split(answer):
        sentence = sentence.strip()
        if len(sentence.split()) < 5:
            continue
        if sentence.endswith("?") or not REPORT_BEHAVIOUR.search(sentence):
            continue
        if not stands_alone(sentence):
            continue
        if A_REFERRAL.search(sentence):
            continue
        shared = len(about & set(_report_content(sentence)))
        if shared > best_shared:
            best, best_shared = sentence, shared
    if not best or best_shared < 1:
        return ""
    if _flat(best).lower() in {_flat(t.get("bot")).lower() for t in turns[-2:]}:
        return ""
    return _capital(best)
