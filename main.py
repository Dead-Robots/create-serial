#!/usr/bin/python3 -u
from time import sleep
from myserial import open_serial, close_serial
from createCommands import open_create, close_create, read_create_encoders, create_drive, create_dd, create_pwm


def main():
    # Open a serial port connection to the Create
    open_serial()

    # Initialize the Create
    open_create()

    # Get Create sensor values: wheel encoders
    read_create_encoders()

    # Drive
    create_drive(100, 0x8000)
    # create_dd(100, 100)
    # create_pwm(127, 127)
    sleep(1)
    create_drive(-100, 0x8000)
    # create_dd(-100, -100)
    # create_pwm(-127, -127)
    sleep(1)
    create_drive(0, 0x8000)
    # create_dd(0, 0)
    # create_pwm(0, 0)
    sleep(0.5)

    # Get Create sensor values: wheel encoders
    read_create_encoders()

    # Terminate communications with the Create
    close_create()

    # Close serial port connection to the Create
    close_serial()


if __name__ == "__main__":
    main()
