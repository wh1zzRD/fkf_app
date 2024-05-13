import threading
import time

from PySide6 import QtCore
from PySide6.QtCore import Signal, QObject

from Communication import SerialMessenger
from Window import Window
from gamepad_code import XboxController


class Controls(QObject):
    second_signal = Signal()

    def __init__(self):
        super().__init__()

        self.gamepad = XboxController()

        self.gamepad.leftJoystickMove.connect(self.left_joystick_move_slot)
        self.gamepad.rightJoystickMove.connect(self.right_joystick_move_slot)

        self.gamepad.buttonAClicked.connect(self.a_clicked)
        self.gamepad.buttonBClicked.connect(self.b_clicked)
        self.gamepad.buttonXClicked.connect(self.x_clicked)
        self.gamepad.buttonYClicked.connect(self.y_clicked)

        self.window = Window()

        self.comms = SerialMessenger("COM3", baud_rate=9600)

        self.send = threading.Thread(target=self.comms.print_data, daemon=True)
        self.send.start()

    def emit_signal(self):
        self.second_signal.emit()
        time.sleep(1)

    @QtCore.Slot(float, float)
    def left_joystick_move_slot(self, x, y):
        # send data
        # move the joystick in the app

        self.comms.tank.speed1 = x
        self.comms.tank.speed2 = y
        self.window.update_gui("left_joystick", x, y)

    @QtCore.Slot(float, float)
    def right_joystick_move_slot(self, x, y):
        # send data
        # move the joystick in the app

        self.comms.tank.tower = x
        self.window.update_gui("right_joystick", x, y)

    @QtCore.Slot()
    def a_clicked(self):
        self.comms.tank.water = 1
        self.window.update_gui("button_water", 0, 0)

    @QtCore.Slot()
    def b_clicked(self):
        self.comms.tank.sth = 1
        self.window.update_gui("button_sth", 0, 0)

    @QtCore.Slot()
    def x_clicked(self):
        self.comms.tank.light = 1
        self.window.update_gui("button_light", 0, 0)

    @QtCore.Slot()
    def y_clicked(self):
        self.comms.tank.sound = 1
        self.window.update_gui("button_sound", 0, 0)
