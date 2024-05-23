"""Module for controlling a tank system via serial communication and updating a GUI based on gamepad input.

This module provides functionality for controlling a tank system through
serial communication with an Arduino board. It interfaces with a gamepad
controller to receive input from the user and updates a graphical
user interface (GUI) accordingly.
Represent the controller in the MVC. Uses Singleton.

Typical usage example:

    controls = Controls()
    controls.window.show()
"""

import json
import sys
import threading
from datetime import datetime, timedelta

import inputs
from PySide6 import QtCore
from PySide6.QtCore import QObject

from model.communication import SerialMessenger
from view.window import Window
from .gamepad import XboxController


class Controls(QObject):
    """Handles the control flow between the gamepad input and the application window.

    This class manages the connection between a gamepad and the application, including
    serial communication setup, signal-slot connections, and user interface interactions.

    Attributes:
        window: The main application window.
        comms: An instance of SerialMessenger for serial communication.
        gamepad: An instance of XboxController for handling gamepad inputs.
        send: A threading.Thread for handling background serial communication.
    """
    def __init__(self) -> None:
        """Initializes the Controls class, setting up the window, ports, gamepad, and communication.
        Connects the signals with the according slots.
        """
        super().__init__()

        self.window = Window()

        port = self.check_previous_ports() or self.window.handle_port_selection_dialog()
        if not port:
            sys.exit()

        self.save_ports_to_json(port)

        if not inputs.devices.gamepads:
            self.window.critical_dialog("No Gamepad Connected", "You did not connect any Gamepad")
            sys.exit()

        self.comms = SerialMessenger(port, baud_rate=9600)

        self.gamepad = XboxController()

        self.gamepad.leftJoystickPos.connect(self.left_joystick_move_slot)
        self.gamepad.rightJoystickPos.connect(self.right_joystick_move_slot)

        self.gamepad.bChanged.connect(self.b_clicked)
        self.gamepad.xChanged.connect(self.x_clicked)
        self.gamepad.l2_pressed.connect(self.l2_pressed)
        self.gamepad.r2_pressed.connect(self.r2_pressed)

        self.send = threading.Thread(target=self.comms.print_data, daemon=True)
        self.send.start()

    @classmethod
    def load_ports_from_json(cls) -> dict:
        """Load previously saved port data from JSON file.

        Returns:
            dict: A dictionary containing port data loaded from the JSON file.
                If the file doesn't exist, an empty dictionary is returned.
        """
        try:
            with open("../ports.json", "r", encoding="utf-8") as f:
                data = json.load(f)
            return data
        except FileNotFoundError:
            return {}

    @classmethod
    def save_ports_to_json(cls, port: str) -> None:
        """Save the selected port to a JSON file with timestamp.

        Args:
            port (str): The selected port to be saved to the JSON file.
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        with open("../ports.json", "w", encoding="utf-8") as f:
            json.dump({"port": port, "timestamp": timestamp}, f)

    def check_previous_ports(self) -> str:
        """Check if a port was previously selected within a time frame of 5 minutes.

        Returns:
            str: The previously selected port if it was selected within the
                specified time frame and is available; otherwise, an empty string.
        """
        ports_data = self.load_ports_from_json()

        if "timestamp" in ports_data and "port" in ports_data:
            timestamp = datetime.strptime(ports_data["timestamp"], "%Y-%m-%d %H:%M:%S")
            if datetime.now() - timestamp < timedelta(minutes=5) and ports_data["port"] in SerialMessenger.all_ports():
                previous_port = ports_data["port"]
                return previous_port

        return ""

    @QtCore.Slot(float)
    def l2_pressed(self, r: float):  # pylint: disable=missing-function-docstring
        if r > 0.1:
            self.comms.tank.sound = 1
        else:
            self.comms.tank.sound = 0

        self.window.update_gui("button_sound")

    @QtCore.Slot(float)
    def r2_pressed(self, r: float):  # pylint: disable=missing-function-docstring
        if r > 0.1:
            self.comms.tank.water = 1
        else:
            self.comms.tank.water = 0

        self.window.update_gui("button_water")

    @QtCore.Slot(float, float)
    def left_joystick_move_slot(self, x: float, y: float):  # pylint: disable=missing-function-docstring
        self.comms.tank.speed1 = x
        self.comms.tank.speed2 = y
        self.window.update_gui("left_joystick", x, y)

    @QtCore.Slot(float, float)
    def right_joystick_move_slot(self, x: float, y: float):  # pylint: disable=missing-function-docstring
        self.comms.tank.tower_x = x
        self.comms.tank.tower_y = y
        self.window.update_gui("right_joystick", x, y)

    @QtCore.Slot(int)
    def b_clicked(self, val: int):  # pylint: disable=missing-function-docstring
        self.comms.tank.sth = val
        self.window.update_gui("button_sth")

    @QtCore.Slot(int)
    def x_clicked(self, val: int):  # pylint: disable=missing-function-docstring
        self.comms.tank.light = val
        self.window.update_gui("button_light")
