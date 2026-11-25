from .lookup import a_food_is_being_kept, entry

ANSWERS = ("home-and-diy",)

_PAINT_WORD = ("paint", "paints", "painted", "painting", "repaint", "repainting", "re-paint",
               "gloss", "glossing", "glossed", "satin", "eggshell", "undercoat", "undercoating",
               "primer", "priming", "primed", "varnish", "varnishing", "varnished", "coating")

_A_FINISH = ("gloss", "glossy", "satin", "eggshell", "sheen", "matt", "matte", "undercoat",
             "primer", "primed", "varnish", "varnished", "lacquer", "lacqered", "lacquered",
             "oil", "oiled", "mdf")

_A_SURFACE = ("door", "doors", "cupboard", "cupboards", "kitchen", "skirting", "skirtings",
              "banister", "banisters", "bannister", "bannisters", "woodwork", "radiator",
              "radiators", "wall", "walls", "ceiling", "ceilings", "room", "rooms", "floor",
              "floors", "floorboard", "floorboards", "window", "windows", "frame", "frames",
              "sill", "sills", "windowsill", "furniture", "table", "tables", "chair", "chairs",
              "shelf", "shelves", "shed", "fence", "fences", "gate", "gates", "bedroom",
              "bathroom", "hallway", "stairs", "stair", "handrail", "architrave", "trim",
              "wardrobe", "wardrobes", "cabinet", "cabinets", "drawer", "drawers", "toy",
              "toys", "car", "cars", "bike", "bicycle")

_A_ACCIDENT = ("carpet", "carpets", "rug", "rugs", "sofa", "sofas", "couch", "settee",
               "curtain", "curtains", "cushion", "cushions", "clothes", "clothing", "shirt",
               "shirts", "jeans", "trousers", "jacket", "jackets", "hands", "hand", "hair",
               "skin", "fingers", "fingernails", "nails", "washing machine", "bath", "sink",
               "tiles", "tile", "tiling", "grass", "patio", "drive", "driveway")

_A_WAIT = ("how long", "take to dry", "takes to dry", "dry", "dries", "drying", "dried",
           "recoat", "re-coat", "between coats", "touch dry", "hard", "cure", "curing",
           "seconds", "minutes", "hours", "days")

_A_STRIPPER = ("remove", "removing", "removal", "get off", "take off", "taking off",
               "strip", "stripping", "stripper", "sand off", "sanding off", "peel", "peeling",
               "peeled", "flake", "flaking", "bubble", "bubbling", "blister", "blistering")

_THE_TRIM = ("skirting", "skirtings", "skirting board", "skirting boards", "banister",
             "banisters", "bannister", "bannisters", "woodwork", "architrave", "handrail",
             "handrails", "spindle", "spindles", "balustrade", "picture rail", "dado rail",
             "window sill", "windowsill", "window sills", "windowsills", "sill", "sills",
             "trim", "door frame", "door frames")

_ON_THE_WAY = ("on", "onto", "off", "getting", "goes", "going", "got", "spilt", "spilled",
               "splash", "splashes", "splashed", "drips", "dripping", "runs", "running",
               "from", "under", "behind", "against", "down", "near", "round", "around")

_A_MARK = ("stain", "stains", "stained", "mark", "marks", "knot", "knots", "rust", "rusty",
           "nicotine", "tar", "smoke", "grease", "oily", "biro", "pen", "marker", "crayon",
           "felt tip", "felt pen", "watermark", "watermarks", "tide mark", "tide marks")

_A_LEAKING = ("leak", "leaks", "leaking", "leaked", "damp", "damp patch", "damp patches",
              "water", "rain", "raining", "roof", "gutter", "gutters", "pipe", "pipes", "burst",
              "condensation", "mould", "mold", "mouldy", "moldy", "flood", "flooded")

_A_OVER = ("paint over", "painting over", "paint on top of", "cover", "covering",
           "showing through", "shows through", "showing up", "coming through", "come through",
           "bleeding through", "bleeds through", "seeping through", "block", "blocking",
           "stain block", "stainblock", "hiding")


def _words(understood):
    if not isinstance(understood, dict):
        return ()
    return [str(word).lower().strip(",.;:!?") for word in (understood.get("words") or ())]


def _paint_is_the_subject(understood):
    if not isinstance(understood, dict):
        return False
    return not a_food_is_being_kept(understood)


def _a_finish_with_no_surface(understood):
    if not _paint_is_the_subject(understood):
        return False
    words = _words(understood)
    if not any(word in _A_FINISH for word in words):
        return False
    if any(word in _A_SURFACE for word in words):
        return False
    if any(word in _A_ACCIDENT or word in _A_WAIT or word in _A_STRIPPER for word in words):
        return False
    return True


def _the_paint_has_sealed_it(understood):
    if not _paint_is_the_subject(understood):
        return False
    return any(word in _PAINT_WORD for word in _words(understood))


def _the_trim_is_what_is_painted(understood):
    if not _paint_is_the_subject(understood):
        return False
    words = _words(understood)
    for at, word in enumerate(words):
        if word not in _PAINT_WORD:
            continue
        for said in words[at + 1:at + 5]:
            if said in _ON_THE_WAY:
                break
            if said in _THE_TRIM:
                return True
    return False


def _a_stain_under_the_coat(understood):
    if not _paint_is_the_subject(understood):
        return False
    words = _words(understood)
    if not any(word in _A_MARK for word in words):
        return False
    if any(word in _A_ACCIDENT or word in _A_LEAKING for word in words):
        return False
    return any(word in _A_OVER or word in _A_FINISH or word == "paint" or word == "painting"
               for word in words)


ENTRIES = [
entry("painted-shut",
      (("painted shut", "stuck shut", "sealed shut", "glued shut", "paint has sealed",
        "sealed with paint", "stuck with paint", "glued with paint", "paint in the gap",
        "paint in the cracks", "wont open", "won't open", "cannot open", "cant open",
        "can't open", "stuck fast", "jammed", "wont close", "won't close", "wont shut",
        "won't shut", "hard to close", "doesnt close", "doesn't close"),
       ("door", "doors", "front door", "back door", "drawer", "drawers", "cupboard door",
        "cupboard doors", "hatch", "lid")),
      "Score round the edge with a sharp knife where the paint has bridged it to the frame - down "
      "both sides, across the top, then along the bottom - and it will come free with a push "
      "rather than a shoulder. Then sand the paint off the edge and out of the rebate back "
      "to the wood, and rub a candle, a bar of soap or a little wax along the edge so the next "
      "coat cannot glue it again. If it is still tight afterwards, take a millimetre at a time "
      "off the edge with a plane or a sanding block, and prime the bare wood so it does not "
      "swell when the room gets damp. A lock or a handle painted over wants scoring round the "
      "same way before it will turn.",
      bias=2,
      avoid=("car", "cars", "van", "fridge", "freezer", "oven", "microwave", "washing machine",
             "dishwasher", "jar", "bottle", "glue", "superglue", "adhesive", "silicone",
             "caulk", "key", "keys", "lock", "locks", "locked out", "shut up", "shed door",
             "leak", "leaks", "leaking", "damp", "damp patch", "water", "rain", "raining",
             "roof", "gutter", "gutters", "pipe", "pipes", "condensation", "mould", "mold",
             "mouldy", "moldy", "plaster", "brick", "bricks", "brickwork", "ceiling", "flood",
             "flooded", "stain", "stains", "stained", "spilled", "spill", "scrub", "wipe off",
             "get it off", "remove", "removing", "clean off",
             "window", "windows", "sash", "sash window", "casement", "sill", "frame", "frames"),
      guard=_the_paint_has_sealed_it),

entry("a-coat-over-a-finish",
      (("paint over", "painting over", "paint on top of", "painting on top of", "over gloss",
        "over the gloss", "over satin", "over eggshell", "over old paint", "over the old paint",
        "over a finish", "gloss over", "satin over", "matt over", "matte over", "eggshell over",
        "brush marks", "brushmarks", "brush strokes", "brushstrokes", "brush lines",
        "stopping brush marks", "no brush marks"),
       ("gloss", "glossy", "satin", "eggshell", "sheen", "matt", "matte", "undercoat",
        "primer", "priming", "primed", "varnish", "varnished", "lacquer", "lacquered", "paint",
        "painting", "painted", "coat", "coats", "wood", "wooden", "mdf")),
      "Sand it dull first: new paint needs a key to grip, so take the shine off old gloss with "
      "120 grit, wipe off the dust, then one coat of undercoat and your topcoat. A water-based "
      "satin goes on after the sanding alone and dries in a couple of hours; oil gloss straight "
      "onto old gloss is the way to get peeling in a year. Brush marks come from too much paint "
      "on a cheap brush, so thin it a little if it drags and keep the brush moving one way.",
      bias=3,
      avoid=("what colour", "what color", "which colour", "which color", "colour", "colours",
             "color", "colors", "better", "worse", "which is", "matt or gloss", "gloss or matt",
             "satin or gloss", "gloss or satin", "eggshell or gloss", "wallpaper", "wall",
             "walls", "ceiling", "ceilings", "room", "rooms", "bedroom", "bathroom", "hallway",
             "kitchen", "tiles", "tile", "tiling", "grout", "damp", "mould", "mold", "dulux",
             "farrow", "little greene", "buy", "bought", "cost", "price", "cheap", "litre",
             "litres", "how much", "how many coats") + _A_ACCIDENT + _A_WAIT + _A_STRIPPER,
      guard=_a_finish_with_no_surface),

entry("the-trim-is-what-is-painted",
      (("paint the skirting", "paint skirting", "paint skirting boards", "painting the skirting",
        "painting skirting boards", "paint my skirting", "gloss the skirting",
        "gloss the skirting boards", "paint the banister", "paint banisters",
        "painting the banister", "painting the banisters", "paint the woodwork",
        "painting the woodwork", "paint woodwork", "gloss the banister", "gloss the woodwork",
        "paint the architrave", "paint the window sill", "paint the windowsill",
        "paint a banister", "paint a bannister", "paint a spindle", "paint a handrail",
        "paint an architrave", "paint a door frame", "paint a skirting",
        "paint the door frame", "paint the trim", "paint the handrail", "paint the spindles",
        "paint", "painting", "painted", "repaint", "repainting", "gloss", "glossing", "satin",
        "undercoat", "primer"),
       _THE_TRIM),
      "Sand them, wipe the dust off and run masking tape along the carpet, then brush with the "
      "grain in long strokes and a light load on the brush so it does not run onto the wall. Two "
      "thin coats beat one thick one, and satin or eggshell is easier to wipe than gloss. If you "
      "are doing the walls too, do the woodwork first.",
      bias=4,
      ask=("how", "what", "which", "should", "can", "best", "way", "sand", "sanding", "prep",
           "prepare", "method", "start", "need to", "give", "im", "i'm", "i am", "im just",
           "just painting", "just glossing", "want to", "wanna", "going to", "gonna"),
      avoid=("stop paint", "paint getting", "getting paint", "getting", "keep paint", "keep",
             "protect", "protecting", "mask", "masking", "cut in", "cutting in", "neatly",
             "neat", "splash", "splashes", "splashed", "spillage", "drips", "dripping",
             "clean", "cleaning", "cleaner", "clean off", "off the", "dust", "dusty",
             "wipe", "remove", "removing", "strip", "stripping", "sanding off", "colour",
             "color", "what colour", "which colour", "how much", "cost", "price", "buy"),
      guard=_the_trim_is_what_is_painted),

entry("a-stain-under-the-coat",
      (
       ("over a stain", "over the stain", "over stains", "over old stains", "over a mark",
        "over the mark", "over marks", "over rust", "over the rust", "over nicotine",
        "cover", "covering", "showing through", "shows through", "showing up",
        "coming through", "come through", "bleeding through", "bleeds through", "seeping through",
        "stain block", "stainblock", "block the stain", "block a stain", "hiding"),
       ("stain", "stains", "stained", "mark", "marks", "knot", "knots", "rust", "rusty",
        "nicotine", "tar", "smoke", "grease", "oily", "biro", "pen", "marker", "crayon",
        "felt tip", "felt pen", "watermark", "watermarks", "tide mark", "tide marks", "wood",
        "wooden", "door", "doors", "skirting", "ceiling", "wall", "walls", "table", "shelf")),
      "Scrub it back first - sugar soap for grease or nicotine, a light sand for a mark in the "
      "wood - then seal it with a stain block: shellac or an aluminium primer, because ordinary "
      "undercoat lets the mark creep back through in a month. Two thin coats of block, then your "
      "finish. A knot wants the resin scraped out and shellac over it, and rust wants sanding "
      "back to bare metal and a rust-killing primer before the topcoat.",
      bias=2,
      avoid=(
             "ceiling", "ceilings", "wall", "walls", "roof", "keeps", "kept", "keep coming back",
             "how do i get", "get out", "get off", "out of", "off the", "off my", "remove",
             "removing", "clean", "cleaning", "scrub out", "washing", "wash",
             "colour", "color", "which colour", "what colour", "how much", "cost", "price",
             "buy") + _A_ACCIDENT + _A_LEAKING + _A_WAIT,
      guard=_a_stain_under_the_coat),
]
