""" A module for interfacing with an Xbox controller and emitting signals based on input events."""

import math
import threading

from PySide6.QtCore import QObject, Signal

from inputs import get_gamepad


class XboxController(QObject):
    """Handles Xbox controller inputs and emits signals for various actions.

    This class monitors the Xbox controller inputs and emits signals for joystick movements,
    trigger presses, and button clicks.
    It also handles toggling variables for specific buttons.

    Attributes:
        leftJoystickPos: A signal emitted with two floats for the left joystick position.
        rightJoystickPos: A signal emitted with two floats for the right joystick position.
        l2_pressed: A signal emitted with a float for the left trigger pressure.
        r2_pressed: A signal emitted with a float for the right trigger pressure.
        buttonAClicked: A signal emitted when the A button is clicked.
        buttonYClicked: A signal emitted when the Y button is clicked.
        xChanged: A signal emitted with an integer when the X button toggles variable changes.
        bChanged: A signal emitted with an integer when the B button toggles variable changes.
        MAX_TRIG_VAL: The maximum value for trigger inputs.
        MAX_JOY_VAL: The maximum value for joystick inputs.
    """
    leftJoystickPos = Signal(float, float)
    rightJoystickPos = Signal(float, float)
    l2_pressed = Signal(float)
    r2_pressed = Signal(float)

    buttonAClicked = Signal()
    buttonYClicked = Signal()

    xChanged = Signal(int)  # Signal to indicate a change in the X button toggle variable
    bChanged = Signal(int)  # Signal to indicate a change in the B button toggle variable

    MAX_TRIG_VAL = math.pow(2, 8)
    MAX_JOY_VAL = math.pow(2, 15)

    def __init__(self) -> None:
        """ Initializes joystick, trigger, and button states, and starts a thread to monitor the controller inputs."""
        super().__init__()

        self._left_joystick_y = 0
        self._left_joystick_x = 0
        self._right_joystick_y = 0
        self._right_joystick_x = 0
        self._left_trigger = 0
        self._right_trigger = 0
        self._left_bumper = 0
        self._right_bumper = 0
        self._a = 0
        self._x = 0
        self._y = 0
        self._b = 0
        self._left_thumb = 0
        self._right_thumb = 0
        self._back = 0
        self._start = 0
        self._left_d_pad = 0
        self._right_d_pad = 0
        self._up_d_pad = 0
        self._down_d_pad = 0

        self._monitor_thread = threading.Thread(target=self._monitor_controller, args=())
        self._monitor_thread.daemon = True
        self._monitor_thread.start()

        self._prev_left_x = 0
        self._prev_left_y = 0

        self._toggle_variable_x = 0
        self._toggle_variable_b = 0

    def toggle_variable_x_handler(self):
        """Toggles handler for button X.

        This method toggles the X variable between zero and one and emits a signal if it changes.
        """
        new_value = 1 - self._toggle_variable_x  # Toggle the X variable between 0 and 1 and emit signal if it changes
        if new_value != self._toggle_variable_x:
            self._toggle_variable_x = new_value
            self.xChanged.emit(self._toggle_variable_x)

    def toggle_variable_b_handler(self):
        """Toggles handler for button B.

        This method toggles the B variable between zero and one and emits a signal if it changes.
        """
        new_value = 1 - self._toggle_variable_b  # Toggle the B variable between 0 and 1 and emit signal if it changes
        if new_value != self._toggle_variable_b:
            self._toggle_variable_b = new_value
            self.bChanged.emit(self._toggle_variable_b)

    def _monitor_controller(self) -> None:
        """Monitors controller inputs and emit signals accordingly.

        This method continuously monitors the Xbox controller inputs and emits signals
        based on joystick movements, trigger presses, and button clicks.
        Runs inside a thread.
        """
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

                if abs(self._right_joystick_x) > 0.1 or abs(self._right_joystick_y) > 0.1:
                    self.rightJoystickPos.emit(self._right_joystick_x, self._right_joystick_y)
                if abs(self._left_joystick_x) > 0.1 or abs(self._left_joystick_y) > 0.1:
                    self.leftJoystickPos.emit(self._left_joystick_x, self._left_joystick_y)

    def _handle_left_joystick_y(self, event) -> None:
        self._left_joystick_y = event.state / self.MAX_JOY_VAL  # normalize between -1 and 1

    def _handle_left_joystick_x(self, event) -> None:
        self._left_joystick_x = event.state / self.MAX_JOY_VAL  # normalize between -1 and 1

    def _handle_right_joystick_y(self, event) -> None:
        self._right_joystick_y = event.state / self.MAX_JOY_VAL  # normalize between -1 and 1

    def _handle_right_joystick_x(self, event) -> None:
        self._right_joystick_x = event.state / self.MAX_JOY_VAL  # normalize between -1 and 1

    def _handle_left_trigger(self, event) -> None:
        self._left_trigger = event.state / self.MAX_TRIG_VAL  # normalize between 0 and 1
        self.l2_pressed.emit(self._left_trigger)

    def _handle_right_trigger(self, event) -> None:
        self._right_trigger = event.state / self.MAX_TRIG_VAL  # normalize between 0 and 1
        self.r2_pressed.emit(self._right_trigger)

    def _handle_left_bumper(self, event) -> None:
        self._left_bumper = event.state

    def _handle_right_bumper(self, event) -> None:
        self._right_bumper = event.state

    def _handle_button_a(self, event) -> None:
        self._a = event.state
        self.buttonAClicked.emit()

    def _handle_button_y(self, event) -> None:
        self._y = event.state  # previously switched with X
        self.buttonYClicked.emit()

    def _handle_button_x(self, event) -> None:
        self._x = event.state  # previously switched with Y
        if self._x == 1:  # Only emit when the button is pressed down
            # self.buttonXClicked.emit()
            self.toggle_variable_x_handler()

    def _handle_button_b(self, event) -> None:
        self._b = event.state
        if self._b == 1:  # Only emit when the button is pressed down
            # self.buttonBClicked.emit()
            self.toggle_variable_b_handler()

    def _handle_left_thumb(self, event) -> None:
        self._left_thumb = event.state

    def _handle_right_thumb(self, event) -> None:
        self._right_thumb = event.state

    def _handle_back(self, event) -> None:
        self._back = event.state

    def _handle_start(self, event) -> None:
        self._start = event.state

    def _handle_left_d_pad(self, event) -> None:
        self._left_d_pad = event.state

    def _handle_right_d_pad(self, event) -> None:
        self._right_d_pad = event.state

    def _handle_up_d_pad(self, event) -> None:
        self._up_d_pad = event.state

    def _handle_down_d_pad(self, event) -> None:
        self._down_d_pad = event.state
