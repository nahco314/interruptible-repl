import argparse
from pathlib import Path

from interruptible_repl.repl import run


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("repl_path", type=Path)
    parser.add_argument("code")
    parser.add_argument("--output-path", "-o", default=None, type=Path)
    args = parser.parse_args()

    run(args.repl_path, args.code, output_path=args.output_path)


if __name__ == "__main__":
    main()
