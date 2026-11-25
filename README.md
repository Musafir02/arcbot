# Arcai

Arcai is a rule-based chatbot written in plain Python. It uses no model, no weights, no training, and no API. Every reply comes from hand-written rules, so it runs fully offline and starts in a moment.

This project is based on PyBot from Hugging Face.

## How it works

At startup `bot/runtime.py` imports every file in `bot/modules`.

Each module declares three things:

- `PRIORITY`: a number that decides the order modules are asked
- `ANSWERS`: the topics the module can answer
- `respond(text, memory)`: returns a reply string, or `None` when it has no match

A single turn works like this:

1. Observer modules read the message and update memory.
2. Every module's `respond` is called with the text and a copy of memory.
3. Modules that return a reply become candidates.
4. The arbiter in `bot/modules/arbiter.py` picks one candidate.
5. The memory from the winning module is kept.
6. `after` hooks run and the reply is returned.

If no module matches, Arcai replies with `Hello!`.

## Requirements

- Python 3.8 or newer
- No third-party packages

## Usage

Start the interactive chat:

```bash
python arcbot.py
```

Inside the chat:

| Command | What it does |
| --- | --- |
| `/help` | show the commands |
| `/reset` | clear memory and start again |
| `/exit` | quit |

Ask one question and exit:

```bash
python arcbot.py -p "what is the capital of france?"
```

Pipe several lines, one reply per line:

```bash
printf "who are you?\nwhat is the capital of france?\n" | python arcbot.py
```

Options:

```text
-p, --prompt TEXT   reply to one message and exit
-i, --interactive   keep chatting after the first reply
-s, --seed N        fix the wording choice for repeatable replies
-v, --verbose       show the module and time for each reply
--version           show the version
```

Install it as a command:

```bash
pip install .
arcbot
```

## Project layout

```text
arcbot.py             command line entry point
bot/runtime.py        loads modules and runs one turn
bot/modules/          rule modules, one topic per file
bot/compose/          builds replies
bot/knowledge/        shared knowledge helpers
bot/memory/           conversation memory
bot/understanding/    text normalization and parsing
pyproject.toml        package setup
```

## Adding a module

Create a file in `bot/modules`:

```python
PRIORITY = 1000
ANSWERS = ("geography",)


def respond(text, memory):
    line = text.lower()
    if "capital of france" in line:
        return "Paris."
    return None
```

Modules with a higher `PRIORITY` are asked first. Keep patterns specific so the arbiter has an easy choice.

## License

MIT. See [LICENSE](LICENSE).
