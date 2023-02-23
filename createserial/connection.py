from createserial.serial import open_serial, close_serial
from createserial.commands import open_create, close_create, reset_create


def connect():
    """Connect to the create in a safe manner"""
    open_serial()  # open a serial port connection to the Create
    reset_create()  # reset Create to start with a clean slate
    open_create()  # initialize the Create
    

def disconnect():
    """Disconnect from the create in a safe manner"""
    close_create()
    close_serial()

class CreateConnection:
    """Allow for use the with statement for Create connections"""
    def __init__(self):
        pass

    def __enter__(self):
        connect()
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        disconnect()
