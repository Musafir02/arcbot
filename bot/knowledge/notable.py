from .lookup import entry

ANSWERS = ("entertainment", "geography-and-travel", "history")

ENTRIES = []


def _row(*args, **kwargs):
    ENTRIES.append(entry(*args, **kwargs))

WHO = ("who", "who's", "whos", "current", "still", "now", "today", "name", "is",
       "at the moment", "at the minute")

CAST = ("who plays", "who play", "who played", "who's playing", "whos playing", "who is playing",
        "who was playing", "who starred", "who stars", "who voices", "who does the voice",
        "who was the voice", "the actor who", "the actor that", "actor who plays", "that plays",
        "which actor", "which actress", "name the actor", "tell me the actor", "the guy who plays",
        "the girl who plays", "the woman who plays", "the man who plays", "played by",
        "cast of", "the cast", "who was in", "who is in", "starring", "starred in",
        "actor", "actress")

OTHER_PLACES = tuple(
    "india indian china chinese japan japanese russia russian ukraine ukrainian france french "
    "germany german spain spanish italy italian portugal portuguese greece greek ireland irish "
    "canada canadian australia australian new zealand brazil brazilian mexico mexican "
    "south africa israel israeli iran iranian iraq syria syrian turkey turkish egypt egyptian "
    "saudi saudi arabia pakistan pakistani bangladesh nigeria kenya ghana netherlands dutch "
    "holland belgium belgian sweden swedish norway norwegian denmark danish finland finnish "
    "poland polish hungary austria austrian switzerland swiss argentina chile colombia peru "
    "cuba cuban indonesia philippines vietnam thailand thai malaysia singapore hong korea "
    "korean taiwan afghanistan lebanon palestine morocco ethiopia somalia sudan zimbabwe qatar "
    "dubai emirates czech romania bulgaria croatia serbia lithuania latvia estonia slovakia "
    "slovenia iceland luxembourg malta cyprus".split())

CROWD = ("population", "people live", "many people", "many people live", "inhabitants",
         "how big is", "big is")


_row("uk-prime-minister", (("prime minister", "the pm", "uk pm", "british pm", "pm"), WHO),
      "Keir Starmer is the prime minister - Labour, in office since July 2024, when his party won "
      "the general election. The next one has to be held by August 2029.",
      bias=2,
      avoid=("first", "walpole", "churchill", "thatcher", "blair", "was", "did", "history",
             "ww2", "war",
             "my office", "our office", "office manager", "workplace", "at work", "my company",
             "our company", "my team", "our team", "tenants", "residents", "association",
             "committee") + OTHER_PLACES)

_row("uk-monarch", (("king", "queen", "monarch", "royal family"), WHO),
      "Charles III is the king: he became monarch in September 2022, when Elizabeth II died. "
      "Camilla is queen, and the heir is Prince William.",
      bias=2,
      avoid=("chess", "check", "bed", "size", "size bed", "burger", "lion", "prawn",
             "prawns", "card", "cards", "poker", "hearts", "spades", "drag", "prom", "band",
             "bohemian", "bee", "bees", "henry", "victoria", "elizabeth", "tudor", "cleopatra",
             "arthur", "luther", "stephen", "bb", "awards", "speech", "xmas speech",
             "king of the", "queen of the",
             "first", "athelstan", "first king",
             "spaniel", "cavalier", "king charles spaniel", "dog", "dogs", "puppy",
             "my king", "our king", "my queen", "our queen", "pub", "hotel") + OTHER_PLACES)

_row("us-president", (("president", "potus", "us president", "american president",
                       "president of the united states", "president of america", "us president"), WHO),
      "Donald Trump is the US president: he took office in January 2025 for a second term, after "
      "beating Kamala Harris in November 2024. JD Vance is vice president. A president serves "
      "four years and can be elected twice.",
      bias=1,
      avoid=("vice", "club", "society", "company", "union", "student", "board", "obama",
             "biden", "lincoln", "kennedy", "washington", "assassinated", "election",
             "elections", "who won", "vote",
             "my tenants", "tenants", "residents", "association", "committee", "my office",
             "our office", "office manager", "workplace", "at work", "my company", "our company",
             "my club", "our club", "golf", "darts", "pigeon", "tenants association",
             "commission", "council", "court", "european") + OTHER_PLACES)

_row("us-vice-president", (("vice president", "vp"), WHO),
      "JD Vance is the US vice president, sworn in in January 2025 alongside Donald Trump. The "
      "job is to take over if the president cannot serve, and to break ties in the Senate.",
      bias=3,
      avoid=OTHER_PLACES)

_row("uk-chancellor", (("chancellor", "exchequer"), WHO),
      "Rachel Reeves is the chancellor of the exchequer - Labour, in office since July 2024, and "
      "the first woman to hold the job. The chancellor writes the budget and sets the tax rules.",
      bias=2,
      avoid=("university", "german", "germany", "berlin", "merkel", "scholz", "merz", "court",
             "vice chancellor", "degree", "graduation") + OTHER_PLACES)

_row("scotland-first-minister", (("first minister", "fm", "prime minister", "pm", "leader"),
                                ("scotland", "scottish", "holyrood", "snp", "swinney", "sturgeon")),
      "John Swinney is Scotland's first minister - SNP, in office since May 2024, when Humza "
      "Yousaf resigned. The Scottish parliament sits at Holyrood in Edinburgh.",
      bias=2,
      avoid=("northern ireland", "wales", "welsh") + OTHER_PLACES)

_row("wales-first-minister", (("first minister", "fm"), ("wales", "welsh", "senedd", "morgan")),
      "Eluned Morgan is Wales's first minister - Labour, in office since August 2024, and the "
      "first woman to hold the job. The Welsh parliament is the Senedd, in Cardiff Bay.",
      bias=2,
      avoid=OTHER_PLACES)

_row("ni-first-minister", (("first minister", "fm"), ("northern ireland", "ni", "stormont",
                                                          "oneill", "oneil", "sinn fein")),
      "Michelle O'Neill is Northern Ireland's first minister - Sinn Féin, in office since "
      "February 2024, with Emma Little-Pengelly of the DUP as deputy first minister. The two "
      "jobs are always held by the two biggest parties.",
      bias=2,
      avoid=tuple(word for word in OTHER_PLACES
                  if word not in ("ireland", "irish", "iceland")))

_row("first-minister-which", (("first minister",), WHO), bias=0,
     ask=("who", "who's", "whos", "current", "still", "now", "which", "name", "is"),
     reply="There are three. Scotland's is John Swinney (SNP), Wales's is Eluned Morgan "
           "(Labour), and Northern Ireland's is Michelle O'Neill (Sinn Féin), with Emma "
           "Little-Pengelly as deputy. Which one did you mean?",
     avoid=("scotland", "scottish", "wales", "welsh", "northern ireland", "stormont",
            "senedd", "holyrood"))

_row("home-secretary", (("home secretary",), WHO),
      "Yvette Cooper is the home secretary - Labour, in office since July 2024. The Home Office "
      "covers the police, the borders, immigration and passports.",
      bias=2,
      avoid=OTHER_PLACES)

_row("london-mayor", (("mayor of london", "london mayor"), WHO),
      "Sadiq Khan is the mayor of London: first elected in 2016 and re-elected in May 2024. The "
      "job covers transport, policing and planning for the whole of London.",
      bias=3,
      avoid=OTHER_PLACES)

_row("pope", (("pope", "pontiff"), WHO),
      "Leo XIV is the pope: elected in May 2025 and taking the name Leo XIV, after Francis. He "
      "was Cardinal Robert Prevost, and he is the first pope from the United States.",
      bias=2,
      avoid=("said", "quote", "hat", "costume", "fancy dress", "card", "who was",
             "worth", "days", "enough", "visit", "visiting", "tour", "trip", "open", "hours",
             "long", "tickets", "museum", "museums", "basilica", "sistine", "sightseeing",
             "whole day"))


_row("plays-iron-man", (("iron man", "tony stark"), CAST),
      "Robert Downey Jr plays Tony Stark: Iron Man (2008) through Avengers: Endgame (2019). He "
      "started the Marvel film run and was in nine of them.",
      bias=3,
      avoid=("costume", "suit", "make", "made", "draw", "wrote", "comic", "toy"))

_row("plays-batman", (("batman", "bruce wayne", "dark knight"), CAST),
      "Robert Pattinson plays Batman in The Batman (2022). Before him: Christian Bale in the Dark "
      "Knight trilogy (2005-2012), Ben Affleck in the two Justice League-era films, and Michael "
      "Keaton in 1989 and 1992.",
      bias=3,
      avoid=("costume", "suit", "make", "draw", "wrote", "comic", "toy", "cartoon", "lego",
             "dark knight rises", "batman begins", "the dark knight", "christian bale", "bale",
             "trilogy", "2008", "2012", "2005"))

_row("plays-batman-dark-knight",
     (("batman", "bruce wayne", "dark knight", "batman begins"),
      ("dark knight", "dark knight rises", "batman begins")),
      "Christian Bale plays Batman in the Dark Knight trilogy: Batman Begins (2005), The Dark "
      "Knight (2008) and The Dark Knight Rises (2012). Heath Ledger played the Joker in The Dark "
      "Knight, and Tom Hardy played Bane.",
      bias=6,
      ask=("dark knight", "dark knight rises", "batman begins", "bale", "trilogy", "2008",
           "2012", "2005"),
      avoid=("costume", "suit", "make", "draw", "wrote", "comic", "toy", "cartoon", "lego",
             "joker", "who plays the joker", "bane", "heath ledger"))

_row("plays-thor", (("thor",), CAST),
      "Chris Hemsworth plays Thor, from Thor (2011) to Thor: Love and Thunder (2022).",
      bias=3,
      avoid=("costume", "hammer", "norse", "myth", "god of thunder", "wrote", "comic"))

_row("plays-captain-america", (("captain america",), CAST),
      "Chris Evans plays Captain America: The First Avenger (2011) through Avengers: Endgame "
      "(2019).",
      bias=3,
      avoid=("costume", "make", "draw", "wrote", "comic"))

_row("plays-spider-man", (("spider man", "spiderman", "peter parker"), CAST),
      "Tom Holland plays Spider-Man in the three Home films (2017-2021). Andrew Garfield did the "
      "two Amazing Spider-Man films, and Tobey Maguire the three before those.",
      bias=3,
      avoid=("costume", "make", "draw", "wrote", "comic", "spider in my", "bite"))

_row("plays-wonder-woman", (("wonder woman", "diana prince"), CAST),
      "Gal Gadot plays Wonder Woman: Batman v Superman (2016), her own film in 2017, and 1984 in "
      "2020.",
      bias=3)

_row("plays-harry-potter", (("harry potter",), CAST),
      "Daniel Radcliffe plays Harry Potter in all eight films (2001-2011). He was eleven when the "
      "first one was shot and twenty-one by the last.",
      bias=4,
      avoid=("wrote", "written", "author", "book", "books", "read", "reading", "rowling",
             "snape", "severus", "hermione", "granger", "hagrid", "dumbledore", "malfoy",
             "draco", "voldemort", "dobby", "mcgonagall", "weasley", "ron", "ginny",
             "professor"))

_row("plays-sherlock", (("sherlock", "holmes"), CAST),
      "Benedict Cumberbatch plays Sherlock Holmes in the BBC series (2010-2017), with Martin "
      "Freeman as Watson. Robert Downey Jr played him in the two Guy Ritchie films, and Jeremy "
      "Brett in the 1980s series.",
      bias=4,
      avoid=("wrote", "written", "author", "book", "books", "read", "reading", "doyle",
             "stories"))

_row("plays-james-bond", (("james bond", "007"), CAST),
      "Daniel Craig played James Bond in five films, Casino Royale (2006) to No Time to Die "
      "(2021). The next Bond has not been announced. Before Craig: Pierce Brosnan, Timothy "
      "Dalton, Roger Moore, George Lazenby and Sean Connery.",
      bias=3,
      avoid=("wrote", "author", "book", "books", "ian fleming", "fleming", "car", "watch"))

_row("plays-dumbledore", (("dumbledore",), CAST),
      "Michael Gambon played Dumbledore in six of the eight Harry Potter films, taking over from "
      "Richard Harris, who died after the second. Jude Law plays him young in the Fantastic "
      "Beasts films.",
      bias=3,
      avoid=("wrote", "author", "book", "books", "dumbledore quote", "said"))

_row("plays-doctor-who", (("doctor who", "the doctor"), CAST),
      "Ncuti Gatwa plays the Doctor, from the 2023 Christmas special on. Before him: Jodie "
      "Whitaker, Peter Capaldi, Matt Smith, David Tennant and Christopher Eccleston since the "
      "series came back in 2005.",
      bias=3,
      avoid=("watch", "wrote", "author", "book", "episode order", "start"))

_row("plays-shrek", (("shrek",), CAST),
      "Mike Myers voices Shrek, with Eddie Murphy as Donkey and Cameron Diaz as Fiona, in the four "
      "films from 2001 to 2010.",
      bias=3)

_row("plays-joker", (("joker",), CAST),
      "Joaquin Phoenix plays the Joker in Joker (2019) and Folie a Deux (2024). Heath Ledger did "
      "it in The Dark Knight (2008), Jack Nicholson in 1989 and Jared Leto in Suicide Squad.",
      bias=3,
      avoid=("card", "cards", "joke", "pun", "costume"))


_row("plays-wednesday", (("wednesday addams", "wednesday"), CAST),
     "Jenna Ortega plays Wednesday Addams in Wednesday (2022), the Netflix series. Christina "
     "Ricci, who was Wednesday in the two 1990s films, plays her mother in it.",
     bias=3,
     avoid=("day", "days", "lunch", "dinner", "off", "bank holiday", "week", "on tv",
            "whats on", "tonight", "night", "listings", "channel", "ash wednesday", "wrote",
            "book"))

_row("plays-eleven", (("eleven", "stranger things"), CAST),
     "Millie Bobby Brown plays Eleven in Stranger Things (2016-2025).",
     bias=3,
     avoid=("number", "count", "counting", "wrote", "book"))

_row("plays-gollum", (("gollum", "smeagol", "lord of the rings"), CAST),
     "Andy Serkis plays Gollum: the voice and the motion capture in The Lord of the Rings and The "
     "Hobbit films. He also second-unit directed parts of the Hobbit trilogy.",
     bias=2,
     avoid=("wrote", "book", "books", "tolkien", "read"))

_row("plays-jack-sparrow", (("jack sparrow", "pirates of the caribbean"), CAST),
     "Johnny Depp plays Jack Sparrow, in all five Pirates of the Caribbean films (2003-2017).",
     bias=3)

_row("plays-katniss", (("katniss", "hunger games"), CAST),
     "Jennifer Lawrence plays Katniss Everdeen in the four Hunger Games films (2012-2015).",
     bias=3,
     avoid=("wrote", "book", "books", "read"))

_row("plays-neo", (("neo", "the matrix"), CAST),
     "Keanu Reeves plays Neo in The Matrix (1999) and its three sequels, and again in Resurrections "
     "(2021).",
     bias=3)

_row("plays-harley-quinn", (("harley quinn",), CAST),
     "Margot Robbie plays Harley Quinn in Suicide Squad (2016), Birds of Prey (2020) and The "
     "Suicide Squad (2021). Lady Gaga plays her in Joker: Folie a Deux.",
     bias=3,
     avoid=("costume", "make up", "costume make up", "wrote", "comic", "cartoon"))

_row("plays-john-wick", (("john wick",), CAST),
     "Keanu Reeves plays John Wick, in all four films (2014-2023).",
     bias=3)

_row("plays-elsa", (("elsa", "frozen"),
                    CAST + ("from",
                            "song", "songs", "sing", "sings", "sang", "soundtrack",
                            "come out", "came out", "release", "released", "when did",
                            "suitable for", "ok for", "scary", "3 year old", "4 year old",
                            "5 year old", "toddler", "sequel", "plot", "about", "ending")),
     "Idina Menzel is the voice of Elsa in Frozen (2013) and Frozen 2 (2019) and sings Let It Go; "
     "Kristen Bell is Anna. Both films are U certificates of about 100 minutes, so they are fine "
     "for a three year old - the ice monster in the first one is the only bit that frightens some "
     "small children.",
     bias=3,
    avoid=("frozen food", "freezer", "wrote", "book",
            "cook", "cooking", "cooked", "roast", "roasted", "oven", "fry", "fried", "bake",
            "baked", "grill", "microwave", "air fryer", "slow cooker", "defrost", "defrosted",
            "thaw", "thawed", "still frozen", "cook from frozen", "cooked from frozen",
            "cooking from frozen", "roast from frozen", "straight from frozen",
            "chicken", "turkey", "duck", "meat", "beef", "pork", "lamb", "fish", "salmon",
            "cod", "prawn", "prawns", "shrimp", "sausage", "sausages", "mince", "chop", "chops",
            "turkey", "bacon", "joint", "steak", "steaks", "liver", "kidneys",
            "chips", "peas", "veg", "vegetables", "spinach", "berries", "fruit", "bread",
            "rolls", "pastry", "pizza", "lasagne", "curry", "rice", "pie", "raw", "eat",
            "eaten", "edible",
            "yoghurt", "yogurt", "ice cream", "ice lolly", "shoulder", "freezer", "ice",
            "fish fingers", "pudding", "dessert", "smoothie", "berries"))

_row("plays-hermione", (("hermione", "granger"), CAST),
     "Emma Watson plays Hermione Granger in all eight Harry Potter films (2001-2011).",
     bias=3,
     avoid=("wrote", "book", "books", "rowling"))

_row("plays-ron", (("ron", "rupert grint", "weasley"), CAST),
     "Rupert Grint plays Ron Weasley in all eight Harry Potter films (2001-2011).",
     bias=3,
     avoid=("wrote", "book", "books", "rowling", "ronaldo", "ronan", "ronnie", "veronica"))

_row("plays-snape", (("snape", "severus"), CAST),
     "Alan Rickman plays Severus Snape in all eight Harry Potter films (2001-2011).",
     bias=3,
     avoid=("wrote", "book", "books", "rowling"))

_row("plays-homer-simpson", (("homer simpson", "the simpsons"), CAST),
     "Dan Castellaneta voices Homer Simpson, and has since the first short in 1987 - he also does "
     "Grampa, Krusty and Barney.",
     bias=4,
     avoid=("odyssey", "iliad", "greek", "poet", "wrote"))

_row("plays-geralt", (("geralt", "the witcher"), CAST),
     "Henry Cavill plays Geralt in the first three series of The Witcher (2019-2023); Liam "
     "Hemsworth took the part from series four.",
     bias=3,
     avoid=("wrote", "book", "books", "read", "game"))

CITIES = {
    "london": "London has about 8.9 million people, and about 14 million in the wider area "
              "around it. It is the biggest city in the UK by a long way - Birmingham, the "
              "second, has about 1.1 million.",
    "manchester": "Manchester itself has about 550,000 people; Greater Manchester, the whole "
                  "cluster of towns around it, has about 2.9 million.",
    "birmingham": "Birmingham has about 1.15 million people, which makes it the second biggest "
                  "city in the UK after London.",
    "leeds": "Leeds has about 810,000 people, the biggest of the Yorkshire cities.",
    "glasgow": "Glasgow has about 635,000 people, and about 1.7 million in the wider Clyde "
               "valley. It is Scotland's biggest city.",
    "edinburgh": "Edinburgh has about 510,000 people - smaller than Glasgow, though it is the "
                 "capital, and the festival more than doubles it in August.",
    "cardiff": "Cardiff has about 370,000 people, and about 1.1 million in the wider south "
               "Wales area.",
    "belfast": "Belfast has about 350,000 people, and about 670,000 in the wider area.",
    "new york": "New York City has about 8.3 million people - 8.3 million in the five "
                "boroughs, and around 19 million in the metro area. It is the biggest city in "
                "the United States.",
    "paris": "Paris has about 2.1 million people inside the city limits, and about 11 million in "
             "the whole metro area - the city proper is small, and the suburbs are where most "
             "Parisians live.",
    "tokyo": "Tokyo has about 14 million people in the city, and about 37 million in the wider "
             "metro area, which makes it the biggest in the world.",
    "sydney": "Sydney has about 5.3 million people, the biggest city in Australia.",
    "berlin": "Berlin has about 3.8 million people, the biggest city in Germany and about eight "
              "times the size of Frankfurt.",
    "dublin": "Dublin has about 590,000 in the city and about 1.5 million in the county, which is "
              "roughly a third of the people in Ireland.",
}

for _city, _fact in CITIES.items():
    _row(
        f"population-{_city.replace(' ', '-')}", (_city, CROWD), _fact,
        avoid=("serve", "serves", "serving", "recipe", "dinner", "cook", "feed", "portions",
               "guests", "how many people for"))
del _city, _fact


_row("eu-commission-president", (("president of the european commission",
                                  "european commission", "eu commission", "brussels",
                                  "president of the eu", "eu president"), WHO),
      "Ursula von der Leyen is the president of the European Commission: in office since "
      "December 2019, and given a second five-year term from December 2024 after the European "
      "elections in June. The commission proposes EU law; the parliament and the member states' "
      "governments pass it.",
      bias=2,
      avoid=("club", "society", "company", "union", "student", "board", "golf", "council",
             "court", "charity"))


LEADER_WORDS = ("president", "prime minister", "pm", "chancellor", "leader", "taoiseach",
                "king", "queen", "monarch", "head of state", "first minister", "emperor",
                "supreme leader", "general secretary", "in charge", "runs the country",
                "running the country", "who leads", "government")

LEADERS = {
    "france": (("france", "french"),
               "Emmanuel Macron is the president of France: elected in 2017 and re-elected in "
               "2022. A French president serves five years, so the next election is due in 2027, "
               "and the prime minister, who runs the day-to-day government, is appointed by the "
               "president."),
    "germany": (("germany", "german"),
                "Friedrich Merz is the chancellor of Germany: in office since May 2025, after his "
                "CDU/CSU bloc won the February 2025 election. The president, whose job is mostly "
                "ceremonial, is Frank-Walter Steinmeier."),
    "italy": (("italy", "italian"),
              "Giorgia Meloni is the prime minister of Italy: in office since October 2022, "
              "leading a coalition built round her Brothers of Italy party. The president, who "
              "picks the prime minister after an election, is Sergio Mattarella."),
    "spain": (("spain", "spanish"),
              "Pedro Sanchez is the prime minister of Spain: in office since 2018, and back in "
              "office after the 2023 election. The head of state is King Felipe VI, whose role is "
              "ceremonial."),
    "ireland": (("ireland", "irish", "taoiseach"),
                "Micheal Martin is the taoiseach, or prime minister, of Ireland: in office since "
                "January 2025. The president, a largely ceremonial role, is Catherine Connolly, "
                "elected in October 2025.",
                ("northern ireland", "northern irish", "belfast", "stormont", "ulster")),
    "canada": (("canada", "canadian"),
               "Mark Carney is the prime minister of Canada: in office since March 2025, and his "
               "Liberal party won the April 2025 election. He took over from Justin Trudeau, who "
               "resigned after nine years."),
    "australia": (("australia", "australian", "aussie"),
                  "Anthony Albanese is the prime minister of Australia: in office since May 2022 "
                  "and re-elected in May 2025. The head of state is King Charles III, represented "
                  "there by a governor-general."),
    "new zealand": (("new zealand", "new zealander", "kiwi"),
                    "Christopher Luxon is the prime minister of New Zealand: in office since "
                    "November 2023, leading a National-led coalition. The head of state is King "
                    "Charles III, represented by a governor-general."),
    "india": (("india", "indian"),
              "Narendra Modi is the prime minister of India: in office since 2014, and in his "
              "third term since June 2024. The president, whose role is largely ceremonial, is "
              "Droupadi Murmu."),
    "china": (("china", "chinese"),
              "Xi Jinping is the president of China: in office since 2013, and general secretary "
              "of the Communist Party since 2012. The party holds the power, and since 2018 there "
              "is no limit on his terms."),
    "japan": (("japan", "japanese"),
              "Sanae Takaichi is the prime minister of Japan: in office since October 2025, and "
              "the first woman to hold the job. The head of state is the emperor, Naruhito."),
    "russia": (("russia", "russian"),
               "Vladimir Putin is the president of Russia: in office since 2000, with four years "
               "as prime minister under Dmitry Medvedev in the middle. His current term runs to "
               "2030."),
    "ukraine": (("ukraine", "ukrainian"),
                "Volodymyr Zelenskyy is the president of Ukraine: elected in 2019. A presidential "
                "election is due, but it cannot be held while martial law is in force."),
    "turkey": (("turkey", "turkish", "turkiye"),
               "Recep Tayyip Erdogan is the president of Turkey: in office since 2014, and prime "
               "minister before that from 2003. The presidency became the centre of power after "
               "the 2017 referendum."),
    "greece": (("greece", "greek"),
               "Kyriakos Mitsotakis is the prime minister of Greece: in office since 2019 and "
               "re-elected in June 2023, leading New Democracy. The president, a ceremonial role, "
               "is chosen by parliament."),
    "poland": (("poland", "polish"),
               "Donald Tusk is the prime minister of Poland: in office since December 2023, after "
               "the October 2023 election. The president is Karol Nawrocki, elected in June 2025."),
    "sweden": (("sweden", "swedish"),
               "Ulf Kristersson is the prime minister of Sweden: in office since October 2022, "
               "leading a coalition that the Sweden Democrats support from outside it. The head "
               "of state is King Carl XVI Gustaf."),
    "norway": (("norway", "norwegian"),
               "Jonas Gahr Store is the prime minister of Norway: in office since 2021, and Labour "
               "won the September 2025 election, so he carried on. The head of state is King "
               "Harald V."),
    "denmark": (("denmark", "danish"),
                "Mette Frederiksen is the prime minister of Denmark: in office since 2019. The "
                "head of state is King Frederik X, who took over in January 2024."),
    "belgium": (("belgium", "belgian"),
                "Bart De Wever is the prime minister of Belgium: in office since February 2025, "
                "after seven months of coalition talks. The head of state is King Philippe."),
    "portugal": (("portugal", "portuguese"),
                 "Luis Montenegro is the prime minister of Portugal: in office since April 2024 "
                 "and re-elected in May 2025. The president, who can dissolve parliament, is "
                 "Marcelo Rebelo de Sousa."),
    "mexico": (("mexico", "mexican"),
               "Claudia Sheinbaum is the president of Mexico: in office since October 2024, and "
               "the first woman to hold the job. A Mexican president serves one six-year term and "
               "cannot stand again."),
    "brazil": (("brazil", "brazilian"),
               "Luiz Inacio Lula da Silva is the president of Brazil: in office since January "
               "2023, his third term. A Brazilian president serves four years and can be "
               "re-elected once in a row."),
    "argentina": (("argentina", "argentinian", "argentine"),
                  "Javier Milei is the president of Argentina: in office since December 2023. He "
                  "won on a promise to dollarise the economy and cut the state back."),
    "south africa": (("south africa", "south african"),
                     "Cyril Ramaphosa is the president of South Africa: in office since 2018, and "
                     "chosen again by parliament in June 2024 after the ANC lost its majority. The "
                     "ANC has governed since 1994."),
    "nigeria": (("nigeria", "nigerian"),
                "Bola Tinubu is the president of Nigeria: in office since May 2023. A Nigerian "
                "president serves four years and can stand for a second term."),
    "kenya": (("kenya", "kenyan"),
              "William Ruto is the president of Kenya: in office since September 2022. A Kenyan "
              "president serves a maximum of two five-year terms."),
    "egypt": (("egypt", "egyptian"),
              "Abdel Fattah el-Sisi is the president of Egypt: in office since 2014, after leading "
              "the 2013 takeover. The president holds most of the power, and the army is a large "
              "part of the economy."),
    "israel": (("israel", "israeli"),
               "Benjamin Netanyahu is the prime minister of Israel: in office since December 2022, "
               "and the longest-serving prime minister the country has had. Israel has a "
               "president too - Isaac Herzog - but that job is ceremonial."),
    "iran": (("iran", "iranian"),
             "Masoud Pezeshkian is the president of Iran: in office since July 2024. The man with "
             "the final say is the supreme leader, Ali Khamenei, and the president runs the "
             "government under him."),
    "saudi arabia": (("saudi arabia", "saudi", "saudi arabian"),
                     "King Salman is the king of Saudi Arabia, but his son Mohammed bin Salman - "
                     "crown prince, and prime minister since 2022 - runs the country day to day."),
    "south korea": (("south korea", "korea", "korean"),
                    "Lee Jae-myung is the president of South Korea: in office since June 2025, "
                    "after winning the snap election that followed Yoon Suk Yeol's impeachment. A "
                    "South Korean president serves one five-year term.",
                    ("north", "north korea", "kim jong", "pyongyang", "dprk")),
    "north korea": (("north korea", "north korean"),
                    "Kim Jong Un has led North Korea since 2011, when his father Kim Jong Il died. "
                    "He is not the head of state on paper: the constitution gives that title to "
                    "the president of the presidium of the Supreme People's Assembly, Choe Ryong "
                    "Hae. The Workers' Party is the only party that decides anything."),
    "pakistan": (("pakistan", "pakistani"),
                 "Shehbaz Sharif is the prime minister of Pakistan: in office since March 2024. "
                 "The president is a ceremonial role; the prime minister runs the government, "
                 "though the army has a large say."),
    "indonesia": (("indonesia", "indonesian"),
                  "Prabowo Subianto is the president of Indonesia: in office since October 2024, "
                  "after winning the February 2024 election. A president serves five years and can "
                  "be re-elected once."),
    "singapore": (("singapore", "singaporean"),
                  "Lawrence Wong is the prime minister of Singapore: in office since May 2024, "
                  "when Lee Hsien Loong stepped down after twenty years. The PAP has governed "
                  "since independence in 1965."),
    "malaysia": (("malaysia", "malaysian"),
                 "Anwar Ibrahim is the prime minister of Malaysia: in office since November 2022, "
                 "after decades in opposition. The king, whose crown rotates every five years "
                 "between the state rulers, is the head of state."),
    "philippines": (("philippines", "filipino"),
                    "Ferdinand Marcos Jr is the president of the Philippines: in office since June "
                    "2022. A Philippine president serves one six-year term."),
}

_LEADER_AVOID = ("club", "society", "company", "union", "student", "board", "golf", "darts",
                 "my office", "our office", "workplace", "at work", "my company", "our company",
                 "my team", "our team", "committee", "association", "residents", "tenants",
                 "university", "cricket", "football", "charity", "history", "was the",
                 "first president", "first prime minister", "war", "recipe",
                 "school", "school council", "parish", "tenants association")

for _place, _row_data in LEADERS.items():
    _words, _reply = _row_data[0], _row_data[1]
    _extra = _row_data[2] if len(_row_data) > 2 else ()
    _row("leader-" + _place.replace(" ", "-"), (_words, LEADER_WORDS), _reply,
         avoid=_LEADER_AVOID + tuple(_extra))
del _place, _row_data, _words, _reply, _extra


LEADERS_SECOND = {
    "germany-president": (("germany", "german"), ("president",),
                          "Frank-Walter Steinmeier is the president of Germany: in office since "
                          "2017 and re-elected in 2022. The job is mostly ceremonial - the "
                          "chancellor, Friedrich Merz, runs the government."),
    "spain-king": (("spain", "spanish"), ("king", "queen", "monarch", "head of state"),
                   "Felipe VI is the king of Spain: he took the throne in June 2014 when his "
                   "father Juan Carlos abdicated. The king is head of state but does not run the "
                   "government - the prime minister, Pedro Sanchez, does."),
    "italy-president": (("italy", "italian"), ("president",),
                        "Sergio Mattarella is the president of Italy: in office since 2015 and "
                        "re-elected in 2022. The president is head of state and picks the prime "
                        "minister after an election; Giorgia Meloni runs the government."),
    "ireland-president": (("ireland", "irish"), ("president",),
                          "Catherine Connolly is the president of Ireland: elected in October "
                          "2025. The job is largely ceremonial - the taoiseach, Micheal Martin, "
                          "runs the government.", ("northern ireland", "northern", "belfast",
                                                   "stormont", "ulster")),
    "israel-president": (("israel", "israeli"), ("president",),
                         "Isaac Herzog is the president of Israel: in office since 2021. The job "
                         "is ceremonial - the prime minister, Benjamin Netanyahu, runs the "
                         "government."),
    "portugal-president": (("portugal", "portuguese"), ("president",),
                           "Marcelo Rebelo de Sousa is the president of Portugal: in office since "
                           "2016 and re-elected in 2021. Unlike most ceremonial presidents he has "
                           "real power, including the right to dissolve parliament; the prime "
                           "minister is Luis Montenegro."),
    "japan-emperor": (("japan", "japanese"), ("emperor", "empress", "head of state"),
                      "Naruhito is the emperor of Japan: he took the throne in May 2019, when his "
                      "father Akihito stepped down. The emperor is a symbol of the state and has "
                      "no political power - the prime minister, Sanae Takaichi, runs the "
                      "government."),
    "poland-president": (("poland", "polish"), ("president",),
                         "Karol Nawrocki is the president of Poland: elected in June 2025. The "
                         "president can veto laws, and the prime minister, Donald Tusk, runs the "
                         "government."),
}

for _name, _row_data in LEADERS_SECOND.items():
    _words, _offices, _reply = _row_data[0], _row_data[1], _row_data[2]
    _extra = _row_data[3] if len(_row_data) > 3 else ()
    _row(_name, (_words, _offices), _reply, bias=1, avoid=_LEADER_AVOID + tuple(_extra))
del _name, _row_data, _words, _offices, _reply, _extra
