"""
Macro-level Create2 functions
"""

from myserial import send_to_create, receive_from_create, close_serial
from colorama import Fore
from colorama import init as colorama_init

colorama_init(autoreset=True)

# Create Opcodes
START = 128
SAFE = 131
FULL = 132
POWER = 133
DRIVE = 137
LEDS = 139
QUERY = 142
DRIVE_DIRECT = 145
DRIVE_PWM = 146
QUERY_LIST = 149
LEDS_ASCII = 164
STOP = 173

# Create Sensor Packet numbers
VOLTAGE = 22
LEFT_ENCODER = 43
RIGHT_ENCODER = 44

# Create Power LED values
POWER_LED_GREEN = 0
POWER_LED_YELLOW = 64
POWER_LED_INTENSITY_OFF = 0
POWER_LED_INTENSITY_FULL = 255

# Create's Other LEDs
CHECK_ROBOT__DOCK__SPOT__DEBRIS__ALL_OFF = 0

POWER_ON_CREATE_MSG = '\nCheck Create power and cable!!!\n'


def open_create():
    # Start dialog with Create - must do this first before sending any other command
    send_to_create([START])

    # Turn off the Create's safety features
    send_to_create([FULL])

    # Read Create's battery voltage to verify the Create is powered on and communicating
    # "size" is the number of bytes expected in the reply sent by the Create
    size = 2
    send_to_create([QUERY, VOLTAGE])
    data = receive_from_create(size)
    if len(data) == size:
        voltage = float((data[0] << 8) + data[1]) / 1000.0
        battery_voltage_msg(voltage)
        # if voltage > 14.4:
        #     print(Fore.GREEN + f'Create battery is {voltage} Volts\n')
        # elif voltage > 14.0:
        #     print(Fore.YELLOW + f'Create battery is {voltage} Volts - charge now?\n')
        # else:
        #     print(Fore.RED + f'Create battery is {voltage} Volts - charge now!\n')
    elif len(data) > 0:
        print(Fore.YELLOW + f'\nExpected {size} bytes, got {len(data)}')
    else:
        print(Fore.RED + POWER_ON_CREATE_MSG)
        send_to_create([STOP])
        close_serial()
        exit()

    # Set Create's Power LED to yellow
    send_to_create([LEDS,
                    CHECK_ROBOT__DOCK__SPOT__DEBRIS__ALL_OFF,
                    POWER_LED_YELLOW,
                    POWER_LED_INTENSITY_FULL])

    # Set Create's 7-segment LED array to 'CONN' denoting it is connected
    display_on_create('CONN')


def battery_voltage_msg(voltage):
    if voltage > 14.4:
        print(Fore.GREEN + f'Create battery is {voltage} Volts\n')
    elif voltage > 14.0:
        print(Fore.YELLOW + f'Create battery is {voltage} Volts - charge now?\n')
    else:
        print(Fore.RED + f'Create battery is {voltage} Volts - charge now!\n')


def close_create():
    # Set Create's LEDs and LED array to a default state
    send_to_create([LEDS,
                    CHECK_ROBOT__DOCK__SPOT__DEBRIS__ALL_OFF,
                    POWER_LED_GREEN,
                    POWER_LED_INTENSITY_FULL])

    # Clear Create's 7-segment LED array
    display_on_create('    ')

    # Prepare to disconnect from the Create - not needed?
    # send_to_create([SAFE])

    # Tell Create to power down
    # send_to_create([POWER])

    # Shut down communications between the Wombat and the Create
    send_to_create([STOP])


def display_on_create(msg):
    # Set Create's 7-segment LED array to display msg
    msg = msg[0:4]
    cmd = bytearray(' ' + msg, 'utf-8')
    # Insert Create OpCode into fist byte
    cmd[0] = LEDS_ASCII
    send_to_create(cmd)


def read_create_encoders():
    # Read Create's left and right wheel encoder values
    size = 4
    send_to_create([QUERY_LIST, 2, LEFT_ENCODER, RIGHT_ENCODER])
    data = receive_from_create(size)
    l_encoder = 0
    r_encoder = 0
    if len(data) == size:
        l_encoder = (data[0] << 8) + data[1]
        r_encoder = (data[2] << 8) + data[3]
        # print('Left  Encoder Count: ', l_encoder)
        # print('Right Encoder Count: ', r_encoder)
    elif len(data) > 0:
        print(Fore.YELLOW + f'\nExpected {size} bytes, got {len(data)}')
    else:
        print(Fore.RED + POWER_ON_CREATE_MSG)
    return l_encoder, r_encoder


class Encoders:
    def __init__(self):
        self.__prev_left, self.__prev_right = self.__get_raw()
        self.__left = self.__right = 0

    @property
    def values(self):
        left, right = self.__get_raw()
        adjusted_left, adjusted_right = self.__adjust(left, self.__prev_left), self.__adjust(right, self.__prev_right)
        self.__prev_left, self.__prev_right = left, right
        self.__left += adjusted_left
        self.__right += adjusted_right
        return self.__left, self.__right

    @staticmethod
    def __adjust(value, prev):
        if abs(value - prev) > 32768:
            value = value + 65536 if value < 32768 else value - 65536
        return value - prev

    @staticmethod
    def __get_raw():
        return read_create_encoders()


# fake = [(65520, 65520), (65530, 65530), (100, 100), (150, 150), (10, 10), (65525, 65525), (65520, 65520), (65510, 65510)]

# def fake_read():
#     return fake.pop(0)

# e = Encoders()
# print(e.values)
# print(e.values)
# print(e.values)
# print(e.values)
# print(e.values)
# print(e.values)
# print(e.values)


def high_byte(val):
    # Extracts high byte
    return (val >> 8) & 0xff


def low_byte(val):
    # Extracts low byte
    return val & 0xff


def create_drive(speed, radius):
    # Drive using Create's "drive" command
    # speed range -500 to 500 mm/sec
    # print(f'speed  high:low bytes {hex(high_byte(speed))}:{hex(low_byte(speed))}')
    # print(f'radius high:low bytes {hex(high_byte(radius))}:{hex(low_byte(radius))}')
    send_to_create([DRIVE, high_byte(speed), low_byte(speed), high_byte(radius), low_byte(radius)])


def create_dd(l_speed, r_speed):
    # Drive using Create's "drive direct" command
    # Speed range -500 to 500 mm/sec
    # print(f'left  speed high:low bytes {hex(high_byte(l_speed))}:{hex(low_byte(l_speed))}')
    # print(f'right speed high:low bytes {hex(high_byte(r_speed))}:{hex(low_byte(r_speed))}')
    send_to_create([DRIVE_DIRECT, high_byte(r_speed), low_byte(r_speed), high_byte(l_speed), low_byte(l_speed)])


def create_pwm(l_pwm, r_pwm):
    # speed (pwm) range -255 to 255
    # print(f'left  pwm high:low bytes {hex(high_byte(l_pwm))}:{hex(low_byte(l_pwm))}')
    # print(f'right pwm high:low bytes {hex(high_byte(r_pwm))}:{hex(low_byte(r_pwm))}')
    send_to_create([DRIVE_DIRECT, high_byte(r_pwm), low_byte(r_pwm), high_byte(l_pwm), low_byte(l_pwm)])
