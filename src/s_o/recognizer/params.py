import argparse
import os
from collections import namedtuple
from pathlib import Path

Params = namedtuple("Params",
                    (
                        "directory",
                        "confidence_threshold",
                    ))


def get_params() -> Params:
    confidence_threshold = float(os.getenv("RECOGNIZER_CONFIDENCE_THRESHOLD", 0.4))
    parser = get_parser()
    parsed_args = parser.parse_args()
    directory = parsed_args.directory
    return Params(directory, confidence_threshold)


def get_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="recognizer",
        description='Recognize speech from raw audio file'
    )
    parser.add_argument(
        '-d',
        dest='directory',
        metavar='directory',
        type=str,
        required=True,
        help='directory with files for recognition'
    )
    return parser


def set_environment_variables():
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.path.join(Path.home(), "gac.json")
