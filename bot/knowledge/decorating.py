
import re

from .lookup import a_food_is_being_kept, entry

ANSWERS = ("home-and-diy",)

PAINT = ("paint", "paints", "painted", "painting", "repaint", "repainting", "gloss", "glossing",
         "emulsion", "satin", "eggshell", "undercoat", "primer", "priming", "woodwork",
         "woodwork", "decorating", "decorate", "decorated", "roller", "rollers", "brush",
         "brushes", "paintbrush", "paintbrushes", "sleeve", "masking tape", "filler", "sander")

GOING_WRONG = ("drip", "drips", "dripping", "dripped", "run", "runs", "running", "ran",
               "sag", "sags", "sagging", "sagged", "curtain", "curtains", "slide", "sliding",
               "slid", "trickle", "trickles", "trickling", "patchy", "uneven", "transfer",
               "showing", "shows", "visible")

A_LEAK = ("leak", "leaks", "leaking", "leaked", "damp", "damp patch", "damp patches", "water",
          "watermark", "water marks", "rain", "raining", "roof", "gutter", "gutters", "pipe",
          "pipes", "burst", "condensation", "mould", "mold", "mouldy", "moldy", "plaster",
          "render", "brick", "bricks", "brickwork", "ceiling tile", "flood", "flooded",
          "overflow", "tank", "radiator leak", "washing machine", "dishwasher")

A_STAIN = ("stain", "stains", "stained", "staining", "spilled", "spill", "spillage", "soaked",
           "soak", "scrub", "wipe off", "get it off", "get off", "remove", "removing", "clean off",
           "cleaning off", "off my hands", "off my skin", "out of my clothes", "out of a carpet",
           "off the floor")

A_DIFFERENT_JOB = ("hole", "holes", "crack", "cracks", "cracked", "skim", "skimming", "plastering",
                   "plasterer", "fill a wall", "wallpaper", "wallpapering", "stripping",
                   "strip the", "how much paint", "litre", "litres", "how many coats",
                   "which colour", "what colour", "farrow", "dulux", "buy", "bought", "cost",
                   "price", "cheap")


_PAINT_WORD = re.compile(
    r"\b(?:" + "|".join(re.escape(word) for word in sorted(PAINT, key=len, reverse=True)) + r")\b")
_DECORATED_SURFACE = re.compile(
    r"\b(?:skirting|skirtings|skirting\ board|skirting\ boards|woodwork|door\ ?frame|door\ ?frames|"
    r"architrave|architraves|picture\ rail|banister|banisters)\b")


def _paint_is_the_subject(understood):
    if not isinstance(understood, dict):
        return False
    if a_food_is_being_kept(understood):
        return False
    said = " ".join(str(one) for one in (understood.get("words") or ())).lower()
    if not said:
        said = str(understood.get("clean") or understood.get("text") or "").lower()
    return bool(_PAINT_WORD.search(said) or _DECORATED_SURFACE.search(said))


_STEPS = {"fill": "fill", "filling": "fill", "filled": "fill", "filler": "fill",
          "patch": "fill", "patching": "fill",
          "sand": "sand", "sanding": "sand", "sanded": "sand", "sandpaper": "sand",
          "smooth": "sand", "smoothing": "sand",
          "prime": "finish", "priming": "finish", "primer": "finish", "undercoat": "finish",
          "varnish": "finish", "varnishing": "finish", "varnished": "finish",
          "oil": "finish", "oiling": "finish", "wax": "finish", "waxing": "finish",
          "stain": "finish", "painting": "finish", "paint": "finish", "gloss": "finish",
          "lacquer": "finish", "coat": "finish", "coats": "finish"}
_ORDER_WORDS = ("first", "before", "after", "or", "between", "then")
_NOT_WOODWORK = ("floor", "floors", "floorboard", "floorboards", "decking", "driveway", "path",
                 "pavement", "wall", "walls", "ceiling", "ceiling", "plaster", "plasterboard",
                 "brick", "bricks", "concrete", "paving", "grout", "car", "cars", "rust",
                 "windscreen", "fence", "gate")


_ASKS_THE_MATERIAL = ("what grit", "which grit", "what sandpaper", "which sandpaper",
                      "what paper", "which paper", "what paint", "which paint", "what varnish",
                      "which varnish", "how many coats", "how long between", "best sandpaper",
                      "best paper", "how much paint", "how much varnish", "what filler",
                      "which filler", "what brush", "which brush")


def _the_order_of_two_steps(understood):
    text = str((understood or {}).get("text") or (understood or {}).get("clean") or "").lower()
    if any(word in text for word in _NOT_WOODWORK):
        return False
    if any(word in text for word in _ASKS_THE_MATERIAL):
        return False
    if not any(word in text for word in _ORDER_WORDS):
        return False
    return len({step for word, step in _STEPS.items() if word in text}) >= 2


def _a_shelf_and_its_brackets(understood):
    text = str((understood or {}).get("text") or (understood or {}).get("clean") or "").lower()
    if "shelf" not in text and "shelves" not in text:
        return False
    if "bracket" not in text and "brackets" not in text:
        return False
    return any(word in text for word in ("first", "before", "or", "then", "put up", "hang"))


ENTRIES = [
entry("paint-runs-and-sags",
      (PAINT, GOING_WRONG),
      "Load less: a third of the bristles wet, half a roller of paint, and lay it off with light "
      "strokes in one direction rather than going back over it. A run is too much paint in one "
      "spot, so scrape the roller back over the tray's ramp every time and don't reload until it "
      "stops giving paint, and keep the brush moving in one direction instead of scrubbing back "
      "and forth. When a run has started, brush it out while it is still wet - lay the brush flat "
      "and drag the run sideways into the dry paint - then leave it alone: going back over paint "
      "as it dries is what leaves the brushmarks. On a ceiling, paint towards yourself and slightly "
      "away from the wall so the last stroke is a pulled one, and thin the paint only if it is "
      "genuinely thick.",
      bias=3,
      avoid=A_LEAK + A_STAIN + A_DIFFERENT_JOB + ("peel", "peels", "peeling", "peeled", "peely",
                                                  "flake", "flakes", "flaking", "flakey", "flaky",
                                                  "bubble", "bubbles", "bubbling", "bubbled",
                                                  "blister", "blisters", "blistering",
                                                  "hobby", "hobbies", "acrylics", "acrylic",
                                                  "watercolour", "watercolors", "canvas",
                                                  "oil painting", "art", "draw", "drawing",
                                                  "learn to paint", "start painting",
                                                  "beginner", "nail", "nails", "nail varnish",
                                                  "car", "cars", "hair", "cake", "icing",
                                                  "kids", "children", "toddler", "spray paint",
                                                  "spraying", "graffiti",
                                                  "drying out", "dried out", "keep paint",
                                                  "keeping paint", "store paint", "storing paint",
                                                  "leftover paint", "left over paint",
                                                  "old paint", "tip", "tin", "tins"),
      guard=_paint_is_the_subject),

entry("roller-splatter",
      (("roller", "rollers", "rolling", "sleeve", "sleeves", "rolling pin"),
       ("splatter", "splatters", "splattering", "spatter", "spatters", "spattering",
        "flick", "flicks", "flicking", "splash",
        "splashes", "splashed", "splashing", "spitting", "spits", "spitting paint", "flinging",
        "throwing", "flies", "flying", "mess", "messy", "dots", "droplets", "spray", "spraying",
        "splatter paint", "tracks", "lines")),
      "Half a roller of paint, a slow push, and roll the excess off on the tray's ramp before "
      "the sleeve touches the wall: a roller splatters because it is overloaded and moving too "
      "fast, and paint spins off the top of a sleeve that is turning at the ceiling. Then roll "
      "from the dry part into the wet in long strokes with light pressure. The sleeve matters "
      "too - short pile for smooth plaster, medium for a light texture, and a long pile holds so "
      "much paint that it throws it - and a brand new cheap sleeve spits fuzz for the first wall, "
      "so wash it out first or wrap tape round your hand and run it over. Sheet the floor and "
      "tape the edges, and any fleck that lands wipes off with a damp cloth while it is wet.",
      bias=3,
      avoid=A_LEAK + A_STAIN + ("pastry", "baking", "dough", "lint", "deodorant", "hair",
                                "paint off", "get paint off", "remove paint", "stripper"),
      guard=_paint_is_the_subject),

entry("paint-on-the-skirting",
      (("skirting", "skirtings", "skirting board", "skirting boards", "woodwork", "door frame",
        "doorframe", "door frames", "architrave", "picture rail", "banister", "banisters",
        "radiator pipe", "socket", "sockets", "light switch", "light switches"),
       ("paint", "paints", "painted", "painting", "roller", "rollers", "brush", "brushes",
        "splash", "splashes", "splashed", "drips", "dripping", "mess", "messy", "marks",
        "keep", "stop", "protect", "cover", "covering", "masking", "tape", "taping", "getting",
        "goes", "going", "cut in", "cutting in", "neat", "neatly")),
      "Press a low-tack masking tape along the top edge of the skirting, working it down into "
      "the join with a fingernail, then cut in with a 2 inch angled brush and brush the last inch "
      "slowly towards the tape rather than at it, so the paint is not pushed underneath. Pull the "
      "tape off at a shallow angle while the paint is still soft - leave it until the paint is "
      "hard and it tears the edge off with it. Anything that does get through: a wet cloth takes "
      "emulsion off a gloss skirting straight away, and once it is dry a sharp scraper or a "
      "fingernail lifts it without marking the gloss. Masking tape, not parcel tape, and not "
      "left on for a week, or it takes the gloss with it when it comes off.",
      bias=3,
      avoid=A_LEAK + A_STAIN + A_DIFFERENT_JOB + ("paint off", "get paint off", "getting paint off",
                                                  "clean paint off", "cleaning paint off",
                                                  "remove paint", "removing paint",
                                                  "off the door", "off the frame", "off the floor",
                                                  "paint the skirting", "paint a skirting",
                                                  "painting the skirting", "painting a skirting",
                                                  "paint my skirting", "painting my skirting",
                                                  "gloss the skirting", "glossing the skirting",
                                                  "skirting tile", "tiles", "tiling", "grout",
                                                  "caulk", "silicone", "rot", "woodworm",
                                                  "how do i fit", "fitting", "replace",
                                                  "replacing", "remove", "removing a",
                                                  "how high", "height"),
      guard=_paint_is_the_subject),

entry("brush-for-paint",
      (("brush", "brushes", "paintbrush", "paintbrushes", "filament", "filaments", "bristle",
        "bristles", "sleeve", "roller"),
       ("gloss", "glossing", "emulsion", "satin", "eggshell", "undercoat", "primer", "paint",
        "paints", "painting", "water based", "waterbased", "oil based", "oilbased", "solvent",
        "cutting in", "cut in", "woodwork", "trim", "skirting", "door", "doors")),
      "Synthetic filaments for anything water-based - emulsion, water-based gloss and satin - and "
      "natural bristle for oil-based gloss, which holds the solvent and lays off flatter without "
      "leaving brushmarks. Width matters more than brand: a 2 inch angled sash brush for cutting "
      "in and for gloss on woodwork, a 3 or 4 inch brush for a wall, and cheap is fine for "
      "emulsion but not for gloss, where a shedding brush leaves hairs in the finish. Between "
      "coats, wrap a water-based brush in a damp cloth inside a bag rather than washing it out "
      "each time, and comb a bristle brush straight after cleaning so it dries in shape.",
      bias=2,
      avoid=("hair", "hairbrush", "beard", "dog", "cat", "pet", "pastry", "basting", "makeup",
             "make up", "blusher", "nail", "toothbrush", "teeth", "broom", "yard brush",
             "clean", "cleaning", "clean a paintbrush", "washing out", "dried out",
             "how do i clean", "buy", "bought", "best brand", "cheap", "price", "cost"),
      guard=_paint_is_the_subject),

entry("thinning-paint",
      (("thin", "thinning", "thinned", "thinner", "thinners", "dilute", "diluting", "water down",
        "water it down", "too thick", "thick", "stiff"),
       ("gloss", "glossing", "emulsion", "satin", "eggshell", "undercoat", "primer", "paint",
        "paints", "painting", "varnish", "lacquer", "solvent", "white spirit", "turps",
        "brush marks", "brushmarks")),
      "White spirit for oil-based gloss, water for water-based paint, and only a little: about "
      "one part white spirit to ten parts paint, stirred in rather than shaken, and no more than "
      "about a tenth of water in emulsion or water-based gloss. More than that and the paint stops "
      "forming a film, so it dries patchy and the sheen goes. Thin only when the paint is "
      "genuinely stiff - a fresh tin that is hard to brush is usually too cold rather than too "
      "thick, so stand it in warm water for ten minutes first, and never thin a primer or an "
      "undercoat to stretch it, because that is what makes it fail.",
      bias=2,
      avoid=A_STAIN + ("gravy", "sauce", "soup", "jam", "cream", "yoghurt", "smoothie", "hair",
                       "blood", "nail varnish", "nail polish", "lose weight", "thinner person",
                       "become thin", "too thin", "underweight", "varnish a floor", "floorboards",
                       "french polish", "car paint", "car", "cars", "spray"),
      guard=_paint_is_the_subject),
entry("prep-before-finish",
      (("sand", "sanding", "sanded", "sandpaper", "sand down", "smooth", "fill", "filling",
        "filled", "filler", "patch", "patching"),
       ("varnish", "varnishing", "varnished", "oil", "oiling", "wax", "waxing", "stain",
        "painting", "paint", "gloss", "lacquer", "prime", "priming", "primer", "undercoat",
        "coat", "coats", "first", "before", "after", "between")),
      "Fill first, then sand, then finish: push the filler into the dents and holes, leave it a "
      "little proud, and sand it back level with the wood once it is hard. Then sand the whole "
      "surface - 120 grit on a block for paint or varnish, 80 to 100 on a filler patch - wipe "
      "the dust off with a tack cloth, and put the first coat on. Sand lightly between coats "
      "with 180 to 240 grit and wipe the dust off again, because that is what makes the last "
      "coat sit flat; leave the final coat alone. On a wall you only need to sand between coats "
      "if there is a run or a bit of grit.",
      guard=_the_order_of_two_steps,
      bias=1),
entry("brackets-then-the-shelf",
      (("shelf", "shelves", "bracket", "brackets", "shelf bracket", "floating shelf"),
       ("first", "before", "or", "then", "put up", "hang", "fix", "fixing")),
      "The brackets go up first. Hold the shelf where you want it, mark the holes through the "
      "brackets with a pencil, take the shelf down, and fix the brackets to the wall with a "
      "fixing that suits it: a wall plug in brick or block, a screw into a stud, or a "
      "hollow-wall anchor in plasterboard with nothing behind it. Then screw the shelf to the "
      "brackets and check it with a spirit level along the shelf itself, not along one bracket.",
      guard=_a_shelf_and_its_brackets,
      bias=1),
]
