import threading
import time

import serial
import serial.tools.list_ports

from Tank import Tank


class SerialMessenger:
    def __init__(self, port, baud_rate=9600, communication_possible=False):
        if communication_possible:
            self.port = port
            self.baud_rate = baud_rate
            self.ser = serial.Serial(port, baud_rate)

        self.communication_possible = communication_possible

        self.tank = Tank()

    # def __init__(self):
    #     self.tank = Tank()

    @staticmethod
    def all_ports():
        all_ports = []
        ports = serial.tools.list_ports.comports()
        for port in ports:
            print(port.device)
            all_ports.append(port.device)

        return all_ports

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
            if self.communication_possible:
                print(self.tank.get_values())
                time.sleep(1)
