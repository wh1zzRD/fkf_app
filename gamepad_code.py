from inputs import get_gamepad
import math
import threading

from PySide6.QtCore import QObject, Signal, Slot


class XboxController(QObject):
    leftJoystickMove = Signal(float, float)
    rightJoystickMove = Signal(float, float)
    leftJoystickPos = Signal(float, float)
    rightJoystickPos = Signal(float, float)
    l2_pressed = Signal(float)
    r2_pressed = Signal(float)

    no_gamepad_connected = Signal()

    l2_status = Signal(float)
    r2_status = Signal(float)

    buttonAClicked = Signal()
    buttonBClicked = Signal()
    buttonXClicked = Signal()
    buttonYClicked = Signal()

    xChanged = Signal(int)  # Signal to indicate a change in the X button toggle variable
    bChanged = Signal(int)  # Signal to indicate a change in the B button toggle variable

    MAX_TRIG_VAL = math.pow(2, 8)
    MAX_JOY_VAL = math.pow(2, 15)

    def __init__(self):
        super().__init__()

        self.LeftJoystickY = 0
        self.LeftJoystickX = 0
        self.RightJoystickY = 0
        self.RightJoystickX = 0
        self.LeftTrigger = 0
        self.RightTrigger = 0
        self.LeftBumper = 0
        self.RightBumper = 0
        self.A = 0
        self.X = 0
        self.Y = 0
        self.B = 0
        self.LeftThumb = 0
        self.RightThumb = 0
        self.Back = 0
        self.Start = 0
        self.LeftDPad = 0
        self.RightDPad = 0
        self.UpDPad = 0
        self.DownDPad = 0

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

    @Slot()
    def toggle_variable_x_handler(self):
        # Toggle the X variable between 0 and 1 and emit signal if it changes
        new_value = 1 - self.toggle_variable_x
        if new_value != self.toggle_variable_x:
            self.toggle_variable_x = new_value
            self.xChanged.emit(self.toggle_variable_x)

    @Slot()
    def toggle_variable_b_handler(self):
        # Toggle the B variable between 0 and 1 and emit signal if it changes
        new_value = 1 - self.toggle_variable_b
        if new_value != self.toggle_variable_b:
            self.toggle_variable_b = new_value
            self.bChanged.emit(self.toggle_variable_b)

    def _monitor_controller(self):
        while True:
            events = get_gamepad()
            for event in events:
                if event.code == 'ABS_Y':
                    self.LeftJoystickY = event.state / XboxController.MAX_JOY_VAL  # normalize between -1 and 1
                elif event.code == 'ABS_X':
                    self.LeftJoystickX = event.state / XboxController.MAX_JOY_VAL  # normalize between -1 and 1
                elif event.code == 'ABS_RY':
                    self.RightJoystickY = event.state / XboxController.MAX_JOY_VAL  # normalize between -1 and 1
                elif event.code == 'ABS_RX':
                    self.RightJoystickX = event.state / XboxController.MAX_JOY_VAL  # normalize between -1 and 1
                elif event.code == 'ABS_Z':
                    self.LeftTrigger = event.state / XboxController.MAX_TRIG_VAL  # normalize between 0 and 1
                    self.l2_pressed.emit(self.LeftTrigger)
                elif event.code == 'ABS_RZ':
                    self.RightTrigger = event.state / XboxController.MAX_TRIG_VAL  # normalize between 0 and 1
                    self.r2_pressed.emit(self.RightTrigger)
                elif event.code == 'BTN_TL':
                    self.LeftBumper = event.state
                elif event.code == 'BTN_TR':
                    self.RightBumper = event.state
                elif event.code == 'BTN_SOUTH':
                    self.A = event.state
                    self.buttonAClicked.emit()
                elif event.code == 'BTN_NORTH':
                    self.Y = event.state  # previously switched with X
                    self.buttonYClicked.emit()
                elif event.code == 'BTN_WEST':
                    self.X = event.state  # previously switched with Y
                    if self.X == 1:  # Only emit when the button is pressed down
                        self.buttonXClicked.emit()
                elif event.code == 'BTN_EAST':
                    self.B = event.state
                    if self.B == 1:  # Only emit when the button is pressed down
                        self.buttonBClicked.emit()
                elif event.code == 'BTN_THUMBL':
                    self.LeftThumb = event.state
                elif event.code == 'BTN_THUMBR':
                    self.RightThumb = event.state
                elif event.code == 'BTN_SELECT':
                    self.Back = event.state
                elif event.code == 'BTN_START':
                    self.Start = event.state
                elif event.code == 'BTN_TRIGGER_HAPPY1':
                    self.LeftDPad = event.state
                elif event.code == 'BTN_TRIGGER_HAPPY2':
                    self.RightDPad = event.state
                elif event.code == 'BTN_TRIGGER_HAPPY3':
                    self.UpDPad = event.state
                elif event.code == 'BTN_TRIGGER_HAPPY4':
                    self.DownDPad = event.state

                if abs(self.RightJoystickX) > 0.1 or abs(self.RightJoystickY) > 0.1:
                    self.rightJoystickPos.emit(self.RightJoystickX, self.RightJoystickY)
                if abs(self.LeftJoystickX) > 0.1 or abs(self.LeftJoystickY) > 0.1:
                    self.leftJoystickPos.emit(self.LeftJoystickX, self.LeftJoystickY)
