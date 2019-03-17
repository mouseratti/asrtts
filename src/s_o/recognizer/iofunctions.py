from os import listdir, path
from typing import ByteString
from typing import Generator
from typing import IO

from s_o.recognizer.sleep import sleep_ms
from s_o.recognizer.log import configure_log

logger = configure_log(__name__)

FILE_READ_DELAY_MS = 100

def read_files(files: Generator[IO, None, None]) -> Generator[ByteString, None, None]:
    for f in files: yield from read_file_full(f)

# def read_file(file: IO, buffer_size = 5000) -> Generator[ByteString, None, None]:
#         counter = 0
#         while True:
#             buffer = file.read(buffer_size)
#             if not buffer:
#                 counter += 1
#                 if counter > 3:
#                     break
#                 continue
#             yield buffer

def read_file_full(file: IO) -> Generator[ByteString, None, None]:
    buffer = file.read()
    logger.debug("read {} bytes from file {}".format(len(buffer), file))
    if not buffer:
        sleep_ms(FILE_READ_DELAY_MS)
        buffer = file.read()
        logger.debug("read {} bytes from file {} after pause!".format(len(buffer), file))
    yield buffer

def get_files_from_directory(directory: str) -> Generator[IO, None, None]:
    for filename in _get_next_filename(directory):
        with open(filename, "rb") as f:
            yield f


def _get_next_filename(directory: str, timeout=2000) -> Generator[str, None, None]:
    processed = set()
    timeout_per_file = 0
    while True:
        if timeout_per_file >= timeout:
            logger.warn("timeout! processed files {}".format(sorted(processed)))
            break
        files = set(listdir(directory)) - processed
        if files:
            timeout_per_file = 0
            for f in sorted(files):
                filename = path.join(directory, f)
                logger.debug("found {}".format(filename))
                yield filename
                processed.add(f)
        else:
            sleep_ms(FILE_READ_DELAY_MS)
            timeout_per_file += FILE_READ_DELAY_MS
    logger.debug("no more files!!! exit from _get_next_filename")
