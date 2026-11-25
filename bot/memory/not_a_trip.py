import re

DETERMINER = frozenset("""
a an the my your our their his her its this that these those some any another each every no
""".split())
BELONGS_TO_THE_PLACE = frozenset("the a an".split())
PARTICLE = frozenset("""
about up down out back off over through around round along into away
""".split())
DOING_AFTER_TO = frozenset("""
wait waits waited waiting hold holds held holding hope hopes hoped hoping plan plans planned
planning think thinks thought thinking save saves saved saving spend spends spent spending
finish finishes finished finishing decide decides decided deciding apply applies applied applying
arrange arranges arranged arranging aim aims aimed aiming avoid avoids avoided avoiding
worry worries worried worrying sort sorted sorting
be been being get gets got getting go goes going do does did doing see sees saw seeing
try tries tried trying have has had having keep keeps kept keeping quit quits quitting
leave leaves left leaving start starts started starting stop stops stopped stopping
manage manages managed managing afford affords afforded affording book books booked booking
lose loses lost losing win wins won winning sell sells sold selling
ask asks asked asking tell tells told telling call calls called calling look looks looked looking
find finds found finding put puts putting buy buys bought buying eat eats ate eating
drink drinks drank drinking work works worked working sleep sleeps slept sleeping
pass passes passed passing faint faints fainted fainting collapse collapses collapsed collapsing
throw throws threw thrown throwing die dies died dying move moves moved moving
wean weans weaned weaning
""".split())
ORDINARY = frozenset("""
uni university unis college colleges campus nursery nurseries creche childcare playschool
""".split())
DOING = frozenset("""
feel feels felt feeling
cry cries cried crying sob sobs sobbing weep weeps weeping wail wails wailing
laugh laughs laughed laughing giggle giggles giggling chuckle chuckles chuckling
scream screams screamed screaming shout shouts shouted shouting yell yells yelled yelling
panic panics panicked panicking faint faints fainted fainting
throw throws threw throwing vomit vomits vomited vomiting puke pukes puked puking
sneeze sneezes sneezed sneezing cough coughs coughed coughing hiccup hiccups hiccuping
burp burps burped burping gag gags gagged gagging choke chokes choked choking
die dies died dying explode explodes exploded exploding burst bursts bursting
moan moans moaned moaning groan groans groaned groaning snore snores snored snoring
sweat sweats sweated sweating blush blushes blushed blushing
shiver shivers shivered shivering tremble trembles trembled trembling
wet wee poo splutter splutters spluttering
# The same word twice, once as the doing and once as the idiom it makes: "im going to lose it"
# and "im going to crack up" are the temper, "im going to pass out" is the body, and "im going
# to snap" is both. A place is never one of these on its own, so the second word does not matter.
lose loses losing lost crack cracks cracked cracking snap snaps snapped snapping
pop pops popped popping flip flips flipped flipping pass passes passed passing
break breaks breaking broke broken
""".split())


def a_doing_after_to(going_words):
    kept = [word for word in going_words
            if str(word).strip(" ,.;:!?'\u2019") not in ("",)]
    if kept and kept[0].lower().strip(" ,.;:!?") in BELONGS_TO_THE_PLACE:
        kept = kept[1:]
    if not kept:
        return False
    first = kept[0].lower().strip(" ,.;:!?'\u2019")
    if first in DOING_AFTER_TO or first in DOING:
        return True
    if len(kept) < 2:
        return False
    second = kept[1].lower().strip(" ,.;:!?'\u2019")
    return second in DETERMINER or second in PARTICLE


def a_place_of_ordinary_life(place):
    words = [word.lower().strip(" ,.;:!?'\u2019") for word in str(place or "").split(" ")]
    words = [word for word in words if word]
    if words and words[0] in BELONGS_TO_THE_PLACE:
        words = words[1:]
    return bool(words) and words[0] in ORDINARY


def not_a_destination(going_words, place):
    return a_doing_after_to(going_words) or a_place_of_ordinary_life(place)


A_PERSON = (r"(?:sister|brother|mother|father|son|daughter|mum|mom|dad)[\s-]in[\s-]laws?|"
            r"sisters?|brothers?|mum|mom|mam|mother|father|dad|parents?|gran|granny|nan|nana|"
            r"grandma|granddad|grandad|grandpa|grandparents?|aunts?|aunty|auntie|uncles?|cousins?|"
            r"in[\s-]?laws?|sons?|daughters?|kids|children|family|friends?|mates?|pals?")
VISIT_TO = re.compile(
    r"\b(?:(?:to|at)\s+|(?:to\s+)?(?:see|seeing|visit|visiting)\s+)"
    r"(?P<own>my|our|his|her|their)\s+(?:the\s+)?(?:own\s+)?(?P<person>" + A_PERSON + r")"
    r"(?:\u2019s|'s|s')?s?(?:\s+(?P<thing>house|place|flat|home))?"
    r"\s*(?=$|[,.!?;]|\b(?:for|on|at|this|next|tonight|tomorrow|today|later|after)\b)",
    re.IGNORECASE)


THEIR_PERSON = re.compile(
    r"^\s*(?P<own>my|our|his|her|their)\s+(?:own\s+)?(?P<person>" + A_PERSON + r")"
    r"(?:\u2019s|'s|s')?s?(?:\s+(?P<thing>house|place|flat|home))?\s*$", re.IGNORECASE)


def _the_person_in(found):
    who = " ".join(found.group("person").lower().split())
    if who.startswith("in"):
        who = "in-laws"
    said = found.group("own").lower() + " " + who
    thing = (found.groupdict().get("thing") or "").lower()
    return said + " " + thing if thing else said


def a_person(place):
    found = THEIR_PERSON.match(str(place or ""))
    return _the_person_in(found) if found else ""


GOING_BEFORE = re.compile(
    r"\b(?:going|goes|went|off|away|over|down|up|round|around|out|back|heading|driving|flying|"
    r"travelling|traveling|staying|stay)\b", re.I)
FILLER_BEFORE = re.compile(r"^\s*(?:(?:so|and|but|oh|also|anyway|then|now|well|ok|okay|right|"
                           r"im|i'm|i am|we're|we are|were|i|we)\s+){0,3}$", re.I)


IN_A_CARING_PLACE = re.compile(
    r"\b(?:at|in|to)\s+(?:the\s+|a\s+)?(?:hospital|hospice|care home|nursing home|residential "
    r"home|clinic|infirmary|surgery|ward|a&e|ae|icu|intensive care|high dependency|"
    r"coronary care|children'?s ward)\b", re.I)


def the_visit(line):
    said = str(line or "")
    if IN_A_CARING_PLACE.search(said):
        return ""
    found = VISIT_TO.search(said)
    if not found:
        return ""
    before = said[:found.start()]
    if not (GOING_BEFORE.search(before) or FILLER_BEFORE.match(before)):
        return ""
    return _the_person_in(found)
