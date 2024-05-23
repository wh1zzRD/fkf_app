from typing import Optional

from PySide6.QtGui import QPainter
from PySide6.QtCore import QPointF, QRectF

from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QColor


class QJoystick(QWidget):
    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.setMinimumSize(100, 100)
        self.grab_center = False
        self.radius = 50
        self.handle_radius = 20

        self.handle_x = 0
        self.handle_y = 0

        self.handle_coords = QPointF(0, 0)

    def paintEvent(self, event) -> None:  # pylint: disable=unused-argument
        painter = QPainter(self)
        bounds = QRectF(-self.radius, -self.radius, self.radius * 2,
                        self.radius * 2).translated(self._center())
        painter.drawEllipse(bounds)
        painter.setBrush(QColor(255, 0, 0, 127))
        painter.drawEllipse(self.handle())

    def get_distance(self) -> QPointF:
        res = QPointF(self.handle_coords.x() * self.radius, self.handle_coords.y() * self.radius)
        return res

    def handle(self) -> QRectF:
        point = self._center() + self.get_distance() - QPointF(self.handle_radius, self.handle_radius)
        return QRectF(point.x(), point.y(), self.handle_radius * 2, self.handle_radius * 2)

    def _center(self) -> QPointF:
        return QPointF(self.width() / 2, self.height() / 2)

    def set_joystick_position(self, x: float, y: float) -> None:
        self.handle_coords = QPointF(x, -y)
        self.update()
