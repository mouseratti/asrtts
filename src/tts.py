# -*- coding: utf-8 -*-
from subprocess import Popen, PIPE
import json
TTS_TRANSLATOR = "tts"
TTS_OUTPUT_DIRECTORY = "/opt/naumen/nauphone/spool/naubuddy/ivr/ASRTTS"
TIMEOUT_MS = 10000
ENVIRONMENT = {
    "GOOGLE_APPLICATION_CREDENTIALS": "/home/voip/gac.json"
}

class Tts():

    def _tts_log(self, message):
        self.buddy.sayDebugMessage("TTS: {}".format(message))
        return

    def tts_play_phrase(self, phrase):
        """1. Call this method to play phrase with Google TTS API"""
        try:
            filename = self._tts_execute_translator(phrase)
            if filename is None:
                raise Exception("General Error!!! filename is None!")
            self._tts_play_filename(filename)
            return 0
        except Exception as e:
            self._tts_log("error on tts_play_phrase {}".format(e))
            return 1


    def _tts_play_filename(self, filename):
        self.playFile(filename) # playFile is a method of Base class


    def _tts_format_command(self, phrase):
        return '''{} --dir {} "{}" '''.format(TTS_TRANSLATOR, TTS_OUTPUT_DIRECTORY, phrase)

    def _tts_execute_translator(self, phrase):
        cmd = self._tts_format_command(phrase)
        popen = Popen(cmd, shell=True, env=ENVIRONMENT, stdout=PIPE, stderr=PIPE)
        popen.command = cmd
        timeout = TIMEOUT_MS
        while True or timeout > 0:
            if popen.poll() is not None:
                break
            self.sleep_ms(100)
            timeout -= 100
        return self._tts_handle_popen(popen)


    def _tts_handle_popen(self, popen):
        if popen.poll() is None:
            popen.kill()
            raise TimeoutError("{} executed too long!!".format(popen.command))
        if 0 != popen.poll():
            self._tts_log("popen stderr {}".format(popen.stderr.read().decode()))
            raise RuntimeError("{} returned code {}".format(popen.command, popen.poll()))
        stdout = popen.stdout.read()
        return self._tts_parse_stdout(stdout)

    def _tts_parse_stdout(self, stdout):
        stdout = stdout.decode()
        try:
            return json.loads(stdout).get('filename')
        except Exception as e:
            self._tts_log("error on deserialisation: {}".format(e))
            return None