from multiprocessing import Process, Event
from os import getpid, kill
from time import sleep


class Watcher:
    def __init__(self):
        self._stop_event = Event()
        self._proc = Process(target=self._watcher_function, args=(getpid(), self._stop_event), daemon=False)

    def start(self):
        self._proc.start()

    def signal(self):
        self._stop_event.set()

    @staticmethod
    def check_pid(pid):
        """
        Check For the existence of a unix pid.
        Source: https://stackoverflow.com/questions/568271/how-to-check-if-there-exists-a-process-with-a-given-pid-in-python
        """
        try:
            kill(pid, 0)
        except OSError:
            return False
        else:
            return True

    def _watcher_function(self, watch_pid, event):
        import sys
        with open("/log.log", "w+") as sys.stdout:
            while self.check_pid(watch_pid) and not event.is_set():
                sleep(0.25)
            if not event.is_set():
                from createserial.serial import open_serial
                from createserial.connection import disconnect
                open_serial()
                disconnect()
