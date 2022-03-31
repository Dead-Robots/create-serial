"""
Lowest level controller-to-Create2 serial interface functions
"""

import serial
from time import sleep
from colorama import Fore
from colorama import init as colorama_init

colorama_init(autoreset=True)

# Serial interface initialization parameters
BAUD_RATE = 115200
TIMEOUT = 1.0
PORT = '/dev/ttyUSB0'

# Instantiate class to use globally while program is running
ser = serial.Serial()

# Delay needed for Create to allow current command to complete (15 ms per Create2 documentation)
SERIAL_IO_WAIT = 0.015


def open_serial():
    # Attempt to open serial port connection to the Create
    ser.port = PORT
    ser.baudrate = BAUD_RATE
    ser.timeout = TIMEOUT
    try:
        ser.open()
    except serial.SerialException:
        print(Fore.RED + f'\nFailed to open port:{PORT}\nCheck Create cable at Wombat!!!\n')
        exit(1)
    print(Fore.GREEN + f'\nConnected to Create on:\n{ser.port} at {ser.baudrate} bps')

    # Check and clear any extraneous serial input bytes
    sleep(SERIAL_IO_WAIT)
    if ser.in_waiting:
        print(Fore.YELLOW + f'Cleared {ser.in_waiting} extraneous bytes from serial input')
        ser.reset_input_buffer()


def close_serial():
    # Close serial port connection to the Create
    if ser.is_open:
        ser.close()
        print(Fore.GREEN + f'Closed port:{ser.port}')
    print()


def send_to_create(cmd):
    # Send command and any parameters to Create
    # cmd: list of bytes to write to the Create serial port
    # TODO figure out how to handle an exception when sending a command to Create
    try:
        ser.write(serial.to_bytes(cmd))
    except serial.SerialException:
        print(Fore.RED + '\nError sending command to Create\n')
    sleep(SERIAL_IO_WAIT)


def receive_from_create(num_bytes):
    # Return Create sensor values as an array of bytes
    return ser.read(num_bytes)
