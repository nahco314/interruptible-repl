from __future__ import annotations

import sys
from code import InteractiveConsole
from pathlib import Path
from typing import BinaryIO
from typing import Optional

import dill


class REPL(InteractiveConsole):
    @classmethod
    def load(cls, file: BinaryIO, **kwargs) -> REPL:
        repl = dill.load(file, **kwargs)
        return repl

    def dump(self, file: BinaryIO, **kwargs) -> None:
        dill.dump(self, file, **kwargs)

    def runsource(self, source: str, filename="<input>", symbol="single"):
        code = None
        try:
            code = self.compile(source, filename, symbol)
        except (OverflowError, SyntaxError, ValueError):
            # Case 1
            self.showsyntaxerror(filename)
            exit(1)

        if code is None:
            # Case 2
            return True

        # Case 3
        self.runcode(code)
        return False

    def runcode(self, code):
        try:
            exec(code, self.locals)
        except SystemExit:
            raise
        except Exception as e:
            self.showtraceback()
            exit(1)


def run(
    repl_path: Path, code: str, *, output_path: Optional[Path] = None, not_exist_ok=True
) -> None:
    if output_path is None:
        output_path = repl_path

    if not repl_path.exists():
        if not_exist_ok:
            repl_path.touch()
            repl = REPL()
        else:
            raise FileNotFoundError(f"{repl_path} does not exist")
    else:
        with repl_path.open("rb") as repl_file:
            repl = REPL.load(repl_file)

    repl.runsource(code + "\n")

    with output_path.open("wb") as repl_file:
        repl.dump(repl_file)
