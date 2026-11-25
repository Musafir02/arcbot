import re
import unicodedata

WORD = re.compile(r"[a-z0-9]+(?:'[a-z]+)?")

STOPWORDS = frozenset("""
a an the and or but if then than so because as of at by for from in into on onto over
under to up with without about after before between during through out off down again
once here there when where why how what which who whom whose this that these those it
its is are was were be been being am do does did doing done can could should would will
shall may might must not no yes ok okay just also too very really quite more most i me
my mine we us our you your he him his she her they them their please pls thanks thank hi
hello hey take want wanna tell know need help always perhaps whereas sometimes
alas
""".split())

EXPAND = {
    "what's": ("what", "is"),
    "how's": ("how", "is"),
    "where's": ("where", "is"),
    "who's": ("who", "is"),
    "that's": ("that", "is"),
    "it's": ("it", "is"),
    "there's": ("there", "is"),
    "here's": ("here", "is"),
    "i'm": ("i", "am"),
    "i've": ("i", "have"),
    "i'll": ("i", "will"),
    "i'd": ("i", "would"),
    "you're": ("you", "are"),
    "you've": ("you", "have"),
    "you'll": ("you", "will"),
    "you'd": ("you", "would"),
    "he's": ("he", "is"),
    "she's": ("she", "is"),
    "we're": ("we", "are"),
    "we've": ("we", "have"),
    "we'll": ("we", "will"),
    "they're": ("they", "are"),
    "they've": ("they", "have"),
    "they'll": ("they", "will"),
    "don't": ("do", "not"),
    "doesn't": ("does", "not"),
    "didn't": ("did", "not"),
    "can't": ("can", "not"),
    "cannot": ("can", "not"),
    "won't": ("will", "not"),
    "wouldn't": ("would", "not"),
    "shouldn't": ("should", "not"),
    "couldn't": ("could", "not"),
    "isn't": ("is", "not"),
    "aren't": ("are", "not"),
    "wasn't": ("was", "not"),
    "weren't": ("were", "not"),
    "hasn't": ("has", "not"),
    "haven't": ("have", "not"),
    "hadn't": ("had", "not"),
    "let's": ("let", "us"),
    "gonna": ("going", "to"),
    "wanna": ("want", "to"),
    "gotta": ("got", "to"),
    "kinda": ("kind", "of"),
    "sorta": ("sort", "of"),
    "dunno": ("do", "not", "know"),
    "coz": ("because",),
    "cos": ("because",),
    "bc": ("because",),
    "pls": ("please",),
    "plz": ("please",),
    "thx": ("thanks",),
    "u": ("you",),
    "ur": ("your",),
    "r": ("are",),
    "ok": ("okay",),
}

US_UK = {
    "color": "colour",
    "colors": "colours",
    "colored": "coloured",
    "favorite": "favourite",
    "favorites": "favourites",
    "realize": "realise",
    "realized": "realised",
    "realizing": "realising",
    "organize": "organise",
    "organized": "organised",
    "organizing": "organising",
    "center": "centre",
    "centers": "centres",
    "liter": "litre",
    "liters": "litres",
    "meter": "metre",
    "meters": "metres",
    "tire": "tyre",
    "tires": "tyres",
    "apartment": "flat",
    "apartments": "flats",
    "vacation": "holiday",
    "vacations": "holidays",
    "cookie": "biscuit",
    "cookies": "biscuits",
    "fries": "chips",
    "eggplant": "aubergine",
    "cilantro": "coriander",
    "mom": "mum",
    "math": "maths",
    "gray": "grey",
}

IRREGULAR = {
    "children": "child",
    "feet": "foot",
    "teeth": "tooth",
    "mice": "mouse",
    "geese": "goose",
    "men": "man",
    "women": "woman",
    "people": "person",
    "knives": "knife",
    "loaves": "loaf",
    "shelves": "shelf",
    "wolves": "wolf",
    "halves": "half",
    "calves": "calf",
    "scarves": "scarf",
    "wives": "wife",
    "lives": "life",
    "selves": "self",
    "elves": "elf",
    "hooves": "hoof",
    "dwarves": "dwarf",
    "movies": "movie",
    "movie": "movie",
    "zombies": "zombie",
    "zombie": "zombie",
    "brownies": "brownie",
    "brownie": "brownie",
    "smoothies": "smoothie",
    "smoothie": "smoothie",
    "selfies": "selfie",
    "selfie": "selfie",
    "hoodies": "hoodie",
    "hoodie": "hoodie",
    "calories": "calorie",
    "calorie": "calorie",
    "series": "series",
    "species": "species",
    "shoes": "shoe",
    "shoe": "shoe",
    "canoes": "canoe",
    "canoe": "canoe",
    "toes": "toe",
    "toe": "toe",
    "foes": "foe",
    "foe": "foe",
    "veggies": "veggie",
    "veggie": "veggie",
    "newbies": "newbie",
    "newbie": "newbie",
    "freebies": "freebie",
    "freebie": "freebie",
    "aunties": "auntie",
    "auntie": "auntie",
    "rookies": "rookie",
    "rookie": "rookie",
    "sorties": "sortie",
    "sortie": "sortie",
    "prairies": "prairie",
    "prairie": "prairie",
    "analyses": "analysis",
    "diagnoses": "diagnosis",
    "theses": "thesis",
    "crises": "crisis",
    "parentheses": "parenthesis",
    "syntheses": "synthesis",
    "hypotheses": "hypothesis",
    "prostheses": "prosthesis",
    "oases": "oasis",
    "using": "use",
    "used": "use",
    "agreed": "agree",
    "freed": "free",
    "guaranteed": "guarantee",
    "refereed": "referee",
    "dying": "die",
    "lying": "lie",
    "tying": "tie",
    "eying": "eye",
    "icing": "ice",
    "aging": "age",
    "belied": "belie",
    "belies": "belie",
    "underlies": "underlie",
    "diabetes": "diabetes",
    "herpes": "herpes",
    "rabies": "rabies",
    "scabies": "scabies",
    "shingles": "shingles",
    "quiz": "quiz",
    "quizzes": "quiz",
    "quizzing": "quiz",
    "quizzed": "quiz",
    "panicking": "panic",
    "panicked": "panic",
    "picnicking": "picnic",
    "picnicked": "picnic",
    "trafficking": "traffic",
    "trafficked": "traffic",
    "mimicking": "mimic",
    "mimicked": "mimic",
    "frolicking": "frolic",
    "frolicked": "frolic",
    "politicking": "politic",
    "politicked": "politic",
    "budgies": "budgie",
    "genies": "genie",
    "foodies": "foodie",
    "sweeties": "sweetie",
    "hippies": "hippie",
    "yuppies": "yuppie",
    "groupies": "groupie",
    "walkies": "walkie",
    "cooties": "cootie",
    "hoagies": "hoagie",
    "bookies": "bookie",
    "preemies": "preemie",
    "made": "make",
    "taken": "take",
    "took": "take",
    "given": "give",
    "gave": "give",
    "written": "write",
    "wrote": "write",
    "eaten": "eat",
    "ate": "eat",
    "broken": "break",
    "broke": "break",
    "chosen": "choose",
    "chose": "choose",
    "frozen": "freeze",
    "froze": "freeze",
    "hidden": "hide",
    "fallen": "fall",
    "known": "know",
    "knew": "know",
    "grown": "grow",
    "grew": "grow",
    "thrown": "throw",
    "threw": "throw",
    "drawn": "draw",
    "drew": "draw",
    "seen": "see",
    "paid": "pay",
    "said": "say",
    "sold": "sell",
    "told": "tell",
    "bought": "buy",
    "brought": "bring",
    "thought": "think",
    "taught": "teach",
    "caught": "catch",
    "found": "find",
    "held": "hold",
    "kept": "keep",
    "lost": "lose",
    "sent": "send",
    "spent": "spend",
    "built": "build",
    "felt": "feel",
    "slept": "sleep",
    "fed": "feed",
    "heard": "hear",
    "won": "win",
    "ran": "run",
    "sat": "sit",
    "got": "get",
    "came": "come",
    "became": "become",
    "had": "have",
    "gassing": "gas",
    "gassed": "gas",
    "gasses": "gas",
    "bussing": "bus",
    "bussed": "bus",
    "busses": "bus",
    "focussing": "focus",
    "focussed": "focus",
    "focusses": "focus",
    "biassing": "bias",
    "biassed": "bias",
    "biasses": "bias",
}

S_BASES = frozenset("""
bus gas lens plus bonus campus virus status focus cactus octopus analysis basis
crisis thesis axis canvas atlas alias bias christmas xmas chaos cosmos pathos
ethos thermos asbestos rhinoceros news measles mumps
""".split())

E_BASES = frozenset("""
creat decid divid provid includ collid coincid subsid improv remov becom welcom
handl measur prepar compar requir shar car stor scor ignor explor restor smil
fil pil rul typ escap phon imagin combin defin leav believ receiv achiev arriv
surviv forgiv argu valu continu rescu pursu issu queu glu updat grad shad trad
persuad evad invad blockad upgrad downgrad calculat estimat donat negotiat
communicat participat concentrat motivat activat relocat celebrat decorat
educat generat operat separat demonstrat illustrat indicat associat appreciat
appropriat approximat articulat coordinat comput disput distribut contribut
attribut substitut constitut institut execut pollut abus accus amus confus
diffus excus fus mus refus reclus suffus transfus misus complet compet delet
concret unit ignit invit cit recit excit incit quot vot not dat rat hat stat
ach cach nich clich ganach crech brioch tranch cloch douch moustach mustach
backach heartach bellyach toothach earach stomachach headach avalanch quich
pastich psych
""".split())

G_NO_E = frozenset("""
sing ring bring spring swing hang sting cling fling sling wring string wing
bang ping ding zing long belong wrong throng
""".split())

L_BASES = frozenset("""
travel cancel label model signal total level control patrol compel expel
propel rebel excel fulfil enrol distil instil channel tunnel fuel jewel kennel
shovel snorkel dial initial final refuel unravel marvel counsel shrivel panel
towel yodel
""".split())

VOWELS = frozenset("aeiou")
CANON_CACHE = {}
PLAIN_SPLIT = re.compile(r"[^a-z0-9']+")


def _ascii(text):
    text = str(text or "")
    if text.isascii() and "&" not in text:
        return " ".join(text.lower().split())
    text = text.replace("\u2019", "'").replace("\u2018", "'").replace("\u02bc", "'")
    text = text.replace("\u201c", '"').replace("\u201d", '"')
    text = text.replace("&", " and ")
    text = unicodedata.normalize("NFKD", text)
    text = text.encode("ascii", "ignore").decode("ascii")
    return " ".join(text.lower().split())


def _cvc(stem):
    if len(stem) < 3:
        return False
    if stem[-1] in VOWELS or stem[-1] in "ywx":
        return False
    return stem[-2] in VOWELS and stem[-3] not in VOWELS


def _vowel_groups(stem):
    groups = 0
    previous = False
    for char in stem:
        vowel = char in VOWELS
        if vowel and not previous:
            groups += 1
        previous = vowel
    return groups


def _strip_ending(word, ending):
    stem = word[:-len(ending)]
    if stem in E_BASES:
        return stem + "e"
    if stem.endswith("y"):
        return stem
    doubled = len(stem) > 3 and stem[-1] == stem[-2] and stem[-1] not in VOWELS
    if doubled and stem[-1] in "bdgmnprt":
        return stem[:-1]
    if doubled and stem[-1] == "l" and stem[:-1] in L_BASES:
        return stem[:-1]
    if stem.endswith("c"):
        return stem + "e"
    if stem.endswith("g") and stem not in G_NO_E:
        return stem + "e"
    if stem.endswith("s") and not stem.endswith(("ss", "us", "as")):
        return stem + "e"
    if _cvc(stem) and _vowel_groups(stem) == 1 and stem[-1] not in "scg":
        return stem + "e"
    if len(stem) == 2 and stem[-1] not in VOWELS:
        return stem + "e"
    return stem


def _canon(word):
    mapped = US_UK.get(word)
    if mapped:
        word = mapped
    if word.isdigit():
        return word
    if word.endswith("'s") and len(word) > 3:
        word = word[:-2]
    elif word.endswith("s'") and len(word) > 3:
        word = word[:-2]
    irregular = IRREGULAR.get(word)
    if irregular:
        return irregular
    if len(word) <= 3:
        return word
    if word.endswith("ies") and len(word) > 4:
        return word[:-3] + "y"
    if word.endswith("ied") and len(word) > 4:
        return word[:-3] + "y"
    if word.endswith("eed"):
        return word
    if word.endswith("ing") and len(word) > 5:
        return _strip_ending(word, "ing")
    if word.endswith("ed") and len(word) > 4:
        return _strip_ending(word, "ed")
    if word.endswith("es") and len(word) > 4:
        if word in S_BASES:
            return word
        stem = word[:-2]
        if stem in E_BASES:
            return stem + "e"
        if stem.endswith(("ss", "x", "zz", "ch", "sh", "o")) or stem in S_BASES:
            return stem
        return word[:-1]
    if word.endswith("s") and not word.endswith("ss") and len(word) > 3:
        if word in S_BASES or word.endswith(("us", "is")):
            return word
        return word[:-1]
    return word


def canon(word):
    got = CANON_CACHE.get(word)
    if got is not None:
        return got
    out = _canon(word)
    if len(CANON_CACHE) >= 200000:
        CANON_CACHE.clear()
    CANON_CACHE[word] = out
    return out


def tokens(text):
    clean = _ascii(text)
    out = []
    for raw in WORD.findall(clean):
        for part in EXPAND.get(raw, (raw,)):
            part = US_UK.get(part, part)
            if part in STOPWORDS:
                continue
            part = canon(part)
            if part and part not in STOPWORDS:
                out.append(part)
    return tuple(out)


def pattern_tokens(text):
    text = str(text or "").lower()
    if "&" in text:
        text = text.replace("&", " and ")
    stripped = text.strip()
    if stripped.replace(" ", "").isalnum():
        words = stripped.split()
    else:
        words = PLAIN_SPLIT.split(text)
    out = []
    expand = EXPAND
    us_uk = US_UK
    stop = STOPWORDS
    cache = CANON_CACHE
    for raw in words:
        if not raw:
            continue
        parts = expand.get(raw, (raw,)) if "'" in raw else (raw,)
        for part in parts:
            mapped = us_uk.get(part)
            if mapped is not None:
                part = mapped
            if part in stop:
                continue
            part = cache.get(part) or canon(part)
            if part and part not in stop:
                out.append(part)
    return tuple(out)


def normalise(text):
    return " ".join(tokens(text))
