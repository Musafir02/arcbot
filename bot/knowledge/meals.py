import functools
import random
import re

from .cleaning import not_a_mark_on_a_thing
from .lookup import not_the_heat_of_an_argument as _not_an_argument
from .dishes import KIDS_IDEA, a_dish_is_already_the_plan
from .occasions import BRING_NOT_FOOD
from ..compose import fit
from ..understanding import line_as_read
from .lookup import entry, says_it_has_gone_off

ANSWERS = ("cooking", "food-and-drink")



SAID_AS = {"dhal": "a lentil dhal", "chilli": "a chilli"}


class Dish:
    __slots__ = ("name", "uses", "minutes", "diet", "how", "favourite", "said")

    def __init__(self, name, uses, minutes, diet, how):
        self.name = name
        self.said = SAID_AS.get(name, name)
        self.uses = tuple(uses)
        self.minutes = minutes
        self.diet = diet
        self.how = how
        self.favourite = name in FAVOURITES

    def __repr__(self):
        return f"<Dish {self.name}>"


FAVOURITES = ("a frittata", "tomato pasta", "chickpea curry", "dhal", "a bean stew",
              "a chicken traybake", "macaroni cheese", "a sausage traybake", "tuna pasta",
              "vegetable soup", "a potato curry", "a salmon traybake")
SHOW_OFF = ("a salmon traybake", "a chicken traybake", "mushroom risotto",
            "aubergine parmigiana", "a sausage and mash", "a cod traybake", "chilli",
            "spaghetti bolognese", "a halloumi traybake", "a turkey traybake",
            "a squash and chickpea traybake", "chicken curry")

DISHES = (
    Dish("a frittata", ("egg", "spinach"), 20, "vegetarian",
         "beat six eggs, stir in whatever vegetables you have (spinach wilted first if it is "
         "raw), cook it in an oiled ovenproof pan for 5 minutes and finish it under the grill "
         "for 8"),
    Dish("shakshuka", ("egg", "tomato", "onion"), 25, "vegetarian",
         "soften an onion with a tin of tomatoes and a pinch of cumin for 10 minutes, crack the "
         "eggs into the sauce, cover and cook 5 minutes more"),
    Dish("egg fried rice", ("egg", "rice", "pea"), 15, "vegetarian",
         "fry cold cooked rice in hot oil for 5 minutes, push it to one side, scramble two eggs "
         "in the gap, then stir it all together with soy sauce and peas"),
    Dish("an omelette", ("egg", "cheese"), 10, "vegetarian",
         "whisk two or three eggs, cook them gently in butter for 2 minutes, add grated cheese "
         "and fold it over"),
    Dish("a Spanish tortilla", ("egg", "potato", "onion"), 30, "vegetarian",
         "fry sliced potato and onion softly for 15 minutes, mix them into five beaten eggs and "
         "set it in the pan for another 10"),
    Dish("carbonara", ("pasta", "egg", "bacon", "cheese"), 20, "meat",
         "fry the bacon, cook the pasta, then toss it off the heat with beaten eggs, grated "
         "cheese and plenty of black pepper"),
    Dish("tomato pasta", ("pasta", "tomato", "garlic"), 20, "vegan",
         "fry sliced garlic in olive oil for a minute, add a tin of tomatoes and simmer 10 "
         "minutes while the pasta cooks"),
    Dish("tuna pasta", ("pasta", "tuna"), 15, "fish",
         "stir a tin of tuna through hot pasta with olive oil, lemon and capers if you have them"),
    Dish("pesto pasta", ("pasta", "pesto"), 12, "vegetarian",
         "stir pesto through hot pasta with a spoonful of the cooking water to loosen it"),
    Dish("macaroni cheese", ("pasta", "cheese", "milk"), 25, "vegetarian",
         "make a quick white sauce from butter, flour and milk, melt the cheese into it and stir "
         "it through cooked pasta"),
    Dish("courgette pasta", ("pasta", "courgette", "garlic"), 20, "vegan",
         "fry thin courgette slices with garlic for 8 minutes and toss them with pasta, lemon "
         "and black pepper"),
    Dish("broccoli pasta", ("pasta", "broccoli", "garlic"), 20, "vegetarian",
         "boil the broccoli with the pasta for the last 5 minutes, then toss it all with garlic "
         "fried in oil and a lot of pepper"),
    Dish("mushroom risotto", ("rice", "mushroom", "onion"), 30, "vegetarian",
         "soften the onion, add the rice and mushrooms, then stir in hot stock a ladle at a time "
         "for 20 minutes"),
    Dish("mushrooms on toast", ("mushroom", "bread", "garlic"), 15, "vegetarian",
         "fry the mushrooms hard in butter so they colour, add garlic at the end and pile them "
         "onto toast"),
    Dish("chickpea curry", ("chickpea", "tomato", "onion"), 25, "vegan",
         "fry an onion with curry powder, add a tin of chickpeas and a tin of tomatoes and simmer "
         "for 15 minutes"),
    Dish("dhal", ("lentil", "onion", "garlic"), 30, "vegan",
         "simmer red lentils with onion, garlic and cumin in plenty of water for 25 minutes, "
         "until soft, then salt it"),
    Dish("a bean stew", ("bean", "tomato", "onion"), 25, "vegan",
         "fry the onion, add a tin of beans, a tin of tomatoes and paprika and simmer 15 minutes"),
    Dish("chilli", ("mince", "bean", "tomato", "onion"), 40, "meat",
         "brown the mince, add onion, a tin of beans and a tin of tomatoes with chilli and cumin, "
         "and simmer it 25 minutes"),
    Dish("a veggie chilli", ("bean", "pepper", "tomato", "onion"), 25, "vegan",
         "fry a chopped pepper and onion, add beans, tomatoes and chilli powder and simmer 20 "
         "minutes; rice or a baked potato alongside"),
    Dish("a sausage traybake", ("sausage", "potato", "onion"), 45, "meat",
         "toss sausages, halved potatoes and onion wedges with oil on a tray at 200C (180C fan) "
         "for 40 minutes, turning once"),
    Dish("a chicken traybake", ("chicken", "potato", "lemon"), 40, "meat",
         "toss chicken thighs, potato chunks and lemon slices with oil at 200C (180C fan) for 40 "
         "minutes, skin side up"),
    Dish("a chicken stir-fry", ("chicken", "pepper", "noodle"), 20, "meat",
         "slice the chicken thin, fry it hot for 5 minutes with sliced peppers, then add cooked "
         "noodles and soy sauce"),
    Dish("chicken curry", ("chicken", "onion", "tomato"), 35, "meat",
         "brown the chicken, add onion and curry paste, then a tin of tomatoes, and simmer 20 "
         "minutes"),
    Dish("a salmon traybake", ("salmon", "potato", "broccoli"), 30, "fish",
         "roast the potatoes at 200C for 20 minutes, then add the salmon and broccoli with oil "
         "and lemon and give it 12 minutes more"),
    Dish("a salmon rice bowl", ("salmon", "rice", "cucumber"), 25, "fish",
         "pan-fry the salmon 4 minutes a side and flake it over rice with sliced cucumber and soy"),
    Dish("a smoked haddock fish pie", ("smoked haddock", "potato", "milk"), 40, "fish",
         "poach the haddock in milk for 5 minutes, flake it into a dish with that milk and a spoon "
         "of flour, top it with mashed potato and bake at 200C for 25 minutes"),
    Dish("a tuna salad", ("tuna", "tomato", "cucumber"), 10, "fish",
         "drain a tin of tuna into a bowl with chopped tomato and cucumber, dress it with oil, "
         "lemon and salt, and add a handful of leaves or cold pasta if you want it filling"),
    Dish("a chickpea salad", ("chickpea", "tomato", "cucumber", "lemon"), 10, "vegan",
         "toss a drained tin of chickpeas with chopped tomato and cucumber, dress it with lemon "
         "juice, olive oil and salt, and crumble cheese over it if you eat it"),
    Dish("a chicken salad", ("chicken", "lettuce", "tomato"), 15, "meat",
         "fry or griddle a chicken breast 5 minutes a side, rest it 5 minutes, then slice it over "
         "leaves and tomato with oil and lemon"),
    Dish("a prawn stir-fry", ("prawn", "noodle", "pepper"), 15, "fish",
         "fry the prawns 2 minutes, add peppers, cooked noodles and soy sauce and toss until hot"),
    Dish("a tofu stir-fry", ("tofu", "pepper", "rice"), 20, "vegan",
         "pat the tofu dry, fry it until golden, add peppers, soy and ginger, and serve it on rice"),
    Dish("a baked potato with beans", ("potato", "bean", "cheese"), 25, "vegetarian",
         "microwave the potato 8 minutes, rub it with oil and salt and crisp it in a hot oven for "
         "15, then top it with hot beans and cheese"),
    Dish("a potato curry", ("potato", "onion", "tomato"), 30, "vegan",
         "fry onion with spices, add cubed potato and tomatoes with a splash of water and simmer "
         "20 minutes"),
    Dish("a bacon and egg hash", ("potato", "bacon", "egg"), 25, "meat",
         "fry cubed cooked potato until crisp, add chopped bacon, then crack an egg in and cover "
         "the pan for 3 minutes"),
    Dish("a cheese toastie", ("bread", "cheese", "butter"), 10, "vegetarian",
         "butter the outside, fill it with cheese and cook it in a dry pan for 3 minutes a side "
         "with something heavy on top"),
    Dish("beans on toast", ("bread", "bean"), 8, "vegan",
         "warm the beans in a pan with a little oil and plenty of pepper and pour them over thick "
         "toast"),
    Dish("a quesadilla", ("tortilla", "cheese", "bean"), 10, "vegetarian",
         "fill a tortilla with cheese and beans, fold it and dry-fry it 2 minutes a side"),
    Dish("vegetable soup", ("carrot", "onion", "potato"), 30, "vegan",
         "fry the onion and carrot 5 minutes, add potato and enough stock to cover, simmer 20 "
         "minutes and blend it"),
    Dish("a leek and potato soup", ("leek", "potato", "onion"), 30, "vegetarian",
         "sweat sliced leeks and onion in butter for 8 minutes without colouring them, add cubed "
         "potato and stock to cover, simmer 20 minutes and mash it roughly"),
    Dish("lentil soup", ("lentil", "carrot", "onion"), 35, "vegan",
         "fry onion and carrot, add lentils and stock and simmer for 25 minutes"),
    Dish("pea and mint soup", ("pea", "onion"), 15, "vegan",
         "simmer frozen peas and a chopped onion in stock for 10 minutes with a handful of mint, "
         "then blend it"),
    Dish("spinach and chickpea curry", ("spinach", "chickpea", "onion", "tomato"), 25, "vegan",
         "fry an onion with curry powder, add a tin of chickpeas and a tin of tomatoes and simmer "
         "15 minutes, then stir the spinach in at the end until it wilts"),
    Dish("a halloumi traybake", ("halloumi", "potato", "pepper", "onion"), 35, "vegetarian",
         "toss cubed potato and sliced pepper in oil and roast 20 minutes at 200C (180C fan), then "
         "add thick slices of halloumi for the last 12 minutes and squeeze lemon over it"),
    Dish("cabbage with bacon", ("cabbage", "bacon"), 20, "meat",
         "fry chopped bacon until crisp, add shredded cabbage and a splash of water and cook it 8 "
         "minutes"),
    Dish("spaghetti bolognese", ("mince", "tomato", "onion", "pasta"), 30, "meat",
         "brown the mince with a chopped onion, add a tin of tomatoes and a stock cube and "
         "simmer it 20 minutes while the spaghetti cooks"),
    Dish("a sausage and mash", ("sausage", "potato", "onion"), 30, "meat",
         "boil the potatoes 15 minutes, fry or roast the sausages, then mash the potatoes with "
         "butter and make a quick onion gravy in the pan"),
    Dish("a chicken and rice", ("chicken", "rice", "onion"), 30, "meat",
         "fry strips of chicken with an onion, add a tin of tomatoes or a spoon of curry paste, "
         "then stir in cooked rice for the last 2 minutes"),
    Dish("roast veg pasta", ("pasta", "veg", "carrot", "pepper", "onion"), 30, "vegan",
         "roast chopped veg at 200C (180C fan) for 25 minutes with oil and salt and stir it "
         "through cooked pasta"),
    Dish("a bacon pasta", ("pasta", "bacon", "tomato", "onion"), 20, "meat",
         "fry the bacon with an onion in a dry pan, add a tin of tomatoes, and toss it through "
         "pasta with a splash of the cooking water"),
    Dish("mince and cabbage", ("mince", "cabbage", "onion"), 20, "meat",
         "brown the mince with a chopped onion, add shredded cabbage and a splash of water and "
         "cook it 8 minutes with a lid on"),
    Dish("a cheesy potato hash", ("potato", "egg", "cheese", "onion"), 25, "vegetarian",
         "boil the diced potato 12 minutes, fry it with an onion until it colours, then crack "
         "eggs over it and scatter cheese on top"),
    Dish("a cod traybake", ("white fish", "potato", "tomato"), 35, "fish",
         "roast potato chunks and cherry tomatoes at 200C (180C fan) for 20 minutes, then lay "
         "the cod on top with oil and lemon and give it 12 minutes more"),
    Dish("a turkey traybake", ("turkey", "potato", "onion"), 40, "meat",
         "toss turkey pieces, potato chunks and onion wedges with oil and paprika at 200C "
         "(180C fan) for 35 minutes"),
    Dish("a sweet potato curry", ("sweet potato", "chickpea", "tomato", "onion"), 30, "vegan",
         "fry onion with curry powder, add cubed sweet potato and a tin of tomatoes, simmer 20 "
         "minutes and stir in a tin of chickpeas"),
    Dish("aubergine parmigiana", ("aubergine", "tomato", "cheese"), 45, "vegetarian",
         "fry sliced aubergine in plenty of oil until soft, layer it in a dish with tomato sauce "
         "and grated cheese, and bake at 190C (170C fan) for 25 minutes"),
    Dish("a squash and chickpea traybake", ("squash", "chickpea", "onion"), 35, "vegan",
         "toss squash chunks, onion wedges and cumin with oil at 200C (180C fan) for 25 minutes, "
         "then stir in a tin of chickpeas and a squeeze of lemon"),
    Dish("a ham and potato chowder", ("bacon", "potato", "onion", "milk"), 30, "meat",
         "fry chopped ham and onion 5 minutes, add diced potato and stock to cover, simmer 15 "
         "minutes and stir in a splash of milk"),
    Dish("a baked feta pasta", ("feta", "pasta", "tomato"), 25, "vegetarian",
         "put a block of feta in a dish with halved cherry tomatoes, oil, oregano and a pinch "
         "of chilli, bake at 200C (180C fan) for 20 minutes, then mash it into the tomatoes and "
         "stir through cooked pasta"),
    Dish("a fish foil bake", ("salmon", "lemon", "potato"), 25, "fish",
         "wrap the fish in foil with lemon and butter and bake at 200C (180C fan) for 12 to 15 "
         "minutes, with boiled potatoes on the side"),
)

INGREDIENTS = {
    "egg": ("egg", "eggs"),
    "cheese": ("cheese", "cheddar", "mozzarella", "parmesan"),
    "feta": ("feta", "feta cheese"),
    "milk": ("milk", "cream"),
    "coconut milk": ("coconut milk", "tinned coconut milk", "coconut cream"),
    "oat milk": ("oat milk",),
    "soy milk": ("soy milk", "soya milk"),
    "almond milk": ("almond milk",),
    "rice milk": ("rice milk",),
    "plant milk": ("plant milk", "plant milks"),
    "condensed milk": ("condensed milk",),
    "evaporated milk": ("evaporated milk",),
    "butter bean": ("butter beans", "butter bean"),
    "butter": ("butter",),
    "pasta": ("pasta", "spaghetti", "penne", "macaroni"),
    "noodle": ("noodle", "noodles", "ramen"),
    "rice noodle": ("rice noodles", "rice noodle"),
    "rice": ("rice", "risotto"),
    "bread": ("bread", "toast", "baguette", "rolls"),
    "tortilla": ("tortilla", "tortillas", "wrap", "wraps"),
    "potato": ("potato", "potatoes", "spud", "spuds"),
    "sweet potato": ("sweet potato", "sweet potatoes"),
    "squash": ("butternut", "butternut squash", "squash", "pumpkin"),
    "tomato": ("tomato", "tomatoes", "toms", "passata", "tinned tomatoes",
               "chopped tomatoes"),
    "onion": ("onion", "onions", "shallot", "shallots"),
    "leek": ("leek", "leeks"),
    "garlic": ("garlic",),
    "pepper": ("pepper", "peppers", "capsicum"),
    "carrot": ("carrot", "carrots"),
    "courgette": ("courgette", "courgettes", "zucchini"),
    "aubergine": ("aubergine", "eggplant"),
    "broccoli": ("broccoli",),
    "cabbage": ("cabbage",),
    "pea": ("pea", "peas"),
    "bean": ("bean", "beans", "baked beans", "kidney beans", "black beans"),
    "chickpea": ("chickpea", "chickpeas", "hummus"),
    "lentil": ("lentil", "lentils", "dhal", "dal"),
    "spinach": ("spinach", "kale", "chard"),
    "mushroom": ("mushroom", "mushrooms"),
    "chicken": ("chicken",),
    "sausage": ("sausage", "sausages"),
    "mince": ("mince", "minced beef", "ground beef", "beef"),
    "bacon": ("bacon", "ham", "pancetta", "chorizo"),
    "tuna": ("tuna",),
    "salmon": ("salmon",),
    "white fish": ("cod", "haddock", "pollock", "white fish", "fish fillets", "fish"),
    "smoked haddock": ("smoked haddock", "smoked fish"),
    "turkey": ("turkey",),
    "prawn": ("prawn", "prawns", "shrimp"),
    "tofu": ("tofu",),
    "quorn": ("quorn", "quorn mince", "quorn pieces", "quorn fillets", "mycoprotein"),
    "lemon": ("lemon", "lemons", "lime", "limes"),
    "pesto": ("pesto",),
    "maple syrup": ("maple syrup",),
    "chocolate": ("chocolate", "dark chocolate", "milk chocolate", "cooking chocolate",
                  "chocolate chips"),
    "bagel": ("bagel", "bagels"),
    "cucumber": ("cucumber",),
    "lettuce": ("lettuce", "salad leaves", "leaves", "rocket"),
    "spring greens": ("spring greens", "spring green", "collard greens", "collard",
                      "greens"),
    "halloumi": ("halloumi", "paneer"),
    "veg": ("veg", "vegetables", "vegetable", "frozen veg", "frozen vegetables", "mixed veg",
            "mixed vegetables", "frozen mixed veg"),
}

IN_A_DISH = frozenset(name for _dish in DISHES for name in _dish.uses)

FISH_INGREDIENTS = frozenset(("white fish", "salmon", "tuna", "prawn"))

WORD = re.compile(r"[a-z0-9]+(?:'[a-z]+)?")

DISH_STYLE = ("curry", "soup", "stew", "stir fry", "stir-fry", "traybake", "pie", "salad",
              "roast", "risotto", "noodles", "casserole", "bake")
STYLE_WANT = ("fancy", "mood for", "feel like", "up for", "craving", "i want a", "i want some")
STYLE_CUES = {"spicy": ("curry", "chilli", "stir fry"), "hot": ("curry", "chilli", "stir fry"),
              "creamy": ("risotto", "pasta", "curry"), "cosy": ("soup", "stew", "casserole"),
              "cosy night": ("soup", "stew"), "comfort": ("soup", "stew", "pie", "macaroni"),
              "warming": ("soup", "stew", "casserole"),
              "fresh": ("salad", "stir fry"), "light": ("salad", "soup")}
CARRY_ASK = ("picnic", "picnics", "beach", "day out", "day trip", "road trip", "train journey",
             "long journey", "flight", "cool box", "coolbox", "cooler box", "flask")
CARRY_REPLIES = (
    ("Things that travel well: a frittata or a quiche cut in wedges, cold sausages or sausage "
     "rolls, cheese and oatcakes, cherry tomatoes, and fruit that survives a bag. Pack anything "
     "wet in its own box and take a bag for the rubbish."),
    ("Cold and easy to carry: a frittata cut in wedges, sausage rolls, cheese with oatcakes or "
     "bread, tomatoes and a bag of grapes. Freeze a bottle of water the night before - it keeps "
     "the food cold and then it is your drink."),
)
CHEAP_ASK = ("cheaper", "cheap", "cheapest", "budget", "afford", "save money", "less money",
             "tight month", "low on money", "money is tight", "skint", "payday", "hard up",
             "no money", "short of money", "on a tight budget",
             "student", "students", "uni", "university", "fresher", "freshers", "halls",
             "shared kitchen", "one pan")
LIGHT_ASK = ("healthy", "healthier", "healthily", "light", "lighter", "slimming", "low calorie",
             "low fat", "nutritious", "fresh", "clean eating", "balanced", "not too heavy",
             "something light")
LIGHT_SET = ("a salmon traybake", "a salmon rice bowl", "a tofu stir-fry", "a chickpea salad",
             "a chicken salad", "vegetable soup", "a leek and potato soup", "lentil soup",
             "pea and mint soup", "spinach and chickpea curry", "a chicken stir-fry",
             "a prawn stir-fry", "a fish foil bake", "a cod traybake", "roast veg pasta",
             "a squash and chickpea traybake", "a bean stew", "a chicken and rice")
SMALL_PEOPLE = ("toddler", "toddlers", "baby", "babies", "kid", "kids", "children", "child",
                "nursery", "grandchild", "grandchildren", "easter", "halloween", "christmas",
                "birthday", "bonfire night")
CHILD_AT_TABLE = ("toddler", "toddlers", "baby", "babies", "kid", "kids", "children", "child",
                  "little ones", "little one", "grandchild", "grandchildren", "family",
                  "families", "my son", "my daughter")
EVENT_WORDS = ("race", "match", "game", "training", "workout", "gym", "run", "10k", "5k",
               "marathon", "football", "rugby", "cricket", "netball", "swim", "competition",
               "tournament", "triathlon", "fight", "climb")
BEFORE_EVENT = ("before a", "before the", "before my", "before i", "morning of", "day of",
                "pre workout", "pre-workout", "fuel for", "fuelling", "fueling")
MEAL_WORD = ("dinner", "tea", "supper", "lunch", "meal", "meals", "cook", "cooking", "eat",
             "eating", "food", "hungry", "starving", "bake", "baking")

CHEAP_SET = ("egg", "potato", "bean", "chickpea", "lentil", "pasta", "rice", "onion",
             "tomato", "cheese", "cabbage", "carrot", "bread", "pea", "spinach", "cucumber",
             "lemon", "tofu", "noodle", "mushroom", "courgette", "aubergine", "squash",
             "pepper", "broccoli")
CHEAP = set(CHEAP_SET)


def cheap(item):
    return all(use in CHEAP for use in item.uses)

FOOD_WORDS = tuple(word for forms in INGREDIENTS.values() for word in forms)
FOOD_WORDS += ("meal", "meals", "dinner", "supper", "teatime", "lunch", "food", "cook",
               "cooking", "recipe", "eat", "eat something", "hungry", "kitchen", "fridge",
               "cupboard", "starving", "starved", "famished",
               "something quick", "something fast", "something easy", "something simple",
               "something filling", "something hot")
FOOD_WORDS += tuple(DISH_STYLE) + tuple(STYLE_CUES)

NO_MEAT = ("vegetarian", "veggie", "vegan", "meatless", "no meat", "without meat", "less meat",
           "cut out meat", "cut down on meat", "no meat or fish", "meat free", "meat-free")
NO_CHEESE = ("dairy", "lactose", "no cheese", "without cheese", "cheeseless")
FOOD_WORDS += tuple(NO_MEAT) + tuple(NO_CHEESE)
NO_CUE = ("no", "without", "arent", "isnt", "dont want", "dont eat", "dont like", "doesnt eat",
          "doesnt like", "sick of", "bored of", "tired of", "had enough", "not in the mood for",
          "cant eat", "cant have", "allergic to", "instead of",
          "hate", "hates", "hated", "dislike", "dislikes", "disliked", "loathe", "cant stand",
          "can't stand", "not a fan", "not a fan of", "not fussed", "not keen", "not keen on",
          "fed up of", "fed up with", "had it with",
          "wont eat", "won't eat", "will not eat", "wont touch", "won't touch",
          "out of", "ran out of", "run out of", "none left", "no more",
          "dont have", "do not have", "havent got", "have not got", "got no", "short of")
NO_GAP = ("", " any", " the", " a", " an", " some", " more", " any more", " of the",
          " of any", " any of the",
          " of", " on")

GAME_WORDS = ("game", "games", "board game", "board games", "boardgame", "boardgames",
              "puzzle", "puzzles", "jigsaw", "jigsaws", "chess", "cards", "quiz")

TECHNIQUE = ("how", "long", "safe", "time", "temperature", "temp", "defrost", "thaw", "store",
             "keep", "best way", "way to cook", "way to make", "how to",
             "reheat", "burning", "burnt", "smell", "rubbery", "sticky", "soggy", "lumpy", "raw",
             "pink", "undercooked", "ruined", "freeze", "why")

USE_UP_TECHNIQUE = tuple(word for word in TECHNIQUE if word != "how") + ("stale",)

USE_UP = (
    (("chicken", "turkey", "meat", "beef", "pork", "lamb", "ham", "joint"),
     "Shred it into fried rice, or fold it through a white sauce with pasta and bake it 20 minutes "
     "at 200C; cooked meat only needs heating through"),
    (("potato", "potatoes"),
     "Fry cold chopped potatoes with an onion until crisp, or fold them into a frittata and finish "
     "it under the grill; both take about 20 minutes"),
    (("bread", "loaf"),
     "Tear it into a salad with tomatoes, oil and salt, or blitz it into breadcrumbs and freeze "
     "them for topping a bake"),
    (("cheese",),
     "Grate it into a macaroni cheese, or make a toastie with it and a little mustard"),
)

UP_GREENS = ("spinach", "cabbage", "kale", "chard", "greens", "collard", "collards", "savoy",
             "sprout", "sprouts", "broccoli", "broccolini", "cauliflower", "romanesco",
             "kalettes", "spring green", "spring greens", "lettuce", "rocket", "cress",
             "watercress", "pea", "peas", "green bean", "green beans", "mangetout", "asparagus")
UP_ALLIUMS = ("onion", "onions", "leek", "leeks", "shallot", "shallots", "garlic",
              "spring onion", "spring onions", "red onion", "red onions")
UP_ROOTS = ("beetroot", "parsnip", "parsnips", "carrot", "carrots", "turnip", "turnips",
            "swede", "celeriac", "squash", "pumpkin", "sweet potato", "sweet potatoes",
            "potato", "potatoes", "artichoke", "artichokes", "fennel", "jerusalem artichoke",
            "jerusalem artichokes")
UP_SOFT = ("courgette", "courgettes", "zucchini", "aubergine", "aubergines", "pepper",
           "peppers", "mushroom", "mushrooms", "tomato", "tomatoes", "corn", "sweetcorn",
           "butternut", "okra", "bean", "beans")
UP_GRAINS = ("rice", "quinoa", "couscous", "bulgur", "barley", "pasta", "noodle", "noodles",
             "spaghetti", "macaroni", "lentil", "lentils", "chickpea", "chickpeas", "porridge",
             "oat", "oats")
UP_FRUIT = ("cranberry", "cranberries", "apple", "apples", "pear", "pears", "banana",
            "bananas", "berry", "berries", "raspberry", "raspberries", "strawberry",
            "strawberries", "rhubarb", "plum", "plums", "peach", "peaches", "nectarine",
            "nectarines", "mango", "pineapple", "orange", "oranges", "grapes", "cherry",
            "cherries", "apricot", "apricots", "fig", "figs", "melon")
UP_MEAT = ("chicken", "beef", "lamb", "pork", "ham", "bacon", "sausage", "sausages", "turkey",
           "duck", "mince", "steak", "liver", "chorizo", "gammon", "meat", "meatballs")
UP_FISH = ("salmon", "cod", "haddock", "tuna", "prawn", "prawns", "mackerel", "trout", "fish",
           "fishcake", "fishcakes", "sardine", "sardines", "crab", "anchovy", "anchovies")
UP_CLASSES = (
    (UP_GREENS, "butter or oil in a hot pan for 3 or 4 minutes is enough, or stir through a "
                "soup, an omelette or a pasta sauce just before you serve. Shred raw into a "
                "salad with oil and lemon if you would rather have it cold."),
    (UP_ALLIUMS, "cook slowly in butter until sweet, which takes 15 minutes and is worth it, "
                 "then stir through a soup, a gravy or a tray of roasted veg. On a pizza, a tart "
                 "or a piece of toast it is a topping on its own."),
    (UP_ROOTS, "cut into cubes and fry in a little oil until the edges crisp, or mash with "
               "potato for a bubble and squeak, or simmer into a soup. Cold in a salad with a "
               "sharp dressing is just as good."),
    (UP_SOFT, "fry in a hot pan with garlic and oil until the water is gone, stir into a pasta "
              "or a sauce, or bake under cheese."),
    (UP_GRAINS, "fry hard with an onion and whatever veg you have, loosen into a soup or a stew, "
                "or fold into a salad with oil and lemon. Heat through until piping hot, and bin "
                "it if it has sat out."),
    (UP_FRUIT, "simmer 10 minutes with a spoon of sugar and a splash of water for a compote, "
               "fold into a crumble, or spoon over yoghurt or porridge."),
    (UP_MEAT, "shred or slice into a sandwich, a salad, a fried rice or a curry, and add at the "
              "end so it only heats through. Covered in the fridge it keeps 3 days."),
    (UP_FISH, "flake cold through pasta or a salad with lemon and yoghurt, or mix into a fishcake, "
              "and don't reheat it hard or it dries out."),
)
UP_FOODS = UP_GREENS + UP_ALLIUMS + UP_ROOTS + UP_SOFT + UP_GRAINS + UP_FRUIT + UP_MEAT + UP_FISH
_UP_FOOD_SET = frozenset(UP_FOODS)


USE_DISH_WORDS = ("soup", "broth", "stew", "curry", "casserole", "salad", "pasta", "risotto",
                  "traybake", "pie", "gratin", "mash", "remoulade", "pancake", "fritter",
                  "dhal", "dal", "sauce", "compote", "crumble", "hummus", "dip", "fajita", "cake",
                  "bread", "toast", "sandwich", "omelette", "frittata", "pizza", "burger",
                  "pilaf", "snack", "crisp", "chip", "relish", "chutney", "slaw")


def _up_food(words):
    for index, word in enumerate(words):
        if word in _UP_FOOD_SET:
            return word
        if index + 1 < len(words) and " ".join(words[index:index + 2]) in _UP_FOOD_SET:
            return " ".join(words[index:index + 2])
    return None


def idea_is_a_dish(idea):
    return any(word in str(idea or "").lower() for word in USE_DISH_WORDS)


def named_food(words, understood=None):
    named = _up_food(words) or _named(understood or {})
    if isinstance(named, (list, tuple)):
        named = named[0] if named else None
    return named or None


def use_it_up(name):
    said = str(name or "").strip()
    folded = said.lower()
    for words, move in UP_CLASSES:
        if folded in words:
            return "Leftover %s: %s" % (said, move)
    for words, move in UP_CLASSES:
        if any(folded.endswith(" " + word) or folded.startswith(word + " ") for word in words):
            return "Leftover %s: %s" % (said, move)
    return ("Leftover %s: already cooked, so treat it as an ingredient - stir through a soup or "
            "a curry, fry with an onion and an egg, or eat cold in a salad with oil and vinegar."
            % said)


QUICK = ("quick", "quicker", "quickly", "fast", "faster")
BEDTIME = ("off to bed", "to bed soon", "in bed soon", "early night", "bed early", "knackered",
           "shattered", "exhausted", "up early", "early start")

HUNGRY = ("starving", "starved", "famished", "hungry", "hank marvin", "need to eat",
          "need something to eat", "something to eat", "skip lunch", "skipped lunch",
          "havent eaten", "have not eaten")

IMPRESS = ("nice", "fancy", "special", "impress", "impressive", "anniversary", "birthday",
           "date night", "romantic", "treat", "trying to cook something")

IMPRESS_ASK = ("impress", "impressing", "to impress", "make an effort", "pull out all the stops",
               "special occasion", "something special", "trying to cook something")
IMPRESS_FOR = ("for my girlfriend", "for my boyfriend", "for my partner", "for my wife",
               "for my husband", "for my mum", "for my mom", "for my dad", "for my in laws",
               "for my in-laws", "for her", "for him")
IMPRESS_WORTH = ("nice", "fancy", "special", "impressive", "impress", "treat", "birthday",
                 "anniversary", "proper", "best", "good")

NOT_A_MEAL = ("exercise", "workout", "workouts", "run", "runs", "walk", "meditate", "shower",
              "study", "clean", "sleep", "nap", "train", "commute", "boil", "bake")

ANOTHER_MEAL = ("breakfast", "brunch", "snack", "snacks", "lunch", "luncheon", "pudding",
                "dessert", "afters", "afternoon tea", "high tea", "elevenses")

NOT_FOR_ME = ("allergy", "allergic", "allergies", "nut", "nuts", "peanut", "peanuts",
              "intolerance", "intolerant", "coeliac", "celiac", "temp", "temperature")

HEALTH = ("pox", "fever", "flu", "vomiting", "diarrhoea", "diarrhea", "migraine", "nausea",
          "nauseous", "throwing up", "sore throat", "cant keep anything down", "sick bug")
NO_DAIRY = ("no dairy", "without dairy", "dairy free", "dairy-free", "lactose", "no milk",
            "without milk", "milk free", "milk-free", "cant have dairy", "cannot have dairy")

UNWELL = ("stomach", "tummy", "dodgy stomach", "bad stomach", "upset stomach", "sick", "sickness",
          "being sick", "feel sick", "feeling sick", "throwing up", "nausea", "nauseous",
          "diarrhoea", "diarrhea", "constipated", "constipation", "food poisoning", "have a cold", "got a cold",
          "a bad cold", "chest infection", "tooth", "teeth", "dentist", "wisdom tooth",
          "tooth out", "toothache", "root canal", "filling", "gums", "sore mouth",
          "mouth ulcer", "tonsils", "out of date", "use by", "past their date", "past its date",
          "past the date", "gone off", "off eggs", "still ok to eat", "still safe to eat")

SICK_OF = ("sick of", "tired of", "bored of", "bored with", "fed up with", "had enough of",
           "sick and tired")

CONDITION = ("diabetes", "diabetic", "type 1", "type 2", "blood sugar", "ibs", "irritable bowel",
             "crohns", "crohn's", "colitis", "gout", "kidney", "kidneys", "cholesterol",
             "coeliac", "celiac", "anaphyla", "allergy", "allergic", "pregnant",
             "pregnancy", "breastfeeding")

EMPTY = ("no food", "nothing in", "empty fridge", "empty cupboards", "bare cupboard",
         "nothing at home", "no shopping", "run out of food")

NOT_AN_IDEA = ("leftover", "left over", "leftovers", "spare", "use up", "using up")

HOW_TO = ("need to", "do i need", "is it safe", "still use", "can i use", "wash", "washing",
          "wrong", "normal", "matter", "cheaper", "worth", "difference", "better to",
          "how do i", "why does", "why do", "is that ok", "is that ok", "is it ok",
          "from frozen", "still frozen", "defrost", "defrosting", "thaw", "thawing")

SOUP_NAMED = ("soup", "soups", "broth", "broths")

OWN_MEAL = ("im cooking", "i'm cooking", "i am cooking", "cooking a", "cooking some",
            "already cooking", "on the hob", "in the oven", "making a", "im making",
            "i'm making", "just made")

OTHER_PEOPLE = ("only eat", "only eats", "only ate", "wont eat", "won't eat", "doesnt eat",
                "doesn't eat", "refuses to eat", "refuses")

BROKEN = ("noise", "noisy", "rattling", "broken", "broke down", "not working", "stopped working",
          "leaking", "leak", "repair", "repairs", "warranty", "engineer", "fuse", "socket",
          "smells", "smelly", "won't close", "wont close")

WHAT_GOES = ("goes with", "go with", "serve with", "goes nicely")

NOT_MY_KITCHEN = ("cat", "cats", "dog", "dogs", "kitten", "puppy", "pets", "hamster", "rabbit",
                  "called", "named", "nickname")

MEASURING = ("scales", "weigh", "weighing", "weighed", "convert", "converting", "conversion",
             "grammes", "ounces", "tablespoon", "tablespoons", "teaspoon", "teaspoons",
             "ml", "litres", "millilitres")

SLEEP = ("bed", "before bed", "bedtime", "sleep", "asleep", "awake", "waking", "insomnia")

DRINK = ("tea", "brewing", "brewed", "tea bag", "tea bags", "kettle", "mug",
         "drinking", "drinks") + SLEEP

AILING_PLANT = ("blight", "mildew", "mould", "mold", "mouldy", "moldy", "rot", "rots", "rotting",
                "rotted", "rust", "wilt", "wilting", "yellowing", "yellow leaves",
                "yellowed", "drooping", "dying", "disease", "diseased", "infected", "infection",
                "aphids", "blackfly", "whitefly", "slugs", "snails", "caterpillars",
                "not growing", "stopped growing", "flowering", "fruiting", "prune", "pruning",
                "compost", "allotment", "greenhouse", "polytunnel", "raised bed", "sowed",
                "sowing", "planted", "planting", "growing", "grow", "harvest", "crop", "crops")

NOT_A_DISH = NOT_A_MEAL + ("packed lunch", "packed lunches", "pack lunch", "packing lunch",
                           "lunchbox", "lunchboxes", "lunch box", "lunch boxes", "school lunch",
                           "bento", "picnic", "buffet", "canape",
                           "finger food", "party food")

REPAIR = ("too much salt", "much salt", "much spice", "much chilli", "much pepper", "much sugar",
          "too salty", "over salted", "oversalted", "too spicy", "too hot to eat",
          "too thin", "too thick", "too sweet", "too sour", "burnt", "burning", "caught on the",
          "sticking to the pan", "stuck to the pan", "soggy", "curdled", "split", "went wrong",
          "messed up", "ruined", "dried out", "overcooked", "undercooked", "not cooked",
          "still raw", "raw in the middle", "tastes off", "smells off", "went off")

MONEY_MATTERS = ("refund", "refunds", "refunded", "money back", "get my money",
                 "reimbursed", "reimbursement", "compensation", "compensated", "claim",
                 "claimed", "claiming", "charge", "charges", "charged", "fee", "fees",
                 "voucher", "insurance", "rebook", "rebooking", "no show", "no-show",
                 "missed", "delay", "delayed", "cancelled", "canceled", "cancellation",
                 "didnt take", "didn't take", "did not take", "didnt go", "couldnt go",
                 "could not go")

SAYING = ("what do i say", "what should i say", "what can i say", "what shall i say",
          "what do i tell", "what should i tell", "what can i tell", "what shall i tell",
          "what to say", "what to tell", "how do i say", "how should i say",
          "what do i reply", "what should i reply", "what to reply")

NOT_MINE = tuple(dict.fromkeys(
    NOT_A_DISH + NOT_AN_IDEA + OWN_MEAL + OTHER_PEOPLE + HOW_TO + WHAT_GOES + BROKEN + HEALTH
    + EMPTY + MEASURING + REPAIR + UNWELL + SAYING))

NOT_MINE_ENTRY = tuple(w for w in NOT_MINE
                       if w not in ("buffet", "canape", "canapes", "finger food", "party food",
                                    "how do i", "how to"))
NOT_MINE_OUT = tuple(w for w in NOT_MINE if w not in ("run", "runs", "out of", "ran out of"))
NOT_MINE_ASK = tuple(w for w in NOT_MINE
                     if w not in ("im cooking", "i'm cooking", "i am cooking", "cooking a",
                                  "cooking some", "already cooking",
                                  "cheaper", "worth", "afford"))
NOT_MINE_CHEAP = tuple(w for w in NOT_MINE_ASK if w not in ("cheaper",))

OPENERS = ("Try", "I'd do", "Go for", "How about", "Go with")
TIMES = ("About {n} minutes.", "Roughly {n} minutes in all.", "{n} minutes, give or take.")
TOTAL_TIMES = ("Roughly {n} minutes in all.", "About {n} minutes in all.",
               "{n} minutes from start to finish.", "Roughly {n} minutes, start to finish.")
COOK_TIME = re.compile(r"\d+\s*(?:to\s*\d+\s*)?(?:min|minute|hour|hr)")
FOLLOW_ON = ("If you'd rather have something else, {alt} takes {n} minutes.",
             "Something else that works is {alt}, at {n} minutes.")
FOLLOW_ON_NO_CHEESE = "Without the cheese, there is {alt}, at {n} minutes."


def _variant(options, understood, memory):
    turns = memory.get("turns") or []
    clean = (understood.get("clean") or "") if isinstance(understood, dict) else ""
    seed = len(turns) * 7919 + sum(ord(c) for c in clean)
    return random.Random(seed).choice(list(options))


NOT_A_MEAL_SUBJECT = ("what to wear", "wear to", "to wear", "dress code", "outfit", "dinner roll",
                      "dinner lady", "dinner jacket", "what to bring", "what should i bring",
                      "bring to a", "take to a dinner party")

DESSERT_ASK = ("dessert", "desserts", "pudding", "puddings", "afters", "something sweet",
               "sweet thing", "sweet treat", "ice cream")

MAKING_AT_HOME = ("make my own", "make our own", "making my own", "making our own", "made my own",
                  "made our own", "make it myself", "make them myself", "make it ourselves",
                  "make them ourselves", "make your own", "making your own", "from scratch")

TECHNIQUE_ASK = ("how long", "how do i", "how do you", "how to", "how many minutes",
                 "what temperature", "what temp", "how much water", "how much rice",
                 "how much pasta", "should i boil", "do i need to soak")
USE_UP_ASK = ("use up", "using up", "used up", "eat up", "eating up")

NO_HAVE = ("dont have", "don't have", "didnt have", "didn't have", "havent got",
           "haven't got", "havent any", "haven't any", "have no", "got no", "there is no",
           "theres no", "there's no")

NO_HAVE_GAP = r"(?: (?:any|a|an|the|some|more|of|that|this)){0,2}"


@functools.lru_cache(maxsize=None)
def _no_have(cue, shape):
    return re.compile(r"(?<![a-z])" + re.escape(cue) + NO_HAVE_GAP
                      + r" " + re.escape(shape) + r"(?![a-z])")


DOUBLE_NO = ("dont dislike", "do not dislike", "doesnt dislike", "does not dislike",
             "dont hate", "do not hate", "doesnt hate", "does not hate", "dont mind",
             "do not mind", "doesnt mind", "does not mind")


def _ruled_out(text):
    plain = " " + " ".join(WORD.findall(text.replace("'", ""))) + " "
    for phrase in DOUBLE_NO:
        if f" {phrase} " in plain:
            plain = plain.replace(f" {phrase} ", " ")
    out = set()
    for ingredient, forms in INGREDIENTS.items():
        for form in forms:
            if not form.isalpha() and " " not in form:
                continue
            if not form.isalpha():
                shape = form.replace("'", "")
            else:
                shape = form
            if f" {shape} " not in plain:
                continue
            for cue in NO_CUE:
                if any(f" {cue}{gap} {shape} " in plain for gap in NO_GAP):
                    out.add(ingredient)
                    break
            else:
                for cue in NO_HAVE:
                    if _no_have(cue, shape).search(plain):
                        out.add(ingredient)
                        break
    return out


def _the_fish_are_out(clean, diet=""):
    plain = " " + " ".join(WORD.findall(clean.replace("'", ""))) + " "
    for cue in NO_CUE:
        for family in ("fish", "seafood"):
            if f" {cue} {family} " in plain:
                return True
    diet = (diet or "").lower()
    return "fish" in diet or "seafood" in diet


def _is_the_ruled_out_food(word, text):
    word = word.strip().lower()
    if not word:
        return False
    for ingredient in _ruled_out(text):
        for form in INGREDIENTS.get(ingredient, ()) + (ingredient,):
            form = form.strip().lower()
            if form == word or form.startswith(word) or word.startswith(form):
                return True
    return False


def _named(understood):
    words = list(understood.get("words") or [])
    tidied = understood.get("norm_text")
    if not isinstance(tidied, str):
        tidied = " ".join(understood.get("norm") or [])
    for word in WORD.findall(tidied):
        if word not in words:
            words.append(word)
    text = " ".join(words)
    found = []
    for ingredient, forms in INGREDIENTS.items():
        phrases = [form for form in forms if not form.isalpha()]
        hit = [phrase for phrase in phrases if phrase in text]
        if hit:
            found.append(ingredient)
            for phrase in hit:
                text = text.replace(phrase, " ")
                words = [w for w in words if w not in phrase]
    for ingredient, forms in INGREDIENTS.items():
        if ingredient in found:
            continue
        if any(form in words for form in forms if form.isalpha()):
            found.append(ingredient)
    return found


def _clock(numbers):
    for number in numbers or ():
        if not isinstance(number, dict):
            continue
        if number.get("unit") not in ("minutes", "minute", "min", "mins"):
            continue
        try:
            value = int(number.get("value"))
        except (TypeError, ValueError):
            continue
        if value > 0:
            return value
    return None


_NO_MEAT_BLOCKER = ("time", "times", "rush", "money", "energy", "idea", "clue", "chance",
                    "reason", "need", "way", "point", "room", "doubt", "harm", "but")


def _no_meat(text):
    if any(cue in text for cue in NO_MEAT):
        return True
    words = [word.strip(",.!?;:") for word in text.split()]
    for cue in NO_CUE:
        cue_words = cue.split()
        width = len(cue_words)
        for start in range(len(words) - width + 1):
            same = words[start:start + width] == cue_words
            if not same and width == 1 and words[start] in ("nothing", "none", "nobody"):
                same = True
            if not same:
                continue
            after = words[start + width:start + width + 5]
            if any(word in _NO_MEAT_BLOCKER for word in after):
                continue
            if "meat" in after or "chicken" in after:
                return True
    return False


def _later(memory, understood):
    plan = memory.get("meal_plan") if isinstance(memory.get("meal_plan"), dict) else {}
    if plan.get("offered"):
        return suggest(memory, understood)
    text = " ".join(understood.get("words") or [])
    if any(word in text for word in FOOD_WORDS) or any(
            cue in text for cue in ("dinner", "tea", "supper", "lunch", "meal", "recipe",
                                    "cook", "eating", "eat", "food")):
        return suggest(memory, understood)
    return None


LUNCH_ASK = ("lunch", "lunchbox", "lunchboxes", "lunch box", "lunch boxes", "packed lunch",
             "school lunch", "lunchtime", "lunch time", "brunch")


IDEA_ASK = ("idea", "ideas", "suggest", "suggestion", "recommend", "options", "option",
            "recipes", "inspiration")


def _limits(understood, memory):
    clean = understood.get("clean") or ""
    text = " ".join(understood.get("words") or [])
    allowed, without = None, set()
    said_now = set(_named(understood))

    if _no_meat(clean):
        allowed = {"vegan", "vegetarian"}
    if "vegan" in text or any(cue in clean for cue in NO_DAIRY):
        allowed = {"vegan"}
    if "no fish" in clean or "without fish" in clean or "no seafood" in clean:
        allowed = set(allowed or {"vegan", "vegetarian", "fish"}) - {"fish"}
    if any(cue in clean for cue in NO_CHEESE):
        without.add("cheese")
    without.update(_ruled_out(clean))
    minutes = _clock(understood.get("numbers"))
    if minutes is None and ("quicker" in text or "faster" in text):
        plan_now = memory.get("meal_plan")
        was = (plan_now or {}).get("pick") if isinstance(plan_now, dict) else ""
        order = ([was] if was else []) + list(
            reversed((plan_now or {}).get("offered") or () if isinstance(plan_now, dict) else ()))
        for name in order:
            item = next((dish for dish in DISHES if dish.name == name), None)
            if item is not None:
                minutes = item.minutes - 1
                break
    if minutes is None and any(word in text for word in QUICK) and (
            memory.get("meal_plan") or any(word in text for word in FOOD_WORDS)
            or any(cue in text for cue in ("dinner", "tea", "supper", "lunch", "meal",
                                           "recipe", "eating", "cook"))):
        minutes = 20
    if minutes is None and ("half an hour" in clean or "30 minutes" in clean):
        minutes = 30
    if any(cue in clean for cue in BEDTIME):
        minutes = min(minutes or 15, 15)

    about = memory.get("user") if isinstance(memory.get("user"), dict) else {}
    diet = str(about.get("diet") or "").lower()
    if allowed is None and diet:
        if "vegan" in diet:
            allowed = {"vegan"}
        elif "vegetarian" in diet:
            allowed = {"vegan", "vegetarian"}
    if "dairy" in diet or "lactose" in diet or "cheese" in diet:
        without.add("cheese")
    if _the_fish_are_out(clean, diet):
        without.update(FISH_INGREDIENTS)
    for allergy in about.get("allergies") or ():
        name = str(allergy).lower().rstrip("s")
        if name in INGREDIENTS:
            without.add(name)

    for person in memory.get("others") or ():
        theirs = str((person or {}).get("diet") or "").lower() if isinstance(person, dict) else ""
        if not theirs:
            continue
        if "vegan" in theirs or "plant" in theirs:
            allowed = {"vegan"}
        elif "vegetarian" in theirs or _no_meat(theirs):
            if allowed is None:
                allowed = {"vegan", "vegetarian"}
        if "dairy" in theirs or "cheese" in theirs:
            without.add("cheese")
        if "fish" in theirs or "seafood" in theirs:
            without.update(("fish", "tuna", "salmon", "prawn", "cod"))

    if allowed is None or not without:
        for turn in reversed((memory.get("turns") or [])[-6:]):
            said = str((turn or {}).get("user") or "").lower() if isinstance(turn, dict) else ""
            if not said:
                continue
            if _no_meat(said) or "vegan" in said:
                if not any(cue in said for cue in IDEA_ASK):
                    if allowed is None and _no_meat(said):
                        allowed = {"vegan", "vegetarian"}
                    if "vegan" in said:
                        allowed = {"vegan"}
            if any(cue in said for cue in NO_CHEESE) or "no dairy" in said:
                without.add("cheese")
            for gone in _ruled_out(said):
                if gone not in said_now:
                    without.add(gone)

    plan = memory.get("meal_plan")
    wanted = [name for name in _named(understood) if name not in without]
    if isinstance(plan, dict) and not wanted \
            and len(memory.get("turns") or []) - plan.get("turn", 0) <= 3:
        if allowed is None and plan.get("allowed"):
            allowed = set(plan["allowed"])
        without.update(plan.get("without") or ())
        minutes = minutes if minutes is not None else plan.get("minutes")
    return allowed, without, minutes


def _fits(item, allowed, without, minutes, grace=0):
    if allowed is not None and item.diet not in allowed:
        return False
    if without and set(item.uses) & without:
        return False
    if minutes is not None and item.minutes > minutes + grace:
        return False
    return True


def _rotate(items, understood, memory):
    if not items:
        return items
    seed = len(memory.get("turns") or []) * 7919 + sum(ord(c) for c in understood.get("clean", ""))
    start = seed % len(items)
    return list(items[start:]) + list(items[:start])


GRACE = 10
HARD_CLOCK = ("under", "only", "max", "maximum", "less", "tops", "just")

STAPLE = frozenset("""
onion garlic butter milk egg cheese pasta rice bread tomato potato bean pea carrot lemon flour
oil stock herb spice pepper salt noodle tortilla butter
""".split())


def _spread(ranked):
    picks = []
    shapes = set()
    for low, high in ((0, 15), (16, 25), (26, 95)):
        fits = [item for item in ranked if low <= item.minutes <= high]
        distinct = [item for item in fits if _shape(item) not in shapes]
        for pool in (distinct, fits):
            if pool:
                chosen = [item for item in pool if item.favourite] or pool
                picks.append(chosen[0])
                shapes.add(_shape(chosen[0]))
                break
    return picks


DISH_SHAPES = ("soup", "stew", "curry", "pasta", "traybake", "salad", "stir-fry", "risotto",
               "hash", "bake", "pie", "toast", "sandwich", "omelette", "tortilla", "frittata",
               "potato", "rice", "noodles", "bolognese", "chowder", "parmigiana", "mash")


def _shape(item):
    words = item.name.replace("-", " ") + " " + item.name.replace("-", " ").replace(" ", "")
    for shape in DISH_SHAPES:
        if shape.replace(" ", "") in item.name.replace("-", " ").replace(" ", ""):
            return shape
    return ""


def _best(names, allowed, without, minutes, memory, understood):
    plan = memory.get("meal_plan")
    offered = set(plan.get("offered") or ()) if isinstance(plan, dict) else set()
    if isinstance(plan, dict) and plan.get("turn", -1) >= len(memory.get("turns") or []):
        offered = set()
    said = " ".join((understood or {}).get("words") or ())
    style = [cue for cue in DISH_STYLE if cue in said]
    for word, shapes in STYLE_CUES.items():
        if word in said:
            style += [shape for shape in shapes if shape not in style]
            style = [shape for shape in style if shape in DISH_STYLE or any(
                shape in item.name for item in DISHES)]
    named = set(names)
    words = set((understood or {}).get("words") or ())
    hard = bool(words & set(HARD_CLOCK))
    grace = GRACE if named and not hard else 0
    pool = [item for item in DISHES if _fits(item, allowed, without, minutes, grace)]
    if not pool:
        pool = [item for item in DISHES if _fits(item, allowed, without, None)] or list(DISHES)
    across = _said_about(memory, said)
    if any(cue in across for cue in CHEAP_ASK):
        thrifty = [item for item in pool if cheap(item)] or [item for item in DISHES if cheap(item)]
        if thrifty:
            pool = thrifty
    if any(cue in across for cue in LIGHT_ASK):
        light = [item for item in pool if item.name in LIGHT_SET]
        if light:
            pool = light
    if style:
        named_shape = any(cue in said for cue in DISH_STYLE)
        styled = [item for item in DISHES
                  if any(cue in item.name.replace("-", " ") for cue in style)
                  and _fits(item, allowed, without, None if named_shape else minutes, grace)]
        if styled:
            pool = styled
    if named:
        using = [item for item in pool if named & set(item.uses)]
        if not using:
            using = [item for item in DISHES if named & set(item.uses)
                     and _fits(item, allowed, without, None)]
        if using:
            pool = using
    if offered and all(item.name in offered for item in pool):
        fresh = [item for item in DISHES if item.name not in offered]
        still = [item for item in fresh if named & set(item.uses)]
        if named and fresh and not still:
            pool = [item for item in pool if named & set(item.uses)] or pool
        else:
            wider = ([item for item in fresh if named & set(item.uses) and _fits(item, allowed, without, minutes)]
                     or [item for item in fresh if named & set(item.uses)]
                     or [item for item in fresh if _fits(item, allowed, without, minutes)]
                     or fresh)
            if wider:
                pool = wider
    if not named:
        favourites = _rotate([item for item in pool if item.favourite], understood, memory)
        others = _rotate([item for item in pool if not item.favourite], understood, memory)
        order = favourites + others
        order.sort(key=lambda item: item.name in offered)
        return order

    def rank(item):
        used = len(named & set(item.uses))
        extra = set(item.uses) - named
        lead = bool(names) and names[0] in item.uses
        titled = any(word in item.name for word in names)
        return (item.name in offered, -used, not lead, len(extra - STAPLE), len(extra),
                not titled, item.minutes)

    return sorted(pool, key=rank)


UNCOUNTABLE = frozenset("""
mince beef pork lamb chicken turkey bacon ham fish salmon tuna rice pasta bread cheese milk
butter spinach broccoli cabbage kale leek garlic onion sugar flour yoghurt courgette aubergine
""".split())


def _prose(names):
    said = []
    for name in sorted(names):
        if name in UNCOUNTABLE:
            said.append(name)
        elif name in ("potato", "tomato"):
            said.append(name + "es")
        else:
            said.append(name + "s")
    if len(said) > 1:
        return ", ".join(said[:-1]) + " and " + said[-1]
    return said[0] if said else ""


def _stick(memory, names, allowed, without):
    plan = memory.get("meal_plan") if isinstance(memory.get("meal_plan"), dict) else {}
    for name in reversed(plan.get("offered") or ()):
        item = next((dish for dish in DISHES if dish.name == name), None)
        if item is not None and set(names) & set(item.uses) and _fits(item, allowed, without, None):
            return item
    return None


DAIRY_EXTRAS = (", and crumble cheese over it if you eat it",)


def _without_dairy(text, without):
    if "cheese" not in without and "milk" not in without:
        return text
    for extra in DAIRY_EXTRAS:
        text = text.replace(extra, "")
    return text


def _times(how):
    return TOTAL_TIMES if COOK_TIME.search(how or "") else TIMES


def _describe(item, understood, memory, without=()):
    turns = memory.get("turns") or []
    last = (turns[-1].get("bot") if turns else "") or ""
    openers = [option for option in OPENERS if not last.startswith(option)] or list(OPENERS)
    opener = _variant(openers, understood, memory)
    when = _variant(_times(item.how), understood, memory).format(n=item.minutes)
    how = _without_dairy(item.how, without)
    how = how[0].upper() + how[1:]
    return f"{opener} {item.said}: {how}. {when}"


def use_up(memory, understood):
    words = list(understood.get("words") or [])
    text = " ".join(words)
    said = None
    up = _up_food(words)
    for forms, how in USE_UP:
        if up is not None and up not in forms:
            continue
        hit = [form for form in forms if form in words] or [form for form in forms if form in text]
        if hit:
            said = hit[0]
            memory["meal_plan"] = {"turn": len(memory.get("turns") or []), "ingredients": [],
                                   "allowed": None, "without": [], "minutes": None,
                                   "offered": [said]}
            return f"Leftover {said}: {how[0].lower()}{how[1:]}."
    named = up or _named(understood)
    if named:
        said = named[0] if isinstance(named, list) else named
        from . import cooking
        idea = cooking.pantry_idea(said) or ""
        if any(word in idea.lower() for word in USE_DISH_WORDS):
            return None
        memory["meal_plan"] = {"turn": len(memory.get("turns") or []), "ingredients": [],
                               "allowed": None, "without": [], "minutes": None,
                               "offered": [said]}
        return use_it_up(said)
    return None


def _plan(memory, names, allowed, without, minutes, offered):
    earlier = memory.get("meal_plan") if isinstance(memory.get("meal_plan"), dict) else {}
    memory["meal_plan"] = {
        "turn": len(memory.get("turns") or []),
        "ingredients": list(names) or list(earlier.get("ingredients") or ()),
        "allowed": sorted(allowed) if allowed is not None else earlier.get("allowed"),
        "without": sorted(without),
        "minutes": minutes,
        "offered": (list(earlier.get("offered") or ()) + list(offered))[-4:],
        "pick": (list(offered) or [earlier.get("pick") or ""])[0],
    }


ASK_WORDS = ("what", "whats", "any", "dinner", "dinners", "tea",
             "supper", "supper", "lunch", "lunches", "breakfast", "meal", "meals", "food",
             "hungry", "starving", "idea", "ideas", "suggest", "suggestion",
             "recommend", "recommendation", "something", "anything", "tonight",
             "recipe", "recipes", "leftover",
             "leftovers", "use up", "eat up", "cook up", "fridge", "freezer", "cupboard",
             "pantry", "hungry", "inspiration", "options")


DIET_SAID = (("dairy free", "dairy free"), ("lactose", "lactose intolerant"),
             ("vegan", "vegan"), ("vegetarian", "vegetarian"), ("gluten free", "gluten free"),
             ("no meat", "not eating meat"), ("no fish", "not eating fish"),
             ("no dairy", "dairy free"), ("cutting out", "cutting things out"))


ACK_WORDS = ("thanks", "thank you", "thx", "cheers", "nice one", "will do", "ill try that",
             "i'll try that", "sounds good", "good idea", "great idea", "lovely", "perfect")


DIET_WORDS = ("vegetarian", "vegan", "veggie", "dairy free", "lactose", "gluten free",
              "no meat", "meat free", "meatless", "pescatarian", "pescetarian", "allergic",
              "allergy", "nut free", "nut allergy", "halal", "kosher")


ASK_CUES = ("what", "which", "anything", "any", "need", "want", "feed", "party", "guests",
            "everyone", "ideas", "idea", "suggest", "recommend", "decide", "menu", "plan",
            "help me")


ASK_IN_NEWS = ("what to cook", "what to make", "what to have", "what to eat", "what should i",
               "what can i", "ideas for", "idea for", "help me", "need something", "need a",
               "trying to work out", "trying to decide", "trying to plan", "cant decide",
               "can't decide", "any suggestions", "suggest something")


def reads_as_news(understood, clean=""):
    understood = understood if isinstance(understood, dict) else {}
    if str(understood.get("intent") or "") != "news":
        return False
    low = str(clean or understood.get("clean") or "").lower()
    return not any(cue in low for cue in ASK_IN_NEWS)


def asks_for_a_meal(understood, clean=""):
    understood = understood if isinstance(understood, dict) else {}
    intent = str(understood.get("intent") or "")
    kind = str(understood.get("kind") or "")
    if reads_as_news(understood, clean):
        return False
    if kind == "question" or intent in ("question", "request"):
        return True
    low = str(clean or understood.get("clean") or "").lower()
    return any(cue in low.split() for cue in ASK_CUES)


def says_a_diet(text):
    low = str(text or "").lower()
    return any(cue in low for cue in DIET_WORDS)


def _carry(memory, understood):
    line = str(understood.get("clean") or "").lower()
    if not any(word in line for word in ("make", "take", "bring", "pack", "packing", "food",
                                         "eat", "eating", "lunch", "idea", "ideas", "need",
                                         "snack", "snacks", "something", "anything",
                                         "for a picnic", "on a picnic", "day out",
                                         "veggie", "vegetarian", "vegan", "no meat", "gluten",
                                         "kid", "kids", "children", "child", "toddler",
                                         "people", "family", "friends")):
        return None
    if any(word in line for word in ("went to", "was at", "we had", "yesterday", "last week")):
        return None
    if any(word in line for word in ("flight", "flights", "plane", "airport", "airline",
                                     "cancelled", "canceled", "delayed", "delay", "refund",
                                     "owed", "compensation", "lighter", "luggage", "baggage",
                                     "security", "passport", "check in", "check-in")):
        if not any(word in line for word in ("food", "eat", "eating", "lunch", "snack", "snacks",
                                             "picnic", "sandwich", "meal", "meals", "drink",
                                             "drinks", "breakfast", "dinner", "packed")):
            return None
    if any(word in line for word in ("packed lunch", "lunchbox", "lunch box", "school lunch",
                                     "bento")):
        return None
    if any(word in line for word in ("flight", "flights", "plane", "airport", "airline",
                                     "security")) and any(
            word in line for word in ("can i take", "can i bring", "can we take",
                                      "can we bring", "could i take", "could i bring",
                                      "am i allowed", "are we allowed", "allowed to take",
                                      "allowed to bring", "allowed on", "100ml", "liquids")):
        return None
    reply = _variant(CARRY_REPLIES, understood, memory)
    if any(word in line for word in ("veggie", "vegetarian", "vegan", "no meat")):
        reply = reply.replace("cold sausages or sausage rolls, ", "").replace(
            "sausage rolls, ", "")
    if any(word in line for word in ("kids", "children", "child", "toddler", "little ones")):
        reply += " For small people, add something they will actually eat: breadsticks, cheese."
    return reply


def _kitchen_answer(understood):
    from . import cooking
    answer = cooking.without(understood)
    return answer if isinstance(answer, str) and answer.strip() else None


GLUTEN = ("coeliac", "celiac", "gluten", "wheat free", "no wheat", "no gluten")


def _said_about(memory, clean=""):
    said = [str(clean or "")]
    for turn in (memory.get("turns") or ())[-4:]:
        if isinstance(turn, dict) and turn.get("user"):
            said.append(str(turn["user"]).lower())
    return " ".join(said)


def _diet_said(memory, understood=None):
    said = " ".join(str((turn or {}).get("user") or "").lower()
                    for turn in (memory.get("turns") or ())[-6:] if isinstance(turn, dict))
    if isinstance(understood, dict) and understood.get("clean"):
        said += " " + str(understood["clean"]).lower()
    about = memory.get("user") if isinstance(memory.get("user"), dict) else {}
    said = (str(about.get("diet") or "").lower() + " " + said).strip()
    for cue, reads in DIET_SAID:
        if cue in said:
            return reads
    return ""


def _fresh(reply, item, memory):
    turns = memory.get("turns") or []
    last = ""
    for turn in reversed(turns):
        if isinstance(turn, dict) and turn.get("bot"):
            last = str(turn["bot"])
            break
    if not last:
        return reply
    head = re.split(r"(?<=\.)\s+", reply)[0]
    if head and head in last:
        return f"{item.said.capitalize()} takes about {item.minutes} minutes."
    return reply


CROWD_SAID = {"two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7, "eight": 8,
              "nine": 9, "ten": 10, "eleven": 11, "twelve": 12, "fifteen": 15, "twenty": 20,
              "thirty": 30}
CROWD_ASK = ("party", "buffet", "birthday", "wedding", "christening", "guests", "everyone")


def _crowd_answer(memory, understood):
    from . import cooking
    said = [str(understood.get("clean") or "")]
    for turn in (memory.get("turns") or ())[-4:]:
        if isinstance(turn, dict) and turn.get("user"):
            said.append(str(turn["user"]))
    text = " ".join(said).lower()
    text = re.sub(r"\bfor\s+\d{1,3}\s*(?:min|mins|minute|minutes|hour|hours|sec|seconds)\b",
                  " ", text)
    answer = cooking._crowd_or_any(text, cooking._excluded(text))
    return answer if isinstance(answer, str) else None


COUNT_WORDS = {2: "two", 3: "three", 4: "four", 5: "five", 6: "six", 7: "seven", 8: "eight",
               9: "nine", 10: "ten", 11: "eleven", 12: "twelve"}


def _count_word(number):
    return COUNT_WORDS.get(int(number), str(int(number)))


_AGE_SHAPE = re.compile(
    r"\b(?:\d{1,2}|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve)"
    r"(?:\s*(?:,|and|&)\s*(?:\d{1,2}|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve))?"
    r"\s*(?:years?|yrs?)\s*(?:-\s*)?olds?\b", re.I)


def _for_a_table(memory, understood):
    said = [str(understood.get("clean") or "").lower()]
    for turn in (memory.get("turns") or ())[-4:]:
        if isinstance(turn, dict) and turn.get("user"):
            said.append(str(turn["user"]).lower())
    joined = " ".join(said)
    kids_named = bool(_AGE_SHAPE.search(joined))
    text = _AGE_SHAPE.sub(" ", joined)
    counts = [int(n) for n in re.findall(
        r"\bfor\s+(\d{1,3})\b(?!\s*(?:min|mins|minute|minutes|hour|hours|sec|seconds)\b)",
        text)]
    for word, value in CROWD_SAID.items():
        if re.search(r"\bfor\s+" + word + r"\b(?!\s*(?:min|minute|hour))", text) \
                or re.search(r"\b" + word + r"\s+(?:people|of us|adults|guests|coming)\b",
                             text):
            counts.append(value)
    if any(phrase in text for phrase in CROWD_ASK):
        counts.append(6)
    if counts:
        best = max(counts)
        if kids_named and re.search(r"\badults?\b", text):
            return best + len(_AGE_SHAPE.findall(joined))
        return best
    return 0 if kids_named else 0


KITCHEN_WORDS = set(
    ["a", "an", "the", "my", "our", "some", "any", "half", "leftover", "left", "over", "frozen",
     "fresh", "tin", "tins", "can", "cans", "jar", "jars", "packet", "packets", "pack", "packs",
     "bag", "bags", "bunch", "few", "bit", "bits", "little", "of", "and", "or", "in", "on",
     "fridge", "freezer", "cupboard", "what", "can", "could", "i", "we", "you", "make", "made",
     "cook", "cooking", "do", "done", "with", "from", "use", "up", "using", "recipe", "recipes",
     "ideas", "idea", "please", "tonight", "dinner", "tea", "supper", "lunch", "meal", "meals",
     "food", "eat", "have", "got", "there", "is", "are", "only", "just", "lot", "lots", "loads",
     "plenty", "still", "also", "for", "to", "it", "this", "that", "these", "those", "one", "two",
     "three", "four", "five", "kg", "g", "grams", "oz", "lb", "big", "small", "old", "new",
     "cooked", "raw", "tinned", "dried", "spare", "extra", "again", "rest", "leftovers"])
WITH_ASK = re.compile(r"\b(?:with|using|from)\s+(.{2,60})")
RECIPE_FOR = re.compile(r"\b(?:recipe|recipes)\b(?:\s+(?:for|of|to make))?\s+(.{2,60})")
NOT_A_DISH_NAME = ("idea", "ideas", "meal", "meals", "dinner", "dinners", "tea", "supper",
                   "lunch", "tonight", "please", "pls", "plz", "quick", "easy", "cheap")


COMPANY = frozenset((
    "kid", "kids", "child", "children", "toddler", "toddlers", "baby", "babies", "teen",
    "teens", "teenager", "teenagers", "family", "families", "friend", "friends", "mate",
    "mates", "flatmate", "flatmates", "housemate", "housemates", "partner", "partners",
    "husband", "wife", "boyfriend", "girlfriend", "mum", "mums", "dad", "dads", "mother",
    "mothers", "father", "fathers", "parent", "parents", "sister", "sisters", "brother",
    "brothers", "gran", "grans", "grandma", "grandmas", "grandad", "grandads", "nan", "nans",
    "grandparent", "grandparents", "grandchild", "grandchildren", "nephew", "nephews",
    "niece", "nieces", "cousin", "cousins", "son", "sons", "daughter", "daughters", "in law",
    "in laws", "in-laws", "inlaw", "inlaws", "law", "laws", "guest", "guests", "people",
    "one", "ones", "everyone",
    "somebody", "someone", "workmate", "workmates", "colleague", "colleagues", "crowd",
    "household", "neighbours", "neighbors", "visitors", "company", "others", "them", "us",
    "we", "me", "you", "ourselves", "myself", "yourself", "anyone", "nobody"))


NOT_AN_INGREDIENT = frozenset((
    "my", "your", "his", "her", "its", "our", "their", "mine", "yours", "hers", "ours",
    "theirs", "is", "are", "was", "were", "be", "been", "being", "am", "do", "does", "did",
    "done", "should", "shall", "would", "could", "can", "will", "year", "years", "old",
    "month", "months", "week", "weeks", "day", "days", "tonight", "today", "tomorrow",
    "it", "them", "him", "we", "us", "they", "these", "those", "again", "still", "coming",
    "coming", "staying", "stay", "stays", "visiting", "visit", "over", "coming", "around",
    "here", "there", "soon", "later", "too", "also", "just", "now", "quite", "really",
    "time", "times", "hour", "hours", "minute", "minutes", "mins", "moment", "rush",
    "hurry", "while", "effort",
    "no", "not", "any", "some", "much", "many", "more", "less", "enough", "half",
    "little", "bit", "proper", "decent", "nice", "simple", "whole", "quick", "quickly",
    "fast", "easy", "something", "anything", "thing", "things"))


def _company(tail):
    return any(word in COMPANY or word.rstrip("s") in COMPANY for word in tail)


def _unknown_ingredient(clean, known):
    for match in WITH_ASK.finditer(clean):
        rest = [word for word in WORD.findall(match.group(1))
                if word not in KITCHEN_WORDS and word not in NOT_AN_INGREDIENT
                and not word.isdigit()]
        if not rest:
            return False
        if _company(rest):
            continue
        if not any(word in known or word.rstrip("s") in known or word.rstrip("es") in known
                   for word in rest):
            return True
    return False


def _unknown_dish_recipe(clean, known):
    match = RECIPE_FOR.search(clean)
    if not match:
        return False
    tail = [word for word in WORD.findall(match.group(1)) if word not in KITCHEN_WORDS
            and word not in NOT_A_DISH_NAME and not word.isdigit()]
    if not tail:
        return False
    return not any(word in known or word.rstrip("s") in known or word.rstrip("es") in known
                   for word in tail)


def unknown_food(understood):
    clean = line_as_read(understood).lower()
    known_food = set(FOOD_WORDS) | set(INGREDIENTS)
    for words in INGREDIENTS.values():
        known_food.update(words)
    if _unknown_ingredient(clean, known_food):
        return True
    return _unknown_dish_recipe(clean, known_food)


NOT_FOOD_LIMITS = ("meat", "dairy", "gluten", "wheat", "lactose", "sugar", "salt", "fat", "nuts",
                   "nut", "fish", "seafood", "shellfish", "eggs", "carbs", "carb", "calories",
                   "oil", "butter", "flour", "pasta", "rice", "potato", "potatoes")

WITHOUT_WORD = re.compile(r"\bwithout\s+(?:the\s+|any\s+|a\s+|much\s+|so\s+much\s+)?"
                          r"(?P<food>[a-z][a-z'-]{1,24})", re.I)


def _something_it_has_not_got(understood, allowed, without):
    if allowed is not None or without:
        return False
    clean = str((understood or {}).get("clean") or "").lower()
    match = WITHOUT_WORD.search(clean)
    if not match:
        return False
    word = match.group("food").lower()
    return word not in NOT_FOOD_LIMITS and word not in FOOD_WORDS \
        and word.rstrip("s") not in FOOD_WORDS


def suggest(memory, understood):
    if says_it_has_gone_off(understood.get("clean")):
        return None
    if a_dish_is_already_the_plan(str((understood or {}).get("norm_text")
                                      or (understood or {}).get("clean") or "")):
        return None
    plan = memory.get("meal_plan") if isinstance(memory.get("meal_plan"), dict) else {}
    allowed, without, minutes = _limits(understood, memory)
    names = [name for name in _named(understood) if name not in without]
    if _something_it_has_not_got(understood, allowed, without):
        return None
    if names and not any(name in IN_A_DISH for name in names):
        return None
    clean = str(understood.get("clean") or "").lower()
    if (not names and not _for_a_table(memory, understood)
            and any(cue in clean for cue in MEAL_WORD)
            and any(cue in clean for cue in CHILD_AT_TABLE)):
        return KIDS_IDEA
    kitchen = _kitchen_answer(understood)
    if kitchen:
        return kitchen
    if any(cue in clean for cue in BEFORE_EVENT) and any(
            word in clean for word in EVENT_WORDS):
        return None
    if any(cue in clean for cue in SMALL_PEOPLE) and not any(
            cue in clean for cue in MEAL_WORD):
        return None
    if any(cue in clean for cue in NOT_A_MEAL_SUBJECT):
        return None
    if any(cue in clean for cue in DESSERT_ASK):
        return None
    if any(cue in clean for cue in TECHNIQUE_ASK) and not any(
            cue in clean for cue in USE_UP_ASK):
        return None
    if any(cue in clean for cue in REPAIR):
        return None
    if any(cue in clean for cue in MAKING_AT_HOME):
        return None
    if any(cue in clean for cue in OTHER_PEOPLE):
        return None
    if any(cue in clean for cue in UNWELL) and not any(
            cue in clean for cue in SICK_OF):
        return None
    if unknown_food(understood):
        return None
    if any(cue in _said_about(memory, clean) for cue in GLUTEN + CONDITION):
        return None
    asked = any(word in clean for word in ASK_WORDS)
    impress = any(cue in clean for cue in IMPRESS)
    impress_ask = (any(cue in clean for cue in IMPRESS_ASK)
                   or (any(cue in clean for cue in IMPRESS_FOR)
                       and any(cue in clean for cue in IMPRESS_WORTH)))
    news = reads_as_news(understood, clean)
    hungry = any(cue in clean for cue in HUNGRY)
    fancying_a_shape = (any(cue in clean for cue in DISH_STYLE)
                        or any(cue in clean for cue in STYLE_CUES))
    wanting = any(cue in clean for cue in STYLE_WANT) and fancying_a_shape
    out_of = bool(_ruled_out(clean)) and bool(plan.get("offered"))
    if news and minutes is None and not names and not plan.get("ingredients") and not hungry \
            and not wanting and not out_of and not impress_ask:
        return None
    limit_follow = allowed is not None and bool(plan.get("offered"))
    if not (names or plan.get("ingredients") or minutes is not None or asked or limit_follow
            or wanting or out_of or impress_ask):
        return None
    if not names and str(understood.get("kind") or "") == "thanks":
        return None
    if (_for_a_table(memory, understood) >= 6 and asks_for_a_meal(understood, clean)
            and not says_a_diet(clean)):
        crowd = _crowd_answer(memory, understood)
        if crowd:
            return crowd
    if any(cue in clean for cue in LUNCH_ASK):
        return None
    if not names and WITH_ASK.search(clean):
        asked_for = [word for word in WORD.findall(WITH_ASK.search(clean).group(1))
                     if word not in KITCHEN_WORDS and word not in NOT_AN_INGREDIENT
                     and not word.isdigit()]
        known_here = {form for forms in INGREDIENTS.values() for form in forms}
        if asked_for and not _company(asked_for) and not any(
                word in known_here or word.rstrip("s") in known_here for word in asked_for):
            return None
    carried = not names
    names = names or [name for name in plan.get("ingredients") or () if name not in without]
    if carried and names and (any(cue in clean for cue in DISH_STYLE)
                              or any(cue in clean for cue in STYLE_CUES)):
        names = []
    ruled_now = _ruled_out(str(understood.get("clean") or ""))
    off_limits = [name for name in _named(understood) if name not in ruled_now
                  and (name in without
                       or (allowed is not None
                           and not any(name in dish.uses and dish.diet in allowed
                                       for dish in DISHES)))]
    names = [name for name in names if name not in off_limits]
    if off_limits and not names:
        pick = _best([], allowed, without, minutes, memory, understood)[0]
        _plan(memory, [], allowed, without, minutes, [pick.name])
        reason = _diet_said(memory)
        lead = (f"Since you are {reason}, I'd leave that out" if reason
                else "I'd leave that out")
        return (f"{lead} and do {pick.said} ({pick.minutes} minutes): {pick.how}.")
    ranked = _best(names, allowed, without, minutes, memory, understood)
    offered = list(plan.get("offered") or ())
    fresh = [dish for dish in ranked if dish.name not in offered]
    if not fresh and names and minutes is not None:
        best = ranked[0]
        _plan(memory, names, allowed, without, minutes, [best.name])
        return (f"{best.said.capitalize()} is the quickest I know with {_prose(names)}, at "
                f"{best.minutes} minutes; that is every dish I have for them.")
    ranked = fresh or ranked
    if impress and not names:
        slower = [dish for dish in ranked if dish.minutes >= 30]
        ranked = slower or ranked
        shown = [dish for dish in ranked if dish.name in SHOW_OFF]
        ranked = shown or ranked
    first = ranked[0]
    if names and minutes is not None and (
            not (set(first.uses) & set(names)) or first.minutes > minutes + GRACE):
        stick = _stick(memory, names, allowed, without)
        if stick is not None:
            how = stick.how[0].upper() + stick.how[1:]
            when = _variant(_times(stick.how), understood, memory).format(n=stick.minutes)
            _plan(memory, names, allowed, without, minutes, [stick.name])
            return (f"{stick.said.capitalize()} is still the quickest I know with "
                    f"{_prose(names)}: {stick.how}. {when}")
    second = ranked[1] if len(ranked) > 1 else None
    if not names and not without and allowed is None and minutes is None and not impress:
        picks = _spread(ranked)
        if len(picks) >= 2:
            names_offered = [item.name for item in picks]
            _plan(memory, names, allowed, without, minutes, names_offered)
            said = ", ".join(f"{item.said} in {item.minutes}" for item in picks[:-1])
            last = picks[-1]
            said_words = " ".join(understood.get("words") or [])
            thrifty = any(cue in _said_about(memory, said_words) for cue in CHEAP_ASK)
            eaters = _for_a_table(memory, understood)
            if thrifty and 2 <= eaters <= 12:
                opener = f"Cheap, and enough for {_count_word(eaters)}:"
            elif thrifty:
                opener = "Cheap:"
            else:
                opener = "Quick:"
            if fit.wanted(memory) == "pick" and not thrifty:
                one, rest = picks[0], picks[1:]
                others = "".join(f", or {item.said} in {item.minutes}" for item in rest)
                return (f"Here's my pick: {one.said} in {one.minutes} minutes{others}. "
                        "Tell me what is in the fridge and I will narrow it down.")
            return (f"{opener} {said}, or {last.said} if you have {last.minutes} minutes. Tell "
                    f"me what is in the fridge and I will pick properly.")
    if not names and second is not None:
        _plan(memory, names, allowed, without, minutes, [first.name, second.name])
        if second.minutes < first.minutes - GRACE:
            tail = f"If you want something quicker, {second.said} takes {second.minutes} minutes."
        elif abs(second.minutes - first.minutes) <= GRACE:
            tail = f"Something else that works is {second.said}."
        else:
            tail = f"Something else that works is {second.said}, at {second.minutes} minutes."
        return (f"I'd do {first.said} ({first.minutes} minutes): {first.how}. " + tail)
    reply = _describe(first, understood, memory, without)
    shared = len(set(second.uses) & set(names)) if second is not None else 0
    if (second is not None and names and shared >= min(2, len(names))
            and second.minutes <= max(25, first.minutes + 10)):
        options = FOLLOW_ON
        if "cheese" in without and "cheese" not in second.uses:
            options = FOLLOW_ON + (FOLLOW_ON_NO_CHEESE,)
        if abs(second.minutes - first.minutes) <= GRACE:
            alt = _variant(("Something else that works is {alt}.",
                            "There is {alt} as well."), understood, memory)
            alt = alt.format(alt=second.said)
        else:
            alt = _variant(options, understood, memory).format(alt=second.said, n=second.minutes)
        reply = _fresh(f"{reply} {alt}", first, memory)
    _plan(memory, names, allowed, without, minutes,
          [first.name] + ([second.name] if second else []))
    return _fresh(reply, first, memory)


TAKEOUT_PICKS = (
    (("pizza place", "pizza shop", "pizza parlour", "pizza parlor", "pizza", "pizzas",
      "dominos", "domino's"),
     "One pizza each and a garlic bread to share: a 12-inch is one hungry person and a 9-inch a "
     "light one, so a 12-inch between two plus a side is the cheaper way to feed a pair. A plain "
     "margherita and one with a topping beats two fully loaded ones, which are the ones left "
     "half eaten."),
    (("bakery", "bakers", "baker", "patisserie", "bakery shop"),
     "Buy the loaf that is still warm and one pastry to eat before you get home: a sourdough or a "
     "tin loaf keeps two days on the board and a week sliced in the freezer, and a cheese twist or "
     "a croissant is what a bakery is for. Ask which loaf is today's rather than yesterday's - it "
     "is the one question they are always happy to answer."),
    (("sandwich shop", "deli", "deli counter", "subway", "baguette shop", "sandwich bar"),
     "The filling that is made fresh, in a baguette or a sub rather than sliced bread, and ask for "
     "the salad on the side if it has to travel back to a desk: wet salad in the sandwich is what "
     "makes it collapse. A hot filling - meatballs, a toastie, a chicken escalope - is the one "
     "worth ordering out, because it is the one that will not be as good made at home."),
)
TAKEOUT_PLACES = tuple(name for names, _ in TAKEOUT_PICKS for name in names)

TAKEOUT_ASK = ("what", "whats", "what is", "what are", "nice", "good", "best", "better",
               "recommend", "order", "get", "have", "should i", "should we", "do i",
               "do we", "worth", "idea", "ideas",
               "how many")


def _takeout_pick(memory, understood):
    clean = str((understood or {}).get("clean") or "").lower()
    best, longest = None, -1
    for names, reply in TAKEOUT_PICKS:
        for name in names:
            if len(name) > longest and re.search(r"\b" + re.escape(name) + r"\b", clean):
                best, longest = reply, len(name)
    return best


def _counters_named(clean):
    rows = set()
    for index, (names, _) in enumerate(TAKEOUT_PICKS):
        for name in names:
            if re.search(r"\b" + re.escape(name) + r"\b", clean):
                rows.add(index)
                break
    return rows


DEFINITION_SHAPE = re.compile(r"\bwhat(?:'s| is| are|s)?\s+(?:a|an|the)\s+([a-z']+)")
ASKING_WORDS = {"good", "great", "nice", "best", "better", "cheap", "cheapest", "decent",
                "safe", "healthy", "worth", "solid", "vegetarian", "vegan"}


def _one_counter(understood):
    clean = str((understood or {}).get("clean") or "").lower()
    if re.match(r"^(?:is|are|was|were)\b", clean):
        return False
    shape = DEFINITION_SHAPE.search(clean)
    if shape and shape.group(1) not in ASKING_WORDS:
        return False
    return len(_counters_named(clean)) <= 1


SPOILT_FOOD = ("mouldy", "mould", "moldy", "mold", "blue spots", "green spots", "white spots",
               "black spots", "spots", "speckled", "fluff", "fluffy", "fuzzy", "furry", "fur",
               "green bits", "white bits", "blue bits", "smells", "smelly", "smelt", "stinks",
               "gone off", "went off", "going off", "slimy", "sour", "rancid", "stale",
               "fizzy", "curdled", "separated", "went bad", "gone bad", "rotten", "off it")

def _not_a_mark_and_not_a_row(understood):
    return not_a_mark_on_a_thing(understood) and _not_an_argument(understood)


ENTRIES = [
    entry("meal-hurry",
          (("need something", "something on the table", "on the table", "get dinner on",
            "dinner on the table", "feed the kids", "something fast"),
           ("minutes", "minute", "mins", "min", "quick", "quickly", "fast", "hurry", "now",
            "late", "knackered", "shattered", "starving", "hungry")),
          suggest, bias=-1,
          avoid=("sleep", "bed", "tired out", "go to bed", "nap", "breath", "chest", "pain",
                 "hurt", "doctor", "gp", "hospital", "panic", "anxious", "worried")
                + NOT_A_DISH + HOW_TO + MEASURING + DRINK + NOT_MY_KITCHEN),
    entry("meal-tonight", (("tonight", "supper", "teatime", "what should i cook",
                            "what can i cook", "what should i make", "what can i make",
                            "what can i eat", "what should i eat", "what to eat", "whats for",
                            "what can i have", "what should i have", "what to have",
                            "what can we have", "what shall i have", "what can i make for",
                            "whats to eat", "what is for", "what would you cook",
                            "what do i eat", "what do i cook", "what shall i eat",
                            "impress", "impressing", "to impress", "in laws", "in-laws",
                            "guests", "guest", "dinner party", "special dinner"),
                           ("impress", "impressing", "impressive", "in laws", "in-laws",
                            "guests", "guest", "special dinner", "made an effort",
                            "looks impressive", "look impressive", "looks like effort"),
                           FOOD_WORDS + ("impress", "impressing", "in laws", "in-laws",
                                         "guests", "guest", "fancy", "special")), suggest,
          bias=-1,
          avoid=("long", "time", "temperature", "oven", "safe", "defrost", "thaw", "reheat",
                 "store", "keep", "burnt", "burning", "smell", "gone", "off",
                 "dairy", "gluten", "wheat", "lactose", "vegan", "vegetarian", "vegetarians",
                 "allergic", "allergy", "coeliac", "celiac", "intolerant",
                 "doesnt eat", "does not eat", "can not eat", "cant eat", "can not have",
                 "cant have",
                 "hardly eats", "hardly eat", "barely eats", "barely eat", "wont eat",
                 "won't eat", "stopped eating", "not eating", "isnt eating", "isn't eating",
                 "no appetite", "lost his appetite", "lost her appetite", "off her food",
                 "off his food", "gone off her food", "gone off his food", "not hungry",
                 ) + UNWELL
                + OWN_MEAL + OTHER_PEOPLE + NOT_A_DISH + NOT_AN_IDEA + NOT_MY_KITCHEN + MEASURING
                + DRINK + ANOTHER_MEAL
                + SAYING),
    entry("meal-ideas-anything", (("idea", "ideas", "suggest", "suggestion", "suggestions",
                                   "inspiration",
                          "recommend", "recommendation", "options", "something", "quick"),
                         FOOD_WORDS), suggest,
          bias=-1,
          avoid=("book", "books", "film", "films", "movie", "podcast", "album", "gift", "present",
                 "name", "poison", "read", "watch", "tv", "show", "series", "surname", "word",
                 "card", "cards",
                 "tub", "bottle", "bath", "yoga", "tap", "weather", "radiator", "shower")
                 + OWN_MEAL + OTHER_PEOPLE + NOT_A_DISH + NOT_AN_IDEA + NOT_MY_KITCHEN + MEASURING
                 + DRINK + HOW_TO + BROKEN + HEALTH + EMPTY,
          ask=("idea", "ideas", "suggest", "recommend", "option", "options", "inspiration",
               "for dinner", "for tea", "for lunch", "for supper", "to cook", "to make",
               "to eat", "something with", "something quick", "fancy", "hungry", "starving",
               "dinner", "tea", "supper", "lunch", "meal", "cook", "make")),
    entry("meal-with", (FOOD_WORDS, ("make", "cook", "should i cook", "should i make",
                                     "can i cook", "can i make", "shall i cook", "shall i make")),
          suggest, bias=-1,
          avoid=TECHNIQUE + OWN_MEAL + OTHER_PEOPLE + NOT_A_DISH + NOT_AN_IDEA + NOT_FOR_ME + HEALTH
                + EMPTY + NOT_MY_KITCHEN + MEASURING + DRINK + HOW_TO + WHAT_GOES + BROKEN
                + SOUP_NAMED),
    entry("meal-haves", (FOOD_WORDS + ("what else can i do with", "what else can i make with",
                                       "what else can i cook with", "what else with",
                                       "something else to do with", "other ideas for",
                                       "any other ideas"), ("have", "has", "got", "only", "pack",
                                      "packs", "packet", "tin", "tins", "bag", "bags", "bunch",
                                      "leftover", "leftovers", "left over", "half a", "few",
                                      "else", "other")), suggest, bias=-1,
          avoid=OWN_MEAL + OTHER_PEOPLE + NOT_A_DISH + NOT_AN_IDEA + NOT_FOR_ME + HEALTH + EMPTY
                + NOT_MY_KITCHEN + MEASURING + DRINK + HOW_TO + WHAT_GOES + BROKEN + AILING_PLANT
                + SPOILT_FOOD
                + SOUP_NAMED
                + ("how",),
          guard=_not_a_mark_and_not_a_row),
    entry("meal-limit", (("without", "no", "minus", "skip", "vegetarian", "veggie", "vegan"),
                         ("meat", "cheese", "dairy", "fish", "pork", "chicken", "milk", "gluten")),
          suggest, bias=-1, avoid=HEALTH + EMPTY + NOT_MY_KITCHEN + MEASURING),
    entry("meal-quick", (("quick", "fast"), ("minute", "minutes", "min", "mins", "time")),
          suggest, bias=-1, avoid=OWN_MEAL + OTHER_PEOPLE + NOT_A_DISH + NOT_AN_IDEA + NOT_MY_KITCHEN + MEASURING
          + DRINK + HOW_TO + BROKEN + HEALTH + EMPTY),
    entry("meal-clock", (("minute", "minutes", "min", "mins", "hour", "hours", "half an hour"),
                         ("dinner", "supper", "tea", "eat", "eating", "cook", "cooking", "table",
                          "food", "meal", "lunch", "breakfast", "hungry")),
          suggest, bias=-1, avoid=OWN_MEAL + OTHER_PEOPLE + NOT_A_DISH + NOT_AN_IDEA + NOT_MY_KITCHEN + MEASURING
          + DRINK + HOW_TO + BROKEN + HEALTH + EMPTY + ("been", "how", "long", "oven", "boil", "bake")),
    entry("meal-hurry-quick", (("quick", "quicker", "fast", "hurry", "hurry up", "starving"),
                               ("please", "something", "idea", "one", "dinner", "food", "meal")),
          suggest, bias=-1, avoid=OWN_MEAL + OTHER_PEOPLE + NOT_A_DISH + NOT_AN_IDEA + NOT_MY_KITCHEN + MEASURING
          + DRINK + HOW_TO + BROKEN + HEALTH + EMPTY + ("walk", "chat")),
    entry("meal-more", (("quicker", "faster", "different", "another", "other", "instead",
                         "else"),
                        ("something", "idea", "ideas", "option", "options", "meal", "dinner",
                         "dish")),
          suggest, bias=-1, avoid=OWN_MEAL + OTHER_PEOPLE + NOT_A_DISH + MEASURING + HOW_TO + BROKEN + HEALTH + EMPTY,
          ask=FOOD_WORDS + ("dinner", "tea", "meal", "supper", "food", "eat", "tonight", "cook",
                            "cooking", "quick", "quicker", "faster", "hungry")),
    entry("meal-use-up", (("leftover", "left over", "leftovers", "spare", "use up", "using up",
                          "rest of"),
                          ("turkey", "meat", "beef", "pork", "lamb", "ham", "potato",
                           "potatoes", "vegetables", "veg", "greens", "cabbage", "broccoli",
                           "carrots", "bread", "loaf", "cheese", "joint")),
          use_up, bias=1, avoid=USE_UP_TECHNIQUE),
    entry("meal-tea", (("tea", "teatime", "tea time"),
                       ("for tea", "make", "cook", "shall", "should", "whats", "what can i",
                        "ideas", "idea", "quick", "something", "tonight", "supper", "cheap",
                        "easy", "hurry", "starving")),
          suggest, bias=-1,
          avoid=TECHNIQUE + OWN_MEAL + OTHER_PEOPLE + NOT_A_DISH + NOT_AN_IDEA + NOT_MY_KITCHEN
          + MEASURING + HOW_TO + BROKEN + HEALTH + EMPTY
                + ("brew", "brewing", "steep", "tea bag", "tea bags", "green tea", "black tea",
                   "cup of tea", "cup of", "mug", "kettle", "herbal", "chamomile", "peppermint",
                   "drink", "drinking", "cold", "desk", "caffeine", "sugar") + SLEEP),
    entry("meal-diet-again", (("something", "anything", "and", "make it", "make", "instead"),
                              ("vegetarian", "vegan", "meat free", "meat-free", "meatless")),
          _later, bias=-1,
          avoid=NOT_FOR_ME + HEALTH + EMPTY + NOT_MY_KITCHEN + MEASURING + DRINK + HOW_TO
                + WHAT_GOES + NOT_AN_IDEA),
    entry("meal-cheaper", (("cheaper", "cheap", "cheapest", "budget", "afford", "save money",
                            "less money", "money is tight"),
                           ("something", "and", "dinner", "tonight", "meal", "idea", "ideas",
                            "make", "cook", "what", "any", "else")),
          _later, bias=-1,
          avoid=NOT_MINE_CHEAP + TECHNIQUE + HEALTH + WHAT_GOES + MEASURING
                + ("insure", "insurance", "insured", "car insurance", "policy", "premium",
                   "third party", "no claims", "mot")),
    entry("meal-out-of", (("out of", "ran out of", "run out of", "none left", "no more"),
                          FOOD_WORDS),
          suggest, bias=-1,
          avoid=NOT_MINE_OUT + TECHNIQUE + HOW_TO + HEALTH + WHAT_GOES + MEASURING
                + ("left out", "out of the fridge", "out of the freezer", "all night",
                   "overnight", "two hours", "safe to eat", "gone off")),
    entry("meal-style", (("what", "whats", "any", "good", "nice", "fancy", "fancy a", "i fancy",
                          "feel like", "up for", "want", "mood", "the mood", "craving", "do",
                          "ideas", "idea", "suggest",
                          "quick", "easy", "best", "make", "cook", "having"),
                         DISH_STYLE),
          suggest, bias=-1,
          avoid=NOT_MINE + TECHNIQUE + HOW_TO + HEALTH + DRINK + SLEEP + WHAT_GOES + MEASURING),
    entry("takeaway-choice",
          (("takeaway", "takeaways", "take away", "chippy", "chip shop", "chinese", "indian",
            "kebab", "kebabs", "thai", "pizza night", "delivery", "deliveroo", "just eat",
            "curry house", "chicken shop"),
           ("should we get", "shall we get", "what should we get", "what shall we get",
            "what should i get", "what shall i get", "which", "which one", "cant decide",
            "can't decide", "decide", "choose", "any ideas", "ideas", "idea", "recommend",
            "what do you think", "or", "we always get", "same takeaway", "same old", "bored of",
            "sick of", "the kids", "kids want", "something different", "not the usual")),
          "Fish and chips feeds a group for the least money and nobody argues about it. If tastes "
          "differ, Indian beats Chinese: more vegetarian mains, and the sides stretch, so two "
          "mains with one rice and one bread feeds three. With a fussy child or someone veggie, a "
          "Chinese with plain rice and a separate veg dish keeps everyone fed. And if it is the "
          "same order every week, add one dish you have never had rather than swapping the whole "
          "thing - that is how you find the next usual.",
          avoid=("calorie", "calories", "healthy", "healthier", "diet", "slimming", "lose weight",
                 "how do i make", "make at home", "recipe", "cook it", "how do i cook", "freeze",
                 "freezing", "reheat", "left over", "leftover", "food poisoning", "hygiene",
                 "arrived cold", "wrong order", "forgot", "missing", "refund", "complain",
                 "complaint", "allergy", "allergic", "gluten", "price", "cheaper", "cost",
                 "spicy", "mild", "heat", "paste", "powder", "sauce", "spice", "spices",
                 "ingredient", "ingredients", "marinade")),
    entry("meal-for-one", (("cooking", "cook", "dinner", "tonight", "meal", "supper"),
                           ("for one", "for myself", "just me", "on my own", "by myself")),
          suggest, bias=-1,
          avoid=NOT_MINE_ASK + TECHNIQUE + DRINK + SLEEP + HEALTH + HOW_TO
                + GAME_WORDS),
    entry("meal-for-two", (("cooking", "cook", "dinner", "tonight", "meal", "supper", "date night",
                            "date-night", "anniversary", "nice", "fancy", "special", "treat",
                            "impress",
                            "valentines", "valentine", "valentine's", "valentines day"),
                           ("for two", "for 2", "for three", "for 3", "for four", "for 4",
                            "for five", "for 5", "for the two of us", "date night", "date-night",
                            "anniversary", "romantic", "looks nice", "look nice", "to impress",
                            "for my girlfriend", "for my boyfriend", "for my partner",
                            "for my wife", "for my husband", "for her", "for him",
                            "for my mum", "for my mom", "for my dad", "to say sorry",
                            "valentines", "valentine", "valentine's", "valentines day",
                            "thing to cook", "something to cook", "nice thing to cook",
                            "something nice to cook", "nice meal", "nice dinner")),
          suggest, bias=-1,
          avoid=NOT_MINE_ASK + TECHNIQUE + DRINK + SLEEP + HEALTH + HOW_TO + GAME_WORDS + (
              "present", "presents", "gift", "gifts", "voucher",
              "buy him", "buy her", "get him", "get her", "what should i get",
              "what can i get", "what to get")),
    entry("meal-carry", (CARRY_ASK,
                         ("something", "anything", "make", "take", "bring", "pack",
                          "packing", "food", "eat", "eating", "lunch", "ideas", "idea",
                          "snack", "snacks", "family", "friends", "kids", "children",
                          "toddler", "veggie", "vegetarian", "vegan")),
          _carry, bias=-1,
          ask=("something", "anything", "make", "take", "bring", "pack", "packing", "food",
               "eat", "eating", "eaten", "lunch", "lunches", "lunchbox", "lunchboxes",
               "picnic", "picnics", "flask", "cool box", "coolbox", "cooler box", "drink",
               "drinks", "snack", "snacks", "ideas", "idea", "breakfast", "supper",
               "dinner", "tea", "hungry"),
          avoid=tuple(word for word in NOT_MINE if word not in ("picnic", "picnics"))
                + TECHNIQUE + HOW_TO + HEALTH + SLEEP + DRINK + WHAT_GOES + MEASURING
                + MONEY_MATTERS
                + ("eat out", "eating out", "anywhere to eat", "anywhere good to eat",
                   "anywhere nice to eat", "somewhere to eat", "place to eat", "places to eat",
                   "good place to eat", "restaurant", "restaurants", "cafe", "pub lunch")
                + ("airport", "airports", "security", "hand luggage", "carry on", "carry-on",
                   "cabin bag", "100ml", "liquids")
                + tuple(word for word in BRING_NOT_FOOD
                        if "dog" in word or "cat" in word)),
    entry("meal-faster", (("quick", "quicker", "faster", "fast", "soon"),
                          ("and", "please", "make it", "make", "something")),
          _later, bias=-1,
          avoid=NOT_FOR_ME + HEALTH + EMPTY + NOT_MY_KITCHEN + MEASURING + DRINK + HOW_TO
                + WHAT_GOES + NOT_AN_IDEA + SLEEP),
    entry("meal-limit-only", (("less", "no", "without", "only", "instead", "cut down",
                               "cut out", "cutting down", "cutting out", "reduce", "minus",
                               "skip", "quick", "faster", "half an hour"),
                              ("meat", "dairy", "cheese", "fish", "pasta", "rice",
                               "minutes", "minute", "hour", "gluten", "sugar")),
          suggest, bias=-1, ask=("what", "shall", "should", "can i", "could i", "idea", "ideas",
                        "suggest", "recommend", "dinner", "tea", "supper", "lunch", "meal",
                        "cook", "make", "tonight", "quick", "fast", "hurry", "something",
                        "instead", "please", "starving", "hungry"),
          avoid=OWN_MEAL + OTHER_PEOPLE + NOT_A_DISH + MEASURING + HOW_TO + BROKEN + HEALTH + EMPTY),
    entry("pick-at-the-counter", (TAKEOUT_PLACES, TAKEOUT_ASK),
          _takeout_pick, bias=1, guard=_one_counter,
          avoid=("calorie", "calories", "healthy", "healthier", "diet", "slimming",
                 "lose weight", "nutrition", "how many calories", "how many kcal",
                 "how many carbs", "how much", "price", "cheaper",
                 "cost", "expensive", "cheapest", "deal", "voucher", "discount",
                 "open", "opening", "closing", "closed", "late", "near me", "nearby",
                 "where is", "nearest", "deliver to", "allergy", "allergic", "gluten",
                 "vegetarian", "vegan", "halal", "hygiene", "food poisoning", "refund",
                 "wrong order", "missing", "arrived cold", "complain", "complaint",
                 "how do i make", "make at home", "at home", "recipe", "cook it",
                 "how do i cook", "spicy", "mild", "heat", "paste", "powder", "sauce",
                 "spice", "spices", "marinade", "ingredient", "ingredients", "freeze",
                 "freezing", "reheat", "left over", "leftover", "work", "job", "career",
                 "wholesale", "bulk", "in spain", "in france", "in italy", "in germany",
                 "topping", "toppings", "pizza oven", "pizza stone", "best pizza",
                 "dough", "base from scratch", "how do i make", "make a pizza", "cook a pizza",
                 "should i make", "can i make", "to make",
                 "how long", "how hot", "bake", "baking", "baked", "oven", "temperature",
                 "temp", "degrees", "gas mark", "minutes", "takes to cook",
                 "take to cook", "until crisp", "until golden",
                 "bad for you", "is pizza",
                 "bin", "bins", "recycling", "recycle", "cardboard", "compost", "bin it",
                 "throw away", "get rid", "box", "boxes",
                 "crispy", "crisp", "crust", "soggy", "dough", "flour", "yeast", "rise",
                 "prove", "proving", "proofing", "stretch", "stretching", "homemade",
                 "from scratch", "my pizza", "the base", "sticking", "sticks", "stuck",
                 "tray", "trays", "thin crust", "thick crust")),
]

for _row in ENTRIES:
    _row.avoid = tuple(_row.avoid) + NOT_A_MEAL_SUBJECT
