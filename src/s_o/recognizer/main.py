import json
from typing import List, Generator, ByteString
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
        recognition_config: types.StreamingRecognitionConfig,
        max_duration_millis = 10000,
        next_phrase_timeout_millis = 3000,
    ) -> Generator[types.SpeechRecognitionAlternative, None, None]:
    """Streams transcription of the given audio file."""
    requests = (types.StreamingRecognizeRequest(audio_content=chunk) for chunk in bytestream)
    responses = client.streaming_recognize(
        get_streaming_recognition_config(recognition_config),
        requests
    )
    max_duration_timeout = Timeout(max_duration_millis)
    next_phrase_timeout = Timeout(next_phrase_timeout_millis, start_now=False)
    while not (max_duration_timeout.is_timeout or next_phrase_timeout.is_timeout):
        try:
            resp = next(responses)
        except StopIteration:
            logger.info("no more responses!")
            break
        logger.debug("reading next response; results is {}".format(resp.results))
        if resp.results:
            final = [x for x in resp.results if x.is_final]
            if final:
                try:
                    next_phrase_timeout.restart()
                    yield final[0].alternatives[0]
                except IndexError:
                    logger.warning("no any SpeechRecognitionAlternative for response {}".format(resp.results))
    logger.info("recognize_stream timed out...")


def format_recognition_result(args: List[types.SpeechRecognitionAlternative]) -> RecognitionResult:
    phrase = " ".join(arg.transcript for arg in args)
    confidence = sum(arg.confidence for arg in args) / len(args)
    return RecognitionResult(phrase, confidence)

def to_json(r: RecognitionResult) -> str:
    output_dict = {"PHRASE": r.PHRASE, "CONFIDENCE": r.CONFIDENCE}
    return json.dumps(output_dict)


def main():
    try:
        params = get_params()
        logger.debug("start new session! params {}".format(params))
        google_client = speech.SpeechClient()
        alternatives_list: List[types.SpeechRecognitionAlternative] = recognize_stream(
            read_files(get_files_from_directory(params.directory)),
            google_client,
            get_streaming_recognition_config(get_recognition_config()),
            params.duration,
            params.next_phrase_timeout
        )
        result = format_recognition_result([_ for _ in alternatives_list])
        jsoned = to_json(result)
        logger.debug("result is {}".format(jsoned))
        print(jsoned)
    except Exception as e:
        logger.exception("error on recognize", exc_info=True)
        raise Exception