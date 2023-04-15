from threading import Thread
from time import sleep, time
from createserial.commands import close_create, create_dd
from createserial.serial import close_serial, ser
from kipr import shut_down_in


def shutdown_create_in(seconds):
    t = Thread(target=thread_main, args=(seconds,), daemon=True)
    t.start()


def thread_main(seconds):
    start = time()
    sleep(seconds)
    print("Time for create to shutdown...")
    if ser.is_open:
        create_dd(0, 0)
        close_create()
        close_serial()
    print("Create base shutdown after", round(time() - start, 2), "seconds")
    shut_down_in(0)  # shutdown the wombat
