"""
Lowest level controller-to-Create2 serial interface functions
"""

from time import sleep
import serial
import threading
from colorama import Fore
from colorama import init as colorama_init

lock = threading.Lock()

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
    """Attempt to open serial port connection to the Create"""
    ser.port = PORT
    ser.baudrate = BAUD_RATE
    ser.timeout = TIMEOUT
    try:  # Try closing the connection in case it is already open
        ser.close()
    except serial.SerialException:
        pass
    try:
        ser.open()
    except serial.SerialException:
        print(Fore.RED + f'\nFailed to open port:{PORT}\nCheck Create cable at Wombat!!!\n')
        exit(1)
    print(Fore.GREEN + f'\nConnected to Create on:\n{ser.port} at {ser.baudrate} bps')

    # Check and clear any extraneous serial input bytes
    sleep(SERIAL_IO_WAIT)
    if ser.in_waiting:
        msg = receive_from_create(1000)
        print(Fore.YELLOW + f'Cleared {len(msg)} extraneous bytes from serial input')
        # ser.reset_input_buffer()


def close_serial():
    """Close serial port connection to the Create"""
    if ser.is_open:
        ser.close()
        print(Fore.GREEN + f'Closed port:{ser.port}')
    print()


def send_to_create(cmd):
    """
    Send command and any parameters to Create
    cmd: list of bytes to write to the Create serial port
    """
    # TODO figure out how to handle an exception when sending a command to Create
    try:
        with lock:
            ser.write(serial.to_bytes(cmd))
    except serial.SerialException:
        print(Fore.RED + '\nError sending command to Create\n')
    sleep(SERIAL_IO_WAIT)


def receive_from_create(num_bytes):
    """Return Create sensor values as an array of bytes"""
    with lock:
        return ser.read(num_bytes)


def query_create(cmd, num_bytes, timeout=None):
    """Send a command to the create and return its response"""
    cached_timeout = timeout
    if timeout is not None:
        ser.timeout = timeout

    send_to_create(cmd)
    response = receive_from_create(num_bytes)

    # Clean out erroneous create messages and re-query
    while response.startswith(b' ' * max(num_bytes, 4)):
        ser.timeout = 0.01  # Small timeout to clear out buffer
        bad_response = receive_from_create(100)
        print(Fore.YELLOW + f"--> I handled a bad response: '{bad_response}'")
        ser.timeout = cached_timeout if timeout is None else timeout
        send_to_create(cmd)
        response = receive_from_create(num_bytes)

    if timeout is not None:
        ser.timeout = cached_timeout

    return response
