import re

from .lookup import entry

ANSWERS = ("cooking", "food-and-drink")


LEFT_OUT_KEEP = ("bread", "loaf", "cake", "butter", "cheese", "cheddar", "parmesan", "jam",
                 "marmalade", "pickle",
                 "chutney", "fruit", "banana", "apple", "orange", "biscuit", "crisps",
                 "chocolate", "honey", "cereal", "flour", "sugar", "nuts", "olives", "capers")
LEFT_OUT_SOFT_CHEESE = ("soft cheese", "brie", "camembert", "mozzarella", "feta", "cream cheese",
                        "blue cheese", "stilton", "gorgonzola", "ricotta", "cottage cheese",
                        "mascarpone", "goats cheese", "goat cheese", "halloumi", "paneer")
LEFT_OUT_DAIRY = ("milk", "cream", "yoghurt", "yogurt", "custard", "ice cream", "ice-cream")
LEFT_OUT_BOTTLE = ("formula", "breast milk", "baby milk", "expressed milk", "bottle of milk",
                   "baby bottle", "baby's bottle", "bottles of milk")
LEFT_OUT_RICE = ("rice", "risotto")
LEFT_OUT_MEAT = ("chicken", "turkey", "beef", "pork", "lamb", "ham", "bacon", "sausage",
                 "meat", "steak", "steaks", "chops", "mince", "burger", "burgers", "meatballs",
                 "gammon", "venison", "duck",
                 "sausages", "fish", "salmon", "tuna", "stew", "curry", "soup", "gravy",
                 "pasta", "spaghetti", "quiche", "mayonnaise", "mayo",
                 "potato salad", "pie", "pizza", "mince", "bolognese", "chilli", "lasagne",
                 "shepherds",
                 "peas", "beans", "sweetcorn", "couscous", "stuffing", "potatoes", "mashed potato",
                 "sandwich", "sandwiches", "wrap", "wraps", "coleslaw", "sushi", "prawn",
                 "prawns", "tofu", "sauce", "sauces")
LEFT_OUT_EGG = ("egg", "eggs")
EGG_COOKED = ("cooked", "boiled", "scrambled", "fried", "poached", "omelette", "frittata",
              "hard boiled", "soft boiled", "quiche", "mayonnaise", "custard", "raw egg",
              "cracked", "broken egg", "shell", "smashed", "batter")
LEFT_OUT_ASK = ("left out", "left it out", "left them out", "left over out", "out overnight",
                "overnight", "all night", "sat out", "sit out", "sitting out", "stood out",
                "stay out", "stays out", "staying out",
                "out on the counter", "on the counter", "on the side", "on the hob",
                "out of the fridge", "forgot to put", "forgot it", "didnt put it",
                "did not put it", "room temperature", "went cold", "still out",
                "was left out", "that was left out", "left out overnight", "sat out overnight",
                "was sat out",
                "left", "out")

STILL_OK_ASK = ("still cook it", "still eat it", "can i cook it", "can i eat it", "can i still",
                "is it still ok", "still ok to eat", "still safe", "safe to eat", "still use it",
                "should i bin it", "should i throw it", "should i chuck it", "still good",
                "is it still safe", "can we still eat", "will it still be ok")

LEFT_OUT_PHRASE = tuple(phrase for phrase in LEFT_OUT_ASK if phrase not in ("left", "out"))

OUT_OF_THE_FRIDGE = ("left out", "left it out", "left them out", "left this out", "sat out",
                     "sit out", "sitting out", "stood out", "standing out", "still out",
                     "been out", "out on the", "out all night", "out overnight", "out since",
                     "on the side", "on the counter", "on the worktop", "on the hob",
                     "on the table", "on top of the", "overnight on the")


def soak_but_not_left_out(understood):
    said = str((understood or {}).get("clean") or (understood or {}).get("text") or "").lower()
    if not re.search(r"\bsoak", said):
        return True
    return any(phrase in said for phrase in OUT_OF_THE_FRIDGE)
_FREEZER_WORD = re.compile(r"\bfreez(?:e|es|er|ers|ing|ed)?\b|\bfrozen\b", re.I)
_OUT_OF_THE_FREEZER = re.compile(
    r"\bout\s+(?:of\s+)?(?:the\s+|my\s+|a\s+|your\s+|its\s+|their\s+)?freez(?:er|ers)\b", re.I)


def soak_but_not_left_out_or_in_the_freezer(understood):
    if not soak_but_not_left_out(understood):
        return False
    said = str((understood or {}).get("clean") or (understood or {}).get("text") or "").lower()
    if _FREEZER_WORD.search(said) and not _OUT_OF_THE_FREEZER.search(said):
        return False
    return True


_LEAVING_VERB = (r"leave|leaves|leaving|left|forget|forgets|forgot|forgotten")
_LEAVING_OUT = re.compile(
    r"(?:\b(?:" + _LEAVING_VERB + r"|"
    r"sit|sits|sitting|sat|stand|stands|standing|stood|stay|stays|stayed|"
    r"keep|keeps|kept|been|being|is|are|was|were|still)\b"
    r"(?:\W+\w+){0,6}?\W+out\b(?!\s+of\b)"
    r"|\bout\b(?:\W+\w+){0,6}?\W+(?:" + _LEAVING_VERB + r")\b"
    r"|\bout\s+of\s+(?:the\s+|my\s+|a\s+|your\s+|its\s+)?(?:freez(?:er|ers)|fridge)\b)")


LEFT_OUT_FOODS = tuple(sorted(set(LEFT_OUT_MEAT) | set(LEFT_OUT_RICE) | set(LEFT_OUT_DAIRY)
                              | set(LEFT_OUT_KEEP) | set(LEFT_OUT_SOFT_CHEESE)
                              | set(LEFT_OUT_EGG) | set(LEFT_OUT_BOTTLE)
                              | {"food", "leftovers", "leftover", "takeaway", "sauce",
                                 "sandwich", "wrap", "curry", "soup", "stew"}))


def _asks_if_it_is_still_all_right(text):
    return any(phrase in text for phrase in STILL_OK_ASK)


def _the_line_it_leans_on(memory, reading, text):
    if _leaving_out(text):
        return text, False
    if not _asks_if_it_is_still_all_right(text):
        return text, False
    earlier = ""
    leans = reading.get("leans_on") if isinstance(reading, dict) else None
    if isinstance(leans, dict):
        earlier = str(leans.get("text") or "").lower()
    if not earlier:
        try:
            from ..memory import last_user
            earlier = str(last_user(memory) or "").lower()
        except Exception:
            earlier = ""
    earlier = " " + earlier + " "
    if not earlier.strip():
        return text, False
    if not (_names_any(earlier, LEFT_OUT_FOODS) and _leaving_out(earlier)):
        return text, False
    named = _names_any(text, LEFT_OUT_FOODS)
    if named and not set(named) & set(_names_any(earlier, LEFT_OUT_FOODS)):
        return text, False
    return earlier + text, True


def says_a_food_was_left_out(text):
    return _leaving_out(" " + str(text or "").lower() + " ")


def _leaving_out(text):
    if any(phrase in text for phrase in LEFT_OUT_PHRASE):
        return True
    return bool(_LEAVING_OUT.search(text))

_COUNT_WORDS = {"a": 1, "an": 1, "one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
                "six": 6, "half": 0.5, "couple": 2, "couple of": 2, "few": 3, "a few": 3,
                "several": 3, "twelve": 12}
_SPAN = re.compile(r"\b(\d+(?:\.\d+)?|a few|couple of|half|a|an|one|two|three|four|five|six|"
                   r"several|twelve|few|couple)\s*(hours?|hrs?|minutes?|mins?)\b")


def _hours_out(text):
    found = _SPAN.search(text)
    if found:
        count = _COUNT_WORDS.get(found.group(1))
        if count is None:
            try:
                count = float(found.group(1))
            except (TypeError, ValueError):
                return None
        return count / 60.0 if found.group(2).startswith("min") else count
    if re.search(r"\b(overnight|all night|the night|night|next morning|in the morning)\b", text):
        return 8.0
    return None


def _names_any(text, words):
    return [word for word in words if re.search(r"\b" + re.escape(word) + r"\b", text)]


def _agree(thing):
    many = thing.endswith("s") and not thing.endswith("ss")
    return {"be": "are" if many else "is", "were": "were" if many else "was",
            "them": "them" if many else "it", "they": "they" if many else "it",
            "look": "look" if many else "looks", "smell": "smell" if many else "smells"}


def _how_long(text, soft, kept, meat, rice, dairy):
    if soft:
        return ("Two hours on the side is the line for soft cheese: past that, bin it, because "
                "brie, camembert, mozzarella, feta and cream cheese can carry listeria, which "
                "grows in the fridge and changes neither the taste nor the smell. Hard cheese is "
                "the exception and can stay out a lot longer.")
    if rice:
        return ("Two hours is the line for cooked rice, and it is the strictest food there is: "
                "cool it fast, get it into the fridge within the hour and eat it within a day, "
                "because the toxin it can grow survives reheating.")
    if meat:
        return ("Two hours is the line for cooked meat, fish, gravy, pasta and anything with egg "
                "or mayonnaise in it - past that it is a bin job even if it looks and smells "
                "fine. Rice is the same. Bread, cake, butter, hard cheese, jam and fruit are the "
                "exceptions and come to no harm at all.")
    if dairy:
        return ("Two hours for milk, cream and yoghurt, and a whole night out is the bin job: "
                "they sour and can grow bacteria you cannot see or smell. Go by the smell if it "
                "is borderline.")
    if kept:
        word = kept[0]
        verb = _agree(word)
        return ("{thing} {be} one of the ones with no time limit: there was never a food-poisoning "
                "risk at room temperature, so a night out only makes {them} stale, dry or soft. "
                "The two hours and the bin apply to cooked meat, rice, milk and anything with "
                "mayonnaise.").format(thing=word.capitalize(), be=verb["be"], them=verb["them"])
    return ("Two hours out of the fridge is the line for anything cooked, and after a whole night "
            "it is a bin job - meat, fish, rice, milk and anything with egg or mayonnaise "
            "especially. Bread, cake, butter, hard cheese, jam and fruit are the exceptions and "
            "keep for a long time on the side.")


_CHICKEN_OUT = re.compile(r"\bchicken(?:s|ed|ing)?\s+out\b")
_LEFTOVER_WORD = re.compile(r"\b(?:left ?over|leftovers?|spare)\b")
_LEFT_OUT_WORD = re.compile(
    r"\b(?:left|leave|leaves|leaving|forgot|forget|forgotten|sat|sit|sits|sitting|stood|stand|"
    r"standing|still|overnight|nite|tonight|night|hours?|counter|side|worktop|hob|fridge|"
    r"freezer|frozen|defrost|out of)\b")
_OUT_OF_PLACE_WORD = re.compile(
    r"\b(?:out|overnight|nite|tonight|night|hours?|counter|side|worktop|hob|fridge|"
    r"freezer|frozen|defrost|room temperature|sat|sit|sits|sitting|stood|standing|still)\b")
COOKING_RESULT = ("came out", "come out", "comes out", "came up", "turned out", "turn out",
                  "turns out", "boiled over", "boils over", "boiling over", "boil over",
                  "boiled dry", "boils dry", "boiling dry", "caught on the bottom",
                  "catches on the bottom", "stuck to the pan", "sticks to the pan",
                  "stuck to the bottom", "went wrong", "goes wrong", "gone wrong")
_SAID_OUT = re.compile(
    r"\b(?:left|leave|leaves|leaving|sat|sitting|stood|standing|kept|been)\b[^.]{0,20}?\bout\b"
    r"|\bout\s+(?:overnight|all\s+night|all\s+day|since|for)\b"
    r"|\b(?:overnight|all\s+night|all\s+day|this\s+morning|last\s+night|yesterday)\b"
    r"|\bfor\s+(?:\d+|a\s+few|a\s+couple\s+of|a|an)\s*(?:minutes?|mins?|hours?|hrs?)\b", re.I)

_TAKING_OUT = re.compile(r"\b(?:take|takes|taking|took|taken|get|gets|getting|got)\b"
                         r"[^.;]{0,24}\bout\b")
_SPENT_ON_THE_SIDE = re.compile(r"\b(?:overnight|nites?|nights?|tonight|hours?|counter|worktop|"
                                r"hob|side|room temperature|since|left it|leaving it)\b")
_A_BIRD = re.compile(r"\b(?:chicken|chickens|poultry)\b")

BURNT_WORK = ("burnt", "burned", "burning", "burn", "scorched", "blackened", "charred")
BURNT_VESSEL = ("pan", "pans", "pot", "pots", "tin", "tins", "tray", "trays", "shelf", "shelves",
                "oven", "hob", "wok", "saucepan", "saucepans", "skillet", "griddle", "baking tray",
                "cake tin", "roasting tin", "baking tin", "baking sheet", "casserole")


def _left_out(memory, reading):
    text = " " + (reading.get("clean") or "").lower() + " "
    text, borrowed = _the_line_it_leans_on(memory, reading, text)
    reply = _left_out_card(text)
    return _the_follow_up(text, reply) if borrowed and reply else reply


def _left_out_card(text):
    if _CHICKEN_OUT.search(text) and not _LEFT_OUT_WORD.search(text):
        return None
    if (_TAKING_OUT.search(text) and _A_BIRD.search(text)
            and not _SPENT_ON_THE_SIDE.search(text)):
        return None
    if not _leaving_out(text):
        return None
    if (_names_any(text, COOKING_RESULT) and _hours_out(text) is None
            and not _SAID_OUT.search(text)):
        return None
    if _LEFTOVER_WORD.search(text) and not _OUT_OF_PLACE_WORD.search(text):
        return None
    hours = _hours_out(text)
    short = hours is not None and hours <= 2
    soft = _names_any(text, LEFT_OUT_SOFT_CHEESE)
    kept = _names_any(text, LEFT_OUT_KEEP)
    meat = _names_any(text, LEFT_OUT_MEAT)
    rice = _names_any(text, LEFT_OUT_RICE)
    dairy = _names_any(text, LEFT_OUT_DAIRY)
    egg = _names_any(text, LEFT_OUT_EGG)
    cooked_egg = bool(egg) and bool(_names_any(text, EGG_COOKED))

    if _names_any(text, BURNT_WORK) and _names_any(text, BURNT_VESSEL):
        return None

    sitting = any(word in text for word in (" sit", "sits", "sitting", " leave", "leaves",
                                            "out", "keep", "keeps"))
    if "how long" in text and sitting and not cooked_egg:
        return _how_long(text, soft, kept, meat, rice, dairy)

    if cooked_egg and not meat:
        meat = ["egg"]

    if egg and not cooked_egg and not short:
        return ("Whole eggs are fine: they are sold and kept on a shelf at room temperature and "
                "keep for weeks, so a night on the side changes nothing. It is a cracked egg, or "
                "a cooked one - scrambled, boiled, fried, an omelette - that follows the two-hour "
                "rule and goes in the bin after a night out.")

    if soft:
        if short:
            return ("Inside the two hours, so it is fine even for this one: get it back in the "
                    "fridge now and eat it within a couple of days. Soft cheese is the risky end "
                    "of cheese, so it does not get the long stay a hard cheddar does.")
        return ("Bin it, I'm afraid. Soft cheese is the risky end of cheese: brie, camembert, "
                "mozzarella, feta, cream cheese and blue cheese can carry listeria, which grows in "
                "the fridge and does not change the taste or the smell. Anything more than two "
                "hours out is a bin job, and a hard cheese is the only one you can leave.")
    if kept and not (meat or rice or _names_any(text, LEFT_OUT_DAIRY)):
        word = kept[0]
        verb = _agree(word)
        return ("{thing} {be} one of the safe ones: there was never a food-poisoning risk at room "
                "temperature, so a night on the side only makes {them} stale, dry or soft. Put "
                "{them} back and carry on - it is cooked meat, rice, milk and anything with "
                "mayonnaise that you cannot leave out.").format(
                    thing=word.capitalize(), be=verb["be"], them=verb["them"])
    bottle = _names_any(text, LEFT_OUT_BOTTLE)
    if bottle:
        if hours is not None and hours >= 3:
            return ("Bin it. A made-up bottle is two hours from the moment it is made, and an "
                    "hour once the baby has started it, whatever the room is like: bacteria from "
                    "the baby's mouth get into the milk and warm milk grows them fast. It is not "
                    "one of the things you can judge by smell.")
        return ("Made-up formula or expressed milk is good for two hours at room temperature and "
                "a bottle the baby has started for one hour, so this one is inside the window: use "
                "it now rather than later, and past two hours it is a bin job. It is not dairy you "
                "can test by smell - two hours is the number, not the sniff.")
    if _names_any(text, LEFT_OUT_DAIRY):
        if short:
            return ("A couple of hours on the table is fine for milk, cream and yoghurt: get it "
                    "back in the fridge now and it will be good to the date on the pack. A whole "
                    "night out is the bin job, because they sour and can grow bacteria you cannot "
                    "smell.")
        return ("Milk, cream and yoghurt are fine on the table for a couple of hours at a meal, and "
                "a whole night out is a bin job: they sour and can grow bacteria you cannot see or "
                "smell. Keep it at the back of the fridge, not in the door, and go by the smell if "
                "you are not sure.")
    if rice:
        if short:
            return ("Inside the two hours, so it is fine: get it into the fridge now in a shallow "
                    "tub so it cools fast, and eat it within a day. Rice is the one to be careful "
                    "with, because the toxin it can grow survives reheating.")
        return ("Bin it after 2 hours out, and this one is the strictest of the lot: cooked rice "
                "can grow a toxin that reheating does not destroy, and it looks and smells fine "
                "while it does it. Next time cool it fast, fridge it within the hour, and eat it "
                "within a day.")
    if meat:
        word = meat[0]
        verb = _agree(word)
        if short:
            return ("{thing} inside the two-hour limit {be} fine: get {them} into the fridge "
                    "now, where cooked food keeps 3 days. It is only past two hours that this "
                    "becomes a bin job.").format(thing=word.capitalize(), be=verb["be"],
                                                  them=verb["them"])
        return ("Bin it, I'm afraid. {thing} left out for more than 2 hours {be} not safe to eat, "
                "even if {they} {look} and {smell} fine. Meat, fish, gravy and anything with egg or "
                "mayonnaise in it all follow that rule, so next time get it into the fridge "
                "within the hour.").format(
                    thing=word.capitalize(), be=verb["be"], they=verb["they"],
                    look=verb["look"], smell=verb["smell"])
    if short:
        return ("Inside the two hours, so it is fine: get it covered into the fridge now and eat "
                "it within a day or two. Two hours out is the limit, and it is a night out that "
                "makes it a bin job.")
    return ("Two hours out of the fridge is the line, and after a whole night it is a bin job for "
            "anything cooked, especially meat, fish, rice, milk or a dish with mayonnaise or egg "
            "in it. Bread, cake, butter, hard cheese, jam and fruit are the exceptions and come to "
            "no harm.")


def the_still_ok_follow_up(text, memory):
    here = " " + str(text or "").lower() + " "
    if _leaving_out(here) or _asks_if_it_is_still_all_right(here):
        verdict = _the_left_out_follow_up(here, memory)
        if verdict:
            return verdict
    return _the_food_it_just_said_to_bin(here, memory)


def _the_left_out_follow_up(here, memory):
    earlier = ""
    try:
        from ..memory import last_user
        earlier = " " + str(last_user(memory) or "").lower() + " "
    except Exception:
        return None
    if not (_names_any(earlier, LEFT_OUT_FOODS) and _leaving_out(earlier)):
        return None
    named = _names_any(here, LEFT_OUT_FOODS)
    if named and not set(named) & set(_names_any(earlier, LEFT_OUT_FOODS)):
        return None
    card = _left_out_card(earlier + here)
    if not card:
        return None
    return _the_follow_up(earlier + here, card)

SAYS_BIN = ("bin it", "bin them", "into the bin", "in the bin", "throw it away", "throw it out",
            "throw them away", "chuck it", "dispose of it")
HOW_IT_IS_KEEPING = ("going off", "gone off", "smells off", "smell off", "smells bad",
                    "smells funny", "is it ok", "still ok", "still good", "is it safe",
                    "is it off", "gone bad", "has gone bad", "use by", "out of date",
                    "past its date", "off yet", "gone slimy", "is it still")
WHAT_TO_DO_WITH_IT = re.compile(
    r"\b(?:what|what can i|what can we|what should i|what shall i|what do i|what will i)\b"
    r"[^.?!]*\b(?:do|make|cook|use|eat)\b[^.?!]*\b(?:with (?:it|them|that|this))\b"
    r"|\b(?:can|could|should|shall|will|is it ok to|is it safe to|is it fine to)\b"
    r"[^.?!]*\b(?:still )?(?:cook|use|eat|keep|freeze|save)\b", re.I)


def _the_food_it_just_said_to_bin(here, memory):
    if not WHAT_TO_DO_WITH_IT.search(here):
        return None
    try:
        from ..memory import last_bot, last_user
        said = " " + str(last_bot(memory) or "").lower() + " "
        earlier = " " + str(last_user(memory) or "").lower() + " "
    except Exception:
        return None
    if not any(words in said.split(". ")[0] for words in SAYS_BIN):
        return None
    if not (_asks_if_it_is_still_all_right(earlier) or _leaving_out(earlier)
            or any(words in earlier for words in HOW_IT_IS_KEEPING)):
        return None
    food = _names_any(earlier, LEFT_OUT_FOODS)
    if not food:
        return None
    named = _names_any(here, LEFT_OUT_FOODS)
    if named and not set(named) & set(food):
        return None
    thing = food[0]
    agree = _agree(thing)
    return ("Nothing to cook, I'm afraid: {thing} that {look} or {smell} like that {be} a bin "
            "job, and no recipe makes {them} safe - heat kills the bacteria growing on {them} "
            "but not the toxins they have already left behind. If the only thing wrong with "
            "{them} is the date on the packet, use {them} tonight rather than keep {them} for "
            "another day."
            .format(thing=thing, look=agree["look"], smell=agree["smell"], be=agree["be"],
                    they=agree["they"], them=agree["them"]))


def _the_follow_up(text, reply):
    first = reply.split(". ")[0].lower()
    if "bin" not in first or _names_any(text, LEFT_OUT_BOTTLE):
        return reply
    hours = _hours_out(text)
    if hours is not None and hours <= 2:
        return ("Inside the two hours, so yes: use it now rather than later, and do not put it "
                "back in the fridge to keep. Two hours out is the line - past that it is a bin "
                "job even when it looks and smells fine.")
    return ("Bin it, I'm afraid: past two hours out it is not safe, and cooking does not undo "
            "that - heat kills the bacteria that grew while it sat out, but not the toxins some "
            "of them have already left behind, so it can still make you ill. Two hours is the "
            "line for meat, fish, rice, milk and anything with egg or mayonnaise in it.")


def _in_the_car(memory, reading):
    text = " " + (reading.get("clean") or "").lower() + " "
    thing = None
    for words in (LEFT_OUT_BOTTLE, LEFT_OUT_DAIRY, LEFT_OUT_MEAT, LEFT_OUT_KEEP):
        found = _names_any(text, words)
        if found:
            thing = found[0]
            break
    hot = bool(re.search(r"\b(hot day|heatwave|in the sun|all afternoon|all day|sunny|summer|"
                         r"hot car|warm car)\b", text))
    if thing is None:
        thing = "food"
    if hot:
        return ("{Thing} in a hot car is the worst place it can be: a warm car gets well past "
                "fridge temperature, so count it as more than two hours out and bin anything "
                "cooked, dairy or made with mayonnaise that spent the afternoon there. On a hot "
                "day a cool bag, or buying the {thing} last, saves the whole question."
                ).format(Thing=thing.capitalize(), thing=thing)
    if re.search(r"\b(car|cars|boot|back seat|van|drive)\b", text):
        where = ("A car is a warm room with no fridge in it, so the two-hour rule applies to the "
                 "{thing} as it does anywhere else: fine for the drive home, then straight into "
                 "the fridge.")
    else:
        where = ("Out of the fridge with no cool bag is the same as the table, so the two-hour "
                 "rule applies to the {thing} as it does anywhere else: fine for the journey, "
                 "then into the fridge as soon as you are in.")
    return (where + " Anything cooked, dairy or made with mayonnaise that spent the afternoon "
            "warm is a bin job - warmth is what the bacteria that change neither taste nor "
            "smell need.").format(thing=thing)


def _marinate(memory, reading):
    text = " " + (reading.get("clean") or "").lower() + " "
    meat = _names_any(text, ("chicken", "fish", "salmon", "prawns", "turkey"))
    if meat:
        return ("Overnight is fine for a marinade, in the fridge: {thing} takes 30 minutes to 2 "
                "hours at room temperature and up to a day in the fridge, and the fridge is the "
                "safer way to do it. Whisk 3 parts oil to 1 part acid - lemon, wine or vinegar - "
                "with salt, then garlic, honey, soy or herbs.").format(thing=meat[0])
    return ("Overnight is what a marinade is for, and it belongs in the fridge: tougher cuts take "
            "4 hours or a full night, steak and lamb chops a few hours, and fish no more than an "
            "hour because the acid starts to cure it. Whisk 3 parts oil to 1 part acid - lemon, "
            "wine or vinegar - with salt, then garlic, honey, soy or herbs. More than a day in "
            "acid or sugar turns the meat mushy.")


_A_FAULT_IN_THE_FOOD = re.compile(
    r"\b(?:too (?:spicy|hot to eat|hot for|salty|salt\w*|sweet|sour|bitter|thick|thin|dry|bland)"
    r"|way too (?:spicy|hot|salty)|far too (?:spicy|hot|salty)|cool it down|make it milder"
    r"|less spicy|too much (?:chilli|chili|salt|spice))\b")

_A_COOLING_SUBJECT = frozenset((
    "fridge", "refrigerator", "cool", "cooling", "cooled", "warm", "warmish", "hot", "lukewarm",
    "steaming", "leftover", "leftovers", "food", "stew", "curry", "soup", "rice", "pasta",
    "chilli", "chili", "casserole", "chicken", "meat", "pot", "pots", "pan", "saucepan",
    "milk", "bottle", "cake", "cakes", "sponge", "batch", "bolognese", "sauce", "stock",
    "tub", "tupperware", "containers", "container", "boxes", "box",
))


_GADGETS = ("phone", "phones", "mobile", "iphone", "android", "smartphone", "camera", "watch",
            "tablet", "ipad", "laptop", "airpods", "headphones", "earbuds", "keyboard", "remote",
            "sim card", "memory card", "screen", "battery", "charger", "charging port")


def _a_gadget_in_the_talk(memory, understood):
    if any(word in str(understood.get("clean") or "").lower() for word in _GADGETS):
        return True
    turns = (memory or {}).get("turns") or ()
    recent = [str(one.get("user") or "").lower() for one in turns[-3:] if isinstance(one, dict)]
    return any(word in line for line in recent for word in _GADGETS)


def _cool_before_fridge(memory, understood):
    words = set()
    for word in (understood.get("words") or ()):
        if isinstance(word, str):
            words.add(word.lower())
    said = str(understood.get("clean") or "").lower()
    if not words & _A_COOLING_SUBJECT:
        return None
    if _A_FAULT_IN_THE_FOOD.search(str(understood.get("clean") or "").lower()):
        return None
    if re.search(r"\bwhat time\b|\bwhen should i\b|\bwhen do i\b|\bwhat time do i\b", said) \
            and not re.search(r"\b(?:fridge|freez\w*|refrigerat\w*|cool\w*|cold|ice|chill\w*|"
                              r"worktop|defrost\w*)\b", said):
        return None
    if _a_gadget_in_the_talk(memory, understood):
        return None
    quick = words & {"quickly", "quick", "fast", "faster", "fastest", "quickest", "rapidly",
                     "speed", "sooner", "hurry"}
    if "rice" in words:
        return ("Cool cooked rice fast, not slowly: spread it in a shallow tray and leave it no "
                "more than an hour, then cover it and put it in the fridge and eat it within a "
                "day, reheated until it is steaming hot. Rice left at room temperature grows a "
                "toxin that reheating does not destroy, which is why it gets an hour where a "
                "stew gets two.")
    if words & {"milk", "bottle", "bottles", "formula", "bottle of milk", "breast milk"}:
        return ("Stand the bottle in a jug of cold water for ten minutes, or hold it under the "
                "cold tap, then put it straight back in the fridge. Milk that has been warmed "
                "keeps about two days, so use it before the rest of the bottle and do not warm "
                "it twice - and never keep what a baby has already drunk from.")
    if words & {"cake", "cakes", "sponge", "brownie", "brownies", "muffin", "muffins",
                "cupcake", "cupcakes", "loaf", "loaves", "traybake", "bread", "buns"}:
        return ("Leave it in the tin for ten minutes, then turn it out onto a rack and let it go "
                "cold before anything goes on it: a warm cake steams itself soggy and the icing "
                "slides off. Do not put it in the fridge to speed it up - a chilled sponge goes "
                "heavy and stale faster than one kept in a tin.")
    if quick:
        return ("Stand the pot in a sink of cold water, with a cold pack or a tray of ice in it, "
                "and stir every few minutes: a big pot comes down to warm in about 20 minutes "
                "rather than two hours. Then cover it and put it in the fridge - it does not "
                "need to be stone cold, just not steaming. Past two hours out of the fridge, "
                "bin it.")
    if words & {"pot", "pots", "pan", "saucepan", "stew", "soup", "curry", "chilli", "chili",
                "casserole", "stock", "batch", "bolognese", "sauce"}:
        return ("Let it cool on the worktop for up to two hours, then cover it and put it in the "
                "fridge. A big pot straight off the hob warms the whole fridge, so split it into "
                "shallow tubs first - it does not need to be stone cold, just not steaming. "
                "Past two hours out, bin it.")
    return ("Spread it out in a shallow tub so it cools faster, leave it on the worktop for up to "
            "two hours, then cover it and put it in the fridge - it does not need to be stone "
            "cold, just not steaming. Eat leftovers within two days and reheat them until they "
            "are steaming hot all through. Past two hours out of the fridge, bin it.")


PAST_IT_PRODUCE = ("banana", "bananas", "apple", "apples", "pear", "pears", "grape", "grapes",
                   "berries", "strawberries", "raspberries", "blueberries", "peach", "peaches",
                   "plum", "plums", "mango", "avocado", "avocados", "tomato", "tomatoes",
                   "spinach", "lettuce", "salad", "salad leaves", "rocket", "watercress",
                   "kale", "cabbage", "leafy", "greens", "carrot", "carrots", "cucumber",
                   "pepper", "peppers", "courgette", "courgettes", "broccoli", "cauliflower",
                   "onion", "onions", "fruit", "vegs", "vegetables", "veg", "produce")
PAST_IT_STATE = ("gone soft", "went soft", "gone a bit soft", "a bit soft", "soft", "softened",
                 "wrinkly", "wrinkled", "shrivelled", "shrunken", "limp", "wilting", "wilted",
                 "floppy", "rubbery", "dry", "dryish", "stale", "gone a bit", "old", "slimy",
                 "slimey", "sticky",
                 "smelling", "smells", "smelly", "sour", "leaking", "mouldy", "mould",
                 "black spots", "spotty")
PAST_IT_ASK = ("can i eat", "can i still", "is it ok", "is it still", "still ok", "still good",
               "still safe", "safe to eat", "eat it", "eat them", "use it", "use them",
               "should i bin", "throw it", "throw them", "chuck it", "ruined", "bin it",
               "what can i do with", "why is my", "why has my", "why are my", "why have my",
               "are they ok", "is it fine", "ok to eat", "gone a bit", "old", "been there a while",
               "has gone", "have gone", "went soft", "gone soft", "smells", "smelly", "slimy")
PAST_IT_BIN = ("slimy", "slimey", "sticky", "sour", "smelly", "smells", "stinks", "mouldy",
               "mould", "mold", "furry", "fuzz", "leaking", "gone off", "went off", "rotten")
PAST_IT_KINDS = (
    (("spinach", "lettuce", "salad", "salad leaves", "rocket", "watercress", "kale", "cabbage",
      "leafy", "greens"),
     "Leaves that have gone a bit yellow or brown are older, not unsafe: the colour is the leaf "
     "giving up its green, and it does not make anybody ill. Pick out any that are slimy or "
     "smelly - those are the ones to bin - and eat or cook the rest, because a yellowed leaf is "
     "still good wilted in a pan or stirred into soup."),
    (("banana", "bananas"),
     "A soft banana is a ripe one: the starch has turned to sugar, so it is sweeter and easier to "
     "mash - eat it, or put it in a smoothie or banana bread. A banana is the fruit that keeps "
     "best in the fruit bowl, never the fridge."),
    (("grape", "grapes"),
     "A wrinkly grape has lost water and is sweeter for it, so eat them - and pick out any that "
     "are leaking or furred, because one going over spoils the rest in the punnet."),
    (("berries", "strawberries", "raspberries", "blueberries", "blackberries"),
     "A soft berry has only lost water, so it is still fine to eat - pick out any that are "
     "leaking or furred, because one going over spoils the rest in the punnet, and eat them "
     "sooner rather than later or cook them down with a little sugar."),
    (("apple", "apples", "pear", "pears", "peach", "peaches", "plum", "plums", "mango"),
     "A soft or shrivelled apple or pear has lost water: it is fine to eat, and it is at its best "
     "stewed, baked or in a crumble."),
    (("carrot", "carrots"), "A floppy carrot has lost water, not gone off: peel it and it is fine "
     "to eat, and standing it in a glass of cold water for an hour firms it up again."),
    (("cucumber", "courgette", "courgettes", "pepper", "peppers", "broccoli", "cauliflower"),
     "A soft cucumber, pepper or courgette has lost water and is fine, just not crisp: cook it "
     "rather than eat it raw, and cut away any soft spots."),
    (("tomato", "tomatoes"), "A soft tomato is fine and sweeter: cook it into a sauce rather than "
     "slice it raw, and use it before the ones around it go too."),
)
PAST_IT_GENERAL = ("It has lost water rather than gone off, so it is still fine to eat and better "
                   "cooked than raw.")


_STATE_WORD = re.compile(
    r"\b(?:" + "|".join(re.escape(word) for word in sorted(PAST_IT_STATE, key=len, reverse=True))
    + r")\b")


_NOT_WANTING_TO_EAT = re.compile(
    r"\b(?:wont eat|won't eat|will not eat|wouldn't eat|would not eat|doesn't eat|does not eat"
    r"|refuses|refusing|refused|fussy|picky|won't touch|wont touch|will not touch|year old"
    r"|toddler|my son|my daughter|my child|my kid|my kids|children|kids|nursery|school dinner"
    r"|fed up of|sick of eating|only eats|ate nothing|eats nothing|barely eats)\b")


_HOW_TO_MAKE_IT_SO = re.compile(
    r"\b(?:how do i|how do you|how can i|how to|how would i|how should i|whats the best way to"
    r"|what's the best way to|best way to|quickest way to|easiest way to|any way to|way of)"
    r"(?:\W+\w+){0,2}?\W+(?:dry|drying|dry them|dry it|dehydrate|pickle|pickling|freeze|freezing"
    r"|ferment|fermenting|cure|curing|smoke|smoking|bottle|bottling|can|canning|preserve"
    r"|preserving|keep|keeping|store|storing|revive|reviving|crisp up|crisp it up)\b")


def _says_the_state(understood):
    said = str((understood or {}).get("clean") or (understood or {}).get("text") or "").lower()
    if _NOT_WANTING_TO_EAT.search(said):
        return False
    if _HOW_TO_MAKE_IT_SO.search(said):
        return False
    return bool(_STATE_WORD.search(said))


def _past_its_best(memory, understood):
    text = " " + str((understood or {}).get("clean") or (understood or {}).get("text")
                     or "").lower() + " "
    named = _names_any(text, PAST_IT_PRODUCE)
    if not named:
        return None
    if any(word in text for word in PAST_IT_BIN):
        return ("Bin it. The feel and the smell are what the stomach reacts to, not the colour, "
                "and cooking does not make it safe again: the bacteria that grew leave toxins "
                "behind that heat does not touch. Compost it and wash the drawer it was in.")
    for names, said in PAST_IT_KINDS:
        if any(word in text for word in names):
            return said
    return PAST_IT_GENERAL



_A_PERIOD_OF_TIME = re.compile(
    r"\b(?:\d+|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|a|an|another|few"
    r"|several|couple(?=\s+of))\s+"
    r"(?:day|days|week|weeks|fortnight|fortnights|month|months|night|nights)\b"
    r"|\bsince\s+(?:yesterday|monday|tuesday|wednesday|thursday|friday|saturday|sunday)\b"
    r"|\b(?:been|sat|sitting|stood|stored|kept|left|made|cooked|bought)\b(?:\W+\w+){0,4}?\W+"
    r"(?:in|inside|out)\s+of\s*the\s+(?:fridge|refrigerator)\b")


_COLD_MACHINE = re.compile(
    r"\b(?:my|the|our|your|his|her|their|this|that|a|an)\s+"
    r"(?:fridge freezer|fridge|freezer)\b")
_IN_THE_DISH = re.compile(
    r"\b(?:pot|pots|pan|pans|saucepan|saucepans|wok|bowl|bowls|tub|tubs|tray|trays|stew|stews|"
    r"casserole|casseroles|curry|curries|soup|soups|rice|pasta|chilli|chili|stock|leftover|"
    r"leftovers|dish|dishes|pie|pies|roast|chicken|meat|joint|batch|bolognese|sauce|beans|"
    r"lentils|porridge|pudding|cake|cakes|bread|bottle|bottles|milk|formula|yoghurt|yogurt|"
    r"cream|muffin|muffins|loaf|loaves)\b")


def the_cold_machine_and_not_the_dish(understood):
    said = " ".join(str(word).lower() for word in ((understood or {}).get("words") or ()))
    if not said:
        said = str((understood or {}).get("clean") or (understood or {}).get("text") or "").lower()
    return not (_COLD_MACHINE.search(said) and not _IN_THE_DISH.search(said))


def a_cooling_question_not_a_keeping_one(understood):
    said = " ".join(str(word).lower() for word in ((understood or {}).get("words") or ()))
    if not said:
        said = str((understood or {}).get("text") or "").lower()
    return not _A_PERIOD_OF_TIME.search(said)


_DRY_LOAF = re.compile(r"\b(?:hard|hardened|dry|dried|stale|stalish|tough|crusty|brittle)\b")
_BREAD_SPOILT = re.compile(r"\b(?:mould|mouldy|mold|moldy|green|blue|furry|fuzz|fluff|spores|"
                           r"spots|speckled|specked|smell|smells|smelly|smelt|slimy|damp)\b")

_HOW_TO_KEEP_IT_FRESH = re.compile(
    r"\b(?:how do i stop|how to stop|how do i keep|how to keep|how can i keep|how can you keep"
    r"|stop it going|stop them going|prevent|keep it fresh|keep them fresh|keep bread|keep a loaf"
    r"|make it last|make bread last|last longer|stay fresh|keep fresh|fresh for longer)\b")


def _not_just_a_hard_loaf(understood):
    said = str((understood or {}).get("clean") or (understood or {}).get("text") or "").lower()
    if not _DRY_LOAF.search(said):
        return True
    return bool(_BREAD_SPOILT.search(said))


def _not_how_to_keep_it_fresh(understood):
    said = str((understood or {}).get("clean") or (understood or {}).get("text") or "").lower()
    return not _HOW_TO_KEEP_IT_FRESH.search(said)


ENTRIES = [
    entry("cool-before-fridge",
          (("warm", "warmish", "hot", "still warm", "lukewarm", "cool", "cooled", "cooling",
            "room temperature", "steaming", "left to cool", "leftover", "leftovers", "stew",
            "curry", "soup", "rice", "chilli", "casserole", "pasta", "meat", "chicken", "food"),
           ("fridge", "refrigerator", "put it in", "put them in", "put in the fridge",
            "put it in the fridge", "in the fridge", "store", "keep it", "put away",
            "how do i cool", "how to cool", "cool it quickly", "cool them quickly",
            "cool down quickly", "quickest way to cool", "fastest way to cool",
            "cool quickly", "cool it down")),
          _cool_before_fridge,
          guard=lambda understood: (a_cooling_question_not_a_keeping_one(understood)
                                     and the_cold_machine_and_not_the_dish(understood)),
          bias=1,
          avoid=("freezer", "freeze", "frozen", "defrost", "refreeze", "reheat", "oven",
                 "microwave", "how long", "how many", "keeps", "last", "lasts",
                 "how do i store", "how to store", "how should i store", "storing", "storage",
                 "keep for", "keeps for", "how long do leftovers keep",
          "what can i cook", "what can i make", "what shall i cook", "what shall i make",
          "what to cook", "what to make", "what can i do with", "meal ideas", "dinner ideas",
                 "claim", "claims", "refund", "money back", "compensat", "who pays",
                 "insurance", "ruined", "wasted", "spoiled", "spoilt",
                 "go warm", "goes warm", "getting warm", "gets warm",
                 "fridge is warm", "fridge is cold", "fridge feels warm", "fridge feels cold",
                 "partially warm", "slightly warm", "half warm", "barely cold",
                 "fridge too warm", "fridge is not cold", "fridge isnt cold",
                 "stopped cooling", "not cooling", "stopped getting cold", "not getting cold",
                 "temperature", "thermometer", "fridge smells", "warm in the fridge",
                 "not cold", "isn't cold", "isnt cold", "stopped working", "power cut",
                 "power went off", "thermometer", "drinks", "beer", "wine",
                 "when i take it out", "out of the fridge",
                 "day", "days", "tomorrow", "next day",
                 "how long", "keeps", "keeping", "will it keep", "does it keep", "raw",
                 "phone", "phones", "mobile", "iphone", "camera", "watch", "tablet", "laptop",
                 "airpods", "headphones", "keyboard", "remote", "sim", "battery", "charger",
                 "wont turn on", "wont turn off", "wont charge", "wont switch on", "wet",
                 "all night", "overnight", "still ok", "still okay", "still safe",
                 "still good", "still fine", "safe to eat", "can i eat it", "can i eat that",
                 "can i eat them", "is it ok to eat", "do i have to bin", "throw it away",
                 "too warm", "warm fridge", "fridge is too", "fridge so warm",
                 "flat", "room", "rooms", "house", "bedroom", "the heat", "sun", "sunburn",
                 "burn", "burnt", "scald", "fever", "temperature of", "baby", "babies", "child",
                 "toddler", "after a run", "after exercise", "after a workout", "gym", "run",
                 "body", "drink", "tea", "coffee", "wash", "washing up", "clean the pot")),
    entry("food-left-out",
          (("rice", "pizza", "milk", "cream", "yoghurt", "yogurt", "soup", "stew", "turkey",
            "chicken", "pasta", "potato salad", "mayonnaise", "mayo", "butter", "cheese",
            "bread", "cake", "curry", "gravy", "sausages", "eggs", "quiche", "fish", "ham",
            "bacon", "food", "leftovers", "leftover", "risotto", "pie", "chilli", "lasagne",
            "meat", "steak", "steaks", "chops", "mince", "burger", "burgers", "meatballs",
            "gammon", "duck", "joint",
            "crisps", "biscuits", "chocolate", "banana", "apples", "orange", "honey", "cereal",
            "peas", "beans", "sweetcorn", "potatoes",
            "flour", "jam", "marmalade", "chutney", "loaf", "fruit", "brie", "camembert",
            "mozzarella", "feta", "stilton", "cheddar", "parmesan", "halloumi", "paneer",
            "takeaway", "takeaways", "take out food", "chinese", "kebab", "curry house",
            "mascarpone", "ricotta",
            "sandwich", "sandwiches", "wrap", "wraps", "coleslaw", "sushi", "prawn", "prawns",
            "tofu", "sauce", "formula", "baby bottle", "bottle of milk"),
          LEFT_OUT_ASK),
          _left_out,
          bias=1,
          avoid=("goes with", "go with", "going with", "goes on the side", "goes nicely",
                 "what side", "which side", "side dish", "side dishes", "sides with",
                 "serve with", "serving with", "to serve with", "to go with", "alongside",
                 "reheat", "reheating", "warm it up", "warm up", "in the fridge",
                 "how many days", "keep for", "recipe", "how do i",
                 "how to make", "make a", "order", "delivery", "dough", "toppings", "defrost",
                 "come to room temperature", "come up to room temperature",
                 "to room temperature before", "room temperature before",
                 "let it come to", "bring it to room temperature", "get it to room temperature",
                 "comes out", "come out", "came out", "coming out", "turned out", "turns out",
                 "turning out", "works out", "worked out", "figure out", "find out", "check out",
                 "point out", "sort out",
                 "spits it out", "spitting it out", "spits the food out", "spitting the food out",
                 "spits food out", "spitting food out", "spits his food out",
                 "spits her food out", "spat the food out", "spat it out",
                 "night out", "meal out", "out for drinks", "out for a drink",
                 "took me out", "taking me out", "took us out",
                 "eat out", "eating out", "take out the", "ordered from",
                 "tooth", "teeth", "milk tooth", "fell out", "wobbly",
                 "out of milk", "out of bread", "out of butter", "out of eggs", "out of cheese",
                 "run out", "ran out", "running out", "we are out", "weve run", "run out of",
                 "shopping list", "need to buy", "need to get", "forgot to buy",
                 "at home", "at work", "in the car", "on the train", "in the office",
                 "in the oven", "in the pan", "on the hob cooking", "my lunch at",
                 "left my job", "left my husband", "left my partner", "left the country",
                 "left school", "left it too late", "left in the tin", "left the lid",
                 "left over",
                 "marinate", "marinade", "marinating", "marinated",
                 "left on", "left the oven", "left the light", "left it running",
                 "out of date", "use by", "best before", "gone off", "gone bad", "expired",
                 "went off", "smells off", "how long does it last", "past its date",
                 "went white", "white", "bloom", "bloomed", "bloomy", "grey", "greyed",
                 "turned pale",
                 "carpet", "carpets", "rug", "upholstery", "curtain", "curtains", "mattress",
                 "shirt", "shirts", "jumper", "jumpers", "blouse", "trousers", "fabric",
                 "sleeve", "sleeves", "cushion", "cushions", "red wine", "white wine",
                 "coffee on", "on my shirt", "on the carpet", "out of the carpet",
                 "the sofa", "my sofa", "cream sofa", "on the sofa", "out of the sofa",
                 "ask out", "asking out", "asked out", "ask her out", "ask him out",
                 "ask them out", "ask someone out", "ask a girl out", "ask a guy out",
                 "crush",
                 "chickened out of", "chickening out of", "chicken out of",
                 "chickened out about", "chickening out about",
                 "i chickened out", "i chicken out", "i chickening out", "i keep chickening",
                 "i always chicken", "i usually chicken", "ive chickened out", "i've chickened",
                 "on a date", "first date"),
          guard=soak_but_not_left_out_or_in_the_freezer),
    entry("food-in-the-car",
          (("milk", "cream", "yoghurt", "yogurt", "formula", "bottle", "cheese", "butter",
            "chicken", "turkey", "ham", "sausages", "sausage", "bacon", "sandwich",
            "sandwiches", "wrap", "prawns", "fish", "mince", "steak",
            "eggs", "mayonnaise", "mayo", "cake", "chocolate",
            "food", "foods", "shopping", "groceries",
            "leftovers", "lunch", "snacks", "takeaway"),
           ("in the car", "in my car", "in the boot", "back seat", "on the back seat", "car boot",
            "in a hot car", "hot car", "warm car", "got warm", "went warm",
            "keep it cold", "keep food cold", "keep it cool", "keep cold", "cold in the car",
            "on the drive", "walked home", "on the way home",
            "in the van", "picnic")),
          _in_the_car,
          avoid=("cool bag", "cool box", "cooler bag", "cooler box", "cool bag", "ice pack",
                 "ice packs", "ice blocks", "freezer blocks", "picnic", "picnic box",
                 "fridge", "refrigerator", "freezer", "how does", "how do fridges", "how it works",
                 "why does a fridge", "compressor"),
          ask=("left", "leave", "leaves", "leaving", "forgot", "sat", "sitting", "kept",
               "stored", "packed", "bought", "brought",
               "how long", "how many hours", "still safe", "safe to eat",
               "got", "went", "get", "keep", "keeping", "cold", "warm"),
          bias=3,
          guard=lambda understood: not any(
              word in (understood.get("clean") or "").lower().split() for word in
              ("dog", "dogs", "puppy", "pup", "puppies", "cat", "cats", "kitten", "kittens",
               "pet", "pets"))),
    entry("marinate-the-meat",
          (("marinate", "marinade", "marinating", "marinated", "marinade for", "marinade in"),
           ("chicken", "meat", "steak", "lamb", "pork", "fish", "salmon", "tofu", "beef",
            "prawns", "turkey", "lamb chops", "chops")),
          _marinate,
          bias=8),

    entry("fridge-order",
          (("fridge", "fridge freezer", "fridges", "shelf", "shelves", "drawer", "crisper"),
           ("what goes off first", "goes off first",
            "go off first", "what should i eat first", "what should i use first",
            "what to eat first", "what to use first", "eat first", "use first", "use up first",
            "what goes where", "where in the fridge", "fridge order", "which shelf",
            "top shelf", "bottom shelf", "middle shelf", "salad drawer", "crisper",
            "how should i organise the fridge", "how do i organise my fridge",
            "how do i organise the fridge", "how do i stack the fridge",
            "what goes on which shelf"),),
          "Eat in date order first, and after that the food that is on borrowed time: fresh fish "
          "and mince within a day or two, then soft fruit, berries and salad leaves, then milk, "
          "yoghurt and cream, then hard cheese, butter and cooked leftovers. Where it sits "
          "matters as much as the order - cooked and ready-to-eat food on the top shelves, raw "
          "meat and fish on the bottom shelf in a box so nothing drips, and vegetables in the "
          "drawer. The door is the warmest part, so keep milk out of it, and the top of the door "
          "is fine for butter and condiments.",
          avoid=("gone off", "is it ok", "safe to eat", "still ok", "freezer", "freeze",
                 "frozen", "waste", "throw", "bin", "buy too much", "how long does",
                 "how long can i keep", "use by", "best before", "smell"),
          bias=2),

    entry("past-its-best",
          (PAST_IT_PRODUCE, PAST_IT_STATE, PAST_IT_ASK),
          _past_its_best,
          guard=_says_the_state,
          bias=3,
          avoid=("mouldy", "mould", "mold", "green potato", "sprouting", "sprouted", "sprouts",
                 "bread", "loaf", "baguette", "rolls", "toast", "croutons",
                 "basil", "parsley", "mint", "coriander", "cilantro", "chives", "thyme",
                 "rosemary", "herb", "herbs", "houseplant",
                 "keep for", "keeps for", "how long do", "how long does", "how long will",
                 "store", "storing", "storage", "keep them", "keep it", "last", "lasts",
                 "garden", "plant", "plants", "tree", "grow", "growing", "fertiliser",
                 "compost", "water them", "water it", "leaves on", "pot it", "repot",
                 "from going slimy", "from going soft", "from going brown", "from going limp",
                 "how do i keep", "how to keep", "how can i keep", "keep a bag", "keep them fresh",
                 "keep it fresh", "stop it going", "stop them going", "prevent", "last longer",
                 "stay fresh", "keep fresh", "make it last", "keep them from", "keep it from",
                 "why does", "why do", "what makes", "what causes",
                 "kitchen smells", "kitchen smell", "smells of", "smell of", "smells like",
                 "smell like", "stinks of", "stink of", "the house smells", "the fridge smells",
                 "too sour", "too sweet", "too salty", "too bitter", "a bit sour",
                 "sauce", "soup", "stew", "curry", "casserole", "dough", "batter", "cake",
                 "recipe", "recipes", "meal idea", "meal ideas",
                 "limp", "limper", "wilted", "wilting", "wilt", "floppy leaf", "floppy leaves",
                 "revive", "reviving", "bring it back", "bring them back", "crisp it up",
                 "crisp them up", "make it crisp", "make them crisp", "what can i do with",
                 "what to do with", "use it up", "use them up", "use up",
                 "how long", "how many minutes", "soak", "soaking", "ice water", "iced water")),
]
