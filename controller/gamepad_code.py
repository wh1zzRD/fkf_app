import math
import threading

from PySide6 import QtCore
from PySide6.QtCore import QObject, Signal

from inputs import get_gamepad


class XboxController(QObject):
    leftJoystickPos = Signal(float, float)
    rightJoystickPos = Signal(float, float)
    l2_pressed = Signal(float)
    r2_pressed = Signal(float)

    buttonAClicked = Signal()
    buttonBClicked = Signal()
    buttonXClicked = Signal()
    buttonYClicked = Signal()

    xChanged = Signal(int)  # Signal to indicate a change in the X button toggle variable
    bChanged = Signal(int)  # Signal to indicate a change in the B button toggle variable

    MAX_TRIG_VAL = math.pow(2, 8)
    MAX_JOY_VAL = math.pow(2, 15)

    def __init__(self) -> None:
        super().__init__()

        self.left_joystick_y = 0
        self.left_joystick_x = 0
        self.right_joystick_y = 0
        self.right_joystick_x = 0
        self.left_trigger = 0
        self.right_trigger = 0
        self.left_bumper = 0
        self.right_bumper = 0
        self.a = 0
        self.x = 0
        self.y = 0
        self.b = 0
        self.left_thumb = 0
        self.right_thumb = 0
        self.back = 0
        self.start = 0
        self.left_d_pad = 0
        self.right_d_pad = 0
        self.up_d_pad = 0
        self.down_d_pad = 0

        self._monitor_thread = threading.Thread(target=self._monitor_controller, args=())
        self._monitor_thread.daemon = True
        self._monitor_thread.start()

        self.prev_left_x = 0
        self.prev_left_y = 0

        # Initialize the toggle variables
        self.toggle_variable_x = 0
        self.toggle_variable_b = 0

        # Connect the signals to the toggle handlers
        self.buttonXClicked.connect(self.toggle_variable_x_handler)
        self.buttonBClicked.connect(self.toggle_variable_b_handler)

    @QtCore.Slot()
    def toggle_variable_x_handler(self):
        # Toggle the X variable between 0 and 1 and emit signal if it changes
        new_value = 1 - self.toggle_variable_x
        if new_value != self.toggle_variable_x:
            self.toggle_variable_x = new_value
            self.xChanged.emit(self.toggle_variable_x)

    @QtCore.Slot()
    def toggle_variable_b_handler(self):
        # Toggle the B variable between 0 and 1 and emit signal if it changes
        new_value = 1 - self.toggle_variable_b
        if new_value != self.toggle_variable_b:
            self.toggle_variable_b = new_value
            self.bChanged.emit(self.toggle_variable_b)

    def _monitor_controller(self) -> None:
        event_handlers = {
            'ABS_Y': self._handle_left_joystick_y,
            'ABS_X': self._handle_left_joystick_x,
            'ABS_RY': self._handle_right_joystick_y,
            'ABS_RX': self._handle_right_joystick_x,
            'ABS_Z': self._handle_left_trigger,
            'ABS_RZ': self._handle_right_trigger,
            'BTN_TL': self._handle_left_bumper,
            'BTN_TR': self._handle_right_bumper,
            'BTN_SOUTH': self._handle_button_a,
            'BTN_NORTH': self._handle_button_y,
            'BTN_WEST': self._handle_button_x,
            'BTN_EAST': self._handle_button_b,
            'BTN_THUMBL': self._handle_left_thumb,
            'BTN_THUMBR': self._handle_right_thumb,
            'BTN_SELECT': self._handle_back,
            'BTN_START': self._handle_start,
            'BTN_TRIGGER_HAPPY1': self._handle_left_d_pad,
            'BTN_TRIGGER_HAPPY2': self._handle_right_d_pad,
            'BTN_TRIGGER_HAPPY3': self._handle_up_d_pad,
            'BTN_TRIGGER_HAPPY4': self._handle_down_d_pad,
        }

        while True:
            events = get_gamepad()
            for event in events:
                handler = event_handlers.get(event.code)
                if handler:
                    handler(event)

                if abs(self.right_joystick_x) > 0.1 or abs(self.right_joystick_y) > 0.1:
                    self.rightJoystickPos.emit(self.right_joystick_x, self.right_joystick_y)
                if abs(self.left_joystick_x) > 0.1 or abs(self.left_joystick_y) > 0.1:
                    self.leftJoystickPos.emit(self.left_joystick_x, self.left_joystick_y)

    def _handle_left_joystick_y(self, event) -> None:
        self.left_joystick_y = event.state / self.MAX_JOY_VAL  # normalize between -1 and 1

    def _handle_left_joystick_x(self, event) -> None:
        self.left_joystick_x = event.state / self.MAX_JOY_VAL  # normalize between -1 and 1

    def _handle_right_joystick_y(self, event) -> None:
        self.right_joystick_y = event.state / self.MAX_JOY_VAL  # normalize between -1 and 1

    def _handle_right_joystick_x(self, event) -> None:
        self.right_joystick_x = event.state / self.MAX_JOY_VAL  # normalize between -1 and 1

    def _handle_left_trigger(self, event) -> None:
        self.left_trigger = event.state / self.MAX_TRIG_VAL  # normalize between 0 and 1
        self.l2_pressed.emit(self.left_trigger)

    def _handle_right_trigger(self, event) -> None:
        self.right_trigger = event.state / self.MAX_TRIG_VAL  # normalize between 0 and 1
        self.r2_pressed.emit(self.right_trigger)

    def _handle_left_bumper(self, event) -> None:
        self.left_bumper = event.state

    def _handle_right_bumper(self, event) -> None:
        self.right_bumper = event.state

    def _handle_button_a(self, event) -> None:
        self.a = event.state
        self.buttonAClicked.emit()

    def _handle_button_y(self, event) -> None:
        self.y = event.state  # previously switched with X
        self.buttonYClicked.emit()

    def _handle_button_x(self, event) -> None:
        self.x = event.state  # previously switched with Y
        if self.x == 1:  # Only emit when the button is pressed down
            self.buttonXClicked.emit()

    def _handle_button_b(self, event) -> None:
        self.b = event.state
        if self.b == 1:  # Only emit when the button is pressed down
            self.buttonBClicked.emit()

    def _handle_left_thumb(self, event) -> None:
        self.left_thumb = event.state

    def _handle_right_thumb(self, event) -> None:
        self.right_thumb = event.state

    def _handle_back(self, event) -> None:
        self.back = event.state

    def _handle_start(self, event) -> None:
        self.start = event.state

    def _handle_left_d_pad(self, event) -> None:
        self.left_d_pad = event.state

    def _handle_right_d_pad(self, event) -> None:
        self.right_d_pad = event.state

    def _handle_up_d_pad(self, event) -> None:
        self.up_d_pad = event.state

    def _handle_down_d_pad(self, event) -> None:
        self.down_d_pad = event.state
