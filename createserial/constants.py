from enum import IntEnum


class Opcode(IntEnum):
    """Create Opcodes"""
    RESET = 7
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


class Packet(IntEnum):
    """Create Sensor Packet numbers"""
    VOLTAGE = 22
    LEFT_ENCODER = 43
    RIGHT_ENCODER = 44
    LEFT_CLIFF = 9
    RIGHT_CLIFF = 12
    LEFT_CLIFF_SIGNAL = 28
    RIGHT_CLIFF_SIGNAL = 31


class PowerLED(IntEnum):
    """Create Power LED values"""
    GREEN = 0
    YELLOW = 64
    INTENSITY_OFF = 0
    INTENSITY_FULL = 255


# Create's Other LEDs
CHECK_ROBOT__DOCK__SPOT__DEBRIS__ALL_OFF = 0
