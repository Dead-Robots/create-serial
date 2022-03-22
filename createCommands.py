from myserial import send_to_create, receive_from_create, close_serial
import constants as c

POWER_ON_CREATE_MSG = '\n!!! Check Create power and cable !!!\n'


def open_create():
    # Start dialog with Create - must do this first before sending any other command
    send_to_create([c.START])

    # Turn off the Create's safety features
    send_to_create([c.FULL])

    # Read Create's battery voltage to verify the Create is powered on and communicating
    # "size" is the number of bytes expected in the reply sent by the Create
    size = 2
    print('Create battery: ', end='')
    send_to_create([c.QUERY, c.VOLTAGE])
    data = receive_from_create(size)
    if len(data) == size:
        print('{} Volts'.format(float((data[0] << 8) + data[1]) / 1000.0))
    elif len(data) > 0:
        print('\nExpected {} bytes, got {}'.format(size, len(data)))
    else:
        print(POWER_ON_CREATE_MSG)
        send_to_create([c.STOP])
        close_serial()
        exit()

    # Set Create's Power LED to yellow
    send_to_create([c.LEDS,
                    c.CHECK_ROBOT__DOCK__SPOT__DEBRIS__ALL_OFF,
                    c.POWER_LED_YELLOW,
                    c.POWER_LED_INTENSITY_FULL])

    # Set Create's 7-segment LED array to 'CONN' denoting it is connected
    display_on_create('CONN')


def close_create():
    # Set Create's LEDs and LED array to a default state
    send_to_create([c.LEDS,
                    c.CHECK_ROBOT__DOCK__SPOT__DEBRIS__ALL_OFF,
                    c.POWER_LED_GREEN,
                    c.POWER_LED_INTENSITY_FULL])

    # Clear Create's 7-segment LED array
    display_on_create('    ')

    # Prepare to disconnect from the Create - not needed?
    # send_to_create([c.SAFE])

    # Tell Create to power down
    # send_to_create([c.POWER])

    # Shut down communications between the Wombat and the Create
    send_to_create([c.STOP])


def display_on_create(msg):
    # Set Create's 7-segment LED array to display msg
    msg = msg[0:4]
    cmd = bytearray(' ' + msg, 'utf-8')
    # Insert Create OpCode into fist byte
    cmd[0] = c.LEDS_ASCII
    send_to_create(cmd)


def read_create_encoders():
    # Read Create's left and right wheel encoder values
    size = 4
    send_to_create([c.QUERY_LIST, 2, c.LEFT_ENCODER, c.RIGHT_ENCODER])
    data = receive_from_create(size)
    if len(data) == size:
        print('Left  Encoder Count: ', (data[0] << 8) + data[1])
        print('Right Encoder Count: ', (data[2] << 8) + data[3])
    elif len(data) > 0:
        print('\nExpected {} bytes, got {}'.format(size, len(data)))
    else:
        print(POWER_ON_CREATE_MSG)


# Deprecate?
def convert_int_to_bytes(val):
    # splits "val" into high and low bytes
    high_byte = (val >> 8) & 0xff
    low_byte = val & 0xff
    return [high_byte, low_byte]


def create_drive(speed, radius):
    # Drive using Create's "drive" command
    # print("speed in bytes high,low {},{}".format(hex((speed >> 8) & 0xff), hex(speed & 0xff)))
    # print("radius in bytes high,low {},{}".format(hex((radius >> 8) & 0xff), hex(radius & 0xff)))
    send_to_create([c.DRIVE, (speed >> 8) & 0xff, speed & 0xff, (radius >> 8) & 0xff, radius & 0xff])


def create_dd(l_speed, r_speed):
    # Drive using Create's "drive direct" command
    # Speed range -500 to +500 mm/sec
    # print("left in bytes high, low {}, {}".format(hex((l_speed >> 8) & 0xff), hex(l_speed & 0xff)))
    # print("right in bytes high, low {}, {}".format(hex((r_speed >> 8) & 0xff), hex(r_speed & 0xff)))
    send_to_create([c.DRIVE_DIRECT, (r_speed >> 8) & 0x0ff, r_speed & 0xff, (l_speed >> 8) & 0xff, l_speed & 0xff])


def create_pwm(l_pwm, r_pwm):
    # speed (pwm) range -255 to + 255
    # print("left in bytes high, low {}, {}".format(hex(l_pwm_bytes[0]), hex(l_pwm_bytes[1])))
    # print("right in bytes high, low {}, {}".format(hex(r_pwm_bytes[0]), hex(r_pwm_bytes[1])))
    send_to_create([c.DRIVE_PWM, (r_pwm >> 8) & 0xff, r_pwm & 0xff, (l_pwm >> 8) & 0xff, l_pwm & 0xff])
