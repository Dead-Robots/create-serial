#!/usr/bin/python3 -u
import math
import time
from time import sleep
from myserial import open_serial, close_serial
from createCommands import open_create, close_create, read_create_encoders, create_drive, create_dd, create_pwm, \
    Encoders
import sys

# from kipr import push_button, gyro_z


def grayson():
    print('Python ', sys.version)

    # Open a serial port connection to the Create
    open_serial()

    # Initialize the Create
    open_create()

    # close_create()
    #
    # # Close serial port connection to the Create
    # close_serial()
    #
    # exit()

    # baseline = 0
    # for _ in range(0, 100):
    #     time.sleep(0.01)
    #     baseline += gyro_z()
    # baseline /= 100
    #
    # gyro = lambda: gyro_z() - baseline
    #
    # angle = 0
    # t = time.time()
    # create_pwm(-100, 100)
    # while angle < 4*(45) and not push_button():
    #     # time.sleep(0.1)
    #     dt = time.time() - t
    #     angle -= gyro() * dt
    #     t = time.time()
    # create_pwm(1, -1)
    # time.sleep(0.2)

    # e = Encoders()
    # while not push_button():
    #     time.sleep(1)
    #     print(e.values, read_create_encoders())

    # Get Create sensor values: wheel encoders
    # straight(43, 100)
    for x in range(4):
        spin(90, 100)
        while not push_button():
            pass
        while push_button():
            pass
    # straight(36, 100)

    # Terminate communications with the Create
    close_create()

    # Close serial port connection to the Create
    close_serial()


def stop():
    create_pwm(-1, -1)
    time.sleep(0.2)
    create_pwm(1, 1)
    time.sleep(0.2)


def spin(angle, speed):
    l_encoder_start, r_encoder_start = read_create_encoders()
    print('Left  Encoder Count: ', l_encoder_start)
    print('Right Encoder Count: ', r_encoder_start)
    inches = lambda n: n * (math.pi * 72 / 508.8) / 24.5
    le = re = 0
    ls = rs = speed
    p = 40
    i = 1

    dist = angle/360 * math.pi * 9.25
    print("dist", dist)
    while le < dist and not push_button():
        tle, tre = read_create_encoders()
        a, b = abs(inches(tle - l_encoder_start)), abs(inches(tre - r_encoder_start))
        ld, rd = a - le, b - re
        le, re = a, b

        error = p * (ld - rd) + i * (le - re)

        print(round(error, 2))

        ls -= int(error)
        rs += int(error)

        create_pwm(-ls if angle > 0 else ls, rs if angle > 0 else -rs)
        # time.sleep(0.02)

    create_pwm(1 if angle > 0 else -1, -1 if angle > 0 else 1)
    time.sleep(0.2)


def straight(dist, speed):
    l_encoder_start, r_encoder_start = read_create_encoders()
    print('Left  Encoder Count: ', l_encoder_start)
    print('Right Encoder Count: ', r_encoder_start)
    inches = lambda n: n * (math.pi * 72 / 508.8) / 24.5
    le = re = 0
    ls = rs = speed
    p = 200
    i = 1
    while le < dist and not push_button():
        tle, tre = read_create_encoders()
        a, b = inches(tle - l_encoder_start), inches(tre - r_encoder_start)
        ld, rd = a - le, b - re
        le, re = a, b

        error = p * (ld - rd) + i * (le - re)

        print(error)

        ls -= int(error)
        rs += int(error)

        create_pwm(ls, rs)
        # time.sleep(0.02)


def main():
    print('Python ', sys.version)

    # Open a serial port connection to the Create
    open_serial()
    # Initialize the Create
    open_create()

    # Get Create sensor values: wheel encoders
    l_encoder_start, r_encoder_start = read_create_encoders()
    print('Left  Encoder Count: ', l_encoder_start)
    print('Right Encoder Count: ', r_encoder_start)

    # Drive commands
    # create_drive(200, 0x8000)
    create_dd(100, 100)
    # create_pwm(150, 150)
    sleep(1)
    # create_drive(-200, 0x8000)
    create_dd(-100, -100)
    # create_pwm(-150, -150)
    sleep(1)
    # create_drive(0, 0x8000)
    create_dd(0, 0)
    # create_pwm(0, 0)
    sleep(0.5)

    # Get Create sensor values: wheel encoders
    l_encoder_end, r_encoder_end = read_create_encoders()
    # print('Left  Encoder Count:', l_encoder_end)
    # print('Right Encoder Count:', r_encoder_end)
    #
    # print('Left Encoder Delta Count:', l_encoder_end - l_encoder_start)
    # print('Right Encoder Delta Count:', r_encoder_end - r_encoder_start)
    #
    # print('Left Encoder Dist:', (l_encoder_end - l_encoder_start) * (math.pi * 72 / 508.8))
    # print('Right Encoder DIst:', (r_encoder_end - r_encoder_start) * (math.pi * 72 / 508.8))

    # Terminate communications with the Create
    close_create()

    # Close serial port connection to the Create
    close_serial()


if __name__ == "__main__":
    main()
