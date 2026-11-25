
BITE_DONE = (
    r"\b(?:dog|dogs|puppy)\b\s+(?:has\s+|had\s+|'s\s+|just\s+)?(?:bit|bitten|nipped)\s+"
    r"(?:me|him|her|them|my|his|their)\b",
    r"\b(?:dogs?|puppy)\b.{0,25}\b(?:bit\s+(?:me|him|her|them|my|his|their|a|the)|bitten|nipped|"
    r"snapped\s+at|went\s+for)\b.{0,30}"
    r"\b(?:me|my|his|her|their|the\s+(?:child|kid|baby)|a\s+(?:child|kid|baby))\b",
    r"\b(?:bitten|nipped|bit\s+(?:me|my|him|her|them))\b.{0,25}\b(?:by\s+a\s+dog|dog|puppy)\b",
    r"\b(?:bitten|bit\s+(?:me|my|him|her|them))\b.{0,20}\b(?:face|cheek|lip|hand|finger|arm|leg|ankle)\b",
    r"\b(?:bit|bites?|bitten|nipped)\s+"
    r"(?:me|my\s+(?:hand|hands|finger|fingers|thumb|wrist|arm|arms|leg|legs|foot|feet|toe|toes|"
    r"face|cheek|nose|ear|lip|shoulder|chest|belly|back|head|neck|skin))\b[^.?!]{0,30}"
    r"\b(?:bled|bleeds?|bleeding|blood|bloody|broke\s+(?:the|my)\s+skin|broke\s+skin|"
    r"marks?|drew\s+blood|draw\s+blood|drawn\s+blood|infected|needs?\s+stitches|"
    r"wont\s+stop\s+bleeding|won't\s+stop\s+bleeding)\b",
    r"\b(?:dog|dogs|puppy|puppies|cat|cats|kitten|kittens|pet|pets|horse|pony|rabbit|hamster|"
    r"parrot|budgie|ferret|gerbil)\b[^.?!]{0,30}\b(?:attacked|savaged|mauled|set\s+about|"
    r"went\s+for|went\s+at|lurched\s+at|turned\s+on)\s+"
    r"(?:me|him|her|them|us)\b",
    r"\b(?:dog|dogs|puppy|puppies|cat|cats|kitten|kittens|pet|pets|horse|pony|rabbit)\b"
    r"[^.?!]{0,20}\b(?:attacked|savaged|mauled|went\s+for|went\s+at|turned\s+on)\s+"
    r"(?:my|his|her|their|our)\s+(?:hand|hands|finger|fingers|thumb|arm|arms|leg|legs|foot|"
    r"feet|face|cheek|lip|ankle|head|neck|shoulder|ear|ears|nose|eye|wrist|toe|toes|thigh|"
    r"shin|knee|stomach|back)\b",
    r"\b(?:i|we)\b[^.?!]{0,15}\b(?:was|were|got|have\s+been|has\s+been|had\s+been)\s+"
    r"(?:attacked|savaged|mauled)\s+by\b.{0,20}\b(?:dog|dogs|puppy|puppies|cat|cats|kitten|"
    r"kittens|pet|pets|horse|pony|rabbit|hamster|parrot|budgie|ferret|gerbil)\b",
    r"\b(?:i|we)\b[^.?!]{0,15}\b(?:was|were|got|have\s+been|has\s+been|had\s+been)\s+"
    r"(?:bit|bitten|nipped)\s+by\b.{0,20}"
    r"\b(?:dog|dogs|puppy|puppies|cat|cats|kitten|kittens|pet|pets|horse|pony|rabbit|hamster|"
    r"parrot|budgie|ferret)\b",
    r"\b(?:my|his|her|their|our)\s+(?:hand|hands|finger|fingers|thumb|arm|arms|leg|legs|foot|"
    r"feet|face|cheek|lip|ankle|head|neck|shoulder|ear|ears|nose|eye|wrist|toe|toes)\b"
    r"[^.?!]{0,15}\b(?:was|were|got|has\s+been|had\s+been)\s+(?:bit|bitten|nipped)\s+by\b"
    r".{0,20}\b(?:dog|dogs|puppy|puppies|cat|cats|kitten|kittens|pet|pets|horse|pony|rabbit|"
    r"hamster|parrot|budgie|ferret)\b",
    r"\b(?:dog|dogs|cat|cats|puppy|puppies|kitten|kittens|pet|pets|horse)\b[^.?!]{0,15}"
    r"\bbites?\b[^.?!]{0,30}\b(?:infected|infection|septic|pus|ooz\w*|weep\w*|swollen|"
    r"swelling|red|hot|stitches?|tetanus|an?\s*(?:and|&)\s*e|hospital|antibiotics?)\b",
    r"\b(?:infected|septic|oozing|swollen|stitches?|tetanus|antibiotics?)\b[^.?!]{0,25}"
    r"\b(?:dog|cat|puppy|kitten)\s?bites?\b",
    r"\btetanus\b[^.?!]{0,30}\b(?:bite|bitten|bit|dog|cat|puppy|kitten|scratch)\b",
)



ALLERGY_NOW = (
    r"\b(?:i|im|i'?m|we|we'?re|he|she|they|my\s+\w+)\b[^.?!]{0,14}"
    r"\b(?:having|getting|developing|going\s+into)\b[^.?!]{0,20}"
    r"\b(?:allergic\s+reaction|reaction|anaphyla\w*)\b",
    r"\b(?:allergic\s+reaction|reaction)\b[^.?!]{0,14}"
    r"\b(?:right\s+now|now|starting|coming\s+on|just\s+happened)\b",
)


ALLERGY_SIGN_NAMED = (
    r"\b(?:swell\w*|swollen|puff(?:ed|y)?|bloat\w*|lips?|tongue|throat|mouth|face)\b",
    r"\b(?:breath\w*|wheez\w*|stridor|hoarse|croak\w*|voice)\b",
    r"\b(?:dizzy|faint\w*|light\s?headed|collapse\w*|passing\s+out|vomit\w*|throwing\s+up|sick)\b",
    r"\b(?:sting|stung|epipen|injector)\b",
    r"\b(?:hives?|rash\w*|itch\w*|blotch\w*|red\s+spots?|nettle\s+rash)\b",
    r"\b(?:fine\s+now|was\s+fine|settled|went\s+away|calmed\s+down|last\s+(?:year|week|month)|"
    r"years\s+ago|as\s+a\s+kid|used\s+to|once|back\s+then)\b",
)


GRATER_CUT = (
    r"\bgrat(?:e|es|ed|ing)\b[^.?!]{0,24}\b(?:my|his|her|their|the)\s+"
    r"(?:finger|thumb|hand|knuckle|nail|fingertip|palm)",
)


STRUCK_BY_A_VEHICLE = (
    r"\b(?:nearly|almost|close\s+to|came\s+close\s+to|just\s+about)\b[^.?!]{0,20}"
    r"\b(?:(?:got|get|gets|getting|been|be|being|was|were|had)\s+)?"
    r"(?:run\s+over|hit|struck|clipped|swiped|knocked\s+(?:off|down|over))\b[^.?!]{0,16}\b(?:by|"
    r"by\s+a|by\s+the)\b",
    r"\b(?:nearly|almost|close\s+to|came\s+close\s+to|just\s+about)\b[^.?!]{0,20}"
    r"\b(?:got|get|gets|getting|been|be|being|was|were|had)?\s*"
    r"(?:run\s+over|knocked\s+off|knocked\s+down|knocked\s+over|clipped|swiped|"
    r"rammed|mow(?:ed|n)\b[^.?!]{0,10}\bdown)\b",
    r"\b(?:bus|car|lorry|truck|van|tram|train|taxi|cab|motorbike|motorcycle|moped|scooter|bike|"
    r"bicycle|cyclist|driver)\b[^.?!]{0,12}\b(?:nearly|almost)\s+"
    r"(?:hit|missed|struck|clipped|knocked)\s+(?:me|us|him|her|them|my\s+\w+)\b",
    r"\b(?:nearly|almost)\b[^.?!]{0,16}\b(?:went|go|going|gone|fell|ended\s+up)\b[^.?!]{0,14}"
    r"\bunder\s+(?:a|the|an)\s+(?:bus|car|lorry|truck|van|tram|train)\b",
    r"\b(?:nearly|almost|close\s+to|just\s+about)\b[^.?!]{0,10}\b(?:ran|run|runs)\s+"
    r"(?:me|us)\s+(?:over|down)\b",
)


STRUCK_MY_BIKE = (
    r"\b(?:my|our|his|her|their|the)\s+(?:bike|bicycle|motorbike|motorcycle|scooter|moped)\b"
    r"[^.?!]{0,24}\b(?:got|get|gets|was|were|is|are|been|had\s+been)\s*"
    r"(?:clipped|hit|struck|swiped|knocked|nudged|shunted|rammed|sideswiped)\b"
    r"[^.?!]{0,18}\b(?:van|car|lorry|truck|bus|coach|taxi|cab|tractor|driver)\b",
    r"\b(?:a|an|the|some|one|another)\s+(?:van|car|lorry|truck|bus|coach|taxi|cab|tractor|"
    r"driver)\b[^.?!]{0,16}\b(?:clipped|hit|struck|swiped|knocked|nudged|shunted|rammed|"
    r"sideswiped)\b[^.?!]{0,12}\b(?:my|our|his|her|their|the)\s+(?:bike|bicycle|motorbike|"
    r"motorcycle|scooter|moped)\b",
)


NEAR_HIT_ON_A_ROAD = (
    r"\b(?:nearly|almost|close\s+to|just\s+about)\b[^.?!]{0,12}\b(?:hit|hits|struck|"
    r"ran\s+over|run\s+over|knocked|clipped|caught)\s+(?:me|us)\b",
)
NEAR_HIT_ON_A_ROAD_PLACE = (
    r"\b(?:crossing|zebra|pelican|crossroads|pavement|kerb|curb|road|street|junction|"
    r"roundabout|bollard|cycle\s*lane|bike\s*lane|lay-?by|motorway|dual\s+carriageway|"
    r"bus\s+stop|car\s+park|driveway|level\s+crossing|lights)\b",
)


STRUCK_BY_A_VEHICLE_NOT = (
    r"\b(?:step(?:ped|ping)?|walk(?:ed|ing)?|jump(?:ed|ing)?|stand(?:ing)?|stood|lay|laid|sat|"
    r"sitting|straddl\w*|leant|leaned)\b",
)


INSECT_BITE_BODY = (
    r"(?:arms?|hands?|fingers?|thumb|legs?|feet|foot|ankles?|wrists?|neck|face|cheek|head|back|"
    r"shoulders?|knees?|elbow|shin|toes?|hip|stomach|belly|ears?|eyes?|chest|forehead|scalp)"
)


INSECT_BITE_NEEDS_A_LOOK = (
    r"\b(?:hands?|wrists?|fingers?|thumb|face|cheek|eyes?|knees?|elbows?|joints?)\b",
)


INSECT_BITE = (
    r"\b(?:mosquito(?:es)?|midges?|gnats?|fleas?|horse\s?fly|horseflies|cleg|spiders?|bed\s?bugs?|"
    r"sand\s?fly|ants?)\b[^.?!]{0,24}\b(?:bit|bitten|bite|nipped|stung?)\b[^.?!]{0,10}"
    r"\b(?:me|him|her|them|us)\b[^.?!]{0,8}\b(?:on|in|under|between)\b[^.?!]{0,8}"
    r"\b(?:the|my|his|her|their|both)\b\s*" + INSECT_BITE_BODY + r"\b",
    r"\b(?:mosquito(?:es)?|midges?|gnats?|fleas?|horse\s?fly|horseflies|cleg|spiders?|bed\s?bugs?|"
    r"ants?)\b[^.?!]{0,24}\b(?:bit|bitten|bite|nipped|stung?)\b\s+"
    r"(?:my|his|her|their)\s+" + INSECT_BITE_BODY + r"\b",
    r"\b(?:i|we)\b[^.?!]{0,15}\b(?:was|were|got|have\s+been|has\s+been|had\s+been)\b[^.?!]{0,10}"
    r"\b(?:bit|bitten|stung)\s+by\s+(?:a|an|the)?\s*(?:mosquito|midge|gnat|flea|ant|spider|"
    r"horse\s?fly)\b[^.?!]{0,10}\b(?:on|in)\b",
)


TICK_BITE = (
    r"\bticks?\b[^.?!]{0,24}\b(?:bit|bitten|bite|on\s+me|on\s+my|attached|dug\s+in|"
    r"burrow\w*|stuck\s+in|in\s+my)\b",

    r"\b(?:a\s+|the\s+)?tick\s+(?:bite|bites)\b",
    r"\b(?:i|we)\b[^.?!]{0,15}\b(?:was|were|got|have\s+been|has\s+been|had\s+been|might\s+have\s+been)\s+"
    r"(?:bit|bitten)\s+by\s+(?:a|an|the|some)?\s*tick\b",
)


TICK_ALREADY = (r"\b(?:found|pulled|removed|took|got\s+(?:it|one))\b",)


BAT_BITE = (
    r"\b(?:bat|bats)\b[^.?!]{0,24}\b(?:bit|bitten|bite|scratch(?:ed|es)?|claw(?:ed)?|nipped)\b"
    r"[^.?!]{0,24}\b(?:me|him|her|them|us|my|his|her|their)\b",
    r"\b(?:i|we)\b[^.?!]{0,15}\b(?:was|were|got|have\s+been|has\s+been|had\s+been|might\s+have\s+been)\s+"
    r"(?:bit|bitten|nipped|scratched|clawed)\s+by\s+(?:a|an|the)?\s*bat\b",
    r"\b(?:a|an|the|that|this|my|his|her|their)\s+bat\s+(?:bite|bites|scratch|scratches)\b"
    r"(?!\s+(?:a|an|the|it)\b)",
    r"\bbat\b[^.?!]{0,40}\b(?:woke\s+up\s+with|marks?|a\s+mark|scratch\w*)\b",
)


WILD_BITE = (
    r"\b(?:fox|foxes|badger|badgers|squirrel|squirrels|rat|rats|hedgehog|hedgehogs|mouse|mice|"
    r"deer|otter|weasel|stoat|mole|vole|seagull|gull|swan|goose|geese|crow|magpie|pigeon|"
    r"kestrel|buzzard|owl|tick|ticks|wild\s+animal)\b[^.?!]{0,24}"
    r"\b(?:bit|bitten|bite|nipped|scratched|clawed|went\s+for|attacked)\b[^.?!]{0,20}"
    r"\b(?:me|him|her|them|us|my|his|her|their)\b",
    r"\b(?:i|we)\b[^.?!]{0,15}\b(?:was|were|got|have\s+been|has\s+been|had\s+been)\s+"
    r"(?:bit|bitten|nipped|scratched|clawed)\s+by\s+(?:a|an|the|some)?\s*"
    r"(?:fox|badger|squirrel|rat|hedgehog|mouse|deer|otter|seagull|gull|swan|goose|"
    r"wild\s+animal)\b",
    r"\b(?:a|an|the|that|this|my|his|her|their)\s+(?:fox|badger|squirrel|rat|hedgehog)\s+"
    r"(?:bite|bites|scratch)\b(?!\s+(?:a|an|the|it)\b)",
)


COUNTERFACTUAL_WISH = (
    r"\bwis?h\b[^.?!]{0,24}\b(?:i|he|she|they|it|the\s+\w+|that\s+\w+)\b[^.?!]{0,16}"
    r"\b(?:had|have|would\s+have|'d)\b[^.?!]{0,12}"
    r"\b(?:died|been\s+killed|killed\s+me|not\s+survived|never\s+woke\s+up|ended\s+it|"
    r"gone\s+ahead|done\s+it|finished\s+it|not\s+woken\s+up)\b",
    r"\bwis?h\b[^.?!]{0,16}\b(?:i|he|she|they)\b[^.?!]{0,10}"
    r"\b(?:hadn'?t|had\s+not|never)\b[^.?!]{0,10}"
    r"\b(?:survived|woken\s+up|made\s+it|come\s+round|pulled\s+through)\b",
    r"\b(?:nearly|almost)\b[^.?!]{0,30}\b(?:died|killed\s+(?:my|him|her)self|got\s+hit|"
    r"been\s+hit|run\s+over|knocked\s+(?:me\s+)?(?:off|down|over)|gone\s+under)\b"
    r"[^.?!]{0,40}\bwis?h\b[^.?!]{0,30}\b(?:it|that|i|they)\b[^.?!]{0,12}"
    r"\b(?:had|would\s+have|'d)\b[^.?!]{0,16}"
    r"\b(?:worked|happened|gone\s+through|succeeded|done\s+it|killed\s+me|finished\s+(?:it|"
    r"the\s+job|me\s+off)|taken\s+me|done\s+for\s+me)\b",
)


EFFORT_BEFORE = (
    r"\b(?:came|come|fell|fallen|slipped|tripped|tumbled|crashed|went\s+over|got\s+knocked)\b"
    r"[^.?!]{0,24}\b(?:nearly|almost)\b[^.?!]{0,20}\b(?:killed|kill)\s+my\s*self\b"
)


EFFORT_DIED = (
    r"\b(?:nearly|almost|came\s+close\s+to|so\s+close\s+to)\b[^.?!]{0,20}"
    r"\b(?:died|killed\s+(?:my|him|her|them)self)\b"
)


COME_OFF_IT = (
    r"\b(?:off|on|from)\s+(?:(?:my|his|her|their|our|a|the)\s+)?"
    r"(?:bike|bicycle|motorbike|motorcycle|scooter|moped|horse|pony|quad|skateboard|"
    r"ladder|roof|scaffold|balcony|wall|fence|trampoline|stairs|steps|staircase|"
    r"road|motorway|kerb|car|van|truck|lorry|tractor|boat)\b"
)


EFFORT_DOING = (
    r"\b(?:nearly|almost)\b[^.?!]{0,24}\b(?:killed|kill)\s+(?:my|him|her|them)self\s+"
    r"(?P<doing>[a-z']+ing)\b"
)


EFFORT_NOT_AN_ACCIDENT = (
    r"\b(?:on\s+purpose|deliberately|by\s+choice|meant\s+to|tried\s+to|wanted\s+to)\b",
    r"\b(?:wish|wished|hope|hoped)\b",
    r"\b(?:so\s+i\s+(?:would|could)\s+die|to\s+die)\b",
)


COUNTERFACTUAL_IDIOM = (
    r"\b(?:died|killed\s+(?:my|him|her)self|killed\s+me)\s+"
    r"(?:laughing|of\s+(?:embarrassment|boredom|shame|thirst|curiosity))\b",
)

PERSON_HANGING = (
    r"\b(?:he|she|they|hes|shes|theyre|someone|somebody|(?:my|his|her|their|our)\s+(?:brother|"
    r"sister|mum|mom|mam|dad|father|mother|son|daughter|child|kid|boy|girl|baby|husband|wife|"
    r"partner|boyfriend|girlfriend|ex|uncle|aunt|nan|nana|gran|granny|grandad|grandpa|grandma|"
    r"grandmother|grandfather|cousin|friend|mate|flatmate|housemate|neighbour|neighbor|carer|"
    r"stepdad|stepson|stepdaughter|nephew|niece)s?)\b[^.?!]{0,20}?'?s?\s+"
    r"(?:is\s+|was\s+)?(?:hanging|hung)\b"
    r"(?!\s+(?:the|a|an|his|her|their|my|our|your|some|those|these|up|out|around|about|"
    r"over|back|"
    r"christmas|fairy|lights|decorations|baubles|garland|wreath|washing|laundry|clothes|out\s+with|"
    r"wallpaper|tinsel|foil|lining|bunting|paper|"
    r"himself|herself|themselves|my\s*self|myself|"
    r"on\s+the\s+(?:phone|line|doorstep|door|bell|internet|web|sofa|fence|gate|wall))\b)"
    r"(?!\s+(?:by\s+a\s+thread|by\s+(?:his|her|their|my)\s+fingertips?|in\s+there)\b)"
    r"(?!\s+on\b\s*(?:$|[.,!?;]|\bin\s+there\b|at\b))"
    r"(?!\s+(?:on|from|off)\s+(?:the\s+)?(?:monkey\s+bars|wall\s+bars|climbing\s+frame|"
    r"trampoline|slide|swing|bars|sofa|couch|settee|bed|bunk|bunk\s+bed|chair|table|bike|"
    r"swing\s+set)\b)"
    r"(?!\s+upside\s+down\b)"
    r"(?!\s+(?:on\s+)?for\s+dear\s+life\b)"
    r"(?!\s+[a-z]+s\b)"
    r"(?!\s+round\b)"
    r"(?!\s+with\s+(?:(?:his|her|their|my|our)\s+|the\s+)?(?:mates?|friends?|family|kids|lads|"
    r"girls|boys|crowd)\b)"
    r"(?!\s+(?:by|at)\s+the\s+(?:bar|counter|pub)\b)",
)

HEAD_OUT_COLD = (
    r"\bout\s+cold\b[^.?!]{0,30}\b(?:tackle[ds]?|rugby|football|boxing|match|game|scrum|"
    r"fell|fall|fallen|collided|collision|crashed?|crash|"
    r"car|van|bike|motorbike|lorry|stairs|steps|ladder|wall|door|branch|tree|"
    r"goalpost|post|railing|kerb|curb|round|rounds|canvas|ring|ring\s+rope)\b",
    r"\bout\s+cold\b[^.?!]{0,30}\b(?:hit|banged?|struck|smacked|cracked|knocked)\b"
    r"[^.?!]{0,12}\bheads?\b",
    r"\bheads?\b[^.?!]{0,20}\b(?:injur\w+|wound|trauma)\b[^.?!]{0,20}\bout\s+cold\b",
    r"\bout\s+cold\b[^.?!]{0,60}\b(?:after|from|when|because)\b[^.?!]{0,30}"
    r"\b(?:a\s+bang|bang(?:ed)?|hitting|hit|blew|blow|knocked|knock|fall|fell|falling|"
    r"blow\s+to|kick|punch|crash|accident|smack)\b",
    r"\bout\s+cold\b[^.?!]{0,40}\b(?:bleeding|bled|blood|fitting|"
    r"had\s+a\s+fit(?!\s+of\s+(?:giggles|the\s+giggles|laughing))|seizure|"
    r"convuls\w*|stopped\s+breathing|not\s+breathing|vomit\w*|threw\s+up|being\s+sick)\b",
    r"\b(?:hit|banged?|knocked|struck|clipped|collided|fell|fallen|crashed|tackled)\b"
    r"[^.?!]{0,30}\bout\s+cold\b",
    r"\bout\s+cold\b[^.?!]{0,20}\b(?:floor|ground|street|pavement|road|sofa|couch)\b",
    r"\bfound\s+(?:him|her|them|my\s+\w+|\w+)\b[^.?!]{0,25}\bout\s+cold\b",
    r"\bout\s+cold\b[^.?!]{0,30}\bwhen\s+i\s+(?:found|got\s+home|got\s+in|got\s+back|"
    r"came\s+in|came\s+home|arrived)\b",
    r"\bout\s+cold\s+for\s+(?:more\s+than\s+a\s+minute|(?:two|three|four|five|six|seven|"
    r"eight|nine|ten|fifteen|twenty|thirty|forty|fifty|sixty|\d{2,})\s*(?:mins?|minutes?|"
    r"hours?|hrs?)|ages|hours)\b",
    r"\bout\s+cold\b[^.?!]{0,20}\b(?:blue|grey|gray|clammy|mottled|ashen)\b",
    r"\bout\s+cold\b[^.?!]{0,40}\b(?:wet\s+my\s*self|wet\s+the\s+bed|wet\s+(?:him|her)\s*self|"
    r"soaked\s+my\s*self|peed\s+my\s*self|peed\s+(?:him|her)\s*self|incontinent)\b",
)

STRUCK_NOT_NOW = (
    r"\b(?:fell|fallen|falling|came|come|comes|slipped|toppled|tipped)\s+off\s+(?:\w+\s+)?"
    r"(?:bike|bicycle|motorbike|motorcycle|scooter|moped|skateboard|horse)\b[^.?!]{0,40}\b"
    r"(?:hit|hits|banged|bangs|struck|strikes)\s+(?:my|his|her|their|our|your)\s+"
    r"(?:head|face|chin|nose|knee|elbow|arm|leg|hip|shoulder|hand|wrist|ankle|back|chest)\b",
    r"\bnearly\b", r"\balmost\b", r"\bjust\s+about\b", r"\bnarrowly\b", r"\bclose\s+call\b",
    r"\bwhat\s+if\b", r"\bif\s+(?:i|he|she|they|we|my\s+\w+)\b", r"\bimagine\b",
    r"\bsuppose\b",
    r"\b(?:years?|decades?)\s+(?:ago|back)\b", r"\bin\s+(?:19|20)\d\d\b",
    r"\bwhen\s+(?:i|he|she|they)\s+(?:was|were)\s+(?:a\s+|an\s+)?"
    r"(?:kid|child|little|small|young|boy|girl|teenager|teen)\b",
    r"\blast\s+(?:year|summer|winter|christmas|xmas|term|month|week)\b",
    r"\bmissed\s+(?:me|him|her|them|us|my\s+\w+)\b",
    r"\bfrom\s+behind\b", r"\bin\s+the\s+back\b", r"\brear-?end\w*\b", r"\bwhiplash\b",
    r"\bshunt\w*\b", r"\bwrote\s+(?:it|the\s+car)\s+off\b",
    r"\bover\s+to\b",
    r"\bover\s+(?:the\s+|a\s+|our\s+|my\s+|your\s+)?(?:plan|plans|details|budget|figures|numbers|"
    r"points|list|lists|options|wording|email|emails|costs|cost|rules|schedule|story|recipe|"
    r"contract|draft|accounts|it|them|this|that)\b",
    r"\bran\s+over\s+time\b", r"\bover\s+time\b",
    r"\b(?:you|we|i|they)\s+(?:can|could|should|must)\s+run\s+over\b",
    r"\b(?:foxe?s?|badgers?|hedgehogs?|deer|squirrels?|owls?|swans?|pigeons?|hares?)\b"
    r"\s+(?:\w+\s+){0,3}(?:run|ran|runs|got|get|was|were|is)?\s*"
    r"(?:over|hit|hits|struck|clipped|knocked)\b",
    r"\bby\s+(?:a\s+|the\s+)?(?:trolley|shopping\s+trolley|pram|pushchair|buggy|wheelchair|"
    r"mobility\s+scooter|crowd|queue)\b",
    r"\b(?:a|an|the|its|his|her|their|my|our)\s+(?:\w+\s+)?doors?\b",
    r"\b(?:hit|hits|struck|strikes|clipped|clips)\s+(?:me|him|her|them|us)\s+with\b",
    r"\b(?:mum|mom|mother|dad|father|son|daughter|husband|wife|partner|boyfriend|girlfriend|"
    r"brother|sister|friend|child|kid|baby|boy|girl|man|woman|lady|neighbou?r|colleague|mate|"
    r"gran|granny|nan|grandad|grandma|grandpa|passenger|cyclist|pedestrian|toddler|teenager|"
    r"nephew|niece|cousin|aunt|uncle|stepson|stepdaughter|stepdad|stepmum|driver|owner)"
    r"\s*['\u2019]?s?\s+(?:car|cars|bike|bikes|van|vans|lorry|lorries|truck|trucks|bus|buses|"
    r"wall|walls|fence|fences|gate|gates|hedge|hedges|house|window|windows|bins?|garden|"
    r"garage|drive|driveway|shed|roof|bumper|wing|mirror|gatepost|door|school|schools|"
    r"nursery|playground|office|work|workplace|shop|shops|church|building|home|flat|room)\b",
)

SELF_HARM_HABIT = (
    r"\bi\s+(?:keep|keeps|kept|keep\s+on)\s+(?:cutting|hurting|burning)\b"
    r"(?=\s*(?:$|[.,!?]|and\b|again\b|so\b|all\b|every\b))",
    r"\b(?:keep|keeps|kept|keep\s+on)\s+(?:cutting|hurting|burning|scratching|hitting|banging|"
    r"punching|choking|starving)\s+(?:(?:my|him|her|your)\s*self|them\s*selves|them\s*self)\b",
    r"\b(?:we'?ve|i'?ve|we|i)\s+(?:have|has|had|'?ve)?\s*been\s+(?:on\s+)?"
    r"cutting\b(?=\s*(?:$|[.,!?]|a\s+lot\b|recently\b|lately\b|too\b|most\b|badly\b|"
    r"every\s+day\b|now\b|on\s+and\s+off\b|again\b|"
    r"for\s+(?:weeks|months|years|ages|days|a\s+while|a\s+bit|a\s+long\s+time)\b|"
    r"since\s+(?:i\s+was|then|last\s+year|christmas|primary|school|my\s+teens|"
    r"forever)\b|and\s+(?:i|it)\b|so\s+(?:much|badly|many|hard)\b))",
    r"\bi\s+cut\s+again\b(?!\s+(?:on|with|at|in|while|after|during|doing|from|"
    r"using|because|the\s+(?:knife|bread|glass|gym|run))\b)",
)

HEAL_TIME = {
    "sprain": (
        "It depends how bad it is. A mild sprain is usually much better in one to two weeks and "
        "normal again in four to six; a bad one with a lot of bruising can take eight to twelve "
        "weeks, and the first 48 hours of rest, ice and keeping it raised are what set that up. "
        "Start gentle movement and walking on it as the pain allows rather than staying off it, "
        "and get it seen if you cannot put weight on it at all, it is very swollen, or it is no "
        "better after a week.",
        "Most sprains are much better in one to two weeks and properly right in four to six; a bad "
        "one can take a couple of months. Ice and rest for the first two days, then gentle walking "
        "and moving it as far as it lets you. A joint you cannot put weight on, or one that is no "
        "better after a week, is worth having looked at."),
    "burn": (
        "A small burn usually settles in a week to ten days, and a blistering one takes about two "
        "to three weeks to heal from underneath. Keep it clean and covered and leave blisters "
        "alone; anything bigger than your palm, on the face or hands, or slow to heal after two "
        "weeks should be seen.",
        "A small burn is mostly fine in seven to ten days, and a blistered one in about two to "
        "three weeks. Leave the blisters alone and keep it covered; a burn that is not healing "
        "after a fortnight, or is on the face or hands, needs a nurse."),
    "blister": (
        "A rubbed blister drains and dries up in about three to five days and the skin under it "
        "is new in a week or two; leave the roof on, cover it with a padded plaster and keep it "
        "dry. One that is hot, spreading or weeping pus is the doctor's rather than time.",
        "Most blisters settle in three to five days and are properly new skin in a week or two. "
        "Cover it, don't pop it, and keep it dry; hot, spreading or pus needs a doctor."),
    "cut": (
        "A small cut closes over in a few days and is usually fully healed in a week or two, with "
        "the edges kept together and the dressing changed. Redness spreading, pus, or a cut that "
        "gapes needs to be seen the same day rather than waited on.",
        "Small cuts close in a few days and are properly healed in a week or two. Keep it clean and "
        "covered, and get it looked at if it goes red and hot, weeps pus, or will not close."),
    "sunburn": (
        "The redness of sunburn usually settles in three to five days and the peeling in about a "
        "week. Cool showers, plenty of water and leaving the peeling skin alone are what help; "
        "shivering, dizziness or bad blisters need a doctor.",
        "Sunburn redness mostly fades in three to five days and the peeling takes about a week. "
        "Cool showers and water help, and leave the skin alone; shivery, dizzy or badly blistered "
        "is a doctor."),
}

HEAD_REPLIES = {
    "head_bang": (
        "A bang on the head is usually fine, but the next 24 hours are the ones to watch: being sick, "
        "being knocked out, or feeling confused or unusually sleepy means an ambulance or A&E rather "
        "than wait, and 111 will advise you on anything milder. Are you up and talking normally now, "
        "or has anything changed since it happened?",
        "A bumped head hurts for a day or two and an ice pack on it for ten minutes is plenty, but "
        "a knock-out, being sick, or feeling confused or sleepier than usual means an ambulance or A&E "
        "rather than wait - 111 for anything milder. Are you up and talking normally now, or has "
        "anything changed since it happened?",
    ),
    "head_bang_other": (
        "A bang on the head is usually fine, but the next 24 hours are the ones to watch: being sick, "
        "being knocked out, or {s} seeming confused or unusually sleepy means an ambulance or A&E "
        "rather than wait, and 111 will advise you on anything milder. Is {s} up and talking normally "
        "now, or has anything changed since it happened?",
        "A bumped head hurts for a day or two, but a knock-out, being sick, or {s} seeming confused or "
        "sleepier than usual means an ambulance or A&E rather than wait - 111 for anything milder. Is "
        "{s} up and talking normally now, or has anything changed since it happened?",
    ),
    "head_bang_red": (
        "That is a 999 call rather than wait and see: being knocked out, confused, drowsy or sick after "
        "a bang on the head is a head injury until a doctor says otherwise. Keep still and awake, stay "
        "with someone, and don't drive yourself.",
        "Ring 999 or 911 now rather than waiting to see: confusion, drowsiness or sickness after a bang "
        "on the head is a head injury until a doctor says otherwise. Keep awake and still while you "
        "wait, and don't take anything for the headache until someone has seen you.",
    ),
    "head_bang_red_other": (
        "That is a 999 call rather than wait and see: being knocked out, confused, drowsy or sick after "
        "a bang on the head is a head injury until a doctor says otherwise. Stay with {o}, keep {o} "
        "awake and still, and don't let {o} drive.",
        "Ring 999 or 911 now rather than waiting to see: confusion, drowsiness or sickness after a bang "
        "on the head is a head injury until a doctor says otherwise. Keep {o} awake and still, and stay "
        "with {o} until help comes.",
    ),
}

HUMAN_BITTEN = (
    r"\b(?:bit|bitten|nipped|snapped\s+at|went\s+for|attacked)\s+(?:me|him|her|us|them)\b",
    r"\b(?:bit|bitten|nipped)\s+(?:my|his|her|their|our)\s+(?:hand|hands|finger|fingers|thumb|"
    r"arm|arms|leg|legs|foot|feet|face|cheek|lip|ankle|head|neck|shoulder|ear|ears|nose|eye|wrist|"
    r"toe|toes)\b",
    r"\b(?:bit|bitten|nipped)\s+(?:the|a)\s+(?:child|kid|baby|boy|girl|man|woman|postman|postie|"
    r"vet)\b",
    r"\b(?:my|our|her|his|their)\s+(?:son|daughter|child|kid|baby|husband|wife|partner|mum|mom|"
    r"dad|father|mother|friend|neighbour|neighbor|postman|postie)\b[^.?!]{0,20}"
    r"\b(?:was|were|got|has\s+been|had\s+been)\s+(?:bit|bitten)\b",
    r"\b(?:i|we)\b[^.?!]{0,12}\b(?:was|were|got|have\s+been|has\s+been|had\s+been)\s+"
    r"(?:bit|bitten)\b",
    r"\b(?:i|we)\b[^.?!]{0,15}\b(?:was|were|got|have\s+been|has\s+been|had\s+been)\s+"
    r"(?:attacked|savaged|mauled|scratched|clawed)\b",
    r"\b(?:my|his|her|their|our)\s+(?:hand|hands|finger|fingers|thumb|arm|arms|leg|legs|foot|"
    r"feet|face|cheek|lip|ankle|head|neck|shoulder|ear|ears|nose|eye|wrist|toe|toes)\b"
    r"[^.?!]{0,15}\b(?:was|were|got|has\s+been|had\s+been)\s+(?:bit|bitten)\b",
    r"\b(?:scratch(?:ed|es|ing)?|claw(?:ed|s|ing)?)\s+(?:me|him|her|us|them)\b",
    r"\b(?:scratch(?:ed|es|ing)?|claw(?:ed|s|ing)?)\s+(?:my|his|her|their|our)\s+(?:hand|hands|"
    r"finger|fingers|thumb|arm|arms|leg|legs|foot|feet|face|cheek|lip|ankle|head|neck|shoulder|"
    r"ear|ears|nose|eye|wrist|toe|toes|skin)\b",
)



MILD = (
    r"\bthrough\s+my\s+nose\b", r"\bfood\s+poisoning\b", r"\bpoison\s+ivy\b", r"\bpoisonous\s+(?:plant|mushroom|snake|spider)\b",
    r"\bfire\s+(?:alarm|drill|station|escape|pit|place|works|extinguisher|guard|fighter)s?\b",
    r"\b(?:camp|bon)fire\b", r"\bfireworks?\b", r"\bfired?\s+(?:from|up)\b", r"\bon\s+fire\b.*\b(?:team|player|form|streak)\b",
    r"\b(?:bleed|bled|bleeding)\s+(?:the|my|a)\s+(?:radiator|pipe|boiler|brakes?)\b",
    r"\bbleed(?:ing)?\s+the\s+(?:heating|radiators?)\b",
    r"\bblood\s+(?:test|pressure|donor|donation|type|sugar|group)\b", r"\bbloody\b",
    r"\bkill(?:ing)?\s+(?:time|the\s+weeds)\b", r"\bdead\s+(?:battery|phone|line|end|weight)\b",
    r"\bdie\s+cast\b", r"\bcut\s+(?:my|the)\s+(?:hair|nails|lawn|grass)\b", r"\bcut\s+it\s+out\b",
    r"\bwak(?:e|ing)\s+up\s+(?:in|before)\s+(?:the\s+morning|noon|\d)",
    r"\bchest\s+of\s+drawers\b", r"\bfire\s+me\b", r"\brained\s+off\b", r"\bstabbed\s+in\s+the\s+back\b",
    r"\bhit\s+the\s+nail\s+on\s+the\s+head\b", r"\bhead\s*-?\s*bang(?:ing|er|ers)\b",
    r"\b(?:i|im|i'?m|i'?ve)\b[^.?!]{0,20}\bbang(?:ing|ed)?\s+my\s+head\s+against\s+"
    r"(?:a\s+|the\s+)?(?:wall|brick|desk|door|table)\b",
    r"\bbang(?:ing|ed)?\s+(?:your|his|her)\s+head\s+against\s+(?:a\s+|the\s+)?(?:wall|brick|"
    r"desk|door|table)\b",
    r"\bhead\s+(?:over\s+heels|start|of\s+(?:the\s+)?(?:department|house|school|state)|count)\b",
    r"\bknock(?:ed|s)?\s+out\s+of\s+(?:the\s+)?(?:cup|competition|tournament|playoffs?|championship|league|competition|semis?|final|series|race)\b",
    r"\bknock(?:ed|s)?\s+(?:it|this|that|things)\s+out\s+of\s+the\s+park\b",
    r"\b(?:dog|puppy|pup|cat|kitten|horse|pony|rabbit|hamster|parrot|bird)\s+(?:is|was|seems|gets|looks|has\s+got)\s+(?:really\s+|very\s+|so\s+|a\s+bit\s+)?(?:scared|afraid|terrified|frightened|nervous|anxious)\b",
)

SCALD = (
    r"\b(?:burn\w*|scald\w*|boiling\s+water|hot\s+oil|steam|pan\s+of\s+"
    r"(?:water|oil|fat))\b[^.?!]{0,40}"
    r"\b(?:skin\s+)?(?:is\s+|gone\s+)?(?:peeling|peeled|peeling\s+off|waxy|charred|"
    r"blackened)\b",
    r"\b(?:kettle|saucepan|pan)\b[^.?!]{0,40}\b(?:skin|hand|arm|foot|feet|leg|face|wrist|"
    r"fingers?|chest|shoulder|thigh|thumb|toes?)\b[^.?!]{0,30}\b(?:peeling|peeled|waxy|charred|"
    r"blackened)\b",
    r"\b(?:skin|hand|arm|foot|feet|leg|face|wrist|fingers?|chest|shoulder|thigh|thumb|toes?)\b"
    r"[^.?!]{0,30}\b(?:peeling|peeled|waxy|charred|blackened)\b[^.?!]{0,30}\b(?:kettle|"
    r"saucepan|pan)\b",
    r"\b(?:went|gone|turned|turning|going|is|was)\s+white\b[^.?!]{0,40}"
    r"\b(?:burn\w*|scald\w*|boiling|hot\s+oil|steam|kettle|water\s+(?:hit|landed|went))\b",
    r"\b(?:burn\w*|scald\w*|boiling|hot\s+oil|steam|kettle)\b[^.?!]{0,40}"
    r"\b(?:went|gone|turned|turning|going|is|was)\s+white\b",
    r"\b(?:baby|toddler|child|son|daughter|kid|little\s+one)\b[^.?!]{0,40}"
    r"\b(?:kettle|saucepan|pan)\b[^.?!]{0,40}\b(?:over|on\s+(?:him|her|them)sel(?:f|ves)|"
    r"on\s+him|on\s+her)\b",
    r"\b(?:boiling|scalding)\s+(?:water|oil|fat|soup|tea|coffee)\b[^.?!]{0,30}"
    r"\b(?:over|on|onto)\s+(?:my|his|her|their|the)\s+(?:baby|toddler|child|son|daughter|kid)\b",
    r"\b(?:baby|toddler|child|son|daughter|kid|little\s+one)\b[^.?!]{0,40}"
    r"\b(?:boiling|scalding)\s+(?:water|oil|fat|soup|tea|coffee|kettle|pan)\b",
    r"\b(?:boiling|scalding)\s+(?:water|oil|fat|soup|tea|coffee|kettle|pan)\b[^.?!]{0,40}"
    r"\b(?:him|her|them)sel(?:f|ves)\b",
    r"\b(?:baby|toddler|child|kid|little\s+one|boy|girl)\b[^.?!]{0,30}"
    r"\b(?:scalded|burnt|burned)\s+(?:him|her|them)sel(?:f|ves)\b",
    r"\b(?:son|daughter|boy|girl|child|kid|niece|nephew)\b[^.?!]{0,40}"
    r"\b(?:scalded|burnt|burned)\b[^.?!]{0,50}"
    r"\b(?:screaming|screamed|crying|badly|all\s+over|blister\w*|peeling)\b",
)

HYPERBOLE_WISH = (
    r"\b(?:i'?m|im|i\s+am|i\s+feel|feeling)\s+"
    r"(?:(?:so|too|that|this|really|proper|bloody|absolutely|utterly|completely|dead)\s+)?"
    r"(?:tired|exhausted|bored|knackered|shattered|worn\s+out|sleepy|hungry|thirsty|hot|cold|"
    r"sore|aching|full|stuffed|busy|fed\s+up|embarrassed|mortified|old|poor|skint|stressed|"
    r"nervous|scared|itchy|sweaty|dirty|covered\s+in\s+\w+|hungover|hung\s?over|ill|poorly|"
    r"unwell|headachy|aching|achy|cream\s+crackered|croaky|snotty|sniffly)"
    r"\b[^.?!]{0,24}\b(?:wish|wished|wishing)\b",
    r"\b\w+(?:\s+\w+)?\s+(?:is|are|was|were)\s+(?:(?:so|too|that|this|really|proper|bloody)\s+)?"
    r"(?:boring|dull|slow|tiring|tedious|repetitive|long|hot|cold|loud|noisy|busy|quiet|"
    r"rubbish|crap|annoying|fiddly|heavy|stiff|itchy|sweaty|grim|depressing|pointless|"
    r"bad|worse|awful|terrible|horrible|dreadful|miserable|sore|painful|aching|achy|hungover|"
    r"hung\s?over|exhausting|stressful|tough|hard|chaotic|mental|hectic|shocking|useless)\b"
    r"[^.?!]{0,24}\b(?:wish|wished|wishing)\b",
    r"\b(?:my\s+)?\w+\s+(?:is|are|have\s+been)\s+killing\s+me\b[^.?!]{0,24}"
    r"\b(?:wish|wished|wishing)\b",
    r"\b(?:my|his|her|their)\s+(?:head|heads|feet|foot|knees?|back|legs?|arms?|shoulders?|hips?|"
    r"teeth|tooth|neck|stomach|belly|ankles?|wrists?|hands?|thighs?|calves|calf|elbows?|joints?|"
    r"shoulder\s+blade|lower\s+back|sciatica)\b[^.?!]{0,28}"
    r"\b(?:hurt|hurts|hurting|aching|aches?|sore|agony|killing\s+me|throbbing|stiff|bad)\b"
    r"[^.?!]{0,20}\b(?:wish|wished|wishing)\b",
)

PURSUIT_PLACE_HOME = (
    r"\b(?:outside|in\s+front\s+of|at\s+the\s+end\s+of|round\s+the\s+back\s+of)\s+"
    r"(?:my|our)\s+(?:house|home|flat|door|doorstep|front\s+door|window|gate|drive|driveway|"
    r"garden)\b",
    r"\b(?:banging|hammering|pounding|knocking|ringing)\s+(?:on|at)\s+(?:my|our|the)\s+"
    r"(?:door|doorbell|window|buzzer)\b",
    r"\b(?:waiting|waits|sat|sitting|stood|standing|parked|lurking|hiding|hovering|hanging\s+around)\s+"
    r"(?:right\s+|still\s+|now\s+)?(?:outside|in\s+front\s+of|at\s+the\s+end\s+of|"
    r"round\s+the\s+back\s+of)\s+(?:my|our)\s+(?:house|home|flat|door|doorstep|front\s+door|"
    r"window|gate|drive|driveway|garden)\b",
    r"\b(?:turned|turns|turning|showed|shows|showing)\s+up\s+(?:at|outside|in|on)\s+"
    r"(?:my|our)\s+(?:house|home|flat|door|doorstep|work|office|workplace|mum'?s|mum|mother'?s|"
    r"parents'?|school|gate)\b",
    r"\b(?:turned|turns|turning|showed|shows|showing)\s+up\s+(?:outside|unannounced|uninvited)\b",
    r"\b(?:at|on)\s+(?:my|our)\s+(?:front\s+)?(?:door|doorstep|buzzer)\b",
    r"\b(?:following|followed|follows)\s+(?:me|us)\b"
    r"(?!\s+(?:back\s+)?(?:on|at|in)\s+(?:instagram|insta|facebook|fb|twitter|x|tiktok|"
    r"socials?|social\s+media|linkedin|youtube|reddit|snapchat|strava|whatsapp|threads|"
    r"the\s+app|here))",
    r"\bstalk(?:s|ing|ed)\s+(?:me|us)\b"
    r"(?!\s+(?:back\s+)?(?:on|at|in)\s+(?:instagram|insta|facebook|fb|twitter|x|tiktok|"
    r"socials?|social\s+media|linkedin|youtube|reddit|snapchat|strava|whatsapp|threads))",
    r"\b(?:watching|watched|watches)\s+(?:my|our)\s+(?:house|home|flat)\b",
)

INJURY_HOW = (
    r"\b(?:hurt|hurting|injured|injuring|tweaked|strained|pulled|sprained|wrenched)\s+my\s*self\s+"
    r"(?:while\s+|when\s+)?(?:lifting|carrying|moving|shifting|digging|running|jogging|walking|"
    r"hiking|cycling|swimming|training|exercising|boxing|climbing|dancing|skating|skiing|rowing|"
    r"playing|gardening|cooking|chopping|cleaning|hoovering|decorating|painting|diy|stretching|"
    r"working\s+out|squatting|deadlifting|shopping|ice\s+skating)\b",
    r"\b(?:hurt|hurting|injured|injuring)\s+my\s*self\b[^.?!]{0,24}\b(?:in|at|on)\s+(?:the|my|a)\s+"
    r"(?:kitchen|garden|garage|gym|office|stairs|bathroom|shower|shed|workshop|pitch|field|"
    r"court|track|pool|sea|road|street|bus|train|ladder|roof|site|building\s+site|work)\b",
    r"\b(?:hurt|hurting|injured|injuring)\s+my\s*self\s+at\s+work\b",
    r"\b(?:hurt|hurting|injured|injuring)\s+my\s*self\s+(?:on|with)\s+(?:a|an|the|some)\s+"
    r"(?:\w+\s+){0,2}(?:door|shelf|drawer|car|bike|ladder|knife|drill|saw|pan|oven|hob|kettle|"
    r"weight|weights|barbell|dumbbell|box|bag|suitcase|pram|wheelchair|step|stair|curb|kerb)\b",
    r"\b(?:hurt|hurting|injured|injuring)\s+my\s*self\b[^.?!]{0,30}\band\s+(?:it|my\s+\w+)\s+"
    r"(?:still\s+)?(?:hurts|aches|is\s+sore|swelled|swollen|is\s+bruised)\b",
    r"\b(?:fell|fallen|falling|tripped|slipped)\b[^.?!]{0,32}\b(?:hurt|injured|cut|cutting|"
    r"nicked|sliced|grazed|scraped)\s+my\s*self\b",
    r"\b(?:hurt|hurting|injured|injuring|cut|cutting|nicked|sliced)\s+my\s*self\s+"
    r"(?:falling|tripping|slipping)\b",
)

LIPS_SWELL_BARE = (
    r"\b(?:my|his|her|their)\s+(?:lips?|tongue|throat|face)\s+(?:are\s+|is\s+|'s\s+)?"
    r"(?:swelling|swollen|swelled|puff\w*\s+up|puffed\s+up|puffing\s+up|blowing\s+up)\b",
    r"\b(?:my|his|her|their)\s+(?:throat|tongue|uvula)\b[^.?!]{0,15}\b(?:is|'s|feels?)\s+"
    r"(?:closing|tight|swelling|swollen)\b",
    r"\b(?:my|his|her|their)\s+(?:uvula)\s+(?:is\s+|'s\s+)?(?:swelling|swollen)\b",
    r"\b(?:stung|stings?)\b[^.?!]{0,40}\b(?:dizzy|dizziness|faint\w*|"
    r"light\s?headed|clammy)\b",
    r"\b(?:dizzy|dizziness|faint\w*|light\s?headed|clammy)\b[^.?!]{0,40}\b(?:stung|stings?)\b",
    r"\b(?:stung|stings?)\b[^.?!]{0,40}\b(?:throat|tongue)\b[^.?!]{0,12}"
    r"\b(?:feels?|is|going|getting)\s+(?:a\s+bit\s+|a\s+little\s+|really\s+|very\s+|so\s+)?"
    r"(?:funny|odd|weird|strange|thick|tickl\w*|itch\w*)\b",
    r"\b(?:throat|tongue)\b[^.?!]{0,12}\b(?:feels?|is)\s+(?:a\s+bit\s+|a\s+little\s+|"
    r"really\s+|very\s+|so\s+)?(?:funny|odd|weird|strange|thick|tickl\w*|itch\w*)\b"
    r"[^.?!]{0,40}\b(?:stung|stings?)\b",
    r"\b(?:throat|tongue)\b[^.?!]{0,15}\b(?:tickl\w*|itches|itching)\b[^.?!]{0,40}"
    r"\b(?:stung|stings?)\b",
    r"\b(?:stung|stings?)\b[^.?!]{0,40}\b(?:throat|tongue)\b[^.?!]{0,15}"
    r"\b(?:tickl\w*|itches|itching)\b",
)

DOG_ATTACK = (
    r"\bdogs?\b.{0,30}\b(?:attacking|mauling|savaging|biting|went\s+for)\b"
    r"(?!\s+(?:his|her|its|their|the|a)\s+(?:paw|paws|tail|leg|legs|foot|feet|ear|ears|fur|"
    r"skin|lead|fence|toy|bed|nappy|blanket|cushion))\b",
    r"\bdogs?\s+(?:has\s+|have\s+)?bit\s+(?:me|my|his|her|him|them|a\s+(?:child|kid|baby))\b",
    r"\b(?:bit|bitten)\s+by\s+a\s+dog\b",
    r"\b(?:attacking|mauling)\s+(?:him|her|them|me|my\s+\w+)\b.{0,20}\bdogs?\b",
    r"\b(?:being\s+)?attacked\s+by\s+(?:a\s+)?dogs?\b",
    r"\bdogs?\b.{0,25}\b(?:is|are|was|were)?\s*(?:going\s+for|after|lunging\s+at|snapping\s+at|growling\s+at)\s+(?:me|my|him|her|them)\b",
    r"\bdogs?\b[^.?!]{0,30}\b(?:bit|bitten|biting|nipped|nipping|snapped\s+at)\b[^.?!]{0,25}"
    r"\b(?:me|us|my\s+(?:hand|hands|arm|arms|leg|legs|foot|feet|face|finger|fingers|head|"
    r"shoulder|wrist|ankle|neck|cheek|nose|toe|toes|chin))\b",
)

_A_LOW_FIGURE = r"(?:0\.[1-9]|[1-3](?:\.\d)?)(?:\s*mmol)?\b"

_A_READING_NOUN = r"(?:(?:blood\s+)?sugars?|(?:blood\s+)?glucose)"

SUGAR_READING_LOW = (
    r"\b" + _A_READING_NOUN + r"\s+(?:levels?\s+|readings?\s+)?"
    r"(?:is|was|are|at|reads?|reading|of|:)\s*" + _A_LOW_FIGURE,
    r"\bblood\s+sugars?\s+(?:levels?\s+|readings?\s+)?(?:of\s+|:\s*)?" + _A_LOW_FIGURE,
    r"\b(?:blood|my|his|her|their|the)\s+glucose\s+(?:levels?\s+|readings?\s+)?"
    r"(?:of\s+|:\s*)?" + _A_LOW_FIGURE,
    r"\bglucose\s+(?:levels?|readings?)\s+(?:is\s+|was\s+|of\s+|:\s*)?" + _A_LOW_FIGURE,
)

HYPO_SIGN = (
    r"\b(?:im|i'?m|am|is|are|'s|'re|hes|he'?s|shes|she'?s|theyre|they'?re|youre|you'?re|"
    r"was|were)\s+(?:having|getting|going\s+into)\s+(?:a\s+|another\s+)?hypo\b",
    r"\b(?:and|then|now)\s+(?:(?:hes|he'?s|shes|she'?s|theyre|they'?re|im)\s+)?"
    r"(?:having|getting|going\s+into)\s+(?:a\s+|another\s+)?hypo\b",
    r"\bthink\s+(?:i'?m|im|i\s+am)\s+(?:having|getting)\s+(?:a\s+|another\s+)?hypo\b",
    r"\bconfus\w*", r"\bdisorient\w*", r"\bsweat\w*", r"\bclammy\b", r"\bshak\w*",
    r"\btrembl\w*", r"\bjitter\w*", r"\bdrows\w*", r"\b(?:very\s+)?sleepy\b",
    r"\bslurr\w*", r"\bacting\s+(?:drunk|odd|strange|weird|pissed|funny)\b",
    r"\bnot\s+(?:him|her|them|himself|herself|themselves)\b", r"\bwobbly\b",
    r"\b(?:pale|grey|gray|white)\s+as\s+a\s+sheet\b", r"\b(?:won'?t|wont)\s+wake\b",
    r"\bfeels?\s+(?:faint|funny|wobbly|drunk)\b", r"\bcan'?t\s+stay\s+awake\b",
    r"\b(?:passed|passing)\s+out\b", r"\b(?:blacked|blacking)\s+out\b", r"\bout\s+cold\b",
    r"\bfaint\w*", r"\bcollaps\w*", r"\bkeel\w*\s+over\b", r"\ba\s+fit\b",
    r"\bseizure\w*", r"\bconvuls\w*", r"\bcoma\b", r"\bunconscious\b", r"\bunresponsive\b",
    r"\bnot\s+making\s+(?:any\s+)?sense\b", r"\bgibberish\b",
    r"\b(?:talking|talked|saying)\s+(?:nonsense|rubbish)\b",
    *SUGAR_READING_LOW,
    r"\b(?:blood\s+)?(?:sugars?|glucose)\s+(?:is\s+|was\s+|has\s+|have\s+|had\s+|levels?\s+(?:is\s+|are\s+)?)?"
    r"(?:low|dropped|dropping|dipped|crashing|too\s+low)\b",
    r"\b(?:blood\s+)?(?:sugars?|glucose)\s+level\w*\s+(?:is\s+|are\s+)?(?:low|dropping|dropped)\b",
    r"\b(?:blood\s+)?glucose\s+(?:is\s+|was\s+)?(?:falling|fallen|plummet\w*)\b",
)

SELF_HARM_REPEAT_CAUSE = (
    r"\b(?:boiler|wifi|wi-?fi|internet|router|broadband|signal|connection|car|van|engine|motorbike|"
    r"bike|mower|lawnmower|laptop|phone|computer|screen|tv|telly|radio|fridge|freezer|fan|"
    r"washing\s+machine|dishwasher|dryer|heater|radiator|heating|oven|hob|cooker|grill|kettle|"
    r"toaster|iron|straighteners|hairdryer|hair\s+dryer|light|lights|bulb|plug|socket|charger|"
    r"cable|battery|drill|saw|knife|blade|glass|bleach|acid|pan|pot|plate|shower|tap|mattress|"
    r"brakes?|clutch|gears?|fuse|power|electricity|sun|sunburn|candle|lighter|fire|barbecue|"
    r"barbeque|stove|radiator|ice|snow|shelf|shelves|cupboard|ceiling|door|desk|chair|sofa|"
    r"table|worktop|counter|bed|floor|stairs|nails?)\b",
    r"\b(?:eczema|psoriasis|dandruff|rash|itch\w*|dry\s+skin|allergy|allergic|hives|heating|"
    r"in\s+the\s+night|at\s+night|in\s+my\s+sleep)\b",
    r"\b(?:lifting|carrying|moving|shifting|digging|painting|gardening|running|jogging|walking|"
    r" cycling|swimming|exercising|training|playing|football|rugby|netball|gym|workout|squats?|"
    r"deadlifts?|weights|boxes?|furniture|bags?|shopping|hoovering|cleaning|scrubbing|typing|"
    r"at\s+work|in\s+the\s+garden)\b",
    r"\b(?:after\s+(?:work|the\s+gym|a\s+run|a\s+walk|lifting|football|netball|rugby|a\s+shift|"
    r"the\s+shopping)|when\s+i\s+(?:lift|run|cycle|walk|play|train|work\s+out|carry|exercise|"
    r"climb|swim|dig|garden))\b",
)

FOLLOW_UP = (
    r"\bwhile\s+(?:we|i|they|you)\s+wait\b", r"\bwhat\s+(?:do|should)\s+(?:i|we)\s+do\b",
    r"\bwhat\s+now\b", r"\banything\s+else\b", r"\bis\s+(?:that|it|this)\s+(?:ok|okay|right|normal|safe|dangerous)\b",
    r"\bis\s+it\s+safe\s+to\b", r"\bthe\s+ambulance\b", r"\bthey'?re\s+(?:coming|on\s+their\s+way)\b",
    r"\bhelp\s+is\s+(?:coming|on\s+the\s+way)\b", r"\bstill\s+waiting\b",
    r"\bshould\s+i\s+(?:use|give|move|leave|go|call|keep|do|put|take|wash|clean|rinse|cover|wrap|bandage)\b",
    r"\bcan\s+i\s+(?:give|move|leave|go|use|do|put|take|wash|clean|rinse|cover|wrap|bandage|walk|stand|sit|lie|help|carry)\b",
    r"\bwhat\s+(?:else\s+)?can\s+i\s+do\b", r"\bkeep\s+(?:them|him|her)\s+(?:warm|still|awake)\b",
    r"\b(?:cpr|dispatcher|call\s+handler)\b", r"\b(?:breathing|feels?|looks?|seems?)\s+(?:better|easier|worse|normally|again)\b",
    r"\bthey\s+(?:seem|look|are)\s+(?:better|worse|okay|ok)\b",
    r"\b(?:i'm|im|we're|we\s+are|i\s+am)\s+(?:outside|out|safe|clear)\b",
    r"\b(?:fire\s+(?:brigade|service|fighters?)|paramedics?|ambulance)\b",
    r"\b(?:he|she|they|it)(?:'s|'re|\s+is|\s+are)\s+(?:awake|breathing|okay|ok)\b",
    r"\b(?:it|the\s+bleeding)\s+(?:has\s+)?stopped\b",
    r"\b(?:called|rang|phoned)\s+(?:999|911|112)\b", r"\bon\s+(?:the\s+phone|hold)\b",
    r"\b(?:still|really)\s+(?:scared|frightened|terrified|afraid|shaky|panicking|panicky)\b",
    r"\bstill\s+(?:soaking|bleeding|coming|pouring)\b", r"\bsoaking\s+through\b",
    r"\bit'?s\s+still\s+\w+ing\b",
    r"\bshould\s+i\s+(?:try|open|shut|close|turn|grab|hold|press|cover|warm|sit|lie|stand|walk|drive|eat|drink|wake|ring|phone|tell|say|text|message|put|take|wash|clean|rinse|wrap|bandage)\b",
    r"\bcan\s+i\s+(?:open|shut|close|turn|give|move|go|drive|eat|drink|wake|ring|phone|put|take|wash|clean|rinse|cover|wrap|bandage|walk|stand|sit|lie|help|leave|try|carry|hold|press)\b",
    r"\bis\s+it\s+(?:ok|okay|safe|alright|fine)\s+to\b",
)

LIMP_ONGOING = (
    r"\b(?:my|his|her|their|the|your)\s+ms\b", r"\bmultiple\s+sclerosis\b",
    r"\bparkinsons?\b", r"\bparkinson'?s\b", r"\b(?:brain|head|spinal)\s+injur\w+",
    r"\bcerebral\s+palsy\b", r"\bspina\s+bifida\b", r"\bmuscular\s+dystrophy\b",
    r"\bamputat\w+\b",
    r"\bprosthe\w+\s+(?:leg|legs|limb|limbs|knee|knees|ankle|ankles|foot|feet|hip|hips|"
    r"thigh|thighs|calf|calves)\b",
    r"\b(?:leg|legs|limb|limbs|knee|knees|ankle|ankles|foot|feet|hip|hips|thigh|thighs|"
    r"calf|calves)\s+prosthe\w+",
    r"(?<!eye )(?<!ocular )\bprosthe\w+\b(?!\s+(?:eye|eyes|eyeball|socket))",
    r"\bpolio\b", r"\bdrop\s+foot\b",
    r"\bsince\s+(?:he|she|they|i)\s+(?:was|were)\s+(?:little|born|a\s+baby|small)\b",
    r"\bsince\s+(?:birth|childhood|i\s+was\s+born|he\s+was\s+born|she\s+was\s+born)\b",
    r"\b(?:all|all\s+of)\s+(?:my|his|her|their)\s+life\b",
    r"\bborn\s+(?:blind|with)\b",
)

SHOULD_I_CALL = (
    r"^[\s,]*(?:so|ok|okay|right|well|then)?[\s,]*"
    r"(?:do\s+you\s+think|i\s+think|honestly|really)?[\s,]*"
    r"(?:i|we)?\s*(?:should|shall|do)\s*(?:i|we)?\s*(?:call|ring|phone|dial)\s+(?:an?\s+)?"
    r"(?:ambulance|999|911|112|emergency\s+services)\b"
    r"[\s?!.]*(?:please|thanks|thank\s+you|or\s+not|yes\s+or\s+no)?[\s?!.]*$",
    r"^[\s,]*(?:should|shall|do)\s+(?:i|we)\s+(?:call|ring|phone|dial)\s+(?:an?\s+)?"
    r"(?:ambulance|999|911|112|emergency\s+services)\b[^?.!]*"
    r"\b(?:or|otherwise)\b[^?.!]*[?!.]*$",
    r"^[\s,]*(?:is|isnt|isn'?t)\s+(?:that|this|it)\s+(?:really\s+)?(?:a\s+)?"
    r"(?:999|911|112)\s+job\b[\s?!.]*$",
    r"^[\s,]*(?:so|ok|okay|right|well|then)?[\s,]*"
    r"(?:do\s+you\s+think|i\s+think|honestly|really)?[\s,]*"
    r"(?:should|shall|do)?\s*(?:i|we)?\s*(?:need\s+to|have\s+to|bother(?:\s+\w+)?)\s*"
    r"(?:calling|ringing|phoning|dialing|dialling|call|ring|phone|dial)?[\s,]*\s*(?:an?\s+)?"
    r"(?:ambulance|999|911|112|emergency\s+services)\b"
    r"[\s?!.]*(?:please|thanks|or\s+not|yes\s+or\s+no)?[\s?!.]*$",
    r"^[\s,]*(?:so|ok|okay|right|well|then)?[\s,]*"
    r"(?:do\s+you\s+think|i\s+think|honestly|really)?[\s,]*"
    r"(?:do\s+i\s+|do\s+we\s+|i\s+)?(?:need|needs|want|wants)\s+(?:an?\s+)?"
    r"(?:ambulance|999|911|112|emergency\s+services)\b"
    r"[\s?!.]*(?:please|thanks|or\s+not|yes\s+or\s+no)?[\s?!.]*$",
)

NOT_JUST_A_NEAR_THING = (
    r"\b(?:i\s+)?(?:just\s+)?(?:cant|can'?t|couldnt|couldn'?t)\s+"
    r"(?:do\s+(?:this|it)|take\s+(?:it|this)|go\s+on|carry\s+on|keep\s+going|keep\s+on)\s*"
    r"(?:any\s?more|anymore)\b",
    r"\b(?:i\s+)?(?:just\s+)?(?:don'?t|dont|do\s+not)\s+care\s+"
    r"(?:if\s+i\s+(?:live|die|wake|make\s+it|survive)\b|any\s?more\b|anymore\b|"
    r"about\s+(?:anything|myself|it)\b|whether\s+i\s+(?:live|die)\b)",
    r"\b(?:i\s+)?(?:just\s+)?(?:feel|feeling|felt|am|im)\s+(?:so\s+|really\s+|totally\s+)?"
    r"(?:empty|numb|hollow|dead\s+inside)\b",
    r"\bwish\s+(?:i|it|that\s+i|the\s+car|that\s+car)\b[^.?!]{0,24}"
    r"\b(?:crashed|died|gone\s+through|not\s+woken|killed\s+me|hit\s+me|"
    r"finished\s+it|done\s+it|succeeded|worked)\b",
    r"\b(?:would|would'?ve|would\s+have)\s+(?:be\s+)?(?:better|easier)\s+if\s+i\b",
    r"\b(?:i\s+)?(?:honestly\s+)?(?:don'?t|dont)\s+want\s+to\s+be\s+here\b",
    r"\bnot\s+worth\s+(?:being\s+here|carrying\s+on|going\s+on)\b",
    r"\b(?:havent|have\s+not)\s+(?:got\s+)?(?:anything|much)\s+left\b",
    r"\b(?:i\s+)?(?:really\s+|just\s+|honestly\s+|so\s+)?hate\s+my\s*self\b",
    r"\bwish\s+(?:i|that\s+i)\s+(?:wasnt|wasn'?t|werent|weren'?t|was\s+not|were\s+not)\b",
    r"\b(?:want|wanted|wanna|wishing|wish)\s+(?:to\s+)?(?:disappear|vanish|"
    r"stop\s+existing|cease\s+to\s+exist|not\s+exist|be\s+gone|be\s+dead|be\s+here\s+any\s?more)\b",
    r"\b(?:cant|can'?t|couldnt|couldn'?t)\s+(?:take|stand)\s+(?:it|this|much\s+more)\b",
    r"\bnot\s+(?:wake|waking)\s+up\b",
)

LIMP_PERSON = (
    r"\b(?:i|he|she|they|we)\s+(?:am|is|are|was|were|have\s+been|has\s+been)\s+"
    r"(?:still\s+|now\s+|really\s+|badly\s+|left\s+)?limp(?:ing)?\b",
    r"\bmy\s+(?:son|daughter|child|boy|girl|kid|toddler|baby|husband|wife|partner|mum|mom|dad|"
    r"mother|father|nan|grandad|grandma|grandson|granddaughter|niece|nephew|friend|sister|brother)"
    r"\s+(?:is|was|keeps?|has\s+been|had\s+been)\s+(?:still\s+)?limp(?:ing)?\b",
    r"\b(?:son|daughter|child|boy|girl|kid|toddler|baby|husband|wife|partner|mum|mom|dad|mother|"
    r"father|nan|nana|grandad|grandma|grandson|granddaughter|niece|nephew|friend|sister|brother)"
    r"\s+limp(?:s|ed)\b",
    r"\b(?:i|he|she)\s+limp(?:s|ed)\b",
    r"\b(?:keeps?\s+limping|started\s+limping|stop\s+limping|stopped\s+limping|been\s+limping|"
    r"still\s+limping|stop\s+(?:\w+\s+){0,2}limping)\b",
    r"\b(?:my|his|her|their|our)\s+(?:\w+\s+){0,2}limp(?:ing)\b",
    r"\b(?:has|have|had|has\s+got|have\s+got|had\s+got|developed|developing|been\s+left\s+with)"
    r"\s+(?:a\s+|an\s+|this\s+|that\s+)?(?:bad\s+|slight\s+|really\s+|sore\s+)?limp\b",
    r"\b(?:walks|walking|walked|hobbles|hobbling)\s+with\s+(?:a\s+|this\s+)?limp\b",
    r"\bgot\s+(?:a\s+|this\s+)?(?:bad\s+|slight\s+)?limp\b",
    r"\bwith\s+(?:a\s+)?(?:bad\s+|slight\s+)?limp\b",
    r"\b(?:leg|knee|ankle|foot|hip|back)\s+(?:is\s+)?limp(?:ing)?\b",
)

PURSUIT_FINE = (
    r"\b(?:to|with|for)\s+(?:the\s+)?(?:kids|children|child|dog|stuff|things|bags)\b",
    r"\b(?:dropping|dropped|drop)\s+(?:off|the|it|them)\b",
    r"\b(?:picking|picked|pick)\s+(?:up|the|them)\b",
    r"\b(?:handover|hand\s*over|collecting|collected|collect)\b",
    r"\b(?:comes|coming|came)\s+(?:to|for|round)\b",
    r"\b(?:pick(?:ing|ed|s)?\s+(?:me|us|him|her|them)\s+up|pick\s*-?\s*up|"
    r"lift\s+(?:home|to\s+work|back)|give\s+(?:me|us|him|her|them)\s+a\s+lift|"
    r"for\s+a\s+lift|to\s+be\s+let\s+in|let\s+(?:me|us|him|her)\s+in|"
    r"locked\s+(?:out|himself\s+out|herself\s+out))\b",
    r"\b(?:follow\w*|stalk\w*)\s+(?:me|us)\b[^.?!]{0,12}\b(?:instagram|insta|facebook|fb|"
    r"twitter|tiktok|socials?|social\s+media|linkedin|youtube|reddit|snapchat|strava|whatsapp|"
    r"threads)\b",
    r"\b(?:husband|wife|partner|boyfriend|girlfriend|fiance|fiancee)\b[^.?!]{0,30}"
    r"\b(?:outside|at|near|by)\s+(?:the|her|his|their)\s+(?:school|work|office|nursery|"
    r"college|uni|university|gates?)\b",
    r"\b(?:scared|frightened|worried|afraid|panicking|nervous)\b[^.?!]{0,30}\b(?:late|"
    r"on\s+time|in\s+trouble)\b",
    r"\b(?:shouting|yelling|screaming)\s+at\s+(?:the\s+)?(?:football|telly|tv|match|game|"
    r"radio|news|ref|referee)\b",
)

LIMB_IS_A_THING = (
    r"\b(?:arm|leg)\s+(?:of|on)\s+(?:my|the|our|his|her|their|your)\s+"
    r"(?:[\w-]+\s+){0,2}"
    r"(?:glasses|specs|spectacles|sunglasses|monitor|screen|telly|tv|lamp|light|tripod|mirror|"
    r"chair|table|desk|sofa|settee|stool|bed|shelf|shelves|gate|door|bike|scooter|guitar|"
    r"violin|rack|stand|pram|pushchair|buggy|"
    r"jeans|trousers|pants|joggers|jogging bottoms|leggings|shorts|chinos|cords|combats|"
    r"pyjamas|pyjama bottoms|pjamas|pjs|tights|skirt|dress|dresses|shirt|shirts|coat|coats|"
    r"jacket|jackets|sock|socks|boot|boots|shoe|shoes|slipper|slippers)\b",
    r"\b(?:glasses|specs|spectacles|sunglasses|monitor|screen|chair|table|desk|sofa|settee|"
    r"stool|lamp|tripod|mirror|pram|pushchair|buggy|guitar|violin|bike|scooter|"
    r"jeans|trousers|leggings|shorts|pyjamas|jacket|coat|shirt|dress)\b"
    r"(?:'s)?\s+(?:arm|leg)\b",
    r"\b(?:the|a|my|our|his|her|their|your)\s+(?:glasses|specs|spectacles|sunglasses|chair|"
    r"table|desk|sofa|settee|stool|lamp|monitor|screen|tripod|mirror|pram|pushchair|buggy|"
    r"jeans|trousers|leggings|shorts|pyjamas|jacket|coat|shirt|dress)\b"
    r"[^.?!]{0,20}\b(?:bent|deformed)\b",
    r"\b(?:trouser|trousers|jeans|jean|pyjama|pyjamas|pajama|pajamas|jacket|shirt|coat|sleeve|"
    r"chair|table|sofa|settee|desk|stool|lamp|monitor|screen|glasses|door|gate)\s+"
    r"(?:leg|legs|arm|arms)\b",
)

HIT_IN_FUN_HARD = (
    r"\bi\s+(?:just\s+|was\s+|were\s+|am\s+)?laugh(?:ing|ed|s)?\b",
    r"\bi\s+(?:just\s+|was\s+|were\s+|am\s+)?(?:only\s+|just\s+)?(?:joking|kidding|kiddin)\b"
    r"(?![^.?!]*\bwe\s+(?:both\s+)?(?:laughed|were\s+laughing|laughing)\b)",
    r"\bwhile\s+(?:i\s+was\s+)?(?:joking|kidding)\b"
    r"(?![^.?!]*\bwe\s+(?:both\s+)?(?:laughed|were\s+laughing|laughing)\b)",
    r"\bit\s+(?:stung|stings?|hurt|hurts|smarts?|throbs?|burn(?:s|ed)?)\b",
    r"\bduring\s+(?:the\s+)?play\b",
    r"\b(?:face|head|throat|neck|nose|eyes?|jaw|ribs?|stomach|belly|genitals?|chest)\b",
    r"\b(?:hard|harder|really\s+hurt|properly|painful|bruis\w*|blood|bled|bleeding|mark)\b",
    r"\b(?:afraid|scared|frightened|terrified)\b",
    r"\b(?:wouldn'?t\s+stop|didn'?t\s+stop|kept\s+(?:on|going)|not\s+the\s+first\s+time|"
    r"every\s+day|all\s+the\s+time)\b",
    r"\b(?:every\s+(?:single\s+)?(?:time|week|night|month|birthday)|each\s+time|"
    r"whenever|constantly|regularly|"
    r"always\s+(?:hits?|hit|slapp?(?:s|ped)?|punch(?:es|ed)?|kick(?:s|ed)?|shov(?:es|ed)|"
    r"push(?:es|ed)|beats?|hurts?))\b",
    r"\b(?:knife|belt|bottle|weapon|stick|pan|chair|bat)\b",
    r"\b(?:said|says|saying|say|called|calls|calling|claimed|claims|claiming|told|tells|telling)"
    r"\b[^.?!]{0,25}\b(?:joke|joking|laugh|laughing|fun|banter|mess(?:ing)?\s+about)\b",
    r"\b(?:it\s+was|it\s+were)\s+(?:only\s+|just\s+|all\s+)?(?:a\s+)?"
    r"(?:joke|joking|banter|laugh)\b",
    r"\b(?:only|just)\s+joking\b",
    r"\b(?:down\s+the\s+stairs|downstairs|fell|fallen|falling|fell\s+over|tripped\s+me|"
    r"knocked\s+me\s+(?:over|down)|off\s+the\s+(?:ladder|chair|bike)|into\s+the\s+road)\b",
)

WATER_DANGER = (
    r"\b(?:under|below)\s+(?:the\s+|his\s+|her\s+|their\s+)?(?:water|surface)\b",
    r"\b(?:fell|fallen|falls?|went|goes|gone|slipped|slips?|dropped|drops?|jumped|jumps?|pushed|"
    r"pushed\s+in|tipped|tumbled|sank|sunk|wa(s|s)\s+in|were\s+in|is\s+in|went\s+in)\b"
    r"[^.?!]{0,20}\b(?:in|into)\s+(?:the\s+)?(?:water|pond|river|lake|sea|canal|pool|stream|"
    r"reservoir|loch|harbour|harbor|lagoon|deep\s+end|shallow\s+end)\b",
    r"\b(?:went\s+under|goes\s+under|gone\s+under|disappeared\s+under|underwater)\b",
    r"\b(?:sank|sunk|sinking)\s+(?:under|below|to\s+the\s+bottom)\b",
    r"\b(?:sank|sunk|sinking)\s+(?:in|into)\s+the\s+(?:water|pond|river|lake|sea|canal|pool|"
    r"stream|reservoir|loch|harbour|harbor|lagoon)\b",
    r"\b(?:slipped|slips?|fell|fallen|sank|sunk|tipped|tumbled|rolled)\s+under\b"
    r"[^.?!]{0,25}\b(?:bath|tub)\b",
    r"\b(?:bath|tub)\b[^.?!]{0,20}\b(?:went|goes|gone|sank|sunk|slips?|slipped|fell|fallen)"
    r"\s+under\b",
    r"\bunder\s+for\s+(?:\d+|a\s+few|several|two|three|four|five|ten|twenty|thirty)\s*"
    r"(?:seconds?|secs?|minutes?|mins?)\b",
    r"\bface\s+down\b[^.?!]{0,20}\b(?:water|bath|tub|pool|pond)\b",
    r"\bin\s+the\s+water\b[^.?!]{0,30}\bcan'?t\s+see\b",
    r"\b(?:can'?t|cant|couldn'?t|could\s+not)\s+see\b[^.?!]{0,25}\b(?:in|under)\s+"
    r"(?:the\s+)?(?:water|pool|sea|pond|river|lake|canal)\b",
    r"\b(?:pulled|drags?|dragged|lifted|hauled|got|gets|getting|fished)\s+(?:[\w']+\s+){0,3}"
    r"out\s+of\s+the\s+(?:water|pool|sea|pond|river|lake|canal)\b",
    r"\bnearly\s+drowned\b[^.?!]{0,20}\b(?:water|pond|river|lake|sea|pool|canal|reservoir|"
    r"loch|deep\s+end|bath|tub)\b",
)

_PET_DAMAGE_THING = (
    r"(?:sofas?|couches?|settees?|armchairs?|chairs?|stools?|seats?|curtains?|blinds?|carpets?|"
    r"rugs?|mats?|bedding|duvet|pillows?|cushions?|blankets?|throws?|towels?|linen|"
    r"clothes|jumpers?|cardigans?|shirts?|dress(?:es)?|trousers|jeans|skirts?|coats?|jackets?|"
    r"sleeves?|socks?|tights|shoes?|slippers?|trainers?|boots?|laces?|shoelaces?|hats?|scarves?|"
    r"bags?|rucksacks?|backpacks?|handbags?|wallets?|purses?|phones?|mobiles?|cables?|chargers?|"
    r"wires?|leads?|laptops?|keyboards?|mice|remotes?|tvs?|televisions?|screens?|monitors?|"
    r"headphones|speakers?|wallpaper|walls?|doors?|doorways?|doorframes?|skirtings?|paint|floors?|"
    r"floorboards?|tables?|desks?|shelves|shelf|bookcases?|cupboards?|wardrobes?|cabinets?|"
    r"worktops?|counters?|sideboards?|garden|lawn|grass|fences?|gates?|sheds?|decking|patios?|"
    r"plants?|flowers?|houseplants?|trees?|bark|scratch\s*posts?|posts?|toys?|tunnels?|carpet|"
    r"furniture|woodwork|paintwork|bannister|banister|radiator|switch|light\s*switch)"
)

BLEEDING_SMALL = (
    r"\b(?:he|she|they|his|her|their|my\s+(?:dad|mum|mom|father|mother|son|daughter|child|kid|baby|"
    r"husband|wife|partner|brother|sister|nan|gran|grandma|grandad|friend|neighbour|neighbor|boy|"
    r"girl|man|woman|lad|mate|colleague))\b.{0,25}"
    r"\b(?:is|are|'s|was|keeps?|has\s+been)\s+bleeding\b(?!\s+(?:me\s+)?(?:dry|white))",
    r"\b(?:my|his|her|their|your)\s+(?:hand|arm|leg|foot|head|finger|thumb|wrist|knee|elbow|face|"
    r"lip|scalp|shin|shoulder|ear|cheek|mouth|brow|eyebrow|chin|jaw|forearm|upper\s+arm|"
    r"thigh|calf|palm|heel|toe|knuckle|knuckles|belly|chest|neck|back)\s+"
    r"(?:is\s+|are\s+|keeps?\s+|started\s+|won'?t\s+stop\s+)?(?:bleeding|bled)\b",
    r"\b(?:cut|sliced|nicked|gashed|slashed)\b.{0,25}"
    r"\b(?:won'?t|wont|doesn'?t|didn'?t|keeps?)\s+stop\s+bleeding\b",
    r"\b(?:dogs?|cats?|pupp(?:y|ies)|kittens?|pets?)\b"
    r".{0,25}"
    r"\b(?:bit|bitten|scratched|clawed|claw|nicked)\b.{0,20}"
    r"\b(?:(?:me|us)\b|(?:him|her|them)\b(?!\s+\w)|"
    r"(?:my|his|her|their|your|our)\s+"
    r"(?!(?:\w+['’]s\s+)?(?:[a-z]+\s+){0,2}(?:" + _PET_DAMAGE_THING + r")\b)\w)",
)

A_TOOTH_OWNER = (r"(?:my|his|her|their|the|your|our|a|an|son'?s|daughter'?s|kid'?s|child'?s|"
                 r"husband'?s|wife'?s|partner'?s|friend'?s|mum'?s|dad'?s)")

TOOTH_OUT = (
    r"\b" + A_TOOTH_OWNER + r"\s+(?:front\s+|back\s+|adult\s+|baby\s+|milk\s+)?"
    r"(?:tooth|teeth)\b[^.?!]{0,20}"
    r"\b(?:knock(?:ed|s|ing)?\s+out|came\s+out|comes?\s+out|fell\s+out|falls?\s+out|"
    r"is\s+hanging)\b",
    r"\b(?:knock|knocks|knocked|knocking|kick|kicks|kicked|kicking|punch|punches|punched|"
    r"punching|smash|smashes|smashed|smashing)\s+"
    r"(?:my|his|her|their|our|your|a|an|out\s+)\s*(?:front\s+|back\s+)?tooth\b",
    r"\b(?:knock|knocks|knocked|knocking|kicking|kicked|punch|punched|punching|smash|smashed|"
    r"smashing)\s+(?:my|his|her|their|the|our|your|out\s+)\b[^.?!]{0,18}\bteeth\b",
    r"\b(?:knocked|came|fell)\s+(?:out\s+)?(?:\w+\s+){0,4}(?:teeth|tooth)\b",
    r"\b(?:teeth|tooth)\s+(?:got\s+|were\s+|was\s+|both\s+)?(?:knocked|came|fell)\s+out\b",
)

A_TOOTH_DAMAGED = (r"(?:chips?|chipped|chipping|cracks?|cracked|cracking|breaks?|breaking|broke|"
                   r"broken|busts?|busted|busting|snaps?|snapped|snapping)")

TOOTH_CHIPPED = (
    r"\b" + A_TOOTH_OWNER + r"\s+(?:front\s+|back\s+|baby\s+|adult\s+)?"
    r"(?:tooth|teeth)\b[^.?!]{0,20}\b" + A_TOOTH_DAMAGED + r"\b(?!\s*out)",
    r"\b" + A_TOOTH_DAMAGED + r"\s+" + A_TOOTH_OWNER +
    r"\s+(?:front\s+|back\s+|baby\s+|adult\s+)?tooth\b(?!\s*out)",
)

WEIGHT_JOINT = (
    r"\b(?:ankle|ankles|knee|knees|foot|feet|heel|heels|toe|toes|leg|legs|wrist|wrists|hand|"
    r"hands|elbow|elbows|shoulder|shoulders|finger|fingers|thumb|thumbs)\b",
)

BODY = (
    r"(?:hands?|fingers?|fingertips?|thumbs?|arms?|wrists?|elbows?|tongue|mouth|throat|lips?|"
    r"faces?|cheeks?|nose|ears?|eyes?|feet|foot|toes?|legs?|knees?|shins?|chest|backs?|skin|palms?|"
    r"knuckles?|head|scalp|neck|stomach|belly)\b"
)

SCORCHED_A_PERSON = (
    r"\b(?:scorch(?:ed|es|ing)?|singe(?:d|s|ing)?|scold(?:ed|ing))\s+" r"(?:my|his|her|their|your|our|the|a)\s+" r"(?:(?:left|right|own|whole|poor|other|inner|top)\s+)?" + BODY,
    r"\b(?:a|an|the|this|that)\s+" r"(?:bad|nasty|small|minor|little|sore|red|fresh|ugly)?\s*" r"(?:scorch|singe)(?:\s+marks?)?\s+(?:on|to)\s+(?:my|his|her|their|your|the)\s+" + BODY,
    r"\bmy\s+" + BODY + r"\s+(?:is|are|was|were|got)\s+(?:scorched|singed)\b",
    r"\b(?:scorch(?:ed|es|ing)?|singe(?:d|s|ing)?|scold(?:ed|ing))\s+" r"(?:the\s+)?(?:side|back|top|front|inside|outside|roof|tip)\s+of\s+" r"(?:my|his|her|their|your|our)\s+" + BODY,
    r"\b(?:got|get|gets)\s+(?:scorched|singed)\b[^.?!]{0,25}" r"\b(?:by|on|from|with)\s+(?:the\s+|a\s+|an\s+|my\s+|his\s+|her\s+|some\s+)?" r"(?:steam|sun|iron|hob|grill|oven|fire|flames?|heat|barbecue|bbq|pan|kettle|" r"hot\s+water|oil|saucepan|toaster|sand)\b",
    r"(?!(?:.*?)\bkettle\b)" r"\b(?:iron|pan|saucepans?|frying\s+pan|chip\s+pan|grill|oven|tray|baking\s+" r"tray|pot|fryer|toaster|jug|hotplate|cooker)\b[^.?!]{0,25}" r"\b(?:fell|fall|falls|dropped|tipped|tips|slipped|slid|touched|touching|" r"came\s+down|knocked\s+over)\b[^.?!]{0,25}\b(?:on|onto|over|into|across)\s+" r"(?:my|his|her|their|our|your)\s+" + BODY,
    r"(?!(?:.*?)\bkettle\b)" r"\b(?:iron|pan|saucepan|hob|grill|oven|pot|fryer|toaster|tray)\b" r"[^.?!]{0,15}\b(?:touched|touching|brushed|grazed|nicked|caught)\b\s+" r"(?:my|his|her|their|our|your)\s+" + BODY,
    r"\b(?:oil|fat|grease)\b[^.?!]{0,15}\b(?:splash(?:ed|es)?|spat|spits?|popped|" r"sprayed|jumped)\b[^.?!]{0,20}\b(?:on|onto|over)\s+" r"(?:my|his|her|their|our|your)\s+" + BODY,
    r"\b(?:scorch(?:ed|es|ing)?|singe(?:d|s|ing)?|scold(?:ed|ing))\s+" r"(?:me|my\s*self|your\s*self|him\s*self|her\s*self|them\s*selves)\b" r"[^.?!]{0,20}\b(?:on|with)\b",
)

BURN_ON_BODY = (
    r"(?:hands?|fingers?|fingertips?|thumbs?|arms?|wrists?|elbows?|tongue|mouth|throat|lips?|"
    r"faces?|cheeks?|nose|ears?|eyes?|feet|foot|toes?|legs?|knees?|shins?|chest|backs?|skin|palms?|"
    r"knuckles?|head|scalp|neck|stomach|belly)\b"
)

NOT_BURN_ON_BODY = (
    r"(?:on|to|in|across)\s+(?:(?:my|his|her|their|your|our|the|a|this|that)\s+)?"
    r"(?!" + BURN_ON_BODY + r"|me\b|him\b|her\b|them\b|us\b|myself\b|yourself\b)\w"
)

HOT_SURFACE = (
    r"\b(?:(?:hot\s+)?(?:hob|grill|oven\s+door|oven\s+shelf|hotplate|cooker\s+ring)|"
    r"(?:hot|boiling|scalding|burning)\s+(?:iron|pan|kettle|saucepan|dish|tray|oil|fat|spoon|"
    r"tin|water))\b"
)

HOT_COMFORT = (
    r"\b(?:hot\s+water\s+bottl\w*|ice\s+pack|heat\s+pack|wheat\s+bag|hot\s+towel|"
    r"hot\s+drink|hot\s+chocolate|hot\s+bath|hot\s+shower|hot\s+water\s+tap)\b"
)

CUT_BODY_PART = (
    r"(?:hands?|fingers?|fingertips?|thumbs?|arms?|wrists?|elbows?|lips?|faces?|cheeks?|nose|"
    r"ears?|eyes?|forehead|feet|foot|toes?|legs?|knees?|shins?|chest|palms?|knuckles?|head|scalp|"
    r"neck|stomach|belly|thighs?|calves|calf|heels?|shins?|ankles?|shoulders?|forearms?|skin)s?\b"
)

PET_OWNS_THE_WOUND = (
    r"(?:my|our|the|his|her|their)\s+(?:dog|dogs|cat|cats|puppy|puppies|kitten|kittens|pup|pet|"
    r"parrot|budgie|hamster|rabbit|bunny|horse|pony|guinea\s+pig|tortoise|ferret|gerbil|rat|lizard|"
    r"snake|hen|chicken)\b[^.?!]{0,25}\b(?:has|have|had|got|with|cut|is|was)\b"
)

NOT_A_PET_LINE = (
    r"\A(?!.*\b(?:dog|dogs|puppy|pup|pups|cat|cats|kitten|kittens|rabbit|hamster|guinea|horse|"
    r"pony|bird|parrot|pet|pets|vet|paw|paws|hoof|fur|tail|beak|snake|lizard)\b).*?"
)

CUT_ON_BODY = (
    r"^(?!.*\b(?:dog|dogs|puppy|pup|pups|cat|cats|kitten|kittens|rabbit|hamster|guinea|"
    r"horse|pony|bird|parrot|pet|pets|vet|paw|paws|hoof|fur|tail|beak|snake|lizard)\b).*?"
    r"\b(?:have|has|had|got|get|gets|getting|gave|gives?|with|from)\b[^.?!]{0,25}"
    r"\b(?:cut|gash|graze|scrape|scratch|nick)\s+"
    r"(?:on|to|in|above|below)\s+(?:my|his|her|their|your|the)\s+"
    r"(?:hands?|fingers?|fingertips?|thumbs?|arms?|elbows?|lips?|"
    r"faces?|cheeks?|nose|ears?|eyes?|eyebrows?|forehead|feet|foot|toes?|legs?|knees?|shins?|"
    r"chest|backs?|palms?|knuckles?|head|scalp|stomach|belly|thighs?|calves|calf|heels?|"
    r"ankles?|shoulders?|hips?)\b"
)

CUT_ON_THROAT_BODY = (
    r"\b(?:cut|gash|scratch|graze|scrape|nick|slice)\b"
    r"(?:\s+(?:on|in|to|across)\s+(?:my|his|her|their|the|your)\s+|\s+(?:my|his|her|their|your)\s+|\s+)"
    r"(?:wrists?|neck|throat)\b"
)

RING_STUCK = (r"\bring\b", r"\bwedding\s+ring\b", r"\bengagement\s+ring\b")

PET_PASSES_BLOOD = (r"[^.?!]*\b(?:wee\w*|urine|urinating|pee\w*|piss\w*|stool|poo\w*|vomit\w*|"
                    r"sick|diarrh\w*|tummy|gut)\b")

PET_WOUND = (
    r"\A(?=.*" + PET_OWNS_THE_WOUND + r")(?!" + PET_PASSES_BLOOD + r")"
    r".*?\b(?:cut|gash|graze|scrape|scratch|nick|wound|sore|blister|bleed\w*|bled|blood)\b",
)

PET_ANIMAL_HURT = (
    r"\b(?:my|our|the|his|her|their)\s+(?:dogs?|cats?|pupp(?:y|ies)|kittens?|pup|pets?|parrot|"
    r"budgie|hamster|rabbit|bunny|horse|pony|guinea\s+pig|tortoise|ferret|gerbil|rats?|lizard|"
    r"snake|hen|chicken)\b[^.?!]{0,32}?\b(?:burnt|burned|scalded|grazed|cut|nicked|"
    r"splinter|blister\w*|broke|broken|bleed\w*|bled|blood|wound|gash\w*|scraped|scrapes)\b",
)
PET_OWNS_A_THING = (
    r"\b(?:dogs?|cats?|pupp(?:y|ies)|kittens?|pup|pets?|parrot|budgie|hamster|rabbit|bunny|horse|"
    r"pony|guinea\s+pig|tortoise|ferret|gerbil|rats?|lizard|snake|hen|chicken)(?:'s)?\s+"
    r"(?:flap|lead|leash|harness|collar|tag|bowl|bed|basket|blanket|toy|toys|coat|jacket|gate|"
    r"door|hutch|kennel|cage|tank|claw|claws|nail|nails)\b",
    r"\b(?:broke|broken|split|torn|lost|caught|trimmed|clipped)\s+(?:a|his|her|its|the)\s+"
    r"(?:nail|nails|claw|claws)\b",
)
HUMAN_OWN_INJURY = (
    r"\b(?:my|our|his|her|their)\s+(?:hand|hands|finger|fingers|thumb|thumbs|wrist|wrists|arm|"
    r"arms|elbow|shoulder|knee|shin|calf|ankle|foot|feet|toe|toes|face|cheek|lip|nose|head|back|"
    r"chest|stomach|leg|legs)\b[^.?!]{0,25}?\b(?:burnt|burned|scalded|sprained|grazed|cut|nicked|"
    r"blister\w*|broke|broken|bleed\w*|bled|blood)\b",
    r"\b(?:burnt|burned|scalded|sprained|grazed|cut|nicked|scratched|bit|bitten|nipped|broke|broken)"
    r"\b[^.?!]{0,20}?\b(?:my|our|their)\s+(?:hand|hands|finger|fingers|thumb|thumbs|wrist|"
    r"wrists|arm|arms|elbow|shoulder|knee|shin|calf|ankle|foot|feet|toe|toes|face|cheek|lip|nose|"
    r"head|back|chest|stomach|leg|legs)\b",
)

PET_NAIL = (
    r"\b(?:my|our|the|his|her|their)\s+(?:dogs?|cats?|puppy|puppies|kitten|kittens|pup|pet|parrot|"
    r"budgie|rabbit|bunny|hamster|horse|pony|guinea\s+pig|ferret|gerbil|lizard)\b[^.?!]{0,30}?\b"
    r"(?:cut|clipped|trimmed|nicked|caught|tore|torn|snapped)\b[^.?!]{0,20}?\b(?:nail|nails|claw|"
    r"claws|quick)\b",
    r"\b(?:my|our|the|his|her|their)\s+(?:dogs?|cats?|puppy|puppies|kitten|kittens|pup|pet)'?s?\s+"
    r"(?:nail|nails|claw|claws|quick)\b[^.?!]{0,30}?\b(?:too\s+short|cut\s+too|clipped\s+too|"
    r"trimmed\s+too|nicked|torn|snapped|split)\b",
    r"\bi\s+(?:cut|clipped|trimmed|nicked)\s+(?:the\s+|his\s+|her\s+|its\s+)?quick\b",
)

BURN_VERB = r"(?:burnt|burned|burn|scald(?:ed|s)?|scorch(?:ed|es|ing)?|singe(?:d|s|ing)?)"

SIGHT_EVER = (
    r"\b(?:sight|eyesight|vision|eye|eyes)\b",
)

SIGHT_LIFE_REPLIES = (
    "Sight that has always been like that is not an emergency, but it is worth a proper eye test: "
    "an optician can test it and your GP can refer you, and there is practical help too - a "
    "certificate for sight loss and the support that comes with it. If it has changed even a "
    "little this week, that is a same-day call instead.",
)

BURNT_BODY_VERB = (
    r"\b(?:my|his|her|their|your|our)\s+(?:faces?|skin|hands?|arms?|legs?|neck|chest|shoulders?|"
    r"backs?|tummy|belly|feet|foot|fingers?|fingertips?|thumbs?|thighs?|palms?|wrists?|lips?|ears?|"
    r"cheeks?|chin|forehead|scalp|eyebrows?|knees?|elbows?|calves|calf|shins?|toes?)\b"
    r"[^.?!]{0,15}\b(?:is|are|was|were|got|gets|has\s+got|have\s+got|looks?)\s+(?:all\s+)?"
    r"(?:burnt|burned|scalded|blister\w*)\b"
    r"(?![^.?!]{0,20}\b(?:from|because\s+of|due\s+to|off)\s+(?:the\s+|all\s+the\s+)?"
    r"(?:cry\w*|tears?|weep\w*|sob\w*)\b)",
    r"\b(?:my|his|her|their|your|our)\s+(?:faces?|skin|hands?|arms?|legs?|neck|chest|shoulders?|"
    r"backs?|tummy|belly|feet|foot|fingers?|fingertips?|thumbs?|thighs?|palms?|wrists?|lips?|ears?|"
    r"cheeks?|chin|forehead|scalp|knees?|elbows?|shins?|toes?)\b[^.?!]{0,15}"
    r"\b(?:is|are|was|were|got|gets|looks?)\s+(?:all\s+)?red\s+raw\b"
    r"(?=[^.?!]{0,30}\b(?:sun|sunburn\w*|sunburnt|hot|boil\w*|oven|kettle|pan|steam|steam\w*|"
    r"iron|wax|scald\w*|fire|flame\w*|barbecue|bbq|cooker|hob|radiator|heat\w*|heated|"
    r"straightener\w*|blow\s+dry\w*|hot\s+water)\b|\Z)",
    r"\bburn(?:t|ed)\b[^.?!]{0,10}\b(?:my|his|her|their|your|our)\s+"
    r"(?:hands?|fingers?|fingertips?|thumbs?|arms?|wrists?|lips?|faces?|cheeks?|nose|ears?|legs?|"
    r"knees?|chest|skin|neck|chin|forehead|eyebrows?|scalp|back|thighs?|feet|foot|toes?|stomach|"
    r"belly|shoulders?)\b",
)

WAX_BODY = (
    r"(?:hands?|fingers?|fingertips?|thumbs?|arms?|wrists?|legs?|thighs?|knees?|feet|foot|toes?|"
    r"lips?|faces?|cheeks?|chin|skin|stomach|belly|chest|neck|back|shoulders?|ears?)\b"
)

HOT_WAX_ON_BODY = (
    r"\b(?:hot|melted|molten|warm|boiling)\s+wax\b[^.?!]{0,25}\b(?:on|onto|over|down|across)\b"
    r"[^.?!]{0,15}\b(?:my|his|her|their|your|our)\s+" + WAX_BODY,
    r"\b(?:wax|waxing\s+wax|wax\s+pot|wax\s+burner)\b[^.?!]{0,25}"
    r"\b(?:spilt|spilled|dripped|dribbled|poured|splashed|leaked|came\s+off)\b"
    r"[^.?!]{0,25}\b(?:my|his|her|their|your|our)\s+" + WAX_BODY,
)

PART_OFF_PART = (
    r"(?:fingers?|fingertips?|thumbs?|toes?|hands?|feet|foot|arms?|legs?|ears?|noses?|lips?|tongues?)"
)

PART_OFF_NOT = (
    r"\A(?!.*\b(?:prosthe\w+|false|glass|denture|dentures|nails?|toenails?|fingernails?|hair|tooth|"
    r"teeth|wig|hairpiece|rings?|earrings?|bracelet|watch|plaster|cast|bandages?|dressings?|brace|"
    r"retainer|contacts?|tags?|labels?|buttons?|sticker|stuck\s+on)\b).*?"
)

PART_OFF = (
    PART_OFF_NOT
    + r"\b(?:my|his|her|their|your|our)\s+" + PART_OFF_PART + r"\b[^.?!]{0,12}\b"
    r"(?:hanging\s+off|hanging\s+by|hanging\s+on\s+by|half\s+off|hanging\s+loose|"
    r"hangs?\s+off)\b",
    PART_OFF_NOT
    + r"\b(?:my|his|her|their|your|our)\s+" + PART_OFF_PART + r"\b[^.?!]{0,15}\b"
    r"(?:has|have|had|was|were|is|are|got|been)?\s*(?:been\s+)?"
    r"(?:cut|chopped|sliced|severed|taken|took|bitten|ripped|torn|broke|snapped)\s+off\b",
    PART_OFF_NOT
    + r"\b(?:cut|sliced|chopped|severed|took|nipped|bit|ripped|tore)\s+(?:the\s+)?"
    r"(?:top|tip|end|part)\s+of\s+(?:my|his|her|their|your)\s+" + PART_OFF_PART + r"\s+off\b",
    PART_OFF_NOT
    + r"\b(?:cut|sliced|chopped|severed|amputated)\s+(?:my|his|her|their|your)\s+"
    + PART_OFF_PART + r"\s+off\b",
    PART_OFF_NOT
    + r"\b(?:severed|amputated)\s+(?:my|his|her|their|your)\s+" + PART_OFF_PART + r"\b",
    PART_OFF_NOT
    + r"\b(?:the\s+)?(?:top|tip|end)\s+of\s+(?:my|his|her|their|your)\s+"
    r"(?:fingers?|thumbs?|toes?|noses?|ears?)\s+(?:came|come|has\s+come|had\s+come|is|was)\s+off\b",
    PART_OFF_NOT
    + r"\b(?:my|his|her|their|your)\s+(?:hands?|arms?|fingers?)\s+"
    r"(?:got|was|is|were|has\s+been|had\s+been)?\s*"
    r"(?:caught|trapped|stuck|pulled|dragged|crushed)\s+(?:in|into|under)\s+(?:the|a)\s+"
    r"(?:machine|machinery|press|lathe|blender|mincer|saw|chipper|shredder|mower|drill|mixer|"
    r"guillotine|baler|combine)\b",
    PART_OFF_NOT
    + r"\b(?:got|get|put|puts|had|has|have|stuck|shoved|pushed|caught)\s+"
    r"(?:my|his|her|their|your)\s+(?:hands?|arms?|fingers?)\s+(?:in|into|under)\s+(?:the|a)\s+"
    r"(?:machine|machinery|press|lathe|blender|mincer|saw|chipper|shredder|mower|drill|mixer|"
    r"guillotine|baler|combine)\b",
    PART_OFF_NOT
    + r"\b(?:my|his|her|their|your)\s+" + PART_OFF_PART + r"\b[^.?!]{0,12}\b"
    r"(?:mashed|mangled|crushed|pulped|squashed\s+flat|flattened)\b",
    PART_OFF_NOT
    + r"\b(?:crushed|smashed|squashed)\s+(?:my|his|her|their|your)\s+"
    r"(?:fingers?|thumbs?|hands?|toes?|feet|foot)\b",
)


MINOR = (
    ("mouth_burn", (r"\b(?:burnt|burned|scalded)\s+(?:the\s+roof\s+of\s+my|inside\s+of\s+my|my\s+(?:tongue|mouth|throat))\b",),
     ("Sip cold water or suck an ice cube, and skip hot, salty or citrus food for a couple of days; "
      "the roof of your mouth usually settles within a week. Get it looked at if it's a big white "
      "patch or still sore after a week.",
      "Cold water or an ice cube is the fix, and give hot, salty and citrus food a miss for a few "
      "days. It normally heals in about a week; anything large or still painful after that should be "
      "checked.")),
    ("tooth_chipped", TOOTH_CHIPPED,
     ("A chipped tooth is a dentist's, not an ambulance: if a piece came off, keep it in milk, and "
      "ring 111 for an urgent dental appointment. Go today if it is bleeding, hurts a lot, or you "
      "can see a pink or red centre in it.",
      "Ring 111 and ask for an urgent dentist, usually within a day or two; keep any piece that "
      "came off in milk and eat on the other side. Bleeding that will not stop, or a bad knock "
      "with it, wants to be seen today.")),
    ("tooth_out", TOOTH_OUT,
     ("Pick the tooth up by the crown and never the root, put it straight back in the socket if you "
      "can, or keep it in milk or saline: a dentist within the hour gives it the best chance, so "
      "ring 111 for the emergency dentist now. A bang on the head as well, or bleeding you cannot "
      "stop, is 999 or A&E.",
      "Hold it by the crown, put it back in the socket if you can and bite gently on a cloth, or "
      "keep it in milk or saline, and ring 111 for an emergency dentist now - the first hour is what "
      "matters. If there was a bang on the head or the bleeding will not stop, ring 999.")),
    ("should_i_call", SHOULD_I_CALL,
     ("That is a 999 or 911 call, not a judgement call: if the question is in your head at all, "
      "ring and say what you can see - they would far rather have the call than not, and being "
      "wrong about it costs you nothing.",
      "Ring 999 or 911 and say what you can see; the call taker decides what to send, and they "
      "would rather hear from you than not. If it turns out to be nothing much, nobody will mind.")),
    ("part_off", PART_OFF,
     ("A part that is off, or hanging on by a thread, is a hospital job now rather than a plaster: "
      "press a clean cloth on the wound and keep pressing, and if a piece has come away, wrap it in "
      "a clean cloth, seal it in a bag and keep the bag cool - never the piece straight on ice. Ring "
      "999 or 911 if the bleeding will not slow or they go pale or dizzy; if it has slowed, go "
      "straight to A&E.",
      "Do not wait on that one: press a clean cloth on it and hold it without lifting it to look, "
      "and if a piece has come away, wrap it in a clean cloth, seal it in a bag and keep the bag "
      "cool. Ring 999 or 911 if the bleeding will not stop or they look pale or clammy - otherwise "
      "A&E now, not tomorrow.")),
    ("bleeding", BLEEDING_SMALL,
     ("Press a clean cloth on the cut and hold it there without lifting it to look for ten minutes; "
      "most cuts stop by then. If it soaks through, the edges gape, or they go pale or dizzy, that's "
      "999 or 911.",
      "Press a clean cloth on it and keep pressing for ten minutes without lifting it to look; add "
      "another cloth on top if it soaks through. If it's still going after twenty minutes or they go "
      "pale or dizzy, that's 999 or 911.")),
    ("cut_wrist", CUT_ON_THROAT_BODY,
     ("Press a clean cloth on it and hold for ten minutes, and get it looked at if it gapes or keeps "
      "bleeding. If you did that to yourself, please tell someone today - Samaritans is 116 123, free "
      "and open any hour, and one cut on a wrist is not a fuss.",
      "Hold a clean cloth on it for ten minutes; if it needs a stitch or will not stop, that is A&E. "
      "And if that was on purpose, tell someone today - 116 123 is Samaritans, free and open any "
      "hour.")),
    ("pet_nail", PET_NAIL,
     ("Press a pinch of flour, cornflour or a styptic pencil on the end of the nail and hold it there "
      "for five minutes without lifting it to look - a cut quick bleeds much more than the nick "
      "deserves, and it stops with pressure. Keep them off the pavement and the stairs for the rest "
      "of the day, and ring the vet if it is still going after ten minutes, if the nail is torn or "
      "hanging, or if a cat has caught a claw.",
      "Flour or cornflour pressed on the tip for five minutes is the first thing, and most stop "
      "there; a torn nail or one that keeps bleeding needs the vet today, and so does a cat's caught "
      "claw, which snags again until it is trimmed back. Soft ground and no jumping for the rest of "
      "the day.")),
    ("pet_wound", PET_WOUND,
     ("Bathe it with cool water or salt water and pat it dry, then keep the animal off it - a buster "
      "collar or a sock over a paw - because licking keeps a wound wet and slow to heal. Ring the "
      "vet today if it gapes open, keeps bleeding, or is on a paw, an ear or near an eye, and put "
      "nothing from the bathroom cabinet on it.",
      "Cool water or salt water, pat it dry, and keep the animal from licking it - a cone or a sock "
      "over a paw does that better than telling it off. Anything that gapes, keeps bleeding, or is "
      "on a paw, an ear or an eye is a vet visit today rather than a wait-and-see, and nothing from "
      "the bathroom cabinet goes on it: a pet licks a plaster off and the cream is not made for "
      "animals.")),
    ("cut", (r"\b(?:cut|cuts|sliced|slices|nicked|nicks|grazed|grazes|scraped|scrapes)\s+"
              r"(?:my|his|her|their|the)\s+(?:finger|thumb|hand|"
              r"arm|leg|foot|toe|knee|head|face|lip|eye|ear|tongue|palm|heel|knuckle|shin|"
              r"elbow|fingertip)s?\b",
              r"\b(?:scratched|scratches)\s+(?:my|his|her|their|the)\s+(?:finger|thumb|hand|"
              r"arm|leg|foot|toe|knee|head|face|lip|ear|tongue|palm|heel|knuckle|shin|"
              r"elbow|fingertip|forearm|forehead|chin)s?\b",
              r"\A(?!.*" + PET_OWNS_THE_WOUND + r").*?"
              r"\b(?:cut|gash|scratch|graze|scrape|nick|slice)\b"
              r"(?:\s+(?:on|in|to|across)\s+(?:my|his|her|their|the|your)\s+"
              r"|\s+(?:my|his|her|their|your)\s+|\s+)"
              r"(?:finger|thumb|hand|arm|leg|foot|toe|knee|head|face|lip|eye|ear|tongue|palm|"
              r"heel|knuckle|shin|elbow|fingertip|forearm|forehead|chin)s?\b",
              r"\bpaper\s+cut\b", r"\bcut\s+my\s*self\b",
              r"\b(?:cut|cutting|nicked|sliced|grazed|scraped)\s+(?:him|her|them)sel(?:f|ves)\b",
              CUT_ON_BODY,
              r"\b(?:my|his|her|their|your|the)\s+(?:cut|gash|graze|scrape|scratch)\b"
              r"[^.?!]{0,20}\bbleeding\b",
              NOT_A_PET_LINE
              + r"\b(?:a|an|this|that|my|his|her|their)\s+"
              r"(?:nasty|deep|bad|sore|bleeding|weeping)?\s*"
              r"(?:cut|gash|graze|scrape|scratch|nick|slice)\s+(?:on|in|to|across|near)\s+"
              r"(?:my|his|her|their|your)\s+" + CUT_BODY_PART,
              NOT_A_PET_LINE
              + r"\b(?:have|has|got|get|had)\s+(?:a|an|this|that)\s+"
              r"(?:small|little|nasty|deep|bad|tiny|sore|long|clean|weeping)\s+"
              r"(?:cut|gash|graze|scrape|scratch|nick)\b",
              NOT_A_PET_LINE
              + r"\b(?:have|has|had|got|get)\s+(?:a|an)\s+"
              r"(?:cut|gashed|grazed|scraped|scratched)\s+" + CUT_BODY_PART,
              r"(?!(?:.*?)\b(?:car|cars|van|bike|motorbike|wheel|wheels|bumper|alloy|paint|door|"
              r"doors|wall|table|worktop)\b)"
              r"\b(?:have|had|got)\s+(?:a|an)\s+(?:graze|scrape|gash)\b",
              r"\b(?:nicked|sliced|grazed|scratched|scraped|caught)\s+my\s*self\b",
              r"\b(?:nicked|sliced|grazed|scratched|scraped|caught)\s+"
              r"(?:him|her|them)sel(?:f|ves)\b"),
     ("Press a clean cloth on it and keep pressing for ten minutes without lifting it to look; most "
      "small cuts stop by then. If the edges gape, it's deep, or it's still bleeding after twenty "
      "minutes of steady pressure, get it looked at.",
      "Wash it under the tap, press a clean cloth down and hold for ten minutes; that's what stops "
      "most cuts. A cut that gapes open, is deep, or keeps bleeding through the cloth needs a nurse "
      "or A&E.")),
    ("burn", (r"\b" + BURN_VERB + r"\s+(?:my|his|her|their|me|myself|yourself|himself|herself|themselves)\b"
              r"(?!\s+(?:bridges|candle\s+at|holes?|midnight|hair|fringe|bangs|ponytail|plait|"
              r"braid)\b)",
              *BURNT_BODY_VERB,
              r"\b(?:small|minor|little)\s+(?:burn|scald)s?\b",
              r"\bblister\w*\s+(?:from|off|after)\s+(?:the\s+|a\s+|my\s+|his\s+|her\s+|"
              r"their\s+)?(?:kettle|oven|hob|grill|toaster|iron|pan|fryer|barbecue|bbq|fire|"
              r"flames?|steam|boiling\s+water|hot\s+water|hot\s+oil|hot\s+fat|hot\s+pan)\b",
              r"\b(?:burn|burnt|burned|burning|scalds?|scalded|scalding)\b[^.?!]{0,25}"
              r"\bblister\w*\b",
              HOT_WAX_ON_BODY[0], HOT_WAX_ON_BODY[1],
              r"(?!(?:.*?)\b" + NOT_BURN_ON_BODY + r")"
              r"\b(?:got|get|have|has|had)\s+(?:a|an|this|that|some)\s+"
              r"(?:bad|nasty|nasty|small|minor|little|sore|red|nasty)*\s*(?:burn|scald)s?\b",
              r"\b(?:a|the|this|that)\s+(?:bad|nasty|small|minor|little|sore|red)?\s*burn\s+"
              r"(?:from|off)\b",
              r"\b(?:a|the|this|that)\s+(?:bad|nasty|small|minor|little|sore|red)?\s*burn\s+"
              r"(?:on|to)\s+(?:my|his|her|their|your|the)\s+" + BURN_ON_BODY,
              r"\b(?:burnt|burned|scalded|scald|burn)\s+(?:the\s+roof\s+of\s+my|inside\s+of\s+my)\b",
              r"\b" + BURN_VERB + r"\s+(?:my|his|her|their|me|on\s+my)\s+"
              r"(?:hand|finger|arm|wrist|thumb|tongue|mouth|foot|leg)s?\b",
              r"\b(?:put|putting|puts|placed?|placing|rest(?:ed|ing)?|touch(?:ed|ing)?|touches|"
              r"grab(?:bed|bing)?|grabs|picked?\s+up|lean(?:ed|t|ing)?\s+on|sat\s+on|slipped)\s+"
              r"(?:my|his|her|their)\s+(?:hand|hands|finger|fingers|thumb|palm|forearms?|arm|wrist|"
              r"bottom|bum|leg|legs|back)\b[^.?!]{0,25}\b"
              r"(?:hob|grill|oven\s+door|oven\s+shelf|hotplate|cooker\s+ring|cooker)\b",
              r"\b(?:put|puts|putting|stuck|stick|sticks|sticking|thrust|shoved|shove|dipped|"
              r"dip|place[ds]?|placing)\s+(?:my|his|her|their|our|your)\s+"
              r"(?:hand|hands|finger|fingers|thumb|thumb|arm|arms|foot|feet|fist)\b"
              r"[^.?!]{0,15}\b(?:in|into|through|over)\s+(?:the|a|an)\s+"
              r"(?:fire|flames|flame|campfire|bonfire|barbecue|barbeque|bbq|coals|embers|"
              r"burning\s+coals)\b",
              r"\b(?:my|his|her|their|our|your)\s+(?:hand|hands|fingers?|arm|arms|foot|feet)\b"
              r"[^.?!]{0,12}\b(?:is|was|were|got|went|had\s+gone)\b[^.?!]{0,6}"
              r"\b(?:in|into|through)\s+(?:the|a|an)\s+(?:fire|flames|campfire|bonfire|coals|"
              r"embers)\b",
              r"\b(?:brushed|brushing|brushes|graze[ds]?|grazing|scraped|rubbed|caught)\s+"
              r"(?:against|past|up\s+against|on)?\s*"
              r"(?:(?:the|a|an|my|his|her|their|our)\s+)?"
              r"(?:hot|boiling|scalding|red\s?hot|searing|sizzling)\s+"
              r"(?:grill|hob|ring|oven|oven\s+door|oven\s+shelf|iron|pan|pot|kettle|cooker|"
              r"hotplate|radiator|heater|burner|stove|saucepan|element|plate|tray|shelf)\b"
              r"(?![^.!?]{0,25}\b(?:was|were|is|are|had\s+been|has\s+been)\s+"
              r"(?:already\s+|still\s+|stone\s+|completely\s+)?(?:cold|off|not\s+hot|"
              r"not\s+warm|switched\s+off|turned\s+off|unplugged|cooled)\b)",
              r"\b(?:hot|boiling|scalding|searing|sizzling)\s+"
              r"(?:oil|fat|water|stock|soup|gravy|syrup|sugar)\b[^.?!]{0,10}"
              r"\b(?:on|over|onto|down|across)\s+"
              r"(?:my|his|her|their|our|your)\s+"
              r"(?:hand|hands|arm|arms|wrist|wrists|leg|legs|foot|feet|lap|chest|tummy|belly|"
              r"neck|face|skin|shoulder|shoulders|back|thigh|thighs|knee|knees|fingers?|thumb|"
              r"toes?|ankle|body|mouth|chin)\b",
              r"(?!(?:.*?)\b" + HOT_COMFORT + r")"
              r"\b(?:touch(?:ed|ing)?|touches|"
              r"grab(?:bed|bing)?|grabs|held|holding|lean(?:ed|t|ing)?\s+on|"
              r"rest(?:ed|ing)?\s+(?:on|onto|against|over)|"
              r"sat\s+on|slipped)\b[^.?!]{0,25}(?:(?:the|a|an|my|his|her|their|our)\s+)?"
              + HOT_SURFACE,
              r"(?!(?:.*?)\b" + HOT_COMFORT + r")"
              r"\brest(?:ed|ing)?\b[^.?!]{0,20}(?:(?:the|a|an|my|his|her|their|our)\s+)?"
              + HOT_SURFACE +
              r"\b[^.?!]{0,12}\b(?:on|onto|against|over|across)\s+"
              r"(?:my|his|her|their|our|your)\s+"
              r"(?:hand|hands|arm|arms|finger|fingers|thumb|wrist|leg|legs|knee|knees|lap|foot|feet|"
              r"chest|face|skin|shoulder|shoulders|thigh|back|belly|tummy)\b",
              r"(?!(?:.*?)\b" + HOT_COMFORT + r")"
              r"\b(?:put|putting|puts|placed?|placing|rest(?:ed|ing)?|touch(?:ed|ing)?|touches|"
              r"grab(?:bed|bing)?|grabs|picked?\s+up|lean(?:ed|t|ing)?\s+on|sat\s+on|slipped)\s+"
              r"(?:my|his|her|their)\s+(?:hand|hands|finger|fingers|thumb|palm|forearms?|arm|wrist|"
              r"bottom|bum|leg|legs|back)\b[^.?!]{0,25}\b"
              r"(?:hot|boiling|scalding|burning)\s+(?:iron|water|pan|kettle|saucepan|dish|tray|"
              r"oil|fat|spoon|tin)\b",
              r"\b(?:spill\w*|spilt|pour\w*|tip\w*|knock\w*|get\w*|got|drop\w*|dropped|"
              r"splash\w*|throw\w*|threw|chuck\w*)\s+(?:boiling|hot|scalding)\s+"
              r"(?:water|oil|fat|soup|tea|coffee)\s+(?:on|over|onto)\s+"
              r"(?:(?:my|his|her|your|their|our)\s+(?:hand|hands|arm|arms|wrist|wrists|leg|legs|"
              r"foot|feet|lap|chest|tummy|belly|neck|face|skin|shoulder|shoulders|back|thigh|thighs|"
              r"knee|knees|fingers?|thumb|toes?|ankle|body|mouth|chin)"
              r"|me|him|her|them|us|my\s*self|your\s*self|him\s*self|her\s*self|them\s*selves|"
              r"our\s*selves)\b",
              r"\bmy\s+(?:hand|finger|arm|wrist|thumb|tongue|mouth|foot|leg|skin)\b.{0,15}"
              r"\b(?:is|got|keeps?\s+getting)\s+(?:burnt|burned|scalded|blistered|scorched|"
              r"singed)\b",
              *SCORCHED_A_PERSON,

              r"\b(?:put|rub|apply|use|spread)\b[^.?!]{0,30}\b(?:on|onto)\s+(?:a|the|my|this|that)\s+"
              r"(?:bad\s+|red\s+|small\s+|nasty\s+|serious\s+|little\s+|sore\s+|fresh\s+)*"
              r"(?:burn|scald)s?\b",

              r"\b(?:burn|burns|burning|scald|scalds|scalding)\s+(?:my|your|his|her|their|me|"
              r"myself|yourself|himself|herself|themselves)\b"
              r"(?!\s+(?:bridges|candle\s+at|holes?|midnight)\b)",
              r"\b(?:get|got|gets)\s+(?:burnt|burned|scalded)\b(?!\s*(?:out\b|by\b|on\s+(?:that|the\s+deal|a\s+deal)\b))",
              r"\b(?:burn|burns|burning|scald|scalds|scalding)\b[^.?!]{0,20}"
              r"\b(?:my|your|his|her|their)\s+(?:hand|hands|finger|fingers|thumb|arm|wrist|"
              r"tongue|mouth|foot|feet|leg|skin|face|neck)\b",
              r"\b(?:first\s+aid\s+for|treat|treating|soothe|helps?|do\s+for|good\s+for|"
              r"best\s+(?:thing\s+)?for)\b[^.?!]{0,20}"
              r"\b(?:a|the|this)\s+(?:bad\s+|red\s+|small\s+|nasty\s+|serious\s+)?(?:burn|scald)\b"),
     ("Cool it under cool running water for twenty minutes, then cover it loosely with cling film "
      "or a clean non-fluffy cloth. Don't use ice, butter or cream, and get it checked if it's bigger "
      "than your palm, on the face or hands, or blistered.",
      "Twenty minutes under cool running water is the thing that helps, starting straight away. "
      "Cover it loosely and skip ice and butter; a burn that blisters or is on the face, hands or "
      "joints should be seen.")),
    ("nosebleed", (r"\bnose\s*bleed\b", r"\bnose\s+(?:is\s+|keeps\s+|started\s+)?bleeding\b",
                   r"\bnose\b.{0,20}\bbleed\w*\b"),
     ("Sit up, lean forward and pinch the soft part of your nose for ten minutes without checking. "
      "Spit out any blood rather than swallowing it; if it's still going after twenty minutes, get "
      "help.",
      "Lean forward, pinch the soft part of the nose and hold for ten minutes; leaning back just "
      "sends blood down your throat. If it keeps coming back or lasts over twenty minutes, see "
      "someone.")),
    ("weight_limb_long", WEIGHT_JOINT,
     ("Weeks or months of it is a GP job rather than A&E: book an appointment, say how long it has "
      "been going on and what sets it off, and keep off it as much as you can meanwhile. Anything "
      "sudden, or clearly worse than usual, is the exception - that is A&E the same day.",)),
    ("ring_stuck", RING_STUCK,
     ("Get the ring off now, before the finger swells any further: hold your hand above your head "
      "for a few minutes, then work it round with soap and water or a little cooking oil, twisting "
      "rather than pulling. If it will not move, wind dental floss or thin thread under the band "
      "and unwrap it towards the fingertip; a jeweller can cut it off, and so can A&E. If the "
      "finger has gone numb, cold or blue, go today rather than waiting - a ring left on a "
      "swelling finger can cut the blood off within hours.",
      "Get it off today if you can: hand up above your head for a few minutes, then soap and "
      "water or a little oil, twisting rather than pulling, and do not keep at it. Floss wound "
      "under the ring and unwrapped towards the tip will walk it off. If it will not move, or the "
      "finger is numb, cold or blue, that is A&E or 111 today; a jeweller can cut it off too.")),
    ("weight_limb", WEIGHT_JOINT,
     ("A joint that won't take weight is an X-ray today rather than a wait-and-see: go to A&E or a "
      "minor injuries unit, and keep it still on the way. Ice it and keep it raised until it has "
      "been seen.",
      "Don't wait to see whether it eases: a joint that won't take weight wants an X-ray today, at "
      "A&E or a minor injuries unit. Keep it still and raised on the way there.")),
    ("sprain", (r"\bsprain(?:ed)?\s+(?:my|his|her|their)\b",
                r"\bsprain(?:ed)?\s+(?:a|an|the|both|your)?\s*(?:ankle|ankles|knee|knees|wrist|"
                r"wrists|thumb|elbow)s?\b",
                r"\btwisted\s+my\s+(?:ankle|knee|wrist)\b",
               r"\brolled\s+my\s+ankle\b", r"\b(?:went\s+)?over\s+on\s+my\s+ankle\b",
               r"\bhurt\s+(?:my|his|her|their)\s+(?:knee|ankle|wrist|shoulder|elbow)\b",
               r"\b(?:ankle|knee|wrist|elbow|foot|finger|thumb|shoulder)\b.{0,40}"
               r"\b(?:swollen|swelling|puffy|bruised|bruising)\b",
               r"\b(?:swollen|swelling|puffy|bruised|bruising)\b.{0,40}"
               r"\b(?:ankle|knee|wrist|elbow|foot|finger|thumb|shoulder)\b"),
     ("Rest it, put an ice pack on for 15 minutes at a time, and wrap it snugly but not tight; keep "
      "it up when you sit down. If you can't put weight on it or it swells badly, get it checked.",
      "Ice for 15 minutes, raise it, and take it easy for a day or two. If you can't bear weight or "
      "it's very swollen and bruising fast, have it looked at.")),
    ("sight_long", SIGHT_EVER,
     SIGHT_LIFE_REPLIES),
    ("limp_long", LIMP_PERSON,
     ("A limp that has been going on for weeks is a GP job rather than A&E: book an appointment, "
      "say how long it has been there and what makes it worse, and keep up what you can do without "
      "pain meanwhile. Get it seen sooner if it is getting worse, if the joint gives way, or if "
      "there is swelling or heat in it.",)),
    ("limp", LIMP_PERSON,
     ("Check it while they are sitting: look for swelling and bruising, run a hand down the shin "
      "and press gently round the ankle and the knee, and see which way it hurts. Ice it for 15 "
      "minutes, rest it and give children's paracetamol if the age allows; if they will not put "
      "weight on it, the joint is swollen or hot, or a small child will not walk at all, that is "
      "the same day at a minor injuries unit.",
      "A limp that comes after a knock is rest, ice for 15 minutes and a day or two off it. Get it "
      "looked at the same day if you cannot put weight on it, if it is swollen or hot, or if a "
      "small child has stopped walking on it altogether.")),
    ("sunburn", (r"\bsun\s?burnt\b", r"\bsun\s?burn(?:ed)?\b", r"\bsunburn\b"),
     ("Get out of the sun, cool the skin with a shower or a damp cloth, and drink plenty of water; "
      "calamine or after-sun takes the sting out. Blisters, shivering or feeling faint need a doctor, "
      "and keep it covered for a few days.",
      "Cool showers, plenty of water and a loose cotton shirt are what help; leave blisters alone. "
      "If someone is shivery, dizzy or badly blistered, that needs a doctor.")),
    ("splinter", (r"\bsplinter\b",),
     ("Soak it in warm water for ten minutes and pull it out with tweezers in the direction it went "
      "in. If it's deep, under a nail, or the area gets red and hot, get it looked at.",
      "Warm water first, then tweezers along the line it went in. Anything deep or going red and hot "
      "should be checked.")),
    ("broken", (r"\b(?:broken|broke|fractured)\s+(?:my|his|her|their|a)\b.{0,25}\b(?:arm|leg|wrist|"
                r"ankle|hip|finger|thumb|toe|ribs?|collarbone|shoulder|foot|hand|nose|knee|elbow)\b",
                r"\bmy\s+(?:ribs?)\s+(?:is|are|'s|'re|feels?|looks?)\s+"
                r"(?:broken|cracked|fractured|snapped)\b",
                r"\b(?:cracked|crack|snapped|snap|broke|broken|fractured)\s+"
                r"(?:a|my|his|her|their|two|three)\s+(?:ribs?|rib\s?cage)\b",
                r"\bthink\s+(?:i'?ve\s+)?(?:broken|fractured)\b", r"\b(?:bone|wrist|arm|leg)\b.{0,25}"
                r"\b(?:sticking|poking|piercing)\s+out\b",
                r"\b(?:my|his|her|their)\s+ribs?\b[^.?!]{0,15}"
                r"\b(?:is|are|was|were|got|might\s+be|may\s+be|feels?)\b[^.?!]{0,10}"
                r"\b(?:broken|cracked|fractured)\b",
                r"\b(?:cracked|crack|broke|broken|fractured)\s+(?:a|my|his|her|their)\s+ribs?\b"
                r"(?!\s+(?:of\s+beef|of\s+pork|joint|roast|recipe|rub|rack))",
                r"\bthink\s+(?:i'?ve\s+|i\s+)?(?:cracked|broken|fractured)\s+"
                r"(?:a\s+|my\s+)?ribs?\b",
                r"\b(?:broken|cracked|fractured)\s+ribs?\b"
                r"(?!\s*(?:of\s+(?:beef|pork|lamb)|joint|roast|recipe|rub|rack|in\s+the))",
                r"(?:^|[,.!?;]|\band\b|\bbut\b|\bso\b|\bi\s+think\b|\bi\s+reckon\b)\s*"
                r"(?:my|his|her|their)\s+jaw\b[^.?!]{0,15}"
                r"\b(?:is|are|'?s|'?re|was|were)\s+(?:broken|fractured)\b(?!\s+out\b)",
                r"(?:^|[,.!?;]|\band\b|\bbut\b|\bso\b|\bi\s+think\b|\bi\s+reckon\b)\s*"
                r"(?:my|his|her|their)\s+nose\b[^.?!]{0,15}"
                r"\b(?:is|are|'?s|'?re|was|were)\s+"
                r"(?:broken|cracked|fractured|snapped)\b(?!\s+out\b)",
                r"(?:^|[,.!?;]|\band\b|\bbut\b|\bso\b|\bi\s+think\b|\bi\s+reckon\b)\s*"
                r"(?:my|his|her|their)\s+collarbone\b[^.?!]{0,15}"
                r"\b(?:is|are|'?s|'?re|was|were)\s+snapped\b",
                r"\b(?:broken|broke|fractured)\s+(?:my|his|her|their)\s+jaw\b",
                r"\b(?:broken|broke|fractured|cracked|snapped)\s+(?:my|his|her|their)\s+nose\b",
                r"\b(?:snapped)\s+(?:my|his|her|their)\s+collarbone\b",
                r"\b(?:my|his|her|their|your)\s+(?:fingers?|thumb|toes?)\b[^.?!]{0,20}"
                r"\b(?:is|are|looks?|went|gone|got)\s+(?:all\s+)?(?:bent|bent\s+back|twisted|"
                r"out\s+of\s+shape|at\s+a\s+funny\s+angle)\b"),
     ("Keep it still and supported, ice it for twenty minutes and take paracetamol; don't try to "
      "straighten it yourself. Go to A&E or a minor injuries unit, and ring 999 if the bone is "
      "through the skin, it looks bent, or the fingers or toes go numb or white.",
      "Support it where it is, ice it and take painkillers; a bent limb, bone through the skin or "
      "numb fingers is 999, otherwise get it checked at A&E or a minor injuries unit today.")),
)

import re

LAUGH_WORD = (
    r"\blaugh\w*\b", r"\bgiggl\w*\b", r"\bchuckl\w*\b", r"\blol\b",
)
LAUGH_TAKES_BREATH = (
    r"\bbreath\w*\b[^.!?]{0,30}\b(?:when|whenever|if|while|after)\b[^.!?]{0,20}"
    r"\blaugh\w*\b",
    r"\b(?:when|whenever|while|if|after)\b[^.!?]{0,15}\blaugh\w*\b[^.!?]{0,40}"
    r"\bbreath\w*\b",
    r"\blaugh\w*\b[^.!?]{0,40}\b(?:can'?t|cannot|couldn'?t|makes?\s+me|lose|lost|losing)\b"
    r"[^.!?]{0,20}\bbreath\w*\b",
    r"\blaugh\w*\b[^.!?]{0,40}\b(?:out\s+of\s+(?:breath|puff)|breathless|puffed|winded)\b",
    r"\b(?:lose|lost|losing)\s+(?:my|his|her|their|our)\s+breath\b[^.!?]{0,25}\blaugh\w*\b",
    r"\bbreath\b[^.!?]{0,25}\blaugh\w*\b",
)
LAUGH_BREATH_RED = (
    r"\b(?:stopped\s+breathing|isn'?t\s+breathing|not\s+breathing|gasping|turned\s+blue|"
    r"went\s+blue|blue\s+lips|pass(?:ed)?\s+out|blacked\s+out|fainted|faint|collapsed|"
    r"hurts?|wheez\w*|"
    r"at\s+night|in\s+the\s+(?:night|evening)|during\s+the\s+night|night[\s-]?time|"
    r"wok(?:e|en)(?:\s+up)?|wakes?\s+(?:me|up)|waking\s+(?:up|me)|"
    r"coughing\s+up|blood|dizz\w*|light[\s-]?headed|see\s+stars|blurr\w*|"
    r"\bnow\b|\bat\s+all\b|\bstill\b|\bnot\s+(?:coming|getting|back|stopping)\b|"
    r"\b(?:hasn'?t|havent|haven'?t|didnt|didn'?t|won'?t|wont)\s+(?:come|got|get|stop)\b|"
    r"\b(?:been\s+going|going|gone)\s+on\s+for\b|\bfor\s+\d+\s+(?:minutes?|hours?)\s+now\b|"
    r"(?:\bfor|\btakes?)\s+(?:ages|a\s+(?:long\s+)?(?:while|time)|minutes)\b)\b",
)
LAUGH_OTHER_PERSON = (
    r"\b(?:he|she|they)\b[^.?!]{0,25}"
    r"\b(?:couldn'?t|couldnt|stopped|wasnt|was\s+not|isnt|is\s+not)\b[^.?!]{0,15}\bbreath\w*",
    r"\b(?:my|our|her|his|their)\s+(?:son|daughter|child|kid|baby|boy|girl|husband|wife|partner|"
    r"mum|mom|dad|father|mother|brother|sister|nan|grandma|grandad|grandmother|grandfather|"
    r"friend|mate|neighbour|neighbor)\b[^.?!]{0,25}\b(?:was|were)\s+laugh\w*",
    r"\b(?:someone|somebody)\b[^.?!]{0,20}\b(?:couldn'?t|couldnt|stopped)\b[^.?!]{0,12}"
    r"\bbreath\w*",
)

PET_BREATH = (
    r"\b(?:dog|dogs|pupp\w*|cat|cats|kitten|kittens|pet|parrot|budgie|hamster|rabbit|bunny|"
    r"horse|pony|guinea\s+pig|tortoise|ferret|gerbil|rat|lizard|snake|animal)\b\s*"
    r"(?:,\s*(?:he|she|it)\s+)?"
    r"(?:is|are|was|were|gets?|got|keeps?|seems?|looks?|sounds?|'s|has\s+been|have\s+been)\s+"
    r"(?:\w+\s+){0,2}"
    r"(?:breathless|out\s+of\s+(?:puff|breath)|puffed|winded)\b",
    r"\b(?:dog|dogs|pupp\w*|cat|cats|kitten|kittens|pet|parrot|budgie|hamster|rabbit|bunny|"
    r"horse|pony|guinea\s+pig|tortoise|ferret|gerbil|rat|lizard|snake|animal)\b\s*"
    r"(?:,\s*(?:he|she|it)\s+)?"
    r"(?:(?:is|was|are|were|keeps?|'s)\s+)?"
    r"(?:can'?t|cannot|couldn'?t|could\s+not|is\s+not|isn'?t|struggl\w*)\s+"
    r"(?:to\s+)?(?:catch|get|find)\s+(?:his|her|its|their)\s+breath\b",
)
PET_BREATH_NOW = (
    r"\b(?:can'?t|cannot|couldn'?t|could\s+not|struggl\w*|struggled)\s+(?:to\s+)?"
    r"(?:catch|get|find)\s+(?:his|her|its|their)\s+breath\b",
)
PET_EFFORT = (
    r"\b(?:play\w*|running|ran(?:\s+about)?|runs?\b|fetch\w*|walk\w*|park|chase\w*|ball|"
    r"exercise\w*|training|agility|swim\w*|"
    r"trot\w*|canter\w*|gallop\w*|ride|rides|riding|ridden|lunge\w*|hack\w*|jump\w*|"
    r"lesson|schooling)\b",
)
_PET_APPOSITIVE = (
    r"\b(?:dog|dogs|pupp\w*|cat|cats|kitten|kittens|pet|parrot|budgie|hamster|rabbit|bunny|"
    r"horse|pony|guinea\s+pig|tortoise|ferret|gerbil|rat|lizard|snake|animal)\b\s*,\s*"
    r"(?:he|she|it)\b"
)
PET_APPOSITIVE = (_PET_APPOSITIVE,)
PET_APPOSITIVE_SUB = re.compile(_PET_APPOSITIVE, re.I)
PET_CANT_SETTLE = (
    r"\b(?:can'?t|cannot|won'?t|wont|not)\s+(?:get\s+)?(?:comfortable|comfy|settle[ds]?)\b",
)

HEAT_CAUSE = (
    r"\b(?:this|the|all\s+this)\s+heat\b|\bheat\s?wave\b|\bhumidi(?:d|ty)\b|\bhumidity\b|"
    r"\b(?:hot|boiling|muggy|stifling|sweltering)\s+(?:weather|day|room|office|night|bus|tube)\b|"
    r"\b(?:so|too|really|very)\s+(?:hot|humid|muggy|stuffy)\b|"
    r"\bheat\s+of\s+the\s+day\b|\b\d{2,3}\s*degrees\b",
)
HEAT_NOT_WEATHER = (
    r"\b(?:chilli?|chili|curry|pepper\w*|spic(?:y|e|ier|iest)|wasabi|horseradish|mustard|"
    r"salsa|sauce|wings|broth|soup|kebab|taco\w*|jalape\w*|paprika|ginger|"
    r"oven|grill|barbecue|bbq|bonfire|sauna|steam(?:er|y)?|toaster?)\b",
)
BREATH_BARE = (
    r"\b(?:can'?t|cannot|couldn'?t|hard\s+to|difficult\s+to)\s*"
    r"(?:breathe|breath\b|get\s+my\s+breath|catch\s+my\s+breath)\b|"
    r"\bstruggl\w*\s+(?:to\s+)?breathe\b",
)
HEAT_BREATH_RED = (
    r"\b(?:faint\w*|dizz\w*|light[\s-]?headed|confus\w*|sick|vomit\w*|"
    r"one\s+side|slurr\w*|for\s+hours?|all\s+day|since\s+(?:yesterday|this\s+morning)|"
    r"asthma|inhaler|COPD\b|"
    r"not\s+settl\w*|wont\s+settle|won'?t\s+settle|no\s+better|getting\s+worse)\b",
)

ALLERGY_FOOD = (
    r"\b(?:swelling|swollen|swelled|puff\w*\s+up|puffed\s+up|puffing\s+up|puffy|hives?|urticaria|"
    r"welts?|blotch\w*|rash)\b[^.!?]{0,45}\b(?:after|from|since|because\s+of)\b[^.!?]{0,25}"
    r"\b(?:eat\w*|ate|eaten|having|had|drank|drink\w*|tried|tast\w*|bit\s+into|food|meal|"
    r"breakfast|lunch|dinner|snack|formula|milk|sting\w*|stung|bee|wasp|antibiotic\w*|medicine|"
    r"tablet\w*)\b",
    r"\b(?:after|from)\b[^.!?]{0,15}\b(?:eating|having|drinking|trying|tasting|taking)\b"
    r"[^.!?]{0,30}\b(?:swelling|swollen|swelled|puff\w*|puffy|hives?|urticaria|welts?|rash|"
    r"itch\w*|tingl\w*|blotch\w*)\b",
    r"\b(?:stung|stings?)\b[^.!?]{0,30}\b(?:and|,)\b[^.!?]{0,20}\b(?:now\s+)?"
    r"\b(?:her|his|their|my|our|the)\b[^.!?]{0,18}"
    r"\b(?:hand|arm|foot|leg|face|lips?|tongue|throat|finger|ankle|wrist|cheeks?)\b"
    r"[^.!?]{0,20}\b(?:swell\w*|swollen|puff\w*|itch\w*|hives?|rash)\b",
    r"\b(?:ate|eaten|eating|had|tried|drank|drinking)\b[^.!?]{0,30}\b(?:and|,)\b[^.!?]{0,20}"
    r"\b(?:her|his|their|my|our|the)\b[^.!?]{0,18}\b(?:lips?|tongue|throat|face|mouth|cheeks?)\b"
    r"[^.!?]{0,20}\b(?:puff\w*|puffy|swell\w*|swollen|itch\w*|tingl\w*|hives?|rash)\b",
)
ALLERGY_AIRWAY = (
    r"\b(?:tongue|throat|voice|swallow\w*|breath\w*|can'?t\s+breathe|wheez\w*|faint\w*|"
    r"dizz\w*|limp|floppy|collapse\w*|unconscious|shock)\b",
)
ALLERGY_OFF = (
    r"\b(?:chapped|cold\s+sore|piercing|teething|dummy|chewed|bit\s+my\s+lip|bitten\s+lip|"
    r"sunburn\w*|in\s+the\s+cold|from\s+the\s+cold|dehydrat\w*|mouth\s+ulcer|bump\w*\s+it)\b",
)

ALLERGY_FACE = (
    r"\b(?:lips?|tongue|throat|face|mouth|cheeks?)\b",
)
STING_WORDS = (
    r"\b(?:bee|bees|wasp|wasps|hornet\w*|stung|stings?|bumble\s?bee\w*)\b",
)
FOOD_WORDS = (
    r"\b(?:eat\w*|ate|eaten|food|meal|breakfast|lunch|dinner|snack|formula|milk|drank|drink\w*)\b",
)

CRUSH_ON_A_PERSON = (
    r"\b(?:someone|somebody|a\s+(?:man|woman|child|kid|bloke|lady|person)|him|her|them|people|"
    r"anyone|everyone)\b",
    r"\b(?:my|his|her|their|our|your)\s+(?:husband|wife|partner|fianc|boyfriend|girlfriend|son|"
    r"daughter|child|kid|kids|baby|boy|girl|mum|mom|mother|dad|father|brother|sister|friend|"
    r"mate|neighbour|neighbor|gran|granny|grandma|grandad|grandpa|uncle|aunt|cousin|nan|nana|"
    r"colleague|boss|carer|lodger|housemate|flatmate|dog|cat|puppy|kitten|pet|"
    r"hands?|fingers?|thumbs?|arms?|wrists?|elbows?|legs?|feet|foot|toes?|knees?|ankles?|shins?|"
    r"chest|back|head|neck|face|shoulders?|hips?|ribs|pelvis|thighs?|calf|calves|torso|spine|"
    r"belly|stomach|lap)\b",
)
CRUSH_HEAVY_ON_A_PRONOUN = (
    r"\b(?:roof|roofs|roofing|chimney|ceiling|ceilings|wall|walls|beam|beams|joist|joists|"
    r"scaffold\w*|slab|slabs|brick|bricks|masonry|rubble|debris|wardrobe|cupboard|shelves|shelf|"
    r"bookcase|cabinet|fridge|freezer|door|ladder|television|tv|mirror|glass|window|tiles?|"
    r"slates?|gutter\w*|fence|fencing|panel|panels|gate|garage\s+door|car|van|lorry|truck|"
    r"container|pallet|machinery|machine|tree|trees|branch|branches|trunk|limb)\b"
    r"[^.!?]{0,30}"
    r"\b(?:fallen|fell|come\s+down|came\s+down|collapsed|toppled|tumbled|gave\s+way)\b"
    r"[^.!?]{0,20}\b(?:on|onto)\b[^.!?]{0,15}"
    r"\b(?:me|us|myself|yourself|himself|herself|themselves|everybody|everyone|someone|"
    r"somebody|anyone|anybody)\b"
)
CRUSH = (
    CRUSH_HEAVY_ON_A_PRONOUN,
    r"\b(?:collapsed|fallen|fell|come\s+down|came\s+down|tumbled|toppled|gave\s+way|give\s+way)\b"
    r"[^.!?]{0,30}\b(?:and|,|with)\b[^.!?]{0,25}"
    r"(?:" + "|".join(CRUSH_ON_A_PERSON) + r")"
    r"[^.!?]{0,25}\b(?:under|underneath|trapped|stuck|pinned|buried)\b",
    r"\b(?:fallen|fell|came\s+down|come\s+down|collapsed|toppled|toppled\s+over)\b[^.!?]{0,20}"
    r"\b(?:on|onto)\b[^.!?]{0,15}"
    r"(?:" + "|".join(CRUSH_ON_A_PERSON) + r")",
    r"\b(?:someone|somebody|a\s+(?:man|woman|child|kid|person)|my\s+\w+|he|she|they|i)\b"
    r"[^.!?]{0,25}\b(?:crushed|pinned|buried|trapped)\b[^.!?]{0,15}\b(?:by|under|underneath)\b",
    r"\b(?:crushed|pinned)\s+(?:by|under)\b[^.!?]{0,25}"
    r"\b(?:machine|machinery|truck|van|car|lorry|wall|ceiling|roof|beam|scaffold\w*|slab|"
    r"container|pallet|forklift|tractor|rubble|debris)\b",
)
CRUSH_OFF = (
    r"\b(?:duvet|blanket|quilt|covers|pillow|cushions?|bed|toddler|cat|dog|puppy|kitten)\b",
)
CRUSH_HARD = (
    r"\b(?:machine\w*|truck|van|car|lorry|wall|walls|ceiling|roof|beam|scaffold\w*|slab|"
    r"container|pallet|forklift|tractor|rubble|debris|tree|branch|gate|lift|door)\b",
)

MY_OWN_PART = (
    r"\bmy\s+(?:arm|arms|leg|legs|hand|hands|face|side|foot|feet|mouth|eye|eyes|lip|lips|cheek|"
    r"shoulder|hip|knee|grip|voice|speech|vision|tongue|fingers|toes)\b",
    r"\b(?:i|im|i'm)\b[^.?!]{0,14}\b(?:can'?t|cannot|couldn'?t|struggling\s+to|unable\s+to)\s+"
    r"(?:see|walk|feel|talk|speak|hold|move|smile|swallow)\b",
    r"\b(?:i|im|i'm)\b[^.?!]{0,8}\b(?:have|ve|'ve)\s+(?:gone|become)\s+(?:weak|numb|blind)\b",
)

PET_WEAK = (
    r"\b(?:on\s+)?(?:one|his|her|its|their|the|left|right)\s+side\b",
    r"\b(?:gone|gone\s+all|has\s+gone|have\s+gone)\s+weak\b",
    r"\b(?:is|are|seems|looks|been)\s+weak\s+(?:on|in|down)\b",
    r"\b(?:half|one\s+half)\s+of\s+(?:his|her|its|their)\s+(?:body|face)\b",
    r"\bdroop\w*|\bdropping\b",
    r"\bdragging\b|\bdragged\b",
    r"\btilt(?:ed|ing)\b",
    r"\b(?:back|front|hind)\s+legs?\b",
)
