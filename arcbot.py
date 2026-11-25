import argparse
import os
import random
import sys
import time

__version__ = "0.1.0"

SOURCE_COMMIT = "24cbc0439e07fd015c0747ab3be6e782a42b5c5b"

LOGO = r"""
   ___   ____   ____  ____  ____  _____
  / _ \ |  _ \ / ___||  _ \|  _ \| ____|
 | | | || |_) | \___ \| |_) | |_) |  _|
 | |_| ||  _ <  ___) |  _ <|  _ <| |___
  \___/ |_| \_\|____/|_| \_\|_| \_\_____|
""".strip("\n")
TAGLINE = "I am Arcai, developed by Ibrahim Shaikh. No weights, no training, just rules."

USER_PREFIX = "user: "
BOT_PREFIX = "arcai: "

HINT = "Type a message and press Enter. /reset starts a new conversation, /exit quits."

HELP = """Commands:
  /reset   clear the screen and start again (Arcai forgets what was said)
  /help    show this help
  /exit    quit (Ctrl+D works too)"""


def load_bot():
    try:
        from bot import runtime
    except ModuleNotFoundError as error:
        if error.name != "bot":
            raise
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        from bot import runtime
    return runtime


def answer(runtime, text, memory):
    start = time.perf_counter()
    try:
        result = runtime.turn(text, memory)
        reply = " ".join(str(result["reply"]).split()) or "Hello!"
        module = result.get("module")
    except Exception:
        reply, module = "Hello!", None
    return reply, module, time.perf_counter() - start


def details(module, seconds):
    return "[module: %s | %.0f ms]" % (module or "none", seconds * 1000)


def one_shot(runtime, args):
    reply, module, seconds = answer(runtime, args.prompt, {})
    print(reply, flush=True)
    if args.verbose:
        print(details(module, seconds), file=sys.stderr)


def pipe(runtime, args):
    memory = {}
    for line in sys.stdin:
        reply, module, seconds = answer(runtime, line.rstrip("\r\n"), memory)
        print(reply, flush=True)
        if args.verbose:
            print(details(module, seconds), file=sys.stderr, flush=True)


def opening():
    print(LOGO + "\n")
    print(TAGLINE)
    print(HINT + "\n")


def clear_screen():
    if os.name == "nt":
        os.system("cls")
    else:
        sys.stdout.write("\033[H\033[2J\033[3J")
        sys.stdout.flush()


def chat(runtime, args):
    try:
        import readline
    except ImportError:
        pass
    opening()
    memory = {}
    first = args.prompt
    while True:
        if first is not None:
            text, first = first, None
            print(USER_PREFIX + text)
        else:
            try:
                text = input(USER_PREFIX)
            except (EOFError, KeyboardInterrupt):
                print()
                break
        command = text.strip().lower()
        if command in ("/exit", "/quit", "/bye"):
            break
        if command == "/reset":
            memory = {}
            if args.seed is not None:
                random.seed(args.seed)
            if sys.stdout.isatty():
                clear_screen()
                opening()
            else:
                print("New conversation.\n")
            continue
        if command == "/help":
            print(HELP + "\n")
            continue
        if not command:
            continue
        reply, module, seconds = answer(runtime, text, memory)
        print(BOT_PREFIX + reply)
        if args.verbose:
            print(details(module, seconds))
        print()


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog="arcbot",
        description="Chat with Arcai, a chatbot written in plain Python: no model, no weights.",
        epilog="With no options, Arcai starts an interactive chat. "
               "When input is piped in, it prints one reply per input line.")
    parser.add_argument("-p", "--prompt", metavar="TEXT",
                        help="reply to this one message and exit")
    parser.add_argument("-i", "--interactive", action="store_true",
                        help="with -p: keep chatting after the first reply")
    parser.add_argument("-s", "--seed", type=int, metavar="N",
                        help="seed for Arcai's choice of wording, to get the same replies again")
    parser.add_argument("-v", "--verbose", action="store_true",
                        help="after each reply, show the module that produced it and the time it took")
    parser.add_argument("--version", action="version",
                        version="arcbot %s (bot at commit %s)" % (__version__, SOURCE_COMMIT[:12]))
    args = parser.parse_args(argv)

    if args.seed is not None:
        random.seed(args.seed)
    interactive = (args.prompt is None and sys.stdin.isatty()) or (args.prompt is not None and args.interactive)
    if interactive:
        print("Loading Arcai...", end="", file=sys.stderr, flush=True)
    runtime = load_bot()
    if interactive:
        print("\r" + " " * 16 + "\r", end="", file=sys.stderr, flush=True)
        chat(runtime, args)
    elif args.prompt is not None:
        one_shot(runtime, args)
    else:
        pipe(runtime, args)
    return 0


if __name__ == "__main__":
    sys.exit(main())
