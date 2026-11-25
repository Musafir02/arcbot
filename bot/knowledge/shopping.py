import re

from ..compose import pick
from ..memory import newborn, people
from ..understanding import topics as reading
from .lookup import (PRESENT_ASK, PRICE_COMPARED, a_food_is_being_kept, a_price_not_a_loan,
                     about_them, asks_where, asks_where_a_shop_answers, entry)

ANSWERS = ("shopping", "money", "technology")


_GIFT_ANYONE = ("Buy into what they already do: a good version of something they use every "
                "week (a proper kitchen knife, warm socks, decent coffee), a voucher for a place "
                "they go anyway, or a day out the two of you share. Tell me what they do at the "
                "weekend and I'll narrow it down.")


PERSON_WORDS = frozenset("""mum mother dad father sister brother nan nana grandma grandad granny
    son daughter wife husband partner friend mate flatmate boyfriend girlfriend colleague aunt
    uncle cousin stepmum stepdad he she they him her his hers their stepmother stepfather""".split())
TASTE_WORDS = frozenset("""loves love likes like enjoys enjoy keen into fond obsessed collects
    plays does goes went favourite favorite hobby hobbies garden gardening cooks cooking bakes
    baking fishing reads reading runs running knitting sewing cycling walking football music
    books films plants allotment""".split())


_FOLD = (("'s", ""), ("s'", ""), ("s", ""), ("'", ""))


SUPERMARKETS = (
    ("Aldi", ("aldi",), 0, "the cheapest of the big names",
     "own-brand staples run roughly a fifth less than at Tesco or Sainsbury's, on a smaller range "
     "with few named brands",
     "has the cheaper staples and a smaller range"),
    ("Lidl", ("lidl",), 0, "one of the two cheapest of the big names",
     "own-brand staples run roughly a fifth less than at Tesco or Sainsbury's, with a strong "
     "bakery and few named brands",
     "is level on price and stronger on the bakery"),
    ("Farmfoods", ("farmfoods",), 0, "cheap for frozen food",
     "the frozen and branded boxes are cheap and the fresh food is thin",
     "is cheaper on frozen and thinner on fresh"),
    ("Asda", ("asda",), 1, "usually the cheapest of the big four",
     "a like-for-like basket comes out cheapest at Asda, and it price-matches Aldi and Lidl on "
     "the basics",
     "price-matches Aldi on the basics and runs more brands"),
    ("Iceland", ("iceland",), 1, "cheap for frozen food",
     "frozen and ready meals are cheap and everything else is dearer",
     "is cheaper on frozen and dearer on the rest"),
    ("Morrisons", ("morrisons", "morrison"), 2, "mid-priced",
     "it sits with Tesco and Sainsbury's, and is often the cheapest of the big four on fresh meat "
     "and fish",
     "is close on price with better fresh meat and fish"),
    ("Tesco", ("tesco", "tescos"), 2, "mid-priced",
     "its Aldi Price Match holds the basics at Aldi's price, and the rest of the basket costs more",
     "holds the basics at Aldi's price and costs more for the rest"),
    ("Sainsbury's", ("sainsburys", "sainsbury's", "sainsbury"), 2, "mid-priced like Tesco",
     "the basics are price-matched to Aldi and the brands are what cost more",
     "matches the basics and costs more for the brands"),
    ("Ocado", ("ocado",), 3, "M&S food delivered",
     "it is priced like M&S rather than like a discounter",
     "is priced like M&S"),
    ("The Co-op", ("co-op", "co op", "coop", "co operative", "cooperative"), 3, "a convenience shop",
     "it is dearer than the big four on almost everything, so it is a top-up shop",
     "is dearer, which is what the convenience buys"),
    ("Waitrose", ("waitrose",), 4, "one of the two dearest",
     "it runs around 10-20% more than Tesco on the same basket, and the fresh food is better",
     "costs more and is better on fresh food"),
    ("M&S", ("marks and spencer", "marks spencer", "m and s", "m&s", "marks & spencer"), 4,
     "the dearest of the big names",
     "it runs around 10-20% more than Tesco on the same basket, and the ready meals are why "
     "people go",
     "costs more, and the ready meals are why people go"),
)

_CHEAPEST_TAIL = (" It is one of the cheapest places to do a full shop, though the range of "
                  "brands is smaller, so anything specific may need a second stop.")
_MIDDLE_TAIL = (" The basics are price-matched to the discounters, so it is the brands in the "
                "trolley that make the difference: a basket of own-brand staples will be cheaper "
                "at Aldi or Lidl.")
_DEAR_TAIL = (" For a cheaper basket on the same list, the discounters save around a fifth and "
              "Asda or Tesco most of the rest.")


_QUALITY_WORDS = ("good", "quality", "as good", "better", "worse", "taste", "tasty", "nicer",
                  "fresh")


def _supermarket_quality(named):
    named.sort()
    if len(named) >= 2:
        cheap, dear = named[0], named[-1]
        if cheap[0] < dear[0]:
            return ("On quality they are close on the staples: most own-brand basics are made in "
                    "the same "
                    "factories as the named ones, so the store cupboard is the same food under a "
                    "different label. It shows in the fresh food and the range - %s %s, where %s "
                    "%s. For a full shop the cheaper one is fine; for a specific ingredient, or "
                    "for a weekend meal, the dearer one earns it." %
                    (cheap[1], cheap[4], dear[1], dear[4]))
        return ("On quality they are closer than on price: the basics are the same food under a "
                "different label, so what you pay for is the fresh food and the range - %s %s, "
                "and %s %s." % (cheap[1], cheap[4], dear[1],
                                 _without_the_same_opening(cheap[4], dear[4])))

    rank, name, sentence, why, contrast = named[0]
    if rank >= 4:
        return ("%s is %s: %s. The extra money goes on the parts of the shop the staples do not "
                "cover, not on the basics, which are the same items under a different label, so a "
                "full shop there costs more for much the same basket." % (name, sentence, why))
    if rank <= 1:
        return ("%s is %s: %s. None of that makes the staples worse: most own-brand basics come "
                "from the same factories as the named ones, so the saving is on the same food, and "
                "a basket built on ingredients rather than ready-made versions of them misses the "
                "weakest part." % (name, sentence, why))
    if rank == 3:
        return ("%s is %s: %s. Much the same as the rest on quality: the basics are the same "
                "items, and what the extra buys is convenience." % (name, sentence, why))
    return ("%s is %s: %s. Much the same as the rest on quality: the basics are the same items at "
            "a price-matched price, and what it adds is range and fresh food." %
            (name, sentence, why))


_RANGE_WORDS = ("gluten", "free from", "free-from", "freefrom", "vegan", "vegetarian",
                "dairy free", "dairy-free", "nut free", "nut-free", "allergy", "allergies",
                "allergic", "coeliac", "celiac", "organic", "halal", "kosher", "good for",
                "fine for", "ok for", "okay for", "any good for", "better for", "stock",
                "stocks", "sell", "sells", "range of", "own brand")


def _without_the_same_opening(first, second):
    for lead in ("costs more, and ", "costs more and ", "costs more, ", "costs more "):
        if first.startswith("costs more") and second.startswith(lead):
            return second[len(lead):].strip()
    return second


_SERVICE_WORDS = ("mobile", "broadband", "internet", "wifi", "phone", "phones", "sim", "sim only",
                  "telly", "tv", "bank", "banking", "current account", "savings account",
                  "insurance", "insure", "credit card", "loan", "mortgage", "tariff", "energy",
                  "gas and electric", "electricity", "petrol", "diesel", "fuel", "travel money",
                  "currency", "holiday", "holidays", "package holiday", "phone contract")


def _a_service_not_a_basket(line):
    return any(word in line for word in _SERVICE_WORDS)


def _the_turn_just_typed(memory):
    from ..memory import recent

    turns = recent(memory, 1)
    return str(turns[-1].get("user") or "") if turns else ""


_SHOP_ASK = ("should", "shall", "would", "worth", "better", "cheaper", "cheapest", "which",
             "what about", "instead of", "or ", "vs", "versus", "good", "decent", "ok")


def _a_statement_about_where_i_shop(typed):
    if not any(phrase in typed for phrase in ("i shop at", "i shop in", "i get my shopping")):
        return False
    return not any(word in typed for word in _SHOP_ASK)


def _supermarket_cheapest(memory, understood):
    typed = _the_turn_just_typed(memory).lower()
    if any(word in typed for word in _RANGE_WORDS):
        return None
    line = _said_line(understood).lower().replace("\u2019", "'")
    if any(word in line for word in _RANGE_WORDS):
        return None
    if _a_service_not_a_basket(line):
        return None
    if _a_statement_about_where_i_shop(line):
        return None
    named = []
    for name, spellings, rank, sentence, why, contrast in SUPERMARKETS:
        if any(spelling in line for spelling in spellings):
            named.append((rank, name, sentence, why, contrast))
    if named and any(word in line for word in _QUALITY_WORDS):
        return _supermarket_quality(list(named))
    if not named:
        return ("Aldi and Lidl are the cheapest of the big names for own-brand staples, around a "
                "fifth less than Tesco or Sainsbury's. Asda is usually the cheapest of the big "
                "four, Morrisons, Tesco and Sainsbury's come next and price-match Aldi on the "
                "basics, and Waitrose and M&S are the dearest. A convenience shop - the Co-op, a "
                "corner shop - costs more again, so it is for a top-up, not the weekly shop.")
    named.sort()
    if len(named) >= 2:
        cheap, dear = named[0], named[-1]
        if cheap[0] == dear[0]:
            return ("%s and %s are level on price, so pick on what you cook: %s %s, and %s %s. "
                    "Go to whichever is nearer." %
                    (cheap[1], dear[1], cheap[1], cheap[4], dear[1], dear[4]))
        return ("%s is the cheaper of the two: %s. %s %s." %
                (cheap[1], cheap[3], dear[1], dear[4])) + (
                " Check the price per 100g on the shelf label rather than the pack size, because "
                "the price match only covers the basics." if cheap[0] >= 2 else "")
    rank, name, sentence, why, contrast = named[0]
    tail = _CHEAPEST_TAIL if rank <= 1 else _MIDDLE_TAIL if rank == 2 else _DEAR_TAIL
    return "%s is %s: %s.%s" % (name, sentence, why, tail)


def _fold(word):
    if word in PERSON_WORDS or word in TASTE_WORDS:
        return word
    for cut, join in _FOLD:
        if word.endswith(cut) and word[: -len(cut)] + join in PERSON_WORDS | TASTE_WORDS:
            return word[: -len(cut)] + join
    return word


def _the_words(line):
    return {_fold(word) for word in re.findall(r"[a-z']+", str(line or "").lower())}


def _said_line(understood):
    if not isinstance(understood, dict):
        return ""
    return str(understood.get("text") or understood.get("clean") or "")


def _knows_a_taste(memory, understood=None):
    from ..memory import recent

    lines = [str(turn.get("user") or "") for turn in recent(memory, 8)]
    said = _said_line(understood)
    if said:
        lines.append(said)
    for line in lines:
        words = _the_words(line)
        if words & PERSON_WORDS and words & TASTE_WORDS:
            return True
    return False


CHILD_WORDS = ("kid", "kids", "child", "children", "childrens", "childs", "toddler", "toddlers",
               "baby", "babies", "boy", "boys", "girl", "girls", "teenager", "teenagers", "teen",
               "teens", "grandchild", "grandchildren", "grandson", "granddaughter", "niece",
               "nephew", "son", "sons", "daughter", "daughters", "school age", "year old",
               "year old")

CHEAP_ADULT = (
    "Spend it on something consumable and a notch better than the everyday: a good candle, "
    "decent coffee or tea, a nice bar of chocolate, a scratch card, seeds and a pot, a "
    "paperback you would actually recommend, or a really good pair of socks. £10 goes a "
    "long way on any of those and nothing needs a size or a taste test; if the group has a "
    "joke running, a silly gift that gets a laugh beats an expensive one that gets a polite "
    "smile. Keep the receipt.")

CHEAP_CHILD = (
    "For a child, spend it on things they use up or grow out of: bubble mix, a big sticker book, "
    "a colouring pad with good pens, bath crayons, play dough, a torch, a pack of cards, or a "
    "small Lego set on offer. Nothing needs a size and batteries are the only trap, so check the "
    "box. Socks, gloves and a book they will actually read are the safe last-minute ones.")


CHEAP_TEEN = (
    "For a teenager, a tenner is best spent on one thing they pick themselves: a voucher for the "
    "cinema or a shop they already use, phone credit, decent earphones or the cable they keep "
    "losing, or a game they can play with friends. Ask what they are into and buy the small "
    "version of that: the money goes further on one thing they want than on three they do not.")


def _gift_cheap(memory, understood):
    age = _an_age_in_the_line(understood)
    if age is None:
        age = people.the_age_of_the_person_they_mean(memory, understood)
    if age is not None:
        if age < 13:
            return CHEAP_CHILD
        if age < 20:
            return CHEAP_TEEN
        return CHEAP_ADULT
    clean = understood.get("clean") or ""
    for word in CHILD_WORDS:
        if re.search(r"(?<![a-z])" + re.escape(word) + r"(?![a-z])", clean):
            return CHEAP_CHILD
    return CHEAP_ADULT

def _the_tastes(memory, understood=None):
    from ..memory import recent

    said = []
    lines = [str(turn.get("user") or "") for turn in recent(memory, 4)]
    here = _said_line(understood)
    if here:
        lines.append(here)
    for turn in reversed(lines):
        for word in re.findall(r"[a-z']+", turn.lower()):
            name = _fold(word)
            for candidate in (name, name + "ing"):
                if candidate in INTEREST_GIFTS and candidate not in said:
                    said.append(candidate)
        if said:
            return said
    return said


def present_known(interests=(), memory=None, understood=None):
    wanted = _interest_phrase(interests)
    picks = []
    for interest in interests or ():
        for item, price in INTEREST_GIFTS.get(str(interest).lower(), ()):
            if item not in [name for name, _ in picks]:
                picks.append((item, price))
    if not picks:
        return None
    picks.sort(key=lambda pair: pair[1])
    named = ["%s (%s)" % (item, _money(price)) for item, price in picks[:3]]
    listed = named[0] if len(named) == 1 else ", ".join(named[:-1]) + " or " + named[-1]
    sentence = ("For someone into %s: %s. Buy the one {they} will actually use rather than three "
                "{they} might, and put a real message in the card." % (wanted, listed))
    if memory is None and understood is None:
        return sentence
    return about_them(sentence)(memory or {}, understood or {})


PRICE_SAID = re.compile(r"\u00a3|\d+\s*(?:pounds?|quid)\b|\bunder\s+\d|\bbudget\b", re.IGNORECASE)
A_VERDICT_WORD = (r"(?:weird|odd|tacky|rude|appropriate|all\s+right|ok|okay|too\s+much|"
                  r"too\s+little|too\s+expensive|too\s+cheap|wrong|enough|worth\s+it|"
                  r"worth\s+the\s+money|a\s+good\s+(?:present|gift|idea)|"
                  r"a\s+bad\s+(?:present|gift|idea))")
A_VERDICT_ON_A_PRESENT = re.compile(
    r"\b(?:is|would|will|was)\s+(?:(?:that|it|this|a|an|my|the)\s+)?[^?.!]{0,40}?"
    r"\b" + A_VERDICT_WORD + r"\b", re.I)

A_VERDICT_THING = re.compile(
    r"\b(?:is|would|will|was)\s+(?:(?:that|it|this)\s+)?"
    r"([^?.!,]{2,30}?)\s+(?:be\s+)?(?:" + A_VERDICT_WORD + r")\b", re.I)

VERDICT_YES = (
    "No, that is a good pick at {age}: {thing} gets used every day, and the plain one with room "
    "to grow beats the flashy one.",
    "Not at all - at {age} {thing} is exactly the kind of present that gets used. Plain and "
    "sturdy is the right call there.",
    "That sounds right to me: at {age}, {thing} is a good present, and asking the parents what "
    "they already have too much of saves you buying the second one.",
)
MONEY_VERDICT_YES = (
    "No need to spend much: at {age} {thing} is a good present, and the plain one is the one that "
    "gets used, so the extra money buys nothing the child will notice.",
    "No, and cheap is right here: at {age} {thing} gets used hard, and the basic version lasts as "
    "long as the expensive one.",
)
A_VERDICT_ABOUT_MONEY = re.compile(
    r"\b(?:too\s+expensive|too\s+cheap|expensive|cost|costs|price|pricier|worth\s+it|spend|"
    r"spending|afford|afford\s+it)\b", re.I)
A_CARD_IS_NOT_A_PRESENT = re.compile(
    r"\bcard(?:s)?\b", re.I)
NOT_THAT_CARD = re.compile(
    r"\b(?:bank|debit|credit|sim|sd|memory|store|loyalty|id|payment|graphics|smart|gift)\s*"
    r"cards?\b|\bcard\s+(?:declined|blocked|number|details|payment|reader|machine)\b", re.I)
CARD_AFTER_A_PRESENT = (
    "The card is the part people keep: two lines in your own words - one thing they did that you "
    "still think about, and a wish - beats anything printed inside it.",
    "A card is worth the five minutes. One specific line about them, no joke off the shelf, and "
    "your name at the bottom, because that is the bit they keep.",
    "Write the card yourself rather than signing a printed one: name the thing you like about "
    "them and what you hope for them, and stop there.",
)


def the_card_after_a_present(understood, memory=None, line=None):
    said = line if isinstance(line, str) and line.strip() else _said_line(understood)
    if not A_CARD_IS_NOT_A_PRESENT.search(said or "") or NOT_THAT_CARD.search(said or ""):
        return None
    return pick(CARD_AFTER_A_PRESENT, memory or {}, said)


A_CHEAP_ASK = re.compile(
    r"\b(?:cheap|cheaper|cheapest|inexpensive|budget|tenner|fiver|stocking\s+fillers?|"
    r"stocking\s+filler|secret\s+santa|small\s+gifts?|small\s+presents?|little\s+gifts?|"
    r"under\s+a\s+(?:tenner|fiver|ten|five))\b", re.I)


GIFT_FOR_A_CONDITION = (
    (("doesnt drink", "doesn't drink", "does not drink", "not drinking", "non drinker",
      "non-drinker", "nondrinker", "teetotal", "teetotaller", "sober", "given up drinking",
      "given up alcohol", "gave up drinking", "stopped drinking", "off the drink",
      "no alcohol", "cant drink", "can't drink", "cannot drink", "not a drinker"),
     "Keep the alcohol out of it, even in a hamper: a good alcohol-free bottle (Lyre's or "
     "Seedlip), a proper coffee or a loose-leaf tea set, or a voucher for a meal out.",
     ("a decent bottle of what he already drinks, ",
      "a decent bottle of what he already drinks",
      "a little of something she loves to eat, ",
      "a bottle of what she already drinks, ")),
    (("vegetarian", "veggie", "vegan", "plant based", "doesnt eat meat", "doesn't eat meat",
      "no meat", "pescatarian"),
     "And buy into the vegetarian side of it: a good vegetarian cookbook, a voucher for a veggie "
     "restaurant, or a decent olive oil and a spice set rather than a hamper of pate.",
     ()),
    (("diabetic", "diabetes", "on a diet", "dieting", "watching sugar", "no sugar",
      "cutting out sugar", "blood sugar"),
     "Keep the sugar out of it: no chocolates or biscuit hamper - a magazine or audiobook "
     "subscription, or something for a hobby they already have, works better.",
     ("chocolates", )),
    (("coeliac", "celiac", "gluten free", "gluten-free", "dairy free", "dairy-free",
      "lactose", "allergy", "allergic", "allergies", "nut allergy", "intolerance"),
     "And nothing that might hold what they cannot eat: a voucher, a plant, or something for a "
     "hobby beats a hamper or a box of chocolates.",
     ()),
)


def not_a_present(understood):
    return not reading.gift_ask(understood)


_PRESENT_PEOPLE = ("mum", "mom", "mother", "dad", "father", "sister", "brother", "son", "daughter",
                   "wife", "husband", "partner", "grandad", "grandma", "nan", "granny", "aunt",
                   "uncle", "cousin", "friend", "mate", "colleague", "coworker", "boss",
                   "neighbour", "neighbor", "teacher", "carer", "nurse", "stepmum", "stepdad",
                   "boyfriend", "girlfriend", "teenager", "child", "baby")


def _the_condition_in(text):
    text = " " + str(text or "").lower() + " "
    for phrases, sentence, drop in GIFT_FOR_A_CONDITION:
        if any(phrase in text for phrase in phrases):
            return sentence, drop
    return None


def _the_condition_gift(understood, memory=None):
    line = str(_said_line(understood) or "")
    found = _the_condition_in(line)
    if found is None:
        low = " " + line.lower() + " "
        if not any(" " + word + " " in low or " " + word + "s " in low
                   for word in _PRESENT_PEOPLE):
            turns = (memory or {}).get("turns")
            if isinstance(turns, list):
                earlier = " ".join(str(turn.get("user") or "") for turn in turns[-2:]
                                   if isinstance(turn, dict))
                found = _the_condition_in(earlier)
    return found or ("", ())


def _present_answer(text):
    def reply(memory, understood):
        return _with_the_condition(text, understood, memory)
    return reply


def _the_thing_a_verdict_is_about(line):
    found = A_VERDICT_THING.search(str(line or ""))
    if not found:
        return ""
    thing = " ".join(found.group(1).split())
    thing = re.sub(r"^(?:(?:that|it|this)\s+)+", "", thing, flags=re.I)
    if thing.lower() in ("a", "an", "the", "my", "some", "a gift", "a present", "that", "it",
                         "this", "them", "they"):
        return ""
    if not thing or not re.search(r"[a-z]{3}", thing, re.I):
        return ""
    return thing


def _the_only_age_in_the_store(memory):
    ages = []
    for entry in (memory or {}).get("others") or ():
        if isinstance(entry, dict) and people._with_an_age(entry):
            ages.append(people._age(entry))
    held = (memory or {}).get("their_age")
    if isinstance(held, dict) and people._with_an_age(held):
        ages.append(people._age(held))
    if len(ages) == 1 and ages[0] is not None:
        return ages[0]
    return None


NOT_THE_THING = frozenset("""
that this they them their there here what have has had with from your yours been being every
each some more most much only also just like both other another same sure back over into than
then age ages day days hour hours week weeks month months year years time times little bit
lot lots thing things present present gift gifts idea ideas kind sort
""".split())


def _a_pick_for_that_age(pool, thing):
    if not pool or not thing:
        return False
    thing = re.sub(r"^(?:a|an|the|my|some)\s+", "", thing.strip(), flags=re.I)
    words = [word for word in re.findall(r"[a-z]+", thing.lower())
             if len(word) > 2 and word not in NOT_THE_THING]
    if not words:
        return False
    low = pool.lower()
    return any(re.search(r"\b" + re.escape(word) + r"s?\b", low) for word in words)


def the_verdict_on_a_present(memory, understood):
    line = _said_line(understood)
    if not A_VERDICT_ON_A_PRESENT.search(line):
        return None
    thing = _the_thing_a_verdict_is_about(line)
    held = _an_age_in_the_line(understood) or people.the_age_of_the_person_they_mean(
        memory, understood) or _the_only_age_in_the_store(memory)
    if not held:
        return None
    pool = _gift_for_an_age(held)
    if not thing:
        return None
    if not _a_pick_for_that_age(pool, thing):
        return None
    age = str(int(held)) if float(held) == int(held) else str(held)
    if held < 1:
        age = "a baby"
    elif held == 1:
        age = "one"
    pool_of_words = MONEY_VERDICT_YES if A_VERDICT_ABOUT_MONEY.search(line) else VERDICT_YES
    return pick(pool_of_words, memory, line).format(age=age, thing=thing)


def _gift_row(fallback):
    def reply(memory, understood):
        verdict = the_verdict_on_a_present(memory, understood)
        if verdict:
            return verdict
        if A_VERDICT_ON_A_PRESENT.search(_said_line(understood)):
            return None
        if not reading.gift_ask(understood):
            if A_CARD_IS_NOT_A_PRESENT.search(_said_line(understood)):
                return None
            return fallback
        if PRICE_SAID.search(_said_line(understood)):
            return None
        if A_CHEAP_ASK.search(_said_line(understood)):
            cheap = _gift_cheap(memory, understood)
            return _with_the_condition(cheap, understood, memory) if cheap else None
        if not _knows_a_taste(memory, understood):
            baby = _the_newborn_present(memory, understood)
            if baby:
                return _with_the_condition(baby, understood, memory)
            pool = _gift_for_an_age(
                _an_age_in_the_line(understood)
                or people.the_age_of_the_person_they_mean(memory, understood))
            if pool:
                return _with_the_condition(pool, understood, memory)
            if _only_a_them_says_who(understood):
                return None
            return _with_the_condition(fallback, understood, memory)
        if PRICE_SAID.search(_said_line(understood)):
            return None
        picks = present_known(_the_tastes(memory, understood), memory, understood)
        return _with_the_condition(picks or fallback, understood, memory)
    return reply


PLURAL_ONLY = re.compile(r"\b(?:them|they|theirs|their)\b", re.I)
PLURAL_WORDS = frozenset("they them their theirs".split())


def _only_a_them_says_who(understood):
    if not PLURAL_ONLY.search(_said_line(understood)):
        return False
    return not (_the_words(_said_line(understood)) & (PERSON_WORDS - PLURAL_WORDS))


def _the_newborn_present(memory, understood):
    if not newborn.the_thread_has_a_new_baby(memory, understood):
        return None
    return _gift_for_an_age(0.5)


def _with_the_condition(text, understood, memory=None):
    if not text:
        return text
    note, drop = _the_condition_gift(understood, memory)
    if not note or note.lower() in str(text).lower():
        return text
    answer = str(text)
    for phrase in drop:
        answer = answer.replace(phrase, "")
    return answer.rstrip() + " " + note


def _gift_anyone(memory, understood):
    if not reading.gift_ask(understood):
        return None
    if _knows_a_taste(memory, understood):
        picks = present_known(_the_tastes(memory, understood), memory, understood)
        if picks:
            return picks
        return None
    held = people.the_age_of_the_person_they_mean(memory, understood)
    pool = _gift_for_an_age(held) or _the_newborn_present(memory, understood)
    if pool:
        return _with_the_condition(pool, understood, memory)
    if people.a_child_the_chat_is_about(memory, understood):
        return _with_the_condition(CHILD_GIFT, understood, memory)
    return _with_the_condition(_GIFT_ANYONE, understood, memory)


def _laptop_general(memory, understood):
    return ("Get 16GB of RAM and a 512GB SSD if the budget stretches, 8GB and 256GB if it doesn't, "
            "and a 13 or 14 inch screen for carrying about. Don't pay for a graphics card unless "
            "you game or edit video; a good screen and keyboard matter far more day to day.")


GIFT_ASK = ("gift", "present", "get", "got", "buy", "christmas", "birthday", "60th", "70th",
            "80th", "idea", "for my", "for his", "for her")

LOSS = ("died", "death", "passed away", "funeral", "buried", "grief", "grieving",
        "bereavement", "widow", "miss her", "miss him", "miss mum", "miss dad")

CRISIS = ("fell", "fall", "fallen", "floor", "cant get up", "can't get up", "cannot get up",
          "hospital", "ambulance", "unresponsive", "not breathing", "collapsed", "stroke",
          "chest pain", "in a coma")
CHOOSING = (("pick", "picking", "choose", "choosing", "choice"),
            ("buy", "buying", "get a", "getting a", "shopping",
             "need a", "need some", "want a", "looking for a"),
            ("which", "what should i", "what to look for", "look for", "recommend",
             "recommendation", "suggestion",
             "what to get", "which to get", "what to buy", "which to buy", "dont know what",
             "don't know what", "not sure what", "not sure which", "which laptop", "laptop to get",
             "what laptop"),
            ("worth", "worth it", "best", "spend", "budget", "upgrade", "replace"),
            ("how much ram", "how much memory", "how much storage", "what specs", "specs",
             "processor", "how fast",
             "what size", "how big", "screen size"))


PERSON_ASK = ("gift", "present", "presents", "what should i get", "what should i buy",
              "what can i get", "what can i buy", "what to get", "what to buy",
              "what would you get", "what would you buy", "what do i get", "what do i buy",
              "what do you get", "what do you buy", "what do you give", "what do you get them",
              "what do you buy them", "what to get them", "what should i bring",
              "what can i give", "what to give", "what should i give", "what could i give",
              "what do i give", "what would you give")

TODDLER_GIFT = (
    "For a toddler, one thing they will use every day beats a pile of toys: a set of chunky "
    "blocks, a ball, a book with flaps to lift, or a scooter they will still fit next year. Ask "
    "the parents what they already have too much of, and buy the batteries with it.")
CHILD_GIFT = (
    "For that age, one thing they will use every day beats a pile of toys: a scooter, duplo, "
    "sticker and activity books, or a decent football. Ask the parents what they already have "
    "too much of, and buy the batteries with it. Wrap it in something they can play with "
    "afterwards.")
TEEN_GIFT = (
    "For a teenager, money or a voucher beats a guess, and headphones, gaming credit, a hoodie "
    "from a shop they like or a ticket to something are the safe few. Ask them once, buy the "
    "thing they named, and keep the change in a card with a real message in it.")
GROWN_GIFT = (
    "For that age, buy something they would use every week and would not buy themselves: good "
    "coffee or tea, a bottle of what they already drink, a voucher for a place they like, or a "
    "book by an author they follow. One useful thing beats a pile of small ones.")


def _openings(*pools):
    out = []
    for pool in pools:
        for row in ((pool, ) if isinstance(pool, str) else pool):
            if isinstance(row, str) and len(row.strip()) > 20:
                out.append(" ".join(row.split())[:28])
    return tuple(out)


PRESENT_OPENINGS = _openings(
    TODDLER_GIFT, CHILD_GIFT, TEEN_GIFT, GROWN_GIFT, _GIFT_ANYONE, CHEAP_ADULT, CHEAP_CHILD,
    CHEAP_TEEN)


def a_present_was_answered(memory):
    from ..memory import last_bot
    said = " ".join(str(last_bot(memory) or "").split())
    if not said:
        return False
    return any(opening in said for opening in PRESENT_OPENINGS)


AGE_ASK = ("gift", "presents", "present", "what should i get", "what should i buy",
           "what can i get", "what can i buy", "what to get", "what to buy",
           "what would you get", "what would you buy", "what do i get", "what do i buy",
           "what do you get", "what do you buy", "what do you give", "what do you get them",
           "what do you buy them", "what to get them",
           "what can i give", "what to give", "what should i give", "what do i give")

APPLIANCE_VALUE = (
    (("air fryer", "air fryers", "airfryer"),
     "An air fryer is a small oven that blows hot air fast: chips, roast veg and salmon in 10 to 15 "
     "minutes with a spoon of oil. Worth it for one or two people who hate heating a big oven; skip "
     "it for four, since a 4-litre basket is one tray. £50 to £80 is plenty."),
    (("slow cooker", "slow cookers"),
     "A slow cooker is worth it if you are out all day: load it before work and cheap cuts are "
     "tender by dinner. Skip it if you want anything crisp or fast. A £30 one cooks the same as "
     "a £100 one."),
    (("pressure cooker", "instant pot", "pressure cookers"),
     "A pressure cooker is worth it if you cook beans, stews or tough meat from scratch: a beef stew is 40 minutes "
     "instead of two hours, and dried beans are 25. Skip it for anything quick or crisp, and know "
     "that it is a big pan to store. A 6-litre one suits most kitchens."),
    (("bread maker", "bread machine", "bread makers"),
     "A bread maker is not worth it for most people: skip it unless you eat a loaf a day, since it "
     "takes three to four hours for a small loaf with a soft crust, and a £15 tin in a hot oven "
     "makes better bread. It earns its space only if you want the dough made overnight with no "
     "hands."),
    (("dishwasher", "dishwashers"),
     "A dishwasher is worth it for three or more people: it uses less water than washing up by hand "
     "and saves about half an hour a day. Skip it if you live alone and cook little, since filling "
     "it takes a week. Check the noise (under 45dB) if the kitchen is also the living room, and a "
     "45cm slimline model fits a small kitchen."),
    (("heat pump dryer", "heat pump dryers", "heat pump tumble dryer", "heat pump tumble drier",
      "heat pump drier", "heat pump condensing dryer"),
     "A heat pump dryer is worth it if you dry two or more loads a week: it uses about half the "
     "electricity of a vented one, roughly 25p a cycle against 60p, so 150 to 200 pounds more up "
     "front pays back in about two years. It runs cooler, so a load takes an hour longer, and the "
     "fluff filter and condenser want clearing often. Skip it if you dry rarely, if the room is "
     "cold, or if you have nowhere to empty the water."),
    (("tumble dryer", "tumble dryers"),
     "A tumble dryer is worth it if you have no outside space or a house full of laundry: a heat-pump dryer costs more "
     "(£350 up) but uses about half the electricity of a vented one. Skip it if you have a "
     "garden and an airer: it is the most expensive way to dry clothes."),
    (("smart thermostat", "smart thermostats", "heating thermostat", "nest thermostat",
      "hive thermostat", "tado", "thermostatic radiator valve", "thermostatic radiator valves",
      "trv", "trvs"),
     "A smart thermostat is worth it if the house is empty in the day: about £50 to £100 a year "
     "off a gas bill, so £150 to £250 fitted pays back in two to three years. Skip it if someone "
     "is home all day, or if the heating is already set to come on only when you are in: turning "
     "the flow temperature down and putting thermostatic valves on the radiators gets much of the "
     "saving for a fraction of the price."),
    (("water filter jug", "water filter jugs", "filter jug", "brita", "water filter"),
     "A water filter changes the taste and takes out the chlorine, and a plumbed-in one under the "
     "sink is the same job done once instead of every jug: neither softens hard water nor takes out "
     "much else. Worth it if your tap water tastes of "
     "chlorine and you drink it cold all day, at about £20 for the jug and £4 a month for cartridges. "
     "A jug of tap water left in the fridge overnight does most of the same for nothing, so try "
     "that first."),
    (("humidifier", "humidifiers"),
     "A humidifier is worth it in one dry room, usually a bedroom with the heating on and the "
     "windows shut, if you wake with a dry throat or nosebleeds, or have a cold. Skip it in a room "
     "that has damp on the walls or condensation on the glass, because adding moisture makes that "
     "worse, and clean it every week: a dirty humidifier sprays mould into the air. £30 to £60 for "
     "a cool-mist one."),
    (("mattress topper", "mattress toppers", "bed topper"),
     "A mattress topper is worth it if the mattress is sound but too firm, or you want it softer: "
     "5cm of memory foam or a wool topper costs £60 to £120 and changes the feel for a fraction of "
     "a new mattress. It will not fix a mattress that sags, is over about eight years old or gives "
     "you backache, and a topper on a bad mattress is £100 spent on the wrong thing."),
    (("water softener", "water softeners", "water softening"),
     "A water softener is worth it in a hard water area if scale is a daily nuisance: kettles, "
     "shower screens and the washing machine stop furring up, and the boiler keeps its efficiency. "
     "It is about £1,000 to £2,000 fitted plus £100 to £150 a year in salt, so it is a family and "
     "hard-water answer rather than a flat one. A filter jug does not soften water, and a magnetic "
     "or electronic conditioner does not take the calcium out."),
    (("robot mower", "robot mowers", "robot lawn mower", "robotic mower"),
     "A robot mower is worth it for a flat, open lawn with no narrow gaps: it cuts a little every "
     "day, so the grass stays tidy and there is no grass to collect. It costs £500 to £1,500 and "
     "most need a boundary wire laid round the edge. Skip it for a small lawn, a steep slope, or one "
     "full of bulbs and toys."),
    (("video doorbell", "video doorbells", "ring doorbell", "doorbell camera"),
     "A video doorbell is worth it if parcels go missing or you cannot hear the door from where you "
     "work: £50 to £120, and stored clips usually need a subscription of £2 to £4 a month unless you "
     "take a local-storage model. Wired is more reliable than battery. Point it at your own path and "
     "door rather than the pavement, and if you rent, ask before drilling."),
    (("fan heater", "fan heaters", "electric heater", "electric heaters", "oil filled radiator",
      "convector heater", "space heater", "halogen heater"),
     "A fan heater is worth it for one room for twenty minutes, not for a whole evening or a whole "
     "house: cheap to buy at £20 to £40 and dear to run, since 2kW is about 60p an hour on current "
     "electricity prices. For a room you sit in, an oil-filled radiator is silent and "
     "holds the heat after it clicks off, and heating the person beats heating the room: a throw, "
     "a hot water bottle and warm socks are free after the first winter."),
    (("fan", "fans", "electric fan", "tower fan", "pedestal fan", "desk fan", "floor fan",
      "standing fan", "cooling fan"),
     "A fan does not cool the air, it moves it, and moving air over your skin is enough to feel a "
     "few degrees cooler, so it is worth it for sleeping in a hot room: a tower or pedestal fan at "
     "£25 to £60 is much quieter than a cheap one, and it costs a penny or two an hour to run. Put "
     "it in the window at night to pull cool air in, and skip portable air conditioning unless the "
     "room is also humid, since that is the expensive way round."),
    (("robot vacuum", "robot hoover", "robot vacuums"),
     "A robot vacuum is worth it as a daily top-up on hard floors and one level, not as a deep "
     "clean: skip it if the floor has stairs, thick rugs or a trail of cables and toys, since it "
     "will not get them and you still empty it. Best value in a house with a pet that sheds."),
    (("dehumidifier", "dehumidifiers"),
     "A dehumidifier is worth it in a flat that steams up and grows black mould on the window frames: a 10 to 12 "
     "litre one dries washing indoors and stops the mould, which costs more to fix than the machine. "
     "Skip it if the damp is a leak or a broken gutter, since that needs fixing at the source."),
    (("coffee machine", "bean to cup", "coffee machines"),
     "A coffee machine is worth it if you drink two coffees a day at home: a £150 bean-to-cup pays for itself in "
     "about three months against buying them out. Skip it if you have one coffee a day: a £30 "
     "filter machine with fresh ground coffee tastes better than a cheap pod machine, and the pods "
     "are the expensive part."),
    (("stand mixer", "kitchenaid", "stand mixers"),
     "A stand mixer is worth it if you bake most weeks: it creams butter and kneads dough for you and lasts decades. "
     "Skip it if you bake a few times a year: a £15 hand mixer does the same job and lives in a "
     "drawer."),
    (("meal kit", "meal kits", "recipe box", "hello fresh", "gousto"),
     "A meal kit is worth it for the decision taken away, not the food: about £5 a portion and "
     "no waste. Skip it if you already cook, since the same dinner is £1.50 a portion from a "
     "supermarket. Try two boxes and cancel."),
    (("kindle", "e reader", "ereader", "e-reader"),
     "A Kindle is worth it if you read in bed or travel: a Paperwhite is readable in the dark, holds "
     "hundreds of books and the battery lasts weeks. Skip it if you mostly read at home: library "
     "ebooks through Libby or BorrowBox are free on a phone, and paper is better for anything with "
     "maps or photos. Buy last year's model, not the newest."),
    (("noise cancelling headphones", "noise cancelling headphone", "noise cancelling"),
     "Noise cancelling headphones are worth it if you commute by train, plane or sit in a loud "
     "office: over-ear ones cut the engine noise that earbuds let through. About £70 to £120 "
     "is the sweet spot, and last year's model sounds the same as the new one for half the price. "
     "Skip them for a quiet room or for cycling, where hearing traffic matters."),
    (("fitness tracker", "fitness trackers", "fitbit"),
     "A fitness tracker is worth it for steps and sleep, not for the heart-rate number: a £25 band "
     "counts steps and sleep well, and a watch ten times the price adds mostly a screen and GPS. Skip "
     "it if you already walk enough and know it, since most people stop looking after a month."),
    (("smart watch", "smart watches", "apple watch"),
     "A smart watch is worth it if you want notifications, contactless payment and a run tracker on "
     "your wrist without getting your phone out. Skip it if you only want steps, where a £25 band "
     "does the same. An iPhone pairs best with an Apple Watch, an Android with a Wear OS watch or a "
     "Garmin."),
    (("standing desk", "standing desks", "sit stand desk"),
     "A standing desk is worth it if you sit for eight hours and your back aches, and the useful part "
     "is changing position rather than standing all day: a £25 riser on the desk you have does most "
     "of it. Skip the motorised ones unless you know you will raise them, and stand for 20 minutes at "
     "a time rather than the afternoon."),
    (("weighted blanket", "weighted blankets"),
     "A weighted blanket is worth it if the feeling of weight settles you: about 10% of your body "
     "weight is the usual guide, and it helps some people fall asleep and does nothing for others. "
     "Skip it for a toddler, or for anyone who could not push it off, and try one under a duvet "
     "before spending £60."),
    (("steam cleaner", "steam cleaners", "steam mop"),
     "A steam cleaner is worth it for hard floors, tiles and grout, and the bathroom: it lifts grease "
     "with no chemicals and the water is free after the machine. Skip it on laminate, unsealed wood "
     "and anywhere the moisture can get under the floor, and skip it for carpets, where a hire "
     "machine once a year is cheaper than owning one."),
    (("a cleaner", "the cleaner", "my cleaner", "our cleaner", "cleaners worth",
      "cleaning lady", "cleaning service", "housekeeper"),
     "A cleaner is worth it if two hours back at the weekend matter more than £15 to £20 an "
     "hour: two hours a fortnight covers a flat. Go through an agency with insurance, agree in "
     "writing what is included and be in the first time. Skip it while you are paying off a debt."),
    (("food processor", "food processors", "kitchen machine"),
     "A food processor is worth it if you chop a lot of onions or make pastry: it does in a minute "
     "what a knife takes ten. Skip it if you cook simply, since it is heavy to wash up for one job. "
     "A £40 one chops as well as a £200 one."),
    (("air purifier", "air purifiers"),
     "An air purifier is worth it in a bedroom if you have hay fever, a cat or a sealed window: a "
     "HEPA filter on low all night changes how you sleep. Skip it for damp, which needs a "
     "dehumidifier, and check the replacement filters are cheap before you buy."),
    (("heated airer", "heated clothes airer", "heated drying rack", "heated clothes horse"),
     "A heated airer is worth it if you dry clothes indoors in winter: about 6p an hour against 50p "
     "or more for a tumble dryer, and it does not shrink anything. Skip it if you have a garden and "
     "dry outside in summer, and buy the larger winged one so a full wash fits on it. A cover cuts "
     "the drying time by half."),
    (("electric blanket", "electric blankets", "heated blanket"),
     "An electric blanket is worth it for a cold bedroom: 20 minutes before bed costs pennies and "
     "beats heating the room all evening. Skip it if it would be on all night, since a hot water "
     "bottle does the same for nothing, and replace one over ten years old."),
    (("microwave", "microwaves"),
     "A microwave is worth it for reheating, porridge, scrambled eggs and defrosting, not for cooking a meal from "
     "scratch: skip it if you want to roast or bake, since an oven does that better. A basic 800W "
     "one is enough; pay more for a bigger turntable and easier controls, not for modes nobody "
     "uses."),
)

CHOICE_VALUE = (
    (("gym membership", "gym memberships", "join a gym", "joining a gym", "gym worth",
      "should i go to the gym", "should i go to gym", "shall i go to the gym",
      "should i go back to the gym", "should i go to the gym again",
      "should i bother going to the gym", "should i bother with the gym",
      "should i bother with a gym", "should i start going to the gym",
      "is it worth going to the gym", "worth going to the gym",
      "any point going to the gym", "should i go to the gym or"),
     "A gym is worth it if the door is within ten minutes of you and you will go twice a week: the "
     "walk decides it, not the equipment. Skip it if the nearest one is a drive away, and pay "
     "monthly rather than a year up front. A £20 leisure-centre one you use beats a £60 "
     "one you dread."),
    (("heat pump dryer", "heat pump tumble dryer", "heat pump drier", "heat pump tumble drier",
      "heat pump dryers", "heat pump condensing dryer"),
     "A heat pump dryer is worth it if you dry two or more loads a week: the cycle uses about half "
     "the electricity of a vented one, roughly 25p against 60p, so it pays back its extra 150 to "
     "200 pounds in about two years. It runs cooler and slower, so a load takes two hours and more, "
     "and it needs the fluff filter and condenser cleared often. Skip it if you dry rarely or have "
     "nowhere for the waste water, and never buy one without a heat pump if the room is cold."),
    (("heat pump", "heat pumps"),
     "A heat pump is worth it if you are replacing the boiler anyway and the house is insulated: the "
     "grant covers a few thousand, the running cost is close to gas, and it heats a well-insulated "
     "home steadily rather than in bursts. Skip it in a draughty house with no wall or loft "
     "insulation, since the insulation comes first and pays back faster."),
    (("electric car", "electric cars", "ev "),
     "An electric car is worth it if you can charge at home and do under about 200 miles a week: "
     "home charging is roughly 3p a mile against 15p for petrol, and there is almost no servicing. "
     "Skip it if you cannot charge at home, or if you regularly do long motorway runs, where public "
     "charging costs nearly as much as fuel."),
    (("smart meter", "smart meters"),
     "A smart meter is worth having: your supplier fits one free, and the in-home display shows "
     "what the kettle and the heating cost as you use them. Ask for a second-generation (SMETS2) one "
     "so it keeps working if you switch supplier. It will not cut the bill on its own."),
    (("water meter", "water meters"),
     "A water meter usually saves money if there are more bedrooms than people: the rule of thumb is "
     "that you pay less on a meter when there are fewer of you than rooms. Check the bill estimate "
     "first, and remember you can go back to an unmetered bill within the first year in England and "
     "Wales if it costs you more."),
    (("season ticket", "season tickets"),
     "A season ticket pays off at about three days a week: below that, the flexible or weekly "
     "options are usually cheaper. Work out the yearly cost against 40 weeks of daily returns "
     "before you commit, and check whether a part-time or flexi season covers the days you "
     "actually travel."),
)

APPLIANCE_ASK = ("worth", "worth it", "worth the money", "should i get", "should i buy",
                 "do i need", "need one", "shall i get", "good buy", "any good", "is it good",
                 "a good", "good cheap", "good and cheap", "the best", "best one",
                 "buy", "buying", "getting", "get one",
                 "should i use", "should we use", "should i try", "is it ok", "is it safe",
                 "should i go", "shall i go", "should we go", "should i start", "should i bother",
                 "is it worth going", "worth going",
                 "would you", "will it help", "does it help",
                 "recommend", "recommended", "recommendation", "recommendations",
                 "will a", "will an", "does a", "does an", "would a", "would an",
                 "will my", "does my", "would my",
                 "any point in", "any point to", "point in a", "point in an", "point in",
                 "point to", "point of a", "point of an", "waste of money",
                 "wasting money", "money well spent", "bother with", "bother")


_METER_FAULT = ("blank", "stopped", "broken", "faulty", "dead", "warning", "error", "gone",
                "connect", "sending", "signal", "wrong", "wtong")
_METER_READ = ("read", "reading", "readings", "button", "show", "shows", "find", "mean", "means",
               "numbers", "figure", "figures", "kwh")


def _smart_meter_how(memory, understood):
    said = str(understood.get("text") or understood.get("clean") or "").lower()
    words = understood.get("words") or []
    if any(word in said for word in _METER_FAULT) or "not working" in said:
        return ("Ring your supplier and say the meter or its display has stopped - it is their "
                "equipment, so fixing it is free, and it is usually a firmware update or a new "
                "display they send out. Photograph the reading on the meter itself before you ring, "
                "and send them a reading weekly until it is sorted, so you are not billed on an "
                "estimate in the meantime.")
    if any(word in _METER_READ for word in words):
        return ("Press the button marked A (some meters say B) until the screen shows a number with "
                "kWh after it - that is your reading, and the one the supplier wants. On a smart "
                "meter the in-home display shows it too, and with a single-rate tariff it is the "
                "only number that matters; a two-rate one shows day and night separately, so send "
                "both.")
    return ""


_DECISION_WORDS = frozenset((
    "a", "an", "the", "i", "me", "my", "we", "us", "our", "you", "your", "it", "its", "im",
    "ive", "id", "is", "are", "was", "were", "am", "do", "does", "did", "doing", "done", "be",
    "been", "being", "should", "shall", "would", "will", "can", "could", "may", "might", "must",
    "worth", "any", "point", "in", "to", "of", "for", "at", "on", "with", "and", "or", "so",
    "if", "that", "this", "these", "those", "then", "than", "now", "today", "tomorrow",
    "tonight", "later", "still", "just", "really", "actually", "honestly", "though", "again",
    "back", "go", "goes", "going", "went", "get", "gets", "getting", "got", "bother",
    "bothering", "start", "starting", "started", "try", "trying", "buy", "buying", "join",
    "joining", "one", "ones", "thing", "things", "time", "times", "not", "no", "yes", "ok",
))
_ACTION_NAME = re.compile(r"\b(go|going|went|start|starting|bother|bothering|try|trying)\b")


def _bare_decision(said, name, ask):
    rest = said
    for phrase in (name,) + tuple(ask):
        phrase = phrase.strip()
        if phrase:
            rest = re.sub(r"\b" + re.escape(phrase) + r"\b", " ", rest)
    return all(word in _DECISION_WORDS for word in re.findall(r"[a-z0-9']+", rest))


def _longest_match_named(said, table):
    best, longest, found = None, -1, ""
    for names, reply in table:
        for name in names:
            name = name.strip()
            if len(name) > longest and re.search(r"\b" + re.escape(name) + r"\b", said):
                best, longest, found = reply, len(name), name
    return best, found


def _longest_match(said, table):
    best, longest = None, -1
    for names, reply in table:
        for name in names:
            name = name.strip()
            if len(name) > longest and re.search(r"\b" + re.escape(name) + r"\b", said):
                best, longest = reply, len(name)
    return best


_TRADER_WORDS = ("builder", "builders", "plumber", "plumbers", "electrician", "electricians",
                 "decorator", "decorators", "plasterer", "plasterers", "roofer", "roofers",
                 "joiner", "joiners", "tiler", "tilers", "carpenter", "carpenters", "gardener",
                 "gardeners", "tradesman", "tradesmen", "trade", "contractor", "contractors",
                 "quote", "quotes", "quotation", "quotations", "day rate", "labour", "estimate")


def _haggle(memory, understood):
    reading = understood if isinstance(understood, dict) else {}
    said = " ".join(str(part) for part in (
        reading.get("clean"), reading.get("text"), " ".join(reading.get("words") or ()))).lower()
    if re.search(r"\brude\b|\bawkward\b|\bembarrass", said):
        return ("No - asking once is normal in a market, a car boot sale, a small independent shop "
                "or on anything big like a sofa, and in a chain with price tags it is still fine "
                "to ask. One question, then take the answer and either buy or leave: asking twice "
                "or arguing after a no is the part that gets awkward.")
    if any(word in said for word in _TRADER_WORDS):
        return ("Get three written quotes first, then ask each trader the same question: what "
                "would bring that down? Supplying the materials, being flexible on dates so the "
                "job fills a gap in their diary, and paying a deposit up front are the three that "
                "work. Compare the quotes line by line rather than on the total, and treat one "
                "miles under the others as a warning: the extras come later.")
    return ("Ask once, cheerfully, once you have picked the thing - \"is there anything you can "
            "do on the price?\" - then stop talking and be ready to walk away: silence and a "
            "customer who will leave are what move a price. Take the display model or last "
            "season's colour, offer to pay in full today, check the online price so they can "
            "match it, and never say your maximum. At a market or car boot sale, offer about two "
            "thirds and settle in the middle.")


_DRYER_WORDS = ("dryer", "dryers", "drier", "driers", "tumble dryer", "tumble drier")

def _choice_value(memory, understood):
    reading = understood if isinstance(understood, dict) else {}
    said = " ".join(str(part) for part in (
        reading.get("clean"), reading.get("text"), " ".join(reading.get("words") or ()))).lower()
    row, name = _longest_match_named(said, CHOICE_VALUE)
    if row is not None and _ACTION_NAME.search(name) and not _bare_decision(said, name, APPLIANCE_ASK):
        return None
    if row is not None and any(word in said for word in _DRYER_WORDS):
        for names, answer in CHOICE_VALUE:
            if any("dryer" in name or "drier" in name for name in names):
                return answer
    return row


def _appliance_value(memory, understood):
    reading = understood if isinstance(understood, dict) else {}
    said = " ".join(str(part) for part in (
        reading.get("clean"), reading.get("text"), " ".join(reading.get("words") or ()))).lower()
    return _longest_match(said, APPLIANCE_VALUE)


EVERYDAY_WHERE = (
    (("stamp", "stamps", "postage", "first class", "second class", "signed for",
      "recorded delivery"),
     "Any post office counter has them, and so do most supermarkets, corner shops and newsagents. "
     "A book of 12 costs less per stamp than singles, and Royal Mail's own site will post a book "
     "out if you are not going past a counter."),
    (("birthday card", "birthday cards", "christmas cards", "christmas card", "greetings card",
      "greetings cards", "card shop", "cards"),
     "A card shop, a supermarket or a petrol station will have one, and the supermarket's own "
     "range is two pounds rather than four. If it is a big one, buy it this week rather than the "
     "day before - the good ones go first."),
    (("envelope", "envelopes", "stationery", "wrapping paper", "note paper", "printer paper",
      "pens", "a pen", "felt tips", "sellotape", "sticky tape", "glue", "a folder"),
     "A stationery shop or the back-to-school aisle of a supermarket has it, and for a batch "
     "envelopes or a box of paper an office supplier is cheaper and delivers. A card shop sells "
     "envelopes on their own if you only need a few."),
    (("sleeping bag", "sleeping bags", "tent", "rucksack", "camping gear", "camping stove",
      "walking boots"),
     "An outdoor shop is where the real ones are: Decathlon for the cheap end, Go Outdoors or a "
     "proper mountaineering shop for the rest. A charity shop or a car boot sale often has a "
     "decent sleeping bag for a tenner, and a borrowed one for a first trip is better than buying."),
    (("paint", "paintbrush", "paintbrushes", "roller", "dust sheet", "dust sheets",
      "undercoat", "primer"),
     "A decorator's merchant rather than a chain for the paint itself: the trade brands cover "
     "better, cost less and they will mix a colour to a sample. For one room, a DIY shop for the "
     "brushes, trays and sheets is fine, and cheap brushes are the false economy - they shed."),
    (("batteries", "battery", "light bulb", "lightbulb", "bulb", "fuse", "plug",
      "extension lead"),
     "A supermarket, a hardware shop or a pound shop has them. Take the old one with you, or "
     "photograph the numbers printed on it, because the size is the thing people get wrong: a "
     "bulb needs its fitting and its wattage, a battery its number, a fuse its amps."),
    (("boxes", "moving boxes", "cardboard boxes", "bubble wrap", "packing tape"),
     "A supermarket will give you banana boxes free if you ask at the customer desk, and a "
     "removal firm sells proper double-walled ones for a few pounds each. Ask on a Monday, "
     "before the delivery cages are taken back."),
)


_INSIDE = re.compile(r"\b(?:in|inside|under|behind|on top of|on)\s+"
                     r"(?:the|my|our|your|their|his|her)\s+([a-z'\u2019]+)")
_MINE = re.compile(r"\b(?:my|our)\b")
_SHOP_PLACES = frozenset("""
    shop shops store stores supermarket supermarkets online internet ebay amazon argos
    town city high street market sale sales chemist chemist's counter department
    """.split())


_THE_EVERYDAY_THINGS = tuple(sorted({name for names, _ in EVERYDAY_WHERE for name in names}))


def _everyday_where(memory, understood):
    reading = understood if isinstance(understood, dict) else {}
    said = " ".join(str(part) for part in (
        reading.get("clean"), reading.get("text"), " ".join(reading.get("words") or ()))).lower()
    if not said:
        return None
    inside = _INSIDE.search(said)
    if inside and inside.group(1) not in _SHOP_PLACES:
        return None
    if "find" in said.split() and _MINE.search(said):
        return None
    return _longest_match(said, EVERYDAY_WHERE)


def _gift_for_an_age(age):
    if age is None:
        return None
    if age < 1:
        return ("Under a year, buy the boring things the parents will use: clothes in the size for "
                "three to six months ahead, a pack of muslins, a board book, or a soft ball. Skip "
                "anything that needs batteries or a cot to hang it from, and skip newborn sizes, "
                "because everyone buys those and the baby grows out of them in a fortnight.")
    if age >= 20:
        return GROWN_GIFT
    if age >= 13:
        return TEEN_GIFT
    return TODDLER_GIFT if age <= 2 else CHILD_GIFT


TURNING = re.compile(r"\b(?:turning|turns)\s+(?P<age>\d{1,3})\b", re.I)


def _an_age_in_the_line(understood):
    for number in (understood or {}).get("numbers") or []:
        if number.get("unit") == "months":
            return number.get("value") / 12.0
        if number.get("unit") == "years":
            return number.get("value")
    line = " ".join(str((understood or {}).get("clean") or "").lower().split())
    turning = TURNING.search(line)
    if turning:
        age = int(turning.group("age"))
        if 0 <= age <= 120 and any(number.get("value") == age
                                   for number in (understood or {}).get("numbers") or []):
            return age
    return None


CHILD_PEOPLE = ("son", "daughter", "child", "children", "kid", "kids", "niece", "nephew",
                "grandson", "granddaughter", "grandchild", "grandchildren", "boy", "girl",
                "boys", "girls", "lad", "lads", "lass", "little one", "youngest", "eldest",
                "stepson", "stepdaughter", "godson", "goddaughter", "toddler",
                "schoolboy", "schoolgirl")


def _a_child_is_the_one_they_buy_for(understood):
    words = _the_words(_said_line(understood))
    if words & set(CHILD_PEOPLE):
        return True
    return bool(words & {"teenager", "teenagers", "teen", "teens", "teenage",
                         "schoolkid", "schoolkids", "schoolboy", "schoolgirl"})


def _the_person_row(adult, child):
    grown_up = _gift_row(adult)
    young = _gift_row(child)

    def reply(memory, understood):
        chosen = young if _a_child_is_the_one_they_buy_for(understood) else grown_up
        return chosen(memory, understood)
    return reply


CHILD_PRESENT = ("For a child the age is most of the answer, so it is worth asking. Under three, "
                 "something to push, stack or post. Four to seven, something to build, draw or "
                 "dress up. Eight to eleven, a kit or a game with real pieces. Twelve and up, "
                 "money towards one thing they have chosen. With no age to go on, a good book and "
                 "a small craft set is the safe pair, and paper and ribbon do the rest.")


_AGE_WORDS = ("one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|thirteen"
              "|fourteen|fifteen|sixteen|seventeen|eighteen|nineteen")
_AN_AGE = r"(?:\d{1,3}|" + _AGE_WORDS + r")"

_A_CHILDS_AGE = re.compile(
    r"\b(?:"
    r"" + _AN_AGE + r"\s*(?:yr|yrs|year|years|yr-old|year-old)\s*(?:old|ole)?\b"
    r"|" + _AN_AGE + r"\s*months?\b"
    r"|\b(?:hes|shes|he's|she's|he is|she is|who is|that is|is|aged|age|turning)\s*"
    r"" + _AN_AGE + r"\b"
    r"|\b(?:1[0-9]|[1-9])(?:st|nd|rd|th)\b"
    r"|\b(?:toddler|toddlers|preschool|preschooler|newborn|new born|teen|teens|teenager"
    r"|teenagers|teenage)\b"
    r")")


_SAID_AS_WORDS = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7,
                  "eight": 8, "nine": 9, "ten": 10, "eleven": 11, "twelve": 12, "thirteen": 13,
                  "fourteen": 14, "fifteen": 15, "sixteen": 16, "seventeen": 17,
                  "eighteen": 18, "nineteen": 19}

_AN_AGE_SAID = re.compile(
    r"\b(?:(?P<years>" + _AN_AGE + r")\s*(?:yr|yrs|year|years|yr-old|year-old)\b"
    r"|(?P<months>\d{1,2}|" + _AGE_WORDS + r")\s*months?\b"
    r"|(?:hes|shes|he's|she's|he is|she is|who is|that is|is|aged|age|turning)\s*"
    r"(?P<near>" + _AN_AGE + r")\b"
    r"|(?P<ordinal>1[0-9]|[1-9])(?:st|nd|rd|th)\b)")


def _an_age_given(said):
    if said.isdigit():
        return int(said)
    return _SAID_AS_WORDS.get(said)


def _an_age_said_in_the_line(line):
    found = _AN_AGE_SAID.search(str(line or "").lower())
    if not found:
        return None
    if found.group("months"):
        months = _an_age_given(found.group("months"))
        return months / 12.0 if months else None
    for name in ("years", "near", "ordinal"):
        if found.group(name):
            age = _an_age_given(found.group(name))
            return float(age) if age is not None else None
    return None


def _names_a_childs_age(line):
    if isinstance(line, dict):
        line = line.get("clean") or line.get("text") or ""
    text = str(line or "").lower()
    return bool(_A_CHILDS_AGE.search(text))


def _this_row_answers_the_line(line):
    if isinstance(line, dict):
        line = line.get("clean") or line.get("text") or ""
    text = str(line or "").lower()
    if not text:
        return False
    named = _a_child_is_named(text)
    if not _A_CHILDS_AGE.search(text):
        return not named
    age = _an_age_said_in_the_line(text)
    if named and age is not None and age > 19:
        return False
    return True


def _a_child_is_named(text):
    words = re.findall(r"[a-z']+", str(text or "").lower())
    for person in CHILD_PEOPLE:
        if " " in person:
            if person in text:
                return True
        elif person in words:
            return True
    return False


def _gift_by_age(memory, understood):
    low = str((understood or {}).get("clean") or (understood or {}).get("text") or "").lower()
    chosen = _gift_for_an_age(_an_age_in_the_line(understood)
                              or _an_age_said_in_the_line(low))
    if chosen:
        return chosen
    if re.search(r"\b(?:toddler|toddlers|preschool|preschooler|baby|babies)\b", low):
        return TODDLER_GIFT
    if re.search(r"\b(?:teen|teens|teenager|teenagers|teenage)\b", low):
        return TEEN_GIFT
    return CHILD_GIFT


def _the_age_row(memory, understood):
    card = the_card_after_a_present(understood, memory)
    if card:
        return card
    return _gift_by_age(memory, understood)


_WATCH_SMART = ("smart watch", "smartwatch", "smart watches", "smartwatches", "apple watch",
                "garmin", "fitbit", "galaxy watch", "fitness watch", "watch for running",
                "watch for steps", "track my steps", "track my sleep")
_WATCH_PLAIN = ("For a first proper watch, a plain quartz from Casio or Timex at £40 to £150 keeps "
                "better time than anything dearer; a mechanical watch is for people who enjoy "
                "them, not for accuracy. Look for a sapphire crystal if you can, 50m water "
                "resistance and a strap you can change yourself. What will you mostly wear it "
                "with?")
_WATCH_SMART_SAY = ("Buy for the battery first: most smartwatches last a day or two, so one that "
                    "lasts a week changes how you use it. A fitness band at £40 to £80 covers "
                    "steps, sleep and notifications; pay £200 to £300 only if you want a screen and "
                    "apps on your wrist, and expect the step and heart-rate numbers to be rough "
                    "rather than medical. Is it for exercise, notifications, or looks?")


_WATCH_VERBS = ("watching", "watched", "to watch", "worth watching", "worth a watch",
                "watch it", "watch on", "should i watch", "binge")
_WATCH_VERB_SHAPE = re.compile(
    r"\bwatch\s+(?:out\b"
    r"|for\s*(?:$|[?.!,;]"
    r"|\b(?:what|how|when|if|that|anything|something|signs?|symptoms?|changes?|it|them|"
    r"him|her|me|us|you)\b))")


def _watch_help(memory, understood):
    forms = [str((understood or {}).get(key) or "").lower()
             for key in ("clean", "norm_text", "norm")]
    said = " ".join(forms)
    if any(word in said for word in _WATCH_SMART):
        return _WATCH_SMART_SAY
    if any(word in said for word in _WATCH_VERBS):
        return None
    if any(_WATCH_VERB_SHAPE.search(form) for form in forms):
        return None
    return _WATCH_PLAIN


INTEREST_GIFTS = {
    "fishing": (("a float and hook kit", 12), ("a decent tackle box", 30),
                ("a landing net", 25), ("a good folding chair for the bank", 40)),
    "angling": (("a float and hook kit", 12), ("a decent tackle box", 30),
                ("a landing net", 25), ("a good folding chair for the bank", 40)),
    "tackle": (("a float and hook kit", 12), ("a decent tackle box", 30)),
    "gardening": (("good gloves that fit", 12), ("a decent trowel", 20),
                  ("secateurs", 30), ("a voucher for the nearest garden centre", 25)),
    "garden": (("good gloves that fit", 12), ("a decent trowel", 20),
               ("secateurs", 30), ("a voucher for the nearest garden centre", 25)),
    "plants": (("a good houseplant in a proper pot", 15), ("a nice watering can", 25)),
    "allotment": (("good gloves that fit", 12), ("secateurs", 30),
                  ("a voucher for the nearest garden centre", 25)),
    "cooking": (("a decent chef's knife", 35), ("a good olive oil and a nice tin", 20),
                ("an apron and a decent wooden spoon", 15)),
    "baking": (("a good loaf tin", 12), ("a set of measuring spoons and a decent vanilla", 12)),
    "reading": (("a paperback they would not pick themselves", 10),
                ("a book token", 20), ("a nice bookmark and a good bar of chocolate", 8)),
    "books": (("a paperback they would not pick themselves", 10),
              ("a book token", 20)),
    "music": (("a record or CD they would not buy", 20), ("a voucher for a record shop", 25)),
    "running": (("a head torch", 20), ("good running socks", 15), ("a decent water bottle", 15)),
    "cycling": (("a good bike light set", 25), ("a decent multi-tool", 20)),
    "football": (("a club shirt", 45), ("good socks and a proper ball", 25)),
    "films": (("a cinema voucher", 20), ("a good film on disc", 12)),
    "photography": (("a decent camera strap", 20), ("a good memory card", 20)),
    "knitting": (("a skein of good wool", 15), ("a decent set of needles", 20)),
    "sewing": (("a good pair of fabric scissors", 20), ("a decent seam ripper and pins", 12)),
    "coffee": (("good ground coffee", 15), ("a decent cafetiere", 25),
               ("a nice mug and a bag of good beans", 20)),
    "tea": (("a proper loose-leaf tea and a strainer", 15), ("a nice mug and good tea", 18)),
    "gaming": (("a voucher for the shop they use", 25), ("a good headset", 35)),
    "birdwatching": (("a decent pair of binoculars", 45), ("a bird book for their area", 15)),
    "diy": (("a good screwdriver set", 25), ("a decent tape measure", 12)),
}

PRESENT_BANDS = (
    (10, "Under {money}, buy one small thing properly rather than three cheap ones: a bar of the "
         "good chocolate, a decent paperback, a nice bar of soap, or good coffee."),
    (20, "For under {money}, buy one thing they will use this month: a decent paperback, good "
         "chocolate, a jar of something they like, or a small plant in a proper pot."),
    (40, "For under {money}, one good thing beats three safe ones: a decent thermos, woolly socks "
         "and a book, good olive oil and a nice tin, or a voucher for something they already do "
         "at the weekend."),
    (100, "Under {money} you can buy an experience rather than an object: two cinema tickets and "
          "dinner, a day out they would not book themselves, or a decent bottle with a good "
          "glass to drink it from."),
)
PRESENT_OVER = ("At {money} there is room for the proper version of something they use every day "
                "and would not spend on themselves - a good bag, a decent pair of boots, or the "
                "thing they have been putting off - and a real message in the card.")


BUY_INTO = (" If you know what they are into, buy into that instead: secateurs for a gardener, "
            "a head torch for a runner, a knife for someone who cooks.")


def _money(amount):
    try:
        amount = int(round(float(amount)))
    except (TypeError, ValueError):
        return ""
    return "\u00a3%d" % amount


def _interest_phrase(interests):
    named = [str(word) for word in interests if word]
    if not named:
        return ""
    if len(named) == 1:
        return named[0]
    return ", ".join(named[:-1]) + " and " + named[-1]


def present_within(money, interests=()):
    wanted = _interest_phrase(interests)
    fits = []
    for interest in interests or ():
        for item, price in INTEREST_GIFTS.get(str(interest).lower(), ()):
            if price <= money and (item, price) not in fits:
                fits.append((item, price))
    fits.sort(key=lambda pair: -pair[1])
    if fits:
        listed = ", ".join("%s (%s)" % (item, _money(price)) for item, price in fits[:2])
        if money >= 40 and fits[0][1] < money / 2:
            return ("%s is plenty for someone into %s: %s, and the rest towards something they "
                    "have been putting off." % (_money(money), wanted, listed))
        return ("%s or less, for someone into %s: %s. Buy the one thing they will actually use "
                "rather than three they might, and put a real message in the card."
                % (_money(money), wanted, listed))
    if not money:
        return PRESENT_OVER.format(money="that")
    for band, advice in PRESENT_BANDS:
        if money <= band:
            return _with_buy_into(advice.format(money=_money(money)), interests)
    return _with_buy_into(PRESENT_OVER.format(money=_money(money)), interests)


def _with_buy_into(advice, interests=()):
    return advice if interests else advice + BUY_INTO


def present_less(interests=()):
    wanted = _interest_phrase(interests)
    fits = []
    for interest in interests or ():
        for item, price in INTEREST_GIFTS.get(str(interest).lower(), ()):
            if item not in [name for name, _ in fits]:
                fits.append((item, price))
    if fits:
        fits.sort(key=lambda pair: pair[1])
        item, price = fits[0]
        return ("Cheaper than that: %s (%s) is the small version of the same idea for someone into "
                "%s, and a good one beats something bigger and cheaper." % (item, _money(price),
                                                                            wanted))
    return ("Cheaper than that: go for the small version of the same idea - a good bar of "
            "chocolate, a decent paperback, nice soap, or a packet of good coffee - and let the "
            "card do the rest.")


_COAT_KINDS = (
    (("down", "puffer", "padded", "padding", "quilted", "synthetic", "insulated",
      "insulation"),
     "Down is the warmest for its weight and packs down small, so look for 600 fill power or "
     "more and it will last a decade, but it insulates badly once it is wet. Synthetic padding "
     "costs about half as much, is heavier and bulkier, and still keeps you warm when damp, "
     "which suits a wet winter better than down unless you want it for real cold."),
    (("wedding", "funeral", "christening", "interview", "smart", "formal", "dress code", "party",
      "office", "town", "work"),
     "For anything smart - a wedding, a funeral, a winter interview - a wool or wool-blend coat "
     "is the answer: it hangs properly over a dress or a suit, and a mid-calf length in navy, "
     "grey, camel or black goes with everything. Check that it closes over the jacket you will "
     "wear underneath and try it on in the shoes you will be standing in, because a heavy coat "
     "pushes the shoulders up."),
    (("wool", "woollen", "woolen", "duffle", "tweed", "overcoat"),
     "A wool coat is warm, smart enough for town and fine in a shower, but it gets heavy once "
     "it is soaked and wants dry cleaning rather than a wash. Check the lining and the buttons, "
     "buy it loose enough for a jumper under it, and keep it for the days you are not out in "
     "the rain."),
    (("waterproof", "rain", "shell", "gore", "storm", "wet"),
     "For rain, a waterproof shell with taped seams (Gore-Tex or similar) at £150 to £250 "
     "outlasts three cheap ones: check the hood, the zip and the seams under the arms, and try "
     "it on over a jumper. A shower-resistant jacket is fine for a dash to the shops and no good "
     "for a wet walk."),
    (("worth", "expensive", "spend", "how much", "cheaper", "budget", "value", "price"),
     "Yes, if it is one you will wear for years: a coat is the piece of clothing where the money "
     "shows, and £80 to £150 buys a padded coat that lasts a decade, £150 to £250 a waterproof "
     "shell that does not leak at the shoulders. Cheap coats cost more in the end because the "
     "zip goes and the seams soak through, so buy the best you can in a plain colour you will "
     "still wear in five years."),
)

_COAT_CHECK = ("Check the hood stays up in wind, the zip works with gloves on, the seams are taped "
               "and there is room for a jumper underneath. Look at the lining where it rubs under "
               "the arm and at the stitching on the pockets: those are the two places a cheap coat "
               "shows itself first.")
_HEIGHT = re.compile(r"\b(\d)\s*(?:foot|feet|ft|')\s*(\d{1,2})\b")


def _coat_to_buy(memory, understood):
    reading = understood if isinstance(understood, dict) else {}
    said = " ".join(str(part) for part in (
        reading.get("clean"), reading.get("text"), " ".join(reading.get("words") or ())
    )).lower()
    tall = _HEIGHT.search(said)
    if tall:
        feet, inches = tall.group(1), tall.group(2)
        total = int(feet) * 12 + int(inches)
        low, high = int(total * 0.42), int(total * 0.50)
        return ("At %s foot %s, look for a coat about %d to %d inches from the shoulder - mid-thigh "
                "on you - so it keeps your legs warm without swamping you. Check the sleeve ends "
                "at your wrist bone with your arms down, and try it on over the thickest jumper "
                "you own." % (feet, inches, low, high))
    for words, reply in _COAT_KINDS:
        if any(re.search(r"\b" + re.escape(word), said) for word in words):
            return reply
    generic = ("Pick the coat by the weather you are actually out in: a waterproof shell for "
               "rain, down or padded for cold and dry, wool for town. £80 to £150 buys a padded "
               "coat that lasts a decade, £150 to £250 a waterproof shell that does not leak at "
               "the shoulders.")
    if _mentions_coat_check(said):
        return _COAT_CHECK if _coat_said_already(memory) else generic + " " + _COAT_CHECK
    return generic


_COAT_CHECK_WORDS = ("look for", "look out for", "check", "what should i", "fit", "fits", "long",
                     "length", "short", "tall", "size", "sizing", "cuff", "hood", "sleeve",
                     "sleeves", "quality", "warm enough")


def _coat_said_already(memory):
    from ..memory import last_bot

    said = str(last_bot(memory) or "").lower()
    return ("buys a padded coat" in said or "pick the coat by the weather" in said
            or "waterproof shell with taped seams" in said)


_NAMED_BY_PRONOUN = {"her", "him", "them", "hers", "his", "theirs"}


def _nobody_named_by_pronoun(understood):
    if not isinstance(understood, dict):
        return True
    words = understood.get("words") or understood.get("norm") or ()
    return not _NAMED_BY_PRONOUN.intersection(str(word).lower() for word in words)


def _mentions_coat_check(said):
    return any(re.search(r"\b" + re.escape(word), said) for word in _COAT_CHECK_WORDS)

_KEEP_RECEIPT_RE = re.compile(
    r"\b(?:how long|how many|years?|months?|decades?|tax return|self assessment|expense claim|"
    r"expenses claim|employer|for work|at work|work expenses)\b")


def _not_a_length(understood):
    if not isinstance(understood, dict):
        return True
    said = ("%s %s" % (understood.get("text") or "", understood.get("clean") or "")).lower()
    return not _KEEP_RECEIPT_RE.search(said)



def _the_bag_is_not_packaging(understood):
    return not a_food_is_being_kept(understood)

def _the_place_not_the_shop(understood):
    said = " " + (understood.get("clean") or understood.get("text") or "").lower() + " "
    going = (" pack", " packing", " trip", " travel", " travelling", " traveling", " flight",
             " fly", " holiday", " holidays", " visit", " visiting", " hotel", " weather",
             " things to do", " airport", " tourist", " sightseeing", " northern lights",
             " what to wear", " what to take", " what to see", " in october", " in november",
             " in december", " in january", " in february", " in march")
    place = (" with kids", " with children", " with a family", " with the family", " with a baby",
             " how many days", " how long", " best time to", " when to go", " worth visiting",
             " things to do", " it worth going", " reykjavik", " blue lagoon", " golden circle",
             " whale watching", " northern lights", " hire car", " car hire", " road trip",
             " visa", " what to pack", " what to wear", " is it safe", " safe to")
    price = (" cheap", " cheaper", " price", " prices", " quality", " fresh", " value",
             " compare", " comparison", " expensive", " basket", " groceries", " supermarket",
             " shop")
    if any(word in said for word in place):
        return False
    if any(word in said for word in going) and not any(word in said for word in price):
        return False
    return True


ENTRIES = [
    entry("wine-pick", (("wine", "wines", "red wine", "white wine", "rose", "prosecco",
                         "supermarket wine", "red", "fizz", "champagne"),
                        ("cheap", "cheaper", "good", "nice", "decent", "best", "pick", "choose",
                         "buy", "buying", "recommend", "bargain", "tenner", "budget", "bottle",
                         "bottles", "supermarket", "worth", "shopping for"),
                        ("pick", "picking", "which", "choose", "choosing", "buying", "recommend",
                         "looking for", "under a tenner", "good value", "worth buying")),
          "Buy the shop's own-label bottle from a named region rather than a brand at the same "
          "price: a \u00a37 C\u00f4tes du Rh\u00f4ne, Rioja or Chianti from the supermarket's own range usually "
          "beats a \u00a37 brand, because you are paying for the wine and not the label. On a red, look "
          "for the words reserva, crianza or a named village; for a white, Picpoul, Muscadet and an "
          "own-label Albari\u00f1o are the safest cheap buys, and a screw cap keeps it fresher. Skip the "
          "half-price 'was \u00a312' bottles - the plain \u00a36 to \u00a39 rows are where the value is. For "
          "fizz, the word Valdobbiadene on a prosecco, or a Cr\u00e9mant instead of champagne, gets you "
          "the same evening for a third of the price.",
          ask=("wine", "wines", "red", "white", "rose", "prosecco", "fizz", "champagne",
               "bottle", "bottles", "merlot", "rioja", "shiraz", "pinot", "chardonnay"),
          avoid=("goes with", "go with", "pair", "pairing", "with lamb", "with steak", "with fish",
                 "with chicken", "sauce", "stew", "deglaze", "cook", "cooking", "recipe",
                 "open bottle", "opened", "keeps", "keep", "freeze", "leftover", "how long",
                 "gift", "present", "birthday", "christmas", "units", "calorie", "calories",
                 "pregnan", "breastfeed", "allergy", "sulphite", "stain", "carpet", "spill",
                 "hangover", "how many",
                 "cabbage", "meat", "beef", "onion", "onions", "pepper", "peppers", "lentil",
                 "lentils", "bean", "beans", "rice", "curry", "good for you", "healthy",
                 "healthier", "vitamin", "vitamins", "iron", "protein", "sugar", "salt",
                 "paint", "paintwork", "primer", "wall", "walls", "ceiling", "shirt", "shirts",
                 "dress", "dresses", "curtain", "curtains", "sofa", "sofas", "shoes", "trainers",
                 "socks", "jumper", "bedding", "sheet", "sheets", "ink", "printer")),
    entry("applecare", (("apple care", "applecare", "apple care plus", "applecare plus",
                         "protection plan"),
                        ("laptop", "macbook", "mac", "iphone", "ipad", "phone", "device", "worth",
                         "buy", "get", "cancel", "need", "should i")),
          "Worth it mainly for accidental damage on a Mac or an iPhone: a screen repair is around "
          "£100 to £300 without it, and the plan covers two incidents a year with an excess of "
          "roughly £25 to £79 depending on the device. Skip it if your home contents insurance or "
          "the card you paid with already covers the device; the free one-year warranty covers "
          "faults, never drops.",
          bias=1),
    entry("warranty-claim",
          (("warranty", "guarantee", "extended warranty", "out of warranty", "still covered"),
           ("claim", "broke", "broken", "faulty", "fix", "fixed", "repair", "replace",
            "replacement", "expired", "ran out", "run out", "cover", "covered",
            "receipt", "shop", "store", "currys", "argos", "john lewis", "back", "money")),
          "Claim from the shop you bought it from, not the warranty: in the UK the retailer owes "
          "you a repair or replacement for up to six years in England, Wales and Northern Ireland "
          "(five in Scotland), and a manufacturer's guarantee sits on top of that rather than "
          "replacing it. Put it in writing with the order number, the fault and the date, and ask "
          "for a repair, a replacement or a refund in that order. Out of warranty, ask anyway: a "
          "goodwill repair is common, and the card you paid with may carry its own cover.",
          avoid=("boiler", "washing machine", "fridge", "freezer", "oven", "dishwasher", "tumble",
                 "car", "van", "tyres", "service", "mot", "parts", "engine")),
    entry("laptop-pick", ("laptop", ("pick", "buy", "choose", "recommend", "good", "need", "new",
                                     "one", "help", "look for", "what to look for", "specs",
                                     "spec", "ram", "memory", "storage", "upgrade", "upgrading",
                                     "upgrad",
                                     "which", "what", "get")),
          _laptop_general, ask=CHOOSING,
          avoid=("battery", "cracked", "screen", "keyboard", "keys", "charger", "charging",
                 "slow", "fan", "loud", "hot", "overheat", "crash", "freeze", "virus",
                 "wont", "won't", "broken", "repair", "fix", "pdf", "form", "password",
                 "reset", "install",
                 "security", "airport", "tray",
                 "did you", "you like", "your favourite", "your favorite")),
    entry("laptop-upgrade", ("laptop", ("upgrade", "upgrading", "upgrad", "more ram",
                                        "more memory")),
          ("Yes, if you keep running out of memory: going from 8GB to 16GB is the upgrade that "
           "shows up most, and it is £30 to £60 if the laptop has a slot you can open. Check the "
           "model takes a stick first, because many thin ones are soldered, and a bigger SSD helps "
           "more than RAM if the drive is the thing that is always full."),
          ask=(("upgrade", "upgrading", "upgrad", "more ram", "more memory"),), bias=2,
          avoid=("which laptop", "buy a laptop", "new laptop", "replace my laptop",
                 "ssd", "ssds", "hard drive", "hard disk", "disk")),
    entry("laptop-creative", ("laptop", (("video editing", "video edit", "editing", "gaming",
                                          "games", "photoshop", "architecture", "cad", "design",
                                          "3d", "render", "blender"))),
          ("For video editing, gaming or CAD you do need a dedicated graphics card: look for 16GB "
           "of RAM (32GB for 4K video) and a screen that covers 100% sRGB. Expect to pay £900 to "
           "£1,300, and check the weight before you commit to carrying it."), bias=1),
    entry("laptop-student", ("laptop", ("student", "uni", "university", "school", "cheap", "budget",
                                        "essays", "coursework")),
          ("For essays, video calls and Netflix, almost anything current works: 8GB RAM, a 256GB "
           "SSD and a 14 inch screen, around £400 to £550. A Chromebook is fine if everything lives "
           "in Google Docs, but avoid it for a course that needs Windows software."), bias=1),
    entry("phone-refurbished", (("phone", "iphone", "android", "handset", "mobile"),
                                ("refurbished", "used", "second hand", "cheap", "new")),
          ("A refurbished phone is a good way to save 30 to 50%: buy from a seller who grades the "
           "condition and gives a 12-month warranty, and check the battery health figure. Avoid "
           "anything sold as \"for parts\" or with an iCloud lock."),
          ask=("buy", "buying", "bought", "worth", "cheap", "cheaper", "refurbished", "refurb",
               "used", "second hand", "secondhand", "recommend", "should i get", "pay", "price",
               "need a", "need some", "want a", "budget", "afford", "spend", "looking for"),
          avoid=("fix", "fixing", "repair", "repairing", "broken", "cracked", "wont charge",
                 "not charging", "battery drains")),

    entry("phone-pick", (("phone", "iphone", "android", "handset"),
                         ("buy", "buying", "choose", "choosing", "look for", "look out for",
                          "best", "worth", "recommend", "which", "upgrade", "buying one")),
          ("Spend on the battery and the update years, not the camera: a mid-range phone at £250 to "
           "£400 lasts as long as a flagship if the maker promises four or five years of security "
           "updates (Samsung, Google and Apple do; many cheap brands promise two). Get at least "
           "128GB, check the battery is 5,000mAh or more, and make sure it takes a physical SIM as "
           "well as an eSIM if you travel."),
          avoid=("battery", "batteries", "charge", "charging", "screen", "cracked", "crack",
                 "lost", "lost it", "water", "wet", "hot", "slow", "storage", "full",
                 "transfer", "wont turn on", "turn on", "screenshot", "print", "repair",
                 "fix", "broken", "move", "wifi", "everything")),
    entry("running-shoes", (("running shoes", "running trainers", "trainers", "shoes", "runners"),
                            ("expensive", "worth", "running", "run", "jog", "jogging", "marathon",
                             "parkrun", "5k", "10k", "pay", "price")),
          ("For running, yes: a proper pair makes a real difference to your knees, and a running "
           "shop will watch you run and fit you for £90 to £130. Replace them every 500 to 800km, "
           "or when the midsole feels flat."), bias=1,
          avoid=("personal trainer", "dog trainer", "a trainer", "gym trainer", "trainer at",
                 "school", "schools", "nursery", "uniform", "plimsolls",
                 "dry", "drying", "dried", "soaked", "soaking", "newspaper", "radiator",
                 "washing machine", "smelly", "smell", "clean them", "clean my")),
    entry("shoes-buy-cheap",
          (("school shoes", "school shoe", "school trainers", "school footwear",
            "shoes for school", "school uniform shoes", "uniform shoes", "kids shoes",
            "kids trainers", "kids school shoes", "childrens shoes", "children's shoes",
            "nursery shoes", "reception shoes", "plimsolls"),
           ("cheap", "cheapest", "afford", "where", "shop", "shops", "buy cheap", "buying",
            "buy", "price", "prices", "cost", "spend", "pairs", "pair of", "pair",
            "year old", "old", "age", "teenager", "teen", "boys", "girls", "september",
            "start school", "starting school", "back to school", "which",
            "what school", "what kind of school", "which school")),
          ("Cheap is fine if the fit and the sole are right: supermarket own-brands are £10 to "
           "£25, and an outlet or the January sales gets a good pair at £25 to £35 rather than "
           "£50. Check for a thumb's width at the toe, room across the widest part and a sole you "
           "can bend - a school-age child will need the next size in four to six months."),
          avoid=("too small", "too tight", "fit", "fits", "fitting", "size", "sizes", "measure",
                 "blister", "blisters", "rub", "rubs", "rubbing", "hurt", "hurts", "hurting",
                 "sore", "uncomfortable", "smelly", "smell", "clean", "polish", "scuff",
                 "repair", "split", "return", "refund", "lost", "wet", "muddy", "new",
                 "running", "run", "jog", "jogging", "marathon", "parkrun", "5k", "gym",
                 "wedding", "work", "safety", "steel toe", "heels",
                 "personal trainer", "personal trainers", "dog trainer", "dog trainers",
                 "gym trainer", "trainer at", "a trainer", "pt session"),
          bias=1),
    entry("shoes-standing", (("shoes", "trainers", "boots"),
                             ("standing", "walking", "comfortable", "all day", "work", "feet")),
          ("For standing all day, prioritise a cushioned sole, room at the toes and a snug heel, "
           "and buy at the end of the day when your feet are at their biggest. Two pairs worn "
           "alternately last far longer than one."),
          avoid=("squeak", "squeaks", "squeaking", "squeaky", "creak", "creaking", "noise",
                 "noisy", "mould", "moulds", "mold", "molds", "mouldy", "moldy", "mildew",
                 "mildewy", "musty", "mustiness", "smell", "smells", "smelly", "damp", "spores")),
    entry("coat-worth", (("coat", "jacket", "raincoat", "parka", "puffer", "anorak", "duffle",
                          "overcoat", "shell"),
                         ("worth", "expensive", "buy", "buying", "waterproof", "warm", "warmest",
                          "good", "look for", "look out for", "choose", "choosing",
                          "pick", "pick out", "last", "lasts", "which", "what", "best",
                          "material", "fabric", "winter", "cold", "wind", "rain", "spend",
                          "cheap", "budget", "price", "under", "quid", "recommend", "need",
                          "get")),
          _coat_to_buy,
          avoid=("zip", "zipper", "broken", "broke", "torn", "tear", "tore", "hole", "holes",
                 "ripped", "rip", "seam", "seams", "stuck", "lost", "leak", "leaks", "leaking",
                 "wet inside", "damp", "child", "children", "kid", "kids", "son", "daughter",
                 "toddler", "baby", "babies", "pram", "pushchair", "buggy", "car seat",
                 "boy", "girl", "year old",
                 "tonight", "today", "tomorrow", "right now", "this morning", "this afternoon",
                 "this evening", "weather", "forecast", "cold out", "chilly out", "warm out",
                 "raining", "rain today", "umbrella",
                 "stain", "stains", "stained", "mark", "marks", "dirty", "dirt", "mud", "grease",
                 "wash", "washing", "clean", "cleaned", "cleaner", "sponge", "brush",
                 "store", "stores", "stored", "storing", "storage", "put away", "pack away",
                 "packed away", "put it away", "away for the summer", "until next winter",
                 "till next winter", "moths", "moth", "cedar", "vacuum bag", "garment bag",
                 "dry clean", "dry-clean", "dry cleaning", "dry-cleaned")),

    entry("bike-second-hand", ("bike", ("second hand", "used", "check", "buy", "before", "worth",
                                        "choose", "choosing", "look for", "look out for")),
          ("Check the frame for cracks and dents around the welds, spin both wheels to see if they "
           "wobble, and test the brakes and gears on a ride. Ask for the frame number and check it "
           "against a stolen-bike register before you pay; a service costs £50 to £95, so leave "
           "room in the budget."),
          avoid=("gears", "gear", "slip", "slips", "slipping", "chain", "brakes", "brake",
                 "puncture", "punctures", "tyre", "tyres", "wheel", "wheels", "rusty", "rust",
                 "squeak", "squeaks", "squeaking", "click", "clicking", "noisy"),
          bias=1),
    entry("bike-kids", ("bike", ("child", "kid", "kids", "age", "size", "grow")),
          ("Go by inside leg, not age: a child should be able to put both feet flat on the ground "
           "with the saddle at its lowest. A bike one size up with the seat down is safer than an "
           "oversized one they can't control, and balance bikes beat stabilisers.")),
    entry("learn-to-ride", (("ride", "riding", "pedal", "pedalling", "cycle", "cycling"),
                            ("teach", "teaching", "learn", "learning", "child", "kid", "kids",
                             "son", "daughter", "toddler", "stabilisers", "balance bike",
                             "cant", "can't", "cannot", "never learnt", "never learned")),
          ("Take the pedals off and drop the saddle until both feet reach the ground, then let them "
           "push along and coast with their feet up - a child who can balance for five seconds can "
           "ride, and an adult learning does the same on a bike with the saddle low. Hold the back of "
           "the saddle, not the handlebars, when they first pedal, and let go without saying so. "
           "Twenty minutes at a time beats an afternoon, and a flat, empty car park beats a narrow "
           "pavement."),
          avoid=("verruca", "verrucas", "wart", "warts", "foot", "feet", "itch", "itchy",
                 "sore", "hurts", "pain", "blister", "blisters", "toe", "toes", "nail",
                 "nails", "skin", "rash")),

    entry("office-chair", (("office chair", "desk chair", "chair"),
                           ("cost", "much", "price", "spend", "decent", "budget", "pay",
                            "worth", "good", "buy", "choose", "look for", "look out for",
                            "recommend", "recommended", "recommendation", "recommendations")),
          ("About £100 to £200 buys a decent one: adjustable height and armrests, a seat you can set "
           "to the right depth, and a five-year guarantee on the gas strut. Cheaper chairs lose "
           "their height and wobble within a year; a used Steelcase or Herman Miller for the same "
           "money is the better buy if you can sit in it first."),
          avoid=("high chair", "highchair", "high chairs", "baby", "babies", "child", "children",
                 "kid", "kids", "toddler", "booster", "nursery")),
    entry("frying-pan", (("frying pan", "pan", "wok"),
                         ("buy", "cost", "much", "price", "best", "good", "decent", "non-stick",
                          "nonstick", "replace", "choose", "look for", "look out for")),
          ("£25 to £40 buys a good non-stick one: a thick base, a metal handle you can finish in "
           "the oven, and no rivets inside where food catches. Cheap non-stick dies in a year or "
           "two, so either buy mid-price and expect to replace it, or spend a bit more on carbon "
           "steel and season it."),
          avoid=("burnt", "burned", "burnt on", "burnt bits", "burned bits",
                 "clean a pan", "clean the pan", "clean my pan", "clean a frying pan",
                 "clean the frying pan", "scour", "scrub", "burnt food",
                 "stuck to the bottom", "stuck on the bottom", "bottom of the pan")),
    entry("mattress-buy", ("mattress", ("buy", "buying", "choose", "choosing", "firm", "soft",
                                        "best", "good", "replace", "cost", "much", "price",
                                        "decent", "spend", "which", "need", "look for",
                                        "look out for", "pick", "picking", "back",
                                        "get", "getting", "should",
                                        "cheap", "cheaper", "budget")),
          ("Spend your budget on support, not springs: a medium-firm pocket-sprung or foam mattress "
           "suits most people, and you should lie on it for 15 minutes in the shop. Buy somewhere "
           "with a 100-night trial, and replace it every 8 to 10 years."),
          avoid=("clean", "cleaning", "stain", "stains", "smell", "smells", "wash", "washing",
                 "vacuum", "wet", "accident", "bedbugs", "bed bugs",
                 "turn", "turning", "turned", "flip", "flipping", "flipped", "rotate",
                 "rotating", "rotation", "head to foot", "two sided", "sag", "sagging",
                 "saggy", "dip", "dips", "lumpy", "worn out",
                 "carried", "carrying", "lifted", "lifting", "hauled", "dragged", "shifted",
                 "sack truck", "up the stairs", "up two flights",
                 "topper", "toppers", "mattress topper", "mattress toppers", "protector",
                 "mattress protector"),
          bias=2),
    entry("washing-machine", ("washing machine", ("buy", "choose", "choosing", "best", "good",
                                                 "need", "size", "look for", "look out for",
                                                 "recommend", "which washing machine",
                                                 "what washing machine")),
          ("Get an 8kg drum for a family, a 1,400 spin speed and the best energy rating you can "
           "afford: the running cost over ten years beats the purchase price difference. Measure "
           "the gap and the door before you order, and check the warranty length."),
          avoid=("leak", "leaks", "leaking", "leaked", "drain", "drains", "draining", "drained",
                 "spin", "spins", "spinning", "broken", "broke", "fix", "fixed", "fixing",
                 "repair", "repairs", "not working", "stopped working", "wont start",
                 "won't start", "noise", "noisy", "banging", "stuck", "error", "smell", "smells")),
    entry("furniture-second-hand", (("sofa", "furniture", "table", "wardrobe"),
                                    ("second hand", "used", "buy", "check", "charity")),
          ("Second-hand furniture is the best value there is, and charity shops and Freecycle are "
           "the places to look. Check for woodworm holes, sagging cushions and smoke smell, and "
           "measure your door and stairs before you collect anything big."),
          avoid=("washing", "laundry", "detergent", "powder", "washing powder", "soap", "bleach",
                 "cleaner", "cleaners", "nappies", "toilet roll", "loo roll", "kitchen roll",
                 "coffee", "tea bags", "cereal", "tins", "pet food", "food", "drink", "sauce")),
    entry("is-the-deal-real", (("sale", "deal", "deals", "discount", "offer", "offers",
                               "bargain", "price drop", "price cuts", "reduced"),
                               ("real", "really", "worth", "genuine", "good", "actually",
                                "check", "too good")),
          ("Check the price history before believing a sale: CamelCamelCamel does it for Amazon and "
           "Keepa for many shops, and a \"was £200\" tag that was £200 for one week tells you "
           "nothing. Compare the unit price (per kg or per wash) rather than the pack price."),
          avoid=("house", "houses", "flat", "property", "asking price", "estate agent",
                 "below asking", "under asking", "mortgage", "seller", "landlord")),
    entry("reviews-fake", (("review", "reviews", "rating", "ratings", "stars"),
                           ("fake", "fooled", "fool", "trust", "reliable", "believe", "real",
                            "genuine", "sponsored", "paid", "honest")),
          ("Read the two- and three-star reviews first: they say what actually goes wrong, while "
           "five-star ones are often written the day the thing arrived. Then check whether the "
           "reviews are spread over months or all landed in one week (a burst is bought), look for "
           "the line that says the purchase was verified, and search the product name with "
           "\"problem\" or \"broke\" to find the complaints. A brand-new product with hundreds of "
           "glowing reviews is the one to distrust most.")),
    entry("review-leave",
          (("leave a review", "leave reviews", "leaving a review", "write a review",
            "writing a review", "post a review", "leave a rating", "leave feedback",
            "leave a bad review", "write a bad review", "leave a negative review",
            "1 star review", "one star review", "edit a review", "change a review",
            "review i left", "review a product", "review a restaurant", "review a shop",
            "review a hotel", "review a company", "where to leave a review",
            "good review", "good reviews", "helpful review", "honest review",
            "useful review", "what makes a good review"),
           ("how", "should", "where", "can", "worth", "want", "going to", "do i",
            "what makes", "what counts as",
            "google", "amazon", "tripadvisor", "trustpilot", "yelp", "product",
            "restaurant", "shop", "hotel", "star", "online", "bad")),
          ("Leave it where people look, and where the business will see it: the order page for an "
           "online shop (that is the one the seller can answer), Google Maps for a cafe, shop or "
           "restaurant, TripAdvisor for a hotel. Three or four lines beat a rant - what you bought, "
           "when, what went wrong, and what you want - and give the stars you actually mean, since "
           "a 2 with a fair paragraph is read and a 1 with none is not. Post within a week or so "
           "while the details are checkable, keep the order number and any photos, and you can edit "
           "or delete your own review later from your account."),
          avoid=("reply", "replies", "reply to", "respond", "responding", "answer a",
                 "apologise", "apologize", "removed", "remove", "taken down", "delete",
                 "my app store", "subscription", "subscriptions", "chargeback",
                 "appraisal", "performance review", "my boss", "my manager", "at work",
                 "colleague", "colleagues", "coworker", "co-worker", "teammate", "team",
                 "staff", "employee", "employees", "the team", "my team", "presentation",
                 "customer", "customers", "my business", "my shop", "my restaurant")),
    entry("review-taken-down",
          (("review removed", "review taken down", "remove a review", "delete a review",
            "get a review removed", "get a bad review removed", "bad review removed",
            "bad review taken down", "bad review of my business", "review about my business",
            "negative review", "unfair review", "can i report a review", "report a review",
            "review of my shop", "review of my business", "review of my restaurant",
            "review of my company", "review of my cafe", "review of our shop",
            "a customer left", "review on my", "review for my", "one star review",
            "1 star review"),
           ("how", "can", "someone", "business", "shop", "restaurant", "customer",
            "customers", "left", "got", "google", "tripadvisor", "amazon", "report",
            "remove", "removed", "taken", "take down", "down", "delete", "deleted",
            "untrue", "lies", "defamatory", "slander", "my shop", "my business")),
          ("Only the platform can take a review down, and only when it breaks their rules: no proof "
           "of purchase, abuse, the wrong business, or a rant about something else. Open the review, "
           "use its report button and pick the rule it breaks, and keep a screenshot. If the platform "
           "says no, ask once more with the order number as proof of what really happened, and reply "
           "once in public with the fix - readers weigh that calm reply more than the complaint. Never "
           "offer a refund or a freebie for a good review or a deletion: that breaks the rules itself "
           "and can cost the listing its stars."),
          avoid=("how do i reply", "reply to a bad review", "respond to a review",
                 "apologise to a customer", "appraisal", "performance review", "my boss",
                 "my manager")),
    entry("where-to-buy-cheapest",
          (("cheapest", "cheapest place", "cheapest shop", "where to buy", "where can i buy",
            "where should i buy", "where do i buy", "best place to buy", "best price",
            "who sells", "where sells",
            "where do i get", "where can i get", "where to get", "where should i get"),
           ("get one",) + PRICE_COMPARED),
          "Compare the exact model across two or three shops, and check its price history first: a "
          "\"was £500\" tag is often a week old. For appliances the cheapest safe route is usually "
          "refurbished or graded stock with a real warranty, or ex-display if you ask. Buy at the "
          "end of the season or when a new model lands, and pay by credit card over £100 for the "
          "extra protection.",
          guard=lambda understood: (not asks_where(understood)
                                    or asks_where_a_shop_answers(understood)),
          avoid=("groceries", "grocery", "weekly shop", "food shop", "supermarket", "milk",
                 "meat", "vegetables", "dinner", "meal", "meals", "recipe", "recipes",
                 "broken", "not working", "stopped working", "wont start", "won't start",
                 "repair", "repairs", "fix", "faulty", "leaking", "leaks", "error code",
                 "sofa", "furniture", "table", "wardrobe", "laptop", "phone", "iphone",
                 "android", "tablet", "mattress", "washing machine", "washer dryer",
                 "running shoes", "trainers", "coat", "jacket", "office chair", "frying pan",
                 "bike",
                 "used car", "secondhand car", "second hand car", "new car", "cheap car",
                 "car for sale", "printer",
                 "pram", "prams", "contact lenses", "contact lens", "glasses frames",
                 "which", "to run", "running cost", "cost to run", "per year", "a year",
                 "energy", "electricity", "water use", "uses", "efficient",
                 "descaler", "descale", "descaling", "limescale",
                 "plant", "plants", "flower", "flowers", "tree", "trees", "seed", "seeds",
                 "bulbs", "shrub", "bush", "houseplant", "hanging basket", "compost",
                 "chicken", "chickens", "fish", "eggs", "fruit", "veg", "vegetables")),
    entry("where-to-buy-everyday",
          (("where can i buy", "where do i buy", "where to buy", "where can i get",
            "where do i get", "where can i find", "where do i find", "best place to buy",
            "best place to get", "who sells", "where sells"),
           _THE_EVERYDAY_THINGS),
          _everyday_where,
          avoid=("boiler", "boilers", "consumer unit", "fuse box", "fuse board", "trip switch",
                 "rcd", "colour code", "color code", "paint code", "code for the paint")),
    entry("haggle-price",
          (("haggle", "haggling", "haggled", "bargain", "bargaining", "bargained", "negotiate",
            "negotiating", "negotiation", "talk them down", "money off", "discount", "discounts",
            "lower price", "better price", "cheaper price", "best price", "price down"),
           ("how", "is", "it", "can i", "should i", "do i", "is it", "you", "my", "what", "tips",
            "rude", "worth",
            "price", "prices", "shop", "shops", "market", "car boot", "boot sale", "sofa",
            "mattress", "builder", "builders", "plumber", "tradesman", "tradesmen", "quote",
            "quotes", "deal", "cheaper", "down", "washing machine", "fridge", "car")),
          _haggle,
          avoid=("used car", "second hand car", "dealership", "test drive", "mileage", "car dealer",
                 "real bargain", "actually a bargain", "good bargain", "is it worth", "worth it",
                 "voucher", "vouchers", "promo code", "discount code", "coupon", "coupons",
                 "student discount", "loyalty", "clubcard", "nectar", "cashback",
                 "what is a bargain", "whats a bargain", "is this a bargain", "is that a bargain",
                 "a real bargain", "such a bargain", "bargain hunter",
                 "council tax", "energy", "bill", "bills", "gas", "electric", "electricity",
                 "water bill", "train", "trains", "rail", "railcard", "bus", "buses", "flight",
                 "flights", "house", "houses", "mortgage", "offer on a house", "estate agent",
                 "sell", "sells", "selling", "sold", "ebay", "vinted", "gumtree", "insurance",
                 "salary", "salaries", "pay rise", "payrise", "raise", "wages", "wage",
                 "job offer", "new job", "promotion", "appraisal", "interview",
                 "flexible", "flexible working", "flexible hours", "hours", "boss", "manager",
                 "employer", "employers", "employee", "work from home", "wfh", "part time",
                 "full time", "shift", "shifts", "rota", "annual leave", "holiday entitlement",
                 "redundancy", "union", "colleague", "colleagues", "hr",
                 "rent", "rents", "rent increase", "rent rise", "landlord", "landlords",
                 "tenancy", "tenancies", "lease", "deposit", "section 13",
                 "mobile", "phone", "phones", "handset", "sim", "sim only", "tariff",
                 "contract", "contracts", "broadband", "tv licence", "gym", "gym membership",
                 "insurance quote",
                 "new car", "new cars", "brand new car", "buy a car", "buying a car",
                 "car finance"),
          guard=a_price_not_a_loan),
    entry("supermarket-cheapest",
          (("aldi", "lidl", "asda", "tesco", "sainsburys", "sainsbury's", "morrisons", "waitrose",
            "marks and spencer", "marks and spencers", "m and s", "m s", "ms", "marks & spencer",
            "co-op", "co op", "coop", "iceland", "farmfoods",
            "ocado",
            "supermarket", "supermarkets", "groceries", "weekly shop"),
           ("cheaper", "cheapest", "expensive", "compare", "comparison", "best value",
            "better value", "which is", "worth switching", "switch", "price", "prices",
            "value for money", "or",
            "shop at", "shopping at", "worth it", "worth shopping", "as good", "good quality",
            "quality", "which shop", "which one",
            "good", "better", "worse", "fresh", "fresher", "taste", "tasty", "nicer",
            "worth", "worth the money",
            "decide", "deciding", "choose", "choosing", "pick", "between", "should i",
            "shall i", "should we", "shop at", "shopping at")),
          _supermarket_cheapest,
          ask=("cheaper", "cheapest", "expensive", "compare", "comparison", "best value",
               "better value", "better", "worse", "as good", "fresh", "fresher", "which",
               "which is", "which shop", "which one", "worth", "worth it", "switch",
               "prices", "price", "value", "quality", "good", "shop at", "shopping at", "or",
               "vs", "versus", "instead of",
               "should i", "shall i", "should we", "should", "decide", "deciding", "choose",
               "choosing", "pick", "help me"),
          guard=_the_place_not_the_shop,
          avoid=("meal plan", "meal planning", "meal prep", "what should i cook", "recipes",
                 "food waste", "waste food", "refund", "refunds", "complaint", "complain",
                 "delivery", "deliveroo", "just eat", "substitute", "out of stock",
                 "parking", "opening hours", "open today", "nearest",
                 "clubcard", "club card", "loyalty", "loyalty card", "nectar", "reward points",
                 "petrol", "fuel", "diesel", "gluten", "free from", "free-from", "vegan",
                 "vegetarian", "coeliac", "celiac", "dairy free", "nut free", "allergy",
                 "organic", "halal", "kosher", "any good for", "good for", "fine for", "ok for",
                 "okay for", "meal deal",
                 "my weekly shop", "would a weekly shop", "is a weekly shop cheaper",
                 "cheaper to do a weekly shop", "my shopping", "i do my shopping",
                 "too expensive", "my basket",
                 "shop at the", "shopping at the", "i always shop", "i only shop")
                 + _SERVICE_WORDS),
    entry("bulk-buying", (("supermarket", "shopping", "groceries"),
                          ("cheaper", "save", "save money", "bulk", "value", "budget")),
          ("Compare the price per 100g on the shelf label, not the pack size: bigger packs are "
           "often, but not always, cheaper. Own-brand staples (rice, pasta, tinned tomatoes, oats) "
           "are usually the same product, and the savings there pay for the things you care about.")),

    entry("gift-dad-fishing", (("fishing", "fish", "tackle", "angling"),
                               ("dad", "father", "grandad", "stepdad", "gift", "present")),
          about_them("{they} {has} told you what {they} {likes}, so buy into it: a decent "
                      "tackle box, or a float and hook kit if {they} {is} starting out, fits any "
                      "budget and gets used. Add one small thing {they} wouldn't buy {self} - a "
                      "box set of the old films {they} {loves}, a decent flask - and a card that "
                      "says why. One thing {they} will actually use beats three safe ones."),
          avoid=LOSS + CRISIS, bias=2, ask=GIFT_ASK),
    entry("gift-dad", (("dad", "father", "grandad", "stepdad"),
                       ("gift", "gifts", "present", "presents", "60th", "70th",
                        "what to get", "what to buy", "what should i get", "what should i buy",
                        "what can i get", "what can i buy", "what do i get", "what do i buy",
                        "gift ideas", "present ideas", "christmas ideas", "birthday ideas",
                        "ideas for a gift", "ideas for a present",
                        "christmas present", "christmas gift", "fathers day", "father's day",
                        "get him", "get her", "buy him", "buy her",
                        "what to give", "what should i give", "what can i give")),
          _present_answer(
           "Go consumable and a notch better than he'd buy himself: good coffee, a decent bottle "
           "of what he already drinks, or a voucher for something he already does at the weekend. "
           "If he insists he wants nothing, replace one small thing he has been putting off - a "
           "wallet, a torch, a decent belt - and add a card that says why. One thoughtful thing "
           "beats three safe ones."),
          avoid=LOSS + CRISIS + ("speech", "toast", "best man", "maid of honour", "few words",
                                 "card", "cards", "message", "messages", "write", "writing",
                                 "what do i say", "what to write", "what do i write"),
          bias=1),
    entry("gift-mum-garden", (("garden", "gardening", "plants", "allotment", "garden centre"),
                              ("mum", "mother", "nan", "grandma", "gift", "present")),
          about_them("{they} {has} told you what {they} {likes}, so buy into it: good gloves "
                      "that fit properly, a decent trowel, a bag of good compost, or a voucher "
                      "for the nearest garden centre. Add one small thing {they} would not buy "
                      "{self} and a card that says why."),
          avoid=LOSS + CRISIS, bias=2, ask=GIFT_ASK),
    entry("gift-mum", (("mum", "mother", "nan", "grandma"),
                       ("gift", "gifts", "present", "presents", "mother's day", "mothers day",
                        "what to get", "what to buy", "what should i get", "what should i buy",
                        "what can i get", "what can i buy", "what do i get", "what do i buy",
                        "gift ideas", "present ideas", "christmas ideas", "birthday ideas",
                        "ideas for a gift", "ideas for a present",
                        "christmas present", "christmas gift",
                        "get her", "get him", "buy her", "buy him",
                        "what to give", "what should i give", "what can i give")),
          _present_answer(
           "Make something she uses every week a bit nicer: a proper thermos, a voucher for the "
           "place she likes, a photo book of the family, or a little of something she loves to "
           "eat. Experience gifts work well for someone who already has everything."),
          avoid=LOSS + CRISIS),
    entry("gift-someone", ("present for someone", "present for somebody", "gift for someone",
                           "gift for somebody", "presents for someone", "gifts for someone",
                           "present for anyone", "gift for anyone", "get someone something",
                           "get somebody something"),
          _gift_anyone, avoid=LOSS + CRISIS),
    entry("gift-leaving-work",
          (("retiring", "retires", "retired", "retirement", "leaving present", "leaving do",
            "leaving work", "leaves work", "last day at work"),
           ("present", "presents", "gift", "gifts", "gift ideas", "present ideas",
            "what to get", "what to give", "what to buy", "what do i get", "what do i give",
            "what do i buy", "what should i get", "what should i give", "what should i buy",
            "what can i get", "what can i give", "what can i buy", "what is a good present",
            "what is a good gift", "get them", "get her", "get him", "buy them", "give them")),
          _present_answer(
           "A leaving present is about what comes next rather than the job: something for the "
           "thing they will now have time for - a book, a course, a voucher for the garden centre "
           "or the cinema, a decent bottle for the first Friday. If the team is chipping in, "
           "\u00a310 to \u00a315 each buys one good thing, which beats five fillers, and the card "
           "everyone signs with one real memory each is the part people keep. Ask first whether "
           "they want a fuss at all: some people would rather have a pint after work."),
          avoid=LOSS + CRISIS + (
              "mum", "mother", "dad", "father", "nan", "grandma", "grandad", "granny",
              "sister", "brother", "aunt", "uncle", "wife", "husband", "partner",
              "son", "daughter", "baby", "child",
              "speech", "toast", "few words", "card", "cards", "message",
              "what do i say", "what to write", "what do i write"),
          bias=1),
    entry("gift-hospital", (("hospital", "ward", "in hospital", "hospital bed", "hospice",
                             "in a hospice", "hospice bed",
                             "having an operation", "operation", "surgery", "recovering",
                             "in recovery"),
                             ("gift", "present", "presents", "idea", "ideas",
                              "what to get", "what should i get", "what can i get",
                              "what do i get", "what to buy", "what should i buy",
                              "what can i buy", "what do i buy", "what to bring",
                              "what should i bring", "what can i bring", "what do i bring",
                              "what to take", "what should i take", "what can i take",
                              "what do i take", "what do you buy", "what would you buy",
                              "what do you get", "what would you get",
                              "what do you bring", "what would you bring",
                              "what do you take", "what would you take",
                              "what should i get them", "what can i get them",
                              "flowers", "ok to bring", "is it ok to bring",
                              "get her", "get him", "get them",
                              "get my mum", "get my dad", "get my nan",
                              "buy her", "buy him", "buy them",
                              "bring her", "bring him", "bring them",
                              "take her", "take him", "take them",
                              "visit", "visit her", "visit him",
                              "see her", "see him", "cheer", "cheer her", "cheer him")),
          ("Small things they can use lying in bed: a long phone cable and a charged power bank, "
           "earphones, a puzzle book or a magazine, a decent lip balm, a light blanket, or a "
           "printed photo of the family to put on the locker. Skip flowers on most wards and skip "
           "food unless you know the diet. Ask the ward what is allowed before you bring it in, "
           "and go when you can stay a while - the visit is the gift."),
          avoid=("visiting hours", "visiting times", "visiting time", "when can i visit",
                 "what time can i visit", "when can we visit", "when can you visit",
                 "what time can you visit", "can i visit", "can we visit", "is it ok to visit",
                 "ok to visit", "should i visit", "let visitors in", "visitors allowed",
                 "visitors in"),
          bias=2),
    entry("gift-someone-ill",
          (("ill", "sick", "poorly", "unwell", "flu", "a cold", "chest infection", "virus",
            "lurgy", "man flu", "recovering", "getting over", "in bed", "off work ill",
            "was in hospital", "out of hospital", "had an operation", "after an operation"),
           PERSON_ASK + ("cheer her up", "cheer him up", "cheer them up", "cheer up",
                         "take round", "bring round", "something to take round",
                         "what can i bring", "what to bring", "what do i bring",
                         "what can i take round", "anything i can", "anything we can")),
          ("Something that makes a day in bed easier: a flask of soup with bread, a box of their "
           "favourite tea, a magazine or puzzle book, and a link to a film you know they like. "
           "Offer one specific thing at one specific time - \"I'll leave soup on the step on "
           "Thursday\" - because \"let me know if you need anything\" is the thing a poorly "
           "person never does. Skip flowers and skip food you do not know they can face."),
          avoid=(
                 "do about", "anything i can do", "what can i do",
                 "dose", "doses", "medicine", "medication", "paracetamol", "ibuprofen", "calpol",
                 "syrup", "painkiller", "painkillers", "how much", "how many", "fever",
                 "temperature", "rash", "vomiting", "diarrhoea", "cough", "coughs", "sore throat",
                 "is it normal", "see a doctor", "how long", "hospital", "ward", "a and e",
                 "999", "111", "symptom", "symptoms",
                 "for a fever", "for a cough", "for the cough", "for a temperature",
                 "for the pain", "for a cold", "for flu", "for the flu", "for a sore throat",
                 "for a headache", "for sickness", "my son", "my daughter", "my child",
                 "my baby", "my kid", "my kids", "my toddler", "my boy", "my girl",
                 "has the flu", "had the flu", "has flu", "is in bed ill") + LOSS + CRISIS,
          bias=1),
    entry("gift-person", (("sister", "brother", "friend", "friends", "mate", "cousin", "aunt",
                           "uncle", "colleague", "coworker", "boss", "manager", "neighbour",
                           "wife", "husband", "partner",
                           "son", "daughter", "child", "children", "kid", "kids", "niece",
                           "nephew", "grandson", "granddaughter", "grandchild", "grandchildren",
                           "godson", "goddaughter", "godchild", "stepson", "stepdaughter",
                           "neighbor", "teacher", "carer", "nurse", "stepmum", "stepdad", "them"),
                          ("gift", "present", "get", "got", "buy", "birthday", "christmas",
                           "30th", "40th", "50th", "idea", "ideas")),
          _the_person_row("Pick something they would use every week and would not buy "
                          "themselves: good "
                    "coffee and a proper mug, woolly socks, a decent notebook, or a voucher for "
                    "the thing they always say they will do. If you know what they are into, buy "
                    "into it - a good knife for someone who cooks, a head torch for a runner, "
                    "secateurs for a gardener - and put a real message in the card, which does "
                    "half the work.",
                    CHILD_PRESENT),
          avoid=LOSS + CRISIS, bias=2, ask=PERSON_ASK),
    entry("gift-child-age", (("year old", "years old", "year-old", "yr old", "yrs old",
                              "month old", "months old", "aged", "toddler",
                              "preschool", "school age",
                              "teenager", "teenagers", "teen", "teens", "teenage")
                             + CHILD_PEOPLE,
                             ("gift", "present", "get", "got", "buy", "birthday", "christmas",
                              "1st", "2nd", "3rd", "4th", "5th", "6th", "7th", "8th", "9th",
                              "10th", "11th", "12th", "idea", "ideas")),
          _the_age_row,
          shape=(_names_a_childs_age,),
          avoid=LOSS + CRISIS + ("cheap", "cheaper", "cheapest", "inexpensive",
                                 "tenner", "fiver", "stocking", "small", "money", "cash",
                                 "voucher"),
          guard=_this_row_answers_the_line,
          bias=3, ask=AGE_ASK),
    entry("gift-new-baby",
          (("new baby", "newborn", "new born", "baby shower", "new arrival", "baby that has",
            "friend had a baby", "given birth", "just had a baby",
            "had a baby", "had her baby", "had the baby", "mate had a baby",
            "sister had a baby", "brother had a baby", "wife had a baby",
            "wifes had a baby", "wife has had a baby", "partner had a baby",
            "daughter had a baby", "son had a baby", "colleague had a baby",
            "coworker had a baby", "neighbour had a baby", "neighbor had a baby",
            "she had a baby", "they had a baby", "someone had a baby"),
           ("gift", "gifts", "present", "presents", "what should i get", "what do i get",
            "what can i get", "what to get", "what do you get", "take to", "take round", "bring",
            "what should i send", "what to send", "what do i send", "what do i bring",
            "what should i bring", "what to bring", "what should i take", "what to take",
            "what do i take", "what can i take", "get her something", "get him something",
            "get them something", "something for the baby", "something for her",
            "something for him",
            "idea", "ideas")),
          ("Buy the boring things that get used up: clothes in the three to six month size, a "
           "pack of muslins, a board book, or a voucher for a meal they do not have to cook. Skip "
           "newborn sizes (everyone buys them and the baby outgrows them in a fortnight), skip "
           "toys (a baby cannot hold one) and skip anything big, since they have no room. Offer "
           "to hold the baby while they sleep: that is the thing they actually want."),
          avoid=("health visitor", "fever", "temperature", "feeding", "feed", "sleep", "jaundice",
                 "rash", "crying", "will not stop", "wont stop", "weaning", "milk", "nappy",
                 "nappies", "cord", "weight", "is it normal", "how do i", "what if",
                 "shower food", "food ideas", "food for a shower", "food for the shower"),
          bias=2),
    entry("gift-for-a-pet",
          (("cat", "cats", "kitten", "kittens", "dog", "dogs", "puppy", "puppies", "pup",
            "rabbit", "rabbits", "bunny", "hamster", "gerbil", "guinea pig", "guinea pigs",
            "budgie", "parrot", "horse", "pony", "tortoise", "pet", "pets"),
           ("gift", "gifts", "present", "presents", "gift idea", "gift ideas", "present idea",
            "present ideas", "christmas present", "christmas gift", "birthday present",
            "birthday gift", "stocking", "christmas ideas", "presents for",
            "for christmas", "for his christmas", "for her christmas", "for its christmas",
            "for his birthday", "for her birthday", "for its birthday", "for their birthday",
            "what should i get my", "what can i get my", "what do i get my",
            "what should i buy my", "what can i buy my", "what do i buy my",
            "what should i get for my", "what to get my", "what to buy my")),
          ("For a pet, buy the comfort they use every day rather than another toy: a cat wants a "
           "warm bed by a radiator, a scratch post tall enough to stretch up on, or a food-puzzle "
           "ball; a dog wants a long-lasting chew it only gets on the day, a snuffle mat, or a "
           "spare lead for the car. A rabbit or a guinea pig wants a bigger hidey house and a "
           "chew stick, and a box with a blanket in it is famously the best present of all. Keep "
           "chocolate, grapes, raisins and anything with xylitol away from a dog, and skip the "
           "novelty toys they will ignore by Boxing Day."),
          avoid=LOSS + CRISIS + (
              "to eat", "eat", "eats", "eating", "feed", "feeds", "feeding", "food", "diet",
              "drink", "drinks", "water", "litter", "poo", "wees", "wee", "sick", "ill",
              "poorly", "vet", "vets", "limp", "limping", "pain", "hurt", "wont eat",
              "will not eat", "not eating", "off her food", "off his food", "diarrhoea",
              "vomiting", "scratching", "chewing", "barking", "biting", "training", "train",
              "walk", "walks", "walking", "to stop", "stop it", "behaviour", "behaving",
              "shampoo", "coat", "flea", "fleas", "worm", "worming", "neutered", "spay",
              "should i buy", "worth it", "is it worth", "need a", "harness", "lead", "collar",
              "muzzle", "crate", "carrier", "litter tray", "to sleep in", "to sleep on",
              "lover", "lovers", "someone who has", "somebody who has", "who has a", "who has an",
              "who owns", "owner", "owners", "anyone who", "person who",
              "bringing", "brings", "bring in", "brings in", "brought in", "brought me",
              "dead", "mice", "mouse", "bird", "birds", "vole", "voles", "rat", "rats",
              "hunting", "hunted", "killed", "caught", "cat flap"),
          bias=3),

    entry("gift-wedding", (("wedding", "registry", "marrying", "married"),
                           ("gift", "gifts", "present", "presents", "registry", "money", "buy",
                            "buying", "spend", "spending", "idea", "ideas", "what should i get",
                            "what do i get", "what can i get", "what to get", "what shall i get",
                            "get them", "get her", "get him", "give them", "give her", "give him",
                            "bring")),
          ("About £50 is the usual gift from a friend, £100 or more from a close friend or when "
           "the two of you go as a couple; what you can afford beats the table you are given. "
           "Check the registry next, since most couples list what they actually need, and a "
           "contribution to the honeymoon beats a guess. If there is no list, money in a card "
           "with a real note is never wrong, and one small thing for their home lands better "
           "than something big and impersonal. Say yes to the registry rather than worry about "
           "being original."),
          avoid=LOSS + CRISIS + ("getting married", "getting wed", "get married", "we are engaged",
                                 "engaged", "engagement", "planning", "venue", "guest list",
                                 "tax", "taxed", "taxable", "tax free", "declare", "hmrc",
                                 "our wedding", "my wedding", "save the date",
                                 "thank you card", "thank you letter", "thank you note",
                                 "thank you message", "thank you wording",
                                 "music", "song", "songs", "playlist", "band", "dj",
                                 "first dance", "aisle",
                                 "food", "menu", "menus", "catering", "caterer", "buffet",
                                 "meal", "eat", "feed", "canapes", "hog roast", "supper",
                                 "drinks", "food ideas", "flowers", "florist", "bouquet",
                                 "buttonhole", "photographer", "photographs", "photos",
                                 "readings", "vows", "order of the day", "what time"),
          bias=3, ask=GIFT_ASK),
    entry("gift-anniversary", ("anniversary", ("gift", "present", "ideas", "idea", "what to get",
                                               "what should i get", "what should we do")),
          ("Go for something shared rather than an object: dinner somewhere she has mentioned, a "
           "night away, or a small thing tied to a memory you both have. Write a card that says why, "
           "and it will beat anything expensive and impersonal.")),
    entry("gift-her", (("her", "him", "his", "their", "them", "they"),
                       ("get", "got", "buy", "bought", "give", "gives", "giving", "gave",
                        "present for", "presents for", "gift for", "gifts for")),
          _gift_anyone,
          avoid=LOSS + CRISIS + ("bought him", "bought her", "bought them", "gave him",
                                 "gave her", "gave them", "i bought", "i gave",
                                 "already bought", "already got", "have bought"),
          ask=("what", "which", "should", "could", "would", "any", "idea", "ideas", "suggest",
               "recommend", "stuck", "christmas", "birthday", "anniversary", "present",
               "gift", "still", "yet", "havent", "anything", "nothing")),
    entry("gift-generic", (("present", "gift"),
                           ("idea", "ideas", "stuck", "no idea", "what should", "suggest",
                            "for my", "for a", "for his", "for her", "christmas",
                            "good", "best", "nice", "any", "decent")),
          _gift_row("Pick something they'd use every week and wouldn't buy themselves: good "
                    "coffee and a proper mug, woolly socks, nice soap, a book about something "
                    "they care about. If you know what they do at the weekend, buy into that "
                    "instead - a voucher for the pool, the cinema or a class. Something "
                    "consumable and slightly better than usual is the safest bet for someone you "
                    "don't know well."),
          avoid=("say thank", "say thanks", "what do i say", "what should i say", "what to say",
                 "thank you for", "thank them", "thanks for the", "giving me", "gave me",
                 "got me", "i dont like", "i don't like", "dont like it", "don't like it",
                 "hate it", "returns", "return it", "regift"),
          guard=_nobody_named_by_pronoun),

    entry("gift-money", (("voucher", "vouchers", "gift card", "gift cards", "gift voucher",
                           "gift vouchers", "cash", "money", "banknote", "banknotes",
                           "tenner in a card", "a tenner in a"),
                          ("cop out", "lazy", "rude", "cheeky", "impersonal", "tacky",
                           "boring", "unoriginal", "lame", "bad present", "bad gift",
                           "good present", "good gift", "nice present", "acceptable present",
                           "ok present", "okay present", "ok gift", "okay gift", "fine present",
                           "instead of a gift", "instead of a present", "give money",
                           "giving money", "give cash", "giving cash", "give a voucher",
                           "give a gift card", "gift", "present", "presents", "sensible",
                           "safe bet")),
          "A voucher is not a cop out - a vague one is. Make it specific: a card for somewhere "
          "they already go (the cinema, a bookshop, the garden centre, their favourite cafe), or "
          "for a thing rather than a shop, and write on the card what you would do with it. Cash "
          "is fine too, and nobody is insulted by it: 'I did not know which one you wanted, so put "
          "it towards it' is the whole note. What reads as lazy is the generic card for a shop they "
          "never go in, handed over with nothing written on it - and a small thing plus a voucher "
          "beats both.",
          avoid=("expired", "expire", "expires", "expiry", "run out", "ran out", "refund",
                 "refunded", "went bust", "has closed", "closed down", "cashback", "atm",
                 "withdraw", "withdrawal", "borrow", "borrowed", "lend", "lending",
                 "loan", "pay rise", "salary", "wage", "bank transfer", "wedding",
                 "christening", "how much money should i give", "how much should i spend",
                 "how much is usual", "tax", "voucher code", "discount code", "coupon",
                 "balance", "left on", "how much is left", "how much left", "how much is on",
                 "how much is there", "how much have i got",
                 "top up", "top it up", "load it", "reload", "remaining", "still valid")),

    entry("gift-cheap", (("secret santa", "santa", "stocking filler", "stocking fillers",
                          "tenner", "under a tenner", "under 10", "under ten pounds",
                          "under a fiver", "cheap present", "cheap gift", "small gift",
                          "little gift", "cheap ideas",
                          "stocking filler for kids", "gifts for kids", "gift for kids",
                          "gifts for children", "gift for children", "presents for kids",
                          "presents for children", "kids presents", "childrens presents",
                          "little gift for a child"),
                         ("idea", "ideas", "gift", "gifts", "present", "presents", "get",
                          "got", "buy", "bought", "under", "cheap", "what", "suggest",
                          "suggestion", "suggestions", "christmas",
                          "limit", "limits", "spend", "spending",
                          "child", "children", "kid", "kids", "toddler", "toddlers", "boy",
                          "girl", "son", "daughter", "niece", "nephew", "grandchildren",
                          "grandchild", "teenager")),
          _gift_cheap,
          bias=1,
          avoid=("how much", "budget", "day out", "days out", "meal", "meals", "dinner",
                 "food", "eat", "cook", "cooking", "recipe", "recipes", "holiday",
                 "days out with the kids", "something to do", "things to do", "cinema tickets",
                 "friend", "friends", "mate", "mates", "colleague", "colleagues", "workmate",
                 "mum", "mother", "nan", "grandma", "dad", "father", "grandad", "sister",
                 "brother", "husband", "wife", "partner", "boyfriend", "girlfriend",
                 "teacher", "neighbour", "neighbor", "cousin", "auntie", "uncle")),

    entry("gift-has-everything", (("has everything", "who has everything", "wants nothing",
                                   "needs nothing", "hard to buy for", "impossible to buy for",
                                   "doesnt want anything", "does not want anything",
                                   "says they want nothing", "want for nothing"),
                                  ("gift", "gifts", "present", "presents", "get", "got",
                                   "buy", "bought", "idea", "ideas", "what", "christmas",
                                   "birthday", "suggest", "suggestions",
                                   "already")),
          ("Go for time and something used up rather than another object: a meal or a night away "
           "somewhere they have mentioned, tickets to something on their list, a lesson in a thing "
           "they keep talking about, or a very good version of a daily thing - coffee, olive oil, "
           "socks - with a note saying why you picked it. Someone who wants for nothing is short "
           "of time and good consumables, not of things."),
          bias=1,
          avoid=("nothing to eat", "no money", "cant afford", "food bank", "hospital", "ward",
                 "dying", "died", "funeral", "grief", "grieving", "cancer", "care home",
                 "job", "rent", "benefits",
                 "mum", "mother", "nan", "grandma", "granny", "dad", "father", "grandad",
                 "stepdad", "sister", "brother", "husband", "wife", "partner", "boyfriend",
                 "girlfriend", "colleague", "workmate", "teacher", "neighbour", "neighbor",
                 "write", "writing", "written", "card message", "card say", "card says",
                 "what to say", "the message", "message in", "words")),

    entry("used-car", (("used car", "second-hand car", "second hand car", "buying a car",
                        "car for sale"),
                       ("used", "second hand", "buy", "buying", "check", "seller", "inspector",
                        "deposit", "mot", "mileage", "history")),
          ("Ask how long they've owned it and why they're selling, then check the MOT history "
           "online for gaps and advisories before you look at the paint. On the drive, listen for "
           "knocks over bumps and make sure every gear and switch works; pay for an inspection on "
           "anything over a couple of thousand, and never send a deposit before you've seen the car "
           "and the V5 in their name."),
          avoid=("lease", "leasing", "leased", "pcp", "contract hire", "hire purchase",
                 "finance", "on finance", "car finance", "car loan", "loan for a car",
                 "monthly payment", "monthly payments", "per month", "rent or buy")),

    entry("car-history-check",
          (("car", "cars", "vehicle", "van", "motor", "hpi", "motorbike", "v5c", "v5",
            "log book", "history check", "vehicle check", "hpi check"),
           ("car history", "vehicle history", "history check", "history on", "hpi",
            "hpi check", "been in an accident", "in an accident", "any accidents",
            "written off", "write off", "write-off",
            "clocked", "mileage on", "the mileage", "outstanding finance", "finance on it",
            "finance outstanding", "not stolen", "is stolen", "been stolen", "stolen",
            "v5", "v5c", "log book", "vin", "previous owner", "previous keepers",
            "before buying", "genuine", "real", "fake", "forged", "verify", "legit",
            "history")),
          ("Yes, two checks cover it, one free and one about fifteen pounds. Put the number plate into "
           "gov.uk's MOT history page first: every test since 2005, the mileage at each one, and "
           "the gaps and repeated advisories that a tidy advert hides. Then buy a full history "
           "check - HPI, the AA or Total Car Check - which tells you about outstanding finance, a "
           "stolen record, an insurance write-off and a mileage discrepancy. Before you pay, match "
           "the VIN on the windscreen to the V5C, check the V5C is in the seller's name at the "
           "address you are standing at, and walk away from anything that does not line up."),
          bias=2,
          ask=("check", "checks", "checking", "checked", "history", "safe", "genuine", "real",
               "trust", "verify", "make sure", "before", "buy", "buying", "worth", "how do i",
               "is there", "does it", "has it", "can i", "should i"),
          avoid=("insurance", "claim", "claims", "payout", "write it off", "my car", "our car",
                 "i crashed", "crashed", "i hit", "scratch", "scratched", "dented", "repair",
                 "repairs", "garage", "bodywork", "injury", "injured", "hurt", "police",
                 "crash", "bump", "no claims", "excess", "premium", "quote", "renewal",
                 "sell my", "selling my", "part exchange", "trade in", "trade-in",
                 "family", "medical", "health", "symptoms", "heart", "cancer", "mental",
                 "doctor", "gp", "hospital",
                 "history of", "long history", "history month", "the history")),

    entry("write-off-category",
          (("cat s", "cat n", "cat c", "cat d", "cat a", "cat b", "category s", "category n",
            "category c", "category d", "write off", "write-off", "written off",
            "insurance write off", "write off category", "kill the car"),
           ("car", "van", "vehicle", "buy", "buying", "bought", "safe", "worth", "should i",
            "what", "mean", "means", "difference", "between", "explain", "any good", "avoid",
            "insure", "insurance", "cheaper", "value", "sell")),
          ("Both mean an insurer wrote the car off instead of repairing it, and both are legal to "
           "buy and drive once the repair has been signed off. Cat N is non-structural damage - "
           "usually a stolen-and-recovered car, a bump or flood - and cat S is structural damage "
           "that was pulled straight again. (Cat A and B are breaker-only and must never go back on "
           "the road.) An S car is worth less than an N, both are worth noticeably less than a "
           "clean one, and both are harder to insure and to sell on: ask for the damage photos and "
           "the repair invoice, have an inspection done, and get an insurance quote on the "
           "registration before you commit."),
          bias=2,
          avoid=("crashed", "crash", "i hit", "accident", "claim", "claims", "payout",
                 "my insurance", "the insurance", "other driver", "police", "repair it",
                 "repairs", "garage", "injury", "injured", "hurt")),
    entry("used-car-seller", (("seller",),
                              ("ask", "question", "questions", "happy", "know", "check", "car",
                               "hpi", "history")),
          ("Ask how long they've owned it and why they're selling, whether it's ever been in an "
           "accident, what the mileage is, when the cambelt or chain was last done, and whether "
           "the service history and V5 are both in their name. Ask to see it at their home rather "
           "than a car park: it tells you how the car has been kept, and it's where a private "
           "seller's story tends to come apart.")),

    entry("first-car",
          (("first car", "new driver", "learner driver", "car for a new driver",
            "car for a learner", "learner car", "car for a learner driver"),
           ("good", "best", "buy", "buying", "recommend", "cheap", "what", "which", "how do i",
            "should i", "advice", "get", "start")),
          "Small, petrol, and as dull as you can bear: a hatchback like a Corsa, Fiesta, Polo or "
          "Yaris with a small engine. Check two things before the car itself - the insurance "
          "group, because a 1.0-litre in a low group can cost half what a bigger car costs to "
          "insure, and the MOT history on gov.uk for gaps and advisories. Spend under half your "
          "budget on the car and keep the rest for insurance, tax and the first repair, and avoid "
          "anything modified, since insurers charge more for it.",
          bias=2,
          avoid=("i passed my test", "passed my driving test", "taxi", "van", "motorbike",
                 "insurance quote", "how much is insurance", "tyre", "tyres", "battery", "oil")),

    entry("used-car-inspection",
          (("inspection", "inspections", "inspecting", "checked over", "pre purchase",
            "pre-purchase", "aa check", "rac check", "vehicle check", "vehicle inspection",
            "history check", "hpi", "hpi check", "buyers report", "buyer's report"),
           ("worth", "pay", "paying", "car", "cars", "need", "should", "cost", "costs",
            "how much", "money", "expensive", "bother", "any point", "get one",
            "get it checked", "get checked")),
          ("Yes, and about a hundred to two hundred pounds: a pre-purchase inspection from the AA, "
           "RAC or a good local garage costs that on anything over about two thousand pounds, and "
           "it catches the hidden faults a test drive can't. Book it after you've seen the car and "
           "agreed a price in principle, and walk away if the seller won't allow one."),
          bias=1),

    entry("used-car-price", (("used car", "second-hand car", "second hand car", "secondhand car"),
                            ("how much", "cost", "costs", "price", "prices", "spend", "pay",
                             "budget", "afford", "expensive", "cheap", "too much")),
          "A used car is about £2,000 to £4,000 for 10 to 15 years old and 80,000 miles or more, "
          "£5,000 to £8,000 for 5 to 8 years old, and £9,000 to £14,000 for 3 to 5. Whatever the "
          "price, check the MOT history free on gov.uk and keep £500 back for the first repair.",
          ask=("how much", "cost", "price", "spend", "pay", "budget", "expensive", "much"),
          bias=2,
          avoid=("insurance", "insure", "tax", "fuel", "petrol", "diesel", "running",
                 "service", "servicing", "repair", "repairs", "fix", "mot", "tyre",
                 "tyres", "lease", "leasing", "finance", "rent", "rental", "hire",
                 "sell", "selling", "worth", "trade in", "part exchange", "haggle",
                 "bike", "bicycle", "van", "caravan", "motorbike", "scooter", "taxi",
                 "train", "parking", "clamp", "first car", "learner", "good", "best",
                 "weigh", "weight", "run", "running costs", "wash", "valet", "battery",
                 "clutch", "breakdown", "new", "brand new", "brand-new")),

    entry("new-car-price", (("new car", "brand new car", "brand-new car"),
                            ("how much", "cost", "costs", "price", "prices", "spend", "pay",
                             "budget", "afford", "expensive", "cheap", "worth")),
          "A new small car starts around £18,000 and a new family car around £28,000, and either "
          "loses a fifth to a third of that in the first year, most of it in the first hour. A "
          "two or three year old version of the same car is about half the new price, which is "
          "why that age is where most people buy.",
          ask=("how much", "cost", "price", "spend", "pay", "budget", "expensive", "worth"),
          bias=2,
          avoid=("used", "second hand", "secondhand", "insurance", "insure", "tax", "fuel",
                 "petrol", "diesel", "running", "service", "servicing", "repair", "fix",
                 "mot", "tyres", "lease", "leasing", "finance", "rent", "hire", "sell",
                 "selling", "trade in", "part exchange", "haggle", "bike", "van", "caravan",
                 "weigh", "weight", "wash", "valet", "breakdown", "first car", "good",
                 "best", "electric", "ev", "hybrid")),

    entry("flowers-or-plant", (("flowers", "flower", "bouquet", "plant", "orchid", "houseplant"),
                               ("or", "instead", "better", "gift", "present", "get", "buy",
                                "thank", "sorry")),
          ("Flowers, most of the time: go to a florist rather than a garage and ask for what is in "
           "season, and a mixed bunch is always safe. A plant lasts years and is the better present "
           "for someone who likes looking after things, but give an orchid or a houseplant only to "
           "a person who will remember to water it."),
          avoid=("garden", "gardening", "grow", "growing", "seed", "seeds", "soil",
                 "compost", "lawn", "prune", "allergic", "dying", "wilt",
                 "cheaper", "cheapest", "price", "cost", "online", "delivery", "sale",
                 "water", "watering", "stem", "stems", "roots", "root", "drink", "drinking",
                 "leaves", "leaf", "yellow", "yellowing",
                 "tree", "trees", "shrub", "shrubs", "hedge", "hedges", "bulbs", "sow", "sowing",
                 "plant out", "planting out", "when to plant",
                 "photosynthesis", "make food", "makes food", "their food", "own food", "food for",
                 "energy", "sunlight", "carbon dioxide", "chlorophyll", "feed", "feeds",
                 "feeding", "fertiliser", "fertilizer",
                 "mould", "mold", "mouldy", "moldy", "mildew", "fungus", "fuzzy", "furry",
                 "rot", "rotting", "repot", "repotting", "gnat", "gnats",
                 "sorry for itself", "look sad", "looks sad", "looking sad", "unhappy",
                 "miserable", "sulking", "drooping", "droopy", "limp", "floppy",
                 "cactus", "cacti", "cactuses", "succulent", "succulents",
                 "to flower", "flower again", "flowers again", "in flower", "bloom", "blooms",
                 "blooming", "blossom", "buds", "no flowers", "not flowering", "won't flower",
                 "wont flower", "died", "dies", "repot", "repotting")),
    entry("appliance-worth",
          (("air fryer", "air fryers", "airfryer", "slow cooker", "slow cookers", "pressure cooker",
            "instant pot", "bread maker", "bread machine", "dishwasher", "dishwashers",
            "tumble dryer", "tumble dryers", "robot vacuum", "robot hoover", "dehumidifier",
            "heat pump dryer", "heat pump dryers", "heat pump drier", "heat pump tumble dryer",
            "heat pump tumble drier", "heat pump condensing dryer", "vented dryer",
            "vented tumble dryer", "condenser dryer", "condenser tumble dryer",
            "coffee machine", "bean to cup", "stand mixer", "microwave", "microwaves",
            "food processor", "kitchen machine", "air purifier", "heated airer",
            "meal kit", "meal kits", "recipe box", "hello fresh", "gousto", "kindle", "e reader",
            "ereader", "noise cancelling headphones", "noise cancelling",
            "fitness tracker", "fitness trackers", "fitbit", "smart watch", "smart watches",
            "apple watch", "standing desk", "standing desks", "sit stand desk",
            "weighted blanket", "weighted blankets", "steam cleaner", "steam cleaners",
            "steam mop", "cleaner", "cleaners", "cleaning service",
            "housekeeper",
            "heated clothes airer", "heated drying rack", "electric blanket",
            "heated blanket",
            "smart thermostat", "thermostat", "water filter jug", "water filter", "filter jug",
            "humidifier",
            "mattress topper", "bed topper", "water softener", "robot mower", "robot lawn mower",
            "video doorbell", "ring doorbell", "fan", "fans", "tower fan", "pedestal fan",
            "fan heater", "electric heater", "oil filled radiator", "space heater"),
           ("worth", "worth it", "worth the money", "should i", "do i need", "need", "buy",
            "buying", "get", "getting", "good", "any good", "value", "money",
            "recommend", "recommended", "recommendation", "recommendations",
            "any point in", "any point to", "point in", "point to", "point of",
            "waste of money", "wasting money", "money well spent", "bother with", "bother",
            "help", "help with", "helped")),
          _appliance_value,
          ask=APPLIANCE_ASK,
          avoid=("battery life", "battery", "charge", "charging", "pair", "pairing",
                 "pairs with", "sync", "syncs", "syncing", "steps", "step count",
                 "heart rate", "companion app", "notifications", "fitness tracker",
                 "fitness watch",
                 "my ", "our ", "broken", "broke", "repair", "repairing", "fix", "fixing",
                 "leaking", "noisy", "not heating", "wont", "won't", "error", "fault",
                 "warranty", "guarantee", "manual", "clean", "cleaning", "descale",
                 "how do i", "how to",
                 "recipes for", "recipe for", "recipes with", "recipe with", "recipe ideas",
                 "recipe idea", "cooker recipe", "cooker recipes", "fryer recipe",
                 "fryer recipes", "maker recipe", "maker recipes", "cook recipe",
                 "cook recipes", "what to cook", "what can i cook", "meal ideas",
                 "dinner ideas", "to cook in", "cook in a", "cook in an", "cook in it",
                 "cook with it", "something to cook"),
          guard=lambda understood: not asks_where_a_shop_answers(understood),
          bias=1),
    entry("choice-worth",
          (("gym membership", "gym memberships", "join a gym", "joining a gym",
            "go to the gym", "go the gym", "going to the gym", "back to the gym",
            "bother going to the gym", "bother with the gym", "bother with a gym",
            "start going to the gym", "start at the gym",
            "heat pump",
            "heat pumps", "electric car", "electric cars", "season ticket", "season tickets",
            "smart meter", "smart meters", "water meter", "water meters"),
           ("worth", "worth it", "worth the money", "should i", "shall i", "shall we",
            "should we", "do i need", "buy", "buying",
            "get", "join", "joining", "pay", "paying", "better", "off",
            "recommend", "recommended", "recommendation", "recommendations",
            "any point in", "point in", "point to", "waste of money", "money well spent")),
          _choice_value,
          ask=APPLIANCE_ASK,
          avoid=("insurance", "warranty", "uni", "university", "degree", "mattress", "inspection",
                 "how often", "how many times a week", "how many times a month", "how regular",
                 "how busy", "what time", "what should i do", "what to do at",
                 "how do i", "how to", "tax", "lease", "hire purchase", "prices", "price",
                 "cost per", "how much",
                 "read", "reading", "blank", "display", "sending", "signal", "stopped", "faulty",
                 "not working",
                 "meter fitted", "meter fitting",
                 "fit the meter", "fit a meter", "fitting the meter", "fitting a meter",
                 "install the meter", "install a meter", "installing the meter",
                 "installing a meter", "installation of the meter", "installation of a meter"),
          bias=1),
    entry("smart-meter-what",
          (("smart meter", "smart meters", "in home display", "in-home display"),
           ("what is", "whats", "what are", "what does", "what do", "explain", "definition",
            "mean", "means", "work out")),
          "A smart meter is the gas and electricity meter that sends your readings to your supplier "
          "itself, so nobody has to read it and the bill is based on what you used rather than an "
          "estimate. It comes with a small display for the kitchen that shows what you are spending "
          "as you use it. It is free from your supplier and it does not change your tariff.",
          avoid=("worth", "worth it", "should i", "any good", "good buy", "read", "reading",
                 "blank", "stopped", "faulty", "broken", "not working", "display is",
                 "fitted", "fitting", "install", "installed", "installation", "appointment"),
          bias=1),
    entry("smart-meter-fitting",
          (("smart meter", "smart meters", "meter", "meters"),
           ("fitting", "fit one", "fit mine", "fit my", "fit a", "fit the", "fitted", "install",
            "installed", "installation", "appointment", "coming round", "coming to", "engineer",
            "next week", "next month", "on the day", "switch over", "swapping", "change my meter",
            "upgrade")),
          "Clear the cupboard the meters are in and take a photo of the readings first, because "
          "the old ones go with the fitter. Someone over 18 has to be in, and it takes about an "
          "hour per fuel; the gas and electricity go off for a few minutes each. The fitter should "
          "leave the in-home display set up and working, and the old meters away - if a display "
          "is not showing, ring the supplier rather than living with it.",
          ask=("smart meter", "smart meters", "meter", "meters"),
          avoid=("worth", "worth it", "should i", "broken", "faulty", "not working", "blank",
                 "leaking", "water meter", "parking", "electricity bill", "read my"),
          bias=1),
    entry("smart-meter-how",
          (("smart meter", "smart meters", "in home display", "in-home display"),
           ("read", "reading", "readings", "button", "blank", "stopped", "faulty", "broken",
            "working", "display", "sending", "signal", "connect", "wrong", "show", "shows",
            "mean", "means", "numbers")),
          _smart_meter_how,
          avoid=("worth", "worth it", "should i", "good buy", "any good"),
          bias=1),
    entry("watch-buy", (("watch", "watches", "wristwatch", "wrist watch", "smartwatch",
                         "smart watch", "apple watch", "garmin", "fitbit", "casio", "timex",
                         "seiko", "normal watch", "ordinary watch", "mechanical watch",
                         "analogue watch", "analog watch"),
                        ("buy", "buying", "get", "getting", "new", "which", "recommend", "worth",
                         "good", "first", "choose", "choosing", "spend", "spending", "best",
                         "pick", "should", "vs", "versus", "or")),
          _watch_help,
          ask=("buy", "buying", "get", "getting", "new", "which", "recommend", "worth", "good",
               "first", "choose", "choosing", "spend", "spending", "best", "pick", "should"),
          avoid=("tonight", "film", "films", "movie", "movies", "series", "tv", "programme",
                 "program", "show", "netflix", "episode", "stream", "streaming", "cinema",
                 "box set", "match", "game", "football", "stopped", "broken", "broke", "fault",
                 "repair", "strap", "battery", "not working", "screen", "loses time", "fast",
                 "slow",
                 "to watch", "watch tonight", "watch on", "whats on", "watch it",
                 "should i watch", "should we watch", "shall i watch", "shall we watch",
                 "can i watch", "can we watch", "i watch", "we watch", "worth watching"),
          bias=2),
    entry("buy-a-vacuum", (("hoover", "hoovers", "vacuum cleaner", "vacuum cleaners", "vacuums"),
                           ("buy", "buying", "look for", "choose", "choosing", "best", "worth",
                            "which", "recommend", "new")),
          "Check the weight and the cord length before anything else, because the best vacuum is "
          "the one you will actually push round the house. A bagged machine holds its suction and "
          "suits anyone with allergies; a bagless one is cheaper to run but needs emptying over a "
          "bin. A cordless is a quick-clean tool and rarely enough on its own in a carpeted house, "
          "so try one for weight and check the filters can be washed.",
          avoid=("robot", "car", "flask", "seal", "bags for", "washing machine")),
    entry("price-match",
          (("price match", "price match it", "match the price", "match a price", "price promise",
            "price guarantee", "cheaper elsewhere", "cheaper in another shop", "cheaper online",
            "found it cheaper", "same thing cheaper", "beat the price", "beat it by"),
           ("can i", "will they", "do they", "ask", "get", "how", "shop", "store", "retailer",
            "online", "till", "checkout", "worth", "any point", "does", "you", "they", "it",
            "elsewhere", "i found")),
          "Ask at the till before you pay, because almost no retailer matches a price after the "
          "sale. Have the competitor's page open on your phone with the exact model, the price and "
          "the date, and check the small print first: most promises exclude marketplace and "
          "third-party sellers, sale and clearance prices, membership prices, vouchers and "
          "mis-priced listings. Some chains match online prices only against their own website, and "
          "a few knock off the difference rather than the whole amount. If the assistant says no, "
          "ask for the manager and ask which rule you missed - a written promise on the wall is "
          "worth quoting.",
          avoid=("flights", "hotel", "insurance", "energy", "broadband", "mobile", "mortgage",
                 "train", "supermarket", "petrol"),
          ask=("do", "does", "can", "will", "should", "how", "worth", "found", "ask", "try")),
    entry("online-or-in-store",
          (("buy online", "buying online", "buy it online", "order online", "order it online",
            "in store", "in the shop", "in a shop", "in person", "go to the shop", "collect",
            "click and collect", "online or in store", "online or in the shop",
            "online or shop", "shop or online"),
           ("cheaper", "cheap", "better", "should i", "worth", "or", "which", "safer", "returns",
            "return", "rights", "guarantee", "warranty", "problem")),
          "Buying online gives you a 14-day right to change your mind from the day it arrives, and "
          "you only pay the return postage unless the shop says otherwise; buying in a shop gives "
          "you no right to change your mind at all, only the shop's own policy. That is the real "
          "difference, not the price. So for anything you might not keep - clothes, a mattress, "
          "furniture in a colour you have not seen - order online and check the returns page before "
          "you pay. For something you need today, or want to try first, buy in the shop and ask "
          "what their returns policy is in writing.",
          avoid=("flight", "hotel", "train", "ticket", "insurance", "car insurance", "energy",
                 "broadband", "mobile phone contract", "grocery", "food shop")),
    entry("bag-charge",
          (("bag charge", "bag charges", "charge for bags", "carrier bag", "carrier bags",
            "plastic bag", "plastic bags", "5p bag", "10p bag", "bag for life", "reusable bag",
            "pay for bags", "pay for a bag", "bags cost",
            "charged for a bag", "charged for bags", "charged me for a bag",
            "charged me for bags", "a bag at the till", "charge me for a bag"),
           ("why", "how much", "have to", "must i", "do i", "charge", "cost", "free", "law",
            "shop", "supermarket", "still", "tax", "gone up",
            "till", "checkout", "charged me", "i was", "didnt ask", "didn't ask")),
          "Shops in the UK have to charge for single-use carrier bags, and the money goes to good "
          "causes rather than to the shop, which is why the charge exists at all: it is there to cut "
          "how many bags are thrown away, and it works. A bag for life is the cheap way round it - "
          "most supermarkets replace it free when it finally splits - and small paper bags for loose "
          "fruit and veg are usually free and are not the charge. If you are charged for a bag you "
          "did not ask for, say so at the till and it comes off.",
          avoid=("hand luggage", "airline", "flight", "carrier bag levy ireland", "bin bag",
                 "vacuum", "hoover", "sleeping bag", "tea bag", "bags for",
                 "didnt want", "didn't want", "did not want", "didnt need",
                 "not ordered", "didnt order", "did not order"),
          guard=_the_bag_is_not_packaging),
    entry("complain-about-a-shop",
          (("complain about a shop", "complaint about a shop", "complain about a store",
            "complain to a shop", "complain to the shop", "complain about a purchase",
            "complain about the service", "bad service", "rude staff", "complaint about",
            "complain about a company", "escalate a complaint", "ombudsman", "small claims",
            "trading standards", "resolver", "complain", "complains", "complained", "complaint",
            "complaints"),
           ("how", "how do i", "shop", "store", "retailer", "company", "where", "next",
            "still not", "nothing happened", "no reply", "ignored", "refund", "money back")),
          "Complain to the shop first, in writing, and keep it to facts: what you bought, when, what "
          "went wrong, what you want and by when. Use email or the online form rather than the phone "
          "so there is a record, and give them 14 days. If they do not fix it, escalate inside the "
          "company - ask for the complaints procedure and the name of the person dealing with it - "
          "then go outside: Citizens Advice or Trading Standards for a legal point, the relevant "
          "ombudsman for a service, and the small claims track for money you are owed. Card payment "
          "is your spare lever: a claim under section 75 over 100 pounds, or a chargeback under it.",
          avoid=("landlord", "council", "council tax", "nhs", "hospital", "dentist", "school",
                 "doctor", "doctors", "gp", "surgery", "nurse", "clinic", "consultant",
                 "midwife", "treatment", "care home", "care homes",
                 "builder", "builders", "tradesman", "tradesmen", "plumber", "plumbing",
                 "electrician", "decorator", "painter", "contractor", "rogue trader",
                 "teacher", "boss", "employer", "bank", "energy", "broadband", "mobile",
                 "manager", "managers", "management", "colleague", "colleagues", "coworker",
                 "co-worker", "hr",
                 "insurer", "insurers", "insurance", "policy", "claim", "claims",
                 "flight", "airline", "train", "hotel", "delivery", "parcel", "neighbour",
                 "neighbor", "noise", "my ex", "family", "restaurant", "takeaway", "cafe",
                 "coffee shop", "pizza", "meal", "my order", "food order",
                 "wrong order", "courier")),
    entry("return-without-receipt",
          (("receipt", "receipts", "proof of purchase", "no receipt", "without a receipt",
            "gift receipt", "lost the receipt", "lost my receipt", "bank statement",
            "card statement"),
           ("return", "returns", "returning", "refund", "refunds", "exchange", "back",
            "take it back", "take back", "without", "lost", "need", "still",
            "need to keep")),
          "You do not need the paper slip. Proof of purchase can be a bank or card statement showing "
          "the payment, an order confirmation email, a photo of the receipt or a gift receipt, and a "
          "shop that can see the purchase on its own system cannot insist on the paper. For anything "
          "faulty your claim is against the shop, not the maker: a full refund within 30 days, then "
          "repair or replacement, and in England, Wales and Northern Ireland up to six years to "
          "claim (five in Scotland) - a statement from your bank proves it just as well. If you are "
          "returning something because you changed your mind, there is no such right in a shop at "
          "all, so you are on their returns policy; ask the manager politely what proof they will "
          "accept, and if the goods were faulty and they still refuse, say you are going to Citizens "
          "Advice and put the claim in writing.",
          avoid=("read receipt", "read receipts", "blue tick", "blue ticks", "delivery",
                 "parcel", "courier", "wan", "rent", "landlord", "tenant", "tenancy"),
          guard=_not_a_length,
          bias=1),
    entry("a-copy-of-the-receipt",
          (("receipt", "receipts", "till receipt", "proof of purchase", "vat receipt",
            "bank statement", "card statement"),
           ("copy", "duplicate", "replacement", "another", "reprint", "print", "printed",
            "emailed", "email", "didnt give", "didn't give", "never gave", "not given",
            "no receipt", "ask for", "asked for", "can i get", "how do i get", "cash")),
          "Any shop can print or email another copy, because it can find the sale from the date, "
          "the time on the till roll and the last four digits of your card, so ask at the till "
          "and say roughly when you paid. If it cannot, a card or bank statement showing the "
          "payment is proof of purchase for a return, and a photo of the paper slip in your phone "
          "covers most warranties and expenses. Ask for a VAT receipt when you pay if you need to "
          "reclaim the VAT, since an ordinary till receipt often has no VAT number on it.",
          avoid=("tax return", "self assessment", "hmrc", "expenses", "expense", "employer",
                 "keep", "keeping", "how long", "read receipt", "delivery", "parcel", "courier",
                 "donation", "donations", "charity", "gift aid",
                 "rent", "landlord", "tenant", "tenancy"),
          bias=1),
    entry("refund-how-long",
          (("refund", "refunds", "refunded", "money back", "returns money"),
           ("how long", "long", "when", "how many days", "days", "waiting", "take", "takes",
            "not had", "still", "not received", "chase", "chasing")),
          "Usually three to five working days on a card, and up to 14 days is still normal for "
          "online returns once the shop has the item back. Cash comes back at the till straight "
          "away, PayPal is often a day or two, and a card refund can take a full statement period to "
          "show because the bank holds it after the shop has paid it. If nothing has appeared after "
          "14 days, send the shop a short written request with your order number and the date you "
          "returned it, then take it to your card provider, who can raise a chargeback.",
          avoid=("faulty", "broken", "sale", "flight", "airline", "train", "hotel", "holiday",
                 "deposit", "rent", "landlord", "council", "tax", "ticket", "concert", "course",
                 "how do i get", "entitled", "can i get"),
          bias=1),
]

ENTRIES.append(entry(
    "olive-oil-pick",
    (("olive oil", "olive oils", "extra virgin", "extra virgin olive oil", "evoo"),
     ("pick", "choose", "choosing", "buy", "buying", "best", "good", "which", "worth",
      "supermarket", "brand", "bottle", "tin", "cheap", "expensive", "difference", "use",
      "cooking", "kitchen")),
    "Look for \"extra virgin\" and a harvest date, not a best-before: oil is a fruit juice and it "
    "fades, so the newest pressing tastes best. A dark glass bottle or a tin keeps it that way, "
    "and a peppery catch at the back of your throat means the good bitter polyphenols are still "
    "there. Spend on the bottle you use raw - dressing, bread, a finished dish - and use a cheaper "
    "olive oil or a plain oil for roasting and frying. \"Light\" on the label means light in taste, "
    "not in calories.",
    avoid=("car", "cars", "engine", "motorbike", "bike", "hair", "skin", "essential oil",
           "olive tree", "grow", "fryer", "deep fat", "chip pan", "paint", "lamp",
           "cake", "cakes", "sponge", "muffin", "muffins", "loaf", "loaves", "brownies",
           "brownie", "traybake", "tray bake", "carrot cake", "chocolate cake", "banana bread",
           "pastry", "shortbread", "biscuits", "cookies",
           "good for you", "good for me", "good for us", "bad for you", "bad for me", "healthy",
           "unhealthy", "fattening", "calorie", "calories", "cholesterol", "heart",
           "fry", "fries", "frying", "deep fry", "roasting", "roast potatoes"),
    ask=("pick", "choose", "choosing", "buy", "buying", "best", "good", "which", "worth",
         "supermarket", "brand", "difference", "use", "cooking")))

ENTRIES.append(entry(
    "gift-house-move",
    (("gift", "gifts", "present", "presents", "what should i get", "what can i get",
      "what do i get", "what to get", "what should i buy", "what can i buy", "what to buy",
      "what can i give", "what should i give", "what to give", "what do i give",
      "what should i bring", "what to bring", "what can i bring", "what do you get",
      "what do you buy", "what do you give", "housewarming present", "housewarming gift",
      "ideas", "idea"),
     ("moving house", "moving home", "moving in", "moving into", "just moved", "moved house",
      "moved in", "new house", "new flat", "new home", "first home", "first flat",
      "housewarming", "house warming", "moving away", "bought a house", "got the keys",
      "new place", "new apartment")),
    ("Buy for the first night, not for the shelves: a takeaway voucher for the evening the boxes "
     "are still out, a box with loo roll, tea, milk, mugs, bin bags, a corkscrew and a phone "
     "charger, or a hot meal you turn up with. A plant, a good bottle or a decent set of tea "
     "towels all last longer than another candle, and a voucher for a hardware shop is the "
     "unromantic one people are pleased about. Ask first whether they want things or help: an "
     "afternoon of unpacking and a trip to the tip is often the present."),
    ask=("gift", "gifts", "present", "presents", "get", "buy", "give", "bring", "take round",
         "ideas", "idea"),
    avoid=LOSS + CRISIS + ("where to start", "where do i start", "where do we start",
                           "where should i start", "where to begin", "where do i begin",
                           "no idea where to start", "dont know where to start",
                           "don't know where to start", "not sure where to start",
                           "my new flat", "my new house", "my new place", "our new house",
                           "our new flat", "my first flat", "my first house", "im moving",
                           "i am moving", "were moving", "we are moving", "i move", "we move",
                           "removals", "van hire", "packing", "council tax", "utilities",
                           "school", "doctor", "deposit", "landlord", "mortgage",
                           "hire a van", "man and van"),
    bias=2))

_CHOOSE_ASK = ("pick", "picking", "choose", "choosing", "choice", "buy", "buying", "bought",
               "best", "good", "decent", "which", "what should i look for", "look for",
               "look out for", "worth", "spend", "budget", "recommend", "recommendation",
               "what to get", "which to get", "what should i get", "need a", "need some",
               "want a", "size", "much", "price", "cost", "cheap", "expensive", "difference",
               "better", "worse", "bigger", "smaller", "cheaper", "dearer")

ENTRIES.append(entry(
    "duvet-choose",
    (("duvet", "duvets", "quilt", "quilts", "continental quilt", "tog"),
     _CHOOSE_ASK),
    "Go by tog: 4.5 for summer, 9 to 10.5 for spring and autumn, 13.5 for winter, or one 10.5 "
    "all year with a 4.5 on top in January. Match the size to the bed - single 135x200cm, double "
    "200x200, king 225x220, super king 260x220 - because a duvet smaller than the bed leaves a "
    "cold edge. Down and feather are warmest for the weight, wool breathes and handles damp best, "
    "and hollowfibre is the cheap washable one; a synthetic duvet goes in a 9kg drum at home, while "
    "down wants a launderette and a tumble dryer with dryer balls to bring the loft back.",
    avoid=("wash", "washing", "washed", "clean", "cleaning", "dry clean", "dry clean only",
           "dryer", "tumble", "machine", "stain", "stains", "smell", "smells", "smelly",
           "store", "storing", "storage", "put away", "pack away", "summer storage",
           "cover", "covers", "coverless", "sheet", "sheets", "bedding set", "mend", "repair",
           "torn", "rip", "hole", "allergy", "allergies", "asthma", "eczema", "dust mite"),
    bias=2))

ENTRIES.append(entry(
    "pillow-choose",
    (("pillow", "pillows", "pillowcase"),
     _CHOOSE_ASK),
    "Match the pillow to how you sleep: on your side you want a firm, high one that fills the gap "
    "between shoulder and ear, on your back a medium one, and on your front a soft, thin one so "
    "your neck is not cranked up. A pillow that folds in half and stays folded is worn out - most "
    "last two to three years, not ten. Memory foam and latex hold their shape, hollowfibre is cheap "
    "and washable at 60C, and down is soft but needs plumping; a washable protector keeps whichever "
    "you pick clean.",
    avoid=("wash", "washing", "washed", "clean", "cleaning", "dry clean", "dryer", "tumble",
           "machine", "stain", "stains", "smell", "smells", "smelly", "yellow", "mould", "mold",
           "neck", "stiff neck", "sore", "ache", "aches", "aching", "pain", "hurt", "hurts",
           "sciatica", "migraine", "headache", "sew", "sewing", "make", "making", "pattern",
           "toddler", "baby", "cot", "cushion", "cushions", "throw"),
    bias=2))

ENTRIES.append(entry(
    "kettle-choose",
    (("kettle", "kettles"),
     _CHOOSE_ASK),
    "Get a 3kW one for speed and 1.7 litres for a family, or a 1 litre one if it is mostly you - "
    "a small kettle boiled often costs less than a big one boiled for two cups. A concealed "
    "element and a wide lid make descaling easy, a water-level window on both sides saves "
    "guessing, and temperature settings are worth it only if you make green tea or filter coffee. "
    "Decide stainless steel or glass by looks, then check the minimum fill line: a kettle that "
    "needs half a litre before it will switch on wastes water and power.",
    avoid=("descale", "descaling", "limescale", "scale", "fur", "furred", "broken", "not working",
           "stopped", "faulty",
           "gone", "went", "knackered", "on the blink",
           "leak", "leaks", "leaking", "switch", "element", "noisy", "rattle",
           "boil", "boiling", "boils", "how long", "vinegar", "citric", "bicarbonate",
           "tea", "teapot", "coffee", "cup of tea", "electricity", "energy"),
    bias=2))

ENTRIES.append(entry(
    "suitcase-choose",
    (("suitcase", "suitcases", "cabin bag", "cabin case", "cabin luggage", "hand luggage",
      "carry on", "carry-on", "holdall", "luggage", "case"),
     _CHOOSE_ASK),
    "Start with the airline, because cabin sizes differ: a 55x40x20cm case fits most paid cabin "
    "allowances, while the free underseat bag is around 40x20x25cm, and a bag outside the airline's "
    "own limit is the one thing that gets charged at the gate. Four wheels and a hard "
    "polycarbonate shell survive the hold better, soft bags give and squash into a car; either way "
    "check the empty weight against a 23kg allowance and buy from a brand that covers wheels and "
    "handles for years rather than months. A TSA lock matters only for the US. For a week "
    "away, 40 to 45 litres of cabin case is enough if you pack light and wash a shirt.",
    avoid=("lost", "missing", "delayed", "damaged", "broken", "wheel broke", "zip", "zips",
           "lock stuck", "stolen", "claim", "compensation", "airline", "flight", "pack", "packing",
           "packed", "unpack", "unpacking", "what to take", "what to pack", "holiday packing",
           "storage", "store", "handbag", "handbag", "briefcase", "laptop bag",
           "phone", "iphone", "mobile", "tablet", "ipad", "laptop", "glasses", "spectacles",
           "hearing aid", "airpods", "earbuds", "camera", "console", "switch case"),
    bias=2))

ENTRIES.append(entry(
    "sofa-choose",
    (("sofa", "sofas", "settee", "couch", "three piece suite", "armchair"),
     _CHOOSE_ASK),
    "Measure the room, the door and the stairs before you fall for one, and keep 60cm of walking "
    "space past it. Then look at the build: a hardwood or beech frame screwed and glued, not "
    "stapled chipboard, and seat cushions of 30 to 35kg foam with a fibre wrap, or feather if you "
    "will plump them daily. Sit on it for ten minutes rather than three, and check the fabric's rub "
    "count - 25,000 for adults, 30,000 and up for children and pets. Made-to-order sofas take six "
    "to twelve weeks, so ask about the return policy before you pay.",
    avoid=("clean", "cleaning", "washer", "wash", "stain", "stains", "smell", "smells", "pet hair",
           "sag", "sagging", "saggy", "squeak", "squeaks", "broken", "repair", "re-upholster",
           "reupholster", "moving house", "move a sofa", "get it upstairs", "cover", "covers",
           "throw", "throws", "cushion", "cushions", "leather", "scratched"),
    bias=2))

ENTRIES.append(entry(
    "coffee-to-buy",
    (("coffee", "coffees", "coffee beans", "ground coffee", "instant coffee", "filter coffee"),
     ("pick", "picking", "choose", "choosing", "buy", "buying", "best", "good", "decent",
      "which", "what should i look for", "look for", "worth", "roast", "bean", "beans",
      "brand", "supermarket", "grind", "ground", "roasted", "fresh", "strength", "strong")),
    "Look for a roast date, not a best-before: beans are best from a few days to about six weeks "
    "after roasting, and supermarket bags with only a best-before are usually months old. Buy "
    "whole bean and grind per brew - fine for espresso, medium for a filter machine, coarse for a "
    "cafetiere - or ask the shop to grind it for the pot you use. A medium roast suits most "
    "brewing, and about 60g of coffee to a litre of water is the strength to start from. Keep the "
    "bag sealed and in a cupboard, not the fridge.",
    avoid=("make", "making", "brew", "brewing", "brewed", "cup", "cups", "mug", "machine",
           "machine descale", "descale", "caffeine", "sleep", "anxiety", "good for you",
           "bad for you", "healthy", "pregnant", "pregnancy", "withdraw", "withdrawal", "stop",
           "give up", "quit", "cafe", "cafes", "barista", "shop", "starbucks", "costa",
           "stain", "stains", "grinder", "frother",
           "milk", "milks", "dairy"),
    bias=2))

ENTRIES.append(entry(
    "rug-choose",
    (("rug", "rugs", "carpet rug", "runner", "runners"),
     _CHOOSE_ASK),
    "Go bigger than feels right: in a living room the rug should reach under the front legs of the "
    "sofa, so about 160x230cm for a small room and 200x290cm behind a three-seater, and a "
    "bedroom rug wants to run at least 60cm past each side of the bed. Wool wears and cleans "
    "better than polyester and does not flatten as fast; a thick underlay makes a cheap rug feel "
    "expensive and stops it creeping. Take the size you are considering and tape it out on the "
    "floor before you buy, and check it can be washed or spot-cleaned.",
    avoid=("clean", "cleaning", "wash", "washing", "stain", "stains", "smell", "smells", "moth",
           "moths", "slipping", "slips", "slides", "curl", "curling", "creases", "shed", "shedding",
           "hoover", "vacuum", "flat", "flattened", "repair", "fringe", "fringes", "lay", "laying"),
    bias=2))

ENTRIES.append(entry(
    "curtains-choose",
    (("curtain", "curtains", "blind", "blinds", "drapes", "curtain rail", "curtain pole"),
     _CHOOSE_ASK),
    "Buy one and a half to twice the window width in fabric, or the curtains hang flat and let "
    "light round the edges, and measure the drop from the pole or track to where you want them to "
    "end - just below the sill, or to the floor for a longer look. A lined curtain keeps heat in "
    "and light out far better than an unlined one, and a thermal lining is worth it in a bedroom. "
    "Eyelet headings slide easily on a pole, pencil pleat gives a fuller look on a track; for "
    "anything over 2m wide, two panels rather than one.",
    avoid=("hang", "hanging", "hem", "hemming", "shorten", "lengthen", "sew", "sewing", "iron",
           "ironing", "wash", "washing", "clean", "cleaning", "dry clean", "stain", "stains",
           "mould", "mold", "damp", "black mould", "repair", "broken", "cord", "track broken",
           "child safety", "blind cord"),
    bias=2))

ENTRIES.append(entry(
    "toaster-choose",
    (("toaster", "toasters"),
     _CHOOSE_ASK),
    "Two slots do for one or two people and four for a family, and the slot width matters more "
    "than the wattage: look for wide slots if you toast bagels, crumpets or thick-cut bread. "
    "Variable browning plus a cancel button is the pair that stops you scraping burnt toast, and a "
    "defrost setting is worth having if you freeze bread. A removable crumb tray and a cord that "
    "tucks away are the two things you will notice every week; anything over about 1,500W toasts "
    "no better than 900W.",
    avoid=("broken", "not working", "stopped", "faulty", "smoking", "smoke", "burnt", "burning",
           "stuck", "wont pop", "won't pop", "pop up", "clean", "cleaning", "crumbs", "crumb tray",
           "repair", "fuse", "element", "sandwich", "toastie", "air fryer", "grill"),
    bias=2))



KITCHEN_MACHINE_VALUE = (
    (("rice cooker", "rice cookers"),
     "A rice cooker is worth it if rice is a daily thing: it times it, keeps it warm for an hour and "
     "leaves the hob free, and a 40 pound one cooks as well as a 200 pound one. Skip it if you eat "
     "rice twice a month, since a pan with a lid is the same rice in 12 minutes."),
    (("soup maker", "soup makers"),
     "A soup maker is worth it if you make soup most weeks and want one jug and no pan to watch: it "
     "cooks and blends in about 20 minutes. Skip it if you like soup with chunks in it, or cook for "
     "four, because most jugs hold 1.6 litres and the blade takes everything smooth."),
    (("sous vide", "sous vide stick", "sous vide machine", "sous vide cooker"),
     "Sous vide is worth it if you cook steak, chicken breast or eggs to a temperature and do not "
     "mind waiting: a 60 pound stick in a lidded pan holds the water steady for an hour or more, and "
     "nothing overcooks. Skip it if dinner has to be on the table in 20 minutes, where a thermometer "
     "and a hot pan get most of the way."),
    (("dehydrator", "dehydrators", "food dehydrator"),
     "A dehydrator is worth it if you dry things often: herbs, apple rings, jerky or vegetables for "
     "stock, in 4 to 12 hours at 40 to 60C with no oven on. Skip it if that is a twice-a-year job, "
     "since an oven on its lowest setting with the door ajar dries a tray at a time."),
    (("juicer", "juicers"),
     "A juicer is worth it only if you drink juice most mornings: it separates the pulp in seconds, "
     "and cleaning the mesh takes five minutes every time. Skip it if you would rather eat the "
     "fruit, which keeps the fibre the juice leaves behind."),
    (("yogurt maker", "yoghurt maker", "yogurt makers"),
     "A yogurt maker is worth it if you get through a tub a week: a litre of milk makes a litre of "
     "yogurt for about 60p, and it holds the warmth steady for 8 to 12 hours. Skip it if you eat "
     "yogurt now and then, since a flask and a warm cupboard do the same job."),
    (("ice cream maker", "ice cream makers"),
     "An ice cream maker is worth it if you make it more than a few times a summer: the bowl has to "
     "be frozen overnight, so it is never a last-minute thing, and a 40 pound one with a pre-frozen "
     "bowl is fine. Skip it if you would use it twice, where a loaf tin and a fork every half hour "
     "gets close."),
    (("contact grill", "panini press", "sandwich press", "george foreman", "health grill"),
     "A contact grill is worth it if you toast sandwiches or cook chops and vegetables for one or "
     "two: it heats both sides at once and the fat runs off. Skip it if you cook for four, since the "
     "plates take two sandwiches at a time, and skip it if you have a frying pan and a lid."),
    (("electric steamer", "steam cooker", "food steamer"),
     "An electric steamer is worth it if you steam vegetables, dumplings or fish often and like "
     "setting a timer and walking away: the tiers hold a whole dinner over one ring. Skip it if a pan "
     "with a colander and a lid already does it, which for most people it does."),
    (("electric whisk", "hand whisk", "hand mixer", "electric hand whisk"),
     "An electric hand whisk is worth it for anyone who creams butter or whips cream even a few times "
     "a month: about 15 pounds, a minute instead of ten with a fork, and it lives in a drawer. Skip "
     "it only if you bake twice a year."),
    (("mandoline", "mandolines", "mandoline slicer"),
     "A mandoline is worth it if you slice a lot of vegetables thin and even - gratins, slaw, pickles "
     "- and you will use the hand guard every single time. Skip it if you cook for one: a sharp knife "
     "is safer and nearly as quick."),
    (("spiralizer", "spiralizers", "spiraliser"),
     "A spiralizer is worth it only if you really eat courgette or carrot noodles: a 10 pound "
     "hand-held one does it in a minute and the counter-top ones add nothing. Skip it if you would "
     "use it once, where a julienne peeler does the same job and fits in a drawer."),
    (("soda stream", "sodastream", "soda maker", "sparkling water maker"),
     "A soda maker is worth it if you drink sparkling water every day: a gas cylinder makes about 60 "
     "litres for 10 pounds to swap, so it pays for itself in a few months and saves carrying bottles. "
     "Skip it if you drink it now and then, or would mostly use the flavour syrups, which cost more "
     "than supermarket bottles."),
    (("vacuum sealer", "vacuum sealers", "food sealer", "food sealers"),
     "A vacuum sealer is worth it if you buy meat in bulk or freeze portions: it stops freezer burn "
     "and the bags can be boiled, so a batch of chilli reheats in the bag. Skip it if you freeze "
     "little, since a freezer bag with the air pressed out does most of it."),
)

APPLIANCE_VALUE = APPLIANCE_VALUE + KITCHEN_MACHINE_VALUE
KITCHEN_MACHINE_NAMES = tuple(name for names, _trade in KITCHEN_MACHINE_VALUE for name in names)
for _worth_it_entry in ENTRIES:
    if _worth_it_entry.id == "appliance-worth":
        _worth_it_entry.key = ((_worth_it_entry.key[0] + KITCHEN_MACHINE_NAMES,)
                               + tuple(_worth_it_entry.key[1:]))

ENTRIES.append(entry(
    "sleeping-bag-choose",
    (("sleeping bag", "sleeping bags", "camping bag", "down bag", "mummy bag"),
     _CHOOSE_ASK),
    "Ignore the \"extreme\" number and look at the comfort rating: a 2 or 3 season bag rated to "
    "about 0C comfort covers British camping from spring to autumn, and a 3 season one is the "
    "usual first buy. Down is lighter and packs smaller but useless once wet, synthetic keeps some "
    "warmth damp and is cheaper and washable, and a mummy shape is warmer for its weight than a "
    "rectangular one. The mat under you decides how warm you sleep as much as the bag does, so "
    "spend there too.",
    avoid=("wash", "washing", "clean", "cleaning", "damp", "wet", "smell", "smells", "smelly",
           "mould", "mold", "store", "storing", "storage", "pack", "packing", "stuff sack",
           "zip", "zips", "repair", "torn", "cold at night", "cant sleep", "can't sleep",
           "sleeping badly", "insomnia", "tent", "mat", "airbed", "camping site"),
    bias=2))


ENTRIES.append(entry(
    "second-hand-worth-it",
    (("second hand", "secondhand", "second-hand", "pre owned", "preowned", "pre-owned",
      "used", "buying used", "buy used", "charity shop", "car boot", "facebook marketplace",
      "gumtree", "vinted", "ebay", "refurbished", "refurb"),
     ("cheaper", "cheap", "save", "saving", "worse", "worth", "worth it",
      "should i buy", "should i get", "should we buy", "should we get",
      "good idea", "buy", "buying", "or new", "vs new", "instead of new",
      "money", "value", "second hand", "used")),
    "Yes, usually by a third to a half, and the older the thing gets the better the saving: "
    "furniture, bikes, tools, a pram, kids' clothes and kitchen kit lose most of their value in "
    "the first year and then almost nothing. Buy new the things that wear unseen or are used "
    "against your body - a mattress, running shoes, a bike helmet, anything with a safety job "
    "(a car seat, a life jacket, a smoke alarm) - and buy new where a warranty is what you are "
    "really paying for, like a laptop or a washing machine. Check a used phone or laptop's "
    "battery health, ask for the age of a washing machine's drum, and never pay before you see "
    "it. From a shop, second-hand goods carry the same rights as new ones: 30 days to reject it, "
    "then repair or replacement; from a private seller it is buyer beware unless the advert lied.",
    avoid=("car", "cars", "van", "vans", "motorbike", "motorbikes", "vehicle", "mileage",
           "mot", "v5", "bike", "bikes", "bicycle", "cycle", "house", "flat", "mortgage",
           "phone", "phones", "mobile", "iphone", "android", "laptop", "laptops", "tablet",
           "tablets", "computer", "computer", "console", "games console",
           "sell", "selling", "sold", "sale", "declare", "tax", "to the taxman",
           "furniture", "sofa", "sofas", "couch", "couches", "settee", "armchair", "armchairs",
           "wardrobe", "wardrobes", "dresser", "sideboard", "sideboards", "bookshelf",
           "bookshelves", "bookcase", "bookcases", "bed frame", "table", "tables", "chairs",
           "cabinet", "cabinets", "chest of drawers",
           "look for", "what should i look for", "what to look for", "what should i check",
           "what to check", "check", "checks", "checking", "checked",
           "safe", "safely", "scam", "scams", "scammer", "scammed", "trust", "trustworthy",
           "risky", "risk", "insurance",
           "watch", "watches", "wristwatch", "clock", "clocks", "jewellery", "jewelry",
           "ring", "rings", "necklace", "bracelet", "earrings", "brooch", "antique",
           "antiques", "collectible", "collectibles", "vinyl", "record", "records",
           "book", "books", "novel", "novels"),
    ask=("cheaper", "worth", "should i", "buy", "buying", "save", "value")))
