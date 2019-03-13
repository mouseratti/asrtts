import json
from collections import namedtuple
from sys import exit

from google.cloud import speech
from google.cloud.speech import types

from s_o.recognizer.configs import get_recognition_config, get_streaming_recognition_config
from s_o.recognizer.io import read_files, get_files_from_directory
from s_o.recognizer.params import get_params, set_environment_variables
from s_o.recognizer.log import configure_log

logger = configure_log()

RecognitionResult = namedtuple("RecognitionResult", ("PHRASE", "CONFIDENCE", "ERROR"))



def recognize_stream(stream_generator, client, recognition_config):
    """Streams transcription of the given audio file."""
    requests = (types.StreamingRecognizeRequest(audio_content=chunk) for chunk in stream_generator)
    responses = client.streaming_recognize(
        get_streaming_recognition_config(recognition_config),
        requests
    )
    for response in responses:
        logger.debug(response)
        for result in response.results:
            logger.debug(result)
            if result.is_final:
                return result.alternatives


def build_result(*args) -> RecognitionResult:
    logger.debug(args)
    if 3 == len(args):
        return RecognitionResult(*args)
    if 1 == len(args):
        result = args[0]
        if result is None: return RecognitionResult(None, 0, None)
        most_likely = result[0]
        return RecognitionResult(most_likely.transcript, most_likely.confidence, None)


def to_json(r: RecognitionResult) -> str:
    output_dict = {"PHRASE": r.PHRASE, "CONFIDENCE": r.CONFIDENCE, "ERROR": r.ERROR}
    return json.dumps(output_dict)


def main():
    set_environment_variables()
    params = get_params()
    try:
        google_client = speech.SpeechClient()
        chunks = read_files(get_files_from_directory(params.directory))
        recognized = recognize_stream(chunks, google_client, get_recognition_config())
        result = build_result(recognized)
        logger.debug("build_result is {}".format(result))
    except Exception as e:
        logger.exception("error on recognize", exc_info=True)
        result = build_result(None, None, str(e))

    jsoned = to_json(result)
    print(jsoned)
    if result.ERROR is not None: exit(777)


