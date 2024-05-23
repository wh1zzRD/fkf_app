from typing import List, Optional

from PySide6.QtWidgets import QDialog, QDialogButtonBox, QVBoxLayout, QLabel, QComboBox, QMainWindow


class CustomDialog(QDialog):
    def __init__(self, options: List[str], parent: Optional[QMainWindow] = None) -> None:
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
        return self.combo_box.currentText()
