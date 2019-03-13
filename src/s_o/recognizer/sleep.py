import time


def sleep_ms(delay=100):
    if not delay: return
    time.sleep(delay / 1000)