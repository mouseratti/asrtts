from time import sleep
from threading import Lock, Timer


def sleep_ms(delay=100):
    if not delay: return
    sleep(delay / 1000)



class Timeout():
    _timer: Timer
    _is_timeout: bool
    _mutex : Lock
    _millis: int

    def __init__(self, millis: int =10, start_now: bool =True):
        self._is_timeout = False
        self._mutex = Lock()
        self._millis = millis
        self._set_timer()
        if start_now: self.start()

    def _set_timer(self):
        with self._mutex: self._timer = Timer(self._millis * 0.001, self._set_timedout)


    @property
    def is_timeout(self) -> bool:
        return self._is_timeout

    def _set_timedout(self):
        with self._mutex: self._is_timeout = True


    def start(self):
        with self._mutex: self._timer.start()

    def restart(self):
        self._timer.cancel()
        self._set_timer()
        self.start()

    def cancel(self):
        self._timer.cancel()

