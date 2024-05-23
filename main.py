import sys
from PySide6.QtWidgets import QApplication
from controller.Controls import Controls

if __name__ == "__main__":
    app = QApplication(sys.argv)

    controls = Controls()
    controls.window.show()

    sys.exit(app.exec())
