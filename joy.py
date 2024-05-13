from PySide6.QtWidgets import QWidget

from PySide6.QtGui import *
from PySide6.QtCore import *


class Joystick(QWidget):
    def __init__(self, radius=50, parent=None):
        super(Joystick, self).__init__(parent)

        self.setMinimumSize(radius * 2, radius * 2)
        self.grabCenter = False
        self.radius = radius

        self.handle_radius = 40
        self.handle_x = 0
        self.handle_y = 0

        self.center = QPointF(self.width() / 2, self.height() / 2)

    def paintEvent(self, event):
        painter = QPainter(self)
        bounds = QRectF(-self.radius, -self.radius, self.radius * 2, self.radius * 2).translated(self.center)
        painter.drawEllipse(bounds)
        painter.setBrush(QColor(255, 0, 0, 127))
        handle = self.handle()
        painter.drawEllipse(handle[0], handle[1], self.handle_radius, self.handle_radius)

    def handle(self):
        return self.center.x() + self.handle_x, self.center.y() + self.handle_y

    def bound_handle(self, point):
        limit_line = QLineF(self.center, point)
        if limit_line.length() > self.radius:
            limit_line.setLength(self.radius)
        return limit_line.p2().x(), limit_line.p2().y()

    def mousePressEvent(self, event):
        handle = QRectF(self.handle_x, self.handle_y, self.handle_radius, self.handle_radius)
        self.grabCenter = handle.contains(event.pos())
        return super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        self.grabCenter = False
        self.handle_x, self.handle_y = 0, 0
        self.update()

    def mouseMoveEvent(self, event):
        if self.grabCenter:
            self.handle_x, self.handle_y = self.bound_handle(event.pos())
            self.update()
