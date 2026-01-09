from enum import Enum
from typing import override
from src.movement import Direction, Movement, Rotation


class Color(Enum):
    RED = 1
    YELLOW = 2
    WHITE = 3
    BLUE = 4
    GREEN = 5
    ORANGE = 6


Grid = list[list[Color]]


class Face:
    grid: Grid

    def __init__(self, color: Color) -> None:
        self.grid = [
            [color, color, color],
            [color, color, color],
            [color, color, color],
        ]

    def rotate(self, rotation: Rotation) -> None:
        match rotation:
            case Rotation.SIMPLE_CLOCKWISE:
                self._rotate_clockwise()
            case Rotation.DOUBLE_CLOCKWISE:
                self._rotate_clockwise()
                self._rotate_clockwise()
            case Rotation.COUNTER_CLOCKWISE:
                self._rotate_counter_clockwise()

    def _rotate_clockwise(self) -> None:
        self.grid = [list(row) for row in zip(*self.grid[::-1])]

    def _rotate_counter_clockwise(self) -> None:
        self.grid = [list(row) for row in zip(*[row[::-1] for row in self.grid])]


class Cube:
    faces: dict[Direction, Face]

    def __init__(self) -> None:
        self.faces = {
            Direction("U"): Face(Color.WHITE),
            Direction("D"): Face(Color.YELLOW),
            Direction("F"): Face(Color.RED),
            Direction("B"): Face(Color.ORANGE),
            Direction("L"): Face(Color.BLUE),
            Direction("R"): Face(Color.GREEN),
        }

    def move(self, movement: Movement) -> None:
        direction = movement.direction
        rotation = movement.rotation

        self.faces[direction].rotate(rotation)

        if rotation == Rotation.DOUBLE_CLOCKWISE:
            self._swap_edges(direction)
            self._swap_edges(direction)
        elif rotation == Rotation.COUNTER_CLOCKWISE:
            self._swap_edges(direction)
            self._swap_edges(direction)
            self._swap_edges(direction)
        else:
            self._swap_edges(direction)

    def is_solved(self) -> bool:
        expected = {
            Direction.UP: Color.WHITE,
            Direction.DOWN: Color.YELLOW,
            Direction.FRONT: Color.RED,
            Direction.BACK: Color.ORANGE,
            Direction.LEFT: Color.BLUE,
            Direction.RIGHT: Color.GREEN,
        }

        for direction, expected_color in expected.items():
            face = self.faces[direction]
            for row in face.grid:
                for tile in row:
                    if tile != expected_color:
                        return False
        return True

    def _swap_edges(self, direction: Direction) -> None:
        match direction:
            case Direction.UP:
                self._swap_up_edges()
            case Direction.DOWN:
                self._swap_down_edges()
            case Direction.FRONT:
                self._swap_front_edges()
            case Direction.BACK:
                self._swap_back_edges()
            case Direction.LEFT:
                self._swap_left_edges()
            case Direction.RIGHT:
                self._swap_right_edges()

    def _swap_up_edges(self) -> None:
        front_top = [self.faces[Direction.FRONT].grid[0][i] for i in range(3)]
        right_top = [self.faces[Direction.RIGHT].grid[0][i] for i in range(3)]
        back_top = [self.faces[Direction.BACK].grid[0][i] for i in range(3)]
        left_top = [self.faces[Direction.LEFT].grid[0][i] for i in range(3)]

        for i in range(3):
            self.faces[Direction.FRONT].grid[0][i] = right_top[i]
            self.faces[Direction.RIGHT].grid[0][i] = back_top[i]
            self.faces[Direction.BACK].grid[0][i] = left_top[i]
            self.faces[Direction.LEFT].grid[0][i] = front_top[i]

    def _swap_down_edges(self) -> None:
        front_bot = [self.faces[Direction.FRONT].grid[2][i] for i in range(3)]
        left_bot = [self.faces[Direction.LEFT].grid[2][i] for i in range(3)]
        back_bot = [self.faces[Direction.BACK].grid[2][i] for i in range(3)]
        right_bot = [self.faces[Direction.RIGHT].grid[2][i] for i in range(3)]

        for i in range(3):
            self.faces[Direction.FRONT].grid[2][i] = left_bot[i]
            self.faces[Direction.LEFT].grid[2][i] = back_bot[i]
            self.faces[Direction.BACK].grid[2][i] = right_bot[i]
            self.faces[Direction.RIGHT].grid[2][i] = front_bot[i]

    def _swap_front_edges(self) -> None:
        up_bot = [self.faces[Direction.UP].grid[2][i] for i in range(3)]
        left_right = [self.faces[Direction.LEFT].grid[i][2] for i in range(3)]
        down_top = [self.faces[Direction.DOWN].grid[0][i] for i in range(3)]
        right_left = [self.faces[Direction.RIGHT].grid[i][0] for i in range(3)]

        for i in range(3):
            self.faces[Direction.UP].grid[2][i] = left_right[2 - i]
            self.faces[Direction.LEFT].grid[i][2] = down_top[i]
            self.faces[Direction.DOWN].grid[0][i] = right_left[2 - i]
            self.faces[Direction.RIGHT].grid[i][0] = up_bot[i]

    def _swap_back_edges(self) -> None:
        up_top: list[Color] = [self.faces[Direction.UP].grid[0][i] for i in range(3)]
        right_right: list[Color] = [self.faces[Direction.RIGHT].grid[i][2] for i in range(3)]
        down_bot: list[Color] = [self.faces[Direction.DOWN].grid[2][i] for i in range(3)]
        left_left: list[Color] = [self.faces[Direction.LEFT].grid[i][0] for i in range(3)]

        for i in range(3):
            self.faces[Direction.UP].grid[0][i] = right_right[2 - i]
            self.faces[Direction.RIGHT].grid[i][2] = down_bot[i]
            self.faces[Direction.DOWN].grid[2][i] = left_left[2 - i]
            self.faces[Direction.LEFT].grid[i][0] = up_top[i]

    def _swap_left_edges(self) -> None:
        up_left: list[Color] = [self.faces[Direction.UP].grid[i][0] for i in range(3)]
        front_left: list[Color] = [self.faces[Direction.FRONT].grid[i][0] for i in range(3)]
        down_left: list[Color] = [self.faces[Direction.DOWN].grid[i][0] for i in range(3)]
        back_right: list[Color] = [self.faces[Direction.BACK].grid[i][2] for i in range(3)]

        for i in range(3):
            self.faces[Direction.UP].grid[i][0] = back_right[2 - i]
            self.faces[Direction.BACK].grid[i][2] = down_left[2 - i]
            self.faces[Direction.DOWN].grid[i][0] = front_left[i]
            self.faces[Direction.FRONT].grid[i][0] = up_left[i]

    def _swap_right_edges(self) -> None:
        up_right: list[Color] = [self.faces[Direction.UP].grid[i][2] for i in range(3)]
        front_right: list[Color] = [self.faces[Direction.FRONT].grid[i][2] for i in range(3)]
        down_right: list[Color] = [self.faces[Direction.DOWN].grid[i][2] for i in range(3)]
        back_left: list[Color] = [self.faces[Direction.BACK].grid[i][0] for i in range(3)]

        for i in range(3):
            self.faces[Direction.UP].grid[i][2] = front_right[i]
            self.faces[Direction.FRONT].grid[i][2] = down_right[i]
            self.faces[Direction.DOWN].grid[i][2] = back_left[2 - i]
            self.faces[Direction.BACK].grid[i][0] = up_right[2 - i]

    def apply_moves(self, movements: list[Movement]) -> None:
        for movement in movements:
            self.move(movement)

    @override
    def __str__(self) -> str:
        lines: list[str] = []
        lines.append("Cube state:")
        for direction in Direction:
            lines.append(f"\n{direction.name} face:")
            face = self.faces[direction]
            for row in face.grid:
                lines.append("  " + " ".join(c.name[0] for c in row))
        return "\n".join(lines)
