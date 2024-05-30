"""Main Window Module.

Contains the main application window class and related widgets.
"""

from functools import partial

from PySide6 import QtCore
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QMainWindow, QPushButton, QWidget, QHBoxLayout, QVBoxLayout, QMessageBox

from model.communication import SerialMessenger
from view.custom_dialog import CustomDialog
from view.joystick import QJoystick
from view.rotation_widget import RotationWidget


class Window(QMainWindow):
    """Main Application Window.

    Represents the main application window for the FKF App.
    The View in the MVC. Manages all widgets and all GUI operations.

    Attributes:
        monitor: A QWidget representing the monitoring widget.
        joystick: A QJoystick instance representing the joystick widget.
        rotation_widget: A RotationWidget instance representing the rotation control widget.
        button_water: A QPushButton for water control.
        button_light: A QPushButton for light control.
        selected_port: The selected port from the dialog for serial communication.
        controls_functions: A dictionary mapping control signals to corresponding functions.
    """

    def __init__(self) -> None:
        """Initializes the window instance and all graphic layouts."""
        super().__init__()
        self.setWindowTitle("FKF App")
        self.setFixedSize(600, 400)

        self.monitor = QWidget()
        self.joystick = QJoystick()
        self.rotation_widget = RotationWidget()

        self.button_water = QPushButton()
        self.button_light = QPushButton()

        self._setup_layout()

        self.selected_port = None

        self.controls_functions = {
            "right_joystick": self.rotation_widget.set_joystick_position,
            "left_joystick": self.joystick.set_joystick_position,
            "button_water": self.button_water.animateClick,
            "button_light": self.button_light.animateClick
        }

    def handle_port_selection_dialog(self) -> str:
        """Handle the port selection dialog.

        Returns:
            str: The selected port for serial communication.
        """
        dlg = CustomDialog([""] + SerialMessenger.all_ports(), self)
        dlg.accepted.connect(partial(self.accepted_slot, dlg))
        dlg.rejected.connect(self.rejected_slot)
        dlg.exec()
        return self.selected_port

    def critical_dialog(self, label: str, text: str) -> None:
        """Display a critical dialog with the given label and text.

        Args:
            label (str): The label of the dialog.
            text (str): The text to display in the dialog.
        """
        QMessageBox.critical(
            self,
            label,
            text,
            buttons=QMessageBox.Ok,
            defaultButton=QMessageBox.Ok,
        )

    @QtCore.Slot(CustomDialog)
    def accepted_slot(self, dlg):  # pylint: disable=missing-function-docstring
        selected_option = dlg.get_selected_option()
        if selected_option:
            self.selected_port = selected_option
        else:
            self.critical_dialog("No Port Selected", "You did not select a port")

    @QtCore.Slot()
    def rejected_slot(self):  # pylint: disable=missing-function-docstring
        self.critical_dialog("No Port Selected", "You did not select a port")

    def _setup_layout(self) -> None:
        """Set up the layout of the main window."""
        full_layout = QVBoxLayout()

        central_widget = QWidget()
        central_widget.setLayout(full_layout)
        self.setCentralWidget(central_widget)

        full_layout.addLayout(self._setup_monitor_layout())
        full_layout.addLayout(self._setup_controls_layout())

    def _setup_monitor_layout(self) -> QVBoxLayout:
        """Set up the layout for the monitor widget.

        Returns:
            QVBoxLayout: the ready layout
        """
        monitor_layout = QVBoxLayout()
        monitor_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.monitor.setFixedSize(300, 200)  # Set size of rectangular widget
        self.monitor.setStyleSheet("background-color: gray; border: 1px solid black;")

        monitor_layout.addWidget(self.monitor)

        return monitor_layout

    def _setup_controls_layout(self) -> QHBoxLayout:
        """Set up the layout for the control widgets, e.g., buttons and joysticks.

        Returns:
            QHBoxLayout: the ready layout
        """
        controls_layout = QHBoxLayout()

        controls_layout.addWidget(self.joystick)
        controls_layout.addWidget(self.rotation_widget)

        controls_layout.addLayout(self._setup_buttons())

        return controls_layout

    def _setup_buttons(self) -> QHBoxLayout:
        """Set up the layout for the control buttons.

        Returns:
            QHBoxLayout: the ready layout
        """
        button_grid = QHBoxLayout()
        button_data = [("Water", 60, 60), ("Light", 60, 60)]

        # Create buttons and add them to the layout
        for button_name, width, height in button_data:
            button = QPushButton(button_name)
            button.setFixedSize(width, height)
            button_grid.addWidget(button)

            # Add button as a member of the class
            setattr(self, f"button_{button_name.lower()}", button)

        return button_grid

    def update_gui(self, element: str, x: float = 0, y: float = 0) -> None:
        """Update the GUI based on the provided element and coordinates.

        Args:
            element (str): The element to update.
            x (float): The x-coordinate.
            y (float): The y-coordinate.
        """
        if element in ("left_joystick", "right_joystick"):
            self.controls_functions[element](x, y)
        else:
            self.controls_functions[element]()
