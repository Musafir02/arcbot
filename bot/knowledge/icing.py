import re

from .lookup import entry

ANSWERS = ("cooking-and-food",)

ICING = ("frosting", "frostings", "icing", "icings", "buttercream", "butter cream", "ganache",
         "cream cheese icing", "cream cheese frosting", "glace icing")

ICING_KEEP = ("keep", "keeps", "keeping", "kept", "last", "lasts", "lasting", "how long",
              "store", "stores", "stored", "storing", "freeze", "freezes", "frozen",
              "overnight", "room temperature", "ahead", "ahead of time", "day before",
              "night before", "make it the day before", "make ahead", "sit out", "sat out",
              "left out", "out overnight", "shelf life", "still ok", "still good", "gone off",
              "go off", "goes off")

_FROSTING_UP = re.compile(r"\b(?:frosting|frosted|icing|iced) up\b|\bice building up\b", re.I)


def _not_a_freezer_frosting_up(understood):
    line = (understood.get("clean") or understood.get("text") or "")
    return not _FROSTING_UP.search(line)

NOT_THE_ICING = ("icing sugar", "sugar paste", "frosting mix", "buttercream powder",
                 "powdered sugar", "confectioners sugar", "fondant icing sugar")

SET_ICING = ("royal icing", "sugar paste", "writing icing", "piping icing", "ready to roll icing",
             "glace icing", "glacé icing", "fondant", "marzipan")

ENTRIES = [
    entry("icing-keeps",
          (ICING, ICING_KEEP),
          "Buttercream or ganache keeps 3 to 4 days in a sealed tub in the fridge, or 2 months "
          "in the freezer: thaw it in the fridge overnight and beat it again, because it splits "
          "when it is cold. Cream cheese frosting is the short one at 2 to 3 days, and it does "
          "not freeze well. Keep an iced cake in a tin rather than the fridge, where it sweats.",
          avoid=NOT_THE_ICING,
          guard=_not_a_freezer_frosting_up,
          bias=3),
    entry("icing-that-sets",
          (SET_ICING, ICING_KEEP),
          "Royal icing sets hard: keep it in an airtight tub at room temperature for about 2 "
          "weeks, or freeze it for up to 3 months, and cover the surface with cling film "
          "straight away because it starts to crust as soon as it meets the air. Sugar paste "
          "keeps 2 to 3 weeks in a sealed bag, and a drop of water is what revives a dry one. "
          "Neither belongs in the fridge - the damp makes both go sticky.",
          avoid=NOT_THE_ICING,
          bias=3),
]
