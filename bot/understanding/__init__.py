import re

from . import attempts
from . import body
from . import breeds
from . import cars, kinds, lexicon, normalize, references, senses, topics
from .normalize import (background_positions, normalise, respell_urgent,
                        _the_part_that_hurts, _the_sugar_that_is_blood,
                        without_the_figure_of_speech)
from . import confusion

STOPWORDS = frozenset("""
a an the and or but if then than that this these those there here it its i me my myself
we our us you your yours he him his she her hers they them their theirs am is are was were be
been being do does did doing done have has had having will would shall should can could may
might must not no nor so too very just really quite only also as at by for from in into of
off on onto out over under up with within without about above after again against all any
both each few more most other some such own same what which who whom whose when where why how
please thanks thank hi hello hey ok okay yeah yes sure sorry oh um uh like get got to want
need help tell give show find know think guess
""".split())
MAX_KEYWORDS = 14
LOOKBACK = 4
CARRY_TOPIC = 2
CARRY_WORDS = 8
CARRY_PASS = frozenset("empty greeting farewell thanks ack smalltalk laugh about_bot".split())
THANKED_FOR = frozenset("for about of so again".split())
DID_IT = frozenset("""set put turned used tried made did got added took left changed lowered
    raised cleaned fixed swapped bought watched read told asked moved ran went came filled
    drained switched adjusted threw cleaned""".split())
PRAISED = frozenset("""perfect perfectly great brilliant sorted solved fixed works working
    lovely gorgeous spot marvellous marvelous amazing""".split())
ABOUT_THE_BOT = "about-the-bot"
SECOND_PERSON = frozenset("you your yours yourself u ur youre ya ye yous".split())
ASKING_WORDS = frozenset("what which who whom whose where when why".split())
COPULA_AUX = frozenset("do does did are is was were have has will would".split())
MODAL_WORDS = frozenset("can cant cannot could".split())
MODAL_STATE = frozenset("see hear listen think feel remember understand know learn sleep dream "
                        "sing draw read write talk speak taste smell count help cook make".split())
WHO_ENDS = frozenset("from here there".split())
AFTER_BOT_FILLER = frozenset("ever always still actually really even also just then now never "
                             "a an the".split())
BOT_STATE = MODAL_STATE | frozenset("""have has had got get make makes think thinks know knows
    remember remembers understand see hear listen feel feel help helps do does done
    bot bots robot robots llm ai chatgpt gpt claude human person people real alive awake
    busy smart clever intelligent right wrong sure ok okay there here about up online around
    ready name named personality hobbies hobby fun weekend weekends day days week evening
    morning night thing things lot bit much many answers answer mean means meant""".split())
BOT_NOUNS = frozenset("model models llm llms ai bot bots robot robots chatgpt gpt claude "
                      "name names personality hobby hobbies".split())
HYPOTHETICAL = frozenset("would wouldnt wouldve".split())
DAY_VERBS = frozenset("was is are did has have were s".split())
MEANING_WORDS = frozenset("mean means meant".split())
MEANING_TAIL = frozenset("by that this it there here then exactly you i".split())
DAY_WORDS = frozenset("day week weekend morning night evening afternoon".split())

SECOND_JOIN_HEAD = re.compile(
    r"^(?:(?:and|also|plus|but|so|then|yeah|yes|and\s+then|oh|and\s+yeah)\s+)+", re.I)
SECOND_JOIN_TAIL = re.compile(
    r"[\s,]*(?:\btoo\b|\bas\s+well\b|\balso\b|\ban\s+all\b|\band\s+all\b|"
    r"\band\s+that\b|\baswell\b)[\s.!?]*$", re.I)
CORRECTION_HEAD = re.compile(
    r"^(?:(?:no|nah|sorry|actually|wait|no\s+sorry|sorry\s+no)[\s,]+)?"
    r"(?:(?:i\s+mean|i\s+meant|i\s+did\s+mean|mean)"
    r"|(?:it'?s|it\s+is))\s+", re.I)
CORRECTION_MARKER = re.compile(
    r"^(?:(?:no|nah|sorry|actually|wait|no\s+sorry|sorry\s+no)[\s,]+)"
    r"|^(?:i\s+mean|i\s+meant|i\s+did\s+mean|mean)\b", re.I)
A_VALUE_IN_FRONT_OF_NOT = re.compile(r"\S.*\bnot\b", re.I)
OWN_VERB = frozenset("""is are was were am be been being do does did done have has had having
    will would can could should shall may might must went go goes gone going came come comes
    coming get gets got getting make makes made making want wants wanted like likes liked need
    needs needed think thinks thought know knows knew say says said tell tells told try tries
    tried use uses used eat eats ate eating drink drinks drank cook cooks cooked buy buys bought
    sell sells sold work works worked play plays played watch watches watched read reads run
    runs ran walk walks walked live lives lived feel feels felt hurt hurts ache aches""".split())
A_FAULT_TO_LEND = re.compile(
    r"\b(is\s+killing\s+me|kills\s+me|is\s+playing\s+up|is\s+on\s+the\s+blink|"
    r"(?:is|are)\s+not\s+working|(?:isnt|aren't|aint|isn't)\s+working|has\s+stopped|"
    r"have\s+stopped|keeps\s+stopping|wont\s+start|won't\s+start|doesnt\s+start|"
    r"doesn't\s+start|wont\s+turn\s+on|won't\s+turn\s+on|doesnt\s+turn\s+on|"
    r"doesn't\s+turn\s+on|wont\s+come\s+on|isnt\s+working|isn't\s+working|"
    r"is\s+blocked|is\s+blocked\s+up|is\s+leaking|is\s+flat|is\s+dead|"
    r"is\s+sore|is\s+stiff|is\s+swollen|is\s+broken|has\s+gone|is\s+bad|itches|itch|"
    r"hurts|hurting|hurt|aches|aching|ache)\b", re.I)


def _the_second_thing(text):
    line = str(text or "").strip()
    if not line:
        return ""
    correction = CORRECTION_HEAD.match(line)
    if correction and not _says_which_value_is_meant(line):
        correction = None
    head = correction or SECOND_JOIN_HEAD.match(line)
    rest = line[head.end():] if head else line
    tail = SECOND_JOIN_TAIL.search(rest)
    core = (rest[:tail.start()] if tail else rest).strip()
    if not core:
        return ""
    if correction:
        words = [word.lower() for word in re.findall(r"[A-Za-z']+", core)]
        if not words or len(words) > 5 or any(word in OWN_VERB for word in words):
            return ""
        return core
    if not head and not tail:
        return ""
    words = [word.lower() for word in re.findall(r"[A-Za-z']+", core)]
    if not words or len(words) > 5:
        return ""
    if any(word in OWN_VERB for word in words):
        return ""
    return core


def _says_which_value_is_meant(line):
    if CORRECTION_MARKER.match(line):
        return True
    rest = CORRECTION_HEAD.match(line)
    if not rest:
        return False
    return bool(A_VALUE_IN_FRONT_OF_NOT.search(line[rest.end():]))


def _the_fault_to_lend(previous):
    found = A_FAULT_TO_LEND.search(str(previous or ""))
    return found.group(1) if found else ""


STAND_IN_WORDS = frozenset("""cold hot warm cool freezing big small little large tiny huge
    old new broken faulty dodgy leaky cracked chipped rusty worn dead slow fast noisy loud
    quiet heavy light cheap expensive dear long short tall wide narrow thick thin hard soft wet
    dry clean dirty full empty spare extra front back top bottom middle inner outer upstairs
    downstairs left right wrong loose tight green red blue black white dark pale stained
    missing""".split())

STAND_IN_SELECTORS = frozenset("""other first second third last next same former latter""".split())

A_DESCRIBING_SUBJECT = STAND_IN_WORDS | lexicon.A_STATE | lexicon.FEELINGS | lexicon.A_DESCRIBING

A_STAND_IN = re.compile(r"\b(the|these|those|my|our|your|his|her|their|both)\s+"
                        r"(?:([a-z][a-z'-]*)\s+)?(ones|one)\b", re.I)


def _a_stand_in(text):
    if not isinstance(text, str):
        return None
    for match in A_STAND_IN.finditer(text):
        lead = match.group(2)
        if lead is not None and lead.lower() not in STAND_IN_WORDS:
            continue
        if lead is not None and lead.lower() in STAND_IN_SELECTORS:
            continue
        return {"word": match.group(3).lower(), "at": match.start(3), "end": match.end(3),
                "lead": (lead or "").lower()}
    return None


def _plural_of(phrase):
    head, _, last = phrase.rpartition(" ")
    word = last or phrase
    many = _a_plural_word(word)
    return (head + " " + many) if head else many


def _a_plural_word(word):
    lower = word.lower()
    if lower.endswith("ss"):
        return word + "es"
    if lower.endswith("s"):
        return word
    if lower.endswith(("ch", "sh", "x", "z")):
        return word + "es"
    if lower.endswith("y") and len(lower) > 1 and lower[-2] not in "aeiou":
        return word[:-1] + "ies"
    return word + "s"


STAND_IN_NOT_THINGS = frozenset("""winter summer spring autumn morning afternoon evening night
    week weekend month year hour minute day today tomorrow yesterday christmas birthday
    holiday weekend weeknight fortnight decade moment time while""".split())


def _singular_of(phrase):
    head, _, last = phrase.rpartition(" ")
    word = last or phrase
    one = _a_singular_word(word)
    return (head + " " + one) if head else one


def _a_singular_word(word):
    lower = word.lower()
    if lower.endswith("ies") and len(lower) > 3:
        return word[:-3] + "y"
    if lower.endswith(("ses", "xes", "zes", "ches", "shes")):
        return word[:-2]
    if lower.endswith("s") and not lower.endswith("ss"):
        return word[:-1]
    return word


def _the_noun_to_lend(memory, plural=False):
    for earlier in reversed(_user_lines(memory, 3)):
        line = normalise(earlier)
        entities = [entity for entity in topics.detect_entities(line)
                    if isinstance(entity, dict)]
        name, kind = references._target(line, entities, None)
        if kind != "thing" or not isinstance(name, str) or len(name) < 3:
            continue
        if name.lower() in STAND_IN_NOT_THINGS:
            continue
        if plural and not name.lower().split()[-1].endswith("s"):
            continue
        return name
    return ""


def _with_the_noun_lent(text, memory):
    stand = _a_stand_in(text)
    if not stand:
        return "", ""
    noun = _the_noun_to_lend(memory, plural=stand["word"] == "ones")
    if not noun:
        return "", ""
    if stand["word"] == "ones":
        noun = _plural_of(noun)
    else:
        noun = _singular_of(noun)
    return text[:stand["at"]] + noun + text[stand["end"]:], noun


def _a_describing_word_is_the_subject(read):
    for word, weight in read.get("topic_from") or []:
        if weight >= 2 and str(word).lower() in A_DESCRIBING_SUBJECT:
            return True
    things = [str(entity.get("text") or "").lower() for entity in read.get("entities") or []
              if entity.get("type") == "thing"]
    return bool(things) and all(thing in A_DESCRIBING_SUBJECT for thing in things)


def _stand_in_here(text):
    stand = _a_stand_in(text)
    if not stand:
        return None
    return {"word": stand["word"], "noun": None}


def _with_the_fault_lent(text, memory):
    core = _the_second_thing(text)
    if not core:
        return ""
    fault = ""
    for earlier in reversed(_user_lines(memory, 3)):
        found = _the_fault_to_lend(earlier)
        if found:
            fault = found
            break
        if not _the_second_thing(earlier):
            break
    if not fault:
        return ""
    if A_FAULT_TO_LEND.search(core):
        return ""
    return core + " " + fault


def _turns(memory):
    turns = memory.get("turns") if isinstance(memory, dict) else None
    return turns if isinstance(turns, list) else []


HOME_LOOKBACK = 8


def _user_lines(memory, limit):
    lines = []
    for turn in reversed(_turns(memory)):
        text = turn.get("user") if isinstance(turn, dict) else None
        if isinstance(text, str) and text.strip():
            lines.append(text)
            if len(lines) >= limit:
                break
    return list(reversed(lines))


def _pointable(entities):
    kept = []
    for entity in entities:
        kind, word = entity.get("type"), str(entity.get("text", "")).lower()
        if kind in ("thing", "place", "person", "title"):
            kept.append(entity)
        elif kind == "name" and "'" not in word and word not in topics.COMMON_WORDS:
            kept.append(entity)
    return kept


def _pointed_at(history):
    for text in reversed(history):
        read = normalise(text)
        entities = _pointable(topics.detect_entities(read))
        if entities:
            return read, entities
    return None, []


ANY_PRONOUN = frozenset(word for aliases in references.PRONOUNS.values() for word in aliases)


def _the_recorded_subject(memory):
    record = memory.get("topic") if isinstance(memory, dict) else None
    if not isinstance(record, dict):
        return None, []
    for key in ("of", "text"):
        line = record.get(key)
        if not isinstance(line, str) or not line.strip():
            continue
        read = normalise(line)
        entities = _pointable(topics.detect_entities(read))
        if entities:
            return read, entities
    return None, []


def _recent_topic(lines):
    best = None
    for index, text in enumerate(lines):
        read = normalise(text)
        topic, score = topics.detect_topic(read, None, topics.detect_entities(read))
        if topic and score >= CARRY_TOPIC:
            key = (score, -index)
            if best is None or key > best[0]:
                best = (key, topic)
    return best[1] if best else None


SHIFTS = ("never mind", "nevermind", "forget that", "forget it", "different question",
          "new question", "new topic", "changing the subject", "change of subject",
          "on another note", "moving on", "back to", "anyway", "anyways", "instead",
          "another thing", "unrelated", "off topic")
SHIFT_ACTUALLY = re.compile(r"(?:^|\|)\s*actually\b|\b(?:no|oh|well|sorry|and|but),? actually\b")


def _changes_subject(line):
    padded = " " + line["norm_text"] + " "
    if any(cue in padded for cue in SHIFTS):
        return True
    return bool(SHIFT_ACTUALLY.search(line["norm_text"]))


def _names_a_bot_noun(words):
    return any(word in BOT_NOUNS for word in words)



CHAT_WORDS = frozenset("""talk talking talks chat chatting chats message messages conversation
ramble rambling wittering waffling going typing write writing""".split())

TALK_ASK = re.compile(
    r"\b(?:bor(?:ing|ed)|annoy(?:ing|ed)|wast(?:e|ing)\s+(?:your|my)\s+time|keeping\s+you|"
    r"still\s+(?:with|there|following|listening)|too\s+(?:long|much)|going\s+on|ramble|"
    r"rambling|wittering|waffling)\b", re.I)

PERSON_STOP = re.compile(
    r"^(?:so|and|but|ok|okay|well|then|hmm|erm|um|oh|ah|right|alright|just|also)?[\s,]*"
    r"(?:should|shall|can|could)\s+i\s+(?:stop|quit|shut\s+up|leave\s+it)"
    r"(?:\s+(?:now|then|talking|chatting|going\s+on))?[\s.!?]*$", re.I)


def _a_stop_in_a_chat_about_something(norm, memory):
    said = norm if isinstance(norm, str) else " ".join(str(word) for word in norm or ())
    if not PERSON_STOP.fullmatch(said.strip()):
        return False
    if not isinstance(memory, dict) or not memory:
        return False
    turns = memory.get("turns")
    last = turns[-1] if isinstance(turns, list) and turns else None
    if isinstance(last, dict) and str(last.get("module") or "") == "keeping":
        return False
    if isinstance(last, dict):
        before = str(last.get("user") or "")
        if TALK_ASK.search(before) or PERSON_STOP.match(before.strip()):
            return False
    topic = memory.get("topic")
    said = set(topic.get("words") or []) if isinstance(topic, dict) else set()
    return bool(said) and not (said & CHAT_WORDS)

def _about_the_bot(line, read, entities=()):
    if read.get("intent") == "about_bot":
        return True
    if read.get("kind") != "question" or entities:
        return False
    words = [word for word in (line.get("words") or []) if word != "|"]
    if len(words) < 2:
        return False
    if (words[0] == "how" and len(words) > 3 and words[2] in SECOND_PERSON
            and words[1] in DAY_VERBS):
        return any(word in DAY_WORDS for word in words[3:])
    if words[1] in SECOND_PERSON:
        if words[0] in COPULA_AUX:
            rest = [word for word in words[2:] if word not in AFTER_BOT_FILLER]
            return not rest or rest[0] in BOT_STATE or _names_a_bot_noun(words)
        return (words[0] in MODAL_WORDS and 2 < len(words) <= 4
                and words[2] in BOT_STATE)
    if not (words[0] in ASKING_WORDS
            and any(word in SECOND_PERSON for word in words[:4])):
        return False
    if words[0] == "who":
        return words[-1] in SECOND_PERSON or words[-1] in WHO_ENDS
    bot_at = next(index for index, word in enumerate(words) if word in SECOND_PERSON)
    if any(word in HYPOTHETICAL for word in words[1:bot_at]):
        return False
    rest = [word for word in words[bot_at + 1:] if word not in AFTER_BOT_FILLER]
    if (rest and rest[0] in MEANING_WORDS
            and all(word in MEANING_TAIL for word in rest[1:])):
        return True
    if len(words) > 5:
        return False
    return not rest or rest[0] in BOT_STATE or _names_a_bot_noun(words)


PRESENCE_SUBJECT = frozenset("you u ya your yourself me".split())
PRESENCE_WORD = frozenset("""up there around about here online awake alive ready with
    free""".split())
PRESENCE_FILLER = frozenset("""still ok okay good right fine then now anyone anybody someone
    hello hey hi hiya heya howdy yo morning evenin again mate pal buddy all are is r else
    later soon l8r""".split())
PRESENCE_ASKER = frozenset("anyone anybody someone".split())
PRESENCE_NOT = frozenset("""greeting thanks farewell empty""".split())
PRESENCE_MAX = 5
PRESENCE_GREETING = frozenset(word for word in kinds.GREETINGS if " " not in word)
GREETING_PHRASE = frozenset(word for word in kinds.GREETINGS if " " in word)
OWN_QUESTION_TOPIC = "nature-and-weather"


NOTHING_NAMED_ASK_WORDS = frozenset("""what which who how why when where do does did would should
    will can could is are any anything something else more that this it for me i we to about of
    in on with""".split())
NOTHING_NAMED_VIEW_WORDS = frozenset("""think say suggest recommend advise reckon opinion advice
    thoughts thought view take recommendation suggestion ideas idea""".split())
NOTHING_NAMED_FILLER = frozenset("""so and ok okay right well but then now here first next
    actually please pls""".split())
BOT_ASK_WORDS = frozenset("you u ya your yours yourself".split())

BROKEN_OF_A_THING = ("knackered", "buggered")
WORN_OUT_OF_A_PERSON = {"knackered": "knackered", "buggered": "exhausted"}
SPEAKER_SUBJECTS = frozenset(("i", "im", "ive", "me"))
BE_VERB = frozenset("""am is are was were be been being""".split())
A_CONDITION_AFTER = frozenset(("if", "unless", "when", "till", "until"))
NOT_A_SUBJECT = BE_VERB | frozenset("""a an the and but so really very totally completely
    absolutely utterly quite pretty dead proper just now too also always still only even""".split())
OTHER_PRONOUNS = frozenset("""we us our ours they them their theirs he him his she her hers
    it its you your yours""".split())
EDGE_PUNCTUATION = ".,!?;:'\"()"
A_CLAUSE_VERB = frozenset("""have has had having do does did done get gets got getting
    go goes went gone make makes made making take takes took taken come comes came bet bet
    felt feel feels leave leaves left keep keeps kept put puts""".split())


def _the_speaker_is_the_subject(between):
    rest = [word for word in between if word.isalnum() and word not in NOT_A_SUBJECT]
    return len(rest) == 1 and rest[0] in SPEAKER_SUBJECTS


def _a_word_that_depends_on_the_owner(plain, entities, state_owner=None):
    if not plain:
        return plain
    things = set()
    people = set()
    for entity in entities or ():
        words_of = [word.lower() for word in entity.get("text", "").split()]
        if entity.get("type") == "thing":
            things.update(words_of)
        elif entity.get("type") == "person":
            people.update(words_of)
    words = plain.split()
    out = []
    for at, word in enumerate(words):
        bare = word.strip(EDGE_PUNCTUATION).lower()
        if bare not in BROKEN_OF_A_THING:
            out.append(word)
            continue
        between = []
        whose = None
        for back in range(at - 1, -1, -1):
            earlier = words[back]
            if any(mark in earlier for mark in ",;:?!."):
                break
            low = earlier.strip(EDGE_PUNCTUATION).lower()
            if low in things:
                whose = "thing"
                break
            if low in people:
                whose = "person"
                break
            between.append(low)
        if any(word_ in OTHER_PRONOUNS for word_ in between):
            whose = None
        elif whose is None and _the_speaker_is_the_subject(between):
            whose = "person"
        after = [word_.strip(EDGE_PUNCTUATION).lower() for word_ in words[at + 1:at + 3]]
        if whose is None or any(word_ in A_CONDITION_AFTER for word_ in after):
            out.append(word)
        elif any(word_ in A_CLAUSE_VERB for word_ in between):
            out.append(word)
        elif whose == "thing":
            out.append(word.replace(word.strip(EDGE_PUNCTUATION), "broken"))
        else:
            out.append(word.replace(word.strip(EDGE_PUNCTUATION),
                                    WORN_OUT_OF_A_PERSON[bare]))
    return " ".join(out)


def _opens_the_conversation(previous):
    if previous is None:
        return True
    return len([word for word in previous.get("norm") or [] if word and word != "|"]) <= 3


def asks_with_nothing_named(norm):
    words = [word for word in norm if word and word != "|"]
    if not any(word in BOT_ASK_WORDS for word in words):
        return False
    if not any(word in NOTHING_NAMED_VIEW_WORDS for word in words):
        return False
    rest = set(words) - NOTHING_NAMED_ASK_WORDS - BOT_ASK_WORDS - NOTHING_NAMED_VIEW_WORDS \
        - NOTHING_NAMED_FILLER
    if rest:
        return False
    return not (words[0] in ("can", "could") and len(words) > 1
                and words[1] in BOT_ASK_WORDS)


def _presence(line):
    words = [word for word in line["norm"] if word and word != "|"]
    if words and words[0] in PRESENCE_GREETING:
        words = words[1:]
    if not words or len(words) > PRESENCE_MAX:
        return False
    if not any(word in PRESENCE_WORD for word in words):
        return False
    asked = any(word in PRESENCE_SUBJECT or word in PRESENCE_ASKER for word in words)
    dropped_subject = len(words) <= 2
    if not asked and not dropped_subject:
        return False
    return all(word in PRESENCE_WORD or word in PRESENCE_SUBJECT or word in PRESENCE_ASKER
               or word in PRESENCE_FILLER for word in words)


MOMENT_WORDS = frozenset("""sec secs second seconds min mins minute minutes mo moment
    time""".split())
MOMENT_VERBS = frozenset("got have get spare".split())
MOMENT_FILLER = frozenset("""a an the to for chat talk and i you u me ask something question
    quick please ta thanks can could would may might will just wanted like us we mind if
    wondering favour favor do does did hey hi hello so well um er there""".split())
ASK_PERMISSION = ("ask you something", "ask you a question", "ask you one", "ask a question",
                  "ask something", "ask you quick question", "ask a quick question",
                  "bend your ear", "pick your brains", "ask your advice",
                  "talk to you", "talk with you", "chat to you", "chat with you",
                  "can we talk", "could we talk", "can we chat", "have a word", "quick word",
                  "quick question", "quick one", "ask a favour", "ask you a favour")
PERMISSION_FILLER = frozenset("""you u ya your yourself need needed want wanted mind about
    something then now bit wee little one just really actually
    ok okay hey hi hello so well oh ah and but or yeah yes please ta thanks love mate""".split())
ASK_FREE_WORDS = frozenset("free around available busy".split())
ASK_FREE_FILLER = frozenset("""are is you u ya to for a chat talk then now still or and quick
    moment min minute sec second right mate please""".split())


NOT_MANNER = frozenset("""silly friendly lovely lonely ugly early daily weekly monthly yearly
    likely only family reply supply apply july italy belly jelly rally fly""".split())
TALK_VERBS = frozenset("talk talking speak speaking chat chatting discuss discussing".split())
MORE_WORDS = frozenset("more much really very".split())
MANNER_TALK = frozenset("""properly privately seriously openly honestly frankly quietly calmly
    briefly quickly plainly directly bluntly gently carefully sensibly reasonably""".split())
GOOD_TIME_WORDS = frozenset("""a an the it this that is s good bad ok okay fine right wrong
    better best time moment now for to then or""".split())
TALK_FILLER = frozenset("""can could would will may might shall should we i you u ya us to for a
    about with now just please then""".split())


def _a_manner(norm, at):
    word = norm[at]
    if len(word) <= 4 or not word.endswith("ly") or word in NOT_MANNER:
        return False
    if word in MANNER_TALK:
        return True
    back = at - 1
    if back >= 0 and norm[back] in MORE_WORDS:
        back -= 1
    return back >= 0 and norm[back] in TALK_VERBS


def _not_manner(norm):
    left = set()
    for at, word in enumerate(norm):
        if _a_manner(norm, at):
            continue
        if word in MORE_WORDS and at + 1 < len(norm) and _a_manner(norm, at + 1):
            continue
        left.add(word)
    return left


LEANS_ON_THEM = re.compile(
    r"\b(?:everyone|everybody|they all|all of them)\s+"
    r"(?:leans?|rel(?:y|ies)|depends?|counts?|comes?|come)\s+(?:on|to)\s+(?:me|us)\b")
DOES_IT_ALL = re.compile(
    r"\bi\s+(?:do|handle|manage|carry|hold|sort|run|organise|organize|deal\s+with)\s+"
    r"(?:it\s+all|everything|the\s+lot|all\s+of\s+it|the\s+whole\s+lot)\b"
    r"|\bi\s+(?:carry|hold)\s+(?:the\s+)?(?:whole\s+)?(?:house|family)\b"
    r"|\bi\s+do\s+everything\s+for\s+(?:everyone|everybody|them|the\s+kids)\b")
NO_TIME_OFF = re.compile(
    r"\bi\s+(?:never|hardly\s+ever|rarely)\s+get\s+(?:a\s+break|five\s+minutes)\b"
    r"|\bi\s+(?:never|hardly\s+ever|rarely)\s+get\s+a\s+(?:minute|moment|second)\s+"
    r"(?:to\s+myself|for\s+myself|off)\b"
    r"|\bi\s+(?:never|dont|do\s+not)\s+get\s+any\s+time\s+(?:to\s+myself|off|for\s+myself)\b")
ALL_ON_THEM = re.compile(
    r"\b(?:it'?s|its|it\s+is|everything\s+is|everything'?s)\s+(?:all\s+)?on\s+me\b"
    r"|\bit'?s\s+all\s+(?:down\s+)?to\s+me\b"
    r"|\ball\s+on\s+my\s+(?:own\s+)?(?:plate|shoulders|back)\b")
THE_ONE_WHO = re.compile(
    r"\bi'?m\s+(?:always\s+|usually\s+|often\s+)?(?:the\s+|the\s+only\s+)?one\s+(?:who|that)\b"
    r"|\bi\s+am\s+(?:always\s+)?(?:the\s+|the\s+only\s+)?one\s+(?:who|that)\b")
NO_ONE_HELPS = re.compile(
    r"\b(?:no ?one|nobody)\s+(?:else\s+)?"
    r"(?:helps?|helped|helps\s+out|does\s+anything|lifts\s+a\s+finger)\b")
EVERYTHING_AT_ONCE = re.compile(
    r"\b(?:everything|everyone|everybody|all\s+of\s+it|it\s+all|nothing|nobody|no ?one"
    r"|the\s+lot|the\s+whole)\b")
DOES_ALL_THEY_CAN = re.compile(r"\beverything\s+(?:i|we)\s+(?:can|could)\b")
THIRD_PERSON = re.compile(
    r"\b(?:she|he|they|her|his|their|them|him|mum|mom|mother|dad|father|parents"
    r"|sister|brother|son|daughter|partner|husband|wife|friend|colleague|boss)\b")
FIRST_PERSON_ANYWHERE = re.compile(r"\b(?:i|me|my|mine|myself|we|us|our)\b")
ASKS_WHY_IT_IS = re.compile(r"^\s*(?:why|how\s+come|what\s+makes|whats\s+making|what'?s\s+making)\b")
WORK_SCOPE = re.compile(r"\b(?:at|from|in|to)\s+work\b|\bwork(?:ing)?\s+(?:all|every)\s+(?:day|night)\b")
HOME_SCOPE = re.compile(r"\b(?:at|in)\s+(?:home|the\s+house|our\s+house|this\s+house)\b|\bhome\b")
DOES_IT_RIGHT = re.compile(r"\b(?:it|everything|things)\s+(?:all\s+)?(?:right|perfectly|correctly)\b")
RUNS_THE_HOUSE = re.compile(
    r"\bi\s+(?:run|runs|running|manage|managing)\s+"
    r"(?:the|this|our)\s+(?:house|home|family)\b"
    r"|\bi'?m\s+(?:the\s+)?only\s+one\s+(?:who\s+)?(?:holds?|holding|keeps?|keeping|runs|running)"
    r"\b[^.]*\btogether\b"
    r"|\b(?:i'?m|i\s+am)\s+(?:always\s+|usually\s+)?(?:the\s+)?one\s+who\s+"
    r"(?:runs?|keeps?|holds?)\s+(?:the|this|our)\s+(?:house|home|family)\b")
RUNS_MYSELF_RAGGED = re.compile(
    r"\bi\s+(?:run|runs|running|work|working|push|pushing|drive|driving)\s+myself\s+"
    r"(?:ragged|into\s+the\s+ground|to\s+the\s+bone)\b")
HELPS_ME_NOT = re.compile(
    r"\b(?:no ?one|nobody)\s+(?:else\s+)?(?:helps?|helped)\s+me\s+(?:with|at|around)\b")


def a_load_carried(text):
    said = " ".join(str(text or "").lower().replace("\u2019", "'").split())
    if not said:
        return False
    said = said.strip("'\" ")
    for piece in re.split(r"[.!?,;:]+|\bbut\b|\bthough\b", said):
        piece = piece.strip()
        if not piece or ASKS_WHY_IT_IS.match(piece) or DOES_ALL_THEY_CAN.search(piece):
            continue
        if WORK_SCOPE.search(piece) and not HOME_SCOPE.search(piece):
            continue
        if DOES_IT_RIGHT.search(piece):
            continue
        if RUNS_MYSELF_RAGGED.search(piece) or RUNS_THE_HOUSE.search(piece):
            return True
        if HELPS_ME_NOT.search(piece):
            return True
        if LEANS_ON_THEM.search(piece) or DOES_IT_ALL.search(piece):
            return True
        if NO_TIME_OFF.search(piece) or ALL_ON_THEM.search(piece):
            return True
        unhelped = NO_ONE_HELPS.search(piece)
        if unhelped:
            head = piece[:unhelped.start()]
            if FIRST_PERSON_ANYWHERE.search(head) and not THIRD_PERSON.search(head):
                return True
        if THE_ONE_WHO.search(piece) and EVERYTHING_AT_ONCE.search(piece):
            return True
    return False


def _asks_for_a_moment(line):
    norm = [word for word in line["norm"] if word and word != "|"]
    if not norm or len(norm) > 9:
        return False
    bare = " ".join(norm)
    for phrase in ASK_PERMISSION:
        if phrase in bare:
            rest = bare.replace(phrase, " ").split()
            last = phrase.split()[-1]
            if last in TALK_VERBS:
                rest = [last] + rest
            if not (_not_manner(rest) - MOMENT_FILLER - MOMENT_WORDS - MOMENT_VERBS
                    - PERMISSION_FILLER):
                return True
            continue
    while norm and norm[0] in PRESENCE_GREETING:
        norm.pop(0)
    if len(norm) > 2 and " ".join(norm[:2]) in GREETING_PHRASE:
        norm = norm[2:]
    words = set(norm)
    if not words:
        return False
    if words & ASK_FREE_WORDS and (words & PRESENCE_SUBJECT or len(norm) <= 2):
        return not _not_manner(norm) - ASK_FREE_FILLER - ASK_FREE_WORDS
    if "the time" in " ".join(norm) and not ((words - {"time"}) & MOMENT_WORDS
                                             or words & TALK_VERBS):
        return False
    if words & MOMENT_WORDS and words & MOMENT_VERBS:
        return not (_not_manner(norm) - MOMENT_FILLER - MOMENT_WORDS - MOMENT_VERBS
                    - {"you", "u", "ya"})
    if words & {"time", "moment"} and (words - TALK_VERBS) <= GOOD_TIME_WORDS:
        return True
    if len(norm) <= 6 and words & TALK_VERBS:
        return not _not_manner(norm) - TALK_FILLER - TALK_VERBS
    return False


def _keywords(norm):
    return [word for word in norm
            if word not in STOPWORDS and (len(word) > 1 or word.isdigit())][:MAX_KEYWORDS]


PROPERTY_SUBJECTS = frozenset("""
temperature temp temps degrees centigrade fahrenheit heat time times price cost size
setting weight length height age speed amount number
""".split())

SUBJECT_TYPES = ("title", "name", "person", "place", "thing")


PROPERTY_ASK = re.compile(r"^\s*(?:and|so|ok|okay|also|but)?\s*[,:]?\s*(?:what|which|how)\b")


def _asks_a_property_and_nothing_else(text):
    low = str(text or "").strip().lower()
    if not PROPERTY_ASK.match(low):
        return False
    found = _keywords(low.split())
    return bool(found) and all(word in PROPERTY_SUBJECTS for word in found)

def _the_chat_subject(chat):
    text = str((chat or {}).get("text") or "").strip()
    if not text:
        return None, None, []
    named = [entity for entity in topics.detect_entities(normalise(text))
             if entity["type"] in SUBJECT_TYPES]
    if not named:
        return None, None, []
    plain = [entity for entity in named if entity["type"] not in ("name", "title")]
    chosen = (plain or named)[-1]
    words = [str(word).lower() for word in (chat or {}).get("words") or []]
    return chosen["text"].lower(), chosen["type"], words


def _the_meaning_is_applied_to_what_was_said(line, leans_on, memory):
    applied = kinds.MEANT_APPLIED_TO.search(str(line.get("text") or line.get("clean") or ""))
    if not applied:
        return True
    thing = applied.group(1).lower()
    said = []
    if isinstance(leans_on, dict):
        said.append(leans_on.get("text"))
        said.append(leans_on.get("subject"))
        said.extend(word for word in (leans_on.get("words") or []) if isinstance(word, str))
    turns = memory.get("turns") if isinstance(memory, dict) else None
    if isinstance(turns, list) and turns and isinstance(turns[-1], dict):
        said.append(turns[-1].get("bot"))
    words = set()
    for blob in said:
        words |= set(re.findall(r"[a-z]+", str(blob or "").lower()))
    return any(word.startswith(thing) or thing.startswith(word)
               for word in words if len(word) > 2)


def _leans_on(line, read, ref, carried_text, carried, previous, own_topic, previous_topic,
              previous_entities, carried_is_older=False, chat=None):
    if not carried_text or read["intent"] in CARRY_PASS:
        return None
    if not ref["followup"] and own_topic:
        return None
    if _changes_subject(line):
        return None
    words = breeds.the_animal_a_breed_is(_keywords(carried["norm"]))
    if carried is not previous and not carried_is_older:
        for word in _keywords(previous["norm"]):
            if word not in words:
                words.append(word)
    chat_subject, chat_type, chat_words = _the_chat_subject(chat)
    for word in chat_words:
        if word not in words:
            words.append(word)
    words = words[:CARRY_WORDS]
    if not words:
        return None
    asked_only = _asks_a_property_and_nothing_else(carried_text)
    words = [word for word in words if word not in PROPERTY_SUBJECTS] if asked_only else words
    named = [entity for entity in previous_entities if entity["type"] in SUBJECT_TYPES
             and not (asked_only and entity["text"].lower() in PROPERTY_SUBJECTS)]
    plain = [entity for entity in named if entity["type"] not in ("name", "title")]
    chosen = next((entity for entity in reversed(plain or named)), None)
    subject = chosen["text"].lower() if chosen else None
    subject_type = chosen["type"] if chosen else None
    if chat_subject and subject != chat_subject and subject not in chat_words:
        subject, subject_type = chat_subject, chat_type
    return {"text": carried_text, "words": words, "subject": subject,
            "subject_type": subject_type, "topic": previous_topic}


PERSON_HEADS = frozenset("""i im ive ill id youre you he hes she shes they theyre we were weve
    weve us""".split())
POSSESSIVE = frozenset("my his her their our your".split())
AT_IT_STILL = frozenset("still again now".split())


def _about_a_person_or_a_trouble(after):
    if set(after) & (kinds.NEEDS_ANSWER | AT_IT_STILL):
        return True
    if kinds.STILL_WRONG.search(" ".join(after)):
        return True
    if after[0] in PERSON_HEADS:
        return True
    if (after[0] in POSSESSIVE and len(after) > 1
            and after[1] in kinds.OTHER_PEOPLE | kinds.PERSON_NOUNS | kinds.MOOD_NOUNS):
        return True
    return False


def _about_something_of_its_own(after):
    if len(after) < 2 or after[0] in kinds.ADDRESS_WORDS:
        return False
    if after[0] == "i" and after[1] in DID_IT:
        if not set(after) & kinds.NEEDS_ANSWER and not kinds.STILL_WRONG.search(" ".join(after)):
            return False
    words = set(after)
    if words & PRAISED:
        return False
    if kinds._a_step_done(after) and not kinds._the_step_went_wrong(after):
        return False
    if words & kinds.PRAISING_VERB or kinds.PRAISE_SAID.search(" ".join(after)):
        return False
    if kinds._a_fall_that_is_not_one(after):
        return False
    if "temperature" in after or kinds.SIGNING_OFF.search(" ".join(after)):
        return False
    if not _about_a_person_or_a_trouble(after):
        return False
    rest = normalise(" ".join(after))
    entities = topics.detect_entities(rest)
    topic, score = topics.detect_topic(rest, None, entities, False)
    return topic is not None and score >= CARRY_TOPIC + 1


FOLLOW_OPENER = (("and", "what", "about"), ("what", "about"), ("how", "about"), ("and",),
                 ("or",), ("also",), ("what",), ("how",))
NOT_A_THING = frozenset("""i im ive me we us you your youre u he she they theyre it its is are
    was were am be been being do does did can could should would will shall may might have has
    had if when while because since until though although than that this then there here and or
    but not no""".split())
CORRECTION_OPENER = frozenset("""no nah sorry actually oops wait nope""".split())
DETERMINER_TAIL = frozenset("the a an my your our their his her each every".split())


def _the_new_thing(words):
    phrase = list(words or ())
    dropped = True
    while dropped and phrase:
        dropped = False
        for opener in FOLLOW_OPENER:
            if tuple(phrase[:len(opener)]) == opener:
                phrase = phrase[len(opener):]
                dropped = True
                break
    while phrase and phrase[0] in CORRECTION_OPENER:
        phrase = phrase[1:]
    if not phrase or len(phrase) > 5:
        return None
    for word in phrase:
        if word in NOT_A_THING:
            return None
    if not any(len(word) > 2 or word in lexicon.COMMON_NAMES for word in phrase):
        return None
    return phrase


SAME_KIND_WORDS = (("person", topics.RELATIONS), ("name", lexicon.COMMON_NAMES),
                   ("part", lexicon.BODY_PARTS), ("time", normalize.COUNT_UNITS))


def _the_same_kind(a, b):
    for kind, words in SAME_KIND_WORDS:
        if a in words and b in words:
            return kind
    if any(ch.isdigit() for ch in a) and any(ch.isdigit() for ch in b):
        return "number"
    return None


def _where_the_swap_goes(before, phrase):
    places = list(before or ())
    if not places or not phrase:
        return None
    for word in phrase:
        for at, earlier in enumerate(places):
            kind = _the_same_kind(word, earlier)
            if not kind:
                continue
            end = at + 1
            if any(ch.isdigit() for ch in earlier):
                while end < len(places) and (places[end] in normalize.COUNT_UNITS
                                             or places[end] in ("a", "an", "each", "per", "every")):
                    end += 1
            return at, end, kind
    return None


def _the_swap_is_said(before, phrase, place):
    places = list(before or ())
    said = list(phrase or ())
    if not places or not said or place is None:
        return None
    start, end, _kind = place
    if start > 0 and places[start - 1] in DETERMINER_TAIL and said[0] in DETERMINER_TAIL:
        said = said[1:]
    if not said:
        return None
    return " ".join(places[:start] + said + places[end:])


def _the_line_before(read, memory):
    turns = (memory or {}).get("turns") if isinstance(memory, dict) else None
    for turn in reversed(turns or ()):
        if isinstance(turn, dict) and isinstance(turn.get("user"), str) and turn["user"].strip():
            return turn["user"]
    leans = (read or {}).get("leans_on") if isinstance(read, dict) else None
    if isinstance(leans, dict) and isinstance(leans.get("text"), str):
        return leans["text"]
    return None


def _asked_again(read, memory=None):
    if not isinstance(read, dict):
        return None
    if not isinstance(read.get("leans_on"), dict):
        return None
    before = _the_line_before(read, memory)
    if not isinstance(before, str) or not before.strip():
        return None
    phrase = _the_new_thing(read.get("norm"))
    if not phrase:
        return None
    earlier = normalise(before)
    at = _where_the_swap_goes(earlier["norm"], phrase)
    if at is None:
        return None
    said = _the_swap_is_said(earlier["norm"], phrase, at)
    if not said or said == " ".join(earlier["norm"]):
        return None
    return said, at[2]


SUBJECT_TYPES = ("title", "name", "person", "place", "thing")


def _the_spans_of(clauses):
    spans = []
    at = 0
    for clause in clauses or ():
        spans.append((at, at + len(clause)))
        at += len(clause)
    return spans


def _the_thing_the_ask_names(clauses, focus, entities):
    named = [entity for entity in entities or () if entity.get("type") in SUBJECT_TYPES]
    if not named:
        return None, None, None
    ask_span = None
    for clause, span in zip(clauses or (), _the_spans_of(clauses)):
        if list(clause) == list(focus or ()):
            ask_span = span
    if ask_span is None:
        return named[0]["text"].lower(), None, "ask"
    start, end = ask_span
    inside = next((entity for entity in named if start <= entity.get("at", -1) < end), None)
    outside = next((entity for entity in named if not start <= entity.get("at", -1) < end),
                   None)
    return (inside["text"].lower() if inside else None,
            outside["text"].lower() if outside else None,
            "ask" if inside else "setting")


def understand(text, memory=None):
    read = _read_line(text, memory)
    stated = _an_introduction_that_says_how_they_are(text)
    if stated:
        alt = _read_line(stated, memory)
        alt["text"] = read["text"]
        return alt
    errand, at_the_head = _the_ask_inside_an_errand(text)
    if errand:
        alt = _read_line(errand, memory)
        if _reaches(alt) and (not _reaches(read)
                              or (at_the_head and _A_THING_THAT_CHANGES.search(alt.get("clean")
                                                                              or errand or ""))):
            alt["text"] = read.get("text") if isinstance(read.get("text"), str) else ""
            alt["fixes"] = read.get("fixes")
            alt["errand"] = errand
            return alt
        if at_the_head and not _reaches(read):
            read["errand"] = errand
            return read
    lent = _with_the_fault_lent(text, memory)
    if lent:
        alt = _read_line(lent, memory)
        if _reaches(alt):
            alt["text"] = read["text"]
            return alt
    stand = _a_stand_in(text)
    if stand and _a_describing_word_is_the_subject(read):
        lent_noun, noun = _with_the_noun_lent(text, memory)
        alt = _read_line(lent_noun, memory) if lent_noun else None
        if alt is not None and _reaches(alt):
            alt["text"] = read["text"] if isinstance(read.get("text"), str) else ""
            alt["stand_in"] = {"word": stand["word"], "noun": noun}
            return alt
    asked = _asked_again(read, memory)
    if asked:
        said, kind = asked
        asked = said if (read.get("kind") == "question" or kind != "number") else None
    if asked:
        alt = _read_line(asked, memory)
        if alt.get("clean"):
            alt["text"] = read["text"] if isinstance(read.get("text"), str) else ""
            alt["fixes"] = read.get("fixes")
            alt["ref"] = read.get("ref")
            alt["leans_on"] = read.get("leans_on")
            alt["asked_again"] = asked
            return alt
    if _reaches(read):
        return read
    swapped, pairs = _confused_text(text)
    if not swapped:
        return read
    alt = _read_line(swapped, memory)
    if not _reaches(alt):
        return read
    alt["text"] = read["text"]
    alt["fixes"] = list(alt.get("fixes") or []) + pairs
    return alt


def line_as_read(understood):
    if not isinstance(understood, dict):
        return ""
    plain = understood.get("plain")
    if isinstance(plain, str) and plain.strip():
        return plain
    return str(understood.get("clean") or understood.get("text") or "")


REACHING_KEYS = ("topic", "emotion", "body", "numbers", "summons", "presence")


_SEARCH_FRAME = re.compile(
    r"^(?P<polite>\s*(?:(?:can|could|would|will)\s+you\s+|please\s+|pls\s+|just\s+|ok(?:ay)?\s+"
    r"|so\s+|and\s+|go\s+|quick\s+)*)"
    r"(?:search\s+for|search\s+up|look\s+up)\s+"
    r"|^(?P<polite2>\s*(?:(?:can|could|would|will)\s+you\s+|please\s+|pls\s+|just\s+)*)google\s+",
    re.IGNORECASE)

_A_CLAUSE_WITH_NO_SUBJECT = re.compile(r"^(?:whether|if|that)\b", re.IGNORECASE)

_A_THING_THAT_CHANGES = re.compile(
    r"\b(?:what\s+time|when|hours?|opening|opens?|clos(?:es|ing)|shut|open\s+(?:today|tonight|"
    r"now)|price|prices|cost|much|fee|weather|forecast|rain|sun|snow|wind|temperature|warm|cold\s+"
    r"tomorrow|today|tonight|tomorrow|weekend|sunday|saturday|monday|holiday|tide|traffic|delays?|"
    r"available|availability|in\s+stock|stock|timetable|timetables|times|schedule|next|"
    r"score|scores|result|results|kick\s+off|live)\b",
    re.IGNORECASE)

_NOT_ABOUT_THE_THING = re.compile(
    r"\s+(?:for|on)\s+(?:me|us)\b.*$"
    r"|\s+(?:online|on the internet|on the web)\b.*$"
    r"|,?\s+(?:please|thanks|ta|for me|for us)\s*$",
    re.IGNORECASE)


def _the_ask_inside_an_errand(text):
    line = str(text or "")
    match = _SEARCH_FRAME.match(line)
    if not match:
        return "", False
    rest = _NOT_ABOUT_THE_THING.sub("", line[match.end():]).strip(" ,.?!")
    if len(rest.split()) < 2:
        return "", False
    if _A_CLAUSE_WITH_NO_SUBJECT.match(rest):
        return "", False
    at_the_head = not (match.group("polite") or match.group("polite2") or "").strip()
    return rest, at_the_head


def _reaches(reading):
    if not isinstance(reading, dict):
        return False
    for key in REACHING_KEYS:
        value = reading.get(key)
        if value:
            return True
    return False


def _an_introduction_that_says_how_they_are(text):
    match = INTRODUCING_A_STATE.match(str(text or "").strip())
    if not match:
        return ""
    word = match.group(1).lower()
    if word in lexicon.A_DESCRIBING or word in lexicon.TRAITS or word in lexicon.A_STATE:
        return "im " + word
    return ""


INTRODUCING_A_STATE = re.compile(
    r"^\W*(?:(?:you can|please|just|ok|okay)\s+)*"
    r"(?:call me|my names?|my name['\u2019]s|my name is|im called|i am called|"
    r"i['\u2019]m called|known as)\s+"
    r"(?:(?:actually|honestly|properly|officially|tbh|really|very|so|quite|a bit|a little)\s+)*"
    r"([a-z][a-z'-]{1,19})"
    r"(?:\s*[,.!]*\s*(?:please|lol|lols|thanks|ta|cheers|then|btw|tbh|lmao|ha))?\s*[.!]*$", re.I)


def _said_of_themselves(words, place):
    back = place - 1
    while back >= 0 and words[back][0] in lexicon.FEELING_FILLER:
        back -= 1
    if back < 0:
        return False
    lead = words[back][0]
    if lead in lexicon.FEELING_LEAD:
        return True
    return (lead in ("was", "wasnt", "wasn't", "is", "isnt", "isn't", "get", "got")
            and back > 0 and words[back - 1][0] in ("i", "im", "i'm", "iam"))


def _confused_text(text):
    if not isinstance(text, str) or not text.strip():
        return "", []
    words = [(match.group(0).lower(), match.start(), match.end())
             for match in re.finditer(r"[A-Za-z']+", text)]
    if not words:
        return "", []
    pieces, pairs, cut = [], [], 0
    for place, (word, start, end) in enumerate(words):
        before = words[place - 1][0] if place else ""
        after = words[place + 1][0] if place + 1 < len(words) else ""
        meant = lexicon.CONFUSIONS.get(word)
        if not meant:
            pair = lexicon.CONFUSIONS_AFTER.get(word)
            if pair and before in pair[1]:
                meant = pair[0]
            else:
                pair = lexicon.CONFUSIONS_BEFORE.get(word)
                if pair and after in pair[1]:
                    meant = pair[0]
                elif not after:
                    meant = None
        if not meant:
            pair = lexicon.CONFUSIONS_IN_A_FEELING.get(word)
            if pair and (not after or after in pair[1]) and _said_of_themselves(words, place):
                meant = pair[0]
        if not meant and after in lexicon.QUESTION_WORDS:
            meant = lexicon.CONFUSIONS_BEFORE_A_QUESTION.get(word)
        if not meant or meant == word:
            continue
        pieces.append(text[cut:start])
        pieces.append(meant)
        cut = end
        pairs.append((word, meant))
    if not pairs:
        return "", []
    pieces.append(text[cut:])
    return "".join(pieces), pairs


CONSTRAINT_FACT = re.compile(
    r"^\s*(?:my|our|the)\s+(?:budget|price|cost|age|salary|wage|wages|income|savings|time|"
    r"spending|tariff|allowance)\s+(?:is|was|'s)\b")


def _a_constraint_on_the_thing(line):
    if not isinstance(line, dict):
        return False
    return CONSTRAINT_FACT.match(" ".join(line.get("norm") or ())) is not None


def _read_line(text, memory=None):
    memory = memory if isinstance(memory, dict) else {}
    line = normalise(_the_sugar_that_is_blood(
        _the_part_that_hurts(without_the_figure_of_speech(text))))
    read = kinds.classify(line)
    if read["kind"] == "thanks":
        after = kinds.the_line_after_a_courtesy(line["norm"])
        if after and after[0] not in THANKED_FOR and _about_something_of_its_own(after):
            line = normalise(" ".join(after))
            read = kinds.classify(line)

    history = _user_lines(memory, LOOKBACK)
    previous_text = history[-1] if history else None
    previous = normalise(previous_text) if previous_text else None
    previous_entities = topics.detect_entities(previous) if previous else []
    previous_topic = None
    if previous:
        previous_topic, _ = topics.detect_topic(previous, None, previous_entities)
    carried_text, carried = previous_text, previous
    carried_is_older = False
    constraint_before = _a_constraint_on_the_thing(previous)
    if previous and (not previous_entities or constraint_before):
        own_subject = None if constraint_before else topics.subject_topic(previous,
                                                                       previous_entities)
        earlier, earlier_entities = _pointed_at(history[:-1])
        if not earlier_entities and set(line["norm"]) & ANY_PRONOUN:
            earlier, earlier_entities = _the_recorded_subject(memory)
            carried_is_older = bool(earlier_entities)
        if earlier_entities and own_subject is not None and not constraint_before:
            earlier_subject = topics.subject_topic(earlier, earlier_entities)
            if earlier_subject is not None and earlier_subject != own_subject:
                earlier, earlier_entities = None, []
                carried_is_older = False
        if earlier_entities:
            previous_entities = earlier_entities
            carried_text, carried = earlier["text"], earlier
            if previous_topic is None:
                previous_topic = topics.detect_topic(earlier, None, earlier_entities)[0]

    ref = references.resolve(line, read, previous, previous_entities, previous_topic)
    about = kinds.after_any_link(line["norm"])
    topic_line = line
    after_entities = topics.detect_entities(normalise(" ".join(about))) if about else None
    if after_entities is not None and topics.subject_topic(
            normalise(" ".join(about)), after_entities) is not None:
        topic_line, entities = normalise(" ".join(about)), after_entities
    else:
        entities = topics.detect_entities(line)
    continues = ref["followup"] or topics.subject_topic(topic_line, entities) is None
    inherited = None
    if continues and not _changes_subject(line):
        claimed = memory.get("topic")
        if isinstance(claimed, str) and claimed:
            inherited = claimed
        else:
            inherited = _recent_topic(history) or previous_topic

    if (read["kind"] == "statement" and not read["asks"]
            and any(entity["type"] == "place" for entity in entities)
            and kinds.noun_phrase_request(line)):
        read["intent"] = "request"
        read["asks"] = ["recommend"]
        read["replies_to_bot"] = False
    asks_something = read["kind"] == "question" or read["intent"] in ("request", "advice")
    own_topic, own_score = topics.detect_topic(topic_line, None, entities, asks_something)

    topic, score = topics.detect_topic(topic_line, inherited, entities, asks_something)
    ranked = [name for name, points in topics.rank_topics(topic_line, None, entities, asks_something)]
    if _a_stop_in_a_chat_about_something(line["norm"], memory):
        if read.get("intent") == "about_bot":
            read["intent"] = "question"
        read["about_bot"] = False
        read["about_bot_kind"] = None
    if (topic is None and not kinds.opening_line(line["norm"])
            and _about_the_bot(line, read, entities)):
        topic = ABOUT_THE_BOT
        ranked = [ABOUT_THE_BOT] + [name for name in ranked if name != ABOUT_THE_BOT]
    elif topic is None and read["intent"] in ("greeting", "smalltalk"):
        topic = "small-talk"
    elif (topic is None and read.get("state_owner") == "self" and read.get("emotion")
          and not entities and read["intent"] not in ("question", "request")):
        topic = "feelings"
        ranked = ["feelings"] + [name for name in ranked if name != "feelings"]
    if read["kind"] == "question" and topic == "small-talk" and OWN_QUESTION_TOPIC in ranked:
        topic = OWN_QUESTION_TOPIC
        ranked = [OWN_QUESTION_TOPIC] + [name for name in ranked if name != OWN_QUESTION_TOPIC]
    subject = next((entity["text"].lower() for entity in entities
                    if entity["type"] in SUBJECT_TYPES), None)
    ask_subject, setting, subject_from = _the_thing_the_ask_names(
        line["clauses"], line.get("focus"), entities)
    topic_from = topics.the_words_that_said(line, topic, entities)
    leans_on = _leans_on(line, read, ref, carried_text, carried, previous, own_topic,
                         previous_topic, previous_entities, carried_is_older,
                         memory.get("topic"))

    intent = read["intent"]
    if not ranked and intent in ("question", "request", "news", "statement", "ack") \
            and kinds.opening_line(line["norm"]):
        intent = "opening"
    elif not entities and not leans_on and intent in ("question", "request") \
            and _opens_the_conversation(previous) \
            and not (previous_topic or previous_entities) \
            and asks_with_nothing_named(line["norm"]):
        intent = "opening"
    elif intent in ("question", "request", "news", "statement", "ack") \
            and kinds.talk_frame(line["norm"]):
        intent = "opening"
    presence = _presence(line) or _asks_for_a_moment(line)
    if presence and read["intent"] in PRESENCE_NOT:
        presence = (bool(set(line["norm"]) & (PRESENCE_SUBJECT | PRESENCE_ASKER))
                    or _asks_for_a_moment(line))
    if presence:
        intent = "presence"

    plain = _a_word_that_depends_on_the_owner(line["plain"], entities, read["state_owner"])

    words = breeds.the_animal_a_breed_is(line["words"])
    animal_in_hand = references.the_animal_in_hand(ref, words)
    if not animal_in_hand:
        animal_in_hand = references.the_animal_the_chat_is_on(
            words, memory.get("understood") if isinstance(memory, dict) else None)

    over_time, over_time_what = kinds.over_time(line, read)
    last_read = memory.get("understood") if isinstance(memory, dict) else None

    out = {
        "text": text if isinstance(text, str) else "",
        "clean": line["clean"],
        "words": words,
        "plain": plain,
        "animal_in_hand": animal_in_hand,
        "change_of_subject": bool(line.get("change_of_subject")),
        "dropped_subject": line["dropped_subject"],
        "sense": senses.senses(line),
        "over_time": over_time,
        "over_time_what": over_time_what,
        "kept": line.get("kept"),
        "kind": "question" if presence else read["kind"],
        "intent": intent,
        "asks_how_i_am": (kinds.asks_how_i_am(line["norm"])
                          and intent in ("smalltalk", "greeting")),
        "presence": presence,
        "asks": read["asks"],
        "tag": bool(read.get("tag")),
        "taking_up": kinds.taking_up(line, read),
        "shift": kinds.shift_worked(line["clean"]),
        "care_home": (kinds.a_care_home(line["clean"])
                      or kinds.a_home_carried_forward(line["clean"],
                                                      _user_lines(memory, HOME_LOOKBACK))),
        "setup": kinds.the_setup(line),
        "help_ask": read["help_ask"],
        "asks_a_verdict": read["asks_a_verdict"],
        "emotion": read["emotion"],
        "state_owner": read["state_owner"],
        "shortage": read.get("shortage"),
        "polarity": read["polarity"],
        "warmth": topics.the_warmth_said(line["norm"]),
        "body": body.read(line["norm_text"]),
        "own_output": topics.own_output_word(line["norm"]),
        "short": read["short"],
        "first_person": read["first_person"],
        "about_bot": read["about_bot"],
        "about_bot_kind": read["about_bot_kind"],
        "counts_the_bots_own_day": bool(read.get("counts_the_bots_own_day")),
        "replies_to_bot": read["replies_to_bot"],
        "agrees_to_try": bool(read.get("agrees_to_try")) and intent == "ack",
        "wants_a_quiz": bool(read.get("wants_a_quiz")),
        "agreement": read.get("agreement"),
        "tight_on_money": topics.tight_on_money(line["norm"], read["kind"],
                                                line.get("text") or ""),
        "amount_left": topics.purse_till_at(line["norm"], line.get("text") or "") is not None,
        "routine": kinds.is_a_routine(line, read),
        "a_load_carried": a_load_carried(line["clean"]),
        "car_fault": cars.a_broken_car_is_the_subject(
            line["clean"], _user_lines(memory, cars.LOOKBACK)),
        "summons": read["summons"],
        "asks_back": read["asks_back"],
        "stand_in": _stand_in_here(text),
        "excludes": read.get("excludes") or [],
        "constraint": bool(read.get("constraint")),
        "confusion": confusion.confusion_of(line),
        "suggestion": read.get("suggestion"),
        "ruled_out": read.get("ruled_out") or [],
        "norm": line["norm"],
        "norm_text": line["norm_text"],
        "fixes": line["fixes"],
        "clauses": line["clauses"],
        "focus": line["focus"],
        "asking": line.get("asking") or line["focus"],
        "signals": line["signals"],
        "topic": topic,
        "topic_score": score,
        "topics": ranked,
        "topic_own": own_topic,
        "topic_own_score": own_score,
        "topic_from": topic_from,
        "topic_is_a_brush": all(weight < 2 for _word, weight in topic_from),
        "unsure": topics.unsure_words(line.get("norm") or [], own_topic or topic),
        "entities": entities,
        "person_names": topics.person_names(line),
        "background": [line["norm"][index] for index in
                       sorted(background_positions(line["norm"]))],
        "intensifier": list(line.get("intensifier") or []),
        "intensifier_left": list(line.get("intensifier_left") or []),
        "subject": subject,
        "subject_unclear": topics.unclear_subject(line["norm"], inherited, previous),
        "ask_subject": ask_subject,
        "setting": setting,
        "subject_from": subject_from,
        "numbers": topics.detect_numbers(line),
        "tried": attempts.things_tried(line["text"] if isinstance(line.get("text"), str) else "",
                                       line["norm"]),
        "keywords": _keywords(line["norm"]),
        "ref": ref,
        "followup": ref["followup"],
        "someone_new": references.person_is_new(line, previous_entities),
        "asks_what_was_meant": (read["asks_what_was_meant"]
                                  and _the_meaning_is_applied_to_what_was_said(line, leans_on,
                                                                              memory)),
        "leans_on": leans_on,
    }
    carrying_on = kinds.over_time(line, out, last_read, carrying_on=True)
    if carrying_on is not None:
        out["over_time"], out["over_time_what"] = carrying_on
    return out
