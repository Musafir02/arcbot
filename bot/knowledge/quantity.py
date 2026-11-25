import re

UNITS = frozenset("""
kg kgs kilo kilos g gram grams gm gms lb lbs pound pounds st stone stones
l litre litres liter liters ml cl cm mm m metre metres meter meters km
""".split())

AFTER_A_FIGURE = re.compile(
    r"\b\d+(?:[.,]\d+)?\s*(?:kg|kgs|kilo|kilos|g|gram|grams|gm|gms|lb|lbs|pound|pounds|st|stone"
    r"|stones|l|litre|litres|ml|cl|cm|mm|metre|metres|km)\b", re.I)


def a_figure_with_a_unit(understood=None, text=""):
    numbers = (understood or {}).get("numbers") or []
    for number in numbers:
        if not isinstance(number, dict):
            continue
        unit = str(number.get("unit") or "").strip().lower()
        if unit in UNITS:
            return True
    body = text or str((understood or {}).get("clean") or (understood or {}).get("text") or "")
    return bool(AFTER_A_FIGURE.search(body))
