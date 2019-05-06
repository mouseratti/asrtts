# -*- coding: utf-8 -*-
import json
from collections import namedtuple
from datetime import datetime
from os import path, mkdir
from subprocess import Popen, PIPE
from threading import Thread, Lock
from time import sleep
from uuid import uuid4
import traceback
import yaml

# PARAMS
ASR_WORKING_DIRECTORY = "/opt/naumen/nauphone/spool/naubuddy/ivr/ASRTTS"
ASR_MAX_TIMEOUT_DEFAULT = 10000
ASR_RECOGNIZER_UTILITY = "python36 -m s_o.recognizer"
ENV = {
    "GOOGLE_APPLICATION_CREDENTIALS": "/home/voip/gac.json"
}
Configuration = namedtuple("Configuration", (
    "duration",
    "fragments_count",
    "min_confidence",
    "max_timeout",
))


class Asr:
    _ASR_RECOGNITION_RESULTS = {}
    _ASR_LOCK = Lock()

    def _asr_debug(self, message):
        self.buddy.sayDebugMessage("ASR {}: {}".format(datetime.now(), message))
        return

    @staticmethod
    def sleep_ms(time_to_sleep_ms):
        sleep(0.001 * time_to_sleep_ms)

    def _asr_format_filename(self, task, fragment):
        return path.join(self._asr_format_dirname(task), "{:0>4}.raw".format(fragment))

    def _asr_format_dirname(self, task):
        return path.join(ASR_WORKING_DIRECTORY, task)

    def _asr_get_deferred(self, task):
        return self._ASR_RECOGNITION_RESULTS.get(task)

    def _asr_put_deferred(self, result):
        assert (isinstance(result, dict))
        if result:
            with self._ASR_LOCK:
                self._ASR_RECOGNITION_RESULTS.update(result)

    def _asr_is_finished(self, task):
        popen = self._asr_get_deferred(task)
        return popen is not None and popen.poll() is not None

    def ASR_RUN(self, config_path):
        '''ENTRYPOINT FOR IVR'''
        try:
            return self._asr_run(config_path)
        except Exception as e:
            self._asr_debug("error on recognize: {}".format(e))
            self._asr_debug(traceback.format_exc())

    def _asr_run(self, config_path):
        config = self._asr_read_config(config_path)
        task = self._asr_generate_name()
        self._asr_record_audio(task, config)
        self._asr_start_recognition(task, config_path)
        return self._asr_poll_result(task, config)

    def _asr_read_config(self, filename):
        with open(filename) as file:
            cfg_dict = yaml.safe_load(file)
        self._asr_debug("cfg_dict {}".format(cfg_dict))
        cfg = Configuration(
            cfg_dict.get("duration"),
            cfg_dict.get("fragments_count"),
            cfg_dict.get("min_confidence"),
            cfg_dict.get("max_timeout"),
        )
        for key in cfg:
            if key is None:
                raise Exception("Invalid configuration!!! {}".format(cfg))
        return cfg

    @staticmethod
    def _asr_generate_name():
        """First step. generate name"""
        return str(uuid4())

    def _asr_record_audio(self, task, config):
        """2nd step. Start record files"""
        full_dirname = self._asr_format_dirname(task)
        mkdir(full_dirname)
        def record():
            fragments_count = config.fragments_count
            fragment_duration = config.duration / float(fragments_count)
            for fragment_number in range(fragments_count):
                if self._asr_is_finished(task):
                    self._asr_debug("{} is finished. stopping record new fragments..")
                    break
                filename = self._asr_format_filename(task, fragment_number)
                self.startRecord(filename)
                self.sleep_ms(fragment_duration)
                self.stopRecord()

        Thread(target=record).start()

    def _asr_start_recognition(self, task, config_path):
        """3rd step. start recognition"""
        Thread(target=self._asr_run_recognizer, args=(task, config_path)).start()

    def _asr_poll_result(self, task, config):
        """4th step. poll result"""
        timeout = config.max_timeout
        while timeout > 0:
            popen = self._asr_get_deferred(task)
            if popen is not None:
                if popen.poll() is not None: break
            self.sleep_ms(100)
            timeout -= 100
        return self._asr_handle_recognizer_process(popen)

    def _asr_run_recognizer(self, task, config_path):
        self.sleep_ms(1000)
        cmd = self._prepare_exec_string(task, config_path)
        self._asr_debug("run {}".format(cmd))
        self._asr_put_deferred({task: Popen(cmd.split(), env=ENV, stdout=PIPE, stderr=PIPE)})

    def _prepare_exec_string(self, task, config_path):
        return "{} -d {} -c {}".format(
            ASR_RECOGNIZER_UTILITY,
            self._asr_format_dirname(task),
            config_path
        )

    def _asr_handle_recognizer_process(self, popen):
        if popen is None: raise Exception("popen is None!!! can not found recognizer process")
        if popen.poll() is None:
            self._asr_debug("{} is still running, will be killed...".format(popen))
            popen.kill()
            raise Exception("recognizer is frozen!")
        if popen.poll() != 0:
            stderr = popen.stderr.read()
            raise Exception("recognizer returned an error!!! {}".format(stderr))
        stdout = popen.stdout.read()
        self._asr_debug("stdout from recognizer {}".format(stdout))
        return parse_output(stdout)


def parse_output(output):
    output = output.decode()
    parsed = json.loads(output)
    return parsed.get("PHRASE"), parsed.get("CONFIDENCE")
