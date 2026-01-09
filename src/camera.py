import math
import pyray


class OrbitCamera:
    distance: float
    angle_h: float
    angle_v: float
    sensitivity: float
    camera: pyray.Camera3D

    def __init__(self, distance: float = 8.0) -> None:
        self.distance = distance
        self.angle_h = math.pi / 4
        self.angle_v = math.pi / 4
        self.sensitivity = 0.005
        self.camera = self._create_camera()

    def _create_camera(self) -> pyray.Camera3D:
        x = self.distance * math.cos(self.angle_v) * math.sin(self.angle_h)
        y = self.distance * math.sin(self.angle_v)
        z = self.distance * math.cos(self.angle_v) * math.cos(self.angle_h)

        camera = pyray.Camera3D(
            pyray.Vector3(x, y, z),
            pyray.Vector3(0.0, 0.0, 0.0),
            pyray.Vector3(0.0, 1.0, 0.0),
            45.0,
            pyray.CameraProjection.CAMERA_PERSPECTIVE,
        )
        return camera

    def _update_position(self) -> None:
        x = self.distance * math.cos(self.angle_v) * math.sin(self.angle_h)
        y = self.distance * math.sin(self.angle_v)
        z = self.distance * math.cos(self.angle_v) * math.cos(self.angle_h)
        self.camera.position = pyray.Vector3(x, y, z)

    def update(self) -> None:
        if pyray.is_mouse_button_down(pyray.MouseButton.MOUSE_BUTTON_LEFT):
            delta = pyray.get_mouse_delta()
            self.angle_h -= delta.x * self.sensitivity
            self.angle_v += delta.y * self.sensitivity
            self.angle_v = max(-math.pi / 2 + 0.1, min(math.pi / 2 - 0.1, self.angle_v))
            self._update_position()
