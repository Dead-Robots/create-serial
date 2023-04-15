import atexit
import signal
from createserial.connection import disconnect


def handle_exit():
    print("Exiting")
    disconnect()


def handle_exit_dirty(*args):
    print("Exiting,", args)
    handle_exit()
    exit(42)


atexit.register(handle_exit)
signal.signal(signal.SIGTERM, handle_exit_dirty)
signal.signal(signal.SIGINT, handle_exit_dirty)
