import re

from ..memory import last_bot
from .badnews import reads_as_bad_news, reads_as_pregnancy_bleeding, reads_as_sudden_loss, \
    reads_like_a_symptom
from .loss import names_a_feeling

OFFER = re.compile(r"\bi can draft that\b|\bi can write it\b|\bi'll draft it\b|"
                   r"\bi'll write something you can send\b|\bgive me the gist and i'll draft it\b|"
                   r"\bi(?:'ll|\s+(?:can|could|will|would)) write (?:it|yours|one|that)\b|"
                   r"\bwrite (?:it|yours|one) for you\b")

FORMAL = frozenset((
    "boss", "manager", "employer", "company", "hr", "work", "workplace", "office",
    "landlord", "landlady", "letting", "agent", "lettings", "housing", "council",
    "school", "head", "headteacher", "teacher", "tutor", "nursery", "childminder",
    "university", "college", "lecturer", "professor", "surgery", "gp", "doctor", "dentist",
    "hospital", "clinic", "bank", "insurer", "insurance", "utility", "energy", "council",
    "department", "tenant", "customer", "client", "supplier", "landlord's",
))

LEADS = (
    (re.compile(r"^(?:and\s+|so\s+|ok\s+|okay\s+|well\s+|right\s+)?(?:it'?s\s+|its\s+)?"
                r"(?:saying|say|to\s+say|i\s+was\s+going\s+to\s+say)\s+(?:that\s+)?(?:i\s+)?"
                r"(?:am\s+|was\s+)?(?=\w)"), "said"),
    (re.compile(r"^(?:and\s+|so\s+|ok\s+|okay\s+|right\s+)?(?:it'?s\s+|its\s+)?"
                r"(?:asking|ask|to\s+ask)\s+(?:for|about)\s+"), "asked"),
    (re.compile(r"^(?:and\s+|so\s+|ok\s+|okay\s+|right\s+)?(?:it'?s\s+|its\s+)?"
                r"(?:to\s+say|saying|the\s+message\s+is)\s+(?:that\s+)?"), "said"),
    (re.compile(r"^(?:and\s+|so\s+|ok\s+|okay\s+|well\s+|right\s+)?"
                r"(?:telling|told)\s+(?:them|him|her)\s+(?:that\s+)?"), "told"),
    (re.compile(r"^(?:and\s+|so\s+|ok\s+|okay\s+|well\s+|right\s+)?(?:"
                r"i\s+(?:just\s+)?(?:want|need|would\s+like)\s+to\s+say|"
                r"i(?:'d|\s+would)\s+like\s+to\s+say|let\s+(?:them|him|her)\s+know|"
                r"tell\s+(?:them|him|her))\s+(?:that\s+)?"), "said"),
    (re.compile(r"^(?:and\s+|so\s+|ok\s+|okay\s+|right\s+)?(?:that\s+|it'?s\s+)"), "said"),
)

TIDY = {
    "im": "I'm", "i": "I", "ive": "I've", "id": "I'd",
    "cant": "can't", "wont": "won't", "dont": "don't", "doesnt": "doesn't", "didnt": "didn't",
    "isnt": "isn't", "wasnt": "wasn't", "couldnt": "couldn't", "wouldnt": "wouldn't",
    "shouldnt": "shouldn't", "havent": "haven't", "thats": "that's", "theres": "there's",
    "whats": "what's", "lets": "let's", "pls": "please", "plz": "please", "thx": "thanks",
    "tmrw": "tomorrow", "tomoz": "tomorrow", "tomorow": "tomorrow", "tommorow": "tomorrow",
    "u": "you", "ur": "your", "n": "and", "cos": "because", "coz": "because",
    "appt": "appointment", "appointment's": "appointment's", "meds": "medication",
    "i'll": "I'll",
}

ABSENT = re.compile(r"\b(?:off\s+(?:sick|ill|work)|sick\s+(?:leave|note|pay)|"
                    r"day\s+off|time\s+off|not\s+coming\s+in|won'?t\s+be\s+in|"
                    r"cant\s+come\s+in|can'?t\s+come\s+in)\b")

THIRD_PERSON = re.compile(r"\b(?:her|him|them|his|hers|they|she|he)\b")

APOLOGY = re.compile(r"^(?:i'?m\s+|i\s+am\s+)?sorry\b|^apolog(?:y|ise|ize)\b")
APOLOGY_ACT = re.compile(r"\bsorry\s+(?:for|about)\s+(?:being\s+)?([a-z']+ing)\b"
                         r"|\bsorry\s+(?:that\s+)?(?:i|we)\s+([a-z']+)\b")
APOLOGY_SELF = re.compile(r"\bsorry\s+(?:for|about)\s+(?:being\s+)?"
                          r"(?:such\s+)?(?:a\s+|an\s+)?"
                          r"(?:mess|burden|nightmare|nuisance|pain|disaster|state|rubbish"
                          r"|useless|awful|horrible|annoying|needy|too much|like this|this way"
                          r"|me|myself|the way i am)\b")
SORRY = re.compile(r"\b(?:sick|ill|unwell|off\s+work|not\s+(?:coming|in|be\s+in)|"
                   r"won'?t\s+be\s+(?:in|there)|can'?t\s+(?:come|make|be\s+(?:in|there))|"
                   r"cant\s+come|cannot\s+come|late|miss(?:ing)?|day\s+off|time\s+off|"
                   r"cancel(?:ling)?|postpone|reschedule|sorry)\b")

SUBJECT = re.compile(r"^(?:won'?t|can'?t|cannot|should\s+be|will\s+be|might\s+be|not\s+be|"
                     r"going\s+to|need|want|wonder|hope|must|would\s+like|would|didn'?t|"
                     r"don'?t|am|was|were|have|had|keep|late\b|stuck\b|away\b)\b")
COPULA = re.compile(r"^(?:off\b|sick\b|ill\b|unwell\b|back\s+(?:in|at|on|from)\b|"
                    r"still\s+(?:off|ill|unwell|sick)\b)")

CREATIVE = frozenset(("poem", "poems", "poetry", "haiku", "story", "stories", "song", "songs",
                      "rhyme", "rhymes", "joke", "jokes", "speech", "speeches", "limerick"))

AGREEMENT = frozenset((
    "ok", "okay", "okey", "k", "yes", "yeah", "yep", "yup", "aye", "sure", "please", "thanks",
    "thank", "you", "ta", "cheers", "go", "on", "then", "ahead", "that", "thats", "it", "is",
    "that's", "alright", "right", "cool", "great", "fine", "nice", "sound", "and", "so", "do",
    "thatll", "that'll", "let's", "lets", "have", "a", "shot", "give", "us", "for", "me", "my",
    "no", "nope", "nah", "not", "now", "later", "sounds", "good", "perfect", "lovely", "brilliant",
))

QUESTION = re.compile(r"^\s*(?:what|why|how|who|which|when|where|should|could|would|can|do|"
                      r"does|did|is|are|was|were|will|have|has|any)\b")

CAPITALS = frozenset((
    "monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday",
    "january", "february", "march", "april", "may", "june", "july", "august", "september",
    "october", "november", "december",
))

VENT = frozenset(("nightmare", "joke", "useless", "annoying", "awful", "horrible", "rubbish",
                  "unbearable", "impossible", "toxic", "miserable", "unfair", "frustrating",
                  "exhausting"))
VENT_PHRASES = ("a pain in the", "fed up", "had enough", "cant stand", "driving me mad",
                "driving me up the wall", "driving me crazy")

NEWS = frozenset(("died", "death", "dead", "funeral", "buried", "cremation", "cancer", "tumour",
                  "hospital", "hospice", "ward", "icu", "stolen", "burgled", "robbed",
                  "mugged", "struggling", "panicking", "hyperventilating", "breakdown",
                  "tumor", "diagnosed", "diagnosis", "miscarriage", "stillborn", "chemo",
                  "redundant", "sacked", "fired", "bankrupt", "evicted", "divorce", "divorced",
                  "breakup", "dumped", "debt", "debts", "arrears", "homeless", "bereaved",
                  "bereavement", "dying"))
NEWS_PHRASES = ("passed away", "lost my job", "lost his job", "lost her job", "lost the baby",
                "in debt", "behind on", "split up", "walked out", "left me", "laid off",
                "in hospital", "in the hospital", "my phone was", "got stolen", "was stolen",
                "panic attack", "anxiety attack", "im struggling", "really struggling",
                "not coping", "falling apart", "i feel awful", "feel terrible")
FEELING = frozenset(("tired", "exhausted", "knackered", "shattered", "drained", "stressed",
                     "overwhelmed", "anxious", "depressed", "upset", "unhappy", "miserable",
                     "angry", "furious", "worried", "scared", "awful", "terrible", "horrible",
                     "panicky", "terrified", "devastated", "heartbroken", "gutted", "low"))
FEELING_PHRASES = ("fed up", "had enough", "cant cope", "can't cope", "burnt out", "worn out")
MESSAGE_SHAPES = (
    re.compile(r"\bi (?:need|want|would like|have) to\b|\bi (?:need|want)\b|\bcan i\b|"
               r"\bcould i\b|\bplease\b|\basking (?:for|about)\b|\bi(?:'m| am|m) asking\b"),
    re.compile(r"\bi(?:'ll| will|ll) be\b|\bi(?:'m| am|m) (?:off|out|away|late|not coming|"
               r"stuck|leaving|moving|starting|finishing|going to|back)\b|"
               r"\bi (?:cant|cannot|can not|wont|will not)\b|\bi(?:'ve| have|ve) (?:decided|"
               r"quit|resigned|booked|cancelled)\b|"
               r"\bi dont (?:think i can|want to come)\b"),
)
THING_GONE_WRONG = re.compile(r"\b(?:my|the|our)\b[^.,!?]{0,28}\b(?:broke|broken|bust|busted|"
                              r"snapped|stopped working|wont start|packed in|died|got stolen|"
                              r"was stolen|flooded|leaking|blocked|failed|cancelled|fell through)\b")
NOT_A_CHANGE = re.compile(r"\bi (?:cant|cannot|can not|wont|will not|dont|do not)\s+"
                          r"(?:sleep|eat|stop|breathe|walk|see|hear|swallow|keep|remember|"
                          r"focus|concentrate|pee|cry|poo|sit|stand)\b")
WANT_FROM = re.compile(r"\bi (?:need|want|would like)\b[^.,!?]{0,30}\bfrom\b")
NO_MESSAGE = re.compile(r"\bi (?:dont|do not) know\b|\bno idea\b|\bnot sure (?:what|how)\b|"
                        r"\bi cant (?:think|find the words)\b|\bwhat should i say\b|"
                        r"\bhelp me (?:word|say)\b|\bi dont know what to say\b")
A_WISH_FOR_SOMEONE = re.compile(r"\b(?:want|wants|wanted|wish|wishing)\s+"
                                r"(?:her|him|them|it)\s+back\b")
HURT_WORD = (r"(?:kill|murder|hurt|punch|hit|smash|beat|stab|shoot|strangle|choke|throttle|"
             r"slap|kick|wring|batter|poison|drown)")
HURT_TARGET = (r"(?:me|you|him|her|them|us|myself|yourself|himself|herself|themselves|"
               r"my|his|her|their|our|someone|somebody|everyone|everybody)")
HURT_WISH = (r"\b(?:i|we|ill|i'll|im|i'm|id|i'd)\s+"
             r"(?:really\s+|just\s+|so\s+|seriously\s+)?(?:want|wanna|wanted|would\s+like|"
             r"would\s+love|need|have|am\s+going|going|will|ll|might|should|could|must|"
             r"love|like|planned?\s+to|wish(?:ed)?)\s+(?:to\s+)?")
HURTS_SOMEONE = re.compile(HURT_WISH + HURT_WORD + r"\s+(?:\w+\s+){0,3}" + HURT_TARGET + r"\b")
WANTS_THEM_DEAD = re.compile(r"\b(?:want|wants|wanted|wish|wishes|wished)\s+"
                             r"(?:\w+\s+){0,2}dead\b")


def _wants_to_hurt(low):
    return bool(HURTS_SOMEONE.search(low) or WANTS_THEM_DEAD.search(low))


def _is_a_message_shape(low):
    if NO_MESSAGE.search(low) or NOT_A_CHANGE.search(low) or WANT_FROM.search(low):
        return False
    if len(re.findall(r"[a-z']+", low)) < 2:
        return False
    if any(shape.search(low) for shape in MESSAGE_SHAPES):
        return True
    return bool(THING_GONE_WRONG.search(low) and says_it_is_the_message(low))


REPORTS_ON_SOMEONE = re.compile(r"^\s*(?:he|she|they)\b|\b(?:keeps?|kept)\s+(?:asking|saying|"
                               r"telling|ringing|texting|changing|forgetting|moaning)\b")
NOT_YET = (
    "That's the mood rather than the words - give me the one line you want the message to say "
    "and I'll write it.",
    "Nearly: tell me what the message should actually say, and I'll put it in order.",
    "Got the feeling. Now the words: what do you want them to read?",
)

LEAD_INS = (
    "Here's something you could send:",
    "Try this:",
    "Something like this works:",
    "Here's a short version:",
)


def names_a_draft(reply):
    return str(reply or "").lstrip().startswith(LEAD_INS)


def offers_a_draft(reply):
    return bool(OFFER.search(str(reply or "").lower()))


QUOTED = re.compile(r"[\"\u201c]([^\"\u201d]{15,})[\"\u201d]")


def hands_over_words(reply):
    for body in QUOTED.findall(str(reply or "")):
        if len(body.split()) >= 4:
            return True
    return False


MESSAGE_WORD = re.compile(r"\b(?:text|message|email|e-mail|note|letter)\b")
SHAPE_CUES = re.compile(r"\b(?:say|says|keep|short|specific|ask\s+for|ask\s+them|mention|put|"
                        r"include|subject|sign\s?-?off|signed|date[ds]?|address|tell\s+them|"
                        r"follow\s+it\s+up|first\s+sentence|first\s+line|opening|closing|"
                        r"paragraphs?|\d+\s*words|bullet\s+points?|three\s+or\s+four|"
                        r"few\s+lines|lines)\b")


def hands_over_the_shape(reply):
    low = str(reply or "").lower()
    cues = len(set(m.group(0) for m in SHAPE_CUES.finditer(low)))
    return cues >= 3 or (cues >= 2 and bool(MESSAGE_WORD.search(low)))


MESSAGE_NOUN = r"(?:text|message|msg|email|note|letter)"
WRITING_ASK = re.compile(
    r"\b(?:can|could|would|will)\s+(?:you\s+)?(?:please\s+)?(?:help\s+(?:me\s+)?)?"
    r"(?:write|word|draft|phrase|put\s+together)\b[^?]{0,40}?" + MESSAGE_NOUN + r"\s+(?:to|for)\b"
    r"|\bhelp\s+me\s+(?:write|word|draft|phrase)\b[^?]{0,40}?" + MESSAGE_NOUN + r"\s+(?:to|for)\b"
    r"|\b(?:write|draft|word)\s+me\s+(?:a|an|the)\s+(?:short\s+|quick\s+|nice\s+|polite\s+|firm\s+)?"
    + MESSAGE_NOUN + r"\s+(?:to|for)\b")

THE_CONTENT = re.compile(r"\b(?:saying|says|tell(?:ing)?|about|asking|ask|because|cos|since|"
                        r"explaining|to\s+say|to\s+ask|that)\b")


def reads_as_a_writing_ask(line):
    clean = " ".join(str(line or "").lower().split())
    if not clean:
        return False
    if CREATIVE & set(re.findall(r"[a-z']+", clean)):
        return False
    if re.match(r"^\s*(?:how|what|where|when|why)\b", clean):
        return False
    found = WRITING_ASK.search(clean)
    if not found:
        return False
    return THE_CONTENT.search(clean[found.end():]) is None


AFTER_ILL = frozenset(("be", "have", "see", "try", "call", "let", "need", "get", "go", "ring",
                       "text", "come", "bring", "pay", "ask", "tell", "do", "send", "sort"))


def _tidy(text):
    words = str(text or "").split()
    if len(words) > 1 and words[0].strip(".,!?;:").lower() == "ill" \
            and words[1].strip(".,!?;:").lower() in AFTER_ILL:
        text = "i'll " + " ".join(words[1:])
    out = []
    for word in text.split():
        bare = word.strip(".,!?;:")
        tail = word[len(bare):] if bare and word.startswith(bare) else ""
        if bare.lower() in CAPITALS:
            out.append(bare[0].upper() + bare[1:] + tail)
            continue
        fixed = TIDY.get(bare.lower())
        if fixed and bare.islower():
            out.append(fixed + tail)
        else:
            out.append(word)
    line = " ".join(out).strip(" .")
    if not line:
        return ""
    return line[0].upper() + line[1:]


def _small(text):
    if not text or not text[:1].isupper() or text.startswith(("I ", "I'", "I,")):
        return text
    if text.split()[0].strip(".,!?;:").lower() in CAPITALS:
        return text
    return text[0].lower() + text[1:]


WANTS_MORE_OF_IT = re.compile(
    r"^(?:and\s+|so\s+|ok\s+|okay\s+)?i\s+(?:just\s+)?(?:want|wants|need|needs|would\s+like|"
    r"wanna)\s+(?:to\s+)?(?:\w+\s+){0,4}?"
    r"(?:more|less|again|every\s+day|every\s+week|every\s+morning|more\s+often)\b")


def _content(text):
    line = " ".join(str(text or "").split())
    if not line or "?" in line:
        return None, None
    low = line.lower()
    if low in {"ok", "okay", "yes", "yeah", "no", "thanks", "thank you", "hi", "hello", "hey"}:
        return None, None
    if all(word.strip(".,!?;:'") in AGREEMENT for word in line.split()):
        return None, None
    if QUESTION.match(low):
        return None, None
    shape = "said"
    for pattern, kind in LEADS:
        found = pattern.match(low)
        if found:
            shape = kind
            line = line[found.end():].strip()
            break
    low = line.lower()
    if WANTS_MORE_OF_IT.match(low):
        return None, None
    words = line.split()
    if len(words) < 2 or len(words) > 30:
        return None, None
    if set(w.lower().strip(".,!?;:") for w in words) & CREATIVE:
        return None, None
    body = _tidy(line)
    if not body:
        return None, None
    return body, shape


def _formal(memory, words):
    if set(words) & FORMAL:
        return True
    for turn in (memory.get("turns") or [])[-4:]:
        text = str((turn or {}).get("user") or "").lower()
        if set(re.findall(r"[a-z']+", text)) & FORMAL:
            return True
    return False


def _said_before(memory, line):
    if not OFFER.search(str(last_bot(memory) or "").lower()):
        return None
    low = " ".join(str(line or "").lower().split())
    if not low or "?" in low:
        return None
    return low


A_SPAN = re.compile(
    r"\b(?:since|for)\s+(?:\d+\s+|a\s+|an\s+|two\s+|three\s+|four\s+|five\s+|six\s+|seven\s+|eight\s+|nine\s+|ten\s+)?"
    r"(?:day|days|week|weeks|fortnight|fortnights|month|months|year|years|january|february|march|april|may|"
    r"june|july|august|september|october|november|december)\b"
    r"|\b(?:has|had)\s+been\b|\bkeeps?\s+(?:coming|going|happening|flaring|leaking|breaking)\b")


REPORTED_SPEECH = re.compile(r"\b(?:says?|said|telling|told|reckons?|thinks?|asked|wants?\s+me\s+to)\b")


def _a_fault_they_were_asked_for(low):
    if not A_SPAN.search(low):
        return False
    if THIRD_PERSON.search(low) or REPORTED_SPEECH.search(low):
        return False
    words = set(re.findall(r"[a-z']+", low))
    if words & (NEWS | FEELING):
        return False
    return not any(phrase in low for phrase in NEWS_PHRASES + FEELING_PHRASES)


def is_theirs(memory, line):
    low = _said_before(memory, line)
    if low is None:
        return False
    if A_WISH_FOR_SOMEONE.search(low):
        return True
    if _wants_to_hurt(low):
        return True
    lead = _names_the_message(low)
    if lead is not None:
        if lead is BARE_LEAD and not _is_a_message_shape(low):
            return True
        rest = low[lead.match(low).end():]
        if set(re.findall(r"[a-z']+", rest)) & (NEWS | FEELING):
            return True
        if any(phrase in rest for phrase in NEWS_PHRASES + FEELING_PHRASES):
            return True
        return False
    if APOLOGY.match(low) and not THIRD_PERSON.search(low):
        return False
    if ABSENT.search(low):
        return False
    if low.startswith(("i feel", "im ", "i'm ", "i am ", "ive been ", "i've been ")) \
            and (set(re.findall(r"[a-z']+", low)) & FEELING
                 or any(phrase in low for phrase in FEELING_PHRASES)):
        return True
    if set(re.findall(r"[a-z']+", low)) & VENT:
        return False
    if any(phrase in low for phrase in VENT_PHRASES) or REPORTS_ON_SOMEONE.search(low):
        return False
    if not (_is_a_message_shape(low) or _a_fault_they_were_asked_for(low)):
        return True
    if set(re.findall(r"[a-z']+", low)) & (NEWS | FEELING):
        return True
    if any(phrase in low for phrase in NEWS_PHRASES + FEELING_PHRASES):
        return True
    return bool(reads_as_pregnancy_bleeding(low) or reads_as_sudden_loss(low)
                or reads_as_bad_news(low) or reads_like_a_symptom(low)
                or names_a_feeling(low))


BARE_LEAD = LEADS[-1][0]


def _names_the_message(low):
    for pattern, _kind in LEADS:
        if pattern.match(low):
            return pattern
    return None


def says_it_is_the_message(line):
    lead = _names_the_message(" ".join(str(line or "").lower().split()))
    return bool(lead) and lead is not BARE_LEAD


def not_the_message(memory, line):
    low = _said_before(memory, line)
    if low is None or is_theirs(memory, line):
        return False
    if set(re.findall(r"[a-z']+", low)) & VENT:
        return True
    if any(phrase in low for phrase in VENT_PHRASES):
        return True
    return bool(REPORTS_ON_SOMEONE.search(low))


TELL_FRAME = re.compile(r"^(?:and\s+|so\s+|ok\s+|okay\s+)?i\s+(?:just\s+)?(?:need|want|have)\s+"
                        r"to\s+tell\s+(?:them|him|her)\s+(?:that\s+)?")


def drafter(memory, line, words=None):
    if not OFFER.search(str(last_bot(memory) or "").lower()):
        return None
    if is_theirs(memory, line) or not_the_message(memory, line):
        return None
    frame = TELL_FRAME.match(" ".join(str(line or "").lower().split()))
    if frame:
        rest = " ".join(str(line or "").lower().split())[frame.end():].strip(" ,.")
        if not rest or THIRD_PERSON.search(rest):
            return None
        line = rest
    body, shape = _content(line)
    if not body:
        return None
    if shape == "told":
        return None
    if shape == "asked":
        body = "I wanted to ask about " + _small(body)
    if body.endswith(("?", "!", ".")):
        body = body[:-1]
    body = _small(body)
    if COPULA.match(body.lower()):
        body = "I'm " + body[0].lower() + body[1:]
    elif SUBJECT.match(body.lower()):
        body = "I " + body[0].lower() + body[1:]
    apology = APOLOGY.match(body.lower()) is not None
    if apology:
        if APOLOGY_ACT.search(body.lower()) is None or APOLOGY_SELF.search(body.lower()):
            return None
        body = body + ". I shouldn't have done that"
    elif SORRY.search(body.lower()):
        small = body[0].lower() + body[1:]
        keeps_cap = re.match(r"i(?:'|\b)", body, re.I) is not None
        body = "sorry for the short notice - " + (body if keeps_cap else small)
    friendly = not _formal(memory, set(words or re.findall(r"[a-z']+", str(line).lower())))
    hello = "Hey" if friendly else "Hi"
    sign = "Cheers" if friendly else "Thanks"
    if apology or len(re.findall(r"[a-z']+", body.lower())) <= 4:
        return f"{hello}, {body}."
    return f"{hello}, {body}. {sign}."


SUBJECT_EXAMPLES = (
    (re.compile(r"\b(?:plumber|electrician|boiler|leak|radiator|roofer|builder|joiner|"
                r"damp|drain|washing machine|fridge|oven|heating|handyman)\b", re.I),
     "Leak under the kitchen sink - when can you come?"),
    (re.compile(r"\b(?:teacher|school|headteacher|head|nursery|childminder|tutor|"
                r"college|university|lecturer|professor|year \d+|form|class)\b", re.I),
     "Year 6 trip - a question about the form"),
    (re.compile(r"\b(?:gp|doctor|surgery|dentist|hospital|clinic|prescription|appointment|"
                r"nurse|consultant)\b", re.I),
     "Repeat prescription - could you check this for me"),
    (re.compile(r"\b(?:landlord|landlady|letting|lettings|agent|housing|council|tenant)\b", re.I),
     "Boiler still not working - flat 3"),
    (re.compile(r"\b(?:boss|manager|employer|hr|work|workplace|office|team|colleague|"
                r"shift|rota)\b", re.I),
     "A quick question about Thursday"),
    (re.compile(r"\b(?:invoice|payment|paid|pay|bill|overdue|refund|quote|estimate|"
                r"customer|client|supplier)\b", re.I),
     "Invoice 2144 - payment due"),
)


def example_subject(understood):
    line = ""
    if isinstance(understood, dict):
        line = str(understood.get("clean") or understood.get("text") or "")
    else:
        line = str(understood or "")
    for pattern, example in SUBJECT_EXAMPLES:
        if pattern.search(line):
            return example
    return "Invoice 2144 - payment due"
