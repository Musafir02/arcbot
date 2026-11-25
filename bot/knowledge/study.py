import re
import unicodedata

from . import quantity
from .lookup import A_WHAT_TO_WEAR, entry
from ..understanding.normalize import BASE as ENGLISH_WORDS
from .wording import NERVES_BODY, nerves_opening

ANSWERS = ("school-and-study", "language-and-writing")


FRACTIONS_DIVIDE = (
    "Flip the second fraction upside down and multiply: 2/3 divided by 3/5 is 2/3 x 5/3 = 10/9. "
    "Multiplying is top times top and bottom times bottom (2/3 x 3/5 = 6/15, which "
    "simplifies to 2/5), and adding or subtracting needs the same bottom number first, so "
    "1/3 + 1/4 = 4/12 + 3/12 = 7/12.")
FRACTIONS_MULTIPLY = (
    "Top times top, bottom times bottom: 2/3 x 3/5 = 6/15, which simplifies to 2/5. Dividing is "
    "the same trick with the second one flipped over, so 2/3 divided by 3/5 is 2/3 x 5/3 = 10/9. "
    "Adding and subtracting need the same bottom number first: 1/3 + 1/4 = 4/12 + 3/12 = 7/12.")
FRACTIONS_ADD = (
    "Get the same bottom number first: 1/3 + 1/4 becomes 4/12 + 3/12 = 7/12, and subtracting "
    "works the same way. Multiplying is top times top and bottom times bottom (2/3 x 3/5 = 6/15, "
    "which simplifies to 2/5); dividing flips the second one over and multiplies, so 2/3 divided "
    "by 3/5 is 2/3 x 5/3 = 10/9.")
FRACTIONS_SIMPLIFY = (
    "Divide the top and the bottom by the same number until nothing goes into both: 6/15 divide "
    "by 3 and you get 2/5. For sums, multiply top times top and bottom times bottom (2/3 x 3/5 = "
    "6/15, then simplify), divide by flipping the second fraction over (2/3 divided by 3/5 is "
    "2/3 x 5/3 = 10/9), and add or subtract once the bottom numbers match (1/3 + 1/4 = 7/12).")
FRACTIONS_FIRST = (
    (("divide", "dividing", "divided"), FRACTIONS_DIVIDE),
    (("multiply", "multiplying", "multiplied", "times"), FRACTIONS_MULTIPLY),
    (("add", "adding", "plus", "subtract", "subtracting", "subtracted", "minus"),
     FRACTIONS_ADD),
    (("simplify", "simplifying", "cancel", "lowest"), FRACTIONS_SIMPLIFY),
)


_PAST_PAPERS = (
    "Do them under timed conditions, then mark yourself against the real mark scheme - "
    "the marking is where most of the learning is. Keep a list of the question types you "
    "lose marks on and redo only those next time. If you are short of time, do the paper "
    "in your head and write full answers only for the weak sections.")
_PAST_PAPERS_WHEN = (
    "Start about six to eight weeks before the exam, one paper a week, then two a week in the "
    "last month, so the early marks still leave you time to fix what they show. Do each under "
    "timed conditions and mark it against the real mark scheme, and redo only the question "
    "types you lose marks on.")
_PAST_PAPERS_ASK_WHEN = frozenset((
    "when", "should", "start", "starting", "begin", "leave", "leaving", "left", "soon", "late",
    "early", "before", "how long", "how many weeks", "how many months"))


def _past_papers_reply(memory, reading):
    line = str((reading or {}).get("text") or (reading or {}).get("norm") or "").lower()
    words = set(re.findall(r"[a-z']+", line))
    if any(word in words for word in _PAST_PAPERS_ASK_WHEN) and (
            "when" in words or "should" in words or "start" in words or "begin" in words
            or "how long" in line or "how many" in line or "soon" in words):
        return _PAST_PAPERS_WHEN
    return _PAST_PAPERS


def _fractions_reply(memory, reading):
    line = str((reading or {}).get("text") or (reading or {}).get("norm") or "").lower()
    words = set(re.findall(r"[a-z']+", line))
    for asking, said in FRACTIONS_FIRST:
        if any(word in words for word in asking):
            return said
    return FRACTIONS_MULTIPLY



PHRASES = {
    "toilet": {
        "portuguese": ("Onde fica a casa de banho?", "ON-dy FEE-ka a KA-za dy BAN-yo"),
        "greek": ("Poú eínai i toualéta? (πού είναι η τουαλέτα)", "poo EE-neh ee too-a-LEH-ta"),
        "turkish": ("Tuvalet nerede?", "too-va-LET NEH-reh-deh"),
        "welsh": ("Ble mae’r toiled?", "bleh mire TOY-led"),
        "japanese": ("Toire wa doko desu ka (トイレはどこですか)", "TOY-reh wah DOH-koh dess kah"),
        "chinese": ("Xǐshǒujiān zài nǎr? (洗手间在哪儿)", "shee-show-jyen dzai nar"),
        "dutch": ("Waar is het toilet?", "vaar is hut twa-LET"),
        "spanish": ("¿Dónde está el baño?", "DON-day es-TA el BAN-yo"),
        "french": ("Où sont les toilettes ?", "oo son lay twa-LET"),
        "italian": ("Dov'è il bagno?", "do-VEH eel BAN-yo"),
        "german": ("Wo ist die Toilette?", "vo ist dee toy-LET-tuh"),
        "welsh": ("Ble mae'r toiled?", "blay my-re TOY-led"),
        "irish": ("Cá bhfuil an leithreas?", "kaw will an LEH-rass"),
    },
    "thank you": {
        "portuguese": ("Obrigado (a woman says obrigada)", "oh-bree-GAH-doo"),
        "greek": ("Efcharistó (ευχαριστώ)", "ef-kha-ree-STOH"),
        "turkish": ("Teşekkürler", "teh-shek-kewr-LER"),
        "welsh": ("Diolch", "DEE-olch"),
        "japanese": ("Arigatou (ありがとう)", "a-ree-GA-toh"),
        "chinese": ("Xièxie (谢谢)", "shyeh-shyeh"),
        "dutch": ("Dank je wel", "dank yuh vel"),
        "spanish": ("Gracias", "GRA-thee-as"),
        "french": ("Merci", "mair-SEE"),
        "italian": ("Grazie", "GRAT-zee-eh"),
        "german": ("Danke", "DAN-kuh"),
        "welsh": ("Diolch", "DEE-olkh"),
        "irish": ("Go raibh maith agat", "guh rev MAH a-gut"),
        "gaelic": ("Tapadh leat", "TA-pah lat"),
    },
    "please": {
        "portuguese": ("Por favor", "por fa-VOR"),
        "greek": ("Parakaló (παρακαλώ)", "pa-ra-ka-LOH"),
        "turkish": ("Lütfen", "LEWT-fen"),
        "welsh": ("Os gwelwch yn dda", "oss gwel-ooch un thah"),
        "japanese": ("Onegaishimasu (お願いします)", "o-neh-GUY-shee-mas"),
        "chinese": ("Qǐng (请)", "ching"),
        "dutch": ("Alstublieft", "als-too-BLEEFT"),
        "spanish": ("Por favor", "por fa-VOR"),
        "french": ("S'il vous plaît", "seel voo PLEH"),
        "italian": ("Per favore", "per fa-VO-reh"),
        "german": ("Bitte", "BIT-tuh"),
        "welsh": ("Os gwelwch yn dda", "os GWEL-ookh un thah"),
        "irish": ("Le do thoil", "leh duh HULL"),
        "gaelic": ("Mas e do thoil e", "mas eh daw HOLL eh"),
    },
    "hello": {
        "portuguese": ("Olá", "oh-LAH"),
        "greek": ("Kaliméra (καλημέρα)", "ka-lee-MEH-ra"),
        "turkish": ("Merhaba", "mer-ha-BAH"),
        "welsh": ("Helo (Bore da in the morning)", "HEH-loh"),
        "japanese": ("Konnichiwa (こんにちは)", "kon-nee-CHEE-wah"),
        "chinese": ("Nǐ hǎo (你好)", "nee HOW"),
        "dutch": ("Hallo", "HAL-oh"),
        "spanish": ("Hola", "OH-la"),
        "french": ("Bonjour", "bon-ZHOOR"),
        "italian": ("Ciao", "chow"),
        "german": ("Hallo", "HAL-oh"),
        "welsh": ("Helo", "HEH-lo"),
        "irish": ("Dia dhuit", "DEE-a gwit"),
        "gaelic": ("Halò", "ha-LAW"),
    },
    "goodbye": {
        "portuguese": ("Adeus", "a-DEHS"),
        "greek": ("Antío (αντίο)", "an-DEE-oh"),
        "turkish": ("Hoşça kalın", "hosh-cha ka-LUN"),
        "welsh": ("Hwyl fawr", "hooil vowr"),
        "japanese": ("Sayounara (さようなら)", "sa-YOH-na-ra"),
        "chinese": ("Zàijiàn (再见)", "dzai-jyen"),
        "dutch": ("Tot ziens", "tot zeens"),
        "spanish": ("Adiós", "a-DYOS"),
        "french": ("Au revoir", "oh ruh-VWAR"),
        "italian": ("Arrivederci", "a-ree-veh-DAIR-chee"),
        "german": ("Auf Wiedersehen", "owf VEE-der-zayn"),
        "welsh": ("Hwyl fawr", "hooil vower"),
        "irish": ("Slán", "slawn"),
        "gaelic": ("Mar sin leat", "mar shin lat"),
    },
    "how much": {
        "portuguese": ("Quanto custa?", "KWAN-too KOOSH-ta"),
        "greek": ("Póso kánei? (πόσο κάνει)", "POH-so KA-nee"),
        "turkish": ("Ne kadar?", "neh ka-DAR"),
        "welsh": ("Faint yw hwn?", "fynt yoo hoon"),
        "japanese": ("Ikura desu ka (いくらですか)", "ee-KOO-rah dess kah"),
        "chinese": ("Duōshao qián? (多少钱)", "dwaw-shau chyen"),
        "dutch": ("Hoeveel kost het?", "hoo-VAYL kost hut"),
        "spanish": ("¿Cuánto cuesta?", "KWAN-to KWES-ta"),
        "french": ("Combien ça coûte ?", "kom-BYAN sa KOOT"),
        "italian": ("Quanto costa?", "KWAN-to KOS-ta"),
        "german": ("Was kostet das?", "vas KOS-tet das"),
        "welsh": ("Faint yw hyn?", "fynt yoo hin"),
        "irish": ("Cé mhéad?", "kay vayd"),
    },
    "the bill": {
        "spanish": ("La cuenta, por favor", "la KWEN-ta por fa-VOR"),
        "french": ("L'addition, s'il vous plaît", "la-dee-SYON seel voo PLEH"),
        "italian": ("Il conto, per favore", "eel KON-to per fa-VO-reh"),
        "german": ("Die Rechnung, bitte", "dee REKH-noong BIT-tuh"),
        "welsh": ("Y bil, os gwelwch yn dda", "uh bill os GWEL-ookh un thah"),
    },
    "sorry": {
        "spanish": ("Perdón", "per-DON"),
        "french": ("Pardon", "par-DON"),
        "italian": ("Scusi", "SKOO-zee"),
        "german": ("Entschuldigung", "ent-SHOOL-dee-goong"),
        "welsh": ("Mae'n ddrwg gen i", "mine throog gen ee"),
        "irish": ("Tá brón orm", "taw brone or-um"),
    },
    "i don't understand": {
        "spanish": ("No entiendo", "no en-TYEN-do"),
        "french": ("Je ne comprends pas", "zhuh nuh kom-PRAN pa"),
        "italian": ("Non capisco", "non ka-PEES-ko"),
        "german": ("Ich verstehe nicht", "ikh fair-SHTAY-uh nikht"),
        "welsh": ("Dw i ddim yn deall", "doo ee thim un day-al"),
        "irish": ("Ní thuigim", "nee HIG-im"),
    },
    "do you speak english": {
        "spanish": ("¿Habla inglés?", "AB-la een-GLES"),
        "french": ("Parlez-vous anglais ?", "par-lay VOO on-GLEH"),
        "italian": ("Parla inglese?", "PAR-la een-GLEH-zeh"),
        "german": ("Sprechen Sie Englisch?", "SHPREKH-en zee ENG-lish"),
        "welsh": ("Ydych chi'n siarad Saesneg?", "UD-ikh kheen SHAR-ad SICE-neg"),
    },
    "water": {
        "spanish": ("Agua", "AH-gwa"),
        "french": ("De l'eau", "duh loh"),
        "italian": ("Acqua", "AH-kwa"),
        "german": ("Wasser", "VAS-ser"),
        "welsh": ("Dŵr", "door"),
        "irish": ("Uisce", "ISH-ka"),
        "gaelic": ("Uisge", "OOSH-ka"),
    },
    "help": {
        "spanish": ("Socorro", "so-KO-ro"),
        "french": ("Au secours", "oh suh-KOOR"),
        "italian": ("Aiuto", "a-YOO-to"),
        "german": ("Hilfe", "HIL-fuh"),
        "welsh": ("Help!", "help"),
        "irish": ("Cabhair!", "KOW-ir"),
        "gaelic": ("Cuideachadh!", "KOO-jokh-ug"),
    },
    "good morning": {
        "spanish": ("Buenos días", "BWEH-nos DEE-as"),
        "french": ("Bonjour", "bon-ZHOOR"),
        "italian": ("Buongiorno", "bwon-JOR-no"),
        "german": ("Guten Morgen", "GOO-ten MOR-gen"),
        "welsh": ("Bore da", "BOR-eh da"),
        "irish": ("Maidin mhaith", "MA-jin vah"),
        "gaelic": ("Madainn mhath", "MA-din vah"),
    },
    "good night": {
        "spanish": ("Buenas noches", "BWEH-nas NO-chess"),
        "french": ("Bonne nuit", "bon NWEE"),
        "italian": ("Buonanotte", "bwo-na-NOT-teh"),
        "german": ("Gute Nacht", "GOO-tuh nakht"),
        "welsh": ("Nos da", "noss da"),
        "irish": ("Oíche mhaith", "EE-ha vah"),
    },
    "cheers": {
        "spanish": ("Salud", "sa-LOOD"),
        "french": ("Santé", "son-TAY"),
        "italian": ("Salute", "sa-LOO-teh"),
        "german": ("Prost", "prohst"),
        "welsh": ("Iechyd da", "YAKH-id da"),
        "irish": ("Sláinte", "SLAWN-cha"),
        "gaelic": ("Slàinte mhath", "SLAWN-cha vah"),
    },
}

WELSH_AND_IRISH = {
    "thank you": {"welsh": ("Diolch", "DEE-olch"),
                  "irish": ("Go raibh maith agat", "guh rev MAH-ut uh-gut")},
    "please": {"welsh": ("Os gwelwch yn dda", "os GWEL-ookh un thah"),
               "irish": ("Le do thoil", "leh duh HULL")},
    "hello": {"welsh": ("Helo", "HEH-loh"),
              "irish": ("Dia duit", "DEE-uh gwit")},
    "goodbye": {"welsh": ("Hwyl fawr", "hoo-il vowr"),
                "irish": ("Slán", "slawn")},
    "sorry": {"welsh": ("Mae'n ddrwg gen i", "mine throog gen ee"),
              "irish": ("Tá brón orm", "taw brone or-um")},
    "water": {"welsh": ("Dŵr", "door"),
              "irish": ("Uisce", "ISH-keh")},
}
for _concept, _by_language in WELSH_AND_IRISH.items():
    PHRASES.setdefault(_concept, {}).update(_by_language)

LANGUAGES = {
    "spanish": "Spanish", "espanol": "Spanish", "español": "Spanish",
    "french": "French", "francais": "French", "français": "French",
    "italian": "Italian", "italiano": "Italian",
    "german": "German", "deutsch": "German",
    "welsh": "Welsh", "cymraeg": "Welsh", "wales": "Welsh",
    "irish": "Irish", "gaeilge": "Irish", "gailge": "Irish", "as gaeilge": "Irish",
    "gaelic": "Scottish Gaelic", "scottish gaelic": "Scottish Gaelic",
    "portuguese": "Portuguese", "portugues": "Portuguese", "português": "Portuguese",
    "greek": "Greek", "turkish": "Turkish",
    "japanese": "Japanese", "chinese": "Chinese", "mandarin": "Chinese",
    "dutch": "Dutch",
}

CONCEPTS = (
    (("toilet", "loo", "bathroom", "restroom", "bog"), "toilet"),
    (("thank", "thanks"), "thank you"),
    (("please",), "please"),
    (("hello", "hi"), "hello"),
    (("good morning",), "good morning"),
    (("good night", "goodnight"), "good night"),
    (("cheers",), "cheers"),
    (("goodbye", "bye"), "goodbye"),
    (("how much", "cost", "price"), "how much"),
    (("bill", "check", "cheque"), "the bill"),
    (("sorry", "excuse me"), "sorry"),
    (("don't understand", "dont understand", "do not understand"), "i don't understand"),
    (("speak english", "english"), "do you speak english"),
    (("water",), "water"),
    (("help",), "help"),
)


CONCEPT_WORDS = ("thank you", "thanks", "thank", "cheers", "hello", "hi", "please", "goodbye",
                 "bye", "sorry", "excuse me", "water", "help", "toilet", "loo", "bathroom",
                 "good morning", "good night", "goodnight", "how much", "the bill", "bill",
                 "dont understand", "don't understand", "do you speak english", "speak english")

NATIVE = {}
for _concept_name, _said_in in PHRASES.items():
    for _language, (_phrase, _say) in _said_in.items():
        for _word in (_phrase, _phrase.strip("!?¿")):
            _word = _word.strip("!?¿.,").lower()
            if (len(_word) > 2 and _word.isalpha() and _word not in _concept_name.split()
                    and _word not in ENGLISH_WORDS):
                NATIVE.setdefault(_word, (_language, _concept_name))
                _plain = "".join(c for c in unicodedata.normalize("NFKD", _word)
                                 if not unicodedata.combining(c))
                if _plain != _word and _plain not in ENGLISH_WORDS:
                    NATIVE.setdefault(_plain, (_language, _concept_name))
del _concept_name, _said_in, _language, _phrase, _say, _word, _plain


_A_MEANING_IS_ASKED = re.compile(
    r"\bwhat\s+(?:does|do|did)\b[^?.!]{0,40}\bmean(?:s|ing)?\b"
    r"|\bmean(?:s|ing|ings)?\b"
    r"|\bhow\s+(?:do|can|would|should|could)\s+(?:you|i|we)\s+say\b"
    r"|\btranslat(?:e|ion|ions)\b", re.I)

LANGUAGE_NAMES = ("german", "french", "spanish", "italian", "welsh", "irish", "gaelic",
                  "portuguese", "greek", "polish", "dutch", "turkish", "japanese", "chinese",
                  "mandarin", "cantonese", "arabic", "russian", "hindi", "urdu", "bengali",
                  "punjabi", "somali", "romanian", "czech", "swedish", "norwegian", "danish",
                  "finnish", "korean", "thai", "vietnamese", "hebrew", "swahili", "tagalog",
                  "ukrainian", "latin", "afrikaans", "albanian", "bulgarian", "croatian",
                  "serbian", "slovak", "slovenian", "estonian", "latvian", "lithuanian",
                  "hungarian", "icelandic", "malay", "indonesian", "persian", "farsi", "kurdish",
                  "amharic", "yoruba", "zulu", "xhosa", "creole", "filipino", "sign language")


_ENGLISH_FURNITURE = frozenset((
    "a", "an", "the", "is", "are", "was", "were", "be", "am", "what", "whats", "what's", "which",
    "it", "this", "that", "these", "those", "in", "on", "of", "to", "for", "and", "or", "do",
    "does", "did", "you", "i", "we", "they", "he", "she", "mean", "means", "meaning", "say",
    "please", "so", "my", "your", "his", "her", "their", "our", "there", "here", "s"))


_SOMETHING_WRITTEN = (
    "essay", "essays", "dissertation", "coursework", "assignment", "assignments", "report",
    "reports", "paragraph", "paragraphs", "write", "writing", "written", "thesis", "paper",
    "papers", "project", "projects", "chapter", "chapters", "story", "stories", "mark", "marks",
    "grade", "grades", "tutor", "teacher", "lecturer", "uni", "university", "college", "gcse",
    "a level", "a-level", "aqa", "edexcel", "english", "history", "politics", "sociology",
    "psychology", "biology", "geography", "question", "questions", "title",
    "speech", "speeches", "talk", "talks",
)
_A_CONCLUSION_SAID = ("conclusion", "conclusions", "conclude", "sum up", "summarise", "summarize",
                      "last paragraph", "final paragraph", "wrap up")


def _the_ending_is_written(understood):
    clean = " ".join(str(understood.get("clean") or understood.get("text") or "").split()).lower()
    if not clean:
        return False
    for word in _A_CONCLUSION_SAID + _SOMETHING_WRITTEN:
        if re.search(r"(?<![a-z0-9])" + re.escape(word) + r"(?![a-z0-9])", clean):
            return True
    return False


def _a_translation_is_asked(understood):
    clean = str(understood.get("clean") or understood.get("text") or "").lower()
    if _A_MEANING_IS_ASKED.search(clean):
        return True
    words = [str(word).lower() for word in (understood.get("words") or ())]
    content = [word for word in words if word not in _ENGLISH_FURNITURE]
    named = any(re.search(r"(?<![a-z])" + name + r"(?![a-z])", clean) for name in LANGUAGE_NAMES)
    if named and (any(word in NATIVE for word in content) or _A_MEANING_IS_ASKED.search(clean)
                  or re.search(r"\bsay\b|\bhow do you\b|\bhow do i\b", clean)):
        return True
    return bool(content) and all(word in NATIVE for word in content)


def _what_does_it_mean(memory, understood):
    if not _a_translation_is_asked(understood):
        return None
    clean = (understood.get("clean") or "").lower()
    for word in sorted(NATIVE, key=len, reverse=True):
        if re.search(r"(?<![a-z])" + re.escape(word) + r"(?![a-z])", clean):
            language, concept = NATIVE[word]
            english = "I don't understand" if concept == "i don't understand" else concept
            return (f"That is {LANGUAGES[language]} for '{english}'. It is a phrase people say a "
                    "lot, so learn it whole and out loud rather than word by word, and the reply "
                    "you get back will tell you whether it landed.")
    return None


_MEANING_FRAME = re.compile(r"\bwhat\s+does\b|\bwhat'?s\b|\bwhat\s+is\b|\bmean(s|ing)?\b"
                           r"|\bstand\s+for\b|\btranslate[sd]?\b|\btranslation\b")
_ASKED_OUTRIGHT = re.compile(r"\bmean(s|ing)?\b|\bstand\s+for\b|\btranslate[sd]?\b"
                             r"|\bhow\s+do\s+you\s+say\b")
_ENGLISH_TOO = frozenset((
    "was", "die", "non", "tot", "mas", "nos", "dia", "per", "mar", "faint", "bore", "dank",
    "salute", "sante", "santé", "wasser", "ble"))


def _a_word_is_being_asked_about(understood):
    said = str((understood or {}).get("clean") or (understood or {}).get("text") or "").lower()
    if not _MEANING_FRAME.search(said):
        return False
    named = [word for word in NATIVE
             if re.search(r"(?<![a-z])" + re.escape(word) + r"(?![a-z])", said)]
    if not named:
        return False
    if any(word not in _ENGLISH_TOO for word in named):
        return True
    return bool(_find(said, LANGUAGES)) or '"' in said or "\u201c" in said


def _find(text, table):
    for name in sorted(table, key=len, reverse=True):
        if re.search(r"\b" + re.escape(name) + r"\b", text):
            return name
    return None


def _concept(text):
    for alternatives, name in CONCEPTS:
        for alternative in alternatives:
            if re.search(r"(?<![a-z])" + re.escape(alternative) + r"(?![a-z])", text):
                return name
    return None


_ABOUT_THE_PLATE = re.compile(
    r"(?<![a-z])(?:food|foods|cuisine|dish|dishes|eat|eating|meals?|restaurants?)"
    r"(?![a-z])", re.I)
_SAY_OR_TRANSLATE = re.compile(
    r"(?<![a-z])(?:say|says|saying|pronounce|pronounced|translate|translated|translation|"
    r"mean|means|how do you say)(?![a-z])", re.I)


_PHRASE_ASK = re.compile(
    r"\bhow\b[^?.!]{0,30}\b(?:say|pronounce|translate)\b"
    r"|\bsay\b|\bpronounce\b|\btranslat(?:e|ion|ions)\b"
    r"|\bwords?\s+for\b|\bphrase(?:s)?\s+for\b"
    r"|\bin\s+(?:%s)\b" % "|".join(LANGUAGE_NAMES), re.I)


_CORRECTION_WORDS = frozenset((
    "actually", "no", "not", "sorry", "im", "i'm", "meant", "mean", "instead", "rather",
    "then", "make", "change", "changed", "changing", "switch", "switched", "let", "lets",
    "let's", "learn", "learning", "learnt", "studying", "study", "pick", "picking",
    "choose", "choosing", "language", "languages", "one", "ones", "about", "also", "too",
    "both", "them", "other", "another", "re", "well", "decide", "deciding", "decided"))
_CORRECTION_FURNITURE = _ENGLISH_FURNITURE | _CORRECTION_WORDS


def _a_language_alone(text):
    words = [word for word in re.findall(r"[a-z']+", text)
             if word not in _CORRECTION_FURNITURE]
    return bool(words) and all(word in LANGUAGE_NAMES for word in words)


def _a_phrase_is_asked(understood):
    text = " ".join(str((understood or {}).get("clean")
                       or (understood or {}).get("text") or "").lower().split())
    if _PHRASE_ASK.search(text):
        return True
    if _concept(text):
        return True
    return _a_language_alone(text)


def _say_in_language(memory, understood):
    clean = (understood.get("clean") or "").lower()
    if _ABOUT_THE_PLATE.search(clean) and not _SAY_OR_TRANSLATE.search(clean):
        return None
    language = _find(clean, LANGUAGES)
    if not language:
        return None
    concept = _concept(clean)
    if not concept:
        return (f"Learn {LANGUAGES[language]} as a set of whole phrases rather than word by word, "
                "and learn them out loud: 'hello', 'please', 'thank you', 'sorry, I don't understand', "
                "'do you speak English?' and 'how much is that?' cover most of a short trip. Ask me any "
                "of those in one language and I will give you the phrase and how to say it.")
    pair = PHRASES.get(concept, {}).get(language)
    if not pair:
        return (f"Learn {LANGUAGES[language]} as a set of whole phrases rather than word by word, "
                "and learn them out loud: 'hello', 'please', 'thank you', 'sorry, I don't understand', "
                "'do you speak English?' and 'how much is that?' cover most of a short trip. Ask me any "
                "of those in one language and I will give you the phrase and how to say it.")
    phrase, say = pair
    question = concept if concept != "i don't understand" else "I don't understand"
    return (f"'{question.capitalize()}' in {LANGUAGES[language]} is {phrase} — say it roughly "
            f"\"{say}\". Learn it out loud a few times rather than reading it, and people will "
            "understand you even if the pronunciation is not perfect.")


_A_DEGREE_OF_HEAT = ("heat", "warm", "hot", "cold", "weather", "celsius", "centigrade",
                     "fahrenheit", "temperature", "thermostat", "fever", "oven",
                     "washing machine", "angle", "bend", "slope", "latitude",
                     "gas mark", "convert", "conversion", "degrees c", "degrees f")

_TEMPERATURE_DEGREES = re.compile(
    r"(?<![\w:.\d])(?<!\d\s)(?:[1-9]|[1-3][0-9]|40)\s*(?:degrees?\b|deg\b|°)")
_NUMBER_WORDS = frozenset((
    "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven",
    "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen",
    "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety", "hundred"))


def _a_number_word(words):
    for word in words:
        for part in re.split(r"[-\s]", word):
            if part in _NUMBER_WORDS:
                return True
    return False


def _the_degrees_are_heat(understood):
    text = str(understood.get("clean") or understood.get("text") or "").lower()
    words = set(understood.get("words") or ())
    if not ({"degree", "degrees"} & words):
        return True
    if not (_TEMPERATURE_DEGREES.search(text) or _a_number_word(words)):
        return True
    if (words - {"degree", "degrees"}).intersection(_EXAM_IN_THE_WORDS):
        return True
    if re.search(r"\b(?:my|the|a|his|her|their|your)\s+degree\b|\bdegree\s+(?:in|course|exam)\b",
                 text):
        return True
    return False


_FAILING = frozenset(("fail", "failed", "failing", "fails", "flunk", "flunked", "flunking"))
_EXAM_IN_THE_WORDS = frozenset((
    "exam", "exams", "examination", "gcse", "gcses", "a-level", "a-levels", "alevel", "alevels",
    "as-level", "as-levels", "mock", "mocks", "coursework", "resit", "resits", "retake",
    "retakes", "remark", "remarks", "module", "modules", "degree", "semester", "dissertation",
    "grade", "grades", "uni", "university", "college", "school", "sixth", "year", "paper",
    "papers", "results", "sats", "btec", "ib",
))


def _a_failure_of_something_else(understood):
    words = [str(word).lower() for word in (understood or {}).get("words") or []]
    if not any(word in _FAILING for word in words):
        return False
    return not any(word in _EXAM_IN_THE_WORDS for word in words)


NOT_AN_EXAM = ("blood", "driving", "pregnant", "pregnancy", "swab", "urine", "hearing",
               "eye", "eyes", "sight", "allergy", "allergies", "covid", "pcr", "lateral",
               "theory", "smear",
               "cv", "resume", "résumé",
               "cricket", "cricketer", "cricketers", "test match", "test matches", "wicket",
               "wickets", "innings", "bowler", "bowlers", "bowling", "batting", "batter",
               "batsman", "stumps", "ashes", "lbw",
               "motor", "motors", "engine", "engines", "car", "cars", "van", "vans",

               "battery", "batteries", "lawnmower", "mower", "boiler", "starter motor",
               "changing the subject", "change the subject", "changed the subject",
               "change of subject", "off topic", "on a different subject",
               "onto a different subject")

NOT_A_PERSONS_NOTE = (
    "thank you note", "thank-you note", "thankyou note", "thanks note",
    "apology note", "apologise note", "apologize note", "apologising note", "apologizing note",
    "sorry note", "condolence note", "sympathy note", "get well note", "welcome note",
    "short note", "little note", "note saying", "a note to my", "note to my", "note for my",
    "note to the", "note for the", "note to a", "note for a",
)

LOSING_TRACK_OF_MONEY = ("money", "spending", "spent", "spend", "budget", "budgets",
                         "outgoings", "goes out", "going out of my account", "bank", "bills",
                         "paycheck", "payday", "salary", "wages", "direct debit",
                         "direct debits", "standing order", "statement", "account",
                         "what i earn", "savings", "overdrawn", "debt", "debts"),


TEST_AS_A_VERB = re.compile(
    r"\btest(?:ed|ing|s)?\s+(?:if|whether|that|the|a|an|my|your|our|his|her|its|this|these|"
    r"those|any|some|for|out|with|by)\b", re.I)

TIME_AFTER_TEST = re.compile(
    r"\btest\s+(?:a|an|one|two|three|\d+)\s+"
    r"(?:week|weeks|day|days|month|months|year|years|fortnight|hour|hours|minute|minutes)\b",
    re.I)

LEARNING_OBJECTS = frozenset("""knowledge memory learning revise revised revising revision
exam exams mock mocks vocab vocabulary spelling spellings grammar tenses reading maths math
gcse alevel a-level subject subjects topic topics syllabus paper comprehension
know knows knew remember remembers remembered learnt learned french spanish german italian
english history geography science biology chemistry physics chinese""".split())


def _a_test_of_a_thing(understood):
    if not isinstance(understood, dict):
        return False
    text = understood.get("norm_text") or understood.get("clean") or ""
    if not text or not TEST_AS_A_VERB.search(str(text)):
        return False
    if TIME_AFTER_TEST.search(str(text)):
        return False
    words = {str(word).lower() for word in (understood.get("words") or [])}
    return not (words & LEARNING_OBJECTS)


def _unless_testing_a_thing(reply):
    def answer(memory, understood):
        if _a_test_of_a_thing(understood):
            return ""
        return reply
    return answer



ASLEEP = ("asleep", "falling asleep", "sleepy", "tired", "drowsy", "nodding off", "sleep")

_OTHER_PEOPLE = frozenset((
    "dad", "dads", "father", "mum", "mums", "mother", "husband", "wife", "partner",
    "spouse", "nan", "nana", "gran", "granny", "grandma", "grandmother", "grandad",
    "granddad", "grandfather", "brother", "sister", "aunt", "auntie", "uncle",
    "father in law", "mother in law", "in laws", "other half", "boyfriend", "girlfriend"))
_FORGETTING = frozenset((
    "forget", "forgets", "forgetting", "forgot", "forgotten", "remember", "remembers",
    "remembering", "memory", "recall", "names", "name", "words"))


EXAM_NERVES = ("Going blank is your body, not your memory: breathe out longer than you breathe "
               "in for a minute and it settles. Then read the whole paper and start with the "
               "question you know best, and if a question stalls, jot the first line you can and "
               "move on. Do not spend the first five minutes trying to feel calm — just start "
               "writing.")


def _exam_nerves(memory, understood):
    said = str(understood.get("clean") or understood.get("text") or "").lower()
    if any(phrase in said for phrase in NERVES_BODY):
        return (nerves_opening(said, "before an exam", "adrenaline, not a bug") +
                ": eat something plain, take water in with you, and breathe out slowly for a "
                "minute in the queue. " + EXAM_NERVES)
    return EXAM_NERVES


def _somebody_else_forgets(understood):
    words = [str(word).lower() for word in (understood or {}).get("words") or []]
    if not any(word in _FORGETTING for word in words):
        return False
    return any(word in _OTHER_PEOPLE for word in words)

REST_ASK = ("take a break", "take breaks", "take my break", "take a rest", "a break from",
            "break from studying", "break from revision", "break from revising", "breaks from",
            "rest from studying", "how often break", "how often should i break",
            "how long a break", "how long should i break", "break between", "breaks between",
            "should i break", "should i take a break")

NOT_A_START_OF_EXAMS = ("running out of time", "run out of time", "ran out of time",
                       "out of time", "no time left", "time in the exam", "time in exams",
                       "finish the paper")
NOT_REVISION = ("instructions", "assembling", "manual", "flat pack", "flatpack", "ikea",
                "rota", "rotas", "advert", "adverts", "job advert", "the wording", "its wording",
                "policy document", "policy wording", "terms and conditions", "the invoice",
                "an invoice", "before signing",
                "revise the contract", "revise a contract", "revise my contract",
                "revising the contract", "revise the lease", "revise the agreement",
                "revise the budget", "revise my budget", "revise a budget",
                "revise my essay", "revise the essay", "revise my cv", "revise my resume")

LANGUAGE_LEARNING = ("language", "languages", "spanish", "french", "italian", "german",
                     "portuguese", "japanese", "chinese", "mandarin", "cantonese", "welsh",
                     "korean", "russian", "arabic", "dutch", "greek", "polish", "turkish",
                     "urdu", "punjabi", "hindi", "british sign language", "sign language",
                     "fluent", "fluency", "fluently", "duolingo", "bilingual")

MOCK = ("mock", "mocks", "practice paper", "practice papers", "predicted",
        "predicted grade", "predicted grades")

HOW_ASK = ("good way", "best way", "right way", "proper way", "way", "ways", "tips", "tip",
           "advice", "the trick")

A_SUBJECT = ("maths", "math", "mathematics", "algebra", "geometry", "trigonometry", "physics",
             "chemistry")

A_MARK_NOT_A_GRADE = ("out", "of", "than", "per", "over", "under")
COUNTED_AFTER = ("marks", "mark", "out", "%", "percent", "subjects", "hours", "years", "days",
                 "weeks", "months", "kids", "children", "grandchildren", "questions", "pages",
                 "miles", "minutes", "times", "weeks", "gcse", "gcses")


GRADE_NAME = re.compile(r"^(?:a[\s*-]?stars?|a\*s?|grades?|gcses?|a[\s-]?levels?|btecs?)\b")
LETTER_GRADES = re.compile(r"^(?:as|bs|cs|ds|es|fs|us)(?:$|\s+(?:and|in)\b)")


TOP_GRADES = re.compile(r"\b(?:[2-9]|1[0-2])\s+a[\s*-]?stars?\b|\b(?:straight|all)\s+(?:9s|8s)"
                        r"|\b[2-9]\s+a\*s\b", re.I)


def _grade_in(clean):
    words = clean.replace(",", " ").split()
    for n, word in enumerate(words):
        match = re.fullmatch(r"([1-9])%?", word)
        if not match:
            continue
        before = words[n - 1] if n else ""
        after = words[n + 1] if n + 1 < len(words) else ""
        next_two = " ".join(words[n + 1:n + 3])
        if before in A_MARK_NOT_A_GRADE or word.endswith("%"):
            continue
        if (after in COUNTED_AFTER or next_two.startswith("a level")
                or GRADE_NAME.match(next_two) or LETTER_GRADES.match(next_two)):
            continue
        return match.group(1)
    return None


def _grade_sentence(grade):
    if grade == "9":
        return "A 9 is the top grade, above the old A*."
    if grade in ("7", "8"):
        a = "An" if grade == "8" else "A"
        return f"{a} {grade} is a top grade, the old A and above."
    if grade == "6":
        return "A 6 is a good pass, about the old B."
    if grade == "5":
        return "A 5 is a strong pass, the old high C, and over the line most colleges ask for."
    if grade == "4":
        return ("A 4 is a standard pass, the old C: you are over the line most colleges ask for, "
                "and a 5 is the strong pass above it.")
    return (f"A {grade} is below a pass at GCSE. Most sixth forms and colleges take you on other "
            "subjects and have you retake English or maths alongside, and that retake is free "
            "until you are 18, so it does not close anything on its own.")


SCORE = re.compile(r"\b(\d{1,3})\b[^0-9,]{0,30}?\b(?:out of|/)\s*(\d{1,3})\b")


def _score_out_of(clean):
    match = SCORE.search(clean)
    if not match:
        return None
    got, total = int(match.group(1)), int(match.group(2))
    if not 1 <= got <= total <= 200 or total < 5:
        return None
    return got, total, round(100 * got / total)


def _score_sentence(score):
    got, total, percent = score
    part = "about half" if 40 <= percent <= 60 else ("most" if percent > 60 else "under half")
    return f"That is {got} out of {total}, {part} the marks."


def _grade_answer(memory, understood):
    clean = (understood.get("clean") or "").lower()
    if TOP_GRADES.search(clean):
        return None
    score = _score_out_of(clean)
    if score is not None:
        return (_score_sentence(score) + " Treat that as a score rather than a grade, because a "
                "GCSE grade is where you stand across a whole subject and one piece of work "
                "cannot tell you that. Go through it and write down the questions that lost the "
                "marks, then ask your teacher for the mark scheme on the worst two, since the "
                "same kind of question is usually where the marks are next time.")
    grade = _grade_in(clean)
    if grade is None:
        if not re.search(r"\b(?:gcses?|grades?|marks|score|scores|pass|passed|mocks?|exams?)\b",
                         clean):
            return None
        return ("GCSE grades run from 9 down to 1: 4 is a standard pass, 5 a strong one, and 7 "
                "to 9 are the top grades. Below 4 is not a pass yet, and English and maths can "
                "be retaken at college until you are 18. Tell me the grade and the subject and "
                "I will say what it opens up.")
    if grade >= "4":
        return (f"{_grade_sentence(grade)} English and maths are the two that colleges and "
                "employers look at first, whatever else you take.")
    return _grade_sentence(grade)


def _mock_answer(memory, understood):
    clean = (understood.get("clean") or "").lower()
    grade = _grade_in(clean)
    score = _score_out_of(clean)
    answer = ("" if score is None else _score_sentence(score) + " ") + (
              "A mock or a predicted grade is a signal, not a verdict: find out which topics cost "
              "you the marks — the mark scheme for a mock, your teacher for a predicted grade — "
              "and give the worst two a 25-minute slot each week. Moving a grade or two in a term "
              "is normal.")
    if grade is not None:
        answer = f"{_grade_sentence(grade)} {answer}"
    if re.search(r"\buni\b|\buniversit(y|ies)\b|\bcollege\b|sixth form", clean):
        answer += (" For the university question, what counts is what the course asks for: check "
                   "two or three you like and their entry requirements, because a 6 at GCSE rarely "
                   "closes a door on its own.")
    return answer

_FEELS_WRONGED = re.compile(
    r"\bhate[sd]?\b|\bhating\b|doesn'?t like me|does not like me|dont like me|"
    r"picks? on me|picked on|shouts? at me|\bunfair\b|\bmean\b|\bharsh\b|\bganging\b")


_IS_CHILD = re.compile(r"\bson\b|\bdaughter\b|\bchild\b|\bkids?\b|\bstepson\b|"
                       r"\bstepdaughter\b|\bniece\b|\bnephew\b|\bgrandson\b|"
                       r"\bgranddaughter\b")

_SCHOOL_THINGS = re.compile(
    r"\bteacher|\bclass\b|\bclasses\b|\blesson|\bschool|\bform tutor\b|\btutor\b|"
    r"\bhead of year\b|\bheadteacher|\bpupil|\bhomework|\bmarks\b|\bdetention|\bexcluded\b|"
    r"\bmaths\b|\bmath\b|\bmathematics\b|\benglish\b|\bscience\b|\bhistory\b|"
    r"\bgeography\b|\bchemistry\b|\bphysics\b|\bbiology\b|\bfrench\b|\bspanish\b|"
    r"\bgerman\b|\bart\b|\bmusic\b|\bdrama\b|\bcomputing\b|\bict\b|\bgcses?\b|"
    r"\ba levels?\b|\bsats\b|\bform\b|\bassembly\b|\bplayground\b")


def _a_school_line(understood):
    read = understood if isinstance(understood, dict) else {}
    said = " ".join(str(read.get("clean") or read.get("text") or "").lower().split())
    return bool(_SCHOOL_THINGS.search(said))


def _strict_teacher(memory, understood):
    text = ""
    if isinstance(understood, dict):
        text = understood.get("norm_text") or understood.get("clean") or ""
    plan = ("Do the boring things first and most strict teachers stop being a problem: hand work "
            "in on time, sit where you are seen, and ask one question in the lesson so they know "
            "your name for the right reason. If it is personal - sarcasm, singled out, marks that "
            "do not match the work - ask for the marked work back in writing and take it to your "
            "form tutor or head of year with dates and one example, not a general complaint. Keep "
            "the tone flat and factual, because a complaint that is a feeling gets deflected and "
            "one that is a date, a thing said and a mark does not. Ask a parent to come to the "
            "meeting if you are at school.")
    if not _FEELS_WRONGED.search(text.lower()):
        return plan
    if _IS_CHILD.search(text.lower()):
        return ("Take it seriously, then test it before you act: ask what happens in that lesson "
                "and whether other children say the same, because most of these turn out to be "
                "about one subject or one seating plan. Then ask the school for a short meeting "
                "with the class teacher, and go to the head of year if nothing changes in a term. "
                "Ask for the marked work so the conversation is about the marks and not about "
                "whether the teacher likes him.")
    return ("That is a miserable way to spend a lesson, and it is worth testing before you believe "
            "it: most teachers who seem to hate one person are strict with the whole class. " + plan)


LANGUAGE_HOURS = {
    "spanish": 600, "french": 600, "italian": 600, "portuguese": 600, "dutch": 600,
    "afrikaans": 600, "swedish": 600, "norwegian": 600, "danish": 600, "romanian": 600,
    "german": 750, "welsh": 900, "irish": 900, "greek": 1100, "polish": 1100,
    "russian": 1100, "turkish": 1100, "hebrew": 1100, "hindi": 1100, "urdu": 1100,
    "punjabi": 1100, "vietnamese": 1100, "thai": 1100, "persian": 1100, "farsi": 1100,
    "japanese": 2200, "chinese": 2200, "mandarin": 2200, "cantonese": 2200,
    "korean": 2200, "arabic": 2200,
}


def _names_a_language(understood):
    if not isinstance(understood, dict):
        return False
    clean = (understood.get("clean") or understood.get("text") or "").lower()
    leaned = understood.get("leans_on") if isinstance(understood.get("leans_on"), dict) else {}
    said = " ".join([clean, " ".join(understood.get("words") or ()),
                     str(leaned.get("text") or ""),
                     " ".join(leaned.get("words") or ())]).lower()
    if _find(said, LANGUAGE_HOURS):
        return True
    words = set(re.findall(r"[a-z']+", said))
    return bool(words & {"language", "languages", "fluent", "fluency", "fluently", "bilingual",
                         "conversation", "conversations", "speak", "speaking", "spoken"})


def _the_language_the_chat_named(memory):
    if not isinstance(memory, dict):
        return ""
    for turn in reversed((memory.get("turns") or [])[-6:]):
        said = str(turn.get("user") or "").lower() if isinstance(turn, dict) else ""
        named = _find(said, LANGUAGE_HOURS) if said else ""
        if named:
            return named
    return ""


def _language_hours(memory, understood):
    clean = (understood.get("clean") or "").lower()
    named = _find(clean, LANGUAGE_HOURS) or _the_language_the_chat_named(memory)
    hours = LANGUAGE_HOURS.get(named or "", 600)
    where = named.capitalize() if named else "Spanish, French or Italian"
    years = max(2, round(hours / 365))
    return (f"About {hours} hours of real study to hold a proper conversation in {where} - around "
            f"{years} years at an hour a day, or three times that at twenty minutes a day, which "
            "is why a little every day beats a long weekend. A holiday and small talk come far "
            "sooner: about 100 hours, which a twice-weekly evening class reaches in a year.")



_FORGET_TO_DO = re.compile(
    r"\bforget(?:s|ting)?\s+to\s+(?:ring|call|text|reply|post|book|pay|take|drink|eat|feed|walk|"
    r"charge|water|tidy|clean|put|send|bring|buy|collect|cancel|renew|order|email|message|"
    r"pick|do|go|get|check|ask|tell|remind|turn|lock|switch|defrost|batch|prep)\b")
_THE_PAGE = ("read", "reading", "book", "books", "chapter", "page", "pages", "textbook",
             "article", "paragraph", "notes", "revision", "revise", "study", "studying")

_LAST_TIME = re.compile(
    r"\b(?:cant|dont|couldnt|doesnt|didnt|did not|do not|cannot)\s+remember\s+"
    r"(?:(?:the|a)\s+)?last\s+(?:time|night|day|week|month|year)\b")


_HOW_TO_REMEMBER = re.compile(
    r"\bhow\s+(?:can|do|should|would|could)?\s*(?:i|you|we|to)\s+(?:better\s+|best\s+)?"
    r"(?:remember|memorise|memorize|retain|take in)\b")


def _the_page_is_what_was_forgotten(understood):
    reading = understood if isinstance(understood, dict) else {}
    text = " ".join(str(reading.get("clean") or reading.get("text") or "").lower().split())
    if any(word in text.split() for word in _THE_PAGE):
        return True
    if _HOW_TO_REMEMBER.search(text):
        return True
    if _LAST_TIME.search(text):
        return False
    if _FORGET_TO_DO.search(text):
        return False
    return False


CLASS_BAND = {
    "first": 70,
    "2:1": 60,
    "2:2": 50,
    "third": 40,
}

CLASS_SAYS = {
    "first": (
        "a first is a first-class honours degree: a weighted average of 70% or more, the top "
        "class, and the one PhD funding usually asks for. Below it, a 2:1 is 60 to 69, a 2:2 is "
        "50 to 59, a third is 40 to 49, and a degree passes at 40% overall."),
    "2:1": (
        "a 2:1 is an upper second-class honours degree: a weighted average of 60 to 69%, the "
        "class most graduate schemes and master's courses ask for. Above it a first is 70% and "
        "up, below it a 2:2 is 50 to 59 and a third is 40 to 49, and a degree passes at 40% "
        "overall."),
    "2:2": (
        "a 2:2 is a lower second-class honours degree: a weighted average of 50 to 59%, one band "
        "below a 2:1 (60 to 69) and one above a third (40 to 49). A degree passes at 40% overall, "
        "and plenty of jobs and master's courses still take a 2:2."),
    "third": (
        "a third is a third-class honours degree: a weighted average of 40 to 49%, still honours "
        "but the lowest class, one band below a 2:2 (50 to 59). A degree passes at 40% overall."),
    "distinction": (
        "a distinction is the top award on a master's: an average of 70% or more, with a merit "
        "at 60 to 69 and a pass at 50 (a bachelor's degree passes at 40%)."),
    "merit": (
        "a merit is the middle award on a master's: an average of 60 to 69%, between a "
        "distinction (70 and up) and a pass at 50 (a bachelor's degree passes at 40%)."),
}

CLASS_NAMES = (
    ("2:1", (r"\b2\s*:\s*1\b", r"\b2\.1\b", r"\b2\s1\b", r"\bupper second\b",
             r"\bupper-second\b")),
    ("2:2", (r"\b2\s*:\s*2\b", r"\b2\.2\b", r"\b2\s2\b", r"\blower second\b",
             r"\blower-second\b")),
    ("first", (r"\bfirst class\b", r"\bfirst-class\b", r"\b1st class\b")),
    ("third", (r"\bthird class\b", r"\bthird-class\b", r"\b3rd class\b")),
    ("distinction", (r"\bdistinction\b",)),
    ("merit", (r"\bmerit\b",)),
)
CLASS_ALONE = (
    ("first", re.compile(r"\b(?:a|the|my|get|got|need|want)\s+first\b")),
    ("third", re.compile(r"\b(?:a|the|my|get|got|need|want)\s+third\b")),
)
NOT_THE_CLASS = ("first year", "first term", "first attempt", "first time", "first day",
                 "first week", "first draft", "first choice", "first job", "first child",
                 "first baby", "first home", "first house", "first car", "third year",
                 "third term", "third attempt", "third time", "third week", "third child",
                 "third baby", "third party")


def _classes_named(clean):
    found = []
    for name, patterns in CLASS_NAMES:
        for pattern in patterns:
            match = re.search(pattern, clean)
            if match and name not in found:
                found.append((match.start(), name))
    if not found and not any(phrase in clean for phrase in NOT_THE_CLASS):
        for name, pattern in CLASS_ALONE:
            match = pattern.search(clean)
            if match and name not in found:
                found.append((match.start(), name))
    return [name for _, name in sorted(found)]


HALF_OF_CLASS = (
    ("low", r"\blow\s+(?:2\s*:\s*1|2\.1|upper second)\b", "2:1", 60, 64),
    ("high", r"\bhigh\s+(?:2\s*:\s*1|2\.1|upper second)\b", "2:1", 65, 69),
    ("low", r"\blow\s+(?:2\s*:\s*2|2\.2|lower second)\b", "2:2", 50, 54),
    ("high", r"\bhigh\s+(?:2\s*:\s*2|2\.2|lower second)\b", "2:2", 55, 59),
)


def _half_of_class_said(clean):
    for word, pattern, name, low, high in HALF_OF_CLASS:
        if re.search(pattern, clean):
            side = "bottom" if word == "low" else "top"
            return (f"A {word} {name} is the {side} of that band: a weighted average of "
                    f"{low} to {high}%, and it counts as a {name} on a certificate.")
    return ""


PASS_MARK = (
    "A degree passes at 40% in most UK universities (50% in Scotland, and 50% for a taught "
    "masters), and the class comes from your average, weighted by credits: 70% and up is a "
    "first, 60 to 69 a 2:1, 50 to 59 a 2:2 and 40 to 49 a third. Modules usually need 40% to "
    "count, a resit is often capped at the pass mark, and some courses need a pass in every "
    "year to carry credits forward, so check your course handbook.")


def _university_pass_mark(memory, understood):
    understanding = understood or {}
    clean = str(understanding.get("clean") or "").lower()
    asks = tuple(understanding.get("asks") or ())
    classes = _classes_named(clean)
    if not classes:
        return PASS_MARK
    if "how" in asks or "steps" in asks:
        return PASS_MARK
    defines = ("definition" in asks or "compare" in asks
               or any(word in clean for word in
                      ("mean", "means", "stands for", "stand for", "difference between"))
               or any(word in clean for word in ("percentage", "percent", "what grade")))
    if not defines:
        return PASS_MARK
    half = _half_of_class_said(clean)
    if half:
        return "In UK universities, " + half[0].lower() + half[1:] + " " + "In full, " + CLASS_SAYS[classes[0]]
    said = "In UK universities, " + CLASS_SAYS[classes[0]]
    if len(classes) > 1:
        said += " " + CLASS_SAYS[classes[1]][0].upper() + CLASS_SAYS[classes[1]][1:]
        first, second = classes[0], classes[1]
        if first in CLASS_BAND and second in CLASS_BAND:
            gap = abs(CLASS_BAND[first] - CLASS_BAND[second])
            bands = "one band" if gap == 10 else f"{gap // 10} bands"
            said += (f" So the line between them is {gap} points of average, {bands}, and the "
                     "higher one is the class a course or a job asks for by name.")
    return said



ENTRIES = [
    entry("homework-worth-it", (("homework", "home work", "homeworks"),
                                ("good idea", "a good idea", "worth it", "worthwhile", "useful",
                                 "point", "bad", "benefit", "help", "helps", "think", "opinion",
                                 "too much", "actually", "effective", "any good", "necessary",
                                 "good", "helps", "kids", "children"),
                                ("good idea", "worth it", "worthwhile", "useful", "actually",
                                 "think", "opinion", "too much", "point", "benefit",
                                 "necessary", "effective", "any good", "helps")),
          "Homework earns its place in small doses: about ten minutes a night in the first years "
          "of primary, half an hour by the end of it and an hour or so at secondary, and the "
          "evidence for it is weakest for the youngest children. What makes it work is the same "
          "each night - a fixed time, a clear table, and you nearby without taking over. If it is "
          "regularly taking much longer than the school's own limit, or ending in tears, that is "
          "worth one short message to the teacher rather than a battle every evening.",
          ask=("homework", "home work", "homeworks"),
          bias=1,
          avoid=("how do i", "how to get", "get him to", "get her to", "get them to", "wont do",
                 "won t do", "refuses", "refusing", "refuse", "every night", "routine", "reward",
                 "chart", "sticker", "timetable", "times tables", "spelling", "maths", "english",
                 "revision", "revise", "exam", "concentrate", "focus", "adhd", "dyslex",
                 "teacher", "school said")),
    entry("past-papers",
          (("past paper", "past papers", "mock", "exam paper", "mark scheme"),
           ("how", "do", "use", "practice", "best", "worth", "marks", "when", "should", "start",
            "starting", "begin", "leave", "left", "soon", "many", "much", "often")),
          _past_papers_reply),
    entry("flashcards",
          (("flashcard", "flashcards", "anki", "quizlet"),
           ("how", "make", "use", "best", "worth", "many")),
          "One fact per card, question on one side, answer on the other, and no paragraphs: "
          "\"What year was the Battle of Hastings?\" not \"notes on 1066\". Review only the cards "
          "you get wrong, in short daily sessions, and make them yourself - writing them is half "
          "the memory work. Anki does the spacing for you if you prefer an app."),
    entry("mnemonics",
          (("mnemonic", "mnemonics", "memory trick", "remember a list"),
           ("how", "remember", "best", "use", "lists", "what", "whats", "mean", "meaning")),
          "Build a sentence from the first letters (Never Eat Shredded Wheat for the compass), "
          "or tie items to places on a walk round your house - the sillier the image, the better "
          "it sticks. Mnemonics are good for lists and orders, useless for understanding; use "
          "them for the facts you keep dropping."),

    entry("remember-names",
          (("names", "name", "forget names", "remembering names", "forget peoples names"),
           ("remember", "remembering", "forget", "forgetting", "keep forgetting", "how", "best",
            "trick", "tip", "tips", "help", "never", "cant remember", "can't remember")),
          "Use the name out loud in the first minute - \"Nice to meet you, Sarah\" - and hang it on "
          "something physical: alliteration (Tall Tom), a rhyme, or a face feature. Repeating it "
          "twice early beats any trick later, and if it has gone, say so straight away: \"Sorry, "
          "your name's gone\" costs less than guessing.",
          ask=("remember", "remembering", "forget", "forgetting", "keep forgetting", "how", "best",
               "trick", "tip", "tips", "help", "never", "cant remember", "can't remember"),
          guard=lambda understood: not _somebody_else_forgets(understood),
          avoid=("baby", "babies", "dog", "cat", "puppy", "kitten", "company", "business",
                 "domain", "website", "username", "password", "rename", "change my name",
                 "middle name", "surname", "spell my name", "write my name", "sign my name",
                 "film", "films", "movie", "movies", "song", "songs", "tune", "book", "books",
                 "novel", "show", "series", "actor", "actress", "band", "album",
                 "name our", "name the team", "name the quiz", "name the club",
                 "naming our", "team name", "team names", "quiz name", "quiz names",
                 "club name", "club names", "call our team", "call the team",
                 "call the quiz", "call our quiz", "call the club", "call our club",
                 "needs a name", "need a name", "name ideas", "name for our",
                 "names for our",
                 "dementia", "alzheimers", "alzheimer's", "sign of", "symptom", "worried",
                 "worry", "should i be concerned", "is it normal")),
    entry("memorise-dates",
          (("dates", "timeline", "history"),
           ("remember", "memorise", "memorize", "learn", "keep forgetting")),
          "Put the dates on a blank timeline you draw yourself, and group them around a few "
          "anchor events you already know. Then link each new date to a story or a person rather "
          "than a bare number, and test yourself by covering the dates and filling them in. Ten "
          "dates you can place beat fifty you half-remember.",
          avoid=("my wife", "my husband", "my partner", "our dates", "our anniversary",
                 "our plans", "marriage")),
    entry("fraction-meaning",
          (("fraction", "fractions", "numerator", "denominator", "decimal"),
           ("what", "whats", "mean", "meaning", "definition", "is a", "are")),
          "A fraction is a part of a whole written as one number over another: the bottom says "
          "how many equal pieces the whole is cut into and the top says how many of those you "
          "have, so 3/4 is three pieces out of four. The one thing that trips people up is that "
          "the same amount has lots of names - 2/4 is 1/2, and 0.5 is 1/2 too - which is why you "
          "can simplify and compare them by putting them over the same bottom number.",
          avoid=("minutes", "seconds", "as a fraction", "in a fraction", "out of", "of my",
                 "of the", "fraction of an hour is", "fraction of a day is",
                 "fraction of a week is", "fraction of a minute is"),
          bias=1),
    entry("fractions-explain",
          (("fraction", "fractions", "numerator", "denominator"),
           ("explain", "simple", "simply", "struggling", "understand", "child", "son", "daughter",
            "kid", "teach", "help")),
          "Start with something they can eat: cut an apple into four, take one piece - that is "
          "one quarter. Then show that the bottom number is how many pieces the whole was cut "
          "into and the top is how many you have. Do halves, quarters and thirds with real "
          "objects before any writing, then move to drawing them as bars of chocolate.",
          bias=1),
    entry("times-tables",
          (("times tables", "times table", "multiplication", "times by", "6 times 7"),
           ("learn", "memorise", "remember", "how", "help", "child", "quick")),
          "Do them out loud, in order, then shuffled, in two-minute bursts a few times a day - "
          "short and often beats long and rare. Learn the easy ones first (2s, 5s, 10s, then the "
          "squares) so more than half the table is familiar. The hard ones are 6x7, 7x8, 8x9; "
          "make up a silly rhyme for just those.",
          bias=1),
    entry("long-division",
          (("long division", "division", "divide", "dividing",
            "short division", "bus stop method", "bus stop", "remainder", "remainders"),
           ("explain", "teach", "simple", "simply", "method", "child", "year old", "works",
            "stuck", "remember", "steps", "step by step", "by hand", "without a calculator",
            "show me", "work out", "help",
            "do long division", "long division method", "learn", "homework", "practice",
            "practise",
            "how do i do", "how do you do", "how to do", "what is", "whats", "mean",
            "meaning", "big number", "big numbers")),
          "Long division is the same four steps over and over: divide, multiply, subtract, bring "
          "down. Take 492 divided by 4: 4 goes into 4 once (write 1), 1 x 4 = 4, subtract to get 0, "
          "bring down the 9. 4 into 9 goes twice (write 2), 2 x 4 = 8, 9 - 8 = 1, bring down the 2 "
          "to make 12. 4 into 12 is 3, so the answer is 123. Say each step out loud the first few "
          "times, and use real objects for the first example so the place value makes sense.",
          avoid=("decimal", "decimals", "3 by 8", "as a decimal", "two decimal places",
                 "bill", "bills", "chores", "pizza", "taxi", "rent", "custody", "excel",
                 "spreadsheet", "formula", "assets", "inheritance", "profits", "bonus",
                 "holiday", "money between", "between us", "dividing up")),
    entry("fractions-sums",
          (("fraction", "fractions"),
           ("multiply", "multiplying", "multiplied", "times", "divide", "dividing",
            "divided", "add", "adding", "subtract", "subtracting", "plus", "minus",
            "common denominator", "same denominator", "simplify", "cancel down")),
          _fractions_reply,
          avoid=("decimal", "decimals", "percent", "percentage", "percentages", "what is a",
                 "whats a", "mean"),
          bias=1),
    entry("maths-word-problems",
          (("word problem", "word problems", "maths problem", "maths question"),
           ("solve", "how", "stuck", "approach", "help", "cant")),
          "Underline what the question actually asks, then write down the numbers it gives you "
          "and what units they are in. Guess the answer roughly before calculating - if your "
          "working is far off the guess, the sum is wrong, not the guess. Draw it if there is "
          "any shape, distance or time in it."),
    entry("science-project-build",
          (("volcano", "volcanoes", "model volcano", "volcano model"),
           ("build", "make", "model", "ideas", "school", "project", "science project",
            "school project", "kids", "child", "daughter", "son", "erupt", "erupts",
            "eruption", "explain", "why", "how")),
          "For a volcano: a bottle in a cone of foil and clay, then bicarbonate of soda with "
          "vinegar and a little washing-up liquid for the eruption (red food colouring helps). "
          "The part that earns marks is the write-up: label the bottle as the magma chamber, and "
          "explain that the gas is what pushes it out. It takes an afternoon and a tray.",
          avoid=("timeline", "gantt", "project plan", "deadline", "schedule", "sprint", "client",
                 "stakeholder", "at work", "for work", "milestone", "roadmap",
                 "what makes", "what causes", "which makes", "that makes", "causes it",
                 "the cause", "the reason")),
    entry("spelling-test",
          (("spelling test", "spelling bee", "spellings", "spelling list", "weekly spellings",
            "cant spell", "can't spell", "cannot spell", "bad at spelling", "struggles to spell",
            "struggle to spell", "spelling"),
           ("daughter", "son", "child", "kid", "kids", "practise", "practice", "help", "how",
            "ready", "test", "school", "ten words", "prepare")),
          "Five words a night, not the whole list: look at the word, say it, cover it, write it, "
          "then check it, and put the ones she gets wrong to the back of the queue. Say the word "
          "in a sentence as you test her, because a spelling she can only write in a list is not "
          "learnt yet. Ten minutes is enough, and the night before is for the five she keeps "
          "missing, not for the twenty she knows.",
          avoid=("how do you spell", "how do i spell", "how to spell", "spell the word",
                 "spell it", "spelling of", "improve", "improving"),
          bias=2),
    entry("essay-plan",
          (("essay", "coursework", "assignment"),
           ("plan", "start", "stuck", "blank", "deadline", "how", "write", "writing")
           + HOW_ASK),
          "Make the plan first and write the essay from it: list three or four points that answer "
          "the question, put one piece of evidence under each, and put them in the order that "
          "makes the argument grow. Then write the body paragraphs first and the introduction "
          "last, when you know what you argued. Two hours of planning saves a day of staring.",
          avoid=("mistakes", "mistake", "grammar", "spell", "spelling", "proofread", "typo",
                 "typos", "check", "unclear", "structure of the sentence")),
    entry("proofread-help",
          (("spell check", "spellcheck", "proofread", "proof read", "check this email",
            "check my email", "check this essay", "check my essay", "check my cv"),
           ("can", "could", "you", "please", "how", "help", "this", "my")),
          "I cannot read it for you, but the check that catches most of it is reading it aloud: "
          "your ear stops on the missing word and the doubled one. Then look at four things in "
          "order - the name at the top, the ask in the first line, any number or date, and the "
          "last line. Shorten any sentence you have to read twice, and leave it for ten minutes "
          "before the last read if you can.",
          avoid=("essay", "essays", "dissertation", "coursework", "assignment", "thesis")),
    entry("reading-comprehension",
          (("comprehension", "reading", "passage"),
           ("understand", "answer", "questions", "help", "improve", "exam", "better",
            "get better", "struggling", "weakest")),
          "Read the questions before the passage, so you know what to look for. Then read once "
          "for sense and go back to the lines the questions point at, quoting a few words in your "
          "answer. For \"why\" questions, answer with because plus something from the text; for "
          "\"how do you know\", quote it.",
          avoid=("my son", "my daughter", "my kid", "my child", "bedtime", "learn to read",
                 "read to me", "reading age", "phonics", "sounding out",
                 "music", "sheet music", "sight read", "sight-read", "sight reading")),
    entry("reading-with-a-child", (("reading", "read", "books", "phonics"),
                                   ("my son", "my daughter", "my kid", "my child", "bedtime",
                                    "learn to read", "reading age", "every night", "refuses",
                                    "reluctant", "help him", "help her",
                                    "count as reading", "counts as reading", "count as a book",
                                    "reading practice", "reading practise", "ok for reading",
                                    "good for reading", "for reading practice")),
          "Ten minutes a night, the same time, with them reading out loud to you: stop at the "
          "first hard word, sound it out together, and let them finish the sentence. Read the "
          "same short book twice, because the second read is where the confidence comes from, "
          "and keep a book in the car or bag for dead time. Ask one question about the story "
          "afterwards rather than testing words.",
          avoid=("my eyes", "eyes hurt", "eyes ache", "eyes are sore", "eye strain", "eyestrain",
                 "in bed", "my eyesight", "tired eyes", "sore eyes",
                 "music", "sheet music", "sight read", "sight-read", "sight reading",
                 "notation", "an instrument", "piano", "guitar", "violin")),
    entry("a-comic-counts-as-reading",
          (("count as reading", "counts as reading", "count as a book", "count as books",
            "still reading", "proper reading"),
           ("comic", "comics", "comic book", "comic books", "graphic novel", "graphic novels",
            "manga", "audio book", "audio books", "audiobook", "audiobooks", "magazine",
            "magazines", "picture book", "picture books", "kindle", "e-reader", "ereader")),
          "Yes, it counts. Comics, graphic novels, magazines and audio books all build the same "
          "thing a book does - the habit and the vocabulary - and a child who reads what they like "
          "reads far more of it than one handed a book they do not. Keep one chapter book alongside "
          "it rather than banning the comics, and ask what happened in the story afterwards. For "
          "audio books, same idea: the words go in by ear, and a paper copy of the same book helps "
          "once they can follow along.",
          bias=1),
    entry("study-breaks",
          (("pomodoro", "study breaks", "study break", "how long should i study", "how long to study",
            "breaks when studying"),
           ("how", "long", "often", "best", "study", "studying", "revision", "technique",
            "method", "mean", "work")),
          "25 minutes on, 5 off, and a longer break every four blocks: the short block keeps "
          "quality up, the break is what makes it repeatable. In the break, stand up and move "
          "rather than scrolling, because a phone break turns five minutes into twenty. Stop "
          "while it is still going well, so tomorrow is easier to start.",
          avoid=("instructions", "assembling", "manual", "recipe", "flat pack", "flatpack",
                 "how long should i study", "how long should i revise", "how many hours"),
          bias=1),
    entry("study-with-adhd",
          (("adhd", "attention deficit"),
           ("study", "revise", "focus", "concentrate", "help", "tips")),
          "Make the task visible and small: one page, one timer, everything else out of the room. "
          "Body-doubling works for a lot of people - study alongside someone, in person or on a "
          "video call with mics off. Move between two or three subjects rather than forcing one, "
          "and use a paper checklist you tick, because visible progress is the fuel."),
    entry("motivation-to-study",
          (("motivation", "motivated", "pointless", "cant be bothered", "no point"),
           ("study", "revise", "school", "exam", "how", "help", "why")),
          "Motivation follows action, not the other way round: do ten minutes and decide after. "
          "Pick the subject you least dread but find easiest to start with, because a bad day is "
          "about getting one thing done, not all of it. If it has felt pointless for weeks, tell "
          "someone at school or work; that is a different problem from laziness."),
    entry("learn-to-the-test",
          (("learn", "memorise"),
           ("fast", "quickly", "overnight", "in a day", "last minute", "exam")),
          "Last-minute learning works for facts and structures, not skills: take the syllabus or "
          "mark scheme, list what is actually examinable, and learn the highest-mark items with "
          "self-testing. Sleep before the exam and skip the things you already know. Be honest "
          "with yourself - this buys a pass, not understanding.",
          avoid=LANGUAGE_LEARNING + ("the job", "my job", "new job", "the role", "my role",
                                     "at work", "on the job", "job quickly", "the ropes",
                                     "ropes", "up to speed")),
    entry("stop-cramming",
          (("cram", "cramming", "crammed", "all nighter", "all-nighter", "all-nighters",
            "last minute revision", "last-minute revision", "leave it to the last minute",
            "leaving it late", "leaving everything", "leaving revision"),
           ("stop", "stops", "how", "help", "tips", "avoid", "not", "always", "every",
            "why", "end up", "keep")),
          "Make the first session tiny and today: open the topic list, pick the one you know "
          "least, and test yourself on it for ten minutes, because starting is the part that is "
          "failing rather than the studying. Then put three short sessions in the week you "
          "actually have, each ending with a self-test instead of a reread, and give each one a "
          "stopping time so it cannot drift to midnight. Testing yourself is what makes the last "
          "day calm instead of terrible; if the exam is tomorrow, pack the bag, read your "
          "one-page summary once, and sleep.",
          avoid=("no sleep", "bad sleep")),
    entry("practise-a-talk",
          (("practise", "practice", "practising", "practicing", "rehearse", "rehearsal",
            "rehearsing", "run through", "run it through", "go through it out loud"),
           ("presentation", "talk", "speech", "pitch", "slides", "audience", "wedding",
            "best man", "bride", "groom", "interview", "assembly", "meeting", "conference")),
          "Say it out loud three times, standing up, with the slides in front of you: the first "
          "run finds the sentences that only looked fine on paper, the second is against a timer, "
          "and the third is to one person who will tell you where they lost the thread. Time it "
          "against the slot you were given and cut material rather than speed up. Write the "
          "opening sentence and the closing one out in full and keep everything between them to a "
          "few words per card, then practise stopping for a second after your last point instead "
          "of trailing off.",
          bias=1),
    entry("group-project",
          (("group project", "group work", "team project", "presentation with", "work in a group",
            "work well in a group", "work as a group", "group of us", "work with a group"),
           ("how", "help", "lazy", "fair", "split", "work", "handle")),
          "At the first meeting, split the work in writing with names and dates, and pick one "
          "person to hold the whole thing together. Swap drafts before the deadline so no one is "
          "the bottleneck. If someone does nothing, tell them early what you need by when; "
          "chasing at the end is where the resentment comes from."),
    entry("teach-someone",
          (("explain it to someone", "teach someone", "teach it to someone", "teaching someone",
            "feynman"),
           ("how", "best way to learn", "understand", "check", "learn")),
          "Explain it out loud to someone who does not know it, without notes. Where you stumble "
          "or reach for jargon is exactly what you do not understand yet, so go back to that bit "
          "and try again. Ten minutes of teaching yourself in the mirror is worth an hour of "
          "rereading."),
    entry("grade-meaning", (("grade", "grades", "gcse", "gcses", "a level", "a-level",
                            "alevel", "alevels", "marks", "score"),
                           ("1", "2", "3", "4", "5", "6", "7", "8", "9", "bad", "good",
                            "mean", "pass", "passed", "average", "standard", "decent",
                            "changed", "compare")),
          _grade_answer, avoid=NOT_AN_EXAM + MOCK + (
                                                     "credit score", "credit rating", "credit file",
                                                     "credit report", "credit history",
                                                     "piano", "guitar", "violin", "ballet",
                                                     "dance", "swimming", "abrsm", "trinity",
                                                     "instrument", "music", "singing", "choir",
                                                     "theory test", "driving test",
                                                     "football", "rugby", "netball", "cricket",
                                                     "hockey", "team", "league", "club",
                                                     "martial arts", "karate", "judo"), bias=2),
    entry("mock-grade", (MOCK,
                         ("1", "2", "3", "4", "5", "6", "7", "8", "9", "grade", "grades",
                          "bad", "good", "mean", "worried", "worry", "failed", "gutted",
                          "matter", "count", "what should")),
          _mock_answer, avoid=NOT_AN_EXAM, bias=2),
    entry("revision-start", (("revising", "revise", "revision", "exam", "exams", "test", "mocks",
                              "mock"),
                             ("putting off", "procrastinat", "get started", "started", "start",
                              "begin", "behind", "timetable", "schedule", "overwhelmed",
                              "how", "tips", "advice", "best", "help", "should", "weeks",
                              "soon", "coming",
                              "prepare", "preparing", "prep", "get ready",
                              "havent revised", "havent started", "havent done", "havent begun",
                              "not revised", "not started", "not begun", "no revision",
                              "done nothing", "nothing yet", "done none", "havent touched",
                              "havent opened", "left it", "left everything", "not done any",
                              "in two days", "in 2 days", "in three days", "in 3 days",
                              "in a few days", "days time", "days left", "run out of time",
                              "no time")),
          _unless_testing_a_thing(
              "Start with something tiny today: open the past paper or the topic list and write "
              "down what you already know about one topic — ten minutes, that is the whole job. "
              "Then work backwards from the exam date and give each topic a day, in 25-minute "
              "blocks with a 5-minute break. The last week should be past papers under time, not "
              "reading notes."),
          avoid=NOT_AN_EXAM + NOT_REVISION + ASLEEP + REST_ASK
          + ("time of day", "what time", "best time", "better time", "when is the best",
             "at night or", "or in the morning", "or in the evening", "in the morning or",
             "morning or night", "night or morning", "evening or morning", "morning or evening")
          + NOT_A_START_OF_EXAMS,
          bias=1),
    entry("revision-active", (("revising", "revise", "revision", "studying", "study",
                               "revision notes", "make revision notes", "revision methods",
                               "revision techniques"),
                              ("remember", "sticks", "stays", "stuck", "head", "brain",
                               "memory", "memorise", "memorize", "reread", "rereading",
                               "notes", "method", "technique", "effective", "how", "tips",
                               "best", "help") + HOW_ASK),
          "Testing yourself is what makes things stick; rereading notes mostly feels productive "
          "without being so. Turn each topic into five questions and answer them with the book "
          "shut, then check, and redo the ones you got wrong tomorrow and again in a week. "
          "Reread only the bits you could not answer.",
          avoid=NOT_AN_EXAM + NOT_REVISION + ASLEEP + REST_ASK + A_SUBJECT
          + ("time of day", "best time", "better time", "what time", "when is the best")
          + NOT_A_START_OF_EXAMS, bias=1),
    entry("revision-method-names", (("active recall", "spaced repetition", "spaced practice",
                                     "retrieval practice", "testing yourself", "interleaving",
                                     "blurting", "leitner"),
                                    ("what", "whats", "mean", "means", "is", "explain", "about",
                                     "definition", "define", "work", "does", "do")),
          "Testing yourself is what makes things stick; rereading notes mostly feels productive "
          "without being so. Turn each topic into five questions and answer them with the book "
          "shut, then check, and redo the ones you got wrong tomorrow and again in a week. "
          "Reread only the bits you could not answer.",
          bias=1),
    entry("study-time-of-day", (("study", "studying", "revise", "revising", "revision"),
                                 ("morning", "night", "evening", "time of day", "better time",
                                  "best time", "best time to", "best time of day", "good time",
                                  "right time", "when in the day", "what time of day",
                                  "what time", "which time", "what hour",
                                  "when")),
          "The time you will actually do it beats the perfect time, and for anything that needs "
          "concentration most people are sharper in the morning. Hard topics first, drilling and "
          "past papers later, and keep the last half hour before bed off screens if you can. If "
          "you are a night owl and it works, do not fight it — just do it at the same time each day.",
          avoid=NOT_AN_EXAM + ASLEEP + ("shift", "shifts", "rota", "work nights",
                                        "night shift")),
    entry("vocab-test", (("vocabulary", "vocab", "words"),
                         ("remember", "learn", "memorise", "memorize", "test", "language",
                          "french", "spanish", "german", "italian")),
          "Learn seven to ten words at a time, out loud, and test yourself instead of reading the "
          "list: cover the English side and say the word, then swap. Put each new word in a short "
          "sentence you would actually say, and go back over yesterday's words for two minutes "
          "before adding new ones — spacing is what makes them stay.",
          guard=lambda understood: not _somebody_else_forgets(understood),
          avoid=NOT_AN_EXAM + ASLEEP, bias=1),
    entry("exam-night-before", (("exam", "exams", "test"),
                                ("night before", "tomorrow", "cram", "cramming", "evening",
                                 "sleep", "bedtime")),
          "Sleep is worth more than the extra hours of cramming: a rested brain recalls what you "
          "already know, a tired one does not. Pack your bag and the pens you need, read your "
          "one-page summary once, then stop by nine and do something that is not revision. If you "
          "really cannot settle, write down the three things you are worried about forgetting.",
          avoid=NOT_AN_EXAM, bias=1),
    entry("exam-nerves", (("exam", "exams", "test"),
                          ("nervous", "nerves", "nerve", "panic", "panicking", "blank", "anxious",
                           "freeze", "freaking", "scared", "stress", "stressed", "dread",
                           "dreading", "worried",
                           *NERVES_BODY)),
          _exam_nerves,
          bias=1,
          avoid=NOT_AN_EXAM),
    entry("exam-day-food", (("exam", "exams", "test", "tests", "mock", "mocks",
                            "exam day", "exam morning"),
                           ("eat", "eating", "ate", "food", "breakfast", "lunch", "drink",
                            "drinking", "water", "snack", "snacks", "coffee", "caffeine",
                            "hungry", "sugary", "energy drink")),
          "Something slow and ordinary an hour or two before, with water: porridge, toast and egg, "
          "or cereal and a banana. A sugary breakfast spikes and drops you by the second hour, "
          "which is exactly when the paper gets hard, so keep the sweet thing for the break. Take "
          "a bottle of water and a plain snack in, and if the exam is in the afternoon eat a light "
          "lunch rather than a big one - a full stomach is what makes people sleepy at 2pm. Keep the "
          "coffee you usually drink and nothing more: a double espresso you never have "
          "is what sends people to the loo twice in the first half hour.",
          avoid=NOT_AN_EXAM
          + ("blood", "diabetes", "diabetic", "my diet", "lose weight", "thinking of food",
             "overeating", "appetite", "nausea", "sick", "vomit", "allergic", "allergy",
             "bring water", "take water", "into the exam", "into an exam", "allowed in",
             "bring in", "take in"),
          bias=2),
    entry("essay-opening", ("essay", ("opening", "first sentence", "first line", "introduction",
                                      "start", "begin", "sentence", "hook")),
          "Answer the question in your first sentence, plainly, and let the rest of the essay back "
          "it up: \"Prisons in the 1800s did more to hide poverty than to fix it.\" No \"In this "
          "essay I will discuss\" and no dictionary definition — a marker wants to see your answer "
          "straight away.",
          avoid=NOT_AN_EXAM, bias=2),
    entry("essay-structure", ("essay", ("structure", "paragraph", "paragraphs", "conclusion",
                                        "argue", "argument", "organise", "organize")),
          "One idea per paragraph: a sentence that says what it argues, the evidence for it, then a "
          "line saying why that matters to the question. Your conclusion should answer the "
          "question as asked, not repeat the introduction. If you are stuck, write the paragraphs' "
          "first sentences as a list first and check they add up to an argument.",
          avoid=NOT_AN_EXAM, bias=1),
    entry("essay-check", ("essay", ("proofread", "check", "mistakes", "shorter", "word count",
                                    "edit", "cut", "improve")),
          "Read it out loud, or have your computer read it aloud: the places you stumble are the "
          "places to fix. Cut every \"very\", \"really\" and \"basically\", make sure each "
          "paragraph's first sentence says its point, and check names, dates and quotes — those "
          "are what get marked down.",
          avoid=NOT_AN_EXAM),
    entry("notes-lecture", (("note", "note-taking", "notetaking", "notes from"),
                            ("lecture", "lectures", "class", "lesson", "better", "take", "taking",
                             "handwriting", "laptop", "book", "books", "textbook", "textbooks",
                             "chapter", "chapters", "reading", "seminar",
                             "write", "writing", "good", "good notes")),
          "Write in your own words, in short lines, and do not try to transcribe: you are making a "
          "map to come back to, not a transcript. Leave a wide margin for questions after the "
          "lesson and add them the same evening, in five minutes, while it is still fresh. "
          "Handwriting beats typing for remembering, if it is a choice.",
          avoid=NOT_AN_EXAM + NOT_A_PERSONS_NOTE, bias=1),
    entry("study-distracted", (("focus", "focusing", "concentrate", "concentrating",
                                "concentrated", "distracted", "distraction", "concentration",
                                "mind wanders", "wanders", "zone out", "zoning out",
                                "lose track"),
                               ("study", "studying", "revising", "revision", "homework", "sit down",
                                "end up", "tiktok", "youtube", "better", "worse", "work",
                                "office", "job", "desk", "task", "tasks", "mind", "wanders",
                                "keep losing", "losing track", "get on with", "get anything",
                                "get distracted", "cant", "can t", "read", "reading", "book",
                                "books", "meeting", "meetings", "conversation")),
          "Put the phone in another room — not face down, another room — and work in 25-minute "
          "blocks with a 5-minute break where you get up. Before each block, write the one thing "
          "you will finish on a scrap of paper so you do not have to decide where to start. Same "
          "desk, same time, same little ritual helps more than willpower.",
          avoid=NOT_AN_EXAM + LOSING_TRACK_OF_MONEY,
          bias=2),
    entry("concentration", (("concentrate", "concentrating", "concentration", "focus",
                             "focusing", "focused", "distracted", "distracting",
                             "distraction", "wanders", "attention", "procrastination",
                             "procrastinating", "procrastinate"),
                            ("how do i focus", "how can i focus", "how do i concentrate",
                             "how can i concentrate", "how do i stay", "how do i keep",
                             "how do i improve", "how do i pay", "how do i stop",
                             "how do i beat", "better", "improve", "improving", "stay",
                             "keep", "cant", "cannot", "why", "help", "class", "mind",
                             "anything", "beat", "pay")),
          "Mostly it is the setup, not willpower: enough sleep, food, the phone in another "
          "room and one thing open at a time. Work in 25-minute blocks on a single task "
          "written down first, because choosing where to start is half the distraction, and "
          "stand up for the break. If your mind wanders when you read, take notes by hand and "
          "say the page back to yourself in one line at the end of it.",
          avoid=("camera", "lens", "autofocus", "photograph", "photo", "diet", "weight",
                 "good things", "road", "driving", "meeting", "meetings"),
          bias=-1),
    entry("learn-language-daily", (("learning", "learn", "learnt", "study", "picking up",
                                   "memorise", "memorize", "memorising", "memorizing",
                                   "fluent", "fluency", "fluently", "speak", "speaking"),
                                   ("language", "spanish", "french", "italian", "german",
                                    "portuguese", "japanese", "chinese", "welsh", "korean",
                                    "russian", "arabic", "dutch", "greek", "polish")),
          "Split your time in three: a few minutes going over yesterday's phrases out loud, most "
          "of it on new phrases said aloud and written down once, and a few minutes listening to "
          "something short at normal speed. Learn whole phrases you will use rather than grammar "
          "tables, and speak from the first week — even to yourself in the kitchen. One lesson or "
          "one conversation partner a week is what makes the rest work.",
          avoid=NOT_AN_EXAM, bias=1),
    entry("pick-a-language",
          (("which language should", "what language should", "language should i",
            "languages should i", "what language to", "which language to", "what language do i",
            "which language do i", "best language to", "easiest language to",
            "hardest language to", "good language to", "useful language to",
            "most useful language", "language worth", "languages worth",
            "which language is", "what language is", "pick a language", "choose a language",
            "which language first", "what language first", "easiest language",
            "hardest language", "best language"),
           ("learn", "learning", "learnt", "study", "studying", "pick", "picking", "choose",
            "choosing", "start", "starting", "first", "worth", "recommend",
            "english speaker", "english speakers")),
          "Pick by what you will actually use it for, not by which is easiest on paper: the "
          "language of the country you visit, or of the family you are marrying into, beats any "
          "ranking. With no reason to choose, Spanish is the usual bet - about 500 million "
          "speakers, spelling that matches the sound, and a lot of cheap material - and if you "
          "already have French or Italian, the other one of the pair is the cheapest start of "
          "all. The clock is the real cost: about 600 to 750 hours of class for Spanish, French "
          "or Italian, but roughly 2,200 for Arabic, Chinese, Japanese or Korean.",
          avoid=NOT_AN_EXAM + ("say", "says", "saying", "pronounce", "translate", "translation",
                               "phrase", "phrases", "speak", "speaks", "speaking", "spoken",
                               "in spanish", "in french", "in italian", "in german",
                               "in welsh", "in irish", "in gaelic", "in portuguese",
                               "sign language", "duolingo", "app", "apps", "lesson", "lessons",
                               "class", "classes", "course", "courses", "gcse", "a level",
                               "a-level", "degree", "university", "abroad", "moving to",
                               "live in", "holiday", "my child", "my son", "my daughter"),
          bias=2),
    entry("language-hours",
          ((LANGUAGE_LEARNING + ("learn", "learning", "learnt", "learned", "become fluent",
                                "get fluent", "pick up")),
           ("long", "hours", "years", "months", "weeks", "until", "soon", "time")),
          _language_hours,
          ask=("how long", "how many hours", "how many years", "how many months",
               "how many weeks", "how soon", "how much time", "how long until", "how long till",
               "how long before", "until i'm", "until im", "to become", "does it take"),
          avoid=NOT_AN_EXAM + ("a week", "per week", "each week", "every week", "hours a week",
                               "how often", "sign language", "translate", "translation",
                               "pronounce", "pronunciation", "spell", "spelling", "grammar",
                               "lesson", "lessons", "class", "classes", "course", "courses",
                               "app", "apps", "duolingo", "gcse", "a level", "a-level",
                               "ielts", "degree", "university",
                               "have you been", "did it take you", "you been",
                               "how long have you"),
          guard=_names_a_language,
          bias=2),
    entry("trip-phrases", (("phrases", "phrasebook"),
                           ("learn", "before", "holiday", "trip", "italy", "spain", "france",
                            "language", "useful")),
          "Learn these twelve and you can get through most of a holiday: hello, goodbye, please, "
          "thank you, sorry, excuse me, do you speak English, I don't understand, how much is this, "
          "the bill please, where is the toilet, and help. Say them out loud until they are "
          "automatic, because under pressure you will use what you can say without thinking.",
          avoid=NOT_AN_EXAM),
    entry("say-language", (("say", "pronounce", "translate", "translation"),
                           ("spanish", "french", "italian", "german", "espanol", "español",
                            "francais", "français", "italiano", "deutsch",
                            "portuguese", "portugues", "português", "greek", "turkish",
                            "japanese", "chinese", "mandarin", "dutch",
                            "welsh", "cymraeg", "irish", "gaeilge", "gaelic")),
          _say_in_language, avoid=NOT_AN_EXAM, guard=_a_phrase_is_asked, bias=3),
    entry("say-welsh-irish", (("say", "pronounce", "translate", "translation",
                               "whats", "what is", "what's"),
                              ("welsh", "cymraeg", "wales", "irish", "gaeilge")),
          _say_in_language, avoid=NOT_AN_EXAM, guard=_a_phrase_is_asked, bias=3),
    entry("say-language-phrase", (("spanish", "french", "italian", "german", "espanol", "español",
                                   "francais", "français", "italiano", "deutsch",
                                   "welsh", "cymraeg", "irish", "gaeilge", "gaelic"),
                                  CONCEPT_WORDS,
                                  ("whats", "what is", "what's", "how", "i need", "translate",
                                   "actually", "instead", "make that", "not", "no", "then",
                                   "what about", "about", "or", "rather", "i mean", "mean")),
          _say_in_language, avoid=NOT_AN_EXAM, guard=_a_phrase_is_asked, bias=2),
    entry("what-does-that-mean", (("mean", "means", "meaning", "what does", "whats"),
                                  tuple(sorted(NATIVE))),
          _what_does_it_mean,
          ask=("mean", "means", "meaning", "translate", "translation", "stand for",
               "stands for", "what does it say", "in english"),
          avoid=("i mean", "i meant", "meaning to say"),
          bias=1,
          guard=_a_word_is_being_asked_about),
    entry("subjects-choose", (("choose", "choosing", "pick", "picking"),
                              ("a-levels", "alevels", "a levels", "gcses", "subjects", "degree",
                               "course", "university", "college")),
          "Pick the subjects you will still work at on a bad week, then check the entry "
          "requirements for two or three courses you might want later, because that is what closes "
          "doors rather than the subjects themselves. Keeping one essay subject and one numerical "
          "one keeps more options open than people expect. Ask a teacher you trust what they think "
          "you would enjoy, not just what you are good at.",
          avoid=NOT_AN_EXAM),
    entry("university-worth", (("university", "uni", "degree"),
                               ("worth", "going", "go", "should", "apprenticeship", "debt",
                                "better",
                                "need", "needed", "necessary", "alternative", "alternatives",
                                "without a degree")),
          "It depends on what you want to do: for nursing, engineering, law or teaching the degree "
          "is the door, and for plenty of other jobs experience gets you further for less money. "
          "Compare a degree with a degree apprenticeship in the same field — earn while you learn, "
          "no fees — and look at what people actually doing the job you want studied. Ask two of "
          "them before deciding.",
          avoid=NOT_AN_EXAM + _A_DEGREE_OF_HEAT),
    entry("apprenticeship-worth",
          (("apprenticeship", "apprenticeships", "apprentice", "degree apprenticeship",
            "higher apprenticeship", "level 2 apprenticeship", "level 3 apprenticeship"),
           ("worth", "worth it", "should", "paid", "pay", "pays", "earn", "earning", "money",
            "wage", "wages", "much", "better", "instead", "uni", "university", "degree", "what",
            "whats", "good")),
          "An apprenticeship is a paid job with the training built into the week: most of the "
          "time you work, about a fifth of it you study, and there are no tuition fees. They run "
          "from GCSE level up to degree apprenticeships in engineering, digital, nursing and "
          "accountancy, so one can stand in place of a degree - you earn while you learn and "
          "finish with experience and no student debt, but with less choice of where you study. "
          "Pay is at least the apprentice minimum wage and more on most schemes.",
          avoid=NOT_AN_EXAM + ("apply", "applying", "get one", "get an", "get a", "how do i get",
                               "how to get", "find one", "find an", "where do i", "search",
                               "become an", "become a", "start one", "start an", "vacancies",
                               "vacancy", "looking", "look for", "start looking")),

    entry("results-day", (("results", "grades", "gcse", "gcses", "a-level", "a level",
                           "a levels", "alevels"),
                          ("didn't", "didnt", "bad", "worse", "failed", "disappointed", "resit",
                           "clearing", "not what", "missed", "offer", "rejected", "options",
                           "now what")),
          "First, it is not the end of anything: there are more routes from here than there were "
          "before results day. If you have missed a university offer, ring the university "
          "yourself today — courses take people who call — and look at Clearing the same afternoon. "
          "For school exams, ask about a remark and about resitting in November or next summer; "
          "both are normal and neither sets you back a year if you use the time.",
          avoid=NOT_AN_EXAM + MOCK, bias=1),
    entry("study-procrastinate", (("procrastinat", "put off", "putting off", "put it off",
                                   "put things off", "cant start", "can't start", "cannot start",
                                   "keep putting", "get started", "get going"),
                                  ("study", "studying", "revising", "revision", "homework",
                                   "essay", "uni", "university", "college", "school", "coursework",
                                   "dissertation", "thesis", "assignment", "reading", "deadline",
                                   "stop")),
          "Do the smallest possible first step, not the whole job: open the book at the page and "
          "write the title and today's date, or set a timer for five minutes and let yourself do "
          "it badly. Putting it off is mostly about the task feeling too big to start, and it "
          "shrinks as soon as you are in it. Decide tonight what tomorrow's first step is, so "
          "then it is an instruction to follow rather than a choice to make.",
          avoid=NOT_AN_EXAM + ("exam", "exams", "gcse", "gcses", "a-level", "a levels", "mocks",
                               "mock", "test", "tests"),
          bias=2),
    entry("thesis-statement", (("thesis statement", "topic sentence", "thesis"),
                               ("what", "write", "how", "example", "essay", "introduction",
                                "start", "good", "should", "my")),
          "A thesis statement is one sentence that says the claim your essay will prove, and why it "
          "matters: \"Cheaper public transport would cut city emissions more than electric cars, "
          "because most journeys are short.\" Put it at the end of your first paragraph, make it "
          "something a reasonable person could disagree with, and check that every paragraph after "
          "it is evidence for that one sentence. If a paragraph is not, either cut it or change the "
          "thesis.",
          avoid=("phd", "masters", "supervisor", "submitted", "binding", "library")),
    entry("study-timetable", (("timetable", "revision timetable", "schedule", "planner",
                               "spreadsheet", "plan", "planning"),
                              ("revision", "revise", "revising", "exam", "exams", "subject",
                               "subjects", "study", "studying", "gcse", "gcses", "a-level",
                               "a levels", "mocks")),
          "Count the days you actually have (sleep and school nights are not revision), list the "
          "topics per subject, and give each topic one block rather than one subject one day: three "
          "blocks a day is a real day's work. Put the subject you dread first, in the morning. "
          "Leave the last three days for past papers under time, and leave one day empty, because "
          "something always slips.",
          avoid=NOT_AN_EXAM, bias=2),
    entry("study-how-long", (("study", "studying", "revise", "revising", "revision", "homework"),
                             ("how long", "how many hours", "hours", "long", "blocks", "pomodoro",
                              "breaks", "break",
                              "take a break", "take breaks", "a break from", "break from",
                              "break between", "breaks between", "how often break",
                              "how often should i break", "how long a break",
                              "how long should i break")),
          "About 25 to 45 minutes at a time, then a proper 5 to 10 minutes away from the desk: "
          "two or three hours of that is a good day, and four is a very long one. What counts is "
          "testing yourself in the block, not the hours you sat there. If you keep losing track, "
          "set a timer for the block and stop when it goes, even mid-sentence — stopping on a "
          "problem you can pick up again makes the next start easy.",
          avoid=NOT_AN_EXAM + NOT_REVISION
          + ("how long before", "how long until", "how far ahead", "how early",
             "weeks before", "months before", "days before", "how long do i need",
             "how long does it take to revise", "how long should i revise for the exam"),
          bias=2),
    entry("homework-amount",
          (("homework", "home work"),
           ("how much", "much homework", "how long should homework", "how many minutes",
            "how many hours of homework", "how long homework")),
          "Most primary homework is 20 to 30 minutes a night by the last years at primary, and "
          "about an hour a night in year 7 and up, with a break part way. If a piece runs well "
          "past that, write a note to the teacher rather than pushing through it, because homework "
          "that takes an hour and ends in tears is usually the wrong homework.",
          avoid=("wont", "won't", "will not", "refuses", "refusing", "hates", "hate", "battle",
                 "fight", "fights", "fighting", "nightmare", "sit down", "every night",
                 "help", "struggling", "struggles", "routine", "table"),
          bias=1),
    entry("study-forgetting", (("forget", "forgetting", "forgot", "cant remember",
                                "can't remember", "wont stick", "won't stick", "doesnt stick",
                                "doesn't stick"),
                               ("revise", "revising", "revision", "study", "studying", "learn",
                                "learned", "learnt", "memory", "remember", "everything")),
          "That is normal and it has a fix: what you re-read fades in a day or two, and what you "
          "test yourself on comes back. Same day, look at the topic and cover it and say it out "
          "loud; then again after two days, after a week, and after a month. Turn each topic into "
          "five questions and keep them on cards, and go through yesterday's cards for two minutes "
          "before starting anything new.",
          ask=("revise", "revising", "revision", "study", "studying", "learn", "learned",
               "learnt", "exam", "exams", "test", "tests", "school", "college", "uni",
               "university", "homework", "re-read", "reread"),
          avoid=NOT_AN_EXAM),
    entry("revision-essay-subjects",
          (("english", "english literature", "english language", "english lit", "history",
            "geography", "psychology", "sociology", "economics", "business studies",
            "religious studies", "politics", "media studies", "classics", "law a level"),
           ("revise", "revising", "revision", "exam", "exams", "test", "tests", "failing",
            "fail", "failed", "behind", "bad at", "rubbish at", "struggling", "stuck", "how",
            "better", "improve", "improving", "marks", "grade", "grades")),
          "Essay subjects are learned by writing answers, not by reading the notes again: get "
          "the mark scheme for your board, write three timed past questions a week and plan the "
          "other two in a spider diagram. Mark your own answer against the criteria and count "
          "what you missed - a point you did not make, a quote, the evaluation sentence at the "
          "end - because the marks are in the structure as much as the knowledge. Learn five "
          "specific examples or quotes per topic rather than twenty vague ones, and keep them on "
          "cards: one named case with a date beats a paragraph about 'many historians'.",
          ask=("revise", "revising", "revision", "exam", "exams", "study", "studying", "learn",
               "school", "college", "a level", "a levels", "gcse", "gcses", "test", "tests",
               "how", "better", "failing", "fail", "behind", "help", "tips"),
          avoid=("browser", "browser history", "search history", "watch history", "clear my",
                 "delete my", "cookies", "cache", "incognito", "medical history", "family history",
                 "ancestry", "genealogy", "ancestors", "my gp", "symptoms",
                 "speak english", "speaking english", "pronounce", "pronunciation", "accent",
                 "learn english", "improve my english", "fluent", "english speaking",
                 "native speaker", "another language")),
    entry("revision-maths", (("maths", "math", "mathematics", "algebra", "geometry",
                              "trigonometry", "physics", "chemistry", "biology", "science",
                              "calculations"),
                             ("revise", "revising", "revision", "exam", "exams", "test", "learn",
                              "practise", "practice", "marks", "better", "how",
                              "failing", "fail", "failed", "fails", "struggling", "struggle",
                              "behind", "bad at", "rubbish at", "slipping", "stuck")),
          "Maths and the sciences are learned by doing, not reading: work through the examples with the book open, "
          "then close it and do them again, then do past papers with the mark scheme next to you. "
          "Mark them honestly and write down the topics that lost marks; those get redone three "
          "days later. Learn the formulas by using them in questions rather than copying them out "
          "ten times, and if a topic still will not work, ask a teacher or a classmate to watch you "
          "do one question.",
          avoid=NOT_AN_EXAM, bias=2),
    entry("memorise-lines", (("memorise", "memorize", "memorising", "memorizing", "learn by heart",
                              "off by heart", "learn lines", "my lines", "lines"),
                             ("speech", "poem", "lines", "script", "play", "part", "presentation",
                              "talk", "wedding", "words", "monologue")),
          "Split it into chunks of three or four lines and learn the first word of each chunk, "
          "because that is what you will forget first. Read the chunk aloud, look away and say it, "
          "then add the next chunk and say both; record yourself and listen while walking or "
          "washing up. Say the whole thing out loud twice a day and it settles in about a week.",
          avoid=NOT_AN_EXAM + ("opening line", "opening lines", "first line", "first words",
                               "opener", "icebreaker", "ice breaker", "hook", "joke", "jokes",
                               "funny")),
    entry("study-mornings", (("get up", "getting up", "get out of bed", "wake up", "waking up",
                              "mornings", "morning", "alarm"),
                             ("early", "study", "studying", "revise", "revising", "revision",
                              "5am", "6am", "before school", "before work")),
          "Put the alarm across the room, and set it for the same time every day including "
          "weekends, because a lie-in on Sunday is what makes Monday impossible. Be in bed eight "
          "hours before it, and leave the book open at the page the night before so the first ten "
          "minutes need no decision. Then get up when it rings: negotiating with yourself is the "
          "part that fails.", bias=3,
          avoid=("cant sleep", "can't sleep", "insomnia", "wont wake", "wakes me", "nap",
                 "tired all", "cant get up", "can't get up",
                 "dog", "dogs", "puppy", "puppies", "cat", "cats", "kitten", "kittens",
                 "pet", "pets",
                 "baby", "babies", "toddler", "toddlers", "child", "children", "kid", "kids",
                 "son", "daughter", "year old", "year olds", "year-old", "yr old", "yrs old",
                 "time of day", "better time", "best time", "morning or", "evening or",
                 "or evening", "or night", "or morning", "which is better", "what time of day",
                 "better at night", "better in the morning", "better in the evening",
                 "better in the day", "study better", "revise better", "really better",
                 "at night or", "or in the morning", "or in the evening", "or in the day",
                 "in the morning or", "in the evening or", "night or morning",
                 "evening or morning", "morning or night", "morning or in",
                 "sharper",
                 "feel", "feeling", "feels", "felt", "sick", "nauseous", "nausea",
                 "anxious", "anxiety", "panic", "panicky", "dread", "dreading",
                 "exhausted", "tired", "stress", "stressed", "worry", "worried",
                 "unhappy", "depressed", "miserable", "low mood")),
    entry("speech-opener",
          (("opening line", "opening lines", "first line", "first words", "opener", "openers",
            "icebreaker", "ice breaker", "one liner", "one-liner", "hook", "open my speech",
            "open a speech", "open my talk", "open a talk", "open my presentation",
            "open a presentation"),
           ("speech", "talk", "presentation", "toast", "audience", "room", "stage",
            "best man", "maid of honour", "wedding", "assembly", "work do", "leaving do")),
          "Ask the room something it already knows the answer to, or name the one detail everyone "
          "there has seen - \"hands up who has been handed a handbag and told to hold it\" - then "
          "wait a beat before your name. Keep it under ten seconds and make the joke about you "
          "rather than anyone in the room, and if nothing comes, open with the strangest real "
          "detail of the story instead of a joke.",
          avoid=("poem", "poems", "script", "play", "monologue", "card", "cards", "vows",
                 "eulogy", "thank you letter"),
          bias=1),
    entry("study-awake", (("awake", "tired", "sleepy", "nodding off", "drowsy", "exhausted",
                           "asleep", "falling asleep", "sleep"),
                          ("study", "studying", "revise", "revising", "revision", "homework",
                           "lecture", "class", "stay", "staying")),
          "Stand up and move for two minutes every half hour, drink water, and put a bright light "
          "on your face — sleepiness at a desk is often boredom plus warm air. Do the hardest thing "
          "first and leave the reading for when you are flagging. If you are falling asleep at 9pm "
          "you need sleep, not coffee: an early night and an hour in the morning beats two hours "
          "of fighting it.",
          avoid=NOT_AN_EXAM + ("homework battle", "battle over homework",
                               "battles over homework", "homework is a battle",
                               "homework every night", "every night is a battle",
                               "the homework battle"),
          bias=2),
    entry("homework-child", (("homework",),
                             ("son", "daughter", "child", "kid", "kids", "children", "teenager",
                              "wont", "won't", "refuses", "refusing", "refused", "battle",
                              "battles", "nightmare", "help", "struggling", "struggles",
                              "fights", "every night",
                              "year old", "years old")),
          "Same time and same table every night, twenty minutes then a break, and the phone in "
          "another room — the fight is usually about the phone and the sudden start, not the work. "
          "Sit nearby doing your own quiet job rather than over their shoulder, and only help when "
          "they ask. If it is still a battle after a week, tell the teacher what you are seeing: "
          "homework that takes an hour and ends in tears is usually the wrong homework.",
          ask=("wont", "won't", "refuses", "refusing", "refused", "hates", "battle", "battles",
               "fights", "fighting", "nightmare", "struggling", "struggles", "every night",
               "will not", "wont sit", "will not sit", "sit down", "get him to", "get her to",
               "get them to", "get my", "hates homework", "hate homework",
               "how do i help", "how can i help", "how to help", "how do i get him",
               "how do i get her", "what should i do about"),
          avoid=NOT_AN_EXAM + ("ok il try", "ok i'll try", "ill try that", "i'll try that",
                               "i will try that", "ok thanks", "thanks that helps",
                               "that helps", "will do", "ok will do", "sounds good",
                               "okay i will", "ok i will")),
    entry("essay-reference", (("reference", "references", "referencing", "cite", "citation",
                               "bibliography", "sources"),
                              ("essay", "book", "article", "website", "harvard", "style", "write",
                               "list", "how", "dissertation", "assignment", "coursework",
                               "sources")),
          "Every claim that is not yours needs the author, the year and the page, and every source "
          "you used goes in the list at the end: author, year, title, publisher (or URL and the "
          "date you looked at it). Use the exact style your course asks for — Harvard, APA and MLA "
          "differ — and copy the format from your course guide rather than from memory. Quote "
          "sparingly and put the page number in, because a quote without one is the thing markers "
          "flag.",
          ask=("essay", "assignment", "coursework", "dissertation", "university", "college",
               "school", "harvard", "apa", "mla", "book", "website", "article", "sources"),
           bias=1,
          avoid=NOT_AN_EXAM + ("job", "jobs", "application", "applications", "interview",
                               "interviews", "cv", "employer", "referee", "boss", "manager")),
    entry("learn-an-instrument-as-an-adult", (("piano", "guitar", "violin", "instrument",
                                               "instruments", "keyboard", "drums", "clarinet",
                                               "flute", "saxophone", "sax", "cello", "trumpet",
                                               "ukulele", "banjo", "recorder", "harmonica",
                                               "trombone", "viola", "double bass", "oboe",
                                               "bassoon", "harp"),
                                              ("adult", "adults", "learning", "learn", "taking up",
                                               "take up", "late", "start", "starting", "old")),
          ("It is not too late: adults pick up the theory faster than children, they just need "
           "shorter and more regular practice. Twenty minutes a day gets you a simple song in two "
           "or three months, and four chords in about a month. Have six lessons with a teacher "
           "first, so nobody has to unlearn your posture."),
          ask=("too old", "too late", "start", "starting", "take up", "taking up", "begin",
               "worth it", "should i", "can i", "advice", "think about")),
    entry("evening-course",
          (("evening course", "evening courses", "evening class", "evening classes",
            "night class", "night classes", "adult education", "adult course", "adult courses",
            "adult learning", "part time course", "part-time course", "part time degree",
            "part-time degree", "access course", "access to higher education",
            "college course", "community course", "evening college"),
           ("worth", "worth it", "hours", "how much work", "how much time", "how long", "start",
            "starting", "enrol", "enroll", "sign up", "beginner", "level", "fees", "fee", "cost",
            "commitment", "a week", "per week", "workload", "homework", "fit", "manage",
            "should i", "shall i", "can i", "do i need", "is it")),
          ("Most evening courses are two or three hours of class a week plus about the same again "
           "at home, so plan on one evening and four or five hours a week. Ask for the guided "
           "learning hours before you enrol, because the college has to publish them, and check "
           "the fee: in England, English and maths up to GCSE are free for anyone who does not "
           "already have them, and a first level 2 or 3 qualification is often free if you are "
           "under 23 or on a low income. At the open evening, ask what the last group went on to "
           "do - that is what tells you whether it is worth the year."),
          ask=("course", "courses", "class", "classes", "college", "adult", "evening", "night",
               "worth", "hours", "workload", "should i", "shall i", "is it worth"),
          bias=1,
          avoid=("essay", "essays", "coursework", "assignment", "dissertation", "exam", "exams",
                 "revision", "revise", "boil", "oven", "swim", "swimming", "running", "race",
                 "golf", "dinner", "meal", "online course", "free course online")),
    entry("learn-guitar-first-steps", (("guitar", "guitars", "ukulele", "bass guitar",
                                        "learning guitar", "play guitar"),
                                       ("start", "starting", "beginner", "first", "learn",
                                        "learning", "app", "apps", "lessons", "teacher",
                                        "cheap", "buy", "practice", "practise", "good way",
                                        "how do i")),
          "Buy a used acoustic from a shop that sets it up for you, 80 to 150 pounds: a 30 pound "
          "supermarket one sits too high off the neck, hurts your fingers and is why people stop "
          "after a fortnight. Practise fifteen minutes a day, not an hour once a week, and learn G, "
          "C, D and Em, which is most of the songs you already like. An app is fine for a month; "
          "six lessons after that fix your hands before the habits set.",
          avoid=("old", "late", "sell", "selling", "repair", "string", "strings", "broken",
                 "tuning", "amp", "amplifier"),
          ask=("how", "what", "which", "should", "is it", "is a", "is an", "any", "tip", "tips",
               "advice", "best", "good way", "worth", "start", "beginner", "cheap", "cost")),

    entry("handwriting", (("handwriting", "hand writing", "write neatly", "neat writing",
                           "messy writing", "illegible", "joined up writing", "cursive"),
                          ("improve", "better", "messy", "neat", "neater", "legible", "fix",
                           "practice", "practise", "slow", "read", "help", "child", "children",
                           "kid", "kids", "son", "daughter", "awful", "terrible", "bad", "poor",
                           "school")),
          "Slow down by about a third for a week and use lined paper: most messy handwriting is "
          "speed, not hand shape. Then pick the two or three letters you join badly (r, n, m and "
          "your a's) and copy a paragraph a day, ten minutes, saying each letter as you write it. "
          "Check the shelf: a pen with a grip you actually hold, sitting up with both feet down and "
          "the paper turned slightly. If it is a child, check the grip first - a fist grip or a "
          "thumb over the top makes neat writing almost impossible - and use a pencil long enough "
          "to reach the table."),

    entry('school-bag',
          (('school bag', 'schoolbag', 'book bag', 'backpack', 'rucksack',
            'bag for school', 'bag ready for school',
            'bag tidy', 'keep my bag', 'my bag tidy', 'my bag is a mess', 'bag is a mess',
            'in my bag', 'my bag is always', 'pack my bag', 'packing my bag', 'my bag packed',
            'organise my bag', 'organize my bag', 'sort my bag', 'sorting my bag'),
           ('tidy', 'tidy up', 'keep tidy', 'organise', 'organised', 'organize', 'mess', 'messy',
            'lost', 'losing', 'forget', 'forgot', 'pack', 'packing', 'everything')),
          "Pack it the night before, not in the morning: the timetable, then the books for those "
          "lessons, then the kit or the letter that has to go back. One pocket for pens, one for "
          "paper, one for the phone, and nothing loose at the bottom - a bag you can empty in one "
          "look is a bag you stop losing things in."),
    entry('ask-teacher', (('teacher', 'tutor', 'lecturer',
                           'in class', 'after class', 'in the lesson', 'in a lesson',
                           'office hours', 'my class', 'in lectures'),
          ('ask for help', 'struggling', 'behind', 'help', 'fail', 'talk', 'email',
           'home', 'dont get it', "don't get it", 'shy', 'scared', 'nervous', 'afraid',
           'embarrassed', 'dont understand', "don't understand", 'confused', 'stuck',
           'ask', 'asked', 'asking', 'a question', 'questions', 'the question', 'message',
           'send an email', 'get help', 'extra help', 'more help',
           'hand up', 'raise my hand', 'raised hand', 'wasnt picked', "wasn't picked",
           'never get picked', 'not picked',
           'answer in class', 'answering in class', 'speak up in class',
           'one to one', 'reply', 'behind on',
           'ask for feedback', 'asking for feedback', 'for feedback', 'what to improve')),
          'Ask in person after class with one specific thing ("I get the formula but I can\'t do the'
          ' last question on the sheet"), and say what you\'ve already tried. Teachers help far more'
          ' often than students expect, and an email the same day saying thank you makes them'
          ' remember you next time.',
          avoid=("take notes", "taking notes", "make notes", "notes in class", "note taking",
                 "notes", "focus", "focusing", "pay attention", "paying attention", "attention",
                 "concentrate", "concentrating", "concentration", "listen better",
                 "revise", "revising", "revision", "revising for", "exam", "exams", "mock",
                 "mock exam", "marks", "mark scheme",
                 "stop talking", "talking in class", "chatting", "chat", "distracting",
                 "call out", "calling out", "shouting out", "loud in class", "noisy class",
                 "emailed me", "email me", "emailing me", "rang me", "called me", "my son",
                 "my daughter", "my child", "my kid", "my kids", "his teacher", "her teacher",
                 "their teacher", "parents evening", "parent evening", "parent teacher",
                 "parent-teacher", "head teacher", "headteacher", "my boy", "my girl")),
    entry("masters-cost",
          (("masters", "master's", "msc", "ma ", "mba", "postgraduate", "postgrad",
            "postgraduate degree", "taught masters"),
           ("cost", "costs", "how much", "fees", "fee", "tuition", "price", "expensive",
            "afford", "worth it", "worth", "loan", "bursary", "scholarship", "funding",
            "save up", "part time", "part-time")),
          "For a UK student, a taught masters is usually £9,000 to £15,000 for the year - around "
          "£8,000 to £12,000 for a classroom subject, £12,000 to £20,000 for a lab one, and an MBA "
          "can be £25,000 or more - plus living costs for a full-time year. A postgraduate "
          "master's loan from Student Finance covers up to about £12,500 of it, paid in three "
          "instalments, and it does not depend on your income. Ask the department about "
          "scholarships and fee waivers before you ask a bank, and check whether the course runs "
          "part time, because that spreads the cost over two years while you work.",
          avoid=("personal statement", "statement of purpose", "cover letter", "essay",
                 "undergraduate", "bachelors", "bachelor", "a level", "a-level",
                 "student loan", "maintenance loan", "rent", "deposit"),
          bias=1),
    entry('university-apply', (('university', 'uni', 'college application', 'personal statement', 'ucas'),
          ('apply', 'application', 'write', 'how', 'should', 'start', 'deadline')),
          "Apply on UCAS: one form, up to five courses, the personal statement and a reference, "
          "with 15 October for Oxford, Cambridge, medicine and veterinary science and mid-January "
          "for everything else. The statement is the part people worry about, and the rule is to "
          "start with the subject, not your childhood: what you have read, built or done that made "
          "you want it, then what you want to learn next. Two drafts and one reader who knows the "
          "subject beats five drafts alone.",
          avoid=("how long", "how many words", "how many characters", "word count", "characters",
                 "maximum length", "how many lines",
                 "should i go", "shall i go", "is it worth", "worth it", "worth going",
                 "do i need", "not worth", "alternatives", "if i go", "whether to go"),
          bias=1),
    entry("what-is-ucas",
          (("ucas", "ucas form", "ucas application", "ucas account"),
           ("what is", "whats", "what's", "what does", "stand for", "mean", "means",
            "how does it work", "explain", "what do i need")),
          "UCAS is the one form that covers almost every full-time UK degree: you fill it in once, "
          "add up to five courses, write a personal statement, and a teacher or employer adds a "
          "reference. The fee is about \u00a328. The early deadline is 15 October for Oxford, "
          "Cambridge, medicine, dentistry and veterinary science, and the main one is in "
          "mid-January. Offers come back between then and May, and you pick a firm choice and an "
          "insurance one.",
          avoid=("points", "tariff", "how many points", "clearing", "personal statement length",
                 "how long", "how many words"),
          bias=1),
    entry('ucas-statement-length',
          (('personal statement',),
           ('how long', 'how many words', 'how many characters', 'word count', 'words',
            'characters', 'maximum', 'limit', 'length')),
          'Four thousand characters including spaces, or forty-seven lines - whichever you hit '
          'first - and that is one side of A4 in plain prose. Write the draft long, then cut: '
          'the sentences that say nothing ("ever since I was young") go first, then any '
          "description of the course you can read on the university's own page. Paste it into "
          'a character counter rather than guessing, and leave room for the edit.',
          avoid=('cv', 'c v', 'resume', 'r\u00e9sum\u00e9', 'tax return', 'taxes')),

    entry('maths-homework', (('maths', 'math', 'algebra', 'equation', 'equations', 'geometry', 'homework problem'),
          ('help', 'solve', 'understand', 'explain', 'how', 'stuck')),
          "Ask them to show you the first step they'd try, then work one example together and let"
          " them do the next alone: that's the bit that teaches. If they're stuck on why, not how,"
          ' draw it; almost every school maths idea has a picture (a bar for fractions, a graph for'
          ' equations).',
          avoid=('helping my', 'my son', 'my daughter', 'my kid', 'my child', 'my children',
                 'wont do', "won't do", 'refuses', 'battle', 'every night', 'nagging',
                 'homework-child')),
    entry('spelling-improve', (('spelling', 'spell', 'spelling mistakes', 'grammar'),
          ('improve', 'better', 'how', 'fix', 'help')),
          'Keep a list of the words you actually get wrong (not a generic list), and test yourself'
          ' on those five at a time by writing them, saying them and covering them. For the ones'
          ' that refuse to stick, break them into a silly phrase or find the small word inside the'
          ' big one (there\'s "a rat" in separate).'),
    entry('school-presentation', (('presentation', 'talk', 'speech'),
          ('school', 'class', 'students', 'assembly', 'nervous')),
          'Write the first sentence and the last sentence first, then three points in between, one'
          ' card each. Practise out loud standing up, once to a person and once to a wall, and print'
          ' the cards in big letters: looking up at people is what makes a school talk go well, and'
          " you can't look up at a phone.",
          avoid=("stop talking", "talking too much", "talk too much", "chatting", "chatty",
                 "chatter", "chatterbox", "blurt", "blurting", "keep talking", "distracting",
                 "nobody talks", "no one talks", "nobody speaks", "no one speaks",
                 "talks to me", "speaks to me", "talk to me", "speak to me",
                 "nobody will talk", "no one will talk")),

    entry("talkative-in-class",
          (("class", "classes", "classroom", "lesson", "lessons", "school", "teacher",
            "lecture", "lectures", "seminar", "seminars", "assembly", "assemblies",
            "tutor", "tutors", "tutorial", "tutorials", "playground", "playgrounds"),
           ("stop talking", "talk too much", "talking too much", "talk to much", "chat too much",
            "chatting", "chatty", "chatter", "chatterbox", "blurt", "blurting", "keep talking",
            "quiet", "quieter", "distract", "distracting", "shouting out", "too loud")),
          "Sit where the chat cannot start: front row, or beside someone you do not talk to, and "
          "ask the teacher to move you, which is a normal request and not a confession. Keep a "
          "corner of the page for the things you want to say and hold them to the end of the "
          "lesson - most of them keep, and the good ones come back to you. If it is answers "
          "blurting out, count to three and write the answer down first; the urge drops once it "
          "is on the page.",
          avoid=NOT_AN_EXAM + ("classmate", "classmates", "presentation", "presentations",
                               "speech", "exam", "exams", "revision", "revise",
                               "test", "grade", "grades")),

    entry("memorise-quotes",
          (("quotes", "quote", "quotations", "key quotes"),
           ("memorise", "memorize", "memorising", "learn", "remember", "english lit", "essay",
            "exam", "revise", "revision", "how")),
          "Pick eight to ten short ones you can use for more than one theme, and learn them in "
          "fours to six words rather than whole speeches - \"a plague o' both your houses\" is "
          "learnable, a fifteen-line speech is not. Say each aloud, look away and say it, then "
          "write it from memory; do three a day and cycle back through the rest. Practise the "
          "sentence you will build around it, because the quote alone earns nothing without the "
          "two lines of analysis after it.",
          avoid=NOT_AN_EXAM),

    entry("exam-timing",
          (("running out of time", "out of time", "time in exams", "didnt finish",
            "didn't finish", "no time left", "ran out of time", "finish the paper"),
           ("exam", "exams", "paper", "test", "revision", "how", "help", "tips", "stop")),
          "Give each question the minutes it is worth: one mark is about one minute, so a "
          "ten-mark question gets ten. Write the clock time you must move on by in the margin "
          "before you start, and move on when it arrives even if the answer is unfinished - a "
          "half answer plus the next question beats a perfect first one and three blanks. Read "
          "the whole paper first, do the question you know best, and keep the last five minutes "
          "for checking names, units and whether every question has an answer.",
          avoid=NOT_AN_EXAM,
          bias=4),

    entry("gap-year",
          (("gap year", "year out", "take a year off", "defer", "deferring"),
           ("should", "worth", "take", "better", "do", "plan", "uni", "university", "offer",
            "money", "work",
            "what is", "whats", "what's", "mean", "means", "definition", "define", "explain")),
          "It is worth it when there is a reason you can name: a paid job that builds a skill, a "
          "season abroad with the cost worked out, or time for something you could not do later. "
          "Ask your university in writing to defer - most hold the offer for one year if you ask "
          "before the start date - and keep the place in mind, because reapplying is harder than "
          "deferring. Work out the money first: a year abroad is cheap only if the flights and the "
          "first month are paid for before you go.",
          avoid=NOT_AN_EXAM),

    entry("marks-question",
          (("marked me down", "marks me down", "marking me down", "marks down", "low marks",
            "bad marks", "marks are low", "marked down", "unfair mark", "unfair marks",
            "marks dont make sense", "dont understand my marks", "teacher marks"),
           ("why", "teacher", "ask", "unfair", "lower", "explain", "dont know", "appeal",
            "grade", "grades", "feedback", "marked")),
          "Ask for the mark scheme, not for a favour: \"could I see which part of question 3 "
          "lost the marks?\" That is a normal request, and a good teacher will show you. Then ask "
          "for one example of what a full-mark answer looked like and rewrite that paragraph with "
          "it in front of you. If the marks still look wrong against the published scheme, ask the "
          "school for a remark in writing rather than arguing in the corridor.",
          avoid=NOT_AN_EXAM + ("stain", "washing", "shirt", "carpet", "wood", "paint")),

    entry("uni-cost",
          (("uni cost", "university cost", "cost of uni", "cost of university", "tuition fee",
            "tuition fees", "student debt", "how much does uni", "how much does university"),
           ("much", "total", "cost", "costs", "pay back", "worth", "how", "year", "all")),
          "In England the fee is £9,250 a year, so a three-year course is about £27,750, and "
          "living costs add roughly £9,000 to £12,000 a year on top. Nobody pays it up front: it "
          "is a loan repaid at 9% of what you earn above about £25,000, and what is left is "
          "written off after 40 years, so the monthly figure matters far more than the headline. "
          "Check the maintenance loan for your household income, and pay the deposit for "
          "accommodation out of the first instalment rather than a credit card.",
          avoid=NOT_AN_EXAM),
    entry("remember-reading",
          (("remember what i read", "remember what i've read", "remember a book",
            "remember a chapter", "remember reading", "take notes from a book",
            "make notes from a book", "read and remember", "reading for study",
            "how do i remember",
            "retain", "take in", "takes in", "sink in", "sinks in", "sticks",
            "cant remember what i read", "can't remember what i read",
            "dont remember what i read", "don't remember what i read",
            "forget what i read", "nothing i read",
            "cant remember", "can't remember", "dont remember", "don't remember",
            "remember any of it", "forget", "forgetting", "forgot"),
           ("read", "reading", "book", "chapter", "textbook", "notes", "remember", "memory",
            "revision", "revise", "study", "keep", "how", "page", "pages", "article",
            "paragraph")),
          "Read a section, then close the book and say its three points out loud before going on - "
          "rereading feels like study but the recall is what sticks. Turn each heading into a "
          "question first (\"what is a supply curve?\") and answer it from memory, then write one "
          "line per page in your own words. Come back to those lines after ten minutes, the next "
          "day and a week later, and you keep most of it with far less total time.",
          guard=_the_page_is_what_was_forgotten,
          avoid=("phone number", "pin", "password", "birthday", "name of", "surname",
                 "my ex", "get over", "move on", "grief", "grieving", "bereaved", "died",
                 "death", "passed away", "him", "her", "someone", "somebody", "breakup",
                 "break up", "affair", "cheated", "how to", "names", "anniversary", "word",
                 "spelling", "where i put", "where i left", "appointment", "medication",
                 "tablet", "keys", "glasses", "wallet",
                 "barbecue", "barbecues", "bbq", "barbeque", "grill", "grilling", "pan", "pans",
                 "wok", "pasta", "rice", "dough", "pastry", "meat", "chicken", "fish",
                 "pancake", "pancakes", "crepe", "crepes", "batter", "waffle", "waffles",
                 "yorkshire", "yorkshires", "yorkshire pudding", "pikelet", "pikelets",
                 "cooking", "cook", "recipe", "oven", "sauce", "gravy", "soup",
                 "bread", "loaf", "loaves", "cake", "cakes", "baking", "bake", "batter",
                 "sponge", "souffle", "risen",
                 "curtain", "curtains", "shower", "shower curtain", "screen protector", "phone",
                 "laptop", "phone screen", "cling film", "bin bag", "zip", "drawer", "door",
                 "window", "sticker", "stickers", "tape", "plaster", "saucepan", "frying pan",
                 "pasta", "rice", "pan", "pans", "dough", "pastry",
                 "our plans", "our dates", "partner", "husband", "wife", "marriage",
                 "subscription", "subscriptions", "cancel", "cancelling", "canceling",
                 "direct debit", "insurance", "bill", "bills", "renewal", "renew", "payment",
                 "payments", "policy",
                 "make it stick", "make it stick this time", "stick with it", "stick at it",
                 "keep at it", "keep it up", "keep going")),
    entry("fail-exams",
          (("fail my exams", "failed my exams", "fail my exam", "failed my exam", "fail my a levels",
            "failed my a levels", "fail my gcses", "failed my gcses", "fail the year",
            "failed the year", "failed my degree", "fail my degree", "did badly in my exams",
            "did badly in my exam", "flunked", "i failed", "get a remark", "ask for a remark",
            "remark my exam", "a remark"),
           ("what", "should", "do", "now", "next", "resit", "retake", "remark", "appeal",
            "university", "college", "sixth form", "year", "help",
            "i", "my")),
          "Speak to your school or college on results day, not next month: they can tell you the "
          "resit date (usually November for maths and English, the following summer for most "
          "others) and whether the university or college will hold your place, which plenty will "
          "once they know. If you were a mark or two off a grade boundary, a remark can be worth "
          "it, but it can also go down, so ask the exams officer what the risk is. Failing one "
          "paper is not failing the year, and a plan made this week beats a summer of dread.",
          bias=2,
          avoid=NOT_AN_EXAM + ("missed my offer", "missed the offer", "missed my place",
                               "clearing", "my offer", "firm choice", "insurance choice",
                               "rejected by", "rejected me"),
          guard=lambda understood: not _a_failure_of_something_else(understood)),
    entry("college-or-university",
          (("college or university", "university or college", "difference between college",
            "college and university", "should i go to college", "college instead of university",
            "is college better than university", "btec or a levels",
            "sixth form or college", "what is college"),
           ("difference", "better", "worth", "should", "which", "or", "need", "instead of",
            "what", "why", "choose", "decide", "go to", "matter")),
          "College is further education: A-levels, BTECs, T-levels, apprenticeships and access "
          "courses, usually for 16 to 18 year olds and mostly free until 19. University is a "
          "degree, three or four years, with tuition loans and maintenance loans to pay for it. "
          "The route that works for most people is whichever gets you the qualification the job "
          "you want actually asks for: a trade, nursing or design can go straight from college "
          "into work, while law, medicine and teaching need the degree. College first is not a "
          "step down - an access or foundation year costs less than a wasted degree and keeps the "
          "university route open.",
          avoid=("how do i apply", "ucas", "student loan", "student finance", "tuition fee",
                 "how much does university cost", "open day", "personal statement")),
    entry("essay-conclusion",
          (("conclusion", "conclusions", "conclude", "ending", "sum up", "summarise",
            "summarize", "wrap up", "last paragraph", "final paragraph",
            "strong conclusion", "good conclusion", "essay conclusion", "write a conclusion",
            "conclusion for", "conclusion of", "conclusion to"),
           ("essay", "essays", "dissertation", "coursework", "assignment", "report", "write",
            "writing", "how", "start", "phrases", "words", "should", "what", "need", "good",
            "strong", "help")),
          "The last paragraph is where you say what it adds up to, not what you have already "
          "said: one sentence that answers the question in the title, one on the strongest "
          "evidence that got you there, then the wider point or what should happen next. Four or "
          "five sentences is enough, with no new evidence and no new quotation - if a fact belongs "
          "in the conclusion, it belongs in the body first.",
          guard=_the_ending_is_written,
          avoid=("i came to the conclusion", "came to the conclusion", "test", "experiment",
                 "war", "wars", "battle", "battles", "revolution", "armistice", "trench",
                 "trenches", "empire", "1914", "1918", "1939", "1945",
                 "chat", "chats", "chatting", "conversation", "conversations", "phone call",
                 "phone calls", "party", "parties", "relationship",
                 "tenancy", "lease", "contract", "subscription", "argument", "friendship",
                 "end things", "boyfriend", "girlfriend", "partner", "husband", "wife",
                 "break up", "breaking up", "divorce", "marriage", "my marriage", "fiance",
                 "fiancee",
                 "lab report", "results", "data", "conclusion of my", "doctor", "gp",
                 "diagnosis",
                 "end up", "ended up", "ends up", "ending up", "homework", "son", "daughter",
                 "child", "children", "kids", "kid", "maths", "times tables",
                 "end of life", "end-of-life", "life care", "dying", "died", "dies",
                 "dying", "palliative", "hospice", "hospices", "terminally", "terminal",
                 "bereavement", "grief", "funeral", "my mum is", "my dad is",
                 "my mother is", "my father is",
                 "end a fast", "end my fast", "end the fast", "end this fast",
                 "end a diet", "end my diet", "end the diet",
                 "end a poem", "end my poem", "end the poem", "end a verse",
                 "end a sentence", "end my sentence", "end a paragraph", "end my paragraph",
                 "end a chapter", "end my chapter", "end a book", "end my book",
                 "end a story", "end my story", "end a novel", "end my novel",
                 "interview", "interviews", "interviewing", "interviewer", "job interview",
                 "panel", "appraisal", "one to one", "1:1",
                 "end a meeting", "end the meeting", "end my meeting", "meeting",
                 "end a shift", "end my shift", "end the shift", "end a call", "end the call"),
          bias=1),
    entry("mature-student",
          (("go back to uni", "go back to university", "going back to uni",
            "going back to university", "back to uni", "back to university",
            "back to studying", "back to study", "mature student", "mature students",
            "go back to college", "back to college", "going back to college",
            "college at 30", "college at 40", "college at 50", "evening class", "evening classes",
            "study as an adult", "degree as an adult", "evening degree", "part time degree",
            "open university", "study at night",
            "university at 30", "university at 40", "university at 50", "uni at 30", "uni at 40",
            "uni at 50", "degree at 30", "degree at 40", "in my 30s", "in my 40s", "in my 50s",
            "late in life"),
           ("40", "30", "35", "45", "50", "older", "later", "at my age", "worth", "should",
            "how", "as an adult", "after kids", "after children", "career change", "money",
            "cost", "afford")),
          ("Going back later is common, and the money is the first thing to check: a "
           "full-time degree is three years without a salary, so most people do it part time, one "
           "module at a time, or with the Open University. Student finance counts you as an "
           "independent student, so your own income decides the loan, and a course can credit "
           "what you already know. Do one evening class first, before you commit to three years."),
          avoid=("pass mark", "passing mark", "pass", "passes", "percent", "percentage", "grade",
                 "grades", "classification", "2:1", "first class", "ucas", "personal statement",
                 "student loan", "tuition fee", "tuition fees", "how do i apply", "open day")),
    entry("university-pass-mark",
          (("university", "uni", "degree", "degrees", "undergraduate", "bachelors", "masters",
            "msc", "bsc", "postgrad", "postgraduate", "module", "modules", "semester",
            "2:1", "2.1", "2:2", "2 1", "2 2", "first class", "upper second", "lower second",
            "distinction", "merit", "classification", "pass mark", "passing mark"),
           ("pass mark", "pass", "passing", "passed", "fail", "fails", "failing", "mark", "marks",
            "40", "50", "60", "70", "percent", "percentage", "average", "need", "what",
            "how much", "grade", "grades", "worth", "count", "counts", "resit", "resubmit",
            "good", "is", "are", "dont", "mean", "means")),
          _university_pass_mark,
          avoid=("gcse", "gcses", "a level", "a-level", "alevel", "alevels", "sixth form",
                 "year 11", "year 10", "sats", "11+", "secondary school", "high school",
                 "what should i study", "should i study", "what to study",
                 "what should i take", "what should i do at uni",
                 "what should i do at university",
                 "tuition fee", "fees", "student loan", "student finance", "maintenance loan",
                 "how do i apply", "ucas", "personal statement", "open day", "is university",
                 "is uni", "worth going", "how much does",
                 "worth it", "is it worth", "worth doing", "worth the money", "worth the debt",
                 "at 40", "at 30", "at 50", "at 45", "in my 40s", "in my 30s", "in my 40's",
                 "go back to uni", "back to uni", "back to university", "mature student",
                 *_A_DEGREE_OF_HEAT,
                 "do i need a degree", "need a degree to", "degree to be", "to be a", "to be an",
                 "become a", "become an", "get into", "qualify as", "train as",
                 "stamp", "stamps", "postage", "post office", "postbox", "post box",
                 "royal mail", "envelope", "envelopes", "signed for", "recorded delivery",
                 "first class stamp", "second class stamp", "first class post",
                 "second class post", "train ticket", "plane ticket", "flight", "seat",
                 "carriage", "railcard")
                 + A_WHAT_TO_WEAR,
          bias=1,
          guard=lambda understood: (not quantity.a_figure_with_a_unit(understood)
                                    and _the_degrees_are_heat(understood))),

    entry("course-choice",
          (("which course", "what course", "course to study", "choose a course", "pick a course",
            "choosing a course", "which degree", "what degree", "choose a degree",
            "university course", "which university", "choose a university",
            "what to study at university", "what to study at uni",
            "what should i study", "what should i do at university", "what should i do at uni",
            "subject to study", "what subject"),
           ("should i", "how do i", "help", "advice", "choose", "pick", "decide", "between",
            "better", "best", "worth", "difference", "study", "do")),
          "Choose on the modules in years two and three, not the course title: read them, and if "
          "half of them bore you the course is wrong whatever it is called. Then check the entry "
          "requirements against your predicted grades, the contact hours and whether a placement "
          "or a year in industry is offered, and the graduate outcomes page for where last year's "
          "students went. Go to an open day and sit in one lecture if you can, because a "
          "department feels like something on the day. Apply to five with one dream and two safe "
          "choices, and keep the one you would be happy at if the grades go wrong.",
          ask=("should i", "how do i", "help", "advice", "choose", "pick", "decide", "between",
               "better", "best", "worth", "difference", "study"),
          avoid=("university worth", "worth it", "ucas", "personal statement", "apply", "clearing",
                 "gap year", "a level subject", "a levels to", "gcse",
                 "a level", "a levels", "a-level", "as level", "gcse", "gcses")),
    entry("clearing",
          (("clearing", "clearing place", "clearing course",
            "a place at university", "which university", "adjustment"),
           ("what is", "how does", "university", "ucas", "uni", "college", "course", "apply",
            "get in", "get a place", "get onto", "find", "place", "vacancy", "vacancies",
            "missed", "grades", "worse than", "not got in", "offer", "adjustment",
            "open", "opens", "start", "starts", "begin", "begins", "still")),
          "Clearing is how you get a place when you have no offer or your grades missed: from "
          "July to October, search the official UCAS Clearing service for courses with vacancies, "
          "then ring the university yourself with your UCAS personal ID, your grades and the "
          "course code - an offer made on that call is a real offer. Have the list and your "
          "grades in front of you, ring three or four in one morning, and add the one you want in "
          "UCAS Track before you relax. If you already have a place and want a better one, that "
          "is adjustment, which is the same search with a deadline of five days.",
          ask=("what is", "how does", "how do i", "apply", "get", "find", "place", "vacancy",
               "missed", "grades", "when", "still", "open"),
          avoid=("failed my", "resit", "remark", "a level results day", "my teacher",
                 "cache", "cached", "cookies", "browser", "chrome", "safari", "app",
                 "clear my", "clear the", "clear a", "clear an", "clear our", "clear your",
                 "clear out", "clear up", "clearing my", "clearing the", "clearing out",
                 "clear space", "clear some space", "clear storage", "clear enough",
                 "cleared my", "cleared the", "clear some", "clear any",
                 "clear debt", "clear debts", "clear arrears", "clear balance",
                 "clear credit card", "clear loan", "clear loans", "clear mortgage",
                 "clear overdraft", "clear it",
                 "condensation", "condensed", "steamed up", "steaming up", "misted up",
                 "fogged up", "fogging up", "pane", "panes", "squeegee", "windscreen",
                 "clear room", "clear some room", "room on my", "room for",
                 "laptop", "computer", "junk files", "downloads")),
    entry("first-class",
          (("first class", "first in my degree", "get a first", "2:1", "2.1", "second class",
            "degree classification", "final year", "dissertation"),
           ("how do i", "how to", "get", "aim", "need", "what", "difference", "improve",
            "better", "marks", "grade", "degree", "honours", "worth", "matter")),
          "The marks come from the same three things in every module: answer the exact question "
          "that was set, argue one clear line rather than describe everything you know, and quote "
          "the reading to back it. Get the marking criteria for each module and treat it as the "
          "checklist, then use the feedback on your first essay - the same weakness costs marks "
          "three times if nobody fixes it. Go to the lectures and seminars, because the person "
          "marking it notices, and start the dissertation in the summer before final year: a "
          "first is usually decided by the dissertation and two strong modules, not by all of "
          "them.",
          ask=("how do i", "how to", "get", "aim", "need", "what", "difference", "improve",
               "better", "matter", "want", "want to", "hoping", "aiming", "trying"),
          avoid=("a level", "gcse", "exam", "revision", "essay", "reference", "notes",
                 "first aid", "first-aid", "aid", "certificate", "course",
                 "stamp", "stamps", "postage", "post office", "letter", "parcel")),
    entry("lab-report",
          (("lab report", "lab reports", "write up", "write-up", "practical report",
            "experiment write up", "practical write up", "biology practical",
            "chemistry practical", "physics practical"),
           ("how do i", "how to", "write", "writing", "sections", "layout", "format",
            "include", "need", "goes in", "as level", "a level", "gcse", "university")),
          "Write it in this order and the marks look after themselves: aim in one sentence, "
          "method in numbered steps someone else could follow, results as a table plus one graph "
          "with labelled axes and units, then a conclusion that says whether the prediction was "
          "right, then an evaluation of what went wrong. Keep the method past tense and passive "
          "('the solution was heated'), put numbers to the precision the instrument allows, and "
          "have one paragraph on sources of error with what you would change - that paragraph is "
          "the difference between a pass and a good mark. Do the graph and the evaluation first "
          "when you are short of time, because they carry the most marks.",
          ask=("how do i", "how to", "write", "writing", "sections", "layout", "format",
               "include", "need"),
          avoid=("essay", "coursework", "dissertation", "thesis", "book report", "report on",
                 "business report", "annual report")),
    entry("sixth-form-grades",
          (("sixth form", "sixth-form", "college place", "a level place", "a level entry",
            "get into sixth form", "year 12", "year 11",
            "college", "gcse", "gcses", "a level"),
           ("what grades", "grades do i need", "grades", "requirements", "need", "entry",
            "points", "average", "enough", "to do", "get in", "apply")),
          "Most sixth forms and colleges ask for five GCSEs at grade 4 or above, including "
          "English and maths, and then a 6 or a 7 in the subjects you want to take at A level - "
          "so check the subject page, not the general prospectus, because the maths and science "
          "requirement is usually higher than the rest. If you miss the grades, ask about a "
          "level 3 course or a mixed programme, which often lets you move on to A level after a "
          "year, and apply early with a backup choice: places are offered from the autumn of "
          "year 11, not on results day.",
          ask=("what grades", "grades", "requirements", "need", "entry", "points", "enough",
               "get in", "apply"),
          avoid=("university", "uni", "ucas", "degree", "offer", "clearing", "what does",
                 "what do my grades mean", "my grades mean",
                 "licence", "license", "driving", "motorway", "speeding", "insurance",
                 "how many a levels", "how many a level", "how many subjects",
                 "apply for college", "applying for college", "apply to college",
                 "college application", "apply for sixth form",
                 "nurse", "nursing", "teacher", "teaching", "vet", "veterinary", "doctor",
                 "lawyer", "solicitor", "midwife", "electrician", "to be a"),
          bias=1),
    entry("leaving-school-at-16",
          (("leave school", "leaves school", "left school", "leaving school", "quit school",
            "quitting school", "drop out of school", "dropping out of school", "not stay on",
            "stay on at school", "stay at school", "sixth form", "college instead"),
           ("16", "sixteen", "at 16", "year 11", "year 12", "after gcses", "after gcse",
            "wont go", "won't go", "doesnt want", "refuses", "refusing", "should i let",
            "let him", "let her", "is it ok", "is it legal", "allowed", "have to", "must",
            "law")),
          "In England they can leave school at 16 but not stop learning: education or training "
          "has to continue until 18, and a college course, an apprenticeship or a job with "
          "accredited training in the week all count, so it does not have to be more school. "
          "The realistic routes are A levels at a sixth form, a level 2 or 3 vocational course "
          "(BTEC, T level, NVQ) at college, or an apprenticeship, which is a paid job with the "
          "training built in and usually one day a week at college. Visit one college open day "
          "together before deciding, and ask about a level 2 course if the GCSEs are shaky, "
          "because that is a stepping stone to level 3 rather than a dead end.",
          ask=("can they", "can my", "is it", "should", "do they have to", "have to", "what are",
               "what can", "options", "instead", "wants to", "want to", "doesnt want",
               "does not want", "wont", "refuses", "leave", "leaving", "quit", "drop out"),
          report=True,
          avoid=("what grades", "grades do i need", "how do i apply", "apply for college",
                 "apply to college", "ucas", "university", "uni", "a level results",
                 "gcse results", "results day", "birthday", "16th", "driving", "licence",
                 "license", "moped", "cigarettes", "alcohol", "consent", "minimum wage",
                 "national insurance")),
    entry("strict-teacher",
          (("strict teacher", "strict", "harsh teacher", "mean teacher", "unfair teacher",
            "teacher hates me", "teacher doesnt like me", "teacher doesn't like me",
            "does not like me", "doesnt like me", "does not like my", "dont like me",
            "picks on me", "picking on me", "picked on by", "shouted at by teacher",
            "teacher keeps",
            "hates", "hated", "hate my teacher"),
           ("what do i do", "how do i", "deal with", "handle", "cope", "help", "should i",
            "talk to", "complain", "tell", "my teacher", "teacher", "class", "lesson")),
          _strict_teacher,
          ask=("what do i do", "how do i", "deal with", "handle", "help", "should i", "talk to",
               "complain", "tell", "hate", "hates", "picks on", "picked on", "shouts",
               "unfair", "mean", "harsh", "like me", "not like"),
          bias=1,
          guard=lambda understood: _a_school_line(understood),
          avoid=("boss", "manager", "work", "my job", "colleague", "bully", "bullied",
                 "bullying", "homework", "exam",
                 "the hate u give", "read after", "read next", "reading next", "what to read",
                 "books like", "book like", "book after", "novel", "novels")),]

_REMEMBERS = ("memorise", "memorize", "memorising", "memorizing", "remember", "remembering",
              "learn", "learning", "memory", "brain", "forget", "forgetting", "forgetful",
              "revise", "revising", "revision")

_MEMORISE = ("Test yourself instead of rereading: cover the page, say or write what you remember, "
             "then check. That one change does more than any technique. Then space it out - the "
             "same thing tomorrow, in three days, in a week - because the forgetting and the "
             "effort of getting it back is what makes it stay. Say it out loud or write it by hand "
             "rather than only reading, link a new fact to one you already know, and sleep on it: "
             "a night's sleep is when it gets filed.")


def _memorise(memory, understood):
    line = " " + " ".join(str(w) for w in ((understood or {}).get("norm") or
                                          (understood or {}).get("plain") or "")).lower() + " "
    if not any(word in line for word in _REMEMBERS):
        return None
    return _MEMORISE


ENTRIES.append(entry(
    "memorise-faster",
    (("memorise", "memorize", "memorising", "memorizing", "remember", "remembering", "learn",
      "learning", "memory", "brain"),
     ("faster", "quickly", "quick", "better", "stick", "sticks", "sticking", "stuck", "forget",
      "forgetting", "keeps forgetting", "keep forgetting", "more", "improve", "sharper",
      "technique", "techniques", "trick", "tricks", "tips", "how", "best", "effective", "way")),
    _memorise,
    avoid=("dates", "timeline", "history", "flashcard", "flashcards", "anki", "quizlet",
           "the job", "my job", "new job", "the role", "my role", "at work", "on the job",
           "the ropes", "ropes", "up to speed",
           "mnemonic", "mnemonics", "spelling", "spell", "password", "passwords",
           "names and faces", "faces and names",
           "dream", "dreams", "where i put", "where i left", "remember to", "remind me",
           "reminder", "birthday", "anniversary", "asleep", "tired", "sleepy",
           "mum", "mom", "mother", "dad", "father", "parent", "parents", "grandma",
           "grandmother", "grandad", "grandfather", "gran", "nan", "nana", "mother in law",
           "father in law",
           "touch type", "touch-type", "touch typing", "touch-typing", "typing", "keyboard",
           "wpm", "words a minute",
           "drive", "driving", "cook", "cooking", "bake", "baking", "swim", "swimming",
           "knit", "knitting", "sew", "sewing", "draw", "drawing", "dance", "dancing",
           "guitar", "piano", "drums", "violin", "ride a bike", "cycle", "cycling",
           "code", "coding", "programming", "touch typing", "juggle", "whistle",
           "husband", "wife", "partner", "boyfriend", "girlfriend", "granny", "grandpa",
           "getting forgetful", "gets forgetful", "memory loss", "losing his memory",
           "losing her memory", "dementia", "alzheimers", "alzheimer's", "as you get older",
           "getting older", "my age",
           "oven", "cooked", "recipe", "recipes", "dish", "dishes", "tray", "trays",
           "tin", "tins", "roast", "kitchen"),
    ask=("faster", "quickly", "quick", "better", "stick", "sticks", "sticking", "stuck",
         "forget", "forgetting", "keeps forgetting", "keep forgetting", "more", "improve",
         "sharper", "technique", "techniques", "trick", "tricks", "tips", "how", "best",
         "effective", "way")))

ENTRIES.append(entry(
    "learn-touch-typing",
    (("touch type", "touch-type", "touch typing", "touch-typing", "typing", "wpm",
      "words a minute"),
     ("learn", "learning", "teach myself", "improve", "quicker", "speed", "properly", "proper",
      "start", "practice", "practise")),
    "Start on the home keys and do not look down: left hand on a s d f, right hand on j k l and "
    "the semicolon, thumbs on the space bar, and cover your hands with a cloth if you keep "
    "peeking. Ten to fifteen minutes a day on a free drill site, typing real sentences rather "
    "than random letters, is enough to build it. Accuracy first and speed second, because a "
    "wrong key costs more time than a slow one: most people go from about 30 to 50 words a "
    "minute in a month of daily practice, and the last stretch comes from typing your own "
    "messages rather than the drills.",
    ask=("how", "how do i", "how can i", "how to", "whats the best way", "can i", "help", "tips",
         "faster", "better"),
    avoid=("wrong letters", "wrong letter", "types the wrong", "typing the wrong", "not working",
           "broken", "broke", "spilled", "sticky", "missing keys", "virtual", "on screen",
           "clean", "cleaning", "cleaned", "wipe", "dirty", "crumbs", "grubby", "disinfect",
           "phone keyboard", "autocorrect", "swipe",
           "symbol", "symbols", "special character", "special characters", "emoji", "emojis",
           "accent", "accents", "capital letter", "capital letters", "uppercase", "underscore",
           "hashtag", "slash", "asterisk", "tilde", "key combination", "shortcut", "shortcuts"),
    bias=1))

_LATER_STUDY = re.compile(
    r"\b(?:course|courses|college|university|uni|degree|gcse|gcses|a[ -]?levels?|night school|"
    r"evening class|evening classes|access course|study|studying|lessons?|retrain|retraining|"
    r"qualification|qualifications|apprenticeship|masters|phd|bookkeeping|"
    r"nursing|tutor|lectures?|homework|exams?|revision|traineeship|nvq)\b")

_CAREER_CHANGE = re.compile(
    r"\b(?:too old|too late)\b[^.?!]*\b(?:become|becoming|train as|training as|retrain as|"
    r"retraining as|qualify as|qualifying as|career change|change career|change jobs|switch careers?|"
    r"switch to|move into|go into|get into)\b")

_NOT_AGE_STUDY = re.compile(
    r"\b(?:baby|babies|pregnan\w*|ivf|fertility|children|kids|puppy|puppies|dog|dogs|cat|cats|"
    r"driving|drink\w*|tattoo|piercing|marathon|gym|weight|surgery|operation|"
    r"piano|guitar|violin|viola|cello|drums|instrument|instruments|keyboard|ukulele|flute|"
    r"business|businesses|startup|startups|company|shop|restaurant|cafe|"
    r"dad|father|mum|mom|mother|parent|parents|grandma|grandmother|grandad|grandfather|"
    r"footballer?|athlete|olympic|rugby|boxer|boxing|singer|dancer|actor|actress|model|"
    r"influencer|youtuber|streamer)\b")


_AGE_ASK = re.compile(
    r"\b(?:too old|too late|at my age|my age|the age|an age|age matter|age matters|age stop|"
    r"age a problem|age hold|can i still|could i still|is it still|still worth|"
    r"worth it at|at \d{2}|in my (?:thirties|forties|fifties|sixties|seventies))\b")

_AGE_NUMBER = re.compile(r"\b(\d{2})\b")


def _study_later(memory, understood):
    clean = re.sub(r"[^a-z0-9' ]+", " ", " " + str(
        understood.get("clean") or understood.get("text") or "").lower() + " ")
    if _NOT_AGE_STUDY.search(clean):
        return None
    career = bool(_CAREER_CHANGE.search(clean))
    if not (_AGE_ASK.search(clean) or career):
        return None
    if not (_LATER_STUDY.search(clean) or career):
        turns = memory.get("turns")
        seen = False
        if isinstance(turns, list):
            for turn in turns[-2:]:
                if isinstance(turn, dict) and _LATER_STUDY.search(
                        str(turn.get("user") or "").lower()):
                    seen = True
        if not seen:
            return None
    match = _AGE_NUMBER.search(clean)
    age = int(match.group(1)) if match else 0
    if 18 <= age <= 90:
        if age > 60:
            return (f"At {age} you would be older than most of the class, and that is normal on "
                    "these courses: what decides it is not the age but the routine - one fixed "
                    "evening in class and one more for reading, kept for the length of the "
                    "course - and a subject you will still open on a bad week. Ask the college "
                    "what share of last year's class finished, and whether any of it can be done "
                    "in the daytime or online, because that is what makes it stick.")
        opener = f"At {age} you would not be late: "
    else:
        opener = "You would not be late: "
    return (opener + "evening classes, access courses, apprenticeships and part-time degrees are "
            "full of people in their thirties, forties and fifties, and the ones who finish are "
            "the ones with a "
            "protected evening rather than the fastest readers. What decides it is the routine — "
            "one fixed evening in class and one more for reading, kept for the length of the "
            "course — and a subject you will still open on a bad week. Ask the college what share "
            "of last year's class finished, because these courses are lost to work and life far "
            "more than to age.")


_COURSE_TIME = ("how much work", "how much time", "how much reading", "how many hours",
                "much study", "workload", "hours a week", "a week", "per week", "each week",
                "evenings a week", "commitment", "much effort",
                "the hours", "what hours", "hours be", "hours like")

def _course_hours(memory, understood):
    clean = str(understood.get("clean") or understood.get("text") or "").lower()
    if _LATER_STUDY.search(clean):
        return None
    turns = memory.get("turns")
    if isinstance(turns, list):
        for turn in turns[-2:]:
            if not isinstance(turn, dict):
                continue
            before = str(turn.get("user") or "").lower()
            if _LATER_STUDY.search(before) or _CAREER_CHANGE.search(before):
                return COURSE_HOURS
    return None


COURSE_HOURS = ("Budget two to three hours of reading and homework for every hour in class: a "
                "three-hour evening class is usually 9 to 12 hours a week including the class, "
                "and a part-time degree is 16 to 20 hours a week because it is half of a "
                "full-time course. The college has to publish those guided-learning hours on the "
                "course page, so ask for them before you enrol and pick the two evenings you "
                "would protect. Reading is what gets dropped first, so put it in the diary as an "
                "appointment rather than a hope.")


ENTRIES.append(entry(
    "study-age",
    (("at my age", "my age", "too old", "too old for", "too late", "mature student",
      "mature students", "older student", "am i too old", "is it too late", "age matter",
      "does age", "age stop me", "age too late"),
     ("sensible", "worth", "wise", "should i", "do it", "thing to do", "go for it", "go back",
      "study", "studying", "university", "uni", "college", "course", "retrain", "learn",
      "start", "doing",
      "become", "becoming", "be a", "qualify", "qualifying", "career", "careers",
      "change career", "switch")),
    _study_later,
    avoid=("retire", "retiring", "retirement", "pension", "mortgage", "bus pass", "state pension",
           "driving licence", "insurance", "job interview", "cv"),
))

ENTRIES.append(entry(
    "course-hours",
    (_COURSE_TIME,
     ("course", "courses", "college", "university", "uni", "evening class", "evening classes",
      "night school", "part time", "part-time", "degree", "study", "studying", "would it",
      "would that", "would i need", "do you think", "be",
      "is that", "is it", "that", "it")),
    _course_hours,
    avoid=("sleep", "overtime", "shift", "shifts", "salary", "pay", "job", "jobs", "driving",
           "revise", "revising", "revision", "exam", "exams", "test", "tests", "gcse", "gcses",
           "a level", "a levels", "mocks", "homework", "work out my", "do i work"),
))

ENTRIES.append(entry(
    "improve-english",
    (("english", "spanish", "french", "italian", "german", "portuguese", "polish", "welsh",
      "irish", "dutch", "a language", "languages", "language"),
     ("improve", "better", "learn", "learning", "fluent", "fluently", "speak", "speaking",
      "practice", "practise", "practising", "practicing", "study", "studying", "get better",
      "conversation", "conversational")),
    "Understand more before you try to speak, and speak badly early: ten minutes of listening or "
    "reading you mostly follow, every day, does more in a month than a grammar book. Learn whole "
    "phrases rather than single words - \"could I have...\", \"I've just...\" - because they come "
    "out in the right order without you building them. Then say them: out loud on your own, to a "
    "tutor once a week if you can, or to anyone patient. Get corrected on the mistakes you make "
    "every time, not on every mistake, and keep a list of your own bad habits. Watching something "
    "you already know with subtitles in the new language is the cheapest hour there is.",
    avoid=("spell", "spelt", "spelling", "grammar", "comma", "apostrophe", "semicolon",
           "synonym", "meaning", "means", "difference between", "pronounce", "pronunciation",
           "translate", "translation", "essay", "coursework", "gcse", "a level", "ielts",
           "exam", "test", "do you speak", "can you speak", "why is"),
    ask=("improve", "better", "learn", "learning", "fluent", "fluently", "speak", "speaking",
         "practice", "practise", "practising", "practicing", "study", "studying", "get better",
         "conversation", "conversational", "how"),
))
ENTRIES.append(entry(
    "gcse-points",
    (("gcse points", "points for college", "points for a levels",
      "how many gcses", "how many gcse", "grades do i need", "grades to get in",
      "entry requirements", "entry grades", "what grades", "which grades", "gcse grades"),
     ("how many", "how much", "need", "needs", "needed", "college", "sixth form", "a level",
      "a levels", "course", "get in", "get into", "require", "required", "points", "university")),
    "Colleges usually ask for five GCSEs at grade 4 or above, including maths and English, and a "
    "sixth form taking A levels often wants a 6 in the subjects you pick - a 6 in maths for maths, "
    "for instance. The points people talk about are just that arithmetic: a grade 4 is worth 4, so "
    "five grade 4s is 20 points, and each college publishes what it asks for. If English or maths "
    "is below 4, most colleges will let you take it alongside the course rather than turn you away,"
    " so ring admissions with the exact course and ask.",
    avoid=("driving", "licence", "license", "theory test", "penalty", "speeding", "blood",
           "grade 4 mean", "what is a grade", "what does a grade",
           "oil", "oils", "engine", "engines", "car", "cars", "petrol", "diesel", "fuel",
           "tyre", "tyres", "brake", "brakes", "coolant", "wood", "timber", "steel",
           "meat", "beef", "steak", "coffee", "paint", "milk", "eggs", "whisky", "wine",
           "nurse", "nursing", "teacher", "teaching", "vet", "veterinary", "doctor",
           "lawyer", "solicitor", "midwife", "electrician",
           "ucas points", "ucas tariff", "ucs points")))

ENTRIES.append(entry(
    "ucas-points",
    (("ucas points", "ucas tariff", "ucas tariff points", "ucs points", "tariff points"),
     ("how many", "how much", "need", "needed", "do i need", "are", "is", "does", "my",
      "points", "level", "a level", "btec", "university", "course", "offer", "get")),
    "UCAS tariff points come from level 3 qualifications only, so GCSEs carry none: an A level "
    "is 48 points at grade A, 40 at B, 32 at C, 24 at D and 16 at E, and a BTEC Extended Diploma "
    "can score more than three A levels. Add them up across everything you have and compare with "
    "the course page, which usually prints both the points and the grades it asks for - when the "
    "grades are the offer, the points are only the summary.",
    avoid=("gcse", "gcses", "sixth form", "college place"),
    bias=2))

ENTRIES.append(entry(
    "a-levels-count",
    (("how many a levels", "how many a level", "how many subjects at a level",
      "how many subjects for a level", "three or four a levels", "four a levels",
      "how many a levels should i take"),
     ("how many", "should i take", "should i do", "need", "take", "do", "three", "four",
      "a level", "a levels", "subjects", "sixth form", "college")),
    "Three A levels is the standard full programme and what nearly every offer is written on; "
    "take four only if one is further maths, or if you are keeping a fourth for a course that "
    "asks for it, because a fourth A level rarely improves an offer and always costs marks in the "
    "other three. Two A levels plus a BTEC or an EPQ is a normal shape too - check the entry "
    "requirements for two or three courses before you choose the number.",
    avoid=("university", "uni", "ucas", "grade", "grades", "drop", "results day", "fail")))

_GRADES_ROUTE = (
    (("doctor", "medical school", "medicine"),
     "Medicine wants strong GCSEs, usually 5s and 6s including maths, English and a science, then "
     "A level chemistry plus one more science or maths, and some work experience in a care setting "
     "before you apply."),
    (("pharmacist", "pharmacy"),
     "Pharmacy wants A level chemistry and one other science, then the four-year MPharm and the "
     "year of training after it."),
    (("physiotherapist", "physiotherapy"),
     "Physiotherapy wants A level biology, most courses ask for a B or above at A level, and then "
     "the degree."),
    (("architect", "architecture"),
     "Architecture wants A level maths or physics, then the degree, then two years of practice "
     "before the final exam."),
    (("social worker", "social work"),
     "Social work wants GCSEs in English and maths, then a degree in social work, then "
     "registration with Social Work England."),
    (("police", "police officer"),
     "The police ask for a level 3 qualification - A levels or a BTEC both count - plus the "
     "fitness test and the background checks."),
)



def _job_grades(memory, understood):
    length = _the_length_answer((understood or {}).get("clean") or "", memory)
    if length:
        return length
    text = " " + " ".join(understood.get("words") or []) + " "
    first = ""
    for words, sentence in _GRADES_ROUTE:
        if any(" %s " % word in text for word in words):
            first = sentence
            break
    if not first:
        first = ("The route sets the grades, so there is no single number: the job names the course, "
                 "and the course names the subjects.")
    return (first + " Check the entry requirements on two or three course pages before you apply, "
            "because the subjects named there are what decide it - a grade below them is the thing "
            "to fix first, and a course that asks for less is the fallback.")


ENTRIES.append(entry(
    "job-grades",
    (("what grades do i need to be a", "what gcses do i need to be a", "grades do i need to be a",
      "gcses do i need to be a", "how many gcses do i need to be a", "gcses do i need for",
      "gcses to be a", "grades to be a", "what grades for", "what gcses for",
      "what do i need to be a", "grades do i need for", "grades do i need to be an",
      "gcses do i need to be an", "what grades do i need to be an", "grades to be an",
      "how many gcses to be a", "how many gcses for"),
     ("doctor", "medicine", "medical school", "pharmacist", "pharmacy", "physiotherapist",
      "physiotherapy", "architect", "architecture", "social worker", "social work", "police",
      "police officer")),
    _job_grades,
    bias=3))

ENTRIES.append(entry(
    "job-route",
    (("become", "becoming", "get into", "getting into", "qualify as", "train as", "want to be",
      "how do i become", "how i become", "what do i need to",
      "do i need a degree", "need a degree to", "degree to be", "degree to become",
      "a degree to", "to be a", "to be an"),
     ("doctor", "medical school", "medicine", "pharmacist", "pharmacy", "physiotherapist",
      "physiotherapy", "architect", "architecture", "social worker", "social work", "police",
      "police officer")),
    _job_grades,
    avoid=("pension", "mortgage", "insurance", "credit", "ucl", "an apprentice", "apprenticeship",
           "my teacher", "my son", "my daughter", "my mum", "my dad"),
    bias=2))

ENTRIES.append(entry(
    "sixth-form-application",
    (("apply for college", "applying for college", "apply to college", "college application",
      "apply for sixth form", "apply to sixth form", "how do i apply for college"),
     ("how do i", "how can i", "do i", "when do i", "apply", "application", "deadline",
      "college", "sixth form", "place")),
    "Apply straight to the college, not through your school: every college has an online form "
    "on its own site, and for a September start the deadline is usually the spring before, with "
    "places filling from January. You apply before your GCSE results, the offer is conditional "
    "on the grades, and you confirm it on results day - so apply to two colleges if you are not "
    "sure, and ring admissions the week results come out if anything goes wrong.",
    avoid=("university", "uni", "ucas", "degree", "student finance", "job", "visa")))

ENTRIES.append(entry(
    "apprenticeship-how",
    (("apprenticeship", "apprenticeships", "apprentice", "apprentices"),
     ("get", "getting", "find", "finding", "apply", "applying", "start", "starting", "look",
      "looking", "search", "searching", "how", "where", "become", "becoming", "want", "wanted",
      "want to", "should")),
    "Apply to them like jobs, because that is what they are: the vacancies are on the government "
    "Find an Apprenticeship service (gov.uk in England, apprenticeships.scot in Scotland, "
    "careerswales in Wales, nidirect in Northern Ireland), and big employers also advertise on "
    "their own sites with closing dates in the autumn and winter before a September start, so "
    "apply months early and to several. They come at four levels: GCSE-level, A-level, higher "
    "(the first two years of a degree) and degree, and the degree ones are competitive and want "
    "A-levels or a good BTEC. You need English and maths at GCSE for most of them, and if you "
    "missed those the employer usually puts you through them alongside the job. Pay is at least "
    "the apprentice minimum wage and rises with each year, so check the travel before you accept: "
    "a low wage plus a long commute is the thing people regret.",
    avoid=("degree apprenticeship", "degree apprenticeships", "worth it", "worth doing",
           "how many hours", "holidays", "time off", "overtime", "part time", "shift",
           "better than", "instead of university", "rather than university", "levy",
           "my employer", "our company", "we want to hire", "i employ"),
    ask=("how", "where", "what", "can i", "do i", "should i", "want to", "looking for",
         "help me", "advice")))

EXAM_WHEN = (
    "GCSE and A-level exams run from the middle of May to the middle of June, and the exact "
    "timetable for your subjects is published by the exam board - AQA, Edexcel, OCR or WJEC - "
    "about a year ahead, with the month-by-month dates on the board's site for the year you are "
    "sitting. Your school gives you your own timetable with the room and the start time once the "
    "entries are confirmed in February, and that is the one to go by. Results come out in the "
    "middle of August on a Thursday, with A-levels a week before GCSEs, and mocks sit in "
    "November or December before that."
)


def _exam_when(memory, understood):
    clean = ((understood or {}).get("clean") or "").lower()
    if re.search(r"(?<![a-z])mocks?(?![a-z])", clean):
        return ("Your school sets its own mock dates, and they are usually in November or December "
                "of the year before, so ask your head of year for the week rather than a "
                "national one. The summer exams themselves run from the middle of May to the "
                "middle of June, and the board's timetable for your subjects is on AQA, Edexcel, "
                "OCR or WJEC's site about a year ahead.")
    return EXAM_WHEN


ENTRIES.append(entry(
    "exam-dates",
    (("gcse", "gcses", "a level", "a levels", "alevels", "national 5", "higher", "highers",
      "mock", "mocks", "exams"),
     ("when", "what date", "which date", "start", "starts",
      "starting", "begin", "begins", "timetable", "timings", "how long until")),
    _exam_when,
    avoid=NOT_AN_EXAM + ("predicted", "predicted grade", "predicted grades",
                         "practice paper", "practice papers",
                         "results day", "my results", "got my results", "failed",
                         "fail", "clearing", "remark", "resit", "revise", "revising",
                         "revision", "timetable for revision", "how do i", "best way"),
    ask=("when", "what date", "which date", "dates", "how long until", "timetable"),
    bias=1))


CAREER_SUBJECTS = (
    (("nurse", "nursing"),
     "Nursing wants five GCSEs at grade 4 or above, including English, maths and a science, and "
     "then a nursing degree, a nursing associate apprenticeship or a degree apprenticeship at a "
     "trust. Most universities also ask for A-levels or a BTEC in a science or health subject, and "
     "care experience - a care home, a hospice, a hospital volunteer - is what separates people "
     "with the same grades. Check the entry requirements for each course, because they differ."),
    (("midwife", "midwifery"),
     "Midwifery asks for the same five GCSEs at grade 4 or above, English, maths and a science "
     "among them, and then a midwifery degree or one of the new midwifery apprenticeships. It is "
     "one of the most competitive courses there is, so care or maternity experience and a week "
     "spent shadowing a midwife are worth more than an extra A-level."),
    (("doctor", "medicine", "medical school", "surgeon"),
     "Medicine wants strong GCSEs, usually 5s and 6s including maths, English and science, then "
     "A-level chemistry plus one more science or maths, because nearly every medical school "
     "requires chemistry. Then it is a five-year degree, the UCAT test in the summer before you "
     "apply, and work experience or volunteering in a care setting; the interview is about what "
     "you saw there."),
    (("teacher", "teaching", "primary school teacher", "secondary school teacher"),
     "Teaching wants GCSEs at grade 4 or above in English and maths, plus a science for primary, "
     "then a degree in a subject schools teach, then a PGCE or a school-based training place - or "
     "a teaching apprenticeship, where you are paid while you train. Primary teaching takes any "
     "degree but checks your curriculum subjects, and secondary wants the subject you will teach."),
    (("vet", "veterinary", "vet school"),
     "Veterinary medicine wants A-level chemistry and usually biology, grades A or A*, and weeks "
     "of work experience with animals - a farm, a stable, a vet practice - before you apply. The "
     "degree is five years and hard to get into, so apply to two or three vet schools and have a "
     "second choice you would genuinely take."),
    (("lawyer", "law", "solicitor", "barrister", "law degree"),
     "Law takes no particular A-levels: grades and a degree matter, and any subject is fine, so "
     "pick what you will do well in. The law degree (or any degree plus the conversion course) is "
     "followed by the SQE exams for solicitors or the bar course for barristers, and the thing "
     "that gets you a training place is experience - a law centre, a solicitor's office, mooting "
     "at university."),
    (("engineer", "engineering", "mechanical engineer", "civil engineer", "electrical engineer"),
     "Engineering wants A-level maths and physics, then an accredited MEng or BEng degree, and the "
     "accreditation is the part to check because it is what leads to chartership. The other route "
     "is a degree apprenticeship with an employer, which pays from day one and ends with the same "
     "qualification, or a technician apprenticeship if you would rather start with your hands."),
    (("accountant", "accountancy", "accounting", "chartered accountant"),
     "Accountancy asks for no fixed subjects, though maths and a numerical subject help, and there "
     "are three ways in: A-levels then an AAT or ACCA/ACA training contract, a degree then the "
     "same exams, or an accountancy degree apprenticeship where the employer pays for the exams. "
     "The exams are the qualification either way, so the route with the least debt is usually the "
     "apprenticeship."),
    (("paramedic", "paramedic science"),
     "Paramedic science wants a science A-level or an access course, and usually GCSEs at grade 4 "
     "or above in English, maths and science, then a three-year paramedic science degree - or the "
     "technician route inside an ambulance service, which pays while you train. Get a first aid "
     "certificate and some time in a care or St John Ambulance role first, because the courses and "
     "the interviews both ask what you have seen."),
    (("electrician", "plumber", "plumbing", "mechanic", "chef", "carpenter",
      "bricklayer", "joiner", "gas engineer"),
     "The trades ask for no GCSEs to start, though English and maths help with the theory and "
     "employers usually want 4s in them. The way in is an apprenticeship - level 2 then level 3 "
     "with an NVQ - or a college course alongside finding an employer yourself, and for gas, "
     "electrics and heating there is a registration scheme at the end that you cannot skip. Ring "
     "local firms and ask for a trial week: that is how most people get taken on."),
)

THE_GENERAL_CAREER = (
    "Check the entry requirements on the university or college page for the exact course, because "
    "they differ more than people expect - most want five GCSEs at grade 4 or above including "
    "English and maths, and A-levels or a BTEC in a subject that fits. Pick the subjects that keep "
    "two doors open rather than one, and ask a teacher or someone doing the job now what they "
    "actually needed.")


JOB_LENGTHS = (
    (("nurse", "nursing"),
     "Three years for a nursing degree, two for a nursing associate course, or four on a degree "
     "apprenticeship where you are paid while you train.",
     "A return-to-practice course, not the degree again: about 450 hours of supervised practice "
     "and a short theory module, which most trusts run over three to six months, and they tell "
     "you which one they take at the interview."),
    (("midwife", "midwifery"),
     "Three years for a midwifery degree, or four years on a midwifery apprenticeship, which "
     "pays while you train.",
     "A return-to-practice course of a few months supervised in a maternity unit, rather than the "
     "degree again, if you have let your registration lapse."),
    (("dentist", "dentistry", "dental school", "dental surgeon"),
     "Five years at dental school, then a year of dental foundation training in a practice "
     "before you can work on your own, so six years from starting to being paid as a dentist.",
     "A return-to-practice or the overseas registration exam rather than the degree again: "
     "around a year of study and supervised practice, and the General Dental Council says which "
     "route your qualification needs."),
    (("doctor", "medicine", "medical school", "surgeon"),
     "Five years at medical school, then two foundation years in a hospital before you can apply "
     "for specialty training, which runs from three to eight years depending on the field.",
     "If you qualified as a doctor abroad, the route is the PLAB exams and then a couple of years "
     "in a training post, not a second degree."),
    (("teacher", "teaching", "primary school teacher", "secondary school teacher"),
     "Three years for a degree and then one more for a PGCE or a school-based training year, so "
     "four in all, or about the same on a teaching apprenticeship, which pays.",
     "A refresher course of a few weeks rather than a second degree, if you taught before and let "
     "the registration go."),
    (("vet", "veterinary", "vet school"),
     "Five years at vet school, and there is no shorter route into it.",
     ""),
    (("lawyer", "law", "solicitor", "barrister", "law degree"),
     "Three years for a law degree, then two years of qualifying work experience while you sit "
     "the SQE exams - so four to five years in all, or a year more if you do a conversion course "
     "instead of the law degree.",
     "A conversion course of a year, then the same two years of qualifying work experience."),
    (("engineer", "engineering", "mechanical engineer", "civil engineer", "electrical engineer"),
     "Four years for an MEng, or three for a BEng and then a few years of supervised work to "
     "chartership.",
     "A degree apprenticeship of four to six years, paid throughout, which is the usual way back "
     "in if you already work in the industry."),
    (("accountant", "accountancy", "accounting", "chartered accountant"),
     "Three to four years of exams, AAT first and then ACCA or ACA, taken while you work, so you "
     "are paid from the first year.",
     "The same three to four years of exams, starting at the level you left off at, and a firm "
     "will usually take you on as a trainee while you sit them."),
    (("paramedic", "paramedic science"),
     "Three years for a paramedic science degree, or about two years as an associate ambulance "
     "practitioner inside a trust, which pays.",
     ""),
    (("pharmacist", "pharmacy"),
     "Four years for an MPharm, then a year of foundation training in a pharmacy before you "
     "register.",
     "A refresher placement and the registration assessment rather than the degree again."),
    (("physiotherapist", "physiotherapy"),
     "Three years for a physiotherapy degree, or two on an accelerated Masters if you already "
     "have a degree in a science.",
     "A return-to-practice course of a few weeks, run by the Chartered Society of Physiotherapy, "
     "if you have been out of the register."),
    (("architect", "architecture"),
     "Three years for a degree, then two years of practical experience and the Part 3 exam - "
     "seven years in all, and the Part 3 is the part people underestimate.",
     "The Part 2 and Part 3 years, on top of the experience you already have, rather than the "
     "whole degree again."),
    (("social worker", "social work"),
     "Three years for a social work degree, or two on a Masters if your first degree is in "
     "something related, and there are fast-track programmes that pay a salary while you train.",
     "A return-to-practice course of a few weeks, and the register tells you what you need."),
    (("police", "police officer"),
     "No degree is needed: you apply to a force and train on the job, or take the three-year "
     "police constable degree apprenticeship, which is paid throughout.",
     "You go back in at your previous rank where the force allows it, with a short refresher "
     "rather than the full training again."),
    (("electrician", "plumber", "plumbing", "gas engineer"),
     "Three to four years for a level 3 apprenticeship, which is how nearly everyone gets in, and "
     "the gas or electrics registration adds a year or two after that.",
     "A level 2 refresher and the registration assessment rather than the whole apprenticeship."),
    (("chef",),
     "Two to three years as a commis chef through an apprenticeship or a college course, and you "
     "are paid from the first week.",
     "A short refresher in a kitchen and the level 2 assessment rather than the whole thing again."),
    (("mechanic", "carpenter", "bricklayer", "joiner"),
     "Three to four years for a level 3 apprenticeship, which is how nearly everyone gets in.",
     "A short refresher and the level 2 assessment rather than the whole apprenticeship."),
)

_ASKS_THE_LENGTH = re.compile(
    r"(?<![a-z])(?:how many years|how many months|how long|what length|"
    r"years of study|length of the course|length of the training)(?![a-z])")

_DONE_IT_BEFORE = re.compile(
    r"(?<![a-z])(?:retrain|retraining|retrained|go back to|going back to|went back to|"
    r"return to|returning to|returned to|years ago|used to be|i was a|i used to work|"
    r"lapsed|let it lapse|on a break|career break|years out|years off|years away)(?![a-z])")


def _the_job_row(text):
    words = " " + str(text or "").lower() + " "
    for names, length, returning in JOB_LENGTHS:
        for name in names:
            if re.search(r"(?<![a-z])" + re.escape(name) + r"(?![a-z])", words):
                return names, length, returning
    return None


def _the_length_answer(clean, memory=None):
    said = str(clean or "").lower()
    row = _the_job_row(said)
    if row is not None and isinstance(memory, dict):
        memory["career"] = row[0][0]
    elif row is None and isinstance(memory, dict) and isinstance(memory.get("career"), str):
        row = _the_job_row(memory["career"])
    if row is None or not _ASKS_THE_LENGTH.search(said):
        return None
    _, length, returning = row
    if returning and _DONE_IT_BEFORE.search(said):
        return returning
    return length


def _career_subjects(memory, understood):
    clean = ((understood or {}).get("clean") or "").lower()
    length = _the_length_answer(clean, memory)
    if length:
        return length
    row = _the_job_row(clean)
    if row is not None and isinstance(memory, dict):
        memory["career"] = row[0][0]
    for names, reply in CAREER_SUBJECTS:
        for name in names:
            if re.search(r"(?<![a-z])" + re.escape(name) + r"(?![a-z])", clean):
                return reply
    return THE_GENERAL_CAREER


ENTRIES.append(entry(
    "career-subjects",
    (("gcse", "gcses", "a level", "a levels", "alevels", "subjects", "grades", "qualifications",
      "entry requirements", "requirements",
      "ucas points", "how many points", "points do i need", "points needed", "points for",
      "nurse", "nursing", "midwife", "midwifery", "doctor", "medicine",
      "a teacher", "teachers", "primary teacher", "secondary teacher", "teacher training",
      "teach primary", "teach secondary",
      "teaching",
      "vet", "veterinary", "lawyer", "solicitor", "barrister", "engineer", "engineering",
      "accountant", "accountancy", "accounting", "electrician", "plumber",
      "mechanic", "chef", "carpenter", "bricklayer", "joiner", "paramedic"),
     ("need", "needs", "needed", "require", "requires", "required", "be a", "be an", "to be a",
      "to be an", "become", "becoming", "get into", "getting into", "get on", "take", "want",
      "go back to", "going back to", "return to", "returning to",
      "should i take", "what", "which", "for", "how",
      "good career", "a good career", "career", "careers", "retrain", "retraining", "retrained",
      "go back to", "back to", "return to", "job", "jobs", "worth it",
      "going back to", "returning to", "after 10 years", "after five years", "after 5 years",
      "after ten years", "years off", "years out", "years away")),
    _career_subjects,
    avoid=NOT_AN_EXAM + MOCK + (
                                "point of any", "point of it", "point of this", "point of all",
                                "point of that", "point anymore", "no point", "any point",
                                "f1", "formula 1", "formula one", "grand prix", "motogp",
                                "podium", "pole position", "try", "tries", "goal", "goals",
                                "touchdown", "conversion", "rugby", "football", "soccer",
                                "cricket", "netball", "basketball", "hockey", "tennis",
                                "league", "score", "scored", "scoring", "season",
                                "licence", "license", "penalty points", "speeding", "driving",
                                "banned", "parked", "road", "motorway", "insurance",
                                "ask a teacher", "ask my teacher", "ask the teacher",
                                "ask a lecturer", "ask my lecturer", "ask the lecturer",
                                "ask my tutor", "ask a tutor", "email my teacher",
                                "email a teacher", "email my lecturer", "email my tutor",
                                "ask for help", "for help", "struggling", "how do i ask",
                                "a question for", "ask a question",
                                "choose", "choosing", "choice of", "pick", "picking",
                                "my options", "options evening", "options form",
                                "complain", "complaint", "complaining", "rude", "unfair",
                                "shouted at me", "picked on", "my grades are",
                                "results day", "i got a", "got a grade", "bad grade", "failed",
                                "resit", "remark", "revise", "revising", "revision",
                                "my dog", "my cat", "my pet", "the dog", "the cat", "puppy",
                                "teach my", "teaching my", "teach a dog", "teach the dog",
                                "teach him", "teach her", "teach them", "teach it",
                                "how to teach", "teach someone", "teach me",
                                "kitten", "rabbit", "hamster", "horse", "pony", "livestock",
                                "boiler", "leak", "leaking", "dripping", "blocked", "fuse",
                                "fuse box", "rewire", "wiring", "socket", "sockets", "radiator",
                                "drain", "toilet", "tap", "shower", "washing machine",
                                "find a", "finding a", "how do i find", "where do i find",
                                "recommend", "recommended", "recommendation", "hire", "hiring",
                                "a good plumber", "a good electrician", "a good builder",
                                "a good decorator", "a good roofer", "trustworthy",
                                "reputable", "cowboy", "quote", "quotes", "tradesperson",
                                "tradesman", "a decent plumber", "a reliable plumber",
                                "find a good", "find a reliable", "find a decent",
                                "i need a plumber", "i need an electrician",
                                "i need a mechanic", "call a plumber", "call an electrician",
                                "call a mechanic", "car needs", "car wont", "car won't",
                                "team", "teams", "league", "netball", "football", "rugby",
                                "hockey", "cricket", "climbing", "bouldering", "piano",
                                "guitar", "violin", "flute", "music", "ballet", "dancing",
                                "drums", "singing", "road", "path", "flight", "hotel",
                                "restaurant", "steak", "coffee", "beef", "petrol", "diesel",
                                "what does a", "what do a", "do all day", "day to day",
                                "a day in the life",
                                "buy", "buying", "bought", "shopping", "shop for",
                                "bank", "joint", "savings", "current account", "my account",
                                "the account", "an account", "account number", "account details",
                                "my accounts", "online accounts",
                                "google", "facebook", "instagram", "snapchat", "tiktok",
                                "twitter", "linkedin", "social media", "gmail", "outlook",
                                "see a doctor", "my doctor", "the doctor", "book a doctor",
                                "book", "booking", "register with", "doctor's", "gp", "surgery",
                                "nhs", "hospital", "appointment", "waiting list", "referral",
                                "i feel", "im feeling", "i am feeling"),
    ask=("become", "becoming", "be a", "be an", "to be a", "to be an", "get into",
         "getting into", "qualify", "qualified", "train", "training", "study", "studying",
         "subjects", "subject", "grades", "grade", "gcse", "gcses", "a level", "a levels",
         "alevels", "qualifications", "qualification", "requirements", "entry requirements",
         "ucas", "ucas points", "points", "degree", "university", "college", "apprenticeship",
         "course", "career", "careers", "work experience", "what does", "what do i need",
         "what will i need", "how long does",
         "go back to", "going back to", "return to", "returning to",
         "job", "jobs", "worth it"),
    bias=1))

ENTRIES.append(entry(
    "dissertation",
    (("dissertation", "dissertations", "final year project", "final project",
      "undergraduate thesis", "masters thesis", "doctoral thesis", "capstone project"),
     ("what", "whats", "what is", "mean", "means", "definition", "how long", "how many words",
      "how do i", "how to", "start", "starting", "begin", "structure", "write", "writing",
      "word count", "length", "supervisor", "plan", "planning", "is a", "for")),
    "A dissertation is one long piece of work - usually 8,000 to 12,000 words for a bachelor's "
    "and up to 20,000 for a master's - where you answer one question of your own with evidence, "
    "rather than showing what you know about a subject. It is marked on the question, the reading "
    "and the argument, in that order. Start with a question narrow enough to answer in the word "
    "count, then a plan of four or five chapters, then read for that plan only. Book two "
    "supervisor meetings before Christmas and take a written note of what was agreed at each one: "
    "the students who fall behind are the ones who go quiet, not the ones who ask.",
    avoid=NOT_REVISION + ("marks", "mark", "grade", "grades", "extension", "extend",
                          "deadline", "late", "penalty", "plagiarism", "reference",
                          "supervisor never", "supervisor wont", "supervisor does not",
                          "supervisor doesnt", "supervisor ignores", "supervisor is useless",
                          "supervisor is awful", "my supervisor", "my tutor never"),
    bias=1,
))

ENTRIES.append(entry(
    "phd",
    (("phd", "ph.d", "doctorate", "doctoral", "dphil", "postgraduate research", "phd thesis"),
     ("what", "whats", "what is", "mean", "means", "definition", "how long", "how many years",
      "worth it", "should i", "funding", "funded", "cost", "how do i", "apply", "difference",
      "is a", "do i need", "for")),
    "A PhD is three to four years of full-time original research under a supervisor, ending in a "
    "thesis of about 60,000 to 80,000 words and a spoken exam called a viva: it trains you to "
    "produce new knowledge, and it is not required for most jobs outside research. Look for a "
    "funded place first - a studentship pays fees and a stipend, and the funded ones are "
    "advertised on FindAPhD and on university pages - because self-funding a PhD is expensive for "
    "the career it buys. Write to a named supervisor with a two-page proposal and ask what they "
    "have funding for, rather than applying to a department in general.",
    avoid=NOT_REVISION + ("marks", "grade", "grades", "essay", "revision", "exam", "gcse",
                          "a level", "child", "children", "kid", "kids", "my son", "my daughter",
                          "or get a job", "or a job", "phd or", "masters or", "or a masters",
                          "worth it", "worth the money", "worth the cost", "worth the debt", "interview",
                          "should i do", "should i", "is it worth", "should i bother",
                          "interview for", "prepare for an interview"),
    bias=1,
))

ENTRIES.append(entry(
    "dyslexia-reading",
    (("dyslexic", "dyslexia", "reading is slow", "reading takes forever", "reading takes me ages",
      "words jump", "words move on the page", "letters move", "read slowly", "slow reader"),
     ("read", "reading", "study", "studying", "revision", "revise", "exam", "exams", "uni",
      "university", "school", "college", "how do i", "help", "cope", "takes forever", "slow",
      "takes me", "struggle", "struggling")),
    "Ask for the formal help first: a dyslexia assessment at university goes through the "
    "disability service, and it unlocks extra time in exams, a reader or text-to-speech software, "
    "and often a grant for equipment - at school it is the SENCO, and it costs you nothing to ask. "
    "For the reading itself, use text-to-speech so the page reads to you while you follow with a "
    "finger, take the chapter in 20-minute blocks with the summary read first, and ask for the "
    "reading list in advance so you are never reading against a deadline. Being slow at decoding "
    "is not being slow at thinking, and the extra time is the standard fix, not a favour.",
    avoid=("my son", "my daughter", "my child", "my kid", "year old", "toddler", "baby",
           "spelling test", "handwriting"),
    bias=1,
))

EXTENSION_ASK = ("extension", "extensions", "extend", "mitigating circumstances", "mitigation",
                 "extenuating circumstances", "special circumstances", "more time",
                 "late submission", "submit late", "hand in late", "extra time")
ESSAY_WORDS = ("essay", "essays", "coursework", "assignment", "assignments", "dissertation",
               "project write-up", "lab report", "thesis", "submission", "portfolio",
               "exam", "exams", "module")

ENTRIES.append(entry(
    "essay-extension",
    ((EXTENSION_ASK + ("deadline", "deadlines")),
     (ESSAY_WORDS + ("how do i", "ask", "asking", "get", "apply", "tutor", "lecturer",
                     "teacher", "professor", "module leader", "uni", "university", "school",
                     "college", "who do i", "can i", "what do i", "email", "form"))),
    "Ask the module leader or tutor before the deadline, in writing, with the date you need - and "
    "ask what the evidence rule is at your place, because it is a form with a name: mitigating "
    "circumstances, extenuating circumstances or special circumstances. Send the form and the "
    "evidence (a GP note, a letter, a hospital appointment) in one email, and keep a copy. The "
    "standard extension is a week or two for a short illness; longer or repeated problems go to "
    "the mitigating circumstances panel rather than to your tutor. Ask early: most universities "
    "will not accept a claim made after the deadline has passed, and asking costs nothing.",
    avoid=("boss", "manager", "client", "at work", "my job", "council", "tax return", "visa",
           "rent", "landlord", "planning permission", "mortgage", "insurance"),
    ask=ESSAY_WORDS + ("mitigating circumstances", "mitigating", "extenuating", "tutor",
                       "lecturer", "module leader", "professor", "uni", "university",
                       "school", "college"),
    bias=1,
))

ENTRIES.append(entry(
    "missed-essay-deadline",
    (("missed the deadline", "missed my deadline", "miss a deadline", "missed a deadline",
      "handed in late", "submitted late", "late submission", "missed the submission",
      "deadline passed", "deadline has passed", "deadline gone", "didnt submit",
      "didn't submit", "wasnt in on time", "wasn't in on time",
      "missed my coursework", "missed the coursework", "missed my essay", "missed the essay",
      "missed my assignment", "missed my submission", "coursework deadline", "essay deadline",
      "deadline for my essay", "deadline for the essay", "deadline for my coursework"),
     (ESSAY_WORDS + ("uni", "university", "school", "college", "module", "tutor", "lecturer",
                     "teacher", "what happens", "what now", "what do i do", "will i fail",
                     "fail", "penalty", "capped", "resit", "appeal", "talk to", "email"))),
    "Email the module leader today, before they chase you: say the piece is late, give the reason "
    "in one sentence and name the date you will submit. Most places take 10% off a day up to a "
    "cap of a pass mark for a few days, and the late penalty is usually shown on your marks "
    "breakdown - check your module handbook for the exact rule rather than guessing. If the "
    "reason was illness or something serious, ask for mitigating circumstances now: it can remove "
    "the late penalty and give you a resit as if for the first time. Silence is the only version "
    "where nothing can be fixed.",
    avoid=("boss", "manager", "client", "at work", "my job", "council", "tax return", "visa",
           "rent", "landlord", "planning permission", "mortgage", "insurance", "car", "mot",
           "report", "the report", "the figures", "client", "board", "audit", "invoice"),
    bias=2,
))

ENTRIES.append(entry(
    "apprentice-hours",
    (("apprentice", "apprentices", "apprenticeship", "apprenticeships"),
     ("hours", "hour", "how many hours", "how long", "time off", "holiday", "holidays",
      "overtime", "week", "a week", "work", "can i work", "allowed to work", "part time",
      "evenings", "weekends", "shifts")),
    "At least 30 hours a week of paid work, and an apprentice under 18 cannot be asked to do "
    "more than 40 hours a week or more than 8 hours a day. Everyone still counts the 28 days' "
    "paid holiday a year, bank holidays on top if the contract says so, and the off-the-job "
    "training - about a fifth of the hours - happens inside your paid time rather than after it. "
    "Overtime is allowed if you are over 18 and it is in the contract, and the 48-hour average "
    "week limit applies as it does to any job.",
    bias=1,
))

ENTRIES.append(entry(
    "a-deadline-and-nothing-written",
    (("essay", "essays", "assignment", "assignments", "coursework", "dissertation",
      "piece of work", "thesis",
      "words", "word count"),
     ("due", "deadline", "deadlines", "hand in", "hand-in", "handing in", "submit",
      "submission", "last minute", "behind",
      "havent started", "haven t started", "not started", "havent done", "haven t done",
      "left it", "running out of time", "no time"),
     ("due", "deadline", "hand in", "hand-in", "submit", "submission", "last minute", "behind",
      "havent started", "haven t started", "not started", "havent done", "haven t done",
      "left it", "running out of time", "no time")),
    "Work backwards from the deadline: decide the three or four points that answer the "
    "question, put a heading for each, write the middle sections badly and fast, then the "
    "introduction and the conclusion last, then read it out loud once. Ask "
    "for a short extension today rather than after the deadline and put the request in writing, "
    "because most tutors will say yes before the date and almost none can after it. A complete "
    "plain answer scores more than a perfect first half, so hand in every section, even thin.",
    avoid=("revise", "revising", "revision", "exam", "exams", "mock", "past paper", "how do i",
           "how to", "how can i", "what should i write", "structure", "introduction",
           "conclusion", "reference", "references", "citation", "cite", "plagiaris",
           "spelling", "grammar", "word count", "grade", "marks",
           "my son", "my daughter", "my kid", "my child", "my boy", "my girl", "my children",
           "his teacher", "her teacher", "the teacher", "school report", "at work",
           "my boss", "to my boss", "the boss", "for work", "client"),
    bias=1,
))


_CHILD = ("child", "children", "kid", "kids", "son", "daughter", "boy", "girl", "toddler",
          "youngest", "eldest", "reception", "reception class", "preschool", "nursery",
          "year old", "year-old", "4 year old", "5 year old", "6 year old", "7 year old")

_AGE_SAID = (re.compile(r"\b(\d{1,2})\s*(?:year|yr)s?[\s-]*(?:old|young)\b"),
             re.compile(r"\b(?:is|at|aged|age|turned|nearly)\s+(\d{1,2})\b"),
             re.compile(r"\b(\d{1,2})\s*(?:and|,)\s*(?:cant|can't|cannot|doesnt|doesn't|"
                        r"still|only|hasnt|hasn't)\b"))


def _the_age_of_a_child(reading):
    said = " ".join(str((reading or {}).get("clean") or "").lower().split())
    for pattern in _AGE_SAID:
        found = pattern.search(said)
        if found:
            try:
                age = int(found.group(1))
            except (TypeError, ValueError):
                continue
            if 0 < age <= 18:
                return age
    return None


_WRITING_HAND = (
    "Give the hand other work first - threading, cutting, playdough, big chalk on the path - and "
    "practise the name in short bursts with a chunky pencil and a dotted version to trace, five "
    "minutes at a time and no more.")


def the_writing_card(memory, reading):
    age = _the_age_of_a_child(reading)
    if age is not None and age <= 4:
        return ("At three or four that is not late at all: the shoulder and hand are still "
                "building, and a child who cannot write their name yet is exactly on time. "
                + _WRITING_HAND + " Nobody should be sitting a four year old down to drill it, "
                "and if a five year old cannot hold a pencil or copy a circle, that is worth a "
                "word with the health visitor.")
    if age is not None and age >= 7:
        return ("At seven this is past the usual age, so get it looked at rather than practised "
                "harder: most children write a recognisable name by five or six. Ask the teacher "
                "what it looks like in class, have hearing and vision checked, and if it is just "
                "the same at school ask about handwriting practice with an occupational therapist "
                "or the SENCO. Keep the practice at home short and keep the worry off it.")
    if age is not None:
        return ("Late but still inside normal, and worth a light touch rather than a push: most "
                "children write a recognisable name between four and six. " + _WRITING_HAND +
                " Ask the teacher whether the grip looks right, and if it has not moved by the "
                "end of the year get hearing and vision checked.")
    return ("Five is early for a name and nothing to worry about: the shoulder and hand are still "
            "building, so most children get a recognisable name somewhere between four and six. "
            + _WRITING_HAND.replace("Give the hand", "Give the hand") + " Worth asking nursery or "
            "the reception teacher whether the grip is right, and worth a word with the health "
            "visitor if a child of six cannot hold a pencil or copy a circle at all.")
ENTRIES.append(entry(
    "child-cant-write-his-name",
    (_CHILD,
     ("write his name", "write her name", "write their name", "write his own name",
      "write her own name", "writes his name", "writes her name", "writing his name",
      "writing her name", "write the name", "write name", "write his", "write her",
      "cant write", "can't write", "cannot write", "cant hold a pencil", "cant hold the pencil",
      "pencil grip", "holds a pencil", "hold a pencil", "holding a pencil", "pencil properly",
      "letter formation", "write letters", "writing letters", "recognise his name",
      "recognise her name", "know his letters", "know her letters", "learn to write",
      "scribbles", "wont write", "hates writing", "hate writing")),
    the_writing_card,
    avoid=("my handwriting", "handwriting", "my writing", "neater", "neatly", "spelling",
           "grammar", "signature", "copy", "font", "illegible", "my notes", "my essay",
           "school place", "choose a school", "apply for a school", "adult", "i cant write"),
    bias=1))


ENTRIES.append(entry(
    "child-exam-nerves",
    (("exam", "exams", "tests", "mocks", "revision", "revising", "gcses", "gcse", "a levels",
      "a level", "sats", "school tests"),
     _CHILD + ("teenager", "teenagers", "teen", "year old", "year-old", "15 year old",
               "16 year old", "17 year old", "she", "he"),
     ("cant sleep", "can't sleep", "not sleeping", "wont sleep", "won't sleep", "up late",
      "staying up", "awake", "tired", "nervous", "worried", "worry", "stressed", "stress",
      "anxious", "panic", "crying", "cries", "not eating", "off their food", "revision")),
    "Take the pressure off the night, not the work: the revision is done by then, so the job is a "
    "fixed stop time, the phone out of the room, and something that is not revision for the hour "
    "before bed. Keep the worry concrete - ask what they are most afraid of forgetting, write it "
    "down and leave it on the desk, because a written worry stops the circling. If the exams are "
    "weeks away and sleep is still gone, or they are not eating or cannot get to school, tell "
    "their tutor, because that is worth more than any technique.",
    ask=("cant sleep", "can't sleep", "not sleeping", "wont sleep", "won't sleep", "up late",
         "staying up", "awake", "tired", "nervous", "worried", "worry", "stressed", "stress",
         "anxious", "panic", "crying", "cries", "not eating", "off their food", "nerves"),
    avoid=("my exams", "my revision", "im revising", "i cant sleep", "i can't sleep",
           "i am revising", "toddler", "baby", "cot", "crib", "nursery", "my exam",
           "my test", "my driving test", "blood test", "pregnancy test", "urine"),
    bias=1))
_ASKED_TO_MOVE = ("how", "what", "when", "which", "why", "can i", "could i", "should",
                  "should i", "do i", "is it", "too late", "wrong", "regret", "hate",
                  "want to", "worth it", "thinking of", "considering", "decided", "allowed",
                  "possible", "advice", "help", "best",
                  "first year", "second year", "third year", "year 10", "year 11", "year 12",
                  "year 13", "halfway through", "just started", "already started")

_THE_ANNOUNCEMENT = ("changing subject", "changing subjects", "changing the subject",
                     "changing topic", "changing the topic", "change topic", "change of subject",
                     "moving on", "next subject", "different subject", "different topic")
_LEAD_IN = ("what about", "how about", "what", "and", "but", "so", "ok", "okay", "anyway",
            "right", "well", "now", "then", "also", "plus", "just", "let us", "lets",
            "let's", "can we", "can i", "could we", "shall we", "maybe")


def _asks_to_move(understood):
    said = " " + " ".join(str((understood or {}).get("plain")
                              or (understood or {}).get("text") or "").lower().split()) + " "
    bare = said.strip(" .,!?;:-\u2026")
    changed = True
    while changed:
        changed = False
        for lead in _LEAD_IN:
            if bare == lead or bare.startswith(lead + " "):
                bare = bare[len(lead):].strip(" ,")
                changed = True
    if bare in _THE_ANNOUNCEMENT:
        return False
    return any((" " + word + " ") in said or said.startswith(" " + word + " ")
               or said.rstrip().endswith(" " + word) for word in _ASKED_TO_MOVE)
ENTRIES.append(entry(
    "change-subject-or-course",
    (("change", "changing", "changed", "switch", "switching", "swap", "swapping", "transfer",
      "transferring", "move", "moving", "drop", "dropping", "quit", "quitting", "hate",
      "hating", "wrong", "regret", "regretting", "stuck with",
      "change my a level", "change a level", "change my a levels", "change a levels",
      "change my subject", "change subjects", "change my course",
      "change course", "change courses", "change my degree", "change degrees",
      "changing subjects", "changing course", "changing courses",
      "changing degree", "changing my degree", "changing my course", "changing my subjects",
      "switching subject", "switching subjects", "switching course", "switching courses",
      "switching degree", "switching degrees", "switching my course",
      "switch course", "switch courses", "switch degree", "switch degrees",
      "wrong a levels", "wrong a level",
      "hate my course", "hate my uni", "hate my degree", "regret my degree",
      "regret my course", "too late to change"),
     ("a level", "a levels", "a-level", "as level", "subjects", "subject", "course", "courses",
      "degree", "uni", "university", "college", "gcse", "gcses", "sixth form", "year 12",
      "year 13", "year 10", "first year", "second year", "apprenticeship")),
    ("You can usually still change it, and the sooner you ask the easier it is: at school or "
     "college, go to the head of sixth form or the exams officer, and a change is normally "
     "possible in the first two or three weeks of Year 12 - after that it is their call, and how "
     "much you would catch up that decides it. At university, ask your personal tutor or the "
     "course leader about transferring to another course at the same place before you think "
     "about leaving, which is usually easier than a fresh application through UCAS or Clearing. "
     "Changing after a full year costs money as well as time, because student finance does not "
     "normally fund a second first year."),
    ask=_ASKED_TO_MOVE,
    guard=_asks_to_move,
    avoid=("drop a subject", "drop my subject", "drop an a level", "drop a level",
           "drop one of my a levels", "drop one of my", "dropping a level", "dropping an a level",
           "drop as level", "quit a subject", "give up a subject", "dropping a subject",
           "change the subject", "the subject to",
           "course offer", "university offer", "uni offer", "firm offer",
           "job", "jobs", "boss", "career", "careers", "my work", "at work", "address", "bank",
           "energy", "supplier", "broadband", "mobile", "insurance", "password", "email",
           "car", "boiler", "vet", "dog", "cat", "recipe", "diet", "gym", "running", "hair",
           "doctor", "medication", "dressing", "nappy", "light bulb", "bedding", "taps",
           "course of", "steroids", "antibiotics", "how i feel", "my mood"),
    bias=2,
))

CATCHING_UP = (
    "Find the first topic you stopped understanding rather than the newest one, because everything "
    "after it is built on it: go through the textbook contents or the topic list and mark the last "
    "thing that made sense. Then do three things - tell the teacher you have fallen behind and ask "
    "which two topics matter most for the next test, spend twenty minutes a day on those two only, "
    "and get one session with a classmate who is good at them. Catching up is a short list worked "
    "through patiently, not the whole course read again.")

ENTRIES.append(entry(
    "catching-up-at-school",
    (("fallen behind", "fell behind", "behind at school", "behind in class",
     "catch up at school", "catch up in class", "catch up at college",
     "catch up on school", "catch up on schoolwork", "catch up on classwork",
     "catch up on lessons", "catch up on the work",
     "catch up on everything at school", "catch up on everything in class",
     "catch up after being off", "catching up at school", "catching up in class",
     "missed a lot", "missed lessons",
     "missed school", "missed classes", "a lot of school", "months off school",
     "off school for months", "off school for weeks",
     "gaps in my knowledge", "dont understand anything", "don't understand anything",
     "no idea what is going on", "lost at school", "struggling at school", "struggling in class",
     "school work", "schoolwork", "classwork", "coursework"),
     ("how do i", "how", "catch up", "catching up", "help", "behind", "school", "class",
      "college", "teacher", "subject", "start", "should i", "what do i do")),
    CATCHING_UP,
    ask=("how", "catch up", "catching up", "help", "behind", "start", "what do i do", "should i",
         "missed a lot", "missed school", "missed lessons", "missed classes", "a lot of school",
         "months off school", "off school for months", "off school for weeks"),
    avoid=("ill", "illness", "sick", "hospital", "diagnosis", "anxiety", "depressed", "depression",
           "adhd", "autism", "dyslexia", "statement", "ehcp", "sen", "expelled", "excluded",
           "bully", "bullied", "bullying", "rent", "mortgage", "bill", "bills", "credit",
           "loan", "sleep", "penalty", "fine", "council", "truancy", "attendance",
           "snow", "snowing", "snowed", "snow day", "closed", "shut", "strike", "inset day",
           "holidays", "half term", "summer holiday", "bored", "my children", "my kids",
           "the children", "the kids", "toddler", "nursery",
           "son", "sons", "daughter", "daughters", "child", "teenager", "teenagers", "teen",
           "stepson", "stepdaughter", "my boy", "my girl", "his school", "her school",
           "their school", "his teacher", "her teacher", "their teacher",
           "email", "emails", "inbox", "deadline", "deadlines", "boss", "job", "jobs",
           "project", "projects", "client", "clients", "paperwork", "timesheet", "overtime",
           "workload", "office", "meeting", "meetings", "shift",
           "my work", "at work", "on my work", "for work", "with work", "his work", "her work"),
    bias=1))
