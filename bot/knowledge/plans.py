import re

from ..compose import pick, said_again
from ..compose.repair import amends_to, line_of, owns_the_deed
from .cooking import ANNOUNCED_DISH, RECIPES
from .dishes import a_dish_is_already_the_plan
from .lookup import A_HOURS_ASK, A_WEATHER_ASK, PEOPLE_FEMALE, PEOPLE_MALE, entry

ANSWERS = ("home-and-diy", "family-and-parenting", "geography-and-travel")

PLAN_ASK = ("how", "what", "whats", "what's", "where", "when", "any", "help", "should", "could",
            "would", "can i", "can you", "much", "idea", "ideas", "tips", "advice", "start",
            "best way",
            "planning", "plan", "plans", "organising", "organizing", "arranging", "throwing",
            "thrown", "hosting", "sorting out", "putting together", "getting ready for")

_OWN_COUNT = re.compile(
    r"\bhow many (?:\w+ ){0,3}(?:do|does|did) (?:i|we) (?:have|got)\b"
    r"|\bhow many (?:\w+ ){0,3}have (?:i|we) got\b")


def _not_a_count_of_their_own(understood):
    text = understood.get("text")
    if not isinstance(text, str) or not text:
        words = understood.get("words") or ()
        text = " ".join(w for w in words if isinstance(w, str))
    return not _OWN_COUNT.search(" " + text.lower() + " ")

_A_DATE_ASK = re.compile(r"\b(?:when|what date|which date|what day)\b")

_A_DO = re.compile(r"\b(?:party|parties|invitations?|invites?|guests?|venue|plan|plans|planning|"
                   r"organis\w*|organiz\w*|menu|buffet|food|catering|decorations?|cake|games|"
                   r"themes?|book|booking)\b")


def _not_a_date_question(understood):
    text = understood.get("text")
    if not isinstance(text, str) or not text:
        words = understood.get("words") or ()
        text = " ".join(w for w in words if isinstance(w, str))
    line = " " + text.lower() + " "
    return not (_A_DATE_ASK.search(line) and not _A_DO.search(line))


_WHAT_HAPPENED = re.compile(
    r"\b(?:did|has|have)\s+(?:anything|something|much|any good)\b"
    r"|\bwhat(?:'s|s| is)?\s+happened\b"
    r"|\banything (?:good |nice |interesting )?happen\b", re.I)


def _asks_for_ideas(understood):
    text = understood.get("text")
    if not isinstance(text, str) or not text:
        words = understood.get("words") or ()
        text = " ".join(w for w in words if isinstance(w, str))
    return not _WHAT_HAPPENED.search(" " + text.lower() + " ")


def _the_free_weekend_fits_and_is_asked(understood):
    return _free_weekend_fits(understood) and _asks_for_ideas(understood)


_ASKS_A_CLOCK = re.compile(
    r"\bwhat time (?:is|are|was|were|do|does|did|will|would)\b"
    r"|\bwhen (?:is|are|was|were|do|does|did|will) (?!i\b|we\b|you\b)", re.I)


_PEOPLE = tuple(w for w in PEOPLE_MALE + PEOPLE_FEMALE
                if w not in ("he", "him", "his", "she", "her", "hers", "his"))
_A_PRESENT_FOR = tuple("%s my %s" % (verb, who)
                       for verb in ("get", "gets", "getting", "got", "buy", "buys", "buying",
                                    "bought", "give", "gives", "giving", "gave")
                       for who in _PEOPLE)


def _not_a_deed_of_their_own(reading):
    return not (owns_the_deed(reading) or amends_to(line_of(reading)))

_DECLUTTER_ASK = ("clear out", "clearing out", "clearout", "clear the clutter", "clear clutter",
                  "declutter", "too much stuff", "too much clutter", "fed up with", "sick of",
                  "rid of everything", "rid of it all", "rid of the lot", "rid of all of it")

_DECLUTTER_ROOM = ("room", "rooms", "house", "home", "flat", "place", "garage", "loft", "shed",
                   "attic", "wardrobe", "wardrobes", "cupboard", "cupboards", "closet", "kitchen",
                   "bedroom", "bedrooms", "cellar", "spare room", "drawer", "drawers", "shelves",
                   "hall", "hallway", "landing", "under the stairs", "cabinets", "units",
                   "car boot", "box room", "study", "desk", "filing")
_DECLUTTER_STUFF = ("stuff", "clutter", "junk", "rubbish", "things", "mess", "gear", "bits",
                    "crap", "tat", "odds and ends", "it all", "everything")

_BARE_RID = re.compile(r"\bget rid of\s*(?:$|[.?!])")
_JOB_NAMED = ("clear out", "clearing out", "clearout", "declutter", "clear the clutter",
              "clear clutter", "big tidy", "tidy up the house", "tidy my house",
              "tidy up my house", "sort the house out", "sort the house")
_TOO_MUCH = re.compile(r"\btoo much (?:stuff|clutter|junk|rubbish|things|mess|gear|crap|tat)\b")


def _declutter_fits(understood):
    text = understood.get("clean") or understood.get("text") or ""
    if not isinstance(text, str):
        text = " ".join(w for w in (understood.get("words") or ()) if isinstance(w, str))
    clean = " " + " ".join(text.split()) + " "
    if _BARE_RID.search(clean):
        return True
    if any(" " + job + " " in clean for job in _JOB_NAMED):
        return True
    if _TOO_MUCH.search(clean):
        return True
    names_room = any(" " + room + " " in clean for room in _DECLUTTER_ROOM)
    names_pile = any(" " + pile + " " in clean for pile in _DECLUTTER_STUFF)
    return bool(names_room or names_pile)

_WEDDING_PAPERS = ("paperwork", "notice", "registrar", "register office", "legal", "admin",
                   "papers", "documents", "bring",
                   "how do i get married", "how do we get married", "how to get married",
                   "how do you get married", "how do i marry", "how do we marry",
                   "how do i arrange", "how does it work",
                   "licence", "license", "certificate", "witness", "witnesses", "need to do",
                   "what do i need", "what do we need", "whats needed", "what's needed",
                   "need before", "before we get married", "getting married what",
                   "give notice", "notice to marry", "give notice to marry", "to marry")
_WEDDING_ASK = ("notice", "paperwork", "registrar", "register office", "need to", "to marry",
                "witness", "witnesses")
_WEDDING_COUNT = re.compile(r"how many (?:guests|people|to invite|should we (?:invite|have))"
                            r"|number of guests|how big|guest count|size of the wedding")
_WEDDING_WHEN = ("far ahead", "how early", "how long before", "lead time", "how soon",
                 "when should we book", "when do we book", "when to book", "when should i book",
                 "book the venue", "book a venue", "book the photographer", "book a photographer",
                 "book the registrar", "book the caterer", "book the church")
_WEDDING_GUESTS = (
    "There is no right number, only a price: each guest costs roughly \u00a3100 to \u00a3150 at "
    "a catered wedding, so 100 guests is a \u00a310,000 to \u00a315,000 decision. Write two "
    "lists - the people you would be sad not to see, then everyone else - and cut from the "
    "second until the money works. The room is the other hard limit, because a seated meal needs "
    "about 1.2 square metres a head, and children count towards both.")
_WEDDING_LEAD_TIME = (
    "Venue first: a year to 18 months ahead for a Saturday in summer, and six months is enough "
    "for a winter Friday or a village hall. The registrar or celebrant as soon as the date is "
    "fixed, the photographer nine to twelve months out, the caterer six to nine, the cake and "
    "the outfit four to six. Ask the venue for its own notice period before you fall for a date, "
    "because a barn that has to give notice to the council can block a summer Saturday.")

_WEDDING_MONEY = ("cost", "costs", "much", "budget", "cheap", "cheapest", "afford", "price",
                  "save", "saving", "spend", "quotes", "quote", "\u00a3")


VAGUE_TOPICS = (None, "", "small-talk", "opinions", "creative")

TRY_ONCE_ASK = ("what", "whats", "what's", "should", "suggest", "recommend", "tell", "give",
                "idea", "ideas", "anything", "something", "one thing", "surprise", "want",
                "need", "any", "name")

TRY_ONCE = (
    "Learn to make one loaf of bread by hand: flour, water, yeast, salt, an hour of rising, and "
    "the house does the rest. The first one is always a bit wonky and nobody minds.",
    "Swim outside once - a lake, a lido, the sea in October - with a friend and a towel waiting. "
    "Twenty seconds is enough to know you did it.",
    "See a band you have never heard of in a small room on a week night. A cheap ticket, no "
    "expectations, and it is the best way to find music you keep.",
    "Take one night away on your own: a train, a cheap room, a book. It is a different kind of "
    "trip from a holiday with people, and easier than it sounds.",
    "Watch the sunrise on purpose once: check the time, set an alarm, take a flask. One early "
    "start buys you a morning you will talk about for years.",
    "Learn to change a tyre and check your oil before you have to. Ten minutes of practice on "
    "your own drive beats an hour on a hard shoulder in the rain.",
    "Eat in a restaurant by yourself, with a book, once. Nobody is looking, and it is the most "
    "peaceful hour you can buy for the price of a lunch.",
    "Post a real letter to somebody who will not expect it - a grandparent, an old teacher, a "
    "friend who moved away. It lands differently from a message.",
    "Plant something you can eat and keep it alive to the plate. Herbs on a windowsill count, and "
    "one tomato plant teaches you more than a book does.",
    "Go to a match of a sport you know nothing about and sit with the crowd. Someone will explain "
    "the rules before half time, and the noise is the point.",
    "Give a morning to something local - a food bank, a park clean-up, a repair cafe. One morning "
    "with no commitment afterwards, and you will meet people you would never otherwise meet.",
    "Cook the same dish once a week until you can do it without the recipe. Everyone should own "
    "one dinner, and six goes is usually enough.",
    "Draw something badly on purpose, and keep it. Being a beginner at something for an afternoon "
    "is good for you.",
    "Catch a train to a town an hour away with no plan for the day: walk it, have lunch, come "
    "home. The having-no-plan is the good bit.",
    "Take a class where you make something with your hands - pottery, woodwork, knitting, "
    "welding. A thing that stays made is a rare sort of satisfaction.",
    "Sleep outside once: a tent in a friend's garden, a campsite, a bothy. You will remember the "
    "night, not how well you slept.",
    "Learn ten words of a language before you go somewhere that speaks it. Shopkeepers forgive a "
    "lot for one honest attempt.",
    "Ask an older relative to tell you about their childhood and record it on your phone. It is "
    "the cheapest history you will ever collect.",
)

TRY_ONCE_MORE = (("another one", "one more", "another idea", "one more idea", "another thing",
                  "something else to try", "anything else to try", "a different one",
                  "more ideas", "give me more", "another suggestion"),
                 ("give", "one", "more", "another", "try", "idea", "ideas", "else",
                  "anything", "something", "different"))


def _try_once(memory, understood):
    if (understood or {}).get("subject"):
        return None
    if (understood or {}).get("topic") not in VAGUE_TOPICS:
        return None
    return pick(TRY_ONCE, memory, _words_of(understood))


def _try_once_more(memory, understood):
    turns = memory.get("turns") or []
    last = turns[-1].get("bot") if turns and isinstance(turns[-1], dict) else ""
    if said_again(last) not in {said_again(one) for one in TRY_ONCE}:
        return None
    if (understood or {}).get("subject"):
        return None
    return pick(TRY_ONCE, memory, _words_of(understood))



def _wedding_plan(memory, understood):
    line = " " + str(understood.get("clean") or understood.get("text") or "").lower() + " "
    if any(word in line for word in _WEDDING_WHEN):
        return _WEDDING_LEAD_TIME
    if any(word in line for word in _WEDDING_PAPERS) and not any(
            word in line for word in _WEDDING_MONEY):
        return ("Give notice first: you each do it at your local register office at least 29 days "
                "before the wedding (in Scotland a marriage notice to the registrar), with a "
                "passport or birth certificate and proof of address. Book the venue and the "
                "registrar's slot, and find two witnesses. The 29 days is a legal minimum, not a "
                "booking window, so do not leave it late.")
    if _WEDDING_COUNT.search(line):
        return _WEDDING_GUESTS
    return ("Guest list first, because it sets the cost of everything else: the venue, the food and "
            "the drink are about 60% of a wedding, and halving the guest list roughly halves the "
            "bill. Book the venue and the registrar next (a year ahead for a Saturday), then the "
            "photographer, and keep 10% back for what you forgot.")

FREE_TIME = ("weekend", "weekends", "this weekend", "next weekend", "long weekend",
             "saturday", "sundays", "on saturday", "on sunday", "day off", "bank holiday",
             "tonight", "this evening", "free evening", "after work", "free afternoon",
             "home from work", "get home from work", "back from work", "from work",
             "when i get home", "when i get in", "finish work", "finished work",
             "leave work", "left work", "got home from work",
             "this afternoon", "afternoon off", "free day", "nothing planned",
             "evenings", "my evenings", "weekday evenings",
             "week off", "weeks off", "week off work", "days off", "few days off",
             "time off", "time to myself", "days to myself",
             "off next week", "off for a week", "off all week", "whole week off", "week free",
             "a week free", "week at home", "week to myself", "off work for a week",
             "off work next week",
             "next week off", "next week off work", "week off next month", "a few days off",
             "few days off", "days off next month", "off for a few days")
FREE_TIME_ASK = ("what should i do", "what can i do", "what do i do", "what to do",
                 "any ideas", "ideas for", "any suggestions", "suggestions for",
                 "something to do", "anything to do", "what shall i do", "where should i go",
                 "where can i go", "whats on", "what's on", "big plans",
                 "nothing planned", "nothing on", "any tips", "tips", "advice",
                 "suggestions", "what do you suggest", "plan it", "help me plan",
                 "a few days off", "few days off", "days off next month", "week off next month",
                 "i have the day off", "i have a day off", "have the day off", "day off on",
                 "got the day off", "got a day off",
                 "day off tomorrow", "i have a long weekend", "long weekend free",
                 "days off next week", "days off next month", "days off this week",
                 "days off at the end of", "i have days off", "have days off", "got days off",
                 "days holiday", "days free next week", "days free next month",
                 "weekend free", "i have days off", "i have the weekend", "the weekend to myself",
                 "in the summer", "in summer", "in the winter", "in winter", "in the spring",
                 "in spring", "this summer", "this winter", "no plans", "nothing to do with it",
                 "use a week off", "use my week off", "week off well", "make the most of",
                 "plan a week off", "plan my week off", "plan the week off",
                 "spend a week off", "spend my week off", "spend the week off",
                 "how do i use", "how do i plan", "how should i spend", "sort my", "sort out")

DAY_PLAN = (
    "Put two things in the afternoon and give each a time: one that gets you out (a walk you "
    "have not done, a park, the library) and one you keep putting off that takes an hour. A free "
    "afternoon with no time on it is what dissolves into the phone.")

DAY_OFF_PLAN = (
    "Treat it as a small Saturday: one thing out of the house (a walk you have not done, a "
    "market, a museum or gallery - most are free), one job you keep putting off that takes an "
    "hour, and one person to see. Put times on the first two the night before; a free day goes "
    "in small pieces when nothing is decided.")

_THE_EVENING = ("tonight", "this evening", "free evening", "after work", "evening", "evenings",
                "home from work", "get home from work", "back from work", "from work",
                "when i get home", "when i get in", "finish work", "finished work",
                "leave work", "left work", "got home from work")

EVENING_PLAN = (
    "Give the evening a shape rather than waiting for an idea: one thing you will actually "
    "do at 8pm (a film you have been meaning to watch, a walk before it gets dark, a call to "
    "someone you like), tea that takes a bit of effort, and the phone in another room for the "
    "first hour. A free evening feels long when nothing is decided and short when one thing is.")

WEEKEND_PLAN = (
    "Three things, one each: something out of the house (a walk you have not done, a park, the "
    "library, a free museum), one job you keep putting off but that takes an hour (the drawer, "
    "the bike, the photos), and one thing with a person - a call, a walk with someone, a coffee. "
    "Put the outdoor one on the better day and keep Sunday evening free, or the weekend ends "
    "in a rush and feels like it never happened.")

WEEK_OFF = ("week off", "weeks off", "week off work", "time off", "time to myself",
            "days to myself", "off next week", "off for a week", "off all week",
            "whole week off", "week free", "a week free", "week at home", "week to myself",
            "off work for a week", "off for the week", "off work next week")

WEEK_PLAN = (
    "Put a couple of nights away in the middle of the week and keep the first and last days "
    "free: somewhere two or three hours away by train is enough, and going Tuesday to Thursday "
    "costs less than the weekend. Fill the other days a day at a time - one thing out of the "
    "house, one job you keep putting off - and a week off stops slipping past unnoticed.")

SUMMER_WEEK = ("In summer, put the outdoors before ten or after five and keep the middle of the "
               "day for the job you keep putting off, so the heat sets the day instead of you.")
WINTER_WEEK = ("In winter, plan round the dark: the walk or the market at midday, and the "
               "cinema, the museum and the long cook for the evenings.")

WEEK_PLAN_SKINT = (
    "Start with the days that cost nothing: the walk you have not done, the library, a market, a "
    "park with a flask and a sandwich. Put the one paid thing in the middle of the week, because "
    "a cheap train day trip on a Tuesday off-peak is the best value going, and give each day one "
    "job out of the house so the week does not go by in small pieces.")


FREE_WEEKEND = (
    "Pick two things and put them in the diary by Friday: one that gets you out of the house - a "
    "walk with a destination, a market on Saturday morning, a museum or gallery you keep meaning "
    "to visit - and one person to see or one thing waiting for you at home. The free ones that "
    "work are the walk, the park, a canal, a hill with a view, the library and a market on a "
    "Saturday morning. Two plans makes a good weekend; five makes a list you abandon by Saturday "
    "lunchtime. An evening is the same rule: one thing out and one thing in. Tell me the town and "
    "who is with you and I can suggest something specific.")

MEDICINE_NEEDS_A_REASON = (
    "What is it for? That decides it, and the same tablet is right for one thing and wrong for "
    "the next: paracetamol or ibuprofen at the dose on the pack covers most aches, and a "
    "pharmacist will check anything for a stomach ulcer, a kidney problem or another medicine "
    "you take. Tell me the symptom and I will say what you can take tonight and what to keep "
    "off.")

_AN_IDEA_ASKED_FOR = re.compile(r"\b(?:ideas?|suggestions?|things to do|something to do|"
                                 r"nothing to do|what can i do|what can we do|what should i do|"
                                 r"what should we do|what shall i do|what shall we do|"
                                 r"what to do|what else|recommend|recommendations|any good)\b")

_SWALLOWED_THING = ("tablet", "tablets", "pill", "pills", "medicine", "medicines",
                    "painkiller", "painkillers", "paracetamol", "ibuprofen", "aspirin",
                    "antibiotic", "antibiotics", "antihistamine", "antihistamines",
                    "omeprazole", "dose", "supplement", "vitamin", "vitamins",
                    "swallow", "swallows", "swallowed", "swallowing")

_SWALLOWED = ("take", "taking", "took", "give", "giving", "swallow", "tablet", "tablets",
              "pill", "pills", "medicine", "medicines", "painkiller", "painkillers",
              "paracetamol", "ibuprofen", "aspirin", "antibiotic", "antibiotics",
              "antihistamine", "antihistamines", "omeprazole", "dose", "supplement",
              "vitamin", "vitamins")


_BRING_IT = ("picnic", "picnics", "bbq", "bbqs", "barbecue", "barbecues", "barbie", "party",
             "parties", "dinner party", "housewarming", "host", "hosts", "hostess",
             "birthday", "wedding", "buffet", "round", "potluck", "gathering")

_OWN_ACTIVITY = ("weekend", "weekends", "saturday", "sunday", "day off", "days off",
                 "walk", "walks", "film", "films", "book", "books", "cook", "cooking",
                 "garden", "gardening", "friend", "friends", "market", "museum", "gallery",
                 "park", "library", "gym", "game", "games", "shop", "shopping", "trip",
                 "away", "pub", "coffee", "music", "cinema", "tv", "series", "run", "swim")


_THE_WORLD = ("in the world", "around the world", "across the world", "world news", "the news",
              "the headlines", "headlines", "current events", "in the country")
_ASKS_THE_WORLD = re.compile(
    r"\b(?:what|whats|what's|hows|how's|any|latest|tell|give|show)\b[^.]{0,24}\b(?:going on|"
    r"happening|happened|news|headlines|new)\b|\b(?:any|the|todays|today's)\s+(?:world\s+)?"
    r"news\b|\bheadlines\b|\bcurrent events\b", re.I)


def _asks_about_the_world(said):
    return bool(_holds(said, _THE_WORLD) and _ASKS_THE_WORLD.search(said))


def _said_words(understood):
    parts = [(understood or {}).get("clean"), (understood or {}).get("text")]
    parts.extend((understood or {}).get("words") or ())
    return " ".join(str(part) for part in parts if part).lower()


def _said_now(understood):
    clauses = [clause for clause in ((understood or {}).get("clauses") or []) if clause]
    if clauses:
        return " ".join(str(word) for word in clauses[-1]).lower()
    return _said_words(understood)


_A_MOVE_TO_PLAN = re.compile(
    r"\b(?:plan|planning|planned|organise|organize|organising|organizing|prep|prepare|preparing|"
    r"arrange|arranging|checklist|tips?|advice|start|started|starting|before|ahead|get ready|"
    r"getting ready|ready)\b.{0,24}\b(?:a move|the move|the house move|my move|our move|"
    r"move out|move in)\b|\b(?:a move|the move|my move|our move)\b.{0,24}\b(?:plan|planning|"
    r"organise|organize|checklist|tips?|advice|prepare|prep|arrange)\b"
    r"|\bwhen\s+(?:i|we|you)\s+move\b|\bwhen\s+moving\b|\bbefore\s+(?:i|we|you)\s+move\b"
    r"|\bwe\s*(?:'|\s)?re\s+moving\b", re.I)
_A_MOVE_ELSEWHERE = re.compile(
    r"\b(?:abroad|overseas|emigrat\w*|visa|another country|different country|new country|"
    r"australia|canada|new zealand|america|usa|spain|france|portugal|germany|ireland|dubai|"
    r"team|teams|job|jobs|career|office|house share|houseshare|chess|piece|checkmate|"
    r"the goalposts|goalposts|"
    r"in together|moving in with|move in with)\b", re.I)


def _a_household_move(understood):
    said = _said_words(understood)
    return bool(_A_MOVE_TO_PLAN.search(said)) and not _A_MOVE_ELSEWHERE.search(said)


_HOME_IN_THE_LINE = re.compile(r"\b(?:house|houses|home|homes|flat|flats|apartment|apartments)\b",
                               re.I)


def _a_household_move_or_a_named_move(understood):
    if _HOME_IN_THE_LINE.search(_said_words(understood)):
        return True
    return _a_household_move(understood)


_TODAY_WORDS = ("today", "tonight", "this afternoon", "this morning", "this evening", "tomorrow")
_WEEKEND_WORDS = ("weekend", "weekends", "saturday", "sunday", "day off", "days off",
                  "week off", "long weekend")


def _a_free_weekend(memory, understood):
    said = _said_words(understood)
    if _a_medicine_line(said):
        return MEDICINE_NEEDS_A_REASON
    if _holds(said, _TODAY_WORDS) and not _holds(said, _WEEKEND_WORDS):
        if _holds(said, ("tonight", "this evening")):
            return EVENING_PLAN
        return DAY_OFF_PLAN
    return FREE_WEEKEND


def _holds(said, words):
    return any(re.search(r"\b" + re.escape(word) + r"\b", said) for word in words)


def _a_medicine_line(said):
    if not _holds(said, _SWALLOWED):
        return False
    if _AN_IDEA_ASKED_FOR.search(said) and not _holds(said, _SWALLOWED_THING):
        return False
    return True


FREE_TIME_TIME = frozenset("""
    weekend weekends saturday saturdays sunday sundays friday fridays monday mondays tuesday
    tuesdays wednesday wednesdays thursday thursdays week weeks weekday weeknight evening
    evenings afternoon afternoons morning mornings night nights tonight tomorrow today
    holiday holidays day days off hour hours while time break
    spring summer autumn winter terms half-term
    """.split())
FREE_TIME_WORDS = FREE_TIME_TIME | frozenset("""
    cheap cheaper cheapest cheaply budget budgets free money cost costs spend spending spent
    afford much less little broke skint quid pound pounds
    """.split())
FREE_TIME_WHO = frozenset("""
    i me my we us our you your they them he she him her kid kids child children family families
    everyone anybody somebody friend friends partner husband wife mum dad son daughter baby
    toddler
    """.split())


HOLIDAY_PREFIX = frozenset("bank public school".split())
AT_HOME = re.compile(r"\b(?:at home|at ours|indoors|inside|outdoors|outside|out and about)\b")
FREE_TIME_CUE = re.compile(
    r"\bnothing (?:much )?planned\b|\b(?:no|not much|nothing much) plans?\b"
    r"|\bnothing (?:at all )?(?:to do|going on|on)\b|\bnot a thing planned\b", re.I)
A_DAY_CONDITION = frozenset("""
    cold colder hot hotter warm warmer wet damp raining rainy rain sunny freezing frozen snow
    snowy icy windy foggy grey gray dark weather forecast degrees bored boring bored stiff
    """.split())


def _a_stretch_of_time_to_fill(understood):
    named = []
    subject = understood.get("subject")
    if subject:
        named.append(str(subject).lower())
    for found in understood.get("entities") or ():
        if isinstance(found, dict) and found.get("text"):
            named.append(str(found["text"]).lower())
    line_said = str(understood.get("clean") or "").lower()
    if FREE_TIME_CUE.search(line_said) and all(
            word in FREE_TIME_WORDS or word in FREE_TIME_WHO or word in A_DAY_CONDITION or
            word in FREE_TIME_TIME
            for word in re.findall(r"[a-z']+", " ".join(named).lower())):
        return True
    words_named = re.findall(r"[a-z']+", AT_HOME.sub(" ", " ".join(named).lower()))
    if any(word in FREE_TIME_TIME for word in words_named):
        words_named = [word for word in words_named if word not in HOLIDAY_PREFIX]
    covered = _covered_words(line_said, FREE_TIME)
    here_now = _the_place_the_block_is_at(
        line_said, block=bool(covered) or bool(set(re.findall(r"[a-z']+", line_said))
                                              & FREE_TIME_TIME))
    for word in words_named:
        if word in FREE_TIME_WORDS or word in FREE_TIME_WHO:
            continue
        if word in covered or word in here_now:
            continue
        return False
    line = line_said
    if set(re.findall(r"[a-z']+", line)) & FREE_TIME_TIME:
        return True
    if AT_HOME.search(line):
        return True
    if covered:
        return True
    topic = understood.get("topic_own", understood.get("topic"))
    return not topic or topic == "small-talk"


def _free_weekend_fits(understood):
    if _about_a_thing_the_person_has(understood):
        return False
    said = _said_words(understood)
    if _ASKS_A_CLOCK.search(said):
        return False
    if _asks_about_the_world(said):
        return False
    leans = understood.get("leans_on")
    follows = isinstance(leans, dict) and bool(leans.get("subject"))
    if _holds(said, _BRING_IT) and re.search(r"\b(take|taking|took|bring|bringing|give|"
                                            r"giving|make)\b[^.]*\bto\b", said):
        return False
    if _holds(said, _SWALLOWED) and not _holds(_said_now(understood), _SWALLOWED):
        return _holds(_said_now(understood), _OWN_ACTIVITY)
    if not _a_medicine_line(said):
        if follows and leans.get("topic") == "health" and not _holds(said, _OWN_ACTIVITY):
            return False
        return True
    return not follows


_FOR_A_RAINY_DAY = re.compile(r"\bfor a rainy day\b")
_MONEY_WITH_IT = re.compile(r"\b(?:save|saves|saving|saved|savings|put aside|aside|fund|funds|"
                            r"money|cash|pounds?|quid|income|salary|afford|afforded|budget|"
                            r"emergency|invest|investing|interest)\b")


def _a_rainy_day_is_money(reading):
    said = _said_words(reading)
    if not _FOR_A_RAINY_DAY.search(said):
        return True
    return bool(_MONEY_WITH_IT.search(said))


NO_MONEY = ("None of that has to cost anything: the walk and the library are free either way, "
            "and a flask beats a cafe.")

MONEY_WORDS = ("no money", "not much money", "dont have money", "don't have money", "broke",
               "skint", "no cash", "on a budget", "tight budget", "money is tight", "cant afford",
               "can't afford", "cheap things", "free things", "as little as possible")

_COLD = re.compile(r"((with|have|has|had|got|caught|a|the|my|his|her|their)\s+cold\b"
                   r"|\bcold\s+(sore|virus|coming on|and a cough|at the moment))")
_COLD_WEATHER = re.compile(r"((is it|it is|it's|its|too|so|very|really|freezing|bit|outside"
                           r"|weather|getting|turning|pretty)\s+(\w+\s+)?cold\b"
                           r"|\bcold\s+(today|tomorrow|outside|weather|enough|out)\b)")

_UNWELL = ("sick", "ill", "unwell", "poorly", "flu", "covid", "migraine", "surgery",
           "operation", "hospital", "injury", "injured", "recovering", "recovery", "pain",
           "hurts", "hurting", "sore", "ache", "aching", "back", "knee", "shoulder", "ankle",
           "stomach", "chest", "fever", "temperature", "dizzy", "exhausted", "burnt out")


NEWBORN_WEEK = (
    "With a newborn the week plans itself, so plan the small things instead: take the nights in "
    "shifts so one of you gets a four-hour stretch, get out once a day even if it is only round "
    "the block, and say yes to anyone who offers to hold the baby while you sleep. Register the "
    "birth inside 42 days, keep the health visitor's number to hand, and book nothing that has a "
    "start time - a week off now is recovery, not a holiday.")

_NOTE_ASK = ("need a note", "need the note", "fit note", "sick note", "doctors note",
             "doctor's note", "medical note", "medical certificate", "self certificate",
             "self-certificate", "self cert", "self-certify", "signed off", "sign me off",
             "getting a note", "get a note", "note from the doctor")

_EVENT_AWAY = ("wedding", "funeral", "christening", "baptism", "moving house", "moving home",
               "house move", "moving day", "exam", "exams", "revision", "court", "interview")

_WHERE_GO_PHRASES = ("where should i go", "where can i go", "where to go", "where should we go",
                     "where can we go", "where would you go", "where could i go", "where to",
                     "where would we go", "where could we go", "which country", "what place",
                     "somewhere warm", "somewhere hot", "somewhere near", "where shall we go",
                     "where shall i go")

_AMBIGUOUS_CITY_WORDS = ("bath",)


def _a_city_is_named(line):
    from .travel import CITIES

    for city in CITIES:
        if city in _AMBIGUOUS_CITY_WORDS:
            continue
        if re.search(r"(?<![a-z])%s(?![a-z])" % re.escape(city), " " + line + " "):
            return True
    return False


_TRIP_PHRASES = ("plan a trip", "planning a trip", "planning a holiday", "book a trip",
                 "going away", "go away", "get away for", "away for a", "a trip", "trip with",
                 "trip for", "holiday with", "travel with", "a break away", "book a holiday",
                 "go somewhere", "going somewhere", "somewhere away", "stay at home",
                 "staying at home", "at home or away", "away or at home",
                 "weekend away", "weekends away", "away for the weekend", "away for a weekend")

_WHEN_AWAY = ("in january", "in february", "in march", "in april", "in may", "in june",
              "in july", "in august", "in september", "in october", "in november",
              "in december", "in the summer", "in summer", "in the winter", "in winter",
              "in spring", "in autumn", "at christmas", "over christmas", "next summer",
              "half term", "bank holiday week", "shoulder season", "in the sun", "for some sun")

_MONEY_ONLY = ("quid", "pounds", "euros", "dollars", "budget", "cheap", "afford")

_GIFT_ASK = ("what should i get", "what do i get", "what can i get", "what to get",
             "what should i buy", "what can i buy", "what to buy", "should i get",
             "ideas for a present", "ideas for a gift", "present ideas", "gift ideas",
             "ideas for presents", "ideas for the present", "ideas for her", "ideas for him",
             "present for", "presents for", "gift for", "gifts for", "buy for",
             "get her for", "get him for", "get them for", "get my mum", "get my dad",
             "get my mam", "get my mom", "get my mother", "get my father", "get my sister",
             "get my brother", "get my nan", "get my gran", "get my partner",
             "get my wife", "get my husband", "get my friend")

_EVENT_EVENING = ("parents evening", "parent evening", "school evening", "open evening",
                  "induction evening", "college evening", "back to school evening",
                  "parents nights", "parents night", "open night")

_MEDIUM_NAMED = ("netflix", "iplayer", "prime video", "disney", "now tv", "nowtv",
                 "britbox", "paramount", "all 4", "apple tv", "hayu", "youtube",
                 "streaming", "film", "films", "movie", "movies", "series", "show",
                 "shows", "boxset", "box set", "episode", "episodes", "documentary",
                 "documentaries", "sitcom", "sitcoms", "drama series", "podcast",
                 "podcasts", "audiobook", "audiobooks", "album", "playlist", "novel",
                 "novels", "something to read", "something to watch")

_MONTHS = ("january", "february", "march", "april", "may", "june", "july", "august",
           "september", "october", "november", "december")

_WORK_BLOCK = ("off work", "off next week", "next week off", "week off work", "off all week",
               "off for a week", "taking next week off", "taking the week off", "the week off",
               "off from monday", "off work for", "week at home")

_TIME_WORDS = frozenset(
    "tonight today tomorrow evening evenings afternoon afternoons morning mornings night "
    "nights weekend weekends week weeks weekday weekdays day days month months year years "
    "saturday sunday monday tuesday wednesday thursday friday summer winter spring autumn "
    "christmas easter holiday holidays time break "
    "when once whenever after before until till while".split())
_NO_SUBJECT = frozenset("things thing something anything stuff more other else".split())
_IDEA_FILLER = frozenset(
    "a an the any some more other no not few couple another new better good great best "
    "and or of on for to up out off my your our their his her its i we you they have has "
    "had got need needs want wants running stuck fresh different".split())
_IDEAS_FOR = re.compile(r"\bideas?\s+(?:for|about|on)\s+(.+)", re.I)
_IDEAS_ASK = re.compile(r"\bideas?\s+(?:what|which|who|where|how|when)\b", re.I)
_IDEA_NONE = re.compile(r"\b(no|not|never|without|dont|don't|doesnt|doesn't|havent|haven't)"
                        r"\s+(?:idea|ideas)\b", re.I)


def _ideas_about_a_thing(understood):
    clean = str((understood or {}).get("clean") or "").lower()
    if not clean:
        return False
    if _IDEA_NONE.search(clean):
        return False
    if _IDEAS_ASK.search(clean):
        return True
    found = _IDEAS_FOR.search(clean)
    if found:
        rest = found.group(1)
        words = [word for word in re.findall(r"[a-z']+", rest)
                 if word not in _IDEA_FILLER]
        if any(word in ("away", "somewhere", "abroad") for word in words):
            return True
        if not words:
            return False
        covered = _covered_words(rest, FREE_TIME + WEEK_OFF)
        here = _the_place_the_block_is_at(clean, block=True)
        words = [word for word in words if word not in covered and word not in here]
        if not words:
            return False
        return words[0] not in _TIME_WORDS and words[0] not in _NO_SUBJECT
    return False


_A_THING_THE_PERSON_HAS = ("health", "fitness", "sleep")


_ASKS_ABOUT_IT = ("what can i do", "what should i do", "what do i do", "what to do",
                  "what shall i do", "what can we do", "what should we do", "how do i",
                  "how can i", "what helps", "what would help", "what can i take",
                  "can i take", "anything i can", "anything to take", "anything i can take")


def _about_a_thing_the_person_has(reading):
    reading = reading or {}
    if not reading.get("subject"):
        return False
    if reading.get("topic_own") not in _A_THING_THE_PERSON_HAS:
        return False
    return _holds(_said_words(reading), _ASKS_ABOUT_IT)


def _a_day_out_is_the_question(reading):
    if _ideas_about_a_thing(reading):
        return False
    return not _about_a_thing_the_person_has(reading)


_ASKS = ("what should i do", "what can i do", "what do i do", "what to do", "what shall i do",
         "any ideas", "ideas", "idea", "anything to do", "something to do", "suggestions",
         "suggestion", "tips", "tip", "advice", "nothing planned", "nothing on", "no idea",
         "bored", "plan it", "help me plan", "plan something", "whats on", "what's on",
         "big plans", "recommend", "how do i fill", "fill the time", "keep busy", "keep me busy")

_SHORT_RUN = re.compile(
    r"\b(?:\d+|one|two|three|four|five|six)\s+(?:whole\s+|full\s+|more\s+)?days?\s+"
    r"(?:off|free|holiday|to myself|at home)\b"
    r"|\b(?:a\s+)?(?:few|couple\s+of|handful\s+of)\s+days?\s+(?:off|free|to myself)\b")

_PURPOSE_AFTER_RUN = re.compile(
    r"\b(?:to\s+[a-z]+|for\s+(?:the|a|an|my|our|his|her|their|some)\b"
    r"|so\s+(?:i|we)\s+can\b|because\b)")


def _short_run(line):
    found = _SHORT_RUN.search(line)
    if not found:
        return None
    if _PURPOSE_AFTER_RUN.search(line[found.end():]):
        return None
    return found

_REQUESTING_TIME = ("book a day off", "book a week off", "book time off", "book some time off",
                    "book the day off", "book it off", "take a day off", "take a week off",
                    "take time off", "take some time off", "take the day off", "take it off",
                    "request a day off", "request a week off", "request time off",
                    "ask for a day off", "ask for a week off", "ask for time off",
                    "ask my boss", "ask the boss", "ask my manager", "put in for",
                    "want to book", "want to take a day", "want to take a week",
                    "can i book", "can i take a day", "can i take a week",
                    "could i take", "could i book", "am i allowed to take")


_FREE_BLOCK_WORDS = frozenset((
    "weekend", "weekends", "saturday", "sundays", "sunday", "day", "days", "evening",
    "evenings", "night", "nights", "tonight", "afternoon", "morning", "holiday", "holidays",
    "week", "weeks", "time", "leave", "rest", "break", "free", "off", "plans", "plan",
    "work", "tomorrow", "today", "now", "later",
    "nothing", "home", "myself", "ourselves", "me", "us", "family", "friends",
    "monday", "mondays", "tuesday", "tuesdays", "wednesday", "wednesdays", "thursday",
    "thursdays", "friday", "fridays", "saturday", "weekday", "weekdays", "weeknight",
    "rainy", "wet", "cold", "indoors", "outside", "sunny", "summer", "winter", "autumn",
    "spring", "hot",
))

_ASK_WORDS = frozenset((
    "what", "whats", "what's", "which", "where", "when", "how", "why", "who",
    "should", "shall", "can", "could", "would", "will", "do", "does", "did", "doing",
    "i", "we", "you", "id", "im", "ive", "us", "me", "my", "our", "your",
    "the", "a", "an", "this", "that", "these", "those", "next", "last", "coming",
    "some", "any", "something", "anything", "nothing", "thing", "things", "stuff",
    "ideas", "idea", "suggestions", "suggestion", "suggest", "recommend",
    "tips", "tip", "advice", "advise", "good", "nice", "fun", "funny", "best", "better",
    "on", "in", "at", "for", "to", "of", "and", "or", "but", "with", "without",
    "around", "about", "out", "up", "there", "here", "together", "nearby", "local",
    "all", "day", "whole", "long", "few", "couple", "off", "free", "bored", "nothing",
    "fill", "busy", "keep", "make", "most", "use", "spend", "sort", "go", "going",
    "somewhere", "anywhere", "nowhere", "else", "instead", "please", "help", "planned",
    "plans", "plan", "properly", "proper", "decent", "little", "bit", "much", "spend",
    "spending", "spent", "cost", "costs", "price", "prices", "hi", "hiya", "hey",
    "hello", "yo", "ok", "okay", "so", "well", "just", "really", "actually", "still",
))

_JOB_WORDS = frozenset((
    "sort", "sorted", "sorting", "tidy", "tidying", "clear", "clearing", "clean", "cleaning",
    "declutter", "decluttering", "pack", "packing", "unpack", "unpacking", "paint", "painting",
    "fix", "fixing", "mend", "mending", "repair", "repairing", "decorate", "decorating",
    "redecorate", "reorganise", "reorganising", "organise", "organising", "rearrange",
    "hoover", "weed", "weeding", "tackle", "tackling", "file", "filing", "paperwork",
))

_COUNT_WORDS = frozenset("""
    one two three four five six seven eight nine ten eleven twelve dozen couple few several
    half single both
    """.split())

_NOT_THE_THING = frozenset((
    "not", "isnt", "isn't", "arent", "aren't", "wasnt", "wasn't", "no", "without", "non",
    "except", "besides", "bar", "minus", "other", "than", "rather", "instead", "nor", "never",
))

_BLOCK_QUALIFIERS = frozenset((
    "cheap", "free", "budget", "afford", "money", "quid", "pounds", "tenner", "fiver",
    "spare", "skint", "pennies", "cash", "nice", "quiet", "lazy", "relaxing",
    "broke", "broken", "poor", "brassic", "skint", "tight", "moneyless", "bust",
))


_AT_HOME = ("kitchen", "house", "flat", "home", "loft", "attic", "cellar",
            "living room", "dining room", "bedroom", "bathroom", "spare room",
            "conservatory", "study", "front room", "back room", "box room",
            "utility room", "hall", "hallway", "landing", "porch")
_AT_THE_PLACE_WORDS = ("in", "at", "on", "into", "inside", "around", "round")
_FOR_THE_PLACE_WORDS = ("for",)
_THE_OWNER = ("the", "my", "our", "your", "his", "her", "their")


def _the_place_the_block_is_at(said, block=False):
    words = re.findall(r"[a-z']+", str(said or "").lower())
    preps = set(_AT_THE_PLACE_WORDS) | (set(_FOR_THE_PLACE_WORDS) if block else set())
    here = set()
    for i, word in enumerate(words):
        if word not in preps:
            continue
        j = i + 1
        if j < len(words) and words[j] in _THE_OWNER:
            j += 1
        pair = " ".join(words[j:j + 2])
        if pair in _AT_HOME:
            here.update(pair.split())
        elif j < len(words) and words[j] in _AT_HOME:
            here.add(words[j])
    return here


def _names_the_free_block(named):
    words = [word for word in re.split(r"[^a-z0-9']+", str(named or "").lower()) if word]
    if not words:
        return True
    return all(word in _FREE_BLOCK_WORDS or word in _ASK_WORDS or word in _BLOCK_QUALIFIERS
               or word in _COUNT_WORDS for word in words)


def _covered_words(text, phrases):
    covered = {}
    left = " %s " % text
    for phrase in sorted(phrases, key=len, reverse=True):
        pattern = r"(?<![a-z0-9])%s(?![a-z0-9])" % re.escape(phrase)
        while re.search(pattern, left):
            left = re.sub(pattern, " ", left, count=1)
            for word in phrase.split():
                covered[word] = covered.get(word, 0) + 1
    return covered


_MUSING = re.compile(r"\b(?:i|we)\s+(?:suppose|guess|reckon|expect|think)\b"
                     r"|\b(?:maybe|perhaps|probably)\b[^.?!]*\b(?:i|we)\b")


def _names_a_thing_of_its_own(understood):
    words = {word.lower().replace("'", "") for word in (understood.get("keywords") or ())
             if isinstance(word, str)}
    if words & _JOB_WORDS:
        return False
    said = " %s " % str(understood.get("clean") or "").lower()
    if _MUSING.search(said):
        return False
    holds_block = bool(_covered_words(said, FREE_TIME + WEEK_OFF + _WORK_BLOCK)) or bool(
        set(re.findall(r"[a-z']+", said)) & FREE_TIME_TIME)
    here = _the_place_the_block_is_at(said, block=holds_block)
    shown = understood.get("subject")
    if isinstance(shown, str) and shown:
        left = " ".join(word for word in re.split(r"[^a-z0-9']+", shown.lower())
                        if word and word not in here)
        if left and not _names_the_free_block(left):
            return True
    covered = _covered_words(said, FREE_TIME + WEEK_OFF + FREE_TIME_ASK + _ASKS + _WORK_BLOCK)
    for word in understood.get("keywords") or ():
        if not isinstance(word, str):
            continue
        low = word.lower().replace("'", "")
        if (low in _FREE_BLOCK_WORDS or low in _ASK_WORDS or low in _BLOCK_QUALIFIERS
                or low in _COUNT_WORDS):
            continue
        if low.isdigit():
            continue
        if low in here:
            continue
        if covered.get(low):
            covered[low] -= 1
            continue
        if _said_as_the_thing_it_does_not_want(str(understood.get("clean") or ""), low):
            continue
        return True
    return False


def _said_as_the_thing_it_does_not_want(line, word):
    found = re.search(r"(?<![a-z0-9])%s(?![a-z0-9])" % re.escape(word.lower()), line.lower())
    if not found:
        return False
    before = line[:found.start()].lower().split()
    return bool(before[-2:] and set(before[-2:]) & _NOT_THE_THING)


def _free_time(memory, understood):
    said = " ".join(str(word).lower() for word in (understood.get("words") or []))
    clean = str(understood.get("clean") or "").lower()
    line = said + " " + clean
    if a_dish_is_already_the_plan(clean):
        return None
    if any(re.search(r"(?<![a-z0-9])" + re.escape(word) + r"(?![a-z0-9])", line)
           for word in _UNWELL):
        return None
    if _COLD.search(line) and not _COLD_WEATHER.search(line):
        return None
    if (any(phrase in line for phrase in _WHERE_GO_PHRASES)
            and any(word in line for word in MONEY_WORDS + _MONEY_ONLY + _WHEN_AWAY)):
        return None
    if any(phrase in line for phrase in _TRIP_PHRASES):
        return None
    if any(word in line for word in _MONTHS):
        return None
    if _a_city_is_named(line):
        return None
    if _dish_for_tonight(memory, understood):
        return None
    if any(phrase in line for phrase in _NOTE_ASK):
        return None
    if any(word in line for word in _EVENT_AWAY):
        return None
    if any(phrase in line for phrase in _EVENT_EVENING):
        return None
    if any(phrase in line for phrase in _MEDIUM_NAMED):
        return None
    if any(word in line for word in ("newborn", "new baby", "new-born", "just had a baby",
                                     "had a baby", "baby is due", "baby due", "paternity",
                                     "maternity leave", "on maternity")):
        return NEWBORN_WEEK
    if any(phrase in line for phrase in _REQUESTING_TIME):
        return None
    if (any(phrase in line for phrase in _WORK_BLOCK)
            and not _short_run(line)
            and not any(phrase in line for phrase in _ASKS)):
        return None
    if _ideas_about_a_thing(understood):
        return None
    if _about_a_thing_the_person_has(understood):
        return None
    if _names_a_thing_of_its_own(understood):
        return None
    if any(phrase in line for phrase in _GIFT_ASK):
        return None
    if any(word in line for word in ("this afternoon", "free afternoon", "afternoon off")):
        plan = DAY_PLAN
    elif any(word in line for word in ("day off", "days off", "free day")):
        plan = DAY_OFF_PLAN
    elif any(word in line for word in _THE_EVENING):
        plan = EVENING_PLAN
    elif ((_short_run(line)
           or any(word in line for word in ("few days", "couple of days")))
          and not any(word in line for word in ("week off", "a week off", "weeks off",
                                                "whole week", "week free"))):
        plan = DAY_PLAN
    elif any(word in line for word in WEEK_OFF):
        plan = WEEK_PLAN
    else:
        plan = WEEKEND_PLAN
    if plan is WEEK_PLAN and any(word in line for word in MONEY_WORDS + _MONEY_ONLY):
        plan = WEEK_PLAN_SKINT
    if plan is WEEK_PLAN:
        if any(word in line for word in ("summer", "hot", "heat", "sunny", "sunshine")):
            plan = plan + " " + SUMMER_WEEK
        elif any(word in line for word in ("winter", "autumn", "frost", "snow", "dark")):
            plan = plan + " " + WINTER_WEEK
    if any(word in line for word in MONEY_WORDS):
        plan = plan + " " + NO_MONEY
    return plan

_BABY_GEAR = (
    (("pram", "prams", "pushchair", "pushchairs", "buggy", "buggies", "stroller", "strollers",
      "travel system"), "pram",
     "A pram is £150 to £400 new and £60 to £150 second-hand, and what matters is that it "
     "folds into the car and lies flat for a newborn. A second-hand one is fine if the frame is "
     "straight, the brakes hold and the fabric washes."),
    (("carrier", "carriers", "sling", "slings", "baby carrier", "baby sling"), "carrier",
     "A carrier or sling is £30 to £90, and it is the easy one on a bus, on stairs and in the "
     "first weeks; a pram carries the shopping and the sleeping baby. Most people end up with "
     "both, a sling first and a pram from about three months."),
    (("cot", "cots", "cot bed", "cotbed", "crib", "cribs", "moses basket", "travel cot"), "cot",
     "A cot is £100 to £250 new and £30 to £80 second-hand. The cot itself can be second-hand, "
     "but the mattress has to be new and firm and fit with no gaps round the edge, 120 by 60cm "
     "for a cot and 140 by 70cm for a cot bed. A Moses basket is for the first months only."),
    (("car seat", "car seats", "carseat", "carseats", "i-size", "isofix", "infant carrier"),
     "car seat",
     "A car seat is £80 to £250 new and it is the one piece not to buy second-hand unless you "
     "know its history: a seat that has been in a crash may look fine and still be spent. i-Size "
     "(R129) is the newer standard, and how it fits your car matters more than the brand."),
    (("high chair", "highchair", "high chairs"), "high chair",
     "A high chair is £25 to £150 and it can wait until six months, so it is the one piece you "
     "leave: a £25 one that wipes clean and has a footrest does the job."),
    (("baby monitor", "monitor", "monitors"), "baby monitor",
     "A baby monitor is £30 to £120 and it is a comfort rather than a must: it does not stop "
     "anything happening, so a cheap audio one beside the cot is enough."),
)

_BABY_GEAR_FAULT = ("squeak", "squeaks", "squeaking", "squeaky", "sticking", "stuck", "jammed",
                    "jam", "wobbly", "loose", "broken", "broke", "snapped", "wont fold",
                    "won't fold", "wont push", "won't push", "dragging", "rusty", "rust",
                    "cracked", "torn", "rips", "ripped", "fraying", "buckle", "buckles",
                    "harness", "brake", "brakes", "wheel", "wheels", "axle", "axles", "handle")

_BABY_GEAR_MEND = ("Squeaking or sticking wheels are the axle: a drop of silicone spray or a dry "
                   "PTFE lubricant on each axle and the grit wiped off the wheels, and a brake "
                   "that will not hold wants its little spring or cable adjusting. A wobbly "
                   "handle is a bolt inside the frame to tighten, a torn hood or seat is a "
                   "replacement cover from the maker, and a bent frame is the one fault that "
                   "means a new pram rather than a mending job.")


def _gear_named(words):
    return [name for keys, name, _said in _BABY_GEAR if any(_has_word(words, key) for key in keys)]


def _has_word(words, word):
    return re.search(r"(?<![a-z0-9])" + re.escape(word) + r"(?![a-z0-9])", words) is not None


def _a_piece_of_baby_gear(memory, understood):
    words = _words_of(understood)
    named = _gear_named(words)
    fault = any(_has_word(words, word) for word in _BABY_GEAR_FAULT)
    if fault and not named:
        carried = (memory or {}).get("topic") or {}
        topic = str(carried.get("text") or "").lower()
        named = _gear_named(topic)
    if fault and named:
        return _BABY_GEAR_MEND
    if len(named) >= 2 and ("which" in words or "better" in words or " or " in " %s " % words
                            or "versus" in words or "vs" in words):
        said = {name: sentence for _keys, name, sentence in _BABY_GEAR}
        pair = " ".join(said[name] for name in named[:2])
        return ("Whichever you use most is the one to spend on. " + pair).strip()
    if len(named) == 1:
        for keys, name, sentence in _BABY_GEAR:
            if name == named[0]:
                return sentence
    return ("Buy second-hand for all of it except the mattress: a cot (mattress 120 by 60cm) or "
            "cot bed (140 by 70cm) with a new firm mattress that fits with no gaps, a car seat "
            "that has not been in a crash and whose history you know - i-Size (R129) is the newer "
            "standard, and how it fits your car matters more than the brand - and a pram that "
            "folds small enough for your car and lies flat for a newborn. Prices: a new pram "
            "£150 to £400, second-hand £60 to £150, a cot £100 to £250 new. You need little "
            "else at the start (six babygros in two sizes, nappies, muslins); a monitor is a "
            "comfort rather than a must, and a high chair can wait until six months.")


def _words_of(understood):
    parts = [(understood or {}).get("clean"), (understood or {}).get("text")]
    parts.extend((understood or {}).get("words") or ())
    return " ".join(str(part) for part in parts if part).lower()


def _dish_for_tonight(memory, understood):
    said = _words_of(understood)
    found = []
    for aliases, keys, body, avoid in RECIPES:
        if not any(re.search(r"\b" + re.escape(alias) + r"\b", said) for alias in aliases):
            continue
        if any(re.search(r"\b" + re.escape(word) + r"\b", said) for word in avoid):
            continue
        found.append((max(len(alias) for alias in aliases
                          if re.search(r"\b" + re.escape(alias) + r"\b", said)), body))
    if not found:
        return None
    return max(found, key=lambda pair: pair[0])[1]
_ADULT_PARTY = (
    "Count the people first, because it decides the room and the food: 8 to 12 is easy to cook "
    "for at home, 30 to 40 is about as many as a house takes, and a pub's back room or a "
    "restaurant takes 20 to 60 for a similar price to a hall. Pick the day and send one message "
    "with the date, time, place and whether it is a meal or drinks, because \"let me know if you "
    "can make it\" gets half-answers. Keep the food to things made the day before - a pie or a "
    "chilli kept warm, a baked ham, bread, two salads and a bought cake - and give two people one "
    "job each, drinks and cards and the speech, so you are not doing all of it. Send the "
    "invitations three to four weeks ahead, six for a big do or a date near Christmas, and ask for "
    "replies by a date a week before. Budget £10 to £15 "
    "a head for a buffet at home and £25 to £40 in a restaurant's back room, drink on top.")

_KIDS_PARTY = (
    "Two hours and about age-plus-one guests is the sweet spot: one venue or one big activity, "
    "food that can be made the day before, and a bag for the way home. At home it costs around "
    "£5 a head but you need a wet-weather plan and one adult per four children; a hall or "
    "soft-play party at £10 to £15 a head buys you both.")

_CHILD_AT_PARTY = ("kid", "kids", "child", "children", "childs", "toddler", "toddlers",
                   "son", "sons", "daughter", "daughters", "grandson", "granddaughter",
                   "grandchild", "grandchildren", "godson", "goddaughter", "school",
                   "nursery", "soft play", "playcentre", "reception class", "year one")
_AGE_AT_PARTY = re.compile(r"\b(\d{1,2})(?:st|nd|rd|th)?\b")

_A_MILESTONE_PERSON = re.compile(
    r"\b(?:mum|mums|mom|moms|mam|mams|dad|dads|father|mother|nan|nans|nana|nan's|gran|grans|"
    r"granny|grandma|grandad|grandpa|grandmother|grandfather|aunt|auntie|uncle|sister|brother|"
    r"wife|husband|partner|mother in law|father in law|she|he|son|sons|daughter|daughters|"
    r"grandson|granddaughter|grandchild|godson|goddaughter|nephew|niece|kid|kids|child|children)\b")
_A_CHILD_AT_A_MILESTONE = re.compile(
    r"\b(?:son|sons|daughter|daughters|grandson|granddaughter|grandchild|godson|goddaughter|"
    r"nephew|niece|kid|kids|child|children|boy|girl|toddler)\b")
_A_MILESTONE_AGE = re.compile(
    r"\b(?:is|turns|turning|will be|going to be|hits|becomes)\s+(?:the age of\s+)?(\d{1,2})\b")
_A_MILESTONE_SOON = re.compile(
    r"\b(?:next (?:week|month|weekend|saturday|sunday|friday|year)|this (?:week|weekend)|"
    r"on (?:monday|tuesday|wednesday|thursday|friday|saturday|sunday)|soon|coming up|"
    r"in \w+ (?:weeks|days))\b")


_A_PRESENT_ASKED = re.compile(
    r"\b(?:present|presents|gift|gifts)\b"
    r"|\bwhat\s+(?:should|shall|can|could|do|would)\s+(?:i|we)\s+(?:get|buy|give|make|send)\b"
    r"|\b(?:get|buy|give|make|send)\s+(?:her|him|them|my\s+(?:mum|mom|mother|dad|father|"
    r"gran|grandma|grandad|granny|nan|nana|wife|husband|partner|son|daughter|sister|brother|"
    r"friend|parents?))\b"
    r"|\bideas?\s+(?:for|of)\s+(?:a\s+)?(?:present|gift)\b")


_MILESTONE_AGES = tuple(range(1, 100))
_MILESTONE_SAID = tuple("%s %d" % (verb, years)
                        for years in _MILESTONE_AGES
                        for verb in ("is", "turns", "turning", "will be"))


def _a_milestone_said_as_an_age(understood):
    line = " ".join([str((understood or {}).get("clean") or "")]
                    + [str(word) for word in ((understood or {}).get("words") or ())]).lower()
    if not _A_MILESTONE_PERSON.search(line):
        return False
    age = _A_MILESTONE_AGE.search(line)
    if not age:
        return False
    years = int(age.group(1))
    if years < 18 and not _A_CHILD_AT_A_MILESTONE.search(line):
        return False
    if _A_PRESENT_ASKED.search(line):
        return False
    return bool(_A_MILESTONE_SOON.search(line))


def _party_plan(memory, reading):
    clean = str((reading or {}).get("clean") or "").lower()
    words = " ".join(str(word) for word in ((reading or {}).get("words") or ()))
    line = clean + " " + words
    ages = [int(found) for found in _AGE_AT_PARTY.findall(line) if 1 <= int(found) <= 99]
    if ages:
        return _KIDS_PARTY if min(ages) < 13 else _ADULT_PARTY
    if any(re.search(r"\b" + word + r"\b", line) for word in _CHILD_AT_PARTY):
        return _KIDS_PARTY
    return _ADULT_PARTY


def _not_a_gift_ask(understood):
    line = " " + str((understood or {}).get("clean") or "").lower() + " "
    line += " ".join(str(word).lower() for word in ((understood or {}).get("words") or ())) + " "
    return not any(phrase in line for phrase in _GIFT_ASK)


def _not_a_gift_or_a_date(understood):
    return _not_a_gift_ask(understood) and _not_a_date_question(understood)


_KITCHEN_PLAN = (
    "Plan a kitchen round the three points that get used most - the sink, the hob and the fridge: "
    "any two of them want 1.2 to 2.7 metres between them, the sink wants a clear 600mm of worktop "
    "on each side, and the hob wants space to put a pan down on the right and nothing flammable "
    "beside it. Then list what you need before what you want: deep drawers beat a bottom cupboard, "
    "a socket every metre of worktop, a tall cupboard for the ironing board and the hoover. Mark "
    "where the pipes, the soil stack and the door swing are before you fall in love with a layout, "
    "because moving a drain is most of a kitchen's cost. Tape the outline on the floor and walk it "
    "for a week before you order.")

_BATHROOM_PLAN = (
    "Plan a bathroom round the soil pipe: the toilet has to stay where the drain already is unless "
    "you raise the floor for a new one, so put the toilet and the bath first and the basin where "
    "there is wall for it. A bath needs 1.7m and a shower 900mm square, and leave 700mm clear in "
    "front of the basin and 600mm beside the toilet. Decide the shower before the tiles, because a "
    "wet room floor has to fall to a drain and a screen cannot be added later, and set the shower "
    "valve about 1.1m off the floor so nobody has to reach. A bathroom also needs an extractor that "
    "moves about 15 litres a second, or the paint and the grout will go.")


_UTILITY_PLAN = (
    "Plan a utility room round the machines and the water: the washing machine and the dryer "
    "want an outside wall for the vent and the plumbing, a sink close to the drain, and a "
    "worktop over the appliances at about 900mm so there is a surface to fold on. Leave 600mm "
    "clear in front of every door you have to open, put the boiler behind a cupboard you can "
    "still get into, and keep a shelf at eye height for powder, pegs and the iron - it is the "
    "walk-through clutter, not the size of the room, that makes a utility room useless.")


_A_PLANNED_ROOM = ("kitchen", "kitchens", "bathroom", "bathrooms", "bath", "baths", "shower",
                   "showers", "toilet", "toilets", "loo", "loos", "ensuite", "en suite",
                   "wet room", "utility", "utility room", "laundry", "laundry room",
                   "boot room", "small room", "spare room", "dining room")


def _a_room_plan(memory, understood):
    said = str((understood or {}).get("clean") or (understood or {}).get("text") or "").lower()
    if not re.search(r"(?<![a-z0-9])(?:" + "|".join(re.escape(word) for word in _A_PLANNED_ROOM)
                     + r")(?![a-z0-9])", said):
        return None
    if any(word in said for word in ("utility", "laundry", "boot room")):
        return _UTILITY_PLAN
    if any(word in said for word in ("bath", "bathroom", "shower", "toilet", "loo", "ensuite",
                                     "wet room")):
        return _BATHROOM_PLAN
    return _KITCHEN_PLAN


ENTRIES = [
    entry("free-time-plan",
      (FREE_TIME,
       ("do", "doing", "go", "going", "ideas", "idea", "suggestions", "something", "anything",
        "plan", "plans", "bored", "nothing", "saturday", "sunday",
        "tips", "tip", "advice", "suggest",
        "days off", "day off", "time off", "off work",
        "weekend free", "long weekend", "weekend to myself",
        "summer", "winter", "spring", "autumn", "no plans", "well", "use", "spend", "sort")),
      _free_time,
      ask=FREE_TIME_ASK, bias=2,
      guard=_a_stretch_of_time_to_fill,
      avoid=("cook", "cooking", "recipe", "dinner", "tea", "lunch", "breakfast", "bake",
             "shop", "shopping", "supermarket", "kids", "children", "toddler", "baby",
             "car", "mot", "van", "garage", "boiler", "washing machine", "essay",
             "coursework", "assignment", "deadline", "tax return", "invoice",
             "homework", "revise", "revision", "exam", "at work", "office", "shift",
             "overtime", "rota",
             "weather", "rain", "forecast", "train", "bus", "flight", "traffic",
             "ache", "aches", "aching", "pain", "toothache", "tooth", "hurt", "hurts",
             "ill", "sick", "fever", "temperature", "rash", "dizzy", "dentist", "doctor",
             "pharmacy", "hospital", "symptom", "symptoms", "headache",
             "left", "leftover", "leftovers", "left over", "use up", "using up", "with it",
             "with them", "with these", "goes off", "go off", "out of date",
             "there", "trip", "break away", "visit", "visiting", "hotel", "city", "abroad",
             "travel", "flights", "in rome", "in paris", "in london", "in new york",
             "weekend away", "weekend break", "city break", "city breaks", "night away",
             "nights away", "mini break", "short break", "getaway", "days away",
             "couple of nights", "few nights away", "two nights away", "weekend in",
             "feel low", "feeling low", "feel really low", "feeling really low",
             "feel down", "feeling down", "feel really down", "feeling really down",
             "feel sad", "feeling sad", "feel depressed", "feeling depressed", "depressed",
             "feel anxious", "feeling anxious", "anxious", "feel lonely", "feeling lonely",
             "lonely", "feel miserable", "feeling miserable", "miserable",
             "feel rubbish", "feeling rubbish", "feel awful", "feeling awful",
             "feel terrible", "feeling terrible", "feel like crying", "cant be bothered",
             "no energy", "hate everything",
             "can i have", "can i take", "can i book", "can i get", "could i have", "could i take",
             "may i have", "may i take", "am i allowed", "is it ok if i", "is it okay if i",
             "do i have to book", "my boss", "my manager", "ask for it off",
             "take a day off", "take a week off", "take time off", "take some time off",
             "book a day off", "book a week off", "book time off", "want to take", "want to book",
             "request a day off", "request a week off", "request time off", "put in for",
             "hoping to take", "hoping to book",
             ) + A_HOURS_ASK),

    entry("move-house-plan",
          (("moving house", "moving home", "moving flat", "moving out", "house move",
            "move house", "move flat", "moving next month", "packing up the house",
            "move to a new house", "move to a new flat", "move into a new house",
            "move into a new flat", "move into my first",
            "how do i move house", "how do i move home", "how do i move flat",
            "how do i move out", "how to move house", "how to move home",
            "how do i move to a new house", "how do i move to a new flat",
            "what do i need to move house", "what do i need to move home",
            "when moving", "when we move", "when i move", "when you move", "if we move",
            "plan a move", "planning a move", "plan the move", "planning the move",
            "organise a move", "organising a move", "organize a move", "organizing a move",
            "a move to plan", "before a move", "before the move", "the move go",
            "prepare for a move", "prepare to move", "get ready for a move",
            "get ready to move", "ready for a move", "start with a move",
            "start on a move", "start with moving", "sort out a move",
            "moving out of my", "moving out next"),
           ("plan", "planning", "start", "organise", "organize", "checklist", "prepare",
            "sorted", "first", "ahead", "organise", "where do i", "tips", "advice",
            "move", "moving", "moved")),
          "Work back from the date: book a van or removals six to eight weeks out, and tell the "
          "council, energy, water and broadband a month before, because the bills follow you. Box "
          "the things you don't use three weeks out, label every box with its room, and pack one "
          "bag with a kettle, mugs, loo roll, bedding and chargers for the first night.", ask=PLAN_ASK,
          guard=_a_household_move_or_a_named_move,
          avoid=("council", "doctor", "gp", "surgery", "dentist", "school", "register",
                 "council tax", "notify",
                 "cheap", "cheaper", "cheapest", "cheaply", "cost", "costs", "price", "how much",
                 "van", "removals", "man with a van",
                 "hoping", "hopin", "hope to move", "hopin to move", "hopes to",
                 "thinking of moving", "thinking about moving", "dream of moving",
                 "dreaming of moving", "want to move out", "cant wait to move",
                 "tell my landlord", "tell the landlord", "landlord", "landlady",
                 "letting agent", "notice period", "give notice",
                 "can't wait to move", "one day",
                 "my back", "back is killing", "back hurts", "bad back", "sore back",
                 "pulled my back", "hurt my back", "done my back",
                 "pack", "packing", "packed", "boxes", "box up", "label", "labels",
                 "bubble wrap", "what to pack", "declutter", "unpack",
                 "how do i tell", "how to tell", "how do i explain", "what do i say",
                 "tell the kids", "tell my kids", "tell the children", "tell my children",
                 "tell my son", "tell my daughter", "break the news", "explain to my",
                 "how do i break",
                 "with kids", "with children", "with a baby", "with a toddler", "with a child",
                 "my kids", "my children", "my son", "my daughter", "pregnant", "my baby",
                 "toddler", "toddlers", "kids", "children",
                 "with my partner", "with a partner", "move in with", "moving in with",
                 "moved in with", "move into his", "move into her", "my girlfriend",
                 "my boyfriend", "my partner")),

    entry("birthday-date",
          (("when is", "when's", "whens", "what date", "which date", "what day"),
           ("birthday", "birthdays")),
          "I can't look a birthday up, and guessing one is worse than asking: a text now, and the "
          "answer goes in your phone with a reminder a week before. People rarely mind being "
          "asked.",
          avoid=("party", "parties", "invite", "invites", "invitations", "present", "presents",
                 "gift", "gifts", "buy", "plan", "planning", "many", "venue", "cake", "food",
                 "guest", "guests", "surprise", "ideas", "organise"),
          bias=1),

    entry("party-milestone",
          (_MILESTONE_SAID,
           ("do", "doing", "what", "how", "should", "could", "can we", "ideas", "any",
            "anything", "something", "plan", "planning", "organise", "help", "sort", "get",
            "make", "give")),
          _party_plan, ask=PLAN_ASK, guard=_a_milestone_said_as_an_age, bias=1,
          avoid=("years old", "year old", "miles", "years", "kg", "degrees")),

    entry("party-grownup",
          (("birthday party", "birthday for", "party for my", "party for her", "party for him",
            "surprise party", "anniversary party", "retirement party", "retirement do",
            "big birthday", "40th", "50th", "60th", "65th", "70th", "75th", "80th", "90th",
            "my mums birthday", "my dads birthday", "my mums 60th", "mums 70th",
            "a party", "the party", "house party", "party at home", "birthday", "birthdays",
            "invite to a party", "people to invite", "how many to invite", "guest list",
            "invitations", "the invitations", "send invitations", "send the invitations",
            "my nans birthday", "my nans 80th", "my grans birthday", "nans 80th", "grans 80th",
            "her 80th", "her 70th", "her 90th", "his 70th", "his 80th", "for her birthday",
            "for his birthday", "what can we do for",
            "leaving do", "leaving party", "retirement do", "work do", "christmas do"),
           ("plan", "planning", "start", "first", "organise", "organized", "invite", "how many",
            "how much", "food", "venue", "where", "ideas", "tips", "advice", "sorted",
            "guests", "guest list", "party",
            "do", "doing", "what", "how", "should", "want", "wanted", "throwing", "throw",
            "hosting", "host", "send", "sent", "when", "what can we do", "we do")),
          _party_plan, ask=PLAN_ASK,
          avoid=(
                 "annual leave", "days leave", "day leave", "much leave", "leave days",
                 "leave left", "leave balance", "leave allowance", "leave entitlement",
                 "holiday entitlement", "days off", "annual leave entitlement",
                 "end a chat", "end the chat", "end a conversation", "end the conversation",
                 "chat at a party", "conversation at a party", "small talk", "stop talking",
                 "get out of a conversation", "nattering",
                 "get out of", "dont want to go", "don't want to go", "do i have to go",
                 "cant come", "can't come", "make my excuses", "would rather not go",
                 "decline", "turn down", "say no", "back out of", "not going",
                 "kids party", "children's party", "childs party", "toddler party", "soft play",
                 "conversation", "conversations", "chat", "excuse myself", "cornered",
                 "mingle", "mingling",
                 "remember", "remembering", "forget", "forgetting", "forgot", "keep track",
                 "track of", "reminder", "reminders", "calendar", "diary", "list of birthdays",

                 "playcentre", "kids", "kid", "child", "children", "year old", "years old",
                 "5th", "6th", "7th", "8th", "9th", "10th", "11th", "12th",
                 "toddler", "toddlers", "nursery", "school", "dinner party", "buffet for",
                 "people coming over", "christmas party", "office party", "political",
                 "party wall", "hen do", "stag do", "wedding", "baby shower", "christening",
                 "present", "presents", "gift", "gifts", "buy", "buying", "bought", "get her",
                 "get him", "get my", "get our", "card", "cards", "what to write",
                 "wear", "wearing", "put on", "putting on", "dress", "dress code", "outfit",
                 "outfits", "shoes", "what to get",
                 _A_PRESENT_FOR,
                 "what should i write", "what do i write",
                 "write in", "writing in", "message", "messages", "verse", "verses", "poem",
                 "poems", "wishes", "what to say", "what do i say",
                 "say goodbye", "say goodbyes", "goodbye", "goodbyes", "say bye",
                 "leave the party", "leave a party", "leaving the party", "leaving a party",
                 "leave early", "leaving early", "slip away", "say my goodbyes", "head off",
                 "make my excuses", "when to leave", "how do i leave",
                 "what should i cook", "what to cook", "what should i make", "what food should i",
                 "what can i cook", "what can i make", "what should i serve", "what to make",
                 "what shall i cook", "what do i cook",
                 "card", "cards", "write in", "write on", "what to write", "what should i write",
                 "message in", "note in", "sign the",
                 "buy my", "get a", "buy a", "get for", "buy for",
                 "what should i get", "what do i get", "what can i get", "what shall i get",
                 "what could i get", "what would i get", "get them", "give them",
                 "something for", "present for", "gift for",
                 "game", "games", "board game", "board games", "party game", "party games",
                 "what should we play", "something to play", "quiz", "games night"),
          bias=1,
          guard=lambda u: _not_a_gift_or_a_date(u) and _not_a_deed_of_their_own(u)),
    entry("party-kids",
          (("kids party", "children's party", "childs party", "birthday party",
            "birthday for", "party for a", "5th birthday", "6th birthday", "7th birthday",
            "8th birthday", "toddler party", "how many kids", "how many children",
            "invite to a birthday"),
           ("plan", "planning", "start", "idea", "ideas", "much", "activities", "food",
            "venue", "where", "organise", "invite", "cost", "decorate", "theme", "games",
            "cake", "guests", "party", "birthday", "toddler", "activities")),
          _KIDS_PARTY, ask=PLAN_ASK, guard=_not_a_count_of_their_own,
          avoid=("my mum", "my mom", "my dad", "my mother", "my father", "my husband",
                 "my wife", "my partner", "grandma", "grandad", "nana", "nan", "granny",
                 "40th", "50th", "60th", "65th", "70th", "75th", "80th", "90th",
                 "retirement", "anniversary", "grown up", "for adults",
                 "card", "cards", "message", "messages", "wishes", "what to write",
                 "what should i write", "what do i write", "write in", "message in",
                 "what food should i bring", "what food should i take", "what food can i bring",
                 "what food can i take", "what food do i bring", "what food to bring",
                 "bring a dish", "dish to bring", "food to bring", "what should i bring",
                 "what can i bring", "anything i can bring")),

    entry("wedding-plan",
          (("wedding", "weddings", "marriage", "civil partnership", "getting married",
            "marry", "marrying", "engagement party", "hen do", "stag do",
            "get married", "married", "we are getting married", "give notice",
            "notice of marriage", "notice to marry", "wedding day",
            "book the venue", "book a venue", "the wedding venue",
            "book the photographer", "book a photographer"),
           ("plan", "planning", "budget", "guest list", "guests", "afford", "cheap",
            "start", "organise", "venue", "save",
            "first", "sort", "sort first", "sort out first", "pick", "pick first", "order",
            "prioritise", "priorities", "before what",
            "what do i need", "need to do", "whats needed", "what's needed", "paperwork",
            "papers", "document", "documents", "bring", "what to bring",
            "notice", "notice of marriage", "registrar", "register office", "legal", "admin",
            "witness", "witnesses", "arrange",
            "how do i get married", "how do we get married", "how to get married",
            "how do you get married", "how do i marry", "how do we marry",
            "how do i arrange", "how do we arrange", "what do i do", "what do we do",
            "what do i need to do", "where do i start", "how does it work",
            "how many guests", "how many people", "how many should we invite",
            "how many to invite", "number of guests", "how big", "size of the wedding",
            "far ahead", "how early", "how long before", "lead time", "how soon",
            "when should we book", "when to book", "book the venue", "book a venue",
            "book the photographer", "book a photographer", "book the registrar",
            "book the venue", "book a venue", "the wedding venue",
            "the photographer", "a photographer")),
          _wedding_plan,
          ask=PLAN_ASK + _WEDDING_ASK + ("how many", "how far", "how long", "how soon", "how big",
                                         "when", "count"),
          bias=1,
          avoid=("cost", "costs", "how much", "price", "prices", "spend", "\u00a3",
                 "wear", "wearing", "outfit", "outfits", "dress", "dresses", "jumpsuit",
                 "jumpsuits", "hat", "hats", "fascinator", "shoes", "heels", "tie",
                 "colour", "color", "dress code", "black tie",
                 "landlord", "landlords", "landlady", "letting agent", "letting agents",
                 "tenancy", "tenancies", "tenants", "my flat", "my lease", "the flat",
                 "rent", "notice period", "evict", "deposit",
                 "already booked", "havnt booked", "havent booked", "got the venue",
                 "venue booked")),

    entry("wedding-food",
          (("wedding", "weddings", "wedding breakfast", "wedding reception", "reception",
            "getting married", "we are getting married", "marrying", "barn wedding",
            "wedding day", "big day", "the wedding", "our wedding", "my wedding",
            "for a wedding", "a wedding"),
           ("food", "menu", "menus", "cater", "caters", "catering", "caterer", "caterers",
            "buffet", "meal", "meals", "eat", "eating", "feed", "feeding", "supper", "dinner",
            "breakfast", "hog roast", "barbecue", "bbq", "canapes", "finger food", "serve",
            "serving", "cook", "cooking", "drinks", "what should we eat", "what do we eat",
            "sit down", "sit-down", "plated")),
          "Decide the shape before the menu: a sit-down meal is about £35 to £60 a head catered "
          "and a buffet or hog roast about £20 to £35, while doing it yourselves lands near £10 "
          "to £15 a head and costs you the day. Work back from the number of guests - 60 people "
          "is a caterer's job unless you have a big kitchen and willing help - and ask the venue "
          "first, because many barns and halls either insist on their own list or charge corkage "
          "and a kitchen fee. Book six to nine months ahead for a summer Saturday, put dietary "
          "needs on the reply card, and plan evening food if the day runs past nine: something "
          "hot and cheap at 9pm saves a long hungry evening.",
          ask=PLAN_ASK + ("food", "menu", "cater", "caterer", "caterers", "catering", "buffet",
                          "eat", "feeds", "feed", "serve", "serving", "need", "needs",
                          "what do we", "what should we", "guests"),
          avoid=("gift", "gifts", "present", "presents", "notice", "registrar",
                 "register office", "witness", "witnesses", "wear", "wearing", "outfit",
                 "dress code", "speech", "photographer", "flowers", "music", "playlist",
                 "band", "dj", "first dance", "honeymoon", "thank you card"),
          bias=2),
    entry("wedding-timings",
          (("wedding", "weddings", "wedding day", "ceremony", "reception", "wedding breakfast",
            "getting married", "we are getting married", "big day", "marrying",
            "the invite", "the invitation", "on the invite", "on the invitation",
            "what time on the invite", "order of the day"),
           ("what time", "when should", "what time should", "order of the day", "timetable",
            "timeline", "schedule", "run order", "running order", "how early",
            "how long does the day", "how long does it last", "how long is the ceremony",
            "how long do we need", "how long should the day",
            "long does the day", "how long is the day", "day last", "whole day", "day go on",
            "how long do guests", "how long are guests", "long does a wedding",
            "long is a wedding", "wedding last", "how long the day",
            "what time do people",
            "what time do you", "what time is usual", "usual time", "start time", "what hour")),
          "The time on the invite is the ceremony time, not the time to arrive: guests should be "
          "there 20 to 30 minutes before, so say the ceremony time and let the venue tell people "
          "when to turn up. A ceremony runs about 30 minutes, then drinks and photographs for an "
          "hour to ninety minutes while the room is turned round, then the meal - which takes "
          "about two hours with speeches after it. Evening guests usually come from 7pm, and the "
          "first dance follows the evening food. Work backwards from the meal, because caterers "
          "want the room by a set time, and leave 20 minutes of slack: a late registrar cannot "
          "be made up.",
          ask=PLAN_ASK + ("what time", "when", "order", "timetable", "timeline", "schedule",
                          "run order", "running order", "usual"),
          avoid=("gift", "gifts", "present", "presents", "notice", "registrar",
                 "register office", "witness", "witnesses", "wear", "wearing", "outfit",
                 "dress code", "speech", "honeymoon", "food", "menu", "catering", "buffet",
                 "venue", "cost", "how much",
                 "ago", "how long ago", "how old", "already been",
                 "hotel", "hotels", "guesthouse", "guest house", "b&b", "a room", "rooms",
                 "flight", "flights", "travel", "parking", "taxi"),
          bias=1),
    entry("renovation-plan",
          (("renovation", "renovating", "extension", "building work", "new kitchen",
            "new bathroom", "rewire", "refurb", "doing up", "do up the house", "knock through",
            "kitchen", "kitchens", "bathroom", "bathrooms"),
           ("plan", "planning", "start", "quote", "quotes", "architect", "order", "first",
            "organise", "cost", "timeline", "how long", "permission")),
          "Get three quotes on the same written scope, and don't start until you have the money "
          "for the whole job plus 15% for what the walls hide. Order the kitchen or bathroom six "
          "to eight weeks before you need it, because that is the delay everyone hits, and put the "
          "start date and the payment stages in a contract rather than agreeing them by text.", ask=PLAN_ASK,
          avoid=("clean", "cleans", "cleaning", "cleaned", "tidy", "tidies", "tidying",
                 "scrub", "scrubbing", "hoover", "hoovering", "vacuum", "vacuuming",
                 "mop", "mopping", "dust", "dusting", "wipe", "wiping", "wash",
                 "washing up", "bleach", "disinfect", "smell", "smells", "smelly",
                 "mould", "mold", "damp")),

    entry("room-plan",
          (("kitchen", "kitchens", "new kitchen", "bathroom", "bathrooms", "new bathroom",
            "utility room", "laundry room", "refurb", "refit", "redo"),
           ("plan", "planning", "planned", "lay out", "layout", "design", "designing",
            "redesign", "work triangle", "where do things go", "where should things go",
            "how should i lay", "how do i arrange", "rearrange", "sizes", "measurements",
            "what size", "get it right")),
          _a_room_plan,
          avoid=("cost", "costs", "how much", "price", "prices", "quote", "quotes", "cheap",
                 "cheapest", "budget", "afford", "builder", "builders", "architect", "permission",
                 "planning permission", "how long", "timeline", "contractor", "contractors",
                 "clean", "cleaning", "tidy", "mess", "messy", "hoover", "scrub"),
          bias=1),

    entry("baby-plan",
          (("baby", "pregnant", "pregnancy", "newborn", "due date", "nursery"),
           ("plan", "planning", "prepare", "preparing", "need", "needs", "buy", "buying",
            "hospital bag", "nesting", "ready for the baby", "before the baby", "shopping list",
            "organise", "cot", "pram", "car seat")),
          "Buy very little in advance: a car seat, a cot or Moses basket with a firm new mattress, "
          "a pram, six babygros in two sizes, nappies and whatever you're feeding with. Put the cot "
          "in your room, empty, with no bumpers or pillows, and pack the hospital bag at 36 weeks "
          "with snacks and a long phone charger — everyone forgets the charger.", ask=PLAN_ASK,
          avoid=("sleep", "sleeping", "hurt", "hurts", "pain", "aching", "feed", "feeding",
                 "formula", "temperature", "fever", "cold", "cough", "sick", "ill",
                 "health visitor", "jar", "jars", "pouch", "pouches", "puree", "purees",
                 "baby food", "food", "eat", "eating", "eats", "meal", "meals", "weaning",
                 "breakfast", "lunch", "dinner", "snack", "snacks", "milk")),

    entry("baby-gear",
          (("pram", "prams", "pushchair", "pushchairs", "buggy", "buggies", "cot", "cots",
            "moses basket", "car seat", "car seats", "bouncy chair", "high chair", "highchair",
            "travel cot", "crib", "cotbed", "cot bed", "nursery furniture", "baby monitor"),
           ("buy", "buying", "get", "getting", "need", "needs", "which", "what about", "best",
            "cheap", "cheapest", "second hand", "secondhand", "second-hand", "new", "safe",
            "worth", "shop", "shopping", "borrow", "hand me down", "choose", "recommend",
            "compare", "price", "cost", "much", "how much",
            "squeak", "squeaks", "squeaking", "squeaky", "sticking", "stuck", "jammed",
            "wobbly", "broken", "broke", "snapped", "wont fold", "won't fold", "wont push",
            "won't push", "brake", "brakes", "wheel", "wheels", "fix", "mend", "repair")),
          _a_piece_of_baby_gear,
          avoid=("sleep", "sleeping", "wont sleep", "hurt", "hurts", "pain", "aching", "feed",
                 "feeding", "formula", "temperature", "fever", "cold", "cough", "sick", "ill",
                 "reflux", "colic", "teething", "rash", "health visitor", "cat", "cats", "dog",
                 "dogs", "pregnant", "pregnancy", "labour", "hospital bag",
                 "clean", "cleaning", "stain", "stains", "stained", "spill", "spills", "spilt",
                 "spilled", "smell", "smells", "smelly", "stinks", "vomit", "wash", "washing",
                 "dirty", "mould", "mold", "wipe", "scrub", "dry", "drying",
                 "out of", "out the", "off a", "off my", "off the", "off our", "off his",
                 "off her", "got it on", "got on the", "soaked", "spilled on",
                 "smoke", "smoky", "cigarette", "cigarettes", "odour", "valet", "get rid",
                 "sick in",
                 "coat", "coats", "jacket", "jackets",
                 "afford", "affords", "affording", "can i afford", "save up", "saving up",
                 "savings", "budget", "budgeting", "pay for it", "installments",
                 "instalments", "on finance", "payment plan"),
          bias=1),

    entry("pram-buy",
          (("pram", "prams", "pushchair", "pushchairs", "buggy", "buggies", "travel system",
            "travel systems", "stroller", "strollers"),
           ("buy", "buying", "bought", "which", "what", "best", "choose", "choosing",
            "look for", "look out for", "worth", "recommend", "new", "second hand",
            "secondhand", "second-hand", "cheap", "price", "cost", "get", "need",
            "better", "worse", "bigger", "smaller")),
          "Lay it flat first: a newborn needs a carrycot or a seat that goes properly flat, and "
          "after that the fold and the boot decide it - fold it one-handed in the shop and lift it "
          "into your own boot before you pay. Check the brake holds on a slope with the child in "
          "it, that the handle suits your height, and that the wheels are big enough for the "
          "pavement you actually walk on. A new one is \u00a3150 to \u00a3400 and a good second-hand "
          "pram is \u00a360 to \u00a3150, which is the better buy; the car seat is the one piece worth "
          "buying new, or with a history you know.",
          avoid=("fold", "folding", "folded", "stuck", "clean", "cleaning", "wash", "washing",
                 "stain", "stains", "smell", "smells", "mould", "mold", "repair", "fix",
                 "bus", "plane", "airport", "safe to", "car seat", "isofix", "wont sleep",
                 "sleep", "reflux", "colic",
                 "carrier", "carriers", "sling", "slings", "or a carrier", "or a sling",
                 "where can i", "where to buy", "where do i buy", "which shop",
                 "cheapest place", "shop"),
          bias=2),

    entry("holiday-countdown",
          (("holiday", "trip", "flight", "flights", "fly to", "flying to", "flying out",
            "going abroad", "abroad", "vacation", "travel insurance", "passport", "airport"),
           ("plan", "planning", "prepare", "countdown", "organise", "checklist",
            "need to do", "what do i need", "sort out", "still to do",
            "book first", "first", "where do i start", "where to start", "how do i start",
            "start with")),
          "Two months out: check the passport has six months left on it, book what sells out, and "
          "take the insurance out the day you book, so a cancellation is covered. Two weeks out: "
          "repeat prescriptions, any jabs the country wants, and a card that works abroad; a week "
          "out, send copies of the passport and insurance to someone at home.", ask=PLAN_ASK,
          avoid=("coach trip", "coach journey", "train journey", "train ride", "train trip",
                 "bus trip", "bus journey", "on a train", "on the train", "on a coach",
                 "for hours", "long journey")),

    entry("declutter-plan",
          (("declutter", "clear out", "clearout", "big tidy", "tidy up the house", "loft",
            "garage", "spare room", "wardrobe clear",
            "hire a skip", "skip hire", "a skip", "skip for", "full of junk", "junk",
            "clutter", "clear the clutter", "clear clutter", "messy house", "tidy my house",
            "tidy up my house", "clear my desk", "clear a room", "clear the room",
            "tidy my flat", "tidy the flat", "tidy my home", "tidy the house",
            "tidy my whole house", "tidy the whole house",
            "too much stuff", "clear the house",
            "rid of", "the mess", "mess everywhere", "clear the mess",
            "too much clutter", "sort the house out", "sort the house"),
           ("plan", "planning", "start", "where", "first", "organise", "how", "much time",
            "weekend", "sorted",
            "hire", "should", "suppose", "then", "worth", "need", "full", "rubbish", "junk",
            "clear out", "declutter", "rid of", "stuff", "mess", "too much", "sort")),
          "One room at a time, three bags on the floor — bin, donate, keep — and the donate bags go "
          "to the car the same day or they drift back. Ten minutes a day beats a lost weekend, and "
          "start with the room you walk through most, because clearing that one is what makes the "
          "rest of the house feel possible.", ask=PLAN_ASK + _DECLUTTER_ASK,
          guard=_declutter_fits,
          avoid=("warm", "warmer", "warmth", "heat", "heated", "heating", "radiator",
                 "insulate", "insulation", "lagging", "mineral wool", "loft insulation",
                 "board out", "boarding", "floor the loft",
                 "paint", "painting", "painted", "repaint",
                 "charge", "charges", "charge for", "labour", "hourly", "mot", "service",
                 "servicing", "serviced", "full service",
                 "spend money", "spending money", "spent money", "save money",
                 "saving money", "waste money", "wasting money", "money on", "junk food",
                 "smoke", "smoking", "smoky", "fumes", "smell", "smells", "smelly", "damp",
                 "mould", "mold", "condensation", "air out", "air it out",
                 "stink", "stinks", "odour", "odor", "reek", "musty",
                 "radiator", "radiators", "rad", "rads", "towel rail", "heating", "boiler",
                 "thermostat", "thermostatic", "valve", "trv", "frost setting", "bleed",
                 "fix", "fixed", "fixing", "repair", "repairs", "repaired", "broken",
                 "not working", "doesnt work", "doesn't work", "wont close", "won't close",
                 "wont open", "won't open", "stuck", "leak", "leaking", "replace", "replacing",
                 "roller", "spring", "lock", "handle", "hinge", "jammed",
                 "car", "cars", "van", "bike", "bicycle", "motorbike", "phone", "laptop",
                 "washing machine", "fridge", "freezer", "dishwasher", "tumble dryer",
                 "sell", "selling", "sold", "scrap", "part exchange", "trade in", "get rid of my",
                 "mattress", "mattresses", "sofa", "settee", "couch", "armchair", "bed", "beds",
                 "cot", "carpet", "carpets", "rug", "tyre", "tyres", "tire", "tires", "battery",
                 "rubble", "hardcore", "garden waste", "tree", "branches", "asbestos",
                 "paddling pool", "trampoline",
                 "moth", "moths", "fly", "flies", "ant", "ants", "mouse", "mice", "rat", "rats",
                 "slug", "slugs", "snail", "snails", "weed", "weeds", "moss", "aphid", "aphids",
                 "bedbug", "bedbugs", "bed bugs", "flea", "fleas", "wasp", "wasps",
                 "cockroach", "cockroaches", "woodlice", "spider", "spiders", "pigeon",
                 "pigeons", "fox", "foxes", "stain", "stains",
                 "weevil", "weevils", "mite", "mites", "flour mite", "flour mites", "larder",
                 "silverfish", "booklice", "woodworm", "carpet beetle", "clothes moth",
                 "fruit fly", "fruit flies", "drain fly", "drain flies", "gnat", "gnats",
                 "midge", "midges", "wasp nest", "ants nest",
                 "flatmate", "flatmates", "housemate", "housemates", "roommate", "roommates",
                 "house share", "houseshare", "lodger",
                 "dust", "dusty", "dusting", "cobweb", "cobwebs", "hoover", "hoovering",
                 "vacuum", "vacuuming", "wipe", "wiping", "mop", "mopping", "polish",
                 "cleaning", "clean the", "scrub", "scrubbing", "limescale",
                 "to move", "moving house", "moving home", "moving flat", "moving out",
                 "moved house", "house move", "removal", "removals",
                 "pack up", "packing", "care home", "residential home", "nursing home",
                 "email", "emails", "inbox", "spam", "junk mail", "newsletter",
                 "newsletters", "unsubscribe")),
    entry("weekend-ideas",
          (("weekend", "weekends", "day off", "days off", "saturday", "sunday", "free day",
            "bank holiday weekend", "bank holiday", "next weekend", "this weekend",
            "this evening", "tonight", "today", "around here", "near here", "near me",
            "in town", "in the area",
            "tomorrow", "tomorrow morning", "tomorrow afternoon", "tomorrow evening",
            "tomorrow night"),
           ("what", "anything", "ideas", "idea", "things to do", "something to do", "do this",
            "suggest", "recommend", "bored", "plan", "plans", "shall i", "can i do",
            "what can i do", "what should i do", "what can we do", "what shall we do",
            "nothing to do", "what is there to do", "any ideas", "do with")),
          _a_free_weekend,
          guard=lambda reading: (_the_free_weekend_fits_and_is_asked(reading)
                                 and _a_stretch_of_time_to_fill(reading)),
          avoid=("clear out", "clear the", "tidy", "chores", "garage", "loft", "cupboard",
                 "what helps", "what would help", "helps it", "help it", "help the",
                 "ease it", "relief", "get rid of", "make it better", "stop it",
                 "tablet", "tablets", "medicine", "medicines",
                 "medication", "painkiller", "painkillers", "ibuprofen", "paracetamol",
                 "antihistamine", "antibiotic", "dose", "pharmacy", "chemist", "prescription",
                 "symptom", "symptoms", "toothache", "headache", "migraine", "sore throat",
                 "temperature", "fever", "nausea", "cramps", "stomach ache", "dizzy",
                 "dentist", "gp", "doctor", "nurse", "111", "999", "side effect", "side effects",
                 "decorate", "painting", "diy", "away", "hotel", "flight", "abroad",
                 "match", "race", "half marathon", "long run", "work", "shift",
                 "wear", "wearing", "wore", "put on", "dress", "dressing",
                 "what should i take", "what should i bring", "what to take", "what to bring",
                 "take with", "bring with", "take to a", "bring to",
                 "need to bring", "need to take", "need to pack", "must bring", "to bring tomorrow",
                 "pack", "packs", "packing", "packed", "suitcase", "suitcases", "luggage",
                 "hand luggage", "carry on", "toiletries", "wash bag", "rucksack",
                 "watch", "watching", "film", "films", "series", "netflix", "tv", "read",
                 "reading", "book", "books", "cook", "cooking", "recipe", "recipes",
                 "telly", "television", "bbc", "itv", "channel 4", "channel 5",
                 "channel four", "channel five", "listings", "on telly", "on tv",
                 "dinner", "lunch", "eat", "food", "bake", "baking", "shop", "buy",
                 "train", "training", "gym", "run", "running", "football", "park",
                 "kids", "children", "child", "baby",
                 "cheap", "free", "money", "cost", "costs", "budget", "pay", "price",
                 "any plans", "got plans", "got any plans", "up to tonight", "up to later")
                 + A_WEATHER_ASK
                 + A_HOURS_ASK),

    entry("hosting-food",
          (("dinner party", "having people over", "people coming over", "guests", "buffet",
            "barbecue", "bbq", "roast for", "cooking for", "family over"),
           ("plan", "planning", "much", "how many", "ahead", "timing", "timings", "first",
            "menu", "quantities", "12 people", "10 people", "8 people")),
          "Choose a menu you can cook twice before: one oven dish, something cold on the side, "
          "bread, and a pudding made the day before, so you're out of the kitchen when they arrive. "
          "For a barbecue, allow 250g of meat a head plus a vegetarian option; for a sit-down "
          "dinner, eight people is the most a normal oven does well.", ask=PLAN_ASK,
          bias=1),

    entry("late-guests",
          (("guests", "guest", "guests coming", "guest coming", "guests are coming",
            "people coming", "people are coming", "people over", "people round",
            "people arriving", "people turning up", "friends coming", "friends are coming",
            "friends over", "friends round", "friends arriving", "friends turning up",
            "family coming", "family over", "company coming", "company over", "visitors",
            "visitors coming", "someone coming over", "people for dinner", "guests for dinner",
            "people coming for dinner", "hosting dinner", "having people over",
            "having friends over", "having guests", "party tonight", "people here at",
            "people are here", "guests are here", "theyre here", "they are here",
            "people are at the door", "someone at the door", "somebody at the door",
            "friend dropping", "friend popping", "dropping round", "popping round",
            "dropping by", "popping in", "coming round", "coming over",
            "someone", "somebody", "in laws", "in-laws", "mother in law", "father in law",
            "parents", "mum", "dad", "sister", "brother", "aunt", "uncle", "cousin",
            "grandparents", "neighbours"),
           ("in an hour", "in half an hour", "in a hour", "in 20 minutes", "in twenty minutes",
            "in 30 minutes", "in thirty minutes", "in 10 minutes", "in ten minutes",
            "in 15 minutes", "in fifteen minutes", "in 45 minutes", "in two hours",
            "in a couple of hours", "in a bit", "in 40 minutes", "this evening", "tonight",
            "nothing is ready", "nothing ready", "nothing prepared", "nothing made",
            "nothing in", "not ready", "im not ready", "i'm not ready", "not prepared",
            "havent started", "haven't started", "havent even started", "havent cooked",
            "last minute", "at short notice", "short notice", "unexpected", "unannounced",
            "turned up", "turning up", "arrived early", "arriving early", "early",
            "just told me", "just rang", "just called", "just texted", "surprise visit",
            "on their way", "on his way", "on her way", "on the way", "minutes away",
            "20 minutes away", "ten minutes away", "five minutes away",
            "at 6", "at 7", "at 8", "at 6pm", "at 7pm", "at 8pm", "at six", "at seven", "at eight",
            "at the door", "at my door", "already here", "later", "this afternoon",
            "only have", "only got", "nothing in", "nothing much in", "no food in")),
          "Do the three things they will actually notice, in this order: clear the floor into one "
          "basket and shut the doors on the rest, put out glasses and something to nibble, and "
          "cook one thing from what you already have - pasta, an oven tray of whatever vegetables "
          "and sausages are in, or bread, cheese and something cold from the fridge. Buy only the "
          "missing bit on the way home, and don't start a clean nobody will see: a drink in their "
          "hand and food within half an hour is the whole of it.",
          avoid=("what should i cook", "what can i cook", "what to cook", "what can i make",
                 "what to make", "recipe", "recipes", "what should i wear", "what to wear",
                 "cook", "cooking", "cooked", "menu", "roast", "for dinner", "dinner party",
                 "dinner tonight", "meal", "meals", "food for", "feed", "what do i cook",
                 "mess", "messy", "clean", "cleaning", "tidy", "tidy up", "hoover", "vacuum",
                 "dust", "dishes", "washing up", "disaster", "shambles", "dirty", "filthy",
                 "stay with us", "staying with us", "for the weekend", "for a week",
                 "next week", "next month", "in a few weeks", "in two weeks", "tomorrow",
                 "keeps turning up", "keeps coming over", "keeps coming round",
                 "keeps dropping in", "keeps dropping by", "keeps popping in",
                 "turning up unannounced", "unannounced", "uninvited", "without asking",
                 "every weekend", "all the time", "every day", "again and again",
                 "boundary", "boundaries", "how do i tell", "how do i ask",
                 "without warning", "without telling me", "out of the blue",
                 "watch", "watching", "watch with", "what to watch", "something to watch",
                 "watch tonight", "film", "films", "movie", "movies", "box set", "box sets",
                 "series", "telly", "netflix", "prime", "disney", "iplayer", "streaming",
                 "episode", "episodes", "listen to", "listen with", "play with", "a game",
                 "board game", "board games", "cards",
                 "whenever she likes", "whenever he likes", "whenever they like",
                 "turns up without", "turned up without"),
          bias=10),

    entry("christmas-plan",
          (("christmas", "xmas", "christmas day", "christmas dinner", "boxing day"),
           ("plan", "planning", "organise", "ahead", "timing", "timings", "hosting", "much",
            "start", "list", "prepare", "shop")),
          "Write every cooking time on one sheet and work back from when you want to eat: the bird "
          "rests an hour, so it comes out an hour before, and the potatoes go in as it comes out. "
          "Shop for the cold stuff two days before rather than on the day, because fridge space "
          "runs out, and hand out the pudding, the drinks and the ice to other people.", ask=PLAN_ASK),

    entry("road-trip-plan",
          (("road trip", "long drive", "driving down", "driving to", "driving holiday",
            "driving abroad"),
           ("plan", "planning", "stops", "route", "how long", "overnight", "break", "rest",
            "hours", "first", "check")),
          "Plan the driving days rather than the hours: put the stops in first, every two hours and "
          "one proper stop a day, and don't book more than six hours of driving in a day. Book the "
          "first and last night's bed before you go, check the spare tyre, the oil and the "
          "breakdown cover, and keep the overnight bag on the back seat.", ask=PLAN_ASK,
          avoid=("how long is the drive", "how long would the drive", "how long does the drive",
                 "how far is", "how many miles", "how long does it take to drive",
                 "warning light", "warning lights", "engine light", "dashboard", "mot",
                 "car service", "full service", "needs a service", "due a service",
                 "due for a service", "service the car", "serviced", "servicing",
                 "breakdown", "battery light", "oil light")),

    entry("week-plan",
          (("my week", "the week ahead", "plan my week", "my time", "everything at once",
            "everything feels urgent", "to do list", "never enough time"),
           ("plan", "planning", "organise", "prioritise", "prioritize", "urgent", "start",
            "manage", "sorted")),
          "Write down what is actually due this week, then pick three things a day and put them in "
          "the diary as blocks; the rest waits, and that is fine. Real deadlines go in first, the "
          "urgent-but-not-important jobs get one slot a day, and the way to protect the rest is to "
          "say no to one thing out loud.", ask=PLAN_ASK),
    entry("food-shop-waste",
          (("food", "food shopping", "groceries", "shopping", "supermarket", "fridge", "veg",
            "vegetables", "leftovers", "left over"),
           ("waste", "wasting", "wasted", "throw", "throwing", "threw", "thrown",
            "throw away", "throwing away", "thrown away", "throws away", "toss out",
            "bin", "binned", "binning", "in the bin", "rubbish", "goes off", "going off",
            "gone off", "rot", "rotting", "never use it", "never use them",
            "never get through", "buy too much", "buying too much", "buy less",
            "shop better")),
          "Write the week's four meals down before you shop and buy for those, not for the week "
          "you imagine. Keep a box in the fridge for what must go first, and put tonight's dinner "
          "in it when you unpack. Cook double twice a week and freeze the spare that evening, "
          "because leftovers in the fridge are what gets binned, and buy fresh less often: a "
          "top-up on the way home beats a full trolley on a Sunday.",
          avoid=("use by", "best before", "how long", "safe to eat", "still ok", "cat food",
                 "dog food", "food bank", "school dinner", "packed lunch", "declutter",
                 "moving house", "kitchen bin",
                 "left out", "all night", "overnight", "out of the fridge", "is it ok",
                 "two hours", "bin it", "gone bad",
                 "goes off first", "go off first", "eat first", "use first", "use up first",
                 "which shelf", "top shelf", "bottom shelf", "middle shelf", "salad drawer",
                 "crisper", "fridge order", "where in the fridge", "what goes where",
                 "off her food", "off his food", "off their food", "off our food",
                 "off my food", "off your food", "gone off food", "gone off eating",
                 "appetite")),
    entry("saving-plan",
          (("save money", "saving money", "start saving", "savings", "save each month",
            "save every month", "put money aside", "money aside", "save some money",
            "save a bit", "i need to save", "need to save up", "for a rainy day",
            "save up"),
           ("how", "what", "whats", "what's", "where", "any", "help", "should", "could", "best",
            "idea", "ideas", "tips", "advice", "start", "better at", "get better",
            "want", "wanted", "trying", "need", "intend",
            "never have anything left", "keep", "manage", "much", "each month", "every month")),
          "Track two weeks of what actually leaves the account before you change anything: the "
          "subscriptions you forgot are usually where it went. Then pick an amount you will not "
          "miss, 10 to 20 per cent of what you take home, and move it on pay day into a separate "
          "account you carry no card for, so saving happens before the spending. Build towards "
          "three to six months of essential bills as the buffer, and raise the standing order by "
          "10 pounds whenever a bill or a habit goes.",
          ask=("how", "what", "whats", "what's", "any", "help", "should", "could", "best",
               "ideas", "tips", "advice", "start", "better", "want", "wanted", "trying", "need",
               "intend", "help me"),
          avoid=("daylight saving", "daylight savings", "summer time", "the clocks",
                 "how long", "per month for", "interest", "isa", "pension", "mortgage", "deal",
                 "cheaper", "coupon", "voucher", "insurance", "contract", "flight", "holiday",
                 "christmas", "student loan", "overdraft fee", "moving", "move", "removal", "van",
                 "sofa", "flat", "house",
                 "heating", "boiler", "electricity", "energy", "gas", "water", "petrol", "fuel",
                 "bill", "bills", "broadband", "phone", "groceries", "takeaway", "subscription",
                 "account", "accounts", "rate", "rates", "bank", "gone", "lost", "losing",
                 "things to do", "something to do",
                 "bored", "kids are", "keeping the kids", "rainy day out",
                 "ideas for a rainy day", "rainy day ideas", "ideas for rainy days",
                 "what can i do for a rainy day", "what can we do for a rainy day",
                 "what can i do on a rainy day", "what can we do on a rainy day",
                 "what should i do on a rainy day", "what shall we do on a rainy day",
                 "film", "films", "movie", "movies", "watch", "watching", "tv", "telly",
                 "series", "box set", "netflix", "read", "reading", "book", "books",
                 "listen", "listening", "podcast", "game", "games",
                 "music", "song", "songs", "album", "albums", "playlist", "playlists",
                 "spotify", "tunes", "band", "bands",
                 "draw", "drawing", "drawings", "doodle", "doodling", "sketch", "sketching",
                 "crayons", "colouring", "coloring", "paint", "painting",
                 "where should i keep", "where do i keep", "where to keep", "keep my savings",
                 "credit card", "card", "pay off", "paying off", "debt", "debts", "overdraft",
                 "loan",
                 "what did i say", "what did i tell", "did i say", "did i tell", "remind me",
                 "you said", "again"),
          guard=_a_rainy_day_is_money),
    entry("out-of-a-rut",
          (("rut", "stuck", "same thing every day", "groundhog", "bored of my life",
            "bored of everything", "going nowhere", "in a slump", "slump", "plateau"),
           ("in", "get out", "getting out", "escape", "break", "how", "feel", "feeling",
            "again", "fix", "change")),
          "Change one thing you do on autopilot - a different walk, a new lunch, saying yes to the "
          "first invitation - because a rut is a loop of the same cues. Put one thing in the diary "
          "this week that you are looking forward to: the lift comes from having something ahead "
          "more than from willpower.",
          avoid=("depressed", "depression", "weeks now", "months now", "can't get out of bed",
                 "no pleasure", "anxious", "anxiety", "job", "career", "relationship",
                 "marriage", "running", "training", "weight", "gym",
                 "traffic", "jam", "queue", "lift", "snow", "mud", "airport", "stuck on",
                 "stuck at", "stuck in a meeting", "stuck in the house", "stuck indoors",
                 "stuck with", "wheel", "drawer", "jar",
                 "contract", "contracts", "contractor", "cancellation", "minimum term",
                 "cake", "cakes", "loaf", "sponge", "bun", "buns", "muffin", "muffins",
                 "bread", "tin", "tins", "baking", "pan", "tray", "mould", "pastry",
                 "cash machine", "cashpoint", "atm", "card reader",
                 "chip and pin", "ticket machine", "parking machine",
                 "throat", "lump", "swallow", "swallowing", "swallowed", "something stuck",
                 "i feel stuck", "feel stuck", "stuck in life", "feels stuck",
                 "gear", "gears", "gearbox", "derailleur", "chain", "chains", "chainring",
                 "pedal", "pedals", "cranks", "brakes", "brake", "clutch", "engine",
                 "wheel", "wheels", "handlebars", "saddle", "bike", "bikes", "bicycle",
                 "motorbike", "scooter", "mower", "lawnmower", "printer", "scanner",
                 "laptop", "computer", "tablet", "keyboard", "mouse", "phone",
                 "washing machine", "tumble dryer", "dishwasher", "vacuum", "fridge",
                 "freezer", "boiler", "radiator", "oven", "microwave", "toilet", "tap",
                 "shower", "door", "doors", "window", "windows", "gate", "zip", "zipper",
                 "button", "screw", "screws", "bolt", "bolts", "lock", "key", "keys",
                 "stuck in gear", "stuck in a gear", "stuck in first", "stuck in second",
                 "stuck in third", "stuck in top gear", "stuck on the same gear",
                 "gears are stuck", "gears wont", "gears won't", "wont go into gear",
                 "won't go into gear", "wont shift", "won't shift")),
    entry("new-year-resolution",
          (("new year", "new years", "resolution", "resolutions", "new year's"),
           ("keep", "keeping", "stick", "sticking", "goal", "goals", "promise", "start",
            "starting", "how", "make", "best", "good", "succeed")),
          "Make it one resolution, small enough to do on your worst day - ten minutes, not an hour "
          "- and tie it to something you already do, like a walk after your morning coffee. Mark "
          "the days you did it rather than the streak you broke, and if you miss once, the rule is "
          "never to miss twice.",
          avoid=("when is", "date", "eve", "party", "fireworks", "open", "closed", "traffic",
                 "dinner", "meal", "gym membership", "join",
                 "died", "dies", "dying", "death", "dead", "passed away", "funeral", "killed",
                 "grief", "grieving", "loss", "lost him", "lost her", "lost them", "miss him",
                 "miss her", "miss them", "keep going over", "going over",
                 "over the last", "that night", "cant stop thinking", "can't stop thinking")),
    entry("how-to-set-a-goal",
          (("goal", "goals", "goal setting", "set a goal", "set goals", "plan for the year",
            "yearly plan", "five year plan", "5 year plan", "3 year plan", "life plan",
            "plan my year", "plan my life", "what i want to achieve", "achieve", "ambition"),
           ("how", "set", "setting", "make", "making", "write", "start", "stick", "keep to",
            "better", "worth", "should i", "realistic", "realistically", "stuck", "no idea")),
          "Pick one theme for the year rather than ten goals, then turn it into three actions with "
          "dates: \"run 5k by June - book a race in January, run twice a week\" does more than "
          "\"get fit\". Make each one small enough to start in ten minutes on a bad day, put the "
          "first step in the diary this week, and look at the list once a month rather than every "
          "day. Two things that raise the odds: write them down where you will see them, and tell "
          "one person.",
          avoid=("new year", "resolution", "resolutions", "save", "saving", "savings",
                 "deposit", "pension", "budget", "calories", "weight", "marathon", "training",
                 "revision", "exam", "deadline", "workout", "gym"),
          bias=1),
    entry("what-to-do-with-my-life",
          (("what should i do with my life", "what to do with my life",
            "what do i do with my life", "dont know what to do with my life",
            "don't know what to do with my life", "no idea what to do with my life",
            "what next in life", "direction in life", "purpose in life", "my purpose",
            "where am i going", "what am i doing with my life", "find my purpose"),
           ("what", "how", "should", "find", "figure", "work out", "decide", "lost", "stuck",
            "confused", "help", "advice", "next")),
          "Don't try to answer the whole of it at once. Write three short lists: what you are good "
          "at (the things other people ask you for, not what you would like to be good at), what "
          "you would do for free, and what you need money for. Then pick one small experiment that "
          "touches two of the three - a course, a volunteering shift, a paid side project - and "
          "give it three months, because direction comes from doing rather than deciding. Keep "
          "whatever you would happily do again.",
          avoid=("depressed", "depression", "anxious", "suicidal", "weeks now", "months now",
                 "cant get out of bed", "career change", "apply", "ucsas", "ucas", "course fees",
                 "my job", "my boss", "my partner", "my husband", "my wife", "boyfriend",
                 "girlfriend", "divorce", "break up", "grief", "died", "funeral"),
          bias=1),
    entry("free-day-out",
          (("free", "cheap", "cheaper", "no money", "not much money", "skint", "broke",
            "dont cost",
            "doesnt cost", "thank mustnt", "tight budget", "on a budget", "low cost"),
           ("day out", "days out", "things to do", "something to do", "something nice",
            "something special", "what can i do",
            "what can we do", "where can we go", "where can i go", "near me", "this weekend",
            "at the weekend", "with the kids", "take the kids", "with children", "family")),
          "Free ones that work: a walk with a purpose (a park, a canal, the woods, a hill with a "
          "view - flask in the bag), a museum or gallery with free entry, the library, or a "
          "Saturday market. With kids, add a list of five things to find and a ball. Take snacks "
          "and a drink, and the day costs you parking and a coffee.",
          bias=1,
          avoid=("meal", "meals", "food", "eat", "eating", "dinner", "lunch", "tea",
                 "breakfast", "takeaway", "cook", "cooking", "recipe", "recipes", "bake",
                 "baking", "shop", "shopping", "grocery", "groceries", "supermarket",
                 "film", "films", "movie", "watch", "book", "books", "read", "reading",
                 "freezer", "freeze", "sugar free", "gluten free", "dairy free", "free range",
                 "car", "cars", "van", "insurance", "rent", "bill", "bills", "delivery",
                 "postage", "sim", "tariff", "subscription", "mobile",
                 "present", "presents", "gift", "gifts", "secret santa", "stocking",
                 "stocking filler")),

    entry("cheap-things-to-do",
          (("things to do", "something to do", "what can i do", "what should i do", "what to do",
            "what can we do", "what should we do", "anything to do", "ideas", "activities",
            "activity", "day out", "days out", "afternoon out"),
           ("weekend", "saturday", "sunday", "free", "cheap", "cheaply",
            "budget", "family", "everyone", "at home", "indoors", "outside")),
          ("Pick one shape and put a time on it, because a free day with no plan turns into the "
           "sofa. The ones that cost nothing: a walk with a destination (a park, a canal, a hill, "
           "a shop that sells something you like), a free museum or gallery - most have a permanent "
           "collection that costs nothing - and the library, which has events, papers and warmth. "
           "At home: a film nobody has seen, a bake with whatever is in the cupboard, a swap of "
           "clothes or books with friends, or a board game with a rule that the phones stay in "
           "another room. For a family, one outside thing in the morning and one quiet thing after "
           "lunch is plenty: children remember the day that had a walk and a picnic in it, not the "
           "one that cost forty pounds."),
          avoid=("recipe", "cook", "cooking", "dinner", "lunch", "tea", "eat", "meal", "back",
                 "breakfast", "breakfasts", "brunch", "snack", "snacks", "packed lunch",
                 "pain", "knee", "doctor", "gp", "work", "job", "boss", "office", "school run",
                 "hotel", "flight", "flights", "abroad", "holiday", "leave my", "quit",
                 "city break", "city breaks", "weekend away", "weekend break", "break away",
                 "night away", "couple of nights", "few nights", "weekend in",
                 "rent", "bills", "benefits", "save money", "savings", "invest", "loan", "debt",
                 "kids", "children", "child", "toddler", "baby", "year old", "entertain",
                 "keep busy", "stuck inside", "bored", "boring", "half term",
                 "thunderstorm", "thunderstorms", "lightning", "thunder",
                 "flood", "floods", "flooding", "flooded",
                 "dairy free", "gluten free", "gluten-free", "sugar free", "sugar-free",
                 "wheat free", "egg free", "nut free", "meat free", "fat free", "lactose free",
                 "caffeine free", "alcohol free", "free from", "free range", "freezer", "freezers",
                 "frozen", "duty free", "hands free", "hands-free", "free trial",
                 "present", "presents", "gift", "gifts", "secret santa", "stocking",
                 "stocking filler"),
          bias=1,
          guard=lambda reading: (_a_day_out_is_the_question(reading)
                                 and _a_stretch_of_time_to_fill(reading))),

    entry("dish-for-tonight",
          (tuple(alias for aliases, _keys, _body, _avoid in RECIPES for alias in aliases),
           ("tonight", "this evening", "this afternoon", "for tea", "for dinner", "for supper",
            "for lunch", "later", "this weekend", "tomorrow night"),
           ("planning", "planning on", "plan", "plans", "planned", "fancy", "fancied",
            "i might", "shall i", "should i", "decided to")),
          _dish_for_tonight,
          bias=-3,
          avoid=("went wrong", "too thin", "too thick", "too salty", "bland", "burnt",
                 "what should i cook", "what can i cook", "what shall i cook", "what to cook",
                 "what should i make", "what can i make", "what should i eat", "what can i eat",
                 "whats for", "what's for", "what to eat", "meal ideas", "dinner ideas",
                 "watery", "dry", "recipe", "how long", "how do i", "what goes with",
                 "vegan", "vegetarian", "veggie", "dairy", "gluten", "wheat", "allergic",
                 "allergy", "coeliac", "celiac", "intolerant", "calories", "healthy",
                 "keep", "keeps", "store", "freeze", "leftover", "left over", "reheat",
                 "restaurant", "takeaway", "shop", "buy", "supermarket", "tesco", "aldi",
                 "make", "makes", "making", "made", "cook", "cooks", "cooking", "cooked",
                 ) + ANNOUNCED_DISH),

    entry("try-once",
          (("try once", "tried once", "at least once", "once in my life",
            "once in a lifetime", "never done", "never tried", "never have i", "ive never",
            "i have never", "something new", "something different", "new thing",
            "worth trying", "something to try", "one thing to try", "bucket list",
            "everyone should try", "everyone should do", "everyone should have",
            "everyone has to do", "wouldnt think of", "try next", "something ive not",
            "before i die", "missing out"),
           TRY_ONCE_ASK),
          _try_once,
          ask=("try", "tried", "trying", "should", "suggest", "recommend", "tell", "give",
               "idea", "ideas", "anything", "something", "one thing", "surprise", "once",
               "want", "need"),
          bias=6,
          avoid=("cook", "cooking", "recipe", "recipes", "dinner", "lunch", "breakfast",
                 "tea", "bake", "baking", "food", "restaurant", "meal", "meals",
                 "gym", "workout", "training", "running", "run", "diet", "exercise",
                 "hair", "skin", "garden", "plant", "plants", "decorate", "paint",
                 "job", "jobs", "career", "interview", "course", "holiday", "trip",
                 "city", "town", "hotel", "shop", "shopping", "buy", "money",
                 "song", "album", "band", "film", "films", "book", "books", "series",
                 "game", "games", "music", "podcast", "tv", "netflix", "sport",
                 "booked", "already", "tried it", "tried that", "didnt like",
                 "not for me", "went wrong",
                 "every", "each", "daily", "everyday", "weekly", "monthly", "routine",
                 "habit", "habits", "regularly", "stick to", "keep it up")),
    entry("try-once-more", TRY_ONCE_MORE, _try_once_more, bias=4,
          avoid=("cook", "cooking", "recipe", "dinner", "food", "paint", "garden")),
]
