from unittest import TestCase
from .asr import Asr
from unittest import mock

class TestAsr(TestCase):

    def setUp(self):
        self.asr = Asr()
        self.asr.buddy = mock.Mock()


    def test__asr_debug(self):
        msg = "test message"
        self.asr._asr_debug(msg)
        self.asr.buddy.sayDebugMessage.assert_called_once()

    def test__asr_format_filename(self):
        task, fragment  = "task", 5
        self.assertEquals(self.asr._asr_format_filename(task, fragment))

    def test__asr_format_dirname(self):
        self.fail()

    def test__asr_get_deferred(self):
        self.fail()

    def test__asr_put_deferred(self):
        self.fail()

    def test__asr_is_finished(self):
        self.fail()

    def test_ASR_RUN(self):
        self.fail()

    def test__asr_run(self):
        self.fail()

    def test__asr_read_config(self):
        self.fail()

    def test__asr_generate_name(self):
        self.fail()

    def test__asr_record_audio(self):
        self.fail()

    def test__asr_start_recognition(self):
        self.fail()

    def test__asr_poll_result(self):
        self.fail()

    def test__asr_run_recognizer(self):
        self.fail()

    def test__prepare_exec_string(self):
        self.fail()

    def test__asr_handle_recognizer_process(self):
        self.fail()
