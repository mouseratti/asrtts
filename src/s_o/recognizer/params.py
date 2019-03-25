import yaml
import argparse
from typing import IO
from collections import namedtuple

Params = namedtuple("Params",
                    (
                        "directory",
                        "confidence_threshold",
                        "duration",
                        "next_phrase_timeout",
                    ))

Configuration = namedtuple("Configuration",
                    (
                        "confidence_threshold",
                        "duration",
                        "next_phrase_timeout",
                    ))


class WrongConfigurationError(RuntimeError): pass

def get_params() -> Params:
    parser = get_parser()
    parsed_args = parser.parse_args()
    directory = parsed_args.directory
    with open(parsed_args.configfile) as file:
        configuration: Configuration = parse_config(file)
    return Params(
        directory,
        configuration.confidence_threshold,
        configuration.duration,
        configuration.next_phrase_timeout,
        )


def parse_config(file: IO) -> Configuration:
    keys_from_yaml: dict = yaml.safe_load(file)
    cfg: Configuration = Configuration(
        keys_from_yaml.get("confidence_threshold"),
        keys_from_yaml.get("duration"),
        keys_from_yaml.get("next_phrase_timeout"),
    )
    for elem in cfg:
        if elem is None: raise WrongConfigurationError("{} has undefined elements!!!".format(cfg))
    return cfg



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
    parser.add_argument(
        '-c',
        dest='configfile',
        metavar='configfile',
        type=str,
        required=True,
        help='recognition config'
    )
    return parser
