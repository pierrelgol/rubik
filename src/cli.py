from argparse import ArgumentParser
from src import __version__
from typing import cast
from pathlib import Path


class Config:
    file_path: Path | None
    generate: int

    def __init__(self, file_path: Path | None, generate: int = 0) -> None:
        self.file_path = file_path
        self.generate = generate


class MissingArguments(Exception):
    pass


class Cli:
    parser: ArgumentParser

    def __init__(self) -> None:
        self.parser = ArgumentParser(
            prog="rubik",
            description="Rubik's Cube solver - finds optimal solutions to scrambled cubes",
        )

        _ = self.parser.add_argument(
            "--version",
            action="version",
            version=f"%(prog)s {__version__}",
        )

        _ = self.parser.add_argument(
            "--generate",
            "-g",
            type=int,
            help="length of the scrambling sequence",
        )

        _ = self.parser.add_argument(
            "--input",
            "-i",
            type=Path,
            help="Input file containing scramble sequences (one per line, # for comments)",
        )

    def parse(self, argc: int, argv: list[str]) -> Config:
        if argc <= 1:
            raise (MissingArguments)
        parsed = self.parser.parse_args(argv[1:])
        file_path = cast(Path | None, parsed.input)
        return Config(file_path=file_path)
