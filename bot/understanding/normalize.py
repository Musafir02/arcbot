import itertools
import re
import unicodedata

from . import lexicon

_MEASURE = (r"[0-9]+(?:[.,][0-9]+)*[a-z%]*"
            r"|[a-z]{1,3}[0-9]+(?:[a-z]{1,3}[0-9]*)*(?![a-z0-9])"
            r"|[a-z]+(?:'[a-z]+)*")
WORD = re.compile(_MEASURE)
SAID_OUT = {word: lexicon.CHAT[word]
            for word in lexicon.PLAIN_EXPANDS | lexicon.PLAIN_ONE_WORD
            if word in lexicon.CHAT and word not in lexicon.EXPAND}

CHAT_KEPT_AS_TYPED = frozenset("""
    u ur urs yr yrs urself y r n k b c d v x ar av sed prob cause cos tho owt
    wif wtf pressie pressies prezzie prezzies prezzy
    """.split())
CHAT_AS_ONE_WORD = {word: meaning for word, meaning in lexicon.CHAT.items()
                    if " " not in meaning and word not in CHAT_KEPT_AS_TYPED
                    and word not in SAID_OUT}
SAID_OUT.update(CHAT_AS_ONE_WORD)

RAW_WORD = re.compile(_MEASURE)


URGENT_WORDS = frozenset(lexicon.URGENT_MISSPELLINGS.values()) | frozenset(("having",))

_ANY_WORD = re.compile(r"[a-z]+(?:'[a-z]+)*", re.IGNORECASE)


def respell_urgent(text):
    if not isinstance(text, str) or not text:
        return ""
    fixes = lexicon.URGENT_MISSPELLINGS

    def put(match):
        word = match.group(0)
        fix = fixes.get(word.lower())
        if not fix:
            guessed = fix_typo(word.lower())
            return guessed if guessed in URGENT_WORDS else word
        keep = word[:1].isupper()
        return fix.capitalize() if keep else fix

    return CLIPPED_FAMILY.sub(_family_put_back, _ANY_WORD.sub(put, text))


CLIPPED_FAMILY = re.compile(
    r"\b(?P<owner>my|our|his|her|their)\s+(?P<word>dd|ds|dh|mil|fil|sil|bil|oh|lo)\b"
    r"(?P<rest>(?:\s+[a-z']+){0,2})", re.IGNORECASE)


def _family_put_back(match):
    rest = (match.group("rest") or "").split()
    after = rest[0].lower() if rest else None
    after_after = rest[1].lower() if len(rest) > 1 else None
    family = _family_short(match.group("word").lower(), match.group("owner").lower(),
                           after, after_after)
    if not family:
        return match.group(0)
    return match.group("owner") + " " + " ".join(family) + (match.group("rest") or "")


def _doubles_its_last_letter(word):
    if len(word) < 3 or not word.isalpha():
        return False
    if word[-3] in "aeiou" or word[-2] not in "aeiou" or word[-1] in "aeiouwxy":
        return False
    return len(re.findall(r"[aeiou]+", word)) == 1


VOWEL_SET = frozenset("aeiou")
VOWEL_SET_OR_Y = VOWEL_SET | frozenset("y")


def _drops_a_final_e(word):
    return word.endswith("e") and len(word) > 2


def _keeps_its_e_before_ing(word):
    return len(word) > 2 and word.endswith(("ee", "ye", "oe"))


def _ing_form(word):
    return word + "ing" if _keeps_its_e_before_ing(word) else word[:-1] + "ing"


def _inflections(word):
    out = set()
    if len(word) < 3 or not word.isalpha():
        return out
    y_for_i = word.endswith("y") and word[-2] not in VOWEL_SET
    out.add(word + "ly")
    if not y_for_i:
        out.add(word + "s")
    if _doubles_its_last_letter(word):
        out.update((word + word[-1] + "ing", word + word[-1] + "ed", word + word[-1] + "er"))
    elif _drops_a_final_e(word):
        out.update((_ing_form(word), word[:-1] + "ed", word[:-1] + "er"))
    else:
        out.add(word + "ing")
        if not y_for_i:
            out.update((word + "ed", word + "er"))
    if word.endswith("e"):
        out.update((word[:-1] + "ing", word[:-1] + "ed"))
    if word.endswith("y"):
        out.update((word[:-1] + "ies", word[:-1] + "ied", word[:-1] + "ier"))
    if word.endswith("s"):
        out.add(word[:-1])
    return out


_BASE = (
    lexicon.COMMON.split() + lexicon.CORE.split()
    + " ".join(lexicon.CHAT.values()).split()
    + " ".join(lexicon.EXPAND.values()).split()
    + " ".join(lexicon.MISSPELLINGS.values()).split()
    + " ".join(lexicon.REAL_WORDS).split()
)
BASE = frozenset(_BASE)
LEXICON = BASE | frozenset(f for word in _BASE for f in _inflections(word))
COMMON_RANK = {word: i for i, word in enumerate(lexicon.CORE.split() + lexicon.COMMON.split())}

ME_FOR_MY_CLOSES = frozenset("""
    is are was were am be been being isnt arent wasnt werent aint
    has have had having got gets getting get
    will wont would could should can cant cannot must might may shall
    do does did doing done dont doesnt didnt
    hurts hurt hurting aches ache aching bangs bang banging throb throbs throbbing kills kill
    feels feel feeling looks look looking smells smell smelling sounds sound sounding seems seem
    needs need wants want keeps keep kept goes go going went comes come coming came broke broken
    breaks break stopped stops started starts works worked died dies dying
    in on out off up down at to for with from by about over under around through into onto
    and or but so because as than then
    not no never still too also just again now today tomorrow yesterday tonight anymore
    all both every any some
""".split())

THING_WORDS_BY_LENGTH = {}
THING_WORDS = set()


def learn_thing_words(words):
    for word in words:
        if isinstance(word, str) and word.isalpha() and len(word) > 2:
            THING_WORDS.add(word)
            THING_WORDS_BY_LENGTH.setdefault(len(word), set()).add(word)

PHRASES = sorted(
    {k: v for k, v in lexicon.CHAT.items() if " " in k or "/" in k or "&" in k}.items()
    | {k: v for k, v in lexicon.MISSPELLINGS.items() if " " in k}.items(),
    key=lambda item: -len(item[0]),
)

BREAKS = frozenset(
    "anyway anyways btw actually instead otherwise also plus so but then oh ok okay right now "
    "still however meanwhile finally".split()
)
PRONOUN_BASES = frozenset(
    "i it that this there here he she we they who what where how when why everyone somebody "
    "someone nobody everybody one".split()
)
ASK_WORDS = frozenset(
    "what why how when where who which whose can could should would is are do does did will "
    "have has shall may might am was were".split()
)
WANT_WORDS = frozenset(
    "want need like looking help recommend suggest advice idea ideas tip tips know wonder "
    "thinking plan trying".split()
)
WH_WORDS = frozenset("what why when where who which whose".split())
AUX_WORDS = frozenset(
    "is are was were am do does did can could should would will shall have has may might".split()
)
BE_WORDS = frozenset("is are was were am".split())
SUBJECT_WORDS = frozenset("i we you they he she".split())
HOW_DEGREE = frozenset(
    "long much many often old far big soon hot cold tall early late heavy deep".split()
)
NO_ASK_AFTER = frozenset("that if whether what why when where who which whose how".split())
ASK_NOUNS = frozenset("""time day date week month year kind sort type colour color size
amount number temperature age price reason way one ones much many long often far""".split())
REPORTING = frozenset("""know knows knew known tell tells told say says said ask asks asked
wonder wondered wondering remember remembered forget forgot decide decided sure idea clue
mean means meant matter matters question doubt explain explains argue argued arguing
disagree disagreed discuss discussed debate debated talk talked mention mentioned
consider considered""".split())
COPULAS = frozenset("is are was were am be been being".split())
NOMINAL_BEFORE_COPULA = frozenset("""this that it there here all exactly precisely just
question thing problem point issue doubt reason answer part bit main only also still really
actually probably""".split())
DETERMINERS = frozenset("""a an the my your his her our their its this that these those
some any no every each another anyone everyone someone nobody people ones""".split())
RELATIVE = frozenset("who which whose".split())
RELATIVE_ASKS = frozenset("could can should would will shall do does did".split())


FREQUENT = frozenset((lexicon.CORE + " " + lexicon.COMMON).split()[:420])
AEIOU = frozenset("aeiou")
VOWELS = "aeiou"


def _double_variants(word):
    out = set()
    for i, char in enumerate(word):
        if char in VOWELS + "y":
            continue
        if i + 1 < len(word) and word[i + 1] == char:
            out.add(word[:i] + word[i + 1:])
        else:
            out.add(word[:i] + char + word[i:])
    return out


def _a_doubled_letter_typed_once(word):
    out = set()
    for i, char in enumerate(word):
        if char.isalpha():
            out.add(word[:i] + char + word[i:])
    return out


def _three_of_a_letter(word):
    return any(word[at] == word[at + 1] == word[at + 2] for at in range(len(word) - 2))


def _doubled_letter_words(word):
    if word in LEXICON:
        return []
    return [w for w in _a_doubled_letter_typed_once(word)
            if (w in BASE or (w in LEXICON and w + "s" not in BASE))
            and not _three_of_a_letter(w)]


def _ie_variants(word):
    out = set()
    for pair, other in (("ie", "ei"), ("ei", "ie")):
        start = word.find(pair)
        while start != -1:
            out.add(word[:start] + other + word[start + 2:])
            start = word.find(pair, start + 1)
    return out


S_CLUSTERS = "tpskmlnwhqc"


def _missing_vowel(word):
    if len(word) < 5 or word in LEXICON:
        return ()
    out = set()
    for i in range(1, len(word) + 1):
        start = i
        while start > 0 and word[start - 1] not in VOWELS:
            start -= 1
        end = i
        while end < len(word) and word[end] not in VOWELS:
            end += 1
        cluster = word[start:end]
        if len(cluster) < 3 or (cluster[0] == "s" and cluster[1] in S_CLUSTERS):
            continue
        for vowel in VOWELS:
            candidate = word[:i] + vowel + word[i:]
            if candidate in BASE:
                out.add(candidate)
    return out


def _extra_vowel(word):
    if len(word) < 8:
        return ()
    out = set()
    for i, char in enumerate(word):
        if char not in "ei" or i + 1 == len(word):
            continue
        before = word[i - 1] if i else ""
        after = word[i + 1]
        if before in VOWELS or after in VOWELS:
            out.add(word[:i] + word[i + 1:])
    return out


_A_WORDS = frozenset("cola tuna mocha salsa karma pasta data area idea".split())


def _a_said_for_an_ending(word):
    if word in _A_WORDS:
        return ()
    if word.endswith("as") and len(word) >= 5:
        stem, plural = word[:-2], "s"
    elif word.endswith("a") and len(word) >= 4:
        stem, plural = word[:-1], ""
    else:
        return ()
    if stem[-1:] in VOWELS:
        return ()
    return tuple(stem + ending + plural for ending in ("er", "or", "ar", "ow"))


def _dropped_letter(word):
    if len(word) < 3 or word.endswith("w"):
        return ()
    return (word + "w",)


def _an_ing_said_as_n(word):
    if (len(word) < 5 or not word.endswith("n") or word in LEXICON
            or word in lexicon.COMMON_NAMES):
        return None
    if any(char in VOWELS for char in word[-3:-1]):
        return None
    stem = word[:-1]
    forms = [stem + "ing"]
    if len(stem) > 1 and stem[-1] == stem[-2]:
        forms.append(stem[:-1] + stem[-1] + "ing")
    known = {form for form in forms if form in LEXICON}
    if len(known) == 1:
        return known.pop()
    return None


def _a_leading_h(word):
    if len(word) < 4 or word[:1] not in "aeiou":
        return ()
    if word.endswith("s") and word[:-1] in BASE:
        return ()
    return ("h" + word,)


E_KEPT_WORDS = frozenset({"dyeing", "singeing", "tingeing", "swingeing"})


def _e_kept_before_ing(word):
    if len(word) < 6 or not word.endswith("eing") or word in E_KEPT_WORDS:
        return ()
    shorter = word[:-4] + "ing"
    return (shorter,) if shorter in LEXICON else ()


def _swapped_pair(word):
    if len(word) < 5 or _a_word_the_bot_writes(word):
        return ()
    out = set()
    for at in range(len(word) - 1):
        pair = word[at:at + 2]
        if len(pair) < 2 or pair[0] == pair[1]:
            continue
        if pair[0] in VOWELS or pair[1] in VOWELS:
            continue
        out.add(word[:at] + word[at + 1] + word[at] + word[at + 2:])
    return out


def _two_letters_the_wrong_way_round(word):
    if len(word) < 5 or word in LEXICON or _a_word_the_bot_writes(word):
        return ()
    out = set()
    for at in range(len(word) - 1):
        pair = word[at:at + 2]
        if pair[0] == pair[1]:
            continue
        if (pair[0] in VOWELS) == (pair[1] in VOWELS):
            continue
        made = word[:at] + pair[1] + pair[0] + word[at + 2:]
        if made not in NO_SWAP_TO:
            out.add(made)
    return out

NO_SWAP_TO = frozenset(("hanged",))


_A_WORD_THE_BOT_WRITES = None


def _words_the_bot_writes():
    global _A_WORD_THE_BOT_WRITES
    if _A_WORD_THE_BOT_WRITES is None:
        words = set()
        try:
            from bot.knowledge import entries as knowledge_entries
            from bot.knowledge import lookup as knowledge_lookup
            for entry in knowledge_entries():
                for field in ("reply", "ask", "key", "id", "domain"):
                    value = getattr(entry, field, "")
                    for text in (value if isinstance(value, (list, tuple, set)) else [value]):
                        if isinstance(text, str):
                            words.update(knowledge_lookup.tokens(text))
            _, _, known = knowledge_lookup._vocabulary(knowledge_entries())
            words.update(word for word in known if isinstance(word, str))
        except Exception:
            pass
        _A_WORD_THE_BOT_WRITES = frozenset(
            word.lower() for word in words if word.isalpha())
    return _A_WORD_THE_BOT_WRITES


def _a_word_the_bot_writes(word):
    if word in lexicon.TYPED_WORDS or word in lexicon.COMMON_NAMES:
        return True
    return word in _words_the_bot_writes()


def _bones(word):
    return "".join(char for char in word if char not in VOWELS)


def _longest_consonant_run(word):
    run = best = 0
    for char in word:
        if char in VOWELS or char == "y":
            run = 0
        else:
            run += 1
            if run > best:
                best = run
    return best


URGENT_BONES = {}


def _an_emergency_word_left_out(word):
    if len(word) < 6 or word in LEXICON or _longest_consonant_run(word) < 3:
        return None
    if not URGENT_BONES:
        for known in URGENT_WORDS:
            URGENT_BONES.setdefault(_bones(known), []).append(known)
    found = [known for known in URGENT_BONES.get(_bones(word), ()) if len(known) > len(word)]
    return found[0] if len(found) == 1 else None


NAME_FRAMES = frozenset("called named".split())

CHAT_NAMES = frozenset(word for word in lexicon.CHAT if word in lexicon.COMMON_NAMES)
NAME_ROLL = frozenset("""names name named go goes going by im am i'm""".split())
NAME_CALLS = frozenset("""call calls called calling callin name names named""".split())


def _a_name_slot(before, before_before, word):
    if not word.isalpha() or len(word) < 2 or word in LEXICON:
        return False
    if before in NAME_FRAMES:
        return True
    if before in BE_WORDS and before_before == "name":
        return True
    if word in CHAT_NAMES and (before in NAME_ROLL
                               or (before in ("me", "you", "u") and before_before in NAME_CALLS)
                               or (before == "not"
                                   and before_before in BE_WORDS | {"im", "i"})):
        return True
    return (word in lexicon.COMMON_NAMES
            and before in KIN and before_before in POSSESSIVES)


def _dropped_g(word):
    if (len(word) < 4 or not word.endswith("in") or word in LEXICON
            or word in lexicon.REAL_IN or word in lexicon.COMMON_NAMES):
        return None
    longer = word + "g"
    if longer in LEXICON:
        return longer
    stem = word[:-2]
    if _drops_a_final_e(stem) and len(stem) > 2:
        dropped = _ing_form(stem)
        if dropped in LEXICON:
            return dropped
    stem = word[:-2]
    if len(stem) > 3 and stem[-1] == stem[-2]:
        stem = stem[:-1]
    if _doubles_its_last_letter(stem) and (stem in BASE or stem in LEXICON):
        doubled = stem + stem[-1] + "ing"
        if doubled in LEXICON:
            return doubled
    return None


STOPPED_TH_STEMS = {
    "any": "anything", "eny": "anything", "ani": "anything",
    "some": "something", "sum": "something", "som": "something", "sumn": "something",
    "every": "everything", "evry": "everything", "evrey": "everything",
    "nuf": "nothing", "nuff": "nothing", "nof": "nothing", "noff": "nothing",
    "nut": "nothing", "nuth": "nothing", "not": "nothing", "no": "nothing",
}


def _stopped_th(word):
    if len(word) < 5 or word in LEXICON:
        return None
    for suffix in ("fings", "fing", "finks", "fink", "fins", "fin"):
        if word.endswith(suffix):
            stem = word[:-len(suffix)]
            break
    else:
        return None
    plural = suffix.endswith("s")
    found = STOPPED_TH_STEMS.get(stem)
    return found + "s" if found and plural else found


SHION_WORDS = frozenset("""
cushion fashion passion mission session version decision occasion discussion permission
television conclusion explosion confusion illusion vision revision division provision
suggestion tension expression compassion impression profession possession aggression
admission commission expansion extension pension mansion excursion invasion collision
emission transmission procession succession confession depression digression obsession
recession concession progression exclusion inclusion seclusion precision derision
magician musician electrician politician technician physician statistician optician
beautician mathematician paediatrician dietician clinician""".split())


def _shun_variant(word):
    if word in LEXICON:
        return None
    if word.endswith("shuns") and len(word) > 7:
        singular = _shun_variant(word[:-1])
        if singular:
            return singular + "s"
        return None
    if word.endswith("kshun"):
        stem = word[:-5]
    elif word.endswith("shun"):
        stem = word[:-4]
    else:
        return None
    if len(stem) < 2 or not stem.isalpha():
        return None
    kept = stem + "s"
    for spelled in (stem + "shion", stem + "ssion", stem + "sion", stem + "tion",
                    kept + "tion", kept + "ssion", kept + "sion", stem + "cian"):
        if spelled in LEXICON or spelled in SHION_WORDS:
            return spelled
    return stem + "tion"


F_TYPED_FOR_TH = {
    "fe": "the", "fis": "this", "fey": "they", "fem": "them", "fere": "there",
    "fing": "thing", "fings": "things", "fird": "third",
    "fousand": "thousand", "fousands": "thousands",
    "freat": "threat", "freaten": "threaten", "freatens": "threatens",
    "freatened": "threatened", "freatening": "threatening",
}


def _said_with_an_f(word):
    if word in F_TYPED_FOR_TH:
        return F_TYPED_FOR_TH[word]
    if not word.isalpha() or not word.startswith("f") or word in LEXICON:
        return None
    if len(word) < 4:
        return None
    spelled = "th" + word[1:]
    if spelled in LEXICON or spelled in lexicon.CHAT or spelled in lexicon.EXPAND:
        return spelled
    for ending in ("s", "es", "d", "ed", "ing"):
        stem = spelled[:-len(ending)]
        if spelled.endswith(ending) and len(stem) >= 5 and stem in LEXICON:
            return spelled
    if spelled.endswith("in") and spelled + "g" in LEXICON:
        return spelled + "g"
    return None


A_THING_TYPED_AS_A_LITTLE_WORD = {
    "wif": "wife",
    "wiff": "wife",
}
A_THING_GOES_AFTER = frozenset("the".split())


def _said_with_an_f_anywhere(word):
    if len(word) < 3 or not word.isalpha() or "f" not in word or word in LEXICON:
        return None
    if word.endswith("ff"):
        if word.startswith("w"):
            return None
        spelled = word[:-2] + "th"
        return spelled if spelled in LEXICON else None
    for at, letter in enumerate(word):
        if letter != "f":
            continue
        spelled = word[:at] + "th" + word[at + 1:]
        if spelled in LEXICON:
            return spelled
    return None


def _a_thing_where_a_thing_goes(word, before):
    if before not in POSSESSIVES and before not in A_THING_GOES_AFTER:
        return None
    thing = A_THING_TYPED_AS_A_LITTLE_WORD.get(word)
    return thing if thing in LEXICON else None


def _missing_e(word):
    if len(word) < 4 or not word.endswith("d") or word in LEXICON:
        return None
    if word.endswith("yd"):
        if word[-3] in VOWELS or word[-3] == "y":
            return None
        longer = word[:-2] + "ied"
        return longer if longer in LEXICON else None
    if word[-2] not in MISSING_E_AFTER:
        return None
    longer = word[:-1] + "ed"
    return longer if longer in LEXICON else None


def _short_double(word):
    if len(word) < 3 or word in LEXICON:
        return None
    variants = _double_variants(word)
    if word[-1] == word[-2]:
        variants.add(word[:-1])
    keep = [variant for variant in variants
            if variant in LEXICON and variant in FREQUENT]
    keep.sort(key=lambda variant: COMMON_RANK.get(variant, 10 ** 6))
    return keep[0] if keep else None




def _one_letter_apart(word, other):
    if abs(len(word) - len(other)) > 1:
        return False
    if len(word) == len(other):
        differ = [i for i in range(len(word)) if word[i] != other[i]]
        if len(differ) == 1:
            i = differ[0]
            return word[i] in VOWEL_SET_OR_Y and other[i] in VOWEL_SET_OR_Y
        if len(differ) == 2:
            i, j = differ
            return j == i + 1 and word[i] == other[j] and word[j] == other[i]
        return False
    short, long = (word, other) if len(word) < len(other) else (other, word)
    i = 0
    while i < len(short) and short[i] == long[i]:
        i += 1
    if i == len(short):
        return False
    if short[i:] != long[i + 1:]:
        return False
    if word is long:
        return long[i] in VOWEL_SET
    return True


CORE_VERBS = frozenset("""take get give make have go do say see know think want need feel look
    come wake walk work eat drink buy pay keep leave sleep live start stop try help tell ask
    call find bring wear watch read cook clean wash sit stand run drive ride""".split())
AFTER_A_VERB = frozenset("up off out in on back over down away".split())
BEFORE_A_VERB = frozenset("i we they you he she".split())


def _one_letter_wrong(word, other):
    if abs(len(word) - len(other)) > 1:
        return False
    if len(word) == len(other):
        differ = [i for i in range(len(word)) if word[i] != other[i]]
        if len(differ) == 1:
            return True
        if len(differ) == 2:
            i, j = differ
            return j == i + 1 and word[i] == other[j] and word[j] == other[i]
        return False
    short, long = (word, other) if len(word) < len(other) else (other, word)
    i = 0
    while i < len(short) and short[i] == long[i]:
        i += 1
    return short[i:] == long[i + 1:]


def _a_word_the_reading_knows(word):
    if _known_word(word):
        return True
    return any(_known_word(stem) for stem in _stems_of(word))


def _known_word(word):
    return word in LEXICON or word in THING_WORDS


def _stems_of(word):
    stems = set()
    if word.endswith("ing") and len(word) > 5:
        stems.update((word[:-3], word[:-3] + "e"))
    if word.endswith("ed") and len(word) > 4:
        stems.update((word[:-2], word[:-1]))
    if word.endswith("es") and len(word) > 5:
        stems.add(word[:-2])
    if word.endswith("s") and len(word) > 4:
        stems.add(word[:-1])
    return stems


def _a_thing_a_letter_short(word):
    if len(word) < 4:
        return None
    if _a_word_the_bot_writes(word) or _a_word_the_reading_knows(word):
        return None
    fits = [w for w in THING_WORDS_BY_LENGTH.get(len(word) + 1, ())
            if w[0] == word[0] and w[-1] == word[-1] and _one_letter_wrong(word, w)]
    return fits[0] if len(fits) == 1 else None


def _a_core_verb_typed_wrong(word, before, after=None):
    if not word.isalpha() or len(word) < 3 or len(word) > 7:
        return None
    if before not in BEFORE_A_VERB:
        return None
    if word in LEXICON or word in lexicon.COMMON_NAMES or word in _words_the_bot_writes():
        return None
    found = {verb for verb in CORE_VERBS if _one_letter_wrong(word, verb)}
    if word.endswith("d"):
        found.discard(word[:-1])
    if not found and after in AFTER_A_VERB:
        found = {verb for verb in CORE_VERBS if _its_vowels_typed_wrong(word, verb)}
    if len(found) == 1:
        return found.pop()
    return None


def _its_vowels_typed_wrong(word, other):
    if word == other or word[0] != other[0] or not other.startswith(word[0]):
        return False
    if abs(len(word) - len(other)) > 1:
        return False
    consonants = "".join(letter for letter in word if letter not in "aeiou")
    return consonants and consonants == "".join(letter for letter in other if letter not in "aeiou")


def _near_a_part(word):
    if len(word) < 3 or not word.isalpha() or word in LEXICON or word in lexicon.BODY_PARTS:
        return None
    found = set()
    for part in lexicon.BODY_PARTS:
        if len(part) < 4 or abs(len(part) - len(word)) != 1:
            continue
        short, long = (word, part) if len(word) < len(part) else (part, word)
        i = 0
        while i < len(short) and short[i] == long[i]:
            i += 1
        if short[i:] == long[i + 1:]:
            found.add(part)
    return found.pop() if len(found) == 1 else None


PART_REACH = 3


A_SIDE = frozenset("five six seven eight nine".split())


ABOUT_THE_FORM = re.compile(r"""
    \bhow\s+many\s+(?:players?|people|a\s+side)\b
  | \bhow\s+(?:long|many\s+halves)\b[^.]{0,40}\b(?:match|game|half|halves)\b
  | \b(?:the\s+)?rules?\b
  | \boffside\b
  | \bhow\s+big\b
  | \bpitch\s+(?:size|dimensions)\b
  | \bfull\s+(?:match|game)\b
""", re.VERBOSE | re.IGNORECASE)
FINDING_A_TEAM = re.compile(r"""
    \b(?:join|joining|find|finding|looking\s+for|sign\s+up\s+(?:for|to)|get\s+into)\b
  | \bteams?\b[^.]{0,24}\b(?:in|near|around|local)\b
  | \b(?:clubs?|leagues?)\b
""", re.VERBOSE | re.IGNORECASE)


def _a_game_named_another_way(norm, words):
    flat = " ".join(norm)
    if ABOUT_THE_FORM.search(flat) or FINDING_A_TEAM.search(flat):
        return norm, words
    if (any(word in lexicon.BODY_PARTS for word in words)
            and any(word in lexicon.PAIN_WORDS for word in words)):
        return norm, words
    out = []
    read = []
    index = 0
    while index < len(norm):
        if (norm[index] in A_SIDE and index + 2 < len(norm)
                and norm[index + 1] == "a" and norm[index + 2] == "side"):
            out.append("football")
            read.append("football")
            index += 3
            continue
        if norm[index] == "kickabout" or (norm[index] == "kick"
                                          and norm[index + 1:index + 2] == ["about"]):
            out.append("football")
            read.append("football")
            index += 1 if norm[index] == "kickabout" else 2
            continue
        out.append(norm[index])
        index += 1
    if not read or "football" in words:
        return out, words
    return out, list(words) + ["football"]


def _parts_that_hurt(words, fixes):
    pain = [at for at, word in enumerate(words) if word in lexicon.PAIN_WORDS]
    if not pain:
        return words
    out = []
    for at, word in enumerate(words):
        part = _near_a_part(word)
        beside = at - 1 in pain or at + 1 in pain
        mine = words[at - 1:at] in (["my"], ["our"]) and any(
            abs(other - at) <= PART_REACH for other in pain)
        if part and (beside or mine):
            fixes.append((word, part))
            out.append(part)
        else:
            out.append(word)
    return out


def _where_a_state_stands(before, before_before, after, before_words=None):
    words = [word for word in (before_words if before_words is not None
                               else (before_before, before)) if word is not None]
    if words and words[-1] in DETERMINER_IN_FRONT:
        done_to = (words[-1] in POSSESSIVE_IN_FRONT
                   and any(word in CAUSES_A_STATE for word in words))
        if not done_to:
            return False
    end = len(words) - 1
    back = end
    while back >= 0 and _measures_a_state(words[back]):
        back -= 1
    if back < 0:
        return _opens_a_state(after)
    stands = words[back]
    if stands in BE_BEFORE_A_STATE:
        return True
    if stands in THIRD_PERSON_BE:
        return _ends_a_state(after, opening=not (back >= 1 and (words[back - 1] in PERSON_WORDS
                                                               or words[back - 1] in OBJECT_PRONOUN)))
    if stands in CAUSES_A_STATE:
        return back < end or _ends_a_state(after)
    if stands in OBJECT_PRONOUN and back >= 1 and words[back - 1] in CAUSES_A_STATE:
        return True
    if stands == "my" and back >= 1 and words[back - 1] in CAUSES_A_STATE:
        return _ends_a_state(after)
    wide = back
    while wide >= 0 and _measures_a_state(words[wide], wide=True):
        wide -= 1
    if wide < back and wide >= 0 and words[wide] in BE_BEFORE_A_STATE:
        return True
    if wide < back and wide < 0:
        return _opens_a_state(after)
    return False


CAUSES_A_STATE = frozenset("""got get gets getting gotten make makes made making left leave leaves
    leaving kept keep keeps keeping felt feels feel feeling found find finds find made became
    become becomes turned turns turn drove driven drive drives""".split())
OBJECT_PRONOUN = frozenset("""me us him her them you u u's myself yourself himself herself
    ourselves themselves""".split())

PHRASE_MEASURES = frozenset("""a an the bit little lot lots tad touch wee kind sort of out much
    many far way right that this these those enough half twice few some more most less least
    loads bunch ton tons hell heck mega extra damn damned fricking freaking""".split())


TIMES_A_STATE = frozenset("""yesterday last this week weekend morning mornings night nights
    evening evenings afternoon afternoons ago monday tuesday wednesday thursday friday saturday
    sunday january february march april june july august september october november december""".split())
AFTER_A_TIME = frozenset("""all after before until till during while once then later earlier
    afterwards""".split())


def _ends_a_state(after, opening=False):
    if after is None or after == "|" or after in AFTER_A_STATE:
        return True
    if opening:
        return False
    return (after in TIMES_A_STATE or after in AFTER_A_TIME
            or after in A_STATE_THEN_A_TIME)


def _opens_a_state(after):
    return _ends_a_state(after, opening=True) or after in NOT_A_THING


def _a_measure_spelt_wrong(word):
    if not (len(word) >= 6 and word.isalpha()):
        return False
    if any(_one_letter_apart(word, measure) for measure in AMOUNT_BEFORE_A_STATE):
        return True
    if word.endswith(("aly", "lye", "yl")):
        return True
    return len(word) >= 9 and word.endswith("ley")


def _measures_a_state(word, wide=False):
    if wide and word in PHRASE_MEASURES:
        return True
    return (word in AMOUNT_BEFORE_A_STATE or word in BARE_TO
            or (len(word) >= 5 and word.endswith("ly")) or _a_measure_spelt_wrong(word))


def _a_letter_typed_twice(word):
    if len(word) < 4 or word in lexicon.COMMON_NAMES:
        return None
    for place in range(len(word) - 1):
        if word[place] != word[place + 1]:
            continue
        shorter = word[:place] + word[place + 1:]
        if shorter in lexicon.FEELINGS:
            return shorter
    return None


INTRODUCING_A_PERSON = frozenset("""
    hi hello hey heya hiya hii hiii yo howdy greetings morning afternoon evening sup meet
""".split())
INTRODUCING_AFTER = frozenset("here from".split())


def _an_introduction(before, before_before, after, before_words=None, after_words=None):
    for word in (before_words or ()):
        if word in INTRODUCING_A_PERSON:
            return True
    if after in INTRODUCING_AFTER:
        return True
    if before == "is" and before_before in ("this", "that"):
        return True
    if after == "is" and before in (None, "|"):
        return True
    if after in ("and", "|") or (after or "").isdigit():
        for word in list(after_words or ())[:3]:
            if word.isdigit():
                return True
    return False


STATES_OF_A_PERSON = frozenset("""hungry thirsty starving famished peckish sleepy tired
    exhausted shattered knackered drained dizzy queasy nauseous bunged freezing frozen cold
    hot warm boiling sweaty bored lonely miserable""".split())


def _a_letter_wrong_in_a_state(word):
    if len(word) < 5 or word in LEXICON or word in lexicon.COMMON_NAMES:
        return None
    found = {state for state in STATES_OF_A_PERSON
             if state[:1] == word[:1] and _a_letter_apart(word, state)}
    if len(found) == 1:
        return found.pop()
    return None


def _a_letter_apart(word, other):
    if _one_letter_apart(word, other):
        return True
    if abs(len(word) - len(other)) != 1:
        return False
    short, long = (word, other) if len(word) < len(other) else (other, word)
    return any(short == long[:i] + long[i + 1:] for i in range(1, len(long)))


def _near_a_feeling(word, before=None, before_before=None, after=None, alone=False,
                    before_words=None, after_words=None):
    if not alone and not _where_a_state_stands(before, before_before, after, before_words):
        return None
    if len(word) < 4 or word in LEXICON or word in lexicon.NOT_A_FEELING:
        return None
    twice = _a_letter_typed_twice(word)
    if twice and not _an_introduction(before, before_before, after, before_words, after_words):
        return twice
    if len(word) == 4:
        if after is not None and after != "|":
            return None
        if word in lexicon.COMMON_NAMES:
            return None
    if word.endswith("cious") and word[:-5] + "xious" in lexicon.FEELINGS:
        return word[:-5] + "xious"
    if word.endswith("ctious") and word[:-6] + "xious" in lexicon.FEELINGS:
        return word[:-6] + "xious"

    found = sorted(feeling for feeling in lexicon.FEELINGS
                   if _one_letter_apart(word, feeling)
                   and (len(word) >= 5 or len(feeling) == len(word) + 1)
                   and not _a_consonant_left_out_of_an_ing_word(word, feeling))
    if len(found) == 1:
        return found.pop()
    if after in (None, "|") and _the_state_is_the_whole_frame(before, before_before,
                                                              before_words):
        return the_feeling_two_letters_are_gone_from(word)
    return None


def _a_consonant_left_out_of_an_ing_word(word, feeling):
    if not word.endswith("ing") or len(feeling) != len(word) + 1:
        return False
    i = 0
    while i < len(word) and word[i] == feeling[i]:
        i += 1
    return word[i:] == feeling[i + 1:] and feeling[i] not in VOWEL_SET


def _the_state_is_the_whole_frame(before, before_before, before_words=None):
    words = [word for word in (before_words if before_words is not None
                               else (before_before, before)) if word]
    back = len(words) - 1
    while back >= 0 and _measures_a_state(words[back]):
        back -= 1
    return back == 0


def the_feeling_two_letters_are_gone_from(word):
    if not isinstance(word, str):
        return None
    low = word.strip().lower()
    if len(low) < 6 or low in lexicon.COMMON_NAMES:
        return None
    found = sorted(feeling for feeling in lexicon.FEELINGS if _two_letters_out(low, feeling))
    return found[0] if len(found) == 1 else None


def _two_letters_out(word, feeling):
    if len(feeling) - len(word) not in (1, 2) or word[:1] != feeling[:1]:
        return False
    if _one_letter_apart(word, feeling):
        return False
    rest = iter(feeling)
    return all(letter in rest for letter in word)


def _feeling_without_its_ending(word):
    if len(word) < 3 or not word.isalpha():
        return None
    known = lexicon.FEELINGS | lexicon.A_STATE
    if word in known:
        return None
    for ending in ("ed", "d", "y", "s", "us", "e", "g", "ing", "l", "ty"):
        if word + ending in known:
            return word + ending
    return None


def reads_as_a_feeling(word):
    if not isinstance(word, str):
        return False
    low = word.strip().strip(".,!?;:'\"()").lower()
    if not low or not low.isalpha():
        return False
    if _feeling_without_its_ending(low) or _a_letter_wrong_in_a_state(low):
        return True
    if low in lexicon.SOUNDS_LIKE_A_FEELING:
        return True
    if any(word in lexicon.FEELINGS or word in lexicon.A_STATE
           or word in STATES_OF_A_PERSON
           for word in _token(low, [], alone=True)):
        return True
    if low + "d" in lexicon.FEELINGS | lexicon.A_STATE:
        return True
    if _a_vowel_left_out_of_a_state(low):
        return True
    return False


def _a_vowel_left_out_of_a_state(word):
    if not 3 <= len(word) < 5 or not word.isalpha():
        return None
    if word in LEXICON or word in lexicon.COMMON_NAMES:
        return None
    found = sorted(state for state in lexicon.FEELINGS | lexicon.A_STATE
                   if len(state) == len(word) + 1 and word in _one_vowel_less(state))
    return found[0] if len(found) == 1 else None


def _one_vowel_less(word):
    return {word[:at] + word[at + 1:] for at, letter in enumerate(word)
            if letter in VOWEL_SET and 0 < at < len(word) - 1}


def reads_as_a_sound(word):
    if not isinstance(word, str):
        return False
    low = word.strip().strip(".,!?;:'\"()").lower()
    if not low or not low.isalpha():
        return False
    from . import kinds
    return kinds.feeling_by_sound(low) is not None


def repaired_tokens(word):
    if not isinstance(word, str):
        return []
    low = word.strip().strip(".,!?;:'\"()").lower()
    if not low:
        return []
    return list(_token(low, [], alone=True))


def spelled(word):
    if not isinstance(word, str):
        return []
    low = word.strip().strip(".,!?;:'\"()").lower()
    if not low:
        return []
    for table in (lexicon.CHAT, lexicon.EXPAND, lexicon.US_SPELLINGS,
                  lexicon.MISSPELLINGS, lexicon.URGENT_MISSPELLINGS):
        if low in table:
            return table[low].split()
    return []


def _unsays_the_word(word, variant):
    if len(variant) >= len(word):
        return False
    ending = next((end for end in ("ing", "est", "ed", "er") if variant.endswith(end)), "")
    if not ending:
        return False
    stem = variant[:-len(ending)]
    if len(stem) < 2:
        return False
    doubled = stem + stem[-1]
    return word == doubled + ending


def _a_word_of_the_bots(word):
    if word in NO_SWAP_TO:
        return False
    return word in BASE or word in _words_the_bot_writes()


def fix_typo(word):
    if not word.isalpha():
        return None
    if word in BASE:
        return None
    if word in lexicon.TYPED_WORDS:
        return None
    if word in _words_the_bot_writes():
        return None
    if word in lexicon.NOT_A_FEELING:
        return None
    if word in lexicon.COMMON_NAMES:
        return None
    shunned = _shun_variant(word)
    if shunned:
        return shunned
    stopped = _stopped_th(word)
    if stopped:
        return stopped
    short = _short_double(word)
    if short:
        return short
    doubled_once = _doubled_letter_words(word)
    if len(word) == 3 and doubled_once:
        best = sorted(doubled_once, key=lambda w: COMMON_RANK.get(w, 10 ** 6))[0]
        if COMMON_RANK.get(best, 10 ** 6) < 2000:
            return best
    if len(word) < 4:
        return None
    a_thing = _a_thing_a_letter_short(word)
    if a_thing:
        return a_thing
    candidates = [w for w in _double_variants(word)
                  if _a_word_of_the_bots(w) and not _unsays_the_word(word, w)]
    candidates += doubled_once
    candidates += [w for w in _ie_variants(word) if _a_word_of_the_bots(w)]
    dropped = _dropped_g(word)
    if dropped:
        candidates.append(dropped)
    said_as_n = _an_ing_said_as_n(word)
    if said_as_n:
        candidates.append(said_as_n)
    candidates += [w for w in _dropped_letter(word) if _a_word_of_the_bots(w)]
    candidates += [w for w in _a_leading_h(word) if _a_word_of_the_bots(w)]
    candidates += [w for w in _extra_vowel(word) if _a_word_of_the_bots(w)]
    candidates += [w for w in _missing_vowel(word) if _a_word_of_the_bots(w)]
    candidates += [w for w in _a_said_for_an_ending(word)
                   if w in BASE or (w.endswith("s") and w in LEXICON)]
    candidates += [w for w in _swapped_pair(word) if _a_word_of_the_bots(w) or w in URGENT_WORDS]
    candidates += [w for w in _two_letters_the_wrong_way_round(word) if _a_word_of_the_bots(w)]
    flat_ed = _missing_e(word)
    if flat_ed:
        candidates.append(flat_ed)
    candidates += [w for w in _e_kept_before_ing(word) if w in LEXICON]
    left_out = _an_emergency_word_left_out(word)
    if left_out:
        candidates.append(left_out)
    def _a_silent_t_put_back(typed):
        for ending in ("en", "le"):
            if typed.endswith(ending) and len(typed) > len(ending) + 1:
                if typed[-len(ending) - 1] in VOWELS:
                    continue
                yield typed[:-len(ending)] + "t" + ending

    candidates += [w for w in _a_silent_t_put_back(word) if w in BASE or w in LEXICON]
    typed_is_a_word = word in BASE
    candidates += [w for w in _double_variants(word)
                   if w in BASE and not (typed_is_a_word and _unsays_the_word(word, w))]
    words = sorted(set(candidates), key=lambda w: COMMON_RANK.get(w, 10 ** 6))
    if not words:
        return None
    if len(words) == 1:
        return words[0]
    if COMMON_RANK.get(words[0], 10 ** 6) < 120 and COMMON_RANK.get(words[1], 10 ** 6) > 900:
        return words[0]
    return None


OPENERS = frozenset(lexicon.OPENERS.split())
WH_OPENERS = frozenset("what why when where who which whose how".split())


def _slip(word, opener):
    if word == opener or word[:1] != opener[:1] or abs(len(word) - len(opener)) != 1:
        return None
    short, long = (word, opener) if len(word) < len(opener) else (opener, word)
    i = 0
    while i < len(short) and short[i] == long[i]:
        i += 1
    if short[i:] != long[i + 1:]:
        return None
    return "missing" if short is word else "extra"


def fix_opener(word):
    if not word.isalpha() or len(word) < 2:
        return None
    doubled = len(word) > 2 and word[-1] == word[-2]
    short = len(word) == 2
    fits = []
    for opener in OPENERS:
        shape = _slip(word, opener)
        if not shape:
            continue
        if short and opener not in WH_OPENERS:
            continue
        if shape == "extra" and not doubled:
            continue
        fits.append((opener, shape))
    for test in (lambda opener: opener[-1] == word[-1],
                 lambda opener: doubled and opener[-1] == word[-2]):
        if len(fits) > 1:
            kept = [f for f in fits if test(f[0])]
            fits = kept if len(kept) == 1 else fits
        if len(fits) == 1:
            break
    return fits[0][0] if len(fits) == 1 else None


def _plain_word(word):
    return word in BASE or word in lexicon.CHAT or word in lexicon.MISSPELLINGS \
        or word in lexicon.EXPAND


def _repair_openers(clauses, fixes):
    for clause in clauses:
        for start in sorted({0, len(clause) - len(strip_leaders(clause))}):
            if start >= len(clause):
                continue
            word = clause[start]
            if _plain_word(word):
                continue
            fixed = fix_opener(word)
            if fixed:
                fixes.append((word, fixed))
                clause[start:start + 1] = _token(fixed, fixes)
                break
    return clauses


def _four_spells_for(word):
    if len(word) < 4 or not word.startswith("4") or not word[1:].isalpha():
        return None
    rest = word[1:]
    if rest[0] not in "aeioug":
        return None
    if rest in BASE or rest in lexicon.CHAT or rest in lexicon.MISSPELLINGS or rest in LEXICON:
        return "for" + rest
    return None


def _collapse(word):
    if not re.search(r"(.)\1\1", word):
        return None
    runs = list(re.finditer(r"(.)\1+", word))
    if len(runs) > 3:
        return None
    choices = [range(1, min(3, len(match.group(0))) + 1) for match in runs]
    for lengths in itertools.product(*choices):
        variant = word
        for match, length in reversed(list(zip(runs, lengths))):
            variant = variant[:match.start()] + match.group(1) * length + variant[match.end():]
        if variant != word and variant in LEXICON:
            return variant
    return None


def _apostrophe(word):
    if "'" not in word:
        return None
    base, _, rest = word.partition("'")
    if rest == "t" and word.endswith("n't"):
        stem = word[:-3]
        if stem == "ca":
            return ["can", "not"]
        if stem == "wo":
            return ["will", "not"]
        if stem == "sha":
            return ["shall", "not"]
        if stem == "ai":
            return ["is", "not"]
        return [stem, "not"] if stem else None
    if rest == "m":
        return [base, "am"]
    if rest == "re":
        return [base, "are"]
    if rest == "ve":
        return [base, "have"]
    if rest == "ll":
        return [base, "will"]
    if rest == "d":
        return [base, "would"] if base in PRONOUN_BASES else [base]
    if rest == "s":
        if base in PRONOUN_BASES:
            return [base, "is"]
        read = (lexicon.CHAT.get(base) or lexicon.MISSPELLINGS.get(base)
                or lexicon.URGENT_MISSPELLINGS.get(base) or "")
        if read and " " not in read:
            return [read, "is"]
        return [base]
    return None


DIGIT_WORDS = dict(zip("0123456789",
                       "zero one two three four five six seven eight nine".split()))
DIGIT_WORDS.update({str(n): w for n, w in zip(
    range(10, 21),
    "ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen "
    "twenty".split())})


BEFORE_WORD = frozenset("""the a an my your his her their our its this that these those
me you him us them it""".split())
BEFORE_VERB = frozenset("""go get do make see eat cook buy book call ask tell say try keep
put wear bring take watch read start stop pay save sleep work clean fix check learn study
write send order pick choose plan join find leave stay drink wash boil roast give show help
move sort turn cut fill set talk chat walk run live meet visit play listen wait come sit
stand hold pour chop stir fry bake serve mix add remove park drive catch post share print
sign email text speak change cancel return swap replace freeze heat store wrap pack load
grill steam reheat defrost tidy paint build grow plant have know""".split())
FOR_A = frozenset("""the a an my your his her their our its this that these those
me you him us them one two three""".split())
FOR_OBJECT = frozenset("""lunch dinner tea breakfast supper brunch now later tonight
tomorrow today free once example sure good real ages fun sale keeps christmas weekend
everyone everybody nothing starters afters dessert pudding coffee cake
milk bread butter cheese sugar flour rice pasta petrol diesel fuel wine beer juice""".split())
FOR_MEAL = frozenset("""lunch dinner tea breakfast supper brunch starters afters dessert
pudding cake""".split())
BE_VERBS = frozenset("am is are was were".split())
TOO_A = frozenset("""much many late early soon long often hard fast big small hot cold
tired busy expensive cheap old young loud noisy sweet salty spicy easy quick heavy light
slow warm dark bright strong weak soft loud""".split())
TOO_AFTER = frozenset("me you us him her them i we they it".split())
TO_AFTER = frozenset("up down over back out round through along".split())
A_NEGATION_BEFORE = frozenset("not".split())
TOO_A_GRADED = TOO_A | frozenset("""bad shabby keen happy far sure worried good pleased glad
    proud cross upset annoyed safe well fun useful handy honest bright""".split())
OPERATORS = frozenset("x * / + - plus minus times divided squared".split())
COUNTS = frozenset("a an per each".split())
COUNT_UNITS = frozenset("""year month week day hour minute second mile miles kilometre kilo
gram litre pint cup quid pound euro dollar pence percent point star item person people child
children man men woman women foot feet grand ton bob
yr yrs mth wks wk hr hrs min mins sec secs km cm mm kg g mg ml cl lb lbs oz ft yds yd
tsp tbsp
pack slice seat piece wheel toaster suite star speed door
january february march april may june july august september october november december
jan feb mar apr jun jul aug sep sept oct nov dec""".split())
COMPOUND_HEADS = frozenset("bed class bay birth seat".split())
COMPOUND_TAILS = frozenset("""house flat home room rooms car cars van cottage bungalow
door doors window windows drive suite garden""".split())
NOT_COUNTED_AFTER = frozenset("""and or but so in on at of to by as is was were for with from
about than per each every a an the my your his her their our its this that these those
more fewer less most other others another few out tomorrow today tonight now later soon twice please
am pm oclock o'clock o’clock""".split())


NOT_A_COMPOUND_HEAD = frozenset("""new old small big cheap little large lovely nice good bad
first second third last next own same whole different other another
i me you him her us them he she we they it""".split())
NOT_A_COMPOUND_TAIL = frozenset("""i we they he she it you me us them there thats that's
and or but so if when because though anyway""".split())


def _counts_a_compound(head, tail):
    if not head or not tail or head == "|" or tail == "|":
        return False
    if head.isdigit() or tail.isdigit():
        return False
    if head in NOT_COUNTED_AFTER or tail in NOT_COUNTED_AFTER:
        return False
    if head in NOT_A_COMPOUND_HEAD or tail in NOT_A_COMPOUND_TAIL:
        return False
    if head.endswith("ing") or tail.endswith("ing"):
        return False
    return True


A_LABEL_BEFORE = frozenset("""year years class classes grade grades form forms level levels stage
stages part parts section sections page pages question questions chapter chapters episode episodes
lesson lessons unit units term terms step steps""".split())


NUMBERS_BEFORE = frozenset("""take took takes taking ate eaten eat drink drank drinks
buy bought buys get got gets use used uses add added adds gave give gives
a an the my your his her their our another first last only just""".split())


def _counts_a_thing(word):
    if not word or word == "|":
        return True
    word = (word.split() or ["|"])[0]
    if word.isdigit() or word in COUNT_UNITS or word in NOT_COUNTED_AFTER:
        return True
    return len(word) > 2 and word.endswith("s") and not word.endswith(("ss", "us", "is"))


def _digit_word(token, before, after, after_after=None):
    if token not in ("2", "4"):
        return None
    if (after or "").lower() in ("yr", "yrs"):
        return "two" if token == "2" else "four"
    before = before or "|"
    spelled = lexicon.CHAT.get(before) or lexicon.EXPAND.get(before) or before
    spoken_before = (spelled.split() or ["|"])[-1]
    after = lexicon.CHAT.get(after, after) if after else "|"
    after = (after.split() or ["|"])[0]
    number = "two" if token == "2" else "four"
    if after in OPERATORS or before in OPERATORS:
        return number
    if after in COUNTS and (before in BEFORE_VERB or before in TOO_AFTER or before == "|"):
        tail = lexicon.CHAT.get(after_after, after_after) if after_after else "|"
        tail = (tail.split() or ["|"])[0]
        if tail in A_PERIOD_FOLLOWS or tail == "|":
            return number
        return "for"
    if spoken_before in A_LABEL_BEFORE and not after.isdigit():
        return number
    if token == "2" and before in MOTION_BEFORE and after not in A_PERIOD_FOLLOWS:
        return "to"
    if after in DEMONSTRATIVE:
        after_after = lexicon.CHAT.get(after_after, after_after) if after_after else "|"
        after_after = (after_after.split() or ["|"])[0]
        if after_after in A_PERIOD_FOLLOWS:
            return number
    if token == "2":
        if before in TO_AFTER and (after == "|" or after in UP_TO_TAGS):
            return "to"
        if after == "|":
            return "too" if before in TOO_AFTER else number
        if after in TOO_A:
            return "too"
        if after in BEFORE_WORD or after in BEFORE_VERB:
            return "to"
        if after in TOO_A_GRADED and spoken_before in A_NEGATION_BEFORE:
            return "too"
        return number
    if before in BE_VERBS:
        return number
    if after in FOR_A:
        return "for"
    if after in FOR_OBJECT and (before != "|" or after in FOR_MEAL):
        return "for"
    if after.isdigit() and not before.isdigit():
        return "for"
    if after_after is not None:
        head = after
        tail = lexicon.CHAT.get(after_after, after_after) if after_after else "|"
        tail = (tail.split() or ["|"])[0]
        if head in COMPOUND_HEADS and tail in COMPOUND_TAILS:
            return number
    if before in NUMBERS_BEFORE and not _counts_a_thing(after):
        return number
    if after_after is not None:
        tail = lexicon.CHAT.get(after_after, after_after) if after_after else "|"
        tail = (tail.split() or ["|"])[0]
        if _counts_a_compound(after, tail):
            return number
    if not _counts_a_thing(after):
        return "for"
    return number


REPEAT_ONCE = frozenset("""i you we they he she it me my the a an to and of in is am are
was were do does not at on for""".split())


REPEAT_ONCE_SUBJECTS = frozenset("i you we they he she it u".split())


def _once_only(tokens):
    out = []
    for token in tokens:
        if out and token == out[-1] and token in REPEAT_ONCE:
            continue
        out.append(token)
    return out


AUX_OPENS = frozenset("am is are was were have has had been".split())
DROPPED_SUBJECT_AUX = frozenset("am was have".split())
_SUBJECTS = frozenset("""i you we they he she it there that this these those one anyone someone
    everyone nobody nothing none who which what""".split())
_PREDICATE_ONLY = frozenset("""going gonna off out away back home up down well knackered
    shattered exhausted drained starving fine alright okay ok rubbish great late here""".split())
_A_STATE_OF_THE_PERSON = frozenset("""hungry thirsty starving famished peckish busy rushed
    freezing frozen broke skint brassic sleepy
    dizzy tired shattered knackered exhausted drained ill unwell poorly sick lousy rough
    down low fed up miserable sad happy chuffed pleased livid fuming cross annoyed upset gutted
    relieved worried anxious nervous scared frightened stressed""".split())
_SUBJECTLESS_AUX = frozenset("am was were".split())
_STATE_FILLER = frozenset("""both so really very totally absolutely properly too all quite still
    always just completely dead kind of a bit""".split())
_STATE_TAIL = frozenset("""at in on for after before by since till until from about with around
    over through during the a an this that these those my your his her their our
    last next today tonight tomorrow yesterday week weekend morning afternoon evening night
    month year day now then again still too also already anymore lately recently though but and
    so because when while if all every up out off sick stiff rotten
    to be been being had got go going""".split())
_SUBJECTLESS_ONLY = frozenset("am was".split())
_HAVE_NEGATIONS = frozenset("no none nothing".split())
_HAVE_PARTICIPLES = frozenset("got had been seen made taken spent".split())
_HAVE_THING = frozenset("a an the my our his her their your some this that".split())
_HAVE_ASKING = frozenset("minute moment sec second mo chance word".split())
_AFTER_PARTICIPLE = frozenset("""of to for in on at with about from by up out off over through
    into onto and but so or because if when while then that than as not never ever too also
    just""".split())


def opens_without_subject(words, index):
    if index >= len(words) or not words[index]:
        return False
    word = words[index]
    if word not in AUX_OPENS:
        return False
    rest = [w for w in words[index + 1:] if w != "|"]
    if not rest:
        return False
    second = rest[0]
    if second in _SUBJECTS:
        return False
    if word == "am":
        return True
    if second in _PREDICATE_ONLY:
        return True
    if word in _SUBJECTLESS_AUX:
        clause = []
        for word_after in words[index + 1:]:
            if word_after == "|":
                break
            clause.append(word_after)
        at = 0
        while at < len(clause) and clause[at] in _STATE_FILLER:
            at += 1
        if (at < len(clause) and clause[at] in _A_STATE_OF_THE_PERSON
                and (at + 1 == len(clause) or clause[at + 1] in _STATE_TAIL
                     or clause[at + 1] in _STATE_FILLER)):
            return True
    if second in _HAVE_NEGATIONS and word == "have":
        return True
    if word == "have" and second in _HAVE_PARTICIPLES and len(rest) > 2:
        return (rest[1] in _HAVE_THING and rest[2] not in _HAVE_ASKING
                and not any(w in TIME_WORDS for w in rest[1:]))
    if len(second) > 4 and (second.endswith("ing") or second.endswith("ed")):
        if len(rest) < 2:
            return True
        if word in _SUBJECTLESS_ONLY:
            return rest[1] in _AFTER_PARTICIPLE
        after = rest[2] if len(rest) > 2 else ""
        return rest[1] in _AFTER_PARTICIPLE and after.endswith(("ing", "ed"))
    return False


def _only_leaders_before(words, index):
    start = 0
    for i in range(index):
        if words[i] == "|":
            start = i + 1
    return all(word in LEADERS for word in words[start:index])


def _lookahead(words, index, n=3):
    out = []
    for word in words[index + 1:index + 1 + n]:
        if word == "|":
            break
        out.append(_token(word, [])[0] if _token(word, []) else word)
    return out


def subject_missing(words, index):
    return words[index] in DROPPED_SUBJECT_AUX and opens_without_subject(words, index)


def _opener_is(word):
    if len(word) < 4 or word[-1] not in "sz":
        return None
    stem = word[:-1]
    if stem in WH_OPENERS:
        return [stem, "is"]
    spelled = (lexicon.CHAT.get(stem) or lexicon.EXPAND.get(stem)
               or lexicon.MISSPELLINGS.get(stem) or "").split()
    if len(spelled) == 1 and spelled[0] in WH_OPENERS:
        return [spelled[0], "is"]
    return None


CAUSE_A_SUBJECT_FOLLOWS = frozenset("""i im ive id ill you youre youve we were weve they theyre
    theyve he hes she shes it its that thats this these those there theres my your our his her
    their if when whenever while since as so and but or not never no nobody nothing everyone
    everybody someone something anyone anything am is are was were do does did dont doesnt did
    didnt cant cannot couldnt wont wouldnt shouldnt isnt wasnt arent hasnt havent hadnt u ur ya""".split())
CAUSE_A_CLAUSE_VERB = frozenset("""is was were are am has had have will would can could did does
    do dont doesnt didnt wont cant cannot isnt wasnt arent hasnt hadnt""".split())
CAUSE_BEFORE_A_NOUN = frozenset("the a an this that my your our his her their any no every some "
                                "another one".split())
CAUSE_BEFORE_A_VERB = frozenset("to could would can may might must should will shall does did do "
                                "doesnt didnt dont wont cant cannot never not".split())
CAUSE_A_DEMONSTRATIVE = frozenset("this that these those".split())


def _cause_in_place_is_the_verb(before, after, after_words=None):
    if before in CAUSE_BEFORE_A_VERB:
        return True
    if before in CAUSE_BEFORE_A_NOUN:
        return True
    if after in CAUSE_A_DEMONSTRATIVE:
        rest = list(after_words or ())[1:2]
        return not rest or rest[0] not in CAUSE_A_SUBJECT_FOLLOWS
    if after in CAUSE_A_SUBJECT_FOLLOWS:
        return False
    if after is None:
        return False
    if after == "the" and any(word in CAUSE_A_CLAUSE_VERB
                              for word in (after_words or ())[1:4]):
        return False
    return True


def _token(word, fixes, before=None, before_before=None, after=None, alone=False,
           before_words=None, after_words=None):
    if word == "cause" and _cause_in_place_is_the_verb(before, after, after_words):
        return [word]
    if before is not None:
        thing = _a_thing_where_a_thing_goes(word, before)
        if thing:
            fixes.append((word, thing))
            return [thing]
    if word in DIGIT_WORDS:
        return [DIGIT_WORDS[word]]
    if word in lexicon.CHAT:
        return lexicon.CHAT[word].split()
    if word in lexicon.EXPAND:
        return lexicon.EXPAND[word].split()
    if word in lexicon.US_SPELLINGS:
        return [lexicon.US_SPELLINGS[word]]
    if word in lexicon.MISSPELLINGS:
        return lexicon.MISSPELLINGS[word].split()
    if word in lexicon.URGENT_MISSPELLINGS:
        fixes.append((word, lexicon.URGENT_MISSPELLINGS[word]))
        return [lexicon.URGENT_MISSPELLINGS[word]]
    if "'" in word:
        expanded = _apostrophe(word)
        if expanded:
            return expanded
    for_spelled = _four_spells_for(word)
    if for_spelled:
        fixes.append((word, for_spelled))
        return [for_spelled]
    collapsed = _collapse(word)
    if collapsed:
        fixes.append((word, collapsed))
        return [collapsed]
    if word in LEXICON or not word.isalpha() or len(word) < 2:
        return [word]
    opened = _opener_is(word)
    if opened:
        fixes.append((word, opened[0]))
        return opened
    pluraled = _z_for_s(word)
    if pluraled:
        fixes.append((word, pluraled))
        return [pluraled]
    ached = _ache_for_aike(word)
    if ached:
        fixes.append((word, ached))
        return [ached]
    corrected = fix_typo(word)
    if corrected:
        fixes.append((word, corrected))
        return [corrected]
    fronted = _said_with_an_f(word)
    if fronted:
        fixes.append((word, fronted))
        return [fronted]
    swapped_inside = _said_with_an_f_anywhere(word)
    if swapped_inside:
        fixes.append((word, swapped_inside))
        return [swapped_inside]
    feeling = _near_a_feeling(word, before, before_before, after, alone, before_words,
                              after_words)
    if feeling:
        fixes.append((word, feeling))
        return [feeling]
    return [word]


ONE_WORD_FOODS = (
    (re.compile(r"(?<![a-z])chick pea(?![a-z])"), "chickpea"),
    (re.compile(r"(?<![a-z])chick peas(?![a-z])"), "chickpeas"),
    (re.compile(r"(?<![a-z])sweet corn(?![a-z])"), "sweetcorn"),
)


def _one_word_food(clean):
    for pattern, one in ONE_WORD_FOODS:
        clean = pattern.sub(one, clean)
    return clean


JOINED_WORDS = re.compile(r"(?<![a-z])(?:%s)(?![a-z])"
                           % "|".join(sorted(lexicon.JOINED_WORDS, key=len, reverse=True)))


def _joined_words(clean):
    if not JOINED_WORDS.search(clean):
        return clean
    return JOINED_WORDS.sub(lambda m: lexicon.JOINED_WORDS[m.group(0)], clean)


def _z_for_s(word):
    if len(word) < 4 or not word.endswith("z"):
        return None
    if word in LEXICON or _a_word_the_bot_writes(word):
        return None
    fixed = word[:-1] + "s"
    return fixed if fixed in LEXICON or _a_word_the_bot_writes(fixed) else None


def _ache_for_aike(word):
    for tail in ("aike", "ayke", "eake"):
        if word.endswith(tail) and len(word) > len(tail):
            fixed = word[:-len(tail)] + "ache"
            if fixed in LEXICON:
                return fixed
    return None


SPLIT_CONTRACTION = re.compile(
    r"\b(i|u|you|he|she|it|we|they|that|there|what|who|where|when|how|this|these|those|let)"
    r"\s+(s|m|re|ve|ll|d)\b(?=\s|[.,!?;:)]|$)", re.IGNORECASE)
SPLIT_NOT = re.compile(r"\b([a-z]{2,}n)\s+t\b(?=\s|[.,!?;:)]|$)", re.IGNORECASE)
NOT_WORDS = frozenset("""dont doesnt didnt isnt wasnt arent werent havent hasnt hadnt cant couldnt
    shouldnt wouldnt wont mustnt neednt aint shant mightnt""".split())


def _a_contraction_typed_with_a_space(clean):
    if not SPLIT_CONTRACTION.search(clean) and not SPLIT_NOT.search(clean):
        return clean
    clean = SPLIT_CONTRACTION.sub(lambda m: m.group(1) + "'" + m.group(2), clean)

    def join_not(match):
        if match.group(1) + "t" not in NOT_WORDS:
            return match.group(0)
        return match.group(1) + "'t"

    return SPLIT_NOT.sub(join_not, clean)


UP_TOO_ASKS = re.compile(r"(\b(?:what|whats|watcha|whatcha|wotcha)\b[^.!?]{0,24}?\b)up too\b")

HEART_MEASURES = """so really very too pretty quite still just totally completely absolutely
    utterly properly well a bit a little kind of sort of that this""".split()
HEART_FEELINGS = (
    ("heartbroken", ("broken", "breaking", "shattered", "crushed", "torn", "broke", "snapped",
                     "in pieces", "in bits", "in two")),
    ("disappointed", ("sank", "sinking", "dropped")),
)
HEART_SAID_AS_A_FEELING = tuple(
    (re.compile(
        r"(?<![a-z0-9])(?:"
        r"(?:my|me)\s+heart(?:'s|s)?\s+(?:(?:is|was|feels|felt|looks)\s+)?(?:(?:%s)\s+)*"
        r"(?:%s)\b(?!\s+open)(?:\s+(?:in\s+(?:two|bits|pieces)|into\s+(?:a\s+million\s+)?pieces"
        r"|to\s+pieces))?"
        r"|(?:[a-z']+\s+)?(?:broke|breaks|breaking|broken)\s+(?:my|me)\s+heart"
        r")" % ("|".join(re.escape(word) for word in HEART_MEASURES),
                "|".join(re.escape(word) for word in states))),
     " i am " + feeling + " ")
    for feeling, states in HEART_FEELINGS)


SAID_AS_A_FEELING = (
    (re.compile(r"(?<![a-z0-9])broken[\s-]?hearted(?![a-z0-9])"), " heartbroken "),
    (re.compile(r"(?<![a-z0-9])broken[\s-]?heart(?![a-z0-9])"), " heartbroken "),
    (re.compile(r"(?<![a-z0-9])heart[\s-]?broken(?![a-z0-9])"), " heartbroken "),
    (re.compile(r"(?<![a-z0-9])(?:my|me)\s+(?:whole\s+)?(?:world|life)\s+"
                r"(?:fell|has\s+fallen|had\s+fallen|is\s+falling|came|came\s+crashing)\s+"
                r"(?:apart|down|crashing\s+down)(?![a-z0-9])"), " i am sad "),
    (re.compile(r"(?<![a-z0-9])(?:(?:my|me)\s+)?heart(?:'s|s)?\s+"
                r"(?:(?:is|was|feels|felt)\s+)?in\s+(?:my|me)\s+"
                r"(?:mouth|boots|throat|stomach|shoes)(?![a-z0-9])"), " i am nervous "),
    (re.compile(r"(?<![a-z0-9])(?:im|i\s+am|i\s+feel|i\s+felt|i\s+was)\s+"
                r"(?:so\s+|really\s+|totally\s+|completely\s+|utterly\s+|absolutely\s+)?"
                r"crushed(?![a-z0-9])(?!\s+by\b)"), " i am sad "),
)


SAID_IT = re.compile(
    r"\bwhat (?:was|is) it (?:that )?(?P<who>i|we) (?:said|told you|mentioned)\b"
    r"|\bwhat (?:was|is) it (?:that )?(?P<saying>i|we) (?:was|were|am|are) (?:saying|telling you)\b")


def _the_ask_said_plainer(text):
    return SAID_IT.sub(
        lambda one: (f"what did {one.group('who')} say" if one.group("who")
                     else f"what {'was' if one.group('saying') == 'i' else 'were'} "
                          f"{one.group('saying')} saying"), text)


_A_CLOSING_WORD = "|".join(sorted((re.escape(word) for word in ME_FOR_MY_CLOSES),
                                  key=len, reverse=True))
_A_HEAD_IN_THE_IDIOM = re.compile(r"(?<![a-z0-9])me head(?=\s+in(?![a-z0-9]))")
_A_CLIPPED_HEAD = re.compile(
    r"(?<![a-z0-9])(?:me|my) (?:ed|ead)(?!s?(?:[a-z0-9]))"
    r"(?=\s+(?:" + _A_CLOSING_WORD + r")(?![a-z0-9])|\s*$|\s*[,.;:!?])")


def _me_for_my_pass(text):
    text = _A_HEAD_IN_THE_IDIOM.sub(" my head", text)
    return _A_CLIPPED_HEAD.sub(" my head", text)

def _phrase_pass(text):
    text = _me_for_my_pass(text)
    for heart, feeling in HEART_SAID_AS_A_FEELING:
        if heart.search(text):
            text = heart.sub(feeling, text)
    for pattern, feeling in SAID_AS_A_FEELING:
        if pattern.search(text):
            text = pattern.sub(feeling, text)
    for phrase, value in PHRASES:
        pattern = r"(?<![a-z0-9])" + re.escape(phrase) + r"(?![a-z0-9])"
        if re.search(pattern, text):
            text = re.sub(pattern, " " + value + " ", text)
    text = UP_TOO_ASKS.sub(r"\1up to", text)
    text = _the_ask_said_plainer(text)
    return text


PUNCT_BREAK = re.compile(r"\s*[,;:!?]\s*")
SENTENCE_END = re.compile(r"(?<=[a-z0-9]{2})\.(?=\s|$)")
TOKEN = re.compile(_MEASURE + r"|\|")
THOUSANDS = re.compile(r"(\d),(?=\d\d\d\b)")
THOUSANDS_SAID_WITH_A_SPACE = re.compile(r"(?<!\d)(?<!\d{4} )(\d{1,3})((?:[ \u00a0]\d{3})+)(?!\d)")

CURRENCY_SIGNS = {"\u00a3": "quid", "$": "dollars", "\u20ac": "euros"}
CURRENCY_SIGN = re.compile(r"([\u00a3$\u20ac])\s*(\d+(?:[.,]\d+)*)\s*([km])?(?![\w])", re.I)
CURRENCY_FACTOR = {"k": 1000, "m": 1000000}


def _the_figure(figure):
    if "," in figure and "." in figure:
        decimal = "," if figure.rfind(",") > figure.rfind(".") else "."
        thousands = "." if decimal == "," else ","
        figure = figure.replace(thousands, "").replace(decimal, ".")
    elif "," in figure:
        figure = figure.replace(",", "") if len(figure.split(",")[-1]) == 3 else figure.replace(",", ".")
    value = float(figure)
    return ("%d" % value) if value == int(value) else ("%.2f" % value).rstrip("0")


def _a_sign_is_a_word(text):
    def spelled(match):
        sign, figure, scale = match.group(1), match.group(2), (match.group(3) or "").lower()
        value = float(_the_figure(figure).replace(",", ""))
        if scale:
            value = value * CURRENCY_FACTOR[scale]
        written = ("%d" % value) if value == int(value) else ("%.2f" % value)
        return written + " " + CURRENCY_SIGNS[sign]

    return CURRENCY_SIGN.sub(spelled, text)




NOT_A_THING = frozenset("""
a an the this that these those my your his her its our their some any no every each another
i you he she it we they me him us them who whom whose which what when where why how
is am are was were be been being do does did have has had can could will would shall should
may might must not so as than then too also either neither nor and or but if because
while whilst until till unless whether whenever wherever though although since whereas
in on at to for with from by about into over under after before between through during
up down out off away here there now later soon again still just only even ever never always
please thanks sorry ok okay
myself yourself himself herself itself ourselves yourselves themselves
thinks
""".split())

AFTER_A_THING = BE_WORDS | AUX_WORDS | REPORTING | frozenset(DIGIT_WORDS)

BEFORE_A_THING = frozenset("""
with for about of on in at from to over under into by off near round around behind
and but so then also plus because when if or though although since
wiv wid wif abt frm
""".split())

BEFORE_A_PREPOSITION = frozenset("""
with for about of on in at from to over under into by off near round around behind
wiv wid wif abt frm
""".split())
NOT_A_THING_ENDING = ("ed", "ing")
LONG_ENOUGH_TO_BE_A_VERB = {"ed": 5, "ing": 6}
ING_THINGS = frozenset("""
ceiling ceilings landing landings building buildings bedding wedding weddings pudding
puddings dressing dressings shopping evening evenings morning mornings washing parking
meeting meetings ceiling fencing railing railings
""".split())
DOING_NOT_THING = frozenset("""
shut went goes gone came come left leaves broke broken breaks keeps kept got get gives gave
said says say told tells tell makes made takes took put puts ran runs run fell falls sees saw
seen knew knows know thought thinks think found finds feel feels felt closes close opens open
stops stop starts start works work sits sit""".split())


def _is_doing_something(word):
    if word in DOING_NOT_THING:
        return True
    for ending in NOT_A_THING_ENDING:
        if word.endswith(ending) and len(word) >= LONG_ENOUGH_TO_BE_A_VERB[ending]:
            return word not in ING_THINGS
    return False


KIN = frozenset("""
mother mum mom mam mammy mummy father dad daddy son daughter sister brother wife husband
partner nan nana granny gran grandma grandad grandpa grandmother grandfather aunt auntie uncle
cousin niece nephew kid kids child children baby toddler boyfriend girlfriend fiance fiancee
""".split())

NOT_A_THING_AFTER = NOT_A_THING | frozenset("""
first last next once twice today tonight tomorrow yesterday afterwards afternoons personally
anyway anyhow anymore anymore later sooner honestly really actually probably maybe usually
normally mostly nearly almost quite rather fairly simply clearly obviously certainly
definitely absolutely totally completely entirely exactly precisely again yet ever still
both too either neither together alike forever
alone sometimes earlier meanwhile eventually awhile anyway
""".split())

TIME_WORDS = frozenset("""
monday tuesday wednesday thursday friday saturday sunday
january february march april may june july august september october november december
morning afternoon evening night tonight tomorrow today yesterday midday noon midnight
week weekend weekday month year hour minute
""".split())
PLACE_WORDS = frozenset("""
outside inside indoors outdoors upstairs downstairs home ahead nearby nowhere somewhere
anywhere everywhere
""".split())
NOT_A_THING_PAIR = frozenset(("part time", "full time", "half time", "day time",
                               "night time", "real time", "spare time", "free time",
                               "every time"))


OWNING_VERBS = frozenset("""
lost lose losing dropped drop broke broken break cut burnt burned burn forgot forget forgotten
left spilled spilt ripped tore torn smashed chipped scratched hurt banged stubbed twisted
strained scraped find finding wash washing washed ironed ironing doing doin
""".split())

ASKS_WHOSE = frozenset("where wheres what whats wher whers wer wers".split())


def possessive_me(tokens):
    out = []
    for index, token in enumerate(tokens):
        if token == "me" and index + 1 < len(tokens):
            thing = tokens[index + 1]
            after = tokens[index + 2] if index + 2 < len(tokens) else None
            before = tokens[index - 1] if index else None
            before_before = tokens[index - 2] if index >= 2 else None
            asks_whose = (before in ASKS_WHOSE
                          or (before in BE_WORDS and before_before in ASKS_WHOSE))
            owns_a_person = (thing in KIN
                             and (after is None or after in AFTER_A_THING
                                  or after in BEFORE_A_THING or after in TIME_WORDS
                                  or after in PLACE_WORDS))
            owns_the_thing = (after in AFTER_A_THING
                              or before in OWNING_VERBS
                              or owns_a_person
                              or (after in lexicon.PAIN_WORDS
                                  and (before is None or before in BEFORE_A_THING))
                              or (asks_whose and thing not in NOT_A_THING_AFTER
                                  and not thing.endswith(("ly", "ing", "ed")))
                              or ((before is None or before in BEFORE_A_THING)
                                  and thing not in NOT_A_THING_AFTER
                                  and not thing.endswith("ly")
                                  and not (before in BEFORE_A_PREPOSITION
                                           and _is_doing_something(thing))))
            how_or_when = (thing in TIME_WORDS or thing in PLACE_WORDS or after in TIME_WORDS
                           or f"{thing} {after}" in NOT_A_THING_PAIR)
            if (owns_the_thing and thing.isalpha() and len(thing) > 2
                    and thing not in NOT_A_THING and (owns_a_person or not how_or_when)):
                out.append("my")
                continue
        out.append(token)
    return out


SUN_WORDS = frozenset("""
bed beds cream creams lounger loungers tan tans burn burns burnt burned hat hats roof roofs
light lights shine shines shining shiny screen screens glasses lotion deck decks rise set
heat trap traps flower flowers dial lamp star stroke dried dry baked bathing baked
""".split())

OWNING_A_PERSON = frozenset("my our their your his her me".split())
SON_VERBS = AUX_WORDS | frozenset("""
got gotten gets get keeps keep kept went goes gone came comes coming said says saying told tells
telling feels feel felt seems seem seemed looks look looked needs need needed wants want wanted
hates hate hated loves love loved likes like liked hurts hurt hurting cuts cut broke broken breaks
started starts woke wakes woken sleeps slept eats ate eating drinks drank drinking walks walked
talks talked cries cried crying swims swam swim wont cant doesnt didnt isnt wasnt hasnt havent
couldnt wouldnt shouldnt
""".split())


def a_son_not_the_sun(tokens):
    out = []
    for index, token in enumerate(tokens):
        if (token in ("sun", "suns") and index
                and tokens[index - 1] in OWNING_A_PERSON):
            after = tokens[index + 1] if index + 1 < len(tokens) else None
            if after not in SUN_WORDS and after in SON_VERBS:
                out.append("son" if token == "sun" else "sons")
                continue
        out.append(token)
    return out


LOOSE_FOR_LOSE = {"loose": "lose", "looses": "loses", "loosing": "losing", "loosed": "lost"}
THE_LOSING = frozenset("""weight pounds lb lbs kilos kilo kg kgs stones stone inches inch
    centimetres centimeters cm""".split())
BEFORE_THE_LOSING = frozenset("""some a an any that the this bit little more few of
    couple coupleof stone
    # "sum" is "some" with the o left out, and it stands where "some" stands: "i gotta loose sum
    # weight b4 the weddin" was "Got it. Is there anything you'd like a hand with?" because the
    # word between "loose" and "weight" was not one the reader knew, while "i gotta lose some
    # weight before the wedding" gets the weight answer.
    sum""".split())


A_PART_THE_PAIN_IS_IN = frozenset("""chest stomach tummy throat ear ears tooth teeth jaw shoulder
    shoulders hip hips neck wrist ankle elbow heel knee knees ribs rib kidney kidneys groin
    armpit chests leg legs arm arms foot feet hand hands head""".split())
A_GLASS_OR_A_PAN = frozenset("""window windows windscreen windscreens glass door doors
    frame frames greenhouse glazing mirror mirrors skylight skylights leaded stained shutter
    shutters cupboard drawer drawers kitchen oven hob handle handles lid lids frying roasting
    saucepan nonstick teflon wok tray freezer freezers""".split())
A_PART_A_PERSON_OWNS = frozenset("""back side head belly gut upper lower middle shoulder
    tummy chest arm arms leg legs foot feet hand hands""".split())
A_PAIN_WORD = {"pan": "pain", "pane": "pain", "panes": "pains"}
A_KEEPING_A_THING = frozenset("""keep keeps kept store stored stores storing hang hangs hung
    put puts putting stick stuck stash stashed""".split())
THE_HEART_SAID_THE_OTHER_WAY = frozenset("""attack attacks racing pounding murmur murmer murmurs
    failure bypass flutter flutters palpitations transplant stent pacemaker cardiologist
    valve valves arrest disease angina ecg""".split())
A_CHOKE_SAID_THE_OTHER_WAY = frozenset("""think he she hes shes im i we they baby son daughter child
    kid kids boy girl man woman dad mum someone somebody anyone anyone food blue bit sweet grape
    nearly started being""".split())
A_THING_WORN = frozenset("""wedding funerals funeral party interview dress dressed suit suits
    shoes shoe coat coats jeans jacket jackets gym tonight outside today work smart casual
    layers boots hat""".split())
A_STATE_YOU_CAN_FEEL = frozenset("""sick ill tired low anxious depressed dizzy faint better
    worse fine ok okay good great awful terrible rough rubbish angry sad happy nervous scared
    worried guilty lonely numb hot cold shaky weepy tearful emotional strange odd funny like
    sickly unwell pleased proud relieved""".split())
A_COPULA = frozenset("""am is are was were be been get got gets getting really very quite so
    still bit too pretty rather always""".split())
BEFORE_A_JOB = frozenset(("my", "the", "this", "a"))
A_JOB = frozenset("""job jobs work role position post company school course flat house city
    country marriage""".split())
A_TIME_TO_LEAVE = frozenset("""in next on at by from after before tomorrow tonight soon then end
    month week year monday tuesday wednesday thursday friday saturday sunday january february
    march april may june july august september october november december""".split())


def _a_slip_that_is_a_word(tokens):
    lowered = [token.lower() for token in tokens]
    out = list(tokens)
    slips = {}
    for index, token in enumerate(lowered):
        right = None
        before = lowered[index - 1] if index else None
        after = lowered[index + 1] if index + 1 < len(lowered) else None
        after_that = lowered[index + 2] if index + 2 < len(lowered) else None
        if token in A_PAIN_WORD:
            kept = (before in DETERMINERS and index > 1
                    and lowered[index - 2] in A_KEEPING_A_THING)
            after_body = False
            if after == "in":
                for place in range(index + 2, min(len(lowered), index + 5)):
                    part = lowered[place]
                    if part in A_PART_THE_PAIN_IS_IN:
                        after_body = True
                        break
                    if (part in A_PART_A_PERSON_OWNS
                            and lowered[place - 1] in OWNING_A_PERSON):
                        after_body = True
                        break
            before_body = (before in A_PART_THE_PAIN_IS_IN
                           or (before in A_PART_A_PERSON_OWNS and index > 1
                               and lowered[index - 2] in OWNING_A_PERSON))
            feels = after in A_STATE_YOU_CAN_FEEL or after in A_COPULA or after in (
                "hurt", "hurts", "ache", "aches", "aching", "kill", "killing",
                "throb", "throbbing")
            pain_frame = (before_body and feels) or after_body
            if (not kept and not any(word in A_GLASS_OR_A_PAN for word in lowered)
                    and pain_frame):
                right = A_PAIN_WORD[token]
        elif token == "hart" and any(word in THE_HEART_SAID_THE_OTHER_WAY
                                     for word in lowered):
            right = "heart"
        elif (token in ("chocked", "chockes")
              and after not in DETERMINERS
              and any(word in A_CHOKE_SAID_THE_OTHER_WAY for word in lowered)):
            right = "choked" if token == "chocked" else "chokes"
        elif token in ("ware", "wared") and any(word in A_THING_WORN for word in lowered):
            right = "wear" if token == "ware" else "wore"
        elif token == "desert" and before == "for":
            right = "dessert"
        elif (token == "live" and after in BEFORE_A_JOB and after_that in A_JOB
              and (lowered[index + 3:index + 4] or [None])[0] in
              (A_TIME_TO_LEAVE | {None, "|"})):
            right = "leave"
        elif (token == "saw" and before in A_COPULA
              and any(part in A_PART_THE_PAIN_IS_IN for part in lowered)):
            right = "sore"
        elif token == "felling" and after in A_STATE_YOU_CAN_FEEL:
            right = "feeling"
        if right and right != token:
            out[index] = right
            slips[tokens[index]] = right
    return out, slips


def loose_is_lose(tokens):
    out = []
    for index, token in enumerate(tokens):
        fixed = LOOSE_FOR_LOSE.get(token)
        if fixed:
            for step in (1, 2, 3, 4):
                after = tokens[index + step] if index + step < len(tokens) else None
                if after is None:
                    break
                if after in THE_LOSING:
                    out.append(fixed)
                    break
                if after not in BEFORE_THE_LOSING and not after.isdigit():
                    break
            else:
                out.append(token)
                continue
            if out and out[-1] == fixed:
                continue
        out.append(token)
    return out


DIGIT_AS_WORD = {"2": "to", "4": "for"}
MOTION_BEFORE = frozenset("""go goes going went gone come comes coming came back off
    goin gona gonna""".split())
DEMONSTRATIVE = frozenset(("this", "that", "these", "those"))
A_PERIOD_FOLLOWS = frozenset("""time times week weeks weekend month months year years
    morning afternoon evening night term semester summer winter spring autumn day days
    hour hours minute minutes second seconds""".split())
A_WORD_CAN_FOLLOW = frozenset((
    "the", "a", "an", "my", "your", "his", "her", "our", "their",
    "you", "u", "ur", "it", "me", "us", "him", "them", "myself",
    "what", "how", "why", "where", "when", "who",
))

KNOW_SUBJECT = frozenset((
    "i", "u", "you", "we", "they", "he", "she", "anyone", "any1", "ne1",
    "someone", "some1", "everyone", "every1", "ppl", "people",
))
NOT_BEFORE_KNOW = frozenset((
    "not", "dont", "don't", "didnt", "didn't", "doesnt", "doesn't", "dnt",
    "havent", "haven't", "havnt", "aint", "ain't", "never",
))
A_VERB_CAN_FOLLOW = frozenset((
    "you", "u", "ur", "it", "me", "us", "him", "them", "i", "we", "he", "she",
    "they", "what", "how", "why", "were", "wer",
    "where", "when", "who", "that", "the", "a", "an", "my", "your", "his", "her",
    "our", "their", "something", "anything", "nothing",
    "yet", "if", "whether", "about", "for", "much", "many", "anyone", "anybody",
    "anymore", "either", "myself",
))


BE_FORMS = frozenset("am is are was were".split())
HAVE_FORMS = frozenset("have has had having".split())
MODAL_FORMS = frozenset("could would should must might may ought shall will can".split())


LEFT_OFF_CONTRACTION = {
    "were": ("we", "are"),
}
CONTRACTION_NEXT = BEFORE_VERB | frozenset("""
    be been being have had not never also just only still both already always definitely
    probably going off back home away
    having moving getting thinking trying staying doing seeing planning hoping
    let ring phone pop drop grab manage chase quit resign hire rent lock measure weigh need
    love like want miss mean mind aim assume bet guess hope wish promise remind stay sow weed
    mow dig sand tile grout seal glue screw drill hang level varnish log batch bottle
    """.split())


PLURAL_SUBJECTS = frozenset("i you we they".split())
THIRD_PERSON = frozenset("he she it".split())

PERSON_WORDS = frozenset("""
    i you he she we they it mum mums mom moms mother mother's fathers dad dads father sister
    sisters brother brothers son sons daughter daughters wife husband partner mates mate
    friend friends boss kid kids baby gran nans nan grandad grandma granny aunt uncle cousin
    neighbour neighbor neighbour's colleague doctor nurse teacher cat cats dog dogs puppy
    puppies kitten kittens rabbit rabbits hamster budgie bird birds horse horses fish
""".split())
PERSON_PREPS = frozenset("in at on to out back away off home there round around up down".split())
HOW_FOLLOWS = frozenset("""much many long far old often big deep quick soon fast come
    did do does can could would should is are was were about of to lot""".split())
BEEN_WORDS = frozenset("""sick ill unwell poorly bad awful great good alright quiet busy
    late away round back out down off twice""".split())
BEEN_SUBJECT = frozenset("""i you we they he she it that thats its hes shes this these those
    there which what who everything nothing something""".split())
THING_POSSESSIVES = frozenset("my our your his her their its".split())
IN_NOUNS = frozenset("""
cabin robin basin margin satin ruin twin grin coin pumpkin napkin muffin raisin resin
vitamin protein aspirin insulin cousin dolphin penguin violin mandolin origin virgin cabbage
""".split())
BIN_CONTAINERS = frozenset("""
kitchen compost food wheelie recycling waste rubbish trash dust garden nappy nappies sharps
bathroom pedal swing carrier paper
""".split())


def _the_thing_has_been(word):
    plain = _plain_chat(word) if word else ""
    if not plain:
        return False
    if plain in BEEN_WORDS or plain.endswith(("ing", "ed")):
        return True
    return plain != "in" and plain.endswith("in") and plain not in IN_NOUNS


def _is_person(word):
    if not word:
        return False
    bare = word.replace("'", "").replace("\u2019", "")
    if bare in PERSON_WORDS or bare.rstrip("s") in PERSON_WORDS:
        return True
    plain = _plain_chat(word)
    if plain in PERSON_WORDS:
        return True
    spelled = (lexicon.CHAT.get(word) or lexicon.EXPAND.get(word) or "").split()
    return bool(spelled) and spelled[0] in PERSON_WORDS


def _plain_chat(word):
    if not word:
        return ""
    spelled = lexicon.CHAT.get(word) or lexicon.EXPAND.get(word) or word
    return spelled.split()[0]


def _spells_a_helper(word):
    if not word or word == "|":
        return False
    spelled = (lexicon.CHAT.get(word) or lexicon.EXPAND.get(word) or word).split()
    if not spelled:
        return False
    last = spelled[-1]
    return (last in MODAL_FORMS or last in BE_FORMS or last in HAVE_FORMS
            or last in ("to", "not"))


def _is_be(word):
    if not word:
        return False
    if word in BE_FORMS:
        return True
    spelled = lexicon.CHAT.get(word) or lexicon.EXPAND.get(word)
    return bool(spelled) and spelled.split()[-1] in BE_FORMS


IRREGULAR_PARTICIPLES = frozenset("""
    been gone done had seen said made taken given told known written eaten drunk spoken broken
    chosen driven fallen flown forgotten got gotten hidden held kept left lost met paid put read
    run come become begun brought bought caught fought found heard meant sent shown slept spent
    stood taught thought understood won worn
""".split())


def _is_participle(word):
    if not word or word in ("|",) or word == "or":
        return False
    plain = _plain_chat(word)
    if plain.endswith("ed") or plain in IRREGULAR_PARTICIPLES:
        return True
    return False


KIN_SINGULAR = {
    "mums": "mum", "mams": "mam", "moms": "mom", "dads": "dad",
    "husbands": "husband", "wives": "wife", "partners": "partner",
    "nans": "nan", "grans": "gran", "grandmas": "grandma", "grandads": "grandad",
    "mothers": "mother", "fathers": "father",
    "boyfriends": "boyfriend", "girlfriends": "girlfriend",
}

KIN_HAS = frozenset("got had been gone".split())
KIN_IS = frozenset("""
    on in at off out away here back home due around
    pregnant engaged married divorced retired widowed ill sick poorly unwell upset fine ok okay
    worried tired late early better worse mad angry happy sad lonely dead alive well drunk hungover
    coming going staying moving working getting having being doing feeling expecting visiting
    arriving leaving starting recovering struggling coping waiting looking planning hoping trying
    applying retraining babysitting sitting standing living travelling traveling
    """.split())
KIN_FILLERS = frozenset("just still always now already recently never not really very so quite"
                        .split())
CAN_FOLLOW_A_VERB = frozenset("""
    a an the this that these those my his her their our your its
    in on at to from with about for of into onto over under up down out off back home
    away around round through across along behind past near
    me him her them us it you
    and but or so because when while if then than
    today tonight tomorrow now again soon later already still just always never ever not
    late early hard well badly properly slowly quickly together alone anymore
    fine ok okay alright better worse
""".split())


def _a_gerund_reads_as_a_verb(word, after_after):
    if not isinstance(word, str) or not word.endswith("ing") or len(word) < 5:
        return True
    if after_after in (None, "", "|"):
        return True
    return after_after in CAN_FOLLOW_A_VERB


def _kin_needs_a_helper(token, before, after, opens_the_clause, after_after=None):
    if not opens_the_clause or before != "my":
        return None
    if token not in KIN_SINGULAR:
        return None
    if after in KIN_HAS:
        return [KIN_SINGULAR[token], "has"]
    if after in KIN_IS or after == "not" or (after or "").isdigit():
        if after in KIN_IS and not _a_gerund_reads_as_a_verb(after, after_after):
            return None
        return [KIN_SINGULAR[token], "is"]
    if after in KIN_FILLERS and (after_after in KIN_IS or after_after in KIN_HAS
                                 or after_after == "not"):
        return [KIN_SINGULAR[token],
                "has" if after_after in KIN_HAS else "is"]
    return None


FAMILY_SHRT = {
    "mil": ("mother", "in", "law"), "fil": ("father", "in", "law"),
    "sil": ("sister", "in", "law"), "bil": ("brother", "in", "law"),
    "oh": ("other", "half"), "lo": ("little", "one"),
    "dd": ("daughter",), "ds": ("son",), "dh": ("husband",),
}
SHRT_THINGS = {
    "ds": frozenset("""broken broke charging charge charger battery screen console game games
        lite dead working works""".split()),
    "dd": frozenset("""bra cup size in january february march april may june july august
        september october november december""".split()),
}
POSSESSIVES = frozenset("my your his her our their ur me mums dads sons daughters".split())


def _family_short(token, before, after, after_after):
    if token not in FAMILY_SHRT or not _is_possessive(before):
        return None
    things = SHRT_THINGS.get(token)
    if things and (after in things or after_after in things):
        return None
    return list(FAMILY_SHRT[token])


PERIOD_COUNTS = frozenset("""week weeks month months year years hour hours minute minutes""".split())

CLIPPED_UNITS = {"yr": ("year", "years"), "hr": ("hour", "hours"),
                 "min": ("minute", "minutes"), "sec": ("second", "seconds")}
CLIPPED_THINGS = {"rad": ("radiator", "radiators"), "rads": ("radiator", "radiators")}
THING_AFTER = frozenset("""is are was were wont wont keeps keep needs need broke broken leaking leaky
    cold hot noisy warm blocked bleed bleeding clean cleaning fix fixed valve valves
    died dies dead stopped stopping working works faulty glitchy tinny quiet sounds sound
    cuts cutting muted mute drops dropped plug plugged cable battery""".split())
THING_JOIN = frozenset("and but so though although because when if then".split())
THING_PLACE_AFTER = frozenset("in on at".split())
THING_DETERMINER = frozenset("""a an the my our your his her their its both each every no any
    this these those""".split())
THING_PLACE_WORDS = frozenset("""a an the my our your his her their its this these those that""".split())
THING_SUBJECT = frozenset("""a an the my our your his her their its this these those both
    each every no any leaky leaking cold hot noisy warm blocked old spare""".split())
A_COUNT = frozenset("""one two three four five six seven eight nine ten eleven twelve
    thirteen fourteen fifteen sixteen seventeen eighteen nineteen twenty thirty forty fifty
    sixty ninety a an couple few several hundred thousand million""".split())


def _counts_a_period(word):
    return _plain_chat(word or "") in PERIOD_COUNTS


def _is_a_count(word):
    plain = _plain_chat(word or "")
    return plain.isdigit() or plain in A_COUNT


A_PARTS_OF_A_PERIOD = frozenset("""next last this every each per past coming previous
    whole""".split())


HR_IS_THE_DEPARTMENT_AFTER = frozenset("""department departments team teams policy policies
    advice manager managers meeting meetings issue issues people rep reps email emailed staff
    director directors""".split())


def _hr_is_the_department(after):
    return _plain_chat(after or "") in HR_IS_THE_DEPARTMENT_AFTER


def _says_one(word):
    plain = _plain_chat(word or "")
    return plain in ("1", "a", "an", "one") or plain in A_PARTS_OF_A_PERIOD


NOT_BEFORE_A_NOUN = frozenset("""a an the my your his her our their its this that these
    of in at on to for from with per and or so but then than ago later old olds off out up
    down back over about around by as if sleep nap rest wait left more less most least
    now today tonight tomorrow yesterday""".split())


def _is_a_thing_here(before, after, after_after=None):
    said_after = (after or "").lower().strip("|")
    if said_after in THING_AFTER:
        return True
    if said_after in THING_JOIN:
        return _plain_chat(before or "") in THING_SUBJECT
    if said_after in THING_PLACE_AFTER:
        if _plain_chat(before or "") not in THING_DETERMINER:
            return False
        return (after_after or "").lower().strip("|") in THING_PLACE_WORDS
    return not said_after and _plain_chat(before or "") in THING_SUBJECT


def _clipped_thing(token):
    one, many = CLIPPED_THINGS[token]
    return many if token.endswith("s") else one


def _is_before_a_noun(token, after):
    if token.endswith("s") or not after or after == "|":
        return False
    return _plain_chat(after) not in NOT_BEFORE_A_NOUN


def _is_said_of_a_person(word):
    if not word or word in ("|",) or word in PERSON_PREPS:
        return False
    plain = _plain_chat(word)
    if len(plain) > 3 and (plain.endswith("ing") or plain.endswith("ed")
                           or plain.endswith("in")):
        return True
    return plain in IRREGULAR_PARTICIPLES or plain in BEEN_WORDS


def _is_possessive(word):
    if not word:
        return False
    bare = word.replace("'", "").replace("\u2019", "")
    return bare in POSSESSIVES


A_FEELING_CAN_BE_FOLLOWED = frozenset("""at in on with about of today tonight now again lately
    atm tbh so as all time work home stiff shit""".split())


BEFORE_A_FEELING = frozenset("""so really very well still always constantly dead proper
    pretty totally completely""".split())


def _sounds_like_a_feeling(token, before, after, before_before=None):
    if before in BEFORE_A_FEELING:
        before = before_before
    if before not in FIRST_PERSON_BE or token not in lexicon.SOUNDS_LIKE_A_FEELING:
        return None
    if after and after not in A_FEELING_CAN_BE_FOLLOWED:
        return None
    return lexicon.SOUNDS_LIKE_A_FEELING[token]


AINT_FORMS = frozenset(("aint", "ain't", "aint'", "a'int", "ai'nt", "aint,"))
HAS_SUBJECT = THIRD_PERSON | frozenset("this that there everyone somebody someone nobody".split())
AINT_PLURAL = frozenset("you we they ye these those".split())
MISSING_E_AFTER = frozenset("ktvpsmfgxzcjq")
PAST_AS_PARTICIPLE = frozenset("""spoke broke woke drank wrote rang sang began swam took gave
    ate fell forgot stole drove rode wore chose froze ran came grew knew threw flew drew""".split())


HV_SUBJECTS = frozenset("i we you they u ye".split())
HV_HELPERS = MODAL_FORMS | frozenset("to do does did not".split())
FIRST_PERSON_BE = frozenset(("im", "i'm", "i’m", "am", "m"))
AMOUNT_BEFORE_A_STATE = frozenset("""just only still so really very pretty quite too not never
    always often all sometimes ever constantly honestly actually kinda rather super totally
    completely proper propper dead well awful bloody terribly""".split())

BE_BEFORE_A_STATE = frozenset("""im i'm i\u2019m m am i been being feel feels feeling feelin felt""".split())

THIRD_PERSON_BE = frozenset("""is are was were r re hes he's shes she's its it's theyre they're
    youre you're ure we're seems seem looks look""".split())
BARE_TO = frozenset(("to", "two", "2"))

DETERMINER_IN_FRONT = frozenset("""
a an the every each no another this these those some any
my your his her its our their
""".split())

POSSESSIVE_IN_FRONT = frozenset("my your his her its our their".split())
AFTER_A_STATE = frozenset("""about of at with by for from since because and but so that today
    tonight now lately again too enough when as than in on to not all these days these days""".split())

A_STATE_THEN_A_TIME = frozenset("""after before yesterday tomorrow already last earlier later
    soon still early late ever during while whenever yet until till whole every""".split())

_WERE_STATE = frozenset("""gutted shattered exhausted knackered tired worried stressed anxious
    frightened scared annoyed angry furious upset sad unhappy miserable depressed lonely bored
    happy glad pleased proud relieved grateful shattered wiped drained bushed sleepy sick ill
    unwell poorly broke skint done fine ok okay stuck sorted lost ready low""".split())
_WERE_ARE = frozenset("gonna gunna".split())
_WERE_DOING = frozenset("""thinking having going coming driving flying travelling traveling
    staying doing getting making taking working playing visiting eating cooking watching
    planning trying looking waiting hoping wondering moving camping hiking jogging running
    walking cycling swimming skiing sailing fishing gardening studying revising rehearsing
    baking painting decorating renovating unpacking babysitting feeling jogging""".split())
_AFTER_A_DOING = frozenset("""a an the my your our their his her its this that these those some
    any no every each another all both just still quite really very too so not up out off away
    back over down around together apart through in on at to with for from about into onto by of
    and or but because while when if i you we they he she it me us them him there here""".split())

_WERE_PLACE = frozenset("in at near up down out over round around on inside outside".split())
_WERE_IN_THE_PAST = frozenset("""last yesterday then earlier previously ago once before
    afterwards that those""".split())
_AFTER_A_LEAD_IN_SUBJECT = frozenset("""i you we they he she it them us him her me of""".split())
_WERE_LEAD_IN = frozenset("""so not too very really all both just still quite pretty always
    never literally definitely probably already almost nearly gonna gunna about""".split())
_A_QUESTION_VERB = frozenset("""is are was were am do does did can could would should will
    shall may might must has have had""".split())


def _were_for_another_word(before, after, after_after=None):
    if before not in (None, "|"):
        return None
    if after in (None, "|"):
        return None
    if after in _A_QUESTION_VERB:
        return ["where"]
    if after in _WERE_STATE or after in _WERE_DOING or after in _WERE_ARE:
        return ["we", "are"]
    if after in _WERE_LEAD_IN:
        if after_after in _WERE_STATE or after_after in _WERE_DOING:
            return ["we", "are"]
        if after_after is not None and _a_doing(after_after):
            return ["we", "are"]
        if after_after in _AFTER_A_LEAD_IN_SUBJECT:
            return ["were"]
        return None
    if _a_doing(after) and (after_after is None or after_after in _AFTER_A_DOING):
        return ["we", "are"]
    if after in _WERE_PLACE and after_after not in _WERE_IN_THE_PAST:
        return ["we", "are"]
    return None


def _a_doing(word):
    if not word:
        return False
    bare = word.replace("'", "")
    if bare.endswith("ing"):
        return bare in LEXICON or bare[:-3] in LEXICON
    if bare.endswith("in") and len(bare) >= 6:
        return bare in LEXICON or bare[:-2] in LEXICON
    return False


UP_TO_SPELLINGS = frozenset("wuu2 wu2 wyu2 wuut".split())
WHAT_ARE_YOU_SPELLINGS = frozenset("watcha whatcha wotcha watchu whatchu watchya whatchya".split())
WHAT_ARE_YOU_AFTER = frozenset("up doing doin do been".split())
LETTER_C_IS_SEE = frozenset("u ya you yeah yah".split())
UP_TO_LEADS = frozenset("""so ok okay oh ah and but well just hi hey hiya hello right then now
    anyway""".split())
UP_TO_TAGS = frozenset("""mate hun love pet duck sunshine hen flower chuck dear pal buddy friend
    guys folks all both then though now lol haha ha x xo xx""".split())
GLUED_LEFT = frozenset("is do does did can could would will should have are was were am "
                       "what whats where wheres when why how hows who whos".split())
GLUED_RIGHT = frozenset("it that this there they you i we he she your my "
                        "much long many the can should do does is are will would could did".split())
GLUED_COLLAPSE = {"itthere": ["there"]}
GLUED_DO = frozenset("do does did".split())
GLUED_AFTER_A_DO = frozenset("is are was were am will would can could should shall may might "
                             "must wont wouldnt cant couldnt shouldnt mustnt shant mightnt".split())


def _a_doubtful_split(pieces, after=None):
    if len(pieces) > 1 and pieces[0] == pieces[1]:
        return True
    return (pieces[0] in GLUED_DO and isinstance(after, str)
            and after in GLUED_AFTER_A_DO)


I_GLUED = frozenset("""dont cant wont didnt doesnt havent havnt couldnt shouldnt wouldnt isnt
    wasnt want feel need know think hope wish hate love miss just also really always never got
    went have had will would should could might must am was did saw live work been told said
    tried lost quit moved found bought sold left met heard broke failed cried slept woke rang
    asked felt started stopped changed forgot paid spent took gave kept began ran walked drove
    ate drank won hired retired dumped applied booked cancelled emailed phoned texted replied
    agreed signed decided hated loved missed needed wanted hoped knew thought""".split())
A_PRONOUN_GLUED = ("u", "i", "we", "you", "they", "he", "she")

A_PRONOUN_STATE = {
    "im": frozenset("""not so sorry still done going glad happy sad fine ok okay afraid worried
        tired starving hungry thirsty freezing boiling home back here sure just really trying
        working off out up sick lost confused angry upset lonely scared nervous bored at on in
        sitting lying waiting
        struggling stressed fed exhausted overwhelmed anxious depressed panicking hopeless
        worthless gutted furious annoyed irritated shattered unwell ill hurt aching shaky dizzy
        sleepless restless moody numb broke skint stuck busy late""".split()),
    "ive": frozenset("""given got been had never just tried lost done seen told said finished
        started stopped found made taken read heard watched eaten bought moved left paid spent
        decided noticed asked called checked waited worked lived known thought wanted needed
        felt learned kept written broken forgotten
        only already finally recently lately quit joined applied booked sent posted texted
        emailed ordered become grown gained""".split()),
}


_PLACES_SAID_WHOLE = [None]


def _a_place_said_whole(bare):
    if bare in lexicon.COMMON_NAMES:
        return True
    places = _PLACES_SAID_WHOLE[0]
    if places is None:
        try:
            from bot.knowledge.geography import COUNTRIES
            places = frozenset(COUNTRIES)
        except Exception:
            places = frozenset()
        _PLACES_SAID_WHOLE[0] = places
    return bare in places


def _a_pronoun_said_together(token):
    bare = token.replace("'", "").replace("\u2019", "")
    if _a_place_said_whole(bare):
        return None
    for who, after in A_PRONOUN_STATE.items():
        if bare.startswith(who) and bare[len(who):] in after:
            return [who, bare[len(who):]]
    for who in A_PRONOUN_GLUED:
        if bare.startswith(who) and len(bare) > len(who) and bare[len(who):] in I_GLUED:
            return [who, token[len(who):]
                    if token.startswith(who) else bare[len(who):]]
    return None


def _a_state_typed_onto_im(token):
    if len(token) < 4 or not token.startswith("im") or not token.islower():
        return None
    rest = token[2:]
    if rest in lexicon.STATES_SAID_ONTO_IM:
        return ["im", rest]
    return None


def _glued_words(token, after=None):
    if len(token) < 4 or token in LEXICON or not token.islower():
        return None
    said_together = _a_pronoun_said_together(token)
    if said_together:
        return said_together
    a_state = _a_state_typed_onto_im(token)
    if a_state:
        return a_state
    half, odd = divmod(len(token), 2)
    if not odd and token[:half] == token[half:]:
        return None
    for cut in (6, 5, 4, 3, 2):
        if token[:cut] not in GLUED_LEFT:
            continue
        rest = token[cut:]
        if rest in GLUED_RIGHT:
            pieces = [token[:cut], rest]
            return None if _a_doubtful_split(pieces, after) else pieces
        if rest in GLUED_COLLAPSE:
            return [token[:cut]] + GLUED_COLLAPSE[rest]
        for second in (5, 4, 3, 2):
            if rest[:second] in GLUED_RIGHT and rest[second:] in GLUED_RIGHT:
                pieces = [token[:cut], rest[:second], rest[second:]]
                return None if _a_doubtful_split(pieces, after) else pieces
    return None


MRS_IS_THE_WIFE = re.compile(r"\b(the|my|our|his|her)\s+([Mm]rs)\b\.?(?!\s+[A-Z])")


def _the_mrs_is_the_wife(text):
    return MRS_IS_THE_WIFE.sub(r"\1 wife", text)

_SUBJECT_SAID = frozenset(("i", "we", "you", "they", "he", "she", "it", "people", "folk",
                           "u", "ya", "yous", "everyone", "everybody", "somebody", "nobody"))


def _chat_words_said_out(clean):
    if not clean:
        return clean
    out = []
    for word in clean.split():
        spelled = SAID_OUT.get(word)
        before = SAID_OUT.get(out[-1].lower(), out[-1].lower()).split() if out else []
        if spelled and before and before[-1] in _SUBJECT_SAID and spelled.startswith(("i ", "I ")):
            spelled = spelled.split(" ", 1)[1]
        out.append(spelled or word)
    return " ".join(out)


HELLO_SAID_SHORT = (
    ("top of the morning", "good morning"),
    ("g morning", "good morning"),
    ("gmorning", "good morning"),
    ("g'morning", "good morning"),
    ("gm", "good morning"),
    ("gday", "good day"),
    ("g'day", "good day"),
    ("mornin'", "morning"),
    ("mornin", "morning"),
    ("evenin'", "evening"),
    ("evenin", "evening"),
)
HELLO_TAIL = frozenset("all everyone everybody guys folks friends there you mate to".split())


def _a_hello_said_short(clean):
    if not clean:
        return clean
    for typed, meant in HELLO_SAID_SHORT:
        if clean == typed:
            return meant
        if not (clean.startswith(typed + " ") or clean.startswith(typed + ",")
                or clean.startswith(typed + "!")):
            continue
        words = clean[len(typed):].strip(" ,!.").split()
        while words and words[0].strip(",.!") in HELLO_TAIL:
            words.pop(0)
        rest = " ".join(words).strip(" ,!.")
        return rest or meant
    return clean


def _glued_said_apart(clean):
    out = []
    words = clean.split()
    for index, token in enumerate(words):
        pieces = _glued_words(token, words[index + 1] if index + 1 < len(words) else None)
        if pieces:
            spread = lexicon.CHAT.get(pieces[0])
            if spread and " " in spread:
                pieces = spread.split() + pieces[1:]
        out.extend(pieces if pieces else [token])
    return " ".join(out)


RUN_ON_OPENERS = frozenset("what how why when where who which whats hows wheres whos "
                           "nothing nobody everything everyone something someone "
                           "can cant could couldnt should shouldnt would wouldnt will wont "
                           "do dont does doesnt did didnt is are was were shall".split())
RUN_ON_SELF = frozenset("i im ive id ill idk idunno cant dont didnt doesnt wont isnt arent".split())
RUN_ON_MINE = frozenset("my your his her our their".split())
RUN_ON_WORDS = LEXICON | frozenset("""a i im ive id ill idk idunno dunno cant dont didnt
    doesnt wont isnt arent wasnt werent wouldnt couldnt shouldnt""".split())
RUN_ON_PEOPLE = frozenset("""i im ive id ill me my we us our you your he him his she her it its
    they them their there this that these those nothing nobody everything everyone something
    someone anyone no one""".split())
RUN_ON_SELF_LONGEST = 9
RUN_ON_SHORTEST = 8
RUN_ON_LAST_PIECES = frozenset("ever ether soever".split())


def _said_run_on(token):
    if not token.isalpha():
        return None
    token = token.lower()
    if len(token) < RUN_ON_SHORTEST:
        return None
    if token in LEXICON:
        return None
    best = {0: ()}
    for start in range(len(token)):
        pieces = best.get(start)
        if pieces is None:
            continue
        for end in range(len(token), start, -1):
            piece = token[start:end]
            if piece not in RUN_ON_WORDS:
                continue
            here = pieces + (piece,)
            there = best.get(end)
            if there is None or len(here) < len(there):
                best[end] = here
    split = best.get(len(token))
    if not split or len(split) < 2:
        return None
    if split[-1] in RUN_ON_LAST_PIECES:
        return None
    if sum(1 for piece in split if len(piece) == 1) > 1:
        return None
    if split[0] in RUN_ON_SELF or split[0] in RUN_ON_MINE:
        if len(token) < RUN_ON_SELF_LONGEST or len(split) < 3:
            return None
        return list(split)
    if split[0] in RUN_ON_OPENERS:
        if not any(piece in RUN_ON_PEOPLE for piece in split):
            return None
        return list(split)
    return None


def _a_run_and_what_surrounds_it(token):
    start = 0
    while start < len(token) and not token[start].isalpha():
        start += 1
    end = len(token)
    while end > start and not token[end - 1].isalpha():
        end -= 1
    return token[:start], token[start:end], token[end:]


def _typed_without_spaces(clean):
    out = []
    for token in clean.split():
        before, letters, after = _a_run_and_what_surrounds_it(token)
        pieces = _said_run_on(letters)
        if pieces:
            spread = lexicon.CHAT.get(pieces[0])
            if spread and " " in spread:
                pieces = spread.split() + pieces[1:]
            out.extend(pieces)
            if after:
                out[-1] = out[-1] + after
            if before:
                out[0] = before + out[0]
        else:
            out.append(token)
    return " ".join(out)


APOSTROPHE_TAILS = frozenset("m re ve ll d s".split())
APOSTROPHE_BASES = frozenset("""i you we they he she it that there here what who where when
    why how let everyone everybody someone somebody nobody""".split())
APOSTROPHE_NOT = frozenset([("i", "s")])


def _the_said_apart_forms():
    forms = {}
    for joined in tuple(lexicon.EXPAND) + tuple(lexicon.TYPED_CONTRACTIONS):
        if not joined.isalpha() or not 2 <= len(joined) <= 10:
            continue
        for pieces in _the_ways_a_word_is_typed_apart(joined):
            forms.setdefault(pieces, joined)
    for base in APOSTROPHE_BASES:
        for tail in APOSTROPHE_TAILS:
            if (base, tail) in APOSTROPHE_NOT:
                continue
            one = base + "'" + tail
            if _apostrophe(one):
                forms.setdefault((base, tail), one)
    return forms


def _the_ways_a_word_is_typed_apart(joined):
    ways = []
    for cut in range(1, len(joined)):
        first, rest = joined[:cut], joined[cut:]
        if len(first) == 1 or len(rest) == 1:
            ways.append((first, rest))
    for first_cut in range(1, len(joined) - 1):
        for second_cut in range(first_cut + 1, len(joined)):
            pieces = (joined[:first_cut], joined[first_cut:second_cut], joined[second_cut:])
            if 1 in (len(piece) for piece in pieces):
                ways.append(pieces)
    return ways


SAID_APART_FORMS = _the_said_apart_forms()
SAID_APART = re.compile(
    r"(?<![a-z])(?:%s)(?![a-z])" % "|".join(
        r"\s+".join(pieces) for pieces in sorted(SAID_APART_FORMS,
                                                  key=lambda pieces: -sum(len(p) for p in pieces))))


A_LETTER_AFTER = frozenset("""my your his her their our the a an this that these those no any
    every each another some""".split())


def _said_apart(tokens):
    if len(tokens) < 2:
        return tokens
    said = " ".join(tokens)
    if not SAID_APART.search(said):
        return tokens

    def put_together(match):
        before = said[:match.start()].split()
        if before and before[-1] in A_LETTER_AFTER:
            return match.group(0)
        return SAID_APART_FORMS[tuple(match.group(0).split())]

    return SAID_APART.sub(put_together, said).split()


def said_apart(line):
    line = str(line or "")
    words = line.split()
    if len(words) < 2:
        return line
    return " ".join(_said_apart(words))


SOLFEGE = frozenset("do re mi fa sol la ti so".split())
MI_IS_ME_AFTER = frozenset("and n or nor & too either neither also".split())
MI_IS_ME_BEFORE = frozenset("""the a an this that these those later soon now again what how why
    when where if to in on at up out over please pls plz today tomorrow tonight then also
    though anyway know alone""".split())
MI_IS_A_NAME_AFTER = frozenset("the a an this that these those another".split())
MI_BACK_VERBS = frozenset("""text ring call phone send pass get give pay email message pm
    whatsapp reply write leave take bring hand poke shout""".split())


ILL_GOES_ON = frozenset("go take catch".split())


def _ill_is_i_will_going(token, before, after):
    if token != "ill" or after not in ILL_GOES_ON:
        return None
    if before is not None and before != "|" and before not in LEADERS:
        return None
    return ["i", "will"]


def _an_ill_that_is_i_will(clean):
    words = clean.split()
    changed = False
    for index, word in enumerate(words):
        if word != "ill" or index + 1 >= len(words):
            continue
        if words[index + 1] not in ILL_GOES_ON:
            continue
        before = words[index - 1] if index else None
        if before is not None and before != "|" and before not in LEADERS:
            continue
        words[index] = "i will"
        changed = True
    return " ".join(words) if changed else clean


def _left_off_contraction(token, before, after, before_before):
    words = LEFT_OFF_CONTRACTION.get(token)
    if not words or after not in CONTRACTION_NEXT:
        return None
    if before is not None and before != "|":
        leaders_only = before in LEADERS and (
            before_before in (None, "|") or before_before in LEADERS)
        if not leaders_only:
            return None
    return list(words)

ONE_OF_A_KIND = frozenset("""back head neck chest stomach tummy belly throat nose waist spine
    forehead tongue heart pelvis gullet""".split())
ONE_PART_AFTER = frozenset("""is was has been s keeps kept does did will would going playing
    killing hurting aching throbbing banging pounding killing""".split())


def _one_of_the_parts(token, before, after):
    if not token.endswith("s") or len(token) < 4 or token[:-1] not in ONE_OF_A_KIND:
        return None
    if not _is_possessive(before):
        return None
    if after in ONE_PART_AFTER or (after or "").endswith(("ing", "in")):
        return token[:-1]
    return None


VEGGIES_AFTER = frozenset("""roast roasted roasting grilled grilling steamed steaming fried frying
    stir braised baked charred sauteed saute boiled raw leftover leftovers fresh frozen chopped
    diced sliced seasonal mixed cook cooked cooking eat eating ate""".split())


WEARS_AFTER = frozenset("""i you u we they he she it people everyone somebody anybody
mum mums dad dads mam mother father sister brother son daughter wife husband nan gran
grandma grandad granparents mates kids children boy girl lad lass""".split())


def _wers_word(before):
    if before in (None, "|") or before in LEADERS:
        return ["where", "is"]
    if _plain_chat(before) in WEARS_AFTER or _is_person(before):
        return ["wears"]
    return ["where", "is"]


SUM_THE_NOUN = frozenset("""a an the my your his her our their its this that these those another
    each every no any do did does doing done work worked works add added adds total totals
    lump round large small tidy princely big hefty cash whole same missing""".split())


SUM_STAYS_AFTER = frozenset("up it things that this them total".split())


def _sum_word(before, after=None):
    spelled = _plain_chat(before) if before not in (None, "|") else ""
    if spelled in SUM_THE_NOUN:
        return ["sum"]
    behind = _plain_chat(after) if after not in (None, "|") else ""
    if behind in SUM_STAYS_AFTER:
        return ["sum"]
    if spelled in ("in", "to") and behind not in SUM_STAYS_AFTER:
        return ["sum"]
    return ["some"]


def _positional_word(token, before, after, after_after=None, before_before=None,
                     before_words=None):
    if (token in UP_TO_SPELLINGS
            and (before is None or before == "|" or before in UP_TO_LEADS)
            and (after is None or after == "|" or after in UP_TO_TAGS)
            and (after_after is None or after_after == "|")):
        return ["what", "you", "up", "to"]
    if token in WHAT_ARE_YOU_SPELLINGS and after in WHAT_ARE_YOU_AFTER:
        return ["what", "you"]
    if token == "w":
        return ["with"]
    if token == "c" and after in LETTER_C_IS_SEE:
        return ["see"]
    if token == "wers":
        return _wers_word(before)
    if token == "sum":
        return _sum_word(before, after)
    if token == "were":
        spelled = _were_for_another_word(before, after, after_after)
        if spelled:
            return spelled
    if token in CLIPPED_THINGS and _is_a_thing_here(before, after, after_after):
        return [_clipped_thing(token)]
    if token in CLIPPED_UNITS and (_is_a_count(before) or _says_one(before)):
        one, many = CLIPPED_UNITS[token]
        if token == "hr" and _hr_is_the_department(after):
            return [token]
        if _says_one(before) or _is_before_a_noun(token, after):
            return [one]
        return [many]
    contraction = _left_off_contraction(token, before, after, before_before)
    if contraction:
        return contraction
    going = _ill_is_i_will_going(token, before, after)
    if going:
        return going
    feeling = _sounds_like_a_feeling(token, before, after, before_before)
    if feeling:
        return [feeling]
    read = _digit_word(token, before, after, after_after)
    if read:
        return [read]
    if token == "wdyt" and after and after != "|":
        return ["what", "do", "you", "think"]

    one_part = _one_of_the_parts(token, before, after)
    if one_part:
        return [one_part]
    if token == "ow" and after in HOW_FOLLOWS:
        return ["how"]
    if token == "bout" and before not in DETERMINERS:
        return ["about"]
    if token == "no" and (before in KNOW_SUBJECT or before in NOT_BEFORE_KNOW):
        after_read = _plain_chat(after) if after and after != "|" else after
        if (after is None or after == "|" or after in A_VERB_CAN_FOLLOW
                or after_read in A_VERB_CAN_FOLLOW):
            return ["know"]
    if token == "hv":
        before_read = _plain_chat(before) if before else ""
        after_read = _plain_chat(after) if after else ""
        if before_read in DETERMINERS:
            return [token]
        if before_read in HV_SUBJECTS or before_read in HV_HELPERS or after_read == "to":
            return ["have"]
        if after_read in HV_SUBJECTS:
            return ["have"]
    if token == "bin":
        if before in HAVE_FORMS or (before or "").endswith("ve"):
            return ["been"]
        if _is_person(before) and (after in PERSON_PREPS or _is_participle(after)
                                   or _is_said_of_a_person(after)):
            return ["been"]
        if before_before in THING_POSSESSIVES \
                and (_plain_chat(before) if before else "") not in BIN_CONTAINERS \
                and _the_thing_has_been(after):
            return ["been"]
        if (before in BEEN_SUBJECT or before in BE_FORMS or before in (None, "|")) \
                and (_is_said_of_a_person(after) or (after or "").isdigit()
                     or _counts_a_period(after) or _counts_a_period(after_after)
                     or (before in BEEN_SUBJECT and after in ("a", "an"))):
            return ["been"]
    if token == "of" and _plain_chat(before) in MODAL_FORMS and _is_participle(after) \
            and before_before not in DETERMINERS:
        return ["have"]
    if token in AINT_FORMS:
        if _is_participle(after) or after in PAST_AS_PARTICIPLE:
            return ["has", "not"] if before in HAS_SUBJECT else ["have", "not"]
        if _plain_chat(before) == "i":
            return ["am", "not"]
        if _plain_chat(before) in AINT_PLURAL:
            return ["are", "not"]
        return ["is", "not"]
    if token == "of" and after == "to" and _is_be(before):
        return ["off"]
    if token == "b" and _spells_a_helper(before):
        return ["be"]
    if (after is None or after == "|") and _where_a_state_stands(
            before, before_before, after, before_words):
        state = _a_letter_wrong_in_a_state(token)
        if state:
            return [state]
    if before in FIRST_PERSON_BE or (before_before in FIRST_PERSON_BE
                                    and before in AMOUNT_BEFORE_A_STATE):

        feeling = _feeling_without_its_ending(token)
        if feeling:
            return [feeling]
    kin = _kin_needs_a_helper(token, before, after,
                              before_before is None or before_before == "|"
                              or before_before in LEADERS, after_after)
    if kin:
        return kin
    if token in ("yr", "yrs") and (before or "").isdigit():
        return ["years" if token.endswith("s") or after == "old" else "year"]
    family = _family_short(token, before, after, after_after)
    if family:
        return family
    if token == "veggies" and before in VEGGIES_AFTER:
        return ["vegetables"]
    if token in ("ur", "your") and after and after in YOU_ARE_AFTER:
        return ["you're"]
    if token == "mi" and after in MI_IS_ME_AFTER:
        return ["me"]
    if token == "mi" and before in MI_IS_A_NAME_AFTER:
        return [token]
    if token == "mi" and after in MI_IS_ME_BEFORE:
        return ["me"]
    if token == "mi" and after == "back" and before in MI_BACK_VERBS:
        return ["me"]
    if token == "mi" and (after is None or after == "|"):
        return ["me"]
    if token == "mi" and not (before in SOLFEGE
                              and (after is None or after == "|" or after in SOLFEGE)):
        if before is not None and before != "|" and before not in LEXICON:
            return [token]
        return ["my"]
    return [token]


YOU_ARE_AFTER = frozenset("""a an the such so too very really quite bloody proper
    going gonna joking kidding being not""".split())


def _join_chat_digits(tokens):
    joined = []
    index = 0
    while index < len(tokens):
        token = tokens[index]
        following = tokens[index + 1] if index + 1 < len(tokens) else None
        if (following is not None
                and (following[:1].isdigit() or token.isdigit())
                and (token + following in lexicon.CHAT
                     or token + following in lexicon.MISSPELLINGS)):
            joined.append(token + following)
            index += 2
            continue
        spelt = _said_apart_as_one(tokens, index)
        if spelt is not None:
            joined.append(spelt[0])
            index = spelt[1]
            continue
        joined.append(token)
        index += 1
    return joined


_SPACED_RUN = re.compile(r"(?<![\w'])([a-z0-9](?:[ \t]+[a-z0-9]){2,3})(?![\w'])", re.IGNORECASE)


def _said_apart_as_one_word(clean):
    if not _SPACED_RUN.search(clean):
        return clean

    def join(match):
        pieces = match.group(1).split()
        for length in range(len(pieces), 2, -1):
            word = "".join(pieces[:length]).lower()
            if word in lexicon.CHAT or word in lexicon.MISSPELLINGS:
                return " ".join([word] + pieces[length:])
        return match.group(0)

    return _SPACED_RUN.sub(join, clean)


_SPACED_PIECE = re.compile(r"^[a-z0-9]$")


def _said_apart_as_one(tokens, start):
    if not _SPACED_PIECE.match(tokens[start]):
        return None
    for length in (4, 3):
        pieces = tokens[start:start + length]
        if len(pieces) < length or not all(_SPACED_PIECE.match(piece) for piece in pieces):
            continue
        word = "".join(pieces)
        if word in lexicon.CHAT or word in lexicon.MISSPELLINGS:
            return word, start + length
    return None


DOCS_VISIT = frozenset("""go goes going gone went see sees seeing saw seen visit visits visiting
    ring rings ringing rang call calls calling called phone phones phoned ask asks asking asked
    book booked appointment appointments consult surgery gp""".split())
DOCS_PAPER = frozenset("""send sends sent email emails emailed print printed download downloaded
    upload uploaded scan scanned file files folder contract contracts paperwork invoice invoices
    lease leases tax read reading sign signed attach attached share forward forwarded page pages
    pdf copy copies draft document documents solicitor mortgage insurance check checked
    through""".split())
DOCS_SCREEN = frozenset("""tablet laptop pc screen online app apps link links browser website web
    google drive cloud portal intranet""".split())
DOCS_ON = frozenset(("on", "in", "via", "from", "as", "into"))


def _docs_on_a_screen(words):
    if any(word in DOCS_SCREEN for word in words):
        return True
    for index, word in enumerate(words):
        if word in ("phone", "tablet", "laptop", "pc", "screen", "file"):
            if any(back in DOCS_ON for back in words[max(0, index - 2):index]):
                return True
    return False


MEAL_WORDS = frozenset("""tea dinner supper lunch breakfast brunch snack food""".split())
FOOD_SLOT_LEAD = frozenset("""for at after before til till until round over about""".split())
NOT_A_MEAL_TYPO = frozenset(("tee",))
TIME_AFTER_MEAL = frozenset("time tonight tomorrow today now later".split())


def _near_a_meal(word, before, after=None):
    if not word or len(word) < 3 or word in LEXICON:
        return None
    if _plain_chat(before) not in FOOD_SLOT_LEAD:
        return None
    if after is not None and _plain_chat(after) not in TIME_AFTER_MEAL:
        return None
    if word in NOT_A_MEAL_TYPO:
        return None
    for meal in sorted(MEAL_WORDS):
        if len(word) >= 4 and meal.startswith(word):
            return meal
    found = sorted(meal for meal in MEAL_WORDS if _one_letter_apart(word, meal))
    return found[0] if len(found) == 1 else None


def _a_meal_word_misspelt(clean, words):
    places = {}
    for index, word in enumerate(words):
        if not index:
            continue
        after = words[index + 1] if index + 1 < len(words) else None
        meal = _near_a_meal(word, words[index - 1], after)
        if meal:
            places[index] = meal
    if not places:
        return clean, words
    pieces, last = [], 0
    for index, match in enumerate(RAW_WORD.finditer(clean)):
        pieces.append(clean[last:match.start()])
        pieces.append(places.get(index, match.group(0)))
        last = match.end()
    pieces.append(clean[last:])
    for index, meal in places.items():
        words[index] = meal
    return "".join(pieces), words


def _docs_doctor(clean, words):
    if not any(word in ("doc", "docs") for word in words):
        return clean, words
    if any(word in DOCS_PAPER for word in words):
        return clean, words
    if _docs_on_a_screen(words):
        return clean, words
    places = set()
    for index, word in enumerate(words):
        if word not in ("doc", "docs"):
            continue
        near = words[max(0, index - 4):index] + words[index + 1:index + 3]
        if any(other in DOCS_VISIT for other in near):
            places.add(index)
    if not places:
        return clean, words
    pieces, last = [], 0
    for index, match in enumerate(RAW_WORD.finditer(clean)):
        pieces.append(clean[last:match.start()])
        pieces.append("doctor" if index in places else match.group(0))
        last = match.end()
    pieces.append(clean[last:])
    for index in places:
        words[index] = "doctor"
    return "".join(pieces), words

ONE_RELATION = frozenset("""mum mom mam mummy mommy dad daddy nan nana gran granny grandad
    grandpa granddad grandma grandmother grandfather mother father husband wife""".split())
HAS_FORMS = frozenset(("got", "bin", "had"))
ONE_RELATION_VERBS = frozenset("""got bin wont cant said says told went came goes needs wants
    keeps lives works gets thinks loves hates""".split())


SORE_IN_FRONT = frozenset("""is are was were been feels feel felt gets get got still""".split())
SORE_FILLERS = frozenset("""so very really bit little too pretty quiet that""".split())
SORE_PARTS = frozenset("""throat back head neck shoulder shoulders knee leg legs foot feet arm
    arms toe toes hip ankle wrist elbow ear ears eye eyes tooth teeth gum mouth hand hands
    finger fingers belly stomach muscle muscles chest side sides rib ribs heel heels jaw skin
    tongue sunburn""".split())


def a_sor_bit_is_sore(tokens):
    out = []
    for index, token in enumerate(tokens):
        if token == "sor":
            before = tokens[index - 1] if index else None
            after = tokens[index + 1] if index + 1 < len(tokens) else None
            fills = (index > 1 and before in SORE_FILLERS
                     and tokens[index - 2] in SORE_IN_FRONT)
            if ((before is not None and (before in SORE_IN_FRONT or fills))
                    or (after is not None and after in SORE_PARTS)):
                out.append("sore")
                continue
        out.append(token)
    return out


def _one_relation_says(words):
    out = []
    for index, word in enumerate(words):
        after = words[index + 1] if index + 1 < len(words) else None
        if (index and after and word.endswith("s") and word[:-1] in ONE_RELATION
                and _is_possessive(words[index - 1])):
            read = _plain_chat(after)
            if read in ONE_RELATION_VERBS or read in HAVE_FORMS or read in BE_FORMS \
                    or read in MODAL_FORMS:
                out.append(word[:-1])
                if read in HAS_FORMS:
                    out.append("has")
                continue
        out.append(word)
    return out


def _ask_start(clause):
    if not clause or clause[0] in WH_WORDS or clause[0] in AUX_WORDS:
        return None
    for start in range(1, len(clause)):
        token = clause[start]
        following = clause[start + 1] if start + 1 < len(clause) else None
        after = clause[start + 2] if start + 2 < len(clause) else None
        if following is None:
            continue
        if token in WH_WORDS:
            if following in AUX_WORDS or _a_word_between_the_ask_and_its_aux(clause, start):
                if _reported(clause, start):
                    continue
                return start
            if following in HOW_DEGREE or (following in ASK_NOUNS and after in AUX_WORDS):
                if _reported(clause, start):
                    continue
                return start
        elif token in AUX_WORDS and following in SUBJECT_WORDS:
            if clause[start - 1] in NO_ASK_AFTER:
                continue
            if clause[start - 1] in SUBJECT_WORDS:
                continue
            if token in BE_WORDS:
                continue
            return start
    return None


WH_QUANTIFIERS = frozenset("""else other others kind sort type size colour color number
    make model brand version flavour flavor""".split())
NOT_IN_A_QUESTION_PHRASE = frozenset("""
    i me my mine we us our you your he him his she her it its they them their
    the a an this that these those some each every which what who whom whose
    to of for in on at by with from about as than if whether there here
    do does did is are was were am be been being have has had will would shall should can
    could may might must not no never""".split()) | WH_QUANTIFIERS
AFTER_AN_INVERTED_AUX = frozenset("""
    i we you he she they there it this that these those
    the a an my our your his her their some any""".split()) | SUBJECT_WORDS


def _a_word_between_the_ask_and_its_aux(clause, start):
    span = clause[start + 1:start + 6]
    for offset, word in enumerate(span):
        if word in AUX_WORDS:
            crossed = [w for w in span[:offset] if w not in WH_QUANTIFIERS
                       and w not in ("of", "for")]
            subject = clause[start + 2 + offset] if start + 2 + offset < len(clause) else None
            return (len(crossed) <= 2 and not (set(crossed) & NOT_IN_A_QUESTION_PHRASE)
                    and subject in AFTER_AN_INVERTED_AUX)
    return False


def _inverted_ask(clause, start):
    after = clause[start + 1:start + 3]
    return (len(after) > 1 and after[0] in RELATIVE_ASKS
            and after[1] in SUBJECT_WORDS)


def _reported(clause, start):
    before = clause[max(0, start - 2):start]
    if not before:
        return False
    if set(before) & REPORTING:
        return True
    if (clause[start] in RELATIVE
            and not _inverted_ask(clause, start)
            and before[-1] not in AUX_WORDS and before[-1] not in WH_WORDS
            and before[-1] not in REPORTING
            and (before[-1] in DETERMINERS or len(before) > 1
                 and (before[-2] in DETERMINERS or before[-2] in NOMINAL_BEFORE_COPULA))):
        return True
    return (before[-1] in COPULAS
            and (len(before) < 2 or before[-2] in NOMINAL_BEFORE_COPULA))


def _split_ask(clauses):
    out = []
    for clause in clauses:
        start = _ask_start(clause)
        if start is None or start >= len(clause) - 1:
            out.append(clause)
            continue
        out.append(clause[:start])
        out.append(clause[start:])
    return out


CLAUSE_OPENERS = frozenset("""i we you they he she it this that there anyone anybody someone
    everyone somebody nobody nothing""".split())


def _opens_clause(token):
    return (token in CLAUSE_OPENERS or token in SUBJECT_WORDS or token in WH_WORDS
            or token in BREAKS or token in LEADERS)


HAS_AFTER = frozenset("""got been had""".split())
HAS_SUBJECTS = frozenset("she he who".split())


def _says_has(words):
    for index in range(1, len(words) - 1):
        if words[index] != "is" or words[index - 1] not in HAS_SUBJECTS:
            continue
        after = words[index + 1]
        if after in HAS_AFTER or (after == "gone" and index + 2 < len(words)):
            words[index] = "has"
    return words


def _clauses(tokens):
    out, current = [], []
    for n, token in enumerate(tokens):
        if token == "|":
            if current:
                out.append(current)
                current = []
            continue
        following = tokens[n + 1] if n + 1 < len(tokens) else None
        if (token in BREAKS and len(current) >= 2 and following
                and _opens_clause(following)):
            out.append(current)
            current = []
            continue
        current.append(token)
    if current:
        out.append(current)
    return out


LEADERS = frozenset("""and so but also then ok okay oh well right now anyway anyways
hi hiya hey hello morning evening thanks thank thx cheers ty please just actually still
finally instead otherwise plus however meanwhile btw honestly anyway""".split())


LIKE_STARTS_A_CLAUSE = frozenset("""
i im ive id ill me my mine we were weve us our ours you youre youve your he hes she shes it its
they theyre theyve their them
what why how when where who which whose
can cant cannot could couldnt should shouldnt would wouldnt do dont doesnt did didnt
is are was were will wont have has had havent hasnt dont didnt get got gets need needs want
wants keep keeps just never not so too always still really gonna wanna dunno idk
u ur ya yall
""".split())


def _a_leading_like_is_a_filler(clean):
    head, _, rest = clean.partition(" ")
    if head.strip(",.!?") != "like" or not rest:
        return clean
    after = rest.split(" ", 1)[0].strip(",.!?")
    if after not in LIKE_STARTS_A_CLAUSE:
        return clean
    return rest


EXCLAIMED_AFTER_A_QUESTION = re.compile(
    r"\b(what|how|why|where|who|which|when|whatever|however|whoever|whenever)\s+"
    r"(?:on\s+earth|in\s+the\s+world|the\s+dickens|the\s+blazes|on\s+god'?s\s+earth)\b")


EXCLAMATION_OPENS = frozenset("""god honestly ugh jesus christ blimey crikey cor gosh omg
    jeez sheesh oh ah""".split())

EXCLAMATION_PHRASE = re.compile(
    r"^(?:oh\s+my\s+god|my\s+god|good\s+grief|for\s+goodness'?\s*sake|"
    r"for\s+god'?s?\s*sake)\s+")

_EXCLAMATION_SUBJECTS = frozenset("""i im ive id ill we weve youre you he hes she shes they
    theyre it its my me your our""".split())


def without_a_leading_exclamation(clean):
    return _an_exclamation_in_front(clean)


def _an_exclamation_in_front(clean):
    for _ in range(3):
        phrase = EXCLAMATION_PHRASE.match(clean)
        if phrase:
            rest = clean[phrase.end():]
            if rest and rest.split(" ", 1)[0].strip(",.!?;:-|") in _EXCLAMATION_SUBJECTS:
                clean = rest
                continue
            return clean
        head, _, rest = clean.partition(" ")
        if not rest or head.strip(",.!?;:-|") not in EXCLAMATION_OPENS:
            return clean
        after = rest.split(" ", 1)[0].strip(",.!?;:-|")
        if after in _EXCLAMATION_SUBJECTS or after in EXCLAMATION_OPENS:
            clean = rest
            continue
        return clean
    return clean


def _an_exclamation_is_not_a_thing(clean):
    return EXCLAIMED_AFTER_A_QUESTION.sub(r"\1", clean)


def strip_leaders(clause):
    start = 0
    while start < len(clause) - 1 and clause[start] in LEADERS:
        start += 1
    return clause[start:]

_LEADER_WORD = re.compile(r"^\s*([A-Za-z']+)\s*[,.;:!\-\u2014]*\s*")


def without_leaders(text):
    said = str(text or "")
    while True:
        match = _LEADER_WORD.match(said)
        if not match or match.group(1).lower() not in LEADERS:
            return said
        rest = said[match.end():]
        if not rest.strip():
            return said
        said = rest


_PLACE_STOP = frozenset("""last next this that yesterday today tomorrow tonight morning
    afternoon evening night week weekend month year hour minute monday tuesday wednesday
    thursday friday saturday sunday""".split())

_PLACE_LEADS = frozenset("""was were is am are been being s started starts began begins
    went go goes coming came got get stays stayed lived living working""".split())


_WH_QUESTIONS = frozenset("what why how when where who whose which".split())


def _clause_stop(norm, index):
    stop = index + 1
    while (stop < len(norm) and norm[stop] not in lexicon.CLAUSE_BREAKS
           and norm[stop] not in _WH_QUESTIONS):
        stop += 1
    return stop


def background_clause(norm):
    norm = list(norm)
    for index, word in enumerate(norm):
        if not index or word not in lexicon.BACKGROUND_STARTS:
            continue
        if norm[index - 1] in REPORTING:
            continue
        return set(range(index, _clause_stop(norm, index)))
    return set()


REASON_STARTS = frozenset("""because cause cos cus coz since""".split())


def reason_positions(norm):
    norm = list(norm)
    for index, word in enumerate(norm):
        if not index or word not in REASON_STARTS:
            continue
        return set(range(index, _clause_stop(norm, index)))
    return set()


def background_positions(norm):
    norm = list(norm)
    skip = set()
    spans = []
    if norm[:1] == ["it"] and len(norm) > 1 and norm[1] in lexicon.START_VERBS:
        spans.append((0, _clause_stop(norm, 1), True))
    clause = background_clause(norm)
    if clause:
        spans.append((min(clause), max(clause) + 1, False))
    for start, stop, anywhere in spans:
        index = start
        while index < stop:
            if norm[index] not in lexicon.PLACE_PREPS:
                index += 1
                continue
            if not anywhere and index and not (norm[index - 1] in _PLACE_LEADS
                                               or index - 1 in skip):
                index += 1
                continue
            index += 1
            taken = 0
            while (index < stop and taken < 3
                   and norm[index] not in lexicon.CLAUSE_BREAKS
                   and norm[index] not in _PLACE_STOP
                   and norm[index] not in lexicon.PLACE_PREPS):
                skip.add(index)
                index += 1
                taken += 1
    return skip




def _the_measure_clause(clause):
    stripped = strip_leaders(clause)
    return len(stripped) > 1 and stripped[0] == "how" and stripped[1] in HOW_DEGREE


def _asking(clauses, focus):
    if not focus:
        return []
    at = None
    for index, clause in enumerate(clauses):
        if clause is focus:
            at = index
            break
    if at is None:
        for index, clause in enumerate(clauses):
            if clause == focus:
                at = index
                break
    if at and _the_measure_clause(clauses[at - 1]):
        return list(clauses[at - 1]) + list(focus)
    return list(focus)


def _focus(clauses):
    for clause in reversed(clauses):
        stripped = strip_leaders(clause)
        if stripped and stripped[0] in ASK_WORDS:
            return clause
    for clause in reversed(clauses):
        if any(token in WANT_WORDS for token in clause):
            return clause
    for clause in reversed(clauses):
        stripped = strip_leaders(clause)
        if stripped:
            return clause
    return clauses[-1] if clauses else []


LETTERS = str.maketrans({
    "æ": "ae", "Æ": "AE", "œ": "oe", "Œ": "OE", "ø": "o", "Ø": "O", "ł": "l", "Ł": "L",
    "đ": "d", "Đ": "D", "ð": "d", "Ð": "D", "þ": "th", "Þ": "TH", "ß": "ss", "ı": "i",
})


def _unaccent(text):
    split = unicodedata.normalize("NFKD", text.translate(LETTERS))
    return "".join(char for char in split if not unicodedata.combining(char))


_INTENSIFIER = (r"on\s+earth|in\s+the\s+world|"
                r"the\s+(?:hell|heck|devil|blazes|dickens|fuck)")
WH_INTENSIFIER = re.compile(r"^\s*(?:" + _INTENSIFIER + r")\s*$")
WH_INTENSIFIER_LINE = re.compile(
    r"(?<![a-z'])\b(what|why|when|where|who|which|whose|how)\s+(?:" + _INTENSIFIER + r")\b",
    re.I)
WH_ANY = frozenset("what why when where who which whose how".split())


def intensifier_positions(norm):
    positions = set()
    for index, word in enumerate(norm):
        if word not in WH_ANY:
            continue
        for size in (3, 2):
            phrase = norm[index + 1:index + 1 + size]
            if len(phrase) == size and WH_INTENSIFIER.match(" ".join(phrase)):
                positions.update(range(index + 1, index + 1 + size))
                break
    return positions


_TYPED_SURPRISE = re.compile(
    r"(?<![a-z'])\b(?:what|why|when|where|who|which|whose|how|whatever|however|whoever|whenever)"
    r"\s+(?:" + _INTENSIFIER + r")", re.I)


def _the_surprise_typed(text):
    flat = re.sub(r"[^a-z']+", " ", text.lower().replace("\u2019", "'"))
    flat = re.sub(r"\b(?:wtf|wth|wtaf)\b", "what on earth", flat)
    words = []
    for match in _TYPED_SURPRISE.finditer(flat):
        for word in match.group(0).split()[1:]:
            word = word[:-2] if word.endswith("'s") else word
            if word not in words:
                words.append(word)
    return words


def _without_the_intensifier(norm):
    out = []
    index = 0
    while index < len(norm):
        word = norm[index]
        if word in WH_ANY and index + 1 < len(norm):
            phrases = intensifier_positions(norm)
            if index + 1 in phrases:
                end = index + 1
                while end < len(norm) and end in phrases:
                    end += 1
                out.append(word)
                index = end
                continue
        out.append(word)
        index += 1
    return out


_A_CLIP = {
    "mon": ("moon", frozenset("""moon moons full half crescent phase waxing waning eclipse
        lunar sky night tonight bright light lit shines shine rises rising stars""".split())),
}


def _a_clip_kept_only_with_its_cue(plain, norm, fixes, line):
    bent = dict(fixes)
    for typed, (longer, cues) in _A_CLIP.items():
        if bent.get(typed) != longer or any(word in cues for word in line):
            continue
        fixes = [pair for pair in fixes if pair[0] != typed]
        plain = [typed if word == longer else word for word in plain]
        norm = [typed if word == longer else word for word in norm]
    return plain, norm, fixes


def _fix_auxiliaries(tokens):
    if "been" not in tokens:
        return tokens
    out = []
    for index, word in enumerate(tokens):
        if word == "been" and out:
            last = out[-1]
            if last in BE_FORMS:
                out[-1] = "have" if (len(out) > 1 and out[-2] in PLURAL_SUBJECTS) else "has"
            elif last in PLURAL_SUBJECTS or last in THIRD_PERSON:
                before_it = out[-2] if len(out) > 1 else None
                if before_it not in HAVE_FORMS and before_it not in BE_FORMS \
                        and before_it not in MODAL_FORMS and before_it != "not":
                    out.append("have" if last in PLURAL_SUBJECTS else "has")
        out.append(word)
    return out


TAG_WORDS = frozenset("""x xx xxx xo xxo xoxo mwah kisses""".split())
TAG_PLEASE = frozenset("please pls plz pls.".split())
TAG_THANKS = frozenset("thanks thank cheers thx ty ta".split())
TAG_QUESTION_LEADS = frozenset("""what why how when where who which whose can could should
    would will is are do does did have has am was were may might shall""".split())
TAG_GUARD_BEFORE = frozenset("""a an the this that my your his her their our for of is are was
    were be been being with than to from called named call name letter mark spot sign cross tick
    size sized equals equal and or but not no""".split())


CHANGE_OF_SUBJECT = re.compile(
    r"^(?:(?:and|so|but|oh|ok|okay|right|now|anyway|anyways|also|plus|well)\s*,?\s*){0,3}"
    r"(?:"
    r"(?:changing|change\s+of|changing\s+the)\s+(?:the\s+)?(?:subject|topic|tack)"
    r"|(?:moving\s+on\s+to|on\s+to|onto|on|to)\s+(?:a\s+)?(?:new|different|another)\s+"
    r"(?:subject|topic|tack)"
    r"|(?:moving\s+on\s+to|on\s+to|onto)\s+something\s+else"
    r"|moving\s+on"
    r"|(?:a\s+)?(?:new|different|another)\s+(?:subject|topic|tack)"
    r")"
    r"\s*[,;:.\u2013\u2014-]+\s*(?=\S)")


def _change_of_subject_off(clean):
    seen = CHANGE_OF_SUBJECT.match(clean)
    if not seen:
        return clean, False
    rest = clean[seen.end():]
    if len(RAW_WORD.findall(rest)) < 2:
        return clean, False
    return rest, True


def _without_a_tag_at_the_end(clean):
    words = str(clean or "").split()
    asks = bool(words and words[0].strip(".,!?") in TAG_QUESTION_LEADS) or "?" in clean
    dropped = []
    while len(words) > 1 and words[-1].strip(".,!?") in TAG_WORDS:
        if words[-2].strip(".,!?") in TAG_GUARD_BEFORE:
            break
        dropped.insert(0, words.pop())
    while len(words) > 1 and words[-1].strip(".,!?") in TAG_PLEASE and asks:
        dropped.insert(0, words.pop())
    while len(words) > 1 and words[-1].strip(".,!?") in lexicon.LAUGHTER and asks:
        dropped.insert(0, words.pop())
    while len(words) > 3 and words[-1].strip(".,!?") in TAG_THANKS and asks:
        dropped.insert(0, words.pop())
    return " ".join(words), dropped


SPELLING_ASK = frozenset("spell spells spelling spelt spelled misspelt misspelled pronounce".split())


SPELLING_ENDINGS = ("ly", "ness", "ing", "ed", "es", "s", "d", "e")


def _spellings_of_one_word(one, other):
    if not one or not other:
        return False
    if one == other:
        return True
    short, longer = (one, other) if len(one) <= len(other) else (other, one)
    if len(short) < 4 or not longer.startswith(short):
        return False
    return longer[len(short):] in SPELLING_ENDINGS


NAMED_LETTER = re.compile(
    r"\b(?:with\s+(?:an?|one|two|three|double)\s+[a-z](?![a-z])"
    r"|(?:one|two|three|a\s+double)\s+[a-z](?![a-z])\s+or\s+(?:one|two|three|an?)\b"
    r"|double\s+[a-z](?![a-z])\b"
    r"|[a-z](?<![a-z])\s+or\s+(?:two|three)\b)")


def _names_a_letter_beside_a_slip(words, fixed):
    if not fixed:
        return False
    for at, word in enumerate(words):
        if word not in fixed:
            continue
        near = " ".join(words[max(0, at - 4):at + 5])
        if NAMED_LETTER.search(near):
            return True
    return False


_A_SHORT_WORD_IS_NAMED_BEFORE = frozenset((
    "letter", "letters", "word", "words", "vowel", "consonant", "initial", "alphabet", "grade",
    "grade", "type", "blood", "vitamin", "plan", "shape", "u", "the",
))
_A_SHORT_WORD_IS_NAMED_AFTER = frozenset((
    "turn", "turns", "turn-", "boat", "boats", "bend", "shaped", "shape", "tube", "value", "values",
))


def _a_short_word_named(short, before, after):
    if before in _A_SHORT_WORD_IS_NAMED_BEFORE or after in _A_SHORT_WORD_IS_NAMED_AFTER:
        return True
    return after is not None and after.endswith("'s") and short == "u"


def _asks_the_spelling(words, fixed):
    if not fixed:
        return False
    if any(word in SPELLING_ASK for word in words):
        return True
    if _names_a_letter_beside_a_slip(words, fixed):
        return True
    for at, word in enumerate(words):
        if word != "or":
            continue
        before = words[at - 1] if at else ""
        after = words[at + 1] if at + 1 < len(words) else ""
        if before in fixed and after in (fixed[before], before):
            return True
        if after in fixed and before in (fixed[after], after):
            return True
        if before in fixed and _spellings_of_one_word(fixed[before], after):
            return True
        if after in fixed and _spellings_of_one_word(fixed[after], before):
            return True
    return False


DAY_NAMED = re.compile(r"\b(birthday|anniversary|wedding)s?\b", re.I)
OWNER_WITHOUT_THE_DAY = re.compile(
    r"\b(?:it|its|it's|that|thats|that's)(?:\s+is)?\s+(?:not\s+)?(?:my|our)\s+([a-z]+'?s)\b",
    re.I)
TAIL_OF_A_DAY = frozenset("""
    tomorrow today tonight soon next this on in at already too as well then
""".split())


CAN_NOT = re.compile(r"\bcan\s+not\b")


def _can_not_as_one_word(clean):
    return CAN_NOT.sub("cant", clean)


def _the_day_left_out(text):
    named = DAY_NAMED.search(text)
    if not named:
        return text
    day = named.group(1).lower()
    pieces = []
    last = 0
    for found in OWNER_WITHOUT_THE_DAY.finditer(text):
        if found.start() < named.end():
            continue
        tail = re.split(r"[,.;:!?]", text[found.end():], 1)[0].split()
        if any(word.lower() not in TAIL_OF_A_DAY for word in tail):
            continue
        pieces.append(text[last:found.end()])
        pieces.append(" " + day)
        last = found.end()
    if not pieces:
        return text
    pieces.append(text[last:])
    return "".join(pieces)


A_NUMBER_OF_SOMEONES_DAY = re.compile(
    r"\b(?:my|our)\s+([a-z]+\'?s?)\s+(\d+(?:st|nd|rd|th))\b", re.I)
NOT_MY_OWN_DAY = re.compile(
    r"\s*(?:,?\s*\b(?:and\s+)?not\s+(?:my|mine)\s+"
    r"(birthday|bday|anniversary|wedding)\b)", re.I)


def _a_day_named_as_not_mine(text):
    negated = NOT_MY_OWN_DAY.search(text)
    if not negated:
        return text
    day = negated.group(1).lower()
    owner = None
    for found in A_NUMBER_OF_SOMEONES_DAY.finditer(text[:negated.start()]):
        if found.group(1).lower().rstrip("s") in KIN:
            owner = found
    if owner is None:
        return text
    whole = text[:owner.end()] + " " + day + text[owner.end():negated.start()] + text[negated.end():]
    return " ".join(whole.split())
_KEEPING_PLACES = frozenset((
    "fridge", "fridgefreezer", "refrigerator", "freezer", "cupboard", "larder", "pantry",
    "worktop", "counter", "countertop", "out", "outside", "coolbox", "coolbag", "bag"))
_KEPT_THINGS = frozenset((
    "leftover", "leftovers", "cooked", "uneaten", "spare", "rest", "remains", "opened"))
_DAY_WORDS = frozenset((
    "day", "days", "night", "nights", "week", "weeks", "month", "months"))
_KEPT_ALREADY = frozenset(("overnight", "yesterday", "since"))
_SMALL_NUMBERS = frozenset((
    "a", "an", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten",
    "couple", "few", "several", "many", "half"))
_NUMBER_SHAPE = re.compile(r"^\d{1,3}(?:st|nd|rd|th)?$")


def _a_number(word):
    return bool(_NUMBER_SHAPE.match(word)) or word in _SMALL_NUMBERS


def _kept_for(flat):
    if not flat:
        return None
    time = None
    at = None
    for index, word in enumerate(flat):
        if index + 1 < len(flat) and _a_number(word) and flat[index + 1] in _DAY_WORDS:
            time, at = "%s %s" % (word, flat[index + 1]), index
            break
        if word in _KEPT_ALREADY:
            after = flat[index + 1] if index + 1 < len(flat) else ""
            time = (word + " " + after).strip() if word == "since" and after else word
            at = index
            break
    if time is None:
        return None
    place = None
    for index, word in enumerate(flat):
        if word in _KEEPING_PLACES:
            place = word
            break
    if place is not None:
        if abs(at - index) <= 10:
            return {"place": place, "time": time}
        return None
    if _KEPT_THINGS.intersection(flat):
        return {"place": None, "time": time}
    return None


def _only_doubles_a_letter(typed, mended):
    if len(mended) != len(typed) + 1:
        return False
    return any(mended[at] == mended[at + 1] and mended[:at] + mended[at + 1:] == typed
               for at in range(len(mended) - 1))


def normalise(text):
    text = text if isinstance(text, str) else ""
    clean = _glued_said_apart(" ".join(_unaccent(text).split()))
    clean = _typed_without_spaces(clean)
    clean = _said_apart_as_one_word(clean)
    clean = _the_mrs_is_the_wife(clean)
    clean = " ".join(clean.lower().split())
    clean = _can_not_as_one_word(clean)
    clean = _the_day_left_out(clean)
    clean = _a_day_named_as_not_mine(clean)
    clean = THOUSANDS.sub(r"\1", clean)
    clean = THOUSANDS_SAID_WITH_A_SPACE.sub(
        lambda m: m.group(1) + m.group(2).replace(" ", "").replace("\u00a0", ""), clean)
    clean = _one_word_food(clean)
    clean = _a_leading_like_is_a_filler(clean)
    clean = _joined_words(clean)
    clean = _a_contraction_typed_with_a_space(clean)
    clean = _an_exclamation_in_front(clean)
    clean = _an_exclamation_is_not_a_thing(clean)
    clean = _a_hello_said_short(clean)
    clean = _chat_words_said_out(clean)
    clean = _an_ill_that_is_i_will(clean)
    clean, tags_at_the_end = _without_a_tag_at_the_end(clean)
    clean, change_of_subject = _change_of_subject_off(clean)
    clean, words = _a_meal_word_misspelt(clean, RAW_WORD.findall(clean))
    clean, words = _docs_doctor(clean, words)
    said = _a_sign_is_a_word(clean)
    words = RAW_WORD.findall(said)
    fixes = []
    norm = []
    plain = []
    fixed = {}
    subject_put_back = False
    sentence_ends = SENTENCE_END.sub(" | ", _phrase_pass(said))
    tokens = TOKEN.findall(PUNCT_BREAK.sub(" | ", sentence_ends))
    joined = _one_relation_says(
        a_son_not_the_sun(a_sor_bit_is_sore(
            loose_is_lose(possessive_me(_said_apart(_join_chat_digits(tokens)))))))
    joined, slips = _a_slip_that_is_a_word(joined)
    for typed, meant in slips.items():
        fixes.append((typed, meant))
        fixed[typed] = meant
    for index, word in enumerate(joined):
        before = joined[index - 1] if index else None
        after = joined[index + 1] if index + 1 < len(joined) else None

        if ((before is None or before == "|"
             or (before in LEADERS and _only_leaders_before(joined, index)))
                and word in DROPPED_SUBJECT_AUX
                and subject_missing([word] + _lookahead(joined, index), 0)):
            norm.extend(["i"] + _token(word, fixes, before))
            plain.append(word)
            subject_put_back = True
            continue
        after_after = joined[index + 2] if index + 2 < len(joined) else None
        before_before = joined[index - 2] if index >= 2 else None
        if _a_name_slot(before, before_before, word):
            norm.append(word)
            plain.append(word)
            continue
        before_words = joined[max(0, index - 5):index]
        after_words = joined[index + 1:index + 4]
        verb = _a_core_verb_typed_wrong(word, before, after)
        if verb:
            fixes.append((word, verb))
            fixed[word] = verb
        for spelled in ([verb] if verb else
                        _positional_word(word, before, after, after_after, before_before,
                                         before_words)):
            parts = _token(spelled, fixes, before, before_before, after,
                           before_words=before_words, after_words=after_words)
            if parts and norm and parts[0] == norm[-1] and parts[0] in REPEAT_ONCE:
                parts = parts[1:]
            elif (len(parts) > 1 and norm and parts[0] == "i"
                  and parts[1] == "do" and norm[-1] in REPEAT_ONCE_SUBJECTS):
                parts = parts[1:]
            if not parts:
                continue
            norm.extend(parts)
            if len(parts) > 1 and spelled in lexicon.PLAIN_EXPANDS:
                plain.append(" ".join(parts))
            elif (len(parts) == 1 and spelled not in DIGIT_WORDS
                    and spelled not in lexicon.US_SPELLINGS):
                plain.append(parts[0])
                if parts[0] != spelled and (spelled in lexicon.MISSPELLINGS
                                            or spelled in lexicon.URGENT_MISSPELLINGS
                                            or (spelled in lexicon.SAID_SHORT
                                                and not _a_short_word_named(spelled,
                                                                           before, after))):
                    fixed[spelled] = parts[0]
                elif spelled != word and word in lexicon.STATES_WITHOUT_G:
                    fixed[word] = spelled
                elif word == "bin" and parts[0] == "been":
                    fixed[word] = parts[0]
            else:
                plain.append(lexicon.TYPED_CONTRACTIONS.get(spelled, spelled))
    norm = _fix_auxiliaries(_says_has(norm))
    intensifier = _the_surprise_typed(text)
    intensifier_left = [norm[index] for index in sorted(intensifier_positions(norm))]
    if not intensifier:
        intensifier = list(intensifier_left)
    if intensifier_left:
        norm = _without_the_intensifier(norm)
    norm, words = _a_game_named_another_way(norm, words)
    norm = _parts_that_hurt(norm, fixes)
    if any(word in lexicon.PAIN_WORDS for word in norm):
        mended = dict(fixes)
        plain = [mended.get(word, word) for word in plain]
    plain, norm, fixes = _a_clip_kept_only_with_its_cue(plain, norm, fixes, joined)
    clauses = _split_ask(_repair_openers(_clauses(norm), fixes))
    flat = [word for clause in clauses for word in clause]
    focus = _focus(clauses)
    asking = _asking(clauses, focus)
    signals = {
        "question_mark": "?" in text,
        "shout": sum(1 for w in text.split() if len(w) > 2 and w.isupper()) > 0,
        "laughter": any(lexicon.is_a_laugh(w) for w in norm + tags_at_the_end)
                    or bool(re.search(r"\b(?:ha\s*){2,}|\b(?:heh\s*){2,}", text)),
        "ellipsis": "..." in text or ".." in text,
        "exclamation": "!" in text,
        "empty": not words,
    }
    keep = _asks_the_spelling(words, fixed)
    settled = dict(fixed)
    for typed, mended_word in fixes:
        if typed != mended_word and " " not in mended_word \
                and (typed in fixed or not _only_doubles_a_letter(typed, mended_word)):
            settled.setdefault(typed, mended_word)
    return {
        "text": text,
        "clean": clean,
        "words": list(words) if keep else [settled.get(word, word) for word in words],
        "plain": re.sub(r"\s*\|", ",", " ".join(plain)).strip(" ,"),
        "norm": flat,
        "norm_text": " | ".join(" ".join(clause) for clause in clauses) if clauses else "",
        "fixes": dict(fixes),
        "intensifier": intensifier,
        "intensifier_left": intensifier_left,
        "clauses": clauses,
        "focus": focus,
        "asking": asking,
        "signals": signals,
        "dropped_subject": subject_put_back,
        "change_of_subject": change_of_subject,
        "kept": _kept_for(flat),
    }


SICK_AS_FEELING = re.compile(
    r"\b(?:sick|ill|unwell|nauseous|nauseated|queasy|shaking|shaky|trembling|dizzy)"
    r"\s+(?:(?:with|from)\s+)?"
    r"(worry|worrying|worried|stress|stress(?:ed)?\s+out|fear|fright|frightened|panic\w*|"
    r"nerves|nervous|anxious|anxiety|guilt\w*|grief|shame|ashamed|dread\w*|anger|rage|"
    r"jealousy|it\s+all)\b",
    re.I)
_FEELING_WORD = {
    "worry": "worried", "worrying": "worried", "worried": "worried", "stress": "stressed",
    "stressed out": "stressed", "stressed": "stressed", "fear": "frightened",
    "fright": "frightened", "frightened": "frightened", "panic": "panicky",
    "panicking": "panicky", "panicky": "panicky", "nerve": "nervous", "nerves": "nervous",
    "nervous": "nervous", "anxious": "anxious", "anxiety": "anxious", "guilt": "guilty",
    "guilty": "guilty", "grief": "grieving", "shame": "ashamed", "ashamed": "ashamed",
    "dread": "dreading", "dreading": "dreading", "anger": "angry", "rage": "angry",
    "jealousy": "jealous", "it all": "overwhelmed",
}
FEELING_BEFORE_SICK = re.compile(
    r"\b(?:worried|scared|frightened|terrified|bored|stressed|anxious)\s+sick\b", re.I)


def _the_feeling_word(match):
    said = " ".join(match.group(1).lower().split())
    return _FEELING_WORD.get(said, "upset")


def without_the_figure_of_speech(clean):
    clean = FEELING_BEFORE_SICK.sub(lambda m: m.group(0).split()[0], str(clean or ""))
    return SICK_AS_FEELING.sub(_the_feeling_word, clean)


SUGAR_LEVEL = frozenset("""low high dropped drop drops dropping crashed crash crashes crashing
    dipped dip dips dipped levels level reading readings rises rose rising spike spiked spiking
    fell falls falling down up""".split())
SUGAR_AFTER_ROSE = frozenset("""to from after again overnight during before since sharply
    steadily quickly suddenly a bit so very high low all above around past 6 7 8 9""".split())
SUGAR_PRICE = frozenset("""price prices cost costs pound pounds lb lbs kilo kilos bag bags packet
    packets tin tins gram grams spoon spoons teaspoon teaspoons""".split())
SUGAR_PRICE_SHAPE = re.compile(r"^(?:[£$€]|\d+(?:\.\d+)?p(?:ence)?$)", re.I)
SUGAR_FIRST_PERSON = re.compile(
    r"\b(my|his|her|their|your)\s+sugar\b((?:\s+[a-z0-9'£$€]+){0,5})", re.I)


BAD_SAYING = (r"(?:an?\s+|such\s+an?\s+|one\s+big\s+"
              r"|an?\s+(?:complete|right|total|proper|real|absolute|utter|bit\s+of\s+a|bloody)\s+)?"
              r"(?:joke|nightmare|mess|disaster|wreck|state|shambles|agony|torture|car\s+crash|"
              r"pain\s+in\s+the\s+(?:arse|bum|butt|neck|back))")
BAD_WORD = (r"(?:terrible|awful|rubbish|crap|horrible|dreadful|brutal|shocking|knackered|shot|"
            r"agony|unbearable|wrecked|ruined|buggered|done\s+in)")
PART_THAT_IS_BAD = re.compile(
    r"\b(my|his|her|their|our|your)\s+("
    + "|".join(sorted(lexicon.BODY_PARTS, key=len, reverse=True))
    + r")\s+(?P<link>is|are|was|were|has\s+been|have\s+been|feels?|feels?\s+like)\s+(?:"
    + BAD_SAYING + "|" + BAD_WORD + r")\b", re.I)


THE_ODD_PLURALS = frozenset("feet teeth calves".split())


def _the_part_that_is_bad(match):
    part = match.group(2).lower()
    plural = part.endswith("s") or part in THE_ODD_PLURALS
    link = " ".join(str(match.group("link") or "").lower().split())
    if link in ("has been", "have been"):
        verb = "have been hurting" if plural else "has been hurting"
        return "%s %s %s" % (match.group(1), match.group(2), verb)
    verb = "hurt" if plural else "hurts"
    return "%s %s %s" % (match.group(1), match.group(2), verb)


def _the_part_that_hurts(clean):
    return PART_THAT_IS_BAD.sub(_the_part_that_is_bad, str(clean or ""))


def _the_sugar_that_is_blood(clean):
    def rewrite(match):
        tail = [word.strip(".,!?").lower() for word in match.group(2).split()]
        if any(SUGAR_PRICE_SHAPE.match(word) for word in tail):
            return match.group(0)
        if any(word[:1].isdigit() for word in tail):
            return "%s blood sugar%s" % (match.group(1), match.group(2))
        near = tail[:3]
        level = [word for word in near if word in SUGAR_LEVEL]
        if level == ["rose"]:
            following = tail[tail.index("rose") + 1:]
            if following and following[0] not in SUGAR_AFTER_ROSE \
                    and not following[0][:1].isdigit():
                level = []
        if level:
            for at, word in enumerate(tail):
                if word in SUGAR_LEVEL and SUGAR_PRICE & set(tail[at + 1:at + 4]):
                    return match.group(0)
            return "%s blood sugar%s" % (match.group(1), match.group(2))
        return match.group(0)
    return SUGAR_FIRST_PERSON.sub(rewrite, str(clean or ""))


def glued_words(token, after=None):
    return _glued_words(token, after)
