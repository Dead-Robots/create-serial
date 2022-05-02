import atexit
import signal
from createserial.commands import close_create
from createserial.serial import close_serial, ser

def handle_exit():
    print("Exiting")
    if ser.is_open:
        close_create()
        close_serial()

def handle_exit_dirty(*args):
    print("Exiting,", args)
    handle_exit()
    exit(23)

atexit.register(handle_exit)
signal.signal(signal.SIGTERM, handle_exit_dirty)
signal.signal(signal.SIGINT, handle_exit_dirty)
