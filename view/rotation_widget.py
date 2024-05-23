import math
from typing import Tuple, Optional

from PySide6.QtGui import QPainter
from PySide6.QtCore import QRectF, QPointF
from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QColor


def cartesian_to_polar(x: float, y: float) -> Tuple[float, float]:
    r = math.sqrt(x ** 2 + y ** 2)
    theta = math.atan2(y, x)
    return r, theta


def polar_to_cartesian(r: float, theta: float) -> Tuple[float, float]:
    x = r * math.cos(theta)
    y = r * math.sin(theta)
    return x, y


class RotationWidget(QWidget):

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.joystick_x = 0
        self.joystick_y = 0

        self.radius = 50
        self.pointer_radius = 10

    def paintEvent(self, event) -> None:  # pylint: disable=unused-argument
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        bounds = QRectF(-self.radius, -self.radius, self.radius * 2,
                        self.radius * 2).translated(self._center())
        painter.drawEllipse(bounds)

        painter.setBrush(QColor(255, 0, 0, 127))
        painter.drawEllipse(self.pointer())

    def _center(self) -> QPointF:
        return QPointF(self.width() / 2, self.height() / 2)

    def pointer(self) -> QRectF:
        # Calculate the angle from the joystick position
        _, theta = cartesian_to_polar(self.joystick_x, self.joystick_y)
        # Use the angle and y-coordinate to find the position on the circle's edge
        x, y = polar_to_cartesian(self.radius, theta)
        return QRectF(-self.pointer_radius / 2, -self.pointer_radius / 2,
                      self.pointer_radius, self.pointer_radius).translated(self._center() + QPointF(x, -y))

    def set_joystick_position(self, x: float, y: float) -> None:
        self.joystick_x = x
        self.joystick_y = y
        self.update()
