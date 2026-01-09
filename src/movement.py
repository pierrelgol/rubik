from enum import StrEnum
from typing import NamedTuple, override


class Direction(StrEnum):
    UP = "U"
    DOWN = "D"
    LEFT = "L"
    RIGHT = "R"
    FRONT = "F"
    BACK = "B"


class Rotation(StrEnum):
    SIMPLE_CLOCKWISE = ""
    COUNTER_CLOCKWISE = "'"
    DOUBLE_CLOCKWISE = "2"


class Movement(NamedTuple):
    direction: Direction
    rotation: Rotation

    def inverse(self) -> "Movement":
        match self.rotation:
            case Rotation.SIMPLE_CLOCKWISE:
                return Movement(self.direction, Rotation.COUNTER_CLOCKWISE)
            case Rotation.COUNTER_CLOCKWISE:
                return Movement(self.direction, Rotation.SIMPLE_CLOCKWISE)
            case Rotation.DOUBLE_CLOCKWISE:
                # Double rotation is its own inverse
                return Movement(self.direction, Rotation.DOUBLE_CLOCKWISE)

    @override
    def __str__(self) -> str:
        return f"{self.direction.value}{self.rotation.value}"


Moves = list[Movement]


def reverse_moves(initial: Moves) -> Moves:
    return [move.inverse() for move in reversed(initial)]
