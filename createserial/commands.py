"""
Macro-level Create2 functions
"""
from createserial.constants import Opcode, Packet, PowerLED, CHECK_ROBOT__DOCK__SPOT__DEBRIS__ALL_OFF
from createserial.serial import send_to_create, receive_from_create, close_serial
from colorama import Fore
from colorama import init as colorama_init

colorama_init(autoreset=True)

POWER_ON_CREATE_MSG = '\nCheck Create power and cable!!!\n'


def open_create():
    """Open a connection to the Create"""
    # Start dialog with Create - must do this first before sending any other command
    send_to_create([Opcode.START])

    # Turn off the Create's safety features
    send_to_create([Opcode.FULL])

    # Read Create's battery voltage to verify the Create is powered on and communicating
    # "size" is the number of bytes expected in the reply sent by the Create
    size = 2
    send_to_create([Opcode.QUERY, Packet.VOLTAGE])
    data = receive_from_create(size)
    if len(data) == size:
        voltage = float((data[0] << 8) + data[1]) / 1000.0
        battery_voltage_msg(voltage)
    elif len(data) > 0:
        print(Fore.YELLOW + f'\nExpected {size} bytes, got {len(data)}')
    else:
        print(Fore.RED + POWER_ON_CREATE_MSG)
        send_to_create([Opcode.STOP])
        close_serial()
        exit()

    # Set Create's Power LED to yellow
    send_to_create([Opcode.LEDS,
                    CHECK_ROBOT__DOCK__SPOT__DEBRIS__ALL_OFF,
                    PowerLED.YELLOW,
                    PowerLED.INTENSITY_FULL])

    # Set Create's 7-segment LED array to 'CONN' denoting it is connected
    display_on_create('CONN')


def battery_voltage_msg(voltage):
    """Print a battery voltage message"""
    if voltage > 14.4:
        print(Fore.GREEN + f'Create battery is {voltage} Volts\n')
    elif voltage > 14.0:
        print(Fore.YELLOW + f'Create battery is {voltage} Volts - charge now?\n')
    else:
        print(Fore.RED + f'Create battery is {voltage} Volts - charge now!\n')


def close_create():
    """Close a connection to the Create"""
    # Set Create's LEDs and LED array to a default state
    send_to_create([Opcode.LEDS,
                    CHECK_ROBOT__DOCK__SPOT__DEBRIS__ALL_OFF,
                    PowerLED.GREEN,
                    PowerLED.INTENSITY_FULL])

    # Clear Create's 7-segment LED array
    display_on_create('    ')

    # Shut down communications between the Wombat and the Create
    send_to_create([Opcode.STOP])


def display_on_create(msg):
    """Set Create's 7-segment LED array to display msg"""
    msg = msg[0:4]
    cmd = bytearray(' ' + msg, 'utf-8')
    # Insert Create OpCode into fist byte
    cmd[0] = Opcode.LEDS_ASCII
    send_to_create(cmd)


def read_create_encoders():
    """Read Create's left and right wheel encoder values"""
    size = 4
    send_to_create([Opcode.QUERY_LIST, 2, Packet.LEFT_ENCODER, Packet.RIGHT_ENCODER])
    data = receive_from_create(size)
    l_encoder = 0
    r_encoder = 0
    if len(data) == size:
        l_encoder = (data[0] << 8) + data[1]
        r_encoder = (data[2] << 8) + data[3]
    elif len(data) > 0:
        print(Fore.YELLOW + f'\nExpected {size} bytes, got {len(data)}')
    else:
        print(Fore.RED + POWER_ON_CREATE_MSG)
    return l_encoder, r_encoder


class Encoders:
    """Represents the encoders of the Create and handles value wraparound"""

    def __init__(self):
        self.__prev_left, self.__prev_right = self.__get_raw()
        self.__left = self.__right = 0

    @property
    def values(self):
        """The left and right encoder values relative to the robot's start"""
        left, right = self.__get_raw()
        adjusted_left = self.__adjust(left, self.__prev_left)
        adjusted_right = self.__adjust(right, self.__prev_right)
        self.__prev_left, self.__prev_right = left, right
        self.__left += adjusted_left
        self.__right += adjusted_right
        return self.__left, self.__right

    def reset(self):
        """Reset the values back to 0"""
        self.__init__()

    @staticmethod
    def __adjust(value, prev):
        if abs(value - prev) > 32768:
            value = value + 65536 if value < 32768 else value - 65536
        return value - prev

    @staticmethod
    def __get_raw():
        return read_create_encoders()


def _high_byte(val):
    """Extracts high byte"""
    return (val >> 8) & 0xff


def _low_byte(val):
    """Extracts low byte"""
    return val & 0xff


def as_bytes(val):
    """Extracts the value as high and low bytes"""
    return _high_byte(val), _low_byte(val)


def create_drive(speed, radius):
    """
    Drive using Create's "drive" command
    speed range -500 to 500 mm/sec
    """
    send_to_create([Opcode.DRIVE, *as_bytes(_limit(speed, -500, 500)), *as_bytes(radius)])


def create_dd(l_speed, r_speed):
    """
    Drive using Create's "drive direct" command
    Speed range -500 to 500 mm/sec
    """
    send_to_create([Opcode.DRIVE_DIRECT, *as_bytes(_limit(r_speed, -500, 500)), *as_bytes(_limit(l_speed, -500, 500))])


def create_pwm(l_pwm, r_pwm):
    """speed (pwm) range -255 to 255"""
    send_to_create([Opcode.DRIVE_DIRECT, *as_bytes(_limit(r_pwm, -255, 255)), *as_bytes(_limit(l_pwm, -255, 255))])


def _limit(num, minimum, maximum):
    return min(max(minimum, num), maximum)
