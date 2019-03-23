# -*- coding: utf-8 -*-
import json
from time import sleep
from collections import namedtuple
from subprocess import Popen, PIPE
from os import path, mkdir
from threading import Thread, Lock
from uuid import uuid4
from datetime import datetime

# PARAMS
ASR_WORKING_DIRECTORY = "ASR_RECORDS"
ASR_DIRNAME_TEMPLATE = "{}/"
ASR_RECOGNITION_TIMEOUT_MS = 4000
ASR_WORKING_DIRECTORY_PREFIX="/opt/naumen/nauphone/spool/naubuddy/ivr/"
ASR_RECOGNIZER_UTILITY = "python36 -m s_o.recognizer -d"

RecognitionResult = namedtuple("RecognitionResult", ("PHRASE", "CONFIDENCE", "ERROR"))
class Asr:
    _ASR_RECOGNITION_RESULTS = {}
    _ASR_LOCK = Lock()

    @staticmethod
    def sleep_ms(time_to_sleep_ms):
        sleep(0.001 * time_to_sleep_ms)

    def _asr_get_deferred(self, filename):
        return self._ASR_RECOGNITION_RESULTS.get(filename)

    def _asr_put_deferred(self, result):
        with self._ASR_LOCK:
            self._ASR_RECOGNITION_RESULTS.update(result)

    @staticmethod
    def asr_generate_name():
        """First step. generate name"""
        filename = ASR_DIRNAME_TEMPLATE.format(str(uuid4()))
        return path.join(ASR_WORKING_DIRECTORY, filename)

    def asr_record_to_dir(self, dirname, fragment_duration_ms = 1500, fragments=2):
        """2nd step. Start record files"""
        dirname = self._asr_get_fullname(dirname)
        mkdir(dirname)
        def record():
            for fragment in range(fragments):
                filename = path.join(dirname,"{:0>3}.raw".format(fragment))
                self.startRecord(filename)
                self.sleep_ms(fragment_duration_ms)
                self.stopRecord()
        # TODO: stop recording if recognize result has already been given
        Thread(target=record).start()



    def asr_start_recognition(self, filename):
        """3rd step. start recognition"""
        self.buddy.sayDebugMessage(
            "{} asr_start_recognition {}".format(datetime.now(), filename)
        )
        Thread(target=self._asr_run_recognizer, args=(filename,)).start()


    def asr_poll_result(self, filename, timeout = ASR_RECOGNITION_TIMEOUT_MS):
        """4th step. poll result"""
        self.buddy.sayDebugMessage(
            "{} asr_poll_result {}".format(datetime.now(), timeout)
        )
        while timeout > 0:
            popen = self._asr_get_deferred(filename)
            if popen is not None:
                if popen.poll() is not None:
                    self.buddy.sayDebugMessage("popen.poll is {}".format(popen.poll()))
                    break
            self.sleep_ms(100)
            timeout -= 100
        result = self._asr_handle_recognizer_process(popen)
        return tuple(result)


    def _asr_run_recognizer(self, filename):
        self.sleep_ms(1000)
        cmd = self._prepare_exec_string(filename)
        self.buddy.sayDebugMessage("trying to run cmd {}".format(cmd))
        self._asr_put_deferred({filename: Popen(cmd.split(),stdout=PIPE, stderr=PIPE)})

    def _prepare_exec_string(self, name):
        return "{} {}".format(ASR_RECOGNIZER_UTILITY, self._asr_get_fullname(name))

    @staticmethod
    def _asr_get_fullname(dirname):
        return path.join(ASR_WORKING_DIRECTORY_PREFIX, dirname)

    def _asr_handle_recognizer_process(self, popen):
        if popen is None: return RecognitionResult(None, None, "No such key!!!")
        if popen.poll() is None:
            self.buddy.sayDebugMessage("process is still running, will be killed...")
            popen.kill()
            return RecognitionResult(None, None, "TimeoutError")
        if popen.poll() != 0:
            stderr = popen.stderr.read()
            self.buddy.sayDebugMessage("recognizer stderr: {}".format(stderr))
        try:
            stdout = popen.stdout.read()
            self.buddy.sayDebugMessage("stdout from recognizer {}".format(stdout))
            return parse_output(stdout)
        except Exception as e:
            return RecognitionResult(None, None, "ParseResultError: {}".format(e))


def parse_output(output):
    output = output.decode()
    parsed = json.loads(output)
    return RecognitionResult(
        parsed.get("PHRASE"),
        parsed.get("CONFIDENCE"),
        parsed.get("ERROR"),
    )
