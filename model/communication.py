import time

import serial
import serial.tools.list_ports

from model.tank import Tank


def float_to_byte(value):
    # Ensure the value is within the expected range
    if value < -1 or value > 1:
        raise ValueError("Input value should be in the range [-1, 1]")
    # Normalize the value to [0, 1]
    normalized_value = (value + 1) / 2

    # Scale to the range [0, 255]
    byte_value = int(normalized_value * 255)
    return byte_value


class SerialMessenger:
    def __init__(self, port, baud_rate=9600):
        self.port = port
        self.baud_rate = baud_rate
        self.ser = serial.Serial(port, baud_rate)

        self.tank = Tank()

    @staticmethod
    def all_ports():
        all_ports = []
        ports = serial.tools.list_ports.comports()
        for port in ports:
            all_ports.append(port.device)

        return all_ports

    def close_serial(self):
        if self.ser.is_open:
            self.ser.close()

    def print_data(self):
        while True:
            tank_values = self.tank.get_values()
            print(tank_values)
            byte_msg = [
                float_to_byte(tank_values[0]),
                float_to_byte(tank_values[1]),
                float_to_byte(tank_values[2]),
                float_to_byte(tank_values[3]),
                tank_values[4],
                tank_values[5],
                tank_values[6],
                tank_values[7]
            ]
            print(byte_msg)
            byte_data = bytes(byte_msg)
            # Send the byte data over serial
            self.ser.write(byte_data)
            time.sleep(1)
