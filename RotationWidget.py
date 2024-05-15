from PySide6.QtGui import *
from PySide6.QtCore import *
import sys
from enum import Enum

from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QColor

import math


def cartesian_to_polar(x, y):
    r = math.sqrt(x ** 2 + y ** 2)
    theta = math.atan2(y, x)
    return r, theta


def polar_to_cartesian(r, theta):
    x = r * math.cos(theta)
    y = r * math.sin(theta)
    return x, y


class RotationWidget(QWidget):

    def __init__(self, parent=None):
        super(RotationWidget, self).__init__(parent)
        self.joystick_x = 0
        self.joystick_y = 0

        self.radius = 50
        self.pointer_radius = 10

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        bounds = QRectF(-self.radius, -self.radius, self.radius * 2,
                        self.radius * 2).translated(self._center())
        painter.drawEllipse(bounds)

        painter.setBrush(QColor(255, 0, 0, 127))
        painter.drawEllipse(self.pointer())

    def _center(self):
        return QPointF(self.width() / 2, self.height() / 2)

    def pointer(self):
        # Calculate the angle from the joystick position
        _, theta = cartesian_to_polar(self.joystick_x, self.joystick_y)
        # Use the angle and y-coordinate to find the position on the circle's edge
        x, y = polar_to_cartesian(self.radius, theta)
        return QRectF(-self.pointer_radius / 2, -self.pointer_radius / 2,
                      self.pointer_radius, self.pointer_radius).translated(self._center() + QPointF(x, -y))

    def set_joystick_position(self, x, y):
        self.joystick_x = x
        self.joystick_y = y
        self.update()
