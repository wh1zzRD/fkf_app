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

        self.gamepad.leftJoystickPos.connect(self.left_joystick_move_slot)
        # self.gamepad.rightJoystickMove.connect(self.right_joystick_move_slot)
        self.gamepad.rightJoystickPos.connect(self.right_joystick_move_slot)

        self.gamepad.bChanged.connect(self.b_clicked)
        self.gamepad.xChanged.connect(self.x_clicked)
        self.gamepad.l2_pressed.connect(self.l2_pressed)
        self.gamepad.r2_pressed.connect(self.r2_pressed)

        self.window = Window()

        self.current_selected_port = None

        # self.communication_possible = False
        if self.window.selected_port is not None:
            self.comms = SerialMessenger(self.window.selected_port, baud_rate=9600, communication_possible=True)
        else:
            self.comms = SerialMessenger("", baud_rate=9600, communication_possible=False)
        # self.comms = SerialMessenger()

        self.send = threading.Thread(target=self.comms.print_data, daemon=True)
        self.send.start()

    def _monitor_selected_item(self):
        while True:
            if self.window.selected_port != self.current_selected_port:
                self.current_selected_port = self.window.selected_port
                self.comms = SerialMessenger(self.window.selected_port, baud_rate=9600, communication_possible=True)
                print("changed")
            time.sleep(0.1)

    def emit_signal(self):
        self.second_signal.emit()
        time.sleep(1)

    @QtCore.Slot(float)
    def l2_pressed(self, r):
        if r > 0.1:
            self.comms.tank.sound = 1
        else:
            self.comms.tank.sound = 0

        self.window.update_gui("button_sound", 0, 0)

    @QtCore.Slot(float)
    def r2_pressed(self, r):
        if r > 0.1:
            self.comms.tank.water = 1
        else:
            self.comms.tank.water = 0

        self.window.update_gui("button_water", 0, 0)

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

        self.comms.tank.tower_x = x
        self.comms.tank.tower_y = y
        self.window.update_gui("right_joystick", x, y)

    @QtCore.Slot(int)
    def b_clicked(self, val):
        self.comms.tank.sth = val
        self.window.update_gui("button_sth", 0, 0)

    @QtCore.Slot(int)
    def x_clicked(self, val):
        self.comms.tank.light =val
        self.window.update_gui("button_light", 0, 0)
