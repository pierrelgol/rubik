import logging as log
from pathlib import Path

from src.parser import Parser
from src.movement import Moves
from src.cli import Cli, Config
from src.generator import generate_random_moves
from src.renderer import Renderer


def inputs_from_file(maybe_file_path: Path | None) -> list[Moves] | None:
    if file_path := maybe_file_path:
        parser = Parser()

        try:
            parser.parse(file_path.absolute())
        except Exception as e:
            log.error(f"{e}")
            return None

        return parser.value
    else:
        return None


def inputs_from_generator(n: int) -> list[Moves]:
    return [generate_random_moves(n)]


def main(argc: int, argv: list[str]) -> None:
    if argc <= 1:
        log.error("Missing arguments.")
        exit(1)

    arguments = Cli()
    parsed: Config

    try:
        parsed = arguments.parse(argc=argc, argv=argv)
    except Exception as e:
        log.error(f"{e}")
        exit(1)

    maybe_inputs: list[Moves] | None = inputs_from_file(parsed.file_path)
    movements: Moves = []

    if inputs := maybe_inputs:
        print(f"Loaded {len(inputs)} scramble sequences from file")
        movements = inputs[0] if inputs else []
        if movements:
            print(
                f"Loaded sequence with {len(movements)} moves: {' '.join(str(m) for m in movements[:10])}{'...' if len(movements) > 10 else ''}"
            )
    elif inputs := inputs_from_generator(n=parsed.generate):
        print(f"Generated random sequence: {' '.join(str(m) for m in inputs[0])}")
        movements = inputs[0]

    renderer = Renderer(width=800, height=600, movements=movements)
    renderer.run()

    return None
