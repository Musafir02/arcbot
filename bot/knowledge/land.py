from .lookup import entry

ANSWERS = ("home-and-diy", "money")


ENTRIES = [entry(
    "who-owns-some-land",
    (("who owns", "who owned", "land registry", "title register", "title deeds", "deeds",
      "piece of land", "plot of land", "land next to", "land behind", "field behind",
      "property boundary", "boundary line", "boundary dispute"),
     ("land", "plot", "field", "boundary", "deeds", "register", "property", "garden", "hedge",
      "owns", "owner", "mine", "next door", "neighbour", "neighbors")),
    "In England and Wales the owner is on the title at HM Land Registry: use its Find a property "
    "service, pay about £3, and the title register gives you the owner's name, the price last paid "
    "and the boundaries on a map, without telling them you asked. Scotland is Registers of "
    "Scotland, and Northern Ireland is Land and Property Services. If the plot is unregistered, "
    "the deeds are with the owner or held by the Land Registry, and your council can help you "
    "find out who to ask.",
    avoid=("what is", "what are", "whats", "what does", "meaning", "difference between",
           "define", "explain", "sell", "selling", "sold", "buy land", "buying land",
           "build on", "permission", "planning permission", "mortgage", "stamp duty", "tax",
           "inheritance", "will", "squatter", "adverse possession", "trespass", "fence cost",
           "how much", "cost of",
           "moon", "planet", "space", "orbit", "satellite",
           "buy a piece of land", "buy some land", "buy land", "buying a piece of land",
           "buying some land", "buying land"),
    bias=1)]
