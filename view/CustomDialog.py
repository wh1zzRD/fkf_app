from PySide6.QtWidgets import QDialog, QDialogButtonBox, QVBoxLayout, QLabel, QComboBox


class CustomDialog(QDialog):
    def __init__(self, options, parent=None):
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

        self.comboBox = QComboBox(self)
        self.comboBox.addItems(options)
        self.layout.addWidget(self.comboBox)

        buttons = QDialogButtonBox.Ok | QDialogButtonBox.Cancel

        self.buttonBox = QDialogButtonBox(buttons)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.layout.addWidget(self.buttonBox)

    def get_selected_option(self):
        return self.comboBox.currentText()
