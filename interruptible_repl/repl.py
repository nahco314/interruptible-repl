from __future__ import annotations

import pickle
from code import InteractiveConsole
from pathlib import Path
from typing import BinaryIO


class REPL(InteractiveConsole):
    @classmethod
    def load(cls, file: BinaryIO, **kwargs) -> REPL:
        repl = pickle.load(file, **kwargs)
        return repl

    def dump(self, file: BinaryIO, **kwargs) -> None:
        pickle.dump(self, file, **kwargs)


def run(repl_path: Path, code: str, *, not_exist_ok=True) -> None:
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

    with repl_path.open("wb") as repl_file:
        repl.dump(repl_file)
