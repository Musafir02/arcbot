import re

from ..knowledge.lookup import find
from ..understanding import understand

PRIORITY = 1200
ANSWERS_INSTEAD = ("cooking", "food-and-drink", "home-and-diy")

A_CAKE = re.compile(
    r"(?<![a-z])(?:cake|cakes|sponge|gateau|cupcake|cupcakes|victoria sponge|"
    r"victoria sandwich|madeira|loaf cake|sandwich cake)(?![a-z])", re.I)
BETWEEN = re.compile(
    r"(?<![a-z])(?:filling|fill|filled|between the layers|between the two|in the middle|"
    r"the middle of|middle of it|layer|layers|layer it|two layers|three layers|split|"
    r"split it|sandwich it|halve|in half|what cream|which cream|what jam|cream goes|"
    r"jam goes|goes between|goes in the middle)(?![a-z])", re.I)
NOT_ASKING = re.compile(
    r"\b(?:why|sank|sink|sunk|sinking|stodgy|dense|heavy|dry|burn|burnt|undercooked|raw|gummy|"
    r"domed|dropped|didnt rise|didn't rise|flat|stale|birthday|vegan|gluten|egg free|"
    r"no eggs|cupcake cases|icing|frosting|whip|whipping|myself|himself|herself|a slice|"
    r"a piece of|how long|keep|keeps|last|freeze|fridge|calorie|calories|how many|many people|"
    r"serves|feed|tin size|what size tin|instead of the egg)\b", re.I)

NOT_THE_CAKE_ROW = frozenset((
    "recipe-lemon-drizzle", "amount-in-a-dish", "plan-followup", "hair-cut-yourself",
    "half-of-a-number", "bakes",
))

THE_FILLING = (
    "Jam and buttercream, jam first: a thin layer of jam stops the two halves sliding, then "
    "buttercream on top of it - about 3 tablespoons of jam and 150g of buttercream for a 20cm "
    "cake. Split the sponge by pushing cocktail sticks in at the height you want all the way "
    "round, then cut to them with a long serrated knife, turning the cake as you go so the line "
    "meets itself. A chocolate cake takes ganache instead - 100g dark chocolate melted into 100ml "
    "double cream, cooled until it holds - and fresh cream with fruit is the best filling there "
    "is, though it wants making on the morning you eat it.")


def asks_about_its_layers(said):
    if not isinstance(said, dict):
        return False
    if said.get("kind") not in (None, "question", "request", ""):
        return False
    text = " ".join(
        str(part) for part in (said.get("clean"), said.get("text")) if isinstance(part, str))
    if isinstance(said.get("words"), (list, tuple)):
        text = text + " " + " ".join(str(word) for word in said["words"])
    if not text.strip():
        return False
    return bool(A_CAKE.search(text) and BETWEEN.search(text) and not NOT_ASKING.search(text))


def respond(text, memory):
    if not isinstance(text, str) or not isinstance(memory, dict):
        return None
    said = understand(text, memory)
    if not asks_about_its_layers(said):
        return None
    row = _the_row(text, memory)
    if row is not None and getattr(row, "id", "") not in NOT_THE_CAKE_ROW:
        return None
    return THE_FILLING


def _the_row(text, memory):
    try:
        return find(understand(text, memory if isinstance(memory, dict) else {}))
    except Exception:
        return None


