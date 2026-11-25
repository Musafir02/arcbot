# Bulk knowledge schema

Arcai has two knowledge layers. The original rule modules live in `bot/modules` and keep their priority. The bulk layer lives in `bot/bulk/data` and is only used when no original module gives a real answer.

The bulk layer is plain Python data. There is no model, no embedding, no vector store, and no cache file. `bot/bulk/index.py` reads the data once per process and builds a token index in memory.

## Folder layout

```text
bot/bulk/data/
  food/
    boiling_and_steaming/
      __init__.py
      _domain.json
      boiling_eggs.py
      steaming_vegetables.py
      ... 48 more modules
    ... 9 more domains
  ... 19 more categories
```

The full target is 20 categories, 10 domains per category, and 50 modules per domain: 10,000 modules.

The category and domain folder names must match the values inside every module and the manifest.

## One module

A module is a `.py` file with only these assignments:

```python
MODULE = "food.boiling_and_steaming.boiling_eggs"
CATEGORY = "food"
DOMAIN = "boiling_and_steaming"
TOPIC = "boiling eggs"
PRIORITY = 5000
ANSWERS = ("cooking-and-food",)
ITEMS = (
    (
        (
            "how long does it take to boil an egg",
            "how many minutes should i boil an egg for",
            "... eight more patterns ...",
        ),
        "For a soft yolk, simmer a medium egg for about 4 minutes. For a jammy yolk, give it 6 to 7 minutes, and for a firm yolk, 8 to 9 minutes. Cool the egg in cold water before peeling.",
    ),
    "... nine more items ...",
)
```

`bot/bulk/EXAMPLE.py` is a complete reference module with 10 items and 100 patterns.

### Fields

| Field | Rule |
| --- | --- |
| `MODULE` | `category.domain.file_name` without `.py`. Must match the file path. |
| `CATEGORY` | One of the 20 category folders. |
| `DOMAIN` | One of the 10 domain folders inside the category. |
| `TOPIC` | Short lowercase phrase that names the subject. ASCII, at most 80 characters. |
| `PRIORITY` | Always the integer `5000`. The dispatcher, not the module, owns the real priority. |
| `ANSWERS` | A one-item tuple with a label from `bot/knowledge/__init__.py`. |
| `ITEMS` | Exactly 10 items. Each item is `(patterns, answer)`. |

Each `patterns` value is a tuple of exactly 10 real phrasings. Each `answer` is one string.

A module therefore carries 100 phrasings and 10 answers.

## Pattern rules

- Lowercase ASCII only.
- 12 to 110 characters, 3 to 16 words.
- No leading or trailing whitespace, no double spaces.
- No `?`, `!`, or `.` at the end.
- No filler words such as `question`, `pattern`, `placeholder`, `example`, `test`, `todo`, `tbd`, `fixme`, `lorem`.
- Every pattern must name the topic in some way, using at least one content word from `TOPIC`.
- The 10 patterns of one module must be different after normalisation. Stopwords, plurals, `-ing`, `-ed`, and US spellings are reduced by the matcher, so do not submit two patterns that collapse to the same tokens.
- Write how a real person would ask. Do not write keyword lists.
- Do not copy a pattern between modules. The full validator checks this across all 10,000 modules.

## Answer rules

- ASCII, 80 to 500 characters.
- One to three sentences.
- Plain text only: no markdown, no bullets, no URLs, no code, no placeholders.
- No `as an AI`, `I think`, `I believe`, or `in my opinion`.
- British spelling: `colour`, `favourite`, `organise`, `centre`, `litre`, `metre`, `tyre`, `holiday`, `biscuit`, `chips`, `aubergine`, `coriander`, `mum`, `maths`, `grey`.
- Give a direct, useful answer. If the honest answer is "it depends", say what it depends on and give the common cases.
- Do not invent a precise number, date, price, dose, or law. Use a range or say when to check locally.
- Health, law, money, and safety answers must stay general and tell the reader when to get a qualified person involved.

## Domain manifest

Every domain folder has `_domain.json`:

```json
{
  "category": "food",
  "domain": "boiling_and_steaming",
  "title": "Boiling and steaming",
  "modules": [
    {"file": "boiling_eggs", "title": "Boiling eggs"},
    {"file": "steaming_vegetables", "title": "Steaming vegetables"}
  ]
}
```

`modules` must list exactly the 50 module files, without `.py`, and each entry needs a short title.

## Topic labels

`ANSWERS` uses one of the labels returned by `bot.knowledge.topics()`:

```text
cars conditions cooking cooking-and-food creative entertainment everyday-help
family-and-parenting fitness food-and-drink friends-and-relationships
garden-and-plants garden-tools geography-and-travel health health-and-fitness
history home-and-diy kept-animals kits-and-claims language-and-writing
maths-and-numbers meat-in-a-card money nature-and-weather nursing opinions pets
safety school-and-study science shopping sleep small-talk sport technology
travel work
```

Pick the closest label. The label is for broad routing and memory, not for matching.

## Validation

From the repository root:

```bash
python tools/validate_bulk.py --domain food/boiling_and_steaming
python tools/validate_bulk.py --all --duplicates
python tools/validate_bulk.py --complete --duplicates
```

`--domain` checks the files currently present and does not require the manifest or all 50 modules. Use it while writing a domain.

`--all` requires every existing domain to have 50 modules and a valid `_domain.json`.

`--complete` additionally requires 200 domains, 10,000 module files, 1,000,000 usable patterns, and 100,000 answers.

## How matching works

`bot/bulk/text.py` lowercases, strips accents, expands common contractions, removes stopwords, maps US spellings to UK spellings, and reduces plurals and verb endings to a canonical token.

`bot/bulk/index.py` stores one posting list per token. A query first takes the rarest tokens, prunes the candidate patterns, then scores each candidate on:

- how much of the pattern the query covers
- how much of the query the pattern covers
- how many adjacent word pairs agree
- how rare the shared words are

A match is accepted only when the score and the coverage are high and the best candidate is clearly ahead of the second. Otherwise the dispatcher returns `None` and the normal Arcai modules answer.

`bot/modules/bulk_dispatch.py` runs at `PRIORITY = -999.9`. Original answers at priority `0` or higher always win. The dispatcher only beats the greeting fallback at `-1000`.
