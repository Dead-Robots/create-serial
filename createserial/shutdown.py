from threading import Thread
from time import sleep, time
from createserial.commands import close_create
from createserial.serial import close_serial, ser

def shutdown_create_in(seconds):
    t = Thread(target=thread_main, args=(seconds,), daemon=True)
    t.start()

def thread_main(seconds):
    start = time()
    sleep(seconds)
    print("Time for create to shutdown...")
    if ser.is_open:
        close_create()
        close_serial()
    print("Create base shutdown after", round(time()-start, 2), "seconds")
