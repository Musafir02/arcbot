import re

from ..compose.repair import owns_the_deed
from ..understanding.attempts import asks_for_one_more
from .lookup import entry


_AMBIGUOUS_CITY_WORDS = ("bath",)


def _a_chess_line(understood):
    said = " ".join(str((understood or {}).get(key) or "")
                    for key in ("clean", "norm_text", "text")).lower()
    if _CHESS_WORDS.search(said):
        return True
    return bool(_CASTLING_VERB.search(said))


_CHESS_WORDS = re.compile(r"\b(chess|chessboard|rook|rooks|king|kings|kingside|queenside|"
                          r"queen|pawn|pawns|bishop|knight|checkmate|check mate|castling|"
                          r"moves?)\b")
_CASTLING_VERB = re.compile(r"\b(how|when|can i|should i|do i|where do i|why)\b[^.?!]{0,18}"
                            r"\bcastl(e|es|ed|ing)\b")


def _no_city_is_named(understood):
    from .travel import CITIES

    clean = " %s " % str(understood.get("clean") or "").lower().replace("-", " ")
    for city in CITIES:
        if city in _AMBIGUOUS_CITY_WORDS:
            continue
        if re.search(r"(?<![a-z])%s(?![a-z])" % re.escape(city), clean):
            return False
    return True


ANSWERS = ("entertainment", "creative")

WATCHING = ("i'm watching", "im watching", "are watching", "i was watching",
            "we were watching", "we watched a", "we watched the",
            "i watched a", "i watched the")

CHILD = ("child", "children", "kid", "kids", "year old", "year-old", "toddler",
         "baby", "grandchild", "grandchildren", "daughter", "son", "niece", "nephew",
         "grandson", "granddaughter")

SCREEN_TIME = ("too much", "screen time", "all day", "hours a day", "how many hours",
               "hours of screen", "hours of tv", "hours watching", "hours in front",
               "bedtime", "limit", "how long should", "how long can")

SPORT = ("cricket", "football", "rugby", "tennis", "match", "darts", "golf", "boxing",
         "race", "f1", "grand prix", "sport")

WORKS = {
    "1984": ("George Orwell", "published in 1949; his real name was Eric Blair",
             "novel"),
    "nineteen eighty four": ("George Orwell", "published in 1949", "novel"),
    "animal farm": ("George Orwell", "published in 1945", "novel"),
    "pride and prejudice": ("Jane Austen", "published in 1813", "novel"),
    "jane eyre": ("Charlotte Bronte", "published in 1847 under the name Currer Bell",
                  "novel"),
    "wuthering heights": ("Emily Bronte", "her only novel, published in 1847", "novel"),
    "great expectations": ("Charles Dickens", "published in 1861", "novel"),
    "a christmas carol": ("Charles Dickens", "published in 1843", "novella"),
    "oliver twist": ("Charles Dickens", "published in 1838", "novel"),
    "moby dick": ("Herman Melville", "published in 1851", "novel"),
    "the hobbit": ("J. R. R. Tolkien", "published in 1937", "book"),
    "lord of the rings": ("J. R. R. Tolkien", "published in three parts in 1954 and 1955",
                          "book"),
    "harry potter": ("J. K. Rowling", "the first one came out in 1997", "book"),
    "to kill a mockingbird": ("Harper Lee", "published in 1960", "novel"),
    "the great gatsby": ("F. Scott Fitzgerald", "published in 1925", "novel"),
    "of mice and men": ("John Steinbeck", "published in 1937", "novella"),
    "the catcher in the rye": ("J. D. Salinger", "published in 1951", "novel"),
    "war and peace": ("Leo Tolstoy", "published in 1869", "novel"),
    "crime and punishment": ("Fyodor Dostoevsky", "published in 1866", "novel"),
    "frankenstein": ("Mary Shelley", "published in 1818, when she was 20", "novel"),
    "dracula": ("Bram Stoker", "published in 1897", "novel"),
    "the handmaids tale": ("Margaret Atwood", "published in 1985", "novel"),
    "brave new world": ("Aldous Huxley", "published in 1932", "novel"),
    "dune": ("Frank Herbert", "published in 1965", "novel"),
    "the hitchhikers guide to the galaxy": ("Douglas Adams", "it began as a radio series in 1978",
                                           "book"),
    "sherlock holmes": ("Arthur Conan Doyle", "the first story came out in 1887", "character"),
    "the diary of a young girl": ("Anne Frank", "written in hiding in Amsterdam, 1942 to 1944",
                                  "diary"),
    "the very hungry caterpillar": ("Eric Carle", "published in 1969", "picture book"),
    "the gruffalo": ("Julia Donaldson", "published in 1999, with pictures by Axel Scheffler",
                     "picture book"),
    "matilda": ("Roald Dahl", "published in 1988", "children's book"),
    "charlie and the chocolate factory": ("Roald Dahl", "published in 1964", "children's book"),
    "the lion the witch and the wardrobe": ("C. S. Lewis", "published in 1950", "book"),
    "hamlet": ("William Shakespeare", "written around 1600", "play"),
    "macbeth": ("William Shakespeare", "written around 1606", "play"),
    "romeo and juliet": ("William Shakespeare", "written in the 1590s", "play"),
    "king lear": ("William Shakespeare", "written around 1605", "play"),
    "a midsummer nights dream": ("William Shakespeare", "written in the 1590s", "play"),
    "the raven": ("Edgar Allan Poe", "published in 1845", "poem"),
    "mona lisa": ("Leonardo da Vinci", "painted around 1503 to 1519, and it hangs in the Louvre",
                  "painting"),
    "the last supper": ("Leonardo da Vinci", "painted in the 1490s in Milan", "painting"),
    "starry night": ("Vincent van Gogh", "painted in 1889 from the window of an asylum",
                     "painting"),
    "sunflowers": ("Vincent van Gogh", "painted in Arles in 1888", "painting"),
    "the scream": ("Edvard Munch", "painted in 1893", "painting"),
    "girl with a pearl earring": ("Johannes Vermeer", "painted around 1665", "painting"),
    "the birth of venus": ("Sandro Botticelli", "painted in the 1480s", "painting"),
    "guernica": ("Pablo Picasso", "painted in 1937 after the bombing of the town", "painting"),
    "the night watch": ("Rembrandt", "finished in 1642", "painting"),
    "ninth symphony": ("Ludwig van Beethoven", "first performed in 1824, when he was deaf",
                       "symphony"),
    "moonlight sonata": ("Ludwig van Beethoven", "written in 1801", "sonata"),
    "the four seasons": ("Antonio Vivaldi", "written around 1725", "set of concertos"),
    "bohemian rhapsody": ("Queen", "released in 1975, written by Freddie Mercury", "song"),
    "hey jude": ("the Beatles", "written by Paul McCartney and credited to Lennon and McCartney",
                 "song"),
    "the magic flute": ("Wolfgang Amadeus Mozart", "first performed in 1791", "opera"),
    "jurassic park": ("Steven Spielberg", "released in 1993", "film"),
    "the godfather": ("Francis Ford Coppola", "released in 1972", "film"),
    "titanic": ("James Cameron", "released in 1997", "film"),
    "jaws": ("Steven Spielberg", "released in 1975", "film"),
    "e.t.": ("Steven Spielberg", "released in 1982", "film"),
    "schindlers list": ("Steven Spielberg", "released in 1993, in black and white", "film"),
    "pulp fiction": ("Quentin Tarantino", "released in 1994", "film"),
    "the shawshank redemption": ("Frank Darabont", "released in 1994", "film"),
    "star wars": ("George Lucas", "the first one came out in 1977", "film"),
    "the wizard of oz": ("Victor Fleming", "released in 1939", "film"),
    "casablanca": ("Michael Curtiz", "released in 1942", "film"),
    "psycho": ("Alfred Hitchcock", "released in 1960", "film"),
    "gone with the wind": ("Victor Fleming", "released in 1939", "film"),
    "the sound of music": ("Robert Wise", "released in 1965", "film"),
    "mary poppins": ("Robert Stevenson", "released in 1964", "film"),
    "toy story": ("John Lasseter", "released in 1995, the first fully computer-animated "
                  "feature", "film"),
    "finding nemo": ("Andrew Stanton", "released in 2003", "film"),
    "frozen": ("Chris Buck and Jennifer Lee", "released in 2013", "film"),
    "the lion king": ("Roger Allers and Rob Minkoff", "released in 1994", "film"),
    "paddington": ("Paul King", "released in 2014", "film"),
    "the dark knight": ("Christopher Nolan", "released in 2008", "film"),
    "inception": ("Christopher Nolan", "released in 2010", "film"),
    "avatar": ("James Cameron", "released in 2009", "film"),
    "back to the future": ("Robert Zemeckis", "released in 1985", "film"),
    "lord of the flies": ("William Golding", "published in 1954", "novel"),
    "an inspector calls": ("J. B. Priestley", "first staged in 1945, in Moscow", "play"),
    "the old man and the sea": ("Ernest Hemingway", "published in 1952", "novella"),
    "a view from the bridge": ("Arthur Miller", "first staged in 1955", "play"),
    "the color purple": ("Alice Walker", "published in 1982", "novel"),
    "things fall apart": ("Chinua Achebe", "published in 1958", "novel"),
    "the persistence of memory": ("Salvador Dali", "painted in 1931", "painting"),
    "the kiss": ("Gustav Klimt", "painted in 1907 and 1908", "painting"),
    "imagine": ("John Lennon", "released in 1971", "song"),
    "wonderwall": ("Oasis", "released in 1995, written by Noel Gallagher", "song"),
    "smells like teen spirit": ("Nirvana", "released in 1991, written by Kurt Cobain",
                               "song"),
    "like a rolling stone": ("Bob Dylan", "released in 1965", "song"),
}

WHO_MAKERS = ("wrote", "written", "author", "painted", "composed", "composer", "sculpted",
              "made", "directed", "director", "sang", "sung", "singer", "by")


VIEWS = {
    "the wire": ("*The Wire* is worth it, and the slow start is the point - give it four or "
                 "five episodes. Five series, a whole city in it, and it does not go soft at "
                 "the end."),
    "breaking bad": ("Yes. Short episodes, five series, and it gets darker every year without "
                     "losing the plot; Bryan Cranston is the reason it works."),
    "better call saul": ("Slower than *Breaking Bad* on purpose, and worth the patience if you "
                         "liked that one: it is a long, careful fall and it sticks the ending."),
    "the sopranos": ("Yes - the drama that started the run of great telly. Six series, and a "
                     "last scene people are still arguing about."),
    "succession": ("Yes: four series of a family at each other's throats, and much funnier "
                   "than it sounds. If you liked *The Thick of It*, start tonight."),
    "fleabag": ("An easy yes, and it takes about one evening: two series of six short "
                "episodes, funny first and then quietly devastating."),
    "happy valley": ("Three series and Sarah Lancashire is extraordinary in it; the third is "
                     "the best of them."),
    "line of duty": ("Six series of interviews and bent coppers - start at the first one, "
                     "because the story builds rather than resets."),
    "peaky blinders": ("Six series, very stylish, and a bit of a slog in the middle; Cillian "
                       "Murphy is the reason to watch it."),
    "chernobyl": ("Five episodes and the best short drama about a disaster ever made. Worth "
                  "one evening even if you think you know the story."),
    "the bear": ("Yes, and the episodes are about half an hour: loud, stressful, and really "
                 "about a family, with a sandwich shop round it."),
    "ted lasso": ("Warm and funny, and the first series is the best of the three - if you want "
                  "something kind on a wet evening, this is it."),
    "schitts creek": ("Worth it, but start knowing the first series is the weakest: it finds "
                      "its feet in the second and the last one is a joy."),
    "derry girls": ("Three short series and properly funny; the last one has the Good Friday "
                    "Agreement underneath it and still makes you laugh."),
    "game of thrones": ("Worth it, with a warning: most people hate the last series. The first "
                        "six are as good as television gets."),
    "the crown": ("Six series, each with a new cast, and the first two with Claire Foy are the "
                  "best; watch those and decide whether to go on."),
    "stranger things": ("The first series is the one - 80s, kids on bikes, a monster. It gets "
                        "bigger and sillier after that, so treat the later ones as a bonus."),
    "sherlock": ("Four short series of 90-minute episodes, and the first two are the good ones; "
                 "start with 'A Study in Pink'."),
    "black mirror": ("It is an anthology, so pick the standouts first - 'San Junipero' and "
                     "'USS Callister' - and skip around rather than in order."),
    "killing eve": ("The first series is brilliant; it gets weaker after that, but Jodie Comer "
                    "is worth staying for."),
    "mad men": ("Seven series in a 1960s ad agency: slow, stylish and really about people lying "
                "to themselves. Give it three episodes."),
    "downton abbey": ("Six series of a country house upstairs and down; gentle, easy and very "
                      "watchable if you want something undemanding."),
    "only murders in the building": ("Yes - a funny whodunnit with two older men and a young "
                                     "woman, three series of short episodes."),
    "the traitors": ("Genuinely gripping for a reality show; the UK version is the one to start "
                     "with and the round tables are the best part."),
    "doctor who": ("Start with the 2005 revival rather than the old ones: each episode stands "
                   "alone, and the first series with Christopher Eccleston is a good way in."),
    "pride and prejudice": ("Worth reading, and funnier than school makes it sound - give it "
                            "three chapters and you will know whether you get on with it."),
    "1984": ("Yes, and it is shorter and bleaker than most people expect; the middle is a long "
             "essay about power and the story around it is what stays."),
    "to kill a mockingbird": ("Worth it: a child's-eye view of a court case, and the first half "
                              "is slow on purpose - it is setting up what you will care about."),
    "dune": ("Worth it either way: the film tells the story cleanly and you do not need the book "
             "first. The book is denser and better on the politics, and both start slowly."),
    "the office": ("Yes, and start with the UK one - twelve episodes and then it is over, so it "
                   "costs you an evening to find out. The US one is gentler and much longer."),
    "oppenheimer": ("Worth it in a cinema if you can, because the sound is half of it; three "
                    "hours of men in rooms that somehow never drags."),
    "the godfather": ("Yes, and it holds up: the first two are the ones. Part three is the one "
                      "people argue about, so leave it until you care."),
    "lord of the rings": ("The fellowship one is the place to start, and the extended cut is "
                          "worth it once you know you like it - three hours a film, so give it "
                          "a free evening."),
    "harry potter": ("Worth it, and the books hold up better than the films for a reader past "
                     "ten; the third book is where it gets properly good."),
    "gone girl": ("Worth it: a thriller that turns halfway and takes you with it. The film is "
                  "faithful, so pick either one and skip the other."),
    "my neighbour totoro": ("Worth it at any age: gentle, almost nothing goes wrong, and it is "
                            "the film for a rainy afternoon or after a bad week. 86 minutes, and "
                            "no baddie to speak of."),
    "spirited away": ("Yes - the best way into Studio Ghibli and the one that wins over people "
                      "who say they do not like animation. Subtitled if you can; the English "
                      "voices are good too."),
    "parasite": ("Yes, and go in knowing nothing: it turns about halfway and the less you know "
                 "the better. Subtitles, two hours, and it never feels long."),
    "paddington 2": ("The rare sequel better than the first: warm, funny, and Hugh Grant having "
                     "the time of his life. The safest film there is for a mixed-age evening."),
    "everything everywhere all at once": ("Worth it if you have the energy for it: two hours "
                                          "twenty of noise, jokes and feeling, and the last "
                                          "twenty minutes earn all of it. Have tissues."),    "squid game": ("Yes - the first series is the one to start with: one game an episode, and "
                   "the tension is in the rules rather than the blood. The later series are "
                   "slower, so only go on if you liked the first."),
    "the last of us": ("Worth it even if you never played the game: nine episodes, and the third "
                       "one is a whole love story with almost nobody else in it. Bleak, so not a "
                       "background watch."),
    "shogun": ("Yes - a stranger in a strange court, and it is about power and translation more "
               "than battles. Partly subtitled, and better for it."),
    "slow horses": ("Yes: Gary Oldman as a filthy, brilliant spymaster, six short series, and it "
                    "gets funnier as it gets darker. Start at the first."),
    "severance": ("Worth it: office workers whose memories are split between work and home, and "
                  "the slowest drip of information you will be glad of. Short episodes, and pay "
                  "attention."),
    "the boys": ("Yes if you like your superheroes filthy and angry - it is a satire with a lot "
                 "of gore. If you want charm, this is not it."),
    "money heist": ("Worth it for the first two parts, which are one long heist with a hostage "
                    "negotiator; the later parts stretch a good idea a long way. Try the "
                    "original audio rather than the dub."),
    "bridgerton": ("Yes if you want gorgeous, silly, warm romance: each series is one couple and "
                   "a lot of string-quartet pop. It is not trying to be serious."),
    "the witcher": ("The first series is confusing on purpose and settles by the second; watch "
                    "it for the monster-of-the-week episodes and Henry Cavill's growl."),
    "gilmore girls": ("Worth it: seven series of very fast talking, a small town, and a mother "
                      "and daughter who are friends. Comfort television rather than plot."),
    "sex education": ("Yes - four series, funny and kind, about a teenager running an advice "
                      "clinic at school, with Gillian Anderson as his mother."),
    "normal people": ("Worth it: two people circling each other over twelve short episodes, and "
                      "the most honest silences on television. Bleak in a quiet way."),
    "bluey": ("Yes, and not only for the children: seven-minute episodes about a family of dogs "
              "that are funnier and sadder than they need to be, and a parent gets more out of "
              "it than the child."),
    "avatar the last airbender": ("Worth it: three series of a cartoon that is really a war "
                                  "story with a twelve-year-old in the middle, and it earns its "
                                  "ending. Start at episode one, not the film."),
    "the matrix": ("Yes, and it holds up: the first film is the one, and the effects still work "
                   "because they serve the story. The sequels are for people who want more of "
                   "the world."),
    "inception": ("Worth it: a heist inside dreams, and it explains its own rules as it goes. "
                  "Watch it without your phone and the ending lands."),
    "interstellar": ("Yes, on the biggest screen you can: a father-and-daughter story with a "
                     "black hole in the middle, and the sound is half of it. The middle act is "
                     "slow."),
    "everything everywhere all at once": ("Yes, and give it twenty minutes: it is silly and fast "
                                          "and then it is about a mother and a daughter and you "
                                          "are crying. The middle is a lot of noise."),
    "barbie": ("Worth it: funny and strange and about more than the doll, and Ryan Gosling steals "
               "it. Two hours, and it knows exactly what it is doing."),
    "wonka": ("Worth it for a family evening: warm, colourful, songs you half know, and "
              "Chalamet is charming. Nobody needed it, but it is a good time."),
    "the holdovers": ("Yes - a grumpy teacher, a stranded student and a cook at a boarding school "
                      "over Christmas. Small, funny, and it earns its ending."),
    "past lives": ("Worth it: two childhood friends in different countries and twenty years of "
                   "what-ifs. Quiet, short, and it does not go where you expect."),
    "where the crawdads sing": ("Worth it if you want a slow, sad mystery about a girl raising "
                                "herself in a marsh. The book is better and the film is "
                                "faithful to it."),
    "the midnight library": ("Worth it: a woman between life and death tries the lives she did "
                             "not live. Gentle, quick, and the ending is the argument."),
    "lessons in chemistry": ("Yes - a chemist in the 1960s turns a cooking show into a lecture, "
                             "and it is funny and angry at once. A dog narrates a chapter."),
    "the seven husbands of evelyn hugo": ("Worth it: an old film star tells her life story to a "
                                          "reporter, and it is a soap opera in the best sense."),
    "tomorrow and tomorrow and tomorrow": ("Yes - two friends making video games over thirty "
                                           "years, and it is really about work, and love, and "
                                           "the friend you do not marry."),
    "a little life": ("Worth it, but be warned: it is long, it is about damage, and it is "
                      "relentless. Read it when you have a fortnight and somebody to talk to "
                      "about it."),
    "klara and the sun": ("Worth it: an artificial friend watches a family and misunderstands "
                          "beautifully. Quiet, and the ending stays with you."),
    "the song of achilles": ("Yes - the Iliad told by Patroclus, and it is a love story first and "
                             "a war epic second. Have the tissues ready."),
    "circe": ("Worth it: the witch of the Odyssey tells her own story, and it is about power and "
              "exile. Slow to start, then it grips."),
    "piranesi": ("Worth it, and go in knowing nothing: a man lives in an infinite house of "
                 "statues. Short, strange, and the reveal is the reward."),
    "project hail mary": ("Yes - a man wakes alone on a spaceship and has to science his way out, "
                          "with one very funny alien. Best read cold."),
    "the martian": ("Worth it: one man, one planet, and a lot of problem-solving, and the most "
                    "cheerful survival story there is."),
    "sapiens": ("Worth it as an argument rather than a history: bracing and readable, and "
                "confidently wrong in places, so read it with a pinch of salt."),

}

JUDGE_ASKS = ("worth watching", "worth a watch", "worth reading", "worth a read",
              "worth playing", "worth seeing", "any good", "is it good", "is it any good",
              "should i watch", "should i read", "should i start", "is it worth")

JUDGE_WORDS = ("good", "worth", "worthwhile", "like", "boring", "rubbish", "any", "better",
               "watch", "watching", "read", "reading", "see", "start", "best", "should")

VERDICT_ASKS = ("worth", "worthwhile", "good", "any good", "any cop", "like", "boring",
                "rubbish", "bother", "should i watch", "should i read", "should i start",
                "should i see", "shall i watch", "shall i read", "is it any good",
                "is it good", "worth watching", "worth reading", "worth a watch",
                "worth a read")

A_PLACE_NOT_A_WORK = ("commute", "commuting", "each way", "into the office", "to the office",
                      "in the office", "at the office", "from the office", "office days",
                      "days a week", "my desk", "work from home", "working from home", "hybrid",
                      "my boss", "canteen", "open plan")

_THE_OFFICE_IS = re.compile(
    r"the office (?:is|was|'s)\s+(?:(?:so|too|really|quite|very|only|about|just|always)\s+)?"
    r"(?:\d+\s*(?:minute|min|hour)|cold|freezing|boiling|hot|stuffy|noisy|loud|quiet|far|"
    r"near|closer|close|empty|dead|busy|full|open plan|tiny|huge|big|grim|depressing|miserable)")

WANT_ASKS = ("want", "wanted", "fancy", "fancied", "feel like", "in the mood", "mood for",
             "need", "would love", "id love", "i'd love", "looking for", "after a", "give me",
             "craving")
ANY_MOOD_ASKS = ("something", "anything", "some", "in the mood", "fancy", "want", "wanted",
                 "need", "recommend", "suggest", "ideas", "any", "give me", "what should i",
                 "looking for", "feel like", "would love", "id love", "i'd love",
                 "put me in the mood", "mood for", "shorter", "quicker")
NOT_A_MOOD_PICK = (
    "film", "films", "movie", "movies", "cinema", "watch", "watching", "watched",
    "tv", "telly", "series", "show", "shows", "boxset", "box set", "binge", "episode",
    "episodes", "netflix", "iplayer", "streaming", "book", "books", "novel", "novels",
    "read", "reading", "audiobook", "audiobooks", "podcast", "podcasts", "album", "albums",
    "song", "songs", "playlist", "game", "games", "board game",
    "say", "tell me", "joke", "jokes", "story", "stories", "happened", "happens",
    "happening", "at work",
    "hand", "hands", "a hand with", "lend a hand", "give me a hand", "help me with",
    "present", "gift", "birthday", "anniversary", "christmas", "valentine", "for my wife",
    "for my husband", "for my partner", "for my mum", "for my dad",
    "im feeling", "i am feeling", "feel sad", "feel down", "feel low", "feeling sad",
    "feeling down", "feeling low", "scared", "frightened", "terrified", "worried",
    "to be happy", "be happy", "depressed", "anxious",
    "journey", "long journey", "long drive", "car journey", "car ride", "road trip",
    "motorway", "on the motorway", "flight", "flights", "plane", "ferry",
    "train journey", "on the train",
    "news", "sad news", "bad news", "no news", "the news", "heard the news", "some news",
    "any news", "news about", "news that", "good news",
    "passed away", "passed on", "died", "death", "funeral", "burial", "cremation",
    "bereaved", "bereavement", "grief", "grieving", "mourning", "widow", "widowed",
    "diagnosed", "diagnosis", "hospice", "in hospital", "terminally", "miscarriage",
    "stillborn", "broke up", "broken up", "split up", "divorce", "divorced",
    "lost my job", "redundant", "made redundant", "evicted",
)
PICK_ASKS = ("a film", "a movie", "a book", "a series", "a show", "a podcast",
             "a documentary", "best film", "best movie", "best series", "best show",
             "to watch", "to read", "anything", "something", "recommend", "suggest",
             "what should", "whats on", "netflix", "iplayer", "prime video", "disney",
             "streaming", "on telly")

UNNAMED_ASKS = ("worth watching", "worth a watch", "worth reading", "worth a read",
                "worth playing", "worth seeing", "should i watch", "should i read",
                "any good", "is it any good", "is it good")

HABIT_ASKS = ("for you", "for me", "for kids", "for a child", "healthy", "unhealthy",
              "bad for", "good for", "before bed", "help me", "improve", "screen time",
              "too much")
NOT_A_VERDICT = HABIT_ASKS + ("films", "movies", "books", "shows", "podcasts", "documentaries")

SEEN_ALREADY = re.compile(r"\b(?:i|we|he|she|they)\s+(?:have\s+|had\s+|just\s+|finally\s+|"
                          r"already\s+)?(?:watched|saw|seen|read|finished|binged)\b")
AGE_ASK = re.compile(r"\b\d+ ?(?:year|yr)s?[ -]?old\b|\b(?:toddler|baby|teenager|teen)\b")

ASKING_FIRST = re.compile(r"\b(?:should|shall|can|could|would|do|does|did|might|may|any|worth|"
                          r"good|what|which)\b")

_SMALL = {"and", "the", "of", "a", "an", "in", "on", "to", "for", "with"}


def _title(work):
    words = work.split()
    if words and words[0].isdigit():
        return work
    return " ".join(word if (i and word in _SMALL) else word[:1].upper() + word[1:]
                    for i, word in enumerate(words))


def who_made(memory, understood):
    clean = (understood or {}).get("clean") or (understood or {}).get("text") or ""
    clean = clean.lower().replace("'", "").replace("\u2019", "")
    best = None
    for work in WORKS:
        if re.search(r"\b" + re.escape(work) + r"\b", clean):
            if best is None or len(work) > len(best):
                best = work
    if best is None:
        return None
    maker, detail, kind = WORKS[best]
    name = _title(best)
    article = "an" if kind[:1] in "aeiou" else "a"
    return (f"{name} is {article} {kind} by {maker}, {detail}.")


BOOK_AUTHORS = (
    ("pride and prejudice", "Jane Austen"),
    ("sense and sensibility", "Jane Austen"),
    ("emma", "Jane Austen"),
    ("persuasion", "Jane Austen"),
    ("mansfield park", "Jane Austen"),
    ("northanger abbey", "Jane Austen"),
    ("oliver twist", "Charles Dickens"),
    ("great expectations", "Charles Dickens"),
    ("a christmas carol", "Charles Dickens"),
    ("david copperfield", "Charles Dickens"),
    ("a tale of two cities", "Charles Dickens"),
    ("bleak house", "Charles Dickens"),
    ("1984", "George Orwell"),
    ("animal farm", "George Orwell"),
    ("down and out in paris and london", "George Orwell"),
    ("to kill a mockingbird", "Harper Lee"),
    ("jane eyre", "Charlotte Bronte"),
    ("wuthering heights", "Emily Bronte"),
    ("the great gatsby", "F. Scott Fitzgerald"),
    ("moby dick", "Herman Melville"),
    ("frankenstein", "Mary Shelley"),
    ("dracula", "Bram Stoker"),
    ("little women", "Louisa May Alcott"),
    ("the hobbit", "J.R.R. Tolkien"),
    ("the lord of the rings", "J.R.R. Tolkien"),
    ("the fellowship of the ring", "J.R.R. Tolkien"),
    ("harry potter and the philosopher's stone", "J.K. Rowling"),
    ("harry potter", "J.K. Rowling"),
    ("a game of thrones", "George R.R. Martin"),
    ("the hunger games", "Suzanne Collins"),
    ("the shining", "Stephen King"),
    ("misery", "Stephen King"),
    ("carrie", "Stephen King"),
    ("murder on the orient express", "Agatha Christie"),
    ("and then there were none", "Agatha Christie"),
    ("the murder of roger ackroyd", "Agatha Christie"),
    ("the hound of the baskervilles", "Arthur Conan Doyle"),
    ("sherlock holmes", "Arthur Conan Doyle"),
    ("the adventures of tom sawyer", "Mark Twain"),
    ("adventures of huckleberry finn", "Mark Twain"),
    ("of mice and men", "John Steinbeck"),
    ("the grapes of wrath", "John Steinbeck"),
    ("lord of the flies", "William Golding"),
    ("brave new world", "Aldous Huxley"),
    ("fahrenheit 451", "Ray Bradbury"),
    ("the handmaid's tale", "Margaret Atwood"),
    ("beloved", "Toni Morrison"),
    ("half of a yellow sun", "Chimamanda Ngozi Adichie"),
    ("americanah", "Chimamanda Ngozi Adichie"),
    ("the kite runner", "Khaled Hosseini"),
    ("life of pi", "Yann Martel"),
    ("the martian", "Andy Weir"),
    ("project hail mary", "Andy Weir"),
    ("normal people", "Sally Rooney"),
    ("eleanor oliphant is completely fine", "Gail Honeyman"),
    ("the midnight library", "Matt Haig"),
    ("where the crawdads sing", "Delia Owens"),
    ("the thursday murder club", "Richard Osman"),
    ("the secret history", "Donna Tartt"),
    ("the goldfinch", "Donna Tartt"),
    ("a little life", "Hanya Yanagihara"),
    ("the book thief", "Markus Zusak"),
    ("the alchemist", "Paulo Coelho"),
    ("one hundred years of solitude", "Gabriel Garcia Marquez"),
    ("the road", "Cormac McCarthy"),
    ("never let me go", "Kazuo Ishiguro"),
    ("the remains of the day", "Kazuo Ishiguro"),
    ("romeo and juliet", "William Shakespeare"),
    ("hamlet", "William Shakespeare"),
    ("macbeth", "William Shakespeare"),
    ("king lear", "William Shakespeare"),
    ("othello", "William Shakespeare"),
    ("a midsummer night's dream", "William Shakespeare"),
    ("julius caesar", "William Shakespeare"),
    ("the tempest", "William Shakespeare"),
    ("twelfth night", "William Shakespeare"),
    ("the odyssey", "Homer"),
    ("the iliad", "Homer"),
    ("the canterbury tales", "Geoffrey Chaucer"),
    ("paradise lost", "John Milton"),
    ("sapiens", "Yuval Noah Harari"),
    ("becoming", "Michelle Obama"),
    ("the diary of a young girl", "Anne Frank"),
    ("the bell jar", "Sylvia Plath"),
    ("mrs dalloway", "Virginia Woolf"),
    ("to the lighthouse", "Virginia Woolf"),
    ("the picture of dorian gray", "Oscar Wilde"),
    ("the importance of being earnest", "Oscar Wilde"),
    ("treasure island", "Robert Louis Stevenson"),
    ("dr jekyll and mr hyde", "Robert Louis Stevenson"),
    ("alice in wonderland", "Lewis Carroll"),
    ("alice's adventures in wonderland", "Lewis Carroll"),
    ("through the looking glass", "Lewis Carroll"),
    ("the wizard of oz", "L. Frank Baum"),
    ("the secret garden", "Frances Hodgson Burnett"),
    ("charlie and the chocolate factory", "Roald Dahl"),
    ("matilda", "Roald Dahl"),
    ("the bfg", "Roald Dahl"),
    ("james and the giant peach", "Roald Dahl"),
    ("the witches", "Roald Dahl"),
    ("gangsta granny", "David Walliams"),
    ("the gruffalo", "Julia Donaldson"),
    ("the very hungry caterpillar", "Eric Carle"),
    ("the tale of peter rabbit", "Beatrix Potter"),
    ("war horse", "Michael Morpurgo"),
    ("the lion the witch and the wardrobe", "C.S. Lewis"),
    ("northern lights", "Philip Pullman"),
    ("percy jackson", "Rick Riordan"),
    ("diary of a wimpy kid", "Jeff Kinney"),
    ("a brief history of time", "Stephen Hawking"),
    ("the catcher in the rye", "J.D. Salinger"),
    ("the old man and the sea", "Ernest Hemingway"),
    ("anna karenina", "Leo Tolstoy"),
    ("crime and punishment", "Fyodor Dostoevsky"),
    ("the count of monte cristo", "Alexandre Dumas"),
    ("les miserables", "Victor Hugo"),
    ("don quixote", "Miguel de Cervantes"),
    ("middlemarch", "George Eliot"),
    ("things fall apart", "Chinua Achebe"),
    ("the colour purple", "Alice Walker"),
    ("gone girl", "Gillian Flynn"),
    ("the girl on the train", "Paula Hawkins"),
    ("the silent patient", "Alex Michaelides"),
    ("lessons in chemistry", "Bonnie Garmus"),
    ("klara and the sun", "Kazuo Ishiguro"),
    ("a thousand splendid suns", "Khaled Hosseini"),
    ("the seven husbands of evelyn hugo", "Taylor Jenkins Reid"),
    ("the little prince", "Antoine de Saint-Exupery"),
    ("the selfish gene", "Richard Dawkins"),
    ("the origin of species", "Charles Darwin"),
    ("a short history of nearly everything", "Bill Bryson"),
)

TITLE_SPELLING = {"the color purple": "the colour purple"}

AUTHOR_KEYS = tuple(dict.fromkeys(writer.split()[-1].lower()
                                  for _title, writer in BOOK_AUTHORS))
AUTHOR_ALSO = {"doyle": "conan doyle", "rowling": "jk rowling", "martin": "george rr martin",
               "fitzgerald": "scott fitzgerald", "lewis": "cs lewis"}

ASKED_WROTE = ("write", "wrote", "written", "writes", "writing", "author", "authors",
               "book", "books", "novel", "novels", "play", "plays", "poem", "poems",
               "story", "stories", "else", "other", "also", "more", "by")


def _author_key(author):
    return author.split()[-1].lower()


def _titles_of(author):
    return [title for title, writer in BOOK_AUTHORS if writer == author]


def _title_in(clean):
    best = None
    for title, author in BOOK_AUTHORS:
        if re.search(r"(?<![a-z0-9])" + re.escape(title) + r"(?![a-z0-9])", clean):
            if best is None or len(title) > len(best[0]):
                best = (title, author)
    return best


def _author_in(clean, title=None):
    for author in dict.fromkeys(writer for _title, writer in BOOK_AUTHORS):
        key = _author_key(author)
        words = [key]
        also = AUTHOR_ALSO.get(key)
        if also:
            words.append(also)
        for word in words:
            if title and word in title:
                continue
            if re.search(r"(?<![a-z0-9])" + re.escape(word) + r"(?![a-z0-9])", clean):
                return author
    return None


TITLE_AS = {"the bfg": "The BFG", "dr jekyll and mr hyde": "Dr Jekyll and Mr Hyde",
            "1984": "1984", "jk rowling": "J.K. Rowling"}

TITLE_SMALL = ("and", "of", "the", "a", "an", "in", "to", "on", "for", "at", "with")


def _display(text):
    if text in TITLE_AS:
        return TITLE_AS[text]
    words = text.split()
    out = [words[0][:1].upper() + words[0][1:]]
    for word in words[1:]:
        out.append(word if word in TITLE_SMALL else word[:1].upper() + word[1:])
    return " ".join(out)


def _said(text):
    return text.replace(".", "")


def _list_words(items):
    items = list(items)
    if len(items) == 1:
        return items[0]
    return ", ".join(items[:-1]) + " and " + items[-1]


def _who_wrote(memory, understood):
    clean = (understood.get("clean") or "").replace(" & ", " and ")
    for spelling, standard in TITLE_SPELLING.items():
        clean = clean.replace(spelling, standard)
    found = _title_in(clean)
    named = _author_in(clean, found[0] if found else None)
    if found:
        title, author = found
        others = [t for t in _titles_of(author)
                  if t != title and title not in t and not t.startswith(title)
                  and not title.startswith(t)]
        rest = (f" Other books by {_said(author)}: "
                f"{_list_words(_display(t) for t in others[:3])}." if others else "")
        if named and named != author:
            return (f"Not quite - {_display(title)} is by {_said(author)}, not "
                    f"{_said(named)}.{rest}")
        if named:
            return f"Yes - {_display(title)} is by {_said(author)}.{rest}"
        return f"{_display(title)} is by {_said(author)}.{rest}"
    if not named:
        return None
    titles = _titles_of(named)
    if not titles:
        return None
    said = _list_words(_display(t) for t in titles[:5])
    more = "" if len(titles) <= 5 else ", among others"
    return f"{_said(named)} wrote {said}{more}."


BOOK_MATCHES = (
    ("normal people",
     "If you liked *Normal People*, *Conversations with Friends* is the same author on the same "
     "ground, and *Exciting Times* by Naoise Dolan has the same cool, sharp voice about love and "
     "money. For warmth too, *The Rachel Incident* by Caroline O'Donoghue."),
    ("the midnight library",
     "*The Humans* by the same author is the closest, and *A Man Called Ove* by Fredrik Backman "
     "has the same kind of kindness in it. *Eleanor Oliphant Is Completely Fine* if you want "
     "another odd person finding their way."),
    ("gone girl",
     "Try *The Silent Patient* by Alex Michaelides: short chapters, an unreliable narrator and a "
     "twist you won't see coming. *The Girl on the Train* by Paula Hawkins is the other obvious "
     "next step, and *Sharp Objects* is the same author as Gone Girl and nastier."),
    ("the thursday murder club",
     "The next one is *The Man Who Died Twice* by Richard Osman, the same four friends again. "
     "For a different author, *The Marlow Murder Club* by Robert Thorogood is close in tone, or "
     "*The Silent Patient* if you want a darker twist."),
    ("the martian",
     "Try *Project Hail Mary* by Andy Weir, the same author: one man solving one problem at a "
     "time, funnier than The Martian. For something bigger but just as engineering-minded, "
     "*Seveneves* by Neal Stephenson."),
    ("project hail mary",
     "*The Martian* is the same author and the same kind of puzzle-solving, and *Children of "
     "Time* by Adrian Tchaikovsky is the step up: bigger ideas, still easy to read."),
    ("harry potter",
     "*His Dark Materials* by Philip Pullman is the next step: magic, a child at the centre of "
     "it and better writing. *Percy Jackson* by Rick Riordan is easier and funnier, and *The "
     "Worst Witch* suits a younger reader."),
    ("klara and the sun",
     "*Never Let Me Go* is the same author on the same question, and quieter. *Machines Like Me* "
     "by Ian McEwan is the other one about a machine in a family."),
    ("never let me go",
     "*Klara and the Sun* and *The Remains of the Day* are the same author, and both are about "
     "somebody who only sees the truth too late. *The Road* by Cormac McCarthy if you want the "
     "same quiet grief."),
    ("the secret history",
     "*If We Were Villains* by M. L. Rio is the closest thing to it, and *The Likeness* by Tana "
     "French has the same closed group of clever friends. *The Goldfinch* is the same author and "
     "longer."),
    ("where the crawdads sing",
     "*The Great Alone* by Kristin Hannah has the same wild setting and the same lone girl, and "
     "*The Marsh King's Daughter* by Karen Dionne is the darker version."),
    ("eleanor oliphant is completely fine",
     "*A Man Called Ove* by Fredrik Backman is the same lonely person, warmer, and *The Rosie "
     "Project* by Graeme Simsion is funnier. Both are easy to read."),
    ("the song of achilles",
     "*Circe* is the same author and just as good, and *The Silence of the Girls* by Pat Barker "
     "tells the same war from the women's side."),
    ("the silent patient",
     "*The Girl on the Train* by Paula Hawkins and *The Guest List* by Lucy Foley both keep the "
     "twist hidden, and both are quick. *Gone Girl* if you want the coldest narrator of the lot."),
    ("a little life",
     "*Shuggie Bain* by Douglas Stuart is the same weight of sadness and just as well written, "
     "and *The Goldfinch* by Donna Tartt is the other long one people finish and then sit still."),
    ("the book thief",
     "*All the Light We Cannot See* by Anthony Doerr is the closest in feeling, and *The Boy in "
     "the Striped Pyjamas* is easier if it is for a younger reader."),
    ("lessons in chemistry",
     "*Remarkably Bright Creatures* by Shelby Van Pelt has the same warmth and a woman who "
     "carries on her own, and *Eleanor Oliphant Is Completely Fine* the same odd, funny voice."),
    ("the seven husbands of evelyn hugo",
     "*Daisy Jones and the Six* by Taylor Jenkins Reid is the same author and the same glamour "
     "with a dark edge, and *City of Girls* by Elizabeth Gilbert is the other long, warm life "
     "story."),
    ("conversations with friends",
     "*Normal People* is the same author and easier, and *Exciting Times* by Naoise Dolan has "
     "the same clever young people making a mess of it."),
    ("it ends with us",
     "*Me Before You* by Jojo Moyes is the one everyone else starts with, and *The Last Letter "
     "from Your Lover* is the same kind of love story with a hard centre."),
    ("the hunger games",
     "*Divergent* by Veronica Roth is the closest to it, and *The Giver* by Lois Lowry is "
     "shorter and stranger. For a grown-up version, *The Handmaid's Tale*."),
    ("the girl with the dragon tattoo",
     "*The Girl on the Train* moves faster, and *The Silence of the Lambs* is the colder one. "
     "*Sharp Objects* by Gillian Flynn if you want a family full of secrets."),
    ("the glass hotel",
     "*Station Eleven* is the same author and the better one to read first: the same quiet "
     "collapse and the same people holding on. *Cloud Atlas* by David Mitchell is the other "
     "one that moves between times like this."),
    ("station eleven",
     "*The Glass Hotel* is the same author, and *The Road* by Cormac McCarthy is the harsher, "
     "shorter version of the same world. *Severance* by Ling Ma is the funnier one."),
    ("verity",
     "The same kind of twist, done colder: *The Housemaid* by Freida McFadden, or *The Last "
     "Mrs Parrish* by Liv Constantine. *The Silent Patient* if you have not read it yet."),
    ("the housemaid",
     "*Verity* by Colleen Hoover is the closest and the fastest, and *The Last Mrs Parrish* by "
     "Liv Constantine has the same servant-in-the-house trick with more bite."),
    ("fourth wing",
     "*A Court of Thorns and Roses* by Sarah J. Maas is the same author-on-romance-and-war "
     "shape and the usual next step, and *Throne of Glass* is the same author, longer."),
    ("the da vinci code",
     "*Angels and Demons* is the same author and the same puzzle chase. For the real thing, "
     "*The Name of the Rose* by Umberto Eco is the same story with more history."),
    ("to kill a mockingbird",
     "*Of Mice and Men* is shorter and just as much about who gets a fair go, and *The Book "
     "Thief* is the other one about a child watching a town fail."),
    ("of mice and men",
     "*To Kill a Mockingbird* is the other short one about fairness, and *The Grapes of Wrath* "
     "is the same author and the same journey, much longer."),
    ("lord of the flies",
     "*The Hunger Games* does the same thing with a plot, and *The Graveyard Book* by Neil "
     "Gaiman suits a reader who wants it darker but shorter."),
    ("life of pi",
     "*The Old Man and the Sea* is the short one with the same sea and the same stubborn man, "
     "and *The Alchemist* is the other fable people read next."),
    ("the kite runner",
     "*A Thousand Splendid Suns* is the same author and better, and *And the Mountains Echoed* "
     "is the third one. *The Bookseller of Kabul* if you want the true version."),
    ("the alchemist",
     "*Life of Pi* has the same fable feel with a story that holds, and *Siddhartha* by Hermann "
     "Hesse is the short one behind it."),
    ("percy jackson",
     "*Magnus Chase* by Rick Riordan is the same author doing Norse myth, *Artemis Fowl* by "
     "Eoin Colfer is cleverer and funnier, and *Nevermoor* by Jessica Townsend is the safest "
     "pick for a younger reader."),
    ("the maze runner",
     "*The Hunger Games* by Suzanne Collins if you have not read it, *Divergent* by Veronica "
     "Roth next, and *Scythe* by Neal Shusterman when you want the same idea with more "
     "thinking in it."),
    ("divergent",
     "*The Hunger Games* is the one to read first if you skipped it, *Legend* by Marie Lu is "
     "the closest in shape, and *The Darkest Minds* by Alexandra Bracken has the same "
     "runaways-with-powers feel."),
    ("twilight",
     "*The Mortal Instruments* by Cassandra Clare is the next step for most readers, "
     "*Vampire Academy* by Richelle Mead is lighter and funnier, and *Crave* by Tracy Wolff "
     "is the newer, sillier version."),
    ("lord of the rings",
     "*The Hobbit* first if you have not read it. After that *The Name of the Wind* by "
     "Patrick Rothfuss for the prose, or *A Wizard of Earthsea* by Ursula K. Le Guin if you "
     "want the whole thing in 200 pages."),
    ("the hobbit",
     "*The Lord of the Rings* is the sequel and the reason to read it. *The Chronicles of "
     "Narnia* if you want shorter and lighter, or *A Wizard of Earthsea* for a quieter kind "
     "of magic."),
    ("game of thrones",
     "*The Blade Itself* by Joe Abercrombie for the same grim humour with fewer characters "
     "to keep track of, *The Name of the Wind* for one voice telling its own story, or *The "
     "Priory of the Orange Tree* if you want dragons in a single volume."),
    ("dune",
     "*Foundation* by Isaac Asimov for the politics across centuries, *Hyperion* by Dan "
     "Simmons for the strangeness, and *Children of Time* by Adrian Tchaikovsky for the "
     "biology."),
    ("1984",
     "*Animal Farm* by the same author first, because it is one evening's reading and the "
     "same argument. Then *Brave New World* by Aldous Huxley, and *Fahrenheit 451* by Ray "
     "Bradbury for the shortest of the three."),
    ("animal farm",
     "*1984* by the same author is the longer version of the same warning, then *Brave New "
     "World* by Aldous Huxley, or *Fahrenheit 451* by Ray Bradbury if you want it short."),
    ("brave new world",
     "*1984* by George Orwell is the pair everyone reads next, *Fahrenheit 451* by Ray "
     "Bradbury is shorter, and *The Handmaid's Tale* by Margaret Atwood is the one that "
     "still feels closest to now."),
    ("the handmaid's tale",
     "*The Testaments* by Margaret Atwood is the sequel from 2019 and answers what happened. "
     "*Vox* by Christina Dalcher is the same idea done faster, and *Red Clocks* by Leni "
     "Zumas is the quieter one."),
    ("pride and prejudice",
     "*Persuasion* is the next Austen - shorter and sadder. *Jane Eyre* by Charlotte Bronte "
     "for the gothic version, or *Bridget Jones's Diary* for the modern retelling."),
    ("the great gatsby",
     "*The Sun Also Rises* by Hemingway for the same lost generation, *Mrs Dalloway* by "
     "Virginia Woolf for a party that holds a whole life, or *Rules of Civility* by Amor "
     "Towles for the modern version."),
    ("diary of a wimpy kid",
     "*Tom Gates* by Liz Pichon is the same diary shape with more doodles, *Big Nate* by "
     "Lincoln Peirce is the school one, and *Captain Underpants* by Dav Pilkey if they want "
     "sillier."),
    ("alex rider",
     "*Cherub* by Robert Muchamore is the closest: teenagers trained as agents, more brutal "
     "than it looks. *Young Bond* by Charlie Higson for the origin story, or *Artemis Fowl* "
     "if they would rather be the genius."),
    ("jacqueline wilson",
     "*Cathy Cassidy* next for the same warm, short chapters, *The Suitcase Kid* or *Double "
     "Act* if they want another Wilson, or *Once* by Morris Gleitzman when they are ready "
     "for something harder."),
    ("agatha christie",
     "*The Thursday Murder Club* by Richard Osman for the modern cosy version, *Strong "
     "Poison* by Dorothy L. Sayers for the classic one, or *Magpie Murders* by Anthony "
     "Horowitz, which is a Christie puzzle inside a Christie puzzle."),
    ("stephen king",
     "*11.22.63* is his best if the storytelling was the draw, *The Shining* for the proper "
     "horror, and *Heart-Shaped Box* by Joe Hill - his son - for the same voice."),
    ("the fault in our stars",
     "*Eleanor & Park* by Rainbow Rowell is the closest in feeling, *Me and Earl and the "
     "Dying Girl* by Jesse Andrews if you want it funny as well as sad, and *Five Feet "
     "Apart* by Rachael Lippincott for the same story again."),
    ("the hate u give",
     "*Dear Martin* by Nic Stone is the closest next read, *The Poet X* by Elizabeth Acevedo "
     "if the voice is what you liked, and *Long Way Down* by Jason Reynolds, which is one "
     "elevator ride in verse."),
    ("wonder",
     "*Out of My Mind* by Sharon M. Draper, *Fish in a Tree* by Lynda Mullaly Hunt and *The "
     "Goldfish Boy* by Lisa Thompson all do the same thing: a child nobody expects much "
     "from, telling it themselves."),
    ("the catcher in the rye",
     "*The Perks of Being a Wallflower* by Stephen Chbosky is the closest in voice, *Looking "
     "for Alaska* by John Green for the same boy at boarding school, and *The Bell Jar* by "
     "Sylvia Plath when you want the darker one."),
    ("little women",
     "*Anne of Green Gables* by L. M. Montgomery, *Pride and Prejudice* for the sisters and "
     "the wit, or *The Railway Children* by E. Nesbit for the family doing without."),
    ("anne of green gables",
     "*Emily of New Moon* is the same author's other girl and most people who love Anne love "
     "her too. *Little Women* next, or *Pollyanna* for the same bright stubbornness."),
    ("the secret garden",
     "*The Railway Children* by E. Nesbit, *Anne of Green Gables* for another child sent "
     "somewhere she does not want to be, or *Tom's Midnight Garden* by Philippa Pearce."),
    ("narnia",
     "*The Hobbit* is the obvious next one, *A Wizard of Earthsea* by Ursula K. Le Guin for "
     "the quieter magic, and *His Dark Materials* by Philip Pullman when they are a year or "
     "two older."),
    ("his dark materials",
     "*The Chronicles of Narnia* for the other world through a door, *A Wizard of Earthsea* "
     "for the magic with a price, and *The Lie Tree* by Frances Hardinge for the historical "
     "version."),
    ("ready player one",
     "*Snow Crash* by Neal Stephenson is the book it borrows from, *Ender's Game* by Orson "
     "Scott Card is the training-school one, and *The Martian* if the problem-solving was "
     "the best part."),
)

BOOK_LIKE_ASKS = ("like", "liked", "likes", "similar", "similar to", "something like",
                  "anything like", "after", "next", "what next", "loved", "loves", "enjoyed",
                  "recommend", "recommendation")
BOOK_LIKE_THINGS = (("book", "books", "novel", "novels", "read", "reading")
                    + tuple(title for title, _reply in BOOK_MATCHES))

LIKE_A_NAMED_BOOK = re.compile(
    r"\b(?:books?|novels?|reading|read)\s+(?:like|similar to|after)\s+([a-z0-9'&: -]{2,40})"
    r"|\b(?:something|anything)\s+(?:like|similar to)\s+([a-z0-9'&: -]{2,40})")


def _book_title_named(text):
    best = ""
    for title, _reply in BOOK_MATCHES:
        if len(title) > len(best) and re.search(r"(?<![a-z0-9])" + re.escape(title)
                                                + r"(?![a-z0-9])", text):
            best = title
    return best


def _book_like(memory, understood):
    text = (understood.get("clean") or understood.get("norm_text") or "").lower()
    named = _book_title_named(text)
    scan = text.replace(named, " ") if named else text
    if re.search(r"\b\d+ ?year old|\byear olds?\b|\bkids?\b|\bchildren?\b|"
                 r"\btoddlers?\b|\bbab(?:y|ies)\b|\b(?:my|our|his|her|their) "
                 r"(?:son|daughter|child|boy|girl|grandson|granddaughter|niece|nephew)\b",
                 scan):
        return ""
    for title, reply in BOOK_MATCHES:
        if title == named:
            return reply
    found = LIKE_A_NAMED_BOOK.search(text)
    said = ""
    if found:
        said = (found.group(1) or found.group(2) or "").strip(" .?!")
        said = re.split(r"\b(?:but|that|which|without|and|because)\b", said)[0].strip(" .?!")
    if said:
        return ("I don't know *%s* well enough to match it, and a guess would waste your evening. "
                "Tell me what you liked about it - the people, the pace, or the writing - and "
                "I'll pick something close." % said.title())
    return ""


CHILD_WORDS = ("kid", "kids", "child", "children", "toddler", "toddlers", "preschooler",
               "preschoolers", "baby", "babies", "little one", "little ones", "school", "reception",
               "nursery", "year old", "year olds", "years old", "year old's", "yr old",
               "daughter", "son", "girl", "girls", "boy", "boys", "grandchild", "grandchildren",
               "1st", "2nd", "3rd", "4th", "5th", "6th", "7th", "8th", "9th", "10th")


_AGE_SHAPES = (
    r"\b(\d{1,2})\s*(?:st|nd|rd|th)\b",
    r"\b(\d{1,2})\s*(?:year|yr)s?[ -]old\b",
    r"\b(\d{1,2})\s*(?:year|yr)s?\s*olds?\b",
    r"\bage[d]?\s*(\d{1,2})\b",
    r"\bturning\s+(\d{1,2})\b",
    r"\b(?:is|she is|hes|he is|they are)\s+(\d{1,2})\b",
)

_PARTY_TINY = ("Keep each game to five minutes and let everyone win: pass the parcel with a "
               "sweet in every layer, musical statues where you freeze in a silly shape, "
               "sleeping lions, and a treasure hunt of pictures taped at their height round one "
               "room. Cake and food first, games after, is easier at that age.")
_PARTY_MIDDLE = ("Ten minutes a game is plenty at that age: musical statues, pass the parcel with "
                 "a sweet in every layer, pin the tail on the donkey, and a treasure hunt of "
                 "picture clues round the garden. Sleeping lions calms them down before food, and "
                 "Simon Says fills the gap while the cake comes out.")
_PARTY_OLDER = ("At that age they want to win something: a treasure hunt with written clues, a "
                "relay or an obstacle race in the garden, and musical chairs with music they "
                "picked. Have two prizes a game so nobody is out early for long, and keep one "
                "quiet game for the end, when the sugar has worn off.")
_PARTY_ANY = ("Ten minutes a game is plenty: musical statues, pass the parcel with a sweet in "
              "every layer, pin the tail on the donkey, and a treasure hunt of picture clues "
              "round the garden. Sleeping lions calms them down before food, and Simon Says "
              "fills the gap while the cake comes out. Tell me the age and I'll pitch it right.")


def _age_in(line):
    for shape in _AGE_SHAPES:
        found = re.search(shape, line)
        if found:
            years = int(found.group(1))
            if 1 <= years <= 16:
                return years
    return None


def _party_games_for_kids(memory, understood):
    line = ((understood.get("clean") or understood.get("text") or "")).lower()
    if not any(word in line for word in CHILD_WORDS):
        return ""
    if "adult" in line or "grown up" in line or "grown-up" in line:
        return ""
    years = _age_in(line)
    if years is None:
        if any(word in line for word in ("toddler", "toddlers", "baby", "babies", "nursery")):
            years = 2
        else:
            said = _PARTY_ANY
            return _indoors(said, line) if "indoor" in line else said
    if years <= 4:
        said = _PARTY_TINY
    elif years <= 7:
        said = _PARTY_MIDDLE
    else:
        said = _PARTY_OLDER
    return _indoors(said, line)


def _indoors(said, line):
    if "indoor" in line or "indoors" in line or "inside" in line or "flat" in line:
        return said.replace("round the garden", "round the house")
    return said


def _listen_when(memory, understood):
    line = ((understood.get("clean") or understood.get("text") or "")).lower()
    if "podcast" in line or "podcasts" in line:
        said = " %s " % " ".join(line.split())
        if " about " in said or " on " in said:
            return None
    if any(word in line for word in ("drive", "driving", "car", "road trip", "motorway")):
        return ("For a long drive: *Rumours* by Fleetwood Mac and *Graceland* by Paul Simon "
                "are both easy to sing along to, and *The Rest Is History* if you would rather "
                "have talking than music. Make one playlist before you go, because changing it "
                "at 70mph is the annoying part.")
    if any(word in line for word in ("kids party", "kids' party", "childrens party",
                                     "children's party", "childs party", "child's party",
                                     "toddler party", "party for kids", "party for children",
                                     "kids birthday", "childrens birthday")):
        return ("For a children's party the music wants to be louder and shorter than you think: "
                "a 60 to 90 minute playlist of songs they already know - *The Greatest Showman*, "
                "*Frozen*, Taylor Swift, whatever the school run plays - from a phone on a "
                "speaker away from the food table, started the moment they arrive. Cue musical "
                "statues about halfway through: it costs nothing and it resets a room that is "
                "getting wild.")
    if any(word in line for word in ("aisle", "walking in", "processional", "walk in to",
                                     "coming in to")) and "first dance" not in line:
        return ("For the aisle pick the entrance, not a favourite song: *Canon in D* (Pachelbel) "
                "is the default for good reason, *Here Comes the Bride* (Bridal Chorus) is the one "
                "everybody knows, *A Thousand Years* (Christina Perri) or *Sweet Disposition* "
                "(Temper Trap) for something modern, or a string version of a song you love if "
                "the room is small. Two minutes is plenty, and play it again as you leave.")
    if any(word in line for word in ("funeral", "memorial", "cremation", "crematorium", "burial",
                                     "church service", "send off", "wake")):
        return ("Three songs is the usual shape: one going in, one for the reflection or the "
                "photos, one to walk out to. *Somewhere Over the Rainbow* (the Israel "
                "Kamakawiwo'ole version) or *Ave Maria* suit a church, *Fix You* and *Everybody "
                "Hurts* suit a room that wants to cry, *My Way* (Sinatra) or *Thank You for the "
                "Days* (the Kinks) walk people out smiling. Give the funeral director titles, "
                "artists and exact versions a week ahead.")
    if "first dance" in line:
        return ("The song you both already sing badly in the car beats any list, but if you want "
                "somewhere to start: *At Last* by Etta James, *You Are the Best Thing* by Ray "
                "LaMontagne, *Can't Help Falling in Love* by Elvis, *Tenerife Sea* by Ed Sheeran, "
                "*The Book of Love* by Peter Gabriel for something quieter, or *You're My Best "
                "Friend* by Queen for a room that will sing along. Play each one all the way "
                "through and pick the one you can sway to for three minutes without counting the "
                "beats, then give the DJ that exact version - a remix has ruined more first dances "
                "than bad dancing.")
    if any(word in line for word in ("signing of the register", "sign the register",
                                     "register signing", "signing the register")):
        return ("For the register, something the room knows and can hum while they wait: *A "
                "Thousand Years* (Christina Perri), *Make You Feel My Love* (Adele), *Jesu, Joy "
                "of Man's Desiring* if it is a church, or *Better Together* (Jack Johnson). Two "
                "songs is right - one while the first people sign, one for the second - because "
                "signing takes longer than anyone plans for.")
    if ("wedding" in line or "marrying" in line) and any(
            word in line for word in ("music", "song", "songs", "playlist", "band", "dj")):
        return ("Three moments, three songs: walk in - *Canon in D*, or the *Trumpet Voluntary* if "
                "it is grand; sign the register - *A Thousand Years* or *Make You Feel My Love*; "
                "walk out - *Signed, Sealed, Delivered* or *This Will Be*. For the evening, the "
                "songs everyone already knows (ABBA, Queen, *Mr Brightside*) fill a floor better "
                "than anything tasteful. Ask the couple which three songs they would dance to in "
                "an empty kitchen.")
    if any(word in line for word in ("wedding song", "wedding songs", "songs for a wedding",
                                     "wedding music", "music for a wedding", "song for a wedding",
                                     "ceremony music", "song for my wedding")):
        return ("Three moments, three songs: walk in - *Canon in D*, or the *Trumpet Voluntary* if "
                "it is grand; sign the register - *A Thousand Years* or *Make You Feel My Love*; "
                "walk out - *Signed, Sealed, Delivered* or *This Will Be*. For the evening, the "
                "songs everyone already knows (ABBA, Queen, *Mr Brightside*) fill a floor better "
                "than anything tasteful. Ask the couple which three songs they would dance to in "
                "an empty kitchen.")
    if any(word in line for word in ("wedding", "first dance", "reception", "bridal")):
        return ("Split the day, because a wedding is two different rooms: for the ceremony and the "
                "meal, something quiet and familiar that nobody has to listen to - a solo piano or "
                "string version of songs the couple likes - and for the evening, the songs everyone "
                "already knows so the dance floor fills. Ask the couple for five songs they both "
                "love and build the evening around those, keep a do-not-play list, and have the "
                "first dance track loaded and cued rather than searched for on the night.")
    if any(word in line for word in ("dinner party", "party", "barbecue", "bbq", "guests",
                                     "drinks", "buffet")):
        return ("For a room with people talking in it, the music is wallpaper, not the show: "
                "something familiar and mid-tempo that nobody has to listen to - a Motown or "
                "soul compilation, *Rumours*, or any 'dinner party' playlist in the 90 to 110 "
                "beats-per-minute range. Start it thirty minutes before people arrive, keep it "
                "quiet enough to talk over while you eat, and turn it up once the plates are "
                "cleared.")
    if "podcast" not in line and any(word in line for word in (
            "rainy day", "rainy afternoon", "rainy sunday", "rainy weekend", "rainy morning",
            "wet afternoon", "wet day", "wet weekend", "snowy day", "stuck indoors")):
        return ("For a rainy day: *Rumours* by Fleetwood Mac, *Blue* by Joni Mitchell if you "
                "want something quieter, or *Graceland* by Paul Simon for a kitchen that needs "
                "waking up. Rain is the one day a whole album beats a playlist, so put one on "
                "and leave it alone.")
    if any(word in line for word in ("cook", "cooking", "kitchen", "dinner")):
        return ("While you cook: *Kind of Blue* by Miles Davis, *The Köln Concert* by Keith "
                "Jarrett, or any Motown compilation. All of them have no words to follow, so "
                "you can still hear the timer.")
    if any(word in line for word in ("run", "running", "jog", "gym", "workout")):
        return ("For a run: something around 160 to 170 beats per minute keeps the pace steady, "
                "so *Mr Brightside*, *Titanium* and *Don't Stop Me Now* all work, or a Daft Punk "
                "album run straight through if you would rather not think about it.")
    if any(word in line for word in ("walk", "walking", "way to work", "walk to work",
                                     "commute", "commuting", "journey to work")):
        return ("For a commute: *The Rest Is History* or *Desert Island Discs* if you want "
                "talking, *Rumours* if you want music. Podcasts beat music for a commute because "
                "the time passes without you counting it.")
    return ("For a long listen: *Rumours* by Fleetwood Mac, *Graceland* by Paul Simon, or *The "
            "Rest Is History* if you would rather hear talking. Tell me what the journey is and "
            "I'll make it specific.")


def _family_film(memory, understood):
    clean = understood.get("clean") or ""
    said = " ".join(str((understood or {}).get(key) or "") for key in ("clean", "text"))
    if not any(word in said for word in CHILD + ("family", "teenager", "teenagers", "teen", "teens")):
        return _films_within(
            "For a laugh: *Groundhog Day* is the funniest safe pick, *The Grand Budapest Hotel* "
            "if you want something stylish with the same warmth, and *Paddington 2* if you want "
            "to laugh from the first minute. All three are fine with anyone in the room.", said)
    if re.search(r"\bteen\w*|\badolescen\w*|\b1[3-9]\s*(?:year|yr)"
                 r"|\b(?:aged|age)\s*1[3-9]\b", clean):
        return ("With teenagers in the room: *Spider-Man: Into the Spider-Verse* (funny, fast and "
                "genuinely good), *Knives Out* if they will sit through a 12A whodunnit, and "
                "*Back to the Future* for the one everybody ends up watching. *The Mitchells vs "
                "the Machines* is the safe pick for a mixed-age sofa, and *Paddington 2* still "
                "works on a teenager who has not seen it.")
    ages = [int(a or b or c) for a, b, c in re.findall(
        r"\b(\d{1,2})\s*(?:year|yr)s?[ -]old\b|\bage[d]?\s*(\d{1,2})\b"
        r"|\b(?:is|are)\s+(\d{1,2})\b", clean)]
    ages = sorted(set(n for n in ages if 1 <= n <= 16))
    if ages:
        years = ages[0]
        if years <= 4:
            return ("For a four-year-old: *The Gruffalo* and *Room on the Broom* (both about 25 "
                    "minutes) and *The Snail and the Whale* are the safest, then *Zootropolis* or "
                    "*Paddington 2* for a full film. Save *Matilda* and *The Mitchells vs the "
                    "Machines* for a year or two.")
        if years <= 7:
            return ("For a five- or six-year-old: *Paddington 2* (funny, warm, no real peril), "
                    "*The Gruffalo* and *Room on the Broom* (both about 25 minutes), and "
                    "*Zootropolis* if you want a full film. Save *Matilda* for a year or two.")
    return ("*Paddington 2*: funny for the adults too, and nothing in it will scare an 8- or "
            "11-year-old. *The Mitchells vs the Machines* or *Matilda* are good backups.")


FILM_MATCHES = (
    ("paddington", "If you liked *Paddington*, try *The Mitchells vs the Machines* or *Matilda*: "
                   "warm, funny and nothing scary. For a clever, warm film, *Knives Out* or *The "
                   "Grand Budapest Hotel* are the next step."),
    ("martian", "If you liked *The Martian*, try *Apollo 13* (tense and practical), *Arrival* "
                "(clever and quiet) or *Gravity* (a tight 90 minutes). All solve problems rather "
                "than fight."),
    ("get out", "If you liked *Get Out*, *Us* and *Nope* are the closest Jordan Peele follow-ups, "
                "and *Sorry to Bother You* is stranger and sharper. All three are unsettling "
                "rather than gory."),
    ("john wick", "If you liked *John Wick*, try *Atomic Blonde* or *Nobody* for the same close-up "
                  "action, or *The Raid* if you want the fights turned up. Short on plot, long on "
                  "choreography."),
    ("interstellar", "If you liked *Interstellar*, try *Arrival* for the ideas, *Contact* for the "
                     "wonder and *Moon* for a small, tense one. All quieter than *Interstellar*."),
    ("knives out", "If you liked *Knives Out*, *Glass Onion* is the direct sequel; *The Grand "
                   "Budapest Hotel* has the same wit, and *Clue* is the silly classic."),
    ("godfather", "If you liked *The Godfather*, try *Goodfellas* or *The Departed* for crime with "
                  "momentum, or *Heat* for the bank job and the shootout."),
    ("mean girls", "If you liked *Mean Girls*, try *Clueless*, *Easy A* or *Booksmart*: the same "
                   "sharp high-school comedy, all easy to like."),
    ("breaking bad", "After *Breaking Bad*: *Better Call Saul* first (same world, slower and just "
                     "as good), then *Ozark* for the same dread, or *Narcos* if you want the real "
                     "story. *The Wire* is the step up if you have not seen it."),
    ("the bear", "After *The Bear*: *Boiling Point* (the film, one unbroken take), *Burnt* for a "
                 "lighter kitchen, or *The Bear*'s closest cousin *Shameless* (US) for a family "
                 "that shouts. All short episodes."),
    ("happy valley", "After *Happy Valley*: *Sherwood*, *Bodyguard* or *Line of Duty* for British "
                     "tension, and *Unforgotten* if you want the detective work without the "
                     "violence. *Scott & Bailey* is the gentler one."),
    ("succession", "After *Succession*: *The Thick of It* (same writer, sharper jokes), "
                   "*Billions* for the money, or *Industry* for the young version. *Veep* if you "
                   "want the comedy turned up."),
    ("stranger things", "After *Stranger Things*: *Dark* (German, twistier), *The OA*, or "
                        "*Super 8* for the film version. *Paper Girls* is the closest comic-book "
                        "feel."),
    ("the crown", "After *The Crown*: *The Queen* and *The Iron Lady* for the same world in film "
                  "form, *Victoria* for the earlier reign, or *A Very English Scandal* for the "
                  "same era and wit."),
    ("line of duty", "After *Line of Duty*: *Happy Valley* first, then *Bodyguard*, *Sherwood* or "
                     "*Vigil*. All British, all tense, none gory."),
    ("peaky blinders", "After *Peaky Blinders*: *Boardwalk Empire* (the American version), "
                       "*Gangs of London* for the violence, or *Taboo* with the same lead actor. "
                       "*Ripper Street* for the period."),
    ("game of thrones", "After *Game of Thrones*: *House of the Dragon* is the direct prequel; "
                        "*The Last Kingdom* is the better-paced one, and *Rome* is the closest in "
                        "scheming."),
    ("friends", "After *Friends*: *Brooklyn Nine-Nine* for the same comfort, *Parks and "
                "Recreation* (start at series 2), or *Schitt's Creek*, which gets funny fast. "
                "*How I Met Your Mother* if you want the same shape."),
    ("the office", "After *The Office*: the UK original if you have only seen the US one, then "
                   "*Parks and Recreation*, *Brooklyn Nine-Nine* or *Superstore*. All the same "
                   "mockumentary warmth."),
    ("derry girls", "After *Derry Girls*: *The Young Offenders*, *Moone Boy* or *This Way Up* for "
                    "the same sharp Irish comedy. *Bad Sisters* if you want a darker one."),
    ("friday night dinner", "After *Friday Night Dinner*: *The Inbetweeners* or *Gavin & Stacey* "
                            "for the same family shouting, and *Plebs* if you want the silly "
                            "version."),
    ("ted lasso", "After *Ted Lasso*: *Schitt's Creek* (the same kindness arriving slowly), "
                  "*Detectorists* for the gentle British version, or *The Good Place* if you want "
                  "the jokes and the thinking."),
    ("the wire", "After *The Wire*: *The Shield* and *Generation Kill* (same creator), *Bosch* for "
                 "the police work, or *Oz* for the same prison-city sweep."),
)
AFTER_TITLE_WORDS = tuple(title for title, _ in FILM_MATCHES)

PLAIN_TITLES = frozenset((
    "friends", "the office", "the crown", "the bear", "the wire", "get out"))
PLAIN_SENSE = {
    "friends": ("my friends", "our friends", "his friends", "her friends", "their friends",
                "your friends", "make friends", "new friends", "best friends", "best friend",
                "friends are", "friends came", "friends and family", "a few friends"),
    "the office": ("my office", "our office", "your office", "his office", "her office",
                   "their office", "new office", "back to the office", "at the office",
                   "in the office", "the office is", "office job", "office chair", "office move",
                   "office party"),
    "the crown": ("my crown", "the crown of", "crown court", "crown jewels", "crown fell",
                  "half crown", "crown is loose", "crown came off"),
    "the bear": ("a bear", "the bear is", "bears are", "bear attack", "polar bear", "teddy",
                 "bear claw", "bear claws", "claw"),
    "the wire": ("a wire", "the wire is", "wires", "wiring", "rewire", "live wire", "wire wool"),
    "get out": ("get out of", "got out of", "getting out of", "get out the", "get out more"),
    "knives out": ("knives out for", "sharp knives", "kitchen knives"),
}
WORK_EVIDENCE = (
    "watch", "watched", "watching", "film", "films", "movie", "movies", "series", "show",
    "shows", "episode", "episodes", "season", "seasons", "binge", "binged", "bingeing",
    "stream", "streamed", "netflix", "tv", "telly", "iplayer", "prime video", "read", "reading",
    "book", "books", "novel", "novels", "chapter", "finished", "finishing", "seen", "started",
    "caught up", "got through", "box set")
NEXT_EVIDENCE = (
    "what next", "what now", "what else", "anything else", "something else", "similar",
    "anything like", "something like", "like that", "recommend", "recommendation",
    "recommendations", "suggestion", "suggestions", "what should i watch")


MAKING_UP = ("i'm writing", "im writing", "i am writing", "i'm trying to write",
             "im trying to write", "writing a story", "writing a novel", "writing a book",
             "write a story", "write a novel", "help me write", "my own story", "my novel",
             "my story", "my character", "my main character", "in my story", "for my story",
             "a story where", "a story set in", "story where", "script", "screenplay",
             "short story", "plot", "villain", "poem about")



EASY_FILM_LIST = ("If you want something easy and good tonight: *Groundhog Day* for comedy, "
                  "*Knives Out* for a clever whodunnit, or *Arrival* if you'd rather think. All "
                  "three work on a sofa with no planning.")


_ASKS_FOR_A_FILM = re.compile(
    r"\b(?:want|wants|need|needs|fancy|looking for|after|recommend|recommendation|suggest|"
    r"should i|shall i|can you|could you|give me|got any|any|what|which|good|best|decent|"
    r"mood for|in the mood)\b")


GENTLE_LIST = ("*Knives Out*, *The Grand Budapest Hotel* and *Paddington 2* are warm, funny and "
               "tense in the right places, and nothing that will keep you up. For a series, *The "
               "Detectorists* is gentle and very good, *Ghosts* is daft and kind, and *Happy "
               "Valley* is the tense British crime one.")


def _the_gentle_list(memory, understood):
    last = memory.get("last_answer") if isinstance(memory, dict) else None
    said = str((last or {}).get("reply") or "") if isinstance(last, dict) else ""
    if said and _plain_words(said) == _plain_words(GENTLE_LIST):
        if _pick_kind(" ".join(_own_texts(understood))) not in ("", "film"):
            return GENTLE_LIST
        other = FILM_MOODS.get("funny") or ""
        if other and _plain_words(other) != _plain_words(GENTLE_LIST):
            return other
        return None
    return GENTLE_LIST


def _the_chat_turned_down(names, memory, after=None):
    topics = memory.get("topics") if isinstance(memory, dict) else None
    if not isinstance(topics, list):
        return False
    names = frozenset(names)
    for topic in reversed(topics):
        text = str(topic.get("text") or "") if isinstance(topic, dict) else ""
        if not text:
            continue
        if not (names & frozenset(_plain_words(text).split())):
            continue
        return _a_word_is_turned_down(text, names, after)
    return False


def _the_mood_the_chat_turned_down(memory):
    topics = memory.get("topics") if isinstance(memory, dict) else None
    if not isinstance(topics, list):
        return False
    for topic in reversed(topics):
        text = str(topic.get("text") or "") if isinstance(topic, dict) else ""
        if not text:
            continue
        got = _mood_of(text)
        if got:
            return bool(got[1])
    return False


def _the_mood_the_chat_holds(memory):
    topics = memory.get("topics") if isinstance(memory, dict) else None
    if not isinstance(topics, list):
        return None
    for topic in reversed(topics):
        text = str(topic.get("text") or "") if isinstance(topic, dict) else ""
        if not text:
            continue
        got = _mood_of(text)
        if got and not got[1]:
            return got[0]
    return None


def _film_like(memory, understood):
    texts = [one.lower() for one in (understood.get("clean") or "",
                                     understood.get("norm_text") or "") if one]
    if not _the_liked_thing_is_asked_about(understood):
        held = _the_mood_the_chat_holds(memory)
        if held:
            picks = FILM_MOODS.get(held)
            if picks:
                return _films_within(picks, str(understood.get("clean") or ""))
        return EASY_FILM_LIST
    for text in texts:
        pick = _table_pick(text)
        if pick:
            return pick
    for text in texts:
        named = re.search(r"\b(?:film|movie|show|series|programme)s?\s+(?:like|similar to)\s+"
                          r"([a-z0-9'&: -]{2,40})", text)
        if named:
            title = re.split(r"\b(?:but|that|which|without|and|or|please)\b"
                             r"|\b(?:film|movie|show|series|programme)s?\b",
                             named.group(1))[0].strip(" .?!")
            if title:
                return ("I don't know *%s* well enough to match it. Tell me what you liked about "
                        "it: the story, the jokes, or how tense it was, and I'll pick something "
                        "close." % title.title())
    own = str((understood or {}).get("text") or (understood or {}).get("clean") or "").lower()
    if not (_ASKS_FOR_A_FILM.search(own) and re.search(r"\b(?:films?|movies?)\b", own)):
        return ""
    return ("Tell me what you liked about the last film you enjoyed: the story, the jokes, or how "
            "tense it was. Name one and I'll suggest something close.")


SCARE_WORDS = frozenset(("scary", "scariest", "scare", "scares", "scared", "horror", "horrifying",
                         "horrific", "frightening", "frightened", "creepy", "terrifying", "spooky",
                         "gory", "gore", "blood", "bloody", "haunted", "slasher", "zombie",
                         "ghost", "jump scare"))
SCARE_TURNED_DOWN = frozenset(("dislike", "dislikes", "loathe", "detest", "bored", "sick",
                               "tired", "over", "spare", "except", "against", "refuse", "stop",
                               "done", "meh", "avoid"))
SCARE_REFUSED_AFTER = re.compile(
    r"\b(?:is|are|was|were)?\s*(?:not|never)\s+(?:really\s+)?(?:for\s+(?:me|us)|my\s+(?:thing|"
    r"sort|cuppa|cup|kind)|what\s+i|something\s+i|anything\s+i|a\s+fan|keen|into\s+it)\b"
    r"|\bis\s+out\b|\bare\s+out\b|\btoo\s+much\b|\btoo\s+scary\b|\bscares?\s+me\b"
    r"|\bmakes?\s+me\s+(?:jump|nervous)\b|\bgives?\s+me\s+nightmares\b|\bover\s+the\s+top\b",
    re.I)
NOT_A_TURN_DOWN = re.compile(
    r"\b(?:not\s+(?:really\s+)?sure|no\s+idea|no\s+clue|not\s+bothered|do\s+not\s+mind|"
    r"do\s+not\s+care|not\s+fussed)\b", re.I)


TURNED_DOWN_WANT = ("dont really want", "do not really want", "dont want", "do not want",
                    "dont fancy", "do not fancy", "dont feel like", "do not feel like",
                    "not in the mood for", "not really in the mood for", "not into",
                    "bored of", "bored with", "tired of", "sick of", "no more",
                    "anything but", "apart from", "other than", "except for", "nothing with",
                    "dont like", "do not like", "cant stand", "can not stand", "cannot stand")


TURNS_BACK = frozenset(("but", "instead", "rather", "prefer", "preferably", "though", "however",
                        "actually", "or"))


def _a_word_is_turned_down(text, names, after=None):
    names = frozenset(names)
    if not names or not isinstance(text, str) or not text:
        return False
    plain = NOT_A_TURN_DOWN.sub(" ", _plain_words(text))
    for phrase in TURNED_DOWN_WANT:
        plain = plain.replace(phrase, " not ")
    words = plain.split()
    for at, word in enumerate(words):
        if word not in names and word.rstrip("s") not in names:
            continue
        before = words[max(0, at - 8):at]
        for cut in range(len(before) - 1, -1, -1):
            if before[cut] in TURNS_BACK:
                before = before[cut + 1:]
                break
        if any(one in NEGATORS or one in SCARE_TURNED_DOWN for one in before):
            return True
        if after is not None and after.search(" ".join(words[at + 1:at + 9])):
            return True
    return False


def _own_texts(understood):
    understood = understood if isinstance(understood, dict) else {}
    text = understood.get("text")
    if isinstance(text, str) and text.strip():
        return [text]
    texts = []
    for key in ("norm_text", "clean"):
        value = understood.get(key)
        if isinstance(value, str) and value and value not in texts:
            texts.append(value)
    return texts


def _the_scare_is_refused(understood):
    for text in _own_texts(understood):
        if _a_word_is_turned_down(text, SCARE_WORDS, SCARE_REFUSED_AFTER):
            return True
    return False

FILM_ASK_WORDS = frozenset(("film", "films", "movie", "movies", "series", "watch", "watching",
                            "telly", "tv", "netflix", "boxset", "episode", "episodes", "iplayer"))


def _a_film_ask(understood):
    for text in _own_texts(understood):
        plain = " " + _plain_words(text) + " "
        if any((" " + word + " ") in plain for word in FILM_ASK_WORDS):
            return True
    return _the_scare_is_refused(understood)


def _the_scare_is_wanted(understood):
    return not _the_scare_is_refused(understood)


def _work_named(text):
    best = ""
    for title in VIEWS:
        if len(title) > len(best) and re.search(r"(?<![a-z0-9])" + re.escape(title)
                                                + r"(?![a-z0-9])", text):
            best = title
    return best


_FRESH_LIST = re.compile(
    r"\b(?:any|some|more|which|what)\s+(?:good\s+|other\s+|different\s+)?(?:films?|movies?|"
    r"books?|novels?|series|shows?|programmes?|programs?|podcasts?)\b"
    r"|\b(?:films?|movies?|books?|novels?|series|shows?|programmes?|programs?|podcasts?)\s+"
    r"(?:for|to watch|to read|to listen|on the|for the)\b")


def _the_liked_thing_is_asked_about(understood):
    reading = understood if isinstance(understood, dict) else {}
    own = str(reading.get("text") or reading.get("clean") or "").lower()
    if not _FRESH_LIST.search(own):
        return True
    if re.search(r"\b(?:like|likes|liked|loves?|loved|enjoyed|similar)\b", own):
        return True
    return bool(_book_title_named(own) or _work_named(own))


A_PERSON_TO_CONSULT = re.compile(
    r"\b(?:see|seeing|visit)\s+(?:someone|somebody|anyone|anybody|him|her|them|"
    r"(?:a|the|my|your)\s+(?:doctor|gp|dentist|nurse|physio\w*|specialist|consultant|surgeon|"
    r"optician|vet|midwife|pharmacist|counsellor|therapist|chiropractor|osteopath))\b")


def _about_a_person(text):
    if AGE_ASK.search(text):
        return True
    return bool(not ASKING_FIRST.search(text) and SEEN_ALREADY.search(text))


def _a_place_not_a_work(text):
    return bool(_THE_OFFICE_IS.search(text)
                or any(phrase in text for phrase in A_PLACE_NOT_A_WORK))


GENRE_START = {
    "jazz": ("*Kind of Blue* by Miles Davis is the one to start with: quiet, unhurried, and every "
             "tune is a simple theme with the solos built on it. Then *Blue Train* by John "
             "Coltrane for something with more muscle, and *Ella and Louis* if you would rather "
             "hear a voice first. Play one album right through twice before you decide - jazz "
             "gives up its tune on the second listen."),
    "classical": ("Start with the short, loud, famous pieces rather than a symphony: Vivaldi's "
                  "*Four Seasons*, the first movement of Beethoven's fifth, and Holst's *The "
                  "Planets*. Then sit with one symphony whole - Beethoven's seventh, or Dvorak's "
                  "*New World* - because the point of the long form is how it carries you from "
                  "the first minute to the last. Films are a good way in too: most film scores "
                  "are classical music that already has your attention."),
    "hip hop": ("*Illmatic* by Nas for words and storytelling, *The Miseducation of Lauryn Hill* "
                "for singing and soul, and *good kid, m.A.A.d city* by Kendrick Lamar for a whole "
                "album that tells one story. Read the words once on paper - rap is the one pop "
                "form where the writing rewards a second pass."),
    "rap": ("*Illmatic* by Nas for words and storytelling, *The Miseducation of Lauryn Hill* for "
            "singing and soul, and *good kid, m.A.A.d city* by Kendrick Lamar for a whole album "
            "that tells one story. Read the words once on paper: rap is the one pop form where "
            "the writing rewards a second pass."),
    "country": ("*Live at Folsom Prison* by Johnny Cash is the doorway: no polish, all story. Then "
                "Dolly Parton's *Jolene* for the songwriting, and Chris Stapleton's *Traveller* if "
                "you want the modern, soul-tinged end of it. Country is story-first, so listen to "
                "the words before the twang."),
    "metal": ("*Paranoid* by Black Sabbath for where it came from, *Master of Puppets* by "
              "Metallica for the playing, and *The Number of the Beast* by Iron Maiden for the "
              "melody. Start with one band, not a playlist: metal makes more sense album by album."),
    "soul": ("*What's Going On* by Marvin Gaye, *Otis Blue* by Otis Redding, and Stevie Wonder's "
             "*Songs in the Key of Life* cover the whole of it - protest, heartbreak and joy. "
             "Motown's *The Ultimate Collection* of singles is the cheap way in if you only know "
             "the hooks."),
    "motown": ("Start with the singles: *The Ultimate Collection* by The Supremes or a Motown "
               "greatest-hits record, then *What's Going On* by Marvin Gaye and Stevie Wonder's "
               "*Songs in the Key of Life* for what the hit factory turned into."),
    "blues": ("*King of the Delta Blues* by Robert Johnson for the source, *Live at the Regal* by "
              "B.B. King for what a guitar can say to a room, and *At Newport* by Muddy Waters for "
              "the electric jump from country blues to the band that became rock."),
    "folk": ("*Pink Moon* by Nick Drake for voice and guitar alone, *Blood on the Tracks* by Bob "
             "Dylan for words, and Fleet Foxes' first album if you want harmony. Folk is words and "
             "one instrument, so start with one person and a guitar."),
    "reggae": ("*Exodus* by Bob Marley and the Wailers is the album, and *Legend* is the singles if "
               "you want the familiar ones first. Then Toots and the Maytals' *Funky Kingston* for "
               "the voice, which is the best shouting in the genre."),
    "punk": ("*Never Mind the Bollocks* by the Sex Pistols for the noise, *London Calling* by The "
             "Clash for what punk did with the rest of music, and *Rocket to Russia* by the "
             "Ramones for songs under three minutes. Loud, short, and it makes sense in a car."),
    "electronic": ("*Discovery* by Daft Punk for tunes, *Selected Ambient Works 85-92* by Aphex "
                   "Twin for the quiet end, and The Chemical Brothers' *Dig Your Own Hole* for the "
                   "big-beat one. Dance music is built to be heard whole, so let an album run."),
    "techno": ("Start with the compilations rather than a single artist: a *Fabric* or *Global "
               "Underground* mix, then Jeff Mills' *The Occurrence* for how stripped back it can "
               "be. Techno is about the build over eight minutes, so give it time."),
    "house": ("*Discovery* by Daft Punk and a *Defected* house compilation cover the friendly end, "
              "then Frankie Knuckles' *Best of* for where the sound started. House is warm and "
              "repetitive on purpose - let it run and it works."),
    "opera": ("Start with *La Boheme* or *Carmen* - two or three hours, famous tunes, and a story "
              "you can follow without the plot notes. Watch a filmed production rather than "
              "listening only, because a lot of what happens is on the faces. Subtitles are normal, "
              "not cheating."),
    "k-pop": ("Start with one group and one record: *Love Yourself: Tear* by BTS, or *Born Pink* by "
              "BLACKPINK if you want the louder one. Watch the videos as well as playing the album -"
              " the visuals are half of what the form is."),
    "gospel": ("*Amazing Grace* by Aretha Franklin, then *The Gospel According to...* by the "
               "Staple Singers, and Mahalia Jackson's *Greatest Hits* for the voice that set the "
               "standard. It is church music first, so the live recordings beat the studio ones."),
    "disco": ("*Saturday Night Fever* is the honest starting point, then Chic's *Risque* for the "
              "guitar and Donna Summer's *Bad Girls* for the voice. Disco is a rhythm, so play it "
              "loud in the kitchen and it explains itself."),
    "indie": ("*Funeral* by Arcade Fire, *Is This It* by The Strokes, and *For Emma, Forever Ago* "
              "by Bon Iver cover the three strands: the big one, the fast one and the quiet one."),
}
MUSIC_START_ASKS = ("get into", "getting into", "start", "starting", "begin", "beginner",
                    "listen", "listening", "recommend", "suggest", "where do i", "where should i",
                    "what should", "which album", "first album", "appreciate", "learn about",
                    "introduce",
                    "difference", "different", "differ", "vs", "versus", "compared")

MUSIC_PAIRS = (
    (("jazz", "blues"),
     "They are cousins and the blues is the older one. Blues is a form: twelve bars, three "
     "chords, a singer telling you what went wrong, and the words matter more than the playing - "
     "start with Robert Johnson or Muddy Waters. Jazz took that feeling and gave the players room "
     "to invent on top of it, so the same tune is different every night - start with *Kind of "
     "Blue*. If you hear a voice carrying the song it is probably the blues; if you hear an "
     "instrument wander off and come back, it is jazz."),
    (("rap", "hip hop"),
     "Rap is the act - someone talking in time over a beat. Hip hop is the whole culture around "
     "it: the beat, the DJ, the dancing, the graffiti, the way people dress. So every rap record "
     "is hip hop, and a hip hop night can go hours without a rapper. For the words, start with "
     "*Illmatic*; for the sound, *The Miseducation of Lauryn Hill*."),
    (("classical", "opera"),
     "Classical is the whole tradition of written music played by an orchestra; opera is the part "
     "of it that is sung on a stage as a play, with costumes and a plot. An opera is classical "
     "music, but most classical music has nobody singing. Start the orchestral side with "
     "Vivaldi's *Four Seasons* and the sung side with *Carmen*."),
)

CARD_GAMES = {
    "uno": ("Deal seven cards each and turn one over as the pile. On your turn put down a card "
            "matching the top one in colour or number, or use the action card you are holding: "
            "skip, reverse, and the +2 make the next player miss or draw. You win by getting rid "
            "of every card, and you must call 'uno' when you are down to one - that is the rule "
            "everyone forgets."),
    "solitaire": ("Deal seven columns of one to seven cards, only the top card of each face up, and "
                  "the rest of the pack face down as the stock. Build the columns downwards in "
                  "alternating colours and the four piles upwards from ace in one suit, moving "
                  "cards between columns as they turn over. Turn the stock one card at a time - "
                  "that is the version most people play; the win is all four suits stacked to "
                  "king."),
    "rummy": ("Deal ten cards each and turn one card face up to start the discard pile. On your "
              "turn draw one from the pack or take the top discard, then throw one away, and lay "
              "down any sets of three or more of the same number or runs of three in one suit when "
              "you can. The first player to get rid of every card wins the hand."),
    "snap": ("Deal the whole pack out between you and turn cards face up into the middle one at a "
             "time. When two cards of the same number land on top of each other, the first person "
             "to shout 'snap' and put a hand flat on the pile takes it. Whoever ends up with "
             "every card wins, and small children are much better at this than adults."),
    "go fish": ("Deal five cards each and spread the rest face down in the middle. On your turn ask "
                "one player for a number you already hold, and if they have it you take the card "
                "and ask again; if not they say 'go fish' and you take one from the middle. Lay "
                "down every pair you complete, and the most pairs at the end wins."),
    "blackjack": ("The aim is to get closer to 21 than the dealer without going over: number cards "
                  "count their number, picture cards ten, and an ace is 1 or 11, whichever helps. "
                  "You are dealt two cards and choose hit or stand; the dealer must draw to 16 and "
                  "stop on 17. Over 21 is a bust and you lose at once, which is why 16 is a bad "
                  "hand to be brave on."),
}
CARD_ASKS = ("rules", "how do i play", "how to play", "how do you play", "how does", "deal",
             "score", "scoring", "win", "wins", "set up", "set up", "start", "teach me",
             "explain")

IN_TUNE = {
    "guitar": ("Clip a tuner on the headstock and take the string order low to high: E, A, D, G, "
               "B, E - the sixth string is the thick one, and the top E is the thin one. Turn the "
               "peg slowly and always come up to the note from below, because slackening down to "
               "it leaves the string ready to slip. Ten seconds a string, and tune every time you "
               "pick it up; guitars move with the room."),
    "bass": ("A clip-on tuner and the string order low to high: E, A, D, G. Turn the peg slowly and "
             "come up to each note from below rather than down onto it. A bass needs tuning less "
             "often than a guitar but goes out if the room changes temperature."),
    "ukulele": ("Clip-on tuner, and the four strings low to high are G, C, E, A - the top G is the "
                "one people get wrong, because on a ukulele it is the higher G, not the lowest "
                "note. Turn the peg in small movements and check the string again after you play a "
                "chord: nylon strings settle slowly and need a week of retuning when they are new."),
    "violin": ("A clip-on tuner and the order G, D, A, E from the lowest string up - and the pegs "
               "are for the big jumps while the fine tuners at the tailpiece do the last bit. Turn "
               "the peg with a little inward pressure so it grips, or it will slip as soon as you "
               "let go."),
    "piano": ("An upright or grand is a job for a tuner, not for you: an annual visit, and twice a "
              "year if it is in a room that gets hot in summer. A digital piano needs nothing. If "
              "one note has gone badly wrong on an acoustic, stop playing it and get the tuner in, "
              "because it is usually a string or a hammer rather than the tuning."),
}
TUNE_ASKS = ("tune", "tuning", "in tune", "out of tune", "stay in tune", "keep in tune",
             "tuned", "sounds wrong", "flat", "sharp", "pitch")

BUZZ_ASKS = ("buzz", "buzzing", "buzzes", "rattles", "rattling", "rattle", "dead note",
             "fret buzz", "sounds tinny", "fret noise")


ACTIVITY_START = {
    "birdwatching": ("Go out with binoculars borrowed from a friend or a reserve's visitor centre "
                     "first, and start with the birds in your own street: the RSPB and the "
                     "Woodland Trust both have a garden bird sheet for free. A pair of 8x42 "
                     "binoculars for about a hundred pounds is the one purchase, second hand is "
                     "fine, and early morning in spring is when everything is singing."),
    "photography": ("Use the phone you already have for a month and finish one project - a colour, "
                    "a street, one tree every day - before you buy a camera. Then a second-hand "
                    "body with a single 35mm or 50mm lens beats a new camera with two bad ones. "
                    "Learn three things first: light behind you, get closer than feels natural, "
                    "and take ten shots of one thing instead of one shot of ten things."),
    "knitting": ("A pair of 4mm needles and a ball of smooth aran wool is the whole kit, about ten "
                 "pounds, and a plain square is the first project. Watch one slow video of knit "
                 "and purl rather than reading about it, make a dishcloth, and only then start a "
                 "scarf. Wool shops and libraries both run free sit-and-knit groups, which is how "
                 "most people get past the first mess."),
    "pottery": ("Book a one-off taster session before you buy anything: most cities have a studio "
                "that runs two-hour wheel evenings for about thirty pounds. If you like it, a "
                "six-week course teaches more than a year of videos, and hand-building at home "
                "needs only clay, a board and a cheap kiln share from the same studio."),
    "woodworking": ("Start with one joint and one small thing - a box, a stool - using hand tools: a "
                    "hardpoint saw, a chisel, a square and a bench hook will do more than a garage "
                    "of machines. Men's sheds and community workshops hire out bench time and "
                    "somebody to ask, which is worth more than the tools when you are starting."),
    "fishing": ("In England and Wales you need a rod licence first - about seven pounds for a "
                "day, from the Environment Agency online - and then a day ticket at a local club "
                "water and a beginner's float rod set for about forty pounds. Go with somebody "
                "who fishes if you can, and learn one knot (the improved clinch), one rig and one "
                "bait before buying anything else. Go in the morning in summer: fishing is mostly "
                "about being somewhere quiet, so the first trip is a success if you enjoy it."),
    "climbing": ("Go to an indoor wall with hired shoes and a taster session first, about twenty "
                 "pounds, and try bouldering: it needs no partner and the routes are the height of "
                 "a room. Give it three visits before you buy shoes, and only then a pair that fits "
                 "tightly. Outdoors comes later, with somebody who already knows how to belay."),
    "painting": ("Start with acrylics: they dry in minutes, clean up with water, and a starter set "
                 "is under twenty pounds. If it is watercolour you want, the paper decides "
                 "everything - cold-pressed 300gsm and no cheaper - and you work light to dark "
                 "because you cannot paint white back in. Either way, paint the same simple thing "
                 "- one mug, one window - five times instead of five different things, and work "
                 "bigger than feels comfortable with one brush that holds a point."),
    "singing": ("Find a choir rather than a teacher first: most towns have a community choir that "
                "takes people who have never sung, no audition, about five pounds a session. "
                "Singing with others teaches pitch faster than singing alone, and the confidence is "
                "most of it. Take a teacher later if you want to sing on your own."),
    "dancing": ("Pick a class that runs a free taster and go with no partner - most salsa, swing and "
                "ceroc nights rotate partners anyway. Wear smooth soles and give it three weeks "
                "before deciding, because the first lesson is always clumsy. A weekly class beats "
                "a course of videos, since the whole thing is other people's timing."),
    "baking": ("Weigh 500g strong white flour, 7g dried yeast, 10g salt and 350ml warm-not-hot "
               "water: that is the whole recipe, and a scale is the only kit you need. Knead ten "
               "minutes, leave it two hours somewhere warm until it has doubled, shape it and bake "
               "it hot. Then bake that same loaf five times rather than five different things - the "
               "first is usually dense and the fifth is usually good, so the only way to fail is "
               "to stop at the first."),
    "sewing": ("A basic machine with a straight stitch and a zigzag is all anyone needs, and a "
               "second-hand one from a repair shop costs less than a new cheap one. Start on "
               "scraps, not clothes: stitch straight lines, then a cushion cover, then take in a "
               "hem on something you do not mind ruining. A local sewing shop's two-hour beginner "
               "class is worth more than a video, because someone sets the tension for you."),
    "board games": ("Go to a board-game cafe or a club night once before buying a box: most of them "
                    "have a shelf and someone who will teach a game in ten minutes. Then buy one "
                    "small game for the people you actually play with, not the one with the best "
                    "reviews. Codenames, Patchwork and Ticket to Ride cover most groups."),
    "yoga": ("Book a beginners' class rather than a video: most studios run a drop-in hatha or "
             "beginner class for about ten to fifteen pounds, and a teacher can see your back, "
             "which a video cannot. Wear something you can move in and borrow a mat - a cheap "
             "6mm mat is the only thing worth buying - and go twice a week for a month before "
             "you judge it. Skip any pose that hurts and tell the teacher about a bad back or "
             "neck before you start."),
    "pilates": ("Start with a beginner mat class, not the reformer: a mat class is about ten to "
                "fifteen pounds, needs only a mat and a cushion, and a teacher who watches you is "
                "the point of it. The one thing to learn first is the breath - wide into the ribs "
                "on the effort, with the belly gently held, never sucked in hard. Twice a week "
                "for a month, and tell the teacher about any back or neck trouble beforehand."),
}
ACTIVITY_ASKS = ("get into", "getting into", "start", "starting", "begin", "beginner", "take up",
                 "taking up", "how do i", "where do i", "any tips", "learn", "try",
                 "cant", "can't", "cannot", "never learnt", "never learned", "never tried")


_PAINTED_SURFACES = frozenset((
    "shed", "sheds", "fence", "fences", "wall", "walls", "door", "doors", "ceiling", "ceilings",
    "cupboard", "cupboards", "cabinet", "cabinets", "tile", "tiles", "radiator", "radiators",
    "bench", "benches", "gate", "gates", "garage", "garages", "greenhouse", "greenhouses",
    "wardrobe", "wardrobes", "skirting", "banister", "banisters", "stairs", "floor", "floors",
    "floorboards", "decking", "deck", "windowsill", "windowsills", "woodwork", "wallpaper",
    "kitchen", "bathroom", "bedroom", "shelf", "shelves",
    "table", "tables", "chair", "chairs", "toy", "toys",
    "stool", "stools", "desk", "desks", "bed", "beds", "cot", "cots", "crib", "cribs",
    "toy box", "toybox", "chest", "trunk", "drawers", "dressing table", "bedside table",
    "picture frame", "photo frame", "mirror frame", "unit", "units", "kitchen unit",
    "kitchen units", "front room", "living room", "lounge", "dining room", "corridor",
    "spare room", "nursery", "staircase", "stair treads", "steps",
    "frame", "frames", "room", "rooms"))
_PAINTED_FAULTS = frozenset((
    "mould", "mold", "mildew", "damp", "creosote", "rust", "peeling", "flaking", "blistering",
    "stripper", "stripping", "strip", "strips"))
_PAINTED_PHRASES = (
    "old paint", "paint stripper", "leftover paint", "left over paint", "spare paint",
    "tin of paint", "tins of paint", "paint tin", "paint tins", "unused paint", "half a tin")


_PAINT_VERBS = frozenset(("paint", "paints", "painted", "painting", "repaint", "repaints",
                          "repainting", "varnish", "varnishing"))


_A_THING_IS_BEING_BAKED = re.compile(
    r"\b(?:bake|bakes|baked|baking)\s+"
    r"(?:a|an|the|my|our|your|his|her|their|some|these|those|two|three|four|half)\s+"
    r"([a-z][a-z'-]*)")
_NOTHING_TO_BAKE = frozenset((
    "bit", "bits", "lot", "lots", "few", "couple", "little", "while", "moment", "time",
    "times", "start", "living", "change", "break", "go", "try", "batch", "whole", "good",
    "better", "decent", "simple", "basic", "proper", "quick", "easy", "beginning",
))


def _a_thing_is_being_baked(text):
    for hit in _A_THING_IS_BEING_BAKED.finditer(text):
        if hit.group(1) not in _NOTHING_TO_BAKE:
            return True
    return False


def _a_surface_is_being_painted(words, padded):
    if not (words & _PAINT_VERBS):
        return False
    if words & _PAINTED_SURFACES or words & _PAINTED_FAULTS:
        return True
    return any(phrase in padded for phrase in _PAINTED_PHRASES)


def _activity_start(memory, understood):
    from .cooking import names_a_dish
    if names_a_dish(understood):
        return None
    text = ((understood.get("clean") or "") + " " + (understood.get("norm_text") or "")).lower()
    if _a_thing_is_being_baked(text):
        return None
    words = set(re.findall(r"[a-z']+", text))
    padded = " %s " % " ".join(re.findall(r"[a-z']+", text))
    if _a_surface_is_being_painted(words, padded):
        return None
    for name in ACTIVITY_START:
        if (" %s " % name) in padded:
            return ACTIVITY_START[name]
    for name in ACTIVITY_VERBS:
        if name in words:
            if name in _FISH_VERBS and _FISH_IS_DINNER.search(text):
                return None
            if name in _PAINT_VERBS and _paints_a_thing(text):
                return None
            return ACTIVITY_START[ACTIVITY_VERBS[name]]
    for name, real in ACTIVITY_OTHER_NAMES.items():
        if (" %s " % name) in padded:
            return ACTIVITY_START[real]
    return None


_FISH_VERBS = frozenset(("fish", "fishing", "fished"))
_FISH_IS_DINNER = re.compile(
    r"\b(?:cook|cooks|cooked|cooking|fry|fries|fried|frying|bake|baked|baking|poach|poached|"
    r"steam|steamed|grill|grilled|oven|pan|pan[s]?|skillet|dinner|tea|supper|lunch|recipe|"
    r"falls? apart|falling apart|breaks? up|breaking up|to bits|crumbles?)\b")


_PAINT_VERBS = frozenset(("paint", "paints", "painting", "painted", "repaint", "repainting"))
_PAINTED_THINGS = re.compile(
    r"\b(?:paint|paints|painting|painted|repaint|repainting)\s+(?:a|an|the|my|our|his|her|their|"
    r"this|that|these|those|its|it)\s+(?:[a-z]+\s+)?(?:window|windows|sash|casement|door|doors|"
    r"wall|walls|ceiling|ceilings|shed|sheds|fence|fences|gate|garage|radiator|radiators|"
    r"skirting|trim|woodwork|wood|cupboard|cupboards|cabinets|cabinet|wardrobe|wardrobes|"
    r"table|tables|chair|chairs|furniture|floor|floors|floorboards|banister|banisters|"
    r"frame|frames|sill|sills|panel|panels|front door|garage door|back door|french doors|"
    r"patio|deck|decking\b)")


_PAINT_AS_A_THING = re.compile(
    r"\b(?:get rid of|dispose of|throw away|throwing away|throw out|bin|recycle|take|taking|"
    r"old|leftover|left over|spare|unused|surplus|half a tin|half used|" 
    r"tin of|tins of|paint tin|paint tins|tin|tins|pot of|tube of|" 
    r"how much|how many|much does|cost of|price of|litres|liters|gallons|coverage|" 
    r"which|what kind of|best|cheapest|store|storing|keep|keeping|freeze|frozen|skin on|"
    r"goes off|gone off|gone hard|separated)\s+(?:[a-z]+\s+){0,2}paint\b")


_PAINT_COLOURS = re.compile(
    r"\bpaint(?:s|ed|ing)?\b(?:\s+[a-z']+){0,2}\s+colou?rs?\b"
    r"|\bcolou?r(?:s|ed)?\b(?:\s+[a-z']+){0,2}\s+paint(?:s|ed|ing)?\b"
    r"|\bcolou?r\s+scheme\b|\bpaint\s+scheme\b|\bcolou?r\s+palette\b")


def _paints_a_thing(text):
    return bool(_PAINTED_THINGS.search(text) or _PAINT_AS_A_THING.search(text)
                or _PAINT_COLOURS.search(text))


ACTIVITY_VERBS = {
    "sing": "singing", "sings": "singing", "dance": "dancing", "dances": "dancing",
    "bake": "baking", "bakes": "baking", "knit": "knitting", "knits": "knitting",
    "paint": "painting", "paints": "painting", "sew": "sewing", "sews": "sewing",
    "photograph": "photography", "pottery": "pottery", "fish": "fishing", "climb": "climbing",
}


ACTIVITY_OTHER_NAMES = {
    "choir": "singing", "singing lessons": "singing", "choir practice": "singing",
    "watercolour": "painting", "watercolours": "painting", "watercolors": "painting",
    "acrylics": "painting", "acrylic paint": "painting",
    "fly fishing": "fishing", "sea fishing": "fishing", "bouldering": "climbing",
}


ORDINARY_GENRES = ("house", "country", "soul", "metal", "folk", "gospel", "punk", "indie")
MUSIC_KINDS_AFTER = ("rock", "pop", "ska", "reggae", "techno", "disco", "grime", "hip hop",
                     "hip-hop", "classical", "opera", "rap", "jazz", "blues", "soul", "metal",
                     "punk", "house", "country", "folk", "indie", "gospel", "dance", "electronic",
                     "edm", "r&b", "rnb", "swing", "bluegrass", "ambient", "trance", "dubstep",
                     "drum and bass", "dnb", "hardcore", "shoegaze", "motown", "afrobeat")
GENRE_WORDS_AFTER = MUSIC_KINDS_AFTER + (
                     "music", "dj", "djs", "track", "tracks", "album", "albums", "mix", "mixes",
                     "tune", "tunes", "band", "bands", "sound", "sounds", "scene", "song",
                     "songs", "record", "records", "remix", "label", "vinyl", "era",
                     "compilation", "classics", "classic", "genre", "guitar", "piano", "singing",
                     "vocals", "drums", "artists", "artist", "singers", "singer", "history",
                     "set", "sets", "festival", "gig", "gigs", "club", "clubs", "instruments",
                     "legends", "standards", "pioneers", "era")
GENRE_NAMES_BEFORE = ("a", "an", "the", "my", "our", "your", "his", "her", "their", "this",
                      "that", "these", "those", "another")
GENRE_NOT_DESCRIBED_BY = ("you", "youd", "youll", "youve", "your", "i", "im", "id", "ill",
                          "we", "weve", "wed", "they", "theyd", "he", "she", "it", "could",
                          "would", "should", "can", "will", "shall", "might", "must", "please",
                          "recommend", "suggest", "thanks", "thank", "then", "too", "even")


def _an_ordinary_word(name, text):
    if name not in ORDINARY_GENRES:
        return False
    for hit in re.finditer(r"\b" + name + r"\b", text):
        after = text[hit.end():].split()
        follows = after[0].strip(",.!?;:") if after else ""
        before = text[:hit.start()].split()
        if follows in GENRE_WORDS_AFTER:
            continue
        if before and before[-1].strip(",.!?;:") in GENRE_NAMES_BEFORE:
            return True
        if follows in ("and", "or", "vs", "versus", "is") or follows in GENRE_NOT_DESCRIBED_BY:
            continue
        if follows:
            return True
    return False


def _genre_start(memory, understood):
    text = ((understood.get("clean") or "") + " " + (understood.get("norm_text") or "")).lower()
    if "countryside" in text or "village" in text or "walk in the country" in text:
        return None
    comparing = any(w in text for w in ("difference", "different", "differ", " vs ", "versus",
                                        "compared", "compare"))
    if comparing:
        for pair, difference in MUSIC_PAIRS:
            if all(name in text for name in pair):
                return difference
    for name in ("hip hop", "k-pop", "kpop", "r&b", "house music", "dance music", "electronic",
                 "techno", "classical", "country", "metal", "motown", "soul", "blues", "folk",
                 "reggae", "opera", "punk", "indie", "gospel", "disco", "jazz", "rap", "house"):
        if name in GENRE_START and name in text:
            typed = (understood.get("clean") or understood.get("norm_text") or text).lower()
            if _an_ordinary_word(name, typed):
                return None
            return GENRE_START[name]
    return None


def _card_game(memory, understood):
    text = ((understood.get("clean") or "") + " " + (understood.get("norm_text") or "")).lower()
    for name, game in (("uno", "uno"), ("solitaire", "solitaire"), ("patience", "solitaire"),
                       ("rummy", "rummy"), ("snap", "snap"), ("go fish", "go fish"),
                       ("blackjack", "blackjack"), ("pontoon", "blackjack"),
                       ("twenty one", "blackjack")):
        if name in text:
            return CARD_GAMES.get(game)
    return None


def _in_tune(memory, understood):
    text = ((understood.get("clean") or "") + " " + (understood.get("norm_text") or "")).lower()
    if "piano" in text or "keyboard" in text:
        return IN_TUNE["piano"]
    for name in ("guitar", "bass", "ukulele", "violin", "fiddle", "cello", "banjo", "mandolin"):
        if name in text:
            if name in ("bass",):
                return IN_TUNE["bass"]
            if name in ("violin", "fiddle", "cello"):
                return IN_TUNE["violin"]
            return IN_TUNE["guitar" if name in ("banjo", "mandolin") else name]
    return None


def _buzz(memory, understood):
    text = ((understood.get("clean") or "") + " " + (understood.get("norm_text") or "")).lower()
    return ("One buzzing string is usually that string: old, kinked, or sitting too low in its "
            "nut, so change it first and see. Buzz that follows one fret up and down the neck is "
            "that fret or the neck; buzz on every note is usually how hard you are picking, so try "
            "a lighter touch and press just behind the fret rather than on top of it. If it still "
            "rattles in the same place with a new string, the action is too low or the neck has "
            "moved - a shop sets that up for about forty pounds, and it is worth it, because no "
            "amount of technique fixes a guitar set up badly.")


def _worth_it(memory, understood):
    text = (understood.get("clean") or understood.get("norm_text") or "").lower()
    if _about_a_person(text) or _a_place_not_a_work(text):
        return None
    title = _work_named(text)
    return VIEWS[title] if title else None


def _worth_it_unnamed(memory, understood):
    text = (understood.get("clean") or understood.get("norm_text") or "").lower()
    if _about_a_person(text) or _work_named(text) or _a_place_not_a_work(text):
        return None
    if any(word in text for word in NOT_A_VERDICT):
        return None
    if A_PERSON_TO_CONSULT.search(text):
        return None
    if not any(phrase in text for phrase in JUDGE_ASKS):
        return None
    named = _named_work(text)
    if named:
        return ("I don't know *%s* well enough to call it honestly. Tell me what you liked about "
                "the last thing you enjoyed and I'll say whether it's that kind." % named)
    return ("Not one I can call honestly, sorry. Name the last thing you enjoyed and I'll say "
            "whether this one is that kind of thing.")


def _named_work(text):
    cuts = ("worth", "any good", "good", "boring", "like", "as good", "better", "any cop",
            "in the", "or", "on", "at", "tonight", "with", "because", "before", "after", "if",
            "but", "for me", "or not", "yet", "then",
            "my", "your", "his", "her", "our", "their")
    patterns = (r"\b(?:is|are|was)\s+((?:the\s+|this\s+|that\s+)?[a-z0-9'&: -]{2,40})",
                r"\b(?:watch|watching|read|reading|see|play)\s+((?:the\s+|a\s+)?"
                r"[a-z0-9'&: -]{2,40})")
    for pattern in patterns:
        found = re.search(pattern, text)
        if not found:
            continue
        title = found.group(1)
        for cut in cuts:
            title = re.split(r"\b" + re.escape(cut) + r"\b", title)[0]
        title = title.strip(" .?!,-\t")
        if not title or title in ("it", "this", "that", "something", "anything", "one",
                                 "worth", "the", "a", "an"):
            continue
        return _display(title)


def _table_pick(text):
    about_a_work = (any(word in text for word in WORK_EVIDENCE)
                    or any(phrase in text for phrase in NEXT_EVIDENCE))
    for title, reply in FILM_MATCHES:
        if not re.search(r"\b" + re.escape(title) + r"\b", text):
            continue
        if title in PLAIN_TITLES:
            if any(phrase in text for phrase in PLAIN_SENSE[title]):
                continue
            if not about_a_work:
                continue
        return reply
    return ""


def _after_named(memory, understood):
    text = ((understood.get("clean") or "") + " " + (understood.get("norm_text") or "")).lower()
    return _table_pick(text)


SUBJECT_BOOKS = {
    "psychology": ("*Thinking, Fast and Slow* by Daniel Kahneman is the one that changes how you "
                   "see your own decisions, though it is a long read; *The Man Who Mistook His "
                   "Wife for a Hat* by Oliver Sacks is the shorter, stranger way in."),
    "philosophy": ("*Think* by Simon Blackburn is written for someone who has never read any: a "
                   "chapter a question, no jargon. *Sophie's World* by Jostein Gaarder tells the "
                   "whole history of it as a novel if you want the story instead."),
    "economics": ("*The Undercover Economist* by Tim Harford explains prices, markets and why "
                  "things cost what they do without a single equation. *The Armchair Economist* "
                  "by Steven Landsburg is the more argumentative one."),
    "science": ("*A Short History of Nearly Everything* by Bill Bryson is the one to start with: "
                "how we know what we know, and funny throughout. *The Selfish Gene* by Richard "
                "Dawkins if it is evolution you want."),
    "climate": ("*How to Avoid a Climate Disaster* by Bill Gates is the plainest account of where "
                "the emissions actually come from and what would fix each one, without the "
                "gloom. *The Uninhabitable Earth* by David Wallace-Wells is the bleak one."),
    "maths": ("*Alex's Adventures in Numberland* by Alex Bellos is maths as stories about people "
              "and puzzles, so nothing feels like homework. *How Not to Be Wrong* by Jordan "
              "Ellenberg is the one about using it to think."),
    "politics": ("*How Westminster Works... and Why It Doesn't* by Ian Dunt is the short angry "
                 "guide to how British government actually runs. *The Prince* by Machiavelli if "
                 "you want the old one people still quote."),
    "poetry": ("*Staying Alive* edited by Neil Astley is the anthology to start with: modern poems "
               "in English, sorted by what they are about rather than by poet. Read one a night "
               "and skip anything that does not land."),
    "language": ("*The Language Instinct* by Steven Pinker is the readable one on how language "
                 "works in the head, and *Mother Tongue* by Bill Bryson is the fun history of "
                 "English if that is the half you want."),
    "gardening": ("*How to Garden* (DK) is the beginner's standard: a photograph for every job, "
                  "month by month, and no assumed knowledge. *The Allotment Book* by Andi Clevely "
                  "if it is a plot rather than a border."),
    "chess": ("*Bobby Fischer Teaches Chess* is all positions and no theory, so you learn by "
              "doing, and free games online afterwards make it stick. *Chess for Dummies* if you "
              "want the openings named as well."),
    "knitting": ("*Stitch 'n Bitch* by Debbie Stoller: cast on, knit, purl, then patterns you can "
                 "actually finish. A pair of 4mm needles and a ball of aran wool is the whole kit "
                 "and it costs about ten pounds."),
    "crochet": ("*The Happy Hooker* by Debbie Stoller is the crochet one from the same series: the "
                "stitches step by step, then small things worth making. One 4mm hook and a ball of "
                "aran wool to start."),
    "sewing": ("*The Sewing Book* by Alison Smith (DK) photographs every technique from a hem to a "
               "zip, so it stays useful for years. Practise on an old pillowcase rather than good "
               "fabric."),
    "drawing": ("*Drawing on the Right Side of the Brain* by Betty Edwards, because beginners draw "
                "what they think is there instead of what is, which is the thing the exercises "
                "fix. A 2B pencil and cheap paper is the kit."),
    "painting": ("*Watercolour for the Absolute Beginner* by Matthew Palmer: three washes and you "
                 "have painted something, with nothing assumed. Cold-pressed 300gsm paper decides "
                 "more than the paints do, and acrylics are the easier way in."),
    "photography": ("*Understanding Exposure* by Bryan Peterson, since exposure is what separates a "
                    "snapshot from a photograph and the book works on any camera, phone included."),
    "guitar": ("*Hal Leonard Guitar Method, Book 1*: chords and songs from the first pages, with the "
               "audio included. Any cheap acoustic plays well enough to learn on."),
    "piano": ("*Alfred's Basic Adult Piano Course, Book 1* starts at the very beginning and has "
              "both hands together within a few pages. A 61-key keyboard is enough to learn on."),
    "baking": ("*Flour Water Salt Yeast* by Ken Forkish for bread: four ingredients, a schedule, and "
               "a loaf that tastes like a bakery's. *The Great British Bake Off: How to Bake* if it "
               "is cakes and pastry you want."),
    "cooking": ("*Salt, Fat, Acid, Heat* by Samin Nosrat teaches why a dish works, so you stop "
                "following recipes. *Delia's Complete Cookery Course* if you would rather be told "
                "exactly what to do."),
    "running": ("*Run Walk Run* by Jeff Galloway: walking breaks get a beginner to 5k without the "
                "injuries that stop people. Get shoes fitted at a running shop rather than bought "
                "from a supermarket."),
    "yoga": ("*Light on Yoga* by B.K.S. Iyengar is the classic reference, but go to two or three "
             "classes first, because a book cannot see your back."),
    "dog training": ("*Perfect Puppy* by Gwen Bailey covers the first weeks, house training and the "
                     "five things to teach first. *The Dog Listener* by Jan Fennell if the dog is "
                     "out of puppyhood already."),
    "birdwatching": ("*The RSPB Pocket Guide to British Birds* names what you are looking at, and a "
                     "pair of 8x42 binoculars is the one purchase: second hand is fine, and the "
                     "garden birds are the place to start."),
    "astronomy": ("*Turn Left at Orion* by Guy Consolmagno: what to look for first from a back "
                  "garden, and where it is. Binoculars find most of it, so no telescope yet."),
    "coding": ("*Python Crash Course* by Eric Matthes, which has you build a game and a small web "
               "app instead of reading about variables. Free tutorials afterwards are fine."),
    "investing": ("*Smarter Investing* by Tim Hale: the boring index-fund argument, with the numbers "
                  "and the costs. Nothing else is needed until that makes sense."),
    "money": ("*Money: A User's Guide* by Laura Whateley takes bills, debt, pensions and savings in "
              "the order they matter for somebody in the UK."),
    "history": ("*A Little History of the World* by E. H. Gombrich: short chapters, written for a "
                "child but never childish, and it gives you the map everything else hangs on."),
    "wine": ("*Wine Folly* by Madeline Puckette shows the grapes and regions as pictures, which is "
             "how they stick, and the tasting words come after."),
    "woodworking": ("*Woodworking Basics* by Peter Korn takes one joint at a time with hand tools, "
                    "which is the right order. A hardpoint saw, a chisel, a square and a bench hook "
                    "do more than a garage of machines."),
    "fishing": ("*Fishing for Dummies* covers the rig, the bait and the knots for coarse fishing, and "
                "a day ticket at a club water is the way to try it. Rod licence first if you are in "
                "England or Wales."),
    "climbing": ("*How to Rock Climb!* by John Long is the standard for the basics, ropes and knots. "
                 "Go to an indoor wall with hired shoes and try bouldering first, since it needs no "
                 "partner."),
    "diy": ("*The Reader's Digest Complete DIY Manual* covers the jobs in a house from a shelf to a "
            "radiator, and a Haynes manual for your own model if it is the car."),
    "car": ("A Haynes manual for your exact model, since the engine has to match, plus a socket set. "
            "That covers servicing, brakes and most of an MOT."),
}
SUBJECT_BOOK_NAMES = {
    "psychology": "psychology", "the mind": "psychology", "the brain": "psychology",
    "neuroscience": "psychology", "human behaviour": "psychology", "human behavior": "psychology",
    "philosophy": "philosophy", "philosophers": "philosophy",
    "economics": "economics", "the economy": "economics",
    "science": "science", "physics": "science", "chemistry": "science",
    "biology": "science", "evolution": "science", "the universe": "science",
    "climate change": "climate", "climate": "climate", "the climate": "climate",
    "maths": "maths", "mathematics": "maths", "numbers": "maths",
    "politics": "politics", "government": "politics",
    "poetry": "poetry", "poems": "poetry",
    "language": "language", "linguistics": "language", "grammar": "language",
    "gardening": "gardening", "allotment": "gardening", "allotments": "gardening",
    "grow your own": "gardening", "vegetable patch": "gardening", "veg patch": "gardening",
    "vegetable garden": "gardening", "garden": "gardening",
    "chess": "chess",
    "knitting": "knitting", "knit": "knitting",
    "crochet": "crochet",
    "sewing": "sewing", "sew": "sewing", "dressmaking": "sewing",
    "drawing": "drawing", "draw": "drawing", "sketching": "drawing", "sketch": "drawing",
    "watercolour": "painting", "watercolours": "painting", "watercolor": "painting",
    "painting": "painting", "paint": "painting", "acrylics": "painting",
    "photography": "photography",
    "guitar": "guitar",
    "piano": "piano", "keyboard": "piano",
    "bread": "baking", "breadmaking": "baking", "baking": "baking", "bake": "baking",
    "cooking": "cooking", "cook": "cooking",
    "running": "running", "run": "running", "jogging": "running",
    "yoga": "yoga",
    "dog training": "dog training", "training a puppy": "dog training",
    "puppy training": "dog training",
    "birdwatching": "birdwatching", "bird watching": "birdwatching", "birds": "birdwatching",
    "astronomy": "astronomy", "stargazing": "astronomy", "the stars": "astronomy",
    "coding": "coding", "programming": "coding", "python": "coding", "javascript": "coding",
    "code": "coding", "web design": "coding",
    "investing": "investing", "investment": "investing", "index funds": "investing",
    "stocks and shares": "investing",
    "money": "money", "budgeting": "money", "personal finance": "money",
    "history": "history",
    "wine": "wine",
    "woodworking": "woodworking", "carpentry": "woodworking", "woodwork": "woodworking",
    "fishing": "fishing", "fly fishing": "fishing", "sea fishing": "fishing",
    "climbing": "climbing", "bouldering": "climbing",
    "diy": "diy", "home repairs": "diy", "plumbing": "diy", "tiling": "diy",
    "car maintenance": "car", "servicing my car": "car", "car": "car",
}
SUBJECT_BOOK_UNCOVERED = ("pottery", "ceramics", "singing", "dancing", "board games",
                          "poker", "bridge", "golf", "tennis", "beekeeping", "calligraphy",
                          "horse riding", "skiing", "snowboarding", "surfing", "boxing",
                          "martial arts", "meditation", "wild swimming", "swimming", "snooker",
                          "darts", "genealogy", "family history", "astrology", "tarot",
                          "public speaking", "origami", "embroidery", "quilting", "rug making",
                          "home brewing", "beer brewing", "foraging", "mushrooms", "mycology",
                          "bees", "chickens", "keeping chickens", "allotmenteering",
                          "second world war", "world war", "first world war", "ww2", "ww1",
                          "war", "wars")
_SUBJECT_BOOK_ORDER = sorted(SUBJECT_BOOK_NAMES, key=len, reverse=True)
_SUBJECT_UNCOVERED_ORDER = sorted(SUBJECT_BOOK_UNCOVERED, key=len, reverse=True)
_BOOK_ANCHOR = re.compile(
    r"\b(?:about|on|covering|teach(?:es)?|"
    r"for beginners? (?:at|in|to)|"
    r"beginners? (?:guide to|book (?:on|about))|"
    r"for (?:someone|somebody|anyone|anybody|people|a person"
    r"|my (?:mum|mom|dad|mother|father|brother|sister|son|daughter|wife|husband|partner"
    r"|friend|nan|gran|grandad|grandma|grandpa))"
    r" (?:who|that) (?:likes?|loves?|enjoys?|is into|is a fan of|is interested in|is keen on)|"
    r"(?:who|that) (?:likes?|loves?|enjoys?|is into|is a fan of|is interested in|is keen on)|"
    r"(?:someone|somebody|anyone|anybody|people|a person)"
    r" (?:interested in|keen on|into)|"
    r"(?:if|when) (?:i|you|they|he|she|im|i'm) (?:like|love|enjoy|am into|are into|is into)|"
    r"a fan of|interested in|keen on|"
    r"(?:to|for) learn(?:ing)?)\b\s+(.{0,40})")


def _says(phrase, text):
    return re.search(r"(?<![a-z])" + re.escape(phrase) + r"(?![a-z])", text) is not None


_BOOK_SUBJECT_BEFORE = re.compile(r"([a-z' ]{0,40})\bbooks?\b")


def _book_subject(text):
    match = _BOOK_ANCHOR.search(text)
    if match:
        tail = match.group(1)
    else:
        before = _BOOK_SUBJECT_BEFORE.search(text)
        if not before:
            return None, False
        tail = before.group(1)
    for phrase in _SUBJECT_BOOK_ORDER:
        if _says(phrase, tail):
            return SUBJECT_BOOKS[SUBJECT_BOOK_NAMES[phrase]], True
    for phrase in _SUBJECT_UNCOVERED_ORDER:
        if _says(phrase, tail):
            return None, True
    return None, False


def _book_thriller(memory, understood):
    text = ((understood.get("clean") or "") + " " + (understood.get("norm_text") or "")).lower()
    if "thursday murder club" in text:
        return ("The next one is *The Man Who Died Twice* by Richard Osman, the same four friends "
                "again. For a different author, *The Marlow Murder Club* by Robert Thorogood is "
                "close in tone, or *The Silent Patient* if you want a darker twist.")
    return ("*The Silent Patient* by Alex Michaelides and *The Thursday Murder Club* by Richard "
            "Osman are both quick and hard to put down; the second one is much funnier. Tana "
            "French's *In the Woods* if you want something longer and darker.")


def _book_about(memory, understood):
    if not _a_genre_is_the_taste(understood):
        return None
    text = ((understood.get("clean") or "") + " "
            + (understood.get("norm_text") or "")).lower()
    pick, _named = _book_subject(text)
    return pick


_RESERVING_PHRASES = ("book a", "book an", "book the", "book my", "book our", "book some",
                      "to book", "booking a", "booking the", "booked a", "booked the",
                      "book it", "reserve a", "reserve the", "reserved a",
                      "booked for", "booked in", "booked up", "booked with", "is booked",
                      "are booked", "was booked", "were booked", "be booked", "got booked")

_BOOK_VERB_BEFORE = re.compile(
    r"\b(?:should|shall|can|could|must|might|would|will|do|does|did|need|needs|needed|"
    r"worth|to|lets|let's)\s+(?:we\s+|i\s+|you\s+|they\s+|he\s+|she\s+|it\s+)?"
    r"book(?:ing|ed)?\b")
_BOOK_VERB_AFTER = re.compile(
    r"\bbook(?:ing|ed)?\s+(?:first|now|ahead|early|before|soon|online|today|tonight|"
    r"tickets?|in advance|up)\b")
_A_DETERMINER_JUST_BEFORE = re.compile(
    r"\b(?:a|an|the|this|that|my|our|your|his|her|their|its|any|some|no|each|every|"
    r"another|one|same|next|other|good|great|new|second|third)\s+(?:\w+\s+)?$")

def _not_a_reservation(understood):
    if _a_judged_work_named(understood):
        return False
    return not the_book_is_a_reservation(understood)


def _a_judged_work_named(understood):
    text = ((understood.get("clean") or "") + " "
            + (understood.get("norm_text") or "")).lower()
    if not _work_named(text):
        return False
    return any(_says(word, text) for word in JUDGE_WORDS)


def the_book_is_a_reservation(understood):
    for reading in (understood.get("clean"), understood.get("norm_text")):
        if _a_reservation(str(reading or "").lower()):
            return True
    return False


def _a_reservation(text):
    if not text.strip():
        return False
    if any(_says(phrase, text) for phrase in _RESERVING_PHRASES):
        return True
    if _BOOK_VERB_BEFORE.search(text):
        return True
    for match in _BOOK_VERB_AFTER.finditer(text):
        before = text[:match.start()]
        if not _A_DETERMINER_JUST_BEFORE.search(before):
            return True
    return False





_NEAR_ME = re.compile(r"\bnear(?:\s+me|\s+here|by)\b|\bnear\s+where\s+i", re.I)
_SAYS_WHAT_IS_ON = re.compile(
    r"\b(?:on|showing|playing|listings|line[- ]?up|schedule)\b"
    r"|\b(?:tonight|today|this\s+(?:week|weekend|month))\b", re.I)
_ASKS_IF_OPEN = re.compile(
    r"\b(?:open|opens|opening|closed|closes|closing|shut|hours|times)\b", re.I)


def _a_listings_ask_near_me(understood):
    text = " ".join(str((understood or {}).get("clean") or "").lower().split())
    if not _NEAR_ME.search(text):
        return True
    if _ASKS_IF_OPEN.search(text):
        return False
    return bool(_SAYS_WHAT_IS_ON.search(text))


_A_BOOK_I_AM_NOT_ENJOYING = re.compile(
    r"\b(?:boring|bored\s+(?:of|with)|a\s+slog|so\s+slow|really\s+slow|not\s+enjoying|"
    r"can'?t\s+get\s+into|cant\s+get\s+into|gave\s+up\s+on|rubbish|terrible|awful|dull)\b")
_ASKS_FOR_A_PICK = re.compile(
    r"\b(?:recommend|suggest|suggestion|any\s+good|something|what\s+should\s+i\s+read|"
    r"what\s+to\s+read|what\s+can\s+i\s+read|a\s+book\s+(?:that|to|for|about)|"
    r"what\s+book|which\s+book|any\s+ideas|ideas\s+for)\b")


def _book_recommend(memory, understood):
    earlier = " ".join(str(turn.get("user") or "")
                        for turn in (memory.get("turns") or [])[-3:])
    said = ((understood.get("clean") or "") + " "
            + (understood.get("norm_text") or "")).lower()
    pick, named = _book_subject(said)
    if named:
        return pick
    if _A_BOOK_I_AM_NOT_ENJOYING.search(said) and not _ASKS_FOR_A_PICK.search(said):
        return ("Put it down - finishing a book you are not enjoying is not a virtue, and 50 "
                "pages is a fair trial before you give up on it. If you want another: *The "
                "Thursday Murder Club* by Richard Osman is funny with short chapters, *The "
                "Silent Patient* if you want a twist, and *The Midnight Library* by Matt Haig if "
                "you want something to think about. What did the last one you loved have that "
                "this one has not?")
    context = ((understood.get("clean") or "") + " " + earlier).lower()
    named = _book_title_named(context)
    if named:
        context = context.replace(named, " ")
        if not any(word in context for word in ("son", "daughter", "child", "kid", "year old",
                                                "grandson", "granddaughter", "niece", "nephew",
                                                "teenager")):
            return _book_like(memory, understood)
    if any(word in context for word in ("baby", "babies", "toddler", "one year old",
                                        "two year old", "18 months", "six months",
                                        "nine months", "newborn")):
        return ("For a baby, board books that survive being chewed and pulled: *The Very Hungry "
                "Caterpillar* by Eric Carle, *Dear Zoo* by Rod Campbell, *Where's Spot?* by Eric "
                "Hill, or any of the *That's Not My...* touchy-feely books. Read the same three or "
                "four over and over - the repetition is the point at that age - and let them turn "
                "the pages, even if it slows you down.")
    if any(word in context for word in ("my class", "the class", "assembly", "story time",
                                        "storytime", "reception class", "nursery")):
        return ("For reading aloud to a group: *The Gruffalo* by Julia Donaldson for the rhymes, "
                "*The Tiger Who Came to Tea* by Judith Kerr for the pause at the doorbell, and "
                "*Oi Frog!* by Kes Gray for the joke on every page. *The Gruffalo* is the safest "
                "one for a mixed group: the rhythm carries it and there is a repeated line they "
                "can join in with.")
    if any(word in context for word in ("daughter", "son", "child", "kid", "year old",
                                        "grandson", "granddaughter", "niece", "nephew",
                                        "teenager")):
        return ("For a younger reader: *The Bolds* by Julian Clary (funny on every page), "
                "*The Worst Witch* (short chapters), *The Explorer* by Katherine Rundell for "
                "animals and adventure, or *Dog Man* if comics are easier. Start with *The Bolds* "
                "or *Dog Man*: jokes first, and no long descriptions to get through.")
    return ("*The Thursday Murder Club* by Richard Osman is the safest pick: funny, short "
            "chapters, easy to pick up. For something darker, *The Silent Patient*; for a "
            "younger reader, *Wonder* by R. J. Palacio or *The Explorer* by Katherine Rundell. "
            "Tell me what you last enjoyed and I'll narrow it down.")


MOODS = {
    "sad": ("sad", "cry", "crying", "cries", "tears", "tearjerker", "tear jerker",
            "heartbreaking", "heartbroken", "heartbreak", "emotional", "moving", "weepy",
            "sob", "sob story", "devastating", "break my heart", "breaks my heart",
            "make me cry", "makes me cry", "made me cry"),
    "funny": ("funny", "laugh", "laughing", "laughs", "hilarious", "comedy", "comedies",
              "cheer me up", "cheering up", "makes me laugh", "make me laugh"),
    "scary": ("scary", "scariest", "scare", "scares", "horror", "frightening", "creepy",
              "terrifying", "spooky", "jump scares", "ghost story", "halloween"),
    "think": ("makes me think", "make me think", "makes you think", "make you think",
              "thought provoking", "clever", "thoughtful", "philosophical", "mind bending"),
    "uplifting": ("uplifting", "uplifted", "cheerful", "feel good", "feelgood",
                  "heartwarming", "heart warming", "happy", "hopeful", "comforting",
                  "not depressing", "isnt depressing", "isn't depressing", "nothing depressing",
                  "not miserable", "nothing miserable", "not gloomy", "nothing gloomy",
                  "not bleak", "not heavy", "nothing heavy", "nothing sad"),
    "gripping": ("gripping", "page turner", "page turners", "pageturner", "not put it down",
                 "not put down", "not stop reading", "unputdownable", "exciting", "addictive",
                 "tense", "edge of my seat", "hard to put down", "able to put down",
                 "up all night reading", "read in one sitting", "read it in one go",
                 "read at one go"),
    "short": ("short", "shortest", "quick", "quickest", "not too long", "one sitting"),
    "true": ("true story", "true stories", "based on a true story", "real story", "real life",
             "nonfiction", "non fiction", "biography", "memoir", "documentary"),
    "twist": ("twist", "twists", "twisty", "surprise ending", "shock ending"),
    "romance": ("romantic", "romance", "love story", "rom com", "romcom"),
    "light": ("light", "lighthearted", "cosy", "cozy", "gentle", "relaxing", "relaxed",
              "unwind", "wind down", "chill", "chill out", "easy going", "easy watching",
              "fall asleep", "asleep", "to sleep to", "drowse off", "doze",
              "easy read", "nothing heavy", "easy to watch", "switch my brain off",
              "switch off to", "turn my brain off", "brain off", "no thinking",
              "dont want to think", "nothing demanding"),
}
MOOD_ORDER = ("sad", "funny", "scary", "think", "uplifting", "gripping", "short", "true",
              "twist", "romance", "light")
NEGATORS = frozenset(("not", "no", "never", "without", "nothing", "none", "hate", "hates",
                      "avoid", "hardly", "barely"))
CONTRACTIONS = {
    "aint": "are not", "arent": "are not", "cant": "can not", "couldnt": "could not",
    "didnt": "did not", "doesnt": "does not", "dont": "do not", "hadnt": "had not",
    "hasnt": "has not", "havent": "have not", "isnt": "is not", "shouldnt": "should not",
    "wasnt": "was not", "werent": "were not", "wont": "will not", "wouldnt": "would not",
}
SOFT = frozenset(("too", "very", "that", "so", "much", "a", "really", "quite", "at", "all"))
WANTING = frozenset(("want", "wanted", "wants", "like", "likes", "liked", "fancy", "enjoy", "mind"))

FILM_MOODS = {
    "sad": ("For a good cry: *Manchester by the Sea* is quiet and devastating, *Atonement* lands "
            "its ending like a brick, and *Up* does it in the first ten minutes. Have tissues "
            "ready."),
    "funny": ("For laughs: *What We Do in the Shadows* (a daft vampire mockumentary), *The Nice "
              "Guys* (funny and twisty) or *Paddington 2*, which makes almost everyone laugh."),
    "think": ("*Arrival* (would you want to know the future?), *12 Angry Men* (one room, all "
              "talk, gripping) or *Ex Machina* (quiet, unsettling science fiction). All three "
              "stay with you afterwards."),
    "uplifting": ("*Hunt for the Wilderpeople* (funny and warm), *The Shawshank Redemption* (hope "
                  "you have to earn) or *Sing Street* (music, first love and a big grin at the "
                  "end)."),
    "gripping": ("*Prisoners* is tense from the first scene, *Gone Girl* keeps you guessing to "
                 "the end, and *Sicario* turns the screw for two hours straight."),
    "short": ("*Before Sunset* runs 80 minutes, *Locke* is 85 with one man in a car, and *Toy "
              "Story* is 81. All three are short and none of them asks much of a tired evening."),
    "true": ("*Zodiac* (the investigation, not the killings), *Catch Me If You Can* (light and a "
             "lot of fun) or *127 Hours* if you want to be on the edge of your seat."),
    "twist": ("*The Sixth Sense*, *The Prestige* and *Gone Girl* all turn on a twist you will "
              "not see coming. Start with *The Prestige*."),
    "romance": ("*Before Sunrise* (two people talking all night), *When Harry Met Sally* (the "
                "funny one) or *Pride & Prejudice* (2005) for the longing and the costumes."),
    "light": ("*Paddington 2*, *Chef* or *The Detectorists* (a series): warm, low-stakes and easy "
              "to watch, and nothing bad happens in any of them."),
}
BOOK_MOODS = {
    "sad": ("*A Little Life* is the one people sob through, *Never Let Me Go* hurts quietly, and "
            "*The Kite Runner* if you want it to hit hard."),
    "scary": ("*The Haunting of Hill House* is creepy rather than gory, *Bird Box* is fast and "
              "tense, and *The Shining* if you want the classic."),
    "think": ("*Klara and the Sun* (what makes someone human), *The Remains of the Day* (a whole "
              "life looked back on) or *Sapiens* if you would rather have ideas than a story."),
    "uplifting": ("*The Midnight Library* (gentle and hopeful), *Lessons in Chemistry* (funny and "
                  "big-hearted) or *The Hundred-Year-Old Man Who Climbed Out of the Window and "
                  "Disappeared* (daft and warm)."),
    "gripping": ("*Gone Girl* (twisty from page one), *The Martian* (problem-solving and very "
                 "hard to put down) or any *Jack Reacher* book by Lee Child."),
    "short": ("*Of Mice and Men* is about 100 pages, *The Old Man and the Sea* is short and "
              "perfect, and *Small Things Like These* is under 120 pages."),
    "true": ("*Educated* by Tara Westover, *Into the Wild* by Jon Krakauer or *The Diary of a "
             "Young Girl* by Anne Frank: all real, all hard to stop reading."),
    "twist": ("*The Silent Patient* and *Gone Girl* both turn on a twist; *The Seven Husbands of "
              "Evelyn Hugo* if you want the reveal to make you cry as well."),
    "romance": ("*The Flatshare* (funny and warm), *Beach Read* (a bit sharper) or *Pride and "
                "Prejudice* if you want the classic."),
    "light": ("*The Thursday Murder Club* (funny and gentle), *The Midnight Library* or *The No. "
              "1 Ladies' Detective Agency*: easy to pick up and nothing grim."),
}
TV_MOODS = {
    "sad": ("*This Is Us* is built to make you cry weekly, *Normal People* hurts quietly, and "
            "*After Life* mixes the sad with real jokes."),
    "funny": ("*Schitt's Creek* starts daft and gets warmer, *Derry Girls* is sharp and short, "
              "and *The Detectorists* is gentle comedy."),
    "think": ("*Severance* (what work does to a person), *Chernobyl* (how a system fails) or "
              "*The Wire* if you want a whole city to think about."),
    "uplifting": ("*Ted Lasso* is kind and funny, *The Repair Shop* is people mending things "
                  "that matter to them, and *Call the Midwife* if you want warmth and a cry."),
    "gripping": ("*Happy Valley* is tense from the first scene, *The Night Of* does not let go, "
                 "and *Bodyguard* starts at a sprint and stays there."),
    "short": ("Episodes beat films when the evening is short: *The Bear* is 25 minutes an "
              "episode, *Derry Girls* is 22, and *Inside No. 9* is half an hour with a twist."),
    "true": ("*The Long Shadow*, *Des* or *Mr Bates vs The Post Office*: true stories told "
             "straight, all of them hard to stop watching."),
    "twist": ("*Line of Duty* for the reveal at the end of every series, *Severance* for the "
              "strangest one, and *Broadchurch* if you like a whole town hiding something."),
    "romance": ("*Normal People* for the intense one, *Starstruck* for the funny one, and "
                "*Bridgerton* if you want the frocks and the gossip."),
    "scary": ("*The Haunting of Hill House* for dread, *Midnight Mass* if you want one with "
              "ideas in it, and *Inside No. 9* for half-hour creepers."),
    "light": ("*The Detectorists* is the gentlest thing on telly, *Mortimer & Whitehouse: Gone "
              "Fishing* is two friends chatting, and *The Great British Bake Off* needs no "
              "attention at all."),
}
PODCAST_FUNNY = ("For funny: *No Such Thing as a Fish* (four people, one bizarre fact each, about "
                 "half an hour), *The Adam Buxton Podcast* for long chats that wander, or *Off "
                 "Menu* where guests order their dream meal. All easy to dip in and out of.")
PODCAST_CRIME = ("*Serial* series one is where to start: one murder, a year of reporting, and the "
                 "reason everyone else started making them. Then *Casefile* (calm, one case an "
                 "episode), *Criminal* (short, strange cases, less grim) or *The Teacher's Pet* "
                 "if you want one long story done properly.")
PODCAST_MOODS = {
    "funny": PODCAST_FUNNY,
    "think": ("*The Rest Is History* (history with jokes), *Hidden Brain* (why people do what "
              "they do) or *More or Less* if you like numbers checked."),
    "scary": ("*The Battersea Poltergeist* tells one haunting week by week, *Uncanny* collects "
              "real people's stories, and *Lore* does folk tales."),
    "true": ("*The Diary of a CEO* for long interviews, *Desert Island Discs* for real lives in "
             "an hour, or *This American Life* for one story told properly."),
    "gripping": ("*Serial* (the first series) started the genre, *The Teacher's Pet* is grim and "
                 "gripping, and *Sweet Bobby* has a twist you will not believe."),
    "light": ("*Desert Island Discs* is a gentle hour of somebody's life, *Nothing Much Happens* "
              "is made for falling asleep to, and *The Archers* if you want a story to drift "
              "with."),
    "sad": ("*Terrible, Thanks for Asking* is people telling hard things honestly, and *The "
            "Moth* is five-minute true stories, many of which land hard."),
}
MOOD_TABLES = {"film": FILM_MOODS, "book": BOOK_MOODS, "tv": TV_MOODS,
               "podcast": PODCAST_MOODS}
ANY_MOODS = {
    "sad": ("For a good cry: *Manchester by the Sea* on film, *Normal People* as a series, or "
            "*Never Let Me Go* if you would rather read."),
    "funny": ("For a laugh: *Groundhog Day* on film, *Schitt's Creek* on telly, or *The "
              "Thursday Murder Club* if you would rather read. Say which and I'll pick one."),
    "scary": ("Scary: *Get Out* on film, *The Haunting of Hill House* as a series or as the "
              "Shirley Jackson novel, and *Uncanny* if you want it in headphones. Which "
              "suits?"),
    "think": ("Something to think about: *Arrival* on film, *Severance* as a series, or *Klara "
              "and the Sun* to read. None of them tells you what to think."),
    "uplifting": ("Something hopeful: *Hunt for the Wilderpeople* on film, *Ted Lasso* as a "
                  "series, or *The Midnight Library* to read. All three leave you better than "
                  "they found you."),
    "gripping": ("Hard to stop: *Prisoners* on film, *Happy Valley* as a series, or *Gone Girl* "
                 "to read. Give any of them an evening you have nothing else planned for."),
    "short": ("Short and good: *Before Sunset* (80 minutes) on film, *The Bear* (25-minute "
              "episodes) as a series, or *Of Mice and Men* (about 100 pages) to read."),
    "true": ("True stories: *Zodiac* on film, *Mr Bates vs The Post Office* as a series, or "
             "*Educated* by Tara Westover to read."),
    "twist": ("With a twist: *The Prestige* on film, *Line of Duty* as a series, or *Gone Girl* "
              "to read. All three keep the reveal for the end."),
    "romance": ("Romantic: *Before Sunrise* on film, *Starstruck* as a series, or *The Flatshare* "
                "to read."),
    "light": ("Something easy: *Paddington 2* on film, *The Detectorists* on telly, or *The "
              "Thursday Murder Club* to read. None of them asks anything of you."),
}

MEDIUM_WORDS = (
    ("podcast", ("podcast", "podcasts", "listen", "listening")),
    ("book", ("book", "books", "novel", "novels", "read", "reading", "audiobook",
              "audiobooks")),
    ("tv", ("tv", "telly", "series", "show", "shows", "boxset", "box set", "binge",
            "episode", "episodes", "netflix", "iplayer")),
    ("film", ("film", "films", "movie", "movies", "cinema", "watch", "watching")),
    ("music", ("music", "song", "songs", "album", "albums", "playlist")),
)

MOOD_GLUE = frozenset("""a an the it its i me my im i'm you your he she him her they them we
us our want wants wanted would like likes to of for and or but so really very much too not no
never nothing none dont doesnt didnt hardly barely some something that this these those there
here is are was were am be been being do does did have has had will can could should may might
get gets got able one ones make makes made in on at up down out off over with by from as if
than then when while all night""".split())
def _mood_key_words(moods, drop=()):
    shut = {word for phrase in drop for word in str(phrase).split()}
    found = []
    for mood in MOOD_ORDER:
        if mood not in moods:
            continue
        for phrase in moods[mood]:
            for word in str(phrase).split():
                if word in MOOD_GLUE or word in found or word in shut:
                    continue
                found.append(word)
    return tuple(found)


MOOD_WORDS = _mood_key_words(MOODS)


MOOD_BY_WORD = {}
MOOD_SIGNAL_SET = set()


def _mood_signals(words):
    return tuple(word for word in words
                 if _mood_of(word) or _mood_of("not too " + word) or _mood_of("nothing " + word))


def _negated(tokens, start, phrase):
    if not start or phrase[0] in NEGATORS:
        return False
    if tokens[start - 1] in NEGATORS:
        return True
    if start > 1 and tokens[start - 2] in NEGATORS and tokens[start - 1] in SOFT:
        return True
    for back in (1, 2, 3, 4):
        if start > back and tokens[start - back] in WANTING and tokens[start - back - 1] in NEGATORS:
            return True
    return False


_WET_WORDS = ("rain", "rainy", "raining", "rains", "showers", "drizzle", "drizzling",
              "pouring", "downpour", "storm", "storms", "sleeting", "sleet", "snowing")
_WET_PHRASES = ("wet day", "wet days", "wet weekend", "wet weekends", "wet afternoon",
                "wet weather", "wet out", "wet one")
_EVENING_WORDS = ("night in", "tonight", "evening", "at home",
                  "indoors", "cosy", "cozy", "this afternoon in", "day in",
                  "we are staying in", "were staying in", "im staying in",
                  "i am staying in", "staying in tonight", "stay in tonight",
                  "staying in this evening", "stay in this evening", "staying in all")


def _typed_line(understood):
    if not isinstance(understood, dict):
        return " "
    said = understood.get("text") or understood.get("clean") or ""
    return " %s " % _plain_words(said)


def _names_the_weather(understood):
    line = _typed_line(understood)
    return (any((" %s " % word) in line for word in _WET_WORDS)
            or any(phrase in line for phrase in _WET_PHRASES))


def _names_the_evening(understood):
    line = _typed_line(understood)
    return any((" %s " % word) in line for word in _EVENING_WORDS)


def _plain_words(line):
    plain = str(line or "").lower().replace("\u2019", "'").replace("-", " ")
    plain = re.sub(r"n'\s*t\b", "nt", plain)
    plain = plain.replace("'", "")
    words = []
    for word in re.findall(r"[a-z0-9]+", plain):
        words.extend(CONTRACTIONS.get(word, word).split())
    return " ".join(words)


def _mood_of(line):
    plain = _plain_words(line)
    tokens = plain.split()
    if not tokens:
        return None
    refused = None
    for mood in MOOD_ORDER:
        for phrase in MOODS[mood]:
            words = re.findall(r"[a-z0-9]+", re.sub(r"[-']", " ", phrase))
            if not words:
                continue
            for start in range(len(tokens) - len(words) + 1):
                if tokens[start:start + len(words)] != words:
                    continue
                if _negated(tokens, start, words):
                    refused = refused or mood
                    continue
                return (mood, False)
    for at, token in enumerate(tokens):
        if token not in MOOD_SIGNAL_SET:
            continue
        mood = MOOD_BY_WORD.get(token)
        if _negated(tokens, at, [token]):
            refused = refused or mood or token
            continue
        if mood is not None:
            return (mood, False)
    if refused:
        return ("light", True)
    return None


MOOD_SIGNALS = _mood_signals(MOOD_WORDS)
MOOD_SIGNAL_SET.update(MOOD_SIGNALS)
for _mood in MOOD_ORDER:
    for _word in MOODS[_mood]:
        if (isinstance(_word, str) and " " not in _word and _word not in MOOD_BY_WORD
                and _mood_of(_word) == (_mood, False)):
            MOOD_BY_WORD[_word] = _mood


def _no_named_mood(understood):
    said = " ".join(str(word) for word in (understood.get("words") or ()))
    return _mood_of(said) is None


FILM_MINUTES = {
    "Manchester by the Sea": 137, "Atonement": 123, "Up": 96,
    "What We Do in the Shadows": 86, "The Nice Guys": 116, "Paddington 2": 103,
    "Arrival": 116, "12 Angry Men": 96, "Ex Machina": 108,
    "Hunt for the Wilderpeople": 101, "The Shawshank Redemption": 142, "Sing Street": 106,
    "Prisoners": 153, "Gone Girl": 149, "Sicario": 121,
    "Before Sunset": 80, "Locke": 85, "Toy Story": 81,
    "Zodiac": 157, "Catch Me If You Can": 141, "127 Hours": 94,
    "The Sixth Sense": 107, "The Prestige": 130,
    "Before Sunrise": 101, "When Harry Met Sally": 96, "Pride & Prejudice": 129,
    "Chef": 114, "Groundhog Day": 101, "The Grand Budapest Hotel": 99,
    "Get Out": 104, "A Quiet Place": 90, "Hereditary": 127, "The Others": 104,
    "The Mitchells vs the Machines": 114, "Matilda": 102, "Zootropolis": 108,
}


def _films_within(text, line):
    if not text or not isinstance(line, str):
        return text
    limit, strict = _limit_wanted(line)
    if not limit:
        return text
    named = []
    for title in re.findall(r"\*([^*]{2,60})\*", text):
        if title not in named:
            named.append(title)
    if not named or any(title not in FILM_MINUTES for title in named):
        return text
    fit = [title for title in named
           if (FILM_MINUTES[title] < limit if strict else FILM_MINUTES[title] <= limit)]
    if len(fit) == len(named):
        return text
    over = len(named) - len(fit)
    lead = text.split(":")[0].strip()
    has_lead = ":" in text and 0 < len(lead) <= 40 and "*" not in lead
    short = min(named, key=lambda title: FILM_MINUTES[title])
    if not fit:
        if has_lead:
            return ("%s, nothing there comes in %s %d minutes - the shortest is *%s* at %d. Say "
                    "another mood and I will look again."
                    % (lead, "under" if strict else "at", limit, short, FILM_MINUTES[short]))
        return ("Nothing in that list comes in %s %d minutes - the shortest is *%s* at %d. Say "
                "another mood and I will look again."
                % ("under" if strict else "at", limit, short, FILM_MINUTES[short]))
    said_fit = ["*%s* (%d minutes)" % (title, FILM_MINUTES[title]) for title in fit]
    body = said_fit[0] if len(said_fit) == 1 else ", ".join(said_fit[:-1]) + " or " + said_fit[-1]
    if has_lead:
        return ("%s, %s %d minutes: %s. The other %s run%s longer, so say if you would rather "
                "have one of those." % (lead, "under" if strict else "up to", limit, body,
                                        "one" if over == 1 else "two",
                                        "s" if over == 1 else ""))
    return ("Films that fit %s %d minutes: %s. The rest of that list run%s longer, so say if you "
            "would rather have one of those."
            % ("under" if strict else "up to", limit, body, "s" if over == 1 else ""))


def _mood_pick(picks):
    def pick(memory, understood):
        line = ((understood.get("clean") or "") + " " + (understood.get("norm_text") or ""))
        got = _mood_of(line)
        if not got:
            return None
        mood = "light" if got[1] else got[0]
        return _films_within(picks.get(mood), line) if mood else None
    return pick


def _medium_named(text):
    said = " %s " % _plain_words(text)
    best, where = None, len(said) + 1
    for medium, words in MEDIUM_WORDS:
        for word in words:
            at = said.find(" %s " % word)
            if at >= 0 and at < where:
                best, where = medium, at
    return best


def _the_medium(understood, memory):
    understood = understood if isinstance(understood, dict) else {}
    order = ["%s %s" % (understood.get("clean") or "", understood.get("norm_text") or "")]
    lean = understood.get("leans_on") if isinstance(understood.get("leans_on"), dict) else {}
    if lean.get("text"):
        order.append(str(lean.get("text") or ""))
    turns = memory.get("turns") if isinstance(memory, dict) else None
    if isinstance(turns, list) and turns and isinstance(turns[-1], dict):
        order.append(str(turns[-1].get("user") or ""))
        order.append(str(turns[-1].get("bot") or ""))
    for text in order:
        medium = _medium_named(text)
        if medium:
            return medium
    for text in order:
        medium = _title_medium(text)
        if medium:
            return medium
    last = memory.get("last_answer") if isinstance(memory, dict) else None
    last = last if isinstance(last, dict) else {}
    named = str(last.get("id") or "").split("-")[0]
    for medium, words in MEDIUM_WORDS:
        if named and named in [word.split()[0] for word in words]:
            return medium
    return None


def _picks_by_title():
    found = {}
    for medium, table in MOOD_TABLES.items():
        for moods in table.values():
            for title in re.findall(r"\*([^*]{2,60})\*", moods):
                if len(title) >= 6:
                    found.setdefault(_plain_words(title), medium)
    return found


PICK_TITLES = _picks_by_title()


def _title_medium(text):
    said = " %s " % _plain_words(text)
    best, where = None, len(said) + 1
    for title, medium in PICK_TITLES.items():
        at = said.find(" %s " % title)
        if at >= 0 and at < where:
            best, where = medium, at
    return best


def _chat_is_about_a_pick(understood, memory):
    understood = understood if isinstance(understood, dict) else {}
    last = memory.get("last_answer") if isinstance(memory, dict) else None
    last = last if isinstance(last, dict) else {}
    domain = str(last.get("domain") or "")
    topic = str(understood.get("topic") or "")
    if not topic:
        lean = understood.get("leans_on") if isinstance(understood.get("leans_on"), dict) else {}
        topic = str(lean.get("topic") or "")
    if domain == "entertainment" or topic == "entertainment":
        return True
    return not domain and topic in ("", "feelings")


TURNS_IT_DOWN = ("no", "not", "nothing", "dont", "don't", "rather not", "no thanks", "too much",
                 "isnt", "isn't", "wasnt", "wasn't", "cant stand", "can't stand", "hate",
                 "sick of", "bored of", "no more", "anything but", "not really")
TURNED_DOWN_KEEPS_ITS_OWN = NOT_A_MOOD_PICK + (
    "not too long", "nothing too long", "not long", "not too big", "not too expensive",
    "not too many", "not too much", "nothing too much",
)


def _a_pick_of_the_other_mood(memory, understood):
    understood = understood if isinstance(understood, dict) else {}
    line = "%s %s" % (understood.get("clean") or "", understood.get("norm_text") or "")
    got = _mood_of(line)
    if not got or not got[1]:
        return None
    return _a_pick_in_any_medium(memory, understood)


A_LENGTH_MOOD = ("short",)


def _a_pick_in_any_medium(memory, understood):
    understood = understood if isinstance(understood, dict) else {}
    line = "%s %s" % (understood.get("clean") or "", understood.get("norm_text") or "")
    got = _mood_of(line)
    if not got or not _chat_is_about_a_pick(understood, memory):
        return None
    if got[0] in A_LENGTH_MOOD and not (_pick_kind(line) or _pick_carry(memory, line)):
        return None
    own = _mood_of(" ".join(_own_texts(understood)))
    if own and own[1]:
        mood = "light"
    elif own:
        mood = own[0]
    else:
        mood = _the_mood_the_chat_holds(memory)
        if not mood:
            if not _the_mood_the_chat_turned_down(memory):
                return None
            mood = "light"
    if _limit_wanted(line)[0] and not _pick_kind(line) and not _pick_carry(memory, line):
        picks = MOOD_TABLES.get("film") or {}
    else:
        picks = MOOD_TABLES.get(_the_medium(understood, memory)) or {}
    said = picks.get(mood) or ANY_MOODS.get(mood)
    last = memory.get("last_answer") if isinstance(memory, dict) else None
    last = last if isinstance(last, dict) else {}
    said = _films_within(said, line)
    if said and _plain_words(said) == _plain_words(str(last.get("reply") or "")):
        first = re.search(r"\*([^*]{2,60})\*", said)
        if first:
            return "Of those, I'd start with *%s*." % first.group(1)
        return None
    return said


NOT_WATCHING = ("watch for", "watching for", "watch out", "look out for", "keep an eye out",
                "signs of", "symptoms", "what to look")

VIEWING = ("film", "films", "movie", "movies", "tv", "telly", "tele", "show", "shows", "series",
           "episode", "episodes", "netflix", "dvd", "cinema", "documentary", "programme",
           "programmes", "box set", "boxset", "sitcom", "cartoon", "cartoons")

ASKING_TO_WATCH_FOR = ("what should i watch for", "what do i watch for", "what to watch for",
                       "what should i watch out", "what do i watch out", "watch out for",
                       "look out for", "sign", "symptom", "keep an eye",
                       "what to look for", "what should i look for", "what should i be looking")


def not_asking_what_to_watch_for(understood):
    if not isinstance(understood, dict):
        return True
    said = str(understood.get("text") or understood.get("clean") or understood.get("norm_text")
               or " ".join(understood.get("words") or ())).lower()
    if not said:
        return True
    if any(word in said for word in VIEWING):
        return True
    return not any(asked in said for asked in ASKING_TO_WATCH_FOR)


HAIKU = {
    "rain": ("Rain on the window,",
             "a hundred small taps, all night,",
             "and the garden drinks."),
    "sea": ("The sea keeps its own",
            "slow time, and the tide turns twice",
            "before anyone looks."),
    "ocean": ("The sea keeps its own",
              "slow time, and the tide turns twice",
              "before anyone looks."),
    "cat": ("Cat on the warm sill,",
            "one eye on the garden birds,",
            "both ears fast asleep."),
    "kitten": ("Cat on the warm sill,",
               "one eye on the garden birds,",
               "both ears fast asleep."),
    "dog": ("Wet nose at the door,",
            "the whole day arrives at once,",
            "tail first, always first."),
    "puppy": ("Wet nose at the door,",
              "the whole day arrives at once,",
              "tail first, always first."),
    "autumn": ("Autumn in the park,",
               "the trees hand back what they took,",
               "and the air smells cold."),
    "winter": ("Winter on the glass,",
               "the kettle keeps its own time,",
               "and the cat agrees."),
    "snow": ("First snow on the street,",
             "the world turned down to a hush,",
             "footprints, and then none."),
    "spring": ("Spring in the hedges,",
               "green shoots pushing through the dark,",
               "nothing asks to stay."),
    "summer": ("Summer on the lane,",
               "the long evening will not end,",
               "and nobody minds."),
    "night": ("Moon over the roof,",
              "the house settles into dark,",
              "one light left upstairs."),
    "moon": ("Moon over the roof,",
             "the house settles into dark,",
             "one light left upstairs."),
    "sun": ("The sun on my back,",
            "and a chair that is too warm",
            "to do anything."),
    "morning": ("Morning in the house,",
                "the kettle takes its time now,",
                "a sock on the stairs."),
    "tea": ("Steam from the mug climbs,",
            "the morning waits in the pot,",
            "nothing is urgent."),
    "coffee": ("First cup of the day,",
               "the desk, the list, the phone calls,",
               "all of it can wait."),
    "garden": ("Garden after rain,",
               "the snail crosses the whole path,",
               "taking its own time."),
    "city": ("The city at six,",
             "every window lights up late,",
             "one streetlamp still out."),
    "friend": ("Good friend on the phone,",
               "an hour goes like ten minutes,",
               "and nothing was fixed."),
    "mum": ("Mum in the kitchen,",
            "sings the wrong words on purpose,",
            "and I sing them too."),
    "mother": ("Mum in the kitchen,",
               "sings the wrong words on purpose,",
               "and I sing them too."),
    "work": ("The desk light is on,",
             "the list grows shorter, then long,",
             "and five o'clock comes."),
    "job": ("The desk light is on,",
            "the list grows shorter, then long,",
            "and five o'clock comes."),
    "running": ("Legs heavy, lungs loud,",
                "the last mile always uphill,",
                "and the door, and home."),
    "gym": ("Legs heavy, lungs loud,",
            "the last mile always uphill,",
            "and the door, and home."),
    "school": ("School bag by the door,",
               "a hundred small things to learn,",
               "and one of them stays."),
    "baby": ("Small hands on my face,",
             "the whole night in one held breath,",
             "then a milky sleep."),
    "love": ("Love is a kettle",
             "put on without being asked,",
             "and the chair pulled out."),
    "birthday": ("One more candle lit,",
                 "the cake leans under the wish,",
                 "and everyone sings."),
}
HAIKU["kids"] = HAIKU["baby"]
HAIKU["bed"] = HAIKU["night"]
HAIKU["river"] = HAIKU["sea"]

POEMS = {
    "sea": ("The sea is loud and never still,",
            "it takes the sand against its will.",
            "It keeps it for a day or three,",
            "then hands it back to you and me."),
    "rain": ("The rain comes down on everything,",
             "on roof, on road, on outstretched wing.",
             "It does not ask who wants it here,",
             "it just arrives, and then it's clear."),
    "autumn": ("The leaves let go without a sound",
               "and lie in gold across the ground.",
               "The trees stand bare and do not mind:",
               "there is another spring behind."),
    "night": ("The night comes in and closes shop,",
              "the street goes quiet, the traffic stops.",
              "One window keeps its light on late",
              "for someone who is coming in the gate."),
    "cat": ("The cat has found the warmest chair",
            "and settled in it, without care.",
            "The chair was yours an hour ago.",
            "The cat does not believe it so."),
    "mum": ("My mum has heard it all before",
            "and still she stands inside the door.",
            "She says the small things can all wait,",
            "and then she makes the small things fit -",
            "and that is why I ring her late,",
            "and why she never mentions it."),
    "friend": ("A friend is someone at the door",
               "who does not need to say what for.",
               "You put the kettle on for two",
               "and half the weight comes off of you."),
    "garden": ("The garden does not need a plan,",
               "it fills the space up while it can.",
               "A weed is just a plant that knows",
               "the better spot, and simply grows."),
    "winter": ("The winter takes the light away",
               "and gives it back a bit each day.",
               "The cold is honest, and the frost",
               "draws on the glass and counts no cost."),
    "work": ("The work comes in and fills the day,",
             "and takes the evening half away.",
             "I do the bit that's in my hand",
             "and leave the rest where it can stand."),
    "birthday": ("Another year, and here you are,",
                 "with all the miles and all the scars.",
                 "The cake is small, the wish is too:",
                 "more of the good ones, sent to you."),
    "dad": ("My dad will fix it if he can,",
            "and if he can't, he'll have a plan.",
            "He says the worst is never true,",
            "and mostly, it turns out he knew."),
}

LIMERICKS = {
    "cat": ("There once was a cat on a chair,",
            "who hadn't a worry or care.",
            "When the postman came by,",
            "it opened one eye,",
            "and gave him a very long stare."),
    "kitten": ("There once was a cat on a chair,",
               "who hadn't a worry or care.",
               "When the postman came by,",
               "it opened one eye,",
               "and gave him a very long stare."),
    "dog": ("There once was a dog called Ned,",
            "who slept at the end of the bed.",
            "He dreamt of a cat,",
            "of a bone, and of that",
            "half a sausage he thought he'd been fed."),
    "puppy": ("There once was a dog called Ned,",
              "who slept at the end of the bed.",
              "He dreamt of a cat,",
              "of a bone, and of that",
              "half a sausage he thought he'd been fed."),
    "rain": ("There once was a cloud over Crewe",
             "that had far too much rain to do.",
             "It rained on the park",
             "from morning till dark,",
             "and then, just for fun, rained on you."),
    "tea": ("There once was a builder called Len",
            "who brewed up a pot now and then.",
            "When the tea was stewed",
            "it improved his mood,",
            "and he put the kettle on then."),
    "work": ("There once was a report I should write",
             "whose deadline was Tuesday at night.",
             "I opened the file,",
             "stared at it a while,",
             "and closed it again out of spite."),
    "baby": ("There once was a baby called Rose,",
             "who slept like a dream, I suppose.",
             "Till somebody said",
             "'she's asleep!' and instead",
             "she woke up, as everyone knows."),
}
LIMERICKS["job"] = LIMERICKS["work"]
LIMERICKS["mum"] = LIMERICKS["baby"]

GENERIC_LIMERICK = ("There once was a {thing} I knew,",
                    "whose stories were never quite true.",
                    "They wandered the day,",
                    "and took their own way,",
                    "and honestly, what can you do?")

GENERIC_POEM_TWO = ("The {thing} is here and the {thing} is plain,",
                    "it comes round slowly and it comes round again.",
                    "I have no better answer to give it than this,",
                    "so I put it in a line and I let it exist.")
GENERIC_POEM = ("I keep a little {thing} in mind,",
                "the sort of {thing} that's hard to find.",
                "It does not shout, it does not boast,",
                "and that's the {thing} I like the most.")

PEOPLE = ("wife", "husband", "partner", "girlfriend", "boyfriend", "fiance", "fiancee",
          "love", "son", "daughter", "child", "kid", "baby", "sister", "brother",
          "grandma", "grandmother", "nan", "gran", "grandad", "grandfather", "friend",
          "best friend", "mate", "mother", "mum", "mom", "father", "dad")
WARM_POEM = ("You are the one I tell things to,",
             "the dull ones and the hard ones too;",
             "the day can take whatever's spare,",
             "and still I'm glad you're there.")

CARD_OCCASIONS = ("birthday", "christmas", "xmas", "new baby", "wedding", "engagement",
                  "christening", "baptism", "naming ceremony", "communion", "anniversary",
                  "valentines", "valentine's", "mothers day", "mother's day", "fathers day",
                  "father's day", "new home", "housewarming", "graduation", "new job",
                  "promotion", "get well", "get better", "good luck", "retirement",
                  "leaving", "condolence", "sympathy", "thank you", "thankyou")
CARD = (tuple(one + " card" for one in CARD_OCCASIONS) +
        ("in a card", "in my card", "in the card", "in this card", "on a card", "on my card",
         "on the card", "inside the card", "card message", "card wording", "card line",
         "card lines"))

ABSTRACT = ("lockdown", "pandemic", "covid", "coronavirus", "virus", "grief", "loss", "love",
            "hope", "fear", "anxiety", "depression", "stress", "time", "memory", "memories",
            "childhood", "future", "past", "war", "peace", "freedom", "illness", "cancer",
            "dementia", "addiction", "recovery", "friendship", "marriage", "divorce", "work",
            "school", "unemployment", "poverty", "climate", "world", "life", "age", "ageing",
            "motherhood", "fatherhood", "loneliness", "happiness", "sadness", "anger", "regret",
            "guilt", "change", "growing", "job", "money", "death")

STORY_OPENINGS = (
    "It started with {a_thing} nobody in the house had planned for.\n"
    "The Tuesday came and went, and it was still there on the Wednesday.\n"
    "By Friday the whole street had an opinion, and no two of them matched.\n"
    "In the end they kept it, and it kept them.",
    "{The_thing} arrived in a box with no sender and no note.\n"
    "It sat in the hall for a week, and then it started to hum.\n"
    "She unscrewed one corner, looked inside, and sat down on the floor.\n"
    "\"Well,\" she said to nobody at all, \"that changes the week.\"",
    "He had carried {the_thing} from one flat to another for eleven years.\n"
    "The morning he finally opened it, the kettle boiled and the phone rang at the same time.\n"
    "He let the kettle win, and the phone stopped.\n"
    "Then he sat at the table with {the_thing} and read the whole thing twice.",
)

POSSESSIVE = ("my ", "your ", "our ", "his ", "her ", "their ", "its ", "mum's ", "dad's ",
              "nan's ", "gran's ", "mum’s ", "dad’s ")

NO_THING_IN_A_VERSE = {"rap": "beat", "song": "tune"}


def _the_possessive_phrase(thing, said):
    if not said or not thing:
        return ""
    for word in POSSESSIVE:
        start = 0
        while True:
            at = said.find(word, start)
            if at < 0:
                break
            rest = said[at + len(word):]
            spot = rest.find(thing)
            if spot >= 0 and len(rest[:spot].split()) <= 2:
                end = at + len(word) + spot + len(thing)
                return " ".join(said[at:end].split())
            start = at + 1
    return ""


def _article_for(thing, article="the", clean=""):
    said = (clean or "").lower()
    theirs = _the_possessive_phrase(thing, said)
    if theirs:
        return {"a_thing": theirs, "the_thing": theirs,
                "The_thing": theirs[:1].upper() + theirs[1:]}
    their = article + " "
    return {"a_thing": "a " + thing, "the_thing": their + thing,
            "The_thing": (their + thing)[:1].upper() + (their + thing)[1:]}

STORY_LONGER = (
    "The weeks went by and it stopped being strange.\n"
    "Things settled into a shape nobody had chosen, and the shape held.\n"
    "Then one quiet morning there was nothing to decide,\n"
    "and they found they missed the deciding more than they had expected.",
    "There was a phone call in the spring that changed the plan.\n"
    "Nothing was thrown out, though a few things were put away.\n"
    "By summer the {thing} had a place of its own in the house,\n"
    "and nobody could remember what had stood there before it.",
    "It came up again at dinner, the way these things do.\n"
    "Somebody said it out loud and everybody laughed, and then carried on eating,\n"
    "which is how a thing stops being news.\n"
    "After that the {thing} was simply part of the room.",
    "Years later somebody asked where it had come from\n"
    "and got four different answers, all of them true.\n"
    "They settled on the shortest one, because it was the one\n"
    "that left the {thing} where it was.",
)
VERSE_LONGER = (
    "The {thing} is not what the morning planned,\n"
    "it sits in the light and it will not be banned.\n"
    "It is stubborn and it is small and it is here to stay,\n"
    "and I have stopped arguing with it anyway.",
    "There is more to the {thing} than the shape it shows,\n"
    "more than the part that anybody knows.\n"
    "So leave a little room and leave a little light,\n"
    "and the {thing} will get through the rest of the night.",
    "I said what I said and I meant every word,\n"
    "the {thing} is not finished, or so I have heard.\n"
    "So here is one more, and I will keep it plain,\n"
    "for the {thing} and the weather it cannot explain.",
    "The {thing} does not hurry and does not explain,\n"
    "it takes the long way round and it comes back again.\n"
    "So let the day go where it wants to go,\n"
    "the {thing} knows the way and it is not slow.",
)

OCCASION = ("wedding", "weddings", "best man", "maid of honour", "toast", "speech", "vows",
            "eulogy", "anniversary", "retirement")

PICK_WORDS = ("recommend", "recommends", "recommendation", "recommendations", "suggest", "suggests",
              "suggestion", "playlist", "best", "good song", "good songs", "ideas", "any ideas",
              "what should i listen", "album", "albums", "artist", "artists")

STORY_LEADING = {"story": "A short story about {subject}:",
                 "rap": "A rap about {subject}:",
                 "song": "A song about {subject}:"}
NO_SUBJECT_LEADING = {"rap": "A rap, then:", "song": "A song, then:",
                      "story": "Here is one, made up on the spot:"}
GENERIC_RAP = ("Yo, {the_thing} is back and it is here to stay,",
               "I have been up since six and I am out all day.",
               "They said it was nothing, I said it was mine,",
               "so {the_thing} and me, we are doing just fine.")
GENERIC_SONG = ("Verse:\nIt was a Tuesday, nothing much to say,\n"
                "I thought about {the_thing} and I walked away.\n"
                "Chorus:\nOh, {the_thing}, {the_thing},\nit comes back around,\n"
                "{the_thing} comes back around.")
GENERIC_STORY_THING = "small thing"

NICK_FIRST = ("Captain", "Big", "Tiny", "Old", "Sir", "Lady", "Doctor", "Saint")
NICK_LAST = ("Chaos", "Thunder", "Biscuit", "Trouble", "Sunshine", "Nonsense", "Legend",
             "Saturday", "Pockets", "Rocket")

RHYMES_BY_ENDING = {
    "ight": ("light", "night", "bright", "kite", "fright", "tight", "quite"),
    "ay": ("day", "way", "play", "away", "grey", "stay", "today"),
    "ee": ("tree", "see", "me", "free", "three", "agree"),
    "oo": ("blue", "true", "you", "shoe", "through", "new"),
    "ing": ("king", "sing", "ring", "spring", "wing", "thing"),
    "ain": ("rain", "train", "again", "plain", "chain", "brain"),
    "ame": ("name", "game", "same", "flame", "came"),
    "old": ("gold", "cold", "told", "bold", "hold"),
    "ine": ("line", "mine", "shine", "fine", "wine", "nine"),
    "ime": ("time", "climb", "lime", "dime", "rhyme"),
    "ake": ("cake", "lake", "make", "take", "wake", "break"),
    "eat": ("seat", "heat", "street", "meet", "treat", "wheat"),
    "one": ("bone", "stone", "phone", "alone", "own", "thrown"),
    "ate": ("late", "gate", "wait", "plate", "eight", "straight"),
    "ill": ("still", "hill", "will", "fill", "until"),
    "and": ("hand", "sand", "stand", "land", "band"),
    "art": ("heart", "start", "part", "smart", "apart"),
    "eet": ("feet", "street", "sweet", "meet", "sheet"),
    "ide": ("side", "wide", "hide", "ride", "guide"),
    "ound": ("sound", "round", "ground", "found", "around"),
    "own": ("town", "down", "clown", "crown", "brown"),
    "ue": ("blue", "true", "glue", "clue", "view"),
    "at": ("cat", "hat", "mat", "flat", "that", "bat"),
    "og": ("dog", "log", "fog", "jog", "bog"),
    "un": ("sun", "fun", "run", "bun", "one"),
    "ouse": ("house", "mouse", "blouse", "spouse"),
    "ock": ("clock", "sock", "rock", "block", "stock"),
    "air": ("chair", "hair", "fair", "care", "there"),
    "ell": ("bell", "well", "tell", "shell", "fell"),
    "ent": ("tent", "went", "sent", "bent", "spent"),
    "ore": ("door", "shore", "more", "floor", "before"),
    "end": ("friend", "end", "send", "bend", "spend"),
    "ove": ("love", "glove", "above", "dove", "shove"),
    "ome": ("home", "come", "some", "roam", "foam"),
    "oney": ("honey", "money", "sunny", "funny"),
    "eep": ("sleep", "deep", "keep", "sheep", "cheap"),
    "ife": ("life", "wife", "knife", "strife"),
    "ow": ("now", "how", "cow", "allow", "vow"),
    "oon": ("moon", "soon", "spoon", "June", "tune"),
    "all": ("small", "tall", "ball", "fall", "hall"),
    "ess": ("less", "dress", "mess", "press", "guess"),
    "ip": ("ship", "trip", "slip", "chip", "grip"),
    "op": ("shop", "stop", "top", "drop", "chop"),
    "ug": ("hug", "mug", "rug", "bug", "plug"),
    "an": ("man", "plan", "van", "ran", "tan"),
    "ear": ("year", "hear", "near", "clear", "fear"),
}
NO_RHYME = {
    "orange": ("Nothing rhymes exactly with *orange*. The near ones are *sporange* (a spore case "
               "on a fern), *Blorenge* (a hill in Wales) and the two-word *door hinge*. If you "
               "need it for a poem, put *orange* at the end of a line that does not have to "
               "rhyme, and rhyme the line before it with something else."),
    "purple": ("Nothing rhymes exactly with *purple*. *Curple* (a horse's strap) is the "
               "one word that nearly does, and *hirple* (to limp) is a Scottish near miss. In a "
               "poem, end the line on *purple* and rhyme the other line of the pair instead."),
    "silver": ("Nothing rhymes exactly with *silver*. *Chilver* (a ewe lamb) is the near miss, "
               "and most poets rhyme it with *river* or *deliver* and let the vowel do the work."),
    "month": ("Nothing rhymes exactly with *month*. *Oneth* is not a word, and the usual fix is "
              "to end the line on *month* and rhyme the other line of the pair."),
}

STORY_IDEAS = (
    "A person finds a door in their own house that they have never opened, and the key is in "
    "their coat pocket.",
    "Two neighbours share a wall and a secret, and only one of them knows it is shared.",
    "A letter arrives forty years late, and the person it was meant for is still at the same "
    "address.",
    "Someone who has never left their village has to cross a city in one night.",
    "A family inherits a shop that comes with one customer who will not go away.",
    "A rescue dog remembers the person who lost it, and finds them in a supermarket queue.",
    "The last person on a night shift starts getting phone calls from the empty office upstairs.",
    "A cook loses their sense of taste the week they are cooking for the person they want to "
    "impress.",
    "A child's imaginary friend turns up at the school gate, and only the child can see them.",
    "A retired teacher keeps the exercise books of one pupil, and finally works out why.",
    "A train stops at a station that is not on the map, and one passenger gets off.",
    "Two strangers are given the same locker key at a swimming pool.",
    "A man who fixes everything in the street cannot fix the one thing in his own house.",
    "A woman starts receiving post addressed to her in her own handwriting, dated next year.",
    "A wedding photographer finds someone in the background of every photo who was never "
    "invited.",
    "A town agrees to forget one thing together, and one person refuses.",
)

QUIZ_NAMES = ("Quizteam Aguilera", "Les Quizerables", "Norfolk 'n' Chance", "The Quizzly Bears",
              "Sultans of Quiz", "Trivia Newton-John", "University of Trivia", "Agatha Quiztie",
              "Let's Get Quizzical", "The Also Rans")

TEAM_NAMES = ("The Long Shots", "Second Wind", "The Underdogs", "The Night Owls",
              "The Wild Cards", "The Try Hards", "The Comeback Club", "The Early Birds")

GRAVE = ("funeral", "death", "dead", "died", "dying", "cancer", "war", "killed", "ill",
         "sick", "hospital", "grief", "bereaved", "suicide", "miss him", "miss her")

CONNECTORS = {"and", "with", "his", "hers", "their", "our", "who", "in", "at", "for", "to", "a",
              "an", "the"}

SUBJECT_STOP = {"a", "an", "the", "my", "our", "your", "his", "her", "their", "some", "this",
                "that", "of", "about", "on", "called", "named", "please", "thanks", "now",
                "today", "tonight", "too", "really"}
SUBJECT_TAIL = {"please", "thanks", "now", "today", "tonight", "too", "really", "and", "for",
                "about", "card", "me",
                "from", "in", "at", "near", "by", "across", "over", "under", "behind",
                "with"}
SUBJECT_END = {"should", "can", "could", "would", "will", "i", "you", "we", "he", "she", "they",
               "do", "does", "did", "is", "are", "was", "were", "get", "buy", "want", "need",
               "have", "has", "to", "that", "which", "what", "how", "when", "if", "says"}

EMPTY_SUBJECT = {"my", "our", "your", "his", "her", "their", "the", "a", "an", "this", "that",
                 "these", "those", "it", "its", "me", "us", "them", "him", "one", "some"}

ING_NOUNS = {"anything", "beginning", "being", "blessing", "booking", "building", "ceiling",
             "clothing", "darling", "dressing", "earring", "ending", "evening", "feeling",
             "filling", "finding", "gathering", "going", "grandchild", "heading", "hearing",
             "king", "landing", "lightning", "meeting", "morning", "nothing", "offering",
             "opening", "outing", "painting", "pudding", "queen", "ring", "saying",
             "setting", "sibling", "spring", "staffing", "stocking", "string", "stuffing",
             "sung", "thing", "topping", "training", "warning", "wedding", "whatever",
             "wing", "writing", "young"}


def _subject_words(text):
    words = re.findall(r"[a-z']+", text)
    for place, word in enumerate(words):
        if word in SUBJECT_END:
            words = words[:place]
            break
    for place, word in enumerate(words):
        if place and word in CONNECTORS:
            words = words[:place]
            break
    words = words[:3]
    while words and (words[-1] in SUBJECT_TAIL or words[-1] in CONNECTORS):
        words.pop()
    if (len(words) > 1 and words[-1].endswith("ing") and len(words[-1]) > 4
            and words[-1] not in ING_NOUNS):
        if any(word not in SUBJECT_STOP and word not in EMPTY_SUBJECT for word in words[:-1]):
            words.pop()
    return words


NO_SUBJECT_VERSE = {
    "haiku": ("Cold tap in the yard,",
              "the kettle ticks itself warm,",
              "morning starts again."),
    "limerick": ("There once was a fellow called Stan,",
                 "who swapped his old bike for a van.",
                 "It rattles, it groans,",
                 "on cobbles and stones,",
                 "and it still beats the bus, said his gran."),
    "poem": ("Some days are quiet, some are loud,",
             "and some you spend inside a cloud.",
             "The kettle helps, the window too,",
             "and so, quite honestly, do you."),
}


def _no_subject_verse(form, noun=None):
    lines = NO_SUBJECT_VERSE.get(form)
    if not lines:
        return None
    lead = {"haiku": "A haiku, then:", "limerick": "A limerick, then:"}.get(form,
                                                                          "A short poem, then:")
    if noun == "rhyme":
        lead = "A rhyme, then:"
    return _lines(lines, lead)


VERSE_FORM_WORDS = {
    "haiku": ("haiku", "haikus"),
    "limerick": ("limerick", "limericks"),
    "poem": ("poem", "poems", "poetry", "verse", "rhyme", "rhymes", "rhyming", "song", "rap",
             "ode", "odes"),
}
_OTHER_FORM_WORDS = ("sonnet", "sonnets", "ballad", "ballads", "couplet", "couplets",
                     "acrostic", "acrostics", "elegy", "elegies", "epic", "epics",
                     "tanka", "sestina", "villanelle", "clerihew", "quatrain", "haibun")


def _names_another_form(clean, form):
    words = re.findall(r"[a-z']+", clean or "")
    mine = set(VERSE_FORM_WORDS.get(form, ())) | set(VERSE_FORM_WORDS.get("poem", ())) \
        if form == "poem" else set(VERSE_FORM_WORDS.get(form, ()))
    for word in words:
        if word in mine:
            continue
        if word in _OTHER_FORM_WORDS:
            return True
        for name, others in VERSE_FORM_WORDS.items():
            if name != form and word in others:
                return True
    return False


def _asks_for_a_verse(clean, form, noun=None):
    if _names_another_form(clean, form):
        return None
    if re.search(r"\b(?:how do i|how to|how can i|how should i|tips for|advice on|"
                 r"writes|wrote|writing|written|reads|reading)\b", clean):
        return None
    found = re.search(r"\b(?:about|of|on|regarding|describing|named|called|for)\s+(.+)$", clean)
    if found:
        words = _subject_words(found.group(1))
        if words and not (len(words) == 1 and words[0] in WHOM_IT_IS_FOR):
            return None
    return _no_subject_verse(form, noun)


WHOM_IT_IS_FOR = frozenset(("me", "us", "you", "him", "her", "them", "one"))


def _subject(clean):
    found = re.search(r"\b(?:about|of|on|regarding|describing|for|named|called)\s+(.+)$", clean)
    if not found:
        return ""
    words = _subject_words(found.group(1))
    if words and all(word in EMPTY_SUBJECT for word in words):
        return ""
    return " ".join(words)


S_FINAL_SINGULARS = frozenset((
    "christmas", "xmas", "tennis", "news", "series", "canvas", "atlas", "alias", "gas", "lens",
    "bias", "chaos", "ethics", "maths", "aerobics", "measles", "diabetes", "always",
))


def _thing(clean):
    found = re.search(r"\b(?:about|of|on|regarding|describing|for|named|called)\s+(.+)$",
                      clean)
    if not found:
        return ""
    words = _subject_words(found.group(1))
    if not words:
        return ""
    word = words[-1]
    while word in CONNECTORS and len(words) > 1:
        words = words[:-1]
        word = words[-1]
    if word.endswith("'s"):
        word = word[:-2]
    while word in SUBJECT_STOP and len(words) > 1:
        words = words[:-1]
        word = words[-1]
        if word.endswith("'s"):
            word = word[:-2]
    if word.endswith("ies") and len(word) > 4:
        return word[:-3] + "y"
    if (word.endswith("s") and not word.endswith(("ss", "is", "us"))
            and word not in S_FINAL_SINGULARS and len(word) > 3):
        return word[:-1]
    return word


def _named_nothing(clean):
    found = re.search(r"\b(?:about|of|on|regarding|describing|for|named|called)\s+(.+)$", clean)
    if not found:
        return False
    words = _subject_words(found.group(1))
    return bool(words) and all(word in EMPTY_SUBJECT for word in words)


def _lines(lines, lead=None):
    return (lead + "\n" if lead else "") + "\n".join(lines)


def _haiku(memory, understood):
    clean = understood.get("clean") or ""
    if _a_report_of_the_habit(clean):
        return _a_report_answered(clean, understood)
    subject = _subject(clean)
    if not subject:
        return _asks_for_a_verse(clean, "haiku")
    return _say("haiku", _thing(clean), subject)


def _limerick(memory, understood):
    clean = understood.get("clean") or ""
    if _a_report_of_the_habit(clean):
        return _a_report_answered(clean, understood)
    subject = _subject(clean)
    if not subject:
        return _asks_for_a_verse(clean, "limerick")
    return _say("limerick", _thing(clean), subject)


def _poem(memory, understood):
    clean = understood.get("clean") or ""
    if _a_report_of_the_habit(clean):
        return _a_report_answered(clean, understood)
    subject = _subject(clean)
    if not subject:
        return _asks_for_a_verse(clean, "poem", noun="rhyme" if "rhyme" in clean else "poem")
    return _say("poem", _thing(clean), subject,
                noun="rhyme" if "rhyme" in clean else "poem")


def _rhyme(memory, understood):
    clean = understood.get("clean") or ""
    found = re.search(r"rhyme\w*\s+(?:with|for|to)\s+([a-z']+)", clean)
    if not found:
        return None
    word = found.group(1)
    if word in NO_RHYME:
        return NO_RHYME[word]
    bare = word[:-1] if word.endswith("e") and len(word) > 3 else word
    for ending in sorted(RHYMES_BY_ENDING, key=len, reverse=True):
        if word.endswith(ending) or bare.endswith(ending):
            picks = [one for one in RHYMES_BY_ENDING[ending] if one != word][:5]
            if picks:
                return ("Words that rhyme with *%s*: %s. For a poem, the easiest thing is to put "
                        "*%s* at the end of a line and pick the rhyme that says what you mean."
                        % (word, _list_words(picks), word))
    return None


def _story_idea(memory, understood):
    clean = understood.get("clean") or ""
    seed = sum(ord(one) for one in clean) or 1
    first = STORY_IDEAS[seed % len(STORY_IDEAS)]
    second = STORY_IDEAS[(seed + 7) % len(STORY_IDEAS)]
    return ("Two to start with:\n- %s\n- %s\nWhich one sounds like yours? I can help you find "
            "the first scene, or the thing that goes wrong." % (first, second))


BRIGHT = ("sun", "birthday", "friend", "summer", "spring")
CALM = ("garden", "tea", "sea", "night", "morning")
FORMS = {"haiku": HAIKU, "limerick": LIMERICKS, "poem": POEMS}


_A_VERSE_LEAD = re.compile(
    r"^\s*(?:A|An)\s+(?:\w+\s+){0,2}(story|poem|haiku|limerick|rap|song|rhyme)\b", re.I)


def _the_form_last_time(memory):
    turns = [one for one in (memory.get("turns") or [])[-2:] if isinstance(one, dict)]
    for turn in reversed(turns):
        bot = str(turn.get("bot") or "")
        written = _A_VERSE_LEAD.match(bot)
        if written:
            return written.group(1).lower()
        said = (str(turn.get("user") or "") + " " + bot).lower()
        for form in ("haiku", "limerick", "poem"):
            if form in said:
                return form
    return None


def _lead(form, subject):
    if form == "haiku":
        return "A haiku about %s, 5-7-5:" % subject
    if form == "limerick":
        return "A limerick about %s:" % subject
    return "A short poem about %s:" % subject


def _offer(form, subject):
    name = {"haiku": "haiku", "limerick": "limerick", "rap": "rap", "song": "song",
            "story": "story"}.get(form, "poem")
    return ("A %s about %s needs one real thing in it: give me a sound, a smell or a day from it "
            "and I'll build the %s round that." % (name, subject, name))


def _say(form, thing, subject, noun=None):
    form = noun or form
    known = (form in FORMS and thing in FORMS[form]) or thing in POEMS or thing in PEOPLE
    if not known and (thing in ABSTRACT or subject.split()[-1:] and
                      subject.split()[-1] in ABSTRACT):
        return _offer(form, subject)
    if form == "haiku":
        found = HAIKU.get(thing)
        return _lines(found, _lead(form, subject)) if found else None
    if form not in FORMS:
        thing_line = POEMS.get(thing)
        lead = "A rhyme about %s:" % subject
        if thing_line:
            return _lines(thing_line, lead)
        if thing in PEOPLE:
            return _lines(WARM_POEM, lead)
        return _lines([one.format(thing=thing) for one in GENERIC_POEM], lead)
    if thing in FORMS[form]:
        return _lines(FORMS[form][thing], _lead(form, subject))
    if form != "limerick" and thing in PEOPLE:
        return _lines(WARM_POEM, _lead(form, subject))
    if form == "limerick":
        return _lines([one.format(thing=thing) for one in GENERIC_LIMERICK], _lead(form, subject))
    return _lines([one.format(thing=thing) for one in GENERIC_POEM], _lead(form, subject))


def _picked(choices, clean):
    place = sum(ord(one) for one in clean) % len(choices) if clean else 0
    return choices[place]


_A_LISTENER_IS_NAMED = re.compile(
    r"\b(?:for|to)\s+(?:my|our|a|the|his|her|their)?\s*(?:\d+|one|two|three|four|five|six|seven|"
    r"eight|nine|ten)\s*(?:year|yr)s?[ -]?old\b|"
    r"\b(?:for|to)\s+(?:my|our|the)\s+(?:kids?|children|child|toddler|baby|grandchildren|"
    r"grandson|granddaughter|niece|nephew|son|daughter|class|nursery)\b|"
    r"\bbedtime story\b|\bbedtime\b")

CHILD_STORIES = (
    "Once there was a small bear who could not sleep because the moon was too bright. He tried a "
    "hat, a blanket over his eyes and sleeping under the bed, and then he found that the moon was "
    "only a night light, and he was allowed to keep it on. Three minutes, one small problem, and "
    "the bear is safe at the end - which is the whole of what a story for a five year old needs.",
    "The duck who had forgotten how to quack found a frog who could only croak, and between them "
    "they made a noise that woke the whole pond. It ends with everybody laughing rather than with "
    "anybody taught a lesson. About three minutes long, said slowly, with a quack every time the "
    "duck tries.",
    "A little girl put a pea in her pocket and it grew all the way up to the ceiling of her "
    "bedroom, where it turned into a beanstalk with a door in it. She did not go in, because it "
    "was bedtime, and that is the end. A story for a five year old wants one idea, one small "
    "problem, and a safe last line rather than a moral.",
)


CHILD_STORY_OPENINGS = (
    "Once there was a {thing} that could not sleep because the moon was too bright.\n"
    "It tried a hat, a blanket over its eyes and sleeping under the bed, and then it found that "
    "the moon was only a night light, and it was allowed to keep it on.",
    "There was a {thing} in the garden one Tuesday, and nobody in the house had seen one before.\n"
    "The dog said hello first, then everybody did, and by bedtime it had a name and a place by "
    "the door.",
    "A little girl found a {thing} in her pocket one morning and it grew all the way up to the "
    "ceiling of her bedroom.\n"
    "It was bedtime, so she did not climb it. She said goodnight to it instead, and in the "
    "morning it was exactly the same size.",
)


def _the_listener_lead(clean):
    age = re.search(r"\b(\d+|one|two|three|four|five|six|seven|eight|nine|ten)\b", clean)
    return "A short one for a child" if not age else "A short one for a %s year old" % age.group(1)


def _a_story_for_the_listener(clean):
    return _the_listener_lead(clean) + ": " + _picked(CHILD_STORIES, clean)


def _a_child_story_about(clean, thing):
    opening = _picked(CHILD_STORY_OPENINGS, clean + thing)
    return _the_listener_lead(clean) + ": " + opening.format(thing=thing)


_ASKS_ABOUT_A_STORY = re.compile(
    r"\b(?:what makes|how long (?:should|do|does|is)|how (?:do|can|would) (?:i|you|we) "
    r"(?:write|start|plan)|how to (?:write|start|plan)|what should (?:a|my|the) story|"
    r"where do i start|story structure|structure a story)\b", re.I)

ASKS_FOR_A_STORY = re.compile(
    r"\btell\s+(?:me|us)\b|\btell\s+(?:\w+\s+){0,3}(?:a |another |one more )?(?:story|stories|tale)\b"
    r"|\b(?:give|write|read|make up|do|need|want|hear|fancy|have|get)\w*\s+"
    r"(?:\w+\s+){0,3}(?:story|stories|tale)\b|\b(?:story|stories|tale)\s+(?:about|for|of)\b|"
    r"\bbedtime story\b|\banother story\b|\bone more story\b|\bstor(?:y|ies) please\b|"
    r"\b(?:short|quick|little)\s+(?:story|stories|tale)\b|"
    r"\b(?:any|some) (?:good |short |quick |nice |funny )?(?:story|stories)\b")

A_STORY_ALREADY_TOLD = re.compile(r"\b(?:telling|tells|told|reading|reads|read|heard|hears)\b")
A_NEW_ONE_ASKED_FOR = re.compile(
    r"\b(?:write|wrote|make\s+up|made\s+up|compose|draft)\s+(?:me\s+|us\s+)?(?:one|another|a|an|some)\b"
    r"|\b(?:tell|read|give)\s+(?:me|us)\b"
    r"|\b(?:one\s+more|another\s+one|one\s+other)\b"
    r"|\bwant\s+(?:a|another|one\s+more)\b", re.I)
ASKS_THE_BOT = re.compile(r"\b(?:tell|read)\s+(?:me|us)\b")
A_STORY_ALREADY_HEARD = re.compile(r"\b(?:did|do|have|has|had) you (?:ever )?hear(?:d)?\b")


HEARD_IT_ALREADY = (
    "I haven't heard that one - go on, tell me. You'll tell it better than I could make it up.",
    "No, and now I want to. Go on.",
)


def _a_story_is_asked_for(clean):
    if not ASKS_FOR_A_STORY.search(clean):
        return False
    if ASKS_THE_BOT.search(clean):
        return True
    if A_STORY_ALREADY_HEARD.search(clean):
        return False
    if A_NEW_ONE_ASKED_FOR.search(clean):
        return True
    return not A_STORY_ALREADY_TOLD.search(clean)


_SECOND_STORY = re.compile(
    r"^(?:and|then|also|ok|okay|now|so)?\s*(?:one more|one other|another one|one)\s+about\b",
    re.I)
_A_STORY_WORD = re.compile(r"\b(?:story|stories|tale|tales)\b", re.I)


def _the_line_to_read_for_a_story(understood):
    typed = str((understood or {}).get("text") or "").strip()
    clean = str((understood or {}).get("clean") or "")
    if typed and typed != clean and _SECOND_STORY.search(typed.lower()):
        return typed
    return clean


def _the_story_was_just_told(memory):
    for turn in reversed(list((memory or {}).get("turns") or [])):
        if not isinstance(turn, dict):
            continue
        said = str(turn.get("bot") or "")
        if said:
            return bool(re.search(r"\bstory\b", said, re.I))
    return False


_PLACEHOLDER_SUBJECT = frozenset((
    "anything", "something", "nothing", "anyone", "someone", "somebody", "everyone",
    "everybody", "anybody", "nobody", "whatever", "whichever", "whoever", "it", "that", "this",
    "more", "else", "surprise", "me", "them", "us",
))


def _a_placeholder_word(subject):
    words = subject.split()
    if not words:
        return True
    return words[0].strip(".,!?;:'\"").lower() in _PLACEHOLDER_SUBJECT


REPORTS_ON_A_FORM = re.compile(
    r"\b(?:i|we|he|she|they)\s+(?:tried|read|told|watched|listened\s+to|sang|heard)\b"
    r"|\b(?:keeps?|kept)\s+(?:telling|reading|saying|making|watching|singing|doing)\b"
    r"|\b(?:my|our|his|her|the)\s+\w+\s+(?:tells?|told|reads?|sings?|sang|made\s+up)\b"
    r"|\b(?:he|she|they)\s+(?:tells?|reads?|sings?|makes?\s+up|told|read|sang)\b")
ASKS_FOR_ONE = re.compile(
    r"\b(?:write|written|make\s+up|compose|draft|give\s+me|tell\s+me|read\s+me|"
    r"can\s+you|could\s+you|would\s+you|i\s+(?:want|need|would\s+like)|"
    r"any\s+ideas?|what\s+(?:about|should))\b")


def _a_report_of_the_habit(clean):
    line = str(clean or "")
    return bool(REPORTS_ON_A_FORM.search(line)) and not ASKS_FOR_ONE.search(line)


def _the_last_line_reported_a_form(memory):
    turns = [one for one in (memory or {}).get("turns") or [] if isinstance(one, dict)]
    for turn in reversed(turns):
        said = str(turn.get("user") or "")
        if not said:
            continue
        if not str(turn.get("bot") or "").strip() and turn is turns[-1]:
            continue
        return _a_report_of_the_habit(said)
    return False


REPORT_BACK = {
    "story": (
        "A story they ask for again and again is the good kind - they know it by heart by now. "
        "What's it about?",
        "That's a bedtime routine doing its job. Does it have to be word for word, or does it "
        "change a bit each night?",
        "The same story over and over is how a favourite works - they are hearing the bits they "
        "like. Do you get a say in which one?",
        "The same story at the same time every night is a habit worth having. Do they join in on "
        "the lines they know yet?",
    ),
    "rap": (
        "Raps made up at home are words and rhythm at the same time, which is a good sign. What do "
        "they rap about?",
        "Making up raps is how a lot of people find their voice. Does any of it stick, or is it "
        "all gone the moment it's said?",
        "A kid with a rap habit is usually listening to words in a different way to everyone else. "
        "Do you get to hear them?",
    ),
    "song": (
        "The same song on repeat is exactly how a favourite works. Which one is it?",
        "A song sung the same way every time has properly stuck. Do you join in, or is it theirs "
        "alone?",
        "That's a good sign - singing the same thing over is how words and tune get learned. Is it "
        "one you know too?",
    ),
    "poem": (
        "Poems made up at home are somebody playing with words, which is worth a lot. Do you get to "
        "hear them?",
        "A child writing poems is noticing things most people walk past. What are they about?",
        "That's the age poems start, usually - bad ones, brilliant ones, all of them out loud. Does "
        "she read them to you?",
    ),
    "haiku": (
        "Haikus at home is a lovely habit - counting the sounds is half the fun of it. Do you get "
        "to hear them?",
        "A haiku habit means someone has been listening closely to how a line sounds. What do they "
        "write them about?",
    ),
    "limerick": (
        "Limericks are the form people make up without being asked, so that habit usually runs. Do "
        "you get the rude ones?",
        "A limerick habit at home is a good sign - the rhythm does most of the work and the joke "
        "does the rest. Who do they do them for?",
    ),
    "rhyme": (
        "Rhymes made up as they go is how the sound of words gets learned. Do they keep them, or "
        "does each one vanish?",
        "A rhyming habit is a good one to have around. Do you get to hear the new ones?",
    ),
}

A_REPEATED_REPORT = re.compile(
    r"\bkeeps?\b|\bkept\b|\b(?:the\s+)?same\b|\bevery\s+(?:night|day|time|evening|week)\b"
    r"|\bagain\s+and\s+again\b|\bover\s+and\s+over\b|\bevery\s+time\b|\bagain\b", re.I)

REPORT_ONCE_BACK = {
    "story": (
        "Go on - what was the bit you liked best?",
        "Those are the good ones, the ones that turn up out of nowhere. What's stuck with you "
        "from it?",
    ),
}
REPORT_ONCE_GENERIC = (
    "A %s out of nowhere is the best kind. What was it about?",
    "I like that - a bit of a %s in the middle of the day. Did anyone else get to hear it?",
)

_A_FORM_IN_THE_REPORT = (
    ("haiku", re.compile(r"\bhaikus?\b", re.I)),
    ("limerick", re.compile(r"\blimericks?\b", re.I)),
    ("rap", re.compile(r"\braps?\b|\brapping\b", re.I)),
    ("song", re.compile(r"\bsongs?\b|\bsing(?:ing|s|)\b|\bsang\b", re.I)),
    ("rhyme", re.compile(r"\brhym(?:e|es|ing)\b", re.I)),
    ("poem", re.compile(r"\bpoems?\b|\bpoetry\b", re.I)),
    ("story", re.compile(r"\bstor(?:y|ies)\b|\btales?\b", re.I)),
)


A_READING_ROUTINE = re.compile(r"\bread(?:s|ing)?\b|\blistened\s+to\b|\bwatched\b", re.I)
A_MAKING_UP = re.compile(r"\bmak(?:e|es|ing)\s+up\b|\bmade\s+up\b|\bsing|\btells?\b|\btelling\b",
                         re.I)


A_QUESTION_BESIDE_THE_REPORT = re.compile(
    r"\b(?:should|shall|can|could|would|will|is|are|am|do|does|did|what|why|how|when|where|who"
    r"|which|if)\b", re.I)


def _a_report_answered(clean, understood=None):
    if not _a_report_of_the_habit(clean):
        return None
    line = str(clean or "")
    if A_QUESTION_BESIDE_THE_REPORT.search(line):
        return None
    if A_READING_ROUTINE.search(line) and not A_MAKING_UP.search(line):
        return None
    form = "story"
    for name, shape in _A_FORM_IN_THE_REPORT:
        if shape.search(line):
            form = name
            break
    if not A_REPEATED_REPORT.search(line):
        once = REPORT_ONCE_BACK.get(form)
        if once:
            return _picked(once, line)
        return _picked(REPORT_ONCE_GENERIC, line) % form
    return _picked(REPORT_BACK[form], line)


def _story(memory, understood):
    clean = _the_line_to_read_for_a_story(understood)
    if _a_report_of_the_habit(clean):
        return _a_report_answered(clean, understood)
    if (_the_last_line_reported_a_form(memory) and not ASKS_FOR_ONE.search(clean)
            and not _SECOND_STORY.match(str((understood or {}).get("plain") or "").strip())):
        return None
    typed = str((understood or {}).get("plain") or (understood or {}).get("text") or "")
    if typed and typed != clean and not _A_STORY_WORD.search(typed):
        if not _SECOND_STORY.match(typed.strip()) or not _the_story_was_just_told(memory):
            return None
    if not _A_STORY_WORD.search(clean):
        if not _SECOND_STORY.match(clean.strip()):
            return None
        if not _the_story_was_just_told(memory):
            return None
    if _ASKS_ABOUT_A_STORY.search(clean):
        return None
    if A_STORY_ALREADY_HEARD.search(clean) and ASKS_FOR_A_STORY.search(clean):
        return _picked(HEARD_IT_ALREADY, clean)
    if not _a_story_is_asked_for(clean):
        return None
    if _A_LISTENER_IS_NAMED.search(clean):
        named = re.search(r"\b(?:about|of|on|regarding)\s+(?P<subject>\S.*)$", clean)
        if not named or _a_placeholder_word(named.group("subject")):
            return _a_story_for_the_listener(clean)
        child_thing = _thing(named.group(0))
        if child_thing and not _a_placeholder_word(child_thing):
            return _a_child_story_about(clean, child_thing)
        return _a_story_for_the_listener(clean)
    thing = _thing(clean) or GENERIC_STORY_THING
    if _a_placeholder_word(thing):
        thing = GENERIC_STORY_THING
    subject = _subject(clean)
    if subject and _a_placeholder_word(subject):
        subject = None
    if thing in ABSTRACT and subject:
        return _offer("story", subject)
    lead = (STORY_LEADING["story"].format(subject=subject) if subject
            else "Here is one, made up on the spot:")
    opening = _the_opening_not_said_yet(thing, memory, clean)
    return lead + "\n" + opening


def _the_opening_not_said_yet(thing, memory, clean=""):
    start = sum(ord(one) for one in thing) % len(STORY_OPENINGS) if thing else 0
    told = " ".join(str(turn.get("bot") or "") for turn in ((memory or {}).get("turns") or [])
                    if isinstance(turn, dict))
    filled = dict(thing=thing, **_article_for(thing, clean=clean))
    for step in range(len(STORY_OPENINGS)):
        one = STORY_OPENINGS[(start + step) % len(STORY_OPENINGS)].format(**filled)
        if one.split("\n", 1)[0] not in told:
            return one
    return STORY_OPENINGS[start].format(**filled)


def _rap(memory, understood):
    clean = understood.get("clean") or ""
    if _a_report_of_the_habit(clean):
        return _a_report_answered(clean, understood)
    if _named_nothing(clean):
        return None
    thing = _thing(clean) or NO_THING_IN_A_VERSE["rap"]
    subject = _subject(clean) or thing
    if thing in ABSTRACT:
        return _offer("rap", subject)
    lines = [one.format(thing=thing, **_article_for(thing, clean=clean)) for one in GENERIC_RAP]
    lead = (STORY_LEADING["rap"].format(subject=subject) if _subject(clean)
            else NO_SUBJECT_LEADING["rap"])
    return _lines(lines, lead)


def _song(memory, understood):
    clean = understood.get("clean") or ""
    if _a_report_of_the_habit(clean):
        return _a_report_answered(clean, understood)
    if _named_nothing(clean):
        return None
    thing = _thing(clean) or NO_THING_IN_A_VERSE["song"]
    subject = _subject(clean) or thing
    if thing in ABSTRACT:
        return _offer("song", subject)
    lead = (STORY_LEADING["song"].format(subject=subject) if _subject(clean)
            else NO_SUBJECT_LEADING["song"])
    return lead + "\n" + GENERIC_SONG.format(thing=thing, **_article_for(thing, clean=clean))


CHARACTER_NAME_RULES = (
    "Pick a plain first name and a surname that says what they do or where they are from: Nell "
    "Harrow, Amos Pike, Ivy Sanderson. Write down three and the story usually picks one itself - "
    "and say the full name out loud twice, because a name you stumble over is one the reader will "
    "too.",
    "A name that is easy to say and slightly odd is the one that sticks: Ruth Okonkwo, Samuel "
    "Beck, Ada Pryce. Give the villain the smoother name and the hero the plainer one, and skip "
    "the apostrophes - nobody remembers how to spell them.",
    "Old-fashioned first names worn by young people: Walter, Mabel, Agnes, Ernest. It does the "
    "work of a description in one word, because the reader fills in the corners, and it fits "
    "every kind of story from a farm to a space station.",
)


def _character_name(memory, understood):
    clean = str((understood or {}).get("clean") or "")
    if re.search(r"\b(?:villain|villainess|baddie|antagonist|hero|heroine)\b", clean, re.I):
        return CHARACTER_NAME_RULES[1]
    return _picked(CHARACTER_NAME_RULES, clean)


def _nickname(memory, understood):
    clean = understood.get("clean") or ""
    picks = []
    for step in range(3):
        first = NICK_FIRST[(sum(ord(one) for one in clean) + step * 3) % len(NICK_FIRST)]
        last = NICK_LAST[(sum(ord(one) for one in clean) // 7 + step * 5) % len(NICK_LAST)]
        picks.append("%s %s" % (first, last))
    return ("Start with *%s*; *%s* and *%s* if it sticks. A nickname works best when it comes "
            "from something only you two know." % (picks[0], picks[1], picks[2]))


_A_SECOND_ONE = re.compile(
    r"^\s*(?:(?:and|then|also|ok|okay|now|so|go on|come on|can you|could you|would you|please|"
    r"do|give me|write|make|sing|tell|create)\b[\s,]*)*"
    r"(?:one\s+more|one\s+other|another\s+one|another|one)\b"
    r"(?:\s*(?:about|of|on)\s+(.+?))?\s*[.!?]*\s*$", re.I)
_NOT_A_VERSE_ASK = re.compile(
    r"\b(?:thing|question|quick\s+question|moment|minute|sec|favour|favor|idea|point|"
    r"thought|ask|time)\b", re.I)
_ANOTHER_FORM = {"story": "_story", "poem": "_poem", "haiku": "_haiku",
                 "limerick": "_limerick", "rap": "_rap", "song": "_song", "rhyme": "_rhyme"}


def _the_second_one_asked_for(understood):
    for field in ("text", "plain", "clean"):
        typed = " ".join(str((understood or {}).get(field) or "").split())
        if not typed or _NOT_A_VERSE_ASK.search(typed):
            continue
        found = _A_SECOND_ONE.match(typed)
        if found:
            return (found.group(1) or "").strip(" .,!?") or None
    return ""


def _another_one(memory, understood):
    form = _the_form_last_time(memory)
    if not form:
        return None
    second = _the_second_one_asked_for(understood)
    writer = globals().get(_ANOTHER_FORM.get(form, ""))
    if second != "" and writer:
        asked = "a %s about %s" % (form, second) if second else "a %s" % form
        said = writer(memory, {"clean": asked, "text": asked})
        if said:
            return said
    clean = understood.get("clean") or ""
    thing = _thing(clean)
    if thing:
        return _say(form, thing, _subject(clean))
    brighter = re.search(r"happ|bright|cheer|funny|nicer|lighter|lift", clean)
    calmer = brighter or re.search(r"calm|quiet|sooth|gentl|soft|slower|easier", clean)
    if not calmer:
        return None
    for key in (BRIGHT if brighter else CALM):
        if key in FORMS.get(form, {}):
            lead = "Something brighter, then." if brighter else "Something quieter, then."
            return _lines(FORMS[form][key], lead)
    return None


def _quiz_name(memory, understood):
    clean = understood.get("clean") or ""
    seed = sum(ord(one) for one in clean) or 1
    names = QUIZ_NAMES if re.search(r"\b(?:quiz|trivia)\b", clean) else TEAM_NAMES
    picks = [names[(seed + step) % len(names)] for step in (0, 3, 6)]
    return ("For the sheet: *%s*. Others that go down well: *%s* and *%s*."
            % (picks[0], picks[1], picks[2]))


_ALL_ABSTRACT = ABSTRACT
_GLIB = ("lockdown", "pandemic", "covid", "coronavirus", "virus", "grief", "loss", "fear",
         "anxiety", "depression", "stress", "illness", "cancer", "dementia", "addiction",
         "recovery", "divorce", "marriage", "war", "unemployment", "poverty", "loneliness",
         "sadness", "anger", "regret", "guilt", "death", "memories", "memory", "past",
         "childhood", "friendship", "motherhood", "fatherhood", "ageing")
ABSTRACT = tuple(word for word in _ALL_ABSTRACT if word in _GLIB)
_OFFERED = tuple(word for word in _ALL_ABSTRACT if word not in _GLIB)
_OFFER_TAIL = ("\nGive me one real thing from it - a sound, a smell or a day - and I will "
               "write the {form} round that.")


def _asked_for_what_they_already_tried(understood, *things):
    tried = understood.get("tried")
    if not isinstance(tried, list) or not tried:
        return False
    if asks_for_one_more(understood.get("norm")):
        return False
    tried = {str(word).lower() for word in tried}
    for thing in things:
        for word in re.findall(r"[a-z']+", str(thing or "").lower()):
            if word in tried:
                return True
    return False


_THE_FORM_NAMED = {
    "story": ("story", "stories", "tale", "tales"),
    "poem": ("poem", "poems", "verse", "sonnet", "ode", "couplet", "rhyme", "rhymes"),
    "rhyme": ("rhyme", "rhymes", "rhyming"),
    "haiku": ("haiku", "haikus"),
    "limerick": ("limerick", "limericks"),
    "rap": ("rap", "raps", "rapping"),
    "song": ("song", "songs", "lyric", "lyrics"),
}


def _with_the_detail_asked_for(build, form):
    names = _THE_FORM_NAMED[form] if form in _THE_FORM_NAMED else (form, form + "s")

    def answer(memory, understood):
        if _asked_for_what_they_already_tried(understood, *names):
            return None
        reply = build(memory, understood)
        if not reply:
            return reply
        clean = understood.get("clean") or ""
        if _a_report_of_the_habit(clean):
            return reply
        subject = _subject(clean) or ""
        thing = _thing(clean) or ""
        words = subject.split()[-1:]
        if thing in _OFFERED or (words and words[0] in _OFFERED):
            reply = reply + _OFFER_TAIL.format(form=form)
        return reply
    return answer


def _a_second_one_read_first(writer, form):
    def write(memory, understood):
        second = _the_second_one_asked_for(understood)
        if second != "":
            chosen = _the_form_last_time(memory)
            if chosen and chosen != form and chosen in _ANOTHER_FORM:
                asked = ("a %s about %s" % (chosen, second) if second else "a %s" % chosen)
                return globals()[_ANOTHER_FORM[chosen]](memory, {"clean": asked, "text": asked})
            asked = "a %s about %s" % (form, second) if second else "a %s" % form
            said = writer(memory, {"clean": asked, "text": asked})
            return said if said else (None if second is None else writer(memory, understood))
        return writer(memory, understood)
    return write


_haiku = _with_the_detail_asked_for(_haiku, "haiku")
_limerick = _with_the_detail_asked_for(_limerick, "limerick")
_poem = _with_the_detail_asked_for(_poem, "poem")
_story = _with_the_detail_asked_for(_story, "story")
_rap = _with_the_detail_asked_for(_rap, "rap")
_song = _with_the_detail_asked_for(_song, "song")

for _form_name, _form_word in (("_haiku", "haiku"), ("_limerick", "limerick"),
                               ("_poem", "poem"), ("_story", "story"), ("_rap", "rap"),
                               ("_song", "song"), ("_rhyme", "rhyme")):
    globals()[_form_name] = _a_second_one_read_first(globals()[_form_name], _form_word)
del _form_name, _form_word


PICK_MEDIUM = ("film", "films", "movie", "movies", "series", "boxset", "box set", "show",
               "shows", "telly", "book", "books", "novel", "novels", "read", "reading",
               "documentary", "documentaries", "watch", "watching")

PICK_ASK = ("looking for", "looking", "after", "want", "wanted", "wanting", "fancy",
            "fancied", "in the mood", "in the mood for", "need", "need something", "ideas",
            "idea", "any ideas", "recommend", "recommended", "recommendation",
            "recommendations", "suggest", "suggestion", "suggestions", "pick", "picks",
            "decent", "good", "any", "anything", "to watch", "to read")

PICK_WHO = ("with my parents", "my parents", "parents", "with my mum", "with my dad",
            "with my mother", "with my father", "in laws", "my in laws",
            "with my wife", "with my husband", "with my partner",
            "partner", "with my girlfriend", "with my boyfriend", "with friends",
            "my friends", "friends", "for me", "for myself", "just me", "on my own",
            "by myself")

FREE_TELLS = ("only have bbc", "only got bbc", "only bbc", "bbc and itv", "bbc itv",
              "just bbc", "just itv", "only itv", "freeview", "free to air", "free-to-air",
              "terrestrial", "normal telly", "normal tv", "no subscription", "no subscriptions",
              "dont have netflix", "don't have netflix", "no netflix", "canceled netflix",
              "cancelled netflix", "cant afford netflix", "can't afford netflix",
              "only iplayer", "only channel 4", "no sky", "dont have sky", "don't have sky",
              "no streaming", "dont have any subscriptions", "no disney", "no prime")
SUBS_TELLS = ("no subtitles", "not subtitles", "without subtitles", "hate subtitles",
              "do not like subtitles", "does not like subtitles", "do not do subtitles",
              "does not do subtitles", "cannot stand subtitles", "can not stand subtitles",
              "do not want subtitles", "does not want subtitles",
              "hates subtitles", "hate foreign", "hates foreign", "no foreign films",
              "nothing foreign", "dont like subtitles", "doesnt like subtitles",
              "doesn't like subtitles", "dont do subtitles", "doesnt do subtitles",
              "cant stand subtitles", "cannot stand subtitles", "cant read subtitles",
              "no reading subtitles", "turned off by subtitles", "put off by subtitles",
              "wont watch subtitles", "wont watch foreign", "doesnt want subtitles",
              "dont want subtitles", "no dubbing", "prefers dubbing")

CINEMA = {
    "french": ("French", "France", "French"), "france": ("French", "France", "French"),
    "italian": ("Italian", "Italy", "Italian"), "italy": ("Italian", "Italy", "Italian"),
    "spanish": ("Spanish", "Spain", "Spanish"), "spain": ("Spanish", "Spain", "Spanish"),
    "german": ("German", "Germany", "German"), "germany": ("German", "Germany", "German"),
    "japanese": ("Japanese", "Japan", "Japanese"), "japan": ("Japanese", "Japan", "Japanese"),
    "korean": ("Korean", "Korea", "Korean"), "korea": ("Korean", "Korea", "Korean"),
    "chinese": ("Chinese", "China", "Mandarin"), "china": ("Chinese", "China", "Mandarin"),
    "iranian": ("Iranian", "Iran", "Persian"), "iran": ("Iranian", "Iran", "Persian"),
    "danish": ("Danish", "Denmark", "Danish"), "denmark": ("Danish", "Denmark", "Danish"),
    "brazilian": ("Brazilian", "Brazil", "Portuguese"), "brazil": ("Brazilian", "Brazil", "Portuguese"),
    "polish": ("Polish", "Poland", "Polish"), "poland": ("Polish", "Poland", "Polish"),
    "russian": ("Russian", "Russia", "Russian"), "russia": ("Russian", "Russia", "Russian"),
    "swedish": ("Swedish", "Sweden", "Swedish"), "sweden": ("Swedish", "Sweden", "Swedish"),
    "mexican": ("Mexican", "Mexico", "Spanish"), "mexico": ("Mexican", "Mexico", "Spanish"),
    "turkish": ("Turkish", "Turkey", "Turkish"), "turkey": ("Turkish", "Turkey", "Turkish"),
    "greek": ("Greek", "Greece", "Greek"), "greece": ("Greek", "Greece", "Greek"),
    "irish": ("Irish", "Ireland", "English"), "ireland": ("Irish", "Ireland", "English"),
    "nigerian": ("Nigerian", "Nigeria", "English"), "nigeria": ("Nigerian", "Nigeria", "English"),
    "vietnamese": ("Vietnamese", "Vietnam", "Vietnamese"), "vietnam": ("Vietnamese", "Vietnam", "Vietnamese"),
    "thai": ("Thai", "Thailand", "Thai"), "thailand": ("Thai", "Thailand", "Thai"),
    "israeli": ("Israeli", "Israel", "Hebrew"), "israel": ("Israeli", "Israel", "Hebrew"),
    "lebanese": ("Lebanese", "Lebanon", "Arabic"), "lebanon": ("Lebanese", "Lebanon", "Arabic"),
    "indian": ("Indian", "India", "Hindi"), "india": ("Indian", "India", "Hindi"),
    "bollywood": ("Bollywood", "India", "Hindi"),
    "czech": ("Czech", "Czechia", "Czech"), "czechia": ("Czech", "Czechia", "Czech"),
}
CINEMA_WORDS = tuple(CINEMA)

_COUNTRY_AFTER_A_LITTLE_WORD = (
    "out", "up", "off", "it", "them", "the", "my", "our", "your", "his", "her", "their",
    "a", "an", "this", "that", "these", "those", "into", "onto", "again", "properly", "well",
)
_COUNTRY_BEFORE_A_THING = (
    "yoghurt", "yogurt", "salad", "bread", "cheese", "dressing", "sauce", "takeaway",
    "food", "curry", "stew", "sausage", "ham", "mustard", "wine", "beer", "coffee",
    "meatballs", "omelette", "toast", "stick", "beans", "bath", "delight", "barber",
    "massage", "shepherd", "measles", "knotweed", "roulette", "linen", "polish", "plait",
    "onion", "fries", "toast", "press", "cuff",
)


def _a_country_is_a_country(understood):
    words = [w.lower() for w in (understood.get("words") or ())]
    for i, word in enumerate(words[:-1]):
        if word not in CINEMA:
            continue
        after = words[i + 1]
        if after in _COUNTRY_AFTER_A_LITTLE_WORD:
            return False
        if after in _COUNTRY_BEFORE_A_THING:
            return False
    return True


NATIONAL_CINEMA = (
    ("Amelie", "France", "Paris, whimsical, and the film most people mean by a French film"),
    ("The Intouchables", "France", "warm, very funny, and the biggest French hit abroad"),
    ("Portrait of a Lady on Fire", "France", "slow, beautiful, and two hours of looking"),
    ("Cinema Paradiso", "Italy", "a small-town cinema and a whole life in it, and the ending lands"),
    ("The Great Beauty", "Italy", "Rome at its most beautiful and most empty"),
    ("Pans Labyrinth", "Spain", "a fairy tale under a war, and not for young children"),
    ("All About My Mother", "Spain", "Almodovar at his warmest, and it moves fast"),
    ("Good Bye Lenin", "Germany", "funny, about a whole country changing in a year"),
    ("Run Lola Run", "Germany", "81 minutes, fast, and impossible to look away from"),
    ("Spirited Away", "Japan", "the animated one everyone should see once"),
    ("Seven Samurai", "Japan", "the film every action film borrows from"),
    ("Shoplifters", "Japan", "a family that is not quite a family, and very warm"),
    ("Parasite", "Korea", "a comedy that turns into something else, and won Best Picture"),
    ("The Handmaiden", "Korea", "twisty, stylish and not for a family evening"),
    ("Crouching Tiger Hidden Dragon", "China", "the sword fights float, and the story holds"),
    ("Raise the Red Lantern", "China", "beautiful and hard, and it stays with you"),
    ("A Separation", "Iran", "two families and one lie, and nothing else needed"),
    ("Children of Heaven", "Iran", "gentle, about a lost pair of shoes, and safe for children"),
    ("Another Round", "Denmark", "four teachers and a bottle, funny and then serious"),
    ("The Hunt", "Denmark", "Mads Mikkelsen, a small town and a rumour, and it is gripping"),
    ("City of God", "Brazil", "fast, brutal and brilliant, and not a gentle evening"),
    ("Central Station", "Brazil", "a road film about a boy and a woman who writes letters"),
    ("Ida", "Poland", "80 minutes, black and white, and quiet in a good way"),
    ("Cold War", "Poland", "two people across years and borders, and the music"),
    ("Solaris", "Russia", "slow science fiction, for a patient evening"),
    ("Leviathan", "Russia", "a house, a mayor and a bottle, and very Russian"),
    ("The Seventh Seal", "Sweden", "the chess game with Death, and shorter than it sounds"),
    ("Let the Right One In", "Sweden", "a vampire film that is really about being twelve"),
    ("Roma", "Mexico", "a year in one household, and the sea scene alone is worth it"),
    ("Y Tu Mama Tambien", "Mexico", "a road trip that turns, and not for a family evening"),
    ("Once Upon a Time in Anatolia", "Turkey", "slow, patient and worth it"),
    ("Mustang", "Turkey", "five sisters, and it is angry and funny at once"),
    ("Zorba the Greek", "Greece", "the dancing-on-the-beach one, and it is about saying yes"),
    ("The Commitments", "Ireland", "a Dublin soul band, and the songs are the point"),
    ("Lionheart", "Nigeria", "Nollywood's best known, and it is on Netflix"),
    ("The Scent of Green Papaya", "Vietnam", "quiet and beautiful, and very little happens"),
    ("Uncle Boonmee", "Thailand", "slow and strange, for somebody who likes that"),
    ("Waltz with Bashir", "Israel", "animation about memory and war, and it is not gentle"),
    ("Capernaum", "Lebanon", "a child sues his parents, and it is hard but worth it"),
    ("Lagaan", "India", "a village cricket match against the British, and nearly four hours"),
    ("Dangal", "India", "a father, two daughters and wrestling, and it is a true story"),
)

FILM_KINDS = {
    "christmas": ("Christmas", "a Christmas film", (
        ("The Muppet Christmas Carol", 85, "funny, warm, and the songs stay with you"),
        ("It's a Wonderful Life", 130, "the one everyone ends on, and it earns the ending"),
        ("Home Alone", 103, "daft, and everyone in the room has seen it before"),
    )),
    "musical": ("musical", "a musical", (
        ("Singin' in the Rain", 103, "the one that makes people like musicals"),
        ("La La Land", 128, "bright, sad at the end, and easy to follow"),
        ("The Sound of Music", 174, "long, which is what a wet Sunday wants"),
    )),
    "action": ("action", "an action film", (
        ("Die Hard", 132, "still the best one, and it is a Christmas film too"),
        ("Mad Max: Fury Road", 120, "one long chase, and it never drags"),
        ("John Wick", 101, "short, clean, and all about the fighting"),
    )),
    "western": ("western", "a western", (
        ("High Noon", 85, "short, tense, and over in an hour and a half"),
        ("True Grit", 110, "the newer one: funny, and a girl who outtalks everyone"),
        ("Unforgiven", 130, "the one that turns the western over"),
    )),
    "superhero": ("superhero", "a superhero film", (
        ("Spider-Man: Into the Spider-Verse", 117, "the animation is worth it on its own"),
        ("The Incredibles", 115, "works for adults and children in the same room"),
        ("Guardians of the Galaxy", 121, "funny first and superhero second"),
    )),
}
ANIMATION_ROWS = (
    ("Spirited Away", 125, "the one that turns people who say they do not like animation"),
    ("The Mitchells vs the Machines", 114, "fast, funny, and a robot apocalypse a family can watch"),
    ("Toy Story", 81, "short, and it still holds up"),
)
FILM_KINDS["thriller"] = ("thriller", "a thriller", (
    ("Sicario", 121, "cold and relentless, and it never lets you settle"),
    ("Prisoners", 153, "a kidnapping and a father who will not stop looking"),
    ("Gone Girl", 149, "a marriage thriller that keeps turning on you"),
))
FILM_KINDS["animated"] = FILM_KINDS["animation"] = (
    "animated", "an animated film", ANIMATION_ROWS)
FILM_KINDS["cowboy"] = FILM_KINDS["western"]
FILM_KINDS["christmassy"] = FILM_KINDS["christmas"]

FILM_KIND_WORDS = tuple(FILM_KINDS)


def _kind_words(kind):
    label, said_as, _rows = FILM_KINDS.get(kind, ("", "", ()))
    words = {kind, kind + "s", label, label + "s", said_as}
    return frozenset(word for word in words if word)


KIND_REFUSED_AFTER = re.compile(
    r"\b(?:is|are|was|were)?\s*(?:not|never)\s+(?:really\s+)?(?:for\s+(?:me|us)|my\s+(?:thing|"
    r"sort|cuppa|cup|kind)|what\s+i|something\s+i|anything\s+i|a\s+fan|keen|into\s+it)\b"
    r"|\bis\s+out\b|\bare\s+out\b|\btoo\s+much\b|\bover\s+the\s+top\b", re.I)

def _the_subject_is_wanted(understood):
    for text in _own_texts(understood):
        if _a_word_is_turned_down(text, tuple(SHOW_SUBJECT_NAMES), KIND_REFUSED_AFTER):
            return False
    return True


DOCUMENTARY_WORDS = ("documentary", "documentaries", "docuseries", "docu series", "docu-series")


def _a_documentary_is_wanted(understood):
    for text in _own_texts(understood):
        if _a_word_is_turned_down(text, DOCUMENTARY_WORDS, KIND_REFUSED_AFTER):
            return False
    return True


KIND_AVOID = ("dinner", "lunch", "tea", "supper", "breakfast", "recipe", "recipes", "cook",
              "cooking", "roast", "turkey", "stuffing", "pudding", "cake", "mince pies",
              "menu", "meal", "meals", "food", "sauce", "gravy", "table", "tree",
              "decorations", "decorate", "decorating", "presents", "present", "gift",
              "gifts", "cards", "shopping", "buy", "bought", "budget", "leftovers",
              "timing", "opening hours", "church", "midnight mass",
              "party", "parties", "fancy dress", "costume", "costumes", "themed")

FILM_GENRE_WORDS = ("space", "sci-fi", "sci fi", "scifi", "science fiction",
                    "war", "heist", "spy", "gangster", "biopic", "romcom")


def _names_a_film_genre(line):
    words = " " + _plain_words(line) + " "
    return any(re.search(r"(?<![a-z0-9])" + re.escape(word) + r"(?![a-z0-9])", words)
               for word in FILM_GENRE_WORDS)


LIMIT_WORDS = ("under", "less than", "no longer than", "shorter than", "max", "maximum",
               "at most")


FILM_RUNTIME = (
    ("A Grand Day Out", 23, "Wallace and Gromit, and it is over in twenty minutes"),
    ("The Snowman", 27, "the animation, no words, and it is a Christmas thing"),
    ("Sherlock Jr.", 45, "Buster Keaton, silent, and funnier than most films twice as long"),
    ("Before Sunset", 80, "two people talking for the whole film, and it flies"),
    ("Ida", 80, "black and white, quiet, and 80 minutes is the whole of it"),
    ("Toy Story", 81, "the first one, and it has not dated"),
    ("Run Lola Run", 81, "loud, fast, and the same twenty minutes three times"),
    ("Locke", 85, "one man, one car, one phone call after another"),
    ("The Iron Giant", 86, "animation that adults take to as much as children"),
    ("The Muppet Christmas Carol", 85, "funny, warm, and the songs stay with you"),
    ("High Noon", 85, "short, tense, and over in an hour and a half"),
    ("Cold War", 88, "Polish, black and white, and short for how much it holds"),
    ("12 Angry Men", 96, "one room and twelve men, and it never sits still"),
    ("When Harry Met Sally", 96, "the funny one about two people taking years"),
    ("The Grand Budapest Hotel", 99, "stylish, funny, and over before anyone is tired"),
    ("Groundhog Day", 101, "funny from the first scene and easy to talk over"),
    ("Before Sunrise", 101, "the first of the two, and the one to start with"),
    ("Hunt for the Wilderpeople", 101, "daft, warm, and it moves"),
    ("John Wick", 101, "short, clean, and all about the fighting"),
    ("Paddington 2", 103, "warm, funny, and good at any age"),
    ("Singin' in the Rain", 103, "the one that makes people like musicals"),
    ("Home Alone", 103, "daft, and everyone in the room has seen it before"),
    ("True Grit", 110, "funny, and a girl who outtalks everyone"),
    ("The Mitchells vs the Machines", 114, "fast, funny, and a robot apocalypse a family can watch"),
    ("The Incredibles", 115, "works for adults and children in the same room"),
    ("Arrival", 116, "quiet science fiction, for an evening when you would rather think"),
    ("Spider-Man: Into the Spider-Verse", 117, "the animation is worth it on its own"),
    ("The King's Speech", 118, "a true story that gives everyone something to talk about"),
    ("Mad Max: Fury Road", 120, "one long chase, and it never drags"),
    ("Guardians of the Galaxy", 121, "funny first and superhero second"),
    ("Sicario", 121, "cold all the way through, and it does not let you settle"),
    ("Gone Girl", 149, "a marriage thriller that keeps turning on you"),
    ("Prisoners", 153, "a kidnapping and a father who will not stop looking"),
    ("Amelie", 122, "Paris, whimsical, and the film most people mean by a French film"),
    ("Spirited Away", 125, "the one to show someone who says they do not like animation"),
    ("La La Land", 128, "bright, sad at the end, and easy to follow"),
    ("Unforgiven", 130, "the one that turns the western over"),
    ("Knives Out", 130, "a whodunnit everyone can follow, with jokes all the way through"),
    ("It's a Wonderful Life", 130, "the one everyone ends on, and it earns the ending"),
    ("Die Hard", 132, "still the best one, and it is a Christmas film too"),
    ("Parasite", 132, "funny until it is not, and worth the two hours"),
    ("The Sound of Music", 174, "long, which is what a wet Sunday wants"),
    ("Seven Samurai", 207, "three and a half hours, and not one of them is wasted"),
)

PICKS = (
    ("Paddington 2", "film", ("parents", "friends", "partner", ""), True, True,
     "warm, funny, and good at any age"),
    ("Knives Out", "film", ("parents", "friends", ""), False, True,
     "a whodunnit everyone can follow, with jokes all the way through"),
    ("The King's Speech", "film", ("parents", ""), True, True,
     "a true story that gives everyone something to talk about afterwards"),
    ("The Grand Budapest Hotel", "film", ("friends", "partner", ""), False, True,
     "stylish and funny, and under 100 minutes"),
    ("The Best Exotic Marigold Hotel", "film", ("parents",), True, True,
     "gentle comedy about starting again at 60, which parents usually take to"),
    ("When Harry Met Sally", "film", ("partner",), True, True,
     "the funny one: two people taking years to notice each other"),
    ("Groundhog Day", "film", ("friends", ""), True, True,
     "funny from the first scene and easy to talk over"),
    ("Hunt for the Wilderpeople", "film", ("friends", "partner"), False, True,
     "daft, warm and over before anyone gets restless"),
    ("Arrival", "film", ("partner", ""), False, True,
     "quiet science fiction, for an evening when you would rather think"),
    ("Happy Valley", "series", ("parents", ""), True, True,
     "tense British crime, six episodes a series, and it grips from the first ten minutes"),
    ("Ghosts", "series", ("parents", "friends", "partner"), True, True,
     "silly and warm in 25-minute episodes, which is what a mixed room wants"),
    ("The Detectorists", "series", ("parents", "friends"), True, True,
     "gentle and very funny, and nothing in it is upsetting"),
    ("The Bear", "series", ("friends", ""), False, True,
     "short, intense episodes that pull you through a whole series in a weekend"),
    ("The Thursday Murder Club", "book", ("parents", ""), True, True,
     "funny with short chapters, so it is easy to pick up and easy to put down"),
    ("Lessons in Chemistry", "book", ("friends", "partner"), True, True,
     "funny and big-hearted, and everyone in a book group has an opinion on it"),
    ("The Midnight Library", "book", ("", "partner"), True, True,
     "gentle and hopeful, and readable in a few evenings"),
    ("Small Things Like These", "book", ("parents",), True, True,
     "under 120 pages and it stays with you for weeks"),
    ("The Silent Patient", "book", ("friends",), True, True,
     "a twist that lands, which is what a reader who wants to be gripped is after"),
)

PICK_MOODS = ("sad", "crying", "cry", "tears", "tearjerker", "heartbreaking", "weepy", "sob",
              "devastating", "emotional", "moving", "funny", "laugh", "laughing", "laughs",
              "hilarious", "comedy", "comedies", "sitcom", "scary", "scariest", "scares",
              "horror", "frightening", "creepy", "terrifying", "spooky", "halloween",
              "uplifting", "uplifted", "cheerful", "heartwarming", "happy", "hopeful",
              "comforting", "gripping", "unputdownable", "exciting", "addictive", "tense",
              "short", "shortest", "twisty", "romantic", "rom com", "romcom", "lighthearted",
              "cosy", "cozy", "easy watching", "nothing heavy", "switch off", "feelgood",
              "feel good", "thought provoking", "mind bending", "page turner", "true story")

_PICK_AVOID = tuple(word for word in WATCHING + SPORT + CHILD + SCREEN_TIME + NOT_WATCHING
                    + MAKING_UP if word != "boxing")


PICK_OTHER_MEDIUM = ("documentary", "documentaries", "docuseries", "docu series", "podcast",
                     "podcasts", "audiobook", "audiobooks", "true crime", "nature", "stand up",
                     "standup", "anime", "reality tv", "soap")

PICK_SUBJECT = ("about", "to do with", "set in", "based on", "starring")


SHOW_SUBJECTS = {
    "cooking": ("For cooking: *MasterChef: The Professionals* is the one about the cooking itself, "
                "*The Great British Bake Off* for baking and *Saturday Kitchen* for a lazy "
                "morning, all of them long-running and easy to start anywhere."),
    "baking": ("*The Great British Bake Off* is the gentle one everybody watches, *Bake Off: The "
               "Professionals* if you want skill, and *Paul Hollywood* travel shows if it is the "
               "bread you care about."),
    "gardening": ("*Gardeners' World* is the one that tells you what to do this week, *Beechgrove* "
                  "for a colder climate and *Love Your Garden* for the before-and-after. Start "
                  "with Gardeners' World and its monthly jobs."),
    "nature": ("*Planet Earth II* is the best of them, *Blue Planet II* for the sea and "
               "*Springwatch* for British wildlife in real time. The first two look astonishing "
               "on any television."),
    "history": ("*The World at War* is the one people still cite, *Time Team* for digging and "
                "Lucy Worsley's series for the social side. All three are old and none of them "
                "feel dated."),
    "science": ("Brian Cox's *The Planets* is the easy way into space, *Forces of Nature* for "
                "how the world works, and *Chemistry: A Volatile History* if you would rather "
                "have the story of the ideas."),
    "sport": ("*The Last Dance* is the one that grips people who do not follow basketball, "
              "*Sunderland 'Til I Die* for football and *Welcome to Wrexham* if you want to "
              "enjoy one. All three are about the people, not the scores."),
    "true crime": ("*The Jinx* is the one with the ending nobody saw coming, *The Staircase* for "
                   "the long haul, and *Des* for a British one with David Tennant. All three are "
                   "about the case rather than the killings."),
    "quiz": ("*Only Connect* is the cleverest thing on television, *Would I Lie to You?* is the "
             "funniest panel show and *University Challenge* the most tense. Start with Would I "
             "Lie to You? for a group."),
    "property": ("*Grand Designs* for the build, *Location, Location, Location* for the search and "
                 "*The Great Interior Design Challenge* if you want the rooms. Grand Designs is "
                 "the one with the arguments."),
    "travel": ("*Travel Man* for a city in 48 hours, *Race Across the World* for the long way "
               "round and any of Michael Palin's journeys for the old-fashioned version. Travel "
               "Man is the short one."),
    "repair": ("*The Repair Shop* is the warm one about people mending things that matter to "
               "them, *Long Lost Family* for the other kind of mending, and *Salvage Hunters* if "
               "you like the hunt."),
    "documentary": ("*Free Solo* for one man on a cliff, *The Jinx* for a case that turns, and "
                    "*Planet Earth II* for the pictures. None of the three needs any background "
                    "to enjoy."),
}
SHOW_SUBJECT_NAMES = {
    "cook": "cooking", "cooks": "cooking", "cooking": "cooking", "cookery": "cooking",
    "chef": "cooking", "chefs": "cooking", "kitchen": "cooking", "food": "cooking",
    "bake": "baking", "bakes": "baking", "baking": "baking", "bread": "baking",
    "cake": "baking", "cakes": "baking",
    "garden": "gardening", "gardens": "gardening", "gardening": "gardening",
    "gardeners": "gardening", "allotment": "gardening", "allotments": "gardening",
    "nature": "nature", "wildlife": "nature", "animals": "nature", "planet": "nature",
    "history": "history", "historical": "history", "war": "history", "wars": "history",
    "science": "science", "space": "science", "physics": "science", "universe": "science",
    "sport": "sport", "sports": "sport", "football": "sport", "rugby": "sport",
    "cricket": "sport", "tennis": "sport", "boxing": "sport", "racing": "sport",
    "crime": "true crime", "murder": "true crime", "murders": "true crime",
    "detective": "true crime", "police": "true crime",
    "quiz": "quiz", "quizzes": "quiz", "panel": "quiz", "game show": "quiz",
    "property": "property", "properties": "property", "house": "property",
    "houses": "property", "homes": "property", "renovation": "property",
    "travel": "travel", "travels": "travel", "holiday": "travel", "holidays": "travel",
    "repair": "repair", "repairs": "repair", "restoration": "repair", "antiques": "repair",
}
SHOW_MEDIUM_WORDS = ("show", "shows", "series", "programme", "programmes", "telly", "tv",
                     "watch", "watching", "boxset", "box set", "netflix", "iplayer",
                     "documentary", "documentaries", "docuseries", "docu series")
SHOW_DOC_ASK_WORDS = ("what", "which", "any", "good", "best", "something", "recommend",
                      "recommendation", "should i watch", "to watch", "worth watching",
                      "documentary night")

SHOW_SUBJECT_AVOID = (
    "how do i", "how to", "how do you", "cant", "wont", "broken", "repair my", "fix",
    "my tv", "the tv", "signal", "aerial", "remote", "licence", "license", "cancel",
    "subscription", "how much", "cost", "bill", "price", "password", "account",
    "turn on", "switch on", "not working", "no picture", "settings", "channel 4",
    "theatre", "theater", "cinema", "west end", "tickets", "on at",
    "plant", "plants", "sow", "prune", "recipe", "recipes", "sauce", "oven", "roast",
    "in my garden", "my garden", "my lawn", "my allotment", "my house", "my kitchen",
    "my oven", "boil", "bake a", "bake an", "frosting",
    "book", "books", "novel", "novels", "read", "reading", "author", "chapters",
    "film", "films", "movie", "movies", "cinema", "soundtrack",
    "explain", "explaining", "explained", "rules of", "the rules", "how is it played",
    "how do you play", "how does it work", "how it works", "to someone who",
    "someone who only", "never watched", "dont understand", "don't understand",
    "what does it mean",
)


_PLAYING_NOT_WATCHING = re.compile(
    r"\b(?:i'?m|im|i am|we'?re|were|we are)\s+"
    r"(?:playing|training|coaching|refereeing|running|swimming|cycling|rowing|competing|"
    r"sailing|climbing|dancing)\b"
    r"|\bnot watch(?:ing)?\b|\b(?:dont|don't) watch\b")


def _a_programme_is_wanted(understood):
    text = str((understood or {}).get("text") or (understood or {}).get("clean") or "").lower()
    return not _PLAYING_NOT_WATCHING.search(text)


def _show_subject(line):
    words = re.findall(r"[a-z0-9']+", _plain_words(line))
    for word in words:
        if word in SHOW_SUBJECT_NAMES and word not in SHOW_MEDIUM_WORDS:
            return SHOW_SUBJECT_NAMES[word]
    return ""


_SHOW_YES_OR_NO = re.compile(
    r"\b(?:is|are) there (?:a|any|anything)\b|\bany good\b|\banything good\b|"
    r"\bis (?:it|that|this) (?:a )?good\b", re.I)
_SHOW_SUBJECT_LEAD = re.compile(r"^(?:For|On|About) [a-z]+: ", re.I)


def _show_about(memory, reading):
    subject = _show_subject(reading)
    if not subject:
        return None
    pick = SHOW_SUBJECTS.get(subject)
    if not pick:
        return None
    said = reading.get("clean") or reading.get("text") or "" if isinstance(reading, dict) else ""
    if _SHOW_YES_OR_NO.search(str(said)):
        return "Yes - " + _SHOW_SUBJECT_LEAD.sub("", pick)
    return pick


def _pick_kind(line):
    for word in re.findall(r"[a-z0-9']+", _plain_words(line)):
        if word in ("book", "books", "novel", "novels", "read", "reading"):
            return "book"
        if word in ("series", "boxset", "show", "shows", "telly", "episode", "episodes"):
            return "series"
        if word in ("podcast", "podcasts"):
            return "podcast"
        if word in ("film", "films", "movie", "movies", "watch", "watching"):
            return "film"
    return ""


_REFUSED_KIND = re.compile(
    r"\b(?:not|no|dont want|don't want|do not want|rather not|anything but|except|instead of|"
    r"i dont want|im not after|not after|sick of|tired of|bored of|watched all|seen all)\s+"
    r"(?:a|an|any|another|the|more|of|some)?\s*"
    r"(?P<kind>films?|movies?|series|box ?sets?|shows?|telly|episodes?|books?|novels?|"
    r"podcasts?)\b")


def _pick_refused(line):
    found = _REFUSED_KIND.search(" " + _plain_words(line) + " ")
    return _pick_kind(found.group("kind")) if found else ""


def _pick_who(line):
    said = " " + _plain_words(line) + " "
    if any(tell in said for tell in ("parents", " my mum", " my dad", " my mother",
                                     " my father", "in laws", "in law")):
        return "parents"
    if any(tell in said for tell in ("partner", "wife", "husband", "girlfriend",
                                     "boyfriend", "my other half")):
        return "partner"
    if any(tell in said for tell in (" friends", " mate", "mates", "everyone", "the girls",
                                     "the lads")):
        return "friends"
    return ""


def _pick_limit(line, memory=None):
    said = " " + str(line).lower().replace("\u2019", "'") + " " + _plain_words(line) + " "
    if any(tell in said for tell in SUBS_TELLS):
        return "nosubs"
    if any(tell in said for tell in FREE_TELLS):
        return "free"
    turns = memory.get("turns") if isinstance(memory, dict) else None
    mine = _plain_words(line).strip()
    for turn in (turns or [])[-2:]:
        user = str((turn or {}).get("user") or "")
        if _plain_words(user).strip() == mine:
            continue
        said = (" " + user.lower().replace("\u2019", "'") + " " + _plain_words(user) + " ")
        if any(tell in said for tell in SUBS_TELLS):
            return "nosubs"
        if any(tell in said for tell in FREE_TELLS):
            return "free"
    return ""


SUBS_WANT = ("with subtitles", "subtitled", "subtitles", "foreign film", "foreign films",
             "foreign language", "world cinema", "not dubbed")

SUBS_KEY = ("with subtitles", "subtitled", "foreign film", "foreign films", "foreign language",
            "world cinema")


SUBS_TURNED_DOWN = re.compile(
    r"\b(?:not|no|never|dont|doesnt|didnt|isnt|arent|without|hate|hates|hated|cant|cannot|stand|"
    r"tired of|sick of|fed up with)\b(?!\s+mind\b)(?:\s+[\w']+){0,4}\s+"
    r"(?:subtitles?|subtitled|foreign films?|foreign language|world cinema|dubbed|subs)\b")

SUBS_WANT = ("with subtitles", "subtitled", "foreign film", "foreign films", "world cinema",
             "not dubbed", "subtitles please")
SUBS_WANT_IF_WATCHING = ("subtitles", "subtitle", "foreign language")
WATCHES_SOMETHING = re.compile(
    r"\b(?:film|films|movie|movies|watch|watching|watched|series|boxset|box set|cinema|telly|tv|"
    r"screen|show|shows|streaming|netflix|dvd)\b", re.I)


def _wants_subtitles(line):
    words = " " + _plain_words(line) + " "
    if any(tell in words for tell in SUBS_TELLS) or SUBS_TURNED_DOWN.search(words):
        return False
    if any(tell in words for tell in SUBS_WANT):
        return True
    return bool(WATCHES_SOMETHING.search(words)
                and any(tell in words for tell in SUBS_WANT_IF_WATCHING))


def _cinema_of(line):
    words = " " + _plain_words(line) + " "
    for word, said in CINEMA.items():
        at = words.find(" " + word + " ")
        if at < 0:
            continue
        before = words[:at].split()[-2:]
        if any(one in NEGATORS for one in before):
            continue
        return said
    return None


def _rows_from_cinema(country):
    return [(title, "film", (), False, False, reason)
            for title, of, reason in NATIONAL_CINEMA if of == country]


def _pick_rows(kind, who, limit, count=3, country=""):
    if country:
        return _rows_from_cinema(country)[:count]
    rows = [row for row in PICKS if row[1] == kind]
    if kind not in ("film", "series"):
        limit = ""
    if limit == "free":
        free = [row for row in rows if row[3]]
        rows = free or rows
    if limit == "nosubs":
        rows = [row for row in rows if row[4]] or rows
    if who:
        suited = [row for row in rows if who in row[2]]
        rows = suited + [row for row in rows if row not in suited]
    return rows[:count]


def _pick_list(rows):
    said = ["*%s* (%s)" % (row[0], row[5]) for row in rows]
    if len(said) < 2:
        return said[0] if said else ""
    return ", ".join(said[:-1]) + " or " + said[-1]


_PICK_PARENT_VERB = {"film": "watch with a parent", "series": "watch with a parent",
                     "book": "hand to a parent", "podcast": "put on with a parent"}


def _subs_sentence(count, language):
    if count == 1:
        return "It is in %s with subtitles." % language
    if count == 2:
        return "Both are in %s with subtitles." % language
    return "All three are in %s with subtitles." % language


def _pick_reply(kind, who, limit, rows, country="", language=""):
    if kind == "series":
        head = "For a series"
    elif kind == "book":
        head = "For a book"
    elif kind == "podcast":
        head = "For a podcast"
    else:
        head = "For a film"
    if who == "parents":
        head += " with your parents"
    elif who == "partner":
        head += " for the two of you"
    elif who == "friends":
        head += " with friends"
    if country:
        head = "For %s %s film" % ("an" if country[:1].lower() in "aeiou" else "a", country)
    said = head + ": " + _pick_list(rows) + "."
    if country:
        said += " " + _subs_sentence(len(rows), language)
    if limit == "free" and kind in ("film", "series"):
        said += (" All three are free-to-air rather than behind a subscription, and iPlayer and "
                 "ITVX are both free - rights move, so check iPlayer first.")
    elif limit == "nosubs" and kind in ("film", "series"):
        said += (" Nothing there needs subtitles: all of them are in English and none of them is "
                 "harder to follow than a chat show.")
    elif who == "parents":
        said += " All of them are safe to %s, and none needs any explaining." % _PICK_PARENT_VERB[kind]
    elif kind == "book":
        said += " Tell me the last one you enjoyed and I'll match the next."
    else:
        said += " Say the mood and I'll narrow it down."
    return said


PICK_REACT = ("it was", "that was", "we went", "i went", "i watched", "we watched",
              "i saw", "we saw", "ive seen", "i've seen", "i have seen", "i read", "ive read",
              "i've read", "we read", "i finished", "we finished", "i loved", "i enjoyed",
              "loved it", "enjoyed it", "it is on", "its on at")

_LENGTH_AVOID = tuple(word for word in _PICK_AVOID + PICK_REACT + KIND_AVOID
                      if word not in ("hours", "hour", "hrs", "hr", "minutes", "minute",
                                      "mins", "min"))



def _pick_carry(memory, line):
    turns = memory.get("turns") if isinstance(memory, dict) else None
    mine = _plain_words(line).strip()
    for turn in (turns or [])[-2:]:
        user = str((turn or {}).get("user") or "")
        if not user or _plain_words(user).strip() == mine:
            continue
        kind = _pick_kind(user)
        if kind:
            return kind
    return ""


BOOK_AS_VERB = re.compile(
    r"\bbook (?:a|an|the|my|your|our|their|his|her|its|it|us|me|them|some|two|three|four)\b"
    r"|\bto book\b|\bbooked\b|\bbooking\b")


def _pick_stands_down(line):
    words = " " + _plain_words(line) + " "
    if BOOK_AS_VERB.search(words):
        return True
    if any(tell in words for tell in PICK_OTHER_MEDIUM):
        return True
    if any((" " + tell + " ") in words for tell in PICK_SUBJECT):
        return True
    if any((" " + tell + " ") in words for tell in PICK_REACT):
        return True
    return any(tell in words for tell in ("family", "the kids", "kids", "children", "child"))


OTHER_SUBJECT = ("journey", "journeys", "train", "trains", "walk", "walks", "drive", "drives",
                 "flight", "flights", "game", "games", "board game", "board games", "lecture",
                 "lectures", "meeting", "meetings", "shift", "shifts", "page", "pages",
                 "restaurant", "restaurants", "menu", "menus", "music", "spotify", "album",
                 "albums", "playlist", "playlists", "plan", "plans", "planning",
                 "book", "books", "novel", "novels", "podcast", "podcasts")
FILM_SAID = ("film", "films", "movie", "movies", "cinema", "watch", "watches", "watching",
             "watched", "netflix", "screen", "telly", "tv")


def _another_subject(line):
    words = " %s " % _plain_words(line)
    if any((" %s " % word) in words for word in FILM_SAID):
        return False
    return any((" %s " % word) in words for word in OTHER_SUBJECT)


def _pick_line(understood):
    if not isinstance(understood, dict):
        return ""
    said = [understood.get("text") or "", understood.get("clean") or "",
            understood.get("norm_text") or ""]
    return " ".join(part for part in said if part)


def _film_kind(line):
    words = " " + _plain_words(line) + " "
    for kind in FILM_KIND_WORDS:
        found = re.search(r"(?<![a-z0-9])" + kind + r"(?:s|es)?(?![a-z0-9])", words)
        if not found:
            continue
        before = words[:found.start()].split()[-2:]
        if any(one in NEGATORS for one in before):
            continue
        return kind
    return ""


_MINUTES = re.compile(r"(\d{2,3})\s*(?:minutes|minute|mins|min)\b")
_LIMIT_CUE = re.compile(r"(in|of about|of|runs|running|lasts|lasting|for)"
                        r"\s+(?:about\s+|around\s+|roughly\s+|just\s+)?([a-z0-9. ]{1,24})")
_UNDER = re.compile(r"(under|less than|no longer than|shorter than|max|maximum|at most)"
                    r"\s+(?:about\s+|just\s+)?([a-z0-9. ]{1,24})")
STRICT_LIMIT = frozenset(("under", "less than", "shorter than"))
_HOUR_WORDS = {
    "an hour": 60, "one hour": 60, "1 hour": 60, "hour and a half": 90,
    "an hour and a half": 90, "one and a half hours": 90, "1.5 hours": 90,
    "two hours": 120, "2 hours": 120, "two hour": 120, "2 hour": 120,
}
_HOUR_MINUTES = re.compile(r"(\d(?:\.\d)?)\s*(?:hours|hour|hrs|hr)\b")


def _limit_wanted(line):
    words = " " + _plain_words(line) + " "
    found = _UNDER.search(words)
    if found:
        strict = found.group(1) in STRICT_LIMIT
        tail = found.group(2).strip()
    else:
        found = _LIMIT_CUE.search(words)
        if not found:
            return 0, False
        strict = False
        tail = found.group(2).strip()
    number = re.match(r"(\d{2,3})\b", tail)
    if number:
        return int(number.group(1)), strict
    for phrase in sorted(_HOUR_WORDS, key=len, reverse=True):
        if tail.startswith(phrase):
            return _HOUR_WORDS[phrase], strict
    hours = _HOUR_MINUTES.match(tail)
    if hours:
        try:
            return int(round(float(hours.group(1)) * 60)), strict
        except ValueError:
            return 0, False
    return 0, False


def _minutes_wanted(line):
    return _limit_wanted(line)[0]


def _film_under(memory, understood):
    line = _pick_line(understood)
    if _pick_stands_down(line):
        return None
    if _another_subject(line):
        return None
    limit, strict = _limit_wanted(line)
    if not limit:
        return None
    kind = _film_kind(line)
    if kind:
        return _film_kind_reply(memory, understood)
    if _mood_of(line):
        if _pick_kind(line) or _pick_carry(memory, line):
            return None
        return _a_pick_in_any_medium(memory, understood)
    if _names_a_film_genre(line):
        return None
    carried = _kind_carry(memory, line)
    if carried:
        within = _shelf_within(carried, limit, strict)
        if within:
            return within
    rows = [row for row in FILM_RUNTIME
            if (row[1] < limit if strict else row[1] <= limit)]
    if not rows:
        return ("Nothing I know comes in %s %d minutes. The shortest I have is *A Grand Day "
                "Out* at 23 minutes, and *The Snowman* at 27 - say the number again if I have "
                "read it wrong." % ("under" if strict else "at", limit))
    picked = rows[-3:]
    picked.reverse()
    said = ["*%s* (%d minutes)" % (row[0], row[1]) for row in picked]
    if len(said) == 1:
        body = said[0]
    else:
        body = ", ".join(said[:-1]) + " or " + said[-1]
    return ("%s - all %s %d minutes. Say what you feel like and I will pick one."
            % (body, "under" if strict else "up to", limit))


def _shelf_within(kind, limit, strict):
    label, said_as, rows = FILM_KINDS[kind]
    fit = [row for row in rows if (row[1] < limit if strict else row[1] <= limit)]
    if not fit:
        shortest = min(rows, key=lambda row: row[1])
        return ("Nothing on the %s shelf comes in %s %d minutes - the shortest is *%s* at %d. "
                "Say the number again if I have read it wrong, or name another kind."
                % (label, "under" if strict else "at", limit, shortest[0], shortest[1]))
    if len(fit) == len(rows):
        return None
    said = ["*%s* (%d minutes, %s)" % (title, minutes, reason)
            for title, minutes, reason in fit]
    body = said[0] if len(said) == 1 else ", ".join(said[:-1]) + " or " + said[-1]
    return ("%s. %s %s %d minutes, and the other %s on that shelf run%s longer, so say if "
            "you would rather have one of those."
            % (body, said_as[0].upper() + said_as[1:], "under" if strict else "up to", limit,
               "one" if len(rows) - len(fit) == 1 else "two",
               "s" if len(rows) - len(fit) == 1 else ""))


def _kind_carry(memory, line):
    turns = memory.get("turns") if isinstance(memory, dict) else None
    mine = _plain_words(line).strip()
    for turn in (turns or [])[-2:]:
        user = str((turn or {}).get("user") or "")
        if not user or _plain_words(user).strip() == mine:
            continue
        kind = _film_kind(user)
        if kind:
            return kind
    return ""


SHORTEST_WORDS = ("shortest", "quickest", "fastest", "shorter one", "shortest one")


def _shortest_wanted(line):
    if not any(re.search(r"(?<![a-z0-9])" + re.escape(word) + r"(?![a-z0-9])", line)
               for word in SHORTEST_WORDS):
        return False
    return any(re.search(r"(?<![a-z0-9])" + word + r"(?![a-z0-9])", line)
               for word in ("one", "ones", "film", "films", "those", "these", "them", "pick",
                            "of", "which", "what", "three", "any", "any of"))


def _film_kind_reply(memory, understood):
    line = _pick_line(understood)
    if _pick_stands_down(line):
        return None
    if _another_subject(line):
        return None
    words = " " + _plain_words(line) + " "
    kind = _film_kind(line)
    if not kind:
        return None
    if _pick_kind(line) not in ("film", ""):
        return None
    if re.match(r"\s*(?:is|was|are|were|isnt|wasnt)\b", _plain_words(line)) \
            and (" " + kind + " ") in words:
        return None
    if _a_word_is_turned_down(line, _kind_words(kind), KIND_REFUSED_AFTER) \
            or _the_chat_turned_down(_kind_words(kind), memory, KIND_REFUSED_AFTER):
        return None
    label, said_as, rows = FILM_KINDS[kind]
    if _shortest_wanted(words):
        shortest = min(rows, key=lambda row: row[1])
        longer = [row for row in rows if row[0] != shortest[0]]
        said = ("The shortest on that shelf is *%s* at %d minutes, %s"
                % (shortest[0], shortest[1], shortest[2]))
        if longer:
            said += (". *%s* runs %d if you have the time."
                     % (longer[0][0], longer[0][1]))
        return said
    limit, strict = _limit_wanted(line)
    if limit:
        within = _shelf_within(kind, limit, strict)
        if within:
            return within
    said = ["*%s* (%d minutes, %s)" % (title, minutes, reason)
            for title, minutes, reason in rows]
    return ("For %s: %s, or %s. Any of them is a good way in, and I can go shorter or pick one if "
            "you tell me the mood." % (said_as, ", ".join(said[:-1]), said[-1]))


def _pick_plain(memory, understood):
    line = _pick_line(understood)
    if _pick_stands_down(line):
        return None
    if _mood_of(line) is not None:
        return None
    kind = _pick_kind(line) or _pick_carry(memory, line)
    refused = _pick_refused(line)
    if refused and kind == refused:
        carried = _pick_carry(memory, line)
        if carried and carried != refused:
            kind = carried
        elif refused in ("film", "series"):
            kind = "series" if refused == "film" else "film"
        else:
            return None
    if not kind or kind == "podcast":
        return None
    cinema = _cinema_of(line)
    if cinema and kind == "film":
        adjective, country, language = cinema
        rows = _pick_rows("film", "", "", country=country)
        if not rows:
            have = []
            for title, of, reason in NATIONAL_CINEMA:
                if of not in have:
                    have.append(of)
            heard = have[0] + ", " + have[1] + " or " + have[2]
            rest = len(have) - 3
            more = " and %d other countries" % rest if rest > 0 else ""
            return ("I have not got a %s list, and I would rather say so than hand you the wrong "
                    "film. I do have %s%s - tell me a %s film you liked and I will match the next "
                    "one." % (adjective, heard, more, adjective))
        return _pick_reply("film", "", "", rows, country=adjective, language=language)
    if kind == "film" and _wants_subtitles(line):
        picked = NATIONAL_CINEMA[:9:4]
        rows = [(title, "film", (), False, False, "%s: %s" % (of, reason))
                for title, of, reason in picked]
        return ("Subtitled, then: " + _pick_list(rows) + ". Tell me a country and I will give you "
                "three of its films.")
    who = _pick_who(line)
    limit = _pick_limit(line, memory)
    rows = _pick_rows(kind, who, limit)
    if not rows:
        return None
    return _pick_reply(kind, who, limit, rows)


def _pick_limit_reply(memory, understood):
    line = _pick_line(understood)
    if _pick_stands_down(line):
        return None
    limit = _pick_limit(line, memory)
    if not limit:
        return None
    kind = _pick_kind(line)
    if kind == "book":
        return _pick_reply("book", "", "", _pick_rows("book", "", ""))
    if limit == "nosubs":
        rows = _pick_rows("film", "", "nosubs")
        return ("Nothing that needs subtitles, then: " + _pick_list(rows[:3]) + ". All three are "
                "in English, so nobody has to read the screen to follow them.")
    rows = _pick_rows(kind if kind in ("film", "series") else "series", "", "free")
    return ("Then it is iPlayer and ITVX, and both are free. " + _pick_list(rows[:3]) + ". All "
            "three are BBC, so they are on iPlayer, and a film on ITV turns up most weeks too - "
            "check iPlayer rather than trusting a listing, because rights move.")


_AGE_BANDS = (
    (1, 4, "Under five wants picture books and board books, read together: *The Very Hungry "
            "Caterpillar* by Eric Carle, *Dear Zoo* by Rod Campbell, *Each Peach Pear Plum* by "
            "Janet and Allan Ahlberg, or any of the *That's Not My...* books. Read the same three "
            "or four over and over - the repetition is the point at that age - and let them turn "
            "the pages."),
    (5, 7, "Five to seven wants short chapters and a picture every few pages: *The Worst Witch*, "
            "*Mr Gum*, *Dog Man* or *Captain Underpants*."),
    (8, 9, "Eight and nine: *The Boy at the Back of the Class*, *Horrible Histories* or *Percy "
            "Jackson*, and *Dog Man* still works for a reader who wants pictures."),
    (10, 12, "Ten to twelve: *Wonder*, *Artemis Fowl* or *Skulduggery Pleasant*, and anything by "
             "Jacqueline Wilson or David Walliams for a reader who likes a series."),
    (13, 15, "Thirteen to fifteen is when the book has to be theirs: *The Hunger Games*, "
             "*Northern Lights* and *The Book Thief* are the safe three, and *The Hate U Give* "
             "or *Six of Crows* if they want something current."),
    (16, 18, "Sixteen to eighteen: *The Book Thief*, *The Hate U Give* and *Normal People*, or "
             "*Educated* by Tara Westover if they would rather read something true."),
)
_WORD_AGES = {"five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10, "eleven": 11,
              "twelve": 12, "thirteen": 13, "fourteen": 14, "fifteen": 15, "sixteen": 16,
              "seventeen": 17, "eighteen": 18}


def _the_reader_age(line):
    match = re.search(r"\b(\d{1,2})\s*(?:-|\s)?\s*(?:year|years|yr)s?\s*-?\s*old\b", line)
    if match:
        return int(match.group(1))
    match = re.search(r"\b(?:aged|age|who is|who's|is)\s+(\d{1,2})\b", line)
    if match:
        return int(match.group(1))
    for word, age in _WORD_AGES.items():
        if word in line:
            return age
    return 0


def _book_for_the_age(memory, understood):
    reading = understood if isinstance(understood, dict) else {}
    line = str(reading.get("clean") or reading.get("text") or "").lower()
    age = _the_reader_age(line)
    if not age and re.search(r"\bteen(?:ager)?s?\b", line):
        age = 13
    for low, high, lead in _AGE_BANDS:
        if age and low <= age <= high:
            close = (" Take them to a bookshop and let them pick the first one themselves: the "
                     "series they choose is the one they read.")
            return lead + close
    return ("Short chapters and a picture every few pages are what a 5 to 7 year old reading "
            "alone wants: *The Worst Witch*, *Mr Gum*, *Dog Man* or *Captain Underpants*. For 8 "
            "to 9, *The Boy at the Back of the Class*, *Horrible Histories* or *Percy Jackson*. "
            "For 10 to 12, *Wonder*, *Artemis Fowl* or *Skulduggery Pleasant*. For 13 and over, "
            "*The Hunger Games*, *Northern Lights* or *The Book Thief*. Take them to a bookshop "
            "and let them pick the first one themselves; the series they choose is the one they "
            "read.")


_A_SHORT_TIME = re.compile(
    r"\b(?:an?|one|two|three|couple of|few) hours?\b|\bhalf an hour\b")

_AN_HOUR = (
    "For an hour, pick one thing you can finish inside it rather than a plan: a walk round the "
    "block with a podcast, one drawer or one shelf, a chapter, or the phone call you keep putting "
    "off. It ends when the hour does, which is the point. Are you on your own, or is someone with "
    "you?")
_A_DAY = (
    "One thing out of the house and one thing at home usually fills it. Out: a walk somewhere you "
    "have not been, a Saturday market, or a museum or gallery - most are free and good for an hour "
    "or two. Home: something to cook properly, a film, or a jigsaw with the radio on. Rain only "
    "moves the walk to a pool or a cinema. Is it just you, or is someone coming with you?")


def _an_hour_or_a_day(memory, understood):
    reading = understood if isinstance(understood, dict) else {}
    line = str(reading.get("clean") or reading.get("text") or "").lower()
    if _A_SHORT_TIME.search(line):
        return _AN_HOUR
    return _A_DAY
_COMIC_FOR_A_CHILD = (
    "For a child, *Dog Man* by Dav Pilkey is the one that gets read to bits, and *Hilda* by Luke "
    "Pearson is the warmer, stranger alternative. *Naruto* or *One Piece* if they want manga to "
    "live in. A library will lend all of these, and a finished single story is easier to hand "
    "over than a long superhero run.")
_COMIC_FOR_A_TEEN = (
    "*Heartstopper* by Alice Oseman is the warmest place to start: a school story that reads fast "
    "and is kind about being a teenager. *One Piece* if they want a long one to live in, "
    "*Fullmetal Alchemist* if they would rather finish something, and *Persepolis* if they like "
    "real life. A library will lend all of these.")
_TEEN_WORDS = frozenset(("teen", "teens", "teenager", "teenagers", "teenaged", "sixteen",
                         "fifteen", "fourteen", "thirteen", "seventeen", "eighteen"))


_CHILD_OF_THEIRS = frozenset(("son", "daughter", "kid", "child", "boy", "girl", "teen",
                              "teenager", "kids", "children", "boys", "girls", "tween", "tweens",
                              "youngster", "youngsters", "grandchild", "grandchildren", "niece",
                              "nephew", "godson", "goddaughter"))
_LIKING = frozenset(("loves", "love", "likes", "like", "enjoys", "enjoy", "adores", "adores",
                     "reads", "read", "devours", "obsessed", "into"))
_ASKS_FOR_A_PICK_WORDS = frozenset(("recommend", "suggest", "what", "which", "best", "good",
                                    "any", "for", "start", "should", "idea", "ideas", "next"))


def _a_child_who_reads_already(understood):
    words = [str(word).lower() for word in (understood.get("words") or [])]
    if not _CHILD_OF_THEIRS.intersection(words):
        return False
    if "my" not in words and "our" not in words:
        return False
    if not _LIKING.intersection(words):
        return False
    return not _ASKS_FOR_A_PICK_WORDS.intersection(words)


_COMIC_SUITABILITY = (
    "Judge it by the age rating on the back - 8+, 12+ and 16+ - and by what the child already "
    "reads, then read or skim the first few pages yourself for the two things that matter, sex "
    "and violence. *Dog Man* and *Hilda* are safe from about seven, *Heartstopper* and "
    "*Fullmetal Alchemist* from about twelve, and *Watchmen* and *Saga* are the ones to leave "
    "until they are older - *Watchmen* has sexual violence in it. A librarian will tell you what "
    "is in a title in about a minute, and will not mind being asked.")

_SUITABILITY_ASK = re.compile(
    r"\b(?:is|are|was|were|would)\b[^?.!]{0,40}?"
    r"\b(?:ok|okay|suitable|appropriate|fine|alright|all right)\b[^?.!]{0,20}?\bfor\b"
    r"|\b(?:what|which) age\b[^?.!]{0,40}\b(?:suitable|appropriate|ok|okay|right)\b"
    r"|\b(?:too old|too young|right age|age range|age rating)\b"
    r"|\bfor (?:a|an) \d{1,2} ?(?:year|yr)s? ?old\b[^?.!]{0,20}\b(?:ok|okay|suitable)\b")


def _asks_if_a_comic_suits_an_age(understood):
    said = str((understood or {}).get("clean") or (understood or {}).get("text") or "")
    return bool(_SUITABILITY_ASK.search(said.lower()))

_COMIC_FOR_A_GROWN_UP = (
    "*Saga* by Brian K. Vaughan is the usual first pick for an adult: a space story with a family "
    "at its centre and art that carries the plot. *Watchmen* if you want the one that changed "
    "what comics could do, *Persepolis* by Marjane Satrapi for a memoir told this way, and "
    "*Heartstopper* by Alice Oseman for a warm school romance. For manga, *Death Note* or "
    "*One Piece* is where most people start. Begin with a complete story rather than a forty-year "
    "superhero run, and a library will lend all of these.")


_COMIC_MANGA = (
    "*Death Note* (a notebook that kills, and the duel that follows) is the usual first manga: "
    "twelve volumes, a clean ending, and nothing to know beforehand. *One Piece* if they want a "
    "long one to live in, or *Fullmetal Alchemist* if they would rather have something they can "
    "finish. Read right to left, back to front - the pages are printed the Japanese way.")
_COMIC_MARVEL = (
    "*Daredevil: Born Again* by Frank Miller is the one to start with: short, brutal and complete "
    "in itself. *Hawkeye* by Matt Fraction if you want funny, *Ms Marvel* by G. Willow Wilson if "
    "you want a teenager finding her feet. Skip the crossover events - they assume forty years of "
    "reading behind them.")
_COMIC_DC = (
    "*Batman: Year One* by Frank Miller is the cleanest way in: one short story, no homework. "
    "*All-Star Superman* by Grant Morrison if you want the character at his best, *Swamp Thing* "
    "by Alan Moore if you want something strange and grown-up. *Watchmen* is the other DC one "
    "worth the time.")
_COMIC_BEGINNER = (
    "*Bone* by Jeff Smith is the easiest place to start: one long story, funny, and it looks like "
    "a children's book until you are deep in it. *Persepolis* by Marjane Satrapi if you want "
    "something true, *Saga* if you want a space story. A library will have all three, and one "
    "complete story is a better first comic than a run of forty issues.")

_COMIC_MEANING = (
    "A graphic novel is one whole story told in comic panels and published as a single book rather "
    "than a monthly issue - *Persepolis* and *Watchmen* are the classic examples. Manga is "
    "Japanese comics, usually printed right to left, and *Death Note* is an easy first one.")
_COMIC_MEANING_ASK = re.compile(
    r"\bwhat(?:'s| is| are)\s+(?:a|an|the)?\s*"
    r"(?:graphic novels?|mangas?|comic books?|comics?|webtoons?)\s*[?.!]*\s*$"
    r"|\bdifference between\b")
_KIND_WORDS = {"manga": _COMIC_MANGA, "marvel": _COMIC_MARVEL, "dc": _COMIC_DC,
               "batman": _COMIC_DC, "superman": _COMIC_DC}
_BEGINNER_WORDS = frozenset(("beginner", "beginners", "newcomer", "newbie"))
_KIND_ASKS = frozenset(("recommend", "recommendation", "recommendations", "suggest", "what",
                        "which", "good", "best", "read", "reading", "start", "started", "try",
                        "worth", "any", "into", "first", "beginner", "beginners", "next"))


def _the_kind_named(understood):
    said = str((understood or {}).get("clean") or (understood or {}).get("text") or "").lower()
    if _COMIC_MEANING_ASK.search(said):
        return _COMIC_MEANING
    words = [str(word).lower() for word in ((understood or {}).get("words") or [])]
    if not _KIND_ASKS.intersection(words):
        return ""
    for word, card in _KIND_WORDS.items():
        if word in words:
            return card
    if _BEGINNER_WORDS.intersection(words) or "where do i start" in said \
            or "where to start" in said:
        return _COMIC_BEGINNER
    return ""


def _reader_named(words, numbers=()):
    if _TEEN_WORDS.intersection(words):
        return "teen"
    for figure in numbers or ():
        if isinstance(figure, dict) and figure.get("unit") == "years":
            try:
                age = int(figure.get("value"))
            except (TypeError, ValueError):
                continue
            if 13 <= age <= 19:
                return "teen"
            if age <= 12:
                return "child"
    if _CHILD_OF_THEIRS.intersection(words):
        return "child"
    return ""


def _comic_pick(memory, understood):
    if _asks_if_a_comic_suits_an_age(understood):
        return _COMIC_SUITABILITY
    words = [str(word).lower() for word in (understood.get("words") or [])]
    if not _reader_named(words, understood.get("numbers") or ()):
        named = _the_kind_named(understood)
        if named:
            return named
    reader = _reader_named(words, understood.get("numbers") or ())
    if not reader:
        for turn in reversed((memory or {}).get("turns") or []):
            said = str((turn or {}).get("user") or "").lower()
            earlier = [word for word in re.split(r"[^a-z']+", said) if word]
            reader = _reader_named(earlier)
            if reader:
                break
    if reader == "teen":
        return _COMIC_FOR_A_TEEN
    if reader == "child":
        return _COMIC_FOR_A_CHILD
    return _COMIC_FOR_A_GROWN_UP


BOOK_GENRES = ("sci fi", "sci-fi", "scifi", "science fiction", "fantasy", "thriller", "thrillers",
               "crime", "crime fiction", "murder mystery", "mystery", "mysteries", "horror",
               "romance", "romantic", "graphic novel", "graphic novels", "comics", "comic books")
_LIKE_A_GENRE = re.compile(
    r"\b(?:like|similar to|anything like|something like|after)\s+(?:a |an |some |any )?(?:"
    + "|".join(re.escape(word) for word in BOOK_GENRES) + r")\b")


def _a_genre_is_the_taste(understood):
    text = str((understood or {}).get("clean") or (understood or {}).get("text") or "").lower()
    return not _LIKE_A_GENRE.search(text)

_LONGER_ASK = re.compile(
    r"\b(?:a\s+)?longer(?:\s+(?:one|version|story|poem|verse|rhyme))?\b"
    r"|\badd\s+(?:a\s+)?(?:verse|stanza)\b", re.I)
_LONGER_NOT_THIS = ("essay", "essays", "letter", "hair", "lashes", "nails", "battery",
                    "cable", "cables", "warranty", "warranties", "opening hours", "term",
                    "sentence", "sentences", "trousers", "legs", "days", "hours", "holiday",
                    "delay", "wait", "queue", "sleep", "run", "drive", "flight", "shift")
_FIXED_COUNT_FORM = re.compile(r"\b(haiku|limerick)\b", re.I)
_POEM_FORM = re.compile(r"\b(poem|poems|poetry|rhyme|rhymes|verse|verses|rap|song|ode|sonnet|"
                        r"ballad|couplet)\b", re.I)
_VERSE_IN_THE_LAST_TURN = re.compile(
    r"\b(story|stories|tale|tales|poem|poems|poetry|rhyme|rhymes|rap|song|verse|verses|"
    r"limerick|haiku|couplet|ode|sonnet)\b", re.I)


def the_verse_longer(text, memory):
    line = " ".join(str(text or "").lower().split())
    if not _LONGER_ASK.search(line):
        return None
    if any(one in line for one in _LONGER_NOT_THIS):
        return None
    said = ""
    thing = ""
    for turn in reversed([one for one in ((memory or {}).get("turns") or [])
                         if isinstance(one, dict)]):
        said = str(turn.get("bot") or "")
        if said:
            thing = _thing(str(turn.get("user") or ""))
            break
    if not said or "\n" not in said:
        return None
    if said.startswith("Once more"):
        said = said.split("\n", 1)[1] if "\n" in said else said
    lead, rest = (said.split("\n", 1) + [""])[:2] if "\n" in said else ("", said)
    if not lead.rstrip().endswith(":"):
        lead, rest = "", said
    if not _VERSE_IN_THE_LAST_TURN.search(lead or rest.split("\n", 1)[0]):
        return None
    if _FIXED_COUNT_FORM.search(lead):
        return None
    thing = thing or GENERIC_STORY_THING
    pool = VERSE_LONGER if _POEM_FORM.search(lead) else STORY_LONGER
    more = _picked(pool, thing).format(thing=thing)
    return (lead + "\n" + rest + "\n" + more) if lead else (rest + "\n" + more)


_SECOND_VERSE_ABOUT = re.compile(
    r"\b(?:one\s+more|another\s+one|one\s+other|another|one)\s+about\b", re.I)
_THE_SUBJECT_IN_A_LEAD = re.compile(
    r"\b(?:about|of|on|describing|called|named)\s+(.+?)\s*:\s*$", re.I)
_THE_COUNT_AGAIN = re.compile(r"\b(?:one\s+more|another\s+one|one\s+other|another)\b", re.I)
_THE_COUNT_WORDS = (
    r"(?:one\s+more|another\s+one|another|one\s+other|again|once\s+more|more|go\s+on|"
    r"(?:tell|give|do|write|make|say)\s+(?:me\s+)?(?:another|one\s+more|one\s+other))")
_THE_FORM_AFTER_THE_COUNT = (
    r"(?:\s+(?:poem|poems|verse|verses|story|stories|rap|song|rhyme|rhymes|tale|haiku|"
    r"limerick|one))*")
_BARE_COUNT_AGAIN = re.compile(
    r"^(?:(?:ok|okay|yes|yeah|and|so|just|great|nice|lovely|good|perfect)\s+)?"
    + _THE_COUNT_WORDS + _THE_FORM_AFTER_THE_COUNT +
    r"(?:\s+(?:please|then|thanks|thank\s+you))?$")


def _a_second_verse_is_asked_for(text):
    line = " ".join(str(text or "").lower().split())
    if not line:
        return False
    if _BARE_COUNT_AGAIN.match(line):
        return True
    if re.search(r"\b(?:tell me more|more information|what else|explain|meaning|why is|how do i|"
                 r"how to|write|writing|wrote|read|reading|book|books)\b", line):
        return False
    return bool(_SECOND_VERSE_ABOUT.search(line))


_ASK_POLITENESS = re.compile(r"\b(?:please|thanks|thank you|ta|too|as well|also|again|now|then|"
                             r"for me|for us|if you can|quick|quickly)\b", re.I)
_NO_SUBJECT = re.compile(r"^(?:it|its|it's|that|this|them|those|these|him|her|they|one|"
                         r"the same|the other|the first|the last|another)$", re.I)


def _the_subject_from_the_ask(after_the_ask):
    words = [one for one in str(after_the_ask or "").split() if not _ASK_POLITENESS.search(one)]
    subject = " ".join(words).strip(" ,.!?;:")
    if not subject or _NO_SUBJECT.match(subject):
        return ""
    return subject


def _the_second_one_short(lead):
    form = "limerick" if re.search(r"\blimerick\b", lead, re.I) else \
        "haiku" if re.search(r"\bhaiku\b", lead, re.I) else "poem"
    return ("That last one was about nothing in particular - give me one word (the sea, my nan, "
            "the bus) and the next %s will be about that." % form)


def _a_child_story_lead(said):
    found = re.match(r"(A short one for [^:]{1,40}):\s", str(said or ""), re.I)
    return found.group(1) + ":" if found else ""


_FORM_OF_A_WORD = {
    "poem": "poem", "poems": "poem", "poetry": "poem", "verse": "poem", "verses": "poem",
    "ode": "poem", "odes": "poem", "sonnet": "poem", "sonnets": "poem", "ballad": "poem",
    "rhyme": "rhyme", "rhymes": "rhyme", "rap": "rap", "raps": "rap", "song": "song",
    "songs": "song", "lyric": "song", "lyrics": "song",
    "story": "story", "stories": "story", "tale": "story", "tales": "story",
    "limerick": "limerick", "limericks": "limerick", "haiku": "haiku",
}


def _the_form_a_repeat_ask_names(line):
    named = ""
    for word in re.findall(r"[a-z']+", str(line or "")):
        named = _FORM_OF_A_WORD.get(word) or named
    return named


def _the_form_of_the_lead(lead):
    if re.search(r"\bhaiku\b", lead, re.I):
        return "haiku"
    if re.search(r"\blimerick\b", lead, re.I):
        return "limerick"
    if re.search(r"\bstor(?:y|ies)\b|\btale\b", lead, re.I) or re.match(
            r"here is one\b", lead, re.I):
        return "story"
    if re.search(r"\brap\b", lead, re.I):
        return "rap"
    if re.search(r"\bsong\b", lead, re.I):
        return "song"
    if re.search(r"\brhyme\b", lead, re.I):
        return "rhyme"
    if _POEM_FORM.search(lead):
        return "poem"
    return ""


def the_next_verse(text, memory):
    if not _a_second_verse_is_asked_for(text):
        return None
    line = " ".join(str(text or "").lower().split())
    said = ""
    for turn in reversed([one for one in ((memory or {}).get("turns") or [])
                         if isinstance(one, dict)]):
        said = str(turn.get("bot") or "")
        if said:
            break
    if not said:
        return None
    told = " ".join(str(turn.get("bot") or "") for turn in ((memory or {}).get("turns") or [])
                    if isinstance(turn, dict))
    child = _a_child_story_lead(said)
    if child:
        for story in CHILD_STORIES:
            if story[:70] not in told:
                return child + " " + story
        return None
    if "\n" not in said:
        return None
    lead = said.split("\n", 1)[0]
    if not lead.rstrip().endswith(":"):
        return None
    form = _the_form_a_repeat_ask_names(line) or _the_form_of_the_lead(lead)
    if not form:
        return None
    found = _SECOND_VERSE_ABOUT.search(line)
    subject = _the_subject_from_the_ask(line[found.end():] if found else "")
    thing = _thing(line) if subject else ""
    if not subject:
        for one in reversed([str(turn.get("bot") or "")
                             for turn in ((memory or {}).get("turns") or [])
                             if isinstance(turn, dict) and turn.get("bot")]):
            named = _THE_SUBJECT_IN_A_LEAD.search(one.split("\n", 1)[0])
            if not named:
                continue
            subject = _the_subject_from_the_ask(named.group(1)).split(",")[0].strip()
            if subject:
                break
    if not thing and subject:
        thing = _thing("about " + subject)
    if form in ("haiku", "limerick"):
        about_it = _say(form, thing, subject) if subject and thing else None
        if about_it and "\n" in about_it and about_it not in told:
            return about_it
        lines = NO_SUBJECT_VERSE.get(form)
        if lines and lines[0] not in told:
            return "Another %s:\n" % form + "\n".join(lines)
        verse = POEMS.get(thing) if thing else None
        if verse:
            lines = [one.format(thing=thing) for one in verse]
            if lines[0] not in told:
                return ("That is every %s I have about %s - a short poem about it instead:\n"
                        % (form, subject)) + "\n".join(lines)
        return _the_second_one_short(lead)
    if form == "story":
        if not subject or not thing:
            return _the_second_one_short(lead)
        return (STORY_LEADING["story"].format(subject=subject) + "\n" +
                _the_opening_not_said_yet(thing, memory))
    if not (_THE_COUNT_AGAIN.search(line) or _BARE_COUNT_AGAIN.match(line)):
        return None
    if not subject or not thing:
        return _the_second_one_short(lead)
    noun = form
    for verse in (POEMS.get(thing), GENERIC_POEM, GENERIC_POEM_TWO):
        if not verse:
            continue
        lines = [one.format(thing=thing) for one in verse]
        if lines[0] not in told:
            return "Another %s about %s:\n" % (noun, subject) + "\n".join(lines)
    return "Another %s about %s:\n" % (noun, subject) + "\n".join(
        one.format(thing=thing) for one in GENERIC_POEM_TWO)


ENTRIES = [
    entry("make-a-card",
          (tuple(one + " card" for one in CARD_OCCASIONS) +
           ("homemade card", "handmade card", "make a card", "make cards", "make my own card",
            "card for my", "cards for"),
           ("make", "makes", "making", "made", "homemade", "handmade", "craft", "glue", "cut out",
            "design", "how do i make", "how to make")),
          "Fold a sheet of A5 thick paper in half, press the crease under a book, and write inside "
          "before you stick anything on - ink on a finished card is the usual ruin. One bold thing "
          "on the front, a cut shape or a photo or thick pen, and three lines inside naming "
          "something you did together beats a lot of stickers.",
          avoid=("write in", "writing in", "wording", "message", "poem", "verse", "rhyme",
                 "say in", "what do i write", "what should i write", "playing card",
                 "card game", "bank card", "gift card", "sim card", "memory card", "sd card",
                 "business card", "credit card", "debit card", "card payment", "birthday cake",
                 "party bag", "bake", "recipe"),
          bias=1),
    entry("film-family-funny", (("film", "movie"),
                                ("family", "kids", "children", "funny", "comedy") + CHILD
                                + ("teenager", "teenagers", "teen", "teens", "teenage")),
          _family_film, avoid=WATCHING + SPORT + SCREEN_TIME,
          guard=not_asking_what_to_watch_for, bias=1),
    entry("watch-family", (("watch", "watching"),
                           ("family", "kids", "children") + CHILD),
          _family_film, avoid=WATCHING + SPORT + SCREEN_TIME,
          guard=not_asking_what_to_watch_for, bias=1),
    entry("worth-it",
          (tuple(VIEWS), JUDGE_WORDS),
          _worth_it, bias=2,
          ask=VERDICT_ASKS,
          avoid=("tonight", "evening", "for my", "kids", "children", "gift", "present",
                 "ticket", "cinema", "how long", "how much",
                 "what next", "next", "what else", "anything else", "something else", "similar",
                 "like that", "recommend", "recommendation", "recommendations", "suggestions",
                 "now what",
                 "watched all", "seen all", "watched it all", "seen it all", "watched the lot",
                 "binged", "binge watched", "already watched", "already seen", "finished",
                 "got through", "caught up",
                 "if i liked", "if i loved", "i liked", "i loved", "read after", "read next",
                 "what should i read", "recommend something like")),
    entry("worth-it-unnamed", (UNNAMED_ASKS, ("it", "this", "that", "one", "thing")),
          _worth_it_unnamed, bias=1,
          avoid=PICK_ASKS + HABIT_ASKS + ("films", "movies", "books", "shows", "series",
                                          "podcasts", "documentaries", "tonight", "evening",
                                          "for my", "gift", "present", "ticket",
                                          "buy", "buying", "bought", "cost", "price",
                                          "spend", "subscription",
                                          "repair", "repaired", "fix", "fixing", "mend",
                                          "service",
                                          "cinema", "at home", "on tv", "telly")),
    entry("film-tonight", (("film", "movie", "watch", "watching", "netflix"),
                           ("tonight", "evening", "something", "later", "rainy", "sunday",
                            "afternoon", "hangover", "sick day", "day off", "friday",
                            "saturday", "weekend", "night in",
                            "good", "recommend", "recommended", "suggest", "best",
                            "choose", "choosing", "pick", "picking", "decide", "deciding",
                            ) + WANT_ASKS + (
                            "for my mum", "for my mother", "for my dad", "for my father",
                            "for my mum who", "for my dad who", "for my mother who",
                            "for my father who", "for my gran", "for my nan", "for my grandma",
                            "for my grandad", "for my grandpa", "for my parents",
                            "for an older", "for someone who", "for my aunt",
                            "for my uncle")),
          EASY_FILM_LIST,
          avoid=SPORT + CHILD + NOT_WATCHING
          + WATCHING
          + ("it was a", "it was good", "was a good", "went to the cinema", "went to see",
             "saw a film", "i saw", "we saw", "already seen", "have seen",
             "isnt scary", "isn't scary", "not scary", "no scary", "nothing scary",
             "not too scary", "nothing too scary", "isnt sad", "isn't sad", "not sad",
             "nothing sad", "not too sad", "nothing too sad", "no blood", "no gore",
             "not gory", "without the gore", "not too long", "nothing heavy", "isnt funny",
             "isn't funny", "not funny", "nothing funny")
          + ("series", "show", "shows", "on telly", "on tv", "boxset", "box set", "binge",
             "episode", "episodes", "season",
             "netflix", "iplayer", "prime", "disney", "now tv", "nowtv", "streaming",
             "apple tv", "all 4", "channel 4", "paramount"),
          guard=_no_named_mood),
    entry("tv-tonight", (("tv", "telly", "television"),
                         ("on", "tonight", "whats", "what's", "anything", "showing",
                          "listings")),
          ("I can't see tonight's listings, so here is what I would start instead: *Happy Valley* "
           "if you want tense, *The Detectorists* if you want gentle, or *Groundhog Day* if you "
           "want a film you can rely on. Tell me the mood and I'll narrow it."),
          avoid=("licence", "license", "aerial", "signal", "reception", "freeview", "remote",
                 "wrong", "wrong with", "fault", "faulty", "broken", "broke", "gone wrong",
                 "not working", "isnt working", "isn't working", "stopped working",
                 "problem with", "keeps cutting out", "keeps going off", "keeps turning off",
                 "colour", "color", "colours", "picture", "pictures", "flicker", "flickering",
                 "blank", "fuzzy", "gone funny", "patchy", "banding", "pixelated", "retune",
                 "retuning", "tuning",
                 "bracket", "wall mount", "too loud", "sound", "keeps turning",
                 "wall", "walls", "hang", "hanging", "mount", "mounting", "drill", "rawplug",
                 "adverts", "advert", "volume", "much louder", "louder",
                 "turns itself", "turning itself", "wont turn on", "won't turn on", "no picture",
                 "screen", "smart tv", "brand", "buy", "cheapest", "which tv",
                 "turn", "turns", "turning", "switch", "switching", "power", "dead", "broken",
                 "broke", "repair", "fault", "faulty", "working", "channels",
                 "series", "boxset", "box set", "binge", "partner", "episode", "season")),
    entry("listings-at-a-venue",
          (("cinema", "cinemas", "pictures", "theatre", "theater", "matinee", "gig", "gigs",
            "concert", "concerts", "arena", "playhouse", "comedy club", "comedy night",
            "arts centre", "arts center",
            "odeon", "vue", "cineworld", "everyman", "curzon", "picturehouse", "showcase",
            "o2", "apollo", "hippodrome", "village hall", "town hall", "venue", "venues",
            "in town", "round here", "in the area", "locally",
            "near me", "near here", "nearby", "near where i",
            "event", "events"),
           ("whats on", "what's on", "what is on", "anything on", "any on", "whats showing",
            "what's showing", "what is showing", "showing at", "showing",
            "whats playing", "what's playing", "what is playing", "playing at", "listings",
            "anything good", "are on", "is on", "show on", "shows on",
            "any events", "any event", "any shows on", "any show on", "any gig", "any gigs",
            "any concert", "any concerts", "any play", "any film", "any films",
            "on tonight", "on at", "on friday", "on saturday", "on sunday",
            "this weekend", "on this week",
            "on near me", "on near here", "on nearby", "on locally", "on round here")),
          ("I can't see what's on at your local venues from here, sorry. The venue's own site or a "
           "listings app has the times and the tickets, and it is the same page for a film, a play "
           "or a gig. Once you know what is on, tell me the mood or two of the names and I'll say "
           "which to go for."),
          avoid=("refund", "refunds", "money back", "ticket", "tickets", "cancelled",
                 "cancel", "lost", "sell", "selling", "sold", "queer", "wear", "wearing",
                 "wore", "dress", "outfit", "sad", "weird", "alone", "on your own",
                 "on my own", "worth it", "reviews", "review", "spoiler", "spoilers",
                 "nearest", "the nearest",
                 "i have", "we have", "ive got", "i've got", "we've got", "weve got",
                 "im going", "i'm going", "we are going", "we're going", "were going",
                 "going to", "me and", "booked",
                 "went to", "been to", "we saw", "i saw", "watched", "last night i",
                 " tv", "tv ", "on telly", "the telly", "telly", "iplayer", "netflix",
                 "prime video", "disney+", "now tv", "channel", "channels", "freeview",
                 "at work", "for work", "work event", "work do", "office", "my team",
                 "in the office"),
          guard=_a_listings_ask_near_me),
    entry("listings-on-a-channel",
          (("bbc", "bbc one", "bbc1", "bbc two", "bbc2", "bbc four", "itv", "channel 4",
            "channel four", "c4", "channel 5", "channel five", "sky", "dave", "itv2",
            "itvbe", "more 4", "film4", "quest", "radio", "radio 4", "radio 2",
            "local radio", "talksport"),
           ("whats on", "what's on", "what is on", "anything on", "whats showing",
            "what's showing", "whats playing", "what's playing", "on tonight", "tonight",
            "listings", "schedule", "schedules", "showing", "playing")),
          ("I can't see the schedule from here, sorry. The guide on the telly, or the station's "
           "own app, has the times, and the catch-up players - iPlayer, ITVX, Channel 4, BBC "
           "Sounds - keep the same list on the front page. Tell me the mood and I'll name "
           "something worth catching."),
          avoid=("stand for", "stands for", "mean", "means", "licence", "license", "fee",
                 "adverts", "advertising", "remote", "aerial", "signal", "reception",
                 "freeview", "retune", "retuning", "tuning", "channel changer", "tune to",
                 "no signal", "wont", "won't", "broken", "repair")),
    entry("pick-a-streaming-service",
          (("streaming service", "streaming services", "streaming subscription",
            "streaming subscriptions", "streaming", "netflix", "disney", "prime video",
            "now tv", "nowtv", "apple tv", "iplayer", "subscription"),
           ("which", "what", "best", "worth it", "should i get", "should i have",
            "should i pay", "choose", "pick", "worth", "get", "need", "one")),
          ("Take one at a time, a month at a time, and cancel when the series ends: almost every "
           "service sells monthly with no contract, so a year of switching costs far less than a "
           "year of all of them. Two are worth keeping at once at most - one for the family "
           "boxsets and one for what you watch live, football or the soaps. Check the service "
           "you already pay for through the TV or broadband bundle before adding another, "
           "because that is where the cheapest month usually hides."),
          avoid=("good", "anything", "recommend", "watch", "watching", "film", "films", "series",
                 "show", "shows", "boxset", "box set", "episode", "cancel", "cancelling",
                 "expensive", "price", "cost", "cheap", "deal", "free", "licence", "license",
                 "tonight", "movie", "movies", "comedy", "documentary", "sport",
                 "netflix or", "or netflix", "iplayer or", "or iplayer", "prime or", "or prime",
                 "disney or", "or disney", "nowtv or", "or nowtv", "britbox or", "or britbox",
                 "apple tv or", "or apple tv", "paramount or", "or paramount"),
          bias=1),
    entry("streaming-good", (("netflix", "iplayer", "prime", "disney", "now tv", "nowtv",
                              "streaming", "apple tv", "all 4", "channel 4", "paramount"),
                             ("good", "anything", "what", "whats", "what's", "recommend",
                              "suggest", "worth watching", "watch", "tonight", "best",
                              "recommendation", "recommendations", "suggestion",
                              "suggestions", "ideas")),
          ("On any of them: *Knives Out* for a whodunnit everyone enjoys, *Happy Valley* or *The "
           "Bear* for a series you'll finish, *Paddington 2* if children are in the room. Say "
           "which service and the mood and I'll narrow it down."),
          avoid=("cancel", "subscription", "how much", "cost", "price", "password", "account",
                 "log in", "login", "signed out", "not working", "wont load", "won't load",
                 "buffering", "download", "free trial", "worth it", "scam", "charge",
                 "comedy", "comedies", "funny", "sitcom", "laugh", "scary", "horror",
                 "thriller", "romance", "romantic", "documentary") + CHILD),
    entry("watch-tonight", (("watch", "watching"), ("tonight", "evening", "what", "should")),
          ("For tonight: *Groundhog Day* (funny), *Knives Out* (a clever whodunnit) or *Arrival* "
           "(if you want to think). On a series instead, *Happy Valley* is tense and *The "
           "Detectorists* is gentle. All easy picks with no homework needed."),
          avoid=WATCHING + CHILD + SPORT + NOT_WATCHING),
    entry("streaming-comedy", (("netflix", "iplayer", "prime", "disney", "now tv", "nowtv",
                                "streaming", "hayu", "apple tv"),
                               ("comedy", "comedies", "funny", "sitcom", "laugh")),
          ("*Schitt's Creek* is the safe pick: short episodes, funny from the first series. "
           "*Derry Girls* if you want something sharper, or *Paddington 2* if it's a film "
           "tonight rather than a series."),
          avoid=("cancel", "subscription", "how much", "cost", "worth it", "password",
                 "account") + WATCHING),
    entry("film-like", (("film", "movie"), ("like", "liked", "likes", "similar", "loved",
                                           "loves", "enjoyed")),
          _film_like,
          avoid=("gift", "present", "birthday", "christmas", "get my", "buy", "for my dad",
                 "for my mum") + CHILD),
    entry("film-want-scary", (("film", "movie", "series", "watch", "watching"),
                              ("scary", "scariest", "scare", "scares", "horror", "horrifying",
                               "frightening", "creepy", "terrifying", "spooky", "jump scares")),
          ("For a proper scare: *Get Out* is the smart one and not gory, *A Quiet Place* is jumpy "
           "from the first minute, and *Hereditary* is the genuinely unnerving one. For an "
           "old-fashioned ghost story, *The Others*."),
          avoid=("dont want a scary", "dont want scary", "dont want a horror", "dont want horror",
                 "dont want anything scary", "dont want to be scared",
                 "dont want a film that is scary", "do not want a scary", "do not want scary",
                 "dont want a sad one", "dont want anything sad",
                 "not scary", "isnt scary", "isn't scary", "no scary", "nothing scary",
                 "without the scary", "scared of", "hate horror", "dont like horror",
                 "don't like horror", "cant stand horror", "can't stand horror", "no gore",
                 "gory", "blood", "hate scary", "scared easily", "scare easily",
                 "easily scared", "frightened easily", "easily frightened", "get scared",
                 "gets scared", "scare me", "scares me", "not too scary",
                 "nothing too scary") + CHILD,
          ask=("want", "recommend", "suggest", "good", "something", "any", "worth", "fancy",
               "in the mood", "looking for", "tonight", "whats", "what film", "what movie",
               "which", "should i watch", "anything", "be scared", "be frightened",
               "scary", "scariest", "horror", "creepy", "spooky", "terrifying", "frightening",
               "jump scares",
               "halloween", "spooky night", "fright night"),
          guard=_the_scare_is_wanted,
          bias=2),
    entry("film-nothing-scary", (("film", "films", "movie", "movies", "series", "watch",
                                  "watching", "telly", "tv",
                                  "netflix", "something", "anything",
                                  "what should i watch", "should i watch", "should we watch",
                                  "anything to watch", "something to watch"),
                                 ("gory", "scary", "horror", "blood", "scare", "spooky", "creepy",
                                  "frightening", "terrifying", "scared", "haunted")),
          _the_gentle_list,
          bias=2,
          ask=("not", "isnt", "isn't", "no", "without", "nothing", "hate", "dont", "don't",
               "else", "another", "other", "more",
               "cant", "can't", "easily", "gore", "gory", "blood", "scared", "frightened",
               "anything but", "apart from", "except", "other than", "not for me", "avoid",
               "spare me", "too much"),
          guard=_a_film_ask, avoid=CHILD),
    entry("film-dont-want", (("film", "films", "movie", "movies", "watch", "watching",
                              "netflix", "telly", "tv",
                              "cartoon", "cartoons", "documentary", "documentaries",
                              "musical", "musicals", "anime", "sitcom", "thriller"),
                             ("dont want", "do not want", "dont really want", "dont fancy",
                              "dont feel like", "not in the mood for", "bored of",
                              "bored with", "tired of", "sick of", "no more", "anything but",
                              "nothing with", "not into", "dont like",
                              "not for me", "are not for me", "is not for me", "not my thing",
                              "not my kind of film", "not my cup of tea", "not my sort")),
          FILM_MOODS["light"],
          avoid=("sad", "scary", "horror", "gore", "gory", "blood", "heavy", "cry", "funny",
                 "romance", "rom com", "romcom", "series", "boxset", "box set",
                 "them again", "him again", "her again", "me again", "this person", "this guy",
                 "this girl", "the guy", "the girl", "my ex", "ex boyfriend", "ex girlfriend",
                 "break up", "breaking up", "broke up", "dump", "dumped", "tell someone",
                 "let them know", "gently", "let him down", "let her down")
          + CHILD + SPORT + NOT_WATCHING + WATCHING),
    entry("film-space", (("film", "movie"), ("space", "sci-fi", "sci fi", "scifi",
                                             "science fiction")),
          ("*Arrival* is the smartest one, *Apollo 13* the most tense, and *Interstellar* the "
           "biggest. For something lighter, *Galaxy Quest* is a lovely comedy about actors on a "
           "spaceship.")),
    entry("film-mood", (("film", "films", "movie", "movies", "watch", "watching",
                         "something to watch", "give me something", "give me a film",
                         "give me a movie"),
                        _mood_key_words({m: MOODS[m] for m in MOOD_ORDER if m != "scary"},
                                        drop=MOODS["scary"])),
          _mood_pick(FILM_MOODS), bias=1,
          avoid=WATCHING + CHILD + SPORT + SCREEN_TIME + NOT_WATCHING
          + ("gift", "present", "birthday", "christmas", "for my", "for someone",
             "my tv", "telly", "aerial", "remote", "noise", "sound", "picture", "broken",
             "broke", "repair", "fault", "faulty", "not working", "subscription", "cancel",
             "password", "account", "licence", "license", "record", "make a film",
             "make a video", "edit a video", "watch for", "symptoms", "signs of")),
    entry("who-wrote-book",
          (("who", "who's", "whos", "whose", "which author"),
           ("wrote", "write", "writes", "written", "author", "authors", "book", "books",
            "novel", "novels", "play", "plays", "poem", "poems", "story", "stories")),
          _who_wrote, bias=1,
          avoid=("recommend", "suggest", "pick", "read next", "should i read", "to read",
                 "for my", "for a", "for someone", "gift", "present", "never reads",
                 "not a reader", "doesn't read", "doesnt read")),
    entry("author-other-books", (AUTHOR_KEYS, ASKED_WROTE), _who_wrote, bias=1,
          avoid=MAKING_UP),
    entry("book-like", (BOOK_LIKE_THINGS, BOOK_LIKE_ASKS), _book_like, bias=3,
          guard=_a_genre_is_the_taste,
          avoid=("gift", "present", "birthday", "christmas", "get my", "buy", "for my dad",
                 "for my mum", "read to", "reading to", "aloud", "learn to read", "writing",
                 "write a", "book a hotel", "hotel room", "hotels in", "a hotel in", "stay in",
                 "flight", "flights", "tickets",
                 "film", "films", "movie", "movies", "watch", "watching", "series", "tv",
                 "telly", "cinema", "netflix", "episode", "episodes", "box set", "actor",
                 "actors")
          + WATCHING),
    entry("book-recommend", (("book", "books", "read", "reading", "novel"),
                              WANT_ASKS + (
                               "recommend", "suggest", "good", "next", "something", "what should",
                               "what book", "what books", "any books",
                               "book to read", "books to read",
                               "what should", "which should i read", "which book",
                               "novel", "novels",
                               "worth reading", "is it worth reading",
                               "read to", "reading to", "read aloud",
                               "for my mum", "for my mother", "for my dad", "for my father",
                               "for my mum who", "for my dad who", "for my mother who",
                               "for my father who", "for my gran", "for my nan", "for my grandma",
                               "for my grandad", "for my grandpa", "for my parents",
                               "for an older", "for someone who", "for my aunt",
                               "for my uncle",
                               "what about", "how about", "for her", "for him", "for them",
                               "boring", "dull", "slow", "not enjoying", "struggling with",
                               "what to read", "to read next", "read next", "finished")),
          _book_recommend,
          guard=lambda understood: (not the_book_is_a_reservation(understood)
                                    and _no_named_mood(understood)),
          avoid=("gift", "present", "birthday", "christmas", "get my", "buy",
                 "learn to read", "short", "sci-fi",
                 "scifi", "science fiction", "space", "fantasy", "dragons", "magic",
                 "thriller", "crime", "murder", "twist", "romance", "horror", "war",
                 "history", "funny", "comedy",
                 "holiday", "holidays", "beach", "flight", "flights", "plane", "on holiday",
                 "isnt scary", "isn't scary", "not scary", "nothing scary", "not too scary",
                 "nothing too scary", "isnt sad", "isn't sad", "not sad", "nothing sad",
                 "not too sad", "nothing too sad", "not too long", "nothing heavy",
                 "isnt funny", "isn't funny", "not funny", "nothing funny",
                 "label", "labels", "news", "meter", "map", "maps", "instructions", "manual",
                 "recipe", "recipes", "menu", "spreadsheet", "report", "email", "emails",
                 "letter", "sign", "timetable", "bill", "invoice", "forecast", "thermometer",
                 "gauge", "the room", "situation", "contract", "terms and conditions",
                 "small print", "balance", "statement", "essay", "exam paper",
                 "funeral", "funerals", "memorial service", "eulogy", "cremation", "burial",
                 "graveside")),
    entry("book-about-a-subject", (("book", "books", "novel", "read", "reading"),
                                   ("about", "on", "covering", "learn", "learning",
                                    "beginners", "beginner", "guide", "introduction",
                                    "who likes", "who loves", "who enjoys", "who is into",
                                    "a fan of", "likes", "loves", "enjoys", "into",
                                    "interested in", "keen on", "interested", "keen",
                                    "recommend", "recommended", "suggest", "suggestion",
                                    "best", "good", "any", "one")),
          _book_about, bias=3,
          avoid=("gift", "present", "birthday", "christmas", "holiday", "holidays", "beach",
                 "flight", "train", "bus", "commute", "journey", "audio book", "audiobook",
                 "read to", "reading to", "learn to read", "my son", "my daughter",
                 "for a child", "for kids"),
          guard=_not_a_reservation),
    entry("book-thriller", (("book", "novel", "read", "reading"),
                            ("thriller", "twist", "crime", "murder")),
          _book_thriller),
    entry("book-mood", (("book", "books", "novel", "novels", "read", "reading"),
                         _mood_key_words({m: MOODS[m] for m in MOOD_ORDER if m != "funny"},
                                         drop=MOODS["funny"])),
          _mood_pick(BOOK_MOODS), bias=1,
          avoid=("funny", "comedy", "laugh", "hilarious", "gift", "present", "birthday",
                 "christmas", "for my", "for someone", "read to", "reading to",
                 "learn to read", "aloud", "how do i read", "how to read", "writing",
                 "write a", "hotel", "flight", "flights", "appointment", "who wrote", "author",
                 "train", "holiday", "holidays", "beach", "plane", "commute", "journey",
                 "the name of", "name of that", "name of a", "name of the", "name of my",
                 "remember the name", "what was that called", "whats it called",
                 "what's it called", "cant think of the name", "can't think of the name")
          + CHILD),
    entry("show-about-a-subject", (SHOW_MEDIUM_WORDS, tuple(SHOW_SUBJECT_NAMES)),
          _show_about, bias=2, avoid=SHOW_SUBJECT_AVOID, guard=_a_programme_is_wanted),
    entry("a-documentary-pick", (SHOW_DOC_ASK_WORDS,
                                ("documentary", "documentaries", "docuseries", "docu series")),
          SHOW_SUBJECTS["documentary"], bias=2, avoid=SHOW_SUBJECT_AVOID,
          guard=_a_documentary_is_wanted),
    entry("tv-mood", (("series", "show", "shows", "boxset", "box set", "binge", "episode",
                       "episodes", "telly", "on tv"),
                      MOOD_SIGNALS),
          _mood_pick(TV_MOODS), bias=1,
          avoid=SCREEN_TIME + CHILD + SPORT
          + ("netflix", "iplayer", "streaming", "cancel", "subscription", "password",
             "account", "aerial", "remote", "repair", "broken", "not working", "noise",
             "sound", "picture", "licence", "license", "how much", "cost", "worth it",
             "how many episodes", "how long",
             "turn on", "turns on", "turn it on", "wont turn", "will not turn", "not turning",
             "switch on", "switched on", "switching on", "wont switch", "plug", "fuse",
             "signal", "channels", "channel", "standby", "blank", "black screen", "screen",
             "freezing", "frozen", "keeps going off", "turns itself off", "is dead", "died",
             "scares me", "scare me", "scared of", "scared easily", "easily scared",
             "frightened of", "hate horror", "not scary", "nothing scary", "cant stand horror",
             "hate scary", "no horror", "no gore")),
    entry("podcast-mood", (("podcast", "podcasts"),
                           _mood_key_words({m: MOODS[m] for m in MOOD_ORDER
                                            if m != "funny"},
                                           drop=MOODS["funny"])),
          _mood_pick(PODCAST_MOODS), bias=1,
          avoid=("how do i", "how to", "start a", "make a", "record", "edit", "mic",
                 "microphone", "upload", "spotify", "apple", "listen to music") + CHILD),
    entry("a-mood-anywhere", (MOOD_SIGNALS, ANY_MOOD_ASKS), _a_pick_in_any_medium,
          avoid=NOT_A_MOOD_PICK, bias=1),
    entry("a-mood-turned-down", (MOOD_SIGNALS, TURNS_IT_DOWN), _a_pick_of_the_other_mood,
          avoid=TURNED_DOWN_KEEPS_ITS_OWN, bias=1),
    entry("book-holiday", (("read", "reading", "novel", "book for", "books for",
                            "book on the", "books on the", "book to", "book should i",
                            "book recommendation", "book recommendations"),
                           ("holiday", "beach", "flight", "flights", "plane", "easy", "light",
                            "holiday reading", "holiday read", "train", "bus", "coach",
                            "journey", "commute", "tube")),
          ("For a holiday read: *The Thursday Murder Club* (funny, short chapters), *Lessons in "
           "Chemistry* (warm and clever), or *The Midnight Library* (gentle and quick). All three "
           "are easy to pick up and put down."),
          ask=("read", "reading", "reads", "recommend", "recommendation", "recommendations",
               "novel", "fiction", "book", "books", "should i read", "worth reading"),
          avoid=("timetable", "timetables", "schedule", "schedules", "departure board",
                 "departures", "bus times", "train times", "time table", "pattern",
                 "patterns", "map", "maps", "knitting", "crochet", "sewing", "ruler",
                 "tape measure", "spirit level", "meter", "recipe", "chart")),
    entry("book-abandon", (("book", "books", "novel", "novels", "read", "reading",
                            "audiobook", "audiobooks"),
                           ("give up", "gave up", "finish", "finishing", "losing interest",
                            "lost interest", "bored", "boring", "slog", "struggling",
                            "dont like", "don't like", "not enjoying", "not into it",
                            "abandon", "put it down", "halfway", "half way", "started and")),
          ("Give it about 50 pages, or a tenth of the book if it is a long one, and then stop "
           "without guilt if you still do not care: there are more books than evenings. Halfway "
           "through and dreading it is as clear a sign as you get - put it down, and keep it for "
           "a long train journey in case you come back to it. Finishing a book you dislike is not "
           "a virtue, and nobody is marking it."),
          ask=("should i", "is it ok", "is it okay", "do i", "when", "how long", "how many",
               "worth", "or not"),
          bias=1),
    entry("book-not-a-reader", (("book", "read", "reading", "into reading",
                                "get into reading", "back into reading"),
                               ("rarely", "not much", "hardly", "never", "doesn't read",
                                "dont read", "short", "again", "habit", "lapsed",
                                "used to read", "haven't read", "havent read",
                                "stopped reading", "finish a book", "get back into",
                                "back into")),
          ("Start with something short and gripping: *Of Mice and Men* (about 100 pages), *The "
           "Curious Incident of the Dog in the Night-Time*, or any *Reacher* book by Lee Child. "
           "Short chapters and a fast plot matter more than literary prizes when you're out of "
           "the habit."),
          avoid=("eye", "eyes", "eyesight", "surgery", "operation", "glasses", "contact lens",
                 "aloud", "out loud", "to my child", "to my son", "to my daughter", "my kid",
                 "my son", "my daughter", "toddler", "year old", "years old", "school",
                 "podcast", "audiobook", "listen", "film", "series", "after a stroke",
                 "give up", "gave up", "losing interest", "lost interest", "bored", "boring",
                 "halfway", "half way", "finish it", "dont like", "don't like", "not enjoying",
                 "slog", "struggling"),
          bias=1),
    entry("book-funny", (("book", "books", "novel", "read", "reading", "recommend"),
                        ("funny", "comedy", "laugh", "light-hearted", "lighthearted",
                         "cheerful", "feel-good", "feelgood")),
          ("For funny, *The Thursday Murder Club* by Richard Osman is the easy pick: short "
           "chapters, a mystery that keeps moving, and jokes on every page. *Three Men in a Boat* "
           "if you want an old one that still makes people laugh out loud, or *Good Omens* by "
           "Pratchett and Gaiman for something daft and warm."),
          avoid=("kid", "kids", "child", "children", "son", "daughter", "toddler", "teen",
                 "teenager", "year old", "years old", "grandchild", "boy", "girl", "school",
                 "podcast", "podcasts", "listen", "listening", "audiobook", "audiobooks",
                 "film", "films", "movie", "movies", "series", "netflix", "iplayer",
                 "stream", "streaming", "tv",
                 "comic", "comics", "comic book", "comic books", "graphic novel", "graphic novels",
                 "manga",
                 "count as reading", "counts as reading", "count as a book", "count as books",
                 "still reading", "proper reading", "reading practice", "reading practise")),
    entry("book-comics",
          (("comic", "comics", "comic book", "comic books", "graphic novel", "graphic novels",
            "manga", "webtoon",
            "watchmen", "maus", "persepolis", "saga", "one piece", "naruto", "dog man", "hilda",
            "fullmetal alchemist"),
           ("read", "reading", "recommend", "suggest", "what", "which", "good", "best", "start",
            "started", "something", "any", "want", "like", "into", "try", "first", "worth",
            "next", "finished", "beginner", "beginners",
            "kid", "kids", "child", "children", "son", "daughter", "boy", "girl", "teen",
            "teenager", "year old", "years old", "grandchild", "niece", "nephew", "tween",
            "school", "for")),
          _comic_pick,
          bias=2,
          guard=lambda understood: not _a_child_who_reads_already(understood),
          avoid=("only reads", "hates reading", "wont read", "won't read", "reluctant",
                 "refuses", "struggling",
                 "count as reading", "counts as reading", "count as a book", "count as books",
                 "still reading", "proper reading", "reading practice", "reading practise",
                 "film", "films", "movie", "movies", "series", "netflix", "iplayer", "stream",
                 "streaming", "tv",
                 "make a comic", "make comics", "draw a comic", "draw comics", "write a comic",
                 "comic strip", "comic strips", "drawing")),
    entry("book-sci-fi", (("book", "read", "novel"), ("sci-fi", "sci fi", "scifi", "science fiction",
                                                     "space")),
          ("*Project Hail Mary* by Andy Weir is the safest recommendation: funny, fast and full of "
           "problem-solving. *The Left Hand of Darkness* by Ursula K. Le Guin if you want something "
           "deeper."), bias=2),
    entry("book-fantasy", (("book", "read", "novel"), ("fantasy", "magic", "dragons")),
          ("*The Hobbit* is the easiest way in, *Mistborn* by Brandon Sanderson if you want a big "
           "magic system to learn, and *Piranesi* by Susanna Clarke if you'd rather have something "
           "short and strange. All three are fine for adults and teenagers.")),

    entry("tv-line-of-duty", (("line of duty",), ("watch", "series", "next", "like", "liked")),
          ("*Happy Valley* is the closest in quality: British, tense, brilliantly acted, and less "
           "gory than Line of Duty. *Sherwood* and *Bodyguard* are the other two to try next."),
          bias=1),
    entry("tv-series", (("series", "boxset", "binge", "box set", "show", "shows"),
                            ("watch", "next", "recommend", "partner", "couple", "suggest",
                             "suggestion", "good", "any", "what", "binge", "bingeing",
                             "to binge",
                             "rainy weekend", "rainy day", "wet afternoon", "stuck in",
                             "something to watch", "for the weekend", "long weekend",
                             "a night in")),
          ("*Happy Valley* for tense British crime, *The Bear* for short, intense episodes, or "
           "*Detectorists* if you want something gentle and funny. All three are easy to watch "
           "with a partner."),
          avoid=("theatre", "theater", "west end", "gig", "concert", "tickets", "on at",
                 "cinema", "in town")),
    entry("tv-background", (("tv", "series", "watch"), ("background", "relax", "easy", "nothing",
                                                        "tired")),
          ("*The Detectorists*, *Mortimer & Whitehouse: Gone Fishing* or *The Great British Bake "
           "Off*: all warm, low-stakes and easy to follow when you're tired. Nothing in them needs "
           "your full attention.")),

    entry("podcast-history", (("podcast",), ("history", "historical", "true", "stories", "commute")),
          ("*The Rest Is History* is the best all-round history podcast, with two hosts who are "
           "funny as well as accurate. For true stories, *Casefile* for crime and *This American "
           "Life* for real people's lives."), bias=1),
    entry("podcast-crime", (("podcast", "podcasts", "listen", "listening"),
                           ("true crime", "crime", "crimes", "murder", "murders", "serial killer",
                            "serial killers", "killing", "homicide", "unsolved", "casefile",
                            "like serial", "detective", "investigation")),
          PODCAST_CRIME,
          avoid=("book", "books", "novel", "novels", "read", "reading", "film", "films",
                 "movie", "movies", "series", "netflix", "tv", "documentary", "documentaries",
                 "drama", "mystery", "mystery night", "party", "how do i", "how to", "start a",
                 "record", "edit", "mic", "microphone", "upload", "spotify", "apple"),
          bias=3),
    entry("podcast-commute", (("podcast", "podcasts"),
                              ("commute", "car", "drive", "short", "walk", "road trip",
                               "long drive", "journey", "car ride", "car journey", "flight",
                               "plane", "train", "long listen")),
          ("For a commute: *The Rest Is History* (30 to 50 minutes, always interesting), *The "
           "Diary of a CEO* for long interviews, or *Short History Of...* for 40-minute stories. "
           "All work with one earbud in."), bias=3),
    entry("podcast-funny", (("podcast", "podcasts", "listen", "listening"),
                           ("funny", "comedy", "laugh", "light-hearted", "lighthearted")),
          PODCAST_FUNNY,
          avoid=("book", "books", "novel", "novels", "read", "reading", "film", "films",
                 "movie", "movies", "series", "netflix", "tv"),
          bias=2),
    entry("music-focus", (("music", "playlist"), ("focus", "study", "work", "concentrate",
                                                  "background")),
          ("Anything without words works best for focus: lo-fi hip hop, film scores by Hans Zimmer "
           "or Ólafur Arnalds, or ambient Brian Eno. Words compete with reading in a way that "
           "instrumentals don't.")),
    entry("music-recommend", (("music", "album", "band", "artist", "listen", "songs"),
                              ("recommend", "new", "something", "good", "albums", "records",
                               "what", "should i", "suggest", "any", "ideas")),
          ("Give *Rumours* by Fleetwood Mac a go if you've never sat with it, *Blonde* by Frank "
           "Ocean for something slower, or *The Köln Concert* by Keith Jarrett if you want piano "
           "you can work to. Tell me what you already like and I'll narrow it down."),
          avoid=("podcast", "podcasts", "practise", "practice", "learn", "learning", "learnt",
                 "lesson", "lessons", "instrument", "rehearse", "rehearsing", "rehearsal",
                 "chord", "chords", "octave", "octaves", "time signature", "tempo", "bpm",
                 "harmony", "melody", "scale", "scales", "fingering", "what does", "mean",
                 "meaning", "definition", "key of",
                 "wedding", "marrying", "register", "ceremony", "aisle", "first dance",
                 "funeral", "memorial", "christening")),
    entry("listen-when", (("listen", "listening", "music", "playlist", "album", "albums",
                           "podcast", "songs", "song", "hymn", "hymns", "tune", "tunes"),
                          ("drive", "driving", "car", "road trip", "cook", "cooking", "kitchen",
                           "running", "run", "gym", "workout", "jog", "walk",
                           "long drive", "long journey", "long flight", "long trip",
                           "long car ride", "long car journey",
                           "commute", "commuting", "way to work", "walk to work",
                           "journey to work",
                           "dinner party", "party", "barbecue", "bbq", "guests", "guest",
                           "drinks", "wedding", "buffet", "birthday",
                           "first dance", "reception", "bridal",
                           "rainy day", "rainy afternoon", "rainy sunday", "rainy weekend",
                           "rainy morning", "wet afternoon", "wet day", "wet weekend",
                           "snowy day", "stuck indoors",
                           "funeral", "memorial", "cremation", "burial", "wake", "send off",
                           "aisle",
                           "register", "signing of the register", "sign the register",
                           "signing the register", "ceremony")),
          _listen_when,
          avoid=("podcast", "podcasts"), bias=2),
    entry("podcast-any", (("podcast", "podcasts"),
                          WANT_ASKS + ("any", "good", "recommend", "suggest", "like", "liked",
                                       "what", "something", "listen", "new"
                                       "wet day", "wet days", "wet afternoon", "wet weekend",
                                       "snowy day", "stuck indoors")),
          ("Start with *The Rest Is History* (two funny historians), *Desert Island Discs* for "
           "people talking about their lives, or *Casefile* if you want a true crime story told "
           "straight. Tell me what you usually listen to and I'll aim closer."), bias=1,
          avoid=("want to start a podcast", "want to make a podcast", "wanna start a podcast",
                 "thinking of starting a podcast", "thinking about starting a podcast",
                 "should i start a podcast", "start my own podcast", "make my own podcast")),
    entry("podcast-language", (("podcast", "podcasts", "listen", "listening"),
                               ("spanish", "french", "german", "italian", "portuguese", "japanese",
                                "language", "languages", "another language", "learning a language",
                                "learn", "learning", "learn spanish", "learn french",
                                "my spanish", "my french", "my german", "my italian")),
          ("The Coffee Break series - Spanish, French, German, Italian - is the place to start: "
           "15 to 20 minutes a lesson, from hello upwards. Then the Duolingo Spanish Podcast for "
           "real stories told slowly in Spanish with English in between, and *InnerFrench* once "
           "you can follow a two-minute story in French. News in Slow Spanish and News in Slow "
           "French come next, and playing one episode twice beats five played once."),
          avoid=("history", "civil war", "war", "news", "commute", "car", "kids", "children",
                 "crime", "murder", "comedy", "football"),
          bias=2),
    entry("podcast-money", (("podcast", "podcasts"),
                            ("money", "finance", "financial", "business", "economics",
                             "investing", "saving", "boring", "bored")),
          ("*The Money To The Masses Podcast* is the plain-English one, *Meaningful Money* for "
           "pensions and savings, and *Moneybox* for news you can use. All three skip the jargon "
           "and none of them tries to sell you anything."), bias=1),

    entry("board-game-short-rules", (("board game", "game"), ("rules", "easy", "learn", "quick",
                                                              "adults", "simple")),
          ("*Codenames* (2 minutes to learn, works with any group), *Ticket to Ride* (simple, "
           "satisfying trains) and *Sushi Go!* (fast, small, cheap) are the three to start with. "
           "All are done in under an hour."), bias=1,
          avoid=("netball", "basketball", "football", "soccer", "rugby", "cricket", "hockey",
                 "tennis", "badminton", "volleyball", "rounders", "darts", "snooker", "golf",
                 "match", "matches", "sport", "sports", "league", "quarters", "innings",
                 "offside")),
    entry("game-kids", (("game",), ("kids", "children", "rainy", "rain", "raining", "rains",
                                    "family", "bored")),
          ("*Dobble*, *UNO* and *Snakes and Ladders* work for a range of ages, and *Catan Junior* "
           "if they are ready for a proper board game. For a rainy afternoon, a treasure hunt "
           "round the house costs nothing and takes the longest.")),
    entry("game-two-people", (("game", "games", "board game", "board games",
                               "card game", "card games", "cards", "with cards",
                               "something to play", "a game for",
                               "play", "to play"),
                              ("two", "couple", "partner", "2", "two of us", "both of us",
                               "two people", "2 people", "for two", "two players",
                               "two player", "2 players", "2 player", "the two of us",
                               "me and my partner", "with my partner", "me and my wife",
                               "me and my husband", "me and my friend")),
          ("*Patchwork*, *Jaipur* and *Hive* are the three best two-player games that are quick to "
           "learn. For a card game with no kit, gin rummy works just fine.")),
    entry("game-pick", (("board game", "board games", "boardgame", "boardgames",
                         "family game", "family games",
                         "something to play", "anything to play", "a game to play",
                         "games to play", "what to play", "what can we play",
                         "what should we play", "what shall we play"),
                        PICK_ASK + ("what", "which", "best", "should i get", "should we get",
                                    "to play", "to buy", "for christmas", "for a present",
                                    "for a gift", "worth")),
          ("*Codenames* is the safest buy: two teams, one grid of words, five minutes to learn, "
           "and it works from four players up. *Ticket to Ride* if you want a proper board with "
           "a bit of thinking in it, and *Just One* if the table is mixed ages and nobody wants "
           "a rulebook. Tell me how many of you there are and how long you have, and I will pick "
           "one."),
          bias=1,
          avoid=("kids", "children", "child", "toddler", "rainy", "bored",
                 "two", "couple", "partner", "for 2", "2 player", "two player",
                 "group", "friends", "mates", "party", "everyone", "people",
                 "rules", "easy", "learn", "quick", "simple", "adults",
                 "netball", "basketball", "football", "soccer", "rugby", "cricket",
                 "hockey", "tennis", "badminton", "volleyball", "rounders", "darts",
                 "snooker", "golf", "match", "matches", "sport", "sports", "league")),
    entry("game-kids-rainy", (("rainy day", "bored", "all day", "keep busy", "entertain",
                               "afternoon", "busy",
                               "what can i do with", "what do i do with", "what to do with",
                               "things to do with"),
                              ("kids", "children", "afternoon", "toddler", "toddlers",
                               "preschooler", "4 year old", "3 year old", "5 year old",
                               "2 year old", "6 year old", "him", "her", "them")),
          ("A treasure hunt round the house costs nothing and takes longest: ten clues written on "
           "cards, ending in a small prize. For a quieter hour, *Dobble* or a box of felt tips and "
           "a roll of wallpaper."),
          avoid=("game", "games", "board", "phone", "screen", "ipad", "tablet", "tv",
                 "sleep", "sleeps", "sleeping", "slept", "sleepy", "nap", "naps", "napping",
                 "bedtime", "bed time", "night waking", "wakes up", "waking",
                 "drive", "driving", "long drive", "car journey", "long journey", "road trip",
                 "motorway", "in the car", "back seat", "backseat", "plane journey",
                 "long flight", "on a plane", "train journey", "long train", "on the ferry",
                 "train", "on a train", "by train", "ferry", "on a ferry", "by ferry",
                 "flight", "on the plane")),

    entry("party-games-kids", (("party", "birthday"),
                               ("game", "games", "play", "playing", "activities", "activity",
                                "entertain", "entertainment", "fun", "idea", "ideas", "busy",
                                "occupy", "distract", "keep them happy", "keep kids happy")),
          _party_games_for_kids, bias=2,
          guard=lambda reading: not owns_the_deed(reading),
          avoid=("food", "foods", "snack", "snacks", "buffet", "menu", "eat", "eating", "cook",
                 "cooking", "adults", "grown ups", "adult", "teenagers", "teenager", "teens",
                 "teen", "friends", "mates", "everyone", "work party", "office",
                 "cake", "cakes", "bake", "baking", "icing", "frosting", "decorate", "decorating",
                 "candles", "cupcakes", "themed cake", "party bags", "party bag", "favours",
                 "goody bag", "present", "presents", "gift", "gifts",
                 "music", "playlist", "songs", "spotify", "tunes", "album", "dj")),
    entry("audiobook", (("audiobook", "audiobooks", "audio book", "audio books",
                         "listen to a book", "listening to a book", "book on tape"),
                        ("drive", "driving", "car", "commute", "commuting", "journey",
                         "long drive", "flight", "plane", "holiday", "walk", "walking",
                         "what", "which", "any", "good", "best", "recommend", "suggest",
                         "something", "should i", "for a long", "to listen")),
          "For a long drive, a narrator who can hold a voice for hours beats a famous book: "
          "*The Thursday Murder Club* (Lesley Manville, about 7 hours) is easy to follow with "
          "traffic about; *Project Hail Mary* (Ray Porter, about 16 hours) is the one people "
          "finish and start again; *Circe* (Perdita Weeks, about 13 hours) if they want "
          "something with a story to it. Pick something 8 hours or longer for a drive of that "
          "length, and listen to ten minutes of the sample before you commit.",
          avoid=("podcast", "podcasts", "radio", "spotify", "playlist", "music", "song",
                 "songs", "album", "kindle", "library", "borrow", "free", "cheap",
                 "for a child", "for my child", "kids", "children", "bedtime")),

    entry("book-for-a-child", (("book", "books", "novel", "read", "reading", "story",
                                "stories", "chapter book"),
                               ("year old", "year-old", "years old", "yr old",
                                "6 year old", "seven year old", "7 year old",
                                "8 year old", "eight year old", "9 year old",
                                "nine year old", "10 year old", "ten year old",
                                "11 year old", "12 year old", "eleven year old",
                                "twelve year old", "for my son", "for my daughter",
                                "for my grandson", "for my granddaughter", "for my niece",
                                "for my nephew",
                                "13 year old", "thirteen year old", "14 year old",
                                "fourteen year old", "15 year old", "fifteen year old",
                                "16 year old", "sixteen year old", "17 year old",
                                "seventeen year old", "18 year old", "eighteen year old",
                                "for a teenager", "for my teenager", "for a teen",
                                "teenager", "teenagers", "teens", "teen")),
          _book_for_the_age,
          avoid=("for me", "for myself", "my own reading", "bedtime story", "bedtime routine",
                 "read to sleep", "bath", "potty", "toilet training", "school report",
                 "reading age", "struggling", "dyslexia", "reluctant reader",
                 "write a story", "write me a story", "write us a story", "make up a story",
                 "tell me a story", "tell us a story", "write a poem", "write me a poem",
                 "give me a story", "give us a story", "a story about", "stories about",
                 "short story", "story for my")),

    entry("game-group", (("game", "games", "board game", "board games", "play", "playing"),
                         ("friends", "group", "party", "everyone", "mates", "people",
                          "mixed ages",
                          "three", "four", "five", "six", "seven", "eight",
                          "3", "4", "5", "6", "7", "8", "of us", "our lot", "after dinner")),
          ("*Codenames* is the one to bring to a group: two teams, one word grid, and it works "
           "from four players up. *Wavelength* and *Just One* are the same idea for people who "
           "do not like arguing, and for a big party *Werewolf* or *Mafia* needs nothing but a "
           "deck of cards."),
          ask=("what", "which", "any", "best", "good", "suggest", "recommend",
               "game for", "games for", "board game for", "board games for",
               "party game", "party games", "game night", "games night", "for a group",
               "for a party", "for friends", "to play with"),
          avoid=("two", "couple", "partner", "kids", "children")),
    entry("chess-opening",
          (("chess",), ("opening", "openings", "first move", "opening moves", "best first move",
                        "e4", "d4", "start as white", "start as black")),
          "For white, e4 or d4 - both free your pieces and give you a plan - and for black answer "
          "e4 with e5 or the Sicilian, and d4 with d5 or the King's Indian. Learn one opening "
          "each side by its ideas rather than its moves: what the pawns are doing, where the "
          "pieces belong, and which piece you are happy to trade. Ten moves you understand beat "
          "forty you cannot remember.",
          ask=("what", "which", "any", "best", "good", "should", "suggest"),
          avoid=("book", "books", "read", "reading", "course", "set", "board", "computer"),
          bias=1),
    entry("chess-checkmate",
          (("checkmate", "check mate", "in check", "out of check", "being in check",
            "check in chess", "a check in chess", "checks the king", "check the king"),
           ("what", "whats", "mean", "means", "explain", "difference", "different", "vs",
            "versus", "is it", "how do i", "avoid", "get out of", "stuck in", "in check")),
          "Checkmate is a king in check with no legal way out: no square to move to, nothing to "
          "block with, and nothing that can take the piece giving check. Being in check is not "
           "checkmate - you can move the king, block the line or take the attacker, and only if "
           "none of those work is the game over. Stalemate is the other ending, and it is a draw: "
           "the king is not in check but has no legal move, which is why you never chase a lone "
           "king into the corner without giving it a square.",
          ask=("what", "whats", "how", "can", "is", "difference", "explain"),
          avoid=("book", "books", "read", "reading", "opening", "openings", "grandmaster",
                 "tournament", "club", "clock", "board game"),
          bias=1),
    entry("chess-stalemate",
          (("stalemate",),
           ("what", "whats", "mean", "means", "explain", "difference", "different", "vs",
            "versus", "is it", "draw", "how do i")),
          "Stalemate is a draw: the side to move is not in check but has no legal move at all, and "
           "the game ends level even if they are a queen down. It usually happens with a lone king "
           "in front of the enemy king with no square to go to. If you are winning, leave the "
           "other king a square or move a pawn, and if you are losing, look for it on purpose - it "
           "is half a point from nowhere.",
          ask=("what", "whats", "how", "can", "is", "explain"),
          avoid=("book", "books", "read", "reading", "opening", "openings", "talks", "negotiation"),
          bias=1),
    entry("chess-castling",
          (("castle", "castles", "castling", "castled"),
           ("what", "whats", "how", "when", "can i", "do i", "should i", "work", "works",
            "why", "move", "rook", "king", "long", "short", "queenside", "kingside")),
          "Castling moves the king two squares towards a rook and puts that rook on the other side "
           "of it, and it is the one move where two pieces go at once. It takes one move, it is "
           "only legal if neither the king nor that rook has moved, nothing is between them, the "
           "king is not in check, and the king does not pass through or land on a square that is "
           "attacked. Do it early, usually within the first ten moves: it puts the king behind "
           "pawns and brings the rook into the game.",
          ask=("what", "whats", "how", "when", "can", "do", "should", "why", "is"),
          avoid=("sand", "beach", "scotland", "wales", "wedding", "visit", "hotel", "ruins",
                 "book", "books", "read", "reading"),
          guard=_a_chess_line,
          bias=1),
    entry("chess-pawn-moves",
          (("pawn", "pawns", "en passant", "enpassant", "passant"),
           ("move", "moves", "backwards", "backward", "forward", "two squares", "first move",
            "how", "can", "why", "work", "works", "explain", "mean", "means", "promote",
            "promotion", "take", "what", "whats", "what is", "is it", "a pawn")),
          "A pawn moves one square forward and takes one square diagonally forward, so a pawn never "
           "moves or captures backwards. From its starting square only it may go two squares, and "
           "that is what lets the en passant rule exist: if a pawn goes two squares and lands "
           "beside an enemy pawn, that pawn may take it as if it had moved one, on that move only. "
           "Getting to the far end promotes it to a queen, rook, bishop or knight, and a queen is "
           "almost always right.",
          ask=("what", "whats", "how", "when", "can", "do", "why", "is"),
          avoid=("book", "books", "read", "reading", "mortgage", "loan", "car", "camera",
                 "pawn shop", "pawnbroker", "pawnbrokers", "uncle"),
          bias=1),
    entry("chess-improve", (("chess",),
                            ("better", "improve", "learn", "start", "tips", "practise", "practice",
                             "beginner", "good at", "get into", "getting into", "begin")),
          ("Two things move the needle: fifteen minutes of tactical puzzles a day on Lichess or "
           "Chess.com, and playing long games rather than blitz, then looking at where you lost. "
           "Learn the ideas behind one opening for white and one for black instead of memorising "
           "moves, and always ask what your opponent's last move was threatening."),
          ask=("how", "what", "any", "tips", "should", "best", "can")),
    entry("learn-guitar", (("guitar",),
                           ("learn", "start", "beginner", "how long", "take", "teach",
                            "learn to play", "hard")),
          ("Ten to fifteen minutes a day beats one long session a week: learn the four chords G, "
           "C, D and Em first, then play songs that use them, since songs keep you going where "
           "scales do not. Most people can strum through a simple song in two or three months "
           "that way; sore fingertips for the first fortnight are normal."),
          ask=("how", "what", "any", "should", "best", "can", "tips"),
          avoid=("buy", "buying", "bought", "price", "cost", "which one", "second hand",
                 "second-hand", "restring", "string", "tune", "amp", "amplifier")),

    entry("music-genre-start", (tuple(GENRE_START), MUSIC_START_ASKS),
          _genre_start, bias=2,
          avoid=("gig", "gigs", "ticket", "tickets", "concert", "present", "birthday",
                 "film", "films", "documentary", "book", "books", "podcast", "playlist",
                 "country walk", "country walks", "country park", "country garden",
                 "country house", "the country", "countryside", "village", "walk in the country",
                 "my house", "our house", "your house", "decorate", "decorating",
                 "decoration", "decorations", "renovate", "renovating", "renovation",
                 "house prices", "house price", "buy a house", "buying a house", "sell my house",
                 "deposit", "house deposit", "mortgage", "remortgage", "save up", "saving up",
                 "savings", "first home", "first house", "first flat", "stamp duty",
                 "buying a flat", "buy a flat", "getting on the ladder", "housing ladder",
                 "selling my house", "moving house", "house plant", "house plants",
                 "housework", "rent", "landlord",
                 "metal band", "metal detector", "metal detecting", "detector", "detecting",
                 "scrap metal", "metal gate", "metal roof",
                 "metal work", "metalwork", "welding", "welder",
                 "folk dance", "folk dancing", "folk tale", "folk tales", "folk story",
                 "folk stories", "folk medicine", "folk remedy", "folk art",
                 "soul food", "soul mate", "soul mates", "gospel truth", "baby blues",
                 "winter blues", "the blues after", "rap sheet", "take the rap", "indie shop",
                 "indie store", "punk kid", "punk kids",
                 "music night", "club night", "promoter", "night out", "nightclub")),
    entry("card-game-rules", (tuple(CARD_GAMES) + ("patience", "pontoon", "twenty one"),
                              CARD_ASKS),
          _card_game, bias=1,
          avoid=("board game", "board games", "kids", "children", "toddler", "party", "drinking",
                 "bet", "betting", "casino", "real money", "wager", "odds",
                 "for money", "gambling", "poker", "winnings")),
    entry("learn-to-draw", (("draw", "drawing", "sketch", "sketching", "sketches", "doodle",
                             "doodling", "pencil drawing", "line drawing"),
                            ("learn", "start", "starting", "beginner", "better", "improve",
                             "practice", "practise", "talent", "tips", "teach", "how do i",
                             "cant", "can't", "cannot", "never learnt", "never learned")
                            ),
          ("Draw what is in front of you, not from memory: a mug, your own hand, the chair "
           "opposite. Ten minutes a day beats a long session at the weekend, one object a day for a "
           "fortnight, and use a soft pencil (2B) on cheap paper so you are not afraid of it. Copy "
           "one drawing you admire every week and do not rub anything out - the wrong line next to "
           "the right one is how you learn to see."),
          avoid=("curtain", "curtains", "bath", "baths", "bathroom", "pension", "money out",
                 "cash", "card", "tie", "match", "game", "lottery", "raffle", "winner",
                 "kids", "kid", "children", "child", "toddler", "my son", "my daughter",
                 "my boy", "my girl", "school", "nursery", "colouring", "coloring",
                 "draw a picture of my", "draw up", "draw out", "draw in")),
    entry("activity-start", (tuple(ACTIVITY_START) + tuple(ACTIVITY_OTHER_NAMES), ACTIVITY_ASKS),
          _activity_start, bias=1,
          avoid=("present", "birthday", "christmas", "gift", "documentary", "film", "programme",
                 "my son", "my daughter", "my kid", "my child", "kids", "children", "school",
                 "recipe", "flour", "yeast", "sourdough", "starter", "oven", "grams", "500g",
                 "bread", "loaf", "dough", "cake", "cakes", "pastry", "biscuit", "roast",
                 "at work", "set up", "start a choir", "start a club", "start a group",
                 "start a class",
                 "button", "buttons", "hem", "hems", "patch", "patches", "darn", "zip", "zips",
                 "seam", "seams", "unpick", "mend", "alteration", "alterations",
                 "a door", "the door", "my door", "a wall", "the wall", "the walls", "my walls",
                 "a room", "the room", "skirting", "ceiling", "radiator", "fence",
                 "nails", "nail", "fingernails", "fingernail", "toenails", "toenail",
                 "manicure", "pedicure", "nail polish", "nail varnish",
                 "the paint", "paint is", "paint on the", "flaking", "flaky", "flake", "peeling",
                 "peels", "bubbling", "blistering", "chipping", "coming off", "coming away",
                 "use", "using", "thread", "threading", "tension",
                 "rose", "roses", "climbing rose", "climber", "clematis", "wisteria", "vine",
                 "ivy", "shrub", "shrubs", "prune", "pruning", "plant", "plants", "garden",
                 "seedling", "seedlings", "cutting", "cuttings", "greenhouse", "allotment",
                 "nails", "nail", "fingernails", "toenails", "manicure", "pedicure",
                 "nail polish", "nail varnish",
                 "fish tank", "fish tanks", "aquarium", "tank", "tanks", "goldfish", "pond",
                 "smell", "smells", "smelling", "smelly", "stinks", "stink", "get rid",
                 "get rid of", "fishy", "tastes", "taste", "cooked", "fillet", "batter",
                 "chips", "monger", "fish market", "freezer", "kitchen smells",
                 "house smells", "after cooking",
                 "clean up", "cleaning up", "cleaned up", "clear up", "clearing up", "tidy up",
                 "tidying up", "washing up", "wash up", "the wash up", "make a mess",
                 "making a mess", "made a mess", "the mess", "a mess", "messy", "covered in",
                 "all over the", "after baking", "after making", "clean the kitchen",
                 "cook fish", "cooks fish", "cooking fish", "cooked fish", "cook a fish",
                 "cook the fish", "cook my fish", "fry fish", "frying fish", "bake fish",
                 "baked fish", "grill fish", "grilled fish", "fish is done", "fish is cooked",
                 "fish for dinner", "fish for tea", "fish pie", "fishcakes", "fish cakes")),
    entry("chess-play", (("chess",),
                         ("how do i play", "how to play", "how do you play", "rules", "how does",
                          "the moves", "set up", "move the pieces", "win")),
          ("The aim is to trap the other king so it cannot move and cannot escape being taken - "
           "that is checkmate, and you do not capture the king. Pawns go forward one square (two on "
           "their first move) and take diagonally; knights jump in an L; bishops go diagonally any "
           "distance; rooks in straight lines; the queen both ways; the king one square. Set up with "
           "a white square at the bottom right and the queen on her own colour, then play ten games "
           "on Lichess against people at your level - the moves stick after a few losses."),
          bias=1,
          avoid=("better", "improve", "good at", "tips", "practise", "practice", "buy",
                 "buying", "set", "club", "kids", "children", "school")),
    entry("instrument-in-tune", (("guitar", "ukulele", "violin", "fiddle", "bass", "cello",
                                  "banjo", "mandolin", "piano", "keyboard"),
                                 TUNE_ASKS),
          _in_tune, bias=1,
          avoid=("car", "engine", "radio", "station", "tv", "television", "freeview", "aerial",
                 "sat nav", "satnav", "channel")),
    entry("instrument-slips", (("guitar", "ukulele", "violin", "fiddle", "bass", "banjo",
                                "mandolin", "cello"),
                               ("wont stay in tune", "won't stay in tune", "wont hold tune",
                                "keeps going out of tune", "goes out of tune", "out of tune all",
                                "slips", "slipping", "wont tune", "will not stay in tune",
                                "doesnt stay in tune", "doesn't stay in tune")),
          ("Nine times in ten it is the strings: new ones stretch for a week, so tune up, bend "
           "every string a little, and tune again - three or four times the first evening. Old "
           "strings go dead and stop holding pitch, so if they are more than a few months old, "
           "change them. If one string pings as it slips it is catching in the nut, and a pencil "
           "lead scribbled in the slot fixes that tonight. Still slipping with new strings is a "
           "worn peg or a tuner screw, which is a shop job."),
          bias=3,
          avoid=("car", "engine", "radio", "station", "tv", "sat nav")),

    entry("guitar-buzz", (("guitar", "bass", "ukulele", "banjo", "mandolin", "violin"),
                          BUZZ_ASKS),
          _buzz, bias=2,
          avoid=("amp", "amplifier", "speaker", "headphones", "phone", "doorbell", "buzzer",
                 "intercom", "bee", "bees", "wasp")),



    entry("who-made-it", (("who", "name", "band"), WHO_MAKERS),
          who_made,
          avoid=("council", "letter", "email", "wrote to", "that", "this", "quote", "fence",
                 "wall", "door", "house", "room", "shed", "whose", "cake", "dinner", "mess")),

    entry("poetry-kids", (("poetry", "poems", "poem", "rhymes", "rhyming", "nursery rhymes"),
                          ("kids", "children", "child", "toddler", "toddlers", "baby", "babies",
                           "good for", "worth it", "benefit", "help them", "teach")),
          ("Yes, and it is the sound that does the work: rhymes teach a child that words are made "
           "of parts, which is the same skill reading needs. Read one aloud and let them finish "
           "the rhymes, keep it to a couple of minutes, and do not ask them to explain it. Silly "
           "wins - a poem they can shout is one they will remember."), bias=1),
    entry("poem-what", (("poem", "poems", "poetry", "verse"), ("what", "is", "explain", "mean",
                                                             "definition", "form", "rule")),
          ("A poem leans on sound as well as meaning: rhythm, rhyme if you want it, and the line "
           "breaks doing some of the work. No rules you have to follow - the two forms with rules "
           "are the haiku (three lines, 5-7-5) and the limerick (five lines, aabba). Ask me for "
           "either and I'll write one."), bias=2,
          avoid=("read", "reading", "recommend", "book", "books", "novel", "novels",
                 "good for", "worth it", "any good", "benefit", "benefits", "should i")),
    entry("haiku-what", (("haiku", "haikus"), ("what", "is", "explain", "mean", "definition",
                                              "form", "rule", "structure")),
          ("A haiku is three lines counted in sounds: five, then seven, then five, usually about "
           "one moment rather than a story:\nRain on the window,\na hundred small taps, all "
           "night,\nand the garden drinks."), bias=2,
          avoid=("read", "reading", "book", "books")),
    entry("limerick-what", (("limerick", "limericks"), ("what", "is", "explain", "mean",
                                                       "definition", "form", "rule",
                                                       "structure")),
          ("A limerick is five lines that rhyme aabba, with the two in the middle short: it is a "
           "joke in verse.\nThere once was a cloud over Crewe\nthat had far too much rain to "
           "do.\nIt rained on the park\nfrom morning till dark,\nand then, just for fun, rained "
           "on you."), bias=2,
          avoid=("read", "reading", "book", "books")),
    entry("haiku-on", (("haiku", "haikus"), ("about", "of", "on", "write", "make", "give", "one",
                                             "want", "need", "help", "me", "a")),
          _haiku, bias=6,
          avoid=GRAVE + OCCASION + CARD + ("what is", "whats a", "what's a", "meaning",
                                           "definition", "define", "explain", "rule", "rules",
                                           "how many")),
    entry("limerick-on", (("limerick", "limericks"), ("about", "of", "on", "write", "make", "give",
                                                      "one", "want", "need", "help", "me", "a")),
          _limerick, bias=6,
          avoid=GRAVE + OCCASION + CARD + ("what is", "whats a", "what's a", "meaning",
                                           "definition", "define", "explain", "rule", "rules",
                                           "how many")),
    entry("rhyme-word", (("rhyme", "rhymes", "rhyming"), ("with", "for", "word", "does")),
          _rhyme, bias=5),
    entry("poem-on", (("poem", "poems", "verse", "sonnet", "ode", "couplet", "rhyme", "rhymes",
                       "rhyming"),
                      ("about", "of", "on", "write", "make", "give", "one", "want", "need",
                       "short", "help", "me", "a")),
          _poem, bias=3,
          avoid=GRAVE + OCCASION + CARD + ("i'm writing", "im writing", "i am writing", "writing my",
                         "my own", "i have to write", "i've got to write", "help me write",
                         "book", "books", "reading", "recommend",
                         "what is", "what are", "whats a", "what's a", "meaning", "definition",
                         "define", "explain", "difference", "how many lines")),
    entry("poem-for-a-card",
          (("poem", "poems", "verse", "rhyme", "rhymes", "rhyming", "sonnet", "ode", "couplet"),
           ("about", "of", "on")),
          _poem, bias=2, ask=("card", "cards"),
          avoid=GRAVE + OCCASION + ("i'm writing", "im writing", "i am writing", "writing my",
                                    "my own", "i have to write", "i've got to write",
                                    "help me write", "book", "books", "reading", "recommend")),
    entry("one-more-like-that", (("one about", "another one", "do one about", "one for",
                                 "something happier", "something brighter", "something calmer",
                                 "one more please", "one more", "one other", "now one about",
                                 "one more about", "another one about", "and one about",
                                 "one other about"),
                                ("about", "can", "do", "another", "please", "mood", "happier",
                                 "more", "one")),
          _another_one, avoid=GRAVE),
    entry("story-on", (("story", "stories", "tale", "tales",
                        "one more about", "another one about", "and one about", "one about"),
                      ("about", "write", "tell", "make", "short", "one", "give", "me", "a",
                       "funny", "own", "good", "any", "some", "please", "have", "get")),
          _story, bias=1,
          avoid=GRAVE + PICK_WORDS + CARD + ("story idea", "idea for a story")),
    entry("rap-on", (("rap", "raps", "rapping"), ("write", "make", "compose", "up", "sing", "one",
                                                "give me", "for me")),
          _rap, bias=1, avoid=GRAVE + PICK_WORDS + OCCASION + CARD + ("name", "names",
                                                         "called")),
    entry("song-on", (("song", "songs", "lyric", "lyrics"), ("write", "make", "compose", "up",
                                                           "sing", "one", "give me", "for me")),
          _song, bias=1, avoid=GRAVE + PICK_WORDS + OCCASION + CARD),
    entry("character-name", (("character name", "character names", "name for my character",
                              "name for a character", "name my character", "name a character",
                              "name my protagonist", "name for my protagonist",
                              "protagonist name"),
                             ("make", "up", "invent", "suggest", "give", "think", "need",
                              "want", "call", "called", "help", "ideas", "names", "name",
                              "story", "book", "novel", "script", "villain", "hero", "heroine")),
          _character_name, bias=1,
          avoid=("biscuit", "cat", "cats", "dog", "dogs", "horse", "hamster", "rabbit", "pet",
                 "band", "stage", "rap", "nickname", "variable", "password", "domain",
                 "username", "wifi", "baby", "boy", "girl", "child", "children", "baby name")),
    entry("nickname", (("nickname", "nicknames", "nick name", "nick names", "rap name",
                        "stage name", "band name", "dj name"),
                      ("make", "up", "invent", "suggest", "give", "think", "me", "a", "for",
                       "need", "want", "call", "called")),
          _nickname, bias=1),
    entry("story-idea", (("story idea", "story ideas", "plot idea", "idea for a story",
                         "short story idea", "idea for my story"),
                        ("give", "need", "want", "help", "any", "what", "some", "me")),
          _story_idea, bias=3),
    entry("quiz-team-name", (("pub quiz", "quiz team", "team name", "quiz name", "quiz", "team"),
                            ("name", "names", "called", "call", "idea"),
                            ("team", "our team")),
          _quiz_name,
          ask=("name our", "name the", "name a", "name an", "name my", "name this",
               "names for", "name for", "naming", "call our", "call the", "call a", "call my",
               "call us", "help us name", "help me name", "help us call", "help me call",
               "what to name", "what should we call", "what should i call", "what should we name",
               "what should i name", "what would you call", "what would you name",
               "come up with a name", "come up with names", "think of a name", "any name",
               "needs a name", "need a name", "name ideas", "idea for a name", "ideas for a name",
               "team name", "team names", "quiz name", "quiz names", "quiz team name",
               "quiz team names", "pub quiz name", "pub quiz team name", "pub quiz team",
               "quiz team", "quiz teams", "funny name", "funny names", "pun name", "punny name"),
          avoid=("baby", "babies", "child", "children", "kid", "kids", "dog", "dogs", "cat",
                 "cats", "kitten", "puppy", "puppies", "business", "company", "shop", "boat",
                 "wifi", "network", "band", "song", "album", "podcast", "cocktail", "pet",
                 "remember", "remembering", "memorise", "memorize", "recall", "forget",
                 "forgetting", "keep forgetting"),
          bias=1),
    entry("band-name", (("band", "bands", "group", "act", "duo", "trio"),
                        ("name", "named", "naming", "call it", "call us", "call my",
                         "call the", "call ourselves", "come up with", "think of")),
          ("Short, sayable and easy to spell is the whole brief: two words, no apostrophes, and "
           "nothing you have to explain down a phone. Say 'we are the ...' out loud and get a "
           "friend to spell it back after hearing it once, then search it and check it is not "
           "another band or a trademark, because a name you cannot print on a poster is not a "
           "name."),
          ask=("should i name", "should we name", "should i call", "should we call",
               "what should i name", "what should i call", "what to name", "what could i name",
               "suggest", "ideas", "idea", "any name", "good name", "nice name", "name for my",
               "name my", "help me name", "help me pick", "recommend", "come up with",
               "think of a name", "how do i name", "rename", "what would you call"),
          avoid=("member", "members", "singer", "drummer", "guitarist", "bassist", "song",
                 "songs", "album", "track", "wifi", "network", "boat", "starter", "podcast",
                 "cat", "dog", "kitten", "puppy", "baby", "business", "company", "band camp",
                 "mean", "means", "meaning", "history", "started", "formed", "origin"),
          bias=1),


    entry("gaming-platform",
          (("console", "consoles", "playstation", "ps5", "ps4", "xbox", "nintendo",
            "nintendo switch", "switch 2", "switch lite", "gaming pc", "steam deck", "handheld"),
           ("better", "worth", "should i get", "should i buy", "or", "vs", "versus", "which",
            "choose", "buy", "getting", "get", "instead", "difference")),
          "A console is cheaper and simpler: it plays everything at good quality for years, no "
          "upgrades, and you can sell it on. A gaming PC costs more up front but gets cheaper "
          "games, higher settings and mods, and doubles as a work machine - so pick the console "
          "for a shared living room and the PC if you already sit at a desk with a monitor.",
          avoid=("broken", "fix", "repair", "not working", "boot", "screen", "overheat",
                 "energy", "supplier", "suppliers", "tariff", "broadband", "bank account",
                 "phone", "insurance", "electricity", "gas", "provider", "mobile",
                 "for my son", "for my daughter", "for a kid", "for kids", "for christmas",
                 "birthday", "present", "gift", "how much is", "price of")),
    entry("read-more-books",
          (("book", "books", "read", "reading", "novel", "novels"),
           ("more", "habit", "regularly", "again", "start", "started", "stopped", "get back",
            "get into", "tips")),
          "Keep the book where you idle - beside the kettle, in your bag, by the bed - and read in "
          "the small gaps instead of waiting for a free evening. Quit a book at about 50 pages if "
          "it has not gripped you: forcing yourself to finish things you dislike is what stops "
          "the habit.",
          ask=("more", "habit", "tips", "want", "wants", "get back", "get into", "again",
               "started", "stopped", "regularly"),
          avoid=("recommend", "recommendation", "suggest", "what should i read", "good book",
                 "book club", "book clubs", "reading group", "book group", "reading club",
                 "for my mum", "for my dad", "for her", "for him", "present", "gift", "read to",
                 "reading to", "bedtime story", "learn to read", "struggling", "dyslexia",
                 "help my", "help him", "help her", "help them", "his reading", "her reading",
                 "their reading", "year old", "son", "daughter", "child", "children", "kid",
                 "kids", "toddler", "pupil", "school", "phonics", "aloud",
                 "book a", "book an", "book my", "booking a", "booked a", "appointment", "table",
                 "hotel", "flight", "flights", "reserve", "in a week")),

    entry("after-named-title",
          (("liked", "loved", "enjoyed", "finished", "just finished", "binged", "got through",
            "what next", "what else", "anything else", "anything similar", "next one",
            "similar to", "like", "anything like", "after", "watch after", "next after"),
           ("what next", "what else", "anything else", "anything similar", "watch", "watching",
            "series", "tv", "telly", "film", "movie", "netflix",
            "season", "episode", "programme", "program",
            "just finished", "just watched", "just binged", "finished watching", "watched all",
            "watched the whole", "binged the whole",
            "anything like", "like this", "like that", "next after", "next one", "next")
           + AFTER_TITLE_WORDS),
          _after_named, ask=AFTER_TITLE_WORDS, bias=1),
    entry("new-hobby",
          (("hobby", "hobbies", "pastime", "something new to do"),
           ("new", "start", "take up", "should i", "what", "which", "ideas", "suggest",
            "learn", "beginner", "any",
            "need", "want", "find",
            "how", "get a", "get into", "looking for", "fancy", "stick", "sticks",
            "stuck with", "keep up", "advice", "recommend")),
          "Pick the one thing you would happily be bad at, and buy the cheapest version: a ten "
          "pound ukulele, a second-hand chess set, a supermarket sketchbook and pencils. Keep it "
          "in the room where you sit, and give it twenty minutes twice a week. The hobby that "
          "sticks is the one with the shortest walk to it, not the one you researched most.",
          avoid=("no money", "broke", "skint", "friend", "friends")),
    entry("weekend-do",
          (("should i do", "can i do", "shall i do", "shall we do", "what do i do", "what to do",
            "anything to do", "something to do", "things to do"),
           ("weekend", "weekends", "this weekend", "next weekend", "at the weekend",
            "on the weekend", "for the weekend", "saturday", "sundays", "sunday", "this saturday",
            "this sunday", "day off", "day off on", "free day", "free saturday", "free sunday",
            "an hour", "half an hour", "an hour to", "an hour or two", "a couple of hours",
            "couple of hours", "two hours", "three hours", "a few hours", "spare hour",
            "free hour")),
          _an_hour_or_a_day,
          ask=("what", "any", "ideas", "suggest", "recommend", "how"),
          avoid=("with it", "with them", "with that", "what should i do there", "there",
                 "toothache", "tooth", "teeth", "pain", "hurts", "hurting", "ache", "aches",
                 "sick", "ill", "unwell", "doctor", "dentist", "hospital", "pharmacy",
                 "cook", "cooking", "eat", "eating", "recipe", "dinner", "lunch", "breakfast",
                 "bbq", "barbecue", "roast", "cabbage",
                 "watch", "watching", "film", "films", "series", "boxset", "box set", "netflix",
                 "read", "reading", "book", "books", "wear", "outfit", "plant", "plants",
                 "garden", "weeds", "mow", "prune", "clean", "cleaning", "tidy", "paint",
                 "decorate", "away", "holiday", "holidays", "trip", "abroad", "kids",
                 "children", "child", "toddler", "baby", "family", "work", "working", "shift",
                 "overtime", "homework", "revision", "study", "exam", "gym", "run", "running",
                 "exercise", "weight", "budget", "money", "afford", "shop", "shopping", "buy",
                 "buying", "book a", "book an", "booking", "leave", "annual leave", "birthday",
                 "present", "gift", "on tv"),
          guard=_no_city_is_named,
          bias=1),
    entry("evening-in",
          (("night in", "evening in", "night at home", "evening at home", "staying in",
            "stay in tonight", "staying in tonight", "cosy night", "cozy night",
            "cosy evening", "cozy evening", "quiet night in", "night indoors"),
           ("ideas", "idea", "what", "any", "something", "suggest", "recommend", "fun",
            "to do", "can do", "can we do", "plan", "anything", "whats", "what's")),
          "Three things, and the cooking is what makes it an evening rather than a sofa: a "
          "supermarket dough ball each to top yourselves, a slow thing in the oven, or a "
          "cocktail that takes two people. Then one film nobody in the house has seen, started "
          "before nine, and a game that is not a screen - cards, a jigsaw, or a quiz you write "
          "for each other.",
          guard=_names_the_evening,
          avoid=("night out", "night away", "night shift", "hotel", "hospital",
                 "stay in bed", "overnight", "in the fridge", "in the oven", "marinade",
                 "kids", "kid", "children", "child", "toddler", "baby", "teen", "teenager",
                 "family", "with my parents", "babysit", "romantic", "proposal",
                 "cook", "cooking", "roast", "bake", "oven", "recipe", "marinade", "dinner",
                 "supper", "eat", "eating", "make for")),
    entry("wet-day",
          (("rain", "raining", "rains", "rainy", "pouring", "drizzle", "drizzling",
            "showers", "storm", "storms", "wet day", "wet days", "wet weekend",
            "wet weekends", "wet afternoon", "wet weather", "wet out", "wet one"),
           ("things to do", "something to do", "what can i do", "what can we do",
            "what shall we do", "what should i do", "what to do", "ideas", "idea", "bored",
            "fill the day", "day off", "is there to do", "there to do", "anything to do")),
          "One thing out of the house and one long thing at home is what saves a wet day. Out: "
          "the swimming pool, the library, a free museum gallery, or a walk in proper "
          "waterproofs, because a wet park is empty. Home: something with a start and an end, a "
          "whole film, a proper cook, a board game, or the job you keep not doing. Decide both "
          "in the morning, or the afternoon goes to the sofa and a phone.",
          guard=_names_the_weather,
          avoid=("kid", "kids", "child", "children", "toddler", "baby", "family", "teen",
                 "school holiday", "half term", "leak", "leaking", "roof", "gutter",
                 "gutters", "damp", "flood", "flooded", "puddle", "washing", "laundry",
                 "dry my", "drying", "put the washing", "line", "umbrella", "coat",
                 "jacket", "boots", "waterproof", "commute", "drive", "driving", "cycle",
                 "cycling", "bike", "motorbike", "bbq", "barbecue", "wedding", "fete",
                 "match", "pitch", "cricket", "tennis", "golf", "picnic", "camping",
                 "tent", "garden", "plants", "sow", "plant out", "hose", "water the",
                 "windscreen", "car", "roof rack", "drain", "drains", "gutter down",
                 "sports day", "walk to work", "school run",
                 "save", "saves", "saving", "savings", "put by", "put away", "set aside",
                 "rainy day fund", "emergency fund", "fund", "invest", "pension", "budget",
                 "afford", "debt", "pay off", "overdraft", "credit card", "interest",
                 "basement", "cellar", "attic", "loft", "wall", "walls", "ceiling",
                 "ceilings", "floor", "floors", "floorboard", "floorboards", "carpet",
                 "soaked", "condensation", "radiator", "pipe", "pipes", "plumbing",
                 "water coming in", "water coming through", "water coming up",
                 "coming through the", "coming in through", "sodden", "wet patch",
                 "damp patch", "mould", "mold", "smell of damp")),
    entry("start-a-book-club",
          (("book club", "book clubs", "reading group", "reading club", "book group",
            "book circle"),
           ("start", "starting", "set up", "setup", "run", "running", "first meeting",
            "how do i", "how to", "choose books", "pick books", "organise", "organize")),
          "Ask four or five people, not a crowd, and fix the next date before the first meeting "
          "ends - a club that meets every six weeks at a set day keeps going, one that waits for "
          "everyone to be free does not. Pick short books to begin with, let whoever chose it "
          "lead for ten minutes, and bring one question rather than a summary: \"who did you "
          "believe?\", \"what would you have done?\". Rotate who chooses, keep food simple, and "
          "let people come having only read half. To join one instead of starting one, ask at "
          "the library and the independent bookshop: both keep a list, and a group of five "
          "usually has room.",
          ask=("start", "starting", "set up", "setup", "run", "running", "first meeting",
               "how do i", "how to", "organise", "organize", "choose books", "pick books"),
          avoid=("recommend", "recommendation", "what should i read", "good book", "for my mum",
                 "for my dad", "present", "gift", "read to", "reading to", "bedtime story",
                 "learn to read", "struggling", "dyslexia", "audiobook", "kindle", "library",
                 "how many books", "how long to read")),
    entry("pick-country", (CINEMA_WORDS, PICK_ASK + ("ones", "one", "more", "another", "other")),
          _pick_plain, bias=1, guard=_a_country_is_a_country,
          avoid=_PICK_AVOID + ("seen", "watched", "liked", "loved")),
    entry("film-kind", (FILM_KIND_WORDS, PICK_MEDIUM + PICK_ASK),
          _film_kind_reply, bias=2,
          avoid=_PICK_AVOID + PICK_REACT + KIND_AVOID
          + ("flight", "flights", "hotel", "hotels", "taxi", "ticket", "tickets",
             "book a", "book my", "book the", "booking", "reserve", "table for",
             "appointment",
             "works do", "work do", "christmas do", "office party", "christmas party",
             "night out", "dont want to go", "don't want to go", "do i have to go",
             "get out of", "make my excuses", "cant come", "can't come")),

    entry("film-length", (PICK_MEDIUM + LIMIT_WORDS, (
                              "minutes", "minute", "mins", "min",
                              "hours", "hour", "hrs", "hr")),
          _film_under, bias=3, avoid=_LENGTH_AVOID),

    entry("pick-plain", (PICK_MEDIUM, PICK_ASK + PICK_WHO + CINEMA_WORDS + SUBS_KEY),
          _pick_plain, bias=1, guard=_a_country_is_a_country,
          avoid=_PICK_AVOID + PICK_MOODS
          + ("gift", "presents", "birthday", "christmas", "buy", "bought", "buying",
             "for my mum", "for my dad", "for her", "for him",
             "tonight", "evening", "night in", "weekend", "saturday", "sunday", "afternoon",
             "later on", "this evening",
             "subscription", "subscriptions", "cancel", "netflix", "prime", "disney", "now tv",
             "apple tv", "streaming", "iplayer", "all 4", "itvx", "channel 4",
             "abroad", "outside the uk", "vpn", "in spain", "in france", "in america",
             "in australia", "in canada", "download", "record", "not working", "wont play",
             "won't play", "wont load", "buffering", "no signal", "aerial", "licence",
             "license", "password", "account", "log in", "login", "cost", "price",
             "how much", "free trial", "scam", "charge",
             "more", "this year", "habit", "every day", "resolution", "get back into",
             "get into", "started", "stopped", "concentration", "focus", "before bed",
             "for you", "good for", "bad for", "healthy", "unhealthy", "screen time",
             "help me", "improve", "worth reading",
             "aloud", "read to", "reading to", "learn to read", "struggling", "dyslexia",
             "phonics", "bedtime story",
             "book a", "book an", "book my", "hotel", "table", "flight",
             "flights", "train", "taxi", "ticket", "tickets", "appointment", "reserve",
             "holiday", "holidays", "beach", "pool", "plane", "journey", "commute",
             "exam", "exams", "revision", "revise", "revising", "study", "studying",
             "remember", "forget", "forgetting", "memorise", "memorize", "concentrate",
             "label", "labels", "news", "meter", "map", "maps", "instructions", "manual",
             "recipe", "recipes", "menu", "spreadsheet", "report", "email", "emails",
             "letter", "sign", "timetable", "bill", "invoice", "forecast", "thermometer",
             "gauge", "contract", "terms and conditions", "small print", "balance", "statement",
             "weight", "diet", "dieting", "calories", "what i eat",
             "repair", "fix", "broken", "fault", "faulty", "broken down")),
    entry("pick-limit", (FREE_TELLS + SUBS_TELLS,
                         ("only", "just", "got", "have", "no", "not", "dont", "doesnt", "cant",
                          "never", "hate", "hates", "without", "like", "want", "watching")),
          _pick_limit_reply, bias=1,
          avoid=("not working", "wont play", "won't play", "wont load", "not loading",
                 "no signal", "aerial", "licence", "license", "log in", "login", "password",
                 "account", "how much", "cost", "price", "abroad", "outside the uk", "vpn",
                 "in spain", "in france", "turn off", "turned off", "turn on", "turned on",
                 "enable", "disable", "size", "colour", "color", "sync", "delay", "tiny",
                 "missing", "gone", "wont turn", "won't turn", "appear", "come back")),
    entry("costume-at-home",
          (("costume", "costumes", "fancy dress", "dress up", "dressing up", "world book day",
            "what can i be", "what shall i be"),
           ("make", "making", "made", "homemade", "home made", "at home", "last minute", "cheap",
            "cheaply", "diy", "ideas", "what can i", "how do i", "out of things", "from things",
            "no time", "quick")),
          ("Make the shape, not the whole outfit: black leggings and a black top read as almost "
           "anything, then one thing does the work - a cardboard box for a robot or a rocket, a "
           "bin bag and a belt for a cape, a paper plate and elastic for a mask, a stripy top and "
           "an eye patch for a pirate. Paint it the night before, not the morning of, and ask the "
           "party's theme first. If it is for world book day, check the school's rules, because "
           "some ban masks and face paint."),
          avoid=("buy", "buying", "bought", "shop", "hire", "hiring", "rent", "price", "cost",
                 "how much", "where can i", "in the wash", "stain", "stains", "too small",
                 "alter", "altering", "hem", "sew", "sewing machine", "photo", "photos")),

]


def _film_list(text):
    def said(memory, understood):
        line = "%s %s" % ((understood.get("clean") or "") if isinstance(understood, dict) else "",
                          (understood.get("norm_text") or "") if isinstance(understood, dict) else "")
        return _films_within(text, line)
    return said


for _e in ENTRIES:
    if isinstance(_e.reply, str) and len(set(re.findall(r"\*([^*]{2,60})\*", _e.reply))
                                        & set(FILM_MINUTES)) >= 2:
        _e.reply = _film_list(_e.reply)
MUSIC_TERMS = {
    "chord": ("A chord is three or more notes played together: C major is C, E and G, all at "
              "once. Major chords sound settled and minor ones sound sad, which is most of why a "
              "song has a mood at all."),
    "key": ("The key is the home note a piece is built around and comes back to: a song in C "
            "keeps landing on C. The notes it uses are that key's scale, and a key change lifts "
            "the whole song."),
    "scale": ("A scale is the ladder of notes a key is made of, up or down: do re mi fa sol la "
              "ti do. A major scale sounds bright and a minor one darker, and both are eight "
              "notes with the first repeated at the top."),
    "octave": ("An octave is the gap between a note and the same note higher or lower, eight "
              "notes up the scale. It sounds like the same note because the frequency exactly "
              "doubles: A is 440 vibrations a second, the A above it 880."),
    "time signature": ("The two numbers at the start of the music. The top one is how many beats "
                       "are in a bar and the bottom one which note gets the beat, so 4/4 is four "
                       "quarter notes to the bar (most pop) and 3/4 is a waltz."),
    "bar": ("A bar is one group of beats, marked off by the bar lines on the page: in 4/4 that "
            "is four beats to a bar, which is why eight bars is the length of most pop verses. A "
            "bar and a measure are the same thing."),
    "beat": ("The beat is the steady pulse you clap or tap along to; the rhythm is the pattern "
             "played on top of it. Four beats to the bar is most pop, three is a waltz, and a "
             "drummer keeps the beat while everyone else plays around it."),
    "tempo": ("Tempo is how fast the music goes, counted in beats per minute: 60 is one a second "
              "and a ballad, 120 is two a second and a dance track. A metronome clicks it for you."),
    "bpm": ("BPM is beats per minute, how fast the music goes: 60 is one a second and a ballad, "
            "120 is two a second and a dance track. A metronome clicks it for you."),
    "pitch": ("Pitch is how high or low a note is, set by how fast the sound vibrates: a short "
              "string or a tight one vibrates faster and sounds higher."),
    "melody": ("The melody is the tune - the line of single notes you could sing on its own. The "
               "harmony is the chords underneath it, and the rhythm is the pattern in time."),
    "harmony": ("Harmony is two or more notes sounding together, usually as the chords under the "
                "melody. It is what makes a bare tune sound full, and what a second singer adds."),
    "rhythm": ("Rhythm is the pattern of the music in time - where the beats fall and which are "
               "strong. A drummer keeps it, and you can clap it without knowing any notes."),
    "pre chorus": ("The pre-chorus is the short section between the verse and the chorus that "
                   "builds towards it: the words change each time, the music lifts, and then the "
                   "chorus lands. It is the ramp rather than the hook."),
    "chorus": ("The chorus is the part that comes round again with the same words - the bit you "
               "can sing back after one listen, and usually the title. The verses in between "
               "change each time and carry the story, and a bridge is the one different section "
               "near the end."),
    "hook": ("The hook is the short phrase that catches you: a chorus line, a riff or a bit of "
             "vocal you find yourself humming. A producer will often make it the first thing you "
             "hear in the song."),
    "riff": ("A riff is a short repeated phrase of notes, usually on guitar or keys, that a song "
             "is built on: the opening of *Smoke on the Water* or *Seven Nation Army*. It is a "
             "hook you can play rather than sing."),
    "sample": ("A sample is a piece of an existing recording lifted into a new track - a drum "
               "break, a vocal line or a chord. Hip hop and dance music are built on them, and "
               "the original artist is usually credited and paid."),
    "progression": ("A chord progression is the order the chords come in, usually a short loop "
                    "that repeats: C, G, A minor, F is the one behind a thousand pop songs. The "
                    "loop is what the melody and the words sit on, and changing one chord changes "
                    "the whole mood."),
    "key signature": ("The key signature is the sharps or flats written at the start of every "
                      "line of music, and they say which key the piece is in: one sharp is G "
                      "major, one flat is F major, none is C major. It saves writing the same "
                      "sharp or flat beside every note."),
    "arpeggio": ("An arpeggio is a chord played one note at a time instead of all together: C, "
                 "E, G, one after another, low to high. It is what fingerpicking is made of and "
                 "what you hear when a piano player rolls through the chords."),
    "tab": ("Tab (tablature) is guitar music written as six lines for the six strings, with a "
            "number on a line meaning that fret on that string: a 3 on the top line is the third "
            "fret of the top string. It is read left to right like a sentence, it skips the "
            "rhythm, and it is how most people learn a song by ear-free copying."),
    "interval": ("An interval is the distance between two notes, counted in the steps of the "
                 "scale: C up to G is a fifth, C up to E a third, and the same note twice an "
                 "octave. Every chord and tune is made of them, so learning their sounds by ear "
                 "is the single most useful bit of theory there is."),
    "clef": ("A clef is the sign at the start of the staff that says which lines are which notes. "
             "Treble clef curls round the second line up, which is G, and is used for the right "
             "hand of a piano, the violin and most singing; bass clef covers the low lines for the "
             "left hand, the cello and the bass."),
    "middle c": ("Middle C is the C nearest the middle of a piano keyboard, the one four white "
                 "keys in from the left of the group of two black keys in the middle. Written in "
                 "treble clef it sits on its own short line just below the staff, and in bass clef "
                 "on a short line just above it, which is why it is the note that joins the two "
                 "hands."),
    "transpose": ("To transpose is to move a whole piece into a different key, keeping the tune "
                  "and the shapes of the chords the same and shifting every note by the same "
                  "amount - usually so a singer can reach it. On a guitar a capo transposes "
                  "without changing anything you play; a keyboard has a transpose button that "
                  "does it for you."),
    "metronome": ("A metronome clicks a steady beat at whatever speed you set, in beats per minute, "
                  "so you can hear whether you are rushing. Practise the hard bar at a speed you "
                  "can play it clean three times running, then nudge it up five at a time - it is "
                  "the cheapest way to get faster, and a phone app does the job."),
    "producer": ("The producer is the person who shapes the recording: the arrangement, the "
                 "sounds, how the parts fit, and the mix at the end. They are not the songwriter "
                 "and not the engineer. In film the word means the person who runs the money and "
                 "the schedule, a different job."),
}
MUSIC_TERMS["transposing"] = MUSIC_TERMS["transpose"]

_MUSIC_ASKS = ("what is", "whats", "what's", "what are", "mean", "meaning", "definition",
               "define", "explain", "difference", "simple terms", "music", "theory",
               "where is", "where's", "how do i use", "how di i use", "how to use")


_MUSIC_WORD_BESIDE = {
    "producer": ("music", "song", "songs", "album", "record", "records", "band", "studio",
                 "track", "single", "beats", "rap", "mix", "mixing"),
}
_MUSIC_ALL = ("music", "song", "songs", "album", "albums", "record", "band", "track")
_MUSIC_GEAR = ("pedal", "pedals", "amp", "amps", "amplifier", "string", "strings", "case",
               "stand", "pick", "picks", "capo", "tuner")

_MUSIC_ELSEWHERE = {
    "pitch": ("sales", "sell", "selling", "sold", "football", "soccer", "rugby", "hockey",
              "tent", "roof", "mortgage", "elevator", "throw", "pitcher", "baseball", "cricket",
              "market", "investor", "investors", "deck", "campaign"),
    "key": ("house", "home", "door", "doors", "car", "cut", "spare", "locked", "lock", "lost",
            "keyboard", "fob", "window", "safe", "padlock", "gate", "bike", "shed", "rental",
            "shift", "ctrl", "alt", "enter", "tab", "caps", "typing", "laptop", "computer",
            "marriage", "success", "happiness", "key to", "key to a", "to a good",
            "relationship", "friendship", "healthy", "losing weight", "weight loss"),
    "harmony": ("home", "family", "relationship", "marriage", "team", "office", "work",
                "neighbours", "neighbors", "kids", "children", "household", "flat", "staff"),
    "scale": ("kettle", "weigh", "weight", "kitchen", "bathroom", "pay", "salary", "wage",
              "tap", "taps", "shower", "showers", "shower head", "showerhead", "boiler",
              "radiator", "radiators", "washing machine", "dishwasher", "toilet", "bath",
              "limescale", "descale", "descaling", "furred", "furring", "chalky", "hard water",
              "white marks", "white stuff", "water",
              "business", "map", "model", "ladder", "fish", "economies", "earthquake",
              "maths", "math", "mathematics", "graph", "axis", "ruler", "drawing", "draw",
              "plan", "measurement", "measure", "richter", "temperature",
              "ph", "ph scale", "ph of", "ph value", "ph level", "acidity", "acid", "alkaline",
              "litmus", "chemistry", "chemical", "beaufort", "wind", "likert", "survey",
              "pain", "rating"),
    "tempo": ("temperature", "fever", "symptom", "symptoms",
              "run", "runs", "running", "ran", "jog", "jogging", "marathon", "5k", "10k",
              "race", "parkrun", "threshold", "interval", "intervals", "splits", "pace",
              "pacing", "mile", "miles", "training", "workout", "gym", "cycling", "swim",
              "swimming", "chess", "move", "moves", "board", "opening", "endgame", "game"),
    "chorus": ("cold", "colds", "chest", "cough", "coughing", "throat", "sore throat",
               "flu", "covid", "symptom", "symptoms", "fever", "blocked", "runny",
               "line", "lines", "chorus girl", "girls", "dancers", "dancer", "choreography",
               "stage", "theatre", "theater", "west end", "broadway", "musical"),
    "progression": ("career", "job", "work", "promotion", "training", "disease", "diseases",
                    "illness", "condition", "symptoms", "cancer", "treatment", "patients"),
    "riff": ("comedy", "comedian", "comedians", "joke", "jokes", "humour", "humor", "rant",
             "stand up", "stand-up", "satire", "parody", "improvise"),
    "bpm": ("watch", "smartwatch", "fitness", "tracker", "heart", "pulse", "resting",
            "exercise", "cardio", "fat burn", "zone", "run", "runs", "running", "jog",
            "jogging", "pace", "marathon", "5k", "10k", "training"),
    "bar": ("pub", "pint", "chocolate", "soap", "gold", "silver", "iron", "exam", "chart",
            "graph", "code", "barcode", "sandwich", "protein", "cereal", "snack", "cafe",
            "restaurant", "drinks", "beer", "wine", "cocktail", "nightclub", "crowbar",
            "tow bar", "handlebar", "sandbar", "bar chart", "bar exam", "bar of"),
    "beat": ("eggs", "egg", "whisk", "police", "cop", "cops", "officer", "officers",
             "patrol", "patrols", "village", "constable", "cheat", "defeat", "beaten", "boxing",
             "record", "records", "opponent", "tennis", "chess", "game", "score", "team",
             "traffic", "heart", "rate", "price", "expectations", "inflation"),
    "hook": ("coats", "coat hook", "curtain", "curtains", "curtain hook", "towels",
             "hangers", "hanger", "boxing", "punches", "punch", "jabbed", "left hook",
             "right hook", "golf", "tennis", "fishing", "fishes", "crane", "hoist",
             "crochet", "knitting", "sewing", "dressing gown", "picture hook", "ceiling",
             "hook up", "wall hook", "lifting", "climbing", "cargo", "scaffold",
             "python", "programming", "plugin", "react hook", "git hook", "hooks in",
             "writing", "essay", "essays", "story", "paragraph", "introduction", "headline",
             "blog", "article", "opening line", "reader"),
    "chord": ("spinal", "vocal", "struck", "touch", "geometry", "circle", "triangle", "arc",
              "angle", "angles", "maths", "math", "radius", "diameter", "theorem"),
    "tab": ("browser", "chrome", "firefox", "safari", "window", "windows", "bar tab",
            "run a tab", "pickup", "truck", "tablet", "tabs open"),
    "interval": ("run", "runs", "running", "jog", "jogging", "cycling", "walking", "training",
                 "workout", "gym", "sprint", "sprints", "5k", "10k", "marathon", "parkrun",
                 "hiit", "rest", "reps", "sets", "blood", "screening", "appointment"),
    "sample": ("soil", "blood", "urine", "swab", "dna", "water", "rock", "seed", "lab",
               "laboratory", "testing", "tested", "statistics", "survey", "data"),
}


_A_MUSIC_WORD = ("music", "musical", "song", "songs", "tune", "tunes", "melody", "chorus",
                 "verse", "band", "guitar", "piano", "drums", "singing", "singer", "album",
                 "track", "rhythm", "bars", "notes", "orchestra", "violin", "lyrics", "gig",
                 "concert", "playlist", "bpm", "beats per minute", "time signature", "octave",
                 "chord", "scale", "harmony", "key of")

_NEEDS_A_MUSIC_WORD = frozenset(("hook", "beat", "riff", "sample", "tab", "interval"))


_POSSESSIVE = ("my", "our", "his", "her", "their", "your", "my mums", "my dads", "our mums",
               "our dads", "his mums", "her mums", "his dads", "her dads")
_A_THING_OF_THEIRS = ("key", "keys", "scale", "scales")

_LOOKING_FOR_THE_THING = ("wheres", "where's", "where", "lost", "find", "seen", "mislaid",
                          "misplaced", "cant", "can't", "missing", "look", "looking")


def _somebodys_own_thing(said, at):
    if not at:
        return False
    before = said[at - 1]
    if before not in _POSSESSIVE and not (at >= 2 and " ".join(said[at - 2:at]) in _POSSESSIVE):
        return False
    if before == "your" or " ".join(said[at - 2:at]).endswith("your"):
        return any(one in said for one in _LOOKING_FOR_THE_THING)
    return True


def _music_elsewhere(understood):
    said = [str(word).lower() for word in (understood.get("words") or ())]
    flat = " ".join(said)
    for word in sorted(MUSIC_TERMS, key=len, reverse=True):
        forms = [at for at, one in enumerate(said) if one == word or one == word + "s"]
        if forms or (" " in word and word in flat):
            elsewhere = [one for one in _A_MUSIC_WORD if one not in (word, word + "s")]
            if word in _A_THING_OF_THEIRS and any(
                    _somebodys_own_thing(said, at) for at in forms) and not any(
                        one in said or one in flat for one in elsewhere):
                return False
            if word in _NEEDS_A_MUSIC_WORD and not any(
                    one in said or one in flat for one in _A_MUSIC_WORD):
                return False
            return not any(one in said or one in flat
                           for one in _MUSIC_ELSEWHERE.get(word, ()))
    return True


def _music_term(memory, understood):
    said = [str(word).lower() for word in (understood.get("words") or ())]
    flat = " ".join(said)
    for word in sorted(MUSIC_TERMS, key=len, reverse=True):
        if word in said or (" " in word and word in flat):
            beside = _MUSIC_WORD_BESIDE.get(word)
            if beside and not any(one in said or one in flat for one in beside):
                continue
            return MUSIC_TERMS[word]
    return ("A chord is three or more notes together, the key is the home note a song keeps "
            "returning to, and an octave is the same note higher or lower. The time signature "
            "says how many beats are in a bar. Ask about one and I'll give you its answer.")


_MUSIC_TERM_KEY = tuple(word for word in MUSIC_TERMS if word not in _MUSIC_WORD_BESIDE)

ENTRIES.append(entry("music-term", (_MUSIC_TERM_KEY + ("music theory",), _MUSIC_ASKS),
                     _music_term,
                     avoid=("podcast", "podcasts", "recommend", "should i listen",
                            "what should i listen", "playlist", "spotify",
                            "practise", "practice", "learn to play", "should i learn",
                            "how do i get better") + _MUSIC_GEAR,
                     ask=_MUSIC_ASKS,
                     guard=_music_elsewhere))

ENTRIES.append(entry("music-producer", (("producer", "producers", "music producer"),
                                        _MUSIC_WORD_BESIDE["producer"] + ("do", "does", "did")),
                     MUSIC_TERMS["producer"],
                     avoid=("film producer", "film", "films", "movie", "movies", "tv",
                            "television", "documentary")))

def _a_bridge_in_music(understood):
    clean = understood.get("clean")
    if not isinstance(clean, str):
        return False
    low = " " + clean.lower() + " "
    return any(" %s " % word in low or low.strip().startswith(word + " ")
               for word in ("song", "songs", "chorus", "verse", "music", "musical", "track",
                            "tune", "album", "band", "bridge of the song", "in the song"))


ENTRIES.append(entry("song-bridge", (("bridge",), ("song", "songs", "chorus", "verse", "music",
                                                  "track", "tune")),
                     "A bridge is the section that comes once, usually after the second chorus, "
                     "and sounds like neither the verse nor the chorus - it is there to stop the "
                     "song repeating itself before the last chorus, and it often changes key or "
                     "drops to a quiet moment first.",
                     guard=_a_bridge_in_music))

_INSTRUMENT_COUNTS = {
    "violin": "A violin has four strings, tuned G, D, A and E from the lowest up.",
    "fiddle": "A fiddle is a violin, so four strings: G, D, A and E from the lowest up.",
    "viola": "A viola has four strings, C, G, D and A - a fifth lower than a violin.",
    "cello": "A cello has four strings, C, G, D and A, an octave below a viola.",
    "double bass": "A double bass has four strings, E, A, D and G, and some have a fifth.",
    "bass": "A bass guitar has four strings, E, A, D and G - the same notes as the bottom four "
            "of a guitar, an octave lower.",
    "guitar": "A guitar has six strings, E, A, D, G, B and E from the thickest up. A 12-string "
              "guitar has twelve, in six pairs.",
    "ukulele": "A ukulele has four strings, G, C, E and A.",
    "banjo": "A five-string banjo has five, with the short fifth string partway up the neck.",
    "mandolin": "A mandolin has eight strings in four pairs, tuned like a violin: G, D, A, E.",
    "piano": "A piano has 88 keys: 52 white and 36 black, seven and a bit octaves from A0 to C8.",
    "keyboard": "A full-size piano keyboard has 88 keys; a smaller synth or starter keyboard "
                "usually has 61 or 49.",
    "harp": "A concert harp has 47 strings, six and a half octaves.",
}
_COUNT_ASKS = ("how many", "number of", "how much", "count")


def _instrument_count(memory, understood):
    said = [str(word).lower() for word in (understood.get("words") or ())]
    flat = " ".join(said)
    for name in sorted(_INSTRUMENT_COUNTS, key=len, reverse=True):
        if name in said or name in flat:
            return _INSTRUMENT_COUNTS[name]
    return ("A guitar has six strings, a violin four, a bass four and a piano 88 keys. Ask me "
            "about the one you have and I'll tell you the count and the tuning.")


_PRACTICE_INSTRUMENTS = ("piano", "guitar", "violin", "cello", "viola", "double bass",
                         "bass guitar", "drums", "drum kit", "flute", "clarinet", "saxophone",
                         "sax", "trumpet", "trombone", "keyboard", "ukulele", "banjo",
                         "mandolin", "harp", "oboe", "bassoon", "recorder", "harmonica",
                         "instrument", "instruments", "music", "scales", "metronome",
                         "sheet music", "strumming", "picking", "fingerpicking",
                         "chord changes", "barre chord", "barre chords", "sight reading")

_PRACTICE_ASKS = ("practise", "practice", "practising", "practicing", "get better",
                  "better at", "improve", "how long should i practise", "how often should i practise",
                  "how long should i practice", "how often should i practice",
                  "what scales", "which scales", "scales to learn", "routine", "warm up",
                  "warm-up", "learn to read music", "read music", "reading music",
                  "sight read", "sight-read", "sight reading")

_PRACTICE_READ_MUSIC = ("Start with the rhythm, not the notes: clap a line of the music while a "
                        "metronome clicks, because the note names are the easy half. Then learn "
                        "the five lines of the treble staff with a mnemonic you make up, ten "
                        "minutes a day, and read one new short piece slowly each day rather than "
                        "the same one until it is perfect - reading is the skill of playing what "
                        "you have not seen before.")

_PRACTICE_CORE = ("Fifteen to twenty minutes a day beats two hours on Sunday, and start with the "
                  "hardest four bars rather than the beginning: play them slowly enough to get "
                  "them right, four times in a row, then put them back in the piece. Use a "
                  "metronome at a speed you can play cleanly and nudge it up two beats a minute, "
                  "because sloppy and fast teaches sloppy. Scales and one technical exercise "
                  "first warm the hands up, and finish on something you enjoy so you want to come "
                  "back tomorrow.")


_READ_MUSIC_WORDS = ("read music", "reading music", "sight read", "sight-read",
                     "sight reading", "learn to read", "sheet music")


def _music_practice(memory, understood):
    said = " ".join(str(word).lower() for word in (understood.get("words") or ()))
    if any(word in said for word in _READ_MUSIC_WORDS):
        return _PRACTICE_READ_MUSIC + " " + _PRACTICE_CORE
    return _PRACTICE_CORE


ENTRIES.append(entry("instrument-count", (tuple(_INSTRUMENT_COUNTS), _COUNT_ASKS),
                     _instrument_count,
                     ask=_COUNT_ASKS,
                     avoid=("lesson", "lessons", "teacher", "cost", "price", "expensive",
                            "cheap", "buy", "hire", "rent", "worth", "learn",
                            "orchestra", "orchestras", "band", "choir", "ensemble")))


ENTRIES.append(entry(
    "fly-a-kite",
    (("kite", "kites", "kite flying"), ("fly", "flying", "how do i", "how to", "launch",
                                        "get it up", "wont go up", "won't go up", "keep it up",
                                        "wont stay up", "wind", "first time", "stuck",
                                        "up in the air", "get up", "goes up", "air")),
    "Fly it in open ground away from trees and power lines, with the wind at your back. Let out "
    "ten or fifteen metres of line, have someone hold the kite up and walk back until the line is "
    "tight, then pull gently and let line run through your hands as it climbs. A steady 8-20 mph "
    "is the sweet spot: if it loops and dives, let out line, and if it will not rise at all, wait "
    "for more wind rather than running.",
    avoid=("kite runner", "book", "novel", "film", "movie", "author", "kite mark",
           "kite-mark", "kite marked", "kite-marked")))
ENTRIES.append(entry(
    "first-kite",
    (("kite", "kites"), ("buy", "buying", "first", "for a child", "for my son", "for my daughter",
                         "for a 5 year old", "for a 6 year old", "for a 7 year old",
                         "recommend", "which", "best", "beginner", "easy", "present")),
    "A diamond or a delta, about 1.2 to 1.5 metres across, is the usual first kite: it launches "
    "easily, flies in light wind and costs about fifteen to twenty-five pounds. Look for one "
    "with a long tail (it steadies the flight for a child) and a line of at least 30 metres on a "
    "winder. Skip the stunt kites and the two-line ones: they need more wind and a lot more "
    "practice. A cheap supermarket delta is fine to learn on - you can spend more when they ask "
    "for a second one.",
    avoid=("kite runner", "book", "novel", "film", "movie", "author", "kite mark",
           "kite-mark", "kite marked", "kite-marked"),
    bias=1))


ENTRIES.append(entry("film-war", (("war", "wartime"),
                                  ("film", "films", "movie", "movies", "watch", "watching",
                                   "recommend", "suggest", "suggestion", "good", "best",
                                   "something", "tonight")),
                     ("*Paths of Glory* is the one to start with: Kubrick, the WWI trenches, 88 "
                      "minutes. *Went the Day Well?* (92 minutes) is a British village invasion "
                      "story from 1942, and *Journey's End* (107 minutes) stays in one dugout and "
                      "never shows the battle. All three fit inside two hours, and *Full Metal "
                      "Jacket* is 116 if you want the training half too."),
                     bias=2, guard=_the_subject_is_wanted,
                     avoid=WATCHING + CHILD + SPORT + SCREEN_TIME + NOT_WATCHING +
                           ("board game", "computer game", "video game", "toy", "poppy",
                            "memorial", "war on", "war on drugs", "war on obesity")))
ENTRIES.append(entry(
    "cant-recall-the-name",
    (("remember", "forgot", "forget", "forgotten", "forgetting", "recall", "cant think",
      "can't think", "think of", "thinking of", "name", "named", "called", "what was that",
      "whats that", "what's that", "which was that", "half remember", "half-remember"),
     ("film", "films", "movie", "movies", "song", "songs", "tune", "album", "band", "book",
      "books", "novel", "show", "shows", "series", "programme", "program", "episode",
      "actor", "actress", "documentary", "cartoon", "title", "sitcom", "podcast")),
    ("Describe it to a search instead of reaching for the name: the year, one scene you are "
     "sure of, an actor's face. \"film where a boy finds a whale, 90s\" finds it, and IMDb's "
     "advanced plot search takes one detail at a time.",
     "Say what you do remember out loud - a scene, a voice, where you were when you saw it - and "
     "put that into a search or a forum; somebody always knows it. The name usually surfaces once "
     "you stop chasing it, and running the alphabet for the first letter shakes it loose. For a "
     "song, hum it into a song-finder app; for a book, the cover colour and the shop are as good "
     "as the title."),
    ask=("remember", "forgot", "forget", "recall", "cant think", "can't think", "think of",
         "name", "called", "what", "which", "half"),
    avoid=("baby", "babies", "puppy", "kitten", "dog", "cat", "company", "business", "domain",
           "website", "username", "password", "team", "band name", "middle name", "surname",
           "first name", "nickname", "pet", "boat", "house name", "wifi", "recommend",
           "recommendation", "what should i watch", "what should i read", "watch tonight",
           "read next", "something to watch", "something to read")))

ENTRIES.append(entry("instrument-strings", (("string", "strings", "guitar string",
                                             "guitar strings", "bass string", "bass strings",
                                             "violin string", "violin strings"),
                                            ("breaking", "break", "breaks", "broke", "snapped",
                                             "snap", "snapping", "change", "changed", "replace",
                                             "how often", "how long", "rusty", "corroded", "dull",
                                             "dead", "dirty", "old")),
                     "Change them every one to three months of near-daily playing, or when they "
                     "look dull or rusty and go out of tune within minutes - a set is six to ten "
                     "pounds. A string that keeps breaking at the same place means a sharp edge on "
                     "the saddle or the nut, or a burr in the tuning peg, so run a fingernail along "
                     "each and file any catch smooth. Change one at a time so the neck keeps its "
                     "tension, and stretch each new string by pulling it gently away from the "
                     "board before you tune it up.",
                     avoid=("tune", "tuning", "tuner", "in tune", "out of tune", "stay in tune",
                            "buzz", "buzzing", "fret buzz", "how many", "count", "number of",
                            "orchestra", "orchestras", "string section", "piece of string",
                            "on a string", "no strings",
                            "snapped", "snap", "snaps", "snapping", "broke", "broken",
                            "breaking", "breaks", "keep breaking", "keeps breaking",
                            "keep snapping", "keeps snapping", "bust")))


ENTRIES.append(entry("music-practice", (_PRACTICE_INSTRUMENTS, _PRACTICE_ASKS), _music_practice,
                     ask=("practise", "practice", "get better", "improve", "how long", "how often",
                          "scales", "read music"),
                     avoid=("lesson", "lessons", "teacher", "tutor", "cost", "price", "expensive",
                            "cheap", "free", "buy", "hire", "rent", "worth",
                            "which instrument", "guitar or piano", "piano or guitar",
                            "learn guitar", "learn piano", "learn to play",
                            "tune", "tuning", "tuner", "in tune", "out of tune", "stay in tune",
                            "buzz", "buzzing", "string", "strings", "restring",
                            "singing", "sing", "voice", "choir", "how many", "count",
                            "taste", "recommend", "playlist", "listen", "spotify",
                            "what should i listen",
                            "what scales are there", "which scales are there",
                            "what are the scales", "how many scales")))

_PODCAST_SUBJECTS = (
    ("science",
     ("science", "scientific", "physics", "chemistry", "biology", "space", "astronomy",
      "the universe", "nature", "wildlife", "animals", "climate", "climate change",
      "environment", "ecology", "engineering", "maths", "mathematics"),
     "For science with jokes: *The Infinite Monkey Cage*, a physicist and a comedian on one "
     "question in 45 minutes. *Science Vs* takes one claim an episode and weighs the evidence, "
     "and *Ologies* is a long friendly interview with a scientist each time. For space, *13 "
     "Minutes to the Moon* is the best thing made about Apollo."),
    ("food",
     ("food", "foods", "cooking", "cook", "chef", "chefs", "baking", "bake", "recipes",
      "recipe", "kitchen", "restaurants", "eating"),
     "*Home Cooking* (Samin Nosrat and Hrishikesh Hirway) answers listeners' kitchen questions "
     "and is the friendliest place to start. *The Sporkful* is about how and why people eat what "
     "they eat, and *Gastropod* takes one food an episode and does its history and science."),
    ("health",
     ("health", "healthy", "medicine", "medical", "doctor", "sleep", "insomnia", "fitness",
      "exercise", "running", "nutrition", "diet", "weight", "mental health", "anxiety",
      "stress", "wellbeing"),
     "For health with the evidence shown: *Zoe Science & Nutrition*, one food or habit an "
     "episode with a scientist and a doctor. For sleep, *Nothing Much Happens* reads quiet "
     "stories slowly and *Sleep With Me* rambles on purpose, both made to send you off rather "
     "than to be listened to."),
    ("sport",
     ("sport", "sports", "football", "cricket", "rugby", "tennis", "f1", "formula 1", "boxing",
      "golf", "athletics", "cycling", "match", "matches"),
     "For football, *Football Weekly* from the Guardian is twice a week, quick and funny, and "
     "*The Rest Is Football* is Lineker, Richards and Shearer talking. For cricket, *Tailenders* "
     "is the one people who do not like cricket listen to."),
    ("technology",
     ("tech", "technology", "technologies", "gadgets", "computer", "computers", "phone",
      "phones", "ai", "artificial intelligence", "internet", "software", "programming",
      "coding", "cyber", "hacking"),
     "*Hard Fork* (Kevin Roose and Casey Newton) is the weekly one on what the tech companies "
     "just did, and it is funny. *Darknet Diaries* is true stories of hacks and the people who "
     "did them, and *The Vergecast* is the long argument about gadgets."),
    ("news",
     ("news", "politics", "political", "current affairs", "world", "election", "elections",
      "government"),
     "*The Daily* takes one story a day and reports it properly in 20 minutes, *Today in Focus* "
     "does the same from a British side, and *The Briefing Room* explains one running story with "
     "the people who know it. For business, *The Bottom Line* puts three chief executives in a "
     "room and asks them the same question."),
    ("people",
     ("psychology", "psychologist", "human behaviour", "human behavior", "behaviour", "behavior",
      "relationships", "relationship", "feelings", "emotions", "people", "mindfulness",
      "meditation", "habits"),
     "*Hidden Brain* is the one to start with: one piece of psychology an episode, told as a "
     "story. *The Happiness Lab* is the research on what actually makes people happier, and "
     "*Where Should We Begin?* is Esther Perel with one real couple in a single session."),
    ("parenting",
     ("parenting", "parent", "parents", "babies", "baby", "newborn", "toddler", "kids",
      "children", "family", "families", "motherhood", "fatherhood"),
     "*Parenting Hell* (Rob Beckett and Josh Widdicombe) is two fathers being honest about how "
     "badly it is going, which is the most reassuring thing on the subject. *Happy Mum Happy "
     "Baby* is the calmer interview version, one parent an episode."),
    ("music",
     ("music", "songs", "song", "albums", "album", "bands", "band", "guitar", "singing"),
     "*Song Exploder* takes one song and has the person who made it pull it apart, track by "
     "track, in 20 minutes. *Desert Island Discs* is the long interview with the music choices in "
     "it, and *All Songs Considered* is the weekly new-music one."),
    ("business",
     ("business", "businesses", "company", "companies", "startup", "startups", "start a business",
      "starting a business", "entrepreneur", "entrepreneurs", "selling", "sales", "marketing",
      "the economy", "economy", "economics", "finance", "financial"),
     "*How I Built This* has the founder of one company telling how it actually started, in an "
     "hour, and it is the most useful one if you are thinking of starting something. *The Bottom "
     "Line* puts three bosses in a room and asks them the same question, and *StartUp* follows "
     "one company from the first day, mistakes included."),
    ("gardening",
     ("garden", "gardening", "gardens", "allotment", "allotments", "vegetables", "plants",
      "lawn", "grow your own"),
     "*Gardeners' Question Time* is the one to start with: three experts answering listeners' "
     "questions, so you get the answer to the thing you were wondering about. *Talking Gardens* "
     "is the interview version and *The RHS Podcast* the seasonal jobs."),
    ("film",
     ("film", "films", "movie", "movies", "cinema", "tv", "television", "series", "telly"),
     "*The Rewatchables* is one film an episode and why it still works, which is the best "
     "listen for someone who likes films. *Kermode & Mayo's Take* reviews what is out now, and "
     "*You Must Remember This* tells the old Hollywood stories properly."),
)

_PODCAST_FOR_KIDS = (
    "for kids", "for children", "for a child", "for my kids", "for my children", "for my son",
    "for my daughter", "with my kids", "with my children", "kids podcast", "kids podcasts",
    "podcast for kids", "podcasts for kids", "childrens podcast", "children's podcast",
    "child friendly", "family friendly", "my 5 year old", "my 6 year old", "my 7 year old",
    "my 8 year old", "a childrens", "a kids",
    "for a 4 year old", "for a 5 year old", "for a 6 year old", "for a 7 year old",
    "for an 8 year old", "for a 9 year old", "for a 10 year old",
    "4 year old", "5 year old", "6 year old", "7 year old")

_PODCAST_NOT_THIS = {"parenting": _PODCAST_FOR_KIDS, "people": _PODCAST_FOR_KIDS,
                     "science": _PODCAST_FOR_KIDS, "film": _PODCAST_FOR_KIDS}

ENTRIES.append(entry(
    "podcast-for-kids",
    (("podcast", "podcasts", "listen", "listening"), _PODCAST_FOR_KIDS),
    "*Wow in the World* is the best one to start with: science stories with two silly hosts, made "
    "for 5 to 8 year olds. *Story Pirates* turns stories children send in into sketches and songs, "
    "and *Circle Round* tells a folk tale in fifteen minutes with a proper cast. *But Why* answers "
    "the questions children actually ask, and *Smash Boom Best* is two things argued over by "
    "comedians with your child as the judge.",
    bias=3))

for _podcast_subject, _podcast_words, _podcast_reply in _PODCAST_SUBJECTS:
    ENTRIES.append(entry(
        "podcast-" + _podcast_subject,
        (("podcast", "podcasts"), _podcast_words),
        _podcast_reply,
        avoid=("book", "books", "novel", "novels", "read", "reading", "audiobook", "audiobooks",
               "recipe", "recipes to", "tonight", "watch")
               + _PODCAST_NOT_THIS.get(_podcast_subject, ()),
        bias=2))
GAME_KINDS = ("game", "games", "board game", "board games", "video game", "video games",
              "computer game", "computer games", "console", "playstation", "ps4", "ps5", "xbox",
              "nintendo", "steam", "puzzle game", "puzzle games", "co-op", "coop", "co op",
              "switch game", "switch games", "on my switch", "on the switch")
GAME_ASKS = ("recommend", "recommended", "recommendation", "recommendations", "suggest",
             "suggestion", "suggestions", "what should i", "what can i", "what to", "which",
             "any good", "any decent", "good", "best", "worth", "new", "next", "start",
             "beginner", "i need", "i want", "to play", "should i play", "buy",
             "getting", "something", "any", "new", "tonight", "evening", "weekend",
             "for a while", "to fill", "can i", "should i",
             "calm", "relax", "relaxing", "chill", "stressed", "anxious", "short", "quick",
             "story", "co-op", "coop", "co op", "puzzle", "puzzles", "two of us", "together",
             "me and my", "for the two", "for two",
             "board games", "board game", "puzzle games", "co-op games", "coop games",
             "co op games", "video games", "switch games", "card games", "two player games")
NOT_A_GAME_PICK = ("football", "soccer", "rugby", "cricket", "tennis", "badminton", "netball",
                   "basketball", "hockey", "golf", "darts", "snooker", "sport", "sports",
                   "match", "matches", "league", "team", "played for", "cup final",
                   "bet", "betting", "gamble", "gambling", "casino", "poker", "roulette",
                   "lottery", "scratchcard", "odds", "winnings",
                   "hunting", "game pie", "venison", "pheasant", "rabbit", "deer",
                   "party", "parties", "friends", "group", "grown ups", "kids", "children",
                   "toddler", "family", "two", "couple", "partner", "chess", "rules", "long",
                   "easy to learn", "simple", "parental", "controls", "restrict", "limit",
                   "addicted", "addiction", "screen time", "hours", "set up", "safely",
                   "how much", "price", "cost", "expensive", "cheap", "thrones", "squid game",
                   "mind games", "playing games", "game plan", "the game is",
                   "wedding", "funeral", "playlist", "music", "song", "songs", "radio",
                   "opening", "opens", "opened", "open on", "open today", "open till",
                   "closed", "closes", "closing", "shut", "shuts", "shutting", "what time",
                   "shop", "shops", "store", "supermarket", "aisle", "aisles", "checkout",
                   "meal deal", "sandwich", "milk", "bread", "receipt", "parking",
                   "nearest", "near me", "closest", "postcode", "address", "directions",
                   "whats the address", "which one is",
                   "job", "jobs", "work at", "works at", "working at", "shift", "shifts",
                   "the guitar", "piano", "instrument", "character", "part in",
                   "my son", "my daughter", "my kid", "my kids", "my child", "my children",
                   "year old", "toddler", "grandson", "granddaughter", "niece", "nephew",
                   "nursery", "birthday", "five a side", "five-a-side", "five aside",
                   "switch off", "switch on", "switching off", "jigsaw", "jigsaw puzzle",
                   "hunger games", "guitar", "piano", "drums", "cinema", "whats playing",
                   "what's playing", "school play",
                   "worth getting", "worth buying", "console or", "pc or", "gaming pc",
                   "which console", "or a pc", "or console",
                   "sell", "sells", "sold", "selling", "bestseller", "best seller",
                   "best selling", "best-selling", "top selling", "copies sold", "units sold",
                   "at christmas", "on christmas", "christmas day", "christmas eve",
                   "for christmas", "over christmas", "xmas eve", "at new year",
                   "for new year", "new years eve", "new year's eve", "on new years eve",
                   "make you", "makes you", "making you", "make people", "makes people",
                   "violent", "violence", "bad for you", "bad for kids", "rot your",
                   "are addictive", "too much screen", "ruin",
                   "present", "presents", "gift", "gifts", "stocking filler", "stocking fillers",
                   "secret santa")
GAME_PICKS = (
    (("switch", "nintendo", "mario"),
     "On a Switch: *Animal Crossing: New Horizons* to wind down, *Mario Kart 8 Deluxe* for "
     "people in the room, and *The Legend of Zelda: Breath of the Wild* for a big adventure."),
    (("xbox", "playstation", "ps4", "ps5", "console", "big screen"),
     "On a console: *Hades* for short, fast runs, *The Last of Us* if you want a story to sit "
     "through, and *Elden Ring* if you want a huge, hard world. *Hades* is the one I'd start "
     "with."),
    (("pc", "steam", "laptop", "computer"),
     "On a PC: *Stardew Valley* for something calm that never ends, *Portal 2* for puzzles, and "
     "*Disco Elysium* if you want to read as much as you play. *Stardew Valley* is the easy "
     "pick."),
    (("puzzle", "puzzles", "brain", "think"),
     "For puzzles: *Portal* (short, funny, brilliant), *The Witness* if you want to be stuck "
     "properly, or *Baba Is You* for something unlike anything else. *Monument Valley* on a "
     "phone if you only have ten minutes."),
    (("co-op", "coop", "co op", "girlfriend", "boyfriend", "wife", "husband", "together",
      "with my other half"),
     "For two of you: *It Takes Two* is built for exactly that, *Overcooked 2* if you want to "
     "shout at each other and laugh, and *Portal 2* for puzzles you solve as a pair. *It Takes "
     "Two* first."),
    (("calm", "relax", "relaxing", "cosy", "cozy", "chill", "stressed", "wind down", "anxious"),
     "*Stardew Valley* is the one for that: farm, fish, befriend the village, nothing is timed "
     "against you. *Animal Crossing* on a phone or a Switch, or *Unpacking* if you want "
     "something short and gentle."),
    (("story", "narrative", "plot", "emotional", "sad", "cry", "film like", "like a film"),
     "For a story: *The Last of Us* (grief and a road trip), *Red Dead Redemption 2* (a slow "
     "western with a lot of heart), or *Disco Elysium* if you would rather read. *The Last of "
     "Us* is the one people finish and then sit still for a while."),
    (("short", "quick", "evening", "few hours", "one sitting"),
     "Short ones: *Unpacking* (about three hours, and it says more than it sounds like it "
     "would), *Portal* (also about three), or *Firewatch* (an evening, and it stays with you)."),
    (("board", "boardgame", "boardgames", "tabletop", "card game", "cards"),
     "On a table: *Ticket to Ride* (trains, simple, satisfying), *Codenames* (two teams, one "
     "word grid) and *Azul* (tiles, quick, sharp). *Ticket to Ride* is the safest box for a "
     "household."),
)


def _not_a_crowd(understood):
    if str(understood.get("topic") or "") == "family-and-parenting":
        return False
    leaning = understood.get("leans_on") or {}
    if isinstance(leaning, dict):
        words = [str(word).lower() for word in (leaning.get("words") or ())]
        words.append(str(leaning.get("subject") or "").lower())
        words.append(str(leaning.get("text") or "").lower())
        flat = " ".join(words)
        if any(word in flat for word in _A_CROWD):
            return False
    return True


_A_CROWD = ("kids", "kid", "child", "children", "toddler", "boy", "girl", "son",
            "daughter", "grandchild", "party", "friends", "friend", "group", "family",
            "guests", "cousins", "nieces", "nephews", "playdate", "birthday")


_CHILD_WORDS = ("my son", "my daughter", "my boy", "my girl", "my kid", "my kids",
                "my child", "my children", "toddler", "grandson", "granddaughter",
                "with the kids", "with my kids", "playdate")


def _a_child_in_the_chat(memory):
    for said in (memory.get("turns") or ())[-8:]:
        words = str((said or {}).get("user") or "").lower()
        if not words or not any(word in words for word in _CHILD_WORDS):
            continue
        ages = [int(age) for age in re.findall(r"\b(\d{1,2})\s*(?:years? old|year old|yo)\b",
                                               words)]
        if ages and min(ages) >= 13:
            continue
        return True
    return False


def _the_game_pick(memory, reading):
    from .kept_animals import keeping_an_animal
    if keeping_an_animal(reading):
        return ""
    line = "%s %s" % (reading.get("clean") or "", reading.get("norm_text") or "")
    line = line.lower()
    if _a_child_in_the_chat(memory):
        return ("*Dobble*, *UNO* and *Jenga* work from about five up, and *Catan Junior* if they "
                "are ready for a proper board game. A treasure hunt round the house costs "
                "nothing and takes the longest.")
    for words, said in GAME_PICKS:
        if any(word in line for word in words):
            return said
    return ("*Hades* is the one I'd hand you first: fast, short runs, and it never wastes your "
            "time. *Stardew Valley* if you want calm, and *The Last of Us* if you want a story "
            "to sit through.")


NAMED_GAME_TITLES = ("monopoly", "catan", "settlers", "scrabble", "cluedo", "clue", "uno",
                     "risk", "ticket to ride", "azul", "codenames", "dixit", "carcassonne",
                     "pandemic", "boggle", "rummikub", "draughts", "checkers", "chess",
                     "minecraft", "fortnite", "roblox", "zelda", "mario", "animal crossing",
                     "hades", "stardew", "among us", "fifa", "call of duty")

GAME_JUDGED = ("is it any good", "good game", "good games", "any good", "worth it",
               "worth playing", "worth buying", "what do you think of", "what's it like",
               "whats it like", "like it")


_PLATFORMS = ("console", "consoles", "xbox", "playstation", "ps4", "ps5", "switch",
              "nintendo", "steam deck", "steam", "pc", "gaming pc", "gaming laptop",
              "graphics card", "controller", "controllers", "handheld", "game pass",
              "series s", "series x", "vr headset", "meta quest")
_BUYING_THE_MACHINE = re.compile(
    r"\b(?:buy|buying|bought|get|getting|upgrade(?:d|s)?\s+to|upgrading\s+to|"
    r"should\s+i\s+(?:buy|get))\s+(?:a|an|the|another|a\s+new|the\s+new)?\s*"
    r"(?:%s)\b" % "|".join(re.escape(word) for word in _PLATFORMS))
_MACHINE_SHAPES = (" worth it", " is it worth", " worth buying", " worth getting", "price of",
                   "how much does", "how much is a", "how much are", " best console",
                   " which console", " cheapest console", " cheaper ", " vs ", " versus ",
                   " or a ", " or an ", " cost ")


def _a_hardware_decision(understood):
    clean = " %s " % str(understood.get("clean") or "").lower().replace("-", " ")
    if not any(word in clean for word in _PLATFORMS):
        return False
    if _BUYING_THE_MACHINE.search(clean):
        return True
    return any(shape in clean for shape in _MACHINE_SHAPES)


def _a_game_pick_line(understood):
    if not _not_a_crowd(understood):
        return False
    if _a_hardware_decision(understood):
        return False
    clean = " %s " % str(understood.get("clean") or "").lower().replace("-", " ")
    if any(shape in clean for shape in (" get better at ", " get good at ",
                                        " how do i improve ", " how can i improve ")):
        return False
    judged = any(shape in clean for shape in GAME_JUDGED)
    if judged:
        for title in NAMED_GAME_TITLES:
            if re.search(r"(?<![a-z])%s(?![a-z])" % re.escape(title), clean):
                return False
    return True


GAME_SOLO_WORDS = ("on my own", "by myself", "by my self", "alone", "solo", "single player",
                   "singleplayer", "on my tod", "no one to play with", "nobody to play with",
                   "no one else to play with", "nothing to do with no one")
GAME_SOLO_ASKS = ("game", "games", "play", "playing", "board game", "video game")


def _the_solo_game(memory, reading):
    if _a_child_in_the_chat(memory):
        return ("*Dobble* is fine with one player as a speed game, and *UNO* works solo if you "
                "play the house down. *Catan Junior* really needs two, though.")
    return ("*Stardew Valley* is the one: farm, fish, befriend the village, nothing timed against "
            "you, and it runs on almost anything. *Hades* if you want ten-minute runs with a "
            "fight in them, or *Unpacking* for an evening of something quiet.")


ENTRIES.append(entry("game-picks", (GAME_KINDS, GAME_ASKS), _the_game_pick,
                     ask=GAME_ASKS, avoid=NOT_A_GAME_PICK, bias=2,
                     guard=_a_game_pick_line))
ENTRIES.append(entry("game-solo", (GAME_SOLO_WORDS, GAME_SOLO_ASKS), _the_solo_game,
                     avoid=NOT_A_GAME_PICK, bias=3))


ENTRIES.append(entry(
    "page-turner",
    (("page turner", "page turners", "pageturner", "page-turner", "page-turners",
      "unputdownable", "cant put it down book"),
     ("what is", "whats", "what does", "mean", "means", "recommend", "suggest", "which",
      "any", "good", "best", "book", "books", "novel", "read", "reading", "holiday")),
    "A page turner is a book whose plot pulls you through - short chapters, a question you want "
    "answered, a twist you did not see - rather than one you admire slowly. The shorthand comes "
    "from book reviews because it says nothing about quality: a thriller can be a page turner and "
    "so can a good memoir. If you want one, say what you last could not put down and I will find "
    "something in the same shape; if you want a specific book, tell me the kind of story rather "
    "than the word.",
    avoid=("bookmark", "page number", "printer", "paper", "print", "browser", "website",
           "web page", "homepage", "kindle", "page count"),
    bias=1))
