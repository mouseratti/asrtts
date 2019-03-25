from time import sleep
from unittest import TestCase
from s_o.recognizer.timeouts import Timeout


class TestTimeout(TestCase):
    timeout : Timeout = None


    def setUp(self):
        self.timeout = Timeout(400)

    def test_start_timer_works_as_expected(self):
        sleep(0.1)
        self.assertFalse(self.timeout.is_timeout)
        sleep(0.3)
        self.assertTrue(self.timeout.is_timeout)

    def test_restart(self):
        sleep(0.2)
        self.timeout.restart()
        sleep(0.3)
        self.assertFalse(self.timeout.is_timeout)