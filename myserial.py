import serial
from time import sleep


# Serial interface initialization parameters
BAUD_RATE = 115200
TIMEOUT = 1.0
PORT = '/dev/ttyUSB0'

# Instantiate class to use globally while program is running
ser = serial.Serial()

# Delay needed for Create to allow current command to complete (15 ms per Create2 documentation)
SERIAL_IO_WAIT = 0.015


def open_serial():
    # Open serial port connection to the Create
    ser.port = PORT
    ser.baudrate = BAUD_RATE
    ser.timeout = TIMEOUT
    try:
        ser.open()
    except serial.SerialException:
        print('\n!!! Unable to open port: Check Create cable at Wombat !!!\n')
        exit(1)
    if ser.isOpen():
        print('\nOpened port to Create: {} at {} bps\n'.format(ser.port, ser.baudrate))
    else:
        raise Exception('\n!!! Failed to open {} at {} !!!\n'.format(PORT, BAUD_RATE))
    # Check and clear any extraneous serial input bytes
    sleep(SERIAL_IO_WAIT)
    if ser.inWaiting():
        print("Cleared {} extraneous bytes from serial input".format(ser.inWaiting()))
        ser.reset_input_buffer()


def close_serial():
    # Close serial port connection to the Create
    if ser.isOpen():
        ser.close()
        print('\nClosed port: {}'.format(ser.port))
    print()


def send_to_create(cmd):
    # Send command and any parameters to Create
    # cmd: list of bytes to write to the Create serial port
    ser.write(serial.to_bytes(cmd))
    sleep(SERIAL_IO_WAIT)


def receive_from_create(num_bytes):
    # Return Create sensor values as an array of bytes
    return ser.read(num_bytes)
