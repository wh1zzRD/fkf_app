from PySide6.QtWidgets import QDialog, QDialogButtonBox, QVBoxLayout, QLabel, QComboBox, QPushButton


class CustomDialog(QDialog):
    def __init__(self, options, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Select an Option")

        self.layout = QVBoxLayout(self)

        self.label = QLabel("Choose an option:", self)
        self.layout.addWidget(self.label)

        self.comboBox = QComboBox(self)
        self.comboBox.addItems(options)
        self.layout.addWidget(self.comboBox)

        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.layout.addWidget(self.buttonBox)

    def get_selected_option(self):
        return self.comboBox.currentText()



