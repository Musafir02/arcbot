import re

from .cakes import (CAKE_AVOID, CAKE_EGGS_AVOID, CAKE_EGGS_KEY, CAKE_KEY,
                    cake_eggs as _cake_eggs, cake_plan as _cake_plan)
from .cleaning import not_a_mark_on_a_thing
from .lookup import (DAY_WORDS, MIN_TYPO_LENGTH, _engine_reads, _one_edit, entry,
                     tokens)
from .shopping import not_a_present
from ..understanding import topics as reading

DISH_WORDS = (
    "egg", "eggs", "chicken", "rice", "pasta", "potato", "potatoes", "steak", "beef",
    "mince", "sausage", "sausages", "bacon", "salmon", "fish", "cod", "prawns", "cake",
    "bread", "sourdough", "quinoa", "couscous", "porridge", "oats", "broccoli", "soup",
    "curry", "gravy", "mushroom", "mushrooms", "onion", "onions", "garlic", "tomato",
    "tomatoes", "avocado", "banana", "cheese", "milk", "butter", "flour", "yoghurt",
    "yogurt", "lentils", "chickpeas", "beans", "noodles", "prawn", "turkey", "lamb",
    "pork", "ham", "spinach", "carrot", "carrots", "cabbage", "peas", "corn", "leek",
    "aubergine", "courgette", "pepper", "peppers", "salad", "casserole", "roast dinner",
)

VEG_WORDS = ("veg", "vegetables", "vegetable", "carrot", "carrots", "courgette", "courgettes",
             "zucchini", "broccoli", "spinach", "peas", "greens", "cauliflower", "beetroot",
             "swede", "squash", "pumpkin", "leek", "leeks", "cabbage", "kale", "pepper",
             "peppers", "mushroom", "mushrooms", "tomato", "tomatoes", "parsnip", "parsnips",
             "turnip", "turnips", "sweetcorn", "beans", "lentils", "aubergine", "celery")

PLANS = {
    "roast-chicken": {
        "names": (("roast chicken",), ("whole chicken",), ("the chicken",),
                  ("a chicken",), ("chicken",)),
        "avoid": ("pox", "shop", "shops", "wing", "wings", "nugget", "nuggets", "soup",
                  "stock", "sandwich", "salad", "curry", "pie",
                  "breast", "breasts", "thigh", "thighs", "leg", "legs", "fillet", "fillets"),
        "temp": "190C, or 170C in a fan oven, in the middle of the oven.",
        "time": ("20 minutes per 500g plus 20 minutes on top: 40 minutes per kilo, so 1 hour "
                 "40 for a 2kg bird."),
        "done": ("74C in the thickest part of the thigh on a digital thermometer, pushed in "
                 "without touching bone, and the juices run clear with the leg moving freely in "
                 "the socket; 75C for a moment is the same thing."),
        "rest": ("15 minutes under foil before carving, or the juice ends up on the board "
                 "instead of in the meat."),
        "skin": ("Leave the skin on: it crisps and keeps the breast moist. Only take it off if "
                 "someone at the table wants skinless, and expect the breast to dry a little."),
        "stuffing": ("Stuff the neck end only, weigh the bird with the stuffing in and add 15 "
                     "to 20 minutes; check the stuffing is piping hot in the middle, not just "
                     "the meat."),
        "ahead": ("You can get it ready the day before: rub it with butter and salt, keep it "
                  "covered in the fridge, and roast it from cold with 10 minutes extra."),
        "keep": ("Wrap the leftovers within an hour and they keep 3 days in the fridge; the "
                 "carcass makes good stock."),
        "fill": "Push a lemon and a few garlic cloves into the cavity, rub the skin with butter and salt, and put onion and carrot in the tin under the bird for the gravy.",
    },
    "chicken-thighs": {
        "names": (("chicken thigh",), ("chicken thighs",), ("thighs",), ("traybake",),
                  ("tray bake",)),
        "temp": "200C, or 180C in a fan oven, and the tray on a high shelf.",
        "time": "35 to 40 minutes at 200C (180C fan), skin side up.",
        "done": ("The skin is crisp and the juices run clear when you pierce the thickest "
                 "part; 74C with a thermometer."),
        "skin": ("Keep the skin on and salt it: it is the best part, and it protects the meat "
                 "underneath. Skinless thighs need only 25 to 30 minutes."),
        "ahead": ("You can marinate them the night before, or roast them in the morning and "
                  "reheat at 180C for 10 minutes."),
        "keep": "They keep 3 days in the fridge and reheat better than breast.",
        "rest": ("5 minutes on the tray under foil is plenty: they are small, so there is no "
                 "need to rest them like a whole bird."),
        "fill": "Marinate them in yoghurt with paprika, cumin and garlic for an hour if you can, or just oil, salt and lemon: they take strong flavours and stay juicy.",
        "sides": "Potatoes tossed in the same tray save a pan; they need 40 minutes, so start them first.",
    },
    "chicken-breast": {
        "ahead": ("Season them and keep them covered in the fridge a few hours before, or cook "
                  "them in the morning and slice them cold: reheated they dry out."),
        "names": (("chicken breast",), ("chicken breasts",), ("breast",)),
        "temp": "200C, or 180C in a fan oven.",
        "time": ("18 to 20 minutes at 200C (180C fan) for a flattened breast, and 12 to 15 for "
                 "a small one."),
        "done": ("The middle is white with no pink, and a thermometer reads 74C; take them out "
                 "the moment they are there."),
        "rest": "5 minutes under foil, so the juice stays in when you cut them.",
        "keep": "They keep 3 days, and are better sliced cold in a salad than reheated.",
        "fill": "Salt it, then a herb butter or a spoon of pesto under the skin-side: breast is the one cut that needs help to stay moist.",
    },
    "salmon": {
        "names": (("salmon",), ("salmon fillet",), ("salmon fillets",)),
        "temp": "200C, or 180C in a fan oven.",
        "time": "12 to 15 minutes at 200C (180C fan), or 4 minutes skin side down in a hot pan.",
        "done": ("The flesh just flakes when you press it with a fork, and it is still slightly "
                 "translucent in the very middle."),
        "skin": ("Leave the skin on for the oven or a pan: it protects the fish and goes crisp. "
                 "It slides off easily once cooked."),
        "ahead": "You can bake it cold the night before and flake it into a salad or pasta.",
        "keep": "Cooked salmon keeps 2 days in the fridge, and does not freeze well.",
        "rest": "No need to rest it: serve salmon straight away, while it is still hot and flaky.",
        "fill": "Salt, pepper, a slice of lemon and a knob of butter, or a spoon of pesto or soy and honey. Keep it simple, the fish does the work.",
    },
    "steak": {
        "names": (("steak",), ("sirloin",), ("ribeye",), ("rump steak",)),
        "avoid": ("gammon", "gammon steak", "tuna", "salmon", "fish"),
        "temp": "A hot pan or 220C (200C fan) in the oven to finish.",
        "time": ("2 to 3 minutes a side for medium rare, 4 a side for medium, plus 5 minutes "
                 "resting."),
        "done": ("Press it with a finger: springy like the base of your thumb is medium rare, "
                 "firm is well done. A thermometer reads 50C for rare, 55C medium rare, 60C "
                 "medium."),
        "rest": ("Rest it 5 minutes under foil, always: the heat drives the juice to the middle while it cooks, and resting lets it spread back out through the meat. Cut straight away and it ends up on the board."),
        "skin": "Trim any hard fat, but leave a rim of it on: it bastes the steak as it cooks.",
        "fill": "Salt it generously just before it goes in the pan, then pepper after: pepper burns. A knob of butter and a garlic clove basted over at the end is the restaurant trick.",
    },
    "gammon steak": {
        "label": "gammon steak",
        "names": (("gammon steak",), ("gammon steaks",), ("gammon",)),
        "temp": "A hot frying pan, or a grill on high.",
        "time": ("4 to 5 minutes a side in a hot pan, or 15 to 20 minutes under the grill, "
                 "turning once."),
        "done": ("It is cooked through, not pink: no pink in the middle, and a thermometer reads "
                 "70C. It is cured pork, so it wants longer than a beef steak."),
        "rest": "2 or 3 minutes is enough - there is less juice in it to settle than in beef.",
        "keep": ("It keeps 2 days cooked, and it is better cold in a sandwich than reheated, "
                 "which dries it out."),
        "fill": ("Nothing more than pepper: it is already salty. A spoon of honey or marmalade "
                 "in the pan at the end glazes it."),
    },

    "sausages": {
        "ahead": ("Cook them on the day. They take 25 to 30 minutes and reheat badly, so "
                  "there is little to gain by doing them early."),

        "label": "sausages",
        "names": (("sausage",), ("sausages",)),
        "temp": "200C, or 180C in a fan oven.",
        "time": "25 to 30 minutes at 200C (180C fan), turning once.",
        "done": ("They are cooked when they are browned all over and the juices run clear; "
                 "press one and it should feel firm, not springy."),
        "skin": ("Don't prick them: the skin holds the juice in, and pricking is what makes "
                 "them dry."),
        "keep": "They keep 3 days in the fridge and freeze well, cooked or raw.",
        "fill": "Nothing inside them: put onion, apple or fennel in the tin beside them, and let the fat that comes out season the mash.",
    },
    "roast-potatoes": {
        "names": (("roast potatoes",), ("roast potato",), ("roasties",)),
        "temp": "200C, or 180C in a fan oven, in a thin layer of hot oil.",
        "time": ("Parboil 8 minutes, then 40 to 45 minutes in the oven, turning once halfway."),
        "done": "They are ready when the edges are deep gold and crusty; shake the tin and they should rattle.",
        "ahead": ("Parboil and rough them up in the morning, keep them in the fridge, and roast "
                  "them at the last minute."),
        "skin": "Leave the skin on if the potatoes are small: it goes crisper than a peeled one.",
        "keep": "They reheat well at 200C for 8 minutes, better than in a microwave.",
        "fill": "Parboil them, shake them in the pan to rough up the edges, then hot fat or oil, salt and a sprig of rosemary: the rough edges are what go crisp.",
    },
    "cake": {
        "names": (("cake",), ("sponge",), ("birthday cake",), ("layer cake",)),
        "temp": "180C, or 160C in a fan oven.",
        "time": ("A 20cm sponge bakes for 25 to 30 minutes and a loaf tin for 45 to 55; about "
                 "an hour and a half start to finish once you count mixing and cooling."),
        "done": ("A skewer in the middle comes out clean, and the top springs back when you "
                 "press it lightly."),
        "ahead": ("Bake it the day before, cool it completely, wrap it well and fill it on the "
                  "day: it keeps 3 days in a tin."),
        "keep": "It keeps 3 days in a tin, or freezes for 2 months undecorated.",
        "allergy": ("Leave the nuts out altogether and swap in a handful of chocolate chips or "
                    "raisins; check the chocolate and any ready-made icing for 'may contain "
                    "nuts', and keep the tin and worktop clean if the allergy is serious."),
        "fill": "Butter and sugar creamed first, then eggs a little at a time, then flour folded in gently, and a spoon of milk if the mix is stiff.",
        "sides": "Buttercream is 100g soft butter to 200g icing sugar, beaten with a splash of milk.",
        "frosting": ("Buttercream or ganache keeps 3 to 4 days in a sealed tub in the fridge, or "
                     "2 months in the freezer: bring it back to room temperature and beat it "
                     "again before you use it. The cake is better filled on the day."),
    },
    "curry": {
        "names": (("curry",), ("tikka",), ("korma",), ("dhal",), ("daal",)),
        "temp": "Medium heat on the hob, 190C (170C fan) if it goes in the oven.",
        "time": ("35 to 45 minutes from scratch: 10 minutes of frying the onions and spices, "
                 "then 25 to 30 minutes simmering."),
        "done": ("The sauce has darkened and thickened and the oil comes back to the surface; "
                 "the meat should be tender enough to cut with a spoon."),
        "ahead": ("It is better made the day before: cool it quickly, keep it in the fridge and "
                  "reheat it gently with a splash of water."),
        "keep": "It keeps 3 days in the fridge and freezes well for 3 months.",
        "fill": "Start with onion, garlic and ginger, then the spices (cumin, coriander, turmeric, chilli) fried for 30 seconds in the oil, then the meat or veg and a tin of tomatoes or coconut milk.",
        "sides": ("Rice, and naan or a chapati if you have them: a mug of rice to one and a half "
                  "of water, 12 minutes with the lid on, and a spoon of yoghurt or raita beside "
                  "it."),
    },
    "bread": {
        "names": (("bread",), ("sourdough",), ("loaf",), ("dough",)),
        "temp": "230C, or 210C in a fan oven, with the oven well preheated.",
        "time": ("35 to 45 minutes for a large loaf, 20 to 25 for rolls; the first 15 minutes "
                 "with steam."),
        "done": ("It sounds hollow when you tap the base, and a thermometer reads 95C inside."),
        "ahead": ("You can leave the shaped loaf in the fridge overnight and bake it straight "
                  "from cold, which gives a better flavour."),
        "keep": "It keeps 3 days in a paper bag; slice and freeze what you won't eat.",
        "fill": "Flour, water, salt and yeast, and time: a slow rise in the fridge overnight gives more flavour than anything you can add.",
    },
    "chips": {
        "names": (("chips",), ("fries",), ("oven chips",), ("frozen chips",)),
        "temp": "200C, or 180C in a fan oven, on a tray with space between them.",
        "time": ("20 to 25 minutes at 200C from frozen, turning once; an air fryer does them in "
                 "12 to 15 minutes at 200C. Fresh-cut chips want 30 to 35 minutes."),
        "done": "Golden at the edges and hollow-sounding when you shake the tray.",
        "keep": ("They are only good the day they are cooked: reheat them 5 minutes at 200C, "
                 "never in a microwave, or they go limp."),
        "fill": "Salt after, not before, and a sprig of rosemary or a shake of paprika in the last few minutes. Vinegar at the table.",
        "sides": ("Fish fingers, a fried egg or a burger, and peas, pickles or coleslaw: something "
                  "sharp cuts the fat."),
    },
    "pie": {
        "names": (("pie", "fruit pie", "apple pie", "pie dish"), ("pies", "fruit pies")),
        "temp": "200C, or 180C in a fan oven.",
        "time": ("30 to 35 minutes for a fruit pie with a pastry lid, and 45 minutes if it is a "
                 "deep one; blind bake an empty case 15 minutes first."),
        "done": ("The pastry is golden and pulls away from the dish a little, and the filling "
                 "bubbles up through the hole in the middle."),
        "keep": ("A fruit pie keeps 2 days in the fridge once it is baked, and reheats at 180C "
                 "(160C fan) for 15 minutes, which brings the pastry back. Unbaked, it freezes for "
                 "3 months: freeze it in the dish, then bake it from frozen at 200C (180C fan) for "
                 "20 minutes longer than the recipe says."),
    },
    "savoury pie": {
        "names": (("shepherd's pie", "shepherds pie", "shepherd pie", "cottage pie",
                   "chicken pie", "steak pie", "pot pie", "savoury pie", "savory pie"),
                  ("shepherd's pies", "cottage pies", "chicken pies", "steak pies")),
        "temp": "190C, or 170C in a fan oven.",
        "time": ("35 to 40 minutes from cold for a shepherd's or cottage pie; a pastry-topped one "
                 "wants 200C (180C fan) for 30 minutes."),
        "done": ("The top is browned and the filling bubbles at the edges; a skewer in the middle "
                 "comes out hot."),
        "keep": ("It keeps 3 to 4 days in the fridge, covered, and reheats at 180C for 20 minutes "
                 "or in portions in the microwave. It freezes well for 3 months: freeze it before "
                 "baking, then cook it from frozen for about an hour, or thaw it overnight first."),
    },
    "scones": {
        "names": (("scone",), ("scones",), ("fruit scone",), ("cheese scone",)),
        "temp": "220C, or 200C in a fan oven, on a hot floured tray near the top.",
        "time": "12 to 15 minutes, and no longer than that or they go dry.",
        "done": ("They are risen and browned on top, and the sides look dry; a skewer in the "
                 "middle comes out clean."),
        "keep": ("Best eaten the day they are made, warm. They freeze well, split first, and "
                 "come back in a low oven for 5 minutes."),
        "fill": ("Rub cold butter into self-raising flour with a pinch of salt, add the milk in "
                 "one go, and handle the dough as little as you can: cut out the rounds and put "
                 "them straight in, and do not twist the cutter."),
    },
    "muffins": {
        "names": (("muffin",), ("muffins",), ("blueberry muffin",), ("chocolate muffin",)),
        "temp": "200C, or 180C in a fan oven.",
        "time": "18 to 22 minutes for a normal-sized tin.",
        "done": ("The tops are domed and spring back when pressed, and a skewer comes out with "
                 "crumbs rather than wet batter."),
        "keep": "They keep 2 days in a tin and freeze for 2 months.",
        "fill": ("Melt the butter and mix the wet into the dry in one go, then stop: lumps are "
                 "right for a muffin. Ten stirs too many is what makes them tough, and frozen "
                 "berries go in unthawed."),
    },
    "biscuits": {
        "names": (("biscuit", "biscuits", "cookie", "cookies"), ("shortbread",), ("flapjack",)),
        "temp": "180C, or 160C in a fan oven, on a lined flat tray.",
        "time": "10 to 12 minutes for a drop cookie; shortbread wants 20 to 25 at 160C.",
        "done": ("The edges are set and the middle still looks slightly underdone, which is "
                 "right: they firm up as they cool on the tray."),
        "keep": "They keep a week in a sealed tin, and freeze for 3 months.",
        "fill": ("Cream the butter and sugar first, fold the flour in last, and chill the dough "
                 "20 minutes so they spread less. Leave 5cm between them on the tray."),
    },
    "meringues": {
        "names": (("meringue",), ("meringues",), ("pavlova",)),
        "temp": "100C to 120C, or 90C to 100C in a fan oven, on greaseproof paper.",
        "time": "1 hour to 1 hour 15 for dry meringues, then leave them in the switched-off oven "
                "until it is cold.",
        "done": ("They lift off the paper cleanly and sound hollow when tapped on the base."),
        "keep": "They keep a week in an airtight tin, and go soft in the fridge.",
        "fill": ("Bowl and whisk free of grease, no trace of yolk in the whites, and sugar a "
                 "spoonful at a time once they hold a soft peak: that is what stops them "
                 "weeping."),
    },
    "yorkshire-puddings": {
        "names": (("yorkshire pudding",), ("yorkshire puddings",), ("yorkshires",),
                  ("popover",), ("popovers",)),
        "temp": "220C, or 200C in a fan oven, with the tin of fat smoking hot first.",
        "time": "20 to 25 minutes without opening the door.",
        "done": ("They are tall, crisp and brown at the edges; a pale one has not had enough "
                 "heat or enough fat."),
        "keep": "They freeze for a month and come back at 200C for 5 minutes.",
        "fill": ("Equal volumes of egg, milk and plain flour, rested half an hour, into a "
                 "centimetre of smoking oil or dripping: the hot fat is what makes them rise."),
    },
    "roast-vegetables": {
        "ahead": ("Chop them the night before and keep them in a bowl of cold water in the "
                  "fridge; drain, oil and roast them as usual."),
        "names": (("roast vegetables",), ("roast veg",), ("roasted vegetables",)),
        "temp": "200C, or 180C in a fan oven.",
        "time": "30 to 40 minutes, turning once, with 20 minutes for softer veg like peppers.",
        "done": "The edges are browned and a knife goes in easily.",
        "keep": "They keep 4 days in the fridge and are good cold in a salad or a wrap.",
        "fill": "Oil, salt and pepper is the base; add whole garlic cloves, rosemary or thyme, and a spoon of honey or balsamic for the last 10 minutes.",
    },
    "spag-bol": {
        "names": (("spag bol",), ("spaghetti bolognese",), ("spaghetti bolognaise",),
                  ("bolognese",), ("bolognaise",), ("bol",)),
        "temp": "Medium heat on the hob: the mince browns in a dry hot pan before the sauce goes in.",
        "time": ("an hour start to finish, and the sauce is worth the last half of it at a bare "
                 "simmer with the lid off. Thirty minutes is edible, an hour is good."),
        "done": ("The sauce has darkened and thickened and the fat pools a little at the edge; "
                 "season it with more salt than feels right and a pinch of sugar."),
        "keep": ("Better the next day. It keeps 3 days in the fridge and freezes for 3 months, "
                 "so a big pot is worth it."),
        "fill": "Onion, carrot and celery chopped small and softened first, then mince, tomato puree, tinned tomatoes and a splash of milk or wine; a bay leaf and a pinch of sugar finish it.",
        "sides": ("Garlic bread and a green salad, and keep a mug of the pasta water back to "
                  "loosen the sauce with."),
    },
    "lasagne": {
        "names": (("lasagne",), ("lasagna",), ("lasagne verdi",)),
        "ahead": ("Assemble it the day before, keep it covered in the fridge and add 5 to 10 "
                  "minutes in the oven from cold; the ragu alone can be made two days early."),
        "temp": "180C, or 160C in a fan oven, on the middle shelf.",
        "time": ("35 to 40 minutes in the oven, and the ragu wants 30 to 40 minutes on the hob "
                 "before you build it."),
        "rest": "10 to 15 minutes out of the oven, or it slumps when you cut it.",
        "done": ("Bubbling at the edges with the top browned, and a knife through the middle "
                 "meets no resistance from the pasta; rest it so it cuts cleanly."),
        "keep": ("It keeps 3 days in the fridge and freezes in portions for 3 months: reheat "
                 "covered at 180C for 25 minutes."),
        "fill": "A ragu of mince, onion, carrot and tomato cooked down for at least an hour, a bechamel, and parmesan between and on top: the rest is layering.",
        "sides": ("Garlic bread and a green salad with a sharp dressing, because the salad is what "
                  "cuts through the sauce: tear the bread, rub it with garlic, oil and salt and "
                  "give it 8 minutes in a hot oven while the pasta cooks."),
    },
    "stew": {
        "names": (("beef stew",), ("stew",), ("casserole",), ("hotpot",), ("hot pot",)),
        "ahead": ("It is better the next day, so make it the day before and reheat it gently "
                  "with a splash of water; it keeps 3 days in the fridge and freezes well."),
        "avoid": ("apple", "apples", "fruit", "prune", "prunes", "rhubarb", "plum", "plums",
                  "pear", "pears", "berry", "berries"),
        "temp": "150C (130C fan) in the oven with the lid on, or the lowest ring on the hob.",
        "time": ("two to two and a half hours at a bare simmer, and longer at a lower heat "
                 "always beats hotter and shorter."),
        "done": ("The beef pulls apart with a fork and the liquid has thickened; if it is still "
                 "tight, another 30 minutes will not hurt it."),
        "keep": "Better the next day, and it keeps 3 days in the fridge or 3 months frozen.",
        "fill": "Onion, carrot, celery and a spoon of tomato puree; add potatoes or dumplings if you want it to be the whole meal, and a splash of Worcestershire or stout for depth.",
        "sides": "Mash, or dumplings dropped in for the last 25 minutes with the lid on.",
    },
    "chilli": {
        "names": (("chilli con carne",), ("chilli",), ("chili",), ("chile con carne",)),
        "avoid": ("powder", "flakes", "flake", "sauce", "oil", "plant", "plants", "seeds",
                  "seed", "grow", "growing", "grew"),
        "temp": "Medium heat on the hob, or 160C (140C fan) in the oven with the lid on.",
        "time": ("45 minutes to an hour from scratch, and better for longer: brown the mince, "
                 "then soften the onion and pepper and let the tomatoes and beans go slowly."),
        "done": ("Darkened and thickened and the fat pools at the edge: taste it and add salt, "
                 "then a square of dark chocolate if it tastes sharp."),
        "keep": "It keeps 3 days in the fridge and freezes for 3 months, and it is better the next day.",
        "fill": "Mince (or beans and mushrooms), onion, garlic, cumin, smoked paprika and chilli, a tin of tomatoes and a tin of kidney beans; a square of dark chocolate at the end rounds it off.",
        "sides": "Rice, or tortillas and a bowl of grated cheese and sour cream on the table.",
    },
    "fish-pie": {
        "names": (("fish pie",), ("fishpie",)),
        "temp": "180C, or 160C in a fan oven.",
        "time": ("35 to 40 minutes at 180C from cold, or 25 minutes if the filling is still "
                 "warm."),
        "rest": "10 minutes out of the oven, so the sauce settles and it does not run.",
        "done": "The sauce bubbles up at the edges and the top is crisp; a knife in the middle comes out hot.",
        "keep": ("It keeps 3 to 4 days in the fridge, covered, and reheats at 180C for 20 "
                 "minutes or in portions in the microwave. It freezes well for 3 months: freeze "
                 "it unbaked, then cook it from frozen at 180C for about an hour, or thaw it "
                 "overnight and give it the usual 35 to 40 minutes."),
        "fill": "Fish (smoked haddock and a white fish is the classic), a white sauce made with the milk the fish was poached in, and mashed potato on top with a little mustard and cheese.",
        "sides": ("New potatoes and peas, or rice with greens wilted in a pan with butter. A "
                  "squeeze of lemon and yoghurt with chopped dill is all the sauce it needs, and "
                  "both take less time than the fish."),
    },
    "pasta-bake": {
        "names": (("pasta bake",), ("baked pasta",), ("tuna bake",), ("macaroni cheese bake",)),
        "ahead": ("Boil the pasta and make the sauce the day before, mix and cover it in the "
                  "fridge, then bake it from cold with 10 minutes extra; baked and cooled it "
                  "reheats covered at 180C for 20 minutes."),
        "temp": "200C, or 180C in a fan oven.",
        "time": "25 to 30 minutes at 200C, or 20 minutes if the pasta and sauce are still hot.",
        "done": ("The cheese is browned and the sauce bubbles at the edges; cook the pasta 2 "
                 "minutes short of the packet first, or it goes soft in the oven."),
        "keep": "It keeps 3 days in the fridge and reheats covered at 180C for 20 minutes.",
        "fill": "A tomato sauce with garlic and basil, cooked pasta, and mozzarella or cheddar on top; add bacon, courgette or spinach to the sauce if you have them.",
        "sides": ("Garlic bread, rubbed with a cut clove and oiled, or a green salad with a sharp "
                  "dressing: the bake is rich, so something crisp and acidic beside it is the "
                  "whole job."),
    },
    "sunday-roast": {
        "ahead": ("Prep the night before: parboil and rough up the potatoes and keep them in "
                  "the fridge, and peel the veg into a bowl of cold water. The meat goes in on "
                  "the day, because that is the part that wants the oven."),
        "names": (("sunday roast",), ("roast dinner",), ("roast lunch",), ("a roast",)),
        "avoid": ("vegetables", "veg", "potatoes", "potato", "chicken", "beef", "lamb", "pork",
                  "turkey", "duck", "nuts", "chestnuts", "coffee", "beans", "peppers",
                  "tomatoes", "onions", "parsnips", "carrots", "garlic"),
        "temp": ("190C (170C fan) for a joint or a bird, and the potatoes go up to 200C once "
                 "the meat is out and resting."),
        "time": "about 1 hour 40 at 190C for a 2kg joint or bird.",
        "rest": ("15 to 20 minutes under foil while the potatoes finish and the gravy is made, "
                 "which is what makes the timings work."),
        "done": "74C in the thickest part of a chicken thigh, or 60C for beef you want pink.",
        "keep": "Leftovers keep 3 days, and the bones make the gravy or a stock.",
        "fill": "A joint, potatoes parboiled and roasted in hot fat, and two veg: carrots or parsnips in the oven, greens on the hob. Gravy from the tin juices.",
        "sides": ("Parboil the potatoes 8 minutes, shake them in the pan with hot fat and roast "
                  "40 to 45 minutes at 200C; greens take 5 minutes at the end, and the gravy "
                  "wants the roasting tin on the hob with a spoon of flour and the stock."),
    },
}

READY_NOTES = {
    "rice": (
        ("rice", "basmati", "long grain", "jasmine rice", "pilau", "arborio",
         "risotto rice", "brown rice"),
        "When the water has gone and the grains are tender with a little bite at the centre: taste "
        "one rather than watching the clock, and if it is still chalky add a splash of water and "
        "give it 3 more minutes with the lid on, then leave it off the heat with the lid on for "
        "5 minutes.",
    ),
    "pasta": (
        ("pasta", "spaghetti", "penne", "fusilli", "macaroni", "tagliatelle", "rigatoni",
         "noodles"),
        "Fish a piece out and bite it: tender all the way through with no chalky core and still a "
        "little firm in the middle. Start tasting 2 minutes before the packet time, and dip a mug "
        "of the cooking water out before you drain it, because it is what loosens the sauce.",
    ),
    "egg": (
        ("egg", "eggs", "boiled egg", "boiled eggs", "soft boiled egg", "hard boiled egg"),
        "It depends what you want: 4 minutes for a runny yolk, 6 for a soft one and 8 to 9 for a "
        "firm one, counted from the moment they go into water that is already boiling, then into "
        "cold water so they stop cooking.",
    ),
    "poached egg": (
        ("poached egg", "poached eggs", "poach", "poaching", "poached"),
        "A poached egg is done when the white is opaque and set and the yolk still gives when you "
        "press it lightly: 3 minutes in barely simmering water for a runny one, 4 for a set white. "
        "Lift it out with a slotted spoon and drain it on kitchen paper.",
    ),
    "scrambled egg": (
        ("scrambled egg", "scrambled eggs", "scramble", "scrambled", "scrambling"),
        "Scrambled eggs are done when they are just set and still glossy: take them off the heat "
        "while they look a little wetter than you want, because they go on cooking in the pan and "
        "on the plate. Low heat and slow stirring is what keeps them soft.",
    ),
    "fried egg": (
        ("fried egg", "fried eggs", "fry an egg", "frying an egg", "sunny side up"),
        "A fried egg is done when the white is fully set with no clear, wobbly patches and the "
        "yolk is as firm as you like it: about 3 minutes on a low-medium heat with the lid on for "
        "a soft yolk, 4 to 5 without.",
    ),
    "porridge": (
        ("porridge", "oats", "oatmeal", "porridge oats"),
        "When the oats have collapsed into the milk and it coats the back of the spoon. Take it "
        "off while it is still a little looser than you want it, because it thickens as it sits "
        "in the bowl.",
    ),
    "omelette": (
        ("omelette", "omelet", "omelettes", "omelets"),
        "An omelette is done when the top is just set and the middle still has a slight wobble: "
        "fold it while the centre is a little soft, because it finishes on the plate. Two or three "
        "minutes on a medium heat, and off the pan before it browns.",
    ),
    "lentils": (
        ("lentils", "lentil", "dal", "dhal"),
        "Taste one: a lentil is done when it gives under the tooth with no chalky middle. Green "
        "and brown take 20 to 25 minutes, red split lentils 15 to 20 and go mushy on purpose.",
    ),
    "soup": (
        ("soup", "broth", "bisque"),
        "When the hardest thing in it - a carrot, a potato, a lentil - gives to a knife with no "
        "resistance, and it has had 15 minutes after that for the flavours to come together. "
        "Season at the end, not the start.",
    ),
}

READY_NAMES = tuple(sorted({name for names, _ in READY_NOTES.values() for name in names}))


def _ready_food(text):
    line = str(text or "")
    best, best_len = None, 0
    for food, (names, _) in READY_NOTES.items():
        for name in names:
            if len(name) > best_len and _phrase_in(line, name):
                best, best_len = food, len(name)
    return best


def _ready_note(memory, understood):
    text = _line_text(understood)
    if dish_in(text):
        return None
    food = _ready_food(text)
    if food is None:
        for earlier in recent_texts(memory)[:4]:
            food = _ready_food(earlier)
            if food:
                break
    if food is None:
        return None
    return READY_NOTES[food][1]


SIDES = {
    "rice": ("Rice: 1 part rice to 1.5 parts water, 12 minutes with the lid on, then 10 "
             "minutes off the heat without lifting the lid."),
    "potatoes": ("Potatoes: boil them for 15 to 20 minutes, or roast them at 200C for 40 "
                 "to 45 minutes if you have the oven on anyway."),
    "salad": ("A bag of leaves with a squeeze of lemon and a little oil is enough; dress it "
              "at the table so it does not go limp."),
    "bread": "Warm bread or a naan straight from the oven, no need for anything clever.",
    "vegetables": ("Green vegetables: broccoli or beans steamed for 4 to 5 minutes, while "
                   "everything else is on the table."),
    "gravy": ("Gravy: whisk a teaspoon of flour into the meat juices off the heat, then add "
              "stock and simmer it for 5 minutes, stirring the brown bits up. If it goes lumpy, "
              "push it through a sieve."),
}

SIDE_WORDS = {
    "rice": ("rice", "basmati", "pilau", "pilaf"),
    "potatoes": ("potato", "potatoes", "mash", "chips", "roasties"),
    "salad": ("salad", "slaw", "lettuce"),
    "bread": ("bread", "naan", "pitta", "pita", "rolls", "garlic bread"),
    "vegetables": ("veg", "vegetables", "greens", "broccoli", "beans", "peas", "carrots"),
    "gravy": ("gravy", "jus"),
}

ASK_KINDS = (
    ("fix", ("how do i stop", "how can i stop", "how to stop", "how do i fix", "how can i fix",
             "how to fix", "what am i doing wrong", "what went wrong", "why does it keep",
             "why does my", "why is my", "why do my", "how do i make it not", "how do i get it to",
             "what can i add", "what can i do about"),
     ("it", "that", "this", "them", "always", "keeps", "keep", "going", "come", "comes",
      "coming", "out", "turn", "turns", "my", "the")),
    ("temp", ("temperature", "temp", "degrees c", "how many degrees", "what degrees", "gas mark",
              "how hot", "how warm", "what heat", "which shelf"),
     ("oven", "fan", "bake", "roast", "cook", "hot", "heat", "setting")),
    ("time", ("how long", "how many minutes", "how many hours", "how much time",
              "what time", "how long will", "long enough", "per kilo", "per kg"),
     ("oven", "take", "takes", "long", "time", "minutes", "hours", "cook", "roast", "bake",
      "kilo", "kilos", "kilogram", "kg", "total", "altogether", "should", "need", "about")),
    ("done", ("how do i know when", "how do i know its done", "how do i know it is cooked",
              "how can i tell when", "how can i tell its done",
              "how can i tell it is done", "how can i tell its cooked",
              "how do i tell when", "how do i tell its done",
              "how do i tell it is done", "how do i tell its cooked",
              "how can i tell if it is done", "how can i tell if its done",
              "how can i tell if it is cooked", "how can i tell if its cooked",
              "how can i tell if it is ready", "how can i tell if its ready",
              "how do i tell if it is done", "how do i tell if its done",
              "how do i tell if it is cooked", "how do i tell if its cooked",
              "how can i tell if the", "how do i tell if the",
              "is it done", "when is it done", "ready yet",
              "is it cooked", "how do i check if", "how do i check when",
              "how can i check if", "how can i check when", "how do i check its done",
              "how do i check it is done", "how will i know",
              "how do i test if", "how do i test whether", "how do i test",
              "how can i test", "how do you test", "how should i test"),
     ("done", "cooked", "ready", "check", "tell", "test", "thermometer", "juice", "juices",
      "it", "is", "when")),
    ("skin", ("skin", "skins", "skinless"),
     ("off", "on", "need", "take", "leave", "should", "do", "remove", "keep", "it")),
    ("stuffing", ("stuff", "stuffing", "stuffed"),
     ("it", "should", "can", "need", "do", "if", "and", "chicken", "the")),
    ("frosting", ("frosting", "icing", "buttercream", "ganache", "filling"),
     ("it", "the", "make", "made", "can", "could", "should", "day", "before", "ahead",
      "keep", "keeps", "stays", "ok", "make")),
    ("ahead", ("ahead", "ahead of time", "in advance", "day before", "night before",
               "make it earlier", "prepare it", "get it ready"),
     ("make", "made", "prepare", "bake", "cook", "can", "could", "should", "it", "that")),
    ("keep", ("can i still use it", "can i still use that", "can i still eat it",
              "is it still ok", "is it still good", "is it still all right", "is it still alright",
              "how long will it keep", "how long does it keep", "how long do they keep",
              "how long will they keep", "will it keep", "does it keep", "can i keep",
              "can i store", "how do i store", "how should i store", "how long does it last",
              "how long will it last", "can i freeze", "does it freeze", "can it be frozen",
              "how do i reheat", "what about the leftovers", "what do i do with the leftovers",
              "keep fresh", "keep it fresh", "keeps fresh", "stay fresh", "stays fresh",
              "keep them fresh", "keep mine fresh", "from going stale", "stop it going stale",
              "going stale", "goes stale", "goes hard", "going hard"),
     ("long", "it", "that", "they", "days", "day", "ok", "safe", "again", "much", "fridge",
      "freezer", "leftover", "leftovers")),
    ("rest", ("rest", "resting", "rested"),
     ("it", "should", "long", "how", "need", "do", "before", "then")),
    ("allergy", ("allergic", "allergy", "allergies", "nut", "nuts", "intolerance"),
     ("he", "she", "they", "son", "daughter", "child", "is", "has", "to", "what", "can")),
    ("sides", ("what should i have with it", "what should i have with that",
               "what can i have with it", "what to have with it", "anything with it",
               "what goes with it", "what side", "which side", "any sides", "what sides",
               "what to serve with it", "serve with it", "what about the side"),
     ("it", "that", "with", "go", "goes", "have", "side", "sides", "serve", "dish", "on")),
    ("fill", ("what should i put in", "what do i put in", "what goes in", "what shall i put in",
              "what to put in", "ingredients", "what do i need in it", "what should go in"),
     ("put", "in", "goes", "go", "inside", "need", "add", "with")),

)


def _phrase_in(text, phrase):
    wanted = tokens(phrase)
    have = tokens(text)
    if not wanted or not have:
        return False
    n = len(wanted)
    for i in range(len(have) - n + 1):
        if all(have[i + j] == wanted[j] or _same_word(have[i + j], wanted[j])
               for j in range(n)):
            return True
    return False


CUT_OFF = ("breast", "breasts", "thigh", "thighs", "leg", "legs", "wing", "wings",
           "fillet", "fillets", "drumstick", "drumsticks", "supreme", "supremes")


def _one_slip(word, target):
    if word == target or len(word) < 4 or abs(len(word) - len(target)) > 1:
        return False
    if len(word) == len(target):
        return sum(1 for a, b in zip(word, target) if a != b) == 1
    shorter, longer = (word, target) if len(word) < len(target) else (target, word)
    for i in range(len(longer)):
        if longer[:i] + longer[i + 1:] == shorter:
            return True
    return False


def _a_cut(word):
    return any(_same_word(word, cut) or _one_slip(word, cut) for cut in CUT_OFF)


def _same_word(a, b):
    if a == b:
        return True
    for one, two in ((a, b), (b, a)):
        if len(one) > 3:
            if one.endswith("s") and one[:-1] == two:
                return True
            if one.endswith("es") and one[:-2] == two:
                return True
            if one.endswith("ing") and (one[:-3] == two or one[:-3] + "e" == two):
                return True
            if one.endswith("ed") and one[:-2] == two:
                return True
    return False


def _slip_of(typed, word):
    key = word.strip().lower()
    typed = (typed or "").strip().lower()
    if len(key) < MIN_TYPO_LENGTH or len(typed) < MIN_TYPO_LENGTH or " " in key:
        return False
    if typed[:1] != key[:1] or _engine_reads(typed):
        return False
    return _one_edit(typed, key)


_A_MADE_DISH = ("soup", "soups", "broth", "broths")


def _a_made_dish(word):
    return any(_same_word(word, dish) for dish in _A_MADE_DISH)

_RULE_OUT = {
    "no", "not", "never", "isnt", "arent", "wasnt", "werent", "dont", "doesnt", "didnt",
    "cant", "cannot", "wont", "without", "except", "excepting", "instead", "apart", "but",
    "other", "rather", "sick", "bored", "tired", "hate", "hates", "dislike", "loathe",
    "skip", "avoid", "anything", "nothing",
}
_RULE_OUT_FILLER = {
    "a", "an", "the", "any", "more", "another", "one", "of", "to", "do", "doing", "make",
    "making", "cook", "cooking", "have", "having", "want", "wanting", "that", "this", "it",
    "its", "my", "our", "us", "me", "them", "for", "with", "be", "being", "even",
}


_INGREDIENT_AFTER = {
    "paste", "powder", "sauce", "stock", "cube", "cubes", "tin", "tins", "jar", "jars",
    "packet", "packets", "pack", "packs", "sachet", "sachets", "oil", "puree", "mix",
    "seasoning", "leaves", "seeds", "granules", "concentrate", "flavouring", "flavourings",
    "essence", "syrup",
}


def _ruled_out_near(have, at, width=1):
    after = at + width
    if after < len(have):
        tail = have[after].replace("\u2019", "").replace("'", "")
        if tail in _INGREDIENT_AFTER:
            return False
    for step in range(1, min(at, 5) + 1):
        word = have[at - step].replace("\u2019", "").replace("'", "")
        if word in _RULE_OUT_FILLER:
            continue
        return word in _RULE_OUT
    return False


def not_ruled_out(*keys):
    def guard(understood):
        text = (str((understood or {}).get("clean") or (understood or {}).get("text") or ""))
        return not (set(keys) & dishes_ruled_out(text))
    return guard


def _ruled_out_spans(have):
    covered = set()
    for plan in PLANS.values():
        for names in plan.get("names", ()):
            for name in (names if isinstance(names, tuple) else (names,)):
                wanted = tokens(name)
                if not wanted or len(wanted) > len(have):
                    continue
                for i in range(len(have) - len(wanted) + 1):
                    if not _ruled_out_near(have, i, len(wanted)):
                        continue
                    if all(_same_word(have[i + j], wanted[j]) for j in range(len(wanted))):
                        covered.update(range(i, i + len(wanted)))
    return covered


def dishes_ruled_out(text):
    have = tokens(text or "")
    out = set()
    for key, plan in PLANS.items():
        for names in plan.get("names", ()):
            for name in (names if isinstance(names, tuple) else (names,)):
                wanted = tokens(name)
                if not wanted or len(wanted) > len(have):
                    continue
                for i in range(len(have) - len(wanted) + 1):
                    if all(_same_word(have[i + j], wanted[j]) for j in range(len(wanted))) \
                            and _ruled_out_near(have, i, len(wanted)):
                        out.add(key)
                        break
    return out


def _named(text):
    have = tokens(text)
    elsewhere = reading.says_another_thing(text)
    ruled = _ruled_out_spans(have)
    best = None
    for key, plan in PLANS.items():
        for names in plan.get("names", ()):
            for name in (names if isinstance(names, tuple) else (names,)):
                wanted = tokens(name)
                if not wanted or len(wanted) > len(have):
                    continue
                avoid = plan.get("avoid", ())
                for i in range(len(have) - len(wanted) + 1):
                    if not all(_same_word(have[i + j], wanted[j])
                               or (len(wanted) > 1 and _slip_of(have[i + j], wanted[j]))
                               for j in range(len(wanted))):
                        continue
                    after = have[i + len(wanted)] if i + len(wanted) < len(have) else ""
                    if after and any(_same_word(after, word) or _slip_of(after, word)
                                     for word in avoid):
                        continue
                    if after and _a_cut(after):
                        continue
                    if after and _a_made_dish(after):
                        continue
                    if elsewhere and any(word in elsewhere
                                         for word in have[i:i + len(wanted)]):
                        continue
                    if any(at in ruled for at in range(i, i + len(wanted))):
                        continue
                    found = (len(wanted), i, key)
                    if best is None or found[:2] > best[:2]:
                        best = found
    return best


_PLAN_MARKER = (
    "making", "doing", "cooking", "roasting", "baking", "starting", "having",
    "im going to", "i'm going to", "we're going to", "we are going to", "going to cook",
    "going to make", "going to do",
    "fancy", "fancying", "thinking of", "thinking about", "thought about", "considering",
    "considered", "feel like", "feeling like", "in the mood for", "might do", "might make",
    "might cook", "planning", "planning on", "plan to",
)
_IDEA_ASK = (
    "what should i cook", "what can i cook", "what shall i cook", "what do i cook",
    "what to cook", "what should i make", "what can i make", "what shall i make",
    "what else", "what can i eat", "what should i eat", "what shall i eat", "what do i eat",
    "what to eat", "whats for", "what's for", "what is for", "what can i have",
    "what should i have", "what shall i have", "what to have", "what can we have",
    "ideas", "idea", "suggest", "recommend", "options", "something to cook",
    "something quick", "something easy", "meal plan", "meal ideas", "dinner ideas",
    "bored of", "bored with", "sick of", "tired of", "fed up", "had enough of", "instead of",
    "any more", "other than", "another", "different", "impress", "in laws", "in-laws",
    "new recipe", "any good recipes",
)


def a_dish_is_already_the_plan(text):
    text = str(text or "").lower()
    if not text or dish_in(text) is None:
        return False
    if not any(marker in text for marker in _PLAN_MARKER):
        return False
    return not any(phrase in text for phrase in _IDEA_ASK)


def dish_in(text):
    if not isinstance(text, str) or not text.strip():
        return None
    found = _named(text)
    return found[2] if found else None


PART_OF = {
    "frosting": "cake", "icing": "cake", "buttercream": "cake", "ganache": "cake",
}

IMPLIED_ASKS = ("ahead", "ahead of time", "in advance", "day before", "night before",
                "make it earlier", "prepare it", "get it ready",
                "how long will it keep", "how long does it keep", "will it keep",
                "keep for", "keeps for", "can i keep", "can i store", "how do i store",
                "how long does it last", "how long will it last", "can i freeze",
                "does it freeze", "can it be frozen")


PART_NOT = ("icing sugar", "sugar paste", "frosting mix", "buttercream powder")


def implied_dish(text):
    if not isinstance(text, str) or not text.strip():
        return None
    if any(_phrase_in(text, no) for no in PART_NOT):
        return None
    for part, key in PART_OF.items():
        if _phrase_in(text, part) and key in PLANS:
            return key
    return None


def _line_text(understood):
    if not isinstance(understood, dict):
        return ""
    return understood.get("norm_text") or understood.get("clean") or ""


def side_in(text):
    if a_colour_choice(text):
        return None
    for key, phrases in SIDE_WORDS.items():
        for phrase in phrases:
            if _phrase_in(text, phrase):
                return key
    return None


def recent_texts(memory):
    users = []
    turns = memory.get("turns")
    if isinstance(turns, list):
        for turn in reversed(turns[-4:]):
            if isinstance(turn, dict) and isinstance(turn.get("user"), str):
                users.append(turn["user"])
    record = memory.get("topic")
    if isinstance(record, dict) and isinstance(record.get("text"), str):
        users.append(record["text"])
    return users


def dish_for(memory, understood):
    text = ""
    if isinstance(understood, dict):
        text = understood.get("norm_text") or understood.get("clean") or ""
    key = dish_in(text)
    if key:
        return key
    if _names_food(text):
        return None
    for earlier in recent_texts(memory)[:6]:
        key = dish_in(earlier)
        if key:
            return key
    return None


_STARCH = ("mash", "mashed potato", "mashed potatoes", "potato", "potatoes", "rice", "porridge",
           "oats", "oatmeal", "couscous", "polenta", "noodles", "pasta", "dumplings", "gnocchi")

_POT = ("soup", "soups", "stew", "stews", "sauce", "sauces", "curry", "curries",
        "casserole", "casseroles", "gravy", "chilli", "broth", "daal", "dhal")


def _heavy(memory, understood):
    words = [str(word).lower() for word in ((understood or {}).get("words") or [])]
    if any(_same_word(word, wanted) for word in words
           for wanted in _POT):
        return None
    if any(_same_word(word, wanted) for word in words
           for wanted in ("mash", "mashed potato", "mashed potatoes", "potato", "potatoes")):
        return ("Heavy mash is wet potatoes and too much mashing: drain them well, let the steam off "
                "for a minute, mash them hot with warm milk and butter, and stop as soon as they are "
                "smooth. If it is already heavy, beat in a spoon of warm milk or a knob of butter and "
                "serve it at once.")
    if any(_same_word(word, wanted) for word in words for wanted in _STARCH):
        return ("Stodgy rice, porridge or couscous is too much water and too much stirring: use less "
                "liquid than the packet says, stop stirring once it is in the pan, and let it stand "
                "off the heat for 5 minutes so the starch sets before you serve it.")
    return ("Bread and cakes go heavy when the raising agent is stale, the mix is overworked or "
            "the oven is too cool: check the date on the powder, fold rather than beat, and give "
            "the oven 20 minutes to heat properly.")


_GLUE = (
    ("mash", "mashed potato", "mashed potatoes", "potato", "potatoes"),
    ("pasta", "penne", "spaghetti", "rigatoni", "macaroni", "fusilli", "tagliatelle", "farfalla"),
    ("noodle", "noodles", "udon", "ramen", "rice noodle", "rice noodles"),
    ("couscous", "bulgur", "bulghur", "quinoa", "polenta"),
)


_MUSHY_WORDS = ("mushy", "soggy", "overcooked", "over cooked", "over-cooked", "squashy")

_MUSHY_FIX = {
    "risotto": ("Risotto goes to porridge when it takes too much stock or too much stirring: add "
                "the stock a ladleful at a time and stir only enough to stop it catching, and take "
                "it off while the grains still have a chalky line through the middle. If it has "
                "already gone soft, beat in a knob of cold butter and the parmesan off the heat "
                "and serve it straight away - it will not come back, but it will taste right."),
    "mash": ("Mushy potatoes were boiled too long, or they are a waxy salad potato that goes to "
             "paste: use a floury one like Maris Piper or King Edward, drain the water the moment a "
             "knife slides in, let the steam off for a minute, and mash with warm milk and butter. "
             "Potatoes already sitting in water keep softening, so drain them as soon as they are "
             "done."),
    "rice": ("Soggy rice took too much water, not too little: 1 part rice to 1.5 parts water, the "
             "lid on and no stirring at all, then take it off the heat and let it stand 5 minutes "
             "with the lid on so the last of the water is taken up. Long grain and basmati want less "
             "water than pudding rice, and rinsing the rice first stops the outside going pasty."),
    "grain": ("Soggy couscous or quinoa took too much water: pour boiling water or stock over it in "
              "a wide bowl, 1 part to 1.5 for couscous and 1 to 2 for quinoa and bulgur, cover it "
              "and leave it 5 minutes, then fork it through. Polenta wants 1 part to 4 of liquid, "
              "stirred for 5 minutes and then left to set."),
    "porridge": ("Mushy porridge is too much water and too long in the pan: use 1 part oats to 2.5 "
                 "parts liquid for rolled oats, stir it now and then, and take it off while it is "
                 "still a little looser than you want it, because it thickens as it stands. Never "
                 "drain porridge: loosen it with a splash more milk or water."),
    "bake": ("Mushy is the wrong word for a bake, but it means the same thing: too much liquid or "
             "not long enough in the oven. Put it back at 160C (140C fan) for 10 minutes with foil "
             "loosely over the top so the middle catches up without the crust burning, and test it "
             "with a skewer - damp crumbs, not wet mixture. Bread that is doughy in the middle wants "
             "10 more minutes at 200C and a tap on the base for a hollow sound."),
    "sauce": ("A mushy sauce has too much water in it, not too little: take the lid off, keep it at a "
              "gentle simmer and let it reduce until it coats the back of a spoon, then taste it for "
              "salt, because reducing concentrates that too. A soup that was meant to be thick is "
              "better finished with a handful of rice or a spoon of flour slaked in cold water than "
              "with more time on the heat."),
    "": ("Mushy means too much water and too long in it, whatever the food is: take it off the heat "
         "while it still has some bite and get it out of the water rather than letting it sit. Tell "
         "me what it is - a bake, a grain, a sauce - and I can be exact about the next step."),
}


def _gluey(memory, understood):
    words = [str(word).lower() for word in ((understood or {}).get("words") or [])]
    mushy = any(_same_word(word, wanted) for word in words for wanted in _MUSHY_WORDS)
    if mushy:
        if any(_same_word(word, wanted) for word in words
               for wanted in ("mash", "mashed potato", "mashed potatoes", "potato", "potatoes")):
            return _MUSHY_FIX["mash"]
        if any(_same_word(word, wanted) for word in words
               for wanted in ("bread", "cake", "sponge", "loaf", "loaves", "muffin", "muffins",
                              "brownie", "brownies", "pastry", "bun", "buns", "scone", "scones")):
            return _MUSHY_FIX["bake"]
        if any(_same_word(word, wanted) for word in words
               for wanted in ("risotto", "risotto rice", "paella")):
            return _MUSHY_FIX["risotto"]
        if any(_same_word(word, wanted) for word in words
               for wanted in ("sauce", "gravy", "curry", "soup", "stew", "custard", "bolognese")):
            return _MUSHY_FIX["sauce"]
        if any(_same_word(word, wanted) for word in words for wanted in ("rice", "risotto")):
            return _MUSHY_FIX["rice"]
        if any(_same_word(word, wanted) for word in words
               for wanted in ("couscous", "bulgur", "bulghur", "quinoa", "polenta")):
            return _MUSHY_FIX["grain"]
        if any(_same_word(word, wanted) for word in words
               for wanted in ("porridge", "oats", "oatmeal", "porage")):
            return _MUSHY_FIX["porridge"]
        return _MUSHY_FIX[""]
    have = any(any(_same_word(word, wanted) for wanted in group) for group in _GLUE for word in words)
    if not have:
        return ("Gluey starch is nearly always too much water and too much stirring: stop stirring "
                "it, drain off any water it is still sitting in as soon as a piece is tender, and "
                "let it stand off the heat for a minute before you serve it.")
    if any(_same_word(word, wanted) for word in words
           for wanted in ("mash", "mashed potato", "mashed potatoes", "potato", "potatoes")):
        return ("Mash goes gluey when it is mashed too long, or the potatoes went in wet: drain them "
                "well and let the steam off for a minute, mash while they are hot with warm milk and "
                "butter rather than cold, and stop as soon as it is smooth. A gluey mash that is "
                "already made comes back if you beat in a spoon of warm milk and serve it at once, "
                "but never put it in a food processor.")
    if any(_same_word(word, wanted) for word in words
           for wanted in ("noodle", "noodles", "udon", "ramen", "rice noodle", "rice noodles")):
        return ("Noodles clump when they are boiled in a small pan and then left to sit: give them a "
                "big pan of boiling water, stir them apart in the first minute, and rinse them under "
                "warm water once they are drained if you are not serving them at once. A drop of oil "
                "in the water does nothing.")
    if any(_same_word(word, wanted) for word in words
           for wanted in ("couscous", "bulgur", "bulghur", "quinoa", "polenta")):
        return ("This one wants less water and a fork, not a spoon: pour boiling water or stock over "
                "it in a wide bowl, 1 part to 1.5 parts for couscous and 1 to 2 for quinoa, cover it "
                "and leave it 5 minutes, then fork it through to break the lumps. Stirring it while it "
                "soaks is what makes it claggy.")
    return ("Sticky pasta is a starch coating, not a cooking fault: use a big pan with plenty of "
            "water, stir it for the first minute so the pieces separate, and drain it but do not "
            "rinse it unless it is for a cold salad. If it has already clumped, a spoon of the "
            "cooking water tossed through it loosens it again.")


_TOUGH_BAKE = ("A tough or chewy bake has been mixed too much or has been in a little too long: "
               "stir only until the flour disappears and fold rather than beat, and weigh the "
               "butter and sugar rather than eyeballing them. If it is the oven, take the next "
               "batch out 2 minutes earlier - biscuits and meringues go chewy as they dry out, "
               "and a bake that is already tough is better eaten warm with butter or cream.")

_DRY_BAKE = ("A dry bake has been in the oven too long, or has more flour in it than the recipe "
             "meant: ovens run 10 to 20C hot or cold, so check it 5 minutes before the time and "
             "take it out while the middle is still a shade soft, and weigh the flour rather "
             "than using a cup. One that has already dried out is better eaten warm with butter, "
             "cream or fruit than thrown away.")

_GRAINY = (
    (("mash", "mashed potato", "mashed potatoes", "potato", "potatoes"),
     "grainy-mash"),
    (("hummus", "houmous", "humus", "dip", "dips", "smoothie", "pesto", "soup", "soups"),
     "grainy-blend"),
    (("custard", "cream", "creme fraiche", "yoghurt", "yogurt", "hollandaise",
      "mayonnaise", "mayo"),
     "grainy-curdle"),
    (("polenta", "couscous", "porridge", "oats", "oatmeal", "semolina", "grits"),
     "grainy-grain"),
)

_GRAINY_FIX = {
    "grainy-mash": ("Grainy mash is the potato and the tool, not the butter: a floury potato mashed "
                    "while it is cold, or a masher that works it into paste. Drain them the moment "
                    "a knife slides in, let the steam off for a minute, put them through a ricer "
                    "or a sieve rather than mashing hard, and beat in warm milk and butter off the "
                    "heat. Once it is grainy, warm milk and a good beat will loosen it, but a food "
                    "processor will only make it worse."),
    "grainy-blend": ("A grainy blend stopped too soon or has too little fat in it: blend it 3 to 4 "
                     "minutes rather than 30 seconds, scrape the sides down twice, and add the oil or "
                     "tahini in a thin stream while the motor runs. A spoon of iced water loosens a "
                     "thick hummus far better than more oil. Chickpea skins and tomato skins are the "
                     "other half of it, so push it through a sieve if it still feels rough."),
    "grainy-curdle": ("Grainy custard, cream or mayonnaise has curdled: the eggs or the fat got too "
                      "hot, or acid went in too fast. Everything you make this way wants low heat and "
                      "a bowl over simmering water, not a pan on the ring. To rescue a curdled one, "
                      "take it off the heat and whisk in a spoonful of cold milk or cream it has not "
                      "split yet - and a graininess you can taste rather than see is usually salt, "
                      "sugar or an over-tight emulsion, not heat."),
    "grainy-grain": ("Grainy polenta, couscous or porridge is lumps of dry grain that never took up "
                     "water: rain it into boiling liquid in a thin stream while you whisk, instead of "
                     "tipping it in and stirring after. Polenta wants 1 part to 4 of liquid and 5 "
                     "minutes of stirring; couscous wants boiling water poured over it, a lid and a "
                     "fork, never a spoon. Any lumps left at the end go through a sieve or get "
                     "whisked out with a little more hot liquid."),
    "": ("Grainy means the texture broke up instead of holding together, and what to do depends on "
         "what broke: meat that steamed instead of browning wants a hotter pan and less stirring, "
         "mashed or blended food wants a gentler tool and more fat, and eggs or cream that went "
         "grainy have curdled and are already cooked. Tell me which dish it is and I can be exact."),
}


def _fault_groups(memory, understood, groups):
    said = [str(word).lower() for word in ((understood or {}).get("words") or [])]
    for names, key in groups:
        if any(_same_word(word, wanted) for word in said for wanted in names):
            return key
    if not _names_food(_line_text(understood)):
        return None
    return ""


def _grainy(memory, understood):
    key = _fault_groups(memory, understood, _GRAINY)
    return None if key is None else _GRAINY_FIX[key]


_LUMPY = (
    (("polenta", "couscous", "porridge", "oats", "oatmeal", "semolina", "grits", "mash",
      "mashed potato", "mashed potatoes", "potato", "potatoes"), "lumpy-starch"),
    (("custard", "cream", "sauce", "sauces", "gravy", "roux", "cheese sauce", "white sauce",
      "batter", "pancakes", "pancake", "yorkshire"), "lumpy-liquid"),
    (("hummus", "houmous", "humus", "dip", "dips", "pesto", "smoothie"), "lumpy-blend"),
)

_LUMPY_FIX = {
    "lumpy-starch": ("Lumps in porridge, polenta, couscous or mash are dry grain or dry potato that "
                     "never took up liquid: tip the grain into the liquid in a thin stream while you "
                     "whisk, rather than adding the liquid to the grain, and stir the bottom of the "
                     "pan as it comes up to the boil. A mash goes lumpy when it is mashed cold or "
                     "with thin liquid: warm it through with a splash of hot milk and put it through "
                     "a sieve, which takes out every lump in one go."),
    "lumpy-liquid": ("A lumpy sauce is flour that cooked before it met the liquid, or liquid that "
                     "went in faster than the whisk could follow: slake the flour or cornflour in "
                     "cold water first, add the hot liquid in a thin stream, and keep the whisk flat "
                     "on the bottom of the pan where the flour settles. Off the heat, a hard whisk "
                     "and a sieve rescue a sauce that has already lumped - or strain it, put it back "
                     "on the heat and start the thickening again with fresh roux, which is quicker "
                     "than fighting the lumps."),
    "lumpy-blend": ("Lumps in a blend are too little liquid under the blade and too short a run: add "
                    "the liquid first, blend 2 to 3 minutes and scrape down twice, and thin it with "
                    "iced water rather than oil. Anything with skins in it - chickpeas, tomatoes, "
                    "nuts - will stay rough until it goes through a sieve."),
    "": ("Lumpy food is dry powder or cold fat that met hot liquid too fast: mix the starch with cold "
         "water first, add it in a thin stream while you whisk, and keep the whisk flat on the "
         "bottom of the pan. Off the heat, whisk it hard and push it through a sieve. Tell me which "
         "dish it is and I can say what went wrong in that one."),
}


def _lumpy(memory, understood):
    key = _fault_groups(memory, understood, _LUMPY)
    return None if key is None else _LUMPY_FIX[key]


PROBLEMS = {
    "grainy": (
        ("grainy", "grainy texture", "gone grainy", "went grainy", "tastes grainy"),
        _grainy,
        {"spag-bol": ("Grainy bolognese is the mince rather than the tomato: mince that goes into a "
                      "cool pan and is stirred at once steams in its own juice and breaks into "
                      "little grey grains. Get the pan properly hot, brown it in two batches and "
                      "leave the first minute alone before you stir, tip off the fat, then reduce a "
                      "glass of wine and 100ml of milk in it before the tomatoes go in. A sauce "
                      "that has already gone grainy comes back with a long bare simmer - 2 to 3 "
                      "hours, lid off - and a sieve takes out the skin and seed if that is what is "
                      "roughening it.")}),
    "lumpy": (
        ("lumpy", "lumps", "all lumps"),
        _lumpy,
        {}),
    "dry": (
        ("dry", "dries", "overcooked", "over cooked", "over-cooked", "too long", "ruined"),
        ("Nearly always the time, not the temperature: take it out 5 minutes earlier than you "
         "think, cover it with foil and let it rest 10 minutes. It carries on cooking off the "
         "heat and the juices settle back into the meat."),
        {"roast-chicken": ("Cook it to 74C in the thickest part of the thigh and no further: "
                           "cover the bird with foil once the skin is brown so the breast does "
                           "not dry out while the thighs finish, and rest it 15 minutes."),
         "chicken-thighs": ("Thighs dry out when they are skinless or crowded on the tray: keep "
                            "the skin on, leave a gap between them, and take them out at 74C "
                            "rather than giving them another ten minutes to be safe."),
         "chicken-breast": ("Breasts are the easiest thing to overcook: flatten them to an even "
                            "thickness with the heel of your hand, roast 18 to 20 minutes at "
                            "200C, and rest 5 minutes before slicing."),
         "salmon": ("Salmon dries out in a hot oven: 12 to 15 minutes at 180C is enough for a "
                    "fillet, and it is done when the white lines between the flakes just start "
                    "to show. Take it out looking slightly underdone."),
         "cake": ("A dry sponge means too long in the oven or too much flour: check 5 minutes "
                  "early with a skewer, weigh the flour rather than using a cup, and soak the "
                  "cake with a little syrup if it has already gone dry."),
         "sausages": ("Sausages dry out when they are pricked or cooked too fast: keep them "
                      "whole, cook them 25 to 30 minutes at 180C, and turn them once."),
         **{bake: _DRY_BAKE for bake in ("scones", "muffins", "biscuits", "meringues",
                                         "yorkshire-puddings")}}),
    "tough": (
        ("tough", "chewy", "leathery", "like shoe"),
        ("Tough meat is usually cooked too fast or too briefly: give it longer at a lower heat "
         "with a splash of liquid, and slice it across the grain."),
        {"steak": ("Steak goes tough when it is cold in the pan or cooked past medium: take it "
                   "out of the fridge 20 minutes before, dry it, sear it in a very hot pan 2 "
                   "minutes a side, then rest it 5 minutes and slice across the grain."),
         "roast-chicken": ("A bird cooked too fast goes tough outside and raw in: 190C for 20 "
                           "minutes per 500g plus 20, then rest it 15 minutes before carving."),
         "stew": ("A tough stew is an underdone one, not an overcooked one: another 30 to 45 "
                  "minutes at a bare simmer with the lid on, and top the liquid up if it is low. "
                  "A simmer that is really a boil tightens the meat instead of softening it."),
         **{bake: _TOUGH_BAKE for bake in ("cake", "scones", "muffins", "biscuits", "meringues",
                                           "yorkshire-puddings")}}),
    "soggy": (
        ("soggy", "limp", "not crisp", "not crispy", "wont crisp", "won't crisp"),
        ("Soggy means too much water, and what to do depends on the food. Pasta, noodles and "
         "rice are simply overcooked: drain them the moment they are tender and get the sauce in "
         "straight away so they cannot sit wet. Roast things need one layer with space between "
         "them, the oil hot before they go in and the oven door shut. A bake that is soggy in the "
         "middle went in too wet or came out too soon: back it at 160C for 10 minutes under foil."),
        {"cake": ("A soggy cake is underbaked or wetter than the recipe meant: put it back at "
                  "160C for 10 minutes with foil over the top, and next time weigh the milk and "
                  "butter and test with a skewer - it wants crumbs, not batter. A soggy bottom "
                  "is the tin on a cold shelf: bake one shelf up, or slide a tray under it."),
         "bread": ("Soggy bread is underbaked or was cut while it was hot: stand the loaf out of "
                   "its tin for another 10 minutes at 200C, and cool it on a rack, because a loaf "
                   "cut warm steams itself and goes doughy."),
         "pastry": ("A soggy pastry base is a wet filling or an oven that was not hot enough: "
                    "blind bake it 15 minutes at 200C with paper and beans, then brush the base "
                    "with beaten egg and give it 5 minutes more."),
         "biscuits": ("Soggy biscuits are underbaked or were left in the tin: give them 2 more "
                      "minutes at 180C, then 5 minutes in the tin and the rest on a rack - they "
                      "firm as they cool."),
         "roast-potatoes": ("Soggy potatoes are usually parboiled too long or put in cold oil: "
                            "8 minutes in boiling water, drain and shake them rough, then into "
                            "a thin layer of hot oil at 200C and do not crowd the tin."),
         "roast-vegetables": ("Wet vegetables steam instead of roasting: dry them, toss in oil, "
                              "and spread them in a single layer with room between them.")}),
    "dense": (
        ("dense", "heavy", "sank", "stodgy", "sink", "sinks", "sinking"),
        _heavy,
        {"bread": ("Dense bread is usually under-proved or over-kneaded: let the shaped loaf "
                   "double somewhere warm, and use a thermometer on the water — yeast wants "
                   "blood heat, not hot."),
         "cake": ("A cake sinks when the oven door is opened early or the raising agent is too "
                  "much: bake at 180C without opening the door for the first 20 minutes, and "
                  "check with a skewer at the earliest time in the recipe.")}),
    "bland": (
        ("bland", "tasteless", "no flavour", "no flavor", "boring", "nothing taste"),
        ("Bland food is nearly always short of salt and acid rather than spices: a good pinch "
         "of salt, a squeeze of lemon or a splash of vinegar lifts it more than another spoon "
         "of spice."),
        {"curry": ("Taste the curry for salt first, then add a squeeze of lemon or a spoon of "
                   "yoghurt; if it still tastes thin, fry the spices in oil at the start for "
                   "30 seconds and let the sauce reduce uncovered for 5 minutes."),
         "roast-vegetables": ("Vegetables taste flat when they are crowded and pale: give them "
                              "room, roast until the edges colour, and salt them as they come "
                              "out of the oven.")}),
    "sticky": (
        ("sticky", "gluey", "mushy", "claggy", "stodgy rice"),
        _gluey,
        {"curry": ("Rice under a curry goes sticky when it is stirred while it cooks: rinse it, "
                   "bring it to a simmer, put the lid on and leave it alone for 12 minutes."),
         "bread": ("Sticky dough is nearly always wet dough: add strong white flour a spoonful "
                   "at a time and knead it in for a minute before judging, because dough firms "
                   "as it rests. Wet your hands rather than flouring them to shape it, and give "
                   "it 20 minutes covered - a slack dough that has rested handles far better.")}),
    "watery": (
        ("watery", "runny sauce", "too thin", "thin sauce", "sauce is runny"),
        ("Watery sauce is a sauce that has not had time to reduce: simmer it uncovered for 5 to "
         "10 minutes, or stir in a teaspoon of cornflour slaked in cold water."),
        {"curry": ("Simmer the curry uncovered for 10 minutes to reduce it, or stir in a spoon "
                   "of tomato puree; a spoon of yoghurt at the end thickens it without flour."),
         "fish-pie": ("A watery fish pie is a filling that went on warm or thin: poach the fish in "
                      "milk, use 40g each of butter and flour to 500ml of that milk, and let it "
                      "cool right down before the mash goes on.")}),
}


VEG_FAMILIES = (
    (("green beans", "runner beans", "broad beans", "french beans", "beans", "mangetout",
      "sugar snap", "sugar snaps", "peas"),
     "Beans go tough when they are old or undercooked: top and tail them, pull the string down "
     "the seam of runners, and boil 4 to 5 minutes in salted water. Peas and mangetout need 2 "
     "minutes at most, and a minute in a hot pan at the end brings the bite back."),
    (("cabbage", "sprouts", "sprout", "broccoli", "cauliflower", "romanesco", "kalettes",
      "spring greens", "leafy greens", "collard greens", "mixed greens", "collard", "pak choi",
      "bok choy", "broccolini", "savoy", "spring cabbage"),
     "Slice it thinner and give it longer: a brassica goes tough when the stalk is undercooked, "
     "so cut a cross in the stalk or slice it thin and steam 5 to 8 minutes, until a knife "
     "slides in. If it has turned grey and sulphury it is overcooked instead, so give it two "
     "minutes less next time."),
    (("carrot", "carrots", "parsnip", "parsnips", "swede", "turnip", "turnips",
      "beetroot", "celeriac", "sweet potato", "sweet potatoes", "jerusalem artichoke"),
     "Roots go hard in the middle when the pieces are uneven: cut them no bigger than a thumb, "
     "start them in cold salted water and simmer 15 to 20 minutes, or roast them covered in foil "
     "first. If the core is woody, cut it out - an old carrot or parsnip will not soften however "
     "long it cooks."),
    (("kale", "cavolo nero", "chard", "spinach"),
     "Strip the leaves off the stalks, because the stalk is what stays tough: steam the leaves 3 "
     "to 4 minutes, or rub kale with oil and salt for a minute to soften it for a salad without "
     "any heat."),
    (("aubergine", "aubergines", "courgette", "courgettes", "zucchini", "pepper",
      "peppers", "squash", "pumpkin", "fennel", "okra", "tomato", "tomatoes"),
     "Give it longer in a hot oven, 200C, until it collapses and the edges colour: these are "
     "mostly water, so they taste raw and squeaky until that water cooks out. Salt aubergine "
     "and courgette first and dry them, and spread them out so they roast rather than steam."),
    (("leek", "leeks", "celery", "onion", "onions", "spring onion", "spring onions",
      "shallot", "shallots"),
     "Slice it thinner and cook it slower: leeks, onions and celery stay tough when they go into "
     "a dry pan over high heat, so give them a knob of butter, a splash of water and a lid for 10 "
     "minutes. Only the dark green tops of a leek are tough enough to keep back - put those in a "
     "stock instead."),
    (("vegetables", "veg", "veggies", "root veg", "roast veg", "stir fry veg",
      "mixed veg", "ratatouille"),
     "Cut it into even pieces, no thicker than a finger, and give it longer: a tough vegetable "
     "is nearly always undercooked in the middle. Salted water for boiling, 200C in a single "
     "layer for roasting, and a knife should slide in before it comes off the heat."),
)

VEG_NAMES = tuple(name for names, _fix in VEG_FAMILIES for name in names) + (
    "potato", "potatoes", "new potatoes", "jacket potato", "jacket potatoes",
    "baked potato", "baked potatoes", "mushroom", "mushrooms")


VEG_FAULTS = ("tough", "tougher", "hard", "harder", "still hard", "too hard",
              "undercooked", "under cooked", "under-done", "not cooked", "not soft",
              "woody", "stringy", "squeaky", "chewy", "raw", "firm", "rubbery")


def _veg_fix(text):
    if not isinstance(text, str) or not text:
        return None
    if not any(_phrase_in(text, fault) for fault in VEG_FAULTS):
        return None
    if any(_phrase_in(text, whole) for whole in ("jacket potato", "baked potato",
                                                 "jacket potatoes", "baked potatoes")):
        return ("A jacket potato is hard in the middle because it was rushed: prick it, "
                "microwave it 8 to 10 minutes until a knife goes in, then 15 to 20 minutes at "
                "200C to crisp the skin. In the oven alone it needs an hour and a quarter at "
                "200C, so give it that long or start it early.")
    if any(_phrase_in(text, word) for word in ("potato", "potatoes", "new potatoes")):
        if any(_phrase_in(text, word) for word in ("roast", "roasted", "roasting", "oven",
                                                   "crispy", "tray")):
            return ("Hard roast potatoes went in too big or came out too early: give them another "
                    "10 to 15 minutes at 200C, and next time cut them no bigger than a golf ball "
                    "and parboil them 8 minutes first, which is what cooks the middle before the "
                    "outside crisps.")
        return ("Boiled potatoes go hard in the middle when the pieces are uneven: cut them the "
                "same size, start them in cold salted water and simmer 15 to 20 minutes, until a "
                "knife slides in. An old potato can be woody at the core, and that will not "
                "soften however long it cooks.")
    if any(_phrase_in(text, word) for word in ("mushroom", "mushrooms")):
        return ("Rubbery mushrooms have been steamed rather than fried: they hold a lot of water, "
                "so give them a wide hot pan with a little oil, one layer and no lid, and let that "
                "water cook off before you turn them. A pinch of salt only at the end, or they "
                "give up their water early and stew.")
    if any(_phrase_in(text, word) for word in ("dried", "haricot", "haricots", "cannellini",
                                               "borlotti", "butter bean", "butter beans",
                                               "chickpea", "chickpeas", "split peas", "lentil",
                                               "lentils", "puy")):
        return None
    for names, fix in VEG_FAMILIES:
        for name in names:
            if _phrase_in(text, name):
                return fix
    return None


_SINK_VERBS = ("sink", "sinks", "sinking")
_SINK_AS_A_BAKE = ("bread", "breads", "loaf", "loaves", "cake", "cakes", "sponge", "sponges",
                   "bun", "buns", "roll", "rolls", "muffin", "muffins", "scone", "scones",
                   "souffle", "soufflé", "yorkshire", "dough", "batter", "pastry", "bake",
                   "bakes", "baked", "baking", "oven", "risen", "proved")


def _a_sink_is_a_bake(text):
    low = (text or "").lower()
    return any(_phrase_in(low, word) for word in _SINK_AS_A_BAKE)


_PLAN_THAT_MIGHT_BE_RUINED = re.compile(
    r"\b(?:does|do|will|would|can|could|might|may|shall|should)\s+"
    r"(?:that|this|it|they|these|those)\s+"
    r"(?:ruin|ruins|spoil|spoils|wreck|wrecks)\b", re.I)

_ASKED_ABOUT_THE_FAULT = re.compile(
    r"\b(?:why|how come|what went wrong|what did i do wrong|how do i stop|how can i stop)\b",
    re.I)


def a_plan_that_might_be_ruined(understood):
    if not isinstance(understood, dict):
        return True
    text = str(understood.get("plain") or understood.get("clean") or understood.get("text")
               or "")
    if _ASKED_ABOUT_THE_FAULT.search(text):
        return True
    return _PLAN_THAT_MIGHT_BE_RUINED.search(text) is None


def problem_in(text):
    for key, (words, _general, _by_dish) in PROBLEMS.items():
        for word in words:
            if word in _SINK_VERBS and not _a_sink_is_a_bake(text):
                continue
            if _phrase_in(text, word):
                return key
    return None


FOOD_WORDS = (
    "rice", "chips", "chip", "fries", "pasta", "spaghetti", "noodles", "gravy", "sauce", "soup",
    "stew", "casserole", "pie", "pizza", "egg", "eggs", "omelette", "bacon", "tofu", "quinoa",
    "couscous", "porridge", "mash", "burger", "burgers", "kebab", "fish", "lamb", "pork",
    "turkey", "mushroom", "mushrooms", "beans", "cabbage", "carrot", "carrots", "broccoli",
    "peas", "spinach", "pancakes", "biscuits", "cookies", "brownies", "pastry", "batter",
    "stock", "yorkshire", "mince", "bolognese", "chilli", "meat", "pudding",
    "custard", "jam", "sourdough", "dough", "buns", "loaf",
    "risotto", "polenta", "semolina", "grits", "hummus", "houmous", "roux", "mash",
)


_A_STATE_VERB = re.compile(r"\b(?:is|are|was|were|be|been|gets?|got|gotten|tastes?|seems?|"
                           r"looks?|feels?|sounds?|smells?)\b", re.IGNORECASE)

NOT_THE_FOOD = frozenset("""
soil compost ground earth dirt air weather room house home flat kitchen garden lawn grass plant
plants leaves leaf stem stems root roots skin hair hands hand face lips feet foot pan tray tin
oven hob grill fridge freezer sink washing clothes towel floor worktop counter table shelf
radiator boiler heating window windowsill sill dish dishes plate plates bowl bowls
""".split())

_STANDS_FOR_IT = frozenset("it its they them this that these those one ones".split())


def _the_subject_of_the_state(text, word):
    low = text.lower()
    found = re.search(r"\b" + re.escape(word.lower()) + r"\b", low)
    if not found:
        return []
    before = low[:found.start()]
    clause = re.split(r"[,.;:!?]|\band\b", before)[-1]
    words = clause.split()
    verbs = [i for i, one in enumerate(words) if _A_STATE_VERB.fullmatch(one)]
    if not verbs:
        return []
    subject = [one for one in words[:verbs[-1]] if one.isalpha()]
    return subject[-2:]


def _the_state_is_about_the_food(text, key):
    words, _general, _by_dish = PROBLEMS[key]
    for word in words:
        subject = _the_subject_of_the_state(text, word)
        if not subject:
            continue
        if any(one in _STANDS_FOR_IT for one in subject):
            return True
        if any(_same_word(one, not_food) for one in subject for not_food in NOT_THE_FOOD):
            return False
        return True
    return True


def _names_food(text):
    return any(_same_word(word, food) for word in tokens(text) for food in FOOD_WORDS)


_COOK_PHRASES = ("what can i make", "what can i do with", "what should i make", "what do i do with",
            "what to make", "what to do with", "make with", "made with", "do with", "use up",
            "using up", "recipe", "recipes", "cook", "cooking", "eat", "eating", "dinner",
            "lunch", "supper", "tea", "meal", "meals", "meal idea", "leftover", "leftovers",
            "left over", "something quick", "something easy")


def cook_ask(understood):
    text = ((understood or {}).get("norm_text") or (understood or {}).get("clean") or "").lower()
    if not any(word in text for word in _COOK_PHRASES):
        return False
    return any(food in text for food in FOOD_WORDS)


def _problem(memory, understood):
    text = ""
    if isinstance(understood, dict):
        text = understood.get("norm_text") or understood.get("clean") or ""
    key = problem_in(text)
    if key and not _the_state_is_about_the_food(text, key):
        return None
    if not key:
        for earlier in recent_texts(memory)[:2]:
            key = problem_in(earlier)
            if key and not _the_state_is_about_the_food(earlier, key):
                key = None
                continue
            if key:
                break
    if not key:
        return _veg_fix(text)
    words, general, by_dish = PROBLEMS[key]
    dish = dish_for(memory, understood)
    if dish in by_dish:
        return by_dish[dish]
    if dish is None and not any(_names_food(one) for one in [text] + recent_texts(memory)[:2]):
        return None
    veg = _veg_fix(text)
    if veg:
        return veg
    if callable(general):
        return general(memory, understood)
    return general


PLAIN = {"temp", "time"}

PART = {"skin", "stuffing", "frosting"}


DONE_ASK = re.compile(r"\b(?:is|are|are'?nt|aren't|isnt|isn't)\s+"
                      r"(?:my|the|our|it|they|these|those|this|that)\b"
                      r"[^?.!]{0,40}?\b(?:done|ready|cooked|through)\b", re.I)

DONE_VERB_ASK = re.compile(r"\b(?:tell|know|check|test|see)\b[^?.!]{0,40}?"
                           r"\b(?:is|are|its|it's)\s+(?:done|ready|cooked|through)\b", re.I)


DONE_POSSESSIVE = ("is my", "is the", "is our", "is it", "is this", "is that",
                   "are my", "are the", "are our", "are they", "are these", "are those",
                   "isnt my", "isn't my", "arent the", "aren't the", "is my dish")
DONE_WORD = ("done", "ready", "cooked", "through")


_ASK_NOISE = frozenset("""a an the my our your his her their its it they them these those this that
    is are was were be been being isn t isn't arent aren't not
    i we you he she they should shall can could would do does did know tell check test see
    if whether when how what which that so yet still actually really even just about
    left enough thorough properly all way to""".split())

_GENERIC_SUBJECT = frozenset("""dish food meal dinner tea supper lunch breakfast thing stuff
    one ones piece bit pan pot oven""".split())


_ANY_FOOD = None


def _any_food():
    global _ANY_FOOD
    if _ANY_FOOD is None:
        _ANY_FOOD = tuple(sorted(set(PLAN_NAMES) | set(FOOD_WORDS) | set(DISH_WORDS)))
    return _ANY_FOOD


def _asks_doneness(text):
    said = str(text or "")
    match = DONE_ASK.search(said) or DONE_VERB_ASK.search(said)
    if not match:
        return False
    span = match.group(0).lower()
    if _ready_food(span):
        return True
    if any(_phrase_in(span, name) for name in _any_food()):
        return True
    subject = [word for word in re.findall(r"[a-z']+", span)
               if word not in _ASK_NOISE and word not in DONE_WORD]
    return all(word in _GENERIC_SUBJECT for word in subject)

MAKING_A_FAULT = re.compile(
    r"\b(?:make|making|made|cook|cooking|cooks|roast|roasting|bake|baking|baked|fry|frying|"
    r"fried|grill|grilling|boil|boiling|simmer|simmering)\b[^?.!]{0,60}?"
    r"\b(?:hard|harder|stale|soggy|dry|tough|rubbery|mushy|burnt)\b", re.I)


def ask_kind(understood):
    if not isinstance(understood, dict):
        return None
    text = understood.get("norm_text") or understood.get("clean") or ""
    have = tokens(text)
    if not have:
        return None
    said = str(text)
    ready = 6 if _asks_doneness(said) else 0
    keeps = 6 if KEEP_ASK.search(str(text)) else 0
    making_a_fault = bool(MAKING_A_FAULT.search(str(text)))
    best, best_rank = None, (0, 0)
    for kind, asks, helpers in ASK_KINDS:
        score = 0
        for ask in asks:
            if _phrase_in(text, ask):
                score += 2 + len(tokens(ask))
                break
        if kind == "done" and ready:
            score = max(score, ready)
        if kind == "keep" and keeps:
            score = max(score, keeps)
        if not score:
            continue
        if any(_same_word(word, helper) for word in have for helper in helpers):
            score += 1
        if kind == "keep" and making_a_fault:
            continue
        rank = (2 if kind in PART else 0 if kind in PLAIN else 1, score)
        if rank > best_rank:
            best, best_rank = kind, rank
    return best


KEEP_ASK = re.compile(
    r"\bhow long (?:does|do|will|can|would)\s+(?:\w+\s+){0,4}(?:last|keep)\b"
    r"|\bhow (?:do|can|should|would) (?:i|you|we) keep (?:\w+\s+){0,4}"
    r"(?:fresh|good|from going (?:stale|hard|soft))\b",
    re.I)

TIME_IN_ANSWER = re.compile(r"\b(\d{1,3})\s*(?:to\s*\d{1,3}\s*)?(minute|hour)", re.I)


KEEPING_LEAD = ("within", "after", "up to", "keep", "keeps", "kept", "keeping", "freeze",
                "freezer", "fridge", "refrigerator", "cool", "store", "stored", "lasts",
                "left in", "left out", "use up")


def _first_minutes(text):
    if not isinstance(text, str):
        return None
    for found in TIME_IN_ANSWER.finditer(text):
        head = text[:found.start()].lower()[-30:]
        if any(word in head for word in KEEPING_LEAD):
            continue
        count = int(found.group(1))
        return count * 60 if found.group(2).lower().startswith("hour") else count
    return None


def _last_answer_said(memory):
    turns = memory.get("turns")
    if not isinstance(turns, list) or not turns or not isinstance(turns[-1], dict):
        return ""
    said = turns[-1].get("bot")
    return said if isinstance(said, str) else ""


def _plan_contradicts_the_last_answer(memory, plan):
    told = _first_minutes(_last_answer_said(memory))
    if told is None or not told:
        return False
    ours = _first_minutes(plan.get("time") or "")
    if ours is None or not ours:
        return False
    return max(told, ours) > 2 * min(told, ours)


PART_WORDS = ("frosting", "icing", "buttercream", "ganache", "filling", "stuffing", "skin")

PART_BACKREF = ("and", "also", "what about", "how about", "or", "same for", "what for")


def _parts_in(text):
    return {word for word in PART_WORDS if _phrase_in(text or "", word)}


def _answering_line(memory):
    turns = memory.get("turns")
    if not isinstance(turns, list):
        return ""
    for turn in reversed(turns):
        if isinstance(turn, dict) and isinstance(turn.get("user"), str):
            if turn["user"].strip():
                return turn["user"]
    return ""


def _same_answer_but_a_new_part(memory, understood, answer):
    if not answer:
        return None
    text = _line_text(understood)
    asked = _parts_in(text)
    if not asked or not any(_phrase_in(text, phrase) for phrase in PART_BACKREF):
        return None
    already = _parts_in(_answering_line(memory))
    if asked - already:
        part = sorted(asked - already)[0]
        return f"Same for the {part}: " + answer[0].lower() + answer[1:]
    if asked and not asked - already and not already:
        return None
    return None


def _dish_named_in_the_line(understood):
    if not isinstance(understood, dict):
        return None
    return dish_in(understood.get("norm_text") or understood.get("clean") or "")


_NAMES_A_SAUCE = re.compile(
    r"\b(sauce|sauces|gravy|jus|relish|chutney|coulis|compote|salsa|dressing)\b", re.I)


def reply(kind, memory, understood):
    key = dish_for(memory, understood)
    plan = PLANS.get(key) if key else None
    if plan is None:
        return None
    if _NAMES_A_SAUCE.search(str(_line_text(understood))):
        return None
    if (kind == "time" and not _dish_named_in_the_line(understood)
            and _plan_contradicts_the_last_answer(memory, plan)):
        return None
    if kind in PART_OF and any(_phrase_in(_line_text(understood), no) for no in PART_NOT):
        return None
    answer = plan.get(kind) or None
    if kind == "ahead" and not answer:
        answer = plan.get("keep")
    if answer and answer == _last_answer_said(memory):
        part = _same_answer_but_a_new_part(memory, understood, answer)
        if isinstance(part, str) and part.strip():
            return part
        return answer
    return answer


def _part_ahead(memory, understood):
    if dish_for(memory, understood) is not None:
        return None
    text = _line_text(understood)
    key = implied_dish(text)
    if key is None:
        return None
    if not any(_phrase_in(text, phrase) for phrase in IMPLIED_ASKS):
        return None
    plan = PLANS.get(key) or {}
    answer = plan.get("frosting") or plan.get("keep")
    if answer and answer == _last_answer_said(memory):
        return None
    return answer


_KEEP_BUT_COOKING = ("oven", "bake", "baking", "cook", "cooking", "roast", "fry", "frying",
                     "grill", "boil", "simmer", "reheat", "rest", "resting", "ahead",
                     "day before", "night before", "prepare",
                     "sink", "sinks", "sinking", "sank", "sunken", "soggy", "stick", "sticks",
                     "sticking", "curdle", "curdling", "split", "splitting", "burn", "burning",
                     "burnt", "collapse", "collapsing", "dry out", "going dry", "going hard",
                     "stale", "risen", "rise", "raising", "grey", "mushy", "raw")
_KEEP_ASK = re.compile(
    r"\b(?:keep|keeps|keeping|last|lasts|store|storing|stays good|freeze|freezer|"
    r"shelf[ -]life"
    r"|go off|goes off|going off|gone off)\b")


def _is_a_keeping_line(text):
    line = (text or "").lower()
    return bool(_KEEP_ASK.search(line)) and not any(w in line for w in _KEEP_BUT_COOKING)


PERSON_STATE = re.compile(
    r"^\s*(?:i|we)\s*(?:'m|'ve|'d| am| have| had| got| feel| was| were| keep| come|'s)\b"
    r"|^\s*(?:im|ive|i've|i'm)\s+\w", re.I)

PERSON_REST = re.compile(
    r"\bi\s+need\s+(?:to\s+(?:rest|lie|sleep|sit|stop|go\s+to\s+bed)"
    r"|a\s+(?:rest|break|nap|lie\s+down|sit\s+down))\b", re.I)

BODY_TEMPERATURE = re.compile(
    r"\b(?:has|have|had|having|got|getting|running|runs|comes? down with|down with|with)\s+"
    r"(?:a|the|any|another|high|slight)?\s*(?:temperature|temp|fever)\b"
    r"|\btemperature\s+of\s+\d|\bmy\s+(?:temp|temperature)\s+(?:is|was)\b", re.I)


def _about_a_person(text):
    line = text or ""
    return bool(PERSON_STATE.match(line) or BODY_TEMPERATURE.search(line)
                or PERSON_REST.search(line))


RAW_WORDS = ("raw", "undercooked", "underdone", "runny", "pink")


def _raw_in_flight(memory):
    for line in recent_texts(memory)[:3]:
        if any(_same_word(word, raw) for word in tokens(line) for raw in RAW_WORDS):
            return True
    return False


def _follow_up(memory, understood):
    line = _line_text(understood)
    if _about_a_person(line) and not (_dish_named_in_the_line(understood) or dish_in(line)):
        return None
    kind = ask_kind(understood)
    if kind == "keep" and _raw_in_flight(memory):
        return None
    if kind != "keep" and not _parts_in(_line_text(understood)) \
            and _is_a_keeping_line(_line_text(understood)):
        answer = reply("keep", memory, understood)
        if answer:
            return answer
    if kind == "fix":
        return _problem(memory, understood) or _part_ahead(memory, understood)
    answer = reply(kind, memory, understood) if kind else None
    if answer:
        return answer
    if kind == "done":
        ready = _ready_note(memory, understood)
        if ready:
            return ready
    return _part_ahead(memory, understood)


def follow_up(memory, understood):
    if not isinstance(memory, dict) or not isinstance(understood, dict):
        return None
    return _follow_up(memory, understood)


PLAN_NAMES = tuple(sorted({
    name for plan in PLANS.values() for group in plan.get("names", ()) for name in group}))


COOKING_WORDS = (
    "oven", "bake", "baking", "baked", "roast", "roasting", "roasted", "cook", "cooking",
    "cooked", "pan", "tray", "tin", "dish", "temperature", "degrees", "heat", "gas", "shelf",
    "kilo", "kilos", "kilogram", "kg", "gram", "grams",
    "fridge", "freezer", "freeze", "frozen", "reheat", "leftover", "leftovers", "skin",
    "skinless", "stuff", "stuffed", "stuffing", "rest", "resting", "sides", "side", "done",
    "raw", "pink", "juices", "crisp", "crispy", "brown", "boil", "simmer", "fry", "grill",
    "airfryer", "sauce", "gravy", "water", "ahead", "before", "frosting", "icing",
    "buttercream", "ganache", "filling", "recipe",
    "start to finish", "in the oven", "per kilo", "per kg", "the day before", "night before",
) + FOOD_WORDS + DISH_WORDS + PLAN_NAMES


def _temp_asks():
    asks, helpers = [], []
    for kind, parts, words in ASK_KINDS:
        if kind != "temp":
            continue
        for part in parts:
            if part not in asks:
                asks.append(part)
        for word in words:
            if word not in helpers:
                helpers.append(word)
    return tuple(asks), tuple(helpers)


_RECIPE_CARDS = (
    "biscuit", "biscuits", "cookie", "cookies", "shortbread", "flapjack", "flapjacks",
    "bread", "sourdough", "loaf", "loaves",
    "chilli con carne", "chilli", "chili",
    "chips", "oven chips", "frozen chips",
    "curry", "tikka", "korma",
    "fish pie",
    "gammon", "gammon steak", "gammon steaks",
    "meringue", "meringues", "pavlova",
    "pasta bake", "baked pasta",
    "pie", "pies", "apple pie", "fruit pie",
    "roast potatoes", "roast potato", "roasties",
    "scone", "scones", "fruit scone", "cheese scone",
    "spag bol", "spaghetti bolognese", "spaghetti bolognaise", "bolognese", "bolognaise",
    "beef stew", "stew", "casserole",
    "sunday roast", "roast dinner", "roast lunch")


def _the_heat(memory, understood):
    if ask_kind(understood) != "temp":
        return None
    if not _dish_named_in_the_line(understood):
        return None
    return reply("temp", memory, understood)


def _asks():
    asks, helpers = [], []
    for _, parts, words in ASK_KINDS:
        for part in parts:
            if part not in asks:
                asks.append(part)
        for word in words:
            if word not in helpers:
                helpers.append(word)
    return tuple(asks), tuple(helpers)


ASK_OPENERS = ("and", "what", "how", "shall", "should", "do", "does", "any", "with", "also",
               "then", "ok", "okay", "great", "so", "could", "can", "would", "will")
ASK_PHRASES = ("what about", "how about", "shall i", "should i", "go with", "serve with",
               "alongside", "with it", "as well", "any good", "any ideas", "do we need",
               "do i need")

USE_UP_PHRASES = ("what can i do with", "what do i do with", "what should i do with",
                  "what can i make with", "what can i use", "use up", "using up", "use it up",
                  "besides", "instead of", "other than", "apart from", "bag of")


def _asking_for_a_side(text):
    have = tokens(text)
    if not have:
        return False
    if any(_phrase_in(text, phrase) for phrase in USE_UP_PHRASES):
        return False
    if any(_phrase_in(text, phrase) for phrase in ASK_PHRASES):
        return True
    return have[0] in ASK_OPENERS


PLAN_NAMES_LONGEST = tuple(sorted(
    [name for name in PLAN_NAMES if name.split()[0] not in ("a", "an", "the")],
    key=lambda name: (-len(name.split()), name)))

WHEN_WORDS = ("tonight", "tomorrow", "today", "this evening", "this weekend", "this afternoon",
              "later", "on sunday", "on saturday", "on friday", "for dinner", "for tea",
              "for lunch", "for sunday", "for supper", "this week")

START_WORDS = (("doing", "cooking", "making", "roasting", "baking", "starting",
                "thinking of", "thinking about", "considering", "fancy", "fancying",
                "feel like", "feeling like", "in the mood for", "planning", "planning on",
                "might do", "might make", "might cook"),
               PLAN_NAMES_LONGEST + ("tonight", "tomorrow", "this weekend", "this evening", "later",
                             "today", "on sunday", "on saturday", "on friday", "for dinner",
                             "for tea", "for lunch", "for sunday",
                             "for the first time", "first time", "for my", "for a", "for the",
                             "for six", "for 6", "for eight", "for 8", "for four", "for 4",
                             "for two", "for 2",
                             "i am", "we are"))


PERSON_START = re.compile(r"\b(i'?m|i am|we'?re|we are)\b")

DELIBERATING_START = re.compile(
    r"\b(?:thinking (?:of|about)|thought about|considered|considering|fancy|fancying|"
    r"feel(?:ing)? like|in the mood for|might (?:do|make|cook|have)|may (?:do|make|cook)|"
    r"planning|planning on|plan to)\b")


def _start(memory, understood):
    if ask_kind(understood):
        return None
    text = ""
    if isinstance(understood, dict):
        text = understood.get("norm_text") or understood.get("clean") or ""
    announced = bool(PERSON_START.search(text))
    if not (announced or DELIBERATING_START.search(text)):
        return None
    if not announced and not any(word in text for word in WHEN_WORDS):
        return None
    if _their_diet_refuses(memory, understood, text):
        return None
    return _start_sentence(memory, understood)


def _their_diet_refuses(memory, understood, text):
    from .cooking import _bans_for, _bans_it, _bans_said, _foods_named
    banned = _bans_for(understood, memory)
    if not _bans_said(banned):
        return False
    return any(_bans_it(food, banned) for food in _foods_named(text))


def _start_sentence(memory, understood):
    key = dish_for(memory, understood)
    plan = PLANS.get(key) if key else None
    if plan is None:
        return None
    label = plan.get("label") or plan["names"][0][0]
    low = label.lower()
    text = str((understood or {}).get("norm_text") or (understood or {}).get("clean") or "").lower()
    said = next((name for group in plan["names"] for name in group
                 if name.split()[0] not in ("a", "an", "the")
                 and re.search(r"(?<![a-z0-9])" + re.escape(name) + r"(?![a-z0-9])", text)), None)
    if said and said not in low and low not in said and said[:6] != low[:6]:
        label = said
    label = label[0].upper() + label[1:]
    time, temp = plan.get("time"), plan.get("temp")
    if time and temp and temp.split("C")[0].strip() in time:
        temp = None
    parts = [time, temp]
    return f"{label}: " + " ".join(part for part in parts if part)


STARTED_PARTS = ("time", "temp", "done")

STAGE_PARTS = ("prove", "proof", "proofs", "proving", "rise", "rises", "rising", "risen",
               "rest", "rests", "resting", "knead", "kneads", "kneading", "chill", "chills",
               "chilling", "cool", "cools", "cooling", "marinate", "marinades", "marinating",
               "soak", "soaks", "soaking", "set", "sets", "setting")


ASK_FILLER = frozenset("""
    a about after again all also an and any are as at be been before but by can could do does
    doing done down for from get gets give go goes going had has have he her him his how i if in
    into is it its just keep keeps know like long many may me min mins minute minutes more most
    much my need needs not now of off on once one only or other our out over own per please put
    quite rather really right roughly same shall she should so some still such take takes than
    that the their them then there these they thing things this those time to too under until up
    us use very want wants was way we well were what when where which while who why will with
    would you your ok okay alright thanks thank then till yet
    bake bakes baking boil boils boiling check chill cook cooks cooking cool cools fry grill
    leave leaves let marinate oven pan rest roasts roast roasting simmer simmering sit stand
    steam stir temperature temp turn turns wait
    each side sides bit piece half quarter top bottom middle rack shelf tin dish tray foil lid
    cover covered uncover grate hob degrees degree kilo kilos kg pound pounds lb lbs gram grams
    cm inch inches total altogether overall low high medium slow fast quick quickest minimum
    maximum well rare done cold frozen fresh warm hot cool leftovers leftover
""".split())


def _asks_about_another_thing(text, key):
    plan = PLANS.get(key) or {}
    own = set()
    for group in plan.get("names") or ():
        for name in (group if isinstance(group, (list, tuple)) else (group,)):
            own.update(tokens(str(name)))
    parts = re.split(r"\bhow\b|\bwhat temperature\b|\bwhat temp\b|\bis it done\b",
                     str(text).lower())
    if len(parts) < 2:
        return False
    for word in tokens(parts[-1]):
        if word in ASK_FILLER or word in own or any(char.isdigit() for char in word):
            continue
        return True
    return False


def announced_part(memory, understood):
    if not isinstance(memory, dict) or not isinstance(understood, dict):
        return None
    kind = ask_kind(understood)
    if kind not in STARTED_PARTS:
        return None
    words = [str(word).lower() for word in (understood.get("words") or ())]
    if any(word in STAGE_PARTS for word in words):
        return None
    text = understood.get("norm_text") or understood.get("clean") or ""
    if not PERSON_START.search(text):
        return None
    key = dish_in(text)
    if not key:
        return None
    if _asks_about_another_thing(text, key):
        return None
    if kind in ("time", "temp"):
        answer = _start_sentence(memory, understood)
    else:
        answer = reply(kind, memory, understood)
    return answer if isinstance(answer, str) and answer.strip() else None


SIDE_METHOD = ("do the", "do them", "do it", "cook the", "cook them", "roast the", "boil the",
               "in with", "in too", "put them in", "put it in", "same oven", "same time",
               "blend", "blended", "blender", "puree", "pureed", "purée", "liquidise",
               "liquidize", "hide", "hidden", "sneak", "grate", "grated")


GOES_WITH = ("go with", "goes with", "serve with", "serving with", "pairs with", "have with",
             "eat with", "alongside")

GOES_WITH_SHAPE = re.compile(
    r"\b(?:go|goes|going|went|serve|serves|serving|pair|pairs|pairing|eat|eats|eating|"
    r"have|has|having)\s+(?:\w+\s+){0,2}with\b"
    r"|\b(?:go|goes|serve|serves|pair|pairs)\s+alongside\b"
    r"|\b(?:on|as)\s+(?:the|a)\s+side\b|\bside\s+dishes?\b")


def _asking_to_pair(text):
    return bool(GOES_WITH_SHAPE.search(text))

PAIRING_FOODS = ("cheese", "apples", "apple", "pear", "pears", "grapes", "fig", "figs",
                 "penne", "fusilli", "macaroni", "rigatoni", "tagliatelle", "linguine",
                 "gnocchi", "couscous", "quinoa", "halloumi", "lentils", "chickpeas",
                 "sausages", "sausage", "ham", "salmon", "mackerel", "prawns", "tofu",
                 "avocado", "tomatoes", "cucumber", "courgette", "aubergine", "beetroot",
                 "sweet potato", "butternut", "hummus", "houmous", "yoghurt", "oats",
                 "porridge", "eggs", "bacon", "chorizo", "steak", "chicken", "lamb", "pork",
                 "duck", "turkey", "cod", "haddock", "tuna", "mushrooms", "peppers", "spinach",
                 "broccoli", "cabbage", "peas", "beans", "carrots", "potatoes", "rice", "pasta",
                 "noodles", "bread", "mash", "chips", "polenta", "wrap", "wraps", "pitta")

PAIRING_RICH = ("Rich food wants something sharp and something crisp beside it: pickle or "
                "chutney, a few grapes or a sliced pear, crackers or warm bread, and a handful of "
                "leaves with a mustardy dressing if it has to be a meal. The rule underneath is "
                "that fat needs acid - the same reason chips want vinegar and pork wants apple "
                "sauce.")

PAIRING_PLAIN = ("Plain and starchy wants something wet on top: a sauce, a stew, a curry, or "
                 "the juices from the pan, plus one sharp thing because the starch has no acid "
                 "of its own. So pasta wants a sauce with garlic and a little of the water it "
                 "cooked in; rice wants a curry or a daal and a squeeze of lemon; bread wants "
                 "olive oil, tomato or soup.")

PAIRING_LEAN = ("Something starchy, something green, and something sharp or juicy: potatoes "
                "or rice or bread, a green vegetable with butter or oil on it, and a squeeze of "
                "lemon, a spoon of yoghurt, or a tomato salad. Keep it to one of each and it "
                "works with nearly anything - the sharp thing is what stops the plate tasting "
                "flat.")

RICH_FOODS = ("cheese", "cream", "butter", "lamb", "duck", "pork", "sausage", "sausages",
              "bacon", "chorizo", "halloumi", "pie", "pastry", "batter", "chips", "avocado",
              "salmon", "mackerel", "chocolate", "goats cheese", "feta", "steak", "beef")

PLAIN_FOODS = ("rice", "pasta", "spaghetti", "penne", "fusilli", "macaroni", "rigatoni",
               "tagliatelle", "linguine", "noodles", "couscous", "quinoa", "bread", "potato",
               "potatoes", "mash", "polenta", "porridge", "oats", "wrap", "wraps", "pitta")


def _names_any(text, words):
    return any(_phrase_in(text, word) for word in words)


def asks_for_a_side_of_a_food(text):
    return _asking_to_pair(text) and _names_any(text, PAIRING_FOODS)


def general_sides(text):
    if _names_any(text, RICH_FOODS):
        return PAIRING_RICH
    if _names_any(text, PLAIN_FOODS):
        return PAIRING_PLAIN
    return PAIRING_LEAN


COLOUR_CHOICE = re.compile(
    r"\b(?:the|this|that|these|those|my|your|his|her|their|our|a|an)\s+"
    r"(?:green|blue|red|black|white|grey|gray|brown|pink|purple|orange|yellow|beige|cream)\s+"
    r"(?:one|ones|thing|things|version|colour|color)\b", re.I)

_CHOICE_FRAME = re.compile(
    r"\bor\b|\bvs\b|\bversus\b|\bbetween\b|\bwhich\b|\bshall i\b|\bshould i\b"
    r"|\bdo you want\b|\bwould you\b|\brather\b|\bprefer\b|\bpick\b", re.I)


def a_colour_choice(text):
    text = str(text or "")
    return bool(COLOUR_CHOICE.search(text) and _CHOICE_FRAME.search(text))


def _sides(memory, understood):
    text = ""
    if isinstance(understood, dict):
        text = understood.get("norm_text") or understood.get("clean") or ""
    if a_colour_choice(text):
        return None
    if not _asking_for_a_side(text):
        return None
    if any(phrase in text for phrase in SIDE_METHOD):
        return None
    key = side_in(text)
    plan = PLANS.get(dish_for(memory, understood) or "")
    if key and plan is None and _asking_to_pair(text):
        return None
    if key:
        return SIDES.get(key)
    if plan:
        return plan.get("sides")
    if asks_for_a_side_of_a_food(text):
        return general_sides(text)
    return None


IDEAS = (
    ("eggs", ("egg", "eggs"),
     "Eggs are the fastest dinner there is: an omelette takes 2 minutes, a frittata with last "
     "night's vegetables 10 minutes, and eggs on toast is a proper dinner if there is cheese in "
     "the fridge."),
    ("pasta", ("pasta", "spaghetti", "macaroni", "tagliatelle", "noodles"),
     "Pasta, about 12 minutes: put it on, and while it cooks warm garlic and chilli in olive "
     "oil, then toss the drained pasta through with a handful of cheese and a spoon of the "
     "water it cooked in."),
    ("rice", ("rice",),
     "Rice, about 15 minutes: start it with the lid on, and while it steams fry onion, garlic "
     "and whatever veg you have, then stir the rice through with soy sauce and an egg."),
    ("veg", ("vegetables", "veg", "broccoli", "spinach", "peppers", "mushrooms", "courgette",
             "aubergine", "chickpeas", "beans", "lentils"),
     "Whatever veg you have, 15 minutes: fry it hot in a big pan, add a tin of chickpeas or "
     "beans and a spoon of curry paste, and serve it with rice, couscous or bread."),
    ("fish", ("fish", "salmon", "cod", "haddock", "prawns", "prawn", "tuna"),
     "Fish, about 15 minutes: a fillet skin side down in a hot pan for 4 minutes, then 2 on "
     "the other side, with rice or a bag of greens alongside."),
    ("chicken", ("chicken", "turkey"),
     "Chicken, about 20 minutes: slice a breast thin, fry it hot for 5 or 6 minutes, then add "
     "a tin of tomatoes or a spoon of pesto and serve it with pasta or a wrap. Whole thighs "
     "take 35 minutes, so save those for a night with more time."),
    ("mince", ("mince", "beef", "pork", "lamb"),
     "Mince, about 20 minutes: brown it hard, add a tin of tomatoes, a spoon of tomato puree "
     "and whatever veg is in the drawer, and simmer 10 minutes while rice or pasta cooks."),
    ("potatoes", ("potato", "potatoes"),
     "Potatoes, about 25 minutes: cut them into wedges, toss in oil and salt and roast at 200C "
     "while you cook something else, or boil and mash them with butter and a spoon of mustard."),
)

TRAY_IDEA = ("One tray: sausages or chicken thighs, chopped potatoes, onion and peppers, oil, "
             "salt and a spoon of paprika at 200C for 40 minutes, turning once. One tray, one "
             "wash.")

APPLIANCE_IDEAS = (
    (("slow cooker", "slow-cooker", "crockpot", "crock pot"),
     "Slow cooker: chilli, curry, stew or a shoulder of pork, on low for 6 to 8 hours or high "
     "for 3 to 4. Brown the meat first or the flavour is thin, keep the liquid to about half "
     "what you want at the end, and put herbs in for the last hour."),
    (("air fryer",),
     "Air fryer: chicken thighs 25 minutes at 190C, chips 20 at 200C after a shake in oil, "
     "salmon 10 at 190C. It is a small hot oven, so one layer and a shake halfway, or it "
     "steams instead of browning."),
    (("tray bake", "traybake", "roasting tin", "one pan", "one pot"),
     TRAY_IDEA),
)

VEGAN_IDEA = ("Vegan and still a proper dinner: a chickpea and spinach curry with rice, a lentil "
              "and tomato lasagne with oil in place of the cheese sauce, or a tray of roasted veg "
              "with chickpeas and couscous. Check the stock cubes, the bread and the pesto, which "
              "are where the milk usually hides.")

VEGGIE_IDEA = ("Vegetarian and still a proper dinner: a chickpea and spinach curry with rice, a "
               "lentil and mushroom lasagne, or a tray of roasted veg with feta and couscous. "
               "One dish everyone eats beats a meat main with something made separately.")

VEGGIE_SWAP_IDEA = ("Nothing has to change about the amounts: swap the meat for a fist of chickpeas, "
                    "lentils, eggs or cheese, and keep the vegetables, rice or potatoes as they are.")
VEGAN_SWAP_IDEA = ("Nothing has to change about the amounts: swap the meat for a fist of chickpeas, "
                   "lentils, tofu or nuts, use oil or a plant spread instead of butter, and keep the "
                   "vegetables and rice or potatoes. Check the stock cubes, the bread and the pesto, "
                   "where the milk usually hides.")

OVEN_WORD = re.compile(r"\boven\b", re.I)

NICE_IDEA = ("Something worth sitting down to, and hard to get wrong: chicken thighs roasted "
             "skin side up on a tray of potatoes, onion and peppers at 200C (180C fan) for 40 "
             "minutes, or a salmon fillet with the same tray for 15. Buy a good pudding and the "
             "whole thing feels like a dinner.")

COMPARE_IDEAS = (
    (("air fryer", "oven"),
     "The air fryer is a small hot oven: quicker to heat, better for chips and one or two "
     "portions, worse for a big tray or a cake, because food in one layer is all it browns. Use "
     "it for a dinner for two and the oven for a family tray, a joint or anything that needs "
     "even heat."),
    (("slow cooker", "oven"),
     "The slow cooker is for a cheap cut and a long afternoon: it cannot brown anything, so the "
     "oven is the one for a roast, a tray of veg or a bird. Brown in a pan first and the slow "
     "cooker wins on a stew."),
)

KIDS_IDEA = ("Kids, about 15 minutes: pasta with butter and cheese, fish fingers or a small "
             "roast tray of chips and peas, or scrambled eggs on toast. Keep the sauce on the "
             "side and give them less than you think they want, then let them ask for more.")

CHEAP_IDEA = ("Cheap and filling: a lentil or bean chilli, pasta with a tin of tomatoes and "
              "garlic, jacket potatoes with cheese and beans, or egg fried rice with frozen "
              "veg. Pulses and tins cost pennies a portion, and meat is the line that moves a "
              "weekly shop.")

AHEAD_IDEA = ("Tomorrow, cook double: a chilli, a curry, a lasagne or a stew is better the next "
              "day, and the second portion is tomorrow sorted. Rice and pasta do not keep as "
              "well as the sauce, so cook those fresh.")

_BIRDS = ("chicken", "turkey", "duck")
_RED_MEAT = ("beef", "pork", "lamb", "mince", "sausage", "sausages", "ham", "bacon", "gammon",
             "venison")


def _another_meat(food):
    name = str(food or "").lower()
    if any(_same_word(name, bird) for bird in _BIRDS):
        return "beef or pork"
    if any(_same_word(name, red) for red in _RED_MEAT):
        return "chicken thighs"
    return "chicken thighs or beef"


SUBSTITUTES = (
    (("mushroom", "mushrooms"),
     "No mushrooms then: leave them out and put a tin of chickpeas, a handful of spinach or some "
     "roasted peppers in their place. In a lasagne or a curry they are only there for texture, "
     "so the dish still works, and the curry and the tray of roast veg have none to start with."),
    (("onion", "onions", "shallot", "shallots"),
     "No onion then: start the dish with a leek, a stick of celery or a spoon of tomato puree "
     "instead, and leave out the raw onion on top. The onion is there for the base, and any of "
     "those does that job."),
    (("garlic",),
     "No garlic then: leave it out and add a spoon of the green tops of a spring onion at the "
     "end. It is the raw heat people mind, most of the time, rather than the flavour."),
    (("cheese", "dairy"),
     "No cheese then: leave it off and finish the dish with a squeeze of lemon, a spoon of "
     "olive oil and some black pepper, with a spoon of pesto or a few fried onions on top if you "
     "want something savoury there. Check the stock cube and the pesto, which often have milk in "
     "them."),
    (("fish", "salmon", "cod", "haddock", "tuna", "prawn", "prawns", "seafood"),
     "No fish then: chicken thighs or a tin of chickpeas go into the same sauce in the same "
     "time, and it is the sauce and the texture that carry the dish."),
    (("meat",),
     "Then leave the meat out: a tin of chickpeas or lentils, or a handful of mushrooms, with a "
     "stock cube, gives the dish the body the meat was doing, and the vegetarian list above is "
     "where to start."),
    (("chicken", "beef", "pork", "lamb", "turkey", "mince", "sausage", "sausages", "ham",
      "bacon", "gammon", "duck", "venison"),
     "No {food} then: swap in {other} - same dish, same time, and for a roast the same oven, "
     "potatoes and gravy - or a tin of chickpeas if you would rather have no meat."),
    (("nuts", "nut", "peanut", "peanuts", "almond", "almonds", "walnut", "walnuts", "cashew",
      "cashews", "pesto"),
     "No nuts then: toasted seeds do the same job on top, and check the pesto, the chocolate and "
     "anything marked 'may contain nuts', which is where they usually hide."),
    (("chilli", "chillies", "chili", "spicy", "heat", "curry powder", "curry paste"),
     "No chilli then: smoked paprika or a spoon of tomato puree gives the depth without the "
     "heat, and taste as you go rather than adding it at the table."),
    (("coriander", "cilantro"),
     "No coriander then: flat-leaf parsley does the same fresh job, or leave the green out and "
     "finish with a squeeze of lime. If it tastes of soap, that is a gene and not the cook, and "
     "nothing you do to it will change that."),
    (("olives", "olive"),
     "No olives then: capers or a spoon of chopped sun-dried tomato give the same salty hit, and "
     "a little more salt and lemon does it if you have neither."),
    (("peppers", "bell pepper", "bell peppers", "red pepper", "green pepper", "yellow pepper",
      "sweet pepper", "capsicum"),
     "No peppers then: courgette, mushrooms or fennel roast in the same time and give the same "
     "bulk, and a spoon of smoked paprika puts the sweet smokiness back."),
    (("mayonnaise", "mayo"),
     "No mayonnaise then: yoghurt with a squeeze of lemon and a pinch of salt does the same "
     "creamy job, or a spoon of mustard thinned with oil."),
    (("cucumber",),
     "No cucumber then: celery, lettuce or thin ribbons of courgette give the same crunch, and "
     "they take a dressing the same way."),
    (("tomato", "tomatoes", "passata"),
     "No tomato then: a little stock with a spoon of miso or a splash of balsamic gives the sauce "
     "its savoury body, and a tin of coconut milk does it for a curry; roasted red pepper, "
     "skinned and mashed, is the closest thing to the texture."),
    (("egg", "eggs"),
     "No egg then: a spoon of cornflour or a little of the water the pasta cooked in brings the "
     "sauce together, and check the pasta itself if it is the fresh kind."),
)

DISLIKED = ("mushroom", "mushrooms", "onion", "onions", "shallot", "shallots", "garlic",
            "cheese", "dairy", "milk", "butter", "cream", "yoghurt", "yogurt", "fish", "salmon",
            "cod", "haddock", "tuna", "prawn", "prawns", "seafood", "meat", "chicken", "beef",
            "pork", "lamb", "mince", "sausage", "sausages", "ham", "bacon", "nuts", "nut",
            "peanut", "peanuts", "almond", "almonds", "walnut", "walnuts", "cashew", "cashews",
            "pesto", "chilli", "chillies", "chili", "spicy", "tomato", "tomatoes", "passata",
            "egg", "eggs", "coriander", "cilantro", "olives", "cucumber", "mayonnaise", "mayo",
            "peppers", "capsicum")

DISLIKE_SHAPES = ("hates", "hate", "hated", "doesnt like", "doesn't like", "does not like",
                  "dont like", "don't like", "do not like", "cant stand", "can't stand",
                  "cannot stand", "no", "not a fan of", "sick of", "can not stand",
                  "never eats", "never eat",
                  "is not a fan of", "are not a fan of",
                  "dont have", "don't have", "do not have", "havent got", "haven't got",
                  "have not got", "ran out of", "run out of", "out of", "none left", "got no",
                  "wont eat", "won't eat", "will not eat", "wouldnt eat", "wouldn't eat",
                  "doesnt eat", "doesn't eat", "does not eat", "refuses", "refuse",
                  "dislikes", "dislike")

OUT_OF_CUE = re.compile(
    r"\b(?:dont|don't|do not|havent|haven't|have not|hasnt|hasn't|has not)\s+(?:got|have|has)\b"
    r"|\bgot no\b|\b(?:ran|run)\s+out\s+of\b|\bout\s+of\b|\bnone left\b|\bnothing left\b",
    re.I)
KITCHEN_SWAP = ("milk", "butter", "cream", "sour cream", "double cream", "single cream",
                "creme fraiche", "buttermilk", "yoghurt", "yogurt")


WASTE_WORDS = ("wasting", "waste", "wasted", "throwing", "throw", "thrown", "bin", "binning",
               "buying", "bought", "cooking", "making", "chopping", "peeling", "eating",
               "smelling", "the smell of", "the taste of")

FOOD_TAIL_OK = ("and", "or", "in", "on", "at", "for", "with", "please", "thanks", "though",
                "tho", "either", "tonight", "today", "now", "anymore", "any", "more", "all",
                "at all", "whatsoever", "ever", "honestly", "really", "but", "so", "because",
                "if", "when", "as", "to", "from", "into", "out", "off", "up", "away",
                "instead", "here", "there", "myself", "himself", "herself", "themselves",
                "food", "foods", "dishes", "stuff", "things", "anything", "meals", "dinners",
                "what", "which", "who", "can", "could", "shall", "should", "would", "will",
                "do", "does", "did", "is", "are", "was", "were", "i", "we", "you", "they",
                "idea", "ideas", "recipe", "recipes", "suggestions", "suggestion", "instead",
                "tonight", "today", "for", "with", "any", "some")

HOW_WORDS = re.compile(r"^\s*(?:how|can|could|do|does|is|what do i)\b|\binstead of\b|"
                       r"\bsubstitute\b", re.I)

GENERIC_SWAP = ("Then leave the {food} out: cook the rest as it is and add something with the "
                "same job - a tin of chickpeas for body, a squeeze of lemon or a spoon of "
                "mustard for the edge - and taste it before it goes to the table.")


CUPBOARD = re.compile(r"\bwhat can i (?:make|do|cook|have) (?:with|out of|from)\b|"
                      r"\bwhat (?:to|shall i) (?:make|do|cook)\b", re.I)


def _foods_named(understood):
    if not isinstance(understood, dict):
        return False
    from . import cooking
    try:
        if cooking.ingredients(understood):
            return True
    except Exception:
        return False
    return False


HAVE_WORDS = re.compile(r"\b(?:i|we) ?(?:'ve|have(?: got)?|only have|just have|still have|got)\b"
                        r"|\ball i (?:have|have got|ve got)\b|\bthere(?:'s| is) only\b|"
                        r"\bonly (?:got|have)\b", re.I)


def _states_what_they_have(text):
    return bool(HAVE_WORDS.search(text or ""))


def _dish_in_flight(memory, understood, food):
    from . import cooking
    said = _recent_answers(memory)
    if any(word in DISH_WORDS or word in BAKE_WORDS for word in tokens(said)):
        return True
    text = understood.get("norm_text") or understood.get("clean") or ""
    foods = DISH_WORDS + BAKE_WORDS + tuple(getattr(cooking, "_FOOD", ()))
    for word in tokens(text):
        if word in MEAL_WORDS:
            continue
        if word in foods and not any(_same_word(word, name) for name in DISLIKED):
            return True
    for line in recent_texts(memory)[1:4]:
        if any(word in DISH_WORDS for word in tokens(line)):
            return True
    return False


SAID_DISLIKE = ("hate", "hates", "hated", "dislikes", "dislike", "doesnt like",
                "doesn't like", "does not like", "dont like", "don't like", "do not like",
                "cant stand", "can't stand", "cannot stand", "can not stand", "wont eat",
                "won't eat", "will not eat", "refuses to eat", "refuse to eat", "never eats",
                "never eat", "allergic to", "intolerant to", "sick of", "not a fan of",
                "is not a fan of", "are not a fan of", "off ")


def _said_dislike(text):
    lowered = str(text or "").lower().replace("\u2019", "'")
    return any(_phrase_in(lowered, shape) for shape in SAID_DISLIKE)


DINNER_ASK = ("dinner", "tea", "supper", "lunch", "cook", "cooking", "make", "meal", "meals",
              "recipe", "recipes", "idea", "ideas", "suggest", "what can i", "what should i",
              "what do i", "feed", "tonight")


def _asks_for_a_dinner(text):
    lowered = str(text or "").lower().replace("\u2019", "'")
    return any(_phrase_in(lowered, shape) for shape in DINNER_ASK)


OTHER_PEOPLE = ("my wife", "my husband", "my partner", "my son", "my daughter", "my child",
                "my children", "my kid", "my kids", "my mum", "my mom", "my mother", "my dad",
                "my father", "my parents", "my family", "my friend", "my brother", "my sister",
                "my boyfriend", "my girlfriend", "my flatmate", "my housemate", "my nan",
                "my grandma", "my grandad", "my stepson", "my stepdaughter", "he ", "she ",
                "they ", "his ", "her ", "their ", "the kids", "the children", "the little one",
                "someone", "somebody", "our guest", "one of the guests", "my guests")

SAID_DISLIKE_OTHER = ("hates", "dislikes", "does not like", "doesnt like", "doesn't like",
                      "wont eat", "won't eat", "will not eat", "refuses", "refuse", "never eats",
                      "not a fan", "allergic to", "intolerant to")


def _somebody_else_refuses(text):
    lowered = str(text or "").lower().replace("\u2019", "'")
    if not any(_phrase_in(lowered, shape) for shape in SAID_DISLIKE_OTHER):
        return False
    return any(_phrase_in(lowered, person.strip()) for person in OTHER_PEOPLE)


LIKING = ("i love", "i like", "i prefer", "we love", "we like", "i adore", "my favourite",
          "i rather have", "i would rather", "he loves", "she loves", "the kids love",
          "the children love", "they love")


def _two_tastes(text):
    for part in str(text or "").lower().replace("\u2019", "'").split("|"):
        if any(_phrase_in(part, shape) for shape in DISLIKE_SHAPES):
            continue
        if any(_phrase_in(part, shape) for shape in LIKING):
            return True
    return False


DIET_FAMILIES = ("dairy", "meat", "gluten", "wheat", "soya", "soy", "sugar",
                 "carbs", "carbohydrate", "carbohydrates")


def _a_diet_family(food):
    return any(_same_word(food, family) for family in DIET_FAMILIES)


EATING_REFUSALS = ("wont eat", "won't eat", "will not eat", "refuse to eat", "refuses to eat",
                   "never eat", "never eats", "doesnt eat", "doesn't eat", "does not eat")


def _disliked_food(have):
    for index, word in enumerate(have):
        if not any(_same_word(word, name) for name in DISLIKED):
            continue
        before = " ".join(have[max(0, index - 4):index])
        if not any(_phrase_in(before, shape) for shape in DISLIKE_SHAPES):
            continue
        if (not any(_phrase_in(before, shape) for shape in EATING_REFUSALS)
                and any(_same_word(w, waste) for w in have[max(0, index - 3):index]
                        for waste in WASTE_WORDS)):
            continue
        if _same_word(word, "peppers") and any(
                _same_word(w, kind) for w in have[max(0, index - 2):index]
                for kind in ("black", "white", "ground", "cracked", "peppercorn", "peppercorns")):
            continue
        after = have[index + 1:index + 2]
        if after and not any(_same_word(after[0], word) for word in FOOD_TAIL_OK):
            continue
        return word
    return None


SHORTAGE_MARKERS = ("left", "none left", "ran out", "run out", "out of", "in the house",
                    "in the cupboard", "in the fridge", "not got", "havent got", "haven't got",
                    "dont have", "don't have", "short of", "all gone", "none of")
DISLIKE_VERBS = tuple(shape for shape in DISLIKE_SHAPES if shape != "no")
PERSON_DISLIKE = ("hates", "hate", "hated", "doesnt like", "doesn't like", "does not like",
                  "dont like", "don't like", "do not like", "cant stand", "can't stand",
                  "cannot stand", "can not stand", "not a fan of", "is not a fan of",
                  "are not a fan of", "never eats", "never eat")
OWN_DISLIKE = ("i hate", "i hates", "i dont like", "i don't like", "i do not like",
               "i cant stand", "i can't stand", "i cannot stand", "im not a fan",
               "i'm not a fan", "i never eat", "i never eats", "i avoid")
OTHER_PEOPLE = ("son", "sons", "daughter", "daughters", "kid", "kids", "child", "children",
                "toddler", "baby", "mum", "mother", "dad", "father", "husband", "wife",
                "partner", "boyfriend", "girlfriend", "nan", "nana", "gran", "granny",
                "grandma", "grandad", "grandpa", "brother", "sister", "friend", "friends",
                "mate", "mates", "guest", "guests", "he", "she", "they", "him", "her",
                "their", "them", "his", "hers", "everyone", "family", "flatmate", "housemate")


def _someone_elses_dislike(have, text):
    if any(_phrase_in(text, shape) for shape in OWN_DISLIKE):
        return False
    return any(word in OTHER_PEOPLE for word in have)


def _a_shortage_the_swap_table_answers(text, have, memory, understood):
    if any(_phrase_in(text, verb) for verb in DISLIKE_VERBS):
        return None
    if CUPBOARD.search(text):
        return None
    if not any(_phrase_in(text, marker) for marker in SHORTAGE_MARKERS):
        return None
    from . import cooking
    for row in cooking.ENTRIES:
        if not str(row.id).startswith("swap-"):
            continue
        if not any(_same_word(word, name) for word in have for name in row.key[0]):
            continue
        said = row.reply(memory, understood) if callable(row.reply) else row.reply
        if isinstance(said, str) and said.strip():
            return said
    return None


A_CHILD = frozenset(("son", "sons", "daughter", "daughters", "kid", "kids", "child", "children",
                     "toddler", "toddlers", "baby", "boy", "girl", "year old", "yearold"))
COOK_ASK_WORDS = frozenset(("cook", "cooking", "make", "making", "dinner", "dinners", "tea",
                            "supper", "lunch", "meal", "meals", "recipe", "recipes", "idea",
                            "ideas", "suggest", "suggestions", "suggestion", "feed"))


EATING_REFUSAL = ("wont eat", "won't eat", "will not eat", "wouldnt eat", "wouldn't eat",
                  "refuses to eat", "refused to eat", "doesnt eat", "doesn't eat",
                  "does not eat", "never eats")


def _a_child_who_will_not_eat(text, have):
    if not any(_phrase_in(text, word) for word in A_CHILD):
        return False
    if not any(_phrase_in(text, phrase) for phrase in EATING_REFUSAL):
        return False
    return not any(word in COOK_ASK_WORDS for word in have)


LUNCH_MEALS = frozenset("breakfast breakfasts brunch lunch lunches lunchbox lunchboxes".split())


def _swap_said(food, said, understood, text):
    from . import cooking
    refused = {name for name in cooking._refused_foods(text, families=True)
               if not _same_word(name, food)}
    if refused and any(_same_word(token, name) for token in tokens(said) for name in refused):
        words = tokens(GENERIC_SWAP)
        if any(_same_word(token, name) for token in words for name in refused):
            return None
        return GENERIC_SWAP.format(food=food)
    return said


def _a_family_ruled_out(have):
    for index, word in enumerate(have):
        if not _a_diet_family(word):
            continue
        before = " ".join(have[max(0, index - 4):index])
        if any(_phrase_in(before, shape) for shape in DISLIKE_SHAPES):
            return word
    return None


def _dislike(memory, understood):
    if not isinstance(understood, dict):
        return None
    text = understood.get("norm_text") or understood.get("clean") or ""
    have = tokens(text)
    if any(word in LUNCH_MEALS for word in have):
        return None
    if _a_child_who_will_not_eat(text, have) \
            and not any(_phrase_in(text, marker) for marker in SHORTAGE_MARKERS):
        return None
    shortage = _a_shortage_the_swap_table_answers(text, have, memory, understood)
    if shortage is not None:
        return shortage
    food = _disliked_food(have)
    family = _a_family_ruled_out(have)
    if family is not None and (food is None or not _same_word(food, family)):
        return None
    if food is not None and _a_diet_family(food):
        return None
    if food is not None and CUPBOARD.search(text):
        food = None
    if (food is not None and not _dish_in_flight(memory, understood, food)
            and _someone_elses_dislike(have, text)):
        for names, said in SUBSTITUTES:
            if any(_same_word(food, name) for name in names):
                said = _swap_said(
                    food, said.format(food=food, other=_another_meat(food)), understood, text)
                if said is None:
                    return None
                return said + (_ALLERGEN_NOTE if _an_allergen(food) else "")
        return _swap_said(food, GENERIC_SWAP.format(food=food), understood, text)
    if food is not None and not _dish_in_flight(memory, understood, food):
        if _two_tastes(text):
            return None
        if _states_what_they_have(text) and not _somebody_else_refuses(text):
            food = None
        elif not (_foods_named(understood)
                  or _somebody_else_refuses(text)
                  or (_said_dislike(text) and _asks_for_a_dinner(text))):
            food = None
    if food is None and not (HOW_WORDS.search(text) or NO_APPLIANCE.search(text)):
        return None
    if food is None and not _food_context(memory, understood):
        return None
    if food is None or HOW_WORDS.search(text):
        from . import cooking
        for table in (cooking.without, cooking.dish, cooking.meal):
            said = table(understood, text=text) if table is cooking.meal else table(understood)
            if isinstance(said, str) and said.strip():
                return said
        return None
    if not _food_context(memory, understood):
        return None
    if _bake_in_flight(memory) and any(_same_word(food, name) for name in ("egg", "eggs")):
        return EGG_FREE_BAKE
    if any(_same_word(food, name) for name in ("egg", "eggs")) and _an_egg_dish(memory):
        return EGG_IS_THE_DISH
    if any(_same_word(food, name) for name in DEFER_TO_ALLERGY) and _bake_in_flight(memory):
        return NUT_FREE_BAKE
    if OUT_OF_CUE.search(text) and any(_same_word(food, name) for name in KITCHEN_SWAP):
        return None
    for names, said in SUBSTITUTES:
        if any(_same_word(food, name) for name in names):
            said = said.format(food=food, other=_another_meat(food))
            return said + (_ALLERGEN_NOTE if _an_allergen(food) else "") + _the_dish_still(
                memory, food, said)
    return (GENERIC_SWAP.format(food=food) + (_ALLERGEN_NOTE if _an_allergen(food) else "")
            + _the_dish_still(memory, food, GENERIC_SWAP.format(food=food)))


TIME_IN_A_STEP = re.compile(r"\b\d{1,3}\s*(?:to\s*\d{1,3}\s*)?(?:minutes?|hours?|seconds?)"
                            r"\b|\b\d{1,3}\s*degrees\b", re.I)
DISH_LEAD = re.compile(r"^[A-Za-z][A-Za-z '&-]{2,28}:\s+")


def _the_dish_still(memory, food, said):
    if not isinstance(memory, dict):
        return ""
    turns = memory.get("turns")
    if not isinstance(turns, list):
        return ""
    for turn in reversed(turns[-4:]):
        if not isinstance(turn, dict) or not isinstance(turn.get("bot"), str):
            continue
        answer = turn["bot"].strip()
        if not answer or answer in said:
            continue
        for sentence in re.split(r"(?<=[.!?])\s+", answer):
            sentence = sentence.strip()
            if not sentence or not TIME_IN_A_STEP.search(sentence):
                continue
            if any(_same_word(item, food) for item in tokens(sentence)):
                continue
            if _phrase_in(said, sentence.split(":")[-1][:24].strip().lower()):
                continue
            step = DISH_LEAD.sub("", sentence).strip()
            if step[:1].islower():
                step = step[:1].upper() + step[1:]
            if tokens(step) and any(word in STEP_VERBS for word in tokens(step)):
                return " " + step
            return ""
    return ""


STEP_VERBS = ("whisk", "cook", "bake", "roast", "fry", "boil", "simmer", "grill", "pour", "stir",
              "layer", "finish", "leave", "rest", "turn", "add", "cover", "reduce", "chop",
              "heat", "mix", "fold", "beat", "chill", "set", "strain", "drain", "put")


EGG_FREE_BAKE = ("No egg then, and it still works: one egg becomes 60g of yoghurt, half a "
                 "mashed banana, or a tablespoon of ground flax or chia stirred into 3 "
                 "tablespoons of water and left 10 minutes. Those bind but do not lift, so add "
                 "half a teaspoon of baking powder as well, and give a batter an extra splash "
                 "of milk to loosen it.")


NUT_FREE_BAKE = ("No nuts then, and the cake still works: leave them out of the sponge and "
                 "the icing rather than swapping the cake. Check the chocolate, the icing sugar "
                 "and anything ready-made for 'may contain nuts', and keep the worktop, the tin "
                 "and the spoon clean if the allergy is serious.")

DEFER_TO_ALLERGY = ("nut", "nuts", "peanut", "peanuts", "almond", "almonds", "cashew",
                    "cashews", "walnut", "walnuts", "pistachio", "pistachios", "hazelnut",
                    "hazelnuts", "sesame", "shellfish", "prawn", "prawns")

ALLERGENS = ("nut", "nuts", "peanut", "peanuts", "almond", "almonds", "cashew", "cashews",
             "walnut", "walnuts", "pistachio", "pistachios", "hazelnut", "hazelnuts", "sesame",
             "egg", "eggs", "fish", "shellfish", "prawn", "prawns", "milk", "dairy", "cheese",
             "butter", "cream", "yoghurt", "yogurt", "gluten", "wheat", "flour", "soya", "soy",
             "mustard", "sulphites", "sulfites")

_ALLERGEN_NOTE = (" If someone at the table is allergic rather than fussy, read the labels for "
                  "'may contain' and keep the worktop, the tin and the spoon clean.")


KEEP_ASK_WORDS = ("keep", "keeps", "keeping", "last", "lasts", "lasted", "store", "stores",
                  "storing", "stored", "still good", "still ok", "stays good", "shelf life",
                  "freeze", "freezes", "freezer", "fridge", "frozen", "gone off", "next day",
                  "tomorrow", "use by", "out of date",
                  "still use", "still use it", "still eat", "still eat it", "still have",
                  "still alright", "still all right", "is it ok", "is it okay", "was it ok",
                  "was it okay")

NOT_A_DISH = ("plant", "plants", "houseplant", "houseplants", "plant pot", "pot plant",
              "garden", "lawn", "grass", "soil", "compost", "watering", "repot", "wilt",
              "wilted", "prune", "pruning", "fertiliser", "fertilizer", "seedling",
              "seedlings", "sow", "sowing", "indoors", "greenhouse", "allotment", "flower bed",
              "a day", "every day", "each day", "a week", "every week", "once a week",
              "how often", "every morning", "every night", "healthy", "unhealthy",
              "good for you", "bad for you", "fattening", "calories", "calorie", "diet",
              "dieting", "nutrition", "protein", "vitamins", "too much", "too many")


NOT_A_KEEPING_QUESTION = RAW_WORDS + ("raw egg", "raw flour", "pink in the middle", "pink inside",
                                      "runny yolk", "runny egg", "still frozen",
                                      "defrosted properly", "thawed properly")

KEEP_QUALITY_WORDS = (
    "warm", "hot", "moist", "juicy", "juicier", "tender", "tenderer",
    "from drying out", "drying out", "dry out", "from going dry",
    "from sticking", "not sticking", "sticking", "sticks together",
    "sticking together", "fluffy", "separate", "separated", "from going brown",
    "going brown", "from drying out", "drying out", "from drying", "from curdling",
    "curdling", "from splitting", "splitting", "runny", "setting", "from setting",
)


BAKE_WORDS = ("cake", "cakes", "sponge", "biscuit", "biscuits", "cookie", "cookies", "loaf",
              "bread", "muffin", "muffins", "brownie", "brownies", "tart", "pie", "birthday",
              "batter", "icing", "buttercream", "frosting",
              "pancake", "pancakes", "waffle", "waffles", "yorkshire", "crepe", "crepes")


EGG_DISH_WORDS = ("omelette", "omelet", "omlette", "scrambled", "scramble", "frittata",
                  "quiche", "poached", "shakshuka", "benedict")

EGG_IS_THE_DISH = ("Eggs are the whole dish there, so there is no swapping them out of it — what "
                   "works is the dish that stands in for it. Chickpea flour for an omelette: "
                   "120g gram flour and 150ml water whisked with a pinch of salt and turmeric, "
                   "fried thin in a hot oiled pan, 2 to 3 minutes a side. Crumble firm tofu into "
                   "a pan with turmeric and black pepper for a scramble, 5 minutes, and a pinch "
                   "of black salt if you keep it for the egg taste. A quiche sets the same way "
                   "with a tofu or chickpea-flour custard poured into the case.")


def _a_dish_in_flight(memory, words):
    for line in recent_texts(memory)[:4]:
        if any(_same_word(word, dish) for word in tokens(line) for dish in words):
            return True
    return False


def _bake_in_flight(memory):
    return _a_dish_in_flight(memory, BAKE_WORDS)


def _an_egg_dish(memory):
    return _a_dish_in_flight(memory, EGG_DISH_WORDS)


def _an_allergen(food):
    return any(_same_word(food, name) for name in ALLERGENS)


PUDDINGS = (
    (("no oven", "without an oven", "no baking", "no bake", "hob only", "just a hob", "fridge"),
     "No oven, so a cold one: an Eton mess (broken meringue, whipped cream, strawberries or "
     "raspberries), a lemon posset (300ml cream, 75g sugar and the juice of a lemon, simmered 3 "
     "minutes and set overnight), or a chocolate fridge cake (200g chocolate and 100g butter "
     "melted over broken biscuits, chilled 2 hours)."),
    (("chocolate", "choccy", "chocolatey"),
     "Chocolate mousse: melt 200g of chocolate, beat in 3 egg yolks, fold in 300ml of whipped "
     "cream and chill 2 hours. A fridge cake is quicker - broken biscuits, melted chocolate and "
     "butter, a handful of raisins, 2 hours in the fridge."),
    (("cold", "ice cream", "icecream", "frozen", "summer", "hot day"),
     "Something cold: an Eton mess, a lemon posset, or affogato - a scoop of vanilla ice cream "
     "with a shot of hot espresso over it."),
    (("quick", "quickly", "fast", "easy", "last minute", "ten minutes", "5 minutes"),
     "Ten minutes: an Eton mess, bananas with ice cream and butterscotch sauce, or yoghurt with "
     "honey and toasted nuts. A good shop-bought tart with cream is a proper pudding too, and no "
     "one minds."),
)

CROWD_PUDDING = ("For a crowd, one big dish rather than plates: an apple and blackberry crumble "
                 "(fruit in a dish, a crumble of 100g each of flour and butter with 50g of sugar, "
                 "40 minutes at 180C/160C fan, with custard), or a baked rice pudding, or a bread "
                 "and butter pudding - all made in the morning, and all soft enough for anyone "
                 "who finds chewing hard. An Eton mess takes five minutes if you buy the "
                 "meringues.")

CROWD_WORDS = ("crowd", "lots", "many", "everyone", "party", "dozen", "guests", "guest",
               "people",
               "six", "seven", "eight", "nine", "ten", "eleven", "twelve", "thirteen",
               "fourteen", "fifteen", "sixteen", "eighteen", "twenty", "thirty", "forty",
               "fifty", "hundred")


def _a_crowd(memory, text, have):
    for line in [text] + [one for one in recent_texts(memory) if isinstance(one, str)]:
        if any(_says(line, word, tokens(line)) for word in CROWD_WORDS):
            return True
        for chunk in tokens(line):
            if chunk.isdigit() and 6 <= int(chunk) <= 200:
                return True
    return False


FRUIT_PUDDING = ("An apple and blackberry crumble: the fruit in a dish with a spoon of sugar, a "
                 "crumble of 100g each of flour and butter rubbed together with 50g of sugar, 40 "
                 "minutes at 180C (160C fan), and custard. It scales to any number, it is better "
                 "made in the morning, and it is the pudding people are pleased to see.")

DESSERT_WORDS = ("pudding", "puddings", "pud", "dessert", "desserts", "afters", "sweet",
                 "sweets", "puddingy")


def _says(text, word, have):
    if " " in word:
        return word in text
    return word in have


def _pudding_for(have, text):
    for phrases, said in PUDDINGS:
        for phrase in phrases:
            if _phrase_in(text, phrase) or any(_same_word(word, phrase) for word in have):
                return said
    return None


ATE_ALREADY = re.compile(r"\b(?:ate|eaten|drank|drunk|had|has had|have had|having)\b", re.I)

REWARDED = re.compile(r"\b(?:reward|rewards|rewarding|rewarded|bribe|bribes|bribing|bribed|"
                      r"good behaviou?r|star chart|sticker|stickers|incentive|incentives|"
                      r"pocket money|allowance)\b", re.I)
PUDDING_ASK = re.compile(
    r"\b(?:what|which|who|any|anything|ideas?|suggest\w*|recommend\w*|make|makes|making|made|"
    r"recipe|serve|serving|shall|could|should|want|need|fancy|instead|tonight|pudding|dessert)\b",
    re.I)


def _pudding(memory, understood):
    if not isinstance(understood, dict):
        return None
    text = understood.get("norm_text") or understood.get("clean") or ""
    have = tokens(text)
    if not any(_says(text, word, have) for word in DESSERT_WORDS):
        return None
    if REWARDED.search(text):
        return None
    if ATE_ALREADY.search(text) and not PUDDING_ASK.search(text):
        return None
    if _diet(memory, understood):
        return None
    said = _pudding_for(have, text)
    if said:
        return said
    if _a_crowd(memory, text, have):
        return CROWD_PUDDING
    return FRUIT_PUDDING

OR_WORD = re.compile(r"\bor\b", re.I)

PRONOUN = re.compile(r"\b(?:it|that|this|one|its)\b", re.I)

NO_APPLIANCE = re.compile(r"\b(?:no|without a|not got a|haven't got a|havent got a)\s+"
                          r"(?:oven|hob|cooker|grill)\b", re.I)

SAFETY_WORDS = re.compile(r"\b(?:frozen|freeze|freezer|defrost\w*|thaw\w*|raw|reheat\w*|"
                          r"left out|gone off|off meat|use by|after its date)\b", re.I)

MEAL_WORDS = ("cook", "cooking", "cooked", "dinner", "tea", "supper", "lunch", "meal", "meals",
              "eat", "eating", "food", "kitchen", "recipe", "fridge", "freezer", "oven",
              "hungry", "shop", "shopping", "supermarket", "leftovers", "leftover",
              "cooker", "fryer", "crockpot", "hob", "pan", "tray", "tin", "bake")


def _food_context(memory, understood):
    if not isinstance(understood, dict):
        return False
    from . import cooking
    text = understood.get("norm_text") or understood.get("clean") or ""
    foods = DISH_WORDS + tuple(getattr(cooking, "_FOOD", ()))
    verbs = {"make", "made", "cook", "cooking", "fix", "fixing", "taste", "tastes",
             "tasted", "came", "out", "turned", "went", "wrong"}
    for line in [text] + recent_texts(memory)[:3]:
        have = tokens(line)
        if any((word in foods and word not in verbs) or word in MEAL_WORDS for word in have):
            return True
    return False


def _idea_for(have):
    for key, names, words in IDEAS:
        for name in names:
            if any(_same_word(word, name) for word in have):
                return key, words
    return None, None


def _already(reply, memory):
    opening = " ".join(reply.lower().split()[:4])
    for turn in reversed((memory.get("turns") or [])[-2:]):
        if isinstance(turn, dict):
            return " ".join(str(turn.get("bot") or "").lower().split()[:4]) == opening
    return False


def _named_dish(text):
    key = dish_in(text)
    if key is None:
        return None
    for group in PLANS[key]["names"]:
        for name in (group if isinstance(group, tuple) else (group,)):
            if len(name.split()) > 1 and _phrase_in(text, name):
                return key
    return None


VEGGIE_KEY = ("vegetarian", "vegetarians", "veggie", "vegan", "vegans", "don't eat meat",
              "dont eat meat", "do not eat meat", "doesn't eat meat", "doesnt eat meat",
              "does not eat meat", "no meat", "meat free", "meat-free", "won't eat meat",
              "wont eat meat", "will not eat meat")


VEGGIE_CARRIERS = ("is", "are", "eat", "eats", "eating", "them", "she", "he", "they", "him",
                   "her", "one", "of", "no", "not", "doesnt", "doesn't", "cant", "can't",
                   "wont", "won't", "guests", "guest", "party",
                   "them", "of us", "mate", "mates", "friend", "friends", "son", "daughter",
                   "mum", "dad", "mother", "father", "wife", "husband", "partner", "brother",
                   "sister", "everyone", "someone", "somebody", "one guest", "one of")


def _negative_forms(food):
    forms = []
    for subject_verb in ("doesnt", "doesn t", "does not", "didnt", "did not", "wont", "won t",
                         "will not", "cant", "can t", "can not", "cannot", "never"):
        for eat in ("eat", "eats", "have", "has"):
            forms.append(f"{subject_verb} {eat} {food}")
    for frame in ("avoids {}", "avoid {}", "avoiding {}", "off {}", "is off {}",
                  "no {} at all", "nothing with {}", "{} is out",
                  "cut out {}", "cutting out {}", "free of {}", "free from {}"):
        forms.append(frame.format(food))
    return tuple(dict.fromkeys(forms))


DIETS = (
    ("dairy",
     ("dairy free", "dairy-free", "no dairy", "lactose free", "lactose intolerant",
      "lactose intolerance", "milk free", "milk-free", "have dairy", "eat dairy", "had dairy",
      "have milk", "eat milk", "drink milk", "no milk", "not dairy"),
     "Dairy free is easy to cook around: oat, soya or almond milk in place of milk, olive oil "
     "instead of butter, and a tin of coconut milk where a recipe wants cream. Watch the labels "
     "for whey, casein, milk powder and lactose, which sit in stock cubes, bread, biscuits and "
     "some crisps, and check the pesto and the chocolate too."),
    ("gluten",
     ("gluten free", "gluten-free", "no gluten", "wheat free", "wheat-free", "eat gluten",
      "have gluten", "had gluten", "eat wheat", "have wheat", "no wheat"),
     "Gluten free: potatoes, rice, corn, quinoa and lentils are all fine, so a chilli, a curry, a "
     "stir-fry or a tray of roast veg with rice needs nothing changed. For a bake, use a "
     "gluten-free plain flour blend with a quarter teaspoon of xanthan gum per 200g and let the "
     "batter stand 20 minutes; cornflour is for thickening a sauce. Watch the labels for wheat, "
     "barley, rye and 'may contain', use tamari in place of soy sauce, and check the sausages and "
     "the stock cubes."),
    ("egg",
     ("egg free", "egg-free", "no eggs", "no egg"),
     "Egg free: in a cake or biscuits one egg becomes 60g of yoghurt, half a mashed banana, or a "
     "tablespoon of ground flax or chia stirred into three of water and left ten minutes - those "
     "bind but do not lift, so add half a teaspoon of baking powder too. Watch the labels for "
     "egg white and albumen, which are in some pasta, mayonnaise, cakes and glazed bread."),
    ("nut",
     ("nut free", "nut-free", "no nuts", "no nut", "eat nuts", "have nuts"),
     "Nut free: toasted seeds do the same job on top and in a flapjack, and check the labels for "
     "'may contain nuts' on chocolate, pesto, cereal and anything made in a bakery, which is "
     "where they usually hide."),
)

_DIET_FOOD = {"dairy": ("dairy", "milk"), "gluten": ("gluten", "wheat"),
              "egg": ("egg", "eggs"), "nut": ("nut", "nuts")}
DIETS = tuple((name,
               tuple(words) + tuple(form for food in _DIET_FOOD.get(name, ())
                                    for form in _negative_forms(food)),
               said)
              for name, words, said in DIETS)

DAIRY_FREE_VEGGIE = ("Vegetarian and no dairy, which is one list and not two: a chickpea and "
                     "spinach curry with rice, a lentil and tomato lasagne made with oil instead "
                     "of the cheese sauce, or a tray of roasted veg with chickpeas and couscous. "
                     "Watch the labels for whey, casein and milk powder, which sit in stock "
                     "cubes, bread and biscuits.")

_MEALS = r"(?:breakfast|brekkie|brekky|lunch|dinner|supper|meal|meals)"
DIET_MEAL_ASK = re.compile(r"\bfor (?:breakfast|brekkie|brekky|lunch|dinner|tea|supper)\b|"
                           r"\b" + _MEALS + r"\b[^.]{0,25}\bideas?\b|"
                           r"\bideas?\b[^.]{0,25}\b" + _MEALS + r"\b", re.I)

DIET_NOT_THIS = re.compile(r"\bcan (?:eat|have|drink)\b|\bhow do i\b|\bhow long\b|"
                           r"\b(?:can|could|should|may) i (?:ever |still |now )?(?:eat|have|drink)"
                           r"(?! for (?:breakfast|lunch|dinner|tea|supper|pudding|dessert|"
                           r"a snack|a starter)\b)"
                           r"\b|\bis it (?:ok|okay|fine|bad|good) (?:to|for me to) "
                           r"(?:eat|have|drink)\b|\bam i allowed to (?:eat|have|drink)\b|"
                           r"\bok (?:if|for|with)\b|\bokay (?:if|for|with)\b|"
                           r"\bfine to eat\b|\bsafe to eat\b|"
                           r"\bdo i have\b|\bin the fridge\b|\bin the cupboard\b", re.I)

DIET_TOO_MEDICAL = re.compile(r"\ballerg|\banaphyla|\bepipen\b|\bcoeliac\b|\bceliac\b|"
                          r"\bcalorie|\bcalories\b|\bprotein\b|\bvitamin|\bhealthy\b|"
                          r"\bis it bad\b|\bgood for you\b|\bweight\b|\bbaby\b|"
                          r"\bchild\b|\bchildren\b|\bpregnant\b|\bpregnancy\b|"
                          r"\bbreastfeed|\bbreast feed|\bnursing\b|\bnurse\b|\blactating\b|"
                          r"\bchestfeed", re.I)


DIET_RECALL = re.compile(r"\bmy diet\b|\bwhat (?:do|did) i eat\b|\bwhat am i eating\b|"
                         r"\bwhat (?:can|can't|cant|could) i (?:not )?(?:eat|have)\b|"
                         r"\bwhat do i not eat\b|\bam i (?:vegetarian|vegan|pescatarian|"
                         r"on a diet)\b", re.I)


VEGAN_WORD = re.compile(r"\b(?:vegan|vegans|plant based|plantbased)\b", re.I)

GUEST_DIET = re.compile(
    r"\b(?:one of (?:them|us|you|the guests|the family|my guests|the party)|one guest|a guest|"
    r"some of them|someone|somebody|everyone|"
    r"one (?:of (?:them|us|the guests|my guests|the family) )?(?:is|was|isnt|doesnt|wont|cant|"
    r"does not|will not|can not|only eats) |"
    r"my (?:friend|mate|son|daughter|mum|dad|mother|father|sister|brother|partner|wife|husband|"
    r"in laws|niece|nephew|cousin|colleague|neighbour))\b", re.I)

COOKING_VERB = re.compile(
    r"\b(?:cook|cooks|cooking|cooked|bake|bakes|baking|roast|roasts|roasting|"
    r"fry|frying|grill|grilling|recipe|recipes|what can i (?:cook|make)|"
    r"what should i (?:cook|make))\b",
    re.I)

MAKE_VERB = re.compile(r"\b(?:make|makes|making)\b", re.I)


def _food_words():
    from . import cooking
    verbs = {"make", "made", "cook", "cooking", "fix", "fixing", "taste", "tastes",
             "tasted", "came", "out", "turned", "went", "wrong"}
    return frozenset(word for word in DISH_WORDS + tuple(getattr(cooking, "_FOOD", ()))
                     if word not in verbs)


def _names_a_food(line):
    words = tokens(str(line or ""))
    foods = _food_words()
    return any(word in foods for word in words)


def _earlier_turns(memory):
    if not isinstance(memory, dict):
        return []
    return [t for t in (memory.get("turns") or []) if isinstance(t, dict) and t.get("user")]


def _a_food_word_with_no_cooking(memory, understood):
    return bool(_earlier_turns(memory)) and not cooking_under_way(memory, understood)


def cooking_under_way(memory, understood):
    text = ""
    if isinstance(understood, dict):
        text = str(understood.get("norm_text") or understood.get("clean") or "")
    for line in [text] + recent_texts(memory or {})[:4]:
        if not line:
            continue
        said = str(line)
        if COOKING_VERB.search(said):
            return True
        if MAKE_VERB.search(said) and _names_a_food(said):
            return True
    return False


def _veggie(memory, understood):
    if not isinstance(understood, dict):
        return None
    text = understood.get("norm_text") or understood.get("clean") or ""
    if DIET_RECALL.search(str(text)):
        return None
    if not _food_context(memory, understood) and not GUEST_DIET.search(str(text)):
        return None
    if _asks_about_the_diet(str(text)):
        return None
    if _a_food_word_with_no_cooking(memory, understood):
        return VEGAN_SWAP_IDEA if VEGAN_WORD.search(str(text)) else VEGGIE_SWAP_IDEA
    if VEGAN_WORD.search(str(text)):
        return VEGAN_IDEA
    return VEGGIE_IDEA


YES_NO_ASK = re.compile(r"^\s*(?:do|does|can|could|should|is|are|would|will|did)\b", re.I)
COOK_ASK = re.compile(r"\b(?:cook|cooking|make|dinner|tea|supper|lunch|feed|menu|recipe|meal)\b",
                      re.I)


def _asks_about_the_diet(text):
    return bool(YES_NO_ASK.search(text or "")) and not COOK_ASK.search(text or "")


def _diet(memory, understood):
    if not isinstance(understood, dict):
        return None
    text = str(understood.get("norm_text") or understood.get("clean") or "")
    if not text.strip():
        return None
    if (DIET_RECALL.search(text) or DIET_NOT_THIS.search(text) or DIET_TOO_MEDICAL.search(text)
            or DIET_MEAL_ASK.search(text)):
        return None
    for name, words, said in DIETS:
        if not any(_phrase_in(text, word) for word in words):
            continue
        if any(_phrase_in(text, word) for word in VEGGIE_KEY):
            return DAIRY_FREE_VEGGIE
        if _already(said, memory):
            return None
        return said
    return None


def has_a_veggie_reply(memory, understood):
    return bool(_veggie(memory, understood))


def has_a_diet_reply(memory, understood):
    return bool(_diet(memory, understood))


def has_a_dislike_reply(memory, understood):
    return bool(_dislike(memory, understood))


def _recent_answers(memory):
    turns = memory.get("turns") if isinstance(memory, dict) else None
    said = []
    for turn in (turns or [])[-2:]:
        if isinstance(turn, dict) and isinstance(turn.get("bot"), str):
            said.append(turn["bot"])
    return " ".join(said)


def _idea_food(have):
    for _key, names, _words in IDEAS:
        for name in names:
            for word in have:
                if _same_word(word, name):
                    return word
    return None


PICK_WORDS = ("minutes", "minute", "hour", "hours", "quick", "quickly", "fast", "easy",
              "cheap", "cheaper", "cheapest", "budget", "broke", "nice", "nicer", "special",
              "treat", "fancy", "tomorrow", "kids", "kid", "children", "child", "toddler")

NICE_WORDS = ("nice", "nicer", "special", "treat", "fancy", "impress", "impressive", "lovely")

GUEST_WORDS = ("girlfriend", "boyfriend", "partner", "wife", "husband", "date", "anniversary",
               "guests", "guest", "friends", "family", "in-laws", "parents", "people")



_CLEANING_IT = re.compile(
    r"\b(?:clean|cleaning|cleaned|wash|washing|scrub|scouring|dishwasher|dishwashers)\b"
    r"|\b(?:burnt|baked|stuck|crusted)\s+on\b|\bhow do i clean\b", re.I)


_PICK_ONE = re.compile(r"\b(?:or|vs|versus|rather|which|better|best)\b", re.I)


def _two_appliances(text):
    named = {phrases[0] for phrases, _text in APPLIANCE_IDEAS
             if any(_phrase_in(text, phrase) for phrase in phrases)}
    if OVEN_WORD.search(text or ""):
        named.add("oven")
    return len(named) > 1


def _appliance(text):
    if _CLEANING_IT.search(text or ""):
        return None
    if _two_appliances(text or "") and _PICK_ONE.search(text or ""):
        return None
    for phrases, reply_text in APPLIANCE_IDEAS:
        if any(_phrase_in(text, phrase) for phrase in phrases):
            return reply_text
    if OVEN_WORD.search(text):
        return TRAY_IDEA
    return None


WHOLE_FOOD = re.compile(r"\bwhole (?:chicken|bird|fish|leg|shoulder|duck|turkey|ham)\b|"
                        r"\b(?:leg|shoulder|joint) of\b|\b(?:bought|got|have) a (?:joint|bird)\b",
                        re.I)


def _already_cooking(memory):
    for line in recent_texts(memory)[:2]:
        if WHOLE_FOOD.search(line or ""):
            return True
    return False

CUT_WORDS = ("leg", "legs", "drumstick", "drumsticks", "thigh", "thighs", "wing", "wings",
             "breast", "breasts", "fillet", "fillets", "joint", "shoulder", "rib", "ribs")


def _names_an_appliance_and_a_cut(text):
    if not any(_phrase_in(text, phrase) for phrases, _text in APPLIANCE_IDEAS
               for phrase in phrases) and not OVEN_WORD.search(text):
        return False
    return bool({word.lower() for word in tokens(text)} & set(CUT_WORDS))


def _idea(memory, understood):
    if not isinstance(understood, dict):
        return None
    text = understood.get("norm_text") or understood.get("clean") or ""
    if _names_an_appliance_and_a_cut(text):
        return None
    have = tokens(text)
    if not have:
        return None
    if not _food_context(memory, understood):
        return None
    if _named_dish(text):
        return None
    if _already_cooking(memory):
        return None
    if SAFETY_WORDS.search(text):
        return None
    if any(_same_word(word, mark) for word in have
           for mark in ("kids", "kid", "children", "child", "toddler", "toddlers", "family")):
        return KIDS_IDEA
    from . import cooking

    for table in (cooking.dish, cooking.meal, cooking.without):
        said = table(understood, text=text) if table is cooking.meal else table(understood)
        if isinstance(said, str) and said.strip():
            return said
    named = _idea_food(have)
    if named is not None and named in tokens(_recent_answers(memory)):
        return None
    if OR_WORD.search(text):
        for phrases, reply_text in COMPARE_IDEAS:
            if all(_phrase_in(text, phrase) for phrase in phrases):
                return reply_text
    named = _appliance(text)
    if named is None and PRONOUN.search(text):
        for earlier in recent_texts(memory)[:3]:
            if NO_APPLIANCE.search(earlier):
                continue
            named = _appliance(earlier)
            if named is not None:
                break
    if named is not None:
        return named
    if any(_same_word(word, mark) for word in have
           for mark in ("cheap", "cheaper", "cheapest", "budget", "broke")):
        return CHEAP_IDEA
    if any(_same_word(word, mark) for word in have for mark in ("tomorrow", "tomorrows")):
        return AHEAD_IDEA
    key, reply_text = _idea_for(have)
    if reply_text is None and any(_same_word(word, mark) for word in have
                                  for mark in GUEST_WORDS + NICE_WORDS):
        return NICE_IDEA
    if reply_text is None:
        if not any(_same_word(word, mark) for word in have for mark in PICK_WORDS):
            return None
        for fallback_key, _, fallback in IDEAS:
            if not _already(fallback, memory):
                return fallback
        return IDEAS[0][2]
    if _already(reply_text, memory):
        for other_key, _, other in IDEAS:
            if other_key != key and not _already(other, memory):
                return other
    return reply_text


IDEA_SHAPES = ("something", "anything", "idea", "ideas", "suggest", "suggestion", "quick",
               "quickly", "easy", "fast", "minutes", "minute", "half an hour", "hour",
               "slow cooker", "slow-cooker", "air fryer", "cheap", "cheaper", "cheapest",
               "what about", "how about", "what else", "what can i do", "what can i cook",
               "what can i put", "what shall i", "one pan", "one pot", "one tray", "tray bake",
               "traybake", "roasting tin")
IDEA_CARRIERS = ("something", "anything", "only", "have", "got", "haven't", "wont", "want",
                 "need", "make", "made", "cook", "cooker", "fryer", "slow", "air", "tomorrow",
                 "fridge", "freezer", "chicken", "mince", "fish",
                 "eggs", "egg", "pasta", "rice", "potatoes", "veg", "vegetables", "cheese",
                 "bread", "kids", "us", "two", "quick", "easy", "cheap", "nice", "nicer",
                 "special", "treat", "fancy", "dinner", "supper", "pan", "pot", "tray",
                 "tin")



OUT_WORDS = ("eat out", "eating out", "where to eat", "where should we eat", "where can we eat",
             "where do we eat", "restaurant", "restaurants", "book a table", "table for",
             "meal out", "dinner out", "lunch out", "brunch out", "somewhere to eat",
             "place to eat", "places to eat", "eat tonight", "eat out tonight", "meal tonight",
             "chippy", "chip shop", "takeaway", "take away", "take-away", "takeout", "take out",
             "order in", "delivery", "deliveroo", "just eat", "uber eats", "curry house",
             "kebab shop", "pizza place",
             "best pizza", "good pizza", "decent pizza", "pizza near me", "pizza nearby",
             "pizza shop", "pizza takeaway", "pizza delivery", "pizza restaurant",
             "tapas", "bistro",
             "where should we go", "where shall we go", "where to go", "somewhere nice",
             "somewhere good", "go out for a meal", "out for dinner", "out for a meal",
             "anywhere to eat", "anywhere good to eat", "anywhere nice to eat",
             "anywhere decent to eat", "good place to eat", "somewhere good to eat")
OUT_ASK = ("cant decide", "can't decide", "cannot decide", "decide", "decided", "choose",
           "choosing", "pick", "picking", "fancy", "fancied", "fancy going", "craving",
           "in the mood", "what shall we", "what should we", "where shall we", "where should we",
           "where can we", "where should i", "what should i", "any ideas", "ideas", "suggest",
           "suggestion", "suggestions", "recommend", "recommendation", "recommendations",
           "same", "bored of", "bored with", "sick of", "treat", "this weekend", "near me",
           "nearby", "want a meal", "want to go out", "fancy a meal", "would like a meal",
           "could do with a meal", "somewhere to go",
           "anywhere", "anything good", "anywhere good", "anywhere nice", "anywhere decent",
           "how do i order", "how to order", "how do you order")
OUT_AVOID = ("make", "making", "made", "cook", "cooking", "recipe", "recipes", "at home",
             "from scratch", "fakeaway", "calories", "calorie", "healthy", "healthier", "diet",
             "bad for you", "fattening", "worth it", "cost", "cheaper", "save money", "budget",
             "sick", "ill", "food poisoning", "diarrhoea", "vomit", "allergy", "allergic",
             "gluten", "vegan", "vegetarian", "halal", "freeze", "frozen", "leftover",
             "reheat", "how long", "grow", "grown", "garden", "gym", "protein", "carbs",
             "wear", "wearing", "dress", "dress code", "outfit", "what to wear",
             "parcel", "parcels", "courier", "couriers", "seller", "tracking", "package",
             "packages", "not arrived", "never arrived", "late delivery", "delivery driver",
             "previous tenant", "refund",
             "late", "delayed", "delay", "arriving", "arrived", "arrive", "dispatched",
             "dispatch", "wrong item", "missing",
             "tip", "tips", "tipping", "service charge", "gratuity")

DOUGH_STICK_LEAD = ("Sticking is nearly always a wet dough meeting a dry surface, so the fix is "
                    "less water and more flour where the two meet. ")


def _dough_sticks(memory, understood):
    text = _line_text(understood)
    if "banneton" in text or "basket" in text or "brotform" in text:
        return DOUGH_STICK_LEAD + (
            "Dust the banneton generously with rice flour, which does not absorb the way wheat "
            "flour does, or line it with a well-floured cloth, and chill the shaped loaf 20 "
            "minutes before it goes in.")
    if "pastry" in text or "shortcrust" in text or "pie" in text or "tart" in text:
        return DOUGH_STICK_LEAD + (
            "Chill the pastry 20 to 30 minutes before rolling, keep the flour light and roll "
            "from the middle out with short strokes: warm pastry sticks however much flour you "
            "use." + (" Dust the pin as well." if "pin" in text else ""))
    if "hands" in text or "fingers" in text:
        return DOUGH_STICK_LEAD + (
            "Wet your hands or rub them with a little oil, and lift the dough with a scraper "
            "instead of pulling at it.")
    if "pin" in text or "rolling" in text:
        return DOUGH_STICK_LEAD + (
            "Dust the pin lightly, lift the dough with a scraper rather than a hand, and give it "
            "a quarter turn after each roll.")
    return DOUGH_STICK_LEAD + (
        "Keep a light dusting of flour on the bench, lift the dough with a scraper instead of "
        "pulling at it, and add strong white flour a spoonful at a time if the dough itself is "
        "too wet to handle.")



def _bake_fault_more(memory, understood):
    words = [str(word).lower() for word in (understood.get("words") or [])]

    def has(*wanted):
        return any(_same_word(word, want) for word in words for want in wanted)

    if has("waffle", "waffles"):
        return ("A soggy waffle is a batter that is too thin or an iron that is not hot enough: "
                "make it thicker than pancake batter - it should plop off the ladle rather than "
                "pour - let it rest 10 minutes so the flour takes up the liquid, and heat the iron "
                "until a drop of water skitters on it. Fill it three-quarters so the steam can "
                "escape, and stand the cooked ones on a rack in a low oven rather than stacking "
                "them, because a stack steams itself soft.")
    if has("flapjack", "flapjacks", "oat bar", "oat bars"):
        if has("set", "firm", "firmed", "runny", "syrup", "sloppy", "sticky", "soggy", "soft"):
            return ("A flapjack that will not set wants less liquid or more oats: about 25g more "
                    "oats and 2 tablespoons less syrup, pressed down hard into the tin with the "
                    "back of a spoon before it bakes. Bake it at 180C (160C fan) for 25 minutes "
                    "until the edges are golden, then leave it in the tin until it is completely "
                    "cold - warm flapjacks are always soft and they firm up as they cool.")
        return ("Flapjacks that crumble were cut warm or short of syrup: cool them completely in "
                "the tin, then cut with a sharp knife straight down, and add 2 tablespoons more "
                "golden syrup or honey to the next batch. Pack the mix down firmly before it "
                "bakes, because a loose tray bakes into crumbs.")
    if has("brownie", "brownies"):
        if has("dry", "cakey", "cake-like", "crumbly", "overbaked", "overbaked", "too long",
               "hard", "stale"):
            return ("A dry brownie stayed in the oven too long or went into too big a tin: 20 to "
                    "25 minutes at 180C (160C fan) in a 20cm square tin, and take it out while "
                    "the middle still looks slightly under, because it sets as it cools. Melt the "
                    "butter and chocolate together gently rather than boiling them, and keep the "
                    "flour light - it is there to hold the brownie together, not to make a cake.")
        return None
    if has("scone", "scones"):
        return ("Dense scones come from working the dough or a wet mix: use cold butter, rub it in "
                "until it looks like breadcrumbs, and bring it together with a knife and one fold "
                "rather than kneading. Pat it 2cm thick, cut straight down with a floured cutter "
                "and bake at 220C (200C fan) for 12 to 15 minutes, because a slow oven sets them "
                "heavy.")
    return None

ENTRIES = [
    entry("cook-from-a-corner-shop",
          (("corner shop", "corner shop", "cornershop", "local shop", "little shop",
            "convenience store", "newsagent", "newsagents", "garage shop", "petrol station",
            "spar", "co-op", "coop", "one stop", "londis", "premier", "nisa", "budgens"),
           ("cook", "cooking", "made", "make", "making", "eat", "dinner", "supper", "lunch",
            "ingredients", "meal", "recipe", "tonight", "stuff", "ingredient")),
          "A corner shop covers more of a dinner than people expect: rice, pasta, eggs, tinned "
          "beans and chickpeas, tinned tomatoes, frozen peas, onions, potatoes, milk, cheese and "
          "a curry powder or stock cubes. What it will not have is fresh herbs, good bread or "
          "anything unusual, so take the dried or tinned version rather than going without. "
          "Rice, eggs and frozen peas make fried rice in 15 minutes, and a tin of chickpeas with "
          "an onion and curry powder is a curry in 25.",
          avoid=("open", "opening", "closed", "closing", "hours", "refund", "complaint",
                 "complain", "delivery", "deliver", "price", "prices", "cost", "cheaper",
                 "near me", "nearest", "parking", "stock", "in stock", "sold out")),
    entry("plan-sides",
          (("what about", "how about", "shall i", "should i", "go with", "alongside", "serve",
            "with", "side", "sides", "need", "any", "and"),
           ("rice", "potato", "potatoes", "salad", "lettuce", "bread", "naan", "pitta",
            "veg", "vegetables", "greens", "broccoli", "beans", "peas", "carrots", "gravy",
            "mash", "chips", "rolls", "slaw", "side", "sides")),
          _sides,
          avoid=("how long", "how do i", "recipe", "allergic", "sticky", "mushy", "gluey",
                 "leftover", "reheat", "water", "ratio", "freeze", "calories", "healthy",
                 "protein", "carbs", "carb", "carbohydrates", "nutrition", "nutrients",
                 "plant", "plants", "growing", "wrong", "yellow", "brown", "wilt", "dying",
                 "soil", "garden", "basil"),
          bias=-2),
] + [
    entry("plan-temp", (_RECIPE_CARDS, _temp_asks()[0]), _the_heat, ask=COOKING_WORDS, bias=3,
          avoid=("rise", "rises", "rising", "prove", "proves", "proving", "proof", "starter",
                 "yeast", "room temperature", "room temp", "fridge", "freezer", "serve",
                 "serving", "reheat", "warm through", "internal", "inside", "safe", "done",
                 "thermometer", "frying pan", "hob", "ring", "grill", "air fryer", "microwave",
                 "slow cooker", "pressure cooker", "bain marie", "water bath", "sugar",
                 "fever", "oven thermostat", "dial", "fan oven conversion", "gas to electric",
                 "bread and butter pudding", "garlic bread", "soda bread", "banana bread",
                 "bread sauce", "breadcrumbs", "bread crumbs", "breadsticks", "bread sticks",
                 "naan bread", "pitta bread", "pita bread")),
    entry("plan-followup", _asks(), _follow_up, ask=COOKING_WORDS, bias=-2,
          avoid=("interview", "interviews", "interviewer",
                 "plant", "plants", "houseplant", "houseplants", "pot plant", "soil", "compost",
                 "garden", "lawn", "grass", "basil", "tomato", "cucumber", "chilli", "herb",
                 "herbs", "mint", "coriander", "parsley", "watering", "repot", "wilt", "wilted",
                 "prune", "fertiliser",
                 "sleep", "slept", "bedtime", "nap", "exam", "exams", "revision", "revising",
                 "worktop", "worktops", "counter", "countertop", "counter top", "sink", "basin",
                 "bath", "enamel", "tile", "tiles", "grout", "plate", "plates", "mug", "mugs",
                 "bowl", "bowls", "laminate", "veneer", "granite", "quartz", "skirting",
                 "windscreen", "windshield")),

    entry("plan-keep", (tuple(PLAN_NAMES) + tuple(DISH_WORDS), KEEP_ASK_WORDS), _follow_up,
          ask=KEEP_ASK_WORDS, bias=-1,
          avoid=NOT_A_DISH + NOT_A_KEEPING_QUESTION + KEEP_QUALITY_WORDS + (
                 "from sinking", "from going soggy", "from sticking", "from burning",
                 "from going stale", "from collapsing", "from curdling", "from splitting",
                 "sinking", "sank", "sunken")),

    entry("plan-done", (DONE_POSSESSIVE, DONE_WORD), _follow_up, bias=-1,
          avoid=("how long", "minutes", "hours", "temperature", "temp", "degrees", "gas mark",
                 "why", "fix", "soggy", "dry", "burnt", "bland", "watery", "raw", "pink",
                 "safe", "keep", "keeps", "fridge", "freezer", "freeze", "reheat",
                 "leftover", "leftovers", "defrost", "store")),

    entry("plan-start", START_WORDS, _start, bias=-3,
          avoid=("what can i", "what should i", "what do i", "what could i", "can i make",
                 "can i cook", "should i make", "how do i", "any idea", "ideas for",
                 "whats good", "what's good",
                 "job", "jobs", "new job", "interview", "career", "shift", "shifts",
                 "school", "term", "exam", "exams", "college", "university", "uni",
                 "course", "class", "classes", "gym", "diet", "marathon",
                 "dieting", "new year", "resolution", "resolutions")),

    entry("dough-sticking", (("dough", "sourdough", "bread dough", "pastry", "banneton",
                              "flour", "knead", "kneading", "rolling pin", "springform"),
                             ("sticking", "sticks", "sticky", "stick", "stuck", "tacky",
                              "bench", "counter", "worktop", "hands", "banneton",
                              "rolling pin", "surface")),
          _dough_sticks,
          bias=1,
          avoid=("tin", "tins", "pan", "pans", "paper", "parchment", "baking paper", "lining",
                 "grease", "greasing", "cake", "sponge", "pasta", "spaghetti", "noodles", "rice",
                 "boil", "boiling", "saucepan", "shape", "shaping", "too sticky", "handle",
                 "tearing", "tears", "torn", "cracks", "crumbling", "dry",
                 "split", "splits", "splitting", "splinter", "splinters", "splintered",
                 "cracked", "rough", "sanded", "sand it",
                 "recipe", "from scratch", "by hand")),
    entry("veg-tough",
          (VEG_FAULTS, VEG_NAMES),
          lambda memory, understood: _veg_fix(_line_text(understood)),
          bias=2,
          avoid=("meat", "chicken", "beef", "pork", "lamb", "turkey", "steak", "water",
                 "tap", "decision", "choice", "exam", "interview", "day", "week",
                 "dried", "dry", "soak", "soaking", "soaked", "overnight", "bag", "bags",
                 "tinned", "canned", "chickpeas", "lentils", "kidney beans", "butter beans",
                 "haricot", "cannellini", "pinto", "split peas")),

    entry("plan-problem",
          (tuple(word for key in PROBLEMS for word in PROBLEMS[key][0]),
           ("why", "always", "keeps", "comes", "come", "out", "wrong", "fix", "stop", "how",
            "do", "i", "my", "the", "is", "are", "it", "what", "can", "going", "every",
            "time", "make", "not", "so")),
          _problem,
          ask=COOKING_WORDS,
          guard=a_plan_that_might_be_ruined,
          bias=-2,
          avoid=("skin", "hands", "hair", "washing", "weather", "tumble", "dryer", "wine",
                 "sense of humour",
                 "hot water", "heating", "heating bill", "boiler", "electricity", "gas bill",
                 "energy bill", "thermostat", "radiator")),

    entry("plan-diet", (tuple(w for _n, words, _s in DIETS for w in words),
                        ("i", "im", "am", "we", "them", "they", "guest", "guests", "friend",
                         "friends", "mate", "mates", "son", "daughter", "mum", "dad", "mother",
                         "father", "sister", "brother", "partner", "wife", "husband", "one",
                         "someone", "everyone", "doesnt", "doesn't", "wont", "won't", "cant",
                         "can't", "avoids", "avoid", "has")),
          _diet, bias=1,
          guard=not_a_mark_on_a_thing,
          avoid=("allergy", "allergic", "anaphylaxis", "epipen", "intolerance", "coeliac",
                 "how do i", "how long", "do i have", "in the fridge", "in the cupboard",
                 "celiac", "is it bad", "good for you", "calories", "protein", "vitamin",
                 "healthy", "health", "weight", "pregnant", "pregnancy", "baby", "child",
                 "children", "when i was", "used to",
                 "breastfeeding", "breast feeding", "breast-feeding", "nursing", "lactating",
                 "chestfeeding", "while im feeding",
                 "out of date", "past its date", "past the date", "use by", "best before",
                 "gone off", "gone sour", "smells off", "smells sour",
                 "breastfeeding", "breast feeding", "nursing", "while feeding", "lactating",
                 "chestfeeding",
                 "antibiotic", "antibiotics", "penicillin", "amoxicillin", "doxycycline",
                 "lymecycline", "tetracycline", "ciprofloxacin", "trimethoprim",
                 "nitrofurantoin", "metronidazole", "statin", "statins", "simvastatin",
                 "atorvastatin", "rosuvastatin", "pravastatin", "warfarin", "blood thinner",
                 "blood thinners", "anticoagulant", "anticoagulants", "inr", "apixaban",
                 "rivaroxaban", "levothyroxine", "thyroxine", "tablet", "tablets", "medicine",
                 "medicines", "medication", "pills", "prescription",
                 "can i eat", "can i have", "can i drink", "should i eat", "should i have",
                 "is it ok to eat", "is it okay to eat", "is it fine to eat",
                 "is it safe to eat", "am i allowed to eat")
                 + DAY_WORDS),

    entry("plan-veggie", (VEGGIE_KEY, VEGGIE_CARRIERS), _veggie, bias=1,
          guard=not_a_present,
          avoid=("healthy", "health", "protein", "iron", "b12", "deficiency", "vitamin",
                 "child", "children", "baby", "weight", "muscle", "pregnant", "calcium")),

    entry("plan-dislike", (DISLIKE_SHAPES, DISLIKED), _dislike, bias=2,
          avoid=("allergy", "allergic", "anaphylaxis", "epipen", "intolerance", "coeliac",
                 "celiac", "anaphylactic", "in the house", "in the fridge",
                 "shopping", "buy", "calories", "protein", "is it bad",
                 "fancy", "no fuss", "fuss", "plain", "basic", "cheap", "skint", "budget",
                 "quick meal", "meal idea", "meal ideas", "meal tonight",
                 "what can i make", "what can i cook", "what should i cook", "use up",
                 "use it up", "leftover", "leftovers",
                 "out of the fridge", "out of the freezer", "overnight", "all night",
                 "out of date", "past its date", "past the date", "past their date",
                 "use by", "best before", "gone past",
                 "run out of", "ran out of", "running out of", "runs out of", "have run out",
                 "has run out", "none left", "nothing left")),
    entry("plan-pudding",
          (("what", "shall", "should", "can", "make", "made", "cook", "serve", "goes", "go",
            "with", "idea", "ideas", "suggest", "finish", "and", "about", "for", "need", "want",
            "have", "got", "fancy", "give", "tonight"),
           DESSERT_WORDS),
          _pudding, bias=3,
          ask=("make", "made", "making", "cook", "cooked", "serve", "serving", "idea", "ideas",
               "suggest", "something", "shall", "should", "can", "finish", "need", "needs",
               "want", "wants", "fancy", "give", "any", "and",
               "goes", "go", "pair", "pairs",
               "whats", "what's", "what are", "what else", "who wants",
               ),
          avoid=(
                 "run", "runs", "running", "jog", "jogging", "jogged", "exercise", "exercising",
                 "exercised", "gym", "training", "workout", "work out",
                 "broken", "broke", "fracture", "fractured", "cast", "plaster", "sprain",
                 "sprained", "injury", "injured", "operation", "surgery", "heal", "healing",
                 "recovery", "wrist", "ankle", "collarbone", "rib", "ribs", "hip", "shoulder",
                 "stretch", "stretches", "stretching", "warm up", "warming up", "cool down",
                 "run", "runs", "running", "jog", "jogging", "jogged", "exercise", "gym",
                 "training", "workout",
                 "ibuprofen", "paracetamol", "aspirin", "naproxen", "painkiller", "painkillers",
                 "tablet", "tablets", "medicine", "medicines", "medication", "antibiotic",
                 "antibiotics", "steroid", "steroids", "vitamin", "vitamins",

                 "calorie", "calories", "healthy", "health", "sugar", "diabetes", "diabetic",
                 "diabetics", "insulin", "blood sugar", "unhealthy", "bad for you", "bad for me",
                 "is it bad", "bad to eat", "every day", "every night", "everyday", "diet",
                 "tooth", "teeth", "sweet potato", "sweetcorn", "black pudding", "yorkshire",
                 "wine", "wines", "port", "sherry", "liqueur", "gift", "present",
                 "christmas pudding", "custard powder", "allergic", "allergy", "recipe",
                 "how long", "how do i", "how to", "buy", "shop", "supermarket", "restaurant",
                 "screen", "screens", "display", "phone", "iphone", "android", "laptop",
                 "computer", "pc", "monitor", "telly", "tv", "timeout", "time out", "minutes",
                 "locks", "lock screen", "brightness",
                 "what i have", "i have", "i've got", "ive got", "nothing in", "cupboard",
                 "leftover", "left over", "in the house", "no eggs",
                 "stink", "stinks", "stinking", "stank", "smell", "smells", "smelly", "smelling",
                 "reek", "reeks", "odour", "pong", "pongs", "musty",
                 "fix", "salvage", "rescue", "ruined", "came out", "come out", "went wrong",
                 "too sweet", "too dry", "too runny", "too wet", "too heavy", "soggy",
                 "sunk", "sunken", "burnt", "burned", "flat", "failed", "split",
                 "didnt set", "did not set", "stodgy",
                 "why", "crave", "craves", "craving", "cravings",
                 "savoury pudding", "savory pudding", "steak and kidney", "suet",
                 "white pudding", "pease pudding",
                 "career", "careers", "job", "jobs", "nursing", "nurse", "nurses", "midwife",
                 "midwifery", "retrain", "retraining", "retrained", "apprenticeship",
                 "college", "university", "degree", "qualification", "qualifications",
                 "salary", "wage", "wages", "promotion", "interview", "probation")),
    entry("plan-ideas", (IDEA_SHAPES, IDEA_CARRIERS), _idea, bias=-2,
          avoid=("gift", "gifts", "present", "presents",
                 "place to buy", "where to buy", "where can i buy", "cheapest place",
                 "price", "prices", "warranty", "guarantee",
                 "frozen", "freezer", "freeze", "defrost", "defrosted", "thaw", "thawed",
                 "easter egg", "easter eggs", "christmas cake", "christmas pudding",
                 "play dough", "playdough", "decorate", "decorating",
                 "dye", "dyeing", "paint", "painting",
                 "smoking", "smokes", "sparking", "wont heat", "won't heat", "not heating",
                 "stopped working", "wont switch on", "wont turn on", "leaking", "tripping",
                 "dead", "no power", "wont come on", "has stopped working", "isnt heating",
                 "won't heat", "wont heat up", "not heating up", "blowing the fuse",
                 "raw", "reheat", "reheated", "left out", "gone off", "dessert", "pudding",
                 "sweet", "cake", "biscuits", "cookies", "breakfast", "cold", "iced",
                 "bored", "bored of", "sick of", "tired of", "fed up", "had enough",
                 "something else", "anything else", "what else")),
] + [
    entry("spice-bloom",
          (("fry the spices", "frying the spices", "fry spices", "frying spices", "fry my spices",
            "fry the spice", "toast the spices", "toast spices", "toasting spices",
            "toasted spices", "toast my spices", "bloom the spices", "bloom spices",
            "blooming the spices", "blooming spices", "temper the spices", "tempering the spices",
            "whole spices", "cook the spices", "cooking the spices", "spices in oil",
            "spices first", "spices before", "spices go in", "spices at the start",
            "add the spices", "add my spices", "add spices", "add the spice",
            "spices to a curry", "spices to the pan", "when do i add the spices",
            "when do you add the spices", "when should the spices",
            "whole cumin", "cumin seeds", "cumin seed", "mustard seeds", "coriander seeds",
            "fennel seeds", "cardamom pods", "cardamom", "star anise", "cinnamon stick",
            "fenugreek", "ajwain", "curry leaves", "dried chillies"),
           ("fry", "frying", "fried", "toast", "toasting", "toasted", "roast", "roasting",
            "roasted", "bloom", "blooming", "bloomed", "temper", "tempering", "do", "should",
            "can", "need", "have to", "must", "when", "first", "before", "how", "worth",
            "necessary", "order", "start", "starting", "begin", "beginning", "always")),
          ("Fry them first: whole spices go into a little oil over a medium heat for 30 seconds "
           "to a minute, until they smell warm and one or two start to pop, because the oil "
           "carries the flavour that water cannot. Ground spices need only 20 to 30 seconds, "
           "added with the onion or just before the liquid goes in. Keep the heat moderate and "
           "have the next ingredient ready: a spice that darkens has gone bitter and cannot be "
           "rescued."),
          avoid=("which spices", "what spices", "how much spice", "what spice", "too spicy",
                 "too hot", "spice up", "relationship", "mild", "hotter", "milder", "spicy",
                 "pantry", "cupboard", "ran out", "havent got",
                 "have not got", "no spices", "shop", "buy", "substitute", "instead of",
                 "sow", "sowing", "plant", "planting", "grow", "growing", "germinate", "garden",
                 "allotment", "soil", "compost", "prune", "flower", "flowers")),
    entry("brine-bird",
          (("brine", "brining", "brined", "wet brine", "wet brined"),
           ("turkey", "chicken", "bird", "crown", "joint", "pork", "how", "should", "long",
            "overnight", "worth it", "need to", "have to")),
          "Dissolve about 50g of salt in a litre of cold water - roughly 2 litres for a whole "
          "bird - and keep it in the fridge for an hour for every kg, or overnight for a "
          "chicken. A big pan or a clean bag works, with something on top to keep the bird "
          "under. Dry the skin well before it goes in the oven and add no more salt; a brined "
          "bird browns faster, so cover the top with foil for the first half hour.",
          avoid=("gargle", "gargling", "sore throat", "throat", "wound", "cut", "saline",
                 "rinse", "mouth", "fish tank", "aquarium", "pool", "swimming", "bath", "soak",
                 "drink",
                 "defrost", "thaw", "frozen", "freeze", "leftover", "leftovers", "stock",
                 "carcass", "gravy", "stuffing", "stuffed", "dry", "juicy", "calories",
                 "price", "how long do i roast", "how long to roast", "temperature"),
          bias=2),
    entry("bake-fault-more",
          (("waffle", "waffles", "flapjack", "flapjacks", "oat bar", "oat bars", "scone",
            "scones", "brownie", "brownies"),
           ("soggy", "limp", "soft", "went soft", "stodgy", "dense", "heavy", "chewy",
            "rubbery", "fell apart", "falling apart", "falls apart", "crumbled", "crumbles",
            "crumbling", "dry", "crumbly", "tough", "wont set", "won't set", "didnt set",
            "didn't set", "not set", "runny", "sloppy", "sticky", "didnt rise", "didn't rise",
            "no rise", "flat", "pale", "soggy middles")),
          _bake_fault_more,
          avoid=("how do i make", "how to make", "recipe", "keep", "keeps", "store", "storing",
                 "freeze", "freezing", "frozen", "reheat", "calories", "healthy", "how long do",
                 "how long to", "topping", "toppings", "fill", "filling", "filling the",
                 "iron wont heat", "iron does not heat", "burnt", "burning", "burns",
                 "stale", "stales")),
    entry("hidden-veg",
          (("hide", "hiding", "hidden", "sneak", "sneaking", "sneaked", "disguise", "smuggle",
            "hide veg", "hide vegetables", "hide the veg", "hide the vegetables",
            "hiding veg", "hiding vegetables", "hidden veg", "hidden vegetables",
            "way to hide vegetables", "ways to hide vegetables", "way to hide veg",
            "hide them in", "hide it in", "sneak them in", "sneak it in", "hide them",
            "does that work", "does it work", "would that work", "would it work",
            "will that work"),
           VEG_WORDS + (
               "them in food", "them in a sauce", "them in the sauce", "it in food",
               "them in his food", "them in her food", "them in their food",
               "them in a meal", "them in meals", "them in dinners", "them in dinner",
               "sauce", "lasagne", "bolognese", "chilli", "soup", "mash", "muffin", "muffins",
               "curry", "stew", "pasta", "smoothie", "omelette", "burger", "burgers",
               "meatballs", "pie", "risotto")),
          "Grate or blitz it into something wet and strongly flavoured: a grated carrot or "
          "courgette in bolognese, chilli, lasagne or a tomato sauce disappears, and a handful "
          "of spinach or a few peas blitzed into soup leaves nothing to pick out. Mash takes "
          "half cauliflower, and grated carrot or beetroot goes into muffins and a fruit loaf "
          "unnoticed. Keep the plain veg on the plate too - hiding gets the vitamins in, but it "
          "does not teach anyone to like it.",
          avoid=("hide and seek", "hide the presents", "hide presents", "hide a key", "hide keys",
                 "spare key", "hide money", "hide cash", "hide the money", "hide the wires",
                 "wires", "cables", "hide the mess", "hide a mess", "stains", "hide a spot",
                 "hide spots", "acne", "bruise", "bruises", "scar", "scars", "dark circles",
                 "grey hair", "hide my belly", "hide my tummy", "homework", "evidence",
                 "hide the smell", "smell of weed", "hide from", "tablet", "tablets",
                 "worming", "medicine", "medication", "pill", "pills",
                 "birthday", "surprise", "presents", "party bag"), bias=2),
]

ANSWERS = ("cooking", "food-and-drink")

ENTRIES.append(entry(
    "eating-out-choose", (OUT_WORDS, OUT_ASK),
    "Decide in this order, because each one removes half the list: set a budget per head and a "
    "distance you will actually travel, then pick a place whose menu is short - eight good dishes "
    "beats forty average ones - and read the reviews from the last month, not the star average. If "
    "two are still level, choose the one you would be sorry to lose; if neither would bother you, "
    "the cheaper one is fine. Still stuck, book a table rather than a takeaway: a table settles it "
    "and you eat something that is not from a box.",
    avoid=OUT_AVOID + ("birthday", "party", "kids", "children", "christening", "wedding",
                       "funeral", "wake", "buffet", "how much food", "how many",
                       "shopping", "supermarket", "list", "meal plan", "meal prep",
                       "holiday", "holidays", "weekend away", "night out", "pub crawl",
                       "few days", "couple of days", "for a few days", "days away", "week in",
                       "concert", "cinema", "what to watch",
                       "chippy", "chip shop", "curry house", "kebab", "chinese", "indian",
                       "thai", "deliveroo", "just eat", "uber eats", "fish and chips",
                       "what should i get", "what should we get", "what do i get",
                       "what do we get", "what should i order", "what should we order",
                       "what to order", "what to get",
                       "what should i eat", "what should we eat", "what to eat",
                       "what should i have", "what should we have", "whats good",
                       "whats nice", "what do you recommend")))

ORDER_AT_A_PLACE = (
    "pub", "restaurant", "restaurants", "cafe", "canteen", "food court", "bistro", "brasserie",
    "carvery", "nandos", "wetherspoons",
    "sushi", "italian", "mexican", "greek", "turkish", "japanese", "korean", "vietnamese",
    "spanish", "french", "pizza", "burger", "tapas", "ramen", "noodle bar",
    "menu", "the menu", "set menu", "tasting menu", "lunch menu", "dinner menu", "specials",
    "specials board", "wine list", "a la carte", "prix fixe")

ORDER_AT_A_PLACE_ASK = (
    "what should i order", "what should we order", "what to order", "what do i order",
    "what shall i order", "what should i get", "what should we get", "what do i get",
    "what should i eat", "what should we eat", "what to eat", "what should i have",
    "what should we have", "whats good", "whats nice", "whats best", "anything good",
    "anything nice", "what do you recommend", "what would you recommend", "what would you get",
    "what would you order", "whats your pick",
    "help me pick", "help me choose", "help me decide", "cant choose", "can't choose",
    "cannot choose", "cant decide", "can't decide", "what would you pick", "what do you pick",
    "what should i choose", "what should we choose")

ENTRIES.append(entry(
    "order-at-a-place", (ORDER_AT_A_PLACE, ORDER_AT_A_PLACE_ASK),
    "Order the thing you would not cook at home, and one shared starter for the middle: a main "
    "each and a side between two is plenty. Ask what is good tonight - the kitchen knows what came "
    "in fresh - and say yes to the dish you cannot quite pronounce.",
    avoid=("takeaway", "take away", "take-away", "takeout", "take out", "order in", "delivery",
           "deliveroo", "just eat", "uber eats", "chippy", "chip shop", "curry house", "kebab",
           "fish and chips",
           "for the week", "this week", "next week", "weekly", "plan", "planning", "meal plan",
           "party", "birthday", "christmas", "wedding", "buffet", "design", "print", "printing",
           "my cafe", "my restaurant", "my pub", "pricing", "profit", "allergen", "allergens")
    + OUT_AVOID))

ENTRIES.append(entry(
    "what-the-menu-words-mean",
    (("set menu", "set menus", "a la carte", "prix fixe", "tasting menu", "tasting menus",
      "table d'hote", "table d'hôte"),
     ("what is", "what are", "what does", "what do", "meaning", "mean", "difference",
      "different", "explain", "explained", "whats the",
      "cheaper", "worth it", "worth", "value", "better value", "best value", "more expensive")),
    "A set menu is one fixed price for two or three courses chosen from a short list, and it is "
    "usually the best value on the board. A la carte is the full list with every dish priced on "
    "its own, so you pay for exactly what you want and nothing else. A tasting menu is a run of "
    "small courses the kitchen decides, priced per person and taken by the whole table. If you "
    "want the cheapest good meal, order the set menu; if there is one dish you really came for, "
    "order that a la carte.",
    avoid=("what should i", "what should we", "what shall i", "what shall we", "what do i order",
           "what to order", "whats good", "whats nice", "recommend", "pick", "choose",
           "cant decide", "can't decide"),
    bias=1))

ENTRIES.append(entry(
    "takeaway-order", (("takeaway", "take away", "take-away", "takeout", "take out", "order in",
                        "delivery", "deliveroo", "just eat", "uber eats", "chippy", "chip shop",
                        "curry house", "kebab", "chinese", "indian", "thai", "fish and chips"),
                       ("what should i", "what should we", "what do i", "what can i",
                        "what shall i", "what shall we", "what to order", "what to get",
                        "whats nice", "whats good", "whats best", "whats the best",
                        "what is nice", "what is good", "what is best", "what are the best",
                        "best thing", "good thing", "nicest", "tastiest", "anything nice",
                        "anything good",
                        "what should i get", "what should we get",
                        "should we get", "should i get",
                        "what would you", "same", "bored of", "sick of",
                        "cant decide", "can't decide", "decide", "choose", "pick", "fancy",
                        "craving", "recommend", "ideas", "suggest")),
    "Order the thing you would not cook at home, and get one more dish than there are people so "
    "there is something left cold for tomorrow: a shared starter, a main each, one side for two "
    "people. On a Chinese that is a soup or the salt and pepper ribs, two mains with rice between "
    "them, and a vegetable; on an Indian it is a dry dish and a wet one, a bread and a rice, not "
    "three curries; on a chippy it is one large chips for two. Collect it if you can - it arrives "
    "hot instead of steamed - and ask for sauces on the side.",
    avoid=OUT_AVOID + ("calories", "how many", "much", "how long", "keep", "reheat", "freeze",
                       "leftover", "recipe", "birthday", "christening", "funeral", "wake",
                       "tonight", "or cook", "or not", "twice a week", "every week", "at the weekend",
                       "how often", "healthy")))
_TWO_OVEN_HEAD = ("Yes, if they want heat within about 20C of each other: put the hotter dish in "
                  "first, or give the slower one a head start, and swap the two trays on their "
                  "shelves halfway through.")
_TWO_OVEN_GAP = ("Leave a finger's gap round each tray, keep the one that needs to brown in the "
                 "middle, and add 5 to 10 minutes because two trays cut the heat - a fan oven "
                 "copes better than a gas one.")
_TWO_OVEN_CAKE = ("A delicate cake should not go in beside a roast, because it takes on the fat "
                  "and the steam: bake the cake in the morning and put the roast in later, or the "
                  "other way round.")
_TWO_OVEN_SPONGE = ("A 20cm sponge needs 25 to 30 minutes at 180C, so it can come out while the "
                    "roast rests.")
_TWO_OVEN_BEEF = ("beef", "lamb", "ham", "pork", "joint", "meat")


def _two_dishes_plan(memory, understood):
    text = " " + str((understood or {}).get("clean") or "").lower() + " "
    if "cake" in text and ("roast" in text or any(" " + word + " " in text
                                                  for word in _TWO_OVEN_BEEF)):
        return " ".join((_TWO_OVEN_CAKE, _TWO_OVEN_SPONGE))
    return " ".join((_TWO_OVEN_HEAD, _TWO_OVEN_GAP, _TWO_OVEN_CAKE, _TWO_OVEN_SPONGE))


ENTRIES.append(entry(
    "cake-size", CAKE_KEY, _cake_plan, avoid=CAKE_AVOID, bias=2))
ENTRIES.append(entry(
    "cake-eggs", CAKE_EGGS_KEY, _cake_eggs, avoid=CAKE_EGGS_AVOID, bias=1))
ENTRIES.append(entry(
    "two-dishes-one-oven",
    (("two dishes", "two things in the oven", "two trays in the oven",
      "two tins in the oven", "both dishes", "one oven", "same oven",
      "two things", "two trays at once", "two tins at once", "two dishes at once",
      "two cakes at once", "two sponges at once", "two tins of cake", "two cake tins",
      "share an oven", "share the oven", "both in the oven",
      "a roast and a cake", "roast and a cake"),
     ("oven", "cook", "cooking", "bake", "baking", "roast", "roasting", "tray",
      "trays", "tin", "tins", "shelf", "shelves", "fit")),
    _two_dishes_plan,
    avoid=("air fryer", "airfryer", "microwave", "slow cooker", "slow-cooker", "pressure",
           "not heating", "wont heat", "won't heat", "not working", "broken", "smell",
           "smoke", "door", "light", "element", "fan", "noisy", "clean", "cleaning",
           "christmas", "buffet", "barbecue", "bbq", "freezer", "fridge", "freeze",
           "reheat", "defrost", "temperature", "gas mark", "hot", "fan oven",
           "potatoes", "roast potatoes", "chicken", "scones", "pizza", "pizzas",
           "bread", "salmon", "sausages", "sausage rolls", "yorkshire", "chips",
           "lasagne", "casserole", "vegetables", "muffins", "cookies", "biscuits",
           "two things together"),
    bias=1))




DISH_WHAT = (
    ("yorkshire-pudding",
     ("yorkshire pudding", "yorkshire puddings", "yorkies", "yorkie puds", "yorkshire puds"),
     "A Yorkshire pudding is a batter of plain flour, eggs and milk baked in a thin layer of "
     "smoking-hot beef dripping or oil, so it puffs up crisp at the edges and soft in the "
     "middle. The fat has to be almost smoking before the batter goes in and the oven door stays "
     "shut for the first twenty minutes, or it will not rise. It is served with roast beef and "
     "gravy, and the batter makes toad in the hole around sausages."),
    ("toad-in-the-hole",
     ("toad in the hole", "toad in the hole"),
     "Toad in the hole is sausages baked in a Yorkshire pudding batter, in one roasting tin, so "
     "the batter rises around them and the sausages flavour it. Brown the sausages first in the "
     "tin with a little oil, get that fat hot, then pour the batter in and bake at 220C (200C "
     "fan) for 25 to 30 minutes. Onion gravy over the top is the usual thing."),
    ("black-pudding",
     ("black pudding", "black puddings"),
     "Black pudding is a sausage of pig's blood, pork fat, oatmeal and seasoning, sliced thick "
     "and fried until the outside crisps - it is a blood sausage, not a dessert. Stornoway and "
     "Bury are the ones people argue about. It is eaten with a full breakfast, or crumbled into "
     "scallops and apple."),
    ("steak-and-kidney-pudding",
     ("steak and kidney pudding", "steak and kidney puddings"),
     "Steak and kidney pudding is diced beef and kidney with gravy, sealed under a suet pastry "
     "crust and steamed for three or four hours rather than baked, then turned out onto the "
     "plate. The suet crust is what makes it a pudding: it stays light and soaks up the gravy, "
     "where a shortcrust would go heavy. If you want it brown on top, the pastry was baked and "
     "that is a pie."),
    ("bara-brith",
     ("bara brith", "bara brith bread"),
     "Bara brith means speckled bread in Welsh: a fruit loaf of dried fruit, brown sugar and "
     "mixed spice, usually with the fruit soaked overnight in strong tea first. It is baked in "
     "a loaf tin like a cake, left a day to settle, then sliced and buttered. It keeps a week in "
     "a tin and is better on the second day."),
    ("parkin",
     ("parkin", "parkin cake", "yorkshire parkin"),
     "Parkin is a sticky ginger cake from Yorkshire and Lancashire, made with oatmeal, black "
     "treacle, golden syrup and ground ginger - oats in a cake is what makes it chewy rather "
     "than spongy. It comes out soft and improves for three or four days in a tin, so it is "
     "made for bonfire night and eaten the week after. Cut it into squares, not slices."),
    ("cobbler",
     ("cobbler", "fruit cobbler", "peach cobbler"),
     "A cobbler is fruit baked under rough spoonfuls of scone dough, so the topping comes out "
     "cobbled rather than rolled flat - it is American, and it is not a pie or a crumble. The "
     "fruit should be bubbling at the edges and the topping golden, and the dough wants a "
     "spoonful of sugar and a little salt in it. Cream or custard over the top, hot."),
    ("stovies",
     ("stovies", "stovie"),
     "Stovies is a Scottish one-pot of potatoes, onions and leftover roast meat cooked slowly in "
     "dripping or stock until the potatoes break down - the name comes from stoving, cooking "
     "slowly in a closed pot. It is made from what is left of a Sunday roast, so it is thrifty "
     "by design. Serve it with oatcakes and a pickled beetroot on the side."),
    ("colcannon",
     ("colcannon",),
     "Colcannon is mashed potato with cooked cabbage or kale folded through it and plenty of "
     "butter, and it is a Halloween dish in Ireland - a ring or a coin used to be hidden in the "
     "pan. Champ is the same idea made with spring onions instead of cabbage. Warm milk and "
     "butter go in last, off the heat, or the mash goes gluey."),
    ("frittata",
     ("frittata", "frittatas"),
     "A frittata is an Italian open omelette of eggs and whatever is in the fridge, cooked slowly "
     "in a pan and then finished under the grill or in the oven so the top sets without the "
     "bottom burning. It is thicker than an omelette and cut in wedges, and it is as good cold "
     "the next day. Cook the vegetables first and drain anything wet, or it will weep."),
    ("tagine",
     ("tagine", "tagines", "tajine"),
     "A tagine is a Moroccan stew named after the conical clay pot it is cooked in: meat, usually "
     "lamb or chicken, with spices, dried fruit and often preserved lemon or olives, cooked low "
     "and slow so it comes out sweet and savoury at once. A heavy pan with a lid does the same "
     "job in an oven at 160C. Couscous or flatbread to mop it up."),
    ("ragu",
     ("ragu", "ragù", "ragus", "bolognese sauce", "bolognese"),
     "A ragu is a slow-cooked Italian meat sauce: onion, carrot and celery softened first, then "
     "mince or a whole piece of meat, wine, a little milk and tomatoes, simmered for two hours "
     "or more - bolognese is one of them. The long cook and the milk are what make it rich "
     "rather than sharp. In Bologna it is served with tagliatelle, because the ragù clings to "
     "the wide strands."),
    ("pilaf",
     ("pilaf", "pilau", "pilaff", "pilafs"),
     "A pilaf is rice fried in a little fat with onion first, then cooked in measured stock with "
     "the lid on and left alone, so every grain stays separate - where a risotto is stirred and "
     "a plain rice is boiled and drained. One part rice to one and a half parts stock, twelve "
     "minutes, then ten minutes off the heat. Dried fruit, nuts or cumin go in at the frying "
     "stage."),
    ("fricassee",
     ("fricassee", "fricassée", "fricasseed chicken"),
     "A fricassee is chicken, rabbit or veal cut into pieces, browned lightly and then stewed in "
     "stock and finished with a white sauce of cream or egg yolk - a French method, and a mild, "
     "pale dish rather than a brown stew. It is what to cook when someone wants something gentle. "
     "Take it off the heat before the egg yolk goes in, or it curdles."),
    ("gratin",
     ("gratin", "gratins", "au gratin"),
     "A gratin is anything topped with cheese, butter and breadcrumbs and browned under the grill "
     "or in a hot oven until the top is crisp - gratin dauphinois is potato and cream cooked for "
     "two hours, and a gratin of pasta or cauliflower works the same way. The browned top is the "
     "point, so give it the last five minutes uncovered. Breadcrumbs on their own brown more "
     "evenly than cheese."),
    ("coulis",
     ("coulis", "fruit coulis"),
     "A coulis is a smooth sauce of raw or lightly cooked fruit blended and then pushed through a "
     "sieve, spooned over ice cream, cheesecake or pancakes - raspberry and mango are the usual "
     "ones. Sieving is what makes it a coulis rather than a purée, and a squeeze of lemon keeps "
     "the colour bright. A spoonful of icing sugar if the fruit is sharp."),
    ("casserole",
     ("casserole", "casseroles", "hotpot", "hot pot"),
     "A casserole is meat and vegetables cooked slowly in liquid in one lidded pot, in the oven "
     "or on the hob - the point is a cheap cut and a long cook, an hour and a half to two hours "
     "at 160C, so shin, shoulder and thighs come out tender. Brown the meat first and keep the "
     "liquid to about a third of the way up, or it turns into soup. Dumplings go on top for the "
     "last twenty minutes; a casserole dish is the pot it is cooked in, not the food."),
    ("bubble-and-squeak",
     ("bubble and squeak", "bubble n squeak"),
     "Bubble and squeak is leftover potatoes and cabbage or sprouts crushed together and fried in "
     "a hot pan until the underside is crusty brown - the name is the noise it made in the pan. "
     "Cold potatoes work better than fresh, because they have dried out. A fried egg on top "
     "makes it breakfast."),
    ("spotted-dick",
     ("spotted dick",),
     "Spotted dick is a steamed suet pudding with currants and raisins in it - the spots are the "
     "dried fruit - served with custard. It is made in a pudding basin, covered and steamed for "
     "an hour and a half rather than baked, which is why it is light rather than heavy. A spoon "
     "of golden syrup in the bottom of the basin is the usual trick."),
    ("beef-wellington",
     ("beef wellington", "wellington beef"),
     "Beef Wellington is a fillet of beef seared, coated in mushroom duxelles and sometimes pâté, "
     "wrapped in puff pastry and baked, then rested and carved in thick slices. The trick is "
     "chilling it after wrapping so the pastry does not go soggy, and a hot oven, 200C (180C "
     "fan), for about 25 minutes for medium rare. It is a dish for a celebration: the fillet is "
     "the expensive cut and it does not want cooking through."),
    ("scotch-egg",
     ("scotch egg", "scotch eggs"),
     "A Scotch egg is a hard-boiled egg wrapped in sausage meat, rolled in breadcrumbs and "
     "deep-fried, so the shell of meat keeps a little juice in and the yolk stays soft if it is "
     "boiled for six minutes first. The ones from a good butcher are a different thing from the "
     "chilled ones in a supermarket. Baked at 200C for 25 minutes works if you would rather not "
     "fry."),
    ("banoffee-pie",
     ("banoffee pie", "banoffi pie"),
     "Banoffee pie is a biscuit-and-butter base, a thick layer of toffee made by boiling a tin of "
     "condensed milk, sliced bananas and whipped cream on top, and none of it is baked. The "
     "toffee is the work: three hours in a pan of simmering water, and let the tin cool before "
     "opening it. Chill the pie for a few hours or it slumps when you cut it."),
    ("coronation-chicken",
     ("coronation chicken",),
     "Coronation chicken is cold cooked chicken in a mild curry and mayonnaise sauce with "
     "apricot, mango chutney or sultanas - a dish invented for the Queen's coronation in 1953, "
     "so it is meant to be gentle rather than hot. It goes in sandwiches, jacket potatoes or on "
     "a salad. Curry powder is better cooked in a little butter and cooled before it meets the "
     "mayonnaise."),
    ("haggis",
     ("haggis", "haggises"),
     "Haggis is a Scottish sausage of sheep's heart, liver and lungs minced with oatmeal, suet, "
     "onion and pepper, and boiled in a casing - it is a savoury pudding, traditionally served "
     "with neeps and tatties. The oatmeal and the pepper are what make it crumbly and warming. "
     "A vegetarian one is made with lentils and oats, and the good ones are as peppery as the "
     "meat."),
    ("hash",
     ("hash", "corned beef hash", "hash dinner"),
     "Hash is cooked meat and potatoes chopped up and fried together in a hot pan until the edges "
     "crisp - corned beef hash is the version most people mean, with onion and a little stock or "
     "gravy to keep it moist. It is a way to use up a Sunday roast, so the potatoes want to be "
     "cold and cooked. A fried egg or brown sauce on top is not optional for most people."),
    ("cornish-pasty",
     ("cornish pasty", "pasty", "pasty's", "pasties"),
     "A Cornish pasty is a half-moon of shortcrust pastry crimped along one edge, filled with "
     "beef skirt, potato, swede and onion, and baked without a tin - the raw filling cooks inside "
     "the sealed pastry, which is why it is juicy. It is eaten by hand, and the thick crimp was "
     "the handle for a miner's dirty fingers. Season it well inside: the pastry keeps the steam "
     "in, so a bland filling stays bland."),
    ("biscuit",
     ("biscuit", "biscuits"),
     "In Britain a biscuit is a small crisp baked thing - a digestive, a custard cream, a "
     "shortbread - while in America a biscuit is a soft soda-raised bread roll eaten with gravy. "
     "The British kind gets its snap from sugar, fat and a short bake: take them out while they "
     "are still slightly soft and they crisp as they cool. A soft biscuit has usually been stored "
     "with moisture, so keep them in a tin, not the fridge."),
    ("dripping",
     ("dripping", "beef dripping"),
     "Dripping is the fat that renders out of a beef roast and sets to a pale, grainy solid in the "
     "fridge - it is the best fat there is for roast potatoes and Yorkshire puddings, because it "
     "takes a much higher heat than oil without burning. Pour it off the roasting tin through a "
     "sieve into a jar, keep it in the fridge for weeks, and spoon out what you need. The dark "
     "jelly under it is the roasting juices and it goes in the gravy."),
    ("suet",
     ("suet", "beef suet"),
     "Suet is the hard white fat from around a cow's or sheep's kidneys, sold shredded and mixed "
     "with a little flour, and it is what makes a steamed pudding light and a dumpling fluffy - it "
     "melts slowly inside the dough and leaves air behind. Shortcrust and dumplings use it where a "
     "softer fat would go heavy. A vegetarian version made from palm or rice bran fat works the "
     "same way."),
    ("scotch-pancake",
     ("scotch pancake", "scotch pancakes", "drop scone", "drop scones"),
     "A Scotch pancake is a small thick pancake from a thick batter poured in spoonfuls onto a "
     "griddle - a drop scone - and it is eaten cold with butter or jam rather than hot with lemon. "
     "Self-raising flour and a rest of ten minutes before cooking give it the height, and the pan "
     "wants to be dry and only just hot enough. They freeze well and toast from frozen."),
    ("bap",
     ("bap", "baps", "barm", "barm cake", "cob", "roll with a crust"),
     "A bap is a soft white bread roll, usually with a floury top and a little milk or butter in "
     "the dough, and the same thing is a barm cake in Lancashire and a cob in the Midlands - it is "
     "the roll a bacon butty or a burger goes in. Softness is the point, so bake it hot and "
     "briefly and cover the rolls with a cloth as they cool. A bap is not a crusty roll, and the "
     "two are not swapped."),
    ("suet-pudding",
     ("suet pudding", "suet puddings", "steamed pudding", "steamed puddings"),
     "A suet pudding is a pudding made with shredded beef suet instead of butter - either a suet "
     "pastry around a filling, like steak and kidney pudding, or a suet sponge with dried fruit, "
     "like spotted dick. The suet melts as it steams, so it comes out light where a butter "
     "sponge would sit heavy. It is always steamed rather than baked, for one and a half hours "
     "and up, in a basin covered with paper."),
    ("bechamel",
     ("bechamel", "bechamel sauce", "white sauce"),
     "Bechamel is milk thickened with a roux of equal weights of butter and plain flour, cooked out "
     "for a minute so it stops tasting of raw flour, then seasoned with salt, pepper and a grating of "
     "nutmeg. It is the white sauce under lasagne and cauliflower cheese, and stirring in cheese "
     "turns it into a Mornay. Warm the milk first and whisk from the bottom of the pan to keep it "
     "smooth."),
    ("hollandaise",
     ("hollandaise", "hollandaise sauce"),
     "Hollandaise is egg yolks whisked over gentle heat until thick, then warm clarified butter "
     "whisked in drop by drop to make an emulsion, sharpened with lemon and salt. It is the sauce on "
     "eggs benedict. Keep it warm rather than hot, because boiling splits it, and a teaspoon of cold "
     "water whisked in often brings a split one back."),
    ("aioli",
     ("aioli", "garlic mayonnaise"),
     "Aioli is garlic pounded to a paste with salt, then olive oil whisked in to make a thick "
     "emulsion - in Provence that is all it is, and the version with egg yolk is mayonnaise with "
     "garlic. It is served cold with fish, boiled vegetables and bread. Pounding the garlic with a "
     "pinch of salt first stops it turning bitter."),
    ("veloute",
     ("veloute", "veloute sauce"),
     "A veloute is a roux loosened with white stock instead of milk, simmered until it coats a spoon "
     "and finished with cream or egg yolk. It is the base of a lot of classic French sauces. Use a "
     "stock you would drink on its own, because there is nothing in a veloute to hide a weak one."),
    ("mayonnaise",
     ("mayonnaise",),
     "Mayonnaise is egg yolk whisked with mustard, salt and vinegar, with oil added a little at a "
     "time until it thickens into an emulsion. The yolk is what holds the oil and the vinegar "
     "together. Eggs at room temperature and a slow drizzle at the start are what stop it splitting."),
    ("gravy",
     ("gravy",),
     "Gravy is the juices left in the roasting tin loosened with stock or wine, thickened a little "
     "with flour and simmered until it tastes of the meat. The flavour is in the browned bits stuck "
     "to the tin, so splash in hot stock and scrape them up. Stir in the juices from the rested joint "
     "at the end so they stay in the gravy."),
    ("pesto",
     ("pesto", "pesto sauce"),
     "Pesto is basil, pine nuts, garlic and parmesan pounded with olive oil into a coarse green paste "
     "- pounded in a mortar rather than blended, because a blade heats it and turns it bitter. Stir "
     "it into hot pasta off the heat with a spoonful of the cooking water to loosen it. Walnuts or "
     "almonds stand in for pine nuts."),
    ("vinaigrette",
     ("vinaigrette",),
     "A vinaigrette is oil and vinegar shaken together with salt, usually three parts oil to one of "
     "vinegar, with a little mustard to hold the two together. It is the dressing for a green salad "
     "and for cold vegetables. Make it in a jar and shake it again just before it goes on, because it "
     "separates as it stands."),
    ("chutney",
     ("chutney", "chutneys"),
     "Chutney is fruit or vegetables cooked down with vinegar, sugar and spice until thick and jammy, "
     "so it keeps for months in jars. The vinegar and sugar are what preserve it, so do not cut them "
     "down. An Indian chutney can also be a fresh uncooked relish, but the jarred British kind is the "
     "cooked one."),
    ("marinade",
     ("marinade", "marinades"),
     "A marinade is a liquid meat, fish or vegetables sit in before cooking: something acidic such as "
     "wine, vinegar, lemon or yoghurt, plus oil, salt and spice. It seasons the surface and "
     "tenderises a little, and the salt and the time matter more than the flavourings. Half an hour "
     "for fish, a few hours for chicken, overnight for a tough cut, always in the fridge."),
    ("brine",
     ("brine", "brining"),
     "Brine is salt water, about five per cent salt, that meat sits in before cooking so it takes up "
     "water and stays juicy. An hour for chops, four to twelve hours for a chicken or a turkey. Pat "
     "it dry before it goes in the pan or it will steam instead of browning."),
    ("glaze",
     ("glaze", "glazes"),
     "A glaze is a thin coating brushed onto food so it cooks to a shine: reduced stock, honey and "
     "soy, jam loosened with water, or sugar and butter. Brush it on towards the end, because the "
     "sugar in it burns before the food is cooked through. Brush again every few minutes so it builds "
     "in layers."),
    ("dry-rub",
     ("dry rub", "spice rub"),
     "A dry rub is salt, sugar and spices patted onto meat with no liquid, so the salt seasons it "
     "right through and the sugar helps the crust colour. Leave it on for half an hour at least, or "
     "overnight uncovered in the fridge for crisper skin. Pat off the loose spice before cooking so "
     "it does not burn."),
    ("soda-bread",
     ("soda bread", "soda breads"),
     "Soda bread is flour, bicarbonate of soda, salt and buttermilk with no yeast - the soda and the "
     "acid in the buttermilk make it rise as it bakes, so it is mixed and in the oven in minutes and "
     "eaten the same day. Handle the dough as little as possible and cut a cross in the top. It "
     "stales fast, so toast or freeze what is left."),
    ("focaccia",
     ("focaccia",),
     "Focaccia is a flat bread of soft wet dough stretched into an oiled tin, dimpled with the "
     "fingers and baked with olive oil, coarse salt and often rosemary. The dimples hold the oil, "
     "which is what makes the top crisp and the crumb light. It is meant to be wet, so resist adding "
     "flour to make it easier to handle."),
    ("ciabatta",
     ("ciabatta",),
     "Ciabatta is a very wet Italian white bread, around three parts water to four of flour, which is "
     "where the big irregular holes and the chewy crust come from. The dough is too sticky to knead "
     "by hand, so it is stretched and folded instead. Prove it slowly and handle it gently or the air "
     "comes out."),
    ("brioche",
     ("brioche", "brioche bun"),
     "Brioche is an enriched bread of flour, eggs and a lot of butter with a little sugar, so it is "
     "soft, yellow and slightly sweet. The butter goes in cold and a little at a time, and the dough "
     "wants a long cold prove. It makes the best burger bun and the worst sandwich for a wet filling."),
    ("bannock",
     ("bannock", "bannocks"),
     "Bannock is a flat quick bread from Scotland and the north of England, of flour, oatmeal or "
     "barley with bicarbonate of soda, salt and buttermilk, cooked on a hot girdle or in a pan rather "
     "than baked. It is ready in minutes and eaten warm with butter. What you buy is a dense round "
     "flat bread for toasting."),
    ("stottie",
     ("stottie", "stottie cake", "stotties"),
     "A stottie is a big flat white loaf from Tyneside, baked slowly so it stays soft and a bit "
     "stodgy inside, then split and filled - ham and pease pudding in a stottie is the classic. The "
     "name comes from stott, to bounce, because the dough is thrown down to knock it back."),
    ("crumpet",
     ("crumpet", "crumpets"),
     "A crumpet is a soft spongy griddle cake of batter cooked on one side only, so the top sets full "
     "of holes, then toasted until the holes fill with butter. The batter has to be bubbly before it "
     "goes into the rings. A pikelet is the thinner version from Wales and the Midlands."),
    ("bagel",
     ("bagel", "bagels"),
     "A bagel is a bread ring boiled for a minute or two before it is baked, which sets the crust and "
     "gives it the chew. It is dense on purpose, so it takes a lot of filling without falling apart. "
     "New York bagels are boiled in malted water, which is where the shine and the colour come from."),
    ("naan",
     ("naan", "naan bread", "naans"),
     "Naan is a soft flatbread of white flour, yoghurt and yeast, slapped onto the wall of a hot "
     "tandoor or cooked in a very hot dry pan so it puffs and blisters in patches. It gets brushed "
     "with butter or ghee as it comes off the heat. The yoghurt is what keeps it soft the next day."),
    ("pitta",
     ("pitta", "pita", "pitta bread", "pita bread"),
     "Pitta is a plain flatbread of flour, water and yeast baked very hot and fast, so the steam "
     "inside separates the two layers and leaves a pocket. That is why it opens for filling instead "
     "of needing to be cut. Keep the pack wrapped so it stays soft enough to open."),
    ("trifle",
     ("trifle", "trifles"),
     "A trifle is sponge or stale cake soaked with sherry or fruit juice, then fruit, then custard, "
     "then whipped cream, and the classic has raspberries and ratafia biscuits. Make the custard with "
     "egg yolks or cornflour rather than custard powder, or it tastes thin. Build it the day before "
     "so the sponge soaks."),
    ("fruit-fool",
     ("fruit fool", "gooseberry fool", "raspberry fool", "rhubarb fool"),
     "A fruit fool is stewed fruit folded into whipped cream and chilled - gooseberry is the classic, "
     "and raspberry and rhubarb work the same way. The fruit has to be cold and thick before it is "
     "folded in or it loosens the cream. It is one of the oldest British puddings and one of the "
     "quickest."),
    ("syllabub",
     ("syllabub",),
     "Syllabub is cream whipped with white wine, lemon juice and sugar until it holds its shape, "
     "sometimes with the wine poured in from a height so it froths on top. It sets because the acid "
     "from the wine and lemon firms the cream. Serve it in glasses with a biscuit, cold and the same "
     "day."),
    ("christmas-pudding",
     ("christmas pudding", "christmas puddings", "plum pudding"),
     "Christmas pudding is a steamed suet pudding of dried fruit, breadcrumbs, brown sugar, spice and "
     "ale or brandy, made weeks ahead so it matures and then reheated on the day - Stir-up Sunday, "
     "five weeks before, is the traditional day to make it. It is steamed for hours, never baked, and "
     "served with brandy butter or custard. Wrapped and kept cool it lasts a year."),
    ("clootie-dumpling",
     ("clootie dumpling", "clootie dumplings"),
     "A clootie dumpling is a Scottish steamed fruit pudding, like a christmas pudding but rounder "
     "and softer, tied in a floured cloth - a cloot - and boiled for hours rather than steamed in a "
     "basin. The cloth gives it its wrinkled skin. Serve it with custard, or sliced and fried with a "
     "cooked breakfast."),
    ("granita",
     ("granita",),
     "Granita is fruit juice or coffee with sugar and water frozen in a tray and forked through every "
     "half hour, so it sets into coarse ice crystals rather than a smooth cream. It needs no churning "
     "or special kit. More sugar means softer crystals, and alcohol keeps it from freezing hard at "
     "all."),
    ("eton-mess",
     ("eton mess",),
     "Eton mess is broken meringue, whipped cream and strawberries folded together, deliberately "
     "messy rather than layered. Assemble it just before it goes to the table or the meringue loses "
     "its crunch. It is said to come from a picnic at Eton where a strawberry and meringue pudding "
     "was dropped, and the name is the whole point."),
    ("cranachan",
     ("cranachan",),
     "Cranachan is a Scottish pudding of whipped cream, toasted oats, whisky and honey with "
     "raspberries folded in. Toast the oats slowly with a little sugar so they stay crisp against the "
     "cream. It is served in layers with a dram on the side."),
    ("tiramisu",
     ("tiramisu",),
     "Tiramisu is savoiardi biscuits dipped in strong coffee and marsala, layered with mascarpone "
     "beaten with egg yolks and sugar, and dusted with cocoa. The coffee has to be cold and the dip "
     "quick, or the biscuits turn to mush. It needs at least four hours in the fridge, so make it the "
     "day before."),
    ("cheesecake",
     ("cheesecake", "cheesecakes"),
     "Cheesecake is crushed biscuit and butter pressed into a tin with a soft cheese filling on top - "
     "baked with eggs and cream for the New York kind, or just chilled for the no-bake one. A baked "
     "cheesecake cracks when the oven is too hot, so bake it low and let it cool in the oven with the "
     "door ajar. Rest it in the fridge overnight."),
    ("sorbet",
     ("sorbet", "sorbets"),
     "Sorbet is frozen fruit puree or juice with sugar syrup and nothing else - no dairy, which is "
     "what makes it different from ice cream. It needs more sugar than ice cream to stop it freezing "
     "solid, and a squeeze of lemon keeps the fruit tasting fresh. Frozen still and scraped with a "
     "fork it is a granita."),
    ("hummus",
     ("hummus", "houmous", "humous", "houmus", "hummus dip"),
     "Hummus is a dip of cooked chickpeas blitzed with tahini, lemon juice, garlic and olive "
     "oil, loosened with a little cold water until it is smooth and pale. Tinned chickpeas work "
     "fine, and a pinch of bicarbonate of soda in the water while they simmer makes them "
     "softer. Spread it in a bowl with a swirl and a pool of olive oil, and eat it with "
     "flatbread or raw vegetables."),
    ("tzatziki",
     ("tzatziki", "tsatsiki", "tatziki"),
     "Tzatziki is a Greek dip of thick yoghurt, grated cucumber, garlic, olive oil and a little "
     "vinegar or lemon, with dill or mint stirred through. Salt the grated cucumber and squeeze "
     "it dry first, or the dip turns watery within the hour. It goes with grilled meat, souvlaki "
     "and flatbread, and cold from the fridge it cools a hot plate down."),
    ("raita",
     ("raita", "cucumber raita", "raitas"),
     "Raita is an Indian side of plain yoghurt with grated cucumber, salt and roasted cumin, "
     "sometimes mint or tomato, served cold beside a hot curry. Whisk the yoghurt smooth, stir "
     "in cucumber that has been salted and squeezed, and dust the cumin on just before it goes "
     "to the table. It is there to cool the mouth, so keep it simple."),
    ("tahini",
     ("tahini", "tahina", "sesame paste"),
     "Tahini is ground sesame seeds and nothing else - a thick, faintly bitter paste used in "
     "hummus, in dressings, and on its own beaten with lemon and water as a sauce. It seizes up "
     "when liquid goes in at first and turns creamy with more beating, so keep going. Stir the "
     "jar before you use it, keep it in the cupboard, and it lasts months."),
    ("jus",
     ("jus", "a jus", "red wine jus", "meat jus"),
     "A jus is the thin gravy that comes from a roast: the juices left in the tin, deglazed with "
     "wine or stock and reduced until it coats the back of a spoon. Nothing thickens it, which "
     "is what makes it lighter and glossier than gravy. Pour the fat off first and strain it if "
     "you want it clear."),
    ("salsa",
     ("salsa", "salsa sauce", "pico de gallo", "tomato salsa"),
     "Salsa is a Mexican sauce, most often raw tomato, onion, chilli, lime and coriander chopped "
     "together - that one is pico de gallo, and it is a relish rather than a dip. Cooked and "
     "blended it is a smoother, smokier salsa for chips or for baking under. The dance of the "
     "same name is a different question."),
    ("brisket",
     ("brisket", "beef brisket", "brisket of beef"),
     "Brisket is the boned chest of the beef, a tough cut full of connective tissue, so it wants "
     "long, slow, moist heat - four or five hours at 150C - rather than a quick roast. Cooked "
     "like that it falls into soft slices; pot-roasted with stock and onions it makes its own "
     "gravy. Always slice it across the grain."),
    ("silverside",
     ("silverside", "salt silverside", "salted silverside"),
     "Silverside is a boned cut from the back of the hindquarter, usually salted and simmered "
     "rather than roasted, then served hot with mustard sauce or cold in sandwiches. Soak a very "
     "salty one overnight before cooking, then bring it to a bare simmer and hold it there - a "
     "rolling boil makes it stringy. Brined and tinned, the same cut is sold as corned beef."),
    ("kipper",
     ("kipper", "kippers", "smoked herring"),
     "A kipper is a herring that has been split, salted and smoked, so it is already cooked and "
     "needs only heating: grill it or poach it in a little water for three or four minutes. It "
     "comes as a whole flattened fish with a lot of fine bones. Serve it with buttered bread and "
     "a squeeze of lemon, and eat it for breakfast if you are in Scotland."),
    ("hake",
     ("hake", "hake fillet", "hake fillets"),
     "Hake is a white sea fish in the cod family, soft-fleshed and sold as fillets or as steaks "
     "with a bone through the middle. It flakes more easily than cod, so cook it briefly - "
     "skin-side down in a hot pan, or 12 to 15 minutes in a hot oven. It takes strong flavours "
     "well: garlic, paprika, tomato and olive oil."),
    ("halloumi",
     ("halloumi", "halloumi cheese", "grilled halloumi"),
     "Halloumi is a Cypriot cheese of sheep's and goat's milk that is heated and pressed as it "
     "is made, so it holds its shape and squeaks instead of melting. Slice it, dry the slices on "
     "kitchen paper, then fry or grill hard for a minute a side until the outside is dark and "
     "crisp. It is very salty, so it wants lemon, chilli or honey rather than more salt."),
    ("paneer",
     ("paneer", "paneer cheese", "indian cheese"),
     "Paneer is an Indian cheese made by curdling hot milk with lemon juice or vinegar and "
     "pressing the curds under a weight, so it is firm, mild and does not melt - it browns in "
     "the pan instead. Fry the cubes first so they keep their shape, then add them to the sauce "
     "at the end. It takes on whatever spice is around it."),
    ("bulgur",
     ("bulgur", "burghul", "bulghur", "bulgur wheat", "cracked wheat"),
     "Bulgur is wheat that has been parboiled, dried and cracked, so it needs only soaking or a "
     "few minutes of simmering rather than half an hour. Coarse bulgur is for pilafs and salads, "
     "fine bulgur for kibbeh and tabbouleh. It swells to twice its size and keeps a firm bite "
     "where rice would go soft."),
    ("quinoa",
     ("quinoa", "quinoa grain", "red quinoa"),
     "Quinoa is a seed from a South American plant, cooked like rice but faster, with a nutty "
     "taste and a slight crunch - it is not a grain. Rinse it before cooking to wash off the "
     "bitter coating, then simmer it in twice its volume of water for about 15 minutes until "
     "the little rings come away. It works hot as a side and cold in salads."),
    ("polenta",
     ("polenta", "polenta grain", "cornmeal polenta"),
     "Polenta is coarsely ground cornmeal simmered in water or stock until it thickens and pulls "
     "away from the side of the pan: about 40 minutes of stirring for the coarse kind, five for "
     "the instant. Served soft with butter and parmesan, or spread in a tray, cooled firm and "
     "cut into slices to fry. The fried leftovers are the best part."),
    ("couscous",
     ("couscous", "cous cous", "instant couscous"),
     "Couscous is semolina rolled into tiny grains by hand and steamed over the stew rather than "
     "boiled; the boxed instant kind has already been steamed, so it only needs boiling water "
     "poured over it. Use the same volume of water as grain, cover it for five minutes, then "
     "fluff it with a fork and stir in butter or oil. It is the bed the stew sits on."),
    ("plantain",
     ("plantain", "plantains", "cooking banana", "green plantain"),
     "Plantain is a cooking banana: bigger, starchier and meant to be cooked, never eaten raw. "
     "Green ones are savoury and firm, so slice them thin and fry them crisp; left until the "
     "skin is black they are sweet, and thick coins fried in butter go soft and caramelised. "
     "Either way they take salt, chilli or a bean stew."),
    ("swede",
     ("swede", "swedes", "rutabaga", "neeps"),
     "Swede is a round root with purple skin and yellow flesh - a bigger, sweeter relative of "
     "the turnip, and called rutabaga in America and neeps in Scotland. It roasts in chunks "
     "around a joint, mashes with butter and pepper, or goes into a pasty. The smaller ones are "
     "sweeter, and it takes longer to cook than a potato."),
    ("parsnip",
     ("parsnip", "parsnips", "roast parsnips"),
     "A parsnip is a long cream root with a sweet, peppery taste that gets sweeter after a frost "
     "because the cold turns its starch to sugar. Roast it in chunks around the meat or mash it, "
     "and cut the woody core out of a big one first. Peel it thinly, since most of the flavour "
     "sits just under the skin."),
    ("shallot",
     ("shallot", "shallots", "banana shallot"),
     "A shallot is a small elongated onion of its own variety, milder and sweeter than an onion, "
     "and it splits into two or three cloves under the skin. It is the one to use raw in a "
     "vinaigrette or pickled whole, and it softens and caramelises faster than an onion does. "
     "The banana shallot is the long one and is easiest to peel."),
    ("cumin",
     ("cumin", "cumin seeds", "ground cumin", "jeera"),
     "Cumin is a warm, earthy spice sold as whole seeds or ground, and the seeds keep their "
     "flavour far longer than the powder. Toast the seeds for a minute in a dry pan, or fry them "
     "in the oil at the start of a curry, then crush them. It is the base note of most curry "
     "powders, of chilli and of a lot of Mexican cooking."),
    ("paprika",
     ("paprika", "smoked paprika", "sweet paprika", "hot paprika"),
     "Paprika is ground dried peppers - sweet, hot or smoked depending on which chilli was used, "
     "and the Hungarian sweet one is what people usually mean. Sweet paprika cannot take high "
     "heat: stir it in near the end, or bloom it in warm oil for a few seconds, or it turns "
     "bitter. Smoked paprika is for depth, in chorizo, beans and roast chicken."),
    ("turmeric",
     ("turmeric", "tumeric", "ground turmeric", "turmeric powder"),
     "Turmeric is a bright yellow root, used dried and ground, with an earthy, slightly bitter "
     "taste and no real heat - it is in curry powder mostly for colour. A little goes a long "
     "way, and it stains boards, cloth and fingers yellow, so keep it off anything pale. Fresh "
     "root is milder and can be grated into rice or a dressing."),
    ("coriander",
     ("coriander", "cilantro", "coriander leaves", "ground coriander", "coriander seeds"),
     "Coriander is two different things from one plant: the leaves and stalks, which taste "
     "bright and faintly soapy and go in raw at the end, and the ground seed, which is warm and "
     "citrusy and goes in at the start. Toast the seeds to wake them up before grinding. In a "
     "curry paste the root is the most flavoursome part."),
    ("samosa",
     ("samosa", "samosas", "vegetable samosa", "lamb samosa"),
     "A samosa is a pastry triangle of spiced potato and peas, or minced lamb, wrapped in a thin "
     "flour pastry and deep-fried until it blisters - or baked, which is lighter but not the "
     "same. The filling has to be cool and dry before it is wrapped or the pastry goes soft. "
     "Serve them with a yoghurt dip or a tamarind chutney."),
    ("falafel",
     ("falafel", "felafel", "falafels"),
     "Falafel is soaked raw chickpeas ground with onion, garlic, herbs and cumin, shaped into "
     "balls and fried until dark and crisp - made from cooked chickpeas the mixture falls apart "
     "in the oil. The chickpeas need an overnight soak, not a simmer. Serve them in flatbread "
     "with salad, pickles and tahini."),
    ("bhaji",
     ("bhaji", "bhajis", "bhajee", "onion bhaji", "onion bhajis"),
     "A bhaji is a fritter of sliced vegetables in a spiced gram flour batter, dropped in "
     "spoonfuls into hot oil: onion is the usual one, and cauliflower and spinach work the same "
     "way. Gram flour, not wheat, is what makes it a bhaji, and the batter should just hold "
     "together. Eat them hot with a yoghurt or tamarind dip."),
    ("gherkin",
     ("gherkin", "gherkins", "cornichon", "cornichons", "pickled cucumber"),
     "A gherkin is a small cucumber pickled in vinegar or brine, eaten whole as a snack or "
     "sliced into a burger; cornichons are the tiny sour French ones. A fresh gherkin is simply "
     "a small cucumber, and only the pickled one keeps for months in the jar. Rinse them if you "
     "want less salt."),
    ("caper",
     ("caper", "capers", "caper berries", "caperberries"),
     "Capers are the unopened flower buds of a Mediterranean shrub, pickled in brine or packed "
     "in salt, and used for a sour, salty hit in tartare sauce, with salmon, and in "
     "puttanesca. Rinse the salted ones before use, and chop rather than crush them. The bigger "
     "caperberries are the open fruit of the same plant and are eaten whole."),
    ("samphire",
     ("samphire", "marsh samphire", "sea samphire", "rock samphire"),
     "Samphire is a salty green that grows on mudflats and beaches, looking like fleshy "
     "joined-up stems, sold fresh in summer - that one is marsh samphire. Wash it well, steam or "
     "boil it for about three minutes and eat it with butter and lemon, no salt. Rock samphire "
     "is the rarer, stronger-tasting one."),
    ("salsify",
     ("salsify", "black salsify", "oyster plant", "scorzonera"),
     "Salsify is a long thin root that tastes faintly of oyster: the black-skinned one is "
     "salsify and the white one is scorzonera. Peel it and drop it straight into water with "
     "lemon juice, or it browns in minutes, then roast or fry it in butter. It is a winter "
     "vegetable and it is best simply cooked."),
    ("kohlrabi",
     ("kohlrabi", "kohl rabi"),
     "Kohlrabi is a swollen stem rather than a root - pale green or purple, with a taste between "
     "cabbage and turnip and the crunch of a crisp apple. Peel the tough outer skin off, then "
     "slice it raw into salad or roast it in wedges until the edges caramelise. The leaves cook "
     "like cabbage."),
    ("fennel",
     ("fennel", "fennel bulb", "fennel bulbs", "fennel fronds"),
     "Fennel is the vegetable with the fat white bulb and feathery green fronds, tasting of "
     "aniseed; the seed is the same plant's spice. Cut the bulb through the core so the wedges "
     "hold together, brown it hard in a pan, then braise or roast it, and use the fronds raw as "
     "a herb. Raw shaved thin with lemon it is a salad on its own."),
    ("leek",
     ("leek", "leeks", "baby leeks"),
     "A leek is a long green and white allium, milder and sweeter than an onion, that softens "
     "and sweetens long before it browns. Slit it lengthwise and rinse between the layers, "
     "because grit grows down inside it. It is the base of leek and potato soup and it braises "
     "well in butter with a little stock."),
    ("chive",
     ("chive", "chives", "garlic chives"),
     "Chives are the thin green stems of a small allium with a mild onion taste, used raw as a "
     "garnish - snipped over eggs, potatoes, soup or a baked potato. Heat kills the flavour, so "
     "add them at the end rather than in the pan. They grow back after cutting, which is why a "
     "pot on the windowsill keeps going."),
    ("pudding",
     ("pudding", "puddings", "a pudding", "sweet pudding"),
     "A pudding is the sweet course at the end of a British meal, and also a family of dishes "
     "steamed or baked under suet pastry or a sponge - sticky toffee, treacle, rice, Christmas "
     "pudding. The word means either the course or the dish, so which one it is depends on the "
     "sentence. Steamed ones cook covered in a water bath; baked ones go straight in the oven."),
    ("shepherds-pie",
     ("shepherd's pie", "shepherds pie", "shepherd pie", "shepherd's pies"),
     "Shepherd's pie is minced lamb cooked with onion and gravy in a dish, with mashed potato "
     "spread over the top and baked until the ridges catch and brown. Lamb is what makes it a "
     "shepherd's pie - made with beef it is a cottage pie. Let the mince cool a little before "
     "the mash goes on, or it sinks in."),
    ("cottage-pie",
     ("cottage pie", "cottage pies", "beef pie with mash"),
     "Cottage pie is minced beef with onion and gravy under a mash crust, baked until the top is "
     "crisp - the beef version of shepherd's pie. Brown the mince properly first and let the "
     "gravy reduce, or the mash slides off in the serving. Fork the mash up before it goes in "
     "the oven so the ridges brown."),
    ("pie",
     ("pie", "pies", "a pie", "savoury pie"),
     "A pie has pastry under the filling and a lid over it, or just a lid, where a tart is open "
     "and a cobbler has scones on top. Shortcrust is the plain one, puff the laminated one that "
     "rises in layers, and hot-water crust is for a raised pork pie. Fillings run from steak and "
     "ale to apple."),
    ("compote",
     ("compote", "fruit compote"),
     "A compote is whole or large pieces of fruit poached gently in sugar syrup, sometimes with "
     "vanilla, lemon peel or spice, until they are soft but still in shape. It keeps in the fridge "
     "for a few days and is served with cream, yoghurt or porridge. Use less syrup than you think, "
     "because the fruit gives up its own juice."),
)

DISH_WHAT_ASKS = ("what is", "what's", "whats", "what are", "what was", "mean", "means",
                  "meaning", "definition", "explain", "tell me about", "what do you mean",
                  "is a", "is an", "is it a", "are they", "what kind of", "what sort of",
                  "where does", "where do",
                  "what does")

DISH_WHAT_LEAD = ("", "so", "ok", "okay", "and", "but", "then", "sorry", "quick",
                  "quick one", "one thing", "also", "yeah", "yes", "hi", "hiya", "hello",
                  "right", "actually", "just", "please", "oh", "um", "er", "well")


def _opens_with_the_ask(said):
    words = said.strip(" .!?,").split()
    for lead in sorted(DISH_WHAT_LEAD, key=len, reverse=True):
        if not lead:
            continue
        if words[:len(lead.split())] == lead.split():
            words = words[len(lead.split()):]
            break
    head = " ".join(words[:3])
    return any(head.startswith(ask) for ask in DISH_WHAT_ASKS)


DISH_WHAT_AVOID = ("how do i", "how to", "how should i", "best way", "recipe", "recipes",
                   "goes with", "go with", "go nicely", "serve with", "serving with", "side for",
                   "sides for", "side dish", "with what", "alongside", "to serve",
                   "for dinner", "for tea", "for lunch", "for a crowd", "for two", "for four",
                  "what about", "how about", "what if", "same for",
                   "favourite", "favorite", "favourites", "favorites", "your favourite",
                   "your favorite", "you like", "do you like", "would you", "prefer",
                   "your pick", "pick one", "which one", "what would you",
                   "how long", "how much", "make it", "make them", "cook it", "cook them",
                   "should i", "can i", "calories", "good for you", "healthy",
                   "what is a good", "what is the best", "best way", "for dinner",
                   "ideas", "suggest", "recommend", "which is better",
                   "casserole dish", "hash brown", "hash browns",
                   "tap", "taps", "washer", "plumbing",
                   "pipe", "pipes", "paint", "radiator", "boiler",
                   "called", "named", "puppy", "puppies", "dog", "dogs", "kitten", "kittens",
                   "cat", "cats", "hamster", "rabbit",
                   "lol", "haha", "ha", "thanks", "ta", "cheers", "bye", "gotta", "swap",
                   "swaps", "swap it",
                   "ceiling", "ceilings", "roof", "wall", "walls", "floor", "floors", "water",
                   "damp", "fridge", "freezer", "window", "windows", "door", "doors",
                   "tag", "tags", "hashtag", "hashtags", "symbol", "key", "code", "sign",
                   "taste like", "tastes like", "smell like", "look like", "sound like",
                   "dance", "dances", "dancing", "dancers")


DISH_BARE_NAMES = ("pie", "pies", "a pie", "pudding", "puddings", "a pudding")


def _qualified_bare_word(row, said):
    names = [name for name in row[1] if name in said]
    if not names or any(name not in DISH_BARE_NAMES for name in names):
        return False
    for name in names:
        noun = name.split()[-1]
        head, _, tail = said.partition(" %s " % noun)
        before = head.split()
        if before and before[-1] not in ("a", "an", "the", "and", "or", "this", "that", "my",
                                         "is", "are", "was", "were"):
            return True
        after = tail.split()
        if after and after[0] not in ("for", "is", "are", "and", "or", "with", "s"):
            return True
    return False


def _what_is_a_dish(memory, understood):
    said = str((understood or {}).get("clean") or
               " ".join((understood or {}).get("words") or ())).lower()
    if not _opens_with_the_ask(said):
        return None
    said = " %s " % said
    found = [row for row in DISH_WHAT if any(" %s " % name in said for name in row[1])]
    if not found:
        return None
    found = [row for row in found if not _qualified_bare_word(row, said)]
    if not found:
        return None
    found.sort(key=lambda row: max(len(name) for name in row[1]), reverse=True)
    top = " %s " % max(found[0][1], key=len)
    found = [found[0]] + [row for row in found[1:]
                          if not any(" %s " % name in top for name in row[1])]
    if len(found) > 1:
        return "%s Or the other way round: %s" % (found[0][2], found[1][2])
    return found[0][2]


for _slug, _names, _what in DISH_WHAT:
    ENTRIES.append(entry(
        "what-is-%s" % _slug, (_names, DISH_WHAT_ASKS), _what_is_a_dish,
        bias=2, ask=DISH_WHAT_ASKS, avoid=DISH_WHAT_AVOID))

ENTRIES.append(entry(
    "cheap-lunch-where",
    (("cheap lunch", "cheap lunches", "cheap eats", "lunch near", "lunch around",
      "where to eat", "where should we eat", "where should i eat", "where can i eat",
      "where can we eat", "somewhere to eat", "anywhere to eat", "anywhere cheap to eat",
      "cheap to eat", "a place to eat", "place to eat", "places to eat", "cheap place to eat",
      "good place to eat", "good place for lunch", "place for lunch", "where to get lunch",
      "grab lunch", "get some lunch", "eat out cheap", "somewhere good for lunch",
      "somewhere for lunch", "lunch in town", "lunch near work", "lunch near here",
      "lunch round here"),
     ("near", "nearby", "around", "station", "office", "work", "town", "lunch",
      "anywhere", "recommend", "suggest", "get", "place", "places", "eat out",
      "cheap", "cheaply", "cheapest", "here", "today", "tonight")),
    "Look for the places that sell a lot of one thing: a market hall or a food court, a bakery, "
    "a cafe at the back of a shop, a street food van in a regular spot, or the lunch board "
    "outside a restaurant that wants the office trade. Walk a street back from the station or "
    "the main road, where the rents are lower, and follow the queue of people who work nearby.",
    avoid=("dinner", "birthday", "anniversary", "valentine", "celebrate", "date night",
           "book a table", "booking", "michelin", "ideas", "packed lunch", "lunchbox",
           "make my own", "recipe", "meal plan", "cook",
           "dog", "dogs", "puppy", "pet", "pets", "kid", "kids", "children", "toddler",
           "baby", "high chair", "vegan", "vegetarian", "veggie", "gluten", "allergy",
           "allergic", "wheelchair", "accessible"),
    bias=2))
