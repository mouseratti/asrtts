from os import listdir, path
from typing import ByteString
from typing import Generator
from typing import IO

from s_o.recognizer.sleep import sleep_ms
from s_o.recognizer.log import configure_log

logger = configure_log(__name__)

FILE_READ_DELAY_MS = 100

def read_files(files: Generator[IO, None, None]) -> Generator[ByteString, None, None]:
    for f in files: yield from read_file(f)

def read_file(file: IO, delay_ms = 20, buffer_size = 5000) -> Generator[ByteString, None, None]:
        counter = 0
        while True:
            buffer = file.read(buffer_size)
            logger.debug("file {} read {} bytes".format(file, len(buffer)))
            if not buffer:
                counter += 1
                if counter > 10:
                    break
                continue
            yield buffer

def get_files_from_directory(directory: str) -> Generator[IO, None, None]:
    for filename in _get_next_filename(directory):
        with open(filename, "rb") as f:
            yield f


def _get_next_filename(directory: str, timeout=3000) -> Generator[str, None, None]:
    processed = set()
    timeout_per_file = timeout
    while True:
        if timeout_per_file <= 0: break
        files = set(listdir(directory)) - processed
        if files:
            for f in sorted(files):
                filename = path.join(directory, f)
                logger.debug("found {}".format(filename))
                yield filename
                processed.add(f)
        else:
            sleep_ms(FILE_READ_DELAY_MS)
            timeout_per_file -= FILE_READ_DELAY_MS
