import serial.tools.list_ports


def list_serial_ports():
    ports = serial.tools.list_ports.comports()
    print("Available Serial Ports:")
    for port in ports:
        print(port.device)


if __name__ == "__main__":
    list_serial_ports()
