import sys

from .runtime import reply


def main():
    memory = {}
    for line in sys.stdin:
        try:
            answer = reply(line.rstrip("\r\n"), memory)
            answer = " ".join(str(answer).split()) or "Hello!"
        except Exception:
            answer = "Hello!"
        print(answer, flush=True)


if __name__ == "__main__":
    main()
