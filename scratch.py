import time
import threading


def print_data():
    while True:
        print("abc")
        time.sleep(1)


if __name__ == '__main__':
    x = threading.Thread(target=print_data, daemon=True)
    x.start()
