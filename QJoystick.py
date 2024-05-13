import random

from PySide6.QtGui import *
from PySide6.QtCore import *
import sys
from enum import Enum

from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QColor

from math import cos, sin, radians


class QJoystick(QWidget):
    def __init__(self, parent=None):
        super(QJoystick, self).__init__(parent)
        self.setMinimumSize(100, 100)
        # self.movingOffset = QPointF(0, 0)
        self.grabCenter = False
        self.radius = 50
        self.handle_radius = 20

        self.handle_x = 0
        self.handle_y = 0

        self.handle_coords = QPointF(0, 0)

    def paintEvent(self, event):
        painter = QPainter(self)
        bounds = QRectF(-self.radius, -self.radius, self.radius * 2,
                        self.radius * 2).translated(self._center())
        painter.drawEllipse(bounds)
        painter.setBrush(QColor(255, 0, 0, 127))
        painter.drawEllipse(self.handle())
        # print(self.movingOffset)

    def get_distance(self):
        res = QPointF(self.handle_coords.x() * self.radius, self.handle_coords.y() * self.radius)
        return res

    def handle(self):
        point = self._center() + self.get_distance() - QPointF(self.handle_radius, self.handle_radius)
        return QRectF(point.x(), point.y(), self.handle_radius * 2, self.handle_radius * 2)

        # if self.grabCenter:
        #     return QRectF(self._center().x() - self.handle_radius + self.handle_x, self._center().y() - self.handle_radius + self.handle_y, self.handle_radius * 2, self.handle_radius * 2)
        # return QRectF(self._center().x() - self.handle_radius, self._center().y() - self.handle_radius, self.handle_radius * 2, self.handle_radius * 2)

    def _center(self):
        return QPointF(self.width() / 2, self.height() / 2)

    # @Slot(float, float)
    def setJoystickPosition(self, x, y):
        # print(x_shift, y_shift)
        # x = random.uniform(-1, 1)
        # y = random.uniform(-1, 1)
        self.handle_coords = QPointF(x, -y)
        self.update()

    def _boundJoystick(self, point):
        # x = self._center().x() - point.x()
        # y = self._center().y() - point.y()
        #
        # if abs(y - self._center().y()) > self.radius:

        limit_line = QLineF(self._center(), point)
        if limit_line.length() > self.radius:
            limit_line.setLength(self.radius)
        return limit_line.p2().x() - self._center().x(), limit_line.p2().y() - self._center().y()

    # def mousePressEvent(self, event):
    #     self.grabCenter = self.handle().contains(event.pos())
    #     return super().mousePressEvent(event)
    #
    # def mouseReleaseEvent(self, event):
    #     self.grabCenter = False
    #     # self.movingOffset = QPointF(0, 0)
    #     self.handle_x, self.handle_y = 0, 0
    #     self.update()
    #     # print(self.movingOffset)
    #
    # def mouseMoveEvent(self, event):
    #     if self.grabCenter:
    #         self.handle_x, self.handle_y = self._boundJoystick(event.pos())
    #         self.update()
    #         # print(self.movingOffset)
    #
    # @Slot(float, float)
    # def handle_joystick_move(self, x, y):
    #     # Handle joystick movement here
    #     # You can use x and y to determine the position of the handle
    #     # For example, you can update the position of the handle and repaint the widget
    #     print("Joystick moved:", x, y)
    #     # Update handle position based on x and y values
    #     # Example:
    #     # self.handle_x = x * self.radius
    #     # self.handle_y = y * self.radius
    #     # self.update()
