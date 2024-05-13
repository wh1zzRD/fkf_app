from PySide6.QtCore import QObject, Signal, QTimer

class SignalEmitter(QObject):
    second_signal = Signal()  # Define a custom signal

    def __init__(self):
        super().__init__()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.emit_signal)

    def start_emission(self):
        self.timer.start(1000)  # Emit the signal every 1000 ms (1 second)

    def stop_emission(self):
        self.timer.stop()

    def emit_signal(self):
        self.second_signal.emit()