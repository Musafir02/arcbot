from ..memory import last_user
from .lookup import entry

ANSWERS = ("health",)

_COUNTER = (
    "over the counter", "over-the-counter", "otc", "from the chemist", "at the chemist",
    "chemist", "from a pharmacy", "at the pharmacy", "from the pharmacy", "pharmacy",
    "pharmacist", "off the shelf", "without a prescription", "no prescription",
    "need a prescription", "prescription for", "on prescription", "ask the chemist",
    "ask a pharmacist", "ask the pharmacist", "from boots", "from superdrug", "shelf",
    "tablet for", "tablets for", "pill for", "pills for", "something for it", "anything for it",
    "medicine for", "medication for", "anything that will", "something that will",
)
_ASKING_FOR_IT = (
    "can i", "could i", "what can i", "what should i", "should i", "is there", "are there",
    "is it ok", "is it safe", "anything", "something", "what is the best", "whats the best",
    "which", "do i need", "will i need", "do you need", "buy", "get", "take", "try", "help",
    "work", "works", "recommend", "how much", "price", "cost", "costs", "more", "another",
    "best", "should", "will",
)

_ITS_A_HEADACHE = ("headache", "headaches", "migraine", "migraines", "head ache", "head hurts",
                   "sore head")
_ITS_A_BACK = ("back pain", "my back", "lower back", "sciatica", "slipped disc", "backache",
               "back ache", "back is", "back has been")
_ITS_PERIOD_PAIN = ("period pain", "period pains", "cramps", "period cramps", "menstrual",
                    "period is", "periods are", "heavy period", "pmt")
_ITS_A_SORE_THROAT = ("sore throat", "throat is sore", "throat hurts", "throat", "tonsils",
                      "tonsillitis", "scratchy throat", "swallowing hurts")
_ITS_A_COUGH = ("cough", "coughs", "coughing", "chesty", "dry cough", "barking")
_ITS_A_COLD = ("cold", "colds", "blocked nose", "stuffy nose", "runny nose", "sniffles",
               "congested", "congestion", "flu", "sinusitis", "sinus")
_ITS_HAY_FEVER = ("hay fever", "hayfever", "allergy", "allergies", "allergic", "pollen",
                  "sneezing", "itchy eyes", "watery eyes")
_ITS_HEARTBURN = ("heartburn", "indigestion", "acid reflux", "reflux", "acid", "gerd")
_ITS_DIARRHOEA = ("diarrhoea", "diarrhea", "the runs", "loose stools", "dioralyte",
                  "stomach bug", "sick bug", "food poisoning")
_ITS_CONSTIPATION = ("constipation", "constipated", "cannot poo", "cant poo", "hard stools",
                     "laxative", "laxatives")
_ITS_THRUSH = ("thrush", "yeast infection", "candida", "itchy down there", "white discharge")
_ITS_VERTIGO = ("vertigo", "dizzy", "dizziness", "spinning", "light headed", "lightheaded",
                "bppv")
_ITS_A_SLEEP_AID = ("sleep aid", "sleeping tablet", "sleeping tablets", "cant sleep",
                    "cannot sleep", "insomnia", "sleeping pill", "sleeping pills",
                    "help me sleep")
_ITS_CYSTITIS = ("cystitis", "uti", "urine infection", "urinary infection", "when i pee",
                 "when i wee", "stings", "stinging", "burning when i", "water infection")
_ITS_AN_EARACHE = ("earache", "ear ache", "ear infection", "ear is", "ear hurts", "sore ear")

_HEADACHE_CARD = (
    "Paracetamol or ibuprofen is what the counter has for a headache: take the dose on the pack "
    "with water and something to eat, and one painkiller at a time to start. Taken more than a "
    "couple of days a week for months, either can cause headaches of its own. A headache that "
    "came on in seconds, is the worst you have ever had, or comes with a fever and a stiff neck, "
    "weakness, confusion or a change in vision is a 999 call, not a tablet.")
_BACK_CARD = (
    "Ibuprofen is what a pharmacist will suggest for a strained back, with paracetamol alongside "
    "if you need it, and a heat pad; keep moving, because rest makes it stiffer. Say yes to their "
    "questions about your stomach, kidneys, heart and blood thinners, as ibuprofen is not for "
    "everyone. Numbness between your legs, a weak leg, or trouble passing water is a same-day GP "
    "appointment.")
_PERIOD_CARD = (
    "Ibuprofen works better than paracetamol for period pain, and starting it the day before "
    "helps; the pharmacist can add codeine (co-codamol) or suggest mefenamic acid if that is not "
    "enough. A heat pad and moving about ease it too. Pain that stops you living normally, or "
    "bleeding that soaks a pad an hour, is worth a GP appointment.")
_THROAT_CARD = (
    "Paracetamol or ibuprofen, plus a medicated lozenge, is what the counter has for a sore "
    "throat, and most settle within a week without anything else. Ask about a spray with a "
    "local anaesthetic if swallowing is the worst part. See a GP if you cannot swallow fluids, "
    "cannot open your mouth wide, or it lasts more than two weeks.")
_COUGH_CARD = (
    "For a cough the pharmacist has honey-based syrups and simple linctus; the evidence for "
    "cough medicines is weak, and honey in warm water does about as well, with paracetamol or "
    "ibuprofen for the aches. Ask about a cough medicine for a night cough only - a chesty one is "
    "better left to clear. A cough with breathlessness, blood, chest pain, a fever that will not "
    "go, or more than three weeks needs a doctor.")
_COLD_CARD = (
    "Nothing cures a cold, so the counter is for the symptoms: paracetamol or ibuprofen for aches "
    "and fever, a decongestant spray or tablet for a blocked nose, and honey for the cough. "
    "Decongestant tablets are not for you if you have high blood pressure, heart trouble or take "
    "an MAOI, so say so at the counter. Most clear in a week to ten days; a cold getting worse "
    "after a week, or a fever with breathlessness, needs a GP.")
_HAY_FEVER_CARD = (
    "A once-a-day antihistamine - loratadine, cetirizine or the pharmacy's own brand, which is "
    "the same tablet for less - is the first thing to try for hay fever, and a steroid nose spray "
    "or eye drops can be added if the nose and eyes are where it is. The spray works best started "
    "a week or two before your season. Wheezing or a tight chest with it is a GP question.")
_HEARTBURN_CARD = (
    "An antacid or an alginate (Gaviscon and the like) settles heartburn in minutes, and a "
    "14-day course of a tablet such as omeprazole is the next step if it keeps coming back - the "
    "pharmacist can suggest both. Losing a little weight, smaller meals and nothing to eat in the "
    "three hours before bed do the rest. Trouble swallowing, weight loss or pain on swallowing is "
    "a GP appointment rather than a repeat bottle.")
_DIARRHOEA_CARD = (
    "The counter has oral rehydration sachets (Dioralyte) and, if you have to travel, loperamide; "
    "the fluid is the part that matters, and most of it settles in two to three days. Keep eating "
    "plain food and stay off dairy and alcohol until it does. Blood in it, a high fever, or not "
    "keeping any water down needs a GP - and 111 if you are frail, pregnant or very young.")
_CONSTIPATION_CARD = (
    "Start with a bulk-forming laxative such as ispaghula (Fybogel) or a stool softener, with "
    "more water and fibre, and give it a few days - the pharmacist can add a short course of a "
    "stimulant laxative if nothing has moved. Ask before using them regularly, as the bowels get "
    "used to it. Constipation that comes with bleeding, weight loss, or a change that lasts weeks "
    "is worth a GP look.")
_THRUSH_CARD = (
    "Thrush is an itch and a thick white discharge, and a pharmacist can treat it without a "
    "prescription: a clotrimazole pessary or cream, or a "
    "single fluconazole tablet if you are not pregnant and not on certain medicines - say what "
    "else you take. The itch eases within a few days, and the whole course still needs finishing. "
    "See a GP if it is the first time you have had it, it keeps returning, or there is bleeding, "
    "pain or a smelly discharge. Cotton rather than lace, nothing perfumed down there, and no "
    "douching, is what stops it coming back.")
_VERTIGO_CARD = (
    "For the common spinning kind, the fix is the Epley manoeuvre rather than a tablet - a GP or "
    "physio can do it in one visit and you can learn it - while the counter can give "
    "prochlorperazine (Stemetil) for a few days to soften the spinning. It makes you drowsy, so "
    "no driving on it. Vertigo with double vision, slurred speech, weakness down one side, or a "
    "sudden bad headache is a 999 call.")
_SLEEP_CARD = (
    "The counter has a short course of a sedating antihistamine (diphenhydramine, promethazine) "
    "for a few nights, and melatonin on prescription or from a pharmacist in some places; all of "
    "them leave you groggy and none is a long-term answer. The routine does more: the same "
    "wake-up time, no screens or caffeine late, and a cool dark room. Ask before mixing any of it "
    "with alcohol, antidepressants or other sedatives; weeks of broken sleep is a GP "
    "conversation.")
_CYSTITIS_CARD = (
    "A pharmacist can treat a simple bladder infection in women aged 16 to 64 with a short course "
    "of an antibiotic (trimethoprim or nitrofurantoin) - ask at the counter, as many pharmacies "
    "run the scheme. Drink plenty and take paracetamol for the burn. Blood in the urine, a fever, "
    "pain in your back or side, being pregnant, or being a man with these symptoms means a GP the "
    "same day.")
_EARACHE_CARD = (
    "Paracetamol or ibuprofen is the counter's answer for earache, and most in adults settle in a "
    "few days as the cold behind it clears; ask about drops only if the ear itself is itchy or "
    "weeping, as drops do not help a middle-ear infection. Nothing down the ear canal, no cotton "
    "buds. Discharge, a high fever, or a child under two with earache is a GP appointment.")

_KINDS = (
    (_ITS_A_HEADACHE, _HEADACHE_CARD),
    (_ITS_A_BACK, _BACK_CARD),
    (_ITS_PERIOD_PAIN, _PERIOD_CARD),
    (_ITS_A_SORE_THROAT, _THROAT_CARD),
    (_ITS_A_COUGH, _COUGH_CARD),
    (_ITS_A_COLD, _COLD_CARD),
    (_ITS_HAY_FEVER, _HAY_FEVER_CARD),
    (_ITS_HEARTBURN, _HEARTBURN_CARD),
    (_ITS_DIARRHOEA, _DIARRHOEA_CARD),
    (_ITS_CONSTIPATION, _CONSTIPATION_CARD),
    (_ITS_THRUSH, _THRUSH_CARD),
    (_ITS_VERTIGO, _VERTIGO_CARD),
    (_ITS_A_SLEEP_AID, _SLEEP_CARD),
    (_ITS_CYSTITIS, _CYSTITIS_CARD),
    (_ITS_AN_EARACHE, _EARACHE_CARD),
)

_NOT_A_SYMPTOM = (
    "my dog", "my cat", "my puppy", "my kitten", "my rabbit", "my horse", "my pet", "my hamster",
    "the dog", "the cat", "cold tap", "cold water", "cold weather", "its cold", "it is cold",
    "freezing", "the fridge", "the freezer", "the heating", "the boiler", "cold sore",
    "cold call", "cold caller", "cold email", "in cold blood",
)


def _words_of(reading):
    if not isinstance(reading, dict):
        return ""
    said = [str(reading.get(part) or "") for part in ("text", "clean")]
    leans = reading.get("leans_on")
    if isinstance(leans, dict):
        said.extend(str(leans.get(part) or "") for part in ("text", "subject", "topic"))
    return " ".join(" ".join(said).split()).lower()


def _the_earlier(memory):
    earlier = last_user(memory) if memory is not None else ""
    return " ".join(str(earlier or "").split()).lower()


def _the_kind_in(said):
    if not said or any(word in said for word in _NOT_A_SYMPTOM):
        return None
    for words, card in _KINDS:
        if any(word in said for word in words):
            return card
    return None


def _the_kind(reading, memory=None):
    return _the_kind_in(_words_of(reading)) or _the_kind_in(_the_earlier(memory))


_OWN_BRAND_CARD = (
    "The own-brand box is the same medicine for less: match the active ingredient and the dose on "
    "the back, and a pharmacy's own hay fever or painkiller tablet is usually a fraction of the "
    "branded price. Ask the pharmacist to put the two boxes side by side if the names confuse - "
    "the licence number and the ingredient are the parts that must match, not the box. The one "
    "place it matters is a medicine you take for something serious, where the brand can change "
    "how much you absorb.")
_PRESCRIBED_CARD = (
    "It cannot be bought over the counter - a prescription-only medicine is not sold off the shelf "
    "whatever the box looks like - but ordering more is a different question, and most pharmacies "
    "will send the repeat request to the surgery for you and have it ready in two or three days. "
    "Ask at the counter, and order about a week before you run out. If the course did not work, "
    "say so when you order: the same thing again is often not what the doctor would choose.")
_PET_CARD = (
    "Nothing from the chemist - a pharmacy's shelves are dosed for people, and a dog or cat can be "
    "poisoned by what is ordinary for us (paracetamol and ibuprofen especially, and some "
    "decongestants). Ring the vet for anything that lasts more than a day or two, and keep every "
    "medicine you buy out of reach, child locks and all. The one thing a pharmacy can do is tell "
    "you what is poisonous, so keep the box to read out.")

_PRICE_WORDS = ("how much", "price", "prices", "cost", "costs", "cheaper", "cheapest", "own brand",
                "own-brand", "brand name", "branded", "much does", "much are", "much is")
_MEDICINE_THINGS = ("tablet", "tablets", "pill", "pills", "medicine", "medicines", "painkiller",
                    "painkillers", "antihistamine", "antihistamines", "syrup", "cream", "drops",
                    "sachets", "spray", "inhaler", "plasters")
_PETS = ("my dog", "my cat", "my puppy", "my kitten", "my rabbit", "my hamster", "my horse",
         "my budgie", "my parrot", "my guinea pig", "my pet", "the dog", "the cat", "our dog",
         "our cat", "the puppy", "the kitten")
_PRESCRIBED = ("antibiotic", "antibiotics", "prescription", "prescribed", "on repeat",
               "repeat prescription", "the tablets i was given", "what the doctor gave me",
               "inhaler", "insulin", "epipen", "epipens", "statins", "blood pressure tablets")


_IS_PREGNANT = ("pregnant", "pregnancy", "expecting a baby", "20 weeks", "12 weeks", "8 weeks",
                "six months pregnant", "breastfeeding", "nursing", "im feeding")
_IS_A_CHILD = ("my son", "my daughter", "my child", "my kid", "my baby", "my toddler",
               "my little one", "the kids", "my kids", "year old", "year-old", "months old",
               "my boy", "my girl", "my grandson", "my granddaughter", "my niece", "my nephew")

_PREGNANT_CARD = (
    "Paracetamol is the painkiller to take in pregnancy - the lowest dose that works, for the "
    "shortest time - and ibuprofen and aspirin are the ones to leave alone unless a doctor "
    "prescribes them, especially after 20 weeks. Ask the pharmacist to check any other box "
    "against the pregnancy, including cold and flu remedies, because several carry a second "
    "ingredient that is not advised; a headache that will not shift, or one that comes with "
    "swelling, blurred vision or pain under the ribs, is a same-day call to the midwife.")
_CHILD_CARD = (
    "For a child the pharmacist will weigh the dose by age, so ask for children's paracetamol or "
    "ibuprofen and give it by the spoon or syringe in the box, never a kitchen spoon. Honey helps "
    "a cough over the age of one, and cough and cold medicines are not licensed for children "
    "under six, so skip those. A baby under three months with a fever, or a child who is limp, "
    "breathing fast or not drinking, is a same-day doctor rather than the counter.")


def _a_person_the_shelf_treats_differently(said):
    if any(word in said for word in _IS_PREGNANT):
        return _PREGNANT_CARD
    if any(word in said for word in _IS_A_CHILD):
        return _CHILD_CARD
    return None


def _at_the_counter(memory, reading):
    said = _words_of(reading)
    earlier = _the_earlier(memory)
    if not said or _names_any(said + " " + earlier, _NOT_A_SYMPTOM):
        return None
    different = _a_person_the_shelf_treats_differently(said + " " + earlier)
    if different:
        return different
    return _the_kind_in(said) or _the_kind_in(earlier)


def _said(reading):
    return _words_of(reading)


def _names_any(said, words):
    return any(word in said for word in words)


def _the_own_brand(memory, reading):
    return _OWN_BRAND_CARD


_NOT_A_SHELF_PRICE = ("morning after", "morning-after", "emergency contraception", "plan b",
                      "levonelle", "ellaone", "ella one", "ulipristal", "contraception",
                      "contraceptive", "the coil", "copper coil", "iud", "implant", "condoms")


def _a_price_was_asked(understood):
    said = _said(understood)
    return (bool(said) and _names_any(said, _MEDICINE_THINGS)
            and not _names_any(said, _PRESCRIBED)
            and not _names_any(said, _NOT_A_SHELF_PRICE)
            and not _names_any(said, _PET_WORDS_FOR_AVOID))


_NOT_A_PRESCRIPTION = ("without a prescription", "without prescription", "no prescription",
                       "not on prescription", "dont need a prescription",
                       "don't need a prescription", "not prescribed")


def _the_prescribed_course(memory, reading):
    said = _words_of(reading) + " " + _the_earlier(memory)
    if not said or not _names_any(said, _PRESCRIBED):
        return None
    if _names_any(said, _NOT_A_PRESCRIPTION):
        return None
    return _PRESCRIBED_CARD


def _a_pet_at_the_counter(memory, reading):
    said = _words_of(reading) + " " + _the_earlier(memory)
    if not said.strip() or not _names_any(said, _PETS):
        return None
    return _PET_CARD


_PET_WORDS_FOR_AVOID = _PETS

ENTRIES = [entry(
    "at-the-counter",
    (_COUNTER, _ASKING_FOR_IT),
    _at_the_counter,
    bias=2,
    avoid=_NOT_A_SYMPTOM),
    entry(
    "a-pet-at-the-counter",
    (_COUNTER, _ASKING_FOR_IT),
    _a_pet_at_the_counter,
    bias=4),
    entry(
    "the-own-brand",
    (_PRICE_WORDS, _MEDICINE_THINGS),
    _the_own_brand,
    guard=_a_price_was_asked,
    bias=7),
    entry(
    "a-prescribed-course",
    (_COUNTER, ("more", "another", "again", "repeat", "top up", "buy one", "buy some", "buy it",
                "get one", "get some", "one", "some", "buy", "get", "take", "order")),
    _the_prescribed_course,
    bias=5),
]
