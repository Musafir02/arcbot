import re

COLOUR = re.compile(r"\b(?:red|reddish|pink|pinkish|blotchy|blotches|flushed)\b")

BLUSH = re.compile(
    r"\b(?:blush\w*|"
    r"(?:face|cheeks?|neck|ears?)\b[^.!?]{0,24}?"
    r"\b(?:goes?|going|went|gone|turns?|turning|turned|gets?|getting|come up|came up)"
    r"\s+(?:(?:bright|very|all|so|quite|a bit|really|dead|properly)\s+)?red\b|"
    r"\b(?:red|redder|redden\w*)\b[^.!?]{0,30}?when(?:ever)? i (?:talk|speak|meet) to?\s?people)\b")

BODY_PARTS = frozenset((
    "head", "face", "neck", "cheek", "cheeks", "forehead", "scalp", "ear", "ears", "nose",
    "chin", "jaw", "lip", "lips", "eyelid", "eyelids", "shoulder", "shoulders", "arm", "arms",
    "elbow", "elbows", "forearm", "forearms", "wrist", "wrists", "hand", "hands", "finger",
    "fingers", "thumb", "chest", "breast", "breasts", "back", "spine", "tummy", "belly", "waist",
    "hip", "hips", "thigh", "thighs", "knee", "knees", "shin", "shins", "calf", "calves",
    "ankle", "ankles", "foot", "feet", "toe", "toes", "heel", "heels", "skin", "torso",
    "underarm", "armpit", "armpits", "bum", "bottom", "crotch", "groin", "navel", "collarbone",
    "knuckle", "knuckles", "bottom",
))

ALSO_A_SYMPTOM = frozenset((
    "itch", "itchy", "itches", "itching", "sting", "stings", "stinging", "burning", "tingling",
    "throbbing", "weeping", "crusty", "flaky", "scaly", "peeling", "swollen", "swelling",
    "warm", "hot", "feverish", "fever", "temperature", "shivery", "shivering", "spreading",
    "spread", "painful", "hurts", "hurting", "sore",
    "pain", "tender", "bleeding", "bled", "blood", "ooze", "oozing", "pus",
    "puffy", "puffiness", "puffed", "raw", "shaved", "shaving", "razor",
    "numb", "numbness", "white", "blue", "tingly", "pins",
    "streak", "streaks", "track", "tracks",
))
A_BURN = frozenset((
    "singed", "singe", "singeing", "boiling", "boiled", "scald", "scalds", "scalded", "steam",
    "steamed", "bleach", "bleached", "chemical", "acid", "oven", "hob", "iron", "ironed",
    "kettle", "frying", "oil", "bonfire", "barbecue", "bbq", "fire", "flare", "sparkler",
))

INSIDE = frozenset((
    "throat", "tonsil", "tonsils", "gum", "gums", "mouth", "tongue", "palate", "sinus",
    "stomach", "gullet", "uvula", "eye", "eyes", "eyeball", "eyesight", "vision",
))

SOMEWHERE_ELSE = frozenset((
    "wine", "sock", "socks", "whites", "shirt", "shirts", "sheet", "sheets", "towel", "towels",
    "carpet", "rug", "stain", "stains", "wash", "washing", "laundry", "dye", "dyed", "paint",
    "painted", "ink", "pen", "marker", "fabric", "curtain", "curtains", "bedding", "sofa",
    "tablecloth", "wall", "walls", "urine", "pee", "dress", "jumper", "blouse", "shoe", "shoes",
    "bag", "phone", "screen", "light", "lights", "sky", "sunset", "car", "door", "window",
    "leaves", "tree", "flower", "flowers", "candle", "flag", "light", "traffic",
))

SOMEONE_ELSE = frozenset((
    "he", "she", "him", "her", "his", "hers", "they", "them", "their", "mum", "dad", "son",
    "daughter", "child", "kid", "kids", "baby", "babies", "toddler", "boy", "girl", "husband",
    "wife", "partner", "nan", "gran", "friend", "mate", "dog", "cat", "puppy", "kitten", "pet",
    "mother", "mom", "father", "sister", "brother", "aunt", "uncle", "niece", "nephew", "cousin",
    "grandma", "grandad", "granny", "stepson", "stepdaughter", "flatmate", "housemate",
    "colleague", "childminder", "babysitter", "siblings", "sibling", "pup", "rabbit", "hamster",
))
PETS = frozenset(("dog", "cat", "puppy", "kitten", "pet", "rabbit", "hamster", "pup", "parrot",
                  "budgie", "guinea", "horse", "pony"))

NOT_A_PATCH = frozenset((
    "mole", "moles", "bite", "bites", "bitten", "burn", "burns", "burnt", "scald", "scalded",
    "sunburn", "sunburnt", "wound", "wounds", "cut", "cuts", "graze", "grazed", "scar", "scars",
    "bruise", "bruises", "bruised", "lump", "lumps", "spot", "spots", "pimple", "pimples",
    "hives", "tattoo", "tattoos", "blister", "blisters", "cyst", "abscess", "sore", "sores",
    "ulcer", "ulcers", "stitches", "dressing", "bandage", "cast", "plaster", "cream", "ointment",
))

PATCH_POOL = (
    "A patch that comes up like that is usually contact or heat - a new soap or washing powder, "
    "a plant, sweat in a warm room - and it fades in a few days without much doing. Keep perfumed "
    "things off it, don't scrub at it, and let a pharmacist look if it spreads or starts to hurt. "
    "If there is a fever with it, or the patch stays red under a glass pressed on it, get seen "
    "today. How long has it been there, and does it itch?",
    "Redness like that is usually contact or heat and it settles on its own in a few days. Plain "
    "water rather than soap, leave it uncovered, and show a pharmacist if it is no better by the "
    "weekend or it is spreading. A fever with it, or red that does not blanch under a glass, is a "
    "same-day call rather than a wait. When did you first notice it?",
    "That sounds like contact or heat: a soap, a plant, a fabric, sweat under a coat. Cool water "
    "and no cream until you know what it is, and a pharmacist if it is still there in a few days "
    "or it starts to hurt. With a fever, or if it stays red where you press a glass on it, get "
    "seen the same day. Is it in one place or spreading?",
    "Patches like that are usually contact or heat and they calm down in a few days. Wash it with "
    "plain water, keep anything perfumed off it, and have a pharmacist look if it spreads or gets "
    "sore. If you also feel feverish or shivery, or the colour stays put under a glass, that is a "
    "today job. Where is it, and has it changed since you first saw it?",
)
BLUSH_POOL = (
    "That is a blush rather than anything wrong: the vessels in the face open up for a moment and "
    "there is nothing to treat. It eases as you get used to the people in the room, and finding "
    "one friendly face to talk to helps more than trying to fight it. What sort of moment sets it "
    "off?",
    "Going red like that is a blush - your own body's alarm, and it fades in a minute or two. Most "
    "people read it as being interested rather than embarrassed. Is it situations with people you "
    "don't know, or does it happen with friends too?",
    "A blush is the face's own thermostat rather than a sign of anything wrong, and everybody has "
    "one. It helps to let it happen instead of fighting it - fighting it is what keeps it going. "
    "Does it bother you more at work or with people you know?",
)

WORD = re.compile(r"[a-z']+")


def _words(text):
    return WORD.findall(text.lower().replace("’", "'"))


def _last_reply(memory):
    turns = (memory or {}).get("turns") or []
    for turn in reversed(turns):
        if isinstance(turn, dict) and turn.get("bot"):
            return " ".join(str(turn["bot"]).split())
    return ""


def _pick(pool, line, memory=None):
    if not pool:
        return ""
    start = sum(ord(letter) for letter in line.lower()) % len(pool)
    last = _last_reply(memory)
    for step in range(len(pool)):
        said = pool[(start + step) % len(pool)]
        if not last or " ".join(said.split()) not in last:
            return said
    return pool[start]


def _someone_elses(words):
    for word in words:
        if word in SOMEONE_ELSE or word in PETS:
            return True
        for suffix in ("'s", "'"):
            if word.endswith(suffix) and word[: -len(suffix)] in SOMEONE_ELSE | PETS:
                return True
        if word.endswith("s") and word[:-1] in SOMEONE_ELSE | PETS:
            return True
    return False


def _thread_names_a_pet(memory):
    turns = (memory or {}).get("turns") or []
    seen = 0
    for turn in reversed(turns):
        if not isinstance(turn, dict):
            continue
        said = (turn.get("user") or "").strip().lower()
        if not said:
            continue
        seen += 1
        if seen > 4:
            break
        if set(_words(said)) & PETS:
            return True
    return False


def reply_for(text, memory=None):
    clean = " ".join((text or "").lower().replace("’", "'").split())
    if not clean:
        return None
    words = set(_words(clean))

    if BLUSH.search(clean):
        if clean.startswith("why") and not (words & {"i", "my", "me", "im", "myself"}):
            return None
        if words & SOMEWHERE_ELSE or words & INSIDE:
            return None
        if _someone_elses(words):
            return None
        return _pick(BLUSH_POOL, clean, memory)

    if COLOUR.search(clean) is None:
        return None
    if not (words & BODY_PARTS):
        return None
    if words & INSIDE:
        return None
    if words & SOMEWHERE_ELSE:
        return None
    if _someone_elses(words):
        return None
    if words & ALSO_A_SYMPTOM or words & NOT_A_PATCH or words & A_BURN:
        return None
    if _thread_names_a_pet(memory):
        return None
    return _pick(PATCH_POOL, clean, memory)
