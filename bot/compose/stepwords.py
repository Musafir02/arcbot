
STEPS = frozenset("""
    abandon adopt apply arrange ask attend bake be begin board book borrow bring build buy call
    cancel catch change check choose clean clear climb close come continue cook cover cut decorate
    decide do drink drive drop eat email empty enter feed fight find finish fix fly follow forget
    get give go grow hand have head help hire hold hunt improve increase install invest invite
    join keep knit launch learn leave lend let listen live log look lose make marry meet move open
    order organise organize paint pass pay phone pick plan plant play post practise prepare put
    quit read record redecorate reduce register remember remove renovate rent repair replace
    report rescue retire return review ride ring run save say see sell send set sew shave shop
    sign sit slow sort speak spend split start stay stop stream study submit swap switch take talk
    teach tell test text throw tidy train transfer travel treat trim try tune turn uncover upgrade
    use visit volunteer wait walk wash watch wear win withdraw work write accept appeal babysit
    celebrate claim cycle decline dye insure jog meditate renew reply respond retrain rewire swim
    complain apologise apologize argue browse cheat chill confess cry cuddle dance delay delete
    download dress forgive gamble hide hug joke kiss laugh lay lie nap panic postpone pray print
    relax scroll shower sing skip sleep snooze stall stretch sulk tease worry yawn
""".split())

DOUBLES = frozenset("""
    begin forget regret admit commit prefer refer occur submit permit upset control patrol compel
    propel equip
""".split())


IRREGULAR = {"be": "being"}


def _ing(word):
    if not word or word.endswith("ing"):
        return word
    if word in IRREGULAR:
        return IRREGULAR[word]
    if word.endswith("ie"):
        return word[:-2] + "ying"
    if word.endswith("e") and not word.endswith(("ee", "ye", "oe")):
        return word[:-1] + "ing"
    short = len(word) <= 4 or word in DOUBLES
    if (short and len(word) > 2 and word[-1] not in "aeiouwxy" and word[-2] in "aeiou"
            and (word[-3] not in "aeiou" or (word[-3] == "u" and word[-4:-3] == "q"))):
        return word + word[-1] + "ing"
    return word + "ing"


def a_step(word):
    return (word or "").strip().lower().strip(".,!?") in STEPS


def said_after_a_to(phrase, ing=None):
    phrase = " ".join(str(phrase or "").split()).strip(" .,!?:;")
    words = phrase.split()
    if not words:
        return ""
    if a_step(words[0]):
        fold = ing or _ing
        return fold(words[0]) + (" " + " ".join(words[1:]) if len(words) > 1 else "")
    return "going to " + phrase


MOVING_TO = "going to|gonna|off to|out to|away to|heading to|heading off to|about to"
