"""Contains a custom dialog with a dropdown out of a given list, where a user has to choose one option.

Typical usage:
    dlg = CustomDialog(["option 1", "option 2"], self)  # self is an instance of QMainWindow
"""

from typing import List, Optional

from PySide6.QtWidgets import QDialog, QDialogButtonBox, QVBoxLayout, QLabel, QComboBox, QMainWindow


class CustomDialog(QDialog):
    """A dialog for selecting an option from a list of options.

    This dialog prompts the user to select an option from a given list.
    It is typically used for selecting a serial port for communication with an ESP32 device.

    Attributes:
        message_label: A Qlabel displaying the instruction message.
        label: A Qlabel prompting the user to choose an option.
        combo_box: A combo box populated with the provided options.
        button_box: A button box containing OK and Cancel buttons.
    """
    def __init__(self, options: List[str], parent: Optional[QMainWindow] = None) -> None:
        """Initializes the CustomDialog with a list of options and an optional parent.

        Args:
            options (List[str]): A list of strings options to populate the combo box.
            parent (Optional[QMainWindow]): The parent window of the dialog.
        """
        super().__init__(parent)
        self.setWindowTitle("Select an Option")

        self.layout = QVBoxLayout(self)

        self.message_label = QLabel(
            "Connect ESP32 to your PC \n"
            "and select the appropriate \n"
            "port for serial communication.\n",
            self
        )
        self.layout.addWidget(self.message_label)

        self.label = QLabel("Choose an option:", self)
        self.layout.addWidget(self.label)

        self.combo_box = QComboBox(self)
        self.combo_box.addItems(options)
        self.layout.addWidget(self.combo_box)

        buttons = QDialogButtonBox.Ok | QDialogButtonBox.Cancel

        self.button_box = QDialogButtonBox(buttons)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        self.layout.addWidget(self.button_box)

    def get_selected_option(self) -> str:
        """Get the selected option from the combo box.

        Returns:
            str: The selected option.
        """
        return self.combo_box.currentText()
