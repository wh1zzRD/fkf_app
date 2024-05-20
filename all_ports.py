import serial.tools.list_ports


def list_serial_ports():
    ports = serial.tools.list_ports.comports()
    if not ports:
        print("No serial ports found.")
        return
    print("Available Serial Ports:")
    for port in ports:
        print(f"Device: {port.device}, Description: {port.description}, HWID: {port.hwid}")


if __name__ == "__main__":
    list_serial_ports()
