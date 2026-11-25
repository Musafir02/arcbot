
from .lookup import entry

ANSWERS = ("cooking", "food-and-drink")

OUT = ("left out", "left it out", "left them out", "sat out", "out of the fridge",
       "out on the counter", "out on the side", "out on the worktop", "on the worktop",
       "left on the counter", "left on the side", "left on the table", "left on the worktop",
       "out overnight", "left overnight", "in my bag", "in my lunch bag", "in my rucksack")

ASKS = ("is it ok", "is it okay", "is it safe", "still ok", "still fine", "still safe",
        "overnight", "all night", "since this morning", "since last night", "can i eat",
        "can i still eat", "ok to eat", "safe to eat", "should i throw", "throw it away",
        "bin it", "gone off", "how long", "keep it", "reheat",
        "food", "lunch", "dinner", "supper", "tea", "meal", "meals", "leftovers", "plate",
        "takeaway", "my food", "the food", "something")

NAMED = ("chicken", "turkey", "beef", "pork", "lamb", "fish", "salmon", "prawns", "prawn",
         "ham", "mince", "sausages", "sausage", "bacon", "rice", "pasta", "milk", "cream",
         "cheese", "butter", "yoghurt", "yogurt", "egg", "eggs", "soup", "stew", "curry",
         "gravy", "cake", "bread", "sandwich", "salad", "pizza", "chips", "mayonnaise",
         "mayo", "custard", "quiche", "sushi", "beans", "peas", "potatoes", "lasagne",
         "lasagna", "casserole", "roast", "stuffing", "pate", "prawn cocktail",
         "formula", "baby bottle", "baby", "bottle", "breast milk", "breastmilk", "milk powder",
         "powdered milk")

NOT_FOOD = ("team", "group", "friends", "party", "invited", "feel", "felt", "feeling",
            "at work", "school", "playground", "chat", "wedding", "the lads", "the girls",
            "family", "excluded", "ignored", "laughed at", "mentioned", "conversation",
            "phone", "mobile", "keys", "wallet", "purse", "laptop", "charger", "book",
            "washing", "clothes", "laundry", "dog", "cat", "pet", "bin", "recycling",
            "paint", "tools", "bike", "car keys", "parcel", "post", "rubbish", "bins",
            "battery", "medicines", "tablets", "razor", "bleach", "washing up",
            "takeaway", "take away", "cooked", "cooking", "roast", "restaurant", "chinese",
            "kebab", "biryani", "doggy bag", "carry out", "ordered in", "delivery")

ENTRIES = [
    entry("left-out-clock",
          (OUT, ASKS),
          "The clock decides, not the look: two hours at room temperature is the limit, and one "
          "hour if the room is hot. Under that, box it and put it in the fridge and use it in the "
          "next day or two. Over it, bin anything with meat, fish, rice, dairy, eggs or a sauce, "
          "because the bugs that make you ill leave the taste and the smell alone and reheating "
          "does not undo it. Bread, cake, biscuits, jam and fruit are the exceptions and keep on "
          "the counter for days.",
          avoid=NAMED + NOT_FOOD,
          bias=0),
]
