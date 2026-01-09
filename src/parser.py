from pathlib import Path
from src.movement import Direction, Rotation, Movement, Moves


class Parser:
    value: list[Moves] | None

    def __init__(self) -> None:
        self.value = None

    def parse(self, absolute_file_path: Path) -> None:
        self.value = []

        i: int = 0
        with open(file=absolute_file_path) as file:
            while untrimmed_line := file.readline():
                line = untrimmed_line.strip()

                if not line or line.startswith("#"):
                    continue

                moves: Moves = []
                for token in line.split():
                    if parsed := self._movement_from_token(token):
                        moves.append(parsed)
                    else:
                        raise ValueError(f"Invalid move notation: '{token}'")
                self.value.append(moves)
                i += 1

    def _movement_from_token(self, token: str) -> Movement | None:
        if not token or len(token) > 2:
            return None

        try:
            direction = Direction(token[0])
        except ValueError:
            return None

        if len(token) == 1:
            return Movement(direction, Rotation.SIMPLE_CLOCKWISE)

        try:
            rotation = Rotation(token[1])
            return Movement(direction, rotation)
        except ValueError:
            return None
