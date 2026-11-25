
ANSWERS = ("cooking", "food-and-drink")

COOKED_KEEP_ASK = ("cooked", "cooked it", "leftover", "leftovers", "left over", "roast",
                   "roasted", "fried", "boiled", "reheated", "reheat", "reheating",
                   "made it", "made too much", "already cooked", "yesterday")

LEFT_OUT_WORDS = ("left out", "left it out", "sat out", "sitting out", "left in the car",
                  "left on the side", "overnight", "all night", "all day", "is it safe",
                  "safe to eat", "still ok", "still okay", "still safe")

REHEAT_AGAIN = ("twice", "two times", "again", "second time", "how many times",
                "more than once", "a third time")

FOOD_SAFETY = ("food poisoning", "poisoning", "poisoned", "food safety", "danger zone")

HOW_REHEAT = ("how do i reheat", "how to reheat", "how should i reheat", "how long do i reheat",
              "how do i warm", "how to warm", "how do i heat up", "how to heat up",
              "best way to reheat", "best way to warm", "what is the best way to reheat")

COOKED_KEEP_AVOID = LEFT_OUT_WORDS + REHEAT_AGAIN + FOOD_SAFETY + HOW_REHEAT + ("cook it", "cook them", "cook it for", "cook them for", "boil it",
                     "boil them", "bake it", "bake them", "roast it", "roast them", "fry it",
                     "fry them", "simmer it", "simmer them", "how long do i cook",
                     "how long to cook", "how long should i cook", "how long do i boil",
                     "how long to boil", "how long do i bake", "how long do i reheat it for",
                     "pressure cook",
                     "juicy", "juicier", "moist", "moister", "tender", "tenderer", "succulent",
                     "stays moist", "keep it moist", "not dry", "does not dry out",
                     "crispy", "crisp", "crispier", "crunchy", "soggy", "limp", "goes soft",
                     "gone soft", "not crispy", "wont crisp", "won't crisp")

COOKED_KEEPS = (
    (("chicken", "chicken breast", "chicken breasts", "chicken thighs", "turkey", "roast chicken"),
     "Cooked chicken or turkey keeps 3 days in the fridge in a covered box, and freezes for up to 3 "
     "months. "
     "Cool it within 2 hours of cooking, reheat it once until it is piping hot all through, and "
     "eat it cold only if it went straight into the fridge."),
    (("mince", "minced beef", "mincemeat", "bolognese", "chilli", "cottage pie", "shepherds pie"),
     "Cooked mince keeps 3 days in the fridge in a sealed box, and freezes for 2 to 3 months. "
     "Reheat it once until it is piping hot right through, and give it 2 days rather than 3 if it "
     "was in a sauce with cream in it."),
    (("sausage", "sausages", "sausage meat"),
     "Cooked sausages keep 3 to 4 days in the fridge in a covered box, and freeze for 2 months. "
     "Reheat them in a pan or the oven until they are hot right through rather than in a microwave, "
     "which leaves the middle cool."),
    (("bacon", "bacon rashers", "streaky bacon", "back bacon"),
     "Cooked bacon keeps 4 to 5 days in the fridge, wrapped or in a box, and freezes for 2 months. "
     "It is already cured, so it lasts longer than other cooked meat: reheat it in a dry pan until "
     "it sizzles, and eat it cold within 3 days."),
    (("gammon", "ham", "ham joint", "roast pork", "pork"),
     "A cooked gammon or ham joint keeps 3 to 5 days in the fridge, and sliced ham 3 days once the "
     "pack is open. Wrap it so it does not dry out, keep it away from raw meat, and freeze slices "
     "for up to 2 months."),
    (("salmon", "fish", "cod", "haddock", "trout", "prawns"),
     "Cooked fish keeps 2 days in the fridge, less than meat: box it once it has cooled, and eat it "
     "cold the next day rather than reheating it, because fish goes dry and rubbery the second "
     "time. It freezes for a month if you cooked too much."),
    (("lentils", "beans", "chickpeas", "kidney beans", "baked beans", "dhal", "dal"),
     "Cooked beans, lentils and chickpeas keep 3 days in the fridge in a covered box, and freeze "
     "for 2 months in portions. Reheat them until they are hot right through, and bin any that "
     "smell sour or have gone fizzy."),
    (("beef", "roast beef", "lamb", "roast lamb", "steak", "pork chop"),
     "Roast meat keeps 3 to 4 days in the fridge, sliced and covered, and freezes for 2 to 3 "
     "months. Rare beef is at the shorter end: 3 days. Reheat it once in gravy so it does not dry "
     "out, and eat the rest cold."),
)
