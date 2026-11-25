import re

from .lookup import a_sanding_job, entry

ANSWERS = ("home-and-diy", "garden-and-plants", "maths-and-numbers")

_NUM = r"(\d+(?:\.\d+)?)"

_PAIR = re.compile(
    _NUM + r"\s*(?:m|metres?|meters?|ft|feet|foot|')?\s*(?:x|by|\*|×|and)\s*"
    + _NUM + r"\s*(?:m|metres?|meters?|ft|feet|foot|')?")
_SQUARE = re.compile(_NUM + r"\s*(?:square\s*(?:metres?|meters?|foot|feet|ft)|sq\s*m|sqm|m2|m²)")
_FEET = re.compile(r"ft|feet|foot|'")
_UNIT = re.compile(r"\d\s*(?:m|metres?|meters?|ft|feet|foot|')")

_DEPTH = re.compile(_NUM + r"\s*(mm|cm|in|inch|inches)\b")

_LOOSE = (
    (("gravel", "shingle", "chippings", "chips", "pea gravel", "pea shingle", "pebbles",
      "stones", "slate", "bark", "bark chippings", "woodchip", "wood chips", "mulch", "aggregate"),
     50, 10,
     "A 850kg bulk bag of {thing} covers about 10 square metres at 50mm, and a 25kg bag "
     "about 0.3 square metres",
     "Put a weed membrane down first if you do not want to hoe it, and keep 20mm below the "
     "damp course on a wall so the rain can drain away."),
    (("topsoil", "soil", "loam"), 100, 7,
     "A 850kg bulk bag of {thing} (about 0.7 cubic metres) covers about 7 square metres at "
     "100mm",
     "Screened topsoil, not subsoil, for anything you want to grow; it settles about a fifth, so "
     "fill to slightly proud of the level you want."),
    (("compost", "multipurpose compost", "manure", "composted manure"), 50, 12,
     "A 60 litre bag of {thing} covers about 1 square metre at 50mm, and a 145 litre bag "
     "about 2.5 square metres",
     "For a raised bed, fill the top 300mm with compost and the rest with rougher soil or "
     "rubble at the bottom; a bed one metre by two at 300mm deep takes about 6 bags of 60 "
     "litres."),
    (("sand", "play sand", "sharp sand", "builder's sand"), 50, 0.6,
     "A 25kg bag of {thing} covers about 0.6 square metres at 50mm, and about a tonne and a "
     "half fills a cubic metre",
     "Play sand, washed and graded, for a sandpit rather than builder's sand; cover it at night "
     "so cats and rain leave it alone."),
)

_SLAB = ("Paving slabs",
         "100mm of compacted MOT Type 1, then 30 to 40mm of sharp sand mixed 5 to 1 with cement "
         "as the bed")
def _area(text):
    pair = _PAIR.search(text)
    if pair and _UNIT.search(pair.group(0)):
        one, two = float(pair.group(1)), float(pair.group(2))
        if _FEET.search(pair.group(0)):
            one, two = one * 0.3048, two * 0.3048
        area = one * two
        if 0.2 <= area <= 20000:
            return round(area, 1)
    square = _SQUARE.search(text)
    if square:
        area = float(square.group(1))
        if _FEET.search(square.group(0)):
            area = area * 0.0929
        if 0.2 <= area <= 20000:
            return round(area, 1)
    return None


def _depth_mm(text, default):
    found = _DEPTH.search(text)
    if not found:
        return default
    amount, unit = float(found.group(1)), found.group(2)
    if unit.startswith("mm"):
        depth = amount
    elif unit.startswith("cm"):
        depth = amount * 10
    else:
        depth = amount * 25
    if 10 <= depth <= 400:
        return depth
    return default


_BAG_WORD = {"sand": "bag", "play sand": "bag", "sharp sand": "bag", "builder's sand": "bag"}


def _sizes(value):
    if abs(value - round(value)) < 0.05:
        return "%d" % round(value)
    return ("%.1f" % value).rstrip("0").rstrip(".")


_A_NUMBER = {1: "one", 2: "two", 3: "three", 4: "four", 5: "five", 6: "six", 7: "seven",
             8: "eight", 9: "nine"}
_A_FRACTION = {0.25: "a quarter", 0.5: "a half", 0.75: "three quarters"}


def _a_bag_count(bags, word):
    quarters = round(bags * 4) / 4.0
    whole = int(quarters)
    part = round(quarters - whole, 2)
    if quarters < 0.25:
        return "about a tenth of a %s" % word
    if quarters < 1:
        if part == 0.25:
            return "about a quarter of a %s" % word
        if part == 0.75:
            return "about three quarters of a %s" % word
        return "about half a %s" % word
    if quarters >= 9.5:
        return "about %d %ss" % (round(bags) if bags < 20 else round(bags, -1), word)
    if part == 0.75:
        whole, part = whole + 1, 0
        if whole == 1:
            return "about one %s" % word
        return "about %s %ss" % (_A_NUMBER[whole], word)
    if part:
        return "about %s and %s %ss" % (_A_NUMBER[whole], _A_FRACTION[part], word)
    if whole == 1:
        return "about one %s" % word
    return "about %s %ss" % (_A_NUMBER[whole], word)


def _count(value):
    if value >= 20:
        return "about %d" % round(value, -1)
    if value >= 4:
        return "about %d" % round(value)
    halves = round(value * 2) / 2
    if halves == int(halves):
        word = _A_NUMBER.get(int(halves))
        if word:
            return "about %s" % word
    return "about %s" % (("%.1f" % halves).rstrip("0").rstrip("."))


def _loose_reply(name, understood):
    text = " " + (understood.get("clean") or "") + " "
    names, depth, covers, lead, extra = _LOOSE[0]
    for row in _LOOSE:
        if name in row[0]:
            names, depth, covers, lead, extra = row
            break
    thing = names[0]
    for name_word in sorted(names, key=len, reverse=True):
        if name_word in text:
            thing = name_word
            break
    if thing == "sand" and ("sandpit" in text or "sand pit" in text or "play sand" in text):
        thing = "play sand"
        lead = ("A 25kg bag of play sand covers about 0.6 square metres at 50mm, so a 1.2m square "
                "sandpit filled to 150mm takes about 10 bags")
    lead = lead.format(thing=thing)
    asked = _depth_mm(text, depth)
    area = _area(text)
    per_bag = covers * (depth / float(asked))
    if area:
        bags = area / per_bag
        word = _BAG_WORD.get(thing, "bulk bag")
        return ("%s square metres at %dmm needs %s of %s. %s, and it is worth a tenth more "
                "than the sums say. %s" % (
                    _sizes(area), asked, _a_bag_count(bags, word), thing, lead, extra))
    return ("%s. Measure the area and work out the volume at the depth you want, then divide by "
            "what a bag holds, and order a tenth more than the sums say - a bag never spreads as "
            "far as the label claims. %s" % (lead, extra))


def _slabs_reply(memory, understood):
    text = " " + (understood.get("clean") or "") + " "
    area = _area(text)
    per_square = 4.0
    size = re.search(_NUM + r"\s*(?:mm)?\s*(?:x|by)\s*" + _NUM + r"\s*(?:mm|cm)?", text)
    if size:
        one, two = float(size.group(1)), float(size.group(2))
        if one < 20:
            one *= 1000
        if two < 20:
            two *= 1000
        if 200 <= one <= 1200 and 200 <= two <= 1200:
            per_square = 1e6 / (one * two)
    side = round(1000 / (per_square ** 0.5))
    if area:
        return ("%s square metres needs %s slabs of %dmm, working at %.1f to the square metre, "
                "with a tenth spare for cuts and breakages. Under them: %s." % (
                    _sizes(area), _count(area * per_square * 1.1), side, per_square, _SLAB[1]))
    return ("Work it out at four 500mm slabs to the square metre, six of 400mm and five and a half "
            "of 600 x 300, then add a tenth for cuts and breakages. Under them: %s." % _SLAB[1])


def _turf_reply(memory, understood):
    text = " " + (understood.get("clean") or "") + " "
    area = _area(text)
    if area:
        return ("%s square metres is %s rolls of turf, ordered a few extra for the edges and "
                "any that go thin. Lay it within a day of delivery, water it the same evening, "
                "and keep off it for a fortnight." % (_sizes(area), _count(area * 1.05)))
    return ("Turf rolls cover about a square metre each, so the area in square metres is the "
            "number of rolls, plus a few for the edges and any that go thin. Lay it within a day "
            "of delivery, water it the same evening, and keep off it for a fortnight.")


_ASKS_MATERIAL = ("how much", "how many", "much ", "many ", "do i need", "will i need",
                  "needed", "need for", "covers", "cover a", "how far does", "bags",
                  "how much do i need", "tonne", "tonnes", "bulk bag")

_ASKS_MATERIAL_AVOID = (
    "cost", "costs", "price", "prices", "cheap", "cheapest", "how much does", "how much is",
    "how much are", "quid", "pounds", "£",
    "how do i lay", "how to lay", "how do i clean", "clean", "cleaning", "jet wash",
    "pressure wash", "how do i fix", "repair", "how do i stop weeds", "kill weeds",
)

_MATERIAL_AVOID = (
    "cost", "costs", "price", "prices", "cheap", "cheapest", "how much does", "how much is",
    "how much are", "quid", "pounds", "£",
    "how do i lay", "how to lay", "how do i clean", "clean", "cleaning", "jet wash",
    "pressure wash", "how do i fix", "repair", "how do i stop weeds", "kill weeds",
    "how deep", "how thick", "what depth",
    "mortar", "pointing", "render", "rendering", "cement", "screed", "concrete", "ballast",
    "block paving", "bedding", "patio base", "sand base", "for a base",
    "fish tank", "fish tank gravel", "aquarium", "tank", "pond", "filter",
    "weed membrane", "membrane", "landscape fabric", "sub-base", "type 1",
    "were ", "was ", "did i", "did we", "did he", "did she", "did they", "do i own",
    "do we own", "have i got", "have we got", "had left", "are left", "is left", "left in",
    "left over", "got left", "are on the", "is on the", "went down", "used to",
    "how long", "long does", "long will", "long do", "long should", "long to", "long before",
    "how many hours", "how many days", "how many minutes", "how much time", "wait before",
)

_A_PERSONS_WEIGHT = re.compile(
    r"\b(?:lose|loses|losing|lost|shed|shift|drop|dropped|weigh|weighs|weighing|weight|"
    r"put\s+on|gained?|gaining|diet|diets|dieting|slim|slimming|bmi|calories|kilos?|kg|"
    r"pounds|lbs?|pregnant)\b[^.?!]{0,40}\bstone\b"
    r"|\b(?:half\s+a|a\s+stone\s+and\s+a\s+half|two|three|1|2|3)\s+stone\b"
    r"[^.?!]{0,40}\b(?:weight|lose|lost|heavier|lighter|diet|target|goal)\b", re.I)


_A_MATERIAL_WEIGHT = re.compile(
    r"\b(?:bulk\s+bag|tonne|tonnes|ton\s+of|tons\s+of|bag\s+of|bags\s+of|"
    r"cubic\s+met(?:re|er)|how\s+heavy|a\s+load\s+of)\b", re.I)


_BULK_WEIGHT = (
    (("bark", "woodchip", "wood chip", "mulch"), "about 350kg to 400kg, and it fills close to a "
     "cubic metre and a half"),
    (("compost", "soil", "topsoil", "loam"), "about 700kg to 750kg, which is roughly 0.7 of a "
     "cubic metre"),
    (("sand", "ballast", "sharp sand", "grit sand"), "about 850kg, which is about half a cubic "
     "metre"),
    (("slate", "pebbles", "pebble", "shingle", "chippings", "gravel", "aggregate", "stone",
      "stones"), "about 850kg, which is about half a cubic metre at 20mm"),
)


def _bulk_bag_weight(memory, understood):
    text = " " + str(understood.get("clean") or understood.get("text") or "") + " "
    what, figures = "gravel or sand", "about 850kg, which is about half a cubic metre"
    for names, line in _BULK_WEIGHT:
        hit = next((n for n in sorted(names, key=len, reverse=True)
                    if " " + n + " " in text or " " + n + "s " in text), None)
        if hit:
            what, figures = hit, line
            break
    return ("A bulk bag of " + what + " is " + figures + " - the bags sold as a tonne bag are "
            "filled to about 850kg for stone and sand, because that is what the bag and a "
            "lorry will take, so buy by the bag rather than by the tonne if the weight matters. "
            "That is the same figure the coverage sums use: 850kg of gravel covers about 10 "
            "square metres at 50mm. A 25kg bag is the same material in a bag you can lift, so "
            "34 of them make a bulk bag.")


def _not_a_persons_weight(understood):
    text = " " + str(understood.get("clean") or understood.get("text") or "") + " "
    if _A_MATERIAL_WEIGHT.search(text):
        return True
    return not _A_PERSONS_WEIGHT.search(text)


def _not_a_sanding_job(understood):
    return not a_sanding_job(understood)

ENTRIES = [
    entry("how-much-gravel", (("gravel", "shingle", "chippings", "pea gravel", "pea shingle",
                               "pebbles", "bark", "bark chippings", "woodchip", "mulch",
                               "slate", "stones", "aggregate"),
                              _ASKS_MATERIAL),
          lambda memory, understood: _loose_reply("gravel", understood),
          ask=_ASKS_MATERIAL, avoid=_MATERIAL_AVOID,
          guard=_not_a_persons_weight, bias=2),
    entry("how-much-topsoil", (("topsoil", "soil", "loam"), _ASKS_MATERIAL),
          lambda memory, understood: _loose_reply("topsoil", understood),
          ask=_ASKS_MATERIAL, avoid=_MATERIAL_AVOID, bias=2),
    entry("how-much-compost", (("compost", "multipurpose compost", "manure"), _ASKS_MATERIAL),
          lambda memory, understood: _loose_reply("compost", understood),
          ask=_ASKS_MATERIAL, avoid=_MATERIAL_AVOID,
          bias=2),
    entry("how-much-sand", (("sand", "play sand", "sharp sand"), _ASKS_MATERIAL),
          lambda memory, understood: _loose_reply("sand", understood),
          ask=_ASKS_MATERIAL, avoid=_MATERIAL_AVOID, bias=2, guard=_not_a_sanding_job),
    entry("how-heavy-is-a-bulk-bag",
          (("bulk bag", "bulk bags", "tonne bag", "tonne bags", "builder's bag", "builders bag",
            "1 tonne bag", "one tonne bag", "a tonne", "cubic metre", "cubic yard"),
           ("weigh", "weighs", "weighing", "weight", "heavy", "how much", "how many kilos",
            "kilos", "kg", "what does", "tonne", "ton")),
          _bulk_bag_weight,
          ask=("weigh", "weighs", "weight", "heavy", "how much", "kilos", "kg"),
          avoid=("cost", "costs", "price", "prices", "cheap", "how much does it cost",
                 "delivery", "deliver", "hire", "skip", "van", "trailer", "car", "boot",
                 "lift", "move", "carry", "bag of cement", "sandbag", "dog food"),
          bias=2),
    entry("sand-and-cement-for-a-base",
          (("sand and cement", "sand cement", "mortar mix", "patio base", "patio foundation",
            "base for a patio", "base for the patio", "sand base", "sub base", "sub-base",
            "type 1", "type one", "slab base", "bedding for slabs", "under the slabs",
            "under patio slabs", "under the paving", "under a patio"),
           _ASKS_MATERIAL),
          "A patio slab sits on a full bed of mortar, not on sand alone and never on five dabs: "
          "40mm to 50mm of sharp sand mixed 4 to 1 with cement, so about half a cubic metre of "
          "sharp sand for 10 square metres - roughly 800kg, most of an 850kg bulk bag - with 5 "
          "bags of 25kg cement. Double both for 20 square metres. Mix it stiff enough to hold "
          "the slab when you tap it down with a mallet and lay to a string line, and under a "
          "patio on soil put 75mm to 100mm of compacted type 1 down first, which is the part "
          "that stops it sinking. Sand alone shifts and washes out, which is why patios laid on "
          "it go wobbly in a couple of winters.",
          ask=_ASKS_MATERIAL,
          avoid=_ASKS_MATERIAL_AVOID + ("block paving", "block paved", "block paver",
                                        "block pavers", "paving blocks", "driveway blocks",
                                        "setts", "block paving drive", "paved drive",
                                        "paving the drive",
                                        "wall", "walls", "garden wall", "brick", "bricks",
                                        "brickwork", "bricklaying", "render", "rendering",
                                        "block wall", "breeze block", "footing", "footings"),
          bias=3),
    entry("how-many-slabs", (("slabs", "paving slabs", "paving", "pavers", "flags",
                              "patio slabs", "block paving", "paving stones"),
                             _ASKS_MATERIAL),
          _slabs_reply, ask=_ASKS_MATERIAL, avoid=_MATERIAL_AVOID, bias=2),
    entry("how-much-turf", (("turf", "rolls of turf"), _ASKS_MATERIAL),
          _turf_reply, ask=_ASKS_MATERIAL, avoid=_MATERIAL_AVOID, bias=2),
]

_LAST_TURNS = 3


def _asked_area(memory, understood):
    area = _area(" " + str(understood.get("clean") or understood.get("text") or "") + " ")
    if area:
        return area
    turns = memory.get("turns") if isinstance(memory, dict) else None
    if not isinstance(turns, list):
        return None
    for turn in reversed(turns[-_LAST_TURNS:]):
        if not isinstance(turn, dict):
            continue
        for key in ("reply", "user"):
            area = _area(" " + str(turn.get(key) or "") + " ")
            if area:
                return area
    return None


def _rolls(area, covers, spare=1.1):
    return max(1, int(-(-(area * spare) // covers)))


def _underlay_reply(memory, understood):
    area = _asked_area(memory, understood)
    how = ("Roll it across the room rather than along it, butt the seams without overlapping and "
           "tape the joins. Foam crumb is the cheap default; rubber crumb or felt is worth it "
           "under a thin carpet and over a hard floor.")
    if area:
        rolls = _rolls(area, 15)
        return ("%s square metres needs %s roll%s of underlay, a roll being 15 square metres "
                "(1.37m by 11m), and the tenth extra covers the cuts round the edges and under "
                "the doorway. %s" % (_sizes(area), _count(rolls), "" if rolls == 1 else "s", how))
    return ("Underlay is sold by area: a roll is usually 15 square metres (1.37m by 11m), so "
            "measure the floor and add a tenth for the cuts. %s" % how)


def _grout_reply(memory, understood):
    area = _asked_area(memory, understood)
    how = ("Mix it to the thickness of toothpaste and only as much as you can use in half an "
           "hour, because it goes off in the bucket.")
    if area:
        bags = _rolls(area, 4.5)
        return ("%s square metres needs %s bag%s of grout, 5kg each: a bag does 4 to 5 square "
                "metres of 30cm tiles with 3mm joints, and small tiles or wide joints take about "
                "twice as much. %s" % (_sizes(area), _count(bags), "" if bags == 1 else "s", how))
    return ("A 5kg bag of grout does about 4 to 5 square metres of 30cm tiles with 3mm joints, so "
            "a bathroom floor is one bag and a kitchen wall two; mosaic or wide joints take about "
            "twice as much for the same area. %s" % how)


def _adhesive_reply(memory, understood):
    area = _asked_area(memory, understood)
    how = ("Comb it out in one direction, press each tile on across the ridges, and lift one now "
           "and then to check the back is covered.")
    if area:
        bags = _rolls(area, 4.5)
        return ("%s square metres needs %s bag%s of tile adhesive, 20kg each: a bag covers 4 to "
                "5 square metres with a 6mm notched trowel, and large tiles or a deeper notch "
                "take it nearer 3. %s" % (_sizes(area), _count(bags), "" if bags == 1 else "s", how))
    return ("A 20kg bag of tile adhesive covers about 4 to 5 square metres with a 6mm notched "
            "trowel, so a small bathroom wall is one bag; large tiles, a 10mm notch or "
            "back-buttering take it nearer 3 square metres a bag. %s" % how)


_BAG_AVOID = _MATERIAL_AVOID + (
    "coming out", "come out", "crumbling", "crumbles", "crumbled", "powdery", "discoloured",
    "discolored", "stained", "staining", "mouldy", "mildew", "re do", "redo", "re-do",
    "hack out", "chisel", "hollow", "wont set", "won't set", "not setting", "keeps coming",
    "lifting", "cracked", "cracking", "loose", "uneven", "squeak", "squeaking",
    "underfloor heating", "wet room", "tile cutter", "spacers", "which tile", "what tile",
)

_FLOOR_NAMES = ("carpet", "carpets", "carpeting", "laminate", "laminate flooring",
                "wood flooring", "engineered wood", "vinyl", "vinyl flooring", "lino",
                "linoleum", "flooring", "skirting", "skirting board", "skirting boards",
                "coving", "dado rail", "dado rails", "floor tiles", "tile floor")
_LENGTH_NAMES = ("skirting", "skirting board", "skirting boards", "coving", "dado rail",
                 "dado rails")
_FLOOR_AVOID = _MATERIAL_AVOID + (
    "how much left", "left over", "last", "lasts", "how long does",
)


def _floor_reply(memory, understood):
    text = " " + (understood.get("clean") or "") + " "
    pair = _PAIR.search(text)
    if any(word in text for word in _LENGTH_NAMES):
        if pair:
            one, two = float(pair.group(1)), float(pair.group(2))
            if _FEET.search(pair.group(0)):
                one, two = one * 0.3048, two * 0.3048
            around = 2 * (one + two)
            boards = int(around / 2.4) + 1
            return ("A room %.1fm by %.1fm has %.1f metres round it, so %.1f metres once a couple "
                    "of doorways are taken off - and boards come in 2.4m lengths, so buy %d of "
                    "them. Cut the joints where two boards meet over a straight bit of wall, "
                    "because the joint shows less there than at a corner." % (
                        one, two, around, around - 1.6, boards))
        return ("Skirting, coving and dado rail are bought by the length, not the area: run a tape "
                "right round the room and take off the doorways, about 0.8m each. A doorway takes "
                "the skirting away and the coving carries on over it. Boards come in 2.4m "
                "lengths, so buy whole boards and join them over a straight run, and add one "
                "board for the corners and the cuts.")
    area = _area(text)
    if area:
        waste = round(area * 1.1, 1)
        packs = area * 1.1 / 2.2
        count = _count(packs)
        return ("%s square metres needs %s square metres of carpet or flooring with the tenth "
                "spare for the cuts and the doorway, which is %s packs of laminate at about 2.2 "
                "square metres a pack. A carpet roll is 4m or 5m wide, which is why the shop asks "
                "for the longest and widest measurement of each room rather than the area alone: "
                "a room under 4m wide comes out of one piece, across the width of the roll, and a "
                "wider one needs a join. Keep the offcuts, because a spare pack for a repair "
                "later is worth more than the few pounds it costs." % (
                    _sizes(area), _sizes(waste), count))
    return ("Measure each room on the floor, not on the plan: length times width in metres, and an "
            "L-shaped room as two rectangles added together. Add a tenth for the cuts and the "
            "doorway, so 12 square metres of floor takes 13.2 square metres of carpet, or six "
            "packs of laminate at 2.2 square metres a pack. A carpet roll is 4m or 5m wide, so "
            "the shop wants the longest and the widest measurement of each room as well as the "
            "area, and a room wider than the roll needs a join.")


_CONCRETE_NAMES = ("concrete", "postcrete", "post mix", "postmix", "cement", "ballast",
                   "concrete mix", "ready mix", "readymix", "mot type 1", "hardcore",
                   "sub base", "subbase")
_CONCRETE_ASKS = _ASKS_MATERIAL + ("bags of", "how many bags", "how much concrete",
                                   "how much ballast", "how much cement", "how much postcrete")
_KIND_ASKS = ("which", "what kind", "what type", "best", "recommend", "suitable", "should i get",
              "should i use",
              "what concrete", "what postcrete", "what cement", "what mortar", "what ballast",
              "what mix", "what ratio")
_CONCRETE_JOBS = ("fence post", "fence posts", "gate post", "post", "posts", "post hole",
                  "post holes", "shed", "shed base", "sheds", "base", "bases", "slab", "slabs",
                  "foundation", "foundations", "footing", "footings", "drive", "driveway",
                  "path", "patio", "wall", "garage")
_CONCRETE_AVOID = (
    "cost", "costs", "price", "prices", "cheap", "cheapest", "how much does", "how much is",
    "how much are", "quid", "pounds", "£", "quote", "hire", "skip",
    "cracked", "cracking", "crumbly", "dusty", "damp", "rising damp", "render", "rendering",
    "plaster", "mortar", "pointing", "screed", "driveway sealer", "seal",
    "repair", "patch", "filler", "glue", "resin", "anchor", "bolt",
    "broken", "sinking", "sunken", "uneven", "pothole", "weeds",
    "acid", "acidic", "alkaline", "alkali", "ph", "litmus", "neutralise", "neutralize",
    "chemical", "chemicals", "erosion", "co2", "carbon", "emissions", "cure", "curing",
    "brick", "bricks", "block", "blocks", "bricklaying", "brickwork", "masonry",
)


_CONCRETE_SURE = ("concrete", "postcrete", "post mix", "postmix", "concrete mix", "ready mix",
                  "readymix", "cement", "mortar")
_CONCRETE_JOB = re.compile(
    r"\b(?:fence|gate|post|posts|hole|holes|shed|sheds|base|bases|slab|slabs|footing|footings|"
    r"foundation|foundations|drive|driveway|driveways|path|paths|patio|patios|wall|walls|garage|"
    r"garages|floor|floors)\b")


def _concrete_is_what_is_asked(understood):
    said = " " + " ".join(str((understood or {}).get(key) or "").lower()
                          for key in ("clean", "text")) + " "
    if any(word in said for word in _CONCRETE_SURE):
        return True
    return bool(_CONCRETE_JOB.search(said))


def _concrete_reply(memory, understood):
    text = " " + (understood.get("clean") or "") + " "
    mixing = ("Concrete is one part cement to six of ballast by volume - six shovels of ballast to "
              "one of cement, mixed dry first, then water until it holds together - and a cubic "
              "metre takes about 1.75 tonnes of ballast and six or seven 25kg bags of cement, "
              "which is two bulk bags of ballast.")
    if re.search(r"\b(?:fence|gate|post|posts|hole|holes|postcrete|post mix|postmix)\b", text):
        return ("One 20kg bag of Postcrete sets one post: the hole wants to be about 250 to 300mm "
                "across and 600mm (two foot) deep, with 50 to 75mm of gravel in the bottom for "
                "drainage. Stand the post, check it upright with a level on two sides, pour the "
                "dry mix in and add the water on top of it. A thicker post, a gate post or a hole "
                "much wider than that takes two bags. %s" % mixing)
    area = _asked_area(memory, understood)
    if area:
        volume = area * (_depth_mm(text, 100) / 1000.0)
        ballast = volume * 1.75
        cement = volume * 6.5
        return ("%s square metres at %dmm is %.2f cubic metres of concrete: about %.1f tonnes of "
                "ballast and %d bags of cement, or %.0f 25kg bags of ready-mixed concrete. %s" % (
                    _sizes(area), _depth_mm(text, 100), volume, ballast,
                    int(-(-cement // 1)), int(-(-(volume * 2400 / 25) // 1)), mixing))
    return ("Work it out as a volume: length times width times depth in metres, so a base 100mm "
            "thick takes 0.1 cubic metres for every square metre, and a 6 by 8 foot shed is about "
            "4.5 square metres - 0.45 cubic metres, which is one 850kg bulk bag of ballast and "
            "three 25kg bags of cement. A single fence post is one 20kg bag of postcrete. %s" %
            mixing)


ENTRIES += [
    entry("how-much-concrete", (_CONCRETE_NAMES, _CONCRETE_ASKS + _CONCRETE_JOBS),
          _concrete_reply, ask=_CONCRETE_ASKS + _KIND_ASKS, avoid=_CONCRETE_AVOID,
          guard=_concrete_is_what_is_asked, bias=2),
    entry("how-much-underlay", (("underlay", "underlayment", "underlay roll"), _ASKS_MATERIAL),
          _underlay_reply, ask=_ASKS_MATERIAL, avoid=_BAG_AVOID, bias=1),
    entry("how-much-grout", (("grout", "grouting"), _ASKS_MATERIAL),
          _grout_reply, ask=_ASKS_MATERIAL, avoid=_BAG_AVOID, bias=1),
    entry("how-much-tile-adhesive", (("tile adhesive", "adhesive", "tile cement", "thin set",
                                      "thinset", "tile glue"), _ASKS_MATERIAL),
          _adhesive_reply, ask=_ASKS_MATERIAL, avoid=_BAG_AVOID, bias=1),
    entry("how-much-flooring", (_FLOOR_NAMES, _ASKS_MATERIAL),
          _floor_reply, ask=_ASKS_MATERIAL, avoid=_FLOOR_AVOID, bias=1),
]
