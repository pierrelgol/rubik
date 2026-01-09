import pyray
from src.cube import Cube
from src.camera import OrbitCamera
from src.cube_visual import CubeVisual
from src.movement import Moves, Movement


class Renderer:
    width: int
    height: int
    cube: Cube
    orbit_camera: OrbitCamera
    visual: CubeVisual
    movements: Moves
    current_move_index: int
    is_animating: bool
    animation_progress: float
    animation_duration: float
    animating_move: Movement | None
    animation_direction: int

    def __init__(self, width: int = 800, height: int = 600, movements: Moves | None = None):
        self.width = width
        self.height = height
        self.cube = Cube()
        self.orbit_camera = OrbitCamera()
        self.visual = CubeVisual(self.cube)
        self.movements = movements if movements is not None else []
        self.current_move_index = -1
        self.is_animating = False
        self.animation_progress = 0.0
        self.animation_duration = 0.3
        self.animating_move = None
        self.animation_direction = 1

    def run(self) -> None:
        pyray.set_config_flags(pyray.ConfigFlags.FLAG_MSAA_4X_HINT)
        pyray.init_window(self.width, self.height, "Rubik's Cube Solver")
        pyray.set_target_fps(60)

        while not pyray.window_should_close():
            self._update()
            self._draw()

        pyray.close_window()

    def _update(self) -> None:
        self.orbit_camera.update()
        self._update_animation()
        self._handle_movement_navigation()

    def _update_animation(self) -> None:
        if not self.is_animating:
            return

        delta_time = pyray.get_frame_time()
        self.animation_progress += delta_time / self.animation_duration

        if self.animation_progress >= 1.0:
            self._complete_animation()

    def _complete_animation(self) -> None:
        if self.animating_move is None:
            return

        if self.animation_direction == 1:
            self.cube.move(self.animating_move)
            self.current_move_index += 1
        else:
            self.cube.move(self.animating_move.inverse())
            self.current_move_index -= 1

        self.is_animating = False
        self.animation_progress = 0.0
        self.animating_move = None

    def _start_animation(self, movement: Movement, direction: int) -> None:
        self.is_animating = True
        self.animation_progress = 0.0
        self.animating_move = movement
        self.animation_direction = direction

    def _handle_movement_navigation(self) -> None:
        if not self.movements or self.is_animating:
            return

        if pyray.is_key_pressed(pyray.KeyboardKey.KEY_RIGHT):
            if self.current_move_index < len(self.movements) - 1:
                next_move = self.movements[self.current_move_index + 1]
                self._start_animation(next_move, direction=1)

        elif pyray.is_key_pressed(pyray.KeyboardKey.KEY_LEFT):
            if self.current_move_index >= 0:
                current_move = self.movements[self.current_move_index]
                self._start_animation(current_move, direction=-1)

    def _draw(self) -> None:
        pyray.begin_drawing()
        pyray.clear_background(pyray.RAYWHITE)
        pyray.begin_mode_3d(self.orbit_camera.camera)
        pyray.draw_grid(10, 1.0)

        if self.is_animating and self.animating_move:
            self.visual.draw_animated(
                self.animating_move, self.animation_progress, self.animation_direction
            )
        else:
            self.visual.draw()

        pyray.end_mode_3d()
        pyray.draw_fps(10, 10)
        self._draw_movement_info()
        pyray.end_drawing()

    def _draw_movement_info(self) -> None:
        if not self.movements:
            pyray.draw_text("No moves loaded", 10, 40, 20, pyray.DARKGRAY)
            return

        current_pos = self.current_move_index + 1
        total_moves = len(self.movements)
        position_text = f"Move: {current_pos}/{total_moves}"
        pyray.draw_text(position_text, 10, 40, 20, pyray.DARKGRAY)

        if self.current_move_index >= 0:
            current_move = self.movements[self.current_move_index]
            move_text = f"Current: {current_move}"
            pyray.draw_text(move_text, 10, 65, 20, pyray.DARKBLUE)

        if self.current_move_index < len(self.movements) - 1:
            next_move = self.movements[self.current_move_index + 1]
            next_text = f"Next: {next_move}"
            pyray.draw_text(next_text, 10, 90, 16, pyray.GRAY)

        pyray.draw_text("← → : Navigate moves", 10, self.height - 30, 16, pyray.DARKGRAY)
