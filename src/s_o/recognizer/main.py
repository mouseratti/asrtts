import json
from typing import List, Generator, ByteString
from queue import Queue, Empty
from threading import Thread
from collections import namedtuple
from google.cloud import speech
from google.cloud.speech import types

from s_o.recognizer.tts_configs import get_recognition_config, get_streaming_recognition_config
from s_o.recognizer.iofunctions import read_files, get_files_from_directory
from s_o.recognizer.log import configure_log
from s_o.recognizer.params import get_params
from s_o.recognizer.timeouts import Timeout

logger = configure_log()

RecognitionResult = namedtuple("RecognitionResult", ("PHRASE", "CONFIDENCE"))


def recognize_stream(
        bytestream: Generator[ByteString, None, None],
        client:speech.SpeechClient,
        recognition_config: types.RecognitionConfig,
        q: Queue
    ):
    """Streams transcription of the given audio file."""
    requests = (types.StreamingRecognizeRequest(audio_content=chunk) for chunk in bytestream)
    responses = client.streaming_recognize(
        get_streaming_recognition_config(recognition_config),
        requests
    )
    while True:
        try:
            resp = next(responses)
            logger.debug("reading next response; resp.results is {}".format(resp.results))
        except StopIteration:
            logger.info("no more responses!")
            break
        if resp.results:
            final = [x for x in resp.results if x.is_final]
            if final:q.put(final[0].alternatives[0])
    logger.info("exit from recognize_stream!")
    return

def format_recognition_result(args: List[types.SpeechRecognitionAlternative]) -> RecognitionResult:
    phrase = " ".join(arg.transcript for arg in args)
    confidence = sum(arg.confidence for arg in args) / len(args)
    return RecognitionResult(phrase, confidence)

def to_json(r: RecognitionResult) -> str:
    output_dict = {"PHRASE": r.PHRASE, "CONFIDENCE": r.CONFIDENCE}
    return json.dumps(output_dict)

def read_queue(q: Queue, output: List, params) -> None:
    duration_timeout = Timeout(params.duration)
    next_phrase_timeout = Timeout(params.next_phrase_timeout, start_now=False)
    while not (next_phrase_timeout.is_timeout or duration_timeout.is_timeout):
        while not q.empty():
            output.append(q.get())
            next_phrase_timeout.restart()
    logger.debug("duration_timeout: {}".format(duration_timeout.is_timeout))
    logger.debug("next_phrase_timeout: {}".format(next_phrase_timeout.is_timeout))
    duration_timeout.cancel()
    next_phrase_timeout.cancel()
    return


def main():
    try:
        params = get_params()
        logger.debug("start new session! params {}".format(params))
        google_client = speech.SpeechClient()
        alternatives_queue = Queue()
        Thread(target=recognize_stream, args=(
            read_files(get_files_from_directory(params.directory)),
            google_client,
            get_recognition_config(),
            alternatives_queue
            ),
            daemon=True
        ).start()
        recognized_results = list()
        read_queue(alternatives_queue, recognized_results, params)
        result = format_recognition_result(recognized_results)
        jsoned = to_json(result)
        logger.debug("result is {}".format(jsoned))
        print(jsoned)
        logger.debug("exit from main!")
        exit(0)
    except Exception as e:
        logger.exception("error on recognize", exc_info=True)
        print("error on recognize! {}".format(e))
        exit(3)