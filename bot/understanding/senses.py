
CUES = {
    "room": {
        "space": frozenset("""
            kitchen kitchens bedroom bedrooms bathroom bathrooms cupboard cupboards wardrobe
            wardrobes freezer fridge car boot shed garage loft attic cellar hall hallway landing
            landing flat house home drawer drawers shelf shelves cupboard worktop bench desk
            storage store storing put fit fits fitting tidy tidier tidy-up clutter stuff boxes
            box cupboard space cramped clutter pots pans utensils microwave toaster kettle
            small tiny little cramped narrow cramped squeeze squashed poky pokey tight
            """.split()),
        "booking": frozenset("""
            hotel hotels motel hostel guest house booking bookings booked book reservation
            reservations reception receptionist desk check checkin check-in concierge night
            nights twin double suite ensuite en-suite overbooked upgrade holiday stay staying
            need needs needed want wants wanted prefer rather looking searching
            traveller traveler luggage suitcase suitcases case cases bags abroad airport
            flight trip refunded
            """.split()),
    },
    "bat": {
        "sport": frozenset("""
            cricket bowling bowler batsman batsmen innings wicket wickets pitch stumps willow
            grip oiling oil knocked-in handle tennis ping pong table shot cover drive yorker
            spinner seamer nets net match club league batting batsman's bails crease
            """.split()),
        "animal": frozenset("""
            flew fly flying loft attic roof rafters eaves belfry wings wing bitten rabies
            droppings squeaking squeak colony pup hibernating hibernate dusk rescued
            hedgehog tree trees garden shed hole
            """.split()),
    },
    "coach": {
        "vehicle": frozenset("""
            train trains rail railway station stations platform platform ticket tickets journey
            journeys seat seats carriage carriages bus buses megabus national-express travel
            travelling traveling trip legroom route timetable delay delays luggage left-luggage
            book booked booking reservations departures
            """.split()),
        "teacher": frozenset("""
            football rugby netball cricket hockey tennis kids child children junior juniors
            under u7 u8 u9 u10 u11 u12 u13 u14 u15 u16 session sessions drill drills players
            squad tactics coaching goalkeeper striker defenders midfield training skills
            """.split()),
        "furniture": frozenset("""
            sofa settee couch lounge upholstery reupholster reupholstered fabric cushions
            cushion seater armchair furniture corner three-piece living rooms room front-room
            """.split()),
    },
    "degrees": {
        "temperature": frozenset("""
            hot cold warm warmer warmest freezing boiling heat humid humidity celsius
            fahrenheit weather forecast summer winter autumn spring sunny sun shade outside
            today tonight tomorrow thermometers thermometer fever thermostat oven roasting
            heatwave heatwaves sweaty sunscreen brollies
            """.split()),
        "university": frozenset("""
            uni university universities college ucas graduate graduates graduated graduation
            student students masters bachelors bachelor bsc ba ma phd honours honours-degree
            dissertation campus term semester freshers results classified first-class 2:1
            studying studied study course courses academic tutor lecturer professor
            """.split()),
        "angle": frozenset("""
            angle angles geometry triangle protractor rotate rotation rotated rotation
            turnaround corner corners bend bends slope sloped incline gradient
            """.split()),
    },
    "late": {
        "time": frozenset("""
            work job boss manager office meeting interview deadline shift roster rota overtime
            colleague bus buses train tram tube flight plane ferry fired sacked redundant
            school class lesson nursery childcare pickup collection homework exam detention
            court dentist hairdresser barber cinema theatre match kickoff traffic jam queue
            road motorway accident closed cancelled overslept alarm form
            """.split()),
        "cycle": frozenset("""
            period missed pregnant pregnancy test bleed bleeding spotting cramp pill
            contraceptive ovulate ovulating ovulation conceive conceiving conception cycle
            womb trimester midwife
            """.split()),
    },
}

CUES_AFTER_A_FIGURE = {"degrees": "temperature"}
_A_FIGURE = frozenset("""
    one two three four five six seven eight nine ten eleven twelve twenty thirty forty fifty
    sixty seventy eighty ninety hundred thousand zero
    """.split())


def _a_figure_before(line, word):
    forms = _forms(word)
    for i, token in enumerate((line.get("norm") or [])):
        if str(token).lower() not in forms or i == 0:
            continue
        before = str(line["norm"][i - 1]).lower().strip(".,!?;:")
        if before.isdigit() or before in _A_FIGURE:
            return True
    return False


def _forms(word):
    forms = {word}
    if len(word) > 3 and word.endswith("s") and not word.endswith("ss"):
        forms.add(word[:-1])
    if len(word) > 5 and word.endswith("es"):
        forms.add(word[:-2])
    return forms


def _the_words(line):
    words = []
    for word in (line.get("norm") or []):
        words.append(str(word).lower())
    clean = str(line.get("clean") or "").lower()
    if clean:
        words.extend(clean.split())
    return {form for word in words for form in _forms(word)}


def _how_many_words(cues, words):
    return len({form for cue in cues for form in (_forms(cue) & words)})


def senses(line):
    if not isinstance(line, dict):
        return {}
    words = _the_words(line)
    if not words:
        return {}
    found = {}
    for word, by_sense in CUES.items():
        if not (_forms(word) & words):
            continue
        scored = sorted(((_how_many_words(cues, words), sense)
                         for sense, cues in by_sense.items()), reverse=True)
        if len(scored) < 2:
            continue
        if scored[0][0] == 0:
            if word in CUES_AFTER_A_FIGURE and _a_figure_before(line, word):
                found[word] = CUES_AFTER_A_FIGURE[word]
            continue
        if scored[0][0] == scored[1][0]:
            continue
        found[word] = scored[0][1]
    return found
