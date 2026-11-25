from .lookup import entry as _entry

ANSWERS = ("cars",)

ENTRIES = [
    _entry("parking-on-the-pavement",
           (("park on the pavement", "parking on the pavement", "pavement", "pavements",
             "park on the verge", "parking on the verge", "verge", "grass verge",
             "footway", "footpaths", "kerb", "curb", "dropped kerb"),
            ("legal", "illegal", "allowed", "allow", "against the law", "law", "permitted",
             "ticket", "fined", "fine", "penalty", "can i", "is it", "is that", "am i",
             "park", "parked", "parking", "ok", "okay")),
           "Parking on the pavement is an offence right across London and in Scotland, and "
           "elsewhere only where a traffic order covers that street - so the signs and lines "
           "on it, and the council's own parking page, are what decide your road, and that is "
           "where to check rather than the country as a whole. Where it is allowed you must "
           "still leave the pavement clear enough for a wheelchair or a pushchair, and blocking "
           "a dropped kerb blocks someone's drive. A ticket for it is a penalty charge notice, "
           "argued in the council's own appeal rather than in a court.",
           ask=("pavement", "pavements", "verge", "grass verge", "footway", "footpaths",
                "kerb", "curb", "dropped kerb"),
           avoid=("trip", "tripped", "tripping", "fell", "fell over", "slipped", "slippy",
                  "icy", "ice", "uneven", "pothole", "potholes", "cracked", "damaged",
                  "injur", "injured", "claim", "compensation", "wheelchair access",
                  "pushed", "buggy", "litter", "dog mess", "graffiti", "fixed", "repair")),
]
