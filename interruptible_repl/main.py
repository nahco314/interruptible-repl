import argparse
from pathlib import Path

from interruptible_repl.repl import run


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("repl_path", type=Path)
    parser.add_argument("code")
    args = parser.parse_args()

    run(args.repl_path, args.code)


if __name__ == "__main__":
    main()
