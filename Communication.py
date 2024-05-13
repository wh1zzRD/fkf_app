import threading
import time

import serial
import serial.tools.list_ports

from Tank import Tank


class SerialMessenger:
    def __init__(self, port, baud_rate=9600):
        self.port = port
        self.baud_rate = baud_rate
        self.ser = serial.Serial(port, baud_rate)

        self.tank = Tank()

    @staticmethod
    def all_ports():
        ports = serial.tools.list_ports.comports()
        print("Available Serial Ports:")
        for port in ports:
            print(port.device)

    def send_message(self, message):
        try:
            self.ser.write(message.encode())
            print("Message sent:", message)
        except serial.SerialException as e:
            print("Serial communication error:", e)

    def close_serial(self):
        if self.ser.is_open:
            self.ser.close()
            print("Serial port closed")

    def print_data(self):
        while True:
            print(self.tank.get_values())
            time.sleep(1)
