import json
import threading
from datetime import datetime, timedelta

import inputs
from PySide6 import QtCore
from PySide6.QtCore import Signal, QObject
from PySide6.QtWidgets import QMessageBox

from Communication import SerialMessenger
from Window import Window
from gamepad_code import XboxController


class Controls(QObject):
    second_signal = Signal()

    def __init__(self):
        super().__init__()

        self.window = Window()

        port = self.check_previous_ports() or self.window.handle_port_selection_dialog()
        if not port:
            exit()

        self.save_ports_to_json(port)

        if not inputs.devices.gamepads:
            self.no_gamepad()

        self.comms = SerialMessenger(port, baud_rate=9600, communication_possible=True)

        self.gamepad = XboxController()

        self.gamepad.leftJoystickPos.connect(self.left_joystick_move_slot)
        self.gamepad.rightJoystickPos.connect(self.right_joystick_move_slot)

        self.gamepad.bChanged.connect(self.b_clicked)
        self.gamepad.xChanged.connect(self.x_clicked)
        self.gamepad.l2_pressed.connect(self.l2_pressed)
        self.gamepad.r2_pressed.connect(self.r2_pressed)

        self.send = threading.Thread(target=self.comms.print_data, daemon=True)
        self.send.start()

    def no_gamepad(self):
        QMessageBox.critical(
            self.window,
            "No Gamepad Connected",
            "You did not connect any Gamepad",
            buttons=QMessageBox.Ok,
            defaultButton=QMessageBox.Ok,
        )
        exit()

    @classmethod
    def load_ports_from_json(cls):
        try:
            with open("ports.json", "r") as f:
                data = json.load(f)
            return data
        except FileNotFoundError:
            return {}

    @classmethod
    def save_ports_to_json(cls, port):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        with open("ports.json", "w") as f:
            json.dump({"port": port, "timestamp": timestamp}, f)

    def check_previous_ports(self):
        ports_data = self.load_ports_from_json()

        if "timestamp" in ports_data and "port" in ports_data:
            timestamp = datetime.strptime(ports_data["timestamp"], "%Y-%m-%d %H:%M:%S")
            if datetime.now() - timestamp < timedelta(minutes=5) and ports_data["port"] in SerialMessenger.all_ports():
                previous_port = ports_data["port"]
                return previous_port

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
        self.comms.tank.speed1 = x
        self.comms.tank.speed2 = y
        self.window.update_gui("left_joystick", x, y)

    @QtCore.Slot(float, float)
    def right_joystick_move_slot(self, x, y):
        self.comms.tank.tower_x = x
        self.comms.tank.tower_y = y
        self.window.update_gui("right_joystick", x, y)

    @QtCore.Slot(int)
    def b_clicked(self, val):
        self.comms.tank.sth = val
        self.window.update_gui("button_sth", 0, 0)

    @QtCore.Slot(int)
    def x_clicked(self, val):
        self.comms.tank.light = val
        self.window.update_gui("button_light", 0, 0)
