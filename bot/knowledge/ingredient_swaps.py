from .lookup import entry

ANSWERS = ("cooking", "food-and-drink")

SWAP_ASK = ("instead", "substitute", "swap", "replace", "alternative", "what can i use",
            "what do i use", "what should i use", "what else can i use", "use in place of",
            "stand-in", "stand in")
OUT_ASK = ("out of", "ran out", "run out", "none left", "nothing left",
           "havent got", "haven't got", "dont have", "don't have",
           "no sugar", "no flour", "no honey", "no icing sugar", "no caster sugar",
           "no plain flour", "no sugar left", "no flour left", "no honey left")
ASK = SWAP_ASK + OUT_ASK

NOT_A_DIET = ("cut down", "cut out", "give up", "less sugar", "reduce", "diet", "dieting",
              "calories", "sweets", "sweets and", "biscuits", "chocolate", "cravings", "crave",
              "stop eating", "healthy", "healthier", "lose weight",
              "cut sugar", "cut the sugar", "cutting sugar", "add sugar", "no idea",
              "in my coffee", "in my tea", "take no sugar", "takes no sugar")
HONEY_COMES_IN = ("use honey", "using honey", "honey instead", "honey rather")
NOT_A_SWAP = ("difference", "different", "same as", "vs", "versus", "better for you",
              "gone hard", "set hard", "hard as", "lumpy", "caked", "clumped", "goes hard",
              "go hard", "how do i store", "keep it soft", "storing",
              "burnt", "burned", "burnt on", "stuck on", "stuck to", "scorched", "charred",
              "clean""out of date", "use by", "use-by", "past its date", "past the date", "best before",
              "gone past")