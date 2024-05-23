"""Custom Qt Widget for Rotation Control.

This module provides a custom Qt widget to display a pointer
being rotated on the circle. The widget allows users to rotate
a pointer on a circle boundary.

Example usage:
    rotation_widget = RotationWidget()
    layout.addWidget(rotation_widget)
"""

import math
from typing import Tuple, Optional

from PySide6.QtGui import QPainter
from PySide6.QtCore import QRectF, QPointF
from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QColor


def cartesian_to_polar(x: float, y: float) -> Tuple[float, float]:
    """Convert Cartesian coordinates to polar coordinates.

    Args:
        x (float): The x-coordinate.
        y (float): The y-coordinate.

    Returns:
        Tuple[float, float]: The polar coordinates (r, theta).
    """
    r = math.sqrt(x ** 2 + y ** 2)
    theta = math.atan2(y, x)
    return r, theta


def polar_to_cartesian(r: float, theta: float) -> Tuple[float, float]:
    """Convert polar coordinates to Cartesian coordinates.

    Args:
        r (float): The radial distance.
        theta (float): The angle in radians.

    Returns:
        Tuple[float, float]: The Cartesian coordinates (x, y).
    """
    x = r * math.cos(theta)
    y = r * math.sin(theta)
    return x, y


class RotationWidget(QWidget):
    """Custom Qt Widget for Rotation Control.

    Represents a custom Qt widget for rotation control, showing where a pointer is on a circle.

    Attributes:
        joystick_x: An int representing the x-coordinate of the joystick.
        joystick_y: An int representing the y-coordinate of the joystick.
        radius: An int representing the radius of the rotation control area.
        pointer_radius: An int representing the radius of the rotation control pointer.
    """

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        """Initializes the widget.

        Args:
            parent: A QWidget inside which the joystick is going to be.
        """
        super().__init__(parent)
        self.joystick_x = 0
        self.joystick_y = 0

        self.radius = 50
        self.pointer_radius = 10

    def paintEvent(self, event) -> None:  # pylint: disable=unused-argument
        """Paint event handler to draw the joystick widget."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, True)

        bounds = QRectF(-self.radius, -self.radius, self.radius * 2,
                        self.radius * 2).translated(self._center())
        painter.drawEllipse(bounds)

        painter.setBrush(QColor(255, 0, 0, 127))
        painter.drawEllipse(self.pointer())

    def _center(self) -> QPointF:
        """Calculate the center point of the widget.

        Returns:
            QPointF: The center point of the widget.
        """
        return QPointF(self.width() / 2, self.height() / 2)

    def pointer(self) -> QRectF:
        """Define the area of the rotation control pointer.

        Returns:
            QRectF: The area of the rotation control pointer.
        """
        # Calculate the angle from the joystick position
        _, theta = cartesian_to_polar(self.joystick_x, self.joystick_y)
        # Use the angle and y-coordinate to find the position on the circle's edge
        x, y = polar_to_cartesian(self.radius, theta)
        return QRectF(-self.pointer_radius / 2, -self.pointer_radius / 2,
                      self.pointer_radius, self.pointer_radius).translated(self._center() + QPointF(x, -y))

    def set_joystick_position(self, x: float, y: float) -> None:
        """Set the position of the joystick pointer.

        Args:
            x (float): The x-coordinate of the joystick.
            y (float): The y-coordinate of the joystick.
        """
        self.joystick_x = x
        self.joystick_y = y
        self.update()
