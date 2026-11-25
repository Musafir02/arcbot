
import re

COMMON = """
the be to of and a in that have i it for not on with he as you do at this but his by from
# The words a person judges themselves with. The answers in bot/modules/chat.py key on them
# ("im a faliure", "i feel usless"), so the reading has to be able to hear a typo of one:
# a word the vocabulary does not hold cannot be repaired, and "i feel like a faliure" came
# back as "Got it. Is there anything you'd like a hand with?" while "i feel like a failure"
# was answered. Nothing here is new to the bot: it is the vocabulary the answers are written in.
failure failures useless worthless hopeless ashamed pathetic burden fraud disappointment
disappointment disgrace waste selfish jealousy uselessness failure
they we say her she or an will my one all would there their what so up out if about who get
which go me when make can like time no just him know take people into year your good some
could them see other than then now look only come its over think also back after use two how
our work first well way even new want because any these give day most us is are was were been
being am does did done doing has had having

hello hi hey morning evening night goodbye bye thanks thank please sorry yes yeah no nah nope
yep ok okay right sure fine cool great nice lovely good bad better best worse worst really
very super too much many more less little bit lot quite rather pretty enough almost just still
again once always never sometimes often usually maybe perhaps probably definitely actually
basically honestly literally obviously obviously anyway anyways somehow somewhere anywhere
everywhere nowhere here there where when why how what who whom whose which while until since
before after during between among through across along around behind beside beyond near off
onto over under above below inside outside toward towards without within upon about against

i you he she it we they me him her us them my your his its our their mine yours hers ours
theirs myself yourself himself herself itself ourselves themselves this that these those
someone somebody something anyone anybody anything everyone everybody everything nobody
nothing none all both each either neither other another such same different

is are was were am be been being do does did done have has had having can could will would
shall should may might must ought need dare let make made get got gotten go went gone going
come came come coming take took taken taking give gave given giving see saw seen seeing say
said saying tell told telling ask asked asking answer know knew known knowing think thought
thinking feel felt feeling want wanted wanting need needed needing like liked liking love
loved loving hate hated hating try tried trying start started starting stop stopped stopping
keep kept keeping put putting set setting run ran running walk walked walking drive drove
driving fly flew flying travel travelled traveled plan planned planning buy bought buying
pay paid paying sell sold selling find found finding look looked looking watch watched
watching read reading write wrote written writing learn learned learnt learning teach taught
teach teaching study studied studying work worked working cook cooked cooking bake baked
baking boil boiled boiling fry fried frying roast roasted roasting chop chopped chopping
wash washed washing clean cleaned cleaning fix fixed fixing build built building grow grew
grown growing plant planted planting water watered watering feed fed feeding walk walked

good bad great awful terrible fine okay nice lovely wonderful brilliant perfect horrible
happy sad angry tired hungry thirsty cold hot warm cool freezing boiling busy stressed
worried nervous scared afraid anxious excited bored lonely upset disappointed pleased glad
proud grateful thankful sorry guilty embarrassed confused lost stuck fed up

morning afternoon evening night today tomorrow tonight yesterday week weekend month year
hour minute second time day date monday tuesday wednesday thursday friday saturday sunday
january february march april may june july august september october november december
spring summer autumn fall winter christmas easter holiday holidays birthday anniversary

home house flat apartment room kitchen bedroom bathroom living room garden garage door
window wall floor ceiling roof table chair bed sofa carpet shelf cupboard fridge oven hob
microwave kettle sink toilet bath shower radiator boiler heating washing machine dishwasher
light lamp plug socket key lock bag box car bike bicycle bus train plane flight airport
station ticket road street city town village country place park river sea beach mountain
hill forest lake garden shop store market supermarket bank post office hospital doctor
dentist pharmacy school university office work job boss colleague meeting money price cost
cheap expensive card cash salary bill budget loan debt savings account

food drink meal breakfast lunch dinner snack water tea coffee milk juice wine beer bread
rice pasta potato potatoes tomato onion garlic carrot chicken beef pork lamb fish egg eggs
cheese butter milk yogurt cream sugar salt pepper oil sauce soup salad sandwich pizza cake
biscuit bread fruit apple banana orange lemon strawberry chocolate vegetable vegetables
beans lentils nuts vegetarian vegan recipe cook oven bake boil grill roast fry

head face eye eyes blink blinks blinking ear ears nose mouth tooth teeth neck throat shoulder arm hand hands hiss
finger fingers chest back stomach leg legs knee foot feet toe toes skin hair blood body
tired sleep asleep wake woke waking rest night bed dream pain hurt ache ache sore sick ill
illness cold flu fever cough headache doctor medicine tablet hospital ambulance diarrhea
hangover hungover jetlag crackered

cat cats dog dogs puppy kitten pet pets bird birds fish goldfish hamster rabbit horse
chocolate dangerous vet lead walk train feed tank

child children kid kids baby toddler son daughter boy girl mother mum mom father dad
parent parents husband wife partner family sister brother friend friends grandmother
grandfather grandma grandpa uncle aunt cousin neighbour colleague

book books read reading novel story film films movie movies watch series show tv
television music song songs podcast game games board game play theatre concert
recommend recommendation best favourite favorite character author writer episode season
boring funny interesting exciting scary sad happy mardy crabbit

computer laptop phone mobile tablet screen keyboard mouse internet wifi email password
software app website online download upload battery charger cable printer photo camera
video call message text imessage imessages

# The cake: "parkin" is "parking" with the g left off, which is the one repair of its kind that
# a real word loses, and "what is parkin" wants the cake and its follow-up.
parkin

fast slow heavy light big small large little long short tall wide narrow new old young
younger older easy hard simple difficult quick quickly slowly careful safely safe
open closed full empty free cheap clean dirty strong weak loud quiet

pounds euros dollars pence cents money cost price cheap expensive worth

jeans trousers pants shoes trainers boots socks shirt tshirt sweatshirt jumper hoodie jacket
coat skirt dress suit hat cap gloves scarf belt wallet purse bag backpack umbrella
wool wood cotton linen silk denim leather velvet metal plastic
ring watch jewellery makeup razor toothbrush toothpaste towel soap shampoo brush comb
pillow blanket duvet curtain rug mat cushion mirror picture poster bin basket
bottle glass cup mug plate bowl knife fork spoon pan pot tray jug tin jar tin foil
washing dryer iron hoover vacuum broom mop sponge cloth detergent bleach
sour cream sauce spice herb herbs pepper sugar flour yeast dough batter
scifi sciencefiction poem poetry joke jokes riddle quiz crossword puzzle
battery charger headphones speaker router printer scanner screen keyboard mouse
vitamins protein fibre fibre carbs calories diet weight muscle
stretch stretching workout gym run running walk cycling swim swimming yoga
budget savings insurance mortgage rent landlord tenant deposit invoice receipt
interview cv resume application deadline meeting email colleague manager
homework exam revision grades term lesson class teacher student
volcano earthquake storm thunder lightning rainbow clouds rain snow wind fog ice
leaves leaf tree trees plant plants soil compost weed weeds seed seeds bulb
dog cat rabbit hamster guinea pig budgie parrot goldfish kitten puppy
shrank shrunk stretched stretch colour color favourite favorite
wrote written built bought brought caught chose chosen drank drunk ate eaten fell fallen
flew flown forgot forgotten gave given grew grown hid hidden knew known lay lain lent
lost made meant met paid put rode ridden rang rung rose risen said saw seen sold sent
sang sung sat slept spoke spoken spent stood stole stolen swam swum taught thought threw
thrown understood woke worn won

add adopted adult adults advice already allergic allotment antibiotics appointment architecture
argument australia bacteria badge balcony ball basil begin bio bleed bleeding blossom blue bot
bottom breath bring broken cancelling capital causing change chasing chat cheapest check cherry
climate coach coached commute completely conference course credit cricket cut debit defensive
didn difference dinosaurs disease difference drains dried driver dropping duty easiest east eat
eating empire end energy erupts essay ever every exactly explain failed fair fan feedback fewer
fight finally finish finished firefighter five float florence football footie footy
four fractions france
french fresh friendship front fun gift giza gory group handle happens hasn haven help helpful
helps heron hides history idea ideas idiot improve industrial inspection instead instrument japan
jet jigsaw joint journey knocked kyoto lag land last lately later leeds left leftover line
lisbon lower main mainly martian match meat men mentioned miles miss mix moon mould move moved
moving musical name next nine noise nurse nutshell offside overgrown overnight own oxygen pack
paint part party pass performance person photosynthesis piano pick plumber politely powder
prepare project proper pulls pyramids questions race rail rainy recline red repairing replace
rescue review revising revolution rid role rolled roman rome rosemary roughly rubbery rude
ruining rule rules runny sam sandwiches sane save science scrambled screenshot seat secondary
security sentence session settle shift shouldn signal simply sitting six sky slipped soda
sounding sounds sourdough space spain spanish speaking speech spend spinach split sticky stiff
struggling suggest sunlight sydney system talk talked team temperature test theme thighs things
thirty thoughtful three thunderstorm tips titles tokyo tom top tricks trip true trust tulip
turn turning twins unblock university unwind usual vaccines virus visiting vocabulary volcanoes
wedding wee west wimbledon word wrong yellow yet yolk
hell
baker bridge bumpy fitter ounce packet plaster poison power primer shout sleepy stroke sweaty
tower

# Found the same way: a scan of every word the knowledge base and the deck use, run through the
# one-edit fixer. Each of these is a word of its own that was being "corrected" into another one
# (bee->be, thin->thing, wee->we, satin->sating, area->are, died->did, wars/wasp->was).
area bee died wars wasp wee satin thin thick war
# A pudding, not a small animal: "chocolate mousse" was read as "chocolate mouse".
mousse
# One edit from a feeling and a word of its own in a line people write often: "i think my email
# has been hacked" was being read as "whacked", and a rabbit that "hasnt pooed" as "pooped".
hack hacked hacking hacker poo pooed pooing
"""
US_SPELLINGS = {
    "mold": "mould", "molds": "moulds", "molded": "moulded", "moldy": "mouldy",
    "moldier": "mouldier", "moldiest": "mouldiest",
    "color": "colour", "colors": "colours", "colored": "coloured",
    "coloring": "colouring", "colorful": "colourful",
    "flavor": "flavour", "flavors": "flavours", "flavored": "flavoured",
    "flavoring": "flavouring", "flavorful": "flavourful",
    "favorite": "favourite", "favorites": "favourites",
    "favor": "favour", "favors": "favours", "favored": "favoured",
    "neighbor": "neighbour", "neighbors": "neighbours",
    "neighborhood": "neighbourhood", "neighborhoods": "neighbourhoods",
    "behavior": "behaviour", "behaviors": "behaviours",
    "humor": "humour", "labor": "labour", "labors": "labours",
    "rumor": "rumour", "rumors": "rumours", "odor": "odour", "odors": "odours",
    "vapor": "vapour", "savior": "saviour",
    "center": "centre", "centers": "centres", "centered": "centred",
    "theater": "theatre", "theaters": "theatres",
    "liter": "litre", "liters": "litres",
    "fiber": "fibre", "fibers": "fibres",
    "gray": "grey", "grays": "greys",
    "pajamas": "pyjamas", "pajama": "pyjama",
    "catalog": "catalogue", "catalogs": "catalogues",
    "dialog": "dialogue", "dialogs": "dialogues",
    "defense": "defence", "offense": "offence", "pretense": "pretence",
    "traveler": "traveller", "travelers": "travellers",
    "traveling": "travelling", "traveled": "travelled",
    "canceled": "cancelled", "canceling": "cancelling",
    "labeled": "labelled", "labeling": "labelling",
    "modeled": "modelled", "modeling": "modelling",
    "fueled": "fuelled", "fueling": "fuelling",
    "jewelry": "jewellery", "license": "licence",
    "aluminum": "aluminium", "mom": "mum", "mommy": "mummy",
    "apologize": "apologise", "organize": "organise", "organized": "organised",
    "realize": "realise", "realized": "realised", "recognize": "recognise",
    "recognized": "recognised", "memorize": "memorise", "memorized": "memorised",
}


COMMON += """
kill argue complain nag moan yell cry panic procrastinate gamble overspend vape smoke bite itch
sneeze vomit spill shrink thaw defrost sharpen descale repaint tidy declutter sweep prune repot
scour scrub soak rinse hang fold unclog worry stress ruin snore drool twitch limp shiver sweat
burn choke gasp bang churn pound sting swell tingle chat nod rub stab throb
dance cramp hurry kneel crouch jog hobble stagger retch unpack chuck wound juggle whinge
scribble trim dust polish sprinkle knead whisk stir simmer mash peel dice slice grate squeeze
# Ordinary words that begin with the sound the f-repair reads as a swapped "th": "fought",
# "frown", "fins" and "fats" are their own words, so the repair must not bend them into
# "thought", "thrown", "thins" and "thats". Kept here because the repair trusts this list to
# say what is already a word.
fought frown frowns frowning fins fats fens finer fated funder
"""

COMMON += """
pray prayed praying prayer prayers fury stare stared staring stare fort acre acres cute
"""

COMMON += """
clammy woozy jittery queasy bleary puffy giddy edgy antsy twitchy drowsy mopey quivery fidgety
wobbly phlegmy wheezy croaky sniffly snotty achy shaky crampy bloated shivery husky sneezy
rattly itchy lightheaded nauseous
"""

CORE = """
the a an and or but not no yes is are was were be been have has had do does did
i you he she we they it me my your his her our their this that these those
what why how when where who which can could would should will just now then
today tonight tomorrow thanks thank please hello hi hey ok okay sorry good great
make get take go come see know think want need like try use find give tell say
"""

def _words(text):
    words = []
    for line in str(text or "").splitlines():
        line = line.split("#", 1)[0]
        for word in line.split():
            bare = word.replace("-", "").replace("'", "")
            if bare.isalpha():
                words.append(word.lower())
    return frozenset(words)


FEELINGS = _words("""sad unhappy miserable down low gutted heartbroken crying tears
disappointed devastated depressed upset lonely alone isolated angry annoyed furious cross
irritated frustrated mad livid raging anxious worried worry nervous scared afraid
frightened stressed overwhelmed panic panicking dreading tired exhausted knackered
# The doing form of a worry: "im worrying", "im stressing", "im overthinking", "im obsessing".
# A word the reading calls a feeling has to be in this list, or "im worrying" is a name.
worrying stressing overthinking obsessing spiralling spiraling
shattered wiped sleepy bushed drained happy glad delighted thrilled pleased excited proud
relieved chuffed grateful thankful appreciate guilty ashamed embarrassed bored boring
stress cry terrified petrified panicky butterflies
weepy tearful homesick shy hungry starving thirsty peckish ravenous
rotten lousy meh rough crap rubbish grumpy restless numb
# "im worse", "im no better": a comparison of two states is how a bad day is told in a second
# turn, and a cue the reading calls a feeling has to be in this list or the line reads as a name.
worse
cheesed empty flat hollow blank
# The plain words for a low day: "i feel awful", "i feel hopeless", "im still grieving",
# "my anxiety is bad". The reading and the reply must agree on what a feeling word is.
awful hopeless worthless grieving mourning despair despairing anxiety
# The plain words for being unsure or worried about something: "im confused", "im concerned",
# and the moods that name themselves: glum, mardy, zonked.
confused confusing confusion puzzled baffled bewildered muddled
interested concerned glum mopey teary downhearted despondent blah bleh cranky
snappy tetchy ratty mardy jittery antsy edgy tense pooped whacked zonked
hungover hangover jet-lagged run-down crackered
# "im fried" is the same tiredness as "im wiped", and it is in the reading's tiredness list, so
# it has to be a feeling word here too: the two lists are read as one (MisspeltFeelingTest).
fried
fuming seething frazzled incandescent narked miffed
# "im awesome", "im hopeful", "im emotional" were answered "Hi Awesome - fair enough" and "Nice
# to meet you, Emotional": the lexicon held the near-synonyms ("excited", "glad") but not the
# words themselves, so neither the reading nor the name reader knew them.
awesome hopeful emotional
# The same gap, one letter out: "im irritble" and "im aprehensive" are answered "Nice to meet
# you, ..." because the one-edit repair has nothing to repair them to - "irritable" and
# "apprehensive" were not in the vocabulary at all, and the lists above held only their
# near-synonyms ("irritated", "anxious"). "im cheerful" was answered "I'm listening" for the
# same reason.
irritable apprehensive cheerful
# The ending a state is said with, which a reply already answers and the reading did not know:
# the pools read "im wrecked", "im spent", "im swamped" and "im jetlagged" as the tired and
# stressed days they are, but none of those words was in the vocabulary, so the one-edit repair
# had nothing to repair a slip toward and the line fell out of its pool altogether - "im wrcked"
# got "Got it. Is there anything you'd like a hand with?", and "im spnt", "im bet" and "im ded"
# were answered "Nice to meet you, Spnt" / "Bet" / "Ded" - a word the reading does not know,
# standing where a state stands after "im", is a name. A state typed correctly was read as an
# introduction for the same reason ("im cheery" was "Hi Cheery").
# Every word here is one a reply in bot/modules/ already answers in a line of its own ("worn"
# and "wearing" only in "worn out" and "wearing thin"), and a word the lexicon knows keeps its
# own meaning in the repair: "boat" is not bent to "beat" and "deaf" is not "dead".
beat dead draining exhausting fagged knackering spent tiring wearing worn wrecked
overwhelming stressful swamped jetlagged cheery buzzing brilliant
# The colour as the mood: "im blue", "feeling a bit blue". It was not a feeling word at all, so
# "im blue" was read as a name and answered "Nice to meet you, Blue". The state has to be said of
# the person (see SELF_ONLY_STATE), because a door and a sea are blue too.
blue
# A condition somebody says they have is how they are, not who they are. "im bipolar" was
# answered "Nice to meet you, Bipolar", and the store filed the word as a name, so every later
# line knew the person by it. The seven below were found by probing the class; the rest are the
# conditions a person names about themselves in the same position. A word here is a state the
# reading knows, which is what stops a name.
bipolar schizophrenic anorexic bulimic narcoleptic psychotic infertile sterile paranoid
transgender nonbinary hiv""")

A_BODY_STATE = frozenset("""pale pallid ashen grey gray greyish grayish mottled blotchy spotty
puffy bloated clammy flushed feverish shivery shaky tender husky snotty sniffly""".split())
A_STATE = frozenset("""hurt hurting desperate content confused confusing broken drunk torn
hungover sober skint shattered wiped gutted
starving fuming freezing boiling raging aching itching shaking shivering sweating
chocka chocker manky wonky tickety wabbit""".split()) | A_BODY_STATE

STATES_SAID_ONTO_IM = FEELINGS | A_STATE | frozenset("""
sick suicidal fine ok okay good better great done stuck lost back home here busy free fed
""".split())

STATES_WITHOUT_G = frozenset(word[:-1] for word in FEELINGS | A_STATE if word.endswith("g"))

COMMON_NAMES = frozenset("""
abbie abigail adam adrian aiden aisha alan albert alex alexa alexander alfred ali alice alicia
allison amanda amber amelia amy ana anastasia andre andrea andrew andy angela angie anita ann
anna anne annette annie anthony antonio april archie arlene arnold arthur ashley audrey austin
ava ayesha barbara barry beatrice becky belinda ben benjamin bernard beth bethany betty beverly
bianca bill billy blake bob bobby bonnie boris brad bradley brandon brenda brendan brian bridget
brittany brooke bruce bryan caitlin callum calvin cameron camila carl carla carlos carmen carol
caroline carrie cary casey cassie catherine cathy chad charlene charles charlie charlotte chelsea
cheryl chloe chris christian christina christine christopher cindy claire clara clarence claudia
clifford clint cody colin connie connor craig crystal curtis cynthia daisy dale damian damon dan
dana daniel danielle danny darcy daren darlene darren darryl dave david dawn dean debbie deborah
debra denise dennis derek diana diane dianne dina dominic don donald donna dora doris dorothy
doug douglas duncan dustin dylan earl eddie edgar edith eduardo edward eileen elaine eleanor
elena eli elias elijah elizabeth ella ellen ellie elliot eloise elsie emily emma emmanuel enid
eric erica erik erin ernest esther ethan eva evan eve evelyn fiona florence floyd frances
francis frank fred freda freddie gabriel gabrielle gail gareth gary gavin gemma gene geoff
geoffrey george georgia gerald geraldine gilbert gina glen glenda glenn gloria gordon grace
graham grant greg gregory gwen gwendolyn hannah harold harriet harry harvey hazel heather
hector heidi helen henry herbert holly hugh hugo ian ida ike imogen irene iris isaac isabel
isabella isla ivan jack jackie jacob jade jaime jake james jamie jan jane janet janice jared
jasmine jason jay jayne jean jeff jeffrey jemma jenny jeremy jerome jerry jess jessica jill
jim jimmy jo joan joanna joanne jodie joe joel joey john johnny jon jonathan jordan jose
joseph josephine josh joshua joyce juan judith judy julia julian julie june justin kara karen
karl kate katherine kathleen kathryn kathy katie katrina kay kayla keith kelly kelsey ken
kenneth kerry kevin kieran kim kimberly kirk kirsty kit kurt kyle lana lance lara larry laura
lauren laurie lawrence leah lee leila lena leo leon leonard lesley leslie lester lewis li liam
lilian lily linda lindsay lindsey lionel lisa lloyd lois lola loren lorenzo lorraine louis
louisa louise lucas lucia lucy lucy luis luke lydia lynn lynne mabel maddie madeleine madison
mae maggie malcolm mandy manuel marc marcus margaret maria marian marie marilyn marina mario
marion marjorie mark marlene marsha marshall martha martin marvin mary mason matt matthew
maureen maurice max maxine may megan mel melanie melissa mia micah michael michele michelle
mickey mike mildred miles millie milton miranda miriam molly monica morgan muhammad myra
nadia nancy naomi natalie natasha nathan neil nelson nicholas nick nico nicola nicolas nicole
nigel nina noah noel nora norma norman olga oliver olivia omar oscar owen pablo paige pamela
patricia patrick patsy paul paula pauline pearl pedro peggy penny percy pete peter phil philip
phillip phoebe phyllis polly peter priya rachel ralph ramon randall randy raul ray raymond
rebecca reggie regina renee rex rhonda ricardo richard rick ricky rita rob robbie robert
roberta roberto robin robyn rodney roger roland ron ronald ronnie rosa rosalie rose rosemary
ross roy ruben ruby russell ruth ryan sally sam samantha samuel sandra sara sarah scott sean
sebastian selina seth shane shannon sharon shawn sheila shelby shelley sherry shirley sid
sidney simon sofia sonia sonya sophia sophie stacey stacy stanley stella stephanie stephen
steve steven stuart sue susan susie suzanne sylvia tamara tammy tanya tara ted teresa terry
tessa thelma theodore theresa thomas tiffany tim timothy tina toby todd tom tommy toni tony
tracey tracy travis trevor tricia trish tristan troy tyler val valerie vanessa vera veronica
vernon vicki vicky victor victoria vince vincent violet vivian vivien wade walter wanda warren
wayne wendy wesley whitney wilbur wilfred will william willie wilson winifred yasmin yolanda
zach zachary zoe zoe
""".split())

SOUNDS_LIKE_A_FEELING = {
    "board": "bored",
    "tried": "tired",
}

CORE_WORDS = frozenset(CORE.split())

CHAT = {
    "u": "you", "ur": "your", "ure": "you are", "urs": "yours", "r": "are", "y": "why",
    "ya": "you", "yah": "yes", "yeh": "yes", "yea": "yes", "yep": "yes", "nope": "no",
    "k": "ok", "kk": "ok", "okey": "ok", "okey dokey": "ok", "cn": "can", "cud": "could",
    "ar": "are", "wuz": "was", "duz": "does", "hav": "have",
    "thx": "thanks", "thnx": "thanks", "thanx": "thanks", "ty": "thanks", "tysm": "thanks",
    "cheers": "thanks", "ta": "thanks", "tyvm": "thanks so much",
    "pls": "please", "plz": "please", "pleas": "please", "plss": "please",
    "bc": "because", "bcoz": "because", "becos": "because", "cuz": "because",
    "coz": "because", "cos": "because", "cause": "because", "caus": "because",
    "thru": "through", "tho": "though", "tho'": "though", "altho": "although",
    "nite": "night", "tonite": "tonight", "2nite": "tonight", "tmrw": "tomorrow",
    "tomoz": "tomorrow", "tomoro": "tomorrow", "tommorow": "tomorrow", "2moro": "tomorrow",
    "tmoro": "tomorrow", "n8": "night", "seeya": "see you", "speek": "speak",
    "gr8": "great", "b4": "before", "w8": "wait", "2day": "today", "2morrow": "tomorrow",
    "rn": "now", "tn": "tonight",
    "h8s": "hates", "l8": "late",
    "msg": "message", "msgs": "messages", "asap": "as soon as possible",
    "idk": "i do not know", "dont know": "do not know",
    "stomakaike": "stomach ache", "stomach ake": "stomach ache",
    "wanna": "want to",
    "gimme": "give me", "outta": "out of",
    "hafta": "have to", "coulda": "could have", "shoulda": "should have",
    "woulda": "would have", "musta": "must have", "nuthin": "nothing",
    "imo": "in my opinion", "imho": "in my opinion",
    "btw": "by the way", "nvm": "never mind", "np": "no problem", "yw": "you are welcome",
    "rn": "right now", "atm": "at the moment", "abt": "about", "abt.": "about",
    "prob": "probably", "probs": "probably", "def": "definitely",
    "w/": "with", "w/o": "without", "b/c": "because", "&": "and", "n": "and",
    "cya": "see you", "gtg": "got to go", "brb": "be right back",
    "afaik": "as far as i know", "iirc": "if i remember correctly",
    "wtf": "what", "smh": "shaking my head", "fwiw": "for what it is worth",
    "irl": "in real life", "dm": "message", "tmi": "too much information",
    "wat": "what", "wats": "what is", "wut": "what", "wot": "what", "whut": "what",
    "kno": "know", "knos": "knows",
    "hows": "how is", "howd": "how did", "whats": "what is", "wots": "what is",
    "wheres": "where is",
    "whatre": "what are", "shouldve": "should have",
    "whos": "who is", "whys": "why is", "whens": "when is", "howsit": "how is it",
    "ne1": "anyone", "sum1": "someone", "any1": "anyone", "every1": "everyone",
    "evry1": "everyone", "no1": "no one", "some1": "someone", "thruout": "throughout",
    "lol": "lol", "lmao": "lol", "haha": "haha", "hehe": "hehe", "omg": "oh my god",
    "hbu": "how about you", "wyd": "what are you doing", "idc": "i do not care",
    "wdyt": "what do you think", "wdy think": "what do you think",
    "jk": "just kidding", "rofl": "lol", "yolo": "you only live once",
    "nm": "not much", "nmu": "not much you", "wbu": "what about you", "ikr": "i know right",
    "tbh": "to be honest", "dunno": "i do not know",
    "dno": "i do not know", "dnno": "i do not know", "iunno": "i do not know",
    "donno": "i do not know", "dnt": "do not",
    "gonna": "going to", "gotta": "got to", "lemme": "let me",
    "kinda": "kind of", "sorta": "sort of", "cmon": "come on", "aint": "is not",
    "wana": "want to", "wanne": "want to", "wannna": "want to", "wanta": "want to",
    "hasta": "have to", "shood": "should", "shuld": "should", "coud": "could",
    "spose": "suppose", "becoz": "because", "plis": "please",
    "tnight": "tonight", "tonyt": "tonight", "tonit": "tonight", "2nit": "tonight",
    "tday": "today", "todai": "today", "tmoz": "tomorrow", "2moz": "tomorrow",
    "wid": "with", "weerd": "weird", "styff": "stuff", "stuf": "stuff",
    "knw": "know", "knwo": "know", "defo": "definitely", "rlly": "really",
    "lik": "like", "lyk": "like", "gd": "good", "qwik": "quick", "quik": "quick",
    "chek": "check", "chekcing": "checking", "shoppin": "shopping", "recive": "receive",
    "h8": "hate", "h8d": "hated", "h8ing": "hating",
    "wna": "want to", "nething": "anything", "nethin": "anything",
}

CHAT.update({
    "tkx": "thanks", "tks": "thanks", "thxs": "thanks", "thnks": "thanks", "thks": "thanks",
    "fanks": "thanks", "thanxs": "thanks",
})

CHAT.update({
    "tmrow": "tomorrow", "tmorro": "tomorrow", "tomo": "tomorrow", "tomoz": "tomorrow",
    "tmw": "tomorrow", "2mora": "tomorrow", "2morra": "tomorrow",
    "yday": "yesterday", "ystday": "yesterday", "yestday": "yesterday", "2day": "today",
})

CHAT.update({
    "bday": "birthday", "b'day": "birthday", "b-day": "birthday", "bdays": "birthdays",
    "xmas": "christmas", "x-mas": "christmas", "crimbo": "christmas",
    "summat": "something", "sommat": "something", "sumfink": "something",
    "missus": "wife", "hubby": "husband", "bubba": "baby",
    "wuu2": "what you up to", "wu2": "what you up to", "wuu": "what you up to",
})

TYPED_CONTRACTIONS = {
    "cnt": "cant", "cudnt": "couldnt", "coudnt": "couldnt", "shudnt": "shouldnt",
    "wudnt": "wouldnt", "dnt": "dont", "wnt": "wont", "didnt": "didnt", "wasnt": "wasnt",
    "isnt": "isnt", "arent": "arent", "werent": "werent", "hasnt": "hasnt",
    "havnt": "havent", "avnt": "havent", "aint": "aint", "doesnt": "doesnt",
}

CONTRACTIONS = {
    "dont": "don't", "cant": "can't", "wont": "won't", "isnt": "isn't",
    "doesnt": "doesn't", "im": "i'm", "ive": "i've", "i'll": "i'll",
    "babys": "baby's", "childs": "child's", "toddlers": "toddler's",
    "cnt": "can't", "cudnt": "couldn't", "coudnt": "couldn't", "shudnt": "shouldn't",
    "wudnt": "wouldn't", "dnt": "don't", "wnt": "won't", "didnt": "didn't",
    "hasnt": "hasn't", "havnt": "haven't", "avnt": "haven't", "aint": "ain't",
}

CHAT.update({
    "fone": "phone", "fones": "phones", "fonecall": "phone call", "phne": "phone",
    "av": "have", "bv": "have", "hve": "have",
    "avnt": "have not", "propa": "proper",
    "gf": "girlfriend", "gfs": "girlfriends", "bf": "boyfriend", "bfs": "boyfriends",
    "sed": "said", "syas": "says",
    "bova": "bothered", "bovad": "bothered", "bovered": "bothered", "botherd": "bothered",
    "cba": "can not be bothered", "cbf": "can not be bothered",
    "giv": "give", "givin": "giving", "gimme a": "give me a",
    "gona": "going to", "gonig": "going", "goina": "going to",
    "nt": "not", "cnt": "can not",
    "havnt": "have not", "avent": "have not",
    "shudnt": "should not", "cudnt": "could not", "wudnt": "would not",
    "dats": "that is", "das": "that is", "dere": "there",
    "tryna": "trying to", "trynna": "trying to",
    "tnx": "thanks", "tnks": "thanks", "thnkx": "thanks", "thnxs": "thanks",
    "sumin": "something", "sumink": "something", "anyfin": "anything",
    "anyfink": "anything", "eveything": "everything", "evrythin": "everything",
    "nuffink": "nothing", "nuffin": "nothing",
    "meds": "medicines",
    "abt": "about", "bout time": "about time",
    "owt": "out", "owtside": "outside", "owta": "out of",
    "owt else": "anything else", "owt wrong": "anything wrong",
})

CHAT.update({
    "avnt": "have not", "havnt": "have not",
    "ment": "meant",
    "normaly": "normally", "usualy": "usually",
    "cupple": "couple", "cupples": "couples",
    "prezzie": "present",
    "prezzy": "present", "prezzies": "presents", "pressie": "present", "pressies": "presents",
    "presant": "present",
})

CHAT.update({
    "decs": "decorations", "decs.": "decorations",
    "lic": "licence",
    "hosp": "hospital",
})

CHAT.update({
    "brekkie": "breakfast", "brekky": "breakfast",
    "biccy": "biscuit", "biccies": "biscuits", "bikkie": "biscuit", "bikkies": "biscuits",
    "choccy": "chocolate", "choccies": "chocolates",
    "sarnie": "sandwich", "sarnies": "sandwiches", "butty": "sandwich", "butties": "sandwiches",
    "on the blink": "not working",
})

MISSPELLINGS = {
    "tite": "tight", "thight": "tight",
    "slurd": "slurred", "slurrd": "slurred", "slured": "slurred",
    "chest pane": "chest pain",
    "hart attack": "heart attack", "hart rate": "heart rate", "hart beat": "heartbeat",
    "my hart": "my heart", "his hart": "his heart", "her hart": "her heart",
    "crak": "crack", "craks": "cracks", "craked": "cracked", "craking": "cracking",
    "feels num": "feels numb", "feel num": "feel numb", "is num": "is numb",
    "are num": "are numb", "gone num": "gone numb", "went num": "went numb",
    "goes num": "goes numb", "going num": "going numb",
    "gaspng": "gasping", "gaspping": "gasping", "gaspin": "gasping",
    "gaspign": "gasping", "gaspeing": "gasping",

    "layed": "laid", "layed off": "laid off",
    "faliure": "failure", "faluire": "failure", "failiure": "failure",
    "dissapointment": "disappointment",
    "dissapointing": "disappointing", "dissapoint": "disappoint",
    "faliur": "failure", "falure": "failure", "fialure": "failure",
    "failur": "failure", "wortles": "worthless", "wothles": "worthless",
    "useles": "useless", "uselss": "useless", "hopeles": "hopeless",
    "nuiscance": "nuisance", "letdow": "letdown",
    "usless": "useless",
    "whcih": "which", "whihc": "which", "whaat": "what", "tounge": "tongue", "toung": "tongue",
    "recipie": "recipe", "reciepe": "recipe", "resipee": "recipe",
    "qinuoa": "quinoa", "qunioa": "quinoa", "quinoia": "quinoa", "quinnoa": "quinoa",
    "sandwhich": "sandwich", "sandwitch": "sandwich",
    "potatos": "potatoes", "tomatos": "tomatoes", "avacado": "avocado", "eg": "egg",
    "definately": "definitely", "definatly": "definitely",
    "sence": "sense",
    "tempreture": "temperature",
    "wierd": "weird",
    "beleive": "believe", "aswell": "as well",
    "apreciate": "appreciate", "appriciate": "appreciate", "apprechiate": "appreciate",
    "alot": "a lot", "thier": "their", "wich": "which",
    "wheather": "weather", "tomorow": "tomorrow", "exercize": "exercise",
    "excercise": "exercise",
    "acheive": "achieve", "adress": "address",
    "goverment": "government", "enviroment": "environment",
    "necesary": "necessary",
    "restaraunt": "restaurant",
    "vegtable": "vegetable", "chocalate": "chocolate", "choclate": "chocolate",
    "spagetti": "spaghetti", "lasagne": "lasagne", "yoghurt": "yogurt",
    "teh": "the", "hte": "the", "adn": "and", "nad": "and", "taht": "that",
    "waht": "what", "whta": "what", "yuo": "you", "fo": "of", "ot": "to",
    "becuase": "because", "becasue": "because", "beacuse": "because",
    "wether": "weather", "wether or not": "whether or not",
    "weather or not": "whether or not",
    "seperate": "separate", "definetly": "definitely",
    "recieve": "receive", "recieved": "received",
    "belive": "believe", "occured": "occurred", "begining": "beginning",
    "calender": "calendar", "recomend": "recommend", "reccomend": "recommend",
    "recomendations": "recommendations", "diffrent": "different", "differnt": "different",
    "excersize": "exercise",
    "tommorow": "tomorrow", "untill": "until", "freind": "friend",
    "freinds": "friends", "garantee": "guarantee", "gratefull": "grateful",
    "immediatly": "immediately", "independant": "independent", "intresting": "interesting",
    "knowlege": "knowledge", "libary": "library", "maintainance": "maintenance",
    "neccessary": "necessary", "occassion": "occasion", "posible": "possible",
    "prefered": "preferred", "recomended": "recommended", "resturant": "restaurant",
    "rythm": "rhythm", "suprise": "surprise",
    "truely": "truly", "useing": "using", "usefull": "useful", "vegeterian": "vegetarian",
    "verry": "very", "writting": "writing",
    "remoov": "remove", "brokn": "broken", "dropin": "dropping", "lern": "learn",
    "gettin": "getting", "goin": "going", "doin": "doing", "nothin": "nothing",
    "somethin": "something", "anythin": "anything", "everythin": "everything",
    "lil": "little", "smth": "something", "sth": "something", "ppl": "people",
    "bcos": "because", "gud": "good",
    "bovvered": "bothered", "bovverd": "bothered", "arsed": "bothered",
    "fink": "think", "mebbe": "maybe", "luvly": "lovely",
    "sista": "sister", "sistah": "sister", "bruv": "brother",
    "bruvva": "brother", "bruvver": "brother", "muvva": "mother", "muva": "mother",
    "muvver": "mother", "fatha": "father",
    "feelin": "feeling", "talkin": "talking", "waitin": "waiting", "makin": "making",
    "tryin": "trying", "lookin": "looking", "comin": "coming", "knowin": "knowing",
    "thinkin": "thinking", "wonderin": "wondering", "l8r": "later", "g2g": "got to go", "m8": "mate",
    "complainin": "complaining", "quittin": "quitting", "shoppin": "shopping",
    "workin": "working", "runnin": "running", "eatin": "eating", "sleepin": "sleeping",
    "drivin": "driving", "sittin": "sitting", "studyin": "studying", "listenin": "listening",
    "holdin": "holding", "livin": "living", "lovin": "loving", "writin": "writing",
    "readin": "reading", "helpin": "helping", "openin": "opening", "closin": "closing",
    "cud": "could", "shoud": "should", "shud": "should", "wud": "would", "wold": "would",
    "hungrey": "hungry", "hungray": "hungry", "thristy": "thirsty",
    "rekon": "reckon", "rekons": "reckons", "rekoning": "reckoning",
    "awsome": "awesome", "awfl": "awful", "awfull": "awful", "hopefull": "hopeful",
    "ankshus": "anxious", "anxios": "anxious", "anxty": "anxious",
    "emosh": "emotional",
    "deprsd": "depressed", "depresd": "depressed", "depresed": "depressed",
    "stresd": "stressed", "woryd": "worried", "angryy": "angry", "irratable": "irritable",
    "chiken": "chicken", "chikcen": "chicken",
    "tink": "think", "tinks": "thinks", "tinking": "thinking", "tinkin": "thinking",
    "tinked": "thought", "tought": "thought",
    "kichen": "kitchen", "kitched": "kitchen", "wach": "watch", "wathc": "watch",
    "bord": "bored", "boared": "bored", "blak": "black", "stomack": "stomach",
    "ankel": "ankle", "plummer": "plumber", "shoer": "shower", "curtins": "curtains",
    "cusion": "cushion", "cupbord": "cupboard", "tabl": "table", "hous": "house",
    "brocolli": "broccoli", "omlette": "omelette", "porrige": "porridge",
    "recepie": "recipe", "recpie": "recipe",
    "tirred": "tired", "tierd": "tired", "headach": "headache", "headace": "headache",
    "docor": "doctor", "reciept": "receipt", "radiater": "radiator", "boilar": "boiler",
    "boilier": "boiler",
    "docer": "doctor", "doctur": "doctor", "dockter": "doctor",
    "ambulnce": "ambulance", "ambulence": "ambulance", "ambulanc": "ambulance",
    "hostpital": "hospital", "hospitl": "hospital",
    "paracetomal": "paracetamol", "paracetemol": "paracetamol", "paracetmol": "paracetamol",
    "ibuprofin": "ibuprofen", "ibruprofen": "ibuprofen", "ibroprofen": "ibuprofen",
    "matress": "mattress", "allergey": "allergy", "allergies": "allergies",
    "appoinment": "appointment", "appointmnt": "appointment", "sanwhich": "sandwich",
    "dishwosher": "dishwasher", "battry": "battery", "washign": "washing",
    "accomodation": "accommodation", "agian": "again", "agianst": "against",
    "arguement": "argument", "bacause": "because", "beleif": "belief",
    "buisness": "business", "catagory": "category", "collegue": "colleague",
    "comittee": "committee", "completly": "completely", "concensus": "consensus",
    "concious": "conscious", "curiousity": "curiosity", "dilemna": "dilemma",
    "dissapointed": "disappointed", "embarassed": "embarrassed", "embarassing": "embarrassing",
    "freindly": "friendly", "frist": "first", "grammer": "grammar", "happend": "happened",
    "harrass": "harass", "intrest": "interest", "jist": "just", "jsut": "just",
    "jstu": "just", "knowlage": "knowledge", "lenght": "length", "lisence": "licence",
    "medecine": "medicine", "millenium": "millennium", "noticable": "noticeable",
    "occuring": "occurring", "paralel": "parallel", "perfomance": "performance",
    "personel": "personnel", "persue": "pursue", "posession": "possession",
    "priviledge": "privilege", "probaly": "probably",
    "pronounciation": "pronunciation", "publically": "publicly", "questionaire": "questionnaire",
    "recommened": "recommended", "refered": "referred", "relevent": "relevant",
    "religous": "religious", "rember": "remember", "remeber": "remember",
    "responsable": "responsible", "scedule": "schedule", "shedule": "schedule",
    "seperated": "separated", "shoudl": "should", "coudl": "could", "woudl": "would",
    "succesful": "successful", "sucessful": "successful", "suprize": "surprise",
    "supercede": "supersede", "temperture": "temperature", "tempriture": "temperature",
    "tendancy": "tendency", "threshhold": "threshold", "tommorrow": "tomorrow",
    "transfered": "transferred", "unecessary": "unnecessary", "usualy": "usually",
    "vaccum": "vacuum", "vegtables": "vegetables", "vehical": "vehicle", "wehn": "when",
    "wiht": "with", "wonderfull": "wonderful", "yuor": "your", "hwat": "what",
    "brill": "brilliant", "seige": "siege", "sieze": "seize", "mediteranean": "mediterranean",
    "nabour": "neighbour", "nabours": "neighbours",
    "nabor": "neighbour", "nabors": "neighbours",
    "neigbour": "neighbour", "neigbours": "neighbours",
    "daugther": "daughter", "daugthers": "daughters",
    "dauter": "daughter", "dauters": "daughters",
    "tird": "tired", "geting": "getting",
    "kiling": "killing", "kilin": "killing", "headeche": "headache", "headche": "headache",
    "headake": "headache", "stomache": "stomach", "kidnees": "kidneys", "kidnies": "kidneys",
    "ancious": "anxious", "anxous": "anxious", "misrable": "miserable",
    "strest": "stressed", "deprest": "depressed", "annoied": "annoyed",
    "embarased": "embarrassed", "overwelmd": "overwhelmed", "greatful": "grateful",
    "sufering": "suffering", "caugh": "cough", "coughin": "coughing", "docter": "doctor",
    "hospitle": "hospital", "medcine": "medicine", "symtoms": "symptoms", "dizy": "dizzy",
    "vometing": "vomiting", "swolen": "swollen", "throte": "throat", "brething": "breathing",
    "bleading": "bleeding",
    "leeking": "leaking", "driping": "dripping", "radiaters": "radiators",
    "freezar": "freezer", "fridg": "fridge", "ovan": "oven", "microwve": "microwave",
    "plumer": "plumber",
    "yesturday": "yesterday", "saterday": "saturday", "wensday": "wednesday",
    "defintely": "definitely", "proberly": "probably", "allways": "always",
    "allready": "already", "intrested": "interested", "restarant": "restaurant",
    "woried": "worried", "worring": "worrying", "cheeper": "cheaper",
    "exersize": "exercise", "vitimens": "vitamins", "proteen": "protein",
    "protien": "protein",
    "proten": "protein", "protine": "protein",
    "recomends": "recommends",
    "temprature": "temperature",
    "tempreature": "temperature", "tempratue": "temperature",
    "migrane": "migraine", "migranes": "migraines", "migrain": "migraine",
    "stomaches": "stomachs",
    "coughting": "coughing",
    "dizey": "dizzy",
    "alergic": "allergic", "allerjic": "allergic",
    "pennicillin": "penicillin", "penicilin": "penicillin", "penicillian": "penicillin",
    "diarhea": "diarrhoea", "diarhoea": "diarrhoea", "dioreah": "diarrhoea",
    "dihorrea": "diarrhoea", "diahorrea": "diarrhoea", "diarrea": "diarrhoea",
    "colestrol": "cholesterol", "cholesteral": "cholesterol", "colesterol": "cholesterol",
    "vomitting": "vomiting", "vommiting": "vomiting",
    "infektion": "infection", "infekshun": "infection", "infecton": "infection",
    "bloked": "blocked", "realy": "really",
    "feaver": "fever", "feaverish": "feverish",
    "a cought": "a cough", "the cought": "the cough", "my cought": "my cough",
    "bad cought": "bad cough",
    "iv gorra": "i have got a", "ive gorra": "i have got a",
    "hes gorra": "he has got a", "shes gorra": "she has got a",
    "we gorra": "we have got a", "they gorra": "they have got a",
    "iv got": "i have got", "iv had": "i have had", "iv been": "i have been",
    "iv just": "i have just", "iv never": "i have never", "iv not": "i have not",
    "iv only": "i have only", "iv always": "i have always", "iv already": "i have already",
    "iv still": "i have still", "iv also": "i have also", "iv lost": "i have lost",
    "iv taken": "i have taken", "iv stopped": "i have stopped", "iv tried": "i have tried",
    "probly": "probably", "probally": "probably",
    "disapointment": "disappointment",
    "disappoinment": "disappointment",
    "burdon": "burden", "burdons": "burdens",
    "worthles": "worthless", "worthlesly": "worthlessly",
}

MISSPELLINGS.update({
    "stomac": "stomach", "swallen": "swollen", "bruse": "bruise", "brusie": "bruise",
    "simptoms": "symptoms", "consentrate": "concentrate",
    "daugher": "daughter", "medicaton": "medication", "presure": "pressure",
    "paracetemol": "paracetamol", "paracetmol": "paracetamol", "ibuprofin": "ibuprofen",
    "ibuprophen": "ibuprofen", "presciption": "prescription", "perscripton": "prescription",
    "apointment": "appointment", "apointmnet": "appointment",
    "heatng": "heating", "triping": "tripping", "kettel": "kettle", "passward": "password",
    "pasword": "password", "tennants": "tenants", "substatute": "substitute",
    "substitue": "substitute", "properley": "properly", "properlly": "properly",
    "yesterdy": "yesterday", "goign": "going", "depresed": "depressed",
    "nakerd": "knackered", "nakered": "knackered", "knackerd": "knackered",
    "starvin": "starving", "starveing": "starving",
    "fumin": "fuming", "fummin": "fuming", "sare": "sore",
    "heachache": "headache", "heachaches": "headaches",
    "sik": "sick", "tyred": "tired",
    "mashine": "machine", "mashines": "machines",
    "beff": "beef", "chese": "cheese", "teatching": "teething",
})


MISSPELLINGS.update({
    "abotu": "about",
    "abuot": "about",
    "aftre": "after",
    "anrgy": "angry",
    "anxoius": "anxious",
    "aobut": "about",
    "aplpes": "apples",
    "appel": "apple",
    "apsta": "pasta",
    "arzor": "razor",
    "asuce": "sauce",
    "atfer": "after",
    "audlt": "adult",
    "awflu": "awful",
    "baout": "about",
    "bioling": "boiling",
    "biuld": "build",
    "blodo": "blood",
    "bolod": "blood",
    "borad": "board",
    "borde": "bored",
    "braed": "bread",
    "brsuh": "brush",
    "bulid": "build",
    "cehst": "chest",
    "chets": "chest",
    "cheast": "chest",
    "chlid": "child",
    "cihld": "child",
    "claen": "clean",
    "clena": "clean",
    "coluor": "colour",
    "craem": "cream",
    "dirnk": "drink",
    "dreyr": "dryer",
    "drnik": "drink",
    "drvie": "drive",
    "dryre": "dryer",
    "duaghter": "daughter",
    "ebans": "beans",
    "ejans": "jeans",
    "elmon": "lemon",
    "enver": "never",
    "eyast": "yeast",
    "fater": "after",
    "fbire": "fibre",
    "feevr": "fever",
    "fimls": "films",
    "firts": "first",
    "fisrt": "first",
    "folor": "floor",
    "folur": "flour",
    "funyn": "funny",
    "fxied": "fixed",
    "giong": "going",
    "goign": "going",
    "hadns": "hands",
    "hosue": "house",
    "hpone": "phone",
    "hsort": "short",
    "htere": "there",
    "hwich": "which",
    "hwile": "while",
    "inght": "night",
    "jenas": "jeans",
    "kinfe": "knife",
    "laern": "learn",
    "lbood": "blood",
    "lcean": "clean",
    "lfoor": "floor",
    "lgass": "glass",
    "lgiht": "light",
    "lovde": "loved",
    "lpace": "place",
    "lpane": "plane",
    "lseep": "sleep",
    "maent": "meant",
    "mnoth": "month",
    "moeny": "money",
    "monht": "month",
    "monye": "money",
    "motuh": "mouth",
    "muontain": "mountain",
    "muoth": "mouth",
    "nevre": "never",
    "ngiht": "night",
    "nigth": "night",
    "nihgt": "night",
    "ocugh": "cough",
    "oculd": "could",
    "odugh": "dough",
    "ofetn": "often",
    "oging": "going",
    "omney": "money",
    "owrth": "worth",
    "palnt": "plant",
    "pasat": "pasta",
    "patsa": "pasta",
    "phnoe": "phone",
    "phoen": "phone",
    "pizaz": "pizza",
    "platn": "plant",
    "puonds": "pounds",
    "raelly": "really",
    "raozr": "razor",
    "rbead": "bread",
    "rceam": "cream",
    "rdink": "drink",
    "rdive": "drive",
    "rievr": "river",
    "rihgt": "right",
    "rtain": "train",
    "salda": "salad",
    "sehlf": "shelf",
    "shuold": "should",
    "sicne": "since",
    "sitll": "still",
    "slepe": "sleep",
    "snakc": "snack",
    "stlil": "still",
    "sugra": "sugar",
    "tarin": "train",
    "tdoay": "today",
    "tehre": "there",
    "tierd": "tired",
    "tinlging": "tingling",
    "toady": "today",
    "tooht": "tooth",
    "totoh": "tooth",
    "tsill": "still",
    "udner": "under",
    "ufnny": "funny",
    "ujice": "juice",
    "umsic": "music",
    "unedr": "under",
    "unitl": "until",
    "upppy": "puppy",
    "usgar": "sugar",
    "veagn": "vegan",
    "wacth": "watch",
    "waetr": "water",
    "wehre": "where",
    "whcih": "which",
    "whiel": "while",
    "whihc": "which",
    "wolud": "would",
    "wotrh": "worth",
    "wroth": "worth",
    "wtaer": "water",
})

URGENT_MISSPELLINGS = {
    "swolen": "swollen", "swollan": "swollen",
    "swalow": "swallow", "swallo": "swallow", "swollow": "swallow",
    "swaloed": "swallowed", "swalowed": "swallowed", "swalloed": "swallowed",
    "swollowed": "swallowed", "swalowing": "swallowing", "swalloing": "swallowing",
    "swollowing": "swallowing",
    "colapse": "collapse", "collpase": "collapse", "collaps": "collapse",
    "colapsed": "collapsed", "collapsd": "collapsed", "collapsesd": "collapsed",
    "colapsing": "collapsing",
    "chok": "choke", "chokng": "choking", "chocking": "choking",
    "chokeing": "choking", "chokking": "choking",
    "unconcious": "unconscious", "unconsious": "unconscious", "unconcius": "unconscious",
    "unconciuos": "unconscious", "unconscience": "unconscious", "unconcsious": "unconscious",
    "unresponsve": "unresponsive",
    "sezure": "seizure", "sezuire": "seizure", "seziure": "seizure", "sezire": "seizure",
    "siezure": "seizure", "seisures": "seizures", "sezures": "seizures",
    "overdos": "overdose", "overdosse": "overdose", "overdosd": "overdosed",
    "overdowsed": "overdosed", "overdosng": "overdosing",
    "bleding": "bleeding", "bleading": "bleeding", "bledding": "bleeding",
    "bleednig": "bleeding",
    "drownd": "drowned", "drownded": "drowned", "drowing": "drowning",
    "drownng": "drowning",
    "brething": "breathing", "breatheing": "breathing", "breathng": "breathing",
    "breahting": "breathing",
    "strok": "stroke", "stroks": "strokes", "vomitting": "vomiting",
    "vometing": "vomiting", "vomitng": "vomiting", "burnng": "burning",
    "bruning": "burning",
    "havin": "having", "chokin": "choking", "bleedin": "bleeding", "bledin": "bleeding",
    "swallowin": "swallowing", "breathin": "breathing", "drownin": "drowning",
    "overdosin": "overdosing", "collapsin": "collapsing", "vomitin": "vomiting",
    "burnin": "burning", "seizurin": "seizing",
    "breaht": "breath", "breth": "breath", "breathh": "breath",
    "burnet": "burnt", "burent": "burnt", "burntt": "burnt", "burnd": "burnt",
    "throt": "throat", "troath": "throat", "thraot": "throat",
    "tempreture": "temperature", "temperture": "temperature", "tempriture": "temperature",
    "temparature": "temperature", "tempurature": "temperature",
    "ancle": "ankle", "ankel": "ankle", "ankkle": "ankle",
    "fel": "fell", "faling": "falling",
}


CHAT.update({
    "yall": "you all", "kay": "ok", "okie": "ok", "thankyou": "thanks",
    "thanku": "thanks", "iono": "i do not know", "pic": "picture",
    "pics": "pictures", "rite": "right", "gunna": "going to", "gna": "going to",
    "gona": "going to", "cu": "see you",
    "gota": "got to",
    "tmr": "tomorrow", "l8r": "later", "rly": "really", "srsly": "seriously",
    "cnt": "can not", "hve": "have", "luv": "love", "lv": "love", "luvs": "loves",
    "wht": "what", "hw": "how", "hwo": "how", "wen": "when", "wens": "when",
    "wher": "where", "yr": "your", "urself": "yourself", "prolly": "probably",
    "mayb": "maybe", "sry": "sorry", "srry": "sorry", "nd": "and",
    "dat": "that", "dis": "this", "dem": "them", "dey": "they",
    "wif": "with", "widout": "without", "wiff": "with",
    "summin": "something", "sumthing": "something", "somet": "something",
    "summink": "something", "eny": "any", "enything": "anything",
    "woz": "was", "haz": "has", "ppls": "people's",
    "txt": "text", "txts": "texts",
    "presnt": "present",
    "wiv": "with", "abit": "a bit", "incase": "in case", "atleast": "at least",
    "eachother": "each other", "infront": "in front",
})

MISSPELLINGS.update({
    "evry": "every", "evrey": "every", "evryone": "everyone", "evrything": "everything",
    "agin": "again", "befor": "before", "agen": "again",
    "sory": "sorry", "skool": "school", "finaly": "finally", "famly": "family",
    "frends": "friends", "frend": "friend", "frendly": "friendly",
    "deposite": "deposit", "holliday": "holiday", "hollidays": "holidays",
    "muney": "money", "managment": "management", "bolognase": "bolognese",
    "similer": "similar", "genuinly": "genuinely", "basicly": "basically",
    "foriegn": "foreign", "quater": "quarter", "secound": "second",
    "surprized": "surprised", "toghether": "together", "yestarday": "yesterday",
    "vegtarian": "vegetarian", "brnded": "branded",
    "meens": "means",
    "meen": "mean", "meening": "meaning", "meent": "meant",
    "deos": "does", "suposed": "supposed", "supose": "suppose",
    "suposedly": "supposedly",
    "dos that": "does that", "dos it": "does it", "dos this": "does this",
    "dus that": "does that", "dus it mean": "does it mean",
    "dos the": "does the", "dos he": "does he", "dos she": "does she", "dos your": "does your",
})

JOINED_WORDS = {
    "fedup": "fed up", "sickof": "sick of", "tiredof": "tired of", "boredof": "bored of",
    "pissedoff": "pissed off", "cheesedoff": "cheesed off", "hadenough": "had enough",
    "shutup": "shut up", "growup": "grow up", "comeon": "come on", "goaway": "go away",
}

CHAT.update({
    "morngin": "morning", "mornging": "morning", "mornign": "morning",
    "mornin": "morning", "gud": "good", "gewd": "good",
    "alrite": "alright", "awrite": "alright", "awright": "alright", "aight": "alright",
    "thnaks": "thanks", "tahnks": "thanks", "thankz": "thanks", "cheerz": "thanks",
    "cheeers": "thanks", "wassup": "what is up", "sup": "what is up",
    "thks": "thanks", "thnx": "thanks", "thanx": "thanks", "thankx": "thanks",
    "tnx": "thanks", "tyty": "thanks", "tysm": "thanks", "10q": "thank you",
    "fankyou": "thank you", "fanku": "thank you", "fank you": "thank you",
    "howz": "how is", "hru": "how are you", "yoo": "hi",
    "yo": "hi", "hai": "hi", "hihi": "hi", "heyoo": "hey",
    "ideeas": "ideas", "ideea": "idea", "wt": "what", "wnt": "want",
    "m8": "mate", "m8s": "mates", "drs": "doctors", "bday": "birthday",
    "appt": "appointment", "appts": "appointments",
})

CHAT.update({
    "urt": "hurt", "urts": "hurts", "urting": "hurting", "urted": "hurt",
    "bort": "bought", "thort": "thought", "brort": "brought",
    "hu": "who",
})

CHAT.update({
    "werk": "work", "werks": "works", "werked": "worked", "werking": "working",
    "elp": "help", "elps": "helps", "elped": "helped", "elping": "helping",
    "reckn": "reckon", "reckns": "reckons", "recknd": "reckoned", "reckning": "reckoning",
})

DIALECT_STATES = {
    "ropey": "unwell", "ropy": "unwell", "hackit": "rough", "gubbed": "shattered",
    "scunnered": "fed up", "crabbit": "grumpy",
}
CHAT.update(DIALECT_STATES)

CHAT.update({
    "nxt": "next", "wk": "week", "wks": "weeks", "wknd": "weekend", "wknds": "weekends",
    "mth": "month", "mths": "months", "mnth": "month", "mnths": "months",
    "2moz": "tomorrow", "2mz": "tomorrow", "tmoz": "tomorrow", "2morro": "tomorrow",
    "yrs": "years", "hrs": "hours", "mins": "minutes", "secs": "seconds",
    "defo": "definitely", "shd": "should", "culd": "could", "spk": "speak",
    "tnite": "tonight", "tnight": "tonight", "tonyt": "tonight", "gna": "going to",
    "jst": "just", "ovr": "over", "abwt": "about", "bwt": "about",
    "skl": "school", "hol": "holiday", "hols": "holidays", "agen": "again",
    "forgetin": "forgetting", "forgettin": "forgetting",
})

CHAT.update({
    "ngl": "not going to lie", "wdym": "what do you mean", "wym": "what do you mean",
    "tbf": "to be fair",
    "in ages": "in a long time", "ages ago": "a long time ago",
    "been ages": "been a long time", "takes ages": "takes a long time",
    "took ages": "took a long time", "taking ages": "taking a long time",
    "ttyl": "talk to you later", "omw": "on my way", "fyi": "for your information",
    "gn": "good night", "gnite": "good night", "gnight": "good night", "gnyt": "good night",
    "buhbye": "bye", "buhbye now": "bye now", "nighto": "night",
    "peace out": "bye", "toodles": "bye",
    "nowt": "nothing", "aye": "yes", "l8ly": "lately", "slee": "sleep",
    "bairn": "child", "bairns": "children",
    "hv": "health visitor", "hvs": "health visitors",
    "wev": "we have", "av": "have",
    "shud": "should", "shld": "should", "wud": "would", "wuld": "would",
    "guna": "going to", "gona": "going to", "goina": "going to",
    "meself": "myself", "mesen": "myself", "me self": "myself",
})

EXPAND = {
    "dont": "do not", "doesnt": "does not", "didnt": "did not", "isnt": "is not",
    "arent": "are not", "wasnt": "was not", "werent": "were not", "cant": "can not",
    "couldnt": "could not", "shouldnt": "should not", "wouldnt": "would not",
    "wont": "will not", "havent": "have not", "hasnt": "has not", "hadnt": "had not",
    "mustnt": "must not", "neednt": "need not", "aint": "is not",
    "im": "i am", "ive": "i have",
    "youre": "you are", "youve": "you have", "youll": "you will", "youd": "you would",
    "theyre": "they are", "theyve": "they have", "theyll": "they will",
    "weve": "we have",
    "shes": "she is", "hes": "he is", "thats": "that is", "theres": "there is",
    "heres": "here is", "lets": "let us",
}

NEGATIONS = frozenset("not no never none nothing nobody neither nor cannot".split())

BACKGROUND_STARTS = frozenset("""when whenever while whilst after before since during until
    where wherever""".split())
START_VERBS = frozenset("""started starts began begins happening happened happens kicked
    comes came""".split())
PLACE_PREPS = frozenset("in at on near inside outside around from".split())
CLAUSE_BREAKS = frozenset("""and but so then now because cos if when while after before
    which that who whose""".split())

OPENERS = """
    what why when where who which whose how
    whats whys whens wheres whos hows
    hi hello hey hiya heya howdy morning evening
    thanks thankyou cheers
    bye goodbye cya
    can could should would will shall is are was were am do does did have has may might
"""

COMMON += """
appeal chance closer crisp depth polite pushy unfair wrinkly
"""

COMMON += """
basin shin
"""

COMMON += """
supper brunch pudding dessert pud afters nibbles elevenses brekkie brekky sarnie butty cuppa
takeout nosh grub chow kebab chippy munchies bap sanger bbq barbecue
"""

COMMON += """
desert deserts deserted deserting
"""

COMMON += """
hiya satay jerry kate preston unfit manic silly
"""

COMMON += """
hope sting freak shit crap cack brick puke barf throw
"""

COMMON += """
shitting crapping cacking
"""


COMMON += """
beat beats beating beaten blow blows blowing blown break breaks breaking broke broken
carry carries carried carrying catch catches catching caught choose chooses choosing chose
chosen climb climbs climbing climbed close closes closing closed decide decides deciding
decided die dies dying died dig digs digging dug draw draws drawing drew drawn drop drops
dropping dropped dry dries drying dried fit fits fitting fitted forget forgets forgetting
forgot forgotten forgive forgives forgiving forgave forgiven happen happens happening
happened hear hears hearing heard hide hides hiding hid hidden hit hits hitting hit hold
holds holding held hope hopes hoping hoped jump jumps jumping jumped kick kicks kicking
kicked laugh laughs laughing laughed leave leaves leaving left lend lends lending lent
listen listens listening listened lose loses losing lost
meet meets meeting met melt melts melting melted mend mends mending mended pull pulls
pulling pulled push pushes pushing pushed ride rides riding rode ridden rise rises rising
rose risen send sends sending sent shake shakes shaking shook shaken share shares sharing
shared shine shines shining shone shoot shoots shooting shot shut shuts shutting sit sits sitting sat slide slides sliding slid smell smells
smelling smelled smile smiles smiling smiled spin spins spinning spun stand stands standing
stood stay stays staying stayed steal steals stealing stole stolen stick sticks sticking
stuck taste tastes tasting tasted tear tears tearing tore torn throw throws throwing threw
thrown understand understands understanding understood visit visits visiting visited wear
wears wearing wore worn win wins winning won wipe wipes wiping wiped wish wishes wishing
wished wonder wonders wondering wondered
"""

COMMON += """
acting adopting affecting amazing annoying apologising applying attacking autocorrecting
avoiding barging barking basting bearing beeping begging blaming bloating blocking bookkeeping
borrowing breastfeeding breeding bubbling buffering bulging bullying bumping bunching bursting
buzzing camping challenging charging cheating chewing chirping chocking christening clanking
clawing clearing clicking clinging clunking clutching coding collapsing commenting comparing
conditioning connecting considering contesting coping covering cracking crackling cramming
crashing craving creaking creasing criticising crumbling crushing crystallising curling
decorating dehydrating depressing dimming dining dipping disappearing disconnecting distracting
dodging dragging draining dreading dribbling drifting drooping drowning dumping dumpling
escalating exhausting expecting fading failing fainting fattening filling firing flaking flaring
flickering flooding flowering flushing foaming fouling frosting funding gaining
gaslighting glazing grabbing grinding grovelling grunting gurgling handwriting hiking hiring
hopping hosting humming ignoring including interfering interrupting investing inviting juddering
knitting knocking leaning leasing licking lifting mentioning meowing merging messing mounting
mourning neutering nipping nitpicking offering ordering outgrowing overcharging overflowing
overhanging overheating overreacting overthinking panicking panting paving peeling piling
pinging pooling popping pouring pricking proofing proving punching queuing raging raising
rattling reassuring recycling redoing refusing renewing replaying replying rereading
rescheduling responding restructuring retaining returning ripening rolling rotting rounding
safeguarding sagging sanding scaffolding scarifying scoring scrambling scratching screaming
scrolling seething servicing serving sewing shaving signing simmering singing siting skiing
skipping slamming slipping slurring snapping sniffling snoozing sobbing sowing sparking spelling
spiralling spitting spreading sprouting squeaking squealing stalking stalling steaming steering
stifling stinking stocking strangling streaming submitting subtracting sucking swearing
switching syncing tangling tempting thickening threatening thumping tipping touching tracking
travelling twirling typing undermining updating upgrading uplifting upsetting wandering warning
wasting waterproofing weeping wetting wheezing wobbling wrapping wrecking wuthering yowling
"""


_DOUBLED_NOT_A_SLIP = """
bled butt cal canceling caper carers casein committed crispin desserts ding fibrin filing
latte
filings filling fillings finnish freeing hover hovering hovers lager latter leds ling losses
mealy moped moping mopped mopping munches noted noting notted notting oily painting paned
pilling planed planing pulsing putin putt queueing saladin sed stalin sumer teether tether
thee traveling travelling wed weds weeing
"""
NOT_A_FEELING = frozenset("""
aging bashed bused cress criss earful etched etching leased naked nappy sacred sagged sappy
scored staring tankful""".split())

REAL_WORDS = frozenset("""career careers dyeing singeing tingeing swingeing
nappy nappies fired""".split())

TYPED_WORDS = frozenset(_DOUBLED_NOT_A_SLIP.split())

REAL_IN = frozenset("""satin raisin basin cabin robin napkin muffin violin margin origin
protein pumpkin cousin resin ruin twin grin shin skin spin chin pin bin din fin gin kin sin
tin win within begin origin vitamin insulin aspirin gelatin tarragon gratin crispin saladin""".split())
LAUGHTER = frozenset("""lol lols lolz lul lulz lolol lololol lmao lmfao lmfaoo rofl roflmao
ha hah haha hahaa hahah hahaha hahahah hahahaha heh hehe heheh hehehe heheheh""".split())

TRAITS = frozenset("""lazy shy awkward clumsy forgetful impatient selfish greedy mean nasty
boring thick stupid dumb daft clueless useless worthless rubbish crap weak cowardly spineless
jealous moody annoying irritating ugly fat""".split())

A_DESCRIBING = frozenset("""quiet messy noisy picky fussy bossy stubborn rude spoilt chatty
negative positive tidy untidy nosy weird odd loud hard""".split())


def is_a_laugh(word):
    if word in NOT_A_LAUGH:
        return False
    if word in LAUGHTER:
        return True
    return bool((len(word) > 2 and _LAUGH_RUN.fullmatch(word)) or _H_RUN.fullmatch(word))


NOT_A_LAUGH = frozenset("huh halo helo hilo hola lolo lulu".split())

_LAUGH_RUN = re.compile(r"(?:ha|he|hi|ho|hu|l(?:ol)+)+")
_H_RUN = re.compile(r"h{2,}")

PLAIN_EXPANDS = frozenset("""cba cbf stomakaike wuu2 wu2 wuu wdyt wdym wym idk dunno seeya
    wanna wana wanne wannna wanta gona gonna gunna guna goina gna gotta gota
    lemme gimme kinda sorta outta owta hafta hasta tryna trynna
    coulda shoulda woulda musta
    shouldve whatre""".split())

PLAIN_ONE_WORD = frozenset("""tmrw tmw tmr tmoz 2moz 2mz 2moro 2mora 2morra 2morro 2morrow
    tmrow tmorro tomoz tomoro tommorow
    tday 2day todai""".split())

SAID_SHORT = {"u": "you", "ur": "your", "ya": "you", "r": "are"}

HANDOFF_LEADS = (
    "one more thing", "one more question", "one more q", "one more ask",
    "one last thing", "one last question", "one final thing",
    "another thing", "another question", "another one", "another ask",
    "the other thing", "one other thing", "the last thing", "the last question",
    "last thing", "last question", "the next thing", "next thing", "next question",
    "quick question", "quick one", "quick q", "a quick question", "a quick one",
    "a different question", "a different one", "a separate question", "an unrelated question",
    "one thing more", "a couple more things", "couple more questions", "two more things",
    "before i forget", "while im here", "while i am here",
)

HANDOFF_BRIDGES = ("about", "on", "re", "regarding", "concerning", "as for", "to do with")

BODY_PARTS = frozenset("""back neck head shoulder shoulders arm arms elbow wrist wrist hand hands
finger fingers thumb thumb chest rib ribs stomach tummy belly knee knees leg legs ankle foot feet
heel hip hips jaw tooth teeth ear ears eye eyes muscle muscles skin
throat nose gut waist spine lung lungs
shin shins thigh thighs calf calves toe toes
mouth tongue gum gums lip lips cheek cheeks chin forehead temple temples armpit groin
palm palms bum
""".split())
PAIN_WORDS = frozenset("""hurt hurts hurting ache aches aching sore painful pain agony killing
throbbing stinging stiff swollen swelling numb cramp cramped burning pins needle
pounding thumping splitting""".split())
CONFUSIONS = {
    "looser": "loser", "loosing": "losing",
}
CONFUSIONS_AFTER = {
    "loose": ("lose", frozenset("""to dont didnt doesnt wont wouldnt cant cannot couldnt
shouldnt gonna gotta want wants wanted try trying tried need needs needed plan planning
help helps helped""".split())),
    "breath": ("breathe", frozenset("""to cant cannot couldnt can hard struggling struggle
need needs needed try trying tried forget forgets forgot remember remembers learn learnt""".split())),
    "dos": ("does", frozenset("what how why when where who which".split())),
}
CONFUSIONS_BEFORE = {
    "quite": ("quiet", frozenset("in at on for tonight today now please here there inside".split())),
}
CONFUSIONS_IN_A_FEELING = {
    "board": ("bored", frozenset("""all of with at because cause cuz so and but when that today
tonight lately atm rn tbh now again too already most there bit""".split())),
}
FEELING_FILLER = frozenset("""so really very proper quite well bit kinda kind of that too
pretty much totally absolutely well""".split())
FEELING_LEAD = frozenset("""im i'm iam am feel feels feeling felt getting being""".split())
CONFUSIONS_BEFORE_A_QUESTION = {"no": "know"}
QUESTION_WORDS = frozenset("when how why what if whether where who which".split())


_ENGINE_WORDS = None


def every_word():
    global _ENGINE_WORDS
    if _ENGINE_WORDS is not None:
        return _ENGINE_WORDS
    from . import body, kinds, topics
    tables = (globals(), vars(topics), vars(kinds), vars(body))
    words = set()
    for table in tables:
        for name, value in table.items():
            if name.startswith("_") or "MISSPELLING" in name:
                continue
            if isinstance(value, (frozenset, set, tuple, list)):
                items = value
            elif isinstance(value, dict):
                items = list(value)
            else:
                continue
            for item in items:
                if not isinstance(item, str):
                    continue
                for word in item.lower().replace(",", " ").split():
                    if word.isalpha():
                        words.add(word)
    _ENGINE_WORDS = frozenset(words)
    return _ENGINE_WORDS
