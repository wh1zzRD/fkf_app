import random
import time

import serial

# Define the serial port and baud rate
port = "COM3"  # Change this to your serial port
baud_rate = 9600

# Create a Serial object
ser = serial.Serial(port, baud_rate)

try:
    while True:
        # Write the bytearray to the serial port
        byte_array = bytearray([random.randint(0, 255) for _ in range(2)])
        ser.write(byte_array)

        # Optional: introduce a delay between each send operation
        time.sleep(1)  # Adjust the delay time as needed
except KeyboardInterrupt:
    # Handle KeyboardInterrupt (Ctrl+C) to gracefully exit the loop
    pass
finally:
    # Close the serial port when done
    ser.close()
