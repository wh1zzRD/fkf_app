""" A module for converting program data to the required format and communicating it via serial.

Represent the part of the model in the MVC. Receives the data from
the controller, converts it to the required byte format and sends
it to a connected microcontroller via pyserial.

Typical usage:

    communication = SerialMessenger(port, baud_rate=9600)
"""

import time
from typing import List

import serial
import serial.tools.list_ports

from model.tank import Tank


def float_to_byte(value: float) -> int:
    """Convert a floating-point value to a byte representation.

        This function takes a floating-point value within the range [-1, 1],
        normalizes it to the range [0, 1], and then scales it to the range [0, 255].

        Args:
            value (float): The value to convert to a byte representation.

        Returns:
            int: An integer representing the byte value.

        Raises:
            ValueError: If the input value is not within the range [-1, 1].
        """
    if value < -1 or value > 1:
        raise ValueError("Input value should be in the range [-1, 1]")
    normalized_value = (value + 1) / 2  # Normalize the value to [0, 1]

    byte_value = int(normalized_value * 255)  # Scale to the range [0, 255]
    return byte_value


def float_to_int_255(value):
    if value < 0 or value > 1:
        raise ValueError("Input value must be in the range [0, 1]")
    return int(round(value * 255))


class SerialMessenger:
    """Communication point between program and physical tank.

    Used by the controller to send its data (user input)
    to an antenna that later communicates it to a
    physical instance of the tank.

    Attributes:
        port: A string representing the serial port to which the device is connected.
        baud_rate: An integer representing the speed of data transmission in bits per second.
        ser: A serial.Serial instance representing the serial connection.
        tank: instance of tank class representing the values needed to be sent
    """
    def __init__(self, port: str, baud_rate: int = 9600) -> None:
        """Initializes the SerialMessenger with a given port and baud rate.

        Args:
            port (str): The serial port to which the antenna is connected.
            baud_rate (int): The speed of data transmission in bits per second (default is 9600).
        """
        self.port = port
        self.baud_rate = baud_rate
        self.ser = serial.Serial(port, baud_rate)

        self.tank = Tank()

    @staticmethod
    def all_ports() -> List[str]:
        """Retrieves a list of all available serial ports.

        Returns:
            List: A list of strings representing the names of all available serial ports.
        """
        all_ports = []
        ports = serial.tools.list_ports.comports()
        for port in ports:
            all_ports.append(port.device)

        return all_ports

    def close_serial(self) -> None:
        """Closes the serial connection."""
        if self.ser.is_open:
            self.ser.close()

    def print_data(self) -> None:
        """Print tank data and send it over serial.

        This method retrieves tank data, converts it to the required byte format,
        and sends it over the serial connection.
        It runs in a loop with a delay of 1 second.
        """
        while True:
            tank_values = self.tank.get_values()
            print(tank_values.values())
            byte_msg = []

            left_sign = 0 if tank_values["left_motor"] < 0 else 1
            right_sign = 0 if tank_values["right_motor"] < 0 else 1

            byte_msg.append(left_sign)
            byte_msg.append(float_to_int_255(abs(tank_values["left_motor"])))

            byte_msg.append(right_sign)
            byte_msg.append(float_to_int_255(abs(tank_values["right_motor"])))

            byte_msg.append(tank_values["light"])
            byte_msg.append(tank_values["water"])
            print(byte_msg)
            byte_data = bytes(byte_msg)
            # Send the byte data over serial
            self.ser.write(byte_data)
            time.sleep(0.1)
