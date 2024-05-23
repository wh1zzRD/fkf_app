"""Custom Qt Widget for a Joystick.

This module provides a custom Qt widget, QJoystick, to display a joystick.
The widget allows users to simulate joystick movement by moving a handle within a circular boundary.

Example usage:
    joystick_widget = QJoystick()
    layout.addWidget(joystick_widget)
"""

from typing import Optional

from PySide6.QtGui import QPainter
from PySide6.QtCore import QPointF, QRectF

from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QColor


class QJoystick(QWidget):
    """Custom Qt Widget for Joystick Control.

    Represents a custom Qt widget for joystick control, allowing users to simulate joystick movement.

    Attributes:
        radius (int): represents the radius of the joystick boundary.
        handle_radius (int): represents the radius of the joystick handle.
        handle_x (int): represents the x-coordinate of the joystick handle.
        handle_y (int): represents the y-coordinate of the joystick handle.
        handle_coords (QPointF): represents the coordinates of the joystick handle.
    """
    def __init__(self, parent: Optional[QWidget] = None) -> None:
        """Initializes the QJoystick widget.

        Args:
            parent (QWidget): A QWidget inside which the joystick is going to be.
        """
        super().__init__(parent)
        self.setMinimumSize(100, 100)
        self.grab_center = False
        self.radius = 50
        self.handle_radius = 20

        self.handle_x = 0
        self.handle_y = 0

        self.handle_coords = QPointF(0, 0)

    def paintEvent(self, event) -> None:  # pylint: disable=unused-argument
        """Paint event handler to draw the joystick widget."""
        painter = QPainter(self)
        bounds = QRectF(-self.radius, -self.radius, self.radius * 2,
                        self.radius * 2).translated(self._center())
        painter.drawEllipse(bounds)
        painter.setBrush(QColor(255, 0, 0, 127))
        painter.drawEllipse(self.handle())

    def get_distance(self) -> QPointF:
        """Calculate the distance between the handle and the center.

        Returns:
            QPointF: The distance between the handle and the center.
        """
        res = QPointF(self.handle_coords.x() * self.radius, self.handle_coords.y() * self.radius)
        return res

    def handle(self) -> QRectF:
        """Define the area of the joystick handle.

        Returns:
            QRectF: The area of the joystick handle.
        """
        point = self._center() + self.get_distance() - QPointF(self.handle_radius, self.handle_radius)
        return QRectF(point.x(), point.y(), self.handle_radius * 2, self.handle_radius * 2)

    def _center(self) -> QPointF:
        """Calculate the center point of the widget.

        Returns:
            QPointF: The center point of the widget.
        """
        return QPointF(self.width() / 2, self.height() / 2)

    def set_joystick_position(self, x: float, y: float) -> None:
        """Set the position of the joystick handle."""
        self.handle_coords = QPointF(x, -y)
        self.update()
