import re

from . import lexicon
from .body import A_GUT_ONLY
from .kinds import ADDRESS_WORDS, VERDICT_NOUNS, _asks_back, a_bad_verdict, small_talk_only
from .normalize import LEXICON as COMMON_WORDS
from .normalize import background_positions, reason_positions
from . import normalize

STRONG = {
    "cooking": """cook cooking recipe recipes bake baking boiled boil fry frying roast roasted
        pudding puddings bbq
        grill simmer oven hob pan pot saucepan whisk knead dough batter marinade seasoning
        chop chopped chopped stir fry leftover leftovers sourdough pastry cake cupcakes
        biscuits bread pizza pasta curry soup stew rice risotto noodles sauce gravy stuffing
        roast scrambled poached omelette pancake pancakes lasagne lasagna meatballs
        undercooked overcooked sticky mushy crispy seasoning vegan vegetarian cheese
        dairy gluten lactose nut soya soy wheat
        cheeses chicken beef pork lamb mince bacon sausages ham fish salmon tuna prawns
        potato potatoes tomato tomatoes onion onions garlic ginger carrot carrots
        cabbage leeks cauliflowers swede peas celery cucumber lettuce beetroot sprouts pepper
        peppers mushroom mushrooms spinach courgette courgettes broccoli beans lentils
        chickpeas pasta spaghetti noodles rice flour sugar butter egg eggs milk cream
        lemon lemons lime limes orange herbs basil thyme rosemary parsley coriander cumin
        paprika cinnamon vanilla honey mustard mayonnaise yoghurt oil vinegar stock
        casserole tray tin whisk blender frying baking grill saucepan saucepan dish
        defrost thaw preheat simmering frying boiling recipes portions portion serving
        brine brining deseed deseeded meringue meringues pavlova guacamole milkshake
        milkshakes melon melons burrito burritos
        refreeze cabbage cauliflower kale lettuce sprouts peas veggie veggies pie quiche
        shortbread sponge scones icing frosting buttercream jam pesto hummus couscous halloumi
        buttermilk pudding puddings bolognese bol spag chilli chips mash loaf yeast
        parboil thicken reheat bland soggy rubbery watery steak chops breast thighs burgers meat
 tablespoon dessertspoon rinse tinned muffins muffin custard flapjacks flapjack popcorn cheesecake brownies brownie
        caramel tzatziki wok jelly aioli clams crumble meringue sorbet coleslaw
        burgers pineapple oats
 turkey knives cheddar quinoa scales sweetcorn mussels burger chinese indian grainy""",
    "food-and-drink": """eat eating food meal breakfast lunch dinner snack snacks drink drinking
        supper brunch dessert pud afters nibbles elevenses brekkie brekky sarnie
        butty cuppa takeout nosh chow kebab chippy munchies bap sanger
        coffee tea water juice wine beer sugar salt pepper cheese butter milk yogurt cream
        vegan vegetarian gluten allergy allergic caffeine decaf fizzy chocolate crisps
        takeaway restaurant menu hungry thirsty tasty delicious bread toast sandwiches
        sandwich cereal porridge yoghurt smoothie chocolate crisps nuts fruit apple apples
        banana bananas orange strawberries berries salad salad dressing mouldy moldy
 leftovers reheating leftovers portions
        ripe granola""",
    "health": """doctor gp hospital nurse pharmacy medicine tablet tablets pill pills symptom
        symptoms pain ache ill illness sick unwell fever temperature cold flu cough sneeze
        headache headaches migraine throat sore throat bleeding bleed cut burn burnt bruise
        infection antibiotics vaccine vaccination allergy allergic dizziness dizzy nausea
        blood pressure appointment clinic injury prescription eyes eye vision headache
        migraines dentist dental toothache teeth stroke numb numbness slurred
        seizure fainted fainting sprain sprained swelling swollen blister blisters
        sliced rash itchy itch vomiting vomit puking puke puked barf barfing diarrhoea constipation
        heartburn indigestion reflux
        cramps cramp bloated congestion earache ankle wrist elbow shoulder knee hip
        thumb finger fingers toe toes spine joint tendon ligament stomach calpol nurofen
        ibuprofen
        paracetamol painkiller painkillers cyst infected hangover hangovers
        nostrils nostril sinus sinuses sniffles sniffly stinging stings stung hoarse
        shivery chills queasy laryngitis tonsils wheezy croaky phlegmy smoking braces
        cholesterol heal healing snacking aching aches hurting nails toothbrush fibre
        fasting rundown mole moles acne hayfever inhaler inhalers colic palpitations antidepressants
        antidepressant dandruff floss plaque smear nits verruca verrucas wart warts
 cystitis menopause measles mumps chickenpox tonsillitis earache toenail
        toenails adhd autism dyslexia ocd ptsd sunscreen aftersun blistering
        pregnancy vitamin limping""",
    "fitness": """run running jog jogging gym workout exercise exercises stretch stretching
        training train fitness muscle muscles cardio weights lifting squat squats push-ups
 plank cycling swim swimming yoga pilates marathon 10k 5k steps calories toned
        insoles reps pace sets""",
    "sleep": """sleep sleeping slept insomnia bedtime nap naps wake waking woke tired exhausted
 mattress pillow duvet toddler wakes snore snoring dreams nightmare melatonin""",
    "money": """money bank savings save saving budget budgeting salary wage wages pay paid
        loan loans mortgage rent debt debts credit debit card overdraft pension
        invest investing insurance tax taxes bills bill invoice receipt refund expensive
        cheap afford spending spent pound pounds euro euros dollar dollars cash atm council
        owes owed supplier payday payment payments doubled income lease vat switching
 deposit skint overcharging overcharged isa retire retired retirement subscriptions allowance overdrawn bailiff bailiffs
        dividend dividends apr payslip payslips annuity
benefit declare hmrc""",
    "work": """job jobs work working boss manager colleague colleagues office interview cv
        resume salary promotion review meeting meetings deadline project team hire hiring
        fired quit resign resignation contract shift shifts overtime coworker workplace
        conference presentation badge rota roster timesheet timesheets appraisal
 payslip warehouse supervisor defensive
        employer reference probation earlies sacked staff published""",
    "school-and-study": """school exam exams revise revising revision study studying homework
        teacher class lesson lessons term semester university college student grades grade
        test tests essays essay coursework dissertation notebook learn learning
        spelling vocabulary subject tutor a-level a-levels alevel alevels gcse
        gcses apprenticeship apprenticeships lecture lectures seminar
 seminars memorise memorising memorised cram cramming timetable
        uni squared levels phd ucas factorise accountant thesis courses maintenance equations lab""",
    "science": """science scientific physics chemistry biology atoms molecules gravity energy
        evolution photosynthesis oxygen carbon climate vaccines virus bacteria cells species
        experiment theory hypothesis dna planets jupiter saturn mars venus mercury
 orbit orbits seasons solar astronomy telescope moon moons
        tan planet thunder lava reflect blink shiver freckles digestion conductor insulator galaxy skyscrapers berry""",
    "history": """history historical century ancient empire revolution war wars king queen
        pharaoh pyramids roman romans greeks medieval victorian industrial
 archaeology civilisation civilization darwin einstein freud waterloo tsar lenin bismarck attila napoleon
        boleyn tudor tudors victorians aztec aztecs inca vikings
        invented britain blitz hitler marx antoinette curie crusades""",
    "geography-and-travel": """travel travelling traveling trip holiday holidays flight fly
        flying airport boarding plane train station passport luggage packing pack suitcase hotel
        booking itinerary visa abroad city countries country capital jet lag jetlag map
 tour tourist sightseeing beach mountains island abroad drive driving
        spain rome cornwall lisbon ferry edinburgh paris portugal london croatia coast naples amalfi airline cabin metro mexico heathrow prague pompeii benidorm""",
    "technology": """phone laptop computer tablet screen keyboard battery charger wifi wi-fi
        internet email app apps website software password passwords download upload update
        install printer router bluetooth notification notifications file files folder backup
        virus hacking privacy screenshot log login account data iphone android mac macbook
        photos delete uninstall restart spam scam texting pointer icloud zoom
        broadband headphones earphones robocall robocalls landline
        
        ipad signal earbuds pdf blurry monitor sim print facebook ssd speaker usb spreadsheet vlookup teams google cloud youtube photograph""",
    "home-and-diy": """house flat apartment kitchen bathroom bedroom ceiling wall walls floor
        carpet paint painting diy drill hammer screw screws shelf cupboard radiator boiler
        sink tap drain drains mould mold damp leak leaking plumber electrician fuse
        furniture sofa bed washing machine dishwasher hoover dyson vacuum suction filter
        ironing ironed curtain curtains
        moving move removal landlord toilet flush flushing grout tile tiles shower smoke alarm
        carbon monoxide draught draughts door doors window windows lock locks thermostat
        heating freezer fridge kettle draft loft gutter guttering locksmith doorbell
        burner burners stove stoves fireplace chimney flue hearth worktop worktops dryer tumble
        jeans shirt shirts jumper towels stain stains condensation limescale kettling extractor
 radiators gutters fence plasterboard drum loader wooden spilt pipes
 wallpaper wallpapering decking wardrobe wardrobes patio toaster cistern ladder ladders tenancy chipped varnish
        blinds cutlery crockery doormat skirting tiling umbrellas knit knitted scarf
        recycling rug bins bedding softener stool""",
    "garden-and-plants": """garden gardening plant plants planting grow growing seed seeds
        seedling seedlings soil compost weed weeds weeding watering pruning prune lawn grass
        flower flowers bulbs tulip tulips basil tomato tomatoes balcony allotment greenhouse
        pots shrubs shrub hedge hedges turf mower rake hoe mulch repot repotting
        deadhead deadheading cuttings propagate houseplant houseplants monstera orchid orchids
        cactus cacti succulent succulents fern ferns lily lilies aloe lavender hydrangea
        daffodil daffodils sunflower sunflowers composted harvest harvesting harvested
        sow sows sowing sowed slug slugs snail snails
        roses moss lawnmower vase bonsai bamboo baskets basket chit""",
    "pets": """pet pets dog dogs puppy cat cats kitten kittens vet vet rabbit rabbits hamster
        goldfish fish tank lead leash walkies dog lead kitten litter kennel rescue adopted
 adopt purring barking bark treats barks fleas collar paw poisonous
        labrador greyhound guinea whippet spaniel pug pig neutering""",
    "family-and-parenting": """child children kid kids baby toddler toddler son daughter
        parent parents mum mom mother dad father husband wife partner family babies nappy nappies
        pram nursery babysit twins birthday party school run parenting newborn
        toddler toddlers potty weaning teething playgroup playschool childminder
        gran grans sister sisters brother brothers sibling siblings grandma grandmas granny grandad
        grandpa grandparents grandmother grandfather grandson granddaughter grandchild
        grandchildren nan nana nanna nephew nephews niece nieces cousin cousins aunt aunty
        auntie uncle uncles stepmother stepfather stepmum stepdad stepson stepdaughter
        stepchild stepchildren stepsister stepbrother half-brother half-sister in-laws
 relatives ex exes
        teen invitations godparent babysitting hymns boys""",
    "friends-and-relationships": """friend friends friendship partner boyfriend girlfriend
        wife husband marry married wedding dating date anniversary argument argued row
        apology apologise apologize forgive trust relationship relationships breakup
        neighbour neighbours colleague flatmate housemate ex exes
 divorce divorced separation separated cheat cheated cheating affair affairs""",
    "shopping": """buy buying bought shop shopping store price prices cheap expensive
        sale discount refund warranty returns second-hand reviews review order
 delivery parcel stock size sizes brand
 moisturiser housewarming bleaching""",
    "cars": """car cars tyre tyres tire tires mot brakes brake braking engine engines clutch
        gearbox windscreen windshield wipers wiper headlights headlight bonnet coolant
        dipstick tread puncture petrol diesel mpg speedometer dashboard mechanic garage
 servicing motoring motorway alloy alloys demist
        ebike pcn bumper pedal penalty motor""",
    "entertainment": """film films movie movies watch watching series tv television show
        shows netflix book books novel novels read reading podcast podcasts music song songs
        album band concert theatre theatre game games play console chess draughts
        backgammon scrabble monopoly jigsaw jigsaws
        documentary comedy comedy episode episodes season author writer actor actress
 streaming
 chords amp iplayer succession western jazz""",
    "sport": """sport sports football footy footie soccer rugby cricket tennis golf match
        matches team
        league cup goal goals offside wicket wickets innings coach coaching training
        bowling yorker googly bouncer crease stumps batsman batsmen wicketkeeper keeper
        olympics tennis badminton swimming race racing formula tennis wimbledon
 player players referee darts snooker hockey netball volleyball athletics
        basketball baseball softball handball squash boxing marathon marathons triathlon
        skiing surfing rowing bowls
        hamstrings""",
    "language-and-writing": """grammar spelling word words writing wrote write sentence
        sentences essay paragraph punctuation apostrophe comma vocabulary phrase
        wording translate translation english language meaning affect effect fewer less
 email draft letter poem speech bio caption congratulations plural plurals semicolon semicolons colon voicemail thesaurus dictionary mumbling
        monotone
        spell fluent exclamation bullet rewrite""",
    "feelings": """feel feeling felt emotional lonely alone sad unhappy upset anxious worried
        nervous stressed stress overwhelmed depressed crying tears heartbroken gutted angry
        annoyed frustrated guilty ashamed jealous embarrassed happy excited relieved proud
 grateful mood feelings grief grieving funeral devastated
        coping knots churning""",
    "small-talk": """jigsaw chatty catch chat catch-up catchup rain raining sunny freezing
 chilly warm cold weather bye lovely
 easter""",
    "opinions": """opinion favourite favorite prefer rather
 worth overrated underrated agree disagree""",
    "creative": """poem poetry story stories joke jokes nickname creative
 write writing speech rhyme character plot lyrics slogan tagline design
        limerick haiku rap""",
    "maths-and-numbers": """percent percentage maths math numbers calculate sum total average
        divide multiply minus plus equation fraction fractions decimals half double triple
 algebra geometry numerator denominator perimeter theorem pythagoras protractor diameter radius
        isosceles quadrilateral quadrilaterals parallelogram rhombus trapezium cuboid
        triangles triangle probability median""",
    "nature-and-weather": """weather rain raining snow snowing storm thunderstorm lightning
        wind windy sunny sunshine clouds cloudy fog foggy freezing frost heatwave forecast
        autumn spring winter summer birds heron robin sparrow wildlife trees nature
 river sea ocean beach stars moon
        animal whale cheetah penguins penguin""",
    "about-the-bot": """chatbot bot robot artificial intelligence human person alive feelings
 remember yourself yourself
        version chatgpt soul""",
}

STRONG["home-and-diy"] += """
        attic cellar mirror mirrors picture pictures frame frames lamp lamps
        socket sockets plug plugs wiring hook hooks armchair armchairs"""


WEAK = {
    "cooking": "make made time minutes hours temperature heat hot plate bowl spoon knife "
               "cookies "
               "dinner tonight lunch breakfast tastes frozen handful freeze",
    "food-and-drink": "like dislike sweet sour spicy fresh cold hot bottle cup glass",
    "health": "feel better worse days week rest sleep tired checked",
    "fitness": "minute minutes week day morning evening body",
    "sleep": "night morning bed room",
    "money": "much cost worth pay month year percent save owe minimum",
    "work": "day week hours people ask",
    "school-and-study": "help practice remember book week day",
    "science": "why works explain",
    "history": "time people built",
    "geography-and-travel": "go going place days week month",
    "technology": "work working broken fix new old connect storage charging broadband",
    "home-and-diy": "room house fix clean door doors window windows repairing replace serviced "
                    "bleach smells smelling dripping banging rattling humming stinks stinking "
                    "squeaking leather patch",
    "garden-and-plants": "water green yellow leaves grow",
    "pets": "feed cat dog walk scratching",
    "family-and-parenting": "home help age",
    "friends-and-relationships": "talk said told mate mates pal pals buddy bloke fella",
    "shopping": "need new look",
    "cars": "start starting noise noisy sound light warning fix cost worth check insurance",
    "entertainment": "good funny watch read listen",
    "sport": "play watch season",
    "language-and-writing": "say write help mean",
    "feelings": "really very today week",
    "small-talk": "today hello hi tomorrow day week morning evening busy tired",
    "opinions": "think really",
    "creative": "help idea",
    "maths-and-numbers": "how many long",
    "nature-and-weather": "today season year",
    "about-the-bot": "you your help",
}

THING_WORDS = frozenset(
    word for words in list(STRONG.values()) + list(WEAK.values()) for word in words.split())
normalize.learn_thing_words(THING_WORDS)

SUMS_AFTER = frozenset("""how what which if whether when where why much many long cost costs
    budget rate rates salary pay bill bills price prices percentage percent total average
    amount area size volume length distance mpg miles tax taxes loan loans owe owes
    spend spending split share calories tiles paint dose timer timers worth number numbers
    cheaper cheapest
    the my our your his her their its this that these those""".split())
NUMBER_WORDS = frozenset("""one two three four five six seven eight nine ten eleven twelve
    thirteen fourteen fifteen sixteen seventeen eighteen nineteen twenty thirty forty fifty
    sixty seventy eighty ninety hundred thousand million billion half quarter""".split())
SUM_MONEY = frozenset("""pay paid salary wage wages tax taxes bill bills budget price prices
    cost costs rate hourly income rent loan loans mortgage overtime notice pension fee fees
    profit loss interest entitlement entitlements cheaper cheapest owe owes
    debt debts refund refunds save savings total""".split())
EXERCISE_AFTER = frozenset("""gym home more often regularly times sets reps cardio weights
    running fit fitness training body muscles arms arm legs leg abs back chest shoulders
    glutes core biceps triceps thighs butt hard lightly daily weekly workout session
    day days week weeks once twice
    morning mornings evening evenings night afternoon today tomorrow""".split())
EXERCISE_NOUNS = frozenset("""heart pulse zone calorie calories macro macros protein
    rep reps weight weights pace treadmill lifting lift sets bodyfat bmi 1rm
    km kilometre kilometres mile miles""".split())


def _work_out_sums(norm):
    hits = set()
    training = any(word in EXERCISE_NOUNS for word in norm)
    for index, word in enumerate(norm):
        if word not in ("work", "works", "working", "worked") or index + 1 >= len(norm):
            continue
        if norm[index + 1] != "out":
            continue
        after = norm[index + 2:index + 8]
        if len(after) >= 3 and after[0] in NUMBER_WORDS and after[1] == "times" \
                and after[2] in NUMBER_WORDS:
            hits.add(index)
            continue
        if training or any(word in EXERCISE_AFTER for word in after[:3]):
            continue
        if any(word in SUMS_AFTER or word in NUMBER_WORDS for word in after) \
                or any(word.isdigit() for word in after):
            hits.add(index)
    return hits


CANCELS = (
    (re.compile(r"\bhow (?:do|does|did|would|will|should) (?:[a-z]+ ){0,3}?work\b"), "work"),
    (re.compile(r"\bhow (?:it|they|this|that|these|those) works?\b"), "work"),
    (re.compile(r"\b(?:does|do|will|would|can|could) (?:it|that|this|they) work\b"), "work"),
    (re.compile(r"\bwhat makes (?:[a-z]+ ){0,3}?work\b"), "work"),
)
CANCEL_AFTER = frozenset("""
    for with in on at to out up like if when as that this it than from about
    and or but so then though because
""".split())

PHRASES = {
    "cooking": ("packed lunch", "packed lunches", "party food", "lunch box", "lunchbox",
                "how long should i cook", "how do i cook", "what can i make", "what can i cook",
                "main course", "cooking for", "i am cooking", "cook for", "easy dinner",
                "quick dinner", "quick meal", "use up",
                "birthday cake", "something to cook", "cook tonight", "meal for",
                "sunday roast", "roast dinner for", "christmas dinner",
                "yorkshire pudding", "yorkshire puddings",
                "pressure cooker", "slow cooker", "air fryer",
                "leftover", "meal idea", "meal ideas", "dinner idea", "dinner ideas",
                "something quick", "under cooked", "ice cream",
                "chopping board", "chopping boards", "cutting board", "cutting boards"),
    "food-and-drink": ("book a table", "a table for", "table for two", "table for four",
                       "high in iron", "iron rich", "rich in iron", "low in iron", "low iron",
                       "iron levels", "iron level", "iron deficiency", "deficient in iron",
                       "more iron", "iron in", "sources of iron", "getting enough iron",
                       "enough iron", "need iron", "anaemic", "anaemia", "anemia", "anemic",
                       "eat out", "go out for dinner", "too much coffee", "less coffee",
                       "ice cream",
                       "is it safe to eat", "out of date", "goes well with", "cheese board",
                       "graze board", "graze boards", "picky bits", "picky tea",
                       "main course", "use by date", "sell by date", "best before",
                       "past its date", "in season"),
    "health": ("see a doctor", "go to the doctor", "should i see a doctor", "sore throat",
               "root canal", "mole checked",
               "throwing up", "throws up", "threw up", "thrown up", "want to throw up",
               "going to throw up", "gonna throw up",
               "high temperature", "blood pressure", "cut my finger", "feeling ill",
               "feel unwell", "get headaches", "have a headache", "my head hurts",
               "making me cry", "stopped bleeding", "wont stop bleeding",
               "signs of a stroke", "burnt my hand", "burnt myself", "burnt my arm",
               "burnt my finger",
               "coming down with", "going down with", "runny nose", "stuffy nose",
               "blocked nose", "bunged up", "bunged nose", "blocked ear", "blocked ears",
               "ear is blocked", "ears are blocked", "ear infection", "sore ears",
               "ringing in my ears", "ears are ringing", "stuffy head", "scratchy throat",
               "sinus infection",
               "my nose is blocked", "my nose is running", "my nose is bunged",
               "my nose is stuffy", "nose bleed", "nose bleeds", "nosebleed",
               "chest congestion", "my chest is congested", "congested chest",
               "nasal congestion", "sinus congestion", "congested nose",
               "im congested", "i am congested", "feel congested", "feeling congested",
               "really congested",
               "mouth ulcer", "mouth ulcers", "ulcer in my mouth", "ulcers in my mouth",
               "ulcer on my tongue", "ulcer on my gum", "canker sore", "canker sores",
               "water in my ear", "water in my ears", "water trapped in my ear",
               "water trapped in my ears", "water stuck in my ear", "water stuck in my ears",
               "water in my ear after swimming", "swimmers ear", "swimmer's ear",
               "upset stomach", "upset tummy", "upset belly", "upset guts",
               "bad guts", "bad belly", "dicky tummy", "dicky stomach",
               "dodgy tummy", "dodgy stomach", "tummy bug", "stomach bug", "sick bug",
               "the runs", "the trots", "the squits", "got the runs", "have the runs",
               "loose stools", "runny tummy", "runny bottom",
               "running to the loo", "running to the toilet", "runs to the loo",
               "runs to the toilet", "back and forth to the loo",
               "stomach is off", "tummy is off", "belly is off", "stomach is queasy",
               "tummy is queasy",
               "diarrhoea", "diarrhea", "sick with diarrhoea", "sick with diarrhea",
               "wisdom tooth", "wisdom teeth", "ingrown toenail", "ingrown nail",
               "ingrowing toenail", "ingrowing nail", "nail is ingrown",
               "nettle sting", "nettle stings", "stung by nettles", "insect bite",
               "insect bites", "insect sting", "bug bite", "bug bites", "hair loss",
               "losing my hair", "going bald", "panic attack", "panic attacks",
               "acid reflux", "acid indigestion", "athletes foot", "athlete's foot",
               "sweating too much", "excessive sweating", "night sweats",
               "heavy period", "period pain", "period pains", "period cramps",
               "on my period", "missed period", "late period", "irregular periods",
               "stop sweating", "sweat so much", "sweating a lot", "sweat a lot",
               "lump in my breast", "lump in my armpit", "lump in my neck",
               "lump under my skin", "swollen glands", "glands are up"),
    "fitness": ("out of breath", "get fit", "lose weight", "work out", "start running",
                "training for", "train for", "train hard", "lower back"),
    "sleep": ("get to sleep", "back to sleep", "wake up", "wakes up", "can not sleep",
              "cant sleep", "sleep through"),
    "money": ("save for", "how much should i save", "pay off", "stamp duty", "worth paying",
              "interest rate", "interest rates", "savings account", "the interest",
              "compound interest",
              "cut my bills", "energy bills", "energy bill", "electricity bill",
              "gas bill", "water bill", "small salary", "how should i budget"),
    "work": ("my boss", "my manager", "job interview", "my colleague", "teaching assistant",
             "performance review", "my team", "too much on my plate",
             "public speaking", "speaking in front of people", "speaking in front of an audience",
             "in front of an audience", "speaking to a room", "before a talk", "at a talk",
             "giving a talk", "give a talk", "nervous about my presentation"),
    "school-and-study": ("revise for", "exam in", "how do i revise", "learn vocabulary",
                         "struggling with", "get started on", "science project",
                         "school project", "for an exam", "a degree worth",
                         "degree still worth", "do a degree",
                         "a-level results", "do my a-levels", "my mocks",
                         "mock exam", "mock exams", "mocks in", "mocks next"),
    "science": ("how does it work", "why does", "why is the sky", "what is the difference between",
                "how do plants", "in a nutshell", "speed of light", "how many moons",
                "why is it hotter",
                "human body", "bones in the", "bones are in", "how many bones",
                "what causes an earthquake", "what causes earthquakes", "how do earthquakes",
                "why do earthquakes", "earthquake happen", "earthquakes happen",
                "how do tsunamis", "what causes a tsunami", "tsunami warning",
                "what causes a volcano", "how do volcanoes", "volcano erupt", "volcano erupts",
                "volcano erupted", "volcanoes erupt", "volcano erupting",
                "volcanoes work", "volcano work", "volcano project", "volcanoes project", "project on volcanoes",
                "project on volcano", "volcanic eruption"),
    "history": ("who built", "when did", "in a nutshell", "roman empire", "industrial revolution",
                "slave trade", "genghis khan",
                "great wall of china", "ancient china",
                "berlin wall", "the berlin wall", "cold war",
                "moon landing",
                "titanic sank", "titanic sink", "titanic sinking", "titanic wreck",
                "titanic iceberg", "the titanic hit", "when did the titanic",
                "how did the titanic", "why did the titanic",
                "the tudors", "tudor period", "tudor times", "tudor england"),
    "geography-and-travel": ("day trip", "jet lag", "shouldn miss", "don t miss",
                             "what should i see", "long flight", "car journey",
                             "capital of", "book a flight", "book a hotel",
                             "book a train", "book a room", "by coach", "a coach to",
                             "coach from", "coach station", "coach trip", "coach leaves",
                             "by train", "train ticket", "train tickets", "train station",
                             "train times", "train fare", "train fares", "catch the train",
                             "the next train", "the last train", "missed the train", "missed my train",
                             "the train to", "train to london", "train to leeds"),
    "technology": ("battery drains", "wont turn on", "wont start", "keeps dropping",
                   "improve the signal", "take a screenshot", "password manager", "group chat"),
    "home-and-diy": ("get rid of", "unblock", "bleed the radiator", "front door", "back door",
                     "clothes iron", "steam iron", "iron a shirt", "iron the shirt",
                     "iron my shirt", "iron a few shirts", "ironing board", "iron board",
                     "my iron", "the iron", "our iron", "iron is broken", "iron broke",
                     "iron has broken", "iron stopped", "iron wont heat", "iron is not heating",
                     "iron is leaking", "iron spits", "iron spitting", "never iron",
                     "never ironing", "hate ironing", "creases out of", "crease out of",
                     "get creases", "stop creases", "trousers creased", "iron the creases",
                     "heat pump", "heat pumps", "cold at the top",
                     "desk fan", "desk fans", "ceiling fan", "ceiling fans",
                     "hot at the bottom", "get red wine out", "paint my", "second hand",
                     "do the dishes", "wash the dishes", "the dishes", "dishes are",
                     "the spring on", "spring broke", "spring has gone", "a new spring",
                     "the spring needs",
                     "smoke alarm", "wont flush", "won t flush", "cold air coming",
                     "water pressure", "low pressure", "pressure gauge",
                     "wood burner", "woodburner", "log burner", "log fire", "wood fire",
                     "burning stove", "wood stove", "fire place"),
    "garden-and-plants": ("turning yellow", "easy to grow", "when should i plant",

                          "plant bulbs", "on the balcony",
                          "when do i harvest", "when should i harvest", "when can i harvest",
                          "when do i sow", "when should i sow", "when can i sow",
                          "when do i lift", "when should i lift", "ready to harvest",
                          "ready to lift"),
    "pets": ("pulls on the lead", "dangerous for dogs", "clean the tank", "getting a puppy",
             "getting a kitten", "rescue dog", "stopped eating", "has not eaten"),
    "family-and-parenting": ("starting school", "with kids", "for my son", "for my daughter",
                             "potty training",
                             "health visitor", "health visitors", "my health visitor",
                             "my parents are visiting", "birthday party",
                             "watch the kids", "watching the kids", "watch my kids",
                             "to watch my kids", "to watch the kids", "to watch the children",
                             "someone to watch"),
    "friends-and-relationships": ("forgot my birthday", "make friends", "anniversary gift",
                                  "had an argument", "bring it up", "best friend",
                                  "on a date", "date night", "blind date", "first date",
                                  "going on a date", "a date with",
                                  "fell out with", "avoiding me", "stopped asking me out",
                                  "stopped speaking to me", "not speaking to me"),
    "shopping": ("worth it", "worth the money", "should i look for", "before buying",
                 "second-hand", "which one should i buy", "buying a car", "used car",
                 "worth paying", "good deal", "bad deal", "better deal", "a deal",
                 "the store", "at the store", "to the store", "in the store", "store was",
                 "store is", "which store", "store sells", "store open", "store closed",
                 "any store", "the shops",
                 "what specs", "how much should a decent"),
    "cars": ("jump start", "warning light", "engine light", "tyre pressure", "oil change",
             "break down", "broken down", "hard shoulder", "won t start", "wont start",
             "won t turn over", "new tyres", "car insurance", "road tax", "mot due",
             "mot fail", "failed its mot", "car tax"),
    "entertainment": ("harry potter", "what should i read", "what should i watch", "anything good",
                      "watch tv", "watch a film", "watch a movie", "watch a series",
                      "watching tv", "watch the match", "watching the match",
                      "something to watch", "anything to watch", "what can i watch",
                      "can i watch", "this book", "a book about", "book club", "which book",
                      "a book for", "what book", "good book", "need a book", "book to read",
                      "book recommendations", "recommend a book", "books for", "favourite book",
                      "favorite book", "to watch", "worth watching", "what to read",
                      "family night", "board game", "play station", "playstation",
                      "for my commute", "season ticket",
                      "season finale", "new season of", "next season of", "series finale"),
    "sport": ("offside rule", "world cup", "how does the game work", "my coach", "coached",
              "coaching", "the match", "match is on", "match tonight", "match day",
              "cricket match", "football match", "rugby match", "tennis match",
              "darts match", "boxing match",
              "this season",
              "next season", "pre-season"),
    "language-and-writing": ("difference between", "is it bad to say", "how do i word",
                             "without sounding rude", "can you help me word"),
    "feelings": ("i feel", "i am feeling", "been feeling", "feel like", "so stressed",
                 "so done", "done with today", "done with this week", "done with today",
                 "fed up", "had enough", "long day", "what a day", "tough day", "rough day",
                 "really lonely", "i am nervous", "nervous about", "i am worried",
                 "i am gutted", "i am upset", "let off steam", "miss my old",
                 "get everything wrong", "gets everything wrong", "do everything wrong",
                 "did everything wrong", "doing everything wrong", "doing it all wrong",
                 "did it all wrong", "everything i do goes wrong", "everything i do is wrong",
                 "mess everything up", "messed everything up", "messing everything up",
                 "mess it all up", "messed it all up", "cant do anything right",
                 "can not do anything right", "never get anything right",
                 "never do anything right"),
    "small-talk": ("how s your day", "how is your day", "how are you", "how is it going",
                   "nice to meet you", "what s up", "any plans", "plans for the weekend",
                   "up to this weekend", "this weekend", "weekend plans"),
    "opinions": ("what do you think", "do you think", "your favourite", "which do you prefer"),
    "creative": ("write a poem", "tell me a joke", "name for", "opening line"),
    "maths-and-numbers": ("how many weeks", "how much is", "percent of", "what is the average",
                          "miles an hour", "miles per hour", "km an hour",
                          "per hour", "per day", "per week", "how many miles"),
    "nature-and-weather": ("change colour", "change color", "leaves change", "leaves fall",
                           "leaves turn", "in a thunderstorm", "in the spring", "this spring",
                           "next spring", "spring is", "spring flowers", "early spring",
                           "going to rain", "will it rain", "is it going to be sunny",
                           "birds might i see", "leaves are"),
    "about-the-bot": ("are you a bot", "are you real", "are you human", "what are you",
                      "who are you", "do you remember", "what can you do",
                      "what kind of things can you help", "how can you help",
                      "how was your day", "how has your day been", "hows your day been",
                      "how s your day been", "hows your day going", "how was your week",
                      "how has your week been", "hows your week been", "how s your week been",
                      "how have you been", "how you been"),
}

NOT_THINGS = frozenset("""
cook cooking bake baking boil boiled frying fry roast roasted grill simmer chop chopped stir
eat eating drink drinking feed fed save saving pay paid spend spent buy buying bought sell
sold work working revise revising study studying learn learning teach taught travel travelling
traveling fly flying drive driving pack packing book booking plan planning move moving rent
watch watching read reading write writing wrote felt feel feeling sleep sleeping slept wake
waking run running jog jogging train training exercise stretching stretch grow growing plant
planting water watering clean cleaning fix fixing paint painting repair repairing adopt adopted
rescue buy fix bleed bleeding cut chopped knocked dropped broke broken spill spilled leak
leaking drain drains turned turning turned stuck stop stopped start started finish finished
scrambled poached undercooked overcooked sticky mushy crispy hungry thirsty tasty delicious
expensive cheap worth tired exhausted lonely sad unhappy upset anxious worried nervous stressed
overwhelmed depressed crying angry annoyed frustrated guilty ashamed jealous happy excited
relieved proud grateful dizzy sore ill sick unwell allergic vegan vegetarian second-hand
best better worst good bad great nice lovely favourite favorite perfect brilliant amazing
fine okay first second third last next more less most least many few several some
percent percentage maths math number numbers average total half double
log lag row sow hoe
""".split())

THINGS = frozenset(
    word
    for words in STRONG.values()
    for word in words.split()
    if len(word) > 2 and word.isalpha() and word not in NOT_THINGS
)

PLACES = frozenset("""
london paris rome florence lisbon madrid barcelona berlin amsterdam brussels dublin edinburgh
glasgow manchester birmingham leeds liverpool bristol cardiff belfast newcastle oxford
cambridge brighton york bath bristol glasgow tokyo kyoto osaka beijing shanghai hong kong
singapore bangkok sydney melbourne auckland delhi mumbai goa istanbul athens cairo dubai
new york chicago boston seattle toronto vancouver mexico brazil argentina spain france
italy germany portugal greece turkey egypt india china japan korea thailand vietnam canada
australia america england scotland wales ireland europe africa asia
eiffel
""".split())

UNIT_WORDS = {
    "g": "g", "gram": "g", "grams": "g", "gramme": "g", "grammes": "g",
    "kg": "kg", "kilo": "kg", "kilos": "kg", "kilogram": "kg", "kilograms": "kg",
    "lb": "lb", "lbs": "lb", "pound": "lb", "pounds": "lb",
    "oz": "oz", "ounce": "oz", "ounces": "oz",
    "ml": "ml", "millilitre": "ml", "millilitres": "ml", "milliliter": "ml",
    "l": "litre", "litre": "litre", "litres": "litre", "liter": "litre", "liters": "litre",
    "tsp": "tsp", "teaspoon": "tsp", "teaspoons": "tsp",
    "tbsp": "tbsp", "tablespoon": "tbsp", "tablespoons": "tbsp",
    "cup": "cup", "cups": "cup",
    "c": "celsius", "°c": "celsius", "celsius": "celsius", "centigrade": "celsius",
    "f": "fahrenheit", "°f": "fahrenheit", "fahrenheit": "fahrenheit",
    "sec": "seconds", "secs": "seconds", "second": "seconds", "seconds": "seconds",
    "min": "minutes", "mins": "minutes", "minute": "minutes", "minutes": "minutes",
    "hr": "hours", "hrs": "hours", "hour": "hours", "hours": "hours",
    "day": "days", "days": "days", "week": "weeks", "weeks": "weeks",
    "month": "months", "months": "months", "year": "years", "years": "years",
    "mile": "miles", "miles": "miles", "km": "km", "kilometre": "km",
    "kilometres": "km", "kilometer": "km", "kilometers": "km",
    "metre": "metres", "metres": "metres", "meter": "metres", "meters": "metres",
    "foot": "feet", "feet": "feet", "ft": "feet", "inch": "inches", "inches": "inches",
    "mph": "mph", "percent": "percent", "%": "percent",
    "quid": "gbp", "£": "gbp", "euro": "eur", "euros": "eur", "€": "eur",
    "dollar": "usd", "dollars": "usd", "$": "usd",
    "people": "people", "person": "people", "kid": "people", "kids": "people",
    "adult": "people", "adults": "people", "guest": "people", "guests": "people",
}
WORD_NUMBERS = {
    "half": 0.5, "one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6,
    "seven": 7, "eight": 8, "nine": 9, "ten": 10, "eleven": 11, "twelve": 12,
    "thirteen": 13, "fourteen": 14, "fifteen": 15, "sixteen": 16, "seventeen": 17,
    "eighteen": 18, "nineteen": 19,
    "twenty": 20, "thirty": 30, "forty": 40, "fifty": 50, "sixty": 60,
    "seventy": 70, "eighty": 80, "ninety": 90,
    "hundred": 100, "thousand": 1000, "couple": 2, "dozen": 12,
}
FIGURE_SIZE_WORDS = frozenset("""k ks grand thousand million millionaire billion bn mil mths""".split())

NUMBER_RE = re.compile(r"(\d+(?:[.,]\d+)?)\s*(%|[a-z]+)?")

CLIPPED_UNIT_WORDS = {
    "yr": "years", "yrs": "years", "y": "years", "yo": "years", "yos": "years",
    "mth": "months", "mths": "months", "mnt": "months", "mnts": "months",
    "wk": "weeks", "wks": "weeks",
}
CLIPPED_AFTER_A_SLASH = re.compile(r"\s*(?:y/o|y\.o\.?|yo)\b")

MIXED_FRACTION = re.compile(r"\s+(?:(?:and|n)\s+)?(?:(?:a|an)\s+)?(?:half|quarter)s?\b")
MIXED_JOINERS = frozenset(("", "n", "and", "a", "an"))

_BREAKS = re.compile(r"[^a-z0-9' ]+")


CARRY = 2
BODY = lexicon.BODY_PARTS
HURTS = lexicon.PAIN_WORDS
SKIN_STATES = frozenset("""dry drier dryness flaky flakes flaking cracked cracking chapped
    itchy itching peeling""".split())
SKIN_REACH = 3
SKIN_BOOST = 4
SKIN_PARTS = BODY | frozenset("""face cheeks cheek knuckles knuckle lips lip mouth heels""".split())
HEAD_WORDS = frozenset("""head brain mind thoughts thinking concentration memory""".split())


HEAD_FOG = frozenset("fog foggy cloudy misty muzzy woolly wooly fuzzy thick".split())
HEAD_FOG_REACH = 4
HEAD_FOG_BOOST = 6


def _head_fog(norm):
    foggy = [at for at, word in enumerate(norm) if word in HEAD_FOG]
    if not foggy:
        return False
    for at, word in enumerate(norm):
        if word in HEAD_FOG or word not in HEAD_WORDS:
            continue
        if any(0 < other - at <= HEAD_FOG_REACH for other in foggy):
            return True
    return False


def _skin_state(norm, skip):
    states = [at for at, word in enumerate(norm)
              if word in SKIN_STATES and at not in skip]
    if not states:
        return None
    for at, word in enumerate(norm):
        if word not in SKIN_PARTS or at in skip:
            continue
        if any(abs(state - at) <= SKIN_REACH for state in states):
            return at
    return None


PLAYS_UP_BEFORE = frozenset("""playing playin plays play played acting acts acted
    """.split())
PLAY_UP_REACH = 3
PART_UP_BOOST = 4


def _a_part_plays_up(norm, skip):
    ups = [at for at, word in enumerate(norm)
           if word == "up" and at and at not in skip
           and (norm[at - 1] in PLAYS_UP_BEFORE
                or (at >= 2 and norm[at - 1] in ("me", "my")
                    and norm[at - 2] in PLAYS_UP_BEFORE))]
    if not ups:
        return None
    for at, word in enumerate(norm):
        if word not in BODY or at in skip:
            continue
        if any(0 < up - at <= PLAY_UP_REACH for up in ups):
            return at
    return None


HURT_BOOST = 5
CONDITION_BOOST = 4
CONDITIONS = frozenset("""cystitis uti thrush dandruff eczema asthma verruca verrucas piles
    haemorrhoids sciatica gout stye styes shingles tonsillitis arthritis coeliac anaemic anaemia
    psoriasis rosacea conjunctivitis bronchitis pneumonia appendicitis vertigo tinnitus
    endometriosis ibs crohns colitis prolapse bunion bunions whitlow ringworm scabies nits
    headlice hypo hypos coldsore coldsores abscess quinsy phlebitis dvt cataract cataracts
    glaucoma gingivitis hiccup hiccups thyroid constipated
    boil boils lump lumps spot spots cyst cysts filling fillings
    pcos copd lupus fibromyalgia hashimotos hypothyroid hyperthyroid epilepsy diabetes
    anorexia bulimia cfs ibd""".split())
CONDITION_NEEDS_PART = frozenset("""boil boils lump lumps spot spots cyst cysts""".split())
CONDITION_NEEDS_WORD = {
    "filling": frozenset("""tooth teeth molar molars cavity cavities dentist dental gum gums
        filled""".split()),
    "fillings": frozenset("""tooth teeth molar molars cavity cavities dentist dental gum gums
        filled""".split()),
}
CONDITION_OTHER_LIFE = {
    "thrush": frozenset("garden lawn bird birds nest hedge tree trees feeder".split()),
    "shingles": frozenset("roof roofs tile tiles tiled shed sheds wall walls house chimney slate".split()),
}
CONDITION_NOT_NEXT = {
    "piles": frozenset("of".split()),
}
CONDITION_REACH = 3


def _named_condition(norm, words, skip):
    if words & PETS and not words & (_person_words() - PETS):
        return False
    for at, word in enumerate(norm):
        if word not in CONDITIONS or at in skip:
            continue
        nexts = CONDITION_NOT_NEXT.get(word)
        if nexts and at + 1 < len(norm) and norm[at + 1] in nexts:
            continue
        other = CONDITION_OTHER_LIFE.get(word)
        if other and words & other:
            continue
        if word in CONDITION_NEEDS_PART and not any(
                abs(other_at - at) <= CONDITION_REACH and other_word in BODY
                for other_at, other_word in enumerate(norm) if other_at not in skip):
            continue
        wanted = CONDITION_NEEDS_WORD.get(word)
        if wanted and not any(
                abs(other_at - at) <= CONDITION_REACH and other_word in wanted
                for other_at, other_word in enumerate(norm) if other_at not in skip):
            continue
        return True
    return False
UNWELL_BOOST = 3
PEOPLE_TOPICS = ("family-and-parenting", "friends-and-relationships", "pets")
UNWELL_SIGNS = frozenset("""unresponsive unconscious drowsy confused floppy limp listless
    dehydrated collapsed fitting seizure seizures temperature fever sepsis bleeding puking
    puke puked barf
    breathless rash cold cough flu dizzy vomiting vomit diarrhoea diarrhea constipated
    wheeze wheezing swollen infection itchy ill unwell allergy allergic diabetic diabetes
    overdose pills operation surgery chemo chemotherapy fell fall fallen broken broke
    fracture fractured stroke injured injury""".split())
UNWELL_NOT = frozenset("""feeding drinking eating responding waking weeing""".split())
NOUNY_SIGNS = frozenset("""temperature cold cough flu pills pill operation surgery infection
    rash seizure seizures allergy overdose chemo chemotherapy diabetes dose medicine""".split())
EXTRA_PEOPLE = frozenset("""newborn newborns toddler toddlers baby babies person people someone
    somebody anyone anybody child children kid kids""".split())


def _person_words():
    words = set(RELATIONS) | EXTRA_PEOPLE | PETS
    for topic in ("family-and-parenting", "friends-and-relationships"):
        words |= set(STRONG[topic].split())
    return frozenset(words)


SIGN_FOLLOWS = frozenset("""a an the his her my your our their its is was are were am has have
    had got get gets of and or but so to for in on at with from since last this that these those
    today tonight yesterday morning night now still again too very really all just should shall
    will would can could do does did not no time times day days week weeks month months about
    up down out over""".split())
HEARERS = frozenset("""me us name names pain voice voices anything anyone nothing stimulus
    sounds noise light lights it them him her breakfast medicine""".split())
COMMS = frozenset("""text texts message messages phone phones mobile mobiles email emails
    call calls whatsapp dm dms letter letters post emailing texting""".split())
BEHAVIOUR = frozenset("""when whenever if unless because after before till until once while""".split())
SIGN_NOT_AFTER = frozenset("""asleep out over apart behind short through pregnant ill about
    for""".split())
UNWELL_IDIOMS = ("bleeding me dry", "bleed me dry", "bleeding us dry", "bleed us dry",
                 "drove me mad", "driving me mad", "worried sick", "bored stiff")
PETS = frozenset("""dog dogs puppy puppies cat cats kitten kittens rabbit hamster parrot goldfish
pet pets""".split())
OWNERS = frozenset("""my our his her their""".split())
ANIMALS = frozenset("""dog dogs puppy puppies cat cats kitten kittens rabbit rabbits hamster
hamsters guinea parrot parrots budgie budgies goldfish fish tortoise tortoises turtle turtles
snake snakes lizard lizards gecko geckos horse horses pony""".split())
PET_BOOST = 3
COUNTRY_BOOST = 6
GIFT_WORDS = frozenset("gift gifts present presents".split())
GIFT_ALWAYS = frozenset("gifts presents".split())
GIVE_VERB = frozenset("get gets got gotten getting buy buys buying bought pick wrap".split())
GIFT_WANTING = frozenset("""need needs needed needing still yet havent havnt haventgot
    must should ought havent got gotta later tomorrow soon""".split())
GIVE_TO = frozenset("""her him them mum mom mother dad father sister brother nan gran
    granny grandma grandad grandpa friend friends teacher husband wife partner son daughter
    nephew niece colleague boss kids child children inlaws flatmate flatmates housemate
    roommate mate mates cousin cousins aunt aunty uncle neighbour neighbor girlfriend
    boyfriend""".split())
GIFT_OCCASION = frozenset("""christmas xmas birthday anniversary wedding graduation
    leaving retiring retirement""".split())
GIFT_ASKING = frozenset("""should could would shall what which worth best any idea ideas""".split())
GIVE_THING = frozenset("""something anything ideas idea nothing""".split())
GIFT_BOOST = 5
GIFTS_OR_OCCASIONS = GIVE_THING | GIFT_WORDS | GIFT_OCCASION
GIVE_THINGS = GIVE_THING | GIFT_WORDS
GIVE_DETERMINERS = frozenset("my your his their our the a an some".split())
GIVE_RELATIVE = frozenset("who whos that".split())

CROP_STATES = ("not ripening", "going blue", "gone blue", "going yellow", "turning yellow",
               "gone to seed", "blossom end rot", "not flowering", "no flowers", "not fruiting",
               "no fruit", "ripening", "bolting", "leggy", "wilting", "drooping", "rotting",
               "rotten", "stunted", "flowering", "splitting", "dying")
CROP_KITCHEN = frozenset("""fridge freezer cupboard pantry shelf shop shops supermarket market
bag box tub jar tin pan pans oven hob pot pots bowl plate dinner lunch tea recipe cook cooked
cooking eat eating mash roast boil boiled fry fried bake baked salad sandwich soup sauce""".split())
CROPS = frozenset("""tomato tomatoes tom toms potato potatoes courgette courgettes zucchini
cucumber cucumbers pepper peppers chilli chillies chili chillis carrot carrots onion onions
leek leeks garlic lettuce spinach kale cabbage cabbages bean beans pea peas strawberry
strawberries raspberry raspberries blackberry blackberries blueberry blueberries apple apples
pear pears plum plums cherry cherries grape grapes rhubarb beetroot beetroot parsnip parsnips
squash pumpkin marrows marrow broccoli cauliflower sweetcorn corn aubergine aubergines
basil mint parsley rosemary thyme coriander chives sage oregano dill herbs herb""".split())
GROWING_PLACES = frozenset("""plant plants vine vines tree trees greenhouse greenhouse allotment
allotments garden plot pots bed beds border seedling seedlings bush bushes""".split())
CROP_BOOST = 3
TRAVEL_CUES = frozenset("""trip holiday flight fly flying visit visiting travel travelling
traveling abroad hotel booking itinerary sightseeing tourist stay staying going go get
plan plans planned planning break weekend week days""".split())

WORLD = frozenset("""sun sky moon stars earth planets planet ocean sea river mountain
mountains snow ice rain wind thunder lightning clouds tides gravity rainbow seasons
winter summer spring autumn frost temperature fish fishes bird
birds animal animals insects bees brain bones lungs cells atoms veins""".split())
WORLD |= BODY - frozenset("back hand hands arm arms leg legs foot feet chest".split())
WORLD_NOT = frozenset("maker machine tray cube bin bucket box cream lolly lollies".split())
NATURE_WORDS = frozenset(STRONG["nature-and-weather"].split())
MECHANISM = ("why", "how")
MECHANISM_HOW = frozenset("old many long far hot cold big deep fast wide".split())
SCIENCE_BOOST = 2
VERB_CUES = {
    "school-and-study": frozenset("""revise revising revision""".split()),
}
STUDY_OBJECTS = frozenset("""exam exams test tests mock mocks gcse a-level alevel biology
chemistry physics maths math history geography french spanish german notes revision
coursework subject term paper spelling vocabulary homework school college university
class lesson a2 as-level sat sats""".split())
DETERMINERS = frozenset("""my your his her their our the a an this that these those some any""".split())
BODY_CUES = frozenset("""burn burnt burned burning scald scalded scalds cut cuts cutting
    bleed bleeding""".split())
PARTS = frozenset("""me myself yourself himself herself themselves ourselves itself tongue lip
lips gum gums cheek cheeks chin forehead scalp brow eyebrow eyelash eyelid palm palms nail
nails knuckle knuckles thigh thighs calf calves shin shins shing toe toes sole soles mouth
mouths face faces nose noses bottom bottoms bum waist sides upper lower""".split())
BODY_OR_SELF = BODY | PARTS
CUE_CARRIERS = frozenset("""and or but so now again today yesterday tomorrow still then than
    it into in on at when if because very really badly slightly a bit
    down back up out off away through over around first next""".split())

JUDGEMENT_OF_RECORD = re.compile(
    r"\b(?:i|i'm)\s+(?:am |was |have |had |been |being |always |still |just |really |"
    r"keep |keeps |kept |constantly |probably )*"
    r"(?:get|gets|getting|got|do|does|did|doing|mess|messes|messed|messing)\s+"
    r"(?:everything|it all)\s+(?:wrong|up)\b")

NOT_CUT_OUT = re.compile(r"\b(?:cut out|made) (?:for|to be)\b")
NOT_WORDS = frozenset("not never dont don't didnt didn't isnt isn't wasnt wasn't aint ain't".split())
OWN_SELF = frozenset("i im i'm me myself".split())
OTHER_PERSON = frozenset("""he she they hes shes theyre him her them his her their you your
    we we're us our my brother sister son daughter mum mom dad father mother husband wife
    partner friend boss colleague""".split())

def reads_as_unfit(text):
    for match in NOT_CUT_OUT.finditer(text):
        before = text[:match.start()].split()[-6:]
        if not any(word in NOT_WORDS for word in before):
            continue
        person = [word for word in before if word in OWN_SELF or word in OTHER_PERSON]
        if not person or person[-1] not in OWN_SELF:
            continue
        return match.start()
    return None




GIVING_UP = ("gave up", "give up", "given up", "gives up", "giving up", "packed in",
             "packing in", "cut out", "cutting out", "cut down on", "cutting down on",
             "stopped eating", "stopped drinking", "gone off")
GIVEN_UP_FOOD = frozenset(STRONG["food-and-drink"].split()) | frozenset(
    word for word in STRONG["cooking"].split()
    if word in ("meat", "dairy", "gluten", "lactose", "nut", "soya", "soy", "wheat"))
GIVING_UP_BOOST = 3


def _a_habit_given_up(norm):
    text = " ".join(norm)
    if not any(word in GIVEN_UP_FOOD for word in norm):
        return False
    return any(phrase in text for phrase in GIVING_UP)


GENERIC = frozenset("""a an the to of in on at for with my your i you it is and or something
someone thing things any some this that these those be have do does""".split())

POLYSEMOUS = frozenset("""date season store book coach dish match spring watch cream
    pressure""".split())

PORTION_WORDS = frozenset("""half double triple""".split())
PORTION_UNITS = frozenset("""cup cups stone stones pint pints litre litres ml gram grams kilo
kilos kg ounce ounces oz tablespoon tablespoons tbsp teaspoon teaspoons inch inches foot feet
mile miles metre metres metre hour hours minute minutes""".split())

POLY_FORMS = POLYSEMOUS | frozenset(word + "s" for word in POLYSEMOUS)

SEASONS = frozenset("spring summer autumn winter".split())
WEATHER_BEFORE = frozenset("""dry wet cold warm mild harsh hard bad good long short late early
    frosty freezing sunny rainy""".split())
WEATHER_ITSELF = frozenset("""warm cold hot sunny cloudy raining snowing windy icy freezing
    icy humid muggy showers drizzle""".split())

SENSE_WEIGHT = 6
SENSE_REACH = 3
SENSE_NEAR = 2
MACHINE_BIN_WORDS = frozenset("""recycle trash windows mac macbook laptop desktop disk disks
    file files folder folders downloads download storage usb restore permanently""".split())
SENSE_PAIRS = {
    "train": (("train", "trains"), "geography-and-travel", (
        (SENSE_REACH, frozenset("""ticket tickets station platform timetable fare fares rail
            railcard carriage intercity""".split())),
        (SENSE_REACH, frozenset("cancelled cancel delayed delay".split())),
        (SENSE_NEAR, frozenset("""missed miss catch catching missed leaves leaving departs
            departing arrives arrival""".split())),
    )),
    "run": (("run", "runs", "running", "ran"), "geography-and-travel", (
        (SENSE_NEAR, frozenset("""bus buses train trains tram trams coach coaches tube
            ferry ferries flight flights timetable""".split())),
    )),
    "chippy": (("chippy", "chippies"), "home-and-diy", (
        (SENSE_NEAR, frozenset("""door doors hinge hinges hang hanging shelf shelves skirting
            timber joiner joiners fitter fitted""".split())),
    )),
    "mole": (("mole", "moles"), "garden-and-plants", (
        (SENSE_REACH, frozenset("""garden gardens lawn lawns grass hedge hedges border borders
            soil flowerbed flowerbed lawnmower molehill molehills tunnel tunnels""".split())),
    )),
    "root": (("root", "roots"), "garden-and-plants", (
        (SENSE_REACH, frozenset("""plant plants tree trees soil pot pots potted repot repotting
            cutting cuttings seedling seedlings""".split())),
    )),
    "root-canal": (("root", "roots"), "health", (
        (SENSE_NEAR, frozenset("""canal tooth teeth dentist dental filling abscess gum
            gums""".split())),
    )),
    "root-maths": (("root", "roots"), "maths-and-numbers", (
        (SENSE_NEAR, frozenset("""square squares squared cube cubed equation equations
            number numbers solve solved divided prime""".split())),
    )),
    "root-access": (("root", "roots"), "technology", (
        (SENSE_NEAR, frozenset("""phone android device access enable enabled boot bootloader
            samsung pixel tablet""".split())),
    )),
    "stock": (("stock", "stocks"), "money", (
        (SENSE_NEAR, frozenset("""market markets share shares trading trader exchange portfolio
            dividend dividends isa""".split())),
    )),
    "stock-pot": (("stock", "stocks"), "cooking", (
        (SENSE_NEAR, frozenset("""cube cubes pot pan soup gravy vegetable chicken beef ham
            simmer simmering broth""".split())),
    )),
    "match": (("match", "matches"), "home-and-diy", (
        (SENSE_REACH, frozenset("""box damp flame flames firelighter firelighters kindling bbq
            barbecue burner smoulder smolder""".split())),
        (SENSE_REACH, frozenset("light lights lit strike struck".split())),
    )),
    "bin": (("bin", "bins"), "technology", (
        (SENSE_REACH, MACHINE_BIN_WORDS),
    )),
}


def the_bin_is_on_a_machine(understood):
    words = set((understood or {}).get("words") or ())
    if words & MACHINE_BIN_WORDS:
        return True
    return "technology" in ((understood or {}).get("topics") or ())


TWO_LIVES = {
    "bank": (("bank", "banks"), (
        (frozenset("""account accounts money cash card cards overdraft loan loans mortgage
            mortgages payment payments paid pay savings branch branches switch switches
            statement statements balance balances deposit deposits withdraw withdrawal
            transfer transfers debit credit cheque cheques interest debt debts atm cashpoint
            salary salaries wages building society current holiday holidays food blood
            england sperm said says told rang ring called phoned robbed robbery robber cashier teller
            vault charge charges charged charging fee fees refund refunds claim claims useless
            overdrawn locked blocked phone app online free pending shut shuts empty sunday
            sundays saturday saturdays weekday weekdays hours opening opens""".split()),
         frozenset(("money", "shopping", "life-admin", "work-and-money"))),
        (frozenset("""river rivers water fish swim swimming path paths walk walked walking boat
            boats flood flooded muddy grass trees reeds ducks swans fishing current currents
            flow steep bridge bridges canal canals lake lakes stream streams shore bankside""".split()),
         frozenset(("nature-and-weather", "geography-and-travel", "fitness", "home-and-diy"))),
    )),
    "seal": (("seal", "seals"), (
        (frozenset("""zoo sea beach ocean shore rocks ice swimming fish pup pups rescue wildlife
            aquarium flipper flippers colony warden vet injured entangled plastic cute cuddly
            adorable""".split()),
         frozenset(("pets", "nature-and-weather", "geography-and-travel"))),
        (frozenset("""jar jars lid lids door doors window windows freezer fridge container
            containers bottle bottles cap caps rubber gasket airtight vacuum preserve jam
            pickle filter filters oven washing machine drum black mould mold leak leaks
            leaking leaked dripping split torn worn perished hardened stiff sticky crumpled
            shut shuts""".split()),
         frozenset(("home-and-diy", "cooking", "cleaning", "food-and-drink"))),
    )),
}
TWO_LIVES_FORMS = {form: tiers for _forms, tiers in TWO_LIVES.values() for form in _forms}
TWO_LIVES_REACH = 99
_A_STATE_VERB = frozenset("""is are was were has have had looks seems seemed becomes became
    sounds feels closed shut broke broken breaks split splits tore torn worn wears""".split())
_THE_OWNER_SETTLES = frozenset(("bank",))
_POSSESSIVE = frozenset("my our your his her their".split())
_NOT_THE_SUBJECT = frozenset("""a an the my our your his her their this that these those i we
    you he she they it there old new local main high street current former usual regular
    well so but and oh hmm actually honestly anyway right now then also just only even
    hi hello hey good morning afternoon evening please thanks thank perhaps maybe""".split())


def unclear_subject(norm, inherited=None, previous=None):
    content = [at for at, word in enumerate(norm) if word not in _NOT_THE_SUBJECT]
    if not content:
        return None
    first = content[0]
    word = norm[first]
    tiers = TWO_LIVES_FORMS.get(word)
    if not tiers:
        return None
    if word in _THE_OWNER_SETTLES and first and norm[first - 1] in _POSSESSIVE:
        return None
    if inherited and any(inherited in sense_topics for _cues, sense_topics in tiers):
        return None
    if previous:
        before = set(previous.get("norm") or ())
        if any(before & cues for cues, _sense_topics in tiers):
            return None
    after = [norm[at] for at in content[1:9]]
    if not any(other in _A_STATE_VERB for other in after):
        return None
    if any(_sense_cue(norm, [first], ((TWO_LIVES_REACH, cues),))
           for cues, _sense_topics in tiers):
        return None
    return word


SENSE_ELSEWHERE = {
    "pie": (("pie", "pies"), (
        (SENSE_NEAR, frozenset("chart charts graph graphs diagram diagrams".split())),
    )),
    "jam": (("jam", "jams"), (
        (SENSE_NEAR, frozenset("traffic queued stuck pickle spot trouble bind work".split())),
    )),
    "chips": (("chip", "chips"), (
        (SENSE_NEAR, frozenset("down poker casino betting stack stacks".split())),
    )),
    "yeast": (("yeast",), (
        (SENSE_NEAR, frozenset("infection infections thrush".split())),
    )),
    "nails": (("nail", "nails"), (
        (SENSE_REACH, frozenset("""shelf hammer wooden wood wall walls box boxes diy rawlplug
            plasterboard studwork picture pictures hang hanging screws screw""".split())),
    )),
    "breast": (("breast", "breasts"), (
        (SENSE_REACH, frozenset("""lump lumps cancer nipple nipples areola sore hurting hurt
            hurts painful ache aches aching swelling discharge mastitis checked checking scan
            mammogram""".split())),
        (SENSE_NEAR, frozenset("milk feeding breastfeeding fed".split())),
    )),
    "spam": (("spam",), (
        (SENSE_REACH, frozenset("post letter letters envelope envelopes doormat junk pile".split())),
    )),
    "thighs": (("thigh", "thighs"), (
        (SENSE_NEAR, frozenset("""tight sore ache aches aching hurt hurts hurting cramp cramps
            chafing""".split())),
    )),
    "icing": (("icing",), (
        (SENSE_REACH, frozenset("""knee knees ankle ankles shoulder elbow muscle muscles
            injury injured swelling sprain bruise bruising hurt hurts""".split())),
    )),
    "fibre": (("fibre", "fiber"), (
        (SENSE_REACH, frozenset("""broadband internet router connection cable provider
            install installed""".split())),
    )),
}


TEETHING_IS_A_FAULT = frozenset("""problem problems trouble troubles fault faults
    niggles issues""".split())
TEETHING_AND_A_CHILD = frozenset("""baby babies child children kid kids toddler toddlers
    son daughter newborn girl boy he she his her their ours""".split())


def _teething_is_a_fault(norm):
    return bool(set(norm) & TEETHING_IS_A_FAULT) and not set(norm) & TEETHING_AND_A_CHILD


SENSE_ELSEWHERE_FORMS = {form: tiers for _forms, tiers in SENSE_ELSEWHERE.values()
                         for form in _forms}


BODY_TWO_LIFE = frozenset("breast breasts thigh thighs".split())
OWNING_WORDS = frozenset("my her his their your our".split())


COLD_WORDS = frozenset("cold freezing frozen chilled".split())
HOT_WORDS = frozenset("""hot boiling roasting sweltering sweaty sweating shivery shivering
    feverish""".split())
WARMTH_WORDS = COLD_WORDS | HOT_WORDS
WARMTH_ARE = frozenset("is are was were am feeling getting being".split()) | frozenset(
    "feel feels felt".split())
WARMTH_DEGREE = frozenset("""a bit lot little tad wee touch really so very too proper bloody
    freezing stone quite that dead still always absolutely proper""".split())
WARMTH_HABITUAL = frozenset("always still".split())
WARMTH_THEN = frozenset("""now today tonight again too still here outside lately""".split())
COLD_PEOPLE = frozenset("""i im i'm iam me she he they we you u everyone everybody someone
    somebody people""".split())


def the_warmth_said(norm):
    for at, word in enumerate(norm):
        if word not in WARMTH_WORDS:
            continue
        back = at - 1
        habit = False
        while back >= 0 and norm[back] in WARMTH_DEGREE:
            if norm[back] in WARMTH_HABITUAL:
                habit = True
            back -= 1
        if back < 1 or norm[back] not in WARMTH_ARE:
            continue
        if habit:
            continue
        who = norm[back - 1]
        if who in COLD_PEOPLE:
            person = True
        elif who in PERSON_WORDS:
            person = True
        elif who.endswith("s") and who[:-1] in PERSON_WORDS:
            person = True
        else:
            person = False
        if not person:
            continue
        rest = [word for word in norm[at + 1:] if word not in WARMTH_THEN]
        if rest and rest[0] not in (".", "!", "?", ","):
            continue
        return word
    return None


def _means_something_else(norm, position):
    if norm[position] == "teething" and _teething_is_a_fault(norm):
        return True
    tiers = SENSE_ELSEWHERE_FORMS.get(norm[position])
    if not tiers:
        return False
    if (norm[position] in BODY_TWO_LIFE and position and norm[position - 1] in OWNING_WORDS):
        return True
    return _sense_cue(norm, [position], tiers)


def says_another_thing(text):
    norm = [word for word in re.split(r"[^a-z0-9]+", str(text or "").lower()) if word]
    return {norm[at] for at in names_another_thing(norm)}


def names_another_thing(norm):
    return frozenset(at for at, word in enumerate(norm)
                     if word in SENSE_ELSEWHERE_FORMS
                     and _means_something_else(norm, at))


MACHINE_WORD_CUES = {
    "mouse": frozenset("""mice kitchen loft attic shed garage garden cupboard bedroom house home
        flat wall walls nest trap traps mousetrap droppings infestation pest pests rodent
        rodents chewing chewed scurrying poison wild tame pet pets caught catch cat cats dog
        dogs cage hutch tank vet alive ran running escape escaped squeak squeaking bait cheese
        bins bin cavity floorboards floorboard living saw seen""".split()),
}
MACHINE_WORD_PHRASES = ("mouse problem", "mouse problems", "mice problem", "mice problems",
                        "mouse infestation", "mouse in the", "mouse in my", "mice in the",
                        "mice in my", "rid of mice", "rid of the mouse", "mouse trap")


def is_a_machine_word(text):
    said = str(text or "").lower().replace("'", "")
    words = set(re.split(r"[^a-z]+", said))
    if "mouse" not in words and "mice" not in words and "mousepad" not in words:
        return False
    if "mice" in words:
        return False
    if any(phrase in said for phrase in MACHINE_WORD_PHRASES):
        return False
    return not (words & MACHINE_WORD_CUES["mouse"])


ASK_PHRASES = frozenset(["any ideas", "do you think"])
ORDINARY_VERBS = frozenset("""keep keeps kept drop drops dropped dropping fall falls falling
    cut cuts cutting stop stops stopped start starts started go goes going get gets getting
    turn turns turned work works worked show shows showed""".split())


_SENSE_TIERS = {}
for _forms, _sense_topic, _tiers in SENSE_PAIRS.values():
    for _form in _forms:
        _SENSE_TIERS.setdefault(_form, []).append((_sense_topic, _tiers))


def _the_sense_the_cues_name(norm, position, word):
    for _topic, tiers in _SENSE_TIERS.get(word, ()):
        if _sense_cue(norm, [position], tiers):
            return True
    return False


def _sense_cue(norm, positions, tiers):
    for cue_at, word in enumerate(norm):
        for reach, cues in tiers:
            if word not in cues:
                continue
            for spot in positions:
                if spot - reach <= cue_at <= spot + reach:
                    return True
    return False


def _index():
    table = {}

    def add(key, topic, weight):
        entries = table.setdefault(key, [])
        for index, (seen, points) in enumerate(entries):
            if seen == topic:
                if weight > points:
                    entries[index] = (topic, weight)
                return
        entries.append((topic, weight))

    for topic, words in STRONG.items():
        for word in words.split():
            if word not in GENERIC:
                add(word, topic, 2)
    for topic, words in WEAK.items():
        for word in words.split():
            if word not in GENERIC:
                add(word, topic, 1)
    for name in CAR_NAMES:
        add(name, "cars", 2)
    for topic, phrases in PHRASES.items():
        for phrase in phrases:
            key = " ".join(_BREAKS.sub(" ", phrase).split())
            if key and key not in GENERIC:
                ordinary = all(word in ORDINARY_VERBS for word in key.split())
                add(key, topic, 1 if key in ASK_PHRASES or ordinary else 3)
    return table


CAR_NAMES = frozenset("""audi fords ford vauxhall toyota honda nissan renault peugeot citroen
    skoda hyundai kia mazda volvo suzuki bmw mercedes volkswagen vw fiat tesla dacia chevrolet
    chrysler dodge subaru mitsubishi lexus saab alfa jeep bentley porsche ferrari lamborghini
    aston lada daewoo infiniti acura punto corsa clio astra mondeo passat micra yaris fabia
    octavia ibiza qashqai juke captur kadjar sandero duster sprinter picanto zafira insignia
    vectra laguna megane berlingo picasso cupra leon toledo kamiq karoq kodiaq tucson sportage
    camaro impreza forester hilux auris avensis prius celica supra aygo navara""".split())


TABLE = _index()


def _takes_an_object(norm, position):
    return position + 1 < len(norm) and norm[position + 1] in DETERMINERS


def _acts_on_a_thing(topic, words, norm, start):
    for offset, word in enumerate(words):
        if word in VERB_CUES.get(topic, ()):
            return _takes_an_object(norm, start + offset)
    return False


DEGREE_NOUNS = frozenset("lot lots bit little much few couple plenty".split())


def _thing_a_cue_acts_on(norm, position):
    if not _takes_an_object(norm, position):
        return ""
    index = position + 2
    noun = norm[index] if index < len(norm) else ""
    if noun in DEGREE_NOUNS and not (index + 1 < len(norm) and norm[index + 1] == "of"):
        return ""
    while index + 1 < len(norm) and norm[index + 1] == "of":
        index += 2
        if index < len(norm) and norm[index] in DETERMINERS:
            index += 1
        noun = norm[index] if index < len(norm) else noun
    return noun


def _acts_on_the_body(norm, position):
    thing = _thing_a_cue_acts_on(norm, position)
    if thing:
        return thing in BODY_OR_SELF
    after = norm[position + 1:position + 2]
    if after and after[0] not in BODY_OR_SELF and after[0] not in CUE_CARRIERS:
        others = {topic for index, word in enumerate(norm)
                  if index != position and word not in POLY_FORMS
                  for topic, weight in _lookup(word)
                  if weight >= 2 and topic not in ("health", "small-talk")}
        return not others
    return True


RUN_OUT_BEFORE = frozenset("run runs running ran".split())


def _is_run_out(norm, position):
    return (norm[position] in RUN_OUT_BEFORE and position + 1 < len(norm)
            and norm[position + 1] == "out")


WATCH_OUT_AFTER = frozenset("for out".split())
WATCHING = frozenset("watch watches watching watched".split())


def _watches_out_for(words, norm, end):
    return (words[-1:] and words[-1] in WATCHING
            and end < len(norm) and norm[end] in WATCH_OUT_AFTER)



def _says_nothing_here(topic, words, norm, start, study):
    if _watches_out_for(words, norm, start + len(words)):
        return True
    if topic == "family-and-parenting" and "health visitor" in " ".join(words):
        rest = " ".join(norm).replace("health visitor", " ").replace("health visitors", " ")
        for word in rest.split():
            if any(topic_ == "health" and weight >= 2 for topic_, weight in _lookup(word)):
                return True
    if len(words) == 1 and words[0] in BODY_CUES:
        return not _acts_on_the_body(norm, start)
    if any(word in VERB_CUES.get(topic, ()) for word in words):
        return _acts_on_a_thing(topic, words, norm, start) and not study
    return False


DRIVEN_PERSON = frozenset("me us him her them you u everyone everybody".split())
DRIVEN_MOOD = frozenset("""mad insane crazy nuts bonkers barmy potty daft distracted wild
    spare""".split())
DRIVEN_TAIL = frozenset("wall walls bend".split())
DRIVEN_JOINERS = frozenset("up round around over".split())
DRIVES = frozenset("drive drives driving drove driven".split())
AGE_NOUNS = frozenset("year years yr yrs month months mth mths week weeks wk wks".split())
AGE_IN_A_YEAR = {"year": 1, "years": 1, "yr": 1, "yrs": 1,
                 "month": 12, "months": 12, "mth": 12, "mths": 12,
                 "week": 52, "weeks": 52, "wk": 52, "wks": 52}
A_CHILD_TILL = 19
AGE_OF_A_CHILD_WORDS = frozenset("""baby babies child children kid kids toddler toddlers
    infant infants newborn boy girl son daughter grandchild lad lass""".split())
THE_PERSONS_OWN = frozenset("my our his her their".split())
AGE_AFTER = frozenset("is are was were be been about turned turns nearly almost just only".split())


def _age_value(word):
    value = WORD_NUMBERS.get(word)
    if value is None:
        digits = WORD_DIGITS.match(word)
        value = float(digits.group(0).replace(",", ".")) if digits else 99
    return value


def _ages_of_a_child(norm):
    ages = []
    for position, word in enumerate(norm):
        if word not in AGE_NOUNS or position == 0 or position + 1 >= len(norm):
            continue
        if norm[position + 1] != "old":
            continue
        number_at = position - 1
        if norm[number_at] in AGE_AFTER:
            continue
        if number_at == 0 or norm[number_at - 1] not in DETERMINERS:
            continue
        if _age_value(norm[number_at]) / AGE_IN_A_YEAR[word] > A_CHILD_TILL:
            continue
        ages.append(number_at)
    return ages


BOOK_WORDS = frozenset("book books novel novels".split())
A_CHILD_TO_READ_FOR = frozenset("""child children kid kids baby toddler boy girl son
    daughter niece nephew grandson granddaughter grandchild teenager teen""".split())


def _a_book_for_a_child(norm, child_ages):
    for position, word in enumerate(norm):
        if word not in BOOK_WORDS or norm[position + 1:position + 2] != ["for"]:
            continue
        after = position + 2
        tail = norm[after:after + 5]
        if set(tail) & A_CHILD_TO_READ_FOR:
            return position
        if any(after <= age <= after + 3 for age in child_ages):
            return position
        if "year" in tail and ("old" in tail or "olds" in tail):
            return position
    return None


def _drives_a_person(norm, position):
    if norm[position] not in DRIVES:
        return False
    if norm[position + 1:position + 2] != [] and norm[position + 1] not in DRIVEN_PERSON:
        return False
    if not norm[position + 1:position + 2]:
        return False
    tail = norm[position + 2:position + 7]
    return bool(set(tail) & DRIVEN_MOOD
                or (set(tail) & DRIVEN_TAIL and set(tail) & DRIVEN_JOINERS))


IDIOM_PHRASES = (
    ("run", "off", "my", "feet"), ("run", "off", "our", "feet"),
    ("run", "off", "your", "feet"), ("running", "off", "my", "feet"),
    ("rushed", "off", "my", "feet"), ("rushed", "off", "our", "feet"),
    ("pushed", "off", "my", "feet"), ("ran", "off", "my", "feet"),
    ("on", "my", "feet", "all", "day"), ("on", "our", "feet", "all", "day"),
    ("on", "my", "feet", "all", "week"), ("up", "on", "my", "feet"),
    ("run", "ragged"), ("running", "ragged"), ("ran", "ragged"),
    ("dead", "on", "my", "feet"), ("dead", "on", "her", "feet"),
    ("dead", "on", "his", "feet"), ("dead", "on", "their", "feet"),
    ("back", "on", "my", "feet"), ("back", "on", "his", "feet"),
    ("back", "on", "her", "feet"), ("back", "on", "its", "feet"),
    ("back", "on", "their", "feet"), ("back", "on", "our", "feet"),
    ("find", "my", "feet"), ("finding", "my", "feet"), ("found", "my", "feet"),
    ("two", "left", "feet"), ("swept", "off", "my", "feet"),
    ("swept", "me", "off", "my", "feet"),
    ("cold", "feet"), ("cold", "turkey"),
    ("snowed", "under"), ("snowed", "under", "with"), ("under", "the", "weather"),
    ("under", "my", "belt"), ("out", "of", "my", "depth"), ("out", "of", "our", "depth"),
    ("at", "my", "wits", "end"), ("at", "our", "wits", "end"), ("at", "wits", "end"),
    ("on", "the", "fence"), ("in", "two", "minds"), ("on", "the", "same", "page"),
    ("over", "the", "moon"), ("in", "the", "same", "boat"),
    ("doing", "my", "head", "in"), ("doing", "my", "nut", "in"),
    ("does", "my", "head", "in"), ("doing", "his", "head", "in"),
    ("doing", "her", "head", "in"), ("doing", "our", "head", "in"),
    ("a", "piece", "of", "cake"), ("piece", "of", "cake"), ("easy", "as", "pie"),
    ("spill", "the", "beans"), ("spilling", "the", "beans"), ("spilled", "the", "beans"),
    ("not", "my", "cup", "of", "tea"), ("my", "cup", "of", "tea"),
    ("the", "icing", "on", "the", "cake"), ("icing", "on", "the", "cake"),
    ("cherry", "on", "the", "cake"), ("half", "baked", "idea"),
    ("the", "last", "straw"), ("a", "storm", "in", "a", "teacup"),
    ("a", "pain", "in", "the", "neck"), ("a", "pain", "in", "the", "backside"),
    ("music", "to", "my", "ears"), ("a", "shot", "in", "the", "arm"),
    ("the", "tip", "of", "the", "iceberg"), ("a", "drop", "in", "the", "ocean"),
    ("a", "grey", "area"), ("off", "the", "rails"), ("off", "the", "boil"),
    ("on", "its", "last", "legs"), ("on", "their", "last", "legs"),
)


def _idiom_positions(norm):
    spots = set()
    joined = " " + " ".join(norm) + " "
    for phrase in IDIOM_PHRASES:
        needle = " " + " ".join(phrase) + " "
        start = 0
        while True:
            at = joined.find(needle, start)
            if at < 0:
                break
            spots.update(range(len(joined[:at].split()), len(joined[:at].split()) + len(phrase)))
            start = at + 1
    return spots


def _bad_verdict_positions(norm):
    return {position for position in range(len(norm)) if a_bad_verdict(norm, position)}


def _drive_idiom(norm):
    idiom = set()
    for position in range(len(norm)):
        if not _drives_a_person(norm, position):
            continue
        idiom.update((position, position + 1))
        for offset in range(position + 2, min(position + 7, len(norm))):
            if norm[offset] in DRIVEN_MOOD or norm[offset] in DRIVEN_TAIL \
                    or norm[offset] in DRIVEN_JOINERS:
                idiom.add(offset)
    return idiom



COMPLAINT_OF = frozenset("sick tired bored weary".split())
COMPLAINT_OF_NEXT = frozenset("of with about".split())


BODILY_OUTPUT = frozenset("""poo poos pooed pooing poop poops pooped pooping stool stools
    faeces feces turd turds bowels bowel""".split())
BODILY_OUTPUT_NOUN = BODILY_OUTPUT - frozenset("pooed pooped pooing pooping".split())
SAMPLE_WORDS = frozenset("""sample samples test tests tested testing kit pot container jar
    form forms""".split())


STOOL_AS_FURNITURE = frozenset("""wobbly wobble wobbles wobbliest rickety leg legs joint joints
    seat seats wood wooden screw screws screwdriver tighten tight creak creaks squeak squeaks
    bracket glue chair chairs table tables bench furniture dresser sideboard carpenter flatpack
    kitchen""".split())
ONLY_A_STOOL = frozenset("stool stools".split())


def _is_a_complaint(norm, position):
    if norm[position] not in COMPLAINT_OF:
        return False
    return position + 1 < len(norm) and norm[position + 1] in COMPLAINT_OF_NEXT


DERIVED_ENDINGS = ("ness", "ment", "tion", "sion", "ity", "ance", "ence", "ancy", "ency",
                   "ism", "ist", "ful", "less", "ing", "ers", "ant", "ent", "er", "ed",
                   "cy", "ic", "al", "ly", "th", "y", "s")
FAMILY_PAIRS = (("ant", "ancy"), ("ent", "ency"), ("ate", "ation"), ("ate", "acy"),
                ("ive", "ion"), ("ible", "ibility"), ("able", "ability"))
FAMILY_STEM = 5
FAMILY_WORD = 5

_FUNCTION_WORDS = None


def _function_words():
    global _FUNCTION_WORDS
    if _FUNCTION_WORDS is None:
        try:
            from . import STOPWORDS
            _FUNCTION_WORDS = frozenset(STOPWORDS)
        except Exception:
            _FUNCTION_WORDS = frozenset()
    return _FUNCTION_WORDS


def _family(word):
    for ending in DERIVED_ENDINGS:
        if word.endswith(ending):
            stem = word[:-len(ending)]
            if len(stem) >= FAMILY_STEM:
                hit = TABLE.get(stem) or TABLE.get(stem + "e")
                if hit:
                    return hit
        if len(word) >= FAMILY_WORD and word not in _function_words():
            hit = TABLE.get(word + ending)
            if hit:
                return hit
    for here, there in FAMILY_PAIRS:
        if word.endswith(here):
            hit = TABLE.get(word[:-len(here)] + there)
            if hit:
                return hit
        if word.endswith(there):
            hit = TABLE.get(word[:-len(there)] + here)
            if hit:
                return hit
    return ()


def _lookup(word):
    hit = TABLE.get(word)
    if hit:
        return hit
    for suffix, replacement in (("ies", "y"), ("es", ""), ("s", ""), ("ing", ""),
                                ("ing", "e"), ("ed", ""), ("ed", "e")):
        if word.endswith(suffix) and len(word) > len(suffix) + 2:
            hit = TABLE.get(word[:-len(suffix)] + replacement)
            if hit:
                return hit
    family = _family(word)
    if family:
        return tuple((topic, weight) for topic, weight in family if topic != "about-the-bot")
    return ()


def _is_a_portion(norm, position):
    if norm[position] not in PORTION_WORDS:
        return False
    after = norm[position + 1:position + 3]
    if not after:
        return False
    if after[0] in ("a", "an", "the"):
        if len(after) > 1 and after[1] in PORTION_UNITS:
            return False
        return True
    return after[0] == "of" and len(after) > 1 and after[1] in ("a", "an", "the")


def _the_weather_is_just_a_season(norm, text):
    spots = [at for at, word in enumerate(norm) if word in SEASONS]
    if not spots:
        return False
    if min(spots) <= 2:
        return False
    if any(norm[at - 1] in WEATHER_BEFORE for at in spots if at):
        return False
    if any(word in WEATHER_ITSELF for word in norm):
        return False
    if any(word not in SEASONS and topic == "nature-and-weather" and weight >= 2
           for word in norm for topic, weight in _lookup(word)):
        return False
    return not any(
        key in text and not set(key.split()) & SEASONS
        for key, entries in TABLE.items() if " " in key
        and any(topic == "nature-and-weather" for topic, _weight in entries))


def score_topics(line, inherited=None):
    norm = line["norm"]
    text = " " + line["norm_text"] + " "
    sums = _work_out_sums(norm)
    study = bool(set(norm) & STUDY_OBJECTS)
    background = background_positions(norm)
    found, own = {}, {}

    def note(topic, weight, position, polysemous):
        score, top, first = found.get(topic, (0, 0, position))
        found[topic] = (score + weight, max(top, weight), first)
        if not polysemous:
            own[topic] = True

    forms_of = {form for forms, _topic, _tiers in SENSE_PAIRS.values() for form in forms}
    idiom = _drive_idiom(norm) | _idiom_positions(norm) | _bad_verdict_positions(norm)
    child_ages = _ages_of_a_child(norm)
    for position, word in enumerate(norm):
        if position in sums or position in background or position in idiom:
            continue
        if _is_run_out(norm, position):
            continue
        if _is_a_complaint(norm, position):
            continue
        if word in PLACES and _names_a_person(norm, position):
            continue
        elsewhere = _means_something_else(norm, position)
        if word in WARMTH_WORDS and the_warmth_said(norm):
            elsewhere = True
        if word in forms_of and _the_sense_the_cues_name(norm, position, word):
            continue
        for topic, weight in _lookup(word):
            if elsewhere:
                continue
            if _says_nothing_here(topic, [word], norm, position, study):
                continue
            note(topic, weight, position,
                 word in POLY_FORMS or _is_a_portion(norm, position))
    for forms, sense_topic, tiers in SENSE_PAIRS.values():
        spots = [at for at, word in enumerate(norm) if word in forms_of and word in forms]
        if spots and _sense_cue(norm, spots, tiers):
            note(sense_topic, SENSE_WEIGHT, spots[0], False)
    family_score = found.get("family-and-parenting", (0, 0, 0))[0]
    if child_ages and (family_score >= 2 or not any(
            score >= 2 for topic, (score, _top, _first) in found.items()
            if topic not in ("family-and-parenting", "feelings"))):
        note("family-and-parenting", 2, child_ages[0], False)
    book_at = _a_book_for_a_child(norm, child_ages)
    if book_at is not None:
        note("entertainment", 3, book_at, False)
    if sums and not any(score >= 2 for score, _top, _first in found.values()):
        note("maths-and-numbers", 2, min(sums), False)
    output_at = _the_persons_own_output(norm)
    if output_at is not None:
        note("health", 2, output_at, False)
    stone_at = stone_weight_at(norm)
    if stone_at is not None:
        note("fitness", 3, stone_at, False)
    tight_at = tight_money_at(norm, line.get("text") or "")
    if tight_at is not None and not any(
            score >= 2 for topic, (score, _top, _first) in found.items() if topic != "money"):
        note("money", 3, tight_at, False)
    if sums and set(norm) & SUM_MONEY:
        note("money", 3, min(sums), False)
    named = {topic for word in norm if word not in ADDRESS_WORDS
             for topic, weight in _lookup(word)
             if weight >= 2 and topic != "small-talk"}
    for key, entries in TABLE.items():
        if " " not in key or key not in text:
            continue
        words = key.split()
        for start in range(len(norm) - len(words) + 1):
            if norm[start:start + len(words)] != words:
                continue
            if start in background:
                continue
            if sums and key == "work out":
                continue
            if named and all(topic == "small-talk" for topic, _weight in entries):
                continue
            for topic, weight in entries:
                if _says_nothing_here(topic, words, norm, start, study):
                    continue
                note(topic, weight, start, False)
            break
    text_norm = " " + " ".join(norm) + " "
    match = JUDGEMENT_OF_RECORD.search(text_norm)
    if match and not any(score >= 3 for score, _top, _first in found.values()):
        note("feelings", 3, text_norm[:match.start()].count(" "), False)
    unfit = reads_as_unfit(text_norm)
    if unfit is not None and not any(score >= 3 for score, _top, _first in found.values()):
        note("feelings", 3, text_norm[:unfit].count(" "), False)
    if _the_weather_is_just_a_season(norm, text) and any(
            other != "nature-and-weather" and score >= 2
            for other, (score, _top, _first) in found.items()):
        own.pop("nature-and-weather", None)
    for pattern, topic in CANCELS:
        if topic not in found:
            continue
        if not any(other != topic and score >= 2 for other, (score, _top, _first)
                   in found.items()):
            continue
        match = pattern.search(text_norm)
        if not match:
            continue
        after = text_norm[match.end():].strip().split()
        if after and after[0] not in CANCEL_AFTER and after[0] not in (".", ",", ";", ":",):
            continue
        score, top, first = found[topic]
        found[topic] = (max(0, score - 2), top, first)
    ranked = sorted(found.items(),
                    key=lambda item: (item[1][0], item[1][1], -item[1][2]), reverse=True)
    return [(topic, score if own.get(topic) else min(score, 1),
             top if own.get(topic) else min(top, 1))
            for topic, (score, top, _first) in ranked]


TWO_HOMES = frozenset("""
    tablet stock fish draughts tomato tomatoes basil virus team
""".split())


LIVES = {
    "tablet": (
        frozenset("""pill pills dose dosage swallow swallowed blister pack pharmacy
            prescription headache headachey painkiller painkillers ibuprofen paracetamol
            antibiotic antibiotics chemist gp food meal meals stomach empty water milk
            coffee breakfast with""".split()),
        frozenset("""screen screens battery charge charging charger charged app apps keypad
            keyboard wifi update downloading cracked ipad android""".split()),
    ),
    "stock": (
        frozenset("""cube cubes gravy soup broth pot saucepan freezer shelf cupboard kitchen
            chicken vegetable vegetables veg boil simmer bone bones""".split()),
        frozenset("""shares share market markets invest investing investment portfolio dividend
            dividends trading trader isa pension ftse broker buy sell buying selling worth
            price prices""".split()),
    ),
    "fish": (
        frozenset("""dinner tea supper lunch cook cooked frying fried grill grilled baked
            fillet fillets bones chips salmon tuna cod haddock mackerel monger fingers rice
            lemon batter""".split()),
        frozenset("""tank tanks pond pond bowl aquarium goldfish swim swimming died dying filter
            feeder feeding feed water""".split()),
    ),
    "draughts": (
        frozenset("""board pieces checkers play playing game games opponent win won lose""".split()),
        frozenset("""door doors window windows draught gap gaps under cold blow blowing seal""".split()),
    ),
    "tomato": (
        frozenset("""sauce sauces salad ketchup slice sliced soup tinned canned ripe puree
            passata sandwich make making cook cooking dinner meal""".split()),
        frozenset("""plant plants grow growing grew seed seeds seedling seedlings garden
            greenhouse blight water watering stake""".split()),
    ),
    "basil": (
        frozenset("""pesto pasta sauce leaves leaf fresh cook cooked make making recipe salad
            sprinkle dish dinner meal pizza""".split()),
        frozenset("""plant plants grow growing grew died dying wilted wilt pot soil water
            watering repot seed seeds""".split()),
    ),
    "virus": (
        frozenset("""laptop computer pc file files email software antivirus malware download
            downloaded popup popups password browser update""".split()),
        frozenset("""cold flu round caught fever cough symptoms sick ill bug bugs tummy
            throwing headache""".split()),
    ),
    "team": (
        frozenset("""rota shift shifts manager boss job work project colleagues colleague
            meeting employer office""".split()),
        frozenset("""match game win won lost lose score scored goal goals player players coach
            league season fans football rugby cricket kit""".split()),
    ),
}
LIVES["tomatoes"] = LIVES["tomato"]


def unsure_words(norm, topic):
    if not topic:
        return []
    words = set(norm)
    in_doubt = []
    for word in words:
        if word not in TWO_HOMES:
            continue
        if any(words & home for home in LIVES.get(word, ())):
            continue
        in_doubt.append(word)
    return sorted(in_doubt)


PLACE_OVER = 2


def _place_points(line, entities, scores, asks=None):
    words = set(line["norm"])
    if words & TRAVEL_STRONG:
        return 4
    if any(item["type"] == "person" for item in entities):
        return 0
    others = [score for topic, score in scores.items()
              if topic not in ("geography-and-travel", "small-talk")]
    if others and max(others) >= PLACE_OVER:
        return 0
    asked = _looks_like_an_ask(line) if asks is None else asks
    return 3 if asked else 0


TRAVEL_STRONG = frozenset("""trip trips holiday holidays flight flights fly flying flew
    visit visiting visited travel travelling traveling travelled traveled abroad hotel hotels
    booking itinerary sightseeing tourist tourists weekend weekends break honeymoon
    going drove driving ride staying""".split())

ASK_WORDS = frozenset("""what how where when why which who whom whose can could should would
    will shall do does did is are was were am any anyone something tell give suggest
    recommend show me""".split())


WANT_VERBS = frozenset("""want wants wanted wanting need needs needed fancies fancy
    fancied fancies""".split())
A_THING_WANTED = frozenset("a an the some another new more".split())
WANTED_BEFORE_A_STOP = frozenset("""for to of at with and but so because when if
    about by from in on""".split())
A_PERSON_WHO_WANTS = frozenset("""wife husband mrs missus partner son daughter kid kids
    child children baby teenager mum mom mother dad father brother sister mate mates friend
    friends boyfriend girlfriend fella bloke lad lass nan nana granny grandad""".split())


def _what_someone_else_wants(norm):
    for at, word in enumerate(norm):
        if word not in WANT_VERBS:
            continue
        if not A_PERSON_WHO_WANTS & set(norm[max(0, at - 3):at]):
            continue
        for spot in range(at + 1, min(len(norm), at + 5)):
            if norm[spot] in WANTED_BEFORE_A_STOP:
                break
            if norm[spot] not in A_THING_WANTED:
                continue
            for candidate in norm[spot + 1:min(len(norm), spot + 5)]:
                if candidate in A_THING_WANTED:
                    continue
                topics = [topic for topic, weight in _lookup(candidate)
                          if topic not in PEOPLE_TOPICS and topic != "small-talk" and weight >= 2]
                if topics:
                    return topics[0], spot + 1
            break
    return None


def _looks_like_an_ask(line):
    text = line.get("text") or ""
    norm = line["norm"]
    if "?" in text or not norm:
        return True
    return norm[0] in ASK_WORDS


FRIEND_WORDS = frozenset("""mate mates pal pals buddy buddies bloke fella
    flatmate flatmates housemate housemates""".split())
OWNED_BY = frozenset("my your his her our their me".split())
FRIEND_BOOST = 1


def _names_a_friend_of_their_own(norm):
    return any(word in FRIEND_WORDS and before in OWNED_BY
               for before, word in zip(norm, norm[1:]))


def _the_persons_own_output(norm):
    if not set(norm) & BODILY_OUTPUT or set(norm) & SAMPLE_WORDS:
        return None
    words = set(norm)
    if words & ONLY_A_STOOL and not words & (BODILY_OUTPUT - ONLY_A_STOOL):
        if words & STOOL_AS_FURNITURE:
            return None
        if not A_GUT_ONLY.search(" ".join(norm)):
            return None
    if set(norm) & ANIMALS:
        return None
    if set(norm) & PETS:
        return None
    words = set(norm)
    person = bool(words & (_person_words() - PETS - ANIMALS))
    for at, word in enumerate(norm):
        if word not in BODILY_OUTPUT:
            continue
        if word in BODILY_OUTPUT_NOUN:
            if at and norm[at - 1] in OWNERS:
                return at
            continue
        if person or words & frozenset("i im ive we weve".split()):
            return at
    return None


def own_output_word(norm):
    return _the_persons_own_output(norm)


def _owns_an_animal(norm):
    return any(word in OWNERS and norm[at + 1] in ANIMALS
               for at, word in enumerate(norm[:-1]))


def _a_crop_is_failing(norm):
    words = set(norm)
    if words & CROP_KITCHEN:
        return False
    text = " ".join(norm)
    if not any(state in text for state in CROP_STATES):
        return False
    if words & GROWING_PLACES:
        return True
    for at, word in enumerate(norm[:-1]):
        if word in OWNERS and norm[at + 1] in CROPS:
            return True
    return False


def _asks_mechanism(norm):
    if not norm or norm[0] not in MECHANISM:
        return False
    if norm[0] == "how":
        return len(norm) > 1 and norm[1] in MECHANISM_HOW
    return True


def _sign_said_of_a_person(norm, words):
    text = " ".join(norm)
    if any(phrase in text for phrase in UNWELL_IDIOMS):
        return False
    for at, word in enumerate(norm):
        after = norm[at + 1] if at + 1 < len(norm) else ""
        before = norm[at - 1] if at else ""
        if word in UNWELL_SIGNS:
            if after in BEHAVIOUR or after in SIGN_NOT_AFTER:
                continue
            if word in NOUNY_SIGNS and after and after not in SIGN_FOLLOWS and not after.isdigit():
                continue
            if word == "broke" and not words & BODY:
                continue
            return True
        if before == "not" and word in UNWELL_NOT:
            if word != "responding":
                return True
            for ahead in norm[at + 1:at + 4]:
                if ahead in COMMS:
                    return False
                if ahead in HEARERS:
                    return True
            return True
    return False


NOSE_BLOCKED = re.compile(
    r"\b(?:im|i am|i feel|im feeling|i am feeling|i feel like i am)\b"
    r"(?:\s+(?:all|really|so|very|a\s+bit|a\s+little|totally|properly|quite|that|bit|"
    r"still|now|again|bit)){0,3}\s+"
    r"(?:stuffy|stuffed\s+up|bunged\s+up|blocked\s+up|congested|congestion|clogged\s+up)\b"
    r"|\b(?:im|ive|i've|i\s+have|i\s+keep)\b"
    r"(?:(?!\b(?:dog|cat|puppy|kitten|baby|kid|boy|girl)\b)[^.!?]){0,18}?"
    r"\b(?:sniffly|sniffles|sniffling|sniffing|snotty)\b"
    r"|\bmy\s+(?:head|nose|sinuses?|nose\s+passages?|face)\b"
    r"(?:\s+(?:is|are|feels?|feeling|gets?|keeps?|has\s+been)){0,2}"
    r"(?:\s+(?:all|really|so|very|a\s+bit|a\s+little|totally|quite|still|now|again|bit)){0,3}"
    r"\s+(?:stuffy|stuffed\s+up|bunged\s+up|blocked\s+up|blocked|congested|congestion)\b")
NOSE_BLOCKED_BOOST = 6


def _a_person_is_unwell(norm, words):
    if not words & UNWELL_SIGNS and not ("not" in words and words & UNWELL_NOT):
        return False
    if not any(word in THE_PEOPLE for word in norm):
        return False
    return _sign_said_of_a_person(norm, words)

MONEY_TIGHT = ("skint", "brassic", "till payday", "until payday", "money is tight",
               "tight month", "on the breadline", "no money till", "no money until",
               "no money left", "no money", "running out of money", "a bit short this month",
               "short this month", "short till payday",
               "short till", "short this week",
               "nothing till", "nothing until", "nowt till", "nowt until",
               "cleaned out", "not got a penny", "penny to my name")
MONEY_TIGHT_MAX = 10

BROKE_AS_SUBJECT = frozenset("""i im am we are he she hes shes they theyre you youre u is
    was were been be being totally completely so officially proper flat dead stone absolutely
    very pretty quite really just still honestly yeah ok okay and but now""".split())
BROKE_AS_TIME = frozenset("""till until by for this week month payday weekend end today
    tomorrow again now already friday monday tuesday wednesday thursday saturday sunday and but
    so or time yet though honestly lol ha thanks anyway right now""".split())


def broke_at(norm):
    for at, word in enumerate(norm):
        if word != "broke":
            continue
        if any(before not in BROKE_AS_SUBJECT for before in norm[:at]):
            continue
        if any(after not in BROKE_AS_TIME for after in norm[at + 1:]):
            continue
        return at
    return None


A_MONEY_WORD = frozenset("quid pound pounds tenner tenners fiver fivers bucks".split())
A_AMOUNT_NOUN = {"tenner": 10, "tenners": 10, "fiver": 5, "fivers": 5}
A_AMOUNT_SYMBOL = re.compile(r"£\s*(\d+(?:[.,]\d+)?)|(?<![\w.])(\d{1,4})\s*p\b")
A_WAIT = frozenset("till until til".split())
A_WAIT_TO = frozenset("""payday friday saturday sunday monday tuesday wednesday thursday week
    weekend month end tomorrow today next""".split())
BIG_PURSE = 500


def _purse_amount(norm, at):
    amount = norm[at - 1]
    if amount.replace(".", "").isdigit():
        return float(amount)
    value = WORD_NUMBERS.get(amount)
    if value is None:
        return None
    if amount in ("hundred", "thousand") and at >= 2:
        before = WORD_NUMBERS.get(norm[at - 2])
        if before is not None:
            return before * value
    return value


def _a_wait_follows(words):
    for spot, word in enumerate(words[:3]):
        if word not in A_WAIT:
            continue
        rest = [one for one in words[spot + 1:spot + 3] if one not in ("the", "a", "i")]
        if rest and rest[0] in A_WAIT_TO:
            return True
    return False


def purse_till_at(norm, text=""):
    for at, word in enumerate(norm):
        if at == 0:
            continue
        if word in A_AMOUNT_NOUN:
            if _a_wait_follows(norm[at + 1:]):
                return at - 1
            continue
        if word not in A_MONEY_WORD:
            continue
        amount = norm[at - 1]
        if amount not in NUMBER_WORDS and not amount.replace(".", "").isdigit():
            continue
        if (_purse_amount(norm, at) or 0) >= BIG_PURSE:
            continue
        if _a_wait_follows(norm[at + 1:]):
            return at - 1
    if text:
        for match in A_AMOUNT_SYMBOL.finditer(text.lower()):
            pounds, pence = match.group(1), match.group(2)
            value = float(pounds.replace(",", "")) if pounds else float(pence) / 100.0
            if value >= BIG_PURSE:
                continue
            after = re.findall(r"[a-z']+", text[match.end():].lower())
            if _a_wait_follows(after):
                return 0
    return None


def tight_money_at(norm, text=""):
    joined = " " + " ".join(norm) + " "
    at = broke_at(norm)
    purse = purse_till_at(norm, text)
    if purse is not None:
        at = purse if at is None else min(at, purse)
    for phrase in MONEY_TIGHT:
        spot = joined.find(" " + phrase + " ")
        if spot < 0:
            continue
        index = len(joined[:spot].split())
        at = index if at is None else min(at, index)
    if at is None:
        return None
    for word in norm:
        for topic, weight in _lookup(word):
            if weight >= 2 and topic not in ("money", "small-talk"):
                return None
    return at


STONE_VERBS = frozenset("""lose loses losing lost loss shed sheds shedding gained gain
    gains gaining weighed weigh weighs weigh-in diet dieting slimming slimmer""".split())
STONE_COMPOUNDS = ("put on", "piling on", "piled on")


def stone_weight_at(norm):
    spots = [at for at, word in enumerate(norm) if word in ("stone", "stones")]
    if not spots:
        return None
    joined = " ".join(norm)
    cues = {at for at, word in enumerate(norm) if word in STONE_VERBS}
    for phrase in STONE_COMPOUNDS:
        start = 0
        while True:
            spot = joined.find(phrase, start)
            if spot < 0:
                break
            cues.add(len(joined[:spot].split()))
            start = spot + 1
    for at in spots:
        if any(abs(at - cue) <= 4 for cue in cues):
            return at
    return None


def tight_on_money(norm, kind=None, text=""):
    if kind == "question" or not norm or len(norm) > MONEY_TIGHT_MAX:
        return False
    return tight_money_at(norm, text) is not None



WORN_OUT = frozenset("shattered whacked zonked pooped bushed fagged drained wrecked frazzled".split())
WORN_OUT_SAID = ("wiped out", "done in", "worn out", "cream crackered", "wiped")
WORN_OUT_CUE = frozenset("im am feel feeling".split())
WORN_OUT_LOOKBACK = 3
WORN_OUT_BOOST = 4


def _worn_out(norm):
    if not norm:
        return False
    for at, word in enumerate(norm):
        if word in WORN_OUT and any(item in WORN_OUT_CUE
                                     for item in norm[max(0, at - WORN_OUT_LOOKBACK):at]):
            return True
    joined = " " + " ".join(norm) + " "
    for phrase in WORN_OUT_SAID:
        spot = joined.find(" " + phrase + " ")
        if spot < 0:
            continue
        back = joined[:spot].split()[-WORN_OUT_LOOKBACK:]
        if any(item in WORN_OUT_CUE for item in back):
            return True
    return False


def rank_topics(line, inherited=None, entities=None, asks=None):
    found = {topic: [score, top] for topic, score, top in score_topics(line)}

    def boost(topic, points):
        entry = found.setdefault(topic, [0, 0])
        entry[0] += points
        entry[1] = max(entry[1], points)

    words = set(line["norm"])
    if entities and any(item["type"] == "place" for item in entities):
        points = _place_points(line, entities,
                               {topic: score for topic, (score, _top) in found.items()},
                               asks)
        if points:
            boost("geography-and-travel", points)
    if entities and any(_a_country_named(item) for item in entities):
        boost("geography-and-travel", COUNTRY_BOOST)
    if entities and any(item["text"].lower().split()[-1] in PETS for item in entities):
        boost("pets", PET_BOOST)
    words = set(line["norm"])
    reason = reason_positions(line["norm"])
    if set(word for position, word in enumerate(line["norm"]) if position not in reason) & BODY \
            and set(word for position, word in enumerate(line["norm"]) if position not in reason) & HURTS:
        boost("health", HURT_BOOST)
    if _head_fog(line["norm"]):
        boost("health", HEAD_FOG_BOOST)
    if _skin_state(line["norm"], reason) is not None and not any(
            found.get(topic, [0])[0] >= 2 for topic in PEOPLE_TOPICS):
        boost("health", SKIN_BOOST)
    if _named_condition(line["norm"], words, reason):
        boost("health", CONDITION_BOOST)
    if _a_part_plays_up(line["norm"], reason) is not None:
        boost("health", PART_UP_BOOST)
    warmth = the_warmth_said(line["norm"])
    sign_words = ([word for word in line["norm"] if word != warmth] if warmth else line["norm"])
    if _a_person_is_unwell(sign_words, set(sign_words)):
        boost("health", UNWELL_BOOST)
    if NOSE_BLOCKED.search(" " + " ".join(line["norm"]) + " "):
        boost("health", NOSE_BLOCKED_BOOST)
    animals = _owns_an_animal(line["norm"])
    if animals:
        boost("pets", PET_BOOST)
    if _names_a_friend_of_their_own(line["norm"]):
        boost("friends-and-relationships", FRIEND_BOOST)
    wanted = _what_someone_else_wants(line["norm"])
    if wanted is not None and any(found.get(topic, [0])[0] >= 2 for topic in PEOPLE_TOPICS):
        topic, at = wanted
        boost(topic, max(found.get(topic, [0])[0], 2) + 1)
    if _a_crop_is_failing(line["norm"]):
        boost("garden-and-plants", CROP_BOOST)
    if _a_habit_given_up(line["norm"]):
        boost("food-and-drink", GIVING_UP_BOOST)

    if _worn_out(line["norm"]) and not _asks_back(line["norm"]):
        boost("sleep", WORN_OUT_BOOST)
    if (words & WORLD and not words & WORLD_NOT and not words & NATURE_WORDS
            and not words & HURTS and not animals and _asks_mechanism(line["norm"])):
        boost("science", SCIENCE_BOOST)
    for number in detect_numbers(line):
        if number["unit"] == "percent":
            boost("maths-and-numbers", 3)
    if _gift_ask(words, line["norm"]):
        boost("shopping", GIFT_BOOST)
    if (found.get("health", [0])[0] >= 3
            and {topic for topic, entry in found.items()
                 if entry[0] >= 2} <= {"health", "small-talk"}):
        found.pop("small-talk", None)
    if inherited:
        for topic, entry in found.items():
            if topic != inherited and entry[1] < 2:
                entry[0] -= 1
        boost(inherited, CARRY)
    scores = {topic: score for topic, (score, _top) in found.items()}
    if _the_weather_is_just_a_season(line["norm"], " " + line["norm_text"] + " "):
        entry = scores.get("nature-and-weather")
        if entry is not None and any(
                other != "nature-and-weather" and score >= 2
                for other, score in scores.items()):
            scores["nature-and-weather"] = min(entry, 1)
    ranked = [(topic, score) for topic, score in scores.items() if score >= 2]
    ranked.sort(key=lambda item: (item[1], item[0] == inherited), reverse=True)
    return ranked


def gift_ask(understood):
    if not isinstance(understood, dict):
        return False
    norm = understood.get("norm")
    if not isinstance(norm, (list, tuple)) or not norm:
        return False
    return _gift_ask(set(norm), list(norm))


def _gift_ask(words, norm):
    if words & GIFT_ALWAYS:
        return True
    if words & GIFT_WORDS and (words & GIFT_ASKING or words & GIVE_VERB
                               or words & GIFT_OCCASION or "for" in words):
        return True
    if words & GIFT_WANTING and _gift_still_to_get(words, norm):
        return True
    if not (words & GIFT_ASKING or words & GIFT_OCCASION):
        return False
    if words & GIFT_OCCASION:
        for position, word in enumerate(norm[:-1]):
            if word in GIVE_TO and set(norm[position + 1:position + 3]) & GIVE_THINGS:
                return True
    for position, word in enumerate(norm):
        if word not in GIVE_VERB:
            continue
        rest = norm[position + 1:]
        if not rest:
            continue
        head = rest[0]
        if head in GIVE_THING or head in GIFT_WORDS or head in GIFT_OCCASION:
            return True
        tail = rest
        for index, one in enumerate(rest[:2]):
            if one in GIVE_TO or (one in GIVE_DETERMINERS and rest[index + 1:index + 2]
                                  and rest[index + 1] in GIVE_TO):
                tail = rest[index + 1:] if one in GIVE_TO else rest[index + 2:]
                break
        else:
            continue
        if not tail or tail[0] in GIVE_RELATIVE:
            return True
        if [one for one in tail[:3] if one in GIFTS_OR_OCCASIONS]:
            return True
        if tail[0] == "for" and any(ch.isdigit() for one in tail[1:4] for ch in one):
            return True
    return False


def _gift_still_to_get(words, norm):
    if words & GIVE_TO and "for" in words and words & {"nothing", "anything"}:
        return True
    for position, word in enumerate(norm):
        if word not in GIVE_VERB:
            continue
        rest = norm[position + 1:]
        for index, one in enumerate(rest[:2]):
            if one in GIVE_TO:
                tail = rest[index + 1:]
                break
            if (one in GIVE_DETERMINERS and rest[index + 1:index + 2]
                    and rest[index + 1] in GIVE_TO):
                tail = rest[index + 2:]
                break
        else:
            continue
        if not tail:
            continue
        if tail[0] in GIVE_THING or tail[0] in GIFT_WORDS:
            return True
        if "for" in tail and words & {"nothing", "anything"}:
            return True
        if [one for one in tail[:3] if one in GIFT_OCCASION]:
            return True
    return False


def subject_topic(line, entities=None):
    for topic, _score, top in score_topics(line):
        if top >= 2:
            return topic
    return None


def the_words_that_said(line, topic, entities=None):
    if not isinstance(topic, str) or not topic:
        return []
    norm = list(line.get("norm") or ())
    found, covered = [], set()
    for size in range(2, 5):
        for start in range(len(norm) - size + 1):
            key = " ".join(norm[start:start + size])
            for name, weight in TABLE.get(key, ()):
                if name == topic:
                    found.append((key, weight))
                    covered.update(norm[start:start + size])
    for position, word in enumerate(norm):
        if word in covered:
            continue
        for name, weight in _lookup(word):
            if name == topic:
                found.append((word, weight))
    found.sort(key=lambda item: (-item[1], item[0]))
    return found


def detect_topic(line, inherited=None, entities=None, asks=None):
    ranked = rank_topics(line, inherited, entities, asks)
    if ranked:
        return ranked[0]
    return (inherited, 0) if inherited else (None, 0)


def _is_name(word):
    lower = word.lower()
    if lower in COMMON_WORDS and lower != "i":
        return False
    stem = lower.split("'")[0]
    if stem != lower and (stem in lexicon.CORE_WORDS
                          or (stem.endswith("n") and stem[:-1] in lexicon.CORE_WORDS)):
        return False
    return lower not in lexicon.CHAT or lower == "i"


NAME_BREAKS = frozenset("""a an the and or but if then than that this these those there here
    i me my we our us you your he him his she her they them their it its am is are was were be
    been being do does did have has had will would shall should can could may might must not no
    so too very just really quite only also as at by for from in into of off on onto out over
    under up with within without about after again against all any both each few more most other
    some such own same what which who whom whose when where why how""".split())
LEADING = frozenset("""i i'm im i've ive i'll ill i'd id we we're we've you you're
    he he's she she's it it's they they're""".split())


def _capitalised(text):
    runs, current = [], []
    for token in text.split():
        bare = token.strip(".,!?;:\"'()[]")
        if bare[:1].isupper() and bare.replace("-", "").replace("'", "").isalpha():
            current.append(bare)
        else:
            if current:
                runs.append(current)
                current = []
    if current:
        runs.append(current)
    names = []
    for run in runs:
        if len(run) == 1:
            if _is_name(run[0]):
                names.append(run[0])
            continue
        if run[0].lower() in ARTICLES or run[0].lower() in LEADING:
            run = run[1:]
        if not run:
            continue
        start = next((at for at, word in enumerate(run)
                      if _is_name(word) or word.lower() in PLACES), None)
        if start is None:
            continue
        part = []
        for word in run[start:]:
            if word.lower() in NAME_BREAKS:
                break
            part.append(word)
        if part:
            names.append(" ".join(part))
    return names


def detect_entities(line, text=None):
    text = line["text"] if text is None else text
    if small_talk_only(line["norm"]):
        return []
    entities, seen = [], set()

    def add(name, kind, at=None):
        key = name.lower()
        if key and key not in seen and len(key) > 1:
            seen.add(key)
            entities.append({"text": name.strip(), "type": kind,
                             "at": _position(line, key) if at is None else at})

    for match in re.finditer(r"\*([^*]{2,60})\*|\"([^\"]{2,60})\"", text):
        add(match.group(1) or match.group(2), "title")
    for person in re.finditer(r"\bmy ([a-z]+(?:\s+[a-z]+)?)", line["clean"]):
        word = person.group(1).split()[0]
        if word in RELATIONS:
            add("my " + word, "person")
            seen.add(word)
    for at in _ages_of_a_child(line["norm"]):
        after = line["norm"][at + 3] if at + 3 < len(line["norm"]) else ""
        if line["norm"][at - 1] not in THE_PERSONS_OWN:
            continue
        if after and after not in AGE_OF_A_CHILD_WORDS and (after in PETS or _thing(after)):
            continue
        add(" ".join(line["norm"][at - 1:at + 3]), "person", at=at - 1)
    for run in _capitalised(text):
        if run.lower() in {"i", "i'm", "im"}:
            continue
        first_word = run.lower().split()[0]
        kind = "place" if run.lower() in PLACES or first_word in PLACES else "name"
        if kind == "name" and _said_as_a_place(run, line["norm"]):
            kind = "place"
        add(run, kind)
    verdicts = _bad_verdict_positions(line["norm"])
    for index, word in enumerate(line["norm"]):
        if index in verdicts:
            continue
        asked = _asked_as_a_country(line["norm"], index)
        if word in PLACES and _names_a_person(line["norm"], index):
            continue
        if word in PLACES and (_names_a_place(word, text, asked)
                               or _placed_by_a_word(line["norm"], index)):
            add(word, "place")
            continue
        if word in RELATIONS:
            if (index and word not in line["clean"].split()
                    and line["norm"][index - 1] in OWNERS):
                add(line["norm"][index - 1] + " " + word, "person", at=index - 1)
                seen.add(word)
                continue
            add(word, "person")
            continue
        thing = _thing(word)
        if thing:
            add(thing, "thing")
    entities.sort(key=lambda entity: entity["at"])
    return entities


PLACE_WORDS = frozenset("""in at from near around across through visit visiting visited
    outside inside via""".split())
PLACE_WORDS_WITH_CUE = frozenset("""to towards toward""".split())

NOT_PLACES = frozenset("""excel word powerpoint outlook onenote slack zoom teams skype discord
    facebook instagram twitter whatsapp tiktok youtube netflix spotify amazon ebay etsy google
    gmail github gitlab python javascript chrome safari windows android iphone ipad mac
    photoshop canva notion trello jira dropbox onedrive icloud uber airbnb booking expedia
    linkedin paypal ebay tinder
drive docs sheets slides mail calendar
tesco sainsbury asda aldi lidl waitrose morrisons coop boots argos ikea currys""".split())
WORK_WORDS = frozenset("""work works working worked workplace office job jobs shift shifts
    employer company meeting meetings boss manager team interview roster rota colleagues""".split())


def _said_as_a_place(run, norm):
    first = run.split()[0].lower().strip(".,!?;:\"'()[]")
    if first in NOT_PLACES:
        return False
    for index, word in enumerate(norm):
        if word != first:
            continue
        if _places_a_name(norm, index):
            return True
        if index >= 2 and norm[index - 1] in PLACE_THING and norm[index - 2] in PLACE_WORDS:
            if norm[index - 2] == "at" and set(norm) & WORK_WORDS:
                return False
            return True
        return False
    return False


PLACE_THING = frozenset("the a an my your his her our their this that some any another".split())


def _placed_by_a_word(norm, index):
    return _places_a_name(norm, index)


def _has_travel_word(norm):
    words = set(norm)
    if words & TRAVEL_CUES:
        return True
    return any(word[:-1] in TRAVEL_CUES for word in words if word.endswith("s"))


def _places_a_name(norm, index):
    if index < 1 or index >= len(norm):
        return False
    before = norm[index - 1]
    if before in PLACE_WORDS_WITH_CUE:
        return _has_travel_word(norm)
    if before not in PLACE_WORDS:
        return False
    if before == "at" and set(norm) & WORK_WORDS:
        return False
    return True


PLACE_HOMOGRAPHS = frozenset("""turkey china brazil bath reading new""".split())
COUNTRY_HOMOGRAPHS = frozenset("""turkey china brazil""".split())

COUNTRY_CUES = frozenset("""hot warm cold sunny rainy weather temperature safe dangerous
    expensive cheap currency capital visa language speak driving flights flight hotel hotels
    resort beaches beach coast airport north south east west trip holiday visit visiting
    travel travelling traveling season best part parts city cities region regions
    january february march april may june july august september october november
    december""".split())
COMPARE_WORDS = frozenset("or and vs versus compared than".split())
ARTICLES = frozenset("the a an my our your his her their this that these those some any".split())


def _a_country_named(entity):
    if not isinstance(entity, dict) or entity.get("type") != "place":
        return False
    text = entity.get("text") or ""
    words = text.lower().split()
    return bool(words) and words[-1] in PLACE_HOMOGRAPHS


def _set_in_a_place(norm, index):
    if index + 2 < len(norm) and norm[index + 1] == "in" and norm[index + 2] in PLACES \
            and norm[index + 2] not in PLACE_HOMOGRAPHS:
        return True
    for near in range(max(0, index - 3), min(len(norm), index + 4)):
        if near != index and norm[near] in PLACES and norm[near] not in PLACE_HOMOGRAPHS:
            between = norm[min(index, near):max(index, near)]
            if any(word in COMPARE_WORDS for word in between):
                return True
    return False


def _asked_as_a_country(norm, index):
    if index and norm[index - 1] in ARTICLES:
        return False
    if set(norm) & COUNTRY_CUES:
        return True
    if _set_in_a_place(norm, index):
        return True
    for near in range(max(0, index - 2), min(len(norm), index + 3)):
        if near != index and norm[near] in PLACES and norm[near] not in PLACE_HOMOGRAPHS:
            between = norm[min(index, near):max(index, near)]
            if any(word in COMPARE_WORDS for word in between):
                return True
    return False


NAME_FRAMES = frozenset("called named call calls".split())


def _names_a_person(norm, index):
    before = norm[index - 1] if index else ""
    if before in PERSON_WORDS or before in NAME_FRAMES:
        return True
    return (index + 3 < len(norm) and norm[index + 1] == "is" and norm[index + 2] == "my"
            and norm[index + 3] in PERSON_WORDS)


def person_names(line):
    norm = line["norm"]
    seen, names = set(), []
    for index, word in enumerate(norm):
        if word in PLACES and word not in seen and _names_a_person(norm, index):
            seen.add(word)
            names.append(word)
    return names


def _names_a_place(word, text, asked=False):
    if word not in PLACE_HOMOGRAPHS:
        return True
    if asked and word in COUNTRY_HOMOGRAPHS:
        return True
    return re.search(r"\b%s\b" % word.capitalize(), text) is not None


def _position(line, name):
    first = name.split()[0]
    for index, word in enumerate(line["norm"]):
        if word == first or word.startswith(first):
            return index
    return len(line["norm"])


def _thing(word):
    if word in THINGS:
        return word
    if len(word) <= 3:
        return None
    for candidate in (word.rstrip("s"), word[:-2] if word.endswith("es") else None,
                      word[:-3] if word.endswith("ies") else None):
        if candidate and candidate in THINGS:
            return word
    return None


WORD_DIGITS = re.compile(r"[0-9]+(?:[.,][0-9]+)?")

_STEPPED_RELATIONS = ("mum", "mom", "mother", "dad", "father", "son", "daughter", "brother",
                      "sister")
_GRAND_RELATIONS = ("mum", "mom", "mother", "dad", "father", "son", "daughter", "child")
_KIN_BUILT = tuple(["step" + word for word in _STEPPED_RELATIONS]
                   + ["grand" + word for word in _GRAND_RELATIONS])

RELATIONS = frozenset("""
son daughter kid kids child children baby toddler mum mom mother dad father husband wife
partner boyfriend girlfriend friend friends boss manager colleague brother sister aunt
uncle cousin gran grandma grandad grandpa grandmother grandfather neighbour neighbour
landlord flatmate housemate boss team pet dog cat puppy kitten
ex exes
""".split()) | frozenset(_KIN_BUILT) | frozenset(("gran", "granddad", "granny"))

PERSON_WORDS = RELATIONS | frozenset("""mate mates nan nana granny auntie pal lad lass fella
    bloke guy missus fiance fiancee stepson stepdaughter""".split())
THE_PEOPLE = _person_words()


def _spoken_numbers(norm):
    values = set()
    for word in norm:
        value = WORD_NUMBERS.get(word)
        if value is not None:
            values.add(value)
            continue
        digits = WORD_DIGITS.match(word)
        if digits:
            try:
                value = float(digits.group(0).replace(",", "."))
            except ValueError:
                continue
            values.add(int(value) if value.is_integer() else value)
    return values


NUMBER_FILLER = frozenset("a an of".split())

A_PORTION_UNITS = frozenset("""g gram grams gramme grammes kg kilo kilos kilogram kilograms
lb lbs pound pounds oz ounce ounces ml millilitre millilitres milliliter milliliters
l litre litres liter liters tsp teaspoon teaspoons tbsp tablespoon tablespoons cup cups
mile miles km kilometre kilometres kilometer kilometers metre metres meter meters
foot feet ft inch inches""".split())
OWNS_THE_UNIT = frozenset(WORD_NUMBERS) | {"quarter", "quarters", "third", "thirds"}
A_PORTION_NEEDS_OF = frozenset({"pound", "pounds", "lb", "lbs"})


def _mixed_number(norm, position, value):
    words = tuple(norm[position + 1:position + 4])
    if not words or words[0] != "and":
        return value, ()
    step = 2 if words[1:2] in (("a",), ("an",)) else 1
    fraction = words[step] if len(words) > step else None
    if fraction not in ("half", "quarter"):
        return value, ()
    return (value + (0.5 if fraction == "half" else 0.25),
            tuple(range(position + 1, position + 1 + step + 1)))


def _the_figure_and_its_unit(digits, unit, raw=""):
    if not unit:
        return digits
    if unit == "%":
        return digits + "%"
    if unit in UNIT_WORDS or unit in CLIPPED_UNIT_WORDS or unit in FIGURE_SIZE_WORDS:
        gap = " " if str(raw)[len(digits):len(digits) + 1].isspace() else ""
        return digits + gap + unit
    return digits


def detect_numbers(line):
    out, seen, typed, merged = [], set(), [], set()
    norm = line["norm"]
    spoken = _spoken_numbers(norm)
    for match in NUMBER_RE.finditer(line["clean"]):
        raw = match.group(0).strip()
        digits, unit = match.group(1), (match.group(2) or "").lower()
        try:
            value = float(digits.replace(",", "."))
        except ValueError:
            continue
        if value.is_integer():
            value = int(value)
        if value not in spoken:
            continue
        if unit in MIXED_JOINERS and MIXED_FRACTION.match(line["clean"], match.end()):
            continue
        canonical = UNIT_WORDS.get(unit) or UNIT_WORDS.get(unit.rstrip("s"))
        if canonical is None:
            canonical = CLIPPED_UNIT_WORDS.get(unit)
        if canonical is None and not unit:
            clipped = CLIPPED_AFTER_A_SLASH.match(line["clean"], match.end())
            if clipped:
                canonical = CLIPPED_UNIT_WORDS.get(clipped.group(0).strip().lower(),
                                                   "years")
        typed.append((line["clean"][:match.start()].count(" "), value))
        key = (value, canonical)
        if key not in seen:
            seen.add(key)
            out.append({"value": value, "unit": canonical,
                        "text": _the_figure_and_its_unit(digits, unit, raw)})
    for position, word in enumerate(norm):
        if word in ("a", "an"):
            if position + 1 < len(norm) and norm[position + 1] in A_PORTION_UNITS:
                before = norm[position - 1] if position else ""
                after = norm[position + 2] if position + 2 < len(norm) else ""
                unit = UNIT_WORDS.get(norm[position + 1])
                if norm[position + 1] in A_PORTION_NEEDS_OF and after != "of":
                    continue
                key = (1, unit)
                if before not in OWNS_THE_UNIT and unit and key not in seen:
                    seen.add(key)
                    out.append({"value": 1, "unit": unit,
                                "text": "%s %s" % (word, norm[position + 1])})
            continue
        value = WORD_NUMBERS.get(word)
        if value is None or _counts_as_number(norm, position):
            continue
        if position in merged:
            continue
        if any(got == value and abs(at - position) <= 1 for at, got in typed):
            continue
        value, folded = _mixed_number(norm, position, value)
        merged.update(folded)
        unit = None
        step = 1 + len(folded)
        while position + step < len(norm) and step <= 5:
            after_word = norm[position + step]
            if after_word in UNIT_WORDS:
                unit = UNIT_WORDS[after_word]
                break
            if after_word not in NUMBER_FILLER:
                break
            step += 1
        key = (value, unit, word)
        if key not in seen:
            seen.add(key)
            out.append({"value": value, "unit": unit, "text": word})
    return out


ONE_IS_A_THING = frozenset("""the this that these those which no any each every another
    nice good great big small little wrong right other same next last first""".split())


def _counts_as_number(norm, position):
    word = norm[position]
    if word != "one":
        return False
    following = tuple(norm[position + 1:position + 4])
    if following[:3] in (("and", "a", "half"), ("and", "an", "half")) \
            or following[:2] in (("and", "half"), ("and", "quarter")):
        return False
    before = norm[position - 1] if position else None
    after = norm[position + 1] if position + 1 < len(norm) else None
    if after and after in UNIT_WORDS:
        return False
    return before is None or before in ONE_IS_A_THING or after is None
