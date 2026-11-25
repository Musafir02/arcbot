
import re

from .lookup import entry

ANSWERS = ("creative", "language-and-writing")


def _story(memory, understood):
    return ("Build it from a want, a wall and a turn: what the character wants in the first "
            "scene, what stops them, and the one thing that changes the plan. A plot that sounds "
            "far-fetched is usually missing the practical steps - the key, the alibi, the person "
            "who noticed - so make the method vague and the aftermath exact: the cup half drunk, "
            "the dog still alive, the wrong person blamed. If you want a villain's plan to be "
            "believable, give them one small mistake a careful reader could spot on a second "
            "read, and let a minor character be the one who spots it.")


def _prose(memory, understood):
    return ("Cut the adverbs and put one thing a reader can see in every paragraph: not 'the "
            "kitchen was messy' but 'the bin was full of cereal boxes'. Then vary the sentence "
            "length - short where it is tense, longer where it is calm - and read it aloud, "
            "because the sentence you stumble on is the one to fix. That is three passes, and "
            "they fix most flat writing.")


def _naming(memory, understood):
    return ("Name the thing, not the idea: a bakery called Crust, a cafe called The Second Cup, "
            "a band called The Rosy Hours. Two short words joined - place plus trade, your own "
            "name plus what you sell - beats anything clever, because people have to say it out "
            "loud and spell it down a phone. Say it with 'I'm just going to' in front of it, check "
            "that the domain and the social handle are free before you fall in love with it, and "
            "check Companies House for the limited company: a name can be yours to trade under "
            "and still be taken as a company.")


_THE_METHOD = (
    "Ordinary clothes plus one big shape, and nothing to sew: a black hoodie with ears on a "
    "headband is a cat, a cardboard box is a robot, a dressing gown and a towel round the head is "
    "a shepherd. Hats, ears and face paint do more than the outfit, and one prop - a cardboard "
    "sword, a wooden spoon, a stack of books - tells everyone who it is meant to be.")

_COSTUME_TIPS = (
    (("world book day", "book day", "book character", "book week", "world book"),
     "For World Book Day pick a character who wears normal clothes - Matilda with a stack of "
     "books, the Worst Witch in school uniform, the Tiger Who Came to Tea with whiskers of face "
     "paint - because the book under the arm does the rest of the work."),
    (("nativity", "shepherd", "shepherds", "wise man", "angel", "angels"),
     "A shepherd is a dressing gown, a towel round the head and a tea towel for a belt; an angel "
     "is white clothes, wings bent out of wire coat hangers and tights, and tinsel on a headband "
     "for a halo."),
    (("pirate", "pirates"),
     "Pirate: a striped top, a scarf knotted as a bandana, an eye patch cut from card, and a sword "
     "of rolled card or a wooden spoon."),
    (("superhero", "superheroes", "super hero", "cape", "batman", "spiderman", "spider man"),
     "Superhero: a plain t-shirt with a paper logo taped on, leggings, and a cape cut from an old "
     "sheet pinned at the shoulders - pinned, never tied round the neck."),
    (("witch", "witches", "wizard", "harry potter"),
     "Witch: black clothes, a cone of card for a hat, and a broom of a stick and a bundle of straw."),
    (("dinosaur", "dinosaurs", "dragon", "dragons"),
     "Dinosaur: a hoodie with triangles of paper or felt down the back of the hood, and a tail "
     "pinned to the trousers."),
    (("robot", "robots", "astronaut", "spaceman"),
     "Robot: a box over the head with eye holes cut out, foil taped on the arms and legs, and "
     "bottle tops glued on for buttons."),
    (("cat", "cats", "dog", "dogs", "mouse", "bunny", "rabbit", "animal", "animals"),
     "Cat or dog: black or brown clothes, ears cut from card on a headband, and whiskers in face "
     "paint."),
    (("princess", "princesses", "fairy", "fairies"),
     "Princess or fairy: a long dress or a sheet, a crown of card and foil, and a sash of ribbon."),
    (("cowboy", "cowgirl", "indian", "sheriff"),
     "Cowboy: jeans, a checked shirt, a scarf at the neck, and a hat of card with a brim."),
    (("skeleton", "ghost", "zombie"),
     "Skeleton: black clothes with bones painted on in white face paint, or cut from paper and "
     "pinned on."),
)


def _costume_word(line):
    for words, tip in _COSTUME_TIPS:
        for word in words:
            if re.search(r"\b" + re.escape(word) + r"\b", line):
                return tip
    return ""


_COSTUME_MAKING = re.compile(
    r"\b(?:costumes?|fancy dress|dress(?:ed)? (?:up|as)|dressing up|outfits?|"
    r"make|makes|making|made|diy|sew|sewing|sewn|put together|throw together|improvise|"
    r"knock up|out of|ideas?|go(?:es|ing)? as|want(?:s)? to be|be a|wear|wearing|need|needs|"
    r"provide|ourselves|myself|cheap|cheaply|easy|last minute|no sewing)\b", re.I)


def _making_a_costume(understood):
    line = (understood or {}).get("clean") or (understood or {}).get("text") or ""
    return bool(_COSTUME_MAKING.search(str(line)))


def _a_costume(memory, understood):
    line = str(understood.get("clean") or understood.get("text") or "").lower()
    tip = _costume_word(line)
    if tip:
        return _THE_METHOD + " " + tip
    return _THE_METHOD


ENTRIES = [
    entry("story-craft",
          (("story", "stories", "plot", "novel", "script", "screenplay", "character", "fiction",
            "villain", "chapter"),
           ("stuck", "idea", "ideas", "start", "where do i start", "believable", "realistic",
            "convincing", "plot", "plan", "help me", "help", "how do i write", "what should",
            "make it work", "going nowhere")),
          _story, bias=1,
          avoid=("write me a story", "write us a story", "tell me a story", "make up a story",
                 "read next", "recommend", "suggest", "should i read", "to read", "book for",
                 "gift", "present", "book club", "audio book", "audiobook")),
    entry("make-writing-better",
          (("writing", "prose", "description", "paragraph", "paragraphs", "draft", "blog post"),
           ("boring", "flat", "dull", "better", "improve", "punchier", "livelier", "read better",
            "less boring", "more interesting", "tighten", "bland")),
          _prose, bias=1,
          avoid=("handwriting", "smaller", "neater", "pen", "spelling", "grammar", "font",
                 "size")),

    entry("name-a-business",
          (("name", "names", "naming", "call it", "called", "what to call"),
           ("business", "shop", "bakery", "cafe", "caf", "restaurant", "company", "brand",
            "team", "podcast", "blog", "stall", "startup", "start up", "etsy", "pub",
            "salon", "studio", "brand name", "small business", "side hustle", "market stall",
            "youtube channel", "newsletter")),
          _naming, bias=1,
          avoid=("puppy", "kitten", "dog", "cat", "hamster", "rabbit", "guinea", "parrot",
                 "budgie", "horse", "pony", "tortoise", "baby", "baby name", "baby names",
                 "what is it called", "whats it called", "what is the name of", "called again"),
          ask=("suggest", "suggestion", "suggestions", "ideas", "idea", "any", "good",
               "help me", "come up with", "think of", "what should i", "what could i",
               "what would you", "how do i name", "name for", "name ideas", "pick a name",
               "choose a name", "shortlist")),

    entry("a-costume-at-home",
          (("costume", "costumes", "fancy dress", "outfit", "dressing up", "dress up box",
            "world book day", "book day", "book character", "book week", "nativity",
            "school play", "halloween", "party costume",
            "pirate", "pirates", "superhero", "superheroes", "cape", "angel", "shepherd",
            "witch", "wizard", "dinosaur", "robot", "princess", "cowboy", "skeleton"),
           ("make", "makes", "making", "made", "diy", "sew", "sewing", "put together",
            "throw together", "improvise", "knock up", "out of", "from what we have",
            "from what i have", "what can i", "what should", "what do i", "how do i",
            "how can i", "go as", "goes as", "going as", "dress as", "dressed as", "ideas", "idea",
            "want to be", "wants to be", "be a", "provide", "ourselves", "myself", "need",
            "easy", "cheap", "last minute", "no sewing")),
          _a_costume, bias=1, guard=_making_a_costume,
          avoid=("swimming", "swimsuit", "swimwear", "bikini", "trunks", "wetsuit",
                 "pool", "chlorine", "wash", "washing", "clean", "stain", "stains", "smell",
                 "smells", "smelly", "iron", "ironing", "mend", "repair", "alter", "tailor",
                 "hire", "hiring", "rent", "rental", "buy", "buying", "shop", "online",
                 "amazon", "where can i get", "where to buy", "sale", "price", "cost",
                 "cake", "cakes", "cupcake", "bake", "baking", "sandwich", "party food",
                 "trick or treat", "sweets", "balloons", "bunting", "decorations",
                 "present", "gift", "what to wear to", "activities", "things to do", "party games",
                 "trick or treating", "carve", "pumpkin")),
]
