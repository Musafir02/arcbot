import re

from .lookup import entry

ANSWERS = ("travel", "health")

_JABS = (
    "jab", "jabs", "vaccination", "vaccinations", "vaccinate", "vaccinated", "vaccine",
    "vaccines", "immunisation", "immunisations", "immunization", "immunizations",
    "travel jabs", "travel vaccines", "travel clinic", "yellow fever", "typhoid", "hepatitis a",
    "hepatitis", "rabies", "cholera", "japanese encephalitis", "tetanus",
    "malaria", "malaria tablets", "malaria pills", "antimalarial", "antimalarials",
)

_JABS_ASK = (
    "need", "needed", "needs", "required", "recommended", "do i need", "will i need",
    "which", "what", "before i go", "before we go", "before we travel", "get", "have",
    "should i get", "should i have", "worth getting", "certificate",
)

_MEDICINES = (
    "medication", "medications", "medicine", "medicines", "prescription", "prescriptions",
    "tablet", "tablets", "pills", "insulin", "epipen", "epi pen", "inhaler", "injections",
    "injection", "drugs", "medical supplies",
    "antibiotics", "antibiotic", "standby antibiotics", "antimalarials",
)

_MEDICINES_ASK = (
    "take", "taking", "bring", "bringing", "carry", "carrying", "pack", "packing",
    "hand luggage", "carry on", "allowed", "legal", "abroad", "away", "travelling", "traveling",
    "travel", "flight", "flying", "fly", "airport", "customs",
)

_PLACES = (
    "spain", "france", "italy", "greece", "portugal", "turkey", "cyprus", "malta", "croatia",
    "canaries", "canary islands", "mallorca", "majorca", "ibiza", "tenerife", "lanzarote",
    "sicily", "sardinia", "corsica", "germany", "austria", "switzerland", "holland",
    "netherlands", "belgium", "ireland", "poland", "czech republic", "prague", "hungary",
    "budapest", "slovenia", "slovakia", "romania", "bulgaria", "serbia", "albania",
    "montenegro", "bosnia", "estonia", "latvia", "lithuania", "finland", "sweden", "norway",
    "denmark", "iceland", "morocco", "tunisia", "egypt", "cape verde", "gambia", "senegal",
    "ghana", "nigeria", "kenya", "tanzania", "zanzibar", "ethiopia", "uganda", "rwanda",
    "south africa", "cape town", "johannesburg", "namibia", "botswana", "zimbabwe", "zambia",
    "madagascar", "mauritius", "seychelles", "dubai", "abu dhabi", "uae", "emirates", "qatar",
    "oman", "jordan", "israel", "lebanon", "saudi arabia", "india", "goa", "kerala", "rajasthan",
    "delhi", "mumbai", "pakistan", "bangladesh", "nepal", "bhutan", "sri lanka", "maldives",
    "thailand", "bangkok", "phuket", "vietnam", "cambodia", "laos", "myanmar", "burma",
    "malaysia", "singapore", "indonesia", "bali", "java", "philippines", "manila", "china",
    "beijing", "shanghai", "hong kong", "japan", "tokyo", "kyoto", "south korea", "seoul",
    "taiwan", "mongolia", "kazakhstan", "uzbekistan", "australia", "sydney", "melbourne",
    "new zealand", "auckland", "fiji", "samoa", "tahiti", "usa", "america", "the states",
    "new york", "florida", "california", "las vegas", "hawaii", "alaska", "canada", "toronto",
    "vancouver", "mexico", "cancun", "cuba", "havana", "jamaica", "barbados", "trinidad",
    "dominican republic", "puerto rico", "bahamas", "antigua", "st lucia", "grenada",
    "guatemala", "belize", "honduras", "costa rica", "panama", "nicaragua", "colombia",
    "ecuador", "galapagos", "peru", "machu picchu", "bolivia", "chile", "argentina",
    "buenos aires", "brazil", "rio", "uruguay", "paraguay", "venezuela", "guyana", "suriname",
)

_ROUTINE = (
    "spain", "france", "italy", "greece", "portugal", "cyprus", "malta", "croatia", "canaries",
    "canary islands", "mallorca", "majorca", "menorca", "ibiza", "tenerife", "lanzarote",
    "fuerteventura", "gran canaria", "sicily", "sardinia", "corsica", "germany", "austria",
    "switzerland", "holland", "netherlands", "belgium", "ireland", "poland", "czech republic",
    "prague", "hungary", "budapest", "slovenia", "slovakia", "romania", "bulgaria", "estonia",
    "latvia", "lithuania", "finland", "sweden", "norway", "denmark", "iceland", "andorra",
    "monaco", "luxembourg", "liechtenstein", "gibraltar", "jersey", "guernsey", "isle of man",
)

_YELLOW_FEVER = (
    "ghana", "nigeria", "senegal", "gambia", "kenya", "tanzania", "zanzibar", "ethiopia",
    "uganda", "rwanda", "zambia", "zimbabwe", "botswana", "namibia", "madagascar", "brazil",
    "peru", "colombia", "ecuador", "bolivia", "venezuela", "guyana", "suriname", "panama",
    "trinidad", "costa rica",
)

_MALARIA = (
    "ghana", "nigeria", "senegal", "gambia", "kenya", "tanzania", "zanzibar", "ethiopia",
    "uganda", "rwanda", "zambia", "zimbabwe", "botswana", "namibia", "madagascar", "malawi",
    "india", "goa", "kerala", "rajasthan", "delhi", "mumbai", "pakistan", "bangladesh", "nepal",
    "sri lanka", "thailand", "bangkok", "phuket", "vietnam", "cambodia", "laos", "myanmar",
    "burma", "malaysia", "indonesia", "bali", "java", "philippines", "manila", "brazil", "peru",
    "colombia", "ecuador", "bolivia", "venezuela", "guyana", "suriname", "panama", "honduras",
    "guatemala", "belize", "nicaragua",
)

_ROUTINE_PLACE = re.compile(
    r"(?<![a-z])(%s)(?![a-z])" % "|".join(re.escape(place) for place in
                                          sorted(_ROUTINE, key=len, reverse=True)), re.I)

_AWAY = re.compile(r"(?<![a-z])(?:abroad|overseas|travel|travels|travelling|traveling|"
                   r"travelled|traveled|trip|trips|holiday|"
                   r"holidays|vacation|flying|fly|flight|flights|airport|goa|going away|"
                   r"going to|backpacking|honeymoon)(?![a-z])", re.I)
_PLACE = re.compile(r"(?<![a-z])(%s)(?![a-z])" % "|".join(re.escape(place) for place in
                                                         sorted(_PLACES, key=len, reverse=True)),
                    re.I)


_ANIMAL = re.compile(r"(?<![a-z])(?:dog|dogs|puppy|puppies|cat|cats|kitten|kittens|pet|pets|"
                     r"horse|horses|pony|rabbit|hamster|parrot|ferret|tortoise)(?![a-z])", re.I)


_NOT_A_TRIP = re.compile(
    r"(?<![a-z])(?:baby|babies|infant|infants|newborn|toddler|toddlers|child|children|kid|kids|"
    r"son|daughter|mum|dad|mother|father|pregnant|pregnancy|expecting|school|nursery|nurse|"
    r"tetanus|cut|cuts|wound|wounds|scratch|scratched|bite|bitten|flu|shingles|hpv|mmr|"
    r"measles|mumps|rubella|whooping|childminder|side effects|side effect|reaction|sore arm|"
    r"antibody|antibodies|immune)(?![a-z])", re.I)


_A_BARE_NEED = re.compile(
    r"\b(?:do|will|would|should|could) (?:i|we) (?:need|needs|have|get|be needing)\b|"
    r"\bwhat (?:jabs|vaccinations|vaccines|injections|immunisations) (?:do|will|would|should) "
    r"(?:i|we)\b|\bwhich (?:jabs|vaccinations|vaccines|injections)\b", re.I)


def _a_trip_is_named(understood):
    text = str(understood.get("clean") or "")
    if _ANIMAL.search(text):
        return False
    if _PLACE.search(text) or _AWAY.search(text):
        return True
    return bool(_A_BARE_NEED.search(text)) and not _NOT_A_TRIP.search(text)


_A_TRAVEL_CLINIC = (
    "Book a travel clinic or a pharmacy that does travel jabs four to six weeks before you fly: "
    "some courses are two or three doses a month apart, and most of them take a fortnight to "
    "work."
)

_THE_REST_OF_THE_LIST = (
    "Thailand and most of Asia, Africa and South America want hepatitis A and typhoid for almost "
    "any trip. Yellow fever is a certificate some countries in Africa and South America ask for "
    "on arrival, and malaria tablets are a separate decision about the risk in the area you are "
    "actually staying in. Check the country on the NHS Fit for Travel or the GOV.UK travel advice "
    "pages - that is the list that counts - and keep the record card with your passport."
)

_CHECK_IT = ("Check %s on the NHS Fit for Travel page - that is the list that counts - and keep "
             "the record card with your passport.")

_WHEN_TO_BOOK_BARE = ("Book it four to six weeks before you fly, because some courses are two or "
                      "three doses a month apart.")

_OTHER_ONES = "The other ones for %s are hepatitis A and typhoid."

_YELLOW_SENTENCE = ("Yellow fever is the one to ask about for %s: the vaccine is for the risk "
                    "areas, and the certificate is what a border asks for when you arrive from "
                    "one, so the clinic needs your route and not only the country.")

_MALARIA_SENTENCE = ("Malaria tablets for %s are a separate decision again - they depend on the "
                     "area and the season you are going in.")

_MALARIA_ASKED = re.compile(r"(?<![a-z])(?:malaria|antimalarial|antimalarials)(?![a-z])", re.I)
_YELLOW_ASKED = re.compile(r"(?<![a-z])(?:yellow fever|certificate)(?![a-z])", re.I)


def _place_named(text):
    for pattern in (_ROUTINE_PLACE, _PLACE):
        there = pattern.search(text)
        if there:
            return there.group(1).strip().lower()
    return None


def _the_jabs_reply(memory, understood):
    text = str(understood.get("clean") or "")
    place = _place_named(text)
    if not place:
        return "%s %s" % (_A_TRAVEL_CLINIC, _THE_REST_OF_THE_LIST)
    name = place.title()
    if place in _ROUTINE:
        return ("Nothing beyond the routine jabs for %s - no travel clinic needed unless you are "
                "staying somewhere unusual or going on somewhere else. Make sure the routine "
                "ones are up to date (MMR, tetanus, polio), and check %s on the NHS Fit for "
                "Travel page if you want it in writing." % (name, name))
    malaria = place in _MALARIA
    yellow = place in _YELLOW_FEVER
    asks_malaria = malaria and _MALARIA_ASKED.search(text)
    asks_yellow = yellow and _YELLOW_ASKED.search(text)
    said = []
    if asks_malaria:
        said.append("Malaria tablets are the decision for %s, and it is the area and the season "
                    "that decide them, so take the clinic's advice for exactly where you are "
                    "staying." % name)
        said.append(_WHEN_TO_BOOK_BARE)
        said.append(_OTHER_ONES % name)
        if yellow:
            said.append(_YELLOW_SENTENCE % name)
    elif asks_yellow:
        said.append("%s is in the yellow fever area: the vaccine is for the areas with risk, and "
                    "the certificate is what a border asks for when you arrive from one, so the "
                    "clinic needs your route and not only the country." % name)
        said.append(_WHEN_TO_BOOK_BARE)
        said.append(_OTHER_ONES % name)
        if malaria:
            said.append(_MALARIA_SENTENCE % name)
    else:
        said.append("Plan on hepatitis A and typhoid for %s, and book a travel clinic or a "
                    "pharmacy that does travel jabs four to six weeks before you fly: some "
                    "courses are two or three doses a month apart, and most of them take a "
                    "fortnight to work." % name)
        if yellow:
            said.append(_YELLOW_SENTENCE % name)
        if malaria:
            said.append(_MALARIA_SENTENCE % name)
    said.append(_CHECK_IT % name)
    return " ".join(said)

_MEDICINES_REPLY = (
    "Carry it in your hand luggage rather than the hold, in the original box with the pharmacy "
    "label showing your name and the dose, and take a few more days' worth than the trip lasts. "
    "A repeat prescription printout or a short letter from the GP answers the customs question "
    "without an argument. Ordinary medicines are fine almost everywhere; anything controlled - "
    "codeine, strong painkillers, sleeping tablets, ADHD medicines - is worth checking with the "
    "embassy of the country before you fly, and a few want a certificate in advance. Insulin and "
    "anything that needs the cold goes in hand luggage too, in a cool bag and never against ice. "
    "Antibiotics are worth asking the GP about before you go rather than buying out there - some "
    "destinations get a standby course for a stomach bug, and it is a prescription, not a "
    "souvenir."
)

ENTRIES = [entry(
    "travel-jabs",
    (_JABS, _JABS_ASK),
    _the_jabs_reply,
    bias=2,
    guard=_a_trip_is_named)]

ENTRIES.append(entry(
    "medication-abroad",
    (_MEDICINES, _MEDICINES_ASK),
    _MEDICINES_REPLY,
    guard=_a_trip_is_named,
    avoid=("with my", "together", "mixing", "mix them", "side effect", "side effects",
           "alcohol", "pregnant", "breastfeeding", "overdose", "my baby", "my child",
           "my son", "my daughter")))
