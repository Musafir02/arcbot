import re

from . import pets
from .lookup import (ASK_ABOUT, FOOD_SUBJECT, TOOTH_OR_GUM, TOOTH_OUT, entry,
                     not_keeping_an_eye_on_it, not_the_flat_you_live_in, said)
from .body import _the_nail_is_a_persons, _the_part_is_a_persons
from .shopping import not_a_present

ANSWERS = ("health",)

PETS = ("cat", "cats", "dog", "dogs", "puppy", "kitten", "vet", "hamster", "rabbit", "parrot",
        "horse", "animal", "guinea", "budgie")

NOT_A_BABY = ("boiler", "oven", "fridge", "freezer", "car", "engine", "dishwasher", "dryer",
              "heating", "radiator", "thermostat", "laptop", "computer")

_A_MACHINE = re.compile(
    r"\b(?:boiler|boilers|combi|central heating|heating|radiator|radiators|"
    r"washing machine|washer|tumble dryer|dishwasher|fridge|freezer|oven|cooker|kettle|"
    r"laptop|computer|phone|printer|machine|appliance)\b", re.I)
_A_FAULT = re.compile(
    r"\b(?:broke|broken|break|breaks|breakdown|packed in|stopped working|not working|faulty|"
    r"dead|leak|leaking|pressure|gauge|reset|error|fault)\b", re.I)


def not_a_machine_that_broke(understood):
    said = understood if isinstance(understood, dict) else {}
    bits = [str(said.get(key) or "")
            for key in ("clean", "text", "raw", "rewritten", "plain")]
    words = said.get("words") or ()
    text = " ".join(bits + [str(word) for word in words])
    return not (_A_MACHINE.search(text) and _A_FAULT.search(text))


_A_WHEN_ASK = re.compile(
    r"\b(?:when|how often|how regularly)\b|\bhow long (?:until|before|between)\b", re.I)


def not_a_when_ask(understood):
    said = understood if isinstance(understood, dict) else {}
    bits = [str(said.get(key) or "") for key in ("clean", "text", "raw", "words")]
    words = said.get("words") or ()
    text = " ".join(bits + ([" ".join(str(w) for w in words)] if words else []))
    return not _A_WHEN_ASK.search(text)


def not_a_season_or_a_machine(understood):
    return not_the_flat_you_live_in(understood) and not_a_machine_that_broke(understood)

HEADACHE_NO_DRUGS = (
    "A pint of water, a cold flannel over the eyes and twenty minutes in a dark quiet room take "
    "most ordinary headaches down, and if you drink coffee daily a small cup early on stops the "
    "caffeine-withdrawal one. Loosen the neck and shoulders: chin down and hold for five seconds, "
    "then each ear to its shoulder, and a hot shower on the back of the neck helps a tension "
    "headache. Peppermint oil on the temples is the old stand-in.")

PLAIN_DO_ASK = ("what should i do", "what can i do", "what do i do", "what shall i do",
                "what could i do", "anything i can do", "anything you can do", "any tips",
                "any advice", "what would you do", "what helps", "anything about",
                "do about", "a remedy for", "anything for a")

def _the_line(understood):
    words = understood.get("words") if isinstance(understood, dict) else None
    if isinstance(words, (list, tuple)) and words:
        return " ".join(str(word) for word in words).lower()
    return str((understood or {}).get("clean") or "").lower()

_A_CHILDS_AGE = re.compile(
    r"\b(?:my|our|the|his|her|their)\s+(?:[a-z]+\s+)?"
    r"(?:baby|babies|child|children|kid|kids|son|daughter|boy|girl|toddler|toddlers|newborn|"
    r"infant|little\s+(?:one|lad|girl|boy|man|fella|fellow)|wee\s+(?:one|man|lad))\s+"
    r"(?:is|are|is now|just turned|turns?)\s+(?:[a-z]+\s+){0,2}?"
    r"(?:\d|\bone\b|\btwo\b|\bthree\b|\bfour\b|\bfive\b|\bsix\b|\bseven\b|\beight\b|"
    r"\bnine\b|\bten\b|\beleven\b|\btwelve\b)", re.IGNORECASE)


def not_a_childs_age(understood):
    return not _A_CHILDS_AGE.search(_the_line(understood))


_ON_THE_CARD = re.compile(
    r"\b(?:covid|coronavirus|flu|influenza|colds?|stomach bugs?|sickness bugs?|gastro\w*|"
    r"norovirus|diarrhoea|diarrhea|vomit\w*|chickenpox|chicken pox|bug|bugs|virus|viral|"
    r"infection|infections|temperature|fever|cough|coughs|sore throat|sore throats)\b")

_AN_ILLNESS = re.compile(
    r"\b(?:tonsillitis|impetigo|hand,? foot and mouth|hand,? foot,? mouth|scarlet fever|measles|"
    r"mumps|rubella|whooping cough|pertussis|strep|conjunctivitis|pink eye|mono|glandular fever|"
    r"shingles|hepatitis|meningitis|tuberculosis|thrush|ringworm|scabies|head lice|nits|"
    r"threadworms|pinworms|verruca|warts?|cold sores?|bronchitis|pneumonia|ear infections?|"
    r"sinusitis|uti|urinary tract infection|cystitis|stye|styes|athlete'?s foot|roseola|"
    r"slapped cheek|parvovirus|laryngitis|pharyngitis|quinsy|abscess|cellulitis|mrsa|lupus|"
    r"croup|bronchiolitis|hand foot mouth)\b")


def _an_illness_the_card_covers(understood):
    text = _the_line(understood)
    if _ON_THE_CARD.search(text):
        return True
    return not _AN_ILLNESS.search(text)


REMEDY_CUES = ("get rid", "get rid of", "clear up", "cure", "treat", "treating", "go away",
               "shift it", "get shot", "stop", "take", "taking")


HEADACHE_PLAIN = (
    "For an ordinary headache, water, a dark quiet room and paracetamol or ibuprofen usually do "
    "more than anything else. If you get them most days, keep a short diary of sleep, food and "
    "screens for two weeks and take it to a pharmacist or GP.")

_PREGNANT_AT_ALL = re.compile(
    r"\b(?:pregnan\w*|expecting a baby|expecting my baby|with child|trimester|"
    r"\d\d? weeks (?:pregnant|gone))\b")
_PREGNANT_DENIED = re.compile(
    r"\b(?:not|isn't|isnt|aren't|arent|no longer|never)\s+(?:pregnan\w*)")

HEADACHE_PREGNANT = (
    "Paracetamol is the one to take for a headache in pregnancy, at the lowest dose that works "
    "and for the shortest time - not ibuprofen or aspirin unless a doctor or midwife has told "
    "you to. Water, food and sleep do a lot, and a skipped meal, dehydration and caffeine "
    "withdrawal are the usual causes. Mention headaches that keep coming back to your midwife, "
    "and go in the same day if a bad headache comes with blurred vision or flashing lights, pain "
    "under the ribs, swelling of the face or hands, or vomiting after 20 weeks: that combination "
    "is the one that has to be checked for pre-eclampsia.")

NO_DRUGS = ("without tablets", "without any tablets", "without pills", "without any pills",
            "without painkillers", "without medicine", "without any medicine",
            "without medication", "without any medication", "without drugs", "without meds",
            "without paracetamol", "without ibuprofen", "without taking anything",
            "without popping", "no tablets", "no pills", "no painkillers", "no medicine",
            "no medication", "no drugs", "no meds", "not taking tablets", "not on tablets",
            "not on medication", "off the tablets", "off the pills",
            "cant take tablets", "can't take tablets", "cannot take tablets",
            "can not take tablets", "cant take pills", "can't take pills", "cannot take pills",
            "cant take painkillers", "can't take painkillers", "can not take painkillers",
            "cant take ibuprofen", "can't take ibuprofen", "can not take ibuprofen",
            "cant take medicine", "can't take medicine", "cant take medication",
            "can't take medication", "cannot take medication", "not allowed ibuprofen",
            "not allowed to take", "hate taking tablets", "hate taking pills",
            "naturally", "instead of tablets", "instead of painkillers",
            "dont want to take", "don't want to take", "dont want pills", "don't want pills",
            "rather not take")


TABLETS_SAFE = (
    ("paracetamol or ibuprofen", "paracetamol"),
    ("paracetamol and ibuprofen", "paracetamol"),
    ("ibuprofen or paracetamol", "paracetamol"),
    ("paracetamol or nurofen", "paracetamol"),
    ("nurofen or paracetamol", "paracetamol"),
)
PREGNANT_TABLETS_NOTE = (
    " Not ibuprofen or aspirin while you are pregnant unless a doctor or midwife has told you to.")


def tablets_for_a_pregnancy(reply, understood):
    if not isinstance(reply, str):
        return reply
    reading = understood if isinstance(understood, dict) else {}
    text = " ".join(str(reading.get("clean") or reading.get("text") or "").lower().split())
    if not _PREGNANT_AT_ALL.search(text) or _PREGNANT_DENIED.search(text):
        return reply
    said = reply
    swapped = False
    for pair in TABLETS_SAFE:
        if pair[0] in said:
            said = said.replace(pair[0], pair[1])
            swapped = True
    for word in ("ibuprofen", "nurofen"):
        if word in said.lower():
            swapped = True
            break
    if swapped:
        said = said + PREGNANT_TABLETS_NOTE
    return said


_TOOTHACHE_PLAIN = (
    "Take paracetamol or ibuprofen, rinse with warm salty water and keep eating on the other "
    "side, but book a dentist: a toothache that wakes you or comes with a swollen face needs "
    "seeing the same day. Clove oil on the tooth numbs it for a while and is the home remedy "
    "worth having - a drop or two on the tooth itself, not swallowed - and do not put aspirin "
    "on the gum, it burns it. Do not use the oil on broken skin, in a child's mouth or on a "
    "gum that is already sore and bleeding.")


def _toothache_help(memory, understood):
    return tablets_for_a_pregnancy(_TOOTHACHE_PLAIN, understood)


def headache_help(memory, understood):
    text = ((understood or {}).get("clean") or "").lower()
    if any(phrase in text for phrase in NO_DRUGS):
        return HEADACHE_NO_DRUGS
    if _PREGNANT_AT_ALL.search(text) and not _PREGNANT_DENIED.search(text):
        return HEADACHE_PREGNANT
    return HEADACHE_PLAIN


_AN_EYE_ON_AN_ANIMAL = re.compile(
    r"\b(?:dog|dogs|puppy|puppies|cat|cats|kitten|kittens|rabbit|rabbits|bunny|bunnies|"
    r"guinea|hamster|hamsters|gerbil|gerbils|rat|rats|mouse|mice|ferret|ferrets|horse|horses|"
    r"pony|ponies|parrot|parrots|budgie|budgies|tortoise|tortoises|chinchilla|chinchillas|"
    r"lizard|lizards|snake|snakes|pet|pets)\b", re.I)
_A_PERSONS_OWN_EYE = re.compile(r"\b(?:my eyes?|me in the eye|my eye is|in my eye)\b", re.I)
_AN_ANIMALS_OWN_EYE = re.compile(r"\b(?:his|her|its|their)\s+eyes?\b", re.I)


def _a_persons_eye(understood):
    said = str((understood or {}).get("clean") or "")
    if _A_PERSONS_OWN_EYE.search(said):
        return True
    if not _AN_EYE_ON_AN_ANIMAL.search(said):
        return True
    return not _AN_ANIMALS_OWN_EYE.search(said)


def _the_eye_is_said(understood):
    said = " ".join(str((understood or {}).get(key) or "")
                    for key in ("clean", "text", "norm_text")).lower()
    return any(word in said for word in ("eye", "eyes", "eyelid", "eyelids", "lash", "lashes"))


def _the_pregnancy_verdict(understood):
    words = set((understood or {}).get("words") or ())
    if not words & {"ibuprofen", "aspirin", "nurofen", "voltarol", "naproxen",
                    "anti-inflammatory", "anti-inflammatories"}:
        return ""
    return ("Avoid ibuprofen and aspirin unless a doctor or midwife has told you otherwise")


def _medicine_when_pregnant_or_feeding(memory, reading):
    words = set(reading.get("words") or ())
    feeding = bool(words & {"breastfeeding", "breast", "feeding", "nursing", "chestfeeding"})
    pregnant = bool(words & {"pregnant", "pregnancy", "expecting", "trimester", "weeks"})
    if feeding and not pregnant:
        return None
    return ("Paracetamol is the painkiller to reach for in pregnancy, at the lowest dose for the "
            "shortest time. Avoid ibuprofen and aspirin unless a doctor or midwife has told you "
            "otherwise, and ask a pharmacist before anything else - many cold and cough remedies "
            "have something in them you would not expect. While breastfeeding, paracetamol and "
            "ibuprofen are both fine at the normal dose; go easy on codeine, which can make a "
            "baby drowsy.")
_GLASS_EYE_URGENT = ("red", "swollen", "swelling", "hot", "discharge", "discharging", "pus",
                     "oozing", "leaking", "smelly", "inflamed", "infection", "infected",
                     "stopped fitting", "doesnt fit", "does not fit", "wont fit",
                     "will not fit", "not fitting")
_GLASS_EYE_CLEAN = (
    "Take it out and clean it: wash the prosthesis in warm water with a little mild soap, rinse it "
    "well in saline, and clean the socket with saline on a clean pad, then leave both to air "
    "before putting it back. Soreness is usually dryness or a crust that has built up, so a "
    "lubricating drop made for prosthesis wearers helps; leave it out overnight if your service "
    "says to. Never put the bathroom or contact-lens solutions in it.")
_GLASS_EYE_CLINIC = (
    "Ring the prosthetics service or an eye clinic today rather than cleaning it again: a socket "
    "that is red, swollen, hot or leaking discharge is an infection or a fit that has changed, and "
    "neither is something a clean and a night out fixes. While you wait, take the eye out and "
    "rinse it and the socket with saline on a clean pad, keep it out while it is uncomfortable, "
    "and never put the bathroom or contact-lens solutions in it. A socket that is badly swollen, "
    "or one with spreading redness or a fever, is 111.")


_PROSTHESIS_CLEAN = (
    "Wash the socket and the liner every day: mild soap and warm water, rinse both well, and dry "
    "them completely before you put them back on - a damp liner is what grows the smell and the "
    "sore patches. Turn the liner inside out to wash it if your service says it can be, and leave "
    "the leg off at night if that is what your fitter told you. No alcohol, no hot wash and no "
    "bathroom cleaners: they harden the liner and the fit goes with it. A liner that has gone "
    "tacky, stiff or baggy is worn out rather than dirty, and the limb-fitting service replaces "
    "it.")
_PROSTHESIS_SORE = (
    "Soreness under a prosthesis is usually the liner or the fit rather than the limb: take it "
    "off, wash and dry the liner and the socket, and look at the skin - a red patch that has not "
    "faded half an hour after it comes off is the one to show someone. If it rubs where it did "
    "not before, ring the limb-fitting service; padding it yourself usually makes the fit worse. "
    "A red, hot, swollen or weeping stump is the same week, not the next appointment.")
_PROSTHESIS_GIVES_WAY = (
    "A leg that gives way, locks or buckles is an alignment or suspension problem rather than "
    "wear: book the limb-fitting service and tell them exactly when it happens - going down "
    "stairs, turning, or at the end of the day when the limb has shrunk - because that is what "
    "tells them which it is. Use the stick or the crutches you were given until it is looked at, "
    "and get it checked the same day if you have fallen on it, or the knee will not straighten "
    "and the skin is broken.")
_PROSTHESIS_CLEANING = re.compile(r"\bclean|\bcleaning|\bwash|\bwashing|\bhygiene|\bsmell|"
                                  r"\bsmelly|\bsweaty|\blook after|\bcare for|\bcare of"
                                  r"|\bshower|\bshowering|\bbathe|\bbathing|\bbath\b"
                                  r"|\bswim|\bswimming|\bwet")
_PROSTHESIS_HURTS = re.compile(r"\bsore|\bhurt|\bpain|\bache|\brub|\bblister|\bchaf|"
                               r"\bred\b|\bswollen|\bweeping|\bnumb|\btingl"
                               r"|\bsqueak|\bcreak|\brattl|\bnoisy|\bclicking")


_PROSTHESIS_GIVING_WAY = re.compile(r"giving way|gives way|gave way|given way|\bbuckl"
                                    r"|\bcollaps|\blocks\b|\blocking\b|\blocks up"
                                    r"|\bfolds under"
                                    r"|\bfolded under|\bwobbl|\bknee goes\b|\bknee went\b")


def _prosthesis_care(memory, reading):
    said = " ".join(str(reading.get(key) or "") for key in ("text", "norm_text", "clean"))
    if _PROSTHESIS_GIVING_WAY.search(said):
        return _PROSTHESIS_GIVES_WAY
    if _PROSTHESIS_HURTS.search(said):
        return _PROSTHESIS_SORE
    if _PROSTHESIS_CLEANING.search(said):
        return _PROSTHESIS_CLEAN
    return _PROSTHESIS_SORE


def _glass_eye_out(memory, reading):
    said = " ".join(str(reading.get(key) or "") for key in ("text", "norm_text", "clean"))
    said = " " + said.lower() + " "
    if any(word in said for word in _GLASS_EYE_URGENT):
        return _GLASS_EYE_CLINIC + " " + _GLASS_EYE_CLEAN
    return _GLASS_EYE_CLEAN


_POO_COLOUR_BLACK = "Black, tarry poo is blood from higher up the gut, and it needs a GP or 999 "
_POO_COLOUR_PALE = "Pale, clay-coloured poo usually means bile is not getting through, so it is "
_POO_COLOUR_RED = "Bright red blood on the paper is usually piles"


def _poo_colour(memory, understood):
    text = ((understood or {}).get("norm_text") or (understood or {}).get("clean") or "").lower()
    if re.search(r"\b(black|tarry|tar\s*-?\s*like|very dark|dark red)\b", text):
        return ("Black, tarry poo is blood from higher up the gut, and it is the same day: ring 111 "
                "or go to A&E if you are dizzy, pale, breathless or it keeps coming, and ring the "
                "GP today if you feel well in yourself. Do not take iron or bismuth for it before "
                "you are seen, because they blacken the stool too and hide the cause.")
    if re.search(r"\b(pale|clay|whitish|white|greasy|yellowish)\b", text):
        return ("Pale, putty-coloured poo usually means bile is not reaching the gut, so it is a GP "
                "question rather than a food one - especially with dark wee, yellow eyes or skin, "
                "an ache under the right ribs or itching, which is the same day. Otherwise make a "
                "routine appointment and mention any new medicine, because some cause it.")
    if re.search(r"\b(faint\w*|dizzy|light[- ]?headed|breathless|short of breath|vomit\w*|"
                 r"sick|throwing up|passing out|passed out|collapsed|collapsing|shaking|"
                 r"clots?|pouring|loads of blood|a lot of blood|so much blood|badly|"
                 r"really bad|severe|unbearable)\b", text):
        return ("Blood in your poo with feeling faint, dizzy, sick or in a lot of pain is not a wait "
                "and see: ring 111 now, or 999 or go to A&E if you are faint, breathless, "
                "vomiting, or the bleeding is heavy or has clots. Steady bright red on the paper "
                "alone is usually piles, but the faintness or the pain is what decides this one, "
                "so get it looked at today rather than working out the cause yourself.")
    return ("Bright red blood on the paper or in the pan is usually piles or a small tear, and it "
            "settles in a few days with plenty of water, fibre and no straining. See the GP if it "
            "is more than a streak, keeps coming for more than a few weeks, or comes with weight "
            "loss, a change in your poo for weeks, pain or a fever: that is not piles, and black "
            "or tarry poo is 111 or A&E the same day.")
def _eye_reply(memory, reading):
    clean = (reading.get("clean") or "").lower()
    words_here = set(re.findall(r"[a-z]+", clean))
    if (any(word in clean for word in ("itchy", "itch", "itches", "itching", "watery", "streaming"))
            and not any(word in clean for word in ("sticky", "crusty", "gunge", "gritty", "pus",
                                                   "discharge", "glued", "infection"))
            and not words_here & {"stye", "sty", "styes", "eyelid", "eyelids", "lash", "lashes",
                                  "lid"}):
        return ("An itchy eye is an allergy until proved otherwise - pollen, dust mites or a cat - "
                "and the itch is the tell, because an infection is sticky or gritty rather than "
                "itchy. Don't rub it, which makes it worse; use a cool compress and antihistamine "
                "or lubricating drops from a pharmacist, keep the windows shut in pollen season "
                "and shower before bed. An eye that is painful, that light hurts, whose sight has "
                "changed, or that is red with a contact lens in, is the same-day GP or optician.")
    if words_here & {"stye", "sty", "styes", "eyelid", "eyelids", "lash", "lashes", "lid"}:
        return ("A stye is a blocked lash follicle: a warm compress for ten minutes, four times "
                "a day, brings it to a head in a few days, and never squeeze it. Leave lenses "
                "and eye make-up off until it has gone. A stye that is getting bigger, or an "
                "eyelid swelling shut, is a same-day GP; pain in the eye itself, light hurting "
                "or blurred vision is A&E.")
    return ("A sticky, gritty red eye with crusty lashes in the morning is usually conjunctivitis: "
            "bathe it with cooled boiled water and a fresh cotton wool ball for each eye, and stop "
            "wearing lenses until it is better. A stye is a blocked lash follicle - a warm compress "
            "for 10 minutes several times a day brings it to a head; never squeeze it. Pain, light "
            "sensitivity or blurred vision is a same-day GP or optician visit.")


STOMACH_HARD = (
    "Take it with or straight after food, or with a glass of milk: ibuprofen, aspirin, naproxen "
    "and steroids are the ones that burn an empty stomach, and a meal is what protects it. "
    "Paracetamol does not need food, and most antibiotics are fine either way unless the label "
    "says otherwise. Taken every day for more than a week or two, or if a tablet still upsets "
    "you, ask a pharmacist rather than stopping it yourself - they can add a stomach protector "
    "or switch you to a coated or gel version.")
STOMACH_PARACETAMOL = (
    "Paracetamol does not need food: an empty stomach is fine, and a meal neither helps nor "
    "hurts it. Keep to 4g a day - eight 500mg tablets - spread through the day, and check the "
    "cold and flu remedies in the cupboard, because most of them contain paracetamol already. "
    "Every day for weeks on end, or with a liver problem or a lot of alcohol, is worth a word "
    "with a GP rather than carrying on.")
STOMACH_ANTIBIOTIC = (
    "Most antibiotics are fine on an empty stomach, and only the label knows the exceptions: "
    "doxycycline and metronidazole want a full glass of water and half an hour upright, metronidazole "
    "means no alcohol, and others are gentler with a meal - so follow the packet where it "
    "disagrees with the leaflet, finish the course, and ask a pharmacist if a tablet comes back "
    "up or gives you the runs. Paracetamol and ibuprofen can be taken alongside them unless the "
    "label says otherwise.")


def _medicine_with_food(memory, reading):
    text = ((reading or {}).get("clean") or "").lower()
    if "antibiotic" in text:
        return STOMACH_ANTIBIOTIC
    harsh = ("ibuprofen", "nurofen", "aspirin", "naproxen", "diclofenac", "steroid",
             "co-codamol", "painkiller")
    if "paracetamol" in text and not any(word in text for word in harsh):
        return STOMACH_PARACETAMOL
    return STOMACH_HARD


SHAKE_HANDS = ("hands", "hand", "fingers", "finger", "arms", "arm", "thumb", "wrists", "wrist")
SHAKE_ALL_OVER = (
    "Most shaking like this is caffeine, a missed meal, anxiety or a fever, and it eases when "
    "that does: cut the coffee to one or two cups, eat every few hours and sleep. Shaking that "
    "crept on over months, is worse on one side, or comes with a slow walk or stiff arm needs a "
    "GP, and so does a tremor with a fast heartbeat or weight loss, because the thyroid gets "
    "checked for that.")
SHAKE_HANDS_TEXT = (
    "Most shaky hands are caffeine, a missed meal, anxiety or a fever, and they ease when that "
    "does: cut the coffee to one or two cups, eat every few hours and sleep. Shaking that crept "
    "on over months, is worse on one side, or comes with a slow walk or stiff arm needs a GP, "
    "and so does a tremor with a fast heartbeat or weight loss, because the thyroid gets "
    "checked for that.")


def shaky_hands_help(memory, understood):
    text = ((understood or {}).get("clean") or "").lower()
    words = set(re.findall(r"[a-z']+", text))
    return SHAKE_HANDS_TEXT if words & set(SHAKE_HANDS) else SHAKE_ALL_OVER
BP_FIGURES = re.compile(r"(\d{2,3})\s*(?:over|/|on)\s*(\d{2,3})")

BP_HIGH = ("A reading of 140/90 or higher, seen twice at home, is high and worth a GP check: they "
           "will confirm it and talk through treatment. Meanwhile cut salt, keep to 14 units of "
           "alcohol a week, and 150 minutes of walking a week lowers it by a few points. 180/120 "
           "or higher with a bad headache, chest pain or blurred vision is 999.")

BP_NORMAL = (
    "That is a normal reading: at home, normal is anything under 135 over 85, so there is nothing "
    "to fix. Check it now and then at the same time of day rather than every hour, and keep off "
    "the salt and keep walking if it has been high before.")


def bp_help(memory, understood):
    clean = ((understood or {}).get("clean") or "").lower()
    found = BP_FIGURES.search(clean)
    if not found:
        if any(word in clean for word in ("normal", "fine", "perfect", "healthy")):
            return BP_NORMAL
        return BP_HIGH
    top, bottom = int(found.group(1)), int(found.group(2))
    figures = f"{top} over {bottom}"
    if top < 90 or bottom < 60 or (top <= 95 and bottom <= 65):
        return (f"{figures} is a low reading, not a high one. If you feel well the usual causes "
                "are dehydration, a hot day and skipping meals: drink a glass of water, eat "
                "something and stand up slowly. See a GP if you faint or feel dizzy on standing, "
                "or if it keeps reading low.")
    if top >= 140 or bottom >= 90:
        return BP_HIGH
    if top >= 135 or bottom >= 85:
        return (f"{figures} is a little above the home range, which stops at 135 over 85: it is "
                "not high enough to act on from one reading. Sit still five minutes before you "
                "take it, do it twice a day for a week at the same times and write the numbers "
                "down - if the week averages over 135 over 85, take the list to the GP.")
    return (f"{figures} is a normal reading: at home, normal is anything under 135 over 85. Check "
            "it now and then at the same time of day rather than every hour, and keep off the salt "
            "if it has been high before.")


EYE_WHAT = (
    "something", "something got in", "grit", "dust", "sand", "eyelash", "lash", "speck",
    "mascara", "shampoo", "soap", "sunscreen", "sun cream", "foreign body", "bit of dirt",
    "dirt", "scratch", "scratched", "scratches", "poked", "poke", "poking",
    "metal", "piece of metal", "bit of metal", "filing", "filings", "swarf", "spark", "sparks",
    "welding spark", "welding sparks", "rust", "ash", "chilli", "chili", "sawdust",
    "wood", "woodchip", "wood chip", "plaster", "plasterboard",
    "piece of glass", "bit of glass", "shard of glass", "shards of glass", "glass in",
    "broken glass", "splinter of glass",
)
WATER_IN_EYE = (
    "water in my eye", "water in my eyes", "water in the eye", "water in the eyes",
    "water getting in my eye", "water gets in my eye", "water keeps getting in",
    "water keep getting in", "water got in my eye", "water went in my eye",
    "get water in my eye", "got water in my eye", "getting water in my eye",
    "soap in my eye", "soap in my eyes", "got soap in my eye", "shampoo in my eye",
    "shampoo in my eyes", "got shampoo in my eye", "shower in my eye",
    "rinse my eye", "rinse my eyes", "rinse the eye", "rinse out my eye",
    "rinse it out of my eye", "how do i rinse my eye", "flush my eye", "flush the eye",
    "flush my eyes", "wash my eye out", "wash out my eye", "wash my eyes out",
    "get the water out of my eye", "get the water out of my eyes", "water out of my eye",
    "water out of my eyes", "get water out of my eye", "get water out of my eyes",
    "get it out of my eye", "something in my eye is water",
)
EYE_RINSE_ASK = (
    "how", "what", "why", "should", "do", "can", "help", "keep", "keeps", "kept", "getting",
    "gets", "got", "rinse", "flush", "wash", "out", "shower", "sting", "stings", "stinging",
    "sore", "hurts", "hurt", "safe", "harm", "harmful", "bad", "ok", "okay", "normal",
    "worry", "worried", "shouldnt", "shouldn't", "again", "still",
)

EYE_WHERE = (
    "in my eye", "in the eye", "in my eyes", "in the eyes", "in both eyes", "in one eye",
    "on my eyeball", "on the eyeball", "in my eyeball", "my eye", "my eyes", "the eye",
    "eyeball", "eyelid", "lid", "eyelashes",
    "his eye", "his eyes", "her eye", "her eyes", "their eye", "their eyes", "your eye",
    "your eyes", "in his eye", "in her eye", "in their eye", "in his eyes", "in her eyes",
    "in their eyes", "in your eye", "in your eyes", "his eyeball", "her eyeball",
)

MELATONIN_CHILD = ("child", "children", "kid", "kids", "son", "daughter", "toddler",
                   "baby", "boy", "girl", "teen", "teenager", "months old",
                   "my lad", "my lass")
MELATONIN_CHILD_TEXT = (
    "Not without a doctor: in the UK melatonin is a prescription for children, not something you "
    "buy, and it is not licensed for the under-twos. For a child who will not settle, the routine "
    "does more than any tablet - the same bedtime every night, a dark room, no screens in the last "
    "hour, and a short goodnight - so give that two or three weeks first. If nights are still bad, "
    "ask your GP or health visitor about a sleep plan before medicine.")
MELATONIN_TEXT = (
    "Melatonin is a short-term sleep aid rather than a knock-out: 1 to 2 mg about an hour before "
    "bed shifts your body clock, so it suits jet lag or a bedtime that has drifted late, and it "
    "works best with a dark room and the same wake-up time. Ask a pharmacist first if you take "
    "blood thinners, epilepsy drugs or antidepressants. If sleep has been poor for weeks, see your "
    "GP - it is not a long-term fix.")
MELATONIN_PREGNANT_TEXT = (
    "Not without asking your midwife or doctor: melatonin is not recommended in pregnancy or while "
    "breastfeeding, because nobody has shown it is safe for the baby. The sleep routine still "
    "helps - a dark cool room, the same bedtime, no screens last thing, and no caffeine after "
    "lunch - and if your sleep is still broken, that is worth raising at your next appointment.")

MELATONIN_PREGNANT = ("pregnant", "pregnancy", "expecting", "breastfeeding",
                      "breast feeding", "nursing", "trimester", "midwife")
GIVE_TO_SOMEONE = ("give him", "give her", "give them", "give it to", "gave him", "gave her",
                   "gonna give", "going to give", "give my son", "give my daughter")
GIVE_TO_A_GROWN_UP = ("wife", "husband", "partner", "mum", "mother", "dad", "father",
                      "friend", "myself", "me", "hubby")
AGE_OF_A_CHILD = re.compile(r"\b(\d{1,2})\s*(?:year|yr)s?\s*old\b")


TABLET_TEXT = (
    "A tablet that has not helped in the time it should is worth checking before you take more: "
    "read the dose and how often it says on the box, and do not add a second thing with the same "
    "ingredient (paracetamol is hidden in a lot of cold remedies). A pharmacist will go through "
    "everything you take together, for free, and say what is safe to add. If it is a prescribed "
    "medicine that is not working, tell the doctor who prescribed it rather than stopping it or "
    "doubling it yourself."
)
TABLET_AS_MEDICINE = frozenset("""took take takes taking taken swallow swallowed doctor gp
    pharmacist pharmacy prescription prescribed prescribe pain painful ache aching painkiller
    painkillers dose dosage daily night morning medicine medication repeat repeats""".split())
TABLET_DEVICE = frozenset("""ipad samsung android apple laptop screen charging charger battery
    wifi app apps stylus keyboard storage slow frozen""".split())


NAMED_MEDICINES = frozenset("""ibuprofen nurofen brufen paracetamol paracetemol panadol
    naproxen diclofenac codeine cocodamol co-codamol codamol solpadeine anadin aspirin
    tramadol""".split())
NOT_HELPED = (
    "not touching", "isnt touching", "doesnt touch", "didnt touch", "not working",
    "isnt working", "arent working", "stopped working", "stopped helping",
    "not helping", "isnt helping", "arent helping", "didnt help", "didnt work",
    "doesnt work", "doesnt help", "hasnt helped", "hasnt worked", "no better",
    "not better", "does nothing",
    "doesnt do anything", "not doing anything", "no good", "wearing off",
    "doesnt help at all", "isnt doing anything",
)


SIDE_EFFECT_TEXT = (
    "Feeling sick, drowsy or off your food on a new medicine is usually worst in the first week "
    "and settles: take it with food or at night if the box allows, and ask a pharmacist about a "
    "different brand or a slow-release version, which often stops it without changing the "
    "medicine. Do not stop a prescribed one on your own - ring the surgery or the pharmacist and "
    "say which tablet, which effect and when it started. If you are vomiting within two hours of "
    "a contraceptive pill, treat it as a missed one and use condoms for seven days."
)
SIDE_EFFECT_KEYS = (("tablet", "tablets", "pill", "pills", "capsule", "capsules", "medicine",
                     "medication", "prescription", "antibiotic", "antibiotics", "statins"),
                    ("makes me feel sick", "make me feel sick", "makes me sick",
                     "make me sick", "feel sick", "feeling sick", "felt sick", "nauseous",
                     "nausea", "makes me tired", "make me tired", "knocks me out", "drowsy",
                     "sleepy", "cant sleep", "bad stomach", "upset stomach", "stomach ache",
                     "headaches", "dizzy", "rash", "side effect", "side effects",
                     "gives me", "constipated", "diarrhoea", "diarrhea", "sweats"))


def _tablet_side_effects(memory, understood):
    text = ((understood or {}).get("clean") or "").lower()
    words = set(re.findall(r"[a-z']+", text))
    if words & TABLET_DEVICE:
        return None
    return SIDE_EFFECT_TEXT


_HELP_WORDS = tuple(tuple(phrase.split()) for phrase in NOT_HELPED)


def _a_medicine_that_has_not_helped(toks):
    marks = [i for i, word in enumerate(toks) if word in NAMED_MEDICINES]
    if not marks:
        return False
    for phrase in _HELP_WORDS:
        span = len(phrase)
        for start in range(len(toks) - span + 1):
            if tuple(toks[start:start + span]) != phrase:
                continue
            if any(abs(mark - start) <= 5 for mark in marks):
                return True
    return False


def _the_named_medicine_has_not_helped(understood):
    if not isinstance(understood, dict):
        return True
    said = understood.get("clean") or understood.get("text") or ""
    toks = re.findall(r"[a-z']+", str(said).lower())
    if not any(tok in NAMED_MEDICINES for tok in toks):
        return True
    return _a_medicine_that_has_not_helped(toks)


def _tablet_not_helping(memory, understood):
    text = ((understood or {}).get("clean") or "").lower()
    words = set(re.findall(r"[a-z']+", text))
    if words & TABLET_DEVICE:
        return None
    if words & NAMED_MEDICINES:
        return TABLET_TEXT if _a_medicine_that_has_not_helped(
            re.findall(r"[a-z']+", text)) else None
    plural = bool(words & {"tablets", "pills", "painkillers", "capsules"} or "on tablets" in text
                  or "my tablets" in text or "the tablets" in text)
    if "a day" in text or "per day" in text or "daily" in text:
        plural = True
    if not plural and not (words & TABLET_AS_MEDICINE):
        return None
    return TABLET_TEXT


def _melatonin(memory, understood):
    text = ((understood or {}).get("clean") or "").lower()
    words = set(re.findall(r"[a-z']+", text))
    if words & set(MELATONIN_PREGNANT):
        return MELATONIN_PREGNANT_TEXT
    age = AGE_OF_A_CHILD.search(text)
    if (age and int(age.group(1)) < 18) or "months old" in text:
        return MELATONIN_CHILD_TEXT
    grown_up = bool(words & set(GIVE_TO_A_GROWN_UP))
    if not grown_up and (words & set(MELATONIN_CHILD)
                         or any(phrase in text for phrase in GIVE_TO_SOMEONE)):
        return MELATONIN_CHILD_TEXT
    return MELATONIN_TEXT


NORMAL_TEMPERATURE = (
    "A normal body temperature is 36.1 to 37.2C (97 to 99F) in the mouth, up to half a degree "
    "higher in the evening. From 38C (100.4F) it is a fever, and 37.5 to 38 is a raised "
    "reading to watch rather than treat. A stiff neck, a rash that does not fade under a "
    "glass, or trouble breathing with a fever is a same-day call, and so is 38C in a baby "
    "under three months.")

COLD_WARMTH_WORDS = frozenset("cold freezing frozen chilled".split())
HOT_WARMTH_WORDS = frozenset("""hot boiling roasting sweltering sweaty sweating shivery
    shivering feverish""".split())

FEVER_ADVICE = (
    "Rest, drink plenty and take paracetamol or ibuprofen to bring it down; there's no need to "
    "strip off or sponge with cold water. Get advice the same day for 38C in a baby under three "
    "months, or a fever with a stiff neck, a rash that does not fade under a glass, "
    "breathlessness, confusion or not drinking.")

FEVER_FROM = 38.0


LOW_FROM = 36.0
COLD_BELOW = 35.0
RAISED_FROM = 37.5


def _in_celsius(number):
    value = number.get("value") if isinstance(number, dict) else None
    if not isinstance(value, (int, float)) or isinstance(value, bool):
        return None
    unit = str(number.get("unit") or "").lower()
    if unit in ("fahrenheit", "f", "degrees f", "deg f") or value >= 45:
        return (value - 32.0) * 5.0 / 9.0
    return value


def _a_reading(value):
    rounded = round(value, 1)
    if rounded == int(rounded):
        return "%dC" % int(rounded)
    return "%.1fC" % rounded


def _the_number_says(value):
    said = _a_reading(value)
    if value >= FEVER_FROM:
        if abs(value - FEVER_FROM) < 0.05:
            return ("%s is a fever: 100.4F is the point where one starts. %s"
                    % (said, FEVER_ADVICE))
        return ("%s is a fever: 38C (100.4F) is where one starts. %s" % (said, FEVER_ADVICE))
    if value < COLD_BELOW:
        return ("%s is below 35C (95F), which is hypothermia territory rather than a fever: get "
                "them out of the cold and out of wet clothes, wrap them in blankets and warm them "
                "slowly with a warm drink if they can swallow. Shivering that stops, slurred "
                "speech, confusion or drowsiness at that reading is a 999 call." % said)
    if value < LOW_FROM:
        return ("%s is a low reading rather than a fever: normal is 36.1 to 37.2C, and a cold "
                "room or a thermometer that slipped reads low more often than an illness does. "
                "Take it again after ten minutes somewhere warm with the arm tucked in, and if it "
                "stays under 36C with shivering, confusion or drowsiness, ask a doctor the same "
                "day." % said)
    if value >= RAISED_FROM:
        return ("%s is a raised reading rather than a fever: normal is 36.1 to 37.2C and 38C "
                "(100.4F) is where a fever starts. A drink, an ordinary room and another reading "
                "in an hour, and a stiff neck, a rash that does not fade under a glass or "
                "trouble breathing is a same-day call." % said)
    return ("%s is within the normal range of 36.1 to 37.2C, which runs half a degree higher in "
            "the evening, and a fever starts at 38C (100.4F), so there is nothing to treat. A "
            "stiff neck, a rash that does not fade under a glass, or trouble breathing with a "
            "fever is a same-day call." % said)


TEMPERATURE_NOUN = re.compile(r"\b(temperature|temp|degrees|fever|fahrenheit|celsius|centigrade)\b")
NOT_A_BODY = ("battery", "phone", "cpu", "gpu", "pressure", "tyre", "tire", "psi", "mph",
              "speed", "price", "cost", "salary", "score", "percent", "litre", "liter", "ml",
              "kg", "gram", "ounces", "mpg", "download", "wifi", "signal", "humidity", "rent",
              "income", "interest", "tax", "storage", "memory", "temperature of the",
              "bath", "bathwater", "hot tub", "jacuzzi", "pool", "swimming", "sauna", "shower",
              "steam room")
BODY_RANGE = (34.0, 42.5)


def _a_body_temperature_number(understood):
    reading = understood or {}
    said = str(reading.get("clean") or reading.get("text") or "").lower()
    if TEMPERATURE_NOUN.search(said):
        return True
    if any(word in said for word in NOT_A_BODY):
        return False
    for number in reading.get("numbers") or []:
        value = _in_celsius(number)
        if value is not None and BODY_RANGE[0] <= value <= BODY_RANGE[1]:
            return True
    return False


_LOW_QUESTION = re.compile(r"\b(too low|a low|low temperature|temperature too low|"
                            r"hypothermia|chilly|very cold|under ?36|below ?36)\b")
LOW_READING = (
    "Normal is 36.1 to 37.2C, so a reading under 36C is low, and a cold room or a thermometer "
    "that slipped is the usual reason: take it again after ten minutes somewhere warm with the "
    "arm tucked in. Below 35C (95F) with shivering that stops, slurred speech, confusion or "
    "drowsiness is hypothermia, and that is a 999 call.")


def temperature_card(memory, reading):
    try:
        given = reading.get("numbers") or []
    except Exception:
        return NORMAL_TEMPERATURE
    for number in given:
        value = _in_celsius(number)
        if value is not None:
            return _the_number_says(value)
    said = str((reading or {}).get("clean") or (reading or {}).get("text") or "").lower()
    if _LOW_QUESTION.search(said):
        return LOW_READING
    return NORMAL_TEMPERATURE

_COLD_SORE_EYE = re.compile(r"\b(eye|eyes|eyelid|optic|sight|vision)\b")
_COLD_SORE_PREGNANT = re.compile(r"\b(pregnan\w*|expecting|midwife|trimester)\b")
_COLD_SORE_BABY = re.compile(r"\b(newborn|new born|new-born|infant|neonate|neonatal|"
                             r"weeks old|four weeks|4 weeks|baby|baby's)\b")
_COLD_SORE_POP = re.compile(r"\b(pop|pops|popping|pick|picking|squeeze|squeezing|burst|scratch|"
                            r"scab|scabby)\b")
_COLD_SORE_SPREAD = re.compile(r"\b(contagious|catch|caught|kiss|kissing|share|sharing|towel|"
                               r"towels|cup|cups|lip balm|swim|swimming|pool|sex|partner|"
                               r"spread|spreading|work|school|gym)\b")
_COLD_SORE_CAUSE = re.compile(r"\b(cause|causes|caused|why|trigger|triggers|keep getting|"
                              r"keeps coming back|come back|comes back|recurring|again|always|"
                              r"every (?:few )?(?:month|months|winter|summer|spring|autumn))\b")
_COLD_SORE_CREAM = re.compile(r"\b(cream|creams|aciclovir|acyclovir|zovirax|ointment|patch|"
                              r"remedy|remedies|treatment|treat)\b")
_COLD_SORE_HELP = re.compile(r"\b(help|helps|helped|anything|what can i (?:do|take|use|put on)|"
                             r"what should i do|what do i do|best thing|sort it)\b")
_COLD_SORE_EARLY = re.compile(r"\b(tingl\w*|itch\w*|start\w*|first day|just noticed|"
                              r"coming on|feel one)\b")


def _cold_sore(memory, reading):
    clean = ((reading or {}).get("clean") or (reading or {}).get("text") or "").lower()
    if _COLD_SORE_EYE.search(clean):
        return ("Keep it off your eye: the virus spreads on your fingers, so wash your hands after "
                "touching the sore and don't rub your eyes. A cold sore that reaches the eye is "
                "seen by a GP or an optician the same day - it can damage the surface of the eye, "
                "and aciclovir eye ointment is a prescription rather than the cream.")
    if _COLD_SORE_PREGNANT.search(clean):
        return ("A cold sore in pregnancy is common and not dangerous in itself, but mention it to "
                "your midwife, and keep it away from a newborn: a cold sore on a baby under four "
                "weeks is a same-day call to a doctor. Aciclovir cream is safe to use in pregnancy "
                "from a pharmacist, and it works best started at the first tingle.")
    if _COLD_SORE_BABY.search(clean):
        return ("Ring 111 or your surgery today: a cold sore on a baby under four weeks is seen the "
                "same day, because the virus is serious in a newborn. Until then, wash your hands "
                "before you pick the baby up, don't kiss the baby while a sore is weeping, and keep "
                "the sore itself away from the baby's face. Ring 999 if the baby is floppy, feeding "
                "badly, or has a temperature.")
    if _COLD_SORE_POP.search(clean):
        return ("Don't pop, squeeze or pick it: the fluid spreads the virus to the rest of your lip "
                "and can leave a scar or an infection. Start aciclovir cream from a pharmacist now, "
                "keep it covered with a dab of cream rather than a plaster, wash your hands after "
                "touching it, and it should clear in 7 to 10 days.")
    if _COLD_SORE_HELP.search(clean) or _COLD_SORE_CREAM.search(clean):
        return ("Aciclovir cream from a pharmacist is the one that works: dab it on at the first "
                "tingle, five times a day for 4 to 5 days, and wash your hands after. It is the "
                "same medicine as Zovirax at a fraction of the price, and a numbing gel helps the "
                "soreness without changing how long it lasts. Keep it off your eye, and see a GP "
                "if it has not crusted over in 10 days.")
    if _COLD_SORE_SPREAD.search(clean):
        return ("A cold sore is contagious from the first tingle until the scab has healed over, so "
                "no kissing, and don't share cups, towels or lip balm while it is there. Swimming "
                "is fine, and so is work or school; wash your hands after touching it, keep it away "
                "from a newborn, and start aciclovir cream at the first tingle to shorten it.")
    if _COLD_SORE_CAUSE.search(clean):
        return ("Cold sores come from the herpes simplex virus, which most people catch as a child "
                "and which then sits dormant and flares up when you are run down - sun, cold wind, "
                "stress, illness, tiredness or a period. There is no cure, but aciclovir cream from "
                "a pharmacist at the first tingle shortens each one, and 7 to 10 days is the usual "
                "run.")
    if _COLD_SORE_EARLY.search(clean):
        return ("Start aciclovir cream from a pharmacist now, at the first tingle: begun that early "
                "it can shorten the sore or stop it coming out at all. Don't kiss anyone or share "
                "towels until it has crusted over, and it clears in about 7 to 10 days.")
    return ("A cold sore clears in about 7 to 10 days. Aciclovir cream from a pharmacist works best "
            "if you start it at the first tingle, and don't kiss anyone or share towels while it is "
            "weeping. See a GP if it is near your eye, if you are pregnant, or if a first outbreak "
            "comes with a fever.")


DRINK = ("drink", "drinking", "drinks", "alcohol", "beer", "beers", "wine", "wines", "lager",
         "pint", "pints", "vodka", "gin", "whisky", "whiskey", "rum", "cider", "prosecco",
         "cocktail", "cocktails", "booze", "boozy", "drunk", "night out", "few drinks",
         "glass of wine", "bottle of wine", "on the lash")

DRINK_PILLS = {
    "ibuprofen": ("Ibuprofen and alcohol both irritate the stomach lining, so one or two drinks "
                  "with food is the sensible ceiling, and none at all if you have an ulcer or "
                  "take a blood thinner. Paracetamol is the gentler painkiller for a big night. "
                  "A single glass of wine with dinner is not the problem."),
    "paracetamol": ("Paracetamol is fine with an ordinary drink - a glass of wine or a pint is not "
                    "the problem. The liver danger is heavy drinking, or a dose taken while "
                    "hungover when the last one is still in you, so never more than 4g in 24 "
                    "hours and keep the drink light if you drink daily. Ibuprofen with alcohol is "
                    "the one that upsets the stomach."),
    "antibiotics": ("Most antibiotics are fine with alcohol. Metronidazole and tinidazole are the "
                    "exceptions: they make you properly sick, so no drink until 48 hours after "
                    "the last tablet. If the label says avoid alcohol, it means it."),
    "codeine": ("Codeine and alcohol both slow you down, so keep it to nothing or one drink, and "
                "no driving or looking after a child on your own. Paracetamol or ibuprofen on "
                "their own are the safer pair with a drink."),
    "blood-pressure": ("Blood pressure tablets and statins are usually fine with a drink in "
                       "moderation: one or two, not a bottle. Alcohol lifts blood pressure a "
                       "little for a few hours, so a heavy night shows on the readings even when "
                       "the tablets are working. Grapefruit, not wine, is the thing to avoid with "
                       "simvastatin and atorvastatin."),
    "antihistamine": ("Antihistamines and alcohol both make you drowsy, and the older ones - "
                      "Piriton, chlorphenamine - far more than a once-a-day cetirizine or "
                      "loratadine. Keep it to one drink and don't drive on the pair; a non-drowsy "
                      "tablet taken in the morning leaves the evening free."),
    "antidepressant": ("Drinking on an SSRI such as sertraline is not forbidden, but alcohol blunts "
                       "the good the tablet is doing: expect a lower mood and worse sleep for a "
                       "day or two after. Keep it to one or two, and don't stack a sleeping tablet "
                       "on top. On an older MAOI such as phenelzine, drink and cheese are both off "
                       "the list."),
}


def _drink_and_the_drug(memory, reading):
    words = set(reading.get("words") or ())
    if words & {"metronidazole", "tinidazole", "antibiotic", "antibiotics", "penicillin",
                "amoxicillin", "trimethoprim", "nitrofurantoin"}:
        return DRINK_PILLS["antibiotics"]
    if words & {"codeine", "co codamol", "co-codamol", "cocodamol", "codamol"}:
        return DRINK_PILLS["codeine"]
    if words & {"blood pressure", "bp", "statin", "statins", "ramipril", "amlodipine",
                "lisinopril", "atorvastatin", "simvastatin", "rosuvastatin", "water tablet",
                "water tablets", "diuretic"}:
        return DRINK_PILLS["blood-pressure"]
    if words & {"antihistamine", "antihistamines", "hayfever", "hay fever", "piriton",
                "cetirizine", "loratadine", "chlorphenamine", "fexofenadine", "allergy"}:
        return DRINK_PILLS["antihistamine"]
    if words & {"antidepressant", "antidepressants", "sertraline", "fluoxetine", "citalopram",
                "escitalopram", "paroxetine", "venlafaxine", "mirtazapine", "ssri"}:
        return DRINK_PILLS["antidepressant"]
    if words & {"paracetamol", "acetaminophen", "calpol", "panadol"}:
        return DRINK_PILLS["paracetamol"]
    if words & {"ibuprofen", "nurofen", "brufen"}:
        return DRINK_PILLS["ibuprofen"]
    return ("One or two drinks is usually fine with an everyday medicine, taken with food. What "
            "decides it is the drug: ibuprofen and other anti-inflammatories irritate the stomach "
            "with alcohol, paracetamol's limit is the liver, codeine and antihistamines add to the "
            "drowsiness, and metronidazole must not meet alcohol at all. A pharmacist will check "
            "the one you actually take.")

WHITLOW_WORDS = ("whitlow", "whitlows", "paronychia", "felon", "nail infection",
                 "infected nail", "finger", "fingers", "thumb", "thumbs", "fingernail",
                 "fingernails", "nail", "nails", "fingertip", "fingertips", "cuticle",
                 "cuticles")

WHITLOW_REPLY = (
    "A red, hot, throbbing finger is an infection of the fingertip or the nail fold - a "
    "whitlow or paronychia - and warm salty water is what helps it: soak it for ten minutes "
    "three or four times a day, keep it clean and covered in between, and take paracetamol for "
    "the throb. Don't squeeze it or dig at the nail, because the fingertip is a closed space and "
    "pus pushed deeper is worse. See a GP the same day if the redness is spreading past the "
    "finger, there is pus, or you have a fever; a red streak running up the arm is 111 today. "
    "Have it looked at sooner if you have diabetes.")


def _names_a_finger(reading):
    said = " " + re.sub(r"[^a-z ]", " ", str(reading.get("clean") or "").lower()) + " "
    for word in WHITLOW_WORDS:
        if re.search(r"\b" + re.escape(word) + r"\b", said):
            return True
    return False


HOT_FLUSH_PHRASES = ("hot flushes", "hot flush", "night sweats", "sweats at night",
                     "perimenopause")
HOT_FLUSH_SECOND = ("40", "41", "42", "43", "44", "45", "46", "47", "48", "49", "50", "51",
                    "52", "53", "54", "55", "40s", "50s", "forties", "fifties", "night",
                    "sudden", "what can i", "help", "stop", "stopping", "hormone", "hrt",
                    "wake", "waking", "keep", "keeps", "getting", "having", "started",
                    "starting", "think")
NOT_A_FLUSH = ("toilet", "loo", "cistern", "drain", "radiator", "boiler", "washing", "tank")
A_CISTERN_FAULT = ("hiss", "hisses", "hissing", "whistling", "whistles", "trickling",
                   "trickle", "keeps filling", "wont stop filling", "wont stop running",
                   "topping up", "fill valve", "flush valve", "ballcock")
A_TOILET_JOB = ("replace a toilet", "replace the toilet", "replace my toilet", "replacing a toilet",
                "replacing the toilet", "toilet replacement", "new toilet", "old toilet",
                "toilet pan", "fit a toilet", "fit a new toilet", "fitting a toilet",
                "install a toilet", "installing a toilet", "install a new toilet",
                "swap the toilet", "swap a toilet", "swapping the toilet",
                "toilet needs replacing", "remove the toilet", "remove a toilet",
                "removing the toilet", "take the toilet out", "taking the toilet out",
                "replace a loo", "replace the loo", "replace my loo", "replacing the loo",
                "new loo", "old loo", "loo pan", "fit a new loo", "loo needs replacing",
                "fix the toilet", "fix my toilet", "fix a toilet", "fix the loo", "fix my loo",
                "repair the toilet", "repair my toilet", "broken toilet", "toilet is broken",
                "toilet has broken", "toilet seat", "toilet lid", "toilet roll", "toilet paper",
                "toilet brush", "cistern replacement", "toilet wont flush", "toilet won't flush",
                "toilet will not flush", "toilet keeps blocking")

YOUNG_FLUSH_AGES = ("18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29",
                    "30", "31", "32", "33", "34", "35", "36", "37", "38", "39",
                    "twenties", "thirties", "twenty", "thirty",
                    "before 40", "under 40", "in my twenties", "in my thirties")
YOUNG_FLUSH_REPLY = (
    "Hot flushes before 40 are usually not the menopause: an overactive thyroid is the commonest "
    "cause, and an infection, some medicines and low oestrogen from another cause do it too. The "
    "GP's first check is a thyroid blood test - and a pregnancy test before anything else if your "
    "periods have stopped. Note down how often they come and whether they bring a racing heart or "
    "weight change, because that is what tells the causes apart. See a GP if they are frequent, "
    "and the same day if you also have a fever or feel faint.")
HOT_FLUSH_REPLY = (
    "Hot flushes in midlife - most often the late forties and fifties - are usually perimenopause: "
    "keep the room cool, wear thin layers, cut back on alcohol and caffeine, and use a fan at "
    "night. HRT "
    "is the most effective treatment and is safe for most women - talk to a GP about your "
    "own risks, and mention any flushes with weight loss, a lump or bleeding after sex.")
MENOPAUSE_SIGNS_REPLY = (
    "The first sign is usually the periods changing - shorter or longer gaps, then skipped ones - "
    "with hot flushes, night sweats, broken sleep and a low mood for most women. The average age "
    "of the last period is 51, and a GP can tell from your symptoms without a blood test. Ask "
    "about HRT: it is the most effective help for flushes, sleep and mood, and safe for most "
    "women.")
MENOPAUSE_HOW_LONG_REPLY = (
    "Flushes and night sweats last about four years on average, and around one in ten women has "
    "them for 12 years or more. The years of changing periods before the last one usually start "
    "in the mid-forties, the average age of the last period is 51, and symptoms that start early "
    "or last long are worth a GP visit - HRT shortens them for most women.")
A_MANS_SWEATS = ("my husband", "my boyfriend", "my partner", "my dad", "my son", "my brother",
                 "he has", "he gets", "he keeps", "he is", "hes", "his night sweats",
                 "his sweats", "my husbands",
                 "im a man", "i am a man", "im male", "i am male", "as a man", "im a bloke",
                 "i am a bloke")
NOT_MY_OWN_BODY = ("my wife", "my husband", "my partner", "my mum", "my mother", "my nan",
                   "my nanna", "my gran", "my sister", "my friend", "my aunt", "my daughter",
                   "my son", "she is", "she has", "he is", "hes", "shes", "her periods",
                   "his")

DEHYDRATION_PLAIN = (
    "You are dehydrated if your urine is dark yellow, your mouth is dry, you are thirsty and "
    "headachy, and you feel flat or dizzy when you stand up; pale straw-coloured urine is the "
    "target. Drink little and often, a glass every hour or so, rather than a lot in one go, "
    "and if it came from heat, exercise or a stomach bug, an oral rehydration sachet from a "
    "pharmacy replaces the salts that water on its own misses. Water, squash and milk all "
    "count, and tea and coffee do too, as long as they are not the only thing you drink. "
    "Ring 111 or see a GP if you have not passed urine in eight hours, or you feel confused "
    "or drowsy, and get help sooner for a baby, a young child or someone elderly, who "
    "dehydrate quickly.")

DEHYDRATION_SICK = (
    "Give fluid in small sips, often: a spoonful of water or an oral rehydration drink every few "
    "minutes, because a glass at once is what comes straight back. An oral rehydration sachet "
    "(Dioralyte) made up exactly as the packet says is better than water alone while it is coming "
    "back up, and keep going while they are thirsty and their urine is still dark. Ring 111 or "
    "your GP today if a child has passed no urine for six hours, is floppy or hard to wake, or "
    "there is blood in the sick.")

KEEPING_FLUID_DOWN = (
    "keep down", "keeps down", "keep it down", "keep water down", "keep fluids down",
    "keep anything down", "keep food down", "kept down", "cant keep", "cannot keep",
    "can't keep", "wont keep", "won't keep",
    "vomit", "vomiting", "vomited", "being sick", "throwing up", "throw up", "thrown up",
    "diarrhoea", "diarrhea", "stomach bug", "norovirus", "gastro", "food poisoning")


def dehydration_help(memory, understood):
    text = ((understood or {}).get("clean") or "").lower()
    if any(phrase in text for phrase in KEEPING_FLUID_DOWN):
        return DEHYDRATION_SICK
    return DEHYDRATION_PLAIN


_RUNNING_WORDS = frozenset((
    "run", "runs", "running", "ran", "jog", "jogging", "jogged", "exercise", "exercising",
    "sprint", "sprinting", "cycling", "swim", "swimming", "walking", "walk", "gym", "training",
    "cramp", "cramps", "cramping", "diaphragm", "breathing"))


_A_SESSION = re.compile(
    r"\b(?:warming\s+up|warmed\s+up|warm\s*-?up|workout|work\s+out|working\s+out|"
    r"gym|weights|deadlift(?:s|ing)?|squat(?:s|ting)?|lunge(?:s|ing)?|"
    r"stretch(?:es|ing|ed)?|press\s*-?ups?|push\s*-?ups?|pull\s*-?ups?|"
    r"run|runs|running|ran|jog|jogging|jogged|cardio|training|trained|"
    r"after\s+lifting|lifting)\b")


_CANNOT_WARM = re.compile(
    r"\b(?:cant|can't|can not|couldnt|couldn't|never|hard|struggl\w*|unable|difficult\w*|"
    r"trouble|takes?\s+ages?)\b[^.!?]{0,20}?\b(?:warm|warmed)\b")


def _not_on_the_warm_up(understood):
    said = _the_line(understood)
    if _CANNOT_WARM.search(said):
        return True
    return not _A_SESSION.search(said)


def _a_wound_not_a_cramp(understood):
    words = [str(word).lower() for word in (understood.get("words") or ())]
    if not words:
        words = (understood.get("clean") or "").split()
    for word in words:
        if word in _RUNNING_WORDS:
            return False
    said = set(words)
    if said & {"stitches", "sutures", "suture", "glued", "glue", "staple", "staples"}:
        return True
    return bool(said & {"cut", "cuts", "wound", "wounds", "gash", "slashed", "bleeding"}) \
        and "stitch" in said


_SOMEONE_ELSE = re.compile(
    r"\b(?:my|his|her|their|our|mums|dads|sisters|brothers|friends)\s+"
    r"(?:mum|mom|mother|dad|father|son|daughter|child|kid|kids|teenager|teen|partner|husband|"
    r"wife|boyfriend|girlfriend|friend|mate|brother|sister|nan|grandma|grandad|nephew|niece|"
    r"colleague|boss|flatmate|roommate|baby|toddler)\b|"
    r"\b(?:in|of|with)\s+(?:a\s+)?(?:teenagers?|teens?|children|child|kids?|men|women|"
    r"pensioners|students)\b")


_SIGNS_ASK = re.compile(r"\b(?:signs?|symptoms?)\s+(?:of|for)\b")


def _is_the_readers_own_line(understood):
    said = str((understood or {}).get("clean") or "")
    if _SIGNS_ASK.search(said):
        return True
    return not _SOMEONE_ELSE.search(said)


_MMOL = re.compile(r"\b(\d{1,2}(?:\.\d)?)\s*(?:mmol)?\b")


MORNING_AFTER_CLOCK = (
    "Take it as soon as you can: levonorgestrel (Levonelle) works best in the first 24 hours and "
    "up to 72, and ulipristal (ellaOne) up to 120.")
MORNING_AFTER_FREE = (
    "It is free at most pharmacies without an appointment, and a sexual health clinic, walk-in "
    "centre or A&E will give it too.")
MORNING_AFTER_COIL = (
    "A copper coil fitted within five days is the most effective of all, and it still works after "
    "the pills' window has closed.")
MORNING_AFTER_EFFECT = (
    "Levonorgestrel stops about 95 in 100 pregnancies in the first 24 hours, about 85 in 100 from "
    "24 to 48 hours and about 58 in 100 from 48 to 72; ulipristal holds about 98 in 100 up to 120 "
    "hours, and the coil is over 99 in 100.")
MORNING_AFTER_OVULATED = (
    "Neither pill stops an egg that has already been released, which is why the coil is offered "
    "when you might have ovulated already.")
MORNING_AFTER_SICK = (
    "It can make you feel sick, and being sick within three hours of the tablet means going back "
    "for another dose, so ask about that when you collect it.")
MORNING_AFTER_AGE = (
    "There is no age limit: a pharmacist will supply it at any age, including under 16, and does "
    "not have to tell your parents or your GP.")
MORNING_AFTER_PREG = (
    "It is not an abortion pill and it cannot work if you are already pregnant, so do a test "
    "three weeks later if your period is late or unusual.")
MORNING_AFTER_FITTED = (
    "The coil is fitted in one appointment of about 15 minutes at a sexual health clinic, your "
    "GP surgery or a pharmacy that offers it, and it can go in on any day of your cycle.")
MORNING_AFTER_FITTED_HURT = (
    "It is uncomfortable for a minute or two, like a smear, and cramping for a day afterwards is "
    "normal.")

_MORNING_AFTER_LATE = re.compile(
    r"\bhow late\b|\btoo late\b|\bhow soon\b|\bhow long after\b|\bwindow\b|\bhours?\b"
    r"|\b72\b|\b120\b|\bfive days\b|\b5 days\b|\bhow quickly\b", re.IGNORECASE)
_MORNING_AFTER_FREEISH = re.compile(
    r"\bfree\b|\bcost\b|\bhow much\b|\bprice\b|\bpay\b|\bcharge\b|\bprescription\b",
    re.IGNORECASE)
_MORNING_AFTER_WHERE = re.compile(
    r"\bwhere\b|\bpharmac\w*|\bchemist\w*|\bboots\b|\bsuperdrug\b|\bgp\b|\bdoctor\b"
    r"|\bclinic\b|\bwalk[- ]in\b|\ba&e\b|\bhospital\b|\bonline\b", re.IGNORECASE)
_MORNING_AFTER_SICKS = re.compile(
    r"\bsick\b|\bnausea\b|\bnauseous\b|\bvomit\w*|\bthrow up\b|\bfeel ill\b"
    r"|\bside effects?\b|\bbad for you\b|\bharmful\b|\bunsafe\b", re.IGNORECASE)
_MORNING_AFTER_OVULATION = re.compile(r"\bovulat\w*|\balready released\b", re.IGNORECASE)
_MORNING_AFTER_HURTS = re.compile(
    r"\bhurt\w*|\bpain\w*|\bsore\b|\bagony\b|\buncomfortable\b|\bhow bad\b"
    r"|\bsick leave\b|\bday off\b", re.IGNORECASE)
_MORNING_AFTER_FITTED = re.compile(
    r"\bfitted\b|\bfitting\b|\bdoes it hurt\b|\bhurts?\b|\bpainful\b|\bappointment\b"
    r"|\bwhere do i get it\b|\bhow do i get it\b", re.IGNORECASE)
_MORNING_AFTER_COILS = re.compile(
    r"\bcoil\b|\biud\b|\bdifference\b|\bbetter than\b|\bwhich is better\b"
    r"|\bmore effective\b|\bwhich works\b", re.IGNORECASE)
_MORNING_AFTER_EFFECTIVE = re.compile(
    r"\beffective\w*|\bhow well\b|\breliable\b|\bsuccess\w*|\bchance\b|\bpercent\b"
    r"|\bhow safe\b|\bprotect\w*", re.IGNORECASE)
_MORNING_AFTER_LEVO = re.compile(r"\blevonorgestrel\b|\blevonelle\b|\bplan b\b", re.IGNORECASE)
_MORNING_AFTER_ULI = re.compile(r"\bulipristal\b|\bellaone\b|\bella one\b", re.IGNORECASE)
_MORNING_AFTER_OLD = re.compile(
    r"\bage limit\b|\bhow old\b|\bunder 1[68]\b|\b1[3-6] years old\b|\bim 1[3-6]\b"
    r"|\bi'm 1[3-6]\b|\bteenage\w*|\bmy daughter\b|\bmy son\b", re.IGNORECASE)


def _morning_after(memory, reading):
    understood = reading if isinstance(reading, dict) else {}
    text = str(understood.get("clean") or understood.get("text") or "")
    lead = None
    if _MORNING_AFTER_OLD.search(text):
        lead = MORNING_AFTER_AGE
    elif _MORNING_AFTER_SICKS.search(text):
        lead = MORNING_AFTER_SICK
    elif _MORNING_AFTER_OVULATION.search(text):
        lead = MORNING_AFTER_OVULATED
    elif (_MORNING_AFTER_HURTS.search(text)
          and re.search(r"\bcoil\b|\biud\b", text, re.IGNORECASE)):
        lead = MORNING_AFTER_FITTED_HURT
    elif (_MORNING_AFTER_FITTED.search(text)
          and re.search(r"\bcoil\b|\biud\b", text, re.IGNORECASE)):
        lead = MORNING_AFTER_FITTED
    elif _MORNING_AFTER_LEVO.search(text) and _MORNING_AFTER_ULI.search(text):
        lead = MORNING_AFTER_EFFECT
    elif _MORNING_AFTER_COILS.search(text):
        lead = MORNING_AFTER_COIL
    elif _MORNING_AFTER_EFFECTIVE.search(text):
        lead = MORNING_AFTER_EFFECT
    elif _MORNING_AFTER_FREEISH.search(text) or _MORNING_AFTER_WHERE.search(text):
        lead = MORNING_AFTER_FREE
    elif _MORNING_AFTER_LATE.search(text):
        lead = MORNING_AFTER_CLOCK
    if lead is None:
        rest = [MORNING_AFTER_CLOCK, MORNING_AFTER_FREE, MORNING_AFTER_COIL, MORNING_AFTER_PREG]
        limit = 4
    else:
        limit = 3
        if lead is MORNING_AFTER_EFFECT:
            rest = [lead, MORNING_AFTER_FREE, MORNING_AFTER_PREG]
        elif lead is MORNING_AFTER_FITTED_HURT:
            rest = [lead, MORNING_AFTER_FITTED, MORNING_AFTER_CLOCK]
        elif lead is MORNING_AFTER_FITTED:
            rest = [lead, MORNING_AFTER_FITTED_HURT, MORNING_AFTER_CLOCK]
        elif lead is MORNING_AFTER_OVULATED:
            rest = [lead, MORNING_AFTER_COIL, MORNING_AFTER_CLOCK]
        else:
            base = [MORNING_AFTER_CLOCK, MORNING_AFTER_FREE, MORNING_AFTER_COIL,
                    MORNING_AFTER_PREG]
            if lead is MORNING_AFTER_COIL:
                base = [MORNING_AFTER_CLOCK, MORNING_AFTER_FREE, MORNING_AFTER_PREG]
            rest = [lead] + [sentence for sentence in base if sentence is not lead]
    said, seen = [], set()
    for sentence in rest:
        if sentence in seen:
            continue
        seen.add(sentence)
        said.append(sentence)
        if len(said) == limit:
            break
    return " ".join(said)


def _a_high_reading(words):
    for match in _MMOL.finditer((words or "").lower()):
        try:
            if float(match.group(1)) >= 15:
                return True
        except ValueError:
            continue
    return False


_NAMES_A_DOCTOR = re.compile(
    r"\b(gp|g\.p\.|doctor|doctors|nurse|surgery|practice nurse|consultation)\b", re.IGNORECASE)
_SAYS_IT_OUT_LOUD = re.compile(
    r"\b(talk|talks|talking|tell|telling|raise|raising|mention|mentioning|bring it up|"
    r"bring up|say|saying|explain|explaining|ask|asking|broach|approach)\b", re.IGNORECASE)


def _not_a_line_about_how_to_tell_the_doctor(understood):
    if not isinstance(understood, dict):
        return True
    said = str(understood.get("text") or understood.get("clean") or "")
    return not (_NAMES_A_DOCTOR.search(said) and _SAYS_IT_OUT_LOUD.search(said))

_NAMES_A_DENTAL_CAUSE = re.compile(
    r"\b(?:dentist|dentists|dental|filling|fillings|tooth out|teeth out|tooth pulled|"
    r"tooth removed|extraction|extractions|root canal|"
    r"wisdom tooth|wisdom teeth|implant|implants|novocaine|lidocaine)\b",
    re.IGNORECASE)
_SAYS_NUMB = re.compile(r"\b(?:numb|numbness|numbed|number than|going numb|gone numb)\b",
                        re.IGNORECASE)
_NAMES_A_STROKE_SIGN = re.compile(
    r"\b(?:droop\w*|twisted|twitching down|slurr\w*|slurring|"
    r"(?:won'?t|wont|can'?t|cannot|can not|not able to|unable to)\s+(?:move|moving|close|smile)|"
    r"half (?:of )?my face|one side of my face|side of my face (?:has|is) (?:gone|dropped|numb|drooping)|"
    r"face (?:is )?(?:going|gone) (?:numb|droopy)|eye (?:won'?t|wont|can'?t) close|"
    r"mouth (?:is )?(?:drooping|dropped)|smile (?:is )?(?:crooked|lopsided|uneven))\b",
    re.IGNORECASE)


def _the_dentist_numbed_it(understood):
    if not isinstance(understood, dict):
        return False
    said = str(understood.get("text") or understood.get("clean") or "")
    if _NAMES_A_STROKE_SIGN.search(said):
        return False
    return bool(_NAMES_A_DENTAL_CAUSE.search(said) and _SAYS_NUMB.search(said))



_TURNED_DOWN = re.compile(
    r"\b(?:turn|turns|turned|turning)\s+(?:me|us|him|her|them|it|you|my)\s+down\b"
    r"|\b(?:turned|turning|turns)\s+down\s+(?:for|at|by|the|a)\b")
_HOW_IT_LEFT_THEM = re.compile(
    r"\b(?:sad|sadness|low|down in the dumps|miserable|unhappy|glum|blue|fed up|tearful|weepy|"
    r"flat|in a rut|stuck in a rut|cheer|happier|awful|terrible|rubbish|crap|horrible|gutted|"
    r"heartbroken|cry|crying|tears|hopeless|worthless|no joy)\b")


def _a_refusal_is_not_a_mood(understood):
    said = str((understood or {}).get("clean") or (understood or {}).get("text") or "").lower()
    return bool(_TURNED_DOWN.search(said)) and not _HOW_IT_LEFT_THEM.search(said)


_A_HOME_WORD = re.compile(
    r"\b(?:house|home|flat|flats|room|rooms|bedroom|bedrooms|kitchen|living room|sitting room|"
    r"lounge|garage|shed|cellar|basement|loft|attic|conservatory|hall|hallway|porch|workshop|"
    r"caravan|bungalow|cottage|office|bedsit|storage heater)\b", re.I)
_A_COLD_OR_DAMP_WORD = re.compile(
    r"\b(?:cold|colder|coldest|freezing|chilly|chilled|perishing|freeze|freezes|frozen|"
    r"warm|warmer|warmest|warmth|heating|heated|radiator|radiators|boiler|thermostat|"
    r"draught|draughts|draughty|draft|drafts|drafty|damp|damps|dampness|damp patch|"
    r"mould|mouldy|mold|moldy|condensation|insulation|insulate|double glazing)\b", re.I)


def not_a_cold_or_damp_house(understood):
    said = str((understood or {}).get("clean") or (understood or {}).get("text") or "")
    return not (_A_HOME_WORD.search(said) and _A_COLD_OR_DAMP_WORD.search(said))


_MOOD_WORDS = ("blue", "flat", "low", "down")
_MOOD_THE_STATE = ("is", "am", "are", "was", "were", "feel", "feeling",
                   "look", "looks", "looked", "looking", "seem", "seems", "seemed",
                   "go", "goes", "went", "gone",
                   "come", "comes", "came", "turn", "turns", "turned", "get", "gets",
                   "got",
                   "taste", "tastes", "tasted", "felt", "feels")
_MOOD_SAID_OF_A_PERSON = ("feel", "feels", "feeling", "felt", "mood", "moods", "i", "im",
                          "i'm", "me", "myself", "we", "us", "you", "he", "she", "they",
                          "them", "it", "everything", "nothing", "anything", "things",
                          "life", "day", "days", "week", "weeks", "lately", "recently",
                          "ive", "i've", "id", "i'd", "im", "weve", "we've", "hes", "he's",
                          "shes", "she's", "theyre", "they're", "youre", "you've")
_MOOD_THE_NOUN = ("my", "your", "our", "their", "his", "her", "its", "the", "a", "an",
                  "this", "that", "these", "those")
_MOOD_JOIN = frozenset("and but or so also too plus".split())
_MOOD_HELPERS = frozenset("""
have has had having been being be am is are was were got gets getting still quite really very so
a an bit lot more most that
""".split()) | frozenset("""
just only even ever never always sometimes often usually mainly mostly actually literally
genuinely honestly probably prob kinda sorta rather pretty all completely totally little
kind of about around dont do does did didnt not yet more less
""".split())
_MOOD_FEELING_SAID = frozenset("""
    feel feels feeling felt mood moods unhappy miserable depressed
""".split())
_MOOD_A_HOME_FLAT = ("my flat", "the flat", "a flat", "new flat", "old flat", "damp flat",
                     "empty flat", "rented flat", "rent a flat", "buy a flat", "sell a flat",
                     "flatmate", "flatmates", "flat share", "flatshare", "flat next door",
                     "into a flat", "into a new flat", "moved flat", "move flat", "moving flat",
                     "leave the flat", "leaving the flat", "in the flat", "from the flat")
_MOOD_THE_VERB_BEFORE = frozenset("""
    stop stopped stopping keep keeps kept want wants wanted try trying tried help helps helped
    avoid prevent beat end fix cope deal handle handling getting get gets got start started
    starting begin began keepon carry carryon
""".split())
_MOOD_WHERE_THE_PERSON_WAS = frozenset("""
    in at from to on into onto off out outside inside back home work up down over
    after before about with around around near by through
    came come comes coming went go goes going gone got get gets getting left leave leaving
    arrived arrive arriving sat sit sitting stood standing lay lying stayed stay walking
    drove drive driving cycled cycled home
""".split())
_MOOD_TIME = frozenset("""
    today tonight lately recently now again still anymore sometimes often always
    yesterday tomorrow morning evening weekend weeks days months years
""".split())
_MOOD_ADVERB = ("so", "too", "really", "very", "quite", "pretty", "all", "still", "always",
                "a", "bit", "little", "completely", "totally", "kind", "of", "just", "rather")


def _the_mood_is_the_persons(understood):
    if not isinstance(understood, dict):
        return True
    words = [w for w in _the_line(understood).split() if w]
    if not words:
        return True
    bare = [w for w in words if w not in _MOOD_THE_NOUN]
    if "flat" in bare and not any(w in _MOOD_FEELING_SAID for w in bare):
        said = " ".join(bare)
        if any(cue in said for cue in _MOOD_A_HOME_FLAT):
            return False
    thing_said = False
    person_said = False
    for i, word in enumerate(bare):
        if word not in _MOOD_WORDS:
            continue
        j = i - 1
        while j >= 0 and bare[j] in _MOOD_ADVERB:
            j -= 1
        found = None
        for k in range(j, max(j - 3, -1), -1):
            if bare[k] in _MOOD_THE_STATE:
                found = k
                break
        if found is None:
            nxt = bare[i + 1] if i + 1 < len(bare) else ""
            if nxt in _MOOD_JOIN:
                continue
            if nxt and nxt not in _MOOD_TIME and nxt not in _MOOD_SAID_OF_A_PERSON:
                thing_said = True
            continue
        at = found - 1
        if found == j:
            k = found - 1
            while k >= 0 and bare[k] in _MOOD_HELPERS:
                k -= 1
            at = k
            pass
        else:
            between = bare[found + 1:i]
            kept = len(between)
            while kept and between[kept - 1] in _MOOD_ADVERB:
                kept -= 1
            if any(w in _MOOD_JOIN for w in between[:kept]):
                person_said = True
                continue
            if any(w in _MOOD_SAID_OF_A_PERSON for w in between[:kept]):
                person_said = True
                continue
            if any(w in _MOOD_ADVERB for w in bare[found + 1:i]):
                k = found - 1
                while k >= 0 and bare[k] in _MOOD_HELPERS:
                    k -= 1
                at = k
            else:
                at = found + 1
        subject = bare[at] if 0 <= at < len(bare) else ""
        if at > 0 and bare[at - 1] in _MOOD_WHERE_THE_PERSON_WAS:
            person_said = True
            continue
        if (subject in _MOOD_SAID_OF_A_PERSON or subject == ""
                or subject in _MOOD_THE_VERB_BEFORE
                or subject in _MOOD_JOIN
                or subject in _MOOD_WORDS):
            person_said = True
            continue
        thing_said = True
    return person_said or not thing_said


_BLUES_SAID = ("baby blues", "how long", "normal", "when does it", "should it last",
              "how many days", "still last")


_A_BABY_IN_THE_LINE = re.compile(
    r"\bbaby\b|\bbabies\b|\bnewborn\b|\bbirth\b|\bgave birth\b|\bchildbirth\b|"
    r"\bpregnan|\bcaesarean\b|\bc section\b|\bc-section\b|\bmaternity\b|\bmidwife\b|"
    r"\bhealth visitor\b|\bpostnatal\b|\bpostpartum\b|\bpost natal\b", re.I)


def _about_a_baby(understood):
    said = understood if isinstance(understood, dict) else {}
    text = str(said.get("text") or said.get("clean") or "")
    if not text:
        text = " ".join(str(one) for one in (said.get("words") or ()))
    return bool(_A_BABY_IN_THE_LINE.search(text))


def _postnatal_mood_reply(memory, understood):
    clean = " " + str((understood or {}).get("clean") or "").lower() + " "
    if any(word in clean for word in _BLUES_SAID) and "depression" not in clean \
            and "weeks" not in clean and "months" not in clean:
        return ("The baby blues are the ordinary version: tearful, irritable and overwhelmed, "
                "starting around day three to five and gone within about ten days to a fortnight. "
                "Sleep when the baby sleeps, eat and drink something at every feed, and take the "
                "help that is offered. If it has not lifted by two weeks, or it is getting worse "
                "rather than better, tell your health visitor or GP - that is when it is called "
                "postnatal depression and it needs treating.")
    return ("What you are describing is common - about one new parent in ten has postnatal "
            "depression - and it is treatable, so tell your GP or health visitor, who asks about "
            "this every week and will not be surprised. It is not the baby blues if it lasts past "
            "the first fortnight, starts months later, or comes with feeling numb about the baby, "
            "guilt, no appetite, or panic; it is not a failure of love and it does not mean anyone "
            "will take the baby away. Talking therapy works, and antidepressants can be taken "
            "while breastfeeding. Ring your GP today, and if you ever think about harming yourself "
            "or the baby, ring 111 or 999 or go to A&E.")


HEAVY_THING = ("sofa", "couch", "settee", "armchair", "washing machine", "washer",
               "tumble dryer", "fridge", "fridge freezer", "freezer", "wardrobe", "sideboard",
               "bookcase", "bookshelf", "piano", "table", "desk", "divan",
               "boxes", "furniture", "chest of drawers", "dresser", "cabinet", "filing cabinet",
               "tv", "television", "paving slab", "slabs", "pallets", "boiler")
LIFT_VERB = ("lifted", "lifting", "lift", "carried", "carrying", "carry", "hauled", "hauling",
             "dragged", "dragging", "shifted", "shifting", "heaved", "heaving", "humped",
             "lugged", "lugging", "manhandled", "picked up", "picking up", "took up",
             "getting it up", "got it up")
LIFT_HAS_A_CARD = (
    "van", "transit", "transport", "removal", "removals", "man with a van", "hire", "hiring",
    "upstairs", "up the stairs", "downstairs", "stairwell", "stairs", "through the door",
    "round the corner", "measure", "measuring", "narrowest",
    "gym", "weights", "deadlift", "deadlifts", "squat", "squats", "bench press", "barbell",
    "dumbbell", "dumbbells", "kettlebell", "workout", "routine", "reps", "protein",
    "stain", "stains", "stained", "mark", "marks", "spill", "spilled", "spilt", "smell",
    "smells", "clean", "cleaning", "scrub", "repair", "broken", "not working", "faulty",
    "leaking", "wobble", "wobbles", "noisy", "price", "cost", "how much", "worth")

_A_NIGHT = re.compile(
    r"\b(?:all night|at night|in the night|every night|each night|most nights|last night|"
    r"night time|nighttime|overnight|twice a night|two or three times a night|"
    r"a few times a night|through the night)\b", re.I)
_UP_TO_THE_LOO = re.compile(
    r"\b(?:running|run|runs|ran|going|go|goes|went|up and down|in and out|trips?|visits?|"
    r"nipping|dashing)\b[^.?!]{0,24}?\b(?:to|into)\s+(?:the\s+|my\s+)?"
    r"(?:loo|toilet|toilets|bathroom|bog|john|restroom|washroom|lavatory)\b", re.I)
_A_STOMACH_SAID = re.compile(
    r"\b(?:diarrhoea|diarrhea|runs|trots|tummy|stomach|belly|guts|loose|vomit\w*|"
    r"throwing up|sick|d&v|stools?|poo|pooing|number twos?)\b", re.I)


def _not_a_night_of_going(understood):
    said = understood if isinstance(understood, dict) else {}
    text = " ".join(str(said.get(key) or "")
                    for key in ("clean", "text", "norm_text", "raw")).lower()
    if _A_STOMACH_SAID.search(text):
        return True
    return not (_A_NIGHT.search(text) and _UP_TO_THE_LOO.search(text))


_SOMEBODY_NAMED = re.compile(
    r"\b(?:mum|mums|mam|mom|mother|dad|dads|father|husband|wife|partner|boyfriend|girlfriend|"
    r"son|sons|daughter|child|children|kid|kids|nan|nana|gran|granny|grandma|grandad|grandpa|"
    r"sister|brother|aunt|uncle|cousin|friend|neighbour|neighbor|patient|client|elderly|"
    r"his|her|their|him|them)\b", re.I)


def _my_own_appetite(understood):
    said = str((understood or {}).get("clean") or (understood or {}).get("text") or "")
    return not _SOMEBODY_NAMED.search(said)


_NOT_A_CONDITION = re.compile(
    r"\b(?:not|never|no longer|isnt|arent|wasnt|werent)\s+(?:a\s+|an\s+|even\s+)?(?:%s)\b")


def _not_a_denial_of(*subject):
    words = "|".join(r"\s+".join(str(word).split())
                     for word in sorted(subject, key=len, reverse=True))
    pattern = re.compile(_NOT_A_CONDITION.pattern % words)

    def guard(understood):
        if not isinstance(understood, dict):
            return True
        said = understood.get("text") or understood.get("clean") or ""
        if not said:
            said = " ".join(understood.get("words") or ())
        return not pattern.search(str(said).lower())

    return guard


_SAID_COLD = re.compile(
    r"\b(?:is|are|was|were|feels|feel|felt|feeling|being|getting)\s+"
    r"(?:(?:a\s+bit|a\s+little|a\s+tad|a\s+lot|a\s+touch|really|so|very|too|that|quite|"
    r"proper|bloody|dead|still|always|freezing)\s+)*(?:cold|freezing|frozen|chilled)\b")

_SAID_HOT = re.compile(
    r"\b(?:is|are|was|were|feels|feel|felt|feeling|being|getting)\s+"
    r"(?:(?:a\s+bit|a\s+little|a\s+tad|a\s+lot|a\s+touch|really|so|very|too|that|quite|"
    r"proper|bloody|dead|still|always|absolutely)\s+)*"
    r"(?:hot|boiling|roasting|sweltering|sweaty|sweating|shivery|shivering|feverish)\b")


_THE_WORD_IS_A_HEAP = re.compile(
    r"\b(?:piles?|piling|piled)\s+up\b|\bpiling\b|\bpiles?\s+of\b", re.IGNORECASE)


def _a_heap_not_the_condition(understood):
    clean = " ".join(str((understood or {}).get(key) or "")
                     for key in ("clean", "norm_text", "text")).lower()
    return not _THE_WORD_IS_A_HEAP.search(clean)


ENTRIES = [
    entry("my-appetite-has-gone",
          (("loss of appetite", "appetite has gone", "appetite is gone", "appetite went",
            "appetite has disappeared", "appetite has vanished", "appetite is poor",
            "poor appetite", "gone off my food", "dont fancy food", "don't fancy food",
            "never hungry", "never feel hungry", "not interested in food",
            "no appetite for weeks", "no appetite for days", "no appetite since",
            "no appetite at all"),
           ("appetite", "loss", "food", "eating", "eat", "hungry", "hunger", "meals", "meal",
            "weeks", "days", "lately", "months", "my", "i", "ive", "i've", "gone", "lost")),
          "Appetite usually goes with something rather than on its own: a bug or an infection "
          "that has not quite cleared, stress or low mood, or a new medicine - some kill appetite "
          "and the leaflet will say so. Meanwhile eat by the clock rather than by hunger: "
          "something small every two or three hours, whatever you fancy, with a glass of milk or "
          "a yoghurt in between, because you will eat more in small amounts than at one plate. "
          "See a GP if it lasts more than a fortnight, if you are losing weight without trying, "
          "or if you are also low, sleeping badly or thirsty all the time.",
          avoid=PETS + ("my mum", "my dad", "my mother", "my father", "my husband", "my wife",
                        "my partner", "my son", "my daughter", "my nan", "my gran",
                        "my sister", "my brother", "my friend", "my neighbour", "elderly",
                        "care home", "dementia", "anorexia", "eating disorder", "bulimia",
                        "lose weight", "losing weight", "diet", "dieting", "fasting",
                        "intermittent", "gym", "workout", "chemo", "chemotherapy"),
          guard=_my_own_appetite,
          bias=1),
    entry("headache-help", (("headache", "headaches", "head", "heads"),
                            ("help", "stop", "get rid", "painkiller", "paracetamol", "bad",
                             "have", "got", "ive", "i've", "banging", "killing", "throbbing",
                             "hurts", "days", "week", "afternoon", "every day", "all day",
                             "anything", "what can i take", "without", "naturally", "tablets",
                             "pills", "medicine")),
          headache_help,
          ask=("killing", "banging", "bang", "pounding", "throbbing", "splitting", "hurts", "hurt",
               "ache", "aching", "pain", "headache", "headaches"),
          avoid=("migraine", "aura", "sudden", "worst", "vision", "stiff", "numb", "fainted",
                 "blood", "spinning", "dizzy", "dizziness", "vertigo", "hangover",
                 "every day", "everyday", "most days", "daily", "all day", "all the time",
                 "for days", "five days", "three days", "constant", "always",
                 "my daughter", "my son", "my child", "my kids", "my kid", "toddler", "school",
                 "child", "children")),
    entry("stop-a-cold-spreading",
          (("spread", "spreading", "going round", "pass it on", "passing it on", "catch it",
            "catching it", "not catch", "keep catching"),
           ("cold", "colds", "flu", "bug", "sniffles", "office", "house", "family", "everyone")),
          "It is hands and air: wash them for twenty seconds after a tissue or a sneeze, keep the "
          "windows open rather than the heating up, and do not share cups, towels or a keyboard. "
          "A cold is infectious for a day or two before the sneezing starts, so it is already "
          "round the office before anyone looks ill.",
          avoid=("stomach", "sick", "vomiting", "diarrhoea", "being sick", "norovirus",
                 "nursery", "childminder", "school", "kids", "child", "children", "baby",
                 "toddler", "butter", "jam", "toast", "mould", "mold", "rash", "measles",
                 "chickenpox")),

    entry("contagious-window",
          (("contagious", "infectious", "still catching", "pass it on", "pass it to",
            "give it to", "catch it", "still spreading", "spreading it"),
           ("bug", "bugs", "stomach", "tummy", "belly", "cold", "colds", "flu", "cough",
            "covid", "coronavirus", "corona", "virus", "infection", "illness", "sick",
            "sickness", "sore throat", "temperature", "fever", "rash", "spots", "it", "this",
            "that"),
           ("how long", "how many days", "when can i", "when is it", "when am i", "until",
            "still", "after", "before symptoms", "back to work", "back at work", "back to school",
            "or not", "ok to", "safe to")),
          ("You are most infectious in the day or two before symptoms and at their "
           "worst. Covid: ten days from two days before, to 24 hours clear of a fever; flu from a "
           "day before to seven days; a cold for a week from the first sore throat; a stomach bug "
           "while the diarrhoea lasts and 48 hours after; chickenpox two days before the rash to "
           "the spots crusting. Stay off while there is a fever."),
          guard=_an_illness_the_card_covers,
          avoid=("chickenpox", "chicken pox", "cold sore", "cold sores", "norovirus",
                 "verruca", "wart", "warts", "measles", "mumps", "glandular fever",
                 "how do i stop", "stop it spreading", "going round", "not catch",
                 "prevent", "avoid catching",
                 "covid last", "covid lasts", "covid lasting", "does covid last",
                 "covid symptoms", "covid test", "tested positive",
                 "lateral flow"),
          bias=2),
    entry("cold-duration", (("a cold", "the cold", "my cold", "common cold", "cold for",
                             "cold is", "cold has", "has a cold", "got a cold", "bad cold",
                             "cold going round", "colds going round"),
                            ("days", "week", "how long", "last", "lingering", "still",
                             "normal")),
          "A normal cold lasts about a week to ten days, and the cough can hang on for two or "
          "three. Rest, fluids and paracetamol are the treatment; see a GP if it's getting worse "
          "after a week rather than better.",
          avoid=("hands", "hand", "fingers", "fingertips", "toes", "toe", "feet", "foot",
                 "raynauds", "raynaud", "raynaud's", "circulation",
                 "weather", "outside", "freezing", "heating", "jacket", "cold sore", "beer",
                 "fridge", "freezer", "lager", "cider", "wine", "milk", "leftovers",
                 "left out", "food", "meat", "cook", "roast", "chicken", "oven", "bake",
                 "recipe", "sarnie", "sandwich", "cold day", "cold days", "cold morning",
                 "cold night", "cold outside", "cold enough",
                 "pack", "packing", "packed", "suitcase", "luggage", "backpack", "rucksack",
                 "wear", "wearing", "clothes", "layers", "holiday", "trip", "away",
                 "see someone", "see a doctor", "see the doctor", "go to the doctor",
                 "worth seeing", "should i see", "should i go",
                 "can i still", "can i run", "can i train", "can i exercise", "can i swim",
                 "can i go to the gym", "should i run", "should i train", "should i exercise",
                 "run with", "train with", "exercise with", "gym", "running", "swim",
                 "swimming", "football", "training",
                 ) + TOOTH_OR_GUM),
    entry("someone-is-cold",
          (("mum", "mom", "mother", "dad", "father", "nan", "nana", "gran", "granny", "grandad",
            "grandma", "grandpa", "husband", "wife", "partner", "boyfriend", "girlfriend",
            "son", "daughter", "kid", "kids", "child", "children", "sister", "brother", "aunt",
            "uncle", "cousin", "friend", "mate", "neighbour", "neighbor", "flatmate",
            "housemate", "she", "he", "they", "them"),
           ("is cold", "are cold", "feels cold", "feel cold", "feeling cold", "being cold",
            "gone cold", "so cold", "very cold", "really cold", "that cold", "too cold",
            "freezing", "shivering", "shivery")),
          "Get them warm before anything else: dry layers, a hot drink, a blanket and the heating "
          "on, and sit with them for a bit. Being cold on its own is usually just the room - an "
          "older person sits still and does not feel it coming - but cold with drowsiness, "
          "confusion, slurred speech or shivering that has stopped is hypothermia, and that is a "
          "111 call. Ring 999 if they are unconscious or breathing oddly.",
          shape=(lambda words: bool(_SAID_COLD.search(words)),),
          guard=lambda understood: (understood or {}).get("warmth") in COLD_WARMTH_WORDS,
          avoid=("baby", "babies", "newborn", "new born", "infant", "toddler", "cot", "cots",
                 "sleepsuit", "sleep suit", "sleeping bag", "at night", "in the night",
                 "bedroom", "room", "room is cold", "rooms", "house", "flat", "heating",
                 "radiator", "radiators", "boiler", "thermostat", "layers", "how many layers",
                 "nursery", "week old", "weeks old", "month old", "months old",
                 "cold sore", "cold sores", "sore", "symptom", "symptoms"),
          bias=2),
    entry("someone-is-hot",
          (("mum", "mom", "mother", "dad", "father", "nan", "nana", "gran", "granny", "grandad",
            "grandma", "grandpa", "husband", "wife", "partner", "son", "daughter", "kid", "kids",
            "child", "children", "sister", "brother", "aunt", "uncle", "cousin", "friend",
            "mate", "neighbour", "neighbor", "flatmate", "housemate", "toddler"),
           ("is hot", "are hot", "feels hot", "feel hot", "feeling hot", "being hot",
            "gone hot", "so hot", "very hot", "really hot", "that hot", "too hot", "boiling",
            "roasting", "sweltering", "sweaty", "sweating", "shivery", "shivering", "feverish")),
          "Take their temperature before anything else: 38C or above is a fever, and rest, "
          "plenty of fluids and paracetamol or ibuprofen are what bring it down. Get advice the "
          "same day for a fever with a stiff neck, a rash that does not fade under a glass, "
          "breathlessness, confusion or not drinking, and ring 999 if they are hard to wake. "
          "An older person with a temperature can go downhill quietly, so a hot nan who is also "
          "drowsy or muddled is a 111 call rather than a wait.",
          shape=(lambda words: bool(_SAID_HOT.search(words)),),
          guard=lambda understood: (understood or {}).get("warmth") in HOT_WARMTH_WORDS,
          avoid=("attractive", "good looking", "good-looking", "looks", "look", "handsome",
                 "pretty", "gorgeous", "fit", "tinder", "date", "dating", "fancy", "fancied",
                 "baby", "babies", "newborn", "new born", "infant", "weeks old", "week old",
                 "months old", "month old", "cot", "sleepsuit", "sleep suit", "room", "house",
                 "flat", "heating", "radiator", "boiler", "thermostat", "oven", "pan", "curry",
                 "chilli", "sauce", "weather", "outside", "sun", "hot tub", "water bottle",
                 "menopause", "hot flush", "hot flushes", "flushes", "period", "pregnant",
                 "pregnancy", "symptom", "symptoms"),
          bias=2),
    entry("ibuprofen-dose", (("ibuprofen", "brufen", "nurofen", "anti inflammatory", "painkiller"),
                             ("how much", "how many", "dose", "dosage", "can i take", "safe",
                              "maximum", "much can", "should i take", "should i be taking",
                              "ok to take", "worth taking", "should i have", "shall i take",
                              "alright to take", "all right to take", "good idea to take",
                              "ok", "okay", "is it ok", "is it safe", "alright", "allowed",
                              "best", "what painkiller", "which painkiller", "what should i take",
                              "what can i take", "what to take", "is best")),
          "For an adult: 200 to 400 mg every four to six hours, at most 1200 mg a day without a "
          "doctor's say-so, and always with food. Skip it if you have a stomach ulcer, kidney "
          "trouble, asthma that aspirin sets off, or are past 20 weeks pregnant; paracetamol is the "
          "safer default. A pharmacist will settle the dose for your case.",
          avoid=("child", "baby", "toddler", "son", "daughter", "kid", "dog", "cat", "pet",
                 "puppy", "paracetamol", "overdose", "year old", "years old", "months old",
                 "my boy", "my girl", "infant", "weighs", "give my", "give him", "give her",
                 "pregnant", "pregnancy", "expecting", "breastfeeding", "breast feeding",
                 "nursing",
                 "newborn", "newborns", "new born", "neonate", "neonates", "week old",
                 "weeks old", "month old", "under 3 months", "under three months",
                 "before or after food", "empty stomach", "with food", "without food",
                 "with a meal", "before food", "after food",
                 "antibiotic", "antibiotics")
                 + DRINK),

    entry("melatonin", (("melatonin", "melatonine", "melatonin gummies", "melatonin spray",
                         "sleeping tablets", "sleeping tablet", "sleeping pills", "sleeping pill"),
                        ("sleep", "sleeping", "asleep", "bed", "bedtime", "night", "wake",
                         "waking", "insomnia", "jet lag", "shift", "safe", "ok", "okay",
                         "give", "take", "taken", "works", "work", "help", "should", "can",
                         "much", "dose", "dosage", "long", "start", "stop", "good", "worth",
                         "for", "use", "child", "kid", "kids", "son", "daughter", "toddler",
                         "baby", "teen", "teenager", "year old", "years old", "tablet",
                         "tablets", "natural", "addicted", "dependent", "breastfeeding",
                         "what is", "whats", "what's", "what is a",
                         "breast feeding", "nursing", "pregnant", "pregnancy", "while",
                         "while breastfeeding", "while breast feeding", "while pregnant")),
          _melatonin,
          bias=1,
          avoid=("overdose", "too many", "took a bottle", "took the lot", "suicide",
                 "kill myself", "self harm", "swallowed", "took all")),

    entry("tablet-side-effects", SIDE_EFFECT_KEYS,
          _tablet_side_effects,
          bias=2,
          avoid=("ipad", "apple", "samsung", "android", "screen", "touch screen", "touchscreen",
                 "charge", "charging", "charger", "battery", "wifi", "wi fi", "app", "apps",
                 "wont turn on", "won't turn on", "restart", "reset", "laptop", "phone",
                 "game", "gaming", "motion sickness", "car", "reading", "bright",
                 "sleeping tablet", "sleeping tablets", "sleeping pill", "sleeping pills",
                 "melatonin",
                 "pregnant", "pregnancy", "breastfeeding", "breast feeding", "expecting",
                 "morning after", "emergency contraception", "plan b", "levonelle", "ellaone",
                 "condom split", "condom broke", "unprotected sex",
                 "child", "children", "baby", "toddler", "kid", "kids", "son", "daughter",
                 "year old", "years old", "months old", "dog", "cat", "pet", "puppy",
                 "overdose", "took the lot", "too many", "suicide", "kill myself", "self harm")),

    entry("tablet-not-helping",
          (("tablet", "tablets", "pill", "pills", "capsule", "capsules", "medicine",
            "medication", "prescription", "prescribed") + tuple(sorted(NAMED_MEDICINES)),
           ("didnt work", "didn't work", "doesnt work", "doesn't work", "didnt help",
            "didn't help", "not helping", "not working", "arent working", "aren't working",
            "stopped working", "no better", "not better", "still in pain", "still hurts",
            "took a tablet", "took the tablet", "took the tablets", "taking tablets",
            "taking a tablet", "on tablets", "dose", "dosage", "side effect", "side effects",
            "twice a day", "once a day", "every day", "a day", "per day", "at once",
            "two at once", "in one go", "how many", "how much", "is it enough",
            "touching the pain", "touching it", "not touching", "isnt touching",
            "doesnt touch", "does nothing", "doesnt do anything", "no good",
            "wearing off", "stopped helping", "still aching", "didnt touch")),
          _tablet_not_helping,
          bias=3,
          guard=_the_named_medicine_has_not_helped,
          avoid=("ipad", "apple", "samsung", "android", "screen", "touch screen", "touchscreen",
                 "charge", "charging", "charger", "battery", "wifi", "wi fi", "app", "apps",
                 "turn on", "wont turn on", "won't turn on", "wont start", "won't start",
                 "restart", "reset", "laptop", "phone", "tablet pc", "stylus", "factory",
                 "update", "software", "cracked", "keyboard", "storage", "slow", "frozen",
                 "pregnant", "pregnancy", "breastfeeding", "breast feeding", "expecting",
                 "morning after", "emergency contraception", "plan b", "levonelle", "ellaone",
                 "condom split", "condom broke", "unprotected sex",
                 "prescription charge", "prescription charges", "prepayment certificate",
                 "prepayment", "how much is a prescription", "how much does a prescription",
                 "how much are prescriptions", "pay for a prescription", "pay for prescriptions",
                 "pay for my prescription", "pay for my prescriptions", "free prescriptions",
                 "exempt", "exemption",
                 "child", "children", "baby", "toddler", "kid", "kids", "son", "daughter",
                 "year old", "years old", "months old", "dog", "cat", "pet", "puppy",
                 "overdose", "took the lot", "too many", "suicide", "kill myself", "self harm",
                 "swallowed the lot",
                 "calpol", "childrens", "children's", "junior", "nurofen for children",
                 "inhaler", "insulin", "epipen", "epi pen",
                 "how much is a prescription", "how much is the prescription",
                 "how much are prescriptions", "how much do prescriptions",
                 "what does a prescription cost", "prescription charge",
                 "prescription charges", "prescription cost", "prescription price",
                 "private prescription", "private prescriptions", "nhs prescription",
                 "prescription fee", "prescription fees", "prescriptions free",
                 "prescription free", "prepayment certificate", "prescription prepayment",
                 "cost of a prescription", "cost of prescriptions")),

    entry("medicine-in-pregnancy", (("ibuprofen", "paracetamol", "aspirin", "painkiller",
                                     "painkillers", "tablets", "medicine", "cold remedy"),
                                    ("pregnant", "pregnancy", "expecting", "breastfeeding",
                                     "breast feeding", "nursing", "while i'm expecting")),
          _medicine_when_pregnant_or_feeding,
          ask=("pregnant", "pregnancy", "expecting", "breastfeeding", "breast feeding", "nursing"),
          lead=("yesno", _the_pregnancy_verdict),
          bias=1),

    entry("nosebleed", (("nosebleed", "nose bleed", "nose bleeds", "nose is bleeding",
                         "nose keeps bleeding", "bleeding nose", "blood from my nose",
                         "bloody nose", "nose bled", "nose is bleeding", "nose bleeding",
                         "blood coming from my nose", "nose blood", "blood in my nose"),
                        ("what", "how", "stop", "should", "why", "do", "keep", "getting",
                         "got", "is", "bad", "have", "coming", "bled", "bleeding", "wont stop",
                         "won't stop", "still")),
          "Sit up, lean forward and pinch the soft part of your nose just below the bone for ten "
          "minutes without peeking, breathing through your mouth. Spit out any blood rather than "
          "swallowing it. See a GP if it lasts over 20 minutes, keeps coming back, or you are on "
          "blood thinners.",
          avoid=("dog", "cat", "puppy", "child", "toddler", "baby", "son", "daughter")),

    entry("morning-nausea",
          (("sick every morning", "sick in the mornings", "nauseous every morning",
            "nausea every morning", "queasy every morning", "sick each morning",
            "wake up feeling sick", "wake up sick", "waking up feeling sick",
            "waking up sick", "feel sick when i wake", "sick when i wake up",
            "morning nausea", "feel sick in the morning", "feel sick in a morning",
            "feel sick every morning", "felt sick every morning", "feeling sick every morning"),
           ("morning", "mornings", "wake", "waking", "every day", "each day", "why",
            "what", "how", "two weeks", "weeks", "fortnight", "month")),
          "Morning sickness that is not pregnancy is usually one of four things: an empty stomach "
          "overnight (low blood sugar makes people queasy), acid coming up when you lie flat "
          "overnight, dehydration, or a medicine taken at night. Try it in that order - a plain "
          "biscuit or a glass of water before you get up, the head of the bed raised a few inches "
          "or no food within three hours of lying down, and a glass of water before bed. Write "
          "down what you ate and drank the night before for a week; the pattern usually names it. "
          "See a GP if it has gone on more than a fortnight, if you are losing weight, if you "
          "vomit blood or have pain, or if it comes with a bad headache and blurred vision.",
          avoid=("school", "nursery", "school morning", "school mornings", "child",
                 "children", "kid", "kids", "son", "daughter", "toddler", "baby",
                 "pregnant", "pregnancy", "morning after", "dog", "cat", "puppy",
                 "motion", "car", "boat", "travel", "hangover", "drunk"),
          bias=2),

    entry("heartburn-not-the-heart",
          (("heartburn", "reflux", "indigestion", "acid", "chest burn", "chest burning", "burns",
            "burning", "burn"),
           ("heart attack", "heartattack", "my heart", "cardiac", "or a heart", "or my heart",
            "a heart", "worried", "worry", "difference", "between", "how do i know",
            "how can i tell", "chest", "chest pain", "comes and goes")),
          "Heartburn is a burning behind the breastbone that comes on after food or when you lie "
          "down, and an antacid settles it in minutes; a heart attack is a heaviness or tightness "
          "that can come on at rest, often spreads to the arm, jaw, neck or back, and comes with "
          "sweating, feeling sick or breathlessness. If the pain is new, crushing, or arrives with "
          "sweating, breathlessness or a spreading ache, treat it as the heart and ring 999 - an "
          "ambulance is the right price of being wrong.",
          avoid=("hurts", "hurting", "pain", "painful", "tight", "pressure", "crushing",
                 "burnt out", "burned out", "burning out", "burn out", "burnout",
                 "exhausted by work", "work is exhausting", "running on empty",
                 "sweating", "sweaty", "breathless", "breathlessness", "short of breath",
                 "right now", "since this morning", "left arm")),

    entry("heart-attack-signs",
          (("heart attack", "heartattack", "heart attacks", "cardiac arrest", "my heart attack"),
           ("symptoms", "symptom", "signs", "sign", "warning signs", "what are", "early signs",
            "start", "starts", "feel like", "feels like", "how do i know", "can you tell",
            "recognise", "recognize", "different from heartburn")),
          "The usual sign is chest pain or tightness, like a band round the chest, spreading to "
          "the arm, neck or jaw, with sweating, feeling sick, breathlessness or sudden "
          "exhaustion - in women, older people and people with diabetes it can be mild, or feel "
          "like indigestion. If that is happening now, ring 999 and sit still until it comes, and "
          "do not drive yourself; chew one adult aspirin if you have one and are not allergic. "
          "Someone who has stopped breathing needs CPR and a defibrillator, and the 999 call "
          "talker will guide you through both.",
          avoid=("chest pain", "i have chest", "having a heart attack", "right now", "should i",
                 "my dad", "my mum", "my husband", "my wife")),

    entry("chest-burning-after-food",
          (("chest", "chest burns", "chest burning", "behind my breastbone", "breastbone"),
           ("after eating", "after food", "after dinner", "after a meal", "after my tea",
            "when i eat", "when i lie down", "lying down", "at night", "burns", "burning")),
          "Burning in the middle of the chest that arrives after food, or when you lie down, is "
          "reflux: acid washing back up the gullet, not the heart. An antacid or an alginate "
          "(Gaviscon and the like) settles it in minutes, and a pharmacy omeprazole taken daily "
          "for a fortnight works better if it keeps coming back - smaller meals, three hours "
          "between dinner and bed and the head of the bed 10 to 15cm up do the rest. See a GP if "
          "it lasts over three weeks or food starts sticking on the way down, and ring 999 instead "
          "if the pain spreads to your arm or jaw or comes with sweating or breathlessness.",
          avoid=("hurts", "hurting", "pain", "painful", "tight", "pressure", "crushing",
                 "sweating", "breathless", "short of breath", "arm", "jaw", "baby", "child")),

    entry("toothache-dentist", (("toothache", "tooth aches", "tooth hurts", "tooth is hurting",
                         "sore tooth", "bad tooth", "gum hurts", "abscess",
                         "clove oil", "oil of cloves", "toothache remedy", "toothache remedies"),
                        ("what", "how", "take", "pain", "hurts", "hurting", "ache", "aching",
                         "help", "should", "do", "is", "got", "bad",
                         "pregnant", "pregnancy", "expecting", "trimester",
                         "remedy", "remedies", "home remedy", "good for", "work", "works",
                         "put on", "rub", "on my tooth", "on the tooth", "on my gum",
                         "for", "with", "and")),
          _toothache_help,
          avoid=("dog", "cat", "puppy", "baby", "toddler",
                 "swollen face", "face is swollen", "face has swollen", "swelling in my face",
                 "my face", "swollen cheek", "cheek is swollen", "jaw is swollen", "swollen jaw",
                 "cant swallow", "cannot swallow", "can not swallow", "trouble swallowing",
                 "difficulty swallowing", "fever", "temperature", "pus", "unwell",
                 "grease", "grease mark", "grease stain", "greasy", "stain", "stains",
                 "worktop", "worktops", "laminate", "sink", "hob", "laundry", "washing up")),

    entry("crown-came-off",
          (("crown", "crowns", "cap came off", "my cap", "veneer", "veneer came off",
            "came off my tooth", "came off a tooth", "come off my tooth"),
           ("came off", "come off", "fell off", "fallen off", "fell out", "loose", "wiggly",
            "broken", "snapped", "out")),
          "Keep the crown, rinse it and take it with you: a dentist can often cement it back on, "
          "and the tooth underneath needs looking at either way. Ring for an appointment in the "
          "next few days, today if the tooth is sore or sharp, keep it clean and chew on the other "
          "side - and do not glue it back with anything from the shed.",
          avoid=("cost", "price", "how much", "nhs", "band", "free", "pay", "dog", "cat")),
    entry("tooth-loose-adult",
          (("tooth is loose", "tooth has come loose", "tooth feels loose", "teeth are loose",
            "teeth is loose", "teeth feel loose", "teeth feel wobbly", "my teeth are moving",
            "gone loose", "has gone loose", "have gone loose", "going loose",
            "adult tooth", "one of my teeth is loose", "my front tooth is loose",
            "tooth has moved", "teeth have moved", "gap between my teeth"),
           ("is", "loose", "what", "should", "how", "do", "why", "worried", "normal", "urgent",
            "happening", "move")),
          "A tooth of your own that has come loose on its own is a dentist this week, and today "
          "if it hurts or the gum is swollen: it is usually gum disease, which is treatable, and "
          "leaving it is what loses the tooth. Do not wobble it, chew on the other side, and if it "
          "was knocked in an accident hold it by the crown, put it back in the socket or in milk "
          "and get to an urgent dentist or A&E inside the hour.",
          avoid=("milk tooth", "milk teeth", "baby tooth", "child", "children", "kid", "kids",
                 "son", "daughter", "toddler", "dog", "cat", "puppy", "kitten"),
          bias=2),
    entry("milk-tooth-loose",
          (("milk tooth", "milk teeth", "baby tooth", "baby teeth", "wobbly tooth",
            "tooth is wobbly", "tooth fell out", "tooth came out"),
           ("is", "loose", "wobbly", "fell", "came out", "normal", "ok", "okay", "should",
            "what", "how", "when", "worry", "worried", "child", "son", "daughter", "kid")),
          "A milk tooth going wobbly from about six is normal - let it come out on its own, and "
          "do not tie a string to it or pull it before it is ready. See a dentist if it stays "
          "loose for weeks with the new tooth coming up behind it, or if the gum is sore or "
          "swollen; a milk tooth knocked right out is not put back, so ring a dentist to check it. "
          "If the wobbly one is an adult tooth of your own, that is a dentist this week instead: a "
          "tooth of your own that has come loose is usually gum disease, and it is treatable.",
          avoid=("dog", "cat", "puppy", "kitten", "vet", "adult tooth", "permanent tooth",
                 "implant", "denture", "last year", "years ago", "months ago", "when i was",
                 "used to", "already gone", "hole", "socket", "bleeding", "bled", "blood",
                 "swollen gum", "gum is swollen")),

    entry("dead-tooth",
          (("tooth", "teeth", "front tooth", "my tooth", "molar", "incisor", "canine",
            "filling", "crown", "veneer", "milk tooth", "baby tooth", "tooth that"),
           ("grey", "gray", "greyed", "dark", "darker", "darkened", "black", "blackish",
            "discoloured", "discolored", "colour change", "colour has changed", "changed colour",
            "changed color", "dead", "dying", "died", "went grey", "gone grey", "going grey",
            "turned grey", "went dark", "gone dark", "turned dark", "went black", "gone black",
            "pull", "pulling", "pulled", "take it out",
            "back to normal", "go back to normal", "stay dark", "stay grey", "stay gray",
            "normal again", "the colour", "the color")),
          "A tooth that changes colour has usually lost its nerve: a knock cuts the blood supply, "
          "the tooth dies and it goes grey or dark over the next few weeks, sometimes months "
          "later. It is not an emergency on its own - get it looked at by a dentist within a week "
          "or two, and the same day if it aches, if the gum under it is swollen or sore, or if "
          "there is a little pimple on the gum, because a dead tooth can go on to abscess and "
          "that is what hurts. It will not go back to normal on its own: whitening and scrubbing "
          "will not bring the colour back. Do not pull it, even if it has gone loose - a loose "
          "tooth comes out when it is ready, and pulling one early tears the gum and can bring "
          "infection. A grey milk tooth in a child often needs nothing: the dentist will say "
          "whether to watch it or take it out, so the adult tooth underneath is not affected.",
          bias=1,
          avoid=("dog", "cat", "puppy", "kitten", "vet", "horse", "implant", "denture", "false "
                 "teeth", "hair", "grout", "washing", "paint", "sky", "mould", "mold", "tile",
                 "cost", "price", "how much", "nhs band", "whiten", "whitening", "yellow",
                 "stain", "stains", "coffee", "tea", "smoking",
                 "run in", "runs in", "run in my family", "runs in my family", "genetic",
                 "genes", "hereditary")),

    entry("weight-loss-hungry", (("lose weight", "slim down", "shed", "drop a stone",
                                  "diet", "calorie deficit"),
                                 ("without", "hungry", "hunger", "starving", "appetite", "keep",
                                  "full", "how")),
          "Fill up on protein and fibre first: eggs, beans, yoghurt, chicken, vegetables and whole "
          "grains keep you full on fewer calories. Eat slowly, drink water before meals, and aim "
          "for half a kilo a week rather than a crash diet, which is what makes hunger unbearable.",
          avoid=("baby", "toddler", "child", "cat", "dog", "puppy", "chicken the", "recipe",
                 "protein",
                 "shed", "fence", "fences", "decking", "patio", "gate", "sheds",
                 "paint", "painting", "painted", "garden shed", "shed door",
                 "shed roof", "potting shed",
                 "in the shed", "the shed", "shed wall",
                 "garage", "in the garage", "loft", "in the loft", "attic",
                 "smell", "smells", "smelly", "stink", "odour", "odor", "reek")),
    entry("energy-drink-good-or-bad",
          (("energy drink", "energy drinks", "red bull", "monster", "relentless", "lucozade",
            "pre workout", "pre-workout"),
           ("bad for me", "bad for you", "healthy", "unhealthy", "good for me", "good for you",
            "worth it", "benefits", "ok for me", "okay for me", "bad", "good", "harmful",
            "dangerous", "every day", "each day", "once a day",
            "can i", "can my", "can he", "can she", "should i", "allowed", "how old", "age")),
          "A 250ml can is about 80mg of caffeine and around 27g of sugar - a coffee's caffeine with "
          "a can of Coke's sugar on top - so it is fine occasionally and poor as a daily habit. "
          "Not after about 2pm if you want to sleep, never as a mixer with alcohol, and none at all "
          "for under-16s, in pregnancy, or with a heart condition.",
          avoid=("how much", "how many", "how often", "limit", "too much", "maximum",
                 "how many cans", "caffeine in", "mg", "mg of", "sugar in", "calories",
                 "price", "cheap", "which one", "brand", "shop", "recipe", "make my own",
                 "homemade", "machine", "coffee", "espresso", "tea", "cola", "coke")),
    entry("sports-drink",
          (("sports drink", "sports drinks", "electrolyte", "electrolytes", "electrolyte drink",
            "electrolyte drinks", "isotonic", "isotonics", "lucozade sport", "gatorade",
            "powerade", "salt tablet", "salt tablets",
            "hydration drink", "hydration drinks", "rehydration drink", "protein water",
            "electro"),
           ("need", "needs", "needed", "should i", "do i", "good for", "bad for", "better than",
            "worth", "when", "after", "during", "before", "running", "gym", "marathon",
            "football", "cycling", "swim", "swimming", "sweat", "sweating", "cramp", "hot",
            "weather", "water", "replace", "made up", "mix",
            "how much", "how many", "calories", "sugar", "carbs")),
          "A sports drink is water with sugar and salt, and it only earns its place in a long or hot "
          "session: over about an hour, or two sessions in a day, or a match in the heat. For an "
          "ordinary gym hour, a 5k or a swim, water is enough - a 500ml bottle of sports drink is "
          "about 30g of sugar, and the salt you lose is replaced by the next meal. A cheap version "
          "of the same thing is squash with a pinch of salt in a bottle of water, and a glass of "
          "milk does more for you after a hard session than most of the shelf does.",
          avoid=("diarrhoea", "diarrhea", "vomiting", "dehydration", "dioralyte", "baby",
                 "babies", "child", "children", "toddler", "kid", "kids", "pregnant",
                 "pregnancy", "caffeine",
                 "energy drink", "energy drinks", "red bull", "monster", "hangover",
                 "medicine", "doctor", "gp", "hospital",
                 "softener", "softeners", "dishwasher", "brine", "water softener")),
    entry("coffee-health", (("coffee", "caffeine", "espresso", "flat white"),
                            ("bad for me", "bad for you", "healthy", "unhealthy", "good for me",
                             "good for you", "worth it", "benefit", "benefits")),
          "Up to about four cups of coffee a day is fine for most adults, and it is linked to "
          "slightly lower risk of type 2 diabetes and liver trouble. Keep it before early "
          "afternoon, and go easy if you are pregnant (200 mg, about two cups) or get heartburn.",
          avoid=("machine", "grinder", "beans", "shop", "cafe", "order", "recipe", "sleep",
                 "bed", "night", "keep me up", "keeps me up", "cafetiere", "per cup", "mug",
                 "teaspoon", "tablespoon", "ground", "brew", "strength", "pregnant",
                 "pregnancy", "breastfeeding", "how much", "how many", "too much")),
    entry("a-drink-on-an-empty-stomach",
          (("coffee", "tea", "caffeine", "espresso", "flat white", "green tea", "matcha",
            "energy drink", "cola", "coke", "black tea", "decaf"),
           ("empty stomach", "on an empty", "before food", "before breakfast", "without food",
            "before i eat", "before eating", "first thing", "no breakfast", "before a meal")),
          "It is fine for most people: the caffeine gets into your blood at about the same speed "
          "whether you have eaten or not. What an empty stomach changes is how it feels - a bit "
          "jittery, slightly queasy, or heartburn if you are prone to it - so put a slice of "
          "toast with it, or milk in it, and that settles. If you get reflux or a sore stomach "
          "most mornings, food first is kinder. Nothing here needs a doctor unless the pain is "
          "bad or it happens every day.",
          avoid=("ibuprofen", "paracetamol", "aspirin", "naproxen", "painkiller", "painkillers",
                 "tablet", "tablets", "antibiotic", "antibiotics", "medicine", "medicines",
                 "medication", "prescription", "pill", "pills", "steroid", "steroids",
                 "stain", "stains", "machine", "grinder", "beans", "cafe", "shop", "buy",
                 "cup holder", "mug", "tablespoon", "teaspoon", "calories", "pregnant",
                 "pregnancy", "breastfeeding", "baby", "toddler", "child"),
          bias=2),
    entry("units-a-week", (("units", "alcohol", "drinking", "beer", "wine", "lager", "vodka"),
                           ("week", "too much", "limit", "safe", "recommended", "guidelines",
                            "pints", "bottles", "glasses", "daily",
                            "units a week", "how many units", "how much is too much",
                            "weekly limit", "safe limit")),
          "The UK limit is 14 units a week, spread over three or more days, with a couple of "
          "drink-free days - that is six pints of average beer or six medium glasses of wine. "
          "There is no drink-free amount that is completely safe, and regular heavy nights matter "
          "more than the weekly total.",
          ask=("units", "alcohol", "drinking", "drink", "beer", "wine", "lager", "vodka", "pints",
               "booze"),
          guard=not_a_present,
          avoid=("opened", "open", "uncorked", "keep", "keeps", "keeping", "stopped", "fridge",
                 "coffee", "coffees", "tea", "teas", "caffeine", "energy drink", "energy drinks",
                 "cola", "coke", "water", "milk", "juice", "squash", "fizzy",
                 "gone off", "off", "still ok", "still good", "last week", "vintage", "cork",
                 "pregnant", "pregnancy", "expecting", "breastfeeding", "breast feeding",
                 "nursing", "antibiotics", "tablets", "medication", "medicine", "pills",
                 "doctor", "driving", "drive", "gift", "present", "recipe", "cake", "sauce",
                 "car", "battery", "tablet", "paracetamol", "ibuprofen", "smelling", "hand gel",
                 "antibiotic", "dose", "sleep", "asleep", "bed", "night",
                 "for the weekend shop",
                 "wine glass", "wine glasses", "glassware", "cloudy", "streaky", "streaks", "carafe", "decant", "dishwasher", "wash them", "washing them", "champagne flute", "champagne flutes", "flutes", "tumblers", "spotless", "smear", "smears", "streak", "fingerprints", "polish", "polishing", "washing up liquid", "sparkle", "sparkling")),

    entry("chesty-cold", (("gone to my chest", "cold on my chest", "chesty", "chest cough",
                           "cough in my chest", "rattly", "rattling", "wheezy",
                           "moved to my chest", "spread to my chest", "in my chest now",
                           "now its in my chest", "now in my chest", "on my chest now"),
                          ("cold", "cough", "what", "help", "should", "do", "how", "gone",
                           "went", "moved", "spread", "now", "started", "hurts")),
          "A cold that has gone to the chest is usually a chesty cough that lasts one to three "
          "weeks: keep drinking, sit in a steamy bathroom, and a spoonful of honey helps a night "
          "cough. See a GP if you are breathless or wheezy, coughing up blood, have a high "
          "temperature for more than three days, or it is still there after three weeks.",
          avoid=("baby", "babies", "toddler", "child", "children", "kid", "kids",
                 "38", "39", "40", "pneumonia", "asthma attack",
                 "window", "windows", "door", "doors", "pipe", "pipes", "radiator", "car",
                 "blinds", "venetian blinds", "shutters", "shutter", "gate", "gates", "fence",
                 "fences", "chimney", "loo seat", "toilet seat", "hinge", "hinges", "squeak",
                 "squeaking", "noisy", "noise")),

    entry("tired-after-flu", (("after the flu", "after flu", "after a virus", "after covid",
                               "after coronavirus", "post viral", "post-viral"),
                              ("tired", "normal", "exhausted", "how long", "weeks", "knackered",
                               "wiped", "no energy", "recovery", "recover")),
          "Feeling wiped out for a week or two after flu is normal: build back slowly, sleep more "
          "than usual, and do not go straight back to full days. See a GP if you are still "
          "exhausted after four weeks, breathless at rest, or getting worse rather than better.",
          avoid=("vaccine", "vaccination", "jab", "shot", "booster")),

    entry("pregnancy-back", (("pregnant", "pregnancy", "weeks pregnant", "expecting a baby"),
                             ("back", "backache", "back pain", "hurts", "ache", "sore", "can i do",
                              "what can i do", "help")),
          "Back pain in later pregnancy is common: a bump pulls the pelvis forward and the "
          "ligaments soften. A support belt, a pillow between your knees at night, sitting with "
          "your hips higher than your knees and a pregnancy-safe physio class all help, and "
          "paracetamol is the painkiller that is considered safe. Ring your midwife the same day "
          "for pain under the ribs, a headache with flashing lights, swelling in the face or "
          "hands, or reduced movement.",
          ask=("pregnant", "pregnancy", "expecting", "weeks"),
          avoid=("cat", "dog", "puppy", "trying to get", "trying for", "no longer"),
          bias=1),

    entry("pregnancy-length", (("pregnancy", "pregnant", "gestation", "due date", "expecting",
                                "full term"),
                               ("how long", "how many weeks", "length", "how far along", "term",
                                "full term", "calculated", "counted", "due date", "how many months")),
          "Pregnancy is counted as 40 weeks from the first day of your last period, which is about "
          "nine months, and it is dated that way rather than from when you conceived because "
          "nobody knows that day. 'Full term' is 37 to 42 weeks, so a due date is a two-week window "
          "rather than a day, and the dating scan at around 12 weeks is what sets it if your "
          "periods are irregular.",
          ask=("how long", "how many weeks", "length", "how far along", "term", "full term",
               "calculated", "counted", "due date", "how many months"),
          avoid=("back", "backache", "pain", "ache", "sore", "sick", "sickness", "nausea",
                 "heartburn", "cramp", "cramps", "bleeding", "spotting", "headache", "rash",
                 "test", "tests", "positive", "scan", "scans", "midwife", "appointment", "food",
                 "eat", "eating", "cheese", "alcohol", "drink", "flight", "travel", "exercise",
                 "gym", "work", "maternity", "leave", "sex", "sleep", "tired", "kicks",
                 "movement", "cat", "dog", "puppy", "trying to get", "trying for", "no longer")),

    entry("five-a-day", (("5 a day", "five a day", "5-a-day", "fruit", "veg", "vegetables",
                          "portions of fruit", "servings of fruit"),
                         ("thing", "really", "actually", "true", "really a thing", "enough",
                          "how much", "mean", "mean", "should", "is", "count", "counts",
                          "vegetables", "fruit")),
          "Yes - five 80g portions of fruit and veg a day, which is about a handful each: a banana, "
          "an apple, three heaped spoons of peas, a cereal bowl of salad. Fresh, frozen, tinned and "
          "dried all count, potatoes do not, and juice or smoothies only count once a day however "
          "much you drink.",
          ask=("5 a day", "five a day", "5-a-day", "fruit", "veg", "vegetables", "portions",
               "servings"),
          avoid=("dog", "cat", "puppy", "baby", "toddler", "recipe", "dinner", "tea", "meal",
                 "cook", "shop", "cheap",
                 "frozen", "freezer", "tinned", "canned", "from a tin", "as good as",
                 "as healthy", "as nutritious", "less nutritious", "better than", "worse than",
                 "as fresh", "than fresh",
                 "dig", "digging", "dug", "spade", "fork", "sow", "sowing", "plant", "planting",
                 "patch", "plot", "allotment", "greenhouse", "compost", "manure", "weed",
                 "weeds", "weeding", "grow", "growing", "raised bed")),

    entry("back-after-gardening", (("gardening", "weeding", "digging", "lifting", "moved furniture",
                                    "moving furniture", "hoovering", "housework", "moved house",
                                    "moving house", "move house", "moving flat", "moved flat",
                                    "moving house", "sofa", "wardrobe", "boxes", "mattress"),
                                   ("back", "backache", "hurts", "sore", "ache", "aching",
                                    "killing me")),
          "Most back pain after a day of lifting or gardening settles within a couple of weeks: "
          "keep moving gently rather than resting it, take paracetamol if you need it, and avoid "
          "the heavy lifting for a few days. See a GP if you cannot weight-bear, have numbness "
          "round the groin or saddle area, or lose control of your bladder or bowels.",
          ask=("hurts", "hurt", "sore", "ache", "aching", "killing me", "kills", "pain",
               "my back went", "back went", "my back has gone", "back has gone",
               "stiff", "did my back in", "tweak", "tweaked", "put my back out",
               "done my back", "went in my back", "rest it", "keep moving"),
          avoid=("allotment", "lawn", "shed", "car", "van", "knife", "arm", "shoulder",
                 "weed killer", "spade"),
          bias=1,
          guard=_the_part_is_a_persons),

    entry(
        "lifting-something-heavy",
        (HEAVY_THING, LIFT_VERB),
        "Bend at the hips and knees, keep the load against your body and your feet hip-width "
        "apart, and take a sofa or a mattress with a second person on the other end: two people "
        "and a strap beat one person and a bad back. If your back has gone since, keep moving "
        "gently rather than resting it in bed - most strains ease in one to two weeks - and ring "
        "the doctor the same day if you cannot weight-bear, go numb round the groin or lose control "
        "of your bladder.",
        avoid=LIFT_HAS_A_CARD,
        bias=1),




    entry("run-down-colds", (("get a cold", "colds", "always ill", "always get ill", "run down",
                              "rundown", "catch everything", "keep getting colds",
                              "get ill when"),
                             ("always", "every", "when", "why", "what", "help", "stop",
                              "prevent", "avoid", "feel", "feeling", "really", "so", "a bit",
                              "constantly")),
          "Adults get two to four colds a year, and they cluster when you are short of sleep, "
          "stressed or run down - that is not a weak immune system, it is the usual pattern. Sleep "
          "seven to nine hours, eat properly, wash your hands and take vitamin D in winter; see a "
          "GP if you are getting infections that need antibiotics more than a few times a year.",
          ask=("run down", "rundown", "when i", "when im", "when i'm", "stressed", "stress",
               "tired", "short of sleep"),
          avoid=("baby", "toddler", "child", "children", "kid", "kids", "dog", "cat",
                 ) + TOOTH_OR_GUM + ("fly", "flies", "flying", "flight", "flights", "plane",
                 "planes", "airport", "aeroplane", "airplane",
                 "hands getting cold", "hands are cold", "hands get cold", "hands go cold",
                 "hands going cold", "cold hands", "hand is cold", "my hand is cold",
                 "fingers are cold", "fingers getting cold", "fingers go cold",
                 "cold fingers", "feet are cold", "feet get cold", "feet getting cold",
                 "feet go cold", "cold feet", "foot is cold", "toes are cold",
                 "toes get cold", "cold toes", "toes go cold")),

    entry("out-of-breath", (("out of breath", "breathless", "short of breath", "puffed",
                             "cant breathe", "can't breathe", "get breathless", "breathing hard")
                            + said("breathless", "puffed", "short of breath", "out of breath"),
                            ("stairs", "walking", "run", "bus", "exercise", "up the", "hill",
                             "climbing", "should", "normal", "worried", "breathless", "puffed")),
          "Being puffed after stairs or a run for the bus is usually just fitness: a brisk walk, "
          "stairs instead of the lift and two or three short bouts of getting out of breath a week "
          "make a real difference in a month or two. Breathlessness that comes on at rest, wakes "
          "you at night, or comes with chest pain, a cough for weeks or swollen ankles should be "
          "checked by a GP rather than worked through.",
          avoid=("asthma", "inhaler", "lung", "copd", "heart", "chest pain", "baby", "toddler",
                 "child", "children", "panic attack", "anxiety", "swallowed", "start running",
                 "start to run", "want to start", "getting into running", "begin running")),

    entry("work-when-ill", (("go to work", "go in tomorrow", "go into work", "go in sick",
                             "day off", "call in sick", "off work",
                             "stay home", "stay off", "back to work", "school tomorrow",
                             "go to school", "go in tomorrow"),
                            ("sore throat", "cold", "colds", "flu", "cough", "fever",
                             "temperature", "ill", "sick")),
          "If you have a fever or feel properly rough, stay home and rest: you will get better faster "
          "and you will not pass it round. With just a sore throat or a mild cold, working is fine if "
          "you feel up to it, but keep your distance and wash your hands. Stay off until 24 hours "
          "after a fever has gone.",
          avoid=("interview", "meeting", "boss", "pay", "salary", "holiday", "leave", "trip",
                 "travel", "flight", "exam", "commute", "traffic",
                 "my daughter", "my son", "my child", "my children", "my kid", "my kids",
                 "nursery", "childminder", "school", "year old"),
          bias=1),
    entry("cold-have", (("i have a cold", "ive got a cold", "i ve got a cold",
                         "i think i have a cold", "i think ive got a cold", "i caught a cold",
                         "caught a cold", "my cold", "got a cold", "this cold", "a bad cold",
                         "i have had this cold", "i have got a cold",
                         "full of cold", "full of the cold", "full of a cold",
                         "rough with a cold", "ill with a cold", "ill and cold",
                         "poorly with a cold", "poorly and cold"),
                        ("what should", "worse", "better", "started", "caught", "help", "do",
                         "rest", "last", "how long", "still", "have", "has", "got", "think",
                         "today", "now", "coming on", "feel", "feeling", "nose", "sneez",
                         "blocked", "runny")),
          "Rest, fluids and paracetamol are the treatment for a cold; it usually clears in about a "
          "week, and the cough can linger for two or three. Honey in warm water eases a cough, and "
          "see a GP if you are getting worse after a week, short of breath, or coughing up blood.",
          avoid=("weather", "outside", "freezing", "heating", "jacket", "sore", "beer", "eye",
                 "eyes", "fridge",
                 "freezer", "lager", "cider", "wine", "milk", "food", "meat", "cook", "roast",
                 "oven", "bake", "recipe", "sandwich", "sarnie", "call", "email", "text",
                 "morning", "night", "tonight", "day", "pack", "packing", "wear", "clothes",
                 "coat", "trip", "break", "forecast", "wedding", "take", "tablets", "medicine",
                 "ibuprofen", "paracetamol", "vitamin", "antibiotic", "antibiotics", "penicillin",
                 "remedy", "cure", "shift", "get rid",
                 "can i still", "can i run", "can i train", "can i exercise", "can i swim",
                 "can i go to the gym", "should i run", "should i train", "should i exercise",
                 "run with", "train with", "exercise with", "gym", "running", "swim",
                 "swimming", "football", "training",
                 "cold drink", "cold drinks", "cold water", "cold food", "cold air",
                 "flu", "or flu", "and flu", "cold or flu", "cold and flu", "is it flu",
                 "influenza",
                 )),
    entry("cough", ("cough", ("night", "dry", "chesty", "lingering", "help", "stop", "weeks",
                              "wont go", "won't go", "wont shift", "go away", "persistent",
                              "month", "months", "ages", "still", "long time",
                              "have", "got", "get rid", "bad", "cure"
                              ) + REMEDY_CUES + PLAIN_DO_ASK),
          "Try a spoonful of honey before bed, prop yourself up on an extra pillow and keep the room "
          "from getting dry; most coughs after a cold settle in two to three weeks. Blood in it, "
          "breathlessness or three weeks of it is a reason to ring the surgery or 111.",
          avoid=PETS + ("baby", "babies", "newborn", "infant", "toddler", "child", "children",
                        "kid", "kids", "year old", "months old", "my son", "my daughter",
                        "cough sweets", "cough medicine", "cough syrup", "cough drop",
                        "cough drops", "honey", "lemon", "recorder", "smoker", "smoking",
                        "vape", "vaping")),
    entry("a-baby-in-the-cold",
          (("baby", "babies", "newborn", "new born", "infant", "toddler", "pram", "buggy",
            "pushchair", "car seat", "little one"),
           ("cold", "cold out", "in the cold", "outside", "out", "walk", "walking", "fresh air",
            "winter", "freezing", "snow", "too cold", "wrap up", "layers",
            "coat", "how many layers", "how warm", "dress")),
          "Yes: a baby can go out in the cold, and the rule is one more layer than you are wearing, "
          "plus a hat, and a blanket over the pram rather than a thick coat in the car seat. Feel "
          "the chest or the back of the neck to check: warm and dry is right, hot and clammy or "
          "cold hands mean a layer is wrong. Below about -5C, or in wind and rain, keep the walk "
          "short, and bring a baby under six months in out of the cold quickly.",
          avoid=("i have a cold", "she has a cold", "he has a cold", "has a cold",
                 "had a cold", "caught a cold", "has a temperature", "poorly", "unwell", "ill",
                 "temperature", "fever", "paracetamol", "ibuprofen", "calpol", "dose", "doctor",
                 "runny nose", "cough",
                 "temperature of", "fever", "snot", "sniffles", "chesty", "chest", "croup",
                 "rash", "nappy", "feeding", "milk", "sleep", "sids", "cot death",
                 "keep", "keeps", "freeze", "defrost", "bath", "door", "window", "garden",
                 "room", "rooms", "cot", "bedroom", "nursery", "heating", "radiator",
                 "thermostat", "indoors", "sleep", "sleeping", "blanket", "blankets"),
          bias=4),
    entry("baby-fever", (("weeks old", "week old", "newborn", "new born", "just born",
                          "months old", "month old", "6 weeks", "8 weeks", "10 weeks",
                          "3 months", "2 months", "baby", "babies"),
                         ("temperature", "temp", "fever", "38", "39", "40", "hot",
                          "burning up")),
          "A baby under three months with a temperature of 38C or more is seen the same day: ring "
          "111 or your GP now rather than waiting, and don't give medicine to bring it down before "
          "they are seen. If they are drowsy, floppy, feeding badly or breathing fast, ring 999.",
          avoid=NOT_A_BABY + (
                 "wont wake", "won't wake", "not waking", "floppy", "limp", "rash", "breathing",
                 "seizure", "fit", "convulsion", "baby shower", "baby name", "cot", "pram",
                 "pushchair", "weaning", "swaddle", "sleep", "teething", "bath",
                 "room", "bedroom", "nursery", "the house", "heating", "thermostat", "how warm",
                 "what temperature should", "how hot should", "whats the best temperature")),

    entry("back-red-flags", (("cant feel my legs", "can't feel my legs", "numb legs",
                              "numb in my legs", "both legs numb", "legs went numb",
                              "legs are numb", "legs feel numb", "legs numb", "feet are numb",
                              "numb round my groin", "numbness in my groin", "numb in my groin",
                              "saddle area", "cant control my bladder", "can't control my bladder",
                              "lost control of my bladder", "wetting myself", "cant feel my bottom",
                              "cant feel when i need a wee"),
                             ("back", "legs", "leg", "groin", "bladder", "bottom", "numb",
                              "cant", "can't", "wee")),
          "Back pain with numbness around the groin or between the legs, or losing control of your "
          "bladder or bowels, needs looking at the same day: ring 111 or go to A&E, and don't wait "
          "for it to settle. The sooner it is seen the better it works out.",
          avoid=("baby", "toddler", "child", "dog", "cat", "wheelchair", "stroke")),

    entry("body-temperature",
          (("normal temperature", "normal temp", "body temperature", "temperature in celsius",
            "temperature in c", "temperature in degrees", "temperature should a body be",
            "temperature", "temp", "degrees", "a fever",
            "normal", "too high", "too low", "ok", "okay"),
           ("normal", "celsius", "degrees", "body", "37", "36", "38", "39", "what", "should",
            "is", "fever", "high", "my",
            "too low", "low", "hypothermia")),
          temperature_card,
          ask=("body", "normal", "fever", "temp", "temperature is", "my temperature", "my temp",
               "i have a temp", "is 3", "37.5", "37", "36", "38", "39", "40", "someone",
               "person", "adult", "celsius", "fahrenheit", "degrees c", "degrees f",
               "too low", "low temperature", "hypothermia", "too high", "high temperature"),
          guard=_a_body_temperature_number,
          avoid=("room", "house", "weather", "outside", "heating", "thermostat", "oven",
                 "in the oven", "fridge", "freezer", "water", "sea", "car", "engine", "cpu",
                 "laptop", "boiler", "radiator", "washing", "wash", "laundry", "clothes",
                 "cook", "meat", "chicken", "thermometer", "bring down", "confused",
                 "breathing", "unresponsive",
                 "yellow", "yellowed", "yellowing", "yellowish", "jaundice", "jaundiced",
                 "cake", "cakes", "sponge", "scone", "scones", "muffin", "muffins", "biscuit",
                 "biscuits", "brownie", "brownies", "baking", "bake", "loaf", "loaves",
                 "bread", "sourdough", "pastry", "meringue", "meringues", "cookie", "cookies",
                 "gingerbread", "traybake", "pizza", "roast", "yorkshire", "gas mark",
                 "fan oven", "oven temperature",
                 "colours", "colors", "darks", "whites", "lights", "cottons", "bedding",
                 "sheets", "duvet", "linen", "towels",
                 "baby", "child", "children", "toddler", "son", "daughter", "kid", "year old",
                 "newborn", "pregnant", "pregnancy", "dog", "cat", "puppy",
                 "kitten", "pet", "vet", "horse", "rabbit", "hamster",
                 "percent", "percentage", "percentages", "per cent", "pass my degree",
                 "pass the degree", "pass rate", "marks", "mark", "module", "modules",
                 "course", "courses", "university", "uni", "exam", "exams", "dissertation",
                 "thesis", "gcse", "gcses", "a level", "a levels", "grade", "grades",
                 "exercise", "exercising", "gym", "run", "running", "jog", "jogging",
                 "workout", "work out", "working out", "train", "training", "weights",
                 "lift", "lifting", "swim", "swimming", "cycle", "cycling")),
    entry("fever", (("fever", "temperature", "temp", "high temp"),
                    ("temperature", "high", "bring down", "child", "adult", "help", "temp",
                     "39", "38", "40", "how high", "year old", "toddler", "kid", "baby", "son",
                     "daughter", "at night", "keep it down", "keep the temperature down")),
          FEVER_ADVICE,
          avoid=("fridge", "freezer", "oven", "room", "outside", "heating", "thermostat",
                 "bath", "baths", "bathtub", "bathe", "bathing", "bath water", "bathwater",
                 "shower", "hot tub",
                 "water", "weather", "car", "engine", "climate", "sea", "cpu", "laptop",
                 "flat", "house", "home", "bedroom", "hall", "office", "gym", "shop",
                 "chickenpox", "chicken pox", "measles",
                 "wont wake", "won't wake", "not waking", "cant wake", "can't wake", "floppy",
                 "limp", "unresponsive", "blue", "rash", "breathing", "ambulance", "seizure",
                 "fit", "convulsion", "stiff neck", "confused", "non blanching",
                 "weeks old", "week old", "newborn", "new born", "just born", "days old",
                 "weeks", "week", "months", "month", "baby", "babies")),
    entry("watch-for-a-child",
          (("watch for", "watch out for", "watching out for", "look out for", "looking out for",
            "keep an eye out for", "keep an eye on", "keeping an eye on", "what to look for",
            "what should i look for", "what do i look for", "warning signs", "signs of",
            "signs that", "what signs", "signs to watch", "be alert for",
            "red flag", "red flags", "getting worse", "get worse",
            "how do i know", "call 111", "needs a doctor", "need a doctor"),
           ("child", "children", "kid", "kids", "baby", "babies", "toddler", "son", "daughter",
            "boy", "girl", "little one", "year old", "years old", "months old",
            "school age", "my lad", "my lass")),
          "Watch four things: whether they will drink, whether they are still weeing, whether "
          "they perk up between bouts, and how they are breathing. A child who is poorly but "
          "plays between bouts is usually fine. Limp or drowsy, breathing fast or grunting, a rash "
          "that will not fade under a glass, no wee for eight hours, or nothing kept down all day "
          "means 111 today, and 999 if they are hard to wake or struggling to breathe.",
          avoid=("fever", "temperature", "temp", "rash", "cough", "croup", "breathing",
                 "chickenpox", "chicken pox", "measles", "mumps", "seizure", "fit", "convulsion",
                 "sick", "sickness", "vomiting", "vomited", "diarrhoea", "diarrhea", "unwell",
                 "poorly", "ill", "not well", "ear", "earache", "throat", "tonsils", "stye",
                 "conjunctivitis", "sticky eye", "head injury", "fell", "bumped",
                 "allergic", "anaphylaxis", "asthma", "inhaler", "diabetes", "eczema",
                 "anxious", "anxiety", "panic", "panicking", "depressed", "depression",
                 "mental health", "self harm", "suicidal",
                 "nappy", "nappies", "teething", "colic", "reflux", "jabs", "vaccination",
                 "vet", "dog", "cat", "puppy", "kitten",
                 "film", "films", "movie", "movies", "tv", "telly", "show", "series",
                 "episode", "netflix", "cinema", "documentary",
                 "newborn", "new born", "just born", "days old", "weeks old"),
          ask=("what should i watch", "what do i watch", "what to watch for", "watch for signs",
               "what signs", "which signs", "what symptoms", "what are the signs",
               "warning signs", "signs of", "signs that", "what should i look",
               "what do i look", "look out for", "watch out for", "keep an eye out",
               "keep an eye on", "what to look for", "what should i be looking",
               "red flag", "how do i know if", "how do i know when", "how do i know whether",
               "when to call 111", "getting worse"),
          bias=2),
    entry("see-doctor-cold", (("doctor", "gp", "pharmacist"), ("cold", "cold's", "cough", "throat",
                                                              "flu", "sniffles", "better",
                                                              "monday", "worse")),
          "Waiting a few more days is fine, but go sooner if you're getting worse instead of "
          "better, are short of breath, or can't keep fluids down. A pharmacist can advise on "
          "coughs and colds without an appointment, and they're good at saying when a GP is needed.",
          avoid=("appointment", "appt", "cancel", "reschedul", "10am", "9am", "11am", "2pm")),
    entry("talk-to-doctor",
          (("doctor", "gp", "g.p.", "nurse", "practice nurse", "surgery", "consultation"),
           ("anxiety", "anxious", "depressed", "depression", "low mood", "mental health",
            "panic", "panicking", "panic attack", "worried", "worry", "worries",
            "embarrassed", "embarrassing", "awkward", "nervous", "ashamed", "stressed",
            "antidepressants", "antidepressant", "adhd", "autism", "eating", "drinking",
            "alcohol", "sleep", "self harm", "bring up", "bring it up", "raise", "tell them")),
          "Write three lines down before you go and read them out, or hand the phone or the "
          "note over: what is happening, how long it has been going on, and what you want out of "
          "it - a referral, tablets, a sick note, or just to be told it is normal. GPs are used "
          "to this and you will not shock them; say it in the first minute rather than the last, "
          "because it is the thing the appointment is about. Ask for a longer appointment if you "
          "need one, take someone with you if that makes it easier, and if talking is too hard "
          "you can book online and type it in the box instead.",
          bias=2,
          avoid=("cough", "cold", "flu", "appointment", "make a doctors", "book a", "cancel",
                 "reschedul", "10am", "9am", "11am", "2pm", "kill myself", "suicide",
                 "end my life", "self harm now", "overdose",
                 "while nursing", "nursing baby", "nursing my", "nursing a baby",
                 "nursing mum", "nursing mom", "still nursing", "breastfeeding",
                 "breast feeding", "breastfed", "chestfeeding", "lactating", "weaning",
                 "formula", "my baby", "feeding my baby", "feeding the baby", "my milk",
                 "milk supply")),
    entry("cold-flu-difference", (("flu", "influenza"), ("difference", "cold", "worse", "symptoms")),
          "A cold creeps up on you with a runny nose and a sore throat; flu hits fast with a fever, "
          "aching all over and real exhaustion. Flu is the one that puts you in bed for a week, and "
          "both are treated with rest and fluids at home."),
    entry("constipation", (("constipation", "constipated", "loo", "toilet", "poo", "bowel")
                           + said("constipated"),
                           ("help", "fix", "fiber", "fibre", "prunes", "week", "laxative",
                            "days", "constipated", "blocked",
                            "keep getting", "keeps coming back", "always", "constant",
                            "again and again", "stop",
                            "eat", "food", "foods", "diet", "change",
                            "rid of", "deal with", "sort out", "sorted", "relieve", "ease it",
                            "shift it", "unblock me", "how do i", "what can i do", "what helps",
                            "remedy", "remedies", "laxatives",
                            "have", "having", "had", "suffering", "suffer",
                            ) + REMEDY_CUES
                           + PLAIN_DO_ASK),
          "More fibre, more water and a short walk usually sort it: porridge, fruit, beans and "
          "wholemeal bread, plus two litres of fluid a day. If nothing has moved for a week, or "
          "there's pain or blood, get it checked.",
          avoid=("leak", "leaks", "leaking", "leaky", "drip", "drips", "dripping", "flush",
                 "flushes", "flushing", "cistern", "ballcock", "ball valve", "plunger", "unblock",
                 "unblocking", "overflow", "overflowing", "running", "runs",
                 "banging") + A_CISTERN_FAULT + A_TOILET_JOB + (
                 "blocked toilet", "toilet blocked", "toilet is blocked", "toilet keeps blocking",
                 "loo is blocked", "loo blocked", "loo keeps blocking", "bog is blocked",
                 "bog blocked", "blocked drain", "blocked drains", "blocked sink", "blocked pipe",
                 "blocked pipes",
                 "yellow skin", "skin is yellow", "gone yellow", "yellow eyes", "yellow eye",
                 "jaundice", "jaundiced", "whites of my eyes",
                 "handle", "tap", "taps", "valve", "washer", "pipe", "pipes", "plumber",
                 "repair",
                 *PETS,

                 "loo seat", "toilet seat", "seat", "seats", "banging", "bang", "bangs",
                 "rattling", "rattle", "noisy", "noise", "squeak", "squeaking", "hinge",
                 "hinges", "bumper", "bumpers", "wobble", "wobbly", "bolt", "bolts", "screw",
                 "screws", "fit a", "fitting a", "installing",
                 "clean", "cleaning", "cleaned", "wash", "washing", "scrub", "bleach", "smell",
                 "smells", "smelly", "stain", "stains", "mould", "mold", "limescale", "descale",
                 "toilet roll", "toilet paper", "toilet brush", "flushable",
                 "child", "children", "childs", "toddler", "toddlers",
                 "in a baby", "in a child", "in a toddler")),
    entry("diarrhoea", (("diarrhoea", "diarrhea", "upset stomach", "upset tummy", "upset belly",
                         "stomach bug", "tummy bug", "the runs", "the trots", "bad guts",
                         "bad belly", "dicky tummy", "dicky stomach", "dodgy tummy",
                         "dodgy stomach", "running to the loo", "running to the toilet",
                         "runs to the loo", "loose stools", "runny tummy",
                         "stools are loose", "stools are runny",
                         "stools are watery", "stools went loose",
                         "watery stools", "runny stools", "loose poo", "loose poos",
                         "poo is loose", "poos are loose", "runny poo",
                         "cant stay off the loo",
                         "stomach is off", "tummy is off", "belly is off",
                         "stomach is queasy", "tummy is queasy"),
                        ("how long", "help", "stop", "what", "rehydrate", "have", "got", "had",
                         "feel", "feeling", "been", "since", "keep", "keeps", "keeping",
                         "are", "is", "were",
                         "cant", "cannot", "with", "and",
                         "running", "rushing", "nipping", "dashing",
                         "stomach is off", "tummy is off", "belly is off",
                         "stomach is queasy", "tummy is queasy")),
          "Drink water with a little salt and sugar in it, keep eating plain food like toast and "
          "rice, and it usually settles in two to three days. See a GP if there's blood, a high "
          "fever, or it lasts more than a week, and keep away from others while it's going on.",
          avoid=("dog", "puppy", "pup", "cat", "kitten", "pet", "vet", "hamster", "rabbit",
                 "running toilet", "runs toilet",
                 "him", "he", "hes", "shes", "his", "she", "her",
                 "toddler", "toddlers", "baby", "babies", "child", "children", "kid", "kids",
                 "son", "daughter", "boy", "girl", "newborn", "wife", "husband", "mum", "dad",
                 "mother", "father", "partner", "pregnant", "pregnancy", "weeks"),
          guard=_not_a_night_of_going),
    entry("mattress", ("mattress", ("new", "replace", "back", "stiff", "old", "years",
                                    "morning", "hurts")),
          "Before you buy one, try the cheap fixes: a firm board under the mattress, rotating it, "
          "and a pillow between your knees if you sleep on your side. If it's over eight years old "
          "or you wake with back pain most mornings, a medium-firm mattress is the usual "
          "recommendation.",
          avoid=("clean", "cleaning", "wash", "stain", "mould", "mold", "smell", "hoover",
                 "buy", "buying", "cost", "price", "cheap", "spend", "decent", "which",
                 "recommend", "best",
                 "carried", "carrying", "lifted", "lifting", "hauled", "dragged", "shifted",
                 "upstairs", "downstairs", "up the stairs", "up two flights", "my back is",
                 "my back hurts", "bad back", "sore back"),
          bias=1),
    entry("eat-late",
          (("8pm", "7pm", "6pm", "9pm", "10pm", "11pm", "midnight", "late", "night", "bed",
            "bedtime", "after 8", "after 9", "after 10", "after 7",
            "eat late", "eats late", "eating late", "ate late", "late at night", "late meal",
            "meal before bed", "eat before bed", "eating before bed", "late dinner",
            "late supper", "eating at night", "eat at night", "just before bed",
            "too late to eat", "eating after", "eat after", "ate after"),
           ("eat", "eats", "eating", "ate", "dinner", "supper", "lunch", "meal", "food"),
           ("bad", "ok", "okay", "fine", "gain", "weight", "sleep", "matter", "hurt",
            "does it", "is it", "can i", "could i", "may i", "am i allowed", "affect",
            "problem", "worse", "ruin", "should i", "fat", "fatter", "fattening", "put on",
            "weigh", "unhealthy", "harm", "myth", "true", "really")),
          "The time you eat matters far less than how much you eat over the day, so a late dinner "
          "will not make you put on weight by itself - but food within two or three hours of lying "
          "down makes heartburn and a broken night more likely, and a heavy meal late can leave you "
          "waking at 3am. If late is the only time you can eat, keep it smaller and lighter: "
          "protein and vegetables rather than a takeaway and a pudding.",
          avoid=PETS + ("toddler", "baby", "child", "children", "kid", "kids", "diabetes",
                        "diabetic", "heartburn", "reflux", "indigestion", "acid",
                        "shift work", "night shift",
                        "left out", "out all night", "out of the fridge", "sit out",
                        "sitting out", "leftover", "leftovers", "gone off", "still safe",
                        "filling", "fillings", "after a filling", "after my filling",
                        "after the filling",
                        "gym", "workout", "work out", "run", "running", "training",
                        "snack", "snacks", "snacking", "cant stop", "can t stop",
                        "keep eating", "keeps eating", "binge", "binging", "bingeing",
                        "craving", "cravings", "habit", "grazing", "overeat", "overeating",
                        "exercise", "lifting", "swim", "swimming", "cycle",
                        "cycling", "football", "match", "sport", "session",
                        "go to bed", "going to bed", "get to bed", "getting to bed",
                        "wake up", "waking up", "woke up", "sleep at",
                        "vomit", "vomits", "vomited", "vomiting", "throw up", "throws up",
                        "threw up", "throwing up", "nausea", "nauseous", "nauseated",
                        "being sick", "feel sick", "feels sick", "feeling sick", "felt sick",
                        "be sick", "unwell", "diarrhoea", "diarrhea",
                        ) + TOOTH_OUT,
          ask=(("eat", "eats", "eating", "ate", "dinner", "supper", "lunch", "meal", "food"),)),

    entry("purging-and-bingeing",
          (("make myself sick", "made myself sick", "making myself sick",
            "make myself throw up", "made myself throw up", "making myself throw up",
            "make myself vomit", "made myself vomit", "making myself vomit",
            "make myself be sick", "made myself be sick", "making myself be sick",
            "made myself puke", "make myself puke",
            "purge", "purged", "purging", "binge and purge", "purge and binge",
            "purged and binged", "binged and purged",
            "binged then purged", "binge then purge",
            "bulimia", "bulimic", "eating disorder", "disordered eating",
            "anorexia", "anorexic", "starve myself", "starving myself", "not eating properly",
            "hate myself after eating", "guilty after eating", "guilt after eating",
            "cant stop bingeing", "can't stop bingeing", "keep bingeing", "keeps bingeing",
            "cant stop binging", "can't stop binging"),
           ("what", "how", "do i", "can i", "should i", "help", "stop", "why", "is it",
            "eat", "eats", "eating", "ate", "meal", "meals", "food", "after", "then", "i",
            "binge", "binges", "binged", "bingeing", "binging", "purge", "purged", "purging")),
          "That is worth taking seriously, and it is treatable - you are not stuck with it. Tell a "
          "GP: they can refer you to an NHS eating disorder service, and in the UK you can also "
          "ring Beat's helpline on 0808 801 0677 to talk it through before you decide anything. "
          "The thing that helps most at the start is one person who will not panic - a friend, a "
          "parent, a nurse - and telling them how often it happens. Try not to start with a diet "
          "or a rule about food; eating like this is usually doing a job for a feeling, and a rule "
          "gives the feeling nowhere to go. If you feel "
          "faint, your heart races, you cannot keep water down or you have not eaten for a day, "
          "treat that as urgent and get seen the same day.",
          avoid=("bug", "norovirus", "food poisoning", "migraine", "pregnant", "pregnancy",
                 "morning sickness", "chemo", "chemotherapy", "hangover", "child", "children",
                 "kid", "kids", "baby", "toddler", "dog", "cat", "left out", "gone off",
                 "still safe", "freeze", "leftovers", "reheat", "diarrhoea", "diarrhea",
                 "son", "daughter", "stepson", "stepdaughter", "my wife", "my husband",
                 "my mum", "my mother", "my dad", "my father", "friend", "flatmate",
                 "boyfriend", "girlfriend", "his", "her",
                 "radiator", "radiators", "boiler", "boilers", "pipe", "pipes", "piping",
                 "plumbing", "plumber", "heating", "central heating", "heat pump", "valve",
                 "valves", "thermostat", "sump", "engine", "coolant", "brake", "brakes",
                 "hydraulic", "airlock", "drain", "drains", "water system", "cooling system",
                 "immersion heater", "hot water", "underfloor", "flush", "flushing",
                 "email", "emails", "inbox", "mailbox", "file", "files", "data", "cache",
                 "computer", "laptop", "phone", "photo", "photos", "folder", "folders",
                 "hard drive", "facebook", "instagram", "twitter", "social media",
                 "loft", "garage", "cupboard", "wardrobe", "shed", "garden", "house",
                 "server", "spreadsheet", "contacts", "downloads", "windows"),
          bias=2),

    entry("blocked-nose-night",
          (("blocked nose", "blocked up", "stuffy nose", "nose is blocked", "nose gets blocked",
            "clear my nose", "unblock my nose", "nose feels blocked",
            "congested", "congestion", "cant breathe through my nose", "bunged up"),
           ("night", "nights", "sleep", "bed", "bedtime", "clear", "unblock", "better", "worse",
            "help", "what can i")),
          "Lie with your head on an extra pillow and keep the room cool, then rinse the nose with a "
          "saline spray or a salt-water rinse before bed - it clears the swelling rather than just "
          "the snot, and it is safe every night. A decongestant spray works for three or four days "
          "only, because after that it makes the blockage worse; steam from a hot shower helps for "
          "an hour. One side blocked for weeks, bleeding, or a lost sense of smell needs a GP.",
          avoid=PETS + ("child", "children", "kid", "kids", "baby", "toddler", "dog", "cat")),

    entry("numb-arm", (("arm", "arms"),
                       ("numb", "numbness", "goes numb", "go numb", "gone numb", "pins and needles",
                        "tingling", "tingles", "dead", "asleep",
                        "cant feel", "can't feel", "cannot feel", "no feeling",
                        "lost the feeling")),
          "A numb arm is usually a nerve being pressed or stretched: lying on it, a heavy bag on "
          "the shoulder, or tight neck and shoulder muscles. Shake it out and change position, "
          "and it should ease. If it came on suddenly, or comes with a weak hand, a drooping face "
          "or slurred speech, ring 999 now; see a GP if it keeps coming back or the arm feels weak.",
          ask=("numb", "numbness", "goes numb", "go numb", "gone numb", "pins and needles",
               "tingling", "tingles", "dead", "asleep", "feel", "feeling", "no feeling",
               "lost the feeling"),
          avoid=("bed", "night", "at night", "sleep", "sleeping", "wake", "lying", "on my side",
                 "pillow", "dog", "cat", "puppy", "baby", "toddler", "child", "leg", "legs",
                 "foot", "feet", "face", "lip", "tongue", "dentist", "anaesthetic")),

    entry("raynaud",
          (("hands", "fingers", "thumbs", "feet", "toes", "fingertips", "toetips"),
           ("numb", "numbness", "number", "goes numb", "go numb", "tingling", "tingles", "tingly",
            "pins and needles", "white", "go white", "goes white", "blue", "purple", "dead",
            "no feeling", "cold and numb")),
          "Fingers or toes that go white, then blue, then red when they warm up, or that go numb "
          "in the cold, are Raynaud's: keep the hands and feet warm, warm up slowly rather than in "
          "hot water, and see a GP this week, because it can be managed and it is sometimes linked "
          "to another condition. Numbness down one side of the body, or a hand that is weak or "
          "drops things, is 999.",
          bias=1,
          avoid=("weather", "gloves", "coat", "heating", "dog", "cat", "puppy", "baby",
                 "toddler", "chicken", "fridge", "freezer", "phone", "mouse", "wifi", "door",
                 "cow", "cows",
                 "dead on my feet", "dead on her feet", "dead on his feet", "dead on their feet",
                 "dead on our feet", "dead on your feet", "back on my feet", "back on her feet",
                 "back on his feet", "back on their feet", "off my feet", "off her feet",
                 "off his feet", "on my feet all day", "on my feet all shift", "on my feet since",
                 "find my feet", "finding my feet", "found my feet", "think on my feet",
                 "fingers crossed", "fingers crossed then", "cross my fingers",
                 "crossing my fingers", "cross your fingers", "keep my fingers crossed",
                 "land on my feet", "landed on my feet", "fall on my feet", "swept off my feet",
                 "swept me off my feet", "run off my feet", "rushed off my feet", "two left feet",
                 "get my feet under", "got my feet under", "my feet up", "feet up",
                 "sleep", "sleeping", "bed", "night", "at night", "lying", "on my side",
                 "pillow", "when i wake", "wake up")),
    entry("cold-feet",
          (("feet", "foot", "toes", "toe", "tootsies"),
           ("cold", "freezing", "freeze", "frozen", "always cold", "ice cold", "never warm",
            "warm them", "warm up", "circulation")),
          "Feet that are always cold are usually circulation: the body pulls blood in from the "
          "skin to keep your middle warm, and the feet are the far end of the line. Thick socks, shoes with a real sole and a walk every half hour help more than a "
          "hot water bottle. Always cold with tiredness or weight gain is worth a thyroid and "
          "anaemia blood test, and one cold foot is a GP question.",
          avoid=("white", "blue", "purple", "colour", "color", "colours", "colors", "numb",
                 "numbness", "tingling", "pins and needles",
                 "raynaud", "one foot", "swollen", "swelling", "burn", "fell", "cut",
                 "wound", "broken", "diabetic", "diabetes", "baby", "child", "toddler",
                 "dog", "cat", "wheel", "tyre",
                 "hands", "hand", "fingers",
                 "cold feet about", "cold feet over", "cold feet before")),
    entry("numb-hands-night-nerve", (("hand", "hands", "fingers", "finger", "thumb", "arm", "arms",
                                "wrist", "wrists"),
                               ("go numb", "goes numb", "gone numb", "numb", "numbness", "asleep",
                                "pins and needles", "tingling", "tingles")),
          "Fingers that go numb in bed are usually a nerve being pressed: carpal tunnel if it is the "
          "thumb, index and middle finger, the ulnar nerve if it is the little finger, or the weight "
          "of your body on the arm. Shake it out, keep the wrist straight, and try a wrist splint "
          "from the pharmacy at night for a couple of weeks; see a GP if it wakes you most nights or "
          "the hand is getting weak. Numbness on one whole side, or in both hands and feet, is a "
          "same-day call.",
          ask=("numb", "numbness", "asleep", "pins and needles", "tingling", "tingles", "dead",
               "wake", "night", "bed", "sleep", "go"),
          avoid=("dog", "cat", "puppy", "baby", "toddler", "child", "children", "foot", "feet",
                 "toe", "toes", "leg", "legs", "back", "face", "lip", "tongue", "phone", "mouse",
                 "keyboard", "dentist", "anaesthetic", "fill")),
    entry("numb-feet-night", (("feet", "foot", "toes", "toe", "soles", "legs", "leg"),
                              ("numb", "numbness", "goes numb", "go numb", "gone numb", "asleep",
                               "pins and needles", "tingling", "tingles", "tingle", "dead",
                               "no feeling")),
          "Feet that go numb or tingle in bed are usually a nerve being pressed by the position: "
          "crossed ankles, sitting on a foot, or a duvet tucked in tight. Change position and "
          "move the foot about, and it should come back within a few minutes. If it happens most "
          "nights, is there in the day too, or both feet are affected, see a GP for a blood test "
          "(B12, thyroid, blood sugar), because a nerve or a vitamin gap is what that pattern "
          "usually means; numbness with a new back pain, or a foot you cannot feel at all, is a "
          "same-day call.",
          ask=("night", "nights", "at night", "in the night", "bed", "in bed", "sleep",
               "sleeping", "asleep", "wake", "wakes", "woke", "waking", "when i wake",
               "most nights", "every night", "overnight"),
          bias=2,
          avoid=("swollen", "swelling", "swells", "puffy", "puffiness", "fluid", "ankle",
                 "ankles", "oedema", "white", "blue", "purple", "raynaud", "cold", "freezing",
                 "frozen", "burn", "burnt", "cut", "wound", "broken", "fell", "diabetic",
                 "diabetes", "cramp", "cramps", "charley horse", "child", "baby", "toddler",
                 "kid", "dog", "cat", "puppy", "hand", "hands", "finger", "fingers", "arm",
                 "arms", "groin", "bladder", "bowels", "cannot walk", "can't walk")),
    entry("sunburn", ("sunburn", ("treat", "help", "red", "sting", "blister")),
          "Get out of the sun, cool the skin with a shower or damp towel, and drink water; "
          "after-sun or plain moisturiser helps the sting. Don't pop blisters, and keep it covered "
          "until it heals."),
    entry("hayfever-summer", (("summer", "sun", "heat"), ("headache", "tired", "dizzy", "water")),
          "Heat and sun take it out of you: drink before you're thirsty, stay out of the midday "
          "sun, and eat something salty if you've been sweating. Feeling dizzy or confused in heat "
          "is a sign to get cool and drink, not to push on.",
          ask=("headache", "headaches", "migraine", "migraines", "tired", "tiredness", "dizzy",
               "dizziness", "faint", "fainting", "light headed", "lightheaded", "thirsty",
               "dehydrated", "nausea", "nauseous", "sick", "sunstroke", "sunburn", "burning"),
          avoid=("boiler", "boilers", "radiator", "radiators", "hot water", "central heating",
                 "thermostat", "immersion", "heating engineer", "not heating",
                 "heating the water", "heating the radiators", "heating is")),

    entry("uti", (("uti", "utis", "cystitis", "urine", "urine infection", "urinary tract infection",
                   "bladder infection", "water infection", "wee", "pee", "peeing", "weeing",
                   "loo", "loos"),
                  ("burn", "burning", "sting", "stinging", "frequent", "all the time", "infection",
                   "hurts", "smell", "blood", "think i", "ive got", "i have", "maybe",
                   "keep needing", "needing", "all day", "lots", "constantly",
                   "blood in my pee", "blood in my urine", "blood in my wee",
                   "blood in your pee", "blood when i pee", "blood when i wee",
                   "blood in the urine")),
          "Drink plenty of water, take paracetamol for the sting, and see a GP or pharmacist "
          "promptly: a short course of antibiotics clears most of these. Go the same day if you "
          "have a fever, back or side pain, blood in your pee, are pregnant, are a man, or it is a "
          "child - those need looking at rather than waiting.",
          avoid=("baby", "nappy", "cat", "dog", "puppy", "toilet training", "wee hours",
                 "night", "nights", "bedtime", "during the night",
                 "wake up", "wakes up", "waking up", "woke up", "woken up", "wake at night",
                 "in the night", "at night", "get up in the night",
                 "cistern", "flush", "flushes", "flushing", "running", "runs", "blocked",
                 "blockage", "leak", "leaks", "leaking", "plumbing", "tap", "drain",
                 "nothing comes out", "nothing came out", "wont come out", "won't come out",
                 "cant pee", "can't pee", "cannot pee", "cant wee", "can't wee", "cannot wee",
                 "unable to pee", "unable to wee", "not peeing")),
    entry("urine-frequent",
          (("loo", "loos", "wee", "weeing", "pee", "peeing", "toilet", "bathroom", "bladder",
            "urine", "urinating"),
           ("all the time", "constantly", "keep needing", "needing", "need", "going often",
            "frequent", "frequently", "often", "lots", "all day", "every hour", "every few")),
          "Going often is worth a check rather than a guess: drink water through the day and cut "
          "tea, coffee and alcohol for a week to see if it settles. If it carries on, or you are "
          "thirsty all the time and passing a lot, see a GP for a blood sugar and urine test, and "
          "go the same day if there is blood, a fever or a pain in your back or side.",
          avoid=("cistern", "flush", "flushes", "flushing", "running", "runs", "blocked",
                 "blockage", "leak", "leaks", "leaking", "plumbing", "tap", "drain",
                 "toilet roll", "toilet seat", "toilet paper", "toilet brush",
                 "filling", "fills", "refilling", "topping up", "overflowing", "trickling",
                 ) + A_CISTERN_FAULT + A_TOILET_JOB + (
                 "night", "nights", "nighttime", "bedtime", "in the night", "at night",
                 "wake up", "wakes up", "waking up", "woke up", "woken up",
                 "baby", "nappy", "toddler", "child", "cat", "dog", "puppy",
                 "sting", "stings", "stinging", "burns", "burning", "hurts", "pain", "painful",
                 "smell", "smelly", "blood", "cystitis", "uti",
                 "nothing comes out", "wont come out", "cant pee", "can't pee", "cannot pee",
                 "cant wee", "can't wee", "cannot wee", "unable to pee", "unable to wee",
                 "tile", "tiles", "tiling", "grout", "regrout", "wallpaper", "paint",
                 "suite", "shower screen", "extractor"),
          bias=2),
    entry("bladder-retention", (("pee", "peeing", "wee", "weeing", "urine", "bladder", "toilet"),
                                ("cant", "can't", "cannot", "unable", "nothing", "wont", "won't",
                                 "not coming", "not going", "comes out", "come out", "stops",
                                 "straining", "dribble", "dribbling")),
          "If you cannot pass urine at all and your bladder is full and painful, that needs looking "
          "at the same day: ring 111 or go to A&E, because waiting makes it worse and it can back up "
          "into the kidneys. If it is a weak dribble rather than nothing, drink water through the "
          "day and get a GP appointment, and go the same day if there is a fever or blood.",
          avoid=("cat", "cats", "dog", "dogs", "puppy", "kitten", "baby", "toddler", "child",
                 "children", "son", "daughter", "nappy", "toilet training", "night", "nights",
                 "bedtime", "in the night", "at night", "bathroom", "mirror", "sink", "pan",
                 "pot", "kettle", "fridge", "pregnant", "pregnancy",
                 "running", "runs", "cistern", "flush", "flushes", "flushing", "leaking",
                 "leaks", "dripping", "drips", "fill valve", "ballcock", "blocked", "overflow",
                 "seat", "lid", "bowl", "drain", "smell", "clean", "cleaning", "limescale",
                 "stain", "stains", "water bill",
                 ) + A_CISTERN_FAULT + A_TOILET_JOB + (
                 "back", "backs", "numb", "numbness", "pins and needles", "legs", "groin")),
    entry("sprain", (("sprain", "sprained", "twisted", "rolled", "turned over"),
                     ("ankle", "wrist", "knee", "heal", "long", "swollen", "swelling", "better",
                      "how long", "rest", "yesterday")),
          "Rest it, ice it for 15 to 20 minutes every few hours for the first two days, wrap it "
          "firmly and keep it up when you sit, then start gentle movement as the pain allows. A "
          "simple sprain settles in one to three weeks. If you cannot put weight on it, it is very "
          "swollen or the pain is over a bone, get it looked at the same day.",
          avoid=("bike", "chain", "garden", "hose", "control", "programme", "engine"),
          bias=1),
    entry("cast-care",
          (("cast", "casts", "plaster cast", "in plaster", "in plaster cast", "back slab",
            "splint", "in a splint", "in splint", "arm in a splint", "wrist in a splint",
            "fiberglass", "fibreglass"),
           ("itch", "itches", "itching", "itchy", "wet", "shower", "showers", "bath", "washing",
            "smell", "smells", "smelly", "loose", "rubbing", "rubs", "tight", "too tight",
            "squeezing", "pinching", "sore", "pain", "hurts", "swollen",
            "swelling", "numb", "tingling", "look after", "care", "keep", "clean", "sleep",
            "sleeping", "sweat", "sweaty", "dirty", "crack", "cracked", "crumbly",
            "write on", "sign",
            "what can i do", "what should i do", "what to do", "advice", "help")),
          "Keep it dry, keep it on and keep it up: a bin bag taped over the top - or a proper cast "
          "cover - gets you in the shower, a bag of frozen peas over a tea towel on and off for the "
          "first couple of days does the swelling, and wiggling the fingers or toes a few times an "
          "hour keeps them working. The itch is the worst part and the answer is not a knitting "
          "needle, a pen or talcum powder down the top: blow cool air down it, tap the outside, or "
          "ask the plaster room. Ring the fracture clinic the same day if the fingers or toes go "
          "white, blue or cold, tingle, or will not move, if the cast is rubbing a sore spot, or if "
          "it splits, cracks or gets soggy - a wet or loose cast is redone, so do not pad it out "
          "yourself. A musty smell with pain is a phone call too.",
          avoid=("wall", "walls", "ceiling", "ceilings", "filler", "polyfilla", "skim",
                 "cast iron", "cast-iron", "skillet", "griddle", "pan", "pans", "frying pan", "wok",
                 "cut", "cuts", "graze", "blister", "wound", "verruca", "corn",
                 "actors", "acting", "play", "audition", "is it broken", "do i need an x-ray",
                 "x-ray", "a&e", "walk on it", "sprain", "sprained", "fish", "mould", "damp"),
          bias=1),
    entry("pulled-muscle",
          (("pulled muscle", "pulled a muscle", "pulled my muscle", "muscle strain",
            "strained muscle", "strained my", "tweaked a muscle", "tore a muscle",
            "torn muscle", "muscle tear", "muscle pull"),
           ("what should", "what can", "what do", "how do", "do about", "help", "better",
            "long", "now", "hurt", "hurts", "hurting", "sore", "pain", "painful", "recover",
            "recovery", "treat", "treating", "heal", "healing", "rid", "shift", "sort")),
          "Most pulled muscles settle in two to three weeks: rest it from the movement that hurt, "
          "ice it for 15 minutes every few hours for the first two days, then keep it gently "
          "moving, because gentle movement after 48 hours heals faster than total rest. "
          "Paracetamol or ibuprofen helps, and ease back into exercise rather than stopping. See "
          "a GP if you heard a pop, cannot put weight on it, or it is no better after a week.",
          ask=("muscle", "muscles", "strain", "strained", "pulled", "pull", "tweaked", "tweak",
               "tore", "torn", "tear"),
          explain=True,
          avoid=("back", "lower back", "spine", "sciatica", "groin", "hernia", "calf", "calves",
                 "clot", "swollen", "chest", "heart", "arm numb", "numb", "tingling",
                 "car", "engine", "wire", "cable", "rope", "chain", "sieve", "colander",
                 "tea", "coffee", "wine", "filter", "strained vegetables", "strained potatoes"),
          bias=1),
    entry("first-aid-injury",
          (("injury", "injuries", "injured", "hurt myself", "hurt me", "done myself",
            "done myself in", "done my in", "did my in", "strain", "strained", "sprain",
            "sprained", "twisted", "knock", "banged myself", "got hurt"),
           ("what should", "what do", "what can", "how do", "how to", "look after", "first aid",
            "treat", "treatment", "care", "help", "advice", "deal with", "do about", "sort",
            "now", "today", "yesterday", "this morning", "recover", "recovery",
            "playing", "at the gym", "in the gym", "running", "football", "rugby", "netball",
            "hockey", "cricket", "match", "training", "sport", "sports")),
          "For a fresh knock, sprain or strain, the first two days do most of the work: rest it "
          "from the movement that hurt, ice it for 15 to 20 minutes every few hours with a cloth "
          "between the pack and the skin, wrap it firmly and keep it up when you sit. After 48 "
          "hours gentle movement beats total rest, and paracetamol or ibuprofen eases the pain. "
          "Go to A&E the same day if you cannot put weight on it, a joint looks crooked, or the "
          "skin past the injury goes numb, white or cold; see a GP or a physio if it is no better "
          "after a week, if it gives way, or if the swelling keeps coming back.",
          avoid=("ankle", "ankles", "knee", "knees", "shoulder", "shoulders", "back", "backs",
                 "wrist", "wrists", "elbow", "elbows", "hip", "hips", "hamstring", "hamstrings",
                 "calf", "calves", "thigh", "thighs", "shin", "shins", "groin", "achilles",
                 "neck", "head", "eye", "eyes", "tooth", "teeth", "finger", "fingers", "thumb",
                 "toe", "toes", "foot", "feet", "hand", "hands", "arm", "arms", "leg", "legs",
                 "chest", "tummy",
                 "car", "engine", "wire", "cable", "rope", "chain", "sieve", "colander",
                 "tea", "coffee", "wine", "filter", "strained vegetables", "strained potatoes",
                 "saucepan", "netting", "fence",
                 "my son", "my daughter", "my child", "my kid", "my baby", "my husband",
                 "my wife", "my partner", "my mum", "my mom", "my dad", "my dog", "my cat",
                 "my puppy", "the dog", "the cat", "horse",
                 "compensation", "claim", "insurance", "sick note", "sick pay", "workplace",
                 "accident at work", "boss", "hr",
                 "prevent", "prevention", "avoid", "stop it happening", "warm up",
                 "start running again", "back to running", "back to the gym", "how often",
                 "start running", "start jogging", "start exercising", "running after",
                 "running again", "get back into", "getting back into", "return to running",
                 "return to exercise", "comeback", "back into training",
                 "how do i not", "how not to", "not get injured", "not get hurt",
                 "stop getting injured", "stop getting hurt", "stop injuring",
                 "keep getting injured", "keep getting hurt", "how do i stop getting",
                 "without getting hurt", "without getting injured", "dont want to get injured")),
    entry("mouth-ulcers-rinse", (("ulcer", "ulcers"), ("mouth", "mouths", "tongue", "gum", "gums",
                                                 "lip", "inside", "recurring")),
          "Most mouth ulcers heal in a week to ten days: rinse with warm salty water, avoid spicy "
          "and acidic food, and a pharmacy can give you a protective gel or a chlorhexidine "
          "mouthwash. Anything still there after three weeks, or ulcers that keep coming back, "
          "should be shown to a dentist or GP.",
          avoid=("stomach", "leg", "legs", "foot", "feet", "varicose", "pressure", "peptic")),
    entry("hair-loss-telogen",
          (("hair", "head", "scalp", "bald"),
           ("falling out", "falls out", "fall out", "thinning", "thinning out", "bald",
            "bald patch", "bald patches", "patch", "patches", "shedding", "coming out", "receding",
            "losing my hair", "loss")),
          "Hair that comes out in handfuls for a few months is usually telogen effluvium: an "
          "illness, a stressful few months, a crash diet or having a baby pushes hair into its "
          "resting phase, and it grows back once the cause passes - iron and thyroid tests are "
          "worth asking for. A smooth round bald patch (alopecia areata) or a scalp that is "
          "scaly, itchy or sore is a GP appointment, and so is hair loss with no obvious trigger.",
          avoid=(
                 "rabbit", "rabbits", "bunny", "bunnies", "guinea pig", "guinea pigs", "hamster",
                 "hamsters", "gerbil", "gerbils", "budgie", "budgies", "budgerigar",
                 "cockatiel", "canary", "canaries", "chinchilla", "ferret", "degu",
                 "tortoise", "horse", "pony", "rat", "rats", "mouse", "mice", "mites",
                 "mange", "dog", "cat", "pet", "brush", "comb", "shampoo brand", "haircut", "fringe",
                 "style", "curly", "greasy", "dandruff only", "pubic", "legs",
                 "grey", "gray", "white", "colour", "color")),
    entry("nail-ridges",
          (("nails", "nail", "fingernails", "toenails", "thumb nail"),
           ("ridged", "ridges", "lines", "grooves", "bumpy", "dents", "pitted", "pits", "spoon",
            "curved", "streak", "split", "splitting", "flaking")),
          "Ridges that run up and down the nail are normal and get more common with age - they are "
          "the nail equivalent of a wrinkle and need nothing. Lines that run across the nail after "
          "an illness, nails that curve up like a spoon, or pitting like a thimble are worth a GP "
          "or pharmacist look, because they can point at iron or thyroid, and a dark streak that "
          "does not grow out is seen within two weeks.",
          avoid=("paint", "varnish", "polish", "gel", "acrylic", "fake", "dog", "cat", "hammer",
                 "snapped", "broke", "filing"),
          guard=_the_nail_is_a_persons),
    entry("throat-lump",
          (("throat",),
           ("something stuck", "something is stuck", "feels like something", "feels stuck",
            "there is a lump", "feels like there is a lump",
            "feels like a lump", "stuck", "lump in my throat", "lump in the throat", "globus", "tight",
            "closed", "swallowing", "swallow", "frog in my throat", "tickle",
            "feels like there is", "feels like there is a lump", "lump in it", "feels like")),
          "A lump feeling in the throat with nothing there is usually globus, and it is common with "
          "reflux, dry air and tension - symptoms that ease when you swallow food, water, or when "
          "you stop noticing it, are the reassuring kind. See a GP if it hurts, comes with food "
          "sticking, weight loss, a hoarse voice or a neck lump, or if it has not settled in three "
          "weeks, because a camera check of the throat is the way to be sure.",
          avoid=("sore", "scratchy", "cold", "flu", "tonsil", "strep", "dog", "cat", "toilet",
                 "seat", "car", "brake",
                 "closing", "closing up", "swelling", "swollen", "cant swallow", "can't swallow",
                 "cannot swallow", "bee", "wasp", "peanut", "nuts", "shellfish")),
    entry("swollen-gland",
          (("gland", "glands", "swollen gland", "swollen glands", "lump in my neck",
            "lymph node", "lymph nodes", "node", "nodes"),
           ("throat", "neck", "under my jaw", "jaw", "behind my ear", "armpit", "groin",
            "is up", "up", "came up", "come up", "swollen", "sore", "tender", "hurts",
            "painful", "how long", "weeks", "worried", "should i", "normal", "big", "hard",
            "go down", "going down", "settle", "one side", "both sides")),
          "A gland that comes up with a cold, a sore throat or a skin infection is doing its job, "
          "and it usually goes back down over two to three weeks. See a GP if it is hard or fixed "
          "in place, bigger than about two centimetres, still up after four weeks, or comes with "
          "night sweats, weight loss or a fever that will not settle.",
          avoid=("thyroid", "overactive", "underactive", "salivary", "parotid", "breast", "testicle",
                 "dog", "cat", "puppy", "kitten", "horse", "vet", "swollen neck",
                 "neck is swollen", "swelling in my neck", "swollen face", "mumps",
                 "found a lump", "i found", "noticed a lump", "there is a lump"),
          bias=2),

    entry("asthma-cold",
          (("asthma", "inhaler", "wheeze", "wheezing", "chest tightness"),
           ("cold", "winter", "frost", "freezing", "cold air", "cold weather", "worse in the cold",
            "out in the cold", "running in the cold")),
          "Cold, dry air narrows the airways, so most people with asthma cough and wheeze more in "
          "winter: breathe through a scarf over your nose and mouth for the first few minutes, warm "
          "up slowly, and take the blue inhaler ten minutes before cold exercise if your nurse "
          "advised it. Keep the preventer going every day, get the flu jab, and see your asthma "
          "nurse if you need the blue inhaler more than three times a week - that is the sign it is "
          "not controlled.",
          avoid=("cant breathe", "can't breathe", "cannot breathe", "struggling to breathe",
                 "attack", "999", "ambulance", "blue lips", "collapsed", "not responding",
                 "nebuliser", "a&e")),
    entry("lump-on-a-leg",
          (("shin", "shins", "shinbone", "thigh", "thighs", "calf", "calves", "leg", "legs",
            "knee", "knees", "ankle", "ankles", "heel", "heels", "hamstring", "hamstrings",
            "lower leg", "back of my leg",
            "arm", "arms", "forearm", "forearms", "elbow", "elbows", "upper arm", "shoulder",
            "shoulders"),
           ("lump", "lumps", "bump", "bumps", "ball", "a pea", "pea sized", "hard lump",
            "soft lump", "small lump", "under the skin", "found a lump", "noticed a lump",
            "got a lump", "have a lump", "has a lump", "lump came up", "lump come up",
            "lump has come up", "lumpy bump")),
          "A lump on an arm or a leg is usually nothing: a knock leaves a bruise under the skin "
          "that takes two or three weeks to go, so carry on using it as normal and ice it for the "
          "first day rather than rubbing it. Without a knock, a soft one that moves and is a bit "
          "tender is usually harmless, and a hard one that does not move, is growing, or is still "
          "there after two weeks needs a GP - the same rule as a lump anywhere else.",
          avoid=("dog", "cat", "puppy", "kitten", "horse", "vet", "sofa", "chair", "table",
                 "bed", "blanket", "tights", "sock", "socks", "boot", "shoe", "shoes",
                 "breast", "testicle", "gland", "glands", "armpit", "groin", "neck",
                 "varicose", "cramp", "cramps", "restless", "water retention", "both legs",
                 "swollen ankles", "swollen legs", "hot and swollen", "red and swollen",
                 "pregnant", "period", "spaniel", "labrador",
                 "wrist", "wrist", "hand", "hands", "finger", "fingers",
                 "bite", "bitten", "sting", "stung", "wasps", "bees", "tick",
                 "under my arm", "under the arm", "underarm", "under my arms", "armpit", "armpits"),
          bias=2),
    entry("wrist-lump",
          (("wrist", "wrist", "hand", "hands", "finger", "fingers", "top of my hand",
            "arm", "arms", "forearm", "elbow", "shoulder"),
           ("lump", "lumps", "bump", "bumps", "swelling", "swollen", "ball", "pea", "bony",
            "hard", "get it checked", "checked", "check", "worried", "what is it")),
          "A smooth lump on the back of the wrist that comes and goes is usually a ganglion cyst: "
          "harmless, often smaller after a few weeks, and worth a GP look only if it is painful, "
          "growing fast or stops you using the hand - they can drain it, but a lot come back. A "
          "hard, fixed lump, or one anywhere else, gets checked by a GP within a couple of weeks.",
          avoid=("breast", "testicle", "testicles", "neck", "armpit", "groin", "throat", "knee",
                 "see a doctor", "see the doctor", "see a gp", "see my gp", "see someone",
                 "toe", "toes", "stomach", "belly", "gum", "gums", "dog", "cat",
                 "bruise", "bruised", "banged", "bump into", "hit it", "after a fall",
                 "sprain", "sprained", "twisted", "swelling after",
                 "sting", "stings", "stung", "bee", "bees", "wasp", "wasps", "hornet",
                 "insect", "insects", "nettle", "nettles", "ant", "ants", "mosquito",
                 "mosquitos", "mosquitoes", "horsefly", "tick", "midge", "gnat",
                 "shine", "shines", "shiny", "sheen", "gleam", "glow", "glowing", "greasy",
                 "hard shoulder", "shoulder of the road", "motorway", "carriageway",
                 "dual carriageway", "verge", "lay-by", "layby", "breakdown", "traffic",
                 "road", "tyre", "tyres", "glass", "windscreen")),
    entry("ankle-giving-way",
          (("ankle", "ankles"),
           ("giving way", "gives way", "gives out", "given way", "wobble", "wobbly", "roll",
            "rolls", "rolling", "twist", "twisted", "sprain", "sprained", "unstable", "weak",
            "keeps going")),
          "An ankle that keeps rolling or giving way has usually left the ligaments loose after an "
          "old sprain, and the fix is strength and balance work rather than a support: stand on one "
          "leg with your eyes shut for a minute a day, do heel raises, and a physio can set you a "
          "short programme. Get it looked at if it swells up after each turn, locks, or you cannot "
          "put weight on it now.",
          avoid=("dog", "cat", "horse", "puppy", "kitten", "car", "bike", "shoe", "boot",
                 "sock", "tights")),
    entry("shaky-hands",
          (("shaking", "shaky", "shake", "shakes", "shivered", "shivering", "trembling",
            "tremble", "trembles", "tremor", "cant stop shaking",
            "can't stop shaking", "keep shaking", "keeps shaking", "feel shaky",
            "wobble", "wobbles", "wobbling", "wobbly", "jittery"),
           ("hands", "hand", "fingers", "arms",
            "shake", "shakes", "shaking", "shaky", "tremble", "trembling", "tremor", "wobble",
            "shiver", "shivered", "shiverin", "shivers", "stop", "cant stop", "can't stop",
            "all over", "whole body", "everywhere",
            "feel", "feeling", "why", "tremors", "have", "has", "got", "started", "suddenly",
            "constant", "constantly", "worse", "worry", "worried", "normal", "serious")),
          shaky_hands_help,
          ask=("shake", "shakes", "shaking", "shaky", "shook", "tremble", "trembles",
               "trembling", "tremor", "tremors", "shiver", "shivers", "shivered", "shivering",
               "shivery", "wobble", "wobbly", "jittery", "jumpy", "vibrating"),
          avoid=("cold", "freezing", "numb", "voice", "nervous", "anxious about", "job interview",
                 "speech", "presentation", "coffee cup is",
                 "dog", "dogs", "puppy", "pup", "cat", "cats", "kitten", "rabbit", "hamster",
                 "horse", "pony", "bird", "parrot", "pet", "pets", "vet",
                 "baby", "babies", "newborn", "toddler", "my son", "my daughter", "my child",
                 "my kid", "seizure", "fit", "convulsion", "epilep",
                 "phone", "car", "steering", "washing machine", "machine", "train", "bus",
                 "lift", "camera", "picture", "video", "cake", "jelly", "tin", "handlebars",
                 "chair", "chairs", "table", "tables", "desk", "stool", "stools", "bench",
                 "sofa", "settee", "wardrobe", "shelf", "shelves", "the fan", "tower fan",
                 "ceiling fan", "desk fan", "pedestal fan", "floor fan", "appliance",
                 "sick", "sickness", "nauseous", "vomit", "vomiting", "throw up",
                 "weak", "weakness",
                 "chest", "heart", "palpitation", "palpitations",
                 "handshake", "shake hands", "shaking hands with")),
    entry("white-patches-mouth",
          (("tongue", "mouth", "gums", "cheek", "throat"),
           ("white patches", "white patch", "white spots", "white coating", "white on my",
            "coated", "patches", "white", "white stuff", "white film", "white furry",
            "looks white", "white tongue", "furred")),
          "White patches in the mouth are usually thrush if they rub off and leave red skin "
          "underneath, or a bit of lichen planus if they sit inside the cheeks in a lace-like "
          "pattern; both are common, and a pharmacist can sell an antifungal gel for thrush. "
          "Anything that does not rub off, bleeds, or is still there after three weeks is a dentist "
          "or GP appointment, because a persistent patch is looked at properly.",
          avoid=("tooth", "teeth", "denture", "braces", "tonsil stone", "thrush is", "baby",
                 "toddler", "child", "wine", "beer", "taste", "tastes", "tasting", "coffee",
                 "food", "drink", "vomit", "sick",
                 "gum", "gums", "abscess", "dentist", "ulcer", "ulcers")),
    entry("biting-cheek",
          (("cheek", "cheeks", "inside of my mouth", "lip", "lips", "tongue"),
           ("bite", "biting", "chew", "chewing", "keep biting", "sore", "ulcer")),
          "Biting the same cheek or tongue is nearly always a habit that shows up when you are tense or "
          "eating fast: slow down at meals, keep the tongue away from the teeth line, and chew gum "
          "when you notice yourself doing it. If it happens in your sleep, a dentist can fit a "
          "soft guard, and a bite that has changed or a rough tooth or filling is worth checking, "
          "because a sharp edge keeps catching the same spot.",
          avoid=("dog", "cat", "puppy", "kitten", "horse", "rabbit", "hamster",
                 "tongue twister", "mouth ulcer")),
    entry("verruca", (("verruca", "verrucas", "verrucae", "wart", "warts", "plantar"),
                      ("foot", "feet", "hand", "hands", "finger", "fingers", "thumb", "knee",
                       "get rid", "help", "treat", "remove",
                       "gone", "spread", "do about", "what do i do", "what should i do",
                       "how do i", "have one", "got one", "advice")),
          "Verrucas and warts usually go on their own within a year or two; a pharmacy salicylic "
          "acid paint or patch speeds that up if you file the hard skin first. Don't pick or cut "
          "them, cover them at the pool, and see a GP or podiatrist if one is painful, bleeding or "
          "spreading quickly.",
          avoid=("plant", "plants", "toad", "fairy", "fasciitis", "plantar fasciitis")),
    entry("tonsillitis", (("tonsillitis", "tonsils", "quinsy"),
                          ("keep", "keeps", "getting", "how", "help", "treat", "long", "sore",
                           "swallow")),
          "Most tonsillitis is viral and settles in a week: paracetamol or ibuprofen, plenty to "
          "drink, and soft food. Ring 111 the same day if you cannot swallow your own spit, your "
          "voice goes muffled or one side swells up, and see a GP if it keeps coming back, because "
          "repeated bouts are worth talking through.",
          avoid=("cold", "colds", "flu", "cough"),
          report=True),

    entry("painkillers-together", (("paracetamol", "ibuprofen", "painkiller", "painkillers",
                                    "co-codamol"),
                                   ("together", "same time", "both", "at once", "mix", "alongside",
                                    "and", "ok together", "safe together", "ok to take both",
                                    "both at once", "can i take both", "can i take them together")),
          "Yes: they work in different ways, so paracetamol and ibuprofen can be taken together, "
          "spaced through the day at the dose on the packet. Skip ibuprofen if you have a stomach "
          "ulcer, kidney trouble or are on blood thinners, and ask a pharmacist if you take anything "
          "regularly.",
          ask=("together", "same time", "both", "at once", "mix", "alongside", "and",
               "both at once", "can i take both", "can i take them together"),
          avoid=("overdose", "too many", "took a load", "handful", "suicide", "kill myself",
                 "self harm",
                 "antibiotic", "antibiotics", "pregnant", "pregnancy", "breastfeeding",
                 "empty stomach", "before or after food", "with food", "without food",
                 "with a meal", "before food", "after food", "eat with", "eat before",
                 "need to eat", "have to eat")),
    entry("medicine-with-food",
          (("ibuprofen", "nurofen", "paracetamol", "aspirin", "naproxen", "diclofenac",
            "co-codamol", "antibiotic", "antibiotics", "steroid", "steroids",
            "anti inflammatory", "anti-inflammatories", "painkiller tablet", "painkiller tablets",
            "my tablet", "my tablets", "the tablet", "a tablet", "my medicine", "my medicines",
            "my medication", "my meds", "this medicine", "these tablets"),
           ("empty stomach", "on an empty stomach", "before food", "after food", "with food",
            "with a meal", "before or after food", "with or without food", "full stomach",
            "without food", "without eating", "before a meal", "after a meal", "with my food",
            "with my meal", "every day", "all the time", "long term", "long-term",
            "bad for my stomach", "bad for the stomach", "upset my stomach", "stomach hurts",
            "stomach pain", "sore stomach", "hurt my stomach", "stomach ache",
            "eat with", "eat before", "before eating", "need to eat", "have to eat",
            "eat something", "something to eat")),
          _medicine_with_food,
          ask=("empty stomach", "stomach", "food", "meal", "eat", "eating", "before", "after",
               "full", "every day", "daily", "long term", "long-term", "antibiotic",
               "antibiotics"),
          avoid=("vitamin", "vitamins", "supplement", "supplements", "multivitamin", "iron",
                 "pregnant", "pregnancy", "breastfeeding", "baby", "child", "children",
                 "toddler", "dog", "cat", "pet", "overdose", "too many", "took a load")),

    entry("sore-limbs", (("leg", "legs", "calf", "calves", "limb", "limbs", "whole body",
                          "all over", "muscles", "everywhere", "everything"),
                         ("ache", "aches", "aching", "sore", "soreness", "stiff", "pain",
                          "paining", "hurts", "killing", "kills", "hurting", "throbbing",
                          "bad today", "bad again", "bad all day", "bad this week",
                          "gone bad", "been bad")),
          "For a joint or muscle that aches without a fall or a twist, keep it moving gently "
          "rather than resting it: a short walk, a warm bath and paracetamol or ibuprofen gel "
          "usually settle it in a week or two, and strength work on the muscles around it is what "
          "stops it coming back. See a GP or physio if it is swollen, locks or gives way, wakes you "
          "at night, or has not improved after two to three weeks.",
          avoid=("run", "running", "jog", "after a run", "exercise", "gym", "stretch",
                 "cant feel", "can't feel", "numb", "numbness", "pins and needles", "tingling",
                 "gave way", "give way", "collapsed",
                 "is that bad", "is it bad", "is that serious", "is it serious", "is that normal",
                 "is it normal", "is that ok", "is that okay", "is it ok", "is it okay",
                 "should i worry", "how bad is it", "how bad", "is that dangerous"),
          guard=_the_part_is_a_persons),


    entry("joints-in-cold-weather",
          (("knee", "knees", "hip", "hips", "hand", "hands", "finger", "fingers", "joint",
            "joints", "back", "shoulder", "shoulders", "wrist", "wrists", "ankle", "ankles",
            "elbow", "elbows", "arthritis", "knuckles", "feet", "foot", "toes", "toe",
            "stiff", "stiffness", "stiffen"),
           ("cold", "colder", "cold weather", "the cold", "weather", "rain", "rains", "raining",
            "rainy", "damp", "humid", "winter", "frost", "frosty", "when it rains",
            "when its cold", "when it's cold", "change in the weather", "barometric")),
          "Weather ache is real and it is not damage: cold and damp stiffen the muscles round a "
          "joint and the joint itself feels thicker, and the drop in pressure before rain is what "
          "people notice most. Nothing about it is doing harm, so the answer is warmth and "
          "movement rather than rest - warm up before you go out, keep the knees and hands covered, "
          "keep walking, and use a warm bath or a wheat bag in the evening. See a GP if one joint "
          "is hot, red or swollen, if the ache is there all the time rather than in the cold, or "
          "if it is waking you at night: that is worth a proper look, and arthritis that is worse "
          "in winter is still worth an appointment to get the treatment right.",
          avoid=("flu", "fever", "temperature", "shivery", "sick", "vomit", "cough", "chest",
                 "breathless", "numb", "cant feel", "can't feel", "pins and needles", "fell",
                 "fall", "twisted", "swollen", "hot and swollen", "red and hot", "gout",
                 "fridge", "freezer", "drink", "drinks", "beer", "water bottle", "room",
                 "house", "flat", "heating", "thermostat", "radiator", "sleeping", "bedroom",
                 ),
          ask=("ache", "aches", "aching", "achey", "achy", "hurt", "hurts", "hurting", "pain",
               "pains", "painful", "sore", "soreness", "stiff", "stiffness", "stiffen",
               "stiffens", "stiffened", "plays up", "playing up", "played up", "joint",
               "joints", "arthritis")),
    entry("metallic-taste", (("metallic taste", "metal taste", "taste of metal", "tastes of metal",
                              "tastes metallic", "funny taste", "bitter taste", "odd taste"),
                             ("mouth", "taste", "eating", "drinking", "have", "keep", "constant",
                              "in my")),
          "A metallic taste is usually harmless and usually has an ordinary cause: gum trouble, a "
          "dry mouth, a new medicine (metronidazole and some blood pressure tablets are famous for "
          "it), a cold or sinus infection, or pregnancy. Brush and floss and drink water through the "
          "day, and see a dentist if your gums bleed; see a GP if it lasts more than a couple of "
          "weeks or comes with weight loss or a lasting dry mouth.",
          avoid=("water", "tap", "kettle", "pipe", "coins", "coin", "cooking", "wine", "beer",
                 "coffee", "food", "pan", "saucepan", "spoon",
                 "rice", "soup", "sauce", "stew", "pasta", "bread", "meat", "fish", "eggs",
                 "milk", "dish", "meal", "leftovers", "tap water", "boiled")),
    entry("shoulder-click", (("shoulder", "shoulders"),
                             ("click", "clicks", "clicking", "clunk", "grind", "grinding", "pop",
                              "popping", "snap", "crack", "cracking")),
          "A shoulder that clicks without pain is usually harmless - it is tendon sliding over bone "
          "or a bit of scar tissue - and it needs nothing. If it clicks and hurts, catches, or the "
          "arm feels weak overhead, see a physio: rotator cuff and shoulder blade exercises fix most "
          "of it without an operation, and the sooner you start the quicker it settles.",
          avoid=("bag", "bags", "chip", "chips", "road", "shrug", "shrugs")),
    entry("back-click", (("back", "lower back", "spine", "backbone"),
                         ("crack", "cracks", "cracking", "cracked", "click", "clicks",
                          "clicking", "clicked", "pop", "pops", "popping", "popped",
                          "snap", "snapping", "crunch", "crunching", "release",
                          "loosen", "loosening")),
          "Don't force it, and don't get somebody to walk on your back or wrench it round - the "
          "pop you are after is a joint letting go, and a hard twist is how discs and ribs get "
          "hurt. What gives the same relief safely is movement: kneel and round your back up and "
          "down slowly (cat-cow) ten times, sit back on your heels with your arms stretched "
          "forward, then lie on your back and pull each knee to your chest. Standing and leaning "
          "back over the edge of an open door with your hands on the frame opens the mid-back "
          "too. If the back is sore rather than stiff, treat it as a strain - keep walking, take "
          "paracetamol or ibuprofen if you can, and see a GP if it is no better in a fortnight.",
          avoid=("hurt", "hurts", "hurting", "pain", "painful", "sore", "ache", "aches",
                 "aching", "sharp", "stiff", "stiffness", "tooth", "teeth", "skin",
                 "hands", "lips", "heel", "heels", "heels are", "egg", "eggs", "phone",
                 "screen", "iphone", "code", "joke", "jokes", "knuckle", "knuckles",
                 "fingers", "password", "voice", "whip", "nuts", "ribs", "rib",
                 "wifi", "wi-fi", "window", "windows", "wall", "walls", "door", "drive",
                 "pavement", "tiles", "ceiling", "plaster", "grout")),
    entry("dry-mouth-night", (("dry mouth", "mouth is dry", "mouth feels dry", "thirsty",
                               "cotton mouth",
                               "mouths been dry", "mouth been dry", "mouth has been dry",
                               "mouth is so dry", "mouth keeps going dry"),
                              ("wake", "wakes", "waking", "morning", "night", "sleep", "asleep",
                               "always", "every", "in the", "all the time", "constant", "day",
                               "my", "is", "feels", "have")),
          "A dry mouth is usually mouth breathing - a blocked nose, a stuffy room, snoring - or "
          "a side effect of a medicine, and alcohol and caffeine late on make it worse. Water by the "
          "bed, a saline spray if your nose is blocked and less to drink in the evening sort most of "
          "it. If you are also thirsty and weeing a lot, or it never goes, ask a GP to check it.",
          avoid=("hay fever", "hayfever", "dog", "cat", "baby", "child", "toddler",
                 "always thirsty", "constantly thirsty", "still thirsty", "so much water",
                 "too much water", "stop drinking", "drink too much", "drinking so much",
                 "drink a lot", "drinking a lot", "never quenched")),
    entry("headache-behind-eyes", (("behind my eyes", "behind the eyes", "behind my eye",
                                    "behind the eye", "over my eyes"),
                                   ("headache", "headaches", "pain", "ache", "hurts", "pressure",
                                    "pounding", "every day", "keep getting")),
          "Pain behind the eyes is usually eye strain or a tension headache: screen breaks, an eye "
          "test if you have not had one, and water and a dark room for an hour help most of it. "
          "Sinusitis makes the area tender and comes with a blocked nose, and migraine can sit there "
          "too. Get seen the same day if it is the worst headache of your life, or comes with a "
          "fever and a stiff neck, or with blurred or double vision.",
          avoid=("black eye", "shiner", "bruise", "makeup", "mascara")),
    entry("big-tablet", (("tablet", "tablets", "pill", "pills", "capsule", "medicine"),
                         ("too big", "swallow", "swallowing", "hard to", "cant take", "choke",
                          "large")),
          "Take a mouthful of water first, put the tablet further back on your tongue than feels "
          "natural and swallow with your chin tipped slightly down, which opens the throat. If it is "
          "a plain tablet the pharmacist can usually give the same medicine as a smaller one or a "
          "liquid, so ask rather than cutting a slow-release one.",
          avoid=("throat", "tonsil", "swallow food")),
    entry("morning-after-pill", (
        ("morning after pill", "morning-after pill", "morning after", "emergency contraception",
         "emergency contraceptive", "levonorgestrel", "levonelle", "ellaone", "ella one",
         "ulipristal", "plan b", "unprotected sex", "condom split", "condom broke",
         "condom came off", "the condom split", "the condom broke", "didnt use a condom",
         "didn't use a condom", "no condom", "forgot to use a condom",
         "coil as emergency", "coil for emergency"),
        ("get", "where", "how", "how long", "work", "works", "do i need", "prescription",
         "pharmacy", "free", "age", "late", "how late", "effective", "side effects", "wait",
         "how soon", "72", "120", "coil", "iud", "what do i do", "what now", "worried",
         "as soon as", "now", "today", "tomorrow", "nearly",
         "sooner", "later", "chance", "chances", "likely",
         "sick", "nausea", "nauseous", "vomit", "throw up", "feel ill",
         "ovulated", "ovulating", "ovulation", "released an egg",
         "age", "age limit", "how old", "16", "15", "under 16", "difference", "better than",
         "what is", "whats", "what's", "mean", "means", "explain",
         "bad for you", "side effects", "side effect", "harmful", "how safe", "risk",
         "how much", "cost", "costs", "price", "pay", "pay for", "charge", "charges")),
        _morning_after,
        ask=("morning after pill", "morning after", "emergency contraception", "unprotected sex",
             "condom split", "condom broke",
             "plan b", "levonelle", "levonorgestrel", "ellaone", "ella one", "ulipristal",
             "side effects", "bad for you", "safe", "what is", "whats", "what's", "is it",
             "does it", "how do i", "can i", "how long", "difference", "better than"),
        avoid=("dog", "dogs", "cat", "cats", "pet", "pets", "vet", "for the dog", "for the cat",
               "already pregnant", "am pregnant", "im pregnant", "i'm pregnant", "abortion",
               "termination")),
    entry("the-pill-and-pregnancy", (
        ("pill", "my pill", "the pill", "combined pill", "mini pill", "contraceptive pill",
         "contraception", "contraceptive"),
        ("pregnant", "get pregnant", "how safe", "safe", "work", "works", "effective",
         "reliable", "chance", "risk", "how likely", "protect", "protects", "trust")),
        "On a combined pill taken every day, about 1 in 100 people get pregnant in a year with "
        "perfect use, and about 9 in 100 with typical use - most of those from a missed pill, a "
        "stomach bug or another medicine interfering. If you want the most reliable, a coil or an "
        "implant is over 99% and needs no daily remembering. On the mini pill three hours late "
        "counts as missed, so take it when you remember and use condoms for seven days.",
        ask=("pregnant", "how safe", "safe", "work", "effective", "reliable"),
        avoid=("missed", "miss", "forgot", "forgotten", "skipped", "morning after", "emergency",
               "tablet", "tablets", "medicine", "medicines", "shelf life", "expire", "expired",
               "sugar", "water", "blood pressure", "statins", "antibiotics", "dose", "dosage")),
    entry("side-effects",
          (("tablet", "tablets", "pill", "pills", "medication", "meds", "medicine", "medicine's",
            "prescription", "dose", "new tablets", "statins", "antibiotics", "antidepressants",
            "inhaler", "jabs", "jab", "side effect", "side effects", "side-effects"),
           ("side effect", "side effects", "side-effects", "making me", "make me", "made me",
            "feel odd", "feel awful", "feel sick", "feel weird", "feeling sick", "feeling odd",
            "feeling awful", "feeling weird", "not myself", "hasnt been himself",
            "hasn't been himself", "hasnt been herself", "hasn't been herself", "is it the",
            "its the tablets", "it's the tablets", "could it be", "is this normal",
            "should i stop", "come off", "stop taking", "different one", "cause",
            "normal", "usual", "expected", "how long", "worth it", "common")),
          "Most side effects are listed in the leaflet in the box, with how common each one is, "
          "and the ones that hit in the first fortnight - sickness, a fuzzy head, tiredness - often "
          "ease by weeks two to four. Do not stop suddenly on your own: steroids, antidepressants, "
          "epilepsy tablets and anything for the heart or blood pressure can be dangerous to stop, "
          "even when they are the problem. Ask the pharmacist today, who is fastest on interactions "
          "and can say whether a different brand, dose or timing would suit better, then ask the GP "
          "for a review with the list of what changed. Get help the same day for a rash with "
          "swelling or trouble breathing, a fast heart with fainting, or new confusion.",
          avoid=("double", "double up", "missed", "forgot", "forget", "ran out", "swallow",
                 "too big", "choke", "with alcohol", "with food", "together", "pregnant",
                 "breastfeeding", "overdose", "too many", "child", "toddler", "baby",
                 "morning after", "emergency contraception", "plan b", "levonelle", "ellaone",
                 "booster", "boosters", "mmr", "measles", "mumps", "rubella", "shingles",
                 "pneumococcal", "pneumonia", "tetanus", "whooping cough", "am i due",
                 "when should i", "do i need", "due for"),
          bias=1,
          lead=("yesno", "Usually, yes")),
    entry("forgetting-tablets", (("forget", "forgetting", "forgot", "forgetful", "miss", "missing",
                                  "missed"),
                                 ("tablet", "tablets", "pill", "pills", "medication", "meds",
                                  "medicine", "dose", "doses", "inhaler")),
          "A pill box with the days on it, filled at the same time each week, is the fix that works "
          "for most people, and a phone alarm set for when you actually eat beats one at a random "
          "hour. Ask your pharmacy about a weekly blister pack as well - many make one up for free.",
          avoid=("password", "name", "birthday", "keys", "appointment", "bus", "train", "flight",
                 "period", "my mum", "my dad", "grandma", "grandad",
                 "double", "doubled", "doubling", "double up", "twice", "two tablets", "two pills",
                 "two of my", "take two", "extra dose", "extra one", "another dose", "catch up",
                 "epilepsy", "epileptic", "warfarin", "blood thinner", "blood thinners", "thyroid",
                 "levothyroxine", "insulin", "diabetes", "diabetic", "heart tablets", "lithium",
                 "ran out", "run out", "running out",
                 "my nan", "my nanna", "my gran", "my granny", "my wife", "my husband",
                 "my partner", "my sister", "my brother",
                 "forgot my tablet", "forgot my tablets", "forgot my pill", "forgot my medication",
                 "forgot to take my tablet", "forgot to take my tablets", "forgot to take my pill",
                 "missed my tablet", "missed my tablets", "missed my medication", "missed my pill",
                 "missed a tablet", "missed a dose", "missed one")),
    entry("eye-test", (("eye test", "eye tests", "eyes tested", "optician", "opticians", "sight test",
                        "specsavers"),
                       ("how often", "when", "yearly", "every", "book", "need", "due", "time")),
          "Every two years is the usual rhythm, and every year if you are over 70, diabetic or have "
          "a close relative with glaucoma. It is free on the NHS for under 16s, over 60s and people "
          "with diabetes, and it checks the health of the eye as well as the prescription."),
    entry("need-glasses",
          (("need glasses", "need new glasses", "need spectacles", "need specs",
            "get glasses", "sight", "eyesight", "my vision", "my eyes", "blurry",
            "blurred", "cant see", "can't see", "struggle to see", "squint at"),
           ("need", "do i need", "do i have to get", "should i get", "will i need",
            "might i need", "worth getting", "have my eyes tested", "get my eyes tested",
            "need an eye test", "need a sight test", "do with")),
          "Book a sight test: about twenty minutes, and the only thing that says whether you "
          "need glasses and what prescription - nothing you do at home settles it. The blur "
          "usually has a name: eyes that ache after a chapter in bed are the focusing muscles "
          "tired from close work and dim light, and a distance that has gone soft is short "
          "sight, which a pair from the test sorts. It is free on the NHS if you are under 16, "
          "over 60, diabetic or a close "
          "relative has glaucoma, and \u00a325-\u00a345 on the high street otherwise. Sudden "
          "blur in one eye, floaters, flashes or a curtain across the sight is an A&E or "
          "optician-today job.",
          ask=("need", "do i need", "should i get", "will i need", "have to", "worth",
               "have my eyes tested", "get my eyes tested", "might i"),
          guard=not_a_when_ask,
          avoid=("clean", "cleaning", "dirty", "smudge", "smudges", "smudged", "fog", "foggy",
                 "water", "drink", "drinks", "drinking", "litre", "litres", "liter", "liters",
                 "pint", "pints", "fluid", "fluids", "wine", "wine glass", "wine glasses",
                 "glass of", "glasses of", "a day", "each day", "per day",
                 "fogged", "scratch", "scratched", "scratches", "repair", "repairs", "fix",
                 "fixed", "broken", "broke", "arm", "arms", "frame", "frames", "lens", "lenses",
                 "sunglasses", "prescription", "how much", "cost", "price", "afford", "free",
                 "how often", "every two years", "driving", "for driving", "contacts",
                 "contact lens", "contact lenses", "laser", "cataract", "floaters",
                 "child", "children", "kid", "kids", "school", "my son", "my daughter",
                 "toddler", "baby"),
          bias=2),
    entry("hypo-signs", (("hypo", "hypos", "hypoglycaemia", "hypoglycemia", "hypo symptoms",
                          "low blood sugar", "blood sugar", "blood sugars"),
                         ("signs", "symptoms", "sign", "warning signs", "feel like", "feels like",
                          "look like", "know", "tell", "recognise", "recognize", "spot")),
          "The early signs are shaky, sweaty and hungry with a fast heart and tingling lips, and "
          "people often get irritable or muddled before they notice anything. Test if you have "
          "your meter; if you cannot, treat anyway - 15 to 20g of fast sugar, a small glass of "
          "juice or four glucose tablets, then retest in 15 minutes and repeat if it is still low. "
          "Follow it with a proper snack, or you will drop again.",
          avoid=("my mum", "my dad", "my son", "my daughter", "my husband", "my wife",
                 "my gran", "my nan", "my brother", "my sister", "my friend", "my neighbour",
                 "my child", "my baby", "unconscious", "passed out", "fitting", "can't wake",
                 "wont wake")),
    entry("hypo-avoiding", (("hypo", "hypos", "hypoglycaemia", "hypoglycemia", "low blood sugar",
                             "blood sugar", "blood sugars"),
                            ("avoid", "avoiding", "prevent", "preventing", "stop having",
                             "not have", "keep having", "keep getting", "more often", "happen",
                             "happens", "why did i", "why do i", "cause", "causes", "last night",
                             "at night", "night", "waking", "wake up", "woken", "in my sleep",
                             "again", "drops", "drop", "crashes", "dips", "after exercise",
                             "after a run", "after sport")),
          "Most hypos come from a meal that was missed or late, a dose that is now too big, "
          "exercise without eating, or alcohol - and drink is the usual reason for one at night, "
          "because it stops the liver putting sugar out while you sleep. Carry glucose tablets and "
          "keep some by the bed, eat before you drink and test before you drive. If you are having "
          "them more than once a week, or waking sweaty with a headache, tell your diabetes team: "
          "the doses need looking at, and that is their call to make.",
          avoid=("my mum", "my dad", "my son", "my daughter", "my husband", "my wife",
                 "my gran", "my nan", "my brother", "my sister", "my friend", "my neighbour",
                 "my child", "my baby", "unconscious", "passed out", "fitting", "can't wake",
                 "wont wake", "what can i eat", "what should i eat")),
    entry("hypo-or-hunger", (("hypo", "hypos", "low blood sugar"),
                             ("or just hungry", "or hunger", "or am i just hungry", "just hunger",
                              "hunger", "hungry", "or just")),
          "Hunger on its own gives you a rumbling stomach and a dip in mood; a hypo also brings the "
          "shakes, sweat, a fast heart and tingling lips, and it comes on fast. If you have "
          "diabetes and cannot test, treat it as a hypo - 15g of fast sugar settles hunger too and "
          "costs you little. If it keeps happening an hour or two after meals, the dose or the meal "
          "is worth looking at rather than eating more.",
          avoid=("my mum", "my dad", "my son", "my daughter", "my husband", "my wife",
                   "my gran", "my nan", "my brother", "my sister", "my friend", "my child",
                   "my baby")),


    entry("night-cramp", (("cramp", "cramps", "cramping", "cramped up", "charley horse"),
                          ("night", "nights", "bed", "sleep", "asleep", "wake", "wakes",
                           "woke", "waking", "wake up", "woke up", "waking up",
                           "foot", "feet", "toe", "toes", "calf", "calves", "leg", "legs",
                           "why", "how", "stop", "help", "get rid", "prevent")),
          "Night cramp in the foot or calf is usually a muscle that has been short all day. The "
            "fix is stretching before bed: stand facing a wall with the back leg straight and "
            "the heel down, hold 30 seconds on each side. When one starts, pull your toes up hard "
            "towards your shin and stand up if you can, which ends it faster than waiting. Keep "
            "water by the bed and a warm blanket on the leg. See a GP if it is most nights, if you "
            "take a water tablet or a statin, or if the calf is swollen, hot or tender - that one "
            "is a clot until a doctor says not, so ring 111 the same day.",
          ask=("night", "nights", "bed", "sleep", "asleep", "wake me", "wakes me", "woke me",
               "wake up", "woke up", "waking up", "waking", "wakes me up"),
          bias=2,
          avoid=("swollen", "swelling", "swells", "puffy", "fluid", "ankle", "ankles",
                 "child", "children", "baby", "toddler", "kid", "kids", "pregnant",
                 "pregnancy", "period", "stomach", "tummy", "dog", "cat",
                 "run", "running", "gym", "marathon", "workout", "swimming", "swim",
                 "stretch", "stretches", "after exercise")),
    entry("restless-legs", (("restless leg", "restless legs", "legs are restless", "legs twitch",
                             "twitchy legs", "crawl in my legs", "fizzy legs", "legs at night"),
                            ("night", "bed", "sleep", "cant", "can't", "help", "why", "how",
                             "stop", "worse", "moving")),
          "Restless legs feel like a crawl or a fizz in the legs in the evening that only moving "
          "eases. Ask a GP for a blood test first, because low iron is a common cause; cut caffeine "
          "and alcohol late, and try a warm bath and calf stretches before bed. If it is disturbing "
          "your sleep most nights, say so, because it is treatable.",
          avoid=("cramp", "cramps", "cramping", "child", "children", "baby", "toddler", "dog",
                 "cat", "stretch", "workout", "run"),
          report=True),

    entry("morning-headache", (("wake up with a headache", "waking up with a headache",
                                "wake with a headache", "woke up with a headache",
                                "headache every morning", "headache in the morning",
                                "morning headache", "headaches in the morning"),
                               ("why", "how", "help", "stop", "what", "should", "every", "always",
                                "keep", "means",
                                "wake", "waking", "woke", "up", "morning", "mornings", "have",
                                "got", "get", "sore", "throbbing", "dull", "bad", "daily",
                                "most")),
          "Morning headaches usually come from the night: too little water, teeth grinding, a hot "
          "room, alcohol, or a pillow that puts your neck out. Try water before bed, a cooler room "
          "and less booze, and see a GP if it is most mornings, if you snore and wake unrefreshed, "
          "or if the pain is worst as you wake.",
          avoid=("child", "children", "kid", "kids", "daughter", "son", "baby", "pregnant",
                 "pregnancy", "toddler", "school", "dog", "cat", "puppy", "kitten", "pet")),

    entry("morning-urine", (("wee is dark in the morning", "wee dark in the morning",
                             "dark wee in the morning", "dark urine in the morning",
                             "urine is dark in the morning", "urine dark in the morning",
                             "dark pee in the morning", "pee is dark in the morning",
                             "wee dark first thing", "urine dark first thing",
                             "dark urine first thing", "dark wee first thing",
                             "dark when i wake up", "dark first thing",
                             "morning wee", "wee in the morning", "urine in the morning"),
                            ("why", "always", "every", "normal", "problem", "should", "worry",
                             "what", "means", "drink", "drinking", "dark", "yellow", "morning",
                             "concentrated", "bad", "ok", "okay", "fine")),
          "Dark urine first thing is normal: you have not had a drink for eight hours, so the "
          "kidney holds on to water and the waste that is left is concentrated. Drink a glass or "
          "two and it should be pale straw within an hour; if it stays dark all day, or looks "
          "like tea or cola, or it comes with thirst, tiredness and needing to wee a lot, get it "
          "checked the same week.",
          avoid=("blood", "smell", "smells", "smelly", "infection", "uti", "cystitis", "burn",
                 "burning", "sting", "stings", "pain", "painful", "child", "children", "kid",
                 "kids", "son", "daughter", "baby", "toddler", "nappy", "pregnant", "pregnancy",
                 "cat", "cats", "dog", "puppy", "toilet cleaner", "stain", "stains")),

    entry("morning-anxiety", (("anxious in the morning", "anxious in the mornings",
                               "anxious every morning", "anxiety in the morning",
                               "morning anxiety", "wake up anxious", "waking up anxious",
                               "woke up anxious", "wake up feeling anxious",
                               "wake up with anxiety", "anxious when i wake up",
                               "anxious as soon as i wake up", "anxious first thing",
                               "dread in the morning", "dreading the morning", "wake up dreading",
                               "wake up panicking", "wake up panicky", "morning panic",
                               "wake up with a knot in my stomach"),
                              ("why", "always", "every", "what", "how", "help", "stop", "should",
                               "can", "morning", "mornings", "wake", "waking", "woke", "up",
                               "feel", "feeling", "do", "get", "rid", "better", "cope")),
          "Anxiety that is worst in the first hour is usually the body waking up rather than a "
          "verdict on your day: cortisol peaks about 30 minutes after you get up, and short sleep, "
          "low blood sugar and alcohol the night before all push it higher. Eat something within "
          "an hour of waking, get outside in daylight before you look at your phone, and leave "
          "the coffee until after food; if it is most mornings for a month, or comes with a "
          "racing heart or breathlessness, have a GP look at it.",
          avoid=("child", "children", "kid", "kids", "son", "daughter", "baby", "toddler",
                 "school", "school refusal", "exam", "test", "interview", "dog", "cat", "puppy",
                 "pregnant", "pregnancy", "morning sickness", "vomit", "nausea", "nauseous",
                 "medication", "tablets", "antidepressant", "side effect", "come down",
                 "withdrawal")),

    entry("blocked-ear", (("blocked ear", "blocked ears", "ear is blocked", "ear feels blocked",
                           "bunged up ear", "ears are blocked", "wax", "ear wax", "unblock my ear",
                           "ear feels full", "ears feel full", "ear is full", "ears are full",
                           "full ear", "ear feels like it needs to pop", "ears feel blocked"),
                          ("how", "what", "help", "should", "can", "get rid", "clear", "remove",
                           "feels", "week", "days")),
          "For a blocked ear, olive oil drops twice a day for a few days soften the wax, and "
          "swallowing or yawning clears the pressure after a cold or a flight. Don't put cotton buds "
          "in it. If hearing drops, there is pain or discharge, or it has lasted a week, a pharmacist "
          "can look and a GP can syringe it.",
          avoid=("child", "children", "baby", "toddler", "dog", "cat", "puppy", "earache",
                 "ear infection", "hearing aid", "phone", "headphone",
                 "table", "tables", "tablecloth", "table top", "floor", "floors", "floorboards",
                 "carpet", "wood", "wooden", "furniture", "worktop", "sofa",
                 "car", "cars", "vehicle", "car seat", "seat", "seats", "upholstery", "bodywork",
                 "paintwork", "car body", "glass", "tiles", "mirror", "sink", "bath", "cloth",
                 "fabric", "surface", "surface", "skirting", "door", "pan", "mould",
                 "leg", "legs", "legs waxed", "bikini", "eyebrow", "eyebrows", "underarm",
                 "armpit", "beard", "salon", "beauty", "hair removal", "laser",
                 "strip wax", "wax strips")),

    entry("water-in-ear", ("water in my ear", "water in my ears", "water is in my ear",
                           "water is in my ears", "water is stuck in my ear",
                           "water is trapped in my ear", "water trapped in my ear",
                           "stuck in my ear", "stuck in my ears", "trapped in my ear",
                           "trapped in my ears",
                           "water trapped in my ears", "water stuck in my ear",
                           "water stuck in my ears", "swimmers ear", "swimmer's ear",
                           "water got in my ear", "got water in my ear",
                           "water out of my ear", "water out of my ears",
                           "get water out of my ear", "water in my ear after swimming",
                           "water in my ear after a bath", "water in my ear after a shower",
                           "water in my ear from swimming"),
          "Tilt that ear down and shake it gently, then pull the lobe and open your mouth wide: "
          "that straightens the canal enough for the water to run out on its own. A hairdryer on "
          "the cool setting, held an arm's length away for a minute, and a few drops of a pharmacy "
          "drying spray do the same job. Don't dig in a cotton bud or a finger - it pushes the "
          "water further in and scratches the skin, which is how the infection starts. Keep the "
          "ear dry for a few days and see a pharmacist or GP if it becomes painful, itchy, leaks "
          "anything, or your hearing stays muffled: that is swimmer's ear, and it needs drops.",
          avoid=("child", "children", "baby", "toddler", "dog", "cat", "puppy", "sink",
                 "pipe", "tap", "boiler", "leak", "leaking", "radiator", "washing machine")),

    entry("red-eye", (("red eye", "red eyes", "eye is red", "my eye is red", "eyes are red",
                       "eye is watery", "eye keeps watering", "eyes streaming", "watery eyes",
                       "watery eye", "itchy eyes", "gunky eye", "sticky eye", "conjunctivitis",
                       "pink eye",
                       "bloodshot", "bloodshot eyes", "bloodshot eye", "blood shot",
                       "eye watering", "eye is watering", "eyes watering", "eye is still watering",
                       "eyes are still watering", "eye still watering", "eye keeps watering",
                       "eyes keep watering", "eye is itchy", "eyes itch", "itchy eye",
                       "eyes are streaming", "eyes always streaming", "eyes are always streaming",
                       "eye is streaming", "eyes stream", "eyes are watering",
                       "eyes always watering", "eyes are always watering", "eye streams"),
                      ("why", "how", "help", "what", "should", "treat", "get rid", "clear",
                       "days", "morning", "keeps", "watery", "watering", "streaming", "gritty",
                       "eye", "eyes",
                       "sticky", "gunky",
                       "itchy", "itch", "think i have", "think ive got", "have i got",
                       "is it", "what is",
                       "have", "got", "ive got", "is", "are", "looks", "look", "told",
                       "eyes", "bloodshot")),
          "A red, watery, gunky eye is usually conjunctivitis or an allergy: cool compresses, "
          "lubricating drops from a pharmacist, and no contact lenses until it settles. See someone "
          "the same day if the eye is painful, light hurts, your sight has dropped, or the eyeball "
          "feels hard - that is a different problem from a sticky eye.",
          avoid=("child", "children", "baby", "toddler", "dog", "cat", "puppy", "screen",
                 "phone", "makeup", "mascara", "tired",
                 "wind", "windy",
                 "keep down", "keeps down", "keep it down", "keep anything down",
                 "keep fluids down", "keep water down", "keep food down", "vomit", "vomiting",
                 "throwing up", "thrown up")),

    entry("dry-eye", (("dry eye", "dry eyes", "eyes are dry", "eyes feel dry",
                       "gritty eyes", "eyes feel gritty", "scratchy eyes", "eyes are scratchy",
                       "eyes water", "eyes are watering", "eyes keep watering", "tired eyes",
                       "sore tired eyes", "eyes sting", "burning eyes", "eyes are burning",
                       "eyes burning", "eyes are stinging", "stinging eyes", "eyes are irritated",
                       "irritated eyes", "eye is stinging", "eye is burning",
                       "eye is irritated", "eye feels irritated", "eye is scratchy",
                       "eye feels scratchy", "eye is gritty", "eye feels gritty",
                       "eyes are gritty", "eyes are sore", "eyes feel sore", "eye is sore",
                       "eye feels sore", "eyes feel tired", "eyes are itchy", "eyes feel itchy",
                       "keeps watering", "keep watering", "always watering", "watering all the",
                       "eyes streaming", "eyes are streaming", "eye streaming",
                       "eyes watering", "eye watering", "still watering", "keeps watering",
                       "kept watering",
                       "eyes being dry", "eyes get dry", "eyes getting dry", "eyes dry out",
                       "eyes drying out", "eyes so dry"),
                      ("what", "help", "how", "stop", "fix", "why", "always", "keep", "keeps",
                       "should", "gritty", "gritty feeling", "sore", "sting", "stings",
                       "stinging", "burning", "irritated", "scratchy", "tired", "screen",
                       "drops",
                       "at night", "in the morning", "worse", "anything", "water", "watering",
                       "all the time", "ache", "aching", "dry", "red", "scratchy", "stinging",
                       "streaming",
                       "burning", "irritated", "tired")),
          "Dry eyes are usually the tear film breaking up: screens, heating, air conditioning, "
          "contact lenses or getting older - and watering is often the same thing, because a dry "
          "surface makes the eye produce tears that do not stay on it. A pharmacist's lubricating "
          "drop - carbomer or "
          "hyaluronic acid - three or four times a day does most of the work, plus the 20-20-20 "
          "rule at the screen. Five minutes of warm compress on the lids helps if they are "
          "crusty. See an optician if it is painful or you need drops every hour.",
          avoid=("child", "children", "baby", "toddler", "dog", "cat", "puppy", "kitten",
                 "red eyes", "red eye", "conjunctivitis", "stye", "gunky", "contact lens",
                 "garden", "plant", "plants", "lawn", "tomato", "tomatoes", "flower",
                 "change the water", "water change", "fish tank", "pond",
                 "kettle", "tap water", "water filter", "drinking water",
                 "flowers", "hanging basket", "watering can", "repot",
                 "houseplant", "houseplants", "house plant", "house plants", "pot plant",
                 "pot plants", "indoor plant", "indoor plants", "potted plant", "potted plants",
                 "cactus", "cacti", "succulent", "succulents", "orchid", "orchids", "fern",
                 "ferns", "peace lily", "spider plant", "monstera", "seedling", "seedlings",
                 "allotment", "border", "borders", "window box", "window boxes", "vegetable plot",
                 "bottle", "bottles", "water bottle", "gym", "drink", "drinks", "drinking",
                 "hydration", "hydrate", "mouth", "swim", "swimming", "pool", "tap", "kettle",
                 "keep down", "keeps down", "keep it down", "keep anything down", "kept down",
                 "keep fluids down", "keep water down", "keep food down", "vomit", "vomiting",
                 "vomited", "being sick", "throwing up", "thrown up", "throw up", "diarrhoea",
                 "diarrhea", "stomach bug", "gastro", "food poisoning", "norovirus",
                 "hosepipe", "hose", "rice", "pasta", "filter", "boil", "sink", "bucket",
                 "company", "companies", "supplier", "suppliers", "bill", "bills", "meter",
                 "meters", "utility", "utilities", "council", "rates", "sewage", "standing",
                 "charge", "account", "direct debit", "landlord", "plumber", "stopcock",
                 "litres", "liters", "litre", "liter", "glasses of water", "glass of water",
                 "how much water", "drink more water", "drink enough water", "eight glasses",
                 "dehydrated", "dehydration", "water intake", "bottle of water",
                 "water bottle",
                 "red", "redness", "bloodshot", "itchy", "itch", "itching", "gunky", "gunge",
                 "sticky", "crusty", "discharge", "pus", "yellow", "green",
                 "yellowed", "yellowing", "yellowish", "jaundice", "jaundiced",
                 "hard water", "hard water stains", "water stains", "water marks",
                 "limescale", "lime scale", "descale", "descaler", "shower head",
                 "shower screen", "shower glass", "shower tray", "shower door", "shower rail",
                 "grout", "the tiles", "tile grout", "kettle", "washing machine",
                 "dishwasher", "iron", "steam iron",
                 "yoghurt", "yogurt", "yoghurts", "yogurts", "raita", "tzatziki", "labneh",
                 "sour cream", "kefir", "fromage frais",
                 "thirsty", "thirst", "parched", "electrolytes", "flask", "pitcher",
                 "on a run", "on a ride", "long run", "half marathon", "marathon",
                 "on a bike", "on the bike", "out cycling"),
          bias=2,
          guard=_the_eye_is_said),

    entry("water-in-the-eye", (WATER_IN_EYE, EYE_RINSE_ASK),
          "Water alone does no harm to an eye, so if it stings there is soap or shampoo in it: hold "
          "the lids open and rinse with cool clean water for about five minutes, blink, and check "
          "your sight is clear. Turn the shower down or aim it at your shoulder while you wash "
          "your hair, and get the eye looked at the same day if it is still sore, red, or your "
          "sight is blurred after the rinsing.",
          avoid=("bleach", "chemical", "chemicals", "acid", "alkali", "paint", "white spirit",
                 "limescale", "hard water", "descale", "shower screen", "shower head",
                 "shower tray", "grout", "plant", "plants", "contact lens", "lens solution"),
          bias=1),

    entry("something-in-the-eye", (EYE_WHAT, EYE_WHERE),
          "Don't rub it - that is what scratches the surface. Blink a few times and let the tears "
          "do the first of it, then rinse the eye with clean, cool water or saline for ten to "
          "fifteen minutes, with the lid held open, over a sink or in the shower. If it is still "
          "there, or it was a piece of metal, grit from grinding or anything that hit the eye fast, "
          "or you cannot see properly, go to an eye casualty the same day rather than "
          "fishing for it. Never use tweezers or a cotton bud, and take a contact lens out.",
          avoid=("bleach", "chemical", "chemicals", "acid", "alkali", "paint", "white spirit",
                 "screen", "screens", "laptop", "dry", "tired", "cut",
                 "chilli", "chili", "chillies", "chilies", "chile", "jalapeno", "jalapenos",
                 "pepper", "peppers", "curry", "hot sauce", "tabasco", "sriracha", "wasabi",
                 "drinking water", "water cold", "keep water cold", "keep my water cold",
                 "water bottle", "water bottles", "cold water", "drinks cold", "keep drinks"),
          bias=2,
          guard=_a_persons_eye),

    entry("swollen-eye", (("eye is swollen", "eye is swollen shut", "swollen eyelid",
                           "eyelid is swollen", "my eyelid has swollen", "swollen eye",
                           "eye has swollen", "puffy eye", "puffy eyes", "eye is puffy",
                           "eyes are puffy", "lid is swollen"),
                          ("what", "why", "help", "how", "should", "treat", "get down", "bring",
                           "reduce", "cold", "worse", "hurts", "painful", "is it", "normal",
                           "have", "got", "shut", "closed", "open", "morning", "swelling",
                           "swollen", "up", "now", "still", "keeps")),
          "Cool it: a clean flannel under the cold tap, wrung out, for ten minutes at a time, and "
          "an antihistamine if the other eye or the nose is itchy too. Go to A&E or an urgent care "
          "the same day if the lid is red, hot and painful rather than just puffy, if the swelling "
          "came on fast, if your sight has changed or the eye itself is bulging, or if you have a "
          "temperature - that is an infection behind the lid and it needs antibiotics.",
          avoid=("black", "bruise", "bruised", "punch", "hit", "shiner", "dog", "cat", "child",
                 "baby")),

    entry("black-eye", (("black eye", "black eyes", "bruised eye", "shiner",
                         "eye is bruised", "bruise around my eye",
                         "eye has gone black", "eye went black", "eye has turned black",
                         "eye turned black", "eye has gone purple", "eye is going black",
                         "eyes have gone black", "eye is black", "black around my eye",
                         "blue around my eye", "purple around my eye"),
                        ("what", "how", "help", "long", "should", "treat", "get rid", "last",
                         "looks", "have", "got", "swollen", "gone", "fade",
                         "black", "purple", "blue", "bruised")),
          "Cold first: a bag of frozen peas wrapped in a tea towel, ten minutes on and ten off, "
          "for the first day or two, then leave it alone. Keep your head up on two pillows at "
          "night so it drains, take paracetamol if you need it, and don't blow your nose for a few "
          "days - that pushes air into the lids. The colour fades over about two weeks. Get it "
          "looked at the same day if your sight changes or goes double, the eye itself is red or "
          "bloody, the pain is severe, or the blow was to the head and you have vomited or feel "
          "drowsy."),

    entry("eye-floaters", (("floater", "floaters", "floater in my eye", "floaters in my eye",
                            "squiggles in my eye", "shapes in my vision", "specks in my vision",
                            "cobweb in my eye", "drifting spots in my vision"),
                           ("what", "why", "help", "normal", "should", "worried", "worry",
                            "sudden", "many", "more", "new", "worse", "loads", "lots", "have",
                            "got", "see", "vision", "flashes")),
          "Floaters are bits of the jelly inside the eye casting a shadow, and one or two that "
          "have been there a while are normal with age - they fade as your brain stops noticing "
          "them. What is not normal is a sudden shower of new ones, flashes like lightning at the "
          "edge of your sight, or a curtain or shadow coming across it: ring an optician or go to "
          "A&E the same day, because that is how a detached retina starts and it is fixable if it "
          "is caught quickly. Also get your sight checked if the floaters came with a blow to the "
          "head."),


    entry("cold-sore-tingle", (("cold sore", "cold sores", "sore on my lip", "blister on my lip",
                         "lip blister", "herpes", "tingle on my lip", "fever blister",
                         "sore on my nose", "blister on my nose", "zovirax", "aciclovir",
                         "cold sore cream", "lip sore"),
                        ("how", "what", "help", "get rid", "treat", "treatment", "cure", "long",
                         "stop", "should", "keep", "heal", "healing", "last", "have", "has", "got",
                         "sore", "sores", "soreness", "hurts", "hurting", "painful", "red",
                         "started", "coming", "contagious", "catch", "cause", "causes", "why",
                         "pop", "pick", "squeeze", "kiss", "kissing", "swim", "swimming",
                         "pool", "pregnant", "pregnancy", "expecting", "newborn", "recurring",
                         "back", "again", "remedy", "remedies", "cream", "work", "use", "use on",
                         "nose", "chin", "face")),
          _cold_sore,
          bias=1,
          avoid=("child", "children", "baby", "toddler", "mouth ulcer", "ulcer", "sore throat",
                 "throat", "canker",
                 "mouth", "gum", "gums")),

    entry("teeth-care", (("look after my teeth", "look after teeth", "healthy teeth",
                          "keep my teeth", "clean my teeth", "brush my teeth", "brushing",
                          "floss", "flossing", "toothpaste", "mouthwash"),
                         ("how", "what", "should", "best", "often", "long", "need", "help",
                          "right", "good", "twice", "day")),
          "Twice a day for two minutes with a fluoride toothpaste, spit rather than rinse so the "
          "fluoride stays on, and clean between the teeth once a day with floss or interdental "
          "brushes. Sugar between meals is what causes decay, so keep it to mealtimes, and a "
          "check-up every year or two keeps small problems cheap.",
          avoid=("child", "children", "baby", "toddler", "kid", "kids", "dog", "cat", "dog",
                 "false teeth", "denture", "braces", "whiten", "whitening", "bleeding",
                 "hair", "my hair", "hairbrush", "brushing my hair", "brush my hair",
                 "paint", "painting", "painted", "repaint", "emulsion", "gloss", "satin",
                 "woodwork", "wall", "walls", "roller", "varnish", "undercoat")),
    entry("electric-brush",
          (("electric toothbrush", "electric brush", "toothbrush", "toothbrushes", "electric"),
           ("better", "worth", "good", "buy", "which", "manual", "than", "should i get",
            "any good", "recommend", "expensive", "cheap", "need", "pay")),
          "A cheap electric brush with a timer cleans more evenly than most hands manage with a "
          "manual, and an expensive one is not twice as good, so pick one with a two-minute timer "
          "and a small round head. Change the head every three months. What matters more than the "
          "brush is a fluoride toothpaste and spitting rather than rinsing at the end.",
          avoid=("child", "children", "toddler", "kid", "kids", "son", "daughter", "baby", "dog",
                 "cat", "puppy", "kitten", "floss", "mouthwash", "whiten", "whitening", "yellow",
                 "bleed", "bleeding", "gums", "denture", "dentures", "braces", "toothache",
                 "how often", "when should", "change", "changing", "replace", "replacing",
                 "head", "heads"),
          ask=("electric toothbrush", "electric brush", "toothbrush", "toothbrushes")),

    entry("lifting-a-low-mood",
          (("sad", "sadness", "miserable", "unhappy", "glum",
            "fed up", "tearful", "weepy", "down in the dumps", "cheer myself up",
            "feeling low", "feel low", "feels low", "im low", "i am low", "bit low", "a bit low",
            "really low", "so low", "very low",
            "feeling down", "feel down", "feels down", "im down", "i am down", "bit down",
            "a bit down", "really down", "so down", "very down",
            "feeling flat", "feel flat", "feels flat", "feeling blue", "feel blue", "im blue",
            "bit blue", "a bit blue", "so blue", "really blue", "very blue", "quite blue",
            "feels blue", "im feeling blue", "im feeling so blue", "feeling so blue",
            "feel so blue", "feel a bit blue", "feeling a bit blue", "feel really blue",
            "feel very blue", "im feeling a bit blue", "feeling really blue",
            "im feeling flat", "feel a bit flat", "feeling a bit flat",
            "am blue", "am so blue", "am i blue", "am i so blue", "know why im blue",
            "feel quite flat", "feeling quite flat", "im quite flat", "im feeling quite flat",
            "feel pretty flat", "feeling pretty flat", "im pretty flat",
            "feel really flat", "feeling really flat", "im really flat",
            "feel very flat", "feeling very flat", "im very flat",
            "feel so flat", "feeling so flat", "im so flat", "im feeling so flat",
            "why do i feel so flat", "why i feel so flat",
            "feel a little flat", "feeling a little flat", "im a little flat",
            "feel a bit flat today", "feeling a bit flat today", "felt flat",
            "feel flat today", "feeling flat today", "feel flat this week",
            "feeling flat this week", "feel flat all week", "feel flat again",
            "feel flat again", "feeling flat again", "feel quite flat today",
            "why i feel blue", "why im so blue", "why i am so blue",
            "feel down in the", "feeling down in the",
            "cheer up", "feel happier", "happier", "feel better", "feeling better",
            "in a rut", "stuck in a rut", "no joy in anything", "nothing interests me"),
           ("how do i", "how can i", "what can i do", "what should i do", "stop", "lift",
            "felt", "today", "yesterday", "this week",
            "cheer", "feel", "feeling", "happier", "better", "keeps", "keep", "always",
            "all the time", "every day", "most days", "advice", "tips", "help", "why",
            "i dont know why", "don't know why", "nothing", "anymore", "any more")),
          "Do one small thing you used to enjoy today, at half enthusiasm, because mood follows "
          "action more often than it arrives on its own: a walk to the shop, a phone call, ten "
          "minutes of a game you liked. Then stack the three things that lift a low mood most "
          "reliably - daylight within an hour of waking, 20 minutes of walking, and one person "
          "you really talk to rather than message - and keep bedtime and meals at the same time, "
          "because a sad week wrecks both and then feeds itself. Write one line a day about how "
          "it went, so you can see it is not all bad. If it is most days for two weeks, if the "
          "pleasure has gone out of everything, or if it is stopping you eating or working, take "
          "it to the GP: talking therapy works, and in most areas you can refer yourself.",
          bias=1,
          guard=lambda understood: (_the_mood_is_the_persons(understood)
                                    and not _a_refusal_is_not_a_mood(understood)
                                    and not_a_cold_or_damp_house(understood)),
          avoid=("hurt myself", "harm myself", "kill myself", "suicide", "end my life",
                 "end it all", "self harm", "self-harm", "not want to be here", "better off dead",
                 "died", "death", "passed away", "funeral", "grief", "grieving", "bereaved",
                 "lonely", "loneliness", "no friends", "depressed", "depression",
                 "winter", "january", "december", "november", "february", "dark evenings",
                 "seasonal", "unhappy at work", "my job", "my boss", "at work",
                 "girlfriend", "boyfriend", "husband", "wife", "partner", "my ex",
                 "break up", "broke up", "divorce", "crying", "cry", "tears",
                 "anxious", "anxiety", "panic", "stressed", "stress", "burnt out", "burnout",
                 "tired", "exhausted", "no energy", "sleep",
                 "cost", "costs", "price", "prices", "bills", "bill", "spend", "spending",
                 "rent", "noise", "volume", "temperature", "calorie", "calories", "weight",
                 "cholesterol", "blood pressure", "salt", "sugar", "fuel", "heating",
                 "swelling", "swollen", "fever", "heart rate", "pulse", "damp", "condensation",
                 "mould", "dust", "weeds", "drinking", "alcohol", "blood sugar", "water",
                 "my heating", "our heating", "the heating", "boiler", "thermostat",
                 "radiator", "radiators", "turn it down", "turn down my", "turn my heating",
                 "heating bill", "heating on",
                 "biscuit", "biscuits", "cake", "cakes", "bread", "dough", "batter",
                 "pastry", "scone", "scones", "meringue", "meringues", "macaron", "macarons",
                 "sponge", "oven", "bake", "baked", "baking", "flour", "yeast", "icing",
                 "risen", "soggy", "crumble", "pancakes", "yorkshire", "prove", "proofed",
                 "lager", "beer", "cider", "prosecco", "fizzy")),

    entry("postnatal-depression",
          (("postnatal depression", "postpartum depression", "post natal depression",
            "pnd", "baby blues", "after having a baby", "after my baby", "since having my baby",
            "since my baby", "after the birth", "since the birth", "had my baby",
            "cry every day", "crying every day", "cry all the time", "bond with my baby",
            "bond with the baby", "not bonding", "havent bonded", "dont love my baby",
            "don't love my baby", "dont feel anything for my baby", "feel nothing for my baby",
            "dont feel anything for the baby", "no bond with"),
           ("depression", "depressed", "low", "sad", "cry", "crying", "tearful", "weepy",
            "anxious", "anxiety", "mood", "blues", "baby", "babies", "newborn", "weeks",
            "months", "how long", "normal", "bond", "bonding", "love", "worthless", "guilty",
            "overwhelmed", "cant cope", "can't cope", "sleep",
            )),
          _postnatal_mood_reply,
          guard=_about_a_baby,
          report=True,
          bias=2,
          avoid=("hurt myself", "harm myself", "kill myself", "suicide", "end my life",
                 "end it all", "self harm", "self-harm", "better off dead", "hurt my baby",
                 "harm my baby", "labour", "labor", "contractions", "waters broke",
                 "epidural", "caesarean", "c section", "c-section", "stitches", "lochia",
                 "bleeding after", "milk supply", "latch", "breastfeeding", "formula",
                 "wont sleep", "wont settle", "colic", "reflux", "winding", "weaning",
                 "lose weight", "losing weight", "weight loss", "lose the baby weight",
                 "put on weight", "putting on weight", "lost weight", "losing the baby weight",
                 "baby weight", "lose a stone", "slimming", "counting calories", "calorie",
                 "diet", "dieting", "get back in shape", "back to my old weight")),

    entry("seasonal-low-mood", (("flat", "low", "down", "miserable", "no energy", "sad",
                                 "knackered", "tired", "exhausted", "weepy"),
                                ("january", "winter", "darker", "dark evenings", "dark mornings",
                                 "darker months", "every year", "seasonal", "this time of year",
                                 "the clocks", "november", "december", "february")),
          "Feeling flat and tired in January or the dark months is common: less daylight shifts "
          "sleep and mood, and most people pick up by March. Get outside within an hour of waking, "
          "even on a grey day, keep up vitamin D in winter, and keep seeing people. If it stops you "
          "working or eating, or lasts beyond the winter, see a GP: light therapy and talking "
          "therapy both work, and it is not something to just push through.",
          avoid=("tyre", "tyres", "battery", "pack", "packed", "packing", "white", "bread",
                 "roof", "mate", "mates", "share", "screen", "beer", "coke", "lemonade",
                 "cap", "caps", "fizz", "stomach", "bike", "car"),
          guard=not_a_season_or_a_machine),

    entry("is-this-depression", (
        ("depressed", "depression", "depressive", "depression symptoms"),
        ("am i depressed", "could i be depressed", "might i be depressed", "is it depression",
         "is this depression", "do i have depression", "have i got depression",
         "i think i might be depressed", "i think i have depression",
         "i think ive got depression", "i think i might have depression",
         "i think im depressed", "i think i am depressed", "i might be depressed",
         "i might have depression", "wondering if im depressed", "how do i know if im depressed",
         "signs of depression", "symptoms of depression", "what are the signs of depression",
         "feel depressed", "feeling depressed", "felt depressed", "feel like im depressed",
         "think im depressed")),
          "Depression is most of the day, most days, for two weeks or more, with the pleasure gone "
          "out of things you usually enjoy and sleep or appetite changed with it. The next step is "
          "the GP: say how long it has been going on and what has changed, and in most areas you "
          "can refer yourself for talking therapy without waiting for them.",
          guard=_is_the_readers_own_line),

    entry("low-mood",
          (("low mood", "feeling low", "feel low", "felt low", "feeling down", "feel down",
            "felt down", "feeling flat", "feel flat", "felt flat", "feeling sad", "feel sad",
            "feeling miserable", "feel miserable", "feeling depressed", "feel depressed",
            "feel empty", "feeling empty", "feel numb", "feeling numb", "depressed",
            "depression", "miserable", "cant be bothered", "can't be bothered",
            "lost interest", "no interest", "dont enjoy", "don't enjoy",
            "no motivation", "unmotivated", "want to stay in bed", "cant face the day"),
           ("for weeks", "for a month", "for months", "for a while", "for ages", "all the time",
            "every day", "most days", "lately", "recently", "since christmas",
            "few weeks", "a few weeks", "couple of weeks", "a couple of weeks",
            "past few weeks", "for years",
            "im", "i am", "ive", "i have", "think im", "think i am", "how long",
            "what helps", "what can i do", "what should i do", "how do i know", "am i depressed",
            "is this depression", "is it depression", "do i have depression", "is it normal",
            "should i", "see someone", "see a gp", "see the doctor", "talk to", "gp", "doctor",
            "help", "get better", "feel better", "will it pass", "keeps coming back",
            "still feel", "cant shift", "worth", "normal")),
          "Depression is low mood most of the day, most days, for two weeks or more, with the "
          "pleasure gone out of things you normally enjoy. At that point see a GP rather than "
          "wait it out: talking therapy is the first treatment and it works, and you can refer "
          "yourself for NHS talking therapy without going through a GP. Meanwhile daylight soon "
          "after waking, a twenty-minute walk and the same wake-up time every day help, and so "
          "does one person who knows how it is.",
          bias=3,
          avoid=("winter", "january", "november", "december", "february", "seasonal",
                 "dark evenings", "dark mornings", "the clocks", "tyre", "tyres", "battery",
                 "batteries", "phone", "laptop", "signal", "flatmate", "flatmates", "white",
                 "bread", "beer", "roof", "share", "shares", "price", "prices", "interest rate",
                 "interest on", "savings", "mortgage", "pension", "isa", "bank", "loan", "rent",
                 "money", "bill", "bills", "job", "work", "boss", "interview", "exam", "exams",
                 "skint", "broke", "overdraft", "payday", "wages", "cost of living", "council tax",
                 "can't afford", "cant afford", "nothing to spend",
                 "died", "death", "funeral", "passed away", "grief", "grieving", "loss of",
                 "pregnant", "pregnancy", "baby", "babies", "newborn", "postnatal", "miscarriage",
                 "child", "children", "kid", "kids", "son", "daughter", "teenager", "teen",
                 "husband", "wife", "partner", "boyfriend", "girlfriend", "friend", "friends",
                 "no energy", "tired", "tiredness", "exhausted", "knackered", "sleepy",
                 "mum", "dad", "mother", "father", "sister", "brother", "dog", "cat", "puppy",
                 "kitten", "vet", "tooth", "teeth", "dentist", "numb mouth", "numb face",
                 "jaw", "fillings", "cocaine", "numb fingers", "numb toes", "numb hands",
                 "kill myself", "suicide", "suicidal", "end it all", "end my life",
                 "hurt myself", "self harm", "self-harm", "cut myself", "harm myself",
                 "not want to be here", "better off dead", "dont want to live",
                 "don't want to live", "want to die", "no point going on", "cant go on",
                 "this afternoon", "after lunch", "the afternoon dip", "afternoon dip",
                 "mid afternoon", "mid-afternoon", "late afternoon"),
          guard=lambda understood: (_the_mood_is_the_persons(understood)
                                   and _not_a_line_about_how_to_tell_the_doctor(understood))),

    entry("blocked-nose", (("nose", "sinuses", "sinus")
                           + said("stuffy", "bunged up", "blocked up", "congested"),
                           ("blocked", "blocked up", "bunged", "bunged up", "stuffy", "stuffed",
                            "congested", "congestion", "cant breathe", "can't breathe",
                            "struggling to breathe", "hard to breathe",
                            "finding it hard to breathe", "hard to breathe through",
                            "cant breathe through", "can't breathe through",
                            "cannot breathe through", "barely breathe", "trouble breathing")),
          "A blocked nose is swollen lining and mucus, so the thing that helps is shrinking the "
          "lining: a saline rinse or spray, steam from a hot shower, and a decongestant spray from "
          "a pharmacist for up to three days (longer and it bounces back). Sleep propped up and "
          "drink more than usual. See a GP if it lasts more than three weeks, if one side is "
          "blocked with bleeding, or if you have face pain and a temperature.",
          avoid=("dog", "cat", "puppy", "kitten", "child", "children", "baby", "toddler",
                 "car", "engine", "sink", "pipe", "drain", "toilet")),

    entry("runny-nose", (("nose", "sinuses", "sinus", "nostrils") + said(
                              "runny", "streaming", "dripping", "snotty", "sniffly"),
                          ("runny", "running", "runs", "streaming", "streams", "drips",
                           "dripping", "drippy", "keeps running", "keep running", "wont stop",
                           "won't stop", "wont stop running", "won't stop running", "sniffles",
                           "sniffing", "sneezes", "sneezing", "snot", "snotty", "dribbling")),
          "A runny nose is the lining making extra mucus to flush out a cold or an allergen, so "
          "saline spray or a salt-water rinse, steam from a shower and a decongestant spray for up "
          "to three days are what settle it. An antihistamine helps if it itches and sneezes too. "
          "See a GP if it is one-sided and bloodstained, lasts more than three weeks, or comes with "
          "face pain and a temperature.",
          avoid=PETS + ("child", "children", "kid", "kids", "baby", "babies", "toddler",
                        "ring", "piercing", "stud", "glasses", "spectacles", "slide", "bleed",
                        "bleeding", "blood", "broken", "broke", "smell", "smells", "smelly",
                        "stuffed", "stuffy", "blocked", "bunged", "congested", "congestion",
                        "surgery", "operation",
                        "covid", "coronavirus", "corona virus", "lateral flow", "pcr test",
                        "positive", "negative")),

    entry("earache", (("ear", "ears",
                       "earache", "ear ache", "ear-ache"),
                      ASK_ABOUT +
                      ("hurts", "hurt", "hurting", "ache", "aches", "aching", "pain", "painful",
                       "sore", "throbbing",
                       "bad", "really bad", "bad now", "is bad", "worse", "woke me", "kept me up")),
          "Earache in an adult is usually a cold or a sore throat spreading to the middle ear, and "
          "it settles in a few days: paracetamol or ibuprofen at the dose on the pack, a warm "
          "flannel over it, and don't poke anything in. See a GP if it lasts more than three days, "
          "if there is discharge from the ear, or if you also have a high temperature or swelling "
          "behind the ear.",
          avoid=("ringing", "tinnitus", "buzzing", "blocked", "wax", "itchy", "itch", "swim",
                 "swimmer", "child", "children", "baby", "toddler", "kid", "dog", "cat",
                 "piercing", "headphones", "phone",
                 "clean", "cleaning", "cleaned", "cotton", "cotton bud", "cotton buds",
                 "bud", "buds", "q-tip", "qtip", "olive oil", "drops", "syringe",
                 "syringing", "unblock", "unblocking", "water in my ear", "water in the ear",
                 "cant hear", "can't hear", "hearing", "hear", "deaf", "deafness",
                 "pressure", "eustachian"),
          bias=1),

    entry("start-again-exercise", (("start", "starting", "again", "back into", "get back",
                                    "restart", "havent", "haven't", "years", "after a break"),
                                   ("exercise", "exercising", "gym", "working out", "workout",
                                    "training", "running", "fit", "fitness", "active")),
          "Start with two walks a week you could hold a conversation through, 20 minutes each, and "
          "add five minutes a week rather than a new plan: after years off, the first month is "
          "about the habit and the tendons, not the heart. Add two short strength sessions (sit to "
          "stand, a push, a pull) once the walking feels easy, and expect soreness for a day or "
          "two, not for a week. If you have a heart condition, joint trouble or are over 60 and "
          "have not exercised in years, a word with a GP first is sensible.",
          avoid=("story", "stories", "poem", "poems", "rhyme", "rap", "song", "lyrics",
                 "how do i start running", "couch to 5k", "knee", "knees", "membership",
                 "cost", "price", "how much", "dog", "puppy", "running", "run", "jogging",
                 "jog", "5k", "10k", "marathon",
                 "swim", "swims", "swimming", "pool", "laps",
                 "at 50", "at 55", "at 60", "at 65", "at 70", "in my 50s", "in my 60s",
                 "older", "pensioner", "elderly",
                 "my train", "the train", "by train", "train was", "train to", "train from",
                 "train ticket", "train fare", "train times", "train station", "trains",
                 "platform", "railway", "rail", "cancelled", "canceled", "cancellation",
                 "delay repay", "strike",
                 "potty", "nappy", "nappies", "toilet training", "toddler", "baby", "babies",
                 "child", "children", "kids", "nursery", "son", "daughter",
                 "bus", "buses", "coach", "coaches", "ticket", "tickets", "fare", "fares",
                 "train ticket", "train tickets", "on the train", "by train", "bus pass",
                 "cat", "cats", "kitten", "kittens", "pet", "pets", "vet", "vets", "rabbit",
                 "hamster", "guinea pig", "budgie", "parrot", "horse", "pony", "fish", "puppies"),
          bias=2,
          guard=lambda u: any(cue in _the_line(u) for cue in (
              "again", "back into", "back to", "get back", "getting back", "got back",
              "restart", "re-start", "havent", "haven't", "not exercised in", "not done",
              "after a break", "after years", "after a long", "years off", "years since",
              "since school", "used to", "out of shape", "stopped exercising"))),

    entry("decaf-pregnancy", (("decaf", "decaff", "decaffeinated"),
                              ("pregnant", "pregnancy", "expecting")),
          "Decaf is fine in pregnancy: a mug of it has well under 10mg of caffeine against about "
          "100mg in the ordinary cup, so it counts towards the 200mg a day but only just. Keep "
          "the total to about 200mg a day - two mugs of instant coffee, one filter coffee, or two "
          "to three cups of tea - and let decaf be the cup that is habit rather than need, such as "
          "the evening one.",
          bias=2),

    entry("caffeine-pregnancy", (("pregnant", "pregnancy", "expecting"),
                                 ("coffee", "caffeine", "tea", "espresso", "latte", "energy drink",
                                  "cola", "coke",
                                  "decaf", "decaff", "decaffeinated")),
          "While pregnant, keep caffeine to about 200mg a day: that is two mugs of instant coffee, "
          "or one filter coffee, or two to three cups of tea, and cola and energy drinks count too. "
          "It is not that a little is dangerous, it is that the baby clears caffeine slowly and "
          "lots of it is linked to a lower birth weight. Switch some cups to decaf or water rather "
          "than cutting it out, and ask your midwife if you are unsure.",
          avoid=("alcohol", "wine", "beer", "drink-drive", "dog", "cat", "puppy",
                 "my baby", "a baby", "the baby", "baby need", "baby have", "baby weigh",
                 "feed", "feeding", "milk", "formula", "burp", "tummy time", "nappy", "sleep"),
          bias=1),

    entry("contact-lens-dry",
          (("contact lens", "contact lenses", "contacts", "lens", "lenses"),
           ("dry", "drying", "dries", "uncomfortable", "scratchy", "gritty", "irritated",
            "irritating", "sore", "hurts", "hurting", "feels", "feel", "itchy", "blurry",
            "sticking", "sticking to", "watery")),
          "A lens that feels dry or scratchy is usually the lens itself: take it out, rinse it in "
          "the proper solution (never tap water), soak it as long as the maker says and put it "
          "back, or start a fresh one for the day. Rewetting drops made for lens wearers help "
          "through the afternoon, and heating, screens and air conditioning dry them out more than "
          "anything else. Leave the lenses out for a day if the eye still feels gritty. If the eye "
          "is red or painful with the lens in, take it out and get it looked at the same day - a "
          "red eye in a lens wearer is the one that needs checking quickly.",
          avoid=("camera", "photography", "photo", "phone", "glasses", "spectacles", "frame",
                 "frames", "telescope", "microscope", "binoculars", "sun glasses", "sunglasses",
                 "magnifying", "projector", "headlight", "child", "children", "baby", "toddler",
                 "dog", "cat",
                 "red eye", "red eyes", "pink eye", "lost", "lost in my eye", "behind my eye",
                 "stuck", "wont come out", "will not come out", "cant get it out", "wont budge",
                 "went behind", "gone behind", "folded", "up under", "disappeared",
                 "cannot get it out", "can't get it out"),
          bias=1),
    entry("water-retention",
          (("water", "fluid"),
           ("retaining", "retain", "retention", "holding on", "holding", "build up", "building up",
            "puffy", "puffiness", "puff up")),
          "Water retention is usually salt and sitting still: cut the salt and processed food for "
          "a week, move your ankles through the day, and put your feet up above heart "
          "height for twenty minutes in the evening. Warm weather and some medicines (ibuprofen, "
          "the pill) do it too. See a GP if one leg is more swollen, if you are short of breath "
          "lying flat, or if the skin dents when you press it.",
          avoid=("bottle", "bottles", "drink", "drinking", "drinks", "hot water", "boiler", "tap",
                 "leak", "leaking", "leaks", "plants", "plant", "flowers", "garden", "pool",
                 "swim", "bath", "swimming", "dog", "cat", "baby", "child", "toddler",
                 "toilet", "cistern", "tank", "pipe", "pipes", "radiator", "radiators", "drain",
                 "drains", "ceiling", "wall", "walls", "damp", "sink", "ear", "ears", "kettle",
                 "one leg", "swollen calf", "swollen leg", "hot and swollen", "red and hot",
                 "flight", "pregnant", "pregnancy")),
    entry("throat-clearing",
          (("throat", "voice"),
           ("clearing", "clear it", "clearing it", "clear my throat", "clearing my throat", "ahem",
            "catarrh", "phlegm", "hawking", "tickle", "tickly")),
          "Constant throat clearing is usually a drip down the back of the nose, from a cold, an "
          "allergy or a blocked nose - or dry air, or reflux, or plain habit. Rinse the nose with "
          "salt water or try a steroid spray, and sip water instead of clearing. See a GP if it "
          "lasts weeks, if the voice changes, or if you can feel a "
          "lump in the neck.",
          avoid=("sore throat", "sore", "tonsil", "tonsils", "strep", "swallow", "swallowing",
                 "cough", "coughing", "cold", "flu", "baby", "child", "toddler", "my son",
                 "my daughter")),
    entry("rash",
          (("rash", "rashes", "blotches", "blotchy", "hives", "spots", "red patches", "itchy skin"),
           ("arm", "arms", "leg", "legs", "chest", "back", "stomach", "skin", "itchy", "itch",
            "spreading", "spread", "appeared", "came up", "sudden", "all over", "red",
            "have", "got",
            "get rid", "get rid of", "go away", "goes away", "clear up", "clears up",
            "treat", "treatment", "cream", "creams", "cure", "soothing", "calm it down")),
          "Most rashes are contact or heat: a new soap or washing powder, a plant, sweat, or a "
          "viral thing that fades in a few days. Cool the skin, skip perfumed products, and an "
          "antihistamine at night helps the itch; a thin layer of 1% hydrocortisone cream twice a "
          "day for up to a week settles a very itchy patch, but keep it off the face. "
          "Two rashes are not wait-and-see - one that does "
          "not fade when you press a glass on it, and one with a fever or a swollen face or lips - "
          "so get those seen the same day.",
          ask=("rash", "rashes", "blotches", "hives", "spots"),
          avoid=("baby", "babies", "child", "children", "toddler", "kid", "kids", "newborn",
                 "dog", "cat", "puppy", "kitten", "pet", "nappy", "nappy rash", "nappy cream",
                 "side effect", "antibiotics", "tablet", "tablets")),

    entry("skin-abscess",
          (("abscess", "abscesses", "boil", "boils", "carbuncle", "carbuncles", "skin infection",
            "infected lump"),
           ("leg", "legs", "arm", "arms", "thigh", "hip", "buttock", "buttocks", "bottom",
            "back", "side", "stomach", "belly", "hand", "hands", "finger", "fingers", "foot",
            "feet", "toe", "toes", "knee", "skin", "under the skin", "lump", "swollen",
            "painful", "hurts", "sore", "red", "hot", "treat", "treating", "drain", "draining",
            "head", "comes to a head", "come to a head", "popped", "pop", "at home", "home remedy")),
          "A skin abscess is a pocket of pus under the skin, and the treatment is to let it "
          "drain rather than squeeze it: hold a warm flannel on it for ten to fifteen minutes "
          "three or four times a day, keep the skin clean and dry, and take paracetamol or "
          "ibuprofen at the dose on the pack if it is sore. Do not squeeze, prick or cut it, "
          "because that pushes the infection deeper. See a GP promptly if it is getting bigger "
          "or more painful, if you have a fever or feel unwell, if it is on your face or hand, "
          "or if you have diabetes or a weakened immune system - those often need antibiotics or "
          "a small drainage. Ring 111 if the redness is spreading quickly, and 999 if you are "
          "confused, breathe fast or feel very ill.",
          ask=("leg", "legs", "arm", "arms", "thigh", "hip", "buttock", "buttocks", "bottom",
               "back", "side", "stomach", "belly", "hand", "hands", "finger", "fingers", "foot",
               "feet", "toe", "toes", "knee", "skin", "under the skin", "lump", "swollen",
               "painful", "hurts", "sore", "red", "hot", "treat", "treating", "drain", "draining",
               "head", "comes to a head", "come to a head", "popped", "pop", "at home", "home remedy"),
          avoid=("tooth", "teeth", "gum", "gums", "dental", "dentist", "jaw", "mouth",
                 "toothache", "wisdom", "filling", "denture", "dentures", "cheek", "face",
                 "eye", "throat", "breast", "pilonidal", "cyst", "acne", "spot", "spots",
                 "boiling water", "boiled water", "boiling hot", "boiling point", "boil the",
                 "boil an egg", "boil my", "boil rice", "boil potatoes", "boil wash",
                 "how long to boil", "how long do i boil", "kettle", "pan of", "saucepan",
                 "spilt", "spilled", "poured", "scald", "scalded", "scalding", "steam", "steamed",
                 "burn", "burns", "burnt", "burned", "burning", "hot water bottle", "hob", "oven",
                 "grill", "iron", "radiator"),
          bias=2),

    entry("scald-boiling-water",
          (("boiling water", "boiling hot water", "boiling pan", "pan of boiling",
            "pot of boiling", "just boiled", "just-boiled", "kettle",
            "hot oil", "oil splashed", "splashed with oil", "splashed with hot oil",
            "hot oil splashed", "splashed by hot oil", "hot fat", "fat splashed",
            "splashed with fat", "splashed with hot fat", "hot fat splashed"),
           ("hand", "hands", "finger", "fingers", "thumb", "thumb", "foot", "feet", "toe",
            "toes", "arm", "arms", "wrist", "wrist", "leg", "legs", "ankle", "thigh", "knee",
            "chest", "stomach", "tummy", "belly", "lap", "face", "chin", "shoulder", "neck",
            "back", "baby", "child", "toddler", "kid")),
          "Twenty minutes under cool running water, starting now, is the thing that decides how "
          "it heals - not ice, not butter, not a cream. Take off a ring or a watch and any "
          "clothing that is not stuck to it, then cover the burn loosely with cling film or a "
          "clean non-fluffy cloth and keep the rest of the body warm. Paracetamol or ibuprofen "
          "helps the soreness. Get it looked at the same day if it blisters, is bigger than the "
          "person's palm, or is on a hand, foot, face or anywhere on a child - those go to a "
          "walk-in or A&E rather than waiting.",
          avoid=("egg", "eggs", "pasta", "rice", "potato", "potatoes", "noodle", "noodles",
                 "vegetable", "vegetables", "how long", "bacteria", "sterilise", "sterilize",
                 "purify", "purified", "drink", "drinking", "descale", "limescale", "hard water",
                 "boiling point", "temperature", "freezes", "freeze", "noisy", "noise",
                 "not working", "broken", "fuse", "switch", "sugar", "salt",
                 "frying", "fry", "fried", "deep fry", "deep fried", "how hot", "degrees",
                 "smoke point", "which oil", "what oil", "reuse", "reusing", "used oil",
                 "dispose", "dispose of", "chips", "chip pan", "oil for", "splash guard",
                 "by hand", "hand wash", "hand-wash", "handwash", "handled", "handle", "lid",
                 "spout", "element", "filter", "cleaning", "clean", "descaling", "garden",
                 "cupboard", "back of", "shelf"),
          bias=1),

    entry("stitches-out",
          (("stitches", "stitch", "sutures", "suture", "stitches out", "staple", "staples"),
           ("how long", "how many days", "come out", "comes out", "coming out",
            "take out", "taken out", "taking out", "remove", "removed", "removing",
            "stay in", "stays in", "left in", "leave in", "leave them in", "left them in",
            "leave stitches in", "leaving stitches in", "leaving them in",
            "dissolve", "dissolvable", "dissolving",
            "when do they", "when do my", "when do the", "when do these", "when will they",
            "when will my", "when will the", "when can they", "when can my", "when are they",
            "when are my", "when should i take", "when should they", "when out", "when is it out",
            "how long until", "how long before", "how long till")),
          "They come out on the body's own timetable: five days on the face or neck, seven to "
          "ten on the scalp, chest or belly, ten to fourteen on an arm or a leg, and around two "
          "weeks over a joint. A nurse at the surgery or the walk-in takes them out, usually "
          "with no appointment, and leaving them in too long is what leaves a ladder of marks. "
          "Keep them dry for the first day or two and do not pick at the scab. Dissolvable "
          "stitches and skin glue need no appointment: the glue peels off by itself in about a "
          "week to ten days, and the stitches under the skin go in two to three weeks.",
          guard=_a_wound_not_a_cramp,
          avoid=("infected", "infection", "pus", "red streak", "smelly", "hot to touch",
                 "should i get", "do i need", "needs stitches", "need stitches",
                 "is it infected",
                 "in stitches", "had me in", "having me in", "left me in", "hysterics",
                 "laughing", "a good laugh",
                 "stapler", "staplers", "paper", "papers", "sheet", "sheets", "paperwork",
                 "documents", "magazine", "magazines", "booklet", "office", "gun",
                 "opened again", "opened up", "reopened", "re-opened", "came apart", "come apart",
                 "split open", "burst open", "fell open", "come undone", "came undone", "undone",
                 "drive", "driving", "shower", "showering", "bath", "bathing", "swim", "swimming",
                 "gym", "exercise", "work out", "workout", "football", "run", "running"),
          bias=1),

    entry("cut-needs-stitches",
          (("stitches", "stitch", "suture", "sutures", "glued", "glue"),
           ("need", "needs", "needed", "get", "getting", "should", "could", "might", "wound",
            "cut", "cuts", "gash", "cutting", "gaping", "deep", "close", "closed", "nurse",
            "hospital", "a&e", "walk-in", "walk in", "how do i know",
            "opened again", "opened up", "reopened", "re-opened", "split open", "came apart",
            "come apart", "fallen apart", "fell apart", "come undone", "came undone", "undone",
            "opened", "split", "burst")),
          "A cut needs closing properly if the edges fall apart when you let go, if it is longer "
          "than about 2cm, if it is on the face, a hand or over a joint, or if it is a bite or has "
          "grit in it: go to a walk-in or A&E, ideally within six to eight hours and sooner for a "
          "face wound. A clean, straight cut shorter than that holds with a plaster or "
          "steri-strips. Press a clean cloth on it hard for ten minutes first so the bleeding "
          "stops, and check your tetanus is up to date.",
          avoid=("how long", "come out", "comes out", "coming out", "take out", "taken out",
                 "remove", "removed", "stay in", "stays in", "left in", "leave in",
                 "dissolve", "dissolvable", "dissolving"),
          guard=_a_wound_not_a_cramp),


    entry("cut-infected",
          (("infected", "infection", "infections", "septic", "pus", "pusy", "pus-filled",
            "puss", "oozing", "weeping", "red streak", "red streaks", "yellow", "green",
            "crusty", "crusting", "smelly", "smell", "hot to touch", "gone hot",
            "red", "redder", "redness", "swollen", "swelling", "warm", "warmer"),
           ("cut", "cuts", "wound", "wounds", "graze", "grazes", "scab", "scabs", "gash",
            "scratch", "scratches", "scrape", "tattoo", "tattoos", "piercing", "piercings",
            "stitch", "stitches", "suture", "sutures", "staple", "staples",
            "finger", "hand", "thumb", "knee", "shin", "arm", "leg", "foot", "toe")),
          "A wound that is infected shows up two or three days after the injury: the redness "
          "spreads outwards (more than about a centimetre a day), the skin round it is hot and "
          "tender, it swells, and there is pus or a yellow crust, or the pain gets worse instead "
          "of better. Soak it in warm salty water for ten minutes twice a day, keep it covered, "
          "and do not squeeze it. See a GP the same day for spreading redness or pus; a red "
          "streak running up the arm or leg, a fever, or feeling shivery and ill is 111 today, "
          "because that is when antibiotics are needed rather than later.",
          ask=(("cut", "cuts", "wound", "wounds", "graze", "grazes", "scab", "scabs", "gash",
                "scratch", "scratches", "scrape", "tattoo", "tattoos", "piercing", "piercings",
                "infection", "infected", "infections", "septic", "pus", "pusy", "puss",
                "pus-filled", "oozing", "weeping", "streak", "streaks", "crust", "crusty",
                "crusting", "smell", "smelly", "hot to touch", "gone hot",
                "stitch", "stitches", "suture", "sutures", "staple", "staples"),),
          avoid=("chest", "throat", "ear", "ears", "urine", "urinary", "uti", "kidney",
                 "sinus", "sinuses", "tooth", "teeth", "gum", "gums", "dental", "dentist",
                 "abscess", "boil", "boils", "cyst", "acne", "spot", "spots", "chickenpox",
                 "chicken pox", "nappy", "baby", "babies", "newborn", "toddler", "child",
                 "children", "kid", "kids", "dog", "cat", "bitten", "bite", "animal",
                 "petrol", "diesel", "gas", "gasoline", "fuel", "exhaust", "smoke", "bleach",
                 "ammonia", "paint", "thinners", "drains", "drain", "sewage", "burning",
                 "oil", "kerosene", "paraffin",
                 "diabetes", "diabetic", "ulcer", "ulcers", "operation", "surgery",
                 "caesarean", "c-section", "stitches out"),
          bias=2),

    entry("infected-finger",
          (("whitlow", "whitlows", "paronychia", "felon", "nail infection", "infected nail",
            "fingernail infection", "finger infection", "infected finger", "thumb infection",
            "infected thumb", "pus under the nail",
            "red", "redness", "hot", "throbbing", "throbs", "throb", "swollen", "swelling",
            "puffy", "tender", "sore", "painful", "pus", "pussy", "abscess", "infected",
            "infection", "septic", "spreading", "streak", "streaks"),
           ("whitlow", "whitlows", "paronychia", "felon", "nail infection", "infected nail",
            "finger", "fingers", "thumb", "thumbs", "fingernail", "fingernails", "nail",
            "nails", "fingertip", "fingertips", "cuticle", "cuticles")),
          WHITLOW_REPLY,
          guard=_names_a_finger,
          report=True,
          avoid=("typing", "type", "typed", "keyboard", "mouse", "laptop", "wrist",
                 "wrists", "carpal", "cut", "cuts", "wound", "wounds", "gash", "graze",
                 "fungal", "fungus", "funguses", "yellow", "thick", "thickened", "crumbly",
                 "lifting", "lifted", "black nail", "athletes foot", "athlete's foot",
                 "scald", "burn", "burns", "burnt", "caught in", "caught", "slammed",
                 "door", "hammer", "hit my", "banged", "bang", "toe", "toes", "toenail",
                 "toenails", "broken", "broke", "fracture", "sprain", "sprained", "numb",
                 "tingling", "cold", "blue", "arthritis", "nail polish", "polish",
                 "fungal", "fungus", "yellow", "crumbly", "thick", "thickened", "discoloured",
                 "discolored", "brittle", "flaky",
                 "paint my nails", "painted nails", "manicure", "pedicure", "bitten nails",
                 "stop biting", "nail biting", "nail varnish", "brittle", "peeling",
                 "dog", "cat", "puppy", "kitten", "bitten", "bite", "insect", "bee",
                 "wasp", "tick", "splinter"),
          bias=1),

    entry("aches-in-the-cold",
          (("joints", "joint", "knees", "knee", "hips", "hip", "shoulders", "shoulder", "hands",
            "arthritis", "bones", "old injury"),
           ("cold", "colder", "winter", "weather", "damp", "rain", "freezing", "frost",
            "cold weather", "in the cold")),
          "Cold does not damage joints, it makes them feel stiffer: muscles and the fluid inside "
          "the joint move less freely when you are cold, so an old injury or arthritis aches more "
          "in winter. Keep it moving - a walk, a warm shower in the morning, layers over the knees "
          "- and see a GP if a joint is hot, swollen, locking or waking you at night.",
          ask=("joints", "joint", "ache", "aching", "hurts", "stiff", "stiffness", "arthritis",
               "bones"),
          bias=1,
          avoid=("flu", "influenza", "cold symptoms", "runny nose", "sore throat", "cough",
                 "sneezing", "dog", "cat", "car", "engine")),


    entry("tailbone-pain",
          (("tailbone", "tail bone", "coccyx", "bottom of my spine", "base of my spine",
            "bum bone"),
           ("hurt", "hurts", "hurting", "ache", "aches", "aching", "sore", "pain", "painful",
            "sitting", "sit", "bruised", "feel", "killing", "kills", "agony", "throbbing",
            "throbs", "pounding")),
          "Tailbone pain is usually from a knock, a long sit or childbirth, and there is nothing "
          "to strap up: it settles over a few weeks. Sit on a soft cushion or lean forward onto "
          "the fronts of your thighs rather than taking the weight on it, stand up often, and use "
          "paracetamol or ibuprofen if you can. See a GP if a fall made it much worse, if you "
          "cannot sit at all, if there is numbness, or if it is still there after eight weeks.",
          avoid=("dog", "cat", "puppy", "kitten", "baby", "child", "toddler", "bike", "bicycle",
                 "horse", "saddle", "chair", "car seat")),

    entry("voice-loss",
          (("voice", "hoarse", "hoarseness", "croaky", "croak", "laryngitis", "raspy", "husky",
            "gravelly"),
           ("lost", "losing", "gone", "went", "hoarse", "croaky", "raspy", "husky", "gravelly",
            "shouted",
            "shouting", "screaming", "singing", "sang", "cold", "laryngitis", "whisper", "talking",
            "speaking", "sore throat", "days", "weeks", "disappeared")),
          "A voice that has gone is usually laryngitis: the vocal cords are swollen from a cold, "
          "or from shouting, singing or a smoky room. Rest it - sip water often and do not "
          "whisper, which strains it more than talking does - and steam helps the rawness. It is "
          "usually back within one to two weeks. See a GP if it lasts more than three weeks, if "
          "you cannot swallow, or if you have a lump in the neck or trouble breathing.",
          avoid=("better", "improve", "training", "lessons", "teacher", "pitch", "range",
                 "karaoke", "voice note", "voice message", "voice memo", "recorder", "alexa",
                 "speaker", "assistant", "baby", "child", "toddler", "dog", "cat")),

    entry("jaw-click",
          (("jaw", "jawbone", "jaw joint", "tmj", "temple"),
           ("click", "clicks", "clicking", "clicked", "clunk", "pop", "pops", "popping", "grind",
            "grinding", "grind", "lock", "locked", "hurts", "hurt", "ache", "sore", "pain", "tight",
            "chew", "chewing", "eating", "yawn", "wide", "stiff",
            "crack", "cracks", "cracking", "cracked", "noisy", "noise", "noises",
            "snap", "snaps", "snapping", "crunch", "crunching", "crunchy", "grates", "grating",
            "sound", "sounds", "sounding", "hurting")),
          "A jaw that clicks on its own is usually harmless, but if it comes with pain or "
          "stiffness it is the jaw joint (TMJ) complaining: eat softer food for a couple of "
          "weeks, stop chewing gum and biting your nails, hold a warm flannel against it, and "
          "avoid opening wide while it settles. A dentist can check the bite, give you exercises "
          "and fit a night guard if you grind. See someone sooner if the jaw locks open or shut, "
          "or if it is very painful. Jaw pain with chest pain or breathlessness is an emergency "
          "- call 999.",
          avoid=("chest", "arm", "arms", "sweating", "sweaty", "breathless", "breathlessness",
                 "heart", "stroke", "baby", "child", "toddler", "dog", "cat", "vice", "clamp",
                 "wrench", "wire", "strippers", "pliers",
                 "jawline", "makeup", "beard", "hair", "shave", "razor")),
    entry("morning-sneezing", (("sneezing", "sneeze", "sneezes"), ("every morning", "in the "
                                                                     "morning", "each morning",
                                                                     "when i wake", "wake up",
                                                                     "always", "every day")),
          ("Sneezing first thing is usually the nose reacting to the change in temperature, dust "
           "mites in the bedding or a dry room, rather than an allergy to anything outside. Wash "
           "the bedding at 60C, air the room and try a saline rinse; an antihistamine at night "
           "helps if it goes on. Itchy eyes and a blocked nose in spring point to hay fever."),
          avoid=("dog", "cat", "pet", "pepper", "mustard")),
    entry("sneezing-a-lot", (("sneezing", "sneeze", "sneezes", "sneezing fits"),
                             ("a lot", "lots", "keep", "keeps", "kept", "cant stop",
                              "can't stop", "non stop", "nonstop", "stop", "how", "why",
                              "always", "all day", "every day", "constant", "constantly",
                              "often", "so much", "fits", "much", "days", "sneezing")),
          "A sneeze is the nose throwing out something that irritates its lining, and what helps "
            "depends on which of the two usual causes it is. If your eyes or the roof of your "
            "mouth itch, it is an allergy: a once-a-day antihistamine started before you go out, a "
            "saline rinse, windows shut in pollen season and a shower before bed. If it came on "
            "with a sore throat and a temperature, it is a cold and settles in a few days: "
            "paracetamol, water and rest. Don't hold a sneeze in with the nose pinched - it can "
            "push air into the ear. See a GP if it is one-sided, bloodstained, or has gone on for "
            "weeks.",
          avoid=("dog", "cat", "puppy", "kitten", "pet", "pets", "pepper", "mustard", "dust",
                 "child", "children", "kid", "kids", "baby", "toddler", "my son", "my daughter",
                 "machine", "sneeze guard", "hay bale", "hay")),
    entry("asthma", (("wheeze", "wheezing", "wheezy", "asthma", "asthmatic", "tight chest"),
                     ("run", "running", "exercise", "cold", "night", "breath", "breathing",
                      "chest", "cough", "when i")),
          ("Wheezing that comes on with running, cold air or at night is asthma until proven "
           "otherwise: see a GP, who will listen to your chest and may give you a blue reliever "
           "inhaler plus a brown preventer steroid inhaler. Use the reliever two puffs through a "
           "spacer when tight, and if it is needed more than three times a week the preventer needs "
           "turning up. Blue inhaler not lasting four hours, or lips going blue, is 999."),
          avoid=("dog", "cat", "puppy", "engine", "car", "fan", "boiler", "pipe", "door")),
    entry("eye-infection", (("eye", "eyes", "stye", "styes"),
                           ASK_ABOUT + ("stye", "have a stye", "has a stye", "got a stye",
                            "eyelid", "lid",
                            "sticky", "red", "pink", "infection", "gunge", "crusty",
                            "watering", "conjunctivitis", "itchy", "swollen",
                            "swollen eyelid", "eyelid is swollen", "eyelid swollen", "swollen lid",
                            "lid is swollen", "puffy eyelid", "eyelid has a", "lump on my eyelid",
                            "bump on my eyelid", "spot on my eyelid", "eyelid hurts")),
          _eye_reply,
          guard=not_keeping_an_eye_on_it,
          avoid=("screen", "screens", "monitor", "phone", "laptop", "tv", "test", "tested",
                 "glasses", "contact lens solution", "makeup", "shadow")),
    entry("glass-eye-sore",
          (("glass eye", "false eye", "prosthetic eye", "artificial eye", "eye prosthes",
            "prosthetic socket"),
           ("sore", "hurts", "hurting", "painful", "pain", "red", "irritated", "uncomfortable",
            "dry", "crusty", "gunge", "discharge", "clean", "care", "take it out", "remove",
            "how do i", "what can i", "itchy", "itches", "itch", "itching", "swollen",
            "keeps",
            "keeps coming out", "keeps falling out", "coming out", "comes out", "falls out",
            "falling out", "fell out", "wont stay",
            "loose", "doesnt fit", "not fitting", "does not fit")),
          _glass_eye_out,
          avoid=("window", "windows", "windscreen", "windscreens", "pane", "test", "tested",
                 "screen", "screens",
                 "fight", "fights", "fighting", "punched", "punch", "punching", "elbow", "elbowed",
                 "headbutt", "headbutted", "hit me", "hit in the", "black eye", "blacked my eye",
                 "banged my eye", "fell on my", "assault", "mugged", "bar fight"),
          bias=2),
    entry("prosthesis-sore",
          (("prosthetic leg", "prosthetic limb", "prosthetic arm", "prosthetic hand",
            "prosthetic foot", "prosthetic knee", "leg prosthesis", "limb prosthesis",
            "prosthetics", "prosthesis", "prosthetic", "my stump", "false leg", "artificial leg",
            "artificial limb", "false limb", "artificial arm", "artificial hand", "false arm",
            "false hand", "false foot", "artificial foot"),
           ("sore", "hurts", "hurting", "painful", "pain", "rubs", "rubbing", "rubbed", "aches",
            "aching", "uncomfortable", "blister", "blisters", "chafing", "red", "swollen",
            "smell", "smelly", "sweaty", "itchy", "itches", "how do i", "what can i", "care",
            "clean", "wash", "washing", "washed", "how often", "wearing", "worn", "take it off",
            "keeps", "keeps coming loose", "loose",
            "wobbly", "cold", "numb", "tingling", "tight", "tightens", "heavy",
            "giving way", "gives way", "gave way", "buckling", "buckles", "locks", "locking",
            "collapses", "folds under", "knee goes",
            "shower", "showering", "bathe", "bath", "swim", "swimming", "wet",
            "squeak", "squeaking", "squeaky", "creak", "creaking", "rattle", "rattling",
            "noisy", "clicking", "clicks",
            "bleeding", "bled", "bleeds", "blood")),
          _prosthesis_care,
          avoid=("eye", "eyes", "socket", "hearing aid", "denture", "dentures", "jaw", "teeth",
                 "tooth", "nose", "breast", "limping", "walk with a limp", "amputat",
                 "cushion", "pillow", "bra", "hair", "penis", "penile",
                 "red and hot", "hot and red", "hot and swollen", "swollen and hot", "red hot",
                 "fever", "temperature", "shivering", "infected", "infection", "pus", "septic",
                 "oozing", "discharge", "wound", "ulcer"),
          bias=5),
    entry("heavy-periods", (("period", "periods", "monthly", "bleeding"), ("heavy", "flooding",
                                                                         "clots", "soaking",
                                                                         "really bad", "normal",
                                                                         "too much", "long")),
          ("Heavy periods mean soaking a pad or tampon every hour for a few hours, clots bigger "
           "than a 50p coin, or bleeding over seven days; if that is most months, see a GP. Common "
           "causes are fibroids, an underactive thyroid and, in your forties, perimenopause. Iron "
           "tablets may be needed if you feel tired, and a hormonal coil or tranexamic acid "
           "usually lightens things a lot."),
          avoid=("car", "insurance", "cover", "sentence", "grammar", "history", "trial",
                 "class", "physics")),
    entry("young-flushes", (HOT_FLUSH_PHRASES, YOUNG_FLUSH_AGES),
          YOUNG_FLUSH_REPLY,
          avoid=NOT_A_FLUSH + A_MANS_SWEATS,
          bias=3),
    entry("hot-flushes", (HOT_FLUSH_PHRASES, HOT_FLUSH_SECOND),
          HOT_FLUSH_REPLY,
          avoid=NOT_A_FLUSH + A_MANS_SWEATS,
          bias=2),
    entry("hot-flushes-plain", (HOT_FLUSH_PHRASES,),
          HOT_FLUSH_REPLY,
          avoid=NOT_A_FLUSH + A_MANS_SWEATS,
          report=True),
    entry("hot-flushes-maybe", (("flushes", "flushing"), HOT_FLUSH_SECOND),
          HOT_FLUSH_REPLY,
          avoid=NOT_A_FLUSH + A_MANS_SWEATS),
    entry("is-this-the-menopause", (("menopause", "menopausal", "perimenopause"),
                                    ("am i", "could i be", "going through", "signs", "symptoms",
                                     "what are", "how do i know", "is it", "is that", "is this",
                                     "what if", "early", "stage", "then")),
          MENOPAUSE_SIGNS_REPLY,
          avoid=("hot flush", "hot flushes", "night sweats", "sweats at night", "flush",
                 "flushes", "flushed") + NOT_MY_OWN_BODY),
    entry("how-long-the-menopause-lasts",
          (("menopause", "perimenopause", "hot flushes", "night sweats"),
           ("how long", "last", "lasts", "years", "how many years", "duration", "finish",
            "over", "end", "worth it")),
          MENOPAUSE_HOW_LONG_REPLY,
          avoid=NOT_A_FLUSH + NOT_MY_OWN_BODY),
    entry("hrt", (("hrt", "hormone replacement", "hormone therapy"),
                  ("what", "whats", "is", "are", "safe", "safety", "should i", "worth", "risk",
                   "risks", "side effects", "start", "starting", "ask", "ask about", "need",
                   "help", "helps", "works", "work", "types", "tablet", "tablets", "patches",
                   "gel", "take", "taking", "any good", "only thing")),
          ("HRT replaces the oestrogen your body stops making, and it is the most effective "
           "treatment for hot flushes, night sweats and the broken sleep they cause: a tablet, "
           "patch or gel, plus a progestogen if you still have a womb. For most women under 60 "
           "the benefits outweigh the risks - the one that rises is breast cancer, about 4 extra "
           "cases per 1,000 women taking combined HRT for five years, and a GP weighs that "
           "against your own history. It works best started within 10 years of your last period, "
           "and it is not a lifelong sentence: many women stop after a few years."),
          avoid=("boiler", "heating", "car")),
    entry("dehydrated", (("dehydrated", "dehydration"), ("how do i know", "signs", "symptoms",
                                                         "am i", "i think", "feel", "is it",
                                                         "what are", "check")),
          ("The simplest signs are dark yellow pee, a dry mouth, tiredness and a headache: aim for "
           "pale straw urine, which is about six to eight glasses a day for most adults. Water, "
           "squash, tea and milk all count. If someone is confused, dizzy on standing, or has not "
           "peed for half a day, especially in the heat or with a bug, that needs a GP."),
          avoid=("kettle", "tea", "teabag", "teabags", "cup", "cups", "cook", "cooking",
                 "pasta", "rice", "soup", "gravy", "bottle", "tap", "bill", "leak", "boiler",
                 "plant", "plants", "fish tank", "garden", "swim", "pool", "bath")),
    entry("breast-lump", (("lump", "lumps", "lumpy"), ("breast", "nipple", "boob", "chest")),
          ("A new lump in the breast should be checked by a GP within a week or two, whatever your "
           "age - most turn out to be harmless cysts or fibroadenomas, and breast lumps are "
           "common. Go the same day if it comes with skin dimpling, a nipple turning in or "
           "bleeding, or a hard lump that does not move. Keep feeling for the other breast so you "
           "know what is normal for you."),
          avoid=("dog", "cat", "pet", "gravy", "sauce", "porridge", "coffee", "drain", "sugar",
                 "sand", "neck", "gland", "throat", "skin"),
          bias=1),
    entry("sore-breasts",
          (("breast", "breasts", "boob", "boobs", "nipple", "nipples"),
           ("sore", "soreness", "hurt", "hurts", "hurting", "pain", "pains", "painful", "ache",
            "aches", "aching", "tender", "tenderness", "heavy", "swollen", "uncomfortable",
            "before a period", "before my period", "before my period starts", "touch",
            "when i touch", "worried", "worry", "supposed to", "both")),
          ("Sore breasts are usually hormonal: both sides tender, heavy or a bit swollen in the "
           "week before a period, and easing once it starts. A bra that fits properly - worn at "
           "night too if they ache in bed - less caffeine and paracetamol or ibuprofen if you "
           "need them are usually enough, and an ice pack or a warm pack over the sore part "
           "helps. Pain in one spot that stays put, one breast that is red, hot or hard, a new "
           "lump, or any discharge or bleeding from the nipple is a GP appointment within a week "
           "or two; a breast that is red, hot and painful with a fever is 111 today, because "
           "that is mastitis and it wants antibiotics."),
          ask=("sore", "hurt", "hurts", "pain", "painful", "ache", "aching", "tender", "why",
               "normal", "what helps", "should i worry", "what can i take", "help"),
          avoid=("lump", "lumps", "lumpy", "shivery", "bleeding", "blood",
                 "discharge", "dimpling", "turning in", "breastfeeding", "breast feeding",
                 "feeding", "nursing", "baby", "milk", "pregnant", "chicken", "meat", "turkey",
                 "duck", "fish", "fillet", "stuffed", "skinless", "roast", "cook", "cooking",
                 "grill", "oven", "pan", "recipe", "dog", "cat")),
    entry("always-cold", (("cold", "body", "chilly", "freezing",
                           "warm"),
                          ("always", "all the time",
                           "constantly", "everyone else",
                           "so cold", "feel the cold",
                           "why am i", "even in summer",
                           "in summer", "all year",
                           "get warm", "getting warm", "to get warm", "cant get warm",
                           "can't get warm", "never warm", "not warm", "cant warm up",
                           "can't warm up", "never warms up", "hard to get warm")),
          ("Feeling cold all the time is usually real rather than imagined: an underactive "
           "thyroid, low iron or a low body weight all do it, and so does being thin, tired or "
           "short of sleep. Ask a GP for a thyroid test and a full blood count if it is new or "
           "getting worse; meanwhile eat regularly, keep moving and wear a layer more than the "
           "people around you."),
          avoid=("hands", "fingers", "feet", "toes", "car", "engine", "radiator", "boiler",
                 "flat", "house", "home", "room", "bedroom", "living room", "the heating",
                 "thermostat", "insulation", "damp", "windows", "window",
                 "weather", "outside", "for the house", "beer", "fridge", "freezer",
                 "house", "houses", "flat", "flats", "home", "my house", "the house", "home is",
                 "house is", "flat is", "bedroom", "bedrooms", "room", "rooms", "kitchen",
                 "bathroom", "garage", "conservatory", "living room", "shed", "sheds",
                 "outbuilding", "outbuildings", "loft", "attic", "cellar", "basement",
                 "hallway", "porch", "workshop", "caravan",
                 "sore", "flu", "virus", "shiver", "shivering", "a cold", "cold sore",
                 "getting colds", "get colds", "catch colds", "catching colds",
                 "cold every", "colds every", "always ill", "always sick", "constantly ill",
                 "sniffles", "runny nose", "sneezing", "sore throat",
                 "why is it so cold", "why is it cold", "why is it colder", "why is it freezing",
                 "why is it so freezing", "is it so cold"),
          guard=_not_on_the_warm_up),
    entry("dizzy", (("dizzy", "dizziness", "lightheaded", "light headed", "giddy",
                     "head rush", "head spins", "feeling faint", "feel faint",
                     "room spun", "the room spun", "room is spinning"),
                    ("how do i", "how can i", "stop", "get rid", "what helps", "what should i do",
                     "what do i do", "why", "keep", "always", "all the time", "feel",
                     "feeling", "get", "getting", "cure", "help", "worried", "normal",
                     "pale")),
          ("Sit or lie down the moment it starts, and stand up in two stages after: sit on the edge "
           "of the bed or the chair for a few seconds, then rise. Most light-headedness is the "
           "blood pressure dip on standing, low blood sugar, or not enough to drink - so have "
           "water and something to eat, and keep your fluids up in hot weather. Crossing your legs "
           "and squeezing, or clenching your fists, pushes the blood back up if it happens again. "
           "See a GP if it keeps happening, and ring 111 or 999 that day for dizziness with chest "
           "pain, a faint, weakness or numbness on one side, a bad headache, or slurred speech."),
          avoid=("spinning", "spins", "room spins", "vertigo", "in the morning", "every morning",
                 "when i wake", "first thing", "standing up", "stand up", "when i stand",
                 "after eating", "hangover", "drunk", "alcohol", "ride", "fairground",
                 "pregnant", "pregnancy", "period", "migraine", "car", "boat", "travel sick"),
          bias=1),

    entry("dizzy-morning", (("dizzy", "dizziness", "lightheaded", "light headed", "giddy"),
                            ("in the morning", "every morning", "morning", "when i wake",
                             "first thing", "waking up", "out of bed")),
          ("Dizzy first thing is usually low blood pressure on getting up, low blood sugar after "
           "a long night, or not enough to drink: sit on the edge of the bed for a minute, have "
           "water and breakfast, and it often settles. If the room spins when you turn over in "
           "bed, that is the crystals in the inner ear (BPPV) and a GP or physio can fix it with "
           "the Epley manoeuvre. See a GP if you faint, or get chest pain, or weakness on one side."),
          avoid=("stand", "standing", "stood", "after eating", "drunk", "hangover", "alcohol",
                 "ride", "fairground"), bias=1),
    entry("exercise-hangover", (("hangover", "hungover", "after drinking"),
                                ("run", "running", "jog", "gym", "workout", "work out", "exercise",
                                 "training", "train", "football", "match", "cycle", "cycling",
                                 "swim", "swimming", "heavy night", "night out")),
          ("An easy run or a light session is fine if you feel like it - keep it short, drink water "
           "before and after, and eat something first. Skip anything hard: alcohol leaves you "
           "dehydrated with a higher resting heart rate, so your usual pace feels twice as hard, "
           "and don't take ibuprofen before you run on a hangover."),
          bias=3),
    entry("fertility", (("pregnant", "conceive", "conceiving", "fertility", "fertile", "baby",
                         "ovulation", "getting pregnant", "fall pregnant"),
                        ("cant get", "can't get", "not getting", "trying for", "trying to",
                         "struggling", "how long", "years", "no luck", "nothing happening",
                         "help", "test", "when to", "track", "am i", "how do i check",
                         "check", "still fertile", "after 35", "at 40")),
          ("Trying for a baby is a wait of up to a year at under 35 and six months at 35 or over: "
           "have sex every two or three days rather than saving up, since timing is less exact than "
           "the apps suggest, and take 400mcg of folic acid daily. Cut alcohol and smoking right "
           "down. See a GP after a year of trying (six months at 35 or over, sooner if periods are "
           "very irregular or painful) - both of you, not just you."),
          avoid=("test is positive", "positive test", "im pregnant", "i'm pregnant", "morning sick",
                 "baby wont sleep", "baby not sleeping", "feeding", "weaning", "nursery",
                 "pushchair", "pram", "cot", "baby monitor", "teething", "colic",
                 "swim", "swims", "swimming", "pool", "pools", "lido", "bath", "sea", "beach",
                 "water", "nappy", "nappies",
                 "baby sleep", "babies sleep", "newborn sleep", "sleep through", "sleeps through",
                 "nap", "naps", "wake for a feed", "waking for feeds",
                 "the baby", "my baby", "our baby", "this baby", "new baby", "newborn",
                 "with a newborn", "look after the baby", "look after my baby", "nobody helps",
                 "no help with", "no one to help", "whos going to help"),
          guard=not_a_childs_age, bias=1),
    entry("testicle-pain", (("testicle", "testicles", "scrotum", "ball", "balls"),
                            ("pain", "hurts", "hurting", "ache", "aching", "swollen", "lump",
                             "tender", "sore", "what", "should")),
          ("Sudden bad pain in one testicle is an emergency - ring 999, or get to A&E - because a "
           "twist can only be saved in the first few hours. A dull ache that came on slowly, or a "
           "small lump, is usually a cyst, a varicocele or an infection and should be looked at by "
           "a GP within a few days rather than left. Do not wait to see if it settles."),
          avoid=("therapist", "kettlebell", "dumbbell", "stress ball", "games", "football")),
    entry("testicle-ache", (("testicle", "testicles", "scrotum", "ball", "balls", "bollock",
                             "bollocks"),
                            ("ache", "aches", "aching", "achy", "dull", "tender", "heavy",
                             "hurts", "hurting", "sore", "cycling", "cycle", "cycled", "bike",
                             "biking", "ride", "rode", "riding", "running", "run", "jog",
                             "jogging", "gym", "squats", "deadlifts", "rugby", "shaving",
                             "shaved", "sex", "hiking", "rowing")),
          ("A dull ache with no cause is more often a cyst, a varicocele or an infection than an "
           "emergency: supportive underwear and an anti-inflammatory help, and a GP should look at "
           "it within a couple of weeks rather than a wait and see. An ache that came on after a "
           "long ride, a run or a session in the gym is usually just the tubes being knocked "
           "about, and settles in a day or two. If it turns sudden and severe, or you are sick "
           "with it, that is the hospital the same day. In a boy or a teenager, ring 111 or the "
           "GP today rather than waiting the fortnight out: a child is the one who cannot afford "
           "to wait."),
          avoid=("therapist", "kettlebell", "dumbbell", "stress ball", "games", "football",
                 "sudden", "suddenly", "severe", "agony", "excruciating", "woke", "woken",
                 "sick", "vomiting", "vomit", "swollen", "swelling", "lump", "hard",
                 "bigger", "larger", "size", "kicked",
                 "kicks", "hit", "punched", "torsion", "twisted", "twisting",
                 "son", "sons", "boy", "boys", "child", "children", "kid", "kids", "lad", "lads",
                 "teenager", "teen", "teenage", "schoolboy", "nephew", "grandson", "year old",
                 "years old", "little boy", "young lad"),
          bias=1),
    entry("testicle-check", (("testicle", "testicles", "ball", "balls"),
                             ("how do i check", "how to check", "how can i check",
                              "how should i check", "check them", "check my balls",
                              "check my testicles", "self check", "self-exam", "self exam",
                              "examine them", "feel for lumps", "look for lumps")),
          ("Once a month, in a warm bath or shower when everything is relaxed, hold each testicle "
           "between the thumb and the first two fingers and roll it gently between them, feeling "
           "for a hard lump, a change in size or a heavy ache that was not there last month. It "
           "should feel smooth and firm, like a peeled egg, with the soft tube at the back. "
           "Anything new that is still there after two weeks is a GP appointment; sudden severe "
           "pain is the hospital the same day."),
          avoid=("therapist", "kettlebell", "dumbbell", "stress ball", "games"),
          bias=1),
    entry("athletes-foot-pharmacy", (("athletes foot", "athlete's foot", "fungal", "fungus",
                             "between my toes", "itchy feet", "smelly feet", "toes"),
                            ("what", "how", "helps", "treat", "get rid", "cure", "peeling",
                             "itchy", "cracked", "smell", "infection", "have", "got",
                             "i have")),
          ("A pharmacy terbinafine or clotrimazole cream clears athlete's foot in two to four "
           "weeks - keep using it a fortnight after the skin looks fine - and dry between the toes "
           "properly, wear cotton socks and change shoes a day on, a day off. Wash socks hot and "
           "don't share towels."),
          avoid=("nail", "nails", "toenail", "toenails", "fingernail", "fingernails",
                 "nail varnish", "gel nails", "manicure", "salon", "fake tan", "nail polish",
                 "false nails")),
    entry("cut-nails",
          (("nails", "nail", "fingernails", "fingernail", "toenails", "toenail", "nail clippers",
            "clippers", "nail scissors"),
           ("cut", "cutting", "trim", "trimming", "clip", "clipping", "short", "how do i",
            "how should i", "the right way", "properly", "straight", "file", "filing",
            "how often")),
          "Cut them straight across rather than down the sides, leave a millimetre or two of "
          "white, then round the two corners with a file so nothing catches on a sock. Do toenails "
          "after a bath, when the nail is soft, and keep them longer than you think: rounding a "
          "toenail drives the edge into the skin and gives you an ingrown one. Once a fortnight is "
          "plenty, and clippers beat scissors on a thick nail. See a GP if one side is red and "
          "painful with skin growing over it, or if a nail has gone thick and yellow.",
          avoid=("baby", "babys", "babies", "newborn", "infant", "toddler", "child", "kid", "son",
                 "daughter", "girl", "boy", "fungal", "fungus", "yellow", "thick", "thickened",
                 "crumbly", "crumbling", "discoloured", "discolored", "lifting", "ridges",
                 "paint", "polish", "varnish", "gel", "acrylic", "manicure", "salon", "biting",
                 "bitten", "chew", "chewing", "dog", "cat", "puppy", "kitten", "hamster", "vet",
                 "horse", "rabbit", "claw", "claws",
                 "ingrown", "ingrowing", "in growing", "grown into", "growing into",
                 "ingrown toenail", "ingrowing toenail", "treat", "podiatrist", "chiropodist",
                 "sore toe", "sore toenail", "red and painful"),
          guard=_the_nail_is_a_persons),
    entry("nail-fungus", (("toenail", "toenails", "fingernail", "fingernails", "nails", "nail",
                           "nail fungus", "fungal nail", "fungus on my nail"),
                          ("yellow", "thick", "thickened", "crumbly", "crumbling", "fungus",
                           "fungal", "discoloured", "discolored", "brown", "lifting",
                           "what", "how", "treat", "get rid", "help", "cure", "infection",
                           "have", "got", "i have")),
          ("A thick, yellow or crumbly nail is a fungal nail infection: a pharmacist can sell you "
           "an amorolfine nail lacquer for a mild one, and a GP can prescribe terbinafine tablets "
           "when several nails or most of a nail is affected. Either way it takes months, because "
           "the damaged nail has to grow out - file it thin, dry your feet properly and don't share "
           "clippers. A dark streak under the nail, or a nail lifting off, is a GP check."),
          avoid=("ridges", "ridge", "paint", "varnish", "polish", "gel", "acrylic", "fake",
                 "cut", "cutting", "trim", "trimming", "clip", "clipping",
                 "snapped", "broke", "filing", "hammer", "dog", "cat", "dent", "pitted",
                 "bitten", "biting", "slammed", "banged", "stubbed", "dropped", "bruise",
                 "bruised", "in the door", "kicked", "trapped", "hit it", "hit my",
                 "ingrown", "ingrowing", "in growing", "growing into", "grown into",
                 "into the skin", "into the side", "sore at the side", "red at the side",
                 "pus", "embedded", "pressing into"),
          guard=_the_nail_is_a_persons),
    entry("ingrown-toenail",
          (("ingrown toenail", "ingrowing toenail", "ingrown", "ingrowing", "ingrown nail",
            "nail growing into", "toenail growing into", "nail digging in", "nail pressed in"),
           ("what", "how", "do i do", "treat", "treatment", "help", "sore", "pain", "painful",
            "hurts", "hurting", "infection", "infected", "get rid", "should", "fix", "cut",
            "cutting", "trimming", "advice", "anything", "deal with", "have", "got",
            "is", "isnt", "now", "again", "bad", "better", "worse",
            "toenail", "nail", "toe")),
          ("An ingrown toenail is a nail edge pressing into the skin at the side: soak the foot in "
           "warm salty water for 10 to 15 minutes twice a day, cut the nail straight across rather "
           "than down the corners, and wear shoes with room in the toe - and don't cut a V in the "
           "middle, which does nothing. See a GP or podiatrist if it is badly painful, if the skin "
           "is red, hot or weeping pus, or if you have diabetes or poor circulation: they can take "
           "a wedge of nail away, and that is the fix that lasts."),
          avoid=("fungus", "fungal", "yellow", "crumbly", "black", "bruise", "bruised",
                 "dropped", "hammer", "stubbed", "kicked", "banged", "slammed", "fell off",
                 "falling off", "lifting off", "ridges", "paint", "polish", "varnish", "gel",
                 "acrylic", "manicure", "pedicure")),
    entry("nail-or-nail-fold",
          (("nail", "nails", "toenail", "toenails", "fingernail", "fingernails", "nail fold",
            "cuticle"),
           ("infected", "infection", "infections", "septic", "abscess", "pus", "pus-filled",
            "oozing", "weeping", "throbbing", "swollen", "swelling", "red", "hot", "angry",
            "inflamed", "is it", "looks bad", "gone bad")),
          ("If it has come up red, swollen and throbbing, especially with pus at the side or base "
           "of the nail, that is a bacterial infection of the nail fold (paronychia) and it is not "
           "the slow yellow fungus: soak it in warm salty water, don't squeeze it, and see a "
           "pharmacist or GP quickly because it often needs an antibiotic. A nail that is thick, "
           "yellow or crumbly, and has been for months, is the fungal one - that takes a lacquer "
           "or tablets and months while the nail grows out."),
          avoid=("ingrown", "ingrowing", "growing into", "grown into", "into the skin",
                 "into the side", "edge", "corner", "cut", "cutting", "trim", "trimming",
                 "clip", "clipping", "black", "bruise", "bruised", "snapped", "hammer", "door",
                 "stubbed", "kicked", "dropped", "fell off", "lifting off", "paint", "polish",
                 "varnish", "gel", "acrylic", "manicure", "pedicure", "yellow", "crumbly")),
    entry("nails-polish",
          (("nails", "nail", "fingernails", "fingernail", "toenails", "toenail", "manicure",
            "nail polish", "nail varnish", "gel nails", "acrylic nails"),
           ("paint", "painting", "polish", "varnish", "manicure", "base coat", "top coat",
            "dry", "drying", "smudge", "smudged", "chip", "chips", "chipping", "last longer",
            "make them last",
            "lumpy", "lumps", "streaky", "streaks", "bubbles", "bubbly", "uneven", "patchy",
            "came out", "goes on thick", "too thick", "dragging", "tacky", "tacky to")),
          ("Two thin coats beat one thick one, and a base coat stops the colour staining the "
           "nail: wipe each nail with remover first so there is no oil on it, paint from the "
           "middle of the cuticle outwards in three strokes, and give each coat 10 minutes so it "
           "sets instead of smudging. A fresh top coat every other day is what keeps a manicure "
           "looking new for a week."),
          avoid=("fungus", "fungal", "yellow", "thick", "crumbly", "ingrown", "ingrowing",
                 "sore", "pain", "painful", "hurts", "black", "bruise", "lifting", "fallen",
                 "remove", "removing", "take off", "taking off", "soak", "soaking", "peel",
                 "peeling", "gel", "acrylic", "extensions", "shellac",
                 "cut", "cutting", "trim", "trimming", "clippers", "too long",
                 "tin of paint", "emulsion", "gloss", "undercoat", "wall", "walls", "door",
                 "skirting", "fence", "wood", "metal", "car",
                 "off the table", "off a table", "on the table", "off the floor", "off the carpet",
                 "on the carpet", "spilled", "spill", "spilt", "stain", "stains", "stained",
                 "on my jeans", "out of clothing", "off my clothes", "off clothing",
                 "leaked", "leaking", "leak", "in my bag", "in the bag", "broke in my bag",
                 "smell", "smells", "smelling", "smells of", "smells like", "smelt",
                 "tastes", "taste", "tasting", "rancid", "gone bad", "gone off", "off",
                 "brewing", "brew")
                 + FOOD_SUBJECT
           ),
    entry("gel-nails-off",
          (("gel nails", "gel polish", "acrylic nails", "acrylics", "nail extensions",
            "shellac", "nails", "nail"),
           ("remove", "removing", "take off", "taking off", "soak", "soaking", "peel",
            "peeling", "off", "grow out", "growing out", "damaged")),
          ("Don't pick or peel it off - that takes the top layers of the nail with it and leaves "
           "it flaky for months: file the shiny surface, soak the nail in acetone for 10 to 15 "
           "minutes, then push the softened gel off gently with an orange stick. A salon soak-off "
           "is quick and cheap, and a fortnight's break between sets is what lets the nail recover."),
          avoid=("fungus", "fungal", "ingrown", "ingrowing", "sore", "pain", "yellow", "thick",
                 "black", "paint", "emulsion", "wall", "walls", "hand", "hands", "car",
                 "nails peeling", "nails are peeling", "nails keep peeling", "nails that peel",
                 "my nails peel", "stop my nails peeling", "peeling nails", "brittle",
                 "spilled", "spill", "spilt", "stain", "stains", "stained", "off the table",
                 "off a table", "on the table", "off the floor", "off the carpet", "on the carpet",
                 "on my jeans", "off my clothes", "off clothing", "off fabric"),
          bias=1),
    entry("glandular-fever",
          (("glandular fever", "glandular", "mono", "mononucleosis", "kissing disease",
            "epstein barr", "epstein-barr", "ebv"),
           ("how long", "last", "lasts", "lingering", "tired", "tiredness", "exhausted",
            "fatigue", "rest", "recover", "recovery", "sport", "sports", "football", "rugby",
            "gym", "exercise", "running", "spleen", "alcohol", "work", "school", "university",
            "blood test", "fever", "sore throat",
            "netball", "hockey", "basketball", "lacrosse", "contact sport", "play sport",
            "back to sport", "training", "team", "match", "matches", "pe kit")),
          "Glandular fever is the Epstein-Barr virus, and for most people it lasts about four to "
          "six weeks, with the tiredness often lingering for two or three months after the sore "
          "throat and fever have gone. Rest is the "
          "treatment: sleep when you need to, drink, take paracetamol or ibuprofen for the sore "
          "throat, and no alcohol while you are unwell because the liver is involved. The one "
          "rule people miss is no contact sport, heavy lifting or anything with a risk of a knock "
          "for at least four weeks - the spleen is enlarged and can rupture - and your GP may say "
          "longer. Sudden severe pain in the upper left of the tummy means A&E. A blood test "
          "confirms it, and tiredness that is not lifting after three months is worth a review.",
          bias=1,
          avoid=("gland", "glands", "lump", "lumps", "neck", "throat lump")),
    entry("shin-splints", (("shin", "shins", "shin splint", "shin splints", "splints", "calf"),
                           ("pain", "hurts", "hurting", "ache", "sore", "running", "run",
                            "what", "help", "should", "treat", "how long", "have", "got",
                            "i have", "ive got", "i've got", "treatment", "cure", "splint")),
          ("That is usually bone and muscle not used to the load: cut back to whatever mileage does "
           "not hurt, run on softer ground, and ice the shin for 10 minutes after. New shoes and a "
           "shorter stride help more than stretching, and calf raises twice a day build the muscle "
           "that takes the strain. A shin with one small spot of sharp pain that hurts to touch, or "
           "pain that carries on at rest, needs a GP, since that can be a stress fracture."),
          avoid=("shin pad", "shin pads", "shin guard", "football", "hockey", "boots",
                 "lump", "lumps")),
    entry("bleeding-gums-plaque", (("gums", "gum", "teeth", "tooth"), ("bleed", "bleeds", "bleeding",
                                                                "blood", "brush",
                                                                "brushing", "swollen",
                                                                "puffy", "receding", "receded",
                                                                "inflamed", "plaque",
                                                                "gingivitis", "disease")),
          ("Bleeding when you brush is usually gum disease and it is fixable: brush all the way to "
           "the gum line for two minutes twice a day, clean between the teeth with floss or "
           "interdental brushes once a day, and use a soft brush rather than pressing harder. "
           "See a dentist or hygienist - a scale and polish plus that routine usually stops it in a "
           "few weeks. Left alone it is the main cause of lost teeth in adults."),
          avoid=("chewing gum", "bubble gum", "shoe", "shoes", "sole", "carpet", "table",
                 "sticker", "label", "envelope", "printer", "hair", "glue", "stamp", "floor",
                 "tarmac", "clothes", "trouser", "trousers", "shirt", "wrapping",
                 "cat", "cats", "dog", "dogs", "puppy", "puppies", "pup", "kitten", "kittens",
                 "pet", "pets", "horse", "rabbit", "hamster", "guinea pig", "vet",
                 "how do i brush", "how to brush", "how should i brush", "how do i get him",
                 "how do i get her", "how do i get them", "how do i teach", "how to teach",
                 "refuses to brush", "refuse to brush", "wont brush", "won't brush",
                 "lies about", "lying about", "mostly about", "brushing her teeth",
                 "brushing his teeth", "brushing their teeth", "teeth every morning",
                 "teeth every night"),
          bias=1),
    entry("iron-supplement", (("iron", "ferritin", "anaemia", "anemia"), ("need", "should",
                                                                          "take", "supplement",
                                                                          "tablets", "low",
                                                                          "deficient", "ferrous")),
          ("Do not start iron tablets on a guess: ask a GP for a blood test first, because iron "
           "builds up and too much is harmful. If your ferritin is low, ferrous fumarate or "
           "sulphate with a glass of orange juice, and a gap of a few hours from tea, coffee and "
           "calcium, is absorbed far better; it takes about three months to refill. Black stools "
           "and constipation are the usual side effects, and vitamin C helps both."),
          avoid=("shirt", "shirts", "cast iron", "pan", "skillet",
                 "golf", "club", "clubs", "gym", "lift", "weights", "curtain", "steam",
                 "scorch", "burn", "crease", "creases", "trouser", "trousers", "dress",
                 "clothes", "clothing", "boiler", "water", "tap",
                 "temperature", "setting", "settings", "ironing", "soleplate", "wool", "silk",
                 "cotton", "linen", "polyester", "ironing board"),
          bias=2),
    entry("hangover", (("hangover", "hungover", "after drinking", "night out", "heavy night",
                        "after a drink", "after a few drinks", "after a few pints",
                        "after a pint", "drank last night", "drinking last night"),
                       ("i have", "i've got", "ive got", "i got", "today", "this morning",
                        "feel", "feeling", "im", "i'm", "still", "rough", "bad", "awful",
                        "dizzy", "dizziness", "spins", "spinning", "room spins", "vertigo",
                        "woozy", "light headed", "lightheaded", "sick", "nauseous")),
          ("There is no cure: water, sleep and food, and time. Drink a pint of water, eat "
           "something plain even if you don't want it, and take paracetamol rather than ibuprofen "
           "if your stomach is sore. Skip the hair of the dog - it buys a few hours and brings the "
           "whole thing back later."),
          bias=2),
    entry("blood-pressure", (("blood pressure", "bp", "hypertension", "hypertensive",
                              "140 over 90",
                              "150 over 95", "160 over 100", "170 over 100", "180 over 120",
                              "blood pressure reading"),
                             ("high", "worry", "worried", "lower", "reduce", "do", "how", "bad",
                              "dangerous", "reading", "stroke",
                              "140", "150", "160", "170", "180", "90", "95", "100",
                              "im", "am", "have", "got", "hypertension", "hypertensive")),
          ("A reading of 140/90 or higher, seen twice at home, is high and worth a GP check: they "
           "will confirm it and talk through treatment. Meanwhile cut salt, keep to 14 units of "
           "alcohol a week, and 150 minutes of walking a week lowers it by a few points. 180/120 "
           "or higher with a bad headache, chest pain or blurred vision is 999."),
          guard=_not_a_denial_of("blood pressure", "bp", "hypertension", "hypertensive"),
          avoid=("book", "books", "novel", "film", "read", "reading", "next", "recommend",
                 "author", "chapter",
                 "tablet", "tablets", "medication", "medicine", "medicines", "pill", "pills",
                 "side effect", "side effects"),
          bias=1),
    entry("lump", (("lump", "lumps", "swelling",
                    "swollen gland", "swollen glands", "gland", "glands", "lymph node",
                    "lymph nodes", "swollen lymph", "lymph gland", "lymph glands"),
                   ("neck", "armpit", "groin", "under my skin",
                                                    "under my arm", "under the arm", "underarm",
                                                    "after a vaccine", "found", "noticed", "what",
                                                    "should", "worried", "check", "feel",
                                                    "back", "head", "thigh", "shin", "ear", "arm",
                                                    "hand", "finger", "foot", "hip", "shoulder",
                                                    "ribs", "collarbone", "jaw", "eyelid",
                                                    "draining", "tender", "hurts", "painful",
                                                    "are", "is", "up", "have", "got", "went",
                                                    "swollen", "sore", "hard", "small", "moved",
                                                    "down",
                                                    "has", "had", "under the skin", "under his",
                                                    "under her", "under their")),
          ("A lump that comes up over a few days in the neck, armpit or groin is usually a swollen "
           "gland from an infection and settles in two to three weeks. Anywhere else, one that is "
           "soft and tender is usually the harmless sort. Anything hard, painless, fixed in place, "
           "or still there after three weeks needs a GP, and so does a lump with night sweats or "
           "weight loss."),
          avoid=PETS + ("breast", "testicle", "bump on the head", "bumped", "dent", "car", "road",
                        "lips", "lip", "tongue", "throat", "face", "closing", "closing up",
                        "breathing", "breathe", "wheeze", "wheezing",
                        "mouth", "in my mouth", "in the mouth", "gum", "gums", "cheek", "palate",
                        "roof of my mouth", "inside my cheek", "on my gum", "on my gums",
                        "wrist", "wrists", "hand", "hands",
                        "gravy", "sauce", "custard", "porridge", "batter", "mash", "soup",
                        "yorkshire pudding", "biscuit mix", "dough", "paint", "plaster",
                        "wallpaper", "cement", "filler", "skim", "screed",
                        "sting", "stings", "stung", "bee", "bees", "wasp", "wasps", "hornet",
                        "insect", "insects", "nettle", "nettles", "mosquito", "horsefly",
                        "tick", "midge", "gnat"),
          bias=1),
    entry("vertigo-rolling-over",
          (("turn over in bed", "turning over in bed", "turns over in bed", "turned over in bed",
            "roll over in bed", "rolling over in bed", "roll onto my side",
            "rolling onto my side", "lying down", "lie down", "lay down", "on my back",
            "bend down", "bending down", "bend over", "bending over", "bent over",
            "bend forward", "bending forward", "bent forward", "bend my head",
            "pick something up", "picking something up", "picking things up",
            "pick things up", "look up", "looking up", "looked up", "tip my head",
            "tipping my head", "tilt my head", "tilting my head", "put my head back",
            "hair wash", "at the hairdresser",
            "vertigo", "bppv"),
           ("dizzy", "dizziness", "spins", "spinning", "room spins", "vertigo", "light headed",
            "lightheaded", "giddy", "worse", "what", "why", "should", "how", "help", "normal",
            "is", "are", "serious", "dangerous", "treat", "treatment", "cure", "causes",
            "cause", "mean", "means", "keep", "keeps", "getting", "get", "have", "had", "got",
            "does", "do"),
           ),
          "That is usually BPPV - tiny crystals loose in the inner ear, so turning the head sets "
          "the room spinning for under a minute. It is not a stroke and it is fixable: a GP or a "
          "physio does the Epley manoeuvre, which moves the crystals back in one or two visits, "
          "and there are steps online to try at home. Sit up slowly and sleep propped on two "
          "pillows until it settles. Get seen the same day if it comes with hearing loss, weakness "
          "or numbness on one side, double vision, slurred speech, or a sudden bad headache.",
          ask=("dizzy", "dizziness", "spins", "spinning", "vertigo", "giddy", "light headed",
               "lightheaded", "room spins"),
          avoid=("my back", "your back", "bad back", "lower back", "upper back", "back pain",
                 "backache", "back ache", "back hurts", "neck", "shoulder", "shoulders", "spine",
                 "hurt", "hurts",
                 "pain", "pains", "painful", "sore", "stiff",
                 "stand", "standing", "stood", "get up", "getting up", "wake", "waking",
                 "morning", "pregnant", "pregnancy", "hangover", "drunk", "ride",
                 "drink", "drinks", "drinking", "drank", "alcohol", "beer", "pint", "pints",
                 "wine", "vodka", "gin", "whisky", "whiskey", "prosecco", "cocktail",
                 "night out", "after a few",
                 "fairground", "child", "children", "baby", "toddler",
                 "hitchcock", "film", "films", "movie", "movies", "song", "songs",
                 "album", "band", "u2", "documentary", "novel", "novels")),

    entry("cut-slow-healing",
          (("cut", "cuts", "wound", "wounds", "graze", "grazes", "scab", "scabs", "sore"),
           ("wont heal", "won't heal", "not healing", "isnt healing", "isn't healing",
            "not healed", "wont scab", "won't scab", "still open", "keeps opening",
            "keep opening", "slow to heal", "taking ages",
            "wont close", "won't close", "not closing", "isnt closing", "isn't closing",
            "hasnt closed", "hasn't closed", "not closed", "wont shut", "won't shut")),
          "A cut still open after a week or two, or one that keeps scabbing over and breaking "
          "down again, needs a GP look rather than more plasters: slow healing is often "
          "circulation, diabetes, low iron, or something left in the wound. Keep it clean and "
          "covered, and leave the scab alone. Get it seen the same day if it is spreading red, "
          "hot, swollen, smelly or weeping pus, or if you have a temperature.",
          avoid=("mouth", "ulcer", "ulcers", "gum", "gums", "dentist", "cold sore",
                 "blister", "infected", "infection", "pus", "smelly", "fever") + PETS),

    entry("mouth-lump",
          (("lump in my mouth", "lump in the mouth", "lump on my gum", "lump on my gums",
            "lump under my tongue", "lump on my tongue", "lump in my cheek",
            "lump on the inside of my cheek", "bump in my mouth", "bump on my tongue",
            "lump on the roof of my mouth", "lump inside my lip", "lump on my lip",
            "swelling in my mouth"),
           ("what", "why", "should", "worried", "how", "is it", "normal", "check", "get rid",
            "how long", "weeks", "days", "painful", "hurt", "hurts", "grown", "growing",
            "have", "has", "got", "i have", "ive got", "i've got", "noticed", "found",
            "there is", "theres", "there's",
            "my lip", "on my lip", "inside my lip", "my cheek", "my gum", "my gums",
            "my tongue", "in my mouth")),
          "Most lumps in the mouth are harmless - a mucocele, which is a small blocked spit gland "
          "and usually on the lower lip, a bony bump on the roof of the mouth, or a firm lump where "
          "a tooth has rubbed. Leave it alone and it often settles in a few weeks. Anything still "
          "there after three weeks, or hard, ulcerated, bleeding, growing or painless, needs a "
          "dentist or a GP within two weeks: that is the mouth cancer pathway, and it is usually "
          "nothing.",
          avoid=("neck", "armpit", "groin", "breast", "throat", "outside", "cold sore",
                 "blister") + PETS,
          bias=1,
          report=True),

    entry("face-droop", (("face", "mouth", "smile"), ("droop", "drooping", "dropped", "sagging",
                                                      "fallen", "numb", "numbness", "twisted",
                                                      "one side", "wont move", "won't move")),
          ("A face that has gone numb, drooped or twisted on one side needs 999 now, not a wait "
           "and see - it can be a stroke even if it feels mild and even if it is passing. Note the "
           "time it started, unlock the door, sit down and stay on the line to the call handler."),
          bias=4,
          guard=lambda understood: not _the_dentist_numbed_it(understood)),

    entry("numb-after-the-dentist",
          (("numb", "numbness", "numbed", "numb again"),
           ("mouth", "lip", "lips", "tongue", "cheek", "cheeks", "chin", "jaw", "gum", "gums",
            "face", "teeth", "tooth")),
          "A numb lip, tongue or cheek after a filling is the local anaesthetic still working: it "
          "fades in two to five hours, and a lower-jaw injection often longer than an upper one. "
          "While it lasts, eat soft cool food and chew on the other side, because it is easy to "
          "bite your lip or cheek without feeling it, and don't have a hot drink. Ring the "
          "dentist if it is still numb the next day, or if there is swelling, a fever or a bitter "
          "taste with pus. A face that droops or will not move on one side, or an eye that will "
          "not close, is not the anaesthetic - that is 999.",
          bias=3,
          guard=_the_dentist_numbed_it),

    entry("itchy-ear",
          (("ear", "ears", "ear canal"),
           ("itchy", "itching", "itch", "itches", "scratch", "scratchy", "tickly", "irritated",
            "irritating")),
          "An itchy ear canal is usually dry skin or a touch of eczema, sometimes a little water "
          "or wax left behind. Leave cotton buds, keys and hairgrips out of it: they scratch the "
          "skin and pack wax against the drum, which is what keeps the itch going. A few drops of "
          "olive oil, or an ear spray from a pharmacist, settles most of it. See a pharmacist or "
          "GP if there is discharge, pain, a drop in hearing, or it has been weeks.",
          avoid=("wax", "blocked", "blocking", "ringing", "tinnitus", "ache", "aches", "aching",
                 "pain", "hurts", "hurt", "swim", "swimming", "water in my ear", "discharge",
                 "pus", "dog", "cat", "puppy", "kitten", "baby", "child", "toddler", "kid",
                 "piercing", "piercings", "phone", "headphone", "headphones", "hearing aid",
                 "cotton bud", "cotton buds", "q tip")),

    entry("dehydration", (("dehydrated", "dehydration", "thirsty", "thirst", "dry mouth",
                           "dark urine", "urine is dark", "urine looks dark", "urine dark",
                           "dark wee", "wee is dark", "wee looks dark", "wee dark",
                           "dark pee", "pee is dark", "pee looks dark", "pee dark",
                           "dark piddle", "piddle is dark",
                           "not drinking enough", "drink enough water",
                           "drinking enough", "how much water",
                           "keep water down", "keeps water down", "keep fluids down",
                           "keep anything down", "keep food down", "keep it down", "keep down",
                           "cant keep water", "cant keep fluids",
                           "keep milk down", "keeps milk down", "keep the milk down",
                           "cant keep milk", "cant keep her milk", "cant keep his milk",
                           "cant keep the milk", "cant keep the bottle", "cant keep her bottle",
                           "cant keep his bottle", "keep bottle down", "brings it back up",
                           "bringing it back up", "brings his milk up", "brings her milk up"),
                          ("am i", "how do i know", "how can i tell", "how to tell", "tell if",
                           "signs", "symptoms", "sign", "do i need", "enough", "should i drink",
                           "what are the", "recognise", "check", "water", "urine", "wee", "dark",
                           "down", "cant", "can't", "cannot", "keeps",
                           "mean", "means", "meaning", "i have", "have a")),
          dehydration_help,
          avoid=("how much water", "how many glasses", "glasses a day", "litres", "liters",
                 "plant", "plants", "garden", "lawn", "hanging basket", "fish tank", "boiler",
                 "radiator", "hot water", "water bill", "water meter", "filter", "softener",
                 "kettle", "washing machine", "dishwasher", "waterproof", "water feature",
                 "pond", "dog", "cat", "puppy", "car", "battery",
                 "feel sick", "feeling sick", "sick feeling",
                 "yellow skin", "skin is yellow", "gone yellow", "yellow eyes", "yellow eye",
                 "jaundice", "jaundiced", "whites of my eyes",
                 "noise", "noisy", "loud", "louder", "turn it down", "keep the noise down",
                 "quiet", "quieter", "music", "radio", "speaker", "speakers",
                 "neighbour", "neighbours", "next door", "colleague", "colleagues",
                 "coworker", "coworkers", "co-worker", "co-workers", "workmate", "workmates",
                 "at work", "office", "my desk", "the desk", "classroom", "library")),

    entry("weight-put-on", (("put on weight", "put on a bit", "put on a few", "put on a stone",
                             "put on half a stone", "gained weight", "gaining weight",
                             "gained a bit", "gone up a size", "heavier than", "getting fat",
                             "got fat", "a bit of weight", "few pounds"),
                            ("weight", "bit", "pounds", "stone", "size", "how do i", "what can i",
                             "what should i", "should i", "worry", "normal", "worried", "help",
                             "do about", "lose", "cut")),
          "A few pounds over a winter or a stressful stretch is normal, and what shifts it is not a "
          "diet but two or three swaps you can actually keep: a slightly smaller plate, water or "
          "squash instead of the sweet drink, fruit in place of the afternoon biscuit, and a walk "
          "after dinner. Weigh yourself once a week at the same time of day rather than daily, "
          "because water swings a kilo or two either way, and muscle and getting older move the "
          "scales without anything being wrong. See a GP if the weight has gone on quickly without "
          "your eating changing, or it comes with being very thirsty, very tired or short of "
          "breath.",
          avoid=("lose weight", "losing weight", "lose a stone", "how to lose", "diet", "calorie",
                 "calories", "bmi", "obese", "obesity", "fasting", "keto", "slimming world",
                 "weight watchers", "ozempic", "wegovy", "car", "van",
                 "caravan", "trailer", "luggage", "suitcase",
                 *pets.ANIMAL_NOUNS,
                 "shirt", "shirts", "top", "my top", "jeans", "trousers", "jumper", "dress",
                 "skirt", "blouse", "cardigan", "hoodie", "coat", "stain", "stains", "stained",
                 "mark", "marks", "out of my", "fabric", "laundry", "washing")),
    entry("diabetic-foot-wound",
          (("diabetic foot", "diabetic feet", "diabetes", "diabetic", "neuropathy",
            "foot ulcer", "foot ulcers", "ulcer on my foot", "ulcer on my feet",
            "lost the feeling in my feet", "cant feel my feet", "can't feel my feet"),
           ("blister", "blisters", "cut", "cuts", "ulcer", "ulcers", "sore", "wound", "graze",
            "scratch", "ingrown", "toenail", "toe nail", "hot", "red", "swollen", "black",
            "weeping", "infection", "infected")),
          "A blister, cut or sore on a diabetic foot is a same-day job rather than a plaster: ring "
          "the GP or your diabetic foot clinic today, and go to A&E if the foot is hot, red, "
          "swollen or has a black or weeping patch, because with diabetes an infection can get "
          "deep before it hurts. Don't cut a corn, don't use a corn plaster or a hot water bottle, "
          "and stay off it and off barefoot floors until it has been looked at.",
          ask=("foot", "feet", "toe", "toes", "sole", "soles", "heel", "heels", "arch",
               "arches", "ankle", "ankles"),
          bias=2),
        entry("diabetic-foot-care",
          (("diabetic foot", "diabetic feet", "diabetes", "diabetic", "neuropathy",
            "lost the feeling in my feet", "cant feel my feet", "can't feel my feet",
            "numb feet", "feet are numb", "numb toes", "numbness in my feet", "numb foot"),
           ("feet", "foot", "toes", "toe", "numb", "numbness", "tingling", "burning",
            "look after", "care", "dry", "cracked", "hard skin", "callus", "corn", "corns",
            "podiatrist", "chiropodist")),
          "Look at both feet every day - the soles with a mirror, and between the toes - and never "
          "go barefoot, even indoors, because with diabetes a small cut can turn into an ulcer "
          "before it hurts. Dry them well, cut the nails straight across, use a moisturiser on hard "
          "skin but not between the toes, and have corns and calluses done by a podiatrist. Ring "
          "the clinic the same day about any cut, blister or red, hot or weeping patch.",
          ask=("diabetic", "diabetes", "neuropathy", "diabetic foot", "diabetic feet", "type 1",
               "type 2", "insulin", "hba1c"),
          avoid=("eye", "eyes", "eye test", "optician", "sight", "retina", "prescription",
                 "glasses", "lenses", "sugar", "blood sugar", "hba1c", "diet", "what can i eat",
                 "metformin", "insulin", "driving", "licence", "travel", "insurance"),
          bias=1),
        entry("diabetic-foot-check",
          (("diabetic foot check", "foot check", "annual foot check", "foot checks",
            "feet checked", "foot examination", "diabetic check"),
           ("diabetes", "diabetic", "year", "yearly", "annual", "how often", "what happens",
            "appointment", "book", "due")),
          "The annual foot check is about ten minutes with a practice nurse or a podiatrist: they "
          "look at the skin and nails, feel the pulses in your feet and test the feeling in your "
          "toes, and ask about your shoes and any sores. It is free and it is how a problem is "
          "caught before it becomes an ulcer, so book it if you have not had one in the last year.",
          ask=("foot", "feet", "toe", "toes", "podiatrist", "podiatry", "shoe", "shoes",
               "soles", "nails"),
          bias=2),

        entry("diabetes-what-to-eat",
          (("diabetic", "diabetics", "diabetes", "type 1 diabetes", "type 2 diabetes",
            "blood sugar", "blood sugars", "my sugar", "hba1c"),
           ("eat", "eating", "food", "foods", "diet", "dieting", "banana", "bananas", "honey",
            "lower", "lowering", "bring down", "get it down", "get my sugar down", "cut down",
            "reduce", "reducing",
            "sugar", "sugars", "carb", "carbs", "carbohydrate", "carbohydrates", "bread",
            "pastry", "chocolate", "sweets", "fruit", "juice", "rice", "pasta", "potato",
            "potatoes", "cake", "biscuits", "alcohol", "beer", "wine", "avoid", "cut out",
            "swap", "porridge", "oats", "oatmeal", "cereal", "milk", "cheese", "eggs")),
          "Nothing is banned: it is the size of the starchy and sugary part that counts. Make half "
          "the plate vegetables, a quarter meat, fish, eggs or beans and a quarter potatoes, rice, "
          "pasta or bread, wholegrain where you can, because it lifts your sugar more slowly. Fruit "
          "whole rather than as juice, cake and sweets after a meal rather than on their own, and "
          "sugary drinks swapped for water or diet ones - that swap does more than any one food "
          "rule. A diabetic nurse can book you on a free course, DESMOND or X-PERT.",
          avoid=("level", "levels", "hba1c", "target", "targets", "normal", "test", "testing",
                 "meter", "reading", "readings", "too low", "too high", "hypo", "hypos",
                 "hypoglycaemia", "hypoglycemia", "ketones", "dka", "coma", "passed out",
                 "unconscious", "shaking", "shaking and sweating", "foot", "feet", "ulcer",
                 "blister", "toes", "eye", "eyes", "sight", "retina", "metformin", "insulin",
                 "tablets", "dose", "doses", "units", "inject", "injection", "pregnant",
                 "pregnancy", "expecting", "child", "kid", "toddler", "baby", "son", "daughter",
                 "mum", "dad", "husband", "wife", "partner",
                 "breakfast", "lunch", "dinner", "snack", "snacks", "supper",
                 "is 1", "is 2", "is 3", "is 4", "reading", "readings"),
          ask=("eat", "eating", "food", "foods", "diet", "dieting", "banana", "bananas", "honey",
               "sugar", "sugars", "carb", "carbs", "carbohydrate", "carbohydrates", "bread",
               "pastry", "chocolate", "sweets", "fruit", "juice", "rice", "pasta", "potato",
               "potatoes", "cake", "biscuits", "alcohol", "beer", "wine", "what can i",
               "what should i", "can i", "should i", "how much", "is it ok", "ok to", "better",
               "avoid", "cut out", "swap", "safe to", "good for", "good for you",
               "good for me", "healthy", "ok for", "okay for", "safe for", "allowed")),
        entry("diabetes-blood-sugar-numbers",
          (("diabetic", "diabetics", "diabetes", "type 2 diabetes", "type 1 diabetes",
            "blood sugar", "blood glucose", "hba1c"),
           ("level", "levels", "number", "numbers", "target", "targets", "normal", "range",
            "mean", "means", "test", "testing", "check", "how often", "before meals",
            "after meals", "morning", "fasting", "good", "should", "be", "aim")),
          "For most adults with type 2 the target is 4 to 7 mmol/L before meals and under 8.5 two "
          "hours after, and an HbA1c of 48 mmol/mol, which is 6.5 per cent - your own team may set "
          "yours higher or lower, so it is worth knowing the numbers they wrote down for you. "
          "HbA1c is the average of the last two or three months rather than one day, which is why "
          "the annual blood test is judged on it. Testing at home is only needed for some people, "
          "so ask whether yours is one of them.",
          avoid=("too low", "very low", "gone low", "is low", "dropped", "dropping", "hypo",
                 "hypoglycaemia", "hypoglycemia", "shaking", "sweating", "confused", "passed out",
                 "unconscious", "ketones", "dka", "very high", "is high", "22", "foot", "feet",
                 "ulcer", "blister", "eye", "eyes", "metformin", "insulin", "tablets", "dose",
                 "pregnan", "child", "kid", "toddler", "baby",
                 "blood sugar is", "blood glucose is", "sugar is 1", "sugar is 2", "sugar is 3",
                 "sugar is 4", "sugar is 5", "sugar is 6", "sugar is 7", "sugar is 8",
                 "sugar was", "reading of", "mmol",
                 "eat", "eating", "ate", "meal", "meals", "breakfast", "lunch", "dinner",
                 "supper", "snack", "snacks", "cook", "cooking", "recipe", "recipes",
                 "foot", "feet", "toes", "ulcer", "blister", "eye", "eyes", "sight",
                 "dentist", "kidney", "cholesterol", "blood pressure", "thyroid"),
          ask=("level", "levels", "number", "numbers", "target", "targets", "normal", "range",
               "should", "mean", "means", "test", "testing", "check", "how often", "before meals",
               "after meals", "morning", "fasting", "hba1c",
               "good blood sugar", "good blood glucose", "good hba1c", "good level",
               "good levels", "good numbers", "good reading", "good range")),
    entry("blood-sugar-testing",
          (("blood sugar", "blood sugars", "blood glucose", "sugar level", "sugar levels",
            "diabetes", "diabetic", "type 1", "type 2", "glucose meter", "meter", "finger prick",
            "finger pricking", "cgm", "libre", "dexcom", "test strips", "strips"),
           ("how often", "how many times", "how frequently", "frequency", "regularly",
            "often should", "times a day", "times a week", "twice a day", "every day",
            "monitor", "monitoring", "test", "testing", "check", "checking", "prick")),
          "It depends on the medicine, and your diabetes team sets the number for you: on insulin "
          "most people test before every meal and again two hours after, plus before bed and "
          "before driving, which lands at four to ten times a day. On tablets or on nothing, two "
          "or three times a week at different times of day is plenty for many people, and some "
          "only need it before breakfast. A sensor reads all day without a prick, and the tablets "
          "that raise the risk of a low are the ones that need the most checking. Ask them at "
          "your next review rather than guessing, and write down what you get so a pattern shows.",
          avoid=("too low", "very low", "gone low", "is low", "dropped", "dropping", "hypo",
                 "hypoglycaemia", "hypoglycemia", "shaking", "sweating", "confused", "passed out",
                 "unconscious", "ketones", "dka", "very high", "is high", "reading", "mmol",
                 "blood sugar is", "blood glucose is", "sugar was", "ate", "eat", "eating", "meal",
                 "meals", "breakfast", "lunch", "dinner", "snack", "cook", "recipe", "metformin",
                 "insulin dose", "how much insulin", "units", "foot", "feet", "eye", "eyes",
                 "pregnant", "pregnancy", "child", "kid", "toddler", "baby",
                 "cat", "cats", "dog", "dogs", "kitten", "puppy", "rabbit", "hamster",
                 "guinea pig", "horse", "pet", "pets", "vet", "vets", "animal"),
          bias=2),
    entry("blood-sugar-high",
          (("blood sugar", "blood sugars", "blood glucose", "sugar level", "sugar levels",
            "sugar reading", "hba1c", "diabetes", "diabetic"),
           ("high", "too high", "very high", "is high", "so high", "spiked", "spike", "spiking",
            "rocketed", "raised", "is up", "gone up", "keeps going high", "over 10", "over 15",
            "over 20", "high all", "high in the morning", "high after")),
          "Twice in a row above 15 mmol/L is a call to your diabetes team today rather than a "
          "wait-and-see, especially with thirst, lots of weeing or a fuzzy head. Drink water, keep "
          "taking your tablets or insulin as prescribed, test more often, and check ketones if you "
          "use insulin. Sleepy, breathing fast, being sick and unable to keep fluid down is 999 - "
          "that is what DKA looks like. One high reading after a big meal is not.",
          avoid=("hypo", "hypos", "low blood sugar", "sugar is low", "too low", "gone low",
                 "dropped", "dropping", "shaking", "sweating", "confused", "unconscious",
                 "passed out", "ketones", "dka", "what should i eat", "what can i eat", "diet",
                 "recipe", "meal ideas", "breakfast", "lunch", "dinner", "snack",
                 "target", "targets", "normal range", "hba1c be", "what is a normal",
                 "how do i lower", "bring it down", "lower my"),
          shape=(_a_high_reading,),
          bias=1),
    entry("blood-sugar-a-reading",
          (("blood sugar", "blood glucose", "sugar reading", "blood sugar reading", "my sugar was",
            "reading of", "mmol", "hba1c", "glucose reading"),
           ("high", "normal", "ok", "okay", "fine", "bad", "too high", "good", "worry",
            "worried", "should i worry", "mean", "means")),
          "A single figure only means something with its timing: 4 to 7 mmol/L before a meal and "
          "under 8.5 two hours after is the usual target for someone with diabetes, so 7.8 two "
          "hours after eating is close to it, and 7.8 before breakfast twice is worth a GP visit. "
          "If you have not been diagnosed, one reading cannot diagnose anything - ask for an "
          "HbA1c, which averages the last two or three months. Write down the time with the number.",
          shape=(lambda words: bool(re.search(r"\d", (words or ""))),),
          guard=lambda understood: not _a_high_reading(understood.get("clean", "")),
          avoid=("target", "targets", "what is a normal", "normal range", "should it be",
                 "how high", "is high", "too high", "hypo", "low blood sugar", "ketones", "dka",
                 "what should i eat", "what can i eat"),
          bias=2),
    entry("give-blood",
          (("give blood", "donate blood", "donating blood", "blood donation", "blood donor",
            "blood donors", "donate plasma", "give plasma", "donate platelets"),
           ("can i", "could i", "should i", "am i able", "am i allowed", "eligible", "how often",
            "how old", "age", "weight", "too old", "too young", "under 18", "tattoo", "piercing",
            "medication", "tablets", "on medication", "pregnant", "breastfeeding", "cold", "flu",
            "how much blood", "does it hurt", "how long does it take", "what happens")),
          "In the UK you can give blood from 17 to 65 if you have not donated before, and you need "
          "to be at least 50kg; men can go every 12 weeks and women every 16. Wait 7 days after a "
          "cold or flu, and 4 months after a tattoo, piercing or acupuncture. Most everyday "
          "medicines are fine - the questionnaire at the session decides, and staff will tell you "
          "there and then. Book at blood.co.uk; a whole donation takes about an hour including the "
          "rest afterwards.",
          avoid=("my blood", "blood test", "blood pressure", "blood group", "blood type",
                 "my period", "period pain", "plasma tv", "platelet count", "clot",
                 "pregnant", "pregnancy", "expecting", "breastfeeding", "just had a baby",
                 "gave birth", "blood thinner", "blood thinners", "warfarin", "apixaban",
                 "rivaroxaban", "clopidogrel", "chemo", "chemotherapy", "cancer")),
    entry("bp-reading", (("blood pressure", "bp", "systolic", "diastolic",
                          "140 over", "150 over", "160 over", "135 over", "130 over",
                          "over 90", "over 95", "110 over", "120 over", "185 over", "180 over"),
                         ("150", "140", "160", "130", "135", "90", "95", "100", "110", "180",
                          "185", "190", "200", "too high", "high", "worry", "worried", "reading",
                          "is that", "over", "what should", "how do i")),
          bp_help,
          bias=2,
          avoid=("chest pain", "blurred vision", "confusion", "pregnant", "pregnancy",
                 "what is a normal", "whats a normal", "what is normal", "normal range",
                 "normal reading", "what should my blood pressure be", "healthy blood pressure",
                 "good blood pressure", "blood pressure range",
                 "lower", "lowering", "bring down", "bring it down", "bring my", "get it down",
                 "getting it down", "reduce", "diet", "lifestyle",
                 "lose weight", "what should i eat", "what can i eat", "what foods",
                 "foods should i avoid", "salt", "exercise", "walking",
                 "medication", "side effects", "tablets work")),
    entry("pale-look",
          (("pale", "paleness", "pallid", "washed out", "no colour", "grey", "gray",
            "white as a sheet", "losing colour", "lost colour", "colour has gone",
            "pinched looking", "peakish", "peaky"),
           ("son", "daughter", "baby", "toddler", "child", "children", "kid", "kids", "boy",
            "girl", "husband", "wife", "partner", "mum", "dad", "mother", "father", "friend",
            "baby's", "face", "lips", "lip", "skin", "tongue", "colour", "he", "she", "they",
            "i", "me", "we", "im", "i am", "am i", "went", "gone", "got")),
          "Pale and otherwise well - eating, drinking, playing, no temperature - is usually "
          "nothing: winter, a growth spurt and a diet low in iron all show in the face, and one "
          "blood test at the GP settles it. Pale with a temperature, fast breathing, floppiness, "
          "unusual sleepiness or no wet nappies is 111 today. Pale with grey or blue lips, a fit, "
          "or someone you cannot wake is 999, and so is pale and clammy with chest pain. Pale with a "
          "rash that does not fade when you press a glass on it is 999 too.",
          avoid=("washing", "washing out", "wash out", "wash", "laundry", "washing line",
                 "line", "peg", "pegs", "dry", "drying", "tumble dryer", "load of washing",
                 "clothes", "whites", "bedsheets", "sheets",
                 "sock", "socks", "shoe", "shoes", "trousers", "shirt", "jumper", "dress",
                 "bread", "pastry", "cake", "sauce", "sourdough", "dough", "roast", "gravy",
                 "mince", "stew", "casserole", "bake", "baked", "baking", "oven", "recipe",
                 "ale", "lager", "beer", "stout", "wine", "coffee", "milk", "tea", "butter",
                 "bolognese", "curry", "onion", "garlic", "rice", "pasta", "potato", "potatoes",
                 "paint", "wall", "walls", "wood", "furniture", "garden", "plant", "plants",
                 "leaves", "leaf", "lawn", "basil", "hydrangea", "grass", "flower", "flowers",
                 "chicken", "egg", "eggs", "yolk", "biscuit", "biscuits", "pizza", "soup",
                 "fever", "feverish", "sweating", "sweaty", "sweats", "clammy",
                 "tired", "exhausted", "knackered", "no energy", "sore throat", "cold",
                 "flu", "run down", "rundown",
                 "breathless", "breathing", "breath", "blue", "grey lips", "rash", "floppy",
                 "limp", "unresponsive", "not drinking", "wont drink", "won't drink",
                 "going grey", "going gray", "turning grey", "turning gray",
                 "turn grey", "turn gray", "grey hair", "gray hair", "beard", "beards",
                 "moustache", "mustache", "eyebrows", "eyebrow",
                 "eyes", "eye", "sky", "cloud", "clouds", "car", "cars", "photo", "picture",
                 "paint", "period", "periods", "cat", "cats", "dog", "dogs", "kitten", "puppy",
                 "jeans", "trousers", "denim", "jumper", "jumpers", "cardigan", "hoodie",
                 "shirt", "shirts", "dress", "dresses", "skirt", "coat", "jacket", "socks",
                 "fabric", "wool", "curtains", "laundry", "washing", "faded", "fading",
                 "clothes", "clothing",
                 "dizzy", "dizziness", "dizzy spells", "light headed", "light-headed",
                 "lightheaded", "faint", "faintness", "fainted", "fainting", "spinning",
                 "the room spins", "room is spinning", "room spun", "spun", "woozy",
                 "unsteady", "swaying", "see stars", "blacked out", "blacking out",
                 "pass out", "passed out", "passing out",
                 "nappies", "nappy", "sleepy", "drowsy", "lethargic", "chest pain",
                 "sick", "vomiting", "diarrhoea", "blood", "bruise", "bruises", "bruising",
                 "iron", "anaemia", "anaemic"),
          bias=1),
    entry("anaemia-signs", (("anaemia", "anaemic", "anemic", "low iron", "iron level",
                             "iron levels", "haemoglobin", "hemoglobin", "iron deficiency"),
                            ("signs", "symptom", "symptoms", "how do i know", "could it be",
                             "am i", "do i have", "always tired", "exhausted", "pale",
                             "breathless", "test", "level", "low", "worried", "is it")),
          "Iron-deficiency anaemia shows up as tiredness, breathlessness on the stairs, pale skin "
          "and sometimes a sore tongue or brittle nails. A simple blood test at the GP confirms "
          "it, and iron tablets with vitamin C usually fix it in a couple of months, but the cause "
          "is worth checking too - heavy periods and a poor diet are the usual ones.",
          bias=1, avoid=PETS),
    entry("morning-throat", (("throat", "voice", "croaky", "hoarse", "husky"),
                             ("every morning", "in the morning", "when i wake", "waking up",
                              "wake up", "first thing", "each morning", "overnight", "every day",
                              "always", "keeps going", "gone", "with a sore")),
          "A throat that is sore or a voice that is rough first thing, then eases through the day, "
          "is usually dry air or breathing through your mouth at night: leave a window open or put "
          "a glass of water by the bed. A sour taste, heartburn at night or a cough means reflux - "
          "raise the head of the bed and eat earlier. A voice hoarse for over three weeks "
          "needs a GP look.",
          avoid=tuple(word for word in PETS if word != "horse") + (
              "my horse", "the horse", "a horse", "horse has", "horse is", "horses",
              "baby", "baby's", "child", "children", "toddler")),
    entry("bites-itch", (("bite", "bites", "bitten", "mosquito", "mosquitoes", "insect", "midge",
                          "midges", "gnat", "gnats", "bug bite", "bug bites", "insect bite"),
                         ("itch", "itchy", "stop", "help", "swollen", "relief", "best", "so",
                          "really", "keep getting", "every summer", "what helps")),
          "Wash the bite, then cool it with an ice pack wrapped in a cloth for ten minutes and try "
          "not to scratch, because scratching is what makes them swell and scar. A pharmacy "
          "antihistamine or a hydrocortisone cream eases the itch. Get help if the skin around it "
          "spreads red and hot, or you feel feverish or unwell.",
          avoid=PETS + ("nail", "nails", "tooth", "gum", "gums", "tetanus", "human", "dog bite",
                        "cat bite")),
    entry("pharmacy-or-gp", (("pharmacy", "pharmacist", "chemist"),
                             ("gp", "doctor", "111", "a&e", "hospital", "instead", "or", "see",
                              "go to", "should i", "first", "which")),
          "Start with a pharmacist for anything minor: coughs, colds, sore throats, aches, rashes, "
          "hay fever, stomach upsets, cystitis, threadworms, and advice on which medicine to buy. "
          "They can treat some of it themselves and will say when it needs a GP. Ring 111 when you "
          "are not sure and it cannot wait, and 999 for chest pain, breathing trouble or a stroke.",
          bias=1,
          avoid=("open", "opening", "hours", "closed", "collect", "pick up", "repeat",
                 "prescription", "deliver", "nearest", "late night", "sunday")),
    entry("phlegm-catarrh",
          (("phlegm", "phlegmy", "catarrh", "catarrhy", "mucus", "mucous", "post nasal drip",
            "postnasal drip", "hawking", "spit", "spitting", "snot"),
           ("always", "keep", "keeps", "constant", "constantly", "what", "why", "how", "help",
            "get rid", "clear", "clearing", "morning", "mornings", "throat", "nose", "chest",
            "worse", "annoying", "stuck",
            "feel", "feeling", "have", "got", "with", "a bit", "so")),
          "Phlegm that sits in the throat is usually a drip from the back of the nose - a cold, "
          "an allergy, a blocked nose, dry air, reflux or smoking - rather than your chest "
          "producing it. A salt water rinse (half a teaspoon in a glass of cooled boiled water) "
          "or a steroid nose spray for a fortnight is what shifts most of it, with plenty of "
          "water and the room not too dry. See a GP if it lasts more than three weeks, comes with "
          "weight loss or night sweats, or if the phlegm is bloodstained or green with a fever.",
          avoid=("cough", "coughing", "coughs", "cold", "colds", "flu", "sore throat", "tonsil",
                 "tonsils", "chesty", "asthma", "inhaler", "bronchitis", "pneumonia",
                 "baby", "child", "toddler", "my son", "my daughter", "dog", "cat",
                 "spitting the food", "spits the food", "spitting food", "spits food",
                 "spitting it out", "spits it out", "spat it out", "spat the food out",
                 "food out", "the spoon", "puree", "mashed")),

    entry("green-poo",
          (("poo", "poos", "poop", "stool", "stools", "bowel movement", "number two", "wee"),
           ("green", "greenish", "yellow green", "spinach", "iron tablets", "food colouring",
            "bile")),
          "Green poo is almost always food moving through a bit fast, so bile does not get time "
          "to turn brown - a stomach bug, a curry, spinach, green food colouring, or iron and "
          "some antibiotics. It settles in a day or two on its own: drink plenty, eat simply, and "
          "keep taking rehydration sachets if there is diarrhoea too. See a GP if it is still "
          "green after a week, if there is blood in it, or if it comes with pain, a fever or "
          "weight loss.",
          avoid=("black", "tarry", "pale", "white", "clay", "blood", "bloody", "red", "mucus",
                 "baby", "newborn", "toddler", "my son", "my daughter", "dog", "cat", "cat litter",
                 "carpet", "nappy")),

    entry("poo-colour",
          (("poo", "poos", "poop", "stool", "stools", "number two", "bowel movement",
            "my bum", "when i wipe", "toilet paper", "toilet", "loo", "in the pan",
            "on the paper"),
           ("black", "tarry", "tar like", "tar-like", "very dark", "dark red", "blood",
            "bloody", "bleeding", "bright red", "red", "pale", "clay", "whitish", "white",
            "yellowish", "greasy")),
          _poo_colour,
          avoid=("green", "greenish", "baby", "newborn", "toddler", "my son", "my daughter",
                 "dog", "cat", "kitten", "puppy", "carpet", "nappy", "litter")),
    entry("boil",
          (("boil", "boils", "skin abscess", "abscess on my skin", "infected lump"),
           ("have", "got", "leg", "arm", "skin", "lump", "pus", "painful", "pain", "getting",
            "keep", "recurring", "back", "bum", "bottom", "thigh", "face", "armpit",
            "under my arm", "on my", "sore", "red", "big", "draining",
            "squeeze", "squeezing", "squeezed", "pop", "popping", "popped", "pick", "picking",
            "picked at", "prick", "pricking", "lance", "lancing", "burst", "bursting",
            "do about", "what can i do", "what do i do", "how do i", "get rid of")),
          "Put a warm flannel on it for ten minutes three or four times a day and cover it with a "
          "clean dressing, and do not squeeze it: most boils come to a head and drain on their own "
          "in a week or two. Take paracetamol if it throbs, and wash your hands after touching it "
          "or the dressing, because the germ spreads. See a GP the same day if the redness is "
          "spreading, the skin around it is hot and swollen, you have a fever, or the boil is on "
          "your face or near the top of your nose; also get it looked at if it is bigger than a "
          "golf ball, if you have diabetes, or if you keep getting them, because a course of "
          "antibiotics or a small drainage is sometimes needed.",
          bias=2,
          avoid=("water", "kettle", "egg", "eggs", "potato", "potatoes", "rice", "pasta", "soup",
                 "tooth", "teeth", "gum", "knee", "chicken", "milk", "sugar", "notice",
                 "mouth", "tongue", "lip", "child", "children", "my son", "my daughter",
                 "baby", "toddler", "breast", "nipple", "piles", "haemorrhoid",
                 "pan", "pans", "saucepan", "saucepans", "pot", "pots", "boiled dry",
                 "boils dry", "boil dry", "dry", "dried", "hob", "stove", "cooker", "heat",
                 "sauce", "gravy", "jam", "syrup", "sugar thermometer")),

    entry("boil-water-notice",
          (("boil notice", "boil water notice", "boil-water notice", "boil water alert",
            "water notice", "water alert", "do not drink the water", "water is not safe",
            "water unsafe", "notice says to boil", "need to boil", "have to boil",
            "should i boil"),
           ("water", "tap", "drink", "drinking", "safe", "kettle", "council", "supplier",
            "company", "still", "how long", "what do", "should i")),
          "While a boil-water notice is on, use tap water that has been brought to a rolling "
          "boil for a minute and then left to cool for anything you swallow: drinking, brushing "
          "teeth, washing salad or fruit, making ice, and a baby's bottle. Kettles, pans and "
          "cooled boiled water are fine; a water filter is not, and neither is bottled water "
          "unless it says it is for a baby. Washing hands, washing up and the loo are fine with "
          "ordinary tap water, and cooled boiled water is also what you want for the pets. "
          "Notices usually lift after a day or two once the samples come back clear - check your "
          "water company's own page for the postcode, and if anyone in the house has had "
          "stomach trouble, ring 111 and mention the notice.",
          ask=("water", "tap", "drink", "drinking", "safe", "kettle", "council", "supplier",
               "company", "still", "how long", "what do", "should i", "there"),
          avoid=("degree", "degrees", "celsius", "fahrenheit", "temperature", "boiling point",
                 "egg", "eggs", "pasta", "rice", "potato", "potatoes", "vegetable",
                 "vegetables", "abscess", "sore", "pus", "squeeze",
                 "gammon", "steak", "steaks", "sausage", "sausages", "bacon", "chicken",
                 "joint", "meat", "mince", "noodle", "noodles", "cabbage", "broccoli",
                 "carrot", "carrots", "kale", "spinach", "beans", "lentils", "quinoa",
                 "couscous")),

    entry("tooth-hole",
          (("hole in my tooth", "hole in a tooth", "hole in the tooth", "hole in my molar",
            "cavity", "tooth decay", "decayed tooth", "black spot on my tooth",
            "chipped tooth", "broken tooth", "broke my tooth", "tooth has broken",
            "tooth has a hole", "tooth is broken", "chipped my tooth", "broke my tooth",
            "cracked my tooth", "my tooth cracked"),
           ("have", "has", "got", "ive got", "feel", "feels", "big", "small", "what",
            "should i", "how", "fix", "dentist", "eat", "eating", "pain", "hurts", "hurt",
            "tooth", "teeth", "hole", "chipped", "broken")),
          "A hole you can feel in a tooth is decay, and it does not fill itself: ring a dentist and "
          "have it looked at before it hurts, because a small filling is quicker and cheaper than "
          "the root canal or the extraction a deep cavity ends up needing. Until then brush it like "
          "the rest - spit rather than rinse after the toothpaste - keep sugary food to mealtimes, "
          "and don't poke at it with a fingernail or a pin. Ring the same day if it is painful, if "
          "food keeps packing into it, or if your face or jaw swells: a broken tooth with a sharp "
          "edge can also be smoothed by a dentist before it cuts your tongue.",
          avoid=("wall", "road", "ground", "garden", "sock", "socks", "golf", "tooth fairy",
                 "drill", "button", "dig")),

    entry("nose-that-runs-all-the-time",
          (("my nose is always running", "nose keeps running", "sneezing in the morning",
            "i sneeze in the morning", "sneezing fits", "i keep sneezing",
            "sneezing every morning", "sniffing all the time", "nose runs every",
            "nose runs in the", "nose runs when"),
           ("always", "keep", "keeps", "morning", "mornings", "all the time", "why", "what",
            "help", "stop", "constant", "constantly", "when", "every", "day", "clear",
            "runny", "running", "sneeze", "sneezing", "have", "got")),
          "A nose that runs all the time is usually an allergy - pollen, dust mites or an animal - "
          "or a rhinitis that comes from cold air, smoke or a spray, and both behave the same way: "
          "a salt water rinse and a steroid nose spray from a pharmacist, used every day for a "
          "fortnight, settle most of it, and an antihistamine helps the itchy, sneezy sort. Keep "
          "the bedroom dusted and the windows shut when the count is high. See a GP if it is only "
          "one side, if there is blood in it, or if it has gone on for months with no cause found.",
          avoid=("dog", "cat", "puppy", "kitten", "pet", "baby", "toddler", "child",
                 "nosebleed", "nose bleed", "bleeding", "broken nose",
                 "spring", "summer", "autumn", "winter", "pollen", "hay fever", "hayfever",
                 "season", "seasonal", "allergy", "allergies", "antihistamine")),

    entry("a-face-puffy-from-crying",
          (("swollen from crying", "puffy from crying", "swollen after crying",
            "puffy after crying", "face is swollen from crying", "face puffy from crying",
            "face is puffy from crying", "swollen with crying", "face swollen with crying",
            "cried so much my face", "crying all night and my face",
            "my face is swollen because i was crying", "eyes are swollen from crying",
            "eyes are puffy from crying", "eyes swollen from crying",
            "lip is swollen after crying", "lip swollen from crying", "lip is puffy from crying",
            "lips are swollen from crying"),
           ("face", "faces", "eyes", "eye", "swollen", "swelling", "puffy", "puffed", "crying",
            "cried", "cry", "sobbing", "sobbed", "what", "help", "how", "stop", "reduce",
            "is", "are", "my")),
          "A face puffed up by crying is the salt in tears and the pressure of it, and it settles "
          "within a few hours. Cold water on a flannel, or a cold spoon held on the puffy places "
          "for five minutes, brings it down fastest, and a glass of water and a sit-down help too. "
          "If it is only one side, painful, or spreading to your lips or tongue, get it looked at "
          "the same day.", 
          avoid=("throat", "tongue", "breath", "breathe", "breathing", "sting",
                 "stung", "bee", "wasp", "nut", "nuts", "peanut", "allergy", "allergic",
                 "dentist", "tooth", "toothache", "gum", "gums", "abscess", "one side", "sine")),

    entry("puffy-eyes",
          (("puffy eyes", "eyes are puffy", "my eyes are puffy", "eye is puffy", "puffy eyelids",
            "swollen eyes", "eyes look puffy", "bags under my eyes", "under eye bags",
            "puffiness under my eyes"),
           ("morning", "mornings", "always", "why", "what", "help", "salt", "sleep", "tired",
            "allergy", "reduce", "get rid", "keep", "wake up", "when i wake", "is it", "worse",
            "have", "got", "are", "look", "looks", "puffy")),
          "Puffy eyes in the morning are usually fluid: too much salt or alcohol the night before, "
          "broken sleep, lying flat, or an allergy, and it settles a couple of hours after you get "
          "up. A cold spoon or flannel on the lids for five minutes, sleeping with your head a "
          "little raised, and going easy on salt in the evening is most of the answer; an "
          "antihistamine at night helps if they itch. See a GP if the puffiness is on one side, is "
          "painful, comes with a red eye, or spreads to your lips or tongue.",
          avoid=("ankle", "ankles", "leg", "legs", "foot", "feet", "baby", "toddler", "child",
                 "dog", "cat", "puppy", "kitten")),

    entry("piles",
          (("piles", "haemorrhoids", "hemorrhoids", "haemorrhoid", "hemorrhoid", "piles are",
            "my piles", "back passage"),
           ("treat", "help", "itch", "itches", "itching", "itchy", "painful", "hurts", "hurt",
            "sore", "bleeding", "bled", "gone", "go away", "went", "cream", "get rid", "serious",
            "normal", "last", "how long", "have", "got", "ive", "i've", "what can i do",
            "what should i do", "lump", "thrombosed", "sitting", "sore",
            "what", "how", "why", "treatment", "cause", "causes", "cured", "cure")),
          "Piles are swollen veins in the back passage: they itch, ache or sting, and often bleed a little when you go. Most settle in a few days. Eat fibre and drink water so you are not straining, don't sit on the loo scrolling, and a pharmacy cream or suppository takes the sting out. See a GP if bleeding keeps up for weeks, if a lump will not go back in, or if it is very painful; dark blood, or blood mixed with the stool, is worth checking sooner.",
          ask=("piles", "haemorrhoids", "hemorrhoids", "haemorrhoid", "hemorrhoid",
               "back passage"),
          guard=_a_heap_not_the_condition,
          avoid=("leaves", "leaf", "washing", "laundry", "paper", "papers", "rubbish", "bin",
                 "bags", "boxes", "books", "clothes", "coal", "wood", "logs", "garden", "lawn",
                 "drive", "shed", "garage", "clutter", "chores", "ironing", "dishes", "snow",
                 "gravel", "soil", "compost", "contract", "tenancy", "landlord",
                 "paperwork", "email", "emails", "inbox", "admin", "messages", "letters",
                 "bills", "unread", "backlog")),
    entry("shingles",
          (("shingles", "shingle rash", "herpes zoster"),
           ("have", "got", "ive", "i've", "think", "painful", "hurts", "hurt", "pain", "rash",
            "blister", "blisters", "itch", "itchy", "last", "how long", "treat", "help", "stop",
            "contagious", "catch", "spread", "started", "start", "back", "side", "chest", "arm",
            "face", "nerve", "burning", "tingling")),
          "Shingles is the chickenpox virus waking along one nerve: burning or tingling on one side, then blisters, settling in two to four weeks. Ring the GP today if the rash is new - an antiviral works best within 72 hours. Seen the same day if it is near an eye or the tip of the nose, in pregnancy, or if your immunity is low. Keep it covered, do not burst the blisters, take paracetamol. You cannot pass on shingles, but you can give chickenpox.",
          ask=("shingles", "shingle rash"),
          avoid=("roof", "roofing", "roofer", "tiles", "tile", "shed", "wall", "walls", "fence",
                 "garden", "house", "drive", "damp", "insulation", "rain", "leak", "chimney")),
    entry("ringworm",
          (("ringworm", "ring worm", "tinea"),
           ("get rid", "treat", "treatment", "cure", "clear", "gone", "itchy", "itching", "itch",
            "spread", "spreading", "arm", "leg", "back", "scalp", "skin", "body", "patch",
            "patches", "ring", "have", "got", "ive", "i've", "how long", "last", "contagious",
            "catch")),
          "Ringworm is a fungus, not a worm: an itchy red ring of scaly skin that clears in the "
          "middle. A pharmacy antifungal cream - clotrimazole or terbinafine - twice a day does "
          "it, and keep using it for a week after the ring has gone or it comes back. Keep the "
          "skin dry, do not share towels, and wash bedding and socks hot. See a GP if it is on "
          "the scalp or the nails, if it is spreading, or if it is no better after two weeks.",
          ask=("ringworm", "ring worm", "tinea"),
          avoid=("dog", "cat", "puppy", "kitten", "pet", "cattle", "horse", "cow")),
    entry("psoriasis",
          (("psoriasis", "psoriatic"),
           ("flaring", "flare", "flares", "bad", "worse", "treat", "help", "itchy", "itch",
            "skin", "elbows", "elbow", "knees", "knee", "scalp", "patches", "patch", "get rid",
            "what helps", "spread", "contagious", "cure", "clear", "have", "got", "ive", "i've",
            "how do i")),
          "Psoriasis is dry, scaly, well-defined patches, most often on elbows, knees and scalp, "
          "and it comes and goes in flares. What helps: a plain emollient daily, a steroid cream "
          "on a flare for a week or two, some daylight on the patches, alcohol and stress down. "
          "It is not contagious and not caused by being unclean. See a GP if it covers a lot of "
          "the body, if your joints are stiff or swollen, or if your cream is not holding it.",
          ask=("psoriasis", "psoriatic"),
          avoid=("dog", "cat", "puppy", "kitten", "pet")),
    entry("thyroid-check",
          (("thyroid", "underactive thyroid", "overactive thyroid", "hypothyroid",
            "hyperthyroid", "hypothyroidism", "hyperthyroidism", "tsh", "levothyroxine"),
           ("could it be", "is my", "is it", "test", "tests", "blood", "check", "checked",
            "tired", "tiredness", "exhausted", "weight", "cold", "hair", "sleep", "sleeping",
            "symptoms", "underactive", "overactive", "doctor", "gp", "problems", "worried",
            "always", "putting on", "losing")),
          "The only way to know is a blood test: ask the GP for thyroid function, TSH plus T4. Go if you are persistently tired, feeling the cold more, or putting on weight without eating more - or the reverse: losing weight, anxious, hot, fast heartbeat. An underactive thyroid is common and treated with one levothyroxine tablet a day, with a repeat test in six to eight weeks to set the dose. Symptoms alone cannot tell you: tiredness has a dozen causes.",
          ask=("thyroid", "hypothyroid", "hyperthyroid", "underactive", "overactive", "tsh",
               "levothyroxine"),
          avoid=("dog", "cat", "puppy", "kitten", "pet", "horse", "boiler", "heating", "car",
                 "engine", "my son", "my daughter", "my child", "baby", "toddler", "pregnant")),
    entry("thyroid-underactive",
          (("underactive", "hypothyroid", "hypothyroidism", "levothyroxine", "thyroxine",
            "thyroid tablets", "borderline"),
           ("my", "i have", "ive", "im", "i am", "on", "doctor", "gp", "said", "diagnosed",
            "taking", "tablet", "tablets", "thyroid", "level", "levels", "result",
            "dose", "doses", "dosage")),
          "An underactive thyroid is treated with one levothyroxine tablet a day, on an empty "
          "stomach half an hour before breakfast, and the dose is set by a blood test six to "
          "eight weeks after you start and then once a year. Do not stop it because you feel "
          "better. Go back sooner if you get palpitations, lose weight without trying, or feel "
          "more tired on the same dose. A borderline result is usually retested before anyone "
          "treats it.",
          ask=("thyroid", "levothyroxine", "thyroxine", "underactive", "hypothyroid", "borderline"),
          bias=6,
          avoid=("i think", "i reckon", "maybe", "wonder", "could it be", "is it my", "do you think",
                 "blood test", "test", "tests", "check", "checked", "normal", "what is",
                 "dog", "cat", "puppy", "kitten", "pet", "horse", "child", "baby", "toddler",
                 "pregnant")),
    entry("thyroid-overactive",
          (("overactive", "hyperthyroid", "hyperthyroidism", "carbimazole", "graves"),
           ("my", "i have", "ive", "im", "i am", "on", "doctor", "gp", "said", "diagnosed",
            "taking", "tablet", "tablets", "thyroid", "eat", "eating", "diet", "food",
            "lost", "losing", "weight")),
          "An overactive thyroid is treated with carbimazole or propylthiouracil, sometimes with "
          "radioiodine or surgery, and the dose is set on blood tests every few weeks at first. "
          "Eat regularly rather than cutting back - it burns through energy, so weight loss is the "
          "thyroid, not the diet - and go back sooner if your heart races, your hands shake, or "
          "your eyes feel gritty or look different.",
          ask=("thyroid", "overactive", "hyperthyroid", "carbimazole", "graves"),
          bias=6,
          avoid=("i think", "i reckon", "maybe", "wonder", "could it be", "is it my", "do you think",
                 "blood test", "test", "tests", "check", "checked", "normal", "what is a thyroid",
                 "dog", "cat", "puppy", "kitten", "pet", "horse", "child", "baby", "toddler",
                 "pregnant")),
]

from .costs import time_entries
ENTRIES += time_entries("dentist", "eye-test", "gp-appointment", "physio")


def _a_rate_reading(memory, reading):
    said = str(reading.get("text") or reading.get("clean") or "").lower()
    device = any(word in said for word in (
        "watch", "fitbit", "garmin", "tracker", "smartwatch", "smart watch", "band", " app"))
    given = None
    for number in reading.get("numbers") or []:
        value = number.get("value") if isinstance(number, dict) else None
        if isinstance(value, (int, float)) and not isinstance(value, bool):
            if 25 <= value <= 250:
                given = int(value)
                break
    if any(word in said.replace("'", " ").split() for word in (
            "kid", "kids", "son", "sons", "daughter", "daughters", "boy", "boys", "girl",
            "girls", "teen", "teens", "teenager", "teenagers", "children", "child", "baby")):
        return ("A child's resting heart rate is higher than an adult's: about 100 to 160 in a "
                "baby, 90 to 150 up to three, 80 to 140 up to six, 70 to 120 up to nine, and 60 "
                "to 100 from about ten. One reading off a watch is usually the moment rather "
                "than the heart, so take it again sitting still; a fast rate that comes with "
                "fever, drowsiness or fast breathing needs a doctor the same day.")
    letters_asked = any(phrase in said for phrase in (
        "mean", "means", "stand for", "stands for", "what does", "whats", "short for",
        "abbreviation", "spell"))
    spread = re.search(r"(\d{2,3})\s*(?:to|-|–)\s*(\d{2,3})", said)
    too_slow = given is not None and given < 60
    if letters_asked and ("bpm" in said or "beats per minute" in said):
        opening = ("BPM is beats per minute, the number of times your heart beats in a minute, and "
                   "one reading is usually the moment rather than the heart")
    elif letters_asked and ("hr" in said.split() or "hr" in said.replace("'", " ").split()):
        opening = "HR is heart rate, and one reading is usually the moment rather than the heart"
    elif letters_asked and device:
        opening = ("On a watch, HR is heart rate, and one reading is usually the moment rather "
                   "than the heart")
    elif spread:
        low, high = int(spread.group(1)), int(spread.group(2))
        opening = ("%d to %d beats a minute is the resting range, so it is where your own number "
                   "sits inside that range that matters rather than one reading" % (low, high))
    elif too_slow:
        opening = ("A heart rate of %d is at the slow end, and a slow resting pulse is normal in "
                   "people who are fit and in sleep" % given)
    elif given is not None and device:
        opening = ("A heart rate of %d on a watch is one reading, and it is usually the moment "
                   "rather than the heart" % given)
    elif given is not None:
        opening = ("A heart rate of %d is one reading, and it is usually the moment rather than "
                   "the heart" % given)
    elif any(word in said.replace("'", " ").split() for word in (
            "high", "higher", "highs", "elevated", "raised")):
        opening = ("A high heart rate means over 100 beats a minute at rest, and one reading is "
                   "usually the moment rather than the heart")
    elif any(word in said.split() for word in ("low", "lower", "slow")):
        opening = ("A low heart rate means under 60 beats a minute at rest, and one reading is "
                   "usually the moment rather than the heart")
    else:
        opening = "HR is heart rate, and one reading is usually the moment rather than the heart"
    if too_slow and not spread and not letters_asked:
        return (opening + ": rest, 60 to 100 beats a minute is normal, and 50 is ordinary for a "
                "regular runner. Take it again sitting still for five minutes; under 50 with "
                "dizziness, fainting or unusual tiredness, or any reading with chest pain or "
                "breathlessness, is a doctor's call.")
    return (opening + ": "
            "coffee, a hot shower, a late night or being unwell push it up, so sit still five "
            "minutes and take it again. Resting, 60 to 100 beats a minute is normal, and a rate "
            "that stays over 100 sitting still, one that stays under 50 and leaves you dizzy, or "
            "any reading with chest pain or breathlessness, is a doctor's call.")


_MEANS = re.compile(r"\b(?:mean|means|meaning|stand for|stands for)\b")
_A_RATE_NAMED_HIGH_OR_LOW = frozenset((
    "high", "higher", "highest", "low", "lower", "lowest", "elevated", "raised", "spike",
    "spiked", "spikes"))


def _not_the_meaning_of_high_or_low(understood):
    if not isinstance(understood, dict):
        return True
    words = understood.get("words")
    if not isinstance(words, (list, tuple, set, frozenset)):
        words = ()
    clean = understood.get("clean") or ""
    return not (_MEANS.search(clean) and _A_RATE_NAMED_HIGH_OR_LOW.intersection(words))


ENTRIES.append(entry(
    "resting-heart-rate",
    (("heart rate", "resting heart rate", "pulse", "pulse rate", "bpm", "beats per minute"),
     ("normal", "average", "should it be", "what is", "whats", "what should", "range", "resting",
      "rest", "healthy", "good", "too high", "too low", "check", "measure", "take my",
      "is that ok", "is it ok", "is that normal", "low", "slow", "fast", "worry")),
    "A normal resting heart rate for an adult is 60 to 100 beats a minute, and most people sit "
    "between 60 and 80; fitter people run lower, and 50 is normal for a regular runner. Take it "
    "properly: sit quietly for five minutes, find the pulse on the thumb side of the wrist, and "
    "count for 30 seconds then double it. A rate that stays over 100 at rest, drops under 60 with "
    "dizziness or fainting, or is irregular should be checked by a doctor rather than watched.",
    avoid=("blood pressure", "bp", "palpitations", "racing", "pounding", "skipping", "chest",
           "faint", "fainted", "passed out", "dizzy", "short of breath", "breathless",
           "kid", "kids", "son", "sons", "daughter", "daughters", "boy", "girl",
           "teen", "teens", "teenager", "teenagers", "children", "child", "baby",
           "watch", "fitbit", "watch says", "apple watch", "smart watch"),
    guard=_not_the_meaning_of_high_or_low))

ENTRIES.append(entry(
    "heart-rate-on-a-watch",
    (("heart rate", "hr", "pulse", "bpm", "beats per minute"),
     ("watch", "watch says", "apple watch", "smart watch", "smartwatch", "fitbit", "garmin",
      "tracker", "band", "app", "says", "shows", "reading", "reading is", "120", "130", "140",
      "150", "160", "170", "meaning", "mean", "stand for", "stands for",
      "is my heart rate", "heart rate is", "heart rate was", "pulse is", "pulse was",
      "hr of", "hr is", "is it too", "ive got a", "i have a")),
    _a_rate_reading,
    avoid=("blood pressure", "bp", "palpitations", "racing", "pounding", "skipping", "chest pain",
           "faint", "fainted", "passed out", "dizzy", "short of breath", "breathless",
           "toddler", "pregnancy", "pregnant", "fever", "temperature",
           "normal", "average", "range", "too high", "too low", "is that normal", "how long",
           "why", "run", "running", "exercise", "gym", "workout", "working out",
           "cycling", "walking", "cardio", "during", "after")))

ENTRIES.append(entry(
    "heart-rate-high",
    (("heart rate", "pulse", "pulse rate"),
     ("why", "high", "higher", "highest", "raised", "went up", "goes up", "spike", "spikes",
      "spiked", "jumps", "jumped", "morning", "over 100")),
    "A high reading is usually the moment rather than the heart: a late night or alcohol, "
    "dehydration, a hot room, coffee, standing up quickly, a stressful start to the day or an "
    "illness coming on will all lift it, and the body's own waking-up hormones lift it too. Sit "
    "for five minutes and take it again, because 60 to 100 at rest is normal. A rate that stays "
    "over 100 sitting still, or comes with chest pain, breathlessness or fainting, is a doctor's "
    "call rather than another reading.",
    avoid=("watch", "fitbit", "garmin", "tracker", "smart watch", "smartwatch", "band",
           "app", "says", "shows", "120", "130", "140", "150", "mean", "stand for",
           "blood pressure", "bp", "palpitations", "racing", "pounding", "skipping", "chest pain",
           "faint", "fainted", "passed out", "dizzy", "short of breath", "breathless",
           "baby", "child", "toddler", "pregnancy", "pregnant",
           "kid", "kids", "son", "sons", "daughter", "daughters", "boy", "girl",
           "teen", "teens", "teenager", "teenagers", "children",
           "fever", "temperature",
           "coffee", "coffees", "caffeine", "espresso", "energy drink", "energy drinks",
           "normal", "average", "range", "too high", "too low", "is that normal", "what is")))

ENTRIES.extend([
    entry("coffee-dehydration",
          (("coffee", "coffees", "tea", "caffeine", "energy drink", "energy drinks", "cola",
            "coke", "espresso", "latte"),
           ("dehydrate", "dehydrated", "dehydration", "dehydrating", "diuretic", "fluid",
            "fluids", "hydration", "water", "pee", "urine", "dry",
            "count as water", "counts as water", "count as a drink", "counts as a drink",
            "count as fluid", "counts as fluid", "count as fluids", "counts as fluids",
            "count towards", "counts towards", "part of my fluids")),
          "No, not in ordinary amounts: a cup of tea or coffee is mostly water, and the caffeine "
          "in it makes you pass only a little more than the drink gave you, so it counts towards "
          "your fluids. The six-to-eight-glasses figure includes them. Strong coffee on an empty "
          "stomach can still leave you headachy and jittery, and if you are thirsty water is still "
          "the better drink.",
          avoid=("machine", "machines", "grinder", "beans", "pods", "pod", "descale", "limescale",
                 "how do i make", "how to make", "recipe", "frother", "milk", "latte art",
                 "sleep", "insomnia", "bedtime", "at night", "before bed", "pregnant",
                 "pregnancy", "heart", "palpitations", "anxiety", "withdraw", "withdrawal",
                 "quit", "give up", "stain", "stains", "spill", "stomach", "acidity",
                 "dog", "cat", "baby", "child", "toddler")),
    entry("swimmers-ear", (("ear infection", "ear infections", "sore ear", "earache", "ear"),
                           ("swim", "swimming", "swimmer", "pool", "sea", "lake", "after swimming",
                            "water in my ear")),
          "An ear that aches and feels blocked after swimming is usually swimmer's ear: water sits "
          "in the canal and the skin gets sore and infected. Keep it dry for a few days, use "
          "painkillers, and let a pharmacist look at it - drops help, but only the right ones, and "
          "not if you have ever had a perforated eardrum. See a GP if there is discharge, fever or "
          "real pain.",
          bias=1,
          avoid=("wax", "ringing", "tinnitus", "cant hear", "can't hear", "hearing", "deaf",
                 "baby", "child", "toddler", "kid", "dog", "cat", "piercing", "itching only",
                 "how long can i", "how long can you")),
    entry("heavy-legs", (("leg", "legs", "calves", "calf"),
                         ("heavy", "heaviness", "weighing a ton", "weigh a ton", "tired",
                          "aching", "achy", "leaden", "drained")),
          "Heavy legs by the evening are usually blood and fluid pooling from sitting or standing "
          "a long time: walk about every hour, put your feet up above hip height for twenty "
          "minutes, and cut back on salt. Compression socks help if it happens most days, and "
          "strong calf muscles do more than anything - calf raises and a daily walk push the "
          "blood back up. See a GP if one leg is swollen, hot or red, if the heaviness is there "
          "in the morning too, or if it comes with breathlessness; and if you are on the pill or "
          "just off a flight and one calf is painful, ring 111 the same day.",
          avoid=("swollen", "swelling", "swell", "puffy", "puffiness", "oedema", "fluid",
                 "cramp", "cramps", "cramping", "restless", "twitch", "twitching",
                 "grown", "growing", "growth", "growth spurt", "growing pains", "shooting up",
                 "grown so fast", "growing so fast", "spurt",
                 "numb", "numbness", "pins and needles", "sciatica", "varicose",
                 "clot", "dvt", "one leg", "red and hot", "hot and red", "hot",
                 "after a run", "after my run", "after the gym", "gym", "workout",
                 "chair", "table", "sofa", "bed", "tripod", "stand", "camera"),
          bias=2),
    entry("swollen-ankles", (("ankles", "ankle", "feet", "foot", "legs", "leg"),
                             ("swell", "swells", "swollen", "swelling", "puffy", "puffiness",
                              "fluid", "oedema", "tight shoes"),
                             ("night", "evening", "by the evening", "end of the day",
                              "at my desk", "sitting", "standing", "long flight", "flight")),
          "Ankles that puff up through the day and go down overnight are usually fluid pooling "
          "from sitting or standing a long time, hot weather or a long flight. Walk about every "
          "hour, put your feet up above hip height and cut back on salt. Ankles puffy on both "
          "sides can also come from a tablet or from the heart. Ring 111 today if an ankle is "
          "hot, red and spreading, or painful on just one side, and see a GP if it is one leg "
          "only, comes on suddenly, or comes with breathlessness.",
          bias=1,
          ask=("night", "evening", "by the evening", "end of the day", "at the end of the day",
               "in the heat", "hot weather", "at my desk", "sitting", "standing", "all day",
               "on my feet", "flight", "fly", "flying"),
          avoid=("sprained", "sprain", "twisted", "injury", "broke", "broken", "fracture",
                 "cramp", "cramps", "cramping", "charley horse",
                 "dog", "cat", "horse", "pregnant", "pregnancy", "feet smell", "smelly",
                 "blister", "verruca", "athlete", "plantar", "heel",
                 "hot", "clot", "clots", "calf", "dvt", "thrombosis", "warm to touch")),
])

_A_PRESSURE_IN_A_PIPE = (
    "shower", "showers", "tap", "taps", "boiler", "boilers", "radiator", "radiators", "pipe",
    "pipes", "plumbing", "hose", "hosepipe", "sprinkler", "irrigation", "pump", "pumps",
    "pressure washer", "jet wash", "washer", "washing machine", "dishwasher", "tyre", "tyres",
    "tire", "tires", "gas", "cylinder", "combi", "central heating", "stopcock", "stop cock",
    "water butt", "water tank", "header tank", "mains",
)
_BLOOD_WORDS = ("blood", "bp", "hypotension", "dizzy", "dizziness", "faint", "fainting",
                "lightheaded", "light headed", "black out", "blackout", "reading")


def _not_a_pressure_in_a_pipe(understood):
    said = " ".join(str(one) for one in ((understood or {}).get("words") or ())).lower()
    if not said:
        said = str((understood or {}).get("clean") or (understood or {}).get("text") or "").lower()
    if not said:
        return True
    if any(word in said for word in _BLOOD_WORDS):
        return True
    return not any(word in said for word in _A_PRESSURE_IN_A_PIPE)


ENTRIES.append(entry(
    "low-blood-pressure",
    (("blood pressure", "bp", "low pressure", "hypotension"),
     ("low", "too low", "drop", "dropped", "drops", "fall", "fell", "down",
      "95 over 60", "90 over 60", "85 over 55", "80 over 50", "100 over 60", "90 over 50",
      "is 95", "is 90", "is 85", "is 80", "is that ok", "is that low", "is it low",
      "worried", "worry", "what is", "whats", "should")),
    ("Under 90/60 is a low reading, and on its own it often means nothing: plenty of healthy "
     "people run at 100/60 all their lives. How you feel is what counts - dizzy or black-visioned "
     "on standing up, light-headed, sick, confused, or actually fainting means it is too low for "
     "you. When it happens, sit or lie down with your feet up, then get up slowly; drink a large "
     "glass of water and don't skip meals. A new or bigger dose of a blood pressure tablet, a "
     "water tablet, some antidepressants, and dehydration from a bug or a hot day are the usual "
     "causes, so ask a pharmacist to go through your medicines. Fainting with an injury, "
     "confusion, chest pain or black stools is 999 or A&E."),
    guard=_not_a_pressure_in_a_pipe,
    avoid=("high", "higher", "140", "150", "160", "170", "180", "stroke", "lower it",
           "bring it down", "get it down", "reduce it", "too high",
           "normal", "healthy", "average", "range")))


ENTRIES.append(entry(
    "contact-lens-stuck",
    (("contact lens", "contact lenses", "my lens", "my lenses", "contacts", "soft lens",
      "daily lens", "monthly lens", "lens"),
     ("stuck", "wont come out", "wont come off", "cant get it out", "cant get it off",
      "cant get it", "cant remove", "not coming out", "will not come out", "lost",
      "went behind", "gone behind", "behind my eye", "folded", "disappeared", "up under",
      "stuck in my eye", "dry", "scratchy", "irritated", "wont budge",
      "cant get", "cannot get", "couldnt get", "cant take", "get out", "get them out",
      "wont come away", "stuck under")),
    ("It cannot go behind your eye - that one is a myth: it has folded up under the upper or "
     "lower lid. Wash your hands, put in a couple of saline or rewetting drops and blink, then "
     "look up, pull the upper lid gently down over the lower lashes and look down; the lens "
     "usually slides out onto your cheek. If it is still there, slide it with the pad of a clean "
     "finger to the white of the eye where it is easier to pinch, and lift it off between thumb "
     "and forefinger - never a nail, tweezers or a cotton bud. Still stuck after half an hour, "
     "or the eye is painful, red or your sight has gone blurred, go to an optician or eye "
     "casualty the same day and take your lens case with you. Don't sleep in it."),
    avoid=("spectacles", "glasses", "prescription", "buy", "cheap", "cost", "solution",
           "bleach", "chemical", "grit", "dust",
           "dry", "gritty", "itchy", "sore", "uncomfortable", "feel")))


ENTRIES.append(entry(
    "inhaler-out-of-date",
    (("inhaler", "inhalers", "blue inhaler", "brown inhaler", "ventolin", "salbutamol",
      "preventer", "reliever", "puffer"),
     ("out of date", "expired", "expire", "expires", "past its date", "past the date",
      "old", "date", "still use", "still work", "safe", "ok to use", "use it", "throw",
      "bin", "replace", "run out", "last")),
    ("An out-of-date blue inhaler is not dangerous, and it is not empty either: salbutamol keeps "
     "most of its strength well past the date on the canister, so if you are wheezy and it is the "
     "only one in the house, use it. Then order a replacement this week - the dose weakens with "
     "age and the propellant runs down. If it is a brown preventer past its date, replace that "
     "first, because it is the one doing the work every day. If you are reaching for the blue one "
     "more than three times a week, the thing to book is an asthma review rather than a new "
     "inhaler: a preventer that suits you should mean you hardly need it."),
    avoid=("attack", "cant breathe", "can't breathe", "cannot breathe", "999", "ambulance",
           "blue lips", "nebuliser", "cold", "winter", "frost")))

ENTRIES.append(entry(
    "talking-therapy",
    (("therapist", "therapists", "therapy", "counsellor", "counsellors", "counselor",
      "counselors", "counselling", "counseling", "psychologist", "psychotherapy",
      "talking therapy", "talking treatment", "cbt", "mental health", "my mental health",
      "talking therapies", "psychiatrist", "psychiatry"),
     ("how do i", "how can i", "how to", "find", "get", "got", "see", "seeing", "refer",
      "referral", "referred", "nhs", "free", "private", "where", "start", "ask", "book",
      "booked", "waiting", "wait", "waiting list", "cost", "costs", "price", "expensive",
      "cheap", "help", "help for", "should i", "need", "need to")),
    ("Ask your GP to refer you, and in England you can also send yourself to an NHS talking "
     "therapies service online without seeing a GP first. Say what you want help with and ask "
     "for it by name - CBT for anxiety or low mood, counselling, or a specific service - because "
     "a named referral gets a date and a vague one sits on a list, and ask how long the wait is "
     "and what you can do meanwhile. Private therapy runs about £40 to £70 a session: check "
     "the therapist is on the BACP, UKCP or BABCP register, and ask about a lower-cost first "
     "session or a trainee rate. If money is the block, ask a charity or a university training "
     "clinic about low-cost counselling."),
    avoid=("couples", "couple", "marriage", "married", "partner", "relationship", "relate",
           "divorce", "affair", "grief", "bereavement", "bereaved", "died", "death",
           "physiotherapist", "physiotherapy", "physio", "osteopath", "chiropractor",
           "occupational", "speech", "speech therapy", "speech and language", "massage",
           "aromatherapy", "cognitive behavioural", "what is cbt", "what does cbt",
           "kill myself", "suicide", "suicidal", "self harm", "self-harm", "999", "a&e",
           "hospital", "sectioned", "section")))

ENTRIES.append(entry(
    "medicine-out-of-date",
    (("tablets", "tablet", "pills", "pill", "medicine", "medicines", "medication",
      "prescription", "paracetamol", "ibuprofen", "painkillers", "antibiotics", "antibiotic",
      "insulin", "eye drops", "cough syrup", "calpol", "nurofen", "antihistamine", "vitamins",
      "supplements", "epipen", "epi pen"),
     ("out of date", "expired", "expire", "expires", "past its date", "past the date",
      "use by", "best before", "old", "still use", "still good", "still ok", "safe",
      "ok to use", "take it", "throw", "bin", "replace", "keep")),
    ("A dry tablet keeps its strength for a long time past the date on the box, and paracetamol "
     "that has sat in a cupboard is usually still fine to take; a pharmacist will check any you "
     "take every day. What does not keep is anything wet: insulin, eye drops, opened liquids and "
     "cough syrup lose their strength and can grow bacteria, so replace those rather than use "
     "them. Never flush old medicines down the loo or put them in the bin - hand them in at any "
     "pharmacy, which takes them for free."),
    avoid=("inhaler", "inhalers", "ventolin", "salbutamol", "preventer", "reliever", "puffer",
           "attack", "cant breathe", "can't breathe", "overdose", "too many", "how many",
           "dose", "dosage", "mg", "child", "baby", "toddler", "pregnant", "pregnancy",
           "breastfeeding", "buy", "price", "cheaper", "prescription cost", "addicted",
           "withdrawal", "side effect", "side effects")))

ANTIBIOTICS = ("antibiotic", "antibiotics", "penicillin", "amoxicillin", "flucloxacillin",
               "erythromycin", "clarithromycin", "doxycycline", "trimethoprim", "nitrofurantoin",
               "metronidazole", "tinidazole", "ciprofloxacin", "cephalexin", "course of tablets")
THE_PILL = ("the pill", "my pill", "birth control", "contraceptive", "contraception",
            "mini pill", "combined pill", "microgynon", "rigevidon", "cerazette",
            "implant", "coil")
ANTIDEPRESSANTS = ("antidepressant", "antidepressants", "ssri", "ssris", "sertraline",
                   "fluoxetine", "citalopram", "escitalopram", "paroxetine", "venlafaxine",
                   "mirtazapine", "prozac")
NSAIDS = ("ibuprofen", "nurofen", "brufen", "naproxen", "diclofenac", "voltarol", "aspirin",
          "anti inflammatory", "nsaid", "nsaids")
ASTHMA = ("asthma", "asthmatic", "wheeze", "wheezing", "salbutamol", "ventolin", "inhaler",
          "inhalers")
ANTACIDS = ("antacid", "antacids", "gaviscon", "rennie", "rennie's", "indigestion tablet",
            "indigestion tablets", "omeprazole", "lansoprazole", "esomeprazole", "ranitidine",
            "heartburn tablet", "heartburn tablets")
IRON = ("iron", "iron tablet", "iron tablets", "ferrous", "ferrous sulphate", "iron supplement",
        "iron supplements")
ANTIHISTAMINES = ("antihistamine", "antihistamines", "hayfever tablet", "hayfever tablets",
                  "hay fever tablet", "hay fever tablets", "cetirizine", "loratadine",
                  "fexofenadine", "piriton", "chlorphenamine", "beconase")
BLOOD_PRESSURE = ("blood pressure", "blood pressure tablet", "blood pressure tablets",
                  "blood pressure medication", "blood pressure pills", "ramipril", "amlodipine",
                  "lisinopril", "bisoprolol", "water tablet", "water tablets", "diuretic")

_ANTACID_MIND_THE_GAP = ("iron", "ferrous", "levothyroxine", "thyroid", "ciprofloxacin",
                         "norfloxacin", "tetracycline", "doxycycline", "antibiotic",
                         "antibiotics", "malaria", "osteoporosis", "alendronic")


def _an_antacid_with_another_tablet(memory, reading):
    line = " ".join(str((reading or {}).get("text") or "").split()).lower()
    if any(word in line for word in _ANTACID_MIND_THE_GAP):
        return ("An antacid can stop that tablet being taken up properly. Iron, levothyroxine and "
                "the antibiotics ciprofloxacin, norfloxacin, tetracycline and doxycycline are the "
                "ones that matter most, and so are alendronate and the other bone tablets. Leave "
                "two hours between the antacid and the other tablet - the leaflet in the box says "
                "for that medicine how long the gap should be.")
    return ("Most tablets are fine with an antacid. The ones that are not are iron, levothyroxine, "
            "alendronate and the antibiotics ciprofloxacin, norfloxacin, tetracycline and "
            "doxycycline: those want two hours between the antacid and the tablet. Paracetamol, "
            "ibuprofen, blood pressure tablets and antidepressants are not affected.")



def _a_painkiller_with_an_antidepressant(memory, reading):
    line = " ".join(str((reading or {}).get("text") or "").split()).lower()
    if any(word in line for word in ("codeine", "co-codamol", "co codamol", "tramadol")):
        return ("Codeine is usually fine with an SSRI for a few days: the things to watch are "
                "constipation and drowsiness, so no driving on it, and if you need more than a "
                "few days' worth ask about something else. Tramadol is the one not to mix with an "
                "SSRI - the two together can bring on too much serotonin - and none of them "
                "belong with an MAOI.")
    if any(word in line for word in ("paracetamol", "painkiller", "painkillers", "pain relief",
                                     "headache")):
        return ("Paracetamol is the painkiller to use with an SSRI antidepressant - it is not the "
                "one the combination is about. Codeine is usually fine too, in the dose on the "
                "packet and for a few days rather than weeks. An anti-inflammatory is the one to "
                "ask about: ibuprofen, naproxen and aspirin add to the bleeding risk an SSRI "
                "already carries, so paracetamol first.")
    return ("An anti-inflammatory on top of an SSRI antidepressant raises the risk of bleeding in "
            "the stomach a little, because both thin the blood in different ways. Paracetamol is "
            "the painkiller to reach for first. If you do need ibuprofen, take it with food at the "
            "lowest dose that works, and get seen if you have a pain high in the stomach, black "
            "tarry poo, or you bruise and bleed more than you used to.")


TOGETHER = (
    ((ANTIBIOTICS, ("alcohol", "drink", "drinking", "beer", "wine", "pint", "pints", "booze")),
     "Most antibiotics are fine with a drink. The two that are not are metronidazole and "
     "tinidazole, which react with alcohol and leave you flushed, sick and pounding - if the "
     "label on yours says to avoid alcohol, keep off it until 48 hours after the last dose. "
     "Anything else, a glass with your meal is not a problem."),
    ((THE_PILL, ANTIBIOTICS),
     "Only rifampicin and rifabutin make the pill less reliable; ordinary antibiotics such as "
     "amoxicillin do not, and that old warning has been dropped. What does matter is a bad "
     "stomach: if you are sick within two hours of taking a pill, or have severe diarrhoea, "
     "follow the leaflet in your packet - usually another pill, and condoms for the next seven "
     "days. Ask a pharmacist if you are on rifampicin."),
    ((ANTIDEPRESSANTS, NSAIDS + ("paracetamol", "painkiller", "painkillers", "pain relief",
                                  "co-codamol", "co codamol", "codeine", "headache")),
     _a_painkiller_with_an_antidepressant),
    ((ASTHMA, NSAIDS),
     "Aspirin and ibuprofen set off an attack in the minority of people with asthma who react to "
     "them, and nobody knows which they are until it happens. If you have taken them before with "
     "no trouble, they are usually fine; if you have ever wheezed after one, or your asthma is "
     "bad at the moment, paracetamol is the one to use."),
    ((ANTACIDS, ("tablets", "tablet", "pills", "pill", "medicine", "medicines", "medication",
                 "prescription", "levothyroxine", "thyroid", "antibiotics", "antibiotic",
                 "antibiotic tablets", "paracetamol", "ibuprofen", "iron")),
     _an_antacid_with_another_tablet),
    ((IRON, ("tea", "coffee", "milk", "cheese", "calcium", "cup of tea", "milky",
             "orange juice", "vitamin c")),
     "Tea and coffee cut how much iron you take up, and so do milk, cheese and calcium tablets; "
     "vitamin C does the opposite. Take the iron with water or a glass of orange juice, an hour "
     "before food or two hours after, and leave an hour between the tablet and a cup of tea."),
    ((ANTIHISTAMINES, BLOOD_PRESSURE),
     "Most antihistamines are fine with blood pressure tablets - loratadine and cetirizine are "
     "the ones that do not make you drowsy. The thing to avoid is a decongestant: pseudoephedrine "
     "and phenylephrine, in the tablets and sprays sold for a blocked nose, push your blood "
     "pressure up. Buy one that says antihistamine only, and ask about a steroid nasal spray."),
)

_PAIR_BIAS = {}



TOGETHER = TOGETHER + (
    ((ANTIHISTAMINES, ("every day", "daily", "long term", "for months", "all summer", "all year",
                       "two", "double", "double up", "more than one", "keep taking", "safe",
                       "years")),
     "One antihistamine a day is fine for months on end - through the whole pollen season if that "
     "is what it takes - and loratadine and cetirizine are the two that do not make you drowsy. "
     "What not to do is take two different ones at once to double the effect; if one at full dose "
     "is not enough, add a steroid nasal spray or eye drops, or ask about montelukast. A sedating "
     "one such as chlorphenamine is the wrong choice for daytime use."),
    ((("laxative", "laxatives", "senna", "movicol", "lactulose", "dulcolax", "bisacodyl",
       "fybogel", "fibergel", "fibre drink", "stool softener"),
      ("how long", "every day", "long term", "safe", "addicted", "addiction", "depend",
       "dependent", "weeks", "months", "regularly", "keep taking", "daily")),
     "Bulk-forming ones - Fybogel, Movicol, lactulose - are the ones that can be taken for weeks "
     "or months, with plenty of water, because they work like fibre. Stimulant ones - senna and "
     "bisacodyl - are for a few days at a time; taken every day they leave you needing them. They "
     "do not damage the bowel and they are not addictive in the way people fear, but if you need "
     "one most weeks the answer is the diet and a GP visit rather than a bigger dose."),
)

TOGETHER = TOGETHER + (
    ((THE_PILL, NSAIDS + ("paracetamol", "painkiller", "painkillers", "pain relief",
                          "co-codamol", "co codamol")),
     "No painkiller on the shelf affects the pill. Paracetamol, ibuprofen, aspirin and codeine do "
     "not make it less reliable, and neither does an antacid or a hayfever tablet. The two things "
     "that do are rifampicin and rifabutin, and the other is a bad stomach - if you are sick "
     "within two hours of a pill or have severe diarrhoea, follow the leaflet in the packet."),
    ((ANTIDEPRESSANTS, ("alcohol", "drink", "drinking", "beer", "wine", "pint", "pints", "booze")),
     "A drink with an SSRI is not dangerous in the way people fear, but it makes you drowsier and "
     "flattens your mood the next day, and the newer antidepressants mostly say avoid it. With "
     "mirtazapine or an older tricyclic the sedation doubles, so one drink is the sensible limit "
     "and none in the first fortnight while you are settling on the dose. Never with an MAOI."),
    ((BLOOD_PRESSURE, NSAIDS),
     "Ibuprofen and the other anti-inflammatories push blood pressure up a little and blunt the "
     "tablets that are meant to bring it down, so paracetamol is the painkiller to use if you "
     "take one every day. A single dose for a headache is not the problem; a week of them is. "
     "Ask a pharmacist if you need an anti-inflammatory for more than a few days."),
    ((ANTIBIOTICS, ("paracetamol", "painkiller", "painkillers", "pain relief", "ibuprofen",
                    "nurofen", "calpol")),
     "Paracetamol and ibuprofen are fine with antibiotics - take them as it says on each packet, "
     "and they help with the fever and the aches while the antibiotic gets on with the infection. "
     "The one to mention at the counter is warfarin, some antibiotics change how it works, and "
     "antacids, which need two hours between them and the antibiotic."),
)

VITAMINS = ("vitamin", "vitamins", "vitamin d", "vitamin c", "multivitamin", "multivitamins",
            "supplement", "supplements", "cod liver oil", "omega 3", "fish oil", "magnesium",
            "zinc", "folic acid", "calcium tablet", "calcium tablets", "probiotic")
ST_JOHNS_WORT = ("st johns wort", "st john's wort", "st johns", "hypericum", "herbal remedy",
                 "herbal", "herbal medicine", "echinacea", "ginkgo", "saw palmetto")

TOGETHER = TOGETHER + (
    ((VITAMINS, ("blood pressure", "blood pressure tablets", "tablets", "tablet", "medication",
                 "medicine", "prescription", "warfarin", "antibiotics", "statin", "statins",
                 "thyroid", "levothyroxine", "antidepressant")),
     "Most supplements are fine with most tablets: vitamin D, vitamin C, a multivitamin, cod "
     "liver oil and a probiotic can be taken alongside blood pressure tablets, statins, "
     "levothyroxine and antibiotics. The two that need care are vitamin K, which works against "
     "warfarin, and calcium or iron tablets, which want four hours between them and a thyroid "
     "tablet. Ask about anything that calls itself a herbal remedy."),
    ((ST_JOHNS_WORT, ANTIDEPRESSANTS + THE_PILL + ("warfarin", "medicine", "medication",
                                                   "tablets", "prescription", "any")),
     "St John's wort is a real drug and it argues with several: it makes the pill less reliable, "
     "it cuts the level of warfarin and of some heart and transplant drugs, and with an SSRI it "
     "can push serotonin too high. Leave it out if you are on any of those, and tell a pharmacist "
     "you take it before you start anything new - people forget it counts as a medicine."),
)

_JAUNDICE_NEWBORN = (
    "A newborn who is yellow in the first 24 hours, or too sleepy to feed, is 111 now. Yellow "
    "skin or yellow eye whites in an older baby or an adult is jaundice: bilirubin, the waste the "
    "liver clears, has built up, and a GP sees you today - it can be the liver, the gallbladder or "
    "the blood, and the blood tests are the same day. A&E for confusion, vomiting blood, black "
    "tarry stools or bad tummy pain.")
_JAUNDICE_ADULT = (
    "Yellow skin, or the whites of the eyes turning yellow, is jaundice: bilirubin, the waste the "
    "liver clears, has built up. See a GP today, not next week - it can be the liver, the "
    "gallbladder or the blood, and the blood tests are the same day. Say when it started and "
    "about pale stools, dark urine or itching. A&E for confusion, vomiting blood, black tarry "
    "stools or bad tummy pain. A yellow newborn in the first 24 hours is 111 now.")


def _jaundice_card(memory, understood):
    if not isinstance(understood, dict):
        return _JAUNDICE_ADULT
    t = str(understood.get("text") or understood.get("clean")
            or understood.get("norm_text") or "").lower()
    if any(w in t for w in ("baby", "babies", "newborn", "newborns", "infant", "infants")):
        return _JAUNDICE_NEWBORN
    return _JAUNDICE_ADULT


_JAUNDICE_SKIN = re.compile(
    r"\b(?:skin|eyeb?all|eyes?|whites|face|body|complexion|all over|lips?|tongue"
    r"|jaundice|jaundiced|mouth"
    r"|baby|babies|newborn|newborns|infant|infants)\b")
_CHANGE_SUBJECT = re.compile(
    r"\b(?:i|he|she|you|skin|face|body|complexion|whites|eyeb?all|eyes?|lips?|tongue|mouth|palms?"
    r"|hands?|fingers?|arms?|legs?|feet|foot|toes?|son|daughter|child|children|baby|babies"
    r"|newborn|newborns|infant|infants|kid|kids|husband|wife|partner|mum|mom|mother|dad|father"
    r"|nan|grandad|grandma|grandpa|friend|man|woman|boy|girl)"
    r"(?:\s+\w+){0,2}\s+(?:gone|went|turned|turning|going|got|getting|look|looks|looking"
    r"|is|are|am|was|were)\b")
_WASTE = re.compile(r"\b(?:poo|poos|stool|stools|urine|wee|faeces|feces)\b")
_EYE_TROUBLE = re.compile(r"\b(?:itch|itchy|itching|itches|gritty|sticky|watery|watering|"
                          r"pinkeye|conjunctivitis|red)\b")
_SKIN_ITSELF = re.compile(r"\b(?:skin|face|body|complexion|whites|eyeballs?|all over)\b")


def _the_colour_is_on_the_skin(understood):
    said = str((understood or {}).get("clean") or (understood or {}).get("text") or "").lower()
    if _WASTE.search(said) and not re.search(r"\b(?:skin|eyes?|eyeb?all|whites|face)\b", said):
        return False
    if _EYE_TROUBLE.search(said) and not _SKIN_ITSELF.search(said):
        return False
    return bool(_JAUNDICE_SKIN.search(said) or _CHANGE_SUBJECT.search(said))


ENTRIES.append(entry(
    "jaundice",
    (("yellow", "yellowed", "yellowing", "yellowish", "jaundice", "jaundiced",
      "gone yellow", "turned yellow", "going yellow", "looks yellow", "look yellow",
      "i have gone yellow", "ive gone yellow", "i have turned yellow", "i am yellow",
      "im yellow", "i have jaundice", "ive got jaundice"),
     ("skin", "eyes", "eye", "whites", "the whites of my eyes", "my face", "face", "body",
      "all over", "complexion",
      "look", "looks", "looking",
      "have", "has", "had", "ive", "im",
      "hand", "hands", "palm", "palms", "arm", "arms", "leg", "legs", "feet", "foot",
      "is", "what", "dangerous", "serious", "worrying", "bad", "contagious", "catch", "spread",
      "cause", "causes", "caused", "mean", "means", "treat", "treated", "treatment", "cure",
      "symptom", "symptoms", "sign", "signs",
      "baby", "babies", "newborn", "newborns", "infant", "son", "daughter", "child")),
    _jaundice_card,
    avoid=("teeth", "tooth", "teething", "nails", "nail", "nail varnish", "fingers", "fingertips",
           "toenail", "toenails", "fingernail", "fingernails", "toe", "toes", "toenail varnish",
           "tobacco", "smoker", "smoking", "nicotine", "bruise", "bruises", "bruised",
           "black eye", "spots", "spot", "pustules", "crust", "crusty", "pus", "discharge",
           "leaves", "leaf", "plant", "plants", "lawn", "grass", "flower", "flowers",
           "stain", "stains", "stained", "wallpaper", "paint", "painted", "tile", "tiles",
           "grout", "card", "cards", "warning", "lines", "line", "van", "car",
           "road", "roads", "traffic", "street", "junction", "signpost", "bus", "lorry",
           "bike", "cycle", "kerb",
           "banana", "bananas", "cheese", "curry", "sauce", "rice", "cake",
           "fake tan", "self tan", "spray tan", "tanning", "tanning bed", "tanning beds",
           "sunbed", "sunbeds", "bronzer", "false tan", "st tropez",
           "yellow fever", "typhoid", "dengue", "malaria", "vaccine", "vaccines",
           "vaccination", "jab", "jabs"),
    guard=_the_colour_is_on_the_skin,
    bias=1,
))

for _pair, _card in TOGETHER:
    ENTRIES.append(entry("medicine-together-%s-%s" % (_pair[0][0].replace(" ", "-"),
                                                      _pair[1][0].replace(" ", "-")),
                         _pair, _card, bias=_PAIR_BIAS.get(_pair[0], 2)))
ENTRIES.append(entry(
    "medicine-and-alcohol",
    (("drink", "drinking", "drinks", "alcohol", "beer", "wine", "lager", "pint", "pints",
      "vodka", "gin", "whisky", "whiskey", "rum", "cider", "prosecco", "cocktail",
      "booze", "drunk", "night out", "few drinks", "glass of wine", "heavy drinker"),
     ("ibuprofen", "nurofen", "brufen", "paracetamol", "painkiller", "painkillers",
      "antibiotic", "antibiotics", "penicillin", "amoxicillin", "metronidazole",
      "tinidazole", "trimethoprim", "nitrofurantoin", "codeine", "co codamol",
      "co-codamol", "cocodamol", "antidepressant", "antidepressants", "sertraline",
      "fluoxetine", "citalopram", "antihistamine", "antihistamines", "piriton",
      "cetirizine", "loratadine", "chlorphenamine", "hayfever", "hay fever", "allergy",
      "blood pressure", "statin", "statins", "amlodipine", "ramipril", "lisinopril",
      "tablets", "medicine", "medication", "pills", "prescription")),
    _drink_and_the_drug,
    avoid=("pregnant", "pregnancy", "expecting", "breastfeeding", "breast feeding",
           "nursing", "child", "baby", "toddler", "kid", "newborn", "year old",
           "years old", "overdose", "took too much", "how much", "how many", "dose",
           "dosage", "mg", "addicted", "withdrawal", "calories", "units", "hangover"),
    bias=2))

_COLD_OR_HAYFEVER = (
    "The itch is the tell: hayfever itches - eyes, nose, the roof of the mouth - and comes with "
    "sneezing fits, clear watery snot and no fever, and it comes back at the same point every "
    "year. A cold starts with a sore throat, turns thicker and yellower after a few days, and can "
    "come with a mild fever and aching, and it is over in about a week. A high fever, shivery "
    "aches or a cold that is no better after ten days is not hayfever, so see a GP.")
_A_NOT_A_COLD = ("tablet", "tablets", "piriton", "cetirizine", "loratadine", "chlorphenamine",
                 "dose", "dosage", "mg", "pregnant", "pregnancy", "breastfeeding",
                 "breast feeding", "baby", "babies", "toddler", "child", "children", "kid",
                 "kids", "year old", "years old", "dog", "cat", "puppy", "kitten", "pet",
                 "pets", "outside", "weather", "room", "house", "radiator", "hands", "feet",
                 "sore", "soup", "lager", "beer", "wine", "drink", "drinks", "food", "fridge",
                 "freezer", "its cold", "it's cold", "im cold", "i'm cold", "feel cold",
                 "feeling cold")
ENTRIES.append(entry(
    "cold-or-hayfever",
    (("cold", "colds", "a cold", "head cold", "chesty cold", "bad cold", "sniffles", "sniffing"),
     ("hayfever", "hay fever", "hay-fever", "hayfevre", "allergy", "allergies", "pollen",
      "antihistamine", "antihistamines")),
    _COLD_OR_HAYFEVER,
    ask=("cold", "colds", "a cold", "hayfever", "hay fever", "hay-fever", "sniffles",
         "sneezing", "sneeze", "runny nose", "itchy", "or a cold", "or the cold"),
    avoid=_A_NOT_A_COLD,
    bias=2))
ENTRIES.append(entry(
    "is-it-hayfever",
    (("hayfever", "hay fever", "hay-fever", "hayfevre"),
     ("is it", "is this", "have i got", "do i have", "could it be", "might it be", "or a cold",
      "or the cold", "which is it", "what is it", "am i getting")),
    _COLD_OR_HAYFEVER,
    avoid=_A_NOT_A_COLD,
    bias=1))

_GRAPEFRUIT = ("grapefruit", "grapefruits", "grapefruit juice", "pomelo", "pomelos",
               "seville orange", "seville oranges")
_CRANBERRY = ("cranberry", "cranberries", "cranberry juice", "cranberry sauce")
_DAIRY = ("milk", "dairy", "cheese", "yoghurt", "yogurt", "yoghurts", "yogurts", "milkshake",
          "calcium", "fromage frais")
_GREENS = ("greens", "leafy greens", "kale", "spinach", "broccoli", "cabbage", "sprouts",
           "salad", "lettuce", "green vegetables", "vitamin k", "collard")
_STATIN = ("statin", "statins", "simvastatin", "atorvastatin", "rosuvastatin", "pravastatin",
           "fluvastatin", "lipitor", "crestor", "zocor")
_THINNER = ("warfarin", "thin", "thinner", "thinners", "anticoagulant", "anticoagulants",
            "inr", "apixaban", "rivaroxaban", "edoxaban", "dabigatran", "eliquis", "xarelto")
_TETRACYCLINE = ("tetracycline", "tetracyclines", "doxycycline", "lymecycline", "minocycline",
                 "ciprofloxacin", "cipro", "quinolone", "quinolones", "moxifloxacin")
_IRON_PILL = ("iron", "ferrous", "ferrous sulphate", "ferrous fumarate")
_THYROID_PILL = ("levothyroxine", "thyroxine", "thyroid tablet", "thyroid tablets",
                 "underactive thyroid")

def _a_food_and_the_drug(memory, reading):
    words = set(reading.get("words") or ())
    if words & set(_GRAPEFRUIT):
        if words & set(_THINNER):
            return ("Warfarin itself is not affected by grapefruit, but the newer blood thinners "
                    "apixaban and rivaroxaban are partly cleared by the enzyme it blocks, so keep "
                    "grapefruit to the odd glass and tell the clinic you eat it. Don't stop the "
                    "tablets over it: what matters is a daily grapefruit habit, not one glass.")
        if words & set(_STATIN):
            return ("Grapefruit lifts the level of simvastatin and atorvastatin in the blood, "
                    "which is what makes the muscles ache, so leave grapefruit and grapefruit "
                    "juice off while you take it - one glass is not an emergency, a daily habit "
                    "is. Pravastatin, rosuvastatin and fluvastatin are barely affected, so a swap "
                    "is easy if you like grapefruit: ask the pharmacist.")
        return ("Grapefruit only matters with a handful of medicines, and statins are the common "
                "one: it blocks the enzyme that clears simvastatin and atorvastatin, so the drug "
                "builds up. Check the leaflet for 'avoid grapefruit', and if yours is one of "
                "those two ask about swapping to pravastatin or rosuvastatin rather than giving "
                "up the fruit. Paracetamol, antibiotics and blood pressure tablets are fine with "
                "it.")
    if words & set(_CRANBERRY):
        return ("Cranberry in normal amounts is fine on warfarin, but a glass every day, or a lot "
                "of it, can push your INR up and make bruising and bleeding more likely. Keep it "
                "occasional, don't start a daily habit, and tell the anticoagulant clinic if you "
                "do, so they can check the INR. It doesn't stop the tablet working, so you can "
                "still drink it for a urine infection.")
    if words & set(_DAIRY):
        if words & set(_THYROID_PILL):
            return ("Levothyroxine wants an empty stomach and no dairy for about four hours: take "
                    "it with water when you wake, then leave the milk in your tea and cereal "
                    "until later. Calcium, iron and antacids with calcium in them do the same "
                    "thing, so the tablet goes first and the dairy after.")
        if words & set(_IRON_PILL):
            return ("Milk is the thing to move, not the tablet: the calcium in milk, cheese and "
                    "yoghurt blocks iron absorption, so take the iron with water or orange juice "
                    "and leave two hours either side of dairy. Vitamin C helps iron in; tea, "
                    "coffee and calcium hold it back.")
        if words & set(_TETRACYCLINE):
            return ("That one does interact: doxycycline, lymecycline and ciprofloxacin bind to "
                    "the calcium in milk, cheese and yoghurt and pass straight through, so take "
                    "the tablet with water and leave two hours before or after dairy. Milk is "
                    "fine with every other antibiotic, and with paracetamol.")
        return ("Milk, cheese and yoghurt don't stop most tablets working, so you can have dairy "
                "with them. The ones that care are the tetracycline antibiotics - doxycycline, "
                "lymecycline - and ciprofloxacin, which bind to dairy calcium, plus an iron "
                "tablet and levothyroxine, which dairy blocks: leave two hours around those and "
                "it makes no difference to the rest.")
    if words & set(_GREENS):
        return ("Leafy greens are good for you on warfarin: the vitamin K in them is what keeps "
                "the dose steady, so the rule is to keep the amount the same week to week rather "
                "than cut them out. What swings an INR is a change - a sudden daily kale or salad "
                "habit, or dropping greens you eat every day - so tell the clinic when that "
                "happens and carry on eating them.")
    return ("Most food is fine with most tablets. The pairs that matter are grapefruit with "
            "simvastatin and atorvastatin, dairy with doxycycline, ciprofloxacin, iron or "
            "levothyroxine, cranberry in quantity with warfarin, and a big change in leafy greens "
            "on warfarin. A pharmacist will check the two you actually have.")


ENTRIES.append(entry(
    "medicine-and-a-food",
    (_GRAPEFRUIT + _CRANBERRY + _DAIRY + _GREENS,
     ("antibiotic", "antibiotics", "penicillin", "amoxicillin", "doxycycline", "lymecycline",
      "tetracycline", "ciprofloxacin", "trimethoprim", "nitrofurantoin", "metronidazole",
      "statin", "statins", "simvastatin", "atorvastatin", "rosuvastatin", "pravastatin",
      "warfarin", "blood thinner", "blood thinners", "anticoagulant", "anticoagulants",
      "inr", "apixaban", "rivaroxaban", "iron tablet", "iron tablets", "levothyroxine",
      "thyroxine", "tablets", "tablet", "medicine", "medicines", "medication", "pills",
      "prescription")),
    _a_food_and_the_drug,
    avoid=("pregnant", "pregnancy", "expecting", "breastfeeding", "breast feeding", "nursing",
           "child", "children", "baby", "babies", "toddler", "kid", "kids", "newborn",
           "year old", "years old", "months old", "overdose", "took too much", "dose", "dosage",
           "mg", "allergic", "allergy", "anaphylaxis", "rash", "recipe", "calories"),
    bias=3))

STATIN_TIMING = (
    "Take it at the same time each day, and for most statins that is the evening: the body makes "
    "most of its cholesterol at night, and simvastatin has to be taken in the evening. "
    "Atorvastatin and rosuvastatin last long enough to work at any time of day, so if mornings "
    "are easier to remember, ask the pharmacist whether yours can move to one.")

STATIN_FIRST_WEEKS = (
    "A statin is usually for the long term, and it is judged on a blood test at about three "
    "months rather than on how you feel, so keep taking it and have that test done. Mention "
    "muscle aches you cannot explain, and any new stomach upset or rash, instead of stopping it "
    "yourself: most people take one for years without trouble, and most of the ones who do get "
    "aches are fine on a different statin.")

STATIN_WITH_OTHER_TABLETS = (
    "Ask a pharmacist with your list in front of you, because it depends on what you take: the "
    "ones that matter are some antibiotics (clarithromycin and erythromycin), some antifungal "
    "tablets, and gemfibrozil, and those raise the level of a statin in the blood and with it the "
    "risk of aching muscles. Most everyday medicines are fine alongside one - paracetamol, "
    "ibuprofen, most blood-pressure tablets - so the pharmacist only needs a minute and the names.")

_MEDICINE_WORDS = ("tablet", "tablets", "pill", "pills", "medicine", "medicines", "medication",
                   "medications", "drug", "drugs", "antibiotic", "antibiotics", "antibody",
                   "painkiller", "painkillers", "supplement", "supplements", "prescription",
                   "prescriptions", "capsules", "inhaler", "inhalers", "injection", "patch",
                   "patches", "spray", "sprays", "drops", "syrup", "steroid", "steroids",
                   "ibuprofen", "paracetamol", "aspirin", "codeine", "naproxen", "blood thinner",
                   "blood thinners", "warfarin", "antidepressant", "antidepressants",
                   "water tablet", "water tablets", "beta blocker", "beta blockers",
                   "blood pressure tablets", "blood pressure pills", "the pill")
_MORE_THAN_ONE = ("other", "another", "rest of", "both", "together", "alongside", "at the same",
                  "same time", "as well as", "plus", "and my", "on top of", "more than one",
                  "with my", "with the", "with any", "with some", "with one of my")
_INTERACTION_WORD = re.compile(
    r"\b(?:interact\w*|interaction\w*|clash\w*|contraindicat\w*|mix(?:es|ed|ing)?|"
    r"conflict\w*|safe (?:with|alongside|to take)|be taken with|taken together|"
    r"go(?:es)? with|compatible)\b")


def _another_medicine_is_named(line):
    if _INTERACTION_WORD.search(line):
        return True
    medicines = [word for word in _MEDICINE_WORDS if word in line]
    if len(medicines) >= 2:
        return True
    if medicines and any(word in line for word in _MORE_THAN_ONE):
        return True
    return False

_STATIN_WHETHER = re.compile(
    r"\b(?:should i (?:take|be on|start|go on)|do i (?:need|have to)|is it worth|"
    r"are statins worth|do i really need|is it necessary)\b")
_STATIN_STARTED = ("start", "started", "starting", "put me on", "prescribed", "just been",
                   "new to", "began", "begin", "first month", "few weeks")

_STATIN_NAMES = ("statin", "statins", "simvastatin", "atorvastatin", "rosuvastatin",
                 "pravastatin", "fluvastatin", "lipitor", "crestor", "zocor",
                 "cholesterol tablet", "cholesterol tablets", "cholesterol pill",
                 "cholesterol pills")


def _a_statin_and_the_day(memory, understood):
    line = _the_line(understood)
    if _another_medicine_is_named(line):
        return STATIN_WITH_OTHER_TABLETS
    if any(word in line for word in ("night", "evening", "morning", "what time", "when",
                                     "same time", "best time", "time of day", "together")):
        return STATIN_TIMING
    if _STATIN_WHETHER.search(line) and not any(word in line for word in _STATIN_STARTED):
        return None
    return STATIN_FIRST_WEEKS


def _the_last_line_named_a_statin(understood):
    lean = (understood or {}).get("leans_on") or {}
    if not isinstance(lean, dict):
        return False
    said = " ".join(str(word) for word in (lean.get("words") or [])).lower()
    said = said or str(lean.get("text") or "").lower()
    return any(name in said for name in _STATIN_NAMES)


ENTRIES.append(entry(
    "statin-when",
    (_STATIN_NAMES,
     ("take", "taking", "taken", "night", "nights", "evening", "evenings", "morning",
      "mornings", "when", "time", "best time", "same time", "start", "started", "starting",
      "new", "just", "put", "prescribed", "first", "month", "months", "how long", "forever",
      "life", "stop", "stopping", "come off", "side effect", "side effects", "muscle",
      "aches", "achy", "should i", "do i",
      "interact", "interaction", "clash", "mix", "safe", "tablet", "tablets", "pill", "pills",
      "medication", "medicine", "medicines", "antibiotic", "antibiotics", "alongside",
      "together", "other tablets", "other medication", "other medicines", "other pills")),
    _a_statin_and_the_day,
    avoid=("grapefruit", "grapefruits", "pomelo", "cranberry", "alcohol", "drink", "beer",
           "wine", "pregnant", "pregnancy", "breastfeeding", "child", "children", "baby",
           "food", "foods", "eat", "eating", "eats", "diet", "dieting", "meal", "meals",
           "breakfast", "lunch", "dinner", "snack", "snacks", "recipe", "recipes",
           "toddler", "dose", "dosage", "mg", "overdose", "allergic", "allergy", "rash",
           "recipe", "calories", "cholesterol level", "cholesterol number", "hdl", "ldl")))

ENTRIES.append(entry(
    "statin-when-said-again",
    (("take it", "take them", "take one", "take mine", "take the tablet",
      "take the tablets", "take this"),
     ("when", "what time", "night", "nights", "evening", "evenings", "morning",
      "mornings", "same time", "best time", "time of day", "before bed")),
    _a_statin_and_the_day,
    avoid=("paracetamol", "ibuprofen", "antibiotic", "antibiotics", "penicillin",
           "asthma", "inhaler", "insulin", "child", "children", "baby", "toddler",
           "dog", "cat", "pet", "food", "foods", "eat", "eating", "diet", "alcohol",
           "pregnant", "pregnancy", "grapefruit", "dose", "mg", "twice", "three times",
           "missed", "forgot", "skipped"),
    guard=_the_last_line_named_a_statin))



_TEST = ("bloods", "results", "result", "test", "tests", "scan", "scans", "x-ray", "xray",
         "vet", "vets", "vet's", "the vets",
         "x ray", "mri", "ct scan", "ct", "ultrasound", "biopsy", "smear", "ecg", "swab")
_READING = ("blood pressure", "bp", "heart rate", "pulse", "cholesterol", "blood sugar",
            "blood group", "temperature")
_A_LUMP_OR_A_RASH = ("lump", "lumps", "bump", "bumps", "mole", "moles", "spot", "spots",
                     "rash", "rashes", "swelling", "swollen", "itch", "itching", "itchy",
                     "bruise", "bruises", "discharge")
_CANNOT_SLEEP = ("sleep", "sleeping", "asleep", "slept", "awake", "insomnia", "waking",
                 "cant sleep", "cannot sleep", "can't sleep")
_NOT_A_MEDICAL_TEST = ("eye test", "eye exam", "sight test", "mot", "mot test", "driving test",
                       "theory test", "test drive", "exam", "exams", "gcse", "a level", "a-level",
                       "school", "college", "university", "interview", "job", "coursework",
                       "assignment", "iq test", "pcr", "swab test kit", "covid test",
                       "results day", "results are out", "grades",
                       "pregnancy test", "pregnancy tests", "lateral flow")

SCAN_MRI = (
    "An MRI uses a strong magnet and radio waves, so it shows brain, muscle and ligament better "
    "than an X-ray can. It does not hurt, but it is loud and you lie still for 15 to 45 minutes, "
    "which is why people find it cramped - say if you are nervous and they will talk you through "
    "it. In pregnancy it is the safe scan, because there is no radiation in it.")
SCAN_CT = (
    "A CT is a ring of X-rays stitched into slices, so it shows bone, blood and bowel all at once. "
    "It does not hurt and takes about 10 minutes on the table, though it is a small dose of "
    "radiation: in pregnancy an X-ray or CT is only done if the picture is worth the small risk.")
SCAN_ULTRASOUND = (
    "An ultrasound uses sound rather than radiation, which is why it is the one used in pregnancy. "
    "It is the quickest of them, 10 to 20 minutes with cold gel and a probe pressed on, and it "
    "does not hurt.")
SCAN_ANY = (
    "An X-ray is a photograph taken through you with radiation and shows bone best; a CT is a ring "
    "of those stitched into slices; an MRI uses a magnet and radio waves and is the best for soft "
    "tissue; an ultrasound uses sound. None of them hurts. An MRI is the loud one where you lie "
    "still for 15 to 45 minutes, and in pregnancy it is the safe scan because there is no "
    "radiation in it.")


def _a_scan_reply(memory, understood):
    text = ((understood or {}).get("clean") or "").lower()
    if re.search(r"\bmri\b|magnetic resonance", text):
        return SCAN_MRI
    if re.search(r"\bct\b|\bcat scan\b|\bct scan\b", text):
        return SCAN_CT
    if "ultrasound" in text or "sonogram" in text:
        return SCAN_ULTRASOUND
    return SCAN_ANY


ABNORMAL_RESULT_TEXT = (
    "An abnormal result is usually a number a little outside the range, not a diagnosis: a "
    "slightly low vitamin D, or a liver figure up after a bug, is repeated in a few weeks and "
    "settles. Ask three things on the phone - which test it was, what your number was and what "
    "the normal range is - and then what the plan is. \"They want to see you again\" usually means "
    "a value worth a look rather than bad news, and you can ask for a copy of the result.")

CHASE_RESULT_TEXT = (
    "Yes - ring the surgery and ask the receptionist whether the result is back and whether "
    "anything needs doing, rather than waiting for a letter, and ask for a copy if you want one. "
    "If it is past the wait they promised, say when the sample was taken and ask who is going to "
    "look at it.")

CLEAR_RESULT_TEXT = (
    "That is good news, and there is nothing to do about it: a clear result means nothing was "
    "found. Keep the letter or save the message, and if the symptom that started it off is still "
    "there in a few weeks, tell the GP even with a clear result behind you.")

CLEAR_RESULT_FOR_A_PET_TEXT = (
    "That is the result you wanted: nothing found means there was nothing to treat, so the visit "
    "did its job. Keep the note the vet gave you, and if the same thing comes back, ring them "
    "rather than waiting to see whether it settles on its own.")
ABNORMAL_RESULT_FOR_A_PET_TEXT = (
    "Ask the vet to say what the result was and what the next step is, in those words. Most "
    "results a little outside the range are repeated in a few weeks rather than treated now, and "
    "it is worth knowing which one this is before you read the worst into it.")

NEGATIVE_RESULT_TEXT = (
    "A negative result means the thing they were looking for was not found, which is usually the "
    "news you want: nothing to act on. If you were expecting it to show something, ring and ask "
    "what it means for you rather than reading it either way.")

AFTER_A_CLEAR_RESULT_EXERCISE = (
    "Yes - nothing was found, so nothing is waiting on it. Build back up over a week or two "
    "rather than straight back to where you were, and ease off again if the symptom comes back.")
AFTER_A_CLEAR_RESULT_MEDICINE = (
    "Don't stop them on the strength of a clear result: ring whoever prescribed them and ask, "
    "because a test clearing one thing does not mean the medicine has done its job. A clear "
    "result answers the test, it does not end a prescription.")
AFTER_A_CLEAR_RESULT_WORK = (
    "Nothing in the result keeps you off - but if you were signed off, whoever signed you off is "
    "the one who says it can end early, so ask them before you go back.")
AFTER_A_CLEAR_RESULT_DRIVING = (
    "Nothing in a clear result stops you driving. If the test was for a licence or an insurance "
    "medical, whoever asked for it decides, not the result on its own.")
AFTER_A_CLEAR_RESULT_TEXT = (
    "Yes - nothing was found, so nothing in that result is holding you up. If it is a medicine "
    "or a note from work, ask whoever prescribed or signed it before you change anything: a "
    "clear result answers the test.")
_A_STOPPING_A_MEDICINE = re.compile(
    r"\b(?:tablets?|pills?|medicines?|medication|meds|inhaler|antibiotics?|dose|dosage|statins?|"
    r"stop taking|stop the|stop my|come off|prescribed)\b", re.I)
_A_DRIVING_AGAIN = re.compile(r"\b(?:driv\w+|licence|license|dvla)\b", re.I)
_A_SPORT_AGAIN = re.compile(
    r"\b(?:gym|run|running|jog\w*|swim\w*|cycl\w*|football|sport\w*|train|training|weights|"
    r"lifting|work out|workout|exercise|exercising|walk\w*|hike|hiking|tennis|badminton|dance|"
    r"dancing|ride|riding)\b", re.I)
_A_JOB_AGAIN = re.compile(
    r"\b(?:work|job|office|shift|shifts|signed off|sick note|back to work)\b", re.I)


def _the_permission_for(text):
    if _A_STOPPING_A_MEDICINE.search(text):
        return AFTER_A_CLEAR_RESULT_MEDICINE
    if _A_DRIVING_AGAIN.search(text):
        return AFTER_A_CLEAR_RESULT_DRIVING
    if _A_SPORT_AGAIN.search(text):
        return AFTER_A_CLEAR_RESULT_EXERCISE
    if _A_JOB_AGAIN.search(text):
        return AFTER_A_CLEAR_RESULT_WORK
    return AFTER_A_CLEAR_RESULT_TEXT

_RESULT_SAYS_ABNORMAL = re.compile(
    r"\b(?:abnormal|borderline|outside the range|out of range|flagged)\b")
_RESULT_SAYS_CLEAR = re.compile(r"\b(?:clear|nothing was found|good news)\b")


_RULES_IT_OUT = re.compile(
    r"\b(?:no|nothing|not)\s+(?:signs?\s+of\s+)?(?:infection|fracture|break|damage|growth|"
    r"lump|clot|blockage|problems?|disease|cancer|abnormalit\w*|arthritis|ulcer|stones?)\b"
    r"|\b(?:showed|found|seen|shows|finds)\s+nothing\b"
    r"|\bno signs? of (?:anything|it|that|a problem|trouble|concern)\b"
    r"|\bnothing\s+(?:there|found|showed|showing)\b", re.I)

_A_TEST_NAME = re.compile(
    r"\b(?:test|tests|result|results|bloods|scan|scans|x[ -]?ray|xray|mri|ct|ultrasound|"
    r"biopsy|smear|ecg|swab|vet|vets)\b")


_A_PERMISSION_ASK = re.compile(
    r"\b(?:can i|can we|could i|am i ok|am i alright|is it ok|is it alright|should i|"
    r"do i need to|does that mean i can|so i can|so can i|when can i|time to|back to)\b", re.I)
_SOMETHING_TO_GO_BACK_TO = re.compile(
    r"\b(?:go back|get back|back to|return to|start again|drive|driving|exercise|gym|running|run|swim|"
    r"swimming|cycling|cycle|football|training|train|weights|lifting|work out|workout|"
    r"work|stop taking|stop the|come off|drink|eat)\b", re.I)


def _after_a_clear_result(memory, understood):
    text = ((understood or {}).get("text") or (understood or {}).get("clean") or "").lower()
    if not _A_PERMISSION_ASK.search(text) or not _SOMETHING_TO_GO_BACK_TO.search(text):
        return None
    last = ""
    for turn in (memory.get("turns") or [])[-2:]:
        if isinstance(turn, dict) and turn.get("bot"):
            last = turn["bot"].lower()
    if not _RESULT_SAYS_CLEAR.search(last):
        return None
    return _the_permission_for(text)


_A_CHECKING_THE_RESULT = re.compile(
    r"^(?:so|and|oh|well|ok|okay|right|thats|that's)?\s*(?:thats|that's|that is|its|it's|it is)?"
    r"\s*(?:good|great|fine|ok|okay|alright|all right|normal|reassuring|brilliant|nice)\b",
    re.I)


def _a_check_on_a_clear_result(memory, understood):
    text = ((understood or {}).get("text") or (understood or {}).get("clean") or "").lower()
    text = text.strip()
    if not text or len(text.split()) > 6 or not _A_CHECKING_THE_RESULT.match(text):
        return None
    last = ""
    for turn in (memory.get("turns") or [])[-2:]:
        if isinstance(turn, dict) and turn.get("bot"):
            last = turn["bot"].lower()
    if not _RESULT_SAYS_CLEAR.search(last):
        return None
    return ("It is - nothing was found, so there is nothing to do about it. If the symptom that "
            "started all this is still there in a few weeks, say so to the GP even with that "
            "result behind you.")


def _a_result_reply(memory, understood):
    text = ((understood or {}).get("text") or (understood or {}).get("clean") or "").lower()
    pet = bool(re.search(r"\b(?:vet|vets)\b", text))
    if _RULES_IT_OUT.search(text):
        return CLEAR_RESULT_FOR_A_PET_TEXT if pet else CLEAR_RESULT_TEXT
    if _A_TEST_NAME.search(text):
        if re.search(r"\b(?:clear|all clear|normal|fine|nothing there|nothing found|no problems|"
                     r"nothing showed up|(?:she|he)'?s fine|(?:she|he) is fine)\b", text):
            return CLEAR_RESULT_FOR_A_PET_TEXT if pet else CLEAR_RESULT_TEXT
        if re.search(r"\b(?:negative|not detected|no trace)\b", text):
            return NEGATIVE_RESULT_TEXT
        if re.search(r"\b(?:abnormal|borderline|flagged|outside the range|out of range|high|low|"
                     r"showed something|shows something|showed up)\b", text):
            return ABNORMAL_RESULT_FOR_A_PET_TEXT if pet else ABNORMAL_RESULT_TEXT
    last = ""
    for turn in (memory.get("turns") or [])[-2:]:
        if isinstance(turn, dict) and turn.get("bot"):
            last = turn["bot"].lower()
    if _RESULT_SAYS_ABNORMAL.search(last):
        return ("Same result, same question to put on the phone: what exactly it says, and what "
                "the range or the next step is. Most abnormal results are a little outside the "
                "range and are repeated in a few weeks, so ask rather than reading the worst into "
                "it.")
    if _RESULT_SAYS_CLEAR.search(last):
        return ("Nothing in a clear result is a warning - it means nothing was found, so there is "
                "nothing to worry about and nothing to act on. If the symptom that started all "
                "this is still there in a few weeks, say so to the GP even with that result behind "
                "you.")
    if re.search(r"\b(?:need(?:s)? (?:a )?follow up|want(?:s)? to see|asked me to come|"
                 r"come back in|another appointment|appointment)\b", text):
        return ABNORMAL_RESULT_TEXT
    if re.search(r"\b(?:follow up|follow-up|chase|chasing|ring|phone|call|ask|heard|hear)\b",
                 text):
        return CHASE_RESULT_TEXT
    if re.search(r"\b(?:result|results|follow up|follow-up|came back)\b", text):
        return ABNORMAL_RESULT_TEXT
    return ("A blood test is a small sting and a vial or two, and there is nothing about having "
            "one to worry about - it is the number it comes back with that matters. If that comes "
            "back outside the range they will tell you, and it is usually repeated in a few weeks.")


_A_FASTING_LENGTH = re.compile(
    r"\bhow long\b[^.?]*(?:fast|fasting|fasted|without food|no food|nothing to eat|empty stomach)"
    r"|(?:fast|fasting|fasted)\b[^.?]*\bhow long\b"
    r"|\bhow many hours\b[^.?]*(?:fast|fasting|fasted|without food|no food|nothing to eat)",
    re.IGNORECASE)

_A_TEST_THAT_TAKES = re.compile(
    r"\b(?:test|tests|appointment|appointments)\s+(?:take|takes|took|last|lasts)\b", re.IGNORECASE)

_A_BLOOD_TEST_TEXT = (
    "A blood test is a small needle in the arm and a vial or two, about five minutes in the "
    "chair, and it checks red and white cells and platelets, kidney and liver figures, "
    "thyroid, cholesterol, vitamin D and blood sugar. It shows how the organs are working "
    "and whether something is short or high, which is what the GP reads against your "
    "symptoms, so ask what your number was and what the normal range is. You do not need to "
    "fast unless the surgery says so.")

_A_FASTING_BEFORE_A_TEST_TEXT = (
    "Eight to twelve hours without food is the usual ask, and water is fine: book the first "
    "appointment of the morning, and tea or coffee with no milk still counts as fasting. Only "
    "some tests need it - a fasting cholesterol or a glucose, not a full blood count or a "
    "thyroid check - so read the letter, because eating by mistake usually means going back "
    "another day. Take your medicine as normal unless the letter says to skip it, and if you "
    "are diabetic ask the surgery how they want that morning to work.")


def _a_blood_test(memory, understood):
    read = understood if isinstance(understood, dict) else {}
    said = " ".join(str(read.get("clean") or read.get("text") or "").split())
    if _A_FASTING_LENGTH.search(said) and not _A_TEST_THAT_TAKES.search(said):
        return _A_FASTING_BEFORE_A_TEST_TEXT
    return _A_BLOOD_TEST_TEXT


ENTRIES.extend([
    entry("results-how-long",
          (_TEST,
           ("how long", "how many days", "wait", "waiting", "be back",
            "is back", "back yet", "not back", "still waiting",
            "chase", "chasing", "when", "heard", "hear", "not heard")),
          "Most GP blood tests come back in two to five days, and thyroid or HbA1c can take a "
          "week. An X-ray is usually read within a few days, a smear takes two to four weeks "
          "because it is looked at under a microscope, and a biopsy one to two. Ring the surgery "
          "and ask rather than waiting by the phone - results do get filed and sit there.",
          avoid=_NOT_A_MEDICAL_TEST + _CANNOT_SLEEP
                + ("is", "cost", "costs", "price", "private")),
    entry("what-a-scan-is",
          (("mri", "ct", "ct scan", "cat scan", "x-ray", "xray", "x ray", "ultrasound", "scan",
            "scans", "radiographer"),
           ("what is", "whats", "what are", "how does", "how do", "difference", "work", "works",
            "hurt", "hurts", "painful", "like", "claustrophobic", "loud", "long", "safe",
            "how long", "take", "takes", "quick",
            "radiation", "pregnant", "contrast", "dye")),
          _a_scan_reply,
          bias=1,
          avoid=_NOT_A_MEDICAL_TEST + ("result", "results", "document", "documents", "paper",
                                       "papers", "receipt", "receipts", "form", "forms",
                                       "letter", "letters", "passport", "photocopy",
                                       "photocopies", "printer", "print", "pdf", "barcode",
                                       "qr", "scan a document", "scan a receipt", "scan it in",
                                       "old photos", "photo", "photos", "scanner")),
    entry("their-own-results-or-records",
          (("test results", "test result", "blood test results", "blood test result",
            "blood results", "scan results", "scan result", "x ray results", "xray results",
            "mri results", "biopsy results", "smear results", "results of my test",
            "results of my scan", "results of my blood test",
            "medical records", "medical record", "gp records", "gp record",
            "patient records", "patient record", "health records", "health record",
            "my records", "my record", "nhs records", "hospital records"),
           ("see", "view", "online", "access", "get", "find", "check", "look at",
            "where", "where can i", "can i see", "can i view", "can i get",
            "can i access", "how do i see", "how do i view", "how do i get",
            "how do i find", "how do i check", "how do i access", "how to see",
            "how to view", "how to get", "how to access")),
          "Your results and records are kept by the GP surgery, not by me: most practices put "
          "them in their online service or the NHS app a few days after they are filed, and "
          "reception can tell you the number and whether anything needs acting on. Take photo ID "
          "the first time you ask for online access; a scan report often appears only after a GP "
          "has read it, so if you can see the test but not the report, ring and ask.",
          avoid=_NOT_A_MEDICAL_TEST + _READING + _A_LUMP_OR_A_RASH
                + ("book", "booking", "appointment", "referral", "request", "arrange",
                   "prepare", "how long", "wait", "waiting", "cost", "costs", "price",
                   "private", "paper", "papers", "past paper", "marks", "mark", "grade",
                   "grades", "resit", "mock", "mocks", "term", "semester", "vinyl", "music",
                   "collection", "criminal", "police", "credit", "loan", "bank",
                   "driving", "theory")),
    entry("result-came-back-abnormal",
          (_TEST,
           ("abnormal", "not normal", "outside the range", "out of range", "borderline",
            "flags", "flagged", "something showed up", "showed something", "shows something",
            "high", "low", "they want to see me", "want to see me",
            "follow up", "follow-up", "another test")),
          ABNORMAL_RESULT_TEXT,
          avoid=_NOT_A_MEDICAL_TEST + _READING + _A_LUMP_OR_A_RASH
                + ("chest pain", "cannot breathe", "cant breathe", "collapse",
                   "collapsed", "bleeding", "unconscious", "ambulance")),
    entry("result-came-back-clear",
          (_TEST,
           ("clear", "all clear", "normal", "fine", "nothing there", "nothing found",
            "no problems", "came back ok", "came back fine", "was fine", "good news",
            "negative", "not detected",
            "bad", "worry", "worried", "worrying", "serious", "worse", "anything to worry about",
            "came back", "came through",
            "no infection", "no fracture", "no damage", "no growth", "no lump", "no clot",
            "no blockage", "no problem", "no problems", "no disease", "no cancer",
            "no arthritis", "no ulcer", "no stones", "no sign", "no signs", "nothing",
            "follow up", "follow-up")),
          _a_result_reply,
          bias=1,
          avoid=_NOT_A_MEDICAL_TEST + _READING + _A_LUMP_OR_A_RASH
                + ("mattress", "car", "phone", "credit", "loan", "dell",
                                       "nervous", "scared", "anxious", "afraid", "dreading",
                                       "dread", "worried about", "needle", "needles",
                                       "claustrophobic")),
    entry("after-a-clear-result",
          (("so i can", "so can i", "does that mean i can", "can i go back", "can i get back",
            "can i return", "can i start", "can i exercise", "can i swim", "can i run",
            "can i train", "can i work out", "can i stop", "can i come off", "can we go back",
            "am i ok to", "am i alright to", "is it ok to", "is it alright to", "when can i",
            "time to go back", "do i need to stop", "can i drive", "am i ok to drive",
            "can i get back to driving", "can i start driving"),
           ("go back", "get back", "back to", "return to", "start again", "exercise", "gym",
            "running", "swim", "cycling", "football", "training", "weights", "work",
            "stop taking", "stop the", "come off", "drink", "eat", "drive", "driving")),
          _after_a_clear_result,
          avoid=_NOT_A_MEDICAL_TEST),
    entry("thats-good-then",
          (("so thats good", "so that's good", "thats good then", "that's good then",
            "is that good", "so its good", "so it's good", "so its fine", "so it's fine",
            "thats fine then", "that's fine then", "so thats fine", "so that's fine",
            "so thats ok", "so that's ok", "so thats okay", "so its ok", "so it's ok",
            "so thats normal", "so its normal", "so its all fine", "is that alright",
            "so thats good news", "thats good news then", "so thats reassuring"),
           ("good", "fine", "ok", "okay", "alright", "normal", "great", "reassuring",
            "news", "then", "clear", "result", "results")),
          _a_check_on_a_clear_result,
          avoid=_NOT_A_MEDICAL_TEST),
    entry("smear-came-back-abnormal",
          (("smear", "smear test", "cervical screening", "colposcopy", "hpv"),
           ("abnormal", "borderline", "positive", "hpv positive", "come back", "came back",
            "result", "results", "mean", "means", "next", "worried", "worry", "bad")),
          "An abnormal smear means some cells looked a little different, not that you have cancer: "
          "the commonest results are borderline or mild changes and most clear up on their own. "
          "HPV found with normal cells usually means a repeat smear in a year; borderline or mild "
          "changes usually mean a colposcopy, a closer look at the cervix that takes about 15 "
          "minutes. Keep the appointment, and ask which of those results you have.",
          bias=1,
          avoid=_NOT_A_MEDICAL_TEST + ("how long", "how many days", "how many weeks",
                                       "when will", "take to come back", "waiting",
                                       "still waiting")),
    entry("biopsy-how-long",
          (("biopsy", "biopsies"),
           ("how long", "take", "takes", "hurt", "hurts", "painful", "procedure", "recover",
            "recovery", "after", "sore", "needle", "numb", "awake", "sedation")),
          "A biopsy takes about 10 to 20 minutes, and the skin is numbed first, so it is a push "
          "rather than a pain; you can eat and drive afterwards. A skin one needs a plaster for a "
          "day, a prostate or breast one is sore for two or three days and paracetamol covers it. "
          "The result is a separate wait of one to two weeks, because the tissue has to be looked "
          "at under a microscope.",
          bias=1,
          avoid=_NOT_A_MEDICAL_TEST + ("result", "results", "get the results",
                                       "hear back", "how many weeks", "when will i know")),
    entry("a-blood-test",
          (("blood test", "blood tests", "blood count", "full blood count", "blood sample",
            "blood samples", "vial", "vials"),
           ("what is", "whats", "what does", "show", "shows", "for", "detect", "check", "checks",
            "take", "takes", "how long", "how much blood", "needle", "hurt", "hurts", "fast",
            "fasting", "eat", "anaemic", "anemia", "anaemia", "test for")),
          _a_blood_test,
          bias=2,
          avoid=("results", "result", "came back", "come back", "back", "wait", "waiting",
                 "showed no", "shows no", "showed nothing", "found nothing", "nothing there",
                 "abnormal", "diagnosed", "diagnosis", "cancer", "leukaemia", "anaemic",
                 "anaemia", "anemia", "iron", "scared", "afraid", "frightened", "hate", "phobia",
                 "sugar", "sugars", "pressure", "cholesterol", "reading", "level", "levels")),
])
LASTS_ASK = ("how long", "last", "lasts", "lasting", "linger", "lingers", "lingering", "days",
             "weeks", "normal", "clear", "clears", "go", "goes", "recover",
             "recovery", "heal", "heals", "healing", "how many days", "how many weeks")
LASTS_AVOID = ("antibiotic", "antibiotics", "amoxicillin", "penicillin", "medicine", "medicines",
               "tablet", "tablets", "paracetamol", "ibuprofen", "work", "school", "nursery",
               "contagious", "catching", "spread", "spreading", "vaccine", "vaccinated", "jab",
               "jabs", "test", "tests", "tested", "treat", "treating", "treatment", "cure",
               "prevent", "avoid", "catch", "vaccination")

HOW_LONG_LASTS = (
    (("chest infection", "chest infections", "a chest infection", "bronchitis"),
     "Most chest infections clear in about a week to ten days, though the cough can hang on for "
     "three or four weeks afterwards. See a GP if you are breathless or coughing up blood, if the "
     "fever lasts more than five days, if it is getting worse rather than better after a week, or "
     "if you are over 65 or have a long-term chest condition, because those want treating sooner."),
    (("covid", "coronavirus", "corona virus"),
     "Most people are over the worst of covid in about a week, though a cough and tiredness "
     "commonly last two to four weeks and a lost sense of smell can take months to come back. "
     "Stay home while you have a temperature. Get help the same day if you are breathless, "
     "confused, or your lips or face look blue."),
    (("sinus infection", "sinus infections", "sinusitis", "sinus"),
     "Most sinus infections settle in two to three weeks without antibiotics: steam, a salt-water "
     "rinse and paracetamol, and give it ten days before expecting a turn. See a GP if it is "
     "worse after ten days, if it keeps coming back, or if one side of the face swells or the "
     "eye is affected, which wants seeing that day."),
    (("pneumonia",),
     "Most people with pneumonia start to feel better three to five days after treatment begins, "
     "and are back to normal in about six weeks, though tiredness can linger for months. Get "
     "seen the same day if breathing is fast or hard, the lips look blue, or you are confused."),
    (("migraine", "migraines", "a headache", "headaches", "my headache", "head ache",
      "head aches"),
     "A migraine attack usually runs from four hours to three days, and an ordinary headache "
     "from a few hours to a day or two. Get seen the same day for a headache that comes on like "
     "a thunderclap, one with a fever and a stiff neck, one after a bang on the head, or one with "
     "weakness, slurred speech or a change in vision."),
    (("sickness bug", "sickness bugs", "stomach bug", "stomach bugs", "winter vomiting bug",
      "norovirus", "gastric flu", "tummy bug"),
     "A sickness bug usually lasts one to three days, and you can feel washed out for a few days "
     "after that. You are most infectious in the 48 hours after it stops, so stay off work or "
     "school for two days after the last episode. Take small sips often; ring 111 if you cannot "
     "keep any fluid down, there is blood, or a baby is not wetting nappies."),
    (("ear infection", "ear infections", "middle ear infection"),
     "An ear infection usually settles in three to seven days without antibiotics. Give "
     "paracetamol or ibuprofen for the pain, and see a GP if there is discharge from the ear, if "
     "it is no better after three days, or the same day if there is swelling, redness or "
     "tenderness behind the ear."),
    (("glue ear", "otitis media with effusion", "fluid in the ear", "fluid behind the eardrum"),
     "Glue ear is fluid behind the eardrum rather than an infection, and it usually clears on its "
     "own but slowly: about half of children are clear within three months, and most within a "
     "year. Antibiotics and decongestants do not help it. Because the hearing is muffled while it "
     "lasts, ask for a hearing test if it has been there three months or more, and see a GP "
     "sooner if the child's speech is behind, if it keeps coming back, or if either ear is sore "
     "or running."),
    (("inhaler", "inhalers", "blue inhaler", "brown inhaler", "ventolin", "salbutamol",
      "preventer inhaler", "reliever inhaler", "puffer", "puffs left"),
     "A blue reliever inhaler holds 100 doses in the small canister and 200 in the bigger one, so "
     "at two puffs four times a day a 200-dose one lasts about three weeks, and one puff a day "
     "would stretch it to months. Most have a dose counter on the side now, and that number is "
     "what to go by rather than the date on the box. A brown preventer at two puffs twice a day "
     "runs out in about a month in the same way. Order the repeat before it empties rather than "
     "after, because the last puffs are weaker.",
     ("side", "effect", "effects", "attack", "asthma", "wheeze", "wheezing",
      "expired", "expire", "breathless", "breathe")),
)

for _names, _reply, *_rest in HOW_LONG_LASTS:
    ENTRIES.append(entry(
        "lasts-%s" % _names[0].replace(" ", "-"),
        (_names, LASTS_ASK),
        _reply,
        avoid=LASTS_AVOID + tuple(_rest[0] if _rest else ()),
        bias=1))

ENTRIES.append(entry(
    "gout",
    (("gout", "gouty", "uric acid", "podagra"),
     ("what is", "whats", "symptoms", "signs", "treat", "treatment", "get rid", "help", "stop",
      "last", "how long", "go away", "diet", "food", "alcohol", "beer", "drink", "beer and",
      "toe", "big toe", "foot", "ankle", "knee", "joint", "attack", "flare", "flare up",
      "swollen", "red", "painful", "pain", "have", "got", "ive", "why", "cause", "causes",
      "prevent", "allopurinol", "tablets", "normal", "serious", "run in family")),
    ("Gout is uric acid forming crystals in a joint, most often the big toe: it comes on over "
     "hours, red, hot, shiny and too sore to bear the weight of a sheet. An attack settles in "
     "three to ten days. Start ibuprofen or naproxen with food straight away, rest and raise the "
     "foot, and see a GP - colchicine or a short steroid course works if anti-inflammatories are "
     "not an option. Once it settles, cutting beer, sugary drinks, shellfish and organ meat off "
     "the ordinary week is what keeps it away; repeated attacks are worth a blood test and daily "
     "allopurinol to bring the uric acid down. See the GP the same day if the joint is hot with a "
     "fever, because that is an infection until proven otherwise."),
    ask=("gout", "gouty", "uric acid", "podagra"),
    avoid=("car", "tyre", "wheel", "alignment", "tracking", "toe in", "toe out", "boot", "shoe")))

ENTRIES.append(entry(
    "norovirus",
    (("norovirus", "norwalk", "winter vomiting", "winter vomiting bug", "sickness bug",
      "vomiting bug", "stomach bug", "d and v", "diarrhoea and vomiting"),
     ("what is", "whats", "symptoms", "signs", "how long", "last", "lasts", "treat", "treatment",
      "get rid", "cure", "contagious", "catch", "spread", "catches", "work", "school", "nursery",
      "back to work", "back to school", "how do i", "what can i do", "help", "stop",
      "have", "got", "ive", "throwing up", "sick", "vomiting", "diarrhoea", "how many days",
      "stay off", "when can i", "food", "eat", "drink", "clean", "bleach", "family", "house")),
    ("Norovirus is the winter vomiting bug: it comes on within a day or two of contact, with "
     "sudden vomiting and watery diarrhoea, and settles by itself in one to three days. There is "
     "no medicine for it - small sips of fluid, little and often, is the whole treatment, and "
     "oral rehydration sachets help if you are being sick a lot. Wash hands with soap and water, "
     "not alcohol gel, which does not kill it, clean surfaces with bleach, and keep away from "
     "work, school or hospital until 48 hours after the last symptom. Ring 111 the same day for a "
     "baby, an older person or anyone who cannot keep fluid down, or if there is blood."),
    ask=("norovirus", "norwalk", "winter vomiting", "sickness bug", "vomiting bug",
         "stomach bug", "d and v", "diarrhoea and vomiting")))

ENTRIES.append(entry(
    "caesarean-recovery",
    (("c section", "c-section", "csection", "caesarean", "cesarean", "caesarian", "cesarian",
      "section scar", "section wound", "belly birth"),
     ("how long", "recover", "recovery", "heal", "healing", "healed", "drive", "driving",
      "car", "lift", "lifting", "carry", "carrying", "exercise", "running", "gym",
      "pain", "painful", "sore", "ache", "aches", "bleed", "bleeding", "blood", "scar",
      "scars", "wound", "bath", "swim", "swimming", "work", "back to work", "weeks", "days",
      "when", "should i", "can i", "is it normal", "normal", "hurt", "hurts", "stitches",
      "clean", "dress", "dressing", "infection", "numb", "overhang", "tired")),
    ("Six weeks is the usual guide for getting back to normal: the cut heals in a fortnight on "
     "the outside, but the muscle and the layers under it take about six weeks, and the operation "
     "itself is 45 minutes to an hour. The first two weeks are for resting and walking, lifting "
     "nothing heavier than the baby, and taking paracetamol and ibuprofen regularly rather than "
     "when it gets bad. Driving waits for the day you can do an emergency stop without pain - "
     "usually two to six weeks - and tell your insurer; do not drive on strong painkillers. Keep "
     "the scar clean and dry, let it get air, and expect it to be numb, itchy or puckered for "
     "months, which is normal. Ring your midwife, health visitor or GP the same day for a fever, "
     "a scar that is red, hot or leaking, smelly discharge, or pain that gets worse not better."),
    avoid=("elective", "planned date", "booked in", "hospital bag", "go into labour",
           "go into labor",
           "epidural", "spinal", "vbac", "induction", "labour", "labor", "contractions",
           "dog", "cat", "pet", "my knee", "my shoulder", "my arm", "my leg", "my hand",
           "my finger", "my foot", "my toe", "my back", "my eye", "my ear", "my tooth",
           "toilet", "toilet seat", "ironing board", "leather", "sofa", "cushion"),
    ask=("c section", "c-section", "csection", "caesarean", "cesarean", "caesarian",
         "cesarian", "section scar", "belly birth"),
    bias=1))

ENTRIES.append(entry(
    "kidney-stone",
    (("kidney stone", "kidney stones", "renal colic", "ureteric stone", "stone in my kidney",
      "stones in my kidney", "stone from my kidney", "stone in my ureter", "passing a stone",
      "pass a stone", "passed a stone", "pass stones", "stones in my urine"),
     ("what is", "whats", "symptoms", "signs", "how long", "last", "lasts", "treat",
      "treatment", "get rid", "cure", "help", "better", "pain", "painful", "hurt",
      "hurts", "pass", "passing", "passed", "back", "side", "blood", "water", "drink",
      "drinking", "beer", "alcohol", "diet", "eat", "food", "avoid", "prevent", "why",
      "cause", "causes", "have", "got", "ive", "gp", "doctor", "hospital", "a and e",
      "paracetamol", "ibuprofen", "painkiller", "painkillers", "sieve", "surgery", "stent",
      "scan", "camera", "when", "should i")),
    ("Kidney stones are crystals of salt in urine, and most pass on their own: drink two to "
     "three litres of water a day - enough that your urine is pale - take paracetamol or "
     "ibuprofen for the pain, and sieve your urine if you have been asked to catch the stone. "
     "A stone under about 5mm usually comes out within a few weeks, and the pain eases as soon "
     "as it moves into the bladder. Go to A&E the same day if the pain is not controlled by "
     "painkillers, you have a fever or shivering, you cannot pass urine, or there is blood and "
     "you feel unwell - a blocked kidney with an infection is an emergency. Once it is out, ask "
     "what the stone is made of, because the diet that keeps the next one away depends on the "
     "type, and cut back on salt meanwhile."),
    avoid=("gallstone", "gallstones", "gall bladder", "gallbladder", "stone wall", "stone walls",
           "paving", "patio", "stone floor", "stone floors", "stone slab", "stone slabs",
           "kilogram", "kilograms", "kilo", "kilos", "in weight", "lose weight", "losing weight",
           "stomach stone", "kidney failure", "kidney disease", "kidney transplant",
           "kidney function", "kidney infection"),
    ask=("kidney stone", "kidney stones", "renal colic", "passing a stone", "pass a stone",
         "passed a stone", "ureteric stone", "stones in my urine"),
    report=True))

ENTRIES.append(entry(
    "sciatica",
    (("sciatica", "sciatic", "sciatic nerve", "trapped nerve", "slipped disc", "prolapsed disc",
      "herniated disc"),
     ("what is", "whats", "symptoms", "signs", "how long", "last", "lasts", "treat", "treatment",
      "get rid", "cure", "help", "better", "go away", "pain", "painful", "leg", "buttock",
      "shooting", "tingling", "numb", "numbness", "walk", "walking", "sit", "sitting",
      "exercise", "stretch", "stretches", "physio", "gp", "doctor", "have", "got", "ive",
      "why", "cause", "causes", "work", "drive")),
    ("Sciatica is the sciatic nerve complaining, usually where a disc or a tight muscle presses "
     "on it: a shooting or burning pain from the buttock down the back of one leg, often with "
     "tingling or numbness. Most cases settle in four to six weeks without anything done to "
     "them - keep moving and walking as much as the pain allows, which is better than bed rest, "
     "and take paracetamol or ibuprofen. See a GP if it is not easing after a few weeks, or "
     "sooner for a physio referral. Go to A&E the same day if you lose feeling around the "
     "saddle area, cannot pass urine, or the leg goes weak - that is the disc pressing on the "
     "nerves at the bottom of the spine and needs seeing at once."),
    ask=("sciatica", "sciatic", "trapped nerve", "slipped disc", "prolapsed disc")))

_CATARACT_WHAT = (
    "A cataract is the lens inside the eye going cloudy, so sight fades slowly and lights glare "
    "and smear at night - it is not a film on the surface, and no drops or glasses fix it. It is "
    "mostly age, and the operation is one of the commonest and safest there is: the cloudy lens is "
    "swapped for a clear plastic one under local anaesthetic, about 20 minutes, and most people "
    "see better within days. Ask the optician at your next test if the glare is affecting driving, "
    "and tell them if sight drops suddenly, which is not a cataract.")
_CATARACT_LENGTH = (
    "About 20 minutes for the operation itself, under local anaesthetic, and most people are in "
    "and out of the hospital the same morning or afternoon: the cloudy lens is swapped for a clear "
    "plastic one, and sight is usually better within days, though the eye can feel gritty and "
    "watery for a week or two. Ask the optician at your next test if the glare is affecting "
    "driving, and tell them if sight drops suddenly, which is not a cataract.")


def _the_cataract_answer(memory, understood):
    said = str((understood or {}).get("clean") or (understood or {}).get("text") or "").lower()
    asks_a_length = ("how long" in said or "how many minutes" in said or "how soon" in said)
    is_the_operation = any(word in said for word in
                           ("operation", "surgery", "operate", "procedure", "the op"))
    is_the_wait = "wait" in said
    is_the_recovery = any(word in said for word in
                          ("recover", "recovery", "heal", "healing", "back to work",
                           "back to normal", "off work", "drive again", "after the op"))
    if asks_a_length and is_the_operation and not (is_the_wait or is_the_recovery):
        return _CATARACT_LENGTH
    return _CATARACT_WHAT


ENTRIES.append(entry(
    "cataract",
    (("cataract", "cataracts", "cloudy lens", "cloudy eye lens"),
     ("what is", "whats", "symptoms", "signs", "treat", "treatment", "operation", "surgery",
      "remove", "fixed", "cure", "cause", "causes", "why", "age", "old", "night", "driving",
      "glare", "blurred", "blurry", "vision", "sight", "see", "seeing", "eyes", "eye",
      "have", "got", "ive", "is it", "serious", "wait", "nhs", "private", "cost", "recover",
      "recovery", "drops", "glasses")),
    _the_cataract_answer,
    ask=("cataract", "cataracts", "cloudy lens")))
ENTRIES.append(entry(
    "reading-in-dim-light",
    (("read", "reading", "read a book", "reading a book", "read in bed", "reading in bed",
      "read at night", "reading at night", "read in the dark", "reading in the dark",
      "dim light", "in dim light", "dim lighting", "low light", "poor light", "bad light",
      "dimly lit", "dimly lit room", "low lamp", "small lamp", "one lamp", "lamplight",
      "lamp light", "bedside lamp", "reading lamp", "light for reading",
      "light to read", "best light for reading", "lamp for reading", "reading light",
      "light when i read", "light when reading", "what light for reading"),
     ("light", "lights", "lighting", "lamp", "lamps", "bulb", "bulbs", "watt", "wattage",
      "bright", "brighter", "dim", "dimmer", "dark", "darkness", "eyes", "eye", "sight",
      "vision", "strain", "straining", "tired", "headache", "headaches", "hurt", "hurts",
      "aching", "sore", "blurry", "glasses", "specs", "optician")),
    ("Reading in dim light does not damage your eyes - it tires them, and a tired eye feels sore, "
     "waters and gives you a headache. What helps is light that comes from the side or over your "
     "shoulder and lands on the page rather than from behind you onto the screen: a lamp at about "
     "40 to 60cm, a little behind your shoulder, and a warm-white LED of 6 to 9 watts is plenty for "
     "a book. Keep the room light on too, so your eye is not looking from a bright page into a "
     "black room, and every 20 minutes look across the room at something far away for 20 seconds. "
     "If the print has to be very close or very bright before it is clear, that is worth an eye "
     "test."),
    avoid=("bedroom dark", "make the room dark", "blackout", "streetlight", "street light",
           "curtain", "curtains", "blind", "blinds", "car", "cars", "driving", "drive",
           "windscreen", "headlights", "full beam", "phone", "screen", "kindle", "monitor",
           "cataract", "cataracts", "night vision", "halos", "night feeds", "baby", "toddler",
           "eyes tired", "eyes are tired", "tired eyes", "eyes hurt", "eyes hurting",
           "eyes are sore", "sore eyes", "eyes ache", "eyes are aching", "aching eyes",
           "eye strain", "strained eyes",
           "smudged", "smudgy", "smudge", "smudges", "smeary", "smeared", "smear", "smears",
           "streaky", "streaked", "scratched", "scratches", "dirty", "dusty", "greasy",
           "fingerprint", "fingerprints", "fogging", "fogged", "foggy", "steamed up",
           "clean my", "cleaning my", "wipe my", "wiping my"),
    bias=3,
))


ENTRIES.append(entry(
    "sepsis",
    (("sepsis", "septicaemia", "septicemia", "blood poisoning", "blood infection"),
     ("what is", "whats", "symptoms", "signs", "treat", "treatment", "cause", "causes", "why",
      "serious", "dangerous", "fatal", "die", "recover", "recovery", "how long", "last",
      "contagious", "catch", "warning", "early", "sign", "is it", "have", "got", "ive",
      "could it be", "might it be", "start", "starts", "how do you get", "how do i know",
      "tell me about", "explain", "info", "information", "learn about", "should i know",
      "test", "tests", "blood test", "check", "septic", "shock")),
    ("Sepsis is the body over-reacting to an infection, and the whole danger is how fast it moves. "
     "Ring 999 now and say the word sepsis if there is an infection with any of: a fever with "
     "shaking chills, new confusion or drowsiness, breathing faster than usual, a lot of pain "
     "anywhere, clammy or mottled skin, or no pee all day. It is not a rash illness and it does "
     "not need a wound: a chest, urine, tooth or skin infection can start it. Treatment is IV "
     "antibiotics in the first hour, which is why the speed matters more than anything else, and "
     "most people who are treated early make a full recovery, though tiredness for weeks after "
     "is normal."),
    ask=("sepsis", "septicaemia", "septicemia", "blood poisoning", "septic"),
    avoid=("sepsis trust", "charity", "fundrais", "awareness", "campaign")))

ENTRIES.append(entry(
    "meningitis",
    (("meningitis", "meningitis b", "meningococcal", "spinal meningitis", "brain infection"),
     ("what is", "whats", "symptoms", "signs", "treat", "treatment", "cause", "causes", "why",
      "serious", "dangerous", "fatal", "die", "recover", "recovery", "how long", "last",
      "contagious", "catch", "spread", "warning", "early", "sign", "is it", "have", "got", "ive",
      "could it be", "might it be", "test", "vaccine", "vaccination", "jab", "rash",
      "tell me about", "explain", "info", "information", "learn about", "should i know",
      "stiff neck", "headache", "light", "viral", "bacterial")),
    ("Meningitis is an infection of the membranes around the brain and spinal cord, and it is a "
     "999 call, not a wait: a fever with a stiff neck, a bad headache, dislike of bright light, "
     "drowsiness or a rash that does not fade when a glass is pressed on it. Do not wait for the "
     "rash, because it can come late or not at all. A baby may only be floppy, feeding badly, "
     "grumpy when picked up, or crying high and not settling. Bacterial meningitis needs "
     "antibiotics in hospital the same day; the viral kind is milder and most people are over it "
     "in a week or two. The routine jabs cover the main bacterial kinds, so the red book is worth "
     "checking."),
    ask=("meningitis", "meningococcal", "meningitis b"),
    avoid=("charity", "fundrais", "awareness", "campaign", "symptoms checker")))

ENTRIES.append(entry(
    "pneumonia",
    (("pneumonia", "chest infection", "lung infection", "bronchopneumonia"),
     ("what is", "whats", "symptoms", "signs", "treat", "treatment", "antibiotics", "cause",
      "causes", "why", "serious", "dangerous", "fatal", "die", "recover", "recovery",
      "how long", "last", "lasts", "contagious", "catch", "spread", "warning", "sign",
      "is it", "have", "got", "ive", "could it be", "hospital", "x ray", "chest x ray",
      "tell me about", "explain", "info", "information", "learn about", "should i know",
      "walking", "elderly", "baby", "child", "cough", "fever", "breathless", "oxygen")),
    ("Pneumonia is an infection deep in the lungs that fills the air sacs with fluid, so it is a "
     "cold or flu that turns into a fever with a wet cough, faster breathing, a sharp pain in one "
     "side on breathing in, and feeling properly ill rather than just bunged up. Most chest "
     "infections are not pneumonia and settle on their own; the ones that are need a GP the same "
     "day, and 999 if there is fast breathing, confusion, or blue lips. A mild case is treated at "
     "home with antibiotics and the fever eases in a few days, though the cough can drag on for "
     "three to six weeks. Older people, babies and anyone with a long-term lung condition are the "
     "ones to ring about early rather than wait."),
    ask=("pneumonia", "chest infection", "lung infection"),
    avoid=("charity", "fundrais", "awareness", "campaign", "vaccine", "vaccination")))

ENTRIES.append(entry(
    "stroke",
    (("stroke", "mini stroke", "tia", "transient ischaemic attack", "brain bleed",
      "brain haemorrhage", "cerebral haemorrhage", "clot on the brain"),
     ("what is", "whats", "symptoms", "signs", "treat", "treatment", "cause", "causes", "why",
      "serious", "dangerous", "fatal", "die", "recover", "recovery", "rehab", "physio",
      "how long", "last", "warning", "sign", "is it", "have", "got", "ive", "could it be",
      "face", "arm", "speech", "slurred", "droopy", "weak", "weakness", "numb", "one side",
      "fast", "prevent", "risk", "blood thinner", "aspirin", "clot", "bleed", "hospital",
      "tell me about", "explain", "info", "information", "learn about", "should i know")),
    ("A stroke is the blood supply to part of the brain cut off, either by a clot or a bleed, and "
     "the test is FAST: Face - has one side dropped when they smile? Arms - can they lift both and "
     "hold them up? Speech - is it slurred or jumbled? Time - if any of those, ring 999 now and "
     "say the time it started, because clot-busting treatment works best in the first few hours. "
     "Give them nothing to eat or drink in case they cannot swallow. A TIA, the same signs passing "
     "in minutes, is still a 999 or same-day GP call, since it warns of a bigger one. Recovery is "
     "mostly physio and speech therapy in the first months, and the sooner it starts the more "
     "comes back."),
    ask=("stroke", "mini stroke", "tia", "brain bleed", "brain haemorrhage"),
    avoid=("heat stroke", "heatstroke", "sun stroke", "sunstroke", "brush stroke", "brushstroke",
           "stroke the", "stroke my", "stroke a", "stroke her", "stroke his", "hair stroke",
           "charity", "fundrais", "awareness", "campaign")))

ENTRIES.append(entry(
    "ibs",
    (("ibs", "irritable bowel", "irritable bowel syndrome", "spastic colon"),
     ("what is", "whats", "symptoms", "signs", "treat", "treatment", "get rid", "help",
      "better", "manage", "diet", "food", "eat", "trigger", "triggers", "cause", "causes",
      "why", "cure", "cured", "test", "tests", "diagnosed", "diagnosis", "how long", "last",
      "bloating", "bloated", "wind", "gas", "cramps", "cramping", "diarrhoea", "constipation",
      "poo", "stomach", "tummy", "have", "got", "ive", "fodmap", "fibre", "probiotic",
      "peppermint", "serious",
      "stop", "stopping", "flare", "flares", "flaring", "flare up", "flares up", "calm",
      "calming", "settle", "worse", "bad", "week", "episode", "how do i stop")),
    ("IBS is a gut that is sensitive rather than damaged: cramping, bloating, wind and a bowel "
     "that swings between loose and constipated, often for years, with nothing wrong found on "
     "tests. It is managed rather than cured. Eat at regular times, keep to soluble fibre - "
     "oats, psyllium, peeled fruit - rather than a lot of bran, drink peppermint tea for the "
     "cramps, and try a probiotic for a month; a dietitian-led low-FODMAP diet is the next step "
     "and is not one to guess at. See a GP for the diagnosis, and go sooner for blood in the "
     "stool, weight loss, a lump, or waking at night with pain, which are not IBS."),
    ask=("ibs", "irritable bowel", "spastic colon")))


ENTRIES.append(entry(
    "diabetes",
    (("diabetes", "diabetic", "type 1 diabetes", "type 2 diabetes", "t2 diabetes", "hba1c",
      "blood sugar", "prediabetes", "pre-diabetes", "insulin resistance"),
     ("what is", "whats", "symptoms", "signs", "treat", "treatment", "manage", "control",
      "look after", "live with", "diet", "food", "sugar", "test", "tests", "check", "checks",
      "blood pressure", "cholesterol", "tablets", "pills", "metformin", "insulin", "hypo",
      "cure", "reverse", "complications", "eyes", "feet", "kidneys", "weight", "exercise",
      "alcohol", "drive", "driving", "serious", "have", "got", "ive", "diagnosed", "told",
      "im", "am",
      "newly", "just", "type", "reverse it")),
    ("Type 2 diabetes is the body answering insulin less well, so blood sugar drifts up; type 1 "
     "is the body making no insulin and needs injecting from day one, and in a child that is a "
     "same-day job rather than a wait for a clinic. Type 2 is managed with an HbA1c blood test "
     "every few months, usually metformin to start, weight loss if that is possible for you, and "
     "fewer sugary drinks; type 1 with insulin and counting the carbs in what you eat. Ask the "
     "surgery for the yearly checks - feet, eyes, kidneys, blood pressure and cholesterol - if "
     "they have not been mentioned. A shaky, sweaty, muddled turn on insulin or a sulfonylurea is "
     "a hypo: sugar fast, then tell the GP."),
    ask=("diabetes", "diabetic", "type 1 diabetes", "type 2 diabetes", "hba1c", "blood sugar"),
    guard=lambda understood: not _a_high_reading(
        str((understood or {}).get("clean") or "") + " "
        + str((understood or {}).get("text") or "")) and _not_a_denial_of(
        "diabetes", "diabetic")(understood),
    avoid=("pregnant", "pregnancy", "expecting", "having a baby", "cook", "cooking", "recipe",
           "recipes", "meal", "meals", "meal ideas", "dinner",
           "lunch", "supper", "breakfast", "guest", "guests", "visitors", "coming for dinner",
           "coming over", "party", "buffet", "menu", "snack", "snacks", "dessert", "pudding",
           "cake", "bake", "baking", "what can i make", "what can i cook", "what should i cook",
           "lower my blood sugar", "lower blood sugar", "lower my sugar",
           "bring my blood sugar down", "bring blood sugar down", "get my blood sugar down",
           "blood sugar down", "reduce my blood sugar", "cut my blood sugar",
           "lower my hba1c", "bring my hba1c down")))

ENTRIES.append(entry(
    "epilepsy",
    (("epilepsy", "epileptic", "convulsion", "convulsions", "tonic clonic", "absence seizure",
      "absence seizures", "auras"),
     ("what is", "whats", "symptoms", "signs", "treat", "treatment", "tablets", "medication",
      "manage", "control", "live with", "drive", "driving", "licence", "dvla", "pregnant",
      "pregnancy", "alcohol", "sleep", "exercise", "sport", "swimming", "work", "job",
      "come off", "stop", "missed", "side effects", "have", "got", "ive", "diagnosed",
      "im", "am",
      "first", "aura", "serious", "curable", "cure", "child", "son", "daughter", "baby")),
    ("Epilepsy is a tendency to have seizures: a burst of electrical activity in the brain that "
     "can be a brief blank stare or a strange smell, or a full fit with jerking and loss of "
     "awareness. Most people are well controlled on one tablet - lamotrigine, levetiracetam or "
     "sodium valproate, chosen by a neurologist - and the three things that keep it that way are "
     "taking it every day, sleeping properly and going gently on alcohol. In the UK a first "
     "seizure means telling the DVLA and not driving for six months, so check the DVLA rules "
     "before you get back in the car. Ring 999 if a fit lasts more than five minutes, if another "
     "follows straight after, or if it is a first seizure and they are not coming round."),
    ask=("epilepsy", "epileptic", "convulsions", "tonic clonic", "absence seizure"),
    guard=_not_a_denial_of("epilepsy", "epileptic"),
    avoid=("fits", "fit", "does it fit", "fitting", "fitting a", "seizure first aid")))

_ASKS_WHETHER_SOMEONE_HAS_IT = re.compile(
    r"^\s*(?:so|and|but|oh|wait|also)?\s*(?:is|was|are|were|does|did|has|have|had)\s+"
    r"(?:\w+\s+){0,4}(?:coeliac|celiac|coeliacs)\s*[?.!,]*$")


def _not_a_yes_no_question(understood):
    return not _ASKS_WHETHER_SOMEONE_HAS_IT.match(str(understood.get("clean", "")).lower())


ENTRIES.append(entry(
    "coeliac",
    (("coeliac", "celiac", "coeliacs", "coeliac disease", "celiac disease",
      "gluten allergy", "gluten intolerant", "gluten intolerance"),
     ("what is", "whats", "symptoms", "signs", "treat", "treatment", "manage", "control",
      "live with", "diet", "testing", "test", "tests", "blood test", "biopsy", "diagnosed",
      "diagnosis", "im", "i am", "am", "is", "are", "was", "have", "has", "got", "ive",
      "my son", "my daughter", "my mum", "my dad", "my husband", "my wife", "child", "baby",
      "newly", "just told", "just been told", "cross contamination", "contamination", "oats",
      "bread", "gluten", "tablets", "pharmacist", "dietitian", "serious", "cure", "cured",
      "get better", "how long", "cause", "causes", "why",
      "anaemia", "anaemic", "iron", "b12", "vitamin", "deficiency", "tired", "tiredness",
      "exhausted", "bloating", "wind", "diarrhoea", "constipation", "weight loss",
      "mouth ulcers", "ulcers", "rash", "itchy", "bones", "osteoporosis", "fertility",
      "pregnant", "pregnancy", "blood test")),
    "Coeliac disease is an immune reaction to gluten that damages the lining of the gut - not "
    "an allergy, and it does not go away; the treatment is a strict gluten-free diet for life, "
    "and the gut heals over a few months of it. Strict, and that means being careful about the "
    "crumbs in a shared kitchen: a separate toaster, no knife going back in the butter or the jam, no chips from a "
    "fryer that has fried battered fish, oats only when the packet says gluten free, and a check "
    "on stock cubes, gravy, soy sauce and sausages. There is no cheat day: a little gluten keeps "
    "the gut inflamed even when you feel nothing, and the damage builds up quietly. Eating out "
    "works if you say coeliac when you book and ask what else goes in the fryer - restaurants "
    "that cook from scratch are easier than ones that assemble, and a takeaway with no answer is "
    "not worth it. Ask the GP for a dietitian once, and the pharmacist whether a tablet is safe. "
    "If it is a suspicion rather than a diagnosis, have the blood test before you cut gluten from "
    "your diet, because it only works while gluten is still in it.",
    ask=("coeliac", "celiac", "coeliacs", "coeliac disease", "celiac disease",
         "gluten allergy", "gluten intolerant", "gluten intolerance"),
    guard=_not_a_yes_no_question,
    bias=1,
    avoid=("cook", "cooking", "recipe", "recipes", "meal", "meals", "dinner", "lunch", "supper",
           "guest", "guests", "visitors", "coming for dinner", "party", "buffet", "menu",
           "cake", "bake", "baking", "what can i cook", "what should i cook", "what can i make",
           "one of them", "one of us", "one of the guests", "one of the others", "and one of",
           "isnt coeliac", "isn't coeliac", "wasnt coeliac", "wasn't coeliac", "not coeliac",
           "isnt celiac", "isn't celiac", "not celiac", "no coeliac", "no celiac",
           "doesnt have", "doesn't have", "dont have", "don't have", "havent got",
           "haven't got", "hasnt got", "hasn't got", "not been diagnosed",
           "never been diagnosed", "tested negative", "came back negative", "negative for",
           "ruled out", "no sign of", "not sure i have", "might have", "could have", "wonder if",
           "do i have", "have i got")))

ENTRIES.append(entry(
    "copd",
    (("copd", "chronic obstructive pulmonary disease", "emphysema", "chronic bronchitis"),
     ("what is", "whats", "symptoms", "signs", "treat", "treatment", "inhaler", "inhalers",
      "oxygen", "smoking", "stop smoking", "quit", "breathless", "breathlessness", "exercise",
      "rehab", "pulmonary rehab", "jab", "jabs", "flu", "vaccine", "worse", "flare", "flare up",
      "get better", "cure", "progress", "stage", "live with", "manage", "have", "got", "ive",
      "diagnosed", "spirometry", "cough", "phlegm", "serious", "life expectancy", "oxygen")),
    ("COPD is damage to the airways and air sacs, almost always from smoking, so breathing out "
     "gets slow: breathless on stairs or a hill, a cough most mornings, chest infections that "
     "hang on. It cannot be cured but it can be slowed a lot - stopping smoking is the one thing "
     "that changes the course, the inhalers work only if they are used every day rather than "
     "when it is bad, and pulmonary rehab, a supervised exercise course, does more for "
     "breathlessness than any tablet. Get the flu and pneumonia jabs, and ask the GP for a plan "
     "for bad days with steroids and antibiotics ready to go. Go to A&E for blue lips, "
     "confusion or breathlessness that is suddenly worse than your normal."),
    ask=("copd", "chronic obstructive pulmonary disease", "emphysema", "chronic bronchitis")))

ENTRIES.append(entry(
    "pcos",
    (("pcos", "polycystic ovary", "polycystic ovaries", "polycystic ovary syndrome"),
     ("what is", "whats", "symptoms", "signs", "treat", "treatment", "weight", "lose weight",
      "diet", "exercise", "period", "periods", "irregular", "missed", "fertility", "pregnant",
      "get pregnant", "trying", "hair", "acne", "skin", "insulin", "metformin", "pill",
      "test", "tests", "scan", "diagnosed", "manage", "control", "cure", "have", "got", "ive",
      "serious", "fertile", "ovulate", "ovulation", "symptoms of")),
    ("PCOS is ovaries that make more testosterone than usual, with insulin resistance behind it: "
     "periods that are irregular or stop, acne, hair on the face or chin, and weight that settles "
     "round the middle. About one woman in ten of childbearing age has it, and losing 5 to 10% of "
     "body weight often brings the periods back on its own. The GP can confirm it with a blood "
     "test and a scan; the pill regulates the periods and helps the skin and hair, metformin "
     "helps the insulin side, and if you want to get pregnant say so early, because a short "
     "course of tablets often restarts ovulation. Ask for a yearly blood pressure and blood "
     "sugar check, since the diabetes risk is the part that is easy to miss."),
    ask=("pcos", "polycystic ovary", "polycystic ovaries", "polycystic ovary syndrome")))

ENTRIES.append(entry(
    "crohns",
    (("crohns", "crohn's", "crohns disease", "crohn's disease", "ileitis"),
     ("what is", "whats", "symptoms", "signs", "treat", "treatment", "diet", "food", "eat",
      "flare", "flare up", "pain", "toilet", "surgery", "biologic", "biologics", "steroids",
      "azathioprine", "manage", "control", "cure", "cured", "test", "tests", "colonoscopy",
      "have", "got", "ive", "diagnosed", "tired", "weight", "serious", "life", "smoking",
      "pregnant", "pregnancy", "child", "work", "travel")),
    ("Crohn's is inflammation that turns up in patches anywhere from the mouth to the back "
     "passage, so it comes in waves: cramping pain, urgent diarrhoea, tiredness and weight loss, "
     "sometimes a sore mouth or sore joints. It is not caused by a bad diet and no diet cures it "
     "- treatment is steroids for a flare, then azathioprine or a biologic that a "
     "gastroenterologist chooses to keep it away, and stopping those because you feel better is "
     "how a flare comes back. Ask the GP to check B12, iron and vitamin D. Stop smoking, which "
     "makes it worse. Ring the IBD nurse at the first sign of a flare rather than waiting for the "
     "clinic, and go to A&E for blood in the stool with a fever and a fast heartbeat."),
    ask=("crohns", "crohn's", "crohns disease", "crohn's disease")))

ENTRIES.append(entry(
    "asthma-condition",
    (("asthma", "asthmatic"),
     ("what is", "whats", "symptoms", "signs", "treat", "treatment", "inhaler", "inhalers",
      "preventer", "reliever", "blue inhaler", "brown inhaler", "steroid", "spacer", "wheeze",
      "wheezing", "breathless", "cough", "night", "worse", "exercise", "running", "sport",
      "cold", "air", "pollen", "hayfever", "allergy", "smoking", "smoke", "vape", "damp",
      "mould", "pets", "cat", "dog", "dust", "attack", "flare", "control", "managed", "manage",
      "peak flow", "diagnosed", "have", "got", "ive",
      "im", "am", "child", "son", "daughter", "baby",
      "walk", "climb stairs", "serious", "cure")),
    ("Asthma is inflamed, twitchy airways: they narrow with a wheeze, a tight chest and a cough "
     "that is worse at night, in cold air or on exercise. The preventer inhaler - usually brown, "
     "a small dose of steroid - is the one that matters, and it has to be taken every day even "
     "when you feel fine; the blue reliever is for symptoms and needing it more than twice a week "
     "means the preventer is not right, so book a review with the asthma nurse. Use a spacer with "
     "both, take the flu jab, and ask for a written action plan. Ring 999 for an attack where "
     "talking in sentences "
     "is hard, the reliever is not helping, or the lips look blue."),
    guard=_not_a_denial_of("asthma", "asthmatic"),
    avoid=("pregnant", "pregnancy", "expecting", "having a baby"),
    ask=("asthma", "asthmatic")))

NAMED_CONDITIONS = (
    "shingles", "ringworm", "psoriasis", "piles", "tonsillitis", "athletes-foot", "verruca",
    "raynaud", "restless-legs", "constipation", "diarrhoea", "anaemia-signs", "throat-lump",
    "hair-loss", "nail-fungus", "nail-ridges", "skin-abscess", "mouth-ulcers", "white-patches-mouth",
    "thyroid-underactive", "thyroid-overactive", "hayfever-summer", "cold-sore", "verruca",
    "swollen-gland", "sore-limbs", "shoulder-click", "jaw-click", "shin-splints", "gum-disease",
    "gout", "norovirus", "sciatica", "cataract", "ibs", "diabetes", "epilepsy", "copd",
    "kidney-stone",
    "pcos", "crohns", "asthma",
)
for _named in ENTRIES:
    if _named.id in NAMED_CONDITIONS:
        _named.explain = True


PALPITATION_WORDS = (
    "racing", "races", "race", "pounding", "pounds", "pounding hard", "thumping", "thumps",
    "fluttering", "flutters", "pitter patter", "hammering", "beats fast", "beating fast",
    "beats quickly", "beating quickly", "fast heartbeat", "skipping", "skips", "skipped a beat",
    "misses a beat", "missed a beat", "irregular", "extra beat", "palpitations", "palpitation",
    "goes funny", "does a funny thing", "a funny turn",
    "keeps me awake", "wakes me up", "at night", "in bed", "when i lie down", "lying down",
    "all of a sudden", "out of nowhere", "for no reason")

_PALPITATIONS_ANSWER = (
    "Most racing, pounding or fluttering hearts are a normal heart beating hard rather than a "
    "damaged one: adrenaline, a big coffee, alcohol, a missed or late meal, dehydration, not enough "
    "sleep and a hot room all do it, and it settles within a few minutes if you sit down, breathe "
    "out for longer than you breathe in, and stop what you were doing. Go easy on the alcohol and "
    "the energy drinks, and eat something if it has been hours. Get it looked at soon if it comes "
    "with chest pain, breathlessness, dizziness or fainting, if it lasts more than a few minutes "
    "while you are sitting still, or if a close relative died young of a heart problem - and ring "
    "999 for chest pain with a racing heart, or if someone passes out.",)


ENTRIES.append(entry(
    "palpitations",
    (("heart", "pulse", "palpitations", "palpitation"),
     PALPITATION_WORDS),
    _PALPITATIONS_ANSWER,
    report=True,
    ask=("racing", "races", "race", "pounding", "pounds", "thumping", "fluttering", "flutters",
         "hammering", "skipping", "skips", "irregular", "palpitations", "palpitation",
         "beats fast", "beating fast", "fast heartbeat", "missed a beat", "misses a beat",
         "goes funny", "suddenly"),
    avoid=("heart rate", "heartrate", "bpm", "beats per minute", "blood pressure", "bp",
           "watch", "watch says", "fitbit", "smart watch", "smartwatch", "tracker", "sensor",
           "chest pain", "chest hurts", "chest tight", "crushing", "heart attack", "cardiac",
           "stent", "bypass", "pacemaker", "afib", "atrial fibrillation", "heart failure",
           "murmur", "cholesterol", "statin", "ecg", "exercise test",
           "coffee", "caffeine", "espresso", "energy drink", "energy drinks", "decaf",
           "heartburn", "indigestion", "heart shaped", "heart shape", "heart in my stomach",
           "love heart", "candy", "candies", "sweetheart", "heart of", "artichoke",
           "dog", "dogs", "puppy", "cat", "cats", "kitten", "rabbit", "hamster", "horse",
           "baby", "babies", "newborn", "toddler", "my son", "my daughter", "my child", "my kid",
           "pregnant", "pregnancy", "my thoughts", "my mind is racing")))


ENTRIES.append(entry(
    "palpitations-word",
    ("palpitations", "palpitation", "heart palpitations", "cardiac palpitations"),
    _PALPITATIONS_ANSWER,
    explain=True,
    report=True))

_LEGS_JELLY_ANSWER = (
    "Legs that feel like jelly for a few minutes are usually one of the ordinary things: a hot "
    "day or a hot room, a missed meal, standing still for a long time, a bug you are getting over, "
    "a first hard session at the gym, or adrenaline before something you are dreading. Sit down "
    "with your feet up for ten minutes, drink a glass of water, and eat something with salt or "
    "sugar in it - that is what puts the strength back. Get it looked at the same day if it comes "
    "with a weak or heavy arm, a drooping face, slurred speech or numbness down one side (ring 999 "
    "for those), if you cannot feel your saddle area or cannot pass urine, if it came on with a "
    "bad back, or if one leg has gone weak and stayed weak. Weak legs that come back every few "
    "days for weeks are worth a GP check with a blood test, because low iron, low vitamin D and a "
    "slow thyroid all do it.")

ENTRIES.append(entry(
    "legs-like-jelly",
    (("legs", "leg", "thighs", "thigh", "knees", "knee"),
     ("like jelly", "jelly", "wobbly", "weak", "weak as", "shaky", "shaking", "rubbery",
      "noodly", "noodles", "give way", "gave way", "giving way", "heavy", "cannot hold me",
      "cant hold me", "wont hold me", "wobble", "wobbles", "trembling", "unsteady", "buckle",
      "buckling", "gone to jelly", "turn to jelly", "turned to jelly", "feel like lead")),
    _LEGS_JELLY_ANSWER,
    bias=1,
    avoid=("chair", "chairs", "table", "tables", "stool", "stools", "bench", "benches", "sofa",
           "settee", "couch", "bed", "beds", "desk", "shelf", "shelves", "wardrobe", "cupboard",
           "drawer", "furniture", "ladder", "lamp", "wheel", "wheels", "pram", "pushchair",
           "buggy", "tripod", "trolley", "table leg", "chair leg", "wood", "wooden")))

_STOMACH_CHURN_ANSWER = (
    "A churning or gurgling stomach is usually wind moving through a normal gut, and it is noisier "
    "when the gut is empty because there is only gas in there to move. Eat something plain if it "
    "has been hours - toast, rice, a banana - chew with your mouth closed, drink water rather than "
    "fizzy drinks, and take a ten minute walk, which shifts trapped wind better than anything. "
    "Butterflies before something nerve-racking are the same feeling and they pass. See a GP if it "
    "comes with pain that keeps coming back, blood in your poo, weight going down, a lump, or more "
    "than three weeks of it, and if you are vomiting or cannot keep fluids down, ring 111.")

ENTRIES.append(entry(
    "stomach-churning",
    (("stomach", "tummy", "belly", "gut", "insides"),
     ("churning", "churns", "gurgling", "gurgles", "rumbling", "rumbles", "growling", "growls",
      "bubbling", "bubbles", "fluttering", "butterflies", "turning", "turns over", "knots",
      "wobbly", "noisy", "singing", "churn")),
    _STOMACH_CHURN_ANSWER,
    bias=1,
    avoid=("stomach ache", "stomachache", "pain", "hurts", "hurting", "agony", "cramps",
           "swollen", "bloated", "reflux", "heartburn", "acid", "sick", "vomit", "diarrhoea",
           "constipated", "pregnant", "period", "dog", "cat", "baby", "toddler", "child")))

_FEEL_FAINT_ANSWER = (
    "Sit or lie down for a few minutes with your feet up and your head low, loosen anything tight "
    "at the neck, and drink a glass of water - most faintness is a moment of low blood pressure or "
    "low blood sugar and passes with that. Eat something if it has been hours since you last did, "
    "and stand up slowly for the rest of the day. Ring 999 if you actually passed out and hit your "
    "head, if it comes with chest pain, a racing heart, breathlessness or a weak arm or drooping "
    "face, or if it happened while driving. Get a GP check soon if it keeps happening, if you are "
    "pregnant, or if you have been losing weight or bleeding.")

ENTRIES.append(entry(
    "feel-faint",
    (("faint", "faintness", "fainted", "light headed", "lightheaded", "light-headed", "woozy",
      "giddy", "seeing stars", "vision grey", "grey out", "greying out",
      "going to pass out", "came over all"),
     ("feel", "feels", "feeling", "felt", "nearly", "almost", "like im", "sudden", "suddenly",
      "all faint", "when i stand", "every time", "keeps", "keep", "a bit")),
    _FEEL_FAINT_ANSWER,
    report=True,
    avoid=("stand up", "standing up", "stood up", "shower", "hot bath", "hot tub", "sauna",
           "chest pain", "chest", "breathless", "short of breath", "racing heart", "palpitations",
           "bleeding", "blood", "stroke", "face", "speech", "arm", "hit my head", "hit his head",
           "bang", "banged", "fell", "fall", "passed out", "pass out", "black out",
           "blacked out", "blacking out", "pregnancy", "pregnant",
           "period", "diabetes", "insulin", "blood sugar", "dog", "cat", "baby", "child",
           "toddler", "driving", "driving home", "car")))

ENTRIES.append(entry(
    "a-shiny-patch-on-the-skin",
    (("patch", "patches", "area"),
     ("shiny", "shine", "greasy", "oily", "forehead", "nose", "cheek", "chin", "face", "skin",
      "scalp", "brow", "temple", "jaw", "t-zone")),
    "A shiny or dry patch on the face is usually one area of skin that is oilier or drier than "
    "the rest of it, "
    "or a little sun damage, and plain care settles most of them: wash with a gentle cleanser, "
    "pat dry rather than rub, and use a light oil-free moisturiser twice a day - give it a "
    "fortnight before you judge it. Show a pharmacist if it is raised, scaly, itchy or bleeding, "
    "because they can tell a harmless patch from one worth checking, and see a GP if it is "
    "growing, changing colour or still there after a few weeks.",
    avoid=("trousers", "jeans", "trouser", "skirt", "dress", "jacket", "sleeve", "sleeves",
           "coat", "shirt", "shoes", "boots", "leather", "fabric", "sofa", "couch", "carpet",
           "table", "wood", "worktop", "floor", "wall", "paint", "painted",
           "nicotine", "nicotine patch", "patch test", "eye patch", "patch of", "vegetable",
           "allotment", "garden", "lawn", "grass", "knee", "knees", "elbow", "elbows",
           "tarmac", "driveway", "road", "concrete"),
    bias=1))

ENTRIES.append(entry(
    "cant-stop-going-over-it",
    (("keep going over", "going over it", "going over the", "going over what", "going round it",
      "going round in my head", "round and round", "cant stop thinking", "can't stop thinking",
      "keep thinking about", "keep replaying", "replaying it", "replaying the", "over and over",
      "cant get it out of my head", "can't get it out of my head", "overthinking"),
     ("it", "that", "this", "what happened", "what i said", "what he said", "what she said",
      "the conversation", "the row", "the argument", "the news", "the diagnosis", "the mistake",
      "cancer", "ill", "illness", "dying", "hospital", "my friend", "my mum", "my dad", "my son",
      "my daughter", "my sister", "my brother", "my partner", "my husband", "my wife",
      "something i said", "yesterday", "last week", "years ago",
      "last message", "the message", "message i sent", "what i sent", "the text",
      "text i sent", "the email", "my reply", "the reply")),
    ("Give the loop a shape instead of trying to switch it off: ten minutes with a pen, one line "
     "saying the thing that keeps coming back, one line for what you are actually afraid of, and "
     "one line for the next thing you can do about it. Then do that one thing today, because going "
     "over a thing feels like working on it and is not: an unanswered message, a question for the "
     "doctor, a text that says you are thinking of them. If it is somebody else's illness, ask them "
     "what they want rather than deciding for them, and offer something specific - a lift, a meal, "
     "an hour on Thursday. If the same loop is still going weeks later, or it comes with no sleep, "
     "no appetite or no pleasure in anything, say so to a GP."),
    ask=("going over", "going round", "replaying", "over and over", "cant stop thinking",
         "can't stop thinking", "keep thinking", "in my head", "out of my head", "overthinking"),
    avoid=("night", "nights", "bed", "bedtime", "asleep", "sleep", "sleeping", "awake", "waking",
           "wake up", "woke up", "3am", "2am", "4am", "suicidal", "kill myself", "self harm",
           "want to die", "panic attack", "cant breathe", "exam", "test tomorrow", "interview",
           "app", "the app", "phone keeps", "computer", "laptop", "game", "the match"),
    bias=2))

HEALTHIER_WANT = ("want", "wanna", "need", "needed", "how", "become", "became", "start",
                  "starting", "improve", "improving", "better", "tips", "tip", "advice",
                  "should", "feel", "sort", "kick", "help", "idea", "ideas")
HEALTHIER_AVOID = (
    "eat", "eats", "eating", "ate", "food", "foods", "diet", "diets", "dieting", "recipe",
    "recipes", "meal", "meals", "dinner", "lunch", "breakfast", "snack", "snacks", "cook",
    "cooking", "porridge", "sugar", "salt", "carbs", "protein", "calories", "vitamin",
    "vitamins", "supplement", "supplements", "five a day", "vegan", "vegetarian", "alcohol",
    "drink", "drinking", "wine", "beer", "smoke", "smoking", "vape", "vaping", "cigarettes",
    "lose", "losing", "weight", "fat", "slim", "slimming", "fit", "fitness", "exercise",
    "exercising", "gym", "run", "running", "walking", "walk", "steps", "sleep", "sleeping",
    "smoking", "hair", "skin", "teeth", "tooth", "nails", "eyes", "blood", "pressure",
    "cholesterol", "diabetes", "thyroid", "liver", "kidney", "heart", "cancer", "ache",
    "pain", "sick", "ill", "cold", "flu", "cough", "baby", "babies", "child", "children",
    "kids", "kid", "toddler", "pregnant", "pregnancy", "dog", "cat", "pet", "pets",
    "coming off", "come off", "stopping", "quitting", "quit", "coffee", "tea", "juice",
    "water", "hydration", "menopause", "period", "perimenopause", "medication", "tablets",
    "battery", "batteries", "phone", "iphone", "android", "laptop", "computer", "tablet",
    "device", "charger", "charging", "boiler", "car", "washing machine", "dishwasher",
)
ENTRIES.append(entry(
    "a-healthier-fortnight",
    (("healthier", "healthiest", "healthy", "health", "general health", "better shape",
      "in shape", "health kick", "wellbeing", "well being", "look after myself",
      "look after myself better"),
     HEALTHIER_WANT),
    "Pick one thing for two weeks, not five: a twenty-minute walk after a meal, a vegetable with "
    "every main meal, or water instead of the second fizzy drink. Any one of those is most of what "
    "\"healthier\" means, one that sticks beats three that don't, and two weeks is long enough to "
    "know whether it fits your week. Which of the three could you start tomorrow?",
    avoid=HEALTHIER_AVOID))

DIABETES_WORDS = ("type 2 diabetes", "type two diabetes", "type 2", "type two", "diabetes",
                  "diabetic", "diabetics", "t2d", "blood sugar", "blood sugars", "hba1c", "a1c",
                  "average blood")
DIABETES_ASK = ("what", "whats", "explain", "tell me", "mean", "means", "reversible", "reverse",
                "remission", "cure", "cured", "serious", "run in families", "families", "family",
                "inherit", "inherited", "tired", "tiredness", "why", "worse", "difference",
                "worse than", "hba1c", "a1c", "type 1", "type one", "number", "numbers",
                "checked", "check", "diagnosed", "diagnosis", "run in the family",
                "in the family", "hereditary", "genetic", "make you tired", "makes you tired",
                "so tired", "exhausted", "knackered", "no energy", "weary")
DIABETES_AVOID = (
    "eat", "eats", "eating", "ate", "food", "foods", "diet", "diets", "recipe", "recipes",
    "meal", "meals", "dinner", "lunch", "breakfast", "snack", "snacks", "cook", "cooking",
    "banana", "bananas", "honey", "fruit", "sugar", "carbs", "carb", "carbohydrate", "rice",
    "bread", "pasta", "potato", "potatoes", "cake", "biscuit", "chocolate", "sweet", "sweets",
    "drink", "drinks", "drinking", "beer", "wine", "alcohol", "pint", "lager", "juice",
    "fizzy", "cola", "coffee", "tea", "insulin", "tablet", "tablets", "medication",
    "medicines", "medicine", "dose", "doses", "metformin", "injection", "injections",
    "exercise", "exercising", "gym", "run", "running", "walk", "walking", "steps", "weight",
    "lose", "losing", "slim", "pregnant", "pregnancy", "expecting", "breastfeeding",
    "child", "children", "kids", "kid", "son", "daughter", "baby", "toddler", "mum", "mother",
    "dad", "father", "husband", "wife", "partner", "friend", "husbands", "foot", "feet", "toe",
    "toes", "wound", "wounds", "cut", "cuts", "sore", "sore", "numb", "eye", "eyes", "vision",
    "kidney", "kidneys", "heart", "stroke", "amputation", "hypo", "hypos", "hyper",
    "test strip", "test strips", "meter", "monitor", "finger prick", "libre", "cgm",
    "course", "carbs", "keto", "fasting", "nurse", "gp", "doctor", "hospital", "appointment",
)
_JUST_TOLD_ROW = entry(
    "just-told-about-diabetes",
    (DIABETES_WORDS,
     ("just told", "just been told", "only just", "just diagnosed", "newly diagnosed",
      "diagnosed", "found out", "told yesterday", "told today", "came as a shock", "shock",
      "shocked", "scared", "frightened", "worried", "worries", "afraid", "nervous", "what now",
      "next", "help", "understand", "makes sense")),
    "That is a lot to take in from one appointment, and it is normal to leave not sure what to do "
    "next. Three things worth asking your GP or diabetes nurse: what is my HbA1c, do I need "
    "medication yet, and can I be referred to a structured course - most areas run one free and "
    "the people who do it keep better numbers. Nothing has to change today.",
    avoid=DIABETES_AVOID)
_JUST_TOLD_ROW.explain = True
ENTRIES.append(_JUST_TOLD_ROW)
ENTRIES.append(entry(
    "smear-test",
    (("smear test", "smear", "smears", "cervical screening", "cervical smear", "pap test",
      "hpv test"),
     ("what is", "whats", "what's", "screening", "letter", "invited", "invitation", "how often",
      "when", "how long", "does it hurt", "hurt", "painful", "pain", "results", "result",
      "abnormal", "come back", "recall", "age", "25", "50", "64", "book", "appointment",
      "nurse", "gp", "should i", "do i need", "worth", "missed", "never been", "first")),
    ("A smear test checks the cells on the cervix for the changes that can turn into cancer, and "
     "it takes about five minutes with a nurse: a soft brush collects a sample and most people "
     "feel a scratch rather than pain. The sample is tested for HPV first, and only a positive "
     "one goes on to be looked at under a microscope, which is why most results come back "
     "normal. It is offered every three years from 25 to 49 and every five years from 50 to 64; "
     "an abnormal result usually means a repeat in a year, not cancer."),
    avoid=("smear test on my dog", "smear of blood", "bloody smear", "smear on the wall",
           "smear of paint", "paprika", "job screening", "dbs", "job interview", "references",
           "recruiter", "film screening", "cinema", "tv screen", "screen door", "sun screen",
           "sunscreen", "screening room"),
    bias=1,
    ask=("smear", "smear test", "cervical screening", "cervical smear", "pap test", "hpv")))

_A_GASP_FOR_A_THING = re.compile(
    r"\bgasp\w*\s+(?:for|at|after)\s+(?:a|an|the|some|any|my|me|that|one)\s+"
    r"(?!(?:[\w'-]+\s+){0,1}(?:air|breath|breathe|breathing|oxygen|help|doctor|nurse|"
    r"ambulance|paramedic|paramedics|inhaler|nebuliser|nebulizer|ventilator|respirator|"
    r"999|911|111|rescue|defibrillator|aed)\b)[\w'-]+")


def _a_gasp_for_a_thing_is_a_thirst(understood):
    line = str(understood.get("clean") or "").lower()
    return not _A_GASP_FOR_A_THING.search(line)


ENTRIES.append(entry(
    "sleep-apnoea",
    (("sleep apnoea", "sleep apnea", "apnoea", "apnea", "obstructive sleep apnoea",
      "obstructive sleep apnea", "stop breathing", "stops breathing", "stopped breathing",
      "gasping for air", "gasping for breath", "gasp for air", "gasp for breath",
      "wake up gasping", "wakes up gasping", "woke up gasping", "waking up gasping",
      "wake up choking", "woke up choking", "gasping in my sleep", "gasp in my sleep",
      "gasping at night", "gasp at night", "snoring and gasping", "snore and gasp",
      "sleep study", "sleep test", "sleep clinic", "cpap",
      "cpap machine", "mouth splint"),
     ("what is", "whats", "what's", "snoring", "snore", "stop breathing", "stops breathing",
      "gasping", "choking", "wake up", "waking", "tired", "knackered", "exhausted", "sleepy",
      "daytime", "headache", "test", "tested", "sleep study", "cpap", "machine", "mask",
      "know", "if i have", "how do i know", "do i have",
      "treatment", "treat", "help", "serious", "dangerous", "lose weight", "alcohol")),
    ("Sleep apnoea is the airway at the back of the throat closing for ten seconds or more, many "
     "times a night, so breathing stops in short bursts and you wake just enough to start again - "
     "which is why the snoring breaks off and why eight hours leaves you flat. The signs are loud "
     "snoring with silences, a gasp or a choke, a dry mouth and a morning headache, and nodding "
     "off in the day; extra weight, a thick neck, alcohol at night and sleeping on your back all "
     "make it worse. Ask a GP for a sleep study - it is done at home with a monitor on your "
     "finger - because a CPAP mask or a mouth splint fixes most cases and untreated it is hard "
     "on the heart."),
    avoid=("dog", "cat", "baby", "newborn", "toddler", "child", "children", "kid", "kids",
           "my son", "my daughter", "snoring joke"),
    ask=("sleep apnoea", "sleep apnea", "apnoea", "apnea", "stop breathing",
         "stops breathing", "gasping", "sleep study", "sleep test", "sleep clinic", "cpap",
         "splint"),
    report=True, bias=1, guard=_a_gasp_for_a_thing_is_a_thirst))

ENTRIES.append(entry(
    "sleep-apnoea-treatment",
    (("sleep apnoea", "sleep apnea", "apnoea", "apnea", "cpap", "cpap machine", "sleep study",
      "sleep test", "sleep clinic", "mouth splint"),
     ("i have", "ive got", "i've got", "got diagnosed", "diagnosed", "treatment", "treat",
      "treating", "manage", "managing", "cope", "help", "machine", "mask", "splint", "study",
      "test", "weight", "alcohol", "how do i", "what can i do", "advice", "better", "worse",
      "worth it", "side effects", "keep taking it off", "cant wear it",
      "sleep study", "sleep test", "sleep clinic", "mouth splint", "splint", "cpap machine",
      "need", "at risk", "risk", "put up with",
      "lose weight", "losing weight", "losing some weight", "cure", "cured", "get rid of",
      "diagnosed with", "what happens")),
    ("The mask is the part that changes things: a CPAP machine holds the throat open with a "
     "gentle stream of air, and a mouth splint does a milder version of the same job. Getting one "
     "starts with a sleep study - usually a night at home with a monitor on your finger, "
     "sometimes a night in a clinic - and the GP refers you for it. Losing some weight if you "
     "can, keeping alcohol to early evening and sleeping on your side all help around the edges. "
     "If you have been given a mask and keep taking it off, say so: most people who give up on "
     "CPAP were fitted with the wrong mask rather than the wrong treatment, and a nasal one or a "
     "different cushion is often all it takes."),
    avoid=("dog", "cat", "baby", "newborn", "toddler", "child", "children", "kid", "kids",
           "my son", "my daughter", "do i have", "if i have", "how do i know",
           "signs", "symptoms"),
    ask=("sleep apnoea", "sleep apnea", "apnoea", "apnea", "cpap", "sleep study", "sleep test",
         "sleep clinic", "splint"),
    report=True, bias=2, guard=_a_gasp_for_a_thing_is_a_thirst))

ENTRIES.append(entry(
    "long-sighted",
    (("long sighted", "longsighted", "long sight", "long-sighted", "hyperopia",
      "hypermetropia", "far sighted", "farsighted", "far-sighted"),
     ("what is", "whats", "what's", "mean", "means", "is it", "am i", "glasses", "test",
      "optician", "blurred", "blurry", "close", "reading", "phone", "headache", "headaches",
      "tired eyes", "children", "child", "age", "get worse", "fix", "correct", "laser",
      "contacts", "contact lenses")),
    ("Long sighted means the near things are the blurry ones: the eye is a little short, or the "
     "lens too weak, so light from a page would come to a focus behind the retina and the eye "
     "has to pull it forward by straining. That is why small print and phone screens get held "
     "further away, and why the eyes ache and the head thumps by evening rather than first thing. "
     "An optician sorts it with glasses or contact lenses, and a child who is long sighted can "
     "read the board but not a book, so a test is worth it if schoolwork slips."),
    avoid=("long sighted animal", "long distance", "long sight of"),
    ask=("long sighted", "longsighted", "long sight", "hyperopia", "far sighted", "farsighted")))


ENTRIES.append(entry(
    "kidney-infection",
    (("kidney infection", "kidney infections", "infected kidney", "pyelonephritis",
      "kidney infection symptoms", "signs of a kidney infection"),
     ("what are", "whats", "what is", "signs", "symptoms", "how do i know", "how long",
      "serious", "dangerous", "should i worry", "need antibiotics", "go to hospital",
      "how do i", "feel like", "symptom", "i have", "i think i have", "got", "diagnosed",
      "been told", "hospital")),
    "The signs are a temperature or shivering with pain in one side of your back under the ribs, "
    "often with the usual urinary signs - needing to wee more, burning, and smelly or cloudy wee - "
    "and sometimes feeling sick. Ring the doctor or 111 the same day and say you think it is a "
    "kidney infection: it needs antibiotics and is not something to wait out. Go to A&E if you "
    "are confused, very shaky, have a stiff neck or stop passing wee.",
    avoid=("cystitis", "uti", "utis", "water infection", "bladder infection", "burning",
           "burns", "stings", "keep getting", "recurrent", "prevent", "stone", "stones",
           "dialysis", "transplant", "disease", "failure", "diet", "function", "creatinine"),
    bias=2))


_GROWN_RELATION = ("brother", "sister", "husband", "wife", "partner", "mum", "mother", "dad",
                   "father", "gran", "grandma", "grandad", "grandpa", "nanna", "nan", "friend",
                   "neighbour", "neighbor", "colleague", "flatmate", "housemate", "uncle",
                   "aunt", "auntie", "boyfriend", "girlfriend", "stepdad", "stepmum")

_CHILD_WORD = ("baby", "babies", "toddler", "toddlers", "newborn", "child", "children", "kid",
               "kids", "infant", "nursery", "school age", "little one", "teenager", "teen",
               "my son", "my daughter", "grandchild", "grandchildren")

_AN_AGE = re.compile(r"\b(\d{1,2})\s*(?:month|months|yr|yrs|year|years)?\s*old\b")

ADULT_COUGH_REPLY = (
    "Most coughs after a cold last two to three weeks and settle on their own: honey in warm "
    "drinks, plenty of fluids and a propped-up pillow at night ease it, and cough medicines do "
    "little. See a GP if it lasts more than three weeks, they are coughing blood or breathless, "
    "they have lost weight, or it came with a fever that will not go - and the same day if they "
    "are breathing fast, suck in under the ribs, or their lips look blue.")


def _grown_cough(memory, understood):
    text = understood.get("clean") or ""
    words = understood.get("words") or []
    joined = (text + " " + " ".join(str(word) for word in words)).lower()
    if not any(word in joined for word in ("cough", "coughing", "coughed")):
        return None
    if any(word in joined for word in _CHILD_WORD):
        return None
    for age in _AN_AGE.findall(joined):
        if int(age) < 18:
            return None
    if any(word in joined for word in _GROWN_RELATION):
        return ADULT_COUGH_REPLY
    return None


ENTRIES.append(entry(
    "a-grown-persons-cough",
    (("cough", "coughing", "coughed"), _GROWN_RELATION),
    _grown_cough,
    bias=4,
    avoid=("my cough", "i have a cough", "ive had this cough", "smoker", "smoking", "vape",
           "x ray", "chest xray",
           "breathless", "short of breath", "struggling to breathe", "can't breathe",
           "cant breathe", "cannot breathe", "blue lips", "fever", "temperature",
           "blood", "chest pain", "chest infection", "wheeze", "wheezing"),
))


ALLERGY_WORDS = ("allergic", "allergy", "allergies", "allergen", "allergens", "antihistamine",
                 "antihistamines", "cetirizine", "loratadine", "piriton", "clarityn",
                 "hayfever", "hay fever", "immunotherapy", "desensitise", "desensitised",
                 "sneeze", "sneezes", "sneezing", "sneezy", "wheezing", "wheezy",
                 "itchy eyes", "watery eyes", "runny eyes", "streaming eyes")

ALLERGY_PETS = ("cat", "cats", "kitten", "kittens", "dog", "dogs", "puppy", "puppies",
                "pet", "pets", "rabbit", "rabbits", "hamster", "hamsters", "guinea",
                "budgie", "budgies", "parrot", "horse", "horses", "fur", "furry", "dander",
                "animal", "animals", "dog hair", "cat hair", "animal hair")

ALLERGY_NOT = ("vet", "vets", "fleas", "flea", "worms", "worming", "vaccination", "jabs",
               "nut", "nuts", "peanut", "peanuts", "egg", "eggs", "milk", "dairy", "soya",
               "soy", "wheat", "gluten", "shellfish", "sesame", "food", "foods", "eat",
               "eating", "ate", "restaurant", "curry", "menu", "takeaway", "weaning",
               "wean", "baby", "babies", "toddler", "reaction", "anaphylaxis", "epipen",
               "epi pen",
               "scratching", "scratches", "scratch", "claws", "biting", "bites", "naughty",
               "door", "sofa", "furniture", "carpet", "litter", "house training",
               "sick", "vomiting", "diarrhoea", "limp", "coughing", "hair loss", "mange"
               )

_PET_AS_SUBJECT = re.compile(
    r"^(?:so|and|but|well|hi|hiya|hello)?\s*(?:my|the|our|his|her|their|this|that)\s+"
    r"(?:\w+\s+){0,2}"
    r"(?:cat|cats|kitten|kittens|dog|dogs|puppy|puppies|pup|rabbit|rabbits|hamster|hamsters|"
    r"guinea|budgie|budgies|parrot|horse)\b")
_PET_SYMPTOM = re.compile(r"sneez|cough|wheez|runny nose|runny eye|sniff|conjunctiv")
_THE_PERSON_IS_REACTING = re.compile(r"\b(?:me|i|i'm|im|my nose|my eyes|my throat|us|we|making|makes|"
                           r"make|gives|giving|gave|set off|sets off)\b")


def _the_pet_has_the_symptom(understood):
    text = (understood.get("clean") or "").lower()
    start = _PET_AS_SUBJECT.match(text)
    if not start:
        return False
    rest = text[start.end():]
    symptom = _PET_SYMPTOM.search(rest)
    if not symptom:
        return False
    return not _THE_PERSON_IS_REACTING.search(rest[:symptom.start()])


ENTRIES.append(entry(
    "pet-allergy",
    (ALLERGY_WORDS, ALLERGY_PETS),
    "Cat and dog allergy is a protein in the skin flakes, saliva and urine rather than in the "
    "hair, and it sticks to anything soft: keep the animal out of the bedroom and off the sofa, "
    "wash your hands after touching it, damp-dust rather than dry-dust, vacuum with a HEPA "
    "filter and wash the bedding at 60C. A daily antihistamine, or a steroid nasal spray from "
    "the pharmacist, covers the days that are bad. See a GP if it is setting off asthma or "
    "waking you at night, and if you want to live with the animal anyway ask about "
    "immunotherapy - three to five years of it is the only thing that changes the allergy "
    "itself rather than the symptoms.",
    ask=ALLERGY_WORDS,
    avoid=ALLERGY_NOT,
    guard=lambda understood: not _the_pet_has_the_symptom(understood),
    bias=2))

_FRUIT_TRIGGER = (
    "strawberries", "strawberry", "apple", "apples", "peach", "peaches", "nectarine", "kiwi",
    "kiwis", "melon", "melons", "banana", "bananas", "cherry", "cherries", "plum", "plums",
    "tomato", "tomatoes", "carrot", "carrots", "celery", "cucumber", "avocado", "raw fruit",
    "raw veg", "raw vegetables", "fruit", "nuts", "hazelnuts", "almonds",
    "pear", "pears", "watermelon", "watermelons", "pineapple", "pineapples", "apricot",
    "apricots", "mango", "mangoes",
    "pollen", "hay fever",
)

_FRUIT_ITSELF = tuple(word for word in _FRUIT_TRIGGER
                      if word not in ("rash", "hives", "itchy", "when i eat", "after eating",
                                      "after i eat"))
ENTRIES.append(entry(
    "fruit-that-itches",
    (("rash when i eat", "rash after eating", "rash after i eat", "itchy mouth", "mouth itches",
      "mouth tingles", "tingling mouth", "mouth is itchy", "mouth gets itchy", "itchy throat",
      "throat itches", "mouth feels funny", "tongue tingles", "scratchy mouth", "sore mouth after",
      "mouth burns when i eat", "allergic to fruit", "allergic to raw", "reaction to fruit",
      "rash", "hives", "itchy") + _FRUIT_TRIGGER[:12],
     _FRUIT_TRIGGER + ("rash", "rashes", "rashy", "hives", "itch", "itches", "itching")),
    "Raw fruit and veg that make your mouth tingle, itch or come up in a rash is usually oral "
    "allergy syndrome: the proteins in apple, peach, kiwi, melon, tomato and strawberry are close "
    "enough to birch or grass pollen that your body treats them as pollen. The itch stays in the "
    "mouth and lips and settles within an hour. Most people find the cooked or peeled version is "
    "fine, because heat and peeling break the protein down, and an antihistamine from a pharmacy "
    "eases a bad day. See a GP if it happens with nuts or several fruits, or the rash spreads "
    "beyond the mouth. Swelling of the lips, tongue or throat, a wheeze, or trouble breathing is "
    "999 - that is a real allergy, not this.",
    bias=1,
    guard=lambda understood: any(word in " " + understood.get("text", "") + " "
                                 for word in _FRUIT_ITSELF),
    avoid=("swell", "swelling", "swollen", "throat closing", "cant breathe", "can't breathe",
           "breathless", "wheeze", "wheezing", "faint", "fainted", "anaphylaxis", "adrenaline",
           "epipen", "eppy pen", "lips", "lip is", "tongue is", "tongue has", "stung", "sting",
           "bee", "wasp", "nettle", "penicillin", "antibiotic", "amoxicillin", "plaster",
           "detergent", "washing powder", "soap", "nickel", "jewellery", "dog", "cat", "puppy",
           "kitten", "baby", "babies", "nappy",
           "hay fever season", "pollen count", "eczema", "psoriasis", "heat rash",
           "nappy rash", "shaving", "deodorant", "sun cream", "suncream", "latex")))
CONDITIONS = (
    ("hernia",
     ("hernia", "hernias", "inguinal hernia", "hiatus hernia", "hiatus hernias", "groin hernia",
      "stomach hernia", "umbilical hernia", "strangulated hernia"),
     "A hernia is tissue pushing through a weak spot in the muscle wall: a soft lump in the groin "
     "or at the navel that shows when you cough or stand, and a hiatus hernia is the stomach "
     "sliding up into the chest and causing heartburn. Most are not urgent, and a GP refers the "
     "ones that hurt or keep growing for a small operation. Get it seen the same day if the lump "
     "goes hard, tender and will not push back in."),
    ("carpal-tunnel",
     ("carpal tunnel", "carpal tunnel syndrome", "tunnel in my wrist", "carpal"),
     "Carpal tunnel is a nerve squeezed where it passes through the wrist: numbness, tingling or "
     "pins and needles in the thumb, index and middle fingers, often worst at night and eased by "
     "shaking the hand. A wrist splint worn at night from a pharmacy is the first thing and "
     "settles most mild cases; if the hand is weak or you keep dropping things, see a GP, because "
     "an injection or a small operation stops it getting worse."),
    ("stomach-ulcer",
     ("stomach ulcer", "stomach ulcers", "gastric ulcer", "duodenal ulcer", "peptic ulcer",
      "ulcer in my stomach", "ulcer in my tummy", "ulcers in my stomach"),
     "A stomach ulcer is a raw patch in the lining of the stomach or the first part of the bowel, "
     "usually from an H. pylori infection or from ibuprofen and other anti-inflammatory "
     "painkillers: a gnawing or burning pain high in the belly, worse when you are hungry or at "
     "night. See a GP - a breath or stool test for H. pylori and a course of acid-suppressing "
     "tablets clears most of them. Ring 999 for vomited blood or black tarry stools."),
    ("cellulitis",
     ("cellulitis", "cellulitis infection", "skin infection cellulitis"),
     "Cellulitis is a skin infection that turns an area red, hot, swollen and tender and keeps "
     "spreading, most often on a lower leg: it needs antibiotics the same day, so ring the GP or "
     "111, and draw a line round the edge with a pen so you can see whether it is shrinking. Get "
     "seen urgently if it is on the face or near an eye, if the skin blisters or goes dark, or if "
     "there is a fever with shivering and feeling very unwell."),
    ("long-covid",
     ("long covid", "long-covid", "long covid symptoms", "post covid", "after covid"),
     "Long covid is symptoms that carry on more than four weeks after the infection: "
     "breathlessness on the stairs, a tiredness that gets worse after effort, brain fog, a racing "
     "heart and poor sleep. What helps most is pacing - a small amount of activity, then a rest "
     "before you feel you need it, rather than pushing through - and a GP can refer you to a long "
     "covid clinic. Keep a note of what you did the day before a bad day."),
    ("flu-jab",
     ("flu jab", "flu jabs", "flu vaccine", "flu vaccines", "flu vaccination", "flu shot",
      "flu injection", "jab for flu", "vaccine for flu", "the flu jab", "the flu vaccine"),
     "The flu jab is one injection in the arm, best in October, and it is free on the NHS for "
     "anyone over 65, pregnant women, children from 2 up to 17 as a nasal spray, carers, and "
     "people with asthma, diabetes, heart, lung or kidney disease or a weakened immune system. It "
     "cannot give you flu; a sore arm for a day or two is the usual reaction. A pharmacy or the GP "
     "surgery books it."),
    ("blood-clot",
     ("dvt", "deep vein thrombosis", "blood clot", "blood clots", "clot in my leg",
      "blood clot in my leg", "clot in the leg", "thrombosis"),
     "A DVT is a clot in a deep vein, usually in the calf: one leg swollen, warm and tender, often "
     "with a heavy ache, and it is a same-day job - ring 111 or the GP, because a clot can travel "
     "to the lung. Sudden breathlessness, a sharp pain when you breathe in, or coughing blood "
     "means a clot may already be there, so ring 999. The GP sorts the scan and the blood thinner; "
     "do not rub the leg or wait to see if it settles."),
    ("scarlet-fever",
     ("scarlet fever", "scarletina", "strawberry tongue", "sandpaper rash"),
     "Scarlet fever is a strep infection: a sore throat with a rough, sandpapery rash that feels "
     "like goosebumps, flushed cheeks and a red strawberry tongue, and it needs antibiotics from "
     "a GP the same day - children are usually much better within 24 to 48 hours of starting "
     "them. Keep them off school until 24 hours of antibiotics have been taken, give plenty to "
     "drink and paracetamol for the sore throat, and get advice if the fever lasts past five "
     "days, the rash spreads, or there is earache or swelling in the neck."),
    ("dengue",
     ("dengue", "dengue fever", "breakbone fever"),
     "Dengue is a virus spread by daytime-biting mosquitoes in the tropics, and it is not passed "
     "from person to person: sudden high fever, a severe headache behind the eyes, deep muscle and "
     "joint pain and often a rash, with the fever usually breaking after three to seven days. Take "
     "paracetamol only - ibuprofen and aspirin raise the risk of bleeding - drink plenty, and get "
     "seen the same day for sickness that will not stop, tummy pain, bleeding gums or nose, or "
     "drowsiness, because those are the warning signs of the severe form. It is worth telling any "
     "doctor you see where you travelled."),
    ("yellow-fever",
     ("yellow fever", "yellow fever vaccine", "yellow fever jab"),
     "Yellow fever is a mosquito-borne virus in parts of Africa and South America, and most people "
     "have a fever, headache, muscle ache and sickness for about a week and then recover. A small "
     "share go on to jaundice, bleeding and organ failure, which is a 999 emergency, so get seen "
     "quickly for yellow skin or eyes, bleeding or vomiting. The vaccine is the protection: a "
     "travel clinic gives it, some countries require a certificate to enter, and it needs booking "
     "at least six to eight weeks before you fly."),
    ("rheumatic-fever",
     ("rheumatic fever", "rheumatic", "strep throat", "strep a"),
     "Rheumatic fever is the body reacting to an untreated strep throat or scarlet fever two to "
     "four weeks later: a fever with painful, swollen joints that move around, sometimes a rash "
     "and a racing heart, and it needs a GP the same day because it can scar the heart valves. "
     "The protection is treating a sore throat with the antibiotics the GP prescribes and finishing "
     "the course, so a sore throat with a fever and swollen neck glands in a child is worth having "
     "swabbed rather than waited out. It is now rare in the UK but still seen in children aged 5 "
     "to 15."),
)

_CONDITION_ASKS = (
    "what is", "what are", "whats", "what's", "tell me", "explain", "describe",
    "treat", "treated", "treatment", "get rid", "cure", "cured", "fix", "help", "ease",
    "cause", "causes", "caused", "why", "how long", "how do i", "how can i", "what should i do",
    "symptom", "symptoms", "sign", "signs", "feel", "feels", "like", "look", "looks",
    "pain", "painful", "hurt", "hurts", "aching", "ache", "sore", "swollen", "swelling",
    "worse", "better", "getting", "spread", "spreading", "spread to", "bigger", "larger",
    "serious", "dangerous", "bad", "catching", "contagious", "infectious", "normal",
    "diagnosed", "diagnosis", "test", "tests", "scan", "operation", "surgery", "operate",
    "tablet", "tablets", "medicine", "medication", "antibiotic", "antibiotics", "cream",
    "diet", "exercise", "prevent", "prevention", "avoid", "stop", "go away", "clear up",
    "recover", "recovery", "long", "weeks", "months", "years", "worried", "worry",
    "gp", "doctor", "111", "999", "hospital", "a and e", "urgent", "same day",
    "should i", "do i need", "is it", "can it", "will it")

_WHEN_TO_GET_IT = ("when should i", "when do i", "when can i", "when is", "how much", "cost",
                   "costs", "price", "prices", "pay", "free", "where can i", "where do i",
                   "book", "booking", "appointment", "pharmacy")

for _condition_id, _condition_names, _condition_said in CONDITIONS:
    ENTRIES.append(entry(
        "condition-" + _condition_id,
        (_condition_names, _CONDITION_ASKS),
        _condition_said,
        explain=True,
        report=True,
        bias=3,
        avoid=PETS + _WHEN_TO_GET_IT))
ENTRIES.append(entry(
    "hoarding-is-a-condition",
    (("hoarding", "hoard", "hoarder", "hoarders", "cant throw anything away",
      "can't throw anything away", "cannot throw anything away", "keep everything",
      "throwing anything away"),
     ("help", "stop", "how", "what can i do", "why", "treatment", "therapy", "cure",
      "get better", "worried", "concerned", "worse", "family", "mum", "dad", "mother",
      "father", "partner", "husband", "wife", "brother", "sister", "friend",
      "start", "begin", "first", "stuck", "cant", "can't", "wont", "won't", "struggling")),
    "Hoarding is a recognised condition, and it is treatable: CBT from a therapist who works on "
    "hoarding is what helps, so the first step is a GP appointment, and it is worth saying how much "
    "of the home is unusable and whether anyone is at risk. Don't let anyone clear the house for "
    "you in one go — it usually comes back and it is frightening to lose things that way. Start "
    "with one shelf or one drawer, decide on the smallest thing first, and ask the GP about a "
    "referral to the local hoarding or mental health team. Mind and Hoarding UK both advise "
    "families too, and Hoarding UK runs support groups.",
    avoid=("clean", "cleaning", "cleaner", "mould", "mold", "damp", "dirt", "dust", "smell",
           "smells", "clutter", "declutter", "clear out", "clearout", "skip",
           "landlord", "eviction", "evict", "fire", "fire safety", "hoover", "vacuum",
           "laundry", "pets", "cats", "dogs", "rats", "mice")))
_TEEN_SAID = re.compile(r"\b(?:teenager|teenagers|teenage)\b")

_ADULT_AGE = re.compile(r"\b(?:1[89]|[2-9]\d)\s*(?:year|yr)s?[\s-]*(?:old|young)\b")
_ADULT_NAMED = re.compile(
    r"\b(?:dad|mum|mom|father|mother|husband|wife|partner|boyfriend|girlfriend|friend|colleague|"
    r"coworker|boss|manager|nan|nana|granny|grandad|granddad|grandma|grandpa|brother|sister|"
    r"flatmate|housemate|aunt|uncle|adult|grown up|grown-up)\b")


def _a_younger_child(understood):
    said = " ".join(str((understood or {}).get("clean") or "").lower().split())
    if _TEEN_SAID.search(said) or _ADULT_AGE.search(said):
        return False
    return not _ADULT_NAMED.search(said)


ENTRIES.append(entry(
    "child-always-tired",
    (("child", "children", "kid", "kids", "son", "daughter", "boy", "girl", "teenager", "teen",
      "toddler", "year old", "year-old", "school age", "my 6 year old", "my 7 year old"),
     ("always tired", "so tired", "tired all the time", "tired constantly", "no energy",
      "lacks energy", "exhausted", "knackered", "worn out", "lethargic", "sleepy",
      "falls asleep", "sleeps a lot", "sleeping a lot", "wants to sleep", "never has energy",
      "cant keep up", "cant wake", "wont get up", "struggles to get up",
      "all the time", "always exhausted", "always so tired", "tired all day")),
    "Count the sleep first, because most of it is that: a 5 to 11 year old needs 9 to 11 hours a "
    "night, a teenager 8 to 10, and school start times steal it. Then look for the other three - "
    "snoring or breathing pauses in the night, a diet short of iron (iron deficiency is the "
    "commonest cause of a tired child), and enough to drink. A child who has been tired for more "
    "than a month, or who is pale, breathless, losing weight or not growing, should have a blood "
    "test, so book the GP and ask for iron and vitamin D.",
    guard=_a_younger_child,
    avoid=("tired of", "my partner", "my husband",
           "my wife", "baby", "newborn", "months old", "cot", "crib", "wont sleep", "not sleeping",
           "sleep training", "burnout", "burnt out", "at work", "puppy", "dog", "cat"),
    bias=1))

ENTRIES.append(entry(
    "episiotomy",
    (("episiotomy", "episiotomies", "episiotomy cut", "cut during birth", "cut during labour",
      "cut in labour", "cut when giving birth", "stitches after birth", "tear or a cut"),
     ("what is", "whats", "what are", "mean", "means", "why", "do i need", "will i need",
      "heal", "healing", "recover", "recovery", "hurt", "pain", "sore", "stitches", "cut",
      "birth", "labour", "giving birth", "better", "weeks")),
    "An episiotomy is a cut a midwife or doctor makes at the opening of the vagina during birth, "
    "under local anaesthetic, to make room for the baby when it is needed quickly or the tissue is "
    "about to tear badly. It is not routine - most births do not need one - and a natural tear is "
    "usually preferred where there is time. The cut is stitched, the stitches dissolve, and it is "
    "sore for a week or two: keep it clean and dry, change pads often, and take the painkillers "
    "you would take for a headache. Ring the maternity unit if the pain gets worse rather than "
    "better, if it smells, or if you cannot pass urine.",
    avoid=("caesarean", "c-section", "c section", "induction", "induced", "forceps", "ventouse",
           "epidural", "gas and air", "home birth", "water birth", "second degree", "third degree",
           "fourth degree", "perineal tear", "tore", "tearing"),
    bias=1))

ENTRIES.append(entry(
    "doula",
    (("doula", "doulas", "birth doula", "postnatal doula", "birth partner for hire",
      "birth companion"),
     ("what is", "whats", "what does", "do i need", "worth", "cost", "how much", "hire",
      "hiring", "difference", "vs", "instead of", "help", "role", "find", "book")),
    "A doula is a trained companion who supports you through pregnancy, birth or the first weeks "
    "at home: she stays with you, helps you understand what is happening and what your choices "
    "are, and looks after the practical side. She is not a midwife and does no medical care - no "
    "examinations, no monitoring, no advice on the baby's health - so she is there alongside the "
    "midwife, not instead of her. Most charge a few hundred to about a thousand pounds for a "
    "birth, and finding one early matters, because good ones book up.",
    avoid=("midwife", "midwives", "health visitor", "nanny", "childminder", "babysitter",
           "au pair", "nursery", "antenatal class", "hypnobirthing"),
    bias=1))

_BLEEDING = ("bleed", "bleeds", "bled", "bleeding", "blood", "spotting", "spot", "spots",
             "spots of blood", "brown discharge", "pink discharge")

ENTRIES.append(entry(
    "bleeding-between-periods",
    (_BLEEDING,
     ("between periods", "between my periods", "between period", "mid cycle", "midcycle",
      "middle of my cycle", "after my period", "after a period", "before my period",
      "halfway through my cycle", "two weeks after my period", "in between periods",
      "between the periods")),
    "Spotting between periods is usually one of four things: the small hormone dip at ovulation, "
    "about 14 days before the next period; the pill, implant or coil, especially in the first "
    "three months; a harmless growth on the cervix or a patch of it that bleeds easily; or an "
    "infection, chlamydia among them. Note the days it happens for two or three cycles, take a "
    "sexual health test if you have changed partners, and see a GP if it keeps happening. Ring "
    "the GP the same week if you are soaking a pad an hour, it hurts, or it is after sex.",
    avoid=("pregnant", "pregnancy", "miscarriage", "after birth", "postpartum", "menopause",
           "menstrual cup", "period pants", "pad", "tampon", "heavy periods", "nappy", "dog",
           "cat", "urine", "poo", "nose", "gums"),
    bias=2))

ENTRIES.append(entry(
    "bleeding-after-sex",
    (_BLEEDING,
     ("after sex", "during sex", "after intercourse", "during intercourse", "after penetrat",
      "when i have sex", "after we have sex", "after being intimate")),
    "Bleeding after sex is common and usually not serious: dryness or thinning skin after the "
    "menopause, a patch on the cervix or a small polyp, or an infection. It is worth a GP "
    "appointment rather than a wait-and-see - they can look at the cervix and check your smear "
    "is up to date - and it is not something to be embarrassed about, they see it every week. "
    "Ring the same week if it is heavy, painful, or there is discharge that smells.",
    avoid=("menopause", "pregnant", "pregnancy", "after birth", "postpartum", "dog", "cat",
           "urine", "poo", "nose", "gums", "mouth", "gum", "first time", "hymen"),
    bias=4))

ENTRIES.append(entry(
    "bleeding-in-early-pregnancy",
    (_BLEEDING,
     ("pregnant", "pregnancy", "weeks pregnant", "early pregnancy", "expecting", "positive test",
      "im pregnant", "i am pregnant", "6 weeks", "7 weeks", "8 weeks", "9 weeks", "10 weeks",
      "11 weeks", "12 weeks")),
    "Ring your GP or the early pregnancy unit today for any bleeding in pregnancy - not because "
    "the worst is likely, but because they can check you and it is the same day's job. Bleeding "
    "is common in early pregnancy and most people who have it go on to have a healthy baby. Ring "
    "999 or 911 if it is heavy with clots, the pain is bad or on one side, you feel dizzy or "
    "faint, or you have pain at the tip of a shoulder - that needs looking at at once.",
    avoid=("after birth", "postpartum", "lochia", "miscarriage", "after a miscarriage",
           "menopause", "implant", "nappy", "dog", "cat", "nose", "gums", "urine", "poo"),
    bias=2))

ENTRIES.append(entry(
    "bleeding-after-a-miscarriage",
    (_BLEEDING,
     ("miscarriage", "lost the baby", "lost my baby", "ectopic", "missed miscarriage",
      "chemical pregnancy")),
    "Expect bleeding like a heavy period for up to two weeks after a miscarriage, sometimes "
    "on and off for three, with cramps that ease over a few days: use pads, and take paracetamol "
    "and ibuprofen as the packets say. Ring the ward or your GP the same day if you soak a pad "
    "in an hour, pass clots bigger than a 50p coin, feel feverish, or the discharge smells - "
    "that can mean tissue is left behind. A pregnancy test at three weeks should be negative; "
    "if it is not, ask to be seen.",
    avoid=("my baby", "newborn", "weeks old", "after birth", "postpartum", "lochia", "dog",
           "cat", "nappy", "nose", "gums", "urine", "poo", "how do i", "what causes",
           "why do miscarriages", "prevent"),
    bias=2))

ENTRIES.append(entry(
    "bleeding-after-the-menopause",
    (_BLEEDING,
     ("menopause", "menopausal", "since my last period", "years since my period",
      "no period for", "havent had a period", "stopped having periods", "post menopausal",
      "postmenopausal")),
    "Any bleeding after the menopause needs to be looked at, and the GP will refer you within "
    "two weeks for a scan of the womb lining - that is the routine for every woman with it, not "
    "a sign that anything is wrong. The usual causes are a dry, thin lining, a polyp or hormone "
    "tablets, and most turn out to be harmless. Ring and say the words 'bleeding after the "
    "menopause' so you get the right appointment, and go the same day if it is heavy or you feel "
    "unwell.",
    avoid=("hot flushes", "hot flush", "night sweats", "hrt", "mood", "sleep", "hair",
           "dog", "cat", "nappy", "nose", "gums", "urine", "poo", "my mum", "my wife"),
    bias=2))
CHILD = ("my son", "my sons", "my daughter", "my daughters", "my child", "my children",
         "my kid", "my kids", "my lad", "my lass", "my boy", "my girl", "my little one",
         "my eldest", "my youngest", "my stepson", "my stepdaughter", "my teenager",
         "my teen", "my toddler", "toddler", "child", "children", "kid", "kids", "school",
         "schools", "nursery", "year old", "year old son", "year old daughter",
         "years old", "teenager", "teen")

CHILD_HEADACHE_ASK = ("headache", "headaches", "head ache", "head aches", "head hurts",
                      "head is sore", "head pain", "head is banging", "banging head",
                      "bad head", "sore head", "migraine", "migraines")

CHILD_HEADACHE_RECUR = ("every day", "every single day", "most days", "daily", "all the time",
                        "each day",
                        "every week", "a few times a week", "twice a week", "three times a week",
                        "keeps coming back", "keep coming back", "wont go away", "won't go away",
                        "for 3 days", "for three days", "for 4 days", "for four days",
                        "for 2 days", "for two days", "for 5 days", "for five days",
                        "a few days", "several days", "a week now", "for a week",
                        "3 days now", "three days now")

ENTRIES.append(entry(
    "child-headache-that-keeps-coming-back",
    (CHILD_HEADACHE_ASK, CHILD),
    "A child who gets them most days is usually one of five things: not enough to drink, a missed "
    "meal, too little sleep, a long stretch on a screen, or eyes that need testing. Write down "
    "the time of day each one comes on and what they had eaten and drunk - that diary is what a "
    "GP asks for first. Never aspirin under sixteen. See a GP about a run like this, and ring 999 "
    "for a stiff neck, a rash that does not fade under a glass, or drowsiness.",
    ask=CHILD_HEADACHE_RECUR,
    avoid=("my wife", "my husband", "my mum", "my mother", "my dad", "my father", "im pregnant",
           "i'm pregnant", "pregnant", "my period", "hormone", "hangover", "drunk", "office",
           "desk", "my boss", "shift work", "covid", "flu", "temperature and a stiff neck",
           "meningitis", "rash", "diarrhoea", "vomiting bug", "sickness bug", "chickenpox",
           "measles", "earache", "ear ache", "toothache", "tooth ache", "sore throat",
           "being sick", "is sick", "was sick", "throwing up", "vomiting", "stiff neck",
           "banged his head", "banged her head", "bang on the head", "fell and hit"),
    bias=5))



_NAMED_CONDITION_AVOID = (
    "dog", "dogs", "puppy", "cat", "cats", "kitten", "rabbit", "hamster", "guinea pig", "horse",
    "pet", "pets", "vet", "baby", "babies", "newborn", "toddler", "my son", "my son's",
    "my daughter", "my child", "my kid", "my mum", "my dad", "my wife", "my husband",
    "my partner", "my friend", "my nan", "my gran",
    "dose", "dosage", "how many", "mg", "overdose", "side effect", "side effects",
    "withdrawal", "addicted", "addiction")

def _hernia(memory, understood):
    line = " " + str((understood or {}).get("clean") or "").lower() + " "
    if "hiatus" in line:
        return (
            "A hiatus hernia is the top of the stomach sliding up through the hole in the diaphragm "
            "that the food pipe comes through, so part of it sits above the muscle that keeps acid "
            "down. It is very common and it is not dangerous in itself: what it causes is heartburn "
            "and reflux, worse lying flat, bending or after a big meal. Smaller meals, nothing to "
            "eat for three hours before bed, the head of the bed up on a couple of books, and losing "
            "weight round the middle all help, and a GP can add a tablet that turns the acid down "
            "if those are not enough. An operation is only for the few people whose reflux still "
            "damages the food pipe on treatment. Trouble swallowing, food sticking, vomiting or "
            "weight loss without trying are the reasons to be seen quickly rather than treated at "
            "home.")
    return _A_HERNIA


_A_HERNIA = (
    "A hernia is a piece of bowel or fat pushing out through a weak spot in the wall of muscle "
    "that is meant to hold it in - commonest in the groin, where the wall is thin already, and "
    "then at the belly button or along an old operation scar. It shows as a soft lump that is "
    "there when you stand and cough and gone when you lie down, and it is usually a dull ache "
    "rather than a pain. It will not mend itself, and it does not need a repair unless it is "
    "bothering you, but it does need to be looked at by a GP so the diagnosis is on your record. "
    "A hiatus hernia is different: the top of the stomach slides up through the diaphragm into "
    "the chest, which causes heartburn and is treated with the reflux advice and a tablet rather "
    "than an operation. Go to A&E the same day if a lump that used to go back in becomes hard and "
    "very tender, or comes with vomiting, a swollen belly or no wind - that is a hernia that has "
    "been trapped, and it needs a surgeon rather than a wait.")


ENTRIES.append(entry(
    "hernia",
    (("hernia", "hernias", "inguinal hernia", "hiatus hernia", "femoral hernia",
      "umbilical hernia", "incisional hernia", "strangulated hernia", "rupture"),
     ("what", "whats", "what's", "is", "mean", "means", "explain", "tell", "about", "cause",
      "causes", "why", "treatment", "operation", "surgery", "repair", "fix", "help", "symptoms",
      "signs", "serious", "dangerous", "can it", "does it", "do i need", "do i have",
      "have i got", "how do i know", "lump in my groin", "lump in my stomach")),
    _hernia,
    explain=True,
    report=True,
    bias=2,
    avoid=_NAMED_CONDITION_AVOID + (
        "pulled", "pulled muscle", "strain", "strained", "back pain", "slipped disc",
        "heartburn", "reflux", "indigestion", "acid", "lump in my breast", "lump in my neck",
        "lump in my armpit", "testicle", "testicles", "testicular", "spot", "cyst")))
