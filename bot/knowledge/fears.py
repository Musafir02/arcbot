
import re

from .lookup import entry

ANSWERS = ("health",)

FEAR = ("fear of", "fear off", "phobia", "phobias", "phobic of", "phobic about",
        "scared of", "scared about", "scared stiff", "afraid of", "terrified of",
        "terrified by", "frightened of", "dread", "dreads", "dreading", "petrified of",
        "hate flying", "hate spiders", "cant stand spiders", "panic when i", "panics when",
        "panic attack when", "panic attacks when", "get the fear",
        "get over", "getting over", "got over", "overcome", "overcoming", "cure my",
        "stop being scared", "stop being afraid", "not be scared", "less scared",
        "irrational fear", "irrational", "how do i stop being")

ASK = ("how do i", "how can i", "how to", "what can i do", "what should i do", "help",
       "get over", "getting over", "overcome", "overcoming", "cure", "stop", "deal with",
       "cope", "manage", "fix", "advice", "tips", "any tips", "any advice",
       "whats the best way", "what is the best way", "is there a way", "can i",
       "am i", "why am i", "what is wrong with me",
       "im scared of", "i am scared of", "im afraid of", "i am afraid of",
       "im terrified of", "i am terrified of", "im frightened of", "i am frightened of",
       "im petrified of", "i am petrified of", "im phobic of", "i am phobic of",
       "im phobic about", "i am phobic about")

_MARKERS = ("fear of", "fear off", "phobia of", "phobia about", "phobic of", "phobic about",
            "scared of", "scared about", "afraid of", "terrified of", "terrified by",
            "frightened of", "petrified of", "phobia")
_STOP = frozenset((
    "i", "im", "i'm", "ive", "i've", "id", "and", "but", "so", "because", "cos", "when",
    "since", "what", "whats", "how", "can", "could", "should", "do", "does", "did", "help",
    "any", "is", "are", "was", "were", "it", "its", "my", "we", "he", "she", "they", "them",
    "that", "this", "never", "always", "really", "very", "too", "now", "please", "thanks",
    "thank", "need", "have", "has", "to", "will", "would", "am", "for", "if", "of", "get",
    "getting", "over", "overcome", "stop", "deal", "cope", "even", "just", "also", "about",
    "on", "at", "in", "with", "from", "there", "here", "as", "than", "then", "make", "makes"))

_TRAILING_FILLER = frozenset((
    "tbh", "tbf", "lol", "lols", "haha", "hah", "tho", "though", "rn", "atm", "idk",
    "nvm", "omg", "honestly", "actually", "basically", "kinda", "sorta", "mate", "pal",
    "thanks", "thank", "thx", "please", "xx", "x", "hey", "now", "still", "again"))


_LINKS = frozenset(("to", "on", "in", "at", "into", "about", "with", "of", "near", "around",
                    "from", "inside"))
_DETERMINERS = frozenset(("the", "a", "an", "my", "our", "your", "his", "her", "their",
                          "this", "that", "its"))


def _the_thing_they_fear(understood):
    said = " ".join(str((understood or {}).get("clean") or "").lower().split())
    found = ""
    at = -1
    for marker in _MARKERS:
        pos = said.find(" " + marker + " ")
        if pos < 0:
            if said.startswith(marker + " "):
                pos = -1
            else:
                continue
        if at < 0 or pos < at or (pos == at and len(marker) > len(found)):
            at = pos
            found = marker
    if not found:
        return ""
    rest = said[at + len(found) + 1:].strip()
    words = []
    doing = False
    for word in rest.split():
        word = word.strip(",.!?;:\"'")
        if not word:
            break
        if len(words) >= (5 if doing else 3):
            break
        if word in _STOP:
            if doing and (word in _LINKS or word in _DETERMINERS):
                words.append(word)
                continue
            break
        words.append(word)
        if len(words) == 1 and word.endswith("ing") and len(word) > 4:
            doing = True
    if not words:
        return ""
    while words and words[-1] in _TRAILING_FILLER:
        words.pop()
    if not words:
        return ""
    while len(words) > 1 and words[-1] in ("to", "on", "in", "at", "into", "about", "with",
                                          "of", "near", "around", "from", "inside"):
        words.pop()
    thing = " ".join(words)
    if thing in ("the", "a", "an", "my", "it", "them", "that", "this"):
        return ""
    return thing


def _the_fear_reply(memory, understood):
    thing = _the_thing_they_fear(understood)
    opening = ("A fear of %s is learned, so it can be unlearned" % thing if thing
               else "A fear like that is learned, so it can be unlearned")
    return (opening + " in small steps: write a ladder from the easiest version of it to the "
            "hardest - a photo of it, then the smallest real version, then all of it - and "
            "only move up when the step you are on has stopped raising your heart. "
            "Pick the easiest rung and stay with it until the wave passes: leaving early is what "
            "teaches the fear that it was right. If it is limiting your life, ask the GP for CBT "
            "with exposure, which is the treatment with the best evidence.")


_PHOBIA_GERUNDS = frozenset((
    "flying", "driving", "vomiting", "being sick", "travelling", "traveling", "sailing",
    "cruising", "going out", "speaking", "presenting", "dating", "eating", "sleeping",
    "swallowing", "choking", "blushing", "sweating"))
_AN_ING_NOUN = frozenset((
    "wedding", "weddings", "building", "buildings", "ceiling", "ceilings", "string", "strings",
    "ring", "rings", "thing", "things", "evening", "evenings", "morning", "mornings",
    "pudding", "puddings", "filling", "icing", "sibling", "siblings", "offspring", "darling",
    "earring", "earrings", "duckling", "lightning", "clothing", "savings", "innings",
    "weddings", "meeting", "meetings"))


def _names_the_thing(understood):
    thing = _the_thing_they_fear(understood)
    if not thing:
        return False
    first = thing.split()[0]
    if (first.endswith("ing") and len(first) > 4 and first not in _AN_ING_NOUN
            and first not in _PHOBIA_GERUNDS):
        return False
    return True


ENTRIES = [
    entry("fear-of-something", (FEAR, ASK), _the_fear_reply, guard=_names_the_thing,
          avoid=("my son", "my daughter", "my child", "my kid", "my toddler", "my baby",
                 "my grandson", "my granddaughter", "4 year old", "5 year old", "3 year old",
                 "2 year old", "6 year old", "toddler", "puppy", "kitten",
                 "my dog", "my cat", "my rabbit", "my horse", "the dog", "the cat",
                 "dog", "dogs", "a dog", "puppies",
                 "public speaking", "presentation", "presentations", "presenting", "speech",
                 "speech in front", "talk in front", "talking in front", "speaking in front",
                 "stage fright", "interview", "interviews", "wedding speech", "best man speech",
                 "speaking up", "speak up", "spoke up", "talking in meetings",
                 "meetings", "meeting", "standup", "stand-up", "stand up", "in the room",
                 "say something in", "board meeting", "team meeting",
                 "dentist", "dental", "hygienist", "doctor", "gp", "hospital appointment",
                 "blood test", "blood tests", "injection", "vaccine", "jab", "anaesthetic",
                 "surgery", "operation", "childbirth", "birth", "labour", "pregnancy",
                 "scan", "mri", "x ray", "xray", "chemo", "needle phobia is stopping me",
                 "lose", "lost my", "my job", "redundancy",
                 "redundant", "being made redundant", "sacked", "fired", "unemployed",
                 "monday", "mondays", "monday morning",
                 "monday mornings", "work tomorrow", "going to work",
                 "commitment", "intimacy", "intimate", "relationship", "relationships",
                 "my marriage", "my partner", "my girlfriend", "my boyfriend",
                 "missing out", "fomo", "being alone", "loneliness", "being judged",
                 "rejection", "being rejected", "abandonment",
                 "mice", "mouse", "rat", "rats", "rodent", "rodents", "kitchen",
                 "mortgage", "mortgages",
                 "arrears", "bailiff", "bailiffs", "debt", "debts", "council tax", "summons",
                 "eviction", "evicted", "landlord", "court", "credit card", "overdraft",
                 "swim", "swims", "swimming", "swimmer", "pool", "pools", "water", "sea",
                 "face in the water", "lessons", "lesson", "instructor",
                 "film", "films", "movie", "movies", "horror", "watch", "watching", "tv",
                 "series", "documentary",
                 "why am i scared of dying", "death", "dying", "panic attack now",
                 "heart is racing", "cant breathe", "chest pain", "suicidal", "kill myself",
                 "abusive", "hit me", "hits me", "threatened", "stalker", "following me"),
          report=True,
          bias=3),
]
