import pyray
from src.cube import Cube, Color as CubeColor
from src.movement import Direction, Movement, Rotation


COLOR_MAP = {
    CubeColor.WHITE: pyray.Color(255, 255, 255, 255),
    CubeColor.YELLOW: pyray.Color(255, 255, 0, 255),
    CubeColor.RED: pyray.Color(255, 0, 0, 255),
    CubeColor.ORANGE: pyray.Color(255, 165, 0, 255),
    CubeColor.BLUE: pyray.Color(0, 0, 255, 255),
    CubeColor.GREEN: pyray.Color(0, 255, 0, 255),
}


class CubeVisual:
    cube: Cube
    gap: float
    tile_size: float

    def __init__(self, cube: Cube):
        self.cube = cube
        self.tile_size = 0.85
        self.gap = 0.08

    def draw(self) -> None:
        core_size = 3.0
        pyray.draw_cube(pyray.Vector3(0.0, 0.0, 0.0), core_size, core_size, core_size, pyray.BLACK)
        self._draw_rounded_edges()
        self._draw_face(Direction.UP)
        self._draw_face(Direction.DOWN)
        self._draw_face(Direction.FRONT)
        self._draw_face(Direction.BACK)
        self._draw_face(Direction.LEFT)
        self._draw_face(Direction.RIGHT)

    def draw_animated(self, movement: Movement, progress: float, direction: int) -> None:
        core_size = 3.0
        pyray.draw_cube(pyray.Vector3(0.0, 0.0, 0.0), core_size, core_size, core_size, pyray.BLACK)
        self._draw_rounded_edges()
        angle = self._calculate_rotation_angle(movement, progress, direction)

        for face_dir in [
            Direction.UP,
            Direction.DOWN,
            Direction.FRONT,
            Direction.BACK,
            Direction.LEFT,
            Direction.RIGHT,
        ]:
            if face_dir == movement.direction:
                self._draw_face_rotated(face_dir, angle)
            else:
                self._draw_face_with_rotation(face_dir, movement.direction, angle)

    def _calculate_rotation_angle(
        self, movement: Movement, progress: float, direction: int
    ) -> float:
        if movement.rotation == Rotation.SIMPLE_CLOCKWISE:
            base_angle = -90.0
        elif movement.rotation == Rotation.COUNTER_CLOCKWISE:
            base_angle = 90.0
        else:
            base_angle = -180.0

        if direction == -1:
            base_angle = -base_angle

        eased_progress = self._ease_in_out(progress)

        return base_angle * eased_progress

    def _ease_in_out(self, t: float) -> float:
        if t < 0.5:
            return 2 * t * t
        else:
            return 1 - pow(-2 * t + 2, 2) / 2

    def _draw_face_rotated(self, direction: Direction, angle: float) -> None:
        axis, origin = self._get_rotation_axis(direction)

        pyray.rl_push_matrix()

        pyray.rl_translatef(origin.x, origin.y, origin.z)
        pyray.rl_rotatef(angle, axis.x, axis.y, axis.z)
        pyray.rl_translatef(-origin.x, -origin.y, -origin.z)

        self._draw_face(direction)

        pyray.rl_pop_matrix()

    def _draw_face_with_rotation(
        self, face_dir: Direction, rotating_dir: Direction, angle: float
    ) -> None:
        face = self.cube.faces[face_dir]

        affected_tiles = self._get_affected_tiles(face_dir, rotating_dir)

        axis, origin = self._get_rotation_axis(rotating_dir)

        for row in range(3):
            for col in range(3):
                color = face.grid[row][col]
                position = self._get_tile_position(face_dir, row, col)
                pyray_color = COLOR_MAP[color]
                dimensions = self._get_tile_dimensions(face_dir)

                if (row, col) in affected_tiles:
                    pyray.rl_push_matrix()
                    pyray.rl_translatef(origin.x, origin.y, origin.z)
                    pyray.rl_rotatef(angle, axis.x, axis.y, axis.z)
                    pyray.rl_translatef(-origin.x, -origin.y, -origin.z)

                    pyray.draw_cube_v(position, dimensions, pyray_color)
                    pyray.draw_cube_wires_v(position, dimensions, pyray.BLACK)

                    pyray.rl_pop_matrix()
                else:
                    pyray.draw_cube_v(position, dimensions, pyray_color)
                    pyray.draw_cube_wires_v(position, dimensions, pyray.BLACK)

    def _get_rotation_axis(self, direction: Direction) -> tuple[pyray.Vector3, pyray.Vector3]:
        match direction:
            case Direction.UP:
                return pyray.Vector3(0, 1, 0), pyray.Vector3(0, 0, 0)
            case Direction.DOWN:
                return pyray.Vector3(0, -1, 0), pyray.Vector3(0, 0, 0)
            case Direction.FRONT:
                return pyray.Vector3(0, 0, 1), pyray.Vector3(0, 0, 0)
            case Direction.BACK:
                return pyray.Vector3(0, 0, -1), pyray.Vector3(0, 0, 0)
            case Direction.LEFT:
                return pyray.Vector3(-1, 0, 0), pyray.Vector3(0, 0, 0)
            case Direction.RIGHT:
                return pyray.Vector3(1, 0, 0), pyray.Vector3(0, 0, 0)

    def _get_affected_tiles(
        self, face_dir: Direction, rotating_dir: Direction
    ) -> set[tuple[int, int]]:
        affected: set[tuple[int, int]] = set(())

        match rotating_dir:
            case Direction.FRONT:
                if face_dir == Direction.UP:
                    affected = {(2, 0), (2, 1), (2, 2)}
                elif face_dir == Direction.DOWN:
                    affected = {(0, 0), (0, 1), (0, 2)}
                elif face_dir == Direction.LEFT:
                    affected = {(0, 2), (1, 2), (2, 2)}
                elif face_dir == Direction.RIGHT:
                    affected = {(0, 0), (1, 0), (2, 0)}

            case Direction.BACK:
                if face_dir == Direction.UP:
                    affected = {(0, 0), (0, 1), (0, 2)}
                elif face_dir == Direction.DOWN:
                    affected = {(2, 0), (2, 1), (2, 2)}
                elif face_dir == Direction.LEFT:
                    affected = {(0, 0), (1, 0), (2, 0)}
                elif face_dir == Direction.RIGHT:
                    affected = {(0, 2), (1, 2), (2, 2)}

            case Direction.UP:
                if face_dir == Direction.FRONT:
                    affected = {(0, 0), (0, 1), (0, 2)}
                elif face_dir == Direction.BACK:
                    affected = {(0, 0), (0, 1), (0, 2)}
                elif face_dir == Direction.LEFT:
                    affected = {(0, 0), (0, 1), (0, 2)}
                elif face_dir == Direction.RIGHT:
                    affected = {(0, 0), (0, 1), (0, 2)}

            case Direction.DOWN:
                if face_dir == Direction.FRONT:
                    affected = {(2, 0), (2, 1), (2, 2)}
                elif face_dir == Direction.BACK:
                    affected = {(2, 0), (2, 1), (2, 2)}
                elif face_dir == Direction.LEFT:
                    affected = {(2, 0), (2, 1), (2, 2)}
                elif face_dir == Direction.RIGHT:
                    affected = {(2, 0), (2, 1), (2, 2)}

            case Direction.LEFT:
                if face_dir == Direction.UP:
                    affected = {(0, 0), (1, 0), (2, 0)}
                elif face_dir == Direction.DOWN:
                    affected = {(0, 0), (1, 0), (2, 0)}
                elif face_dir == Direction.FRONT:
                    affected = {(0, 0), (1, 0), (2, 0)}
                elif face_dir == Direction.BACK:
                    affected = {(0, 2), (1, 2), (2, 2)}

            case Direction.RIGHT:
                if face_dir == Direction.UP:
                    affected = {(0, 2), (1, 2), (2, 2)}
                elif face_dir == Direction.DOWN:
                    affected = {(0, 2), (1, 2), (2, 2)}
                elif face_dir == Direction.FRONT:
                    affected = {(0, 2), (1, 2), (2, 2)}
                elif face_dir == Direction.BACK:
                    affected = {(0, 0), (1, 0), (2, 0)}

        return affected

    def _draw_rounded_edges(self) -> None:
        radius = 0.01
        half = 1.5

        corners = [
            (-half, -half, -half),
            (half, -half, -half),
            (-half, half, -half),
            (half, half, -half),
            (-half, -half, half),
            (half, -half, half),
            (-half, half, half),
            (half, half, half),
        ]

        for x, y, z in corners:
            pyray.draw_sphere(pyray.Vector3(x, y, z), radius, pyray.BLACK)

        for y, z in [(-half, -half), (half, -half), (-half, half), (half, half)]:
            pyray.draw_cylinder_ex(
                pyray.Vector3(-half, y, z),
                pyray.Vector3(half, y, z),
                radius,
                radius,
                8,
                pyray.BLACK,
            )

        for x, z in [(-half, -half), (half, -half), (-half, half), (half, half)]:
            pyray.draw_cylinder_ex(
                pyray.Vector3(x, -half, z),
                pyray.Vector3(x, half, z),
                radius,
                radius,
                8,
                pyray.BLACK,
            )

        for x, y in [(-half, -half), (half, -half), (-half, half), (half, half)]:
            pyray.draw_cylinder_ex(
                pyray.Vector3(x, y, -half),
                pyray.Vector3(x, y, half),
                radius,
                radius,
                8,
                pyray.BLACK,
            )

    def _draw_face(self, direction: Direction) -> None:
        face = self.cube.faces[direction]

        for row in range(3):
            for col in range(3):
                color = face.grid[row][col]
                position = self._get_tile_position(direction, row, col)
                pyray_color = COLOR_MAP[color]
                dimensions = self._get_tile_dimensions(direction)
                pyray.draw_cube_v(position, dimensions, pyray_color)
                pyray.draw_cube_wires_v(position, dimensions, pyray.BLACK)

    def _get_tile_dimensions(self, direction: Direction) -> pyray.Vector3:
        thickness = 0.1

        match direction:
            case Direction.UP | Direction.DOWN:
                return pyray.Vector3(self.tile_size, thickness, self.tile_size)
            case Direction.FRONT | Direction.BACK:
                return pyray.Vector3(self.tile_size, self.tile_size, thickness)
            case Direction.LEFT | Direction.RIGHT:
                return pyray.Vector3(thickness, self.tile_size, self.tile_size)

    def _get_tile_position(self, direction: Direction, row: int, col: int) -> pyray.Vector3:
        u = (col - 1) * (self.tile_size + self.gap)
        v = -(row - 1) * (self.tile_size + self.gap)
        offset = 1.5

        match direction:
            case Direction.UP:
                return pyray.Vector3(u, offset, -v)
            case Direction.DOWN:
                return pyray.Vector3(u, -offset, v)
            case Direction.FRONT:
                return pyray.Vector3(u, v, offset)
            case Direction.BACK:
                return pyray.Vector3(-u, v, -offset)
            case Direction.LEFT:
                return pyray.Vector3(-offset, v, u)
            case Direction.RIGHT:
                return pyray.Vector3(offset, v, -u)
