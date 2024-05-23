from functools import partial
from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QMainWindow, QPushButton, QWidget, QHBoxLayout, QVBoxLayout, QMessageBox

from Communication import SerialMessenger
from CustomDialog import CustomDialog
from QJoystick import QJoystick
from RotationWidget import RotationWidget


class Window(QMainWindow):
    update_previous_port = Signal(dict)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("FKF App")
        self.setFixedSize(600, 400)

        self._setup_layout()

        self.selected_port = None

        self.controls_functions = {
            "right_joystick": (lambda x, y: self.rotation_widget.set_joystick_position(x, y)),
            "left_joystick": (lambda x, y: self.joystick.set_joystick_position(x, y)),
            "button_water": (lambda _, __: self.button_water.animateClick()),
            "button_light": (lambda _, __: self.button_light.animateClick()),
            "button_sound": (lambda _, __: self.button_sound.animateClick()),
            "button_sth": (lambda _, __: self.button_sth.animateClick()),
        }

    def handle_port_selection_dialog(self):
        dlg = CustomDialog([""] + SerialMessenger.all_ports(), self)
        dlg.accepted.connect(partial(self.accepted_slot, dlg))
        dlg.rejected.connect(self.rejected_slot)
        dlg.exec()
        return self.selected_port

    def select_port(self):
        self.handle_port_selection_dialog()
        return self.selected_port

    def critical_dialog(self, label, text):
        QMessageBox.critical(
            self,
            label,
            text,
            buttons=QMessageBox.Ok,
            defaultButton=QMessageBox.Ok,
        )

    def accepted_slot(self, dlg):
        selected_option = dlg.get_selected_option()
        if selected_option:
            self.selected_port = selected_option
        else:
            self.critical_dialog("No Port Selected", "You did not select a port")

    def rejected_slot(self):
        self.critical_dialog("No Port Selected", "You did not select a port")

    def _setup_layout(self):
        full_layout = QVBoxLayout()

        central_widget = QWidget()
        central_widget.setLayout(full_layout)
        self.setCentralWidget(central_widget)

        full_layout.addLayout(self._setup_monitor_layout())
        full_layout.addLayout(self._setup_controls_layout())

    def _setup_monitor_layout(self):
        monitor_layout = QVBoxLayout()
        monitor_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.monitor = QWidget()
        self.monitor.setFixedSize(300, 200)  # Set size of rectangular widget
        self.monitor.setStyleSheet("background-color: gray; border: 1px solid black;")

        monitor_layout.addWidget(self.monitor)

        return monitor_layout

    def _setup_controls_layout(self):
        controls_layout = QHBoxLayout()

        self.joystick = QJoystick()
        self.rotation_widget = RotationWidget()

        controls_layout.addWidget(self.joystick)
        controls_layout.addWidget(self.rotation_widget)

        controls_layout.addLayout(self._setup_buttons())

        return controls_layout

    def _setup_buttons(self):
        button_grid = QHBoxLayout()
        button_data = [("Water", 60, 60), ("Light", 60, 60), ("Sound", 60, 60), ("Sth", 60, 60)]

        # Create buttons and add them to the layout
        for button_name, width, height in button_data:
            button = QPushButton(button_name)
            button.setFixedSize(width, height)
            button_grid.addWidget(button)

            # Add button as a member of the class
            setattr(self, f"button_{button_name.lower()}", button)

        return button_grid

    def update_gui(self, element, x, y):
        self.controls_functions[element](x, y)
