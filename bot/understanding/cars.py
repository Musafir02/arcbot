import re

CAR = re.compile(
    r"\b(?:car|cars|van|vans|mot|mot'd|garage|garages|mechanic|mechanics|tyre|tyres|tire|tires"
    r"|engine|gearbox|clutch|brakes|brake|exhaust|radiator|battery|alternator|starter"
    r"|windscreen|bonnet|suspension|shock|absorber|wheel|wheels|hub|bearing|bearing's"
    r"|jump\s?start|service|serviced|motoring"
    r"|audi|ford|vauxhall|toyota|honda|nissan|renault|peugeot|citroen|skoda|hyundai|kia|mazda"
    r"|volvo|suzuki|bmw|mercedes|volkswagen|vw|fiat|tesla|dacia|chevrolet|chrysler|dodge"
    r"|subaru|mitsubishi|lexus|saab|alfa|jeep|bentley|porsche|ferrari|lamborghini|aston|lada"
    r"|daewoo|infiniti|acura|punto|corsa|clio|astra|mondeo|passat|micra|yaris|fabia|octavia"
    r"|ibiza|qashqai|juke|captur|kadjar|sandero|duster|sprinter|picanto|zafira|insignia|vectra"
    r"|laguna|megane|berlingo|picasso|cupra|leon|toledo|kamiq|karoq|kodiaq|tucson|sportage"
    r"|camaro|impreza|forester|hilux|auris|avensis|prius|celica|supra|aygo|navara)\b")

FAULT = re.compile(
    r"\b(?:noise|noises|noisy|rattle|rattles|rattling|click|clicking|clicks|knock|knocking"
    r"|grinding|squeal|squealing|squeak|squeaking|whining|humming|judder|juddering"
    r"|wont start|won't start|wouldnt start|wouldn't start|not starting|cutting out|cuts out"
    r"|stalls|stalled|warning light|engine light|light on|leak|leaks|leaking|leaked|smoke"
    r"|smoking|overheating|overheated|misfire|misfiring|broken|broke|faulty|gone wrong"
    r"|failed|failing|fail|puncture|punctured|flat|bald|locked up|seized|clunk|clunking"
    r"|vibration|vibrating|pulling|sticking|jammed|rust|rusted|corroded|seized up"
    r"|garage (?:says|said|thinks|reckons|quoted|quotes|wants|has had)|they quoted"
    r"|needs? (?:a )?(?:new|replacing)|worn|knackered|shot)\b")

LEARNING = re.compile(
    r"\b(?:lesson|lessons|learner|learners|instructor|instructors|provisional|theory"
    r"|driving test|test booked|passed|pass|learn|learning|beginners?|tuition)\b")

LOOKBACK = 3


CLAUSE_BREAK = re.compile(r"\b(?:but|and|though|although|while|whereas|so|because|then|except)\b"
                          r"|[;,.!?]")

NOT_A_FAULT = re.compile(r"\b(?:not|no|never|isnt|isn't|arent|wasnt|wasn't|hasnt|hasn't"
                         r"|havent|haven't|dont|don't|cant|can't|fine|ok|okay|sorted|fixed"
                         r"|repaired|stopped|gone|better)\b")

NOT_THE_MACHINE = re.compile(r"\b(?:bike|cycle|bicycle|motorbike|motorcycle|scooter|mower"
                             r"|lawnmower|tractor|lorry|bus|train|plane|caravan|trailer)s?\b")


def _a_fault_that_is_not_undone(clause):
    for match in FAULT.finditer(clause):
        if match.group(0).lower().startswith(("not ", "wont", "won't", "wouldnt", "wouldn't")):
            return True
        before = clause[max(0, match.start() - 24):match.start()]
        after = clause[match.end():match.end() + 24]
        if NOT_A_FAULT.search(before) or NOT_A_FAULT.search(after):
            continue
        return True
    return False


def _the_car_in(clause):
    for match in CAR.finditer(clause):
        before = clause[max(0, match.start() - 20):match.start()]
        if NOT_THE_MACHINE.search(before):
            continue
        return True
    return False


def _says_a_broken_car(text):
    low = (text or "").lower()
    for clause in CLAUSE_BREAK.split(low):
        if _the_car_in(clause) and _a_fault_that_is_not_undone(clause):
            return True
    return False


def a_broken_car_is_the_subject(text, earlier=()):
    low = (text or "").lower()
    if LEARNING.search(low):
        return False
    if _says_a_broken_car(low):
        return True
    return any(_says_a_broken_car(line) for line in list(earlier)[-LOOKBACK:])


def no_broken_car(understood):
    return not (isinstance(understood, dict) and understood.get("car_fault"))


def no_broken_car_or_none(understood):
    return bool(isinstance(understood, dict) and understood.get("car_fault"))
